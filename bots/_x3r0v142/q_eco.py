"""LOKI-1 economy layer -- PORTED, not redesigned.

This module is the one part of LOKI-1 that is deliberately copied rather than
rebuilt.  thor_r1 shipped a from-scratch offensive bot with no harvesters at
all: zero titanium delivered, 2 wins in 60 games.  The bootstrap below is what
keeps us alive to the round where a kill is attempted at all, so it is lifted
from bots/_v103split (main.py `_expand`, `_link_path`, `_build_next_link`,
`_wire_*`, `_pick`, `_bfs_direction`, `_nav`, `_move`, `_siphon_*`, and the
module-level map/seat helpers) with only these changes:

  * the per-map special cases (hive freeze, snowflake/nordkap/atoll role and
    magazine hacks) are dropped -- they were keyed to one opponent's build on
    one layout and LOKI-1 must not carry an opponent-specific table;
  * the interceptor and the siege planner are gone from `_expand`; the raid
    layer owns forward work now and home defence lives in main.py;
  * `_expand`'s multi-healer convergence is kept, because it is the measured
    answer to "one enemy turret out-damages one healer".

Everything else -- the harvester ceiling, the trunk-chain planner, the pave
trail, the heal-seat reservation, the siphon hygiene -- is behaviour-for-
behaviour the incumbent's.
"""
import math
from collections import deque

from fcode import Direction, EntityType, Environment, Position

from q_doctrine import *  # noqa: F401,F403


# ---------------------------------------------------------------------------
# Module-level geometry / map helpers (ported verbatim).
# ---------------------------------------------------------------------------

def enemy_core_for(w, h, own):
    """The enemy Core anchor, from map symmetry alone.

    GENERIC BY CONSTRUCTION (LOKI-1 constraint 4): CORE_PAIRS is a table of
    map dimensions and Core anchors -- terrain, not opponents -- and the
    fallback is the plain point reflection of our own anchor.  Nothing here
    can go stale when an opponent ships a new version.
    """
    for mw, mh, ax, ay, bx, by in CORE_PAIRS:
        if w != mw or h != mh:
            continue
        if own.x == ax and own.y == ay:
            return Position(bx, by)
        if own.x == bx and own.y == by:
            return Position(ax, ay)
    return Position(max(0, w - 2 - own.x), max(0, h - 2 - own.y))


def known_map_for(w, h, own, ct=None):
    candidates = []
    for (mw, mh, ax, ay, bx, by), code in tuple(MAP_CODES.items()) + EXTRA_MAP_CODES:
        if w != mw or h != mh or (own.x, own.y) not in ((ax, ay), (bx, by)):
            continue
        cells = []
        for ch in code:
            val = MAP_ALPHABET.index(ch)
            for _ in range(3):
                cells.append(val % 3)
                val //= 3
        cells = cells[:w * h]
        candidates.append(tuple(
            "".join(".#o"[cells[y * w + x]] for x in range(w))
            for y in range(h)
        ))
    if not candidates:
        return None
    if len(candidates) == 1 or ct is None:
        return candidates[0]
    sensed = []
    try:
        for tile in ct.get_nearby_tiles():
            env = ct.get_tile_env(tile)
            char = "#" if env == Environment.WALL else ("o" if env == Environment.ORE_TITANIUM else ".")
            sensed.append((tile.x, tile.y, char))
    except Exception:
        return candidates[0]
    return min(candidates, key=lambda grid: sum(grid[y][x] != char for x, y, char in sensed))


def pack_pos(pos):
    return ((pos.x + 1) << 16) | (pos.y + 1)


def unpack_pos(val):
    if not val:
        return None
    return Position((val >> 16) - 1, (val & 0xFFFF) - 1)


def nearest_cardinal(d):
    return {
        Direction.NORTH: Direction.NORTH, Direction.NORTHEAST: Direction.EAST,
        Direction.EAST: Direction.EAST, Direction.SOUTHEAST: Direction.EAST,
        Direction.SOUTH: Direction.SOUTH, Direction.SOUTHWEST: Direction.SOUTH,
        Direction.WEST: Direction.WEST, Direction.NORTHWEST: Direction.WEST,
        Direction.CENTRE: Direction.NORTH,
    }[d]


def ring(origin, r=2):
    out = []
    for dx in range(-r, r + 1):
        for dy in range(-r, r + 1):
            if dx or dy:
                out.append(Position(origin.x + dx, origin.y + dy))
    return out


def core_tiles(o):
    return [o, Position(o.x + 1, o.y), Position(o.x, o.y + 1), Position(o.x + 1, o.y + 1)]


def dist_core(pos, o):
    return min(max(abs(pos.x - c.x), abs(pos.y - c.y)) for c in core_tiles(o))


