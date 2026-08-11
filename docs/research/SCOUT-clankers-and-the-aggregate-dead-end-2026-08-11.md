# SCOUTING CLANKERS (2040) — AND THE END OF THE AGGREGATE HUNT

**Research arm, s30, 2026-08-11, on Magnus's go-ahead. Clankers: 467 archived
games already on disk, rating 2040, +351 on us. Comparison population: 72 teams
with ≥40 games; our 4,983 games. Sources: `corpus/events.tsv` (2.8M rows),
`corpus/econ.tsv`, `replay_archive/*.meta.json`. No new decoder — the corpus
already carried all of it.**

**BOTTOM LINE: Clankers' distinctive habits DO NOT GENERALISE, and nine aggregate
axes are now flat inside our own rating band. There is no build-mix, economy or
tempo statistic that separates a 1690 team from a 1780 team. That is the finding.**

## 1. WHAT CLANKERS ACTUALLY DOES (within-game controls, their opponents in the same games)

| per game | **Clankers** | their opponents | **us** | our opponents |
|---|---:|---:|---:|---:|
| harvesters | 4.9 | 5.5 | 6.4 | 5.1 |
| conveyors | 44.6 | 32.0 | 40.5 | 26.3 |
| **barriers** | **8.7** | 3.7 | **3.8** | 2.2 |
| gunners | 1.3 | 6.0 | 1.3 | 6.1 |
| sentinels | 2.2 | 0.9 | 3.3 | 1.7 |
| launchers | 0.1 | 0.3 | **1.0** | 0.6 |
| **total turrets** | **3.6** | 7.2 | **5.6** | 8.4 |
| **forward turret share** | **63%** | 72% | **44%** | 50% |
| **median first turret** | **r39** | r17 | **r7** | r10 |

**They win with half our turrets, built five times later.** The eye-catching one:
Clankers' first turret lands **22 rounds after its opponent's**; ours lands **3
rounds before**. A 25-round doctrine gap.

## 2. ⛔ IT IS AN IDIOSYNCRASY. IT DOES NOT GENERALISE.

Median first-turret round: **Clankers r39 · top-9 (≥1900) r18 · our band r14.**
Across 71 teams, **r(rating, first-turret round) = −0.293** — if anything the
strong build *earlier*, and the late-turret tail is weak teams that barely build.

**Clankers is one 2040 team with an unusual opening, not the top-tier recipe.**
Copying it would be copying an anecdote.

## 3. TWO THINGS LOOKED STRONG LEAGUE-WIDE — AND BOTH DIED IN THE WITHIN-BAND CUT

| | across 72 teams | **within 1550–1800 (n=23)** |
|---|---:|---:|
| forward turret share | **+0.539** | **+0.090** |
| barriers per game | **+0.555** | **+0.072** |

**They separate FUNCTIONAL teams from BROKEN ones, not good from great.** The
bottom of the league builds zero barriers and no forward turrets because it is
barely playing. *(Guard run: this is not a game-length artefact — the longest
games in the league are the weak teams' r1000 grinds, and those teams build the
FEWEST barriers, so the sign would have inverted.)*

## 4. NINE AXES, ALL FLAT INSIDE OUR BAND

ammo converted · conversion timing · turret count · shots fired · decisiveness
(r1000) · first-turret round · forward turret share · barriers · TLE induction.
Plus implied cost scale, the only within-band signal at all (**−0.348, n=23,
underpowered**) — and **we are already on the good side of it: 466% against a band
mean of 497%.**

**TLE induction, blocked on the victim so their own fragility is held constant:
nothing significant — every point estimate has an SE at or above its own size, and
`r(rating, induction) = −0.067`. ⚠ AND THE ESTIMATOR FAILED ITS OWN SANITY CHECK
— a within-victim contrast must average ~0 by construction and came out +3.56, so
no number from it should be quoted at all.** Recorded as an instrument fault, not
a result.

## 5. THE ONE REAL THING THIS FOUND, AND IT IS ABOUT US

**We are an outlier LOW on forward turret share inside our own band: 43.7% against
a band mean of 58% and a top-tier mean of 63%. Rank 44 of 72.** Only 58% of our
games contain a single barrier, against 80% for the ≥1900 group.

**This is a discrepancy, NOT a demonstrated lever** — §3 shows forward share does
not predict rating among teams of our strength. It is worth knowing that we sit at
the bottom of our band on a `NEVER PLAY DEFENCE` axis; it is not evidence that
raising it pays.

## 6. WHAT THIS REDIRECTS

**The aggregate hunt is exhausted and should stop.** Ten axes, league-wide,
third-party, with within-band controls and confound guards. Nothing countable per
game separates us from the teams just above us.

**That is consistent with the programme's own position and is now evidence for it:
the lever is a TRICK, not a STAT.** An aggregate cannot see a trick by
construction — a kidnap that permanently deletes one enemy unit per game moves no
build-mix mean, and `crash_census` already measures **2,451 unexplained unit
removals by opponents against 0 by us.**

⇒ **Next: the ejection machinery, turned around.** We are the field's heaviest user
of enemy-bot ejection — **3,727 hostile throws to their 1,927** — and the median
ejected bot sits **d² 265 from its own core**, i.e. deep in OUR half. Only **1.8%**
land inside their core's heal ring; only **194 of 12,157** forward turret builds
are launchers. **The capability exists, the class is approved and engine-verified,
and it is aimed at the wrong end of the map.** That is a build-and-fire question
for the builder, not another cut.

## 7. WHAT THIS IS NOT

10 days, one league, one window; ratings are final-window values with every team
starting at 1500, so all correlations are STRENGTH associations. Within-band n is
23 teams — **a real effect smaller than roughly r=0.4 would not be visible there**,
so "flat inside the band" means *not detectable at this power*, not *zero*. Under
`FIXTURE_OF_RECORD: live_unrated` this prioritises and closes nothing.
