---
tactic: The ancestor's API is deliberately split into TOTAL predicates that can never throw and PARTIAL getters that can — `canSenseLocation` exists precisely so the guard is a boolean, not a try/catch. Ours has the same split, and I measured exactly where the line falls
source: https://raw.githubusercontent.com/battlecode/battlecode25/master/engine/src/main/battlecode/common/RobotController.java
origin: MIT Battlecode 2025 engine API (repo `battlecode/battlecode25`, branch `master`, `engine/src/main/battlecode/common/RobotController.java`)
evidence: documented
transfers: yes
---
WHAT IT IS — Battlecode does not leave "is this query legal" to exception handling. It
ships a boolean twin for every partial sensing method. The twin's contract is that it is
**total** — it answers for any location, including off-map ones
(`RobotController.java:167-177`, verbatim source lines; the sentence is split across
javadoc lines by `*` markers, so it is reproduced with its own line breaks):

```java
    /**
     * Checks whether the given location is within the robot's vision range, and if
     * it is on the map.
     *
     * @param loc the location to check
     * @return true if the given location is within the robot's vision range and is
     *         on the map; false otherwise
     *
     * @battlecode.doc.costlymethod
     */
    boolean canSenseLocation(MapLocation loc);
```

Its partial partner, immediately below, throws (`RobotController.java:208` and `:212`):

> *"@throws GameActionException if the location is not within vision range"*

```java
    RobotInfo senseRobotAtLocation(MapLocation loc) throws GameActionException;
```

The same pairing runs through the whole class: `canSenseRobot(int id)` / `senseRobot(int id)`,
`canSenseLocation` / `senseMapInfo` / `sensePassability` / `isLocationOccupied`.

WHY IT MIGHT TRANSFER — **our engine has the identical split, and I measured every member
of both halves** (`bots/_probe_oov_surface`, `maps/eider.map26`, seed 1, four builder bots
at four different positions, all four agreeing):

| call, on a tile 185–521 dist² away (vision r²=20) | result |
| --- | --- |
| `is_in_vision(far)` | **`False` — never raises** |
| `is_in_vision(oob)` *(off-map, x=w+5)* | **`False` — never raises** |
| `can_build_barrier(far)`, `can_build_conveyor(far, N)` | **`False` — never raises** |
| `can_heal(far)`, `can_destroy(far)`, `can_fire(far)` | **`False` — never raises** |
| `get_tile_env(far)` | `GameError: Position out of vision range` |
| `is_tile_empty(far)`, `is_tile_passable(far)` | `GameError: Position out of vision range` |
| `get_tile_building_id(far)`, `get_tile_builder_bot_id(far)` | `GameError: Position out of vision range` |
| `get_tile_env(oob)`, `is_tile_empty(oob)` *(off-map)* | `GameError: Position out of vision range` |

**`is_in_vision(pos)` is our `canSenseLocation`: total over every `Position`, on-map or
not, and the single legality mask for the entire `get_tile_*` / `is_tile_*` family.** The
whole `can_*` family is total too — it is safe to ask "can I build here" about a tile you
cannot see, and the answer is always `False`.

That decides sub-question (B) for us in the ancestor's own idiom: **guard the query with a
boolean, and keep the catch-all only as the backstop.** Two layers, different jobs. The
catch-all exists for the bug you did not anticipate
([`catch-everything-at-the-top-of-run`](catch-everything-at-the-top-of-run.md)); the mask
exists so the anticipated case never reaches it.

**This is the plank-enabling half of our 7.08% measurement.** 7.08% of the graph walks we
need exceed a builder's r²=20 and only 53.67% fit the core's r²=36. A walk written as
`while is_in_vision(p): step` terminates on the mask instead of on an exception, and the
walk's own termination condition becomes "I ran out of sight", which is a *fact the walker
can act on* rather than a crash.

WHAT WOULD KILL IT —

- **The mask is per-unit and re-evaluated every call.** `is_in_vision` answers for *this*
  unit, so a mask precomputed by one builder is worthless to another and worthless to
  itself after it moves. There is no cacheable team-level legality mask, because there is
  no team-level anything — see
  [`the-sixteen-ints-really-are-the-only-channel`](the-sixteen-ints-really-are-the-only-channel.md).
- **It does not tell you the tile is EMPTY, only that you may ask.** `False` collapses
  UNKNOWN and OUT-OF-BOUNDS into one value. Any representation built on it must keep that
  distinction itself.
- **It is an enabler, not a plank.** It buys no core-kill share directly. Its currency is
  "walks that terminate instead of killing the walker", which the programme does not score.

BUILDER HOOK — one helper, and make it the only way the codebase reads a tile:

```python
def tile(ct, p):
    return ct.get_tile_env(p) if ct.is_in_vision(p) else None
```

Then `grep -n "get_tile_env\|is_tile_empty\|is_tile_passable\|get_tile_building_id" bots/_v127loki10/` must return
only the helper's own line. That grep is the test, and it is checkable in CI without
running a match.
