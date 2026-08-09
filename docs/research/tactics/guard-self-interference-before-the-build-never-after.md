---
tactic: (D) THE ANSWER TO SUB-QUESTION (D) — self-interference is guarded prophylactically and locally at placement time. NOBODY in this sweep detects it after the fact
source: https://raw.githubusercontent.com/bencbartlett/Overmind/master/src/roomPlanner/RoomPlanner.ts
origin: Overmind (Screeps); NoNoCAB, CluelessPlus and AdmiralAI (OpenTTD NoAI); plus a Screeps forum bug report, https://screeps.com/forum/topic/2200/don-t-let-me-build-roads-on-top-of-walls
evidence: documented
transfers: yes
---

WHAT IT IS — five independent implementations, one pattern: **check ownership and
purpose of the target tile before you commit, and plan the route around what you
have already decided to build.**

**Overmind plans the road network around the planned buildings, before either
exists.** The whole rule is one array:

> *"getObstacles(): RoomPosition[] {"*

> *"const passableStructureTypes: string[] = [STRUCTURE_ROAD, STRUCTURE_CONTAINER, STRUCTURE_RAMPART];"*

Everything in the layout that is not one of those three is fed to the road
planner's cost matrix. It also removes its own misplaced work:

> *"private removeMisplacedConstructionSites() {"*

**NoNoCAB geometrically separates the two ends of a bidirectional route so it does
not shadow itself:**

> *"// In the case of a bilateral connection we want to make sure that"*

> *"// we don't hinder ourselves; Place the stations not to near each"*

> *"// other."*

**CluelessPlus refuses to demolish road with its own vehicle standing on it**, and
refuses to demolish its own depot while repairing:

> *"// There is a non-crashed vehicle in the first of two tiles to remove -> wait so it does not get stuck"*

> *"continue; // don't demolish our own depot!"*

**AdmiralAI removes every company-owned tile from its demolition candidate set
before it starts:**

> *"/* We don't want to delete our own tiles (as it could be stations or necesary roads)"*

> *"* and we can't delete tiles belonging to the competitors. */"*

**And the one report of self-interference being found the hard way describes it as
invisible**, which is why prophylaxis is the pattern:

> *"I had an insidious bug today where my creeps were trying to path through walls and I determined it was because my remote mining code was building roads on some walls. It's really hard to see these roads in the GUI when they are built on top of walls. Having roads on top of walls makes building cost matrices difficult, because you can't just iterate over room.find(FIND_STRUCTURES) and set the matrix entries like the example in the docs suggests."*

The two remedies proposed in that thread are a periodic sweep — *"I just have a
script that deletes my roads under unwalkable structures."* — and a pre-placement
check. **Nobody proposed detecting the bad state from its consequences.**

WHY IT MIGHT TRANSFER — against OUR ruleset specifically:

- **It validates the shape of the plank already in prereg.** LOKI-10 refuses to
  emplace a turret or barrier on a tile a friendly conveyor faces. **That is
  AdmiralAI's ownership guard and Overmind's obstacle set, arrived at
  independently.** The field agrees on the *form*; this file adds no new evidence
  about the *effect*.
- **The direction that plank does NOT cover is the one Overmind covers.** The
  binding-tile cut's §8.5 measured that the co-occurrence arises two ways, and the
  refusal catches only **70% of v102's events and 52% of the Eir archive**: turrets
  built onto an already-faced tile, versus **conveyors built later, aimed at an
  existing friendly turret** (23 and 607 events respectively). **Overmind's
  mechanism catches the second direction, because the road planner treats the
  planned buildings as obstacles rather than the other way round.** Our equivalent:
  a conveyor's facing must not be chosen to point at a friendly turret, barrier or
  harvester. **That is a second refusal, cheap, and it closes the half the prereg
  leaves open.**
- **`INTO_HARVESTER` at 5.64% is the same bug in a third form** — a harvester never
  accepts a stack, so a conveyor facing one is a terminus. **One predicate covers
  all three: the tile a conveyor faces must be able to receive.**

WHAT WOULD KILL IT —

- **⚠ Every one of these guards is prophylactic and none is measured.** No author
  reports what their guard bought. This file establishes that the field does it,
  not that it works — and our own arena cannot tell us either, because the
  turret-siting refusal's outcome channel is closed in 93% of v102 games.
- **A refusal with no fallback moves mass rather than removing it.** If a builder
  refuses every legal facing it will build nothing, and `NO_OUTPUT_BUILT` is already
  15.9% of our blocked mass. **Each refusal must name what it does instead.**
- **Overmind's version needs a persistent plan and we have 16 buffered ints.** The
  transferable part is the *ordering* — decide the route first, then site turrets —
  which we can approximate only if route intent survives across rounds. **It does
  not today.**

BUILDER HOOK — the complement to the existing prereg, and it is symmetric with it:
**a conveyor may not be built facing a tile that holds a friendly turret, barrier or
harvester.** Mechanism counter, directly comparable to the numbers the corpus
already produced: *conveyors built aimed at an existing friendly turret/barrier* —
**607 events across the Eir archive, 23 in v102** — should go to zero in the
treatment arm.
