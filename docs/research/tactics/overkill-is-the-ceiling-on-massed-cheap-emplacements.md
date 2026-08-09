---
tactic: What actually caps a mass of cheap emplacements is OVERKILL, and the fix is a lattice that guarantees they fire in sequence
source: https://battlecode.org/assets/files/postmortem-2024-cout-for-clout.pdf
origin: Battlecode 2024, cout for clout
evidence: documented
transfers: partial
---

## WHAT IT IS

BC2024's cheap static object was the **trap**. A team that massed them found the binding
constraint was not cost and not coverage — it was **redundant triggering**:

> *"The one nuance is preventing too many stun traps triggering at once on a single duck,
> as that's inefficient."*

Their solution was a spacing lattice designed so that the cheap objects fire **in
sequence** rather than simultaneously:

> *"Only diagonal movements can cause multiple traps to detonate at once"*

and the payoff clause of the same layout:

> *"Once the first layer of traps is detonated, another step forward will detonate another
> layer of traps, creating consistent stun coverage"*

They also record the negative result on going *cheaper* — a rival meta got traps at half
price via a unit upgrade, and copying it did not work:

> *"Although this strategy allowed us to place more traps, these traps were much less
> efficient, and it only did better against a few teams, so we got rid of it."*

**Referent, since it carries a demonstrative:** *"this strategy"* is the preceding
sentence's — teams that *"managed to quickly level up to get 3 level 6 builders and build
traps for 50% of the cost."* So the finding is: **halving the unit price of a massed
cheap emplacement made the emplacements individually worse and the strategy net-negative.**
That is a direct counterweight to any "just build more of the cheap one" reading.

## WHY IT MIGHT TRANSFER — against our ruleset

**Overkill is real for us and it has an exact threshold: 40 HP.** An enemy builder bot has
40 HP. A gunner does 7/round, a sentinel 18 per shot. **Three sentinels bearing on the
same tile deal 54 damage to a 40 HP target — 35% of that titanium and ammunition is
thrown away.** Two sentinels (36) plus one gunner (7) is 43, a 7% waste. Against the
**core** (500 HP, 2×2) overkill is impossible and concentration is free.

**So the concentration question has two different answers in our game depending on the
target, and we have never separated them:**

- **Against builders** (the thing that removes our turrets): concentrating more than ~2
  turrets on one tile is waste, and the BC2024 answer — arrange so they fire on
  *successive* rounds along the approach rather than all on one — is exactly right. Our
  version is depth along the approach axis, not breadth across it.
- **Against the core**: no overkill ceiling exists, so pile everything on one tile. This
  is the arithmetic already recorded for the sentinel file (`sentinel-file-stacking`) and
  it is why that file is about cores and not about builders.

**This also supplies the missing reason for a spacing rule.** Sweep 7 correctly noted that
The High Ground's `d² ≥ 8` does not transfer *for its stated reason* — we have no splash,
so "don't lose two to one attack" is empty. **BC2024 supplies a second reason that does
survive here: sequencing.** Emplacements arranged so an attacker crosses them one after
another extract more damage per titanium than emplacements that all bear on the same tile,
whenever the target's HP is below the combined alpha strike.

## WHAT WOULD KILL IT

- **BC2024 traps were one-shot consumables with a trigger radius; our turrets are
  persistent and fire every round.** The overkill mechanism is therefore weaker here — a
  turret that "wastes" a shot on an already-dying target simply fires again next round,
  losing 4 or 10 ammunition rather than its whole existence. **The waste is real but it is
  ammunition, not the emplacement.**
- Our turrets fire a **ray with automatic first-target selection**, so we cannot choose to
  hold fire; sequencing must be achieved by *placement*, which is a much blunter
  instrument than BC2024's trigger design.
- The half-price-traps negative is one team's one experiment, reported in a sentence.

## BUILDER HOOK

The cheapest test is a placement constraint, not a new behaviour: when siting a turret,
reject a tile whose ray substantially overlaps an existing friendly turret's ray **unless
the intended target is the enemy core**. Two rays, same axis, same tiles = the second
turret contributes only overkill against anything with ≤ the first turret's alpha.

The measurement that would price it: across our own games, the distribution of **how many
of our turrets could fire on the same tile in the same round**, and how often the target
on that tile had less HP than the combined shot. If that fraction is material, we are
buying ammunition we throw away.
