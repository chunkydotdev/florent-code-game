#!/usr/bin/env python3
"""Powered-tape cut: kill-round and our-death-round distributions for the v515
FIRED arm and the p514nd baseline, from scratchpad/s51_v515_build/grid/*.tsv.

Outcome taxonomy per game:
  KILL      ours==US   and cond=='Core destroyed'   -> turn is OUR KILL ROUND
  DEATH     ours==OPP  and cond=='Core destroyed'   -> turn is OUR DEATH ROUND
  TIE_WIN   ours==US   and cond!='Core destroyed'   (r1000 tiebreak win)
  TIE_LOSS  ours==OPP  and cond!='Core destroyed'
"""
import glob
import os
import statistics
import sys
from collections import Counter, defaultdict

GRID = "/Users/junghard/Projects/Work/florent-code-game/scratchpad/s51_v515_build/grid"


def load(pattern):
    rows = []
    for p in sorted(glob.glob(os.path.join(GRID, pattern))):
        with open(p) as fh:
            hdr = fh.readline().rstrip("\n").split("\t")
            for line in fh:
                f = line.rstrip("\n").split("\t")
                if len(f) != len(hdr):
                    continue
                rows.append(dict(zip(hdr, f)))
    return rows


def klass(r):
    kill = r["cond"] == "Core destroyed"
    if r["ours"] == "US":
        return "KILL" if kill else "TIE_WIN"
    if r["ours"] == "OPP":
        return "DEATH" if kill else "TIE_LOSS"
    return "NONE"


def q(xs, p):
    if not xs:
        return None
    xs = sorted(xs)
    i = min(len(xs) - 1, max(0, int(round(p * (len(xs) - 1)))))
    return xs[i]


def report(name, rows):
    n = len(rows)
    cl = Counter(klass(r) for r in rows)
    kills = [int(r["turn"]) for r in rows if klass(r) == "KILL"]
    deaths = [int(r["turn"]) for r in rows if klass(r) == "DEATH"]
    print("\n=== %s  n=%d ===" % (name, n))
    for k in ("KILL", "DEATH", "TIE_WIN", "TIE_LOSS", "NONE"):
        print("  %-9s %4d  %5.1f%%" % (k, cl[k], 100.0 * cl[k] / n))
    for label, xs in (("our kill round", kills), ("our death round", deaths)):
        if xs:
            print("  %-16s n=%d  p10=%s p25=%s med=%s p75=%s p90=%s"
                  % (label, len(xs), q(xs, .10), q(xs, .25),
                     statistics.median(xs), q(xs, .75), q(xs, .90)))
    # kill-by-round CDF over ALL games (ITT)
    for r300 in (150, 200, 250, 300, 400, 500):
        c = sum(1 for t in kills if t <= r300)
        print("  kills<=r%-4d %4d/%d = %5.1f%% (ITT)" % (r300, c, n, 100.0 * c / n))
    # deaths by round
    for r300 in (150, 200, 250, 300):
        c = sum(1 for t in deaths if t <= r300)
        print("  deaths<=r%-3d %4d/%d = %5.1f%% (ITT)" % (r300, c, n, 100.0 * c / n))
    # per map
    bym = defaultdict(list)
    for r in rows:
        bym[r["map"]].append(r)
    print("  per map: map  n  win%  KILL%  DEATH%  TIEWIN%  medkill  meddeath")
    for m in sorted(bym):
        rs = bym[m]
        c = Counter(klass(r) for r in rs)
        ks = [int(r["turn"]) for r in rs if klass(r) == "KILL"]
        ds = [int(r["turn"]) for r in rs if klass(r) == "DEATH"]
        print("    %-14s %4d %5.1f %6.1f %6.1f %7.1f %8s %8s"
              % (m, len(rs), 100.0 * sum(1 for r in rs if r["ours"] == "US") / len(rs),
                 100.0 * c["KILL"] / len(rs), 100.0 * c["DEATH"] / len(rs),
                 100.0 * c["TIE_WIN"] / len(rs),
                 statistics.median(ks) if ks else "-",
                 statistics.median(ds) if ds else "-"))


if __name__ == "__main__":
    v = load("v515[A-R].tsv") + load("v515R[A-C].tsv")
    b = load("p514nd[A-R].tsv") + load("p514ndR[A-C].tsv")
    report("v515 FIRED (all blocks)", v)
    report("p514nd baseline (all blocks)", b)
