---
tactic: measure the rank/rating drift of an UNCHANGED artifact and use it as the null distribution
source: https://forum.codingame.com/t/975 · https://www.codingame.com/forum/t/leaderboard-ranking-algorithm-issues/2764
origin: CodinGame — Agade (2015, Back to the Code) and sethorizer (2017)
evidence: documented, self-reported, with denominators in the second case
transfers: yes
---
WHAT IT IS — Two documented measurements of the same thing: **how much a completely
unchanged bot moves when the field moves around it.**

Rank drift with nothing changed (`lad_cg_backtocode.flat`, Agade):
> "For what it's worth I'd like to mention that the end rankings still felt quite random. I
> have already risen 23 spots from my final ranking of 91 without doing anything, no
> resubmit, no changes. I ended up about 30 spots away from people whom I'd been crushing
> all contest."

*(Referent: the 23-place gain is entirely the field's motion plus continued matchmaking
against a fixed artifact of his — he states "no resubmit, no changes".)*

And the same code judged by two populations, **with denominators**
(`lad_cg_lbissues.flat`, sethorizer):
> "Since I didn't modify my contest code yet at all, I did a little investigation: Of the
> 312 entries ranking above me during the contest, 223 submitted their code in the
> multiplayer challenge, and 39 or 17.49% of those actually rank below me in multiplayer (at
> the time of writing). I find this very surprising, especially considering, that many people
> probably improved their multi code by now (hiding the fact, that the discrepancy might be
> bigger)."

**One unchanged bot, two populations, 17.49% of pairwise orderings reversed** — and the
author flags that the other side changed in the interval, which biases his estimate
*downward*.

WHY IT MIGHT TRANSFER — **this is the null distribution we do not have and can get for
free.** Our repo already records a same-bot 12pp swing between consecutive 25-game windows
on a pinned panel; these are the *ladder-rating* analogue, and they say the frozen-artifact
drift band is not small in a league of a few hundred. Two direct uses:

* **A standing control, not an anecdote.** Hold the incumbent across a window with no
  changes and log its rating: that band is the floor beneath which no plank's measured
  effect is interpretable. We do this by default whenever we are not shipping, so the data
  already exists in `elo_history.tsv` and per-match `ourver` — it has simply never been read
  as a control.
* **A denominator for "is our bot getting worse?"** Our own measurement says a frozen bot
  loses **8.00pp of game share per opponent version generation**
  (`block-on-opponent-version-not-opponent-id.md`), which is the mechanism behind Agade's and
  sethorizer's observations. The two literatures agree: **a rating series is a joint
  function of artifact and environment, and a large excursion with no code change is fully
  explicable.** Directly relevant to how the "−57 drawdown" in our notes should be read: a
  drawdown is not evidence about the bot until the environment is ruled out.

The Battlecode version of the same lesson is blunter (`lad_bc_pm2021.flat`, Isaac Liao):
> "My refusal to modify my Sprint 1 code during my development of my new code led to me
> losing every game as a result of the rule change, and my team plummetted far down the
> scrimmage rankings to nearly the 150th rank"

— a rule change, not a field change, but the same structure: the artifact stood still and
the number moved a long way.

WHAT WOULD KILL IT — the CodinGame numbers are **self-reported, n = 1 competitor each**, from
a different league with a different rating system (TrueSkill-style, submission-triggered
batches) and a contest structure where a whole field resubmits at once. **Do not import the
17.49% as our number** — import the *method*. Ours is computable properly: ~150 teams,
per-match versions, 35k matches. The right move is to measure our own discordance rather
than quote theirs, and the instrument to do it already exists.

BUILDER HOOK — two read-only cuts, no matches played:
1. **Frozen-artifact drift band.** For each of our own versions that held the slot for a
   meaningful window with no changes, plot rating over that window. The spread is the null
   band; quote it beside every future ship claim.
2. **Discordance.** Take two windows, compute the pairwise ordering of teams in each, and
   report the fraction of pairs that flip. Restrict to the anchor set of opponents whose
   version is unchanged across both (`anchor-on-opponents-who-did-not-change.md`) and report
   both numbers — the gap between them is the share of apparent movement that is version
   churn rather than strength.
