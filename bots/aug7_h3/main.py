"""aug7_h3 — aug7 + demand-driven ammo conversion (strategy-notes.md /
strategy-log.md 2026-08-07: a flat standing ammo buffer parks titanium as
idle ammo through the long quiet phases instead of building economy, and
raising that flat buffer 20->50 already lost, 45.3% [39.3%, 51.4%]).
Instead of a constant, the core holds a small baseline (one sentinel shot)
once sentinels exist, and converts a burst only while a sentinel has
recently sighted an enemy -- see SLOT_THREAT_ROUND / AMMO_BASELINE /
AMMO_BURST / THREAT_DECAY_ROUNDS below.

aug7 — v4 + Sentinel-first defense (strategy-notes.md: sentinel beats
gunner on nearly every axis except entry cost and re-aim; static base
defense doesn't need either).

v4 — v2's CPU guard + every absolute-direction bias removed.

The seat experiments (docs/strategy-log.md, 2026-08-06) proved the seat-A
wipeouts on some maps were our own absolute orientation: the spawn scan
reaching only the N/W sides of the Core's ring accounted for most of it
(v3), and the movement/scan tie-breaks for the rest. This version carries
the full neutralisation set from probe_neutral — full-ring spawn, randomised
movement tie-break, randomised ore-scan tie-break, shuffled build/heal
scans — plus v2's CPU-budget guard. Direction choices are randomised only
where the old code broke ties by absolute direction; targets themselves are
unchanged.

Original starter-bot docstring follows.

Starter bot — economy-first strategy with light defense.

Each unit gets its own Player instance; the engine calls run() once per round.
Use ct.get_entity_type() to branch on what kind of unit you are.

Strategy:
  1. Core spawns builder bots, publishes its position via the store, and keeps
     a small global-ammo buffer topped up (turrets fire from that shared pool)
  2. Builder bots explore, build harvesters on ore, and lay conveyors toward
     the core so titanium flows back automatically
  3. Once the economy is running (3+ harvesters), builder bots place sentinels
     near the core for defense
  4. Sentinels auto-fire at the closest visible enemy on their attack line

Entity types used:  Core, Builder Bot, Harvester, Conveyor, Sentinel

Communication store slots:
  0  SLOT_CORE_X          Core X position (written by core on round 1)
  1  SLOT_CORE_Y          Core Y position
  2  SLOT_HARVESTER_COUNT Total harvesters built by the team
  3  SLOT_ORE_LOCATION    Packed (x, y) of an uncovered ore tile
  Slots 4-15 are free — use them for your own coordination logic.

Ideas for improvement:
  - Build full conveyor chains from distant harvesters back to the core
  - Tune the ammo buffer: convert more titanium when enemies are near, less
    when you'd rather grow the economy
  - Add sentinels or launchers for stronger defense
  - Explore the map systematically instead of picking random targets
  - Use more store slots to coordinate roles between builder bots
"""

import random

from fcode import Controller, Direction, EntityType, Environment, GameConstants, Position

# All directions except CENTRE — useful for spawning and turret facing (both
# allow diagonals). Builder movement is cardinal-only, so use CARDINALS to move.
DIRECTIONS = [d for d in Direction if d != Direction.CENTRE]

# Cardinal directions only — conveyors and splitters can only face these
# Compass: (0, 0) is the map's NORTHWEST corner, so NORTH = (0, -1) (toward
# row 0) and EAST = (1, 0). In the visualiser's iso view north points up-right
# on screen -- see its corner compass.
CARDINALS = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]

# --- Communication store slot assignments ---
# The store has 16 slots (indices 0-15), each holding a u32 value.
# Writes are buffered: a write_store() call becomes visible to all units
# at the start of the *next* round.
SLOT_CORE_X = 0
SLOT_CORE_Y = 1
SLOT_HARVESTER_COUNT = 2
SLOT_ORE_LOCATION = 3
# Round a sentinel last sighted an enemy in its vision, +1 so 0 still means
# "no signal yet" (see pack_pos's same +1 trick above). Written by sentinels
# in _run_sentinel, read by the core in _run_core. Store writes are buffered
# a round, so a sighting on round N is only visible to the core on N+1.
SLOT_THREAT_ROUND = 4

# How many builder bots the core will spawn over the course of the game
MAX_BUILDERS = 5

