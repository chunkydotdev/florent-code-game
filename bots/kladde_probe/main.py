"""kladde_probe -- kladde-style slow grind. INSTRUMENT, not a ladder bot.

Provenance: replay-extracted from the 1718-rated team "kladde chatte tville (och
oss)", platform match 36f5e137 games 1 and 5, which beat our live v51 by grinding
it down over r381 and r284 rather than by any opening (extracted 2026-08-07).

The shape of those games is patience. Nothing about them is a timing: the economy
is never finished -- harvesters keep going up past r300, builders keep being
spawned as titanium allows, and there is no fixed target for either. Almost the
whole army stands at HOME, 1-4 tiles off their own Core, accumulating through the
entire midgame as sentinels and gunners the economy can pay for. The aggression
that exists is opportunistic: whenever two or more builders are spare, they walk
into the enemy's economic footprint TOGETHER and chew on whatever is adjacent,
harvesters first -- and if that raid dies without landing, nothing is lost,
because it was never the win condition. The win condition is the last 40-50
rounds: with a standing army and a bank of ammunition, one builder walks over and
plants two or three turrets essentially in the enemy Core's face, and both source
games went from no presence at all to a dead Core inside 50 rounds.

This file exists so pressure-over-time can be gated repeatably -- the third
instrument next to band_probe (all-in rush) and flotte_probe (economic
strangulation). Being slow is the point; a win at r200-700 is on-spec and a long
game is not a failure. What it must NOT be is fragile in code terms -- an
uncaught exception permanently deletes the unit for the rest of the match, so
every unit's turn body is wrapped and every mutating call is gated by its
can_*() predicate. (No try/finally anywhere: the platform's bot-code validator
rejects it.)

Deterministic: no random anywhere. Ties break on (distance, x, y).

Phases. These are DESCRIPTIONS, not schedules -- every transition below triggers
on state, never on a round number, with the two exceptions called out in
DEVIATIONS at the bottom of this docstring:

  r0-r2     Core spawns 3 builders, one per round; each plants a harvester on
            the nearest free ore and lays the shortest conveyor run home
  ~r10+     the first free builder plants ONE home turret as insurance
  ...       from here nothing is scheduled. Every free builder each round asks,
            in order: is the late strike on? is another harvester affordable and
            has the pacing interval elapsed? is another home turret affordable?
            are there spare bodies for a raid? -- and otherwise stands at home
            repairing what is damaged
  ...       the Core keeps spawning builders whenever titanium is comfortably
            over the (rising) builder price, so the body count grows with the
            economy rather than to a target
  ...       raiders leave in claimed pairs, walk the enemy's conveyor spine, and
            never come home. When a wave dies the claim goes stale and the next
            pair leaves
  LATE      once the home army reaches 5 turrets, or no enemy harvester has been
            seen for 20 rounds after we have actually been over there to look:
            a striker walks in and plants 3 turrets (sentinel-led) aligned on
            the enemy Core, firing staggered so a hit lands nearly every round

Ammunition is banked in small conversions from r0 out of whatever titanium the
economy and the army are not owed, so that by the time the strike triggers there
are 100+ points sitting there -- a sentinel that has to wait for its first 10
ammo has handed the defender a free repair window. The home turrets draw on the
same pool all midgame; that is intended.

Communication store slots. The store cannot represent a zero: a slot holding 0 is
indistinguishable from a slot nobody has written (docs/game-model.md, measured).
Positions are packed with a +1 offset and round numbers stored as round+1; only
genuine counters (which legitimately start at zero) are stored raw.

  0  SLOT_HOME           packed position of our own Core
  1  SLOT_ENEMY          packed position of the enemy Core, once directly sighted
  2  SLOT_ROLE_NEXT      next builder role index, +1
  3  SLOT_HARVESTERS     harvesters built (uncapped in spirit; soft ceiling only)
  4  SLOT_LAST_HARV      round+1 a builder last CLAIMED the economy slot; this
                         doubles as the pacing interval and as a one-at-a-time
                         mutex on expansion
  5  SLOT_HOME_TURRETS   turrets standing near our own Core
  6  SLOT_RAID_CLAIM     raiders currently committed (reset by the Core when the
                         wave stops pinging)
  7  SLOT_RAID_PING      round+1 a raider last confirmed it is alive
  8  SLOT_HARV_SEEN      round+1 any of our units last saw an enemy harvester
  9  SLOT_SCOUTED        1 once any of our units has reached enemy territory
 10  SLOT_STRIKE         1 once the late strike has been triggered (latched)
 11  SLOT_STRIKE_CLAIM   builders committed to the strike
 12  SLOT_STRIKE_TURRETS turrets planted at the enemy Core
 13  SLOT_TURRET_NEXT    next strike-sentinel stagger index, +1
 14  SLOT_KILLZONE       packed position of a raider's last kill

DEVIATIONS from the literal recipe (also reported to the caller):
  1. Soft ceilings where the recipe says "uncapped": MAX_HARVESTERS,
     HOME_TURRET_MAX, MAX_BUILDERS_TOTAL. All are set well above what a 1000
     round game reaches, so they are runaway guards, not targets.
  2. STRIKE_FALLBACK_ROUND: a third, round-based strike trigger as a safety net
     for maps where neither state trigger ever fires.
  3. Raiders leave within one CLAIM_PERIOD of each other rather than on the
     same round. Simultaneous claiming is what the recipe describes, but with
     buffered store writes it means every idle builder leaves at once; the
     token keeps the pair concurrent in the field without emptying home.
  4. Ammunition conversion scales with genuinely spare titanium instead of
     staying a fixed small chunk. A literal trickle is out-burned by a standing
     army, which starved the strike (see _bank_ammo).
"""

import sys

from fcode import Controller, Direction, EntityType, Environment, GameError, GameConstants, Position

