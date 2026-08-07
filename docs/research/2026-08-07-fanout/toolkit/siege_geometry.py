#!/usr/bin/env python3
"""Siege-ring geometry for Florent Code League maps (.map26).

Reusable toolkit for thread 6 (BARRIER SIEGE-RING GEOMETRY) and the later
cross-check wave.  Read-only: parses maps/*.map26 and computes, per map and
per core seat:

  * the THREAT SET   -- tiles from which a planted turret can hit our Core
  * the PLANTABLE set -- threat tiles an enemy Builder Bot may legally build on
  * the REACHABLE set -- plantable threat tiles with an enemy-reachable
    orthogonal standing tile
  * OCCUPY cost      -- 3 Ti x |reachable plantable sentinel-threat set|
  * MIN VERTEX CUT   -- cheapest set of barrier tiles that separates the enemy
    approach from every plant opportunity (walls are free blockers)
  * LAUNCHER BYPASS  -- whether a Launcher outside the cut can throw a builder
    onto a passable tile inside it (throw r^2 = 26)

Model facts used (docs/game-model.md wins over CLAUDE.md):
  * Core is 2x2; map header stores the NW corner.  Its footprint is never
    bot-passable, for either team.
  * Builder-passable: EMPTY, ORE_TITANIUM, Conveyor, Splitter (either team).
    Impassable: WALL, Harvester, Barrier, turret, Core, another Builder Bot.
    At round 0 the only buildings are the two Cores, so passable == not WALL
    and not a Core footprint tile.
  * Barrier: 30 HP, 3 Ti, blocks movement AND LOS, "cannot be placed on a wall
    tile".  Ore is not a wall and is_tile_empty() is "no building and not a
    wall", so barriers ARE placeable on ore (see verify_barrier_on_ore()).
  * Gunner  : single-tile-wide forward ray, r^2 = 13, blocked by walls and
    stopped by the first targetable tile.
  * Sentinel: single-tile-wide forward ray, r^2 = 32, NEVER blocked.
  * Both turrets may face any of the 8 directions, so a turret threatens only
    tiles that are row-, column- or diagonal-ALIGNED with it.
  * Launcher: pickup r^2 = 2 (incl. diagonal), throw r^2 = 26 measured from the
    Launcher, target must be bot-passable.

Usage:
    .venv/bin/python siege_geometry.py                 # table over maps/*.map26
    .venv/bin/python siege_geometry.py --maps-dir DIR
    .venv/bin/python siege_geometry.py --detail hive   # per-seat dump + cut tiles
    .venv/bin/python siege_geometry.py --ascii hive    # ascii map with overlays
"""

from __future__ import annotations

import argparse
import sys
from collections import deque
from pathlib import Path

# --- protobuf (stdlib only; same minimal decoder as tools/replay_census.py) ---

WIRE_VARINT, WIRE_64, WIRE_LEN, WIRE_32 = 0, 1, 2, 5


def _varint(buf: bytes, i: int):
    result = shift = 0
    while True:
        byte = buf[i]
        i += 1
        result |= (byte & 0x7F) << shift
        if not byte & 0x80:
            return result, i
        shift += 7


def fields(buf: bytes):
    i, n = 0, len(buf)
    while i < n:
        tag, i = _varint(buf, i)
        num, wire = tag >> 3, tag & 7
        if wire == WIRE_VARINT:
            value, i = _varint(buf, i)
            yield num, wire, value
        elif wire == WIRE_LEN:
            length, i = _varint(buf, i)
            yield num, wire, buf[i:i + length]
            i += length
        elif wire == WIRE_32:
            yield num, wire, buf[i:i + 4]
            i += 4
        elif wire == WIRE_64:
            yield num, wire, buf[i:i + 8]
            i += 8
        else:
            raise ValueError(f"bad wire type {wire} for field {num}")


def _packed(buf: bytes):
    out, i, n = [], 0, len(buf)
    while i < n:
        v, i = _varint(buf, i)
        out.append(v)
    return out


def _pos(buf: bytes):
    d = {num: val for num, _, val in fields(buf)}
    return (d.get(1, 0), d.get(2, 0))


