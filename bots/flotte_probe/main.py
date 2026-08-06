"""flotte_probe -- Flotte-style economic strangulation. INSTRUMENT, not a ladder bot.

Provenance: replay-extracted from the 1776-rated team "The Flotte Experience",
platform match 0a88ca71 games 3 and 4, which beat our live v7 on meander (r151)
and eider (r159) by starving its economy rather than out-fighting it
(extracted 2026-08-06).

The shape of that game is: a deliberately small, deliberately finished economy
(exactly three harvesters, shortest possible conveyor runs, never expanded), one
or two forward Gunners screening the approach lane, and -- the payload -- a
single Builder Bot that walks into the enemy's economic footprint around r15-20
and never comes home. It kills harvesters with the 2-damage builder melee, one
after another, loitering on the wreckage to re-kill rebuilds. When the enemy has
no harvester left standing, two Sentinels go up deep in their territory from two
different angles and take the Core apart at leisure.

This file exists so a saboteur-INTERCEPT defence can be gated against that
pressure repeatably: the instrument is only useful if the saboteur genuinely
hunts harvesters and genuinely loiters, so that behaviour is faithful even where
it is strategically dumb. What it must NOT be is fragile in code terms -- an
uncaught exception permanently deletes the unit for the rest of the match, so
every unit's turn body is wrapped and every mutating call is gated by its
can_*() predicate. (No try/finally anywhere: the platform's bot-code validator
rejects it.)

Deterministic: no random anywhere. Ties break on (distance, x, y).

Round budget from the source replays. These are TARGETS ONLY -- every stage
below triggers on state, never on a round number, except the two windows the
recipe states explicitly (the forward-Gunner window and the harvester-quiet
timer):

  r0-r3     Core spawns exactly 4 builders, one per round
  r4-r8     builders 1-3 each plant one harvester on the nearest ore and lay the
            shortest conveyor run back to the Core. That is the whole economy,
            forever -- it is never expanded
  r12-r19   the freed eco builders plant 1-2 forward Gunners on the
            own-Core -> enemy-Core line: a screener at ~18% of the gap and a
            midfielder at ~60%. Gunners rotate to reacquire; they never relocate
  r15-r20   builder #4 -- THE SABOTEUR, never assigned economy -- reaches the
            enemy's economic footprint, skirting the Core neighbourhood
  ...       saboteur kills harvesters (priority) then conveyors/splitters,
            never disengaging a damaged target, loitering on the kill zone
  +15       once no enemy harvester has been seen by ANY of our units for 15
            consecutive rounds, the finishing push: 2 Sentinels deep in enemy
            territory from two different approach angles, fire staggered on
            alternate rounds so the Core takes damage every round

Ammunition: the Core banks a trickle continuously from r0 so that ~60+ is
already sitting there when the push starts -- a Sentinel that has to wait for
its first 10 ammo has given the enemy a free rebuild window.

Communication store slots. All 16 are this bot's. Note that the store cannot
represent a zero: a slot holding 0 is indistinguishable from a slot nobody has
written (docs/game-model.md, measured). Positions are therefore packed with a +1
offset and round numbers are stored as round+1; only genuine counters (which
legitimately start at zero) are stored raw.

  0  SLOT_HOME          packed position of our own Core
  1  SLOT_ENEMY         packed position of the enemy Core, once directly sighted
  2  SLOT_ROLE_NEXT     next builder role index, +1 (0 = nobody has claimed yet)
  3  SLOT_HARV_SEEN     round+1 at which any unit last saw an enemy harvester
  4  SLOT_SAB_PING      round+1 at which the saboteur last confirmed it is alive
  5  SLOT_SAB_ARRIVED   1 once the saboteur has reached enemy territory
  6  SLOT_PUSH          1 once the finishing push has been triggered (latched)
  7  SLOT_SENTINELS     sentinels planted for the push
  8  SLOT_HARVESTERS    harvesters we have built (hard-capped at ECO_HARVESTERS)
  9  SLOT_GUNNERS       forward gunners planted
 10  SLOT_TURRET_NEXT   next sentinel stagger index, +1
 11  SLOT_KILLZONE      packed position of the saboteur's last kill
"""

import sys

from fcode import Controller, Direction, EntityType, Environment, GameError, Position

# --- store slots -----------------------------------------------------------
SLOT_HOME = 0
SLOT_ENEMY = 1
SLOT_ROLE_NEXT = 2
SLOT_HARV_SEEN = 3
SLOT_SAB_PING = 4
SLOT_SAB_ARRIVED = 5
SLOT_PUSH = 6
SLOT_SENTINELS = 7
SLOT_HARVESTERS = 8
SLOT_GUNNERS = 9
SLOT_TURRET_NEXT = 10
SLOT_KILLZONE = 11

