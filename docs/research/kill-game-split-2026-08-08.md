# The kill game is a strength split, not a map or opponent property

**Research arm, session 20, 2026-08-08 22:3x CEST.**
**Version tag:** our live version **v84 "Eir 14"** (bots/_v99mag, md5 dab7766e),
baseline 1593.0 @ 429. Data window spans **our v72–v84** (13 versions).
**Sources:** API only — `fcode match list --mine --type ladder --limit 100` +
`fcode match info --json` per match. **100 matches / 500 games. ZERO replay
downloads.** Cache: scratchpad `mine.json`. No code was read for this doc.
**Prior work checked before running:** `docs/research/` (67 deliverables),
`tools/game_census.py`, `tools/ladder_census.py`, HANDOVER s19 map table.

This tests the one-minute prediction the builder left on the
`ladder-wide-census-THE-GAP` row at the s19 wrap:

> "hive (15% share) and drumlin (24%) should be the maps where we are killed
> FASTEST."

---

## 1. The prediction is half right, and the half that fails is the useful half

| map | n | win% | killed% | **median death turn** | rank by speed |
|---|---|---|---|---|---|
| **drumlin** | 36 | 28% | 53% | **212** | **1 of 15 (fastest)** |
| jackpot | 23 | 52% | 26% | 214 | 2 |
| saga | 42 | 52% | 31% | 229 | 3 |
| nordkap | 31 | 52% | 42% | 237 | 4 |
| lighthouse | 33 | 58% | 33% | 243 | 5 |
| **hive** | 34 | **15%** | **74%** | **246** | **6 of 15 (middle)** |
| snowflake | 36 | 39% | 50% | 252 | 7 |
| … | | | | | |
| antler | 29 | 59% | 24% | 511 | 15 (slowest) |

**drumlin: CONFIRMED.** Fastest death on the board, 212 turns.

**hive: REFUTED.** 246 turns is rank 6 of 15 — squarely mid-pack. hive is not
where we die fastest.

**What hive actually is: the map where we are killed most OFTEN.** 74% of hive
games end with our core destroyed. The next worst map is eider at 59%. That is
a 15-point gap to second place.

### Rate is the predictive variable; speed is nearly not

Across the 15 maps:

```
corr(kill-rate-against-us, our win%)   r = -0.84      <- explains map performance
corr(median death turn,    our win%)   r = +0.34      <- barely does
```

The prediction reached for the right maps through the wrong variable. Ranking
maps by *how often* we are killed puts hive and drumlin at #1 and #3; ranking
by *how fast* puts hive at #6. **Any instrument built to shorten our
time-to-death would be optimising the weaker of the two signals.**

## 2. The map effect is NOT an opponent-mix artefact

The obvious confound: hive and drumlin might simply be drawn more often against
Lunds/Ouroboros/KCM. They are not.

```
hive:    n=34   mean opponent rating 1598
drumlin: n=36   mean opponent rating 1596
ALL:     n=500  mean opponent rating 1595
```

And restricting to opponents rated ≥1550 (n=350) leaves the ordering intact:

| map (strong opponents only) | n | win% | killed% |
|---|---|---|---|
| **hive** | 24 | **12%** | **75%** |
| eider | 21 | 29% | 71% |
| snowflake | 28 | 25% | 61% |
| drumlin | 27 | 22% | 56% |
| … | | | |
| meander | 24 | 71% | 21% |

**hive at 12% win / 75% killed against strong opposition is the single worst
cell on the board, and it is a map, not an opponent.**

## 3. The finding that reorders the reordering

Splitting all 500 games by opponent rating separates two populations that the
project has been averaging together:

| opponent band | n | our win% | r1000 share | win% *in* r1000 | **win% in the kill game** |
|---|---|---|---|---|---|
| 1650–1749 | 70 | 36% | 13% | 67% (n=9) | **31%** |
| 1550–1649 | 280 | 40% | 36% | 50% (n=101) | **34%** |
| <1550 | 150 | **71%** | 23% | 80% (n=35) | **69%** |

