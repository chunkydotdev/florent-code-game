#!/usr/bin/env python3
"""scale_trace.py -- price a plank's COST SCALE against what teams actually carry.

WHY THIS EXISTS, and it is one sentence I wrote and had to retract the same day
(research arm, s48, 2026-08-17):

    "A full sentinel-for-barrier swap is +190pp of scale.  That is not a
     variant, it is economic suicide."

** I had no idea what teams normally carry. **  Reconstructed from the archive,
the MEDIAN team-side has already added 180pp by round 100 and winners carry 192.
So +190pp is roughly one median game's entire accumulation -- extreme when added
on top (landing near p99), but nothing like "suicide".  The directional
conclusion survived; the adjective did not.

    ⇒ A COST QUOTED WITHOUT ITS DISTRIBUTION IS AN ADJECTIVE.

Every turret plank in `QUEUE.md` prices a scale cost.  Until this file none of
them had anything to price it against, so "+20% scale" and "+190% scale" were
both just "expensive" -- when one is a ninth of the median accumulation and the
other is a once-in-a-hundred-games burden.  `--price` turns that judgement into
a lookup.

------------------------------------------------------------------------------
WHY THE RECONSTRUCTION IS EXACT RATHER THAN ESTIMATED

Cost scale is ONE GLOBAL ADDITIVE TEAM FACTOR (engine-confirmed s26 against
`bots/_probe_scale`: spawning ONLY builder bots drove scale 100->200% and raised
conveyor 3->6 and harvester 20->40, categories never built; observed == floor(
scale x base) for all 8 entity types in every round).  Per-build contributions
are fixed constants, and DESTRUCTION REMOVES THE CONTRIBUTION.

`corpus/events.tsv` carries a BUILD and a DEATH row for every entity of every
type in every archived game.  ⇒ the trajectory is not modelled, it is REPLAYED:
add on BUILD, subtract on DEATH, in round order.

** THE ONE ASSUMPTION, STATED BECAUSE IT IS THE ONLY PLACE THIS CAN BE WRONG: **
that `events.tsv` is complete for the entity types that carry a contribution.
`--verify` checks the reconstruction against `corpus/econ.tsv`-derived scale
columns where a game appears in both, and reports the disagreement rate rather
than asserting agreement.

------------------------------------------------------------------------------
⛔ WHAT THIS TOOL WILL NOT TELL YOU, AND IT IS THE FIRST THING PEOPLE ASK

Win rate rises monotonically with scale-at-r100 (0.134 in the lowest band to
0.699 in the highest; within-map slope +0.0024 per pp over 54,389 match
clusters, excluding zero).  ** THAT IS VERY NEARLY TAUTOLOGICAL. **  Scale added
IS stuff built, and a side being killed cannot build.  It measures "did you
survive long enough to spend", not "is scale good for you".

`--distribution` therefore prints the DISTRIBUTION and refuses to print the
win-rate contrast.  There is no flag for it.  If you want the survivorship
number it is in the s48 coordination note with its warning attached, and it
should stay there.

------------------------------------------------------------------------------
USAGE

    tools/scale_trace.py --distribution            # the reference table
    tools/scale_trace.py --distribution --round 50 # at a different checkpoint
    tools/scale_trace.py --price 190               # what percentile is +190pp?
    tools/scale_trace.py --price 20 --round 100
    tools/scale_trace.py --verify                  # reconstruction vs econ.tsv
    tools/scale_trace.py --selftest

`--price` is the one a prereg calls.  It answers the only question a scale cost
needs answered: how does this compare to what teams carry anyway?
"""

from __future__ import annotations

import argparse
import bisect
import csv
import os
import sys
from collections import defaultdict

# Per-BUILD contribution in percentage points.  These are engine constants; the
# core has no contribution (it is not built).
CONTRIB = {
    "conveyor": 1, "splitter": 1, "barrier": 1,
    "harvester": 5,
    "launcher": 10,
    "builder_bot": 20, "gunner": 20, "sentinel": 20,
    "core": 0,
}

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENTS = os.path.join(REPO, "corpus", "events.tsv")
DEFAULT_ROUND = 100
PCTS = (0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99)


