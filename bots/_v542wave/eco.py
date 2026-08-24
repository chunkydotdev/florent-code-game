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
import sys   # ⛔ v528: eco.py did NOT import sys, and that is exactly how
             # v526's WALK tape came out empty while looking healthy -- the
             # `print(..., file=sys.stderr)` raised NameError inside a bare
             # `except Exception: pass`.  Inert with FS_V528_LOG = False.
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


# ⭐ v534 MAPTRUST.
#
# ⛔ THERE IS DELIBERATELY NO MEMO HERE, AND THE FIRST DRAFT OF THIS FIX HAD
# ONE.  It cached "grids definitively refuted" under the key (w, h, our
# anchor), on the argument that terrain is static so a refutation can never
# un-happen.  That argument is correct about a BOARD and wrong about a KEY:
# (w, h, anchor) is exactly the thing this whole build exists because it does
# not identify a map.  `test_f2.py` caught it on the one FS_MAP_SKIP map that
# is IN THE CURRENT POOL -- playing snowflake refuted archipelago's grid under
# the shared (26,26,(5,5)) key, and the next archipelago board in the same
# process then verified against an empty candidate set and came back unknown,
# silently turning archipelago's skip OFF.  A cache keyed on a colliding
# signature reintroduces the collision bug inside the collision fix.
#
# WITHOUT THE MEMO THE COST STILL SITS IN THE RIGHT PLACE, because the loop
# EXITS the moment the last candidate dies: a board that does not match is
# rejected after the first disagreeing tile, and the full sweep is paid only
# when it SUCCEEDS -- once per unit, after which the caller caches the grid and
# stops asking.  Re-verifying on every ask is also what buys opportunistic
# re-verification as a unit's vision widens, for free.


def _maptrust_pick(candidates, w, h, own, ct):
    """v534 F1 -- adopt a catalogued grid only if VISIBLE terrain confirms it.

    Replaces the parent's two unverified adoptions:
      * `len(candidates) == 1` short-circuited straight to the stored grid
        with ZERO terrain checks, so any unseen map colliding on
        (width, height, core anchor) with a catalogued singleton silently
        corrupted map_walls/map_ores/pathing for the whole match;
      * the >=2 path returned the CLOSER stored grid, never None, so a
        colliding map still adopted whichever catalogue entry it resembled
        least badly.
    Both now return None on mismatch, which every caller already routes to the
    live-sensing fallback (main.py's map_grid stays None and the ore scan /
    spiral search run; siege's v524 confirmation reads "unknown" and does not
    cripple).
    """
    if ct is None:
        # No controller, no terrain, no trust.  (Unreachable in this tree --
        # all three call sites pass ct -- kept explicit rather than falling
        # back to the unverified adoption this fix exists to remove.)
        return None
    live = candidates
    try:
        tiles = ct.get_nearby_tiles()
    except Exception:
        return None
    seen = 0
    for tile in tiles:
        x, y = tile.x, tile.y
        # ⛔ EXPLICIT BOUNDS TEST.  `get_nearby_tiles` is documented in-bounds,
        # but `is_in_vision` was documented as a bounds guard too (s50 probe)
        # and is not; an off-map index here would raise out of run() and
        # destroy the unit permanently.
        if x < 0 or y < 0 or x >= w or y >= h:
            continue
        try:
            env = ct.get_tile_env(tile)
        except Exception:
            continue
        char = "#" if env == Environment.WALL else ("o" if env == Environment.ORE_TITANIUM else ".")
        seen += 1
        keep = [g for g in live if g[y][x] == char]
        if len(keep) == len(live):
            continue
        # A disagreement.  Only trust it if the tile carries no building --
        # cheap because it costs one engine call per MISMATCH, never per tile.
        # ⛔ WHY THE GUARD EXISTS: `get_tile_env` is documented as TERRAIN and a
        # harvester sits ON an ore tile rather than replacing it, but this
        # function is asked at ANY round by a unit whose core resolved late, and
        # a build that did change what a tile reads would otherwise refute the
        # CORRECT grid.  One engine call on the rare path buys that out.
        try:
            occupied = ct.get_tile_building_id(tile) is not None
        except Exception:
            occupied = True
        if occupied:
            continue
        live = keep
        if not live:
            return None
    if seen < FS_V534_MIN_TILES:
        # A degenerate ask (no vision yet).  Adopting on ~nothing is the very
        # thing this fix removes; the caller retries next round.
        return None
    return live[0]