def nearest_core_tile(pos, o):
    return min(core_tiles(o), key=lambda c: abs(pos.x - c.x) + abs(pos.y - c.y))


def heal_seats(o, mw, mh):
    """The 8 orthogonal neighbours of a 2x2 Core footprint anchored at `o`.

    The only tiles a builder can heal that Core from, and the only tiles a
    conveyor can deliver into it from.  LOKI-1's raid layer uses this same
    function on the ENEMY anchor -- that symmetry is the whole doctrine.
    """
    seats = (
        Position(o.x, o.y - 1), Position(o.x + 1, o.y - 1),
        Position(o.x + 2, o.y), Position(o.x + 2, o.y + 1),
        Position(o.x + 1, o.y + 2), Position(o.x, o.y + 2),
        Position(o.x - 1, o.y + 1), Position(o.x - 1, o.y),
    )
    return [s for s in seats if 0 <= s.x < mw and 0 <= s.y < mh]


def core_corners(o, mw, mh):
    """The 4 diagonal ring tiles of a 2x2 Core footprint anchored at `o`.

    Together with heal_seats these are the 12 spawn tiles (measured, see
    docs/game-model.md).  A builder standing on a corner is orthogonally
    adjacent to exactly the two seats flanking it, and to no Core tile -- so a
    corner is a BUILD station (it can seal two seats) and never a peck station.
    """
    cs = (
        Position(o.x - 1, o.y - 1), Position(o.x + 2, o.y - 1),
        Position(o.x - 1, o.y + 2), Position(o.x + 2, o.y + 2),
    )
    return [c for c in cs if 0 <= c.x < mw and 0 <= c.y < mh]


def delivery_seats(o, mw, mh, walls, ores):
    seats = heal_seats(o, mw, mh)
    if not seats:
        return []
    usable = [s for s in seats if (s.x, s.y) not in walls]
    if not usable:
        usable = seats
    if ores:
        near = sorted(
            ores,
            key=lambda t: (min(abs(t.x - c.x) + abs(t.y - c.y) for c in core_tiles(o)), t.y, t.x),
        )[:HS_ORE_SAMPLE]

        def score(s):
            return sum(abs(s.x - t.x) + abs(s.y - t.y) for t in near)
    else:
        def score(s):
            return abs(2 * s.x - (mw - 1)) + abs(2 * s.y - (mh - 1))

    order = {(s.x, s.y): i for i, s in enumerate(seats)}
    usable.sort(key=lambda s: (score(s), order[(s.x, s.y)]))
    return usable[:HS_DELIVERY_SEATS]


def pave_blocked_by_ore(ct, tile):
    try:
        if not ct.is_in_vision(tile):
            return True
        return ct.get_tile_env(tile) == Environment.ORE_TITANIUM
    except Exception:
        return True


def pave_blocked(ct, tile, banned):
    if banned is not None and (tile.x, tile.y) in banned:
        return True
    return E2B_ORE_PAVE_BAN_ON and pave_blocked_by_ore(ct, tile)


# ---------------------------------------------------------------------------
# The mixin.
# ---------------------------------------------------------------------------

