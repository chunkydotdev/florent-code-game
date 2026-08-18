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
    answer to "one enemy turret out-damages one healer";
  * LOKI-L4 adds `_l4_repair` and one call site inside `_expand` -- the first
    thing on this line that deliberately reconnects a severed trunk instead of
    waiting for a builder to walk past one.

Everything else -- the harvester ceiling, the trunk-chain planner, the pave
trail, the heal-seat reservation, the siphon hygiene -- is behaviour-for-
behaviour the incumbent's.

LOKI-TURBO (2026-08-15) -- CPU ONLY, NO DOCTRINE.  Nothing in this file decides
anything it did not decide before.  loki_analysis.md 5.2 measured
`_bfs_direction` at 3.48-5.73 ms and `_link_path` at 3.94 ms per call on the
30x30 pool maps, against a 10 ms per-unit server budget, and the ladder
telemetry showed 1,102 builder TLEs in 212 rounds on midgard (61% of builder
turns) -- i.e. the navigation call the whole raid depends on was being
truncated, which is the "we never arrive" symptom.  The dominant term was
`Position.add`: it rebuilds a nine-entry dict inside `Direction.delta()` on
every call and costs 1.35 us against 0.08 us for the same integer arithmetic.

The rewrite is mechanical and is verified, not argued:
  * both floods run over a PADDED FLAT BYTE GRID (see `_flat_template`);
  * every per-round set rebuild (`set(self.map_walls)`, the ore set, the Core
    footprints, the trunk-chain goal ring, the ore partition) is cached on the
    instance and keyed on what it actually depends on;
  * `Position` objects are built only where the engine API takes one.
`tools/turbo_identity.py` calls the old and the new `_bfs_direction` and
`_link_path` side by side over the 15 pool maps with randomised starts, goals,
blocked sets and unit scatter, and asserts identical return values.
"""
import math
from collections import deque

from fcode import Direction, EntityType, Environment, Position

from doctrine import *  # noqa: F401,F403

# Entity types the navigation flood treats as impassable (LOKI had this tuple
# inline in `_bfs_direction`; a frozenset tests the same membership).
BFS_BLOCKING_TYPES = frozenset((
    EntityType.GUNNER, EntityType.SENTINEL, EntityType.LAUNCHER,
    EntityType.HARVESTER, EntityType.BARRIER,
))
# Types a trunk chain may route THROUGH when they are ours (`_link_path`).
BELT_TYPES = frozenset((EntityType.CONVEYOR, EntityType.SPLITTER))
TURRET_TYPES = frozenset((EntityType.GUNNER, EntityType.SENTINEL))
# Anything our own that will take a stack off a harvester (`_has_acceptor`).
ACCEPTOR_TYPES = frozenset((
    EntityType.CONVEYOR, EntityType.SPLITTER, EntityType.CORE,
))
LINK_ROUTABLE_TYPES = frozenset((
    EntityType.CONVEYOR, EntityType.SPLITTER, EntityType.HARVESTER,
))
# Hard cap on nodes one `_link_path` flood may expand.  Cannot fire on a map
# whose passable area is under this; see NAV_NODE_BUDGET in doctrine.py.
LINK_NODE_BUDGET = NAV_NODE_BUDGET


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



# LOKI-TURBO.  The base-27 map decode ran `MAP_ALPHABET.index(ch)` (a linear
# scan of a 27-character string) once per character and then rebuilt every row
# cell-by-cell in a Python genexp -- 900 cells per candidate grid, on the FIRST
# TURN OF EVERY UNIT, which is exactly where loki_analysis.md 5.2 saw the
# first-turn spike.  Each code character expands to a fixed 3-character run, so
# the expansion is a dict lookup and one str.join; the finished grid is then
# memoised, because up to eleven builders decode the same map in one match.
_CHAR3 = {
    ch: (".#o"[i % 3] + ".#o"[(i // 3) % 3] + ".#o"[(i // 9) % 3])
    for i, ch in enumerate(MAP_ALPHABET)
}
_GRID_CACHE = {}


def _decode_grid(code, w, h):
    key = (code, w, h)
    grid = _GRID_CACHE.get(key)
    if grid is None:
        flat = "".join([_CHAR3[ch] for ch in code])[:w * h]
        grid = tuple(flat[y * w:(y + 1) * w] for y in range(h))
        _GRID_CACHE[key] = grid
    return grid


def known_map_for(w, h, own, ct=None):
    candidates = []
    for (mw, mh, ax, ay, bx, by), code in tuple(MAP_CODES.items()) + EXTRA_MAP_CODES:
        if w != mw or h != mh or (own.x, own.y) not in ((ax, ay), (bx, by)):
            continue
        candidates.append(_decode_grid(code, w, h))
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


def cardinal_from_delta(dx, dy):
    """The cardinal whose delta is exactly (dx, dy), or None.

    PLANK SPLIT needs the inverse of `DELTA`, not the nearest-cardinal rounding
    of `nearest_cardinal`: a splitter accepts input ONLY from the tile directly
    behind it, so a facing that is merely close is a splitter that accepts
    nothing at all.
    """
    for i in (0, 1, 2, 3):
        cdx, cdy = CARD_DELTAS[i]
        if cdx == dx and cdy == dy:
            return CARDINALS[i]
    return None


def ring(origin, r=2):
    out = []
    for dx in range(-r, r + 1):
        for dy in range(-r, r + 1):
            if dx or dy:
                out.append(Position(origin.x + dx, origin.y + dy))
    return out


def core_tiles(o):
    return [o, Position(o.x + 1, o.y), Position(o.x, o.y + 1), Position(o.x + 1, o.y + 1)]


def adjacent_to_core(p, o):
    """LOKI's `any(|dx|+|dy| == 1 for c in core_tiles(o))`, without the list.

    Deliberately NOT `min(...) == 1`: a point standing on a footprint tile is
    Manhattan-1 from two of the other three, so the two predicates differ there
    and this one reproduces LOKI's.
    """
    ox, oy = o.x, o.y
    px, py = p.x, p.y
    for cx, cy in ((ox, oy), (ox + 1, oy), (ox, oy + 1), (ox + 1, oy + 1)):
        dx = px - cx
        if dx < 0:
            dx = -dx
        dy = py - cy
        if dy < 0:
            dy = -dy
        if dx + dy == 1:
            return True
    return False


def core_tiles_xy(o):
    """The same four tiles as raw (x, y) pairs -- for set/grid work only.

    LOKI-TURBO: `core_tiles` allocates four Position objects and every caller
    that only wanted coordinates paid for them; `_bfs_direction` alone built
    eight per call before it started.
    """
    ox, oy = o.x, o.y
    return ((ox, oy), (ox + 1, oy), (ox, oy + 1), (ox + 1, oy + 1))


def dist_core(pos, o):
    """Chebyshev distance from `pos` to the 2x2 Core footprint anchored at `o`.

    LOKI-TURBO: closed form, identical for every integer input.  The Chebyshev
    metric is a max-norm and the footprint is a product of two 2-long integer
    intervals, so clamping each coordinate into its interval lands on one of
    the four corners and reproduces `min(... for c in core_tiles(o))` exactly.
    """
    ox, oy = o.x, o.y
    dx = pos.x - ox
    if dx < 0:
        dx = -dx
    elif dx > 1:
        dx -= 1
    else:
        dx = 0
    dy = pos.y - oy
    if dy < 0:
        dy = -dy
    elif dy > 1:
        dy -= 1
    else:
        dy = 0
    return dx if dx > dy else dy


def dsq_core(pos, o):
    """min(pos.distance_squared(c) for c in core_tiles(o)), without the list.

    Squared Euclidean distance is separable, so the minimum over the four
    corners is (min over x) + (min over y) -- exact, not an approximation.
    """
    ox, oy = o.x, o.y
    dx = pos.x - ox
    if dx < 0:
        dx = -dx
    elif dx > 1:
        dx -= 1
    else:
        dx = 0
    dy = pos.y - oy
    if dy < 0:
        dy = -dy
    elif dy > 1:
        dy -= 1
    else:
        dy = 0
    return dx * dx + dy * dy


def sge_centre_q4(pos, o):
    """PLANK P3 SIEGE.  4 x squared Euclidean distance to the Core CENTRE.

    `dsq_core` measures to the nearest FOOTPRINT TILE; the sentinel-geometry
    corpus (top5_pipeline.md (d)) measures every distance to the 2x2 CENTRE,
    which is (o.x + 0.5, o.y + 0.5) and therefore half-integral.  Doubling both
    coordinates clears the halves and keeps the whole comparison in exact
    integers:  4*d^2 = (2*(x-ox) - 1)^2 + (2*(y-oy) - 1)^2.

    Both terms are odd squares, so the result is always == 2 (mod 8) and the
    band bounds SIEGE_BAND_MIN_Q4 / SIEGE_BAND_MAX_Q4 can be integers with no
    rounding question anywhere.  Pure arithmetic: no Position allocation, no
    float, callable on any tile whether or not it is in vision.
    """
    dx = 2 * (pos.x - o.x) - 1
    dy = 2 * (pos.y - o.y) - 1
    return dx * dx + dy * dy


def nearest_core_tile(pos, o):
    """The footprint tile with the least Manhattan distance to `pos`.

    LOKI-TURBO: clamping.  Manhattan is separable and each interval holds two
    consecutive integers, so the minimum is unique (a tie would need pos.x to
    sit half-way between ox and ox+1) and clamping picks the same tile
    `min(core_tiles(o), key=...)` picked.
    """
    ox, oy = o.x, o.y
    cx = ox if pos.x <= ox else (ox + 1 if pos.x >= ox + 1 else pos.x)
    cy = oy if pos.y <= oy else (oy + 1 if pos.y >= oy + 1 else pos.y)
    return Position(cx, cy)


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


# PLANK SOCKET-GUARD.  The eight sockets as raw deltas off the Core anchor, in
# EXACTLY `heal_seats`' order -- that order is the wire format of the Core's
# 4-bit rebuild request (slot 9 bits 28-31), so it may never be permuted.  The
# deltas are used rather than `heal_seats` itself because the request has to be
# encodable and decodable by a unit that cannot see the map edges: `heal_seats`
# DROPS off-map tiles and would shift every index behind the one it dropped.
SG_SOCKET_DELTAS = ((0, -1), (1, -1), (2, 0), (2, 1),
                    (1, 2), (0, 2), (-1, 1), (-1, 0))
# Which FACE of the 2x2 each socket sits on: 0 = -y, 1 = +x, 2 = +y, 3 = -x.
# Two sockets per face.  "Different faces" is the whole point of arm 1: the two
# sockets of one face are orthogonally adjacent to each other, so one enemy
# body standing between them can brick both without moving.
SG_SOCKET_FACE = (0, 0, 1, 1, 2, 2, 3, 3)


def sg_socket(o, i):
    """Socket `i` of the Core anchored at `o`.  No bounds test -- callers that
    can act on the tile test it with the engine's own can_build_*."""
    dx, dy = SG_SOCKET_DELTAS[i]
    return Position(o.x + dx, o.y + dy)