# --- store slots -----------------------------------------------------------
SLOT_HOME = 0
SLOT_ENEMY = 1
SLOT_ROLE_NEXT = 2
SLOT_HARVESTERS = 3
SLOT_LAST_HARV = 4
SLOT_HOME_TURRETS = 5
SLOT_RAID_CLAIM = 6
SLOT_RAID_PING = 7
SLOT_HARV_SEEN = 8
SLOT_SCOUTED = 9
SLOT_STRIKE = 10
SLOT_STRIKE_CLAIM = 11
SLOT_STRIKE_TURRETS = 12
SLOT_TURRET_NEXT = 13
SLOT_KILLZONE = 14

# --- economy ---------------------------------------------------------------
# The opening three go up as fast as builders exist, with no pacing gate: that
# is what pays for everything else. After that the economy is uncapped but
# PACED -- roughly one new harvester per HARV_INTERVAL rounds, for as long as
# reachable ore and spare titanium last, which in the source replays meant an
# economy still growing past r300.
ECO_OPENING = 3
HARV_INTERVAL = 15
# Runaway guard only (see DEVIATIONS). No map in the pool has this much ore
# within a sane conveyor run.
MAX_HARVESTERS = 16
# A run longer than this means the ore was the wrong ore -- an unfinished or
# absurd chain is pure cost, since crediting is delivery-only.
MAX_CHAIN = 18
# Titanium kept clear of the harvester+chain price before expansion is allowed,
# so growing the economy never starves the army or the ammo bank.
ECO_FLOAT = 40
# A builder that cannot reach its ore in this many rounds gives the slot back.
ECO_TIMEOUT = 60

# --- builders --------------------------------------------------------------
OPENING_BUILDERS = 3
# "Spawn builders throughout the game as titanium allows (7-10+ cumulative)."
# Not a target: the Core spawns whenever titanium is comfortably clear of the
# (rising, +20% each) builder price, so the body count tracks the economy.
SPAWN_INTERVAL = 8
SPAWN_FLOAT = 70
MAX_BUILDERS_TOTAL = 16      # runaway guard (see DEVIATIONS)
UNIT_CAP_MARGIN = 4          # leave room under MAX_TEAM_UNITS for strike turrets
# Claim token. Store writes land a round late, so a counter slot that every
# free builder reads and increments on the same round is clobbered: measured
# 2026-08-07 on meander, ten idle builders all read "0 turrets built", all
# built one, and all wrote 1 -- 29 turrets went up against a ceiling of 8, and
# the +20% scale on each one taxed the whole game. A builder may therefore only
# make a claim on rounds where rnd % CLAIM_PERIOD == role % CLAIM_PERIOD, which
# serialises claims to at most one per round. The period equals
# MAX_BUILDERS_TOTAL so every live role owns a distinct slot.
CLAIM_PERIOD = MAX_BUILDERS_TOTAL

# --- home army -------------------------------------------------------------
# "Almost everything stays HOME -- sentinels/gunners within ~1-4 tiles of your
# OWN core as titanium allows through the whole midgame."
HOME_TURRET_MAX = 8          # runaway guard (see DEVIATIONS)
HOME_TURRET_FLOAT = 45       # titanium left clear of the turret price
# Distance-squared band from the nearest own-Core tile. The lower bound keeps
# the 12-tile spawn ring clear: a Core walled in by its own turrets can never
# spawn another builder, which would end the economy permanently.
HOME_MIN_SQ = 4
HOME_MAX_SQ = 20
# "One early home turret as insurance (~first 15% of the game)": a Gunner, the
# cheap one, and then Sentinels with a Gunner every third slot.
EARLY_TURRET_ROUND = 150
GUARD_RING = 3               # tiles out from the Core, on the enemy side
GUARD_TIMEOUT = 25

# --- raiding ---------------------------------------------------------------
# "Opportunistic multi-raider -- whenever 2+ builder bots are available beyond
# economy needs, commit them TOGETHER." Raiders never come home. A wave that
# dies without landing anything costs the plan nothing.
RAID_CONCURRENT = 2
RAID_MIN_BUILDERS = 4        # never raid with the bodies the economy still needs
RAID_STALE_ROUNDS = 5
RAID_RESET_COOLDOWN = 10
ATTACK_COST = 2
APPROACH_OFFSET = 4          # aim beside their Core, where the harvesters are
CORE_STANDOFF_SQ = 9
LOITER_RADIUS = 2
LOITER_DWELL = 3

# --- the late strike -------------------------------------------------------
STRIKE_ARMY_TRIGGER = 5      # "own army >= 5 turrets"
STRIKE_QUIET_ROUNDS = 20     # "...OR enemy harvester count stalled at ~0"
STRIKE_FALLBACK_ROUND = 450  # safety net (see DEVIATIONS)
STRIKE_TURRETS = 3
STRIKERS = 2
SENTINEL_RANGE_SQ = 32
GUNNER_RANGE_SQ = 13
LATERAL_OFFSET = 3
REPOSITION_MAX_RNDS = 12

# --- ammunition ------------------------------------------------------------
# Modest and continuous from r0. AMMO_SPARE_MIN is what makes it modest: the
# Core only converts titanium it has beyond everything currently owed plus a
# working float, so banking never out-competes the army it exists to feed.
AMMO_CHUNK = 5
AMMO_CEILING = 220
AMMO_SPARE_MIN = 80
ROTATE_COST = 10