class EcoMixin:

    # --- budget guards -----------------------------------------------------

    def _cpu_exhausted(self, ct):
        """True once this unit has spent CPU_BUDGET_US of its 10 ms turn.

        An overrun truncates run() mid-statement at a boundary the engine
        picks; this lets the file pick one instead.  Reported once per unit
        lifetime to stderr (print() goes to the replay, not the console).
        """
        try:
            if ct.get_cpu_time_elapsed() < CPU_BUDGET_US:
                return False
        except Exception:
            return False
        if not self.reported_cpu:
            self.reported_cpu = True
            import sys
            print(
                f"CPU-GUARD tripped: round={ct.get_current_round()} "
                f"elapsed_us={ct.get_cpu_time_elapsed()}",
                file=sys.stderr,
            )
        return True

    def _eco_spendable(self, ct, cost):
        ti = ct.get_global_resources()
        if (
            SIEGE_RESERVE_ON
            and ct.read_store(SLOT_UNDER) != 0
            and ct.get_current_round() >= HUNT_MIN_RND
        ):
            return ti >= cost + SIEGE_HEAL_RESERVE_TI
        return ti >= cost

    def _eco_cap(self, ct):
        if (
            ct.get_global_resources() >= SURGE_TI_FLOOR
            and ct.get_current_round() >= SURGE_MIN_RND
        ):
            return SURGE_ECO_CAP
        return ECO_CAP

    # --- our own heal seats ------------------------------------------------

    def _seat_ban(self):
        if not HS_SEAT_PROTECT_ON or self.core is None or not (self.mw and self.mh):
            return None
        if self.seat_ban is None:
            keep = delivery_seats(self.core, self.mw, self.mh, self.map_walls, self.map_ores)
            self.seat_keep = keep
            kept = {(s.x, s.y) for s in keep}
            self.seat_ban = frozenset(
                (s.x, s.y) for s in heal_seats(self.core, self.mw, self.mh)
                if (s.x, s.y) not in kept
            )
        return self.seat_ban

    def _pave_ban(self):
        return self._seat_ban() if HS_SEAT_BAN_CONVEYORS else None

    def _free_seats(self, ct):
        out = []
        p = ct.get_position()
        for s in heal_seats(self.core, self.mw, self.mh):
            try:
                if not ct.is_in_vision(s) or not ct.is_tile_passable(s):
                    continue
                if ct.get_tile_builder_bot_id(s) is not None:
                    continue
            except Exception:
                continue
            out.append(s)
        out.sort(key=lambda s: (abs(p.x - s.x) + abs(p.y - s.y), s.y, s.x))
        return out

    def _seat_seek_target(self, ct):
        if not HS_HEAL_DETAIL_ON or self.core is None:
            return None
        free = self._free_seats(ct)
        if not free:
            return None
        seats = {(s.x, s.y) for s in heal_seats(self.core, self.mw, self.mh)}
        me = ct.get_id()
        seekers = 0
        try:
            for uid in ct.get_nearby_units():
                if uid == me or ct.get_team(uid) != self.team:
                    continue
                if ct.get_entity_type(uid) != EntityType.BUILDER_BOT:
                    continue
                up = ct.get_position(uid)
                if (up.x, up.y) in seats:
                    continue
                if self.core.distance_squared(up) <= HS_SEEK_BAND_DSQ:
                    seekers += 1
        except Exception:
            return None
        if seekers >= len(free):
            return None
        p = ct.get_position()
        if (p.x, p.y) in seats:
            return None
        held = self.hs_seek_seat
        if held is not None:
            for s in free:
                if (s.x, s.y) == held:
                    return s
        choice = free[0]
        self.hs_seek_seat = (choice.x, choice.y)
        return choice

    def _heal_core(self, ct):
        for tile in core_tiles(self.core):
            try:
                if ct.can_heal(tile):
                    ct.heal(tile)
                    return True
            except Exception:
                continue
        return False

    def _heal_adjacent(self, ct):
        """Repair a damaged friendly building we are standing next to.

        1 Ti for +4 HP against an enemy peck's 2 Ti for 2 dmg -- eight to one
        on titanium.  can_heal() enforces adjacency, cost and real damage, so
        this is free on a round when nothing is hurt.
        """
        p = ct.get_position()
        for d in CARDINALS:
            t = p.add(d)
            if not (0 <= t.x < self.mw and 0 <= t.y < self.mh):
                continue
            try:
                if ct.can_heal(t):
                    ct.heal(t)
                    return True
            except Exception:
                continue
        return False

    def _core_shelled(self, ct):
        for eid in ct.get_nearby_buildings():
            try:
                if ct.get_entity_type(eid) == EntityType.CORE and ct.get_team(eid) == self.team:
                    return ct.get_hp(eid) < ct.get_max_hp(eid)
            except Exception:
                continue
        return False

    def _live_home_gun(self, ct):
        if self.core is None:
            return False
        tiles = core_tiles(self.core)
        for bid in ct.get_nearby_buildings():
            try:
                if ct.get_team(bid) != self.team:
                    continue
                if ct.get_entity_type(bid) not in (EntityType.GUNNER, EntityType.SENTINEL):
                    continue
                bp = ct.get_position(bid)
                if min(t.distance_squared(bp) for t in tiles) <= HUNT_BAND_DSQ:
                    return True
            except Exception:
                continue
        return False

    def _sync_harvesters(self, ct):
        if self.core is None:
            return
        p = ct.get_position()
        if p.distance_squared(self.core) > 64:
            return
        live = 0
        for eid in ct.get_nearby_buildings():
            try:
                if ct.get_team(eid) == self.team and ct.get_entity_type(eid) == EntityType.HARVESTER:
                    live += 1
            except Exception:
                continue
        if live > ct.read_store(SLOT_HARVESTERS):
            ct.write_store(SLOT_HARVESTERS, live)
        if live >= ECO_NEED:
            ct.write_store(SLOT_ECO_READY, 1)

    # --- trunk chain planning ---------------------------------------------

    def _link_path(self, ct, hpos):
        raw_goals = set()
        for c in core_tiles(self.core):
            for d in CARDINALS:
                t = c.add(d)
                if 0 <= t.x < self.mw and 0 <= t.y < self.mh and dist_core(t, self.core) > 0:
                    raw_goals.add((t.x, t.y))
        ban = self._pave_ban()
        if ban is not None:
            raw_goals -= ban
        start = (hpos.x, hpos.y)
        if start in raw_goals or not raw_goals:
            return []

        if self.map_grid is not None:
            blocked = set(self.map_walls)
            blocked.update((o.x, o.y) for o in self.map_ores if (o.x, o.y) != start)
            for c in core_tiles(self.core):
                blocked.add((c.x, c.y))
            if ban is not None:
                blocked.update(ban)
            try:
                for eid in ct.get_nearby_buildings():
                    ep = ct.get_position(eid)
                    key = (ep.x, ep.y)
                    et = ct.get_entity_type(eid)
                    if key == start:
                        continue
                    if et == EntityType.CORE:
                        blocked.update((c.x, c.y) for c in core_tiles(ep))
                    elif et not in (EntityType.CONVEYOR, EntityType.SPLITTER):
                        blocked.add(key)
                    elif ct.get_team(eid) != self.team:
                        blocked.add(key)
            except Exception:
                pass
            goals = {g for g in raw_goals if g not in blocked}
            parent = {g: None for g in goals}
            q = deque(goals)
            steps = 0
            while q and start not in parent:
                x, y = q.popleft()
                steps += 1
                if steps % 64 == 0 and self._cpu_exhausted(ct):
                    break
                for d in CARDINALS:
                    n = Position(x, y).add(d)
                    key = (n.x, n.y)
                    if (
                        key in parent or key in blocked
                        or not (0 <= n.x < self.mw and 0 <= n.y < self.mh)
                    ):
                        continue
                    parent[key] = (x, y)
                    q.append(key)
            if start not in parent:
                return []
            path = []
            cur = start
            while parent[cur] is not None:
                cur = parent[cur]
                path.append(Position(cur[0], cur[1]))
            return path

        goals = raw_goals
        prev = {start: None}
        q = deque([start])
        found = None
        steps = 0
        while q:
            x, y = q.popleft()
            steps += 1
            if steps % 64 == 0 and self._cpu_exhausted(ct):
                break
            if (x, y) in goals and (x, y) != start:
                found = (x, y)
                break
            for d in CARDINALS:
                n = Position(x, y).add(d)
                key = (n.x, n.y)
                if key in prev or not (0 <= n.x < self.mw and 0 <= n.y < self.mh):
                    continue
                if dist_core(n, self.core) == 0:
                    continue
                if ban is not None and key in ban:
                    continue
                try:
                    if ct.get_tile_env(n) == Environment.WALL:
                        continue
                except Exception:
                    pass
                try:
                    bid = ct.get_tile_building_id(n)
                except Exception:
                    bid = None
                if bid is not None and key not in goals:
                    try:
                        et = ct.get_entity_type(bid)
                        if et not in (EntityType.CONVEYOR, EntityType.SPLITTER, EntityType.HARVESTER):
                            continue
                    except Exception:
                        continue
                prev[key] = (x, y)
                q.append(key)
        if found is None:
            return []
        path, cur = [], found
        while cur is not None and cur != start:
            path.append(Position(cur[0], cur[1]))
            cur = prev[cur]
        path.reverse()
        return path

    def _wire_on_build(self, ct, bp):
        if not self.link_queue:
            self.link_source = bp
            self.link_queue = self._link_path(ct, bp)
            return
        if not SIPHON_WIRE_ON or len(self.wire_pending) >= SIPHON_WIRE_QUEUE:
            return
        self.wire_pending.append((bp, ct.get_current_round()))

    def _has_acceptor(self, ct, bp):
        for d in CARDINALS:
            t = bp.add(d)
            if not (0 <= t.x < self.mw and 0 <= t.y < self.mh):
                continue
            try:
                bid = ct.get_tile_building_id(t)
                if bid is None or ct.get_team(bid) != self.team:
                    continue
                if ct.get_entity_type(bid) in (
                    EntityType.CONVEYOR, EntityType.SPLITTER, EntityType.CORE
                ):
                    return True
            except Exception:
                continue
        return False

    def _wire_tick(self, ct):
        if not SIPHON_WIRE_ON or not self.wire_pending:
            return
        bp, since = self.wire_pending[0]
        if self._has_acceptor(ct, bp):
            self.wire_pending.pop(0)
            return
        if self.link_queue and ct.get_current_round() - since < SIPHON_WIRE_RNDS:
            return
        path = self._link_path(ct, bp)
        self.wire_pending.pop(0)
        if path:
            self.link_source = bp
            self.link_queue = path

    def _build_next_link(self, ct):
        if not self.link_queue or not self._eco_spendable(ct, ct.get_conveyor_cost()):
            return False
        p = ct.get_position()
        while self.link_queue:
            tile = self.link_queue[0]
            if abs(p.x - tile.x) + abs(p.y - tile.y) > 1:
                return False
            try:
                occupied = ct.get_tile_building_id(tile) is not None
            except Exception:
                return False
            if occupied:
                self.link_queue.pop(0)
                continue
            if p.x == tile.x and p.y == tile.y:
                return False
            break
        if not self.link_queue:
            return False
        tile = self.link_queue[0]
        ban = self._pave_ban()
        if ban is not None and (tile.x, tile.y) in ban:
            self.link_queue = []
            return False
        target = nearest_core_tile(tile, self.core)
        if len(self.link_queue) >= 2:
            f = tile.cardinal_direction_to(self.link_queue[1])
            if f == Direction.CENTRE:
                f = nearest_cardinal(tile.direction_to(target))
        else:
            f = nearest_cardinal(tile.direction_to(target))
        if f == Direction.CENTRE:
            f = Direction.NORTH
        if ct.can_build_conveyor(tile, f):
            ct.build_conveyor(tile, f)
            self.link_queue.pop(0)
            return True
        return False

    def _step_off_link(self, ct):
        p = ct.get_position()
        dirs = []
        if len(self.link_queue) >= 2:
            dirs.append(p.cardinal_direction_to(self.link_queue[1]))
        desired = p.cardinal_direction_to(self.core)
        if desired in CARDINALS:
            i = CARDINALS.index(desired)
            dirs.extend((CARDINALS[(i + 1) % 4], CARDINALS[(i - 1) % 4], desired.opposite()))
        dirs.extend(CARDINALS)
        seen = set()
        for d in dirs:
            if d == Direction.CENTRE or d in seen:
                continue
            seen.add(d)
            if ct.can_move(d):
                ct.move(d)
                return True
        return False

    # --- ore selection and navigation --------------------------------------

    def _pick(self, ct):
        # Static role partitions keep four builders off one deposit.  A raider
        # standing down to the economy (raid.py's state-based fallback) is a
        # full expander for this purpose; only the home defender is excluded,
        # so its local scan keeps it near the Core.
        if self.map_ores and self.role != "defend":
            small = self.mw * self.mh <= 220
            workers = 2 if small else 4
            worker = max(0, self.role_n - 1) % workers
            ordered = sorted(
                self.map_ores,
                key=lambda t: (
                    abs(t.x - self.core.x) + abs(t.y - self.core.y),
                    (t.x * 17 + t.y * 31 + worker * 7) % 97,
                ),
            )
            assigned = ordered[worker::workers] or ordered
            for _ in range(len(assigned)):
                t = assigned[self.ore_cursor % len(assigned)]
                self.ore_cursor += 1
                try:
                    if ct.is_in_vision(t) and ct.get_tile_building_id(t) is not None:
                        continue
                except Exception:
                    pass
                return t

        try:
            ores = [t for t in ct.get_nearby_tiles()
                    if ct.get_tile_env(t) == Environment.ORE_TITANIUM
                    and ct.get_tile_building_id(t) is None]
        except Exception:
            ores = []
        if ores:
            return min(ores, key=lambda t: dist_core(t, self.core))
        r = 3 + (ct.get_current_round() // 30) + (self.idx % 5)
        self.ang = (self.ang + 0.65) % (2 * math.pi)
        return Position(
            max(0, min(self.core.x + int(r * math.cos(self.ang)), self.mw - 1)),
            max(0, min(self.core.y + int(r * math.sin(self.ang)), self.mh - 1)),
        )

    def _bfs_direction(self, ct, target):
        """One exact static-terrain step toward target, visible units avoided."""
        p = ct.get_position()
        if self.map_grid is None:
            return p.cardinal_direction_to(target)

        blocked = set(self.map_walls)
        if self.core is not None:
            blocked.update((c.x, c.y) for c in core_tiles(self.core))
        if self.enemy is not None:
            blocked.update((c.x, c.y) for c in core_tiles(self.enemy))
        try:
            me = ct.get_id()
            for eid in ct.get_nearby_entities():
                if eid == me:
                    continue
                et = ct.get_entity_type(eid)
                ep = ct.get_position(eid)
                if et == EntityType.CORE:
                    blocked.update((c.x, c.y) for c in core_tiles(ep))
                elif et in (
                    EntityType.GUNNER, EntityType.SENTINEL, EntityType.LAUNCHER,
                    EntityType.HARVESTER, EntityType.BARRIER,
                ):
                    blocked.add((ep.x, ep.y))
        except Exception:
            pass
        start = (p.x, p.y)
        blocked.discard(start)

        tkey = (target.x, target.y)
        if tkey not in blocked:
            goals = {tkey}
        elif target == self.core or target == self.enemy:
            goals = set()
            for c in core_tiles(target):
                for d in CARDINALS:
                    qpos = c.add(d)
                    key = (qpos.x, qpos.y)
                    if (
                        0 <= qpos.x < self.mw and 0 <= qpos.y < self.mh
                        and dist_core(qpos, target) > 0 and key not in blocked
                    ):
                        goals.add(key)
        else:
            goals = {
                (qpos.x, qpos.y)
                for d in CARDINALS for qpos in (target.add(d),)
                if 0 <= qpos.x < self.mw and 0 <= qpos.y < self.mh
                and (qpos.x, qpos.y) not in blocked
            }
        if start in goals:
            return Direction.CENTRE
        if not goals:
            return p.cardinal_direction_to(target)

        desired = p.cardinal_direction_to(target)
        if desired in CARDINALS:
            i = CARDINALS.index(desired)
            side = 1 if (self.idx & 1) else -1
            order = [
                desired, CARDINALS[(i + side) % 4],
                CARDINALS[(i - side) % 4], desired.opposite(),
            ]
        else:
            order = CARDINALS
        seen = {start}
        q = deque([(p.x, p.y, Direction.CENTRE)])
        steps = 0
        while q:
            x, y, first = q.popleft()
            steps += 1
            if steps % 64 == 0 and self._cpu_exhausted(ct):
                return p.cardinal_direction_to(target)
            for d in order:
                n = Position(x, y).add(d)
                key = (n.x, n.y)
                if (
                    key in seen or key in blocked
                    or not (0 <= n.x < self.mw and 0 <= n.y < self.mh)
                ):
                    continue
                first_step = d if first == Direction.CENTRE else first
                if key in goals:
                    return first_step
                seen.add(key)
                q.append((n.x, n.y, first_step))
        return p.cardinal_direction_to(target)

    def _nav(self, ct, pave=True):
        if self.tgt is None or ct.get_move_cooldown() != 0:
            return
        desired = self._bfs_direction(ct, self.tgt)
        if desired == Direction.CENTRE:
            return
        if self._move(ct, desired, pave):
            return
        idx = CARDINALS.index(desired) if desired in CARDINALS else 0
        for d in (CARDINALS[(idx + 1) % 4], CARDINALS[(idx + 3) % 4], desired.opposite()):
            if self._move(ct, d, pave):
                return
        self.stuck += 1

    def _move(self, ct, d, pave=True):
        if d == Direction.CENTRE:
            return False
        p0 = ct.get_position()
        nxt = p0.add(d)
        if not (0 <= nxt.x < self.mw and 0 <= nxt.y < self.mh):
            return False
        if PAVE_TRAIL_ON:
            pp = self.pave_prev
            if pp is not None and self.pave_rnd != ct.get_current_round() - 1:
                pp = None
            # A Launcher throw can teleport this builder between turns, which
            # puts pave_prev outside vision and makes is_tile_empty raise.
            # The guard skips the pave, never the move.
            try:
                readable = (
                    pave and self.core and pp is not None
                    and ct.get_action_cooldown() == 0
                    and ct.is_in_vision(pp) and ct.is_tile_empty(pp)
                )
            except Exception:
                readable = False
            if readable:
                ore_ban = pave_blocked(ct, pp, self._pave_ban())
                if not ore_ban and ct.read_store(SLOT_HARVESTERS) >= 1 \
                        and self._eco_spendable(ct, ct.get_conveyor_cost()):
                    if dist_core(pp, self.core) > 0:
                        if dist_core(pp, self.core) == 1:
                            facing = nearest_cardinal(
                                pp.direction_to(nearest_core_tile(pp, self.core)))
                            coreward_ok = True
                        else:
                            facing = self.pave_dir
                            coreward_ok = (
                                abs(p0.x - self.core.x) + abs(p0.y - self.core.y)
                                < abs(pp.x - self.core.x) + abs(pp.y - self.core.y)
                            )
                        try:
                            if coreward_ok and facing is not None \
                                    and ct.can_build_conveyor(pp, facing):
                                ct.build_conveyor(pp, facing)
                        except Exception:
                            pass
        if ct.can_move(d):
            ct.move(d)
            if PAVE_TRAIL_ON:
                self.pave_prev = p0
                self.pave_dir = d
                self.pave_rnd = ct.get_current_round()
            return True
        return False

    # --- siphon hygiene ----------------------------------------------------

    def _siphon_clear(self):
        self.siphon_id = None
        self.siphon_pos = None
        self.siphon_hp = None
        self.tgt = None
        self.stuck = 0
        self.wall = None

    def _siphon_taken(self, ct, bpos, me):
        for d in CARDINALS:
            n = bpos.add(d)
            if not (0 <= n.x < self.mw and 0 <= n.y < self.mh):
                continue
            try:
                oid = ct.get_tile_builder_bot_id(n)
                if oid is not None and oid != me and ct.get_team(oid) == self.team:
                    return True
            except Exception:
                continue
        return False

    def _find_siphon(self, ct):
        """Nearest enemy belt tile orthogonally touching one of OUR harvesters.

        The harvester round-robin is TEAM-BLIND (measured): an enemy conveyor
        beside our harvester is a full-rank acceptor, so it takes half of that
        harvester's output forever.  Removing the belt is the only full stop.
        """
        p = ct.get_position()
        rnd = ct.get_current_round()
        harv = []
        belts = []
        try:
            ids = ct.get_nearby_buildings()
        except Exception:
            return None
        for bid in ids:
            try:
                et = ct.get_entity_type(bid)
                mine = ct.get_team(bid) == self.team
            except Exception:
                continue
            if mine:
                if et == EntityType.HARVESTER:
                    harv.append(ct.get_position(bid))
            elif et in (EntityType.CONVEYOR, EntityType.SPLITTER):
                belts.append((bid, ct.get_position(bid)))
        if not harv or not belts:
            return None
        me = ct.get_id()
        best, best_k = None, None
        for bid, bpos in belts:
            if self.siphon_ban.get((bpos.x, bpos.y), 0) > rnd:
                continue
            if not any(abs(bpos.x - h.x) + abs(bpos.y - h.y) == 1 for h in harv):
                continue
            if self._siphon_taken(ct, bpos, me):
                continue
            k = (p.distance_squared(bpos), bid)
            if best_k is None or k < best_k:
                best, best_k = (bid, bpos), k
        return best

    def _siphon_deny(self, ct):
        if not SIPHON_DENY_ON or self.core is None:
            return False
        if ct.get_global_resources() < SIPHON_FIRE_TI:
            if self.siphon_pos is not None:
                self._siphon_clear()
            return False
        rnd = ct.get_current_round()
        p = ct.get_position()

        hp = ct.get_hp()
        if self.siphon_pos is not None and self.siphon_hp is not None and hp < self.siphon_hp:
            self.siphon_ban[(self.siphon_pos.x, self.siphon_pos.y)] = rnd + SIPHON_BAN_RNDS
            self._siphon_clear()
            return False

        tgt = self.siphon_pos
        if tgt is not None:
            dead = False
            try:
                if ct.is_in_vision(tgt):
                    bid = ct.get_tile_building_id(tgt)
                    dead = bid is None or ct.get_team(bid) == self.team
            except Exception:
                dead = False
            if dead:
                self._siphon_clear()
                tgt = None
            elif rnd - self.siphon_since > SIPHON_MAX_RNDS:
                self.siphon_ban[(tgt.x, tgt.y)] = rnd + SIPHON_BAN_RNDS
                self._siphon_clear()
                tgt = None
        if tgt is None:
            if (rnd + self.idx) % SIPHON_SCAN_EVERY:
                return False
            found = self._find_siphon(ct)
            if found is None:
                return False
            self.siphon_id, self.siphon_pos = found
            self.siphon_since = rnd
            tgt = self.siphon_pos
        self.siphon_hp = hp

        d = abs(p.x - tgt.x) + abs(p.y - tgt.y)
        if d == 1:
            if LOKI_QUIET_ON:
                return False          # QUIET: siphon melee silenced
            if ct.get_action_cooldown() == 0 and ct.can_fire(tgt):
                ct.fire(tgt)
            return True
        if ct.get_move_cooldown() != 0:
            return True
        if d == 0:
            for step in CARDINALS:
                if ct.can_move(step):
                    ct.move(step)
                    return True
            return True
        self.tgt = tgt
        self._nav(ct, pave=False)
        return True

    # --- the expander ------------------------------------------------------

    def _expand(self, ct):
        p = ct.get_position()
        has_launch = ct.read_store(SLOT_LAUNCHER) != 0
        harv = ct.read_store(SLOT_HARVESTERS)
        allow_pave = has_launch or harv >= 2
        endgame = ENDGAME_SWITCH_ON and ct.get_current_round() >= ENDGAME_RND

        if ct.get_action_cooldown() == 0:
            if not endgame and self.link_queue and self._build_next_link(ct):
                return
            if (
                ct.get_global_resources() >= ct.get_harvester_cost()
                if endgame
                else (
                    self._eco_spendable(ct, ct.get_harvester_cost())
                    and harv < self._eco_cap(ct)
                )
            ):
                seat_ban = self._seat_ban()
                for d in DIRECTIONS:
                    bp = p.add(d)
                    if seat_ban is not None and (bp.x, bp.y) in seat_ban:
                        continue
                    if not (0 <= bp.x < self.mw and 0 <= bp.y < self.mh):
                        continue
                    try:
                        ok = ct.can_build_harvester(bp)
                    except Exception:
                        continue
                    if ok:
                        ct.build_harvester(bp)
                        ct.write_store(SLOT_HARVESTERS, ct.read_store(SLOT_HARVESTERS) + 1)
                        if ct.read_store(SLOT_HARVESTERS) >= ECO_NEED:
                            ct.write_store(SLOT_ECO_READY, 1)
                        self._wire_on_build(ct, bp)
                        break
            # CHAIN MEDIC.  ~70% of damage to our economy was enemy builder
            # melee, and every cleared tile was relaid at 3 Ti plus +1% team
            # cost scale per relay.  Healing costs no scale at all.
            rnd_now = ct.get_current_round()
            medic_late = rnd_now >= MEDIC_MIN_RND
            if not endgame and ct.get_global_resources() >= MEDIC_TI_FLOOR and (
                medic_late
                or (MEDIC_EARLY_ON and rnd_now >= MEDIC_EARLY_MIN_RND)
            ):
                for d in CARDINALS:
                    bp = p.add(d)
                    if not (0 <= bp.x < self.mw and 0 <= bp.y < self.mh):
                        continue
                    try:
                        bid = ct.get_tile_building_id(bp)
                        if (
                            bid is not None
                            and ct.get_team(bid) == self.team
                            and ct.get_entity_type(bid) in MEDIC_TYPES
                            and ct.get_hp(bid) <= ct.get_max_hp(bid) - (
                                1 if medic_late else MEDIC_EARLY_MIN_DMG
                            )
                            and ct.can_heal(bp)
                        ):
                            ct.heal(bp)
                            return
                    except Exception:
                        continue

        if self._cpu_exhausted(ct):
            return

        # MULTI-HEALER CONVERGENCE.  One enemy Sentinel is ~-9 HP/round on our
        # Core against one healer's +4; two or three converged healers flip the
        # sign.  Proximity-bounded by construction -- _core_shelled only
        # answers True while the Core is inside this builder's own vision.
        if self.role_n >= 2 and ct.read_store(SLOT_UNDER) != 0 and self._core_shelled(ct):
            self.converging = True
            if ct.get_move_cooldown() == 0 and not any(
                abs(p.x - c.x) + abs(p.y - c.y) == 1 for c in core_tiles(self.core)
            ):
                seat = self._seat_seek_target(ct)
                self.tgt = self.core if seat is None else seat
                self._nav(ct, pave=False)
            return
        if self.converging:
            self.converging = False
            self.tgt = None
            self.stuck = 0
            self.wall = None

        if self._siphon_deny(ct):
            return

        if ct.get_move_cooldown() != 0:
            return
        # ORE STEP-OFF: builds are adjacent-only and never own-tile, so a
        # builder parked ON ore is the one unit that can never mine it.
        try:
            on_ore = ct.get_tile_env(p) == Environment.ORE_TITANIUM
        except Exception:
            on_ore = False
        if len(self.map_walls) >= ORE_STEPOFF_MIN_WALLS and on_ore:
            for d in CARDINALS:
                n = p.add(d)
                if not (0 <= n.x < self.mw and 0 <= n.y < self.mh):
                    continue
                try:
                    ok = (
                        ct.get_tile_env(n) != Environment.ORE_TITANIUM
                        and ct.is_tile_passable(n) and ct.can_move(d)
                    )
                except Exception:
                    continue
                if ok:
                    ct.move(d)
                    self.tgt = None
                    self.stuck = 0
                    return
        if self.link_queue:
            nxt = self.link_queue[0]
            if p.x == nxt.x and p.y == nxt.y:
                self._step_off_link(ct)
            elif abs(p.x - nxt.x) + abs(p.y - nxt.y) == 1:
                return
            else:
                self.tgt = nxt
                self._nav(ct, pave=False)
            return
        if self.tgt is None or p == self.tgt or self.stuck >= 5:
            self.tgt = self._pick(ct)
            self.stuck = 0
            self.wall = None
        if self.tgt is None:
            return
        for d in DIRECTIONS:
            bp = p.add(d)
            if 0 <= bp.x < self.mw and 0 <= bp.y < self.mh:
                try:
                    if ct.get_tile_env(bp) == Environment.ORE_TITANIUM \
                            and ct.get_tile_building_id(bp) is None:
                        self.tgt = bp
                        break
                except Exception:
                    continue
        self._nav(ct, pave=allow_pave)
