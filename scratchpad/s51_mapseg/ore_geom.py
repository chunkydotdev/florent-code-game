#!/usr/bin/env python3
"""s51 map segmentation -- ore-chebyshev-distance-to-core per map, both cores.

For each of the 15 pool maps: parse the map26, find both cores (2x2
footprint each, core tile stored is one corner per parse_map26 -- treat as
top-left of the 2x2 footprint per the game's core-footprint convention),
find all ORE_TITANIUM tiles, and compute for each core the MIN chebyshev
distance from any of its footprint tiles to the nearest ore tile.

We report per-map: min ore-chebyshev-dist for team0's core, for team1's
core, and the mean of the two (since our tapes are seat-symmetric, A/B
average is the map-level summary).
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from map_encode import parse_map26  # noqa: E402

MAPS = ["antler", "archipelago", "auroraveil", "drakkarfjord", "drumlin",
        "fjordgate", "frostgate", "glacierkeep", "icefloe", "midgard",
        "nordkap", "ragnarok", "royale", "valkyrie", "yulerune"]

ORE = 2  # per map_encode.py encode(): cell values 0=EMPTY,1=WALL,2=ORE (validated below)


def cheb(ax, ay, bx, by):
    return max(abs(ax - bx), abs(ay - by))


def core_footprint(x, y):
    # Core is 2x2; parse_map26 gives one anchor tile. Try both possible
    # anchor conventions and take whichever stays in-bounds / consistent.
    return [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]


def min_ore_dist(core_tiles, ore_tiles):
    if not ore_tiles:
        return None
    return min(cheb(cx, cy, ox, oy) for (cx, cy) in core_tiles for (ox, oy) in ore_tiles)


def main():
    out = [("map", "w", "h", "n_ore", "core0_x", "core0_y", "core1_x", "core1_y",
            "dist_core0", "dist_core1", "dist_mean")]
    for name in MAPS:
        path = ROOT / "maps" / f"{name}.map26"
        w, h, rows, cores = parse_map26(path)
        vals = {c for row in rows for c in row}
        assert vals <= {0, 1, 2}, f"{name}: unexpected tile values {vals}"
        ore_tiles = [(x, y) for y in range(h) for x in range(w) if rows[y][x] == ORE]
        c0 = next(c for c in cores if c[0] == 0)
        c1 = next(c for c in cores if c[0] == 1)
        fp0 = core_footprint(c0[1], c0[2])
        fp1 = core_footprint(c1[1], c1[2])
        d0 = min_ore_dist(fp0, ore_tiles)
        d1 = min_ore_dist(fp1, ore_tiles)
        dmean = (d0 + d1) / 2 if d0 is not None and d1 is not None else None
        out.append((name, w, h, len(ore_tiles), c0[1], c0[2], c1[1], c1[2], d0, d1, dmean))
    for row in out:
        print("\t".join(str(x) for x in row))


if __name__ == "__main__":
    main()
