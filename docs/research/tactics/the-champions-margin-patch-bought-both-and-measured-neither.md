---
tactic: At the margin the BC2025 champion bought tempo AND survivability in the same finals patch, in the same paragraph, and separated neither — arrival gated on affordability, plus temporal staggering into enemy fire
source: https://battlecode.org/assets/files/postmortem-2025-just-woke-up.pdf
origin: Battlecode 2025 / Just Woke Up (CHAMPION)
evidence: documented
transfers: partial
---

## WHAT IT IS — arm A and arm B, in the one place where the stakes were highest

Just Woke Up went into the finals having scrimmed *"insanely close"* against the
teams they would face, with a few days to squeeze out margin. Their soldier
changes for the finals are two sentences apart and are **one tempo purchase and
one robustness purchase**.

**The tempo purchase — remove idle wander, gated on AFFORDABILITY:**

> *"if the soldier had enough paint and enough money to build a tower, instead of
> exploring aimlessly, they would b-line straight to the last place where they
> saw an empty ruin without a tower"*
> *"This made it so that if our soldiers had the resources to build, they
> wouldn’t waste as much time wandering around, improving our ability to spread
> and build up quickly."*

**Referent check.** "they" is Just Woke Up's own soldiers; "the last place where
they saw an empty ruin" is a remembered build site, including — the same sentence
continues — *"accounting for tower locations that they only learned about through
comms"*. The trigger is **the unit's own ability to pay**, not a round number,
not a threat, and not a broadcast order.

**The robustness purchase — stagger exposure to enemy fire:**

> *"A last small change we made was ensuring that when our soldiers attacked
> together, they would synchronize their movements to move into tower range on
> even turns. This meant that when we were attacking enemy towers they would only
> be able to hit one of the soldiers per turn, giving our soldiers more time to
> damage the towers before dying."*

**Referent check, and an explicit limit on what is sourced here.** "they would
only be able to hit one of the soldiers" — "they" is the enemy towers, the object
of *"when we were attacking enemy towers"*. **The postmortem does not explain the
mechanism by which synchronising onto even turns produces one-hit-per-turn, and I
am not reconstructing it.** What is sourced is the *shape* of the intervention:
the timing of arrival into the defender's range was made a controlled variable in
order to reduce how much of the attacking force the defender can damage per unit
time. The arithmetic behind it is not in the document.

**Neither change carries a number, and the surrounding text says why.** For the
whole finals patch they report only:

> *"we added some minor optimization here and there that great boosted our
> winrate against our old bot versions"*

— a single pooled win-rate reading over a bundle. **The team that won Battlecode
2025 did not separate its tempo change from its survivability change.** They had
the harness to do it: an automated all-map A/B rig borrowed from camel_case,
which they used elsewhere in the same document. They pooled anyway.

**And this is the same team whose most consequential finals decision overrode
its own A/B**, already filed by sweep 24
([`nobody-in-the-field-has-ever-measured-the-kill-round`](nobody-in-the-field-has-ever-measured-the-kill-round.md)):
> *"Against our past bots it usually went even in wins, or even slightly lost.
> But our bot wasn’t super aggressive, and we believed that this, in theory,
> SHOULD be better against the teams that we have the worst matchups against."*

## WHY IT MIGHT TRANSFER — against OUR ruleset specifically

**The tempo half transfers cleanly and is close to something we already
diagnosed.** Sweep 23 established that our forward metric is an idle-time and
targeting defect, and filed
[`the-idle-forward-unit-gets-a-destination-not-a-recall`](the-idle-forward-unit-gets-a-destination-not-a-recall.md).
**Just Woke Up's addition is the GATE, not the destination**: the unit stops
wandering only *once it can pay for the thing it would go do*. That maps
directly onto our forward sentinel, which is gated on
`get_sentinel_cost() + LOKI_FWD_TI_FLOOR` (`raid.py:408-412`) — a raider
approaching the ring while the bank cannot fund a sentinel is doing the
"exploring aimlessly" half, and one that can pay should be committing to a
station. That is an affordability-gated commitment we do not currently make.

**The robustness half is the weaker transfer and may be inverted here.** Our
turrets are single-target-per-shot with a reload (gunner dmg 7 / reload 1,
sentinel dmg 18 / reload 2), so a defender's throughput against our raid may
already be one body at a time regardless of arrival timing — in which case
staggering buys nothing. **The one thing that could make it matter is line
collateral: the gunner fires a straight-line shot and the sentinel a
single-tile-wide line that ignores obstacles, so bodies queued along a firing
ray are a different exposure than bodies spread across it.** Whether a line shot
damages more than the first entity is **not settled in this repo's engine notes
and must be probed before any plank is written on it.**

**We already ship the SPATIAL half and not the TEMPORAL half.** `raid.py:482`:
*"the raid spreads across the ring on the way in without a single store write
and without four bodies funnelling onto one tile"*, using a deterministic seat
derived from each unit's raid slot. That is spread in *space*. Just Woke Up's is
spread in *time*, and we have no analogue.

**EFFECT ON MEDIAN KILL ROUND — the two halves differ and must not be bundled,
which is the entire lesson of this file.** The affordability gate is a tempo
change and should move the median **earlier**. The temporal stagger delays some
bodies' entry into range by up to one round each and should therefore move it
**later or flat** — it is a defensive purchase and carries
`DEFENCE_ADMISSION_BAR: kill_round_non_regression` on its own, separately.
**Shipping them together would reproduce exactly the confound that makes the
champion's own report unusable to us.**

## WHAT WOULD KILL IT

* **The stagger's mechanism is unexplained in the source and may be
  game-specific.** If it depended on a BC2025 tower attack pattern with no
  analogue here, it does not transfer at all and the honest verdict is `no`.
  This file is `partial` because the *tempo* half stands on its own.
* **The affordability gate could starve the raid.** Our forward sentinel gate is
  a conjunction — bank floor **and** `LOKI_FWD_MIN_HARV = 2` harvesters. Gating
  *movement* on affordability too would let a poor round park the raid at home,
  which is the "one more way it stops being allowed to try" failure
  `doctrine.py:1436` was written to prevent.
* **Neither change is evidenced individually.** The only number attached to
  either is a pooled win rate over a bundle of *"minor optimization here and
  there"*. Treat the direction as suggestive and the magnitude as absent.

## BUILDER HOOK — smallest thing that would test it

Take **the tempo half only**, and test it alone.

No new store slot required (the 16 are fully bound, `doctrine.py:931-961`,
`:1166-1170`). In `raid.py`'s station logic, add an affordability predicate to
the approach: a raider that can currently fund
`get_sentinel_cost() + LOKI_FWD_TI_FLOOR` commits to its station and stops
re-scoring; one that cannot keeps its existing behaviour. This is a strictly
narrower change than a new mode and reuses the cost getters already in the file.
Read out **median kill round** and first-forward-sentinel round.

**Leave the temporal stagger unbuilt until the line-collateral question is
settled on the engine** — that is a probe (`bots/_probe_*` against a known
firing line), not a leg, and it is a prerequisite rather than a plank.
