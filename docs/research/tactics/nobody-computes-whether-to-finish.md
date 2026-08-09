---
tactic: NEGATIVE RESULT — no Battlecode postmortem in eight seasons contains an expected-value or threshold rule for "try to finish vs. bank the tiebreak"
source: https://battlecode.org/past
origin: Battlecode 2019-2026, all 22 official postmortem PDFs, machine-searched
evidence: documented
transfers: partial
---
WHAT IT IS — Question (C) of sweep 17A asked how anyone decided whether to try to
finish at all versus bank the tiebreak, and whether an explicit expected-value or
threshold rule was ever written down. The brief said a clean negative would be a
valuable result. **It is a clean negative, and it is machine-countable.**

All 22 official Battlecode postmortems 2019-2026 were downloaded, converted with
`pdftotext`, whitespace-flattened (including form feeds), and grepped for a
battery of decision-theoretic vocabulary. Counts are files-with-a-hit out of 22:

| string | files | total hits |
| --- | --- | --- |
| `expected value` | 0 | 0 |
| `expected win` | 0 | 0 |
| `win probability` | 0 | 0 |
| `probability of winning` | 0 | 0 |
| `cost-benefit` / `cost benefit` | 0 | 0 |
| `worth attacking` | 0 | 0 |
| `abort` | 0 | 0 |
| `call off` | 0 | 0 |
| `retreat if` | 0 | 0 |
| `give up on` | 0 | 0 |
| `play for the tiebreak` / `play for a tie` | 0 | 0 |
| `bank the` | 0 | 0 |
| `secure the win` | 0 | 0 |
| `if we are winning` / `if we are losing` | 0 | 0 |
| `when ahead` / `when behind` | 0 | 0 |
| `losing position` | 0 | 0 |
| `convert the lead` | 0 | 0 |
| `close the game` | 0 | 0 |
| `settle for` | 1 | 1 |
| `winning position` | 2 | 2 |
| `utility` | 3 | 6 |

The three non-zero rows were read in context and **none of them is a decision
rule.** `settle for` is SPAARK describing a tiling fallback for special resource
patterns. `utility` is three teams naming *utility classes* and one naming a
*utility unit*. Of the two `winning position` hits, one is wololo's textbook
definition of the word "rush", and the other is cout for clout captioning a
figure in which the **opponent** had the winning position.

**The question is not answered badly in this field. It is not asked.** This is
the same shape as sweep 15's finding that no postmortem anywhere separates cause
from marker — the field's authors describe *what they built*, essentially never
*how they decided whether to*.

WHY IT MATTERS HERE — Two consequences, and the second is the one that should
change behaviour.

**First, it bounds the library.** There is no external precedent to copy for a
commit/abort gate. Any threshold we ship is our own arithmetic, and must be
labelled that way — as
[`the-defenders-reserve-and-what-defeats-it`](the-defenders-reserve-and-what-defeats-it.md)
already does for its sentinel count.

**Second, and this is the sharper reading: the absence is itself informative
about the shape of the decision.** What the field *does* contain, in place of a
threshold, is a small number of **structural** answers — a standing allocation
run unconditionally
([`a-standing-allocation-to-the-win-condition`](a-standing-allocation-to-the-win-condition.md)),
a fallback fired on the *failure* of a push rather than on a forecast of it
([`if-the-push-fails-fall-back-to-the-clock`](if-the-push-fails-fall-back-to-the-clock.md)),
and phase gates on clearance rather than on advantage. Nobody computed whether to
commit because **nobody framed it as a forecast**. They framed it as an
allocation and a fallback. Given that our own opening is a near-constant (CV 0.09)
and our paired differentials are opponent thermometers, an allocation-and-fallback
structure is also far cheaper for us to test than a forecast would be.

WHAT WOULD KILL IT — The negative is scoped to **Battlecode postmortems**, which
is a genre that reports design, not deliberation. It does not establish that no
*bot* ever contained such a gate — only that no author wrote one down. A single
open-source Battlecode bot with an explicit EV branch would narrow this to "the
postmortems don't discuss it", which is a weaker and much less interesting claim.
Nobody has grepped the bots; that is the obvious next probe and it has not been
done.

**Scope matters hard in the other direction, and the same sweep found the
positives.** This file's negative is about **Battlecode postmortems only.** Sweep
17A's other legs found explicit numeric rules elsewhere, all verified verbatim:

- **A contest winner commits on a bare turn number** — Code Royale's robostac
  dumps his whole economy for the last 40 of 200 turns, unconditionally on standing
  ([`commit-on-a-deadline-not-on-a-standing`](commit-on-a-deadline-not-on-a-standing.md)).
- **PurpleWave compares a normalised force differential to a moving threshold**,
  lowered once already engaged
  ([`the-commit-threshold-moves-once-you-are-engaged`](the-commit-threshold-moves-once-you-are-engaged.md)).
- **UAlbertaBot and CommandCenter have gates too** — the sign of a simulated
  outcome, and an absolute own-unit count.

So the correct statement is narrower and more useful than "nobody has a rule":
**bot source code has commit gates; postmortem prose does not discuss the
commit/abort trade-off.** And the one thing still not found anywhere, in any league
or any codebase read by any leg of this sweep, is a rule in the *other* direction —
**an explicit "stop attacking and play for the tiebreak score" gate.** Every
positive above decides whether to *start* or *continue* a fight. Nothing decides
whether to *stop trying to win by killing*. That residual negative is the one that
bears on us, because our tiebreak is the road we currently win.

BUILDER HOOK — none yet. This is a bound on the library, not a plank. If a
commit gate is ever built, this file is the reason it must ship labelled as
**our own inference from our own measured rates**, with no external citation
implied.
