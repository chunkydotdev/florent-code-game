---
tactic: (A) `transfers: no` — THE CONTRAST CASE, PRICED. Screeps gives every agent a durable JSON memory keyed to a target id, and that is what makes its plan representation possible. We cannot have it, and knowing exactly which half is unavailable stops the next session designing against it
source: https://docs.screeps.com/global-objects.html
origin: Screeps (official docs + community wiki) and Overmind, contrasted against our engine
evidence: documented
transfers: no
---

## WHAT IT IS

Screeps is the closest analogue to our engine in every respect except one: **its agents have
real memory.** The docs:

> *"Each player has access to the global object Memory in which he/she may store any
> information in the JSON format."*

and the storage discipline that makes plans survivable:

> *"Instead of storing live objects, it is better to store the id property that any game
> object has, and then use Game.getObjectById to retrieve the game object by its id"*

**Referent check.** Both are from the "Global objects" docs page; the second is from its
"Storing game objects in memory" subsection. `Memory` is the per-player persistent JSON store
described there.

**That single facility is what every Screeps plan representation in this sweep is built on.**
Overmind's `Task` serialises itself into `creep.memory` as a plain proto object —
*"* Get a serialized ProtoTask from the current task"* — carrying a target reference and a
cached position so the plan survives loss of sight:

> *"_target: { // Data for the target the task is directed to:"*
> *"ref: string; // Target id or name"*
> *"_pos: ProtoPos; // Target position's coordinates in case vision is lost"*

and a parent pointer that makes the stack:

> *"_parent: ProtoTask | null; // The parent of this task, if any. Task is changed to parent
> upon completion."*

**(All four are quoted from the whitespace-flattened source; the file aligns the comments with
tabs.)**

**And the community wiki names the failure mode that forces the plan into `Memory` rather than
onto the heap** — Global Resets:

> *"Global Resets are a byproduct of the loop architecture."*

> *"They occur when the `global` object is cleared, which causes everything that was cached in
> it to get removed."*

**Referent check.** *"They"* is Global Resets, defined in the sentence immediately before.
**So Screeps has two durability tiers — a heap that is wiped at unpredictable intervals and a
JSON store that is not — and the whole community convention is to put the plan in the durable
one.**

## WHY IT DOES NOT TRANSFER — and this is the useful part

Our engine gives us **two tiers as well, and neither is the one Screeps uses.**

| | Screeps | ours |
|---|---|---|
| durable per-agent store | `creep.memory`, arbitrary JSON, survives global resets | **none** |
| shared team store | `Memory`, arbitrary JSON, unbounded in practice | **16 unsigned 32-bit ints**, buffered one round, last writer wins, a negative write RAISES and permanently destroys the unit |
| volatile per-agent store | the `global` heap, wiped unpredictably | the `Player` instance, **survives the whole match** |
| lifetime of per-agent state | survives the creep's death (memory is keyed by name) | **dies with the unit** |
| across matches | persists | **none** |

**The three consequences, stated so nobody designs against a facility we do not have:**

1. **A serialised per-unit plan object is unavailable.** Overmind's `ProtoTask` is ~7 fields of
   arbitrary JSON per creep. We have 16 integers **for the whole team**, and the only per-unit
   storage is a dict on the `Player` instance keyed by `ct.get_id()`. That dict is *better* than
   Screeps' heap in one way — it is never spontaneously wiped — and **strictly worse in the way
   that matters: it dies with the unit and no other unit can read it.**
2. **"Store the id, not the object" is good advice we can only half take.** We can store an
   entity id. But the library measured that **ids come from one global counter shared with
   resource stacks** (97,455 of the id gaps are stack ids), so **id magnitude is meaningless**
   and a stored id tells you nothing about what it refers to once the entity is gone. Storing a
   `Position` alongside it — Overmind's `_pos … in case vision is lost` — is the transferable
   half, and it is the *only* transferable half.
3. **Anything two units must agree on has to fit through the index.** That is not a limitation
   to work around; it is the design.
   [`the-plan-lives-in-the-code-and-the-store-carries-its-index`](the-plan-lives-in-the-code-and-the-store-carries-its-index.md)
   is what you build *instead* of `Memory`, and
   [`the-blackboard-is-a-one-tick-bus-not-a-memory`](the-blackboard-is-a-one-tick-bus-not-a-memory.md)
   is why treating 16 slots as memory is the bug rather than the feature.

**And one thing our engine has that Screeps does not, which partly compensates.** Our
`Player` object is instantiated once and `run()` is called on it for every unit every round for
the whole match. **Screeps' author had to spend real engineering to stop rebuilding his object
hierarchy every tick — see
[`the-planning-layer-cost-as-much-cpu-as-executing-it`](the-planning-layer-cost-as-much-cpu-as-executing-it.md),
where making it persist cut CPU by over 40%. We get that for free.**

## WHAT WOULD KILL IT

- **Nothing — this is a rules fact, not a hypothesis.** It is filed as `transfers: no` so the
  next session does not spend a plank reinventing `creep.memory` out of 16 integers. The
  library has already measured what happens when someone tries: **the read-increment-write
  ticket idiom collapses silently, five writers producing +1 with all five believing they are
  unit #0.**
- **The one place it could be wrong is the per-unit dict.** This file asserts the `Player`
  instance survives the match and that per-unit state dies with the unit. Both follow from the
  engine's documented contract (`run()` is called per unit per round on the same class) and
  from the library's existing use of the pattern in
  [`the-goal-stack-beats-the-mode-flag`](the-goal-stack-beats-the-mode-flag.md), **but neither
  has been probed directly.** A one-round probe would settle it.

## BUILDER HOOK

None to build. The useful residue is a **checklist to apply to any plan-shaped proposal**:
does it need (a) state that outlives a unit, (b) state one unit writes and another reads within
the same round, or (c) state that survives a match? **If (a) or (c), it is impossible here. If
(b), it costs one round of latency and a single designated writer.** Anything else fits on the
`Player` instance and costs nothing.

## SOURCES QUOTED IN THIS FILE

- https://docs.screeps.com/global-objects.html
- https://wiki.screepspl.us/Global_reset
- https://raw.githubusercontent.com/bencbartlett/Overmind/master/src/tasks/Task.ts

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 18 (2026-08-09).
