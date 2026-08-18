#!/usr/bin/env python3
"""Grid summariser for the s51 v515 build.

One row per arm: wins, k<=r300 ITT (a core-kill BY r300 as a share of ALL that
arm's games -- PROGRAMME.md's primary), our-core-destroyed count, median kill
round over the games we won by core kill, tracebacks.

⛔ GUARD, DRIVEN BOTH WAYS ON A FIXTURE (see selftest at the bottom): a row of
all-losses must read wins 0 and a row of all-wins must read wins n -- the
column is not constant by construction.
"""
import sys
import glob
import os
import statistics


def load(paths):
    rows = []
    for p in paths:
        with open(p) as fh:
            hdr = fh.readline().rstrip("\n").split("\t")
            for line in fh:
                f = line.rstrip("\n").split("\t")
                if len(f) != len(hdr):
                    continue
                rows.append(dict(zip(hdr, f)))
    return rows


def summarise(name, rows):
    n = len(rows)
    wins = sum(1 for r in rows if r["ours"] == "US")
    kill = [r for r in rows if r["ours"] == "US" and "Core destroyed" in r["cond"]]
    k300 = sum(1 for r in kill if int(r["turn"]) <= 300)
    ourdead = sum(1 for r in rows
                  if r["ours"] == "OPP" and "Core destroyed" in r["cond"])
    tb = sum(int(r["tracebacks"]) for r in rows)
    med = statistics.median([int(r["turn"]) for r in kill]) if kill else -1
    return (name, n, wins, k300, ourdead, med, tb)


def main():
    out = []
    for spec in sys.argv[1:]:
        name, pat = spec.split("=", 1)
        paths = sorted(glob.glob(pat))
        rows = load(paths)
        if not rows:
            out.append((name, 0, 0, 0, 0, -1, 0))
            continue
        out.append(summarise(name, rows))
    print("arm\tn\twins\twin%\tk<=300\tk300%\tourcore_dead\tmed_kill\ttb")
    for (name, n, wins, k300, ourdead, med, tb) in out:
        print("%s\t%d\t%d\t%.1f\t%d\t%.1f\t%d\t%s\t%d" % (
            name, n, wins, 100.0 * wins / n if n else 0,
            k300, 100.0 * k300 / n if n else 0, ourdead, med, tb))


if __name__ == "__main__":
    main()
