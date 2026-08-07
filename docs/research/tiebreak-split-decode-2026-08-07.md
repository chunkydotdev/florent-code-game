# Tiebreak-split decode — piece T (delivery continuity) vs control, 120 games

**Research arm, 2026-08-07 (night).** Measurement and attribution only — the
keep/refute verdict belongs to the builder session.

**Corpus.** 60 `_v80e6d_tb` (md5 `005db756`) vs `opp_v69` (md5 `562b01e9`) +
60 `_v79e6c` (md5 `8aaa91e6`) vs the same `opp_v69`. Replays and
`results.json` from the builder's 23:4x instrument legs. `opp_v69` carries an
unseeded spawn salt, so **every comparison below is pooled** — no game in one
leg is paired with a game in the other.

**Topline given, not re-litigated:** tb 26/60, control 31/60; r1000 games tb 28
(14 taken), control 25 (15 taken). This document decomposes it.

---

## FINDINGS

### (a) DELIVERED-FLOOR LIFT — **NO. The floor got worse; the ceiling got better.**

Our delivered titanium in r1000 games:

| | n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|---|
| tb | 28 | **0** | 3760 | 7395 | 13360 | 21350 | 8393 |
| control | 25 | **50** | 4930 | 6430 | 9640 | 21050 | 7688 |

Mann-Whitney on the two distributions: **U=352.0, z=0.04, p=0.97** — no
distributional shift at all.

Low tail (the pre-registered "floor"), count of r1000 games by our delivered:

| delivered | 0–500 | 500–2000 | 2000–5000 | 5000–10000 | 10000+ |
|---|---|---|---|---|---|
| tb | 3 | 3 | 5 | 7 | **10** |
| control | 1 | 1 | 7 | 10 | 6 |

**Piece T widened the distribution in both directions.** Games under 2000 Ti:
6 (tb) vs 2 (control). Games over 10000 Ti: 10 vs 6. The floor metric the
thesis named (min, p25, low tail) moved the *wrong* way.

**Map effects are real and the r1000 map mix is unbalanced.** Only 11 of 15
maps have an r1000 game in *both* legs (tb-only: fjordgate, hive, saga;
control-only: drumlin). Restricted to the 11 common maps: tb n=23 med 7530
min 40 mean 9428 | control n=24 med 6420 min 50 mean 7436. Per-map median our
delivered is higher for tb on **7 of 11** maps, with big swings both ways
(snowflake +12610, antler +5385, moonrise +3940 / eider −7000, lighthouse
−6570, meander −5000, jackpot −4865).

**The conditional cut is the informative one.** Binning r1000 games on our
relay count at r300 (a covariate T.1 cannot change — destroy+rebuild is
same-tile, so relay count is invariant under T.1):

| relays@r300 | leg | n | won | our delivered med | min | wired-frac r999 med |
|---|---|---|---|---|---|---|
| ≥30 | tb | 19 | 13 | **10020** | 3210 | **0.632** |
| ≥30 | control | 19 | 14 | 7480 | 2860 | 0.446 |
| <30 | tb | 9 | 1 | **930** | 0 | 0.133 |
| <30 | control | 6 | 1 | 4635 | 50 | 0.394 |

Piece T lifts delivery **only where a chain already exists** (+34% median in
the healthy bin). In the broken bin — the exact grind shape the thesis
targeted — tb is worse and more numerous.

Delivery rate r300→r1000 (stacks per 100 rounds), r1000 games: tb ours med
74.9 mean 92.4 (theirs med 69.0) | control ours med 71.3 mean 84.1 (theirs med
97.9).

**Our own terminal delivery freeze fired 8/60 in the tb leg vs 4/60 in
control** (test: no delivery for ≥100 rounds to game end with ≥5 of our relays
alive). Four of the eight are r1000 games delivering 40 / 140 / 910 / 1140 Ti.
The defect piece T was written to fix appears *more* often with piece T on.
Small n, not significant, direction adverse.

### (b) TIEBREAK-#1 MARGINS — **margins tighten in both directions; the share does not move.**

Which tiebreak step decided each r1000 game:

| leg | tiebreak #1 (delivered) | #2 (harvesters alive) | #3 (stored) |
|---|---|---|---|
| tb | 27 of 28 (won 14, lost 13) | **0** | 1 (lost) |
| control | 24 of 25 (won 14, lost 10) | **0** | 1 (won) |

