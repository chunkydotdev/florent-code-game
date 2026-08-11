---
tactic: The withdrawal check runs AFTER the task check, not before it — an unconditional threshold aborts work already paid for
source: https://battlecode.org/assets/files/postmortem-2025-om-nom.pdf
origin: Battlecode 2025, om nom
evidence: documented
transfers: yes
---

## WHAT IT IS

om nom's postmortem lists this as improvement #1 of a numbered list, under the
heading of what they changed:

> *"Soldiers should not blindly prioritize going home"*
> *"the soldiers went home unconditionally at around 50 paint to refuel. This would lead to disastrous scenarios where we would barely get to a tower and then retreat without using roughly 10 attacks! Changing the priority meant that we killed towers with much higher odds."*
> *"The same logic was applied to finishing towers and SRPs before going home, if possible."*

**Referent check.** "the soldiers" are om nom's own soldiers; "a tower" is the
*enemy* tower they walked across the map to attack; "roughly 10 attacks" is the
work the unconditional threshold discarded. The failure is not that the threshold
was mistuned — it is that **the threshold was evaluated before the task**, so the
unit spent the entire travel cost and then left without collecting the payload.

## WHY IT MIGHT TRANSFER — the arithmetic is worse for us than for them

om nom threw away ~10 attacks after a walk. Our equivalent unit throws away a
**build**, and our travel is priced in a currency om nom's is not:

* A builder's **act and move are mutually exclusive per turn**, so every tile of
  the walk is one forgone build. The sunk cost of arriving is denominated in the
  same unit as the payload.
* The payload is often **one action** — `build_conveyor` / `build_harvester` /
  `build_gunner` on an orthogonally adjacent tile. An abort one round short of
  that converts the entire errand into zero.
* Our `GIVEUP_RND = 180`-shaped literals are exactly the *"unconditional"*
  construct om nom names: they fire on a global clock with no reference to
  whether the unit is one turn from placing a structure.

**The rule in one line: a dwell limiter must be dominated by
`can_build_<x>(target)` being true.** If the unit could act this turn, it acts;
the limiter is only consulted when it could not.

## WHAT WOULD KILL IT

* **A pathological "one turn from the payload, forever" state.** If the target is
  permanently unbuildable (an enemy body parked on the tile), a
  finish-first rule with no progress term never fires. The fix is a **stall
  counter that resets on progress**, which this library already holds as the
  universal primitive
  ([`the-stuck-counter-is-the-universal-primitive`](the-stuck-counter-is-the-universal-primitive.md))
  — and which our incumbent already has as `self.raid_stalls`
  (`bots/_v135loki18/main.py:90`).
* om nom's fix is reported as a design change with an outcome sentence, **not with
  a number.** `evidence: documented`, effect size unknown.

## BUILDER HOOK

Reorder, do not retune. In the raid arm, evaluate whether a legal build target is
adjacent right now **before** any round-count limiter, and let the limiter fire
only in the else. This is a one-block move with no new state and it is the
single cheapest item in this sweep to try.
