# DOORWAVE decode — registered readout columns (numbers only, no verdicts)

Decoder: `scratchpad/doorwave_decode.py` (this session), built on `tools/replay_census.py` primitives (fields/parse_entity/read_pos/scalars) — the same primitives `tools/corpus/replay_autopsy.py` uses. Engine-side only: placeEntity / moveBuilderBot / removeEntity / updateHp / updatePlayers / builderAttack. No stdout is read.

`d²` throughout = `eco.dsq_core` = min squared distance to the 2x2 core footprint (the bot's own metric, transcribed exactly).

## 0. POSITIVE CONTROL ON THE DETECTOR (mandatory, run before any treatment read)

| paired drive (skald s11, vs `bots/_probe_doorlaunch`) | door pecks read | our builderAttack events (any target) | exposure rounds |
|---|---|---|---|
| `scratchpad/s53_doorwave/flip_on.replay26` | **60** | 60 | 51 |
| `scratchpad/s53_doorwave/flip_off.replay26` | **0** | 0 | 94 |

Registered expectation in the prereg (§BASE RATE, dose path (i)): treatment 60 vs control 0. The detector reproduces **60 / 0** — both verdicts driven on the same surface.

⚠ DECODER DEFECT FOUND AND FIXED BY THAT CONTROL: the first build read **56 of 60** on `flip_on`. `removeEntity` can precede the killing blow's `builderAttack` inside the same round, so resolving the target tile against the live index alone drops exactly one peck per killed turret (4 turrets, 4 dropped pecks). A per-round shadow index of tiles vacated this round restores them. Without the control this would have under-counted every dose column by the killing blow.

⭐ SECOND-INSTRUMENT AGREEMENT ON THE ATTACK CHANNEL: this decoder's count of our `builderAttack` events was compared file-by-file against `corpus/econ.tsv`'s independently-built `attacks` column (built by `tools/corpus/replay_econ.py`, a different parser path) across all 100 leg games — **0 mismatches, 4,215 = 4,215 events.** The door filter is this session's work; the channel it filters is corroborated.

## 1. CELL MEMBERSHIP / PIN VERIFICATION

| cell | games | matches | our ver | opp | opp ver | seats (a/b) | maps (distinct) |
|---|---|---|---|---|---|---|---|
| F-C | 25 | 5 | v177 | farming_200s | v19 | 5/20 | 15: auroraveil×1, bifrost×2, fimbulwinter×1, glacierkeep×1, helheim×3, holmgang×2, icefloe×2, jotunheim×3, longhouse×2, midgard×1, paths×2, skald×1, stavkirke×1, valkyrie×1, yggdrasil×2 |
| F-T | 25 | 5 | v178 | farming_200s | v19 | 5/20 | 13: auroraveil×2, bifrost×3, fimbulwinter×2, glacierkeep×2, helheim×2, holmgang×1, icefloe×2, jotunheim×1, midgard×2, paths×1, skald×2, stavkirke×2, yggdrasil×3 |
| A-C | 25 | 5 | v177 | not adgato | v25 | 15/10 | 13: auroraveil×1, bifrost×2, fimbulwinter×3, glacierkeep×2, helheim×3, holmgang×2, icefloe×2, jotunheim×1, midgard×2, paths×2, stavkirke×3, valkyrie×1, yggdrasil×1 |
| A-T | 25 | 5 | v178 | not adgato | v25 | 15/10 | 14: auroraveil×2, bifrost×3, fimbulwinter×1, helheim×2, holmgang×1, icefloe×1, jotunheim×2, longhouse×1, midgard×3, paths×3, skald×2, stavkirke×1, valkyrie×2, yggdrasil×1 |

No decoded `oppver` differs from its pin inside any cell (§PIN INSTRUMENT-ALARM CLAUSE: CELL F = 19, CELL A = 25; no null values).

**Wall-clock separation between the halves of each cell** (`completedAt`, platform):

| cell | first game completed | last game completed |
|---|---|---|
| F-C | 2026-08-21T14:01:54.566Z | 2026-08-21T14:02:03.995Z |
| F-T | 2026-08-21T15:54:17.025Z | 2026-08-21T16:33:55.525Z |
| A-C | 2026-08-21T14:22:11.466Z | 2026-08-21T14:22:40.672Z |
| A-T | 2026-08-21T15:54:14.997Z | 2026-08-21T16:34:00.491Z |

## 2. DOSE COLUMN (GATE 1)

Door-verb peck event = a `builderAttack` by one of OUR builder bots whose target tile holds an ENEMY entity of type GUNNER/SENTINEL/LAUNCHER at d² ≤ 40 of OUR OWN core. (2 dmg/peck is the builder signature; gunner 7 / sentinel 18 arrive as `fireTurret`, a different event number, so the channels cannot mix.)

| cell | games with ≥1 peck / 25 | Wilson-95 (n_eff = 25/1.434 = 17.4) | total pecks | pecks/game (mean, max) | distinct turrets pecked (total) | first-peck round (median over pecked games) | Ti spent at 2/peck (total) |
|---|---|---|---|---|---|---|---|
| F-C | **0/25** | 0.0% [0.0, 18.1] | 0 | 0.0, 0 | 0 | — | 0 |
| F-T | **25/25** | 100.0% [81.9, 100.0] | 1916 | 76.6, 269 | 35 | 43 (n=25) | 3832 |
| A-C | **0/25** | 0.0% [0.0, 18.1] | 0 | 0.0, 0 | 0 | — | 0 |
| A-T | **18/25** | 72.0% [48.5, 87.5] | 182 | 7.3, 22 | 23 | 40 (n=18) | 364 |

### P3 instrument control — the control-arm zero is SELECTIVE, not blind

If the decoder simply could not see our attack channel in the control arm, the control zero would be an artefact. These columns are the complement: the same parse, same games, counting attacks the door filter REJECTS.

| cell | our builderAttack events, ANY target | of those: on an enemy BUILDING | on an enemy door-type turret at ANY d² | door pecks (d²≤40) |
|---|---|---|---|---|
| F-C | 753 | 753 | 0 | **0** |
| F-T | 3280 | 3280 | 1916 | **1916** |
| A-C | 0 | 0 | 0 | **0** |
| A-T | 182 | 182 | 182 | **182** |

Registered GATE-1 bands (§GATE RESOLUTION): ≥19/25 = DOSE BAR MET · ≤6/25 = DOSE FALSIFIER band · 7–18/25 = UNRESOLVED band.

* **F-T: 25/25 → ≥19/25 band.**
* **A-T: 18/25 → 7–18/25 band.**
* **F-C (control, P3 instrument check): 0/25 games, 0 peck events.**
* **A-C (control, P3 instrument check): 0/25 games, 0 peck events.**

### Per-game dose detail (treatment cells)

**F-T**

| game | pecks | distinct turrets | first peck | target kinds | target HP trajectories (id: born→deaths / deltas) |
|---|---|---|---|---|---|
| 3a83c26e_g1 | 186 | 2 | 45 | sentinel×186 | #99 sentinel r45→alive (-134/+134); #101 sentinel r46→alive (-238/+236) |
| 3a83c26e_g2 | 40 | 2 | 60 | sentinel×40 | #75 sentinel r38→r82 (-40/+0); #96 sentinel r53→r70 (-40/+0) |
| 3a83c26e_g3 | 74 | 1 | 37 | sentinel×74 | #79 sentinel r36→r157 (-267/+225) |
| 3a83c26e_g4 | 33 | 1 | 21 | sentinel×33 | #34 sentinel r20→alive (-66/+66) |
| 3a83c26e_g5 | 119 | 1 | 26 | sentinel×119 | #41 sentinel r22→alive (-238/+238) |
| 785ab980_g1 | 66 | 1 | 15 | sentinel×66 | #39 sentinel r15→alive (-132/+132) |
| 785ab980_g2 | 77 | 1 | 55 | sentinel×77 | #83 sentinel r55→alive (-154/+154) |
| 785ab980_g3 | 51 | 1 | 15 | sentinel×51 | #32 sentinel r11→r93 (-102/+62) |
| 785ab980_g4 | 69 | 1 | 13 | sentinel×69 | #19 sentinel r8→alive (-138/+138) |
| 785ab980_g5 | 98 | 2 | 29 | sentinel×98 | #34 sentinel r23→r48 (-40/+0); #35 sentinel r23→r114 (-156/+116) |
| d250bf69_g1 | 37 | 2 | 43 | sentinel×37 | #69 sentinel r42→alive (-14/+14); #73 sentinel r46→alive (-60/+60) |
| d250bf69_g2 | 66 | 1 | 31 | sentinel×66 | #50 sentinel r17→alive (-132/+132) |
| d250bf69_g3 | 58 | 2 | 101 | sentinel×58 | #59 sentinel r27→alive (-34/+34); #62 sentinel r28→alive (-82/+82) |
| d250bf69_g4 | 9 | 2 | 37 | sentinel×9 | #72 sentinel r36→alive (-4/+2); #75 sentinel r37→alive (-14/+14) |
| d250bf69_g5 | 78 | 1 | 51 | sentinel×78 | #74 sentinel r47→alive (-156/+156) |
| d6331013_g1 | 35 | 2 | 50 | sentinel×35 | #66 sentinel r40→r177 (-209/+169); #69 sentinel r42→alive (-8/+8) |
| d6331013_g2 | 38 | 1 | 43 | sentinel×38 | #76 sentinel r41→alive (-76/+76) |
| d6331013_g3 | 50 | 1 | 26 | sentinel×50 | #41 sentinel r22→alive (-100/+100) |
| d6331013_g4 | 40 | 2 | 46 | sentinel×40 | #99 sentinel r45→r56 (-40/+0); #103 sentinel r46→r71 (-40/+0) |
| d6331013_g5 | 34 | 1 | 52 | sentinel×34 | #87 sentinel r50→r80 (-68/+28) |
| dc572a83_g1 | 101 | 2 | 49 | sentinel×101 | #72 sentinel r47→r97 (-120/+78); #78 sentinel r55→alive (-124/+124) |
| dc572a83_g2 | 37 | 1 | 54 | sentinel×37 | #89 sentinel r50→alive (-74/+74) |
| dc572a83_g3 | 269 | 2 | 46 | sentinel×269 | #53 sentinel r30→r104 (-40/+0); #60 sentinel r38→r426 (-498/+458) |
| dc572a83_g4 | 80 | 1 | 13 | sentinel×80 | #24 sentinel r9→alive (-160/+160) |
| dc572a83_g5 | 171 | 1 | 21 | sentinel×171 | #31 sentinel r20→alive (-468/+464) |

**A-T**

| game | pecks | distinct turrets | first peck | target kinds | target HP trajectories (id: born→deaths / deltas) |
|---|---|---|---|---|---|
| 30f51cc4_g1 | 0 | 0 | — | — | — |
| 30f51cc4_g2 | 20 | 1 | 35 | sentinel×20 | #48 sentinel r35→r54 (-40/+0) |
| 30f51cc4_g3 | 9 | 1 | 59 | sentinel×9 | #105 sentinel r52→alive (-18/+0) |
| 30f51cc4_g4 | 16 | 2 | 56 | sentinel×16 | #77 sentinel r56→alive (-2/+0); #79 sentinel r57→alive (-30/+0) |
| 30f51cc4_g5 | 13 | 1 | 36 | sentinel×13 | #41 sentinel r33→alive (-26/+0) |
| 4f321630_g1 | 22 | 2 | 36 | sentinel×22 | #39 sentinel r33→r47 (-40/+0); #41 sentinel r35→alive (-4/+0) |
| 4f321630_g2 | 10 | 1 | 40 | sentinel×10 | #40 sentinel r40→alive (-20/+0) |
| 4f321630_g3 | 13 | 1 | 36 | sentinel×13 | #44 sentinel r35→alive (-26/+0) |
| 4f321630_g4 | 6 | 1 | 50 | sentinel×6 | #32 sentinel r40→alive (-12/+0) |
| 4f321630_g5 | 2 | 1 | 48 | sentinel×2 | #38 sentinel r35→alive (-4/+0) |
| 88c9b4ad_g1 | 18 | 1 | 54 | sentinel×18 | #86 sentinel r53→alive (-36/+0) |
| 88c9b4ad_g2 | 0 | 0 | — | — | — |
| 88c9b4ad_g3 | 10 | 1 | 59 | sentinel×10 | #30 sentinel r53→alive (-20/+0) |
| 88c9b4ad_g4 | 16 | 1 | 41 | sentinel×16 | #52 sentinel r41→alive (-32/+0) |
| 88c9b4ad_g5 | 1 | 1 | 47 | sentinel×1 | #43 sentinel r32→alive (-2/+0) |
| 944a7b62_g1 | 0 | 0 | — | — | — |
| 944a7b62_g2 | 0 | 0 | — | — | — |
| 944a7b62_g3 | 0 | 0 | — | — | — |
| 944a7b62_g4 | 3 | 2 | 40 | launcher×1, sentinel×2 | #35 sentinel r40→alive (-4/+0); #37 launcher r42→alive (-2/+0) |
| 944a7b62_g5 | 0 | 0 | — | — | — |
| f7f0bf11_g1 | 7 | 2 | 51 | sentinel×7 | #83 sentinel r51→alive (-4/+0); #91 sentinel r55→alive (-10/+0) |
| f7f0bf11_g2 | 1 | 1 | 34 | launcher×1 | #43 launcher r31→alive (-2/+0) |
| f7f0bf11_g3 | 1 | 1 | 31 | launcher×1 | #42 launcher r30→alive (-2/+0) |
| f7f0bf11_g4 | 0 | 0 | — | — | — |
| f7f0bf11_g5 | 14 | 2 | 39 | sentinel×14 | #33 sentinel r36→alive (-2/+0); #37 sentinel r40→alive (-26/+0) |

## 3. EXPOSURE COLUMN

Exposure round = a round in which ≥1 of our LIVING builder bots is orthogonally adjacent to a living enemy GUNNER/SENTINEL/LAUNCHER standing at d² ≤ 40 of our core (state read at end of round). Ti = our global titanium in that round (`updatePlayers`), against `FS_DOOR_TI_FLOOR = 6`.

| cell | games with ≥1 exposure round | exposure rounds (total, mean/game, max) | median Ti in exposure rounds | exposure rounds with Ti < 6 (total) |
|---|---|---|---|---|
| F-C | 21/25 | 471, 18.8, 83 | 15 | 44 |
| F-T | 25/25 | 1879, 75.2, 273 | 18 | 66 |
| A-C | 11/25 | 89, 3.6, 18 | 24 | 7 |
| A-T | 22/25 | 283, 11.3, 20 | 47 | 3 |

## 4. CELL F METRICS (farming_200s v19) — F1–F7

| # | metric | pre-registered control value | **F-C (control, n=25)** | **F-T (treatment, n=25)** |
|---|---|---|---|---|
| **F1 (PRIMARY)** | games with ≥1 forward sentinel (d²≤32) killed >2 rounds before game end | 25.0% (15/60) | **8/25 = 32.0%** Wilson-95 [15.2, 55.3] | **9/25 = 36.0%** Wilson-95 [18.0, 59.1] |
| F2 | share of their forward sentinels killed | 21.9% (21/96) | 10/45 = 22.2% | 13/40 = 32.5% |
| F3 | median lifetime of a killed forward sentinel | 74 rounds | 32.0 (n=10) | 50.0 (n=13) |
| F4 | forward sentinels alive at game end | 78.1% (75/96) | 35/45 = 77.8% | 27/40 = 67.5% |
| F5 | replant failure after we kill one (+ median latency when they do) | 14/21 (66.7%), median 34 | 8/10, median 37 | 13/13, — |
| F6 (COST) | our builder-rounds on the door / Ti at 2 per peck | 0 / 0 by construction | 0 / 0 Ti | 1916 / 3832 Ti |
| F7 (CONTEXT) | our core deaths, and whether a plant preceded each | 32/32 preceded | 16/25 dead, 16/16 plant-preceded | 14/25 dead, 14/14 plant-preceded |

**F1 two-arm difference (T − C): +4.0pp, registered half-width ±31.4pp** (`1.96×sqrt(p̄(1−p̄)×(1.434/25 + 1.434/25))`, p̄ = 0.340). Registered bar (§BAR 2): the 95% interval must EXCLUDE 0.

## 5. CELL A METRICS (not adgato v25) — A1–A7

| # | metric | pre-registered control value | **A-C (control, n=25)** | **A-T (treatment, n=25)** |
|---|---|---|---|---|
| **A1 (PRIMARY)** | plant-to-core-death lag, censored at +150 | 17/19/20/19/23, mean 19.6 (5 games) | mean **30.62** (n=24, sd 36.82), censored 2, no-plant games 1 | mean **18.40** (n=25, sd 2.00), censored 0, no-plant games 0 |
| A2 | enemy home sentinels (d²≤41) alive at r70 | 4/4/4/4/4 | mean 2.60, median 4 (n=5 games reaching r70) | mean 4.00, median 4 (n=4 games reaching r70) |
| A2b | same, at min(r70, last round) — the study's effective form (its 5 baseline games all ended before r70) | 4/4/4/4/4 | mean 3.68, median 4 (n=25) | mean 3.92, median 4 (n=25) |
| A3 | enemy home-sentinel deaths by r70 | 1 of 5 games | 4/25 games, 6 deaths | 2/25 games, 2 deaths |
| A4 | rounds first home plant → SECOND home sentinel death | never (5/5) | 1/25 games have a 2nd death, median 15 | 0/25 games have a 2nd death |
| A5 | round of the first enemy home sentinel | r30/40/35/43/43 | median r33 (n=24), range 21–54 | median r36 (n=25), range 30–54 |
| A6 | our core HP at r70 | dead in 5/5 | our core dead by r70 in 20/25; mean HP at r70 41.0 (n=25) | our core dead by r70 in 23/25; mean HP at r70 7.0 (n=25) |
| A7 (COST) | our builder-rounds on the door / Ti at 2 per peck | 0 / 0 by construction | 0 / 0 Ti | 182 / 364 Ti |

**A1 two-arm difference (T − C): -12.23 rounds**; pooled sd = 25.79 ⇒ half-width = 1.96 × 25.79 × sqrt(1.434 × (1/25 + 1/24)) = **±17.30 rounds** ⇒ 95% interval [-29.53, +5.08]. Registered bar (§BAR 3): interval must exclude BOTH 0 AND +5 rounds; the pre-committed sd ladder gives BAR = +22.30 rounds at this sd (and the registered default: sd > 15 ⇒ bar UNRESOLVED at this n).

## 6. KILL-ROUND GUARD (REPORTED-ONLY per §RATIFICATION 12)

ITT RMST₃₀₀ = mean enemy-core-kill round censored at r300 over ALL games of the arm (no kill scores 300). Kill round = the round our decoder sees the enemy core's HP cross 0 / its removeEntity.

| cell pair | arm | RMST₃₀₀ (mean) | sd | ITT timely-kill by r300 | kills observed |
|---|---|---|---|---|---|
| F | F-C | 272.2 | 59.0 | 5/25 = 20.0% Wilson-95 [7.6, 43.3] | 5 |
| F | F-T | 283.3 | 41.1 | 6/25 = 24.0% Wilson-95 [9.9, 47.4] | 6 |
| A | A-C | 287.0 | 42.3 | 3/25 = 12.0% Wilson-95 [3.4, 34.3] | 3 |
| A | A-T | 300.0 | 0.0 | 0/25 = 0.0% Wilson-95 [0.0, 18.1] | 0 |

* **CELL F RMST₃₀₀ difference (T − C) = +11.1 rounds** — observed pooled sd 50.8 ⇒ half-width ±33.7 rounds; the prereg's registered class interval at sd≈100 is **±66 rounds** (`1.96 × 100 × sqrt(1.434 × 2/25)`), and the readout must print the difference with that interval in the same sentence.
  ITT timely-kill-by-r300 share: F-T 6/25 = 24.0% vs F-C 5/25 = 20.0% ⇒ +4.0pp, half-width ±27.5pp.
* **CELL A RMST₃₀₀ difference (T − C) = +13.0 rounds** — observed pooled sd 29.9 ⇒ half-width ±19.9 rounds; the prereg's registered class interval at sd≈100 is **±66 rounds** (`1.96 × 100 × sqrt(1.434 × 2/25)`), and the readout must print the difference with that interval in the same sentence.
  ITT timely-kill-by-r300 share: A-T 0/25 = 0.0% vs A-C 3/25 = 12.0% ⇒ -12.0pp, half-width ±15.8pp.

## 7. FIXTURE CHECKS (pre-committed positive controls on the fixture)

* **F-C forward-sentinel kill share vs 25.0% (±20pp tolerance):** observed **8/25 = 32.0%** (F1 form: ≥1 forward sentinel killed >2 rounds before game end). |32.0 − 25.0| = 7.0pp ⇒ **inside** the registered ±20pp tolerance.
* **A-C `sentinels alive at r70` reading 4 in the large majority:** 3/5 games that reach r70 read exactly 4 (distribution: {"0": 1, "1": 1, "4": 3}); games not reaching r70: 20.
* **A-C our core dead by r70 in the large majority:** 20/25.

## 8. GAME-LEVEL TABLE (descriptive)

### F-C — game share 9/25 = 36.0% (±23.5pp half-width; descriptive only, never a verdict input)

| game | map | seat | winner | cond | turns | pecks | exp rounds | our core dead | their core dead |
|---|---|---|---|---|---|---|---|---|---|
| 695f892a_g1 | glacierkeep | b | them | core_destroyed | 194 | 0 | 5 | 193 | — |
| 695f892a_g2 | holmgang | b | them | core_destroyed | 343 | 0 | 0 | 342 | — |
| 695f892a_g3 | jotunheim | b | them | core_destroyed | 345 | 0 | 22 | 344 | — |
| 695f892a_g4 | valkyrie | b | us | core_destroyed | 144 | 0 | 0 | — | 143 |
| 695f892a_g5 | fimbulwinter | b | them | core_destroyed | 826 | 0 | 13 | 825 | — |
| 9f9439bf_g1 | stavkirke | b | them | core_destroyed | 173 | 0 | 11 | 172 | — |
| 9f9439bf_g2 | yggdrasil | b | us | core_destroyed | 488 | 0 | 4 | — | 487 |
| 9f9439bf_g3 | bifrost | b | us | core_destroyed | 321 | 0 | 48 | — | 320 |
| 9f9439bf_g4 | helheim | b | them | core_destroyed | 160 | 0 | 46 | 159 | — |
| 9f9439bf_g5 | longhouse | b | us | core_destroyed | 161 | 0 | 12 | — | 160 |
| a3ead0e1_g1 | auroraveil | b | us | harvesters | 1000 | 0 | 10 | — | — |
| a3ead0e1_g2 | icefloe | b | them | core_destroyed | 185 | 0 | 25 | 184 | — |
| a3ead0e1_g3 | longhouse | b | us | core_destroyed | 117 | 0 | 1 | — | 116 |
| a3ead0e1_g4 | skald | b | us | core_destroyed | 222 | 0 | 38 | — | 221 |
| a3ead0e1_g5 | midgard | b | them | core_destroyed | 224 | 0 | 7 | 223 | — |
| c0643408_g1 | jotunheim | a | them | core_destroyed | 386 | 0 | 2 | 385 | — |
| c0643408_g2 | yggdrasil | a | them | core_destroyed | 285 | 0 | 0 | 284 | — |
| c0643408_g3 | paths | a | them | core_destroyed | 122 | 0 | 46 | 121 | — |
| c0643408_g4 | helheim | a | us | core_destroyed | 353 | 0 | 0 | — | 352 |
| c0643408_g5 | bifrost | a | them | core_destroyed | 139 | 0 | 9 | 138 | — |
| e0c1afe9_g1 | paths | b | them | core_destroyed | 153 | 0 | 12 | 152 | — |
| e0c1afe9_g2 | holmgang | b | them | core_destroyed | 121 | 0 | 9 | 120 | — |
| e0c1afe9_g3 | icefloe | b | them | core_destroyed | 217 | 0 | 83 | 216 | — |
| e0c1afe9_g4 | helheim | b | us | core_destroyed | 165 | 0 | 20 | — | 164 |
| e0c1afe9_g5 | jotunheim | b | them | core_destroyed | 325 | 0 | 48 | 324 | — |

### F-T — game share 9/25 = 36.0% (±23.5pp half-width; descriptive only, never a verdict input)

| game | map | seat | winner | cond | turns | pecks | exp rounds | our core dead | their core dead |
|---|---|---|---|---|---|---|---|---|---|
| 3a83c26e_g1 | midgard | b | them | core_destroyed | 357 | 186 | 184 | 356 | — |
| 3a83c26e_g2 | bifrost | b | us | core_destroyed | 253 | 40 | 27 | — | 252 |
| 3a83c26e_g3 | stavkirke | b | us | core_destroyed | 276 | 74 | 43 | — | 275 |
| 3a83c26e_g4 | auroraveil | b | them | core_destroyed | 269 | 33 | 27 | 268 | — |
| 3a83c26e_g5 | glacierkeep | b | them | core_destroyed | 257 | 119 | 107 | 256 | — |
| 785ab980_g1 | helheim | b | us | core_destroyed | 357 | 66 | 52 | — | 356 |
| 785ab980_g2 | yggdrasil | b | them | core_destroyed | 195 | 77 | 43 | 194 | — |
| 785ab980_g3 | holmgang | b | us | core_destroyed | 284 | 51 | 53 | — | 283 |
| 785ab980_g4 | skald | b | them | core_destroyed | 201 | 69 | 78 | 200 | — |
| 785ab980_g5 | jotunheim | b | them | harvesters | 1000 | 98 | 73 | — | — |
| d250bf69_g1 | bifrost | a | them | core_destroyed | 507 | 37 | 24 | 506 | — |
| d250bf69_g2 | helheim | a | us | core_destroyed | 117 | 66 | 85 | — | 116 |
| d250bf69_g3 | icefloe | a | them | core_destroyed | 237 | 58 | 95 | 236 | — |
| d250bf69_g4 | stavkirke | a | them | core_destroyed | 133 | 9 | 9 | 132 | — |
| d250bf69_g5 | yggdrasil | a | us | core_destroyed | 384 | 78 | 54 | — | 383 |
| d6331013_g1 | paths | b | them | core_destroyed | 572 | 35 | 117 | 571 | — |
| d6331013_g2 | bifrost | b | them | core_destroyed | 601 | 38 | 39 | 600 | — |
| d6331013_g3 | glacierkeep | b | them | titanium_stored | 237 | 50 | 59 | 236 | 236 |
| d6331013_g4 | midgard | b | us | core_destroyed | 221 | 40 | 26 | — | 220 |
| d6331013_g5 | fimbulwinter | b | them | titanium_collected | 1000 | 34 | 28 | — | — |
| dc572a83_g1 | yggdrasil | b | them | core_destroyed | 265 | 101 | 109 | 264 | — |
| dc572a83_g2 | fimbulwinter | b | them | core_destroyed | 116 | 37 | 53 | 115 | — |
| dc572a83_g3 | icefloe | b | us | titanium_collected | 1000 | 269 | 273 | — | — |
| dc572a83_g4 | skald | b | us | core_destroyed | 349 | 80 | 83 | — | 348 |
| dc572a83_g5 | auroraveil | b | them | core_destroyed | 169 | 171 | 138 | 168 | — |

### A-C — game share 3/25 = 12.0% (±23.5pp half-width; descriptive only, never a verdict input)

| game | map | seat | winner | cond | turns | pecks | exp rounds | our core dead | their core dead |
|---|---|---|---|---|---|---|---|---|---|
| 099d1b47_g1 | stavkirke | a | them | core_destroyed | 76 | 0 | 0 | 75 | — |
| 099d1b47_g2 | icefloe | a | them | core_destroyed | 53 | 0 | 13 | 52 | — |
| 099d1b47_g3 | paths | a | them | core_destroyed | 78 | 0 | 0 | 77 | — |
| 099d1b47_g4 | helheim | a | them | core_destroyed | 43 | 0 | 0 | 42 | — |
| 099d1b47_g5 | midgard | a | them | core_destroyed | 66 | 0 | 2 | 65 | — |
| 0beb09c5_g1 | paths | a | them | core_destroyed | 65 | 0 | 0 | 64 | — |
| 0beb09c5_g2 | fimbulwinter | a | them | core_destroyed | 49 | 0 | 0 | 48 | — |
| 0beb09c5_g3 | yggdrasil | a | them | core_destroyed | 69 | 0 | 0 | 68 | — |
| 0beb09c5_g4 | bifrost | a | them | core_destroyed | 62 | 0 | 9 | 61 | — |
| 0beb09c5_g5 | holmgang | a | us | core_destroyed | 115 | 0 | 0 | — | 114 |
| 5acd145d_g1 | valkyrie | a | them | core_destroyed | 52 | 0 | 0 | 51 | — |
| 5acd145d_g2 | stavkirke | a | them | core_destroyed | 57 | 0 | 0 | 56 | — |
| 5acd145d_g3 | helheim | a | them | core_destroyed | 58 | 0 | 0 | 57 | — |
| 5acd145d_g4 | glacierkeep | a | them | core_destroyed | 59 | 0 | 0 | 58 | — |
| 5acd145d_g5 | auroraveil | a | them | core_destroyed | 52 | 0 | 18 | 51 | — |
| 993e749d_g1 | stavkirke | b | them | core_destroyed | 53 | 0 | 1 | 52 | — |
| 993e749d_g2 | bifrost | b | them | core_destroyed | 54 | 0 | 0 | 53 | — |
| 993e749d_g3 | fimbulwinter | b | them | core_destroyed | 52 | 0 | 2 | 51 | — |
| 993e749d_g4 | holmgang | b | us | core_destroyed | 271 | 0 | 0 | — | 270 |
| 993e749d_g5 | jotunheim | b | them | core_destroyed | 45 | 0 | 17 | 44 | — |
| cb9b2822_g1 | fimbulwinter | b | us | core_destroyed | 193 | 0 | 1 | — | 192 |
| cb9b2822_g2 | icefloe | b | them | core_destroyed | 56 | 0 | 11 | 55 | — |
| cb9b2822_g3 | helheim | b | them | core_destroyed | 53 | 0 | 0 | 52 | — |
| cb9b2822_g4 | midgard | b | them | core_destroyed | 70 | 0 | 2 | 69 | — |
| cb9b2822_g5 | glacierkeep | b | them | core_destroyed | 63 | 0 | 13 | 62 | — |

### A-T — game share 0/25 = 0.0% (±23.5pp half-width; descriptive only, never a verdict input)

| game | map | seat | winner | cond | turns | pecks | exp rounds | our core dead | their core dead |
|---|---|---|---|---|---|---|---|---|---|
| 30f51cc4_g1 | valkyrie | b | them | core_destroyed | 63 | 0 | 5 | 62 | — |
| 30f51cc4_g2 | bifrost | b | them | core_destroyed | 56 | 20 | 20 | 55 | — |
| 30f51cc4_g3 | midgard | b | them | core_destroyed | 68 | 9 | 12 | 67 | — |
| 30f51cc4_g4 | longhouse | b | them | core_destroyed | 72 | 16 | 16 | 71 | — |
| 30f51cc4_g5 | paths | b | them | core_destroyed | 49 | 13 | 14 | 48 | — |
| 4f321630_g1 | paths | b | them | core_destroyed | 50 | 22 | 15 | 49 | — |
| 4f321630_g2 | yggdrasil | b | them | core_destroyed | 53 | 10 | 10 | 52 | — |
| 4f321630_g3 | skald | b | them | core_destroyed | 49 | 13 | 16 | 48 | — |
| 4f321630_g4 | jotunheim | b | them | core_destroyed | 56 | 6 | 7 | 55 | — |
| 4f321630_g5 | auroraveil | b | them | core_destroyed | 50 | 2 | 5 | 49 | — |
| 88c9b4ad_g1 | midgard | a | them | core_destroyed | 70 | 18 | 18 | 69 | — |
| 88c9b4ad_g2 | helheim | a | them | core_destroyed | 54 | 0 | 0 | 53 | — |
| 88c9b4ad_g3 | jotunheim | a | them | core_destroyed | 69 | 10 | 11 | 68 | — |
| 88c9b4ad_g4 | bifrost | a | them | core_destroyed | 57 | 16 | 17 | 56 | — |
| 88c9b4ad_g5 | valkyrie | a | them | core_destroyed | 48 | 1 | 5 | 47 | — |
| 944a7b62_g1 | bifrost | a | them | core_destroyed | 61 | 0 | 19 | 60 | — |
| 944a7b62_g2 | skald | a | them | core_destroyed | 71 | 0 | 0 | 70 | — |
| 944a7b62_g3 | paths | a | them | core_destroyed | 78 | 0 | 0 | 77 | — |
| 944a7b62_g4 | stavkirke | a | them | core_destroyed | 60 | 3 | 10 | 59 | — |
| 944a7b62_g5 | icefloe | a | them | core_destroyed | 54 | 0 | 17 | 53 | — |
| f7f0bf11_g1 | midgard | a | them | core_destroyed | 71 | 7 | 16 | 70 | — |
| f7f0bf11_g2 | helheim | a | them | core_destroyed | 51 | 1 | 18 | 50 | — |
| f7f0bf11_g3 | auroraveil | a | them | core_destroyed | 49 | 1 | 7 | 48 | — |
| f7f0bf11_g4 | holmgang | a | them | core_destroyed | 51 | 0 | 9 | 50 | — |
| f7f0bf11_g5 | fimbulwinter | a | them | core_destroyed | 54 | 14 | 16 | 53 | — |

## 9. ANTI-GOODHART COLUMN — what happened to the pecked turrets

The prereg's anti-Goodhart clause: *peck counts up with turret lifetime flat is a NULL, not a hit.* This table separates damage delivered from damage that stuck. HP deltas are read off `updateHp` on the pecked turret ids.

| cell | pecks | dmg delivered by pecks (2/peck) | observed NEGATIVE HP deltas on pecked turrets | observed POSITIVE (heal) deltas on those turrets | pecked turrets that died / pecked turrets |
|---|---|---|---|---|---|
| F-T | 1916 | 3832 | -4266 | +3734 | 13/35 |
| A-T | 182 | 364 | -364 | +0 | 2/23 |

## 10. CAVEATS ON THESE COLUMNS (read before quoting any of them)

* **`killed` = a `removeEntity` on that turret id.** The wire does not name a killer, so an enemy `self_destruct` or their own `destroy` would be counted as a kill by us. F1/F2/F4/A3/A4 all rest on that.
* **The A-C control zero is not self-discriminating.** Our builders made **0 builderAttack events of any kind** in all 25 A-C games (the games are short and end with our core dead), so nothing in that cell could have been misattributed either way. The discriminating control-arm read is F-C: **753 of our builderAttack events, 0 of them door pecks** — plus the flip_off drive (0 pecks) and flip_on (60/60).
* **Exposure is sampled at end-of-round state.** A builder that stepped adjacent and acted inside the same round is counted; one that was adjacent only mid-round is not.
* **A2 has two windows** (A2 at r70 for the few games reaching it; A2b at min(70, last round), which is the form the study's 5 baseline games effectively used). Both are printed; they are not interchangeable.
* **F6/A7 charge only the ACTION.** Builder-rounds counted are pecks delivered (1 round each, 2 Ti each). Rounds spent walking to the door are not separable on the wire and are NOT in that number — the cost side is a lower bound. The exposure column is the nearest upper-bound proxy.
* **No cross-cell pooling is computed here**, per §WHAT THIS LEG DOES NOT REGISTER (pooling the two opponents revives the OPPONENT cluster).
