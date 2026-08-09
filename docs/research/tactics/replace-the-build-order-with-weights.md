---
tactic: A fixed build order that cannot be improved by reordering — replace the sequence with per-unit weights that move over time
source: https://battlecode.org/assets/files/postmortem-2021-malott-fat-cats.pdf
origin: Battlecode 2021, Malott Fat Cats (finalist)
evidence: documented
transfers: yes
---

## WHAT IT IS

Malott Fat Cats hit exactly the wall our own corpus measured — **a fixed opening that
resists improvement by reordering** — and reported the negative result plainly before
reporting the fix:

> *"Our build order used for Sprint 2 was surprisingly hard to improve, in the sense that we
> couldn’t get a considerable winrate against our old bot by only changing build order."*

**Referent check.** "our old bot" is their own previous version; the instrument is self-play
win rate (see `self-play-ab-has-the-wrong-population.md` for what that instrument can and
cannot see). The claim is about *reordering a fixed sequence*, not about build orders in
general.

The fix was to stop expressing the opening as an ordered list at all:

> *"In the end we substituted our fixed build order by a more flexible one by giving weights
> to each unit and we would always try to build the unit with the lower total weight."*

> *"The advantage of building units this way is that we can change the weight over time and
> easily prioritize some units over others"*

The surrounding sentence completes the mechanism: *"Whenever that unit is build we added
that weight to its total weight"* — i.e. a **cumulative-cost priority queue**, where each
build raises that category's running total, and the next build is whichever category is
currently cheapest by weight. The opening becomes a *function of state* rather than an index
into a list, and the schedule is steered by editing weights rather than by re-sorting steps.

## WHY IT MIGHT TRANSFER

Two reasons, one structural and one measured.

**Structural: our engine already computes half of this for us.** Cost scaling is exactly
"whenever that unit is built we added that weight to its total weight" — conveyors/splitters/
barriers +1%, harvesters +5%, launchers +10%, builder bots/gunners/sentinels +20%, all
readable through `get_conveyor_cost()`, `get_harvester_cost()`, `get_gunner_cost()` and the
rest. A greedy "build whichever category has the lowest current scaled cost per unit of
value" rule *is* their scheme with the accumulator supplied by the engine. What is missing on
our side is only the **value** numerator and the **time-varying** term.

**Measured: this is precisely the shape our own data says we lack.** From
`docs/research/core-kill-incidence-cut-2026-08-09.md`:

- **17 of 30 of our r0-50 medians are identical between core-kill and non-kill games**, and
  *"Not one of those production counters is a robust discriminator."*
- Our builder-bot coefficient of variation is **0.09 against opponents' 0.26 (2.74×)**;
  builders alive 0.09 vs 0.23; sentinels 0.53 vs 1.46.

Our opening is a list. Theirs became a function. Malott Fat Cats' negative result —
*reordering the list changes nothing* — is the same finding our cut produced from the other
direction, and their conclusion was that the list itself was the wrong object.

Note carefully what this does **not** claim. Sweep 6 established that **fixed openings are
the league norm and our constant is defensible**, and this file does not re-litigate that.
Malott Fat Cats' weights still produce a near-deterministic opening on identical inputs.
The change is that the opening acquires *inputs* — and (C)'s question is exactly what those
inputs were elsewhere.

## WHAT WOULD KILL IT

- **Our economy is already measured as not-the-constraint.** Sweep 8 found cost scaling
  *never binds on harvesters* and the middle game, not the economy, is where we die. A
  build-order refactor that only reshuffles economic categories is optimising a term the
  library has already priced at zero.
- **CPU.** A weight comparison across 8 buildable categories every builder turn, every
  round, inside a 10 ms budget, is cheap — but the cost getters are engine calls, and our
  library records three opponents with conditional compute blow-ups. Cache per-round.
- **It is a mechanism, not a trigger.** Weights that never move over time reproduce the fixed
  order exactly. The value of the scheme is entirely in what varies the weights — which
  points back at `branch-on-distance-to-the-enemy-core.md` and
  `branch-on-a-milestone-not-a-round-number.md` for the inputs.
- The claim rests on **one team's self-play win rate** and no controlled comparison; it is a
  design report, not a measurement.

## BUILDER HOOK

Smallest test: replace one hardcoded early build decision with `argmin` over
`scaled_cost / hand_assigned_value` across the two or three categories that decision chooses
between, and confirm parity first — on identical weights it must reproduce the current
opening exactly. That parity run is the whole plank; the branch inputs are a separate one.

## SOURCES QUOTED IN THIS FILE

- https://battlecode.org/assets/files/postmortem-2021-malott-fat-cats.pdf

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 15 (2026-08-09), except where explicitly marked UNVERIFIED.
