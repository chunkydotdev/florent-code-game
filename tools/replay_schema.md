# The `.replay26` format

Recovered protobuf schema for `battlecode.Replay`, plus the wire-level facts you
need to read one correctly. Consumed by `tools/replay_census.py`; written down
here so the next parser doesn't have to rediscover it.

## How it was recovered

The bundled visualiser carries the **entire protobuf-js JSON descriptor inline**.
No reverse-engineering of bytes was needed for the message tree itself:

```bash
grep -o 'battlecode\.Replay' .venv/lib/python3.13/site-packages/fcode/data/visualiser/assets/main-*.js
```

That one hit is inside `Root.fromJSON(<descriptor>).lookupType("battlecode.Replay")`.
The descriptor object literal sits immediately before it — field names, types and
ids for every message. `battlecode.Map` inside it is the same message
`tools/make_map.py` *writes*, recovered independently from `map-editor-*.js`, and
the two agree, which anchors the field numbering for everything else.

Two things the descriptor does **not** tell you, both found by scanning real
replay bytes for fields the visualiser never reads (see "Undeclared fields"):
`Replay.winCondition` and an unidentified `Player` field 6.

## Message tree

```protobuf
message Replay {
  Map           map          = 1;
  repeated Turn turns        = 3;   // turns[i] IS round i (0-based)
  optional Team winner       = 4;
  string        winCondition = 6;   // undeclared in the visualiser schema
}                                   // fields 2 and 5: never observed

message Map {
  int32                 width  = 1;
  int32                 height = 2;
  repeated TileRow      rows   = 3;   // one per row, top to bottom
  repeated CorePosition cores  = 4;
}                                     // symmetry = 5 and entities = 6 exist in
                                      // files make_map.py writes; the Replay
                                      // copy of the schema omits both
message TileRow      { repeated Environment tiles = 1; }   // packed varints
message CorePosition { int32 id = 1; Team team = 2; Pos position = 3; }
message Pos          { int32 x = 1; int32 y = 2; }
message Turn         { repeated Update updates = 1; }

message Update {                        // oneof kind
  PlaceEntity         placeEntity         = 1;
  MoveBuilderBot      moveBuilderBot      = 2;
  RemoveEntity        removeEntity        = 3;
  DistributeResources distributeResources = 4;
  UpdateHp            updateHp            = 5;
  UpdatePlayers       updatePlayers       = 6;
  SetActionCooldown   setActionCooldown   = 7;
  SetMoveCooldown     setMoveCooldown     = 8;
  BotOutput           botOutput           = 9;
  IndicatorLine       indicatorLine       = 10;
  IndicatorDot        indicatorDot        = 11;
  FireTurret          fireTurret          = 12;
  BuilderAttack       builderAttack       = 13;
  CoreConvertAmmo     coreConvertAmmo     = 14;
  BuilderHeal         builderHeal         = 15;
  BuilderBuild        builderBuild        = 16;
}

message PlaceEntity         { Entity entity = 1; }
message MoveBuilderBot      { int32 id = 1; Pos to = 2; }
message RemoveEntity        { int32 id = 1; }
message DistributeResources { repeated ResourceMove moves = 1; }
message ResourceMove        { Pos from = 1; Pos to = 2; optional int32 resourceId = 3; }
message UpdateHp            { int32 id = 1; int32 delta = 2; }
message UpdatePlayers       { Players players = 1; }
message Players             { Player a = 1; Player b = 2; }
message Player {
  int32 titanium           = 1;
  int32 resourcesCollected = 3;
  int32 titaniumCollected  = 4;
  bytes ???                = 6;   // undeclared, unidentified — see below
  int32 ammo               = 7;
}
message SetActionCooldown { int32 id = 1; int32 value = 2; }
message SetMoveCooldown   { int32 id = 1; int32 value = 2; }
message BotOutput         { int32 id = 1; string stdout = 2;
                            uint32 execTimeUs = 3; bool tled = 4; }
message IndicatorLine     { int32 id = 1; Pos posA = 2; Pos posB = 3;
                            int32 r = 4; int32 g = 5; int32 b = 6; }
message IndicatorDot      { int32 id = 1; Pos pos = 2;
                            int32 r = 3; int32 g = 4; int32 b = 5; }
message BuilderAttack     { int32 id = 1; Pos target = 2; }
message BuilderHeal       { int32 id = 1; Pos target = 2; }
message BuilderBuild      { int32 id = 1; Pos target = 2; }
message FireTurret        { Pos from = 1; Pos to = 2; }
message CoreConvertAmmo   { Team team = 1; int32 amount = 2; }

message Entity {                  // oneof kind over the sub-messages
  int32      id         = 1;
  Team       team       = 2;
  Pos        position   = 3;
  int32      hp         = 4;
  int32      maxHp      = 5;
  BuilderBot builderBot = 10;
  Conveyor   conveyor   = 11;
  Splitter   splitter   = 12;
  Harvester  harvester  = 15;
  Barrier    barrier    = 18;
  Core       core       = 20;
  Gunner     gunner     = 21;
  Sentinel   sentinel   = 22;
  Launcher   launcher   = 24;
}                                 // 6-9, 13, 14, 16, 17, 19, 23: unused/reserved

message BuilderBot { int32 actionCooldown = 1; int32 moveCooldown = 2; }
message Conveyor   { Direction direction = 1; ResourceType stored = 2; }
message Splitter   { Direction direction = 1; ResourceType stored = 2; }
message Harvester  { int32 cooldown = 1; ResourceType resourceType = 2; }
message Barrier    { }                    // empty — zero-length on the wire
message Core       { int32 actionCooldown = 1; }
message Gunner     { Direction direction = 1; ResourceType ammoType = 2; int32 ammoAmount = 3; }
message Sentinel   { Direction direction = 1; ResourceType ammoType = 2; int32 ammoAmount = 3; }
message Launcher   { ResourceType ammoType = 2; int32 ammoAmount = 3; }

enum Team         { TEAM_A = 0; TEAM_B = 1; }
enum Direction    { DIR_CENTRE = 0; DIR_NORTH = 1; DIR_NORTHEAST = 2; DIR_EAST = 3;
                    DIR_SOUTHEAST = 4; DIR_SOUTH = 5; DIR_SOUTHWEST = 6;
                    DIR_WEST = 7; DIR_NORTHWEST = 8; }
enum ResourceType { RESOURCE_NONE = 0; RESOURCE_TITANIUM = 1;
                    RESOURCE_RAW_AXIONITE = 2; RESOURCE_REFINED_AXIONITE = 3; }
enum Environment  { ENV_EMPTY = 0; ENV_WALL = 1;
                    ENV_ORE_TITANIUM = 2; ENV_ORE_AXIONITE = 3; }
```

