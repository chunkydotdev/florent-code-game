"""ouroboros_probe -- Ouroboros-style gunner picket + creep. INSTRUMENT, not a ladder bot.

Provenance: replay-decoded from the team "Ouroboros" over 13 platform replays
(matches 89114461, 9934e516, b498033c, be777476, fcd3e312; decoded 2026-08-07).
Ouroboros is our biggest quantified per-team leak, and until this file existed
there was nothing to gate a counter against.

The shape of that game, as measured, is:

  * GUNNER-ONLY. Across 13 replays and 220+ turret builds, Ouroboros built a
    Gunner every single time -- never a Sentinel, never a Launcher. That is the
    class fingerprint and it is the one thing this file must never break.
  * A normal, growing economy underneath: harvesters on ore with conveyor runs
    home, expanded all game (7 -> 18 harvesters, 15 -> 66 conveyors by r263 on
    eider). It is emphatically NOT a rush -- a probe with no economy would be a
    different instrument entirely.
  * PHASE 1, the picket. One forward Gunner in the corridor between the cores,
    first built r2-r35 (median r22), sited at roughly half the core gap but
    never more than a short walk from home -- which is why the measured standoff
    from the ENEMY core scales with the map: meander dsq 10, eider 25,
    nordkap 49, drumlin 185, atoll 202. It shoots enemy BUILDER BOTS first and
    rotates (10 Ti) to reacquire rather than relocating.
  * PHASE 2, the creep. A new Gunner every ~30 rounds, each one a step closer to
    the enemy core, walking the picket line in: measured dsq-to-enemy-core
    sequence 202 -> 185 -> 148 -> 100 -> 68 -> 52 -> 37 -> 26 -> 17 -> 5 -> 2 -> 1.
    The last 2-4 sit inside dsq 9 of the core footprint and fire it down. First
    core damage lands 30-200 rounds before the kill; kills at r226-r427,
    scaling with map size.
  * Titanium is converted to ammunition aggressively and continuously
    (154-2657 Ti per game; first conversion r3-r44). The gunners never sit dry
    while the bank has titanium.

  The strategy IS the builder attrition: 5/5 of our starting builders were dead
  by r83-r151 on the decoded medium maps, every one of them to gunner fire.

This file exists so counters to that pressure can be gated repeatably. Fidelity
to the decoded pattern beats strength: a probe harsher than the wild exemplar
poisons every verdict taken against it. Where the decode is silent, this file
takes the gentler reading. What it must NOT be is fragile in code terms -- an
uncaught exception permanently deletes the unit for the rest of the match, so
every unit's turn body is wrapped and every mutating call is gated by its
can_*() predicate. (No try/finally anywhere: the platform's bot-code validator
rejects it.)

Deterministic: no random anywhere. Ties break on (distance, x, y).

Seat-general. The decoded games all had Ouroboros as team A, so seat-B
generality comes from the geometry, not from the replays: the enemy core is
taken from a direct sighting when one exists and from point symmetry
(W-2-x, H-2-y) otherwise, and every picket site is expressed as a distance
along the own-core -> enemy-core lane rather than as an absolute coordinate.

Communication store slots:
  0  SLOT_HOME        packed position of our own Core
  1  SLOT_ENEMY       packed position of the enemy Core, once directly sighted
  2  SLOT_ROLE_NEXT   builder role claim counter
  3  SLOT_GUNNERS     gunners built so far == index of the next picket station
  4  SLOT_HARVESTERS  harvesters built so far
  5  SLOT_PICKET_ID   entity id of the builder currently owning picket duty
  6  SLOT_PICKET_PING round+1 that owner last reported alive
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
SLOT_PICKET_ID = 5
SLOT_PICKET_PING = 6

# --- spawns ----------------------------------------------------------------
# Measured: 5 builders standing by r20 in every decoded game, drifting to 6-9
# by r200 as losses are replaced. One per round at the start, then a slow
# trickle -- builder bots carry the same +20% cost scale as gunners, so a
# spammed builder makes every later gunner more expensive.
OPENING_BUILDERS = 5
BUILDER_TRICKLE = 40      # one extra builder per this many rounds...
MAX_BUILDERS_TOTAL = 12   # ...up to this many spawns all game
# If we are down to the core and one unit something has gone badly wrong;
# rebuild regardless of the trickle schedule.
DISTRESS_UNITS = 3
DISTRESS_MAX_SPAWNS = 20

# --- the picket ladder -----------------------------------------------------
# Station 0 sits at FIRST_FRACTION of the core-to-core lane, but never further
# from home than MAX_FIRST_WALK -- that single clamp reproduces the whole
# measured spread of first-gunner standoffs (meander 3.2 tiles from the enemy
# core, eider 5, nordkap 7, drumlin 13.6, atoll 14.2) from one rule.
FIRST_FRACTION = 0.50
MAX_FIRST_WALK = 5.5
# The measured ladder is not one long march: the first several gunners cluster
# in a band around the picket standoff, and only then does the line creep in
# (eider's jump to the core came at r188+). HOLD_STATIONS is the width of that
# band; the remaining stations interpolate from the band standoff down to the
# enemy core's doorstep.
#
# The band spreads ALONG the lane, not just across it, and that is not a
# detail: on eider the exemplar's band was (14,10) r32, (12,10) r35, (15,11)
# r53, (10,10) r76 -- station 1 sits two tiles BEHIND station 0, back toward
# home. That backward station is what covers the corridor behind the picket,
# and in the source replay it is exactly what shot down the Sentinel our
# opponent plants at (13,10) on r11 (7 gunner shots, r44-r49). A band that only
# fans sideways leaves that lane open and the probe's own core dies at r69.
#
# Entries are (extra standoff -- positive is further from the enemy core, i.e.
# nearer home -- perpendicular offset), in tiles.
HOLD_STATIONS = 4
LADDER_STATIONS = 11
BAND_OFFSETS = ((0, 0), (2, 0), (-1, 1), (4, 0))
# Where the creep bottoms out: 1.6 puts the builder on the enemy core's
# doorstep, within building range of a footprint-adjacent tile.
CORE_STANDOFF = 1.6
# The band forms FAST and then the line creeps slowly. Measured first-gunner
# gaps: eider r32/r35, drumlin r22/r24, atoll r31/r33, meander r6/r7 -- the
# first two gunners land 1-3 rounds apart in four of five decoded maps, and
# only then do the gaps stretch to 14-40 rounds. A uniform cadence across the
# band is the wrong shape and leaves the corridor behind the picket open for
# 20 rounds too long.
BAND_DUE = (14, 18, 34, 56)
# ...then one creep station every this many rounds. With the 11-station ladder
# that saturates at the enemy core around r224, inside the measured
# first-core-damage window of r155-r314.
CREEP_INTERVAL = 24
# Once the ladder has saturated at the enemy core the cadence tightens: the
# decoded endgames plant the last 3-5 gunners within ~10 rounds of each other.
SIEGE_INTERVAL = 9
# Perpendicular spread for the saturated stations so the core-killers do not
# all queue for one tile.
SIEGE_SPREAD = (0, 2, -2, 1, -1, 3, -3)

# --- gunners ---------------------------------------------------------------
GUNNER_RANGE_SQ = 13
ROTATE_COST = 10
# Rotating is 10 Ti; the wild bot averages ~1.5 rotations per gunner lifetime,
# so this is deliberately throttled rather than run every round.
ROTATE_MIN_GAP = 5
ROTATE_MIN_TITANIUM = 40

# --- economy ---------------------------------------------------------------
# Growing, not finished: the decoded games end with 5-18 harvesters. The cap is
# a runaway guard, and the cost gate is what actually stops expansion -- once
# the team-wide scale has made a harvester cost this much, the wild bot's
# harvester count flattens too.
ECO_HARVESTER_CAP = 20
HARVESTER_COST_CEILING = 220
MAX_CHAIN = 14
# Builders keep the standing structures repaired. Measured: 74 heal events in
# one decoded game -- 1 Ti for +4 HP is how the exemplar's forward gunners
# survive long enough to become a picket line rather than a sequence of losses.
HEAL_MIN_TITANIUM = 20

# --- ammunition ------------------------------------------------------------
# Measured: first conversion r3-r44, then a balance held around 40-60 all
# midgame with 300+ spikes late; 154-2657 Ti converted per game.
AMMO_FLOOR = 44
# Below this the gunners are within a couple of shots of dry and ammunition
# outranks even the next gunner in the ladder.
AMMO_CRITICAL = 16
AMMO_CEILING = 60
AMMO_RICH_CEILING = 320
AMMO_RICH_TITANIUM = 600
# Titanium the Core will not convert once the ammo floor is already met: the
# next gunner plus a working float for economy and repairs.
ECO_FLOAT = 70
# ...and the much smaller float it holds back while the floor is unmet.
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
        self.is_picket = False
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
        self.cap_tile: Position | None = None
        self.station_idx: int | None = None
        self.station: Position | None = None
        self.explore_idx = 0

        # Turret state
        self.last_rotate = -99

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
        3. Otherwise derive the enemy anchor by point symmetry from home: for
           our Core's NW corner (x, y) on a WxH map the enemy's NW corner is
           (W-2-x, H-2-y). On the mirror-symmetric maps in the pool that guess
           is at most one tile off, and a direct sighting overrides it long
           before any station past the first is placed.
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
    # the picket ladder -- shared geometry, seat-general
    # ------------------------------------------------------------------

    def _station_due_round(self, idx: int, ct: Controller) -> int:
        """Round at which picket station `idx` becomes due.

        Constant cadence down the lane, then a tighter one once the ladder has
        saturated at the enemy core and the remaining gunners are core-killers.
        """
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

    def _standoff(self, ct: Controller, idx: int) -> float:
        """How far short of the enemy core station `idx` stands.

        Flat across the holding band, then a linear walk in.
        """
        first = self._first_standoff(ct)
        if idx < HOLD_STATIONS:
            lane = self._lane(ct)
            back = first + BAND_OFFSETS[idx][0]
            if lane is not None:
                # Never step back past our own core.
                back = min(back, lane[3] - CORE_STANDOFF)
            return max(CORE_STANDOFF, back)
        span = max(1, LADDER_STATIONS - HOLD_STATIONS)
        frac = (idx - HOLD_STATIONS + 1) / float(span)
        return max(CORE_STANDOFF, first + (CORE_STANDOFF - first) * frac)

    def _saturation_index(self, ct: Controller) -> int:
        """First station index whose standoff has bottomed out at the core."""
        for idx in range(LADDER_STATIONS + 1):
            if self._standoff(ct, idx) <= CORE_STANDOFF:
                return idx
        return LADDER_STATIONS

    def _station_site(self, ct: Controller, idx: int) -> Position | None:
        """Where picket station `idx` stands: a point on the own-core ->
        enemy-core lane, `standoff` tiles short of the enemy core, sliding in
        by CREEP_STEP per station until it is on the doorstep. Saturated
        stations fan out perpendicular to the lane so the core-killers do not
        all queue for the same tile.
        """
        lane = self._lane(ct)
        if lane is None:
            return None
        (_hx, _hy), (ex, ey), (ux, uy), _dist = lane
        standoff = self._standoff(ct, idx)
        px = ex - ux * standoff
        py = ey - uy * standoff
        sat = self._saturation_index(ct)
        off = 0
        if idx < HOLD_STATIONS:
            off = BAND_OFFSETS[idx][1]
        elif idx >= sat:
            off = SIEGE_SPREAD[(idx - sat) % len(SIEGE_SPREAD)]
        if off:
            px += -uy * off
            py += ux * off
        w, h = ct.get_map_width(), ct.get_map_height()
        site = Position(
            min(max(int(round(px)), 0), w - 1),
            min(max(int(round(py)), 0), h - 1),
        )
        return self._nudge(ct, site)

    def _lane_reserved(self, ct: Controller, tile: Position) -> bool:
        """Is this tile inside the picket corridor?

        The exemplar's picket stations are never sitting on its own economy --
        on eider its rear gunner stands at (12,10), a tile this probe was
        happily covering with a harvester, which then let the opponent's
        Sentinel plant in the one remaining gap at (13,10) and fire straight
        down row 10 into our core. Harvesters are permanent and cannot be
        rerouted around, so the corridor is kept clear of them; conveyors may
        still cross it and are bulldozed by the picket if they are in the way.
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
        """Builders on a schedule, and titanium into ammunition, always.

        convert_ammo() does not consume the action cooldown, so converting never
        costs a spawn -- it is always tried first.
        """
        pos = ct.get_position()
        if self.home is None:
            self.home = pos
            ct.write_store(SLOT_HOME, pack_pos(pos))
        self._locate(ct)

        self._bank_ammo(ct)

        if ct.get_action_cooldown() != 0:
            return

        rnd = ct.get_current_round()
        allowance = OPENING_BUILDERS
        if rnd > OPENING_BUILDERS:
            allowance += (rnd - OPENING_BUILDERS) // BUILDER_TRICKLE
        allowance = min(allowance, MAX_BUILDERS_TOTAL)
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

    def _bank_ammo(self, ct: Controller) -> None:
        """Aggressive and continuous, from the first round the bank allows.

        The decoded games convert 154-2657 Ti; the balance sits around 40-60 all
        midgame and spikes past 300 once the economy is ahead of the build
        queue. The one thing that must never happen is a gunner sitting dry
        while there is titanium in the bank.
        """
        ammo = ct.get_global_ammo()
        titanium = ct.get_global_resources()
        ceiling = AMMO_RICH_CEILING if titanium >= AMMO_RICH_TITANIUM else AMMO_CEILING
        if ammo >= ceiling:
            return

        # Ammunition outranks everything except getting the opening builders
        # out. The exemplar sat on 4-9 titanium for a hundred rounds at a time
        # while holding 40-50 ammo -- gunners that cannot shoot are the one
        # failure mode this bot never displays. Only once the floor is met does
        # the economy float and the next gunner get reserved out.
        reserve = EMERGENCY_FLOAT
        if self.spawned < OPENING_BUILDERS:
            reserve += (OPENING_BUILDERS - self.spawned) * ct.get_builder_bot_cost()
        if ammo >= AMMO_CRITICAL:
            # Above the critical line the ladder keeps priority over topping
            # ammunition up: the exemplar holds ~45 ammo AND keeps planting.
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

        if self.prev_pos is not None:
            if pos == self.prev_pos:
                self.stuck += 1
            else:
                self.stuck = 0
        self.prev_pos = pos
        # Short tabu list. Without it a builder that meets a blocker on its
        # preferred axis steps aside, finds the axis clear again from the new
        # tile, steps back, and 2-cycles there for the rest of the match --
        # `stuck` never fires because the bot is moving every round.
        self.recent.append((pos.x, pos.y))
        if len(self.recent) > 4:
            self.recent.pop(0)

        self._picket_latch(ct, rnd)

        if self.is_picket or self._assist_open(ct):
            self._run_picket(ct, rnd, pos)
        else:
            self._run_eco(ct, rnd, pos)

    def _assist_open(self, ct: Controller) -> bool:
        """Do extra builders join the push?

        Once the line has left the holding band, one builder cannot walk the
        remaining stations into enemy territory and survive -- and the exemplar
        does not ask it to. Its endgame arrives in bursts (drumlin: gunners
        planted r410, r411, r413, r417; eider: r224, r225, r226, r230), which
        is several builders pushing at once and 2-4 gunners ending up inside
        dsq 9 of the core. Every third builder joins from that point on; the
        rest keep the economy growing, as the exemplar's does all game.
        """
        return (ct.read_store(SLOT_GUNNERS) >= HOLD_STATIONS + 2
                and (self.role or 0) % 3 == 1)

    def _picket_latch(self, ct: Controller, rnd: int) -> None:
        """Exactly one live builder owns picket duty at a time.

        The owner republishes a heartbeat every round; when it dies and the
        heartbeat goes stale any builder may claim the slot. Several may claim
        on the same round -- store writes are last-writer-wins, so exactly one
        value lands and exactly one builder reads its own id back next round.
        """
        my_id = ct.get_id()
        owner = ct.read_store(SLOT_PICKET_ID)
        ping = ct.read_store(SLOT_PICKET_PING)

        if owner == my_id:
            self.is_picket = True
            ct.write_store(SLOT_PICKET_PING, rnd + 1)
            return

        self.is_picket = False
        vacant = ping == 0 or rnd - (ping - 1) > 3
        if vacant:
            ct.write_store(SLOT_PICKET_ID, my_id)
            ct.write_store(SLOT_PICKET_PING, rnd + 1)

    # -- the picket builder ---------------------------------------------

    def _run_picket(self, ct: Controller, rnd: int, pos: Position) -> None:
        """Walk the picket line in, planting one Gunner per station.

        The station index is read from the shared gunner counter, not held
        locally, so a replacement picket builder picks the ladder up exactly
        where its predecessor left it.
        """
        if self.home is None or self.enemy is None:
            return
        idx = ct.read_store(SLOT_GUNNERS)
        if idx != self.station_idx:
            self.station_idx = idx
            self.station = None
        if self.station is None:
            self.station = self._station_site(ct, idx)
        station = self.station
        if station is None:
            self._run_eco(ct, rnd, pos)
            return

        due = self._station_due_round(idx, ct)
        near = pos.distance_squared(station) <= 2
        if near:
            # Holding station on purpose is not being stuck; without this the
            # wait between stations would trip the can't-reach-it fallback.
            self.stuck = 0

        if rnd >= due and ct.get_action_cooldown() == 0:
            if ct.get_global_resources() >= ct.get_gunner_cost():
                # Build from the station tile, or from wherever we have got
                # stuck within sight of it -- a picket that never plants is
                # worse than one planted a tile short.
                if near or (self.stuck >= 6 and pos.distance_squared(station) <= 20):
                    if self._plant_gunner(ct, pos):
                        ct.write_store(SLOT_GUNNERS, idx + 1)
                        self.station_idx = idx + 1
                        self.station = None
                        return

        # Repair the station we are standing on while waiting for the next one.
        if not near or rnd < due:
            if self._step_toward(ct, station):
                return
        if ct.get_action_cooldown() == 0 and ct.get_global_resources() >= HEAL_MIN_TITANIUM:
            self._try_heal(ct, pos)

    def _plant_gunner(self, ct: Controller, pos: Position) -> bool:
        """Gunner on an orthogonally adjacent tile, facing the enemy Core.

        The Gunner fires a single-tile-wide ray, so the facing is what matters,
        not the position; it re-aims later by rotating rather than relocating.
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
            facing = site.direction_to(nearest_core_tile(site, self.enemy))
            if facing == Direction.CENTRE:
                continue
            key = (site.distance_squared(self.enemy), site.x, site.y)
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

    # -- economy builders -----------------------------------------------

    def _run_eco(self, ct: Controller, rnd: int, pos: Position) -> None:
        """Harvester on ore, conveyor run home, repeat. Grows all game."""
        self._scan_ore(ct)
        if self._cpu_exhausted(ct):
            return

        if self.stage == "ore":
            self._eco_seek_ore(ct, pos)
        elif self.stage == "lay":
            self._eco_lay(ct, pos)
        elif self.stage == "cap":
            self._eco_cap(ct, pos)
        else:
            self._eco_idle(ct, pos)

    def _eco_expansion_open(self, ct: Controller) -> bool:
        if ct.read_store(SLOT_HARVESTERS) >= ECO_HARVESTER_CAP:
            return False
        # The team-wide cost scale eventually prices harvesters out; the wild
        # bot's harvester count flattens at the same place for the same reason.
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
            # Keeping the picket corridor clear never outranks having an
            # economy at all: on maps where the home ore all sits in the
            # corridor (atoll from seat B) the discipline starved the probe to
            # two harvesters and it lost on r145.
            free = reserved
        if not free:
            self._step_toward(ct, self._explore_target(ct, pos))
            return
        # Nearest to HOME, not to the builder. The exemplar's economy grows
        # outward from its core in short runs (eider: 15 conveyors carrying 7
        # harvesters by r20, a 2:1 ratio); ranking by distance to the builder
        # walks it steadily away from home and doubles the conveyor run for
        # every harvester, which is where this probe's mining rate was going.
        anchor = self.home if self.home is not None else pos
        free.sort(key=lambda t: (t.distance_squared(anchor), t.x, t.y))
        # Each builder prefers a different one of the nearest few, so they do
        # not all queue for the same tile.
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
        ever box it in.
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
        """Build the final conveyor, the one that actually faces the Core.

        An unfinished chain delivers exactly nothing (measured), so this step is
        not cosmetic -- it is the whole economy.
        """
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
        # Step away from the Core -- back down the chain we just laid, which is
        # conveyor and therefore passable.
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

    def _eco_idle(self, ct: Controller, pos: Position) -> None:
        """Expansion is priced out for now: keep the structures repaired and
        re-check every few rounds in case a harvester died and freed the scale.
        """
        if ct.get_current_round() % 8 == 0 and self._eco_expansion_open(ct):
            self.stage = "ore"
            return
        if ct.get_action_cooldown() == 0 and ct.get_global_resources() >= HEAL_MIN_TITANIUM:
            if self._try_heal(ct, pos):
                return
        hurt = self._damaged_friendly(ct, pos)
        if hurt is not None and pos.distance_squared(hurt) > 1:
            self._step_toward(ct, hurt)

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
        """Enemy BUILDER BOT first, then the enemy Core, then their economy.

        The builder attrition is the strategy -- 5/5 of our starting builders
        were dead by r83-r151 in the decoded medium-map games, every one to
        gunner fire -- so a builder on the ray always outranks the Core sitting
        behind it. When nothing is on the ray the gunner ROTATES to reacquire;
        it never relocates.
        """
        pos = ct.get_position()
        self._locate(ct)

        target = self._pick_target(ct, pos)
        if target is not None:
            try:
                if ct.can_fire(target):
                    ct.fire(target)
                    return
            except GameError:
                return
            return

        self._rotate_to_reacquire(ct, pos)

    def _pick_target(self, ct: Controller, pos: Position) -> Position | None:
        """Best tile on this gunner's ray, by the decoded priority order."""
        my_team = ct.get_team()
        best_builder = None
        best_core = None
        best_turret = None
        best_eco = None
        best_any = None
        try:
            tiles = ct.get_attackable_tiles()
        except GameError:
            return None
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
        # Builder first (the attrition is the strategy), then the Core, then
        # whatever is shooting back -- a Sentinel planted inside our half will
        # take the Core apart in ~56 rounds if nobody ever turns around --
        # then their economy.
        choice = best_builder or best_core or best_turret or best_eco or best_any
        return choice[1] if choice is not None else None

    def _rotate_to_reacquire(self, ct: Controller, pos: Position) -> None:
        """Turn onto an off-ray enemy builder rather than let it peck freely.

        Rotating costs 10 Ti and a cooldown, and the wild bot averages only
        ~1.5 rotations per gunner lifetime, so this is throttled hard: only for
        a builder or the Core, only out of surplus, and never twice in a row.
        """
        rnd = ct.get_current_round()
        if ct.get_action_cooldown() != 0:
            return
        if rnd - self.last_rotate < ROTATE_MIN_GAP:
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
        if builder is not None:
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

        # Legal moves, preferring tiles we have not just come from: that is what
        # walks a builder around a blocker instead of bouncing off it forever.
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
