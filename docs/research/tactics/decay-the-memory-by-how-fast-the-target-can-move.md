---
tactic: (B) EXPLICIT DECAY EXISTS AND ITS TUNING PARAMETER IS TARGET MOBILITY — per-class timeouts of 0 / 5 / 10 rounds in one bot, a flat 100 rounds justified as "since enemies move" in another, and `Forever()` for anything immobile in a third. For us that arithmetic terminates: every attackable target is a building, so N = infinity
source: https://battlecode.org/assets/files/postmortem-2026-lorem-ipsum.pdf
origin: Battlecode 2026 lorem ipsum; Battlecode 2023 4 Musketeers (finalist); PurpleWave (StarCraft AI)
evidence: documented
transfers: partial
---

## WHAT IT IS

Sweep 20C asked whether anyone put an explicit age on remembered information, what N was, and
whether it was tuned or guessed. **Three sources say yes, and all three make N a function of
how fast the remembered thing can move.**

**1. Per-target-class timeouts, in rounds, named (BC2026 lorem ipsum).** The bot gives every
rat a bounded memory of enemies:

> *"Each memory is implemented via a Memory class, which have fields robotLoc, type, friend,
> round respectively."*

> *"It also had an isStale method to check if the memory is ”stale” (old)."*

and the numbers:

> *"Cats, baby-rats, and rat kings all individually had their own timeout, where if a memory
> was older than that we consider it an empty memory (for example, Cats had 5 rounds, rats
> had 0 (has to be this round), kings have 10)."*

**Referent check.** The three classes are the BC2026 unit types; the postmortem's own game
description elsewhere treats Rat Kings as the high-value stationary-ish objective and baby
rats as the numerous cheap mobile unit. **The ordering is the finding: the cheapest, fastest,
most numerous thing gets N = 0 — no memory at all, "has to be this round" — and the biggest,
slowest, most valuable thing gets the longest memory.** (Curly quotation marks in the source
are reproduced as written.)

**2. A flat N with its justification attached (BC2023 4 Musketeers, finalist).** Their
per-sector combat information expires:

> *"since enemies move, we reset that information every 100 (this number changed later)
> rounds, considering it stale."*

**Referent check.** *"that information"* is the enemy-presence data stored on a `SectorInfo`
object; the postmortem describes sectors as a coarse grid partition of the map used because
*"you can only write to it when in range"*. **The stated cause of expiry is mobility, not
uncertainty in general** — and *"(this number changed later)"* is the author telling you the
number was tuned, and telling you he is not reporting the tuned value.

**3. And expiry DEMOTES the belief rather than deleting it (same source).** This is the part
that is easy to miss:

> *"Finally, we have explore sectors, which are the symmetry locations and any combat sectors
> that became stale so that units know to check out the areas and see if there’s anything
> there."*

**A stale belief becomes a REASON TO GO LOOK, not a reason to stop.** Note the company it
keeps in that sentence — the symmetry-derived candidate locations are in the *same* bucket as
expired sightings. Both are "unverified places worth walking to".

**4. The limit case, in code (PurpleWave).** Its belief module computes an
`expectedSurvivalFrames` per remembered unit, and the default arm is unbounded:

> *"// Assume units we haven't seen in a very long time are dead"*

> *"else                                Forever()"*

with a finite value only for units that genuinely expire (Broodlings, Dark Swarm, Disruption
Web, Scanner Sweep), irradiated units, and warriors (*"?(With.strategy.isFfa, Minutes(4),
Minutes(8))()"*). **And the mobile-unit trail-decay it does apply carries two exemptions that
are themselves mobility arguments:**

> *"// Let the trail go cold, as appropriate"*

> *"if (With.framesSince(unit.lastSeen) > 24 * 20 && ! atHome && ! hasCompany) {"*

**Referent check.** `24 * 20` is 20 seconds at BW's 24 frames/second — this is a decay
threshold, not a real-time limit on anything else. `atHome` is *"unit.metro.exists(_.bases.exists(_.owner == unit.player))"* and `hasCompany` is an ally seen within the last
10 seconds and 15 tiles. **A unit sitting in its own base does not go cold, because it has
nowhere it needs to be.**

## WHY IT TRANSFERS ONLY PARTIALLY — AND THIS IS THE USEFUL PART

