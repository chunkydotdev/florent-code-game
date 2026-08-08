#!/usr/bin/env python3
"""Deterministic-paired A/B: run two candidates against a fixed opponent on
identical (map, seed, seat) triples at --tle 0 and account game-level FLIPS
and identical-end-state rates. This is the other accepted shape for
holder/parent comparisons (docs/tooling.md), and the only one that resolves
small effects: only paired same-(map,seed,seat) flips separate signal from the
~10pp cross-batch spread.

PRECONDITION the script measures but does not enforce: all sides must be
deterministic — flip NOISE_ON=False in local COPIES of the bots first (never
edit the canonical bots/ dirs for this), and use a deterministic opponent
(bots/opp_v63 is the measured reference; bots/starter is NOT deterministic).
--tle 0 removes CPU-kill nondeterminism.

Interpretation caveat (docs/tooling.md): det per-map flips are chaos-bounded —
identity (0-flip) results are gold; small flip counts are butterfly-sensitive
and must not be over-read as attribution.

Usage:
  .venv/bin/python tools/det.py tagA=bots/parent tagB=bots/cand <opp_dir> [seeds=8] [map1,map2,...]

Env: DET_JOBS (default 6), DET_OUT (json dump path, default ./det_results.json).

Promoted from the s15 builder scratchpad (validated 2026-08-08); the s15
version's hardcoded dA/dU piece-U harness became this CLI.
"""
import json
import os
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FCODE = ROOT / ".venv" / "bin" / "fcode"


def play(job):
    tag, bot, opp, mp, seed, seat = job
    a, b = (bot, opp) if seat == "a" else (opp, bot)
    pr = subprocess.run([str(FCODE), "run", a, b, mp, "--seed", str(seed), "--tle", "0",
                         "--json", "--replay", "/dev/null"],
                        capture_output=True, text=True, cwd=ROOT)
    res = None
    for line in reversed(pr.stdout.splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                res = json.loads(line)
                break
            except Exception:
                pass
    if res is None:
        return None
    us, them = ("a", "b") if seat == "a" else ("b", "a")
    return dict(tag=tag, map=Path(mp).stem, seed=seed, seat=seat,
                win=res["winner"].lower() == seat,
                turns=res["turns"], cond=res["win_condition"],
                ti=res[f"{us}_titanium_collected"], oti=res[f"{them}_titanium_collected"],
                units=res[f"{us}_units"], bld=res[f"{us}_buildings"],
                tb=pr.stderr.count("Traceback"))


def main():
    if len(sys.argv) < 4:
        sys.exit("usage: det.py tagA=path tagB=path <opp_dir> [seeds] [map1,map2,...]")
    ta, pa = sys.argv[1].split("=", 1)
    tb, pb = sys.argv[2].split("=", 1)
    opp = sys.argv[3]
    seeds = int(sys.argv[4]) if len(sys.argv) > 4 else 8
    mapsel = sys.argv[5].split(",") if len(sys.argv) > 5 else None
    maps = sorted((ROOT / "maps").glob("*.map26"))
    if mapsel:
        maps = [m for m in maps if m.stem in mapsel]
    jobs = []
    for mp in maps:
        for sd in range(1, seeds + 1):
            for seat in ("a", "b"):
                jobs.append((ta, pa, opp, str(mp), sd, seat))
                jobs.append((tb, pb, opp, str(mp), sd, seat))
    out = []
    workers = int(os.environ.get("DET_JOBS", "6"))
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for i, r in enumerate(pool.map(play, jobs), 1):
            if r:
                out.append(r)
            if i % 50 == 0:
                print(f"\r {i}/{len(jobs)}", end="", file=sys.stderr, flush=True)
    print(file=sys.stderr)
    with open(os.environ.get("DET_OUT", "det_results.json"), "w") as f:
        json.dump(out, f)
    idx = {(r["tag"], r["map"], r["seed"], r["seat"]): r for r in out}
    keys = sorted({(k[1], k[2], k[3]) for k in idx})
    flips = []
    diffstate = []
    same = 0
    awins = bwins = n = 0
    for k in keys:
        A = idx.get((ta,) + k)
        B = idx.get((tb,) + k)
        if not A or not B:
            continue
        n += 1
        awins += A["win"]
        bwins += B["win"]
        if A["win"] != B["win"]:
            flips.append((k, A["win"], B["win"], A["ti"], B["ti"]))
        if (A["turns"], A["ti"], A["units"], A["bld"], A["win"]) == \
           (B["turns"], B["ti"], B["units"], B["bld"], B["win"]):
            same += 1
        else:
            diffstate.append((k, A["turns"], B["turns"], A["ti"], B["ti"]))
    if not n:
        sys.exit("no completed paired games")
    print(f"\npaired deterministic games: {n}")
    print(f"  {ta} wins {awins}/{n} = {awins/n:.1%}   {tb} wins {bwins}/{n} = {bwins/n:.1%}")
    print(f"  identical end-state (turns/ti/units/bld/winner): {same}/{n}")
    print(f"  outcome flips: {len(flips)}")
    for f in flips:
        print("    FLIP", f)
    print(f"  non-identical end-state games: {len(diffstate)}")
    for d in diffstate[:40]:
        print("    DIFF", d)
    print(f"  tracebacks across all games: {sum(r['tb'] for r in out)}")


if __name__ == "__main__":
    main()