# --- travel -----------------------------------------------------------------
# Greedy stepping walks into local minima on walled maps and then oscillates
# between two tiles forever: measured 2026-08-07 on hive, one striker spent
# r150-r1000 rocking around (11,18) with a clear route four tiles to its side,
# and a raider sat against the same wall for 355 rounds. When the distance to
# the goal stops improving for NO_PROGRESS_LIMIT rounds the unit commits to a
# sideways waypoint for DETOUR_ROUNDS -- long enough to clear a wall end, short
# enough that it costs nothing when the block was transient.
NO_PROGRESS_LIMIT = 8
DETOUR_ROUNDS = 10
DETOUR_DIST = 4

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
        self.last_spawn_round = -99
        self.raid_reset_round = -99

        # Builder state
        self.role: int | None = None
        self.stage = "eco"
        self.prev_pos: Position | None = None
        self.stuck = 0
        self.known_ore: set = set()
        self.ore_target: Position | None = None
        self.harvester_pos: Position | None = None
        self.trail_prev: Position | None = None
        self.chain_tiles: set = set()
        self.chain_len = 0
        self.cap_tile: Position | None = None
        self.stage_start = 0

        # Home-army state
        self.guard_post: Position | None = None
        self.guard_slot = 0

        # Raider state
        self.approach: Position | None = None
        self.target_id: int | None = None
        self.killzone: Position | None = None
        self.loiter_idx = 0
        self.loiter_since = 0

        # Strike state
        self.reposition_target: Position | None = None
        self.reposition_start = 0

        # Turret state
        self.stagger: int | None = None
        self.forward: bool | None = None

        # Travel watchdog
        self.travel_goal: Position | None = None
        self.best_dist = 0
        self.no_progress = 0
        self.detour: Position | None = None
        self.detour_left = 0
        self.detour_flip = 1

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

        Every unit does this, not just the raiders: one arm of the strike
        trigger is "no enemy harvester seen by ANY of our units", so a home
        turret that can still see one has to be able to veto it.
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

    def _strike_active(self, ct: Controller) -> bool:
        """Latched state trigger for the late decisive strike.

        Two state arms from the recipe, plus a round fallback (see DEVIATIONS):
          - the home army has reached 5 turrets, or
          - nobody has seen an enemy harvester for 20 rounds, and we have
            actually been over there to look (otherwise "no sighting" just
            means "no scout").
        """
        if ct.read_store(SLOT_STRIKE) == 1:
            return True
        if ct.read_store(SLOT_HOME_TURRETS) >= STRIKE_ARMY_TRIGGER:
            return True
        rnd = ct.get_current_round()
        if ct.read_store(SLOT_SCOUTED) == 1:
            seen = ct.read_store(SLOT_HARV_SEEN)
            if seen > 0:
                if rnd - (seen - 1) >= STRIKE_QUIET_ROUNDS:
                    return True
            elif rnd >= STRIKE_QUIET_ROUNDS:
                return True
        return rnd >= STRIKE_FALLBACK_ROUND

    # ------------------------------------------------------------------
    # Core
    # ------------------------------------------------------------------

    def _run_core(self, ct: Controller) -> None:
        """Builders throughout the game, and a steady trickle into ammunition.

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
        if ct.read_store(SLOT_STRIKE) != 1 and self._strike_active(ct):
            ct.write_store(SLOT_STRIKE, 1)

        self._recycle_raid_claim(ct, rnd)
        self._bank_ammo(ct)

        if ct.get_action_cooldown() != 0:
            return
        if not self._should_spawn(ct, rnd):
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
            self.last_spawn_round = rnd

    def _should_spawn(self, ct: Controller, rnd: int) -> bool:
        """The opening three back to back, then whenever titanium allows.

        There is no builder target. The gate is a margin over the CURRENT
        builder price, which rises 20% per body, so the fleet grows exactly as
        fast as the economy can carry it and stops on its own when it cannot.
        """
        if self.spawned >= MAX_BUILDERS_TOTAL:
            return False
        try:
            if ct.get_unit_count() >= GameConstants.MAX_TEAM_UNITS - UNIT_CAP_MARGIN:
                return False
        except GameError:
            return False
        cost = ct.get_builder_bot_cost()
        if self.spawned < OPENING_BUILDERS:
            return ct.get_global_resources() >= cost
        if rnd - self.last_spawn_round < SPAWN_INTERVAL:
            return False
        return ct.get_global_resources() >= cost + SPAWN_FLOAT

    def _recycle_raid_claim(self, ct: Controller, rnd: int) -> None:
        """Free the raid slots once a wave has stopped reporting.

        Raiders never come home, so the claim can only be released by their
        silence. The cooldown covers the buffered-write gap: a freshly committed
        raider needs one round before its first ping is readable, and resetting
        inside that window would commit the whole fleet one pair at a time.
        """
        claimed = ct.read_store(SLOT_RAID_CLAIM)
        if claimed <= 0:
            return
        if rnd - self.raid_reset_round < RAID_RESET_COOLDOWN:
            return
        ping = ct.read_store(SLOT_RAID_PING)
        if ping > 0 and rnd - (ping - 1) <= RAID_STALE_ROUNDS:
            return
        if ping == 0 and rnd < RAID_STALE_ROUNDS + 2:
            return
        ct.write_store(SLOT_RAID_CLAIM, 0)
        self.raid_reset_round = rnd

    def _bank_ammo(self, ct: Controller) -> None:
        """Small, continuous conversions out of genuinely spare titanium.

        The reserve is everything currently owed -- the harvester and chain the
        economy is about to buy, the next home turret, the strike turrets, a
        builder -- plus AMMO_SPARE_MIN of working float. Only what is left over
        becomes ammunition, so the bank fills during the rich stretches and
        pauses on its own whenever the army or the economy wants the titanium.
        """
        ammo = ct.get_global_ammo()
        if ammo >= AMMO_CEILING:
            return

        reserve = ct.get_harvester_cost() + 6 * ct.get_conveyor_cost()
        turrets = ct.read_store(SLOT_HOME_TURRETS)
        if turrets < HOME_TURRET_MAX:
            reserve += ct.get_sentinel_cost()
        strike_built = ct.read_store(SLOT_STRIKE_TURRETS)
        if ct.read_store(SLOT_STRIKE) == 1 and strike_built < STRIKE_TURRETS:
            reserve += (STRIKE_TURRETS - strike_built) * ct.get_sentinel_cost()
        if self.spawned < MAX_BUILDERS_TOTAL:
            reserve += ct.get_builder_bot_cost()
        reserve += AMMO_SPARE_MIN

        spare = ct.get_global_resources() - reserve
        # Modest by default, but a fixed 5/round is not "banking" once a real
        # army exists: measured 2026-08-07 on meander, a standing army burned
        # ammunition faster than the trickle replaced it and finished the match
        # on 3 points with 2439 titanium sitting unspent, which turned a siege
        # into a 950-round grind. So the conversion scales with genuinely spare
        # titanium -- the AMMO_CEILING is what keeps it from becoming a dump.
        amount = min(max(AMMO_CHUNK, spare // 8), AMMO_CEILING - ammo, spare)
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
            self.stage_start = rnd
            # The opening three go straight onto ore; every later body starts
            # free and asks the standing question like everyone else.
            self.stage = "eco" if self.role < ECO_OPENING else "free"

        if self.prev_pos is not None:
            if pos == self.prev_pos:
                self.stuck += 1
            else:
                self.stuck = 0
        self.prev_pos = pos

        self._report_enemy_economy(ct)
        if self.enemy is not None and ct.read_store(SLOT_SCOUTED) != 1:
            if pos.distance_squared(self.enemy) <= 64:
                ct.write_store(SLOT_SCOUTED, 1)

        if self._cpu_exhausted(ct):
            return

        # A raider or striker already committed stays committed -- both are
        # one-way trips. Everyone else re-decides from "free" every round.
        if self.stage == "raid":
            self._raid_turn(ct, rnd, pos)
            return
        if self.stage == "strike":
            self._strike_turn(ct, rnd, pos)
            return

        if self.stage == "eco":
            self._eco_seek_ore(ct, rnd, pos)
        elif self.stage == "lay":
            self._eco_lay(ct, pos)
        elif self.stage == "cap":
            self._eco_cap(ct, pos)
        elif self.stage == "guard":
            self._guard_turn(ct, rnd, pos)
        else:
            self._free_turn(ct, rnd, pos)

    def _enter(self, stage: str, rnd: int) -> None:
        self.stage = stage
        self.stage_start = rnd
        self.stuck = 0

    def _my_claim_round(self, rnd: int) -> bool:
        """Whether this builder owns the claim token this round (see
        CLAIM_PERIOD). Serialising claims is what keeps the counter slots
        honest against the one-round write lag.
        """
        if self.role is None:
            return False
        return rnd % CLAIM_PERIOD == self.role % CLAIM_PERIOD

    # -- the decision every free builder makes, every round -------------

    def _free_turn(self, ct: Controller, rnd: int, pos: Position) -> None:
        """No schedule: a standing builder asks the same four questions each
        round and takes the first one that is affordable and allowed.

        Order is the recipe's own priority. The strike ends the game, so it
        outranks everything. Economy comes before army because economy is what
        pays for the army; it is self-limiting via the pacing interval, so it
        cannot monopolise the fleet. Raiding is last precisely because it is
        opportunistic -- it happens with the bodies nothing else wanted.
        """
        if self._claim_strike(ct, rnd):
            return
        if self._claim_economy(ct, rnd):
            return
        if self._claim_home_turret(ct, rnd):
            return
        if self._claim_raid(ct, rnd):
            return
        self._idle_turn(ct, pos)

    def _claim_strike(self, ct: Controller, rnd: int) -> bool:
        if ct.read_store(SLOT_STRIKE) != 1 and not self._strike_active(ct):
            return False
        if ct.read_store(SLOT_STRIKE_TURRETS) >= STRIKE_TURRETS:
            return False
        if not self._my_claim_round(rnd):
            return False
        claimed = ct.read_store(SLOT_STRIKE_CLAIM)
        if claimed >= STRIKERS:
            return False
        ct.write_store(SLOT_STRIKE_CLAIM, claimed + 1)
        self._enter("strike", rnd)
        return True

    def _claim_economy(self, ct: Controller, rnd: int) -> bool:
        """Take the expansion slot if the pacing interval has elapsed.

        Writing SLOT_LAST_HARV on the CLAIM (not on the build) is what makes
        this both the pacing interval and a mutex: a second builder reading the
        slot next round sees the interval reset and stands down, so expansion
        stays one-at-a-time instead of five builders stampeding the same ore.
        """
        built = ct.read_store(SLOT_HARVESTERS)
        if built >= MAX_HARVESTERS:
            return False
        if built >= ECO_OPENING:
            # The opening three race; every later one waits for its token, so
            # the harvester counter and the pacing interval stay honest.
            if not self._my_claim_round(rnd):
                return False
            last = ct.read_store(SLOT_LAST_HARV)
            if last > 0 and rnd - (last - 1) < HARV_INTERVAL:
                return False
            need = ct.get_harvester_cost() + 6 * ct.get_conveyor_cost() + ECO_FLOAT
            if ct.get_global_resources() < need:
                return False
            ct.write_store(SLOT_LAST_HARV, rnd + 1)
        self._enter("eco", rnd)
        return True

    def _claim_home_turret(self, ct: Controller, rnd: int) -> bool:
        """Army-at-home: as many as titanium allows, all midgame long."""
        built = ct.read_store(SLOT_HOME_TURRETS)
        if built >= HOME_TURRET_MAX:
            return False
        if not self._my_claim_round(rnd):
            return False
        cost = self._home_turret_cost(ct, built)
        # The first one is insurance, not army: it goes up as soon as it can be
        # paid for at all, inside the opening ~15% of the match. Everything
        # after it waits for titanium the economy genuinely does not want.
        float_ti = 0 if (built == 0 and rnd < EARLY_TURRET_ROUND) else HOME_TURRET_FLOAT
        if ct.get_global_resources() < cost + float_ti:
            return False
        self.guard_slot = built
        self.guard_post = None
        self._enter("guard", rnd)
        return True

    def _claim_raid(self, ct: Controller, rnd: int) -> bool:
        """Commit in pairs, and only with bodies the plan does not need.

        The claim token means the pair does not leave on the same round, but it
        does leave within one token period -- and since crossing the map takes
        20-40 rounds, both are in the enemy's footprint at the same time, which
        is what "concurrent raiders, not one lone wolf" actually asks for.
        """
        if ct.read_store(SLOT_ROLE_NEXT) - 1 < RAID_MIN_BUILDERS:
            return False
        if not self._my_claim_round(rnd):
            return False
        claimed = ct.read_store(SLOT_RAID_CLAIM)
        if claimed >= RAID_CONCURRENT:
            return False
        ct.write_store(SLOT_RAID_CLAIM, claimed + 1)
        self._enter("raid", rnd)
        return True

    # -- economy --------------------------------------------------------

    def _scan_ore(self, ct: Controller) -> None:
        """Remember ore tiles seen. Vision is r^2=20, so this is ~60 tiles."""
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

    def _eco_seek_ore(self, ct: Controller, rnd: int, pos: Position) -> None:
        """Walk to the nearest free ore and plant a harvester on it."""
        self._scan_ore(ct)
        if rnd - self.stage_start > ECO_TIMEOUT:
            self._enter("free", rnd)
            return
        if ct.read_store(SLOT_HARVESTERS) >= MAX_HARVESTERS:
            self._enter("free", rnd)
            return

        anchor = self.home if self.home is not None else pos
        cands = sorted(
            (Position(x, y) for (x, y) in self.known_ore),
            key=lambda t: (t.distance_squared(anchor), t.x, t.y),
        )
        free = []
        for tile in cands:
            try:
                if ct.get_tile_building_id(tile) is not None:
                    self.known_ore.discard((tile.x, tile.y))
                    continue
            except GameError:
                pass  # out of vision: assume still free, re-checked on arrival
            free.append(tile)
        if not free:
            self._step_toward(ct, self._explore_target(ct, pos))
            return

        # Builders prefer different ore by role so two of them do not walk to
        # the same tile in the rare rounds when expansion runs in parallel.
        self.ore_target = free[min(self.role % 3, len(free) - 1)]

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
                ct.write_store(SLOT_LAST_HARV, rnd + 1)
                self.harvester_pos = tile
                self.known_ore.discard((tile.x, tile.y))
                self._begin_chain(ct, rnd)
                return
        self._step_toward(ct, self.ore_target)

    def _begin_chain(self, ct: Controller, rnd: int) -> None:
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
                self._enter("free", rnd)
                return
        self._enter("lay", rnd)

    def _eco_lay(self, ct: Controller, pos: Position) -> None:
        """Lay the run back to the Core, one tile per two rounds.

        A builder cannot build on its own tile, so the chain is laid behind it:
        step toward the Core, then conveyor the tile just vacated, facing the
        tile now occupied. Conveyors are bot-passable, so nothing it lays can
        ever box it in.
        """
        rnd = ct.get_current_round()
        if self.home is None or self.chain_len > MAX_CHAIN:
            self._enter("free", rnd)
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
            self._enter("cap", rnd)
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
            self._enter("free", rnd)

    def _eco_cap(self, ct: Controller, pos: Position) -> None:
        """Build the final conveyor, the one that actually faces the Core.

        An unfinished chain delivers exactly nothing (measured), so this step is
        not cosmetic -- it is the whole economy.
        """
        rnd = ct.get_current_round()
        if self.home is None or self.cap_tile is None or self.stuck >= 6:
            self._enter("free", rnd)
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
            self._enter("free", rnd)
            return
        if self._build_link(ct, self.cap_tile, core_tile) or self.stuck >= 4:
            self._enter("free", rnd)

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
        prefs = []
        if self.home is not None:
            # Step away from the Core -- back down the chain we just laid, which
            # is conveyor and therefore passable.
            core_tile = nearest_core_tile(pos, self.home)
            if core_tile.x < pos.x:
                prefs.append(Direction.EAST)
            elif core_tile.x > pos.x:
                prefs.append(Direction.WEST)
            if core_tile.y < pos.y:
                prefs.append(Direction.SOUTH)
            elif core_tile.y > pos.y:
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

    def _explore_target(self, ct: Controller, pos: Position) -> Position:
        """No ore known yet: walk down the lane, where the ore usually is."""
        spot = self._lane_point(ct, 0.3)
        return spot if spot is not None else Position(pos.x + 1, pos.y)

    def _lane_point(self, ct: Controller, fraction: float) -> Position | None:
        """A point `fraction` of the way along the own-Core -> enemy-Core line."""
        if self.home is None or self.enemy is None:
            return None
        hx = self.home.x + 0.5
        hy = self.home.y + 0.5
        px = int(round(hx + (self.enemy.x + 0.5 - hx) * fraction))
        py = int(round(hy + (self.enemy.y + 0.5 - hy) * fraction))
        w, h = ct.get_map_width(), ct.get_map_height()
        return Position(min(max(px, 0), w - 1), min(max(py, 0), h - 1))

    # -- the home army --------------------------------------------------

    def _home_turret_cost(self, ct: Controller, idx: int) -> int:
        return ct.get_gunner_cost() if self._home_turret_type(idx) == EntityType.GUNNER else ct.get_sentinel_cost()

    def _home_turret_type(self, idx: int) -> EntityType:
        """Gunner first -- the cheap insurance piece the recipe wants standing
        early -- then Sentinels, with a Gunner every third slot for close-in
        cover that the r^2=32 line turrets cannot provide.
        """
        return EntityType.GUNNER if idx % 3 == 0 else EntityType.SENTINEL

    def _guard_post_for(self, ct: Controller, idx: int) -> Position | None:
        """A standing spot GUARD_RING tiles out from our Core on the enemy side,
        fanned laterally by slot so the army spreads along the approach face
        instead of stacking on one tile.
        """
        if self.home is None or self.enemy is None:
            return None
        dx = self.enemy.x - self.home.x
        dy = self.enemy.y - self.home.y
        norm = max(abs(dx), abs(dy), 1)
        ux = dx / norm
        uy = dy / norm
        offsets = (0, 2, -2, 3, -3, 1, -1, 4, -4)
        off = offsets[idx % len(offsets)]
        px = self.home.x + int(round(ux * GUARD_RING)) + int(round(-uy * off))
        py = self.home.y + int(round(uy * GUARD_RING)) + int(round(ux * off))
        w, h = ct.get_map_width(), ct.get_map_height()
        return Position(min(max(px, 0), w - 1), min(max(py, 0), h - 1))

    def _guard_turn(self, ct: Controller, rnd: int, pos: Position) -> None:
        """Walk to the guard post and plant one turret beside our own Core."""
        built = ct.read_store(SLOT_HOME_TURRETS)
        if built >= HOME_TURRET_MAX or self.home is None:
            self._enter("free", rnd)
            return
        if self.guard_post is None:
            self.guard_post = self._guard_post_for(ct, self.guard_slot)
        if self.guard_post is None:
            self._enter("free", rnd)
            return
        if rnd - self.stage_start > GUARD_TIMEOUT:
            self._enter("free", rnd)
            return

        if ct.get_action_cooldown() == 0:
            etype = self._home_turret_type(self.guard_slot)
            if ct.get_global_resources() >= self._home_turret_cost(ct, self.guard_slot):
                if self._plant_home_turret(ct, pos, etype):
                    ct.write_store(SLOT_HOME_TURRETS, built + 1)
                    self._enter("free", rnd)
                    return
        if pos.distance_squared(self.guard_post) <= 2 and self.stuck >= 4:
            # Standing on the post with nowhere legal to build it: give the slot
            # back rather than block a body here forever.
            self._enter("free", rnd)
            return
        self._step_toward(ct, self.guard_post)

    def _plant_home_turret(self, ct: Controller, pos: Position, etype: EntityType) -> bool:
        """Turret on an adjacent tile inside the home band, facing the enemy.

        The HOME_MIN_SQ floor is load-bearing: turrets built on the Core's
        12-tile spawn ring would eventually wall the Core in, and a Core that
        cannot spawn has no economy and no army for the rest of the match.
        """
        if self.home is None or self.enemy is None:
            return False
        best = None
        for d in CARDINALS:
            site = pos.add(d)
            if not in_bounds(ct, site):
                continue
            home_d = site.distance_squared(nearest_core_tile(site, self.home))
            if home_d < HOME_MIN_SQ or home_d > HOME_MAX_SQ:
                continue
            facing = site.direction_to(nearest_core_tile(site, self.enemy))
            if facing == Direction.CENTRE:
                continue
            try:
                if not ct.can_build(etype, site, facing):
                    continue
            except GameError:
                continue
            key = (site.distance_squared(self.enemy), site.x, site.y)
            if best is None or key < best[0]:
                best = (key, site, facing)
        if best is None:
            return False
        try:
            ct.build(etype, best[1], best[2])
        except GameError:
            return False
        return True

    # -- standing by ----------------------------------------------------

    def _idle_turn(self, ct: Controller, pos: Position) -> None:
        """Nothing affordable this round: keep the standing structures alive.

        Healing is the cheapest lever in the game -- 1 Ti for +4 HP against
        ~0.56 Ti per point of incoming damage -- and it is the whole reason a
        patient bot survives long enough for its economy to matter.
        """
        if ct.get_action_cooldown() == 0 and self._try_heal(ct, pos):
            return
        hurt = self._damaged_friendly(ct, pos)
        if hurt is not None and pos.distance_squared(hurt) > 1:
            self._step_toward(ct, hurt)
            return
        # Otherwise come back to the home band and hold there -- close enough to
        # repair the army and the Core, far enough off the 12-tile spawn ring
        # that the Core can always place the next builder.
        if self.home is None:
            return
        band = pos.distance_squared(nearest_core_tile(pos, self.home))
        if HOME_MIN_SQ <= band <= HOME_MAX_SQ:
            return
        post = self._guard_post_for(ct, self.role if self.role is not None else 0)
        if post is not None:
            self._step_toward(ct, post)

    def _try_heal(self, ct: Controller, pos: Position) -> bool:
        if ct.get_global_resources() < 4:
            return False
        my_team = ct.get_team()
        best = None
        for d in CARDINALS:
            tile = pos.add(d)
            if not in_bounds(ct, tile):
                continue
            try:
                bid = ct.get_tile_building_id(tile)
                if bid is None or ct.get_team(bid) != my_team:
                    continue
                hp = ct.get_hp(bid)
                if hp >= ct.get_max_hp(bid):
                    continue
                if not ct.can_heal(tile):
                    continue
                is_core = ct.get_entity_type(bid) == EntityType.CORE
            except GameError:
                continue
            # The Core first, always: it is the only building whose loss is the
            # match, and can_heal() already refuses a Core at full HP.
            key = (0 if is_core else 1, hp, tile.x, tile.y)
            if best is None or key < best[0]:
                best = (key, tile)
        if best is None:
            return False
        try:
            ct.heal(best[1])
        except GameError:
            return False
        return True

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
                is_core = ct.get_entity_type(bid) == EntityType.CORE
            except GameError:
                continue
            key = (0 if is_core else 1, pos.distance_squared(where), where.x, where.y)
            if best is None or key < best[0]:
                best = (key, where)
        return best[1] if best is not None else None

    # ------------------------------------------------------------------
    # RAIDING -- opportunistic, concurrent, one-way
    # ------------------------------------------------------------------

    def _raid_turn(self, ct: Controller, rnd: int, pos: Position) -> None:
        """Cross into the enemy's economic footprint and chew on it.

        Order of business every round:
          1. the strike outranks the raid -- by then there is nothing left to
             raid and the turrets are what ends the match
          2. hit whatever enemy building is orthogonally adjacent, harvester
             first, then the conveyor spine, then anything
          3. otherwise walk at the nearest visible enemy economy
          4. otherwise cross toward their footprint, off the core-to-core axis
          5. once there is nothing left, loiter on the wreckage so rebuilds die
             as fast as they go up
        """
        ct.write_store(SLOT_RAID_PING, rnd + 1)
        sightings = self._report_enemy_economy(ct)

        # A raider already standing in enemy territory is the best-placed body
        # in the fleet to plant the siege, so it takes the striker slot if one
        # is free rather than making a fresh builder walk the whole map.
        if self._claim_strike(ct, rnd):
            self._strike_turn(ct, rnd, pos)
            return

        if self._cpu_exhausted(ct):
            return

        if ct.get_action_cooldown() == 0 and ct.get_global_resources() >= ATTACK_COST:
            if self._attack_adjacent(ct, pos):
                return

        goal = self._hunt_target(ct, pos, sightings)
        if goal is not None:
            self._step_toward(ct, goal)
            return
        self.target_id = None

        self._cross_or_loiter(ct, rnd, pos)

    def _attack_adjacent(self, ct: Controller, pos: Position) -> bool:
        """Builder melee: 2 Ti for 2 damage on an orthogonally adjacent tile.

        Priority: the target already wounded by us (never disengage -- that is
        the difference between chipping and killing), then HARVESTER, then the
        conveyor spine, then whatever else is in the way.
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
                rank = 0
            elif etype == EntityType.HARVESTER:
                rank = 1
            elif etype in (EntityType.CONVEYOR, EntityType.SPLITTER):
                rank = 2
            else:
                rank = 3
            key = (rank, hp, tile.x, tile.y)
            if best is None or key < best[0]:
                best = (key, tile, bid, hp)
        if best is None:
            return False

        _, tile, bid, hp = best
        try:
            ct.fire(tile)
        except GameError:
            return False
        self.target_id = bid
        if hp <= 2:
            # That shot killed it. A rebuilt harvester goes back on the same ore
            # tile, so this is the spot worth orbiting.
            self.killzone = tile
            self.loiter_since = ct.get_current_round()
            ct.write_store(SLOT_KILLZONE, pack_pos(tile))
            self.target_id = None
        return True

    def _hunt_target(self, ct: Controller, pos: Position, sightings: list) -> Position | None:
        """Nearest visible enemy economy, harvesters strictly first.

        Following the conveyor spine falls out of this for free: once the
        harvesters in sight are gone, the nearest remaining economy IS the spine
        leading further into their territory.
        """
        if self.target_id is not None:
            for _etype, bid, where in sightings:
                if bid == self.target_id:
                    if abs(where.x - pos.x) + abs(where.y - pos.y) <= 1:
                        return None
                    return where
            self.target_id = None

        best = None
        for etype, _bid, where in sightings:
            rank = 0 if etype == EntityType.HARVESTER else 1
            key = (rank, pos.distance_squared(where), where.x, where.y)
            if best is None or key < best[0]:
                best = (key, where)
        if best is None:
            return None
        # Do not adopt a target we already stand next to -- the attack branch
        # above owns that case; this one is purely for walking.
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
        # Perpendicular to the approach axis. Raiders leave in pairs and the two
        # sides are chosen by role parity, so a wave arrives on two faces of the
        # enemy economy rather than single-file down one lane.
        flip = 1 if (self.role is None or self.role % 2 == 0) else -1
        if abs(dx) >= abs(dy):
            off = Position(self.enemy.x, self.enemy.y + APPROACH_OFFSET * flip)
            alt = Position(self.enemy.x, self.enemy.y - APPROACH_OFFSET * flip)
        else:
            off = Position(self.enemy.x + APPROACH_OFFSET * flip, self.enemy.y)
            alt = Position(self.enemy.x - APPROACH_OFFSET * flip, self.enemy.y)
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
    # THE LATE STRIKE -- 2-3 turrets in the enemy Core's face
    # ------------------------------------------------------------------

    def _strike_turn(self, ct: Controller, rnd: int, pos: Position) -> None:
        """Walk in and plant turrets that can actually hit the Core.

        Sentinel and Gunner both fire a single-tile-wide LINE, so a turret that
        is not on a row / column / diagonal through a Core footprint tile can
        never hit the Core no matter how close it stands. Sites are therefore
        chosen by asking can_fire_from() for the hypothetical turret against
        each of the four footprint tiles, never by proximity alone.
        """
        if self.enemy is None:
            return
        planted = ct.read_store(SLOT_STRIKE_TURRETS)
        if planted >= STRIKE_TURRETS:
            # Job done: stay and repair the siege rather than walk home.
            if ct.get_action_cooldown() == 0 and self._try_heal(ct, pos):
                return
            hurt = self._damaged_friendly(ct, pos)
            if hurt is not None and pos.distance_squared(hurt) > 1:
                self._step_toward(ct, hurt)
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
            # Sentinel-led: the r^2=32 line that ignores obstacles is what does
            # the work; the Gunner is the last slot, planted closest in.
            etype = EntityType.GUNNER if planted >= STRIKE_TURRETS - 1 else EntityType.SENTINEL
            rng = GUNNER_RANGE_SQ if etype == EntityType.GUNNER else SENTINEL_RANGE_SQ
            cost = ct.get_gunner_cost() if etype == EntityType.GUNNER else ct.get_sentinel_cost()
            if ct.get_global_resources() >= cost:
                if self._plant_turret(ct, pos, etype, rng):
                    ct.write_store(SLOT_STRIKE_TURRETS, planted + 1)
                    if planted + 1 < STRIKE_TURRETS:
                        self._set_lateral_target(ct, rnd, pos)
                    return
        self._step_toward(ct, nearest_core_tile(pos, self.enemy))

    def _plant_turret(self, ct: Controller, pos: Position, etype: EntityType, range_sq: int) -> bool:
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
                if dist > range_sq:
                    continue
                facing = site.direction_to(tile)
                if facing == Direction.CENTRE:
                    continue
                try:
                    if not ct.can_fire_from(site, facing, etype, tile):
                        continue
                    if not ct.can_build(etype, site, facing):
                        continue
                except GameError:
                    continue
                key = (dist, site.x, site.y)
                if best is None or key < best[0]:
                    best = (key, site, facing)
        if best is None:
            return False
        try:
            ct.build(etype, best[1], best[2])
        except GameError:
            return False
        return True

    def _set_lateral_target(self, ct: Controller, rnd: int, pos: Position) -> None:
        """Shift off the approach axis so the next turret comes in on a second
        angle and one blocker cannot eat both lines.
        """
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

    def _is_forward(self, ct: Controller, pos: Position) -> bool:
        """Strike turret (deep in enemy territory) or home turret?

        The two have different jobs: a strike turret staggers its Core shots so
        the siege lands damage nearly every round despite the reload, a home
        turret shoots everything it sees the moment it sees it.
        """
        if self.forward is None:
            self._locate(ct)
            if self.enemy is None or self.home is None:
                return False
            self.forward = pos.distance_squared(self.enemy) < pos.distance_squared(self.home)
        return self.forward

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
        pos = ct.get_position()
        self._locate(ct)
        self._report_enemy_economy(ct)

        best_core, best_any = self._scan_line(ct, pos)
        choice = best_core or best_any
        if choice is not None:
            try:
                if ct.can_fire(choice[1]):
                    ct.fire(choice[1])
            except GameError:
                return
            return

        # Nothing on the line: rotate to reacquire rather than relocate. A
        # Gunner is 20 Ti of permanent presence and a rotation is 10 Ti; walking
        # a builder out to rebuild one elsewhere costs both far more.
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
        """Enemy Core first, always.

        Sentinel reload is 2, so two strike Sentinels firing on the same parity
        leave the Core a free round every other round; on opposite parities the
        Core takes 18 damage every round instead. Each claims a parity on its
        first turn from a store counter. Home Sentinels never stagger -- a
        defender that skips a round is a defender that lets a raider through.
        """
        pos = ct.get_position()
        self._locate(ct)
        self._report_enemy_economy(ct)

        best_core, best_any = self._scan_line(ct, pos)
        choice = best_core or best_any
        if choice is None:
            return

        if best_core is not None and self._is_forward(ct, pos):
            if self.stagger is None:
                nxt = ct.read_store(SLOT_TURRET_NEXT)
                self.stagger = nxt if nxt > 0 else 1
                ct.write_store(SLOT_TURRET_NEXT, self.stagger + 1)
                self.stagger -= 1
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
        """One step toward dst, with a watchdog for greedy pathing's failure
        mode: distance stops improving, and the unit rocks between two tiles
        forever. When that is detected the unit commits to a sideways waypoint
        for a fixed number of rounds, alternating side, which is enough to walk
        off the end of the wall that is blocking it. Deterministic throughout.
        """
        if dst is None:
            return False
        if ct.get_move_cooldown() != 0:
            return False
        pos = ct.get_position()

        dist = pos.distance_squared(dst)
        if self.travel_goal is None or dst.distance_squared(self.travel_goal) > 4:
            self.travel_goal = dst
            self.best_dist = dist
            self.no_progress = 0
            self.detour = None
            self.detour_left = 0
        elif dist < self.best_dist:
            self.travel_goal = dst
            self.best_dist = dist
            self.no_progress = 0
            self.detour = None
            self.detour_left = 0
        else:
            self.no_progress += 1

        if self.detour_left > 0:
            self.detour_left -= 1
            if self.detour is not None and self._raw_step(ct, pos, self.detour):
                return True
        elif self.no_progress >= NO_PROGRESS_LIMIT:
            self.detour = self._detour_point(ct, pos, dst)
            self.detour_left = DETOUR_ROUNDS
            self.no_progress = 0
            if self.detour is not None and self._raw_step(ct, pos, self.detour):
                return True
        return self._raw_step(ct, pos, dst)

    def _detour_point(self, ct: Controller, pos: Position, dst: Position) -> Position | None:
        """A waypoint DETOUR_DIST tiles to one side of the blocked heading.

        The side alternates on every trigger, so a unit that detours the wrong
        way around an obstruction tries the other way on its next attempt
        rather than grinding the same dead end.
        """
        dx = dst.x - pos.x
        dy = dst.y - pos.y
        if dx == 0 and dy == 0:
            return None
        self.detour_flip = -self.detour_flip
        norm = max(abs(dx), abs(dy), 1)
        px = int(round(-dy / norm * DETOUR_DIST)) * self.detour_flip
        py = int(round(dx / norm * DETOUR_DIST)) * self.detour_flip
        w, h = ct.get_map_width(), ct.get_map_height()
        return Position(
            min(max(pos.x + px, 0), w - 1),
            min(max(pos.y + py, 0), h - 1),
        )

    def _raw_step(self, ct: Controller, pos: Position, dst: Position) -> bool:
        """One cardinal step toward dst; if the preferred axis is blocked, try
        the other one, then the perpendiculars, then backwards. Deterministic.
        """
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
