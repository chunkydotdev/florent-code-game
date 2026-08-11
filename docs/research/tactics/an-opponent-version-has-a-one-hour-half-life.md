---
tactic: give every opponent-cell statistic a staleness term that inflates on their SHIP events
source: tools/corpus/version_drift.py over corpus/league_matches.tsv; http://www.glicko.net/glicko/glicko.pdf
origin: measured in-repo (research arm, sweep 22, 2026-08-11) + Glickman, the Glicko rating system
evidence: documented
transfers: yes
---
WHAT IT IS — The measured shelf life of any statement we make about a specific opponent.
Over 1,979 observed team-versions in this league (lifetime = a version's debut until that
team's next version debuts; right-censored versions dropped):

| percentile | lifetime |
|---|---|
| p10 | 0.17 h |
| p25 | 0.50 h |
| **p50** | **1.17 h** |
| p75 | 3.83 h |
| p90 | 11.33 h |

**50.0% of versions are replaced within one hour, 82.3% within six, 97.1% within a day.**
The median team runs 20 distinct versions and makes 23 version changes across a 10-day
window; only 4 of 72 active teams never changed version at all. Per-window hazard:
given an opponent plays ≥2 matches inside a 20-minute window, **6.52%** of the time their
version changes inside it; over an hour, **14.11%**.

Glicko has said the general form of the fix since 1995 — verified verbatim,
`acad_g_glicko.flat`:
> "One feature of the system is that game outcomes always decrease a player's RD, and
> that time passing without competing in rated games always increases a player's RD."

and, on the next sentences (referent = *growing uncertainty about the player's true
strength caused by elapsed time, not by any observed result*):
> "As time passes, we become more uncertain about the player's strength, so this is
> reflected in the RD increasing."

Glickman also documents the procedure for **calibrating** that inflation from an assumed
time-to-total-uncertainty — his worked example assumes "5 years (60 months) would need to
pass before the typical player's rating becomes as unreliable as an unrated player's
'rating.'" **We do not have to assume ours. We measured it: 1.17 hours.**

WHY IT MIGHT TRANSFER — because a stale cell and a fresh cell are currently
**byte-identical** in every table we print, which is the exact failure this repo already
booked against `ship_watch` (a healthy line and a blind line, indistinguishable, off rows
seven minutes old). The standing rule — *a monitor that reads a file must report that
file's freshness* — has never been applied to our per-opponent statistics, and they decay
about **forty times faster** than the elo tape that rule was written for.

WHAT WOULD KILL IT — **Glicko's decay model is the wrong shape and must not be ported
literally.** RD inflates smoothly because human skill diffuses; opponent-bot strength does
not diffuse, it **steps** at a ship event. A smooth time-decay would under-inflate at the
one instant that matters (the minute after they ship) and over-inflate through a long
quiet spell when a stale cell is in fact perfectly good. Key the staleness on **observed
version-change events read from `league_matches.tsv`**, and use elapsed time only as a
fallback prior for teams we have not observed recently.

Second qualification, and it cuts the headline number: the lifetime distribution **mixes
real ships with activate-fire-rollback test windows** — the same procedure we run. 63.9%
of active teams show the A→B→A excursion signature, so a large share of the sub-hour mass
is prototypes that were never the team's fielded bot. The p50 of 1.17 h is therefore the
half-life of *the version tag*, not necessarily of *the bot we will face*. For "what will
they field", the match-weighted modal version is the better estimator — and it varies
enormously by opponent (share of our archived games on their single most-played version
runs from **17.8%** for Powerpuff Girls to **96.9%** for Ouroboros).

BUILDER HOOK — smallest useful thing, no bot code:
1. Add two columns to every per-opponent table we print: **age of the newest observation**
   and **number of opponent ship events since it**. Refuse to print a verdict when the
   second is non-zero, the same way the freshness rule refuses past ~2 cadences.
2. Before a leg, check the target's version churn over the previous 24h. An opponent
   averaging a ship an hour cannot be measured by a leg that takes two hours to run —
   pick a stabler cell or accept that the leg measures a moving target and say so in the
   prereg.