**Tiebreak #2 (harvesters alive) never decided a single game in 120.** It was
*reached* exactly twice — the two games where delivered titanium tied dead
level — and tied there too (3–3 harvesters in `archipelago_s2_B`, 2–2 in
`antler_s2_A`), so both fell through to step 3, stored titanium.

Margin (ours − theirs delivered), r1000 games:

| | n | min | p25 | median | p75 | max | mean |
|---|---|---|---|---|---|---|---|
| tb | 28 | −19700 | −2840 | +180 | +3440 | +12330 | −986 |
| control | 25 | −23340 | −6970 | +1490 | +2770 | +6690 | −1586 |

Mann-Whitney on margins: **U=354.5, z=0.08, p=0.94.**

Split by result:
- **losses**: tb med −3415 mean −6602 | control med −8155 mean −9135 → tb loses tiebreak #1 by **less**.
- **wins**: tb med +3140 mean +4630 | control med +2750 mean +3446 → tb wins by **more**.

Yet the share is flat: **tiebreak-#1 wins 14/27 = 51.9% (Wilson 34.0–69.3) for
tb vs 14/24 = 58.3% (38.8–75.5) for control.** Wilson intervals for every cut:

| leg | all | r1000 | tiebreak #1 | core_destroyed |
|---|---|---|---|---|
| tb | 26/60 43.3% (31.6, 55.9) | 14/28 50.0% (32.6, 67.4) | 14/27 51.9% (34.0, 69.3) | 12/32 37.5% (22.9, 54.7) |
| control | 31/60 51.7% (39.3, 63.8) | 15/25 60.0% (40.7, 76.6) | 14/24 58.3% (38.8, 75.5) | 16/35 45.7% (30.5, 61.8) |

Knife-edge games (|margin| ≤ 2000 Ti): **tb 8/28, of which it won 4 and lost
4. Control 4/25, of which it won all 4 and lost 0.** Piece T manufactured more
coin-flip tiebreaks and split them.

### (c) V69 FREEZE LOCALLY — **fires rarely (7/120), and when it fires we win 7/7.**

Terminal-freeze test on their side (no delivery for ≥100 rounds to game end,
≥5 of their relays alive): **1/60 in the tb leg, 6/60 in the control leg.**
Same as the any-100-round-stall count in both legs.

Their directed-wired fraction at r999, r1000 games only: tb-leg med 0.651
(min 0.087, mean 0.60) | control-leg med 0.470 (min 0.035, mean 0.50). Ours at
r999: tb med 0.567 | control med 0.435. **v69 is not chain-collapsed locally —
in the control leg its wiredness is comparable to ours, and in the tb leg it is
better.** The ladder-scale freeze signature (95 conveyors, 1 wired) does not
reproduce at rate in this corpus.

The seven freeze games — **we won all seven**:

| leg | game | turns | their last delivery | their relays | their wired | their Ti | our Ti |
|---|---|---|---|---|---|---|---|
| tb | jackpot_s1_A | 323 | r203 | 26 | 0/26 | 710 | 1570 |
| control | drumlin_s1_A | 289 | r115 | 8 | 5/8 | 270 | 2100 |
| control | fjordgate_s2_A | 602 | r17 | 13 | 0/13 | 30 | 1950 |
| control | heart_s1_A | 1000 | r241 | 12 | 5/12 | 660 | 6410 |
| control | jackpot_s1_B | 1000 | r310 | 57 | 2/57 | 1210 | 7210 |
| control | jackpot_s2_B | 1000 | r152 | 38 | 2/38 | 520 | 2860 |
| control | saga_s1_B | 717 | r146 | 34 | 7/34 | 330 | 390 |

**Attribution: the 6-vs-1 incidence split between legs is opponent
nondeterminism, and it is worth up to five wins — the entire topline gap.**
Excluding freeze games: tb 25/59 = 42.4%, control 25/54 = 46.3%; the gap
narrows from 8.4pp to 3.9pp. Where the tiebreak was won in this corpus it was
usually won by *their* defect, not by our floor.

### (d) HIGH-WATER BOTH SIDES — **the pathology reproduces on our side; T.2 did not mask it.**

Full harvester wipes (count to 0 after peaking ≥2) are rare: **2/60 ours in the
tb leg, 0/60 ours in control, 0/60 theirs in either.** In both tb wipes: 0
harvesters rebuilt afterward, 2–3 relays still placed after the wipe, 122 and
658 rounds of game remaining.

