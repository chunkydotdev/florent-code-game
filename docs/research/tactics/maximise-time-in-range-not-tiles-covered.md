---
tactic: The objective function for a static line is EXPOSURE (enemy time spent in range), not tiles covered — and the counter to a spread line is one concentrated wave
source: https://raw.githubusercontent.com/nknguyenhc/Terminal-Lostkids/main/README.md
origin: Terminal (Correlation One / Citadel), team Lostkids — self-described 3rd place, APAC final
evidence: anecdotal (competitor writeup; the mechanic it exploits is documented from engine source)
transfers: partial
---

## WHAT IT IS

Asked what their defensive layout was *for*, this team gives a one-line objective function
and it is not coverage. The referent of *"the structure"* is established in the preceding
sentence — *"a horizontal wall structure, with 2 entrances into and out of the base on
two sides"*:

> *"The idea is that when an opponent mobile unit attempts to reach the edge, the
> structure maximises the exposure of our turrets on enemy's units, thereby maximising
> damage on enemy's units."*

**The quantity being maximised is enemy time-in-range, purchased with walls that lengthen
the path.** Not tiles covered, not turret count, not survival.

**And they state the failure mode of the alternative, from the attacker's chair.** Two
consecutive bullets, one about a wall-heavy defence and one about a spread one:

> *"Our attack is effective against defense structure with turrets being spread out with
> little walls. This is because in that case, we use one batch of scouts so that turrets
> do not have time to destroy all scouts along the path of traversal."*

**So the counter to a distributed static line is a single concentrated wave that crosses
it faster than it can kill.** Spread buys area and loses time; the attacker chooses time.
Their own attack-side targeting rule is the same idea inverted:

> *"Count the number of turrets on each side (left, right) of the enemy's battlefield and
> change side of attack to the side with significantly less turrets."*

## WHY IT MIGHT TRANSFER — against our ruleset

**Time-in-range is a much better objective for us than tiles-covered, because our turrets
cover a RAY and not an area.** A gunner covers 3 tiles in one direction, a sentinel 5
(2 and 4 diagonally). "Coverage" of a ray is nearly meaningless; **exposure — how many
rounds an approaching builder spends on tiles our ray can hit — is the quantity that
actually converts into damage.**

Worked: a builder bot moves one tile per round (move and act are mutually exclusive). A
gunner facing a corridor gets **3 rounds of fire = 21 damage** on a bot walking its full
ray; a sentinel gets **5 rounds ≈ 45 damage** at its 9/round. A 40 HP builder dies to
either *if it walks the whole ray* — and takes **zero** damage if it steps in from the
side, which is the free counter sweep 7 already identified.

**Therefore the ablative barrier is not only HP — it is an exposure multiplier**, and
this is the reading that makes it worth more than its 10 HP/Ti. A barrier that forces one
extra step through a sentinel's ray is worth 9 damage for 3 Ti, *repeatedly, to every
attacker that takes that path*. That is a better rate than any titanium we can spend on
damage directly.

**The constraint that makes this specifically ours:** the same barrier in front of a
**gunner** blanks it entirely (the gunner's line *"stops at the first targetable tile"*).
So the exposure-lengthening wall must be placed **beside** a gunner's ray and may be
placed **anywhere** relative to a sentinel's. Terminal never had to make that distinction
because Terminal turrets shoot straight through their own walls (engine source: the
target-selection path has no occupancy or intervening-tile term at all).

## WHAT WOULD KILL IT

- **One competitor writeup.** `anecdotal`. It is the clearest statement of the objective
  found anywhere in this sweep, and it is still one team.
- **Terminal's attackers are waves of mobile units on a fixed path; ours are one or two
  builder bots that choose their own tiles.** Path-lengthening against an opponent who
  can simply approach off-axis is worth far less. **The honest version of the transfer is
  narrow: exposure only pays where the approach is already constrained** — which is why
  it composes with the choke-gate rule in
  [`cap-the-expensive-emplacement-and-gate-it-on-a-choke`](cap-the-expensive-emplacement-and-gate-it-on-a-choke.md)
  and not on open ground.
- **The "one concentrated wave beats a spread line" result is an argument against our own
  habit of scattering turrets, but it is also an argument the OPPONENT can run on us.**
  We should expect a burst of builders through the thinnest ray, not a grind.
- I did not find any published *formula* for exposure in Terminal or anywhere else in
  this sweep. The objective is stated in prose only.

## BUILDER HOOK

Replace any tiles-covered term in turret siting with an **exposure count**: for a
candidate site and facing, walk the ray and count the tiles on it that lie on a plausible
approach path to what we are defending (cheapest usable proxy: tiles closer to the enemy
core than the defended object is). Score the site by that count. It is a loop of ≤5 tiles
and costs almost nothing inside a 10 ms budget.

The measurement that would justify it first: **for turrets we have already built, how many
rounds did an enemy builder actually spend on their ray?** If the median is 0-1, our
turrets are not being approached through their fire at all, and the mix question in this
sweep is downstream of a siting problem.
