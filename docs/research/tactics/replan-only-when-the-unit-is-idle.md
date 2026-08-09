---
tactic: (B) THE ANSWER TO OUR 10 ms BUDGET — pay the expensive decision once, then pay only a cheap validity check each round. The Screeps community has a name for it and states CPU, not decision quality, as the reason
source: https://wiki.screepspl.us/Target_lock
origin: Screeps community wiki; Overmind (Screeps); Halite III winner teccles and Battlecode 2026 "food"
evidence: documented
transfers: yes
---

## WHAT IT IS

**The Screeps wiki names the technique and states its purpose in one sentence:**

> *"Target locking is a CPU saving technique where you cache the most optimal target for an
> object to move to or perform any action on, amortizing the cost of the selection process
> over a longer period of time."*

and, of the per-tick check that replaces the per-tick selection:

> *"This step is typically less CPU intensive than the initial selection."*

**Referent check.** *"This step"* is **Target validation**, which is the heading directly
above the sentence; the page names the loop's four steps as target selection, target caching,
target recovery, target validation.

**Overmind implements it as a one-line gate.** From `src/zerg/Zerg.ts`:

> *"get isIdle(): boolean { return !this.task || !this.task.isValid(); }"*

and the runner only calls the (expensive) task assignment when that is true —
`if (creep.isIdle) { … taskHandler(creep); } creep.run();`. **The author states the economics
himself:**

> *"since a creep only needs to request a new task when its old one becomes invalid"*

**Referent check.** The clause is the tail of *"Tasks are generally pretty good and minimize
much of the decision-tree overhead that many AI's feature, since a creep only needs to request
a new task when its old one becomes invalid."* — *"Tasks"* being the Task objects in his own
Overmind codebase, listed among the things he likes about his AI.

**One interrupt is deliberately allowed to bypass the gate.** In `autoRun`, a `fleeCallback`
runs *before* the idle check and `continue`s past task execution entirely. **Flee is the only
thing permitted to override a committed plan.**

**Two other leagues arrive at the same gate without any task machinery.** Halite III's winner:

> *"When ships start to return towards a dropoff or a shipyard, they carry on until they get
> there."*

And Battlecode 2026's team `food`, whose state machine is otherwise re-derived from scratch
every turn:

> *"Once we reach a destination or switch states, we choose a new target based on state:"*

**Referent check.** *"we"* is an individual baby rat evaluating itself; the sentence heads
the "Target Destination" section. **The target is recomputed only on arrival or on a state
change — the commit gate expressed without a single object.**

## WHY IT MIGHT TRANSFER

**This is the only file in the sweep whose primary argument is CPU, and CPU is the constraint
our engine enforces most brutally.**

- **10 ms per unit per turn, and exceeding it silently discards that unit's turn** — no
  exception, no log, no signal. Our own corpus measured Ouroboros discarding **26,356
  unit-turns across 85 games (max 3,508 in one game)** to exactly this limit. A per-round
  full re-scoring of every candidate seat by every builder is the shape that produces that.
- **The validity check is far cheaper than the selection here, by a larger factor than in
  Screeps.** Selecting a turret seat means scoring many tiles with `can_build_*` and
  `can_fire_from`; validating the chosen one means calling `can_build_*` **once**.
- **It composes with everything else the sweep found.** The gate is `not valid` — and
  [`a-plan-step-carries-its-own-termination-condition`](a-plan-step-carries-its-own-termination-condition.md)
  supplies the predicate, [`abandon-the-plan-on-a-progress-timeout`](abandon-the-plan-on-a-progress-timeout.md)
  supplies the backstop, and the flee exception is the one interrupt our own bot already has
  (the core-damage heal pull).
- **It needs no store slot.** The cached target lives on the `Player` instance keyed by
  `ct.get_id()`.

## WHAT WOULD KILL IT

- **A cached target that outlives its validity is exactly the bug this library already has a
  case study for.** Battlecode 2026 Lorem Ipsum: *"each time a target changed, the code was
  supposed to reset bugging"* — persisted low-level state not invalidated when the high-level
  goal changed, and his own diagnosis of why his bot did badly on maze maps. **Cache
  invalidation is the whole cost of this technique.**
- **Our vision is narrower than Screeps'.** A creep can query rooms; our builder sees r²=20.
  A target cached from a position the unit has since left may be unverifiable — which is why
  Overmind's task settings include `blind : true,  // don't require vision of target unless
  in room` and store a saved position: `_pos: ProtoPos; // Target position's coordinates in
  case vision is lost`. We would need the same explicit decision about what "cannot see it"
  means. (Both are quoted from the whitespace-flattened source; the file aligns them with
  tabs.)
- **It is a commitment device and inherits commitment's failure mode.** A unit locked to a
  target it should have abandoned is the mirror image of a unit that thrashes. The two
  failures are opposite and the same file cannot cure both.
- **CPU is not currently our measured bottleneck.** The library records **we sit at 0.00%
  discarded unit-turns**, as does every 1800+ team. **So this is insurance against a cost we
  do not yet pay** — which makes it a prerequisite for anything expensive, not a gain on its
  own.

## BUILDER HOOK

Smallest test: instrument, do not change. Call `ct.get_cpu_time_elapsed()` immediately before
and after the target-selection block for one unit class and `print()` the microseconds. **Read
the distribution off the replay.** If selection is a small fraction of 10,000 µs, target
locking buys nothing today and the file is filed as insurance. If it is a large fraction, the
gate is four lines: cache the target on `self`, validate with one `can_build_*`, and reselect
only when validation fails — with the core-damage heal pull kept as the one bypass, mirroring
Overmind's `fleeCallback`.

## SOURCES QUOTED IN THIS FILE

- https://wiki.screepspl.us/Target_lock
- https://raw.githubusercontent.com/bencbartlett/Overmind/master/src/zerg/Zerg.ts
- https://raw.githubusercontent.com/bencbartlett/Overmind/master/src/tasks/Task.ts
- https://bencbartlett.github.io/blog/screeps-0-a-brief-history-of-game-time/
- https://raw.githubusercontent.com/teccles-halite/halite3-bot/master/README.md
- https://www.alext.app/Battlecode_Postmortem_2026.pdf
- https://battlecode.org/assets/files/postmortem-2026-lorem-ipsum.pdf

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 18 (2026-08-09).
