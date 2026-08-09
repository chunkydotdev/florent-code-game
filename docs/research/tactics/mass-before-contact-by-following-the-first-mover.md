---
tactic: Leaderless massing — every unit follows the first ally it sees move this round
source: https://battlecode.org/assets/files/postmortem-2023-dont-at-me.pdf
origin: Battlecode 2023, don't @ me (the team whose launcher rushing "often decid[ed] the fate of the game in less than 200 rounds")
evidence: documented
transfers: partial
---

## WHAT IT IS

don't @ me lost early small-scale fights and diagnosed it as a *grouping* problem, not a
micro problem:

> *"we were losing early 3v3 duels left and right, with the opponents launcher seemingly
> attacking as if they had comms while our launchers were getting picked off"*

> *"the higher level team’s launchers would stick together, staying constantly adjacent and
> making optimal moves to take grouped trades against isolated launchers"*

Their fix used **turn order as a free coordination channel**, with no communication at all:

> *"we implemented a feature where launchers would follow the first person near them that
> moved"*

**Referent check.** "the first person near them that moved" is detected by comparing each
nearby ally's position against its position last turn — the surrounding text spells this
out: *"If a nearby ally’s location had changed, this meant the robot must have moved, so the
robot follows that one. If none of the locations changed, this likely means that the current
launcher is the “first” robot to move in the pack."* The lowest-ordered unit in the pack
becomes the de facto leader **because it acts first**, and every later unit inherits its
direction within the same round.

They paired it with a movement-parity rule to keep the pack from smearing:

> *"Explore on evens."* (the surrounding sentence: *"Because launchers can only move once per
> every two turns, we decided that launchers all only move on even turns, unless they are in
> combat."*)

## WHY IT MIGHT TRANSFER

This is a mechanism our library has independently proven the precondition for, and has not
used. The confirmed engine fact:

> **Unit turn order is global entity-id ascending** — 1,842,445 ordered pairs over 205
> replays, **0 inversions**, cross-team included, with two causal tests that never look at
> log ordering. **We choose our units' ids by choosing when we build them.**

So "follow the first ally that moved" is not a heuristic here — it is **deterministic**. The
lowest-id builder in a group is guaranteed to have moved before any higher-id builder reads
its position, every round, with no store slot, no buffered-write latency, and no
last-writer-wins hazard. It is a leader election that costs zero titanium and zero
bandwidth, in a game where our comms are 16 integers with next-round visibility.

Why it matters for *first contact* specifically: the failure it fixes is **arriving in
pieces**. Our library's standing arithmetic says a defender wins any titanium-symmetric
attrition race 2.2:1 (4.4:1 on a stacked tile), so damage delivered piecemeal is a donation.
Anything that makes our bodies arrive together raises the concentration term — and
*concentration, not more damage* is the crack the library says exists.

`transfers: partial` for a specific reason: **their launchers were damage; our builders are
not.** A massed group of builder bots deals 2 dmg per 2 Ti each and **cannot target enemy
builder bots at all**. Massing helps us for **heal stacking**, **build escorting**, and
**arriving with enough bodies to place and hold a turret seat** — not for a mobile army
punch, which we do not have.

## WHAT WOULD KILL IT

- **Movement is one cardinal step per round and competes with acting.** A follower that
  moves is a follower that did not build. Massing therefore has the same price as scouting,
  and the same objection applies.
- **A leader with a bad target drags the whole group** — the classic failure of leaderless
  following, and our store gives no cheap veto (writes land next round).
- **Id magnitude is meaningless.** Ids come from one global counter shared with resource
  stacks (97,455 of the gaps are stack ids), so the leader must be identified by *observed
  movement*, exactly as don't @ me did, or by comparing ids directly — never by inferring
  "recently built" from an id delta.
- **A core-spawned builder holds the highest id and acts LAST among our units** (24,045 new
  entities, 0 acted on their creation round). A newly spawned builder is structurally a
  follower, never a leader — which is convenient here, but is a trap for any design that
  wants the newest unit to lead.

## BUILDER HOOK

Smallest test: in the existing builder movement code, before choosing a direction, scan
`get_nearby_units(dist_sq=2)` for a friendly **builder bot** whose position differs from the
position cached last round; if one exists, copy its step. One cached dict of id→position in
instance state, no store slot, no titanium. Measure whether raider groups arrive with more
bodies simultaneously (the corpus already has the decoder for builder positions per round in
`positions.tsv`).

## SOURCES QUOTED IN THIS FILE

- https://battlecode.org/assets/files/postmortem-2023-dont-at-me.pdf

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 15 (2026-08-09), except where explicitly marked UNVERIFIED.
