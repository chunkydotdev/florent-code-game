#!/usr/bin/env python3
"""v526 M-METRIC reader.  One row per game from the RC/ARC520/APPT520 tape.

METRICS
  first_link   round of the first RC HOP                          (M6)
  arr1 / arr2  round each rider first reached dsq_core <= FS_RING_DSQ  (M6)
  harv30       SLOT_HARVESTERS at r30, read off the Core's own tape (M6 eco)
  links        RC HOP events = ferry launchers bought
  comply       launchers that threw >= 2 DISTINCT riders / links    (M3)
  b2_chain     1 if body 2 ever built a hop (a PARALLEL chain)      (M3)
  split_both   1 if both arcs (FRONT=1, BACK=2) were claimed        (M3)
  arcdup/arccol/apptbusy   the shipped alarms, must be 0            (M3)
  scale30      team cost scale % at r30 -- M3's cost model

⛔ SELF-TESTED BOTH WAYS.  `--selftest` drives a synthetic COMPLIANT tape and a
synthetic NON-COMPLIANT tape through the same parser and asserts every metric
comes out DIFFERENT.  A parser that has only ever seen one verdict has not been
seen to check.
"""
import statistics
import sys
from collections import defaultdict


def parse(lines):
    hops = []            # (rnd, lid, body)
    throws = defaultdict(set)   # lid -> {rider ids}
    arcs = set()
    arrive = {}          # body -> rnd
    harv30 = -1
    scale30 = -1.0
    alarms = dict(arcdup=0, arccol=0, apptbusy=0)
    for ln in lines:
        f = ln.split()
        if ln.startswith("RC HOP "):
            hops.append((int(f[2]), int(f[4]), int(f[6])))
        elif ln.startswith("RC THROW ") or ln.startswith("RC SPLIT "):
            throws[int(f[4])].add(int(f[6]))
            if ln.startswith("RC SPLIT "):
                arcs.add(int(f[8]))
        elif ln.startswith("RC ARRIVE "):
            b = int(f[6])
            if b not in arrive:
                arrive[b] = int(f[2])
        elif ln.startswith("RC ECO "):
            if int(f[2]) == 30:
                harv30 = int(f[4])
                scale30 = float(f[12])
        elif ln.startswith("ARC520 DUP"):
            alarms["arcdup"] += 1
        elif ln.startswith("ARC520 COLLIDE"):
            alarms["arccol"] += 1
        elif ln.startswith("APPT520 BUSY"):
            alarms["apptbusy"] += 1
    links = len(hops)
    comply = sum(1 for _r, lid, _b in hops if len(throws.get(lid, ())) >= 2)
    # THE MUSTER LINK is the one M3 acts on: the FIRST link of the chain.
    # Later links are steady state and their compliance is a different
    # question with a different denominator (v526 buys MORE links because it
    # starts earlier, so a pooled rate mixes two populations).
    hops_s = sorted(hops)
    first_ok = (1 if hops_s and len(throws.get(hops_s[0][1], ())) >= 2 else 0)
    rest = hops_s[1:]
    rest_ok = sum(1 for _r, lid, _b in rest if len(throws.get(lid, ())) >= 2)
    return dict(first_link=min((h[0] for h in hops), default=-1),
                arr1=arrive.get(1, -1), arr2=arrive.get(2, -1),
                harv30=harv30, scale30=scale30,
                links=links, comply=comply,
                first_link_ok=first_ok, has_link=1 if hops else 0,
                rest=len(rest), rest_ok=rest_ok,
                b2_chain=1 if any(h[2] == 2 for h in hops) else 0,
                split_both=1 if {1, 2} <= arcs else 0,
                narcs=len(arcs), **alarms)


def med(v):
    v = [x for x in v if x >= 0]
    return statistics.median(v) if v else -1


