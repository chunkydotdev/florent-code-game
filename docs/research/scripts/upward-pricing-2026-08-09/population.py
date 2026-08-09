#!/usr/bin/env python3
"""Population census for the upward-pricing cut: who is above us, and how many
CLEAN THIRD-PARTY replay files do we hold of them?

Bands on ratingABefore/ratingBBefore (cols 13/14) -- NEVER teamARating/teamBRating,
which are live joins identical on every historical row for a team.

    python population.py <freezedir>
"""
from __future__ import annotations
import collections, csv, statistics, sys


def load(fz):
    return list(csv.DictReader(open(f"{fz}/meta_join.tsv"), delimiter="\t"))


def main(argv):
    fz = argv[0]
    rows = load(fz)
    tp = [r for r in rows if r["us_side"] == "none" and r["related"] == "none"]
    ours = [r for r in rows if r["us_side"] != "none" and r["related"] == "none"]
    print(f"attributed rows {len(rows)}   clean third-party {len(tp)}   clean ours {len(ours)}")

    # per-team: files where that team is a side, with its at-match ratingBefore
    files = collections.defaultdict(set)
    matches = collections.defaultdict(set)
    rat = collections.defaultdict(list)
    for r in tp:
        for side in "AB":
            nm = r[f"team{side}Name"]
            files[nm].add(r["file"])
            matches[nm].add(r["match"])
            try:
                rat[nm].append(float(r[f"rating{side}Before"]))
            except ValueError:
                pass
    print(f"\ndistinct third-party teams: {len(files)}")
    tbl = []
    for nm in files:
        med = statistics.median(rat[nm]) if rat[nm] else float("nan")
        tbl.append((med, nm, len(files[nm]), len(matches[nm]), min(rat[nm]), max(rat[nm])))
    tbl.sort(reverse=True)
    print(f"\n{'team':34s} {'medRatBefore':>12s} {'files':>6s} {'matches':>8s} {'min':>7s} {'max':>7s}")
    for med, nm, nf, nm_, lo, hi in tbl:
        if med >= 1600:
            print(f"{nm[:34]:34s} {med:12.1f} {nf:6d} {nm_:8d} {lo:7.0f} {hi:7.0f}")

    # side-games at >=1700 (the victim band question)
    for thr in (1650, 1700, 1750, 1800):
        n_side = sum(1 for r in tp for s in "AB"
                     if _f(r[f"rating{s}Before"]) >= thr)
        n_file = sum(1 for r in tp
                     if max(_f(r["ratingABefore"]), _f(r["ratingBBefore"])) >= thr)
        both = sum(1 for r in tp
                   if min(_f(r["ratingABefore"]), _f(r["ratingBBefore"])) >= thr)
        print(f"\nthreshold {thr}: side-games {n_side}, files with >=1 such side {n_file}, files with BOTH sides {both}")


def _f(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return -1.0


if __name__ == "__main__":
    main(sys.argv[1:])
