#!/usr/bin/env python3
"""v539 build instrument #2 -- the paired aggregator for the famine harness.

Reads harness `--endgame` rows (`k=v` TAB-separated, one per (map, arm, seed)
cell; any other line -- the bot's own log chatter -- is ignored) and prints a
PAIRED table: for each (map, seed) the parent and v539 values side by side, and
a sign test over the pairs.

⛔ PAIRED, NOT POOLED, AND THE REASON IS MEASURED.  The fixture is not
deterministic across PROCESSES: `fcode`'s enums hash by identity, so any set or
dict the bot keys on an enum iterates in a different order in a new
interpreter.  Within ONE process both arms see the same ordering, so a
(map, seed) PAIR is comparable and a cross-run absolute number is not.  Feed
this one harness invocation's output; compare two invocations as REPLICATES,
never by subtracting their absolute cells.

    .venv/bin/python scratchpad/s52_v539_build/agg.py --selftest
    .venv/bin/python scratchpad/s52_v539_build/agg.py OUT_endgame_run1.tsv
"""
import argparse
import sys
from collections import defaultdict

PARENT = "_v537socket"
ARM = "_v542wave"
METRICS = ("first_rebuild_rnd", "mouth_rounds_post", "deliv_sightings_post",
           "harv_built_post", "conv_built_post", "famine_rnd", "run_raised")


def parse(lines):
    rows = []
    for ln in lines:
        ln = ln.strip()
        if not ln.startswith("tree="):
            continue
        d = {}
        for part in ln.split("\t"):
            if "=" not in part:
                continue
            k, v = part.split("=", 1)
            d[k] = v
        if "tree" in d and "map" in d and "seed" in d:
            rows.append(d)
    return rows


def pair(rows):
    """{(map, seed): {arm: row}} -- only cells where BOTH arms are present."""
    by = defaultdict(dict)
    for r in rows:
        by[(r["map"], r["seed"])][r["tree"]] = r
    return {k: v for k, v in by.items() if PARENT in v and ARM in v}


def sign_test(pairs, metric, better="lower"):
    """(n_arm_better, n_parent_better, n_tie) over the paired cells."""
    a = b = t = 0
    for _k, v in sorted(pairs.items()):
        pv = int(v[PARENT][metric])
        av = int(v[ARM][metric])
        # a never-happened sentinel of -1 is WORSE than any real round, and
        # collapsing it to -1 would silently make "never rebuilt" look best.
        if metric == "first_rebuild_rnd":
            pv = 10 ** 6 if pv < 0 else pv
            av = 10 ** 6 if av < 0 else av
        if pv == av:
            t += 1
        elif (av < pv) == (better == "lower"):
            a += 1
        else:
            b += 1
    return a, b, t


def report(rows, out=sys.stdout):
    pairs = pair(rows)
    print("paired cells: %d  (maps %s)" % (
        len(pairs), sorted({k[0] for k in pairs})), file=out)
    print(file=out)
    hdr = "%-14s %-5s %-22s %-22s" % ("map", "seed", PARENT, ARM)
    print(hdr, file=out)
    print("%-14s %-5s %-22s %-22s" % ("", "", "rebuild/mouth/deliv",
                                      "rebuild/mouth/deliv"), file=out)
    for k in sorted(pairs):
        p, a = pairs[k][PARENT], pairs[k][ARM]
        print("%-14s %-5s %-22s %-22s" % (
            k[0], k[1],
            "%s/%s/%s" % (p["first_rebuild_rnd"], p["mouth_rounds_post"],
                          p["deliv_sightings_post"]),
            "%s/%s/%s" % (a["first_rebuild_rnd"], a["mouth_rounds_post"],
                          a["deliv_sightings_post"])), file=out)
    print(file=out)
    for m, better in (("first_rebuild_rnd", "lower"),
                      ("mouth_rounds_post", "higher"),
                      ("deliv_sightings_post", "higher"),
                      ("harv_built_post", "higher"),
                      ("conv_built_post", "higher")):
        a, b, t = sign_test(pairs, m, better)
        print("%-22s (%s is better)  v539 %2d | parent %2d | tie %2d"
              % (m, better, a, b, t), file=out)
    raised = sum(int(v[x]["run_raised"]) for v in pairs.values()
                 for x in (PARENT, ARM))
    fam = sum(1 for v in pairs.values() if int(v[ARM]["famine_rnd"]) >= 0)
    famp = sum(1 for v in pairs.values() if int(v[PARENT]["famine_rnd"]) >= 0)
    print(file=out)
    print("famine declared: v539 %d/%d cells | parent %d/%d (it has no "
          "detector)" % (fam, len(pairs), famp, len(pairs)), file=out)
    print("run() raised, both arms pooled: %d" % raised, file=out)
    return pairs