# How many harvesters we want before switching builder bots to defense duty
TARGET_HARVESTERS = 3

# Demand-driven ammo (replaces a flat AMMO_BUFFER): the core holds only
# AMMO_BASELINE (one sentinel shot) once we have sentinels, and tops up to
# AMMO_BURST only while a sentinel has sighted an enemy within the last
# THREAT_DECAY_ROUNDS rounds. A prior experiment raising a *flat* buffer
# 20->50 lost (docs/strategy-log.md, 2026-08-07): a bigger constant just
# parks titanium as idle ammo through the long quiet phases. Making the
# target conditional on an actual sighting keeps the quiet-phase cost near
# the old floor while still affording a real burst once a fight is on.
AMMO_BASELINE = 10
AMMO_BURST = 40
THREAT_DECAY_ROUNDS = 5

# CPU budget bail-out threshold, in microseconds. The engine allows 10 ms of
# CPU per unit per round (plus a banked buffer of up to 5%); exceeding it
# interrupts run() mid-statement with no cleanup, which both wastes whatever
# the round would have done and can leave instance state half-updated (e.g.
# stuck-counter bumped but the move never issued). Bailing ourselves at 8 ms
# keeps the skip at a phase boundary, so we choose what gets dropped --
# always the lowest-priority phases -- instead of the engine choosing.
CPU_BUDGET_US = 8000


def pack_pos(pos: Position) -> int:
    """Encode a position into a single u32 for the communication store.

    We offset by +1 so that position (0, 0) doesn't encode as 0,
    which we reserve to mean "no data".
    """
    return ((pos.x + 1) << 16) | (pos.y + 1)


def unpack_pos(val: int) -> Position | None:
    """Decode a position from the communication store. Returns None if empty (0)."""
    if val == 0:
        return None
    return Position((val >> 16) - 1, (val & 0xFFFF) - 1)


def in_bounds(ct: Controller, pos: Position) -> bool:
    """True if pos is on the map.

    Needed because Controller tile queries raise GameError off-map rather than
    returning False, and an escaping exception permanently kills the unit.
    """
    return 0 <= pos.x < ct.get_map_width() and 0 <= pos.y < ct.get_map_height()


def nearest_cardinal(d: Direction) -> Direction:
    """Snap any direction to the nearest cardinal direction.

    Conveyors and splitters can only face cardinal directions (N/E/S/W),
    so we use this to convert an arbitrary direction into a valid facing.
    """
    return {
        Direction.NORTH: Direction.NORTH,
        Direction.NORTHEAST: Direction.NORTH,
        Direction.EAST: Direction.EAST,
        Direction.SOUTHEAST: Direction.EAST,
        Direction.SOUTH: Direction.SOUTH,
        Direction.SOUTHWEST: Direction.SOUTH,
        Direction.WEST: Direction.WEST,
        Direction.NORTHWEST: Direction.WEST,
        Direction.CENTRE: Direction.NORTH,
    }[d]


