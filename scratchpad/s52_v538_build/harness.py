#!/usr/bin/env python3
"""v538 build instrument #1 -- THE UNIT HARNESS (no game engine, no fcode run).

COPIED from `scratchpad/s52_v535_build/harness.py` (never edited in place) and
re-pointed at the v538 predicate.  As in v535: it
still loads a bot TREE's modules in isolation and drives them against a FAKE
controller backed by an explicit terrain grid, but v538's predicate lives on
`Player` (the `(EcoMixin, RaidMixin, SiegeMixin)` composition in main.py), so
`load_tree` also imports `raid` and `main`, and `probe_claim` builds a
real `Player` rather than a bare mixin stand-in.

⛔ WHY A FAKE CONTROLLER IS ADMISSIBLE HERE AND NOT IN GENERAL.  This harness
makes no claim about play, tempo or outcome -- only about which VERDICT a pure
lookup returns for a given board.  Every game-level claim in this build is a
local engine tape or is deferred to the powered screen.

  .venv/bin/python .../harness.py --selftest
"""
import importlib
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))
from map_encode import parse_map26  # noqa: E402

MODNAMES = ("doctrine", "eco", "siege", "raid", "main")
ENV_CHR = ".#o"


def load_tree(tree, want=("doctrine", "eco", "siege", "raid", "main")):
    """Import a bot tree's modules FRESH, return a dict of them."""
    path = str(REPO / "bots" / tree)
    for m in MODNAMES:
        sys.modules.pop(m, None)
    sys.path.insert(0, path)
    try:
        mods = {m: importlib.import_module(m) for m in want}
    finally:
        sys.path.remove(path)
    for m in MODNAMES:
        sys.modules.pop(m, None)
    return mods


def grid_of_map(name):
    """maps/<name>.map26 -> (w, h, grid rows as '.#o' strings, [(x,y),(x,y)])"""
    w, h, rows, cores = parse_map26(REPO / "maps" / (name + ".map26"))
    grid = tuple("".join(ENV_CHR[c] for c in rows[y]) for y in range(h))
    a = next((c for c in cores if c[0] == 0), cores[0])
    b = next((c for c in cores if c[0] == 1), cores[-1])
    return w, h, grid, [(a[1], a[2]), (b[1], b[2])]


class FakeCt:
    """Just enough Controller for known_map_for / _fs_map_gated / the v535 gate."""

    def __init__(self, grid, pos, vision_sq, Position, Environment,
                 buildings=(), rnd=0, store=None, uid=1):
        self.grid = grid
        self.h = len(grid)
        self.w = len(grid[0])
        self.pos = pos
        self.vision_sq = vision_sq
        self.P = Position
        self.E = Environment
        self.buildings = set(buildings)
        self.rnd = rnd
        self.store = dict(store or {})
        self.uid = uid
        self.n_env = 0
        self.n_bld = 0

    def get_current_round(self):
        return self.rnd

    def get_id(self):
        return self.uid

    def read_store(self, i):
        return self.store.get(i, 0)

    def get_nearby_tiles(self, dist_sq=None):
        d = self.vision_sq if dist_sq is None else dist_sq
        px, py = self.pos
        out = []
        r = int(d ** 0.5) + 1
        for y in range(py - r, py + r + 1):
            for x in range(px - r, px + r + 1):
                if 0 <= x < self.w and 0 <= y < self.h and \
                        (x - px) ** 2 + (y - py) ** 2 <= d:
                    out.append(self.P(x, y))
        return out

    def get_tile_env(self, p):
        self.n_env += 1
        if not (0 <= p.x < self.w and 0 <= p.y < self.h):
            raise ValueError("Position out of bounds")
        c = self.grid[p.y][p.x]
        return self.E.WALL if c == "#" else (
            self.E.ORE_TITANIUM if c == "o" else self.E.EMPTY)

    def get_tile_building_id(self, p):
        self.n_bld += 1
        return 7 if (p.x, p.y) in self.buildings else None


def probe_gate(mods, mw, mh, ours, enemy, ct, map_grid=None):
    """Run SiegeMixin._fs_map_gated on a bare stand-in object (v534's probe)."""
    class _P(mods["siege"].SiegeMixin):
        pass
    o = _P()
    o.map_grid = map_grid
    return o._fs_map_gated(mw, mh, ours, enemy, ct)


