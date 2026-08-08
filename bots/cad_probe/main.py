"""cad_probe -- CtrlAltDefeat's launcher-insertion opening, frozen as an instrument.

Provenance: replay-extracted from the 0-5 ladder sweep against team
"CtrlAltDefeat" (platform match e40a6c01, decoded 2026-08-07; full workup in
the session's `cad_insertion_diagnosis.md`).  Every one of those five games was
lost by `core_destroyed`, and every one of them opened with the same three
moves from CAD: a Launcher next to their own Core on round 1, two or three of
their own builders thrown at our Core on rounds 2-4, and a turret planted just
outside our Core's melee ring (median round 11, core-dist^2 10-41) that opened
fire on our Core the round after it was built.

The decoded medians this file targets:

  r0        Core converts a little titanium into ammunition (CAD did 8 Ti on
            each of r0/r1/r2, before the Launcher even existed) and spawns its
            first builder on the ring tile nearest the enemy
  r1        that builder plants a LAUNCHER on the Core-adjacent tile facing
            the enemy, then stands still inside the Launcher's pickup ring
  r2-r4     the Launcher throws raider #1, #2, #3 toward the enemy Core
            (observed jumps: dist^2 29-41, roughly halving the gap)
  r5-r15    raiders walk the remainder of the gap
  ~r11      raider #1 plants the first turret inside core-dist^2 10-41, facing
            a Core tile
  ~r12      that turret opens fire on the Core
  r12-...   raiders keep planting turrets (the decoded games reached 5, 11, 2,
            3 and 3 simultaneous in-band turrets) and barriers to shield them;
            dead raiders are replaced by newly thrown builders
  all game  home economy keeps running -- CAD matched or beat our harvester
            count by mid-game in 4 of 5 games, so the insertion is funded, not
            an all-in

What it actually achieves, measured on the two acceptance smokes (both won by
core destruction, no uncaught exception from this file in either):

  eider  (28x20, cores 144 dsq apart)  launcher r1, throws r2/r4/r6,
         first sentry r3 at core-dist^2 9, first fire on the enemy Core r4,
         harvesters r11/r23/r34, enemy Core dead r196-r227 across reruns
  hive   (cores 650 dsq apart -- the map-size outlier)  launcher r1, throws
         r2/r4/r6 landing at dist^2 313, raiders walk the rest, first sentry
         r84, first fire r85, harvesters from r12, Core dead r141-r157

The script beats (launcher / throws / first fire) are identical run to run;
only the kill round moves, and that is the opponent's variance, not this
file's -- nothing here is random.

Two deliberate deviations from the decoded timings, both in the same
direction -- this probe is a slightly HARSHER instrument than the original:

  - Throws land on r2/r4/r6 rather than CAD's r2/r3/r4.  The Core waits
    SPAWN_HOLD_RNDS after each spawn because a fresh builder's first heartbeat
    is a buffered write and spawning blind through that blind spot overshoots
    the population cap.
  - The first sentry goes up around r3-r4 on a tight map instead of CAD's
    median r11.  CAD's raiders dawdled after landing; this one plants the
    moment it is inside PLANT_BAND_SQ with an aligned site.  On a wide map
    (hive) the walk dominates and the timing lands close to CAD's own
    wide-map game (their r156, ours r84).

That last point is what separates this probe from `bots/band_probe`.
band_probe is the Banminary *all-in*: one builder, no economy, everything
converted to ammunition, dead by round 60 if the rush fails.  cad_probe is the
*funded* insertion: the raid never stops because the economy never stops.

INSTRUMENT, NOT A LADDER BOT.  This file exists so defensive changes can be
gated against CAD's specific pressure repeatably.  It is deliberately simple in
strategy terms; what it must NOT be is fragile in code terms -- an uncaught
exception permanently deletes the unit for the rest of the match, so every
unit's turn body is wrapped and every mutating call is gated by its can_*()
predicate.  (No try/finally anywhere: the platform's bot-code validator rejects
`finally` blocks outright -- see docs/tooling.md.)

Deterministic: no random anywhere.  Ties break on (distance, x, y).

Communication store slots:
   0  SLOT_HOME          packed position of our own Core
   1  SLOT_ENEMY         packed position of the enemy Core, once sighted
   2  SLOT_LAUNCHER_POS  packed position of the Launcher, once built
   3  SLOT_THROW_REQ     packed position of a raider asking to be thrown
   4  SLOT_TURRETS       forward turrets planted at the enemy Core
   5  SLOT_BARRIERS      forward barriers planted at the enemy Core
   6  SLOT_RAID_BEAT_0   round+1 of raider seat 0's last turn
   7  SLOT_RAID_BEAT_1   round+1 of raider seat 1's last turn
   8  SLOT_RAID_BEAT_2   round+1 of raider seat 2's last turn
   9  SLOT_HARVESTERS    harvesters built
  10  SLOT_THROWN        throws performed by the Launcher
  11..14 SLOT_HOME_BEAT_0..3  round+1 of each home builder's last turn
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
SLOT_LAUNCHER_POS = 2
SLOT_THROW_REQ = 3
SLOT_TURRETS = 4
SLOT_BARRIERS = 5
SLOT_RAID_BEAT_0 = 6
SLOT_RAID_BEAT_1 = 7
SLOT_RAID_BEAT_2 = 8
SLOT_HARVESTERS = 9
SLOT_THROWN = 10
SLOT_HOME_BEAT_0 = 11

RAID_BEATS = (SLOT_RAID_BEAT_0, SLOT_RAID_BEAT_1, SLOT_RAID_BEAT_2)
HOME_BEATS = (SLOT_HOME_BEAT_0, 12, 13, 14)

ROLE_RAIDER = 1
ROLE_HOME = 2

# --- engine constants used as geometry, not as tuning ----------------------
SENTINEL_RANGE_SQ = 32   # sentinel vision/attack r^2
GUNNER_RANGE_SQ = 13     # gunner vision/attack r^2
LAUNCH_RANGE_SQ = 26     # launcher throw r^2, measured from the launcher
LAUNCH_PICKUP_SQ = 2     # launcher pickup r^2 (orthogonal + diagonal)

# --- tuning ----------------------------------------------------------------
# Opening ammunition.  CAD converted 8 Ti on each of rounds 0, 1 and 2 -- i.e.
# banked before a turret existed, so the first turret fires the round it is
# built.  Three rounds of 10 buys three gunner shots plus change.
OPENING_AMMO = 10
OPENING_AMMO_ROUNDS = 3
# Working ceiling once a forward turret exists.  Topped up every round out of
# titanium not reserved for pending builds, so the bank drains into ammunition
# at roughly the rate the turrets burn it (a sentinel on reload 2 costs 5
# ammo/round sustained; a gunner on reload 1 costs 2).
AMMO_CEILING = 70

# Raiders.  The three RAID_BEATS seats above match CAD's observed 2-3 thrown
# builders, and each seat is refilled when its heartbeat goes stale -- that is
# how CAD kept raiders arriving for hundreds of rounds after our launcher exile
# defence had already ejected the first wave.
#
# Two rounds of slack for the buffered store write, plus two for a turn lost
# to the engine's CPU interrupt (which kills a turn outright, it does not
# resume), so a merely-stalled raider is not mistaken for a dead one.
RAID_STALE_RNDS = 5

# Population.  CAD ran 5 builders by r50 and 7-10 by r200-300 while still
# funding the raid -- crucially their count CLIMBED, so the seats below are
# refilled on death, not a one-shot budget.  Three raider seats plus four home
# seats caps the team at seven live builders (builder cost scales +20% each).
# Rounds the Core waits after a spawn before trusting the heartbeat picture
# again: a fresh builder's first beat is a buffered write, so it is invisible
# for one round, and spawning blind in the meantime overshoots the cap.
SPAWN_HOLD_RNDS = 2

# The forward siege.  Decoded peak simultaneous in-band turrets across the five
# games: 5, 11, 2, 3, 3.  Eleven is the observed maximum and is used as the
# target so the probe reproduces the worst case, not the median.
TURRET_TARGET = 11
# CAD interleaved barriers with turrets (one every few turrets, always inside
# the band) to make the sentries expensive to clear.
BARRIER_PER_TURRET = 1

# Where a sentry may be planted.  The decoded first-sentry core-dist^2 values
# were 41, 18, 10, (n/a) and 25 -- note that 41 and 25 both sit OUTSIDE our own
# INTRUDER_CORE_DSQ=20 hunting band, which is exactly the geometric blind spot
# this probe exists to reproduce.  A site is only used if the turret can
# actually fire on a Core tile from it, so the effective ceiling is the
# sentinel's own range (32); the wider band still governs where the raider
# stops walking and starts looking.
PLANT_BAND_SQ = 45

# Stage A' fallbacks: if the Launcher never appears (blocked terrain, no
# affordable tile) or never throws, raiders stop waiting and walk.
LAUNCHER_GIVEUP_RND = 12
LAUNCH_WAIT_MAX = 20
# A one-tile hop is not worth a launcher action -- the raider walks that.
MIN_THROW_SQ = 4

# After planting a turret the raider sidesteps before planting the next one, so
# the sentries come in on different lines and one blocker cannot eat them all.
LATERAL_OFFSET = 3
REPOSITION_MAX_RNDS = 10

# Repairing a standing sentry is 1 Ti for +4 HP, versus the ~0.18 damage that
# titanium buys as ammunition.  The raider keeps the sentries alive whenever it
# has nothing to build.
HEAL_MIN_TITANIUM = 6

# Home economy.  Deliberately unclever: enough harvesters that the insertion
# never runs out of titanium, laid out along the trail the builder itself
# walked (see _lay_link), never a whole-map search.
HARVESTER_TARGET = 6
# Until this many harvesters exist, the ammunition converter stays shut past
# the opening bank, so builders and harvesters get first call on titanium.
# Lifted unconditionally at ECON_BOOTSTRAP_RND so a failed economy cannot
# silently disarm the siege as well.
ECON_BOOTSTRAP_HARVESTERS = 2
ECON_BOOTSTRAP_RND = 60
# Rounds a home builder will stand next to its chosen ore waiting for the bank
# before deciding the tile is genuinely unbuildable rather than merely
# unaffordable.
ORE_WAIT_MAX = 30
MAX_TRAIL = 36
LINK_MAX_RNDS = 90
LINK_FAIL_LIMIT = 4
# Titanium held back from the ammunition converter so the raid always has a
# turret in its pocket.  Falls to zero once the siege is complete.
TURRET_RESERVE_MULT = 1

# Bail at a phase boundary rather than let the engine truncate a statement.
# NOTE: get_cpu_time_elapsed() reads 0 under local `fcode run` even with --tle
# (docs/tooling.md), so this guard only bites on ladder hardware.
CPU_BUDGET_US = 7500

CARDINALS = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)

# Competition-map Core anchors, copied from bots/_v70cm.  Several pool maps are
# mirror-symmetric rather than 180-degree symmetric, so (w-2-x, h-2-y) is not
# generally the enemy Core; the rotational fallback below keeps the probe
# usable on an unknown map.
CORE_PAIRS = (
    (18, 18, 2, 14, 14, 2), (26, 26, 3, 22, 21, 2),
    (21, 8, 0, 6, 19, 6), (16, 16, 2, 11, 12, 3),
    (12, 12, 1, 8, 9, 2), (20, 20, 2, 15, 16, 3),
    (25, 25, 2, 20, 21, 3), (16, 16, 0, 0, 14, 14),
    (28, 20, 2, 8, 24, 8), (14, 18, 2, 2, 2, 14),
    (24, 24, 2, 2, 20, 20), (24, 24, 2, 11, 20, 11),
    (16, 12, 4, 5, 10, 5), (22, 22, 2, 17, 18, 3),
    (10, 10, 1, 1, 7, 7), (20, 26, 2, 2, 2, 22),
    (12, 8, 0, 6, 10, 0), (25, 15, 0, 0, 0, 13),
    (21, 21, 2, 2, 2, 17), (11, 16, 0, 0, 9, 0),
    (24, 24, 2, 19, 20, 3),
    (21, 8, 5, 3, 14, 3), (26, 26, 5, 5, 19, 19),
    (10, 10, 2, 2, 6, 6), (16, 16, 3, 3, 11, 11),
    (14, 18, 6, 4, 6, 12), (20, 26, 9, 6, 9, 18),
    (28, 20, 7, 9, 19, 9), (25, 15, 11, 3, 11, 10),
    (25, 25, 5, 5, 18, 18), (24, 24, 4, 4, 18, 18),
)


def pack_pos(pos: Position) -> int:
    """Encode a position into one store int, offset so (0,0) is not 'empty'."""
    return ((pos.x + 1) << 16) | (pos.y + 1)


def unpack_pos(val: int):
    if val <= 0:
        return None
    return Position((val >> 16) - 1, (val & 0xFFFF) - 1)


def core_footprint(nw: Position):
    """The 4 tiles of a Core's 2x2 footprint, given its NW corner."""
    return (
        nw,
        Position(nw.x + 1, nw.y),
        Position(nw.x, nw.y + 1),
        Position(nw.x + 1, nw.y + 1),
    )


