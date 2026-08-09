---
tactic: The underdog's upset came from being general exactly where the stronger teams were tuned
source: https://battlecode.org/assets/files/postmortem-2023-dont-at-me.pdf
origin: Battlecode 2023 / don't @ me — 25th seed, upset the 8th seed in Sprint 1 and the 8th seed again in Sprint 2
evidence: documented
transfers: partial
---
WHAT IT IS — The most explicitly-framed "we were worse and beat someone above us" account in the
Battlecode corpus, with a stated mechanism rather than a shrug:

> *"a lot of teams had hardcoded values according to the three original game maps"* … *"some
> teams' robots did not function as intended and were subsequently upset by other teams"* …
> *"our more generalized code (especially in regard to exploring map symmetries) meant that our
> bot could compete and even beat upper level teams, despite our seemingly poor standing
> compared to them"*

They repeated it: *"we pulled an upset and managed to beat the 8th seed Bruteforcer out 3-2 in a
set of very small maps"*. And crucially, the effect appeared on the **ladder** too, with no code
change at all: *"These maps had more variance than the original three maps, allowing our bot to
climb rating without any adjustments."*

**The underdog did not out-play the stronger bots. It stayed correct in a region of the input
distribution where their tuning had never been exercised.**

WHY IT MIGHT TRANSFER — **This is the underdog's structural edge and it is the mirror image of
the top tier's advantage.** A stronger opponent is stronger partly *because* it is tuned, and
tuning is fitted to the distribution it was tuned on. The top of our league has been tuned
against each other and against the mid-field — **not against us specifically**, and by the same
token our own near-constant opening (CV 0.09) is a distribution they have seen little of. The
league-level version of the lever is: find the corner of the input space — map size, symmetry
class, ore density, seat — where our win rate against the 1900+ band is least bad, and ask what
about it is unusual. That is a search over *conditions*, not over tactics, and it costs no bot
change to run.

WHAT WOULD KILL IT — **Three things, and the third is the serious one.** (1) The mechanism was
organiser-supplied — new maps were introduced by the competition, not chosen by don't @ me; they
were beneficiaries, not authors. If our league's map pool is fixed and both sides have seen all
of it, the overfit region may simply not exist. (2) The same team, in the same document, reports
that this stopped working at the top — see
[`generality-saturates-and-then-stops-paying`](generality-saturates-and-then-stops-paying.md).
**By their own account, generality bought upsets against the 8th seed and nothing against the
finalists.** (3) Our own bot is the one with a documented unconditional opening and a width
gradient; on the evidence we currently hold, **we may be the overfitted party on the map axis,
not them.**

BUILDER HOOK — A corpus query, no bot edit: compute our win rate and `core_kill_share` against
the top rating band, **bucketed by map width, height, symmetry class and ore count**. If any
bucket is markedly better than our average against that band, that bucket is the candidate
region — and the next question is whether we can *steer toward* it (we cannot choose maps, but
we can choose behaviour conditional on the map we get). If no bucket separates, record it as a
measured negative and this file's lever is closed for us.
