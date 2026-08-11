---
tactic: redundancy-invariance as a lint rule on every pooled opponent statistic
source: https://arxiv.org/pdf/1806.02643
origin: Balduzzi, Tuyls, Perolat, Graepel (DeepMind), "Re-evaluating Evaluation", NeurIPS 2018
evidence: documented
transfers: yes
---
WHAT IT IS — Balduzzi et al. prove that uniform averaging over an evaluation population is
**not invariant to duplicating members of that population**, and give a worked
counterexample in which nothing about any agent changes — only the census — and the
ranking flips. Verified verbatim (`acad_balduzzi_reeval.flat`):

> "Uniform averaging is not invariant to adding redundant agents; concretely div(A) = 0
> whereas div(A0 ) = (−1.15, 1.15, 0, 0), falsely suggesting agent B is superior."

**Referent, stated because it is load-bearing:** `A` is a three-agent rock-paper-scissors
logit matrix (A, B, C); `A'` is the *same matrix with agent C duplicated* into C₁ and C₂.
No agent's strategy changed. Uniform averaging then reports B as superior. This is a
documented **wrong conclusion produced purely by a mis-weighted population**.

And the mechanism stated for ratings specifically:

> "Secondly, an agent's Elo rating can be inflated by instantiating many copies of an
> agent it beats (or conversely). This can cause problems when Elo guides
> hyper-optimization methods like population-based training"

**Referent of "This":** the inflation mechanism itself — a rating rising because the
evaluation population contains many copies of something the agent beats. The paper's
desired property is stated plainly: "redundant copies of an agent or task to the data
should make no difference."

WHY IT MIGHT TRANSFER — **because this is our bug, stated as a theorem, and it says our
statistic was wrong before we ever looked at which version they fielded.** A team shipping
v7, v8, v9 with small edits is *literally* Balduzzi's C₁/C₂: several near-duplicate players
sharing one team id, each contributing equally to a uniform average. The sweep-22 incident —
a cell statistic pooled over 13 versions of one opponent, 60% of it from one dead version —
is his Example 1 with the roles swapped. The diagnosis transfers with **zero
modification** and it is computable offline from our archive; nothing agent-side is
required.

There is a second, independent bite: the paper states that "Elo bakes-in the assumption
that relative skill is transitive", and **our currency is Elo**. The ladder rating we
optimise carries the defect natively, which is worth holding next to the measured
`R1000_IS_DEFEAT` / game-share arithmetic rather than treating rating as ground truth.

WHAT WOULD KILL IT — the *diagnosis* transfers; the **fix mostly does not**, and saying so
is the point of this file.
* Nash averaging needs a reasonably dense win-rate matrix over the **same** set of
  players. Ours is sparse and its players — the opponents' retired versions — are
  **unplayable**. The maxent Nash would be computed over a population that no longer
  exists.
* Nash averaging answers *"who is best overall"*. Under `R1000_IS_DEFEAT` and a game-share
  currency we do not want "overall" — we want the reachable band right now, which is what
  `tools/target_value.py` already gates on. **Use the invariance property as a lint rule;
  do not adopt the Nash score as a target.**
* **AND THE APPLICATION TO VERSIONS IS OUR INFERENCE, NOT THE AUTHORS' CLAIM.** The paper's
  redundancy argument is entirely about *simultaneous* duplicate agents in one evaluation
  matrix; it never discusses the same agent at two points in time. Treating a retired
  version and a current version as two distinct players sharing a team id is structurally
  identical to C₁/C₂ and is a good inference — but it is the research arm's, and must be
  labelled as such wherever it is repeated.

BUILDER HOOK — a lint rule, not a plank. Any time we average over an opponent, print the
per-version `n` alongside the mean, and check the invariance property by hand: **would this
number change if one of their versions had played twice as many games?** If yes, the
number is measuring our sampling schedule as much as their strength. The concrete
instance is already measured — see `block-on-opponent-version-not-opponent-id.md`, where
the pooled statistic overstates by **8.00pp of game share** with the sign known.
