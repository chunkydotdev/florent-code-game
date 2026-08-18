#!/usr/bin/env python3
"""Mechanism-log reader for the s51 v515 build.

Three counters, one per change, each read off a log line the arm and its mutant
both emit, so "zero" and "nonzero" are the same instrument in both arms:

  door   `FS DOOR <rnd> id ... n ...`  -- one line per door PECK (main.py)
  gate   `SENT515 <rnd> at ... gate (rnd, salt, eco, orth) latch (...)`
  reach  `EVICT515 <rnd> at ... ucov N cov N ceil N ceiltile ...`

⛔ Every counter below is driven to BOTH verdicts by `mech_selftest.py`.
"""
import os
import re
import sys
import glob
import collections


def games(d):
    """{tag: [stderr lines]} for one arm's log directory."""
    out = {}
    for p in sorted(glob.glob(os.path.join(d, "*.err"))):
        tag = os.path.basename(p)[:-4]
        out[tag] = open(p, errors="replace").read().splitlines()
    return out


def mapof(tag):
    m = re.match(r".*?_([a-z]+)_g\d+$", tag)
    return m.group(1) if m else "?"


def door(d, label):
    g = games(d)
    tot = 0
    withany = 0
    for tag, lines in g.items():
        n = sum(1 for L in lines if L.startswith("FS DOOR "))
        tot += n
        withany += 1 if n else 0
    print("DOOR\t%s\tgames %d\tpeck_events %d\tgames_with_a_peck %d"
          % (label, len(g), tot, withany))
    return tot


def gate(d, label):
    g = games(d)
    rows = []
    permap = collections.defaultdict(lambda: [0, 0, [], 0, 0])
    for tag, lines in g.items():
        mp = mapof(tag)
        permap[mp][0] += 1
        first = None
        for L in lines:
            if not L.startswith("SENT515 "):
                continue
            f = L.split()
            rnd = int(f[1])
            m = re.search(r"gate \((\d+), (\d+), (\d+), (\-?\d+)\)", L)
            salt, eco = (int(m.group(2)), int(m.group(3))) if m else (-1, -1)
            if first is None:
                first = (rnd, salt, eco)
                permap[mp][1] += 1
                permap[mp][2].append(rnd)
                permap[mp][3] += salt if salt > 0 else 0
                permap[mp][4] += eco if eco > 0 else 0
            rows.append((tag, mp, rnd, salt, eco))
    print("GATE\t%s" % label)
    print("  map\tgames\tgames_with_sentinel\tfirst_sent_rounds\t"
          "first_by_SALT\tfirst_by_ECO")
    for mp in sorted(permap):
        n, k, rr, s, e = permap[mp]
        print("  %s\t%d\t%d\t%s\t%d\t%d"
              % (mp, n, k, ",".join(str(x) for x in sorted(rr)), s, e))
    tot = sum(v[1] for v in permap.values())
    allr = sorted(r for v in permap.values() for r in v[2])
    print("  TOTAL\tgames %d\twith_sentinel %d\tfirst rounds %s"
          % (sum(v[0] for v in permap.values()), tot, allr))
    return rows


def reach(d, label):
    g = games(d)
    dist = collections.Counter()
    ceil = collections.Counter()
    rows = []
    for tag, lines in g.items():
        for L in lines:
            if not L.startswith("EVICT515 "):
                continue
            m = re.search(r"ucov (\-?\d+) cov (\-?\d+) ceil (\-?\d+)", L)
            if not m:
                continue
            u, c, ce = int(m.group(1)), int(m.group(2)), int(m.group(3))
            dist[u] += 1
            ceil[ce] += 1
            rows.append((tag, mapof(tag), u, c, ce))
    print("REACH\t%s\tgames %d\tevictors_built %d" % (label, len(g), len(rows)))
    print("  ucov distribution: %s"
          % dict(sorted(dist.items())))
    print("  ceiling distribution: %s" % dict(sorted(ceil.items())))
    print("  evictors at ucov>=1: %d\tat ucov>=2: %d"
          % (sum(v for k, v in dist.items() if k >= 1),
             sum(v for k, v in dist.items() if k >= 2)))
    return rows


if __name__ == "__main__":
    S = os.path.dirname(os.path.abspath(__file__))
    L = os.path.join(S, "logs")
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "door"):
        door(os.path.join(L, "m_door"), "FIRED (door off)")
        door(os.path.join(L, "m_dooron"), "MUTANT (door on)")
    if which in ("all", "gate"):
        gate(os.path.join(L, "m_gate"), "FIRED (floor 60)")
        gate(os.path.join(L, "m_gate0"), "MUTANT (floor 0 == v514)")
    if which in ("all", "reach"):
        reach(os.path.join(L, "m_reach"), "FIRED (reach on)")
        reach(os.path.join(L, "m_reachoff"), "MUTANT (reach off, probe on)")
