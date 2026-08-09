---
tactic: Group the emplacements so a single servicing unit reaches all of them — the tradeoff is named, and it lands harder here than where it was written
source: https://wiki.screepspl.us/StructureTower/
origin: Screeps community wiki (StructureTower); the falloff term it trades against is from screeps engine source
evidence: documented (wiki text) — the transfer is inference by this sweep
transfers: partial
---

## WHAT IT IS

The Screeps community wiki states the placement tradeoff for static defensive structures
explicitly, and it is the only place in this sweep where **clustering for logistics** is
weighed against **placement for effect**:

> *"Some players also will group their towers into an area so all are reachable from one
> room position, this allows for easy refilling with creeps in a speedy manor without
> having to travel long distances. This also allows for all towers to be similarly
> effective at w/e range their 'centered' around, this does however weaken the power they
> could have in other spots if they were placed differently."*

*(Typos "manor" and "w/e" are in the original.)*

The cost side of the tradeoff is the range falloff — the same wiki page's preceding
paragraph: *"due to the range falloff, for a tower to be at its maximum effect (either
attacking, healing or repairing) they should be closest to what action you wish to have
them preform."*

The official docs corroborate the practical framing that towers alone do not hold
(`docs.screeps.com/defense.html`): *"well-secured team of creep invaders are able to
withstand the attack by multiple towers at point-blank range. Countering such an attack
requires a symmetrical response: creep defenders."*

## WHY IT MIGHT TRANSFER — and the tradeoff LOSES ITS COST HERE

**Screeps pays for clustering in damage, because damage falls off with range. We do not:
our turrets deal full damage at every tile of their ray** (see
[`range-buys-damage-elsewhere-and-buys-nothing-here`](range-buys-damage-elsewhere-and-buys-nothing-here.md)).
**So for us the clustering tradeoff is one-sided — the logistics benefit is real and the
damage cost is zero.**

**And our "refilling" is heal reachability, which is worth far more than Screeps' energy
logistics.** Our heal is 1 Ti for +4 HP to *all friendly entities on one orthogonally
adjacent tile*, and one builder standing between clustered turrets can service a different
one each round without moving. Against a 2 damage/turn builder attack, one healer
out-repairs one attacker outright; sweep 7 put it plainly — an unhealed 25 HP gunner is 13
enemy builder-turns from death, a healed one **cannot be killed by fewer than three
attackers.**

**This is the independent second source for sweep 7's inversion of the spacing rule.**
Sweep 7 argued from our own rules that The High Ground's `d² ≥ 8` should probably be
inverted here because we have no splash. Screeps' wiki supplies a *positive* reason for
clustering — servicing reach — from a different league, and in our ruleset the reason it
gives is stronger than in the league that wrote it down.

**The counterweight is filed, not buried.** Clustering concentrates the loss: one
successful push takes several turrets instead of one, and the same wiki's Combat page
frames barriers as *"a delay to allow you to create a defensive force of creeps, than as
impenetrable defenses"*. And BC2024's overkill lattice is the argument on the other side —
see
[`overkill-is-the-ceiling-on-massed-cheap-emplacements`](overkill-is-the-ceiling-on-massed-cheap-emplacements.md).
**The two resolve cleanly if you separate the axes: cluster ACROSS the approach for
servicing, sequence ALONG the approach for damage.**

## WHAT WOULD KILL IT

- **A healer beside a gunner may be standing on its firing line and blanking it** —
  already flagged in sweep 7 and the reason clustering is `partial` rather than `yes`.
  Clustering must respect the gunner's ray; it is unconstrained around sentinels, whose
  line passes through friendlies harmlessly (probe-confirmed).
- **The heal adjacency cap.** Four orthogonal neighbours means ~16 HP/round per tile,
  which a big enough push still beats. Clustering does not make a position
  unbreakable — it changes the number of attackers required.
- The wiki is community-written and explicitly non-prescriptive; it closes the section
  with *"Its up to the user to determine their use case for their towers, many different
  users have many different placements."* **This is a stated tradeoff, not a
  recommendation, and it should not be cited as Screeps doctrine.**

## BUILDER HOOK

The measurement first, because it is nearly free and sweep 7 already asked for it and it
appears never to have been run: **what fraction of our turrets ever received a single
heal?** If it is near zero, siting-by-fire-arc is the whole problem and clustering is the
fix. The build change that follows: when siting a turret, require an orthogonally adjacent
tile that is passable, **not on the turret's own firing axis**, and within one step of
another friendly turret — i.e. site the *healer's seat* and the turret together.