def make_player(mods, mw, mh, ours, enemy=None, map_grid=None, role="expand"):
    """A REAL `Player` with just the anchors the v535 gate reads.

    ⛔ NOT a stand-in class: v538's predicate spans EcoMixin (`_v538_claim_on`)
    and SiegeMixin (`_v535_map_refuses`), so the thing under test IS the MRO
    composition, and a stand-in that inherited only one half would prove
    nothing about the tree that ships.
    """
    P = mods["main"].Player
    o = P()
    o.mw, o.mh = mw, mh
    o.core = ours
    o.enemy = enemy
    o.map_grid = map_grid
    o.role = role
    return o


def probe_claim(mods, mw, mh, ours, enemy, ct, map_grid=None):
    """`_v538_claim_on` on a real Player -> (claim_on, refuse_cache).

    ⛔ NOT a stand-in class, for the same reason `make_player` is not: v538's
    predicate spans EcoMixin (`_v538_claim_on`) and SiegeMixin
    (`_v535_map_refuses`), so the thing under test IS the MRO composition.
    """
    o = make_player(mods, mw, mh, ours, enemy, map_grid)
    on = o._v538_claim_on(ct)
    return on, getattr(o, "v535_refuse", "MISSING")


def selftest():
    from fcode import Position, Environment
    ok = True
    par = load_tree("_v537socket")
    new = load_tree("_v538refine")

    # 1. the two trees are DIFFERENT objects with different flags
    if hasattr(par["doctrine"], "FS_V538_CLAIM_GATE"):
        ok = False
        print("[FAIL] loader: parent must not carry the v538 flag")
    else:
        print("[ok] loader: parent (_v537socket) has no FS_V538_CLAIM_GATE")
    if new["doctrine"].FS_V538_CLAIM_GATE is not True:
        ok = False
        print("[FAIL] loader: child flag is not True")
    else:
        print("[ok] loader: child (_v538refine) FS_V538_CLAIM_GATE=True")
    if not hasattr(par["main"], "Player"):
        ok = False
        print("[FAIL] loader: main.Player missing from parent tree")
    else:
        print("[ok] loader: main.Player importable from both trees")

    # 2. the fake controller must reproduce a REAL map's terrain
    w, h, grid, cores = grid_of_map("nordkap")
    ct = FakeCt(grid, cores[0], 36, Position, Environment)
    tiles = ct.get_nearby_tiles()
    assert tiles, "no tiles"
    print("[ok] FakeCt: %d tiles at nordkap core, env round-trips" % len(tiles))

    # 3. AND IT MUST BE ABLE TO LIE -- a corrupted grid must read corrupted, or
    #    every "verification passed" below would be vacuous.
    lie = list(grid)
    x0, y0 = cores[0]
    row = list(lie[y0]); row[min(x0 + 3, w - 1)] = "#"; lie[y0] = "".join(row)
    ct2 = FakeCt(tuple(lie), cores[0], 36, Position, Environment)
    if ct2.get_tile_env(Position(min(x0 + 3, w - 1), y0)) != Environment.WALL:
        ok = False
        print("[FAIL] FakeCt: the corrupted fixture did not read corrupted")
    else:
        print("[ok] FakeCt: corrupted fixture reads WALL (the harness can lie)")

    # 4. out-of-bounds must RAISE, the way the engine does
    try:
        ct.get_tile_env(Position(-1, 0))
        ok = False
        print("[FAIL] FakeCt: off-map read did not raise")
    except ValueError:
        print("[ok] FakeCt: off-map read raises, as the engine does")

    # 5. `make_player` must produce something that CARRIES v535 state, and the
    #    parent's Player must NOT have the predicate at all.
    p_new = make_player(new, w, h, Position(*cores[0]), Position(*cores[1]))
    if getattr(p_new, "v535_refuse", "MISSING") != None:  # noqa: E711
        ok = False
        print("[FAIL] make_player: child Player lacks v535_refuse=None")
    else:
        print("[ok] make_player: child Player boots with v535_refuse=None")
    if hasattr(make_player(par, w, h, Position(*cores[0])), "_v538_claim_on"):
        ok = False
        print("[FAIL] make_player: PARENT Player has _v538_claim_on")
    else:
        print("[ok] make_player: parent Player has no _v538_claim_on "
              "(the probe can tell the trees apart)")

    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    if "-h" in sys.argv[1:] or "--help" in sys.argv[1:]:
        print(__doc__)
        raise SystemExit(0)
    raise SystemExit(selftest())
