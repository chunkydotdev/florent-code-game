"""band_probe -- a Banminary-style all-in launcher rush. INSTRUMENT, not a ladder bot.

Provenance: replay-extracted from the 1711-rated team "Banminary", platform match
82bc1754 game 1, which core-killed our live bot on round 42 (extracted 2026-08-06).
The shape of that opening is: one builder, one launcher, one throw, then two
Sentinels and a Gunner planted in the enemy Core's face -- no economy at all, no
defence, no second wave. Everything the team owns is titanium-for-ammunition.

This file exists so defensive changes can be gated against that pressure
repeatably. It is deliberately simple and deliberately fragile in strategy terms;
what it must NOT be is fragile in code terms -- an uncaught exception permanently
deletes the unit for the rest of the match, so every unit's turn body is wrapped
and every mutating call is gated by its can_*() predicate. (No try/finally
anywhere: the platform's bot-code validator rejects it.)

Deterministic: no random anywhere. Ties break on (distance, x, y).

Round budget from the source replay (25x15 map, 7-tile Core gap). These are
TARGETS ONLY -- every stage below triggers on state, never on a round number:

  r0        Core spawns ONE builder on the ring tile nearest the enemy;
            convert_ammo(30) immediately (action-free, so it costs no spawn)
  r1-r2     Stage A  -- builder plants a LAUNCHER one step toward the enemy and
                        stands adjacent to it, waiting
  r2-r4     Stage A+ -- launcher throws that builder as far toward the enemy
                        Core as can_launch permits (throw r^2 = 26)
  r5-r20    builder walks the remainder of the gap
  r20-r28   Stage B  -- Sentinel #1, aligned on an enemy Core tile (r^2 <= 32)
  r28-r36   Stage C  -- sidestep 3 tiles, Sentinel #2 from a second angle
  r36-r42   Stage D  -- Gunner as close to the Core as alignment allows (r^2<=13)
  r42       enemy Core dead in the source replay

Sentinels and Gunners fire single-tile-wide LINES, so a turret that is not on a
row / column / diagonal through an enemy Core tile can never hit the Core no
matter how close it is. Build sites are therefore chosen with can_fire_from()
against the four Core footprint tiles, not by proximity.

Communication store slots:
  0  SLOT_HOME          packed position of our own Core
  1  SLOT_ENEMY         packed position of the enemy Core, once directly sighted
  2  SLOT_RUSHER_PING   round the rush builder last confirmed it is alive
  3  SLOT_LAUNCHER_POS  packed position of the launcher, once built
  4  SLOT_SENTINELS     sentinels planted at the enemy Core
  5  SLOT_GUNNERS       gunners planted at the enemy Core
"""

import sys

from fcode import Controller, Direction, EntityType, GameError, Position

# --- store slots -----------------------------------------------------------
SLOT_HOME = 0
SLOT_ENEMY = 1
SLOT_RUSHER_PING = 2
SLOT_LAUNCHER_POS = 3
SLOT_SENTINELS = 4
SLOT_GUNNERS = 5

# --- tuning ----------------------------------------------------------------
# Opening conversion: 3 sentinel shots' worth, banked before a sentinel exists
# so the first one fires the round it is built.
OPENING_AMMO = 30
# Working ammunition buffer once any turret exists. This is a CEILING, not a
# budget: it is topped back up every round out of whatever titanium is not
# reserved for the remaining turret builds, so the whole 500 Ti bank drains
# into ammunition at exactly the rate the turrets burn it.
AMMO_CEILING = 90

SENTINEL_TARGET = 2
GUNNER_TARGET = 1

# Stage A' fallback: if the launcher is still unbuilt by this round (blocked
# terrain, no adjacent buildable tile), stop waiting and walk.
LAUNCHER_GIVEUP_RND = 12
# ...and if the launcher exists but never manages a throw, walk anyway.
LAUNCH_WAIT_MAX = 25

# The probe is all-in: no defensive posture, so no replacement builder unless
# the rush is genuinely dead and the game has run long enough to be worth one.
REPLACEMENT_MIN_ROUND = 50
RUSHER_STALE_ROUNDS = 3
MAX_BUILDERS = 2