```
STRONG (opp >= 1550):  n=350   win 38.9%
WEAK   (opp <  1550):  n=150   win 71.3%
```

**Our entire 48.6% is carried by the sub-1550 band.** Against anyone at or above
1550 we win 38.9%, and inside the core-kill population we win **~33%** — flat
across both strong bands.

### This corrects two claims on the s19 wrap block

**(a) "Our 44% core-kill rate is the ceiling metric."** The 44% is real
(158 kill-wins / 354 kill-decided games = 44.6%) but it is a *mixture* that
hides its own shape. It is 69% against weak teams and 33% against everyone
else. There is no single 44% to optimise — there are two regimes, and only one
of them is losing us matches.

**(b) "Our tiebreak edge is in a game the strong field never enters."**
Directionally supported, materially overstated. r1000 share is 13% against the
1650–1749 band — but **36% against the 1550–1649 band, where 280 of our 500
games are played**, and we go exactly 50/50 there. Overall the grind game is
29% of our games and **net +24 for us (85 W / 61 L, 58.2%)**. It is not a dead
game the field refuses to enter; it is the only population where we are above
water. The correct statement is narrower: *the top band resolves before the
grind, so the tiebreak edge cannot be spent against them.*

Global condition split, for the record:

```
OUR WINS   (243)   core_destroyed 158 (65.0%, median 182 turns)
                   titanium       85 (35.0%, median 1000)
OUR LOSSES (257)   core_destroyed 196 (76.3%, median 300 turns)
                   titanium       61 (23.7%, median 1000)
```

## 4. Where the kill-game losses actually sit

All 196 games we lost by core destruction, attributed:

| opponent | kill-losses | share | cumulative |
|---|---|---|---|
| Lunds Stallions | 30 | 15.3% | 15.3% |
| Kings College Munich | 26 | 13.3% | 28.6% |
| Ouroboros | 20 | 10.2% | 38.8% |
| CtrlAltDefeat | 20 | 10.2% | **49.0%** |
| 0033 | 13 | 6.6% | 55.6% |
| Focalground | 11 | 5.6% | 61.2% |
| Powerpuff Girls | 10 | 5.1% | 66.3% |

Per-opponent kill-game records (wins/kill-decided games):

```
Ouroboros              2/22   ( 9%)      Askar City       20/25  (80%)
Kings College Munich   7/33   (21%)      Banminary        18/24  (75%)
Lunds Stallions       11/41   (27%)      Team 48          19/29  (66%)
0033                   5/18   (28%)      Memtrace         17/25  (68%)
CtrlAltDefeat          9/29   (31%)
```

### A correction to my own boot ping

At 22:23 I pinged that THE GAP might make the per-opponent instrument programme
"the wrong SHAPE entirely." **My own data refutes that and I am withdrawing it.**
The same four names carry 49.0% of kill-game losses that carry ~61% of gross
Elo bleed. THE GAP and the per-opponent programme are one finding at two
altitudes, not competitors.

What THE GAP legitimately changes is not the *target* but the *outcome
variable*: instruments aimed at these four should be scored on **kill-game win
rate**, not Elo. Elo mixes in the grind games we already win and needs ~8
matches to say anything; kill-game rate is available per game, is where 100% of
the deficit sits, and against Ouroboros (2/22) has room to move that Elo cannot
resolve.

## 5. What I did not measure, stated so it is not silently assumed

- **No causal mechanism.** This is 500 games of outcome metadata. *Why* hive
  kills us at 75% is not in this data — it needs replays (builds, turret
  placement, damage), which this doc spent zero downloads on.
- **v72–v84 pooled.** 13 of our versions are averaged together. A per-version
  read of the hive cell is possible from the same cache and was not run.
- **Seat is not in this cut.** The cache carries it; the KCM decode found a
  real seat split, and hive/drumlin were not tested for one here.
- **The 1650–1749 r1000 cell is n=9.** The 67% in it means very little; the 13%
  share it sits inside (n=70) is the load-bearing number.
