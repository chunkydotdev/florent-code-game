# Harvester saturation: a general law that dissolves, and one that survives

**Research arm, session 20, 2026-08-09 00:0x CEST.** Live version **v80 "Eir 9b"**
(`bots/_v89sh`) after the v86 rollback at n=4. Data spans our **v72–v84**.
**Sources:** all 455 of our archived replays, per-round harvester tracking over
`placeEntity`/`removeEntity`, plus ore geometry from the `Map` message.
**ZERO downloads.** Run during the 20-match slot freeze — no ladder input needed.

Generalises the hive decode (`hive-decode-2026-08-08.md`): hive is the map where
we saturate the ore field worst. Is that a hive quirk or a global defect?

---

## 1. It is a hive quirk. We out-saturate the field everywhere else.

Saturation = harvesters / (ore tiles ÷ 2), the per-side cap on a mirror-symmetric
map. Peak over the game:

```
map           n   cap   OUR pk   sat   THEIR pk   sat     gap
hive         34     6      3.0   50%        5.5   92%    -42%   <<<
eider        24    16      6.0   38%        9.5   59%    -22%
heart        37    14      3.0   21%        4.0   29%     -7%
drumlin      32    15      8.5   57%        9.5   63%     -7%
...
meander      35    12      7.0   58%        2.0   17%    +42%
lighthouse   26     6      6.0  100%        4.0   67%    +33%
fjordgate    24     3      3.0  100%        2.0   67%    +33%

POOLED across 455 games:  OURS 64%   THEIRS 56%
```

**We are the better saturating side overall.** hive is a −42pp outlier against a
+8pp average, and the second-worst map is less than half as bad. That is a
third independent confirmation of the hive cell, on an axis the first two did
not use.

## 2. The tempting law — and it is a collider

Peak saturation looks like it predicts winning:

```
our peak saturation in WINS   n=217  median 75%
our peak saturation in LOSSES n=238  median 59%
Mann-Whitney p = 0.0013
```

**This is false and I nearly shipped it.** *Peak over the game* conditions on
game length, and game length conditions on the outcome — winners get more rounds
in which to reach a peak. It is structurally the same defect the instrument
audit found in `ceiling.py` hours earlier (median turns-to-kill computed over
kills only), wearing different clothes.

Re-measured at a **fixed round**, where every surviving game contributes exactly
one observation regardless of how it ends:

```
r50    games alive 455   WINS 28%  LOSSES 31%   p = 0.53
r100   games alive 419   WINS 43%  LOSSES 39%   p = 0.85
r150   games alive 362   WINS 50%  LOSSES 50%   p = 0.088
```

**No separation at any round.** The game-level law does not exist. At equal
elapsed time, the games we win and the games we lose have the same harvester
saturation.

**Consequence: do not build a "maximise harvester saturation" plank.** The only
evidence for it is a collider, and this is precisely the class of plausible,
well-measured, useless result the project has been paying for all night.

## 3. What survives: the map-level relationship

The per-map *gap* (ours minus theirs) at a fixed r100, against our win rate on
that map:

```
map           n   our sat  their sat    GAP   win%
hive         32      50%       67%     -17%    12%   <<<
snowflake    30      31%       44%      -9%    37%
eider        22      31%       44%      -9%    32%
...
meander      35      33%        8%     +17%    77%
antler       23      50%       33%     +33%    48%
fjordgate    22     100%       33%     +50%    55%

corr(saturation gap at r100, our win rate) across 15 maps:  r = +0.61
```

This is a **map-level** claim, not a game-level one, so it is not subject to the
section-2 confound — the gap is measured at a fixed round and the win rate is a
property of the map, not of any single game's length.

**Read it as a map-selection diagnostic, not a control lever.** r=+0.61 on n=15
points is one strong outlier (hive) plus a loose trend; drop hive and it
weakens. It says *the maps where we lose the ore race are the maps we lose*, and
that is a description of where to look, not a mechanism to optimise.

## 4. Standing caveats

- **n=15 maps** for the correlation. hive is influential; the relationship is
  suggestive, not established.
- **The cap is estimated** as ore÷2 assuming mirror symmetry. Contested ore
  (33% of hive's tiles are roughly equidistant) means the true per-side cap is
  soft — opponents exceeded my estimated cap on hive repeatedly (Lunds 8,
  Powerpuff 9 against a cap of 6).
- **v72–v84 pooled**, 13 versions. Live v80 is inside the pool.
- **Saturation ignores harvester quality** — a connected harvester and an
  orphaned one count the same here. `chain_dir` in the census tool is the
  measure that distinguishes them and it is not combined with this one.
