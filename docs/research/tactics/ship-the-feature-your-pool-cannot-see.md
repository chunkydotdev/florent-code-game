---
tactic: A THIRD documented override of a self-play A/B by the same winner — and the decision rule behind it
source: https://battlecode.org/assets/files/postmortem-2025-just-woke-up.pdf
origin: Battlecode 2025 / Just Woke Up (winner); BC2026 lorem ipsum supplies the effect-size comparison; BC2021 Malott Fat Cats and BC2025 SPAARK the corroborating cautions
evidence: documented
transfers: yes
---
WHAT IT IS — Sweep 15 filed
[`self-play-ab-has-the-wrong-population`](self-play-ab-has-the-wrong-population.md) on two
documented overrides by the BC2025 winner. **There is a third in the same document, and this time
the team states the decision rule in the abstract before applying it.**

The rule: *"Just because a new bot is worse against your old one doesn't mean it will be worse
against other teams."*

The third application, on a feature they had already killed once on A/B evidence (*"in our AB
testing this seemed to do way worse so we scrapped the idea"*), then reinstated:

> *"Even though in our AB tests the results of rezzing seemed to be not super meaningful, we
> agreed that it was a feature we believed should make our bot better, and even if the numbers
> against our own bots did not show it, we thought it would work better against other teams."*

**And one team publishes the effect-size divergence directly.** BC2026 lorem ipsum, on a single
change measured on both instruments: *"increased our win rat to above 85% in local scrims, and
while there was less of a benefit in online scrims, it still did show up"*. **Same sign, smaller
against real opponents** — the same direction as the ~2× inflation sweep 15 documented from a
CodinGame competitor, now seen a second time in the Battlecode family.

**And the Halite II champion states the same failure with its DIRECTION**, which sweep 15 quoted
only the first half of. The second sentence is the load-bearing one:

> *"Local testing against previous versions was helpful in the beginning, but the exercise became
> increasingly inaccurate and pointless over time. I often had versions performing much better
> online while still performing poorly against the previous version."*

**The self-pool's errors run in the direction that kills good planks**, not the direction that
ships bad ones. CodinGame's Magus (~10th Legend) reports the mirror-image error from a local batch
runner — *"I was better in local (tested with brutaltester) but worse in the arena. Overfit
nightmare."* — so both signs occur, and neither is the ladder.

**The corroborating cautions.** BC2025 SPAARK: *"Scrimmage analysis is still more important than
raw win rate against old bots."* BC2021 Malott Fat Cats hit the flat-signal wall we hit: *"we
couldn’t get a considerable winrate against our old bot by only changing build order."* And
**BC2026 lorem ipsum's published pipeline ends inside the trap**: local maps, then all maps
(reject at ~30%), then *"When we send to online scrims, we then start scrimming a lot of teams
within our rating range"* — accepting at *"roughly slightly above 50%"*, which they themselves
flag as *"(which is pretty low)"*.

WHY IT MIGHT TRANSFER — **`transfers: yes`, because it is a rule about our own process rather
than about the game.** PROGRAMME already sets `WIN_RATE_IS_VERDICT: no`, on the stated
ground that *"the probe pool is dominated (both arms win 87-90%), so a win-rate ceiling that high
cannot show an edge"* — and INDEX records our opening as a near-constant (CV 0.09). The winner's rule is the
missing half: **a null against our own pool is not evidence of no effect when the pool lacks the
opponent behaviour the feature reads.** That converts a whole class of "measured null, plank
dropped" decisions into "measured uninformative, decide on mechanism". Given that a Loki plank is
by construction aimed at behaviour our self-play pool does not contain — a *stronger* opponent's
defensive reflex — this is close to being the default case rather than the exception.

WHAT WOULD KILL IT — **This rule is dangerous in exactly the way it is useful, and that must be
stated plainly: it is a licence to ignore evidence.** The winner used it three times and won, but
three uses by one winning team is survivorship, and this corpus contains no case of a team
reporting that overriding an A/B *lost* them the season — because losers write fewer postmortems.
The safeguard the sources themselves supply is that **every override was justified by a named
population defect** (*"our bot wasn't super aggressive"*, *"the teams that we have the worst
matchups against"*), not by preference. **An override without a named, checkable reason why the
pool cannot see the effect is not this tactic; it is motivated reasoning.** And note lorem
ipsum's number cuts the other way too: the effect *did* still show up online, so a self-play null
that is a null on *sign* as well as magnitude remains informative.

BUILDER HOOK — A one-line addition to the plank verdict template, not code: when a plank measures
null on the self-play pool, record **"which opponent behaviour would this read, and does our pool
contain it?"** If the answer is "no", the verdict is `uninformative`, not `null`, and the plank
goes to the ladder rather than the bin. If the answer is "yes", a null is a real null. This costs
nothing and it distinguishes the winner's practice from the failure mode it resembles.
