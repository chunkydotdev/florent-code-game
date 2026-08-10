# What this game is

Two teams each control a fleet of robots on a rectangular grid (8x8 to 30x30, symmetric by reflection or rotation). A competitor writes a single Python class:

class Player:
def run(self, ct: Controller) -> None:
...

`run()` is called once per round for every living unit on the team (the core and every builder bot, gunner, sentinel, launcher — turrets included). `ct` (a `Controller`) is unit-scoped: all of its methods act on or query relative to "this unit" unless an explicit entity `id` is passed. There is no shared game-object; all state is read through `Controller` getters.

Win condition: destroy the enemy core, or have the better tiebreakers after round 1000 (titanium **collected** → harvesters alive → titanium stored → coinflip). **"collected", not "delivered to core"** — the organisers' primary is internally inconsistent (it uses both phrasings) and the ENGINE settles it: the `cond` string it emits is literally `titanium_collected`. **And key 1 decides almost everything** — over our own 1,055 r1000 games: `titanium_collected` 993 (94.1%), `harvesters` 44 (4.2%), `titanium_stored` 18 (1.7%). **`titanium_collected` EXCLUDES passive income** (engine-probed: a bot that builds no harvester finishes 1000 rounds holding 2,892 Ti of accrued passive with `titanium_collected` = **0** — the same match then tied key 1 at 0-0, tied key 2 at 0-0, and was decided on `titanium_stored`, demonstrating the cascade). **And it counts DELIVERY TO THE CORE, not emission** (engine-probed: one harvester built at r2, alive all game, ~250 stacks' worth emitted over 998 rounds, NO conveyor ever built -> `titanium_collected` = **0**; that match tied key 1 at 0-0 and stopped at key 2, `win_condition: harvesters`). **So the deciding key is harvester throughput THAT REACHES THE CORE — a harvester with no route home is worth zero on it, forever, and any late bank-to-harvester conversion must buy the conveyor line too.** Read this the right way round: **harvesters matter MAXIMALLY, via key 1** — what is nearly worthless is keeping a harvester ALIVE as a countable unit at r1000 (key 2, 4.2%). Cumulative delivery is decisive; late preservation is not. Those are different planks and only the first is worth buying.

Bot file requirements: entry point must be main.py (at the zip root, or inside exactly one top-level directory) containing a top-level `class Player`. Bots are Python only. Auxiliary modules may be imported from other files in the same zip. Each unit gets 10ms CPU time per turn (with a small rolling 5% buffer) — if exceeded, that turn's run() is interrupted and does not resume next turn. This is different from an uncaught exception: if run() raises anything besides that timeout, the engine prints the traceback and permanently destroys that unit — it will never run again for the rest of the match.

# Core game rules

