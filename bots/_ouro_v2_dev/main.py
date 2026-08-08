"""_ouro_v2_dev -- Ouroboros-class battery instrument, RE-FREEZE successor.

Implements docs/research/ouro-probe-refreeze-spec-2026-08-08.md against the
frozen `bots/ouroboros_probe` (md5 8828b5d5...). The frozen probe scored 93.3%
for candidates while the live class win rate was 7.1% -- an 86.2-point
calibration gap. This file changes WHERE the gunners go, WHO plants them and
WHEN the strike lands. It does not change how many there are.

What changed against the frozen probe
-------------------------------------
R1  HOME SCREEN. The frozen probe had one latched picket builder walking the
    whole lane (`_picket_latch`/`SLOT_PICKET_ID`) -- a single point of failure
    the wild never presents. Replaced by a band plan: every station index is
    typed HOME / MID / KILL, and each band is owned by a specific builder duty.
    Two builders are leashed to ~7 tiles of their own core and never leave; they
    plant the screen (measured wild share d>144 of the enemy core: 22.6% of 847
    sites, median lifespan 179 rounds) and heal it. The band plan reproduces the
    measured site distribution exactly over the first 31 stations:
    HOME 7/31 = 22.6%, KILL 5/31 = 16.1%, MID 19/31 = 61.3%.

R2  KILLER BURST. Wild: first gunner at d<=9 of our core at median r124, and it
    arrives as a burst (median 2 within a 12-round window; 3-in-7 and 5-in-9
    observed). The frozen probe's first core-threatening station landed r152-176
    and its burst cadence only started after r224. Here the three prefix KILL
    stations are due r124 / r127 / r130 and are all planted by ONE strike
    builder from a single anchor tile -- three orthogonal neighbours of the tile
    it is standing on, which is exactly the 3-in-7 shape and, because the anchor
    is deterministic, is also the D2 fixed-tile rebuild.

R3  TARGETING. `_pick_target` preferred a builder over the core unconditionally
    and `_run_gunner` bare-returned when its pick was not fireable, so a builder
    standing behind the core suppressed the shot entirely (modelled at 36-53% of
    core shots in the games where our heal line was staffed). Now: gunners that
    SPAWNED inside d<=13 of the enemy core rank core first (wild killers put
    65.5% of fire into the core, 8.2% into builders); every gunner walks its
    candidate list and fires the first fireable tile, with `get_gunner_target()`
    as a last-resort fallback, so a shot is never suppressed.

R4  Rotation throttle relaxed (measured wild median 2.78 per gunner, not 1.5).
R5  Opening spend: 3 builders by r2, 5 by r20, then NOTHING until the late
    replacement batch at r180+ (D6). Wild median 3 by r10, 5 by r40, 7 lifetime.

What is deliberately NOT changed
--------------------------------
The gunner mass curve. `BAND_DUE` / `CREEP_INTERVAL` / `SIEGE_INTERVAL` and the
saturation-index arithmetic are carried over verbatim; `_cadence_standoff` is
the frozen probe's `_standoff`, kept solely so `_saturation_index` -- and
therefore every due round -- is bit-identical. Cumulative planted:
2/3/4/5/9/10/19 at r25/50/75/100/150/200/300 against the wild's
2/3/4/5/8/11/18 (spec A5 tolerance +/-2). The only re-timing is the strike
burst being pulled forward; nothing is added.

Defects preserved (spec section 4) -- these are the exploit surface
------------------------------------------------------------------
D-CRITICAL  Gunners only. No sentinel, no launcher, no splitter, no barrier, and
            no answer at all to a turret planted outside gunner range (r^2=13)
            except walking a builder out to plant another gunner.
D1  Conveyor chipping: a gunner fires at whatever economy is first on its ray
    rather than holding for a better target (31.1% of wild shots).
D2  Fixed-tile rebuild: HOME sites cycle over 3 tiles and the KILL anchor is a
    single deterministic tile, so a dead gunner is re-planted onto the same
    covered ray at full cost rather than relocated.
D3  Zero splitters, zero barriers, ever.
D4  Builder melee never targets a core, a turret, a harvester or a barrier --
    only enemy conveyors. A core at 20 HP with no ray on it survives.
D6  Spawn clusters at r0-r2 and r12-r20, then nothing until r180: a builder
    killed mid-game is not replaced for 100+ rounds.
D7  Mis-aimed doorstep plants: one plant in three inside d<=13 faces 90 degrees
    off and pays 10 Ti to rotate later (wild: 69% face the right way).
D8  Delivery can break outright: the chain-laying stages are untouched, loop
    guard, MAX_CHAIN bail and all. A probe whose economy never fails is a probe
    that never hands us the game the way the wild occasionally does.

Deterministic: no random anywhere. Ties break on (distance, x, y). Silent: no
prints. Seat-general: every station is a policy over (own core, enemy core, map
geometry), never a coordinate -- spec section 6 rule 1. No try/finally anywhere:
the platform's bot-code validator rejects it.

Communication store slots:
  0  SLOT_HOME        packed position of our own Core
  1  SLOT_ENEMY       packed position of the enemy Core, once directly sighted
  2  SLOT_ROLE_NEXT   builder role claim counter
  3  SLOT_GUNNERS     gunners built so far == index of the next station
  4  SLOT_HARVESTERS  harvesters built so far
"""

import sys

from fcode import (
    Controller,
    Direction,
    EntityType,
    Environment,
    GameError,
    Position,
)

# --- store slots -----------------------------------------------------------
SLOT_HOME = 0
SLOT_ENEMY = 1
SLOT_ROLE_NEXT = 2
SLOT_GUNNERS = 3
SLOT_HARVESTERS = 4

# --- spawns (R5 / D6) ------------------------------------------------------
# Wild: median 3 builders by r10, 5 by r40, 7 lifetime (range 5-17), and the
# schedule is three clusters -- r0/r1/r2, two more at r8-r24, then NOTHING until
# a late replacement batch at r150-r330. Five bodies by r5 (the frozen probe)
# costs 222 Ti of the 500 start against 109 for three, and inflates the cost
# scale of every gunner in the match.
OPENING_CLUSTER = (0, 1, 2, 12, 20)
LATE_FIRST = 180
LATE_INTERVAL = 60
MAX_BUILDERS_TOTAL = 14
# If we are down to the core and one unit something has gone badly wrong;
# rebuild regardless of the schedule.
DISTRESS_UNITS = 3
DISTRESS_MAX_SPAWNS = 20

# --- cadence: CARRIED OVER VERBATIM, do not retune --------------------------
# Spec 1.4: "Preserve BAND_DUE / CREEP_INTERVAL / SIEGE_INTERVAL cadence
# arithmetic verbatim; change where the gunners go and who plants them."
# These constants and _cadence_standoff/_saturation_index exist ONLY to
# reproduce the frozen probe's due-round sequence
#   14, 18, 34, 56, 80, 104, 128, 152, 176, 200, 224, 233, 242, ...
# which is what puts cumulative planted on the wild's 2/3/4/5/8/11/18 curve.
FIRST_FRACTION = 0.50
MAX_FIRST_WALK = 5.5
HOLD_STATIONS = 4
LADDER_STATIONS = 11
BAND_OFFSETS = ((0, 0), (2, 0), (-1, 1), (4, 0))
CORE_STANDOFF = 1.6
BAND_DUE = (14, 18, 34, 56)
CREEP_INTERVAL = 24
SIEGE_INTERVAL = 9
SIEGE_SPREAD = (0, 2, -2, 1, -1, 3, -3)