def known_map_for(w, h, own, ct=None):
    candidates = []
    for (mw, mh, ax, ay, bx, by), code in tuple(MAP_CODES.items()) + EXTRA_MAP_CODES:
        if w != mw or h != mh or (own.x, own.y) not in ((ax, ay), (bx, by)):
            continue
        candidates.append(_decode_grid(code, w, h))
    if not candidates:
        return None
    if FS_V534_MAPTRUST:
        return _maptrust_pick(candidates, w, h, own, ct)
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

    def _eco_spendable(self, ct, cost, essential=False):
        """May the economy spend `cost` this round?

        ⛔⛔ v513 CHANGE C, AND IT IS THE `titanium_collected` = 0 BUG.  Two
        reserves that had never been checked against EACH OTHER deadlocked on
        one bank.  This function subtracts `8 * barrier + FS_SEAL_MARGIN` while
        the siege is live; `main.py`'s KILL-phase magazine drains the bank down
        to `8 * barrier`.  The economy's bar therefore sat EXACTLY
        FS_SEAL_MARGIN = 6 titanium above the level the Core drained to, for
        the rest of the match, and no conveyor was ever affordable again.
        MEASURED (s50 diagnostic, 9 local games): 2,653 of 2,809 eco-spend
        denials had a raw bank that covered the cost and were blocked by this
        reserve alone (94.4%); glacierkeep_g5 read `ti=56 res=62 cost=7` one
        thousand two hundred and eighty-four times and delivered 0 titanium in
        447 rounds, while the same fixture with the reserve off built 11
        harvesters, 106 links and collected 470.
        ⭐ THE FIX IS A LIFELINE, NOT A REMOVAL: above it the collar keeps its
        whole reserve (the seal really is worth more than a conveyor), below it
        the economy keeps enough to lay one link.  A reserve that cannot be
        funded protects nothing and starves everything.
        ⭐ AND `essential` IS THE SECOND HALF (autopsy #2): the ONE conveyor
        that connects the belt to our own core footprint is not ordinary eco
        spending -- `titanium_collected` is 0 without it in 11 of 11 games and
        positive in 13 of 13 with it -- so it is exempt from both reserves.
        """
        ti = ct.get_global_resources()
        if LOKI_FS_CREW and FS_BELT_LASTLINK and essential:
            return ti >= cost
        # ⭐ WAVE-LATE-SURGE (c) -- THE v513 CHANGE-C DEADLOCK, THIRD COSTUME.
        # Read the docstring above and then read the bifrost tape: with a
        # raider parked at the enemy ring the collar reserve subtracts
        # `8 * barrier + FS_SEAL_MARGIN` from a bank that reads 89 Ti against a
        # 55 Ti harvester, and `spend 0` is the standing verdict for 700
        # rounds.  Past WAVE_SURGE_RND, with the ratchet still under target,
        # the seal has had 250 rounds to land and has not; the dig outranks it
        # from here.  Bounded THREE ways: never before r250, never once the
        # ratchet reaches WAVE_SURGE_HARV_TARGET, and `ti >= cost` still holds
        # so it can only ever spend money we actually have.
        if WAVE_LATE_SURGE and WAVE_SURGE_FUND and wave_surge_short(ct):
            return ti >= cost
        # ⭐⭐ v539 RUNG A -- THE FAMINE LIFELINE, AND IT IS THE v513 CHANGE-C
        # DEADLOCK IN ITS SECOND COSTUME.  Read the docstring above: two
        # reserves that had never been checked against each other put the
        # economy's bar permanently above the bank and no conveyor was
        # affordable again for the rest of the match.  A WIPE reproduces that
        # from the other end -- the bank is drained to single digits and
        # SLOT_UNDER is latched by the very attack that drained it, so
        # `cost + SIEGE_HEAL_RESERVE_TI` is unreachable on passive income and
        # the economy that would refund the kill can never start.
        # ⛔ THE WAIVER IS NOT A REMOVAL.  `ti >= cost` still holds, so this
        # can only ever spend income the wipe left us -- ~100 Ti over the
        # 40-round window at passive rates.  Expanders only, capped rounds,
        # capped episodes: the collar's 8-barrier reserve outlives all three.
        if (LOKI_FS_V539 and FS_V539_REEST and FS_V539_LIFELINE
                and self._v539_lifeline(ct, cost)):
            return ti >= cost
        # LOKI-FERRY-SIEGE: while a raider is standing at the enemy ring, the
        # titanium the collar still needs is not the economy's to spend.  Eight
        # barriers is the whole heal set and it is the cheapest decisive
        # purchase on the board; a conveyor bought instead of it costs the seal.
        if LOKI_FERRY_SIEGE_ON and FS_COLLAR_RESERVE_ON:
            try:
                v = ct.read_store(SLOT_FS)
                ph = (v >> FS_PHASE_SHIFT) & FS_PHASE_MASK
                beat = v & FS_BEAT_MASK
                if (FS_PH_RING <= ph <= FS_PH_KILL and beat
                        and ct.get_current_round() - (beat - 1) <= FS_BEAT_STALE):
                    res = 8 * ct.get_barrier_cost() + FS_SEAL_MARGIN
                    if LOKI_FS_CREW and FS_BELT_LASTLINK:
                        ti = max(min(ti, FS_ECO_LIFELINE), ti - res)
                    else:
                        ti -= res
            except Exception:
                pass
        if (
            SIEGE_RESERVE_ON
            and ct.read_store(SLOT_UNDER) != 0
            and ct.get_current_round() >= HUNT_MIN_RND
        ):
            return ti >= cost + SIEGE_HEAL_RESERVE_TI
        return ti >= cost

    def _eco_cap(self, ct):
        # ⭐ WAVE-LATE-SURGE (d).  The incumbent surge asks for 1,500 Ti in the
        # bank; the measured stalled-rush bank on bifrost never clears 900 and
        # sits at 80-250 for most of the match, so the ceiling it guards has
        # never once been raised in that class of game.  Same ceiling, same
        # flag, on a floor a stalled rush can actually reach.  Cannot fire
        # before WAVE_SURGE_RND, so r<250 returns the parent's value.
        if (WAVE_LATE_SURGE and wave_surge_on(ct)
                and ct.get_global_resources() >= WAVE_SURGE_TI_FLOOR):
            return SURGE_ECO_CAP
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

    # --- LOKI-V537 "SOCKET": pre-claim our own delivery seat ---------------
    # See the LOKI-V537 block at the bottom of doctrine.py for the measured
    # defect.  One sentence of it: on the two pool maps whose nearest ore is
    # 10-11 tiles away, `_link_path` plans ore-end-first so our own Core seat
    # is the LAST tile of the trunk (r23 / r230), and Mjolnir's collar barrier
    # lands on it at r13-r16.  This makes it the FIRST tile instead.

    def _v537_side(self, s):
        """Which side of the 2x2 Core footprint a ring seat sits on.

        Seats are the 8 orthogonal neighbours, two per side.  Returned as a
        small int so `FS_V537_SIDE_SPREAD` can refuse a second claim beside
        the first: a conveyor is 20 HP against a 2-damage peck, so two seats
        on one side are one demolition job, not two.
        """
        o = self.core
        if s.y == o.y - 1:
            return 0                                   # north
        if s.y == o.y + 2:
            return 2                                   # south
        if s.x == o.x - 1:
            return 3                                   # west
        return 1                                       # east

    def _v537_seat_pool(self):
        """The seats a claim may take, in the trunk planner's own preference.

        `delivery_seats` is what `_seat_ban` would reserve, so claiming from
        it puts our conveyor exactly where the trunk wants to terminate.
        ⛔ Computed FRESH here rather than through `self._seat_ban()`, which
        MEMOISES on first call: calling it at r1 would freeze `seat_ban` /
        `seat_keep` to whatever ore knowledge this body happens to have and
        change downstream behaviour that has nothing to do with this plank.
        """
        if self.core is None or not (self.mw and self.mh):
            return []
        keep = delivery_seats(self.core, self.mw, self.mh,
                              self.map_walls, self.map_ores)
        kept = {(s.x, s.y) for s in keep}
        rest = [s for s in heal_seats(self.core, self.mw, self.mh)
                if (s.x, s.y) not in kept]
        return list(keep) + rest

    def _v537_sockets_held(self, ct, seats):
        """Our own belt buildings standing on our Core ring, RIGHT NOW.

        Re-derived from the engine on every call: no latch, no store slot.  A
        latch would keep reporting "claimed" after they shoot the conveyor off
        the seat; this self-corrects.  Bounds are tested explicitly because
        `is_in_vision` is a pure radius test and is NOT a bounds guard
        (CLAUDE.md, corrected s50) -- and a ring seat is exactly the
        near-the-edge case where that bites.
        """
        held = []
        for s in seats:
            if not (0 <= s.x < self.mw and 0 <= s.y < self.mh):
                continue
            try:
                bid = ct.get_tile_building_id(s)
                if bid is None:
                    continue
                if (ct.get_team(bid) == self.team
                        and ct.get_entity_type(bid) in BELT_TYPES):
                    held.append(s)
            except Exception:
                continue
        return held

    def _v538_claim_on(self, ct):
        """Is the v537 SOCKET CLAIM live on THIS board?

        ⭐ v538 -- THE ONE PREDICATE, and the whole of this build's change.
        The claim has exactly ONE read site (`_v537_socket_claim`, below), so
        this is asked there and nowhere else; if a second consumer ever
        appears it calls THIS, never a second copy of the test.

        The verdict is the siege's own `_fs_map_gated`, read through
        `SiegeMixin._v535_map_refuses` -- geometry and grid-confirmed
        signatures only, NO MAP NAMES (map-robustness policy F3).  `Player` is
        `(EcoMixin, RaidMixin, SiegeMixin)` (main.py), so the call resolves on
        `self` at runtime; eco.py must NOT import siege.py (siege imports eco).

        ⛔ ORDER OF THE THREE TESTS IS LOAD-BEARING.  `FS_V537_SOCKET` first,
        so a socket-off arm never reaches the gate; the v538 master second, so
        `FS_V538_CLAIM_GATE = False` returns EXACTLY `FS_V537_SOCKET` and the
        siege helper is never called at all -- that is what makes flag-off
        byte-identical to `bots/_v537socket` rather than merely equivalent.
        The `except` returns the PARENT behaviour (claim on): an unreadable
        gate must not silently delete a shipped plank.

        ⛔ ASKED INSIDE THE WINDOW, NOT AT THE RUNG.  `_v537_socket_claim`
        early-returns on `rnd > FS_V537_BY_ROUND` BEFORE calling this, so the
        gate costs at most a handful of calls per body per game and nothing at
        all after r4.  Putting it at the main.py rung would have re-asked it
        every round for 1,000 rounds, and main.py stays md5-identical to the
        parent as a side effect.
        """
        if not FS_V537_SOCKET:
            return False
        if not (LOKI_FS_V538 and FS_V538_CLAIM_GATE):
            return True
        try:
            refuses = self._v535_map_refuses(ct)
        except Exception:
            return True
        if refuses:
            self.v538_claim_gated += 1
            return False
        return True

    def _v537_socket_claim(self, ct, rnd):
        """Put one conveyor on one of our own Core delivery seats.

        Returns True if it spent this body's action this round.  Costs one
        conveyor and one builder turn, at most FS_V537_MAX_SOCKETS times, only
        inside the round window.  Never touches the enemy ring.

        ⭐ v538: gated by `_v538_claim_on` -- the claim stands down on boards
        the ferry-siege refuses.  The gate is asked AFTER the window test, so
        it is never computed outside the four rounds it can matter in.
        """
        if self.core is None or not (self.mw and self.mh):
            return False
        if rnd > FS_V537_BY_ROUND:
            return False
        if not self._v538_claim_on(ct):
            return False
        if not FS_V537_RAIDER_CLAIMS and (self.fs_raider or self.role == "raid"):
            return False
        try:
            if ct.get_action_cooldown() != 0:
                return False
            if ct.get_global_resources() < ct.get_conveyor_cost():
                return False
        except Exception:
            return False
        seats = self._v537_seat_pool()
        if not seats:
            return False
        held = self._v537_sockets_held(ct, seats)
        if len(held) >= FS_V537_MAX_SOCKETS:
            return False
        taken = {self._v537_side(s) for s in held}
        p = ct.get_position()
        for s in seats:
            if abs(p.x - s.x) + abs(p.y - s.y) != 1:
                continue                    # build needs orthogonal adjacency
            if FS_V537_SIDE_SPREAD and self._v537_side(s) in taken:
                continue
            f = nearest_cardinal(s.direction_to(nearest_core_tile(s, self.core)))
            if f == Direction.CENTRE:
                continue
            try:
                if not ct.can_build_conveyor(s, f):
                    continue
                ct.build_conveyor(s, f)
            except Exception:
                continue
            if FS_V537_LOG:
                try:
                    print("V537 SOCKET r%d seat=(%d,%d) face=%s held=%d"
                          % (rnd, s.x, s.y, f, len(held) + 1), file=sys.stderr)
                except Exception:
                    pass
            return True
        return False

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
            return ct.read_store(SLOT_HEAL_BUDGET) >= T4_BLEED_MIN
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
        for eid in ct.get_nearby_buildings():
            try:
                if ct.get_team(eid) == self.team and ct.get_entity_type(eid) == EntityType.HARVESTER:
                    live += 1
            except Exception:
                continue
        if live > ct.read_store(SLOT_HARVESTERS):
            ct.write_store(SLOT_HARVESTERS, live)
        elif (LOKI_FS_V539 and FS_V539_REEST and FS_V539_HONEST_SLOT
                and live < ct.read_store(SLOT_HARVESTERS)
                and self._v539_famine(ct)):
            # ⛔⛔ SHIPPED OFF (`FS_V539_HONEST_SLOT = False`).  This is the
            # commission's change -- make the ratchet an honest count during a
            # famine so its consumers see the truth -- built so a leg can
            # price it, NOT because the build believes it.  The enumeration in
            # the build report says it CLOSES four gates that the phantom was
            # holding open, including the r^2=32 forward SENTINEL (needs
            # `>= 2`) and the home LAUNCHER (needs `>= 1`), at exactly the
            # moment Magnus asked why no sentinel was ever bought.  It is also
            # a LOWER BOUND being written over a UNION: `live` here is one
            # builder's r^2=20 view, which is why the slot was a ratchet in
            # the first place.  Do not turn this on without a battery.
            ct.write_store(SLOT_HARVESTERS, live)
        # v514 change A: slot 5 has ONE writer (the Core) -- see FS_ECO_SLOT.
        # This write was dead in the parent (3 writes, 0 reads).
        if live >= ECO_NEED and not (LOKI_FS_V514 and FS_V514_ECOGATE):
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
            goals = {g for g in raw_goals if not blk[(g[1] + 1) * w2 + g[0] + 1]}
            if not goals:
                return []
            par = [0] * (w2 * (mh + 2))
            cur = []
            for gx, gy in goals:
                gi = (gy + 1) * w2 + gx + 1
                par[gi] = -1
                cur.append(gi)
            d0, d1, d2, d3 = -w2, 1, w2, -1          # CARDINALS order
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
                return []
            path = []
            node = start
            while par[node] != -1:
                node = par[node]
                path.append(Position(node % w2 - 1, node // w2 - 1))
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
        # ⭐ v528 -- THE ORPHANED CHAIN HEAD (v513 open item 5).  Past
        # SIPHON_WIRE_RNDS the parent assigns `self.link_queue = path` OVER a
        # live queue and every unbuilt tile of the chain in progress is
        # dropped, so the harvester THAT chain was for emits into nothing for
        # the rest of the match.  Defer instead: hold the pending item, reset
        # its clock, let the live chain drain.  A defer, not an append -- see
        # the doctrine block for why concatenating mis-faces the last link.
        # Bounded, so a chain that never drains cannot starve the queue.
        if LOKI_FS_V528 and FS_V528_WIRE and self.link_queue:
            nd = getattr(self, "_v528_wire_defer", 0) + 1
            if nd <= V528_WIRE_MAX_DEFER:
                self._v528_wire_defer = nd
                self.wire_pending[0] = (bp, ct.get_current_round())
                if FS_V528_LOG:
                    print("V528 WIRE defer %d rnd %d bp %d,%d queue %d"
                          % (nd, ct.get_current_round(), bp.x, bp.y,
                             len(self.link_queue)), file=sys.stderr)
                return
        self._v528_wire_defer = 0
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
        if not self.link_queue:
            return False
        # ⭐ v513 CHANGE C -- THE LAST LINK IS ESSENTIAL SPENDING.  Perfect
        # separation over 24 games: `titanium_collected` > 0 if and only if a
        # conveyor of ours stands beside our own core footprint, and in 8 of
        # the 11 zero games the belt stopped ONE 3-titanium link short.
        ess = False
        if LOKI_FS_CREW and FS_BELT_LASTLINK and self.core is not None:
            try:
                ess = dsq_core(self.link_queue[0], self.core) <= 2
            except Exception:
                ess = False
        if not self._eco_spendable(ct, ct.get_conveyor_cost(), essential=ess):
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
            # ⭐ WAVE-LATE-SURGE (n).  The compass answer above ignores what is
            # on that side; the decoded board has a five-link trunk whose last
            # conveyor faces a WALL.  Rank the four cardinals by what they
            # actually deliver into.  Falls through to `f` unchanged whenever
            # nothing scores better, so the parent's answer is the default and
            # not the exception.
            if WAVE_LATE_SURGE and WAVE_SURGE_ENDFACE and wave_surge_on(ct):
                f = self._wave_end_face(ct, tile, target, f)
        if f == Direction.CENTRE:
            f = Direction.NORTH
        if ct.can_build_conveyor(tile, f):
            ct.build_conveyor(tile, f)
            self.link_queue.pop(0)
            return True
        return False

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

        Splitters are never a feeder.  We build none (nothing in this tree
        calls build_splitter), and a splitter's output rotates among three
        directions, so an empty output tile is its normal state rather than
        evidence of a cut.
        """
        if not LOKI_L4_REPAIR_ON or self.core is None:
            return False
        if self._cpu_exhausted(ct):
            return False
        # ⭐ v513 CHANGE C: a hole beside OUR OWN CORE is the belt's LAST LINK
        # and it is exempt from the eco reserves (see `_eco_spendable`).  The
        # ordinary spendability answer is computed once here and re-asked per
        # candidate gap, so a repair that is NOT the terminus still obeys every
        # reserve the incumbent had.
        spend_ok = self._eco_spendable(ct, ct.get_conveyor_cost())
        lastlink = LOKI_FS_CREW and FS_BELT_LASTLINK
        if not spend_ok and not (
                lastlink
                and self._eco_spendable(ct, ct.get_conveyor_cost(),
                                        essential=True)):
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
            if not spend_ok and not (lastlink and acc_key == (0, 0)):
                continue                 # reserved bank, and this is not the
                                         # core-adjacent terminus
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

    # --- v528 M5: CONNECTION-COST ORDERING ---------------------------------
    #
    # See the doctrine.py v528 block for the marker and the argument.  Three
    # methods: the flood (`_v528_conn_field`), the per-ore read
    # (`_v528_conn_at`), and the chooser (`_v528_pick_conn`).  All three are
    # dead code with `LOKI_FS_V528 = False`, and `_v528_pick_conn` returns None
    # on any degradation so `_pick` falls back to the parent's cursor walk.

    def _v528_conn_field(self, ct):
        """0-1-2 cost flood OUT from our Core's delivery ring.

        Returns `(w2, dist)`, where `dist[i]` is the number of NEW conveyors a
        trunk chain would have to build to connect flat index `i` to the Core,
        counting a tile that already holds one of our belt pieces as free and
        charging `V528_CONN_CONTEST` extra on a contested tile.  Unreached
        tiles hold `V528_CONN_UNREACH`.  `(0, None)` on any degradation.

        ⭐ THE BLOCKED SET IS `_link_path`'s, not a new one.  Same template,
        same goal ring, same ore-is-impassable rule -- so the number this
        scorer ranks on is the number the router will actually have to build.
        """
        if self.core is None or self.map_grid is None:
            return 0, None
        rnd = ct.get_current_round()
        key = (self.core, self.mw, self.mh, rnd // V528_CONN_REFRESH)
        if getattr(self, "_v528_conn_key", None) == key:
            return self._v528_conn_w2, self._v528_conn_dist
        if self._cpu_exhausted(ct):
            # Serve whatever is cached rather than burn the turn; a stale field
            # re-orders slightly wrong, a truncated flood re-orders very wrong.
            return getattr(self, "_v528_conn_w2", 0), \
                getattr(self, "_v528_conn_dist", None)

        mw, mh = self.mw, self.mh
        w2 = mw + 2
        _, tpl, _ore_only = self._link_template()
        blk = bytearray(tpl)
        size = len(blk)
        # cost[i] = titanium-links charged for OCCUPYING tile i.
        cost = bytearray(size)          # default 0; filled to 1 below
        for i in range(size):
            if not blk[i]:
                cost[i] = 1
        ban = self._pave_ban()
        if ban is not None:
            for bx, by in ban:
                if 0 <= bx < mw and 0 <= by < mh:
                    blk[(by + 1) * w2 + bx + 1] = 1
        contest = 1 + V528_CONN_CONTEST
        # ⭐ BELT MEMORY, and without it the scorer answers the wrong question.
        # `get_nearby_buildings()` is bounded by THIS unit's vision (r^2=20),
        # so a builder out at the ore field cannot see the trunk it laid on the
        # way out -- every tile of it would be charged as if it had to be built
        # again, which biases the score AGAINST exactly the ore Magnus's marker
        # is about ("two conveyors from a quick connection" is a claim about
        # belt that ALREADY EXISTS).  So friendly belt sightings persist.
        # Staleness is bounded the only honest way: a remembered tile that is
        # currently IN VISION and no longer friendly belt is dropped.  Tiles
        # out of vision are kept -- that is a guess, and it is the same guess
        # `_link_path` makes when it routes through terrain it cannot see.
        seen = getattr(self, "_v528_belt", None)
        if seen is None:
            seen = self._v528_belt = set()
        now = set()
        try:
            for eid in ct.get_nearby_buildings():
                ep = ct.get_position(eid)
                ex, ey = ep.x, ep.y
                if not (0 <= ex < mw and 0 <= ey < mh):
                    continue
                ei = (ey + 1) * w2 + ex + 1
                et = ct.get_entity_type(eid)
                mine = ct.get_team(eid) == self.team
                if et == EntityType.CORE:
                    for cx, cy in core_tiles_xy(ep):
                        if 0 <= cx < mw and 0 <= cy < mh:
                            blk[(cy + 1) * w2 + cx + 1] = 1
                    continue
                if et in BELT_TYPES and mine:
                    now.add((ex, ey))
                    continue
                blk[ei] = 1
                seen.discard((ex, ey))
                if not mine:
                    for st in (-w2, 1, w2, -1):
                        n = ei + st
                        # Never downgrade an already-free tile to contested:
                        # an enemy standing beside our own belt does not make
                        # that belt need re-building.
                        if 0 <= n < size and not blk[n] and cost[n] == 1:
                            cost[n] = contest
        except Exception:
            pass
        try:
            for xy in list(seen):
                if xy in now:
                    continue
                if ct.is_in_vision(Position(xy[0], xy[1])):
                    seen.discard(xy)        # confirmed gone
        except Exception:
            pass
        seen |= now
        for bx, by in seen:
            if 0 <= bx < mw and 0 <= by < mh:
                bi_ = (by + 1) * w2 + bx + 1
                blk[bi_] = 0
                cost[bi_] = 0               # already built: free to route through
        try:
            for uid in ct.get_nearby_units():
                if ct.get_entity_type(uid) != EntityType.BUILDER_BOT:
                    continue
                up = ct.get_position(uid)
                if not (0 <= up.x < mw and 0 <= up.y < mh):
                    continue
                ui = (up.y + 1) * w2 + up.x + 1
                if not blk[ui] and cost[ui] != 0:
                    cost[ui] = contest
        except Exception:
            pass

        goals = self._link_goals(ban)
        inf = V528_CONN_UNREACH
        dist = [inf] * size
        nb = contest + 1
        buckets = [[] for _ in range(nb)]
        seeded = False
        for gx, gy in goals:
            if not (0 <= gx < mw and 0 <= gy < mh):
                continue
            gi = (gy + 1) * w2 + gx + 1
            if blk[gi]:
                continue
            c = cost[gi]
            if c < dist[gi]:
                dist[gi] = c
                buckets[c % nb].append(gi)
                seeded = True
        if not seeded:
            self._v528_conn_key = key
            self._v528_conn_w2 = w2
            self._v528_conn_dist = None
            return 0, None

        # Dial's algorithm.  Every edge weight is in 0..contest, so `nb`
        # buckets suffice and a zero-cost edge is re-fed into the CURRENT
        # worklist rather than a future bucket.
        dcap = (mw + mh) * contest + contest + 2
        if dcap >= inf:
            dcap = inf - 1
        nodes = 0
        budget = V528_CONN_NODE_BUDGET
        truncated = False
        for d in range(0, dcap + 1):
            bi = d % nb
            work = buckets[bi]
            if not work:
                continue
            buckets[bi] = []
            while work:
                i = work.pop()
                if dist[i] != d:
                    continue
                nodes += 1
                if nodes > budget:
                    truncated = True
                    break
                for st in (-w2, 1, w2, -1):
                    n = i + st
                    if blk[n]:
                        continue
                    nd = d + cost[n]
                    if nd < dist[n]:
                        dist[n] = nd
                        if nd == d:
                            work.append(n)
                        else:
                            buckets[nd % nb].append(n)
            if truncated:
                break
        # A truncated flood still answers correctly for every tile it settled
        # (Dial's is monotone), and everything past the frontier reads
        # UNREACH -- which is finite, so the myopia guard still holds.
        self._v528_conn_key = key
        self._v528_conn_w2 = w2
        self._v528_conn_dist = dist
        return w2, dist

    def _v528_adj_order(self, ct, p, seat_ban):
        """`DIR_DELTAS` re-ordered so the CHEAPEST-to-connect ore comes first.

        Returns None (caller keeps the parent's compass order) when the field
        is unavailable or when fewer than two adjacent ORE tiles are in play --
        with 0 or 1 ore neighbours there is nothing to order and the parent's
        sequence must be preserved exactly.  Non-ore deltas keep their original
        relative order and stay AFTER the ore ones, so the only behaviour that
        can change is which of several adjacent ORES is built on.
        """
        w2, dist = self._v528_conn_field(ct)
        if dist is None:
            return None
        px, py = p.x, p.y
        ores = []
        rest = []
        for i, (ddx, ddy) in enumerate(DIR_DELTAS):
            bx, by = px + ddx, py + ddy
            if not (0 <= bx < self.mw and 0 <= by < self.mh):
                rest.append((i, (ddx, ddy)))
                continue
            if seat_ban is not None and (bx, by) in seat_ban:
                rest.append((i, (ddx, ddy)))
                continue
            try:
                is_ore = ct.get_tile_env(Position(bx, by)) == Environment.ORE_TITANIUM
            except Exception:
                is_ore = False
            if not is_ore:
                rest.append((i, (ddx, ddy)))
                continue
            conn = self._v528_conn_at(w2, dist, Position(bx, by))
            ores.append((conn, i, (ddx, ddy)))
        if len(ores) < 2:
            return None
        ores.sort()                       # (conn, original index) -- ties keep
        return [o[2] for o in ores] + [r[1] for r in rest]

    def _v528_pickreg(self, ct, assigned, chosen):
        """PICK-TIME regret: the decision the plank actually makes.

        ⛔ WHY BUILD-TIME REGRET WAS THE WRONG PLACE, measured before any
        outcome was read: `_v528_regret` compares the ore just built against
        the cheapest ore ANYWHERE in this seat's slice, from a position already
        adjacent to the built one.  That number is nonzero even for a perfect
        chooser, because a 1-link ore twenty tiles away costs twenty rounds of
        walking to reach and the scorer is RIGHT to decline it.  It measures a
        quantity nobody is minimising.

        This measures the one that is: at the moment a target is chosen, the
        score of the CHOSEN candidate against the best score available from
        where the body stands.  Emitted from BOTH arms (gated on FS_V528_LOG
        alone), so the parent's cursor pick and v528's argmin are scored by the
        same yardstick.  v528's value is ~0 BY CONSTRUCTION and that is the
        point -- it is the check that the scorer is wired to the decision.  The
        finding is the PARENT's value.
        """
        try:
            w2, dist = self._v528_conn_field(ct)
            if dist is None:
                return
            p = ct.get_position()
            cs, cconn = self._v528_conn_score(ct, w2, dist, p, chosen)
            bs, bconn = cs, cconn
            bs_all = cs
            n = nb = 0
            # ⛔ THE BAN MUST BE EXCLUDED FROM `bs` OR THE METRIC IS UNFAIR TO
            # ITS OWN ARM.  `_v528_pick_conn` refuses a tile this body has been
            # stuck on (V528_CONN_BAN_RNDS), so scoring the chooser against a
            # best that INCLUDES that tile charges it regret for obeying its own
            # anti-lock.  Measured before this line existed: v528 read mean
            # regret 16.6 with 1339 of 1352 picks nonzero -- an artefact of the
            # ban, not of the ordering.  `bs_all` keeps the unfiltered best so
            # the ban's cost is REPORTED rather than hidden.
            rnd = ct.get_current_round()
            banned = getattr(self, "_v528_ore_ban", None) or {}
            for t in assigned:
                try:
                    if ct.is_in_vision(t) and ct.get_tile_building_id(t) is not None:
                        continue
                except Exception:
                    pass
                n += 1
                s, c = self._v528_conn_score(ct, w2, dist, p, t)
                if s < bs_all:
                    bs_all = s
                exp = banned.get((t.x, t.y))
                if exp is not None and exp > rnd:
                    nb += 1
                    continue
                if s < bs:
                    bs, bconn = s, c
            print("V528 PICK r %d id %d tgt %d,%d cs %d bs %d reg %d "
                  "cc %d bc %d cands %d banned %d regall %d seat %d"
                  % (rnd, ct.get_id(), chosen.x, chosen.y,
                     cs, bs, cs - bs, cconn, bconn, n, nb, cs - bs_all,
                     self.role_n),
                  file=sys.stderr)
        except Exception:
            return

    def _v528_regret(self, ct, bp):
        """CHOSEN-vs-BEST-AVAILABLE connection length, per harvester decision.

        The M5 verification metric.  `chosen` is the links the harvester just
        placed will need; `best` is the smallest over every ore this seat could
        still have taken (no building on it).  `regret = chosen - best` is
        therefore >= 0 by construction, and the claim under test is that the
        PARENT's regret distribution is nonzero while v528's sits at ~0.

        ⛔ It is a pure read: it never touches `self.tgt`, `ore_cursor`,
        `link_queue` or the conn cache's contents, and every engine call is
        inside the try, so a log-on arm cannot diverge from a log-off one by
        anything except stdout.
        """
        try:
            w2, dist = self._v528_conn_field(ct)
            if dist is None:
                return
            chosen = self._v528_conn_at(w2, dist, bp)
            cands = self._pick_assigned or self.map_ores or ()
            best = chosen
            n = 0
            for t in cands:
                if (t.x, t.y) == (bp.x, bp.y):
                    continue
                try:
                    if ct.is_in_vision(t) and ct.get_tile_building_id(t) is not None:
                        continue
                except Exception:
                    pass
                n += 1
                c = self._v528_conn_at(w2, dist, t)
                if c < best:
                    best = c
            print("V528 CONN r %d id %d at %d,%d chosen %d best %d regret %d "
                  "cands %d role %s seat %d"
                  % (ct.get_current_round(), ct.get_id(), bp.x, bp.y,
                     chosen, best, chosen - best, n, self.role, self.role_n),
                  file=sys.stderr)
        except Exception:
            return

    def _v528_conn_at(self, w2, dist, t):
        """Links needed to connect a harvester ON `t`.

        `_link_path` never builds on the harvester's own tile -- the first
        element of the path it returns is a CARDINAL neighbour -- so the read
        is the minimum over `t`'s four cardinal neighbours, not `dist[t]`.
        """
        ti = (t.y + 1) * w2 + t.x + 1
        best = V528_CONN_UNREACH
        for st in (-w2, 1, w2, -1):
            n = ti + st
            if 0 <= n < len(dist):
                v = dist[n]
                if v < best:
                    best = v
        return best

    def _v528_conn_score(self, ct, w2, dist, p, t):
        conn = self._v528_conn_at(w2, dist, t)
        walk = abs(p.x - t.x) + abs(p.y - t.y)
        return (V528_CONN_W_LINK * conn + V528_CONN_W_WALK * walk), conn

    def _v528_pick_conn(self, ct, assigned):
        """Best rounds-to-first-delivery among this seat's OWN candidates.

        ⛔ RE-ORDERS, NEVER TRUNCATES.  Every member of `assigned` is scored;
        an unreachable one scores `V528_CONN_UNREACH` and is still returnable.
        The only exclusions are the parent's own (a visible ore that already
        carries a building) and the stale-target ban below -- and if those
        exclude EVERYTHING, the ban is dropped rather than the candidate list.
        """
        n = len(assigned)
        if not n:
            return None
        w2, dist = self._v528_conn_field(ct)
        if dist is None:
            return None
        rnd = ct.get_current_round()
        # ANTI-LOCK.  The parent's `ore_cursor` rotates on every call, so a
        # permanently unbuildable tile is left behind for free.  A scorer is
        # deterministic and would hand back the same tile forever, which is the
        # M4 failure in a different costume: when `_expand` re-picks BECAUSE
        # this body is stuck, the tile it was stuck on is banned for a while.
        banned = getattr(self, "_v528_ore_ban", None)
        if banned is None:
            banned = self._v528_ore_ban = {}
        if self.stuck >= 5 and self.tgt is not None:
            banned[(self.tgt.x, self.tgt.y)] = rnd + V528_CONN_BAN_RNDS
        p = ct.get_position()
        best_t = None
        best_key = None
        fallback_t = None
        fallback_key = None
        scanned = 0
        start = self.ore_cursor % n
        self.ore_cursor += 1
        for k in range(n):
            t = assigned[(start + k) % n]
            try:
                if ct.is_in_vision(t) and ct.get_tile_building_id(t) is not None:
                    continue
            except Exception:
                pass
            scanned += 1
            if scanned > V528_CONN_MAX_CAND:
                break
            s, _conn = self._v528_conn_score(ct, w2, dist, p, t)
            # Tie-break on the PARENT's own key, so two candidates the new
            # score cannot separate are ordered exactly as before.
            key = (s, abs(t.x - self.core.x) + abs(t.y - self.core.y),
                   (t.x * 17 + t.y * 31) % 97)
            if fallback_key is None or key < fallback_key:
                fallback_key = key
                fallback_t = t
            exp = banned.get((t.x, t.y))
            if exp is not None:
                if exp > rnd:
                    continue
                del banned[(t.x, t.y)]
            if best_key is None or key < best_key:
                best_key = key
                best_t = t
        if best_t is not None:
            return best_t
        return fallback_t

    _WAVE_STEP_DIR = {(0, -1): Direction.NORTH, (1, 0): Direction.EAST,
                      (0, 1): Direction.SOUTH, (-1, 0): Direction.WEST}

    def _wave_end_face(self, ct, tile, target, fallback):
        """Which way the LAST conveyor of a plan should face.

        ⭐ WAVE-LATE-SURGE (n).  Rank 0 = the side already holds one of our
        belt tiles or our own core, i.e. this link actually joins something.
        Rank 1 = the side is at least passable ground a later link can use.
        The compass fallback is kept for rank 2, so a tile with no readable
        neighbour behaves exactly as the parent.  Ties break on Manhattan
        distance to the core, then on the parent's own answer.
        """
        best = None
        best_key = None
        for i, (dx, dy) in enumerate(CARD_DELTAS):
            nx, ny = tile.x + dx, tile.y + dy
            if not (0 <= nx < self.mw and 0 <= ny < self.mh):
                continue
            d = CARDINALS[i]
            n = Position(nx, ny)
            rank = 2
            try:
                if ct.get_tile_env(n) == Environment.WALL:
                    continue
                bid = ct.get_tile_building_id(n)
                if bid is not None:
                    if ct.get_team(bid) == self.team \
                            and ct.get_entity_type(bid) in ACCEPTOR_TYPES:
                        rank = 0
                    else:
                        continue
                else:
                    rank = 1
            except Exception:
                continue
            key = (rank, abs(nx - target.x) + abs(ny - target.y),
                   0 if d == fallback else 1)
            if best_key is None or key < best_key:
                best, best_key = d, key
        return fallback if best is None else best

    def _wave_step(self, ct, target):
        """One cardinal step toward `target` over the tiles the body can SEE.

        ⭐ WAVE-LATE-SURGE (j).  Used only where the tree currently has no
        pathfinding at all -- `map_grid is None`, i.e. a map the catalogue
        does not carry -- and only past WAVE_SURGE_RND.

        The flood is over `is_tile_passable`, which is the engine's own answer
        to "could a friendly builder stand there", so it accounts for walls,
        buildings AND bodies in one call.  Its goal is the reachable tile with
        the smallest Manhattan distance to `target`, not `target` itself:
        the caller's targets are ore tiles and link tiles the body must stand
        BESIDE, and an unreachable goal would otherwise return nothing at all.

        Returns None -- caller falls back to the parent's compass step -- when
        vision is unreadable, when the CPU guard has tripped, or when the best
        reachable tile is the one the body is already on.
        """
        if self._cpu_exhausted(ct):
            return None
        p = ct.get_position()
        start = (p.x, p.y)
        try:
            tiles = ct.get_nearby_tiles()
        except Exception:
            return None
        ok = set()
        for t in tiles:
            tx, ty = t.x, t.y
            if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                continue
            try:
                if ct.is_tile_passable(t):
                    ok.add((tx, ty))
            except Exception:
                continue
        if not ok:
            return None
        ok.add(start)
        gx, gy = target.x, target.y
        prev = {start: None}
        q = deque([start])
        best, best_sc = start, abs(start[0] - gx) + abs(start[1] - gy)
        while q:
            cur = q.popleft()
            for dx, dy in CARD_DELTAS:
                n = (cur[0] + dx, cur[1] + dy)
                if n in prev or n not in ok:
                    continue
                prev[n] = cur
                q.append(n)
                sc = abs(n[0] - gx) + abs(n[1] - gy)
                if sc < best_sc:
                    best, best_sc = n, sc
        if best == start:
            return None
        cur = best
        while prev[cur] != start:
            cur = prev[cur]
        return self._WAVE_STEP_DIR.get((cur[0] - p.x, cur[1] - p.y))

    def _wave_belt_rescue(self, ct):
        """Adopt the nearest dead-ended belt of ours and plan its route home.

        ⭐ WAVE-LATE-SURGE (i).  A `link_queue` is per-unit state.  When the
        body carrying one dies -- and ours die constantly in this matchup --
        its half-built belt is orphaned, and nothing in the tree ever finishes
        it: `_l4_repair` fires only for a harvester with NO acceptor, and a
        stub's first conveyor still is one.  Decoded on the wire: 12
        harvesters alive at r999, TWO connected, ten sitting on 3-to-6-link
        stubs that stop in open ground.

        A dead end is one of OUR conveyors whose output tile carries no
        building.  That test also excludes every conveyor that is delivering,
        because the tile a delivering conveyor faces holds the core, another
        belt tile, or a harvester -- all buildings.  The route is planned FROM
        THE OUTPUT TILE and the output tile is prepended, so
        `_build_next_link` lays it first and faces it at `link_queue[1]`; that
        is what makes the existing stub flow instead of leaving a belt that
        points at a conveyor which points somewhere else.
        """
        p = ct.get_position()
        best = None
        best_d = None
        try:
            ids = ct.get_nearby_buildings()
        except Exception:
            return
        for bid in ids:
            try:
                if ct.get_team(bid) != self.team:
                    continue
                if ct.get_entity_type(bid) != EntityType.CONVEYOR:
                    continue
                bp = ct.get_position(bid)
                bd = ct.get_direction(bid)
            except Exception:
                continue
            dxy = DELTA.get(bd)
            if not dxy or (dxy[0] == 0 and dxy[1] == 0):
                continue
            ox, oy = bp.x + dxy[0], bp.y + dxy[1]
            if not (0 <= ox < self.mw and 0 <= oy < self.mh):
                continue
            out = Position(ox, oy)
            try:
                if ct.get_tile_env(out) == Environment.WALL:
                    continue
                if ct.get_tile_building_id(out) is not None:
                    continue
            except Exception:
                continue
            # NEAREST THE CORE, NOT NEAREST THE BODY.  A dead end two tiles
            # from our own footprint is a whole trunk one 3-Ti link short of
            # delivering -- decoded on the final board of a 700-round game,
            # where the (1,1) harvester's chain read (2,1)v (2,2)v [GAP] (2,4)v
            # into the core and that ONE missing tile was the difference
            # between 2,430 delivered titanium and zero from that deposit.  A
            # dead end out at the map's middle needs six more links and
            # crosses ground the opponent contests.  Walk length is the
            # tiebreak.
            dc = abs(out.x - self.core.x) + abs(out.y - self.core.y)
            d = (dc, (bp.x - p.x) ** 2 + (bp.y - p.y) ** 2)
            if best_d is None or d < best_d:
                best, best_d = out, d
        if best is None:
            return
        try:
            plan = self._link_path(ct, best)
        except Exception:
            return
        if not plan and dsq_core(best, self.core) > 2:
            # No route found and the tile is not itself a delivery seat --
            # laying one conveyor into open ground buys nothing and costs
            # +1% team cost scale.
            return
        self.link_queue = [best] + list(plan)
        self.link_source = best
        self.wave_lq_len = len(self.link_queue)
        self.wave_lq_rnd = ct.get_current_round()

    def _wave_ore_target(self, ct):
        """Nearest remembered-and-still-free ore tile, or None.

        ⭐ WAVE-LATE-SURGE (a).  `known_map_for` only ever returns a grid for a
        map in the catalogue; off it, `map_ores` is empty for the whole match
        and the seat partition in `_pick` never engages.  This is the same
        idea driven by the only other source of terrain there is -- what this
        body has actually SEEN -- accumulated across rounds so a tile stays
        known after it leaves vision.

        ⛔ THE SCAN IS PAID ON A RE-PICK, NEVER PER ROUND.  `_pick` is called
        when the target is reached, cleared or gone stale; between those the
        body navigates on a cached target and this function is not entered.
        `get_tile_building_id` is asked only for tiles that read as ore, so
        the per-call engine cost is one env read per in-vision tile plus one
        building read per ore tile.

        Bounds are tested explicitly before every tile read: `get_nearby_tiles`
        is documented in-bounds, but `is_in_vision` was documented as a bounds
        guard too (s50) and is not, and an escaping GameError is a permanent
        unit death.
        """
        p = ct.get_position()
        seen = self.wave_ore_seen
        full = self.wave_ore_full
        try:
            tiles = ct.get_nearby_tiles()
        except Exception:
            tiles = ()
        for t in tiles:
            tx, ty = t.x, t.y
            if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                continue
            try:
                if ct.get_tile_env(t) != Environment.ORE_TITANIUM:
                    continue
                taken = ct.get_tile_building_id(t) is not None
            except Exception:
                continue
            seen.add((tx, ty))
            # A harvester sits ON its ore, so an occupied ore tile is one this
            # body must stop walking to.  The flag is re-read every time the
            # tile is in vision, so a destroyed harvester frees it again.
            if taken:
                full.add((tx, ty))
            else:
                full.discard((tx, ty))
        cands = [xy for xy in seen if xy not in full]
        if not cands:
            return None
        # ⭐ WAVE-LATE-SURGE (g).  ROUTE LENGTH FIRST, WALK LENGTH SECOND.
        # `titanium_collected` is credited on DELIVERY TO THE CORE, so the ore
        # worth digging is the one whose belt can be finished, not the one
        # under the body's feet.  Manhattan to the core is the link count the
        # belt will need; the walk is the tiebreak.  Coordinates close the
        # order so the choice does not depend on set iteration.
        cx, cy = (self.core.x, self.core.y) if self.core is not None else (p.x, p.y)
        cands.sort(key=lambda o: (
            WAVE_SURGE_ROUTE_W * (abs(o[0] - cx) + abs(o[1] - cy))
            + abs(o[0] - p.x) + abs(o[1] - p.y), o[0], o[1]))
        # SPREAD.  Every expander reads the same ore memory, so without this
        # they all walk to the same deposit and only one of them can build on
        # it.  The parent solved the identical problem with a static seat
        # partition (`ordered[worker::workers]`); this is the same trick with
        # the seat as the offset, capped so a high seat number cannot be sent
        # across the map.
        k = min(self.role_n % WAVE_SURGE_SPREAD, len(cands) - 1)
        ox, oy = cands[k]
        return Position(ox, oy)

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
            # ⭐ v528 M5.  The PARTITION above is untouched -- same seats, same
            # slices, so no two builders converge on a deposit that were kept
            # apart before.  Only the ORDER in which this seat visits its OWN
            # slice changes, from discovery/proximity to rounds-to-first-
            # delivery.  Returns None on any degradation (no map, CPU spent,
            # no reachable ring) and the parent's cursor walk runs unchanged.
            if LOKI_FS_V528 and FS_V528_CONNCOST:
                t = self._v528_pick_conn(ct, assigned)
                if t is not None:
                    if FS_V528_LOG:
                        self._v528_pickreg(ct, assigned, t)
                    return t
            for _ in range(len(assigned)):
                t = assigned[self.ore_cursor % len(assigned)]
                self.ore_cursor += 1
                try:
                    if ct.is_in_vision(t) and ct.get_tile_building_id(t) is not None:
                        continue
                except Exception:
                    pass
                if FS_V528_LOG:
                    self._v528_pickreg(ct, assigned, t)
                return t

        # ⭐ WAVE-LATE-SURGE (a) -- THE PARTITION, RUN OFF LIVE VISION.
        # Reached only when `map_ores` is empty, i.e. only on a map the
        # catalogue does not carry, which is the exact condition that kills
        # the partition above.  Below WAVE_SURGE_RND this is inert and the
        # parent's in-vision scan runs unchanged.
        if WAVE_LATE_SURGE and WAVE_SURGE_SEEN_ORE and wave_surge_on(ct):
            t = self._wave_ore_target(ct)
            if t is not None:
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
            # ⭐ WAVE-LATE-SURGE (j).  This line -- and only this line -- is
            # what "no map in the catalogue" costs at navigation time: a
            # greedy compass step with no obstacle test at all.  Past
            # WAVE_SURGE_RND, flood what the body can SEE instead.  Returns
            # None whenever it has nothing better to say and the parent's
            # compass step runs unchanged.
            if WAVE_LATE_SURGE and WAVE_SURGE_NAV and wave_surge_on(ct):
                d = self._wave_step(ct, target)
                if d is not None:
                    return d
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
                elif et == EntityType.BUILDER_BOT:     # BODYAWARE (#63)
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
        # ⭐ WAVE-LATE-SURGE (f) -- THE PINNED LINK QUEUE.  `_expand`'s
        # `if self.link_queue:` branch returns before the re-pick, so a body
        # holding a plan it can never lay is deleted from the economy for the
        # rest of the match.  `_build_next_link` returns False forever when
        # ANOTHER OF OUR OWN BODIES is standing on `link_queue[0]`:
        # `can_build_conveyor` refuses an occupied tile and the `occupied` pop
        # above it tests `get_tile_building_id` only, which a builder bot is
        # not.  Two of our expanders can hold each other there indefinitely.
        # The queue is dropped, not rerouted -- `_wire_tick` / the next
        # harvester will re-plan from live terrain, which is the cheaper and
        # more honest answer than patching a stale path.
        if WAVE_LATE_SURGE and wave_surge_on(ct):
            n_lq = len(self.link_queue)
            if n_lq == 0:
                self.wave_lq_len = 0
                self.wave_lq_rnd = None
            else:
                rnd_lq = ct.get_current_round()
                if n_lq != self.wave_lq_len or self.wave_lq_rnd is None:
                    self.wave_lq_len = n_lq
                    self.wave_lq_rnd = rnd_lq
                elif rnd_lq - self.wave_lq_rnd >= WAVE_SURGE_LQ_STALE:
                    self.link_queue = []
                    self.link_source = None
                    self.wave_lq_len = 0
                    self.wave_lq_rnd = None
                    self.tgt = None
                    self.stuck = 0
                    self.wall = None

        if ct.get_action_cooldown() == 0:
            # LOKI-SAMESTOP (QUEUE #50): the armed second build takes top
            # priority -- it is a same-round-cost-free opportunity that was
            # already committed to last round, and it must land BEFORE any
            # move (research #50 cut, step 3b).
            if self.samestop_pending is not None and self._samestop_fire(ct):
                return
            if not endgame and self.link_queue and self._build_next_link(ct):
                return
            # ⭐ WAVE-LATE-SURGE (m).  A body holding a live route plan does
            # not open a new hole: `_build_next_link` above returns False
            # whenever it is not adjacent to its own `link_queue[0]`, and
            # without this the fall-through builds a harvester off the walk.
            # See the doctrine note -- this is the measured
            # 12-harvesters-2-connected shape at its source.
            _wave_wire_first = (WAVE_LATE_SURGE and WAVE_SURGE_WIRE_FIRST
                                and self.link_queue and wave_surge_on(ct))
            if not _wave_wire_first and (
                ct.get_global_resources() >= ct.get_harvester_cost()
                if endgame
                else (
                    self._eco_spendable(ct, ct.get_harvester_cost())
                    and harv < self._eco_cap(ct)
                )
            ):
                seat_ban = self._seat_ban()
                px, py = p.x, p.y
                # ⭐⭐ v528 M5, AND THIS IS THE SITE THAT ACTUALLY DECIDES.
                # Re-ordering `_pick` alone re-orders the WALK TARGET; the
                # harvester that gets BUILT is whichever adjacent ore comes
                # first in `DIR_DELTAS`, i.e. compass order -- discovery order,
                # which is exactly what the mandate replaces.  Measured before
                # this clause existed: v528's own connection regret over 20
                # games was NOT ~0 (mean 0.0-86.0 per game, `connread.py`),
                # because the body walked to the cheap ore and then built on
                # whatever ore it happened to stand beside.  Same flag, same
                # plank -- ordering the ADJACENT candidates by the same
                # rounds-to-first-delivery score is the plank finishing its
                # own sentence.  Ties keep `DIR_DELTAS` order, so with one
                # candidate this is byte-identical to the parent.
                if LOKI_FS_V528 and FS_V528_CONNCOST:
                    d0 = self._v528_adj_order(ct, p, seat_ban)
                    if d0 is not None:
                        DIR_DELTAS_LOCAL = d0
                    else:
                        DIR_DELTAS_LOCAL = DIR_DELTAS
                else:
                    DIR_DELTAS_LOCAL = DIR_DELTAS
                for ddx, ddy in DIR_DELTAS_LOCAL:
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
                        # ⭐ v528 M5 INSTRUMENT -- CONNECTION REGRET, and it is
                        # gated on FS_V528_LOG ALONE, never on LOKI_FS_V528.
                        # The parent arm is measured as `LOKI_FS_V528 = False`
                        # with the log ON, so both arms emit the same tape from
                        # the same code and the comparison is not between two
                        # different instruments.
                        if FS_V528_LOG:
                            self._v528_regret(ct, bp)
                        ct.write_store(SLOT_HARVESTERS, ct.read_store(SLOT_HARVESTERS) + 1)
                        # v514 change A: slot 5 has ONE writer (the Core).
                        if ct.read_store(SLOT_HARVESTERS) >= ECO_NEED \
                                and not (LOKI_FS_V514 and FS_V514_ECOGATE):
                            ct.write_store(SLOT_ECO_READY, 1)
                        self._wire_on_build(ct, bp)
                        break
            # TRUNK REPAIR (LOKI-L4).  Ranked below the planned chain and below
            # the harvester bootstrap -- both of those are the economy being
            # BUILT and this is the economy being kept -- and above the medic,
            # because a hole delivers nothing at all while a damaged link still
            # delivers.  It is an eco action and it sits in the eco path: the
            # raid, the seal and the forward sentinel never see it.
            if not endgame and self._l4_repair(ct):
                return
            # CHAIN MEDIC.  ~70% of damage to our economy was enemy builder
            # melee, and every cleared tile was relaid at 3 Ti plus +1% team
            # cost scale per relay.  Healing costs no scale at all.
            rnd_now = ct.get_current_round()
            medic_late = rnd_now >= MEDIC_MIN_RND
            if not endgame and ct.get_global_resources() >= MEDIC_TI_FLOOR and (
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

        # ⭐ WAVE-LATE-SURGE (i) -- THE ORPHANED BELT.  Planning only: it sets
        # `link_queue` and spends no action, so it cannot displace a build, a
        # repair or a heal -- all three sit above it and return.  Duty-cycled
        # by seat so at most one body pays the unknown-map `_link_path` flood
        # in any round, and skipped outright once the CPU guard above has
        # tripped.
        if (WAVE_LATE_SURGE and WAVE_SURGE_RESCUE and not endgame
                and not self.link_queue and self.core is not None
                and wave_surge_on(ct)
                and (ct.get_current_round() % WAVE_SURGE_RESCUE_EVERY
                     == self.role_n % WAVE_SURGE_RESCUE_EVERY)):
            self._wave_belt_rescue(ct)

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
                and ct.read_store(SLOT_HEAL_BUDGET) >= T4_SEAT1_MIN_DMG):
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

        # ⭐ WAVE-LATE-SURGE (l).  THE HALF-BUILT BELT OUTRANKS THE SIPHON
        # HUNT.  `_siphon_deny` sits ABOVE the `if self.link_queue:` movement
        # branch, so a body carrying a route plan gets pulled off it to go
        # break an enemy belt -- and on this map our ore and theirs interleave
        # at x=12-15, so the hunt is always available.  Decoded symptom: a
        # body holding `lq 6 head (9,5)` spent rounds 311-375 at (12,4),
        # (13,3), (12,7), (14,4) -- east, away from its own head, which it
        # never reached.  The siphon costs the enemy half of ONE harvester's
        # output; the unfinished belt costs us ALL of ours, because
        # `titanium_collected` is credited on delivery.  Only while the plan
        # is live, only past r250, only while the ratchet is short.
        if not (WAVE_LATE_SURGE and self.link_queue and wave_surge_short(ct)) \
                and self._siphon_deny(ct):
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
        # ⭐ WAVE-LATE-SURGE (b) -- THE PACE 2-CYCLE, AND WHY `stuck` CANNOT SEE
        # IT.  `self.stuck` counts rounds on which `_nav` moved NOWHERE.  On an
        # uncatalogued map `_bfs_direction` short-circuits to a greedy
        # `cardinal_direction_to` and `_nav`'s fallback ladder ends in
        # `desired.opposite()`, so a body walled off from its target by our own
        # paved ring steps forward, is refused, and steps BACK -- a successful
        # move every round, `stuck` pinned at 0, and the `stuck >= 5` re-pick
        # below unreachable.  Measured on bifrost: 350 consecutive rounds of
        # (0,5)<->(1,5).  Two distinct tiles or fewer over the last
        # WAVE_SURGE_PACE_N recorded rounds is that shape and nothing else --
        # a body making progress fills the window with distinct tiles.
        if WAVE_LATE_SURGE and WAVE_SURGE_UNSTICK and wave_surge_on(ct):
            hist = self.wave_pace
            hist.append((p.x, p.y))
            if len(hist) == hist.maxlen and len(set(hist)) <= 2:
                self.tgt = None
                self.stuck = 0
                self.wall = None
                hist.clear()
        if self.tgt is None or p == self.tgt or self.stuck >= 5:
            self.tgt = self._pick(ct)
            self.stuck = 0
            self.wall = None
        if self.tgt is None:
            return
        # ⭐ v528 M5: the adjacent-ore OVERRIDE is discovery order too -- it
        # takes whichever ore is first around the compass.  Same score, same
        # flag; with fewer than two ore neighbours `_v528_adj_order` returns
        # None and the parent's sequence is preserved byte-for-byte.
        _ord = DIR_DELTAS
        if LOKI_FS_V528 and FS_V528_CONNCOST:
            _o = self._v528_adj_order(ct, p, None)
            if _o is not None:
                _ord = _o
        for odx, ody in _ord:
            bx, by = p.x + odx, p.y + ody
            if 0 <= bx < self.mw and 0 <= by < self.mh:
                bp = Position(bx, by)
                try:
                    if ct.get_tile_env(bp) == Environment.ORE_TITANIUM \
                            and ct.get_tile_building_id(bp) is None:
                        # ⭐ v528 M4 -- THE STALLED WALKER.  A BODY IS NOT A
                        # BUILDING.  Without this predicate the override
                        # re-targets an ore tile that one of our own parked
                        # units is standing on, every round, which pins
                        # `self.tgt` and defeats the `stuck >= 5` re-pick that
                        # just ran three lines above; `can_build_harvester` is
                        # False for as long as the body is there, so nothing
                        # ever changes.  Root-caused by v526 on
                        # `valkyrie_s1_A` id 7, (9,10), r37-r59.
                        if LOKI_FS_V528 and FS_V528_WALK:
                            if ct.get_tile_builder_bot_id(bp) is not None:
                                continue
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