The sensitive test — *harvester famine*: live harvesters fall below 2 after
r300 having peaked ≥2. Nine episodes total:

| leg | side | game | famine from | duration | rebuilds after | relay Δ after | delivered after |
|---|---|---|---|---|---|---|---|
| tb | ours | drumlin_s1_B | r301 | ≥276 | **0** | +1 | **0** |
| tb | ours | eider_s1_B | r301 | ≥699 | **0** | +4 | 4700 |
| tb | ours | hive_s2_A | r301 | ≥699 | **0** | +0 | **0** |
| tb | ours | moonrise_s2_B | r322 | ≥678 | **0** | −4 | 2230 |
| tb | theirs | fjordgate_s1_A | r301 | ≥578 | **0** | −1 | **0** |
| control | ours | lighthouse_s2_B | r496 | ≥22 | **0** | −1 | **0** |
| control | ours | moonrise_s1_A | r301 | ≥106 | **0** | +0 | 260 |
| control | ours | moonrise_s1_B | r301 | ≥699 | **0** | −3 | 120 |
| control | theirs | hive_s2_B | r534 | ≥71 | **0** | +0 | **0** |

**Zero harvester rebuilds in all nine episodes, both sides, both legs.** In
two of the four tb episodes our delivery sat at exactly zero for 276–699
rounds while the relay count held or rose — paving continued as if the farm
existed. The ancestral high-water signature is live in our line, and piece T.2
does not mask it in the tb leg.

### (e) MECHANISM FIRING

**T.1 — FIRES HARD, clean differential, and demonstrably works on its own metric.**

| | tb leg | control leg |
|---|---|---|
| voluntary conveyor destroys (removal at full HP) | **245** | **0** |
| destroy → same-tile rebuild with changed facing | **245** | **0** |
| games with ≥1 T.1 event | **41/60** | 0/60 |
| per-game (60 games) | med 2, p75 5, max 20 | 0 |
| timing | 160 before r300, 85 after | — |
| any same-tile relay rebuild (incl. enemy-cleared relays) | 302 | 39 |

Mechanism effect on the metric it targets — our directed-wired relays at r999,
r1000 games, pooled: **tb 1010/1742 = 58.0%** vs **control 752/1876 = 40.1%**,
and tb does it with *fewer* conveyors (62/game vs 75/game). Per-game medians:
tb 0.567 vs control 0.435 (Mann-Whitney z=1.60, p=0.11). At r300 already: tb
0.622 vs control 0.500.

**T.1's structural blind spot, quantified.** Classifying every one of our
non-delivering relays at r999 in r1000 games by the one-step verdict T.1
itself uses:

| unwired class | tb | control | T.1 behaviour |
|---|---|---|---|
| **chained** (output = friendly relay not aimed back) | **487 (67%)** | **722 (64%)** | verdict `"live"` → **never touched** |
| stray (output = empty tile) | 129 (18%) | 135 (12%) | re-aimed only if a live neighbour exists |
| orphan (edge/wall/enemy/non-accepting) | 116 (16%) | 267 (24%) | acted on |
| of which in a ≥3-conveyor cycle | 6 | 10 | passes every local test forever |

Two thirds of the observed unwiredness is a locally-well-formed chain that is
globally rooted nowhere. `_t_facing_verdict` answers with a one-step downstream
test by design; a chain of correctly-linked conveyors that never reaches the
core returns `"live"` at every tile. So T.1 can address at most ~1/3 of the
defect it was aimed at, and it did — the 18pp wiredness lift is exactly the
orphan+stray share being cleaned up.

**T.2 — DID NOT ENGAGE.**

| | tb | control |
|---|---|---|
| harvester builds after r300 | **48** | 61 |
| per game reaching r300 | 1.23 (39 games) | 1.52 (40 games) |
| games with ≥1 post-r300 build | 10 | 17 |
| ...occurring while our live harvesters were <2 the prior round | **0** | 1 |
| rebuilds during the 7 famine episodes on our side | **0** | **0** |

