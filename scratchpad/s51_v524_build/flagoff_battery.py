#!/usr/bin/env python3
"""v524 verification (d), second half: FLAG-OFF BEHAVIOURAL EQUIVALENCE, n=90.

`LOKI_FS_V524 = False` is claimed to reproduce `bots/_v522floor` unchanged.
The AST scan (flagoff_ast.py) proves there is no derived-default hazard; this
adds the win-rate-level cross-check the house method also runs (v518's
FO1/FO2/FO3 pattern): flagoff (LOKI_FS_V524=False, all 5 modules otherwise
identical to the shipped tree) vs a fixed opponent, INTERLEAVED with the true
parent v522floor vs the SAME opponent, across the full 15-map pool (6 games
each: 3 seeds x 2 seats = 90 games/arm), PAR=4. Expectation: near-parity
between the two arms' win rate against the opponent -- a large, easily-visible
split would mean the flag-off path is NOT actually a no-op.

Usage: .venv/bin/python3 scratchpad/s51_v524_build/flagoff_battery.py
"""
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FCODE = str(ROOT / ".venv/bin/fcode")
OUT = ROOT / "scratchpad/s51_v524_build/flagoff_battery_out"
OUT.mkdir(parents=True, exist_ok=True)

FLAGOFF = str(ROOT / "scratchpad/s51_v524_build/flagoff_arm")
V522 = str(ROOT / "bots/_v522floor")
OPP = str(ROOT / "bots/_v488beltbreak2")
POOL = ["antler", "archipelago", "auroraveil", "drakkarfjord", "drumlin",
        "fjordgate", "frostgate", "glacierkeep", "icefloe", "midgard",
        "nordkap", "ragnarok", "royale", "valkyrie", "yulerune"]
SEEDS_PER_MAP = 3       # x2 seats = 6 games/map/arm = 90 games/arm total
SEED_BASE = 524500      # local-only battery, distinct from outcome_battery's 524200 block
PAR = 4


def one_game(arm, treat, opp, mapname, seed, seat):
    replay = OUT / f"{arm}_{mapname}_{seed}_{seat}.replay26"
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
                    err=r.stderr[-500:])
    treat_side = "A" if seat == "A" else "B"
    won = data.get("winner") == treat_side
    return dict(arm=arm, map=mapname, seed=seed, seat=seat, ok=True,
                winner=data.get("winner"), turns=data.get("turns"),
                cond=data.get("win_condition"), treat_won=won)


def main():
    jobs = []
    seed = SEED_BASE
    for mapname in POOL:
        for i in range(SEEDS_PER_MAP):
            for seat in ("A", "B"):
                jobs.append(("flagoff", FLAGOFF, mapname, seed, seat))
                jobs.append(("v522", V522, mapname, seed, seat))
            seed += 1
    print(f"total games: {len(jobs)} (PAR={PAR})", file=sys.stderr)

    results = []
    with ThreadPoolExecutor(max_workers=PAR) as ex:
        futs = {ex.submit(one_game, arm, treat, OPP, m, s, seat): 1
                for arm, treat, m, s, seat in jobs}
        done = 0
        for fut in as_completed(futs):
            results.append(fut.result())
            done += 1
            if done % 30 == 0:
                print(f"  {done}/{len(jobs)} done", file=sys.stderr)

    out_tsv = OUT / "results.tsv"
    cols = ["arm", "map", "seed", "seat", "ok", "winner", "turns", "cond", "treat_won"]
    with open(out_tsv, "w") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in results:
            fh.write("\t".join(str(r.get(c, "")) for c in cols) + "\n")

    n_fail = sum(1 for r in results if not r["ok"])
    n_tb = sum(1 for r in results if r.get("err") and "raceback" in r["err"])
    flagoff_rows = [r for r in results if r["arm"] == "flagoff" and r["ok"]]
    v522_rows = [r for r in results if r["arm"] == "v522" and r["ok"]]
    w_fo = sum(1 for r in flagoff_rows if r["treat_won"])
    w_v5 = sum(1 for r in v522_rows if r["treat_won"])
    n_fo, n_v5 = len(flagoff_rows), len(v522_rows)
    p_fo = 100 * w_fo / n_fo if n_fo else float("nan")
    p_v5 = 100 * w_v5 / n_v5 if n_v5 else float("nan")
    print("\n=== SUMMARY ===")
    print(f"flagoff  n={n_fo}  wins={w_fo}  ({p_fo:.1f}%)")
    print(f"v522(parent)  n={n_v5}  wins={w_v5}  ({p_v5:.1f}%)")
    print(f"DELTA {p_fo - p_v5:+.1f}pp")
    print(f"parse-fails={n_fail}  tracebacks-in-stderr={n_tb}  total={len(results)}")


if __name__ == "__main__":
    main()
