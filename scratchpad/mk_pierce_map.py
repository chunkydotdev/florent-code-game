#!/usr/bin/env python3
"""Generate the STEP-0 pierce probe map: two cores on the SAME ROW, wide open.

Geometry (16x16, rotational symmetry, y=7 is the shared row):
    A core footprint  (3,7)(4,7)(3,8)(4,8)
    B core footprint  (10,7)(11,7)(10,8)(11,8)
    seat tile for our sentinel: (9,7)  -- orthogonally WEST of B's core
    B's core-mouth belt tile   (12,7)  -- orthogonally EAST of B's core
    far tile                   (13,7)

    A sentinel on (9,7) facing EAST has the B core ON its ray at (10,7),(11,7)
    and the belt tile BEHIND it at (12,7), d^2 = 9 (range r^2 = 32).

Ore is placed off the firing row so nothing but the cores sits on y=7.

Usage: .venv/bin/python scratchpad/mk_pierce_map.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from make_map import encode_map, ROTATIONAL  # noqa: E402

EMPTY, WALL, ORE = 0, 1, 2

W = H = 16
CORE_A = (3, 7)
CORE_B = (10, 7)


def main() -> int:
    grid = [[EMPTY] * W for _ in range(H)]
    # Ore well away from row 7/8 and from both core margins, mirrored.
    for (x, y) in ((5, 3), (6, 3), (5, 12), (6, 12), (9, 3), (10, 12)):
        grid[y][x] = ORE
    out = ROOT / "maps" / "invented" / "pierce16.map26"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(encode_map(grid, CORE_A, CORE_B, ROTATIONAL))
    print(f"wrote {out}  {W}x{H}  cores {CORE_A} {CORE_B}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
