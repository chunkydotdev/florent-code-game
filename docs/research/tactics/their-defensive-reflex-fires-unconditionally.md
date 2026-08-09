---
tactic: The stronger opponent's defensive reflex is unconditional — tax it, and watch for the moment they condition it
source: https://battlecode.org/assets/files/postmortem-2021-wololo.pdf
origin: Battlecode 2021 / wololo — underranked to ~150th after a rule change, then peaked 4th
evidence: documented
transfers: partial
---
WHAT IT IS — wololo could not explain why his rating kept climbing against teams he thought were
stronger, went looking, and found that the top tier's defence was **not a decision**:

> *"I learned that most top turtles operated under the assumption that their turtle was worth
> protecting, and thus attempted to defend until they had enough defense built up to support
> slanderers, consequently using up all their unit count on defense against my burying rushes
> **regardless of whether it would work for them or not**."*

(The referent of *"their turtle"* is the top teams' own defensive formation, and the subject of
*"using up all their unit count"* is those top teams, not wololo.)

**The edge was not that his attack won. It was that their answer to it cost more than the attack
did, and fired whether or not it was correct.** He then made the tax the plan rather than the
kill: *"I then drained the opponent of conviction since defense was expensive, rather than by
boosting my own conviction through self-empowerment, leading to the same winning outcome as
before."*

**And the counter is documented in the same paragraph, which is why this file is honest rather
than a sales pitch.** *"some teams began to learn not to waste conviction on defenses while
facing my muckraker rush"* — and the three teams that adapted each beat him a different way (one
spent the saved resource on votes, one on large converting units, one simply fortified properly
until his rush *"could have no winning response at all"* on medium-to-large maps).

WHY IT MIGHT TRANSFER — **Our tiebreak key makes a resource tax a win condition, not an
annoyance.** Round 1000 resolves on *titanium delivered to core*, so titanium the opponent
diverts into defence that was never needed is subtracted from the quantity that decides the game.
And our defender's own edge — the 2.2:1 heal arithmetic (4.4:1 stacked) — is the very thing that
makes an unconditional defensive reflex expensive: **healing costs titanium every round it runs,
whether or not damage is arriving.** A cheap, persistent, credible threat that never commits is
therefore priced very differently here than a real attack: it buys rounds of enemy heal spend at
1 Ti per 4 HP repaired, against our cost of merely existing nearby. This is the same family as
[`ammo-drain-baiting`](ammo-drain-baiting.md), but wololo supplies the missing mechanism —
**the tax lands because the reflex is unconditional, and it stops landing the instant they
condition it.**

WHAT WOULD KILL IT — **Three hard limits.** (1) **It is an opponent property, not a rule
property.** wololo's own account is that it evaporated within days once opponents noticed; any
plank built on it must assume a short half-life and be cheap to abandon. Sweep 15's standing
caution applies with full force — this is a marker of *these* opponents' habits, not a mechanism
of the game. (2) **We have not measured whether the top of our league actually has an
unconditional defensive reflex.** wololo's finding is that BC2021's did; asserting it of sporks
or Clankers without a measurement would be exactly the "true quote, invented referent" failure
this library exists to catch. (3) The heal arithmetic cuts both ways: an approach that induces
spending but never threatens a kill leaves them *with* the structures they built, and INDEX is
blunt that sub-threshold aggression is a 2.2:1 donation.

BUILDER HOOK — **Measure the reflex before building anything that depends on it.** In the corpus,
for games against the 1900+ band, compare the opponent's defensive spend (turret builds, healer
adjacency, ammo conversion) in the rounds *after* one of our units first enters their vision
against the same window in games where it never does. If their defensive spend rises on our mere
*presence* — not on damage — the reflex is unconditional and measurable, and the cheapest probe
is a single durable unit parked at the edge of their vision. If it does not rise, this file is
closed for our league and should be marked so.
