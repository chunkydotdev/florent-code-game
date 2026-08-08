"""clanker_probe -- team Clankers' HEAL-TANK SIEGE, frozen as an instrument.

Provenance: `docs/research/clankers-noconfound-2026-08-07.md` section 0.4, the
no-confound corpus (10 games / 2 ladder matches, Clankers v1 in both seats,
neither match containing an OpenSverige bot).  Every item below is measured in
>= 8 of those 10 games.  Class label from section 0.5:

    HEAL-TANK SIEGE -- a standing early forward-sentinel siege carried on a
    proportional heal controller, with a reactive counterbattery gunner and an
    income-gated launcher-ejection ring.  Co-labels: conveyor-first econ,
    no-tiebreak.

The eight spec items this file reproduces:

  1. Opening -- 5 builder bots, one per round, r0-r4, on core-adjacent tiles.
  2. Standing forward sentinel -- the first builder walks to a passable tile at
     d^2 16-25 from the ENEMY core and builds a sentinel FACING it as soon as
     30 Ti allows.  Proactive: it precedes any enemy turret.  Timing is
     walk-distance-gated, never schedule-gated.
  3. Proportional heal controller (the class signature) -- each idle builder
     heals the most-damaged friendly asset on an orthogonally adjacent tile;
     the aggregate heal rate tracks incoming damage (4 HP per 1 Ti), capped by
     the titanium budget.  Priority: core >= turret > conveyor.
  4. Reactive counterbattery gunner -- ONLY when an enemy turret is in vision:
     build a gunner at d^2 <= 2 of it, facing it, and fire until it is dead.
     NEVER a gunner when no enemy turret exists.  Never rotate.
  5. Income-gated launcher ring -- 1-3 launchers at d^2 4-17 from our OWN core,
     built r11-r65 when titanium allows; throw any adjacent enemy builder to a
     passable tile FURTHER from our own core.  Suppressed entirely below 50 Ti.
  6. Ammo drip -- one 30 Ti conversion timed to the first turret coming online,
     then 4-10 Ti every 1-2 rounds, holding the balance between 4 and 40.
  7. Conveyor-first economy router -- the chain is laid from the core OUTWARD,
     the terminal conveyor goes orthogonally adjacent to the ore tile FACING
     BACK TOWARD THE CORE, and only then is the harvester placed on the ore.

=====================================================================
  8. THE DEFECTS BELOW ARE DELIBERATE.  DO NOT "FIX" THEM.
=====================================================================
  This probe builds NO BARRIERS and NO SPLITTERS, has NO TIEBREAK/ENDGAME
  LOGIC, and its AMMO DRIP OUTBIDS HARVESTER PURCHASES (the drip runs in the
  Core's turn, before any builder can spend, and reserves nothing for the
  economy).  These are the measured exploit surface of the Clankers class --
  watch items 5, 6 and 8 of the no-confound read -- and they are the entire
  reason the probe exists.  Repairing any of them destroys the instrument and
  silently invalidates every verdict taken against it.
=====================================================================

INSTRUMENT, NOT A LADDER BOT.  Fidelity to the decoded pattern beats strength.
What it must NOT be is fragile in code terms -- an uncaught exception
permanently deletes the unit for the rest of the match, so every unit's turn
body is wrapped and every mutating call is gated by its can_*() predicate.
(No try/finally anywhere: the platform's bot-code validator rejects it.)

Deterministic: no random anywhere, no dict/set iteration order load-bearing --
every candidate list is sorted on an explicit key before a pick, ties on
(x, y) or on entity id.  Byte-identical replays across repeat runs of the same
(map, seed, seat).

Seat-general.  The enemy core is taken from a direct sighting when one exists
and from point symmetry (W-2-x, H-2-y) otherwise; every site is expressed
relative to a core, never as an absolute coordinate.

Communication store slots:
   0  SLOT_HOME        packed position of our own Core
   1  SLOT_ENEMY       packed position of the enemy Core, once sighted
   2  SLOT_ROLE_NEXT   builder role claim counter
   3  SLOT_FWD_ID      entity id of the builder holding forward-sentinel duty
   4  SLOT_FWD_PING    round+1 that the forward owner last reported alive
   5  SLOT_SENT_ALIVE  round+1 that the forward sentinel last acted
   6  SLOT_SENTINELS   forward sentinels built
   7  SLOT_GUNNERS     counterbattery gunners built
   8  SLOT_LAUNCHERS   launchers built
   9  SLOT_CB_LATCH    counterbattery duty: owner id and ping, packed
  10  SLOT_MEDICS      medics the heal controller is currently asking for
  11..15               builder liveness beats, indexed by role % 5
"""

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
SLOT_FWD_ID = 3
SLOT_FWD_PING = 4
SLOT_SENT_ALIVE = 5
SLOT_SENTINELS = 6
SLOT_GUNNERS = 7
SLOT_LAUNCHERS = 8
SLOT_CB_LATCH = 9
SLOT_MEDICS = 10
SLOT_BEAT_0 = 11
BEAT_SLOTS = 5
# One store int carries both the counterbattery owner's entity id and the
# round it last reported in: id * LATCH_MOD + round.  Rounds cap at 1000, so
# LATCH_MOD > 1000 keeps the two fields from colliding for a whole match.
LATCH_MOD = 1024

# --- item 1: the opening ---------------------------------------------------
# 5 builder bots, one per round, r0-r4, on core-adjacent tiles (10/10 games).
OPENING_BUILDERS = 5
OPENING_LAST_ROUND = 4
# The spec is silent on replacement, but a heal controller with no builders is
# not the class signature at all -- losses are replaced back up to the opening
# five, one per round, out of surplus only.  See the report: this is the one
# addition to item 1.
MAX_SPAWNS = 26
REPLACE_FLOAT = 30
BEAT_STALE = 2

# --- item 2: the standing forward sentinel ---------------------------------
SENT_BAND_LO = 16
SENT_BAND_HI = 25
# Offsets from an enemy-core footprint tile that are BOTH inside the measured
# d^2 band and exactly on a sentinel firing ray (the ray is a single tile wide,
# so a site that is not ray-aligned with a footprint tile can never hit the
# core).  d^2: 16, 25 on the cardinals; 18 on the diagonals.
SENT_OFFSETS = (
    (0, -4), (0, 4), (-4, 0), (4, 0),
    (-3, -3), (-3, 3), (3, -3), (3, 3),
    (0, -5), (0, 5), (-5, 0), (5, 0),
)
# Used only when the band is geometrically empty (core in a map corner, walls).
# Still ray-aligned and still inside the sentinel's r^2=32 reach.
SENT_FALLBACK_OFFSETS = (
    (-4, -4), (-4, 4), (4, -4), (4, 4),
    (0, -3), (0, 3), (-3, 0), (3, 0),
    (-2, -2), (-2, 2), (2, -2), (2, 2),
)
MAX_SENTINELS = 4
SENT_BUILD_GRACE = 4
SENT_BEAT_STALE = 3

