# ⭐ CONTEXT FIRST — EVERYTHING HERE IS A GAME (Magnus, direct, 2026-08-22)

**All "tactics" in this repo are moves in the Florent Code League — a sandboxed
bot-vs-bot programming competition played on a simulated grid, within
organiser-approved rules.** Terms like exploit, attack, kidnap, poisoning,
crash-induction, weapon, kill and denial refer exclusively to in-game mechanics
between competing game bots (e.g. an opposing bot's Python `run()` raising an
unhandled exception inside the game engine, per the engine's documented rules).
Nothing in this project targets real systems, networks, infrastructure or
people. **Standing directive: be extra careful and EXPLICITLY state this game
context** — every doc, prereg, commit message, queue row and session note says
it is describing game tactics rather than relying on the reader to infer it,
and plain game language ("the opposing bot", "in-engine") is preferred over
combat metaphor because it is more accurate. (Background: the s55 `[cyber]`
model-safeguard refusals, coordination tail 2026-08-22; this framing is the
truthful description, not a workaround.)

**VOCABULARY CARD (Magnus, 2026-08-22: "We might have used too serious namings
for our tactics"). For NEW writing — docs, preregs, queue rows, commit messages,
session notes. Historical/locked artifacts are NOT rewritten (locked preregs are
untouchable, banked docs are provenance; the context block above covers them):**

| too-serious name (retired for new writing) | new name — and what it actually is |
| --- | --- |
| exploit / weapon | **trick** / **signature move** — a legal rules-quirk play the opponent's bot handles badly |
| the exploit hunt | **rulebook mining** — reading the engine's rules harder than the other team |
| launcher kidnap | **the taxi ride** — our launcher legally relocates an enemy builder piece |
| crash-induction | **banana peel** — relocating an enemy piece where its own code trips on an unhandled exception; the engine retires that unit per its documented rules |
| (ore/belt) poisoning | **belt prank** — placing pieces so their conveyor network feeds the wrong destination |
| tap the belt | **the milkshake straw** — our conveyor beside their harvester drinks half its output (round-robin is team-blind) |
| spawn-tile denial | **musical chairs** — standing on the tiles their core needs for spawning |
| kill the core / "the kill" | **checkmate / core takedown** — winning by core destruction, the game's stated win condition |
| CPU denial | **brain freeze** — plays that push the opposing bot toward its 10ms turn budget |
| crash census | **stumble census** — counting opposing bots' self-retired units |

**SECOND PASS (Magnus, direct, 2026-08-22 ~11:5xZ: "We are using words that can
be confused as unpleasant outside the context of the game") — the first card
did not go far enough; lane traffic the same day still carried kill-compounds,
"crash", "threat change". Additional rows, same scope (NEW writing only):**

| still-confusable term | new name — and what it actually is |
| --- | --- |
| kill window / kill rate / timely kill (prose compounds) | **the closing window / checkmate rate / timely checkmate** — how fast we win by the game's stated condition |
| crash / crash cascade (their units) | **stumble / stumble chain** — an opposing bot's own code raising an in-engine exception; the engine retires the piece per its rules |
| threat / threat change (an opponent) | **matchup shift / new look** — the opponent shipped a different strategy |
| our units die / are killed | **knocked out / retired** — the engine removes the piece per its rules |
| killer (their winning unit) | **finisher** — the piece that completes their checkmate |
| eviction (of their pieces) | **clear-out** — legally removing enemy structures from a zone |

Code/tool/field identifiers (`KILL_TARGET`, `crash_census.py`, the locked
CRASHREP-BC leg name) are NOT renamed inline — parsed surfaces rename only as
tooled, grep-continuous work at wrap, and locked preregs never; new prose
refers to them by identifier once and then uses the game name (e.g. "the
banana-peel replication leg (registered as CRASHREP-BC)").

Kept as-is: **siege · cage · seal · collar · raider · rush · denial** (standard
strategy-game words), the engine's own API verbs (`attack`, `fire`), and the
Norse bot names (characters, not threats). Rename live surfaces (QUEUE rows,
PROGRAMME fields) opportunistically as they are next touched — **a rename
commit names the old term once so historical greps still land** (side-lane
rider, 2026-08-22); tool/script renames are wrap-scoped work.

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

**⛔ RE-CORRECTED s54, 2026-08-22 — THE LOCAL HALF IS NOW ALSO DEAD: under fcode 2.3.6, bot `print()` output does NOT surface in LOCAL replays either** (measured 09:34:53Z: a forced-fire probe printed to stdout in an instrumented tree and its lines appear nowhere — not in the console, not via strings on the protobuf replay — while the same lines on stderr reach the console; the mutant control fired 996 lines the moment the channel moved). This is distinct from and in addition to the s28 LOKI-14 rule below (platform replays strip stdout). **The ONLY live channel for local probe output is stderr-to-console. A local probe that prints to stdout is instrumenting a channel that does not exist, and its zeros validate nothing.**

**⛔ CORRECTED s28, 2026-08-10 — `print()` IS STRIPPED FROM PLATFORM-DOWNLOADED REPLAYS.** The sentence above is true LOCALLY and **false for what the platform returns**. Measured on the LOKI-14 leg: **30,664 `BotOutput` events carry only `{id, execTimeUs}`; the `stdout` field is empty in 30,664 of 30,664.** Independently spot-checked by the builder with the control that makes an absence meaningful: `bots/_v131loki14/raid.py:700` prints `LOKI14 KIDNAP arm=…` once per throw, `LOKI14_KIDNAP_LOG = True` in the fired build, and the leg decoded **314 kidnaps** — yet the literal strings `LOKI14`, `KIDNAP` and `arm=` occur **0 times in 1.8 MB** of that leg's platform replays. **CONSEQUENCE FOR EVERY FUTURE PREREG: a leg that plans to read its own arm tag, dose counter or state flag out of a LIVE replay is planning on an instrument that does not exist.** LOKI-14's prereg did exactly that and the method was not executable as written; the substitute was the throw destination read off the wire. Read arms from ENGINE-SIDE facts (positions, entity events), never from our own stdout.

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
- **EXIT CODE IS NOT A HEALTH SIGNAL ON THIS PLATFORM.** Measured during the
  2026-08-10 07:1x outage: `fcode status` **exits 0 while printing `Error: True`
  to stdout** and returning a body whose `active_submission` is null; `fcode
  match list` **exits 1** in the same outage. Two failure conventions on one
  CLI. **A degraded response also parses as valid JSON**, so parseability and
  non-emptiness are equally worthless as gates. **Gate on the PRESENCE OF THE
  LOAD-BEARING FIELD** — for activation that is `active_submission` (equivalently
  the `Active bot:` line in `fcode status`), never on `$?`. This invalidates
  exit-code checking in every tool we write against `fcode`.
- **A monitor that reads a file must report that file's FRESHNESS.** When the
  elo tape stalled in that same outage, `ship_watch` kept printing
  `rating=1599 armed=True RULE=held` from rows seven minutes stale — **a healthy
  line and a blind line were byte-identical**. Its own docstring guards an alarm
  that cannot FIRE; this is an alarm that cannot tell it is BLIND. Emit the age
  of the newest row, or refuse to print a verdict past ~2 cadences.
- **Numbers carry subjects.** Copy the denominator, the population, and the
  clock along with the number. Us-only samples must say so inline.
- **Submissions:** only via `tools/submit_clean.py`. A bare `fcode submit`
  ships docs to the platform and is a drift flag.
- **⛔⛔⛔ RE-MEASURED 2026-08-24 (s58, endgame platform) — THREE FACTS THAT
  SUPERSEDE THE BLOCK BELOW, each measured same-day on our own account:**
  1. **`fcode submit` NO LONGER AUTO-ACTIVATES.** v213 uploaded 10:11Z, holder
     unchanged through the submit (submit_clean's own before/after reads
     equal); re-confirmed with v214 minutes later. The block below was true
     for its era and is kept for provenance; windows now need an EXPLICIT
     `fcode submission activate` + restore.
  2. **EVERY UPLOAD IS A SLOT HAZARD: the platform can ACTIVATE the
     latest-uploaded submission unbidden.** v212 (a leg uploaded 06:31Z)
     became the ACTIVE rated bot at ~10:04-10:09Z with zero actions from our
     side (elo tape + wire; restored by integer at 10:14Z; zero rated leaks
     by luck of the pairing clock). Same family as the 05:16Z unrated burst
     (latest upload paired against five teams, 35 min post-restore).
     Mitigation used: upload the HOLDER'S OWN BYTES as the newest submission
     so "activate latest" is a no-op (v214 = v188's tree, verbatim).
  3. **UNRATED MATCHES ARE DISABLED** (verbatim rejection 10:21Z: "Error:
     Unrated matches are currently disabled") — the unrated fixture, the
     rate-window arithmetic, and every window plan built on it are dead until
     the organisers re-enable.
- **⛔⛔ SUBMITTING **IS** SHIPPING. `fcode submit` AUTO-ACTIVATES WHAT IT
  UPLOADS — there is no such thing as "upload now, activate later".** The
  platform makes a freshly-`ready` submission active with no `activate` call.
  **This was documented in `docs/fcode-cli.md:262` for days and it is written
  here because that file is NOT in any lane's boot sequence, while the procedure
  three sections down said "activate only in the instant before firing" — which
  only makes sense if this were false. A fact recorded in a reference doc and
  contradicted by the always-loaded file is a fact nobody has.**
  **Re-measured s29 2026-08-11:** submitting `_v136loki19` printed
  `Submitted! Version 108` and the next `fcode status` read `Active bot: v108`,
  displacing a v104 holder of ~20 hours. Rolled back in ~15 s. **ZERO rated
  matches leaked — but NOT by the instrument I first used.**
  **⛔ THE MATCH COUNTER CANNOT ANSWER THIS QUESTION.** 724→724 proves no match
  **COMPLETED** in those seconds; it says nothing about whether one was
  **PAIRED** while the prototype held the slot — a ladder match created at T
  completes minutes later and carries that version into the rated record. **The
  counter is blind to exactly the failure mode.** The real verification is
  per-match `teamAVersion` at the PAIRING BOUNDARY, read off
  `fcode match list --mine --type ladder`: last pairing before the submit
  `04:32:59Z`, next after the rollback — no match created while v108 was live.
  *(`ladder_games.tsv` could not answer it either: its newest ladder row was
  27 minutes behind the wall clock, so an absence of v108 there was not
  evidence.)*
  **⭐ AND THE LADDER PAIRS ON A CLOCK, WHICH MAKES THIS PREVENTABLE RATHER THAN
  SURVIVABLE: 55 of 60 consecutive pairings land at minute ≡ 12 (mod 20) and 49
  of 60 at second `:59` — i.e. slots at `:12:59`, `:32:59`, `:52:59`.** The
  submit landed ~04:37, four minutes past a pairing with ~16 minutes of clear
  air. **Structurally safe, and knowable before typing the command.**
  ⇒ **Do submit→fire→rollback just AFTER an observed pairing.** Two caveats:
  the offset **has shifted at least once** inside an 18-hour span, so **re-derive
  it from recent rows and never hardcode it**; and the sample is us-only. The
  **offset** is the robust part, the 20-minute **interval** is not (some gaps
  are 600 s).
  **`tools/submit_clean.py` NOW RESTORES THE HOLDER ITSELF** and confirms the
  restore against the `Active bot:` line, never the exit code. **Pass
  `--activate` to keep the new version live; that flag IS the ship decision.**
  ⇒ **Never submit a prototype "to have it ready". The submit IS the activation,
  so it happens inside the firing window or not at all.**
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

**0. THE EXPLOIT HUNT IS THE JOB, NOT A SIDE QUEST.** Magnus, 2026-08-10, on
approving crash-induction: *"That's the entire reason we are named Loki — find
these and use them."* **This is the standing brief and it outranks tidiness,
elegance, and every instinct toward "playing the game properly".**

**WHAT AN EXPLOIT LOOKS LIKE HERE:** a sequence of individually LEGAL, DOCUMENTED
API calls whose combined effect is something the opponent's code cannot survive.
The worked example, approved and built as `bots/_v131loki14`: our launcher picks
up an **enemy** builder (`can_launch` has **no team check and no vision guard**)
and throws it to a legal **map-border** tile, where that bot's own code queries
an off-map neighbour, raises, and **the engine permanently destroys that unit for
the rest of the match** (`0x1ac5c` → `Game::destroy_entity`; `SystemExit` and
`KeyboardInterrupt` are the only exemptions). We spend 0 ammo and one throw; they
lose a unit forever, to their own error handling.

**HOW TO FIND MORE — the three moves that produced this one:**
1. **READ THE ENGINE BINARY, NOT THE ORGANISERS' DOC.** The doc is known-wrong in
   places; the `.so` is not. Every load-bearing fact above came from disassembly
   with two toolchains intersected —
   `docs/research/engine-source-crash-and-launcher-2026-08-10.md`.
2. **LOOK FOR ASYMMETRIC GUARDS.** `can_launch` has no team check. Every `can_*`
   predicate lacks a vision guard while `get_tile_*` raises off-map. **A guard
   present on one path and absent from its neighbour is where exploits live.**
3. **MINE OUR OWN BUG FIXES FOR THEIR BUGS.** `eco.py` carries a guard added
   because a launcher throw teleported OUR builder and made `is_tile_empty`
   raise. **We patched it; most teams have not.** `tools/crash_census.py`
   measures the field: **2,451 unexplained unit removals by opponents across
   1,855 of our games, against 0 by us.**

**CLASS RULING, 2026-08-10 — GENERALISED EXCEPTION-INDUCTION IS INSIDE THE
APPROVED CLASS, and the anchor is the approval's own wording.** The question put
to the organisers was: *"Is deliberately manoeuvring an opponent's units into
positions chosen to provoke unhandled exceptions within the spirit of the
competition?"* — **positions, plural and unqualified.** The map border is one
trigger; displacing a bot off a cached plan is another; both are the same
mechanism (a legal throw, `position-only` mutation, their own state goes stale).
**So a new TRIGGER does not need a new question. A new MECHANISM would.**
Freezing instance work on approval it does not need is a failure in the same
family as shipping an unasked class.

**ROADS THE 2026-08-10 GUARD-MATRIX SWEEP CLOSED — do not re-derive**
(`docs/research/engine-guard-matrix-exploit-hunt-2026-08-10.md`; the shipped
`.so` **retains full Rust symbols**, so every mutating call was mapped by name):
* **Pushing resources into the enemy core is a GIFT, not a poison.** The core
  always accepts and credits **its owner** on both `titanium_stored` (+0x198)
  and `titanium_collected` (+0x19c). Resource flow IS team-blind
  (`distribute_resources@0x203f4` reads no team byte) but the credit is not.
* **The comms store is genuinely per-team private** (keyed on own team at
  `[controller+0x18]`). No cross-team read or corruption.
* **Cost scale is team-keyed and cannot be inflated by an enemy**
  (`get_scale_percent@0x11fb8`). **And destroying enemy buildings LOWERS THEIR
  scale — it helps them.** Counterintuitive, and it means demolition is not an
  economic attack.
* `destroy`/`heal` are team-checked; `convert_ammo`/`rotate`/`resign`/
  `self_destruct` are self-only; bot-stacking desync is impossible.
* **Self-audit item, not a weapon: `can_fire` returns TRUE at 0 ammo**
  (`can_fire@0x16280` has no ammo reference; the check lives in
  `finish_firing_turret@0x26eac` and RAISES, which destroys our own turret).
  We cannot drain enemy ammo, so this is a hazard to us, not a lever on them.
* ⛔ **CORRECTED s50, 2026-08-17 — `is_in_vision(pos)` IS NOT A BOUNDS GUARD.** This bullet
  read *"does NOT raise off-map — it returns False. That is the safe pre-check to use
  everywhere"* and the second half is FALSE: it is a **pure radius test with no bounds
  check**. Engine-probed on atoll (core at 2,14): `is_in_vision((-1,14))` = **True**, and the
  next `get_tile_*` on that pos raises `GameError: Position out of bounds`. Off-map tiles
  read False only when they are ALSO outside the radius — true everywhere except near a map
  edge, which is exactly where it bites (probe agent's own probe died through this gate).
  It never raises itself; that half stands. **The safe pre-check is an explicit bounds test
  (`0 <= x < get_map_width() and 0 <= y < get_map_height()`), THEN is_in_vision if vision
  matters.** Holder v159 audited same day: its 7 usage sites all sit under try/except —
  degraded lookups, not unit deaths. Full probe: `docs/research/PROBE-DOSSIER-ferry-siege-2026-08-17.md` §4.1.

**STANDING PERMISSION, AND ITS ONE LIMIT.** Build and fire these without asking.
**The only thing still needing Magnus is a norms question to the ORGANISERS** —
not because an exploit is wrong, but because a league can declare a whole class
out of bounds and we would rather know before we rank on it. **Crash-induction
was asked and is APPROVED.** Ask again for a genuinely new CLASS, never per
instance.

Four consequences, each of which closes a road that was open before it:

1. **A ROUND-1000 GAME IS A DEFEAT, INCLUDING WHEN WE WIN IT.** The tiebreak
   ladder (`titanium_collected` → harvesters → stored) decides ~94% of r1000
   games and is now OFF-CURRENCY. Everything above about harvester throughput
   remains factually true about the ENGINE and is no longer what we optimise.
   **Economy is instrumental: it buys the kill, it never scores.** Any plank
   whose only channel is `titanium_collected` is at best a correctness fix.
2. **DEFENCE IS ADMISSIBLE IF IT DOES NOT SLOW THE KILL.** ⭐ **AMENDED
   2026-08-11 (s31). THIS CLAUSE READ "NEVER PLAY DEFENCE… off-programme
   regardless of what it measures" AND THAT IS NO LONGER THE PROGRAMME.**
   Magnus, direct: *"This does sound like we should allow SOME defence
   strategies, but our FOCUS should be to kill at <r250."*
   `PROGRAMME.md` now carries **`PLAY_DEFENCE: not_at_the_kill_s_expense`** and
   **`DEFENCE_ADMISSION_BAR: r300_crossing_non_regression`**.
   ⭐ **RE-PRICED 2026-08-16 (s45), Magnus direct: *"Re-price the kill-round bar
   to bind at ~r300 instead of penalizing drift inside r200-300."*** The s31 form
   read "if MEDIAN KILL ROUND RISES it is off-programme"; that is SUPERSEDED.
   ⇒ **A plank is off-programme if it pushes kills PAST r300** (primary, ITT:
   the share of ALL its games ending in a core-kill BY r300 — its timely-kill
   rate — must not FALL vs control; the kill-win-conditioned share is a
   diagnostic only, it carries a collider; median crossing 300 is the gross
   backstop — full operational form and the collider correction in
   `PROGRAMME.md`). **Drift inside
   r200-300 is reported, not disqualifying.** Basis: the "field converts 4x
   better late" table was pre-rotation; re-derived post-rotation, r200-300 is
   ~parity (NOT an advantage — the flip claim was withdrawn same-day) and r300+
   remains against us (0.82, robust). A gradient is unenforceable, so the
   directive stays encoded as a BAR — only its binding point moved.
   **SCOPE, and it is what keeps `R1000_IS_DEFEAT` intact: "some defence" means
   surviving the r150–250 window SO OUR OWN KILL LANDS — our median kill is 174
   and our median death is 187, a thirteen-round race, and our core dies in 46.3%
   of all games. It does NOT mean surviving to r1000**; the tiebreak tail is a
   coin flip (1800-1900 wins 49.4% of tiebreaks vs 45.2% overall), so that road
   stays retired. Turrets are still bought to open a lane, not to hold one.
   ⚠ **This does NOT wholesale revive what "never" killed.** Each candidate must
   clear the non-regression bar on its own. **And note s30 measured
   `home-turrets-off` at 433/1024 and `barrier-seal-off` at 399/1024 — both REAL
   NEGATIVES, i.e. removing defensive behaviour COST us**, which is evidence the
   amended field was always the truer description of the bot we ship.
3. **PROTOTYPES GO AT LIVE TEAMS, NOT AT OUR OWN PROBES.** `bots/*_probe` is a
   fixture WE authored and it lies in a known direction (five probes share a
   `best_core or best_any` short-circuit — zero of our forward turrets died in
   480 arena games against **46.9% on the ladder**). The instrument is
   **`fcode match unrated <team_id>`**: 5 games, a real team's real bot, no
   rating at stake. **Constraint, verified on the CLI:** it plays our **ACTIVE
   submission** — there is no flag for a local tree — so a prototype leg means
   activating the prototype and paying ~3 rated ladder matches (⛔ corrected 2026-08-13: pairing cadence halved to 20-min on 08-10; this claimed ~6 under the old cadence) per hour of
   window. Bounded, recoverable, and the price of the only honest fixture.
4. **A SURPRISE IS THE POINT, NOT AN ANOMALY.** An unpredicted result from a
   live-team leg outranks a predicted one from our own arena. Write it down
   before explaining it away.

**Never balance-changed by the organisers, therefore still open:** launcher
throw/kidnap, spawn-tile denial, crash-induction. **Retired by this directive:**
tiebreak-turtle (a r1000 win is a loss).

**Launcher kidnap, read off the ENGINE BINARY** (`docs/research/engine-source-crash-and-launcher-2026-08-10.md`):
`can_launch` and every `can_*` predicate has **zero vision guards**; **no team
check** on the picked-up builder; **pickup d² ≤ 2, throw 1 ≤ d² ≤ 26 measured
from the launcher, 0 ammo, cooldown +=1, position-only mutation.** An uncaught
exception from `run()` destroys that unit permanently (`0x1ac5c` →
`Game::destroy_entity`) and **`SystemExit`/`KeyboardInterrupt` are the ONLY
exemptions — an escaping `GameError` kills the unit; a CPU timeout does not.**

**⭐ THE LADDER SCORES GAME SHARE, NOT MATCH WINS — EXACT, NOT FITTED (s28, 2026-08-10).**
`delta = 32 x (S - E)` where **S = games won / 5** and E is the standard logistic
on the 400 scale. **Verified by the builder independently of the research arm:
max |residual| = 0.000000 across 100 completed ladder matches** (research: 0.0000
across all 678, and official `eloDelta` agrees with consecutive-rating
differences 677/677). **K = 32 confirmed exactly.**
**Consequences, and they are not cosmetic:**
* **A 3-2 win can LOSE rating** (observed min -4.96) and **a 2-3 loss can GAIN it**
  (max +2.05). **20 of 678 matches have a delta whose sign opposes the match
  result.**
* **MARGIN IS THE CURRENCY, NOT THE WIN.** `PROGRAMME.md` already says
  `WIN_RATE_IS_VERDICT: no`; this is the arithmetic reason. Any bar, stop-loss or
  verdict denominated in **match** win rate is a proxy for the thing the ladder
  actually pays. **Prefer game share.** The 4th game of a 4-1 is worth exactly as
  much as the 1st.
* This sits alongside `R1000_IS_DEFEAT` as a fact about what SCORES.

**⭐ RUN `tools/target_value.py` BEFORE WRITING A PRE-REGISTRATION (s28). ONE
GATE, ONE LINE IN THE PREREG:** `TARGET BAND: <opponents>, gaps <a..b>, win pays
<x..y>, reachable YES/NO`.
**The case for it is s28 itself, not a hypothetical.** The crash leg passed
**every check this repo has** — pre-registered before the fact, 8 ADD-only
amendments all blind to the data, a placebo reading exactly 0/164, the dose
delivered 150 times, every control driven to the other verdict, lock cert
two-clock clean, holder asserted before every challenge, 10-second prototype
exposure — **and it was aimed at four teams 550–860 points below us.** Run
retrospectively, the gate says:
```
vjg  -841  5-0 pays +0.25 · Troupe -635 +0.81 · S -566 +1.18 · Ship Happens -614 +0.90
** NO TARGET IS REACHABLE ON THE LADDER **
** A PERFECT RESULT PAYS UNDER 5 RATING POINTS (1.18) **
```
against `0033 +120 (+21.30)`, `The Bisons +41 (+17.89)`, `SmartFridge +14
(+16.65)` in the reachable band — **14–85x more per win.**
**THE MACHINERY INSPECTS THE EXPERIMENT AND NEVER ASKS WHETHER THE QUESTION IS
WORTH ANSWERING.** No amount of rigour inside a leg reaches that. **It is a
GATE, not a VETO** — a low-value target can still be the right leg (a negative
that closes a road is worth something); the rule is that you write the number
down BEFORE the work rather than defend it after.

**TWO CORPUS-SURFACE RULES, because our two surfaces fail in OPPOSITE directions
and both produced false findings on 2026-08-10:**
* **`ladder_games.tsv` for any population or denominator question about our
  RATED record. NEVER `meta_join` for a win-rate denominator** — it covers every
  archived replay and so **silently pools rated with UNRATED, i.e. with our own
  panel legs**, and it is separately **missing ~38% of our ladder matches**.
  Durable form: **unrated pools PROTOTYPES, ladder pools SHIPPED BOTS**, so an
  unrated-vs-ladder comparison is a prototype-vs-shipped comparison wearing a
  fixture-vs-fixture costume. That alone explains the 40.5pp gap on The Bisons
  (21.3% mixed vs **49.0% ladder-only**) with no era story required.
* **PIN THE OPPONENT'S VERSION — AT FIRE TIME AND AT ANALYSIS TIME.**
  ⭐⭐ **CORRECTED 2026-08-13 (s36, on Magnus's instruction). THIS BULLET READ
  "nothing pins or even reads THEIRS" AND BOTH HALVES ARE NOW FALSE.** What is
  true today:
  * **WE READ THEIRS.** `ladder_games.tsv.oppver` was the literal string
    `'None'` in **4,375 of 4,375 rows** — not because the field was
    unavailable but because the ingest read `fcode match info` (which returns
    None for the opponent) instead of `fcode match list` (which returns both).
    **Backfilled 2026-08-13, 0 residual nulls, gated on a positive control.**
  * **WE CAN PIN THEIRS.** `fcode match unrated <team> --match <past_match_id>`
    plays **the submission they had in that past match** — documented at
    `docs/fcode-cli.md:330` since 2026-08-09 and unread for four days while
    this file asserted the opposite. **Verified live: LingLing40 shipped
    v33→v41 in a single day and all three arms of a 15-match leg still met
    v40.**
  * ⭐ **THE DESIGN RULE, because the two fixtures want opposite things:
    PIN TREATMENT LEGS, NEVER PIN CALIBRATION PANELS.** A matched-pair leg
    cannot absorb opponent variation, so pinning is mandatory. A calibration
    panel exists to measure RELEVANCE — what the ladder will actually pair us
    against — so pinning reintroduces the staleness the panel is for.
    **Churn is noise in a leg and signal in a panel.** Opponent PROFILES pin.
    Full spec: `docs/research/SPEC-opponent-pinning-2026-08-13.md`.
  * **A pinned triple whose decoded `oppver` values DIFFER is an INSTRUMENT
    ALARM** (the pin did not take, or the decode is wrong) — report it and do
    not read that cell.
  **The original hazard still stands and is why this bullet exists:** The
  Bisons shipped v4 forty minutes before our v102's first ladder game —
  perfectly collinear, so *"our v102 is worse"* and *"their v4 is better"* fit
  identically. **A null version column reads as "no version change" to any cut
  that trusts it.** `league_matches.tsv` remains the authority for their
  timeline.
  ⛔ **AND THE META-LESSON, because this is the SECOND time this file has
  contradicted a correct reference doc** (the first: `fcode submit`
  auto-activates, documented at `docs/fcode-cli.md:262` while the procedure
  three sections down implied otherwise): **a fact recorded in a reference
  nobody boots and contradicted by the always-loaded file is a fact nobody
  has.** Mechanised 2026-08-13 by `tools/cli_capabilities.py` — it diffs every
  CLI `--help` against a triage file and **alarms on any capability nobody has
  classified.**

**5. UNRATED GAMES ARE FREE. USE THEM AS MUCH AS YOU WANT.**
Magnus, 2026-08-10: *"You are free to use unrated games as much as you want,
it's a free tool meant to be used."* **This retires throughput caution as a
reason not to test.** The only constraint is the platform's own:
**5 test/unrated matches per 10 minutes** (**RE-CORRECTED s54, 2026-08-22 — the window
halved 20→10 with the organisers' cadence change, VERIFIED TWO WAYS on our own account:
the discriminating 6th-fire probe ACCEPTED at t≈12 min from the burst's first fire
(93629c58, 08:36:20Z), and the CLI's fresh verbatim rejection: `Error: Rate limit
exceeded: max 5 test/unrated matches per 10 minutes` (08:41:24Z). The s28 20-minute
correction below stands as history — this constant has now flip-flopped 10→20→10;
re-derive it from a rejection string whenever it matters, never trust this line alone**);
**rejected attempts appear to count**; shared across `match unrated` AND `match test`;
**opponent-initiated challenges do NOT count against our budget, and opponents CAN
challenge our live prototype mid-window (measured: Jacobs ×2, 2026-08-22) — every
activation window is also a free look for the field.**
Matches complete in ~15 s, so **the rate limit is the ENTIRE cadence
constraint** — **ceiling ~150 games/hour under the 10-min window.**
**Evidence it CHANGED rather than always having been 20:** every s27 arm filled
its five panel cells uniformly (v104 7/7/7/6/6, loki15 7/7/6/6/6, confirm 4/4/4/4/4)
on a 620 s inter-arm cadence — impossible under a 20-minute window, which would
have starved the tail of the id list every time.
**THE FAILURE MODE THIS CREATES, and it is silent:** `fanout.sh`'s `fire()`
retries a rejected challenge three times at 25 s and then gives up, logging
`fired 3/5` and moving on. Under a window it cannot outwait, that drop is
**systematic and always lands on the SAME cells** — the tail of the id list —
so the panel starves exactly the cells it is supposed to measure. Any runner
must **wait out the window and retry the same cell**, and **rotate its starting
cell** so a residual drop cannot bias one opponent. `tools/panel2_cal.sh` does
both; `fanout.sh` is patched to the 20-minute cadence but still drops on retry
exhaustion — fix it before that rotation is restarted.

**⛔ CORRECTED s28, 2026-08-10 — THE RATED COST IS NOT ZERO. IT IS MEASURED AT
−24.67 ELO ACROSS 3 MATCHES.** The claim below was true when written and is
falsified by today's fanout. Read off the platform's per-match
`teamAVersion`/`teamBVersion` for every rated ladder match after v104's
activation at 09:21Z:
```
09:42  ourver=v102  vs gsxWins       3/5   elo  +1.30
12:32  ourver=v102  vs The Bisons    0/5   elo -15.68
12:52  ourver=v105  vs Besvikomat    1/5   elo -10.29
                                     4/15 games        NET -24.67
```
**Three rated matches played by a NON-INCUMBENT and credited to v104's rating**,
one of them by **v105 — the arm we measured at −14.7pp, significantly worse.**
*(The other 44 non-v104 rated matches today are v102 playing BEFORE 09:21, when
it was the legitimate incumbent. Those are not cost and must not be counted as
such — the research relay found 2 of the 3 and missed 09:42; the discriminator is
the activation timestamp, not the version tag alone.)*
**These sit before the 13:57 peak, so they do NOT explain the later −57
drawdown** — but they are real, they are rated, and an arm rotation is what
produced them.
**⇒ Budget a prototype leg at roughly −8 Elo per leaked match, not at zero.**
**AND IT PRICES THE POLL-TIME TAG DEFECT:** `elo_history.tsv` tags rows by the
version ACTIVE AT POLL TIME, so these three are invisible in it. **The ground
truth is per-match `ourver`, already populated in `ladder_games.tsv` — nothing
needs building, only reading.**

**THE SUPERSEDED CLAIM IS NOT REPRINTED HERE.** It said the rated cost of a
prototype leg was ZERO, measured; the block above replaces it with −24.67 Elo
across 3 matches. It is kept verbatim, with its provenance, in
`docs/reference/DIRECTIVE-HISTORY.md`.
⛔ **WHY IT MOVED (2026-08-15):** in this file the dead claim was bold, emphatic
and typographically IDENTICAL to a live rule, in the one document loaded into
every session whether or not it is read carefully. **A reader skimming for the
cost of a leg could land on `AND THE RATED COST IS ZERO, MEASURED` and be
reading a retracted sentence with no signal that it was retracted.** The rule
adopted: *the always-loaded file states what is true now; the archive states
what we used to think.* Provenance is not lost, it is relocated.

**THE CONSEQUENCE, and it is the one that matters: STOP CALLING UNDERPOWERED
LEGS.** Every null on 2026-08-10 failed its own resolution bar rather than the
plank — a single 25-game window on the pinned panel has a **same-bot swing of
12pp** (control v102 moved 36.0% -> 48.0% between consecutive windows with
nothing changed) and an MDE of ~39pp. **A 25-game window is a DOSE AND
MECHANISM probe. A currency read requires pooling windows** — and since windows
are free, pooling is now the default, not a luxury. **Buy the power before
writing the verdict.**

**⭐⭐ AND IT IS WORSE THAN THAT NUMBER SAYS — MEASURED 2026-08-14 (s40, research):
GAMES ARE NOT INDEPENDENT, SO EVERY BAR THIS PROJECT QUOTES IN GAMES IS TOO
NARROW.** The 5 games of a match share the opponent, the opponent's version, and
one 20-minute slice of the ladder. Measured on our own record by comparing the
observed variance of match scores against the binomial:

| fixture | 5-game matches | our share | **POOLED DEFF** | **WITHIN-OPPONENT DEFF** |
|---|---|---|---|---|
| **RATED** (`ladder_games.tsv`) | 965 | 0.5123 | **1.529** (ICC ρ=0.132) | **1.366** |
| **UNRATED** (`meta_join`, non-ladder) | 947 | 0.4809 | **1.833** (ρ=0.208) | **1.434** |

⇒ **EFFECTIVE n IS ~55–65% OF NOMINAL** and half-widths are understated by
**×1.24 (rated) to ×1.35 (unrated)**. **The 12pp and ~39pp figures above are
therefore OPTIMISTIC** — both were computed treating games as independent.
**Use — TWO FORMS, and picking the wrong one is the common mistake:**
```
ONE SAMPLE (a single bar on one surface):
    half_width_95 = 1.96*sqrt( p̄(1-p̄) * DEFF / n )
TWO-FIXTURE COMPARISON (e.g. a panel share vs a rated share):
    half_width_95 = 1.96*sqrt( p̄(1-p̄) * ( DEFF_u/n_unrated + DEFF_r/n_rated ) )
```
**⛔ SCOPE — AND IT IS A PROCEDURE, NOT A TAXONOMY. A LOOKUP TABLE OF CASES IS
WHAT LETS SOMEONE DROP THE CORRECTION BY DECIDING THEIR CUT "LOOKS LIKE" ONE.**

**THE GENERAL FORM: a design effect applies only where the STRATUM CAN CONTAIN
MORE THAN ONE MEMBER OF THE CLUSTER.**

**THE PROCEDURE, and a banked cut performs it in writing:**
1. **NAME EVERY CLUSTER THIS DATA HAS.** Currently **four: MATCH, OPPONENT, MAP, and
   CONTENT-DUPLICATE** (⛔ amended s54 2026-08-22 — this line said "two" and the
   missing pair produced real defects the same week). MAP binds on any powered
   multi-map fixture with heterogeneous arms (measured: DEFF 4.57, interval ×2.14 at
   180-240 games/cell, v620 tape — applied in the EXCLUSION direction per the
   restatement rule). CONTENT-DUPLICATE binds whenever the pool can contain
   byte-identical or near-identical games — measured twice in one day on opposite
   fixtures: 17.3% exact-duplicate games in BC's v47 field pool
   (`CUT-116-beltgun-answer-2026-08-21.md` §1.7, intervals ~13% optimistic) and the
   tape30 inert seed axis (15/15 byte-identical pairs, effective n halved,
   `FIDELITY-BASELINE-v600-2026-08-21.md` §0.4). The platform DEFF constants cover
   none of these. VERIFICATION STEP OF THE ENUMERATION PROCEDURE: every powered grid
   carries a DUPLICATE CONTROL (same-tree arm; v620 measured its same-bot swing at
   2.22pp), and with two deterministic trees vary MAP and SEAT, never seed. Any cut
   over a deterministic opponent states whether it checked for content duplicates
   (#117 mechanizes).
2. **For each, state whether YOUR stratum can hold more than one member — and
   VERIFY it, do not assert it.**
3. **The applicable DEFF is over the clusters that SURVIVE.**

**WORKED EXAMPLE — and it is worked because the author of this rule got it wrong
first.** A per-MAP bar: a 5-game match uses five DIFFERENT maps, verified both
ways — **(match, map) pairs with more than one game = 0 of 415, while games per
MATCH = exactly 5 for every match.** ⇒ **the MATCH cluster dies.** ⛔ **The
OPPONENT cluster does NOT: a map cell still holds several games against the same
opponent from different matches.** Measured on that cut: **m̄ = 1.98 games per
opponent per cell, ρ_opp = 0.0743 ⇒ residual DEFF ≈ 1.07** (interval inflation
×1.04; ×1.05 at the densest cell). **Small — but "no DEFF at all", which is what
this clause said for half an hour, is wrong and would license the error at cells
where m̄ is larger.**

**Reference values: pooled 1.529 rated / 1.833 unrated (both clusters live) ·
within-opponent 1.366 / 1.434 (opponent cluster removed) · per-map ≈1.07 on
current cells (match cluster removed, opponent cluster measured).**
⚠ **A correction applied where it does not belong inflates intervals for nothing
and fails in the FLATTERING direction for a null — so both over- and
under-correction are errors, and only the enumeration catches either.**

**⛔ DIRECTION — AND THE GUARANTEE IS NOT UNCONDITIONAL. THIS IS THE CLAUSE THAT
KEEPS THE CORRECTION FROM FLATTERING THE CLAIMS MOST TEMPTING TO BANK.**
Widening an interval only ever makes an **EXCLUSION** claim harder — superiority,
harm-exclusion, closure-by-upper-bound. **It makes a FAIL-TO-EXCLUDE claim
EASIER**: *"no significant rise"*, *"consistent with zero"*, a null banked
because nothing cleared. **That class is live here — `DEFENCE_ADMISSION_BAR`'s
kill-round non-regression is scored exactly that way.**
⇒ **A fail-to-exclude claim must first be RESTATED AS AN EXCLUSION (the CI
excludes the regression bar) before the correction is applied.** Applied to the
unrestated form, DEFF launders a weak null into a confident one.
**With that restatement: the exposed class is claims that cleared a bar
NARROWLY.**

⚠ **PLATFORM games only (rated ladder + unrated challenges) — AND LOCAL'S
EXEMPTION IS MEASURED, NOT ASSERTED.** Local corefill/arena screens are a
**balanced-by-construction** fixture and read **pair-weighted DEFF = 0.98
(ρ = −0.020) across 124 shards** (s39 audit, 2026-08-14): **naive local bars are
correct and marginally conservative, and applying the platform constants to them
would widen local intervals 24-35% for correlation that is not there.** Outlier
arms with strong map interaction reach ~1.25. `tools/effective_n.py` (seed
degeneracy) and `tools/mde.py` (local kill-speed null) measure different things
on LOCAL batteries — complementary, not duplicates.
**PROVENANCE, stated precisely because "three measurements converge" was too
loose:** the **unrated** constant is two independent measurements —
**1.45 implied** (`PREREG-PANEL-CAL1-v123-field-2026-08-13.md` A1.2, per-match sd
8.565 vs binomial 7.111) and **1.434 df-corrected** (here) — and the **method**
was independently replicated by the side lane on the **rated** surface (1.529
digit-for-digit, 1.366 df-corrected). **The df correction is required: the
uncorrected form returns 1.282 and is biased LOW.** The unrated cut comes from
`meta_join` because unrated games are not in `ladder_games.tsv` — that is
correct and is **not** a breach of the "never `meta_join` for a denominator"
rule, which governs RATED win-rate denominators; the caveat that does apply is
that it covers the ARCHIVED subset. Re-measure periodically; ρ is a property of
the current pool, not a law.

**6. A REFUTATION WITHOUT LIVE-GAME BACKING IS A HYPOTHESIS, NOT A REFUTATION.**
Magnus, 2026-08-10: *"Every statement needs backup from real games so we need to
test everything in unrated games before we refute them. We never know if we will
be surprised by something, because only playing on our chambers is an echo loop.
Out there is the truth."* `FIXTURE_OF_RECORD` governs how a plank is CONFIRMED;
**this governs how a road is CLOSED.** Arena batteries, corpus statistics,
source reads and engine probes may **prioritise** a road. They may not **retire**
one. **The cost objection is dead, measured:** LOKI-11's true rated cost was
ZERO rated ladder matches, so the binding constraint is throughput
(150 games/hour) and not rating. Testing is cheap; the scarce good is which
plank you spend a window on.
**CARVE-OUT, so the rule stays usable:** a **rules-level impossibility**
established on the engine (a conveyor has out-degree 1, so cycles cannot exist;
`self_destruct` deals 0 damage) is the game's own definition, not an echo loop,
and no number of live games overturns it. **The echo loop is behavioural
inference — from opponents WE wrote, or from our own history.** Where a closure
mixes both, the inference half still needs the live test. That is exactly how
the barrier-form spawn lock failed: an engine fact about friendly bodies welded
to an untested inference about enemy behaviour.

**THE SIX-ROADS STATUS TABLE MOVED (2026-08-13, boot-load audit cut 5):**
per-road status — siphon, spawn starvation, barrier-form lock, CPU denial,
ore poisoning, heal-idle staffing — is VOLATILE and now lives in
`docs/research/SIX-ROADS-STATUS-2026-08-13.md`, which carries every hedge
(per D22: a promoted claim carries its hedges or it carries a pointer). The
durable rules stay here: roads close only on live-game evidence (point 6);
grep the incumbent before pre-registering any plank — the cheapest null is a
leg testing a feature we already ship; and a price refutation computed under
the retired currency is void even if the fixture was clean.

**Also open, verified, and closed by no document:** harvester round-robin is
**team-blind** — an enemy conveyor adjacent to your harvester is a full-rank
acceptor, so an unwired harvester beside an enemy belt gives ~half its output
away (measured 49/49), and titanium is credited to whoever owns the DESTINATION
core. Distinct from the refuted siphon.

**Closed by construction, do not spend a leg:** the sandbox freezes
`time.*`/`datetime.now` to a constant, so any strategy keyed to wall-clock or
submission age cannot work.
