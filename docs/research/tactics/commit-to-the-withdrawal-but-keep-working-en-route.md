---
tactic: Once the withdrawal starts it is not re-decided — but the unit still takes work it passes, and re-targeting needs a large hysteresis constant
source: https://raw.githubusercontent.com/teccles-halite/halite3-bot/master/README.md
origin: Halite III 2018 — teccles (2nd place) and TheDuck314 (3rd place); Battlecode 2025 SPAARK
evidence: documented
transfers: yes
---

## WHAT IT IS

Two rules that look contradictory and are not. teccles, 2nd in Halite III:

> *"When ships start to return towards a dropoff or a shipyard, they carry on until they get there."*

**No re-decision of the destination.** But the *action each turn* is still
re-evaluated:

> *"Every turn, a ship which is returning considers instead stopping and mining. It does so if the value of the turn for a ship at its destination dropoff is less than the halite it would gather."*

**Referent check.** Both sentences are from the section headed *"Returning to
base"*; "they" and "a ship which is returning" are the same withdrawing ships.
**The commitment is to the destination; the turn is still spent on whatever is
worth more.** SPAARK reached the same shape from the other side — *"Bots refill
if they pass by a tower that has paint in it, even if they are almost full"*
(BC2025): take the resupply opportunistically when it is free, never as a trip.

And the anti-churn constant, from TheDuck314 (3rd):

> *"stay on the current square unless the target square has more than 3x the halite of the current square"*

with the diagnosis stated immediately before it: *"just using this formula the
ships were way too eager to abandon the current square for a nearby richer
square."* The fix he names alongside it is a distance fudge factor of 1.75.

teccles' *second* return trigger is the one worth naming separately, because it
is a withdrawal trigger denominated in **opportunity cost** rather than danger or
supply:

> *"The best score they get for any square is too high"*

i.e. the ship leaves when the best forward work available is worth less than the
trip home is worth. **This is the only economically-framed withdrawal trigger in
the sweep.**

## WHY IT MIGHT TRANSFER

**The hysteresis half is the part our dwell number most plausibly needs.** A
raider that re-picks its target every round in a field of near-equal candidates
will oscillate, and oscillation looks *exactly* like dwell: many rounds forward,
few structures placed, no single cause. This library already holds the general
form — *commitment is one constant added to last round's answer*
([`add-a-constant-to-the-incumbents-score`](add-a-constant-to-the-incumbents-score.md)) —
and TheDuck314 supplies the aggressive end of the range: **3x, not 1.1x.**

**The opportunistic-work half maps onto our act/move exclusivity.** A builder
walking anywhere passes tiles where `can_build_conveyor` is true. Under teccles'
rule, the walk is not sacred: if the tile it is standing on is worth an action
this turn, take it and arrive one round later.

## WHAT WOULD KILL IT

* Halite ships move every turn and mine every turn; our builder does **one or the
  other**, so "work en route" strictly extends the journey rather than being free.
  The comparison teccles makes (value of a turn at the destination vs value here)
  is still well-posed for us, but the constant is not importable.
* teccles' opportunity-cost trigger requires a **value for a turn spent at home**,
  which for us is close to undefined under `R1000_IS_DEFEAT` — economy is
  instrumental and does not score. **A literal port would compute the wrong
  numerator.**
* If our raid target selection is already sticky, the hysteresis plank is a null
  before it starts. **Grep the incumbent before pre-registering it** — this is the
  failure mode `CLAUDE.md` names: *"the cheapest possible null is a leg that tests
  a feature we already shipped."*

## BUILDER HOOK

Cheapest discriminating check, no bot change: over forward raider-rounds, how
often does the chosen target change between consecutive rounds while the previous
target remained legal? A high rate means oscillation and the 3x hysteresis
constant is the intervention; a low rate closes this road.
