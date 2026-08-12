#!/usr/bin/env python3
"""Second, TURRET-specific validation of the decoded Direction field, plus an
explicit compass-convention control.

Check A (conveyor, economy path): to == from + delta(facing).
   controls: ROT+1 (45 deg), ROT+2 (90 deg), FLIP-Y (mirror the y sign, i.e.
   assume NORTH were (0,+1) instead of (0,-1) -- this is the exact sign error
   CLAUDE.md warns about, and it must FAIL).

Check B (gunner, combat path): every FireTurret whose `from` tile holds a
   gunner must have `to` on the ray from `from` in the decoded facing.
   Same three controls.  This is the check that matters for LOKI-17, because a
   sentinel is a turret and not a conveyor.
"""
from __future__ import annotations
import sys, random
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa

DELTA = {0: (0, 0), 1: (0, -1), 2: (1, -1), 3: (1, 0), 4: (1, 1),
         5: (0, 1), 6: (-1, 1), 7: (-1, 0), 8: (-1, -1)}
RING = [1, 2, 3, 4, 5, 6, 7, 8]
# mirror across the x-axis: N<->S, NE<->SE, NW<->SW, E and W fixed
FLIPY = {0: 0, 1: 5, 2: 4, 3: 3, 4: 2, 5: 1, 6: 8, 7: 7, 8: 6}
VARIANTS = ("RAW", "ROT+1", "ROT+2", "FLIP-Y")


def variant_dir(d: int, v: str) -> int:
    if d == 0:
        return 0
    if v == "RAW":
        return d
    if v == "FLIP-Y":
        return FLIPY[d]
    return RING[(RING.index(d) + (1 if v == "ROT+1" else 2)) % 8]


def on_ray(frm, to, d, maxk=64):
    dx, dy = DELTA[d]
    if (dx, dy) == (0, 0):
        return False
    ex, ey = to[0] - frm[0], to[1] - frm[1]
    for k in range(1, maxk + 1):
        if (dx * k, dy * k) == (ex, ey):
            return True
        if abs(dx * k) > 64 or abs(dy * k) > 64:
            break
    return False


def walk(path: Path, conv: dict, gun: dict):
    data = path.read_bytes()
    turn_bufs = [v for num, wire, v in fields(data) if num == 3 and wire == WIRE_LEN]
    tile, ent_pos = {}, {}
    for rnd, tb in enumerate(turn_bufs):
        for _n, _w, ub in fields(tb):
            for un, _uw, uv in fields(ub):
                if un == 1:
                    for en, _ew, ev in fields(uv):
                        if en != 1:
                            continue
                        e = parse_entity(ev, rnd)
                        if e is None:
                            continue
                        ent_pos[e.id] = tuple(e.pos)
                        tile[tuple(e.pos)] = (e.kind, e.direction)
                elif un == 3:
                    eid = next((rv for rn, _rw, rv in fields(uv) if rn == 1), None)
                    p = ent_pos.pop(eid, None)
                    if p is not None:
                        tile.pop(p, None)
                elif un == 2:
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
                elif un == 4:
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
                        for v in VARIANTS:
                            dx, dy = DELTA[variant_dir(cell[1] or 0, v)]
                            conv[v][(frm[0] + dx, frm[1] + dy) == tuple(to)] += 1
                elif un == 12:                    # fireTurret {from=1, to=2}
                    frm = to = None
                    for fn, fw, fv in fields(uv):
                        if fn == 1 and fw == WIRE_LEN:
                            frm = read_pos(fv)
                        elif fn == 2 and fw == WIRE_LEN:
                            to = read_pos(fv)
                    if frm is None or to is None:
                        continue
                    cell = tile.get(tuple(frm))
                    if cell is None or cell[0] != "gunner":
                        continue
                    for v in VARIANTS:
                        gun[v][on_ray(tuple(frm), tuple(to),
                                      variant_dir(cell[1] or 0, v))] += 1


def main():
    n = 60
    for a in sys.argv[1:]:
        if a.startswith("--n="):
            n = int(a.split("=")[1])
    paths = sorted((ROOT / "replay_archive").glob("*.replay26"))
    random.seed(20260810)
    paths = random.sample(paths, min(n, len(paths)))
    conv = {v: Counter() for v in VARIANTS}
    gun = {v: Counter() for v in VARIANTS}
    for p in paths:
        try:
            walk(p, conv, gun)
        except Exception as exc:
            print(f"ERR {p.name}: {type(exc).__name__}: {exc}", file=sys.stderr)
    print(f"# {len(paths)} replays\n")
    for label, t in (("A conveyor delivery tile", conv), ("B gunner shot on facing ray", gun)):
        print(f"CHECK {label}")
        print("variant\tagree\tdisagree\tshare")
        for v in VARIANTS:
            a, b = t[v][True], t[v][False]
            tot = a + b
            print(f"{v}\t{a}\t{b}\t" + (f"{a/tot:.4f}" if tot else "n/a"))
        print()


if __name__ == "__main__":
    main()
