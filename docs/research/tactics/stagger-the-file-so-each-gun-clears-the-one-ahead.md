---
tactic: The only published layout doctrine for structures that block their OWN side's line of fire — stagger them, and mix blocking with non-blocking cover
source: https://dwarffortresswiki.org/index.php/DF2014:Ballista and https://rimworldwiki.com/wiki/Defense_structures
origin: Dwarf Fortress (community wiki, DF2014 ballista battery); RimWorld (community wiki, Defense structures)
evidence: documented
transfers: partial
---

## WHAT IT IS

Question (D) — *where else does a player's own structure block their own ranged attack,
and how did people lay out formations around it?* — has **no precedent in the competitive
RTS canon** (see
[`friendly-line-blocking-has-no-rts-precedent`](friendly-line-blocking-has-no-rts-precedent.md)).
It has exactly two, and they come from colony sims. **They agree with each other, and
neither answer is "build fewer".**

**1. Dwarf Fortress — stagger a file of same-facing engines.** Siege engines occupy 3×3
and fire in one fixed direction; the wiki's corridor-battery layout is built around each
engine's line clipping the one in front:

> *"Because siege engines are 3x3, they need to be staggered, so each one fires through
> the edge of the one ahead of it."*

**Referent check:** the preceding sentence is *"If you place ballistae close enough
together, you can completely cover a two or three tile wide corridor."* — so the subject
is a *deliberately massed* battery aimed down one corridor, which is our sentinel-file /
gunner-file case exactly.

**2. RimWorld — mix blocking and non-blocking structures, and set the ratio by the
angles you need to fire at.** The wiki separates the two classes explicitly:

> *"In addition, walls block line of fire."*
> *"Barricades and sandbags provide 55% cover and do not block line of fire."*

and states the doctrine that follows:

> *"The best arrangement of cover is a mix of walls and barricades/sandbags, as a pawn can
> benefit from barricades whenever they lean out from a wall. The exact ratio will depend
> on what angles the colonist needs to fire at"*

**3. And Factorio names the same constraint from the turret side.** Its one
facing-constrained turret gets a placement rule the omnidirectional ones do not:

> *"Unlike gun turrets and laser turrets, they have a limited firing arc, and should
> therefore be placed at choke points or behind walls."*

**Subject: the flamethrower turret.** *A limited firing arc is a reason to site at a
choke* — the same conclusion BC2025's winner reached empirically for their long-range
tower.

## WHY IT MIGHT TRANSFER — against our ruleset

**Our gunner is a Dwarf Fortress ballista.** Its line *"stops at the first targetable tile
(a builder bot or a building) in its facing direction"* — so **two gunners in file on the
same axis are one gunner and one 20 Ti barrier.** The stagger rule is the direct fix: put
the second gunner one tile off-axis so its ray clears the first one's footprint. This is
not a spacing *floor* (which sweep 7 correctly said does not transfer, since we have no
splash) — it is a **lateral offset requirement**, a different constraint that Battlecode
never had a reason to invent.

**Our sentinel is a RimWorld sandbag and our barrier is a RimWorld wall — with the roles
partly swapped.** A sentinel's line passes through friendly entities harmlessly
(probe-confirmed: 18 damage landed through a friendly bot *and* a friendly barrier), so a
sentinel can sit behind anything. A gunner cannot. **So the RimWorld "mixed ratio set by
firing angles" doctrine has a clean translation:**

> **Barriers and other buildings may go anywhere in front of a SENTINEL and nowhere in
> front of a GUNNER. A defensive cell containing both must be laid out so the barrier
> screens the sentinel while sitting off the gunner's axis.**

That is a concrete cell design, and it is the constructive form of sweep 7's
"the ablative screen is SENTINEL-ONLY" finding — sweep 7 established the constraint,
these two sources supply the layout that satisfies it with both turret types present.

**And it composes with the healer-seat requirement.** Sweep 7 already warned that a healer
standing beside a gunner may be standing on its firing line. The stagger/offset rule and
the healer-seat rule are the same rule applied to two different friendly objects: **the
gunner's axis is a no-build, no-stand corridor for our own side.**

## WHAT WOULD KILL IT

- **Both sources are community wikis for single-player colony sims**, not competitive
  leagues. They are `documented` as statements of those games' doctrine, and they carry no
  win-rate evidence at all.
- **Dwarf Fortress's stagger is forced by a 3×3 footprint; our turrets are 1×1**, so the
  offset needed here is smaller and the cost of getting it wrong is proportionally
  smaller too.
- The DF page's other prominent claim — that ballista arrows *"can and will kill anything
  in their path"* — is **friendly-fire damage, not line blocking**, and is a different
  mechanic that our sentinel explicitly does not have (its line does not harm friendlies).
  Filed here so the two are not conflated; the sweep leg flagged this as the item that
  reads like our mechanic at a glance and is not.
- We have no measurement of how often our own turrets are currently blocking each other.
  **If the answer is "almost never", this whole file is a solution without a problem.**

## BUILDER HOOK

Two, in cost order:

1. **Measure first, and it is a decoder question, not a game change:** for every gunner we
   built, was there a friendly building or bot on its facing ray at any point while it was
   alive, and for how many rounds? That number is the size of the prize.
2. **Then the constraint, which is three lines:** when siting a gunner, reject any tile
   whose ray passes through a friendly building or through a tile our own turrets already
   occupy; and when siting *anything else*, reject tiles that lie on an existing friendly
   gunner's ray. A no-build corridor of ≤3 tiles per gunner, maintained in the same
   structure the bot already uses to mark turret tiles as blocked for pathing.