SENTINEL_RANGE_SQ = 32   # sentinel vision/attack r^2
GUNNER_RANGE_SQ = 13     # gunner vision/attack r^2
LAUNCH_RANGE_SQ = 26     # launcher throw r^2, measured from the launcher
LAUNCH_PICKUP_SQ = 2     # launcher pickup r^2 (orthogonal + diagonal)
MIN_THROW_SQ = 4         # don't spend an action to move a builder one tile

# Stage C sidestep: how far laterally to shift before planting Sentinel #2, so
# the two lines come in on different angles and one blocker cannot eat both.
LATERAL_OFFSET = 3
REPOSITION_MAX_RNDS = 12

# Repairing the forward turrets is not economy and it is what turns the trickle
# of passive income into damage over a long match: 1 Ti buys +4 HP, versus the
# 0.18 damage that same titanium buys as ammunition. The Core protects a small
# repair float from the ammo converter so the builder is never broke.
HEAL_RESERVE = 12
HEAL_MIN_TITANIUM = 4

# Bail at a phase boundary rather than let the engine truncate a statement.
CPU_BUDGET_US = 7000

CARDINALS = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)


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


class Player:
    def __init__(self):
        # Shared / derived map knowledge (one Player instance per unit).
        self.home: Position | None = None
        self.enemy: Position | None = None
        self.enemy_confirmed = False

        # Core state
        self.spawned = 0
        self.opening_ammo_done = False

        # Builder state
        self.prev_pos: Position | None = None
        self.stuck = 0
        self.delivered = False          # thrown, or otherwise past the waiting phase
        self.launcher_pos: Position | None = None
        self.wait_start: int | None = None
        self.built_sentinels = 0
        self.built_gunners = 0
        self.reposition_target: Position | None = None
        self.reposition_start = 0

        # Launcher state
        self.throw_sites: list[Position] | None = None
        self.launched: set = set()

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
        elif etype == EntityType.LAUNCHER:
            self._run_launcher(ct)
        elif etype == EntityType.SENTINEL or etype == EntityType.GUNNER:
            self._run_turret(ct)

    def _cpu_exhausted(self, ct: Controller) -> bool:
        return ct.get_cpu_time_elapsed() >= CPU_BUDGET_US

    # ------------------------------------------------------------------
    # map knowledge
    # ------------------------------------------------------------------

    def _locate(self, ct: Controller) -> None:
        """Establish home and enemy Core positions as cheaply as possible.

        1. Sight them directly if they are in vision (a freshly spawned builder
           is always next to home; a forward turret always sees the enemy Core).
        2. Otherwise read whatever the store already knows.
        3. Otherwise derive the enemy anchor by symmetry from home: every map in
           the pool is rotational, so for our Core's NW corner (x, y) on a WxH
           map the enemy's NW corner is (W-2-x, H-2-y).
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
    # Core
    # ------------------------------------------------------------------

    def _run_core(self, ct: Controller) -> None:
        """One builder, then titanium into ammunition forever.

        convert_ammo() does not consume the action cooldown, so converting never
        costs a spawn -- it is always tried first.
        """
        pos = ct.get_position()
        if self.home is None:
            self.home = pos
            ct.write_store(SLOT_HOME, pack_pos(pos))
        self._locate(ct)

        rnd = ct.get_current_round()
        sentinels = ct.read_store(SLOT_SENTINELS)
        gunners = ct.read_store(SLOT_GUNNERS)

        # Titanium held back for builds still owed. Ammunition must never
        # out-compete the siege it is meant to feed -- but every titanium held
        # back past the last build is a sentinel shot the siege never fires, so
        # the reserve has to fall to zero the moment the plan is complete.
        # (Measured 2026-08-06: an unconditional builder+launcher reserve pinned
        # 95 Ti = ~9 sentinel shots = ~170 damage out of the game forever, and
        # left enemy Cores sitting at single-digit HP for 800 rounds.)
        ping = ct.read_store(SLOT_RUSHER_PING)
        rusher_stale = rnd - ping > RUSHER_STALE_ROUNDS
        reserve = 0
        if sentinels < SENTINEL_TARGET:
            reserve += (SENTINEL_TARGET - sentinels) * ct.get_sentinel_cost()
        if gunners < GUNNER_TARGET:
            reserve += (GUNNER_TARGET - gunners) * ct.get_gunner_cost()
        if self.spawned == 0:
            reserve += ct.get_builder_bot_cost() + ct.get_launcher_cost()
        elif self.spawned < MAX_BUILDERS and rusher_stale:
            reserve += ct.get_builder_bot_cost()
        if sentinels + gunners > 0:
            # A standing turret repaired for 1 Ti (+4 HP) is worth far more than
            # the single point of ammunition that titanium would have become.
            reserve += HEAL_RESERVE

        if not self.opening_ammo_done:
            if ct.can_convert_ammo(OPENING_AMMO):
                ct.convert_ammo(OPENING_AMMO)
                self.opening_ammo_done = True
        elif sentinels + gunners > 0:
            ammo = ct.get_global_ammo()
            if ammo < AMMO_CEILING:
                spare = ct.get_global_resources() - reserve
                amount = min(AMMO_CEILING - ammo, spare)
                if amount > 0 and ct.can_convert_ammo(amount):
                    ct.convert_ammo(amount)

        if ct.get_action_cooldown() != 0:
            return

        if self.spawned >= MAX_BUILDERS:
            return
        if self.spawned > 0:
            # Only ever one replacement, and only once the rush is really dead
            # and the match has run long enough that a fresh walker still has
            # time to matter. A probe has no use for a defensive builder.
            if rnd < REPLACEMENT_MIN_ROUND or not rusher_stale:
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

    # ------------------------------------------------------------------
    # Builder bot -- the single rusher
    # ------------------------------------------------------------------

    def _run_builder(self, ct: Controller) -> None:
        rnd = ct.get_current_round()
        pos = ct.get_position()
        ct.write_store(SLOT_RUSHER_PING, rnd)
        self._locate(ct)

        # A position change of more than one step can only have come from a
        # launcher throw -- that, not a round number, is what ends the wait.
        if self.prev_pos is not None:
            if pos == self.prev_pos:
                self.stuck += 1
            else:
                self.stuck = 0
                if pos.distance_squared(self.prev_pos) > 2:
                    self.delivered = True
        self.prev_pos = pos

        if self.enemy is not None and self.home is not None:
            if pos.distance_squared(self.enemy) < pos.distance_squared(self.home):
                self.delivered = True

        if self.launcher_pos is None:
            self.launcher_pos = unpack_pos(ct.read_store(SLOT_LAUNCHER_POS))
            if self.launcher_pos is not None and self.wait_start is None:
                self.wait_start = rnd

        if self._cpu_exhausted(ct):
            return

        if ct.get_action_cooldown() == 0:
            if self._stage_a(ct, rnd):
                return
            if not self._stage_bcd(ct, rnd):
                self._try_heal(ct)

        if self._cpu_exhausted(ct):
            return
        self._advance(ct, rnd)

    # -- Stage A: plant the launcher, then stand next to it -------------

    def _stage_a(self, ct: Controller, rnd: int) -> bool:
        """Build the launcher on the adjacent tile nearest the enemy. Returns
        True if it acted (or the launcher is this builder's business this turn).
        """
        if self.delivered or self.launcher_pos is not None:
            return False
        if rnd > LAUNCHER_GIVEUP_RND:
            self.delivered = True  # Stage A' fallback: walk the whole way
            return False
        if ct.get_global_resources() < ct.get_launcher_cost():
            return False
        if self.enemy is None:
            return False

        pos = ct.get_position()
        best = None
        for d in CARDINALS:
            tile = pos.add(d)
            if not in_bounds(ct, tile):
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

        ct.build_launcher(best[1])
        self.launcher_pos = best[1]
        self.wait_start = rnd
        ct.write_store(SLOT_LAUNCHER_POS, pack_pos(best[1]))
        return True

    # -- Stages B/C/D: the forward turrets ------------------------------

    def _stage_bcd(self, ct: Controller, rnd: int) -> bool:
        if not self.delivered or self.enemy is None:
            return False
        if self.reposition_target is not None:
            return False  # Stage C sidestep first, build after

        sentinels = max(self.built_sentinels, ct.read_store(SLOT_SENTINELS))
        gunners = max(self.built_gunners, ct.read_store(SLOT_GUNNERS))

        if sentinels < SENTINEL_TARGET:
            if self._plant_turret(ct, EntityType.SENTINEL, SENTINEL_RANGE_SQ):
                self.built_sentinels = sentinels + 1
                ct.write_store(SLOT_SENTINELS, self.built_sentinels)
                if self.built_sentinels < SENTINEL_TARGET:
                    self._set_lateral_target(ct, rnd)
                return True
            return False

        if gunners < GUNNER_TARGET:
            if self._plant_turret(ct, EntityType.GUNNER, GUNNER_RANGE_SQ):
                self.built_gunners = gunners + 1
                ct.write_store(SLOT_GUNNERS, self.built_gunners)
                return True
        return False

    def _plant_turret(self, ct: Controller, etype: EntityType, range_sq: int) -> bool:
        """Build a turret on an orthogonally adjacent tile from which it can
        actually hit an enemy Core tile.

        Both turrets fire a single-tile-wide line, so proximity is worthless
        without alignment: the site is chosen by asking can_fire_from() for the
        hypothetical turret against each of the four Core footprint tiles, and
        the nearest legal (site, facing) pair wins.
        """
        cost = ct.get_sentinel_cost() if etype == EntityType.SENTINEL else ct.get_gunner_cost()
        if ct.get_global_resources() < cost:
            return False

        pos = ct.get_position()
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

    def _set_lateral_target(self, ct: Controller, rnd: int) -> None:
        """Stage C: shift a few tiles off the approach axis so Sentinel #2 comes
        in on a different line from Sentinel #1.
        """
        pos = ct.get_position()
        tile = nearest_core_tile(pos, self.enemy)
        dx = tile.x - pos.x
        dy = tile.y - pos.y
        # Shorter offsets are tried too: on a small map a full 3-tile sidestep
        # can walk the builder clean out of Sentinel range of the Core, and a
        # second angle is worthless if it cannot reach the target from there.
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

    def _try_heal(self, ct: Controller) -> bool:
        """Repair the forward turrets with titanium the ammo ceiling cannot use.
        Never economy, never a trip home.
        """
        if ct.get_global_resources() < HEAL_MIN_TITANIUM:
            return False
        pos = ct.get_position()
        for d in CARDINALS:
            tile = pos.add(d)
            if not in_bounds(ct, tile):
                continue
            try:
                bid = ct.get_tile_building_id(tile)
                if bid is None or ct.get_team(bid) != ct.get_team():
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

    # -- movement -------------------------------------------------------

    def _advance(self, ct: Controller, rnd: int) -> None:
        if ct.get_move_cooldown() != 0:
            return
        pos = ct.get_position()

        # Waiting to be thrown: stay inside the launcher's pickup ring.
        if not self.delivered and self.launcher_pos is not None:
            waited = rnd - (self.wait_start if self.wait_start is not None else rnd)
            if waited > LAUNCH_WAIT_MAX:
                self.delivered = True
            elif pos.distance_squared(self.launcher_pos) <= LAUNCH_PICKUP_SQ:
                return  # in range -- hold still
            else:
                self._step_toward(ct, self.launcher_pos)
                return

        if not self.delivered and self.launcher_pos is None and rnd <= LAUNCHER_GIVEUP_RND:
            return  # still trying to afford/place the launcher; don't wander off

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

        # With the siege planted there is nothing left to build, so the builder's
        # remaining value is keeping the turrets standing. Park next to whichever
        # forward turret is hurt; otherwise keep pressing the enemy Core, which
        # also parks a body in its spawn ring.
        hurt = self._damaged_turret(ct)
        if hurt is not None:
            if pos.distance_squared(hurt) > 1:
                self._step_toward(ct, hurt)
                return
            return
        if self.enemy is not None:
            self._step_toward(ct, nearest_core_tile(pos, self.enemy))

    def _damaged_turret(self, ct: Controller) -> Position | None:
        """Nearest visible friendly turret below full HP, if any."""
        if self.built_sentinels + self.built_gunners == 0:
            return None
        my_team = ct.get_team()
        pos = ct.get_position()
        best = None
        try:
            nearby = ct.get_nearby_buildings()
        except GameError:
            return None
        for bid in nearby:
            try:
                if ct.get_team(bid) != my_team:
                    continue
                if ct.get_entity_type(bid) not in (EntityType.SENTINEL, EntityType.GUNNER):
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

    def _step_toward(self, ct: Controller, dst: Position) -> bool:
        """One cardinal step toward dst; if the preferred axis is blocked, try
        the other one, then the perpendiculars, then backwards. Deterministic.
        """
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

    # ------------------------------------------------------------------
    # Launcher -- one job: throw our builder at the enemy Core
    # ------------------------------------------------------------------

    def _run_launcher(self, ct: Controller) -> None:
        if ct.get_action_cooldown() != 0:
            return
        self._locate(ct)
        if self.enemy is None:
            return

        pos = ct.get_position()
        goal = nearest_core_tile(pos, self.enemy)

        if self.throw_sites is None:
            # Every in-bounds tile the throw can reach, best-first. Static for
            # this launcher's lifetime, so it is built exactly once.
            sites = []
            span = int(LAUNCH_RANGE_SQ ** 0.5) + 1
            for dx in range(-span, span + 1):
                for dy in range(-span, span + 1):
                    if dx * dx + dy * dy > LAUNCH_RANGE_SQ:
                        continue
                    tile = Position(pos.x + dx, pos.y + dy)
                    if in_bounds(ct, tile):
                        sites.append(tile)
            sites.sort(key=lambda t: (t.distance_squared(goal), t.x, t.y))
            self.throw_sites = sites

        my_team = ct.get_team()
        try:
            nearby = ct.get_nearby_units(dist_sq=LAUNCH_PICKUP_SQ)
        except GameError:
            return
        for uid in nearby:
            try:
                if ct.get_entity_type(uid) != EntityType.BUILDER_BOT:
                    continue
                if ct.get_team(uid) != my_team:
                    continue
                bot_pos = ct.get_position(uid)
            except GameError:
                continue
            # Each builder is thrown exactly once. Re-grabbing one that has
            # already been delivered is a tug-of-war the launcher always wins:
            # measured on fjordgate, a builder repositioning for Stage C walked
            # back into the pickup ring and was re-thrown every single round
            # from r5 to r170, so Sentinel #2 was never built and the siege was
            # ground down. The recipe says the launcher's job ends at the throw.
            if uid in self.launched:
                continue
            current = bot_pos.distance_squared(goal)
            for site in self.throw_sites:
                # Sites are sorted best-first, so once they stop improving on
                # where the bot already stands, nothing further can help.
                if site.distance_squared(goal) >= current:
                    break
                # A one-tile hop is not worth an action -- the bot walks that.
                if site.distance_squared(bot_pos) < MIN_THROW_SQ:
                    continue
                try:
                    if not ct.can_launch(bot_pos, site):
                        continue
                except GameError:
                    continue
                ct.launch(bot_pos, site)
                self.launched.add(uid)
                return

    # ------------------------------------------------------------------
    # Turrets -- always the enemy Core if it is on the line
    # ------------------------------------------------------------------

    def _run_turret(self, ct: Controller) -> None:
        """Fire at an enemy Core tile whenever one is on the line, otherwise the
        nearest enemy anything.

        get_attackable_tiles() enumerates row-major in absolute map coordinates,
        so a "first occupied tile wins" scan engages the farthest enemy for
        N/NE/NW/W facings and the nearest for the other four. Targets are picked
        by distance_squared instead, never by enumeration order.
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

        choice = best_core or best_any
        if choice is None:
            return
        try:
            if ct.can_fire(choice[1]):
                ct.fire(choice[1])
        except GameError:
            return