Post-r300 harvester building is *lower* with T.2 on, and no post-r300 build in
either leg is attributable to a harvester famine. T.2 produced no observable
firing. **UNCERTAIN which sub-gate binds** — the `late_sustain` flag only
un-gates the branch; the build still needs `can_build_harvester` on a tile
orthogonally adjacent to the acting builder, plus `SLOT_UNDER == 0`, plus
`resources ≥ harvester_cost + SIEGE_HEAL_RESERVE_TI`. The vision-local count
`_t_visible_harvesters` is a *lower* bound on the global count, so the gate
should open more readily than my global test, not less — which points the
finger at the adjacency/siege/bank conditions rather than the floor test.

**T.3 — FIRES.** Our chain-heal ticks by target, pooled over 60 games:

| leg | harvester | splitter | conveyor | harvester share |
|---|---|---|---|---|
| tb | 2018 | 0 | 3306 | **37.9%** |
| control | 1352 | 0 | 5070 | 21.1% |

The heal choice moved toward the source as designed. Note **splitters are never
built by either side in 120 games** (final splitter count 0 in all 120), so the
`T_CHAIN_RANK` splitter tier is dead code.

### (f) SURPRISES

1. **The topline gap is not in the tiebreak.** Tiebreak-#1 wins are exactly
   **14 vs 14**. The 26-vs-31 deficit sits entirely in decisive games:
   core_destroyed 12/32 (37.5%) tb vs 16/35 (45.7%) control. The instrument's
   own target metric moved by zero games.
2. **Tiebreak #2 (harvesters alive) decided nothing in 120 games**, and step 3
   decided two. The pre-registered "step 1 is everything" premise holds
   completely (51 of 53 r1000 games).
3. **The opponent's defect rate is a bigger lever than the treatment.** Their
   freeze fired 6× in one leg and 1× in the other, decisive 7/7 — larger than
   any measured effect of piece T.
4. **Our own terminal freeze doubled with T on** (8/60 vs 4/60). Adverse
   direction on the very failure mode T targets; n too small to call.
5. **More core pressure in the tb leg**: our core heal ticks 29929 (tb) vs
   22866 (control); our core lost 20 vs 19 games, theirs 12 vs 16.
6. **Zero exception prints from either bot in all 120 games** — the 68/120 v69
   exception-print rate observed in the C1 value leg does not reproduce in this
   corpus. UNCERTAIN whether that is a corpus difference or a detection
   difference (this parser counts `botOutput` payloads matching
   Traceback/Error/EXC).
7. Our final *stored* titanium in r1000 games: tb med 3194 vs theirs 2858;
   control med 3477 vs theirs 4813. Both legs bank thousands while losing
   tiebreak #1 by thousands.

---

## ATTRIBUTION SYNTHESIS (not a verdict)

Ranked by how much of the data each class explains:

**1. FLOOR-DOES-NOT-LIFT (primary, for the T.1 arm).** The mechanism engaged
hard (245 events, 41/60 games) and moved its own metric decisively (directed
wiredness 58.0% vs 40.1% pooled; +18pp), but the pre-registered floor did not
follow: min 0 vs 50, p25 3760 vs 4930, games under 2000 Ti 6 vs 2, our own
freeze rate 8/60 vs 4/60, Mann-Whitney p=0.97 on delivered and p=0.94 on
margin. What lifted was the **ceiling** (median +15% pooled, +17% map-matched,
+34% in the healthy-chain bin; 10 vs 6 games over 10000 Ti). The thesis is
"repair continuity → win grinds at tiebreak #1"; continuity was repaired,
grinds were not won (14 vs 14). The structural reason is measured, not
inferred: **67% of the unwiredness that remains is in T.1's `"live"` blind
spot** — a one-step verdict cannot see a locally-valid chain rooted nowhere.

**2. INSTRUMENT-DID-NOT-ENGAGE (for the T.2 arm specifically).** Zero
attributable firings in 60 games; post-r300 harvester builds *fell* (48 vs 61);
0 rebuilds across 7 of our famine episodes. The high-water hypothesis (d) was
therefore never tested by this battery — it remains open, and the pathology it
describes is confirmed present on our side (delivery pinned at 0 for 276–699
rounds while paving continued).

**3. CONFOUNDED (bounds the topline, not the mechanism).** The 5-game topline
gap must not be read as piece T's cost. Their terminal freeze fired 6× vs 1×
between legs and was decisive 7/7; removing those games moves tb 25/59 (42.4%)
vs control 25/54 (46.3%), i.e. 8.4pp → 3.9pp of a gap whose Wilson intervals
overlap heavily at every cut. On top of that, only 11 of 15 maps have an r1000
game in both legs, and per-map median deltas swing ±12610 Ti.

