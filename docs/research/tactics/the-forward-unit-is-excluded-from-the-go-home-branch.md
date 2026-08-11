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

The distinction PurpleWave draws — **stepping off the tile is a different action
from abandoning the errand** — is exactly the seam our dwell number sits on. A
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

## ⛔ CAVEAT APPENDED 2026-08-11 (s32, research arm) — THIS FILE REASONS ON A RETIRED PROGRAMME FIELD
This file cites **`PLAY_DEFENCE: never`**. That field was amended the same day and now reads
**`PLAY_DEFENCE: not_at_the_kill_s_expense`** with **`DEFENCE_ADMISSION_BAR: kill_round_non_regression`**
(`PROGRAMME.md:19-20`). **A defensive tactic is now ADMISSIBLE IFF it does not slow the kill** — it carries a
kill-round non-regression bar beside its survival bar, and is off-programme only if MEDIAN KILL ROUND RISES.
**"Defensive, therefore off-programme" is no longer a valid closure reason.**
**Scope, unchanged:** this licenses surviving the **r150-250 window so our own kill lands** (median kill 174,
median death 187, core dies in 46.3% of games). It does **NOT** license surviving to r1000 —
**`R1000_IS_DEFEAT: yes` still governs.**
**WHAT THIS DOES AND DOES NOT DO TO THIS FILE:** Line 70 restricts the sidestep tactic's
justification to "keeps the unit *producing forward*, not because it keeps the unit alive" —
i.e., survival could not be cited as a reason under the absolute rule. That restriction is now
narrower than the rule requires: survival is an admissible reason too, provided it clears
`DEFENCE_ADMISSION_BAR` (kill-round non-regression). This does not change the file's BUILDER
HOOK (add a go-home exclusion flag plus a `sidestep()`) — it only removes a now-unnecessary
justification constraint.
**STATUS:** RESTRICTION NARROWED — survival is no longer a disqualifying justification for the
sidestep, only a non-regressing kill round is required.
**NOT REOPENED BY THIS CAVEAT.** Voiding a closure reason does not revive the road; it returns it to the queue
for a live test. Under `docs/research/PROGRAMME-drift-watch-2026-08-09.md` D12 an archive-sourced closure cannot
retire a road, and this caveat cannot restore one.