# --- economy ---------------------------------------------------------------
# "Exactly 3 harvesters on nearest ore, shortest conveyor runs to core. Never
# expand beyond this." This is the recipe's defining economic choice and the
# reason the bot can afford to spend its fourth builder on sabotage forever.
ECO_HARVESTERS = 3
ECO_BUILDERS = 3
# A run longer than this is not a "shortest run" -- the ore was the wrong ore.
MAX_CHAIN = 24

# --- spawns ----------------------------------------------------------------
# 4 builders, r0-r3. #4 is the saboteur.
OPENING_BUILDERS = 4
SABOTEUR_ROLE = 3
# The saboteur dies in enemy territory eventually and the enemy rebuilds
# harvesters behind it. Deviation from the literal recipe: up to two
# replacements, spawned only once the previous one has stopped pinging.
MAX_BUILDERS = 6
SAB_STALE_ROUNDS = 3

# --- forward gunners -------------------------------------------------------
GUNNER_TARGET = 2
GUNNER_WINDOW_START = 12
# Fractions of the own-Core -> enemy-Core gap: screener, then midfield.
GUNNER_FRACTIONS = (0.18, 0.60)
GUNNER_RANGE_SQ = 13
# Rotating costs 10 Ti and a cooldown; only worth it for a real sighting.
ROTATE_COST = 10

# --- the finishing push ----------------------------------------------------
SENTINEL_TARGET = 2
SENTINEL_RANGE_SQ = 32
# "no enemy harvester visible to our units for ~15 consecutive rounds"
HARV_QUIET_ROUNDS = 15
# If we never saw one at all, the trigger still has to fire eventually -- but
# only once someone has actually been over there to look.
PUSH_FALLBACK_ROUND = 60
# Second Sentinel comes in off-axis so one blocker cannot eat both lines.
LATERAL_OFFSET = 3
REPOSITION_MAX_RNDS = 12

# --- ammunition ------------------------------------------------------------
# Banked continuously and modestly from r0: by the time the push triggers there
# must be ~60+ ammo (6 Sentinel shots) already sitting there.
AMMO_CEILING = 120
AMMO_CHUNK = 6
# Titanium the Core will not convert: economy still owed, plus a working float
# for the saboteur's 2-Ti melee attacks and repairs.
SAB_FLOAT = 40

# --- saboteur --------------------------------------------------------------
ATTACK_COST = 2
# Approach aiming point: this far off the core-to-core axis, and never closer
# than this to the enemy Core itself ("avoid the direct centre/core
# neighbourhood" -- their economy sits beside the Core, not on it).
APPROACH_OFFSET = 4
CORE_STANDOFF_SQ = 9
# Loiter loop around the last kill, 3-5 tiles per the recipe.
LOITER_RADIUS = 2
LOITER_DWELL = 3

# Bail at a phase boundary rather than let the engine truncate a statement.
CPU_BUDGET_US = 7000

