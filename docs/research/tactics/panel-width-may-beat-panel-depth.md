---
tactic: spend the unrated budget on MORE DISTINCT OPPONENTS rather than more games per opponent
source: https://arxiv.org/pdf/2004.09468
origin: Czarnecki, Omidshafiei, Gidel, Tracey, Balduzzi, Tuyls, Jaderberg (DeepMind), "Real World Games Look Like Spinning Tops", arXiv 2004.09468, 2020
evidence: documented (theorem + empirical validation over nine OpenSpiel games); the application to our panel is the research arm's inference
transfers: partial
---
WHAT IT IS — In "Games of Skill" — a transitive backbone with a fat cyclic middle — whether
you make monotone progress or spin in cycles is governed by **how many distinct opponents
you evaluate against**, and it behaves as a phase change rather than a gradient. Verified
verbatim (`acad_spinningtops.flat`):

> "The theorem shows that the size of the population, against which we are training, has a
> strong effect on the probability of transitive improvement, as it reduces the variance of
> W at a quartic rate."

**Referents, stated because two demonstratives appear:** "The theorem" is **Theorem 4**,
`S̄ₜ₊₁ > S̄ₜ − W`, where `S̄ₜ` is the population's average transitive strength at time t;
**`W` is the zero-mean noise term in that inequality**, with variance `σ²/m⁴`, and **`m` is
the population size** — so "it" is the population size. This quotes the authors'
characterisation of their own result and takes no position on the exponent.

> "For small population sizes, training does not converge and cycles for all games"

> "when the population exceeds a critical size, training converges to the best strategies in
> almost all experiments"

WHY IT MIGHT TRANSFER — **because it contradicts how this repo currently frames its own
power problem, and the two framings imply opposite spends of the same budget.** Our
documented constraint is *not enough games per cell* — a 25-game window has an MDE of
~39pp and a same-bot swing of 12pp between consecutive windows, so the standing
prescription is to pool windows. Spinning Tops says the binding constraint may instead be
*not enough distinct opponents*: too few, and apparent progress is actually cycling. Under
`WHAT LOKI IS` rule 5 unrated games are free and the rate limit (5 per 20 minutes) is the
only cadence constraint — so the real decision is **how to allocate** those five, and the
two framings answer differently. That makes it discriminable with one leg and no bot code.

WHAT WOULD KILL IT — three things, and the second is the serious one.
* The theorem is about a training loop with an improvement oracle. **We have no such
  loop** — we hand-write planks. The empirical shape is the transferable part; the theorem
  is not about us and must not be quoted as though it were.
* **The theorem's population is a set of strategies you can evaluate against AT WILL; ours
  is a set of teams that change identity underneath us.** Widening the panel adds opponents
  *and* adds drift sources — at a measured median version lifetime of **1.17 hours** — so
  the variance reduction the theorem promises may be cancelled by non-stationarity the
  theorem does not model. **The paper assumes a fixed game; our game's players are not
  fixed.** All nine validation games are two-player zero-sum symmetric with a **static**
  opponent set; there is no version churn anywhere in the experiment.
* Panel width trades against `tools/target_value.py`: more opponents means reaching into
  bands where a win pays under 5 rating points. Width is only free if the added cells are
  in the reachable band.

BUILDER HOOK — one leg, no bot code, and it is cheap because unrated games are free. Split
the same total number of unrated games two ways — **narrow-and-deep** (few opponents, many
games each) versus **wide-and-shallow** (many opponents, few games each) — measuring the
same plank, and compare which arm's verdict reproduces on a second, independent run. The
question is not which arm gives a bigger effect but **which arm gives the SAME answer
twice.** Block both arms on `(opponent_team_id, opponent_version)` per
`block-on-opponent-version-not-opponent-id.md`, or the wide arm will simply absorb more
drift and look worse for a reason that has nothing to do with width.
