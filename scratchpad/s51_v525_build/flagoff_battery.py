#!/usr/bin/env python3
"""v525 verification (d): flag-off behavioural check, n=90, full 15-map pool.

LOKI_FS_V525=False arm (definition-site override in a scratch copy) vs
bots/_v488beltbreak2, interleaved with the true parent bots/_v524exact vs the
same opponent, PAR=2 (PINCERPOOL shard owns the cores), seed base 525500
(distinct block from direction_read.py's 525200).

Method per BUILD-REPORT-v524exact-2026-08-18.md (d): corroborates the AST
scan with a real win-rate read -- no dramatic behavioural split expected
between the flag-off arm and the true parent.

Usage: .venv/bin/python3 scratchpad/s51_v525_build/flagoff_battery.py
"""
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FCODE = str(ROOT / ".venv/bin/fcode")
OUT = ROOT / "scratchpad/s51_v525_build/flagoff_battery"
OUT.mkdir(parents=True, exist_ok=True)

FLAGOFF = str(ROOT / "scratchpad/s51_v525_build/flagoff_arm")
V524 = str(ROOT / "bots/_v524exact")
OPP = str(ROOT / "bots/_v488beltbreak2")
POOL = ["antler", "archipelago", "auroraveil", "drakkarfjord", "drumlin",
        "fjordgate", "frostgate", "glacierkeep", "icefloe", "midgard",
        "nordkap", "ragnarok", "royale", "valkyrie", "yulerune"]
SEEDS = [1, 2, 3]        # 3 seeds x 2 seats x 15 maps = 90 games/arm
SEED_BASE = 525500
PAR = 2


def one_game(arm, treat_dir, mapname, seed, seat):
    tag = f"{arm}_{mapname}_{seed}_{seat}"
    replay = OUT / f"{tag}.replay26"
    if seat == "A":
        A, B = treat_dir, OPP
    else:
        A, B = OPP, treat_dir
    cmd = [FCODE, "run", A, B, str(ROOT / "maps" / f"{mapname}.map26"),
           "--seed", str(seed), "--tle", "10", "--replay", str(replay), "--json"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    tb = "Traceback" in r.stderr
    try:
        data = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:
        return dict(arm=arm, map=mapname, seed=seed, seat=seat, ok=False,
                    err=r.stderr[-500:], stdout=r.stdout[-300:], traceback=tb)
    treat_side = "A" if seat == "A" else "B"
    won = data.get("winner") == treat_side
    return dict(arm=arm, map=mapname, seed=seed, seat=seat, ok=True,
                winner=data.get("winner"), turns=data.get("turns"),
                cond=data.get("win_condition"), treat_won=won, traceback=tb)


def main():
    jobs = []
    seed_ctr = SEED_BASE
    for mapname in POOL:
        for i, s in enumerate(SEEDS):
            for seat in ("A", "B"):
                jobs.append(("flagoff", FLAGOFF, mapname, seed_ctr, seat))
                jobs.append(("v524parent", V524, mapname, seed_ctr, seat))
                seed_ctr += 1
    print(f"total games: {len(jobs)} (PAR={PAR})", file=sys.stderr)

    results = []
    with ThreadPoolExecutor(max_workers=PAR) as ex:
        futs = {ex.submit(one_game, arm, d, m, s, seat): (arm, m, s, seat)
                for arm, d, m, s, seat in jobs}
        done = 0
        for fut in as_completed(futs):
            results.append(fut.result())
            done += 1
            if done % 30 == 0:
                print(f"  {done}/{len(jobs)} done", file=sys.stderr)

    out_tsv = OUT / "results.tsv"
    cols = ["arm", "map", "seed", "seat", "ok", "winner", "turns", "cond", "treat_won", "traceback"]
    with open(out_tsv, "w") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in results:
            fh.write("\t".join(str(r.get(c, "")) for c in cols) + "\n")

    print("\n=== SUMMARY ===")
    for arm in ("flagoff", "v524parent"):
        rows = [r for r in results if r["arm"] == arm]
        oks = [r for r in rows if r["ok"]]
        fails = [r for r in rows if not r["ok"]]
        wins = sum(1 for r in oks if r["treat_won"])
        n = len(oks)
        pct = 100 * wins / n if n else float("nan")
        print(f"{arm:12s} n={n:3d} wins={wins:3d} ({pct:.1f}%)  fails={len(fails)}")

    n_fail = sum(1 for r in results if not r["ok"])
    n_traceback = sum(1 for r in results if r.get("traceback"))
    print(f"\nparse-fails={n_fail}  tracebacks-in-stderr={n_traceback}  total={len(results)}")


if __name__ == "__main__":
    main()
