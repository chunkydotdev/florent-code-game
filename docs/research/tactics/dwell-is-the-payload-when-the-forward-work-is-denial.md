---
tactic: Where longer forward presence WAS correct, the forward work was denial or income — continuous in time — and no withdrawal rule existed at all
source: https://battlecode.org/assets/files/postmortem-2019-smite.pdf
origin: Battlecode 2019 smite (finalist); Battlecode 2020 The High Ground; Halite III TheDuck314
evidence: documented
transfers: partial
---

## WHAT IT IS — arm (D), the falsifier arm

Three cases where the winning choice was to stay forward longer, and in all three
**the value of the forward unit accrued per ROUND rather than per ACTION.**

**1. smite (BC2019) — permanent denial as the whole strategy.**

> *"because the map is symmetric, if we can control even one resource cluster on the enemy side of the map, that creates an asymmetry in resource incomes that should, with optimal play, lead to a win"*

The units that do it are defined by their dwell, not by an errand:

> *"Crusaders/Prophets that rush to enemy clusters and prevent them from colonizing resources on their side of the map."*

and they are dispatched as early as physically possible —

> *"our harassers emerge from castles around turn 4-6, early enough to beat enemies to most clusters."*

**There is no withdrawal rule for a harasser anywhere in smite's postmortem.**
The unit's job is to occupy, and occupation has no completion state.

**2. The High Ground (BC2020) — economic units moved permanently forward.**

> *"we decided to direct our miners to try to run toward the enemy HQ location along our lattice, effectively making them be near the edge of the lattice and ready to build net guns at almost all times."*

and they paid for it knowingly on the other side of the ledger:

> *"we didn't keep a drone back to defend rushes, which made us weaker vs rush teams but stronger vs other non-rush teams, as the harassment from the early drone sometimes snowballed into a decisive economic advantage."*

**3. Halite III (TheDuck314, 3rd) — the rules paid a bonus for proximity to the
enemy, and he built permanent infrastructure to collect it.**

> *"In 4p, there is an extremely harsh penalty for squares far from any enemy ships."*

The following sentence gives the reason: *"This is because I believed I was
losing games by building a dropoff far away in a place where I would never get
any inspiration."*

## WHY IT MIGHT TRANSFER — with one caveat the builder must apply to their own number

**The rule that separates the two regimes: dwell is waste when the forward work
is an EVENT (place a structure), and dwell IS the work when it is a STATE
(occupy a tile, deny a spawn, hold a lane open).**

Our ruleset contains at least one state-valued forward job, and `CLAUDE.md`
already records that we do it: putting a body on the enemy core's 12-tile spawn
ring. A tile occupied is a spawn denied *that round*, every round, and it
produces **no structure at all**. **So a metric of the form "rounds forward per
structure placed" charges every denial round to a build that was never the
point.** That is my inference from the ruleset, not a claim from any source, and
it is a reason to decompose the 2.28x before intervening on it — not a reason to
dismiss it.

Case 3 is the clean untransferable one: **there is no inspiration analogue here.**
Our engine pays nothing for standing near an enemy. Resource flow is team-blind
but credit is team-keyed to the destination core, so proximity is not income —
`../engine-guard-matrix-exploit-hunt-2026-08-10.md`.

## WHAT WOULD KILL IT

* smite's denial is **resource denial in a multi-cluster economy**. Under
  `R1000_IS_DEFEAT` an economic asymmetry that does not convert to a dead core
  scores nothing for us, so smite's *mechanism* transfers only in the
  spawn-denial form, not the ore form.
* The High Ground finished 4th and attribute that finish partly to spreading
  themselves thin. The forward-miner decision is reported as a trade with a named
  loss, not as a free win.
* **`PLAY_DEFENCE: never` cuts both ways here:** "hold a forward position" is
  on-programme only while the position is denying the enemy something. A raider
  parked where nothing is denied is the idle case, not this one.

## BUILDER HOOK

None as a new plank. **Use it as a gate on the existing one:** before spending a
leg on forward dwell, split raider-rounds into denial-productive (a body on a
tile the enemy needs) and inert. If the denial share is large, the dwell number
is partly a feature and the intervention should exempt those rounds.

## ⛔ CAVEAT APPENDED 2026-08-11 (s32, research arm) — THIS FILE REASONS ON A RETIRED PROGRAMME FIELD
This file cites **`PLAY_DEFENCE: never`**. That field was amended the same day and now reads
**`PLAY_DEFENCE: not_at_the_kill_s_expense`** with **`DEFENCE_ADMISSION_BAR: kill_round_non_regression`**
(`PROGRAMME.md:19-20`). **A defensive tactic is now ADMISSIBLE IFF it does not slow the kill** — it carries a
kill-round non-regression bar beside its survival bar, and is off-programme only if MEDIAN KILL ROUND RISES.
**"Defensive, therefore off-programme" is no longer a valid closure reason.**
**Scope, unchanged:** this licenses surviving the **r150-250 window so our own kill lands** (median kill 174,
median death 187, core dies in 46.3% of games). It does **NOT** license surviving to r1000 —
**`R1000_IS_DEFEAT: yes` still governs.**
**WHAT THIS DOES AND DOES NOT DO TO THIS FILE:** Line 75 uses `PLAY_DEFENCE: never` to draw the
line between denial-productive dwell (on-programme) and idle dwell ("the idle case, not this
one"). The denial-vs-idle distinction is a rules/mechanism fact independent of the defence rule
and is unaffected. What changes is the framing that idle-looking dwell was categorically
excluded because it might read as "defence": under the amended field, forward presence that
also happens to aid survival is no longer automatically disqualified, provided it clears the
kill-round non-regression bar. The denial/idle split in this file remains the operative test
either way.
**STATUS:** RESTRICTION NARROWED — the denial-vs-idle distinction stands, but "idle, therefore
forbidden" is no longer the whole story if an idle-looking dwell turns out to help survival
without costing kill speed.
**NOT REOPENED BY THIS CAVEAT.** Voiding a closure reason does not revive the road; it returns it to the queue
for a live test. Under `docs/research/PROGRAMME-drift-watch-2026-08-09.md` D12 an archive-sourced closure cannot
retire a road, and this caveat cannot restore one.
