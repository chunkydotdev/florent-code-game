---
tactic: Mark the expeditionary unit so it is structurally excluded from the go-home branch — its retreat is a sidestep, never a withdrawal
source: https://raw.githubusercontent.com/dgant/PurpleWave/master/src/Micro/Actions/Combat/Maneuvering/Retreat.scala
origin: PurpleWave (Dan Gant), Brood War AI — repeated AIIDE/SSCAIT champion
evidence: documented
transfers: yes
---

## WHAT IT IS

PurpleWave's `Retreat` action computes five candidate goals. Two of them —
`goalReturn` (fall back within the zone) and `goalHome` (leave the zone) — are
each guarded by the **same first conjunct**:

> ```
> ! unit.agent.isScout
> ```

**Referent check.** `unit` is the retreating `FriendlyUnitInfo`; `isScout` is the
flag set on the unit assigned forward reconnaissance. The string occurs exactly
twice in the file, once in `goalReturn` and once in `goalHome`, and nowhere else.
The remaining goals — `goalSidestep`, `goalCircle`, `goalSafety` — are all
**lateral**: they move the unit off a threatened pixel without surrendering the
position. **A scout under threat in PurpleWave steps aside. It never goes home.**

The admission gate for the whole action is one line and contains no health term
and no clock:

> ```
> override def allowed(unit: FriendlyUnitInfo): Boolean = unit.canMove && unit.matchups.threats.nonEmpty
> ```

**Negative control on the same file, run for this sweep:** `hitPoints` 0
occurrences, `health` 0, `hp` 0. The tournament-winning bot's retreat decision
does not read HP at all.

## WHY IT MIGHT TRANSFER — this is the cheapest item in the sweep and it is one boolean

The distinction PurpleWave draws — **"step off the tile" is a different action
from "abandon the errand"** — is exactly the seam our dwell number sits on. A
raider that treats "a turret has line on me" and "my errand is over" as the same
event pays a full traverse for a one-tile problem.

Our geometry makes the sidestep unusually cheap and unusually well-defined:

* Turrets are **immobile and facing-dependent**. A gunner's line *stops at the
  first targetable tile* and reaches 3 tiles cardinally; a sentinel's line is
  **single-tile-wide and ignores obstacles** but it **cannot rotate at all**
  (rotate is gunner-only, 10 Ti and a cooldown). **So for a sentinel, one
  cardinal step out of the file is permanent immunity from that sentinel.**
* `get_attackable_tiles_from(position, direction, turret_type)` returns the raw
  pattern, so the safe-tile set adjacent to us is computable without standing in
  it.
* Builder moves are cardinal-only, so the sidestep is one of at most four
  candidates — trivially enumerable inside the CPU budget.

**And the exclusion flag itself is free:** every unit already runs the same
`main.py`, so a raider role marker is a module-level constant plus one attribute,
not a store slot.

## WHAT WOULD KILL IT

* Act and move are **mutually exclusive per turn** for a builder. A sidestep
  costs the same turn a build would have cost, so it is not free — it is cheaper
  than a traverse, not cheap.
* If our raid deaths are mostly to **sentinels firing along a line the raider
  must occupy to reach its target** (rather than to incidental coverage), the
  sidestep just delays the same shot. That is a distinguishable case and the
  library does not currently know which one we are in.
* `PLAY_DEFENCE: never` still governs: the sidestep is legitimate only because it
  keeps the unit *producing forward*, not because it keeps the unit alive.

## BUILDER HOOK

One boolean on the raider role that makes the go-home branch unreachable, plus a
`sidestep()` that picks the adjacent cardinal tile with the smallest number of
known enemy turret patterns covering it. **Falsifier: if forward rounds per
structure does not fall, the dwell was never withdrawal-caused and the
intervention should be reverted rather than tuned.**
