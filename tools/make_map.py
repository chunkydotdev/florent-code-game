#!/usr/bin/env python3
"""Generate .map26 map files without the platform or the browser map editor.

The .map26 format is protobuf. Schema recovered from the bundled map editor
(fcode/data/visualiser/assets/map-editor-*.js, `battlecode.Map`):

    message Map {
      int32 width = 1;
      int32 height = 2;
      repeated TileRow rows = 3;         // one per row, top to bottom
      repeated CorePosition cores = 4;
      int32 symmetry = 5;                // 0=rotational 1=horizontal 2=vertical
      repeated MapEntity entities = 6;   // decor only; the engine ignores it
    }
    message TileRow     { repeated Environment tiles = 1; }
    message Pos         { int32 x = 1; int32 y = 2; }
    message CorePosition{ int32 id = 1; Team team = 2; Pos position = 3; }
    enum Team        { TEAM_A = 0; TEAM_B = 1; }
    enum Environment { ENV_EMPTY = 0; ENV_WALL = 1; ENV_ORE_TITANIUM = 2; }

Editor constraints worth respecting: dimensions 8..30, both cores present,
core footprints are 2x2 with a 1-tile clear margin (no wall/ore against them),
and the two footprints must be more than 2 tiles apart on both axes.

Usage:
    python3 tools/make_map.py                      # writes the default set into maps/
    python3 tools/make_map.py --out maps
"""

from __future__ import annotations

import argparse
import random
from pathlib import Path

# ---- `--help` CONTRACT (enforced by tests/test_instruments.py) --------------
# Side-effect-free, prints this module's docstring, exits 0.
#
# ⛔ WHY. Probing an unknown tool with `--help` is the first thing anyone does.
# Before 2026-08-15, 40 of 86 tools here had no argparse, so `--help` was just an
# unrecognised argument and THE TOOL RAN FOR REAL -- printing VERDICT-SHAPED text
# that reads as a finding:
#     tools/freshness.py --help  ->  "BLIND: --help has no parseable timestamp"
#     tools/leg_read.py  --help  ->  "LEG: no completed games"
# Both are this repo's own verdict vocabulary. A reader asking a harmless
# question got an authoritative-looking sentence about nothing.
#
# ⛔ GATED ON `__main__`: several of these modules are IMPORTED by other tools
# (freshness by now.py). Ungated, this would fire during that import and make the
# PARENT exit 0 mid-run while printing the CHILD's docstring.
# ⛔ SELF-CONTAINED `import sys`: a first attempt used the file's own import, and
# broke on `import sys as _sys` (NameError) and on files whose imports come in
# two blocks. The guard must not depend on what the host file happens to import.
if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__ + "  (no module docstring)"))
        raise SystemExit(0)

EMPTY, WALL, ORE = 0, 1, 2
ROTATIONAL, HORIZONTAL, VERTICAL = 0, 1, 2

MIN_DIM, MAX_DIM = 8, 30


# --- minimal protobuf writer -------------------------------------------------

def _varint(n: int) -> bytes:
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        out.append(b | (0x80 if n else 0))
        if not n:
            return bytes(out)


def _tag(field: int, wire: int) -> bytes:
    return _varint((field << 3) | wire)


def _vfield(field: int, value: int) -> bytes:
    return _tag(field, 0) + _varint(value)


def _lfield(field: int, payload: bytes) -> bytes:
    return _tag(field, 2) + _varint(len(payload)) + payload


def _packed(field: int, values) -> bytes:
    body = b"".join(_varint(v) for v in values)
    return _tag(field, 2) + _varint(len(body)) + body


def encode_map(grid, core_a, core_b, symmetry=ROTATIONAL) -> bytes:
    """grid is a list of rows (list[int]); core positions are the footprint's top-left."""
    height = len(grid)
    width = len(grid[0])
    out = bytearray()
    out += _vfield(1, width)
    out += _vfield(2, height)
    for row in grid:
        out += _lfield(3, _packed(1, row))
    for cid, team, (cx, cy) in ((1, 0, core_a), (2, 1, core_b)):
        pos = _vfield(1, cx) + _vfield(2, cy)
        out += _lfield(4, _vfield(1, cid) + _vfield(2, team) + _lfield(3, pos))
    out += _vfield(5, symmetry)
    return bytes(out)