**Run the sources' own rule against our entity list and the decay problem evaporates for the
attack plank.**

| what we might remember | can it move? | N implied by these sources |
| --- | --- | --- |
| enemy core (2x2, 500 HP) | never | **infinity** |
| enemy harvester (on ore) | never | **infinity** |
| enemy conveyor / splitter / barrier | never | **infinity** |
| enemy gunner / sentinel / launcher | never | **infinity** |
| terrain (WALL / ORE_TITANIUM / EMPTY) | never (terrain is static) | **infinity** |
| enemy builder bot | yes, 1 cardinal step / cooldown | **0 — and we cannot attack it anyway** |

A builder bot's `attack` is *2 Ti → 2 dmg to the building on an orthogonally adjacent tile*.
**Builder bots cannot damage builder bots at all.** The only thing that shoots a mobile enemy
is a turret, and a turret fires from current vision (`can_fire`), never from memory. **So the
entire class of targets for which a decay constant would be needed is a class we cannot act
on from memory in the first place.** lorem ipsum's `rats had 0 (has to be this round)` is
already our engine's enforced behaviour.

What DOES transfer:

- **The 4 Musketeers demotion rule, inverted into our currency.** Their stale sectors become
  *explore* targets. Ours cannot: re-scouting costs a builder-bot round-trip, and the builder
  is simultaneously our only mobile unit, our only damage source and our only construction
  worker. **Re-verification is priced in the same currency as the attack itself.** Their rule
  says "when in doubt, go look"; ours has to say "when in doubt, keep hitting", which is
  [`retract-the-target-only-on-a-look-not-on-a-clock`](retract-the-target-only-on-a-look-not-on-a-clock.md).
- **PurpleWave's exemption structure is the transferable idea, not its constant.** Decay is
  suppressed where the prior is independently strong (`atHome`, `hasCompany`). Our analogue:
  a belief about a tile *inside the enemy core's own neighbourhood* should never decay,
  because the defender has every reason to keep rebuilding there.

## WHAT WOULD KILL IT

- **The whole file, honestly, if all we ever attack is the core.** Then N is trivially
  infinite and nothing here is buildable. This is filed `partial` for exactly that reason:
  it is a **negative result with a mechanism** — do not spend store slots, CPU or design
  effort on information ageing, because our ruleset already made every attackable target
  permanent.
- **One real exception exists and it cuts the other way: destroy-and-rebuild.** `destroy()`
  is free, instant and unlimited for the owner, so an enemy turret seat can be vacated and
  refilled. A belief about a *seat* (this tile has a turret) can therefore go stale in both
  directions. Nothing in these three sources models a target that comes back.
- **The lorem ipsum numbers are not tuned evidence.** The postmortem gives them as an
  example (*"for example"*) with no ablation, in a bot whose own author lists
  *"All my bots magically “died” all the time"* among its problems. Treat 5/0/10 as a
  demonstration of the *ordering principle*, not as importable constants.
- **The 4 Musketeers number is explicitly not the shipped one** — *"(this number changed
  later)"*. Anyone quoting "100 rounds" as a tuned value is quoting the pre-tuning value.

## BUILDER HOOK

**None yet, and that is the recommendation.** The measurement that would open a hook is the
destroy-and-rebuild exception, and it is a corpus query with no bot change: over the local
replay archive, **how often does an enemy building of any type appear on a tile where an
enemy building of a different type (or none) stood earlier in the same game?** If seat churn
in the enemy half is near zero, belief ageing is provably worthless here and this road closes
permanently. If it is common, the smallest hook is a two-state seat belief with retraction on
look, not on age.

## SOURCES QUOTED IN THIS FILE

- https://battlecode.org/assets/files/postmortem-2026-lorem-ipsum.pdf
- https://battlecode.org/assets/files/postmortem-2023-4-musketeers.pdf
- https://raw.githubusercontent.com/dgant/PurpleWave/master/src/ProxyBwapi/UnitTracking/Imagination.scala

Every quoted string above was verified verbatim by literal `grep -F` against the flattened
primary text (`pdftotext` then `tr -s ' \n\t\f\r' ' '`) or the raw source file, during
tactics sweep 20C (2026-08-10 04:11 UTC, repo HEAD `a08669c`).
