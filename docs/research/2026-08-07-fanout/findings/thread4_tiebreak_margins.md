# Thread 4: Tiebreak-Margin Flip Candidates (2026-08-07)

Read-only replay analysis. All 21 current-era (our version ≥ 54) r1000 losses were already in the shared
replay cache (`SCRATCH/replay_cache/replays/`) — **zero new downloads** were needed for this task.

**Segmentation directive applied**: rows are tagged `CL` (current-line, our version ≥ 59) or `og`
(older-generation, v54–58, context only — that bot no longer plays). Totals are reported both ways.

## Methodology

- **Deciding tiebreak**: compared `delivered` (titanium collected into own core, tiebreak #1) →
  `harvesters alive` (#2) → `stored` (global titanium bank, #3) → coinflip (#4), in engine order.
- **Lever (a) endgame spend-switch**: anchored at round 960 (40 rounds remaining). `k_afford` = max
  harvesters purchasable from our r960 bank, iterating the real scale formula
  (`cost = floor((1 + 0.05·n_harvesters_alive) × 20)`, cost re-evaluated after each purchase — not a
  flat-cost approximation). Each hypothetical harvester adds `((1000−960)//4)×10 = 100` Ti to our
  delivered total and +1 to our final harvester count (per the brief's formula). `a_flip_k` is the
  *smallest* k (searched in tiebreak order — delivered, then harvester-count, then stored) that
  flips the game; `a_flippable` is true iff that k is ≤ `k_afford`.
- **Lever (b) harvester-adjacent conveyor splice**: also anchored at r960. An enemy harvester counts as
  spliceable if (i) it has ≥1 orthogonally-adjacent tile that is empty (no building, not a wall — the
  literal `is_tile_empty` definition) and (ii) that tile is within Chebyshev distance 12 of any of our
  alive builder bots' r960 positions (a rough, generous "could walk there" proxy — no pathfinding).
  Each spliced harvester diverts `40 rounds × 2.5 Ti/rnd × 0.5 = 50` Ti from their delivered total to
  ours = **100 Ti double swing** per harvester, per the brief's formula.
- **Lever (c) one more delivered stack**: whether the delivered deficit (`delivered_them − delivered_us`,
  only when tiebreak #1 was the actual decider or tied) is ≤ 10 / 50 / 190 Ti (k = 1 / 5 / 19 stacks).
- Match ids resolved against `all_games_flat.json`; all 21 map names cross-checked against the brief
  and confirmed exact.

## Ranked table (closest margin first, by |delivered delta|)

| # | Replay id | Map | Opponent | v / line | Decider | Delivered Δ | Harv Δ | Stored Δ | Bank@r960 | Flippable by |
|---|---|---|---|---|---|---:|---:|---:|---:|---|
| 1 | `3b2c12df-d6b2-4ac0-a788-6edb8d4a3876_g3` | atoll | Oresund Overflow | v56 og | **2-harvesters** | 0 (tied) | −4 | +2025 | 2195 | **a** (k=1) |
| 2 | `c106d3d2-c401-4769-b958-b4a4cb7997ad_g3` | hive | Orizon | v56 og | 1-delivered | −260 | −5 | +2631 | 2700 | **a** (k=3), **b** (n=3 of 4 spliceable) |
| 3 | `ad08eb70-4926-4d8a-b459-b48ace96f56c_g2` | jackpot | OopsGotYourElo | v62 CL | 1-delivered | −710 | −1 | −3185 | 4720 | **a** (k=8) |
| 4 | `c00e6c30-1604-4f79-9389-99919c37c16f_g3` | jackpot | Lunds Stallions | v54 og | 1-delivered | −1610 | 0 | +254 | 9067 | **a** (k=17) |
| 5 | `57d5f794-d52f-499c-a04e-3b5d0f60a351_g1` | antler | Memtrace | v61 CL | 1-delivered | −2300 | +2 | −2660 | 4652 | **a** (k=23) |
| 6 | `706faea6-52be-46bf-9b2f-e8d084fc85ed_g3` | hive | Ouroboros | v61 CL | 1-delivered | −2370 | −1 | −2462 | 3834 | **a** (k=24) |
| 7 | `15cabb2e-219e-4c10-b559-bfdf0d1308a6_g5` | fjordgate | farming_200s | v58 og | 1-delivered | −3150 | −1 | −3836 | 2 | — (bank empty at r960) |
| 8 | `17622ae0-d28d-480b-bf12-334997b95116_g1` | saga | Ouroboros | v56 og | 1-delivered | −3900 | −4 | −4042 | 5419 | **a** (k=39) |
| 9 | `17622ae0-d28d-480b-bf12-334997b95116_g5` | jackpot | Ouroboros | v56 og | 1-delivered | −4080 | −2 | −2698 | 6898 | **a** (k=41) |
| 10 | `2618b9b4-c4b8-47f6-acbc-bee5cff5d25f_g3` | atoll | I Stone | v59 CL | 1-delivered | −4300 | −2 | +2268 | 2701 | **a** (k=43) |
| 11 | `706faea6-52be-46bf-9b2f-e8d084fc85ed_g4` | snowflake | Ouroboros | v61 CL | 1-delivered | −5730 | 0 | −1185 | 11257 | **a** (k=58) |
| 12 | `2cfcb658-8c59-4473-9ee0-9971aab1f53a_g2` | nordkap | Ouroboros | v54 og | 1-delivered | −5740 | +9 | −2223 | 13603 | **a** (k=58) |
| 13 | `2618b9b4-c4b8-47f6-acbc-bee5cff5d25f_g4` | drumlin | I Stone | v59 CL | 1-delivered | −8740 | −15 | +2143 | 6518 | **a** (k=88) |
| 14 | `17622ae0-d28d-480b-bf12-334997b95116_g3` | heart | Ouroboros | v56 og | 1-delivered | −9280 | +3 | −7830 | 5254 | — (deficit 9280 > k_afford×100) |
| 15 | `abbf93b4-cbca-4ba7-af80-583d628c6bed_g2` | antler | Askar City | v56 og | 1-delivered | −9850 | −11 | −9667 | 12 | — (bank essentially empty) |
| 16 | `3712fb12-b052-4f1e-bc61-ae517a1585c0_g1` | saga | Lunds Stallions | v55 og | 1-delivered | −12060 | −12 | −8350 | 134 | — |
| 17 | `2618b9b4-c4b8-47f6-acbc-bee5cff5d25f_g2` | saga | I Stone | v59 CL | 1-delivered | −13000 | −5 | −12961 | 7308 | — |
| 18 | `c2e57b46-13ed-46be-9a85-c6e3d5af9acd_g4` | eider | Lunds Stallions | v60 CL | 1-delivered | −13240 | −21 | +942 | 6038 | — |
| 19 | `12df1f45-3317-4ce3-bd3e-ecb2fd26f552_g1` | saga | Powerpuff Girls | v56 og | 1-delivered | −14380 | −15 | −9710 | 4754 | — |
| 20 | `12df1f45-3317-4ce3-bd3e-ecb2fd26f552_g3` | drumlin | Powerpuff Girls | v56 og | 1-delivered | −17430 | −11 | −13505 | 4301 | — |
| 21 | `706faea6-52be-46bf-9b2f-e8d084fc85ed_g1` | eider | Ouroboros | v61 CL | 1-delivered | −24030 | −10 | −18482 | 8106 | — |

Full uuids: `2cfcb658-8c59-4473-9ee0-9971aab1f53a`, `c00e6c30-1604-4f79-9389-99919c37c16f`,
`3712fb12-b052-4f1e-bc61-ae517a1585c0`, `c106d3d2-c401-4769-b958-b4a4cb7997ad`,
`abbf93b4-cbca-4ba7-af80-583d628c6bed`, `12df1f45-3317-4ce3-bd3e-ecb2fd26f552`,
`17622ae0-d28d-480b-bf12-334997b95116`, `3b2c12df-d6b2-4ac0-a788-6edb8d4a3876`,
`15cabb2e-219e-4c10-b559-bfdf0d1308a6`, `c2e57b46-13ed-46be-9a85-c6e3d5af9acd`,
`2618b9b4-c4b8-47f6-acbc-bee5cff5d25f`, `57d5f794-d52f-499c-a04e-3b5d0f60a351`,
`706faea6-52be-46bf-9b2f-e8d084fc85ed`, `ad08eb70-4926-4d8a-b459-b48ace96f56c`.

**Lever (c) note**: not a single one of the 21 delivered-deficits is ≤190 Ti (19 stacks) — the smallest
is 260 Ti (row 2, hive). "One more delivered stack" flips **zero** games at k=1, 5, or 19. The framing
of tiebreak losses as narrow-margin didn't survive contact with the arithmetic: r1000 losses are decided
by hundreds-to-tens-of-thousands of Ti, not single stacks.

## Totals per lever

### All 21 (full current-era set)

| Lever | Games flipped | Elo value @ 6.4/game |
|---|---:|---:|
| (a) endgame spend-switch | 12 / 21 | +76.8 |
| (b) harvester-adjacent splice | 1 / 21 | +6.4 |
| (c) k=1 stack | 0 / 21 | +0.0 |
| (c) k=5 stacks | 0 / 21 | +0.0 |
| (c) k=19 stacks | 0 / 21 | +0.0 |
| **Combined (a or b or c19)** | **12 / 21** | **+76.8** |

(Lever b adds no game lever a doesn't already cover — hive/Orizon is flippable by both.)

### Current-line only (our version ≥ 59 — v59, v60, v61, v62; n=9)

| Lever | Games flipped | Elo value @ 6.4/game |
|---|---:|---:|
| (a) endgame spend-switch | 6 / 9 | +38.4 |
| (b) harvester-adjacent splice | 0 / 9 | +0.0 |
| (c) k=1 / k=5 / k=19 stacks | 0 / 9 | +0.0 |
| **Combined** | **6 / 9** | **+38.4** |

Current-line flips: ad08eb70 g2 jackpot (k=8), 57d5f794 g1 antler (k=23), 706faea6 g3 hive (k=24),
2618b9b4 g3 atoll (k=43), 706faea6 g4 snowflake (k=58), 2618b9b4 g4 drumlin (k=88).

### Older-generation only (v54–58, context — bot no longer plays; n=12)

| Lever | Games flipped | Elo value @ 6.4/game |
|---|---:|---:|
| (a) endgame spend-switch | 6 / 12 | +38.4 |
| (b) harvester-adjacent splice | 1 / 12 | +6.4 |
| (c) k=1 / k=5 / k=19 stacks | 0 / 12 | +0.0 |
| **Combined** | **6 / 12** | **+38.4** |

Older-gen flips: 3b2c12df g3 atoll (k=1!), c106d3d2 g3 hive (k=3, also b), c00e6c30 g3 jackpot (k=17),
17622ae0 g1 saga (k=39), 17622ae0 g5 jackpot (k=41), 2cfcb658 g2 nordkap (k=58).

## Task 3: lost-2-3 series scan (current era)

6 lost-2-3 series found at our version ≥ 54 (all 5 games played, we won exactly 2):

| Series | Opponent | Our version |
|---|---|---|
| `3712fb12-b052-4f1e-bc61-ae517a1585c0` | Lunds Stallions | v55 |
| `c106d3d2-c401-4769-b958-b4a4cb7997ad` | Orizon | v56 |
| `3b2c12df-d6b2-4ac0-a788-6edb8d4a3876` | Oresund Overflow | v56 |
| `2618b9b4-c4b8-47f6-acbc-bee5cff5d25f` | I Stone | v59 (current-line) |
| `249f211f-5a7d-45ef-a75a-6081deb128d4` | 0033 | v58 |
| `a72b53f9-478f-4fbf-b24b-9f62a729e44e` | Orizon | v61 (current-line) |

The first four already contribute their r1000 loss(es) to the 21-game set above. `249f211f` and
`a72b53f9` have **no r1000 games at all** — every game in both series ended by `core_destroyed`.
Listing every non-r1000 loss in all 6 series as candidates for a future close-margin pass
(**list only — no replay decode performed**, per scope):

| Replay id (match_g#) | Map | Turns played |
|---|---|---:|
| `3712fb12-b052-4f1e-bc61-ae517a1585c0_g3` | heart | 184 |
| `3712fb12-b052-4f1e-bc61-ae517a1585c0_g5` | moonrise | 238 |
| `c106d3d2-c401-4769-b958-b4a4cb7997ad_g2` | jackpot | 213 |
| `c106d3d2-c401-4769-b958-b4a4cb7997ad_g5` | fjordgate | 350 |
| `3b2c12df-d6b2-4ac0-a788-6edb8d4a3876_g4` | jackpot | 500 |
| `3b2c12df-d6b2-4ac0-a788-6edb8d4a3876_g5` | nordkap | 115 |
| `249f211f-5a7d-45ef-a75a-6081deb128d4_g1` | jackpot | 65 |
| `249f211f-5a7d-45ef-a75a-6081deb128d4_g4` | eider | 196 |
| `249f211f-5a7d-45ef-a75a-6081deb128d4_g5` | saga | 377 |
| `a72b53f9-478f-4fbf-b24b-9f62a729e44e_g1` | eider | 93 |
| `a72b53f9-478f-4fbf-b24b-9f62a729e44e_g3` | drumlin | 173 |
| `a72b53f9-478f-4fbf-b24b-9f62a729e44e_g5` | snowflake | 115 |

(`2618b9b4` has no non-r1000 games — all 5 of its games ran the full 1000 rounds.) `249f211f` and
`a72b53f9` are match ids outside this thread's 14-match core set; their match_info was already cached
from prior sessions (no download needed here). `a72b53f9`'s three candidate games (g1 eider, g3 drumlin,
g5 snowflake) happen to already have cached `.replay26` files too (from other agents' work), but were
**not decoded** here — out of scope per the "list only" instruction. `249f211f`'s three candidates have
no cached replay yet. `3b2c12df_g4` (jackpot, 500 turns) stands out for future review — longest-lived
non-r1000 loss in the set, worth a closer look for a late, close core death.

## Top-5 flip candidates (by margin, closest first)

1. **`3b2c12df-d6b2-4ac0-a788-6edb8d4a3876_g3`** (atoll vs Oresund Overflow, v56 og) — delivered was
   **exactly tied** (0 Δ); lost purely on harvesters alive (−4). Lever (a): **1 single harvester**
   built at r960 (2195 Ti bank, 48 affordable) flips it outright via tiebreak #1 before harvesters
   even matter. Cheapest flip in the whole set.
2. **`c106d3d2-c401-4769-b958-b4a4cb7997ad_g3`** (hive vs Orizon, v56 og) — delivered Δ −260. Flips
   two ways: lever (a) k=3 harvesters (2700 Ti bank, 54 affordable), or lever (b) splicing 3 of 4
   reachable enemy harvesters (400 Ti double-swing available vs 260 needed). Only game in the set
   where the splice lever alone suffices.
3. **`ad08eb70-4926-4d8a-b459-b48ace96f56c_g2`** (jackpot vs OopsGotYourElo, v62 CL) — delivered Δ
   −710, our newest bot version in the set. Lever (a) k=8 harvesters (4720 Ti bank, 75 affordable) —
   cheap margin, current-line-relevant.
4. **`c00e6c30-1604-4f79-9389-99919c37c16f_g3`** (jackpot vs Lunds Stallions, v54 og) — delivered Δ
   −1610. Lever (a) k=17 (9067 Ti bank, 112 affordable).
5. **`57d5f794-d52f-499c-a04e-3b5d0f60a351_g1`** (antler vs Memtrace, v61 CL) — delivered Δ −2300.
   Lever (a) k=23 (4652 Ti bank, 74 affordable); current-line.

## Files

- `SCRATCH/findings/thread4_analysis.py` — the analysis script (reusable, stdlib + replay_lib only).
- `SCRATCH/findings/thread4_results.json` — full per-game computed fields for all 21 games.
