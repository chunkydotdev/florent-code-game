---
tactic: A mechanism upgrade paid ~nothing where the bot already won 80% and paid most where the matchup was hard
source: https://cdn.aaai.org/ojs/12780/12780-52-16297-1-2-20201228.pdf
origin: Stanescu, Barriga & Buro, "Using Lanchester Attrition Laws for Combat Prediction in StarCraft", AIIDE-15
evidence: documented
transfers: partial
---
WHAT IT IS — **A controlled measurement of where a capability upgrade actually shows up on the
scoreboard, and the answer is the opposite of where most testing looks.** The authors *"integrated
the model into UAlbertaBot, one of the top bots in recent AIIDE StarCraft AI competitions"*, and
changed exactly one decision:

> *"The bot uses simulations to decide if it should attack the opponent with the currently
> available units"* … *"We replaced the simulation call in this decision procedure by our model’s
> prediction."*

Against six top AIIDE-2014 bots, with the caption stating the subject — *"Winning percentages are
computed from 200 games per match-up, 20 each on 10 different maps"* — the baseline row reads
*"UAB 50.0 80.5 27.0 53.5 7.5 31.5 41.6"* and the three upgraded variants average **60.8, 63.9 and
69.7**. **And the authors say where those ~28 points came from:**

> *"It is interesting to note that the least (or no) improvement occurs in our best match-ups,
> where we already win close to 80% of the games."* … *"However, there are bigger improvements for
> the more difficult match-ups, which is an encouraging result."*

(*"our best match-ups"* refers to the modified UAlbertaBot's match-ups within that six-bot pool.)

WHY IT MIGHT TRANSFER — **It is the strongest available argument for why our verdict instrument is
mis-aimed, and it is quantitative rather than rhetorical.** PROGRAMME records that the probe pool
is dominated 87-90%; this source says that in a structurally similar setting, a genuine mechanism
upgrade produced **the least or no improvement in exactly the matchups already won ~80%** — the
authors' own explanation being that such games are *"lopsided"* and that *"one or two extra zealots do
not make any difference to the outcome"*. **So a plank that would move the top band can measure
flat on a dominated pool for a reason that has nothing to do with the plank.** That is the same
conclusion as
[`ship-the-feature-your-pool-cannot-see`](ship-the-feature-your-pool-cannot-see.md), reached from a
paper with a control rather than from a winner's judgement call — and it is the first time in this
library that the claim has a number attached.

It also says something about *which* plank: the thing they upgraded was a **predicted-outcome gate
on whether to commit**, not a new weapon. Our engine exposes the hypothetical form directly —
`can_fire_from(position, direction, turret_type, target)` ignores ammo and cooldown — which sweep
14 already built [`no-lose-engagement-geometry`](no-lose-engagement-geometry.md) on.

WHAT WOULD KILL IT — **Three limits.** (1) **The pool is six top bots, not a dominated one** — the
"best match-ups" they refer to are ~80%, not our 87-90%, and extrapolating the shape past the
measured range is inference. (2) **Their upgrade was to a decision our units mostly cannot make:**
UAlbertaBot's gate decides whether to *attack or retreat with mobile units*, and our damage is
immobile — a turret cannot withdraw, so for us the same gate must fire at **placement** time,
before the cost is sunk, which is a strictly harder problem. (3) The paper is optimising *combat
prediction*; our binding constraint per INDEX is the **heal arithmetic**, not target selection,
and a perfect commit gate does not change a 2.2:1 exchange rate — **it only stops us entering it.**

BUILDER HOOK — Nothing to build; this file changes how a result is *read*. **When a plank measures
null on the dominated pool, this is the sourced reason that null is uninformative**, and it should
be recorded as such per `ship-the-feature-your-pool-cannot-see`'s verdict template. The measurement
that would confirm the shape locally: for any plank we have already run, compare its effect on the
weakest third of the pool against the strongest third. **If effects are systematically larger
against the strongest third, we have reproduced this paper's finding in our own data, and the
dominated pool is formally retired as a verdict instrument.**
