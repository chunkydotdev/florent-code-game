---
tactic: A unit that withdraws must carry information back — the retreat is the cheapest scouting trip you will ever get
source: https://battlecode.org/assets/files/postmortem-2023-4-musketeers.pdf
origin: Battlecode 2023, 4 Musketeers
evidence: documented
transfers: partial
---

## WHAT IT IS

4 Musketeers treat withdrawal as a communication event rather than a movement:

> *"if a carrier encounters an enemy and needs to run away, we don't just run away: we report."*
> *"Our priority is to get home and relay this information as fast as possible."*

**Referent check.** "a carrier" is their resource-gathering unit; "we report"
means writing the well's control status into the shared comms array, and the
stated reason follows immediately: *"If a carrier encounters danger on the way to
the well and back, chances are the next carrier will have the same problem."*
**The withdrawal is priced as a scouting result, so the round spent leaving is
not a wasted round.**

The same team's other withdrawal rule is a **group** condition rather than an
individual one:

> *"unless your health is very high, if you have friendly robots with low health, you should go to heal, too. Stick together and come back to fight later."*

The reasoning quoted just before it is that a split-out withdrawal leaves the
healthiest unit alone and it dies — **the individually-correct withdrawal is
collectively wrong.**

## WHY IT MIGHT TRANSFER — partially, and the limit is our channel

**What transfers:** the framing. Any round in which a raider gives up on a
position is a round in which the raider knows something no other unit knows —
which tiles were covered, which build failed, where a turret has line. Under
`PLAY_DEFENCE: never` this is the honest justification for the movement: the unit
is not saving itself, it is delivering a fact.

**What does not transfer cleanly:** the channel. Our store is **16 integers,
writes visible only next round, last-writer-wins**. 4 Musketeers had a
per-sector array. This library has repeatedly established that the store is
provably safe for **one small non-negative integer per slot** and hazardous for
anything with concurrent writers
([`what-the-sixteen-integers-actually-cost-us`](what-the-sixteen-integers-actually-cost-us.md),
[`the-blackboard-is-a-one-tick-bus-not-a-memory`](the-blackboard-is-a-one-tick-bus-not-a-memory.md)).
**A per-raider report does not fit; a single packed "last position where a raider
took damage" does** — and the incumbent already packs positions this way
(`SLOT_THREAT` at `bots/_v135loki18/main.py:173`).

The group clause transfers **less** than it looks: our builders cannot be killed
by enemy builders at all (builder attacks target buildings only), so the
"healthiest unit left alone gets focused" failure mode needs an enemy turret
covering the tile, not an enemy army.

## WHAT WOULD KILL IT

* **A report nobody reads is a wasted slot.** The plank is only worth a slot if
  some other unit's behaviour changes on it. If no consumer exists, this is a
  logging feature and logging is invisible on the platform anyway — `print()` is
  stripped from downloaded replays (30,664 of 30,664 `BotOutput` events empty).
* Last-writer-wins means the *most recent* raider damage overwrites the rest.
  For a threat map that is arguably correct; for a completeness map it is wrong.

## BUILDER HOOK

If the raid arm gets a withdrawal or sidestep at all, have it write the packed
tile it left into a single slot, and have the *next* raider's target selection
deprioritise that tile. **Falsifier: if raiders rarely revisit tiles a previous
raider abandoned, the slot has no consumer and the plank is dead before it
ships.**

## ⛔ CAVEAT APPENDED 2026-08-11 (s32, research arm) — THIS FILE REASONS ON A RETIRED PROGRAMME FIELD
This file cites **`PLAY_DEFENCE: never`**. That field was amended the same day and now reads
**`PLAY_DEFENCE: not_at_the_kill_s_expense`** with **`DEFENCE_ADMISSION_BAR: kill_round_non_regression`**
(`PROGRAMME.md:19-20`). **A defensive tactic is now ADMISSIBLE IFF it does not slow the kill** — it carries a
kill-round non-regression bar beside its survival bar, and is off-programme only if MEDIAN KILL ROUND RISES.
**"Defensive, therefore off-programme" is no longer a valid closure reason.**
**Scope, unchanged:** this licenses surviving the **r150-250 window so our own kill lands** (median kill 174,
median death 187, core dies in 46.3% of games). It does **NOT** license surviving to r1000 —
**`R1000_IS_DEFEAT: yes` still governs.**
**WHAT THIS DOES AND DOES NOT DO TO THIS FILE:** Line 37 supplies the justification needed to
make a withdrawal-shaped movement (reporting on retreat) legitimate under the absolute rule:
"the unit is not saving itself, it is delivering a fact." That framing is no longer strictly
necessary — under the amended field, a movement that also happens to save the unit is not
automatically disqualified, provided it clears the kill-round non-regression bar. The file's
actual mechanism (pack the abandoned tile into a store slot, deprioritise it for the next
raider) is unaffected either way; only the "must be framed as scouting, not survival"
constraint is loosened.
**STATUS:** RESTRICTION NARROWED — the tactic no longer needs the information-delivery framing
to be admissible; it can also be justified as an admissible survival move if it clears the new
bar.
**NOT REOPENED BY THIS CAVEAT.** Voiding a closure reason does not revive the road; it returns it to the queue
for a live test. Under `docs/research/PROGRAMME-drift-watch-2026-08-09.md` D12 an archive-sourced closure cannot
retire a road, and this caveat cannot restore one.
