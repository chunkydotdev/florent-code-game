## VALIDATION of the HP decode (the two's-complement trap)

updateHp deltas seen across the 1,445 joined replays: **523,802 negative** (damage) and **502,504 positive** (heals). Both signs present, so the varint sign handling is live rather than silently collapsing to one sign -- the failure mode that produced 'exactly 0 core damage across 11,895 insertions' in the throw census.

## 1+2. PLACEBO AND DISCONTINUITY -- P(our builder moves) by d2 to our own core

r0-150, our team only. `core DAMAGED` = our core HP < max at the start of the round. The hypothesised code path fires ONLY when the core is damaged, so a real effect must appear in the DAMAGED column and be absent in the FULL column, with a STEP at d2=25.

| d2 to our core | n (dmg) | P(move) dmg | n (full) | P(move) full | dmg - full |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 30,997 | 0.069 | 31,614 | 0.669 | -0.601 |
| 2 | 40,613 | 0.117 | 49,215 | 0.623 | -0.507 |
| 4 | 30,816 | 0.139 | 37,893 | 0.690 | -0.551 |
| 5 | 41,386 | 0.270 | 70,148 | 0.726 | -0.456 |
| 8 | 7,658 | 0.633 | 25,410 | 0.766 | -0.133 |
| 9 | 5,932 | 0.640 | 20,004 | 0.651 | -0.011 |
| 10 | 10,111 | 0.641 | 34,715 | 0.691 | -0.050 |
| 13 | 7,209 | 0.694 | 28,786 | 0.682 | +0.011 |
| 16 | 3,024 | 0.524 | 12,397 | 0.526 | -0.002 |
| 17 | 5,802 | 0.602 | 21,812 | 0.642 | -0.040 |
| 18 | 2,321 | 0.697 | 8,725 | 0.718 | -0.021 |
| 20 | 5,453 | 0.628 | 20,020 | 0.682 | -0.054 |
| 25   <-- **d2=25 boundary** | 6,000 | 0.577 | 21,678 | 0.633 | -0.055 |
| 26 | 7,098 | 0.417 | 18,481 | 0.551 | -0.134 |
| 29 | 4,793 | 0.625 | 15,768 | 0.622 | +0.004 |
| 32 | 1,770 | 0.630 | 4,640 | 0.713 | -0.083 |
| 34 | 2,879 | 0.635 | 10,533 | 0.661 | -0.026 |
| 36 | 1,997 | 0.516 | 6,372 | 0.519 | -0.003 |
| 37 | 5,140 | 0.428 | 15,106 | 0.490 | -0.063 |
| 40 | 3,923 | 0.597 | 12,328 | 0.627 | -0.030 |
| 41 | 2,936 | 0.638 | 8,668 | 0.726 | -0.087 |
| 45 | 1,999 | 0.756 | 6,731 | 0.727 | +0.029 |
| 49 | 761 | 0.507 | 3,120 | 0.473 | +0.034 |
| 50 | 2,399 | 0.643 | 9,580 | 0.605 | +0.038 |
| 52 | 2,405 | 0.664 | 6,913 | 0.676 | -0.012 |
| 53 | 1,682 | 0.710 | 5,732 | 0.637 | +0.073 |
| 58 | 1,107 | 0.736 | 3,731 | 0.687 | +0.049 |
| 101-200 | 14,570 | 0.420 | 38,928 | 0.509 | -0.089 |
| 201+ | 19,381 | 0.203 | 34,734 | 0.250 | -0.047 |
| 61-100 | 14,338 | 0.679 | 50,181 | 0.628 | +0.051 |

**The step test -- two competing thresholds.** The hypothesis names `dsq 25`. But `can_heal()` enforces ORTHOGONAL ADJACENCY to a core footprint tile, and for a 2x2 core anchored at (x,y) that set is exactly d2 in {1,2,4,5} from the anchor -- d2=8 is the diagonal corner, one tile further out and adjacent to nothing. Both thresholds are tested here, against the opponent's own builders around the opponent's own core as a control.

| window | US: n, P(move) dmg [95% CI] | US: P(move) full | US suppression | THEM: P(move) dmg | THEM: P(move) full | THEM suppression |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| d2 in {1,2,4,5} -- ORTHOGONALLY ADJACENT to the core footprint | 143,812, **0.155** [0.153,0.157] | 0.683 | **-0.527** | 0.282 | 0.434 | -0.152 |
| d2 6-20 -- near but NOT adjacent | 47,510, **0.637** [0.632,0.641] | 0.678 | **-0.041** | 0.627 | 0.608 | +0.020 |
| d2 21-25 -- inside the `dsq 25` gate | 6,000, **0.577** [0.565,0.590] | 0.633 | **-0.055** | 0.522 | 0.558 | -0.035 |
| d2 26-30 -- just OUTSIDE the `dsq 25` gate | 11,891, **0.501** [0.492,0.510] | 0.584 | **-0.082** | 0.560 | 0.511 | +0.049 |
| d2 31-60 | 28,998, **0.601** [0.596,0.607] | 0.621 | **-0.020** | 0.605 | 0.575 | +0.031 |

## 3. PERSISTENCE -- P(move) vs rounds since our core last lost HP

`SLOT_UNDER` is a 50-round latch. If it is what suppresses movement, P(move) for near-home builders should be flat below 50 rounds of age and recover above it.

| rounds since our core last took damage | near (d2<=25) n | P(move) | far (d2>25) n | P(move) |
| --- | ---: | ---: | ---: | ---: |
| 1-5 | 206,534 | 0.318 | 87,187 | 0.485 |
| 5-10 | 20,752 | 0.569 | 8,855 | 0.542 |
| 10-25 | 29,701 | 0.591 | 18,094 | 0.585 |
| 25-50 | 24,739 | 0.628 | 19,618 | 0.591 |
| 50-75   <-- **latch expiry** | 14,205 | 0.665 | 11,579 | 0.582 |
| 75-150 | 11,837 | 0.682 | 10,385 | 0.611 |
| never | 271,971 | 0.688 | 185,006 | 0.534 |

