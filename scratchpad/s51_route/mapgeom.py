#!/usr/bin/env python3
"""s51 ROUTE autopsy -- map LAYOUT (not scalar size) characterisation.

The s51 RING study closed the scalar-geometry road: royale / frostgate /
yulerune are all 20x20 at core d^2 = 196 and we take them 92% / 62% / 18%.
This module measures the things a scalar cannot see -- how many INDEPENDENT
corridors join the two cores, how narrow the narrowest is, and where the ore
sits relative to each core along the walkable graph.

Quantities (all on the CARDINAL passable graph, env != WALL):
  bfs          BFS steps from our core footprint to their core footprint
  mincut       max-flow / min VERTEX cut between the two core footprints
               == number of vertex-disjoint routes between the cores
  narrow       min over BFS levels of |tiles on some shortest path at that level|
  choke_tiles  passable tiles with <= 2 passable cardinal neighbours
  apron_free   passable tiles within d^2 <= 8 of a core (its spawn ring)
  ore_*        ore siting by BFS distance from each core

Usage:
  mapgeom.py --table               # all 15 pool maps, TSV
  mapgeom.py --selftest            # both-verdicts controls
  mapgeom.py <map>                 # one map, verbose
"""
from __future__ import annotations

import sys
from collections import deque
from pathlib import Path

if __name__ == "__main__":
    import sys as _hg
    if "-h" in _hg.argv[1:] or "--help" in _hg.argv[1:]:
        print(__doc__)
        raise SystemExit(0)

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from map_encode import parse_map26  # noqa: E402

CARD = ((0, -1), (1, 0), (0, 1), (-1, 0))
POOL = ["ragnarok", "royale", "nordkap", "frostgate", "drakkarfjord",
        "midgard", "valkyrie", "antler", "archipelago", "fjordgate",
        "drumlin", "glacierkeep", "yulerune", "auroraveil", "icefloe"]


def load(mapname):
    w, h, rows, cores = parse_map26(ROOT / "maps" / f"{mapname}.map26")
    anchors = {c[0]: (c[1], c[2]) for c in cores}
    return w, h, rows, anchors


def footprint(a):
    x, y = a
    return [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]


def passable(rows, w, h):
    return {(x, y) for y in range(h) for x in range(w) if rows[y][x] != 1}


def bfs_from(seeds, ok):
    dist = {t: 0 for t in seeds if t in ok}
    q = deque(dist)
    while q:
        t = q.popleft()
        for dx, dy in CARD:
            n = (t[0] + dx, t[1] + dy)
            if n in ok and n not in dist:
                dist[n] = dist[t] + 1
                q.append(n)
    return dist


def min_vertex_cut(ok, src, dst):
    """Unit-capacity vertex max-flow between two tile sets == # vertex-disjoint
    routes == min number of tiles whose removal separates the cores."""
    srcs, dsts = set(src) & ok, set(dst) & ok
    if not srcs or not dsts:
        return 0
    # node ids: (t, 0)=in (t, 1)=out.  cap(in->out)=1 except terminals (inf).
    INF = 10 ** 6
    cap = {}

    def add(u, v, c):
        cap[(u, v)] = cap.get((u, v), 0) + c
        cap.setdefault((v, u), 0)

    for t in ok:
        add((t, 0), (t, 1), INF if (t in srcs or t in dsts) else 1)
        for dx, dy in CARD:
            n = (t[0] + dx, t[1] + dy)
            if n in ok:
                add((t, 1), (n, 0), INF)
    S, T = ("S", 0), ("T", 1)
    for t in srcs:
        add(S, (t, 0), INF)
    for t in dsts:
        add((t, 1), T, INF)
    adj = {}
    for (u, v) in cap:
        adj.setdefault(u, set()).add(v)
    flow = 0
    while True:                                    # Edmonds-Karp
        prev, q = {S: None}, deque([S])
        while q and T not in prev:
            u = q.popleft()
            for v in adj.get(u, ()):
                if v not in prev and cap.get((u, v), 0) > 0:
                    prev[v] = u
                    q.append(v)
        if T not in prev:
            return flow
        b, v = INF, T
        while prev[v] is not None:
            b = min(b, cap[(prev[v], v)])
            v = prev[v]
        v = T
        while prev[v] is not None:
            cap[(prev[v], v)] -= b
            cap[(v, prev[v])] += b
            v = prev[v]
        flow += b


def narrowest_level(ok, da, db, bfs):
    """Width of the shortest-path bundle at its narrowest level."""
    on = [t for t in ok if t in da and t in db and da[t] + db[t] == bfs]
    if not on:
        return 0
    levels = {}
    for t in on:
        levels[da[t]] = levels.get(da[t], 0) + 1
    return min(levels.values())


