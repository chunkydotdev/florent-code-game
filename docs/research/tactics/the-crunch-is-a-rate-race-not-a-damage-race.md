---
tactic: THE CRUNCH — the field's named mechanism for turning an economic lead into a dead enemy base, and it is sized as a RATE, not a damage total
source: https://battlecode.org/assets/files/postmortem-2020-java-best-waifu.pdf
origin: Battlecode 2020 / Java Best Waifu (2nd, seeding); the same manoeuvre described independently by The High Ground (2020)
evidence: documented
transfers: yes
---
WHAT IT IS — Battlecode 2020's whole field converged on one named move for
converting a won economy into a destroyed enemy HQ. Java Best Waifu states the
problem in the exact terms of our incidence question — they had the lead and
needed a way to *cash it*:

> *"It only remained to capitalize this into a Win Condition, and this was only
> possible with Delivery Drones"*

Referent: "this" is the giant vaporator lattice described in the preceding
sentences — i.e. their finished economy. And the mechanism they cashed it with is
sized explicitly against the defender's **removal rate**, not against the
target's HP:

> *"The idea is to build a huge economy and then spawn a horde of Drones and
> Landscapers and then crunch the enemy HQ with so many of them at the same time
> that even by killing one each turn it wouldn’t be able to stop them"*

The High Ground describes the same move from the outside, and names the
components:

> *"Soon before the lattice would flood, terraform/attack teams would “crunch”
> with their drones, removing enemy landscapers from their turtle wall and
> replacing them with their own, then burying the enemy HQ."*

Note what the crunch is made of: it is **not** a damage push. It is (a) removal
of the defender's repair bodies, (b) substitution of your own bodies onto the
tiles they vacated, (c) then the kill. Three phases, and the first two are
displacement, not damage.

WHY IT MIGHT TRANSFER — This is the field's independent arrival at the arithmetic
this library derived from our own engine. Our standing note says *"our defender's
heal is adjacency-capped at ~16 HP/round per tile while the attacker's damage on
that tile is capped only by titanium"* — concentration, not more damage. Java
Best Waifu's sentence is the same claim from the other side: overwhelm the
**per-turn** removal capacity ("even by killing one each turn"), and HP totals
stop mattering.

The phase structure transfers piece by piece into our ruleset, and unusually well:

- **(a) remove the repair bodies.** Our builder attacks *cannot* touch enemy
  builder bots at all — but the **launcher** can, at 20 Ti, no ammo, grabbing
  either team's builder. That is our drone. Sweep 12 already found the field uses
  the launcher defensively; this is the offensive half of the same verb.
- **(b) substitute our own bodies.** A builder bot standing on a core footprint
  tile is the library's measured 8.00 HP/Ti stack. Taking the tile an enemy
  healer just vacated is the *defensive* version of the same move, already filed
  as [`retake-the-vacated-tile`](retake-the-vacated-tile.md).
- **(c) then the kill.** [`the-defenders-reserve-and-what-defeats-it`](the-defenders-reserve-and-what-defeats-it.md)
  already gives the threshold in sentinels.

The reason this file exists separately from those three is the **ordering
claim**: the crunch is not "do (a), (b) and (c)", it is "(a) and (b) must be
*complete* before (c) starts". Sub-threshold fire before the healers are cleared
is the 2.2:1 donation.

WHAT WOULD KILL IT — The rate argument only holds if the attacking bodies arrive
**simultaneously**. Java Best Waifu's horde was spawned from a finished economy
and flown in by drones; our equivalent has two hard rate caps the 2020 engine did
not have. The core spawns **≤1 builder per turn**, and each builder adds **+20% to
the team's ONE GLOBAL cost scale** (corrected s26 — the scale is a single additive
team factor, not per-category, so every builder makes every *turret* dearer too).
So a "horde" is a savings problem measured in turns, not titanium — and turns are
not purchasable, while the bodies you buy inflate the guns you still need. Second, our only long-range mover is the launcher
throw, and the library measured that **96.4% of enemy victims are off the landing
tile within one round** and post-throw dwell is one round: throws displace, they
do not deliver a standing force. If the bodies trickle in, the defender's heal
rate is never exceeded and every one of them is a donation.

The other killer is the counter Bagger288 shipped against exactly this, in the
same season:

> *"A final shoutout goes to Bagger288, who implemented a strategy where their
> landscapers would self-destruct and be replaced with net guns if they detected
> they were soon going to get crunched on."*

A defender who *detects the commit* and converts repair bodies into turrets
inverts the exchange. Assume a strong opponent can do this to us; our own
`self_destruct()` plus a builder's build action is the same two-step and costs
nothing but the cooldown.

BUILDER HOOK — Make the commit a **two-gate** rather than a fire decision. Gate 1
(clearance): count enemy builder bots orthogonally adjacent to the target core
tile; do not open fire while that count is above the number our bearing turrets
can out-damage. Gate 2 (simultaneity): require the attacking assets to be *in
place* in the same round, not en route — count them with `can_fire_from` on the
target tile rather than by position. Both counts are already cheap; the change is
that firing is conditioned on the *clearance* count, which nothing in our bot
currently reads.