def sg_socket_index(o, x, y):
    """The index of (x, y) in the eight-socket order, or -1."""
    dx, dy = x - o.x, y - o.y
    i = 0
    for sx, sy in SG_SOCKET_DELTAS:
        if sx == dx and sy == dy:
            return i
        i += 1
    return -1


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
    if not (SG_ON and SG_TWO_FEEDERS) or HS_DELIVERY_SEATS < 2:
        return usable[:HS_DELIVERY_SEATS]
    # PLANK SOCKET-GUARD arm 1.  The reserved delivery seats are what
    # `_seat_ban` keeps our OWN harvesters and turrets off; leap6 reserved the
    # two best-scoring seats, and on most maps the two best are the two on the
    # face nearest the ore -- one body standing between them bricks both.
    # Reserve one per FACE instead, best-scoring face first, then top up in the
    # original order if the map has fewer usable faces than seats.  A pure
    # PREFERENCE: the same seats are still candidates and the count is
    # unchanged, so nothing downstream sees a different-sized list.
    out, faces, taken = [], set(), set()
    for s in usable:
        f = SG_SOCKET_FACE[sg_socket_index(o, s.x, s.y)]
        if f in faces:
            continue
        faces.add(f)
        taken.add((s.x, s.y))
        out.append(s)
        if len(out) >= HS_DELIVERY_SEATS:
            return out
    for s in usable:
        if (s.x, s.y) in taken:
            continue
        out.append(s)
        if len(out) >= HS_DELIVERY_SEATS:
            break
    return out


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

    # --- WAVE 22 ARM A5: the titanium-tiebreak endgame ----------------------
    # Spec, evidence and every constant: the WAVE 22 TRACK 2 block at the end
    # of doctrine.py.  Four helpers, all of which return their typed empty
    # value before reading anything when `END_ON` is False, so the OFF twin
    # never executes a line of this.

    def _end_tick(self, ct, rnd):
        """Maintain THIS unit's stall clock.  Two store reads, from r400 on.

        The clock counts consecutive rounds in which the published enemy-Core
        HP band was NOT `SIEGE_HP_LOW` -- i.e. rounds in which nobody on the
        team could see their Core below `SIEGE_MASS3_HP`.  UNKNOWN counts as a
        stall round on purpose: a band nobody has ever published is a Core
        nobody has ever had eyes on, which is not a siege in progress.

        Every unit keeps its own copy so that the arm still works if the Core's
        published bit is ever unavailable (doctrine section 3, risk R4).  A
        body that spawned after `END_ARM_RND` reaches the threshold LATER than
        the Core does, never earlier, so the fallback can only ever be
        conservative.
        """
        if not END_ON or self.end_fired or rnd < END_ARM_RND:
            return
        if self.end_tick_rnd == rnd:
            return
        self.end_tick_rnd = rnd
        if not self.end_armed:
            self.end_armed = True
            if END_LOG:
                print("END arm r=%d" % rnd)
        band = SIEGE_HP_UNKNOWN
        try:
            band = self._sge_band_read(ct)
        except Exception:
            band = SIEGE_HP_UNKNOWN
        if band == SIEGE_HP_LOW:
            self.end_run = 0
            self.end_low_rnd = rnd
        else:
            self.end_run += 1

    def _end_fired(self, ct):
        """Has the endgame fired for this unit?  Latched, memoised per round.

        The authority is the Core's published bit (slot 9 bit 28); this unit's
        own stall clock is the fallback.  Either latches `self.end_fired`, and
        nothing ever clears it -- tiebreak.md 9 rule 2: quit the siege
        "completely and permanently".
        """
        if not END_ON:
            return False
        if self.end_fired:
            return True
        try:
            rnd = ct.get_current_round()
        except Exception:
            return False
        if self._end_rnd == rnd:
            return self._end_val
        self._end_rnd = rnd
        self._end_val = False
        if rnd < END_FIRE_RND:
            return False
        fired = False
        if not SG_ON:
            try:
                fired = bool(ct.read_store(SLOT_HEAL_BUDGET) & END_BIT)
            except Exception:
                fired = False
        if not fired and self.end_run >= END_STALL_RNDS:
            fired = True
        if fired:
            self.end_fired = True
            self.end_rnd = rnd
            if END_LOG:
                print("END fire r=%d run=%d low=%d"
                      % (rnd, self.end_run, self.end_low_rnd))
        self._end_val = fired
        return fired

    def _end_eco_floor(self, ct):
        """Titanium the endgame keeps back for DELIVERY before any magazine.

        One harvester and its first `END_ECO_RESERVE_CONV` conveyors, priced
        live off the engine so the global cost scale is included.  0 on any
        failure, which is the incumbent's floor exactly.
        """
        if not END_ON:
            return 0
        try:
            return (ct.get_harvester_cost()
                    + END_ECO_RESERVE_CONV * ct.get_conveyor_cost())
        except Exception:
            return 0

    def _end_come_home(self, ct, rnd):
        """ARM 1's walk.  True = this body's turn is spent walking home.

        False means "act as an expander now" -- either because the body is
        already inside `END_HOME_DSQ` (in which case the role is flipped here,
        once, permanently) or because the walk has run past `END_RECALL_MAX`
        and the body converts where it stands.
        """
        if not (END_ON and END_QUIT_ON) or self.core is None:
            return False
        try:
            p = ct.get_position()
            d = dsq_core(p, self.core)
        except Exception:
            return False
        if d <= END_HOME_DSQ:
            if self.role == "raid":
                self.role = "expand"
                self.tgt = None
                self.stuck = 0
                self.wall = None
                if END_LOG:
                    print("END home r=%d (%d,%d)" % (rnd, p.x, p.y))
            return False
        if self.end_recall_rnd < 0:
            # First round of the recall: drop every scrap of raid state, or
            # `_nav` steers on a station three tiles from THEIR Core.
            self.end_recall_rnd = rnd
            self.raid_station = None
            self.tgt = None
            self.stuck = 0
            self.wall = None
            self.pave_prev = None
            self.pave_dir = None
            if END_LOG:
                print("END quit r=%d d2=%d" % (rnd, d))
        elif (rnd - self.end_recall_rnd >= END_RECALL_MAX
                or self.stuck >= END_STUCK_MAX):
            # BOXED IN IS NOT SLOW, IT IS STUCK, and the two deserve different
            # patience.  MEASURED on nordkap/seed 204: a body sat at (9,17)
            # with `get_move_cooldown() == 0` and a valid BFS step NORTH for
            # eighty consecutive rounds -- every one of the four `_move`
            # candidates refused, i.e. the body was walled in by buildings.
            # `self.stuck` is `_builder`'s own "my position did not change"
            # counter and it resets on any successful step, so it separates
            # "walking" from "walled in" for free.  Converting the body 68
            # rounds earlier gives those rounds back to the repair and heal
            # arms, which a boxed builder can still reach.
            self.role = "expand"
            self.tgt = None
            self.stuck = 0
            if END_LOG:
                print("END strand r=%d d2=%d" % (rnd, d))
            return False
        try:
            if ct.get_move_cooldown() != 0:
                return True
        except Exception:
            return True
        self.tgt = self.core
        self._nav(ct, pave=False)
        return True

    # --- our own heal seats ------------------------------------------------

    def _seat_ban(self):
        # WAVE 22, ARM A1.  OPENING.md 4.3 rule 1: never a HARVESTER and never
        # a TURRET on one of our own sockets -- both are impassable (engine
        # G), so a socket carrying one is no longer a heal seat and no longer
        # a delivery terminus, and 0 of the corpus's 2 332 own-socket core
        # heals came from a body standing on one.  The parent already bans our
        # harvesters from every non-delivery seat; under the opening the ban is
        # simply ALL EIGHT, because the two the opening wants are conveyors it
        # lays itself and the other six are heal seats we keep open.
        if OPEN_ON and self.core is not None and self.mw and self.mh:
            if self.op_seat_ban is None:
                # `seat_keep` keeps its meaning -- the RESERVED delivery seats,
                # read by `_sg_keep_idx` -- and under the opening those are
                # exactly the two prefill sockets, which is what the trunk
                # planner is already aiming at.  Falls back to the parent's
                # choice until the r0 geometry has resolved.
                keep = []
                g = self.op_geom
                if g is not None:
                    for e in (g["e1"], g["e2"]):
                        if e is not None:
                            keep.append(e["sock"])
                if not keep:
                    keep = delivery_seats(self.core, self.mw, self.mh,
                                          self.map_walls, self.map_ores)
                    self.seat_keep = keep
                    return frozenset(
                        (s.x, s.y) for s in heal_seats(self.core, self.mw, self.mh)
                        if (s.x, s.y) not in {(k.x, k.y) for k in keep})
                self.seat_keep = keep
                self.op_seat_ban = frozenset(
                    (s.x, s.y) for s in heal_seats(self.core, self.mw, self.mh))
            return self.op_seat_ban
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
            # WAVE 22, ARM A1.  OPENING.md 4.3 rule 3: bodies are FORBIDDEN on
            # EMPTY sockets -- a body there blocks our own feeder build, which
            # is the wave-20 M3 defect (106-233 own body-turns on own sockets
            # per zero-collection game).  Only the two PREFILL sockets are
            # withheld, and only until our conveyor stands on them.
            if OPEN_ON and (s.x, s.y) in self._op_empty_socket_keys(ct):
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
        px, py = p.x, p.y
        for dx, dy in CARD_DELTAS:
            tx, ty = px + dx, py + dy
            if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                continue
            t = Position(tx, ty)
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
        # T4 BLEED BEACON.  A builder's vision is r^2 = 20 and the economy works
        # well outside it, so "the Core is not in my nearby buildings" is the
        # NORMAL state, not a safe answer of "unhurt".  The decoded siege had
        # our only eligible converger parked at d^2 = 29 answering False for the
        # whole siege.  The Core publishes its own damage in slot 9 (dead since
        # LOKI-1 reclaimed it); read it when we cannot see for ourselves.
        # Bounded: a body eight tiles out is eight rounds from a seat and worth
        # recalling; one across the map is not, and recalling the whole economy
        # on a latch once finished a measured game with 0 titanium delivered.
        if T4_BLEED_BEACON_ON and self.core is not None:
            if ct.get_position().distance_squared(self.core) > T4_BEACON_BAND_DSQ:
                return False
            return (ct.read_store(SLOT_HEAL_BUDGET) & ARCH_BLEED_MASK) >= T4_BLEED_MIN
        return False

    def _live_home_gun(self, ct):
        if self.core is None:
            return False
        core = self.core
        for bid in ct.get_nearby_buildings():
            try:
                if ct.get_team(bid) != self.team:
                    continue
                if ct.get_entity_type(bid) not in TURRET_TYPES:
                    continue
                bp = ct.get_position(bid)
                if dsq_core(bp, core) <= HUNT_BAND_DSQ:
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
        hurt = False
        for eid in ct.get_nearby_buildings():
            try:
                if ct.get_team(eid) == self.team and ct.get_entity_type(eid) == EntityType.HARVESTER:
                    live += 1
                    # DETECTOR signal S4 (analysis/archetype_detector.md): our
                    # economy is being shot.  Piggy-backed on the census
                    # because a wounded harvester is the ONLY evidence of a
                    # standoff sniper we cannot see -- turret vision reaches
                    # further than a builder's, so the shooter is routinely
                    # outside anybody's sight while its target is not.
                    if ARCH_ON and not hurt and ct.get_hp(eid) < ct.get_max_hp(eid):
                        hurt = True
            except Exception:
                continue
        if hurt:
            self._arch_note(ct, pressure=True)
        if live > ct.read_store(SLOT_HARVESTERS):
            ct.write_store(SLOT_HARVESTERS, live)
        if live >= ECO_NEED:
            ct.write_store(SLOT_ECO_READY, 1)

    # --- LOKI-TURBO: flat-grid scaffolding ---------------------------------
    #
    # Both floods in this file run over a PADDED FLAT GRID: tile (x, y) lives
    # at index (y + 1) * (mw + 2) + (x + 1), and the one-tile border around the
    # map is permanently blocked.  Three things fall out at once, and none of
    # them changes a decision:
    #   * a neighbour is `idx + delta`, so Position.add (1.35 us, because
    #     Direction.delta rebuilds a dict every call) leaves the inner loop;
    #   * the blocked border IS the bounds test, so
    #     `0 <= x < mw and 0 <= y < mh` leaves the inner loop as well;
    #   * "wall", "seen" and "goal" share ONE bytearray, so the per-neighbour
    #     work is a single subscript rather than two tuple hashes into two sets.
    # The static part is built once per (Core anchor, enemy anchor) and copied
    # per call: copying a ~1 KB bytearray is ~0.15 us against the 15-30 us that
    # `set(self.map_walls)` cost on every single call before.

    def _flat_template(self, blocked_xy):
        w2 = self.mw + 2
        h2 = self.mh + 2
        t = bytearray(w2 * h2)
        last = (h2 - 1) * w2
        for x in range(w2):
            t[x] = 1
            t[last + x] = 1
        for y in range(h2):
            t[y * w2] = 1
            t[y * w2 + w2 - 1] = 1
        mw, mh = self.mw, self.mh
        for x, y in blocked_xy:
            if 0 <= x < mw and 0 <= y < mh:
                t[(y + 1) * w2 + x + 1] = 1
        return t

    def _nav_template(self):
        """(w2, template) for `_bfs_direction`: border + walls + both Cores."""
        key = (self.core, self.enemy, self.mw, self.mh)
        if self._nav_key != key:
            blocked = set(self.map_walls)
            if self.core is not None:
                blocked.update(core_tiles_xy(self.core))
            if self.enemy is not None:
                blocked.update(core_tiles_xy(self.enemy))
            self._nav_tpl = bytes(self._flat_template(blocked))
            self._nav_key = key
        return self.mw + 2, self._nav_tpl

    def _link_template(self):
        """(w2, template, ore_only) for `_link_path`.

        `ore_only[i]` marks a tile whose ONLY reason to be blocked is that it
        is ore -- LOKI excluded the harvester's own tile from the ore set but
        blocked walls and the Core footprint unconditionally, so this is what
        makes "copy the template, then unblock the start" exact.
        """
        key = (self.core, self.mw, self.mh)
        if self._link_tpl_key != key:
            mw, mh = self.mw, self.mh
            w2 = mw + 2
            walls = self.map_walls
            corexy = set(core_tiles_xy(self.core))
            blocked = set(walls)
            blocked.update((o.x, o.y) for o in self.map_ores)
            blocked.update(corexy)
            tpl = self._flat_template(blocked)
            ore_only = bytearray(len(tpl))
            for o in self.map_ores:
                k = (o.x, o.y)
                if k in walls or k in corexy:
                    continue
                if 0 <= o.x < mw and 0 <= o.y < mh:
                    ore_only[(o.y + 1) * w2 + o.x + 1] = 1
            self._link_tpl = bytes(tpl)
            self._link_ore_only = bytes(ore_only)
            self._link_tpl_key = key
        return self.mw + 2, self._link_tpl, self._link_ore_only

    def _link_goals(self, ban):
        """The ring of tiles orthogonally beside our Core, minus the ban.

        Pure function of the anchor, the map size and the ban, so it is built
        once instead of once per trunk-chain plan.  Held as the SAME set object
        across calls on purpose: `_link_path` seeds its queue by iterating the
        derived set, and a set's iteration order is a property of its element
        layout, so reusing one object keeps the multi-source BFS's tie-break
        bit-identical to LOKI's.
        """
        key = (self.core, self.mw, self.mh, ban)
        if self._link_goal_key != key:
            ox, oy = self.core.x, self.core.y
            mw, mh = self.mw, self.mh
            g = set()
            for cx, cy in core_tiles_xy(self.core):
                for dx, dy in CARD_DELTAS:
                    tx, ty = cx + dx, cy + dy
                    if not (0 <= tx < mw and 0 <= ty < mh):
                        continue
                    if ox <= tx <= ox + 1 and oy <= ty <= oy + 1:
                        continue                      # dist_core(t) == 0
                    g.add((tx, ty))
            if ban is not None:
                g -= ban
            self._link_goals_set = g
            self._link_goal_key = key
        return self._link_goals_set

    # --- trunk chain planning ---------------------------------------------

    def _link_path(self, ct, hpos):
        ban = self._pave_ban()
        raw_goals = self._link_goals(ban)
        start_xy = (hpos.x, hpos.y)
        if start_xy in raw_goals or not raw_goals:
            return []

        if self.map_grid is not None:
            mw, mh = self.mw, self.mh
            sx, sy = start_xy
            if not (0 <= sx < mw and 0 <= sy < mh):
                # LOKI floods the map and then finds no parent for an
                # off-map start.  Same answer, no flood.
                return []
            w2, tpl, ore_only = self._link_template()
            blk = bytearray(tpl)
            start = (sy + 1) * w2 + sx + 1
            if ore_only[start]:
                blk[start] = 0        # LOKI: every ore EXCEPT the harvester's
            if ban is not None:
                for bx, by in ban:
                    if 0 <= bx < mw and 0 <= by < mh:
                        blk[(by + 1) * w2 + bx + 1] = 1
            try:
                for eid in ct.get_nearby_buildings():
                    ep = ct.get_position(eid)
                    ex, ey = ep.x, ep.y
                    et = ct.get_entity_type(eid)
                    if (ex, ey) == start_xy:
                        continue
                    if et == EntityType.CORE:
                        for cx, cy in core_tiles_xy(ep):
                            if 0 <= cx < mw and 0 <= cy < mh:
                                blk[(cy + 1) * w2 + cx + 1] = 1
                    elif et not in BELT_TYPES:
                        if 0 <= ex < mw and 0 <= ey < mh:
                            blk[(ey + 1) * w2 + ex + 1] = 1
                    elif ct.get_team(eid) != self.team:
                        if 0 <= ex < mw and 0 <= ey < mh:
                            blk[(ey + 1) * w2 + ex + 1] = 1
            except Exception:
                pass

            # Reverse (multi-source) BFS from the Core ring out to the
            # harvester, exactly as before: same sources, same order, same
            # N/E/S/W expansion, so the same first parent wins.  `par` doubles
            # as the visited set; index 0 is a border cell and can never be a
            # parent, so 0 is a safe "unvisited" sentinel and -1 marks a root.
            #
            # LIFTED INTO A CLOSURE for PLANK SOCKET-GUARD arm 1a and NOTHING
            # ELSE: the body below is character-for-character leap6's, and the
            # first call passes leap6's own `raw_goals`, so the unbiased answer
            # is bit-identical.  The closure exists so the SAME flood can be
            # re-run against a single goal without a parallel router.
            def _sg_flood(goal_xy):
                goals = {g for g in goal_xy if not blk[(g[1] + 1) * w2 + g[0] + 1]}
                if not goals:
                    return None
                par = [0] * (w2 * (mh + 2))
                cur = []
                for gx, gy in goals:
                    gi = (gy + 1) * w2 + gx + 1
                    par[gi] = -1
                    cur.append(gi)
                d0, d1, d2, d3 = -w2, 1, w2, -1      # CARDINALS order
                nodes = len(cur)
                while cur and par[start] == 0:
                    nxt = []
                    for node in cur:
                        n = node + d0
                        if par[n] == 0 and not blk[n]:
                            par[n] = node
                            nxt.append(n)
                        n = node + d1
                        if par[n] == 0 and not blk[n]:
                            par[n] = node
                            nxt.append(n)
                        n = node + d2
                        if par[n] == 0 and not blk[n]:
                            par[n] = node
                            nxt.append(n)
                        n = node + d3
                        if par[n] == 0 and not blk[n]:
                            par[n] = node
                            nxt.append(n)
                    nodes += len(nxt)
                    if nodes > LINK_NODE_BUDGET:
                        break
                    cur = nxt
                if par[start] == 0:
                    return None
                out = []
                node = start
                while par[node] != -1:
                    node = par[node]
                    out.append(Position(node % w2 - 1, node // w2 - 1))
                return out

            path = _sg_flood(raw_goals)
            if path is None:
                return []
            # PLANK SOCKET-GUARD arm 1a -- FACE DIVERSITY, bought with routing
            # rather than titanium.  A conveyor cannot fork, so the only honest
            # way to feed a second Core face is to land a WHOLE SECOND CHAIN on
            # it, and the only lever that does that without inventing a second
            # router is the goal set of this very flood.  The Core has already
            # published which sockets it wants claimed (slot 9 bits 28-31, as
            # one socket or as a whole unfed FACE); if the unbiased route does
            # not terminate on one of them, re-run the identical flood against
            # just those and take it only if the detour is within
            # SG_FEED2_DETOUR links.  `path[-1]` is the BFS root, i.e. the
            # socket this chain would plug into.  The second flood runs ONLY
            # while the Core is asking, which is only while we hold fewer than
            # SG_FEED_WANT faces -- never on a healthy game's hot path.
            if (SG_ON and SG_TWO_FEEDERS and path
                    and ct.get_current_round() <= SG_FEED2_RND):
                want = self._sg_req_goals(ct)
                if want:
                    want = tuple(g for g in want if g in raw_goals)
                if want and (path[-1].x, path[-1].y) not in want:
                    alt = _sg_flood(want)
                    if alt is not None and len(alt) - len(path) <= SG_FEED2_DETOUR:
                        path = alt
            # PLANK SPLIT arm A2 -- THE FORK IS ROUTED TO, NOT WAITED FOR.
            # Arm A alone forks only when the unbiased route HAPPENS to arrive
            # through a corner, and `tools/split_geometry.py` enumerated that
            # over all 15 pool maps, both sides, the three nearest ore tiles:
            # **9.2 % of termini**.  The plank would be dead code in nine games
            # out of ten.  The same enumeration priced the fix: re-run this
            # identical flood against the four CORNERS as goals and the corner
            # is reachable for the SAME number of conveyors on 39.1 % of
            # termini and within two extra on 89.7 %.  SP_DETOUR = 0 therefore
            # buys 4x the coverage for exactly nothing -- same chain length,
            # same latency, same cost scale, a different shape -- and the
            # priced variants exist for a measurement to choose between.
            # Structurally this is SG arm 1a, which is why it is here and not
            # in a second router.
            if (SPLIT_ON and SP_ROUTE_BIAS_ON and path
                    and self.sp_built < SP_MAX_PER_UNIT
                    and ct.get_current_round() <= SP_BIAS_RND):
                alt = self._sp_bias_path(_sg_flood, blk, w2, path)
                if alt is not None:
                    path = alt
            return path

        # UNKNOWN MAP.  Forward BFS on live vision; every tile costs two engine
        # calls, so the flood is bounded by the API rather than by arithmetic
        # and the wall-clock probe stays.  Only the Position churn is removed.
        goals = raw_goals
        core = self.core
        mw, mh = self.mw, self.mh
        prev = {start_xy: None}
        q = deque([start_xy])
        found = None
        steps = 0
        while q:
            x, y = q.popleft()
            steps += 1
            if steps % 64 == 0 and self._cpu_exhausted(ct):
                break
            if (x, y) in goals and (x, y) != start_xy:
                found = (x, y)
                break
            for dx, dy in CARD_DELTAS:
                nx, ny = x + dx, y + dy
                key = (nx, ny)
                if key in prev or not (0 <= nx < mw and 0 <= ny < mh):
                    continue
                n = Position(nx, ny)
                if dist_core(n, core) == 0:
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
                        if et not in LINK_ROUTABLE_TYPES:
                            continue
                    except Exception:
                        continue
                prev[key] = (x, y)
                q.append(key)
        if found is None:
            return []
        path, cur = [], found
        while cur is not None and cur != start_xy:
            path.append(Position(cur[0], cur[1]))
            cur = prev[cur]
        path.reverse()
        return path

    def _wire_on_build(self, ct, bp):
        if not self.link_queue:
            self.link_source = bp
            plan = self._link_path(ct, bp)
            self.link_queue = plan
            # LOKI-SAMESTOP (QUEUE #50): only the FIRST harvester of a
            # wiring job is a candidate -- see doctrine.py SCOPE note. A
            # harvester queued behind others below defers its real route to
            # _wire_tick and is out of scope by construction.
            self._samestop_arm(ct, bp, plan)
            return
        if not SIPHON_WIRE_ON or len(self.wire_pending) >= SIPHON_WIRE_QUEUE:
            return
        self.wire_pending.append((bp, ct.get_current_round()))

    def _has_acceptor(self, ct, bp):
        bx, by = bp.x, bp.y
        for dx, dy in CARD_DELTAS:
            tx, ty = bx + dx, by + dy
            if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                continue
            t = Position(tx, ty)
            try:
                bid = ct.get_tile_building_id(t)
                if bid is None or ct.get_team(bid) != self.team:
                    continue
                if ct.get_entity_type(bid) in ACCEPTOR_TYPES:
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

    # --- LOKI-SAMESTOP (QUEUE #50): harvester + first outbound conveyor
    # from one builder stop.  See doctrine.py for the research #50 cut and
    # the mechanism this leans on (_l4_repair fills the vacated stand tile
    # as a HOLE once this builder steps off it). ------------------------

    def _samestop_plan(self, ct, ore):
        """The trunk route home for `ore`, cached per ore tile so the
        stop-tile preference below does not re-run a full-map BFS every
        round a builder is still walking toward it.  Reuses _link_path
        verbatim -- research #50 cut, step 3c: "do not invent a parallel
        router".
        """
        if not LOKI_SAMESTOP_ON:
            return None
        key = (ore.x, ore.y)
        if self.samestop_plan_key == key:
            return self.samestop_plan_cache
        plan = self._link_path(ct, ore)
        self.samestop_plan_key = key
        self.samestop_plan_cache = plan
        return plan

    def _samestop_stand_pref(self, ct, ore):
        """Preferred standing tile T for building a harvester on `ore` --
        the trunk route's own plan[0], IF it is currently passable.

        research #50 cut, step 3a: "Only a PREFERENCE among otherwise-valid
        tiles: if no such T exists, current behaviour is unchanged" --
        returning None does exactly that, since the caller only overrides
        self.tgt when this returns a real tile.
        """
        plan = self._samestop_plan(ct, ore)
        if not plan:
            return None
        t = plan[0]
        try:
            if not ct.is_tile_passable(t):
                return None
        except Exception:
            return None
        return t

    def _samestop_arm(self, ct, ore, plan):
        """Record the SAME-STOP second build for next round (research #50
        cut, step 3b).  Called once, right after the harvester at `ore` is
        built, while this builder is still on its stand tile -- one action
        per turn (build OR move, never both) means the second build cannot
        happen this same round, so this only ARMS it; `_samestop_fire`
        below performs it, next round, before any move.

        `plan` is the SAME list _wire_on_build just assigned to
        self.link_queue -- reused, not recomputed, so this can never
        disagree with the route the incumbent trunk planner is about to
        build (step 3c: "do not invent a parallel router").
        """
        self.samestop_pending = None
        if not LOKI_SAMESTOP_ON or not plan or len(plan) < 2:
            return
        t = ct.get_position()
        if (plan[0].x, plan[0].y) != (t.x, t.y):
            # The planner's first link is not the tile we happen to be
            # standing on -- step 3c: prefer relocating the STOP over
            # changing the plan, so if the stop missed there is nothing
            # coherent left to arm here.
            return
        r = plan[1]
        if abs(r.x - t.x) + abs(r.y - t.y) != 1:
            return
        # Same facing rule _build_next_link uses for a queued link: point at
        # the NEXT planned tile when there is one, else coreward.
        if len(plan) >= 3:
            f = r.cardinal_direction_to(plan[2])
            if f == Direction.CENTRE:
                f = nearest_cardinal(r.direction_to(nearest_core_tile(r, self.core)))
        else:
            f = nearest_cardinal(r.direction_to(nearest_core_tile(r, self.core)))
        if f == Direction.CENTRE:
            f = Direction.NORTH
        self.samestop_pending = (t.x, t.y, r, f)

    def _samestop_fire(self, ct):
        """Fire the armed same-stop conveyor, or drop it silently.

        research #50 cut, step 3b: "If the tile became occupied or the
        builder was displaced, drop the pending build silently and let
        existing behaviour resume." Scale-neutral by construction: R is
        plan[1] exactly as the incumbent planner already produced it -- this
        only changes WHEN and FROM WHERE it gets built, never the count of
        links in the chain.
        """
        tx, ty, r, f = self.samestop_pending
        self.samestop_pending = None
        p = ct.get_position()
        if (p.x, p.y) != (tx, ty):
            return False
        try:
            if not ct.can_build_conveyor(r, f):
                return False
            ct.build_conveyor(r, f)
        except Exception:
            return False
        if LOKI_SAMESTOP_LOG:
            print(f"SS50 SAMESTOP rnd={ct.get_current_round()} "
                  f"stand={tx},{ty} r={r.x},{r.y} face={f.name} id={ct.get_id()}")
        return True

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
        # PLANK SPLIT arm A -- THE FORK IS LAID BY THE TRUNK ITSELF.  The tile
        # about to be laid is the chain's PENULTIMATE link whenever the queue
        # still holds two, and the tile behind it is already standing (the
        # chain is laid harvester-first).  If that penultimate tile is one of
        # our Core CORNERS -- the only tiles orthogonally adjacent to two
        # delivery sockets -- a splitter goes there instead of a conveyor and
        # the line ends in TWO sockets rather than one.  No detour, no second
        # route, no extra build: this is the same build, of a different
        # building.  Falls through to the incumbent conveyor on every tile
        # where the geometry does not carry two sockets.
        if (SPLIT_ON and len(self.link_queue) >= 2
                and self._sp_fork_here(ct, tile, self.link_queue[1])):
            self.link_queue.pop(0)
            return True
        if ct.can_build_conveyor(tile, f):
            ct.build_conveyor(tile, f)
            self.link_queue.pop(0)
            return True
        return False

    # --- PLANK SPLIT (wave 17b): the second delivery route -----------------
    # See the block at the end of doctrine.py.  Three arms, all of them
    # stateless on the board apart from a per-unit re-lay counter: arm A is
    # the hook above, arm B (`_sp_fork`) re-lays a fork that was shot out or
    # upgrades a standing corner conveyor, arm C (`_sp_wire_seat`) wires the
    # second socket the fork opens.

    def _sp_bias_path(self, flood, blk, w2, path):
        """Arm A2: the same chain, re-routed to arrive through a CORNER.

        `flood` is `_link_path`'s own closure -- same blocked template, same
        multi-source reverse BFS, same N/E/S/W expansion order -- run against
        the four corners instead of the eight sockets, and `blk` is that
        template, borrowed and put back byte for byte.

        Two things make the answer usable as a trunk plan:
          * THE SOCKETS ARE MASKED OUT for this flood.  A chain that reaches
            the corner by running THROUGH a socket has already spent the tile
            the fork exists to protect, and it would also put a socket on the
            splitter's BACK, which is the one side a splitter does not output
            to -- the fork would carry one socket, not two.
          * THE SOCKET IS APPENDED.  A corner is not adjacent to the Core, so
            the chain cannot end there: it ends on one of the two sockets the
            corner flanks, which is the tile the fork delivers through first
            and which `_build_next_link` lays exactly as it lays any terminus.
        Total length is therefore len(alt) + 1, and the detour against the
        unbiased chain is that minus len(path), in conveyors.

        Returns the replacement plan, or None to keep the unbiased one.
        """
        seats = self._sp_seat_keys()
        corners = self._sp_corner_keys()
        if not corners or not seats:
            return None
        if (path[-1].x, path[-1].y) not in seats:
            return None
        if len(path) >= 2 and (path[-2].x, path[-2].y) in corners:
            return None                       # already forkable, leave it
        goals = tuple(c for c in corners
                      if not blk[(c[1] + 1) * w2 + c[0] + 1])
        if not goals:
            return None
        saved = []
        for sx, sy in seats:
            i = (sy + 1) * w2 + sx + 1
            saved.append((i, blk[i]))
            blk[i] = 1
        alt = None
        try:
            alt = flood(goals)
        except Exception:                     # noqa: BLE001
            alt = None
        # RESTORED UNCONDITIONALLY, and without a `finally` -- the platform's
        # AST validator rejects `finally` outright.  `blk` is a local bytearray
        # of the caller's frame, so the only path that could leave it masked is
        # one that abandons that frame anyway (a CPU-time interruption).
        for i, v in saved:
            blk[i] = v
        if not alt:
            return None
        if len(alt) + 1 > len(path) + SP_DETOUR:
            return None
        c = alt[-1]
        # The terminus: the socket the unbiased route had already chosen if the
        # corner flanks it, else the first free flanking socket in the fixed
        # `heal_seats` order, so the choice is deterministic.
        want = (path[-1].x, path[-1].y)
        pick = None
        for dx, dy in CARD_DELTAS:
            tx, ty = c.x + dx, c.y + dy
            if (tx, ty) not in seats:
                continue
            if blk[(ty + 1) * w2 + tx + 1]:
                continue
            if (tx, ty) == want:
                pick = (tx, ty)
                break
            if pick is None:
                pick = (tx, ty)
        if pick is None:
            return None
        return alt + [Position(pick[0], pick[1])]

    def _sp_seat_keys(self):
        """{(x, y)} of our own eight sockets.  Cached, pure geometry."""
        if self.core is None or not (self.mw and self.mh):
            return frozenset()
        key = (self.core, self.mw, self.mh)
        if self._sp_seat_key != key:
            self._sp_seats = frozenset(
                (s.x, s.y) for s in heal_seats(self.core, self.mw, self.mh))
            self._sp_seat_key = key
        return self._sp_seats

    def _sp_corner_keys(self):
        """{(x, y)} of our four Core corners -- the only tiles on the board
        orthogonally adjacent to TWO of our sockets, and therefore the only
        tiles a fork can stand on."""
        if self.core is None or not (self.mw and self.mh):
            return frozenset()
        key = (self.core, self.mw, self.mh)
        if self._sp_corner_key != key:
            self._sp_corners = frozenset(
                (c.x, c.y) for c in core_corners(self.core, self.mw, self.mh))
            self._sp_corner_key = key
        return self._sp_corners

    def _sp_feeder(self, ct, c, seats):
        """(x, y) of the tile feeding `c`, or None.

        A splitter accepts input ONLY from the tile directly behind it, so the
        feeder is what fixes the facing and there is nothing to choose: our
        conveyor whose output tile is `c`, or -- for a one-link chain -- our
        harvester beside it, which feeds any adjacent acceptor directly.

        A SOCKET is never accepted as the feeder.  The sockets are what the
        fork exists to reach; a chain arriving through one of them has already
        spent the tile it was meant to make redundant, and putting it behind
        the splitter would leave only one socket among the three outputs.
        """
        cx, cy = c.x, c.y
        harv = None
        for dx, dy in CARD_DELTAS:
            tx, ty = cx + dx, cy + dy
            if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                continue
            if (tx, ty) in seats:
                continue
            t = Position(tx, ty)
            try:
                bid = ct.get_tile_building_id(t)
                if bid is None or ct.get_team(bid) != self.team:
                    continue
                et = ct.get_entity_type(bid)
            except Exception:
                continue
            if et == EntityType.CONVEYOR:
                try:
                    odx, ody = DELTA[ct.get_direction(bid)]
                except Exception:
                    continue
                if tx + odx == cx and ty + ody == cy:
                    return (tx, ty)
            elif et == EntityType.HARVESTER and harv is None:
                harv = (tx, ty)
        return harv

    def _sp_plan(self, ct, c):
        """(facing, sockets_covered, feeder) for a fork at `c`, or None.

        `facing` is the cardinal pointing AWAY from the feeder, which is what
        puts the feeder on the splitter's back.  The other three neighbours are
        its outputs, and `sockets_covered` is how many of them are sockets --
        the number the whole plank turns on, and the one `SP geom` reports.
        """
        fd = self._sp_feeder(ct, c, self._sp_seat_keys())
        if fd is None:
            return None
        f = cardinal_from_delta(c.x - fd[0], c.y - fd[1])
        if f is None:
            return None
        seats = self._sp_seat_keys()
        n = 0
        for dx, dy in CARD_DELTAS:
            tx, ty = c.x + dx, c.y + dy
            if (tx, ty) == fd:
                continue
            if (tx, ty) in seats:
                n += 1
        return (f, n, fd)

    def _sp_count(self, ct):
        """Live forks standing on our own Core corners.

        The team-wide cap, censused off the board rather than off a store slot:
        every arm of this plank acts from a tile orthogonally adjacent to the
        corner it is acting on, so all four corners are inside that body's own
        vision (r^2 = 20) whenever the question is asked.  A corner we cannot
        see is counted as empty, which can only ever cost us one extra fork.
        """
        n = 0
        for cx, cy in self._sp_corner_keys():
            t = Position(cx, cy)
            try:
                if not ct.is_in_vision(t):
                    continue
                bid = ct.get_tile_building_id(t)
                if bid is None or ct.get_team(bid) != self.team:
                    continue
                if ct.get_entity_type(bid) == EntityType.SPLITTER:
                    n += 1
            except Exception:
                continue
        return n

    def _sp_geom_mark(self, ct, tile, corner, n, tag="geom"):
        """`SP geom` -- one line per terminus evaluated, fork or fallback.

        THE COVERAGE INSTRUMENT (`tag="geom"`, arm A only -- arm B re-evaluates
        the same corners under `tag="corner"` so it cannot pollute the
        denominator), and it is the reason arm A logs a NEGATIVE result at all: the fork is placed by geometry the router chose without
        knowing this plank exists, so "how often is a two-socket fork even
        placeable" is a measurement and not a design parameter.  Deduped per
        unit on the tile so a body that stalls beside its terminus for ten
        rounds does not print ten lines.
        """
        if not (SPLIT_ON and SP_LOG):
            return
        key = (tag, tile.x, tile.y, corner, n)
        if self.sp_geom == key:
            return
        self.sp_geom = key
        print("SP %s (%d,%d) corner=%d seats=%d r=%d" % (
            tag, tile.x, tile.y, 1 if corner else 0, n, ct.get_current_round()))

    def _sp_fork_here(self, ct, tile, nxt):
        """Arm A: lay the fork at `tile` instead of a conveyor.  True = built.

        `nxt` is the chain's terminal socket.  Its own four neighbours are one
        Core tile, one corner, the other socket of its face and one outer
        tile -- and every socket is a root of `_link_path`'s reverse flood, so
        a socket can never be the parent of a socket.  The penultimate tile is
        therefore ALWAYS the corner or the outer tile, and this method is the
        coin toss between them.
        """
        if self.sp_built >= SP_MAX_PER_UNIT:
            return False
        rnd = ct.get_current_round()
        if rnd < SP_MIN_RND or rnd > SP_UNTIL:
            return False
        if (nxt.x, nxt.y) not in self._sp_seat_keys():
            return False              # the chain does not terminate on a socket
        corner = (tile.x, tile.y) in self._sp_corner_keys()
        if not corner:
            self._sp_geom_mark(ct, tile, False, 0)
            return False
        plan = self._sp_plan(ct, tile)
        if plan is None:
            return False              # no feeder standing yet: transient, and
        f, n, _fd = plan              # deliberately NOT a geometry verdict
        self._sp_geom_mark(ct, tile, True, n)
        if n < SP_MIN_SEATS:
            return False
        # NO TITANIUM FLOOR ON ARM A, and the first probe is why.  This build
        # REPLACES one `_build_next_link` has already authorised and priced at
        # the conveyor's 3 Ti; charging it the plank's reserve on top made the
        # opening decline the fork at frostgate r28 on a 14 Ti bank against a
        # scaled cost of 11 + 6.  The marginal spend is the price difference,
        # not the whole building, and a chain that must not stall is exactly
        # what `_build_next_link`'s own gate above already guarantees.
        return self._sp_build(ct, tile, f, n, rnd, SP_TRUNK_FLOOR)

    def _sp_build(self, ct, c, f, n, rnd, floor=None):
        """The build itself, shared by arms A and B.  True = the fork is up."""
        try:
            cost = ct.get_splitter_cost()
        except Exception:
            return False
        if not self._eco_spendable(
                ct, cost + (SP_TI_FLOOR if floor is None else floor)):
            return False
        if self._sp_count(ct) >= SP_MAX:
            return False
        try:
            if not ct.can_build_splitter(c, f):
                return False
            ct.build_splitter(c, f)
        except Exception:
            return False
        self.sp_built += 1
        if SP_LOG:
            print("SP fork (%d,%d) seats=%d f=%s r=%d" % (
                c.x, c.y, n, getattr(f, "name", f), rnd))
        return True

    def _sp_terminus(self, ct, c, seats):
        """The live delivery socket beside corner `c`, or None.

        "Live" is the strict test and it is what keeps arm B off a corner that
        is not a terminus at all: OUR conveyor, standing on a socket, whose
        output tile is one of our own Core tiles.
        """
        corexy = core_tiles_xy(self.core)
        for dx, dy in CARD_DELTAS:
            tx, ty = c.x + dx, c.y + dy
            if (tx, ty) not in seats:
                continue
            t = Position(tx, ty)
            try:
                bid = ct.get_tile_building_id(t)
                if bid is None or ct.get_team(bid) != self.team:
                    continue
                if ct.get_entity_type(bid) != EntityType.CONVEYOR:
                    continue
                odx, ody = DELTA[ct.get_direction(bid)]
            except Exception:
                continue
            if (tx + odx, ty + ody) in corexy:
                return t
        return None

    def _sp_fed_by_fork(self, ct, s):
        """Is socket `s` one of the three outputs of a fork of ours?

        The back tile of a splitter is `pos - facing`; every other neighbour is
        an output, and an output on empty ground is a DEAD output the splitter
        skips.  That is precisely the tile arm C exists to fill.
        """
        for dx, dy in CARD_DELTAS:
            tx, ty = s.x + dx, s.y + dy
            if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                continue
            try:
                bid = ct.get_tile_building_id(Position(tx, ty))
                if bid is None or ct.get_team(bid) != self.team:
                    continue
                if ct.get_entity_type(bid) != EntityType.SPLITTER:
                    continue
                odx, ody = DELTA[ct.get_direction(bid)]
            except Exception:
                continue
            if (tx - odx, ty - ody) != (s.x, s.y):
                return True
        return False

    def _sp_wire_seat(self, ct, p, rnd):
        """Arm C: lay the conveyor on the SECOND socket a fork opened.

        Stateless, exactly like `_l4_repair`: the condition is "our fork points
        at this socket, the socket is empty, the Core is beside it", and laying
        the conveyor destroys that condition, so the rule cannot walk and needs
        no memory of what used to stand there.  That is also what re-wires the
        socket after they shoot it out.

        THE SEAT BAN IS DELIBERATELY NOT CONSULTED HERE, and in this lineage
        that costs nothing: `HS_SEAT_BAN_CONVEYORS` is False, so `_seat_ban`
        only keeps our own HARVESTERS and TURRETS off the non-delivery sockets
        and has never applied to belts.  What the socket does cost is a HEAL
        SEAT -- a socket holding a building is one no body of ours can heal
        from -- and that is pre-registered as risk R2.  It is taken because the
        elite-gap finding cuts the other way: in the games we lose those seats
        are THEIRS by r50, and a socket holding OUR conveyor is a socket they
        cannot brick.  At most SP_MAX of them are spent.
        """
        seats = self._sp_seat_keys()
        if not seats:
            return False
        try:
            cost = ct.get_conveyor_cost()
        except Exception:
            return False
        if not self._eco_spendable(ct, cost + SP_TI_FLOOR):
            return False
        corexy = core_tiles_xy(self.core)
        for dx, dy in CARD_DELTAS:
            sx, sy = p.x + dx, p.y + dy
            if (sx, sy) not in seats:
                continue
            s = Position(sx, sy)
            try:
                if not ct.is_tile_empty(s):
                    continue
            except Exception:
                continue
            if not self._sp_fed_by_fork(ct, s):
                continue
            f = None
            for ddx, ddy in CARD_DELTAS:
                if (sx + ddx, sy + ddy) in corexy:
                    f = cardinal_from_delta(ddx, ddy)
                    break
            if f is None:
                continue
            try:
                if not ct.can_build_conveyor(s, f):
                    continue
                ct.build_conveyor(s, f)
            except Exception:
                continue
            if SP_LOG:
                print("SP seat (%d,%d) f=%s r=%d" % (
                    sx, sy, getattr(f, "name", f), rnd))
            return True
        return False

    def _sp_fork(self, ct):
        """Arms C and B, in that order.  True = the action was spent.

        Arm C first on purpose: a fork whose second socket is still empty has
        bought NOTHING -- the splitter skips the dead output and the line is
        exactly the single-socket line it replaced -- so finishing one fork
        outranks starting another.
        """
        if not SPLIT_ON or self.core is None:
            return False
        rnd = ct.get_current_round()
        if rnd < SP_MIN_RND or rnd > SP_UNTIL:
            return False
        p = ct.get_position()
        if dsq_core(p, self.core) > SP_BAND_DSQ:
            return False              # not at home: nothing here can apply
        if self._cpu_exhausted(ct):
            return False
        if SP_SEAT_WIRE_ON and self._sp_wire_seat(ct, p, rnd):
            return True
        if self.sp_built >= SP_MAX_PER_UNIT:
            return False
        seats = self._sp_seat_keys()
        corners = self._sp_corner_keys()
        for dx, dy in CARD_DELTAS:
            cx, cy = p.x + dx, p.y + dy
            if (cx, cy) not in corners:
                continue
            c = Position(cx, cy)
            if self._sp_terminus(ct, c, seats) is None:
                continue              # this corner is not a live terminus
            plan = self._sp_plan(ct, c)
            if plan is None:
                continue
            f, n, _fd = plan
            # A DIFFERENT TAG, and the first smoke batch is why: `SP geom` is
            # arm A's COVERAGE instrument -- one line per trunk terminus the
            # router chose -- and arm B evaluates the same corners again every
            # time a body stands beside one, which inflated the denominator by
            # a third and made a no-bias arm read HIGHER coverage than the
            # biased one.  Arm B reports under `SP corner` and is counted
            # separately or not at all.
            self._sp_geom_mark(ct, c, True, n, "corner")
            if n < SP_MIN_SEATS:
                continue
            try:
                empty = ct.is_tile_empty(c)
            except Exception:
                continue
            if empty:
                # The fork was shot out, or the chain was laid before this
                # plank could reach the tile.  A plain build, no risk.
                if self._sp_build(ct, c, f, n, rnd):
                    return True
                continue
            if not SP_CONVERT_ON:
                continue
            # THE SWAP.  destroy() is free, takes no action cooldown and gives
            # back its own +1 % scale in the same round, so upgrading a
            # standing corner conveyor costs the 3 Ti of price difference and
            # one stack in transit.  It is attempted only on a link that is
            # actually the terminus feed, and only with the replacement
            # already affordable and inside the cap.
            standing = self._sp_standing_link(ct, c)
            if standing is None:
                continue
            try:
                cost = ct.get_splitter_cost()
            except Exception:
                continue
            if not self._eco_spendable(ct, cost + SP_TI_FLOOR):
                continue
            if self._sp_count(ct) >= SP_MAX:
                continue
            try:
                if not ct.can_destroy(c):
                    continue
                ct.destroy(c)
            except Exception:
                continue
            if SP_LOG:
                print("SP conv (%d,%d) r=%d" % (cx, cy, rnd))
            if self._sp_build(ct, c, f, n, rnd):
                return True
            # RECOVERY, and it is not optional: we have just taken a LIVE link
            # out of a delivering chain.  Put it back this same round rather
            # than leave the trunk severed for `_l4_repair` to find.
            try:
                if ct.can_build_conveyor(c, standing):
                    ct.build_conveyor(c, standing)
                    return True
            except Exception:
                pass
            return False
        return False

    def _sp_standing_link(self, ct, c):
        """The facing of OUR conveyor at `c` when it feeds a live socket.

        Returns the facing (so the swap can put it back verbatim if the
        splitter build fails), or None when the tile is not that link.
        """
        try:
            bid = ct.get_tile_building_id(c)
            if bid is None or ct.get_team(bid) != self.team:
                return None
            if ct.get_entity_type(bid) != EntityType.CONVEYOR:
                return None
            odx, ody = DELTA[ct.get_direction(bid)]
        except Exception:
            return None
        if (c.x + odx, c.y + ody) not in self._sp_seat_keys():
            return None
        return cardinal_from_delta(odx, ody)

    # --- trunk repair (LOKI-L4) --------------------------------------------

    def _l4_harvester_starved(self, ct, hpos, gap):
        """True when the harvester at `hpos` has NO acceptor except `gap`.

        The gate on the harvester half of `_l4_repair`, and it is not optional:
        without it the rule fires on any harvester with a spare side next to a
        belt, which is a SECOND route for a harvester that already has one.
        Measured on the first build of this plank, 15 local games: 36 of 55
        repairs were that case and bought nothing -- a harvester emits one
        stack per 4 rounds however many acceptors surround it, so the extra
        link is 3 Ti and +1% team cost scale for zero throughput.  With this
        gate the harvester half only fires on a harvester whose route home is
        GONE, which is the case the corpus says is worth everything: a
        harvester with no route to the Core delivers zero, forever.

        An ENEMY belt beside our harvester is not an acceptor for this purpose.
        The round-robin is team-blind so it does take a share, but it delivers
        that share to THEIR core -- it is the siphon, not a route home.
        """
        hx, hy = hpos.x, hpos.y
        gx, gy = gap.x, gap.y
        for dx, dy in CARD_DELTAS:
            tx, ty = hx + dx, hy + dy
            if tx == gx and ty == gy:
                continue
            if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                continue
            t = Position(tx, ty)
            try:
                bid = ct.get_tile_building_id(t)
                if bid is None or ct.get_team(bid) != self.team:
                    continue
                et = ct.get_entity_type(bid)
                if et == EntityType.CORE or et == EntityType.SPLITTER:
                    return False
                if et == EntityType.CONVEYOR:
                    odx, ody = DELTA[ct.get_direction(bid)]
                    if tx + odx != hx or ty + ody != hy:
                        return False
            except Exception:
                continue
        return True

    def _l4_repair(self, ct):
        """Relay ONE missing link of a chain this builder is standing beside.

        THE RULE, and it is stateless on purpose -- no remembered map, no store
        slot, nothing to go stale when a launcher throws this body across the
        map.  A tile G orthogonally adjacent to this builder is repaired when G
        is empty and, among G's own four orthogonal neighbours, there is BOTH

            a FEEDER   -- our conveyor whose output tile is G (a belt aimed at
                          nothing is delivering nothing through that side), or
                          a STARVED harvester, one with no other acceptor at
                          all (see _l4_harvester_starved);
            an ACCEPTOR -- our Core, or our conveyor whose output tile is NOT G
                          (a conveyor accepts from its other three sides).

        Chain on both sides of an empty tile is a HOLE, not a HEAD, and that is
        what makes the rule safe: filling the hole removes the condition, so it
        cannot walk, and no memory of what used to stand there is required.

        HONEST ABOUT WHAT IT FIXES.  Counted off 15 local replays, the conveyor
        half fires on belts aimed at empty ground -- and only 1 of those tiles
        had ever HELD a conveyor.  The rest are DEAD HEADS: chains this bot
        abandoned mid-walk, which `_build_next_link` never returns to because
        it pops its queue as it lays it.  So this plank repairs two things that
        both present as "a belt that delivers nothing", one of which is the
        enemy cutting us and the other of which is our own planner giving up.

        WHAT IT DELIBERATELY DOES NOT DO.  A two-wide hole has no side with
        both a feeder and an acceptor, so it is left alone; so is a dead head
        with no acceptor in reach.  Repairing those means extending a head
        coreward tile by tile, which is the PIECE F pave trail, and LOKI-13
        measured that off at 38.20 conveyors/game (PAVE_TRAIL_ON, doctrine.py).
        A narrow rule that cannot spam is worth more here than a complete one
        that can.

        Splitters are never a feeder, and PLANK SPLIT does NOT change that.
        This tree now builds them (`_sp_fork`), but a splitter's output rotates
        among three directions and SKIPS the dead ones, so an empty output tile
        is its normal state rather than evidence of a cut -- reading one as a
        feeder would have this rule pave both of its spare sides.  The one
        empty output that IS worth filling is the second SOCKET of a fork, and
        that tile has its own narrow rule in `_sp_wire_seat`, ranked directly
        above this one.
        """
        if not LOKI_L4_REPAIR_ON or self.core is None:
            return False
        if self._cpu_exhausted(ct):
            return False
        if not self._eco_spendable(ct, ct.get_conveyor_cost()):
            return False
        p = ct.get_position()
        px, py = p.x, p.y
        ban = self._pave_ban()
        for gdx, gdy in CARD_DELTAS:
            ggx, ggy = px + gdx, py + gdy
            if not (0 <= ggx < self.mw and 0 <= ggy < self.mh):
                continue
            g = Position(ggx, ggy)
            if (
                LOKI_L4_OWN_HALF_ONLY and self.enemy is not None
                and g.distance_squared(self.core) > g.distance_squared(self.enemy)
            ):
                continue
            try:
                # is_tile_empty is "no building and not a wall", which is
                # exactly the gap condition; a bot standing there is caught by
                # can_build_conveyor below.
                if not ct.is_tile_empty(g):
                    continue
            except Exception:
                continue
            # Same terrain ban the pave path uses: a conveyor on ore costs that
            # harvester site for the rest of the match.
            if pave_blocked(ct, g, ban):
                continue
            feeder = None
            acc_dir, acc_key = None, None
            for ni in (0, 1, 2, 3):
                ndx, ndy = CARD_DELTAS[ni]
                tx, ty = ggx + ndx, ggy + ndy
                if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                    continue
                nd = CARDINALS[ni]
                t = Position(tx, ty)
                try:
                    bid = ct.get_tile_building_id(t)
                    if bid is None or ct.get_team(bid) != self.team:
                        continue
                    et = ct.get_entity_type(bid)
                except Exception:
                    continue
                if et == EntityType.HARVESTER:
                    # Gated: only a harvester with no route home at all.
                    if feeder is None and self._l4_harvester_starved(ct, t, g):
                        feeder = "harv"
                elif et == EntityType.CORE:
                    # The delivery terminus always wins: a hole beside the Core
                    # is the one that costs the whole chain.
                    if acc_key is None or acc_key > (0, 0):
                        acc_dir, acc_key = nd, (0, 0)
                elif et == EntityType.CONVEYOR:
                    try:
                        odx, ody = DELTA[ct.get_direction(bid)]
                    except Exception:
                        continue
                    if tx + odx == ggx and ty + ody == ggy:
                        feeder = "belt"
                        continue
                    # Coreward-most acceptor first, so the relaid link points
                    # down the chain rather than back up it.
                    key = (1, dist_core(t, self.core))
                    if acc_key is None or key < acc_key:
                        acc_dir, acc_key = nd, key
            if feeder is None or acc_dir is None:
                continue
            try:
                if not ct.can_build_conveyor(g, acc_dir):
                    continue
                ct.build_conveyor(g, acc_dir)
            except Exception:
                continue
            if LOKI_L4_LOG:
                print(f"L4R45 L4REPAIR rnd={ct.get_current_round()} "
                      f"tile={g.x},{g.y} face={acc_dir.name} "
                      f"feed={feeder} id={ct.get_id()}")
            # PLANK REPAIR marker.  The inherited rule keeps its own L4R45
            # tag; this one exists so the plank's rebuild half can be counted
            # off a replay with one vocabulary, and it is gated on REPAIR_ON
            # so the inertness leg emits none of it.
            self._rep_mark(ct, "rebuild", g, dedupe=False)
            return True
        # PLANK REPAIR: the two-wide hole the rule above is documented to
        # refuse.  Ranked last so it can never pre-empt the one-wide relay.
        if REPAIR_ON and REPAIR_REBUILD_ON and self._rep_gap2(ct, ban):
            return True
        return False

    # ------------------------------------------------------------------
    # PLANK SOCKET-GUARD (SG) -- see the block at the end of doctrine.py
    # ------------------------------------------------------------------

    def _sg_mark(self, ct, tag, tile):
        """One replay line per SG event.  Local instrument only."""
        if not (SG_ON and SG_LOG):
            return
        print("SG %s (%d,%d) r=%d" % (tag, tile.x, tile.y,
                                      ct.get_current_round()))

    def _sg_terrain(self, ct):
        """Fill map_walls / map_ores from the decoded grid, once.

        `_builder` already does this on its first turn; the CORE never did,
        because nothing it ran needed terrain.  `_sg_request_bits` does: it
        ranks free sockets partly by `delivery_seats`, which is ore-aware, and
        with an empty ore list that degrades to a map-centre heuristic.  Same
        scan, same row-major order, same `str.find` in C.
        """
        if self.map_grid is None or self.map_walls or self.map_ores:
            return
        walls = set()
        ores = []
        for y, row in enumerate(self.map_grid):
            i = row.find("#")
            while i >= 0:
                walls.add((i, y))
                i = row.find("#", i + 1)
            i = row.find("o")
            while i >= 0:
                ores.append(Position(i, y))
                i = row.find("o", i + 1)
        self.map_walls = walls
        self.map_ores = ores

    def _sg_keep_idx(self):
        """Socket indices of the seats the trunk planner has RESERVED."""
        if self.core is None:
            return frozenset()
        self._seat_ban()                      # populates self.seat_keep
        keep = self.seat_keep or ()
        out = set()
        for s in keep:
            i = sg_socket_index(self.core, s.x, s.y)
            if i >= 0:
                out.add(i)
        return out

    def _sg_socket_scan(self, ct, deep=False):
        """Census our own eight sockets.  Only meaningful to a unit that can
        SEE them -- the Core always can, a builder only near home.

        Returns (feed, free, mine, foe, aimed, hfed), all sets of socket index:

            feed  our conveyor standing on it and OUTPUTTING into a Core tile,
                  i.e. a live delivery socket.  A conveyor on a socket facing
                  any other way delivers nothing and is not a feeder.
            free  no building at all (a builder bot standing there does not
                  count -- `is_tile_empty` ignores bodies, and the engine's own
                  can_build_* is what finally decides).
            mine  one of OUR buildings that is not a feeder (our own fill brick
                  or a mis-faced belt) -- this is the self-fill spend census.
            foe   an enemy building: the blockade itself.
            aimed (deep only) FREE sockets that one of our conveyors is already
                  pointing into -- a dead feeder whose line is otherwise
                  intact, so re-laying it restores income the same round.
            hfed  (deep only) FREE sockets orthogonally adjacent to one of our
                  harvesters -- a complete second delivery line for ONE
                  conveyor, because a harvester feeds any adjacent acceptor.

        Memoised per round per unit: the Core calls it once, and a builder may
        reach it from both the fill arm and the rebuild arm in one turn.
        """
        rnd = ct.get_current_round()
        if self.sg_scan_rnd == rnd and (self.sg_scan_deep or not deep):
            return self.sg_scan
        core = self.core
        mw, mh = self.mw, self.mh
        corexy = core_tiles_xy(core)
        feed, free, mine, foe, aimed, hfed = set(), set(), set(), set(), set(), set()
        for i in range(8):
            dx, dy = SG_SOCKET_DELTAS[i]
            tx, ty = core.x + dx, core.y + dy
            if not (0 <= tx < mw and 0 <= ty < mh):
                continue
            t = Position(tx, ty)
            try:
                bid = ct.get_tile_building_id(t)
                if bid is None:
                    # No building.  A WALL is the one other thing that can make
                    # a socket unusable and it is impassable with no building
                    # on it, so this single test separates the two.
                    if ct.is_tile_passable(t):
                        free.add(i)
                    continue
                if ct.get_team(bid) != self.team:
                    foe.add(i)
                    continue
                et = ct.get_entity_type(bid)
            except Exception:
                continue
            if et == EntityType.CONVEYOR:
                try:
                    odx, ody = DELTA[ct.get_direction(bid)]
                except Exception:
                    mine.add(i)
                    continue
                if (tx + odx, ty + ody) in corexy:
                    feed.add(i)
                else:
                    mine.add(i)
            else:
                mine.add(i)
        if deep:
            for i in free:
                dx, dy = SG_SOCKET_DELTAS[i]
                tx, ty = core.x + dx, core.y + dy
                for ndx, ndy in CARD_DELTAS:
                    nx, ny = tx + ndx, ty + ndy
                    if not (0 <= nx < mw and 0 <= ny < mh):
                        continue
                    if (nx, ny) in corexy:
                        continue
                    try:
                        bid = ct.get_tile_building_id(Position(nx, ny))
                        if bid is None or ct.get_team(bid) != self.team:
                            continue
                        et = ct.get_entity_type(bid)
                    except Exception:
                        continue
                    if et == EntityType.HARVESTER:
                        hfed.add(i)
                    elif et == EntityType.CONVEYOR:
                        try:
                            odx, ody = DELTA[ct.get_direction(bid)]
                        except Exception:
                            continue
                        if nx + odx == tx and ny + ody == ty:
                            aimed.add(i)
        self.sg_scan = (feed, free, mine, foe, aimed, hfed)
        self.sg_scan_rnd = rnd
        self.sg_scan_deep = deep
        return self.sg_scan

    def _sg_request_bits(self, ct):
        """CORE ONLY.  The socket request, pre-shifted for slot 9 bits 28-31.

        FOUR BITS, THREE MEANINGS, because the field has two consumers with
        very different costs and conflating them cost a measured game:

            0      stand down: SG_FEED_WANT faces already hold a live feeder.
            1-8    an ACTIONABLE socket, index+1 in the fixed eight-tile order
                   (which is why `SG_SOCKET_DELTAS` may never be permuted).
                   Actionable means one of our belts already points into it (a
                   dead feeder, restored the same round a conveyor lands) or
                   one of our harvesters already touches it (a whole second
                   line for one conveyor).  A body may WALK to this.
            9-12   a face index + 9: "face v-9 has no feeder, route a chain
                   there".  A ROUTING HINT ONLY.  No body walks to it and no
                   body builds on it, because a conveyor on a socket with
                   nothing feeding it costs 3 Ti and +1% scale forever and
                   delivers nothing -- and in the opening EVERY face is unfed,
                   so a walkable request would recall the whole economy onto
                   the doorstep for the first twenty rounds of every game.

        The Core is the only unit that can run this honestly -- its own eight
        sockets are permanently inside its vision and inside nobody else's --
        and it is already the sole writer of this slot every round, so the
        field costs no new store traffic at all (DOCTRINE 6).
        """
        if not (SG_ON and (SG_FEEDER_REBUILD or SG_TWO_FEEDERS)):
            return 0
        if self.core is None or not (self.mw and self.mh):
            return 0
        if self._cpu_exhausted(ct):
            # Re-publish last round's answer rather than 0: a request that
            # flickers off for one round would drop a body's walk budget and
            # un-bias a trunk plan mid-route for no reason.
            return self.sg_req_bits
        self._sg_terrain(ct)
        feed, free, mine, foe, aimed, hfed = self._sg_socket_scan(ct, deep=True)
        faces = set()
        for i in feed:
            faces.add(SG_SOCKET_FACE[i])
        if len(faces) >= SG_FEED_WANT:
            self.sg_req_bits = 0
            return 0
        if not free:
            self.sg_req_bits = 0
            return 0
        keep = self._sg_keep_idx()
        rnd = ct.get_current_round()
        stub_ok = SG_STUB_ON and rnd <= SG_STUB_RND
        best, bkey = None, None
        for i in free:
            # 1. a line of ours already points into it: re-laying restores
            #    income this round.  2. a harvester of ours already touches it:
            #    one conveyor completes a whole second line.  Anything else is
            #    not actionable and falls through to the routing hint below.
            if i in aimed:
                r0 = 0
            elif stub_ok and i in hfed:
                r0 = 1
            else:
                continue
            r1 = 0 if SG_SOCKET_FACE[i] not in faces else 1
            r2 = 0 if i in keep else 1
            key = (r0, r1, r2, i)
            if bkey is None or key < bkey:
                best, bkey = i, key
        if best is not None:
            self.sg_req_bits = (best + 1) << SG_FEED_SHIFT
            return self.sg_req_bits
        # ROUTING HINT.  The best face with no feeder and at least one free
        # socket: prefer a face holding one of the planner's own reserved
        # delivery seats, then the lowest face index for stability -- a hint
        # that flips between two faces every round re-plans every trunk.
        #
        # NEVER BEFORE THE FIRST FEEDER, and this is a MEASURED defect, not a
        # precaution: glacierkeep is 9 conveyors from the nearest ore, and
        # biasing the FIRST chain onto a chosen face cost enough extra links
        # that the bank hit 2 Ti at turn 31 with the line still unconnected --
        # 23 conveyors laid, 0 titanium delivered, 0/2 games, against leap6's
        # 15 conveyors, connected turn 61, 2/2.  Before we are plugged in
        # anywhere the objective is the SHORTEST route to ANY socket, which is
        # exactly what the unbiased incumbent router already computes.  Arm 1a
        # is about the SECOND chain and now it can only ever see the second.
        if not SG_TWO_FEEDERS or not feed:
            self.sg_req_bits = 0
            return 0
        bestf, bfkey = None, None
        for i in free:
            f = SG_SOCKET_FACE[i]
            if f in faces:
                continue
            key = (0 if i in keep else 1, f)
            if bfkey is None or key < bfkey:
                bestf, bfkey = f, key
        if bestf is None:
            self.sg_req_bits = 0
            return 0
        self.sg_req_bits = (9 + bestf) << SG_FEED_SHIFT
        return self.sg_req_bits

    def _sg_req_raw(self, ct):
        """The raw 4-bit request word.  0 when SG is off or unreadable."""
        if not (SG_ON and (SG_FEEDER_REBUILD or SG_TWO_FEEDERS)):
            return 0
        if self.core is None:
            return 0
        try:
            return (ct.read_store(SLOT_HEAL_BUDGET) >> SG_FEED_SHIFT) & SG_FEED_MASK
        except Exception:
            return 0

    def _sg_req_socket(self, ct):
        """The ACTIONABLE socket (values 1-8) as a tile, or None.

        This is the only form a body may spend an action or a move on.
        """
        v = self._sg_req_raw(ct)
        if v < 1 or v > 8:
            return None
        return sg_socket(self.core, v - 1)

    def _sg_req_goals(self, ct):
        """The request as a set of (x, y) trunk-chain goals, or None.

        An actionable socket is one goal; a face hint is the two sockets of
        that face.  Routing only -- nothing here is built or walked to.
        """
        v = self._sg_req_raw(ct)
        if v < 1:
            return None
        o = self.core
        if v <= 8:
            t = sg_socket(o, v - 1)
            return ((t.x, t.y),)
        if v > 12:
            return None
        f = v - 9
        out = []
        for i in range(8):
            if SG_SOCKET_FACE[i] == f:
                t = sg_socket(o, i)
                out.append((t.x, t.y))
        return tuple(out)

    def _sg_aimed_at(self, ct, t):
        """Is one of OUR conveyors already outputting into tile `t`?"""
        for ndx, ndy in CARD_DELTAS:
            nx, ny = t.x + ndx, t.y + ndy
            if not (0 <= nx < self.mw and 0 <= ny < self.mh):
                continue
            try:
                bid = ct.get_tile_building_id(Position(nx, ny))
                if bid is None or ct.get_team(bid) != self.team:
                    continue
                if ct.get_entity_type(bid) != EntityType.CONVEYOR:
                    continue
                odx, ody = DELTA[ct.get_direction(bid)]
            except Exception:
                continue
            if nx + odx == t.x and ny + ody == t.y:
                return True
        return False

    def _sg_harv_at(self, ct, t):
        """Is one of OUR harvesters orthogonally adjacent to tile `t`?

        A harvester pushes its 10-stack into ANY orthogonally adjacent building
        that accepts (engine_mechanics A), so one conveyor on `t` facing the
        Core is a complete, independent delivery line.
        """
        for ndx, ndy in CARD_DELTAS:
            nx, ny = t.x + ndx, t.y + ndy
            if not (0 <= nx < self.mw and 0 <= ny < self.mh):
                continue
            try:
                bid = ct.get_tile_building_id(Position(nx, ny))
                if bid is None or ct.get_team(bid) != self.team:
                    continue
                if ct.get_entity_type(bid) == EntityType.HARVESTER:
                    return True
            except Exception:
                continue
        return False

    def _sg_rebuild(self, ct):
        """ARM 3 / ARM 1b.  Re-lay the requested delivery socket.  Action.

        Ranked at the TOP of the economy: their barriers land 1-5 rounds after
        the feeder dies, and a conveyor whose output tile is empty ground holds
        its stack forever and blocks everything upstream -- so a dead feeder is
        not a slower economy, it is no economy, and the tile is contested.
        """
        if not (SG_ON and SG_FEEDER_REBUILD) or self.core is None:
            return False
        r = self._sg_req_socket(ct)
        if r is None:
            return False
        p = ct.get_position()
        if abs(p.x - r.x) + abs(p.y - r.y) != 1:
            return False
        if self.link_queue and (self.link_queue[0].x, self.link_queue[0].y) == (r.x, r.y):
            return False        # the incumbent trunk planner owns this tile
        if not self._eco_spendable(ct, ct.get_conveyor_cost()):
            return False
        # NO DEAD STUBS.  A conveyor on a socket with nothing feeding it costs
        # 3 Ti and +1% team cost scale FOREVER and delivers nothing, and in the
        # opening the Core is asking for a socket every single round because it
        # has no feeders yet.  So the request is a TARGET, and this is the
        # evidence: build only where a line of ours already points in (a dead
        # feeder, restored the same round) or where a harvester of ours already
        # touches the tile (a whole second line, for one conveyor).
        rebuild = self._sg_aimed_at(ct, r)
        if not rebuild and not (SG_STUB_ON
                                and ct.get_current_round() <= SG_STUB_RND
                                and self._sg_harv_at(ct, r)):
            return False
        f = nearest_cardinal(r.direction_to(nearest_core_tile(r, self.core)))
        if f == Direction.CENTRE:
            return False
        try:
            if not ct.can_build_conveyor(r, f):
                return False
            ct.build_conveyor(r, f)
        except Exception:
            return False
        self._sg_mark(ct, "rebuild" if rebuild else "feeder2", r)
        return True

    def _sg_rebuild_walk(self, ct):
        """ARM 3, the move half.  Step toward the requested socket.  True =
        the move was spent.

        THREE HARD BOUNDS, because recalling the economy on a latch once
        finished a measured game with 0 titanium delivered:
          * only a body ALREADY within SG_REBUILD_BAND_DSQ of our own Core;
          * never a body carrying a trunk chain (the same chain guard PLANK
            REPAIR uses) -- that body is BUILDING the economy right now;
          * at most SG_REBUILD_WALK_RNDS rounds of walking per request, per
            body, after which this body gives up on that socket for good.
        """
        if not (SG_ON and SG_FEEDER_REBUILD) or self.core is None:
            return False
        if self.link_queue:
            return False
        if ct.read_store(SLOT_HARVESTERS) < 1:
            return False        # nothing has ever delivered: no line to restore
        r = self._sg_req_socket(ct)
        if r is None:
            self.sg_walk_key = None
            return False
        key = (r.x, r.y)
        if self.sg_walk_key != key:
            self.sg_walk_key = key
            self.sg_walk_left = SG_REBUILD_WALK_RNDS
        # A per-request budget alone is not a bound: the request can move
        # between sockets and re-arm it.  The LIFETIME cap is the real one.
        if self.sg_walk_left <= 0 or self.sg_walk_total >= SG_REBUILD_WALK_CAP:
            return False
        p = ct.get_position()
        if abs(p.x - r.x) + abs(p.y - r.y) <= 1:
            return False                      # adjacent already, or standing on it
        if p.distance_squared(self.core) > SG_REBUILD_BAND_DSQ:
            return False
        self.sg_walk_left -= 1
        self.sg_walk_total += 1
        self.tgt = r
        self._nav(ct, pave=False)
        return True

    def _sg_fill(self, ct):
        """ARM 2.  One of our own 3-Ti bricks onto a socket we will not use.

        Nothing can be built on an occupied tile, so this is the only measure
        here that makes the blockade IMPOSSIBLE rather than contested.  It is
        also the one that cuts both ways: the eight sockets are our eight heal
        seats and 8 of our 12 spawn tiles, so SG_FILL_FREE_MIN is a hard floor
        on how many stay open, the reserved delivery seats and the Core's live
        request are never bricked, and the window closes at SG_FILL_MAX_RND.
        """
        if not (SG_ON and SG_SELF_FILL) or self.core is None:
            return False
        # WAVE 22, ARM A1.  OPENING.md 4.3 rule 1 again, from the other side: a
        # BARRIER on our own socket blocks our own delivery and destroys the
        # heal seat, and the top five put three of them on their own sockets in
        # 300 sides.  The seal ceiling this arm was buying is bought instead by
        # the two CONVEYORS the prefill lays, which are termini AND seats.
        if OPEN_ON:
            return False
        if self.sg_fill_n >= SG_FILL_MAX_PER_UNIT:
            return False
        rnd = ct.get_current_round()
        if rnd < SG_FILL_MIN_RND or rnd > SG_FILL_MAX_RND:
            return False
        p = ct.get_position()
        if dsq_core(p, self.core) > 4:
            return False                      # not standing beside the ring
        cost = ct.get_barrier_cost()
        if ct.get_global_resources() < cost + SG_FILL_TI_FLOOR:
            return False
        feed, free, mine, foe, aimed, hfed = self._sg_socket_scan(ct, deep=True)
        # NEVER BEFORE WE ARE PLUGGED IN.  MEASURED DEFECT, nordkap seed 2: this
        # arm bricked sockets 2, 5 and 6 on turns 9/17/18 while the trunk was
        # still three conveyors from the ring, the chain then had nowhere to
        # terminate, and the game finished with 0 titanium delivered and the
        # feeder count never leaving zero.  A brick on the tile our own line is
        # walking toward is the enemy's attack, executed by us, for free.  One
        # live feeder is the proof that the line landed somewhere.
        if not feed:
            return False
        # TEAM-WIDE SPEND CAP, censused rather than counted: the bricks that
        # are standing ARE the ledger, so a store slot cannot go stale and a
        # brick the enemy shoots out is re-bought at most SG_FILL_MAX_PER_UNIT
        # times by any one body.  Priced at the BASE 3 Ti so the cap means the
        # same thing at every cost scale.
        if len(mine) * 3 >= SG_FILL_TI_CAP:
            return False
        keep = self._sg_keep_idx()
        req = self._sg_req_socket(ct)
        reqi = -1 if req is None else sg_socket_index(self.core, req.x, req.y)
        fed_faces = set()
        for i in feed:
            fed_faces.add(SG_SOCKET_FACE[i])
        free_per_face = {}
        for i in free:
            f = SG_SOCKET_FACE[i]
            free_per_face[f] = free_per_face.get(f, 0) + 1
        # RING-WIDE OPENNESS.  Everything free that is not already spoken for
        # -- this is the pool of heal seats and spawn tiles a brick spends, and
        # SG_FILL_FREE_MIN is the floor under it.  Measured ring-wide on
        # purpose: the eligibility rule below is much narrower, and applying
        # the floor to the narrow set would silently cap the arm at one brick.
        openable = [i for i in free if i not in keep and i != reqi]
        if len(openable) - 1 < SG_FILL_FREE_MIN:
            return False
        # ONE FACE, THE ONE THEY ARRIVE ON.  MEASURED, 12 paired games: with the
        # whole ring eligible this arm laid 1.17 bricks/game and our OWN live
        # feeder count fell from leap6's 2.76 to 2.13 -- it was taking sockets
        # our own later chains would have plugged into, which is the enemy's
        # attack executed by us, for free.  The blockade arrives from THEIR
        # side and so does every ferry hop, so the two sockets of the face
        # nearest their Core are the ones worth 3 Ti and the ones our chains
        # want least.  Caps the whole arm at 2 bricks / 6 Ti as a side effect.
        E = self.enemy
        eface = None
        if SG_FILL_ENEMY_FACE_ONLY and E is not None:
            bf, bfk = None, None
            for f in (0, 1, 2, 3):
                d = 0
                for i in range(8):
                    if SG_SOCKET_FACE[i] == f:
                        d += dsq_core(sg_socket(self.core, i), E)
                if bfk is None or d < bfk:
                    bf, bfk = f, d
            eface = bf
        spare = []
        for i in openable:
            f = SG_SOCKET_FACE[i]
            if eface is not None and f != eface:
                continue
            # A tile one of our own belts already points into, or that one of
            # our harvesters already touches, is a delivery socket waiting to
            # happen -- never brick it.
            if i in aimed or i in hfed:
                continue
            # Never take the LAST free socket of a face that has no feeder:
            # that is the second face arm 1 is trying to open.
            if f not in fed_faces and free_per_face.get(f, 0) <= 1:
                continue
            spare.append(i)
        if not spare:
            return False
        if E is not None:
            spare.sort(key=lambda i: (dsq_core(sg_socket(self.core, i), E), i))
        for i in spare:
            t = sg_socket(self.core, i)
            if abs(t.x - p.x) + abs(t.y - p.y) != 1:
                continue
            try:
                if not ct.can_build_barrier(t):
                    continue
                ct.build_barrier(t)
            except Exception:
                continue
            self.sg_fill_n += 1
            self._sg_mark(ct, "fill", t)
            return True
        return False

    def _sg_s3_fresh(self, ct, rnd):
        """The detector's S3 signal: an enemy builder seen within d<=8 of our
        Core inside the last SG_S3_FRESH rounds.

        Read, not re-derived: slot 13 bits 10-19 already carry `round+1` of the
        last S3 sighting, written by ANY unit that saw one (main._arch_note),
        so a launcher or a defender that has seen nothing itself still gets the
        Core's eyes for free.  0 means never seen.
        """
        if not ARCH_ON:
            return False
        try:
            it = (ct.read_store(SLOT_ARCH_SEEN) >> 10) & 0x3FF
        except Exception:
            return False
        return bool(it) and (rnd + 1) - it <= SG_S3_FRESH

    # ------------------------------------------------------------------
    # PLANK REPAIR (P1) -- see the block at the end of doctrine.py
    # ------------------------------------------------------------------

    def _rep_mark(self, ct, tag, tile, hp=None, dedupe=True):
        """One replay line per event.  Transitions only, never per round.

        The heal of a single conveyor under a 300-round grind is ONE event as
        far as a decode is concerned, so it is de-duplicated per (tag, tile)
        per body; a relay is a genuine purchase and is not.  The set is capped
        so a pathological game cannot grow it without bound.
        """
        if not (REPAIR_ON and REPAIR_LOG):
            return
        if dedupe:
            key = (tag, tile.x, tile.y)
            if key in self.rep_marked:
                return
            if len(self.rep_marked) >= REPAIR_MARK_MAX:
                return
            self.rep_marked.add(key)
        elif self.rep_marks_n >= REPAIR_MARK_MAX:
            return
        self.rep_marks_n += 1
        if hp is None:
            print("REP %s (%d,%d)" % (tag, tile.x, tile.y))
        else:
            print("REP %s (%d,%d) hp=%d" % (tag, tile.x, tile.y, hp))

    def _rep_hurt(self, ct, tile, rnd, min_dmg=None):
        """Current HP when `tile` holds one of OUR damaged pipeline buildings.

        None otherwise.  Ordered cheapest gate first: ours, a pipeline type,
        deep enough to be worth a round, and on our own half of the board.
        Every lookup is inside vision by construction at the call sites, but
        `get_tile_building_id` raises on anything else, so it is wrapped.
        """
        try:
            bid = ct.get_tile_building_id(tile)
            if bid is None or ct.get_team(bid) != self.team:
                return None
            if ct.get_entity_type(bid) not in REPAIR_TYPES:
                return None
            hp = ct.get_hp(bid)
            gap = ct.get_max_hp(bid) - hp
        except Exception:
            return None
        if min_dmg is None:
            min_dmg = 1 if rnd >= REPAIR_LATE_RND else REPAIR_MIN_DMG
        if gap < min_dmg:
            return None
        if (
            REPAIR_OWN_HALF_ONLY and self.enemy is not None and self.core is not None
            and tile.distance_squared(self.core) > tile.distance_squared(self.enemy)
        ):
            return None
        return hp

    def _rep_crew(self, ct, rnd):
        """Whether this body may spend its round on the economy's health.

        A raider is admitted only inside our own home band: it is walking
        through the farm either way, and a body standing there is not the body
        arriving anywhere.  Outside the band LOKI-QUIET's evidence stands and
        the answer is no.
        """
        if not REPAIR_ON or self.core is None:
            return False
        if rnd < REPAIR_MIN_RND:
            return False
        if self.role == "raid":
            if not REPAIR_RAIDERS_ON:
                return False
            try:
                return dsq_core(ct.get_position(), self.core) <= REPAIR_RAID_HOME_DSQ
            except Exception:
                return False
        if self.role == "defend":
            return REPAIR_DEFENDER_ON
        return True

    def _rep_min_dmg(self, rnd):
        """How deep a wound has to be before this body stops for it."""
        if self.role == "raid":
            return REPAIR_RAID_MIN_DMG
        return 1 if rnd >= REPAIR_LATE_RND else REPAIR_MIN_DMG

    def _rep_watch(self, ct, rnd):
        """Remember tiles where one of OUR belts stood and now does not.

        The engine gives a bot tiles, not death events, so "destroyed" has to
        be inferred: a tile that held our conveyor when this body last looked,
        is inside its vision NOW, and is no longer holding it.  The vision test
        is what makes it evidence rather than a guess -- a belt that merely
        walked out of sight fails it and is never recorded.

        This is the whole difference between relaying a SEVERED trunk and
        extending a DEAD HEAD, and the audit says it is the whole plank: 23 of
        23 ungated two-wide relays were dead heads (see doctrine.py).
        """
        cur = set()
        try:
            for bid in ct.get_nearby_buildings():
                if ct.get_team(bid) != self.team:
                    continue
                if ct.get_entity_type(bid) not in BELT_TYPES:
                    continue
                bp = ct.get_position(bid)
                cur.add((bp.x, bp.y))
        except Exception:
            return
        for key in self.rep_seen:
            if key in cur or len(self.rep_lost) >= REPAIR_LOST_MAX:
                continue
            try:
                if not ct.is_in_vision(Position(key[0], key[1])):
                    continue
            except Exception:
                continue
            self.rep_lost[key] = rnd
            # The severance itself is worth a line: it is the event this plank
            # exists for, and counting it off a replay is how "the opener never
            # fired" gets told apart from "the opener never had a chance".
            self._rep_mark(ct, "lost", Position(key[0], key[1]))
        self.rep_seen = cur

    def _rep_tick(self, ct):
        """True if this body spent its turn keeping the economy alive.

        Called from `_builder` ABOVE the role split and BELOW the emergency
        Core heal and PLANK SAP: a bleeding trunk outranks laying more trunk,
        and nothing outranks the Core or the turret that is shelling it.
        """
        if not REPAIR_ON:
            return False
        rnd = ct.get_current_round()
        if not self._rep_crew(ct, rnd):
            return False
        if ct.get_global_resources() < REPAIR_TI_FLOOR:
            return False
        if self._cpu_exhausted(ct):
            return False
        p = ct.get_position()
        # SAP_CHAIN_GUARD, applied to the same failure: an abandoned chain is a
        # dead end that delivers nothing at all (`_wire_tick`).  A DETOUR is
        # abandonment; a one-round heal is not, so the two get different
        # guards -- the heal is refused only when the next link tile is in
        # reach and the round would otherwise have laid it.  A body refused
        # here still gets turbo7's chain medic, ranked below the chain, from
        # inside `_expand`.
        may_walk = True
        if REPAIR_CHAIN_GUARD and self.link_queue:
            may_walk = False
            nxt = self.link_queue[0]
            if REPAIR_CHAIN_STRICT or abs(p.x - nxt.x) + abs(p.y - nxt.y) <= 1:
                return False
        if ct.get_action_cooldown() == 0:
            px, py = p.x, p.y
            min_dmg = self._rep_min_dmg(rnd)
            for dx, dy in CARD_DELTAS:
                tx, ty = px + dx, py + dy
                if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                    continue
                t = Position(tx, ty)
                hp = self._rep_hurt(ct, t, rnd, min_dmg)
                if hp is None:
                    continue
                try:
                    if not ct.can_heal(t):
                        continue
                    ct.heal(t)
                except Exception:
                    continue
                self._rep_mark(ct, "heal", t, hp)
                return True
            # The hole rule is otherwise reachable only from `_expand`, so the
            # home defender -- the body that stands where the trunk terminates
            # -- never ran it.  Same gates, same rule, one more caller.
            if (REPAIR_REBUILD_ON and REPAIR_DEFENDER_REBUILD
                    and self.role == "defend" and self._l4_repair(ct)):
                return True
        if not may_walk or REPAIR_DETOUR <= 0 or self.role != "expand":
            return False
        if ct.get_move_cooldown() != 0:
            return False
        tgt = self._rep_detour_target(ct, rnd)
        if tgt is None:
            return False
        # `_nav` steers on self.tgt and the eco loop owns that field, so it is
        # borrowed for one call and put back: a repair detour must not survive
        # into the ore picker as a stale objective.
        keep = self.tgt
        self.tgt = tgt
        self._nav(ct, pave=False)
        self.tgt = keep
        try:
            return ct.get_move_cooldown() != 0
        except Exception:
            return True

    def _rep_detour_target(self, ct, rnd):
        """A standable tile beside the nearest damaged trunk building.

        None when there is nothing worth walking to.  Commitment is time-boxed
        and expiry BANS the tile: loki_cage's decode is a builder that
        oscillated four tiles from its objective for sixty rounds while the
        economy finished the game on ten titanium.
        """
        p = ct.get_position()
        cur = self.rep_tgt
        if cur is not None:
            if rnd - self.rep_since > REPAIR_WALK_RNDS:
                if len(self.rep_ban) > 16:
                    self.rep_ban = {k: v for k, v in self.rep_ban.items() if v > rnd}
                self.rep_ban[(cur.x, cur.y)] = rnd + REPAIR_WALK_BAN
                self.rep_tgt = None
                cur = None
            elif self._rep_hurt(ct, cur, rnd) is None:
                # Healed, destroyed, or walked out of vision.  All three mean
                # "stop", and none of them is worth remembering.
                self.rep_tgt = None
                cur = None
        if cur is None:
            best, best_d = None, None
            for bid in ct.get_nearby_buildings():
                try:
                    if ct.get_team(bid) != self.team:
                        continue
                    if ct.get_entity_type(bid) not in REPAIR_TYPES:
                        continue
                    if ct.get_max_hp(bid) - ct.get_hp(bid) < REPAIR_DETOUR_MIN_DMG:
                        continue
                    bp = ct.get_position(bid)
                except Exception:
                    continue
                d = abs(bp.x - p.x) + abs(bp.y - p.y)
                # d <= 1 is the adjacent case and belongs to the heal branch;
                # walking is only ever the answer for something out of reach.
                if d < 2 or d > REPAIR_DETOUR:
                    continue
                until = self.rep_ban.get((bp.x, bp.y))
                if until is not None and rnd < until:
                    continue
                if (
                    REPAIR_OWN_HALF_ONLY and self.enemy is not None
                    and bp.distance_squared(self.core) > bp.distance_squared(self.enemy)
                ):
                    continue
                if best_d is None or d < best_d:
                    best, best_d = bp, d
            if best is None:
                return None
            self.rep_tgt = best
            self.rep_since = rnd
            cur = best
            self._rep_mark(ct, "walk", best)
        # Approach an orthogonal neighbour, never the building's own tile: a
        # heal is d^2 == 1 and a building tile is not standable anyway.
        seat, seat_key = None, None
        grid = self.map_grid
        for dx, dy in CARD_DELTAS:
            qx, qy = cur.x + dx, cur.y + dy
            if not (0 <= qx < self.mw and 0 <= qy < self.mh):
                continue
            if grid is not None and grid[qy][qx] == "#":
                continue
            key = abs(qx - p.x) + abs(qy - p.y)
            if seat_key is None or key < seat_key:
                seat, seat_key = Position(qx, qy), key
        return seat

    def _rep_gap2(self, ct, ban):
        """Open a TWO-wide hole in a chain, which `_l4_repair` refuses.

        The rule is the inherited one with one tile of slack.  For an empty
        tile G beside this builder we require

            an ACCEPTOR beside G -- our Core, or our conveyor whose output
                                    tile is not G (identical to `_l4_repair`);
            an EMPTY tile E beside G, E != the acceptor, itself pave-legal,
                                    with a FEEDER beside E -- our conveyor
                                    aimed at E, or a starved harvester.

        We lay G facing the acceptor.  That turns the two-wide hole into a
        one-wide hole (E, now with a feeder on one side and G on the other)
        which the inherited rule closes on a later turn, so this method never
        has to know about E again.  Every safety property of the parent rule
        survives: chain is required on BOTH ends, so it cannot walk; and the
        build removes its own precondition, so it cannot repeat.  A three-wide
        gap has no such E and is left alone -- that is a trench, not a hole,
        and re-laying it tile by tile is PIECE F's pave trail, measured off.

        Two gates the parent does not have, both from the first smoke game:
        the plank's round floor (before it, an unfinished chain looks exactly
        like a severed one -- 5 of 8 opens landed before r14 while the opening
        trunk was still being laid) and a hard per-body ceiling on relays.
        """
        if ct.get_current_round() < REPAIR_MIN_RND:
            return False
        if self.rep_gap2_n >= REPAIR_GAP2_MAX:
            return False
        if REPAIR_GAP2_SEEN_ONLY and not self.rep_lost:
            return False
        p = ct.get_position()
        px, py = p.x, p.y
        for gdx, gdy in CARD_DELTAS:
            ggx, ggy = px + gdx, py + gdy
            if not (0 <= ggx < self.mw and 0 <= ggy < self.mh):
                continue
            # A tile this body watched one of our belts DIE on -- the whole
            # difference between relaying a severed trunk and extending a dead
            # head (0 of 23 ungated relays were the former; doctrine.py).
            if REPAIR_GAP2_SEEN_ONLY and (ggx, ggy) not in self.rep_lost:
                continue
            g = Position(ggx, ggy)
            if (
                LOKI_L4_OWN_HALF_ONLY and self.enemy is not None
                and g.distance_squared(self.core) > g.distance_squared(self.enemy)
            ):
                continue
            try:
                if not ct.is_tile_empty(g):
                    continue
            except Exception:
                continue
            if pave_blocked(ct, g, ban):
                continue
            acc_dir, acc_key = None, None
            holes = []
            for ni in (0, 1, 2, 3):
                ndx, ndy = CARD_DELTAS[ni]
                tx, ty = ggx + ndx, ggy + ndy
                if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                    continue
                t = Position(tx, ty)
                try:
                    bid = ct.get_tile_building_id(t)
                except Exception:
                    continue
                if bid is None:
                    # Candidate second half of the hole.  Terrain is checked
                    # here so the feeder scan below never runs on a wall.
                    try:
                        if not ct.is_tile_empty(t):
                            continue
                    except Exception:
                        continue
                    if pave_blocked(ct, t, ban):
                        continue
                    holes.append(t)
                    continue
                try:
                    if ct.get_team(bid) != self.team:
                        continue
                    et = ct.get_entity_type(bid)
                except Exception:
                    continue
                if et == EntityType.CORE:
                    if acc_key is None or acc_key > (0, 0):
                        acc_dir, acc_key = CARDINALS[ni], (0, 0)
                elif et == EntityType.CONVEYOR:
                    try:
                        odx, ody = DELTA[ct.get_direction(bid)]
                    except Exception:
                        continue
                    if tx + odx == ggx and ty + ody == ggy:
                        # A feeder aimed straight at G makes this a ONE-wide
                        # hole, which is the parent rule's business, not ours.
                        acc_dir = None
                        holes = []
                        break
                    key = (1, dist_core(t, self.core))
                    if acc_key is None or key < acc_key:
                        acc_dir, acc_key = CARDINALS[ni], key
            if acc_dir is None or not holes:
                continue
            if not any(self._rep_fed(ct, e, g) for e in holes):
                continue
            try:
                if not ct.can_build_conveyor(g, acc_dir):
                    continue
                ct.build_conveyor(g, acc_dir)
            except Exception:
                continue
            self.rep_gap2_n += 1
            self.rep_lost.pop((ggx, ggy), None)
            self._rep_mark(ct, "rebuild2", g, dedupe=False)
            return True
        return False

    def _rep_fed(self, ct, e, skip):
        """True when empty tile `e` has a feeder on a side other than `skip`.

        Same definition of "feeder" as `_l4_repair`: our conveyor whose output
        tile is `e`, or a harvester with no route home at all.  A harvester
        that still has an acceptor is not starved and a second route buys it
        nothing -- 36 of 55 repairs on the first build of that plank were
        exactly that error.
        """
        ex, ey = e.x, e.y
        for dx, dy in CARD_DELTAS:
            tx, ty = ex + dx, ey + dy
            if tx == skip.x and ty == skip.y:
                continue
            if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                continue
            t = Position(tx, ty)
            try:
                bid = ct.get_tile_building_id(t)
                if bid is None or ct.get_team(bid) != self.team:
                    continue
                et = ct.get_entity_type(bid)
            except Exception:
                continue
            if et == EntityType.HARVESTER:
                if self._l4_harvester_starved(ct, t, e):
                    return True
            elif et == EntityType.CONVEYOR:
                try:
                    odx, ody = DELTA[ct.get_direction(bid)]
                except Exception:
                    continue
                if tx + odx == ex and ty + ody == ey:
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
            # LOKI-TURBO: the partition is a pure function of (map ores, our
            # Core, this unit's seat) and none of the three ever changes, but
            # LOKI re-sorted every ore on the map on every call -- ~40 keys on
            # midgard, each building a tuple.  Cached; `ore_cursor` still walks
            # it exactly as before.
            key = (self.core, self.role_n)
            assigned = self._pick_assigned
            if self._pick_key != key or assigned is None:
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
                self._pick_assigned = assigned
                self._pick_key = key
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

    # ======================================================================
    # HAND-MERGED BLOCK (builder s46, 2026-08-16) -- TURBO x BODYAWARE.
    #
    # The two parents both REWROTE `_bfs_direction`, so this is the one
    # function where they collide and the only place either tree was touched:
    #   * TURBO      bots/_x3r0v152/eco.py:1123-1282
    #                padded flat byte-grid, border-as-bounds-test, one
    #                bytearray for wall/seen/goal, up-front-only CPU probe,
    #                NAV_NODE_BUDGET node cap.
    #   * BODYAWARE  bots/_v242bodyaware/eco.py:809-907   (tag "BODYAWARE (#63)")
    #                two-pass flood: pass 0 treats builder-bot BODIES of
    #                EITHER team as soft obstacles, pass 1 drops them and runs
    #                ONLY if pass 0 exhausted without reaching a goal --
    #                "a body can move, a wall cannot".
    #
    # HOW BODIES ENTER THE FLAT GRID: the entity scan writes hard blockers
    # straight into `base` (TURBO's per-call copy of the static template) and
    # collects builder-bot tiles into a separate flat-index list `bodies`.
    # Each pass copies `base` -- ~1 KB, the same copy TURBO already paid once
    # -- and pass 0 additionally stamps `st[bi] = 1` for every body index, so
    # "OR the body array into the blocked test" costs one store per body
    # rather than a second subscript in the inner loop.  A list of indices is
    # used instead of a parallel bytearray because bodies are O(units) and a
    # second full-grid array would cost more to allocate than it saves.
    #
    # PORTED INTO leap6 (2026-08-17) VERBATIM from bots/mate_sleipnir/eco.py
    # -- leap5's `_bfs_direction` was byte-identical to TURBO's, so this is a
    # whole-function swap, not a merge.  ONE deviation from Sleipnir: the
    # BUILDER_BOT branch below is gated on LOKI_BODYAWARE_ON so the plank can
    # be ablated (Sleipnir ships it ungated and unflagged).  Flag ON == the
    # Sleipnir source below character-for-character; flag OFF == leap5.
    # ======================================================================

    def _bfs_direction(self, ct, target):
        """One exact static-terrain step toward target, visible units avoided.

        TURBO's grid, BODYAWARE's semantics.  Same blocked set, same three
        goal cases, same neighbour ordering (target-biased, mirrored on
        `self.idx & 1`), same first-step tie-break, same fallbacks to
        `cardinal_direction_to` -- run over the padded flat grid instead of
        over tuple sets.  The state byte is 0 = free, 1 = blocked or already
        seen, 2 = goal, which collapses LOKI's `key in seen or key in blocked`
        plus `key in goals` into one subscript.  Goals are never blocked by
        construction (all three branches filter on the blocked state), and a
        goal can never be reached twice because the first neighbour that lands
        on one returns, so the three states cannot collide.

        BODYAWARE (#63) adds the pass structure: the goal set itself is
        recomputed per pass, because whether the target tile is "blocked"
        depends on whether a body counts -- exactly as in the parent, where
        `goals` is derived from `blk` inside the pass loop.

        BOTH passes are charged to ONE NAV_NODE_BUDGET (`nodes` lives outside
        the loop), and the CPU probe stays up-front-only: it is asked once,
        immediately before the FIRST flood this call performs, never per pass
        and never mid-flood.
        """
        p = ct.get_position()
        if self.map_grid is None:
            return p.cardinal_direction_to(target)
        mw, mh = self.mw, self.mh
        tx, ty = target.x, target.y
        if not (0 <= tx < mw and 0 <= ty < mh):
            # An off-map target is never blocked, so LOKI took the single-goal
            # branch and then flooded the entire map hunting a tile the bounds
            # test forbids it to expand into, before falling through to the
            # greedy step.  Under BODYAWARE it did that TWICE.  Same answer,
            # without either flood.
            return p.cardinal_direction_to(target)

        w2, tpl = self._nav_template()
        base = bytearray(tpl)
        bodies = []                                # BODYAWARE (#63)
        try:
            me = ct.get_id()
            for eid in ct.get_nearby_entities():
                if eid == me:
                    continue
                et = ct.get_entity_type(eid)
                ep = ct.get_position(eid)
                if et == EntityType.CORE:
                    for cx, cy in core_tiles_xy(ep):
                        if 0 <= cx < mw and 0 <= cy < mh:
                            base[(cy + 1) * w2 + cx + 1] = 1
                elif et == EntityType.BUILDER_BOT and LOKI_BODYAWARE_ON:
                    # BODYAWARE (#63).  GATED FOR ABLATION (leap6 only --
                    # Sleipnir ships this branch ungated).  With the flag
                    # OFF this branch is dead, BUILDER_BOT falls through to
                    # the BFS_BLOCKING_TYPES test (which does not contain
                    # it, exactly as in the parent), `bodies` stays empty,
                    # pass 1 breaks out immediately and the `continue`s land
                    # on the same greedy fallback the parent returned -- so
                    # flag-off is leap5's single-pass semantics exactly.
                    ex, ey = ep.x, ep.y
                    if 0 <= ex < mw and 0 <= ey < mh:
                        bodies.append((ey + 1) * w2 + ex + 1)   # both teams
                elif et in BFS_BLOCKING_TYPES:
                    ex, ey = ep.x, ep.y
                    if 0 <= ex < mw and 0 <= ey < mh:
                        base[(ey + 1) * w2 + ex + 1] = 1
        except Exception:
            pass

        start = (p.y + 1) * w2 + p.x + 1
        base[start] = 0                     # LOKI: blocked.discard(start)
        if bodies:                          # LOKI: bodies.discard(start)
            bodies = [bi for bi in bodies if bi != start]

        # BODYAWARE (#63): pure code motion -- desired/side/order depend only
        # on p, target, self.idx and CARDINALS, never on blocked/bodies/goals,
        # so they are hoisted out of the pass loop.
        desired = p.cardinal_direction_to(target)
        if desired in CARDINALS:
            i = CARDINALS.index(desired)
            side = 1 if (self.idx & 1) else -1
            oi = (i, (i + side) % 4, (i - side) % 4, CARD_OPPOSITE[i])
        else:
            oi = (0, 1, 2, 3)
        flat = (-w2, 1, w2, -1)             # CARDINALS order: N, E, S, W
        d0, d1, d2, d3 = flat[oi[0]], flat[oi[1]], flat[oi[2]], flat[oi[3]]

        tidx = (ty + 1) * w2 + tx + 1
        nodes = 0                           # ONE budget across BOTH passes
        cpu_checked = False
        for _pass in (0, 1):                # BODYAWARE (#63)
            if _pass == 1 and not bodies:
                break        # no bodies -> pass 0 WAS today's search
            st = bytearray(base)
            if _pass == 0:
                for bi in bodies:           # BODYAWARE (#63): blk = blocked|bodies
                    st[bi] = 1

            goals = []
            if st[tidx] == 0:
                goals.append(tidx)
            elif target == self.core or target == self.enemy:
                for cx, cy in core_tiles_xy(target):
                    for dx, dy in CARD_DELTAS:
                        qx, qy = cx + dx, cy + dy
                        if not (0 <= qx < mw and 0 <= qy < mh):
                            continue
                        if tx <= qx <= tx + 1 and ty <= qy <= ty + 1:
                            continue                      # dist_core(qpos) == 0
                        gi = (qy + 1) * w2 + qx + 1
                        if st[gi] == 0:
                            goals.append(gi)
            else:
                for dx, dy in CARD_DELTAS:
                    qx, qy = tx + dx, ty + dy
                    if not (0 <= qx < mw and 0 <= qy < mh):
                        continue
                    gi = (qy + 1) * w2 + qx + 1
                    if st[gi] == 0:
                        goals.append(gi)
            if start in goals:
                return Direction.CENTRE
            if not goals:
                continue                    # BODYAWARE (#63): retry body-free
            for gi in goals:
                st[gi] = 2
            st[start] = 1                   # LOKI: seen = {start}

            # LOKI probed the CPU clock every 64 expansions and degraded to a
            # greedy step when it was already over budget.  Time is frozen
            # inside the sandbox (engine_mechanics.md M) so that clock is the
            # ONLY one, and the whole flood now costs less than the budget
            # slice the probe was protecting -- so it is asked once, up front,
            # which preserves the degradation for a unit that arrives here
            # already spent.  `cpu_checked` keeps "once" meaning once per
            # CALL, not once per pass.
            if not cpu_checked:
                cpu_checked = True
                if self._cpu_exhausted(ct):
                    return p.cardinal_direction_to(target)

            # A frontier list per BFS level, in discovery order, is the same
            # order a single FIFO queue produces -- and `cf` carries LOKI's
            # `first`, the step this branch of the flood started with.
            cur = []
            cf = []
            for j in (0, 1, 2, 3):
                n = start + flat[oi[j]]
                v = st[n]
                if v == 0:
                    st[n] = 1
                    cur.append(n)
                    cf.append(j)
                elif v == 2:
                    return CARDINALS[oi[j]]
            nodes += len(cur)
            while cur:
                nxt = []
                nf = []
                for k in range(len(cur)):
                    node = cur[k]
                    f = cf[k]
                    n = node + d0
                    v = st[n]
                    if v == 0:
                        st[n] = 1
                        nxt.append(n)
                        nf.append(f)
                    elif v == 2:
                        return CARDINALS[oi[f]]
                    n = node + d1
                    v = st[n]
                    if v == 0:
                        st[n] = 1
                        nxt.append(n)
                        nf.append(f)
                    elif v == 2:
                        return CARDINALS[oi[f]]
                    n = node + d2
                    v = st[n]
                    if v == 0:
                        st[n] = 1
                        nxt.append(n)
                        nf.append(f)
                    elif v == 2:
                        return CARDINALS[oi[f]]
                    n = node + d3
                    v = st[n]
                    if v == 0:
                        st[n] = 1
                        nxt.append(n)
                        nf.append(f)
                    elif v == 2:
                        return CARDINALS[oi[f]]
                nodes += len(nxt)
                if nodes > NAV_NODE_BUDGET:
                    return p.cardinal_direction_to(target)
                cur = nxt
                cf = nf
            continue                        # BODYAWARE (#63): retry body-free
        return p.cardinal_direction_to(target)

    # ---- end hand-merged block (TURBO x BODYAWARE) ------------------------

    def _nav(self, ct, pave=True):
        if self.tgt is None or ct.get_move_cooldown() != 0:
            return
        # T5 PLANK Z bookkeeping.  A builder that TRIED to walk and was blocked
        # HAS made a movement decision, so the zero-idle pass must not call
        # this again in the same turn -- a second failed _nav increments
        # self.stuck twice, and `_raid` reads exactly that counter to decide a
        # station is unreachable (it bans the station for 120 rounds and pauses
        # the raider after three).  One line, and it is the difference between
        # a fallback and a corrupted stall detector.
        self.t5_nav_rnd = ct.get_current_round()
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
        ndx, ndy = DELTA[d]
        if not (0 <= p0.x + ndx < self.mw and 0 <= p0.y + ndy < self.mh):
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
        bx, by = bpos.x, bpos.y
        for dx, dy in CARD_DELTAS:
            nx, ny = bx + dx, by + dy
            if not (0 <= nx < self.mw and 0 <= ny < self.mh):
                continue
            n = Position(nx, ny)
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
        # WAVE 22 ARM A5, ARM 3.  The r960 freeze switches the trunk chain,
        # `_l4_repair` and the chain medic off for the last forty rounds --
        # written for the `harvesters` and `titanium_stored` tiebreaks, NEITHER
        # OF WHICH HAS EVER FIRED in 450 games (tiebreak.md 1).  The one that
        # does fire counts deliveries, and a severed trunk delivers nothing at
        # all (engine_mechanics.md B), so under END the last forty rounds are
        # played like the four hundred before them.
        if endgame and END_ON and END_KEEP_DELIVER_ON and self._end_fired(ct):
            endgame = False

        if ct.get_action_cooldown() == 0:
            # PLANK SOCKET-GUARD arm 3.  THE TOP ECONOMY PRIORITY, above even
            # the armed same-stop build: a dead delivery socket is not a slower
            # economy, it is NO economy (a conveyor whose output tile is empty
            # ground holds its stack forever and blocks the whole line), and
            # the tile is contested -- their barrier lands 1-5 rounds after the
            # feeder dies.  Refuses itself unless the tile will actually
            # deliver, so it costs nothing on a healthy game.
            if SG_ON and SG_FEEDER_REBUILD and self._sg_rebuild(ct):
                return
            # LOKI-SAMESTOP (QUEUE #50): the armed second build takes top
            # priority -- it is a same-round-cost-free opportunity that was
            # already committed to last round, and it must land BEFORE any
            # move (research #50 cut, step 3b).
            if self.samestop_pending is not None and self._samestop_fire(ct):
                return
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
                px, py = p.x, p.y
                for ddx, ddy in DIR_DELTAS:
                    bx, by = px + ddx, py + ddy
                    if seat_ban is not None and (bx, by) in seat_ban:
                        continue
                    if not (0 <= bx < self.mw and 0 <= by < self.mh):
                        continue
                    bp = Position(bx, by)
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
            # PLANK SPLIT arms C and B.  Ranked directly ABOVE the trunk
            # repair and directly BELOW the planned chain, and the ranking is
            # the same argument SG arm 3 makes about sockets: a fork whose
            # second socket is still empty is not a slower economy, it is the
            # single-socket economy it was supposed to replace -- the splitter
            # skips the dead output and nothing at all was bought.  Finishing
            # it is therefore worth more than relaying a link somewhere else in
            # the chain, and worth less than laying the chain itself.  Every
            # arm inside is a no-op unless this body is standing beside one of
            # our own four Core corners or beside a socket a fork points at, so
            # on a healthy game this line costs one distance test.
            if not endgame and SPLIT_ON and self._sp_fork(ct):
                return
            # TRUNK REPAIR (LOKI-L4).  Ranked below the planned chain and below
            # the harvester bootstrap -- both of those are the economy being
            # BUILT and this is the economy being kept -- and above the medic,
            # because a hole delivers nothing at all while a damaged link still
            # delivers.  It is an eco action and it sits in the eco path: the
            # raid, the seal and the forward sentinel never see it.
            if not endgame and self._l4_repair(ct):
                return
            # PLANK SOCKET-GUARD arm 2.  Below everything that BUILDS or KEEPS
            # the economy and above the medic: a brick on a socket we will
            # never use denies the blockade permanently for 3 Ti, but it also
            # spends one of our own heal seats, so it may never pre-empt a
            # conveyor.  Self-limiting: a short window, a team-wide titanium
            # cap censused off the bricks that are standing, and a hard floor
            # on how many sockets stay open.
            if not endgame and SG_ON and SG_SELF_FILL and self._sg_fill(ct):
                return
            # WAVE 22 TRACK 3, PLANK RING -- THE CLAIM, in exactly the slot
            # the line above occupies and for exactly its reason: below
            # everything that BUILDS or KEEPS the economy (the planned chain,
            # the harvester bootstrap, the fork, the trunk repair) and above
            # the medic.  The difference from `SG_SELF_FILL` is WHAT is laid --
            # our own CONVEYOR facing into the core, never a barrier -- which
            # is why this one can take the whole ring where that one was capped
            # at the enemy face: a socket carrying our conveyor stays passable,
            # stays a heal seat, and becomes a delivery terminus (OPENING.md 4).
            if not endgame and RING_ON and self._ring_claim(
                    ct, ct.get_current_round()):
                return
            # CHAIN MEDIC.  ~70% of damage to our economy was enemy builder
            # melee, and every cleared tile was relaid at 3 Ti plus +1% team
            # cost scale per relay.  Healing costs no scale at all.
            rnd_now = ct.get_current_round()
            medic_late = rnd_now >= MEDIC_MIN_RND
            # WAVE 22 ARM A5, ARM 4.  A heal is 1 Ti and costs no cost scale;
            # a relay is 3 Ti and +1 % scale for ever, and a belt that dies
            # takes its whole line's income with it.  A 20-Ti floor in front of
            # a 1-Ti action is a floor that only ever binds in the games where
            # the pipeline is the last thing we own.
            medic_floor = MEDIC_TI_FLOOR
            if END_ON and END_MEDIC_ON and self._end_fired(ct):
                medic_floor = END_MEDIC_TI_FLOOR
            if not endgame and ct.get_global_resources() >= medic_floor and (
                medic_late
                or (MEDIC_EARLY_ON and rnd_now >= MEDIC_EARLY_MIN_RND)
            ):
                for mdx, mdy in CARD_DELTAS:
                    bx, by = p.x + mdx, p.y + mdy
                    if not (0 <= bx < self.mw and 0 <= by < self.mh):
                        continue
                    bp = Position(bx, by)
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
        # sign.
        #
        # T4 SEAT-1 ADMISSION.  `role_n >= 2` leaves exactly ONE eligible body
        # in a six-builder game -- seat 0 raids, seats 1-3 expand but seat 3
        # defects to the raid at harv >= ECO_NEED, seat 4 defends -- so the
        # convergence is a one-healer plan against a two-turret siege.  Seat 1
        # owns the trunk chain and recalling it early once finished a game with
        # 0 titanium delivered, so it is admitted only past T4_SEAT1_MIN_DMG:
        # four Sentinel shots, which is past any opening poke and still inside
        # the window where heal/damage >= 0.94 saves the Core.
        min_seat = 2
        if (T4_CONVERGE_SEAT1_ON and T4_BLEED_BEACON_ON
                and (ct.read_store(SLOT_HEAL_BUDGET) & ARCH_BLEED_MASK) >= T4_SEAT1_MIN_DMG):
            min_seat = 1
        if self.role_n >= min_seat and ct.read_store(SLOT_UNDER) != 0 and self._core_shelled(ct):
            self.converging = True
            if ct.get_move_cooldown() == 0 and not adjacent_to_core(p, self.core):
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
        # WAVE 22, ARM A1 -- THE MOVE HALF OF THE OPENING, ranked above every
        # other walk in the economy because all three of these are the schedule
        # itself: reach the diagonal that owns this body's socket, step OUT
        # along its own finished line (conveyors are passable and stacks pass
        # under bodies -- engine G, N.10), and finally STATION on the filled
        # socket, which is the heal wall the twin-battery arithmetic in
        # OPENING.md 4.4 is priced on.  Every one of them refuses itself in one
        # test on a body that does not own a line.
        if OPEN_ON:
            op_rnd = ct.get_current_round()
            if self._op_prefill_walk(ct, op_rnd):
                return
            if self._op_trunk_walk(ct, op_rnd):
                return
            if self._op_station(ct, op_rnd):
                return
        # PLANK SOCKET-GUARD arm 3, the move half.  A body already near home
        # and NOT carrying a trunk chain walks to the socket the Core is
        # asking for.  Three bounds (band, chain guard, per-request walk
        # budget) live in the method; the point of the ranking is only that it
        # beats wandering off to the next ore patch.
        if SG_ON and SG_FEEDER_REBUILD and self._sg_rebuild_walk(ct):
            return
        # WAVE 22 TRACK 3, PLANK RING -- THE MOVE HALF, ranked above every
        # other walk in the economy and below every build, because both walks
        # are bounded three ways (a body already inside the home band, never
        # one carrying a trunk chain, and a per-target plus shared LIFETIME
        # cap on rounds diverted) and both refuse themselves outright when the
        # bank cannot fund what they are walking toward.  Those are the same
        # three bounds SG arm 3's walk carries, and they exist for the same
        # measured reason: recalling the economy on a latch once finished a
        # game with 0 titanium delivered.  EVICT before CLAIM -- a socket
        # already under one of their buildings is income we have lost, a free
        # socket is only income we might lose.
        if RING_ON:
            ring_rnd = ct.get_current_round()
            if self._ring_evict_walk(ct, ring_rnd):
                return
            if self._ring_claim_walk(ct, ring_rnd):
                return
        # ORE STEP-OFF: builds are adjacent-only and never own-tile, so a
        # builder parked ON ore is the one unit that can never mine it.
        try:
            on_ore = ct.get_tile_env(p) == Environment.ORE_TITANIUM
        except Exception:
            on_ore = False
        if len(self.map_walls) >= ORE_STEPOFF_MIN_WALLS and on_ore:
            for si in (0, 1, 2, 3):
                sdx, sdy = CARD_DELTAS[si]
                nx, ny = p.x + sdx, p.y + sdy
                if not (0 <= nx < self.mw and 0 <= ny < self.mh):
                    continue
                d = CARDINALS[si]
                n = Position(nx, ny)
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
        for odx, ody in DIR_DELTAS:
            bx, by = p.x + odx, p.y + ody
            if 0 <= bx < self.mw and 0 <= by < self.mh:
                bp = Position(bx, by)
                try:
                    if ct.get_tile_env(bp) == Environment.ORE_TITANIUM \
                            and ct.get_tile_building_id(bp) is None:
                        self.tgt = bp
                        break
                except Exception:
                    continue
        # LOKI-SAMESTOP (QUEUE #50) STOP-TILE PREFERENCE.  self.tgt is an
        # ore tile at this point (from _pick or the short-circuit above);
        # steer onto the trunk route's own plan[0] instead of an arbitrary
        # neighbour of the ore, so the harvester build and the same-stop
        # conveyor build line up (research #50 cut, step 3a). A PREFERENCE
        # only: if it does not apply or nothing better is found, self.tgt
        # stays the ore tile and navigation is exactly the parent's.
        if LOKI_SAMESTOP_ON and self.tgt is not None:
            try:
                is_ore = ct.get_tile_env(self.tgt) == Environment.ORE_TITANIUM
            except Exception:
                is_ore = False
            if is_ore:
                stand = self._samestop_stand_pref(ct, self.tgt)
                if stand is not None and (stand.x, stand.y) != (p.x, p.y):
                    self.tgt = stand
        self._nav(ct, pave=allow_pave)
