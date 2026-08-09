---
tactic: TRANSFERS: NO — the entire Factorio belt-throughput and balancer literature answers the saturation question, and our own measurement says we are not saturation-bound
source: https://wiki.factorio.com/Balancer_mechanics
origin: Factorio official wiki (community-maintained) — single-player game theory, not competitive-league evidence
evidence: documented
transfers: no
---

WHAT IT IS — the largest and most quantitative body of writing on conveyor networks
anywhere is the Factorio community's throughput and balancer theory. It exists, it
is rigorous, and **it is aimed at a problem we do not have.** Filed as `no` so the
next session does not spend a sweep on it.

The core distinction it makes:

> *"Balancers that are throughput limited may not be able to provide maximum output if one or more outputs are blocked."*

and the constructive result, whose referent *"the first condition"* is stated inside
the same sentence:

> *"A guaranteed method to achieve throughput unlimited balancers is to place two balancers back to back that fulfil the first condition for throughput unlimited balancers (100% throughput under full load)."*

Belt capacity is tabulated by tier — the wiki's own row for the basic belt reads
*"Transport belt 15 1.875 8 None"* under the header *"Max. throughput (Items per
game-second for two lanes)"*, and the four-tier table gives **15 / 30 / 45 / 60**
per second. **The number carries a unit definition the wiki supplies itself:** *"The
"stacks" below refers to stacks created by a stack inserter , not inventory stacks.
If no stack inserters are involved, this is equivalent to items."*

WHY IT DOES NOT TRANSFER —

- **Our binding constraint is measured and it is not capacity.** The binding-tile
  cut: genuine saturation (`DOWNSTREAM_MOVED`) is **14.3% of our blocked mass pooled
  and 0.1% at the median team-side**. Only **6.1% of our team-sides are
  majority-saturation-bound.** *"the median line of ours is not saturated at all"*
- **Splitters — the entire subject of balancer theory — are inert in this league.**
  Splitters are **58,721 of 40,363,446 carrier pushes archive-wide, 0.15%**, and
  `SPLITTER_SIDE_REJECT` binds **0.00%** for us. Merges bind **0.01%**. Core entry
  binds **one round in 1,798,862**. **There is no balancing problem here to solve.**
- **The core face has ≥7.6x headroom.** Eight orthogonally adjacent external tiles,
  each pushing ≤1 stack per round (0 exceptions in 40,363,446 tile-rounds) = 80
  Ti/round available against 10,500 Ti/game delivered ≈ 1.05 stacks/round used.
- **And it is not competitive evidence.** Factorio has no bot league. Every claim
  above is a community wiki assertion about a single-player game, correctly labelled
  as such at the top of this file. **Nothing here is a competitor's measured result.**

WHAT WOULD MAKE IT RELEVANT — a state we are nowhere near, but worth naming so the
`no` has a stated expiry: **if the terminus and repair planks in this sweep work,
our lines become connected, and the binding class shifts from `DEAD_END_*` to
`DOWNSTREAM_MOVED`.** At that point this literature becomes the right one and this
file should be reopened. **The trigger is measurable: saturation share above ~50% at
the *median team-side*, not pooled** — the pooled 14.3% already looks like a
saturation story and is not one, which is exactly the mixture trap the binding-tile
cut's §4 caught.

One thing that IS worth carrying across even now, and it is a segmentation fact
rather than a throughput fact: Factorio's own in-game belt reader defines a
measurable segment as ending at every splitter and side-load — *"It will read all
the belts in the same 'Transport line' as the belt being read. It survives going
through underground belts, but is broken by splitters and side-loading onto another
belt."* **If we ever instrument our chains, the segment boundary should be the
splitter, for the same reason.**

BUILDER HOOK — none, deliberately. **Do not build a splitter strategy.** The one
number that would change that is the median-team-side saturation share, and it is
currently 0.1%.