# --- the band plan (R1) ----------------------------------------------------
# Every station index is typed. Measured wild site distribution by squared
# distance to OUR core (847 sites): d>144 22.6% living a median 179 rounds,
# d 65-144 13.5%, d 27-64 24.3%, d 10-26 23.6%, d<=9 16.1% living ~64.
# The prefix plus the repeating tail reproduce 22.6 / 61.3 / 16.1 exactly over
# the first 31 stations.
BAND_HOME = 0
BAND_MID = 1
BAND_KILL = 2
BAND_PREFIX = (
    BAND_HOME, BAND_HOME,                          # 0,1   r14, r18
    BAND_MID, BAND_MID, BAND_MID, BAND_MID,        # 2-5   r34, r56, r80, r104
    BAND_KILL, BAND_KILL, BAND_KILL,               # 6-8   the strike burst
    BAND_HOME,                                     # 9     r200
    BAND_MID, BAND_MID, BAND_MID,                  # 10-12
    BAND_HOME,                                     # 13
    BAND_MID, BAND_MID, BAND_MID,                  # 14-16
    BAND_HOME,                                     # 17
    BAND_MID,                                      # 18
)
BAND_TAIL = (BAND_KILL, BAND_MID, BAND_HOME, BAND_MID, BAND_MID, BAND_MID)

# HOME screen: (along the own-core -> enemy-core lane, perpendicular), in tiles
# from our own core's centre. Wild first gunner sits a median 3.5 tiles
# centre-to-centre from its OWN core; the builder plants one tile further out
# than it stands, so these land the screen at ~3.4-4.0. Three sites, cycled --
# the 4th home station rebuilds site 0 (D2).
HOME_SITES = ((3.0, 0.0), (2.4, 2.4), (2.4, -2.4))
# A home builder never leaves this radius of its own core (spec: 20% of their
# builders never leave d<=6 of home, median 1 builder lost per game). Kept
# tight: at 7 tiles the screen builders wandered far enough after ore that they
# arrived at their own stations 10 rounds late.
HOME_LEASH_SQ = 36

# MID picket: standoff from the ENEMY core centre, creeping inward over the
# game. On D=20 these are d 121 / 81 / 49 / 30 / 42 / 20 / 64 / 25; on a small
# map they clamp against HOME_CLEAR and are core-threatening immediately, which
# is the measured r2-r10 opening gunner on fjordgate/meander.
MID_STANDOFFS = (11.0, 9.0, 7.0, 5.5, 6.5, 4.5, 8.0, 5.0)
MID_PERP = (0.0, 1.5, -1.5, 0.0, 2.0, -2.0, 1.0, -1.0)
# No station may be planted closer than this to our OWN core centre.
HOME_CLEAR = 3.0

# KILL: the strike builder's anchor tile. It stands here and plants its three
# gunners on three orthogonal neighbours over ~7 rounds. The anchor is
# deterministic, so a later KILL station re-plants the same covered ray (D2).
KILL_STANDOFF = 3.3
KILL_PERP = (0.0, 0.0, 0.0, 1.8, -1.8, 0.0)
# Wild: first gunner at d<=9 of our core at median r124, arriving as a burst of
# 2-3 inside a 12-round window. Cost: nothing -- these three replace the frozen
# probe's stations 6/7/8 (due r128/r152/r176), they are not extra gunners.
KILL_DUE = (124, 127, 130)
# d<=13 of the enemy core is the spec's "killer" band (A7).
KILLER_BAND_SQ = 13

# --- builder duties (R1) ---------------------------------------------------
DUTY_HOME = 0
DUTY_MID = 1
DUTY_STRIKE = 2
# Role -> (duty, slot). With three builders standing by r10 the roster is
# home0 / mid0 / home1, which is exactly who the first three stations need;
# mid1 and strike0 arrive in the r12-r20 cluster in time for stations 3 and 6.
ROLE_DUTY = (
    (DUTY_HOME, 0),
    (DUTY_MID, 0),
    (DUTY_HOME, 1),
    (DUTY_MID, 1),
    (DUTY_STRIKE, 0),
)
# If the owning builder is dead the station does not stall the way the frozen
# probe's single latch did: after this many rounds past due a SECOND duty
# becomes eligible as well, rotating through ROLE_DUTY, so the ladder never
# needs a latch handover. The rightful owner never loses its station -- an
# earlier revision rotated ownership away instead of adding to it and deadlocked
# every station whose owner was still walking to it.
TAKEOVER_GRACE = 20
# Rounds a builder budgets per tile when deciding to set out for a station.
# Measured on snowflake: a builder threading its own economy averages ~2.25
# rounds per tile, so this is deliberately pessimistic -- arriving early and
# guarding the site is free, arriving late costs a station.
TRAVEL_PER_TILE = 2.6
# ...but never set out more than this many rounds before the station is due.
# Without the cap a mid builder leaves for a station 60 rounds early and stands
# on it healing while the economy it should be laying never gets built -- which
# is the difference between the wild's 4,330 Ti collected and zero. The strike
# builder gets a longer lead because its anchor is most of the map away and its
# arrival round is the one thing R2 is actually about.
MAX_LEAD = 26
MAX_LEAD_STRIKE = 64

# --- gunners ---------------------------------------------------------------
GUNNER_RANGE_SQ = 13
ROTATE_COST = 10
# R4: measured median 2.78 rotations per gunner (mean 3.43), not the ~1.5 the
# frozen probe's docstring claimed. A gunner that re-aims tracks a moving heal
# line; one that does not gets walked around.
ROTATE_MIN_GAP = 3
ROTATE_MIN_TITANIUM = 25
# ...and a hard lifetime cap, which the frozen probe did not have. Without it a
# gunner with nothing on its ray re-aims every ROTATE_MIN_GAP rounds forever:
# measured 339 rotations over 6 gunners (56.5 each, 3,390 Ti) on one snowflake
# game. Wild median is 2.78 per gunner over its whole life.
ROTATE_MAX_PER_GUNNER = 4

# --- builder melee (D4 / section 1.1) --------------------------------------
# 446 melee attacks in 45 games, 89.9% on conveyors, ZERO on a core, a turret, a
# harvester or a barrier. This is the single most load-bearing habit in the
# spec: it is why a standoff turret outside r^2=13 is unanswerable.
MELEE_MIN_GAP = 20
MELEE_MAX_PER_BUILDER = 4
MELEE_MIN_TITANIUM = 10

# --- economy ---------------------------------------------------------------
ECO_HARVESTER_CAP = 20
HARVESTER_COST_CEILING = 220
MAX_CHAIN = 14
# A conveyor run that has been open this long is abandoned. Without the bound a
# builder can oscillate inside the `lay` stage indefinitely -- measured once as
# a 876-round ladder stall at 6 gunners, because station duty waits for the run
# to finish. D8 keeps the run's other failure modes; this only bounds the wait.
CHAIN_MAX_ROUNDS = 30
HEAL_MIN_TITANIUM = 20

# --- ammunition ------------------------------------------------------------
# Wild converts a median 1,437 Ti per game and holds 32-56 from r25 onward.
AMMO_FLOOR = 44
AMMO_CRITICAL = 16
AMMO_CEILING = 60
AMMO_RICH_CEILING = 320
AMMO_RICH_TITANIUM = 600
ECO_FLOAT = 70
EMERGENCY_FLOAT = 12

# Bail at a phase boundary rather than let the engine truncate a statement.
CPU_BUDGET_US = 7000

CARDINALS = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)
ECONOMY_TYPES = (EntityType.HARVESTER, EntityType.CONVEYOR, EntityType.SPLITTER)
TURRET_TYPES = (EntityType.GUNNER, EntityType.SENTINEL, EntityType.LAUNCHER)


