---
tactic: block on (opponent id, opponent VERSION) — never on opponent id alone
source: tools/corpus/version_drift.py over corpus/league_matches.tsv (35,642 league matches, 2026-08-01T07:02Z..2026-08-11T05:52Z); design precedent https://cgi.cse.unsw.edu.au/~blair/pubs/1998PollackBlairML.pdf
origin: measured in-repo (research arm, sweep 22, 2026-08-11) + Pollack & Blair, Machine Learning 32, 1998
evidence: documented
transfers: yes
---
WHAT IT IS — Every per-opponent statistic we compute keys on the opponent's TEAM ID.
The league table keys on `(team, version)`, and those are not the same object. Measured
league-wide with **our own bot frozen inside each block** — block = `(team, that team's
own version, opponent)`, so the only thing moving is the opponent's version — a team
scores **8.00 percentage points less game share against the opponent's later versions
than against that same opponent's earlier ones** (1,970 blocks, 27,847 games,
−0.0800 ± 0.0051, **t = −15.81**). At K = 32 that is **2.6 rating points per match**,
and it is invisible to every cut we currently run.

The number survives three controls, one of which was built specifically to kill it:
* **coinflip split inside the block** (null by construction): +0.0022 / +0.0024 / −0.0014
  over three seeds, all |t| < 1.
* **opponent version debut order shuffled within opponent**: +0.0063 ± 0.0050, t = +1.25.
* **THE DISCRIMINATING ONE — blocks where the opponent's version NEVER CHANGED, split by
  median TIME**: −0.0023 ± 0.0038, **t = −0.61**, on a comparable population (1,867
  blocks, 18,981 games). This one matters because a block *ends* when the team ships, and
  teams ship after a bad run — so a pure time trend plus that censoring would have faked
  the entire effect. It does not: with the opponent's version held constant, later-in-block
  is not worse. **The effect is the opponent's version, not the clock.**

The dose-response says it is a **STEP, not a rate**: −6.19pp when the two halves are
under 3 hours apart, −6.96 at 3–8h, −7.72 at 8–16h, −9.79 at 16–36h, −11.80 beyond 36h.
Most of the loss is already present within hours. **Do not annualise it** — an earlier
draft of this file computed "−16pp per day" off the 11.9-hour median separation and that
extrapolation is not licensed by the curve.

WHY IT MIGHT TRANSFER — it is not a transfer, it is a measurement of this league, and it
is the direct explanation of the surprise that opened sweep 22: a cell statistic pooled
across 13 of one opponent's versions, 60% of it from a version they no longer run.
**The bias has a SIGN and we now know which way: pooling OVERSTATES our expected game
share against the version we will actually face.** Every per-opponent gate, panel cell,
target-band estimate and stop-loss in the repo currently reads high. Note the unblocked
version of the same cut gives only −2.74pp: when our own bot is also allowed to move,
our improvement partially masks theirs. **The 8pp is what a FROZEN bot loses — which is
exactly the state an incumbent holding the ladder slot is in.**

The classical design that fixes it exists and predates us by 28 years. Pollack & Blair
had the identical problem (is the mutant better than the champion, when the environment
is adversarial and noisy?) and their answer was to hold the opponent fixed across arms —
verified verbatim, `acad_pollack.flat`:
> "In this new setup the current champion and mutant both play a number of games against
> the same opponent (called the foil) with the same dice-streams, and the weights are
> adjusted only if the champion loses all of these games while the mutant wins all of
> them."

Three separable parts, and only two of them are available to us: (i) a **fixed
third-party foil** — we have this, it is the pinned panel; (ii) **common random
numbers** — we do NOT have this, we cannot seed the engine or choose the map, and it is
the single biggest variance-reduction tool in that paper; (iii) an **asymmetric strict
acceptance rule** — available and well matched to `MARGIN_IS_THE_CURRENCY`.

WHAT WOULD KILL IT — the block is only as good as its key, and **their version can move
between our arms**: median opponent version lifetime in this league is **1.17 hours**
(see `an-opponent-version-has-a-one-hour-half-life.md`), and the team that triggered this
sweep shipped four versions in 4.5 hours. A leg whose arms are separated by more than
about an hour has probably already broken its own block. It would also be killed if the
platform stopped serving per-match `teamAVersion`/`teamBVersion` — that field is the only
reason any of this is measurable, and nothing in our tooling currently reads it for the
OPPONENT (`ladder_games.tsv.oppver` is NULL for whole opponents; `league_matches.tsv` is
the surface that works).

BUILDER HOOK — the smallest version is free and changes no bot code:
1. In every prereg, state the block as `(opponent_team_id, opponent_version)` and record
   the opponent's version **per match on both sides**.
2. **Discard any arm-pair that straddles an opponent ship.** Unrated games are free
   (`WHAT LOKI IS` rule 5), so pay the matches rather than the confound.
3. Interleave arms tightly in time instead of running arm A then arm B — the block
   decays in about an hour.
4. Re-run `python3 tools/corpus/version_drift.py` before any cell-selection decision and
   read the `%onCUR` column: for the top-15 opponents by our archive volume, **72.6% of
   our archived games were played against a version that opponent no longer runs**, and
   for five of those opponents the figure is **0.0% on their current version**.