class Player:
    def __init__(self):
        # Core tracks how many builder bots it has spawned
        self.num_spawned = 0

        # Builder bot navigation state
        self.target: Position | None = None   # where we're trying to walk to
        self.last_pos: Position | None = None  # position last round (for stuck detection)
        self.stuck = 0                         # consecutive rounds without moving

        # Cached core position (read from the store once, then reused)
        self.core_pos: Position | None = None

        # Whether we've already dumped a traceback for this unit (see run()).
        self.reported_error = False

        # Whether we've already reported a CPU-guard trip for this unit
        # (one line per unit lifetime, same rationale as reported_error).
        self.reported_cpu = False

    def run(self, ct: Controller) -> None:
        """Entry point called by the engine every round for each unit.

        Everything is wrapped: an exception that escapes run() makes the engine
        PERMANENTLY delete this unit for the rest of the match. Catching it costs
        us this one round's action instead. There is no situation where letting
        it propagate is better, so this guard is unconditional.

        We report the first traceback per unit to stderr and stay quiet after
        that, so a bug that fires every round can't flood the log (or burn our
        10ms CPU budget on formatting tracebacks).
        """
        try:
            self._dispatch(ct)
        except Exception:
            if not self.reported_error:
                self.reported_error = True
                import sys
                import traceback
                traceback.print_exc(file=sys.stderr)

    def _dispatch(self, ct: Controller) -> None:
        """Route to the right handler for whichever unit type we are."""
        etype = ct.get_entity_type()
        if etype == EntityType.CORE:
            self._run_core(ct)
        elif etype == EntityType.BUILDER_BOT:
            self._run_builder(ct)
        elif etype == EntityType.SENTINEL:
            self._run_sentinel(ct)

    def _cpu_exhausted(self, ct: Controller) -> bool:
        """True once this unit's round has used CPU_BUDGET_US of its 10 ms.

        Callers bail out of the remaining (lower-priority) phases when this
        trips, so the round degrades gracefully instead of being truncated
        mid-statement by the engine. Reported once per unit so a chronically
        slow unit is visible on stderr without flooding the log.
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

    # ------------------------------------------------------------------
    # Core
    # ------------------------------------------------------------------

    def _run_core(self, ct: Controller) -> None:
        """Core logic: publish our position so builder bots can orient toward us,
        then try to spawn a builder bot each round until we hit the cap.
        """
        # Write our position into the store every round so newly spawned bots
        # can read it. Store writes are buffered — they become visible next round.
        pos = ct.get_position()
        ct.write_store(SLOT_CORE_X, pos.x)
        ct.write_store(SLOT_CORE_Y, pos.y)

        # Demand-driven ammo: don't buy ammo before we have a sentinel to
        # spend it (same TARGET_HARVESTERS trigger _run_builder already uses
        # to start building sentinels). Once sentinels exist, hold a small
        # baseline (covers the opening shot even before a threat signal has
        # had a round to propagate) and only burst up to AMMO_BURST while a
        # sentinel has sighted an enemy recently. We still reserve enough for
        # a builder bot so conversion never blocks spawning -- the failure
        # mode the AMMO_BUFFER=50 discard already demonstrated is trading
        # economy for idle ammo, and this guard is what prevents that here.
        harvester_count = ct.read_store(SLOT_HARVESTER_COUNT)
        if harvester_count >= TARGET_HARVESTERS:
            raw_threat = ct.read_store(SLOT_THREAT_ROUND)
            threat_round = raw_threat - 1 if raw_threat > 0 else None
            current_round = ct.get_current_round()
            if threat_round is not None and current_round - threat_round <= THREAT_DECAY_ROUNDS:
                ammo_target = AMMO_BURST
            else:
                ammo_target = AMMO_BASELINE

            ammo = ct.get_global_ammo()
            if ammo < ammo_target:
                spare = ct.get_global_resources() - ct.get_builder_bot_cost()
                amount = min(ammo_target - ammo, spare)
                if amount > 0 and ct.can_convert_ammo(amount):
                    ct.convert_ammo(amount)

        # Don't spawn more than MAX_BUILDERS total
        if self.num_spawned >= MAX_BUILDERS:
            return

        # Check we can afford a builder bot before trying
        ti = ct.get_global_resources()
        cost = ct.get_builder_bot_cost()
        if ti < cost:
            return

        # Spawn on a random legal tile from the WHOLE ring around the 2x2
        # footprint. pos.add(d) reaches only the N/W sides of that ring,
        # because get_position() is the footprint's NW corner — an absolutely
        # oriented candidate set, and the prime suspect for the seat effect:
        # one seat spawns toward the map corner, the other toward the centre.
        candidates = [t for t in ct.get_nearby_tiles(dist_sq=8) if ct.can_spawn(t)]
        if candidates:
            ct.spawn_builder(random.choice(candidates))
            self.num_spawned += 1

    # ------------------------------------------------------------------
    # Builder bot
    # ------------------------------------------------------------------

    def _run_builder(self, ct: Controller) -> None:
        """Builder bot logic, executed each round. Priority order:
        1. Build a harvester if adjacent to uncovered ore
        2. Build a sentinel if we already have enough harvesters
        3. Heal any damaged friendly buildings nearby
        4. Move toward the next target (ore or exploration)
        5. Broadcast any visible ore to teammates via the store
        """
        pos = ct.get_position()

        # On our first turn, read the core's position from the store.
        # We cache it so we don't have to read every round.
        if self.core_pos is None:
            self._read_core_pos(ct)

        # Stuck detection: if we haven't moved in 3 rounds, we'll pick a new
        # target in _move_toward_target to avoid getting permanently stuck.
        if self.last_pos == pos:
            self.stuck += 1
        else:
            self.stuck = 0
        self.last_pos = pos

        # --- Build phase (requires action cooldown == 0) ---
        # Try to build a harvester first; if none available, consider a sentinel
        if ct.get_action_cooldown() == 0:
            if not self._try_build_harvester(ct):
                # Only build sentinels once our economy is up (enough harvesters)
                harvester_count = ct.read_store(SLOT_HARVESTER_COUNT)
                if harvester_count >= TARGET_HARVESTERS:
                    self._try_build_sentinel(ct)

        # Phase priority under CPU pressure: build > heal > move > share.
        # Each check lets us finish the round at a clean boundary.
        if self._cpu_exhausted(ct):
            return

        # If we still have an action left (didn't build anything), heal nearby
        if ct.get_action_cooldown() == 0:
            self._try_heal(ct)

        if self._cpu_exhausted(ct):
            return

        # --- Move phase (requires move cooldown == 0) ---
        self._move_toward_target(ct)

        if self._cpu_exhausted(ct):
            return

        # --- Communication phase (no cooldown needed) ---
        # Share any visible ore location with teammates
        self._share_ore(ct)

    def _read_core_pos(self, ct: Controller) -> None:
        """Read the core's position from the communication store.

        The core writes its position on round 1, so on round 1 these will
        still be 0. We skip storing (0, 0) unless the core really is there.
        """
        x = ct.read_store(SLOT_CORE_X)
        y = ct.read_store(SLOT_CORE_Y)
        if x > 0 or y > 0:
            self.core_pos = Position(x, y)

    def _try_build_harvester(self, ct: Controller) -> bool:
        """Try to build a harvester on an adjacent ore tile.

        Harvesters can only be placed on ore tiles (Environment.ORE_TITANIUM).
        can_build_harvester() checks for ore, empty tile, and sufficient resources.
        After building, we also try to place a conveyor next to it to start
        routing the titanium back toward the core.
        """
        ti = ct.get_global_resources()
        cost = ct.get_harvester_cost()
        if ti < cost:
            return False

        pos = ct.get_position()
        dirs = list(Direction)
        random.shuffle(dirs)
        for d in dirs:
            build_pos = pos.add(d)
            if ct.can_build_harvester(build_pos):
                ct.build_harvester(build_pos)
                # Update the shared harvester counter so other bots know
                count = ct.read_store(SLOT_HARVESTER_COUNT)
                ct.write_store(SLOT_HARVESTER_COUNT, count + 1)
                # Try to add a conveyor next to the harvester to route resources
                self._try_build_conveyor_toward_core(ct, build_pos)
                # Clear our target so we move on instead of lingering near this
                # harvester.  Without this the bot would try to walk onto the
                # (non-passable) harvester tile for 3 rounds before stuck
                # detection finally kicks in.
                self.target = None
                return True
        return False

    def _try_build_conveyor_toward_core(self, ct: Controller, harvester_pos: Position) -> None:
        """Place a conveyor adjacent to a harvester, facing toward the core.

        Harvesters output titanium stacks to adjacent buildings. By placing a
        conveyor on the core-facing side, resources will start flowing in the
        right direction. For a complete supply chain you'd need more conveyors
        linking all the way back to the core.
        """
        if self.core_pos is None:
            return
        ti = ct.get_global_resources()
        cost = ct.get_conveyor_cost()
        if ti < cost:
            return

        # Figure out which cardinal direction points from the harvester toward the core
        toward_core = harvester_pos.direction_to(self.core_pos)
        if toward_core == Direction.CENTRE:
            return  # harvester is right on top of the core (unlikely)
        facing = nearest_cardinal(toward_core)

        # Place the conveyor one step toward the core from the harvester
        conv_pos = harvester_pos.add(facing)
        if ct.can_build_conveyor(conv_pos, facing):
            ct.build_conveyor(conv_pos, facing)

    def _try_build_sentinel(self, ct: Controller) -> bool:
        """Build a sentinel turret on an adjacent tile, facing away from the core.

        Sentinels beat gunners on nearly every axis (strategy-notes.md): more
        damage/round, better Ti-per-damage, more HP, far larger attack radius,
        and an unblockable line shot that ignores obstacles/units. The only
        gunner advantages -- 10 Ti cheaper and re-aimable via rotate() -- don't
        apply to a static base defender, so sentinel-first should out-defend
        gunner-first at the same economy trigger point.

        Note: sentinels fire from the team's global ammo pool (10/shot), which
        the core fills by converting titanium (see AMMO_BASELINE/AMMO_BURST in
        _run_core) -- no physical ammo delivery is needed.
        """
        ti = ct.get_global_resources()
        cost = ct.get_sentinel_cost()
        if ti < cost:
            return False

        pos = ct.get_position()
        # Only build sentinels when we're reasonably close to the core
        if self.core_pos is None or pos.distance_squared(self.core_pos) > 18:
            return False

        # Face the sentinel away from the core (toward incoming enemies)
        facing = pos.direction_to(self.core_pos).opposite()
        if facing == Direction.CENTRE:
            facing = random.choice(DIRECTIONS)

        # Try each adjacent tile for a valid sentinel placement, in random order
        dirs = list(Direction)
        random.shuffle(dirs)
        for d in dirs:
            build_pos = pos.add(d)
            if ct.can_build_sentinel(build_pos, facing):
                ct.build_sentinel(build_pos, facing)
                return True
        return False

    def _try_heal(self, ct: Controller) -> None:
        """Heal a damaged friendly building or bot on an adjacent tile.

        Healing costs 1 titanium and restores 4 HP. can_heal() checks that
        there's actually a damaged friendly entity on the tile.
        """
        pos = ct.get_position()
        dirs = list(Direction)
        random.shuffle(dirs)
        for d in dirs:
            check = pos.add(d)
            if ct.can_heal(check):
                ct.heal(check)
                return

    # ------------------------------------------------------------------
    # Builder bot — movement
    # ------------------------------------------------------------------

    def _move_toward_target(self, ct: Controller) -> None:
        """Navigate toward our current target, picking a new one if needed.

        Target priority: visible ore > ore shared via store > random position.
        If we've been stuck for 3+ rounds, we give up on the current target
        and pick a fresh one.
        """
        if ct.get_move_cooldown() != 0:
            return

        pos = ct.get_position()

        # Pick a new target if we don't have one, reached it, or are stuck
        if self.target is None or pos == self.target or self.stuck >= 3:
            self.target = self._pick_target(ct)
            self.stuck = 0
        if self.target is None:
            return

        # Builder bots move only in cardinal directions. Compute the
        # productive cardinals ourselves and choose between them at random —
        # cardinal_direction_to has a fixed tie-break, i.e. exactly the kind
        # of absolute-direction bias this probe exists to remove.
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

        # Try the ideal cardinal first, then the two perpendicular cardinals,
        # then the reverse -- so if we're boxed in (e.g. by harvesters) we can
        # still route around obstacles instead of sitting stuck. Never diagonal.
        perpendicular = [d for d in CARDINALS if d not in (desired, desired.opposite())]
        random.shuffle(perpendicular)
        alternatives = [desired, *perpendicular, desired.opposite()]
        for d in alternatives:
            if self._try_move(ct, d):
                return

    def _try_move(self, ct: Controller, d: Direction) -> bool:
        """Try to move one step in direction d, laying conveyor infra along the way.

        Builder bots can walk on any tile that isn't a wall or occupied by another
        builder bot. If the destination is empty and we know where our core is, we
        lay a conveyor pointing toward it so it doubles as part of the resource
        network -- this is optional now, not required for movement.
        """
        if d == Direction.CENTRE:
            return False
        pos = ct.get_position()
        next_pos = pos.add(d)

        # Bail before touching the engine if the step leaves the map. Tile
        # queries like is_tile_empty() RAISE on an out-of-bounds position --
        # they don't return False -- and _move_toward_target tries up to four
        # directions, so any bot standing on an edge tile will hit this.
        if not in_bounds(ct, next_pos):
            return False

        if ct.is_tile_empty(next_pos) and self.core_pos is not None:
            toward_core = next_pos.direction_to(self.core_pos)
            cardinal = nearest_cardinal(toward_core)
            if ct.can_build_conveyor(next_pos, cardinal):
                ct.build_conveyor(next_pos, cardinal)

        # A build/attack/heal and a move can never happen in the same round --
        # if we just laid a conveyor above, can_move() below will correctly
        # say False until next round, when the conveyor already exists (so
        # the build attempt becomes a no-op) and the move goes through
        # instead.
        if ct.can_move(d):
            ct.move(d)
            return True
        return False

    def _pick_target(self, ct: Controller) -> Position:
        """Choose the next position to navigate toward.

        Priority:
        1. Closest visible ore tile without a harvester on it — go build one
        2. If economy is established (enough harvesters), head back toward
           the core so we can build sentinels for defense
        3. Ore location shared by a teammate via the store — head that way
        4. Random map position — pure exploration
        """
        pos = ct.get_position()

        # 1. Scan visible tiles for the nearest uncovered ore
        # Nearest uncovered ore, with DISTANCE TIES BROKEN AT RANDOM — the
        # strict < with the engine's fixed tile order always favoured the
        # first-enumerated tile, another absolute-direction bias.
        best_ore: list[Position] = []
        best_dist = float("inf")
        for tile in ct.get_nearby_tiles():
            if ct.get_tile_env(tile) != Environment.ORE_TITANIUM:
                continue
            # Skip ore that already has a building (harvester or otherwise) on it
            if ct.get_tile_building_id(tile) is not None:
                continue
            d = pos.distance_squared(tile)
            if d < best_dist:
                best_dist = d
                best_ore = [tile]
            elif d == best_dist:
                best_ore.append(tile)
        if best_ore:
            return random.choice(best_ore)

        # 2. Once we have enough harvesters, head back to the core so we can
        #    build sentinels nearby.  _try_build_sentinel requires being within
        #    distance² 18 of the core, so we navigate there.
        harvester_count = ct.read_store(SLOT_HARVESTER_COUNT)
        if harvester_count >= TARGET_HARVESTERS and self.core_pos is not None:
            if pos.distance_squared(self.core_pos) > 8:
                return self.core_pos

        # 3. Check the store for an ore location shared by a teammate
        shared = unpack_pos(ct.read_store(SLOT_ORE_LOCATION))
        if shared is not None and pos.distance_squared(shared) > 4:
            return shared

        # 4. No known ore — pick a random position to explore
        w, h = ct.get_map_width(), ct.get_map_height()
        return Position(random.randrange(w), random.randrange(h))

    def _share_ore(self, ct: Controller) -> None:
        """Broadcast a visible uncovered ore tile to teammates via the store.

        Any builder bot that sees ore without a building on it writes the
        location to SLOT_ORE_LOCATION. Other bots can read this to navigate
        toward ore they haven't seen yet.
        """
        tiles = ct.get_nearby_tiles()
        random.shuffle(tiles)
        for tile in tiles:
            if ct.get_tile_env(tile) == Environment.ORE_TITANIUM:
                if ct.get_tile_building_id(tile) is None:
                    ct.write_store(SLOT_ORE_LOCATION, pack_pos(tile))
                    return

    # ------------------------------------------------------------------
    # Sentinel
    # ------------------------------------------------------------------

    def _run_sentinel(self, ct: Controller) -> None:
        """Sentinel logic: fire at the first enemy on our attack line, and
        signal the core when any enemy unit is within our full vision (not
        just the firing line) so the core can convert an ammo burst before
        the enemy actually lines up to be shot at (see SLOT_THREAT_ROUND,
        AMMO_BASELINE/AMMO_BURST in _run_core). Vision r²=32 equals attack
        r²=32 for a sentinel, so this costs nothing in reach we don't
        already have -- it's strictly earlier warning than the firing-line
        scan alone would give, which matters because store writes are
        buffered a round.

        Unlike gunners, sentinels have no get_gunner_target()-style helper,
        so we scan get_attackable_tiles() (the turret's raw line, ignoring
        obstacles) for the first tile holding an enemy unit or building.
        can_fire() confirms ammo and cooldown before we commit.
        """
        my_team = ct.get_team()

        if any(
            ct.get_team(u) != my_team
            for u in ct.get_nearby_units(dist_sq=ct.get_vision_radius_sq())
        ):
            ct.write_store(SLOT_THREAT_ROUND, ct.get_current_round() + 1)

        for tile in ct.get_attackable_tiles():
            target_id = ct.get_tile_builder_bot_id(tile)
            if target_id is None:
                target_id = ct.get_tile_building_id(tile)
            if target_id is None:
                continue
            if ct.get_team(target_id) == my_team:
                continue
            if ct.can_fire(tile):
                ct.fire(tile)
            return