# --- item 4: the reactive counterbattery gunner ----------------------------
# Strict reading of watch item 1: no enemy turret in vision, no gunner, ever.
CB_SITE_SQ = 2       # 17/18 wild gunners sat at d^2 <= 2 of the turret
CB_COVER_SQ = 8      # one gunner per turret; this is "already answered"
MAX_GUNNERS = 6      # wild rate is 18 gunners across 10 games
# The wild bot answers with ONE builder.  Without this latch every builder in
# vision of a turret abandons its post to chase it, which against a turret-heavy
# opponent converts the whole pool into counterbattery and zeroes the economy --
# measured on lighthouse: 5 builders, 17 enemy gunners, 0 harvesters all game.
CB_LATCH_STALE = 3

# --- item 5: the income-gated launcher ring --------------------------------
MAX_LAUNCHERS = 3
LAUNCH_FIRST = 11
LAUNCH_LAST = 65
LAUNCH_GAP = 18      # due at r11 / r29 / r47, all inside the measured window
LAUNCH_MIN_TI = 50   # "suppress entirely when Ti < ~50"
LAUNCH_BAND_LO = 4
LAUNCH_BAND_HI = 17
LAUNCH_SEAT = 1
LAUNCH_THROW_SQ = 26
LAUNCH_TRIES = 12
LAUNCH_CANDIDATES = 10

# --- item 6: the ammo drip -------------------------------------------------
FIRST_CONVERSION = 30
AMMO_URGENT = 12
AMMO_HOLD_MAX = 40
DRIP_SMALL = 4
DRIP_BIG = 10
DRIP_GAP = 2
# The float the Core leaves behind after a drip.  It is small on purpose: this
# is the mechanism by which the drip outbids the 20 Ti harvester (item 8).
DRIP_RESERVE = 2

# --- item 3: the proportional heal controller ------------------------------
HEAL_HP = 4          # +4 HP for 1 Ti
HEAL_COST = 1
MAX_MEDICS = 4
HEAL_RANK_CORE = 0
HEAL_RANK_TURRET = 1
HEAL_RANK_ECON = 2
HEAL_RANK_BOT = 3

# --- item 7: the conveyor-first router -------------------------------------
MAX_ROUTE = 12
# How long a builder will sit on a finished terminal waiting for 20 Ti before
# giving up and routing somewhere else.  This is what produces the measured
# "6 terminals, 0 harvesters, 0 delivered" failure -- it is a defect, not a
# bug (watch item 7).
HARVEST_PATIENCE = 40
# Expansion stops when the team-wide cost scale has priced harvesters out,
# which is the same brake the wild bot's harvester count flattens against.
HARVESTER_COST_CEILING = 200

CARDINALS = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)
TURRET_TYPES = (EntityType.GUNNER, EntityType.SENTINEL, EntityType.LAUNCHER)
ECONOMY_TYPES = (
    EntityType.HARVESTER,
    EntityType.CONVEYOR,
    EntityType.SPLITTER,
    EntityType.BARRIER,
)


def pack_pos(pos: Position) -> int:
    """Encode a position into one store int, offset so (0,0) is not 'empty'."""
    return ((pos.x + 1) << 16) | (pos.y + 1)


def unpack_pos(val: int) -> Position | None:
    if val <= 0:
        return None
    return Position((val >> 16) - 1, (val & 0xFFFF) - 1)


