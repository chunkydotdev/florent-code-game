---
tactic: reducing our own exploitability (mix over strategies, or field a population)
source: https://arxiv.org/pdf/2004.09468 · https://arxiv.org/pdf/1901.08106 · https://arxiv.org/pdf/1711.00832
origin: Czarnecki et al. 2020; Balduzzi et al., "Open-ended Learning in Symmetric Zero-sum Games", arXiv 1901.08106, 2019; Lanctot et al., PSRO, NeurIPS 2017
evidence: documented
transfers: no
---
WHAT IT IS — Given that a fixed policy admits a best response, the literature offers
exactly **two** defences and no third. **Randomise** — play a mixed strategy, unexploitable
but requiring mixing over a support that can be enormous. Verified verbatim
(`acad_spinningtops.flat`):

> "the game of Blotto requires players to mix uniformly over all possible permutations to be
> unexploitable (since the game is invariant to permutations), which is difficult for a
> human player to achieve"

**Referent:** Blotto is offered as a *counterexample* to the Games-of-Skill geometry — a
game where the mixture needed to be unexploitable keeps growing with skill. The trailing
clause is the authors' aside about why such games are not fun, not a measured result.

Or **be a population rather than a point** (`acad_openended.flat`):

> "we do not seek a single agent or mixture, but rather a population that embodies a
> complete understanding of the strategic dimensions of the game"

> "self-play assumes transitivity: that local improvements (vt+1 beats vt ) imply global
> improvements"

WHY IT MIGHT TRANSFER — it does not, and filing that is the point. **Both defences are
structurally unavailable to us.** We hold **one** submission slot, so we cannot field a
population. We have **no cross-game memory**, so we cannot mix across matches; and mixing
*within* a match costs determinism we actually want. The only analogue we could build is
**ship-cadence randomisation** — varying when and how much the shipped bot changes so a
rival's scouting sample goes stale — **and that is not in this literature at all.**

There is also a direct programme conflict: "reduce our exploitability" is a **defensive
objective**, and `NEVER PLAY DEFENCE` governs. PSRO's own framing points the other way and
is the on-programme reading of this whole sub-arm (`acad_psro.flat`):
> "robust counter-strategies that safely exploit opponents in a common competitive
> imperfect information game"

— best-respond to them while bounding your own downside, rather than hardening yourself.

WHAT WOULD KILL IT — **it is already dead for us, and two measured negatives close the
road rather than merely leaving it unexplored.** Corpus: 9 primaries, ~870 KB flattened
(Balduzzi ×2, Czarnecki, Lanctot/PSRO, Hernandez-Leal survey, Vinyals/AlphaStar, Rosin &
Belew, Pollack & Blair, Cartlidge & Bullock).

**NEGATIVE 1 — nobody quantifies the exposure a best-responder needs.**

| term | hits |
|---|---|
| `how many games` | **0** |
| `games needed` | **0** |
| `observed games` | **0** |
| `scouting` | **0** |
| `sample complexity` | 8 — survey only, all about RL *exploration* efficiency, none about observing an opponent |

Every best-response result in this literature assumes either full analytic access to the
opponent's policy (PSRO's oracle, double oracle) or unlimited on-demand games against it
(AlphaStar's exploiters). **The sample-limited scouting regime we actually live in is
unstudied. If we want that number we must measure it in our own archive — there is no
citation to lean on, and any figure quoted as though there were would be fabricated.**

**NEGATIVE 2 — concealment is not a literature here.** `conceal` **0** · `withhold` **0** ·
`secrecy` **0** · `obfuscat*` **0** · `hidden policy` **0** · `information leak` **0** ·
`deceptive` **0**. `deception` returns 1, a passing item in a list of human traits
("fairness, reciprocity, deception") introducing behavioural game theory — not a technique.
**Every one of these papers assumes a mutually observable population and asks only how to
RESPOND to it. What to REVEAL is absent.** This independently reproduces sweep 20A's
finding that the deception seam is empty, from a completely different corpus.

BUILDER HOOK — none. **Do not spend a leg on reducing our own exploitability**, and do not
send anyone looking for the citation that prices it: it does not exist. If the question
ever becomes live, it must be measured here first — see
`our-shipped-bot-is-a-published-pure-policy.md` for the placebo design that a scouting test
would require.
