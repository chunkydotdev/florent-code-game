#!/usr/bin/env python3
"""v525 CHANGE 1+2 verification: the 15-map standdown predicate table, both
ways.

Drives `_fs_map_gated` (the real siege.py method, imported unmodified) against
every `maps/*.map26` in the 15-map pool, with a fake `ct` that senses the
WHOLE board. Runs each map through BOTH `LOKI_FS_V525 = True` (this build, as
shipped) and `LOKI_FS_V525 = False` (the mutant -- must reproduce the true
parent `bots/_v524exact`'s standdown set exactly: GATED =
{antler, archipelago, fjordgate}, CRIPPLE = {midgard, yulerune}).

Usage: .venv/bin/python3 scratchpad/s51_v525_build/predicate_table.py
"""
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

# v525 ON: only midgard stays crippled; antler/fjordgate leave GATED, only
# archipelago remains gated (via FS_MAP_SKIP, unaffected by this build).
EXPECT_V525_ON_GATED = {"archipelago"}
EXPECT_V525_ON_CRIPPLE = {"midgard"}
# v525 OFF (mutant): reproduces bots/_v524exact exactly.
EXPECT_V525_OFF_GATED = {"antler", "archipelago", "fjordgate"}
EXPECT_V525_OFF_CRIPPLE = {"midgard", "yulerune"}


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
    for m in ("doctrine", "eco", "siege"):
        sys.modules.pop(m, None)
    bot_dir = str(ROOT / "bots" / "_v525flip")
    if bot_dir not in sys.path:
        sys.path.insert(0, bot_dir)
    import doctrine
    doctrine.LOKI_FS_V525 = flag_value
    import eco  # noqa: F401
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
        mixin.map_grid = None
        ok = mixin._fs_map_gated(w, h, ours, E, ct)
        rows_out.append((name, w, h, (a[1], a[2]), (b[1], b[2]), ok))
        if not ok:
            selected.append(name)
    return rows_out, set(selected)


# The gate is structural (dim/dsq/FS_MAP_SKIP) and independent of the cripple
# list; classify per-run since v525 changes what "GATED" even contains.
def classify(refused, gated_expected):
    gated = refused & gated_expected if gated_expected else set()
    return refused


def main():
    on_rows, on_refused = run_side(True)
    off_rows, off_refused = run_side(False)

    # GATED = refused independent of the cripple mechanism == the dim/dsq/
    # FS_MAP_SKIP set. We know it structurally per side (it's whatever is
    # refused that ISN'T on the flag's own cripple candidate set).
    on_cripple_candidates = {"midgard"}
    off_cripple_candidates = {"midgard", "yulerune"}
    on_gated = on_refused - on_cripple_candidates
    on_cripple = on_refused & on_cripple_candidates
    off_gated = off_refused - off_cripple_candidates
    off_cripple = off_refused & off_cripple_candidates

    def seg(name, refused, gated_set, cripple_set):
        if name in gated_set:
            return "GATED"
        if name in cripple_set:
            return "CRIPPLE"
        return "siege-active"

    print("=== v525 LOKI_FS_V525 = True (standdown flip, this build) ===")
    for name, w, h, a, b, ok in on_rows:
        s = seg(name, on_refused, on_gated, on_cripple)
        print(f"  {name:14s} {w}x{h:<3d} core {a}/{b}  ok={ok}  -> {s}")
    print(f"  GATED:   {sorted(on_gated)}")
    print(f"  CRIPPLE: {sorted(on_cripple)}")
    print()
    print("=== v525 LOKI_FS_V525 = False (mutant: true parent bots/_v524exact) ===")
    for name, w, h, a, b, ok in off_rows:
        s = seg(name, off_refused, off_gated, off_cripple)
        print(f"  {name:14s} {w}x{h:<3d} core {a}/{b}  ok={ok}  -> {s}")
    print(f"  GATED:   {sorted(off_gated)}")
    print(f"  CRIPPLE: {sorted(off_cripple)}")
    print()

    ok1 = on_gated == EXPECT_V525_ON_GATED and on_cripple == EXPECT_V525_ON_CRIPPLE
    ok2 = off_gated == EXPECT_V525_OFF_GATED and off_cripple == EXPECT_V525_OFF_CRIPPLE
    print(f"VERDICT v525=True stands down exactly {{archipelago}} GATED + {{midgard}} CRIPPLE: {ok1}")
    print(f"VERDICT v525=False reproduces the parent's 5 standdowns exactly: {ok2}")
    if not (ok1 and ok2):
        raise SystemExit("PREDICATE TABLE FAILED")
    print("PREDICATE TABLE OK, both directions.")


if __name__ == "__main__":
    main()
