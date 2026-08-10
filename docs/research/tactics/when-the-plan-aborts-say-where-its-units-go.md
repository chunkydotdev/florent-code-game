---
tactic: (B) THE HALF OF ABORTING NOBODY WRITES DOWN — a plan that dies must hand its units back explicitly, and the two bots that do it also decide what happens to the ones that are already committed and cannot get home
source: https://raw.githubusercontent.com/bmnielsen/Stardust/main/src/Strategist/Play.h
origin: Stardust (2nd AIIDE 2025) and PurpleWave (3rd AIIDE 2025) — StarCraft AI
evidence: documented
transfers: partial
---

## WHAT IT IS

**Stardust makes the handback a required part of the plan's interface**, with the
responsibility stated in the header:

> *"// Called when a play is being disbanded (either removed completely or transitioned to a
> different play)."*

> *"// It is the play's responsibility to call either removedUnitCallback or
> movableUnitCallback for all units that have been assigned"*

Two callbacks, and the caller passes different pairs depending on why the plan ended: on a
**transition** it passes `(removeUnit, moveUnit)` so units flow into the successor; on
**completion** it passes `(removeUnit, removeUnit)` so they return to the free pool.
**The abort path and the succeed path release units differently, and the plan chooses per
unit.**

**PurpleWave goes one step further and handles the units that cannot be released.** Its drop
mission's abort block, run first thing every tick, ends with:

> *"// Godspeed you poor souls"*

on the branch where all the transports are dead and passengers are already inside an enemy
base — those units are flipped to `commit = true` rather than told to retreat. **A plan that
cannot rescue its units tells them to do damage instead of dying on the way home.**

**And the sunk-cost rule sits in the same codebase, in one line.** PurpleWave's production
layer re-derives its request list every tick but carries over anything already paid for,
**before** any matching:

> *"// Requeue any paid-for production, in the same order"*
> *"_queueNext ++= _queueLast.view.filter(_.hasSpent)"*

**PurpleWave's abort block is also worth reading as a whole for its shape** — six independent
termination conditions in seventeen lines, of which two are timeouts (one state-conditional),
two are resource-gone predicates, one is phase-specific, and one drops invalid *steps* from
the front of the itinerary while leaving the *plan* alive:

> *"if (duration > Seconds(45)() && state != Raiding && state != Evacuating) {
> terminate("Expired (not raiding)"); return }"*

## WHY IT MIGHT TRANSFER

`transfers: partial`, because half of it lands and half of it does not.

**What lands:**

- **Our engine has the "cannot get home" case in an unusually sharp form.** The library
  measured that **2.34% of forward throws at r200+ ever land a single attack on the enemy
  core**, and that raider survival falls from 43 rounds to 6 at r150. A builder deep in enemy
  territory when a push is called off is PurpleWave's stranded passenger exactly. **Our
  options for it are `self_destruct()` (no damage), walking home through a kill zone, or
  attacking whatever is adjacent at 2 Ti for 2 damage** — and the library's own arithmetic
  says the walk home is worth close to nothing. *"Godspeed you poor souls"* is a real decision
  here, and our bot does not currently make it explicitly.
- **The sunk-cost rule is sharper here than there.** `destroy()` refunds nothing and cost
  scale is one global additive team factor, so **titanium already committed is unrecoverable
  and its scale contribution persists.** A "keep anything already paid for" guard is one
  condition and it is unambiguously correct under our rules.
- **The abort block's shape is copyable even without the object model** — several independent
  termination conditions, evaluated first, with early returns, and step-level invalidity
  handled separately from plan-level.

**What does not land:**

- **We have no unit pool to hand back to.** Stardust's Strategist is a single global object
  holding every unit; ours is a per-unit `run()` with no shared roster. A "release these units"
  callback has nothing to call. The nearest analogue is a unit clearing its own per-instance
  role and falling back to a default — which is one line, and is not the same mechanism.

## WHAT WOULD KILL IT