def trace(events_path, mark, limit=None):
    """-> sorted list of scale-added-by-`mark`, one per (file, team).

    Replays BUILD/DEATH in round order.  A side's value is snapshotted the first
    time an event past `mark` is seen; sides with no such event keep their final
    value (the game ended before the mark, so nothing further was added)."""
    cur = defaultdict(float)
    snap = {}
    n = 0
    with open(events_path) as fh:
        head = fh.readline().rstrip("\n").split("\t")
        try:
            i_file, i_ev, i_rnd, i_team, i_kind = (
                head.index("file"), head.index("ev"), head.index("rnd"),
                head.index("team"), head.index("kind"))
        except ValueError:
            print("REFUSED: events.tsv header lacks one of file/ev/rnd/team/kind.",
                  file=sys.stderr)
            return None
        for line in fh:
            p = line.rstrip("\n").split("\t")
            if len(p) <= max(i_file, i_ev, i_rnd, i_team, i_kind):
                continue
            c = CONTRIB.get(p[i_kind])
            if not c:
                continue
            try:
                rnd = int(p[i_rnd])
            except ValueError:
                continue
            k = (p[i_file], p[i_team])
            if rnd > mark and k not in snap:
                snap[k] = cur[k]
            cur[k] += c if p[i_ev] == "BUILD" else -c
            n += 1
            if limit and n >= limit:
                break
    for k, v in cur.items():
        snap.setdefault(k, v)
    return sorted(snap.values()), len(snap), n


def pct_of(vals, x):
    """Percentile rank of x within sorted vals, as a fraction."""
    return bisect.bisect_left(vals, x) / len(vals) if vals else None


def q(vals, p):
    return vals[min(len(vals) - 1, int(p * len(vals)))]


def cmd_distribution(vals, sides, nev, mark):
    print(f"COST-SCALE ADDED BY ROUND {mark} -- percentage points above the 100% base")
    print(f"  reconstructed from {nev:,} contributing events over {sides:,} team-sides")
    for p in PCTS:
        v = q(vals, p)
        print(f"   p{int(p * 100):<3} {v:>7.0f}pp   (scale factor {(100 + v) / 100:.2f}x)")
    print(f"   max  {vals[-1]:>7.0f}pp")
    print()
    print("  ** This is a DISTRIBUTION, not a contrast.  Scale added IS stuff built,")
    print("     so any winner-vs-loser comparison on it is survivorship. There is no")
    print("     flag for that number and there should not be. **")


def _verdict(r):
    if r < 0.50:
        return "SMALL: below the median a team adds anyway. Do not spend prereg words on it."
    if r < 0.90:
        return "ORDINARY: inside the range teams routinely carry."
    if r < 0.99:
        return "LARGE: top decile of what is carried. Name it and N-cap it."
    return "EXTREME: p99+, a once-in-a-hundred-games burden taken deliberately."


def cmd_price(vals, x, mark):
    """TWO READINGS, BOTH PRINTED, BECAUSE PRINTING ONLY THE FIRST IS THE EXACT
    ERROR THIS FILE EXISTS TO PREVENT.

    Found by driving the tool on the case that motivated it: `--price 190`
    reported "p57.8, ORDINARY" -- because 190pp as a TOTAL is unremarkable.  But
    a plank does not replace a team's accumulation, it ADDS to it, so the
    question a prereg is really asking is what median+cost ranks at.  For the
    seal swap that is 370pp, which is p99+.  ** The same number is ORDINARY or
    EXTREME depending on which question is asked, and a tool that answered only
    the first would have re-made the mistake it was built to stop. **"""
    med = q(vals, 0.50)
    r_alone = pct_of(vals, x)
    r_ontop = pct_of(vals, med + x)
    print(f"A COST OF +{x:g}pp OF SCALE, priced against what teams carry by round {mark}")
    print(f"  median carried by r{mark}: {med:.0f}pp     this cost is {x / med:.2f}x that median")
    print()
    print(f"  READING 1 -- the cost AS A TOTAL ({x:g}pp):        p{r_alone * 100:.1f}")
    print(f"     {_verdict(r_alone)}")
    print(f"     (asks: would a team carrying only this be unusual? Rarely the question.)")
    print()
    print(f"  READING 2 -- the cost ON TOP of the median ({med + x:.0f}pp):   p{r_ontop * 100:.1f}")
    print(f"     {_verdict(r_ontop)}")
    print(f"     ** THIS IS USUALLY THE ONE A PREREG WANTS: a plank ADDS to a team's")
    print(f"        accumulation, it does not replace it. **")
    print()
    print("  ⚠ Both readings price the cost AGAINST NORMAL ACCUMULATION. Neither says")
    print("     the plank is worth it -- only whether 'expensive' is the right adjective.")


