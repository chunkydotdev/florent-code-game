#!/usr/bin/env python3
"""s48: opening tape -> one row per (map, seat).

For each replay: first-harvester round, the SEAT that built it (spawn order),
that seat's spawn round and spawn tile, the nearest ore to our core, and the
walk-bound lower bound (spawn_round + 1 + steps_to_a_tile_adjacent_to_nearest_ore).

Usage: python3 scratchpad/s48_open_table.py <replay> --team 0 [--label X]
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


def bfs_steps(rep, start, goals):
    """Min cardinal steps from start to any goal over non-wall tiles."""
    if start in goals:
        return 0
    seen = {start}
    q = deque([(start, 0)])
    while q:
        (x, y), d = q.popleft()
        for dx, dy in CARD:
            n = (x + dx, y + dy)
            if n in seen or not (0 <= n[0] < rep.width and 0 <= n[1] < rep.height):
                continue
            if rep.tiles[n[1]][n[0]] == 1:      # WALL
                continue
            if n in goals:
                return d + 1
            seen.add(n)
            q.append((n, d + 1))
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("replay")
    ap.add_argument("--team", type=int, default=0)
    ap.add_argument("--rounds", type=int, default=30)
    ap.add_argument("--label", default="")
    a = ap.parse_args()

    rep = Replay(Path(a.replay), track_flow=False)
    core = next(c["pos"] for c in rep.cores if c["team"] == a.team)
    ent, ev = tape(Path(a.replay), a.rounds)
    mine = [e for e in ev if e[1] == a.team]

    ores = {(x, y) for y, row in enumerate(rep.tiles)
            for x, t in enumerate(row) if t == 2}
    near = min(ores, key=lambda p: abs(p[0] - core[0]) + abs(p[1] - core[1])) if ores else None

    # spawn order -> seat
    seat = {}
    spawn_r, spawn_p = {}, {}
    for (r, t, verb, eid, kind, pos) in mine:
        if verb == "SPAWN":
            seat[eid] = len(seat)
            spawn_r[eid] = r
            spawn_p[eid] = pos

    # positions per round for attribution
    pos_now = dict(spawn_p)
    h1 = c1 = None
    h1_by = h1_pos = None
    hcount = ccount = 0
    h8 = c8 = b8 = 0
    for (r, t, verb, eid, kind, pos) in mine:
        if r <= 8:
            if verb == "BUILD" and kind == "harvester":
                h8 += 1
            elif verb == "BUILD" and kind == "conveyor":
                c8 += 1
            elif verb == "SPAWN":
                b8 += 1
        if verb == "MOVE":
            pos_now[eid] = pos
        elif verb == "SPAWN":
            pos_now[eid] = pos
        elif verb == "BUILD":
            if kind == "harvester":
                hcount += 1
                if h1 is None:
                    h1 = r
                    h1_pos = pos
                    for b, bp in pos_now.items():
                        if bp and abs(bp[0] - pos[0]) + abs(bp[1] - pos[1]) == 1:
                            h1_by = seat.get(b)
                            break
            elif kind == "conveyor":
                ccount += 1
                if c1 is None:
                    c1 = r

    # walk lower bound from the FIRST builder's spawn tile to nearest ore
    lb = None
    if near and seat:
        first_bot = min(seat, key=lambda b: seat[b])
        goals = {(near[0] + dx, near[1] + dy) for dx, dy in CARD}
        goals = {g for g in goals if 0 <= g[0] < rep.width and 0 <= g[1] < rep.height
                 and rep.tiles[g[1]][g[0]] != 1}
        st = bfs_steps(rep, spawn_p[first_bot], goals)
        if st is not None:
            lb = spawn_r[first_bot] + st + 1

    print("\t".join(str(x) for x in (
        a.label, a.team, core, near,
        abs(near[0] - core[0]) + abs(near[1] - core[1]) if near else "-",
        h1, h1_by, h1_pos, c1, lb, hcount, ccount, h8, c8, b8)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