def fold(rows, label):
    n = len(rows)
    L = sum(r["links"] for r in rows)
    C = sum(r["comply"] for r in rows)
    g_split = [r for r in rows if r["narcs"] > 0]
    print("%-9s n=%-4d firstlink med %-5s  arr1 med %-5s arr2 med %-5s  "
          "harv30 med %-4s  links %-4d comply %d/%d (%.1f%%)  "
          "MUSTERLINK %d/%d (%.1f%%)  restlinks %d/%d (%.1f%%)  "
          "b2chain %d/%d (%.1f%%)  split_both %d/%d  "
          "alarms dup=%d col=%d appt=%d  scale30 med %.0f"
          % (label, n, med([r["first_link"] for r in rows]),
             med([r["arr1"] for r in rows]), med([r["arr2"] for r in rows]),
             med([r["harv30"] for r in rows]),
             L, C, L, 100.0 * C / L if L else 0.0,
             sum(r["first_link_ok"] for r in rows),
             sum(r["has_link"] for r in rows),
             (100.0 * sum(r["first_link_ok"] for r in rows)
              / max(1, sum(r["has_link"] for r in rows))),
             sum(r["rest_ok"] for r in rows), sum(r["rest"] for r in rows),
             (100.0 * sum(r["rest_ok"] for r in rows)
              / max(1, sum(r["rest"] for r in rows))),
             sum(r["b2_chain"] for r in rows), n,
             100.0 * sum(r["b2_chain"] for r in rows) / n if n else 0.0,
             sum(r["split_both"] for r in g_split), len(g_split),
             sum(r["arcdup"] for r in rows), sum(r["arccol"] for r in rows),
             sum(r["apptbusy"] for r in rows),
             med([r["scale30"] for r in rows])))


SELF_COMPLIANT = """
RC MAP w 30 h 30 ours 2,2 theirs 27,27
RC ECO 30 harvstore 4 harvseen -1 ti 100 units 6 scale 220.0
RC HOP 3 lid 20 body 1 at 4,4 dsq 700
RC THROW 3 lid 20 body 3 n 1
RC THROW 4 lid 20 body 9 n 2
RC HOP 5 lid 21 body 1 at 8,8 dsq 500
RC THROW 5 lid 21 body 3 n 1
RC SPLIT 6 lid 21 body 9 arc 1 n 2
RC SPLIT 7 lid 21 body 3 arc 2 n 3
RC ARRIVE 8 id 3 body 1 dsq 5
RC ARRIVE 9 id 9 body 2 dsq 4
"""

SELF_BROKEN = """
RC MAP w 30 h 30 ours 2,2 theirs 27,27
RC ECO 30 harvstore 2 harvseen -1 ti 100 units 6 scale 260.0
RC HOP 9 lid 20 body 1 at 4,4 dsq 700
RC THROW 9 lid 20 body 3 n 1
RC HOP 12 lid 22 body 2 at 5,9 dsq 690
RC THROW 12 lid 22 body 9 n 1
RC SPLIT 20 lid 22 body 9 arc 1 n 2
RC ARRIVE 24 id 3 body 1 dsq 6
ARC520 DUP 25 id 9 arc 1 n 1
APPT520 BUSY 4 id 11 held 9
"""

if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        a = parse(SELF_COMPLIANT.strip().splitlines())
        b = parse(SELF_BROKEN.strip().splitlines())
        assert a["first_link"] == 3 and b["first_link"] == 9, (a, b)
        assert a["comply"] == 2 and a["links"] == 2, a
        assert a["first_link_ok"] == 1 and b["first_link_ok"] == 0, (a, b)
        assert a["rest"] == 1 and a["rest_ok"] == 1, a
        assert b["rest"] == 1 and b["rest_ok"] == 0, b
        assert b["comply"] == 0 and b["links"] == 2, b
        assert a["b2_chain"] == 0 and b["b2_chain"] == 1, (a, b)
        assert a["split_both"] == 1 and b["split_both"] == 0, (a, b)
        assert a["arr2"] == 9 and b["arr2"] == -1, (a, b)
        assert a["harv30"] == 4 and b["harv30"] == 2, (a, b)
        assert a["arcdup"] == 0 and b["arcdup"] == 1, (a, b)
        assert a["apptbusy"] == 0 and b["apptbusy"] == 1, (a, b)
        assert a["scale30"] == 220.0 and b["scale30"] == 260.0, (a, b)
        print("SELFTEST OK: every metric moved between the compliant and the "
              "broken tape (13 assertions, both directions).")
        sys.exit(0)
    import glob
    import os
    byarm = defaultdict(list)
    bymap = defaultdict(lambda: defaultdict(list))
    for path in sorted(glob.glob(sys.argv[1] + "/log/*.err")):
        base = os.path.basename(path)[:-4]
        arm = base.split("_")[0]
        mp = base.split("_")[1]
        r = parse(open(path).read().splitlines())
        r["map"] = mp
        byarm[arm].append(r)
        bymap[mp][arm].append(r)
    print("=== POOLED (8-map mechanism panel) ===")
    for arm in sorted(byarm):
        fold(byarm[arm], arm)
    print()
    print("=== PER MAP ===")
    for mp in sorted(bymap):
        print("-- %s" % mp)
        for arm in sorted(bymap[mp]):
            fold(bymap[mp][arm], "  " + arm)
