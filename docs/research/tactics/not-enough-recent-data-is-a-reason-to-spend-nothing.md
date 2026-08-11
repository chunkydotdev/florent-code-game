---
tactic: refuse to prepare against an opponent when the pooled record is strong but the RECENT record is thin
source: http://satirist.org/ai/starcraft/blog/archives/1145-AIIDE-2021-what-Steamhammer-learned.html · http://satirist.org/ai/starcraft/blog/archives/520-Steamhammer-1.4.1-change-list.html
origin: Jay Scott, Steamhammer, AIIDE 2021 and Steamhammer 1.4.1
evidence: documented (he states the decision he made and shows the from-scratch tables); the counter-evidence noted below is anecdotal
transfers: yes
---
WHAT IT IS — The measured negative on static, pre-committed, pooled-statistic opponent
prep, stated by the author who declined to act on the pooled number. Verified verbatim
(`pflat/1145-AIIDE-2021-what-Steamhammer-learned.flat`):

> "When I was preparing opponent-specific data, Steamhammer had an overwhelming score
> against FreshMeat on BASIL. This result is good but not overwhelming; FreshMeat improved
> a lot in a short time. I had recognized that FreshMeat had made great strides, but there
> was not enough recent data to show what was working in the most recent games. So I made
> no preparation at all."

**The whole of sweep 22 is in that paragraph.** A pooled ladder score against a named rival
said *overwhelming*; the rival had improved recently; the pooled number could not be
decomposed into recent-versus-old; **so the correct action was to spend nothing.** Note the
precise wording of the constraint — *"not enough recent data"*, not *"not enough data"*.
The sample was large. It was large about the wrong thing.

The same author dropped hand-built opponent-specific prep from his own configuration
(`pflat/520-Steamhammer-1.4.1-change-list.flat`):

> "A few more opponent-specific strategies were dropped from the configuration, after
> experience showed that they were not needed any longer. My plan is to drop the remaining
> ones in the next version, 1.4.2, and rely solely on learning."

WHY IT MIGHT TRANSFER — this is a **decision rule we can adopt today at zero cost**, and it
is the correct response to our own measurement. We know that 72.6% of our archived games
against our top-15 opponents were played against versions they no longer run, that for five
of those opponents the figure on their current version is **0.0%**, and that a version
generation is worth **−8.00pp of game share**. The rule: **compute the recent/current-version
n before computing the win rate, and if that n is too small, the cell is not selectable —
regardless of how large and how favourable the pooled number is.** A big pooled number
against a rival who has shipped since is a reason for *caution*, not confidence.

It also sharpens what `tools/target_value.py` gates on. That tool asks whether a target is
worth beating; this adds whether the target is **knowable** — a reachable, high-paying cell
we cannot currently measure is not a good cell this hour.

WHAT WOULD KILL IT — **read as a general claim about opponent modelling it is wrong, and
the corpus says so.** Counter-evidence, reported for honesty: one author claims *"So far my
opponent-specific builds have saved 4 wins that otherwise would have been losses (according
to my testing)"* (`pflat/179-SSCAIT-2016-links.flat`) — **anecdotal**, self-reported, own
testing, no denominator. And the AIIDE 2021 write-directory census found that **every single
entrant wrote learning data**, so nobody in that field concluded opponent modelling was
worthless. **The negative is specifically against STATIC, PRE-COMMITTED prep built on a
POOLED STATISTIC — not against opponent adaptation as such.** Ours is a stateless league,
so the only opponent adaptation available to us is at the analysis layer anyway, which is
exactly where the negative bites.

BUILDER HOOK — a gate line, alongside the existing `TARGET BAND` line in every prereg:

`CELL FRESHNESS: opponent <id>, current version <v> (debuted <t>), games we hold on THAT version <n>, share of our archive on retired versions <x%> — selectable YES/NO`

If `n` is under the leg's own MDE, write NO and pick a different cell. `tools/corpus/version_drift.py`
prints the `%onCUR` column that answers this directly.
