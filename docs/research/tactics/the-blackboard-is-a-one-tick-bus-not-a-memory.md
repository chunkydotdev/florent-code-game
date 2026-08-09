---
tactic: (A) THE CORRECTION THAT CHANGES HOW WE SHOULD THINK ABOUT OUR 16 INTS — the field's one real blackboard is WIPED every planning tick on purpose. It is a communication bus, not a memory, and separating "what I decided this tick" from "what I am committed to" is the design rule
source: https://raw.githubusercontent.com/dgant/PurpleWave/master/src/Planning/Blackboard.scala
origin: PurpleWave (StarCraft AI, 1st SSCAIT 2018-19 and 2019-20, 3rd AIIDE 2025)
evidence: documented
transfers: yes
---

## WHAT IT IS

A blackboard is the textbook shared-state plan representation, and the sweep looked for one
across five leagues. **Across the Battlecode corpus, Screeps docs and wiki, Overmind,
TooAngel, Steamhammer, UAlbertaBot and CommandCenter, the literal strings `blackboard`,
`behavior tree` and `behaviour tree` return zero hits.** Exactly one bot in the sweep has a
blackboard: PurpleWave. And it is wiped every planning tick.

Every property on it is registered through an `add(...)` that also registers a reset:

> *"def reset(): Unit = { resets.foreach(reset => reset()) }"*

**(Quoted from the whitespace-flattened source; the file spreads this over four lines.)**

`With.blackboard.reset()` is called by the global task queue immediately **before** the
gameplan updates and before the production timeline is simulated. So nothing written to the
blackboard survives to the next planning tick.

**The commitment lives somewhere else, and the split is explicit.** The multi-step production
timeline is a pure re-derivation — `MacroSim.simulate()` begins by clearing its step buffer
(`steps.clear()`) and rebuilding from live game state. But the *execution objects* persist,
and the sunk cost is handled in **one line**:

> *"// Requeue any paid-for production, in the same order"*
> *"_queueNext ++= _queueLast.view.filter(_.hasSpent)"*

**Referent check.** `_queueLast` and `_queueNext` are the two production lists; `launch()`
rotates one into the other each tick. Anything with `hasSpent` is carried over
**unconditionally, before any matching against the freshly re-derived request list.** So a
build that has already been paid for can never be dropped because the re-derivation changed
its mind.

## WHY IT MIGHT TRANSFER

**Our 16-integer store IS a one-round bus, and this file says that is the correct shape rather
than a limitation to work around.**

- **The engine already implements the reset for us, in a stricter form.** Writes are buffered
  and visible only next round, so every unit reads a consistent snapshot for the whole round.
  That is exactly PurpleWave's discipline — publish what you decided, read what everyone
  decided, do not treat it as memory — **enforced by the engine instead of by a convention.**
- **It reframes the store's known hazards.** Last-writer-wins is a defect *if* the store is a
  memory and a non-issue *if* it is a bus carrying a value all writers agree on. The library's
  own measured failure — the read-increment-write ticket idiom collapsing silently, five
  writers producing +1 with all five believing they are unit #0 — **is precisely the failure
  of treating a bus as a memory.**
- **The rule "commitment lives in the committing object, not on the blackboard" has a direct
  translation.** Anything a unit is committed to belongs on the `Player` instance keyed by
  `ct.get_id()`; anything the team must agree on this round belongs in a slot; **and nothing
  belongs in both.** Our bot does not currently state which is which.
- **The `hasSpent` line is the one-line sunk-cost rule we lack.** Our nearest analogue is
  sharper than his: `destroy()` refunds nothing and cost scale is one global additive team
  factor, so **titanium already spent toward an intention is unrecoverable, and any
  re-derivation that abandons it has thrown it away.** A "keep anything already paid for"
  guard is one condition.

## WHAT WOULD KILL IT

- **PurpleWave's blackboard is re-derived at least every 7 frames, not every frame** — its
  task queue is declared with a skip allowance — whereas our store's cycle is fixed at one
  round by the engine. That is a difference in *rate*, and it means his consumers tolerate
  stale reads in a way ours must not.
- **A bus cannot carry anything a unit needs to remember alone.** The per-unit half of every
  plan file in this sweep (target caches, previous state, progress timestamps) must live on
  the `Player` instance, and **it dies with the unit.** Screeps solves that with real
  persistent memory; we cannot, and no amount of discipline about the store fixes it.
- **Our store is 16 unsigned 32-bit slots and a negative write RAISES**, permanently
  destroying the unit. PurpleWave's blackboard has ~24 typed properties of arbitrary type.
  **The analogy is about lifetime, not capacity**, and should not be stretched into "we have
  a blackboard".
- **No measurement.** This is a design read off shipped source, plus the sweep's own
  zero-hit greps for `blackboard` elsewhere. Evidence is `documented` for the design.

## BUILDER HOOK

Not a build — a **one-page audit with a real deliverable**: enumerate every store slot the bot
currently uses and classify each as *bus* (a value recomputed each round by whoever writes it,
where last-writer-wins is harmless) or *memory* (a value accumulated across rounds, where
last-writer-wins is a bug). **Any slot in the second class is a latent instance of the ticket
bug the library already measured**, and finding one costs nothing but reading our own code. If
the audit finds none, the finding is that our store is already used correctly, which is worth
knowing.

## SOURCES QUOTED IN THIS FILE

- https://raw.githubusercontent.com/dgant/PurpleWave/master/src/Planning/Blackboard.scala
- https://raw.githubusercontent.com/dgant/PurpleWave/master/src/Macro/Scheduling/MacroSim.scala
- https://raw.githubusercontent.com/dgant/PurpleWave/master/src/Tactic/Production/Produce.scala

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 18 (2026-08-09). The zero-hit results for `blackboard`,
`behavior tree` and `behaviour tree` were produced by this sweep's Battlecode/Screeps and
StarCraft-source discovery legs across the corpora they list; I re-ran the greps for
`behavior tree`, `behaviour tree` and `blackboard` against the Battlecode PDFs I downloaded
myself and confirmed zero hits there.
