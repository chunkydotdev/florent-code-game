#!/usr/bin/env python3
"""population_diff.py -- before you compare two groups, find out how they differ.

WHY THIS EXISTS: FIVE TIMES IN ONE SESSION (research arm, s48, 2026-08-17) I
compared two groups and called the difference a variable, when the groups were
drawn from different populations.

    cut-round             two designs, opposite signs      -> not identified
    rebuild conditionality  near-gunner vs far-from-gunner
                            = CONTESTED FORWARD TILES vs everything else
    home-vs-forward turret  HOME SPACE vs FORWARD SPACE, not one placement
                            under two treatments            -> row withdrawn
    opening-builder size    count varies because the bot was STARVED
    v116 vs v125 harvester  THE MAP POOL ROTATED between the eras: 10 of 15
                            maps differ.  On the 5 common maps the medians are
                            IDENTICAL.  The "3-4 round regression" did not
                            exist, and an agent was already running to explain
                            it.

⛔ THE LAST ONE IS THE REASON THIS IS A TOOL AND NOT A RULE.  The correcting
fact was in `CLAUDE.md`.  I had QUOTED THE MAP ROTATION TWICE THAT DAY in other
contexts.  I still did not apply it to my own cut.

    ⇒ KNOWING A CONFOUND IN ONE CONTEXT DOES NOT CARRY IT TO THE NEXT.

Attention-based fixes for this class have now failed repeatedly in this repo:
the interval-ordering rule needed `cluster_ci.py`, the timestamp rule needed a
`printf`-with-`$NOW` idiom, and `FIRINGS-BEFORE-PRIMARY` inverted on its first
real test.  So: no rule.  A command that answers "how do these two groups
differ?" in one call, and prints the answer whether or not you thought to ask.

------------------------------------------------------------------------------
WHAT IT COMPARES

Given two selections of replay files (by `ourver`, by date, by opponent, or by
an explicit file list), it reports for each side:

  * MAP mix              -- the one that fired today; the pool rotates
  * OPPONENT mix         -- who you played is not who they played
  * FIXTURE mix          -- rated vs unrated pools different bots entirely
  * OPPONENT-VERSION mix -- their ship inside your window
  * n, and the OVERLAP   -- Jaccard on each dimension

and then, loudly, the dimensions where overlap is low.

⛔ IT DOES NOT TELL YOU WHETHER YOUR COMPARISON IS VALID, AND IT HAS NO OUTPUT
MODE THAT SAYS SO.  On a clean run it prints the numbers and the moved keys and
stops -- no summary, nothing quotable as a pass.  A TOOL THAT CANNOT CERTIFY
SHOULD HAVE NO CERTIFYING OUTPUT MODE, which is `cluster_ci`'s rule applied
here: that one refuses a VERDICT below 30 clusters; this one can never earn a
clean verdict at all, because it knows four dimensions and the world has more.

Two further limits, both structural:
  * OVERLAP IS NOT CONFOUND MAGNITUDE.  A 0.90 overlap whose disagreeing 10%
    sits on a high-leverage key beats a 0.60 overlap spread over trivial ones.
    The quantity that matters is `overlap x leverage` and this tool sees only
    the first half -- leverage needs the outcome, which is the thing you are
    trying to measure.  So it prints WHICH keys moved and by how much share:
    a domain-aware reader can price those, and cannot price a scalar.
  * IT KNOWS FOUR DIMENSIONS.  Space, time-of-day, CPU load and anything else
    are invisible to it.

------------------------------------------------------------------------------
USAGE

    tools/population_diff.py --ourver-a 104,114,115,116 --ourver-b 125,139,140,152,155
    tools/population_diff.py --ourver-a 152 --ourver-b 155
    tools/population_diff.py --opp-a gsxWins --opp-b Clankers
    tools/population_diff.py --ourver-a 152 --ourver-b 155 --common-maps
    tools/population_diff.py --selftest

`--common-maps` prints the file lists restricted to maps present in BOTH, which
is the repair for the failure that motivated this file.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LADDER = os.path.join(REPO, "corpus", "ladder_games.tsv")
LOW_OVERLAP = 0.70   # a convention, and the design does not depend on its value


def load():
    rows = []
    with open(LADDER) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            rows.append(r)
    return rows


def select(rows, ourver=None, opp=None):
    out = rows
    if ourver:
        want = set(ourver)
        out = [r for r in out if r.get("ourver") in want]
    if opp:
        out = [r for r in out if r.get("opp") == opp]
    return out


def jaccard(a: Counter, b: Counter):
    ka, kb = set(a), set(b)
    return len(ka & kb) / len(ka | kb) if (ka | kb) else 1.0


def share_overlap(a: Counter, b: Counter):
    """Sum of min(share) across keys -- 1.0 if the mixes are identical, 0.0 if
    disjoint.  Stricter than Jaccard: it notices when the SAME keys appear in
    very different proportions, which Jaccard cannot see."""
    ta, tb = sum(a.values()), sum(b.values())
    if not ta or not tb:
        return 0.0
    keys = set(a) | set(b)
    return sum(min(a[k] / ta, b[k] / tb) for k in keys)


DIMS = [("map", "MAP"), ("opp", "OPPONENT"), ("oppver", "OPP VERSION")]


def report(A, B, la, lb):
    print(f"POPULATION DIFF   A = {la}  (n={len(A):,})   B = {lb}  (n={len(B):,})")
    if not A or not B:
        print("REFUSED: one side is empty; there is nothing to compare.")
        return 2
    flagged = []
    for key, label in DIMS:
        ca, cb = Counter(r.get(key) for r in A), Counter(r.get(key) for r in B)
        j, s = jaccard(ca, cb), share_overlap(ca, cb)
        mark = "  " if s >= LOW_OVERLAP else "**"
        print(f"\n{mark} {label}: keys {len(ca)} vs {len(cb)}   "
              f"Jaccard {j:.2f}   SHARE-OVERLAP {s:.2f}")
        # ⛔ ALWAYS PRINT THE KEYS THAT MOVED, NOT ONLY THE SCALAR.
        #
        # The side lane's objection, and it is the one that makes the scalar
        # dangerous rather than merely incomplete: OVERLAP MEASURES POPULATION
        # SIMILARITY, NOT CONFOUND MAGNITUDE.  A 0.90 overlap whose disagreeing
        # 10% sits on a HIGH-LEVERAGE key can move an estimate more than a 0.60
        # overlap spread over low-leverage ones.  The quantity that matters is
        # `overlap x leverage` and this tool can only see the first half --
        # leverage needs the outcome, which is exactly what you are trying to
        # measure.
        #
        # ⇒ so it must not IMPLY it has priced leverage.  It prints WHICH keys
        # moved and by how much share, because a domain-aware reader CAN price
        # them: "is that the map my mechanism lives on?" is answerable from a
        # key list and unanswerable from a scalar.
        ta, tb = sum(ca.values()), sum(cb.values())
        gaps = sorted(((abs(ca[k] / ta - cb[k] / tb), k) for k in set(ca) | set(cb)),
                      reverse=True)
        shown = [f"{k}({ca[k] / ta:.2f}->{cb[k] / tb:.2f})" for g, k in gaps[:8] if g > 0.005]
        if shown:
            print(f"     biggest share moves: {', '.join(shown)}"
                  + (" ..." if len(gaps) > 8 else ""))
        only_a = sorted(set(ca) - set(cb))
        only_b = sorted(set(cb) - set(ca))
        if only_a:
            print(f"     only in A ({len(only_a)}): {', '.join(map(str, only_a[:12]))}"
                  + (" ..." if len(only_a) > 12 else ""))
        if only_b:
            print(f"     only in B ({len(only_b)}): {', '.join(map(str, only_b[:12]))}"
                  + (" ..." if len(only_b) > 12 else ""))
        if s < LOW_OVERLAP:
            flagged.append((label, s))
    print()
    if flagged:
        print("⛔ LOW OVERLAP ON: " + ", ".join(f"{l} ({s:.2f})" for l, s in flagged))
        print("   These are CANDIDATE CONFOUNDS. A difference between A and B may be")
        print("   the dimension rather than the variable you meant to study.")
        print("   For MAP, --common-maps gives the repair; for the others, restrict or")
        print("   stratify before quoting any contrast.")
    # ⛔⛔ THERE IS DELIBERATELY NO "CLEAN" BRANCH HERE.
    #
    # The first version printed "No dimension below the overlap convention" on a
    # clean run, plus a disclaimer saying that was not a clean bill of health.
    # The side lane pointed out that this is the very failure this repo banked
    # hours earlier -- "an honest disclaimer feels like diligence and can
    # substitute for the looking that would have removed the need for it" -- and
    # that the argument against it is `cluster_ci`'s own:
    #
    #     A TOOL THAT CANNOT CERTIFY SHOULD HAVE NO CERTIFYING OUTPUT MODE.
    #
    # `cluster_ci` refuses a VERDICT below 30 clusters.  This tool can NEVER
    # earn a clean verdict, because it knows four dimensions and the world has
    # more.  So it refuses one ALWAYS: the numbers and the moved keys are the
    # output, and there is no summary line for a reader to quote as a pass.
    #
    # The author's own failure is the argument: I corrected for maps, believed
    # I was done, and the tool then found OPPONENT and OPP-VERSION at the same
    # overlap.  Had a four-dimension tool printed "no dimension flagged" that
    # day, I would have stopped looking -- and there is no fifth-dimension
    # checker to catch that one.
    return 1 if flagged else 0


def common_maps(A, B):
    ma, mb = {r.get("map") for r in A}, {r.get("map") for r in B}
    common = ma & mb
    print(f"MAPS COMMON TO BOTH: {len(common)} of {len(ma | mb)}")
    print("  " + ", ".join(sorted(x for x in common if x)))
    a2 = [r for r in A if r.get("map") in common]
    b2 = [r for r in B if r.get("map") in common]
    print(f"  restricted n: A {len(A):,} -> {len(a2):,}   B {len(B):,} -> {len(b2):,}")
    return a2, b2


def selftest():
    ok = True
    A = [{"map": "antler", "opp": "X", "oppver": "1"} for _ in range(50)]
    B = [{"map": "antler", "opp": "X", "oppver": "1"} for _ in range(50)]
    print("  CASE A -- identical populations, must NOT flag:")
    rc = report(A, B, "identical", "identical")
    if rc != 0:
        print("  ** FAIL: identical populations flagged **")
        ok = False
    print("\n  CASE B -- disjoint map pools, MUST flag (this is the s48 failure):")
    B2 = [{"map": "midgard", "opp": "X", "oppver": "1"} for _ in range(50)]
    rc = report(A, B2, "pool 1", "pool 2")
    if rc != 1:
        print("  ** FAIL: a fully disjoint map pool must be flagged -- if it is not,")
        print("     the tool cannot catch the failure it was built for **")
        ok = False
    print("\n  CASE C -- SAME keys, very different PROPORTIONS. Jaccard cannot see this;")
    print("            share-overlap must. If C passes unflagged the strict measure is inert:")
    A3 = [{"map": "antler", "opp": "X", "oppver": "1"} for _ in range(90)] + \
         [{"map": "midgard", "opp": "X", "oppver": "1"} for _ in range(10)]
    B3 = [{"map": "antler", "opp": "X", "oppver": "1"} for _ in range(10)] + \
         [{"map": "midgard", "opp": "X", "oppver": "1"} for _ in range(90)]
    rc = report(A3, B3, "90/10", "10/90")
    if rc != 1:
        print("  ** FAIL: same keys at 90/10 vs 10/90 must flag on share-overlap **")
        ok = False
    print("\nSELFTEST PASS" if ok else "\nSELFTEST FAIL")
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ourver-a")
    ap.add_argument("--ourver-b")
    ap.add_argument("--opp-a")
    ap.add_argument("--opp-b")
    ap.add_argument("--common-maps", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not ((a.ourver_a or a.opp_a) and (a.ourver_b or a.opp_b)):
        ap.error("give a selection for BOTH sides (--ourver-a/--ourver-b or --opp-a/--opp-b)")
    if not os.path.exists(LADDER):
        print(f"REFUSED: {LADDER} not present.", file=sys.stderr)
        return 2
    rows = load()
    A = select(rows, a.ourver_a.split(",") if a.ourver_a else None, a.opp_a)
    B = select(rows, a.ourver_b.split(",") if a.ourver_b else None, a.opp_b)
    la = a.ourver_a or a.opp_a
    lb = a.ourver_b or a.opp_b
    rc = report(A, B, la, lb)
    if a.common_maps:
        print()
        common_maps(A, B)
    return rc


if __name__ == "__main__":
    sys.exit(main())
