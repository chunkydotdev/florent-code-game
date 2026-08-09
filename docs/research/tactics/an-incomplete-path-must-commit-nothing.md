---
tactic: (A) Structural enforcement — the placement loop reads only from a map written solely on planning success, so a partial route physically cannot leak into the world
source: https://raw.githubusercontent.com/bencbartlett/Overmind/master/src/roomPlanner/RoadPlanner.ts
origin: Overmind (Ben Bartlett), open-source Screeps AI
evidence: documented
transfers: yes
---

WHAT IT IS — Overmind's road planner pathfinds first and **returns without
recording anything** if the path is incomplete:

> *"const ret = PathFinder.search(origin, {pos: destination, range: 1}, {roomCallback: callback, maxOps: 40000});"*

> *"if (ret.incomplete) {"*

> *"log.warning(`Roadplanner for ${this.colony.print}: could not plan road path!`);"*

> *"return;"*

The part that makes it an **invariant rather than a good intention** is the data
flow, not the check: construction sites are created only from `this.memory.roadLookup`,
and `roadLookup` is written only by `finalize()`, which runs only after a complete
plan. **A failed path contributes zero positions, so no partial route can reach
`createConstructionSite` even by accident.** The same file also refuses to commit a
base layout that collides with terrain, in `RoomPlanner.finalize()`:

> *"log.warning(`Invalid layout: collision detected at ${collision.print}!`);"*

WHY IT MIGHT TRANSFER — against OUR ruleset specifically:

- **Our failure is the leak this design prevents.** `DEAD_END_GROUND` is 39.6% of
  our blocked mass, and 33.4% of all blocked mass is a line of which the source doc
  says *"it ends on ground where nothing was ever built"* — a route that was started and never finished.
  Overmind's answer is not to detect that state, it is to make it unreachable.
- **The transferable primitive is the separation, not the check.** In our bot the
  equivalent is: **the decision "is this route valid" and the action "place a
  conveyor" must not be the same code path.** A builder should read a validated
  route intent and lay tiles from it; it should not decide tile-by-tile as it
  walks. That distinction is exactly what the Screeps community names as a trap —
  see [`laying-road-where-a-unit-happens-to-walk-is-a-named-trap`](laying-road-where-a-unit-happens-to-walk-is-a-named-trap.md).
- **Overmind also orders the placement so a partly-funded route is contiguous**,
  sorting positions nearest-to-storage first (`roadPositions = _.sortBy(roadPositions, pos => pos.getMultiRoomRangeTo(origin));`).
  In our ruleset a contiguous partial line from the CORE outward is strictly better
  than one from the harvester outward, because **a corked line holds a stack and
  blocks everything upstream** while an unfinished line built core-first simply has
  not reached the ore yet. **Build direction is a free variable we are not using.**

WHAT WOULD KILL IT —

- **We have no `Memory`.** Overmind's invariant is enforced by a persistent
  per-colony object. Ours is 16 buffered unsigned ints, last-writer-wins, shared by
  every unit — **it cannot hold a route.** Any transfer must either recompute the
  route each time it is needed (CPU) or encode a route as something tiny (a
  direction-per-region scheme), and neither is demonstrated here.
- **`maxOps: 40000`.** Overmind is spending a pathfinding budget we do not have.
  Our whole turn is 10 ms for everything the unit does.
- **A route that is invalid *now* may be the only route.** Overmind can decline to
  build and try again in 1000 ticks. A harvester with no output is producing
  nothing meanwhile; **declining to build is not free for us**, and the binding-tile
  cut's `NO_OUTPUT_BUILT` at 15.9% is what "no output at all" costs. A refusal
  predicate with no fallback would move mass from one class to another rather than
  recovering it. **Any implementation needs a fallback, and this source has none.**

BUILDER HOOK — the smallest safe version is a *build-order* change, not a refusal:
when a builder decides to start a new line, **lay it from the core end toward the
ore, not from the ore toward the core.** Cost: reordering an existing loop. It
converts every unfinished line from a cork into a stub, and it is measurable as a
mechanism counter (share of our conveyor builds whose forward walk already reaches
the core at the moment of placement — should go from near-zero to near-one).