- **Neither bot measured any of this.** These are shipped designs in bots that placed 2nd and
  3rd at AIIDE 2025; no ablation, no per-mechanism number. Evidence is `documented` for the
  design only.
- **PurpleWave's drop mission is a rare, expensive, opt-in play** — the machinery is sized for
  something that happens a few times a game with several units aboard a transport. Our nearest
  equivalent (a forward turret plant) commits titanium, not units, and titanium cannot be
  handed back at all.
- **The stranded-unit rule is a licence to spend units badly if it is applied too widely.** A
  builder told to `commit` inside an enemy base deals 2 damage per 2 Ti against a defence that
  heals at 4.00 HP/Ti. **Against a 2.2:1 defensive edge, "do damage on the way out" is
  arithmetic that loses**, and the honest version of this rule here is closer to *do not
  spend more titanium retrieving it than it is worth* than to *fight to the last*.
- **Our library's standing verdict is that the forward road is closed on three instruments.**
  This file describes what to do when a forward plan aborts; it does not argue for having one.

## BUILDER HOOK

Two small, independent things, neither of which needs a plan object:

1. **The sunk-cost guard.** Wherever the bot reconsiders a purchase it has partially committed
   to (titanium reserved, a builder walked into position), make "already spent" an
   unconditional keep. One condition, and our rules make it unambiguous.
2. **The stranded-unit rule, as a measurement first.** Count how many of our builders are
   alive and inside the enemy half when a forward intention is abandoned, and what they do
   next. If the answer is "walk home and die", the decision is worth making explicitly; if it
   is "they were already dead", the case does not arise and the file is closed cheaply.

## SOURCES QUOTED IN THIS FILE

- https://raw.githubusercontent.com/bmnielsen/Stardust/main/src/Strategist/Play.h
- https://raw.githubusercontent.com/bmnielsen/Stardust/main/src/Strategist/Strategist.cpp
- https://raw.githubusercontent.com/dgant/PurpleWave/master/src/Tactic/Missions/MissionDrop.scala
- https://raw.githubusercontent.com/dgant/PurpleWave/master/src/Tactic/Production/Produce.scala

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 18 (2026-08-09).

---

> ### ⚠ CAVEAT ADDED 2026-08-10 (research arm) — **`THE FORWARD ROAD IS CLOSED` IS DEMOTED. DO NOT REASON DOWNSTREAM OF IT AS SETTLED.**
>
> This file treats that conclusion as established. **Two things have happened to it
> and neither had propagated here:**
>
> 1. **Its evidentiary floor did not reproduce.** `INDEX.md` records that the
>    `+11.4 / +16.6 / +22.3pp` home-defence advantage — the floor under the
>    conclusion — **does not reproduce on v102**: Eir home 78.3% vs field 62.0%
>    (+16.3pp) but **v102 71.5% (n=439) vs 81.5% (n=520) = -10.0pp**, and paired
>    within opponent the gap **narrows or flips in 5 of 8**. The index's own words:
>    **"n=439 supports 'does not reproduce', NOT 'refuted'"**.
> 2. **A field-wide cut now runs against it.** `../bisons-fast-kill-2026-08-10.md`:
>    **2+ forward in-range sentinels standing by r45 takes core-kill-by-r100 from
>    3.6% to 23.1% across the field (n=17,235/804, p=1.9e-12)**, with a powered
>    placebo firing null. The Bisons reach that position in **42.3%** of games and
>    convert **47.5%**. **The forward road is demonstrably open for other teams.**
>
> **The defensible statement is narrower than the one in this file: OUR forward road
> was closed on OUR instruments, in the Eir era.** That is not "the forward road is
> closed", and the two were being used interchangeably.
>
> **Under D12** (Magnus, 2026-08-10 - *"test everything in unrated games before we
> refute them"*) **an archive-sourced closure cannot retire a road at all.** This one
> goes to the **bottom of the queue, not off it.**