**Not supported: FLOOR-LIFTS-BUT-DECIDED-ELSEWHERE.** That class would require
the low tail to improve while games were lost to core destruction. The low tail
got worse (6 vs 2 games under 2000 Ti) even as the median rose, so the vehicle
is not the only problem.

**Mechanism-fire counts, one line:** T.1 **245/245** (destroy → refaced
rebuild) across **41/60** games, 160 pre-r300; T.2 **0** attributable firings
(48 post-r300 harvester builds, none under famine); T.3 fires — harvester share
of chain heals **37.9% vs 21.1%**.

---

## r1000-GAME TABLE

`T1` = T.1 events; `T2` = post-r300 harvester builds; `Wfr` = directed-wired
fraction at r999; `H` = harvesters alive at r999. All 53 r1000 games.

### tb leg (`_v80e6d_tb` 005db756 vs opp_v69), 28 games, 14 taken

| map | sd | seat | our dlv | their dlv | margin | res | cond | T1 | T2 | our Wfr | their Wfr | our H | their H |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| antler | 1 | A | 10020 | 2440 | +7580 | W | ti_coll | 13 | 1 | 0.51 | 0.09 | 6 | 3 |
| archipelago | 1 | B | 8260 | 6610 | +1650 | W | ti_coll | 0 | 1 | 0.94 | 0.91 | 4 | 3 |
| archipelago | 2 | B | 7410 | 7410 | 0 | L | **ti_stored** | 0 | 0 | 1.00 | 1.00 | 3 | 3 |
| atoll | 1 | A | 7530 | 6370 | +1160 | W | ti_coll | 12 | 0 | 0.75 | 0.92 | 3 | 3 |
| atoll | 1 | B | 7380 | 4840 | +2540 | W | ti_coll | 7 | 0 | 0.81 | 0.76 | 4 | 3 |
| eider | 1 | A | 21270 | 30070 | −8800 | L | ti_coll | 15 | 2 | 0.57 | 0.79 | 11 | 16 |
| eider | 1 | B | 5480 | 24620 | −19140 | L | ti_coll | 12 | 0 | 0.40 | 0.38 | 1 | 18 |
| eider | 2 | A | 4900 | 24600 | −19700 | L | ti_coll | 18 | 0 | 0.42 | 0.60 | 2 | 14 |
| eider | 2 | B | 13360 | 25770 | −12410 | L | ti_coll | 9 | 4 | 0.31 | 0.48 | 6 | 21 |
| fjordgate | 1 | B | 0 | 9120 | −9120 | L | ti_coll | 0 | 0 | 0.00 | 0.69 | 0 | 5 |
| fjordgate | 2 | A | 9140 | 0 | +9140 | W | ti_coll | 11 | 0 | 0.86 | 0.00 | 4 | 0 |
| heart | 1 | A | 13700 | 5500 | +8200 | W | ti_coll | 5 | 8 | 0.83 | 0.41 | 12 | 10 |
| heart | 2 | B | 13170 | 6770 | +6400 | W | ti_coll | 5 | 0 | 0.71 | 0.78 | 10 | 8 |
| hive | 1 | B | 4880 | 2480 | +2400 | W | ti_coll | 3 | 2 | 0.28 | 0.78 | 6 | 2 |
| hive | 2 | A | 930 | 4920 | −3990 | L | ti_coll | 0 | 0 | 0.00 | 0.55 | 1 | 3 |
| jackpot | 1 | B | 1140 | 2950 | −1810 | L | ti_coll | 0 | 0 | 0.13 | 0.25 | 3 | 3 |
| lighthouse | 1 | A | 910 | 9910 | −9000 | L | ti_coll | 5 | 0 | 0.15 | 0.37 | 2 | 6 |
| meander | 1 | A | 140 | 2400 | −2260 | L | ti_coll | 0 | 0 | 0.06 | 1.00 | 3 | 1 |
| meander | 2 | B | 40 | 2440 | −2400 | L | ti_coll | 0 | 0 | 0.10 | 1.00 | 2 | 1 |
| moonrise | 1 | A | 5640 | 8480 | −2840 | L | ti_coll | 5 | 0 | 0.86 | 0.75 | 2 | 4 |
| moonrise | 1 | B | 4890 | 4900 | −10 | L | ti_coll | 0 | 0 | 0.59 | 0.77 | 2 | 2 |
| moonrise | 2 | B | 3760 | 4710 | −950 | L | ti_coll | 6 | 0 | 0.65 | 0.40 | 0 | 4 |
| nordkap | 1 | A | 21350 | 9020 | +12330 | W | ti_coll | 14 | 0 | 0.75 | 0.47 | 10 | 9 |
| nordkap | 1 | B | 11820 | 8380 | +3440 | W | ti_coll | 20 | 5 | 0.56 | 0.65 | 6 | 7 |
| nordkap | 2 | A | 17810 | 14970 | +2840 | W | ti_coll | 9 | 7 | 0.52 | 0.68 | 11 | 10 |
| nordkap | 2 | B | 17830 | 11620 | +6210 | W | ti_coll | 7 | 14 | 0.85 | 0.51 | 10 | 9 |
| saga | 1 | A | 3210 | 2640 | +570 | W | ti_coll | 4 | 0 | 0.48 | 0.53 | 4 | 3 |
| snowflake | 2 | A | 19040 | 18680 | +360 | W | ti_coll | 16 | 4 | 0.63 | 0.44 | 13 | 15 |