# --- map construction --------------------------------------------------------

def _mirror(x, y, width, height, symmetry):
    if symmetry == ROTATIONAL:
        return width - 1 - x, height - 1 - y
    if symmetry == HORIZONTAL:
        return width - 1 - x, y
    return x, height - 1 - y


def _core_zone(core, pad=1):
    """Footprint tiles plus the required clear margin."""
    cx, cy = core
    return {
        (cx + dx, cy + dy)
        for dx in range(-pad, 2 + pad)
        for dy in range(-pad, 2 + pad)
    }


def build(width, height, core_a, symmetry=ROTATIONAL, ore=14, wall_pct=0.10, seed=0):
    """Build a symmetric map. Everything placed in one half is mirrored into the other."""
    if not (MIN_DIM <= width <= MAX_DIM and MIN_DIM <= height <= MAX_DIM):
        raise ValueError(f"dimensions must be {MIN_DIM}..{MAX_DIM}, got {width}x{height}")

    rng = random.Random(seed)
    core_b = _mirror(core_a[0] + 1, core_a[1] + 1, width, height, symmetry)
    core_b = (min(core_b[0], width - 2), min(core_b[1], height - 2))

    if abs(core_a[0] - core_b[0]) <= 2 and abs(core_a[1] - core_b[1]) <= 2:
        raise ValueError("core footprints too close — need >2 tiles of separation on an axis")

    grid = [[EMPTY] * width for _ in range(height)]
    reserved = _core_zone(core_a) | _core_zone(core_b)

    def place(x, y, kind):
        mx, my = _mirror(x, y, width, height, symmetry)
        for px, py in ((x, y), (mx, my)):
            if not (0 <= px < width and 0 <= py < height):
                return False
            if (px, py) in reserved:
                return False
        for px, py in ((x, y), (mx, my)):
            grid[py][px] = kind
            reserved.add((px, py))
        return True

    # Ore in clusters, so harvesters have somewhere worth defending.
    placed = 0
    guard = 0
    while placed < ore and guard < ore * 200:
        guard += 1
        sx, sy = rng.randrange(width), rng.randrange(height)
        for _ in range(rng.randint(2, 4)):
            if placed >= ore:
                break
            if place(sx, sy, ORE):
                placed += 1
            sx = max(0, min(width - 1, sx + rng.choice((-1, 0, 1))))
            sy = max(0, min(height - 1, sy + rng.choice((-1, 0, 1))))

    # Short wall segments, never sealing a region off completely.
    for _ in range(int(width * height * wall_pct / 3)):
        x, y = rng.randrange(width), rng.randrange(height)
        dx, dy = rng.choice(((1, 0), (0, 1)))
        for i in range(rng.randint(2, 4)):
            place(x + dx * i, y + dy * i, WALL)

    return grid, core_a, core_b


DEFAULT_MAPS = [
    # name,          w,  h, core_a, ore, wall%, seed  — spans the 8..30 range the pool uses
    ("tiny8",         8,  8, (1, 1),   4, 0.06, 11),
    ("small12",      12, 12, (1, 1),   8, 0.08, 22),
    ("duel16",       16, 16, (2, 2),  12, 0.10, 33),
    ("mid20",        20, 20, (2, 2),  16, 0.10, 44),
    ("wide30x14",    30, 14, (2, 6),  18, 0.09, 55),
    ("large30",      30, 30, (3, 3),  28, 0.12, 66),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="maps", help="output directory (default: maps)")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    for name, w, h, core_a, ore, wall_pct, seed in DEFAULT_MAPS:
        grid, ca, cb = build(w, h, core_a, ROTATIONAL, ore, wall_pct, seed)
        dest = out / f"{name}.map26"
        dest.write_bytes(encode_map(grid, ca, cb, ROTATIONAL))
        counts = {k: sum(r.count(k) for r in grid) for k in (WALL, ORE)}
        print(f"  {dest}  {w}x{h}  cores {ca} {cb}  ore={counts[ORE]} wall={counts[WALL]}")


if __name__ == "__main__":
    main()
