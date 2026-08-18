#!/usr/bin/env python3
"""v525 verification (c): direction read n=60/map on the three flipped maps,
vs bots/_v488beltbreak2. Expected bands from scratchpad/s51_forceall/
(n=90/map, forced-rush at current strength): yulerune 91.1 [+-5.9], antler
64.4, fjordgate 63.3 -- this build should read in the same neighbourhood
since it is the SAME rush chassis, just switched on for these three maps
through the real (unforced) gate/cripple mechanism rather than a
zeroed-threshold override. A DIRECTION READ at ~+-13pp (n=60), not a locked
battery -- reported as such, per the project's one-draw-law/pooling standard.

Usage: .venv/bin/python3 scratchpad/s51_v525_build/direction_read.py
"""
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FCODE = str(ROOT / ".venv/bin/fcode")
OUT = ROOT / "scratchpad/s51_v525_build/direction_read"
OUT.mkdir(parents=True, exist_ok=True)

V525 = str(ROOT / "bots/_v525flip")
OPP = str(ROOT / "bots/_v488beltbreak2")
MAPS = ["yulerune", "antler", "fjordgate"]
N_PER_MAP = 60          # 30 per seat
SEED_BASE = 525200      # local-only battery, distinct block, no shard collision
PAR = 2                 # PINCERPOOL shard owns the cores


def one_game(mapname, seed, seat):
    tag = f"v525_{mapname}_{seed}_{seat}"
    replay = OUT / f"{tag}.replay26"
    if seat == "A":
        A, B = V525, OPP
    else:
        A, B = OPP, V525
    cmd = [FCODE, "run", A, B, str(ROOT / "maps" / f"{mapname}.map26"),
           "--seed", str(seed), "--tle", "10", "--replay", str(replay), "--json"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    tb = "Traceback" in r.stderr
    try:
        data = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:
        return dict(map=mapname, seed=seed, seat=seat, ok=False,
                    err=r.stderr[-500:], stdout=r.stdout[-300:], traceback=tb)
    treat_side = "A" if seat == "A" else "B"
    won = data.get("winner") == treat_side
    return dict(map=mapname, seed=seed, seat=seat, ok=True,
                winner=data.get("winner"), turns=data.get("turns"),
                cond=data.get("win_condition"), treat_won=won, traceback=tb)


def main():
    jobs = []
    seed = SEED_BASE
    for mapname in MAPS:
        for i in range(N_PER_MAP):
            seat = "A" if i % 2 == 0 else "B"
            jobs.append((mapname, seed, seat))
            seed += 1
    print(f"total games: {len(jobs)} (PAR={PAR})", file=sys.stderr)

    results = []
    with ThreadPoolExecutor(max_workers=PAR) as ex:
        futs = {ex.submit(one_game, m, s, seat): (m, s, seat) for m, s, seat in jobs}
        done = 0
        for fut in as_completed(futs):
            results.append(fut.result())
            done += 1
            if done % 30 == 0:
                print(f"  {done}/{len(jobs)} done", file=sys.stderr)

    out_tsv = OUT / "results.tsv"
    cols = ["map", "seed", "seat", "ok", "winner", "turns", "cond", "treat_won", "traceback"]
    with open(out_tsv, "w") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in results:
            fh.write("\t".join(str(r.get(c, "")) for c in cols) + "\n")

    print("\n=== SUMMARY (v525 vs bots/_v488beltbreak2) ===")
    forceall_basis = {"yulerune": 91.1, "antler": 64.4, "fjordgate": 63.3}
    for mapname in MAPS:
        rows = [r for r in results if r["map"] == mapname]
        oks = [r for r in rows if r["ok"]]
        fails = [r for r in rows if not r["ok"]]
        wins = sum(1 for r in oks if r["treat_won"])
        n = len(oks)
        pct = 100 * wins / n if n else float("nan")
        basis = forceall_basis[mapname]
        print(f"{mapname:10s} n={n:3d} wins={wins:3d} ({pct:5.1f}%)  "
              f"forceall-basis {basis:5.1f}%  delta {pct-basis:+.1f}pp  fails={len(fails)}")

    n_fail = sum(1 for r in results if not r["ok"])
    n_traceback = sum(1 for r in results if r.get("traceback"))
    print(f"\nparse-fails={n_fail}  tracebacks-in-stderr={n_traceback}  total={len(results)}")


if __name__ == "__main__":
    main()
