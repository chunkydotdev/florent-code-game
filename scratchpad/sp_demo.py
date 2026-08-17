#!/usr/bin/env python3
"""Run a LOKI-SEALPIERCE demo sweep and roll the shot-level tapes up.

Not a battery and not a verdict: this plays games only to make the MECHANISM
observable -- seat Sentinels planted, what stood on the far side of the enemy
Core while they were alive (the OPPORTUNITY), and which rung each shot took.
Per-game rows are printed so a zero can be traced to the game that produced it.

D2: maps rotate over the whole new-maps pool, both seats, rather than the three
convenient ones.

Usage:
  .venv/bin/python scratchpad/sp_demo.py --ours _tmp_pierceon --opp opp_v78 \
      --maps drumlin heart ... --seeds 3 --jobs 6
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scratchpad"))
sys.path.insert(0, str(ROOT / "tools"))
import sp_shots  # noqa: E402

FCODE = ROOT / ".venv" / "bin" / "fcode"
OUT = ROOT / "scratchpad" / "sp_demo_replays"


def play(job):
    ours, opp, mapname, seed, seat = job
    OUT.mkdir(exist_ok=True)
    a, b = (ours, opp) if seat == "A" else (opp, ours)
    rp = OUT / ("%s_%s_%s_s%d_%s.replay26" % (ours, opp, mapname, seed, seat))
    cmd = [str(FCODE), "run", a, b, "maps/new-maps/%s.map26" % mapname,
           "--seed", str(seed), "--tle", "0", "--json", "--replay", str(rp)]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    tb = proc.stderr.count("Traceback (most recent call last)")
    ours_tb = sum(1 for blk in proc.stderr.split("Traceback (most recent call last)")
                  if "bots/%s/" % ours in blk)
    try:
        r = sp_shots.analyse(rp, 0 if seat == "A" else 1, 2, 8)
        j = sp_shots.analyse(rp, 0 if seat == "A" else 1, 2, 8, jitter=(1, 0))
    except Exception as exc:
        return {"map": mapname, "seed": seed, "seat": seat, "error": str(exc)}
    rungs = defaultdict(int)
    for s in r["shots"]:
        rungs[s[6]] += 1
        if s[5]:
            rungs["THROUGH"] += 1
    jr = defaultdict(int)
    for s in j["shots"]:
        jr[s[6]] += 1
    return {
        "map": mapname, "seed": seed, "seat": seat,
        "rounds": r["rep"].rounds,
        "cond": r["rep"].win_condition,
        "won": (r["rep"].winner == (0 if seat == "A" else 1)),
        "seats": len(r["seat"]),
        "seat_rounds": sum(r["live_seat_rounds"].values()),
        "far_belt": r["opp"]["far_belt_rounds"],
        "far_best": r["opp"]["far_belt_rounds_bestfacing"],
        "far_mouth": r["opp"]["far_mouth_belt_rounds"],
        "far_heal": r["opp"]["far_healer_rounds"],
        "MOUTH": rungs["MOUTH"], "APRON": rungs["APRON"],
        "HEALER": rungs["HEALER"], "CORE": rungs["CORE"],
        "OTHER": rungs["OTHER"], "empty": rungs["empty"],
        "THROUGH": rungs["THROUGH"],
        "jMOUTH": jr["MOUTH"], "jAPRON": jr["APRON"],
        "belt_kills": r["kills"]["belt_killed_by_seat"],
        "heal_kills": r["kills"]["healer_killed_by_seat"],
        "refarm": len(r["rekilled"]),
        "tled": r["tled"], "tb": tb, "ours_tb": ours_tb,
        "collected": None,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ours", required=True)
    ap.add_argument("--opp", required=True)
    ap.add_argument("--maps", nargs="+", required=True)
    ap.add_argument("--seeds", type=int, default=2)
    ap.add_argument("--seed0", type=int, default=1)
    ap.add_argument("--jobs", type=int, default=6)
    args = ap.parse_args()

    jobs = [(args.ours, args.opp, m, args.seed0 + s, seat)
            for m in args.maps for s in range(args.seeds) for seat in ("A", "B")]
    rows = []
    with ProcessPoolExecutor(max_workers=args.jobs) as ex:
        for r in ex.map(play, jobs):
            rows.append(r)
            if "error" in r:
                print("ERROR %s" % r)
                continue
            print("%-11s s%-3d %s r=%-4d %-16s win=%-5s seats=%d seatR=%-4d "
                  "far(belt/mouth/heal)=%d/%d/%d  shots M=%d A=%d H=%d C=%d O=%d "
                  "thru=%d  jitM=%d  kills belt=%d heal=%d refarm=%d  tb=%d/%d tled=%d"
                  % (r["map"], r["seed"], r["seat"], r["rounds"], r["cond"], r["won"],
                     r["seats"], r["seat_rounds"], r["far_belt"], r["far_mouth"],
                     r["far_heal"], r["MOUTH"], r["APRON"], r["HEALER"], r["CORE"],
                     r["OTHER"], r["THROUGH"], r["jMOUTH"], r["belt_kills"],
                     r["heal_kills"], r["refarm"], r["ours_tb"], r["tb"], r["tled"]))

    ok = [r for r in rows if "error" not in r]
    t = defaultdict(int)
    for r in ok:
        for k in ("seats", "seat_rounds", "far_belt", "far_best", "far_mouth", "far_heal",
                  "MOUTH", "APRON", "HEALER", "CORE", "OTHER", "empty", "THROUGH",
                  "jMOUTH", "jAPRON", "belt_kills", "heal_kills", "refarm",
                  "tled", "tb", "ours_tb"):
            t[k] += r[k]
    print("\n=== TOTALS over %d games (%s vs %s) ===" % (len(ok), args.ours, args.opp))
    print("games with a seat Sentinel      %d" % sum(1 for r in ok if r["seats"]))
    print("live seat-Sentinel rounds       %d" % t["seat_rounds"])
    print("  ...with an enemy BELT on the far side       %d" % t["far_belt"])
    print("  ...of which on a core MOUTH tile            %d" % t["far_mouth"])
    print("  COUNTERFACTUAL: rounds where SOME legal facing would have had one %d"
          % t["far_best"])
    print("  ...with an enemy BUILDER on a far heal seat %d" % t["far_heal"])
    print("shots  MOUTH=%d APRON=%d HEALER=%d CORE=%d OTHER=%d empty=%d  (through-core %d)"
          % (t["MOUTH"], t["APRON"], t["HEALER"], t["CORE"], t["OTHER"],
             t["empty"], t["THROUGH"]))
    print("JITTER CONTROL (+1,0)  MOUTH=%d APRON=%d  -> %s"
          % (t["jMOUTH"], t["jAPRON"],
             "PASS (lower)" if t["jMOUTH"] + t["jAPRON"] < t["MOUTH"] + t["APRON"]
             else "NOT INFORMATIVE (nothing fired on those rungs)"))
    print("kills  belt=%d healer=%d   tiles re-farmed after rebuild=%d"
          % (t["belt_kills"], t["heal_kills"], t["refarm"]))
    print("hygiene  our tracebacks=%d  all tracebacks=%d  tled bot-turns=%d"
          % (t["ours_tb"], t["tb"], t["tled"]))
    print("games won %d/%d" % (sum(1 for r in ok if r["won"]), len(ok)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
