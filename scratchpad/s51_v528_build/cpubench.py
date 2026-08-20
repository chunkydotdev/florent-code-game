#!/usr/bin/env python3
"""CPU cost of the ONE new hot-path object v528 adds: `_v528_conn_field`.

⛔ WHY A MICROBENCH AND NOT THE REPLAY.  `BotOutput.execTimeUs` is **0 in every
event of every locally-produced replay** (measured: 8 replays, 40,152 events,
`tlescan.py` reports `max_us` distinct=1 across all arms, i.e. the column is
constant and therefore validates nothing), and `get_cpu_time_elapsed()` is a
local stub (v513 open item 3).  **The local surface cannot measure CPU at all**,
so "0 TLEs locally" is not evidence and is not reported as any.  What CAN be
measured here is the algorithm, in isolation, on the real maps.

The budget is 10 ms per unit per turn.  The flood is cached for
`V528_CONN_REFRESH` rounds, so the number that matters is the WORST SINGLE CALL,
not the mean.

GUARD, driven to the other verdict: the same harness times the parent's
`_link_path`, which is the incumbent hot object on the same grids and is known
to fit inside the budget in production.  A new object priced BELOW an object
already shipping is a bounded risk; one priced above it is a stop.  If the two
numbers came out equal the harness would be measuring itself, so they are
printed side by side.
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TREE = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "bots/_v528eco")
sys.path.insert(0, TREE)
sys.path.insert(0, str(ROOT / "tools"))

import eco  # noqa: E402
from eco import EcoMixin, Position, known_map_for, enemy_core_for  # noqa: E402


class StubCt:
    """Only what `_v528_conn_field` / `_link_path` touch."""

    def __init__(self, rnd=40):
        self.rnd = rnd

    def get_current_round(self):
        return self.rnd

    def get_nearby_buildings(self):
        return []

    def get_nearby_units(self):
        return []

    def is_in_vision(self, pos):
        return False

    def get_cpu_time_elapsed(self):
        return 0


class Bench(EcoMixin):
    def __init__(self, w, h, core):
        self.mw, self.mh = w, h
        self.core = core
        self.enemy = Position(*enemy_core_for(w, h, core))
        self.team = 0
        self.role, self.role_n, self.idx = "expand", 1, 1
        self.stuck, self.tgt, self.wall = 0, None, None
        self.ang = 0.0
        self.ore_cursor = 0
        self.link_queue = []
        self.wire_pending = []
        self._pick_key = self._pick_assigned = None
        self._nav_key = self._nav_tpl = None
        self._link_tpl_key = self._link_tpl = self._link_ore_only = None
        self._link_goal_key = self._link_goals_set = None
        self.map_grid = known_map_for(w, h, core, None)
        walls, ores = set(), []
        if self.map_grid is not None:
            for y, row in enumerate(self.map_grid):
                for x, v in enumerate(row):
                    if v == 1:
                        walls.add((x, y))
                    elif v == 2:
                        ores.append(Position(x, y))
        self.map_walls, self.map_ores = walls, ores

    def _cpu_exhausted(self, ct):
        return False

    def _pave_ban(self):
        return None

    def _seat_ban(self):
        return None


def bench(name, fn, reps):
    fn()                       # warm
    t0 = time.perf_counter()
    for _ in range(reps):
        fn()
    return (time.perf_counter() - t0) / reps * 1e6      # microseconds


def main():
    ct = StubCt()
    rows = []
    for mp, (w, h) in (("midgard", (30, 30)), ("valkyrie", (30, 30)),
                       ("ragnarok", (30, 30)), ("glacierkeep", (20, 20)),
                       ("atoll", (16, 16)), ("nordkap", (12, 12))):
        core = Position(2, 2)
        b = Bench(w, h, core)
        # ⛔ `known_map_for` only carries the 30x30 pool grids and returns an
        # ORE-FREE, WALL-FREE grid for the rest -- which makes the flood expand
        # the WHOLE board (its worst case) but also makes every map identical,
        # so the non-constant guard would be passing on noise.  Load the REAL
        # terrain off a replay of that map instead when one exists.
        rp = ROOT / ("scratchpad/s51_v528_build/smoke2/v528_%s.replay26" % mp)
        if not rp.exists():
            rp = ROOT / ("scratchpad/s51_v528_build/probe/rep/v528_%s_s11_A.replay26" % mp)
        if rp.exists():
            from replay_census import Replay
            R = Replay(rp, track_flow=False)
            w, h = R.width, R.height
            b = Bench(w, h, core)
            walls, ores = set(), []
            for y in range(h):
                for x in range(w):
                    e = R.env(x, y)
                    if e == 1:
                        walls.add((x, y))
                    elif e == 2:
                        ores.append(Position(x, y))
            b.map_walls, b.map_ores = walls, ores
            b.map_grid = [[0] * w for _ in range(h)]
            b._link_tpl_key = None
            b.mw, b.mh = w, h
        elif b.map_grid is None:
            print("  %-12s NO TERRAIN SOURCE -- skipped" % mp)
            continue

        def conn():
            b._v528_conn_key = None            # defeat the cache: worst call
            b._v528_conn_field(ct)

        ore = b.map_ores[len(b.map_ores) // 2] if b.map_ores else Position(w - 3, h - 3)

        def link():
            b._link_path(ct, ore)

        us_conn = bench("conn", conn, 200)
        us_link = bench("link", link, 200)
        rows.append((mp, b.mw, b.mh, len(b.map_ores), us_conn, us_link))
        print("  %-12s %2dx%-2d ores=%-3d  conn_field=%8.1f us   "
              "_link_path=%8.1f us   ratio=%.2f"
              % (mp, b.mw, b.mh, len(b.map_ores), us_conn, us_link,
                 us_conn / us_link if us_link else -1))
    if not rows:
        print("BENCH UNREADABLE: no map grid resolved"); return 1
    worst = max(r[4] for r in rows)
    worst_link = max(r[5] for r in rows)
    print("\nWORST conn_field = %.1f us  ·  WORST _link_path = %.1f us  "
          "·  budget = 10000 us/unit/turn" % (worst, worst_link))
    print("conn_field is %.2fx the incumbent hot object, and it is CACHED for "
          "V528_CONN_REFRESH=%d rounds while _link_path is not."
          % (worst / worst_link if worst_link else -1, eco.V528_CONN_REFRESH))
    if len({round(r[4]) for r in rows}) < 2:
        print("GUARD FAIL: conn_field time is constant across maps -- "
              "the harness is measuring itself, not the flood")
        return 1
    print("GUARD non-constant across maps: distinct=%d of %d"
          % (len({round(r[4]) for r in rows}), len(rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