CARDINALS = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)
ECONOMY_TYPES = (EntityType.HARVESTER, EntityType.CONVEYOR, EntityType.SPLITTER)


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
        self.stage = "ore"
        self.prev_pos: Position | None = None
        self.stuck = 0
        self.known_ore: set = set()
        self.ore_target: Position | None = None
        self.harvester_pos: Position | None = None
        self.trail_prev: Position | None = None
        self.chain_tiles: set = set()
        self.chain_len = 0
        self.cap_tile: Position | None = None
        self.gunner_spot: Position | None = None
        self.built_sentinels = 0
        self.reposition_target: Position | None = None
        self.reposition_start = 0

        # Saboteur state
        self.approach: Position | None = None
        self.target_id: int | None = None
        self.target_pos: Position | None = None
        self.killzone: Position | None = None
        self.loiter_idx = 0
        self.loiter_since = 0

        # Turret state
        self.stagger: int | None = None

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
        elif etype == EntityType.SENTINEL:
            self._run_sentinel(ct)

    def _cpu_exhausted(self, ct: Controller) -> bool:
        return ct.get_cpu_time_elapsed() >= CPU_BUDGET_US

    # ------------------------------------------------------------------
    # shared map / intel
    # ------------------------------------------------------------------

    def _locate(self, ct: Controller) -> None:
        """Establish home and enemy Core positions as cheaply as possible.

        1. Sight them directly if they are in vision.
        2. Otherwise read whatever the store already knows.
        3. Otherwise derive the enemy anchor by symmetry from home: for our
           Core's NW corner (x, y) on a WxH map the enemy's NW corner is
           (W-2-x, H-2-y).
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

    def _report_enemy_economy(self, ct: Controller) -> list:
        """Scan vision for enemy economic structures and publish the sighting.

        Every unit does this, not just the saboteur: the push trigger is
        "no enemy harvester visible to OUR UNITS for 15 rounds", so a forward
        Gunner that can still see one has to be able to veto the push.
        Returns [(entity_type, id, pos)] for enemy economy in vision.
        """
        my_team = ct.get_team()
        found = []
        saw_harvester = False
        try:
            nearby = ct.get_nearby_buildings()
        except GameError:
            return found
        for bid in nearby:
            try:
                if ct.get_team(bid) == my_team:
                    continue
                etype = ct.get_entity_type(bid)
                if etype not in ECONOMY_TYPES:
                    continue
                where = ct.get_position(bid)
            except GameError:
                continue
            found.append((etype, bid, where))
            if etype == EntityType.HARVESTER:
                saw_harvester = True
        if saw_harvester:
            ct.write_store(SLOT_HARV_SEEN, ct.get_current_round() + 1)
        return found

    def _push_active(self, ct: Controller) -> bool:
        """Latched state trigger for the finishing push."""
        if ct.read_store(SLOT_PUSH) == 1:
            return True
        if ct.read_store(SLOT_SAB_ARRIVED) != 1:
            return False
        rnd = ct.get_current_round()
        seen = ct.read_store(SLOT_HARV_SEEN)
        if seen > 0:
            return rnd - (seen - 1) >= HARV_QUIET_ROUNDS
        return rnd >= PUSH_FALLBACK_ROUND

    # ------------------------------------------------------------------
    # Core
    # ------------------------------------------------------------------

    def _run_core(self, ct: Controller) -> None:
        """Four builders, a small permanent economy, and a steady ammo trickle.

        convert_ammo() does not consume the action cooldown, so converting never
        costs a spawn -- it is always tried first.
        """
        pos = ct.get_position()
        if self.home is None:
            self.home = pos
            ct.write_store(SLOT_HOME, pack_pos(pos))
        self._locate(ct)
        self._report_enemy_economy(ct)

        rnd = ct.get_current_round()
        if self._push_active(ct) and ct.read_store(SLOT_PUSH) != 1:
            ct.write_store(SLOT_PUSH, 1)

        self._bank_ammo(ct)

        if ct.get_action_cooldown() != 0:
            return
        if self.spawned >= MAX_BUILDERS:
            return
        if self.spawned >= OPENING_BUILDERS:
            # Replacement saboteurs only: the recipe never wants a defensive
            # builder, and the economy is finished and never expanded.
            ping = ct.read_store(SLOT_SAB_PING)
            # ping == 0 means "has never reported", which is also true for the
            # two rounds between spawning the saboteur and its first buffered
            # write landing -- replacing on that would spawn a second saboteur
            # immediately, every game.
            if ping == 0:
                if rnd < OPENING_BUILDERS + SAB_STALE_ROUNDS + 2:
                    return
            elif rnd - (ping - 1) <= SAB_STALE_ROUNDS:
                return
            if ct.read_store(SLOT_SENTINELS) >= SENTINEL_TARGET:
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
        """A steady trickle from r0 so the push never waits on its first shot."""
        ammo = ct.get_global_ammo()
        if ammo >= AMMO_CEILING:
            return
        harvesters = ct.read_store(SLOT_HARVESTERS)
        gunners = ct.read_store(SLOT_GUNNERS)
        sentinels = ct.read_store(SLOT_SENTINELS)

        reserve = SAB_FLOAT
        if harvesters < ECO_HARVESTERS:
            reserve += (ECO_HARVESTERS - harvesters) * ct.get_harvester_cost()
            reserve += (ECO_HARVESTERS - harvesters) * 6 * ct.get_conveyor_cost()
        if gunners < GUNNER_TARGET:
            reserve += (GUNNER_TARGET - gunners) * ct.get_gunner_cost()
        if sentinels < SENTINEL_TARGET:
            reserve += (SENTINEL_TARGET - sentinels) * ct.get_sentinel_cost()
        if self.spawned < OPENING_BUILDERS:
            reserve += (OPENING_BUILDERS - self.spawned) * ct.get_builder_bot_cost()

        spare = ct.get_global_resources() - reserve
        amount = min(AMMO_CHUNK, AMMO_CEILING - ammo, spare)
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

        if self.role >= SABOTEUR_ROLE:
            self._run_saboteur(ct, rnd, pos)
        else:
            self._run_eco(ct, rnd, pos)

    # -- economy builder ------------------------------------------------

    def _run_eco(self, ct: Controller, rnd: int, pos: Position) -> None:
        self._report_enemy_economy(ct)
        self._scan_ore(ct)

        if self._push_active(ct) and self.stage in ("gunner", "idle"):
            self.stage = "push"

        if self._cpu_exhausted(ct):
            return

        if self.stage == "ore":
            self._eco_seek_ore(ct, pos)
        elif self.stage == "lay":
            self._eco_lay(ct, pos)
        elif self.stage == "cap":
            self._eco_cap(ct, pos)
        elif self.stage == "gunner":
            self._eco_gunner(ct, rnd, pos)
        elif self.stage == "push":
            self._push_turn(ct, rnd, pos)
        else:
            self._eco_idle(ct, pos)

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
        """Walk to the nearest free ore and plant a harvester on it.

        "Exactly 3 harvesters on nearest ore" -- so the ranking is by distance
        to our own Core, not to this builder, and the count is hard-capped.
        """
        if ct.read_store(SLOT_HARVESTERS) >= ECO_HARVESTERS:
            self.stage = "gunner"
            return
        anchor = self.home if self.home is not None else pos

        # Each of the three eco builders prefers a different ore by rank, so
        # they do not pile onto the same tile; occupancy re-picks on collision.
        cands = sorted(
            (Position(x, y) for (x, y) in self.known_ore),
            key=lambda t: (t.distance_squared(anchor), t.x, t.y),
        )
        free = []
        for tile in cands:
            try:
                if ct.get_tile_building_id(tile) is not None:
                    continue
            except GameError:
                pass  # out of vision: assume still free, re-checked on arrival
            free.append(tile)
        if not free:
            self._step_toward(ct, self._explore_target(ct, pos))
            return
        rank = min(self.role, len(free) - 1)
        self.ore_target = free[rank]

        if ct.get_action_cooldown() == 0 and ct.get_global_resources() >= ct.get_harvester_cost():
            for tile in free[: ECO_HARVESTERS + 1]:
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
                self._begin_chain(ct, pos)
                return
        self._step_toward(ct, self.ore_target)

    def _begin_chain(self, ct: Controller, pos: Position) -> None:
        """After planting a harvester, decide whether it needs a conveyor run.

        A harvester orthogonally adjacent to the Core delivers straight into it
        (harvesters output to any adjacent accepting building), so the shortest
        possible run is no run at all.
        """
        self.chain_len = 0
        self.trail_prev = None
        self.chain_tiles = set()
        if self.home is not None and self.harvester_pos is not None:
            if adjacent_core_tile(self.harvester_pos, self.home) is not None:
                self.stage = "gunner"
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
            self.stage = "gunner"
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
            self.stage = "gunner"

    def _eco_cap(self, ct: Controller, pos: Position) -> None:
        """Build the final conveyor, the one that actually faces the Core.

        An unfinished chain delivers exactly nothing (measured), so this step is
        not cosmetic -- it is the whole economy.
        """
        if self.home is None or self.cap_tile is None or self.stuck >= 6:
            self.stage = "gunner"
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
            self.stage = "gunner"
            return
        if self._build_link(ct, self.cap_tile, core_tile):
            self.stage = "gunner"
        elif self.stuck >= 4:
            self.stage = "gunner"

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
        away = Position(pos.x - (core_tile.x - pos.x), pos.y - (core_tile.y - pos.y))
        order = [away.x - pos.x, away.y - pos.y]
        prefs = []
        if order[0] > 0:
            prefs.append(Direction.EAST)
        elif order[0] < 0:
            prefs.append(Direction.WEST)
        if order[1] > 0:
            prefs.append(Direction.SOUTH)
        elif order[1] < 0:
            prefs.append(Direction.NORTH)
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

    def _eco_gunner(self, ct: Controller, rnd: int, pos: Position) -> None:
        """Plant the forward Gunners in the r12-19 window, then stand by.

        "1-2 in the r12-19 window along the own-core -> enemy-core line: one at
        ~15-20% of the distance (screener), one at ~50-70% (midfield)."
        """
        if self.home is None or self.enemy is None:
            return
        built = ct.read_store(SLOT_GUNNERS)
        # Which lane slot this builder owns is decided by its role, not by the
        # store counter: store writes land a round late, so two builders that
        # finish their chains on the same round would both read "0 built" and
        # both plant the screener, leaving midfield empty forever.
        idx = self.role
        if built >= GUNNER_TARGET or idx >= min(GUNNER_TARGET, len(GUNNER_FRACTIONS)):
            self.stage = "idle"
            return
        if rnd < GUNNER_WINDOW_START:
            return

        if self.gunner_spot is None:
            self.gunner_spot = self._lane_point(ct, GUNNER_FRACTIONS[idx])
        spot = self.gunner_spot
        if spot is None:
            self.stage = "idle"
            return

        if ct.get_action_cooldown() == 0 and pos.distance_squared(spot) <= 2:
            if ct.get_global_resources() >= ct.get_gunner_cost():
                if self._plant_gunner(ct, pos):
                    ct.write_store(SLOT_GUNNERS, built + 1)
                    self.gunner_spot = None
                    self.stage = "idle"
                    return
        if pos.distance_squared(spot) <= 2 and self.stuck >= 5:
            self.gunner_spot = None
            self.stage = "idle"
            return
        self._step_toward(ct, spot)

    def _lane_point(self, ct: Controller, fraction: float) -> Position | None:
        """A point at `fraction` of the way along the own-Core -> enemy-Core
        line, nudged to the nearest in-bounds tile."""
        if self.home is None or self.enemy is None:
            return None
        hx = self.home.x + 0.5
        hy = self.home.y + 0.5
        ex = self.enemy.x + 0.5
        ey = self.enemy.y + 0.5
        px = int(round(hx + (ex - hx) * fraction))
        py = int(round(hy + (ey - hy) * fraction))
        w, h = ct.get_map_width(), ct.get_map_height()
        return Position(min(max(px, 0), w - 1), min(max(py, 0), h - 1))

    def _plant_gunner(self, ct: Controller, pos: Position) -> bool:
        """Gunner on an adjacent tile, facing down the lane at the enemy Core.

        The Gunner fires a single-tile-wide ray, so the facing is what matters,
        not the position; it re-aims later by rotating rather than relocating.
        """
        if self.enemy is None:
            return False
        best = None
        for d in CARDINALS:
            site = pos.add(d)
            if not in_bounds(ct, site):
                continue
            facing = site.direction_to(nearest_core_tile(site, self.enemy))
            if facing == Direction.CENTRE:
                continue
            try:
                if not ct.can_build_gunner(site, facing):
                    continue
            except GameError:
                continue
            key = (site.distance_squared(self.enemy), site.x, site.y)
            if best is None or key < best[0]:
                best = (key, site, facing)
        if best is None:
            return False
        try:
            ct.build_gunner(best[1], best[2])
        except GameError:
            return False
        return True

    def _eco_idle(self, ct: Controller, pos: Position) -> None:
        """Economy finished and never expanded: keep the standing structures
        repaired, and hold position behind the screener. No second economy, no
        defensive building -- that is the whole point of the recipe.
        """
        if ct.get_action_cooldown() == 0 and self._try_heal(ct, pos):
            return
        if self.home is not None:
            hurt = self._damaged_friendly(ct, pos)
            if hurt is not None and pos.distance_squared(hurt) > 1:
                self._step_toward(ct, hurt)

    def _try_heal(self, ct: Controller, pos: Position) -> bool:
        if ct.get_global_resources() < 4:
            return False
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
                if ct.get_entity_type(bid) == EntityType.CORE:
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
        """No ore known yet: walk down the lane, where the ore usually is."""
        spot = self._lane_point(ct, 0.3)
        return spot if spot is not None else Position(pos.x + 1, pos.y)

    # ------------------------------------------------------------------
    # THE SABOTEUR -- the payload
    # ------------------------------------------------------------------

    def _run_saboteur(self, ct: Controller, rnd: int, pos: Position) -> None:
        """Cross into the enemy's economy and never come home.

        Order of business every single round:
          1. finish whatever is already damaged and adjacent -- never disengage
          2. otherwise hit an adjacent harvester, else an adjacent conveyor
          3. otherwise walk at the nearest enemy harvester, else its conveyors
          4. otherwise cross toward the enemy's economic footprint
          5. once there is nothing left to kill, loiter on the kill zone so
             rebuilds die as fast as they go up
        """
        ct.write_store(SLOT_SAB_PING, rnd + 1)
        sightings = self._report_enemy_economy(ct)

        if self.enemy is not None and ct.read_store(SLOT_SAB_ARRIVED) != 1:
            if pos.distance_squared(self.enemy) <= 64:
                ct.write_store(SLOT_SAB_ARRIVED, 1)

        # The finishing push takes priority over sabotage: by then there is
        # nothing left to sabotage, and the Sentinels are what wins.
        if self._push_active(ct) and ct.read_store(SLOT_SENTINELS) < SENTINEL_TARGET:
            self._push_turn(ct, rnd, pos)
            return

        if self._cpu_exhausted(ct):
            return

        # 1 + 2: attack. Builder melee is fire() on an orthogonally adjacent
        # tile, 2 damage for 2 Ti, buildings only.
        #
        # While a harvester is in sight, an adjacent CONVEYOR is not a target:
        # a conveyor is 3 Ti to replace and the enemy rebuilds it the same
        # round, whereas a dead harvester is 20 Ti plus a permanent +5% scale
        # and stops the income at its source. Standing in their conveyor field
        # chipping 20 HP relays is how a saboteur looks busy and strangles
        # nothing. The restriction lifts if we cannot close on the harvester.
        harv_visible = any(e[0] == EntityType.HARVESTER for e in sightings)
        if ct.get_action_cooldown() == 0 and ct.get_global_resources() >= ATTACK_COST:
            if self._attack_adjacent(ct, pos, harv_visible and self.stuck < 3):
                return

        # 3: close on the nearest enemy economy, harvesters first.
        goal = self._hunt_target(ct, pos, sightings)
        if goal is not None:
            self.target_pos = goal
            self._step_toward(ct, goal)
            return
        self.target_id = None
        self.target_pos = None

        # 4 + 5: cross, then loiter. Never retreat, never return home.
        self._cross_or_loiter(ct, rnd, pos)

    def _attack_adjacent(self, ct: Controller, pos: Position, harvesters_only: bool = False) -> bool:
        """Hit an adjacent enemy building. Priority: the target already damaged
        (never disengage), then HARVESTER, then conveyor/splitter, then anything
        else that happens to be in the way.
        """
        my_team = ct.get_team()
        best = None
        for d in CARDINALS:
            tile = pos.add(d)
            if not in_bounds(ct, tile):
                continue
            try:
                bid = ct.get_tile_building_id(tile)
                if bid is None or ct.get_team(bid) == my_team:
                    continue
                etype = ct.get_entity_type(bid)
                hp = ct.get_hp(bid)
                if not ct.can_fire(tile):
                    continue
            except GameError:
                continue
            if bid == self.target_id:
                rank = 0  # already wounded by us: finish it
            elif etype == EntityType.HARVESTER:
                rank = 1
            elif etype in (EntityType.CONVEYOR, EntityType.SPLITTER):
                rank = 2
            else:
                rank = 3
            if harvesters_only and rank > 1:
                continue
            key = (rank, hp, tile.x, tile.y)
            if best is None or key < best[0]:
                best = (key, tile, bid, hp, etype)
        if best is None:
            return False

        _, tile, bid, hp, etype = best
        try:
            ct.fire(tile)
        except GameError:
            return False
        self.target_id = bid
        self.target_pos = tile
        if hp <= 2:
            # That shot killed it: this is the kill zone to loiter on, because
            # a rebuilt harvester goes back on the same ore tile.
            self.killzone = tile
            self.loiter_since = ct.get_current_round()
            ct.write_store(SLOT_KILLZONE, pack_pos(tile))
            self.target_id = None
            self.target_pos = None
        return True

    def _hunt_target(self, ct: Controller, pos: Position, sightings: list) -> Position | None:
        """Nearest visible enemy economy: harvesters strictly before conveyors.

        A target already under the hammer outranks everything -- "never
        disengage a damaged target" is the line in the recipe that makes the
        difference between chipping and killing.
        """
        if self.target_id is not None:
            for etype, bid, where in sightings:
                if bid == self.target_id:
                    return where
            self.target_id = None

        best = None
        for etype, bid, where in sightings:
            rank = 0 if etype == EntityType.HARVESTER else 1
            key = (rank, pos.distance_squared(where), where.x, where.y)
            if best is None or key < best[0]:
                best = (key, where, bid)
        if best is None:
            return None
        # Do not adopt a target we are already standing next to -- the attack
        # branch above owns that case; this one is purely for walking.
        if abs(best[1].x - pos.x) + abs(best[1].y - pos.y) <= 1:
            return None
        return best[1]

    def _cross_or_loiter(self, ct: Controller, rnd: int, pos: Position) -> None:
        """Cross toward the enemy's economic footprint, then orbit the wreckage.

        The approach point sits off the core-to-core axis and outside the Core
        neighbourhood: their harvesters are beside their Core, and walking down
        the middle only feeds their turrets.
        """
        if self.killzone is None:
            stored = unpack_pos(ct.read_store(SLOT_KILLZONE))
            if stored is not None:
                self.killzone = stored
                self.loiter_since = rnd

        if self.killzone is not None:
            self._loiter(ct, rnd, pos, self.killzone)
            return

        if self.enemy is None:
            return
        if self.approach is None:
            self.approach = self._approach_point(ct)
        if self.approach is None:
            return
        if pos.distance_squared(self.approach) <= 2 or self.stuck >= 6:
            # Arrived with nothing in sight: orbit the approach point itself so
            # the sweep keeps covering fresh tiles rather than parking.
            self.killzone = self.approach
            self.loiter_since = rnd
            self.stuck = 0
            return
        self._step_toward(ct, self.approach)

    def _approach_point(self, ct: Controller) -> Position | None:
        """A tile beside the enemy Core, offset off the axis, standoff kept."""
        if self.home is None or self.enemy is None:
            return None
        dx = self.enemy.x - self.home.x
        dy = self.enemy.y - self.home.y
        # Perpendicular to the approach axis, sign chosen deterministically.
        if abs(dx) >= abs(dy):
            off = Position(self.enemy.x, self.enemy.y + APPROACH_OFFSET)
            alt = Position(self.enemy.x, self.enemy.y - APPROACH_OFFSET)
        else:
            off = Position(self.enemy.x + APPROACH_OFFSET, self.enemy.y)
            alt = Position(self.enemy.x - APPROACH_OFFSET, self.enemy.y)
        w, h = ct.get_map_width(), ct.get_map_height()
        for cand in (off, alt):
            if 0 <= cand.x < w and 0 <= cand.y < h:
                if cand.distance_squared(nearest_core_tile(cand, self.enemy)) >= CORE_STANDOFF_SQ:
                    return cand
        return Position(
            min(max(self.enemy.x, 0), w - 1),
            min(max(self.enemy.y + APPROACH_OFFSET, 0), h - 1),
        )

    def _loiter(self, ct: Controller, rnd: int, pos: Position, centre: Position) -> None:
        """A small fixed loop around the kill zone, so rebuilds are re-killed.

        Deterministic: four waypoints in a fixed order, advanced on arrival or
        after a dwell timeout. Never retreats, never goes home.
        """
        waypoints = (
            Position(centre.x + LOITER_RADIUS, centre.y),
            Position(centre.x, centre.y + LOITER_RADIUS),
            Position(centre.x - LOITER_RADIUS, centre.y),
            Position(centre.x, centre.y - LOITER_RADIUS),
        )
        w, h = ct.get_map_width(), ct.get_map_height()
        for _ in range(len(waypoints)):
            wp = waypoints[self.loiter_idx % len(waypoints)]
            reached = pos.distance_squared(wp) <= 1
            stale = rnd - self.loiter_since > LOITER_DWELL
            off_map = not (0 <= wp.x < w and 0 <= wp.y < h)
            if reached or stale or off_map:
                self.loiter_idx = (self.loiter_idx + 1) % len(waypoints)
                self.loiter_since = rnd
                continue
            self._step_toward(ct, wp)
            return

    # ------------------------------------------------------------------
    # The finishing push -- two Sentinels, two angles
    # ------------------------------------------------------------------

    def _push_turn(self, ct: Controller, rnd: int, pos: Position) -> None:
        """Walk deep and plant a Sentinel that can actually hit the Core.

        Both Sentinel and Gunner fire a single-tile-wide line, so proximity is
        worthless without alignment: the site is chosen by asking
        can_fire_from() for the hypothetical turret against each of the four
        Core footprint tiles, and the nearest legal (site, facing) pair wins.
        """
        if self.enemy is None:
            return
        if ct.read_store(SLOT_SENTINELS) >= SENTINEL_TARGET:
            self.stage = "idle" if self.role < SABOTEUR_ROLE else self.stage
            return

        if self.reposition_target is not None:
            if (
                pos == self.reposition_target
                or self.stuck >= 3
                or rnd - self.reposition_start > REPOSITION_MAX_RNDS
            ):
                self.reposition_target = None
            else:
                self._step_toward(ct, self.reposition_target)
                return

        if ct.get_action_cooldown() == 0:
            if ct.get_global_resources() >= ct.get_sentinel_cost():
                if self._plant_sentinel(ct, pos):
                    planted = ct.read_store(SLOT_SENTINELS) + 1
                    ct.write_store(SLOT_SENTINELS, planted)
                    self.built_sentinels += 1
                    if planted < SENTINEL_TARGET:
                        self._set_lateral_target(ct, rnd, pos)
                    return
        self._step_toward(ct, nearest_core_tile(pos, self.enemy))

    def _plant_sentinel(self, ct: Controller, pos: Position) -> bool:
        if self.enemy is None:
            return False
        targets = core_footprint(self.enemy)
        best = None
        for d in CARDINALS:
            site = pos.add(d)
            if not in_bounds(ct, site):
                continue
            for tile in targets:
                dist = site.distance_squared(tile)
                if dist > SENTINEL_RANGE_SQ:
                    continue
                facing = site.direction_to(tile)
                if facing == Direction.CENTRE:
                    continue
                try:
                    if not ct.can_fire_from(site, facing, EntityType.SENTINEL, tile):
                        continue
                    if not ct.can_build_sentinel(site, facing):
                        continue
                except GameError:
                    continue
                key = (dist, site.x, site.y)
                if best is None or key < best[0]:
                    best = (key, site, facing)
        if best is None:
            return False
        try:
            ct.build_sentinel(best[1], best[2])
        except GameError:
            return False
        return True

    def _set_lateral_target(self, ct: Controller, rnd: int, pos: Position) -> None:
        """Shift off the approach axis so Sentinel #2 arrives on a second angle."""
        if self.enemy is None:
            return
        tile = nearest_core_tile(pos, self.enemy)
        dx = tile.x - pos.x
        dy = tile.y - pos.y
        cands = []
        for off in (LATERAL_OFFSET, LATERAL_OFFSET - 1):
            if abs(dx) >= abs(dy):
                cands.append(Position(pos.x, pos.y + off))
                cands.append(Position(pos.x, pos.y - off))
            else:
                cands.append(Position(pos.x + off, pos.y))
                cands.append(Position(pos.x - off, pos.y))
        for c in cands:
            if not in_bounds(ct, c):
                continue
            if c.distance_squared(nearest_core_tile(c, self.enemy)) > SENTINEL_RANGE_SQ:
                continue
            self.reposition_target = c
            self.reposition_start = rnd
            return

    # ------------------------------------------------------------------
    # Turrets
    # ------------------------------------------------------------------

    def _scan_line(self, ct: Controller, pos: Position):
        """(nearest enemy Core tile, nearest enemy anything) on this turret's ray.

        get_attackable_tiles() enumerates row-major in absolute map coordinates,
        so a "first occupied tile wins" scan engages the farthest enemy for
        N/NE/NW/W facings and the nearest for the other four. Targets are picked
        by distance_squared instead, never by enumeration order.
        """
        my_team = ct.get_team()
        best_core = None
        best_any = None
        try:
            tiles = ct.get_attackable_tiles()
        except GameError:
            return None, None
        for tile in tiles:
            if not in_bounds(ct, tile):
                continue
            try:
                tid = ct.get_tile_building_id(tile)
                if tid is None:
                    tid = ct.get_tile_builder_bot_id(tile)
                if tid is None:
                    continue
                if ct.get_team(tid) == my_team:
                    continue
                is_core = ct.get_entity_type(tid) == EntityType.CORE
            except GameError:
                continue
            key = (pos.distance_squared(tile), tile.x, tile.y)
            if is_core and (best_core is None or key < best_core[0]):
                best_core = (key, tile)
            if best_any is None or key < best_any[0]:
                best_any = (key, tile)
        return best_core, best_any

    def _run_gunner(self, ct: Controller) -> None:
        """Screen the lane: fire down the ray, and ROTATE to reacquire.

        "Rotate to reacquire rather than relocate" -- a Gunner is 20 Ti of
        permanent lane presence, and a rotation is 10 Ti; walking a builder out
        to rebuild one somewhere else costs both far more and the tempo.
        """
        pos = ct.get_position()
        self._locate(ct)
        self._report_enemy_economy(ct)

        best_core, best_any = self._scan_line(ct, pos)
        choice = best_core or best_any
        if choice is not None:
            try:
                if ct.can_fire(choice[1]):
                    ct.fire(choice[1])
                    return
            except GameError:
                return
            return

        # Nothing on the line: turn toward whatever is in vision instead.
        if ct.get_action_cooldown() != 0:
            return
        if ct.get_global_resources() < ROTATE_COST:
            return
        my_team = ct.get_team()
        best = None
        try:
            nearby = ct.get_nearby_entities(dist_sq=GUNNER_RANGE_SQ)
        except GameError:
            return
        for eid in nearby:
            try:
                if ct.get_team(eid) == my_team:
                    continue
                where = ct.get_position(eid)
            except GameError:
                continue
            key = (pos.distance_squared(where), where.x, where.y)
            if best is None or key < best[0]:
                best = (key, where)
        if best is None:
            return
        facing = pos.direction_to(best[1])
        if facing == Direction.CENTRE:
            return
        try:
            if ct.get_direction() == facing:
                return
            if ct.can_rotate(facing):
                ct.rotate(facing)
        except GameError:
            return

    def _run_sentinel(self, ct: Controller) -> None:
        """Enemy Core first, always. Fire staggered on alternate rounds.

        Sentinel reload is 2, so two Sentinels firing on the same parity leave
        the Core a free round every other round; on opposite parities the Core
        takes 18 damage every round instead. Each claims a parity on its first
        turn from a store counter.
        """
        pos = ct.get_position()
        self._locate(ct)
        self._report_enemy_economy(ct)

        if self.stagger is None:
            nxt = ct.read_store(SLOT_TURRET_NEXT)
            self.stagger = nxt if nxt > 0 else 1
            ct.write_store(SLOT_TURRET_NEXT, self.stagger + 1)
            self.stagger -= 1

        best_core, best_any = self._scan_line(ct, pos)
        choice = best_core or best_any
        if choice is None:
            return
        if best_core is not None:
            # Only the Core shot is worth staggering; anything else is
            # opportunistic and should be taken the moment it is offered.
            if (ct.get_current_round() + self.stagger) % 2 != 0:
                return
        try:
            if ct.can_fire(choice[1]):
                ct.fire(choice[1])
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

        for d in prefs:
            try:
                if ct.can_move(d):
                    ct.move(d)
                    return True
            except GameError:
                continue
        return False