ENV_EMPTY, ENV_WALL, ENV_ORE = 0, 1, 2
SYMMETRY_NAME = {0: "rotational", 1: "horizontal", 2: "vertical"}
CARDINALS = ((0, -1), (1, 0), (0, 1), (-1, 0))
DIRS8 = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1))

GUNNER_R2 = 13
SENTINEL_R2 = 32
LAUNCHER_THROW_R2 = 26
CORE_ACTION_R2 = 8          # core spawn ring
BARRIER_COST = 3            # base; scaled cost is floor(scale * 3)


class GameMap:
    """A parsed .map26."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self.name = self.path.stem
        data = self.path.read_bytes()
        self.width = self.height = 0
        self.tiles: list[list[int]] = []
        self.cores: list[dict] = []
        self.symmetry = 0
        for num, wire, value in fields(data):
            if num == 1:
                self.width = value
            elif num == 2:
                self.height = value
            elif num == 3:
                row = []
                for rnum, rwire, rval in fields(value):
                    if rnum == 1:
                        row.extend(_packed(rval) if rwire == WIRE_LEN else [rval])
                self.tiles.append(row)
            elif num == 4:
                core = {"id": 0, "team": 0, "pos": (0, 0)}
                for cnum, _cw, cval in fields(value):
                    if cnum == 1:
                        core["id"] = cval
                    elif cnum == 2:
                        core["team"] = cval
                    elif cnum == 3:
                        core["pos"] = _pos(cval)
                self.cores.append(core)
            elif num == 5:
                self.symmetry = value
        if len(self.tiles) != self.height or any(len(r) != self.width for r in self.tiles):
            raise ValueError(f"{path}: tile grid {len(self.tiles)} rows does not match "
                             f"{self.width}x{self.height}")
        if len(self.cores) != 2:
            raise ValueError(f"{path}: expected 2 cores, got {len(self.cores)}")
        self.core_by_team = {c["team"]: c["pos"] for c in self.cores}

    # -- terrain --

    def env(self, x, y):
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.tiles[y][x]
        return ENV_WALL

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def footprint(self, team):
        x, y = self.core_by_team[team]
        return {(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)}

    @property
    def all_core_tiles(self):
        return self.footprint(0) | self.footprint(1)

    def counts(self):
        walls = sum(1 for r in self.tiles for t in r if t == ENV_WALL)
        ore = sum(1 for r in self.tiles for t in r if t == ENV_ORE)
        return walls, ore


# --- geometry helpers --------------------------------------------------------

def dsq(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def nearest_footprint_dsq(tile, footprint):
    return min(dsq(tile, c) for c in footprint)


def aligned(src, dst):
    """True if dst lies on one of the 8 rays out of src (turret facings)."""
    dx, dy = dst[0] - src[0], dst[1] - src[1]
    if dx == 0 and dy == 0:
        return False
    return dx == 0 or dy == 0 or abs(dx) == abs(dy)


def ray_tiles_between(src, dst):
    """Tiles strictly between src and dst along their shared ray."""
    dx, dy = dst[0] - src[0], dst[1] - src[1]
    steps = max(abs(dx), abs(dy))
    ux = (dx > 0) - (dx < 0)
    uy = (dy > 0) - (dy < 0)
    return [(src[0] + ux * k, src[1] + uy * k) for k in range(1, steps)]


# --- per-seat analysis -------------------------------------------------------

class SeatAnalysis:
    """Siege geometry for one map, one defending core seat."""

    def __init__(self, gmap: GameMap, team: int, half_restricted: bool = True,
                 local_r2: int | None = None):
        self.map = gmap
        self.team = team           # the DEFENDER (our core)
        self.enemy = 1 - team
        self.half_restricted = half_restricted
        # local_r2: if set, barriers may only be placed within this dsq of our
        # Core's NW corner -- the "siege ring around the core" reading, as
        # opposed to a map-halving wall at the midline.
        self.local_r2 = local_r2

        self.fp = gmap.footprint(team)
        self.efp = gmap.footprint(self.enemy)
        self.nw = gmap.core_by_team[team]
        self.core_tiles = self.fp | self.efp

        self._passable()
        self._threat_sets()
        self._reachability()
        self._occupy()
        self._mincut()
        self._launcher_flag()

    # -- passability at round 0 (bare map: only the two Cores are buildings) --

    def _passable(self):
        g = self.map
        self.passable = set()
        for y in range(g.height):
            for x in range(g.width):
                if g.env(x, y) == ENV_WALL:
                    continue
                if (x, y) in self.core_tiles:
                    continue
                self.passable.add((x, y))

    def plantable(self, tile):
        """A Builder Bot could legally place a building on this tile."""
        g = self.map
        x, y = tile
        if not g.in_bounds(x, y):
            return False
        if g.env(x, y) == ENV_WALL:
            return False
        if tile in self.core_tiles:
            return False
        return True   # ore is buildable for everything except... nothing. See docstring.

    # -- threat sets --

    def _threat_sets(self):
        g = self.map
        self.sentinel_threat = set()
        self.gunner_threat = set()
        self.radius_only_32 = set()      # naive dsq<=32 band, no alignment
        for y in range(g.height):
            for x in range(g.width):
                t = (x, y)
                if t in self.core_tiles:
                    continue
                if g.env(x, y) == ENV_WALL:
                    continue
                d = nearest_footprint_dsq(t, self.fp)
                if d <= SENTINEL_R2:
                    self.radius_only_32.add(t)
                # sentinel: aligned, r2<=32, never blocked
                if any(aligned(t, c) and dsq(t, c) <= SENTINEL_R2 for c in self.fp):
                    self.sentinel_threat.add(t)
                # gunner: aligned, r2<=13, walls block; core must be first
                # targetable tile on the ray (bare map -> only walls matter)
                for c in self.fp:
                    if not aligned(t, c) or dsq(t, c) > GUNNER_R2:
                        continue
                    blocked = False
                    for mid in ray_tiles_between(t, c):
                        if g.env(*mid) == ENV_WALL or mid in self.core_tiles:
                            # another core tile in the way is still the Core:
                            # it is targetable and it IS our core, so fine.
                            if mid in self.fp:
                                continue
                            blocked = True
                            break
                    if not blocked:
                        self.gunner_threat.add(t)
                        break
        self.threat = self.sentinel_threat | self.gunner_threat   # sentinel superset in practice
        self.gunner_only = self.gunner_threat - self.sentinel_threat
        # Two distance conventions, because the observed plant band (10-41) was
        # reported against the NW corner, not the nearest footprint tile.
        self.fp_dsq = {t: nearest_footprint_dsq(t, self.fp) for t in self.sentinel_threat}
        self.nw_dsq = {t: dsq(t, self.nw) for t in self.sentinel_threat}
        self.nw_band_1041 = {t for t in self.sentinel_threat if 10 <= self.nw_dsq[t] <= 41}
        # everything the naive "NW-corner dsq in [10,41]" band would cover,
        # threat or not -- i.e. what a band-based deny rule would have to buy
        self.nw_band_all = set()
        for y in range(g.height):
            for x in range(g.width):
                t = (x, y)
                if t in self.core_tiles or g.env(x, y) == ENV_WALL:
                    continue
                if 10 <= dsq(t, self.nw) <= 41:
                    self.nw_band_all.add(t)

    # -- reachability --

    def spawn_ring(self, team):
        """Tiles the Core may spawn a Builder Bot on: passable, within r^2=8 of
        the NW footprint corner and adjacent to the footprint."""
        g = self.map
        nx, ny = g.core_by_team[team]
        fp = g.footprint(team)
        ring = set()
        for dy in range(-3, 5):
            for dx in range(-3, 5):
                t = (nx + dx, ny + dy)
                if not g.in_bounds(*t) or t not in self.passable:
                    continue
                if dsq(t, (nx, ny)) > CORE_ACTION_R2:
                    continue
                if min(max(abs(t[0] - f[0]), abs(t[1] - f[1])) for f in fp) != 1:
                    continue
                ring.add(t)
        return ring

    def _bfs(self, sources, blocked=frozenset()):
        dist = {}
        q = deque()
        for s in sources:
            if s in self.passable and s not in blocked:
                dist[s] = 0
                q.append(s)
        while q:
            v = q.popleft()
            for dx, dy in CARDINALS:
                u = (v[0] + dx, v[1] + dy)
                if u in self.passable and u not in blocked and u not in dist:
                    dist[u] = dist[v] + 1
                    q.append(u)
        return dist

    def _reachability(self):
        self.enemy_ring = self.spawn_ring(self.enemy)
        self.own_ring = self.spawn_ring(self.team)
        self.dist_enemy = self._bfs(self.enemy_ring)
        self.dist_own = self._bfs(self.own_ring)

        def reach_plant(threatset, dist):
            out = set()
            for t in threatset:
                if not self.plantable(t):
                    continue
                for dx, dy in CARDINALS:
                    p = (t[0] + dx, t[1] + dy)
                    if p in dist:
                        out.add(t)
                        break
            return out

        self.sent_reach = reach_plant(self.sentinel_threat, self.dist_enemy)
        self.gun_reach = reach_plant(self.gunner_threat, self.dist_enemy)
        self.sent_reach_own = reach_plant(self.sentinel_threat, self.dist_own)

    # -- (a) occupy every reachable plantable sentinel-threat tile --

    def _occupy(self):
        self.occupy_tiles = set(self.sent_reach)
        # We must be able to stand next to each tile to place the barrier.
        self.occupy_buildable = {t for t in self.occupy_tiles if t in self.sent_reach_own}
        self.occupy_cost = BARRIER_COST * len(self.occupy_tiles)
        # The claim's own reading: only the tiles in the OBSERVED plant band
        # (NW-corner dsq 10..41) that are actually sentinel-threatening.
        self.band_occupy = {t for t in self.sent_reach if t in self.nw_band_1041}
        self.band_occupy_cost = BARRIER_COST * len(self.band_occupy)
        # How much of the threat set the Core itself can see (vision r^2 = 36
        # measured from the NW corner) -- matters for the trigger spec.
        self.threat_in_core_vision = len(
            [t for t in self.sentinel_threat if self.nw_dsq[t] <= 36])
        self.max_nw_dsq = max(self.nw_dsq.values()) if self.nw_dsq else 0
        own_half = {t for t in self.occupy_tiles
                    if self.dist_own.get(t) is not None
                    and self.dist_own.get(t, 10 ** 9) <= self.dist_enemy.get(t, 10 ** 9)}
        self.occupy_own_half = own_half
        self.occupy_own_half_cost = BARRIER_COST * len(own_half)

    # -- (b) minimal vertex cut --

    def _mincut(self):
        """Min-cost set of barrier tiles s.t. no enemy builder can reach a
        standing tile orthogonally adjacent to a surviving plantable threat
        tile.  Node-split max-flow; each barrier-able tile has capacity 1."""
        INF = 10 ** 6
        tiles = sorted(self.passable)
        idx = {t: i for i, t in enumerate(tiles)}
        n = len(tiles)
        S, T = 2 * n, 2 * n + 1
        N = 2 * n + 2
        graph = [[] for _ in range(N)]

        def add(u, v, cap):
            graph[u].append([v, cap, len(graph[v])])
            graph[v].append([u, 0, len(graph[u]) - 1])

        cuttable = set()
        for t in tiles:
            i = idx[t]
            cap = 1
            if t in self.enemy_ring:
                cap = INF                      # cannot barrier their spawn ring
            elif t not in self.dist_own:
                cap = INF                      # we cannot reach it to build there
            elif self.local_r2 is not None and dsq(t, self.nw) > self.local_r2 \
                    and t not in self.sent_reach:
                cap = INF                      # outside the ring we are pricing
            elif self.half_restricted and t not in self.sent_reach:
                # Only our own half is realistically ours to wall.  Threat tiles
                # are always exempt: they sit against our Core, and occupying
                # every one of them is by construction a feasible cut, so the
                # min cut can never come out infeasible.
                de = self.dist_enemy.get(t)
                do = self.dist_own.get(t)
                if de is not None and do is not None and do > de:
                    cap = INF
            if cap == 1:
                cuttable.add(t)
            add(2 * i, 2 * i + 1, cap)

        for t in tiles:
            i = idx[t]
            for dx, dy in CARDINALS:
                u = (t[0] + dx, t[1] + dy)
                if u in idx:
                    add(2 * i + 1, 2 * idx[u], INF)

        for t in self.enemy_ring:
            add(S, 2 * idx[t], INF)

        # A threat tile inside the enemy's own spawn ring can never be denied:
        # they can plant on their own doorstep and still reach our Core.  Those
        # are reported separately rather than being allowed to blow the flow up.
        self.undeniable = {t for t in self.sent_reach
                           if t in self.enemy_ring or t not in self.dist_own}
        sinks = 0
        for t in self.sent_reach:
            if t in self.undeniable:
                continue
            add(2 * idx[t] + 1, T, INF)
            sinks += 1
        self.sink_count = sinks
        self.cuttable_count = len(cuttable)

        if sinks == 0:
            self.mincut_tiles = set()
            self.mincut_cost = 0
            self.mincut_flow = 0
            return

        flow = _dinic(graph, S, T, N)
        self.mincut_flow = flow
        self.mincut_cost = BARRIER_COST * flow

        # recover the cut: tiles whose in-node is reachable in the residual
        # graph but whose out-node is not.
        seen = [False] * N
        dq = deque([S])
        seen[S] = True
        while dq:
            v = dq.popleft()
            for e in graph[v]:
                if e[1] > 0 and not seen[e[0]]:
                    seen[e[0]] = True
                    dq.append(e[0])
        cut = set()
        for t in tiles:
            i = idx[t]
            if seen[2 * i] and not seen[2 * i + 1]:
                cut.add(t)
        self.mincut_tiles = cut

    # -- launcher bypass + what the wall costs our own economy --

    def _launcher_flag(self):
        """With the cut in place, can a Launcher outside it throw a builder onto
        a passable tile inside the protected pocket?  (throw r^2 = 26)"""
        g = self.map
        self.launcher_bypass = None
        self.launcher_min_dsq = None
        self.pocket_landing = 0
        self.pocket_plantable_threat = 0
        self.cut_in_enemy_half = 0
        self.ore_before = 0
        self.ore_after = 0
        our_ore = {t for t in self.dist_own
                   if g.env(*t) == ENV_ORE}
        self.ore_before = len(our_ore)
        if not self.mincut_tiles:
            self.ore_after = self.ore_before
            return
        for t in self.mincut_tiles:
            de, do = self.dist_enemy.get(t), self.dist_own.get(t)
            if de is not None and do is not None and do > de:
                self.cut_in_enemy_half += 1
        blocked = self.mincut_tiles
        outside = set(self._bfs(self.enemy_ring, blocked=blocked))
        pocket = {t for t in self.passable if t not in blocked and t not in outside}
        self.pocket_landing = len(pocket)
        self.pocket_plantable_threat = len(
            {t for t in self.sent_reach if t in pocket and t not in blocked})
        # ore our own builders can still walk to once the wall is up
        after = self._bfs(self.own_ring, blocked=blocked)
        self.ore_after = len({t for t in after if g.env(*t) == ENV_ORE})
        best = None
        for z in pocket:
            for l in outside:
                d = dsq(l, z)
                if best is None or d < best:
                    best = d
        self.launcher_min_dsq = best
        self.launcher_bypass = best is not None and best <= LAUNCHER_THROW_R2

    # -- reporting --

    def row(self):
        g = self.map
        return {
            "map": g.name,
            "w": g.width,
            "h": g.height,
            "sym": SYMMETRY_NAME.get(g.symmetry, str(g.symmetry)),
            "seat": "A" if self.team == 0 else "B",
            "core_nw": f"{self.nw[0]},{self.nw[1]}",
            "band_r32": len(self.radius_only_32),
            "nwband_1041": len(self.nw_band_all),
            "sent_threat": len(self.sentinel_threat),
            "gun_threat": len(self.gunner_threat),
            "gun_only": len(self.gunner_only),
            "sent_plant_reach": len(self.sent_reach),
            "gun_plant_reach": len(self.gun_reach),
            "occupy_ti": self.occupy_cost,
            "band_occ_ti": self.band_occupy_cost,
            "occ_half_ti": self.occupy_own_half_cost,
            "undeniable": len(self.undeniable),
            "mincut_tiles": len(self.mincut_tiles),
            "mincut_ti": self.mincut_cost,
            "cut_far": self.cut_in_enemy_half,
            "pocket": self.pocket_landing,
            "pocket_threat": self.pocket_plantable_threat,
            "ore_before": self.ore_before,
            "ore_after": self.ore_after,
            "launch_dsq": self.launcher_min_dsq,
            "launch_bypass": ("Y" if self.launcher_bypass else
                              ("n" if self.launcher_bypass is False else "-")),
            "core_sees": self.threat_in_core_vision,
            "max_nwdsq": self.max_nw_dsq,
        }


def _dinic(graph, S, T, N):
    INF = float("inf")
    flow = 0
    while True:
        level = [-1] * N
        level[S] = 0
        q = deque([S])
        while q:
            v = q.popleft()
            for e in graph[v]:
                if e[1] > 0 and level[e[0]] < 0:
                    level[e[0]] = level[v] + 1
                    q.append(e[0])
        if level[T] < 0:
            return flow
        it = [0] * N

        def dfs(v, f):
            if v == T:
                return f
            while it[v] < len(graph[v]):
                e = graph[v][it[v]]
                u = e[0]
                if e[1] > 0 and level[u] == level[v] + 1:
                    d = dfs(u, min(f, e[1]))
                    if d > 0:
                        e[1] -= d
                        graph[u][e[2]][1] += d
                        return d
                it[v] += 1
            return 0

        while True:
            f = dfs(S, INF)
            if f == 0:
                break
            flow += f


# --- ascii rendering ---------------------------------------------------------

def render(sa: SeatAnalysis):
    g = sa.map
    out = []
    for y in range(g.height):
        line = []
        for x in range(g.width):
            t = (x, y)
            if t in sa.fp:
                ch = "C"
            elif t in sa.efp:
                ch = "e"
            elif g.env(x, y) == ENV_WALL:
                ch = "#"
            elif t in sa.mincut_tiles:
                ch = "X"
            elif t in sa.sent_reach:
                ch = "s" if g.env(x, y) != ENV_ORE else "S"
            elif t in sa.sentinel_threat:
                ch = "."
            elif g.env(x, y) == ENV_ORE:
                ch = "o"
            else:
                ch = " "
            line.append(ch)
        out.append("".join(line))
    return "\n".join(out)


# --- barrier-on-ore verification from cached replays -------------------------

def verify_barrier_on_ore(replay_paths, repo="/Users/junghard/Projects/Work/florent-code-game"):
    """Scan replays for Barriers standing on ORE_TITANIUM tiles.

    docs/game-model.md only forbids barriers on WALL tiles; ore is
    "traversable, Harvester-buildable" and `is_tile_empty()` is "no building
    and not a wall".  bots/_v70sm shipped ore-denial barriers with a
    self-shutoff in case the engine refused them.  This is the empirical check.
    """
    sys.path.insert(0, str(repo))
    hits, checked = [], 0
    try:
        from tools.replay_census import Replay  # noqa
    except Exception:
        return None
    for p in replay_paths:
        try:
            r = Replay(Path(p), track_flow=False)
        except Exception:
            continue
        checked += 1
        for e in r.entities.values():
            if e.kind == "barrier":
                x, y = e.pos
                if r.env(x, y) == ENV_ORE:
                    hits.append((Path(p).name, e.pos, e.team, e.built_round))
    return checked, hits


# --- CLI ---------------------------------------------------------------------

COLS = ["map", "w", "h", "sym", "seat", "core_nw", "band_r32", "nwband_1041",
        "sent_threat", "gun_threat", "gun_only", "sent_plant_reach",
        "gun_plant_reach", "occupy_ti", "band_occ_ti", "occ_half_ti", "undeniable",
        "mincut_tiles", "mincut_ti", "cut_far",
        "pocket", "pocket_threat", "ore_before", "ore_after",
        "launch_dsq", "launch_bypass", "core_sees", "max_nwdsq",
        "ring_tiles", "ring_ti", "ring_ore_after", "ring_pocket"]


def analyse_dir(maps_dir: Path, half_restricted=True, local_r2=100):
    rows, seats = [], []
    for p in sorted(maps_dir.glob("*.map26")):
        g = GameMap(p)
        for team in (0, 1):
            sa = SeatAnalysis(g, team, half_restricted=half_restricted)
            r = sa.row()
            if local_r2 is not None:
                loc = SeatAnalysis(g, team, half_restricted=half_restricted,
                                   local_r2=local_r2)
                sa.local = loc
                r["ring_tiles"] = len(loc.mincut_tiles)
                r["ring_ti"] = loc.mincut_cost
                r["ring_ore_after"] = loc.ore_after
                r["ring_pocket"] = loc.pocket_landing
            seats.append(sa)
            rows.append(r)
    return rows, seats


def selfcheck(maps_dir: Path):
    """Assert the recovered cut really disconnects the enemy from every plant."""
    bad = 0
    for p in sorted(maps_dir.glob("*.map26")):
        g = GameMap(p)
        for team in (0, 1):
            sa = SeatAnalysis(g, team)
            after = sa._bfs(sa.enemy_ring, blocked=sa.mincut_tiles)
            leak = []
            for t in sa.sent_reach:
                if t in sa.undeniable or t in sa.mincut_tiles:
                    continue
                if any((t[0] + dx, t[1] + dy) in after for dx, dy in CARDINALS):
                    leak.append(t)
            status = "OK " if not leak else f"LEAK {len(leak)}"
            if leak:
                bad += 1
            print(f"{status} {g.name:<12} seat {'AB'[team]} cut={len(sa.mincut_tiles)} "
                  f"undeniable={len(sa.undeniable)} occupy={len(sa.sent_reach)}")
    print("cuts with leaks:", bad)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--maps-dir", default="/Users/junghard/Projects/Work/florent-code-game/maps")
    ap.add_argument("--detail", default=None, help="map name for a per-seat dump")
    ap.add_argument("--ascii", default=None, help="map name for an ascii overlay")
    ap.add_argument("--selfcheck", action="store_true",
                    help="verify each recovered cut actually disconnects")
    ap.add_argument("--unrestricted", action="store_true",
                    help="allow cuts anywhere, not just on our half")
    args = ap.parse_args()

    maps_dir = Path(args.maps_dir)
    if args.selfcheck:
        selfcheck(maps_dir)
        return
    rows, seats = analyse_dir(maps_dir, half_restricted=not args.unrestricted)

    if args.detail or args.ascii:
        want = args.detail or args.ascii
        for sa in seats:
            if sa.map.name != want:
                continue
            print(f"== {sa.map.name} seat {'A' if sa.team == 0 else 'B'} "
                  f"core NW {sa.nw} {sa.map.width}x{sa.map.height} "
                  f"{SYMMETRY_NAME.get(sa.map.symmetry)}")
            print(f"   sentinel threat {len(sa.sentinel_threat)}  "
                  f"reachable+plantable {len(sa.sent_reach)}  "
                  f"gunner {len(sa.gunner_threat)} (only {len(sa.gunner_only)})")
            print(f"   occupy {sa.occupy_cost} Ti | mincut {len(sa.mincut_tiles)} tiles "
                  f"= {sa.mincut_cost} Ti | pocket {sa.pocket_landing} tiles, "
                  f"{sa.pocket_plantable_threat} still plantable | "
                  f"launcher bypass {sa.launcher_bypass} (min dsq {sa.launcher_min_dsq})")
            print("   cut tiles: " + ", ".join(f"({x},{y})" for x, y in sorted(sa.mincut_tiles)))
            if args.ascii:
                print(render(sa))
            print()
        return

    print("\t".join(COLS))
    for r in rows:
        print("\t".join(str(r.get(c, "")) for c in COLS))


if __name__ == "__main__":
    main()
