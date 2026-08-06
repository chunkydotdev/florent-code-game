


=== docs/quick-start ===
### Quick Start

Get up and running in four steps.

### Prerequisites

- Python 3.12 or 3.13 (Python 3.14 is not supported)

- pip (bundled with Python)

- A registered account on the platform

### Step 1 — Install the CLI

```
pip install fcode
fcode --version
```

### Step 2 — Authenticate and scaffold a project

```
fcode login
fcode starter
```

fcode login opens a browser window to link the CLI to your platform account. fcode starter scaffolds a project in the current directory: an fcode.toml, a starter bot at bots/starter/main.py, and a maps/ folder that it fills with the current competition map pool.

Log in before scaffolding — maps are downloaded from the platform, not bundled with the CLI. If you scaffold while logged out, run fcode maps sync afterwards to fetch them.

### Step 3 — Run a local match

```
fcode run starter starter
```

fcode run takes two bots — pass the starter twice for a mirror match. A replay file replay.replay26 is written to the current directory when the match finishes.

Watch the replay in the visualiser:

```
fcode watch replay.replay26
```

### Step 4 — Submit

```
fcode submit bots/starter
```

Your bot is queued for ladder matches. Check the Matches page on the platform to track results.

Next steps:

- CLI reference — full guide to each command

- Game Rules — Overview — understand the map, units, and win conditions

- Controller API Reference — every method available inside run()



=== docs/game-rules-overview ===
### Overview

### Win condition

Destroy the opponent's Core. The Core is each team's single base unit; losing it immediately ends the match as a loss.

If neither Core is destroyed by the end of round 1000, the winner is decided by tiebreakers, in order: most titanium collected, then most harvesters, then most titanium stored, then a coin flip.

### The map

Matches are played on a rectangular grid ranging from 8×8 to 30×30 tiles. Each tile has one of the following environment types:

Environment | Description | 
EMPTY | Traversable by Builder Bots and buildings. | 
WALL | Impassable — blocks all movement and line-of-sight. | 
ORE_TITANIUM | Ore tile; a Harvester built here generates extra titanium. | 

Maps are symmetric and chosen from the competition map pool at random for each match.

### Units and buildings

Every entity on the map belongs to a Team (A or B) and has an EntityType. There are two overlapping categories:

- Units — the Core, Builder Bots, and turrets (Gunner, Sentinel, Launcher). Each runs its own instance of your bot code and uses CPU time every round.

- Buildings — everything immovable: the Core, turrets, conveyors, splitters, harvesters, and barriers.

The Core and turrets are both a unit and a building — Builder Bots are the only unit that isn't also a building, and conveyors/splitters/harvesters/barriers are the only buildings that aren't also units.

### Unit cap

Each team may have at most 50 living units at any time — this includes the Core, Builder Bots, and turrets. Attempts to spawn a Builder Bot (or build a turret) when the cap is reached will fail.

### Turn order

Each round, every living unit executes its run() method in the order it was spawned — the Core (spawned first) always acts before any Builder Bot or turret built later in the match. Within a round, resource changes made by one unit are immediately visible to the next unit that acts.

### CPU time limit

Each unit has 10 ms of CPU time per round, plus a banked extra-time buffer of up to 5% of that limit (unused time is banked; overuse is debited from the bank). If run() exceeds the available time, execution is interrupted immediately and the unit does not resume where it left off — run() is simply called again fresh next round. Use ct.get_cpu_time_elapsed() inside run() to monitor usage.

### Uncaught exceptions

A CPU-time interruption only costs that unit a single round — run() is called again next round as normal. An uncaught exception is not recoverable in the same way: if run() raises anything it doesn't catch (a GameError or otherwise), the engine logs the traceback to the replay and permanently removes that unit from the match. It will never act again for the rest of the match. Wrap risky calls in try/except (see GameError) if a unit should keep playing through an error instead of being destroyed.

### Round limit

Matches end after 1000 rounds if neither Core has been destroyed.



=== docs/game-rules-core ===
### Core

### Overview

The Core is a large, stationary base unit. Each team begins the match with exactly one Core placed on the map. It cannot be moved or rebuilt — if it is destroyed, the match is immediately lost.

### Stats

Property | Value | 
HP | 500 | 
Footprint | 2×2 tiles | 
Vision radius² | 36 | 
Spawn range² | 2 (adjacent ring, including diagonals) | 

### Abilities

### Spawn Builder Bot

The Core can spawn a Builder Bot on any passable tile within its spawn range — a tile orthogonally or diagonally adjacent to its 2×2 footprint (not the footprint itself).

```
if etype == EntityType.CORE:
    for pos in ct.get_nearby_tiles(dist_sq=2):
        if ct.can_spawn(pos):
            ct.spawn_builder(pos)
            break
```

Spawning costs titanium (see ct.get_builder_bot_cost()). The new bot becomes active in the same round it is spawned.

### Convert ammunition

The Core converts your team's titanium into ammunition at a 1:1 rate. Turrets fire directly from this shared ammo balance — see Turrets.

```
if etype == EntityType.CORE:
    if ct.get_global_ammo() < 20 and ct.can_convert_ammo(10):
        ct.convert_ammo(10)
```

