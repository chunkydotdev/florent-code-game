---
tactic: (C) Keep infrastructure completeness as ONE NUMBER that other subsystems read and branch on — not as a fact you check when you happen to look
source: https://raw.githubusercontent.com/bencbartlett/Overmind/master/src/overlords/core/transporter.ts
origin: Overmind (Ben Bartlett), open-source Screeps AI; the scalar is computed in https://raw.githubusercontent.com/bencbartlett/Overmind/master/src/roomPlanner/RoadPlanner.ts
evidence: documented
transfers: yes
---

WHAT IT IS — Overmind maintains `roadCoverage`, the fraction of the path from
storage to each destination that is actually roaded, as a persisted scalar:

> *"roadCoverage : 0.0,"*

> *"get roadCoverage(): number {"*

> *"return this.memory.roadCoverage;"*

**And then a completely different subsystem branches on it.** The transporter
overlord sizes the body of every hauler it spawns from how finished the road is:

> *"const ROAD_COVERAGE_THRESHOLD = 0.75; // switch from 1:1 to 2:1 transporters above this coverage threshold"*

> *"const setup = this.colony.roomPlanner.roadPlanner.roadCoverage < ROAD_COVERAGE_THRESHOLD"*

> *"? Setups.transporters.early : Setups.transporters.default;"*

That is the whole idea: **infrastructure completeness is promoted from an
implementation detail of the builder into a first-class colony-wide signal.**

WHY IT MIGHT TRANSFER — this is, in my judgement, the strongest single item in
sweep 19, and the reason is our store:

- **It compresses to one small non-negative integer, which is precisely the one
  thing our 16-slot store is good at.** Sweep 18's finding on the locker-room
  agreement applies verbatim: **last-writer-wins is harmless when all writers agree,
  and the one-round buffer is harmless for a slowly-moving index.** A percentage
  0-100 in one slot is safe under every measured hazard of that store, including the
  negative-write raise.
- **Any unit can compute a local contribution and any unit can read the aggregate.**
  A builder that walks a chain (see
  [`verify-connectivity-after-building-not-only-before`](verify-connectivity-after-building-not-only-before.md))
  knows one route's verdict. The core, which sees r²=36 and runs every round, is the
  natural writer.
- **We have a decision that should branch on it and currently does not.** The
  binding-tile cut measures **58.8% of our surviving harvesters directed-connected
  against 74.3% for our opponents in the same games**, and our own turrets terminate
  11.1% of our blocked mass. **A bot that knew its own coverage was low could stop
  building new harvesters and new conveyors and spend the builder-rounds on the
  existing lines instead.** Today nothing in our bot can express "the network is in
  bad shape", so nothing can react to it.
- **The threshold shape is the right one for us.** Overmind does not act on the
  scalar continuously; it uses a single constant to pick between two behaviours.
  That is sweep 18's synthesis — *what lost everywhere is a sequence, what won is a
  mode* — arriving independently in a logistics subsystem.

WHAT WOULD KILL IT —

- **A number nobody acts on is pure cost.** Overmind's scalar earns its keep
  because a specific consumer changes a specific decision at 0.75. **If we ship the
  scalar without naming the consumer and the threshold in advance, it is
  instrumentation dressed as a plank.** Name both, or do not build it.
- **The threshold is not ours.** 0.75 is Overmind's constant, tuned for Screeps
  hauler bodies, and its author publishes no derivation. **Do not import the
  number.** Our own distribution — median directed-connected 58.8%, per-team field
  spread min 0 / med 48 / max 100 — says nothing about where a useful cut point is.
- **The aggregate can hide the mixture, which is the failure mode this library
  keeps hitting.** The binding-tile cut's §4 is explicit that our saturation share
  is 14.3% pooled and 0.1% at the median team-side. **A single coverage scalar
  averaged over routes will do the same thing to route health** — one dead route
  among four reads as 75% and looks fine. **The per-route version is the honest one
  and it does not fit in a store slot.** This is a real, unresolved objection.
- **Writes are visible next round.** Every consumer reads a one-round-stale value.
  For a slowly-moving structural fact that is fine; for anything reactive it is not.

BUILDER HOOK — two steps, and the first is free. **(1)** Have the core compute,
each round, the fraction of our living harvesters whose chain reaches a core
footprint tile *within the core's own vision*, and write it to one store slot as an
integer 0-100. Log it. **That alone gives a live in-game number comparable to the
corpus's 58.8%, from a third independent instrument.** **(2)** Only after (1) has
been observed for a while, name one consumer and one threshold — the obvious
candidate is: below T, a builder prefers repairing or terminating an existing line
over starting a new harvester. Gate the leg on the mechanism counter
(conveyor builds that complete a route), never on Elo.
