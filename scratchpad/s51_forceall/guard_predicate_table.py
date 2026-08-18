import importlib
import sys
from pathlib import Path

ROOT = Path("/Users/junghard/Projects/Work/florent-code-game")
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))
from map_encode import parse_map26
from fcode import Environment, Position

POOL = ["antler", "archipelago", "auroraveil", "drakkarfjord", "drumlin",
        "fjordgate", "frostgate", "glacierkeep", "icefloe", "midgard",
        "nordkap", "ragnarok", "royale", "valkyrie", "yulerune"]


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


def load_siege(bot_dir):
    for m in ("doctrine", "eco", "siege"):
        sys.modules.pop(m, None)
    bot_dir = str(bot_dir)
    if bot_dir in sys.path:
        sys.path.remove(bot_dir)
    sys.path.insert(0, bot_dir)
    import doctrine
    import eco  # noqa: F401
    import siege
    return siege


def run_side(bot_dir):
    siege = load_siege(bot_dir)
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
        rows_out.append((name, w, h, ok))
        if not ok:
            selected.append(name)
    return rows_out, set(selected)


def main():
    print("=== UNMODIFIED bots/_v524exact ===")
    rows, refused = run_side(ROOT / "bots" / "_v524exact")
    for name, w, h, ok in rows:
        print(f"  {name:14s} {w}x{h:<3d} ok={ok}")
    print(f"  refused (stood-down) set: {sorted(refused)}  (n={len(refused)})")
    print()

    print("=== PROBE scratchpad/s51_forceall/arm_forceall ===")
    rows2, refused2 = run_side(ROOT / "scratchpad" / "s51_forceall" / "arm_forceall")
    for name, w, h, ok in rows2:
        print(f"  {name:14s} {w}x{h:<3d} ok={ok}")
    print(f"  refused (stood-down) set: {sorted(refused2)}  (n={len(refused2)})")
    print()

    EXPECT_STOOD_DOWN = {"antler", "archipelago", "fjordgate", "midgard", "yulerune"}
    ok1 = refused == EXPECT_STOOD_DOWN
    ok2 = refused2 == set()
    print(f"VERDICT unmodified v524 stands down EXACTLY {{antler,archipelago,fjordgate,midgard,yulerune}}: {ok1} (got {sorted(refused)})")
    print(f"VERDICT probe (forceall) stands down on NO map (all 15 siege-active): {ok2} (got {sorted(refused2)})")
    if not (ok1 and ok2):
        raise SystemExit("GUARD CHECK FAILED")
    print("GUARD CHECK OK, both ways.")


if __name__ == "__main__":
    main()
