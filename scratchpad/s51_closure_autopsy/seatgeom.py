#!/usr/bin/env python3
"""s51 closure autopsy -- STATIC seat geometry per map, from maps/*.map26.

Reproduces the bot's OWN seat definition (`_fs_ring12` -> eco.heal_seats +
eco.core_corners, minus wall tiles, minus off-map tiles) for the ENEMY core of
each seat (A = we are team 0, B = we are team 1).

Emits one row per (map, our_seat, ring tile):
    map seat side tile_x tile_y kind env class
  side  = 'orth' (heal seat) | 'diag' (core corner)
  env   = EMPTY | WALL | ORE
  class = barrier-legal | wall-excluded | offmap-excluded | ore

⛔ STATIC ONLY.  Enemy buildings / bodies on a seat are DYNAMIC and are read
from the replay tape (seattape.py), never from here.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from map_encode import parse_map26  # noqa: E402

MAPS = ["atoll", "midgard", "drakkarfjord", "glacierkeep", "nordkap"]
ENVNAME = {0: "EMPTY", 1: "WALL", 2: "ORE"}


def heal_seats(ox, oy, mw, mh):
    seats = ((ox, oy - 1), (ox + 1, oy - 1), (ox + 2, oy), (ox + 2, oy + 1),
             (ox + 1, oy + 2), (ox, oy + 2), (ox - 1, oy + 1), (ox - 1, oy))
    return seats, [s for s in seats if 0 <= s[0] < mw and 0 <= s[1] < mh]


def core_corners(ox, oy, mw, mh):
    cs = ((ox - 1, oy - 1), (ox + 2, oy - 1), (ox - 1, oy + 2), (ox + 2, oy + 2))
    return cs, [c for c in cs if 0 <= c[0] < mw and 0 <= c[1] < mh]


def map_info(name):
    w, h, rows, cores = parse_map26(ROOT / "maps" / f"{name}.map26")
    a = next(c for c in cores if c[0] == 0)
    b = next(c for c in cores if c[0] == 1)
    return w, h, rows, (a[1], a[2]), (b[1], b[2])


def rows_for(name):
    w, h, rows, A, B = map_info(name)
    out = []
    for seat, (ours, enemy) in (("A", (A, B)), ("B", (B, A))):
        ox, oy = enemy
        allseats, inb = heal_seats(ox, oy, w, h)
        allcorn, inbc = core_corners(ox, oy, w, h)
        for side, alltiles, inbounds in (("orth", allseats, set(inb)),
                                         ("diag", allcorn, set(inbc))):
            for t in alltiles:
                if t not in inbounds:
                    env, cls = "OFFMAP", "offmap-excluded"
                else:
                    e = rows[t[1]][t[0]]
                    env = ENVNAME.get(e, f"?{e}")
                    cls = {0: "barrier-legal", 1: "wall-excluded",
                           2: "ore"}.get(e, "?")
                out.append(dict(map=name, seat=seat, side=side,
                                x=t[0], y=t[1], env=env, cls=cls,
                                enemy_core=f"{ox},{oy}",
                                our_core=f"{ours[0]},{ours[1]}"))
    return out


def main():
    cols = ["map", "seat", "side", "x", "y", "env", "cls", "enemy_core",
            "our_core"]
    print("\t".join(cols))
    for m in MAPS:
        for r in rows_for(m):
            print("\t".join(str(r[c]) for c in cols))


if __name__ == "__main__":
    if "-h" in sys.argv[1:] or "--help" in sys.argv[1:]:
        print(__doc__)
        raise SystemExit(0)
    main()