- convert_ammo(amount) moves amount titanium from your team balance into ammunition; can_convert_ammo(amount) is the legality check.

- At most one conversion per team per turn.

- Converted ammunition is usable the same turn.

- Converting does not use the Core's action cooldown — it never costs you a spawn.

- Teams start with 0 ammunition, and there is no passive ammo income — conversion is the only source.

### Notes

- The Core counts toward the 50-unit cap, like every other unit.

- The Core has no movement or attack actions — its active abilities are spawning Builder Bots and converting ammunition.

- Passive income (10 titanium every 4 rounds) is granted to each team directly and isn't tied to the Core or any other unit.



=== docs/game-rules-harvester ===
### Harvester

### Overview

Harvesters are buildings that generate passive titanium income. A Builder Bot constructs a Harvester on an ORE_TITANIUM tile, and from then on it periodically outputs titanium to an adjacent building without any further action from your bots. Harvesters are buildings, not units — they don't count toward the 50-unit cap and consume no CPU time.

### Stats

Property | Value | 
HP | 30 | 
Base cost | 20 Ti (scales +5% per Harvester built) | 
Output | 10 Ti every 4 rounds | 
Blocks movement | Yes | 
Blocks LOS | No | 

### Output behavior

Every 4 rounds, a Harvester outputs one stack (10 Ti) to an adjacent building, prioritizing whichever of its 4 cardinal output directions was used least recently — the same round-robin pattern used by Splitters. The first output happens immediately on the round the Harvester is built, not after waiting a full 4 rounds.

### Building

Harvesters can only be built on ORE_TITANIUM tiles:

```
if ct.get_tile_env(pos) == Environment.ORE_TITANIUM:
    if ct.can_build_harvester(pos):
        ct.build_harvester(pos)
```

### Notes

- Harvesters are buildings, not units — they don't count toward the 50-unit cap.

- They have no move or action cooldown of their own; their output timer runs independently of your bots' CPU budget.

- Use ct.destroy() to remove a Harvester you no longer need, same as a Conveyor or Splitter.



=== docs/game-rules-turrets ===
### Turrets

Turrets are stationary combat buildings constructed by Builder Bots. Like every other unit, each turret runs its own instance of your bot code once per round.

Gunners and Sentinels fire from your team's global ammunition balance — each shot deducts its ammo cost (4 for a Gunner, 10 for a Sentinel) directly from the shared pool. Turrets hold no ammo themselves, don't accept resources from conveyors, and never need feeding. Ammunition is produced at the Core by converting titanium 1:1 with convert_ammo(); any unit can check the balance with ct.get_global_ammo(). Launchers use no ammo.

Gunners have a facing direction set at build time and adjustable with ct.rotate() — Sentinels also face a fixed direction set at build time, but cannot rotate afterward. The Launcher has no facing direction at all.

### Gunner

A rapid-firing turret that fires a narrow forward ray.

Property | Value | 
HP | 25 | 
Cost | 20 Ti | 
Damage | 7 | 
Ammo per shot | 4 | 
Fire pattern | Forward ray (single tile width) | 
Reload | 1 round | 
Vision / attack radius² | 13 | 

The line stops at the first targetable tile (a builder bot or a building) in its facing direction; empty tiles don't block it, but walls do (and aren't themselves targetable). It is the cheapest turret to build and the only one that can rotate after being built, which makes it good at holding a corridor whose threat direction changes. It is also the most fragile turret and the least ammo-efficient one, and each Gunner adds +20% to your cost scale — the same tax as a Sentinel — so massing them gets expensive quickly.

### Sentinel

A durable long-range turret that fires an obstacle-piercing line.

Property | Value | 
HP | 40 | 
Cost | 30 Ti | 
Damage | 18 | 
Ammo per shot | 10 | 
Fire pattern | Single-tile-wide straight facing line (same width as Gunner, but longer and unblockable) | 
Reload | 2 rounds | 
Vision / attack radius² | 32 | 

Sentinels hit a single tile-wide line along their facing direction, just like a Gunner's shot — but the line reaches much further (vision/attack r²=32 vs. Gunner's 13) and, unlike a Gunner's, is never blocked by walls or units in the way. Each shot costs a large lump of ammunition, but per point of damage a Sentinel is slightly cheaper to run than a Gunner, and it out-damages one over time: 18 every 2 rounds against 7 every round. It is also the toughest turret at 40 HP, so digging one out with Builder Bots takes 20 hits. Facing is fixed at build time; Sentinels cannot rotate.

### Launcher

A utility turret that picks up and throws Builder Bots.

Property | Value | 
HP | 30 | 
Cost | 20 Ti | 
Action | Picks up an adjacent (including diagonal) Builder Bot from either team and throws it to any bot-passable tile in range | 
Pickup radius² | 2 (adjacent, incl. diagonal) | 
Throw radius² | 26 (measured from the Launcher, not the bot) | 
Reload | 1 round | 

The Launcher does not deal direct damage and needs no ammo. Its value is rapid redeployment — it can throw a Builder Bot up to sqrt(26) tiles away in one action, enabling surprise attacks or fast base expansion. It works on Builder Bots from either team: as well as moving your own bots, you can grab an enemy bot that wanders adjacent and fling it somewhere harmless. It has no facing direction and cannot rotate.

