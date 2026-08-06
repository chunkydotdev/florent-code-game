


=== tutorials/movement-sensing/01-welcome ===
· Step 1 of 5

### Welcome & the run() loop

Every bot in Florent Code League is a single Python class: Player. The engine creates one Player instance per unit on your team, and calls its run() method once per round for that unit. Whatever run() does — or doesn't do — is that unit's entire turn.

```
from fcode import Controller, EntityType


class Player:
    def run(self, ct: Controller) -> None:
        etype = ct.get_entity_type()
        if etype == EntityType.CORE:
            pass
```

The ct argument (short for "controller") is your only way to interact with the game — move, build, sense the map, read resources, all of it goes through ct. Since a Core, a Builder Bot, and a Gunner all share the same run() method, the first thing every bot does is check ct.get_entity_type() and branch based on what kind of unit is currently running. Right now we only handle EntityType.CORE, and it does nothing (pass) — this is the smallest bot that's valid Python and won't crash.

### Try it

If you haven't already, install the CLI and scaffold a project:

```
pip install fcode
fcode login
fcode starter
```

Copy the code above into bots/starter/main.py, replacing its contents, then run a mirror match and watch the replay:

```
fcode run starter starter
fcode watch replay.replay26
```

What you should see: two idle Cores sitting on the map for all 1000 rounds. Nothing moves — that's expected, we haven't told anything to happen yet. The match will end in a coin-flip tiebreak, since neither side does anything.

Next: give the Core something to do — spawn a Builder Bot.
Spawning a Builder Bot



=== tutorials/movement-sensing/02-spawning ===
· Step 2 of 5

### Spawning a Builder Bot

The Core is stationary — it can't move or attack. Its one job is spawning Builder Bots, your mobile workforce. Spawning costs titanium and only works on a tile within the Core's spawn range.

```
from fcode import Controller, EntityType


class Player:
    def run(self, ct: Controller) -> None:
        etype = ct.get_entity_type()
        if etype == EntityType.CORE:
            for pos in ct.get_nearby_tiles(dist_sq=2):
                if ct.can_spawn(pos):
                    ct.spawn_builder(pos)
                    break
```

ct.get_nearby_tiles(dist_sq=2) returns every tile within squared-distance 2 of the Core — that's exactly the Core's spawn range: the ring of tiles orthogonally or diagonally adjacent to its 2×2 footprint. We loop over those candidate tiles, and for each one ask ct.can_spawn(pos): is it empty, in range, and can we afford a Builder Bot right now? The first tile that passes gets ct.spawn_builder(pos), and we break so we only spawn one bot per round.

Almost every build action in the game follows this same can_X() / X() pairing — check first, then act. The can_* checks never raise; the action methods (spawn_builder, move, build_harvester, ...) raise a GameError if you call them somewhere illegal, so checking first keeps your bot from crashing mid-match.

### Try it

Replace bots/starter/main.py with the code above, then:

```
fcode run starter starter
fcode watch replay.replay26
```

