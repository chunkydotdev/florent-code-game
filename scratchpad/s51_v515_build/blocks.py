#!/usr/bin/env python3
"""Per-BLOCK paired read of the headline pair.

Each block is 30 games on one seed range, both arms on the SAME seeds.  The
point of printing blocks rather than a pooled number is that the measured
same-config spread on this fixture is large, so a single pooled separation can
be read two ways and the block series cannot.
"""
import glob
import os
import re
import sys


def wins(path):
    if not os.path.exists(path):
        return None
    n = w = k = 0
    with open(path) as fh:
        hdr = fh.readline().rstrip("\n").split("\t")
        for line in fh:
            f = dict(zip(hdr, line.rstrip("\n").split("\t")))
            if len(f) < len(hdr):
                continue
            n += 1
            if f["ours"] == "US":
                w += 1
                if "Core destroyed" in f["cond"] and int(f["turn"]) <= 300:
                    k += 1
    return n, w, k


def main():
    a, b = sys.argv[1], sys.argv[2]
    blocks = sorted(set(
        re.sub(r"^.*/%s(.*)\.tsv$" % a, r"\1", p)
        for p in glob.glob("grid/%s*.tsv" % a)))
    print("block\t%s\t%s\tdelta_wins\t%s_k300\t%s_k300" % (a, b, a, b))
    ta = tb = tn = tka = tkb = 0
    for blk in blocks:
        ra = wins("grid/%s%s.tsv" % (a, blk))
        rb = wins("grid/%s%s.tsv" % (b, blk))
        if not ra or not rb or ra[0] != rb[0]:
            print("%s\tINCOMPLETE\t%s\t%s" % (blk, ra, rb))
            continue
        print("%s\t%d/%d\t%d/%d\t%+d\t%d\t%d"
              % (blk, ra[1], ra[0], rb[1], rb[0], ra[1] - rb[1], ra[2], rb[2]))
        tn += ra[0]
        ta += ra[1]
        tb += rb[1]
        tka += ra[2]
        tkb += rb[2]
    print("POOLED\t%d/%d (%.1f%%)\t%d/%d (%.1f%%)\t%+d\t%d (%.1f%%)\t%d (%.1f%%)"
          % (ta, tn, 100.0 * ta / tn, tb, tn, 100.0 * tb / tn, ta - tb,
             tka, 100.0 * tka / tn, tkb, 100.0 * tkb / tn))
    # naive two-sample 95% half-width, games treated as independent.
    p = (ta + tb) / (2.0 * tn)
    hw = 1.96 * (p * (1 - p) * 2.0 / tn) ** 0.5
    pk = (tka + tkb) / (2.0 * tn)
    hwk = 1.96 * (pk * (1 - pk) * 2.0 / tn) ** 0.5
    print("naive two-sample 95%% half-width: wins %.1fpp  k<=300 %.1fpp"
          % (100 * hw, 100 * hwk))


if __name__ == "__main__":
    main()
