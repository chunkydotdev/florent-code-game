"""rush_probe_fast -- the top-meta Launcher-insertion rush, replicated.

Forked from bots/rush_probe (the verified "walked" rush). That bot proved the
swarm-rush shape (attackers, enemy sentinels, one ring blocker) but starts on
foot and runs no real economy, so it starves its own turrets and leaves its
own Core undefended -- see docs/opponents.md "Albert And Einstein": the top
of the ladder opens Builder Bot turn 0 -> Launcher turn 1 -> Sentinel(s) turn
4-15, using the Launcher to throw the opening scout 6-8 tiles instantly
(docs/game-model.md, "Used offensively on your OWN builder").

Delta vs rush_probe, kept minimal:
  1. Opener: one builder builds a Launcher adjacent to our own Core early;
     the Launcher then throws adjacent friendly builders toward the enemy
     Core (throw r²=26 from the Launcher, not the bot) -- one instant hop,
     then the thrown builder walks the rest, same as the field does it.
  2. Sustaining economy: 2-3 dedicated builders harvest near home and lay a
     full conveyor chain back to the Core as they walk it, each tile facing
     the next tile on the path (rush_probe's single-tile conveyor is a
     dead-end for anything not immediately adjacent to the Core; crediting
     is delivery-only, so a broken chain earns zero) -- this is what keeps
     ammo flowing once Sentinels start firing.
  3. 1-2 home Sentinels, built once an economy builder's chain is done, so
     the Core isn't undefended (rush_probe's Core died 22x to 5 kills).

Infrastructure (movement, stuck-detection, spawn-ring enumeration, CPU guard,
the top-level try/except) is inherited unchanged. See docs/game-model.md and
docs/reference/official-docs.md for the API details this relies on (12-tile
spawn ring geometry, tile-query vision guarding, sentinel targeting order,
Launcher pickup/throw radii).

Entity types used: Core, Builder Bot, Sentinel, Launcher.

Communication store slots:
  0  SLOT_CORE_X          Our Core's X position (written by the core)
  1  SLOT_CORE_Y          Our Core's Y position
  2  SLOT_HARVESTER_COUNT Economy harvesters actually built (target: 2-3)
  3  SLOT_SENTINEL_COUNT  Sentinels built near the enemy Core (target: 3)
  4  SLOT_BLOCKER_ID      Entity id (+1; 0 = unclaimed) of the current ring-blocker
  5  SLOT_BLOCKER_PING    Round the current blocker last confirmed it's alive
  6  SLOT_ENEMY_CORE      Packed (x, y) of the enemy Core once directly sighted
  7  SLOT_LAUNCHER_CLAIM  Entity id (+1) of the builder assigned to build the Launcher
  8  SLOT_LAUNCHER_BUILT  1 once the opener Launcher exists
  9  SLOT_HOME_SENTINEL_COUNT Home-defense Sentinels built (target: 2)
  10 SLOT_ECON_CLAIM      Count of builders claimed for the dedicated harvester role
  11-13 SLOT_HARVESTER_IDS Entity id (+1) of each economy builder -- the Launcher
                        skips these so it never throws one off its route
"""

import math
import random
import sys

from fcode import Controller, Direction, EntityType, Environment, GameError, Position

# Cardinal directions only -- movement, and anything "orthogonally adjacent"
# (builds, heals, fires): conveyors/splitters/heal/fire/build all require it.
CARDINALS = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]

# --- Debug instrumentation -------------------------------------------------
# Set True to get round-numbered stderr evidence (tag RUSHFAST) of opener
# milestones (event=launcher_built/first_throw/contact/first_turret/
# first_shot) plus the swarm/blocker/economy detail underneath them.
# Silenced (False) is the shipped state -- flip only for verification runs.
DEBUG = False


def _dbg(msg: str) -> None:
    if DEBUG:
        print(f"RUSHFAST {msg}", file=sys.stderr)


# --- Communication store slot assignments ---
SLOT_CORE_X = 0
SLOT_CORE_Y = 1
SLOT_HARVESTER_COUNT = 2
SLOT_SENTINEL_COUNT = 3
SLOT_BLOCKER_ID = 4
SLOT_BLOCKER_PING = 5
SLOT_ENEMY_CORE = 6
SLOT_LAUNCHER_CLAIM = 7
SLOT_LAUNCHER_BUILT = 8
SLOT_HOME_SENTINEL_COUNT = 9
SLOT_ECON_CLAIM = 10
# One slot per economy builder (id+1, 0=unfilled) -- the Launcher reads
# these to avoid throwing a "harvester"-role unit off its route (see
# _run_launcher). Fixed-size, sized to TARGET_HARVESTERS.
SLOT_HARVESTER_IDS = (11, 12, 13)

# How many builder bots the core will try to spawn over the game. In practice
# cost-scaling (+20% per builder, additive) makes this ceiling essentially
# irrelevant -- affordability is what actually paces spawning, this just
# stops us from spawning forever if titanium ever gets absurd.
MAX_BUILDERS = 30

# Send an initial wave before the Core starts reserving titanium for
# Sentinels (below) -- enough bodies that some are usually already close to
# the enemy Core by the time the reserve kicks in.
MIN_BUILDERS_BEFORE_RESERVING = 6

# Dedicated economy builders (role "harvester"): claimed once at spawn (see
# _resolve_role), each finds nearby ore, builds a harvester, then walks the
# output back to the Core laying a real conveyor chain -- unlike rush_probe's
# opportunistic single-tile stub, this one actually delivers (crediting is
# delivery-only). Needed to sustain ammo conversion once Sentinels are firing.
TARGET_HARVESTERS = 3

# How far (Chebyshev, in tiles) an economy builder with no ore in sight will
# wander while still looking, capped so it stays near home rather than
# drifting into enemy territory on a small map (see _pick_econ_target).
ECON_WANDER_RADIUS = 7

# Sentinels built adjacent to the enemy Core, facing it.
SENTINEL_TARGET = 3