What you should see: a Builder Bot appears next to each Core in round 1 and just sits there (we haven't given it a run() branch yet, so it does nothing). The unit count in the match summary should read 1 or more per side.

Next: make that Builder Bot actually move.
Welcome & the run() loopMoving your Builder Bot



=== tutorials/movement-sensing/03-moving ===
· Step 3 of 5

### Moving your Builder Bot

Builder Bots are the only unit that can move, and they move only in the four cardinal directions — Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST. (The Direction enum still lists all 8 compass points plus Direction.CENTRE, but diagonals aren't legal moves: ct.move() with a diagonal raises a GameError, and ct.can_move() returns False. Diagonals stay valid elsewhere, e.g. turret facing.) Movement follows the same check-then-act pattern as spawning.

```
from fcode import Controller, Direction, EntityType

CARDINALS = [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]


class Player:
    def run(self, ct: Controller) -> None:
        etype = ct.get_entity_type()
        if etype == EntityType.CORE:
            for pos in ct.get_nearby_tiles(dist_sq=2):
                if ct.can_spawn(pos):
                    ct.spawn_builder(pos)
                    break
        elif etype == EntityType.BUILDER_BOT:
            direction = random.choice(CARDINALS)
            if ct.can_move(direction):
                ct.move(direction)
```

CARDINALS is the four legal move directions — a handy constant you'll reuse throughout these tutorials. Each round, our Builder Bot picks a random cardinal direction and moves there if ct.can_move() says it's legal (not a wall, not occupied, and not a diagonal). Movement puts the unit on a 1-round cooldown, so a bot can only move once every round at most — no double-stepping.

Once you start building/attacking/healing in later tutorials, ct.can_move() can also return False for a different reason: acting and moving are mutually exclusive per round for Builder Bots. If a move you expected to be legal is rejected, check ct.can_act() — if it's False, you're act-locked from a previous action this round, not blocked by terrain or another unit.

This is a genuinely bad movement strategy — the bot has no memory and no goal, so it'll wander in place as often as it makes progress. That's fine for now; the point is confirming movement works before we add any intelligence.

### Try it

```
fcode run starter starter
fcode watch replay.replay26
```

What you should see: the Builder Bot visibly wanders around the map instead of standing still. Scrub through the replay — you should see it occasionally get stuck against a wall (that round it just won't move, since can_move returned False in the direction it picked).

Next: use what the bot can see to move somewhere purposeful, instead of randomly.
Spawning a Builder BotSensing the map



=== tutorials/movement-sensing/04-sensing ===
· Step 4 of 5

### Sensing the map

Every unit has a vision radius, and ct.get_nearby_tiles() returns the tiles inside it. For each tile you can ask ct.get_tile_env(pos), which returns one of three Environment values: EMPTY (plain traversable ground), WALL (impassable), or ORE_TITANIUM (an ore deposit — also traversable, and buildable on, which matters starting next tutorial).

We'll use that to steer away from walls instead of bumping into them at random, and introduce two debugging tools along the way: print() (captured per-round and shown in the visualiser) and ct.draw_indicator_dot() (draws a coloured dot on the map, saved into the replay).

```
import random

from fcode import Controller, Direction, Environment, EntityType

# Builder bots move only in the four cardinal directions.
CARDINALS = [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]


class Player:
    def run(self, ct: Controller) -> None:
        etype = ct.get_entity_type()
        if etype == EntityType.CORE:
            for pos in ct.get_nearby_tiles(dist_sq=2):
                if ct.can_spawn(pos):
                    ct.spawn_builder(pos)
                    break
        elif etype == EntityType.BUILDER_BOT:
            self._run_builder(ct)

    def _run_builder(self, ct: Controller) -> None:
        pos = ct.get_position()
        ct.draw_indicator_dot(pos, 0, 255, 0)

        open_dirs = [
            d for d in CARDINALS
            if ct.can_move(d) and ct.get_tile_env(pos.add(d)) == Environment.EMPTY
        ]
        move_options = open_dirs or [d for d in CARDINALS if ct.can_move(d)]
        if move_options:
            direction = random.choice(move_options)
            ct.move(direction)
            print(f"round {ct.get_current_round()}: moved {direction.name} to {ct.get_position()}")
```

We moved the Builder Bot's logic into its own _run_builder method to keep run() readable — a pattern you'll want as your bot grows. pos.add(direction) returns the position one step in that direction without actually moving, which lets us peek at a tile's environment before committing. We build a list of directions that are both legal (can_move) and lead to plain ground (Environment.EMPTY), preferring those; if none qualify (e.g. surrounded by ore or a dead end) we fall back to any legal move so the bot never just stops.

### Try it

```
fcode run starter starter
fcode watch replay.replay26
```

What you should see: a green dot following the Builder Bot every round, and if your visualiser build supports it, a per-round log line in the replay's debug output showing the direction it chose. The bot should look slightly less erratic than in the previous step, since it's now actively avoiding walking in place against obstacles.

Next: recap, and a look at what's coming.
Moving your Builder BotRecap & checkpoint



=== tutorials/movement-sensing/05-recap ===
· Step 5 of 5

### Recap & checkpoint

You now have a bot that:

- Dispatches on ct.get_entity_type() to handle each unit type separately

- Spawns a Builder Bot from the Core within its spawn range (ct.get_nearby_tiles(dist_sq=2), ct.can_spawn, ct.spawn_builder)

- Moves that Builder Bot around with Direction, ct.can_move, ct.move

- Reads the map with ct.get_tile_env() to avoid walls and prefer open ground

- Debugs itself with print() and ct.draw_indicator_dot()

Every mechanic here — the run() dispatch pattern, the can_X() / X() check-then-act convention, and vision-based sensing — is used identically everywhere else in the game. Turrets, harvesters, and conveyors all build on exactly this foundation.

The bot from step 4 is your starting point for the next tutorial. Keep it around — you'll extend _run_builder rather than starting from scratch.

Next up: Harvesting Titanium — put that wandering Builder Bot to work mining ore and growing your economy.
Sensing the mapFinish & start Harvesting Titanium



=== tutorials/harvesting-titanium/01-the-titanium-economy ===
· Step 1 of 5

### The titanium economy

Titanium is the only resource in Florent Code League. It's a single shared balance per team — every build and spawn action draws from the same pool, and every unit can read it with ct.get_global_resources().

```
import random

from fcode import Controller, Direction, Environment, EntityType

CARDINALS = [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]


class Player:
    def run(self, ct: Controller) -> None:
        etype = ct.get_entity_type()
        if etype == EntityType.CORE:
            self._run_core(ct)
        elif etype == EntityType.BUILDER_BOT:
            self._run_builder(ct)

    def _run_core(self, ct: Controller) -> None:
        titanium = ct.get_global_resources()
        if ct.get_current_round() % 50 == 0:
            print(f"round {ct.get_current_round()}: {titanium} titanium")

        for pos in ct.get_nearby_tiles(dist_sq=2):
            if ct.can_spawn(pos):
                ct.spawn_builder(pos)
                break

    def _run_builder(self, ct: Controller) -> None:
        pos = ct.get_position()
        open_dirs = [
            d for d in CARDINALS
            if ct.can_move(d) and ct.get_tile_env(pos.add(d)) == Environment.EMPTY
        ]
        move_options = open_dirs or [d for d in CARDINALS if ct.can_move(d)]
        if move_options:
            ct.move(random.choice(move_options))
```

This is your Tutorial 1 bot, unchanged apart from the Core printing its balance every 50 rounds. ct.get_global_resources() returns a plain int — your team's current titanium balance. Every cost-related method in the API returns the same kind of plain int; you'll see one in a moment.

Every team also gets passive income: 10 titanium every 4 rounds, regardless of anything you build. It's small, but it means titanium always ticks upward even if your economy does nothing — which is exactly what you'll see in this step, since we haven't built a Harvester yet.

### Try it

```
fcode run starter starter
fcode watch replay.replay26
```

What you should see: the printed balance climbing slowly and steadily — roughly +10 every 4 rounds, minus whatever the Core is spending to spawn Builder Bots. That slow climb is pure passive income.

Next: find some ore.
Finding ore



=== tutorials/harvesting-titanium/02-finding-ore ===
· Step 2 of 5

### Finding ore

Ore tiles show up as Environment.ORE_TITANIUM when you sense them — the same ct.get_tile_env() call from Tutorial 1, just checking for a different value. Let's make the Builder Bot beeline for the nearest one it can see, instead of wandering randomly once ore is in view.

```
import random

from fcode import Controller, Direction, Environment, EntityType

CARDINALS = [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]


class Player:
    def run(self, ct: Controller) -> None:
        etype = ct.get_entity_type()
        if etype == EntityType.CORE:
            self._run_core(ct)
        elif etype == EntityType.BUILDER_BOT:
            self._run_builder(ct)

    def _run_core(self, ct: Controller) -> None:
        for pos in ct.get_nearby_tiles(dist_sq=2):
            if ct.can_spawn(pos):
                ct.spawn_builder(pos)
                break

    def _run_builder(self, ct: Controller) -> None:
        pos = ct.get_position()

        ore_tiles = [
            t for t in ct.get_nearby_tiles() if ct.get_tile_env(t) == Environment.ORE_TITANIUM
        ]
        if ore_tiles:
            target = min(ore_tiles, key=lambda t: pos.distance_squared(t))
            direction = pos.cardinal_direction_to(target)
            if ct.can_move(direction):
                ct.move(direction)
                return

        open_dirs = [
            d for d in CARDINALS
            if ct.can_move(d) and ct.get_tile_env(pos.add(d)) == Environment.EMPTY
        ]
        move_options = open_dirs or [d for d in CARDINALS if ct.can_move(d)]
        if move_options:
            ct.move(random.choice(move_options))
```

Two new Position helpers do the heavy lifting: pos.distance_squared(other) picks the closest ore tile out of everything currently visible, and pos.cardinal_direction_to(other) converts "I want to go there" into a legal move — always one of the four cardinal directions. (Its sibling pos.direction_to(other) snaps to the nearest of all 8 compass directions instead — handy for things like turret facings, but not for movement, since diagonal moves aren't legal.) If no ore is visible yet, we fall back to the same explore-and-avoid-walls logic from Tutorial 1.

This is a "greedy nearest" strategy — it only considers ore it can currently see, and re-evaluates every round, so a bot can flip-flop between two similarly-distant ore patches as it moves. That's fine for now.

### Try it

```
fcode run starter starter
fcode watch replay.replay26
```

What you should see: once a Builder Bot's vision touches an ore tile, it should turn and beeline toward it instead of continuing to wander.

Next: actually build a Harvester there.
The titanium economyBuilding a Harvester



=== tutorials/harvesting-titanium/03-building-a-harvester ===
· Step 3 of 5

### Building a Harvester

Once a Builder Bot is orthogonally adjacent to an ore tile — NORTH, SOUTH, EAST, or WEST of its position, never diagonal and never its own tile — it can build a Harvester there with ct.build_harvester(pos).

```
import random

from fcode import Controller, Direction, Environment, EntityType

CARDINALS = [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]


class Player:
    def run(self, ct: Controller) -> None:
        etype = ct.get_entity_type()
        if etype == EntityType.CORE:
            self._run_core(ct)
        elif etype == EntityType.BUILDER_BOT:
            self._run_builder(ct)

    def _run_core(self, ct: Controller) -> None:
        for pos in ct.get_nearby_tiles(dist_sq=2):
            if ct.can_spawn(pos):
                ct.spawn_builder(pos)
                break

    def _run_builder(self, ct: Controller) -> None:
        pos = ct.get_position()

        for d in CARDINALS:
            tile = pos.add(d)
            if ct.get_tile_env(tile) == Environment.ORE_TITANIUM and ct.can_build_harvester(tile):
                ct.build_harvester(tile)
                return

        ore_tiles = [
            t for t in ct.get_nearby_tiles() if ct.get_tile_env(t) == Environment.ORE_TITANIUM
        ]
        if ore_tiles:
            target = min(ore_tiles, key=lambda t: pos.distance_squared(t))
            direction = pos.direction_to(target)
            if ct.can_move(direction):
                ct.move(direction)
                return

        open_dirs = [
            d for d in CARDINALS
            if ct.can_move(d) and ct.get_tile_env(pos.add(d)) == Environment.EMPTY
        ]
        move_options = open_dirs or [d for d in CARDINALS if ct.can_move(d)]
        if move_options:
            ct.move(random.choice(move_options))
```

We check the four orthogonally adjacent tiles first — if one is ore and buildable, build immediately and stop for this round. Otherwise we fall through to the same seek-and-explore logic as before.

### Try it

```
fcode run starter starter
fcode watch replay.replay26
```

Watch the match summary line at the end of fcode run — it prints something like:

```
Titanium     136 (0 mined)    147 (0 mined)
```

That "0 mined" is not a bug — it's the whole point of this step. Your Harvester is built and ready to output a stack every 4 rounds, but that titanium has nowhere to go. A Harvester only feeds the tiles directly next to it, and unless one of those tiles happens to be your Core, it just sits idle — output ready, going nowhere, not actually wasting anything. Nothing in your printed balance will move because of it.

This is by design: harvesting and delivering are two separate problems. Solving delivery — routing a Harvester's output back to your Core — is the entire subject of the next tutorial.

Next: Conveyors, and the cost of not planning your economy layout.
Finding oreCost scaling & early expansion



=== tutorials/harvesting-titanium/04-cost-scaling ===
· Step 4 of 5

### Cost scaling & early expansion

Every build cost scales up as your team builds more entities — not simply because rounds are passing. The scale factor starts at 100% and increases additively each time something is built (and decreases again if it's destroyed); it never moves on its own between builds. ct.get_scale_percent() returns the current factor, and every ct.get_*_cost() method already bakes it in, so you never have to do the multiplication yourself.

```
import random

from fcode import Controller, Direction, Environment, EntityType

CARDINALS = [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]


class Player:
    def run(self, ct: Controller) -> None:
        etype = ct.get_entity_type()
        if etype == EntityType.CORE:
            self._run_core(ct)
        elif etype == EntityType.BUILDER_BOT:
            self._run_builder(ct)

    def _run_core(self, ct: Controller) -> None:
        if ct.get_current_round() % 50 == 0:
            scale = ct.get_scale_percent()
            harvester_cost = ct.get_harvester_cost()
            print(f"round {ct.get_current_round()}: scale {scale:.0f}%, harvester costs {harvester_cost} Ti")

        for pos in ct.get_nearby_tiles(dist_sq=2):
            if ct.can_spawn(pos):
                ct.spawn_builder(pos)
                break

    def _run_builder(self, ct: Controller) -> None:
        pos = ct.get_position()

        for tile in ct.get_nearby_tiles(dist_sq=2):
            if ct.get_tile_env(tile) == Environment.ORE_TITANIUM and ct.can_build_harvester(tile):
                ct.build_harvester(tile)
                return

        ore_tiles = [
            t for t in ct.get_nearby_tiles() if ct.get_tile_env(t) == Environment.ORE_TITANIUM
        ]
        if ore_tiles:
            target = min(ore_tiles, key=lambda t: pos.distance_squared(t))
            direction = pos.direction_to(target)
            if ct.can_move(direction):
                ct.move(direction)
                return

        open_dirs = [
            d for d in CARDINALS
            if ct.can_move(d) and ct.get_tile_env(pos.add(d)) == Environment.EMPTY
        ]
        move_options = open_dirs or [d for d in CARDINALS if ct.can_move(d)]
        if move_options:
            ct.move(random.choice(move_options))
```

Watch the printed cost climb over the match. It isn't climbing because rounds are passing — it's climbing because the Core is still spawning a new Builder Bot every round it can afford one (that loop was there since Tutorial 1), and each spawned bot nudges your team's scale factor up. If the Core ever ran out of titanium and stopped spawning, the printed cost would stop climbing too, no matter how many more rounds went by. As costs rise, the Core will naturally spawn less often once titanium gets tight, without any extra code from us.

The strategic implication: cost scaling isn't a clock ticking against you — it's a running tally of what your own team has already built. Everything you build makes the next thing you build a little more expensive, so it pays to sequence builds deliberately (cheapest, highest-leverage things first) rather than to rush for its own sake. A bot that spends its first hundred rounds scouting and building nothing pays no scale tax at all when it finally starts building.

### Try it

```
fcode run starter starter
fcode watch replay.replay26
```

What you should see: the printed cost line climbing as the Core keeps spawning Builder Bots — a Harvester that costs 20 Ti before anything is built should cost noticeably more by round 500, purely because of everything spawned in between.

Next: recap, and why this tutorial ends with a bot that still can't grow its economy.
Building a HarvesterRecap & checkpoint



=== tutorials/harvesting-titanium/05-recap ===
· Step 5 of 5

### Recap & checkpoint

You now have a bot that:

- Reads the team's shared titanium balance with ct.get_global_resources()

- Seeks out visible ore using Environment.ORE_TITANIUM, pos.distance_squared(), and pos.direction_to()

- Builds a Harvester on an orthogonally adjacent ore tile with ct.can_build_harvester / ct.build_harvester

- Reads scaling costs with ct.get_scale_percent() and ct.get_*_cost()

But it still ends this tutorial with zero mined titanium reaching its balance, no matter how many Harvesters it builds. That's not a loose end we forgot — a Harvester's income is physically stranded unless something routes it to a sink. That "something" is a Conveyor.

Next up: Logistics: Conveyors & Splitters — finally get that titanium moving.
Cost scaling & early expansionFinish & start Logistics: Conveyors & Splitters



=== tutorials/conveyors-logistics/01-why-routing-matters ===
· Step 1 of 5

### Why routing matters

Tutorial 2 ended with a real Harvester that never grew your balance. Here's why: a Harvester's output only reaches the 4 tiles directly next to it (north, east, south, west). If none of those tiles can accept a stack — and on a real map, none usually can until you build something there — the Harvester just sits idle, output ready but going nowhere. It isn't wasting titanium each round; it simply won't produce the next stack until something is there to receive the current one.

Conveyors solve this by relaying resources one tile per round, in a single direction chosen when you build them. Chain enough of them together and you can move titanium from anywhere on the map back to base.

One API detail matters a lot here: conveyors (and Splitters, later in this tutorial) can only face the 4 cardinal directions — NORTH, EAST, SOUTH, WEST — never a diagonal. That's the same CARDINALS list you've been moving with since Tutorial 1, doing double duty for building facings:

```
CARDINALS = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
```

You'll also need to know exactly where your Core is, in a form that's more precise than "wherever I spawned." Every Builder Bot can find it by scanning its surroundings for a building whose type is EntityType.CORE:

```
core_tile = None
for tile in ct.get_nearby_tiles():
    bid = ct.get_tile_building_id(tile)
    if bid is not None and ct.get_entity_type(bid) == EntityType.CORE:
        core_tile = tile
        break
```

At round 1 the Core is the only building on the map, so the first builder-owned tile this finds is guaranteed to be part of the Core's footprint. Cache the result once — the Core never moves — the same way you'd cache anything expensive to recompute.

Next: put a chain together and watch what happens when you don't quite get the routing right.
Building a conveyor chain



=== tutorials/conveyors-logistics/02-building-a-conveyor-chain ===
· Step 2 of 5

### Building a conveyor chain

Let's build a first version: find ore, build a Harvester on it, then walk back toward the Core one tile at a time, laying a conveyor at each tile that points toward the next one.

```
import random

from fcode import Controller, Direction, Environment, EntityType, Position

# Builder bots move only in the four cardinal directions.
CARDINALS = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]


def in_bounds(ct: Controller, pos: Position) -> bool:
    return 0 <= pos.x < ct.get_map_width() and 0 <= pos.y < ct.get_map_height()


class Player:
    def __init__(self):
        self.core_tile: Position | None = None
        self.harvester_pos: Position | None = None
        self.chain_done = False

    def run(self, ct: Controller) -> None:
        etype = ct.get_entity_type()
        if etype == EntityType.CORE:
            self._run_core(ct)
        elif etype == EntityType.BUILDER_BOT:
            self._run_builder(ct)

    def _run_core(self, ct: Controller) -> None:
        for pos in ct.get_nearby_tiles(dist_sq=2):
            if ct.can_spawn(pos):
                ct.spawn_builder(pos)
                break

    def _run_builder(self, ct: Controller) -> None:
        pos = ct.get_position()
        if self.core_tile is None:
            for tile in ct.get_nearby_tiles():
                bid = ct.get_tile_building_id(tile)
                if bid is not None and ct.get_entity_type(bid) == EntityType.CORE:
                    self.core_tile = tile
                    break

        if self.harvester_pos is None:
            self._seek_and_harvest(ct, pos)
        elif not self.chain_done and self.core_tile is not None:
            self._lay_conveyor_toward_core(ct, pos)

    def _seek_and_harvest(self, ct: Controller, pos: Position) -> None:
        # Only cardinal ore tiles: a Harvester's output only reaches its 4
        # cardinal neighbours, so our chain has to start on one of those exactly.
        for d in CARDINALS:
            tile = pos.add(d)
            if not in_bounds(ct, tile):
                continue
            if ct.get_tile_env(tile) == Environment.ORE_TITANIUM and ct.can_build_harvester(tile):
                ct.build_harvester(tile)
                self.harvester_pos = tile
                return

        ore_tiles = [t for t in ct.get_nearby_tiles() if ct.get_tile_env(t) == Environment.ORE_TITANIUM]
        if ore_tiles:
            target = min(ore_tiles, key=lambda t: pos.distance_squared(t))
            direction = pos.cardinal_direction_to(target)
            if ct.can_move(direction):
                ct.move(direction)
                return

        open_dirs = [
            d for d in CARDINALS
            if ct.can_move(d) and ct.get_tile_env(pos.add(d)) == Environment.EMPTY
        ]
        move_options = open_dirs or [d for d in CARDINALS if ct.can_move(d)]
        if move_options:
            ct.move(random.choice(move_options))

    def _pick_direction(self, ct: Controller, pos: Position) -> Direction | None:
        assert self.core_tile is not None
        dx = self.core_tile.x - pos.x
        dy = self.core_tile.y - pos.y
        if dx != 0:
            d = Direction.EAST if dx > 0 else Direction.WEST
            if ct.can_move(d):
                return d
        if dy != 0:
            d = Direction.SOUTH if dy > 0 else Direction.NORTH
            if ct.can_move(d):
                return d
        return None

    def _lay_conveyor_toward_core(self, ct: Controller, pos: Position) -> None:
        direction = self._pick_direction(ct, pos)
        if direction is None:
            self.chain_done = True
            return

        # Builder bots can only build on an orthogonally adjacent tile,
        # never their own -- so the conveyor goes on the tile we're about
        # to step onto, not the one we're standing on.
        next_pos = pos.add(direction)
        neighbor = next_pos.add(direction)
        facing_core = False
        if in_bounds(ct, neighbor):
            bid = ct.get_tile_building_id(neighbor)
            facing_core = bid is not None and ct.get_entity_type(bid) == EntityType.CORE

        if ct.can_build_conveyor(next_pos, direction):
            ct.build_conveyor(next_pos, direction)

        if facing_core:
            self.chain_done = True
            return

        # A successful build already used this round's action, which now
        # also blocks this round's move -- so this simply does nothing
        # until next round, when the conveyor is already there (the build
        # above becomes a no-op) and the move goes through instead.
        if ct.can_move(direction):
            ct.move(direction)
```

_pick_direction closes the horizontal gap to the Core first, then the vertical one — a simple L-shaped route that's enough to get around a lot of terrain without real pathfinding. Builder Bots can only ever build on a tile orthogonally adjacent to themselves, never their own — so _lay_conveyor_toward_core builds the conveyor one tile ahead, on the tile it's about to step onto, facing the same direction it's about to walk (and, same as before, checks whether that conveyor's own output faces straight into the Core, in which case we're done). Building and moving now share the same round's budget too: a successful build uses up the round's action and blocks that round's move, so the ct.can_move(direction) check right after it will simply come back False the round a build just happened — the bot just waits. Next round, the conveyor is already there, so the build is skipped (can_build_conveyor now returns False) and the guarded move goes through instead. No extra state needed to track any of this — it falls out of the same two checks, one round later.

### Try it

```
fcode run starter starter
fcode watch replay.replay26
```

What you should see: check the match summary for a mined figure next to titanium. Run it a few times, maybe with fcode run starter starter --seed 2 and a couple of other seed numbers — you'll likely notice this chain works some of the time and silently fails the rest. When it fails, don't expect a clean gap in the chain: look closely near the Core in the replay and you may instead find one extra conveyor sitting at the very end, built the round before the bot gave up, facing whichever way it happened to be walking rather than the Core. Either way, no error, no crash, nothing in the logs — titanium just stops arriving. That's a real, reproducible bug in the code above — not a fluke of the RNG. Let's go find it.
Why routing mattersThe last mile



=== tutorials/conveyors-logistics/03-the-last-mile ===
· Step 3 of 5

### The last mile

Here's the bug from the previous step: _pick_direction only returns a direction when ct.can_move(d) is True. The Core's footprint is never bot-passable — not even to its own team — so can_move reliably returns False the moment a neighbouring tile belongs to the Core. That looks like a free "have I arrived?" signal, except the Core is 2×2: approach it diagonally and both candidate directions can be blocked by two different footprint tiles, so _pick_direction gives up (None) without ever checking whether what's blocking it is actually the Core. False from can_move just means "something's there" — a Core tile, a wall, another bot — it can't tell you which. The reliable fix is simpler: stop trying to infer "have I arrived?" from whether you can move forward, and just check who's standing next to you.

```
import random

from fcode import Controller, Direction, Environment, EntityType, Position

# Builder bots move only in the four cardinal directions.
CARDINALS = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]


def in_bounds(ct: Controller, pos: Position) -> bool:
    return 0 <= pos.x < ct.get_map_width() and 0 <= pos.y < ct.get_map_height()


class Player:
    def __init__(self):
        self.core_tile: Position | None = None
        self.harvester_pos: Position | None = None
        self.chain_done = False

    def run(self, ct: Controller) -> None:
        etype = ct.get_entity_type()
        if etype == EntityType.CORE:
            self._run_core(ct)
        elif etype == EntityType.BUILDER_BOT:
            self._run_builder(ct)

    def _run_core(self, ct: Controller) -> None:
        for pos in ct.get_nearby_tiles(dist_sq=2):
            if ct.can_spawn(pos):
                ct.spawn_builder(pos)
                break

    def _run_builder(self, ct: Controller) -> None:
        pos = ct.get_position()
        if self.core_tile is None:
            for tile in ct.get_nearby_tiles():
                bid = ct.get_tile_building_id(tile)
                if bid is not None and ct.get_entity_type(bid) == EntityType.CORE:
                    self.core_tile = tile
                    break

        if self.harvester_pos is None:
            self._seek_and_harvest(ct, pos)
        elif not self.chain_done and self.core_tile is not None:
            self._lay_conveyor_toward_core(ct, pos)

    def _seek_and_harvest(self, ct: Controller, pos: Position) -> None:
        for d in CARDINALS:
            tile = pos.add(d)
            if not in_bounds(ct, tile):
                continue
            if ct.get_tile_env(tile) == Environment.ORE_TITANIUM and ct.can_build_harvester(tile):
                ct.build_harvester(tile)
                self.harvester_pos = tile
                return

        ore_tiles = [t for t in ct.get_nearby_tiles() if ct.get_tile_env(t) == Environment.ORE_TITANIUM]
        if ore_tiles:
            target = min(ore_tiles, key=lambda t: pos.distance_squared(t))
            direction = pos.cardinal_direction_to(target)
            if ct.can_move(direction):
                ct.move(direction)
                return

        open_dirs = [
            d for d in CARDINALS
            if ct.can_move(d) and ct.get_tile_env(pos.add(d)) == Environment.EMPTY
        ]
        move_options = open_dirs or [d for d in CARDINALS if ct.can_move(d)]
        if move_options:
            ct.move(random.choice(move_options))

    def _pick_direction(self, ct: Controller, pos: Position) -> Direction | None:
        assert self.core_tile is not None
        dx = self.core_tile.x - pos.x
        dy = self.core_tile.y - pos.y
        if dx != 0:
            d = Direction.EAST if dx > 0 else Direction.WEST
            if ct.can_move(d):
                return d
        if dy != 0:
            d = Direction.SOUTH if dy > 0 else Direction.NORTH
            if ct.can_move(d):
                return d
        return None

    def _lay_conveyor_toward_core(self, ct: Controller, pos: Position) -> None:
        # Check every tile we could build on for the Core BEFORE calling
        # _pick_direction, independent of movement. Builder bots can only
        # build on an orthogonally adjacent tile now, never their own -- so
        # the final relay conveyor always has to go one tile AHEAD of us,
        # and we have to find that tile by checking who's standing next to
        # each of our neighbours, not by asking whether we can step toward
        # the Core (can_move() fails the same way next to a wall or another
        # bot).
        for d in CARDINALS:
            next_pos = pos.add(d)
            if not in_bounds(ct, next_pos):
                continue
            for d2 in CARDINALS:
                neighbor = next_pos.add(d2)
                if not in_bounds(ct, neighbor):
                    continue
                bid = ct.get_tile_building_id(neighbor)
                if bid is not None and ct.get_entity_type(bid) == EntityType.CORE:
                    if ct.can_build_conveyor(next_pos, d2):
                        ct.build_conveyor(next_pos, d2)
                    self.chain_done = True
                    return

        direction = self._pick_direction(ct, pos)
        if direction is None:
            self.chain_done = True
            return

        next_pos = pos.add(direction)
        if ct.can_build_conveyor(next_pos, direction):
            ct.build_conveyor(next_pos, direction)
        if ct.can_move(direction):
            ct.move(direction)
```

_lay_conveyor_toward_core now checks every tile it could build on for a Core-type building first, independent of _pick_direction — one tile further out than before, since the final relay conveyor can no longer be built by standing on it; it has to be placed from one tile back, exactly like every other segment in the chain. If a candidate tile touches the Core, we build the final conveyor there facing it and stop — we never even attempt to walk onto it, since a conveyor doesn't need a bot standing on it to work. Only if no neighbour leads to a Core-adjacent tile do we fall through to _pick_direction and advance normally.

The general lesson is worth keeping: when you need to know "has something specific happened," query for it directly (get_tile_building_id + get_entity_type) rather than inferring it from a side effect of a different action (can_move). A blocked move can mean a dozen different things — the Core's footprint, a wall, another bot standing there — and treating all of them as "I've arrived" fails silently: no exception, just a chain that stops one tile short with no explanation.

### Try it

```
fcode run starter starter
fcode watch replay.replay26
```

What you should see: noticeably more consistent mined numbers across repeated runs and different seeds — not perfect (independent Builder Bots can still occasionally block each other's paths, since this is still a fairly naive router), but reliably nonzero on at least one side most of the time.

Next: give a Harvester's output more than one place it can go.
Building a conveyor chainSplitting the flow



=== tutorials/conveyors-logistics/04-splitting-the-flow ===
· Step 4 of 5

### Splitting the flow

A plain Conveyor has exactly one output tile: whatever's directly in front of it. A Splitter takes input from directly behind it and can output to any of the other three cardinal sides — useful once you want one Harvester's income to reach your Core by more than one route. It doesn't split a stack across sides simultaneously: each delivery goes whole (10 Ti) to whichever connected side hasn't been used in the longest time, so with multiple outputs wired up, they take turns receiving stacks rather than all carrying titanium at once.

ct.build_splitter(pos, direction) uses direction the same way build_conveyor does: it's the side the flow continues toward. The input side is automatically the opposite direction. So swapping the final segment of our chain from a Conveyor to a Splitter doesn't change how it feeds the Core — it just opens up two more sides for something else to tap into later.

```
                if bid is not None and ct.get_entity_type(bid) == EntityType.CORE:
                    if ct.can_build_splitter(next_pos, d2):
                        ct.build_splitter(next_pos, d2)
                    self.chain_done = True
                    return
```

That's the only change needed to _lay_conveyor_toward_core from the previous step — everywhere else, ct.build_conveyor(next_pos, direction) becomes ct.build_splitter(next_pos, direction) and can_build_conveyor becomes can_build_splitter. Titanium still reaches your Core exactly as before; the difference is invisible until you actually build something on one of the Splitter's other two output sides.

The obvious thing to do with those spare sides is redundancy. A single conveyor chain is a single point of failure: an enemy Builder Bot only has to reach one tile of it and destroy it, and your Harvester's entire income stops arriving until you notice and rebuild. Wire a second path out of a Splitter — even a longer, more roundabout one — and a cut in either branch leaves the other still delivering. The Splitter keeps alternating between whichever sides are still connected, so a sabotaged branch costs you throughput rather than all of your income.

We won't wire up that second route in this tutorial, but keep the idea in mind: a Splitter at a junction is a cheap way to keep your options open, and the cheapest insurance you can buy against having your supply line cut.

### Try it

```
fcode run starter starter
fcode watch replay.replay26
```

What you should see: the same delivery behavior as the previous step — titanium still reaches your Core through the Splitter exactly as it did through the plain Conveyor.

Next: recap, and what this tutorial sets up for combat.
The last mileRecap & checkpoint



=== tutorials/conveyors-logistics/05-recap ===
· Step 5 of 5

### Recap & checkpoint

You now have a bot that:

- Locates its own Core precisely, by scanning for a building of type EntityType.CORE rather than guessing from spawn position

- Builds a cardinal-only conveyor chain from a Harvester back to the Core with ct.can_build_conveyor / ct.build_conveyor

- Routes around simple obstacles with a two-axis (horizontal-then-vertical) walk

- Detects "have I arrived" by querying tile occupancy directly, instead of relying on can_move as a proxy — and knows why that distinction matters

- Understands Splitters as a drop-in upgrade for the last conveyor segment before a destination, opening up extra output sides

Titanium should now be visibly flowing from ore to Core — the "mined" column in your match summary should read nonzero for at least one side most of the time. This bot is still rough: independent Builder Bots can collide with each other's chains, dead ends aren't routed around, and none of this is optimized. That's fine. You have a working economy loop, which is the foundation everything else builds on.

Next up: Building an Army: Turrets & Combat — put that Splitter's spare output to use feeding a Gunner.
Splitting the flowFinish & start Building an Army: Turrets & Combat



=== tutorials/turrets-combat/01-meet-the-turrets ===
· Step 1 of 5

### Meet the turrets

Turrets are stationary buildings that attack automatically once built — no CPU time spent aiming or deciding when to fire. There are three:

Turret | HP | Cost | Damage | Ammo/shot | Reload | 
Gunner | 25 | 20 Ti | 7 | 4 | 1 round | 
Sentinel | 40 | 30 Ti | 18 | 10 | 2 rounds | 
Launcher | 30 | 20 Ti | — (repositions a Builder Bot instead) | — | 1 round | 

The Gunner is what you'll build first: the cheapest turret, firing every round, and the only one you can re-aim after building it. It fires a narrow ray straight ahead in its facing direction — anything in that line, friend or foe, blocks and can be hit. It's also the flimsiest thing you can build at 25 HP, so don't leave one exposed. The Sentinel fires the same single-tile-wide line, but reaches much further and can't be blocked by anything standing in the way — trading 10 more titanium and a 2-round reload for that reach, 18 damage a hit, and enough hit points to survive being shot at; it's a defensive anchor, not something you spam early. The Launcher doesn't deal damage at all — it picks up a Builder Bot within range, from either team, and throws it to a target position, which is a repositioning tool, not a weapon.

One thing isn't obvious from the numbers above: ammunition is a team-wide balance, not something a turret carries — and it starts at 0. A freshly built Gunner simply won't fire, no matter how good its target is, until your Core converts titanium into ammunition for the team. That's the entire subject of the next two steps.

Next: build one and see this for yourself.
Building a Gunner



=== tutorials/turrets-combat/02-building-a-gunner ===
· Step 2 of 5

### Building a Gunner

ct.build_gunner(pos, direction) works exactly like the other builds you already know — check with can_build_gunner, then build, and pick a facing direction for it to watch. Let's set up a small self-contained cluster: a Harvester, and a Gunner right next to it.

```
import random

from fcode import Controller, Direction, Environment, EntityType, Position

CARDINALS = [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]


def in_bounds(ct: Controller, pos: Position) -> bool:
    return 0 <= pos.x < ct.get_map_width() and 0 <= pos.y < ct.get_map_height()


class Player:
    def __init__(self):
        self.built = False

    def run(self, ct: Controller) -> None:
        etype = ct.get_entity_type()
        if etype == EntityType.CORE:
            for pos in ct.get_nearby_tiles(dist_sq=2):
                if ct.can_spawn(pos):
                    ct.spawn_builder(pos)
                    break
        elif etype == EntityType.BUILDER_BOT:
            self._run_builder(ct)
        elif etype == EntityType.GUNNER:
            self._run_gunner(ct)

    def _run_builder(self, ct: Controller) -> None:
        if self.built:
            return
        pos = ct.get_position()

        harvester_pos = pos.add(Direction.NORTH)
        gunner_pos = pos.add(Direction.SOUTH)
        if not in_bounds(ct, harvester_pos) or not in_bounds(ct, gunner_pos):
            self._explore(ct, pos)
            return

        if ct.get_tile_env(harvester_pos) == Environment.ORE_TITANIUM:
            if ct.can_build_harvester(harvester_pos):
                ct.build_harvester(harvester_pos)
            if ct.can_build_gunner(gunner_pos, Direction.SOUTH):
                ct.build_gunner(gunner_pos, Direction.SOUTH)
                self.built = True
            return

        self._explore(ct, pos)

    def _explore(self, ct: Controller, pos: Position) -> None:
        open_dirs = [
            d for d in CARDINALS
            if ct.can_move(d) and ct.get_tile_env(pos.add(d)) == Environment.EMPTY
        ]
        move_options = open_dirs or [d for d in CARDINALS if ct.can_move(d)]
        if move_options:
            ct.move(random.choice(move_options))

    def _run_gunner(self, ct: Controller) -> None:
        if ct.get_current_round() % 100 == 0:
            print(f"round {ct.get_current_round()}: ammo = {ct.get_global_ammo()}")
        target = ct.get_gunner_target()
        if target is not None and ct.can_fire(target):
            ct.fire(target)
```

A Builder Bot that finds ore builds a Harvester one tile north of itself and a Gunner one tile south, facing further south — income and a guard for it, both within its action radius so no extra movement is needed. The Gunner's own run() branch checks ct.get_global_ammo() — the team's shared ammunition balance — and tries to fire at whatever ct.get_gunner_target() finds in its line of sight.

### Try it

```
fcode run starter starter
fcode watch replay.replay26
```

What you should see: every 100 rounds, a printed line reading ammo = 0 — for the entire match. The Gunner never fires, no matter what walks in front of it. It's built, it's facing the right way, and it's completely useless: our team never produced a single unit of ammunition.

Next: fix that with two lines in the Core.
Meet the turretsThe ammo gap



=== tutorials/turrets-combat/03-the-ammo-gap ===
· Step 3 of 5

### The ammo gap

Ammunition isn't a thing turrets carry — it's a team-wide balance, like your titanium, and it starts at 0. There's exactly one way to fill it: your Core converts titanium into ammunition with ct.convert_ammo(amount), 1:1, at most once per turn. The ammunition is usable the same turn, every turret on your team fires from the same pool, and converting doesn't use the Core's action cooldown — it never costs you a spawn.

So the fix for our silent Gunner isn't anywhere near the Gunner. It's two lines in the Core's branch:

```
import random

from fcode import Controller, Direction, Environment, EntityType, Position

CARDINALS = [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]


def in_bounds(ct: Controller, pos: Position) -> bool:
    return 0 <= pos.x < ct.get_map_width() and 0 <= pos.y < ct.get_map_height()


class Player:
    def __init__(self):
        self.built = False

    def run(self, ct: Controller) -> None:
        etype = ct.get_entity_type()
        if etype == EntityType.CORE:
            # Keep the team's ammunition topped up: 1 titanium -> 1 ammo,
            # at most once per turn — and it never costs us a spawn.
            if ct.get_global_ammo() < 20 and ct.can_convert_ammo(10):
                ct.convert_ammo(10)
            for pos in ct.get_nearby_tiles(dist_sq=2):
                if ct.can_spawn(pos):
                    ct.spawn_builder(pos)
                    break
        elif etype == EntityType.BUILDER_BOT:
            self._run_builder(ct)
        elif etype == EntityType.GUNNER:
            self._run_gunner(ct)

    def _run_builder(self, ct: Controller) -> None:
        if self.built:
            return
        pos = ct.get_position()

        harvester_pos = pos.add(Direction.NORTH)
        gunner_pos = pos.add(Direction.SOUTH)
        if not in_bounds(ct, harvester_pos) or not in_bounds(ct, gunner_pos):
            self._explore(ct, pos)
            return

        if ct.get_tile_env(harvester_pos) == Environment.ORE_TITANIUM:
            if ct.can_build_harvester(harvester_pos):
                ct.build_harvester(harvester_pos)
            if ct.can_build_gunner(gunner_pos, Direction.SOUTH):
                ct.build_gunner(gunner_pos, Direction.SOUTH)
                self.built = True
            return

        self._explore(ct, pos)

    def _explore(self, ct: Controller, pos: Position) -> None:
        open_dirs = [
            d for d in CARDINALS
            if ct.can_move(d) and ct.get_tile_env(pos.add(d)) == Environment.EMPTY
        ]
        move_options = open_dirs or [d for d in CARDINALS if ct.can_move(d)]
        if move_options:
            ct.move(random.choice(move_options))

    def _run_gunner(self, ct: Controller) -> None:
        if ct.get_current_round() % 100 == 0:
            print(f"round {ct.get_current_round()}: ammo = {ct.get_global_ammo()}")
        target = ct.get_gunner_target()
        if target is not None and ct.can_fire(target):
            ct.fire(target)
```

The buffer logic is worth reading twice, because it's a pattern you'll reuse: top the pool up to 20 whenever it dips (that's 5 Gunner shots, or 2 Sentinel shots), 10 titanium at a time. ct.can_convert_ammo(amount) is the legality check — it's False if you're not the Core, can't afford amount, or already converted this turn. Don't convert your whole treasury: titanium spent on ammunition can't be spent on builders and buildings, and there's no converting back.

### Try it

```
fcode run starter starter
fcode watch replay.replay26
```

What you should see: the printed ammo line jumps to 20 within the first couple of rounds and stays topped up. Each Gunner shot costs 4 from the pool — if an enemy unit crosses the firing line, you'll see the number dip and recover as the Core converts again. In the visualiser, the team panel on the left shows your Ammo balance next to titanium, so you can watch the economy and the arsenal side by side.

Next: give your Builder Bots a way to defend themselves too.
Building a GunnerHealing and sabotage



=== tutorials/turrets-combat/04-healing-and-sabotage ===
· Step 4 of 5

### Healing and sabotage

Builder Bots have two more combat-adjacent abilities worth knowing, and both are narrower than they might sound at first.

ct.heal(pos) repairs damaged friendly entities on a tile — like fire, it's restricted to a tile that's orthogonally adjacent to the Builder Bot (NORTH, SOUTH, EAST, or WEST, never diagonal and never its own tile) — for 4 HP at a cost of 1 titanium. It heals a building and a Builder Bot standing on it in the same call if both are friendly and damaged. Use ct.can_heal(pos) first — it checks adjacency, cooldown, titanium, and that there's actually damage to repair.

```
for d in (Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST):
    target = ct.get_position().add(d)  # an adjacent tile, never your own
    if ct.can_heal(target):
        ct.heal(target)
        break
```

ct.fire(pos) is more restrictive than it looks: a Builder Bot can only target a tile that's orthogonally adjacent to it — NORTH, SOUTH, EAST, or WEST of its current position, never diagonal and never its own tile — and only damages the building there. It's not a way to attack a nearby enemy unit — for that, you'd need a turret. What it's actually for is sabotage: walk up next to an enemy's logistics chain (Conveyor and Splitter tiles are walkable, so you could also stand on one and fire at whatever's next to you) and damage a building from the side. Two titanium per hit, same as the cost of the shot itself.

```
for d in (Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST):
    target = ct.get_position().add(d)  # an adjacent tile, never your own
    if ct.can_fire(target):
        ct.fire(target)
        break
```

One more method you'll see referenced elsewhere: ct.self_destruct(). Older material (including some in-game documentation) describes it as dealing area damage when you blow up — that's no longer how it works. Self-destructing a Builder Bot today deals zero damage to anything nearby; it just removes the unit. Its only real use is freeing up your 50-unit cap or retreating a doomed bot before it gets picked off for a bounty — it is not a weapon.

### Try it

You don't need a full match to see these work — try building a Conveyor on a tile adjacent to your Builder Bot, firing at that tile a couple of times to damage it, then healing it back up:

```
if ct.can_fire(pos):
    ct.fire(pos)
elif ct.can_heal(pos):
    ct.heal(pos)
```

What you should see: the Conveyor's HP drop by 2 each time you fire, then climb back by 4 each time you heal, in the replay's building-health display.

Next: recap, and putting a full economy-plus-defense bot together.
The ammo gapRecap & checkpoint



=== tutorials/turrets-combat/05-recap ===
· Step 5 of 5

### Recap & checkpoint

You now have a bot that:

- Knows the three turret types and their tradeoffs — Gunner (cheapest, fastest-firing, fragile), Sentinel (durable, hard-hitting, long reach), Launcher (repositions, doesn't damage)

- Builds a Gunner with ct.build_gunner and confirmed it does nothing without ammunition

- Keeps the team's ammunition topped up by converting titanium at the Core (ct.convert_ammo), and watched ct.get_global_ammo() fill up and drop as the Gunner fires

- Uses ct.heal() to repair damaged friendly entities (buildings and Builder Bots alike) on a tile

- Understands ct.fire()'s real scope for Builder Bots — sabotaging whatever building you're standing on, friendly or enemy — and that self_destruct() is a cleanup tool, not a weapon

The combination you built in this tutorial — a Harvester for income, a Gunner guarding it, and a Core that keeps the ammunition balance topped up — is a real, if small, piece of a competitive bot. Everything from here is about connecting more pieces like it and coordinating them.

Next up: Coordination & Strategy — use the Global Communication Store to let multiple Builder Bots share information, and put together a bot that combines everything from all four tutorials.
Healing and sabotageFinish & start Coordination & Strategy



=== tutorials/comms-strategy/01-the-global-communication-store ===
· Step 1 of 4

### The Global Communication Store

Every unit you've written so far has acted alone — a Builder Bot only knows what it can personally see. The Global Communication Store is a shared blackboard: 16 integer slots (indexed 0–15), readable and writable by every unit on your team.

```
ct.write_store(0, 42)
value = ct.read_store(0)
```

There's one timing rule that matters more than anything else about the Store: writes are buffered. A write made this round isn't visible until the next round — not even to the unit that made it.

```
# Core, round N:
ct.write_store(0, 42)
value = ct.read_store(0)  # still 0 -- this round's snapshot hasn't changed

# Any unit, round N+1:
value = ct.read_store(0)  # now 42
```

This is deliberate, not a quirk to work around: it guarantees every unit sees a consistent snapshot of the Store for the entire round, no matter what order units happen to execute in. Design your protocol around the one-round lag rather than fighting it — and give your slots names instead of leaving magic numbers scattered through your code:

```
SLOT_ORE_X = 0
SLOT_ORE_Y = 1
```

Next: put the Store to work letting Builder Bots share what they've found.
Coordinating roles



=== tutorials/comms-strategy/02-coordinating-roles ===
· Step 2 of 4

### Coordinating roles

Back in Tutorial 2, every Builder Bot searched for ore entirely on its own — fine with one bot, wasteful with many, since each one re-discovers the same patches independently instead of splitting up. Let's have any bot that spots an uncovered ore tile broadcast it, so bots with nothing in sight can head toward a real target instead of wandering randomly.

```
import random

from fcode import Controller, Direction, Environment, EntityType, Position

CARDINALS = [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]

SLOT_ORE_X = 0
SLOT_ORE_Y = 1


class Player:
    def run(self, ct: Controller) -> None:
        etype = ct.get_entity_type()
        if etype == EntityType.CORE:
            for pos in ct.get_nearby_tiles(dist_sq=2):
                if ct.can_spawn(pos):
                    ct.spawn_builder(pos)
                    break
        elif etype == EntityType.BUILDER_BOT:
            self._run_builder(ct)

    def _run_builder(self, ct: Controller) -> None:
        pos = ct.get_position()
        self._share_ore(ct, pos)

        for tile in ct.get_nearby_tiles(dist_sq=2):
            if ct.get_tile_env(tile) == Environment.ORE_TITANIUM and ct.can_build_harvester(tile):
                ct.build_harvester(tile)
                return

        ore_tiles = [
            t for t in ct.get_nearby_tiles() if ct.get_tile_env(t) == Environment.ORE_TITANIUM
        ]
        if ore_tiles:
            target = min(ore_tiles, key=lambda t: pos.distance_squared(t))
        else:
            shared_x, shared_y = ct.read_store(SLOT_ORE_X), ct.read_store(SLOT_ORE_Y)
            target = Position(shared_x, shared_y) if (shared_x or shared_y) else None

        if target is not None:
            direction = pos.direction_to(target)
            if ct.can_move(direction):
                ct.move(direction)
                return

        open_dirs = [
            d for d in CARDINALS
            if ct.can_move(d) and ct.get_tile_env(pos.add(d)) == Environment.EMPTY
        ]
        move_options = open_dirs or [d for d in CARDINALS if ct.can_move(d)]
        if move_options:
            ct.move(random.choice(move_options))

    def _share_ore(self, ct: Controller, pos: Position) -> None:
        for tile in ct.get_nearby_tiles():
            if ct.get_tile_env(tile) == Environment.ORE_TITANIUM and ct.get_tile_building_id(tile) is None:
                ct.write_store(SLOT_ORE_X, tile.x)
                ct.write_store(SLOT_ORE_Y, tile.y)
                return
```

_share_ore runs first, every round, for every Builder Bot: the moment any of them sees an ore tile with nothing built on it, its position goes into slots 0 and 1. Any bot that can't see ore itself falls back to reading that shared location instead of wandering — (shared_x or shared_y) is a cheap way to distinguish "nothing's been shared yet" (both slots still at their default 0) from a real coordinate.

This is a genuinely simple protocol — one shared target, overwritten by whoever last saw ore, no negotiation about who should actually go there. Multiple bots can and will pile onto the same tile. That's fine for now; the Store gives you the primitive, and how you use those 16 slots is entirely up to your own strategy.

### Try it

```
fcode run starter starter
fcode watch replay.replay26
```

What you should see: Builder Bots that start with no ore in sight beelining toward a specific spot instead of wandering, once any teammate has spotted ore somewhere on the map.

Next: merge this with everything from the last three tutorials into one bot.
The Global Communication StorePutting it all together



=== tutorials/comms-strategy/03-putting-it-together ===
· Step 3 of 4

### Putting it all together

Everything from Tutorials 1 through 5 fits into one bot: sense the map, harvest ore, route it to the Core with a conveyor chain that ends in a Splitter, use the Splitter's spare side to feed a Gunner, and share ore locations over the Store so Builder Bots aren't all working blind.

```
import random

from fcode import Controller, Direction, Environment, EntityType, Position

CARDINALS = [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]
CARDINALS = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]

SLOT_ORE_X = 0
SLOT_ORE_Y = 1


def in_bounds(ct: Controller, pos: Position) -> bool:
    return 0 <= pos.x < ct.get_map_width() and 0 <= pos.y < ct.get_map_height()


class Player:
    def __init__(self):
        self.core_tile: Position | None = None
        self.harvester_pos: Position | None = None
        self.chain_done = False
        self.gunner_built = False
        self.gunner_side: Direction | None = None
        self.splitter_pos: Position | None = None

    def run(self, ct: Controller) -> None:
        etype = ct.get_entity_type()
        if etype == EntityType.CORE:
            self._run_core(ct)
        elif etype == EntityType.BUILDER_BOT:
            self._run_builder(ct)
        elif etype == EntityType.GUNNER:
            self._run_gunner(ct)

    def _run_core(self, ct: Controller) -> None:
        for pos in ct.get_nearby_tiles(dist_sq=2):
            if ct.can_spawn(pos):
                ct.spawn_builder(pos)
                break

    def _run_builder(self, ct: Controller) -> None:
        pos = ct.get_position()
        if self.core_tile is None:
            for tile in ct.get_nearby_tiles():
                bid = ct.get_tile_building_id(tile)
                if bid is not None and ct.get_entity_type(bid) == EntityType.CORE:
                    self.core_tile = tile
                    break

        self._share_ore(ct, pos)

        if self.harvester_pos is None:
            self._seek_and_harvest(ct, pos)
        elif not self.chain_done and self.core_tile is not None:
            self._lay_conveyor_toward_core(ct, pos)
        elif not self.gunner_built and self.splitter_pos is not None and self.gunner_side is not None:
            self._build_gunner(ct)

    def _share_ore(self, ct: Controller, pos: Position) -> None:
        for tile in ct.get_nearby_tiles():
            if ct.get_tile_env(tile) == Environment.ORE_TITANIUM and ct.get_tile_building_id(tile) is None:
                ct.write_store(SLOT_ORE_X, tile.x)
                ct.write_store(SLOT_ORE_Y, tile.y)
                return

    def _seek_and_harvest(self, ct: Controller, pos: Position) -> None:
        for d in CARDINALS:
            tile = pos.add(d)
            if not in_bounds(ct, tile):
                continue
            if ct.get_tile_env(tile) == Environment.ORE_TITANIUM and ct.can_build_harvester(tile):
                ct.build_harvester(tile)
                self.harvester_pos = tile
                return

        ore_tiles = [t for t in ct.get_nearby_tiles() if ct.get_tile_env(t) == Environment.ORE_TITANIUM]
        if ore_tiles:
            target = min(ore_tiles, key=lambda t: pos.distance_squared(t))
        else:
            shared_x, shared_y = ct.read_store(SLOT_ORE_X), ct.read_store(SLOT_ORE_Y)
            target = Position(shared_x, shared_y) if (shared_x or shared_y) else None

        if target is not None:
            direction = pos.direction_to(target)
            if ct.can_move(direction):
                ct.move(direction)
                return

        open_dirs = [
            d for d in CARDINALS
            if ct.can_move(d) and ct.get_tile_env(pos.add(d)) == Environment.EMPTY
        ]
        move_options = open_dirs or [d for d in CARDINALS if ct.can_move(d)]
        if move_options:
            ct.move(random.choice(move_options))

    def _pick_direction(self, ct: Controller, pos: Position) -> Direction | None:
        assert self.core_tile is not None
        dx = self.core_tile.x - pos.x
        dy = self.core_tile.y - pos.y
        if dx != 0:
            d = Direction.EAST if dx > 0 else Direction.WEST
            if ct.can_move(d):
                return d
        if dy != 0:
            d = Direction.SOUTH if dy > 0 else Direction.NORTH
            if ct.can_move(d):
                return d
        return None

    def _lay_conveyor_toward_core(self, ct: Controller, pos: Position) -> None:
        # Builder bots can only build on an orthogonally adjacent tile now,
        # never their own -- so we check every tile we could build on for
        # the Core first, one tile further out than before, since the
        # final relay (the Splitter) can no longer be built by standing on
        # it either.
        for d in CARDINALS:
            next_pos = pos.add(d)
            if not in_bounds(ct, next_pos):
                continue
            for d2 in CARDINALS:
                neighbor = next_pos.add(d2)
                if not in_bounds(ct, neighbor):
                    continue
                bid = ct.get_tile_building_id(neighbor)
                if bid is not None and ct.get_entity_type(bid) == EntityType.CORE:
                    if ct.can_build_splitter(next_pos, d2):
                        ct.build_splitter(next_pos, d2)
                        self.splitter_pos = next_pos
                        for side in CARDINALS:
                            if side != d2 and side != d2.opposite():
                                self.gunner_side = side
                                break
                    self.chain_done = True
                    return

        direction = self._pick_direction(ct, pos)
        if direction is None:
            self.chain_done = True
            return

        next_pos = pos.add(direction)
        if ct.can_build_conveyor(next_pos, direction):
            ct.build_conveyor(next_pos, direction)
        if ct.can_move(direction):
            ct.move(direction)

    def _build_gunner(self, ct: Controller) -> None:
        assert self.splitter_pos is not None and self.gunner_side is not None
        pos = ct.get_position()
        if pos != self.splitter_pos:
            # The Splitter sits one tile ahead of us -- we stopped short of
            # it on purpose, since it can't be built while standing on it.
            # Splitters are bot-passable, so just walk onto it like any
            # other tile; the Gunner build happens next round from there.
            d = pos.cardinal_direction_to(self.splitter_pos)
            if ct.can_move(d):
                ct.move(d)
            return

        gunner_pos = self.splitter_pos.add(self.gunner_side)
        if in_bounds(ct, gunner_pos) and ct.can_build_gunner(gunner_pos, self.gunner_side):
            ct.build_gunner(gunner_pos, self.gunner_side)
        self.gunner_built = True

    def _run_gunner(self, ct: Controller) -> None:
        target = ct.get_gunner_target()
        if target is not None and ct.can_fire(target):
            ct.fire(target)
```

Nothing here is new mechanically — every piece was introduced and tested in an earlier tutorial. What's new is the state machine tying them together: each Builder Bot works through harvest → route → defend in order, tracked with a handful of instance attributes (harvester_pos, chain_done, gunner_built, ...) that persist for that unit's entire lifetime, exactly like self.num_spawned did all the way back in Tutorial 1.

One genuinely new wrinkle: because the Splitter is now built from one tile back rather than by standing on it, _build_gunner has to walk the bot onto the Splitter's tile first (Splitters are bot-passable) before it can build the Gunner beside it — the same "a build blocks this round's move, so wait a round" pattern you've already seen in _lay_conveyor_toward_core.

Be honest with yourself about what this bot isn't: it's not optimized, it doesn't handle every map layout, and independent Builder Bots can still collide with each other's plans. That's fine. It's a real, working demonstration of every mechanic in the game, and a legitimate base to build a stronger strategy from.

### Try it

```
fcode run starter starter
fcode watch replay.replay26
```

What you should see: Harvesters, conveyor chains, Splitters, and Gunners all appearing over the course of the match, Builder Bots occasionally converging on a shared ore target, and — on at least some runs — a Gunner that actually fires because its ammo pipeline is connected. Run it a few times with different seeds; results will vary, and that's expected.

Next: where to take this from here.
Coordinating rolesWhere to go from here



=== tutorials/comms-strategy/04-where-to-go-from-here ===
· Step 4 of 4

### Where to go from here

You've now touched every major system in the game: movement and sensing, the titanium economy, conveyor logistics, turret combat, and team-wide coordination through the Global Communication Store. That's the whole rulebook — everything from here is strategy, not new mechanics.

The platform ships a more polished reference bot at bots/starter_bot.py (or bots/starter/main.py if you ran fcode starter). It's built from the same pieces you just used, organized a little differently, and its own docstring is honest about what it doesn't do yet:

- Build full conveyor chains from distant Harvesters back to the Core

- Tune the ammo buffer: convert more titanium when enemies are near, less
when you'd rather grow the economy

- Add Sentinels or Launchers for stronger defense

- Explore the map systematically instead of picking random targets

- Use more Store slots to coordinate roles between Builder Bots

Notice that you already solved the second one in Tutorial 4 — the shipped starter bot doesn't. That's not a coincidence; it's a genuinely open problem, and a reasonable place to start improving on the reference implementation rather than your own bot from these tutorials.

Some concrete next steps, roughly in order of effort:

- Read the full Controller API Reference — plenty of methods (get_attackable_tiles, launch, can_fire_from, ...) weren't covered here.

- Fix the "independent bots collide" problem from Tutorial 5 — use Store slots to assign roles (harvester vs. router vs. defender) instead of letting every Builder Bot run the same logic.

- Add real pathfinding — the two-axis walk from Tutorial 3 gets stuck on anything more complex than a simple wall.

- Layer in Sentinels and Launchers — a Gunner-only defense is predictable and easy to counter.

When you're ready to see how your bot holds up:

```
fcode submit bots/starter
```

Your bot gets queued for ladder matches automatically — check the Matches page to see results, and the Ladder page to see how you rank. Good luck.
Putting it all togetherMark complete