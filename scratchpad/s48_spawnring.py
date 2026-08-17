#!/usr/bin/env python3
"""s48: how much walk does the SPAWN TILE cost us?

The core picks a spawn tile out of the ~24 tiles of ring(core,2) by a hash
sort that has no geometry term.  This prints, per replay:
  best_d  = min over the legal ring of (steps from that tile to a tile
            orthogonally adjacent to an ore tile)
  got_d   = the same quantity for each tile we actually spawned on, in order
so the difference is the walk the spawn placement itself bought.

Usage: python3 scratchpad/s48_spawnring.py <replay> --team 0 [--label X]
"""
from __future__ import annotations

import argparse
import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tools.replay_census import Replay, fields, parse_entity, WIRE_LEN  # noqa: E402

CARD = ((0, -1), (1, 0), (0, 1), (-1, 0))


def spawns_of(path, team, rounds=12):
    data = path.read_bytes()
    turns = [v for n, w, v in fields(data) if n == 3 and w == WIRE_LEN]
    out = []
    for r, tb in enumerate(turns[: rounds + 1]):
        for num, wire, value in fields(tb):
            if num != 1 or wire != WIRE_LEN:
                continue
            for n2, w2, v2 in fields(value):
                if n2 != 1 or w2 != WIRE_LEN:
                    continue
                for n3, w3, v3 in fields(v2):
                    if n3 == 1 and w3 == WIRE_LEN:
                        e = parse_entity(v3, r)
                        if e and e.team == team and e.kind == "builder_bot":
                            out.append((r, e.pos))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("replay")
    ap.add_argument("--team", type=int, default=0)
    ap.add_argument("--label", default="")
    a = ap.parse_args()

    rep = Replay(Path(a.replay), track_flow=False)
    core = next(c["pos"] for c in rep.cores if c["team"] == a.team)
    ores = {(x, y) for y, row in enumerate(rep.tiles)
            for x, t in enumerate(row) if t == 2}
    goals = set()
    for ox, oy in ores:
        for dx, dy in CARD:
            g = (ox + dx, oy + dy)
            if 0 <= g[0] < rep.width and 0 <= g[1] < rep.height \
                    and rep.tiles[g[1]][g[0]] != 1:
                goals.add(g)
    dist, q = {}, deque()
    for g in goals:
        dist[g] = 0
        q.append(g)
    while q:
        x, y = q.popleft()
        for dx, dy in CARD:
            n = (x + dx, y + dy)
            if n in dist or not (0 <= n[0] < rep.width and 0 <= n[1] < rep.height):
                continue
            if rep.tiles[n[1]][n[0]] == 1:
                continue
            dist[n] = dist[(x, y)] + 1
            q.append(n)

    foot = {(core[0], core[1]), (core[0] + 1, core[1]),
            (core[0], core[1] + 1), (core[0] + 1, core[1] + 1)}
    ring = []
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            t = (core[0] + dx, core[1] + dy)
            if t in foot or not (0 <= t[0] < rep.width and 0 <= t[1] < rep.height):
                continue
            if rep.tiles[t[1]][t[0]] == 1:
                continue
            ring.append(t)
    ringd = sorted(dist.get(t, 999) for t in ring)
    got = spawns_of(Path(a.replay), a.team)
    print("\t".join(str(x) for x in (
        a.label, len(ring), ringd[:5],
        [(r, dist.get(p, 999)) for r, p in got[:5]],
        sum(dist.get(p, 999) for _, p in got[:5]) - sum(ringd[:5]))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