def pack_pos(pos: Position) -> int:
    """Encode a position into one store int, offset so (0,0) is not 'empty'."""
    return ((pos.x + 1) << 16) | (pos.y + 1)


def unpack_pos(val: int) -> Position | None:
    if val <= 0:
        return None
    return Position((val >> 16) - 1, (val & 0xFFFF) - 1)


def in_bounds(ct: Controller, pos: Position) -> bool:
    """On the map. Necessary but not sufficient before a tile query -- tile
    getters also raise GameError for in-bounds tiles outside current vision.
    """
    return 0 <= pos.x < ct.get_map_width() and 0 <= pos.y < ct.get_map_height()


def core_footprint(nw: Position) -> list[Position]:
    """The 4 tiles of a Core's 2x2 footprint, given its NW corner."""
    return [
        nw,
        Position(nw.x + 1, nw.y),
        Position(nw.x, nw.y + 1),
        Position(nw.x + 1, nw.y + 1),
    ]


def nearest_core_tile(pos: Position, core_nw: Position) -> Position:
    return min(core_footprint(core_nw), key=lambda t: (pos.distance_squared(t), t.x, t.y))


def adjacent_core_tile(pos: Position, core_nw: Position) -> Position | None:
    """The Core footprint tile orthogonally adjacent to pos, if any."""
    for tile in core_footprint(core_nw):
        if abs(tile.x - pos.x) + abs(tile.y - pos.y) == 1:
            return tile
    return None


def band_of(idx: int) -> int:
    """Which band station `idx` belongs to. Pure function of the index."""
    if idx < len(BAND_PREFIX):
        return BAND_PREFIX[idx]
    return BAND_TAIL[(idx - len(BAND_PREFIX)) % len(BAND_TAIL)]


_ORDINAL_CACHE: dict = {}


def band_ordinal(idx: int) -> int:
    """How many stations of the same band came before `idx`. Memoised; the
    cache is keyed on a pure function of the index, so it stays deterministic.
    """
    got = _ORDINAL_CACHE.get(idx)
    if got is not None:
        return got
    band = band_of(idx)
    count = 0
    for j in range(idx):
        if band_of(j) == band:
            count += 1
    _ORDINAL_CACHE[idx] = count
    return count


def station_owner(idx: int) -> tuple:
    """(duty, slot) of the builder that owns station `idx`."""
    band = band_of(idx)
    ordinal = band_ordinal(idx)
    if band == BAND_HOME:
        return (DUTY_HOME, ordinal % 2)
    if band == BAND_MID:
        return (DUTY_MID, ordinal % 2)
    return (DUTY_STRIKE, 0)