# A builder only attempts a sentinel build once within this squared distance
# of the enemy Core -- otherwise it just keeps walking.
SENTINEL_BUILD_RANGE_SQ = 18

# Home-defense Sentinels, built by an economy builder once its harvester
# chain reaches the Core -- so the base isn't undefended while the swarm is
# busy rushing (rush_probe's Core died 22x to 5 kills with zero home defense).
HOME_SENTINEL_TARGET = 2

# Squared distance from our own Core within which the opener Launcher and
# home Sentinels may be built -- the same dist_sq=8 superset bound the Core
# itself uses to enumerate its 12-tile spawn ring (see _run_core), so both
# stay genuinely "adjacent to our own Core".
HOME_BUILD_RANGE_SQ = 8

# Global ammo buffer. 3 Sentinels reloading every 2 rounds cost at most
# 15 ammo / 2 rounds; this buffer is a large multiple of that so conversion
# never bottlenecks firing. This bot has no reason to hoard titanium instead
# -- but only ONCE the swarm is done paying for Sentinels. Diverting the
# full buffer out of the starting 500 Ti on round 1, before any Sentinel
# exists to spend it, was measured (2026-08-06 verification pass) to starve
# early builder spawning and roughly triple how long the first attacker took
# to reach the enemy Core (round ~180 instead of ~60 on lighthouse) -- and
# even after that fix, an EARLY_AMMO_BUFFER that grew the moment the first
# Sentinel existed went right on competing with the Core's reserve for
# Sentinels #2 and #3. Keep a small buffer at all times (enough for a
# freshly-built Sentinel to fire immediately) and only ramp up to the full
# buffer once all SENTINEL_TARGET are built and nothing is competing for
# the pool anymore.
EARLY_AMMO_BUFFER = 40
AMMO_BUFFER = 200

# If the current spawn-ring blocker hasn't refreshed its heartbeat in this
# many rounds, presume it dead and let another builder reclaim the role.
BLOCKER_STALE_ROUNDS = 10

# CPU budget bail-out threshold in microseconds (see aug7 for the full
# rationale) -- bail at a phase boundary ourselves rather than let the
# engine truncate mid-statement.
CPU_BUDGET_US = 8000


def pack_pos(pos: Position) -> int:
    """Encode a position into a single u32 for the communication store.

    Offset by +1 so (0, 0) doesn't encode as 0, which means "no data".
    """
    return ((pos.x + 1) << 16) | (pos.y + 1)


def unpack_pos(val: int) -> Position | None:
    """Decode a position from the communication store. None if empty (0)."""
    if val == 0:
        return None
    return Position((val >> 16) - 1, (val & 0xFFFF) - 1)


def in_bounds(ct: Controller, pos: Position) -> bool:
    """True if pos is on the map.

    Necessary but NOT sufficient before a tile query: get_tile_env(),
    is_tile_passable() and get_tile_building_id() also raise GameError for
    an in-bounds tile outside current vision, with the identical message as
    off-map -- so in-bounds callers still need a try/except.
    """
    return 0 <= pos.x < ct.get_map_width() and 0 <= pos.y < ct.get_map_height()


def cardinal_toward(src: Position, dst: Position) -> Direction | None:
    """The cardinal direction that points most directly from src to dst.

    Comparing |dx| and |dy| directly (rather than snapping an already
    45-degree-quantised Direction) is exact and equivariant under rotation
    and reflection -- see aug7 for the measured rationale. Ties broken at
    random rather than by absolute compass direction.
    """
    dx = dst.x - src.x
    dy = dst.y - src.y
    if dx == 0 and dy == 0:
        return None
    if abs(dx) > abs(dy):
        return Direction.EAST if dx > 0 else Direction.WEST
    if abs(dy) > abs(dx):
        return Direction.SOUTH if dy > 0 else Direction.NORTH
    if random.random() < 0.5:
        return Direction.EAST if dx > 0 else Direction.WEST
    return Direction.SOUTH if dy > 0 else Direction.NORTH


def core_footprint(nw: Position) -> list[Position]:
    """The 4 tiles of a Core's 2x2 footprint, given its NW corner."""
    return [nw, Position(nw.x + 1, nw.y), Position(nw.x, nw.y + 1), Position(nw.x + 1, nw.y + 1)]


def nearest_core_tile(pos: Position, core_nw: Position) -> Position:
    """Whichever of the Core's 4 footprint tiles is nearest to pos."""
    return min(core_footprint(core_nw), key=lambda t: pos.distance_squared(t))


def spawn_ring(core_nw: Position) -> list[Position]:
    """The 12-tile ring orthogonally or diagonally adjacent to a Core's 2x2
    footprint -- exactly its legal spawn tiles (docs/game-model.md,
    verified tile-by-tile in bots/probe_spawn), and so also the tiles a
    body-blocking builder wants to occupy.
    """
    tiles = []
    for dx in range(-1, 3):
        for dy in range(-1, 3):
            if 0 <= dx <= 1 and 0 <= dy <= 1:
                continue  # inside the footprint itself
            tiles.append(Position(core_nw.x + dx, core_nw.y + dy))
    return tiles


