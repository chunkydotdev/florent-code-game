---
tactic: treat the ladder slot as the primary information leak — exposure is dominated by SHIPPING, not by testing
source: https://arxiv.org/pdf/2004.09468 (Appendix B); local measurement on corpus/league_matches.tsv
origin: Czarnecki et al., "Real World Games Look Like Spinning Tops", arXiv 2004.09468, 2020 (rules-level fact) + in-repo measurement 2026-08-11
evidence: documented (the information-structure fact); inference (that any rival acts on it)
transfers: partial
---
WHAT IT IS — In a deterministic, fully observable game a pure strategy's behaviour **is**
its identity, and every game played transmits it. There is no separate act of revealing:
playing is revealing. Verified verbatim (`acad_spinningtops.flat`):

> "Note, that with pure policy, and fully observable game, the only way to sent information
> to the other player is by taking an action (which is observed)."

*(`sent` is the authors' typo, reproduced.)*

> "Our goal is to be able to encode identity of a pure strategy in actions it is taking, in
> such a way, that opponent will be able to decode it."

**⛔ REFERENT WARNING, and it is the reason this file exists rather than a stronger one.**
That passage is **not** a finding about opponents scouting each other. It is a
*construction*: the authors are building "n-bit communicative games" in which agents
deliberately signal their identity, in order to prove a lower bound on how many strategies
a game must contain. **Cite it for the MECHANISM — with a pure policy in a fully observable
game, actions are the only channel and they are observed. Do NOT cite it as evidence that
anyone reads our replays. The authors measured nothing of the kind.**

The local half is measured: **98.0%** of our league match table (34,913 of 35,642 rows) is
matches between other teams, and the platform serves third-party replays. **A bot holding
the ladder slot publishes itself at roughly 6 games/hour for as long as it is active; a
prototype fired in a private 5-game unrated leg shows itself five times.** Exposure is
dominated by shipping, not by testing.

WHY IT MIGHT TRANSFER — this is the one item in the sweep that **survives rule 6's
carve-out without a live leg.** Our bot is a near-pure policy, the game is fully
observable, replays are served: "our shipped bot publishes its behaviour" is the game's own
information structure, in the same class as "a conveyor has out-degree 1". It is not a
behavioural inference about opponents.

The practical consequence inverts the intuition the programme would otherwise carry: the
secrecy cost of a prototype leg is **negligible** next to the standing cost of holding the
slot. That removes "it reveals our tricks" as an argument against firing unrated legs,
which sits alongside `WHAT LOKI IS` rule 5 (unrated games are free) rather than against it.

WHAT WOULD KILL IT — the channel is **narrower than the theorem's idealisation**, in two
measured ways, and both cut in our favour:
* Our bot is not fully deterministic in effect — map, spawn geometry and opponent behaviour
  vary, so a single replay under-determines the policy.
* **`print()` is stripped from platform-downloaded replays** (stdout empty in 30,664 of
  30,664 `BotOutput` events). A rival reading our replays sees positions and entity events
  only — no internal state, no arm tags, no mode flags. The instrument gap that broke
  LOKI-14's prereg protects us here.

**AND THE HALF THAT IS NOT ESTABLISHED MUST NOT TRAVEL WITH THE HALF THAT IS.** That we
*are* published is a rules fact. That any rival *acts* on it is an inference with zero
supporting evidence in our archive, and welding the two is precisely how the barrier-form
spawn lock failed. Under rule 6 the second half needs a live leg before anything is built
on it.

BUILDER HOOK — none as a bot plank, and that is the correct answer for now. If the
inference is ever tested, the design constraint is already known from a peer lane's
retraction: **a scouting-shaped effect must be tested with a placebo shipped at a RANDOM
time, not with a before/after around a real ship** — a 1.46x hazard that looked causal
turned out to be a hump straddling t=0 rather than a step at it, with the placebo alone
reaching 1.26.