def in_bounds(ct: Controller, pos: Position) -> bool:
    """On the map.  Necessary but not sufficient before a tile query -- the
    tile getters also raise GameError for in-bounds tiles outside vision.
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


def core_dist_sq(pos: Position, core_nw: Position) -> int:
    """d^2 from pos to the NEAREST tile of a Core footprint."""
    return min(pos.distance_squared(t) for t in core_footprint(core_nw))


def nearest_core_tile(pos: Position, core_nw: Position) -> Position:
    return min(
        core_footprint(core_nw),
        key=lambda t: (pos.distance_squared(t), t.x, t.y),
    )


def adjacent_core_tile(pos: Position, core_nw: Position) -> Position | None:
    """The Core footprint tile orthogonally adjacent to pos, if any."""
    for tile in core_footprint(core_nw):
        if abs(tile.x - pos.x) + abs(tile.y - pos.y) == 1:
            return tile
    return None


def core_port_ring(core_nw: Position) -> list[Position]:
    """The 8 tiles orthogonally adjacent to a Core footprint -- the only tiles
    a conveyor can occupy and still deliver straight into the Core.
    """
    ring = []
    for tile in core_footprint(core_nw):
        for d in CARDINALS:
            cand = tile.add(d)
            if abs(cand.x - core_nw.x) <= 1 and abs(cand.y - core_nw.y) <= 1:
                continue  # still on the footprint
            ring.append(cand)
    ring.sort(key=lambda p: (p.x, p.y))
    return ring


def manhattan(a: Position, b: Position) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def exact_facing(src: Position, dst: Position) -> Direction | None:
    """The Direction whose ray from src passes exactly through dst, or None.

    A turret ray is a single tile wide, so "roughly toward" is not good enough:
    only a shared row, a shared column or a true diagonal can ever hit.
    """
    dx = dst.x - src.x
    dy = dst.y - src.y
    if dx == 0 and dy == 0:
        return None
    if dx == 0:
        return Direction.SOUTH if dy > 0 else Direction.NORTH
    if dy == 0:
        return Direction.EAST if dx > 0 else Direction.WEST
    if abs(dx) != abs(dy):
        return None
    if dx > 0:
        return Direction.SOUTHEAST if dy > 0 else Direction.NORTHEAST
    return Direction.SOUTHWEST if dy > 0 else Direction.NORTHWEST


class Player:
    def __init__(self):
        # Shared / derived map knowledge (one Player instance per unit).
        self.home: Position | None = None
        self.enemy: Position | None = None
        self.enemy_confirmed = False

        # Core state
        self.spawned = 0
        self.first_conversion = False
        self.last_drip = -99

        # Builder state
        self.role: int | None = None
        self.seat = 0
        self.is_forward = False
        self.prev_pos: Position | None = None
        self.stuck = 0
        self.recent: list = []
        self.known_ore: set = set()
        self.explore_idx = 0

        # Builder -- forward sentinel duty
        self.sent_site: Position | None = None
        self.sent_facing: Direction | None = None
        self.sent_built_round: int | None = None

        # Builder -- launcher duty
        self.launch_sites: list | None = None
        self.launch_idx = 0

        # Builder -- conveyor-first router
        self.stage = "pick"
        self.ore_target: Position | None = None
        self.port: Position | None = None
        self.route_prev: Position | None = None
        self.route_pending: Position | None = None
        self.terminal: Position | None = None
        self.chain_len = 0
        self.wait = 0

    # ------------------------------------------------------------------
    # entry point
    # ------------------------------------------------------------------

    def run(self, ct: Controller) -> None:
        """An exception escaping run() permanently deletes this unit, so the
        guard is unconditional.  Never a try/finally -- the validator rejects
        it.  Silent by construction: this file is a battery instrument and must
        not write to stdout (captured into the replay) or stderr.
        """
        try:
            self._dispatch(ct)
        except Exception:
            return

    def _dispatch(self, ct: Controller) -> None:
        etype = ct.get_entity_type()
        if etype == EntityType.CORE:
            self._run_core(ct)
        elif etype == EntityType.BUILDER_BOT:
            self._run_builder(ct)
        elif etype == EntityType.SENTINEL:
            self._run_sentinel(ct)
        elif etype == EntityType.GUNNER:
            self._run_gunner(ct)
        elif etype == EntityType.LAUNCHER:
            self._run_launcher(ct)

    # ------------------------------------------------------------------
    # shared map / intel
    # ------------------------------------------------------------------

    def _locate(self, ct: Controller) -> None:
        """Establish home and enemy Core positions as cheaply as possible."""
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
        pos = ct.get_position()
        if self.home is None:
            self.home = pos
            ct.write_store(SLOT_HOME, pack_pos(pos))
        self._locate(ct)
        rnd = ct.get_current_round()

        # ITEM 3: the demand side of the proportional heal controller.
        self._publish_heal_demand(ct)

        # ITEM 6 + ITEM 8: the drip runs FIRST, in the Core's turn, before any
        # builder gets to spend a titanium.  That ordering is the defect --
        # a 20 Ti harvester loses to a 4 Ti conversion every single round.
        self._ammo_drip(ct, rnd)

        if ct.get_action_cooldown() != 0:
            return
        self._spawn(ct, rnd)

    def _publish_heal_demand(self, ct: Controller) -> None:
        """Medics wanted = ceil(core HP deficit / 4), capped.

        A pure proportional controller on the deficit: at steady state the
        number of healing builders settles exactly where 4 HP x medics equals
        the incoming damage rate, which is the measured signature (core heal
        rate tracks core damage rate to within 2% in all 7 games their core
        lived).  Deliberately NOT a derivative controller -- the wild bot's
        heal rate lags a damage spike by a round or two, and so does this.
        """
        try:
            hp = ct.get_hp()
            mx = ct.get_max_hp()
        except GameError:
            return
        deficit = mx - hp
        if deficit <= 0:
            want = 0
        else:
            want = (deficit + HEAL_HP - 1) // HEAL_HP
            if want > MAX_MEDICS:
                want = MAX_MEDICS
        ct.write_store(SLOT_MEDICS, want)

    def _ammo_drip(self, ct: Controller, rnd: int) -> None:
        """ITEM 6.  One 30 Ti conversion when the first ammo-burning turret
        comes online, then 4-10 Ti every 1-2 rounds, holding the balance in
        4-40.  convert_ammo() does not consume the action cooldown, so this
        never costs a spawn.
        """
        online = ct.read_store(SLOT_SENTINELS) + ct.read_store(SLOT_GUNNERS)
        if online <= 0:
            return

        titanium = ct.get_global_resources()
        if not self.first_conversion:
            amount = min(FIRST_CONVERSION, titanium)
            if amount > 0 and ct.can_convert_ammo(amount):
                ct.convert_ammo(amount)
                self.first_conversion = True
                self.last_drip = rnd
            return

        ammo = ct.get_global_ammo()
        if ammo >= AMMO_HOLD_MAX:
            return
        gap = 1 if ammo < AMMO_URGENT else DRIP_GAP
        if rnd - self.last_drip < gap:
            return
        chunk = DRIP_BIG if ammo < AMMO_URGENT else DRIP_SMALL
        amount = min(chunk, AMMO_HOLD_MAX - ammo, titanium - DRIP_RESERVE)
        if amount > 0 and ct.can_convert_ammo(amount):
            ct.convert_ammo(amount)
            self.last_drip = rnd

    def _live_builders(self, ct: Controller, rnd: int) -> int:
        live = 0
        for i in range(BEAT_SLOTS):
            beat = ct.read_store(SLOT_BEAT_0 + i)
            if beat > 0 and rnd - (beat - 1) <= BEAT_STALE:
                live += 1
        return live

    def _spawn(self, ct: Controller, rnd: int) -> None:
        """ITEM 1.  One builder per round on r0-r4, then replacement only."""
        if self.spawned >= MAX_SPAWNS:
            return
        if rnd <= OPENING_LAST_ROUND:
            if self.spawned >= OPENING_BUILDERS or self.spawned > rnd:
                return
            if ct.get_global_resources() < ct.get_builder_bot_cost():
                return
        else:
            if self._live_builders(ct, rnd) >= OPENING_BUILDERS:
                return
            need = ct.get_builder_bot_cost() + REPLACE_FLOAT
            if ct.get_global_resources() < need:
                return

        # The whole 12-tile ring, enumerated via get_nearby_tiles(8) and
        # filtered by can_spawn() -- never pos.add(d), which only reaches the
        # N/W half of the ring and decides whole maps by seat.
        pos = ct.get_position()
        anchor = self.enemy if self.enemy is not None else pos
        best = None
        try:
            tiles = ct.get_nearby_tiles(dist_sq=8)
        except GameError:
            return
        for tile in tiles:
            try:
                if not ct.can_spawn(tile):
                    continue
            except GameError:
                continue
            key = (tile.distance_squared(anchor), tile.x, tile.y)
            if best is None or key < best[0]:
                best = (key, tile)
        if best is not None:
            try:
                ct.spawn_builder(best[1])
                self.spawned += 1
            except GameError:
                return

    # ------------------------------------------------------------------
    # Builder bot
    # ------------------------------------------------------------------

    def _run_builder(self, ct: Controller) -> None:
        rnd = ct.get_current_round()
        pos = ct.get_position()
        self._locate(ct)

        if self.role is None:
            # At most one builder is spawned per round (the Core's action
            # cooldown guarantees it) and store writes land next round, so a
            # plain claim counter cannot hand the same index to two builders.
            nxt = ct.read_store(SLOT_ROLE_NEXT)
            self.role = nxt if nxt > 0 else 1
            ct.write_store(SLOT_ROLE_NEXT, self.role + 1)
            self.role -= 1
            self.seat = self.role % BEAT_SLOTS
        ct.write_store(SLOT_BEAT_0 + self.seat, rnd + 1)

        if self.prev_pos is not None:
            if pos == self.prev_pos:
                self.stuck += 1
            else:
                self.stuck = 0
        self.prev_pos = pos
        # Short tabu list.  Without it a builder that meets a blocker on its
        # preferred axis steps aside, finds the axis clear from the new tile,
        # steps back, and 2-cycles there for the rest of the match.
        self.recent.append((pos.x, pos.y))
        if len(self.recent) > 4:
            self.recent.pop(0)

        self._forward_latch(ct, rnd)

        # ITEM 5 first, because it is the only duty here with a deadline: the
        # ring is time-boxed to r11-r65 and fires for one seat, when due and
        # solvent.  Behind counterbattery it never fires at all against a
        # turret-heavy opponent -- measured, 0 launchers on lighthouse/eider.
        if self._launcher_duty(ct, rnd, pos):
            return
        # ITEM 4 is reactive and outranks the rest for the ONE builder holding
        # counterbattery duty: a turret that is already shooting is the only
        # thing the wild bot ever interrupts itself for.
        if self._counterbattery(ct, rnd, pos):
            return
        # ITEM 3: medic duty, sized by the controller's published demand.
        if self._medic_duty(ct, pos):
            return
        if self.is_forward:
            self._run_forward(ct, rnd, pos)
            return
        # ITEM 7.
        self._run_eco(ct, rnd, pos)

    def _forward_latch(self, ct: Controller, rnd: int) -> None:
        """Exactly one live builder owns forward-sentinel duty at a time.

        The owner republishes a heartbeat every round; when it dies and the
        heartbeat goes stale any builder may claim the slot.  Several may claim
        on the same round -- store writes are last-writer-wins, so exactly one
        value lands and exactly one builder reads its own id back next round.
        """
        my_id = ct.get_id()
        owner = ct.read_store(SLOT_FWD_ID)
        ping = ct.read_store(SLOT_FWD_PING)

        if owner == my_id:
            self.is_forward = True
            ct.write_store(SLOT_FWD_PING, rnd + 1)
            return

        self.is_forward = False
        if ping == 0 or rnd - (ping - 1) > 3:
            ct.write_store(SLOT_FWD_ID, my_id)
            ct.write_store(SLOT_FWD_PING, rnd + 1)

    # -- item 4: reactive counterbattery ---------------------------------

    def _counterbattery(self, ct: Controller, rnd: int, pos: Position) -> bool:
        """A gunner at d^2 <= 2 of an enemy turret, facing it -- and ONLY when
        such a turret is in this builder's vision right now.  The strict form
        of watch item 1: 0 of 18 wild gunners ever preceded an enemy turret.
        """
        if ct.read_store(SLOT_GUNNERS) >= MAX_GUNNERS:
            return False
        target = self._nearest_enemy_turret(ct, pos)
        if target is None:
            return False
        if self._already_answered(ct, target):
            return False
        if not self._cb_latch(ct, rnd):
            return False
        # Income gate.  Two of the ten wild games left an enemy forward turret
        # unanswered; a bare cost check is the cheapest honest version of that.
        if ct.get_global_resources() < ct.get_gunner_cost():
            return False

        if ct.get_action_cooldown() == 0:
            best = None
            for d in CARDINALS:
                site = pos.add(d)
                if not in_bounds(ct, site):
                    continue
                dsq = site.distance_squared(target)
                if dsq == 0 or dsq > CB_SITE_SQ:
                    continue
                facing = exact_facing(site, target)
                if facing is None:
                    continue
                try:
                    if not ct.can_build_gunner(site, facing):
                        continue
                except GameError:
                    continue
                key = (dsq, site.x, site.y)
                if best is None or key < best[0]:
                    best = (key, site, facing)
            if best is not None:
                try:
                    ct.build_gunner(best[1], best[2])
                except GameError:
                    return False
                ct.write_store(SLOT_GUNNERS, ct.read_store(SLOT_GUNNERS) + 1)
                return True

        # Not in position yet: walk onto the turret's doorstep.
        return self._step_toward(ct, target)

    def _cb_latch(self, ct: Controller, rnd: int) -> bool:
        """At most one builder is on counterbattery duty at a time.

        Owner id and heartbeat share one store int.  Claims collide harmlessly:
        writes are last-writer-wins, so exactly one value lands and exactly one
        builder reads its own id back next round.  A builder that is not the
        owner does not chase, which is what keeps the other four on the economy
        and on the heal line while a turret-heavy opponent plants all game.
        """
        my_id = ct.get_id()
        packed = ct.read_store(SLOT_CB_LATCH)
        owner = packed // LATCH_MOD
        ping = packed % LATCH_MOD
        if packed > 0 and owner == my_id:
            ct.write_store(SLOT_CB_LATCH, my_id * LATCH_MOD + (rnd % LATCH_MOD))
            return True
        stale = packed <= 0 or ((rnd - ping) % LATCH_MOD) > CB_LATCH_STALE
        if stale:
            ct.write_store(SLOT_CB_LATCH, my_id * LATCH_MOD + (rnd % LATCH_MOD))
        return False

    def _nearest_enemy_turret(
        self, ct: Controller, pos: Position
    ) -> Position | None:
        my_team = ct.get_team()
        best = None
        try:
            nearby = ct.get_nearby_buildings()
        except GameError:
            return None
        for bid in nearby:
            try:
                if ct.get_team(bid) == my_team:
                    continue
                if ct.get_entity_type(bid) not in TURRET_TYPES:
                    continue
                where = ct.get_position(bid)
            except GameError:
                continue
            key = (pos.distance_squared(where), where.x, where.y)
            if best is None or key < best[0]:
                best = (key, where)
        return best[1] if best is not None else None

    def _already_answered(self, ct: Controller, target: Position) -> bool:
        """Is one of our gunners already covering this turret?"""
        my_team = ct.get_team()
        try:
            nearby = ct.get_nearby_buildings()
        except GameError:
            return False
        for bid in nearby:
            try:
                if ct.get_team(bid) != my_team:
                    continue
                if ct.get_entity_type(bid) != EntityType.GUNNER:
                    continue
                if ct.get_position(bid).distance_squared(target) <= CB_COVER_SQ:
                    return True
            except GameError:
                continue
        return False

    # -- item 3: the heal controller -------------------------------------

    def _medic_duty(self, ct: Controller, pos: Position) -> bool:
        """Answer the Core's published demand for medics.

        Seats below the demand line walk home and hold an orthogonally
        adjacent tile, healing the Core every round it is short of full.  The
        forward builder is exempt -- it is tending the siege sentinel.
        """
        if self.is_forward or self.home is None:
            return False
        want = ct.read_store(SLOT_MEDICS)
        if want <= 0 or self.seat >= want:
            return False

        core_tile = adjacent_core_tile(pos, self.home)
        if core_tile is not None:
            if self._heal_here(ct, pos):
                return True
            # Standing by on station -- holding position is the duty.
            return True
        ring = [t for t in core_port_ring(self.home) if in_bounds(ct, t)]
        if not ring:
            return False
        station = ring[self.seat % len(ring)]
        if self._step_toward(ct, station):
            return True
        return self._heal_here(ct, pos)

    def _heal_rank(self, etype) -> int:
        if etype == EntityType.CORE:
            return HEAL_RANK_CORE
        if etype in TURRET_TYPES:
            return HEAL_RANK_TURRET
        if etype in ECONOMY_TYPES:
            return HEAL_RANK_ECON
        return HEAL_RANK_BOT

    def _heal_here(self, ct: Controller, pos: Position) -> bool:
        """Heal the most-damaged friendly asset on an orthogonally adjacent
        tile.  Priority core >= turret > conveyor, then most damaged, then
        (x, y).  can_heal() refuses a full-HP target, so the HP check is not
        redundant -- it is what keeps the scan from burning the turn.
        """
        if ct.get_action_cooldown() != 0:
            return False
        if ct.get_global_resources() < HEAL_COST:
            return False
        my_team = ct.get_team()
        best = None
        for d in CARDINALS:
            tile = pos.add(d)
            if not in_bounds(ct, tile):
                continue
            key = None
            try:
                bid = ct.get_tile_building_id(tile)
                if bid is not None and ct.get_team(bid) == my_team:
                    hp = ct.get_hp(bid)
                    mx = ct.get_max_hp(bid)
                    if hp < mx:
                        key = (
                            self._heal_rank(ct.get_entity_type(bid)),
                            hp - mx,
                            tile.x,
                            tile.y,
                        )
                if key is None:
                    uid = ct.get_tile_builder_bot_id(tile)
                    if uid is not None and ct.get_team(uid) == my_team:
                        hp = ct.get_hp(uid)
                        mx = ct.get_max_hp(uid)
                        if hp < mx:
                            key = (HEAL_RANK_BOT, hp - mx, tile.x, tile.y)
                if key is None:
                    continue
                if not ct.can_heal(tile):
                    continue
            except GameError:
                continue
            if best is None or key < best[0]:
                best = (key, tile)
        if best is None:
            return False
        try:
            ct.heal(best[1])
        except GameError:
            return False
        return True

    # -- item 2: the standing forward sentinel ---------------------------

    def _run_forward(self, ct: Controller, rnd: int, pos: Position) -> None:
        if self.enemy is None:
            self._run_eco(ct, rnd, pos)
            return

        if self._sentinel_alive(ct, rnd):
            # Standing, not one-shot: hold beside it and keep it repaired.
            if self._heal_here(ct, pos):
                return
            if self.sent_site is not None and manhattan(pos, self.sent_site) > 1:
                if self._step_toward(ct, self.sent_site):
                    return
            return

        if ct.read_store(SLOT_SENTINELS) >= MAX_SENTINELS:
            self._run_eco(ct, rnd, pos)
            return

        site = self._sentinel_site(ct)
        if site is None:
            self._run_eco(ct, rnd, pos)
            return
        target, facing = site

        if manhattan(pos, target) == 1:
            if ct.get_action_cooldown() != 0:
                return
            if ct.get_global_resources() < ct.get_sentinel_cost():
                # Walk-distance-gated, then cost-gated: hold and repair.
                self._heal_here(ct, pos)
                return
            try:
                if ct.can_build_sentinel(target, facing):
                    ct.build_sentinel(target, facing)
                    ct.write_store(
                        SLOT_SENTINELS, ct.read_store(SLOT_SENTINELS) + 1
                    )
                    self.sent_site = target
                    self.sent_facing = facing
                    self.sent_built_round = rnd
                    return
            except GameError:
                pass
            # Site refused (occupied / walled): drop it and re-pick next round.
            self.sent_site = None
            self.sent_facing = None
            return

        if pos == target:
            self._step_off(ct, pos)
            return
        if self._step_toward(ct, target):
            return
        if self.stuck >= 6:
            # Cannot reach the chosen site; forget it and let the ranked list
            # hand back the next one.
            self.sent_site = None
            self.sent_facing = None
        self._heal_here(ct, pos)

    def _sentinel_alive(self, ct: Controller, rnd: int) -> bool:
        if self.sent_built_round is not None:
            if rnd - self.sent_built_round <= SENT_BUILD_GRACE:
                return True
        beat = ct.read_store(SLOT_SENT_ALIVE)
        return beat > 0 and rnd - (beat - 1) <= SENT_BEAT_STALE

    def _sentinel_site(self, ct: Controller):
        """A passable tile at d^2 16-25 from the enemy core that is exactly on
        a firing ray through a footprint tile, nearest to home first.

        Cached: the site only changes when it is refused, so this whole scan
        runs a handful of times per match rather than every round.
        """
        if self.sent_site is not None and self.sent_facing is not None:
            return (self.sent_site, self.sent_facing)
        if self.enemy is None:
            return None
        anchor = self.home if self.home is not None else ct.get_position()
        foot = core_footprint(self.enemy)

        for offsets, banded in ((SENT_OFFSETS, True), (SENT_FALLBACK_OFFSETS, False)):
            cands = []
            seen = set()
            for tile in foot:
                for dx, dy in offsets:
                    site = Position(tile.x + dx, tile.y + dy)
                    if (site.x, site.y) in seen:
                        continue
                    seen.add((site.x, site.y))
                    if not in_bounds(ct, site):
                        continue
                    dsq = core_dist_sq(site, self.enemy)
                    if banded and not (SENT_BAND_LO <= dsq <= SENT_BAND_HI):
                        continue
                    facing = exact_facing(site, tile)
                    if facing is None:
                        continue
                    cands.append(
                        (
                            (site.distance_squared(anchor), site.x, site.y),
                            site,
                            facing,
                        )
                    )
            cands.sort(key=lambda c: c[0])
            for _key, site, facing in cands:
                try:
                    if ct.get_tile_env(site) == Environment.WALL:
                        continue
                    if ct.get_tile_building_id(site) is not None:
                        continue
                except GameError:
                    pass  # out of vision: assume clear, re-checked on arrival
                self.sent_site = site
                self.sent_facing = facing
                return (site, facing)
        return None

    # -- item 5: the income-gated launcher ring --------------------------

    def _launcher_duty(self, ct: Controller, rnd: int, pos: Position) -> bool:
        if self.seat != LAUNCH_SEAT or self.home is None:
            return False
        built = ct.read_store(SLOT_LAUNCHERS)
        if built >= MAX_LAUNCHERS:
            return False
        if rnd < LAUNCH_FIRST or rnd > LAUNCH_LAST:
            return False
        if rnd < LAUNCH_FIRST + built * LAUNCH_GAP:
            return False
        titanium = ct.get_global_resources()
        # "Suppress entirely when Ti < ~50" -- zero launchers in the two wild
        # games where titanium sat at 0-22, and those are 2 of the 4 losses.
        if titanium < LAUNCH_MIN_TI or titanium < ct.get_launcher_cost():
            return False

        sites = self._launcher_sites(ct)
        # Skip candidates our own economy has already built over.  The ring
        # band and the conveyor chain occupy the same tiles, so a ring that
        # retires a blocked site permanently never places a second launcher on
        # a dense map -- measured, 0 launchers on lighthouse and eider.
        while self.launch_idx < len(sites):
            cand = sites[self.launch_idx]
            try:
                if ct.get_tile_building_id(cand) is not None:
                    self.launch_idx += 1
                    continue
            except GameError:
                pass  # out of vision: assume clear, re-checked on arrival
            break
        if self.launch_idx >= len(sites):
            return False
        target = sites[self.launch_idx]

        if manhattan(pos, target) == 1:
            if ct.get_action_cooldown() != 0:
                return True
            try:
                if ct.can_build_launcher(target):
                    ct.build_launcher(target)
                    ct.write_store(SLOT_LAUNCHERS, built + 1)
                    self.launch_idx += 1
                    return True
            except GameError:
                pass
            self.launch_idx += 1
            return True
        if pos == target:
            self._step_off(ct, pos)
            return True
        if self._step_toward(ct, target):
            return True
        if self.stuck >= 8:
            self.launch_idx += 1
        return False

    def _launcher_sites(self, ct: Controller) -> list:
        """Tiles at d^2 4-17 from our own core, ranked by how far they lean
        toward the enemy and spaced apart.  Computed once per builder; the
        list is longer than MAX_LAUNCHERS so a blocked site costs a cursor
        step rather than the whole ring.
        """
        if self.launch_sites is not None:
            return self.launch_sites
        if self.home is None:
            return []
        hx = self.home.x + 0.5
        hy = self.home.y + 0.5
        if self.enemy is not None:
            ex = self.enemy.x + 0.5
            ey = self.enemy.y + 0.5
        else:
            ex, ey = hx + 1.0, hy
        dx, dy = ex - hx, ey - hy
        norm = (dx * dx + dy * dy) ** 0.5
        if norm < 1e-6:
            ux, uy = 1.0, 0.0
        else:
            ux, uy = dx / norm, dy / norm

        cands = []
        for ox in range(-5, 7):
            for oy in range(-5, 7):
                site = Position(self.home.x + ox, self.home.y + oy)
                if not in_bounds(ct, site):
                    continue
                dsq = core_dist_sq(site, self.home)
                if not (LAUNCH_BAND_LO <= dsq <= LAUNCH_BAND_HI):
                    continue
                try:
                    if ct.get_tile_env(site) == Environment.WALL:
                        continue
                except GameError:
                    pass
                # Lean toward the enemy: project onto the core-to-core lane.
                vx = site.x + 0.0 - hx
                vy = site.y + 0.0 - hy
                along = vx * ux + vy * uy
                cands.append(((-along, site.x, site.y), site))
        cands.sort(key=lambda c: c[0])
        picked = []
        for _key, site in cands:
            if any(site.distance_squared(p) < 4 for p in picked):
                continue
            picked.append(site)
            if len(picked) >= LAUNCH_CANDIDATES:
                break
        self.launch_sites = picked
        return picked

    # -- item 7: the conveyor-first economy router -----------------------

    def _run_eco(self, ct: Controller, rnd: int, pos: Position) -> None:
        self._scan_ore(ct, rnd)
        if self.stage == "pick":
            self._eco_pick(ct, pos)
        elif self.stage == "port":
            self._eco_port(ct, pos)
        elif self.stage == "route":
            self._eco_route(ct, pos)
        elif self.stage == "cap":
            self._eco_cap(ct, pos)
        elif self.stage == "harvest":
            self._eco_harvest(ct, pos)
        else:
            self._eco_idle(ct, rnd, pos)

    def _scan_ore(self, ct: Controller, rnd: int) -> None:
        """Remember ore tiles seen.  Throttled: vision r^2=20 is ~69 tiles and
        a per-round rescan on every builder is the one obvious CPU sink here.
        """
        if self.stage not in ("pick", "port") and rnd % 4 != self.seat % 4:
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

    def _eco_pick(self, ct: Controller, pos: Position) -> None:
        """Choose the ore this builder will route to, and the core port the
        chain will start from.
        """
        self.route_prev = None
        self.route_pending = None
        self.terminal = None
        self.chain_len = 0
        self.wait = 0

        if self.home is None:
            return
        if ct.get_harvester_cost() > HARVESTER_COST_CEILING:
            self.stage = "idle"
            return

        free = []
        for x, y in sorted(self.known_ore):
            tile = Position(x, y)
            try:
                if ct.get_tile_building_id(tile) is not None:
                    continue
            except GameError:
                pass  # out of vision: assume free, re-checked on arrival
            free.append(tile)
        if not free:
            self._step_toward(ct, self._explore_target(ct, pos))
            return

        # Nearest to HOME, not to the builder: the wild router grows outward
        # from its own core in short runs, and ranking by builder distance
        # doubles the conveyor run for every harvester.
        free.sort(key=lambda t: (core_dist_sq(t, self.home), t.x, t.y))
        rank = min(self.seat % 3, len(free) - 1)
        self.ore_target = free[rank]
        ring = [t for t in core_port_ring(self.home) if in_bounds(ct, t)]
        if not ring:
            self.stage = "idle"
            return
        ring.sort(
            key=lambda t: (t.distance_squared(self.ore_target), t.x, t.y)
        )
        self.port = ring[0]
        self.stage = "port"
        self._eco_port(ct, pos)

    def _eco_port(self, ct: Controller, pos: Position) -> None:
        """Walk to the core-adjacent tile the chain starts from."""
        if self.port is None or self.ore_target is None:
            self.stage = "pick"
            return
        if pos == self.port:
            self.stage = "route"
            self.route_prev = None
            self.route_pending = None
            self._eco_route(ct, pos)
            return
        if not self._step_toward(ct, self.port) and self.stuck >= 6:
            # Port unreachable (another builder parked on it): start the chain
            # from wherever we stand instead of deadlocking.
            self.port = pos
        return

    def _eco_route(self, ct: Controller, pos: Position) -> None:
        """Lay the chain from the core outward toward the ore.

        A builder cannot build on its own tile, so each conveyor goes down on
        the tile just vacated, facing the tile before it -- i.e. FACING BACK
        TOWARD THE CORE.  That is the measured router, and it is also what
        produces the siphon: the terminal ends up beside the ore facing away
        from it before any harvester exists.
        """
        if self.ore_target is None or self.home is None:
            self.stage = "pick"
            return

        if self.route_pending is not None:
            if ct.get_action_cooldown() != 0:
                return
            face = self.route_prev
            if face is None:
                face = adjacent_core_tile(self.route_pending, self.home)
            if face is None:
                self.route_pending = None
                self.stage = "pick"
                return
            if self._build_link(ct, self.route_pending, face):
                self.route_prev = self.route_pending
                self.chain_len += 1
            self.route_pending = None
            return

        if self.chain_len > MAX_ROUTE:
            # Give up on this run.  The half-chain is left standing: an
            # unfinished chain delivers exactly nothing, and that is one of the
            # measured Clankers failure modes, not something to tidy away.
            self.stage = "pick"
            return

        if manhattan(pos, self.ore_target) == 1:
            self.terminal = pos
            self.stage = "cap"
            self._step_off(ct, pos)
            return

        before = pos
        if self._step_toward(ct, self.ore_target):
            after = ct.get_position()
            if after != before:
                self.route_pending = before
            return
        if self.stuck >= 5:
            self.stage = "pick"

    def _eco_cap(self, ct: Controller, pos: Position) -> None:
        """Build the terminal conveyor -- adjacent to the ore, facing back down
        the chain toward the core.  Only then does the harvester go in.
        """
        if self.terminal is None or self.home is None:
            self.stage = "pick"
            return
        if pos == self.terminal:
            self._step_off(ct, pos)
            return
        if manhattan(pos, self.terminal) != 1:
            if not self._step_toward(ct, self.terminal) and self.stuck >= 6:
                self.stage = "pick"
            return
        if ct.get_action_cooldown() != 0:
            return
        face = self.route_prev
        if face is None or manhattan(face, self.terminal) != 1:
            face = adjacent_core_tile(self.terminal, self.home)
        if face is None:
            self.stage = "pick"
            return
        if self._build_link(ct, self.terminal, face):
            self.stage = "harvest"
            self.wait = 0
        elif self.stuck >= 5:
            self.stage = "pick"

    def _eco_harvest(self, ct: Controller, pos: Position) -> None:
        """Harvester on the ore, once the terminal exists and 20 Ti is spare.

        DEFECT PRESERVED (item 8): the Core's ammo drip has already spent this
        round's titanium, so on a suppressed economy this builder can sit here
        for HARVEST_PATIENCE rounds and then walk away to lay yet another
        terminal -- exactly the "6 terminals, 0 harvesters, 0 delivered" game
        in the corpus.
        """
        if self.ore_target is None:
            self.stage = "pick"
            return
        self.wait += 1
        if self.wait > HARVEST_PATIENCE:
            self.stage = "pick"
            return
        if manhattan(pos, self.ore_target) != 1:
            if not self._step_toward(ct, self.ore_target) and self.stuck >= 6:
                self.stage = "pick"
            return
        if ct.get_action_cooldown() != 0:
            return
        if ct.get_global_resources() < ct.get_harvester_cost():
            self._heal_here(ct, pos)
            return
        try:
            if not ct.can_build_harvester(self.ore_target):
                self.known_ore.discard((self.ore_target.x, self.ore_target.y))
                self.stage = "pick"
                return
            ct.build_harvester(self.ore_target)
        except GameError:
            self.stage = "pick"
            return
        self.known_ore.discard((self.ore_target.x, self.ore_target.y))
        self.stage = "pick"

    def _eco_idle(self, ct: Controller, rnd: int, pos: Position) -> None:
        """Nothing to route: become part of the heal controller."""
        if rnd % 8 == 0 and ct.get_harvester_cost() <= HARVESTER_COST_CEILING:
            self.stage = "pick"
            return
        if self._heal_here(ct, pos):
            return
        hurt = self._damaged_friendly(ct, pos)
        if hurt is not None and manhattan(pos, hurt) > 1:
            self._step_toward(ct, hurt)

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
                hp = ct.get_hp(bid)
                mx = ct.get_max_hp(bid)
                if hp >= mx:
                    continue
                where = ct.get_position(bid)
                rank = self._heal_rank(ct.get_entity_type(bid))
            except GameError:
                continue
            key = (rank, pos.distance_squared(where), where.x, where.y)
            if best is None or key < best[0]:
                best = (key, where)
        return best[1] if best is not None else None

    def _build_link(
        self, ct: Controller, tile: Position, toward: Position
    ) -> bool:
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
            ct.build_conveyor(tile, facing)
        except GameError:
            return False
        return True

    def _explore_target(self, ct: Controller, pos: Position) -> Position:
        """No ore in memory: sweep outward from home in a fixed rosette."""
        anchor = self.home if self.home is not None else pos
        w, h = ct.get_map_width(), ct.get_map_height()
        ring = (
            (6, 0), (0, 6), (-6, 0), (0, -6),
            (5, 5), (-5, 5), (5, -5), (-5, -5),
        )
        if self.stuck >= 3:
            self.explore_idx += 1
        dx, dy = ring[(self.explore_idx + self.seat) % len(ring)]
        return Position(
            min(max(anchor.x + dx, 0), w - 1),
            min(max(anchor.y + dy, 0), h - 1),
        )

    # ------------------------------------------------------------------
    # Sentinel -- the siege gun
    # ------------------------------------------------------------------

    def _run_sentinel(self, ct: Controller) -> None:
        rnd = ct.get_current_round()
        ct.write_store(SLOT_SENT_ALIVE, rnd + 1)
        pos = ct.get_position()
        self._locate(ct)
        target = self._ray_target(
            ct,
            pos,
            (
                EntityType.CORE,
                EntityType.GUNNER,
                EntityType.SENTINEL,
                EntityType.LAUNCHER,
                EntityType.BUILDER_BOT,
            ),
        )
        if target is None:
            return
        try:
            if ct.can_fire(target):
                ct.fire(target)
        except GameError:
            return

    # ------------------------------------------------------------------
    # Gunner -- counterbattery only; never rotates
    # ------------------------------------------------------------------

    def _run_gunner(self, ct: Controller) -> None:
        """Fire until the turret it was built to answer is dead, then keep the
        line.  rotate() is never called: the wild gunners are single-purpose
        and are built already facing their target.
        """
        pos = ct.get_position()
        self._locate(ct)
        target = self._ray_target(
            ct,
            pos,
            (
                EntityType.GUNNER,
                EntityType.SENTINEL,
                EntityType.LAUNCHER,
                EntityType.CORE,
                EntityType.BUILDER_BOT,
            ),
        )
        if target is None:
            return
        try:
            if ct.can_fire(target):
                ct.fire(target)
        except GameError:
            return

    def _ray_target(
        self, ct: Controller, pos: Position, order
    ) -> Position | None:
        """Best enemy tile on this turret's ray, by an explicit type order then
        nearest.  Never enumeration order -- get_attackable_tiles() is row-major
        in absolute map coordinates, so "first hit wins" flips near/far with
        facing and is an absolutely-oriented bug.
        """
        my_team = ct.get_team()
        buckets = {}
        fallback = None
        try:
            tiles = ct.get_attackable_tiles()
        except GameError:
            return None
        for tile in tiles:
            if not in_bounds(ct, tile):
                continue
            try:
                tid = ct.get_tile_builder_bot_id(tile)
                is_bot = tid is not None
                if tid is None:
                    tid = ct.get_tile_building_id(tile)
                if tid is None:
                    continue
                if ct.get_team(tid) == my_team:
                    continue
                etype = (
                    EntityType.BUILDER_BOT if is_bot else ct.get_entity_type(tid)
                )
            except GameError:
                continue
            key = (pos.distance_squared(tile), tile.x, tile.y)
            cur = buckets.get(etype)
            if cur is None or key < cur[0]:
                buckets[etype] = (key, tile)
            if fallback is None or key < fallback[0]:
                fallback = (key, tile)
        for etype in order:
            hit = buckets.get(etype)
            if hit is not None:
                return hit[1]
        return fallback[1] if fallback is not None else None

    # ------------------------------------------------------------------
    # Launcher -- ejection ring
    # ------------------------------------------------------------------

    def _run_launcher(self, ct: Controller) -> None:
        """Throw any adjacent enemy builder to a passable tile FURTHER from our
        own core.  439/439 wild ejections were enemy builders, 439/439 away.
        """
        if ct.get_action_cooldown() != 0:
            return
        pos = ct.get_position()
        self._locate(ct)
        if self.home is None:
            return
        my_team = ct.get_team()

        victims = []
        try:
            nearby = ct.get_nearby_units(dist_sq=2)
        except GameError:
            return
        for uid in nearby:
            try:
                if ct.get_team(uid) == my_team:
                    continue
                if ct.get_entity_type(uid) != EntityType.BUILDER_BOT:
                    continue
                where = ct.get_position(uid)
            except GameError:
                continue
            victims.append(((pos.distance_squared(where), where.x, where.y), where))
        if not victims:
            return
        victims.sort(key=lambda v: v[0])
        bot_pos = victims[0][1]

        try:
            tiles = ct.get_nearby_tiles(dist_sq=LAUNCH_THROW_SQ)
        except GameError:
            return
        here = core_dist_sq(bot_pos, self.home)
        ranked = []
        for tile in tiles:
            away = core_dist_sq(tile, self.home)
            if away <= here:
                continue
            ranked.append(((-away, tile.x, tile.y), tile))
        if not ranked:
            return
        ranked.sort(key=lambda r: r[0])
        for _key, tile in ranked[:LAUNCH_TRIES]:
            try:
                if not ct.is_tile_passable(tile):
                    continue
                if not ct.can_launch(bot_pos, tile):
                    continue
                ct.launch(bot_pos, tile)
                return
            except GameError:
                continue

    # ------------------------------------------------------------------
    # movement
    # ------------------------------------------------------------------

    def _step_toward(self, ct: Controller, dst: Position | None) -> bool:
        """One cardinal step toward dst; if the preferred axis is blocked, try
        the other, then the perpendiculars, then backwards.  Deterministic.
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
        major_first = abs(dx) >= abs(dy)
        if self.stuck >= 2:
            # Leading with the minor axis is what gets a bot around a wall
            # corner rather than grinding into it.
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

    def _step_off(self, ct: Controller, pos: Position) -> None:
        """Vacate the current tile so a building can go down on it.  Steps back
        toward the core, which is down the chain we just laid and therefore
        conveyor (bot-passable).
        """
        if ct.get_move_cooldown() != 0:
            return
        prefs = []
        anchor = self.route_prev if self.route_prev is not None else self.home
        if anchor is not None:
            if anchor.x > pos.x:
                prefs.append(Direction.EAST)
            elif anchor.x < pos.x:
                prefs.append(Direction.WEST)
            if anchor.y > pos.y:
                prefs.append(Direction.SOUTH)
            elif anchor.y < pos.y:
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