- Map tiles: Environment.EMPTY, Environment.WALL, Environment.ORE_TITANIUM. Walls block building. Harvesters can only be built on ore tiles.
- Resources: one resource type, ResourceType.TITANIUM. Each team starts with 500 global titanium, plus 10 passive titanium every 4 rounds. Titanium also moves physically through the map in stacks of 10 via conveyors/splitters/harvesters, separate from the global pool used to pay build costs.
- Ammunition: each team also has a global ammunition balance that turrets fire from. Teams start with 0 ammo and there is no passive ammo income — the only source is the core converting global titanium into ammunition 1:1 via convert_ammo(amount).
- Global communication store: 16 integer slots (read_store(index)/write_store(index, value), index 0-15), private per team, shared by all of a team's units. Writes are buffered — visible only from the next round, so every unit sees a consistent snapshot for the whole round.
- Units vs. buildings: units = core, builder bots, gunners, sentinels, launchers (all except builder bots are also buildings). Buildings = everything except builder bots; they're immovable. Each team may have at most 50 living units at once (GameConstants.MAX_TEAM_UNITS), including the core — check with get_unit_count().
- Cooldowns: every unit has an action cooldown and (builder bots only) a move cooldown, both nonnegative integers that decrease by 1 at end of round. Actions/movement require cooldown == 0, and acting or moving is mutually exclusive per round for builder bots — doing one blocks the other until next round.
- Cost scaling: every buildable entity's cost is floor(scale \* base*cost), where scale is **ONE GLOBAL ADDITIVE team factor** (NOT per-category — corrected s26 against the organisers' primary `docs/reference/official-docs.md:1353,1424` and replay-measured at 99.98% of 5,051 clean rounds, `docs/research/gunner-vs-sentinel-pricing-2026-08-09.md`). It starts at 1.0; EVERY build adds to the same factor (conveyor/splitter/barrier +1%, harvester +5%, launcher +10%, builder bot/gunner/sentinel +20%; destruction removes the contribution) and inflates ALL subsequent builds of every type. **CONFIRMED ON THE ENGINE, not only inferred** (`bots/_probe_scale`, s26): spawning ONLY builder bots drove scale 100→120→140→160→180→200% and raised conveyor 3→6, harvester 20→40, launcher 20→40 — categories that were never built — with observed == floor(scale × base) for all 8 entity types in every round. Per-category is dead; additive, not compounding. Consequences: the gunner:sentinel price ratio is pinned 2:3 at every scale; each live builder bot has already added +20% before any turret is bought. Use the get*<entity>\_cost() getters rather than hardcoding base costs, since actual cost depends on live scale.
- Vision vs. action vs. attack radius: vision = what a unit can sense; the core has an action radius of sqrt(8), used to determine where it may spawn builder bots — no other unit has a radius-based action range: all builder bot actions (build/attack/heal/destroy) require an orthogonally adjacent tile; turrets additionally have an attack range for firing, separate from vision.
- Resource distribution happens once at end of round, after all units have acted. Conveyors/splitters/harvesters form a purely economic pipeline into the core — turrets do not participate and never hold or accept resources (yours or the enemy's). Resources can still be pushed onto an opposing team's conveyor network or core.

## Entities

| Entity      | HP  | Base cost | Scale/build | Notes                                                                                                                                                    |
| ----------- | --- | --------- | ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Core        | 500 | —         | —           | 2x2 footprint; vision r²=36, action r²=8; spawns ≤1 builder bot/turn on an adjacent tile                                                                 |
| Builder bot | 40  | 30 Ti     | +20%        | Only mobile unit; vision r²=20; build/attack/heal/destroy all require an orthogonally adjacent tile                                                     |
| Conveyor    | 20  | 3 Ti      | +1%         | Faces a cardinal direction; accepts from 3 sides, outputs to the 4th                                                                                     |
| Splitter    | 20  | 6 Ti      | +1%         | Accepts only from the back; rotates output among 3 directions, least-recently-used first                                                                 |
| Harvester   | 30  | 20 Ti     | +5%         | Built on ore; outputs a stack every 4 rounds (first stack immediately on build)                                                                          |
| Barrier     | 30  | 3 Ti      | +1%         | Cheap HP wall, no other function                                                                                                                         |
| Gunner      | 25  | 20 Ti     | +20%        | Facing turret, vision/attack r²=13; straight-line shot, dmg 7, reload 1, costs 4 ammo/shot from the team global pool; rotate() costs 10 Ti + 1 cooldown |
| Sentinel    | 40  | 30 Ti     | +20%        | Facing turret, vision/attack r²=32; single-tile-wide line shot that ignores obstacles (unlike Gunner), dmg 18, reload 2, costs 10 ammo/shot from the team global pool             |
| Launcher    | 30  | 20 Ti     | +10%        | Facing-independent, vision/attack r²=26; picks up an adjacent builder bot from either team and throws it to a passable tile                              |

Builder bot actions per turn (cooldown-gated, one per turn): build (any building type on an orthogonally adjacent empty tile — not diagonal, not its own tile), attack (2 Ti → 2 dmg to the building on an orthogonally adjacent tile — not diagonal, not its own tile), heal (1 Ti → +4 HP to all friendly entities on an orthogonally adjacent tile — not diagonal, not its own tile), destroy (any allied building on an orthogonally adjacent tile — not diagonal, not its own tile — unlimited per turn, no cooldown), self-destruct (no damage dealt).

Turrets fire from the team's global ammunition balance (gunner 4/shot, sentinel 10/shot; launchers use no ammo) — there is no physical ammo, so turrets never need feeding. The core converts global titanium into ammunition 1:1 with convert_ammo(amount): at most once per team per turn, usable the same turn, and it does not use the core's action cooldown (converting never costs a spawn).

Entities and resource stacks both have unique integer IDs; entity properties are queried via getters like get_hp(id) rather than returned as objects (perf reasons — object construction is slow in the hot path).

# Controller API reference

Every bot interacts with the game exclusively through the Controller instance passed into run(). Methods that take an optional id: int | None default to the calling unit when omitted.

## Info / queries

| Method                                           | Description                                                                     |
| ------------------------------------------------ | ------------------------------------------------------------------------------- | ------------------------------------------------- |
| get_team(id=None) -> Team                        | Team of entity id (or self)                                                     |
| get_position(id=None) -> Position                | Position of entity id (or self)                                                 |
| get_id() -> int                                  | This unit's own entity id                                                       |
| get_action_cooldown() -> int                     | Current action cooldown (0 = can act)                                           |
| get_move_cooldown() -> int                       | Current move cooldown, builder bots only (0 = can move)                         |
| get_vision_radius_sq(id=None) -> int             | Vision radius² of id (or self)                                                  |
| get_hp(id=None) -> int                           | Current HP of id (or self)                                                      |
| get_max_hp(id=None) -> int                       | Max HP of id (or self)                                                          |
| get_entity_type(id=None) -> EntityType           | Type of id (or self)                                                            |
| get_direction(id=None) -> Direction              | Facing of a conveyor/splitter/turret (raises if entity has no direction)        |
| get_stored_resource(id=None) -> ResourceType     | None                                                                            | Resource held by a conveyor/splitter              |
| get_stored_resource_id(id=None) -> int           | None                                                                            | Resource stack id held (distinct from entity ids) |
| get_tile_env(pos) -> Environment                 | Tile terrain at pos                                                             |
| get_tile_building_id(pos) -> int                 | None                                                                            | Building id at pos, if any                        |
| get_tile_builder_bot_id(pos) -> int              | None                                                                            | Builder bot id at pos, if any                     |
| is_tile_empty(pos) -> bool                       | No building and not a wall                                                      |
| is_tile_passable(pos) -> bool                    | A friendly builder bot could stand there                                        |
| is_in_vision(pos) -> bool                        | pos within this unit's vision                                                   |
| get_nearby_tiles(dist_sq=None) -> list[Position] | In-bounds tiles within dist_sq (default: vision radius)                         |
| get_nearby_entities(dist_sq=None) -> list[int]   | Entity ids on tiles within dist_sq                                              |
| get_nearby_buildings(dist_sq=None) -> list[int]  | Building ids within dist_sq                                                     |
| get_nearby_units(dist_sq=None) -> list[int]      | Unit ids within dist_sq                                                         |
| get_map_width() -> int / get_map_height() -> int | Map dimensions                                                                  |
| get_current_round() -> int                       | Round number, 0-indexed (0 on the first round)                                  |
| get_global_resources() -> int                    | This team's titanium balance                                                    |
| get_global_ammo() -> int                         | This team's ammunition balance (starts at 0; no passive income)                 |
| get_scale_percent() -> float                     | Current cost-scale multiplier as a percentage                                   |
| get_cpu_time_elapsed() -> int                    | Microseconds of CPU used this turn so far                                       |
| get_unit_count() -> int                          | Living units on this team (incl. core); compare to GameConstants.MAX_TEAM_UNITS |

## Cost getters

get_conveyor_cost(), get_splitter_cost(), get_harvester_cost(), get_barrier_cost(), get_gunner_cost(), get_sentinel_cost(), get_launcher_cost(), get_builder_bot_cost() — all -> int, return the currently scaled cost. Always prefer these over hardcoded base costs.

## Movement (builder bots only)

| Method                      | Description                                    |
| --------------------------- | ---------------------------------------------- |
| can_move(direction) -> bool | Whether a move in direction is legal this turn |
| move(direction) -> None     | Move one step; raises GameError if illegal     |

## Building

| Method                                                                              | Description                                                                                                                                    |
| ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| can_build_conveyor/splitter/harvester/barrier/gunner/sentinel/launcher(...) -> bool | Legality check per entity type (conveyor/splitter/gunner/sentinel need (position, direction); harvester/barrier/launcher need only (position)); position must be an orthogonally adjacent tile, not diagonal, not this builder bot's own tile |
| build_conveyor/splitter/harvester/barrier/gunner/sentinel/launcher(...) -> int      | Build and return new entity id; raises GameError if illegal                                                                                    |
| can_build(entity_type, position, extra=None) -> bool                                | Generic form; extra is a Direction for conveyor/splitter/gunner/sentinel, unused otherwise; same orthogonal-adjacency restriction on position                                                     |
| build(entity_type, position, extra=None) -> int                                     | Generic form of the above                                                                                                                      |

## Healing / destruction (builder bots only)

| Method                                                            | Description                                                                                                        |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| can_heal(position) -> bool / heal(position) -> None               | Heal all friendly entities on position; builder bots may only target an orthogonally adjacent tile, +4 HP for 1 Ti |
| can_destroy(building_pos) -> bool / destroy(building_pos) -> None | Destroy an allied building on an orthogonally adjacent tile; free, no cooldown, unlimited per turn                 |
| self_destruct() -> None                                           | Destroy this unit; no explosion damage                                                                             |
| resign(message=None) -> None                                      | Forfeit immediately (destroys own core)                                                                            |

## Communication store

read_store(index) -> int / write_store(index, value) -> None — index in 0..GameConstants.STORE_SIZE (16). Writes are buffered until next round.

## Turrets (gunner / sentinel / launcher; builder bots share can_fire/fire for their orthogonally-adjacent-tile attack)

| Method                                                                        | Description                                                                                                                                             |
| ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| can_fire(target) -> bool / fire(target) -> None                               | Attack target; gunners/sentinels spend team global ammo (4/10 per shot), launchers use none; builder bots may only target an orthogonally adjacent tile |
| can_fire_from(position, direction, turret_type, target) -> bool               | Hypothetical-turret version, ignores ammo/cooldown                                                                                                      |
| can_rotate(direction) -> bool / rotate(direction) -> None                     | Gunner-only; 10 Ti, sets action cooldown to 1                                                                                                           |
| get_gunner_target() -> Position                                               | None                                                                                                                                                    | Nearest targetable tile in a gunner's facing line |
| get_attackable_tiles() -> list[Position]                                      | Raw attack pattern for this turret (ignores ammo/cooldown/occupancy)                                                                                    |
| get_attackable_tiles_from(position, direction, turret_type) -> list[Position] | Hypothetical-turret version                                                                                                                             |
| can_launch(bot_pos, target) -> bool / launch(bot_pos, target) -> None         | Launcher-only; pick up an adjacent builder bot from either team, throw to target                                                                        |

## Core

| Method                           | Description                                                                                                                                                      |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| can_spawn(position) -> bool      | Whether the core can spawn a builder bot at position (adjacent to footprint) this turn                                                                           |
| spawn_builder(position) -> int   | Spawn and return the new builder bot's id; costs one action cooldown                                                                                             |
| can_convert_ammo(amount) -> bool | Whether the core can convert amount titanium into ammunition this turn                                                                                           |
| convert_ammo(amount) -> None     | Convert amount global titanium into ammunition 1:1; at most once per team per turn, usable the same turn, does not use the action cooldown (never costs a spawn) |

## Debugging

draw_indicator_line(pos_a, pos_b, r, g, b) and draw_indicator_dot(pos, r, g, b) draw into the replay for visual debugging. print() output is captured to the replay; use stderr for console-only output.

# Key types and constants

- Direction: NORTH, NORTHEAST, EAST, SOUTHEAST, SOUTH, SOUTHWEST, WEST, NORTHWEST, CENTRE. Compass convention: (0, 0) is the map's northwest corner, x grows east and y grows south, so **NORTH is (0, −1)** (toward row 0); in the isometric viewer north renders up-right on screen — see the on-screen compass. Has .delta() -> (dx, dy), .rotate_left(), .rotate_right(), .opposite(), .is_cardinal() -> bool (True only for N/E/S/W). Builder bots may only **move** in the 4 cardinal directions — move(<diagonal>) raises GameError and can_move(<diagonal>) is False. All 8 directions remain valid for turret facing and building orientation.
- Position(x, y) (NamedTuple): .add(direction) -> Position, .distance_squared(other) -> int, .direction_to(other) -> Direction (nearest 45° compass direction — may be diagonal), .cardinal_direction_to(other) -> Direction (best legal cardinal step toward other, or CENTRE if already there; use this when picking a builder move).
- EntityType: BUILDER_BOT, CORE, GUNNER, SENTINEL, LAUNCHER, CONVEYOR, SPLITTER, HARVESTER, BARRIER.
- Environment: EMPTY, WALL, ORE_TITANIUM.
- Team: A, B. ResourceType: TITANIUM (only one, for now).
- GameConstants: MAX_TURNS=1000, STACK_SIZE=10, STARTING_TITANIUM=500, MAX_TEAM_UNITS=50, PASSIVE_TITANIUM_AMOUNT=10, PASSIVE_TITANIUM_INTERVAL=4, STORE_SIZE=16, plus per-entity \_BASE_COST, \_MAX_HP, and radius-squared constants matching the tables above. Prefer these over magic numbers.
- GameError: raised by any illegal action call (e.g. calling move() when unable). Always feasible to check first with the matching can\_\*() predicate. If GameError (or any other exception) escapes run() uncaught, the unit is permanently destroyed for the rest of the match — catch it if the unit should keep playing.

# Minimal idiomatic example

from fcode import Controller, Direction, EntityType, Environment, Position

class Player:
def run(self, ct: Controller) -> None:
kind = ct.get_entity_type()
if kind == EntityType.CORE:
self.\_core_turn(ct)
elif kind == EntityType.BUILDER_BOT:
self.\_builder_turn(ct)

    def _core_turn(self, ct: Controller) -> None:
        # Keep ammunition banked for turrets (does not use the action cooldown).
        if ct.get_global_ammo() < 20 and ct.can_convert_ammo(10):
            ct.convert_ammo(10)
        if ct.get_action_cooldown() != 0:
            return
        if ct.get_global_resources() < ct.get_builder_bot_cost():
            return
        for d in Direction:
            if d == Direction.CENTRE:
                continue
            target = ct.get_position().add(d)
            if ct.can_spawn(target):
                ct.spawn_builder(target)
                return

    def _builder_turn(self, ct: Controller) -> None:
        # Build a harvester on any adjacent ore tile.
        if ct.get_action_cooldown() == 0:
            for tile in ct.get_nearby_tiles(dist_sq=2):
                if ct.get_tile_env(tile) == Environment.ORE_TITANIUM and ct.can_build_harvester(tile):
                    ct.build_harvester(tile)
                    return
        # Otherwise, wander. Builder bots move only in cardinal directions.
        if ct.get_move_cooldown() == 0:
            for d in (Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST):
                if ct.can_move(d):
                    ct.move(d)
                    return

# Notes for the coding agent

- Bots are Python only; the entry point is always a top-level `class Player` with a `run(self, ct: Controller) -> None` method, in main.py.
- Always gate actions with the matching can\_\*() check before calling the mutating method — the engine raises GameError on illegal calls rather than silently no-opping.
- Prefer the get\_\*\_cost() getters and GameConstants over hardcoded numbers, since costs scale with what's already been built.
- run() executes per-unit, every round, for every living unit on the team — branch on ct.get_entity_type() at the top, as in the example above.
- Each unit gets its own 10ms turn budget; avoid unbounded loops or expensive recomputation over the whole map every round if it can be cached via the communication store or kept cheap.
- Stay consistent with the API and idioms above rather than inventing methods that don't exist in this reference.

# Team standing practices (Magnus, 2026-08-09 — applies to EVERY session in this repo, all lanes)

These override attention drift; the full lane protocol is your boot config
(`/builder`, `/research`, `/sidelane`) + `docs/two-session-protocol.md`.

- **Use subagents.** Standing permission, no per-session approval: delegate long
  builds, wide reads, and parallelisable work to keep your own context low.
  Model ALWAYS explicit on every Agent call — `opus` (judgment) or `sonnet`
  (mechanical with a validated method), never omitted. Announce in IN-FLIGHT
  before spawning; relay results before idling — they die with the session.
- **Push every commit immediately.** Commit-without-push has cost us a
  54-commit backlog once already.
- **Timestamps** come from `date` in the same shell call, or a cited git time.
  Never hand-written, never interpolated.
- **Instruments:** anything whose output gets published is an instrument —
  including one-liners and "quick checks". Before trusting one, run it
  against a case where it MUST come out the other way (corrupt the input,
  compute the complement-group control, mutation-test the fixture) — per
  guard, per branch. A check that has never produced the other verdict has
  not been seen to check; a constant column validates anything; alive in
  \`ps\` is not verified.
- **Numbers carry subjects.** Copy the denominator, the population, and the
  clock along with the number. Us-only samples must say so inline.
- **Submissions:** only via `tools/submit_clean.py`. A bare `fcode submit`
  ships docs to the platform and is a drift flag.
- **The iteration mill (Magnus, s25/s26 — the method behind the line's best
  progress):** iterate bot planks in SMALL steps and test each on UNRATED
  legs, many iterations per session. Per leg: a one-paragraph pre-registration
  (treatment bar + falsifier) COMMITTED before leg creation, then fire, then
  bank what measures and own nulls cheaply — a null is an iteration, not a
  failure. Analysis exists to feed this mill, not to replace it. Full ladder:
  `docs/builder-method.md` (S0–S8); prereg template: the obligations doc in
  `docs/research/`.

# WHAT LOKI IS (Magnus, 2026-08-10 — the definition of the active line)

Loaded in EVERY session because it changes what counts as a win. `PROGRAMME.md`
is the machine-readable authority and `tools/gate.py` enforces it; this block is
the directive verbatim so no lane can boot without it.

> *"Loki is the ultimate trickster, playing into other teams by using cheap
> tricks, manipulation, poisoning and every exploit we can find. Loki plays
> dirty and is the ultimate weapon at that. We want to destroy the enemy core,
> never play defence. A r1000 round is a defeat even if we by chance win it.
> You need to constantly figure out and test new tricks that we can use by
> building prototypes and putting them against live teams in unrated games —
> that beats our own calculations every time, and sometimes you find things
> that surprise you. Those are of fantastic importance for our growth."*

Four consequences, each of which closes a road that was open before it:

1. **A ROUND-1000 GAME IS A DEFEAT, INCLUDING WHEN WE WIN IT.** The tiebreak
   ladder (`titanium_collected` → harvesters → stored) decides ~94% of r1000
   games and is now OFF-CURRENCY. Everything above about harvester throughput
   remains factually true about the ENGINE and is no longer what we optimise.
   **Economy is instrumental: it buys the kill, it never scores.** Any plank
   whose only channel is `titanium_collected` is at best a correctness fix.
2. **NEVER PLAY DEFENCE.** Survival, screening, home turrets, heal-uptime — a
   plank whose mechanism is any of these is off-programme regardless of what it
   measures. Turrets are bought to open a lane to the enemy core, not to hold one.
3. **PROTOTYPES GO AT LIVE TEAMS, NOT AT OUR OWN PROBES.** `bots/*_probe` is a
   fixture WE authored and it lies in a known direction (five probes share a
   `best_core or best_any` short-circuit — zero of our forward turrets died in
   480 arena games against **46.9% on the ladder**). The instrument is
   **`fcode match unrated <team_id>`**: 5 games, a real team's real bot, no
   rating at stake. **Constraint, verified on the CLI:** it plays our **ACTIVE
   submission** — there is no flag for a local tree — so a prototype leg means
   activating the prototype and paying ~6 rated ladder matches per hour of
   window. Bounded, recoverable, and the price of the only honest fixture.
4. **A SURPRISE IS THE POINT, NOT AN ANOMALY.** An unpredicted result from a
   live-team leg outranks a predicted one from our own arena. Write it down
   before explaining it away.

**Never balance-changed by the organisers, therefore still open:** launcher
throw/kidnap (we may pick up an ENEMY builder and throw it anywhere passable,
for no ammo), spawn-tile denial, crash-induction. **Retired by this directive:**
tiebreak-turtle. **Already refuted, do not re-derive:** ore poisoning, partial
spawn starvation, siphon, barrier-form spawn lock, CPU denial, heal-idle staffing.