- **Archive floor does not apply** — this is API metadata, not replays, so the
  ~08-07-midday archive floor (workflow-analysis series rule 5) does not
  truncate it. The v72 floor here is the 100-match `match list` cap instead.

---

# ADDENDUM (22:5x CEST) — the per-version and per-seat cuts, run

Same cache, same 500 games, still zero replay downloads. Run because the
builder is live-testing whether the v75→v80 survival machinery (heal_seats,
`_ring_*`, `SIEGE_HEAL_RESERVE_TI`, `HIVE_FREEZE`, `POP_FLOOR`) suppressed our
core-kill rate.

## A. hive is NOT a seat effect — that caveat closes

```
hive        seatA n=20 win 15% killed 70%    seatB n=14 win 14% killed 79%
eider       seatA n=17 win 41% killed 59%    seatB n=10 win 40% killed 60%
drumlin     seatA n=17 win 24% killed 59%    seatB n=19 win 32% killed 47%
snowflake   seatA n=26 win 35% killed 50%    seatB n=10 win 50% killed 50%
```

hive is flat across seats to within 1pp on win rate. The KCM seat split is real
in its own scope; it does not reach the map cells. **hive is a pure map
property.**

## B. hive looks like it got worse — and that read does not survive

```
v72-77:  n=18   win 22%   killed 67%
v78-81:  n=15   win  7%   killed 87%      <- v80 alone: 1/12 win, 10/12 killed
```

Tempting, and it points straight at the survival-machinery era. **Do not spend
it**: n=15 and n=18, and section C shows the same-shaped trend at the global
level dissolving completely under an opponent-mix control.

## C. The apparent decline in our kill-game rate is an OPPONENT-MIX ARTEFACT

Kill-decided games against opponents ≥1550 (n=239), by our version era:

```
v72-76:  51/136 = 37.5%      mean opp rating 1642
v77-81:  18/74  = 24.3%      mean opp rating 1644
v82-84:  10/29  = 34.5%      mean opp rating 1629
EARLY v72-76 37.5%  vs  LATE v77-84 27.2%    Fisher exact two-sided p = 0.098
```

Not significant, and mean opponent rating is flat — so it is not "we started
facing harder teams." **Holding the opponent set fixed to the four bleed
carriers (Lunds / KCM / Ouroboros / CtrlAltDefeat) removes it entirely:**

```
EARLY v72-76:  16/67 = 23.9%
LATE  v77-84:  13/58 = 22.4%
difference:    -1.5 pp     bootstrap 95% CI [-16.1, +13.4] pp
```

Flat. The whole era swing traces to one opponent leaving the pool:

```
v72-76 kill games:  Banminary 14/19 (74%)   <- present
v77-84 kill games:  Banminary absent, replaced by Focalground 1/12, Ouroboros 0/11
```

### What this says about the live hypothesis

**In production, the v75→v80 survival machinery did not suppress our core-kill
rate against the opponents that matter.** Against a fixed opponent set the rate
is 24% before and 22% after.

Stated honestly, because the CI is wide: an effect **larger than ~16pp in
either direction is excluded**; a small one is not. But the direction of the
burden has moved. The ~24% kill-game rate against these four is not something
the survival era introduced — **it is the number we have had for the entire
v72–v84 window, and it is older than the floor of this data.** Removing the
survival machinery is therefore unlikely to recover it.

This does not touch the *local* leg's validity as a mechanism test — it says
what the leg's result will mean if it lands non-null: a mechanism that fires
locally against a ~3-effective-opponent det pool while production shows no
corresponding movement across 125 kill games against the real carriers.

## D. Per-version kill-game rate vs strong opposition, for the record

```
v72  9/19   v73  8/18   v74 10/32   v75 14/43   v76 10/24
v77  8/12   v79  4/20   v80  5/32   v83  5/10   v84  4/16
```
Per-version n is too small to read individually; pooled into eras it is section
C, and section C says flat.

---

# ADDENDUM 2 (23:0x CEST) — I over-read my own map table. Only hive survives.

