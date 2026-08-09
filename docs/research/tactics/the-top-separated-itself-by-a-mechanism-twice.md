---
tactic: In one league the top separated itself by a mechanism the mid-field lacked — twice, with a natural control
source: https://certicky.github.io/files/publications/ecgg15_chapter-competitions.pdf
origin: Churchill, Preuss, Richoux, Synnaeve, Uriarte, Ontañón, Čertický, "StarCraft Bots and Competitions" (AIIDE/CIG 2011-2015)
evidence: documented
transfers: partial
---
WHAT IT IS — **The clearest "different in KIND" evidence in the sweep, because it is a competition
record rather than a competitor's self-assessment, and because one year supplies an accidental
control.**

**Separation #1 — cross-game learning, AIIDE 2012.** The competition added the ability to persist
data between matches, and the adoption split by placement:

> *"Bots could now write information to disk during a match, and then read the information during
> other matches, allowing them to adjust strategies based on previous results. 6 of the 10
> entrants used this feature to aid in strategy selection, including the top 4 finishers."*

**A capability held by 60% of the field but by 100% of the top 4.** Quantified for one bot three
years later: *"AIUR came in 5th place and was a clear demonstration of how learning over time can
dramatically improve results in a tournament, going from 63% win rate early in the competition to
a final win rate of over 73%."*

**Separation #2 — combat simulation, AIIDE 2013**, credited by the authors with the win:

> *"The major addition to UAlbertaBot was a combat simulation package called SparCraft."* … *"This
> addition, combined with some additional bug fixes led to the victory."*

**AND THE NATURAL CONTROL, which is what makes this more than two anecdotes.** The CIG 2013
competition ran the *same field* with the learning feature switched off by accident:

> *"A new competition software was implemented by Tobias but not completely finished in time, so
> that the read/write function that enables learning between games had to be disabled again."*
> … *"We presume that disabling the learning was a disadvantage for the UAlbertaBot who won the
> AIIDE competition and was only runner-up to the Skynet bot here."*

**Same bots, one capability removed, and the AIIDE champion drops to 2nd.** The authors are
careful about the size of it — *"as the result provided in table 10 shows, the effect is
limited"* — and note the effect is bot-specific: *"some bots as the UAlbertaBot make good use of
online learning, whereas others, as Skynet, do not profit from it that much."*

**One counter-case, filed here rather than opposite, because it is the same category:** Halite
III's winner reports that his fanciest mechanism was worthless — *"This neural net idea was great
fun to implement but seemed to have basically no impact on mu."* **A categorically new mechanism
is not automatically the separator; it was in these two AIIDE years and was not in that one.**

WHY IT MIGHT TRANSFER — **Only the second separation transfers at all, and saying so is the point
of the file.** Cross-game learning is **structurally impossible in our engine**: there is no
persistence between matches — the 16-slot store is per-match and buffered, and sweep 6 already
recorded that *"the anti-constant result needs cross-game memory the engine forbids"*. **So the
single mechanism that most cleanly separated a top tier in a comparable league is not available to
us, and that is a firm negative worth having**: it removes a whole class of "why are they better"
hypotheses.

What remains is separation #2 — **a simulated forward look before committing** — which our engine
does support in the only form we need it: `can_fire_from(position, direction, turret_type, target)`
is the hypothetical-turret predicate and ignores ammo and cooldown, so a placement can be scored
before it is paid for. That is the same shape as
[`gains-land-in-the-hard-matchups`](gains-land-in-the-hard-matchups.md) and
[`no-lose-engagement-geometry`](no-lose-engagement-geometry.md), now with a competition record
behind it rather than one bot's postmortem.

WHAT WOULD KILL IT — **Three things.** (1) **The CPU budget.** SparCraft simulates a battle to
2000 frames; we have **10 ms per unit per turn** and an uncaught exception permanently destroys the
unit. Any forward simulation here must be closed-form or a handful of predicate calls, not a
playout — which is a large qualitative gap from what won AIIDE 2013. (2) **AIIDE 2012-13 is a
decade old and a small field** (10 entrants), so "the top 4 all had it" is 4 of 10, and the authors
themselves call the CIG effect *"limited"*. (3) The Halite III counter-case shows the inference
"the top has a mechanism ⇒ get that mechanism" fails often enough to need a specific reason each
time — and [`copying-the-top-tier-is-not-free`](copying-the-top-tier-is-not-free.md) catalogues
what that failure looks like.

BUILDER HOOK — Nothing to build. **The decision-relevant content is the negative:** cross-game
learning is off the table by engine rule, so no amount of "they must be remembering us" is a live
hypothesis, and the remaining in-kind candidate is a cheap pre-commitment predicate at **placement**
time. If a plank in that family is ever run, this file is the argument for evaluating it against
the top band rather than the dominated pool.