def nearest_core_tile(pos: Position, core_nw: Position) -> Position:
    best = None
    for t in core_footprint(core_nw):
        key = (pos.distance_squared(t), t.x, t.y)
        if best is None or key < best[0]:
            best = (key, t)
    return best[1]


def core_dist_sq(pos: Position, core_nw: Position) -> int:
    return pos.distance_squared(nearest_core_tile(pos, core_nw))


def touches_core(pos: Position, core_nw: Position) -> bool:
    """Orthogonally adjacent to some Core footprint tile -- i.e. a legal
    conveyor terminus that can actually output into the Core."""
    for t in core_footprint(core_nw):
        if abs(pos.x - t.x) + abs(pos.y - t.y) == 1:
            return True
    return False


def on_core(pos: Position, core_nw: Position) -> bool:
    return core_nw.x <= pos.x <= core_nw.x + 1 and core_nw.y <= pos.y <= core_nw.y + 1


def enemy_core_for(w: int, h: int, own: Position) -> Position:
    for mw, mh, ax, ay, bx, by in CORE_PAIRS:
        if w != mw or h != mh:
            continue
        if own.x == ax and own.y == ay:
            return Position(bx, by)
        if own.x == bx and own.y == by:
            return Position(ax, ay)
    return Position(max(0, w - 2 - own.x), max(0, h - 2 - own.y))