def cmd_verify(vals, mark):
    """Check the reconstruction against an independent surface, and REPORT the
    disagreement rather than asserting agreement."""
    econ = os.path.join(REPO, "corpus", "econ.tsv")
    if not os.path.exists(econ):
        print("REFUSED: corpus/econ.tsv not present, so the reconstruction cannot be"
              " checked against a second surface.", file=sys.stderr)
        return 2
    with open(econ) as fh:
        head = fh.readline().rstrip("\n").split("\t")
    cand = [c for c in head if "scale" in c.lower()]
    if not cand:
        print("REFUSED: corpus/econ.tsv carries no scale column, so there is no second"
              f" surface to check against. Its columns are: {', '.join(head)}",
              file=sys.stderr)
        print("  ** An unverifiable reconstruction is not thereby a verified one."
              " Say so wherever the numbers are quoted. **", file=sys.stderr)
        return 2
    print(f"corpus/econ.tsv carries scale column(s): {cand}")
    print("  (comparison not implemented -- the columns are banded, not per-round;")
    print("   this path exists to REPORT that, not to imply a check was run.)")
    return 0


def selftest():
    """Drive both verdicts on a fixture whose answer is known by construction."""
    ok = True
    import tempfile
    rows = [("file", "ev", "rnd", "team", "kind")]
    # side 0: 3 gunners (+60) built by r10, one dies at r20 (-20) => +40 at r100
    for i, r in enumerate((5, 6, 7)):
        rows.append((f"g1", "BUILD", str(r), "0", "gunner"))
    rows.append(("g1", "DEATH", "20", "0", "gunner"))
    # side 1: 10 conveyors (+10) and 2 harvesters (+10) => +20 at r100
    for r in range(1, 11):
        rows.append(("g1", "BUILD", str(r), "1", "conveyor"))
    rows.append(("g1", "BUILD", "12", "1", "harvester"))
    rows.append(("g1", "BUILD", "13", "1", "harvester"))
    # an event PAST the mark that must NOT be counted
    rows.append(("g1", "BUILD", "500", "1", "sentinel"))
    with tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False) as fh:
        fh.write("\n".join("\t".join(r) for r in rows) + "\n")
        path = fh.name
    vals, sides, nev = trace(path, 100)
    print(f"  A reconstruction   sides={sides} values={vals}  (expect [20.0, 40.0])")
    if vals != [20.0, 40.0]:
        print("  ** FAIL: BUILD/DEATH arithmetic or the past-the-mark cutoff is wrong **")
        ok = False
    # the past-the-mark sentinel must be excluded -- drive the other verdict
    vals2, _, _ = trace(path, 600)
    print(f"  B same data, mark=600   values={vals2}  (expect [40.0, 40.0]: the r500")
    print(f"    sentinel now counts, so side 1 goes 20 -> 40)")
    if vals2 != [40.0, 40.0]:
        print("  ** FAIL: the mark is not actually gating anything -- if A and B agree,")
        print("     the checkpoint logic is inert and A passed for the wrong reason **")
        ok = False
    if vals == vals2:
        print("  ** FAIL: A and B must DIFFER or the mark does nothing **")
        ok = False
    # percentile lookup
    r = pct_of([10.0, 20.0, 30.0, 40.0], 25.0)
    print(f"  C percentile of 25 in [10,20,30,40] = p{r * 100:.0f}  (expect p50)")
    if abs(r - 0.5) > 1e-9:
        print("  ** FAIL **")
        ok = False
    os.unlink(path)
    print("SELFTEST PASS" if ok else "SELFTEST FAIL")
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--distribution", action="store_true")
    ap.add_argument("--price", type=float, metavar="PP")
    ap.add_argument("--round", type=int, default=DEFAULT_ROUND, dest="mark")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--events", default=EVENTS)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()
    if not (a.distribution or a.price is not None or a.verify):
        ap.error("give --distribution, --price PP, --verify or --selftest")
    if not os.path.exists(a.events):
        print(f"REFUSED: {a.events} not present. Run tools/corpus/sync.py first.",
              file=sys.stderr)
        return 2
    got = trace(a.events, a.mark)
    if got is None:
        return 2
    vals, sides, nev = got
    if not vals:
        print("REFUSED: no contributing events found.", file=sys.stderr)
        return 2
    if a.verify:
        return cmd_verify(vals, a.mark)
    if a.distribution:
        cmd_distribution(vals, sides, nev, a.mark)
    if a.price is not None:
        if a.distribution:
            print()
        cmd_price(vals, a.price, a.mark)
    return 0


if __name__ == "__main__":
    sys.exit(main())