def selftest():
    fails = []

    def chk(c, m):
        print(("  ok   " if c else "  FAIL ") + m)
        if not c:
            fails.append(m)

    def row(tree, mp, sd, reb, mouth, deliv, fam):
        return ("tree=%s\tmap=%s\tharv_built_post=1\tfirst_rebuild_rnd=%d\t"
                "conv_built_post=1\tmouth_rounds_post=%d\t"
                "deliv_sightings_post=%d\tfamine_rnd=%d\trun_raised=0\t"
                "seed=%d" % (tree, mp, reb, mouth, deliv, fam, sd))

    print("[1] the parser ignores the bot's own log chatter")
    rows = parse(["BB48 REFUSE TI n=1 3/4", "L4R45 L4REPAIR rnd=4",
                  row(PARENT, "atoll", 0, 200, 5, 1, -1),
                  row(ARM, "atoll", 0, 160, 90, 20, 150)])
    chk(len(rows) == 2, "2 data rows parsed out of 4 lines")
    chk(len(parse(["BB48 REFUSE TI n=1 3/4"])) == 0,
        "a file of pure chatter parses to 0 rows (the other verdict)")

    print("[2] the sign test moves BOTH ways on inverted inputs")
    p1 = pair(rows)
    a, b, t = sign_test(p1, "first_rebuild_rnd", "lower")
    chk((a, b, t) == (1, 0, 0), "v539 wins when it rebuilds earlier")
    rows_inv = parse([row(PARENT, "atoll", 0, 160, 90, 20, -1),
                      row(ARM, "atoll", 0, 200, 5, 1, 150)])
    a2, b2, _ = sign_test(pair(rows_inv), "first_rebuild_rnd", "lower")
    chk((a2, b2) == (0, 1),
        "PARENT wins on the inverted fixture (the other verdict)")

    print("[3] 'never rebuilt' (-1) is scored as WORSE, not best")
    rows_never = parse([row(PARENT, "atoll", 0, -1, 0, 0, -1),
                        row(ARM, "atoll", 0, 300, 10, 2, 150)])
    a3, b3, _ = sign_test(pair(rows_never), "first_rebuild_rnd", "lower")
    chk((a3, b3) == (1, 0), "a real r300 beats a parent that never rebuilt")
    rows_never2 = parse([row(PARENT, "atoll", 0, 300, 10, 2, -1),
                         row(ARM, "atoll", 0, -1, 0, 0, 150)])
    a4, b4, _ = sign_test(pair(rows_never2), "first_rebuild_rnd", "lower")
    chk((a4, b4) == (0, 1),
        "and an arm that never rebuilt LOSES (the other verdict)")

    print("[4] unpaired cells are dropped, not half-counted")
    rows_un = parse([row(PARENT, "atoll", 0, 200, 5, 1, -1),
                     row(ARM, "eider", 0, 160, 90, 20, 150)])
    chk(len(pair(rows_un)) == 0, "no cell has both arms => 0 pairs")

    print()
    if fails:
        print("SELFTEST FAILED: %d" % len(fails))
        return 1
    print("SELFTEST PASSED")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", nargs="?")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.path:
        ap.print_help()
        return 0
    with open(a.path) as fh:
        report(parse(fh))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
