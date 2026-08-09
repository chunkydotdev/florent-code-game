#!/usr/bin/env python3
"""Our own archived record against every team, with the opponent's at-match
ratingBefore -- so a candidate target can be checked against evidence we already
have rather than only against third-party play.

    python headtohead.py <freezedir>
"""
from __future__ import annotations
import csv, statistics, sys
from collections import defaultdict


def f(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def main(argv):
    fz = argv[0]
    M = [r for r in csv.DictReader(open(f"{fz}/meta_join.tsv"), delimiter="\t")
         if r["us_side"] != "none" and r["related"] == "none"]
    K = {}
    for r in csv.DictReader(open(f"{fz}/killmix.tsv"), delimiter="\t"):
        K.setdefault(r["file"], {})[r["victim_idx"]] = r
    acc = defaultdict(lambda: defaultdict(list))
    for m in M:
        us = m["us_side"]                       # 'a' or 'b'
        them = "b" if us == "a" else "a"
        opp = m[f"team{them.upper()}Name"]
        oppr = f(m[f"rating{them.upper()}Before"])
        if oppr is None:
            continue
        km = K.get(m["file"])
        if not km:
            continue
        us_idx = "0" if us == "a" else "1"
        them_idx = "1" if us == "a" else "0"
        a = acc[opp]
        a["rat"].append(oppr)
        a["ourdeath"].append(int(km[us_idx]["death_rnd"]))
        a["theirdeath"].append(int(km[them_idx]["death_rnd"]))
        a["ver"].append(m[f"team{us.upper()}Version"])
        a["oppver"].append(m[f"team{them.upper()}Version"])
    print(f"{'opponent':30s} {'oppMedRat':>9s} {'games':>6s} {'WE kill%':>9s} "
          f"{'<=r250':>8s} {'medKill':>8s} {'THEY kill%':>11s} {'medDeath':>9s} {'oppVers':>18s}")
    for opp in sorted(acc, key=lambda o: -statistics.median(acc[o]["rat"])):
        a = acc[opp]
        n = len(a["rat"])
        if n < 15:
            continue
        tk = [d for d in a["theirdeath"] if d >= 0]
        ok = [d for d in a["ourdeath"] if d >= 0]
        vs = sorted(set(a["oppver"]))
        print(f"{opp[:30]:30s} {statistics.median(a['rat']):9.0f} {n:6d} "
              f"{100*len(tk)/n:8.1f}% {100*sum(1 for d in tk if d<=250)/n:7.1f}% "
              f"{(statistics.median(tk) if tk else float('nan')):8.0f} "
              f"{100*len(ok)/n:10.1f}% {(statistics.median(ok) if ok else float('nan')):9.0f} "
              f"{','.join(vs[:4])[:18]:>18s}")


if __name__ == "__main__":
    main(sys.argv[1:])
