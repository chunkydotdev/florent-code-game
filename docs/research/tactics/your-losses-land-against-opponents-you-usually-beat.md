---
tactic: A strong bot's losses are concentrated against WEAKER opponents, structurally — so variance reduction pays where the wins already are, not where the hard matchups are
source: http://satirist.org/ai/starcraft/blog/archives/456-luck.html
origin: RTS theory / Jay Scott, "luck", 2018 (AIIDE / SSCAIT crosstable analysis)
evidence: documented
transfers: yes
---

## WHAT IT IS — arm C, and it is the structural argument the variance question actually needed

Jay Scott, analysing Steamhammer's tournament results, states the result and
then the mechanism:

> *"The majority of Steamhammer's losses so far are "unlucky" losses against
> opponents that Steamhammer usually defeats. That is exactly what we should
> expect."*

> *"The bots in the highest places (Steamhammer is currently #6 out of 78) don’t
> have many opportunities to lose to stronger opponents. Look at the crosstable
> and you’ll see that all the top bots have the majority of their losses on the
> right-hand side, against weaker opponents."*

**Referent check.** "the right-hand side" is the crosstable's ordering by rank —
opponents ranked *below* the bot in question. The claim is about the *location*
of a strong bot's losses in the field, and it is presented as an observation over
all top bots, not just his own.

The mechanism is a counting argument, not a claim about play quality: a bot near
the top plays few games against anyone stronger, so almost all of its loss
opportunities are against weaker opponents. He adds the honest caveat that this
does not license writing those losses off:

> *"It’s difficult to judge by intuition whether a bot is getting lucky or
> unlucky."*

and locates the actual cause in his own bot's variance rather than in noise:

> *"In its losses, Steamhammer happens to randomly choose openings that don’t
> work against this opponent, or gets into less common situations where
> weaknesses pop up."*

The summarising line is the one to keep:

> *"Frequent unlikely chances outweigh scarce likely chances."*

## WHY IT MIGHT TRANSFER — against OUR ruleset specifically

**This is a direct instrument correction for how we choose targets and read
results, and it points the opposite way to our instinct.**

`CLAUDE.md` already carries the target-value gate — run `tools/target_value.py`
before a prereg, because a perfect result against a team 550-860 points below us
**PAYS UNDER 5 RATING POINTS** (`CLAUDE.md`, verbatim: *"A PERFECT RESULT PAYS UNDER 5 RATING POINTS (1.18)"*). **This file does not contradict that: a WIN down
there is worth nothing.** What it says is that **the LOSSES down there are where
our rating is actually leaking**, because that is where nearly all our loss
opportunities live. Those two facts are consistent and together they are sharper
than either: *against weaker opponents, upside is negligible and downside is
where the whole distribution sits.* The asymmetry is the argument for buying
consistency specifically in the matchups we already win.

**And the ladder's arithmetic amplifies it exactly here.** `delta = 32 × (S − E)`
with `S = games won / 5`: when `E` is high (a weaker opponent), every game
dropped is expensive and no result is cheap. A 3-2 against a much weaker team
can *lose* rating — the repo has measured deltas whose sign opposes the match
result in 20 of 678 matches. **Dropping one game in five to a team we beat is
priced like a defeat.**

Our own numbers say the loss opportunities are there in bulk: our core dies in
**46.3% of all games**, and our median death (r187) trails our median kill (r174)
by thirteen rounds — a margin thin enough that ordinary variance decides it.
**A thirteen-round margin lost half the time is exactly the signature of
"unlucky losses against opponents we usually beat."**

**EFFECT ON MEDIAN KILL ROUND: none directly — this is an analysis and targeting
discipline, not a plank.** Its consequence for planks is that a change which
tightens the r150-250 window *without* moving the median is worth more than the
median-only reading suggests, because it converts the dropped games in matchups
we already win. That is precisely the shape `PLAY_DEFENCE:
not_at_the_kill_s_expense` was amended to admit.

## WHAT WOULD KILL IT

* **Our position in the field is not Steamhammer's.** He was #6 of 78; we sit at
  ~1600 with the top running 2102/2040/2000/1977/1966 — i.e. **we are rich
  downward and empty upward** (sweep 16's framing). The counting argument gets
  *stronger* the higher you are, so it applies to us but with a larger fraction
  of genuine losses to stronger teams mixed in. **The claim is directional for
  us, not quantitative.**
* **It is an observation about a round-robin crosstable, not a ladder.** Our
  pairings are not uniform over the field, so the "few opportunities to lose
  upward" premise has to be checked against our actual pairing distribution
  rather than assumed.
* **The library's own standing trap applies:** this is a claim about a
  population, and it must be read on `ladder_games.tsv` (rated only) and never
  on `meta_join`, which silently pools our unrated prototype legs into the same
  denominator.

## BUILDER HOOK — none yet; the descendant is a corpus cut, not bot code

Split our rated ladder record by opponent rating band and locate our **losses**:
what share of games lost came against opponents rated *below* us, and how does
that share compare to the share of games *played* against them? If losses are
over-represented below us relative to exposure, the leak is where this file says
it is, and the next plank should be chosen for **tail-shortening in the games we
already win** rather than for a new weapon against teams above us. Zero bot code.

Pin the opponent's version at analysis time (`league_matches.tsv` for their
timeline — `ladder_games.tsv.oppver` is NULL and a null column reads as "no
version change" to any cut that trusts it), and use `ladder_games.tsv` for the
denominator.
