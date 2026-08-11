---
tactic: pin the comparison to the subset of opponents whose version is identical in both windows, and use their common drift as the instrument's own baseline
source: http://satirist.org/ai/starcraft/blog/archives/736-comparing-strength-across-time.html · http://satirist.org/ai/starcraft/blog/archives/1101-Steamhammers-performance-over-time.html
origin: Jay Scott, Jan 2019 (equating design) and July 2021 (inflation control)
evidence: documented for the 26-bot count and for the Elo-inflation observation; inference for the equating method (he proposes it; no post executes it)
transfers: yes
---
WHAT IT IS — Two halves of one idea: **the opponents who did not change are the only
instrument you have.**

**HALF ONE — equating across eras.** You cannot compare ratings from two windows of a
mutating field, so you find the subset that is provably identical in both, pin their
ratings, and re-solve everyone else against those pins. Verified verbatim
(`pflat/736-comparing-strength-across-time.flat`):

> "We need 2 tournaments, preferably round robin, that share some participants—exactly
> identical bots, the more the better."

> "If some participants which are not identical have the same names, distinguish them
> somehow—Steamhammer 2017 versus Steamhammer 2018, or whatever."

> "The identical players have identical strength in both tournaments, so consider their
> elo ratings as fixed. For each tournament separately, compute the elo ratings of the
> remaining players while keeping the ratings of the identical players fixed. The fixed
> ratings are benchmarks that keep the elo comparison stable for the remaining players
> (the idea has been used before)."

and, from his own comment on that post: "I have collected the list of bots which are
unchanged between SSCAIT editions 2017 and 2018: There are 26."

The middle quote is the exact statement our pipeline violates: **entities sharing a name
that are not identical must be given different identities before any pooling.**

**HALF TWO — the unchanged set as a drift baseline.** The same unchanged bots also measure
the *rating system's* own motion (`pflat/1101-Steamhammers-performance-over-time.flat`):

> "I looked at the long-term elo graphs for a number of bots which have not been updated
> the whole time, and they all show elo increases. BASIL has elo inflation, which explains
> some proportion of the elo rise of all bots. It also means that if your elo does not
> increase, maybe your bot is not staying the same, but getting worse! (We could take an
> average of non-updated bots and subtract out their elo inflation to get an estimate of
> true strength over time. There is no reason to expect that the inflation is constant
> over time.)"

*(Referent: "your elo" = the reader's own bot's BASIL rating; "getting worse" means
relative to a field that is itself moving, not an absolute regression.)* The named
mechanism is population turnover — "You can get elo inflation if bots arrive, lose games
and fall in elo to push everybody else up, then are dropped".

WHY IT MIGHT TRANSFER — **we can execute this better than he could.** Jay Scott had to
hand-assemble his list of 26 unchanged bots by inspection; we get
`teamAVersion`/`teamBVersion` free on every match in `corpus/league_matches.tsv`. The
concrete build: for any two windows we want to compare — before/after our own ship, or two
arms of a leg — compute the set of opponents whose version string is **identical in both**,
and use only those as the comparison basis. Everything else in the field is confounded
with its own shipping, which we now know costs **8.00pp of game share per version
generation** (`block-on-opponent-version-not-opponent-id.md`).

Half two flags a hazard we currently carry and do not correct: our ladder has ~150 teams
with free entry and exit, so the **same entry/exit inflation mechanism applies to us and
nothing in our pipeline subtracts it.** A standing unchanged-opponent panel gives us a
drift baseline for our own rating readings for free.

WHAT WOULD KILL IT — **an empty anchor set**, and this is a live risk rather than a
theoretical one. Measured on our league: median opponent version lifetime is **1.17 hours**,
50% of versions are replaced within an hour, and only 4 of 72 active teams never changed
version across ten days. Over any window long enough to be worth comparing, the set of
opponents holding still may be empty — in which case **the correct output is "this
comparison cannot be made", which is itself the finding** and is strictly better than the
pooled number we would otherwise print. A second limit: the equating method is Jay Scott's
*proposal*; across 1,234 of his posts no execution of it was found, so it carries no
empirical track record.

BUILDER HOOK — read-only, no bot code, and it composes with the instrument already
written. Extend `tools/corpus/version_drift.py` with an `anchor_set(window_a, window_b)`
helper returning the opponents whose version is unchanged across both, plus their pooled
game share in each window. Report **two numbers on every cross-window claim**: the raw
delta, and the delta restricted to the anchor set. Where they disagree, the anchor number
is the one to quote, and the disagreement is worth reporting on its own.
