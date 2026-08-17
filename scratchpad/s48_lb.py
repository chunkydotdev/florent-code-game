#!/usr/bin/env python3
"""s48: how much of our first-harvester round is UNAVOIDABLE walk time?

For every builder we spawned in the opening, computes
    beeline = spawn_round + 1 + min cardinal steps from its spawn tile to a
              tile orthogonally adjacent to ANY ore tile
i.e. the earliest round that bot could have placed a harvester if it walked
straight there and built the moment it arrived.  Prints:

  OPT_all   = min beeline over ALL opening builders          (no seat reserved)
  OPT_noS0  = min beeline over builders EXCEPT the first one (seat 0 raids)
  actual h1 = the round our first harvester actually landed

The gap actual-OPT_noS0 is the part of the delay that is NOT walk time and NOT
the raider reservation.

Usage: python3 scratchpad/s48_lb.py <replay> --team 0 [--label X]
"""
from __future__ import annotations

import argparse
import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tools.replay_census import Replay, fields, read_pos, parse_entity, WIRE_LEN  # noqa: E402

CARD = ((0, -1), (1, 0), (0, 1), (-1, 0))


def tape(path: Path, rounds: int):
    data = path.read_bytes()
    turns = [v for n, w, v in fields(data) if n == 3 and w == WIRE_LEN]
    ent, ev = {}, []
    for r, tb in enumerate(turns[: rounds + 1]):
        for num, wire, value in fields(tb):
            if num != 1 or wire != WIRE_LEN:
                continue
            for n2, w2, v2 in fields(value):
                if n2 == 1 and w2 == WIRE_LEN:
                    for n3, w3, v3 in fields(v2):
                        if n3 == 1 and w3 == WIRE_LEN:
                            e = parse_entity(v3, r)
                            if e is None:
                                continue
                            ent[e.id] = [e.team, e.kind, e.pos, r]
                            ev.append((r, e.team, "SPAWN" if e.kind == "builder_bot"
                                       else "BUILD", e.id, e.kind, e.pos))
                elif n2 == 2 and w2 == WIRE_LEN:
                    mid = to = None
                    for n3, w3, v3 in fields(v2):
                        if n3 == 1:
                            mid = v3
                        elif n3 == 2 and w3 == WIRE_LEN:
                            to = read_pos(v3)
                    if mid in ent:
                        ev.append((r, ent[mid][0], "MOVE", mid, "builder_bot", to))
    return ent, ev


def multi_bfs(rep, goals):
    """Distance field: min cardinal steps from every tile to the nearest goal."""
    INF = 10 ** 6
    dist = {}
    q = deque()
    for g in goals:
        dist[g] = 0
        q.append(g)
    while q:
        x, y = q.popleft()
        d = dist[(x, y)]
        for dx, dy in CARD:
            n = (x + dx, y + dy)
            if n in dist or not (0 <= n[0] < rep.width and 0 <= n[1] < rep.height):
                continue
            if rep.tiles[n[1]][n[0]] == 1:
                continue
            dist[n] = d + 1
            q.append(n)
    return dist, INF


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("replay")
    ap.add_argument("--team", type=int, default=0)
    ap.add_argument("--rounds", type=int, default=30)
    ap.add_argument("--label", default="")
    a = ap.parse_args()

    rep = Replay(Path(a.replay), track_flow=False)
    ent, ev = tape(Path(a.replay), a.rounds)
    mine = [e for e in ev if e[1] == a.team]

    ores = {(x, y) for y, row in enumerate(rep.tiles)
            for x, t in enumerate(row) if t == 2}
    # goal set = tiles from which a harvester on an ore tile can be built
    goals = set()
    for ox, oy in ores:
        for dx, dy in CARD:
            g = (ox + dx, oy + dy)
            if 0 <= g[0] < rep.width and 0 <= g[1] < rep.height \
                    and rep.tiles[g[1]][g[0]] != 1:
                goals.add(g)
    dist, INF = multi_bfs(rep, goals)

    spawns = [(r, eid, pos) for (r, t, verb, eid, kind, pos) in mine if verb == "SPAWN"]
    spawns.sort()
    beel = []
    for i, (r, eid, pos) in enumerate(spawns[:6]):
        d = dist.get(pos, INF)
        beel.append((i, r, pos, d, (r + d + 1) if d < INF else None))

    h1 = next((r for (r, t, verb, eid, kind, pos) in mine
               if verb == "BUILD" and kind == "harvester"), None)

    ok = [b[4] for b in beel if b[4] is not None]
    opt_all = min(ok) if ok else None
    ok1 = [b[4] for b in beel[1:] if b[4] is not None]
    opt_no0 = min(ok1) if ok1 else None
    print("\t".join(str(x) for x in (
        a.label, h1, opt_all, opt_no0,
        (h1 - opt_all) if (h1 is not None and opt_all is not None) else "-",
        (h1 - opt_no0) if (h1 is not None and opt_no0 is not None) else "-",
        ";".join(f"s{i}@r{r}{p}d{d}->r{e}" for i, r, p, d, e in beel))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