`archipelago_s2_B` is the tb leg's tiebreak-#3 game: delivered dead level at
7410 each, harvesters 3–3, wiredness 1.00 both sides, lost on stored titanium
20 vs 29.

### control leg (`_v79e6c` 8aaa91e6 vs opp_v69), 25 games, 15 taken

| map | sd | seat | our dlv | their dlv | margin | res | cond | T1 | T2 | our Wfr | their Wfr | our H | their H |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| antler | 1 | A | 4340 | 9400 | −5060 | L | ti_coll | 0 | 0 | 0.37 | 0.56 | 2 | 6 |
| antler | 2 | A | 4930 | 4930 | 0 | W | **ti_stored** | 0 | 0 | 0.40 | 0.47 | 2 | 2 |
| archipelago | 2 | A | 6450 | 16220 | −9770 | L | ti_coll | 0 | 10 | 0.34 | 0.60 | 14 | 21 |
| atoll | 1 | A | 4970 | 7310 | −2340 | L | ti_coll | 0 | 0 | 0.53 | 0.88 | 3 | 4 |
| atoll | 1 | B | 10270 | 3980 | +6290 | W | ti_coll | 0 | 1 | 0.42 | 0.55 | 6 | 2 |
| atoll | 2 | A | 4970 | 11940 | −6970 | L | ti_coll | 0 | 0 | 0.71 | 0.84 | 3 | 4 |
| atoll | 2 | B | 9640 | 6890 | +2750 | W | ti_coll | 0 | 0 | 0.56 | 0.73 | 4 | 3 |
| drumlin | 1 | B | 13730 | 10960 | +2770 | W | ti_coll | 0 | 2 | 0.34 | 0.32 | 7 | 15 |
| eider | 1 | A | 21050 | 19040 | +2010 | W | ti_coll | 0 | 1 | 0.63 | 0.47 | 14 | 10 |
| eider | 1 | B | 7650 | 30990 | −23340 | L | ti_coll | 0 | 9 | 0.42 | 0.75 | 4 | 17 |
| eider | 2 | A | 16420 | 15660 | +760 | W | ti_coll | 0 | 0 | 0.40 | 0.35 | 10 | 16 |
| heart | 1 | A | 6410 | 660 | +5750 | W | ti_coll | 0 | 4 | 0.53 | 0.42 | 10 | 5 |
| heart | 2 | B | 13820 | 8240 | +5580 | W | ti_coll | 0 | 6 | 0.67 | 0.64 | 14 | 7 |
| jackpot | 1 | A | 4800 | 2830 | +1970 | W | ti_coll | 0 | 0 | 0.06 | 0.11 | 3 | 3 |
| jackpot | 1 | B | 7210 | 1210 | +6000 | W | ti_coll | 0 | 0 | 0.19 | 0.04 | 3 | 5 |
| jackpot | 2 | A | 9570 | 4940 | +4630 | W | ti_coll | 0 | 0 | 0.45 | 0.45 | 5 | 6 |
| jackpot | 2 | B | 2860 | 520 | +2340 | W | ti_coll | 0 | 0 | 0.04 | 0.05 | 2 | 3 |
| lighthouse | 1 | A | 7480 | 4820 | +2660 | W | ti_coll | 0 | 15 | 0.43 | 0.57 | 3 | 3 |
| meander | 1 | A | 5100 | 13130 | −8030 | L | ti_coll | 0 | 1 | 0.45 | 0.31 | 5 | 9 |
| meander | 2 | B | 5080 | 11650 | −6570 | L | ti_coll | 0 | 0 | 0.25 | 0.38 | 3 | 7 |
| moonrise | 1 | B | 950 | 9510 | −8560 | L | ti_coll | 0 | 0 | 0.44 | 0.56 | 1 | 4 |
| moonrise | 2 | A | 3900 | 2410 | +1490 | W | ti_coll | 0 | 1 | 0.66 | 0.35 | 3 | 3 |
| moonrise | 2 | B | 50 | 12480 | −12430 | L | ti_coll | 0 | 0 | 0.50 | 0.55 | 0 | 8 |
| nordkap | 1 | B | 14120 | 7430 | +6690 | W | ti_coll | 0 | 1 | 0.56 | 0.36 | 6 | 9 |
| snowflake | 2 | B | 6430 | 14710 | −8280 | L | ti_coll | 0 | 3 | 0.39 | 0.26 | 7 | 18 |

