#!/usr/bin/env python3
"""v524 verification (c): quick outcome read on the two reclaimed maps.

n=60/map, v524 (treatment) vs bots/_v488beltbreak2, INTERLEAVED with
v522floor (parent, the concurrent baseline) vs the same opponent, seat
balanced (30/30), PAR=4 max local worker processes. This is a DIRECTION READ
at +-12pp, not a locked battery -- reported as such.

Usage: .venv/bin/python3 scratchpad/s51_v524_build/outcome_battery.py
"""
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FCODE = str(ROOT / ".venv/bin/fcode")
OUT = ROOT / "scratchpad/s51_v524_build/outcome_battery"
OUT.mkdir(parents=True, exist_ok=True)

V524 = str(ROOT / "bots/_v524exact")
V522 = str(ROOT / "bots/_v522floor")
OPP = str(ROOT / "bots/_v488beltbreak2")
MAPS = ["ragnarok", "frostgate"]
N_PER_MAP = 60          # 30 per seat
SEED_BASE = 524200      # local-only battery, documented inline, no platform/shard collision
PAR = 4


def one_game(arm, treat, opp, mapname, seed, seat):
    tag = f"{arm}_{mapname}_{seed}_{seat}"
    replay = OUT / f"{tag}.replay26"
    if seat == "A":
        A, B = treat, opp
    else:
        A, B = opp, treat
    cmd = [FCODE, "run", A, B, str(ROOT / "maps" / f"{mapname}.map26"),
           "--seed", str(seed), "--tle", "10", "--replay", str(replay), "--json"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    try:
        data = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:
        return dict(arm=arm, map=mapname, seed=seed, seat=seat, ok=False,
                    err=r.stderr[-500:], stdout=r.stdout[-300:])
    treat_side = "A" if seat == "A" else "B"
    won = data.get("winner") == treat_side
    return dict(arm=arm, map=mapname, seed=seed, seat=seat, ok=True,
                winner=data.get("winner"), turns=data.get("turns"),
                cond=data.get("win_condition"), treat_won=won)


def main():
    jobs = []
    seed = SEED_BASE
    for mapname in MAPS:
        for i in range(N_PER_MAP):
            seat = "A" if i % 2 == 0 else "B"
            jobs.append(("v524", V524, mapname, seed, seat))
            jobs.append(("v522", V522, mapname, seed, seat))
            seed += 1
    print(f"total games: {len(jobs)} (PAR={PAR})", file=sys.stderr)

    results = []
    with ThreadPoolExecutor(max_workers=PAR) as ex:
        futs = {ex.submit(one_game, arm, treat, OPP, m, s, seat): (arm, m, s, seat)
                for arm, treat, m, s, seat in jobs}
        done = 0
        for fut in as_completed(futs):
            results.append(fut.result())
            done += 1
            if done % 20 == 0:
                print(f"  {done}/{len(jobs)} done", file=sys.stderr)

    out_tsv = OUT / "results.tsv"
    cols = ["arm", "map", "seed", "seat", "ok", "winner", "turns", "cond", "treat_won"]
    with open(out_tsv, "w") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in results:
            fh.write("\t".join(str(r.get(c, "")) for c in cols) + "\n")

    print("\n=== SUMMARY ===")
    for arm in ("v524", "v522"):
        for mapname in MAPS:
            rows = [r for r in results if r["arm"] == arm and r["map"] == mapname]
            fails = [r for r in rows if not r["ok"]]
            oks = [r for r in rows if r["ok"]]
            wins = sum(1 for r in oks if r["treat_won"])
            n = len(oks)
            print(f"{arm:5s} {mapname:10s} n={n:3d} wins={wins:3d} "
                  f"({100*wins/n:.1f}%)  fails={len(fails)}")
    print()
    for mapname in MAPS:
        v524_rows = [r for r in results if r["arm"] == "v524" and r["map"] == mapname and r["ok"]]
        v522_rows = [r for r in results if r["arm"] == "v522" and r["map"] == mapname and r["ok"]]
        w524 = sum(1 for r in v524_rows if r["treat_won"])
        w522 = sum(1 for r in v522_rows if r["treat_won"])
        n524, n522 = len(v524_rows), len(v522_rows)
        p524 = 100 * w524 / n524 if n524 else float("nan")
        p522 = 100 * w522 / n522 if n522 else float("nan")
        delta = p524 - p522
        print(f"{mapname:10s}  v524 {w524}/{n524} ({p524:.1f}%)  "
              f"v522(parent) {w522}/{n522} ({p522:.1f}%)  DELTA {delta:+.1f}pp")

    n_fail = sum(1 for r in results if not r["ok"])
    n_traceback = sum(1 for r in results if r.get("err") and
                       ("Traceback" in r["err"] or "traceback" in r["err"]))
    print(f"\nparse-fails={n_fail}  tracebacks-in-stderr={n_traceback}  total={len(results)}")


if __name__ == "__main__":
    main()
