"""v61 OFFLINE — Replay-routed macro with early counterbattery pressure.

The ladder replays showed that one-hop Launchers and a 60-ammo stockpile were
dead capital.  This branch instead fields five useful builders, connects ore
immediately, and spends ammunition just in time on forward and home gunners.

_v70th variant: TURRET-HUNTING UNDER SIEGE.  _v70mh's converged healers repair
a shelled Core but never silence what is shelling it, so a Sentinel parked
beside our own footprint out-damages four healers indefinitely.  This branch
lets one designated builder per near-Core enemy turret spend its action pecking
that turret instead of healing, but only while the repair line stays manned or
the turret is already nearly dead.  Everything else -- roles, economy, siege
planning, the interceptor and the saboteur -- is bit-for-bit _v70mh.
"""
import math
import random
from collections import deque

from fcode import Direction, EntityType, Environment, Position


# PIECE SPLIT (s21): every constant and doctrine flag now lives in doctrine.py,
# moved verbatim and proved identical by a det leg.  See that file's header
# for the rule on adding new flags.
from doctrine import *  # noqa: F401,F403



def enemy_core_for(w, h, own):
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

    # The duplicate 26x26 layouts differ within initial builder vision.  Score
    # every sensed environment tile once; buildings and bots do not affect it.
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
    # Conveyor outputs are cardinal.  Chebyshev distance can prefer a diagonal
    # Core tile on a tie and rotate the last conveyor away from the receiver.
    return min(core_tiles(o), key=lambda c: abs(pos.x - c.x) + abs(pos.y - c.y))


def heal_seats(o, mw, mh):
    """PLANK HS: the Core's heal seats, in a fixed clockwise scan order.

    The eight orthogonal neighbours of the 2x2 footprint anchored at `o`, which
    is exactly the set _link_path builds as its raw_goals and exactly the set
    _healer_floor counts -- the only tiles from which a builder can heal a Core
    tile, and the only tiles a conveyor can deliver into the Core from.  None of
    the eight can be a footprint tile by construction, so no dist_core test is
    needed; out-of-bounds seats are dropped, which is what shrinks the ring to
    five or three for an edge or corner Core.  Order is fixed (N pair, E pair, S
    pair, W pair) so every tie-break downstream is deterministic.
    """
    seats = (
        Position(o.x, o.y - 1), Position(o.x + 1, o.y - 1),
        Position(o.x + 2, o.y), Position(o.x + 2, o.y + 1),
        Position(o.x + 1, o.y + 2), Position(o.x, o.y + 2),
        Position(o.x - 1, o.y + 1), Position(o.x - 1, o.y),
    )
    return [s for s in seats if 0 <= s.x < mw and 0 <= s.y < mh]


def delivery_seats(o, mw, mh, walls, ores):
    """PLANK HS: the seats reserved for delivery (see HS_SEAT_PROTECT_ON).

    Every OTHER seat becomes a no-build tile, so this choice is the whole safety
    margin of mechanism 1: pick badly and a harvester chain has nowhere to
    terminate.  Three properties make it safe to compute per unit with no store
    slot and no coordination:

     - PURE FUNCTION OF MAP GEOMETRY.  Footprint, dimensions, decoded walls and
       decoded ore -- all four are identical for every unit on the team, so
       every unit derives the same reserved seats without talking to anyone.  On
       an undecoded map walls and ore are both empty for everyone alike and the
       ore vote falls back to the map centre, which is still unanimous.
     - AIMED AT THE ORE.  The trunk chain arrives from the harvester field, so
       the seats kept open are the ones nearest the HS_ORE_SAMPLE closest ore
       tiles.  Scored as a sum of Manhattan distances rather than against a
       centroid so the whole comparison stays in integers.
     - NEVER EMPTY WHILE A SEAT EXISTS.  Walled seats are dropped first, but if
       that would leave nothing the walled ones come back: an empty reserve
       would make _link_path return no goals at all and silently kill every
       chain on the map, which is a far worse failure than reserving a seat we
       cannot use.
    """
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
    """PIECE E2B predicate (see E2B_ORE_PAVE_BAN_ON): may this tile NOT be paved?

    True means "do not lay a conveyor here".  Unreadable answers count as ore:
    get_tile_env raises outside vision, and per PIECE N a tile this unit
    believes is adjacent can be arbitrarily far away after a Launcher throw, so
    the vision test comes first and every remaining surprise is swallowed.
    Skipping a legal pave costs 3 Ti of trail; paving a mine costs the site.
    """
    try:
        if not ct.is_in_vision(tile):
            return True
        return ct.get_tile_env(tile) == Environment.ORE_TITANIUM
    except Exception:
        return True


def pave_blocked(ct, tile, banned):
    """Shared pave gate: may this tile NOT carry one of our conveyors?

    Two independent bans behind one predicate so the two pave sites in _move
    (and the link planner) cannot drift apart:

     - PLANK HS heal seats.  `banned` is the caller's reserved-seat ban set, or
       None when the ban is off or the Core is not known yet.  Pure set
       membership, no engine call, so it runs first and costs nothing on the
       rounds it does not fire.
     - PIECE E2B ore, unchanged and still the sole owner of the ore question,
       including its fail-closed vision handling.

    With both toggles off this answers False for every tile, which is the
    pre-E2B, pre-plank behaviour exactly.
    """
    if banned is not None and (tile.x, tile.y) in banned:
        return True
    return E2B_ORE_PAVE_BAN_ON and pave_blocked_by_ore(ct, tile)


