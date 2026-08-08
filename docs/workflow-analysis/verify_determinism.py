#!/usr/bin/env python3
"""A7b — MEASURE determinism on the flagless opponent candidates.

Series rule 4: determinism is a measured property, not a code-read one.
The research arm's grep triage eliminated opp_v39 / opp_v44 (random.shuffle)
and passed six as clean. A grep cannot see dict/set iteration order over
nondeterministically-ordered inputs, engine-side variation the bot amplifies,
or timing-dependent branches. This closes the empirical half.

Test: play the SAME (map, seed, seat) N times at --tle 0 against the measured
deterministic reference (opp_v63) and require a byte-identical end state every
time. Any divergence => nondeterministic. Identical across all configs =>
deterministic on the tested configurations (necessary, not sufficient, but it
is the same standard opp_v63 itself was held to).

Read-only: plays matches, writes nothing outside this folder.
Usage: python3 verify_determinism.py [reps] [configs]
"""
from __future__ import annotations

import json
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path("/Users/junghard/Projects/Work/florent-code-game")
FCODE = ROOT / ".venv" / "bin" / "fcode"
REFERENCE = "bots/opp_v63"          # det.py's measured deterministic reference
CANDIDATES = ["bots/opp_v45", "bots/opp_v49", "bots/opp_v50",
              "bots/opp_v56", "bots/opp_v58"]
# controls: starter is the documented counterexample (must FAIL);
# opp_v63 vs itself must PASS; opp_v76 ships NOISE_ON=True (must FAIL).
CONTROLS = ["bots/starter", "bots/opp_v63", "bots/opp_v76"]

KEYS = ("winner", "turns", "win_condition", "a_titanium", "b_titanium",
        "a_titanium_collected", "b_titanium_collected",
        "a_units", "b_units", "a_buildings", "b_buildings")


def play(job):
    bot, mp, seed, seat = job
    a, b = (bot, REFERENCE) if seat == "a" else (REFERENCE, bot)
    cmd = [str(FCODE), "run", a, b, mp, "--seed", str(seed),
           "--tle", "0", "--json", "--replay", "/dev/null"]
    pr = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    for line in reversed(pr.stdout.splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if "winner" in r:
                return json.dumps({k: r.get(k) for k in KEYS}, sort_keys=True)
    return "ERROR"


def main():
    reps = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    ncfg = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    maps = sorted(ROOT.glob("maps/*.map26"))
    configs = [(str(maps[i % len(maps)]), 1 + i, "a" if i % 2 == 0 else "b")
               for i in range(ncfg)]

    jobs, index = [], []
    for bot in CANDIDATES + CONTROLS:
        for mp, seed, seat in configs:
            for _ in range(reps):
                jobs.append((bot, mp, seed, seat))
                index.append((bot, Path(mp).stem, seed, seat))

    print(f"{len(CANDIDATES)} candidates + {len(CONTROLS)} controls "
          f"x {ncfg} configs x {reps} reps = {len(jobs)} matches, "
          f"--tle 0, vs {REFERENCE}\n", file=sys.stderr)

    with ProcessPoolExecutor(max_workers=6) as ex:
        out = list(ex.map(play, jobs))

    groups: dict = {}
    for (bot, mp, seed, seat), res in zip(index, out):
        groups.setdefault((bot, mp, seed, seat), []).append(res)

    print(f"{'bot':<18}{'configs':>9}{'identical':>11}{'verdict':>16}")
    verdicts = {}
    for bot in CANDIDATES + CONTROLS:
        cfgs = [k for k in groups if k[0] == bot]
        ident = sum(1 for k in cfgs if len(set(groups[k])) == 1
                    and "ERROR" not in groups[k])
        err = any("ERROR" in groups[k] for k in cfgs)
        ok = ident == len(cfgs) and not err
        verdicts[bot] = ok
        tag = "ERROR" if err else ("DETERMINISTIC" if ok else "NONDETERMINISTIC")
        print(f"{bot:<18}{len(cfgs):>9}{ident:>11}{tag:>16}")

    print(f"\ncontrols (the test is only trustworthy if these come out right):")
    for bot, expect in (("bots/starter", False), ("bots/opp_v63", True),
                        ("bots/opp_v76", False)):
        got = verdicts.get(bot)
        print(f"  {bot:<18} expected {'DET' if expect else 'NONDET':<7} "
              f"got {'DET' if got else 'NONDET':<7} "
              f"{'OK' if got == expect else '<-- CONTROL FAILED'}")

    passed = [b for b in CANDIDATES if verdicts.get(b)]
    print(f"\nverified deterministic candidates: {len(passed)}/{len(CANDIDATES)}"
          f"  {[Path(b).name for b in passed]}")
    print(f"det screening ceiling = 15 maps x 2 seats x "
          f"{len(passed)+1} opponents (incl. opp_v63) = "
          f"{30*(len(passed)+1)} effective observations")


if __name__ == "__main__":
    main()