`antler_s2_A` is the control leg's tiebreak-#3 game: delivered level at 4930
each, harvesters 2–2, won on stored titanium 107 vs 19.

---

## METHOD NOTES

- **Parser**: `tb_walk.py` in the research scratchpad, derived from
  `v69_walk.py` (same protobuf wire primitives and the same chain-wiredness
  routine documented in `docs/tooling.md`). 120 replays in ~10 s total.
- **Sanity check passed on all 120 games**: `core_deliv * 10 ==
  titaniumCollected` for both teams in every game (the check named in
  tooling.md). Final `titaniumCollected` values also agree with
  `results.json` on every row.
- **placeEntity dedupe by entity id** applied throughout (gunner rotations
  re-emit the same id). No launcher-throw attribution was needed for these
  questions.
- **Team mapping**: replay team 0 = seat A, 1 = seat B; `results.json` `seat`
  names *our* seat, so ours = 0 when seat is A. Both seat orderings are present
  for every map/seed pair.
- **Chain wiredness** is the *directed* metric: a relay counts as wired only if
  a directed path along conveyor facings (splitter = three non-back outputs)
  reaches a core footprint tile. Undirected connectivity is computed too but not
  reported here — it overstates continuity badly.
- **T.1 detection**: a relay removed while at full HP (voluntary `destroy()`;
  a combat kill always shows reduced HP first via `updateHp`) followed by a new
  relay placed on the same tile within 5 rounds. Direction change recorded.
  All 245 tb-leg voluntary destroys matched a same-tile rebuild with a changed
  facing; the control leg had **zero** voluntary relay destroys, so the
  detector has a clean negative control.
- **T.2 detection**: harvester `placeEntity` with round > 300, cross-referenced
  against the team's live harvester count in the preceding round. The gate in
  the bot uses *vision-local* harvester count, which is a lower bound on the
  global count — my global test is therefore conservative in the direction of
  over-counting firings, and it still found zero.
- **T.3 detection**: positive `updateHp` deltas on our own buildings, bucketed
  by entity kind. This counts every heal tick including core self-heal (excluded
  from the chain-heal share).
- **Unwired classification** re-implements `_t_facing_verdict`'s one-step test
  against the final-round board so the categories map exactly onto what the
  shipped mechanism can and cannot see.
- **Freeze test** (both sides): no delivery for ≥100 rounds up to game end with
  ≥5 of that team's relays still alive. An any-window 100-round stall test gave
  identical counts in both legs.
- **Statistics**: Wilson 95% intervals on proportions; Mann-Whitney U with
  normal approximation and tie correction on distributions. Pooled only — the
  opponent is nondeterministic, so no game-to-game pairing across legs is
  valid. n=25–28 per leg on the r1000 subset: every reported difference in win
  share has overlapping intervals, and the two distributional tests on
  delivered/margin are flat (p 0.97, 0.94).
- **Known imbalance**: the r1000 map mix differs between legs (11 of 15 maps
  common). Map-matched figures are reported alongside pooled ones wherever the
  difference matters.
