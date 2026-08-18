#!/usr/bin/env python3
"""s51 closure autopsy -- the consolidated per-game and per-map read.

Joins closure_attrib / residual_seatlife / residual_set / opportunity / gaps /
ferry_launchers into one per-game row (summary_game.tsv) and prints the two
attribution views.

TWO DENOMINATORS, and the second is the one closure actually cares about.

  (A) OPEN-SEAT-ROUNDS.  Fine-grained, precedence-assigned (see closure.py).
      Useful for "where did the siege spend its time", but dominated by the
      early rounds when all 8 seats are trivially open, so it CANNOT identify
      the binding constraint.

  (B) CLOSURE-BINDING SEATS.  Closure is an AND over 8 seats, so what blocks it
      is the seat that was NEVER denied.  Per game we count the seats with
      `ever_denied == 0` over the whole at-ring window and classify each by its
      dominant occupant:
          BELT_PRE   enemy conveyor/splitter present BEFORE our raider arrived
          BELT_POST  enemy building that appeared after arrival
          BODY       enemy builder body squatting (throwable -> evictor's job)
          EMPTY      empty, buildable, legal -- never built (walk/priority)
      A game with ZERO never-denied seats that still did not close failed
      TEMPORALLY: every seat was denied at some point but never all at once
      (attrition / rebuild race).
"""
from __future__ import annotations

import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FIRED = ROOT / "scratchpad/s51_evict_autopsy/fired.tsv"


def load(name, key=None):
    with open(HERE / name) as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def classify_seat(r):
    """-> BELT_PRE | BELT_POST | BODY | EMPTY for a never-denied seat."""
    E, b, empty = int(r["E"]), int(r["b"]), int(r["empty"])
    pre = int(r["enemy_bldg_predates_arrival"])
    if E >= max(b, empty):
        return "BELT_PRE" if pre > 0 else "BELT_POST"
    if b >= max(E, empty):
        return "BODY"
    return "EMPTY"


def main():
    ca = {r["game"]: r for r in load("closure_attrib.tsv")}
    op = {r["game"]: r for r in load("opportunity.tsv")}
    gp = {r["game"]: r for r in load("gaps.tsv")}
    rs = {r["game"]: r for r in load("residual_set.tsv")}
    fired = {}
    with open(FIRED) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            fired[r["game"]] = r
    life = defaultdict(list)
    for r in load("residual_seatlife.tsv"):
        life[r["game"]].append(r)

    rows = []
    for g in sorted(ca):
        nd = [r for r in life[g] if r["ever_denied"] == "0"]
        cls = Counter(classify_seat(r) for r in nd)
        f = fired.get(g, {})
        rows.append(dict(
            game=g, map=ca[g]["map"], seat=ca[g]["seat"], seed=ca[g]["seed"],
            won=1 if f.get("outcome") == "v513_log" else 0,
            end_r=f.get("end_r", "?"), cond=f.get("cond", "?"),
            arrive_r=gp[g]["arrive_r"], ring_rounds=ca[g]["ring_rounds"],
            gap_rounds=gp[g]["gap_rounds"], longest_gap=gp[g]["longest_gap"],
            min_orth=ca[g]["min_orth"], close_r=ca[g]["close_r"],
            seals=ca[g]["seals"], clears=ca[g]["clears"],
            seat_bldg_lost=ca[g]["our_seat_bldg_lost"],
            evicts=ca[g]["evicts"], evictors=ca[g]["evictors"],
            nd_seats=len(nd),
            nd_belt_pre=cls["BELT_PRE"], nd_belt_post=cls["BELT_POST"],
            nd_body=cls["BODY"], nd_empty=cls["EMPTY"],
            osr=op[g]["osr"], osr_notbuildable=op[g]["notbuildable"],
            osr_noadj=op[g]["b_noadj"], osr_adj_funded=op[g]["b_adj_fund"],
            osr_nofund=op[g]["b_adj_nofund"],
            residual_tiles=rs[g]["residual_tiles"]))

    cols = list(rows[0].keys())
    with open(HERE / "summary_game.tsv", "w") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in rows:
            fh.write("\t".join(str(r[c]) for c in cols) + "\n")
    print(f"wrote summary_game.tsv ({len(rows)} rows)\n")

    # ---- (B) closure-binding attribution --------------------------------
    print("(B) CLOSURE-BINDING SEATS -- never-denied seats per game, "
          "classified by dominant occupant")
    print(f"{'map':14}{'games':>6}{'closed':>7}{'ND seats':>10}"
          f"{'BELT_PRE':>10}{'BELT_POST':>11}{'BODY':>6}{'EMPTY':>7}"
          f"{'temporal-only fails':>21}")
    agg = defaultdict(lambda: defaultdict(int))
    for r in rows:
        m = r["map"]
        agg[m]["n"] += 1
        if int(r["close_r"]) >= 0:
            agg[m]["closed"] += 1
        for k in ("nd_seats", "nd_belt_pre", "nd_belt_post", "nd_body",
                  "nd_empty"):
            agg[m][k] += int(r[k])
        if int(r["close_r"]) < 0 and int(r["nd_seats"]) == 0:
            agg[m]["temporal"] += 1
    for m in sorted(agg):
        a = agg[m]
        print(f"{m:14}{a['n']:>6}{a['closed']:>7}{a['nd_seats']:>10}"
              f"{a['nd_belt_pre']:>10}{a['nd_belt_post']:>11}"
              f"{a['nd_body']:>6}{a['nd_empty']:>7}{a['temporal']:>21}")
    print()
    tot = sum(agg[m]["nd_seats"] for m in agg)
    print("share of ALL never-denied seats (n=%d) by cause:" % tot)
    for k, lab in (("nd_belt_pre", "enemy belt, PRE-arrival"),
                   ("nd_belt_post", "enemy building, post-arrival"),
                   ("nd_body", "enemy body squat"),
                   ("nd_empty", "empty & legal, never built")):
        v = sum(agg[m][k] for m in agg)
        print(f"   {lab:34} {v:>4}  {100.0*v/tot:5.1f}%")
    print()
    for m in ("atoll", "midgard"):
        a = agg[m]
        s = a["nd_seats"] or 1
        print(f"{m}: ND seats n={a['nd_seats']}  "
              f"BELT_PRE {100*a['nd_belt_pre']/s:.1f}%  "
              f"BELT_POST {100*a['nd_belt_post']/s:.1f}%  "
              f"BODY {100*a['nd_body']/s:.1f}%  "
              f"EMPTY {100*a['nd_empty']/s:.1f}%  "
              f"temporal-only fails {a['temporal']}/{a['n']}")


if __name__ == "__main__":
    if "-h" in sys.argv[1:] or "--help" in sys.argv[1:]:
        print(__doc__)
        raise SystemExit(0)
    main()
