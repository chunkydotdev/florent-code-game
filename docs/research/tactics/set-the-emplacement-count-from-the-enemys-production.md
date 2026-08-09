---
tactic: Set the number of emplacements from what the ENEMY has built to attack you with, not from a fixed quota — and encode it as a penalty band, not a hard rule
source: https://forum.codingame.com/t/code-royale-cc03-feedback-strategies/30903
origin: CodinGame Code Royale — Azkellas (6th); band form from robostac (1st); saturation form from Shingy (9th)
evidence: documented (competitors' own accounts, official feedback thread and published postmortem)
transfers: yes
---

## WHAT IT IS

Code Royale is the closest priced analogue this library has to our situation: static
towers whose strength is bought with repeated investment, competing for the same currency
as economy. **Three finishers published how they set the tower count, and none of them
used a fixed number.**

**1. Azkellas (6th) indexes the count on the enemy's PRODUCTION BUILDINGS.** The
estimator, then the schedule:

> *"To know if a mine is a good idea, I have a rough estimation that computes the number of
> towers protecting it from any enemy barracks (protecting = on the path)."*
> *"I'd usually ask for 3/4 towers if the enemy has one barracks, 6 if s/he has severals,
> and 2/0 if I'm confident I am playing against a camper that will not attack me."*

**Subjects: his own towers, counted against the number of enemy barracks — the buildings
that produce the units that would attack.** Note the bottom of the range: against an
opponent read as passive, **zero**.

His layout rule is a concentration rule, and he states the reason:

> *"My towers have to be near each other so I can defend easily in the beginning."*

**2. robostac (1st) encodes the count as a PENALTY BAND inside the evaluation, not as a
rule.** Two bands, one per structure class:

> *"If I had less than 5 towers, more than 2 mines and less towers than mines I added a
> large negative penalty. This was disabled if the enemy had no mines after turn 50."*
> *"If I had 0 or more than 2 (3 if I'd triggered my giant strategy) barracks I had a
> large negative penalty to my score."*

**The winner's mix control is a conjunction — a floor of 5 towers, a towers ≥ mines ratio,
and an opponent-state escape clause — expressed as score penalties a search can trade
away when something better is on offer.** That is a materially different mechanism from a
build quota, and it is the form most likely to survive contact with a real game.

**3. Shingy (9th) saturates on QUALITY first, then switches to economy.**

> *"If all towers have sufficient range and my income is low, build more mines."*
> *"If no sites are safe to build mines on and I have at least 5 towers with sufficient
> range, consider replacing my furthest tower from the centre with a mine."*

Two independent finishers arriving at **5** as the saturation point, and the second one
willing to **convert the marginal tower back into economy** once it is reached.

## WHY IT MIGHT TRANSFER — against our ruleset

**We have the enemy-production signal and it is cheaper to read than Code Royale's.**
Their proxy was enemy barracks. Ours is the count of enemy **builder bots** in vision — the
only unit that can remove our structures — and, more durably, the enemy turrets and
harvesters we have seen. Sweep 15 already established that the field's live branch signals
are **economic and enemy-side**, doubly sourced, and that *"rush when they look
aggressive"* is sourced by nobody. **This is the same finding arriving on the defensive
side of the ledger.**

**The zero limb is the part we are least likely to have.** Azkellas builds **two or none**
against an opponent read as a camper. Our own measurement is that we over-garrison
(collar 66.5% against a field 53.2%, and 40.6% at ≥1900) — an unconditional defensive
reflex is exactly what a threat-indexed count would remove, and it removes it *without*
the failure mode of the garrison experiment, because it only thins the collar when the
opponent is measurably passive.

**The band form fits our engine well.** We have no search to trade penalties against, but
the same shape works as a soft gate: turret builds allowed freely below a floor, allowed
above it only when an enemy-threat estimate exceeds a threshold, and disallowed above a
ceiling — with the whole thing disarmed when no enemy builder has been seen for N rounds.
Note that our disarm has a *free* action available that Code Royale did not: `destroy()`
is cooldown-free and refunds the entity's scale contribution, so Shingy's
"replace the furthest tower with a mine" is literally executable here.

## WHAT WOULD KILL IT

- **The specific numbers are Code Royale's and are worthless here.** `5 towers`, `3/4 vs
  6 vs 2/0`, `2 barracks` are tuned to a game with a fixed set of building sites, a mobile
  queen, and creep waves. What transfers is the *form*: an enemy-production index, a
  floor, a ratio, an escape clause, and a saturation point.
- **Two of the three sources are forum posts by 6th and 9th place.** `documented` as their
  own accounts, but not winners' doctrine — only robostac's bands are.
- **Our vision is unit-scoped and our comms store is 16 integers.** Maintaining a
  team-wide enemy-production estimate costs slots and is subject to the buffered-write
  semantics that already caused one latent bug (sweep 7 / `store-semantics`). The estimate
  must be a last-writer-wins scalar, never a read-increment-write counter.
- **The counterweight is real and filed beside this**: Jay Scott's observation that on a
  *bot ladder* heavy static defence often persists simply because opponents fail to punish
  it — see
  [`turtling-persists-because-nobody-punishes-it`](turtling-persists-because-nobody-punishes-it.md).
  A threat-indexed count is only as good as the threat estimate.

## BUILDER HOOK

The smallest version needs one store slot and no new sensing: **each unit that sees an
enemy builder bot writes the current round into a slot; the turret-build gate reads it and
requires "an enemy builder seen within the last N rounds" before allowing a turret above a
small floor.** That is Azkellas's `2/0` limb, implemented with a timestamp instead of an
opponent model, and it is testable on its own before anything more elaborate.