class Player:
    def __init__(self):
        # Shared / derived map knowledge (one Player instance per unit).
        self.home: Position | None = None
        self.enemy: Position | None = None
        self.enemy_confirmed = False

        # Core state
        self.spawned = 0

        # Builder state
        self.role: int | None = None
        self.duty = DUTY_MID
        self.slot = 0
        self.leash_sq: int | None = None
        self.stage = "ore"
        self.prev_pos: Position | None = None
        self.stuck = 0
        self.recent: list = []
        self.known_ore: set = set()
        self.ore_target: Position | None = None
        self.harvester_pos: Position | None = None
        self.trail_prev: Position | None = None
        self.chain_tiles: set = set()
        self.chain_len = 0
        self.chain_open = -1
        self.cap_tile: Position | None = None
        self.heading_idx: int | None = None
        self.station_idx: int | None = None
        self.station: Position | None = None
        self.explore_idx = 0
        self.last_melee = -99
        self.melee_count = 0

        # Turret state
        self.last_rotate = -99
        self.rotations = 0
        self.killer: bool | None = None

        self.reported_error = False

    # ------------------------------------------------------------------
    # entry point
    # ------------------------------------------------------------------

    def run(self, ct: Controller) -> None:
        """An exception escaping run() permanently deletes this unit, so the
        guard is unconditional. Never a try/finally -- the validator rejects it.
        """
        try:
            self._dispatch(ct)
        except Exception:
            if not self.reported_error:
                self.reported_error = True
                import traceback

                traceback.print_exc(file=sys.stderr)

    def _dispatch(self, ct: Controller) -> None:
        etype = ct.get_entity_type()
        if etype == EntityType.CORE:
            self._run_core(ct)
        elif etype == EntityType.BUILDER_BOT:
            self._run_builder(ct)
        elif etype == EntityType.GUNNER:
            self._run_gunner(ct)

    def _cpu_exhausted(self, ct: Controller) -> bool:
        return ct.get_cpu_time_elapsed() >= CPU_BUDGET_US

    # ------------------------------------------------------------------
    # shared map / intel
    # ------------------------------------------------------------------

    def _locate(self, ct: Controller) -> None:
        """Establish home and enemy Core positions as cheaply as possible.

        1. Sight them directly if they are in vision.
        2. Otherwise read whatever the store already knows.
        3. Otherwise derive the enemy anchor by point symmetry from home.
        """
        if self.home is None or not self.enemy_confirmed:
            my_team = ct.get_team()
            try:
                nearby = ct.get_nearby_buildings()
            except GameError:
                nearby = []
            for bid in nearby:
                try:
                    if ct.get_entity_type(bid) != EntityType.CORE:
                        continue
                    where = ct.get_position(bid)
                    if ct.get_team(bid) == my_team:
                        self.home = where
                    else:
                        self.enemy = where
                        if not self.enemy_confirmed:
                            self.enemy_confirmed = True
                            ct.write_store(SLOT_ENEMY, pack_pos(where))
                except GameError:
                    continue

        if self.home is None:
            self.home = unpack_pos(ct.read_store(SLOT_HOME))
        if not self.enemy_confirmed:
            stored = unpack_pos(ct.read_store(SLOT_ENEMY))
            if stored is not None:
                self.enemy = stored
                self.enemy_confirmed = True
        if self.enemy is None and self.home is not None:
            w, h = ct.get_map_width(), ct.get_map_height()
            self.enemy = Position(
                min(max(0, w - 2 - self.home.x), w - 1),
                min(max(0, h - 2 - self.home.y), h - 1),
            )

    # ------------------------------------------------------------------
    # cadence -- carried over verbatim from the frozen probe
    # ------------------------------------------------------------------

    def _station_due_round(self, idx: int, ct: Controller) -> int:
        """Round at which station `idx` becomes due.

        The arithmetic below is the frozen probe's, unchanged. The one override
        is R2: the three prefix KILL stations are pulled forward onto the wild's
        measured strike window (r124 burst) from r128/r152/r176. That is a
        re-timing of three stations that already existed, not extra mass.
        """
        if band_of(idx) == BAND_KILL:
            ordinal = band_ordinal(idx)
            if ordinal < len(KILL_DUE):
                return KILL_DUE[ordinal]
        if idx < len(BAND_DUE):
            return BAND_DUE[idx]
        sat = self._saturation_index(ct)
        base = BAND_DUE[-1]
        creep = min(idx, sat) - (len(BAND_DUE) - 1)
        due = base + max(0, creep) * CREEP_INTERVAL
        if idx > sat:
            due += (idx - sat) * SIEGE_INTERVAL
        return due

    def _lane(self, ct: Controller):
        """(home centre, enemy centre, unit vector home->enemy, gap D)."""
        if self.home is None or self.enemy is None:
            return None
        hx, hy = self.home.x + 0.5, self.home.y + 0.5
        ex, ey = self.enemy.x + 0.5, self.enemy.y + 0.5
        dx, dy = ex - hx, ey - hy
        dist = (dx * dx + dy * dy) ** 0.5
        if dist < 1e-6:
            return None
        return (hx, hy), (ex, ey), (dx / dist, dy / dist), dist

    def _first_standoff(self, ct: Controller) -> float:
        lane = self._lane(ct)
        if lane is None:
            return CORE_STANDOFF
        dist = lane[3]
        walk = min(FIRST_FRACTION * dist, MAX_FIRST_WALK)
        return max(CORE_STANDOFF, dist - walk)

    def _cadence_standoff(self, ct: Controller, idx: int) -> float:
        """The frozen probe's `_standoff`, kept ONLY so `_saturation_index` and
        therefore every due round stay bit-identical. It no longer sites
        anything -- see `_station_site`.
        """
        first = self._first_standoff(ct)
        if idx < HOLD_STATIONS:
            lane = self._lane(ct)
            back = first + BAND_OFFSETS[idx][0]
            if lane is not None:
                back = min(back, lane[3] - CORE_STANDOFF)
            return max(CORE_STANDOFF, back)
        span = max(1, LADDER_STATIONS - HOLD_STATIONS)
        frac = (idx - HOLD_STATIONS + 1) / float(span)
        return max(CORE_STANDOFF, first + (CORE_STANDOFF - first) * frac)

    def _saturation_index(self, ct: Controller) -> int:
        """First station index whose cadence standoff bottoms out at the core."""
        for idx in range(LADDER_STATIONS + 1):
            if self._cadence_standoff(ct, idx) <= CORE_STANDOFF:
                return idx
        return LADDER_STATIONS

    # ------------------------------------------------------------------
    # the band plan -- shared geometry, seat-general
    # ------------------------------------------------------------------

    def _station_site(self, ct: Controller, idx: int) -> Position | None:
        """Where the builder that plants station `idx` stands.

        HOME sites are expressed from our OWN core; MID and KILL sites as a
        standoff from the enemy core along the lane. Nothing is a coordinate --
        spec section 6 rule 1 -- so the whole plan is seat-general and map-general.
        """
        lane = self._lane(ct)
        if lane is None:
            return None
        (hx, hy), (ex, ey), (ux, uy), dist = lane
        band = band_of(idx)
        ordinal = band_ordinal(idx)
        if band == BAND_HOME:
            along, perp = HOME_SITES[ordinal % len(HOME_SITES)]
            along = min(along, max(0.5, dist - CORE_STANDOFF))
            px = hx + ux * along - uy * perp
            py = hy + uy * along + ux * perp
        else:
            if band == BAND_MID:
                standoff = MID_STANDOFFS[ordinal % len(MID_STANDOFFS)]
                perp = MID_PERP[ordinal % len(MID_PERP)]
            else:
                standoff = KILL_STANDOFF
                perp = KILL_PERP[ordinal % len(KILL_PERP)]
            # Never step back past our own doorstep.
            standoff = min(standoff, max(CORE_STANDOFF, dist - HOME_CLEAR))
            px = ex - ux * standoff - uy * perp
            py = ey - uy * standoff + ux * perp
        w, h = ct.get_map_width(), ct.get_map_height()
        site = Position(
            min(max(int(round(px)), 0), w - 1),
            min(max(int(round(py)), 0), h - 1),
        )
        return self._nudge(ct, site)

    def _lane_reserved(self, ct: Controller, tile: Position) -> bool:
        """Is this tile inside the picket corridor?

        Harvesters are permanent and cannot be rerouted around, so the corridor
        is kept clear of them; conveyors may still cross it and are bulldozed by
        the planting builder if they are in the way.
        """
        lane = self._lane(ct)
        if lane is None:
            return False
        (hx, hy), _e, (ux, uy), dist = lane
        vx, vy = tile.x - hx, tile.y - hy
        along = vx * ux + vy * uy
        perp = abs(vx * -uy + vy * ux)
        if perp > 1.2:
            return False
        reach = dist - self._first_standoff(ct) + 2.0
        return 1.0 <= along <= reach

    def _nudge(self, ct: Controller, site: Position) -> Position:
        """Slide a station off a wall or a Core footprint tile onto the nearest
        standable neighbour. Tiles outside vision raise, and are assumed fine.
        """
        blocked = set()
        if self.enemy is not None:
            blocked.update((t.x, t.y) for t in core_footprint(self.enemy))
        if self.home is not None:
            blocked.update((t.x, t.y) for t in core_footprint(self.home))
        if (site.x, site.y) not in blocked:
            try:
                if ct.get_tile_env(site) != Environment.WALL:
                    return site
            except GameError:
                return site
        best = None
        for dx in (-1, 0, 1, -2, 2):
            for dy in (-1, 0, 1, -2, 2):
                cand = Position(site.x + dx, site.y + dy)
                if not in_bounds(ct, cand) or (cand.x, cand.y) in blocked:
                    continue
                try:
                    if ct.get_tile_env(cand) == Environment.WALL:
                        continue
                except GameError:
                    pass
                key = (dx * dx + dy * dy, cand.x, cand.y)
                if best is None or key < best[0]:
                    best = (key, cand)
        return best[1] if best is not None else site

    # ------------------------------------------------------------------
    # Core
    # ------------------------------------------------------------------

    def _run_core(self, ct: Controller) -> None:
        """Builders in clusters (R5/D6), and titanium into ammunition, always.

        convert_ammo() does not consume the action cooldown, so converting never
        costs a spawn -- it is always tried first.
        """
        pos = ct.get_position()
        if self.home is None:
            self.home = pos
            ct.write_store(SLOT_HOME, pack_pos(pos))
        self._locate(ct)

        rnd = ct.get_current_round()
        self._bank_ammo(ct, rnd)

        if ct.get_action_cooldown() != 0:
            return

        allowance = self._spawn_allowance(rnd)
        if self.spawned >= allowance:
            # Total-wipe insurance only; not a standing replacement policy.
            if ct.get_unit_count() > DISTRESS_UNITS or self.spawned >= DISTRESS_MAX_SPAWNS:
                return
        if ct.get_global_resources() < ct.get_builder_bot_cost():
            return

        # Spawn on the ring tile nearest the enemy. The whole 12-tile ring is
        # enumerated via get_nearby_tiles(8) and filtered by can_spawn(), never
        # by pos.add(d) -- that only reaches the N/W half of the ring and is an
        # absolute-direction bug that decides whole maps by seat.
        anchor = self.enemy if self.enemy is not None else pos
        best = None
        for tile in ct.get_nearby_tiles(dist_sq=8):
            if not ct.can_spawn(tile):
                continue
            key = (tile.distance_squared(anchor), tile.x, tile.y)
            if best is None or key < best[0]:
                best = (key, tile)
        if best is not None:
            ct.spawn_builder(best[1])
            self.spawned += 1

    def _spawn_allowance(self, rnd: int) -> int:
        """Three clusters, exactly as measured: r0/r1/r2, r12/r20, then nothing
        at all until the late replacement batch from r180 (D6).
        """
        allowance = 0
        for when in OPENING_CLUSTER:
            if rnd >= when:
                allowance += 1
        if rnd >= LATE_FIRST:
            allowance += 1 + (rnd - LATE_FIRST) // LATE_INTERVAL
        return min(allowance, MAX_BUILDERS_TOTAL)

    def _bank_ammo(self, ct: Controller, rnd: int) -> None:
        """Aggressive and continuous, from the first round the bank allows.

        The wild converts a median 1,437 Ti per game and holds 32-56 from r25
        onward. The one thing that must never happen is a gunner sitting dry
        while there is titanium in the bank.
        """
        ammo = ct.get_global_ammo()
        titanium = ct.get_global_resources()
        ceiling = AMMO_RICH_CEILING if titanium >= AMMO_RICH_TITANIUM else AMMO_CEILING
        if ammo >= ceiling:
            return

        reserve = EMERGENCY_FLOAT
        # Only the cluster spawns that are actually due are reserved for -- the
        # rest of the 500 start is banked and converted, which is where the
        # wild's 5.6x conversion advantage comes from.
        due_now = 0
        for when in OPENING_CLUSTER:
            if rnd >= when:
                due_now += 1
        if self.spawned < due_now:
            reserve += (due_now - self.spawned) * ct.get_builder_bot_cost()
        if ammo >= AMMO_CRITICAL:
            reserve += ct.get_gunner_cost()
        if ammo >= AMMO_FLOOR:
            if titanium < AMMO_RICH_TITANIUM:
                return
            reserve += ECO_FLOAT

        spare = titanium - reserve
        amount = min(ceiling - ammo, spare)
        if amount > 0 and ct.can_convert_ammo(amount):
            ct.convert_ammo(amount)

    # ------------------------------------------------------------------
    # Builder bot
    # ------------------------------------------------------------------

    def _run_builder(self, ct: Controller) -> None:
        rnd = ct.get_current_round()
        pos = ct.get_position()
        self._locate(ct)

        if self.role is None:
            # At most one builder is spawned per round (the Core's action
            # cooldown guarantees it), and store writes land next round, so a
            # simple claim counter cannot hand the same index to two builders.
            nxt = ct.read_store(SLOT_ROLE_NEXT)
            self.role = nxt if nxt > 0 else 1
            ct.write_store(SLOT_ROLE_NEXT, self.role + 1)
            self.role -= 1
            self.duty, self.slot = ROLE_DUTY[self.role % len(ROLE_DUTY)]
            if self.duty == DUTY_HOME:
                self.leash_sq = HOME_LEASH_SQ

        if self.prev_pos is not None:
            if pos == self.prev_pos:
                self.stuck += 1
            else:
                self.stuck = 0
        self.prev_pos = pos
        # Short tabu list. Without it a builder that meets a blocker on its
        # preferred axis steps aside, finds the axis clear again from the new
        # tile, steps back, and 2-cycles there for the rest of the match.
        self.recent.append((pos.x, pos.y))
        if len(self.recent) > 4:
            self.recent.pop(0)

        if self._station_duty(ct, rnd, pos):
            return
        self._run_eco(ct, rnd, pos)

    # -- station duty ----------------------------------------------------

    def _may_plant(self, idx: int, rnd: int, due: int) -> bool:
        """Am I the builder that plants station `idx` this round?

        R1's whole point: the frozen probe had ONE latched picket builder, and
        when it died the ladder stalled for >= 3 rounds while the latch
        reassigned and the replacement re-walked the lane. Here ownership is a
        pure function of (station index, round), so exactly one duty is eligible
        on any round, nothing is stored, and a dead owner costs TAKEOVER_GRACE
        rounds rather than a re-walk.
        """
        want = station_owner(idx)
        mine = (self.duty, self.slot)
        if mine == want:
            return True
        lag = rnd - due
        if lag < TAKEOVER_GRACE:
            return False
        step = (lag - TAKEOVER_GRACE) // TAKEOVER_GRACE + 1
        start = ROLE_DUTY.index(want)
        return mine == ROLE_DUTY[(start + step) % len(ROLE_DUTY)]

    def _next_own_station(self, ct: Controller, idx: int, rnd: int) -> int | None:
        for k in range(idx, idx + 9):
            if self._may_plant(k, rnd, self._station_due_round(k, ct)):
                return k
        return None

    def _station_duty(self, ct: Controller, rnd: int, pos: Position) -> bool:
        """Walk to my next station and plant it. Returns True if the turn is
        spent. Builders that own nothing right now fall through to economy --
        which is most of them, most of the time, which is the point of R1.
        """
        if self.home is None or self.enemy is None:
            return False
        idx = ct.read_store(SLOT_GUNNERS)
        if self.stage in ("lay", "cap"):
            # A half-laid conveyor run delivers exactly nothing, so a builder
            # part-way through one finishes it before it answers the ladder.
            # CHAIN_MAX_ROUNDS bounds how long that can hold the ladder up. The
            # strike builder is the exception: R2 is entirely about the round
            # its burst lands, so it drops whatever it is carrying.
            # (The frozen probe never had this conflict: only the single latched
            # picket builder ever planted.)
            pending = self._next_own_station(ct, idx, rnd)
            if pending is None or band_of(pending) != BAND_KILL:
                return False
            self.stage = "ore"
        if self.heading_idx is not None and self.heading_idx < idx:
            self.heading_idx = None
            self.station = None
        if self.heading_idx is None:
            target = self._next_own_station(ct, idx, rnd)
            if target is not None:
                site = self._station_site(ct, target)
                if site is not None:
                    gap = pos.distance_squared(site) ** 0.5
                    when = self._station_due_round(target, ct)
                    lead = MAX_LEAD_STRIKE if band_of(target) == BAND_KILL else MAX_LEAD
                    if rnd + TRAVEL_PER_TILE * gap + 1.0 >= when and rnd + lead >= when:
                        self.heading_idx = target
                        self.station_idx = target
                        self.station = site
        if self.heading_idx is None:
            return False

        target = self.heading_idx
        if self.station is None or self.station_idx != target:
            self.station_idx = target
            self.station = self._station_site(ct, target)
        station = self.station
        if station is None:
            return False

        near = pos.distance_squared(station) <= 2
        if near:
            # Holding station on purpose is not being stuck.
            self.stuck = 0

        due = self._station_due_round(target, ct)
        if target == idx and rnd >= due and ct.get_action_cooldown() == 0:
            if self._may_plant(target, rnd, due):
                if ct.get_global_resources() >= ct.get_gunner_cost():
                    if near or (self.stuck >= 6 and pos.distance_squared(station) <= 20):
                        if self._plant_gunner(ct, pos, target):
                            ct.write_store(SLOT_GUNNERS, idx + 1)
                            self.heading_idx = None
                            self.station = None
                            self.station_idx = None
                            return True

        if not near and self._step_toward(ct, station):
            return True
        # Standing on the site waiting for it to come due: keep the screen
        # repaired (median 76 heals a game is how a forward gunner becomes a
        # line instead of a loss) and chip whatever enemy conveyor is adjacent.
        if ct.get_action_cooldown() == 0:
            if self._try_melee(ct, pos, rnd):
                return True
            if ct.get_global_resources() >= HEAL_MIN_TITANIUM and self._try_heal(ct, pos):
                return True
        return True

    def _plant_gunner(self, ct: Controller, pos: Position, idx: int) -> bool:
        """Gunner on an orthogonally adjacent tile, facing the enemy Core.

        The Gunner fires a single-tile-wide ray, so the facing is what matters,
        not the position; it re-aims later by rotating rather than relocating.

        D7: only 69% of measured plants inside d<=13 of our core face toward it.
        One doorstep plant in three is deliberately laid 90 degrees off and pays
        10 Ti to rotate later.
        """
        if self.enemy is None:
            return False
        my_team = ct.get_team()
        best = None
        blocked = None
        for d in CARDINALS:
            site = pos.add(d)
            if not in_bounds(ct, site):
                continue
            aim = nearest_core_tile(site, self.enemy)
            facing = site.direction_to(aim)
            if facing == Direction.CENTRE:
                continue
            if idx % 3 == 2 and site.distance_squared(aim) <= KILLER_BAND_SQ:
                facing = facing.rotate_left()
            aligned = 0
            if band_of(idx) == BAND_KILL:
                # A ray that runs straight down a row or column into the 2x2
                # footprint is what puts 65.5% of the wild killers' fire into
                # our core; a diagonal one spends itself on whatever it clips.
                if site.x in (self.enemy.x, self.enemy.x + 1) or \
                        site.y in (self.enemy.y, self.enemy.y + 1):
                    aligned = -1
            key = (aligned, site.distance_squared(self.enemy), site.x, site.y)
            try:
                if ct.can_build_gunner(site, facing):
                    if best is None or key < best[0]:
                        best = (key, site, facing)
                    continue
            except GameError:
                continue
            # Not buildable. If it is one of our own conveyors squatting on the
            # station, it can be cleared: destroy is free and costs no
            # cooldown, so the gunner still goes up this turn.
            try:
                bid = ct.get_tile_building_id(site)
                if bid is None or ct.get_team(bid) != my_team:
                    continue
                if ct.get_entity_type(bid) != EntityType.CONVEYOR:
                    continue
                if not ct.can_destroy(site):
                    continue
            except GameError:
                continue
            if blocked is None or key < blocked[0]:
                blocked = (key, site, facing)

        if best is None and blocked is not None:
            try:
                ct.destroy(blocked[1])
                if ct.can_build_gunner(blocked[1], blocked[2]):
                    best = blocked
            except GameError:
                return False
        if best is None:
            return False
        try:
            ct.build_gunner(best[1], best[2])
        except GameError:
            return False
        return True

    def _try_melee(self, ct: Controller, pos: Position, rnd: int) -> bool:
        """2 Ti for 2 damage into an adjacent ENEMY CONVEYOR, and nothing else.

        446 melee attacks across 45 games, 89.9% of them on a conveyor and ZERO
        on a core, a turret, a harvester or a barrier (D4 / D-CRITICAL). This is
        the habit that makes a standoff turret outside r^2=13 unanswerable, so a
        probe that meleed anything else would erase the exploit lane.
        """
        if rnd - self.last_melee < MELEE_MIN_GAP or self.melee_count >= MELEE_MAX_PER_BUILDER:
            return False
        if ct.get_global_resources() < MELEE_MIN_TITANIUM:
            return False
        my_team = ct.get_team()
        for d in CARDINALS:
            tile = pos.add(d)
            if not in_bounds(ct, tile):
                continue
            try:
                bid = ct.get_tile_building_id(tile)
                if bid is None or ct.get_team(bid) == my_team:
                    continue
                if ct.get_entity_type(bid) != EntityType.CONVEYOR:
                    continue
                if not ct.can_fire(tile):
                    continue
            except GameError:
                continue
            try:
                ct.fire(tile)
            except GameError:
                return False
            self.last_melee = rnd
            self.melee_count += 1
            return True
        return False

    # -- economy builders -----------------------------------------------

    def _run_eco(self, ct: Controller, rnd: int, pos: Position) -> None:
        """Harvester on ore, conveyor run home, repeat. Grows all game.

        Untouched from the frozen probe except for the home leash: D8 says the
        wild's delivery can break outright (2 harvesters, 9 conveyors, ZERO
        titanium collected for 155 rounds), so the chain-laying failure modes
        are preserved exactly as they are.
        """
        self._scan_ore(ct)
        if self._cpu_exhausted(ct):
            return
        if self.stage in ("lay", "cap") and 0 <= self.chain_open <= rnd - CHAIN_MAX_ROUNDS:
            self.stage = "ore"

        if self.stage == "ore":
            self._eco_seek_ore(ct, pos)
        elif self.stage == "lay":
            self._eco_lay(ct, pos)
        elif self.stage == "cap":
            self._eco_cap(ct, pos)
        else:
            self._eco_idle(ct, rnd, pos)

    def _eco_expansion_open(self, ct: Controller) -> bool:
        if ct.read_store(SLOT_HARVESTERS) >= ECO_HARVESTER_CAP:
            return False
        return ct.get_harvester_cost() <= HARVESTER_COST_CEILING

    def _scan_ore(self, ct: Controller) -> None:
        """Remember ore tiles seen. Vision is r^2=20, so this is ~60 tiles."""
        if self.stage != "ore":
            return
        try:
            tiles = ct.get_nearby_tiles()
        except GameError:
            return
        for tile in tiles:
            try:
                if ct.get_tile_env(tile) == Environment.ORE_TITANIUM:
                    self.known_ore.add((tile.x, tile.y))
            except GameError:
                continue

    def _eco_seek_ore(self, ct: Controller, pos: Position) -> None:
        """Walk to the nearest free ore and plant a harvester on it."""
        if not self._eco_expansion_open(ct):
            self.stage = "idle"
            return

        free = []
        reserved = []
        for (x, y) in self.known_ore:
            tile = Position(x, y)
            try:
                if ct.get_tile_building_id(tile) is not None:
                    continue
            except GameError:
                pass  # out of vision: assume still free, re-checked on arrival
            if self._lane_reserved(ct, tile):
                reserved.append(tile)
            else:
                free.append(tile)
        if not free:
            free = reserved
        if self.leash_sq is not None and self.home is not None:
            # A home builder is a screen builder: it does not chase ore out of
            # its own half, it stays and heals what it planted.
            free = [t for t in free if t.distance_squared(self.home) <= self.leash_sq]
            if not free:
                self.stage = "idle"
                return
        if not free:
            self._step_toward(ct, self._explore_target(ct, pos))
            return
        # Nearest to HOME, not to the builder: the wild's economy grows outward
        # from its core in short runs, and ranking by distance to the builder
        # walks it steadily away from home and doubles every conveyor run.
        anchor = self.home if self.home is not None else pos
        free.sort(key=lambda t: (t.distance_squared(anchor), t.x, t.y))
        rank = min((self.role or 0) % 3, len(free) - 1)
        self.ore_target = free[rank]

        if ct.get_action_cooldown() == 0 and ct.get_global_resources() >= ct.get_harvester_cost():
            for tile in free[:4]:
                if abs(tile.x - pos.x) + abs(tile.y - pos.y) != 1:
                    continue
                try:
                    if not ct.can_build_harvester(tile):
                        continue
                except GameError:
                    continue
                ct.build_harvester(tile)
                ct.write_store(SLOT_HARVESTERS, ct.read_store(SLOT_HARVESTERS) + 1)
                self.harvester_pos = tile
                self.known_ore.discard((tile.x, tile.y))
                self._begin_chain(ct)
                return
        self._step_toward(ct, self.ore_target)

    def _begin_chain(self, ct: Controller) -> None:
        """A harvester orthogonally adjacent to the Core delivers straight into
        it, so the shortest possible run is no run at all.
        """
        self.chain_len = 0
        self.chain_open = ct.get_current_round()
        self.trail_prev = None
        self.chain_tiles = set()
        if self.home is not None and self.harvester_pos is not None:
            if adjacent_core_tile(self.harvester_pos, self.home) is not None:
                self.stage = "ore"
                return
        self.stage = "lay"

    def _eco_lay(self, ct: Controller, pos: Position) -> None:
        """Lay the run back to the Core, one tile per two rounds.

        A builder cannot build on its own tile, so the chain is laid behind it:
        step toward the Core, then conveyor the tile just vacated, facing the
        tile now occupied. Conveyors are bot-passable, so nothing it lays can
        ever box it in. (D8: this stage machine can and does fail; that failure
        is measured wild behaviour and is preserved verbatim.)
        """
        if self.home is None or self.chain_len > MAX_CHAIN:
            self.stage = "ore"
            return

        at_port = adjacent_core_tile(pos, self.home) is not None

        if self.trail_prev is not None:
            if ct.get_action_cooldown() != 0:
                return
            if self._build_link(ct, self.trail_prev, pos):
                self.chain_tiles.add((self.trail_prev.x, self.trail_prev.y))
            self.trail_prev = None
            return

        if at_port:
            # This tile is the last link; step off it so it can be built.
            self.cap_tile = pos
            self.stage = "cap"
            self._step_off(ct, pos)
            return

        target = nearest_core_tile(pos, self.home)
        before = pos
        if self._step_toward(ct, target):
            # If the step went backwards onto a tile we already conveyored, do
            # NOT lay behind us: a conveyor facing back into the one that feeds
            # it is a two-tile loop, and a chain with a loop in it delivers
            # exactly nothing (crediting is delivery-only).
            if (ct.get_position().x, ct.get_position().y) not in self.chain_tiles:
                self.trail_prev = before
                self.chain_len += 1
        elif self.stuck >= 4:
            self.stage = "ore"

    def _eco_cap(self, ct: Controller, pos: Position) -> None:
        """Build the final conveyor, the one that actually faces the Core."""
        if self.home is None or self.cap_tile is None or self.stuck >= 6:
            self.stage = "ore"
            return
        if pos == self.cap_tile:
            self._step_off(ct, pos)
            return
        if abs(self.cap_tile.x - pos.x) + abs(self.cap_tile.y - pos.y) != 1:
            self._step_toward(ct, self.cap_tile)
            return
        if ct.get_action_cooldown() != 0:
            return
        core_tile = adjacent_core_tile(self.cap_tile, self.home)
        if core_tile is None:
            self.stage = "ore"
            return
        if self._build_link(ct, self.cap_tile, core_tile) or self.stuck >= 4:
            self.stage = "ore"

    def _build_link(self, ct: Controller, tile: Position, toward: Position) -> bool:
        """One conveyor on tile, facing the neighbouring tile `toward`."""
        if not in_bounds(ct, tile):
            return False
        try:
            if ct.get_tile_building_id(tile) is not None:
                return True  # already linked by another chain; nothing owed
        except GameError:
            pass
        if ct.get_global_resources() < ct.get_conveyor_cost():
            return False
        facing = tile.cardinal_direction_to(toward)
        if facing == Direction.CENTRE:
            return False
        try:
            if not ct.can_build_conveyor(tile, facing):
                return False
        except GameError:
            return False
        ct.build_conveyor(tile, facing)
        return True

    def _step_off(self, ct: Controller, pos: Position) -> None:
        """Vacate the current tile so a conveyor can be built on it."""
        if ct.get_move_cooldown() != 0:
            return
        if self.home is None:
            self._step_toward(ct, Position(pos.x + 1, pos.y))
            return
        core_tile = nearest_core_tile(pos, self.home)
        prefs = []
        if core_tile.x > pos.x:
            prefs.append(Direction.WEST)
        elif core_tile.x < pos.x:
            prefs.append(Direction.EAST)
        if core_tile.y > pos.y:
            prefs.append(Direction.NORTH)
        elif core_tile.y < pos.y:
            prefs.append(Direction.SOUTH)
        for d in CARDINALS:
            if d not in prefs:
                prefs.append(d)
        for d in prefs:
            try:
                if ct.can_move(d):
                    ct.move(d)
                    return
            except GameError:
                continue

    def _eco_idle(self, ct: Controller, rnd: int, pos: Position) -> None:
        """Expansion is priced out for now: keep the structures repaired and
        re-check every few rounds in case a harvester died and freed the scale.

        For the two leashed HOME builders this is the steady state, and it is
        what makes the home screen live a median 179 rounds.
        """
        if rnd % 8 == 0 and self._eco_expansion_open(ct):
            if self.leash_sq is None or self._ore_in_leash(ct):
                self.stage = "ore"
                return
        if ct.get_action_cooldown() == 0:
            if ct.get_global_resources() >= HEAL_MIN_TITANIUM and self._try_heal(ct, pos):
                return
            if self._try_melee(ct, pos, rnd):
                return
        hurt = self._damaged_friendly(ct, pos)
        if hurt is not None and pos.distance_squared(hurt) > 1:
            if self.leash_sq is None or self.home is None:
                self._step_toward(ct, hurt)
            elif hurt.distance_squared(self.home) <= self.leash_sq:
                self._step_toward(ct, hurt)

    def _ore_in_leash(self, ct: Controller) -> bool:
        if self.home is None or self.leash_sq is None:
            return True
        for (x, y) in self.known_ore:
            if Position(x, y).distance_squared(self.home) <= self.leash_sq:
                try:
                    if ct.get_tile_building_id(Position(x, y)) is not None:
                        continue
                except GameError:
                    pass
                return True
        return False

    def _try_heal(self, ct: Controller, pos: Position) -> bool:
        my_team = ct.get_team()
        for d in CARDINALS:
            tile = pos.add(d)
            if not in_bounds(ct, tile):
                continue
            try:
                bid = ct.get_tile_building_id(tile)
                if bid is None or ct.get_team(bid) != my_team:
                    continue
                if ct.get_hp(bid) >= ct.get_max_hp(bid):
                    continue
                if not ct.can_heal(tile):
                    continue
            except GameError:
                continue
            ct.heal(tile)
            return True
        return False

    def _damaged_friendly(self, ct: Controller, pos: Position) -> Position | None:
        my_team = ct.get_team()
        best = None
        try:
            nearby = ct.get_nearby_buildings()
        except GameError:
            return None
        for bid in nearby:
            try:
                if ct.get_team(bid) != my_team:
                    continue
                if ct.get_hp(bid) >= ct.get_max_hp(bid):
                    continue
                where = ct.get_position(bid)
            except GameError:
                continue
            key = (pos.distance_squared(where), where.x, where.y)
            if best is None or key < best[0]:
                best = (key, where)
        return best[1] if best is not None else None

    def _explore_target(self, ct: Controller, pos: Position) -> Position:
        """No ore in memory: sweep outward from home in a fixed rosette."""
        anchor = self.home if self.home is not None else pos
        w, h = ct.get_map_width(), ct.get_map_height()
        if self.leash_sq is not None:
            ring = ((4, 0), (0, 4), (-4, 0), (0, -4), (3, 3), (-3, 3), (3, -3), (-3, -3))
        else:
            ring = ((6, 0), (0, 6), (-6, 0), (0, -6), (5, 5), (-5, 5), (5, -5), (-5, -5))
        if self.stuck >= 3:
            self.explore_idx += 1
        dx, dy = ring[(self.explore_idx + (self.role or 0)) % len(ring)]
        return Position(
            min(max(anchor.x + dx, 0), w - 1),
            min(max(anchor.y + dy, 0), h - 1),
        )

    # ------------------------------------------------------------------
    # Gunner
    # ------------------------------------------------------------------

    def _run_gunner(self, ct: Controller) -> None:
        """R3, both halves.

        (a) Priority is conditional on where this gunner was PLANTED. A gunner
            that spawned inside d<=13 of the enemy core is a killer and ranks
            the core first: measured wild killers put 65.5% of their fire into
            the core and 8.2% into builders, and the frozen probe inverted that.
            A gunner planted further out is a screen gunner and keeps the
            builder-first order -- its measured profile is 44.3% conveyor /
            22.0% builder and it is not aimed at the core at all.

        (b) The frozen probe picked one target and bare-returned when it was not
            fireable. A gunner's ray stops at the first targetable tile, so a
            builder standing behind the core is still in get_attackable_tiles()
            (which ignores occupancy), was still chosen, can_fire() was False,
            and the gunner did nothing that round -- modelled at 36-53% of core
            shots in the games where our heal line was staffed. Now every
            candidate is tried in order and get_gunner_target() is the fallback,
            so a legal shot is never suppressed.
        """
        pos = ct.get_position()
        self._locate(ct)

        if self.killer is None:
            if self.enemy is None:
                self.killer = False
            else:
                gap = pos.distance_squared(nearest_core_tile(pos, self.enemy))
                self.killer = gap <= KILLER_BAND_SQ

        for target in self._target_candidates(ct, pos):
            try:
                if ct.can_fire(target):
                    ct.fire(target)
                    return
            except GameError:
                continue

        if self._fire_fallback(ct):
            return
        self._rotate_to_reacquire(ct, pos)

    def _fire_fallback(self, ct: Controller) -> bool:
        """Whatever the engine itself says is first on our ray. This is the
        second half of the R3 fix: never end a turn holding fire because the
        preferred pick happened to be unreachable.
        """
        try:
            target = ct.get_gunner_target()
        except GameError:
            return False
        if target is None:
            return False
        try:
            bid = ct.get_tile_builder_bot_id(target)
            if bid is None:
                bid = ct.get_tile_building_id(target)
            if bid is not None and ct.get_team(bid) == ct.get_team():
                return False
            if not ct.can_fire(target):
                return False
            ct.fire(target)
        except GameError:
            return False
        return True

    def _target_candidates(self, ct: Controller, pos: Position) -> list:
        """Tiles on this gunner's ray, in the measured priority order for its
        band. Returned as a list so the caller can fall through the whole thing.
        """
        my_team = ct.get_team()
        best_builder = None
        best_core = None
        best_turret = None
        best_eco = None
        best_any = None
        try:
            tiles = ct.get_attackable_tiles()
        except GameError:
            return []
        for tile in tiles:
            if not in_bounds(ct, tile):
                continue
            try:
                tid = ct.get_tile_builder_bot_id(tile)
                is_builder = tid is not None
                if tid is None:
                    tid = ct.get_tile_building_id(tile)
                if tid is None:
                    continue
                if ct.get_team(tid) == my_team:
                    continue
                etype = EntityType.BUILDER_BOT if is_builder else ct.get_entity_type(tid)
            except GameError:
                continue
            key = (pos.distance_squared(tile), tile.x, tile.y)
            if etype == EntityType.BUILDER_BOT:
                if best_builder is None or key < best_builder[0]:
                    best_builder = (key, tile)
            elif etype == EntityType.CORE:
                if best_core is None or key < best_core[0]:
                    best_core = (key, tile)
            elif etype in TURRET_TYPES:
                if best_turret is None or key < best_turret[0]:
                    best_turret = (key, tile)
            elif etype in ECONOMY_TYPES:
                if best_eco is None or key < best_eco[0]:
                    best_eco = (key, tile)
            if best_any is None or key < best_any[0]:
                best_any = (key, tile)

        if self.killer:
            # Core before builder (R3). Economy still ranks above builders,
            # which is D1: 31.1% of wild shots resolve onto one of our
            # conveyors, ~19,100 ammunition chipping 20 HP / 3 Ti buildings.
            order = (best_core, best_turret, best_eco, best_builder, best_any)
        else:
            order = (best_builder, best_core, best_turret, best_eco, best_any)
        out = []
        for entry in order:
            if entry is None:
                continue
            tile = entry[1]
            if tile not in out:
                out.append(tile)
        return out

    def _rotate_to_reacquire(self, ct: Controller, pos: Position) -> None:
        """Turn onto an off-ray target rather than let it peck freely.

        Rotating costs 10 Ti and a cooldown. R4: the measured wild rate is a
        median 2.78 rotations per gunner lifetime, so the throttle is looser
        than the frozen probe's. A killer re-aims onto the core (it is also how
        a D7 mis-aimed doorstep plant fixes itself, at 10 Ti); a screen gunner
        re-aims onto a builder.
        """
        rnd = ct.get_current_round()
        if ct.get_action_cooldown() != 0:
            return
        if rnd - self.last_rotate < ROTATE_MIN_GAP:
            return
        if self.rotations >= ROTATE_MAX_PER_GUNNER:
            return
        if ct.get_global_resources() < max(ROTATE_COST, ROTATE_MIN_TITANIUM):
            return

        my_team = ct.get_team()
        builder = None
        turret = None
        core_seen = False
        try:
            nearby = ct.get_nearby_entities(dist_sq=GUNNER_RANGE_SQ)
        except GameError:
            return
        for eid in nearby:
            try:
                if ct.get_team(eid) == my_team:
                    continue
                etype = ct.get_entity_type(eid)
                if etype == EntityType.CORE:
                    core_seen = True
                    continue
                if etype not in (EntityType.BUILDER_BOT,) + TURRET_TYPES:
                    continue
                where = ct.get_position(eid)
            except GameError:
                continue
            key = (pos.distance_squared(where), where.x, where.y)
            if etype == EntityType.BUILDER_BOT:
                if builder is None or key < builder[0]:
                    builder = (key, where)
            elif turret is None or key < turret[0]:
                turret = (key, where)

        aim = None
        if self.killer and core_seen and self.enemy is not None:
            aim = nearest_core_tile(pos, self.enemy)
        elif builder is not None:
            aim = builder[1]
        elif turret is not None:
            aim = turret[1]
        elif core_seen and self.enemy is not None:
            aim = nearest_core_tile(pos, self.enemy)
        if aim is None:
            return
        facing = pos.direction_to(aim)
        if facing == Direction.CENTRE:
            return
        try:
            if ct.get_direction() == facing:
                return
            if not ct.can_rotate(facing):
                return
            ct.rotate(facing)
            self.last_rotate = rnd
            self.rotations += 1
        except GameError:
            return

    # ------------------------------------------------------------------
    # movement
    # ------------------------------------------------------------------

    def _step_toward(self, ct: Controller, dst: Position | None) -> bool:
        """One cardinal step toward dst; if the preferred axis is blocked, try
        the other one, then the perpendiculars, then backwards. Deterministic.
        """
        if dst is None:
            return False
        if ct.get_move_cooldown() != 0:
            return False
        pos = ct.get_position()
        dx = dst.x - pos.x
        dy = dst.y - pos.y
        if dx == 0 and dy == 0:
            return False

        horiz = Direction.EAST if dx > 0 else Direction.WEST
        vert = Direction.SOUTH if dy > 0 else Direction.NORTH
        prefs = []
        # When stuck, lead with the minor axis instead -- that is what gets a
        # bot around a wall corner rather than grinding into it.
        major_first = abs(dx) >= abs(dy)
        if self.stuck >= 2:
            major_first = not major_first
        if major_first:
            if dx:
                prefs.append(horiz)
            if dy:
                prefs.append(vert)
        else:
            if dy:
                prefs.append(vert)
            if dx:
                prefs.append(horiz)
        for d in CARDINALS:
            if d not in prefs:
                prefs.append(d)

        fresh = []
        stale = []
        for d in prefs:
            try:
                if not ct.can_move(d):
                    continue
            except GameError:
                continue
            dest = pos.add(d)
            if (dest.x, dest.y) in self.recent:
                stale.append(d)
            else:
                fresh.append(d)
        for d in fresh + stale:
            try:
                ct.move(d)
                return True
            except GameError:
                continue
        return False
