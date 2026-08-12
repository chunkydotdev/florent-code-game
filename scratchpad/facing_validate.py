#!/usr/bin/env python3
"""VALIDATE that the decoded Direction field on the replay wire is really facing.

Independent signal: a Conveyor outputs to exactly ONE tile -- the one its facing
points at.  So every `distributeResources` move whose `from` is a conveyor tile
must have `to == from + delta(facing)`.  Nothing about that check uses the
decoded field except the prediction, so agreement is real evidence.

Three verdicts printed:
  RAW   : decoded facing, as-is.
  ROT+1 : every decoded facing rotated ONE compass step (45 deg).  This MUST
          collapse.  A check that cannot fail has not been seen to check.
  ROT+2 : rotated 90 deg.  Must also collapse.

Also prints the direction histogram for conveyor / splitter / gunner / sentinel
so a constant column is visible immediately.
"""
from __future__ import annotations
import sys, random
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa

# CLAUDE.md compass: (0,0) is the map NORTHWEST corner, x grows EAST,
# y grows SOUTH.  Therefore NORTH = (0,-1).  Wire enum from replay_schema.md.
DELTA = {0: (0, 0), 1: (0, -1), 2: (1, -1), 3: (1, 0), 4: (1, 1),
         5: (0, 1), 6: (-1, 1), 7: (-1, 0), 8: (-1, -1)}
NAME = {0: "CENTRE", 1: "N", 2: "NE", 3: "E", 4: "SE",
        5: "S", 6: "SW", 7: "W", 8: "NW"}
# one compass step clockwise on the 1..8 ring (N->NE->E->SE->S->SW->W->NW->N)
RING = [1, 2, 3, 4, 5, 6, 7, 8]


def rot(d: int, steps: int) -> int:
    if d == 0:
        return 0
    return RING[(RING.index(d) + steps) % 8]


def walk(path: Path, hist: Counter, tally: dict):
    data = path.read_bytes()
    turn_bufs = []
    for num, wire, value in fields(data):
        if num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)

    tile = {}          # (x,y) -> (kind, direction)
    ent_pos = {}       # id -> (x,y)
    seen_ids = set()

    for rnd, tb in enumerate(turn_bufs):
        for _n, _w, ub in fields(tb):
            for un, _uw, uv in fields(ub):
                if un == 1:                       # placeEntity
                    for en, _ew, ev in fields(uv):
                        if en != 1:
                            continue
                        e = parse_entity(ev, rnd)
                        if e is None:
                            continue
                        if e.direction is not None and e.id not in seen_ids:
                            hist[e.kind][e.direction] += 1
                        seen_ids.add(e.id)
                        ent_pos[e.id] = tuple(e.pos)
                        tile[tuple(e.pos)] = (e.kind, e.direction)
                elif un == 3:                     # removeEntity
                    eid = None
                    for rn, _rw, rv in fields(uv):
                        if rn == 1:
                            eid = rv
                    p = ent_pos.pop(eid, None)
                    if p is not None:
                        tile.pop(p, None)
                elif un == 2:                     # moveBuilderBot
                    eid, to = None, None
                    for mn, mw, mv in fields(uv):
                        if mn == 1:
                            eid = mv
                        elif mn == 2 and mw == WIRE_LEN:
                            to = read_pos(mv)
                    if eid in ent_pos:
                        old = ent_pos[eid]
                        if tile.get(old, (None,))[0] == "builder_bot":
                            tile.pop(old, None)
                        ent_pos[eid] = tuple(to)
                elif un == 4:                     # distributeResources
                    for mn, mw, mv in fields(uv):
                        if mn != 1 or mw != WIRE_LEN:
                            continue
                        frm = to = None
                        for fn, fw, fv in fields(mv):
                            if fn == 1 and fw == WIRE_LEN:
                                frm = read_pos(fv)
                            elif fn == 2 and fw == WIRE_LEN:
                                to = read_pos(fv)
                        if frm is None or to is None:
                            continue
                        cell = tile.get(tuple(frm))
                        if cell is None or cell[0] != "conveyor":
                            continue
                        d = cell[1] or 0
                        for label, steps in (("RAW", 0), ("ROT+1", 1), ("ROT+2", 2)):
                            dx, dy = DELTA[rot(d, steps)]
                            pred = (frm[0] + dx, frm[1] + dy)
                            tally[label][pred == tuple(to)] += 1


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    n = 150
    for a in sys.argv[1:]:
        if a.startswith("--n="):
            n = int(a.split("=")[1])
    paths = sorted((ROOT / "replay_archive").glob("*.replay26"))
    random.seed(20260810)
    paths = random.sample(paths, min(n, len(paths)))

    hist = {k: Counter() for k in ("conveyor", "splitter", "gunner", "sentinel")}
    tally = {k: Counter() for k in ("RAW", "ROT+1", "ROT+2")}
    for p in paths:
        try:
            walk(p, hist, tally)
        except Exception as exc:
            print(f"ERR {p.name}: {type(exc).__name__}: {exc}", file=sys.stderr)

    print(f"# {len(paths)} replays sampled from replay_archive/\n")
    print("DIRECTION HISTOGRAM (first placeEntity per entity id)")
    print("kind\t" + "\t".join(NAME[d] for d in range(9)) + "\ttotal")
    for k, c in hist.items():
        tot = sum(c.values())
        print(k + "\t" + "\t".join(str(c.get(d, 0)) for d in range(9)) + f"\t{tot}")

    print("\nCONVEYOR OUTPUT CROSS-CHECK  (to == from + delta(facing))")
    print("variant\tagree\tdisagree\tshare")
    for k in ("RAW", "ROT+1", "ROT+2"):
        a, b = tally[k][True], tally[k][False]
        tot = a + b
        print(f"{k}\t{a}\t{b}\t{a / tot:.4f}" if tot else f"{k}\t0\t0\tn/a")


if __name__ == "__main__":
    main()