Run before accepting a 25-download budget aimed at map cells. It changes what
that budget should be spent on.

## The between-map spread is real, but it is ONE map

Null: a single global killed-rate (196/500 = 39.2%) with binomial noise per map.

```
chi-square heterogeneity = 40.2 on 14 df
permutation p (20,000 draws under one global rate) = 0.00030
```

So the maps genuinely differ — the s19 "59-point spread on a near-uniform draw"
is not an illusion. But per-map exact binomial tests, Bonferroni-corrected over
the 15 maps we actually looked at:

```
hive         25/34 = 74%   p=0.0001   p*15 = 0.002   *** SURVIVES
meander       7/36 = 19%   p=0.0193   p*15 = 0.290
eider        16/27 = 59%   p=0.0554   p*15 = 0.830
antler        7/29 = 24%   p=0.1351   p*15 = 1.000
drumlin      19/36 = 53%   p=0.1369   p*15 = 1.000
snowflake    18/36 = 50%   p=0.2486   p*15 = 1.000
...all remaining maps p*15 = 1.000
```

**hive is the only map distinguishable from the global rate once you correct
for having looked at fifteen.** The entire heterogeneity signal is hive.

### What this retracts, in my own doc above

Section 2 presented a tier of bad maps — hive 75%, eider 71%, snowflake 61%,
drumlin 56% against strong opposition. **That tier is not supported.** eider,
snowflake and drumlin are consistent with the global rate. Read section 2 as
"hive, and then fourteen maps," not as a ranking.

Section 1's drumlin result is weaker still. "drumlin is the fastest death at
212 turns" is a rank-1-of-15 claim with no correction applied, and drumlin's
kill *rate* does not survive correction either. **I am withdrawing "drumlin
CONFIRMED."** The honest statement: the builder's prediction named two maps —
one (hive) is the single real cell on the board and was named for the wrong
reason (speed, where it ranks 6th), and the other (drumlin) does not separate
from noise on either variable.

This also disposes of the s19 HANDOVER line "drumlin has never been examined by
anyone." Correct, and there is no measured reason to start.

## The same correction applies to the fork-split table

Splitting each map at the v86 fork point (v72–76 vs v77–84), strong opponents
only, produced per-map deltas from −31% (atoll) to +44% (jackpot) around a
pooled delta of **−3%** (early 47% killed, n=180; late 44%, n=170). At n≈10–20
per cell that is a noise fan, and the apparent improvement on
eider/drumlin/snowflake does not survive:

```
three maps, fixed four carriers: killed 83% (n=24) -> 59% (n=17)
bootstrap 95% CI on the change: [-52%, +3%]   does NOT exclude zero
```

**So I have no evidence that the v77–v84 era helped or hurt any map**, and I am
not offering the builder one for the slot decision. hive is the internal control
that makes this readable: 75% killed before the fork, 75% after, mean opponent
rating 1629 vs 1635 — dead flat while everything around it wobbles.

## What DOES survive, and it answers the gating question

Hive, split at the v86 fork point (v86 = a 128-line diff from `opp_v76`):

```
v72-76  (the lineage v86 DESCENDS FROM):  n=16   win 12%   KILLED 75%
v77-84  (what v86 REVERTED):              n=18   win 17%   KILLED 72%
  strong opponents only:  v72-76  9/12 = 75%     v77-84  9/12 = 75%
```

**The hive defect predates v77. It did not leave the ladder with x3r0's revert —
it is live in v86 right now.** That is the one map-scoped claim in this document
that survives correction, and it is what the download budget should be spent on.
All 25 on hive; nothing on drumlin.

## Process note against myself

Addendum 1 and section 2 both ranked fifteen cells and read the top of the
ranking as a finding. That is the multiple-comparisons trap, and I walked into
it twice in one document before testing for it. The test cost one query. The
s19 delta "a claim's SCOPE is part of the claim" has a sibling: **a claim's
SEARCH SPACE is part of the claim** — "worst of 15" is not a measurement until
it is corrected for the 15.
