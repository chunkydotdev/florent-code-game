#!/usr/bin/env python3
"""v524 CHANGE 1 verification: the 15-map cripple predicate table, both ways.

Drives `_fs_map_gated` (the real siege.py method, imported unmodified) against
every `maps/*.map26` in the 15-map pool, with a fake `ct` that senses the
WHOLE board (so `known_map_for`'s disambiguation always has full information --
the strongest test the offline harness can give the exact-match path). Runs
each map through BOTH `LOKI_FS_V524 = True` (this build, as shipped) and
`LOKI_FS_V524 = False` (the mutant -- must reproduce the parent's 4-map
collision exactly).

Usage: .venv/bin/python3 scratchpad/s51_v524_build/predicate_table.py
"""
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))
from map_encode import parse_map26  # noqa: E402
from fcode import Environment, Position  # noqa: E402

POOL = ["antler", "archipelago", "auroraveil", "drakkarfjord", "drumlin",
        "fjordgate", "frostgate", "glacierkeep", "icefloe", "midgard",
        "nordkap", "ragnarok", "royale", "valkyrie", "yulerune"]

EXPECT_EXACT = {"midgard", "yulerune"}          # v524 CHANGE 1 target
EXPECT_MUTANT = {"midgard", "yulerune", "ragnarok", "frostgate"}  # old bug


class FakeCt:
    def __init__(self, w, h, rows):
        self.w, self.h = w, h
        self.rows = rows
        self._tiles = [Position(x, y) for y in range(h) for x in range(w)]

    def get_current_round(self):
        return 0

    def get_nearby_tiles(self, dist_sq=None):
        return self._tiles

    def get_tile_env(self, pos):
        v = self.rows[pos.y][pos.x]
        return {0: Environment.EMPTY, 1: Environment.WALL,
                2: Environment.ORE_TITANIUM}[v]


def load_siege(flag_value):
    """Import a FRESH copy of the built tree's doctrine/eco/siege modules with
    LOKI_FS_V524 monkeypatched, isolated per import via sys.modules purge so
    the True and False runs never share module-level state (FS_V524_CRIPPLE_GRIDS
    is computed once at siege import time, but it does not depend on the flag,
    only `_fs_map_gated`'s runtime read of the doctrine module attribute does)."""
    for m in ("doctrine", "eco", "siege"):
        sys.modules.pop(m, None)
    bot_dir = str(ROOT / "bots" / "_v524exact")
    if bot_dir not in sys.path:
        sys.path.insert(0, bot_dir)
    import doctrine
    doctrine.LOKI_FS_V524 = flag_value
    import eco  # noqa: F401  (picks up the patched doctrine via `from doctrine import *`)
    import siege
    return siege


def run_side(flag_value):
    siege = load_siege(flag_value)
    mixin = siege.SiegeMixin()
    mixin.map_grid = None
    selected = []
    rows_out = []
    for name in POOL:
        w, h, rows, cores = parse_map26(ROOT / "maps" / f"{name}.map26")
        a = next(c for c in cores if c[0] == 0)
        b = next(c for c in cores if c[0] == 1)
        ours = Position(a[1], a[2])
        E = Position(b[1], b[2])
        ct = FakeCt(w, h, rows)
        mixin.map_grid = None  # fresh per-map disambiguation cache
        ok = mixin._fs_map_gated(w, h, ours, E, ct)
        # `ok=False` here folds GATE + CRIPPLE; isolate CRIPPLE alone by
        # re-running with the two prior gates forced open (impossible without
        # editing the tree) -- instead, report which are structurally gated
        # (they always are, independent of the flag) so cripple-only can be
        # read by subtracting the known GATED set.
        rows_out.append((name, w, h, (a[1], a[2]), (b[1], b[2]), ok))
        if not ok:
            selected.append(name)
    return rows_out, set(selected)


GATED = {"antler", "archipelago", "fjordgate"}  # structurally refuse regardless of V524


def main():
    exact_rows, exact_refused = run_side(True)
    mutant_rows, mutant_refused = run_side(False)

    exact_cripple = exact_refused - GATED
    mutant_cripple = mutant_refused - GATED

    print("=== v524 LOKI_FS_V524 = True (exact match, this build) ===")
    for name, w, h, a, b, ok in exact_rows:
        seg = "GATED" if name in GATED else ("CRIPPLE" if not ok else "siege-active")
        print(f"  {name:14s} {w}x{h:<3d} core {a}/{b}  ok={ok}  -> {seg}")
    print(f"  CRIPPLE-refused (excl. GATED): {sorted(exact_cripple)}")
    print()
    print("=== v524 LOKI_FS_V524 = False (mutant: parent's coarse-only match) ===")
    for name, w, h, a, b, ok in mutant_rows:
        seg = "GATED" if name in GATED else ("CRIPPLE" if not ok else "siege-active")
        print(f"  {name:14s} {w}x{h:<3d} core {a}/{b}  ok={ok}  -> {seg}")
    print(f"  CRIPPLE-refused (excl. GATED): {sorted(mutant_cripple)}")
    print()

    ok1 = exact_cripple == EXPECT_EXACT
    ok2 = mutant_cripple == EXPECT_MUTANT
    print(f"VERDICT exact-match selects EXACTLY {{midgard, yulerune}}: {ok1}  (got {sorted(exact_cripple)})")
    print(f"VERDICT mutant re-selects the 4-map collision: {ok2}  (got {sorted(mutant_cripple)})")
    if not (ok1 and ok2):
        raise SystemExit("PREDICATE TABLE FAILED")
    print("PREDICATE TABLE OK, both directions.")


if __name__ == "__main__":
    main()