def nearest_cardinal(d: Direction) -> Direction:
    if d == Direction.NORTHEAST or d == Direction.SOUTHEAST:
        return Direction.EAST
    if d == Direction.SOUTHWEST or d == Direction.NORTHWEST:
        return Direction.WEST
    if d == Direction.CENTRE:
        return Direction.NORTH
    return d


class Player:
    def __init__(self):
        # --- shared map knowledge (one Player instance per unit) -----------
        self.home = None
        self.enemy = None
        self.enemy_confirmed = False

        # --- Core ----------------------------------------------------------
        self.spawn_hold = 0
        self.ammo_rounds_done = 0

        # --- builder: identity ---------------------------------------------
        self.role = None
        self.seat = -1
        self.beat_slot = None
        self.home_n = 0

        # --- builder: shared movement state ---------------------------------
        self.prev_pos = None
        self.stuck = 0
        self.detour = None
        self.detour_left = 0

        # --- raider ---------------------------------------------------------
        self.delivered = False
        self.launcher_pos = None
        self.wait_start = None
        self.reposition_target = None
        self.reposition_start = 0
        self.no_fire_tiles = set()

        # --- home builder ----------------------------------------------------
        self.trail = []
        self.link_trail = None
        self.link_i = 0
        self.link_start = 0
        self.link_fails = 0
        self.ore_target = None
        self.ore_wait = 0
        self.dead_ore = set()

        # --- launcher --------------------------------------------------------
        self.throw_sites = None
        self.launched = set()

        self.reported_error = False

    # ------------------------------------------------------------------
    # entry point
    # ------------------------------------------------------------------

    def run(self, ct: Controller) -> None:
        """An exception escaping run() permanently deletes this unit for the
        rest of the match, so the guard is unconditional.  Never try/finally --
        the platform validator rejects `finally` blocks.
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
        elif etype == EntityType.LAUNCHER:
            self._run_launcher(ct)
        elif etype == EntityType.SENTINEL or etype == EntityType.GUNNER:
            self._run_turret(ct)

    def _cpu_exhausted(self, ct: Controller) -> bool:
        return ct.get_cpu_time_elapsed() >= CPU_BUDGET_US

    def _in_bounds(self, ct: Controller, pos: Position) -> bool:
        """On the map.  Necessary but not sufficient before a tile query --
        tile getters also raise GameError for in-bounds tiles outside vision.
        """
        return 0 <= pos.x < ct.get_map_width() and 0 <= pos.y < ct.get_map_height()

    # ------------------------------------------------------------------
    # map knowledge
    # ------------------------------------------------------------------

    def _locate(self, ct: Controller) -> None:
        """Establish home and enemy Core positions as cheaply as possible:
        sight them, else read the store, else look the pair up in CORE_PAIRS,
        else fall back to 180-degree rotation.
        """
        if self.home is None or not self.enemy_confirmed:
            my_team = ct.get_team()
            try:
                nearby = ct.get_nearby_buildings()
            except GameError:
                nearby = ()
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
            self.enemy = enemy_core_for(
                ct.get_map_width(), ct.get_map_height(), self.home
            )

    # ==================================================================
    # CORE
    # ==================================================================

    def _run_core(self, ct: Controller) -> None:
        """Spawn the raid, fund the raid, and convert the rest to ammunition.

        convert_ammo() does not consume the action cooldown, so converting
        never costs a spawn -- it is always tried first, exactly as CAD's
        r0/r1/r2 conversions happened alongside their opening spawns.
        """
        pos = ct.get_position()
        if self.home is None:
            self.home = pos
            ct.write_store(SLOT_HOME, pack_pos(pos))
        self._locate(ct)

        rnd = ct.get_current_round()
        turrets = ct.read_store(SLOT_TURRETS)

        # Titanium owed to builds that have not happened yet.  Ammunition must
        # never out-compete the siege it is meant to feed, but every titanium
        # pinned past the last build is a shot the siege never fires, so the
        # reserve falls as the plan completes.
        #
        # This number is the single point of truth for BOTH the converter and
        # the spawner.  Getting that wrong is a death spiral, not a rounding
        # error: an earlier revision let the converter drain the bank to
        # `reserve` while the spawner demanded `builder_cost + reserve`, so
        # after round 4 no builder was ever spawned again -- no home builders,
        # no harvesters, 0 titanium mined in a 405-round game.
        harvesters = ct.read_store(SLOT_HARVESTERS)
        reserve = 0
        if ct.read_store(SLOT_LAUNCHER_POS) <= 0 and rnd <= LAUNCHER_GIVEUP_RND:
            reserve += ct.get_launcher_cost()
        if turrets < TURRET_TARGET:
            reserve += TURRET_RESERVE_MULT * ct.get_sentinel_cost()
        if harvesters < HARVESTER_TARGET:
            reserve += ct.get_harvester_cost()
        free_seats = self._free_seats(ct, rnd)
        if free_seats > 0:
            reserve += ct.get_builder_bot_cost()

        self._convert(ct, rnd, turrets, harvesters, reserve)

        if ct.get_action_cooldown() != 0:
            return
        if free_seats <= 0 or rnd < self.spawn_hold:
            return
        if self._cpu_exhausted(ct):
            return
        self._spawn(ct, pos, rnd, reserve)

    def _free_seats(self, ct: Controller, rnd: int) -> int:
        """Seats whose holder has stopped beating -- i.e. builders to replace.

        This is what keeps the raid alive across hundreds of rounds: CAD's
        exiled and killed raiders were continuously replaced, which is why our
        launcher exile defence ejected the first wave and then lost anyway.
        """
        n = 0
        for slot in RAID_BEATS + HOME_BEATS:
            val = ct.read_store(slot)
            if val == 0 or rnd - (val - 1) > RAID_STALE_RNDS:
                n += 1
        return n

    def _convert(
        self, ct: Controller, rnd: int, turrets: int, harvesters: int, reserve: int
    ) -> None:
        if self.ammo_rounds_done < OPENING_AMMO_ROUNDS:
            if ct.can_convert_ammo(OPENING_AMMO):
                ct.convert_ammo(OPENING_AMMO)
                self.ammo_rounds_done += 1
            return
        if turrets <= 0:
            return
        # Bootstrap guard.  What separates CAD from an all-in rush is that the
        # insertion stayed funded all game, and it only stays funded if the
        # first harvesters get built ahead of the first big conversion (CAD's
        # own big conversions land at r10-r16, after their economy starts).
        # The guard lifts on a deadline so a probe whose economy failed still
        # applies pressure instead of sitting on a full bank.
        if harvesters < ECON_BOOTSTRAP_HARVESTERS and rnd < ECON_BOOTSTRAP_RND:
            return
        ammo = ct.get_global_ammo()
        if ammo >= AMMO_CEILING:
            return
        spare = ct.get_global_resources() - reserve
        amount = min(AMMO_CEILING - ammo, spare)
        if amount > 0 and ct.can_convert_ammo(amount):
            ct.convert_ammo(amount)

    def _spawn(self, ct: Controller, pos: Position, rnd: int, reserve: int) -> None:
        cost = ct.get_builder_bot_cost()
        # `reserve` ALREADY contains one builder cost (the caller adds it
        # whenever a seat is free), so the test is `>= reserve`, never
        # `>= cost + reserve` -- see the note in _run_core.
        if ct.get_global_resources() < max(cost, reserve):
            return

        # Spawn on the ring tile nearest the enemy: that is where the Launcher
        # goes, so raiders land inside its pickup ring on the turn they appear.
        # The whole ring is enumerated via get_nearby_tiles(8) and filtered by
        # can_spawn(), never by pos.add(d) -- that only reaches the N/W half of
        # the ring and is an absolute-direction bug that decides maps by seat.
        anchor = self.enemy if self.enemy is not None else pos
        best = None
        for tile in ct.get_nearby_tiles(dist_sq=8):
            try:
                if not ct.can_spawn(tile):
                    continue
            except GameError:
                continue
            key = (tile.distance_squared(anchor), tile.x, tile.y)
            if best is None or key < best[0]:
                best = (key, tile)
        if best is not None:
            ct.spawn_builder(best[1])
            self.spawn_hold = rnd + SPAWN_HOLD_RNDS

    # ==================================================================
    # BUILDER BOT
    # ==================================================================

    def _run_builder(self, ct: Controller) -> None:
        rnd = ct.get_current_round()
        pos = ct.get_position()
        self._locate(ct)

        if self.role is None:
            self._claim_role(ct, rnd)

        # Movement bookkeeping shared by both roles.  A position change of more
        # than one step can only have come from a launcher throw -- that, not a
        # round number, is what ends a raider's wait.
        jumped = False
        if self.prev_pos is not None:
            if pos == self.prev_pos:
                self.stuck += 1
            else:
                self.stuck = 0
                if pos.distance_squared(self.prev_pos) > 2:
                    jumped = True
        self.prev_pos = pos

        if self.beat_slot is not None:
            ct.write_store(self.beat_slot, rnd + 1)

        if self.role == ROLE_RAIDER:
            self._run_raider(ct, rnd, pos, jumped)
        else:
            self._run_home(ct, rnd, pos)

    def _claim_role(self, ct: Controller, rnd: int) -> None:
        """Claim the lowest raider seat whose heartbeat is missing or stale;
        failing that, the lowest free home seat.

        Raider seats are filled first, which is what reproduces CAD's opening:
        the first three builders are all thrown, and home economy only starts
        once the raid has its bodies.

        The Core spawns at most one builder per turn and a fresh builder claims
        on its first turn, so two units cannot normally contend for a seat.  If
        they ever did, the cost is one extra unit on that seat -- harmless.
        """
        for i, slot in enumerate(RAID_BEATS):
            val = ct.read_store(slot)
            if val == 0 or rnd - (val - 1) > RAID_STALE_RNDS:
                self.seat = i
                self.role = ROLE_RAIDER
                self.beat_slot = slot
                ct.write_store(slot, rnd + 1)
                return
        for i, slot in enumerate(HOME_BEATS):
            val = ct.read_store(slot)
            if val == 0 or rnd - (val - 1) > RAID_STALE_RNDS:
                self.seat = i
                self.role = ROLE_HOME
                self.home_n = i
                self.beat_slot = slot
                ct.write_store(slot, rnd + 1)
                return
        # Every seat is held (only reachable if the Core over-spawned through
        # the buffered-write blind spot): be a home builder with no seat.
        self.seat = -1
        self.role = ROLE_HOME
        self.home_n = 0

    # ------------------------------------------------------------------
    # raider
    # ------------------------------------------------------------------

    def _run_raider(self, ct: Controller, rnd: int, pos: Position, jumped: bool) -> None:
        if jumped:
            self.delivered = True
        if self.enemy is not None and self.home is not None:
            if pos.distance_squared(self.enemy) < pos.distance_squared(self.home):
                self.delivered = True

        if self.launcher_pos is None:
            self.launcher_pos = unpack_pos(ct.read_store(SLOT_LAUNCHER_POS))
            if self.launcher_pos is not None and self.wait_start is None:
                self.wait_start = rnd

        waiting = self._waiting_for_throw(ct, rnd, pos)
        if waiting:
            # Ask to be picked up.  The Launcher only ever throws a builder
            # that has asked, which is what keeps home builders on the ground.
            ct.write_store(SLOT_THROW_REQ, pack_pos(pos))

        acted = False
        if ct.get_action_cooldown() == 0 and not self._cpu_exhausted(ct):
            if self._build_launcher(ct, rnd, pos):
                return
            if not waiting:
                acted = self._forward_work(ct, rnd, pos)
        if acted:
            return
        if self._cpu_exhausted(ct):
            return
        self._raider_move(ct, rnd, pos, waiting)

    def _waiting_for_throw(self, ct: Controller, rnd: int, pos: Position) -> bool:
        """True while this raider is still queueing for the Launcher."""
        if self.delivered:
            return False
        if self.launcher_pos is None:
            return rnd <= LAUNCHER_GIVEUP_RND
        if self.wait_start is not None and rnd - self.wait_start > LAUNCH_WAIT_MAX:
            self.delivered = True
            return False
        # If the Launcher has been killed, stop queueing for a ghost.
        if pos.distance_squared(self.launcher_pos) <= 8:
            try:
                if ct.get_tile_building_id(self.launcher_pos) is None:
                    self.launcher_pos = None
                    self.delivered = True
                    return False
            except GameError:
                pass
        return pos.distance_squared(self.launcher_pos) <= LAUNCH_PICKUP_SQ

    def _build_launcher(self, ct: Controller, rnd: int, pos: Position) -> bool:
        """CAD's round-1 move: a Launcher on the Core-adjacent tile facing the
        enemy, built by the very first builder before it does anything else.
        """
        if self.delivered or rnd > LAUNCHER_GIVEUP_RND:
            return False
        if unpack_pos(ct.read_store(SLOT_LAUNCHER_POS)) is not None:
            return False
        if self.launcher_pos is not None or self.enemy is None:
            return False
        if ct.get_global_resources() < ct.get_launcher_cost():
            return False

        best = None
        for d in CARDINALS:
            tile = pos.add(d)
            if not self._in_bounds(ct, tile):
                continue
            try:
                if not ct.can_build_launcher(tile):
                    continue
            except GameError:
                continue
            key = (tile.distance_squared(self.enemy), tile.x, tile.y)
            if best is None or key < best[0]:
                best = (key, tile)
        if best is None:
            return False

        try:
            ct.build_launcher(best[1])
        except GameError:
            return False
        self.launcher_pos = best[1]
        self.wait_start = rnd
        ct.write_store(SLOT_LAUNCHER_POS, pack_pos(best[1]))
        return True

    def _forward_work(self, ct: Controller, rnd: int, pos: Position) -> bool:
        """Everything a delivered raider does with an action: keep the sentries
        alive first, then plant the next turret, then shield it.
        """
        if not self.delivered or self.enemy is None:
            return False
        if core_dist_sq(pos, self.enemy) > PLANT_BAND_SQ:
            return False

        if self._repair(ct, pos):
            return True
        if self.reposition_target is not None:
            return False  # sidestep to a fresh angle first, plant after

        turrets = ct.read_store(SLOT_TURRETS)
        if turrets < TURRET_TARGET and self._plant_turret(ct, pos):
            ct.write_store(SLOT_TURRETS, turrets + 1)
            self._set_lateral_target(ct, rnd, pos)
            return True

        barriers = ct.read_store(SLOT_BARRIERS)
        if turrets > 0 and barriers < turrets * BARRIER_PER_TURRET:
            if self._plant_barrier(ct, pos):
                ct.write_store(SLOT_BARRIERS, barriers + 1)
                return True
        return False

    def _econ_floor(self, ct: Controller) -> int:
        """Titanium a raider must leave in the bank for the home economy.

        The cost scale in this engine is TEAM-WIDE, not per category (there is
        one get_scale_percent(), and it is what every get_*_cost() multiplies).
        So every sentry the raid plants also raises the price of the next
        harvester: measured on eider, three opening sentinels pushed the first
        harvester from 20 Ti to 58 Ti, the home builder stood next to its ore
        unable to pay for 170 rounds, and the probe mined nothing until r181.
        A raider that spends the last harvester out of the bank is spending its
        own funding.
        """
        harvesters = ct.read_store(SLOT_HARVESTERS)
        if harvesters >= HARVESTER_TARGET:
            return 0
        floor = ct.get_harvester_cost()
        if harvesters < ECON_BOOTSTRAP_HARVESTERS:
            floor += ct.get_builder_bot_cost()
        return floor

    def _plant_turret(self, ct: Controller, pos: Position) -> bool:
        """Build a sentry on an orthogonally adjacent tile from which it can
        actually hit an enemy Core tile.

        Both turret types fire a single-tile-wide LINE, so proximity is
        worthless without alignment: the site is chosen by asking
        can_fire_from() for the hypothetical turret against each of the four
        Core footprint tiles, and the nearest legal (site, facing) pair wins.
        Sentinel first -- 18 damage, r^2=32, and its line ignores obstacles,
        which is what lets a sentry sit outside a defender's hunting band and
        still chip the Core.
        """
        targets = core_footprint(self.enemy)
        floor = self._econ_floor(ct)
        for etype, range_sq, cost in (
            (EntityType.SENTINEL, SENTINEL_RANGE_SQ, ct.get_sentinel_cost()),
            (EntityType.GUNNER, GUNNER_RANGE_SQ, ct.get_gunner_cost()),
        ):
            if ct.get_global_resources() < cost + floor:
                continue
            best = None
            for d in CARDINALS:
                site = pos.add(d)
                if not self._in_bounds(ct, site):
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
                continue
            try:
                ct.build(etype, best[1], best[2])
            except GameError:
                continue
            # Remember this sentry's line so a later barrier never blocks it.
            try:
                for tile in ct.get_attackable_tiles_from(best[1], best[2], etype):
                    self.no_fire_tiles.add((tile.x, tile.y))
            except GameError:
                pass
            return True
        return False

    def _plant_barrier(self, ct: Controller, pos: Position) -> bool:
        """A 30 HP shield on the Core-facing side of the sentries, never on a
        tile one of our own sentries needs to shoot through.
        """
        need = ct.get_barrier_cost() + ct.get_sentinel_cost() + self._econ_floor(ct)
        if ct.get_global_resources() < need:
            return False
        best = None
        for d in CARDINALS:
            tile = pos.add(d)
            if not self._in_bounds(ct, tile):
                continue
            if (tile.x, tile.y) in self.no_fire_tiles:
                continue
            try:
                if not ct.can_build_barrier(tile):
                    continue
            except GameError:
                continue
            key = (core_dist_sq(tile, self.enemy), tile.x, tile.y)
            if best is None or key < best[0]:
                best = (key, tile)
        if best is None:
            return False
        try:
            ct.build_barrier(best[1])
        except GameError:
            return False
        return True

    def _repair(self, ct: Controller, pos: Position) -> bool:
        """1 Ti buys +4 HP on an adjacent friendly building.  This is what
        turned CAD's sentries from a one-off nuisance into a standing siege.
        """
        if ct.get_global_resources() < HEAL_MIN_TITANIUM:
            return False
        my_team = ct.get_team()
        for d in CARDINALS:
            tile = pos.add(d)
            if not self._in_bounds(ct, tile):
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

    def _set_lateral_target(self, ct: Controller, rnd: int, pos: Position) -> None:
        """Shift a few tiles off the approach axis so the next sentry comes in
        on a different line from the last one.
        """
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
            if not self._in_bounds(ct, c):
                continue
            if core_dist_sq(c, self.enemy) > PLANT_BAND_SQ:
                continue
            self.reposition_target = c
            self.reposition_start = rnd
            return

    def _raider_move(self, ct: Controller, rnd: int, pos: Position, waiting: bool) -> None:
        if ct.get_move_cooldown() != 0:
            return

        if waiting:
            if self.launcher_pos is None:
                return  # the Launcher is still being paid for; hold the ring
            if pos.distance_squared(self.launcher_pos) > LAUNCH_PICKUP_SQ:
                self._step_toward(ct, pos, self.launcher_pos)
            return
        if not self.delivered:
            return

        if self.reposition_target is not None:
            if (
                pos == self.reposition_target
                or self.stuck >= 3
                or rnd - self.reposition_start > REPOSITION_MAX_RNDS
            ):
                self.reposition_target = None
            else:
                self._step_toward(ct, pos, self.reposition_target)
                return

        if self.enemy is None:
            return
        # Nothing left to build near a sentry: park on a damaged one so the
        # repair branch can reach it, otherwise keep pressing the Core.
        hurt = self._damaged_building(ct, pos)
        if hurt is not None:
            if pos.distance_squared(hurt) > 1:
                self._step_toward(ct, pos, hurt)
            return
        self._step_toward(ct, pos, nearest_core_tile(pos, self.enemy))

    def _damaged_building(self, ct: Controller, pos: Position):
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
                if ct.get_entity_type(bid) not in (
                    EntityType.SENTINEL, EntityType.GUNNER, EntityType.BARRIER
                ):
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

    # ------------------------------------------------------------------
    # home builder -- harvesters, plus a conveyor chain along its own trail
    # ------------------------------------------------------------------

    def _run_home(self, ct: Controller, rnd: int, pos: Position) -> None:
        if self._cpu_exhausted(ct):
            return
        if self.link_trail is not None:
            if self._lay_link(ct, rnd, pos):
                return

        self._record_trail(pos)

        if ct.get_action_cooldown() == 0 and not self._cpu_exhausted(ct):
            if self._build_harvester(ct, pos):
                return
            if self._repair_home(ct, pos):
                return

        if self._cpu_exhausted(ct):
            return
        self._home_move(ct, rnd, pos)

    def _record_trail(self, pos: Position) -> None:
        """Remember the path this builder actually walked.  It is by
        construction a connected run of passable tiles from the Core to the
        ore, which makes it a valid conveyor route without ever running a
        search over terrain the unit cannot see.

        A trail may only START on a tile orthogonally adjacent to the Core
        footprint.  A chain that starts anywhere else has no valid terminus --
        its Core-end conveyor would output into open ground -- and the whole
        chain is then wasted titanium.  (Measured on eider: harvesters 2-5 all
        produced zero conveyors because their trails began wherever the
        previous chain happened to end.)
        """
        if not self.trail:
            if self.home is not None and touches_core(pos, self.home):
                self.trail.append(pos)
            return
        if self.trail[-1] == pos:
            return
        for i in range(len(self.trail) - 1, -1, -1):
            if self.trail[i] == pos:
                del self.trail[i + 1:]
                return
        self.trail.append(pos)
        if len(self.trail) > MAX_TRAIL:
            del self.trail[0]

    def _build_harvester(self, ct: Controller, pos: Position) -> bool:
        if ct.read_store(SLOT_HARVESTERS) >= HARVESTER_TARGET:
            return False
        if ct.get_global_resources() < ct.get_harvester_cost():
            return False
        for d in CARDINALS:
            tile = pos.add(d)
            if not self._in_bounds(ct, tile):
                continue
            try:
                if ct.get_tile_env(tile) != Environment.ORE_TITANIUM:
                    continue
                if not ct.can_build_harvester(tile):
                    continue
            except GameError:
                continue
            try:
                ct.build_harvester(tile)
            except GameError:
                continue
            ct.write_store(SLOT_HARVESTERS, ct.read_store(SLOT_HARVESTERS) + 1)
            self.ore_target = None
            self._start_link(pos)
            return True
        return False

    def _start_link(self, pos: Position) -> None:
        """Turn the walked trail into a conveyor plan.

        The head is re-checked against the Core footprint anyway: the trail can
        only have started on a Core-adjacent tile, but the Core spawn ring has
        r^2 <= 8 and so includes diagonals, and a conveyor on a diagonal tile
        would output into empty ground instead of into the Core.
        """
        self._record_trail(pos)
        trail = list(self.trail)
        self.trail = []
        if self.home is not None:
            head = None
            for i, t in enumerate(trail):
                if touches_core(t, self.home):
                    head = i
                    break
            if head is None:
                return
            trail = [t for t in trail[head:] if not on_core(t, self.home)]
        if not trail:
            return
        self.link_trail = trail
        self.link_i = len(trail) - 1
        self.link_start = 0
        self.link_fails = 0

    def _link_facing(self, ct: Controller, i: int) -> Direction:
        tile = self.link_trail[i]
        if i >= 1:
            d = tile.cardinal_direction_to(self.link_trail[i - 1])
        elif self.home is not None:
            d = tile.cardinal_direction_to(nearest_core_tile(tile, self.home))
        else:
            d = Direction.NORTH
        if d == Direction.CENTRE or not d.is_cardinal():
            d = nearest_cardinal(d)
        return d

    def _lay_link(self, ct: Controller, rnd: int, pos: Position) -> bool:
        """Walk the plan back toward the Core, laying a conveyor on the tile
        just vacated.  Building requires orthogonal adjacency and the tile must
        be free, so the builder always stands one link closer to the Core than
        the segment it is placing.
        """
        if self.link_start == 0:
            self.link_start = rnd
        if rnd - self.link_start > LINK_MAX_RNDS:
            self.link_trail = None
            return False

        while self.link_i >= 0:
            tile = self.link_trail[self.link_i]
            occupied = False
            try:
                occupied = ct.get_tile_building_id(tile) is not None
            except GameError:
                occupied = False
            if occupied:
                self.link_i -= 1
                self.link_fails = 0
                continue
            break
        if self.link_i < 0:
            self.link_trail = None
            return False

        tile = self.link_trail[self.link_i]

        if pos.distance_squared(tile) == 1:
            if ct.get_action_cooldown() != 0:
                return True
            if ct.get_global_resources() < ct.get_conveyor_cost():
                return False
            facing = self._link_facing(ct, self.link_i)
            built = False
            try:
                if ct.can_build_conveyor(tile, facing):
                    ct.build_conveyor(tile, facing)
                    built = True
            except GameError:
                built = False
            if built:
                self.link_i -= 1
                self.link_fails = 0
                return True
            self.link_fails += 1
            if self.link_fails > LINK_FAIL_LIMIT:
                self.link_i -= 1
                self.link_fails = 0
            return True

        if ct.get_move_cooldown() != 0:
            return True

        if pos == tile:
            # Standing on the segment we are meant to place (only happens for
            # the Core-end link): vacate to any passable neighbour.
            for d in CARDINALS:
                nxt = pos.add(d)
                if not self._in_bounds(ct, nxt):
                    continue
                if self.home is not None and on_core(nxt, self.home):
                    continue
                try:
                    if ct.can_move(d):
                        ct.move(d)
                        return True
                except GameError:
                    continue
            self.link_i -= 1
            return True

        stand = self.link_trail[self.link_i - 1] if self.link_i >= 1 else tile
        self._step_toward(ct, pos, stand)
        return True

    def _repair_home(self, ct: Controller, pos: Position) -> bool:
        """Patch an adjacent damaged harvester/conveyor when idle.  Cheap, and
        it keeps the pipeline alive through incidental chip damage.
        """
        if ct.get_global_resources() < 40:
            return False
        return self._repair(ct, pos)

    def _home_move(self, ct: Controller, rnd: int, pos: Position) -> None:
        if ct.get_move_cooldown() != 0:
            return

        # A trail (and therefore the next conveyor chain) can only begin on a
        # Core-adjacent tile, so a builder between jobs walks home first.  One
        # or two rounds per harvester trip, in exchange for every harvester
        # after the first actually being connected.
        if (
            not self.trail
            and self.home is not None
            and ct.read_store(SLOT_HARVESTERS) < HARVESTER_TARGET
        ):
            self._step_toward(ct, pos, nearest_core_tile(pos, self.home))
            return

        if self.ore_target is not None:
            reached = pos.distance_squared(self.ore_target) <= 1
            stale = False
            try:
                if ct.is_in_vision(self.ore_target):
                    if ct.get_tile_building_id(self.ore_target) is not None:
                        stale = True
                    elif ct.get_tile_env(self.ore_target) != Environment.ORE_TITANIUM:
                        stale = True
            except GameError:
                stale = False
            if reached:
                # Standing next to the ore and still not building is almost
                # always "cannot afford it yet" -- the team-wide cost scale
                # climbs every time the raid plants something.  Blacklisting an
                # ore tile for that reason is how an earlier revision walked a
                # builder around the whole map without ever mining anything, so
                # the tile is only given up when the titanium was there and the
                # build STILL did not happen.
                self.ore_wait += 1
                if self.ore_wait > ORE_WAIT_MAX and (
                    ct.get_global_resources() >= ct.get_harvester_cost()
                ):
                    stale = True
            else:
                self.ore_wait = 0

            if stale:
                self.dead_ore.add((self.ore_target.x, self.ore_target.y))
                self.ore_target = None
                self.ore_wait = 0
            elif reached:
                return  # adjacent; the build branch takes it next turn
            else:
                self._step_toward(ct, pos, self.ore_target)
                return

        if ct.read_store(SLOT_HARVESTERS) < HARVESTER_TARGET:
            self.ore_target = self._find_ore(ct, pos)
            if self.ore_target is not None:
                self._step_toward(ct, pos, self.ore_target)
                return
            self._explore(ct, pos)
            return

        # Economy complete: idle next to the Core where the repair branch can
        # reach the pipeline, and out of the raid's way.
        if self.home is not None and core_dist_sq(pos, self.home) > 8:
            self._step_toward(ct, pos, nearest_core_tile(pos, self.home))

    def _find_ore(self, ct: Controller, pos: Position):
        """Nearest visible unclaimed ore tile.  Vision-scoped, so this is ~70
        tile queries at worst and never a whole-map scan.
        """
        best = None
        try:
            tiles = ct.get_nearby_tiles()
        except GameError:
            return None
        for tile in tiles:
            key2 = (tile.x, tile.y)
            if key2 in self.dead_ore:
                continue
            try:
                if ct.get_tile_env(tile) != Environment.ORE_TITANIUM:
                    continue
                if ct.get_tile_building_id(tile) is not None:
                    continue
            except GameError:
                continue
            key = (pos.distance_squared(tile), tile.x, tile.y)
            if best is None or key < best[0]:
                best = (key, tile)
        return best[1] if best is not None else None

    def _explore(self, ct: Controller, pos: Position) -> None:
        """No ore in sight: fan out.  Each home builder gets a different
        quadrant bias from its serial so they do not all walk the same lane.
        """
        if self.home is None:
            return
        w, h = ct.get_map_width(), ct.get_map_height()
        corners = (
            Position(0, 0), Position(w - 1, 0),
            Position(0, h - 1), Position(w - 1, h - 1),
        )
        goal = corners[self.home_n % 4]
        if pos.distance_squared(goal) <= 4:
            goal = corners[(self.home_n + 1) % 4]
        self._step_toward(ct, pos, goal)

    # ------------------------------------------------------------------
    # movement
    # ------------------------------------------------------------------

    def _step_toward(self, ct: Controller, pos: Position, dst: Position) -> bool:
        """One cardinal step toward dst.  Builder bots may only move in the 4
        cardinal directions, so diagonals are never offered.

        Walls are handled by a committed detour rather than by re-deciding each
        round: grinding into the same wall corner is the failure mode that
        strands a raider halfway across the map.
        """
        dx = dst.x - pos.x
        dy = dst.y - pos.y
        if dx == 0 and dy == 0:
            return False

        if self.detour_left > 0 and self.detour is not None:
            self.detour_left -= 1
            try:
                if ct.can_move(self.detour):
                    ct.move(self.detour)
                    return True
            except GameError:
                pass
            self.detour_left = 0

        horiz = Direction.EAST if dx > 0 else Direction.WEST
        vert = Direction.SOUTH if dy > 0 else Direction.NORTH
        prefs = []
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

        for i, d in enumerate(prefs):
            try:
                if not ct.can_move(d):
                    continue
                ct.move(d)
            except GameError:
                continue
            # Committing to a sideways move only pays when the direct route is
            # blocked; a first-choice step needs no follow-through.
            if self.stuck >= 3 and i > 0:
                self.detour = d
                self.detour_left = 3
            return True
        return False

    # ==================================================================
    # LAUNCHER -- one job: throw raiders at the enemy Core
    # ==================================================================

    def _run_launcher(self, ct: Controller) -> None:
        if ct.get_action_cooldown() != 0:
            return
        self._locate(ct)
        if self.enemy is None:
            return

        req = unpack_pos(ct.read_store(SLOT_THROW_REQ))
        if req is None:
            return

        pos = ct.get_position()
        if pos.distance_squared(req) > LAUNCH_PICKUP_SQ:
            return

        my_team = ct.get_team()
        try:
            uid = ct.get_tile_builder_bot_id(req)
        except GameError:
            return
        if uid is None or uid in self.launched:
            return
        try:
            if ct.get_team(uid) != my_team:
                return
        except GameError:
            return

        goal = nearest_core_tile(pos, self.enemy)

        if self.throw_sites is None:
            # Every in-bounds tile the throw can reach, best-first.  Static for
            # this launcher's lifetime, so it is built exactly once.
            sites = []
            span = int(LAUNCH_RANGE_SQ ** 0.5) + 1
            for dx in range(-span, span + 1):
                for dy in range(-span, span + 1):
                    if dx * dx + dy * dy > LAUNCH_RANGE_SQ:
                        continue
                    tile = Position(pos.x + dx, pos.y + dy)
                    if self._in_bounds(ct, tile):
                        sites.append(tile)
            sites.sort(key=lambda t: (t.distance_squared(goal), t.x, t.y))
            self.throw_sites = sites

        current = req.distance_squared(goal)
        for site in self.throw_sites:
            # Sites are sorted best-first, so once they stop improving on where
            # the raider already stands, nothing further can help.
            if site.distance_squared(goal) >= current:
                break
            if site.distance_squared(req) < MIN_THROW_SQ:
                continue
            try:
                if not ct.can_launch(req, site):
                    continue
                ct.launch(req, site)
            except GameError:
                continue
            # Each builder is thrown exactly once.  Re-grabbing a delivered
            # raider is a tug-of-war the launcher always wins, and it is how a
            # siege gets ground down to nothing (measured on band_probe).
            self.launched.add(uid)
            ct.write_store(SLOT_THROW_REQ, 0)
            ct.write_store(SLOT_THROWN, ct.read_store(SLOT_THROWN) + 1)
            return

    # ==================================================================
    # TURRETS -- always the enemy Core if it is on the line
    # ==================================================================

    def _run_turret(self, ct: Controller) -> None:
        """get_attackable_tiles() enumerates row-major in absolute map
        coordinates, so a "first occupied tile wins" scan engages the farthest
        enemy for N/NE/NW/W facings and the nearest for the other four.  Targets
        are picked by distance_squared instead, never by enumeration order.
        """
        my_team = ct.get_team()
        pos = ct.get_position()
        best_core = None
        best_any = None

        try:
            tiles = ct.get_attackable_tiles()
        except GameError:
            return
        for tile in tiles:
            if not self._in_bounds(ct, tile):
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

        choice = best_core or best_any
        if choice is None:
            return
        try:
            if ct.can_fire(choice[1]):
                ct.fire(choice[1])
        except GameError:
            return