def geom(mapname):
    w, h, rows, anchors = load(mapname)
    ok = passable(rows, w, h)
    fa, fb = footprint(anchors[0]), footprint(anchors[1])
    da, db = bfs_from(fa, ok), bfs_from(fb, ok)
    bfs = min((db[t] for t in fa if t in db), default=-1)
    ore = [(x, y) for y in range(h) for x in range(w) if rows[y][x] == 2]
    nwall = sum(1 for y in range(h) for x in range(w) if rows[y][x] == 1)
    choke = 0
    for t in ok:
        nb = sum(1 for dx, dy in CARD if (t[0] + dx, t[1] + dy) in ok)
        if nb <= 2:
            choke += 1

    def apron(anch):
        cx, cy = anch
        ct = footprint(anch)
        n = 0
        for t in ok:
            if t in ct:
                continue
            if min((t[0] - a) ** 2 + (t[1] - b) ** 2 for a, b in ct) <= 8:
                n += 1
        return n

    # ore siting, from team A's side (maps are symmetric, so B mirrors)
    oa = sorted(da[t] for t in ore if t in da)
    ob = sorted(db[t] for t in ore if t in db)
    mine_a = sum(1 for t in ore if t in da and t in db and da[t] < db[t])
    return {
        "map": mapname, "w": w, "h": h,
        "coredsq": min((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
                       for a in fa for b in fb),
        "bfs": bfs,
        "mincut": min_vertex_cut(ok, fa, fb),
        "narrow": narrowest_level(ok, da, db, bfs),
        "wallpct": round(100.0 * nwall / (w * h), 1),
        "choke_pct": round(100.0 * choke / max(1, len(ok)), 1),
        "apron_a": apron(anchors[0]), "apron_b": apron(anchors[1]),
        "ore_n": len(ore),
        "ore_mine": mine_a,
        "ore_d1": oa[0] if oa else -1,
        "ore_d4": oa[3] if len(oa) > 3 else -1,
        "ore_d1_b": ob[0] if ob else -1,
        "ore_d4_b": ob[3] if len(ob) > 3 else -1,
        "reach": len(da),
        "passable": len(ok),
    }


COLS = ["map", "w", "h", "coredsq", "bfs", "mincut", "narrow", "wallpct",
        "choke_pct", "apron_a", "apron_b", "ore_n", "ore_mine", "ore_d1",
        "ore_d4", "ore_d1_b", "ore_d4_b", "reach", "passable"]


def selftest():
    """BOTH VERDICTS on every derived quantity."""
    ok_all = True

    def chk(name, got, want, why):
        nonlocal ok_all
        good = got == want
        ok_all &= good
        print(f"  [{'PASS' if good else 'FAIL'}] {name}: {got!r} (want {want!r}) {why}")

    print("CONTROL 1 -- min_vertex_cut on hand-built fixtures")
    # a 1-wide corridor must read 1; a 3-wide slab must read 3
    corr = {(x, 0) for x in range(6)}
    chk("1-wide corridor", min_vertex_cut(corr, [(0, 0)], [(5, 0)]), 1, "single file")
    slab = {(x, y) for x in range(6) for y in range(3)}
    chk("3-wide slab", min_vertex_cut(slab, [(0, y) for y in range(3)],
                                      [(5, y) for y in range(3)]), 3, "3 disjoint rows")
    # two parallel 1-wide corridors joined only at the ends: the mid rung
    # tiles (0,1)/(5,1) are terminals but have no route of their own, so the
    # answer is 2, not 3 -- the fixture author guessed 3 and the tool was right.
    split = corr | {(x, 2) for x in range(6)} | {(0, 1), (5, 1)}
    chk("two 1-wide corridors", min_vertex_cut(split, [(0, 0), (0, 1), (0, 2)],
                                               [(5, 0), (5, 1), (5, 2)]), 2,
        "2 disjoint routes")
    # ... and welding a third full row makes it 3, which is the other verdict
    split3 = split | {(x, 1) for x in range(6)}
    chk("three 1-wide corridors", min_vertex_cut(split3, [(0, y) for y in range(3)],
                                                 [(5, y) for y in range(3)]), 3,
        "3 disjoint routes")
    wall = {(x, 0) for x in range(3)} | {(x, 2) for x in range(3)}
    chk("disconnected", min_vertex_cut(wall, [(0, 0)], [(0, 2)]), 0, "no route")

    print("CONTROL 2 -- narrowest_level")
    okc = corr
    da, db = bfs_from([(0, 0)], okc), bfs_from([(5, 0)], okc)
    chk("corridor narrow", narrowest_level(okc, da, db, 5), 1, "")
    da2, db2 = bfs_from([(0, y) for y in range(3)], slab), bfs_from(
        [(5, y) for y in range(3)], slab)
    chk("slab narrow", narrowest_level(slab, da2, db2, 5), 3, "")

    print("CONTROL 3 -- real maps must DISAGREE with each other")
    g = {m: geom(m) for m in ("royale", "yulerune", "ragnarok", "icefloe")}
    for k in ("mincut", "narrow", "choke_pct", "ore_d4", "wallpct"):
        vals = {m: g[m][k] for m in g}
        distinct = len(set(vals.values()))
        good = distinct > 1
        ok_all &= good
        print(f"  [{'PASS' if good else 'FAIL'}] {k} varies across maps: {vals}")

    print("CONTROL 4 -- symmetry: A and B sides must match (maps are symmetric)")
    for m in POOL:
        gg = geom(m)
        good = (gg["apron_a"] == gg["apron_b"] and gg["ore_d1"] == gg["ore_d1_b"]
                and gg["ore_d4"] == gg["ore_d4_b"] and
                gg["ore_mine"] * 2 <= gg["ore_n"] + 2)
        ok_all &= good
        if not good:
            print(f"  [FAIL] {m}: {gg}")
    print(f"  [{'PASS' if ok_all else 'FAIL'}] all 15 maps side-symmetric")
    print("SELFTEST", "PASS" if ok_all else "FAIL")
    return 0 if ok_all else 1


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return 0
    if a[0] == "--selftest":
        return selftest()
    if a[0] == "--table":
        print("\t".join(COLS))
        for m in POOL:
            g = geom(m)
            print("\t".join(str(g[c]) for c in COLS))
        return 0
    for m in a:
        g = geom(m)
        for k in COLS:
            print(f"{k:12s} {g[k]}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
