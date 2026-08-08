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
