#!/usr/bin/env python3
"""v530.1 HARVESTER-BOOTSTRAP PANEL -- the one column this build exists to move.

Reads `harv1` (round of OUR first harvester, -1 = never) off every replay in a
battery directory via `deliv.py`, and folds it per arm into the four numbers
`BUILD-REPORT-v530home-2026-08-20.md` §5.3 stated the defect on:

    noharv   share of games with NO harvester EVER      parent 0.000 / v530 0.096
    h1med    MEDIAN first-harvester round, CONDITIONAL  parent 5     / v530 8
    h1mean   MEAN   first-harvester round, CONDITIONAL  parent 5.79  / v530 42.74
    late60   share of games whose first harvester is after r60
                                                        parent 0.000 / v530 0.154

⛔ THE TWO DENOMINATORS ARE DIFFERENT AND BOTH ARE PRINTED.  `noharv` and
`late60` are over ALL games of the arm; `h1med`/`h1mean` are over the games
that HAVE a harvester (`n_h`).  A game with no harvester is EXCLUDED from the
mean, not counted as some large round -- which is exactly why the parent's mean
and median agree (5.79 vs 5) and v530's do not (42.74 vs 8): the mean is
dragged by the late tail while the never-games sit in `noharv`.  Pooling them
into one column would hide the finding inside the instrument.

SELFTEST (`--selftest`), every guard driven to the OTHER verdict:
  1. an all-early arm and an all-late arm fold to DIFFERENT h1med AND h1mean.
  2. a never-arm reads noharv 1.000 and n_h 0; its h1med/h1mean are -1, NOT 0
     -- a `-1` silently averaged in would read as an early harvester and would
     make this instrument report the defect as an improvement.
  3. `late60` separates an arm at r61 from one at r60 (the boundary is
     STRICTLY after r60, matching the report's wording).
  4. NOT A CONSTANT COLUMN: the three synthetic arms must produce three
     distinct `noharv` values.
"""
from __future__ import annotations

import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def fold(h1s):
    """h1s: list of first-harvester rounds, -1 for never."""
    n = len(h1s)
    ok = [x for x in h1s if x >= 0]
    return {
        "n": n,
        "n_h": len(ok),
        "noharv": (n - len(ok)) / n if n else -1.0,
        "h1med": statistics.median(ok) if ok else -1.0,
        "h1mean": (sum(ok) / len(ok)) if ok else -1.0,
        "late60": sum(1 for x in ok if x > 60) / n if n else -1.0,
    }


def hw(a, n1, b, n2):
    """Two-sample 95% half-width on a SHARE, in percentage points.

    Local fixture, no DEFF (s39 audit: pair-weighted local DEFF 0.98 on a
    balanced-by-construction shard fixture), so the platform constants are not
    applied.
    """
    if not n1 or not n2:
        return 0.0
    pb = (a + b) / (n1 + n2)
    return 1.96 * math.sqrt(pb * (1 - pb) * (1.0 / n1 + 1.0 / n2)) * 100


def main(repdirs, base_arm="parent"):
    import deliv
    byarm = defaultdict(list)
    bymap = defaultdict(list)
    nrep = 0
    for rd in repdirs:
        for p in sorted(Path(rd).glob("*.replay26")):
            r = deliv.row_for(p)
            if r is None:
                continue
            nrep += 1
            byarm[r["arm"]].append(r["harv1"])
            bymap[(r["arm"], r["map"])].append(r["harv1"])
    arms = sorted(byarm, key=lambda a: (a != base_arm, a))
    pool = {a: fold(byarm[a]) for a in arms}
    print("replays read: %d" % nrep)
    print("=== THE HARVESTER-BOOTSTRAP PANEL ===")
    print("%-10s %6s %6s %8s %7s %8s %8s"
          % ("arm", "n", "n_h", "noharv", "h1med", "h1mean", ">r60"))
    for a in arms:
        o = pool[a]
        print("%-10s %6d %6d %8.3f %7.1f %8.2f %8.3f"
              % (a, o["n"], o["n_h"], o["noharv"], o["h1med"], o["h1mean"],
                 o["late60"]))
    print()
    if base_arm in pool:
        b = pool[base_arm]
        bn = sum(1 for x in byarm[base_arm] if x < 0)
        for a in arms:
            if a == base_arm:
                continue
            o = pool[a]
            an = sum(1 for x in byarm[a] if x < 0)
            d = 100.0 * (o["noharv"] - b["noharv"])
            h = hw(an, o["n"], bn, b["n"])
            print("%-10s vs %-8s noharv %+6.2f pp (hw %.2f)  %s"
                  % (a, base_arm, d, h, "OUTSIDE" if abs(d) > h else "inside"))
            print("%-10s vs %-8s h1med  %.1f vs %.1f   h1mean %.2f vs %.2f"
                  % (a, base_arm, o["h1med"], b["h1med"], o["h1mean"],
                     b["h1mean"]))
            print("%-10s vs %-8s MEAN-MINUS-MEDIAN (the tail) %.2f vs %.2f"
                  % (a, base_arm, o["h1mean"] - o["h1med"],
                     b["h1mean"] - b["h1med"]))
            print()
    print("=== PER MAP: noharv share  (h1 median) ===")
    maps = sorted({m for (_, m) in bymap})
    print("%-14s %s" % ("map", "  ".join("%-16s" % a for a in arms)))
    for m in maps:
        cells = []
        for a in arms:
            o = fold(bymap.get((a, m), []))
            cells.append("%5.3f (%4.1f)  " % (o["noharv"], o["h1med"]))
        print("%-14s %s" % (m, "  ".join(cells)))


def selftest():
    early = fold([4, 5, 5, 6, 7])
    late = fold([70, 80, 90, 100, 110])
    never = fold([-1, -1, -1, -1, -1])
    mixed = fold([5, 5, -1, -1, 200])
    assert early["h1med"] != late["h1med"], "h1med does not separate"
    assert early["h1mean"] != late["h1mean"], "h1mean does not separate"
    assert never["noharv"] == 1.0 and never["n_h"] == 0
    assert never["h1med"] == -1.0 and never["h1mean"] == -1.0, \
        "a never-arm must read -1, never 0"
    assert early["noharv"] == 0.0
    assert abs(mixed["noharv"] - 0.4) < 1e-9
    assert mixed["h1mean"] == 70.0 and mixed["h1med"] == 5, \
        "the -1 rows must be EXCLUDED from the conditional mean, not averaged"
    b60 = fold([60, 60, 60, 60])
    b61 = fold([61, 61, 61, 61])
    assert b60["late60"] == 0.0 and b61["late60"] == 1.0, \
        "the >r60 boundary is not strict"
    assert len({early["noharv"], never["noharv"], mixed["noharv"]}) == 3, \
        "noharv is a constant column"
    # the two-sample half-width must also be driven to the other verdict
    assert hw(0, 100, 0, 100) == 0.0
    assert hw(50, 100, 10, 100) > 0.0
    print("SELFTEST OK: h1med and h1mean each separate an early arm from a late "
          "one; a never-arm reads noharv 1.000 / n_h 0 / h1med -1 (NOT 0) and "
          "its rows are excluded from the conditional mean (mixed: mean 70.0, "
          "median 5, noharv 0.400); the >r60 boundary is strict (r60 -> 0.000, "
          "r61 -> 1.000); the three synthetic arms give three distinct noharv "
          "values, so the column is not constant.")
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--selftest":
        sys.exit(selftest())
    base = "parent"
    if "--base" in a:
        i = a.index("--base")
        base = a[i + 1]
        a = a[:i] + a[i + 2:]
    main(a, base)