## 4. DOSE-RESPONSE -- enemy fire at our core vs our builders' dispersal

Exposure: the opponent's turret shots in r0-150 (from the fine-band decoder, cross-validated against `build_agg.tsv` `metric=='shot'`; `econ.tsv.shots` is zero in every row and is not used). Response: the share of our builder-bot round-samples standing OUTSIDE d2=25 of our own core. One point per opponent, N stated.

| opponent | games | their shots/game r0-150 | our core damaged, share of rounds | our builders outside d2=25 | our core-kill share |
| --- | ---: | ---: | ---: | ---: | ---: |
| Lunds Stallions | 130 | 102 | 0.390 | 0.302 | 17.7% |
| Kings College Munich | 115 | 74 | 0.222 | 0.408 | 10.4% |
| Team 48 | 110 | 109 | 0.447 | 0.468 | 61.8% |
| Powerpuff Girls | 105 | 51 | 0.155 | 0.506 | 10.5% |
| Ouroboros | 105 | 99 | 0.088 | 0.472 | 4.8% |
| Leviathan | 95 | 68 | 0.255 | 0.590 | 30.5% |
| OopsGotYourElo | 95 | 45 | 0.083 | 0.575 | 15.8% |
| Memtrace | 85 | 42 | 0.129 | 0.400 | 36.5% |
| CtrlAltDefeat | 85 | 68 | 0.245 | 0.417 | 14.1% |
| Askar City | 75 | 36 | 0.238 | 0.459 | 65.3% |
| Banminary | 70 | 48 | 0.327 | 0.504 | 82.9% |
| 0033 | 45 | 46 | 0.376 | 0.424 | 51.1% |
| opensverige - plan B | 45 | 44 | 0.327 | 0.418 | 31.1% |
| I Stone | 40 | 48 | 0.251 | 0.375 | 42.5% |
| The Bisons | 35 | 64 | 0.564 | 0.242 | 74.3% |
| gsxWins | 30 | 67 | 0.569 | 0.376 | 70.0% |
| Orizon | 25 | 103 | 0.174 | 0.434 | 28.0% |
| farming_200s | 20 | 67 | 0.496 | 0.345 | 70.0% |
| Focalground | 20 | 2 | 0.054 | 0.550 | 20.0% |
| Hugging Farce | 15 | 34 | 0.243 | 0.529 | 33.3% |
| diverge | 15 | 28 | 0.679 | 0.553 | 53.3% |
| Coreflood | 10 | 32 | 0.140 | 0.436 | 20.0% |
| kladde chatte tville (och oss) | 10 | 27 | 0.280 | 0.428 | 0.0% |
| Powered by SmartFridge | 10 | 136 | 0.409 | 0.439 | 40.0% |
| Landers | 10 | 63 | 0.546 | 0.406 | 50.0% |
| arsonist duck | 10 | 53 | 0.631 | 0.324 | 10.0% |

Across the 26 opponents with >=10 archived games:
- corr(their shots/game, our builders outside d2=25) = **-0.280** -- the mechanism predicts a clear NEGATIVE.
- corr(share of rounds our core is damaged, our builders outside d2=25) = **-0.450** -- this is the closer proxy, since the heal is gated on damage, not on fire.
- corr(our builders outside d2=25, our core-kill share) = **-0.171** -- if dispersal is what buys kills this must be clearly positive.
- corr(their shots/game, our core-kill share) = **+0.034**.

**Within-opponent, per game** (the same relationship with opponent identity removed -- rank correlation of our dispersal against our core-kill outcome, computed inside each opponent and pooled):

| opponent | games | mean dispersal in kill games | in non-kill games | diff |
| --- | ---: | ---: | ---: | ---: |
| Lunds Stallions | 130 | 0.360 | 0.257 | +0.102 |
| Kings College Munich | 115 | 0.351 | 0.385 | -0.033 |
| Team 48 | 110 | 0.347 | 0.443 | -0.096 |
| Powerpuff Girls | 105 | 0.601 | 0.462 | +0.139 |
| Ouroboros | 105 | 0.217 | 0.402 | -0.184 |
| Leviathan | 95 | 0.486 | 0.523 | -0.037 |
| OopsGotYourElo | 95 | 0.560 | 0.547 | +0.013 |
| Memtrace | 85 | 0.336 | 0.351 | -0.015 |
| CtrlAltDefeat | 85 | 0.340 | 0.394 | -0.054 |
| Askar City | 75 | 0.402 | 0.491 | -0.089 |
| Banminary | 70 | 0.411 | 0.386 | +0.025 |
| 0033 | 45 | 0.440 | 0.390 | +0.050 |
| opensverige - plan B | 45 | 0.438 | 0.396 | +0.043 |
| I Stone | 40 | 0.411 | 0.385 | +0.026 |
| The Bisons | 35 | 0.273 | 0.278 | -0.005 |
| gsxWins | 30 | 0.373 | 0.278 | +0.095 |
| Orizon | 25 | 0.356 | 0.333 | +0.023 |
| farming_200s | 20 | 0.351 | 0.517 | -0.166 |
| Focalground | 20 | 0.553 | 0.554 | -0.001 |
| Hugging Farce | 15 | 0.353 | 0.442 | -0.089 |
| diverge | 15 | 0.453 | 0.582 | -0.129 |

9 of 21 opponents show higher dispersal in the games we land a core kill; mean difference -0.018.
