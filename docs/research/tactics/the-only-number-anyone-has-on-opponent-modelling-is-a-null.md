---
tactic: (C) The payoff of deception and opponent-modelling has essentially never been measured — and the one clean measurement is a NULL
source: https://github.com/TheDuck314/halite2018
origin: Halite III 2018 / TheDuck314 (opponent-prediction neural net); CodinGame "Ocean of Code" 2020 / kovi (opponent-specific counter); Battlecode 2019-2026 and the IEEE ToG 2018 StarCraft-competition survey as negatives
evidence: documented
transfers: partial
---
WHAT IT IS — **Sweep question (C), answered across five leagues, and the answer is worse than
"anecdote": the field has almost never even tried to measure this, and the one competitor who
built a real opponent model and reported a result reported nothing.**

**The null.** TheDuck314 (Halite III, 2018) built the most serious opponent model in this
sweep — a trained network predicting the opponent's next move, used to license aggressive
positioning:

> *"I trained a small neural net to predict, for each opponent-adjacent square, the probability
> that any opponent would move to that square this turn. Then I allowed my ships to move onto any
> square that the neural net thought was at least 98% safe."*

> *"This neural net idea was great fun to implement but seemed to have basically no impact on mu.
> Probably with some more work it could have been a net positive. It did make me more aggressive
> about playing "move" sometimes, so it probably did make my bot harder to exploit."*

(*"mu"* is the Halite ladder's TrueSkill mean — the competition's own rating. The referent of
*"This neural net idea"* is the opponent-move predictor described immediately above, not some
other network in the same bot.) **A trained, per-opponent, statistically-fed predictor moved the
author's ladder rating by nothing he could detect.**

**The retracted number.** The only positive figure anywhere in this sweep is CodinGame Ocean of
Code 2020, where kovi built a counter aimed at one specific rival, and it comes with its own
retraction inside the same sentence:

> *"I would say that it made me loose less by 5% (I didn't benchmark, and seeing final run, I'm
> not sure about anything). Also it may have false positives on other players, which i accepted."*

(*"it"* = kovi's opponent-specific detection-and-counter feature; the rival named in the
surrounding thread is jolindien. The typo *"loose"* is the source's.) **The author states the
number and withdraws it in the same breath, then names the cost — false positives against
everyone else.**

**The negatives, which are the bulk of the evidence.**

- **Battlecode 2019-2026, 22 official postmortems, 123,745 words:** `decoy`, `feint`, `deceiv`,
  `bluff`, `mislead`, `disguis`, `fake` — **zero hits each**. See
  [`nobody-in-twenty-two-postmortems-built-a-decoy`](nobody-in-twenty-two-postmortems-built-a-decoy.md).
- **Čertický, Churchill et al., "StarCraft AI Competitions, Bots and Tournament Manager
  Software" (IEEE ToG 2018)** — the definitive survey of a decade of StarCraft bot competition,
  8,783 words. `grep -c -i -E "decept|bluff|feint|fake|deceiv|mislead"` returns **0** (file
  sanity-checked non-empty; it discusses *"opponent modeling"* at length and names bots that do
  it). **Ten years of organised bot warfare, surveyed by the organisers, with no deception
  vocabulary in it at all.**

WHY IT MATTERS FOR US — **it sets the prior for every deception proposal that will be made in this
programme, and the prior is low.** Not "unproven" — *unmeasured on one side and null on the other*.
Anyone proposing a decoy, a feint, a fake build or an opponent classifier is proposing something
that (a) nobody in the comparable leagues wrote up as having worked, and (b) the one competitor who
measured a close cousin of it found flat. **The correct response is not to abandon the family — it
is to refuse to spend more than one cheap leg on it before a number exists.**

This also lands on a decision we have already taken and should not revisit:
`docs/research/opponent-recognition-feasibility-2026-08-08.md` measured in-bot lineage recognition
at **0.380 five-fold-CV accuracy against a 0.309 majority baseline** and recommended not building a
classifier. **TheDuck314 and kovi are the external corroboration for that call** — one league found
the model worthless, the other found it unbenchmarked and prone to false positives on the rest of
the pool, which is exactly the failure our own feasibility study predicted.

WHAT WOULD KILL IT — this is a survey of the literature's *measurement practice*, so what changes
it is a measurement, not a rule. Note two honest limits: (i) TheDuck314's null is one bot in one
game whose combat is a simultaneous-move collision problem, and a null on *movement prediction* is
not a null on *provoking a reaction*; (ii) competitor self-reports are biased toward what people
found interesting to write about, so an unmeasured tactic that quietly worked would be invisible
here. **Neither limit rescues the positive case; both just stop this file being over-read.**

BUILDER HOOK — **the hook is a rule for the mill, not a plank.** Any deception-family leg must
pre-register the number it will produce and the branch on which it dies, because **this literature
shows the default outcome is a leg that produces a story instead of a figure.** The cheapest real
number available to us needs no games at all: re-cut
`docs/research/opponent-reaction-atlas-2026-08-09.md` for whether *any* opponent behaviour changes
after a non-threatening structure of ours enters their sensing range. If nothing moves, this whole
family closes on existing data.