## Gotchas

**Round numbering: `turns[i]` IS round `i`, and rounds are 0-based.** The
visualiser prepends an empty turn (`l=[[]]` in `main-*.js`) so its scrubber
position 0 can show the pre-game state — that offset is a visualiser artefact,
not part of the file. Measured against `probe_credit`, which logs
`ct.get_current_round()` on the round it acts: `setup=HARV_OK r=5` /
`setup=CONV_OK r=7` land in `turns[5]` / `turns[7]`, and its per-round log runs
`r=0 .. r=999` over a 1000-turn replay.

**Cores are never placed by an update.** They exist only in `map.cores`; the
visualiser seeds them at 500/500 HP before replaying turn 0. A parser must do
the same or it will miss both Cores entirely — and then `removeEntity` on a Core
id (which is how `core_destroyed` matches end) has nothing to remove.

**A Core's `position` is the NW corner of its 2x2 footprint**, same convention as
`ct.get_position()` and the map editor. Footprint =
`{(x,y), (x+1,y), (x,y+1), (x+1,y+1)}`. Confirmed by the visualiser's own
delivery-target lookup, which registers a 3x3 block around `position` as
belonging to the Core — a deliberate superset of the 2x2.

**`Entity.barrier` is an empty message**, so on the wire it is a zero-length
submessage: present, but with no content. Kind detection must test for field
*presence*, not for content, or every Barrier will be misread as "no kind".

**Each team's opening Builder Bot is spawned by the bot, not the engine.** A bot
that never calls `spawn()` (e.g. `probe_idle`) emits *no* `placeEntity` at all
and finishes with zero units. "First builder_bot round" is a bot decision, not a
constant.

**One delivered stack is 10 titanium.** `DistributeResources` moves whose `to`
lands on a Core footprint tile, counted over the whole match and multiplied by
10, equal that team's final `Player.titaniumCollected` exactly — checked on 56
team-sides across 28 replays, zero mismatches. This is the cheapest available
end-to-end check that a replay parser's geometry and update handling are right.

**Absent means zero.** `resourcesCollected` / `titaniumCollected` are simply
omitted when a team banked nothing (normal proto3 default omission), so a team
that never completes a chain reads 0 — matching `fcode run --json`'s
`a_titanium_collected`.

**Damage-target law: turret fire hits the UNIT, builder attack hits the
BUILDING (research, verified 2026-08-08).** A FireTurret event's damage lands
on the UNIT standing on the target tile (builder bot or turret-as-unit), NOT
on a building occupying it; a builder's attack action damages the BUILDING on
the target tile. HP-delta-verified on 30 events in the v73 production read
(25 enemy-bot hits from turret fire, 0 own-building hits; deliverable
§self-checks). Consequence for decoders: assuming turret fire damages
buildings manufactures phantom own-building-fire events — e.g. a false
S1-guard-miss reading against a bot whose guard is actually clean. Attribute
turret damage to tile OCCUPANT (unit layer), builder-attack damage to tile
BUILDING (building layer), and verify per-game with an HP-delta ledger on
both layers.

## Undeclared fields

Two fields exist in real replays that the visualiser's schema does not declare.
They only turn up by walking the bytes and keeping unknown field numbers.

- **`Replay.winCondition` (field 6, string).** The engine writes it, the
  visualiser never reads it. Observed values: `core_destroyed`,
  `titanium_collected`, `harvesters` — the same strings `fcode run --json`
  reports as `win_condition`.
- **`Player` field 6 (length-delimited, 16-22 bytes).** Changes during a match.
  Not a nested message (its first byte decodes to field 0, which is illegal), and
  does not read as packed varints, floats, or resource ids. **Unidentified.**
  Nothing in the census needs it; noted so the next reader doesn't mistake it for
  corruption.

`Replay` fields 2 and 5 have never been observed in any replay.

## Validation

`tools/replay_census.py` was checked against three independent sources of truth:

| Check | Result |
| --- | --- |
| `probe_credit` stderr vs parsed first-build round + position | `HARV_OK r=5 harv=(1,17)` / `CONV_OK r=7 conv=(0,17) facing=SOUTH` reproduced exactly, including the `DIR_SOUTH` facing |
| `fcode run --json` vs parsed winner / turns / win_condition / titanium / titaniumCollected | exact on every field, 3 matches |
| `fcode run --json` `a_units` / `a_buildings` vs parsed per-type counts | exact on all 6 team-sides (units = builder bots + turrets; buildings = Core + Harvester + Conveyor + Splitter + Barrier) |
| `core_deliv * 10 == titaniumCollected` | 56/56 team-sides, 0 mismatches |