### Rotating turrets

Only the Gunner can rotate after placement:

```
if ct.can_rotate(Direction.WEST):
    ct.rotate(Direction.WEST)
```

Rotation costs exactly 10 Ti and triggers a 1-round action cooldown. Sentinels and Launchers have no rotate() — their orientation (or lack of one) is fixed for their lifetime.



=== docs/global-comms ===
### Global Communication Store

The Global Communication Store gives all your bots a shared blackboard: 16 integer slots that persist across turns. Use it to coordinate strategy without hard-coding locations.

### API

Method | Returns | Description | 
ct.read_store(slot) | int | Read the value in slot slot (0–15). | 
ct.write_store(slot, value) | None | Write value to slot slot (0–15). | 

```
# Read what last turn's bots wrote
attack_x = ct.read_store(0)
attack_y = ct.read_store(1)

# Write a new value for next turn
ct.write_store(0, target.x)
ct.write_store(1, target.y)
```

### Slots

There are 16 slots, indexed 0 to 15. All values start at 0 and accept any non-negative integer. Reading slot 16 or above raises an error.

### Timing: writes are buffered

Writes are not applied immediately. They are committed at the end of the round, and the new values become readable for all your bots in the next round.

Round | Event | 
N | Bot A calls write_store(0, 42) | 
N | Bot B calls read_store(0) → still reads 0 (last round's value) | 
N+1 | Bot B calls read_store(0) → now reads 42 | 

This means every bot sees a consistent snapshot of the store for the entire round, regardless of execution order. Design your communication protocol around this one-round delay.

### Team isolation

Each team has its own store. Your writes are invisible to the opponent, and you cannot read theirs.

### Usage patterns

### Scouting target

Designate fixed slots for a shared attack target:

```
# Any bot that finds the enemy core sets slots 0 and 1
if found_enemy_core:
    ct.write_store(0, enemy_pos.x)
    ct.write_store(1, enemy_pos.y)

# All bots read the target at the start of run()
target_x = ct.read_store(0)
target_y = ct.read_store(1)
if target_x > 0 and target_y > 0:
    move_toward(ct, Position(target_x, target_y))
```

### Unit census

Count units by type to decide when to expand:

```
# Each Builder Bot increments a counter
current = ct.read_store(2)
ct.write_store(2, current + 1)  # buffered, so safe from race conditions
```

Because writes are buffered you need to be careful: read_store(2) + 1 reads the last round's total, so you're incrementing from the previous turn's count. This is consistent and race-free — just account for the lag.

### Status flags

Use individual slots as boolean flags:

```
SLOT_UNDER_ATTACK = 3

if enemy_nearby:
    ct.write_store(SLOT_UNDER_ATTACK, 1)

if ct.read_store(SLOT_UNDER_ATTACK) == 1:
    # enter defensive mode
    pass
```

### Tips

- Assign slot numbers as named constants at the top of your file to avoid magic numbers

- The one-round delay is a feature, not a bug — it guarantees every bot sees the same store state throughout a round

- There is no lock or mutex; the buffered write model makes concurrent updates safe by design



=== docs/robot-api ===
### Controller API Reference

The Controller object (ct) is passed to your run() method every round. All game interactions go through it.

### Movement

Method | Returns | Description | 
ct.move(direction) | None | Move one tile in the given direction. Builder Bots may only move in a cardinal direction (N/S/E/W); a diagonal direction raises. Raises on any failure. | 
ct.can_move(direction) | bool | True if the tile is passable and unoccupied. Always False for a diagonal direction. | 

Compass convention: (0, 0) is the map's northwest corner — x increases eastward, y increases southward, so NORTH is (0, −1), toward row 0. In the visualiser's isometric view north renders up-right on screen (straight up in the square view); the corner compass always shows the current orientation.

Builder Bots move only in the four cardinal directions: NORTH, SOUTH, EAST, WEST. Passing a diagonal (NORTHEAST, NORTHWEST, SOUTHEAST, SOUTHWEST) to ct.move() raises a GameError, and ct.can_move() returns False for it. To turn a target into a legal move, use pos.cardinal_direction_to(target), which always returns a cardinal step (or CENTRE if already there). Diagonal directions remain valid for turret facing and building orientation.

```
from fcode import Direction

# Step toward a target using a legal cardinal direction.
move_dir = ct.get_position().cardinal_direction_to(target)
if move_dir != Direction.CENTRE and ct.can_move(move_dir):
    ct.move(move_dir)
```

### Building & Construction

Builder Bots can construct buildings on an orthogonally adjacent tile — NORTH, SOUTH, EAST, or WEST of the bot's current position. Diagonal tiles and its own tile are not valid build targets. ct.destroy() follows the same orthogonal-adjacency rule. All build methods raise if the build is not possible.

Method | Returns | Description | 
ct.spawn_builder(pos) | int (unit id) | Spawn a Builder Bot at pos (Core only). | 
ct.can_spawn(pos) | bool | True if Core can spawn a bot at pos. | 
ct.build_harvester(pos) | None | Build a Harvester on an orthogonally adjacent ore tile. | 
ct.can_build_harvester(pos) | bool | Check if Harvester can be built. | 
ct.build_conveyor(pos, direction) | None | Build a conveyor in the given direction. | 
ct.can_build_conveyor(pos, direction) | bool | Check if a conveyor can be built. | 
ct.build_splitter(pos, direction) | None | Build a Splitter facing direction (accepts only from the back). | 
ct.can_build_splitter(pos, direction) | bool | Check if a Splitter can be built. | 
ct.build_barrier(pos) | None | Build a Barrier (no facing direction). | 
ct.can_build_barrier(pos) | bool | Check if a Barrier can be built. | 
ct.build_gunner(pos, direction) | None | Build a Gunner turret facing direction. | 
ct.can_build_gunner(pos, direction) | bool | Check if a Gunner can be built. | 
ct.build_sentinel(pos, direction) | None | Build a Sentinel turret. | 
ct.can_build_sentinel(pos, direction) | bool | Check if a Sentinel can be built. | 
ct.build_launcher(pos) | None | Build a Launcher turret (no facing direction). | 
ct.can_build_launcher(pos) | bool | Check if a Launcher can be built. | 
ct.destroy(pos) | None | Destroy the allied building at pos (orthogonally adjacent). | 
ct.can_destroy(pos) | bool | Check if the building at pos can be destroyed. | 
ct.build(entity_type, pos, extra=None) | None | Generic build. extra is a Direction, required for conveyor/splitter/gunner/sentinel, unused otherwise. | 
ct.can_build(entity_type, pos, extra=None) | bool | Generic legality check for the above. | 

### Combat

Method | Returns | Description | 
ct.fire(target) | None | Fire at target position (turrets only). Gunners and Sentinels spend from your team's global ammunition balance (4 and 10 per shot respectively); Launchers use no ammo. | 
ct.can_fire(target) | bool | Check if this unit can fire at target (including having enough global ammunition). | 
ct.can_fire_from(pos, direction, turret_type, target) | bool | Hypothetical version of can_fire: whether a turret of turret_type (EntityType.GUNNER, SENTINEL, or LAUNCHER) at pos facing direction could hit target. Uses current map occupancy/walls but ignores ammo and cooldown. | 
ct.get_attackable_tiles() | list[Position] | List of tiles this unit can currently attack (raw pattern — ignores ammo, cooldown, and occupancy). Raises if this unit is not a turret. | 
ct.get_attackable_tiles_from(pos, direction, turret_type) | list[Position] | Hypothetical version of get_attackable_tiles for a turret of turret_type at pos facing direction. Launchers ignore direction. | 
ct.get_gunner_target() | Position | None | Closest targetable tile in a Gunner's facing line, or None if nothing is in range. Gunner only — raises on any other unit. | 
ct.heal(pos) | None | Heal all friendly entities (building and/or Builder Bot) on pos by 4 HP for 1 Ti. | 
ct.can_heal(pos) | bool | Check if healing is possible. | 
ct.self_destruct() | None | Destroy this Builder Bot. Deals zero damage — not a weapon. | 
ct.rotate(direction) | None | Rotate a Gunner to face direction (10 Ti, 1-round cooldown). Gunner only — errors on any other unit. | 
ct.can_rotate(direction) | bool | Check if rotation is possible (Gunner only). | 
ct.can_launch(bot_pos, target) | bool | Check if this Launcher can pick up the bot at bot_pos (either team; must be adjacent, incl. diagonal) and throw it to target (within throw range, bot-passable). | 
ct.launch(bot_pos, target) | None | Pick up the Builder Bot at bot_pos (either team) and throw it to target (Launcher only). | 

### Vision & Sensing

Method | Returns | Description | 
ct.get_nearby_tiles(dist_sq=None) | list[Position] | Tiles within vision (or dist_sq if specified). | 
ct.get_nearby_entities(dist_sq=None) | list[int] | IDs of entities within range. | 
ct.get_nearby_buildings(dist_sq=None) | list[int] | IDs of buildings within range. | 
ct.get_nearby_units(dist_sq=None) | list[int] | IDs of mobile units within range. | 
ct.is_in_vision(pos) | bool | True if pos is within this unit's vision radius. | 
ct.get_tile_env(pos) | Environment | Environment type of a tile (EMPTY, WALL, ORE_TITANIUM). | 
ct.get_tile_building_id(pos) | int | None | ID of the building at pos, or None. | 
ct.get_tile_builder_bot_id(pos) | int | None | ID of the Builder Bot at pos, or None. | 
ct.is_tile_empty(pos) | bool | True if no unit or building occupies pos. | 
ct.is_tile_passable(pos) | bool | True if a Builder Bot can stand on pos. | 
ct.get_stored_resource(id=None) | ResourceType | None | Resource type held by a conveyor or splitter (this unit or id), or None if empty. Raises if the entity has no storage. | 
ct.get_stored_resource_id(id=None) | int | None | ID of the resource stack held by a conveyor or splitter (distinct from entity IDs), or None if empty. Raises if the entity has no storage. | 

### Unit Information

Method | Returns | Description | 
ct.get_position(id=None) | Position | Position of this unit (or id if given). | 
ct.get_entity_type(id=None) | EntityType | Type of this unit (or id if given). | 
ct.get_hp(id=None) | int | Current HP of this unit (or id). | 
ct.get_max_hp(id=None) | int | Maximum HP. | 
ct.get_direction(id=None) | Direction | Facing direction (turrets). | 
ct.get_id() | int | This unit's ID. | 
ct.get_team(id=None) | Team | Team of this unit (or id). | 
ct.get_vision_radius_sq(id=None) | int | Vision radius squared. | 
ct.get_action_cooldown() | int | Rounds until this unit can act again. | 
ct.get_move_cooldown() | int | Rounds until this unit can move again. | 
ct.can_act() | bool | True if the action cooldown is clear. | 
ct.get_unit_count() | int | Total number of your team's units. | 

For Builder Bots, acting and moving are mutually exclusive per round — a successful build/attack/heal blocks that round's move (and vice versa), so get_action_cooldown() and get_move_cooldown() reflect only their own trigger even though can_move()/can_build_*()/can_fire()/can_heal() already account for both. If can_move() returns False, use ct.can_act() to check directly whether that's because your last action locked movement this round, rather than inferring it from get_action_cooldown() > 0.

### Communication Store

Each team has 16 private integer slots shared by all of its units.

Method | Returns | Description | 
ct.read_store(index) | int | Read the value at index (0–15) from your team's store, as of the start of this round. | 
ct.write_store(index, value) | None | Buffer a write of value to index (0–15). Takes effect at the start of next round, visible to all units. | 

### Resources & Economy

Method | Returns | Description | 
ct.get_global_resources() | int | Current titanium balance for your team. | 
ct.get_global_ammo() | int | Current ammunition balance for your team. Teams start with 0 ammo and there is no passive ammo income. | 
ct.convert_ammo(amount) | None | Convert amount global titanium into amount ammunition (1:1). Core only — at most once per team per turn, usable the same turn, and does not use the Core's action cooldown. | 
ct.can_convert_ammo(amount) | bool | Check if the Core can convert amount titanium into ammunition this turn. | 
ct.get_scale_percent() | float | Current cost scale factor (increases as your team builds entities, not over time). | 
ct.get_builder_bot_cost() | int | Titanium cost to spawn a Builder Bot. | 
ct.get_harvester_cost() | int | Titanium cost to build a Harvester. | 
ct.get_gunner_cost() | int | Titanium cost to build a Gunner. | 
ct.get_sentinel_cost() | int | Titanium cost to build a Sentinel. | 
ct.get_launcher_cost() | int | Titanium cost to build a Launcher. | 
ct.get_conveyor_cost() | int | Titanium cost to build a conveyor. | 
ct.get_splitter_cost() | int | Titanium cost to build a Splitter. | 
ct.get_barrier_cost() | int | Titanium cost to build a Barrier. | 

```
# Core turn: keep ammunition topped up for your turrets.
if ct.get_global_ammo() < 20 and ct.can_convert_ammo(10):
    ct.convert_ammo(10)
```

### Map & Match

Method | Returns | Description | 
ct.get_map_width() | int | Map width in tiles. | 
ct.get_map_height() | int | Map height in tiles. | 
ct.get_current_round() | int | Current round number (0-indexed — 0 on the first round). | 
ct.get_cpu_time_elapsed() | int | Microseconds of CPU time used this turn. | 

### Debugging

Method | Returns | Description | 
ct.draw_indicator_line(pos_a, pos_b, r, g, b) | None | Draw a coloured line in the visualiser. | 
ct.draw_indicator_dot(pos, r, g, b) | None | Draw a coloured dot in the visualiser. | 
ct.resign(message=None) | None | Forfeit the match immediately. |



=== docs/api-types ===
### Types & Enums

All types are importable directly from fcode:

```
from fcode import Controller, Team, EntityType, Environment, Direction, Position, GameError
```

### Team

Identifies which side a unit belongs to.

Value | Description | 
Team.A | Team A | 
Team.B | Team B | 

```
if ct.get_team() == Team.A:
    # we are team A
```

### EntityType

The type of a unit or building.

Value | Category | Description | 
CORE | Base | Team base unit | 
BUILDER_BOT | Mobile | Mobile worker | 
GUNNER | Turret | Forward-ray turret | 
SENTINEL | Turret | Long-range line turret | 
LAUNCHER | Turret | Bot-throwing utility turret | 
HARVESTER | Building | Generates titanium from ore tiles | 
CONVEYOR | Building | Basic resource conveyor | 
SPLITTER | Building | Rotates resource flow between 3 outputs | 
BARRIER | Building | Blocks movement and LOS | 

```
etype = ct.get_entity_type()
if etype == EntityType.GUNNER:
    # handle as a turret
```

### Environment

The terrain type of a tile, returned by ct.get_tile_env().

Value | Description | 
Environment.EMPTY | Traversable ground | 
Environment.WALL | Impassable wall | 
Environment.ORE_TITANIUM | Titanium ore deposit (passable, Harvester-buildable) | 

### Direction

The 8 compass directions plus centre. Used for movement, building, and turret orientation.

Builder Bot movement is cardinal-only. A Builder Bot may only ct.move() in a cardinal direction — NORTH, SOUTH, EAST, or WEST. The four diagonals (NORTHEAST, NORTHWEST, SOUTHEAST, SOUTHWEST) are still valid values, and remain usable for turret facing and building orientation, but passing one to ct.move() raises a GameError (and ct.can_move() returns False). Use Direction.is_cardinal() to test a direction, or Position.cardinal_direction_to() to pick a legal move.

Value | Description | 
Direction.NORTH | Up | 
Direction.SOUTH | Down | 
Direction.EAST | Right | 
Direction.WEST | Left | 
Direction.NORTHEAST | Up-right | 
Direction.NORTHWEST | Up-left | 
Direction.SOUTHEAST | Down-right | 
Direction.SOUTHWEST | Down-left | 
Direction.CENTRE | No movement (current tile) | 

Method | Returns | Description | 
direction.is_cardinal() | bool | True only for NORTH, SOUTH, EAST, WEST (a legal Builder Bot move). | 

### Position

A 2D grid coordinate.

```
pos = Position(x=3, y=7)
```

Attribute / Method | Returns | Description | 
pos.x | int | Column (0-indexed from left) | 
pos.y | int | Row (0-indexed from top) | 
pos.add(direction) | Position | Returns the adjacent position in direction. | 
pos.distance_squared(other) | int | Squared Euclidean distance to other. Avoids floating point. | 
pos.direction_to(other) | Direction | The direction from pos toward other. May be a diagonal, so it is not always a legal Builder Bot move. | 
pos.cardinal_direction_to(other) | Direction | A legal cardinal step from pos toward other (or CENTRE if already there). Prefer this for choosing a move. | 

```
my_pos = ct.get_position()
target = Position(10, 5)
dist_sq = my_pos.distance_squared(target)         # e.g. 50
dir_to = my_pos.direction_to(target)              # e.g. Direction.NORTHEAST (may be diagonal)
move_dir = my_pos.cardinal_direction_to(target)   # e.g. Direction.NORTH (always a legal move)
```

### GameError

Raised when an action is not valid (e.g. moving into a wall, building without sufficient titanium).

```
from fcode import GameError

try:
    ct.move(Direction.NORTH)
except GameError as e:
    # handle gracefully
    pass
```

Prefer using can_* checks before acting to avoid catching exceptions in the hot path.

Letting an exception escape run() uncaught is fatal to the unit. This applies to GameError and any other exception. Unlike a CPU-time interruption — which just skips that unit's turn and calls run() again fresh next round (see CPU time limit) — an uncaught exception permanently destroys the unit. It will never run again for the rest of the match.



=== docs/platform-matches ===
### Matches & Scheduling

### Series structure

Each ladder match is a best-of-five series. The two bots play five individual games; the team that wins three or more games wins the series. Series results (not individual game results) affect ladder ratings.

All five games in a series are played to completion regardless of the intermediate score — there are no early series terminations.

### Map selection

Maps for each series are drawn at random from the current competition map pool. Different games in the same series may use different maps. The map pool is announced at the start of the competition and may be updated between rounds.

The current map pool is listed on the Maps page, with each map's dimensions and symmetry. Download them into your project with fcode maps sync.

### Remote infrastructure

Ladder matches and remote test matches (fcode match test) run on AWS Graviton3 instances. This is the same hardware used for all ranked games, so performance measured in remote tests is representative of what you will see on the ladder.

Local matches (fcode run) run on your own machine and may differ in speed — always profile CPU usage on remote tests before submitting.

### Replays

Every game produces a .replay26 replay file. Replays for all your games are available on the Matches page. Open one directly from the platform with:

```
fcode watch --match <match-id>
```

or download the file and open it locally with fcode watch <file>.replay26.

Replays include the full round-by-round state of the map, unit HP, resource counts, and any indicator overlays (ct.draw_indicator_line / ct.draw_indicator_dot) your bot drew.

### Scheduling

The scheduler runs every 10 minutes. Your bot is automatically paired after submission — you do not need to initiate matches manually. The first match after a new submission may take up to 10 minutes to appear.



=== docs/platform-ladder ===
### Ladder & Rating

### Elo rating

Every team has a ladder rating, starting at 1500. After each rated series, both teams' ratings are updated using the Elo rating system with a fixed K-factor of 32.

Unlike a simple win/loss Elo, the outcome fed into the formula is the fractional series score rather than just who won: a 3-2 series counts as an outcome of 0.6, not a full win, while a 5-0 sweep counts as a full 1.0. This means dominant series move your rating more than narrow ones.

```
expectedA = 1 / (1 + 10^((ratingB - ratingA) / 400))
outcome   = scoreA / (scoreA + scoreB)   // e.g. 3-2 → 0.6
delta     = 32 * (outcome - expectedA)
```

### What affects rating

- Ladder matches — the automatic best-of-five series the scheduler pairs you into (see Matches & Scheduling) — are rated and update both teams' Elo.

- Unrated challenges (fcode match unrated) and remote test matches (fcode match test) never affect rating — they exist purely for testing against real hardware.

### Rating history and rank

Every rated match records a snapshot of each team's rating and leaderboard rank at that point in time, which powers the rating-over-time graphs on the platform. Rank is simply your position when all teams are sorted by current rating, recomputed after every rated match.

### Climbing badge

Teams that have played at least 100 matches and gained 100+ rating points within the last 6 hours are shown with a "climbing" badge on the leaderboard for the following hour — a way to highlight teams on a hot streak.



=== docs/platform-submitting ===
### Submitting Your Bot

### Two ways to submit

- CLI: fcode submit <path> — accepts a bot directory, a single .py file, or a .zip archive. See Submitting (CLI) and the CLI reference.

- Web: Open the Submissions page and upload a .zip directly from your browser.

Both paths run the same validation and enter the same ladder queue — there is no difference in how your bot is judged based on which one you use.

### Bot requirements

- Must contain main.py, either at the root of the zip or inside exactly one top-level directory.

- main.py must define a top-level class Player.

- Pure Python only — no native extensions.

### Upload limits

- 5MB max archive size

- 50MB max decompressed size

- 500 max files

- No native extensions (.so, .pyd, .dylib, .dll) — these bypass the sandbox's Python-level restrictions and are rejected outright

- No path traversal (e.g. ../) in archive entry names

### Submission lifecycle

Each upload is validated immediately and moves through these statuses:

Status | Meaning | 
processing | Upload received, validation/audit in progress. | 
ready | Passed validation, available to activate and play ladder matches. | 
flagged | Passed structural validation but held for automated security audit before becoming ready. | 
rejected | Failed the security audit. | 
error | Failed structural validation (bad zip, missing main.py, over a limit, etc.) — see the error message for the specific cause. | 

### Versions and the active submission

Every upload gets an incrementing version number. You can submit as often as you like — there's no limit on the number of submissions, and old versions are kept.

Only one version is active at a time, and only your active submission plays ladder matches. Set the active version with fcode submission activate VERSION or the Set as Active option on the web Submissions page.

### Submission freezes

Admins can freeze submissions platform-wide (for example, to lock in a snapshot before a tournament's qualifier round). While frozen, uploads and active-submission changes are disabled; the Submissions page shows a banner when this is in effect.



=== docs/cli-reference ===
### CLI Reference

### Global flags

Flag | Description | 
--version | Print the installed fcode version and exit. | 
--help | Show help for the command or subcommand. | 

### fcode login

Authenticate the CLI with your Florent Code League account.

```
fcode login
```

Opens a browser window for OAuth approval. Credentials are stored in ~/.fcode/credentials.json.

### fcode logout

Remove stored credentials.

```
fcode logout
```

### fcode starter

Scaffold a new project in the current directory: an fcode.toml, a .gitignore, bots/ and maps/ folders, and a starter bot at bots/starter/main.py. If you are logged in, the current map pool is downloaded into maps/.

```
fcode starter
```

### fcode maps

List and download the competition map pool. Maps are not bundled with the CLI — the pool is set on the platform and can change during the competition.

```
fcode maps list   # pool contents, and whether each map is present locally
fcode maps sync   # download anything missing or out of date into maps/
```

sync only adds and updates. A map dropped from the pool stays on disk, so you keep practising against it.

### fcode run

Run a local match between two bots.

```
fcode run BOT_A BOT_B [MAP] [--replay FILE] [--seed N] [--watch] [--map-random] [--tle MS]
```

Argument / Flag | Default | Description | 
BOT_A | — | First bot — a path, or a name resolved against your bots/ folder. | 
BOT_B | — | Second bot. Pass the same value as BOT_A for a mirror match. | 
MAP | first map | Optional map — a path or a name resolved against your maps/ folder. Omitted uses the first map in maps/. | 
--replay FILE | replay.replay26 | Path for the output replay file (default from fcode.toml). | 
--seed N | from config | Deterministic match seed. | 
--watch | off | Open the visualiser automatically when the match finishes. | 
--map-random | off | Pick a random map from maps/ when no map is given. | 
--tle MS | 0 (disabled) | Enforce a per-turn CPU time limit locally, in milliseconds. The ladder server always enforces 10 ms; local runs don't unless you pass this. | 

### fcode watch

Open a replay in the browser-based visualiser.

```
fcode watch REPLAY
fcode watch --match MATCH_ID [--game N]
```

Argument / Flag | Description | 
REPLAY | Path to a local .replay26 replay file. | 
--match MATCH_ID | Open a match's replay from the platform instead of a local file. | 
--game N | Game number within the match (for --match). | 

### fcode map-editor

Open the map editor to create or edit .map26 files.

```
fcode map-editor
fcode map-editor --platform
```

Flag | Description | 
--platform | Open the map editor on the platform in your browser instead of running it locally. | 

### fcode submit

Submit a bot to the ladder. Shorthand for fcode submission upload.

```
fcode submit PATH [--name NAME]
```

Argument / Flag | Description | 
PATH | A bot directory (containing main.py), a .py file, or a .zip archive. | 
--name, -n NAME | Optional name for this submission. | 

### fcode submission

Manage bot submissions: upload, list, activate, rename, and download.

### submission upload

```
fcode submission upload PATH [--name NAME]
```

Argument / Flag | Description | 
PATH | A bot directory (containing main.py), a .py file, or a .zip archive. | 
--name, -n NAME | Optional name for this submission. | 

Identical to fcode submit.

### submission list

```
fcode submission list
```

Lists all of your team's submissions with version, name, status, and which one is active.

### submission activate

```
fcode submission activate VERSION
```

Argument | Description | 
VERSION | Version number of the submission to make active on the ladder. | 

### submission rename

```
fcode submission rename VERSION NAME
```

Argument | Description | 
VERSION | Version number of the submission to rename. | 
NAME | New name for the submission. | 

### submission download

```
fcode submission download [VERSION] [--output FILE]
```

Argument / Flag | Default | Description | 
VERSION | active/ready submission | Version number to download. Omitted downloads your currently active (or most recent ready) submission. | 
--output, -o FILE | v<VERSION>.zip | Output file path for the downloaded archive. | 

### fcode match

View, list, and manage matches. Running fcode match MATCH_ID without naming a subcommand is shorthand for fcode match info MATCH_ID.

### match info

```
fcode match info MATCH_ID
```

Shows detailed match info: status, teams, score, rating changes, and a per-game breakdown.

### match list

```
fcode match list [--type ladder|unrated] [--team TEAM] [--mine] [--limit N] [--cursor CURSOR]
```

Flag | Default | Description | 
--type ladder|unrated | all types | Filter by match type. | 
--team TEAM | — | Filter by team name or team ID. | 
--mine | off | Show only your own team's matches. | 
--limit N | 20 | Number of matches to show (max 100). | 
--cursor CURSOR | — | Pagination cursor from a previous page. | 

### match unrated

```
fcode match unrated OPPONENT_ID [--match SOURCE_MATCH_ID] [--map MAP_NAME]
```

Argument / Flag | Description | 
OPPONENT_ID | Team ID to request an unrated match against. | 
--match SOURCE_MATCH_ID | Use the opponent's submission from this specific match instead of their currently active one. | 
--map MAP_NAME | Map to play (repeatable, up to 5). Omitted picks random maps. | 

Requests a friendly, non-rated match against another team using your currently active submission.

### match test

Run a remote test match between two local bots on the server, with time-limit enforcement.

```
fcode match test BOT_A BOT_B [MAPS...]
```

Argument | Description | 
BOT_A, BOT_B | Each is a directory (containing main.py), a .py file, or a .zip. | 
MAPS... | Optional map names, one per game. Omitted runs 5 random maps. | 

Rate limit: 5 matches per 10 minutes per account.

### match replay

```
fcode match replay MATCH_ID [--game N] [--output FILE]
```

Argument / Flag | Default | Description | 
MATCH_ID | — | Match to download replays from. | 
--game, -g N | all games | Game number (1-5) to download. Omitted downloads all games in the match. | 
--output, -o FILE | <matchId>_game_<N>.replay26 | Output file path. | 

### match watch

```
fcode match watch MATCH_ID [--game N]
```

Argument / Flag | Description | 
MATCH_ID | Match to open in the browser-based visualiser. | 
--game, -g N | Game number within the match. | 

Shorthand for fcode watch --match MATCH_ID [--game N].

### match tests

```
fcode match tests [--limit N]
```

Flag | Default | Description | 
--limit N | 20 | Number of test runs to show. | 

Lists your recent fcode match test runs.

### fcode team

Search teams and view team profiles.

### team search

```
fcode team search QUERY
```

Argument | Description | 
QUERY | Search text matched against team names. | 

### team info

```
fcode team info TEAM_ID
```

Argument | Description | 
TEAM_ID | Team to show — name, rating, match count, and members. | 

### fcode ladder

Show the ladder rankings.

```
fcode ladder [--limit N] [--around]
```

Flag | Default | Description | 
--limit N | 20 | Number of teams to show. | 
--around | off | Center the list on your own team's rank (±5), instead of starting from the top. | 

### fcode status

Show your current ladder rating, rank, active submission, and recent match record.

```
fcode status
```



=== docs/cli-submitting ===
### Submitting

### Submit your bot

```
fcode submit bot.py
```

Your submission is uploaded, validated, and entered into the ladder queue. The CLI prints a submission ID when the upload succeeds.

You can submit at any time — there is no limit on the number of submissions. See Submitting Your Bot for upload limits, validation rules, and how submission versions/activation work.

Manage past submissions with fcode submission list, fcode submission activate VERSION, fcode submission rename VERSION NAME, and fcode submission download VERSION — see the CLI reference for details.

### Submitting a multi-file bot

If your bot spans multiple files, collect them into a zip archive first:

```
zip bot.zip bot.py utils.py strategy.py
fcode submit bot.zip
```

The engine runs bot.py as the entry point. All files in the archive are available to import at runtime.

### After you submit

Your bot is automatically paired against other submitted bots — see Matches & Scheduling for how pairing, series, and scoring work. Track results on the Matches page.

### Troubleshooting

Problem | Cause | Fix | 
ValidationError: entry point not found | No bot.py in the archive | Ensure the root of the zip contains bot.py | 
SyntaxError on submission | Python version mismatch | Verify you are using Python 3.12 or 3.13 | 
Bot disqualified mid-match | CPU time exceeded 10 ms | Profile with ct.get_cpu_time_elapsed() and optimise | 
Upload rejected (size / file count / native extension) | Archive fails platform validation | See Upload limits |