class Player:
    def __init__(self):
        # Core: how many builder bots it has spawned
        self.num_spawned = 0

        # Builder bot navigation state
        self.target: Position | None = None
        self.last_pos: Position | None = None
        self.stuck = 0
        # "attacker", "blocker", "launcher_builder" or "harvester"
        self.role: str | None = None
        self.harvester_done = False  # "harvester" role: harvester built, now walking home
        self.chain_gap: Position | None = None  # "harvester" role: see _try_close_chain_gap
        self.dbg_thrown = False  # Launcher only: one-shot first-throw debug flag

        # Cached positions
        self.core_pos: Position | None = None    # our own Core (home)
        self.enemy_pos: Position | None = None   # enemy Core NW corner (estimate or exact)
        self.enemy_confirmed = False              # True once directly sighted (ours or a teammate's)

        # One-shot debug flags so a chatty per-round condition prints once
        self.dbg_reached_enemy = False
        self.dbg_blocker_in_ring = False
        self.dbg_fired = False

        self.reported_error = False
        self.reported_cpu = False

    def run(self, ct: Controller) -> None:
        """Entry point. An exception escaping run() permanently deletes the
        unit for the rest of the match, so this guard is unconditional --
        never remove it, and never wrap it in try/finally (rejected by the
        bot-code validator).
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
        elif etype == EntityType.SENTINEL:
            self._run_sentinel(ct)
        elif etype == EntityType.LAUNCHER:
            self._run_launcher(ct)

    def _cpu_exhausted(self, ct: Controller) -> bool:
        """True once this unit has used CPU_BUDGET_US of its 10ms this round.
        Callers bail at a phase boundary so a slow round degrades gracefully
        instead of being truncated mid-statement by the engine.
        """
        if ct.get_cpu_time_elapsed() < CPU_BUDGET_US:
            return False
        if not self.reported_cpu:
            self.reported_cpu = True
            print(
                f"CPU-GUARD tripped: round={ct.get_current_round()} "
                f"elapsed_us={ct.get_cpu_time_elapsed()}",
                file=sys.stderr,
            )
        return True

    # ------------------------------------------------------------------
    # Core
    # ------------------------------------------------------------------

    def _run_core(self, ct: Controller) -> None:
        """Publish our position, then spend titanium in strict priority
        order: reserve toward the next Sentinel first, then ammo, then
        builder spawning -- no gating on economy otherwise.

        The reserve exists because an unreserved Core happily out-competes
        its own attackers for every spare Ti round after round: builder
        cost is cheap and the spawn check runs every round, while Sentinel
        cost is ~2.5x steeper by the time anyone's in range and only gets
        spent opportunistically by whichever builder happens to be
        standing next to the enemy Core with an action free. Measured
        2026-08-06: without this, the team spawned a large swarm and sat on
        it for the full 1000-round match without ever affording a single
        Sentinel. Ammo conversion is deliberately kept small (see
        AMMO_BUFFER) and subordinate to the reserve too, for the same
        reason -- it was quietly winning the same race.
        """
        pos = ct.get_position()
        ct.write_store(SLOT_CORE_X, pos.x)
        ct.write_store(SLOT_CORE_Y, pos.y)

        sentinel_count = ct.read_store(SLOT_SENTINEL_COUNT)
        reserving = self.num_spawned >= MIN_BUILDERS_BEFORE_RESERVING and sentinel_count < SENTINEL_TARGET
        reserve = ct.get_sentinel_cost() if reserving else 0

        # Ammo conversion doesn't use the action cooldown, so it never costs
        # us a spawn -- try it every round, but only with what's left after
        # protecting both a builder's cost and the Sentinel reserve above.
        # Chase the full buffer only once the swarm owes no more Sentinels;
        # until then keep it small so it isn't ALSO competing for the
        # reserve.
        buffer = AMMO_BUFFER if sentinel_count >= SENTINEL_TARGET else EARLY_AMMO_BUFFER
        ammo = ct.get_global_ammo()
        if ammo < buffer:
            spare = ct.get_global_resources() - ct.get_builder_bot_cost() - reserve
            amount = min(buffer - ammo, spare)
            if amount > 0 and ct.can_convert_ammo(amount):
                ct.convert_ammo(amount)

        if self.num_spawned >= MAX_BUILDERS:
            return

        ti = ct.get_global_resources()
        cost = ct.get_builder_bot_cost()
        if ti < cost + reserve:
            return

        # Spawn from the WHOLE 12-tile ring, not just pos.add(d) (which only
        # reaches the N/W sides of it -- an absolute-direction bug that
        # handed entire maps to one seat; see aug7). dist_sq=8 is a superset
        # bound that can_spawn() then filters exactly down to the ring.
        candidates = [t for t in ct.get_nearby_tiles(dist_sq=8) if ct.can_spawn(t)]
        if candidates:
            ct.spawn_builder(random.choice(candidates))
            self.num_spawned += 1

    # ------------------------------------------------------------------
    # Builder bot
    # ------------------------------------------------------------------

    def _run_builder(self, ct: Controller) -> None:
        """Builder bot logic. Priority order:
        1. Resolve our role (attacker / blocker / launcher_builder /
           harvester) -- cheap, and the blocker's heartbeat needs to survive
           CPU pressure.
        2. Build, by role: launcher_builder -> the opener Launcher;
           harvester -> its harvester, then (once done) a home Sentinel;
           attacker -> a Sentinel near the enemy Core (capped); blocker ->
           nothing. Whoever didn't act tries to heal instead.
        3. Move toward our target (enemy Core for attackers, home for
           launcher_builder/harvester, a ring tile for the blocker) --
           reuses aug7's movement/stuck-detection verbatim.
        """
        pos = ct.get_position()

        if self.core_pos is None:
            self._read_core_pos(ct)
        if self.core_pos is not None:
            self._sync_enemy_core(ct)

        if self.last_pos == pos:
            self.stuck += 1
        else:
            self.stuck = 0
        self.last_pos = pos

        self._resolve_role(ct)

        if DEBUG:
            self._debug_milestones(ct, pos)

        if self._cpu_exhausted(ct):
            return

        if ct.get_action_cooldown() == 0:
            acted = False
            if self.role == "launcher_builder":
                if self._try_build_launcher(ct):
                    acted = True
                    # Job done -- become an attacker (and prime candidate to
                    # be the Launcher's own first throw, since it's likely
                    # still standing right next to it). SLOT_LAUNCHER_BUILT
                    # is buffered and won't be visible for a round, so
                    # without this the sticky role would try to build a
                    # SECOND Launcher next round [measured: it did].
                    self.role = "attacker"
            elif self.role == "harvester":
                if not self.harvester_done:
                    if self._try_build_harvester(ct):
                        self.harvester_done = True
                        self.chain_gap = ct.get_position()
                        acted = True
                elif self.chain_gap is not None:
                    acted = self._try_close_chain_gap(ct)
                else:
                    acted = self._try_build_home_sentinel(ct)
            elif self.role != "blocker":
                acted = self._try_build_sentinel_near_enemy(ct)
            if not acted:
                self._try_heal(ct)

        if self._cpu_exhausted(ct):
            return

        self._move_toward_target(ct)

    def _debug_milestones(self, ct: Controller, pos: Position) -> None:
        """One-shot stderr evidence for the two milestones that are easy to
        miss if only checked at target-repick time (attackers/blocker only
        re-evaluate their target on arrival or when stuck, so a check placed
        there can lag the round the condition actually first became true).
        Checked every round instead, at negligible cost, and only when
        DEBUG -- never runs in the shipped (DEBUG=False) bot.
        """
        if self.enemy_pos is None:
            return
        if self.role == "blocker":
            if not self.dbg_blocker_in_ring and pos in spawn_ring(self.enemy_pos):
                self.dbg_blocker_in_ring = True
                _dbg(f"round={ct.get_current_round()} unit={ct.get_id()} occupying ring tile {pos}")
        elif not self.dbg_reached_enemy:
            d = pos.distance_squared(self.enemy_pos)
            if d <= SENTINEL_BUILD_RANGE_SQ:
                self.dbg_reached_enemy = True
                _dbg(f"r={ct.get_current_round()} event=contact unit={ct.get_id()} dist_sq={d}")

    def _read_core_pos(self, ct: Controller) -> None:
        """Read our own Core's position from the store (written round 1,
        visible from round 2). Skip (0, 0) unless the core really is there.
        """
        x = ct.read_store(SLOT_CORE_X)
        y = ct.read_store(SLOT_CORE_Y)
        if x > 0 or y > 0:
            self.core_pos = Position(x, y)

    def _sync_enemy_core(self, ct: Controller) -> None:
        """Establish where the enemy Core is, cheaply, without ever
        re-querying a tile we can't currently see.

        1. If a teammate already confirmed a sighting, adopt it -- free.
        2. Otherwise compute the point-reflection through the map centre
           (maps are symmetric, so this is exact or very close): for our
           Core's NW corner (cx, cy) on a WxH map, the enemy's is
           (W-2-cx, H-2-cy).
        3. Once we personally see the enemy Core, replace the estimate with
           the exact position and publish it for everyone else.
        Stops scanning once confirmed, by anyone -- get_nearby_buildings()
        is vision-bounded and cheap, but no reason to keep paying for it.
        """
        if self.enemy_confirmed:
            return
        stored = unpack_pos(ct.read_store(SLOT_ENEMY_CORE))
        if stored is not None:
            self.enemy_pos = stored
            self.enemy_confirmed = True
            return
        if self.enemy_pos is None:
            w, h = ct.get_map_width(), ct.get_map_height()
            self.enemy_pos = Position(max(0, w - 2 - self.core_pos.x), max(0, h - 2 - self.core_pos.y))
        my_team = ct.get_team()
        for bid in ct.get_nearby_buildings():
            if ct.get_team(bid) == my_team:
                continue
            if ct.get_entity_type(bid) == EntityType.CORE:
                exact = ct.get_position(bid)
                self.enemy_pos = exact
                self.enemy_confirmed = True
                ct.write_store(SLOT_ENEMY_CORE, pack_pos(exact))
                _dbg(f"round={ct.get_current_round()} unit={ct.get_id()} sighted enemy core at {exact}")
                return

    def _resolve_role(self, ct: Controller) -> None:
        """Dynamically resolve attacker vs. blocker every round from the
        comms store, rather than fixing a role once at spawn -- so if the
        blocker dies, whichever attacker next passes through the check
        below picks the role back up.

        SLOT_BLOCKER_ID holds (unit_id + 1) of the current claimant, or 0
        if unclaimed. The claimant refreshes SLOT_BLOCKER_PING every round;
        if it goes stale (presumed dead), the next builder to check reclaims
        the role. Multiple builders racing to claim the same round is a
        benign, self-correcting race (buffered writes mean only one value
        survives into next round) -- not worth a stricter protocol for a
        probe.
        """
        # "launcher_builder" and "harvester" are one-shot jobs: claimed at
        # most once per unit, on its first-ever resolution (self.role is
        # still None), then remembered locally for the rest of that unit's
        # life -- the early return at the top of this method skips straight
        # past all of the below once either is set. Neither supports the
        # blocker's mid-game reclaim-if-stale below; acceptable for a probe,
        # and moot in practice because the Core spawns at most one new
        # builder per round (its own action cooldown), so these claims are
        # never contested by two units in the same round.
        if self.role in ("launcher_builder", "harvester"):
            return
        fresh = self.role is None
        if fresh and ct.read_store(SLOT_LAUNCHER_BUILT) == 0 and ct.read_store(SLOT_LAUNCHER_CLAIM) == 0:
            ct.write_store(SLOT_LAUNCHER_CLAIM, ct.get_id() + 1)
            self.role = "launcher_builder"
            _dbg(f"r={ct.get_current_round()} event=launcher_claimed unit={ct.get_id()}")
            return

        my_token = ct.get_id() + 1
        rnd = ct.get_current_round()
        claimant = ct.read_store(SLOT_BLOCKER_ID)

        if claimant == my_token:
            self.role = "blocker"
            ct.write_store(SLOT_BLOCKER_PING, rnd)
            return

        if claimant == 0:
            ct.write_store(SLOT_BLOCKER_ID, my_token)
            ct.write_store(SLOT_BLOCKER_PING, rnd)
            self.role = "blocker"
            _dbg(f"round={rnd} unit={ct.get_id()} claims blocker role (unclaimed)")
            return

        last_ping = ct.read_store(SLOT_BLOCKER_PING)
        if last_ping and rnd - last_ping > BLOCKER_STALE_ROUNDS:
            ct.write_store(SLOT_BLOCKER_ID, my_token)
            ct.write_store(SLOT_BLOCKER_PING, rnd)
            self.role = "blocker"
            _dbg(f"round={rnd} unit={ct.get_id()} reclaims stale blocker role (idle since {last_ping})")
            return

        econ_idx = ct.read_store(SLOT_ECON_CLAIM)
        if fresh and econ_idx < TARGET_HARVESTERS:
            ct.write_store(SLOT_ECON_CLAIM, econ_idx + 1)
            ct.write_store(SLOT_HARVESTER_IDS[econ_idx], ct.get_id() + 1)
            self.role = "harvester"
            _dbg(f"r={ct.get_current_round()} event=econ_claimed unit={ct.get_id()}")
            return

        self.role = "attacker"

    def _try_build_launcher(self, ct: Controller) -> bool:
        """Build the opener Launcher on a tile adjacent to our own Core --
        turn ~1, mirroring the top-meta rush (docs/opponents.md, Albert And
        Einstein: Builder Bot turn 0 -> Launcher turn 1 -> Sentinel(s) turn
        4-15). No facing to compute -- build_launcher() takes a position
        only, Launchers have none.
        """
        if self.core_pos is None:
            return False
        ti = ct.get_global_resources()
        cost = ct.get_launcher_cost()
        if ti < cost:
            return False
        pos = ct.get_position()
        if pos.distance_squared(self.core_pos) > HOME_BUILD_RANGE_SQ:
            return False
        dirs = list(CARDINALS)
        random.shuffle(dirs)
        for d in dirs:
            build_pos = pos.add(d)
            if ct.can_build_launcher(build_pos):
                ct.build_launcher(build_pos)
                ct.write_store(SLOT_LAUNCHER_BUILT, 1)
                _dbg(f"r={ct.get_current_round()} event=launcher_built pos={build_pos} unit={ct.get_id()}")
                return True
        return False

    def _try_build_harvester(self, ct: Controller) -> bool:
        """Opportunistic only -- never a dedicated detour. If ore happens to
        be adjacent right now, grab it (capped at TARGET_HARVESTERS by the
        caller) and lay one conveyor home so it isn't wasted production.
        """
        ti = ct.get_global_resources()
        cost = ct.get_harvester_cost()
        if ti < cost:
            return False

        pos = ct.get_position()
        dirs = list(CARDINALS)
        random.shuffle(dirs)
        for d in dirs:
            build_pos = pos.add(d)
            if ct.can_build_harvester(build_pos):
                ct.build_harvester(build_pos)
                count = ct.read_store(SLOT_HARVESTER_COUNT)
                ct.write_store(SLOT_HARVESTER_COUNT, count + 1)
                self._try_build_conveyor_toward_core(ct, build_pos)
                self.target = None  # don't linger trying to walk onto it
                _dbg(f"r={ct.get_current_round()} event=harvester_built pos={build_pos} unit={ct.get_id()}")
                return True
        return False

    def _try_build_conveyor_toward_core(self, ct: Controller, harvester_pos: Position) -> None:
        """Place a conveyor adjacent to a harvester, facing toward our own
        Core, so the rare harvester we do build actually credits titanium
        (crediting is delivery-only -- an unlinked harvester produces
        nothing).
        """
        if self.core_pos is None:
            return
        ti = ct.get_global_resources()
        cost = ct.get_conveyor_cost()
        if ti < cost:
            return
        facing = cardinal_toward(harvester_pos, self.core_pos)
        if facing is None:
            return  # harvester is exactly on the core tile (shouldn't happen)
        conv_pos = harvester_pos.add(facing)
        if ct.can_build_conveyor(conv_pos, facing):
            ct.build_conveyor(conv_pos, facing)

    def _try_close_chain_gap(self, ct: Controller) -> bool:
        """One-shot fixup for a real gap in the chain: the tile a "harvester"
        role builder is STANDING ON when it finishes building (its position
        at that moment, adjacent to the harvester by construction, cached
        as self.chain_gap) can never itself get a conveyor -- "never its own
        tile" -- so it's structurally excluded from both
        _try_build_conveyor_toward_core (which places a conveyor relative to
        the HARVESTER, not the builder, and silently no-ops in exactly the
        geometry where the two coincide) and _try_move_laying_conveyor
        (which only builds on tiles AHEAD as we walk, never the one behind
        us). Measured 2026-08-06: without this, a harvester built this way
        delivered 0 titanium all game despite a "connected-looking" trail
        leading away from it -- the one tile touching the harvester was
        simply never a conveyor.

        Fixed here once the builder has taken its first step away (now
        adjacent to, but no longer standing on, self.chain_gap): build a
        conveyor there, facing toward wherever we are now -- exactly
        bridging harvester -> chain_gap -> the rest of the trail
        _try_move_laying_conveyor lays from here on.
        """
        pos = ct.get_position()
        if pos == self.chain_gap:
            return False  # haven't moved off it yet
        if pos.distance_squared(self.chain_gap) != 1:
            # Cardinal movement only, so this shouldn't happen -- but don't
            # get stuck retrying forever against a stale/unreachable gap.
            self.chain_gap = None
            return False
        facing = self.chain_gap.direction_to(pos)
        if ct.can_build_conveyor(self.chain_gap, facing):
            ct.build_conveyor(self.chain_gap, facing)
            _dbg(f"r={ct.get_current_round()} event=chain_gap_closed pos={self.chain_gap} facing={facing.name}")
            self.chain_gap = None
            return True
        return False

    def _try_build_sentinel_near_enemy(self, ct: Controller) -> bool:
        """Build a Sentinel adjacent to the enemy Core, facing it, once
        we're close enough. Facing is computed from the actual candidate
        build tile (not our own position) so the attack line is aimed at
        whichever footprint tile is really nearest the turret.
        """
        if self.enemy_pos is None:
            return False
        count = ct.read_store(SLOT_SENTINEL_COUNT)
        if count >= SENTINEL_TARGET:
            return False
        ti = ct.get_global_resources()
        cost = ct.get_sentinel_cost()
        if ti < cost:
            return False

        pos = ct.get_position()
        if pos.distance_squared(self.enemy_pos) > SENTINEL_BUILD_RANGE_SQ:
            return False

        dirs = list(CARDINALS)
        random.shuffle(dirs)
        for d in dirs:
            build_pos = pos.add(d)
            target_tile = nearest_core_tile(build_pos, self.enemy_pos)
            facing = build_pos.direction_to(target_tile)
            if facing == Direction.CENTRE:
                continue
            if ct.can_build_sentinel(build_pos, facing):
                ct.build_sentinel(build_pos, facing)
                ct.write_store(SLOT_SENTINEL_COUNT, count + 1)
                event = "first_turret" if count == 0 else "sentinel_built"
                _dbg(
                    f"r={ct.get_current_round()} event={event} sentinel #{count + 1} built "
                    f"at {build_pos} facing {facing.name} by unit={ct.get_id()}"
                )
                return True
        return False

    def _try_build_home_sentinel(self, ct: Controller) -> bool:
        """Build a defensive Sentinel adjacent to our OWN Core, facing
        outward (away from the Core) -- called only once an economy
        builder's harvester chain is done and it has walked back home (see
        _pick_econ_target). Mirrors _try_build_sentinel_near_enemy above,
        aimed the opposite way: rush_probe's Core died 22x to 5 kills with
        zero home defense; this is the fix.
        """
        if self.core_pos is None:
            return False
        count = ct.read_store(SLOT_HOME_SENTINEL_COUNT)
        if count >= HOME_SENTINEL_TARGET:
            return False
        ti = ct.get_global_resources()
        cost = ct.get_sentinel_cost()
        if ti < cost:
            return False

        pos = ct.get_position()
        if pos.distance_squared(self.core_pos) > HOME_BUILD_RANGE_SQ:
            return False

        dirs = list(CARDINALS)
        random.shuffle(dirs)
        for d in dirs:
            build_pos = pos.add(d)
            inward = build_pos.direction_to(nearest_core_tile(build_pos, self.core_pos))
            if inward == Direction.CENTRE:
                continue
            facing = inward.opposite()
            if ct.can_build_sentinel(build_pos, facing):
                ct.build_sentinel(build_pos, facing)
                ct.write_store(SLOT_HOME_SENTINEL_COUNT, count + 1)
                event = "first_turret" if count == 0 else "home_sentinel_built"
                _dbg(
                    f"r={ct.get_current_round()} event={event} home sentinel #{count + 1} "
                    f"built at {build_pos} facing {facing.name} by unit={ct.get_id()}"
                )
                return True
        return False

    def _try_heal(self, ct: Controller) -> bool:
        """Heal a damaged friendly building or bot on an adjacent tile --
        cheap, and keeps our Sentinels/blocker alive under fire."""
        pos = ct.get_position()
        dirs = list(CARDINALS)
        random.shuffle(dirs)
        for d in dirs:
            check = pos.add(d)
            if ct.can_heal(check):
                ct.heal(check)
                return True
        return False

    # ------------------------------------------------------------------
    # Builder bot -- movement (unchanged from aug7: role only decides what
    # _pick_target returns, the walking/stuck-recovery logic is generic)
    # ------------------------------------------------------------------

    def _move_toward_target(self, ct: Controller) -> None:
        if ct.get_move_cooldown() != 0:
            return

        pos = ct.get_position()

        if self.target is None or pos == self.target or self.stuck >= 3:
            self.target = self._pick_target(ct)
            self.stuck = 0
        if self.target is None:
            return

        dx = self.target.x - pos.x
        dy = self.target.y - pos.y
        productive = []
        if dx > 0:
            productive.append(Direction.EAST)
        elif dx < 0:
            productive.append(Direction.WEST)
        if dy > 0:
            productive.append(Direction.SOUTH)
        elif dy < 0:
            productive.append(Direction.NORTH)
        if not productive:
            return
        desired = random.choice(productive)

        perpendicular = [d for d in CARDINALS if d not in (desired, desired.opposite())]
        random.shuffle(perpendicular)
        alternatives = [desired, *perpendicular, desired.opposite()]
        mover = self._try_move
        if self.role == "harvester" and self.harvester_done:
            mover = self._try_move_laying_conveyor
        for d in alternatives:
            if mover(ct, d):
                return

    def _try_move(self, ct: Controller, d: Direction) -> bool:
        """Try to move one step in direction d.

        aug7 also drops a conveyor toward home on every empty tile it steps
        onto, building out a resource network as builders wander. We
        deliberately DON'T reuse that part for attackers/blocker: it spends
        titanium and adds +1% cost-scale per conveyor for a supply network
        this bot has no use for on that path, and measured against a live
        opponent it was competing with Sentinel-building for the same
        titanium pool -- with ~20-30 builders each dropping a trail of
        conveyors on their way to the enemy Core, cost-scale climbed fast
        enough that by the time an attacker was adjacent to the enemy Core,
        the team often couldn't afford a single Sentinel yet. Movement
        itself (this method's actual job) is otherwise unchanged from aug7.
        The "harvester" role uses _try_move_laying_conveyor instead, below
        -- there the trail IS the point (see TARGET_HARVESTERS).
        """
        if d == Direction.CENTRE:
            return False
        pos = ct.get_position()
        next_pos = pos.add(d)

        if not in_bounds(ct, next_pos):
            return False

        if ct.can_move(d):
            ct.move(d)
            return True
        return False

    def _try_move_laying_conveyor(self, ct: Controller, d: Direction) -> bool:
        """Like _try_move, but for a "harvester"-role builder walking a
        finished harvester's output back to the Core: lay a conveyor on the
        tile we're about to step onto, facing further toward the Core, so a
        full multi-tile chain accretes automatically as we walk it home.
        Each tile's facing is computed fresh from THAT tile toward the Core
        (cardinal_toward), so it's always correct regardless of how far
        there still is to go -- this is aug7's verified trail-laying
        pattern (see _try_move above for why attackers deliberately skip
        it); reused here because a real chain is exactly what's needed to
        get a harvester crediting anything (delivery-only, see
        _try_build_conveyor_toward_core).
        """
        if d == Direction.CENTRE:
            return False
        pos = ct.get_position()
        next_pos = pos.add(d)

        if not in_bounds(ct, next_pos):
            return False

        if self.core_pos is not None and ct.is_tile_empty(next_pos):
            cardinal = cardinal_toward(next_pos, self.core_pos)
            if cardinal is not None and ct.can_build_conveyor(next_pos, cardinal):
                ct.build_conveyor(next_pos, cardinal)
                _dbg(
                    f"r={ct.get_current_round()} event=chain_link pos={next_pos} facing={cardinal.name} "
                    f"unit={ct.get_id()} dist_sq_home={next_pos.distance_squared(self.core_pos)}"
                )

        if ct.can_move(d):
            ct.move(d)
            return True
        return False

    def _pick_target(self, ct: Controller) -> Position | None:
        """Attackers beeline for the enemy Core -- no economy detours, no
        ore-seeking. The blocker cycles between enemy spawn-ring tiles. The
        launcher-builder and harvester roles head home instead (see below).
        Reaching an (impassable) Core position just means the unit parks
        adjacent to it, which is exactly where we want it for
        sentinel/launcher-building.
        """
        if self.role == "blocker":
            return self._pick_ring_target(ct)
        if self.role == "launcher_builder":
            return self.core_pos if self.core_pos is not None else self._random_target(ct)
        if self.role == "harvester":
            return self._pick_econ_target(ct)
        if self.enemy_pos is not None:
            return self.enemy_pos
        return self._random_target(ct)

    def _pick_econ_target(self, ct: Controller) -> Position:
        """Economy builder, before building: seek the nearest visible
        unclaimed ore tile (aug7's proven pattern -- ct.get_nearby_tiles()
        is already vision-bounded, so no GameError guarding needed). Once
        built (self.harvester_done), head home instead; _move_toward_target
        switches to _try_move_laying_conveyor for that leg so the walk home
        also lays the delivery chain.

        No ore visible: wander, but bounded NEAR HOME (_random_target_near),
        not _random_target's whole-map roll. Measured 2026-08-06: on a small
        map (fjordgate, 10x10) a whole-map random target routinely lands
        near the enemy Core, so a dedicated economy builder with no local
        ore ends up walking straight into the enemy's defenses instead of
        continuing to look for ore close to home -- 3 of 3 "harvester" role
        builders did exactly this in one match and none ever built anything.

        Ore IS visible but on the enemy's side of the map: skip it too
        (_on_our_side) -- also measured, same match, same failure mode: an
        econ builder that wandered near the midpoint spotted enemy-side ore
        and beelined for it (ending up dist_sq=1 from the enemy Core), which
        is exactly the kind of long, hostile, low-value chain this role
        should never attempt when it's dedicated home economy, not a scout.
        """
        if self.harvester_done:
            return self.core_pos if self.core_pos is not None else self._random_target(ct)

        pos = ct.get_position()
        best: list[Position] = []
        best_dist = None
        for tile in ct.get_nearby_tiles():
            if ct.get_tile_env(tile) != Environment.ORE_TITANIUM:
                continue
            if ct.get_tile_building_id(tile) is not None:
                continue
            if not self._on_our_side(tile):
                continue
            d = pos.distance_squared(tile)
            if best_dist is None or d < best_dist:
                best_dist = d
                best = [tile]
            elif d == best_dist:
                best.append(tile)
        if best:
            return random.choice(best)
        if self.core_pos is not None:
            return self._random_target_near(ct, self.core_pos, ECON_WANDER_RADIUS)
        return self._random_target(ct)

    def _on_our_side(self, pos: Position) -> bool:
        """True if pos is at least as close to our own Core as to the
        enemy's -- the midpoint test shared by _pick_econ_target's ore scan
        and _random_target_near's wander, so economy builders never chase
        ore or drift into the enemy's half looking for something to do.
        """
        if self.core_pos is None or self.enemy_pos is None:
            return True
        return pos.distance_squared(self.core_pos) <= pos.distance_squared(self.enemy_pos)

    def _random_target_near(self, ct: Controller, origin: Position, radius: int) -> Position:
        """A random in-bounds tile within +/-radius of origin (Chebyshev,
        not a true disc -- cheap, and precision doesn't matter for a wander
        target), rejecting candidates closer to the enemy Core than to
        origin. Anchored on origin (not the caller's current position) so
        repeated calls keep exploring the SAME bounded region rather than
        drifting further every time the unit is stuck or arrives.

        The rejection step matters more than the radius: on a small map
        (fjordgate, 10x10, cores ~4 tiles apart) a fixed radius=7 still
        covers nearly the whole board, so a plain box sample kept landing
        past the midpoint -- measured 2026-08-06, 3 of 3 economy builders
        drifted into "contact" range of the enemy Core and never built
        anything. Constraining to "our half" (relative to self.enemy_pos)
        scales correctly with map size instead of needing a tuned radius.
        """
        w, h = ct.get_map_width(), ct.get_map_height()
        for _ in range(6):
            x = max(0, min(w - 1, origin.x + random.randint(-radius, radius)))
            y = max(0, min(h - 1, origin.y + random.randint(-radius, radius)))
            candidate = Position(x, y)
            if self._on_our_side(candidate):
                return candidate
        return origin

    def _pick_ring_target(self, ct: Controller) -> Position:
        """Choose the next enemy spawn-ring tile to occupy: prefer a tile we
        know (from current vision) is passable and not already held by
        someone else; fall back to a tile we can't yet verify (still worth
        walking toward -- can_move() will re-check when we get there); if
        every ring tile is somehow known-bad, just aim at the closest one
        so we keep pressing on the ring instead of giving up.
        """
        if self.enemy_pos is None:
            return self._random_target(ct)

        pos = ct.get_position()
        ring = spawn_ring(self.enemy_pos)

        verified_good = []
        unverified = []
        for t in ring:
            if t == pos or not in_bounds(ct, t):
                continue
            try:
                if not ct.is_tile_passable(t):
                    continue
                occupant = ct.get_tile_builder_bot_id(t)
            except GameError:
                unverified.append(t)
                continue
            if occupant is not None and occupant != ct.get_id():
                continue
            verified_good.append(t)

        pool = verified_good or unverified
        if pool:
            return random.choice(pool)
        # Every ring tile looks bad from here. Aim at one of the closest
        # few, not deterministically THE closest -- if what's blocking us
        # is another builder contesting the same tile (ours or theirs),
        # always picking the single nearest tile means always picking the
        # same tile, i.e. retrying the exact collision every time we get
        # stuck. A little randomness among the near options breaks that.
        by_dist = sorted(ring, key=lambda t: pos.distance_squared(t))
        return random.choice(by_dist[:3])

    def _random_target(self, ct: Controller) -> Position:
        w, h = ct.get_map_width(), ct.get_map_height()
        return Position(random.randrange(w), random.randrange(h))

    # ------------------------------------------------------------------
    # Sentinel
    # ------------------------------------------------------------------

    def _run_sentinel(self, ct: Controller) -> None:
        """Fire at the NEAREST enemy on our attack line -- not the first tile
        enumeration happens to visit.

        get_attackable_tiles() and get_nearby_tiles() both enumerate in
        absolute row-major map order regardless of facing [docs/game-model.md,
        measured 2026-08-08]. A "first hit wins" scan over that order is
        therefore absolutely oriented: N/NE/NW/W-facing turrets would engage
        the FARTHEST enemy on the line and E/SE/S/SW turrets the nearest --
        aug7 has exactly this bug. Since our Sentinels are built facing
        whichever direction points at the enemy Core (all 8 are possible),
        half of them would inherit it. Fixed here with an explicit geometric
        criterion: nearest by distance_squared.
        """
        my_team = ct.get_team()
        best_tile = None
        best_target_id = None
        best_dist = None
        pos = ct.get_position()
        for tile in ct.get_attackable_tiles():
            target_id = ct.get_tile_builder_bot_id(tile)
            if target_id is None:
                target_id = ct.get_tile_building_id(tile)
            if target_id is None:
                continue
            if ct.get_team(target_id) == my_team:
                continue
            d = pos.distance_squared(tile)
            if best_dist is None or d < best_dist:
                best_dist = d
                best_tile = tile
                best_target_id = target_id

        if best_tile is None:
            return
        if ct.can_fire(best_tile):
            ct.fire(best_tile)
            if not self.dbg_fired:
                self.dbg_fired = True
                _dbg(
                    f"r={ct.get_current_round()} event=first_shot sentinel unit={ct.get_id()} "
                    f"fired at {best_tile} target_id={best_target_id}"
                )

    # ------------------------------------------------------------------
    # Launcher (the opener's throwing arm)
    # ------------------------------------------------------------------

    def _run_launcher(self, ct: Controller) -> None:
        """Every round, if we know where the enemy Core is, grab any
        adjacent friendly Builder Bot (pickup r²=2, incl. diagonal) --
        EXCEPT a "harvester"-role economy builder (see SLOT_HARVESTER_IDS)
        -- and throw it as far toward the enemy Core as throw range (r²=26,
        measured from US, not the bot) allows. can_launch()/launch() take
        (bot_pos, target) -- there's no "self" bot to throw, so we scan
        get_nearby_units() for one. The thrown builder walks the rest: one
        throw covers up to ~5 tiles instantly, ordinary cardinal movement
        (unchanged, role stays "attacker") covers the remainder -- see
        docs/opponents.md, Albert And Einstein signature behaviour.

        The harvester exclusion is load-bearing, not defensive coding:
        measured 2026-08-06 (lighthouse) an economy builder mid-chain
        wandered adjacent to our own Launcher and got thrown clear across
        the map towards the enemy, abandoning a chain it had already laid
        20+ tiles of. The blocker and a just-finished launcher_builder (who
        becomes "attacker") are NOT excluded -- getting thrown only helps
        them reach their own targets faster.
        """
        if self.core_pos is None:
            self._read_core_pos(ct)
        if self.core_pos is not None:
            self._sync_enemy_core(ct)

        if self._cpu_exhausted(ct):
            return
        if self.enemy_pos is None:
            return

        pos = ct.get_position()
        my_team = ct.get_team()
        my_id = ct.get_id()
        target = self._throw_target(ct, pos)
        if target is None:
            return

        protected = {v for s in SLOT_HARVESTER_IDS if (v := ct.read_store(s)) != 0}

        for uid in ct.get_nearby_units(dist_sq=2):
            if uid == my_id or ct.get_team(uid) != my_team:
                continue
            if ct.get_entity_type(uid) != EntityType.BUILDER_BOT:
                continue
            if (uid + 1) in protected:
                continue
            bot_pos = ct.get_position(uid)
            if ct.can_launch(bot_pos, target):
                ct.launch(bot_pos, target)
                if not self.dbg_thrown:
                    self.dbg_thrown = True
                    _dbg(f"r={ct.get_current_round()} event=first_throw bot={uid} from={bot_pos} to={target}")
                return

    def _throw_target(self, ct: Controller, pos: Position) -> Position | None:
        """Pick a bot-passable tile within throw range (r²=26, measured
        from the Launcher's own position) that makes maximum progress
        toward the enemy Core. Backs off along the same line (5, 4, 3, 2
        tiles) if the ideal spot is a wall or otherwise illegal rather than
        giving up outright -- wall density runs up to 30.8% on some maps in
        the pool (docs/game-model.md).
        """
        dx = self.enemy_pos.x - pos.x
        dy = self.enemy_pos.y - pos.y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist < 1:
            return None
        for hop in (5.0, 4.0, 3.0, 2.0):
            scale = min(1.0, hop / dist)
            tx = pos.x + round(dx * scale)
            ty = pos.y + round(dy * scale)
            candidate = Position(
                max(0, min(ct.get_map_width() - 1, tx)),
                max(0, min(ct.get_map_height() - 1, ty)),
            )
            if candidate == pos:
                continue
            try:
                if ct.is_tile_passable(candidate):
                    return candidate
            except GameError:
                continue
        return None
