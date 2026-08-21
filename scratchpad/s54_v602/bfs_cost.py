#!/usr/bin/env python3
"""Per-CALL cost of `_bfs_direction` on the biggest pool map (yggdrasil 30x30).

⛔ WHY NOT MEASURE IT INSIDE THE ENGINE: `ct.get_cpu_time_elapsed()` reads 0
under local `fcode run` even with --tle (manifest §4.2, thrice-known), and the
sandbox freezes `time.*` to a constant, so a bot CANNOT time itself locally.
This harness therefore calls the real method on the real board through a stub
Controller and times it with `time.perf_counter` in an ordinary process.

⚠ WHAT THIS IS AND IS NOT.  It is Python wall time for the flood on this
machine, which is the quantity the 10 ms per-unit budget is spent in.  It is NOT
the engine's own CPU accounting, and a platform `match test` is still owed
before any exposure.

Both-ways drive: the same board is timed with `map_grid = None` and
SK_SENSE_NAV's terrain absent (the v601 greedy path, which does no work at all)
so the reported delta is the cost the fix actually adds.
"""
import sys
import time
from pathlib import Path

ROOT = Path("/Users/junghard/Projects/Work/florent-code-game")
TREE = ROOT / "bots" / "_v602skalman"
sys.path.insert(0, str(TREE))
sys.path.insert(0, str(ROOT / "tools"))

from fcode import Direction, EntityType, Position   # noqa: E402
import main as botmain                              # noqa: E402
from replay_census import fields, packed_varints, read_pos, WIRE_LEN  # noqa: E402


def load_map(name):
    data = (ROOT / "maps" / f"{name}.map26").read_bytes()
    w = h = 0
    tiles = []
    cores = []
    for num, wire, val in fields(data):
        if num == 1:
            w = val
        elif num == 2:
            h = val
        elif num == 3:
            row = []
            for rn, rw, rv in fields(val):
                if rn == 1:
                    row.extend(packed_varints(rv) if rw == WIRE_LEN else [rv])
            tiles.append(row)
        elif num == 4:
            c = {"pos": (0, 0)}
            for cn, _cw, cv in fields(val):
                if cn == 3:
                    c["pos"] = read_pos(cv)
            cores.append(c)
    return w, h, tiles, cores


class StubCT:
    """The five getters `_bfs_direction` calls.  No entities: the flood then
    pays its FULL node budget (nothing prunes it), which is the worst case."""

    def __init__(self, pos):
        self.pos = pos

    def get_position(self, eid=None):
        return self.pos

    def get_id(self):
        return 1

    def get_nearby_entities(self, dsq=None):
        return []

    def get_entity_type(self, eid=None):
        return EntityType.BUILDER_BOT

    def get_cpu_time_elapsed(self):
        return 0


def run(name, n=400):
    w, h, tiles, cores = load_map(name)
    walls = {(x, y) for y in range(h) for x in range(w) if tiles[y][x] == 1}
    ours = Position(*cores[0]["pos"])
    theirs = Position(*cores[1]["pos"])
    p = botmain.Player()
    p.mw, p.mh = w, h
    p.core, p.enemy = ours, theirs
    p.map_walls = set(walls)
    p.ore_scanned = set((x, y) for y in range(h) for x in range(w))  # terrain_known
    p.role_parity = 0
    ct = StubCT(Position(ours.x, ours.y + 2))
    target = Position(theirs.x - 1, theirs.y)          # the far corner of the map

    # --- ARM 1: the v602 flood (sensed terrain, grid absent) ----------------
    p.map_grid = None
    d = p._bfs_direction(ct, target)
    t0 = time.perf_counter()
    for _ in range(n):
        p._bfs_direction(ct, target)
    t1 = time.perf_counter()
    flood_us = (t1 - t0) / n * 1e6

    # --- ARM 2: the v601 fallback (no terrain -> greedy, does no work) ------
    p.ore_scanned = set()
    p2 = botmain.Player()
    p2.mw, p2.mh = w, h
    p2.core, p2.enemy = ours, theirs
    p2.map_walls = set()
    p2.ore_scanned = set()
    p2.map_grid = None
    p2.role_parity = 0
    d2 = p2._bfs_direction(ct, target)
    t0 = time.perf_counter()
    for _ in range(n):
        p2._bfs_direction(ct, target)
    t1 = time.perf_counter()
    greedy_us = (t1 - t0) / n * 1e6

    print(f"{name:14s} {w}x{h} walls={len(walls):3d} "
          f"flood={flood_us:8.1f} us/call (step {d})   "
          f"greedy={greedy_us:6.1f} us/call (step {d2})   "
          f"delta={flood_us - greedy_us:8.1f} us  "
          f"= {100 * (flood_us - greedy_us) / 10000:.2f}% of the 10 ms turn")


if __name__ == "__main__":
    for m in (sys.argv[1:] or ["yggdrasil", "fimbulwinter", "glacierkeep"]):
        run(m)
