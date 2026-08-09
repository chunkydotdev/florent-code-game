---
tactic: Put the trigger on a unit that was already going there — scouting with zero marginal cost
source: https://battlecode.org/assets/files/postmortem-2025-the-kragle.pdf
origin: Battlecode 2025 The Kragle (finalist) and Battlecode 2023 Gone Fishin' (finalist)
evidence: documented
transfers: yes
---

## WHAT IT IS

The brief for this sweep names the objection directly: *our only mobile unit is also our
only builder, so every scouting round is a build round forgone.* Two independent finalists
solved that objection the same way — **the trigger is evaluated by a unit that was
travelling for an economic reason anyway**, so the reconnaissance has no separate budget.

**The Kragle (BC2025) — the scout IS the opener.** Their two starting soldiers were sent to
capture the nearest ruin, which is a purely economic errand. The rush decision was read off
what those soldiers found *at the destination they were already going to*:

> *"The first priority of the soldier pair is always to capture an “uncontested” ruin"*

> *"Until the soldiers finished the first ruin, they were in “opening mode.”"*

> *"in the case that the soldiers only found ruins that were “contested,” they would rush"*

> *"On 90% of the test maps, the soldier pair would find an uncontested ruin and capture it
> before turn 20."*

> *"Our logic didn’t result in the soldiers rushing often, but when they did, it was often
> successful in giving our team a large lead."*

So: a **fixed** opening, a branch point defined by an **achievement** rather than a round
number, firing **before turn 20 on 90% of maps**, on information gathered by units doing
their normal job.

**Gone Fishin' (BC2023) — move the scouting onto the cheapest unit, then onto no unit at
all.** They started with a dedicated scout and explicitly retired it as too expensive:

> *"We first had a carrier that goes to the center of the map to scout for symmetry and
> then comes back to report."*

> *"we realized that having carriers scout is a waste of their potential to mine resources,
> which are especially important in the early game"*

> *"Having launchers scout, on the other hand, is less wasteful."*

> *"We then changed to having all launchers scout symmetry on the fly as they guess a base
> location"*

**Referent check.** "carriers" are the 2023 economic unit; "launchers" are the combat unit,
whose alternative use in the early game was lower-value. *"on the fly"* refers to scouting
performed during travel the launchers were already making toward a guessed enemy base — not
a separate trip. The end state is that **no unit is a scout**; scouting is a by-product of
movement everyone was doing.

## WHY IT MIGHT TRANSFER

Our constraint is that acting and moving are mutually exclusive per round, and our mobile
unit is our builder. That makes a *dedicated* scout expensive and a *by-product* scout free.
Our engine gives two by-product channels a bot already pays for:

- **A builder walking to its build site senses continuously.** `get_nearby_buildings()` at
  r²=20 costs one call, not one round. A builder heading toward the midline ore or a forward
  turret seat passes through the same tiles a scout would, and can publish what it saw.
- **The core sees r²=36 and never moves at all.** Anything inside that radius is observed
  for free, every round, by a unit that has no alternative use for its vision.

The Kragle's branch-point design is the transferable part: **do not gate on a round number,
gate on the completion or denial of the first economic objective.** Our nearest equivalent
of *"capture an uncontested ruin"* is *"build the first harvester on the ore we were sent
to"*. Denial has a concrete signature here — the tile is taken, walled, covered by a turret,
or the enemy builder got there first — and it is observable by the builder standing next to
it with no extra travel.

This also reframes what our own cut measured. `US_shot_w50` (AUC 0.64-0.68) is *"we were
already fighting by r50"*, which the cut correctly labels a **marker**. The Kragle's design
says the marker's likely upstream cause is **contest at the first objective** — and that
*is* readable, cheaply, at the place we were already sending the builder.

## WHAT WOULD KILL IT

- **Our first objective may not be contested on any map we play.** The Kragle's trigger
  fired rarely even in their game (*"didn’t result in the soldiers rushing often"*). If our
  ore is always safely on our own half, the branch never fires and the plank is dead weight.
  This is checkable in the corpus before any code is written.
- **A by-product scout sees only what it walks past.** The 43.6% / 70.1% figures in our own
  cut are for *their* early economy inside a builder's r²=20 **at their ring** — which
  requires the builder to have travelled to their ring. A builder that never leaves our half
  sees none of it.
- **One round of store latency** if the observation must reach the core, plus last-writer-
  wins if more than one builder publishes to the same slot.
- **Gone Fishin' lost a finals map to their own scouting design** — *"our scouting algorithm
  could not find the further away wells promptly"* — so a by-product scout is a *cheaper*
  scout, not a *better* one. Cost is what it optimises; coverage is what it sacrifices.

## BUILDER HOOK

Smallest test: the first builder sent to an ore tile records, on arrival, whether the target
ore was **available or denied** (occupied, walled, or inside an enemy turret's
`get_attackable_tiles_from` footprint) and writes a 0/1 into one store slot. Gate nothing on
it for one battery — just **measure** how often it fires, per map, and whether it separates
core-kill from non-kill games in the arena the way `US_shot_w50` does in the corpus. If it
never fires, the road is closed for one plank's cost.

## SOURCES QUOTED IN THIS FILE

- https://battlecode.org/assets/files/postmortem-2025-the-kragle.pdf
- https://battlecode.org/assets/files/postmortem-2023-gone-fishin.pdf

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 15 (2026-08-09), except where explicitly marked UNVERIFIED.