class Player:
    def __init__(self):
        self.n = 0
        self.team = None
        self.core = None
        self.enemy = None
        self.mw = self.mh = 0
        self.role = "expand"
        self.tgt = None
        self.last = None
        self.stuck = 0
        self.wall = None
        self.ang = 0.0
        self.idx = 0
        self.role_n = 0
        self.link_queue = []
        self.link_source = None
        self.dropped = False
        self.map_grid = None
        self.map_walls = set()
        self.melee_first = False
        # PIECE F trail memory (see PAVE_TRAIL_ON).  Per unit instance, no
        # store slot: only this unit's own _move writes it and only its own
        # pave reads it.  pave_prev is the tile vacated by the last successful
        # move and pave_dir the direction of that move, so the conveyor laid on
        # pave_prev outputs onto the tile the unit now stands on.  pave_rnd is
        # the round the move happened; the pave accepts the pair ONLY at
        # pave_rnd == round - 1, which is exactly the mandated "cleared on any
        # round the unit does not move" invalidation, expressed lazily so it
        # also holds on the paths where _builder returns early, where the unit
        # moved outside _move, and where the turn is cut by the CPU guard.
        self.pave_prev = None
        self.pave_dir = None
        self.pave_rnd = -2
        # B8 sensing tier (see B8_ON).  Hoisted here and set once in
        # _builder's team-init block; v79 recomputes both per visible enemy
        # inside the loop, which is the same value every time.  The defaults
        # are today's literals, so a unit that never reaches the team-init
        # block behaves exactly as before.
        self.gun_sense = 64
        self.b_sense = 16
        self.map_ores = []
        self.ore_cursor = 0
        self.forward_guns = 0
        self.forward_barriers = 0
        self.siege_spot = None
        self.siege_approach = None
        self.siege_direction = None
        self.siege_type = None
        self.last_hp = None

        # PLANK HS seat memory (see HS_SEAT_PROTECT_ON).  Per unit instance, no
        # store slot: both are pure functions of map geometry that every unit
        # computes to the same answer, so a slot would only buy a round of lag.
        # seat_ban is the frozen key set of seats this unit may never build on
        # and seat_keep the reserved delivery seats; both stay None until the
        # first call that needs them, which is also the first turn the Core
        # position and the decoded map are both known.
        self.seat_ban = None
        self.seat_keep = None

        # Live-builder accounting, Core-only (see _core).  prev_units is the
        # unit count at the previous Core turn; lost_units the running total of
        # its drops over the match, i.e. how many units we know have died.
        self.prev_units = None
        self.lost_units = 0

        # INCOME METER, Core-only (see the meter block in _core).  Cumulative
        # estimated income in QUARTER-titanium, so passive (10 Ti / 4 rounds)
        # and harvester output (a 10-stack / 4 rounds) are both exact integers
        # per round and no float ever enters the hot path.  The Core is a
        # single unit with a persistent Player instance, so this integrates
        # cleanly without a store slot; only the derived budget is published.
        self.income_q = 0

        # PIECE K heal ledger, per builder instance (see K_HEAL_BUDGET_ON for
        # why this is NOT a team-wide store counter).  Counts heal actions this
        # unit has taken from K's priority block; each is 1 Ti.
        self.heal_spent = 0

        # Interception state, per unit instance -- no store slot is spent on
        # it because exactly one builder (role_n == 1) ever reads or writes it.
        self.chase_id = None
        self.chase_pos = None
        self.chase_seen = 0
        # Escort stalemate ledgers (see _guard_target): building id ->
        # consecutive not-whole escort rounds / ban-until round.
        self.escort_watch = {}
        self.escort_ban = {}

        # SIPHON HYGIENE state, per unit instance -- same locality argument as
        # chase_* and escort_* above: only this builder reads or writes them.
        # wire_pending is [(harvester position, round it was built), ...] for
        # harvesters THIS builder placed that do not have a chain yet; it is
        # keyed on nothing but the build event, so a REBUILD of a site we once
        # wired enqueues exactly like a first build (the adjacency test in
        # _has_acceptor, not any memory of the site, is what retires an entry).
        # siphon_* is the deny arm's target memory plus its write-off ledger.
        self.wire_pending = []
        self.siphon_id = None
        self.siphon_pos = None
        self.siphon_since = 0
        self.siphon_hp = None
        self.siphon_ban = {}

        # True while this expander is converging on a shelled Core (see the
        # MULTI-HEALER CONVERGENCE block in _expand).  Per unit instance, no
        # store slot: it is read and written only by its own unit, and only to
        # detect the falling edge so the expand machine gets a clean state back.
        self.converging = False

        # True while this builder owns a near-Core enemy turret (see the
        # TURRET-HUNTING UNDER SIEGE block above and _hunt_turret).  Per unit
        # instance for the same reason self.converging is: read and written only
        # by its own unit, and only to detect the falling edge -- when the
        # turret dies or leaves the band -- so the heal/converge machine gets a
        # clean state back instead of a stale turret tile in self.tgt.
        self.hunting = False

        # Per-turret deference ledger for the ballot deadlock breaker: turret
        # entity id -> [rounds deferred with no HP progress, last seen HP].
        # Same locality argument as self.hunting; pruned in _hunt_turret so it
        # cannot grow past the handful of turrets a siege ever parks near us.
        self.hunt_defer = {}

        # PIECE I rotation memory (see ROTATE_DISCIPLINE_ON).  The tile this
        # Gunner is currently aimed at, so the hysteresis rule has something to
        # compare a new candidate against.  Per unit instance, no store slot:
        # only this turret's own _idle_rotate reads or writes it, and a stale
        # value fails the liveness test below rather than misleading anyone.
        self.rot_tgt = None

        # Rotation latch (see ROTATE_COOLDOWN_RNDS).  rot_rnd is the round this
        # gunner last PAID for a rotation, rot_prev_dir the facing it left, and
        # rot_lock_d the dsq of the target it bought.  rot_lock_d is the stable
        # yardstick the in-window hysteresis compares against: rot_tgt above is
        # a tile, and a tile goes stale the moment the enemy standing on it
        # takes a step, which is exactly how the nordkap oscillation gets in.
        # Same per-unit-instance argument as rot_tgt -- one Player per unit, so
        # a latch here is this gunner's own and never gags the others.
        self.rot_rnd = -10 ** 9
        self.rot_prev_dir = None
        self.rot_lock_d = 10 ** 9

        # Whether we've already reported a CPU-guard trip for this unit to
        # stderr. One line per unit lifetime so a chronically slow unit
        # can't flood the log (ported from bots/ladder1).
        self.reported_cpu = False

        # Whether we've already reported an escaped exception for this unit
        # (ported from bots/ladder1, v1 heritage). One traceback per unit
        # lifetime so a bug that fires every round can't flood stderr or burn
        # the CPU budget formatting tracebacks.
        self.reported_error = False

    def run(self, ct):
        # An exception that escapes run() makes the engine PERMANENTLY delete
        # this unit for the rest of the match. Catching it costs one round's
        # action instead; there is no situation where propagating is better.
        try:
            self._dispatch(ct)
        except Exception:
            if not self.reported_error:
                self.reported_error = True
                import sys
                import traceback
                traceback.print_exc(file=sys.stderr)

    def _dispatch(self, ct):
        e = ct.get_entity_type()
        if e == EntityType.CORE:
            self._core(ct)
        elif e == EntityType.BUILDER_BOT:
            self._builder(ct)
        elif e in (EntityType.GUNNER, EntityType.SENTINEL):
            self._turret(ct)
        elif e == EntityType.LAUNCHER:
            self._launcher(ct)

    def _cpu_exhausted(self, ct):
        """True once this unit's round has used CPU_BUDGET_US of its 10 ms
        budget. Ported from bots/ladder1.

        Callers bail out of remaining lower-priority work when this trips, so
        a round degrades at a boundary this file chooses instead of being
        truncated mid-statement by the engine. Reported once per unit to
        stderr -- print() is captured into the replay, not the console, so
        stderr is the only way to see this locally (see docs/tooling.md).
        """
        if ct.get_cpu_time_elapsed() < CPU_BUDGET_US:
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

    def _core(self, ct):
        p = ct.get_position()
        w, h = ct.get_map_width(), ct.get_map_height()
        if self.map_grid is None:
            self.map_grid = known_map_for(w, h, p, ct)
        if ct.read_store(SLOT_ENEMY_CORE) == 0:
            ct.write_store(SLOT_ENEMY_CORE, pack_pos(enemy_core_for(w, h, p)))

        under = False
        threat = None
        for eid in ct.get_nearby_entities():
            if ct.get_team(eid) == ct.get_team():
                continue
            d = p.distance_squared(ct.get_position(eid))
            et = ct.get_entity_type(eid)
            if et in (EntityType.GUNNER, EntityType.SENTINEL) and d <= 64:
                under = True
                threat = ct.get_position(eid)
                ct.write_store(SLOT_THREAT, pack_pos(threat))
                break
            if et == EntityType.BUILDER_BOT and d <= 16:
                under = True
                threat = ct.get_position(eid)
                ct.write_store(SLOT_THREAT, pack_pos(threat))
                break
        rnd = ct.get_current_round()
        hp = ct.get_hp()
        if self.last_hp is not None and hp < self.last_hp:
            under = True
        self.last_hp = hp
        if under:
            ct.write_store(SLOT_UNDER, 1)
            ct.write_store(SLOT_ATK_RND, rnd)
        else:
            last = ct.read_store(SLOT_ATK_RND)
            # Latch 35 -> 50 (borrowed from v79 after the atoll decode): a
            # harasser that parks JUST outside every trigger radius lets a
            # 35-round latch expire between pokes, collapsing the ammo
            # magazine to one sentinel shot while the bank holds thousands
            # (measured: 13 shots fired in 1000 rounds on 2,782 banked Ti).
            under = bool(last and rnd - last < 50)
            ct.write_store(SLOT_UNDER, 1 if under else 0)

        harv = ct.read_store(SLOT_HARVESTERS)
        if harv >= ECO_NEED:
            ct.write_store(SLOT_ECO_READY, 1)

        # INCOME METER (feeds PIECE K's heal budget and RIDE-ALONG 2's
        # expansion gate).  There is no engine getter for delivered titanium,
        # and the bank cannot stand in for one: deliveries and spends land
        # between two Core turns, so a bank delta nets them against each other
        # and reads 0 on a round that earned 30 and spent 30.  What IS knowable
        # cheaply is the PIPELINE, and it is the same arithmetic the tiebreak
        # cares about -- passive income is 10 Ti every 4 rounds and every
        # connected harvester adds a 10-stack on the same 4-round cadence.  In
        # quarter-titanium that is a flat +10 per round plus K_HEAL_HARV_Q per
        # harvester per round, integrated by the one unit that runs every round
        # and has no writer to race with.
        #
        # Two documented biases, both deliberate: SLOT_HARVESTERS is a monotone
        # high-water mark of harvesters BUILT (a dead harvester never
        # decrements it), and not every built harvester is directed-connected
        # to the Core -- so K_HEAL_HARV_Q credits half the nominal rate to
        # absorb both.  Cost is one multiply-add per Core turn.
        self.income_q += 10 + K_HEAL_HARV_Q * harv
        income_ti = self.income_q // 4
        if K_HEAL_BUDGET_ON:
            ct.write_store(SLOT_HEAL_BUDGET, income_ti * K_HEAL_RATE_PCT // 100)

        ti, ammo = ct.get_global_resources(), ct.get_global_ammo()

        # PIECE H, CORE HALF -- ENDGAME SPEND-SWITCH (see ENDGAME_SWITCH_ON).
        # Past ENDGAME_RND a banked titanium is the only resource on the board
        # that scores nothing: the tiebreak reads delivered, then harvesters
        # alive, then stored, so stored Ti decides only games the first two
        # already tied.  Ammunition scores in no tiebreak either -- which is
        # exactly why this fires ONLY with a live friendly turret in the
        # Core's own sight.  With a gun standing, 40 rounds of unrestricted
        # fire is a live shot at the enemy Core and beats every tiebreak;
        # with nothing to drink it, converting would burn tiebreak-3 stored
        # titanium for zero, so the bank is left alone.
        #
        # convert_ammo is action-free, once per team per turn, uncapped in
        # amount and usable the same turn, so this is one call and it never
        # costs a spawn.  The reserve is two harvesters at current scale, held
        # back for PIECE H's builder half: a harvester built at r999 is still
        # alive at r1000 and outranks stored titanium.  It runs BEFORE the
        # ordinary magazine block and suppresses it for this turn, so the
        # 16-per-turn drip cannot spend the single conversion first.
        #
        # EIR 5.1 DUMP CAP -- TIEBREAK #3 ARITHMETIC.  As shipped this converted
        # the WHOLE bank, measured at a single 14,634-Ti dump at exactly r960
        # (snowflake g2).  That is correct only when tiebreak #1 or #2 decides
        # the game, because ammunition scores in NO tiebreak and stored titanium
        # is #3: in a delivered-tied AND harvesters-tied endgame the uncapped
        # dump hands #3 to the opponent by zeroing our own side of it.  14,634
        # stored beats any bank they can hold; 14,634 converted loses to 1.
        #
        # So convert only what the guns can plausibly BURN before r1000.  A
        # Gunner is 4 Ti a shot on reload 1 (a shot every 2 rounds, 2 Ti/round),
        # a Sentinel 10 on reload 2 (every 3 rounds, 10/3 Ti/round); x1.5 margin
        # for the rounds a target actually presents itself gives
        #   cap = remaining * (3 * gunners + 5 * sentinels)
        # in whole integers.  One Gunner over the last 40 rounds is 120 Ti, one
        # Sentinel 200 -- against a 14,634 bank the rest simply stays stored and
        # keeps scoring.  Capping against the ammo we ALREADY hold rather than
        # dumping a flat amount is what makes it safe to re-evaluate every round
        # from r960 on: as the clock runs down the cap shrinks, so the arm tops
        # the magazine up early and then goes quiet by construction.  The dump
        # still owns ammo policy for the turn whenever it is live, so the
        # ordinary 16-per-turn drip below cannot push the magazine back over the
        # cap it just set.
        endgame_dumped = False
        if ENDGAME_SWITCH_ON and rnd >= ENDGAME_RND:
            guns, sents = self._core_turret_mix(ct)
            if guns or sents:
                endgame_dumped = True
                cap = (LAST_RND - rnd) * (3 * guns + 5 * sents)
                amt = min(ti - 2 * ct.get_harvester_cost(), cap - ammo)
                if amt > 0 and ct.can_convert_ammo(amt):
                    ct.convert_ammo(amt)
                    ti = ct.get_global_resources()
                    ammo = ct.get_global_ammo()

        # PIECE KIDNAP -- AMMO SURGE (see KIDNAP_AMMO_SURGE_ON).  The launcher
        # raised SLOT_LAUNCHER to 2 last round because a throw landed a hostile
        # in a turret line, or pulled a healer off something we are shooting.
        # convert_ammo is once per team per turn, so running FIRST is what makes
        # this the turn's ammo policy; the ordinary magazine drip below then
        # fails its own can_convert_ammo() gate and is a no-op, with no flag to
        # thread.  Skipped entirely while the endgame dump owns the resource --
        # ammunition scores in no tiebreak and stored titanium is tiebreak #3.
        if (KIDNAP_AMMO_SURGE_ON and not endgame_dumped
                and ct.read_store(SLOT_LAUNCHER) == 2):
            amt = min(KIDNAP_SURGE_TI, ti - KIDNAP_SURGE_TI_FLOOR,
                      KIDNAP_SURGE_AMMO_CAP - ammo)
            if amt > 0 and ct.can_convert_ammo(amt):
                ct.convert_ammo(amt)
                ti = ct.get_global_resources()
                ammo = ct.get_global_ammo()

        # SLOT_HOME_GUN is a monotone count of turrets this team has ever
        # built.  Hoisted above the ammo branch because RIDE-ALONG 2's
        # live-builder bound reads it too, whichever ammo policy is in force.
        weapons = ct.read_store(SLOT_HOME_GUN)

        # RIDE-ALONG 1 -- SPORKS AMMO POLICY (see SPORKS_AMMO_ON).  Owns
        # ammunition for rounds 0..ENDGAME_RND-1 and replaces the working-
        # magazine block below outright: convert_ammo is once per team per
        # turn, so two policies would only mean "whichever ran first wins".
        # From ENDGAME_RND the piece-H dump and its tiebreak-#3 drip
        # suppression own the resource and this arm stands down, leaving that
        # window bit-for-bit as Eir 5.1 shipped it.
        sporks_ammo = SPORKS_AMMO_ON and not (
            ENDGAME_SWITCH_ON and rnd >= ENDGAME_RND
        )
        if sporks_ammo:
            # Round 0: the measured opening, 25 of 25 games, sd 0.  It is paid
            # out of the 500 Ti starting bank and cannot disturb the opening
            # spawn curve -- the five builders cost ~222 Ti at scale and ti is
            # re-read below before can_spend_spawn is computed.
            #
            # Thereafter: top the magazine toward the cap in one-shot
            # increments and leave the rest of the bank to the economy.  The
            # top-up only fires while ammo is BELOW the cap, so a magazine
            # nobody is firing costs nothing at all after the first fill --
            # total lifetime spend is (ammo actually burned) + the cap, not
            # SPORKS_AMMO_TOPUP per round.
            want = SPORKS_AMMO_OPEN if rnd == 0 else SPORKS_AMMO_TOPUP
            amt = min(want, SPORKS_AMMO_CAP - ammo, ti - SPORKS_AMMO_TI_FLOOR)
            if amt > 0 and ct.can_convert_ammo(amt):
                ct.convert_ammo(amt)
                # Ammo conversion is action-free; keep evaluating the Core's
                # spawn/build priorities with the updated resource balance.
                ti = ct.get_global_resources()
                ammo = ct.get_global_ammo()
        else:
            # Keep only a small working magazine.  Conversion is action-free,
            # so a 60-round stockpile merely starves harvesters and
            # counter-gunners.
            atoll_burst_magazine = (
                under and w == 18 and h == 18
                and (p.x, p.y) in ((2, 14), (14, 2))
            )
            hive_magazine = (
                weapons and w == 25 and h == 25
                and (p.x, p.y) in ((2, 20), (21, 3))
            )
            ammo_target = (
                256 if hive_magazine
                else (32 if atoll_burst_magazine else (24 if under else AMMO_FLOOR))
            )
            # Magazine scales with the guns that drink from it (borrowed from
            # v79): a fixed floor was refuted twice here (45.3%, 46.1%), but
            # those raised the target with ZERO turrets too -- the measured
            # failure is the opposite case, dry turrets on a full bank (atoll:
            # 122 Ti converted all match, 2,782 banked, 13 shots).  Four ammo
            # per gunner round is one shot each; 48 caps the magazine at a
            # dozen shots of reserve however many guns exist.
            if weapons:
                ammo_target = max(ammo_target, min(48, 4 * weapons))
            ti_floor = 12 if (under or weapons) else 52
            # PIECE E1 (see E1_AMMO_FLOOR_ON).  `under` is this round's value of
            # SLOT_UNDER -- it is written from this same local a few lines
            # above -- so the raise applies exactly on the peacetime side of
            # the siege latch and the 12-floor siege path is untouched.  max()
            # because the no-turret floor is already 52 and must not drop.
            if E1_AMMO_FLOOR_ON and not under:
                ti_floor = max(ti_floor, min(ct.get_harvester_cost(), E1_RESERVE_CAP) + E1_HARV_RESERVE_MARGIN)
            if not endgame_dumped and (under or weapons or harv >= 2) and ammo < ammo_target and ti > ti_floor:
                amt = min(16, ammo_target - ammo, ti - ti_floor)
                if amt >= 4 and ct.can_convert_ammo(amt):
                    ct.convert_ammo(amt)
                    # Ammo conversion is action-free; keep evaluating the
                    # Core's spawn/build priorities with the updated balance.
                    ti = ct.get_global_resources()
                    ammo = ct.get_global_ammo()

        snowflake_home_b = (
            w == 26 and h == 26 and p.x == 19 and p.y == 19
            and self.map_grid is not None and self.map_grid[0][0] == "."
        )
        nordkap_home_a = w == 20 and h == 26 and p.x == 9 and p.y == 6
        mature_cap = 4 if nordkap_home_a else (6 if snowflake_home_b else MAX_BUILDERS)
        spawn_cap = mature_cap if harv >= 1 else min(EARLY_BUILDERS, mature_cap)
        can_spend_spawn = ti >= ct.get_builder_bot_cost()

        # REPLACEMENT ACCOUNTING (see REPLACEMENT_MAX).  A decrease in the team
        # unit count between two Core turns is a unit that died, and each one
        # buys back one spawn above spawn_cap, REPLACEMENT_MAX for the whole
        # match.  The base spawns are untouched: the second clause is vacuously
        # true while self.n < spawn_cap, so the first five (four on nordkap,
        # six on snowflake) still spawn on exactly the old condition, at the
        # old rounds, against the old cost curve.  Only the ones ABOVE the cap
        # additionally require a healthy bank and a past-opening round.
        units = ct.get_unit_count()
        if self.prev_units is not None and units < self.prev_units:
            self.lost_units += self.prev_units - units
        self.prev_units = units
        spawn_budget = spawn_cap + min(REPLACEMENT_MAX, self.lost_units)
        # LATE LABOR SURGE (see the block by its constants): surplus-bank-only
        # extra seats.  The replacement clause below already demands
        # ti >= REPLACE_TI_FLOOR ∧ rnd >= REPLACE_MIN_RND for any spawn above
        # spawn_cap, which this gate strictly implies.
        if ti >= SURGE_TI_FLOOR and rnd >= SURGE_MIN_RND:
            spawn_budget += SURGE_EXTRA

        # SIEGE RESPAWN FLOOR (see SIEGE_HEAL_RESERVE_TI).  Under siege the
        # bodies ARE the heal line -- HUNT_MIN_HEALERS wants them standing
        # adjacent to the Core -- but that is exactly when REPLACE_TI_FLOOR is
        # least meetable: the decoded hive loss held a 2-12 Ti bank for 500
        # rounds against a 250 floor, so every dead builder stayed dead while
        # REPLACEMENT_MAX seats sat unused.  The third clause spends on a body
        # only out of money the heal line does not need this interval (builder
        # cost + the whole reserve), so bodies never steal heal money, and it
        # rides the same late/under-siege gates as the reserve itself.  `under`
        # is the Core's own fresh computation above, one round newer than the
        # buffered SLOT_UNDER any builder would read.  Base spawns
        # (self.n < spawn_cap) and the surge are untouched.
        #
        # RIDE-ALONG 2 -- POPULATION FLOOR (see POP_FLOOR_ON).  When on, the
        # bank-threshold clause is REPLACED, not supplemented: a refill up to
        # the floor asks only whether the bank covers one scaled body, and a
        # spawn above the floor asks about the delivered-Ti RATE instead of the
        # bank.  The siege clause below stays exactly as it is -- it is strictly
        # more permissive in its own window (it fires above the floor too) and
        # deleting it would lose a shipped, measured behaviour.  REPLACEMENT_MAX
        # and the surge still bound total lifetime spawns through spawn_budget.
        pop_floor = min(POP_FLOOR, spawn_cap) if POP_FLOOR_ON else 0
        pop_refill = POP_FLOOR_ON and self._live_builders(ct, units, weapons) < pop_floor
        pop_expand = (
            POP_FLOOR_ON
            and rnd >= REPLACE_MIN_RND
            and 10 + K_HEAL_HARV_Q * harv >= 4 * POP_EXPAND_TI_RATE
        )
        # PLANK HS, MECHANISM 3 -- POPULATION CEILING LIFT (see
        # POP_CEILING_LIFT_ON).  The refill-to-floor clause is the ONE spawn
        # reason in this block that is already fully gated by its own arithmetic
        # -- it fires only while live builders sit below the floor, and it pays
        # for the body out of a bank read that has to clear the scaled cost
        # anyway -- so the lifetime bound adds nothing to it but a way to run
        # out.  Lifted here rather than inside the disjunction so the bound
        # still binds every other reason unchanged: expansion, replacement and
        # the surge all keep asking `self.n < spawn_budget` exactly as before,
        # and a game whose population never dips below the floor never evaluates
        # this at all.
        budget_ok = self.n < spawn_budget
        if POP_CEILING_LIFT_ON and pop_refill:
            budget_ok = True
        if (
            budget_ok
            and (
                self.n < spawn_cap
                or (
                    (pop_refill or pop_expand) if POP_FLOOR_ON
                    else (ti >= REPLACE_TI_FLOOR and rnd >= REPLACE_MIN_RND)
                )
                or (
                    SIEGE_RESPAWN_ON
                    and under
                    and rnd >= HUNT_MIN_RND
                    and ti >= ct.get_builder_bot_cost() + SIEGE_HEAL_RESERVE_TI
                )
            )
            and can_spend_spawn and ti >= ct.get_builder_bot_cost()
        ):
            cands = ring(p, 2)
            # Dead branch removed: a first-builder enemy-facing sort keyed on
            # SLOT_ENEMY_CORE, written and read in the same round-0 turn, so the
            # buffered store always unpacked None.  Activating it measured 41%.
            # Stable dispersion makes paired offline results reproducible.
            # PIECE G: one re-roll of the dispersion pattern per game, drawn
            # once per match from OS entropy (each game is a fresh interpreter).
            # Within-match stability is preserved -- units still coordinate
            # against a single fixed pattern for the whole match -- while
            # cross-game determinism is deliberately broken, so identical-key
            # ladder games diverge from the first spawn and chaos does the rest.
            # With NOISE_ON False the salt is 0 and the key is arithmetically
            # identical to the pre-Piece-G sort.  No per-turn cost.
            if not hasattr(self, "spawn_salt"):
                self.spawn_salt = random.Random().randrange(97) if NOISE_ON else 0
            cands.sort(key=lambda sp: ((sp.x * 17 + sp.y * 31 + self.n * 13 + self.spawn_salt) % 97, sp.y, sp.x))
            for sp in cands:
                if 0 <= sp.x < w and 0 <= sp.y < h and ct.can_spawn(sp):
                    ct.spawn_builder(sp)
                    self.n += 1
                    return

        # Cores cannot construct turrets; the defender consumes SLOT_THREAT and
        # owns all counterbattery placement.

    def _live_builders(self, ct, units, weapons):
        """RIDE-ALONG 2 -- best cheap LOWER bound on our live builder count.

        The engine gives the Core no way to count builder bots: its vision is
        r^2 = 36 while builders work far outside it, get_unit_count() lumps
        Core, builders and every turret into one number, and the cost scale is
        a single team-wide float that cannot be inverted into a count.  Two
        independent lower bounds are available for a handful of engine calls,
        and the larger of the two is taken because both err the same way:

          (a) spawned minus deaths.  self.n counts builders spawned; lost_units
              counts ALL unit deaths, turrets included, so every turret we lose
              is charged to this bound as a phantom builder death.
          (b) units minus everything that is not a builder.  A "unit" is the
              Core, a builder, a Gunner, a Sentinel or a Launcher, so
              units - 1 - turrets - launcher is exact IF the turret count is
              exact; SLOT_HOME_GUN is monotone (never decremented, rubble still
              counts), so this bound is also depressed, by turret DEATHS.

        Under-reporting means over-spawning, bounded three ways: by pop_floor
        itself (each spawn raises bound (a) by one, so the refill closes), by
        spawn_budget = spawn_cap + REPLACEMENT_MAX above it, and by the bank.
        Over-reporting is the dangerous direction and neither bound can do it.
        """
        by_deaths = self.n - self.lost_units
        by_census = units - 1 - weapons - (1 if ct.read_store(SLOT_LAUNCHER) else 0)
        return max(0, by_deaths, by_census)

    def _note_friendly_launcher(self, ct):
        if ct.read_store(SLOT_LAUNCHER):
            return
        for eid in ct.get_nearby_buildings():
            if ct.get_team(eid) == self.team and ct.get_entity_type(eid) == EntityType.LAUNCHER:
                ct.write_store(SLOT_LAUNCHER, 1)
                return

    def _sync_harvesters(self, ct):
        if self.core is None:
            return
        p = ct.get_position()
        if p.distance_squared(self.core) > 64:
            return
        live = 0
        for eid in ct.get_nearby_buildings():
            if ct.get_team(eid) == self.team and ct.get_entity_type(eid) == EntityType.HARVESTER:
                live += 1
        # A builder only sees a local slice of the map.  Never erase the global
        # lower bound merely because distant harvesters are outside its vision.
        if live > ct.read_store(SLOT_HARVESTERS):
            ct.write_store(SLOT_HARVESTERS, live)
        if live >= ECO_NEED:
            ct.write_store(SLOT_ECO_READY, 1)

    def _eco_spendable(self, ct, cost):
        """Economy funding check, siege-reserved (see SIEGE_HEAL_RESERVE_TI).

        Under siege the ECONOMY paths stop spending the last
        SIEGE_HEAL_RESERVE_TI, so the heal line and the hunt pecks always
        have a till to draw on.  Defense spending is deliberately NOT routed
        through here -- heals, pecks, counterbattery, barriers, the ammo
        conversion and the surge all keep spending to the last titanium,
        because the reserve exists FOR them.

        Both gates are load-bearing.  Sieges land late (the HUNT_MIN_RND
        class logic: kladde sentinels r195/r308, Lunds chip sieges r150-900,
        rushes decided before ~r120), so the round floor conjoined with
        SLOT_UNDER means the reserve can never tax the opening bootstrap --
        the failure the _v70ec reserve/rebuild-cap already measured, gating
        link spending inverted the income bootstrap, collected 9390 -> 3160
        -- nor any rush window.
        """
        ti = ct.get_global_resources()
        if (
            SIEGE_RESERVE_ON
            and ct.read_store(SLOT_UNDER) != 0
            and ct.get_current_round() >= HUNT_MIN_RND
        ):
            return ti >= cost + SIEGE_HEAL_RESERVE_TI
        return ti >= cost

    def _try_build_launcher(self, ct):
        """Only call from defend — claim store first to prevent multi-launcher."""
        if ct.read_store(SLOT_LAUNCHER):
            return False
        for eid in ct.get_nearby_buildings():
            if ct.get_team(eid) == self.team and ct.get_entity_type(eid) == EntityType.LAUNCHER:
                ct.write_store(SLOT_LAUNCHER, 1)
                return False
        if ct.read_store(SLOT_HARVESTERS) < 1:
            return False
        if not self._eco_spendable(ct, ct.get_launcher_cost()):
            return False
        # Claim BEFORE build so later units this round skip
        ct.write_store(SLOT_LAUNCHER, 1)
        p = ct.get_position()
        # PLANK HS (b-rev): launchers are bot-impassable -- never seat one on
        # the 8 core-orthogonal heal seats.  Deliberately the FULL seat set,
        # not _seat_ban(): that helper exempts the <=2 delivery termini so
        # conveyors can end there, but an impassable launcher on a terminus
        # kills the terminus outright.  Corpus-wide evidence for this gate:
        # ungated launcher placement was the most frequent impassable seat
        # blocker (bleed doc s10); worker report ranked it top flag.
        lban = None
        if HS_SEAT_PROTECT_ON and self.core is not None and self.mw and self.mh:
            lban = {(s.x, s.y) for s in heal_seats(self.core, self.mw, self.mh)}
        for d in DIRECTIONS:
            bp = p.add(d)
            if lban and (bp.x, bp.y) in lban:
                continue
            if 0 <= bp.x < self.mw and 0 <= bp.y < self.mh and ct.can_build_launcher(bp):
                ct.build_launcher(bp)
                return True
        # Build failed — release claim so we retry next turn
        ct.write_store(SLOT_LAUNCHER, 0)
        return False

    def _builder(self, ct):
        p = ct.get_position()
        if self.team is None:
            self.team = ct.get_team()
            self.mw, self.mh = ct.get_map_width(), ct.get_map_height()
            # B8 sensing tier, decided once from dimensions alone -- no store
            # slot, no map decode, so it is safe this early in the turn.
            _big_square = self.mw * self.mh >= 650 and self.mw == self.mh
            self.gun_sense = 100 if (B8_ON and _big_square) else 64
            self.b_sense = 36 if (B8_ON and _big_square) else 16
            self.idx = ct.get_id() & 0xFF
            self.ang = (self.idx % 8) * (math.pi / 4)
            n = ct.read_store(SLOT_ROLE_N)
            self.role_n = n
            small = self.mw * self.mh <= 220
            if n == 0:
                self.role = "saboteur"
            elif n <= 3:
                self.role = "expand"
            elif n == 4:
                self.role = "defend"
            else:
                # Sixth and later builder -- a replacement for a dead unit.
                # Generic expander, deliberately: there is exactly one defend
                # seat (role_n == 4, with the role_n == 2 succession behind it)
                # and one interceptor seat (role_n == 1), and both are
                # single-occupancy by design -- a second defender would double
                # the counterbattery scan and a second interceptor would
                # abandon the economy in pairs.  The generic path is also where
                # the measured shortfall was: not enough hands laying
                # harvesters and conveyors.  This generalises the snowflake
                # role_n == 5 special case in _builder, which is now redundant
                # and left in place only as a no-op.
                self.role = "expand"
            ct.write_store(SLOT_ROLE_N, n + 1)

        if self.core is None:
            for eid in ct.get_nearby_buildings():
                if ct.get_entity_type(eid) == EntityType.CORE and ct.get_team(eid) == self.team:
                    self.core = ct.get_position(eid)
                    break
        if self.core is None:
            return

        if self.map_grid is None:
            self.map_grid = known_map_for(self.mw, self.mh, self.core, ct)
            if self.map_grid is not None:
                self.map_walls = {
                    (x, y) for y, row in enumerate(self.map_grid)
                    for x, cell in enumerate(row) if cell == "#"
                }
                self.map_ores = [
                    Position(x, y) for y, row in enumerate(self.map_grid)
                    for x, cell in enumerate(row) if cell == "o"
                ]
                # Decided once, from the decoded grid: on an open map the
                # forward gun duel is won by shooting first, not repairing.
                # Unknown map (map_grid None) keeps the repair-first order.
                self.melee_first = (
                    len(self.map_walls) < MELEE_FIRST_MAX_WALL_FRAC * self.mw * self.mh
                )

        self._note_friendly_launcher(ct)

        # B8 phase 1b -- nearest-threat write.  The loop below has no break and
        # no ordering, so today the LAST qualifying sighting in iteration order
        # wins SLOT_THREAT.  At gun_sense 64 the candidates are all within 8
        # tiles of home and roughly interchangeable; at 100 a distant,
        # unanswerable sentinel can overwrite a near, actionable one every
        # round.  Store writes are buffered, so no cross-unit priority rule is
        # possible -- the fix has to be per-unit, and it is one list slot and
        # one comparison.  Under B8_ON we publish the sighting with the
        # smallest core-distance; UNDER/ATK_RND still latch on the first
        # qualifier.  With B8_ON off the old last-write-wins path is kept
        # byte-for-byte.
        _threat_best = None
        _threat_best_d = 0
        for eid in ct.get_nearby_entities():
            if ct.get_team(eid) == self.team:
                continue
            et = ct.get_entity_type(eid)
            ep = ct.get_position(eid)
            if et == EntityType.CORE:
                self.enemy = ep
                ct.write_store(SLOT_ENEMY_CORE, pack_pos(ep))
            d = self.core.distance_squared(ep)
            if (et in (EntityType.GUNNER, EntityType.SENTINEL) and d <= self.gun_sense) or (
                et == EntityType.BUILDER_BOT and d <= self.b_sense
            ):
                ct.write_store(SLOT_UNDER, 1)
                ct.write_store(SLOT_ATK_RND, ct.get_current_round())
                if B8_ON:
                    if _threat_best is None or d < _threat_best_d:
                        _threat_best, _threat_best_d = ep, d
                else:
                    ct.write_store(SLOT_THREAT, pack_pos(ep))
        if B8_ON and _threat_best is not None:
            ct.write_store(SLOT_THREAT, pack_pos(_threat_best))

        self.enemy = unpack_pos(ct.read_store(SLOT_ENEMY_CORE))
        self._sync_harvesters(ct)

        # The Launcher acknowledges the exact bot it threw.  Without this
        # handshake, a short intermediate throw leaves a launch-wait bot trying
        # to walk home, and nearest-bot selection can steal the economy builder.
        if ct.read_store(SLOT_LAUNCHED_ID) == ct.get_id() + 1:
            self.dropped = True
            self.role = "saboteur"
            # PIECE F: a thrown bot's trail memory is arbitrarily far away --
            # it did not walk here.  can_build_conveyor would fail safe on
            # adjacency anyway, but a stale pave_prev burns an engine call
            # every round until the next move overwrites it.
            if PAVE_TRAIL_ON:
                self.pave_prev = None
                self.pave_dir = None
                self.pave_rnd = -2

        rnd = ct.get_current_round()

        # DEFEND-ROLE SUCCESSION.  Placed here, before every role override
        # below, so a promoted unit is indistinguishable from a natural
        # defender for the rest of this turn and every turn after it.
        #
        # Only role_n == 2 may promote: role_n == 1 is the interceptor and
        # role_n == 3 turns saboteur by design, so 2 is the one pure expander
        # that can be spared.  There is deliberately no chain -- if the
        # successor dies too, the capability is lost again; a second hop would
        # cost a third builder on a map where we are already losing units.
        #
        # Exactly-once falls out of the guards themselves: promotion sets
        # role_n = 4, and the `self.role == "expand"` test is false forever
        # after (the promoted unit is "defend"), so the branch cannot re-fire.
        # The role test also excludes the one way a role_n == 2 unit stops
        # expanding on its own -- being thrown by a Launcher, after which it is
        # a dropped saboteur deep in enemy ground and the worst possible
        # candidate to recall as a home defender.
        #
        # beat == 0 means no defender has ever beaten (see SLOT_DEFEND_BEAT):
        # that is the opening, not a death, so it never promotes.  The stored
        # value is round + 1, hence beat - 1 is the round the beat was written.
        if self.role_n == 2 and self.role == "expand" and rnd > DEFEND_BEAT_MIN_RND:
            beat = ct.read_store(SLOT_DEFEND_BEAT)
            if beat and rnd - (beat - 1) > DEFEND_BEAT_STALE_RNDS:
                self.role_n = 4
                self.role = "defend"
                # Hand a CLEAN state to the defend machine, exactly as
                # _intercept's disengage hands one back to _expand: self.tgt
                # still holds an expansion target and self.stuck counted
                # rounds walking to it.  link_queue is positional and survives
                # untouched -- _defend consumes it itself.
                self.tgt = None
                self.stuck = 0
                self.wall = None

        # The heartbeat is keyed on role_n rather than on identity, so the
        # successor takes over writing it the same turn it promotes.  Written
        # unconditionally and this early because every later path in _builder
        # can return before reaching the bottom.
        if self.role_n == 4:
            ct.write_store(SLOT_DEFEND_BEAT, rnd + 1)

        if (
            self.role_n == 3 and self.role == "expand"
            and self.mw == 20 and self.mh == 26
            and (self.core.x, self.core.y) == (9, 6)
        ):
            self.role = "defend"
        replay_snowflake = (
            self.role_n == 3
            and self.mw == 26 and self.mh == 26
            and (self.core.x, self.core.y) in ((5, 5), (19, 19))
            and self.map_grid is not None and self.map_grid[0][0] == "."
        )
        snowflake_attack_now = (
            replay_snowflake
            and (
                (self.core.x == 5 and self.core.y == 5)
                or rnd >= 8
            )
        )
        if self.role == "expand" and snowflake_attack_now:
            self.role = "saboteur"
        # The fourth macro engineer becomes a second attacker once the initial
        # four-harvester shell exists.  Two others continue scaling economy.
        if (
            self.role == "expand" and self.role_n == 3 and not self.link_queue
            and ct.read_store(SLOT_HARVESTERS) >= 4 and rnd >= 12
        ):
            self.role = "saboteur"

        if self.role == "launchwait":
            if self.dropped:
                self.role = "saboteur"
            elif rnd >= 70 and not ct.read_store(SLOT_LAUNCHER) and self.role_n != 5:
                self.role = "saboteur"
            elif rnd >= LAUNCH_GIVEUP_RND:
                self.role = "saboteur"
            elif rnd - getattr(self, "launchwait_rnd", rnd) >= LAUNCH_STALL_RNDS:
                self.role = "saboteur"
                self.launch_block_until = rnd + 12

        # A Launcher that arrives just after the normal waiting cutoff can
        # recruit one of the original insertion roles back from walking duty.
        # The bound matches the give-up above: at 180 the two fought each other
        # every round to r199, which made the give-up dead code entirely.
        if (
            self.role == "saboteur" and not self.dropped and self.role_n >= 3
            and rnd < LAUNCH_GIVEUP_RND and ct.read_store(SLOT_LAUNCHER)
            and ct.read_store(SLOT_DROPPED) < 3
            and rnd >= getattr(self, "launch_block_until", 0)
        ):
            self.role = "launchwait"
            self.launchwait_rnd = rnd

        # Advertise before the emergency home-defense return below.  Otherwise
        # a melee visitor can prevent an already-adjacent waiter from ever
        # becoming visible to the Launcher.
        if self.role == "launchwait":
            self._offer_launch(ct)

        if self.last == p:
            self.stuck += 1
        else:
            self.stuck = 0
            self.wall = None
        self.last = p

        # TURRET HUNT, AHEAD OF THE HEAL.  This is the only interception point
        # the feature needs: the universal adjacent heal immediately below is
        # what claims the action for a converged expander AND for the defender
        # (_defend's own `shelled and _heal_core` branch is belt-and-braces
        # behind it, and _rank2_hold/_home_defend are only reached after it),
        # so sitting one line above it guarantees the hunter check runs before
        # every heal call in the file without touching any of those branches.
        # Deliberately NOT gated on the action cooldown, unlike the heal: a
        # hunter that still has to walk one tile must be able to do that on a
        # round it cannot act, or it would converge back toward the Core on
        # every other round and never arrive.
        #
        # The falling edge mirrors _expand's `converging` reset exactly.
        # _hunt_turret owns self.hunting outright -- it clears it at the top of
        # every call and re-arms it only while it has a live target -- so
        # "was hunting, is not any more" is the turret dying or leaving the
        # band, and self.tgt (a turret tile the heal/expand machines would
        # never have chosen) plus the stuck counters are cleared here, this
        # same turn, before anything downstream reads them.
        was_hunting = self.hunting
        if self._hunt_turret(ct):
            return
        if was_hunting and not self.hunting:
            self.tgt = None
            self.stuck = 0
            self.wall = None

        # UNIVERSAL ADJACENT HEAL.  Measured over three replays vs 1650-1750
        # teams, heals delivered to our own Core: 0, 0, 82 (+328 HP -- and the
        # 82 was the one win, the siege was survived).  The only difference
        # was whether the single role_n == 4 defender happened to be free that
        # round: healing was a role, not a reflex.  Make it proximity work --
        # any builder standing beside the Core repairs it, before any
        # melee/sabotage short-circuit below can claim the action.
        # The gate is deliberately the loose one, SLOT_UNDER != 0, i.e. any
        # threat level including mere spawn-tile proximity noise.  Noise is
        # free here: can_heal() checks "there's actually damage to repair"
        # (docs/reference/official-tutorials.md), so it refuses a full-HP
        # Core and the 1 Ti is only ever spent when HP is genuinely missing.
        # And when HP is missing, 1 Ti for +4 HP outvalues any alternative
        # action taken under fire.  _heal_core walks the 2x2 footprint and
        # lets can_heal() enforce orthogonal adjacency, so a builder that is
        # merely near the Core is unaffected.  _builder is reached only for
        # EntityType.BUILDER_BOT (see _dispatch), so the Core -- a building,
        # which cannot heal -- never takes this path itself.
        # PIECE J exempts exactly one caller from this heal: the role_n == 4
        # defender, while a threat sits in the home band with no live home
        # turret and the bank can afford the gun.  It is not skipping the heal
        # so much as deferring it one frame -- _defend's action phase still
        # falls back to _heal_core when the counterbattery cannot build -- so
        # nothing is lost on the rounds the exemption cannot be used.
        #
        # PIECE K'' adds a TRUNK arm beside this Core heal; the spend cap
        # (K_HEAL_BUDGET_ON) bounds the TRUNK ARM ONLY.  Three properties:
        #  1. THE SLOT_UNDER GATE STAYS ON THE CORE HEAL.  K v1 deleted it and
        #     was refuted for it -- 27-31% of builder turns spent topping up an
        #     unthreatened Core, ~15 pts vs opp_v63 and ~35 vs band_probe.
        #     can_heal() refusing a full-HP Core does not stand in for the
        #     gate: a Core one peck down is "damaged" and the priority block
        #     will then claim the turn for it on a quiet round.  The latch is
        #     the loose one (any threat level, 50-round decay), so a real siege
        #     is never gated out; it only excludes the peacetime rounds.
        #  2. THE TRUNK ARM IS *NOT* SIEGE-GATED, deliberately and asymmetrically
        #     so.  Its target is the farm raider that never comes near the Core
        #     at all -- the hive tape is ~1 conveyor per 10 rounds for 330
        #     rounds, entirely outside SLOT_UNDER -- and unlike the Core heal it
        #     has no "nothing is threatening this" failure case: a damaged
        #     conveyor is standing evidence that something already hit it.  It
        #     is the budget, not a round floor or a damage depth, that bounds
        #     it; v1's depth gate made this arm dead code in every game.
        #  3. THE CORE HEAL IS EXEMPT FROM THE CAP -- exact Eir 5.1 semantics,
        #     unbounded under siege, no ledger interaction.  K' (the capped
        #     variant) was refuted for the cap: builders went budget-dry by
        #     r10-27 under rush while the Core was still shelled -- ablation
        #     grid 2026-08-07: capped core arm ALONE scored band 56.7 where
        #     this exempt shape scores 95.0 and the K-off control 91.7.  The
        #     972-heal starvation case (v65 antler, Core heal starving piece
        #     H's r1000 arm) is thereby NOT fixed here -- it is 5.1's shipped
        #     behavior, retained knowingly; an ENDGAME_RND standdown on the
        #     Core arm is the parked follow-up candidate, not a ride-along.
        # With K off the original two lines run unchanged.
        if ct.get_action_cooldown() == 0:
            if K_HEAL_BUDGET_ON:
                # Piece J's exemption is left in EXACTLY its shipped state
                # space: it only ever ran while SLOT_UNDER was latched, so it
                # is asked only then here too.  That also keeps its ~dozen-call
                # live-gun scan off the rounds only the trunk arm visits.  When
                # it fires, the whole block stands down -- the defender needs
                # the turn to reach _try_counterbattery, and a trunk patch
                # would take it just as surely as the Core heal would.
                under = ct.read_store(SLOT_UNDER) != 0
                cb = under and self._cb_over_heal(ct)
                if under and not cb and self._heal_core(ct):
                    return
                if not cb and self._heal_budget_left(ct) > 0:
                    if self._heal_trunk(ct):
                        self.heal_spent += 1
                        return
            elif ct.read_store(SLOT_UNDER) != 0:
                if not self._cb_over_heal(ct) and self._heal_core(ct):
                    return

        # Distance from home is not evidence of a Launcher drop: long economy
        # chains routinely travel farther than nine tiles.  Only the explicit
        # launch handshake above may convert an expander into a dropped raider.

        snowflake_home_b = (
            self.mw == 26 and self.mh == 26
            and self.core.x == 19 and self.core.y == 19
            and self.map_grid is not None and self.map_grid[0][0] == "."
        )
        hive_home_a = (
            self.mw == 25 and self.mh == 25
            and self.core.x == 2 and self.core.y == 20
        )
        if snowflake_home_b and self.role_n == 5 and self.role == "defend":
            self.role = "expand"
        if (
            ct.read_store(SLOT_UNDER)
            and (
                (hive_home_a and self.role_n in (1, 2, 3))
                or (snowflake_home_b and self.role_n == 4)
            )
        ):
            self.link_queue = []
            self._rank2_hold(ct)
            return

        # Keep the proven forward artillery on the three layouts where a
        # melee recall loses more pressure than it saves.  Other layouts may
        # recall a nearby idle raider when builders actually reach the Core.
        keep_artillery_forward = (
            (self.mw == 21 and self.mh == 8 and self.core.x == 5)
            or (
                self.mw == 20 and self.mh == 26
                and (self.core.x, self.core.y) in ((9, 6), (9, 18))
            )
            or (
                self.mw == 14 and self.mh == 18
                and (self.core.x, self.core.y) in ((6, 4), (6, 12))
            )
        )
        if self.role in ("saboteur", "launchwait") and self.core and not keep_artillery_forward and p.distance_squared(self.core) <= 25:
            melee = False
            for eid in ct.get_nearby_entities():
                if ct.get_team(eid) == self.team:
                    continue
                if ct.get_entity_type(eid) != EntityType.BUILDER_BOT:
                    continue
                if self.core.distance_squared(ct.get_position(eid)) <= 20:
                    melee = True
                    break
            if melee:
                self._home_defend(ct)
                return

        # Phase boundary: everything above this point is sensing/bookkeeping
        # (role/team/core/map setup, launcher handshake, enemy detection,
        # the melee emergency check just above) and every self.* write in it
        # is a standalone assignment, never split across an engine call. If
        # that alone already used the budget, skip this unit's action/move
        # phase below instead of risking a truncation mid-build inside it
        # (siege planning, the counterbattery scan, and BFS nav all live
        # there). Emergency defense above (_rank2_hold, _home_defend) is
        # intentionally NOT gated by this -- it is the highest-priority work
        # a unit does, not the lowest.
        if self._cpu_exhausted(ct):
            return

        # SIPHON HYGIENE, wire arm (see SIPHON_WIRE_ON).  Pure bookkeeping --
        # it plans a path at most, never acts -- so it sits here, after the CPU
        # gate above and ahead of every role, rather than being duplicated into
        # _expand and _defend (both of which build harvesters).
        self._wire_tick(ct)

        if self.role == "defend":
            self._defend(ct)
        elif self.role == "saboteur":
            self._saboteur(ct)
        elif self.role == "launchwait":
            self._launchwait(ct)
        else:
            self._expand(ct)

    def _home_defend(self, ct):
        """All hands: melee attackers, plant sentinel/barrier, heal Core."""
        p = ct.get_position()
        if ct.get_action_cooldown() == 0:
            if self._sabotage_prio(ct):
                pass
            elif self._try_counterbattery(ct):
                pass
            elif self._heal_core(ct):
                pass
        if ct.get_move_cooldown() != 0:
            return
        # Move onto enemy bots near Core
        threat = None
        best = 10**9
        for eid in ct.get_nearby_entities():
            if ct.get_team(eid) == self.team:
                continue
            ep = ct.get_position(eid)
            if self.core.distance_squared(ep) > 36:
                continue
            d = p.distance_squared(ep)
            if d < best:
                best, threat = d, ep
        if threat is not None:
            self.tgt = threat
        else:
            # PLANK HS, MECHANISM 2 (see HS_HEAL_DETAIL_ON).  No melee target in
            # the home band left this all-hands responder walking at the Core
            # itself; if the Core is provably bleeding, walk at a seat it can
            # heal from instead.  The shelling test is asked only on the
            # no-threat fallback, which is the rare branch here -- this method is
            # entered because an enemy builder is near home in the first place.
            seat = self._seat_seek_target(ct) if self._core_shelled(ct) else None
            self.tgt = self.core if seat is None else seat
        self._nav(ct, pave=False)

    def _rank2_hold(self, ct):
        """Map-gated ranged-battery response: return and repair the Core."""
        if ct.get_action_cooldown() == 0 and self._heal_core(ct):
            return
        if ct.get_move_cooldown() == 0:
            self.tgt = self.core
            self._nav(ct, pave=False)

    def _duel_safe(self, ct, tpos, tid):
        """True if melee-attacking the turret at tpos is a fight we may take.

        Safe iff any of: (a) it is nearly dead (HUNT_FINISH_HP -- finishing
        always pays); (b) a second friendly builder stands adjacent to it
        (volume wins the trade -- fjordgate's 348-hit grind); (c) its
        current firing ray does not cover this builder's tile (a turret
        shelling something else is free to peck -- the same fact
        _hunt_turret already exploits for Core-shelling turrets).
        Unknown/out-of-vision facing reads as UNSAFE.
        """
        if not DUEL_DISCIPLINE_ON:
            return True
        if tid is None:
            return True
        try:
            et = ct.get_entity_type(tid)
        except Exception:
            return False
        # Only guns duel back.  Everything else -- Core, harvester, conveyor,
        # barrier, Launcher -- is a free target and keeps its old priority.
        if et not in (EntityType.GUNNER, EntityType.SENTINEL):
            return True
        # (a) Four pecks or fewer from dead: finishing it always pays.
        try:
            if ct.get_hp(tid) <= HUNT_FINISH_HP:
                return True
        except Exception:
            pass
        # (b) Volume.  Any OTHER friendly builder already orthogonally on it
        # means the grind is shared and the trade flips our way.
        me = ct.get_id()
        for d in CARDINALS:
            n = tpos.add(d)
            if not (0 <= n.x < self.mw and 0 <= n.y < self.mh):
                continue
            try:
                oid = ct.get_tile_builder_bot_id(n)
            except Exception:
                continue
            if oid is not None and oid != me:
                try:
                    if ct.get_team(oid) == self.team:
                        return True
                except Exception:
                    continue
        # (c) Ray test.  No readable facing (no direction, or out of vision)
        # is the unsafe answer: we cannot prove the gun is pointed away.
        try:
            facing = ct.get_direction(tid)
        except Exception:
            return False
        dx, dy = facing.delta()
        if dx == 0 and dy == 0:
            return True
        p = ct.get_position()
        # Attack radii squared: Gunner 13, Sentinel 32.  Both walks are <= 5
        # tiles, so this stays cheap enough for the hot path.
        rng = 32 if et == EntityType.SENTINEL else 13
        x, y = tpos.x, tpos.y
        while True:
            x += dx
            y += dy
            if not (0 <= x < self.mw and 0 <= y < self.mh):
                return True
            if (x - tpos.x) ** 2 + (y - tpos.y) ** 2 > rng:
                return True
            if x == p.x and y == p.y:
                return False
            if et == EntityType.SENTINEL:
                # The Sentinel line ignores obstacles, so nothing between us
                # can shield the peck -- keep walking to our own tile.
                continue
            n = Position(x, y)
            try:
                blocked = (
                    ct.get_tile_building_id(n) is not None
                    or ct.get_tile_builder_bot_id(n) is not None
                )
            except Exception:
                # Out of vision: assume something stands there and eats the
                # shot.  The Gunner's ray stops before reaching us.
                blocked = True
            if blocked:
                return True

    def _sabotage_prio(self, ct):
        p = ct.get_position()
        best, best_p = None, 99
        for d in CARDINALS:
            t = p.add(d)
            if not (0 <= t.x < self.mw and 0 <= t.y < self.mh):
                continue
            bid = ct.get_tile_building_id(t)
            if bid is None or ct.get_team(bid) == self.team:
                continue
            et = ct.get_entity_type(bid)
            pr = {
                EntityType.GUNNER: 0, EntityType.SENTINEL: 0,
                EntityType.CORE: 1, EntityType.HARVESTER: 2,
                EntityType.LAUNCHER: 3, EntityType.CONVEYOR: 4,
                EntityType.SPLITTER: 4, EntityType.BARRIER: 5,
            }.get(et, 6)
            if et in (EntityType.GUNNER, EntityType.SENTINEL) and not self._duel_safe(ct, t, bid):
                # Piece D: a duel we would lose alone.  Skip the candidate
                # entirely so the loop falls through to the next-best target
                # (Core, harvester, conveyor, ...) instead of trading 1-for-1.
                continue
            if pr < best_p and ct.can_fire(t):
                best_p, best = pr, t
        if best is not None:
            ct.fire(best)
            return True
        return False

    def _launchwait(self, ct):
        p = ct.get_position()
        mine = ct.get_id() + 1
        chosen = self._offer_launch(ct)
        if ct.get_action_cooldown() == 0:
            if ct.read_store(SLOT_UNDER):
                self._sabotage_prio(ct)

        if ct.get_move_cooldown() != 0:
            return
        if chosen == mine:
            for eid in ct.get_nearby_buildings():
                if ct.get_team(eid) == self.team and ct.get_entity_type(eid) == EntityType.LAUNCHER:
                    # Path to any cardinal pickup cell around the occupied
                    # Launcher tile; only the explicitly claimed raider stages.
                    self.tgt = ct.get_position(eid)
                    self._nav(ct, pave=False)
                    return
        if p.distance_squared(self.core) > 12:
            self.tgt = self.core
        elif self.tgt is None or p == self.tgt or self.stuck >= 2:
            self.ang = (self.ang + 1.1) % (2 * math.pi)
            self.tgt = Position(
                max(0, min(self.core.x + int(2 * math.cos(self.ang)), self.mw - 1)),
                max(0, min(self.core.y + int(2 * math.sin(self.ang)), self.mh - 1)),
            )
        self._nav(ct, pave=False)

    def _offer_launch(self, ct):
        """Claim the single insertion slot and refresh it as a heartbeat."""
        mine = ct.get_id() + 1
        chosen = ct.read_store(SLOT_LAUNCH_ID)
        chosen_rnd = ct.read_store(SLOT_LAUNCH_RND)
        if chosen in (0, mine) or ct.get_current_round() - chosen_rnd > 4:
            ct.write_store(SLOT_LAUNCH_ID, mine)
            ct.write_store(SLOT_LAUNCH_RND, ct.get_current_round())
            return mine
        return chosen

    def _plan_siege(self, ct):
        """Choose a reachable tile whose weapon ray intersects the enemy Core."""
        if self.map_grid is None or self.enemy is None:
            return False
        cap = 3 if self.role_n == 0 else 2
        if self.forward_guns >= cap:
            return False
        if self.forward_guns >= 1 and ct.read_store(SLOT_HARVESTERS) < ECO_NEED:
            return False

        # Everything from here on is the expensive part of this function: a
        # full terrain flood plus a nested candidate search below. Nothing
        # has been written to self.siege_* yet (that only happens at the very
        # end, once a candidate is chosen), so bailing here is a clean no-op
        # -- identical in effect to the existing "no candidates found" path.
        if self._cpu_exhausted(ct):
            return False

        turret_type = (
            EntityType.SENTINEL
            if PRIMARY_SENTINEL and self.role_n == 0 and self.forward_guns == 0
            else EntityType.GUNNER
        )
        ranges = (5, 4) if turret_type == EntityType.SENTINEL else (3, 2)
        p = ct.get_position()
        blocked = set(self.map_walls)
        blocked.update((c.x, c.y) for c in core_tiles(self.core))
        blocked.update((c.x, c.y) for c in core_tiles(self.enemy))
        blocked.discard((p.x, p.y))

        # One terrain flood supplies a real route distance to every candidate;
        # this avoids choosing a geometrically close ray on the far side of a wall.
        dist = {(p.x, p.y): 0}
        q = deque([(p.x, p.y)])
        siege_bfs_steps = 0
        while q:
            x, y = q.popleft()
            siege_bfs_steps += 1
            if siege_bfs_steps % 64 == 0 and self._cpu_exhausted(ct):
                # Abandon planning for this round rather than run the
                # candidate search below on a starved budget. self.siege_*
                # is still untouched, so this is the same clean no-op as
                # the guard above.
                return False
            for d in CARDINALS:
                n = Position(x, y).add(d)
                key = (n.x, n.y)
                if (
                    key in dist or key in blocked
                    or not (0 <= n.x < self.mw and 0 <= n.y < self.mh)
                ):
                    continue
                dist[key] = dist[(x, y)] + 1
                q.append(key)

        reserved = unpack_pos(ct.read_store(SLOT_SIEGE))
        candidates = []
        seen = set()
        for target in core_tiles(self.enemy):
            for facing in DIRECTIONS:
                unit = Position(0, 0).add(facing)
                max_range = ranges[0] if facing in CARDINALS else ranges[1]
                for ray_len in range(max_range, 0, -1):
                    spot = Position(
                        target.x - unit.x * ray_len,
                        target.y - unit.y * ray_len,
                    )
                    skey = (spot.x, spot.y)
                    if (
                        not (0 <= spot.x < self.mw and 0 <= spot.y < self.mh)
                        or self.map_grid[spot.y][spot.x] != "."
                        or skey in blocked
                        or (
                            self.role_n != 0 and reserved is not None
                            and spot.x == reserved.x and spot.y == reserved.y
                        )
                    ):
                        continue
                    # A wall anywhere before the Core makes a gunner ray inert.
                    if any(
                        (spot.x + unit.x * step, spot.y + unit.y * step) in self.map_walls
                        for step in range(1, ray_len)
                    ):
                        continue
                    if ct.is_in_vision(spot) and ct.get_tile_building_id(spot) is not None:
                        continue
                    # Construction is cardinal-adjacent only.  A diagonal
                    # approach looks close but leaves the engineer idling
                    # forever because every can_build_* call remains false.
                    for ad in CARDINALS:
                        approach = spot.add(ad)
                        akey = (approach.x, approach.y)
                        key = (skey, akey, facing)
                        if (
                            key in seen or akey not in dist
                            or approach == spot
                            or akey in blocked
                        ):
                            continue
                        seen.add(key)
                        # Stand behind or beside the weapon, never in its ray.
                        ray_penalty = 20 if ad == facing else 0
                        terrain_penalty = 2 if self.map_grid[approach.y][approach.x] == "o" else 0
                        candidates.append((
                            dist[akey] + ray_penalty + terrain_penalty,
                            -ray_len, spot.x, spot.y, approach.x, approach.y,
                            spot, approach, facing,
                        ))
        if not candidates:
            return False
        candidates.sort(key=lambda row: row[:6])
        pick = 0 if self.role_n == 0 else min(2, len(candidates) - 1)
        row = candidates[pick]
        self.siege_spot, self.siege_approach, self.siege_direction = row[6:9]
        self.siege_type = turret_type
        return True

    def _try_siege_build(self, ct):
        if self.siege_spot is None and not self._plan_siege(ct):
            return False
        p = ct.get_position()
        spot = self.siege_spot
        if ct.is_in_vision(spot) and ct.get_tile_building_id(spot) is not None:
            self.siege_spot = self.siege_approach = self.siege_direction = self.siege_type = None
            return False
        if max(abs(p.x - spot.x), abs(p.y - spot.y)) > 1 or p == spot:
            return False
        built = False
        if (
            self.siege_type == EntityType.SENTINEL
            and ct.get_global_resources() >= ct.get_sentinel_cost()
            and ct.can_build_sentinel(spot, self.siege_direction)
        ):
            ct.build_sentinel(spot, self.siege_direction)
            built = True
        elif (
            self.siege_type == EntityType.GUNNER
            and ct.get_global_resources() >= ct.get_gunner_cost()
            and ct.can_build_gunner(spot, self.siege_direction)
        ):
            ct.build_gunner(spot, self.siege_direction)
            built = True
        if built:
            self.forward_guns += 1
            ct.write_store(SLOT_HOME_GUN, ct.read_store(SLOT_HOME_GUN) + 1)
            if self.role_n == 0 and self.forward_guns == 1:
                ct.write_store(SLOT_SIEGE, pack_pos(spot))
            self.siege_spot = self.siege_approach = self.siege_direction = self.siege_type = None
            return True
        return False

    def _saboteur(self, ct):
        p = ct.get_position()
        ec = self.enemy or Position(self.mw // 2, self.mh // 2)

        if ct.get_action_cooldown() == 0:
            # Open maps only: melee a mid-map gun before spending the turn on
            # siege repair.  Wall-heavy maps keep the repair-first order.
            if self.melee_first and self._sabotage_prio(ct):
                return
            primary = unpack_pos(ct.read_store(SLOT_SIEGE))
            try:
                can_repair = primary is not None and ct.can_heal(primary)
            except Exception:
                can_repair = False
            if can_repair:
                ct.heal(primary)
                return
            # Persistent ray damage comes before low-value melee.  Once every
            # planned battery tile is occupied, clear hostile guns/economy.
            if self._try_siege_build(ct):
                return
            if not self.melee_first:
                self._sabotage_prio(ct)

        # Action phase over -- _try_siege_build either finishes its build and
        # the matching state update atomically and returns, or changes
        # nothing, so nothing here is half-set. Check before planning the
        # next siege spot and navigating below: both run their own BFS.
        if self._cpu_exhausted(ct):
            return

        if ct.get_move_cooldown() != 0:
            return

        if self.siege_spot is None:
            self._plan_siege(ct)
        if self.siege_approach is not None:
            if self.stuck >= 3:
                self.siege_spot = self.siege_approach = self.siege_direction = self.siege_type = None
                self._plan_siege(ct)
            self.tgt = self.siege_approach or ec
        elif self.forward_guns >= 1 and ct.read_store(SLOT_HARVESTERS) < ECO_NEED:
            self.tgt = p
        else:
            self.tgt = ec
        self._nav(ct, pave=False)

    def _eco_cap(self, ct):
        """ECO_CAP, surge-raised under the LATE LABOR SURGE gate (see its
        constants block): strictly-surplus bank, strictly late, so the normal
        harvester ceiling and its +5%/build scale curve are untouched in any
        game the surge does not reach."""
        if (
            ct.get_global_resources() >= SURGE_TI_FLOOR
            and ct.get_current_round() >= SURGE_MIN_RND
        ):
            return SURGE_ECO_CAP
        return ECO_CAP

    def _turret_on_harvester(self, ct, bp):
        """True if an enemy turret at bp stands orthogonally adjacent to a
        friendly HARVESTER (the eco-siege trigger; see the TWO HUNT MODES
        comment in _hunt_turret).  Neighbours of a visible turret can still
        sit outside our own vision, so every lookup fails safe to False."""
        for d in CARDINALS:
            n = bp.add(d)
            if not (0 <= n.x < self.mw and 0 <= n.y < self.mh):
                continue
            try:
                nid = ct.get_tile_building_id(n)
                if (
                    nid is not None
                    and ct.get_team(nid) == self.team
                    and ct.get_entity_type(nid) == EntityType.HARVESTER
                ):
                    return True
            except Exception:
                continue
        return False

    def _eco_besieged(self, ct):
        """Any visible enemy turret point-blank on a friendly harvester."""
        for bid in ct.get_nearby_buildings():
            if ct.get_team(bid) == self.team:
                continue
            if ct.get_entity_type(bid) not in (EntityType.GUNNER, EntityType.SENTINEL):
                continue
            if self._turret_on_harvester(ct, ct.get_position(bid)):
                return True
        return False

    def _healer_floor(self, ct):
        """HUNT_MIN_HEALERS, scaled down for cornered cores (see the healer
        floor comment in _hunt_turret).  Counts the in-bounds orthogonal
        neighbours of the 2x2 footprint once per call -- eight for an
        interior core, as few as four in a corner -- and demands 2 standing
        healers only when at least six seats exist."""
        seats = 0
        seen = set()
        for c in core_tiles(self.core):
            for d in CARDINALS:
                n = c.add(d)
                if (n.x, n.y) in seen:
                    continue
                seen.add((n.x, n.y))
                if 0 <= n.x < self.mw and 0 <= n.y < self.mh and dist_core(n, self.core) > 0:
                    seats += 1
        return HUNT_MIN_HEALERS if seats >= 6 else 1

    def _seat_ban(self):
        """PLANK HS: heal-seat keys this unit may never build on, or None.

        None is the "no ban" answer every gated call site is written to fall
        through on, so with HS_SEAT_PROTECT_ON off -- or before the Core is
        located, or before the map dimensions are known -- every one of them
        runs its pre-plank code path unchanged.  Computed once per unit and
        frozen; see delivery_seats for why that is safe without coordination.
        """
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
        """PLANK HS: the seat ban as it applies to CONVEYORS specifically.

        Split from _seat_ban because the conveyor half of the ban rests on a
        weaker mechanism than the rest of it -- conveyors are bot-passable, so a
        paved seat is still standable (see the RED FLAG in the plank block) --
        and has to be ablatable on its own.  Turrets, harvesters and barriers
        keep asking _seat_ban directly.
        """
        return self._seat_ban() if HS_SEAT_BAN_CONVEYORS else None

    def _free_seats(self, ct):
        """PLANK HS: seats a builder could step onto and heal from, nearest first.

        Free means passable and unoccupied, which are two different questions in
        this engine: is_tile_passable answers only the first (can_move is
        documented as "passable AND unoccupied"), so the standing-bot test is
        explicit.  Passability is also exactly the right test for the building
        half -- a conveyor or splitter on a seat is walkable and the seat still
        heals, while a harvester, barrier, turret or wall on it is not and does
        not, so the engine draws the line this plank cares about for us.

        Vision is the usual trap: the tile getters raise for an in-bounds tile
        outside this unit's sight with the same error as an off-map one, so a
        seat we cannot read counts as NOT free and the caller falls back to its
        pre-plank target.  Sorted by walking distance from this unit, with the
        fixed seat order breaking ties.
        """
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
        """PLANK HS: the free heal seat this defender should walk to, or None.

        None means "keep the pre-plank target", which in every caller is
        self.core -- _bfs_direction expands that into "any unblocked seat", i.e.
        the generic adjacency this replaces.  The measured failure is not
        willingness to come home (the convergence machinery already does that)
        but arriving at a footprint whose free seats the walker never aimed at.

        CAP.  Never send more bodies than there are seats to stand on: every
        visible friendly builder inside the home band that is not already on a
        seat is counted as a rival seeker, and if they alone can fill the free
        seats this unit keeps its own job.  Deliberately local and deliberately
        pessimistic -- a store slot could not carry this anyway (writes are
        buffered a round) and over-counting only costs the pre-plank behaviour.
        """
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
        # d-rev: tie-break fix ONLY (the c-rev ablation — its turret-gate half
        # is parked refuted).  free[] re-sorts by this unit's own moving
        # position every round, so a walker shuffles between equidistant seats
        # and the abandoned one never backfills (decode-named, jackpot_1_a
        # -25 heals).  Two halves: a unit standing on a seat stops seeking
        # (pre-plank heal-in-place takes over); a walker holds its chosen
        # seat while that seat stays free.
        p = ct.get_position()
        if (p.x, p.y) in seats:
            return None
        held = getattr(self, "hs_seek_seat", None)
        if held is not None:
            for s in free:
                if (s.x, s.y) == held:
                    return s
        choice = free[0]
        self.hs_seek_seat = (choice.x, choice.y)
        return choice

    def _heal_core(self, ct):
        for tile in core_tiles(self.core):
            if ct.can_heal(tile):
                ct.heal(tile)
                return True
        return False

    def _heal_budget_left(self, ct):
        """PIECE K -- heal actions this unit may still take (see
        K_HEAL_BUDGET_ON).

        The Core publishes the income-proportional part of the TEAM budget in
        whole titanium; K_HEAL_BASE_GRANT is added here rather than there so
        the seed is available on round 0, when the buffered store still reads
        0 for a slot the Core writes this very round.  Each unit spends at most
        its own share, which is what makes the ledger safe without a team-wide
        counter no store slot can hold correctly.
        """
        allowance = (K_HEAL_BASE_GRANT + ct.read_store(SLOT_HEAL_BUDGET)) // K_HEAL_SHARES
        return allowance - self.heal_spent

    def _heal_trunk(self, ct):
        """PIECE K' -- repair a damaged economy building we are standing beside.

        The same repair _expand's chain medic performs, promoted out of the
        bottom of one role's action phase into the standing priority line,
        opened to round 0 and to every role, and paid for out of the caller's
        K_HEAL_SHARES budget rather than out of tempo.  Three of the medic's
        four gates are carried over; the fourth is the one K v1 died of.

         - MEDIC_TYPES only.  Turrets and barriers are combat capital with
           their own defense logic; the Core has its own heal above this one.
         - MEDIC_TI_FLOOR.  Below it every titanium belongs to the first
           harvesters and links.  This is a BANK gate, not a damage gate, and
           it stays: a 1 Ti heal taken out of a 19 Ti till is one nineteenth of
           the next conveyor, and the trunk we are patching is worthless
           without the links that bank buys.
         - PIECE H.  Past ENDGAME_RND a +4 HP patch scores in no tiebreak and
           the action is worth more as a harvester (tiebreak 2), so the trunk
           arm stands down exactly as _expand's medic already does.
         - NO DEPTH DISCRIMINATOR.  v1 required MEDIC_EARLY_MIN_DMG = 8 damage
           before MEDIC_MIN_RND and measured ZERO firings across the screening
           battery: the chip rates in this game are 2 (builder peck) and 7
           (gunner, reload 1) against a 20-HP conveyor, so a raided tile passes
           through that window rather than resting in it.  K' asks only
           "damaged at all", which is also all can_heal() itself asks, and
           leans on the budget for the bound the depth gate was supposed to
           provide.  The explicit HP compare is kept ahead of can_heal() purely
           as the cheap short-circuit -- two getters instead of a legality
           check -- and is deliberately identical in meaning to it.
        """
        rnd = ct.get_current_round()
        if ENDGAME_SWITCH_ON and rnd >= ENDGAME_RND:
            return False
        if ct.get_global_resources() < MEDIC_TI_FLOOR:
            return False
        p = ct.get_position()
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
                    and ct.get_hp(bid) < ct.get_max_hp(bid)
                    and ct.can_heal(bp)
                ):
                    ct.heal(bp)
                    return True
            except Exception:
                continue
        return False

    def _core_turret_mix(self, ct):
        """PIECE H -- which friendly Gunners/Sentinels are alive to drink ammo?

        Returns (gunners, sentinels).  Non-zero is the shipped live-turret GATE
        on the endgame dump, unchanged; the counts are the Eir 5.1 addition and
        size the dump (see the DUMP CAP block in _core).

        Called from _core only, so no band test is needed: the Core's own
        vision (r^2 = 36) already bounds it to the home cluster, which is where
        every counterbattery and home gun this file builds ends up.  A forward
        siege gun out of Core sight reads zero -- conservative in the right
        direction, since the endgame dump is spending tiebreak-3 stored
        titanium and should only do so on turrets we can actually see standing.
        SLOT_HOME_GUN cannot answer this: it is never decremented, so rubble
        and distant artillery both read as a live gun (see CB_OVER_HEAL_ON).

        Reads the team off the Controller rather than self.team: _core never
        populates self.team (it uses ct.get_team() inline throughout), so the
        cached attribute is None on the Core's own Player instance.
        """
        mine = ct.get_team()
        guns = sents = 0
        for bid in ct.get_nearby_buildings():
            try:
                if ct.get_team(bid) != mine:
                    continue
                et = ct.get_entity_type(bid)
                if et == EntityType.GUNNER:
                    guns += 1
                elif et == EntityType.SENTINEL:
                    sents += 1
            except Exception:
                continue
        return guns, sents

    def _live_home_gun(self, ct):
        """PIECE J -- is a friendly turret standing in the home band RIGHT NOW?

        The live replacement for `ct.read_store(SLOT_HOME_GUN) >= 1` at the two
        gates that mean "home defense exists" (see CB_OVER_HEAL_ON).  That
        counter is incremented at three sites, one of them the saboteur's
        FORWARD gun at the enemy Core, and never decremented, so it answers
        "did we ever build a turret anywhere" -- rubble and distant artillery
        both read as home defense.  This asks the question the gates actually
        want, off live observation, using the band constant those gates already
        share (HUNT_BAND_DSQ = 41, footprint-measured, twice validated).

        Vision-bounded by construction: get_nearby_buildings returns only what
        this unit can see, so it is only meaningful for a unit standing near
        home -- which is exactly who calls it.  A caller far from the Core gets
        False, i.e. "no home gun I can vouch for", which is the conservative
        answer for both call sites.
        """
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

    def _cb_over_heal(self, ct):
        """PIECE J -- may THIS builder skip a heal to buy a counterbattery?

        True only in the one state where healing provably cannot win: the
        role_n == 4 defender, a threat inside the home band, no live home
        turret, and a bank that can pay for a Sentinel without touching
        SIEGE_HEAL_RESERVE_TI.  See CB_OVER_HEAL_ON for why every clause is
        load-bearing and why this is not a blanket heal/dispatch reorder.

        Ordered cheapest-first: two store reads, then a bank read, and only
        then the ~dozen-call live scan, so a defender that fails any earlier
        clause never pays for the scan.
        """
        if not CB_OVER_HEAL_ON or self.role_n != 4 or self.core is None:
            return False
        threat = unpack_pos(ct.read_store(SLOT_THREAT))
        if threat is None:
            return False
        # The same reach test _try_counterbattery uses: past this band no
        # turret we could build against our own footprint reaches the threat,
        # so skipping the heal would buy literally nothing.
        if min(t.distance_squared(threat) for t in core_tiles(self.core)) > HUNT_BAND_DSQ:
            return False
        if ct.get_global_resources() < ct.get_sentinel_cost() + SIEGE_HEAL_RESERVE_TI:
            return False
        return not self._live_home_gun(ct)

    def _core_shelled(self, ct):
        """True only when our Core is visible AND standing below full HP.

        Direct observation rather than the store.  SLOT_UNDER is a proximity
        flag written from several call sites and cannot tell "an enemy is
        loitering near home" from "the Core is being shot"; a Core below its
        max HP is proof of the latter.  Vision is the trap: get_tile_env,
        is_tile_passable and get_tile_building_id all raise GameError for an
        in-bounds tile outside the caller's vision (docs/game-model.md), with
        the same message as an off-map tile, so the anchor Position cannot be
        queried directly.  get_nearby_buildings returns only what is visible,
        so the scan below never raises -- it is exactly the idiom _builder
        already uses to find the Core in the first place.  Out of vision
        returns False, which is the right answer for both callers: a defender
        that cannot see the Core cannot heal it or usefully judge it either.
        """
        for eid in ct.get_nearby_buildings():
            if ct.get_entity_type(eid) == EntityType.CORE and ct.get_team(eid) == self.team:
                return ct.get_hp(eid) < ct.get_max_hp(eid)
        return False

    def _hunt_turret(self, ct):
        """Peck a near-Core enemy turret instead of healing.  True == turn spent.

        See the TURRET-HUNTING UNDER SIEGE block at the top of this file for
        the measured motivation and for why every one of the gates below is
        there.  Also maintains self.hunting, which _builder reads to detect the
        falling edge; this method is its sole owner, so it is cleared on entry
        and re-armed only while a live target is held.

        Return value is "this turn was spent hunting", NOT "a target exists":
        a hunter that is two tiles out on a round its move cooldown is not zero
        keeps self.hunting set but returns False, so the universal heal below
        can still use the round.  That split is what keeps the state sticky and
        the builder off the converge/hunt oscillation.
        """
        self.hunting = False
        if self.core is None:
            return False
        # Same seats that heal under siege, and only those.  role_n == 1 is the
        # single interceptor and role_n == 0 the siege engineer (role
        # "saboteur"), and both already have their own melee paths; pulling
        # either onto a home turret would cost the capability it exists for.
        if self.role not in ("defend", "expand") or self.role_n == 1:
            return False
        # TWO HUNT MODES (Eir 2).  CORE-SIEGE mode is the shipped v55/Eir
        # behaviour, all gates unchanged: round floor 120, SLOT_UNDER, and
        # direct Core-HP evidence.  ECO-SIEGE mode is new, from the meander
        # r133 loss to Lunds v41: a forward Gunner planted at r69
        # orthogonally beside our harvester killed it at r74 and then farmed
        # every rebuilt conveyor on that link for 60 rounds -- and NEITHER
        # gate could ever answer it: the Core was not bleeding (shelled gate)
        # and the clock was pre-120 (floor).  A turret standing orthogonally
        # adjacent to a friendly HARVESTER is not ambient threat, it is an
        # active point-blank siege of a named asset, and it is huntable at
        # any round with no Core evidence.  STRICT harvester-only adjacency
        # on purpose: conveyor-adjacency would re-open the refuted early
        # ambient hunting on conveyor-dense boards (the eider 8/16 -> 0/16
        # ablation and the fjordgate rush regression both came from exactly
        # that), while a turret parked beside a harvester is unambiguous.
        core_siege = (
            ct.get_current_round() >= HUNT_MIN_RND
            and ct.read_store(SLOT_UNDER) != 0
        )
        # Nothing has been written yet, so bailing here is a clean no-op that
        # degrades to exactly the pre-existing behaviour (heal / converge).
        if self._cpu_exhausted(ct):
            return False
        if core_siege and not self._core_shelled(ct):
            core_siege = False
        eco_mode = not core_siege
        if eco_mode:
            # Only proceed if some visible enemy turret is point-blank on a
            # friendly harvester; the candidate loop re-checks per turret.
            if not self._eco_besieged(ct):
                return False

        p = ct.get_position()
        me = ct.get_id()

        # Candidate turrets: visible enemy Gunners/Sentinels inside the siege
        # band around our Core anchor AND already within our own designation
        # radius.  The second test is not an optimisation -- a builder outside
        # HUNT_DESIGNATE_DSQ is not in the designation set at all, so it could
        # never win the id ballot below -- but it does keep the friendly scan
        # off the wire for every builder that is merely near a shelled Core.
        cands = []
        for bid in ct.get_nearby_buildings():
            if ct.get_team(bid) == self.team:
                continue
            if ct.get_entity_type(bid) not in (EntityType.GUNNER, EntityType.SENTINEL):
                continue
            bp = ct.get_position(bid)
            if eco_mode:
                # ECO-SIEGE: the turret qualifies by what it is doing, not by
                # where it is on the map -- orthogonally adjacent to a
                # friendly harvester, at any range from the Core.
                if not self._turret_on_harvester(ct, bp):
                    continue
            else:
                # CORE-SIEGE band, sized past Sentinel range (r^2 = 32),
                # measured to the nearest tile of the 2x2 footprint.
                # Validated twice: the CtrlAltDefeat decode (sentries
                # shelling from dist^2 25-41, outside the old anchor-measured
                # 20) and the v79 jackpot sweep (sentinel at EXACTLY dsq 32
                # on the diagonal, killed our core with 60 unanswered shots
                # while a builder stood orthogonally adjacent to it).
                if min(t.distance_squared(bp) for t in core_tiles(self.core)) > HUNT_BAND_DSQ:
                    continue
            if p.distance_squared(bp) > HUNT_DESIGNATE_DSQ:
                continue
            cands.append((ct.get_hp(bid), p.distance_squared(bp), bid, bp))
        if not cands:
            return False
        # Weakest first: a turret one peck from dead is worth strictly more
        # than a fresh one, and it is also the only kind HUNT_FINISH_HP lets a
        # lone builder take on.  Distance and id only break ties, so the order
        # is total and deterministic.
        cands.sort(key=lambda row: row[:3])

        # One pass for both remaining questions -- who else is in the ballot,
        # and whether the repair line is still manned.
        mates = []
        for uid in ct.get_nearby_units():
            if uid == me or ct.get_team(uid) != self.team:
                continue
            if ct.get_entity_type(uid) != EntityType.BUILDER_BOT:
                continue
            mates.append((uid, ct.get_position(uid)))
        homes = core_tiles(self.core)
        healers = 0
        for _uid, up in mates:
            if any(abs(up.x - c.x) + abs(up.y - c.y) == 1 for c in homes):
                healers += 1

        # Prune ledger entries for turrets no longer in the candidate set, so
        # a turret that died or left the band does not leave a stale row.
        live_bids = {row[2] for row in cands}
        for stale in [b for b in self.hunt_defer if b not in live_bids]:
            del self.hunt_defer[stale]

        for hp, _d, bid, bp in cands:
            # Designation: lowest entity id inside HUNT_DESIGNATE_DSQ of THIS
            # turret wins it.  Anyone lower that we can see takes it from us --
            # but only for as long as the deference provably works.  See the
            # BALLOT DEADLOCK BREAKER block at the top of the file: if the
            # turret's HP has not dropped for our own staggered override
            # window, the elected unit is not actually hunting (or the turret
            # is escort-healed as fast as it is pecked, which wants more
            # attackers anyway), and the ballot stops binding us.
            if any(
                uid < me and up.distance_squared(bp) <= HUNT_DESIGNATE_DSQ
                for uid, up in mates
            ):
                stalled, last_hp = self.hunt_defer.get(bid, [0, None])
                if last_hp is not None and hp < last_hp:
                    stalled = 0
                else:
                    stalled += 1
                self.hunt_defer[bid] = [stalled, hp]
                if stalled <= HUNT_DEFER_BASE + (me % HUNT_DEFER_SPREAD):
                    continue
            else:
                self.hunt_defer.pop(bid, None)
            # Corner cores can't man HUNT_MIN_HEALERS: a corner 2x2 footprint
            # has only 4 in-bounds orthogonal neighbours against an interior
            # core's 8, so demanding 2 standing healers before anyone hunts
            # is unsatisfiable exactly where the core is most cornered.
            # Measured on the v79 jackpot sweep: the healer floor (not the
            # band) kept an adjacent builder from ever pecking the killer
            # sentinel.  The floor scales with the seats that can exist.
            # The healer floor protects the Core's repair line; an eco-siege
            # target has no repair line to protect (the besieged harvester is
            # dead or doomed either way -- killing the gun is the only play).
            if not eco_mode and healers < self._healer_floor(ct) and hp > HUNT_FINISH_HP:
                continue

            if abs(p.x - bp.x) + abs(p.y - bp.y) == 1:
                # Orthogonally adjacent: peck and hold, exactly as _intercept
                # holds its guard tile.  The turn is owned even on a round the
                # peck cannot be paid for or the cooldown forbids it -- the
                # alternative is drifting back toward the Core under the
                # convergence rule and walking the same tile again next round.
                # A turret shelling the Core does not return fire on whatever
                # is standing beside it, so holding here is free.
                self.hunting = True
                if (
                    ct.get_action_cooldown() == 0
                    and ct.get_global_resources() >= HUNT_FIRE_TI
                    and ct.can_fire(bp)
                ):
                    ct.fire(bp)
                return True

            # One to three tiles out.  _nav's BFS treats an enemy turret tile
            # as blocked and therefore aims at its cardinal neighbours, which
            # is precisely the adjacency the peck needs; no special-casing.
            self.hunting = True
            if ct.get_move_cooldown() == 0:
                self.tgt = bp
                self._nav(ct, pave=False)
                return True
            return False
        return False

    def _try_counterbattery(self, ct):
        """Build only a weapon ray that already contains the reported threat."""
        threat = unpack_pos(ct.read_store(SLOT_THREAT))
        if threat is None:
            return False
        # B8 phase 1b -- reach test.  A Sentinel is r^2=32, so a turret built
        # against our own footprint cannot reach a threat past footprint-dsq
        # ~44: every can_fire_from below returns False and the scan burns its
        # full ~128-256 engine calls for nothing, every defender turn, for up
        # to the 50 rounds the UNDER latch holds.  Widening the sensing tier is
        # exactly what starts publishing threats that far out, so the reach
        # test ships with it.  HUNT_BAND_DSQ = 41 is the already-measured,
        # twice-validated "past Sentinel range, footprint-measured" constant in
        # this file rather than a new number.  Net CPU effect is negative.
        if B8_ON and min(
            t.distance_squared(threat) for t in core_tiles(self.core)
        ) > HUNT_BAND_DSQ:
            return False
        # Mirror of _plan_siege's economy gate: the first emergency battery is
        # free, any further one waits for income.  Ungated, opening threat noise
        # on close-anchor maps buys three fixed-facing Sentinels aimed at
        # transient spawn tiles before the first harvester exists.
        # PIECE J: "a home gun already stands" is what this gate means, so it
        # asks the live scan rather than the monotone SLOT_HOME_GUN counter,
        # which also counts the saboteur's forward gun at the ENEMY core and
        # counts rubble forever.  Harvester test first -- it is a store read,
        # the scan is a dozen engine calls.
        if ct.read_store(SLOT_HARVESTERS) < ECO_NEED and (
            self._live_home_gun(ct) if CB_OVER_HEAL_ON
            else ct.read_store(SLOT_HOME_GUN) >= 1
        ):
            # ...unless the Core is provably BLEEDING.  The gate exists for
            # close-anchor opening noise (transient spawn-tile threats buying
            # three sentinels aimed at nothing), but on meander v79 shelled
            # our base from r7-r9 while this gate held our counterbattery
            # shut until harvester 3 landed at r130 -- we finished with ZERO
            # turrets alive after r299 against his 804 shots.  Real core
            # damage is not noise: _core_shelled is direct HP-bar evidence,
            # the same test every heal path trusts.  (A rich-bank floor on
            # this waiver was tried and refuted: both the CAD insertion and
            # the meander duel open on a still-rich bank, so the floor
            # separated nothing and cost meander games.)
            if not self._core_shelled(ct):
                return False
        p = ct.get_position()
        # PLANK HS (see HS_SEAT_PROTECT_ON).  Hoisted out of the double loop: it
        # is a cached frozenset after the first call, and the placement scan
        # below is the one site in the file that most reliably stands a builder
        # beside its own Core with a turret to place.
        ban = self._seat_ban()
        choices = (
            (
                (EntityType.SENTINEL, ct.get_sentinel_cost()),
                (EntityType.GUNNER, ct.get_gunner_cost()),
            )
            if PRIMARY_SENTINEL else
            (
                (EntityType.GUNNER, ct.get_gunner_cost()),
                (EntityType.SENTINEL, ct.get_sentinel_cost()),
            )
        )
        for turret_type, cost in choices:
            if ct.get_global_resources() < cost:
                continue
            for d in DIRECTIONS:
                # Nothing here is written to self/the store until a build
                # actually succeeds a few lines down, so bailing between
                # candidates is clean. Checked once per `d`, not per
                # `facing` (the innermost loop), to keep the check itself
                # infrequent relative to the up-to-8 engine calls per `d`.
                if self._cpu_exhausted(ct):
                    return False
                bp = p.add(d)
                if not (0 <= bp.x < self.mw and 0 <= bp.y < self.mh):
                    continue
                # PLANK HS: a turret is impassable, so one planted on a heal
                # seat costs that seat's +4 HP/round for the rest of the match
                # -- the worst trade on the board when the reason we are
                # building it is that the Core is already bleeding.  Every other
                # tile in this scan is still offered, so a counterbattery that
                # has any legal ray at all still gets built.
                if ban is not None and (bp.x, bp.y) in ban:
                    continue
                for facing in DIRECTIONS:
                    try:
                        aligned = ct.can_fire_from(bp, facing, turret_type, threat)
                    except Exception:
                        aligned = False
                    if not aligned:
                        continue
                    if turret_type == EntityType.SENTINEL and ct.can_build_sentinel(bp, facing):
                        ct.build_sentinel(bp, facing)
                        ct.write_store(SLOT_HOME_GUN, ct.read_store(SLOT_HOME_GUN) + 1)
                        return True
                    if turret_type == EntityType.GUNNER and ct.can_build_gunner(bp, facing):
                        ct.build_gunner(bp, facing)
                        ct.write_store(SLOT_HOME_GUN, ct.read_store(SLOT_HOME_GUN) + 1)
                        return True
        return False

    def _try_harvester(self, ct, harv):
        p = ct.get_position()
        # PLANK HS: a harvester is impassable and permanent, so ore that happens
        # to sit on a heal seat costs the seat forever.  The reserved delivery
        # seats are still offered -- an ore tile there is worth mining and the
        # chain terminates on it anyway.
        ban = self._seat_ban()
        for d in DIRECTIONS:
            bp = p.add(d)
            if ban is not None and (bp.x, bp.y) in ban:
                continue
            if 0 <= bp.x < self.mw and 0 <= bp.y < self.mh and ct.can_build_harvester(bp):
                ct.build_harvester(bp)
                ct.write_store(SLOT_HARVESTERS, harv + 1)
                if harv + 1 >= ECO_NEED:
                    ct.write_store(SLOT_ECO_READY, 1)
                self._wire_on_build(ct, bp)
                return True
        return False

    def _defend(self, ct):
        p = ct.get_position()
        hive_bunker = (
            self.mw == 25 and self.mh == 25
            and (self.core.x, self.core.y) == (21, 3)
        )
        if hive_bunker and ct.get_action_cooldown() == 0:
            bp = Position(20, 4)
            bid = ct.get_tile_building_id(bp)
            if abs(p.x - bp.x) + abs(p.y - bp.y) == 1:
                if (
                    bid is not None and ct.get_team(bid) == self.team
                    and ct.get_entity_type(bid) == EntityType.BARRIER
                    and ct.can_heal(bp)
                ):
                    ct.heal(bp)
                    return
                # PLANK HS.  (20,4) IS a heal seat of the hive seat-B footprint
                # at (21,3) -- west pair -- and a barrier is impassable, so this
                # map-gated bunker plank permanently costs one of the eight
                # seats.  The ban is applied here for consistency with every
                # other impassable build site; healing an already-standing
                # barrier above is untouched, because this plank never destroys
                # what is already there.  RED FLAG: this is a shipped, measured,
                # single-map behaviour being overridden by a general rule, and
                # the remedy if hive regresses is one exemption clause.
                ban = self._seat_ban()
                if (
                    bid is None
                    and (ban is None or (bp.x, bp.y) not in ban)
                    and ct.get_global_resources() >= ct.get_barrier_cost()
                    and ct.can_build_barrier(bp)
                ):
                    ct.build_barrier(bp)
                    return
        under = ct.read_store(SLOT_UNDER) != 0
        # Proven shelling, observed directly off the Core's own HP bar rather
        # than read out of SLOT_UNDER -- see _core_shelled.  Conjoined with
        # `under` so it cannot fire on old unrepaired damage long after the
        # attacker left, and so the scan is skipped entirely on a quiet map.
        shelled = under and self._core_shelled(ct)
        chase_battery = (
            self.mw == 20 and self.mh == 26
            and self.core.x == 9 and self.core.y == 6
        )
        threat = unpack_pos(ct.read_store(SLOT_THREAT)) if under else None
        harv = ct.read_store(SLOT_HARVESTERS)
        ti = ct.get_global_resources()
        # PIECE H, builder half (see ENDGAME_SWITCH_ON).  Tiebreak 2 counts
        # harvesters ALIVE, so in the last forty rounds every economy ceiling
        # and every reserve is dead weight and a link laid now delivers
        # nothing worth the action.
        endgame = ENDGAME_SWITCH_ON and ct.get_current_round() >= ENDGAME_RND

        if ct.get_action_cooldown() == 0:
            defended = False
            if under:
                # HEAL BEATS SABOTAGE UNDER SHELLING.  On heart the defender
                # stood beside both an enemy Gunner and our Core and spent the
                # whole siege pecking the Gunner for 2 dmg a round (25 HP, at
                # 2 Ti a tick) while the Core it was touching took 0 heals.
                # 1 Ti for +4 HP absorbs more of an 18 dmg Sentinel ray than
                # any melee peck returns.  Belt and braces: the universal heal
                # in _builder already fires first for an adjacent builder, so
                # this holds the order if that call site ever moves.
                # PIECE J: same narrow defender exemption as the universal heal
                # above -- with no home gun standing and a battery in band, +4
                # HP a round against 18-25 loses on arithmetic, so the action
                # goes to _try_counterbattery below and the heal fallback at
                # the bottom of this block still catches the rounds it fails.
                if shelled and not self._cb_over_heal(ct) and self._heal_core(ct):
                    defended = True
                else:
                    defended = (
                        self._sabotage_prio(ct)
                        or self._try_counterbattery(ct)
                    )
                if chase_battery and threat is not None:
                    # On north-side Nordkap the legal battery outranges repair;
                    # spending every action on +4 HP prevents ever reaching it.
                    defended = True
                elif not defended:
                    defended = self._heal_core(ct)
            if not defended:
                if harv < 1 and ti >= ct.get_harvester_cost() and self._try_harvester(ct, harv):
                    return
                # Do not move in a conveyor-build tick: the movement query can
                # still treat the newly placed link as empty and strand us.
                # PIECE H: no new links past ENDGAME_RND -- the action is worth
                # more as a harvester two lines down.
                if not endgame and self.link_queue and ti >= ct.get_conveyor_cost():
                    if self._build_next_link(ct):
                        return
                # Wake the Launcher subsystem: v58's call site, deleted in the
                # v63 rework, restored here. _try_build_launcher() claims
                # SLOT_LAUNCHER before building, so this fires at most once.
                if not endgame and harv >= ECO_NEED and self._try_build_launcher(ct):
                    return
                # PIECE H: _eco_cap is a scale-curve ceiling for a game that
                # still has a future.  At ENDGAME_RND it is dropped outright --
                # any adjacent ore, any bank that covers the (scaled) cost.
                if (endgame or harv < self._eco_cap(ct)) and ti >= ct.get_harvester_cost() and self._try_harvester(ct, harv):
                    return
                if not under:
                    self._heal_core(ct)

        # Action phase is over here and left nothing half-set (every branch
        # above either returns right after its build/heal action or falls
        # through cleanly). Check before the move phase below: every branch
        # of it calls _nav, which runs _bfs_direction -- a BFS over the
        # whole map.
        if self._cpu_exhausted(ct):
            return

        if hive_bunker:
            if ct.get_move_cooldown() == 0:
                self.tgt = Position(20, 3)
                self._nav(ct, pave=False)
            return

        # DEFENDER COMES HOME.  In the meander loss the role_n == 4 defender
        # cycled far-off link/threat tiles for 150 rounds while the Core was
        # shelled to death.  Once the Core is provably losing HP the defender
        # has exactly one job -- stand next to it and heal -- so walking home
        # outranks chasing the threat and outranks finishing a conveyor link.
        # `shelled` requires the Core to be in this builder's own vision
        # (r^2 = 20), so this only fires from within about four tiles of home,
        # which is exactly the range where walking back is feasible anyway.
        if shelled and self.role_n == 4 and ct.get_move_cooldown() == 0 and not any(
            abs(p.x - c.x) + abs(p.y - c.y) == 1 for c in core_tiles(self.core)
        ):
            # PLANK HS, MECHANISM 2 (see HS_HEAL_DETAIL_ON).  The any() above is
            # already the seat test -- Manhattan 1 from a footprint tile IS a
            # seat -- so a unit that reaches here is off-seat by definition.
            # self.core as a target means "any unblocked seat" once
            # _bfs_direction expands it, which is how a defender ends up walking
            # at a seat somebody is already standing on; naming the free seat
            # makes the same walk arrive somewhere it can heal from.
            seat = self._seat_seek_target(ct)
            self.tgt = self.core if seat is None else seat
            self._nav(ct, pave=False)
            return

        if under and threat is not None and ct.get_move_cooldown() == 0:
            self.tgt = threat
            self._nav(ct, pave=False)
            return

        if self.link_queue:
            if ct.get_action_cooldown() == 0 and self._build_next_link(ct):
                return
            if not self.link_queue:
                return
            if ct.get_move_cooldown() == 0:
                nxt = self.link_queue[0]
                if p.x == nxt.x and p.y == nxt.y:
                    self._step_off_link(ct)
                elif abs(p.x - nxt.x) + abs(p.y - nxt.y) == 1:
                    # Already in build range.  Wait for action/resources instead
                    # of occupying the future conveyor cell; dead-end Core inputs
                    # (notably Vase) can otherwise trap the builder permanently.
                    return
                else:
                    self.tgt = nxt
                    self._nav(ct, pave=False)
            return

        if ct.get_move_cooldown() != 0:
            return
        if p.distance_squared(self.core) > 8:
            self.tgt = self.core
        elif self.tgt is None or p == self.tgt or self.stuck >= 2:
            self.ang = (self.ang + 1.0) % (2 * math.pi)
            self.tgt = Position(
                max(0, min(self.core.x + int(2 * math.cos(self.ang)), self.mw - 1)),
                max(0, min(self.core.y + int(2 * math.sin(self.ang)), self.mh - 1)),
            )
        self._nav(ct, pave=False)

    def _expand(self, ct):
        p = ct.get_position()
        # PIECE J, second half of the gun-counter fix: this freeze returns
        # _expand unconditionally on hive, BOTH seats, for the rest of the
        # match once the gun clause holds -- the confirmed economy self-freeze
        # against picket classes, and via _try_siege_build's increment it can
        # arm off our OWN forward gun at the enemy Core.  The live scan asks
        # the intended question ("a home turret is standing here"); the two
        # cheap tests are ordered ahead of it so the scan only runs on hive,
        # past round 42.
        hive_freeze = (
            HIVE_FREEZE_ON
            and self.mw == 25 and self.mh == 25
            and (self.core.x, self.core.y) in ((2, 20), (21, 3))
            and ct.get_current_round() >= 42
            and (
                self._live_home_gun(ct) if CB_OVER_HEAL_ON
                else ct.read_store(SLOT_HOME_GUN) >= 1
            )
        )
        if hive_freeze:
            return

        # SABOTEUR INTERCEPTION.  Ranks above ordinary expand work and below
        # everything already decided in _builder -- the universal Core heal,
        # the map-gated _rank2_hold and the near-Core melee recall all return
        # before _expand is ever entered.  Exactly one worker breaks off so the
        # remaining expanders keep the economy running; role_n == 1 is the
        # first expander and never changes role (only role_n == 3 is ever
        # promoted to saboteur), so ownership is stable for the whole match
        # without a store write.  The role_n == 4 defender is untouched.
        if self.role_n == 1 and self._intercept(ct):
            return

        has_launch = ct.read_store(SLOT_LAUNCHER) != 0
        harv = ct.read_store(SLOT_HARVESTERS)
        allow_pave = has_launch or harv >= 2
        # PIECE H, builder half (see ENDGAME_SWITCH_ON).  Harvesters alive is
        # tiebreak 2; a conveyor link and a 4 HP patch are worth nothing at all
        # by round 1000, so past ENDGAME_RND this expander spends every action
        # it has on ore and lets the economy ceiling and the siege reserve go.
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
                # PLANK HS: same impassable-building ban as _try_harvester's.
                seat_ban = self._seat_ban()
                for d in DIRECTIONS:
                    bp = p.add(d)
                    if seat_ban is not None and (bp.x, bp.y) in seat_ban:
                        continue
                    if 0 <= bp.x < self.mw and 0 <= bp.y < self.mh and ct.can_build_harvester(bp):
                        ct.build_harvester(bp)
                        ct.write_store(SLOT_HARVESTERS, ct.read_store(SLOT_HARVESTERS) + 1)
                        if ct.read_store(SLOT_HARVESTERS) >= ECO_NEED:
                            ct.write_store(SLOT_ECO_READY, 1)
                        self._wire_on_build(ct, bp)
                        break
            # CHAIN MEDIC (heal-in-passing).  Measured in the eider 1000-round
            # tiebreak losses to kladde_probe: ~70% of all damage to our
            # economy buildings was enemy BUILDER MELEE -- 376 hits x 2 dmg =
            # 752 HP, clearing ~37 twenty-HP conveyors -- and every cleared
            # tile was stateless-relaid by the next passer-by at 3 Ti plus,
            # decisively, +1% team-wide cost scale PER RELAY.  146 conveyor
            # builds put +146% on everything bought afterwards, which is what
            # pinned the bank under the respawn floor for ~600 rounds (the
            # money->labour chain of the eider diagnosis).  Healing is the
            # counter that costs no scale at all: 1 Ti for +4 HP outpaces a
            # melee peck's 2 dmg per round outright, and can_heal() refuses a
            # full-HP target, so this fires only when something adjacent is
            # genuinely damaged.  Deliberately LAST in the action phase --
            # link tiles and harvesters outvalue a 4 HP patch -- and floored
            # on a small bank so a starving opening never trades its first
            # harvester for a repair.  (The _v70ec reserve/rebuild-cap
            # approach to the same diagnosis was refuted by ablation: gating
            # link spending inverted the income bootstrap, collected 9390 ->
            # 3160.  Repair attacks the churn without touching the
            # bootstrap.)
            # Two windows.  Late (>= MEDIC_MIN_RND) is unchanged: any damage at
            # all.  Early (>= MEDIC_EARLY_MIN_RND) heals ONLY deep damage,
            # >= MEDIC_EARLY_MIN_DMG down -- the tempo tax the MEDIC_MIN_RND
            # ablation measured came from patching cosmetic opening pecks, and
            # the depth floor excludes exactly those while still covering a
            # sustained farm raid.
            # PIECE H: the medic is off past ENDGAME_RND.  A +4 HP patch on a
            # conveyor scores in no tiebreak; the action it costs could have
            # been a harvester, which scores in tiebreak 2.
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

        # Action phase over -- the harvester build above (if any) already
        # wrote SLOT_HARVESTERS and link_queue together with nothing after
        # it in the same branch, so nothing is left half-set. Check before
        # the move phase below, which calls _pick (an ore scan) and _nav
        # (a BFS over the map).
        if self._cpu_exhausted(ct):
            return

        # MULTI-HEALER CONVERGENCE.  One enemy turret chips the Core faster
        # than one healer repairs it: a Sentinel lands 18 damage every second
        # round, about -9/round, against the single role_n == 4 defender's
        # +4/round.  Measured over four Lunds Stallions games, that arithmetic
        # runs 150-900 rounds of the Core bleeding out while idle expanders
        # work the far side of the map and thousands of titanium sit banked.
        # Two or three converged healers deliver +8 to +12/round for 2-3 Ti a
        # round and flip the sign permanently.
        #
        # Only role_n == 2 and the role_n >= 5 replacements converge.  The
        # other seats keep their jobs: role_n == 0 is the siege engineer,
        # role_n == 1 the single interceptor, role_n == 3 turns saboteur, and
        # role_n == 4 already comes home via the identical rule in _defend.
        #
        # PROXIMITY-BOUNDED BY CONSTRUCTION: _core_shelled only answers True
        # when the Core is inside this builder's own vision (r^2 = 20), so
        # only builders already within about four tiles of home ever converge.
        # There is no cross-map recall and none is wanted -- a far expander
        # cannot see the Core, so it never leaves its ore.
        #
        # Conjoined with SLOT_UNDER exactly as _defend's `shelled` is, for the
        # same two reasons: it cannot fire on old unrepaired damage long after
        # the attacker left, and it is the same gate the universal adjacent
        # heal in _builder uses -- converging when that heal would not fire
        # would park a builder next to the Core for nothing.
        #
        # Once adjacent this holds position rather than falling through to the
        # walk-to-ore below: the healing itself is already handled: the
        # universal heal in _builder fires before _expand is entered on every
        # round the action cooldown allows.  Stepping away on the rounds it
        # cannot would cost a round walking back for every round healed.
        if (self.role_n == 2 or self.role_n >= 5) and ct.read_store(SLOT_UNDER) != 0 \
                and self._core_shelled(ct):
            self.converging = True
            if ct.get_move_cooldown() == 0 and not any(
                abs(p.x - c.x) + abs(p.y - c.y) == 1 for c in core_tiles(self.core)
            ):
                # PLANK HS, MECHANISM 2 (see HS_HEAL_DETAIL_ON) -- identical
                # substitution to _defend's come-home walk, and for the same
                # reason: converging on "the Core" is not the same thing as
                # converging on a seat that is actually free to heal from.  The
                # hold-once-adjacent behaviour above is untouched.
                seat = self._seat_seek_target(ct)
                self.tgt = self.core if seat is None else seat
                self._nav(ct, pave=False)
            return
        if self.converging:
            # Falling edge: the Core is whole again (or the siege is over).
            # Hand a CLEAN state back to the expand machine below, exactly as
            # _intercept's disengage does: self.tgt still holds the Core --
            # an unreachable building tile that _pick would never choose --
            # and self.stuck counted rounds of walking home, so both are
            # cleared, forcing a fresh _pick this same turn.  link_queue is
            # positional and survives the interruption untouched.
            self.converging = False
            self.tgt = None
            self.stuck = 0
            self.wall = None

        # SIPHON HYGIENE, deny arm (see SIPHON_DENY_ON).  Ranked exactly where
        # the measurement puts it: BELOW every survival/heal duty (all of which
        # return in _builder before _expand is entered) and below this
        # builder's own action phase above -- a link or a harvester it can
        # actually place this round outvalues a peck and returns before here --
        # but ABOVE walking off to the next deposit.  A builder wandering
        # between ore while an enemy belt drains one of our harvesters is the
        # exact turn this piece is meant to claim.
        if self._siphon_deny(ct):
            return

        if ct.get_move_cooldown() != 0:
            return
        # ORE STEP-OFF (borrowed from v79 after the heart decode).  Builds
        # are adjacent-only, never own-tile, so a builder standing ON an ore
        # tile is the one unit that can never put a harvester there -- and on
        # heart we parked one builder on tile (5,18) from r160 to r998, left
        # 14 of the map's 28 ore tiles unmined forever, and lost the economy
        # 2.5x.  Wall-dense maps only (his gate, copied): corridors are what
        # turn "standing on ore" from a transient into an 800-round park, and
        # on open maps squatting contested ore is sometimes exactly right
        # (atoll: HIS squatters out-collected us).  Ore is only knowable on
        # decoded maps; map_walls is empty otherwise and the gate stays shut.
        if (
            len(self.map_walls) >= ORE_STEPOFF_MIN_WALLS
            and ct.get_tile_env(p) == Environment.ORE_TITANIUM
        ):
            for d in CARDINALS:
                n = p.add(d)
                if (
                    0 <= n.x < self.mw and 0 <= n.y < self.mh
                    and ct.get_tile_env(n) != Environment.ORE_TITANIUM
                    and ct.is_tile_passable(n)
                    and ct.can_move(d)
                ):
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
                if ct.get_tile_env(bp) == Environment.ORE_TITANIUM and ct.get_tile_building_id(bp) is None:
                    self.tgt = bp
                    break
        self._nav(ct, pave=allow_pave)

    def _find_intruder(self, ct):
        """Nearest visible enemy builder bot operating inside our own half.

        "Our half" is the plain bisector test: closer to our Core than to the
        enemy Core anchor.  Bots within INTRUDER_CORE_DSQ of our Core are
        skipped -- the melee recall in _builder and the defender's threat
        chase already own those, and double-handling them would pull a second
        body onto a target that is already covered.
        """
        p = ct.get_position()
        best, best_d = None, None
        for eid in ct.get_nearby_units():
            if ct.get_team(eid) == self.team:
                continue
            if ct.get_entity_type(eid) != EntityType.BUILDER_BOT:
                continue
            ep = ct.get_position(eid)
            dc = self.core.distance_squared(ep)
            if dc <= INTRUDER_CORE_DSQ or dc >= ep.distance_squared(self.enemy):
                continue
            d = p.distance_squared(ep)
            if best_d is None or d < best_d or (d == best_d and eid < best):
                best, best_d = eid, d
        return best

    def _heal_adjacent(self, ct):
        """Repair a damaged friendly building we are standing next to.

        This, not the melee peck, is what actually stops an economy raider:
        builder fire is 2 Ti for 2 damage and only lands on BUILDINGS (a bot
        cannot be attacked at all -- docs/game-model.md), while a heal is
        1 Ti for +4 HP.  Parked between the raider and what it is chipping,
        the interceptor out-repairs it two-to-one on HP and eight-to-one on
        titanium, so the harvester never dies.  can_heal() enforces adjacency,
        cost, and that there is real damage, so this is free when nothing is
        hurt.
        """
        p = ct.get_position()
        for d in CARDINALS:
            t = p.add(d)
            if 0 <= t.x < self.mw and 0 <= t.y < self.mh and ct.can_heal(t):
                ct.heal(t)
                return True
        return False

    def _guard_target(self, ct, tp):
        """The friendly building this raider is working on, if we can see one.

        Standing next to the RAIDER accomplishes nothing -- it cannot be
        damaged and it is usually on the far side of its victim anyway.
        Standing next to its VICTIM turns the chase into a repair escort,
        which the raider cannot win.  Damaged first, then nearest to it.
        """
        best, best_k = None, None
        rnd = ct.get_current_round()
        for eid in ct.get_nearby_buildings():
            if ct.get_team(eid) != self.team:
                continue
            # STALEMATE DISENGAGE.  Measured in the v79 battery replays: the
            # escort "wins" its stalemate -- +4 heal beats -2 peck -- and
            # that is exactly the trap.  On atoll the raider pecked one
            # sentinel 819 times over r181-999 and the escort healed it 819
            # times: one builder's entire action budget and ~1,100-1,200 Ti
            # (about 20% of match income) spent holding a permanently
            # contested building, three matches out of four (heart: 717
            # pecks on a 3-Ti conveyor; meander: 905 heals on a conveyor
            # inside the enemy kill zone that never delivered a stack).  The
            # raider cannot win the tile, but it converts our escort into a
            # 450-820-round income drain, which is a better trade for it.
            # So the escort keeps score: if a guarded building has not been
            # NET-whole for ESCORT_STALL_RNDS consecutive escort rounds, it
            # is written off for good and the escort goes back to work --
            # losing a 3-20 Ti building outright is strictly cheaper than
            # paying its ransom forever.  Per-unit ledger, same locality
            # argument as hunt_defer.
            if self.escort_ban.get(eid, 0) > rnd:
                continue
            bp = ct.get_position(eid)
            d = bp.distance_squared(tp)
            if d > 4:
                continue
            hp = ct.get_hp(eid)
            if hp < ct.get_max_hp(eid):
                stalled = self.escort_watch.get(eid, 0) + 1
                if stalled >= ESCORT_STALL_RNDS:
                    self.escort_ban[eid] = rnd + ESCORT_BAN_RNDS
                    self.escort_watch.pop(eid, None)
                    continue
                self.escort_watch[eid] = stalled
            else:
                # Whole again: the attacker left or died.  Clean slate.
                self.escort_watch.pop(eid, None)
            k = (0 if hp < ct.get_max_hp(eid) else 1, d, eid)
            if best_k is None or k < best_k:
                best, best_k = bp, k
        return best

    def _intercept(self, ct):
        """Chase the owned intruder.  True when this turn was spent on it."""
        if self.core is None or self.enemy is None:
            return False
        p = ct.get_position()
        rnd = ct.get_current_round()
        eid = self._find_intruder(ct)
        if eid is not None:
            self.chase_id = eid
            self.chase_pos = ct.get_position(eid)
            self.chase_seen = rnd
        elif self.chase_id is None:
            return False
        elif (
            rnd - self.chase_seen >= INTRUDER_FORGET_RNDS
            or p == self.chase_pos
            or (
                ct.is_in_vision(self.chase_pos)
                and ct.get_tile_builder_bot_id(self.chase_pos) is None
            )
        ):
            # The trail went cold, or we can see the last sighting and it is
            # empty -- the raider left our half or died.  (Standing on the
            # tile is checked separately: get_tile_builder_bot_id would return
            # our own id there.)  Drop the chase and hand a CLEAN state back to
            # the expand machine below: self.tgt still holds the intruder's
            # tile and self.stuck counted rounds of chasing, so both are
            # cleared exactly as _expand's own retarget branch clears them,
            # forcing a fresh _pick this same turn.  link_queue is positional
            # and survives the interruption untouched.
            self.chase_id = None
            self.chase_pos = None
            self.tgt = None
            self.stuck = 0
            self.wall = None
            return False
        tp = self.chase_pos
        guard = self._guard_target(ct, tp)
        goal = tp if guard is None else guard
        if abs(p.x - goal.x) + abs(p.y - goal.y) == 1:
            # Orthogonally adjacent: act and hold.  Never nav from here --
            # _bfs_direction would aim at the occupied tile, can_move would
            # refuse it, and _nav's fallbacks would slide us off the target.
            if ct.get_action_cooldown() == 0:
                # Piece D: tbid is None for the usual case (the intruder is a
                # builder bot), which _duel_safe passes straight through -- the
                # gate only ever bites on an enemy Gunner/Sentinel standing on
                # the chased tile, where an unsafe duel falls through to the
                # heal branch below instead of feeding the gun.
                try:
                    tbid = ct.get_tile_building_id(tp)
                except Exception:
                    tbid = None
                # PIECE S1 (see S1_INTERCEPT_GUARD_ON).  fire() hits the
                # BUILDING on the tile, and the chased intruder spends its life
                # standing on our conveyors -- so without this test the chase
                # pays 2 Ti a round to demolish our own chain while the medic
                # heals it back.  Same try/except as the id fetch above: an
                # unreadable team is treated as ours, i.e. hold fire, because
                # the fire is worth 2 damage and the mistake is worth a link.
                own_building = False
                if S1_INTERCEPT_GUARD_ON and tbid is not None:
                    try:
                        own_building = ct.get_team(tbid) == self.team
                    except Exception:
                        own_building = True
                if guard is not None and ct.can_heal(guard):
                    ct.heal(guard)
                elif not own_building and ct.can_fire(tp) and self._duel_safe(ct, tp, tbid):
                    ct.fire(tp)
                else:
                    self._heal_adjacent(ct)
            return True
        if ct.get_move_cooldown() == 0:
            self.tgt = goal
            self._nav(ct, pave=False)
        return True

    def _link_path(self, ct, hpos):
        raw_goals = set()
        for c in core_tiles(self.core):
            for d in CARDINALS:
                t = c.add(d)
                if 0 <= t.x < self.mw and 0 <= t.y < self.mh and dist_core(t, self.core) > 0:
                    raw_goals.add((t.x, t.y))
        # PLANK HS (see HS_SEAT_PROTECT_ON).  raw_goals IS the heal-seat set --
        # every Core input stands on a seat -- so restricting it to the reserved
        # delivery seats is what makes planned chains terminate on those two and
        # nowhere else.  The ban set is also fed to both searches below as
        # blocked ground: seats along one side of the footprint are adjacent to
        # each other, so a tree grown from a delivery seat would otherwise route
        # THROUGH a protected seat on its way out.  delivery_seats never returns
        # empty while any seat exists, so this cannot silently orphan the map.
        ban = self._pave_ban()
        if ban is not None:
            raw_goals -= ban
        start = (hpos.x, hpos.y)
        if start in raw_goals or not raw_goals:
            return []

        # On a known pool map, grow one deterministic reverse tree from every
        # valid Core input.  All harvester chains therefore agree on conveyor
        # direction when they merge.  Other ore is reserved for Harvesters.
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
            link_bfs_steps = 0
            while q and start not in parent:
                x, y = q.popleft()
                link_bfs_steps += 1
                if link_bfs_steps % 64 == 0 and self._cpu_exhausted(ct):
                    # `start` is still not in `parent` at this point (if it
                    # were, the while condition above would already be
                    # False), so breaking here falls straight into the
                    # existing "not found" return just below -- the same
                    # path a search that genuinely exhausts the map takes.
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

        # Unknown-map fallback: use every currently sensed wall/building and
        # re-evaluate on future maps rather than requiring a pool lookup.
        #
        # RED FLAG, left deliberately unfixed here (see E2B_ORE_PAVE_BAN_ON):
        # the decoded branch above blocks every ore tile, this one blocks only
        # WALL and non-pipeline buildings.  So on a map we have not decoded --
        # any pool rotation -- a planned LINK can still route across ore and
        # bury a harvester site, which is precisely the loss E2B closes on the
        # pave path.  The remedy is one clause in the neighbour test here
        # (skip n when get_tile_env(n) == ORE_TITANIUM and n is not the
        # harvester we are wiring), but a planner change is its own piece with
        # its own reachability risk -- a banned tile can disconnect the only
        # corridor -- so it is measured separately, not smuggled in with a
        # pave gate.
        goals = raw_goals
        prev = {start: None}
        q = deque([start])
        found = None
        fallback_bfs_steps = 0
        while q:
            x, y = q.popleft()
            fallback_bfs_steps += 1
            if fallback_bfs_steps % 64 == 0 and self._cpu_exhausted(ct):
                # `found` stays None, which falls straight into the existing
                # "not found" return below -- the same path an exhausted
                # search takes.
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
                # PLANK HS: same protected-seat ban as the decoded branch above.
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
        """Book the harvester just built at bp for a chain (SIPHON_WIRE_ON).

        The two lines this replaces planned a path only when link_queue was
        empty, so a builder that already had a chain in flight left the new
        harvester with NO chain, ever -- the orphan that the wild measurement
        found handing 100% of its output to an adjacent enemy belt (see the
        SIPHON HYGIENE block).  Nothing here keys on the SITE: a rebuild of a
        tile we wired an hour ago books exactly like a first build, because
        the conveyor that used to serve it may well be dead.
        """
        if not self.link_queue:
            self.link_source = bp
            self.link_queue = self._link_path(ct, bp)
            return
        if not SIPHON_WIRE_ON or len(self.wire_pending) >= SIPHON_WIRE_QUEUE:
            return
        self.wire_pending.append((bp, ct.get_current_round()))

    def _has_acceptor(self, ct, bp):
        """True if a friendly building that can take a stack touches bp.

        Deliberately a LIVE adjacency test rather than a memory of what we
        once built: it is what makes a rebuilt harvester on a previously
        wired tile re-enter the queue when its old conveyor is gone.  Out of
        vision reads as "no" -- the pending entry is kept and re-tested.
        """
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
        """Give a pending harvester its chain once the current one is done.

        Waits for the in-flight chain rather than interrupting it: a chain
        abandoned halfway is a DEAD END, and a dead-end conveyor accepts one
        stack and then blocks forever (game-model.md), so preempting would
        leave two harvesters delivering nothing instead of one.  The wait is
        bounded by SIPHON_WIRE_RNDS so a wedged queue cannot orphan the new
        harvester for the rest of the match.
        """
        if not SIPHON_WIRE_ON or not self.wire_pending:
            return
        bp, since = self.wire_pending[0]
        if self._has_acceptor(ct, bp):
            # Served -- by our own chain arriving, or by another builder.
            self.wire_pending.pop(0)
            return
        if self.link_queue and ct.get_current_round() - since < SIPHON_WIRE_RNDS:
            return
        path = self._link_path(ct, bp)
        self.wire_pending.pop(0)
        if path:
            self.link_source = bp
            self.link_queue = path

    def _siphon_clear(self):
        """Drop the siphon target and hand a clean state back to _expand."""
        self.siphon_id = None
        self.siphon_pos = None
        self.siphon_hp = None
        self.tgt = None
        self.stuck = 0
        self.wall = None

    def _find_siphon(self, ct):
        """Nearest enemy belt tile orthogonally touching one of OUR harvesters.

        One pass over get_nearby_buildings -- the scan the base already runs in
        _guard_target and _link_path -- collecting our harvesters and their
        belts, then the adjacency intersection.  Evaluated CONTINUOUSLY, not at
        build time, so it covers both geometries of the wild shape: their
        conveyor creeping in beside a harvester we have been holding, and our
        (re)build on a contested border tile where their intact conveyor is
        already sitting.
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

    def _siphon_taken(self, ct, bpos, me):
        """True if another friendly builder is already pecking this belt.

        One attacker per tile: ten swings kill a conveyor, so a second body is
        pure waste of an expander.  Same idiom as _duel_safe's volume test.
        """
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

    def _siphon_deny(self, ct):
        """Peck down an enemy belt tapping one of our harvesters.

        True when this turn was spent on it.  See the SIPHON HYGIENE block for
        the arithmetic: 20 HP at 2 damage a peck, 2 Ti a peck, against a drain
        of ~2.5 Ti/round that a friendly conveyor can only halve, never stop.
        """
        if not SIPHON_DENY_ON or self.core is None:
            return False
        if ct.get_global_resources() < SIPHON_FIRE_TI:
            # Guarded: _siphon_clear also resets tgt/stuck/wall, and an
            # unheld target must not cost the expander its ore target every
            # round the bank happens to be empty.
            if self.siphon_pos is not None:
                self._siphon_clear()
            return False
        rnd = ct.get_current_round()
        p = ct.get_position()

        # UNDER FIRE: our own HP fell while on this duty.  A 40 HP builder is
        # not worth trading for a 3 Ti conveyor, so the tile is written off and
        # the unit goes back to work -- the duel-discipline rule of _duel_safe,
        # applied to a target that cannot shoot back but can be covered by
        # something that does.
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
                # Ransom, not a grind: something is repairing it faster than we
                # peck.  Stop paying (ESCORT_STALL_RNDS, same reasoning).
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
            if ct.get_action_cooldown() == 0 and ct.can_fire(tgt):
                ct.fire(tgt)
            return True
        if ct.get_move_cooldown() != 0:
            return True
        if d == 0:
            # Belts are bot-passable, so the walk below can land us ON the
            # target.  One step in any direction makes us adjacent.
            for step in CARDINALS:
                if ct.can_move(step):
                    ct.move(step)
                    return True
            return True
        self.tgt = tgt
        self._nav(ct, pave=False)
        return True

    def _build_next_link(self, ct):
        if not self.link_queue or not self._eco_spendable(ct, ct.get_conveyor_cost()):
            return False
        p = ct.get_position()
        while self.link_queue:
            tile = self.link_queue[0]
            # Tile queries are vision-limited.  Walk into build range before
            # inspecting the next planned segment.
            if abs(p.x - tile.x) + abs(p.y - tile.y) > 1:
                return False
            if ct.get_tile_building_id(tile) is not None:
                self.link_queue.pop(0)
                continue
            if p.x == tile.x and p.y == tile.y:
                return False
            break
        if not self.link_queue:
            # Slot 9's "links done" counter was incremented here and below and
            # read nowhere in the file; the slot now carries PIECE K's heal
            # budget (see SLOT_HEAL_BUDGET), so the two dead writes are gone.
            return False
        tile = self.link_queue[0]
        # PLANK HS, belt and braces.  _link_path already refuses to plan through
        # or into a protected seat, so this should be unreachable; if a queue
        # ever outlives a change of ban (a Launcher throw re-homing a unit, a
        # future dynamic reserve), dropping the plan is the self-healing answer
        # -- the next harvester re-plans from scratch, whereas skipping one tile
        # would leave a chain permanently severed at that gap.
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
        """Vacate the planned conveyor cell so it can be built next round."""
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

    def _pick(self, ct):
        if self.map_ores and self.role == "expand":
            # Static role partitions avoid four builders racing toward the same
            # deposit.  Each partition starts in our half and eventually sweeps
            # the whole map if the match lasts long enough.
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
                if ct.is_in_vision(t) and ct.get_tile_building_id(t) is not None:
                    continue
                return t

        ores = [t for t in ct.get_nearby_tiles()
                if ct.get_tile_env(t) == Environment.ORE_TITANIUM and ct.get_tile_building_id(t) is None]
        if ores:
            return min(ores, key=lambda t: dist_core(t, self.core))
        r = 3 + (ct.get_current_round() // 30) + (self.idx % 5)
        self.ang = (self.ang + 0.65) % (2 * math.pi)
        return Position(
            max(0, min(self.core.x + int(r * math.cos(self.ang)), self.mw - 1)),
            max(0, min(self.core.y + int(r * math.sin(self.ang)), self.mh - 1)),
        )

    def _bfs_direction(self, ct, target):
        """Return one exact static-terrain step, with visible units avoided."""
        p = ct.get_position()
        if self.map_grid is None:
            return p.cardinal_direction_to(target)

        blocked = set(self.map_walls)
        if self.core is not None:
            blocked.update((c.x, c.y) for c in core_tiles(self.core))
        if self.enemy is not None:
            blocked.update((c.x, c.y) for c in core_tiles(self.enemy))
        try:
            for eid in ct.get_nearby_entities():
                if eid == ct.get_id():
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
        nav_bfs_steps = 0
        while q:
            x, y, first = q.popleft()
            nav_bfs_steps += 1
            if nav_bfs_steps % 64 == 0 and self._cpu_exhausted(ct):
                # Same fallback this function already returns a few lines
                # above (goals empty) and below (search exhausted): one
                # direct cardinal step toward the target. Pure function, no
                # instance state, so bailing here is trivially safe.
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
        p = ct.get_position()
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
        # Pave toward core, but still attempt move (don't treat pave-only as success)
        # HIVE EXCLUSION for the trail pave.  Diagnosed on hive seat-A vs
        # kladde_probe (seeds 2/5/9, deterministic): a single walk-direction
        # pave at r22 -- an ore-forager stepping through (4,18) -- faced a
        # dead end, and _build_next_link's "occupied implies correct" skip
        # then routed the (17,17) harvester's trunk chain through it 40
        # rounds later: one fewer DIRECTED harvester forever, collection
        # flatlined at 1080 from r250, core dead r717.  F-off wins the same
        # game r325.  Not a volume effect (both variants build exactly 40
        # conveyors).  On this map the geometry-derived old rule never makes
        # the mistake, so hive falls through to it -- same per-map idiom as
        # hive_freeze/hive_bunker.  The root fix (linker verifies facing and
        # destroy()+rebuilds wrong heads -- destroy is measured free) is the
        # follow-on, not this gate.
        hive_map = self.mw == 25 and self.mh == 25 and self.core is not None \
            and (self.core.x, self.core.y) in ((2, 20), (21, 3))
        if PAVE_TRAIL_ON and not hive_map:
            # PIECE F: pave the tile we just LEFT, facing the direction we just
            # MOVED, so its output tile is the one we now stand on -- the next
            # tile of the same trail.  pave_prev is one cardinal step away by
            # construction and pave_dir is always cardinal (moves are
            # cardinal-only), so both legality preconditions are free.
            pp = self.pave_prev
            if pp is not None and self.pave_rnd != ct.get_current_round() - 1:
                pp = None
            # PIECE N (Eir 6e): pave_prev is one step away BY CONSTRUCTION only
            # until a Launcher throw teleports this builder between turns --
            # then pp can sit outside vision and is_tile_empty(pp) raises
            # GameError, aborting the whole dispatch (measured: every
            # "crash" in the 6d race v68 legs, both sides, was exactly
            # this line; also x3r0's kite_proxy stress traceback with high
            # confidence).  The guard skips the pave, never the move.
            if pave and self.core and pp is not None and ct.get_action_cooldown() == 0 \
                    and ct.is_in_vision(pp) and ct.is_tile_empty(pp):
                # PIECE E2B, trail site (see E2B_ORE_PAVE_BAN_ON).  A conveyor
                # here would hold an ore tile for the rest of the match and the
                # linker's "occupied implies done" pop would never clear it.
                # The move below is untouched; only the pave is skipped.
                # PLANK HS rides the same predicate (see pave_blocked): an
                # undirected trail conveyor is the LEAST valuable thing that can
                # ever stand on a heal seat, and this is the site the seat census
                # blames for most of the paved seats it counts.
                ore_ban = pave_blocked(ct, pp, self._pave_ban())
                if not ore_ban and ct.read_store(SLOT_HARVESTERS) >= 1 and self._eco_spendable(ct, ct.get_conveyor_cost()):
                    if dist_core(pp, self.core) > 0:
                        if dist_core(pp, self.core) == 1:
                            # TERMINAL: pp is adjacent to the footprint.  The
                            # old expression is correct here and ONLY here --
                            # it aims into the Core.  The coreward gate cannot
                            # hold on this step (we are leaving), so it is not
                            # applied: this is the trail's delivery point.
                            facing = nearest_cardinal(pp.direction_to(nearest_core_tile(pp, self.core)))
                            coreward_ok = True
                        else:
                            # INTERIOR: output == the tile we now stand on.
                            facing = self.pave_dir
                            coreward_ok = (
                                abs(p0.x - self.core.x) + abs(p0.y - self.core.y)
                                < abs(pp.x - self.core.x) + abs(pp.y - self.core.y)
                            )
                        if coreward_ok and facing is not None and ct.can_build_conveyor(pp, facing):
                            ct.build_conveyor(pp, facing)
        elif pave and self.core and ct.is_tile_empty(nxt) and ct.get_action_cooldown() == 0:
            # PIECE E2B, next-step site (see E2B_ORE_PAVE_BAN_ON).  Same rule as
            # the trail site above: never lay a conveyor on ore.  nxt is one
            # cardinal step away so the vision test inside the predicate is
            # free here, but the predicate is shared so the two sites cannot
            # drift apart.
            ore_ban = pave_blocked(ct, nxt, self._pave_ban())
            if not ore_ban and ct.read_store(SLOT_HARVESTERS) >= 1 and self._eco_spendable(ct, ct.get_conveyor_cost()):
                if dist_core(nxt, self.core) > 0:
                    here = ct.get_position()
                    if abs(nxt.x - self.core.x) + abs(nxt.y - self.core.y) < abs(here.x - self.core.x) + abs(here.y - self.core.y):
                        card = nearest_cardinal(nxt.direction_to(nearest_core_tile(nxt, self.core)))
                        if ct.can_build_conveyor(nxt, card):
                            ct.build_conveyor(nxt, card)
        if ct.can_move(d):
            ct.move(d)
            if PAVE_TRAIL_ON:
                self.pave_prev = p0
                self.pave_dir = d
                self.pave_rnd = ct.get_current_round()
            return True
        return False

    def _turret(self, ct):
        if self.team is None:
            self.team = ct.get_team()
        p = ct.get_position()
        turret_type = ct.get_entity_type()
        enemy_anchor = unpack_pos(ct.read_store(SLOT_ENEMY_CORE))
        healer_focus = (
            ct.get_map_width() == 26 and ct.get_map_height() == 26
            and enemy_anchor is not None
            and enemy_anchor.x == 5 and enemy_anchor.y == 5
        )
        if turret_type == EntityType.GUNNER:
            tgt = ct.get_gunner_target()
            if tgt is not None and ct.can_fire(tgt):
                bid = ct.get_tile_building_id(tgt)
                bot = ct.get_tile_builder_bot_id(tgt)
                hostile = (
                    (bid is not None and ct.get_team(bid) != self.team)
                    or (bot is not None and ct.get_team(bot) != self.team)
                )
                if hostile:
                    ct.fire(tgt)
                    return

        # Sentinels pierce intervening units; scan their whole line and prefer
        # the Core, then combat units/builders, then economic infrastructure.
        try:
            best = None
            best_prio = 99
            for t in ct.get_attackable_tiles():
                bid = ct.get_tile_building_id(t)
                bot = ct.get_tile_builder_bot_id(t)
                et = None
                if bid is not None and ct.get_team(bid) != self.team:
                    et = ct.get_entity_type(bid)
                elif bot is not None and ct.get_team(bot) != self.team:
                    et = EntityType.BUILDER_BOT
                if et is None or not ct.can_fire(t):
                    continue
                if healer_focus:
                    prio = {
                        EntityType.BUILDER_BOT: 0, EntityType.CORE: 1,
                        EntityType.SENTINEL: 2, EntityType.GUNNER: 3,
                        EntityType.LAUNCHER: 4, EntityType.HARVESTER: 5,
                        EntityType.CONVEYOR: 6, EntityType.SPLITTER: 6,
                        EntityType.BARRIER: 7,
                    }.get(et, 8)
                else:
                    prio = {
                        EntityType.CORE: 0, EntityType.SENTINEL: 1,
                        EntityType.GUNNER: 2, EntityType.BUILDER_BOT: 3,
                        EntityType.LAUNCHER: 4, EntityType.HARVESTER: 5,
                        EntityType.CONVEYOR: 6, EntityType.SPLITTER: 6,
                        EntityType.BARRIER: 7,
                    }.get(et, 8)
                if prio < best_prio:
                    best_prio, best = prio, t
            if best is not None:
                ct.fire(best)
                return
        except Exception:
            pass
        for eid in ct.get_nearby_entities():
            if ct.get_team(eid) != self.team and ct.can_fire(ct.get_position(eid)):
                ct.fire(ct.get_position(eid))
                return
        # IDLE ROTATION.  Nothing was firable this turn; a Gunner may re-aim.
        # PIECE I replaces the bare nearest-bearing rotate below -- see
        # ROTATE_DISCIPLINE_ON for the 4,460 Ti / 8 games measurement.  The
        # legacy tail is kept verbatim behind the toggle so the ablation grid
        # measures exactly this change and nothing else.  For a Sentinel both
        # paths are no-ops (the old one computed `enemy` and then failed the
        # GUNNER test), so the early return costs nothing.
        if ROTATE_DISCIPLINE_ON:
            self._idle_rotate(ct, p, turret_type)
            return
        enemy = unpack_pos(ct.read_store(SLOT_ENEMY_CORE))
        best = 10**9
        for eid in ct.get_nearby_entities():
            if ct.get_team(eid) == self.team:
                continue
            ep = ct.get_position(eid)
            d = p.distance_squared(ep)
            if d < best:
                best, enemy = d, ep
        if enemy is not None and turret_type == EntityType.GUNNER:
            want = p.direction_to(enemy)
            if want != Direction.CENTRE and want != ct.get_direction():
                if ct.can_rotate(want):
                    ct.rotate(want)
                else:
                    card = nearest_cardinal(want)
                    if card != ct.get_direction() and ct.can_rotate(card):
                        ct.rotate(card)

    def _ray_lands(self, ct, p, facing, target):
        """Would a Gunner at p facing `facing` have `target` in its line?

        can_fire_from is the hypothetical-turret predicate and ignores ammo and
        cooldown by contract, which is exactly the question the rotation
        decision asks: not "can I shoot right now" but "is this facing worth 10
        Ti and the next shot".  Fails safe to False -- a facing we cannot
        evaluate is a facing we do not pay for.
        """
        try:
            return bool(ct.can_fire_from(p, facing, EntityType.GUNNER, target))
        except Exception:
            return False

    def _hostile_at(self, ct, pos):
        """True if an enemy building or builder bot stands on pos, seen now.

        Out-of-vision tiles raise on the tile getters, so the except arm is the
        answer for a target that has walked out of sight: not live, drop the
        hysteresis latch.
        """
        try:
            bid = ct.get_tile_building_id(pos)
            if bid is not None and ct.get_team(bid) != self.team:
                return True
            bot = ct.get_tile_builder_bot_id(pos)
            return bot is not None and ct.get_team(bot) != self.team
        except Exception:
            return False

    def _facing_has_target(self, ct):
        """Does this Gunner's CURRENT facing still hold a hostile it could shoot?

        Half of the rotation latch's escape clause (see ROTATE_COOLDOWN_RNDS).
        Asked with the same predicate _turret opens with: get_gunner_target is
        the nearest targetable tile in the facing line and will happily hand
        back one of our own buildings, so the tile has to be team-checked before
        it counts.  Reaching _idle_rotate at all means no shot went out this
        turn -- dry magazine or cooldown, since the fire path returns on
        success -- and neither of those is a reason to pay 10 Ti to aim
        somewhere else.  Fails safe to True: a facing we cannot evaluate is a
        facing we do not pay to leave.
        """
        try:
            t = ct.get_gunner_target()
            if t is None:
                return False
            bid = ct.get_tile_building_id(t)
            if bid is not None and ct.get_team(bid) != self.team:
                return True
            bot = ct.get_tile_builder_bot_id(t)
            return bot is not None and ct.get_team(bot) != self.team
        except Exception:
            return True

    def _rotate_allowed(self, ct, p, want, tgt):
        """ROTATION LATCH -- may this Gunner pay for a rotation this round?

        See ROTATE_COOLDOWN_RNDS for the nordkap g3 numbers this exists to stop.
        Outside the window every rotation rules 1-3 approved goes through
        exactly as v65 shipped it, which is what keeps the nine clean production
        games clean.  Inside it, a facing costs 10 Ti only if it is both
        unproductive now and strictly beaten by rule 2's own 3x dsq margin --
        and never if it is the facing we just paid to leave.
        """
        if ct.get_current_round() - self.rot_rnd >= ROTATE_COOLDOWN_RNDS:
            return True
        # The A->B->A edge, refused by name.
        if want == self.rot_prev_dir:
            return False
        if self._facing_has_target(ct):
            return False
        return p.distance_squared(tgt) * 3 <= self.rot_lock_d

    def _idle_rotate(self, ct, p, turret_type):
        """PIECE I -- disciplined idle re-aim for a Gunner.  See
        ROTATE_DISCIPLINE_ON for the measurement and the three rules, and
        ROTATE_COOLDOWN_RNDS for the Eir 5.1 latch layered over them."""
        if turret_type != EntityType.GUNNER:
            return
        cur = ct.get_direction()

        # Rule 3: builder bots only count inside gunner attack range.  Past it
        # they cannot be shot this turn anyway and they will have moved before
        # the rotation cooldown clears -- that is the drumlin thrash, 325
        # rotations in one game, in one line.
        cand, cand_d = None, 10**9
        for eid in ct.get_nearby_entities():
            if ct.get_team(eid) == self.team:
                continue
            ep = ct.get_position(eid)
            d = p.distance_squared(ep)
            if d >= cand_d:
                continue
            if (
                ct.get_entity_type(eid) == EntityType.BUILDER_BOT
                and d > GUNNER_RANGE_DSQ
            ):
                continue
            cand, cand_d = ep, d

        # Rule 2: hysteresis.  Hold the current aim point while it is still a
        # live hostile; a rival has to be 3x closer in dsq to take the facing.
        tgt = cand
        prev = self.rot_tgt
        if prev is not None and self._hostile_at(ct, prev):
            prev_d = p.distance_squared(prev)
            if cand is None or cand_d * 3 > prev_d:
                tgt = prev

        if tgt is not None:
            self.rot_tgt = tgt
            # Rule 1: pay only for a facing that actually lands the ray, and
            # only when the facing we already have does not.
            if self._ray_lands(ct, p, cur, tgt):
                return
            want = p.direction_to(tgt)
            if want == Direction.CENTRE:
                return
            if not self._ray_lands(ct, p, want, tgt):
                # The legacy tail's cardinal fallback, kept but now also
                # ray-checked.  Skipped when the bearing is already cardinal:
                # nearest_cardinal would hand back the same facing we just
                # rejected, for a second engine call and the same answer.
                if want.is_cardinal():
                    return
                want = nearest_cardinal(want)
                if not self._ray_lands(ct, p, want, tgt):
                    return
            if want != cur and ct.can_rotate(want):
                # Eir 5.1 latch (see ROTATE_COOLDOWN_RNDS).  Last gate before
                # the 10 Ti leaves; can_rotate is asked first because it is the
                # cheaper refusal and keeps the latch state honest -- rot_rnd
                # must only ever record a rotation that actually happened.
                if not self._rotate_allowed(ct, p, want, tgt):
                    return
                self.rot_rnd = ct.get_current_round()
                self.rot_prev_dir = cur
                self.rot_lock_d = p.distance_squared(tgt)
                ct.rotate(want)
            return

        # Nothing hostile in sight: fall back to the stored enemy-Core bearing.
        # Exempt from rule 1 by design (the anchor is far past r^2=13) and
        # self-limiting instead: p and the anchor are both fixed, so after this
        # fires once `want` equals the facing and it never fires again.
        self.rot_tgt = None
        # ...  but NOT exempt from the Eir 5.1 latch.  Self-limiting only holds
        # while the facing stays put; a gunner that answered a real target last
        # round and sees the ring empty this round would otherwise pay 10 Ti to
        # walk straight back to the anchor bearing, and pay again when the enemy
        # steps back into vision.  In the window the idle re-aim is the cheapest
        # thing to give up -- it buys no shot this turn either way.
        if ct.get_current_round() - self.rot_rnd < ROTATE_COOLDOWN_RNDS:
            return
        anchor = unpack_pos(ct.read_store(SLOT_ENEMY_CORE))
        if anchor is None:
            return
        want = p.direction_to(anchor)
        if want != Direction.CENTRE and want != cur and ct.can_rotate(want):
            self.rot_rnd = ct.get_current_round()
            self.rot_prev_dir = cur
            # No target bought, so no yardstick to defend: leave rot_lock_d
            # wide open and let a real hostile take the facing on clause (a)
            # alone rather than gating it behind a dsq it cannot beat.
            self.rot_lock_d = 10 ** 9
            ct.rotate(want)

    def _kidnap_probe(self, ct, tag, frm, to, covered, walk, sep, healer, tgt):
        """One stderr row per enemy-bot throw.  Off in shipped bytes.

        stderr, not print(): print() is captured into the replay rather than the
        console (docs/tooling.md), and the analysis script joins these rows to
        the replay's own RemoveEntity stream by round + position.
        """
        if not KIDNAP_PROBE:
            return
        try:
            import sys
            import time
            # ct.get_cpu_time_elapsed() is a stub under local `fcode run`
            # (docs/tooling.md), so local CPU accounting has to come from
            # process_time; the shipped guard still reads the engine counter.
            t0 = getattr(self, "kidnap_t0", None)
            us = -1 if t0 is None else int((time.process_time() - t0) * 1e6)
            print(
                "KIDNAP\t%s\tr=%d\tfrom=%d,%d\tto=%d,%d\tcov=%d\twalk=%d"
                "\tsep=%d\theal=%d\ttgt=%d\tus=%d"
                % (tag, ct.get_current_round(), frm.x, frm.y, to.x, to.y,
                   int(covered), walk, sep, int(healer), tgt, us),
                file=sys.stderr,
            )
        except Exception:
            pass

    def _kidnap_open(self, ct, pos):
        """True if pos is currently empty of wall, building AND builder bot.

        A Gunner's ray is stopped by all three (only empty tiles fail to block),
        so this is the truncation test for its coverage line.  Out-of-vision
        tiles raise on the tile getters, and an unknown tile is treated as
        BLOCKING -- that under-claims coverage, which is the safe direction:
        the rule's whole risk is claiming a killzone we do not have.
        """
        try:
            if not ct.is_tile_empty(pos):
                return False
            return ct.get_tile_builder_bot_id(pos) is None
        except Exception:
            return False

    def _kidnap_cover(self, ct):
        """Tiles a LOADED friendly turret line already covers, as an (x, y) set.

        Computed ONCE per launcher-turn from the turrets rather than per
        candidate tile: each turret contributes at most 5 pattern tiles (gunner
        r^2=13 -> 3 cardinal / 2 diagonal, sentinel r^2=32 -> 5 / 4), so this is
        O(turrets) where the obvious formulation is O(candidates x turrets).

        get_attackable_tiles_from is the RAW pattern and ignores occupancy and
        walls -- exactly right for a Sentinel, whose line ignores obstacles, and
        WRONG for a Gunner, whose ray is stopped by walls, bots and buildings
        alike.  Gunner rays are therefore walked outward and truncated at the
        first non-empty tile.  can_fire_from cannot substitute here: for gunners
        it requires the TARGET tile to be occupied, and a landing tile is empty
        until the throw lands.

        Ammo is a precondition, not a detail -- a line the team cannot pay to
        fire is decoration, and this bot starts every match at 0 ammunition.
        """
        cover = set()
        ammo = ct.get_global_ammo()
        seen = 0
        for eid in ct.get_nearby_buildings():
            if seen >= KIDNAP_MAX_TURRETS:
                break
            try:
                if ct.get_team(eid) != self.team:
                    continue
                et = ct.get_entity_type(eid)
                if et == EntityType.SENTINEL:
                    if ammo < KIDNAP_MIN_AMMO_SENTINEL:
                        continue
                elif et == EntityType.GUNNER:
                    if ammo < KIDNAP_MIN_AMMO_GUNNER:
                        continue
                else:
                    continue
                tp = ct.get_position(eid)
                tiles = ct.get_attackable_tiles_from(tp, ct.get_direction(eid), et)
            except Exception:
                continue
            seen += 1
            if et == EntityType.SENTINEL:
                for t in tiles:
                    cover.add((t.x, t.y))
                continue
            # get_attackable_tiles* enumerates in ABSOLUTE row-major order, not
            # along the ray (game-model.md) -- sort before truncating or the
            # near/far preference flips with facing.
            for t in sorted(tiles, key=lambda q: q.distance_squared(tp)):
                cover.add((t.x, t.y))
                if not self._kidnap_open(ct, t):
                    break
        return cover

    def _kidnap_ours(self, ct):
        """Neighbour-count map: (x, y) -> how many of our non-barrier buildings
        touch that tile.  Built by walking OUR buildings and stamping their
        8-rings, so it costs O(buildings) once instead of 8 lookups on each of
        ~85 candidate landing tiles.  Barriers are excluded on purpose: a
        hostile parked next to a 3 Ti wall costs nothing.
        """
        near = {}
        for eid in ct.get_nearby_buildings():
            try:
                if ct.get_team(eid) != self.team:
                    continue
                et = ct.get_entity_type(eid)
                if et == EntityType.BARRIER:
                    continue
                q = ct.get_position(eid)
            except Exception:
                continue
            seats = core_tiles(q) if et == EntityType.CORE else (q,)
            for s in seats:
                for d in DIRECTIONS:
                    k = (s.x + d.delta()[0], s.y + d.delta()[1])
                    near[k] = near.get(k, 0) + 1
        return near

    def _kidnap_victim(self, ct, bp, dest, cover):
        """Score one hostile in the pickup ring; also flag it a probable healer.

        WHY HEALERS RANK FIRST.  Per titanium: builder heal 4.00 HP/Ti, sentinel
        1.80, gunner 1.75, builder attack 1.00.  Healing beats the best damage
        source by 2.22x, so an attrition race at equal income is unwinnable --
        and a builder bot's attack hits BUILDINGS ONLY, so the only two ways to
        remove an enemy healer are a turret shot or this throw.  The throw costs
        no ammunition.

        The observable proxy is the heal's own precondition: heal targets a
        friendly entity on an ORTHOGONALLY adjacent tile, so a hostile standing
        cardinally next to a DAMAGED entity of its own team is a healer with a
        job.  hp == max_hp next door is not evidence of anything.

        AND THE TRIGGER (KIDNAP_V_UNDER_FIRE).  One healer is ~2 HP/round and
        three of them exactly cancel a Sentinel, so the kidnap flips an
        unwinnable exchange to a winnable one -- but ONLY while we are already
        shooting the thing being repaired.  `cover` is the set of tiles our
        loaded turret lines reach, so "the damaged entity stands on a covered
        tile" is the cheapest honest proxy for that, and it costs one set lookup
        on a value we computed anyway.
        """
        score = 0
        healer = False
        under_fire = False
        target = -1
        if dest is not None and dist_core(bp, dest) <= 1:
            score += KIDNAP_V_CORE_ADJ
        for d in CARDINALS:
            q = bp.add(d)
            try:
                ids = (ct.get_tile_building_id(q), ct.get_tile_builder_bot_id(q))
            except Exception:
                continue
            for oid in ids:
                if oid is None:
                    continue
                try:
                    tm = ct.get_team(oid)
                    if tm == self.team:
                        score += KIDNAP_V_ON_OUR_STUFF
                        continue
                    if ct.get_hp(oid) >= ct.get_max_hp(oid):
                        continue
                    et = ct.get_entity_type(oid)
                except Exception:
                    continue
                if not healer:
                    healer = True
                    target = oid
                    score += KIDNAP_V_HEALER
                if et in (EntityType.CORE, EntityType.SENTINEL,
                          EntityType.GUNNER, EntityType.LAUNCHER):
                    score += KIDNAP_V_HEALER_HIGHVALUE
                    target = oid
                if (q.x, q.y) in cover and not under_fire:
                    under_fire = True
                    score += KIDNAP_V_UNDER_FIRE
        return score, healer, under_fire, target

    def _kidnap(self, ct, lp, w, h, dest, enemy_bots):
        """PIECE KIDNAP.  Returns True iff a hostile was thrown.

        THE RULE, in order:
          1. Grab the most valuable hostile in the ring -- probable healer, then
             one sitting on their Core's ring, then anything.
          2. VETO any landing tile that is uncovered and inside our own home
             band, and every tile within 2 of our own Core footprint.  An
             uncovered hostile dropped at home is an imported saboteur, and that
             is the one way this plank can be worse than the exile it replaces.
          3. Among survivors maximise  killzone + walk-back + separation - our
             own adjacent economy.
          4. If nothing survives, return False and let the caller run the parent
             exile unchanged.

        DOMINANCE, so step 4 cannot make the common case worse: the parent's
        pick is the tile FARTHEST from our Core, which by construction is never
        inside the home band and so always survives the veto.  It is therefore
        always a member of the set this maximises over, and the tile chosen here
        scores at least as high as it under these weights.
        """
        if self._cpu_exhausted(ct):
            return False
        # Coverage first: victim selection needs it for the under-fire trigger,
        # and it is one scan either way.
        cover = self._kidnap_cover(ct)
        pick = None
        pick_s = None
        pick_heal = False
        pick_fire = False
        pick_tgt = -1
        for _eid, bp in enemy_bots:
            s, healer, fire, tgt = self._kidnap_victim(ct, bp, dest, cover)
            if pick_s is None or s > pick_s:
                pick, pick_s, pick_heal, pick_fire, pick_tgt = bp, s, healer, fire, tgt
        if pick is None:
            return False

        near = self._kidnap_ours(ct)
        # For a healer the payoff is SEPARATION AND TIME: every round it spends
        # walking back is a round the thing it was repairing keeps taking
        # damage, and unlike a raider it has a specific tile it must return to.
        sep_w = KIDNAP_W_SEP_HEAL if pick_heal else KIDNAP_W_SEP
        base_walk = dist_core(pick, dest) if dest is not None else 0
        scored = []
        for dx in range(-5, 6):
            for dy in range(-5, 6):
                if dx * dx + dy * dy > 26:
                    continue
                tx, ty = lp.x + dx, lp.y + dy
                if not (0 <= tx < w and 0 <= ty < h):
                    continue
                t = Position(tx, ty)
                covered = (tx, ty) in cover
                if dist_core(t, self.core) <= 2:
                    continue
                if not covered and t.distance_squared(self.core) <= KIDNAP_HOME_VETO_DSQ:
                    continue
                score = KIDNAP_W_KILLZONE if covered else 0
                walk = 0
                if dest is not None:
                    walk = dist_core(t, dest) - base_walk
                    if walk > KIDNAP_WALK_CLAMP:
                        walk = KIDNAP_WALK_CLAMP
                    elif walk < -KIDNAP_WALK_CLAMP:
                        walk = -KIDNAP_WALK_CLAMP
                    score += KIDNAP_W_WALKBACK * walk
                sep = max(abs(tx - pick.x), abs(ty - pick.y))
                if sep > KIDNAP_SEP_CLAMP:
                    sep = KIDNAP_SEP_CLAMP
                score += sep_w * sep
                n = near.get((tx, ty), 0)
                if n > KIDNAP_NEAR_CAP:
                    n = KIDNAP_NEAR_CAP
                score -= KIDNAP_W_NEAR_OURS * n
                scored.append((-score, tx, ty, covered, walk, sep))
        if not scored:
            return False
        scored.sort()
        for _neg, tx, ty, covered, walk, sep in scored:
            site = Position(tx, ty)
            if ct.can_launch(pick, site):
                self._kidnap_probe(ct, "KIDNAP", pick, site, covered, walk,
                                   sep, pick_heal, pick_tgt)
                ct.launch(pick, site)
                # THE WINDOW SIGNAL.  2 == "launcher alive AND a kidnap window
                # is open"; every existing reader of this slot tests truthiness
                # only, so this is bit-for-bit 1 to all of them (see
                # KIDNAP_AMMO_SURGE_ON).  Raised only when the throw actually
                # bought something to shoot: a covered landing tile, or a healer
                # pulled off something we are already firing at.  The launcher
                # rewrites 1 next turn, so the Core bursts exactly once.
                if KIDNAP_AMMO_SURGE_ON and (covered or pick_fire):
                    ct.write_store(SLOT_LAUNCHER, 2)
                return True
        return False

    def _launcher(self, ct):
        if self.team is None:
            self.team = ct.get_team()
        ct.write_store(SLOT_LAUNCHER, 1)
        if KIDNAP_PROBE:
            import sys
            _lp = ct.get_position()
            _md = -1
            _ring = 0
            for _e in ct.get_nearby_entities():
                try:
                    if (ct.get_entity_type(_e) != EntityType.BUILDER_BOT
                            or ct.get_team(_e) == self.team):
                        continue
                    _d = ct.get_position(_e).distance_squared(_lp)
                except Exception:
                    continue
                if _md < 0 or _d < _md:
                    _md = _d
                if _d <= 2:
                    _ring += 1
            print("KLIFE\tr=%d\tmind=%d\tring=%d"
                  % (ct.get_current_round(), _md, _ring), file=sys.stderr)
        if self.core is None:
            for eid in ct.get_nearby_buildings():
                if ct.get_entity_type(eid) == EntityType.CORE and ct.get_team(eid) == self.team:
                    self.core = ct.get_position(eid)
                    break
        if self.core is None:
            return
        w, h = ct.get_map_width(), ct.get_map_height()
        dest = unpack_pos(ct.read_store(SLOT_ENEMY_CORE))
        if dest is None:
            dest = Position(max(0, w - 2 - self.core.x), max(0, h - 2 - self.core.y))

        drop_sites = []
        for c in core_tiles(dest):
            for d in CARDINALS:
                t = c.add(d)
                if 0 <= t.x < w and 0 <= t.y < h and dist_core(t, dest) == 1:
                    drop_sites.append(t)
        for c in core_tiles(dest):
            for d in DIRECTIONS:
                t = c.add(d)
                if 0 <= t.x < w and 0 <= t.y < h and dist_core(t, dest) == 1:
                    drop_sites.append(t)
        for c in core_tiles(dest):
            for d in DIRECTIONS:
                t = c.add(d)
                if 0 <= t.x < w and 0 <= t.y < h and dist_core(t, dest) > 0:
                    drop_sites.append(t)
        seen, uniq = set(), []
        for s in drop_sites:
            key = (s.x, s.y)
            if key not in seen:
                seen.add(key)
                uniq.append(s)
        drop_sites = uniq

        lp = ct.get_position()
        cands = []
        chosen = ct.read_store(SLOT_LAUNCH_ID)
        chosen_rnd = ct.read_store(SLOT_LAUNCH_RND)
        if chosen and ct.get_current_round() - chosen_rnd > 5:
            ct.write_store(SLOT_LAUNCH_ID, 0)
            chosen = 0
        for eid in ct.get_nearby_entities():
            if ct.get_entity_type(eid) != EntityType.BUILDER_BOT or ct.get_team(eid) != self.team:
                continue
            if not chosen or eid + 1 != chosen:
                continue
            bp = ct.get_position(eid)
            if bp.distance_squared(lp) > 49:
                continue
            cands.append((bp.distance_squared(lp), bp))
        cands.sort(key=lambda x: x[0])

        # A Launcher can also remove a hostile bot that walks into its pickup
        # ring.  PIECE KIDNAP (see doctrine.py) chooses WHICH one to grab and
        # WHERE to put it; the legacy "farthest from our Core" exile below is
        # kept verbatim as the fallback and is what runs with KIDNAP_ON off,
        # so the ablation measures exactly this change and nothing else.
        enemy_bots = []
        for eid in ct.get_nearby_entities():
            if ct.get_entity_type(eid) != EntityType.BUILDER_BOT or ct.get_team(eid) == self.team:
                continue
            bp = ct.get_position(eid)
            if bp.distance_squared(lp) <= 2:
                enemy_bots.append((eid, bp))
        if KIDNAP_PROBE:
            import time
            self.kidnap_t0 = time.process_time()
        if enemy_bots and KIDNAP_ON:
            # Blanket guard: anything escaping run() destroys this unit for the
            # rest of the match, so a bug in the new rule costs one throw's
            # quality, never the launcher.
            try:
                if self._kidnap(ct, lp, w, h, dest, enemy_bots):
                    return
            except Exception:
                pass
        for _eid, bp in enemy_bots:
            exile = []
            for dx in range(-5, 6):
                for dy in range(-5, 6):
                    if dx * dx + dy * dy > 26:
                        continue
                    t = Position(lp.x + dx, lp.y + dy)
                    if 0 <= t.x < w and 0 <= t.y < h:
                        exile.append(t)
            exile.sort(key=lambda t: t.distance_squared(self.core), reverse=True)
            for site in exile:
                if ct.can_launch(bp, site):
                    self._kidnap_probe(ct, "EXILE", bp, site, 0, 0, 0, False, -1)
                    ct.launch(bp, site)
                    return

        for _, bp in cands:
            for site in drop_sites:
                if ct.can_launch(bp, site):
                    ct.launch(bp, site)
                    ct.write_store(SLOT_DROPPED, ct.read_store(SLOT_DROPPED) + 1)
                    ct.write_store(SLOT_LAUNCHED_ID, chosen)
                    ct.write_store(SLOT_LAUNCH_ID, 0)
                    return
            if ct.can_launch(bp, dest):
                ct.launch(bp, dest)
                ct.write_store(SLOT_DROPPED, ct.read_store(SLOT_DROPPED) + 1)
                ct.write_store(SLOT_LAUNCHED_ID, chosen)
                ct.write_store(SLOT_LAUNCH_ID, 0)
                return

            # Most maps are wider than the Launcher's sqrt(26) throw radius.
            # Leap the waiting bot as far toward the enemy as the local terrain
            # permits instead of idling forever on an impossible destination.
            advance = []
            for dx in range(-5, 6):
                for dy in range(-5, 6):
                    if dx * dx + dy * dy > 26:
                        continue
                    site = Position(lp.x + dx, lp.y + dy)
                    if 0 <= site.x < w and 0 <= site.y < h:
                        advance.append(site)
            advance.sort(key=lambda t: t.distance_squared(dest))
            for site in advance:
                if site.distance_squared(dest) >= bp.distance_squared(dest):
                    continue
                if ct.can_launch(bp, site):
                    ct.launch(bp, site)
                    ct.write_store(SLOT_DROPPED, ct.read_store(SLOT_DROPPED) + 1)
                    ct.write_store(SLOT_LAUNCHED_ID, chosen)
                    ct.write_store(SLOT_LAUNCH_ID, 0)
                    return
