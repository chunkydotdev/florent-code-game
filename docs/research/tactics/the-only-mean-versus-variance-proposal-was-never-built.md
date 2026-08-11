---
tactic: Store your own build timings as a RANGE rather than a point — the corpus's only explicit mean-vs-variance framing of arrival time, and it was never shipped
source: http://satirist.org/ai/starcraft/blog/archives/981-opening-timing-data-for-Steamhammer.html
origin: RTS theory / Jay Scott (Steamhammer author), "opening timing data for Steamhammer", 2020
evidence: documented — but the proposal itself is explicitly unbuilt
transfers: partial
---

## WHAT IT IS — arm C's direct answer, and the answer is "one person, once, and he did not do it"

Arm C asked whether any competitor reasoned explicitly about the **distribution**
of their own arrival time rather than its average. Across 65 documents and
222,488 words, **exactly one span does.** Jay Scott, laying out a design for
recording his bot's own opening timings:

> *"Even so, timings will vary from game to game, so maybe the timings should
> give low and high values, or mean and variance, or something."*

**Referent check.** "timings" are the timings of his own openings, defined in the
preceding sentences: *"Record timings for all of Steamhammer’s openings, in a
static data file to be read at startup. The timings should include the time when
each tech or production building finishes, plus the number of workers and the
army size and composition at the end of the book line"*. So this is the
distribution of **his own arrival time**, not the opponent's, and not the
distribution of game outcomes.

**And it is a proposal, not a shipped change.** The post opens:

> *"I haven’t decided whether this is what I’ll do next, still thinking. I will
> at least do something similar eventually."*

That hedge is why this file is `evidence: documented` about the *idea* and
carries no claim at all about the *result*. **There is no measured outcome
anywhere in the corpus for trading mean arrival time against its variance.**
Reported as the negative it is: the strategy arm C hypothesised — *always arrive
at r180 beats averaging r170 with a long tail* — is not something this field has
tried, let alone measured. The nearest shipped thing is the *opposite* framing,
variance in the OUTCOME rather than in the TIMING, and that is already filed as
[`all-in-variance-is-a-ladder-tax`](all-in-variance-is-a-ladder-tax.md).

**The one thing he does commit to using the range for is not our question
either** — it is opponent modelling:

> *"Also record the timing and army size and composition of the enemy’s first
> attack, or maybe its first few attacks, or maybe all of its major attacks."*

## WHY IT MIGHT TRANSFER — against OUR ruleset specifically

The reasoning behind arm C is sound for our currency in a way it was not for
his. **The ladder pays game share, `delta = 32 × (S − E)` with `S = games won /
5`** — so a long tail of very late kills does not merely lose those games, it
loses the *margin* on the whole match, and `R1000_IS_DEFEAT` means the extreme
tail scores as a loss even when the tiebreak falls our way. **A distribution
with the same median and a shorter right tail is strictly better paid on our
ladder than on his AIIDE round-robin.**

**But the mechanism he proposes cannot be built here, and the reason is a rule,
not an engineering limit.** His design is a *"static data file to be read at
startup"* accumulated across games — cross-game memory. Our sandbox freezes
`time.*`/`datetime.now` to a constant and our comms store is per-match and
per-team; there is no persistence between matches at all. The library already
records this closure (*"Closed by construction, do not spend a leg"*, `CLAUDE.md`).
**So the DATA half of the proposal is closed for us; only the WITHIN-MATCH half
transfers**, i.e. a bot reasoning about the spread of its own remaining
timeline from what it can see this game.

**EFFECT ON MEDIAN KILL ROUND: EXPLICITLY NOT NEUTRAL, AND POSSIBLY LATER —
this file is flagged accordingly.** A variance-reducing change buys tail
shortening by giving up left tail too; the median can rise even where the mean
falls. Under `DEFENCE_ADMISSION_BAR: kill_round_non_regression` **that makes a
naive variance plank OFF-PROGRAMME on its face**, and the bar is not negotiable
just because the reasoning is elegant. Any variance plank here must be
constructed to cut only the RIGHT tail — which is a much narrower thing than
"reduce variance" and should be pre-registered as such.

## WHAT WOULD KILL IT

* **The cross-game persistence the proposal is built on does not exist for us.**
  That alone reduces this from a portable design to a framing.
* **`PROGRAMME.md`'s bar.** As above: median-kill-round non-regression forbids
  the general form.
* **Our own arrival distribution may not be the high-variance term.**
  `doctrine.py:1479` records that against Ouroboros *"we arrive in 5.8%"* of
  games — a distribution dominated by **non-arrival**, not by late arrival.
  You cannot shorten the tail of a distribution whose mass is at infinity;
  that is an arrival problem, and the fix is the one the tree already pursues.
* This is one author's undelivered design note. It is the weakest evidence class
  in this sweep and is filed to stop the next session hunting for a shipped
  version that does not exist.

## BUILDER HOOK — none yet

Deliberately none. The buildable descendant is **not** a variance plank; it is
the measurement that would tell us whether one is worth designing: **plot our
own kill-round distribution rather than its median**, from the existing replay
corpus, split by whether we arrived at all. If the spread among *games we won* is
narrow and the damage is all in non-arrival, arm C is closed for us on our own
data and this file is the record of why we looked. Zero bot code, zero risk,
and it uses `ladder_games.tsv` for the denominator per the standing corpus rule.
