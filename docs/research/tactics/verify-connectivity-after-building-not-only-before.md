---
tactic: (A) Do not trust that a sequence of successful build calls produced a connected route — re-walk the stored tile list afterwards and patch the gaps
source: https://raw.githubusercontent.com/Wormnest/nonocab/master/pathfinding/pathbuilder.nut
origin: NoNoCAB (Wormnest, successor to NoCAB), OpenTTD NoAI competitive AI; API semantics from https://docs.openttd.org/ai-api/classAIRoad.html
evidence: documented
transfers: yes
---

WHAT IT IS — the complement to
[`test-build-the-whole-route-before-laying-one-tile`](test-build-the-whole-route-before-laying-one-tile.md),
and the one that fits our constraints better. NoNoCAB's path builder declares the
invariant in its own interface comment:

> *"Check if the complete road is build."*

and enforces it at the commit point in `RealiseConnection` — **a build that
returned success but did not connect is treated as a failure**:

> *"if (result && !CheckPath(roadList)) {"*

> *"Log.logWarning("Path was built but with errors!");"*

`CheckPath` is a forward walk over the stored tile list that re-asserts adjacency
tile by tile and repairs any gap it finds:

> *"for (local i = 1; i < roadList.len() - 1; i++) {"*

> *"if (!AIRoad.AreRoadTilesConnected(tile, nextTile) && !BuildRoadPiece(nextTile, tile, Tile.ROAD, 1, false))"*

> *"return false;"*

**Why the walk is necessary rather than lazy, and this is the finding that
transfers:** the NoAI API has no global reachability query. The only connectivity
primitive is adjacency-scoped, and the organisers' reference says so — the
referent of *"the given tiles"* is the `tile_from` / `tile_to` pair the method
takes:

> *"Checks whether the given tiles are directly connected, i.e. whether a road vehicle can travel from the center of the first tile to the center of the second tile."*

> *"'tile_from' and 'tile_to' are directly neighbouring tiles."*

WHY IT MIGHT TRANSFER — against OUR ruleset specifically:

- **Our `Controller` has exactly the same shape of gap.** We can ask
  `get_tile_building_id(pos)` and `get_direction(id)` — adjacency and facing, one
  tile at a time. **There is no `does_this_reach_the_core()`.** So, as in OpenTTD,
  whole-route validity can only be established by walking it, and the walk is the
  only instrument available.
- **It needs no persistent plan.** This is the decisive advantage over the
  test-build pattern for us: `CheckPath` walks a *stored list*, but the same
  invariant can be re-derived from the map alone, because **a conveyor's facing is
  readable**. A builder standing next to a conveyor can follow `get_direction`
  forward and find out where the chain ends, with no memory, no store slot, and no
  cross-round state. **Our 16-int buffered store is the reason the test-build
  pattern is awkward here and this one is not.**
- **It is the exact instrument our own corpus already uses offline.**
  `tools/replay_census.py`'s `chain_dir` walks conveyor facings to a core footprint
  tile and, on 28 replays / 56 team-sides, is documented in that file as *"the
  sharper predictor of whether the team actually banked titanium"* with *"0 false
  positives against 7 for the undirected number"*. **We already trust this walk
  post-hoc; we do not run it in the bot.**
- **NoNoCAB's escalation is worth copying too** — it repairs the gap in place
  rather than abandoning the route, and it treats endpoints as non-negotiable while
  the middle is deferrable (`pathbuilder.nut` comments the *"very first and last
  piece"* as critical). Our endpoints are the harvester's output tile and the tile
  orthogonally adjacent to the core footprint — the two places our binding-tile cut
  finds most of the mass (`NO_OUTPUT_BUILT` 15.9%; and the terminus classes).

WHAT WOULD KILL IT —

- **Vision.** A builder can only walk the part of the chain it can see (r²=20). A
  chain longer than that cannot be validated by one unit in one round. The
  measured median is 3 hops, so this bites on the tail, not the median — but the
  tail is where the worst corks may live and this file does not measure that.
- **CPU.** The walk is O(chain length) `get_tile_building_id` + `get_direction`
  calls per candidate. At 10 ms per unit per turn it must be bounded by a hop cap
  and must not run for every builder every round.
- **`get_direction` raises.** The organisers' reference documents it as returning the
  facing of a conveyor, splitter or turret *"(raises if entity has no direction)"* —
  so a harvester, barrier or core on the chain will throw,
  and **an uncaught exception permanently destroys that unit for the match.** Any
  implementation of this walk must branch on `get_entity_type` before calling
  `get_direction`, or it is a unit-killer. **That is the single most likely way
  this idea goes wrong in practice, and it is a bigger risk than the CPU.**

BUILDER HOOK — a pure function, no behaviour change, testable in isolation:
`chain_reaches_core(ct, pos, max_hops)` → walk forward from `pos` following
friendly conveyor/splitter facings, type-checking every entity before reading its
direction, returning `True` / `False` / `UNKNOWN` (walked out of vision or hit the
hop cap). **Ship it as an instrument first** — have builders `print()` the verdict
for adjacent conveyors and diff the replay against `chain_dir`'s 58.8%. Two
independent instruments agreeing is worth more than either alone, and this one
costs nothing to be wrong about.
