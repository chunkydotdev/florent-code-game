#!/usr/bin/env python3
"""s48 opening decoder: per-round builder spawns, moves and builds, rounds 0-N.

Reads a local .replay26 and prints, for ONE team, the exact opening tape:
  R<r>  SPAWN bot#<id> @(x,y) | MOVE bot#<id> ->(x,y) | BUILD <kind> @(x,y)
plus a summary line: first harvester round, first conveyor round, and the
walk distance from each bot's spawn tile to the tile it first built on.

Usage: python3 scratchpad/s48_opening.py <replay> [--team 0|1] [--rounds 12]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tools.replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa: E402


def decode(path: Path, rounds: int):
    data = path.read_bytes()
    turn_bufs = []
    cores = {}
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            for n2, w2, v2 in fields(value):
                if n2 == 4 and w2 == WIRE_LEN:
                    sub = {}
                    for n3, w3, v3 in fields(v2):
                        sub[n3] = v3
                    cores[sub.get(2, 0)] = read_pos(sub[3]) if 3 in sub else None
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)

    ent = {}          # id -> (team, kind, spawn_pos)
    events = []       # (round, team, verb, id, kind, pos)
    for r, tb in enumerate(turn_bufs):
        if r > rounds:
            break
        for num, wire, value in fields(tb):
            if num != 1 or wire != WIRE_LEN:
                continue
            for n2, w2, v2 in fields(value):
                if n2 == 1 and w2 == WIRE_LEN:          # placeEntity
                    for n3, w3, v3 in fields(v2):
                        if n3 == 1 and w3 == WIRE_LEN:
                            e = parse_entity(v3, r)
                            if e is None:
                                continue
                            ent[e.id] = (e.team, e.kind, e.pos)
                            verb = "SPAWN" if e.kind == "builder_bot" else "BUILD"
                            events.append((r, e.team, verb, e.id, e.kind, e.pos))
                elif n2 == 2 and w2 == WIRE_LEN:        # moveBuilderBot
                    mid, to = None, None
                    for n3, w3, v3 in fields(v2):
                        if n3 == 1:
                            mid = v3
                        elif n3 == 2 and w3 == WIRE_LEN:
                            to = read_pos(v3)
                    if mid in ent:
                        t = ent[mid][0]
                        events.append((r, t, "MOVE", mid, "builder_bot", to))
    return cores, ent, events


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("replay")
    ap.add_argument("--team", type=int, default=0)
    ap.add_argument("--rounds", type=int, default=12)
    ap.add_argument("--quiet", action="store_true", help="summary line only")
    a = ap.parse_args()

    cores, ent, events = decode(Path(a.replay), a.rounds)
    core = cores.get(a.team)
    mine = [e for e in events if e[1] == a.team]

    first = {}
    builder_first_build = {}
    lastpos = {}
    for (r, t, verb, eid, kind, pos) in mine:
        if verb == "SPAWN":
            lastpos[eid] = pos
        elif verb == "MOVE":
            lastpos[eid] = pos
        if verb == "BUILD" and kind not in first:
            first[kind] = r
        if not a.quiet:
            cd = "" if core is None or pos is None else \
                f"  d_core={abs(pos[0]-core[0])+abs(pos[1]-core[1])}"
            print(f"R{r:<3} {verb:<5} #{eid:<4} {kind:<12} @{pos}{cd}")

    h = first.get("harvester")
    c = first.get("conveyor")
    print(f"SUMMARY team={a.team} map_core={core} "
          f"first_harvester={h} first_conveyor={c} "
          f"builders_by_r8={sum(1 for e in mine if e[2]=='SPAWN' and e[0]<=8)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
