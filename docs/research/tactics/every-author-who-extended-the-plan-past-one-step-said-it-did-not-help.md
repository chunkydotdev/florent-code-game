---
tactic: (D) FOUR INDEPENDENT AUTHORS, THREE LEAGUES, ONE RESULT — everyone who tried to use more than the first step of a computed plan reported it did not help, and two of them are contest winners reporting it about their own bots
source: https://raw.githubusercontent.com/teccles-halite/halite3-bot/master/README.md
origin: Halite III (teccles 1st, TheDuck314 6th); CodinGame Fall 2020 Challenge (Agade, 2nd); AI Challenge Planet Wars (Jay Scott)
evidence: documented
transfers: yes
---

## WHAT IT IS

The sweep hunted for cases where multi-step planning lost. The cleanest class is not "a
planner lost a tournament" — it is **authors reporting that lengthening their own plan bought
nothing**, in their own postmortems, about their own bots.

**1. The Halite III winner tried it and it never worked.** teccles:

> *"I tried adding in plans about what square would be mined after the first one. These never
> helped - I suspect because they weren't reliable enough."*

**Referent check.** *"plans about what square would be mined after the first one"* extends his
per-turn target selection from one step to a sequence; *"These"* are those plans. He is
describing his own bot, the one that won.

**2. Halite III's 6th place looked for a way and did not find one.** TheDuck314:

> *"At one point I spent quite a bit of effort trying to think of a way to do more
> sophisticated planning"*

> *"But I didn't come up with anything good."*

**Referent check.** The full sentence is *"At one point I spent quite a bit of effort trying
to think of a way to do more sophisticated planning, where for example we would explicitly
model the whole trip and search over possible mining paths to find the fastest one."*

**3. A CodinGame runner-up ran a real beam search and tried to use more of its output.** Agade,
Fall 2020 Challenge (2nd), whose bot searches sequences with *"uncapped depth, beam width 350
and 30ms computation time"*:

> *"This never showed promise."*

**Referent check, and it must be given because the demonstrative is doing all the work.** The
preceding sentence states what was tried: *"Thus I tried, instead of playing the action leading
to the highest score, playing the action starting most of the top N (e.g. 10) sequences of
actions found by the beam search."* So *"This"* = using the *distribution over sequences*
rather than only the head of the best one. **He plays the first action of the best sequence
and discards the rest.**

**And in the same postmortem, more search bought nothing either:**

> *"I found locally that giving myself more search time and beam width did not improve playing
> strength."*

**4. Deep lookahead in Planet Wars was a total bust.** Jay Scott, on his oddshrimp4.1:

> *"I tested depths up to 30 turns ahead. Total bust! The winner was the most traditional
> version, which makes choices on alternate turns with no gaps."*

**Referent check.** *"depths"* are the choice-point depths in his "lattice search" — an
alpha-beta variant in which choice points may sit at arbitrary depths with the null move
assumed in between. *"The winner"* is **the best-testing variant of his own bot**, not a
contest winner.

**And across the whole 2010 contest field, the deliberative method was a disimprovement:**

> *"alpha-beta was often a disimprovement, or at least difficult to make work well"*

> *"just as other contestants from #1 Gabor Melis to #350 krokokrusa found"*

## ⚠ THE COUNTERWEIGHT, FILED BESIDE IT RATHER THAN BURIED

**The same Jay Scott page reports that adding lookahead was the biggest single improvement to
that bot.** *"The key improvement to start the oddshrimp3.x family is lookahead search."*, and
*"Oddshrimp4.1 has a plain, fixed 6-ply search."* His estimated contest ranks rise from roughly
35 (static analysis, no lookahead) through 20-25 to about 5. **Those ranks are his own
post-hoc estimates from test tournaments against downloaded bots three years after the contest,
not placings; his actual entry ranked 130.**

So the shape of the result is not "lookahead is useless". It is narrower and more useful:
**a fixed, shallow, regularly-spaced search helped; extending its depth, using more of its
output, or spending more time on it did not.**

## WHY IT MIGHT TRANSFER

- **It bounds the ambition of the whole topic before any plank is written.** Our project
  lead's question, quoted from the sweep brief rather than from any source, is *"bigger plans
  than that, more steps"*. **Four authors in three leagues
  tried exactly "more steps" and reported no gain**, two of them while winning or nearly
  winning their contests.
- **The one thing that did pay is the cheapest thing** — a shallow fixed-depth evaluation of
  the immediate move — and we already have its analogue in closed form: the library's heal
  arithmetic (4.00 HP/Ti versus 1.80 HP/Ti best damage, 8.00 on a stacked tile) *is* a
  one-step evaluation of the only exchange that matters.
- **The budget argument is ours, not theirs.** Agade had **30 ms per turn for the whole
  board**; we have 10 ms **per unit**. Every one of these negatives was measured with more
  compute than we have.
- **It explains our own history rather than contradicting it.** The library's standing
  observation is that every gain on our current line came from removing a mechanism. This is
  the same finding, arrived at independently, by people whose bots are stronger than ours.

## WHAT WOULD KILL IT

- **Halite III's plans failed for a stated reason that may not be ours** — *"I suspect because
  they weren't reliable enough"*, i.e. opponent interference made the second step's premise
  unreliable. Our map is smaller, our buildings are immobile, and enemy core position is known
  from symmetry at round 0. **A two-step plan here may be far more reliable than a two-step
  mining plan in Halite III.** That is the strongest argument against transferring this file
  wholesale, and it is not addressed by any source.
- **None of these are ablations with populations.** *"never helped"*, *"never showed
  promise"*, *"total bust"* are author verdicts from self-play testing, with no game counts.
  The one number in the family (*"about once per game on average"*, filed in
  [`drop-the-step-you-cannot-do-and-reorder-around-it`](drop-the-step-you-cannot-do-and-reorder-around-it.md))
  is about a different mechanism.
- **Coordination plans are a different object from lookahead plans**, and the sweep's (C)
  result says the coordination kind *did* measurably pay — see
  [`set-plays-were-ablated-and-set-plays-won`](set-plays-were-ablated-and-set-plays-won.md).
  **This file is about sequences one agent computes for itself. It says nothing about plans
  several units share.**
- **Selection bias.** Authors write up what surprised them. Nobody writes "I extended my plan
  and it worked exactly as expected."

## BUILDER HOOK

None — this is a prior, and the prior is: **before building any two-step plan, state what makes
the second step's premise reliable here that was not reliable in Halite III.** If the answer is
"the enemy core does not move and our buildings do not move", that is a real answer and the
plank is worth attempting. If the answer is "we hope", this file is the reason not to.

## SOURCES QUOTED IN THIS FILE

- https://raw.githubusercontent.com/teccles-halite/halite3-bot/master/README.md
- https://raw.githubusercontent.com/TheDuck314/halite2018/master/README.md
- https://raw.githubusercontent.com/Agade09/Agade-Fall2020-Challenge-Postmortem/master/README.md
- http://satirist.org/ai/planetwars/

Every quoted string above was verified verbatim by literal grep against the flattened primary
text during tactics sweep 18 (2026-08-09).
