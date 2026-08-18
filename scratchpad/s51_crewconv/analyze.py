#!/usr/bin/env python3
"""FS_CREW_CONVERT measurement analysis: overall table + per-map splits +
naive two-sample interval on wins and k<=300, matching the format used
elsewhere in this repo (half-width = 1.96*sqrt(p(1-p)/n) per arm, and for the
delta: 1.96*sqrt(p1(1-p1)/n1 + p2(1-p2)/n2)). NAIVE -- no DEFF applied (that
correction is for platform ladder/unrated games; this is local corefill/arena,
which the project's own audit reads as pair-weighted DEFF ~0.98, i.e. the
naive interval is correct here per the "local's exemption is measured" rule).
"""
import sys
import glob
import math
import statistics
from collections import defaultdict


def load(pattern):
    rows = []
    for p in sorted(glob.glob(pattern)):
        with open(p) as fh:
            hdr = fh.readline().rstrip("\n").split("\t")
            for line in fh:
                f = line.rstrip("\n").split("\t")
                if len(f) != len(hdr):
                    continue
                rows.append(dict(zip(hdr, f)))
    return rows


def stats(rows):
    n = len(rows)
    wins = sum(1 for r in rows if r["ours"] == "US")
    kill = [r for r in rows if r["ours"] == "US" and "Core destroyed" in r["cond"]]
    k300 = sum(1 for r in kill if int(r["turn"]) <= 300)
    ourdead = sum(1 for r in rows
                  if r["ours"] == "OPP" and "Core destroyed" in r["cond"])
    r1000 = sum(1 for r in rows if int(r["turn"]) >= 1000)
    med = statistics.median([int(r["turn"]) for r in kill]) if kill else -1
    tb = sum(int(r["tracebacks"]) for r in rows)
    return dict(n=n, wins=wins, k300=k300, ourdead=ourdead, r1000=r1000,
                med=med, tb=tb, kills=len(kill))


def hw1(p, n):
    if n == 0:
        return 0.0
    return 1.96 * math.sqrt(p * (1 - p) / n)


def hw2(p1, n1, p2, n2):
    if n1 == 0 or n2 == 0:
        return 0.0
    return 1.96 * math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)


def main():
    a_pat, b_pat = sys.argv[1], sys.argv[2]
    a_rows = load(a_pat)
    b_rows = load(b_pat)
    a = stats(a_rows)
    b = stats(b_rows)

    print("=== OVERALL ===")
    print("arm\tn\twins\twin%\thw\tk<=300\tk300%\thw\tourcore_dead\tr1000\tmed_kill\ttb")
    for name, s in (("CARRIER", a), ("CREWCONV", b)):
        pw = s["wins"] / s["n"] if s["n"] else 0
        pk = s["k300"] / s["n"] if s["n"] else 0
        print("%s\t%d\t%d\t%.1f\t%.1f\t%d\t%.1f\t%.1f\t%d\t%d\t%s\t%d" % (
            name, s["n"], s["wins"], 100 * pw, 100 * hw1(pw, s["n"]),
            s["k300"], 100 * pk, 100 * hw1(pk, s["n"]),
            s["ourdead"], s["r1000"], s["med"], s["tb"]))

    pw_a, pw_b = a["wins"] / a["n"], b["wins"] / b["n"]
    pk_a, pk_b = a["k300"] / a["n"], b["k300"] / b["n"]
    print("\nDELTA (CREWCONV - CARRIER):")
    print("  wins    %+.1fpp  half-width %.1f" % (
        100 * (pw_b - pw_a), 100 * hw2(pw_a, a["n"], pw_b, b["n"])))
    print("  k<=300  %+.1fpp  half-width %.1f" % (
        100 * (pk_b - pk_a), 100 * hw2(pk_a, a["n"], pk_b, b["n"])))

    print("\n=== PER-MAP ===")
    print("map\tarm\tn\twins\twin%\tk<=300\tk300%\tourcore_dead\tmed_kill")
    maps = sorted(set(r["map"] for r in a_rows) | set(r["map"] for r in b_rows))
    for mp in maps:
        for name, rows in (("CARRIER", a_rows), ("CREWCONV", b_rows)):
            sub = [r for r in rows if r["map"] == mp]
            s = stats(sub)
            pw = s["wins"] / s["n"] if s["n"] else 0
            pk = s["k300"] / s["n"] if s["n"] else 0
            print("%s\t%s\t%d\t%d\t%.1f\t%d\t%.1f\t%d\t%s" % (
                mp, name, s["n"], s["wins"], 100 * pw, s["k300"], 100 * pk,
                s["ourdead"], s["med"]))


if __name__ == "__main__":
    main()
