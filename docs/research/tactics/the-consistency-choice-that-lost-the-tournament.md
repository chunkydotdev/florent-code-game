---
tactic: FAILURE MODE — a team explicitly traded mean for variance, shipped the "most consistent" bot, and lost, because consistency is defined against a population that then moved
source: https://battlecode.org/assets/files/postmortem-2019-oak.pdf
origin: Battlecode 2019 / Oak's Last Disciple
evidence: documented
transfers: yes
---

## WHAT IT IS — arm C's "in either direction" case, with a documented outcome

Arm C asked who shipped a change that traded mean for variance **in either
direction**. Oak's Last Disciple traded *toward* variance reduction, said so,
and the tournament falsified it — which makes this the most useful arm-C
document in the corpus, because it carries a result.

**The diagnosis is a race whose outcome was a coin flip.** In the contested-cluster
matchup they identified that neither side reliably won:

> *"When facing other cheesy bots, it is literally a coin toss who gets the
> contested clusters. In Battlecode, experience has told me that consistency is
> really valuable."*

**The meta they were reasoning against is an explicit intransitive cycle**, which
is what makes "consistency" well-defined at all:

> *"Rush > Greedier/Cheesier bots > Greedy/Cheesy bots > Eco bots > Rush"*

**The decision, stated as a decision:**

> *"we came to the conclusion that our pre-Sprint eco bot was the most consistent
> one, so we ended submitting it for the final tournament"*

**And the failure, with the assumption named by the authors themselves:**

> *"In our case, we greatly underestimated the amount of greedy and cheesy eco
> bots around."*
> *"Our assumption that the eco bot was the most consistent was assuming that
> there would be a relatively equal proportion of the strategies described."*
> *"However, at the final tournament, there were almost no rush bots left and the
> more conservative bots were heavily punished by not fully investing into
> expansion."*

**Referent check.** "the strategies described" are the four in the cycle above.
"the eco bot" is Oak's own pre-Sprint submission. The failure is *not* that the
consistency reasoning was wrong; it is that **"consistent" is only defined
relative to a mix of opponents, and the mix was not stationary.** Their variance
minimisation was computed against a uniform field and cashed out against a field
that had collapsed onto one strategy.

This is the same team whose consistency quote already appears in
[`all-in-variance-is-a-ladder-tax`](all-in-variance-is-a-ladder-tax.md), where it
supports the case *for* consistency. **That file and this one are the two halves
of one lesson and should be read together:** consistency is correctly priced only
against a population you have actually measured.

## WHY IT MIGHT TRANSFER — against OUR ruleset specifically

**Because the non-stationarity Oak got wrong is a thing this repo has now
measured on its own ladder, twice.** Sweep 22 found an opponent shipping **13
versions** in our archive, **4 in the 4.5 hours** before one of our leg windows,
and established over 4,157 blocks that **pooling a per-opponent statistic across
that opponent's versions overstates our expected game share against the version
we will actually face** — direction and significance replicated, magnitude
estimator-dependent. *"Every per-opponent gate, panel cell and target-band
estimate in this repo currently reads high."*

**Oak's error and ours are the same error at different scopes.** Oak computed
"most consistent" against a field mix that moved between the seeding tournament
and the finals. We compute panel win rates against opponent identities whose
*versions* move between our calibration and our leg. Oak's postmortem is the
cautionary outcome for a mistake we are demonstrably still exposed to, and it
came with a tournament exit attached.

**The transferable rule is narrow and cheap:** a variance-reduction argument
must carry the population it was computed against, with its clock. That is
`CLAUDE.md`'s standing rule — *"Numbers carry subjects."* … *"Copy the
denominator, the population, and the clock along with the number."* (two spans,
quoted separately because a bold marker sits between them in the source) —
arriving as an external cautionary tale
rather than an internal style rule.

**EFFECT ON MEDIAN KILL ROUND: this file ARGUES AGAINST a class of change that
would raise it.** Oak's conservative choice is, in our vocabulary, exactly the
r1000-adjacent trade `R1000_IS_DEFEAT` retires. Filed as a reason to be
suspicious of consistency-motivated planks, not as a plank.

## WHAT WOULD KILL IT

* **Battlecode's tournament structure is not our ladder.** Oak's population
  shifted between two discrete tournaments with a submission deadline between
  them; ours drifts continuously and we play many more games. A continuous
  ladder punishes a mis-specified population more gently and more often, which
  is *better* — the failure is loud rather than fatal.
* **The intransitive cycle is theirs, not ours.** We have no evidence our field
  has a rock-paper-scissors structure at all, and without one, "consistent
  against the mix" collapses to plain "good". **Do not import the cycle** —
  import only the caution about the mix.
* Single case, single team, single year. `evidence: documented` covers the
  quotes and the outcome; the generalisation is our inference.

## BUILDER HOOK — none yet

None. The descendant is a discipline already half-implemented: sweep 22 filed
[`block-on-opponent-version-not-opponent-id`](block-on-opponent-version-not-opponent-id.md)
and [`anchor-on-opponents-who-did-not-change`](anchor-on-opponents-who-did-not-change.md).
This file's only addition is that **the same correction applies to any
consistency or variance argument, not just to win-rate estimates** — if a plank
is justified by "it makes us more reliable", the prereg must name the opponent
population and version window that reliability was computed over, or Oak's
failure is available to us on the same terms.
