#!/usr/bin/env python3
"""Render OUR eco footprint at a chosen round: map terrain + our buildings.

Usage: render.py <replay26> <map> <seat A|B> <round>
Legend: # wall  o ore  C core(ours)  X core(theirs)
        ^>v<  our conveyor by output direction   S splitter   H harvester
        B barrier  G gunner  N sentinel  L launcher  b our body
        lowercase red equivalents for THEIR buildings: h c s b g n l
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "scratchpad" / "s51_route"))
from replay_census import (fields, parse_entity, read_pos,  # noqa: E402
                           DIRECTION_DELTA)
from mapgeom import load, footprint  # noqa: E402

ARROW = {1: "^", 3: ">", 5: "v", 7: "<", 2: "/", 4: "\\", 6: "/", 8: "\\",
         0: "*", None: "?"}
OURS = {"harvester": "H", "splitter": "S", "barrier": "B", "gunner": "G",
        "sentinel": "N", "launcher": "L", "builder_bot": "b", "core": "C"}
THEIRS = {"harvester": "h", "splitter": "s", "barrier": "x", "gunner": "g",
          "sentinel": "n", "launcher": "l", "builder_bot": "p", "core": "X",
          "conveyor": "c"}


def main():
    rp, mapname, seat, upto = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
    w, h, rows, anchors = load(mapname)
    ourteam = 0 if seat == "A" else 1
    data = Path(rp).read_bytes()
    map_buf, turns = None, []
    for num, wire, val in fields(data):
        if num == 1 and wire == 2:
            map_buf = val
        elif num == 3 and wire == 2:
            turns.append(val)
    ents = {}
    for rnd, tb in enumerate(turns[:upto + 1]):
        for _n, _w2, ubuf in fields(tb):
            for unum, _uw, ub in fields(ubuf):
                if unum == 1:
                    for en, _ew, eb in fields(ub):
                        if en != 1:
                            continue
                        e = parse_entity(eb, rnd)
                        if e:
                            ents[e.id] = [e.kind, e.team, e.pos, e.direction]
                elif unum == 2:
                    eid = to = None
                    for a, _b, c in fields(ub):
                        if a == 1:
                            eid = c
                        elif a == 2:
                            to = read_pos(c)
                    if eid in ents and to:
                        ents[eid][2] = to
                elif unum == 3:
                    for a, _b, c in fields(ub):
                        if a == 1:
                            ents.pop(c, None)
    grid = [["#" if rows[y][x] == 1 else ("o" if rows[y][x] == 2 else ".")
             for x in range(w)] for y in range(h)]
    for t in (0, 1):
        for tt in footprint(anchors[t]):
            grid[tt[1]][tt[0]] = "C" if t == ourteam else "X"
    for _eid, (kind, team, pos, d) in ents.items():
        if kind == "core" or not (0 <= pos[0] < w and 0 <= pos[1] < h):
            continue
        if team == ourteam:
            ch = ARROW.get(d, "?") if kind == "conveyor" else OURS.get(kind, "?")
        else:
            ch = THEIRS.get(kind, "?")
        grid[pos[1]][pos[0]] = ch
    print(f"# {Path(rp).name} map={mapname} seat={seat} round={upto}")
    print("    " + "".join(str(x % 10) for x in range(w)))
    for y in range(h):
        print(f"{y:3d} " + "".join(grid[y]))


if __name__ == "__main__":
    main()
