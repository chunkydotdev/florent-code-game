# RMST₃₀₀ BOARD RESCAN — EVERY LOCAL ARM ON THE CORRECTED ESTIMATOR

**Written 2026-08-16T05:51:11Z (`date -u`, same shell). Read-only: no bot, no match, no queue/programme/results/coordination file touched.**

**Re-scores the 150 arms of `R300-BAR-BOARD-SCAN-2026-08-16.md` on the estimator `PROGRAMME.md:504-508` now mandates** — *"THE OPERATIONAL ESTIMATOR IS ITT RMST₃₀₀ … a plank's RMST₃₀₀ must not RISE vs control"*. The superseded scan was briefed on the `AFTER` orientation (`P(kill-win AND turns>300)`); this document replaces its verdicts.

**Same frozen snapshot (2026-08-16T05:21:27Z), same file discovery, same dedupe, same row filter, same recovered fixture metadata** as the superseded scan — reused, not redone. **The verdict changes below are therefore a pure ESTIMATOR contrast, with the data held byte-identical.** Corefill is live and the tree has since grown by one shard; that shard is deliberately excluded so the comparison stays clean.

---

## 0. HEADLINE

**150 arms scored** (n ≥ 2,000 each; **741,902 clean games**). **59 arms refused**, all for n < 2,000 alone — same 150/59 split as the superseded scan, so no arm entered or left the board.

| | count |
|---|--:|
| **FAIL** — RMST₃₀₀ significantly POSITIVE (kills LATER; the bar bites) | **38** |
| **FASTER** — significantly NEGATIVE (kills EARLIER) | **27** |
| flat — CI straddles zero | 85 |

**⭐ 79 of 150 verdicts CHANGE versus the superseded scan's ITT/`AFTER` column (52.7%). 35 of those are HARD SIGN INVERSIONS — significant one way under the old form and significant the OPPOSITE way under RMST₃₀₀.**

**The four required controls all come out right, on the point estimate, to 2dp:**

| control | expected | **measured RMST₃₀₀** | 95% CI (DEFF 0.98, paired) | verdict |
|---|--:|--:|:--:|:--:|
| `NULL114` | flat (+0.42) | **+0.42** | [-2.43, +3.28] | **flat** |
| `NULL5400` | flat | **+0.27** | [-2.18, +2.72] | **flat** |
| `NEG114` | **+33.27** | **+33.27** | [+30.51, +36.03] | **FAIL** |
| `NEG125` | **+64.81** | **+64.81** | [+60.45, +69.17] | **FAIL** |
| `MAPCODE` | **−60.81** | **-60.81** | [-63.96, -57.67] | **FASTER** |

⚠ **ONE INSTRUMENT DISCREPANCY, DIAGNOSED AND CORRECTED — §1.2. The point estimates match the established values exactly; the published INTERVALS in `RMST-ESTIMATOR-2026-08-16.md` are ~18% too NARROW because they use the independent two-sample variance for a PAIRED estimator.** I reproduce their intervals digit-for-digit with that formula and report the corrected (wider) paired intervals throughout.

**Answers to the five questions put to me:**
1. Full ranked table: §4.
2. **38 arms FAIL** (§5) — under the superseded ITT column 58 did. The bar's bite does not merely shrink, it **relocates**: 20 of the old form's 58 FAILs are actually FASTER.
3. **Verdict-change list: 79 arms (§3), 35 of them hard sign inversions.**
4. **27 arms are significantly FASTER (§6). Yes — 16 arms beat `BODYAWR` (−6.84) on the raw board, led by `MAPCODE` −60.81 and `SALTIDLE2` −24.27. ⛔ But every one of them is measured against a SUPERSEDED control, i.e. they are generation gains already banked into the incumbent. Restricted to the current-control class, `BODYAWRR`/`BODYAWR` and `AWRLNCH` remain the fastest and the only NEW name is `SALTREF2` (−3.04). §6.2.**
5. **30 arms are horizon-fragile (§7), 1 with a hard sign flip.** The fragile set is not random: it is dominated by the current-generation `MIX`/`CMB`/`SH` combination family, which drifts monotonically FAIL→flat→FASTER as the horizon widens.

---

## 1. THE ESTIMATOR, AND THE ONE THING I CHANGED

### 1.1 As implemented

```
value(game, side) = min(turns, H)   if that side won by core_destroyed
                  = H               otherwise (loss, tiebreak, r1000, any non-kill)
RMST_diff = mean(value(., T)) - mean(value(., C))          NEGATIVE = kills EARLIER = better
```
Over **ALL** games in the shard, no filtering on outcome; control is each arm's own declared `control=`. Horizons **H = 250 / 300 / 400**. DEFF **0.98** (local, balanced-by-construction); DEFF **1.25** reported alongside for the map-heterogeneous outliers (§8). Platform constants (1.529 / 1.833) are **not** imported.

**Non-degeneracy of the win predicate, reported as required:** over **784,644** nine-field rows in the snapshot, `winner == "T"` returns **398,635 (0.5080)** — non-degenerate and centred where a balanced board should sit. The trap predicate `winner == seat` returns **0 of 784,644 = exactly 0.0000**, a constant column, reproducing the failure mode the brief warned about.

### 1.2 ⛔ THE VARIANCE FORMULA — I DIFFER FROM THE ESTIMATOR DOC, AND IT IS DIAGNOSED, NOT ASSERTED

`value(·,T)` and `value(·,C)` are two outcomes of the **same game**: whenever T kills at turn *t*, `vT = min(t,H)` and `vC = H` **necessarily**. They are mechanically linked, and **measured `corr(vT, vC) = −0.41 to −0.43` on all four control cells.** The estimator is a one-sample mean of the per-game contrast `d_i = vT − vC`, so `Var = var(d)/n`. A negative correlation makes `var(d) = var(vT)+var(vC) − 2cov` **LARGER** than the independent sum — so the independent formula **understates** the interval.

**This reproduces exactly, which is what makes it a diagnosis rather than a disagreement:**

| control | RMST₃₀₀ | **PAIRED (correct)** | INDEPENDENT two-sample | doc's published CI | corr(vT,vC) |
|---|--:|:--:|:--:|:--:|--:|
| `NULL114` | +0.42 | [-2.43, +3.28] | [-1.96, +2.81] | [-1.96, +2.81] | -0.433 |
| `NEG114` | +33.27 | [+30.51, +36.03] | [+30.93, +35.61] | [+30.93, +35.61] | -0.408 |
| `NEG125` | +64.81 | [+60.45, +69.17] | [+61.09, +68.53] | [+61.10, +68.50] | -0.416 |
| `MAPCODE` | -60.81 | [-63.96, -57.67] | [-63.48, -58.15] | [-63.50, -58.10] | -0.426 |

**The INDEPENDENT column equals the doc's published column digit-for-digit on all four.** ⇒ `RMST-ESTIMATOR-2026-08-16.md` used the independent two-sample variance. Its intervals are **17–20% too narrow**; every point estimate in it is correct.

⛔ **AND IT IS THE ERROR THE BOARD SCAN ALREADY DOCUMENTED, ONE DOCUMENT EARLIER.** `R300-BAR-BOARD-SCAN-2026-08-16.md:579-581` states for the ITT indicator contrast: *"The independent two-sample formula is wrong here and understates the variance, since A and B are negatively correlated within a game."* The same structure holds for RMST and the same mistake was made. **A method note written correctly in one document and violated in the next is a note nobody has** — the same failure family `CLAUDE.md` records twice already.

**DIRECTION, per `CLAUDE.md`'s exclusion-restatement clause:** widening the interval makes **exclusion** claims (`FAIL`, `FASTER`) HARDER and fail-to-exclude (`flat`) EASIER. So this correction is **conservative for every verdict this document banks** and permissive only for `flat`, which is not an exclusion and is not banked as one. **Net effect on the headline: 4 arms move FASTER→flat and 0 arms gain a verdict.** The corrected form is used throughout; nothing below depends on the narrow intervals.

### 1.3 Boundary convention — checked, not asserted

`t < H` and `t <= H` at the horizon are **identical to 6dp** (delta 0.000000) on `NULL114`, `BODYAWR`, `MAPCODE` and `NEG114`. This is the defect that flipped a sign in an analogous choice earlier today, so it is measured rather than assumed.

---

## 2. CONTROLS — ALL FOUR CASES, PLUS THE FULL CALIBRATION FAMILY

### 2.1 The four required cells

All four hit their established point estimates **exactly**. **No discrepancy on any of them; the pipeline is not reporting a failure.**

### 2.2 The whole calibration family, which is stronger than the four

| cell | kind | n | RMST₃₀₀ | 95% CI | verdict | correct? |
|---|---|--:|--:|:--:|:--:|:--:|
| `NULL114` | identity / null | 5408 | +0.42 | [-2.43, +3.28] | flat | ✅ |
| `NULL5400` | identity / null | 5400 | +0.27 | [-2.18, +2.72] | flat | ✅ |
| `NULL140B` | identity / null | 5385 | -2.62 | [-5.57, +0.32] | flat | ✅ |
| `SR1NULL` | identity / null | 5408 | +0.23 | [-2.63, +3.08] | flat | ✅ |
| `SR2NULL` | identity / null | 5408 | +1.44 | [-1.38, +4.27] | flat | ✅ |
| `SRNULL0` | identity / null | 5408 | +0.46 | [-2.43, +3.34] | flat | ✅ |
| `NULL123` | identity / null | 2602 | +0.86 | [-2.33, +4.04] | flat | ✅ |
| `NULL125` | identity / null | 5400 | -1.14 | [-3.99, +1.72] | flat | ✅ |
| `SEATREL` | identity / null | 2752 | -1.35 | [-5.26, +2.56] | flat | ✅ |
| `NEG114` | deliberate NEGATIVE | 5408 | **+33.27** | [+30.51, +36.03] | **FAIL** | ✅ |
| `NEG123` | deliberate NEGATIVE | 2529 | **+12.72** | [+9.33, +16.12] | **FAIL** | ✅ |
| `NEG125` | deliberate NEGATIVE | 2225 | **+64.81** | [+60.45, +69.17] | **FAIL** | ✅ |
| `NEG169` | deliberate NEGATIVE | 5408 | **+22.34** | [+19.53, +25.14] | **FAIL** | ✅ |
| `MAPCODE` | shipped `MAP_CODES` fix | 4328 | **-60.81** | [-63.96, -57.67] | **FASTER** | ✅ |

**All 9 identity/null cells read flat** (|Δ| ≤ 2.62 rounds, every CI straddling zero). **All 4 deliberately-degraded NEG cells read SLOWER**, the known-bad direction.

⭐ **THIS IS A STRICTLY STRONGER CALIBRATION RESULT THAN THE BRIEF ASKED FOR, AND IT IS THE CLEANEST INDICTMENT OF THE OLD FORM.** The superseded scan's §4.2 recorded that **all four NEG cells collected `PASS` under the old ITT form — three of them as an *established* fall, the strongest pass the bar can issue.** Under RMST₃₀₀ all four correctly **FAIL**: `NEG114` +33.27, `NEG123` +12.72, `NEG125` +64.81, `NEG169` +22.34. **A bar that awarded its strongest pass to every cell built to be worse has been inverted on exactly the cells whose direction we knew in advance.**

### 2.3 Mutation drive — per guard, per branch, each driven to the other verdict

`turns += 100` applied to one side at a time, everything else held fixed:

| cell | baseline | treatment +100 | control +100 |
|---|:--:|:--:|:--:|
| `NULL114` | +0.42 flat | **+31.19 FAIL** | **-30.41 FASTER** |
| `NULL5400` | +0.27 flat | **+21.33 FAIL** | **-21.18 FASTER** |
| `NULL140B` | -2.62 flat | **+27.75 FAIL** | **-31.11 FASTER** |

**All three verdict labels are reachable, in the correct direction, on both branches, on three independent null cells.** A guard that has never produced the other verdict has not been seen to guard.

---

## 3. ⭐ THE VERDICT-CHANGE LIST — THE COST OF THE ESTIMATOR ERROR

### 3.1 The change matrix

Rows = superseded ITT/`AFTER` verdict (relabelled into RMST's space: its `PASS` = established fall = `FASTER`). Columns = RMST₃₀₀ verdict.

| old ↓ / new → | FAIL | flat | FASTER | total |
|---|--:|--:|--:|--:|
| **FAIL** | 13 | 25 | **20** | 58 |
| **flat** | 10 | 58 | 7 | 75 |
| **FASTER** | **15** | 2 | 0 | 17 |
| **total** | 38 | 85 | 27 | 150 |

**Off-diagonal = 79 of 150 (52.7%). The two bolded corners are the hard sign inversions: 15 + 20 = 35 arms.**

### 3.2 ⛔ INVERSION A — the old form called these an ESTABLISHED IMPROVEMENT; they are significantly SLOWER (15)

| shard | n | win% | old ITT (Δpp) | **RMST₃₀₀** | 95% CI | medkill T / C |
|---|--:|--:|:--:|--:|:--:|--:|
| `NEG125` | 2225 | 24.94 | PASS (-4.67) | **+64.81** | [+60.45, +69.17] | 213 / 164 |
| `SALTOFF` | 2794 | 28.85 | PASS (-6.73) | **+38.05** | [+33.95, +42.16] | 188.0 / 196 |
| `NOAPPROACH` | 2264 | 18.55 | PASS (-40.33) | **+33.81** | [+31.36, +36.26] | 270.0 / 325 |
| `NEG114` | 5408 | 36.32 | PASS (-1.66) | **+33.27** | [+30.51, +36.03] | 226.0 / 194 |
| `IDLECULL` | 3774 | 33.55 | PASS (-6.97) | **+26.84** | [+23.27, +30.41] | 171 / 195.0 |
| `NEG169` | 5408 | 40.53 | PASS (-1.83) | **+22.34** | [+19.53, +25.14] | 216.0 / 199.5 |
| `V120` | 5408 | 36.15 | PASS (-10.50) | **+16.12** | [+13.46, +18.79] | 213 / 227 |
| `NEG123` | 2529 | 43.26 | PASS (-2.49) | **+12.72** | [+9.33, +16.12] | 224 / 214.5 |
| `LAUNCH2` | 5408 | 44.67 | PASS (-1.57) | **+9.43** | [+6.55, +12.31] | 203.0 / 205.0 |
| `LAUNCH3` | 5408 | 43.73 | PASS (-2.92) | **+9.24** | [+6.43, +12.05] | 207.0 / 211 |
| `MINHARV1` | 5408 | 47.24 | PASS (-1.85) | **+7.61** | [+4.85, +10.38] | 216.0 / 212.0 |
| `AMMO0` | 5400 | 46.22 | PASS (-2.07) | **+5.59** | [+2.65, +8.54] | 202 / 205 |
| `BOTH0` | 5408 | 46.43 | PASS (-1.57) | **+5.41** | [+2.56, +8.25] | 206 / 208.0 |
| `FWDFLOOR8` | 2788 | 45.88 | PASS (-2.22) | **+4.51** | [+0.33, +8.69] | 197.0 / 205.5 |
| `GUNAX0` | 5408 | 48.00 | PASS (-1.90) | **+3.32** | [+0.40, +6.24] | 205 / 206 |

**Win shares 18.55%–48.00%. Every one is a LOSING arm, and the set contains all four NEG calibration cells plus `NOAPPROACH` (18.6% win), `SALTOFF` (28.9%) and `IDLECULL` (33.6%).**

### 3.3 ⛔ INVERSION B — the old form FAILED these; they are significantly FASTER (20)

| shard | n | win% | old ITT (Δpp) | **RMST₃₀₀** | 95% CI | medkill T / C |
|---|--:|--:|:--:|--:|:--:|--:|
| `MAPCODE` | 4328 | 73.27 | FAIL (+2.98) | **-60.81** | [-63.96, -57.67] | 165 / 217 |
| `SALTIDLE2` | 5408 | 64.57 | FAIL (+5.12) | **-24.27** | [-26.98, -21.57] | 212.0 / 212.0 |
| `SALTNOBLOCK` | 5408 | 61.35 | FAIL (+6.18) | **-16.92** | [-19.67, -14.16] | 212.0 / 208.0 |
| `SEALREPAIR` | 5396 | 59.30 | FAIL (+5.10) | **-15.90** | [-18.80, -12.99] | 205.0 / 204.0 |
| `MAPFIX2` | 2159 | 57.53 | FAIL (+4.91) | **-15.77** | [-19.89, -11.66] | 230 / 240 |
| `SALT` | 5408 | 61.00 | FAIL (+6.58) | **-15.15** | [-17.87, -12.44] | 218.0 / 210.0 |
| `SALTREP` | 5408 | 60.56 | FAIL (+6.08) | **-14.97** | [-17.70, -12.24] | 216.0 / 207.0 |
| `IDLEVSALT2` | 2545 | 56.82 | FAIL (+1.81) | **-14.00** | [-17.14, -10.86] | 219.0 / 250.5 |
| `SALTCUTONLY` | 5408 | 60.80 | FAIL (+6.62) | **-13.83** | [-16.61, -11.05] | 214 / 204 |
| `SEALREPAIRR` | 5394 | 56.77 | FAIL (+3.78) | **-11.31** | [-14.19, -8.43] | 210.0 / 208 |
| `MAPFIX` | 2160 | 55.65 | FAIL (+3.24) | **-10.78** | [-14.91, -6.66] | 238.0 / 243 |
| `IDLEVSALT` | 5408 | 55.99 | FAIL (+3.05) | **-9.68** | [-12.25, -7.11] | 227 / 226.5 |
| `BODYAWRR` | 5400 | 54.89 | FAIL (+3.22) | **-8.89** | [-11.82, -5.96] | 206.5 / 209.0 |
| `L4REPAIR2` | 5395 | 54.88 | FAIL (+1.43) | **-8.63** | [-11.53, -5.74] | 205 / 211 |
| `BODYAWR` | 10800 | 53.70 | FAIL (+2.66) | **-6.84** | [-8.93, -4.75] | 205 / 207 |
| `AWRLNCH` | 5399 | 53.95 | FAIL (+2.35) | **-6.43** | [-9.34, -3.53] | 205.0 / 208 |
| `SEALFLOOR0R` | 5347 | 53.66 | FAIL (+3.96) | **-5.09** | [-7.91, -2.27] | 217 / 214.0 |
| `SEALFLOOR0` | 5396 | 54.78 | FAIL (+4.78) | **-4.80** | [-7.67, -1.92] | 217.0 / 204.0 |
| `APPRLAUNCH2` | 5400 | 52.39 | FAIL (+1.33) | **-4.33** | [-7.16, -1.50] | 212.0 / 212.0 |
| `GUNAXREP` | 5408 | 52.31 | FAIL (+1.52) | **-3.07** | [-5.93, -0.20] | 210.0 / 206 |

**Win shares 52.31%–73.27%. Every one is a WINNING arm.**

⭐ **THE INVERSION IS PERFECTLY SORTED BY WIN SHARE AND THE TWO GROUPS DO NOT OVERLAP: inversion A spans 18.55–48.00%, inversion B spans 52.31–73.27%, with a clean gap at 50%.** The superseded scan predicted exactly this in its §2.2 (`corr(ITT difference, win share) = +0.776`; the VOLUME channel `r = +0.949`) and stated it could not rule. **Measured against the unbiased estimator, the old ITT/`AFTER` column was reading win share with the sign reversed.**

### 3.4 The remaining 44 changes (a verdict gained or lost, no sign inversion)

| shard | n | win% | old ITT | **RMST₃₀₀** | 95% CI | new verdict |
|---|--:|--:|:--:|--:|:--:|:--:|
| `LATE160AMMO` | 5408 | 53.31 | PASS(nd) (+0.09) | **-6.29** | [-9.21, -3.38] | **FASTER** |
| `APPRLAUNCH` | 5400 | 52.94 | PASS(nd) (+1.30) | **-4.75** | [-7.61, -1.89] | **FASTER** |
| `BURST64B` | 5408 | 51.04 | PASS(nd) (-0.43) | **-3.60** | [-6.57, -0.63] | **FASTER** |
| `ZEROAMMO` | 5408 | 52.90 | PASS(nd) (+0.65) | **-3.53** | [-6.43, -0.63] | **FASTER** |
| `L4REPAIR` | 5408 | 51.28 | PASS(nd) (+0.68) | **-3.12** | [-6.04, -0.21] | **FASTER** |
| `SR1CUR` | 5408 | 51.37 | PASS(nd) (-0.04) | **-3.12** | [-5.95, -0.29] | **FASTER** |
| `SALTREF2` | 5400 | 51.78 | PASS(nd) (+0.91) | **-3.04** | [-5.98, -0.10] | **FASTER** |
| `MIX285mix2` | 5400 | 54.39 | FAIL (+4.44) | **-2.23** | [-5.00, +0.54] | **flat** |
| `AWRSPAWN` | 5400 | 55.06 | FAIL (+5.06) | **-1.97** | [-4.69, +0.75] | **flat** |
| `ECORAID2` | 5400 | 52.91 | FAIL (+3.37) | **-1.78** | [-4.60, +1.03] | **flat** |
| `CMB292` | 5400 | 54.07 | FAIL (+4.15) | **-1.57** | [-4.35, +1.22] | **flat** |
| `ECORAID` | 5400 | 53.22 | FAIL (+4.30) | **-1.56** | [-4.32, +1.20] | **flat** |
| `SALTCLEAR` | 5408 | 52.83 | FAIL (+2.37) | **-1.10** | [-3.60, +1.41] | **flat** |
| `NULLSALT` | 5408 | 51.09 | FAIL (+1.79) | **-1.04** | [-3.57, +1.49] | **flat** |
| `MIX280mix4` | 5400 | 55.24 | FAIL (+5.63) | **-0.87** | [-3.56, +1.82] | **flat** |
| `LNCHRND1` | 5400 | 51.93 | FAIL (+3.04) | **-0.70** | [-3.56, +2.17] | **flat** |
| `COMBO` | 5400 | 52.30 | FAIL (+2.98) | **-0.56** | [-3.33, +2.22] | **flat** |
| `TRIO` | 5807 | 54.35 | FAIL (+4.96) | **-0.34** | [-2.93, +2.25] | **flat** |
| `MIX281mix4` | 5400 | 55.07 | FAIL (+6.50) | **-0.29** | [-2.94, +2.36] | **flat** |
| `ROUTEONLY` | 3632 | 47.60 | PASS (-1.98) | **-0.18** | [-3.12, +2.75] | **flat** |
| `CMB299` | 4372 | 54.25 | FAIL (+5.97) | **-0.11** | [-3.21, +2.98] | **flat** |
| `MIX284mix3` | 5400 | 54.56 | FAIL (+5.85) | **+0.21** | [-2.48, +2.90] | **flat** |
| `HOMEMAX` | 5400 | 51.24 | FAIL (+2.41) | **+0.32** | [-2.47, +3.12] | **flat** |
| `RND1SOLO` | 5400 | 51.30 | FAIL (+1.98) | **+0.40** | [-2.46, +3.26] | **flat** |
| `UNDERECO` | 5400 | 51.56 | FAIL (+2.35) | **+0.61** | [-2.18, +3.41] | **flat** |
| `DIGOUT` | 5400 | 48.67 | PASS (-1.78) | **+1.14** | [-1.66, +3.95] | **flat** |
| `CATRND1L` | 5400 | 51.19 | FAIL (+2.72) | **+1.24** | [-1.62, +4.09] | **flat** |
| `CATRND1` | 4620 | 50.95 | FAIL (+2.68) | **+1.38** | [-1.73, +4.50] | **flat** |
| `MIX282mix5` | 5400 | 54.65 | FAIL (+6.83) | **+1.57** | [-1.14, +4.28] | **flat** |
| `SH288` | 5400 | 53.61 | FAIL (+5.17) | **+1.57** | [-1.23, +4.37] | **flat** |
| `CMB296` | 5400 | 51.85 | FAIL (+3.65) | **+1.78** | [-1.16, +4.72] | **flat** |
| `CMB291` | 5400 | 53.78 | FAIL (+5.91) | **+2.66** | [-0.07, +5.39] | **flat** |
| `F257CATMAX` | 5400 | 50.65 | FAIL (+2.50) | **+2.87** | [-0.01, +5.75] | **flat** |
| `SALTROUTE` | 5408 | 48.74 | PASS(nd) (-0.85) | **+2.97** | [+0.44, +5.49] | **FAIL** |
| `G400g4` | 3545 | 52.95 | FAIL (+5.78) | **+3.27** | [-0.10, +6.64] | **flat** |
| `SENTTHRR` | 5400 | 48.30 | PASS(nd) (-0.07) | **+3.45** | [+0.51, +6.39] | **FAIL** |
| `SCREEN` | 5408 | 48.84 | PASS(nd) (-0.07) | **+3.49** | [+0.60, +6.38] | **FAIL** |
| `SHIPGATE0` | 3089 | 49.27 | PASS(nd) (+0.10) | **+3.92** | [+0.02, +7.83] | **FAIL** |
| `SCREEN4` | 5408 | 48.85 | PASS(nd) (+0.65) | **+4.38** | [+1.52, +7.24] | **FAIL** |
| `SHIPGATE160` | 3048 | 49.41 | PASS(nd) (+0.89) | **+4.76** | [+0.88, +8.64] | **FAIL** |
| `F254COLLARS` | 3740 | 47.62 | PASS(nd) (-1.15) | **+5.98** | [+2.49, +9.47] | **FAIL** |
| `SEALFLOOR6` | 2737 | 47.61 | PASS(nd) (-1.39) | **+6.05** | [+1.87, +10.22] | **FAIL** |
| `EXILE0` | 5408 | 47.02 | PASS(nd) (-0.65) | **+6.23** | [+3.38, +9.07] | **FAIL** |
| `F232SEALTEM` | 5400 | 45.54 | PASS(nd) (-0.54) | **+10.98** | [+7.98, +13.97] | **FAIL** |

*(Against the superseded AS-WRITTEN column instead, 66 of 150 verdicts change. The ITT/`AFTER` comparison above is the load-bearing one, since that is the orientation `PROGRAMME.md` carried when the scan was briefed.)*

---

## 4. FULL RANKED TABLE — ALL 150 ARMS BY RMST₃₀₀

Sorted fastest-first. **Negative = treatment kills EARLIER = better.** Intervals are the corrected PAIRED form at DEFF 0.98. `H250`/`H400` carry their own verdict letter: `F`=FAIL, `·`=flat, `<`=FASTER.

| # | shard | host | n | win% | control | **RMST₃₀₀** | 95% CI | verdict | H250 | H400 | old ITT | Δ? |
|--:|---|---|--:|--:|---|--:|:--:|:--:|--:|--:|:--:|:--:|
| 1 | `MAPCODE` | local | 4328 | 73.27 | `v187saltidle_f` | **-60.81** | [-63.96, -57.67] | **FASTER** | -39.92< | -104.65< | FAIL (+2.98) | **Δ** |
| 2 | `SALTIDLE2` | local | 5408 | 64.57 | `v169launchlate160` | **-24.27** | [-26.98, -21.57] | **FASTER** | -13.75< | -49.33< | FAIL (+5.12) | **Δ** |
| 3 | `SALTNOBLOCK` | local | 5408 | 61.35 | `v169launchlate160` | **-16.92** | [-19.67, -14.16] | **FASTER** | -9.35< | -34.53< | FAIL (+6.18) | **Δ** |
| 4 | `SEALREPAIR` | local | 5396 | 59.30 | `v218mapfix` | **-15.90** | [-18.80, -12.99] | **FASTER** | -9.40< | -31.18< | FAIL (+5.10) | **Δ** |
| 5 | `MAPFIX2` | local | 2159 | 57.53 | `v197mapcode` | **-15.77** | [-19.89, -11.66] | **FASTER** | -10.22< | -29.57< | FAIL (+4.91) | **Δ** |
| 6 | `SALT` | local | 5408 | 61.00 | `v169launchlate160` | **-15.15** | [-17.87, -12.44] | **FASTER** | -8.25< | -32.65< | FAIL (+6.58) | **Δ** |
| 7 | `SALTREP` | local | 5408 | 60.56 | `v169launchlate160` | **-14.97** | [-17.70, -12.24] | **FASTER** | -7.93< | -31.59< | FAIL (+6.08) | **Δ** |
| 8 | `IDLEVSALT2` | local | 2545 | 56.82 | `v178salt` | **-14.00** | [-17.14, -10.86] | **FASTER** | -8.47< | -26.32< | FAIL (+1.81) | **Δ** |
| 9 | `SALTCUTONLY` | local | 5408 | 60.80 | `v169launchlate160` | **-13.83** | [-16.61, -11.05] | **FASTER** | -7.29< | -29.88< | FAIL (+6.62) | **Δ** |
| 10 | `SEALREPAIRR` | work-server-1 | 5394 | 56.77 | `v218mapfix` | **-11.31** | [-14.19, -8.43] | **FASTER** | -6.68< | -21.58< | FAIL (+3.78) | **Δ** |
| 11 | `MAPFIX` | local | 2160 | 55.65 | `v197mapcode` | **-10.78** | [-14.91, -6.66] | **FASTER** | -6.76< | -22.26< | FAIL (+3.24) | **Δ** |
| 12 | `IDLEVSALT` | local | 5408 | 55.99 | `v178salt` | **-9.68** | [-12.25, -7.11] | **FASTER** | -5.63< | -19.92< | FAIL (+3.05) | **Δ** |
| 13 | `BODYAWRR` | work-server-2 | 5400 | 54.89 | `v223sealrepair` | **-8.89** | [-11.82, -5.96] | **FASTER** | -5.80< | -15.64< | FAIL (+3.22) | **Δ** |
| 14 | `L4REPAIR2` | local | 5395 | 54.88 | `v197mapcode` | **-8.63** | [-11.53, -5.74] | **FASTER** | -5.26< | -16.21< | FAIL (+1.43) | **Δ** |
| 15 | `BODYAWR` | local | 10800 | 53.70 | `v223sealrepair` | **-6.84** | [-8.93, -4.75] | **FASTER** | -4.55< | -12.16< | FAIL (+2.66) | **Δ** |
| 16 | `AWRLNCH` | local | 5399 | 53.95 | `v223sealrepair` | **-6.43** | [-9.34, -3.53] | **FASTER** | -3.28< | -14.14< | FAIL (+2.35) | **Δ** |
| 17 | `LATE160AMMO` | local | 5408 | 53.31 | `x3r0_v115` | **-6.29** | [-9.21, -3.38] | **FASTER** | -3.91< | -11.06< | PASS(nd) (+0.09) | **Δ** |
| 18 | `SEALFLOOR0R` | work-server-1 | 5347 | 53.66 | `v197mapcode` | **-5.09** | [-7.91, -2.27] | **FASTER** | -3.21< | -10.11< | FAIL (+3.96) | **Δ** |
| 19 | `SEALFLOOR0` | local | 5396 | 54.78 | `v197mapcode` | **-4.80** | [-7.67, -1.92] | **FASTER** | -2.65< | -10.66< | FAIL (+4.78) | **Δ** |
| 20 | `APPRLAUNCH` | local | 5400 | 52.94 | `v197mapcode` | **-4.75** | [-7.61, -1.89] | **FASTER** | -2.61< | -9.57< | PASS(nd) (+1.30) | **Δ** |
| 21 | `APPRLAUNCH2` | local | 5400 | 52.39 | `v197mapcode` | **-4.33** | [-7.16, -1.50] | **FASTER** | -2.54< | -9.03< | FAIL (+1.33) | **Δ** |
| 22 | `BURST64B` | local | 5408 | 51.04 | `v171late160ammo` | **-3.60** | [-6.57, -0.63] | **FASTER** | -2.53< | -5.21< | PASS(nd) (-0.43) | **Δ** |
| 23 | `ZEROAMMO` | local | 5408 | 52.90 | `x3r0_v115` | **-3.53** | [-6.43, -0.63] | **FASTER** | -2.02< | -7.63< | PASS(nd) (+0.65) | **Δ** |
| 24 | `L4REPAIR` | local | 5408 | 51.28 | `v169launchlate160` | **-3.12** | [-6.04, -0.21] | **FASTER** | -2.13< | -5.09< | PASS(nd) (+0.68) | **Δ** |
| 25 | `SR1CUR` | local | 5408 | 51.37 | `v148ferryfirst` | **-3.12** | [-5.95, -0.29] | **FASTER** | -1.88< | -5.96< | PASS(nd) (-0.04) | **Δ** |
| 26 | `GUNAXREP` | local | 5408 | 52.31 | `v148ferryfirst` | **-3.07** | [-5.93, -0.20] | **FASTER** | -1.56· | -6.88< | FAIL (+1.52) | **Δ** |
| 27 | `SALTREF2` | work-server-1 | 5400 | 51.78 | `v223sealrepair` | **-3.04** | [-5.98, -0.10] | **FASTER** | -1.83· | -5.97< | PASS(nd) (+0.91) | **Δ** |
| 28 | `GUNBLANK` | local | 5408 | 52.11 | `v146gunaxis` | **-2.78** | [-5.70, +0.13] | **flat** | -1.31· | -6.06< | PASS(nd) (+0.72) |  |
| 29 | `FERRY0` | local | 5408 | 50.15 | `v146gunaxis` | **-2.63** | [-5.49, +0.22] | **flat** | -2.23< | -2.69· | PASS(nd) (+0.30) |  |
| 30 | `NULL140B` | work-server-2 | 5385 | 50.88 | `v264nullbeta` | **-2.62** | [-5.57, +0.32] | **flat** | -1.58· | -4.96· | PASS(nd) (+0.11) |  |
| 31 | `SR2CUR` | local | 5408 | 50.98 | `v148ferryfirst` | **-2.55** | [-5.40, +0.30] | **flat** | -1.90< | -3.47· | PASS(nd) (+0.46) |  |
| 32 | `BLANKBORDER` | local | 5408 | 51.29 | `v146gunaxis` | **-2.47** | [-5.39, +0.44] | **flat** | -1.44· | -4.70· | PASS(nd) (+1.24) |  |
| 33 | `GUNEARLY150` | local | 5408 | 50.68 | `v146gunaxis` | **-2.41** | [-5.28, +0.45] | **flat** | -1.54· | -3.98· | PASS(nd) (-0.80) |  |
| 34 | `TWORAID` | local | 5400 | 50.63 | `v197mapcode` | **-2.29** | [-5.17, +0.59] | **flat** | -1.61· | -3.35· | PASS(nd) (+0.31) |  |
| 35 | `MIX285mix2` | local | 5400 | 54.39 | `v223sealrepair` | **-2.23** | [-5.00, +0.54] | **flat** | -0.62· | -6.67< | FAIL (+4.44) | **Δ** |
| 36 | `MAPSALT` | local | 2363 | 50.40 | `v223sealrepair` | **-2.17** | [-6.67, +2.34] | **flat** | -0.57· | -6.00· | PASS(nd) (-1.61) |  |
| 37 | `AWRSPAWN` | work-server-2 | 5400 | 55.06 | `v223sealrepair` | **-1.97** | [-4.69, +0.75] | **flat** | +0.59· | -9.40< | FAIL (+5.06) | **Δ** |
| 38 | `ECORAID2` | local | 5400 | 52.91 | `v197mapcode` | **-1.78** | [-4.60, +1.03] | **flat** | -0.87· | -5.43< | FAIL (+3.37) | **Δ** |
| 39 | `CMB292` | local | 5400 | 54.07 | `v223sealrepair` | **-1.57** | [-4.35, +1.22] | **flat** | -0.16· | -6.12< | FAIL (+4.15) | **Δ** |
| 40 | `ECORAID` | local | 5400 | 53.22 | `v197mapcode` | **-1.56** | [-4.32, +1.20] | **flat** | -0.38· | -5.49< | FAIL (+4.30) | **Δ** |
| 41 | `DELVSDEF` | local | 5408 | 50.20 | `v171late160ammo` | **-1.51** | [-4.47, +1.45] | **flat** | -0.97· | -2.78· | PASS(nd) (-0.78) |  |
| 42 | `TINYECO62` | local | 2700 | 50.93 | `v223sealrepair` | **-1.48** | [-5.15, +2.18] | **flat** | -0.97· | -2.52· | PASS(nd) (+0.15) |  |
| 43 | `GUNSEAT` | local | 5408 | 51.04 | `v146gunaxis` | **-1.41** | [-4.27, +1.44] | **flat** | -0.68· | -3.32· | PASS(nd) (+0.22) |  |
| 44 | `STANDOFF` | local | 5400 | 50.56 | `v197mapcode` | **-1.39** | [-4.24, +1.46] | **flat** | -0.66· | -3.62· | PASS(nd) (+0.15) |  |
| 45 | `SENTTHR` | local | 5400 | 49.80 | `v223sealrepair` | **-1.37** | [-4.32, +1.57] | **flat** | -1.08· | -1.07· | PASS(nd) (-0.91) |  |
| 46 | `SEATREL` | local | 2752 | 50.40 | `v197mapcode` | **-1.35** | [-5.26, +2.56] | **flat** | -0.90· | -1.70· | PASS(nd) (-0.07) |  |
| 47 | `F253CATAPUL` | work-server-2 | 5400 | 50.02 | `v223sealrepair` | **-1.35** | [-4.30, +1.60] | **flat** | -0.83· | -1.68· | PASS(nd) (-0.91) |  |
| 48 | `GUNAXABLR` | work-server-2 | 5400 | 50.61 | `v223sealrepair` | **-1.20** | [-4.15, +1.74] | **flat** | -0.78· | -2.35· | PASS(nd) (+0.11) |  |
| 49 | `LAUNCH0` | local | 5408 | 52.77 | `v146gunaxis` | **-1.16** | [-4.08, +1.77] | **flat** | +0.19· | -4.16· | PASS(nd) (+0.68) |  |
| 50 | `NULL125` | local | 5400 | 51.04 | `v197mapcode` | **-1.14** | [-3.99, +1.72] | **flat** | -0.57· | -2.69· | PASS(nd) (+0.46) |  |
| 51 | `SALTCLEAR` | local | 5408 | 52.83 | `v178salt` | **-1.10** | [-3.60, +1.41] | **flat** | -0.05· | -3.72· | FAIL (+2.37) | **Δ** |
| 52 | `NULLSALT` | local | 5408 | 51.09 | `v178salt` | **-1.04** | [-3.57, +1.49] | **flat** | -0.65· | -2.27· | FAIL (+1.79) | **Δ** |
| 53 | `BURST32B` | local | 5408 | 50.33 | `v171late160ammo` | **-0.94** | [-3.92, +2.04] | **flat** | -0.60· | -1.91· | PASS(nd) (-0.09) |  |
| 54 | `MIX280mix4` | local | 5400 | 55.24 | `v223sealrepair` | **-0.87** | [-3.56, +1.82] | **flat** | +1.35· | -8.67< | FAIL (+5.63) | **Δ** |
| 55 | `HEALERFIRST` | local | 5408 | 50.80 | `v171late160ammo` | **-0.83** | [-3.82, +2.15] | **flat** | -0.60· | -1.42· | PASS(nd) (+0.65) |  |
| 56 | `RAIDDL` | local | 5400 | 50.43 | `v197mapcode` | **-0.73** | [-3.59, +2.14] | **flat** | -0.53· | -1.64· | PASS(nd) (+1.04) |  |
| 57 | `LNCHRND1` | work-server-1 | 5400 | 51.93 | `v223sealrepair` | **-0.70** | [-3.56, +2.17] | **flat** | +0.23· | -2.99· | FAIL (+3.04) | **Δ** |
| 58 | `AIMTHROW2` | local | 4005 | 50.11 | `v218mapfix` | **-0.67** | [-3.94, +2.61] | **flat** | -0.74· | -0.57· | PASS(nd) (+0.32) |  |
| 59 | `COMBO` | local | 5400 | 52.30 | `v197mapcode` | **-0.56** | [-3.33, +2.22] | **flat** | +0.30· | -3.48· | FAIL (+2.98) | **Δ** |
| 60 | `GUNBORDER` | local | 5408 | 50.48 | `v146gunaxis` | **-0.51** | [-3.40, +2.37] | **flat** | -0.30· | -0.96· | PASS(nd) (+0.61) |  |
| 61 | `F232COLLARM` | work-server-2 | 5400 | 49.94 | `v223sealrepair` | **-0.51** | [-3.46, +2.44] | **flat** | -0.75· | -0.07· | PASS(nd) (+0.19) |  |
| 62 | `TRIO` | local | 5807 | 54.35 | `v223sealrepair` | **-0.34** | [-2.93, +2.25] | **flat** | +1.46· | -6.88< | FAIL (+4.96) | **Δ** |
| 63 | `MIX281mix4` | local | 5400 | 55.07 | `v223sealrepair` | **-0.29** | [-2.94, +2.36] | **flat** | +1.75· | -7.43< | FAIL (+6.50) | **Δ** |
| 64 | `GUNBLANKREP` | local | 5408 | 50.30 | `v146gunaxis` | **-0.26** | [-3.11, +2.58] | **flat** | -0.11· | -0.97· | PASS(nd) (+0.57) |  |
| 65 | `GUNPEN16` | local | 5408 | 50.72 | `v146gunaxis` | **-0.19** | [-3.06, +2.67] | **flat** | +0.17· | -1.11· | PASS(nd) (+0.24) |  |
| 66 | `ROUTEONLY` | local | 3632 | 47.60 | `v178salt` | **-0.18** | [-3.12, +2.75] | **flat** | -1.01· | +2.66· | PASS (-1.98) | **Δ** |
| 67 | `CMB299` | local | 4372 | 54.25 | `v223sealrepair` | **-0.11** | [-3.21, +2.98] | **flat** | +0.89· | -4.08· | FAIL (+5.97) | **Δ** |
| 68 | `GUNAXTB` | local | 5408 | 49.82 | `v148ferryfirst` | **-0.01** | [-2.87, +2.84] | **flat** | -0.07· | +0.08· | PASS(nd) (-0.85) |  |
| 69 | `F250HOMEEAR` | work-server-2 | 5400 | 50.48 | `v223sealrepair` | **+0.04** | [-2.86, +2.95] | **flat** | +0.64· | -1.05· | PASS(nd) (-0.07) |  |
| 70 | `SENTSAFE2` | local | 5408 | 49.83 | `v169launchlate160` | **+0.05** | [-2.86, +2.96] | **flat** | +0.00· | +0.14· | PASS(nd) (+0.18) |  |
| 71 | `MIX284mix3` | local | 5400 | 54.56 | `v223sealrepair` | **+0.21** | [-2.48, +2.90] | **flat** | +1.87F | -5.80< | FAIL (+5.85) | **Δ** |
| 72 | `SEALFIRST` | local | 2018 | 49.55 | `v197mapcode` | **+0.22** | [-4.28, +4.73] | **flat** | +0.11· | +0.87· | PASS(nd) (-1.04) |  |
| 73 | `LNCHERL2` | work-server-2 | 5405 | 50.32 | `v223sealrepair` | **+0.23** | [-2.69, +3.15] | **flat** | +0.68· | -0.82· | PASS(nd) (-0.26) |  |
| 74 | `SR1NULL` | local | 5408 | 49.37 | `v151null` | **+0.23** | [-2.63, +3.08] | **flat** | +0.19· | +1.02· | PASS(nd) (-0.44) |  |
| 75 | `NULL5400` | local | 5400 | 49.94 | `v146gunaxis` | **+0.27** | [-2.18, +2.72] | **flat** | +0.04· | +0.52· | PASS(nd) (+0.59) |  |
| 76 | `HOMEMAX` | local | 5400 | 51.24 | `v223sealrepair` | **+0.32** | [-2.47, +3.12] | **flat** | +0.92· | -1.90· | FAIL (+2.41) | **Δ** |
| 77 | `LAUNCHRES0` | local | 5408 | 48.63 | `v169launchlate160` | **+0.34** | [-2.55, +3.23] | **flat** | -0.28· | +1.97· | PASS(nd) (-1.29) |  |
| 78 | `RND1SOLO` | local | 5400 | 51.30 | `v223sealrepair` | **+0.40** | [-2.46, +3.26] | **flat** | +1.13· | -1.87· | FAIL (+1.98) | **Δ** |
| 79 | `NULL114` | local | 5408 | 49.98 | `v146gunaxis` | **+0.42** | [-2.43, +3.28] | **flat** | +0.54· | +0.40· | PASS(nd) (-0.15) |  |
| 80 | `SRNULL0` | local | 5408 | 50.17 | `v148ferryfirst` | **+0.46** | [-2.43, +3.34] | **flat** | +0.06· | +0.33· | PASS(nd) (+1.15) |  |
| 81 | `UNDERECO` | local | 5400 | 51.56 | `v197mapcode` | **+0.61** | [-2.18, +3.41] | **flat** | +0.72· | -1.09· | FAIL (+2.35) | **Δ** |
| 82 | `GUNFERRY` | local | 5408 | 50.20 | `v146gunaxis` | **+0.62** | [-2.28, +3.52] | **flat** | +0.17· | +1.20· | PASS(nd) (+0.91) |  |
| 83 | `GBNOSHIELD` | local | 5408 | 51.02 | `v169launchlate160` | **+0.68** | [-2.26, +3.62] | **flat** | +0.79· | +0.03· | PASS(nd) (+1.07) |  |
| 84 | `GUNEARLY60` | local | 5408 | 49.83 | `v146gunaxis` | **+0.74** | [-2.11, +3.60] | **flat** | +0.57· | +1.80· | PASS(nd) (+0.20) |  |
| 85 | `NULL123` | local | 2602 | 48.58 | `v187saltidle_f` | **+0.86** | [-2.33, +4.04] | **flat** | +0.35· | +3.32· | PASS(nd) (-1.73) |  |
| 86 | `DIGOUT` | local | 5400 | 48.67 | `v197mapcode` | **+1.14** | [-1.66, +3.95] | **flat** | +0.68· | +2.62· | PASS (-1.78) | **Δ** |
| 87 | `LAUNCHRES20` | local | 5408 | 48.95 | `v169launchlate160` | **+1.15** | [-1.72, +4.03] | **flat** | +0.31· | +3.09· | PASS(nd) (-0.37) |  |
| 88 | `CATRND1L` | local | 5400 | 51.19 | `v223sealrepair` | **+1.24** | [-1.62, +4.09] | **flat** | +1.59· | +0.12· | FAIL (+2.72) | **Δ** |
| 89 | `CATRND1` | work-server-1 | 4620 | 50.95 | `v223sealrepair` | **+1.38** | [-1.73, +4.50] | **flat** | +1.56· | -0.04· | FAIL (+2.68) | **Δ** |
| 90 | `GUNPEN4` | local | 5408 | 49.93 | `v146gunaxis` | **+1.41** | [-1.44, +4.26] | **flat** | +1.02· | +1.73· | PASS(nd) (+0.61) |  |
| 91 | `SR2NULL` | local | 5408 | 49.54 | `v152null` | **+1.44** | [-1.38, +4.27] | **flat** | +0.91· | +2.56· | PASS(nd) (+0.61) |  |
| 92 | `CAP6B` | local | 5408 | 49.00 | `v146gunaxis` | **+1.45** | [-1.39, +4.29] | **flat** | +0.71· | +3.01· | PASS(nd) (-0.67) |  |
| 93 | `GUNFIRST` | local | 5408 | 49.61 | `v146gunaxis` | **+1.47** | [-1.40, +4.33] | **flat** | +0.94· | +2.56· | PASS(nd) (+0.54) |  |
| 94 | `MIX282mix5` | local | 5400 | 54.65 | `v223sealrepair` | **+1.57** | [-1.14, +4.28] | **flat** | +3.07F | -4.36· | FAIL (+6.83) | **Δ** |
| 95 | `SH288` | local | 5400 | 53.61 | `v223sealrepair` | **+1.57** | [-1.23, +4.37] | **flat** | +1.98F | -1.52· | FAIL (+5.17) | **Δ** |
| 96 | `F251PINAIM` | work-server-1 | 5400 | 49.30 | `v223sealrepair` | **+1.63** | [-1.33, +4.59] | **flat** | +1.03· | +2.99· | PASS(nd) (-0.37) |  |
| 97 | `SALTREF` | work-server-1 | 5400 | 49.11 | `v223sealrepair` | **+1.64** | [-1.29, +4.57] | **flat** | +1.01· | +3.05· | PASS(nd) (-0.39) |  |
| 98 | `AMMO115` | local | 5408 | 51.16 | `v146gunaxis` | **+1.69** | [-1.19, +4.56] | **flat** | +1.70· | +1.07· | PASS(nd) (+1.00) |  |
| 99 | `CMB296` | local | 5400 | 51.85 | `v223sealrepair` | **+1.78** | [-1.16, +4.72] | **flat** | +2.49F | -1.36· | FAIL (+3.65) | **Δ** |
| 100 | `SHIPGATENULL` | local | 5408 | 49.56 | `v169launchlate160` | **+1.81** | [-1.11, +4.72] | **flat** | +1.64· | +2.21· | PASS(nd) (-0.39) |  |
| 101 | `LAUNCHLATE160` | local | 5408 | 51.42 | `v146gunaxis` | **+1.83** | [-1.05, +4.71] | **flat** | +1.60· | +1.89· | PASS(nd) (+1.22) |  |
| 102 | `LAUNCHLATE80` | local | 5408 | 50.74 | `v146gunaxis` | **+1.94** | [-0.94, +4.81] | **flat** | +1.50· | +2.42· | PASS(nd) (+0.18) |  |
| 103 | `CAP12B` | local | 5408 | 48.93 | `v146gunaxis` | **+2.29** | [-0.62, +5.20] | **flat** | +1.50· | +4.02· | PASS(nd) (-0.04) |  |
| 104 | `GUNAXABL` | local | 5400 | 48.69 | `v223sealrepair` | **+2.30** | [-0.65, +5.24] | **flat** | +1.23· | +4.71· | PASS(nd) (-0.54) |  |
| 105 | `BODYBLK` | local | 3574 | 47.26 | `v223sealrepair` | **+2.37** | [-1.24, +5.98] | **flat** | +1.27· | +5.76· | PASS(nd) (-1.29) |  |
| 106 | `STEPOFF` | local | 2782 | 48.96 | `v197mapcode` | **+2.37** | [-1.55, +6.30] | **flat** | +1.24· | +4.49· | PASS(nd) (-0.65) |  |
| 107 | `GUNAXIS0` | local | 2752 | 49.45 | `v197mapcode` | **+2.38** | [-1.66, +6.41] | **flat** | +1.53· | +4.14· | PASS(nd) (-0.25) |  |
| 108 | `BESTFITB` | local | 5408 | 49.08 | `v146gunaxis` | **+2.58** | [-0.27, +5.44] | **flat** | +1.51· | +5.17F | PASS(nd) (-0.30) |  |
| 109 | `CMB291` | local | 5400 | 53.78 | `v223sealrepair` | **+2.66** | [-0.07, +5.39] | **flat** | +3.48F | -1.44· | FAIL (+5.91) | **Δ** |
| 110 | `F257CATMAX` | work-server-2 | 5400 | 50.65 | `v223sealrepair` | **+2.87** | [-0.01, +5.75] | **flat** | +2.79F | +1.97· | FAIL (+2.50) | **Δ** |
| 111 | `SALTROUTE` | local | 5408 | 48.74 | `v178salt` | **+2.97** | [+0.44, +5.49] | **FAIL** | +2.01F | +4.79F | PASS(nd) (-0.85) | **Δ** |
| 112 | `G400g4` | local | 3545 | 52.95 | `v223sealrepair` | **+3.27** | [-0.10, +6.64] | **flat** | +3.89F | -0.49· | FAIL (+5.78) | **Δ** |
| 113 | `GUNAX0` | local | 5408 | 48.00 | `v169launchlate160` | **+3.32** | [+0.40, +6.24] | **FAIL** | +2.01F | +6.20F | PASS (-1.90) | **Δ** |
| 114 | `GBNS` | local | 3133 | 49.70 | `v197mapcode` | **+3.40** | [-0.36, +7.16] | **flat** | +2.42· | +5.06· | PASS(nd) (+1.47) |  |
| 115 | `SENTTHRR` | work-server-2 | 5400 | 48.30 | `v223sealrepair` | **+3.45** | [+0.51, +6.39] | **FAIL** | +1.94· | +6.87F | PASS(nd) (-0.07) | **Δ** |
| 116 | `SH287` | local | 5400 | 55.20 | `v223sealrepair` | **+3.45** | [+0.89, +6.02] | **FAIL** | +4.22F | -1.95· | FAIL (+8.43) |  |
| 117 | `SCREEN` | local | 5408 | 48.84 | `v169launchlate160` | **+3.49** | [+0.60, +6.38] | **FAIL** | +2.25F | +6.17F | PASS(nd) (-0.07) | **Δ** |
| 118 | `RNDSPAWN` | work-server-2 | 5400 | 51.87 | `v223sealrepair` | **+3.61** | [+0.91, +6.30] | **FAIL** | +3.57F | +2.56· | FAIL (+4.96) |  |
| 119 | `SHIPGATE0` | local | 3089 | 49.27 | `v169launchlate160` | **+3.92** | [+0.02, +7.83] | **FAIL** | +2.58· | +6.65· | PASS(nd) (+0.10) | **Δ** |
| 120 | `SCREEN4` | local | 5408 | 48.85 | `v169launchlate160` | **+4.38** | [+1.52, +7.24] | **FAIL** | +2.91F | +7.11F | PASS(nd) (+0.65) | **Δ** |
| 121 | `FWDFLOOR8` | local | 2788 | 45.88 | `v197mapcode` | **+4.51** | [+0.33, +8.69] | **FAIL** | +1.86· | +11.28F | PASS (-2.22) | **Δ** |
| 122 | `SPAWNLK` | work-server-1 | 5400 | 49.74 | `v223sealrepair` | **+4.75** | [+1.95, +7.54] | **FAIL** | +3.58F | +7.25F | FAIL (+1.94) |  |
| 123 | `SHIPGATE160` | local | 3048 | 49.41 | `v169launchlate160` | **+4.76** | [+0.88, +8.64] | **FAIL** | +3.40F | +7.52F | PASS(nd) (+0.89) | **Δ** |
| 124 | `MIX283mix5` | local | 5400 | 52.83 | `v223sealrepair` | **+5.08** | [+2.31, +7.85] | **FAIL** | +5.14F | +2.19· | FAIL (+6.83) |  |
| 125 | `CMB293` | local | 5400 | 54.48 | `v223sealrepair` | **+5.40** | [+2.84, +7.95] | **FAIL** | +5.84F | +0.92· | FAIL (+7.76) |  |
| 126 | `BOTH0` | local | 5408 | 46.43 | `v146gunaxis` | **+5.41** | [+2.56, +8.25] | **FAIL** | +2.93F | +11.39F | PASS (-1.57) | **Δ** |
| 127 | `AMMO0` | local | 5400 | 46.22 | `v197mapcode` | **+5.59** | [+2.65, +8.54] | **FAIL** | +2.93F | +12.22F | PASS (-2.07) | **Δ** |
| 128 | `SPAWNLKL` | local | 3646 | 49.70 | `v223sealrepair` | **+5.76** | [+2.42, +9.09] | **FAIL** | +4.38F | +7.16F | FAIL (+1.92) |  |
| 129 | `F254COLLARS` | work-server-1 | 3740 | 47.62 | `v223sealrepair` | **+5.98** | [+2.49, +9.47] | **FAIL** | +4.53F | +9.39F | PASS(nd) (-1.15) | **Δ** |
| 130 | `SEALFLOOR6` | local | 2737 | 47.61 | `v223sealrepair` | **+6.05** | [+1.87, +10.22] | **FAIL** | +4.30F | +9.53F | PASS(nd) (-1.39) | **Δ** |
| 131 | `MAXSTACK` | local | 5398 | 52.41 | `v223sealrepair` | **+6.23** | [+3.53, +8.93] | **FAIL** | +5.88F | +4.52· | FAIL (+6.22) |  |
| 132 | `EXILE0` | local | 5408 | 47.02 | `v146gunaxis` | **+6.23** | [+3.38, +9.07] | **FAIL** | +3.66F | +11.79F | PASS(nd) (-0.65) | **Δ** |
| 133 | `G401g5` | local | 2662 | 52.82 | `v223sealrepair` | **+6.51** | [+2.52, +10.50] | **FAIL** | +6.65F | +3.65· | FAIL (+5.97) |  |
| 134 | `CMB290` | local | 5400 | 51.96 | `v223sealrepair` | **+7.18** | [+4.56, +9.79] | **FAIL** | +5.73F | +7.31F | FAIL (+5.33) |  |
| 135 | `MINHARV1` | local | 5408 | 47.24 | `v169launchlate160` | **+7.61** | [+4.85, +10.38] | **FAIL** | +4.49F | +14.92F | PASS (-1.85) | **Δ** |
| 136 | `PINRND1` | work-server-2 | 5405 | 47.59 | `v223sealrepair` | **+8.69** | [+5.78, +11.59] | **FAIL** | +6.16F | +13.83F | FAIL (+1.78) |  |
| 137 | `LAUNCH3` | local | 5408 | 43.73 | `v146gunaxis` | **+9.24** | [+6.43, +12.05] | **FAIL** | +4.91F | +19.83F | PASS (-2.92) | **Δ** |
| 138 | `CMB294` | local | 2723 | 50.68 | `v223sealrepair` | **+9.30** | [+5.57, +13.03] | **FAIL** | +7.37F | +10.86F | FAIL (+4.44) |  |
| 139 | `LAUNCH2` | local | 5408 | 44.67 | `v146gunaxis` | **+9.43** | [+6.55, +12.31] | **FAIL** | +5.08F | +19.77F | PASS (-1.57) | **Δ** |
| 140 | `SH289` | local | 5400 | 52.07 | `v223sealrepair` | **+10.86** | [+8.33, +13.40] | **FAIL** | +9.17F | +11.60F | FAIL (+7.85) |  |
| 141 | `F232SEALTEM` | work-server-1 | 5400 | 45.54 | `v223sealrepair` | **+10.98** | [+7.98, +13.97] | **FAIL** | +7.01F | +19.23F | PASS(nd) (-0.54) | **Δ** |
| 142 | `NEG123` | local | 2529 | 43.26 | `v187saltidle_f` | **+12.72** | [+9.33, +16.12] | **FAIL** | +7.62F | +24.56F | PASS (-2.49) | **Δ** |
| 143 | `CMB298` | local | 4442 | 51.76 | `v223sealrepair` | **+12.78** | [+9.94, +15.63] | **FAIL** | +10.23F | +14.57F | FAIL (+7.45) |  |
| 144 | `V120` | local | 5408 | 36.15 | `v169launchlate160` | **+16.12** | [+13.46, +18.79] | **FAIL** | +9.91F | +31.12F | PASS (-10.50) | **Δ** |
| 145 | `NEG169` | local | 5408 | 40.53 | `v169launchlate160` | **+22.34** | [+19.53, +25.14] | **FAIL** | +13.68F | +41.44F | PASS (-1.83) | **Δ** |
| 146 | `IDLECULL` | local | 3774 | 33.55 | `v171late160ammo` | **+26.84** | [+23.27, +30.41] | **FAIL** | +14.47F | +56.28F | PASS (-6.97) | **Δ** |
| 147 | `NEG114` | local | 5408 | 36.32 | `v146gunaxis` | **+33.27** | [+30.51, +36.03] | **FAIL** | +20.72F | +60.65F | PASS (-1.66) | **Δ** |
| 148 | `NOAPPROACH` | local | 2264 | 18.55 | `v171late160ammo` | **+33.81** | [+31.36, +36.26] | **FAIL** | +19.20F | +73.40F | PASS (-40.33) | **Δ** |
| 149 | `SALTOFF` | local | 2794 | 28.85 | `v197mapcode` | **+38.05** | [+33.95, +42.16] | **FAIL** | +21.94F | +74.99F | PASS (-6.73) | **Δ** |
| 150 | `NEG125` | local | 2225 | 24.94 | `v197mapcode` | **+64.81** | [+60.45, +69.17] | **FAIL** | +42.59F | +110.93F | PASS (-4.67) | **Δ** |

---

## 5. THE ARMS THAT FAIL — WHERE THE BAR ACTUALLY BITES (38)

An arm FAILS iff its RMST₃₀₀ CI lies entirely **above** zero, i.e. the rise is **excluded-from-zero at 95%** — a properly restated exclusion, not a fail-to-find.

| shard | host | n | win% | **RMST₃₀₀** | 95% CI | @DEFF 1.25 | H250 | H400 | medkill T/C | old ITT |
|---|---|--:|--:|--:|:--:|:--:|--:|--:|--:|:--:|
| `SALTROUTE` | local | 5408 | 48.74 | **+2.97** | [+0.44, +5.49] | FAIL | +2.01 | +4.79 | 236 / 233.0 | PASS(nd) |
| `GUNAX0` | local | 5408 | 48.00 | **+3.32** | [+0.40, +6.24] | FAIL | +2.01 | +6.20 | 205 / 206 | PASS |
| `SENTTHRR` | work-server-2 | 5400 | 48.30 | **+3.45** | [+0.51, +6.39] | FAIL | +1.94 | +6.87 | 205 / 207 | PASS(nd) |
| `SH287` | local | 5400 | 55.20 | **+3.45** | [+0.89, +6.02] | FAIL | +4.22 | -1.95 | 250.0 / 209 | FAIL |
| `SCREEN` | local | 5408 | 48.84 | **+3.49** | [+0.60, +6.38] | FAIL | +2.25 | +6.17 | 207.5 / 202.0 | PASS(nd) |
| `RNDSPAWN` | work-server-2 | 5400 | 51.87 | **+3.61** | [+0.91, +6.30] | FAIL | +3.57 | +2.56 | 235.0 / 213.0 | FAIL |
| `SHIPGATE0` | local | 3089 | 49.27 | **+3.92** | [+0.02, +7.83] | flat | +2.58 | +6.65 | 204.0 / 195.0 | PASS(nd) |
| `SCREEN4` | local | 5408 | 48.85 | **+4.38** | [+1.52, +7.24] | FAIL | +2.91 | +7.11 | 213 / 200 | PASS(nd) |
| `FWDFLOOR8` | local | 2788 | 45.88 | **+4.51** | [+0.33, +8.69] | flat | +1.86 | +11.28 | 197.0 / 205.5 | PASS |
| `SPAWNLK` | work-server-1 | 5400 | 49.74 | **+4.75** | [+1.95, +7.54] | FAIL | +3.58 | +7.25 | 224.0 / 210.0 | FAIL |
| `SHIPGATE160` | local | 3048 | 49.41 | **+4.76** | [+0.88, +8.64] | FAIL | +3.40 | +7.52 | 210 / 196.0 | PASS(nd) |
| `MIX283mix5` | local | 5400 | 52.83 | **+5.08** | [+2.31, +7.85] | FAIL | +5.14 | +2.19 | 232 / 198.0 | FAIL |
| `CMB293` | local | 5400 | 54.48 | **+5.40** | [+2.84, +7.95] | FAIL | +5.84 | +0.92 | 252.0 / 209 | FAIL |
| `BOTH0` | local | 5408 | 46.43 | **+5.41** | [+2.56, +8.25] | FAIL | +2.93 | +11.39 | 206 / 208.0 | PASS |
| `AMMO0` | local | 5400 | 46.22 | **+5.59** | [+2.65, +8.54] | FAIL | +2.93 | +12.22 | 202 / 205 | PASS |
| `SPAWNLKL` | local | 3646 | 49.70 | **+5.76** | [+2.42, +9.09] | FAIL | +4.38 | +7.16 | 232.0 / 214.0 | FAIL |
| `F254COLLARS` | work-server-1 | 3740 | 47.62 | **+5.98** | [+2.49, +9.47] | FAIL | +4.53 | +9.39 | 215.0 / 205.0 | PASS(nd) |
| `SEALFLOOR6` | local | 2737 | 47.61 | **+6.05** | [+1.87, +10.22] | FAIL | +4.30 | +9.53 | 211 / 198 | PASS(nd) |
| `MAXSTACK` | local | 5398 | 52.41 | **+6.23** | [+3.53, +8.93] | FAIL | +5.88 | +4.52 | 243.0 / 201.5 | FAIL |
| `EXILE0` | local | 5408 | 47.02 | **+6.23** | [+3.38, +9.07] | FAIL | +3.66 | +11.79 | 211 / 206.0 | PASS(nd) |
| `G401g5` | local | 2662 | 52.82 | **+6.51** | [+2.52, +10.50] | FAIL | +6.65 | +3.65 | 233 / 197 | FAIL |
| `CMB290` | local | 5400 | 51.96 | **+7.18** | [+4.56, +9.79] | FAIL | +5.73 | +7.31 | 249.0 / 213 | FAIL |
| `MINHARV1` | local | 5408 | 47.24 | **+7.61** | [+4.85, +10.38] | FAIL | +4.49 | +14.92 | 216.0 / 212.0 | PASS |
| `PINRND1` | work-server-2 | 5405 | 47.59 | **+8.69** | [+5.78, +11.59] | FAIL | +6.16 | +13.83 | 215.0 / 199 | FAIL |
| `LAUNCH3` | local | 5408 | 43.73 | **+9.24** | [+6.43, +12.05] | FAIL | +4.91 | +19.83 | 207.0 / 211 | PASS |
| `CMB294` | local | 2723 | 50.68 | **+9.30** | [+5.57, +13.03] | FAIL | +7.37 | +10.86 | 249.5 / 209 | FAIL |
| `LAUNCH2` | local | 5408 | 44.67 | **+9.43** | [+6.55, +12.31] | FAIL | +5.08 | +19.77 | 203.0 / 205.0 | PASS |
| `SH289` | local | 5400 | 52.07 | **+10.86** | [+8.33, +13.40] | FAIL | +9.17 | +11.60 | 260.0 / 208.0 | FAIL |
| `F232SEALTEM` | work-server-1 | 5400 | 45.54 | **+10.98** | [+7.98, +13.97] | FAIL | +7.01 | +19.23 | 206 / 200 | PASS(nd) |
| `NEG123` | local | 2529 | 43.26 | **+12.72** | [+9.33, +16.12] | FAIL | +7.62 | +24.56 | 224 / 214.5 | PASS |
| `CMB298` | local | 4442 | 51.76 | **+12.78** | [+9.94, +15.63] | FAIL | +10.23 | +14.57 | 259.0 / 201 | FAIL |
| `V120` | local | 5408 | 36.15 | **+16.12** | [+13.46, +18.79] | FAIL | +9.91 | +31.12 | 213 / 227 | PASS |
| `NEG169` | local | 5408 | 40.53 | **+22.34** | [+19.53, +25.14] | FAIL | +13.68 | +41.44 | 216.0 / 199.5 | PASS |
| `IDLECULL` | local | 3774 | 33.55 | **+26.84** | [+23.27, +30.41] | FAIL | +14.47 | +56.28 | 171 / 195.0 | PASS |
| `NEG114` | local | 5408 | 36.32 | **+33.27** | [+30.51, +36.03] | FAIL | +20.72 | +60.65 | 226.0 / 194 | PASS |
| `NOAPPROACH` | local | 2264 | 18.55 | **+33.81** | [+31.36, +36.26] | FAIL | +19.20 | +73.40 | 270.0 / 325 | PASS |
| `SALTOFF` | local | 2794 | 28.85 | **+38.05** | [+33.95, +42.16] | FAIL | +21.94 | +74.99 | 188.0 / 196 | PASS |
| `NEG125` | local | 2225 | 24.94 | **+64.81** | [+60.45, +69.17] | FAIL | +42.59 | +110.93 | 213 / 164 | PASS |

**Split by control generation** — this is the cut that matters for anything shippable:

| class | arms | FAIL | FASTER | flat |
|---|--:|--:|--:|--:|
| **current control `_v223sealrepair`** | 52 | **17** | 4 | 31 |
| superseded controls (7 distinct) | 98 | **21** | 23 | 54 |

⚠ **`NOAPPROACH` remains the only arm on the board whose CONTROL leg has a median kill round past r300** (medT 270 / med**C** 325) — unchanged from the superseded scan, and it is the control that crosses, not the treatment. The gross median backstop is still essentially never the binding constraint; the RMST contrast is.

---

## 6. THE ARMS THAT ARE SIGNIFICANTLY FASTER (27)

| # | shard | host | n | win% | control | **RMST₃₀₀** | 95% CI | @DEFF 1.25 | H250 | H400 | old ITT |
|--:|---|---|--:|--:|---|--:|:--:|:--:|--:|--:|:--:|
| 1 | `MAPCODE` | local | 4328 | 73.27 | `v187saltidle_f` | **-60.81** | [-63.96, -57.67] | FASTER | -39.92 | -104.65 | FAIL |
| 2 | `SALTIDLE2` | local | 5408 | 64.57 | `v169launchlate160` | **-24.27** | [-26.98, -21.57] | FASTER | -13.75 | -49.33 | FAIL |
| 3 | `SALTNOBLOCK` | local | 5408 | 61.35 | `v169launchlate160` | **-16.92** | [-19.67, -14.16] | FASTER | -9.35 | -34.53 | FAIL |
| 4 | `SEALREPAIR` | local | 5396 | 59.30 | `v218mapfix` | **-15.90** | [-18.80, -12.99] | FASTER | -9.40 | -31.18 | FAIL |
| 5 | `MAPFIX2` | local | 2159 | 57.53 | `v197mapcode` | **-15.77** | [-19.89, -11.66] | FASTER | -10.22 | -29.57 | FAIL |
| 6 | `SALT` | local | 5408 | 61.00 | `v169launchlate160` | **-15.15** | [-17.87, -12.44] | FASTER | -8.25 | -32.65 | FAIL |
| 7 | `SALTREP` | local | 5408 | 60.56 | `v169launchlate160` | **-14.97** | [-17.70, -12.24] | FASTER | -7.93 | -31.59 | FAIL |
| 8 | `IDLEVSALT2` | local | 2545 | 56.82 | `v178salt` | **-14.00** | [-17.14, -10.86] | FASTER | -8.47 | -26.32 | FAIL |
| 9 | `SALTCUTONLY` | local | 5408 | 60.80 | `v169launchlate160` | **-13.83** | [-16.61, -11.05] | FASTER | -7.29 | -29.88 | FAIL |
| 10 | `SEALREPAIRR` | work-server-1 | 5394 | 56.77 | `v218mapfix` | **-11.31** | [-14.19, -8.43] | FASTER | -6.68 | -21.58 | FAIL |
| 11 | `MAPFIX` | local | 2160 | 55.65 | `v197mapcode` | **-10.78** | [-14.91, -6.66] | FASTER | -6.76 | -22.26 | FAIL |
| 12 | `IDLEVSALT` | local | 5408 | 55.99 | `v178salt` | **-9.68** | [-12.25, -7.11] | FASTER | -5.63 | -19.92 | FAIL |
| 13 | `BODYAWRR` | work-server-2 | 5400 | 54.89 | `v223sealrepair` | **-8.89** | [-11.82, -5.96] | FASTER | -5.80 | -15.64 | FAIL |
| 14 | `L4REPAIR2` | local | 5395 | 54.88 | `v197mapcode` | **-8.63** | [-11.53, -5.74] | FASTER | -5.26 | -16.21 | FAIL |
| 15 | `BODYAWR` | local | 10800 | 53.70 | `v223sealrepair` | **-6.84** | [-8.93, -4.75] | FASTER | -4.55 | -12.16 | FAIL |
| 16 | `AWRLNCH` | local | 5399 | 53.95 | `v223sealrepair` | **-6.43** | [-9.34, -3.53] | FASTER | -3.28 | -14.14 | FAIL |
| 17 | `LATE160AMMO` | local | 5408 | 53.31 | `x3r0_v115` | **-6.29** | [-9.21, -3.38] | FASTER | -3.91 | -11.06 | PASS(nd) |
| 18 | `SEALFLOOR0R` | work-server-1 | 5347 | 53.66 | `v197mapcode` | **-5.09** | [-7.91, -2.27] | FASTER | -3.21 | -10.11 | FAIL |
| 19 | `SEALFLOOR0` | local | 5396 | 54.78 | `v197mapcode` | **-4.80** | [-7.67, -1.92] | FASTER | -2.65 | -10.66 | FAIL |
| 20 | `APPRLAUNCH` | local | 5400 | 52.94 | `v197mapcode` | **-4.75** | [-7.61, -1.89] | FASTER | -2.61 | -9.57 | PASS(nd) |
| 21 | `APPRLAUNCH2` | local | 5400 | 52.39 | `v197mapcode` | **-4.33** | [-7.16, -1.50] | FASTER | -2.54 | -9.03 | FAIL |
| 22 | `BURST64B` | local | 5408 | 51.04 | `v171late160ammo` | **-3.60** | [-6.57, -0.63] | FASTER | -2.53 | -5.21 | PASS(nd) |
| 23 | `ZEROAMMO` | local | 5408 | 52.90 | `x3r0_v115` | **-3.53** | [-6.43, -0.63] | FASTER | -2.02 | -7.63 | PASS(nd) |
| 24 | `L4REPAIR` | local | 5408 | 51.28 | `v169launchlate160` | **-3.12** | [-6.04, -0.21] | flat | -2.13 | -5.09 | PASS(nd) |
| 25 | `SR1CUR` | local | 5408 | 51.37 | `v148ferryfirst` | **-3.12** | [-5.95, -0.29] | flat | -1.88 | -5.96 | PASS(nd) |
| 26 | `GUNAXREP` | local | 5408 | 52.31 | `v148ferryfirst` | **-3.07** | [-5.93, -0.20] | flat | -1.56 | -6.88 | FAIL |
| 27 | `SALTREF2` | work-server-1 | 5400 | 51.78 | `v223sealrepair` | **-3.04** | [-5.98, -0.10] | flat | -1.83 | -5.97 | PASS(nd) |

### 6.1 Is there anything faster than `BODYAWR` (−6.84) and `AWRLNCH` (−6.43)? Yes — 16 arms. And that is the wrong reading.

⛔ **CROSS-ARM RANKING ON THE RAW BOARD IS NOT A LEAD BOARD, BECAUSE EACH ARM CARRIES ITS OWN DECLARED CONTROL AND THE CONTROLS ARE A LINEAGE.** The 150 arms run against **12 distinct controls**; the four biggest classes are `_v223sealrepair` (52 arms — the current incumbent), `_v146gunaxis` (26), `_v197mapcode` (25) and `_v169launchlate160` (19).

The lineage is `v169launchlate160 → v178salt → v187saltidle_f → v197mapcode → v218mapfix → v223sealrepair → v242bodyaware / v267awrlnch / v280+`. **Every arm faster than `BODYAWR` is measured against an ANCESTOR of the current control** — `MAPCODE` −60.81 vs `v187saltidle_f`, `SALTIDLE2` −24.27 vs `v169launchlate160`, `SEALREPAIR` −15.90 vs `v218mapfix`. **Those are generation gains already banked into the bot we ship. They are history, not leads** — which is exactly why `MAPCODE` is the designated positive control rather than a candidate.

### 6.2 ⭐ THE COMPARABLE CLASS: 52 arms against the current control `_v223sealrepair`

**Max win share in this class is 55.24% (`MIX280mix4`) — the board ceiling the brief cites, confirmed. Within it only FOUR arms are significantly faster:**

| shard | treatment | n | win% | **RMST₃₀₀** | 95% CI | @DEFF 1.25 | H250 | H400 |
|---|---|--:|--:|--:|:--:|:--:|--:|--:|
| `BODYAWRR` | `v242bodyaware` | 5400 | 54.89 | **-8.89** | [-11.82, -5.96] | FASTER | -5.80 | -15.64 |
| `BODYAWR` | `v242bodyaware` | 10800 | 53.70 | **-6.84** | [-8.93, -4.75] | FASTER | -4.55 | -12.16 |
| `AWRLNCH` | `v267awrlnch` | 5399 | 53.95 | **-6.43** | [-9.34, -3.53] | FASTER | -3.28 | -14.14 |
| `SALTREF2` | `v231saltref` | 5400 | 51.78 | **-3.04** | [-5.98, -0.10] | flat | -1.83 | -5.97 |

**`BODYAWRR` and `BODYAWR` are the SAME treatment/control pair (`_v242bodyaware` vs `_v223sealrepair`) run on two independent hosts — a replication, not two findings.** Pooled over **n = 16,200 games**:

| horizon | pooled RMST | 95% CI (paired, DEFF 0.98) | verdict |
|---|--:|:--:|:--:|
| H=250 | **-4.96** | [-6.12, -3.81] | FASTER |
| **H=300** | **-7.52** | [-9.23, -5.82] | **FASTER** |
| H=400 | **-13.32** | [-16.24, -10.40] | FASTER |

**Sign-stable at every horizon, replicated across two hosts, and the largest sample on the board. This is the strongest kill-speed result the local fixture currently holds against the shipped control.** `AWRLNCH` (`_v267awrlnch`, −6.43) is a second arm of the same family and is likewise sign-stable.

⚠ **The one genuinely NEW name this rescan surfaces is `SALTREF2`** (`_v231saltref`, n=5,400, win 51.78%, **−3.04 [−5.98, −0.10]**) — read `PASS(nd)`/flat by the superseded form. **It is the weakest arm on the FASTER list and it does NOT survive DEFF 1.25 (§8), so it is a lead to power up, not a result to bank.**

⚠ **AND THE HONEST FRAMING FOR THE 60% GATE: none of this is a win-share lead.** The four faster arms in the comparable class win 51.78–54.89%, all below the 55.24% ceiling. **`_v242bodyaware` buys ~7.5 rounds of kill speed, not games.** Whether that is worth anything is a question for the live surface — `PRIMARY_CURRENCY: game_share` is not what this estimator measures, and §9.1 states the limit.

---

## 7. HORIZON-FRAGILE ARMS (30 of 150)

An arm is **horizon-fragile** if its verdict label is not identical at H=250, H=300 and H=400. H=300 is a chosen constant; a verdict that exists only at one horizon is fragile by construction and must not be banked as if it were robust.

| shard | n | win% | H=250 | H=300 | H=400 | pattern |
|---|--:|--:|--:|--:|--:|---|
| `GUNAXREP` | 5408 | 52.31 | -1.56 · | -3.07 < | -6.88 < | · → < → < |
| `SALTREF2` | 5400 | 51.78 | -1.83 · | -3.04 < | -5.97 < | · → < → < |
| `GUNBLANK` | 5408 | 52.11 | -1.31 · | -2.78 · | -6.06 < | · → · → < |
| `FERRY0` | 5408 | 50.15 | -2.23 < | -2.63 · | -2.69 · | < → · → · |
| `SR2CUR` | 5408 | 50.98 | -1.90 < | -2.55 · | -3.47 · | < → · → · |
| `MIX285mix2` | 5400 | 54.39 | -0.62 · | -2.23 · | -6.67 < | · → · → < |
| `AWRSPAWN` | 5400 | 55.06 | +0.59 · | -1.97 · | -9.40 < | · → · → < |
| `ECORAID2` | 5400 | 52.91 | -0.87 · | -1.78 · | -5.43 < | · → · → < |
| `CMB292` | 5400 | 54.07 | -0.16 · | -1.57 · | -6.12 < | · → · → < |
| `ECORAID` | 5400 | 53.22 | -0.38 · | -1.56 · | -5.49 < | · → · → < |
| `MIX280mix4` | 5400 | 55.24 | +1.35 · | -0.87 · | -8.67 < | · → · → < |
| `TRIO` | 5807 | 54.35 | +1.46 · | -0.34 · | -6.88 < | · → · → < |
| `MIX281mix4` | 5400 | 55.07 | +1.75 · | -0.29 · | -7.43 < | · → · → < |
| `MIX284mix3` | 5400 | 54.56 | +1.87 F | +0.21 · | -5.80 < | **⛔ HARD SIGN FLIP** |
| `MIX282mix5` | 5400 | 54.65 | +3.07 F | +1.57 · | -4.36 · | F → · → · |
| `SH288` | 5400 | 53.61 | +1.98 F | +1.57 · | -1.52 · | F → · → · |
| `CMB296` | 5400 | 51.85 | +2.49 F | +1.78 · | -1.36 · | F → · → · |
| `BESTFITB` | 5408 | 49.08 | +1.51 · | +2.58 · | +5.17 F | · → · → F |
| `CMB291` | 5400 | 53.78 | +3.48 F | +2.66 · | -1.44 · | F → · → · |
| `F257CATMAX` | 5400 | 50.65 | +2.79 F | +2.87 · | +1.97 · | F → · → · |
| `G400g4` | 3545 | 52.95 | +3.89 F | +3.27 · | -0.49 · | F → · → · |
| `SENTTHRR` | 5400 | 48.30 | +1.94 · | +3.45 F | +6.87 F | · → F → F |
| `SH287` | 5400 | 55.20 | +4.22 F | +3.45 F | -1.95 · | F → F → · |
| `RNDSPAWN` | 5400 | 51.87 | +3.57 F | +3.61 F | +2.56 · | F → F → · |
| `SHIPGATE0` | 3089 | 49.27 | +2.58 · | +3.92 F | +6.65 · | · → F → · |
| `FWDFLOOR8` | 2788 | 45.88 | +1.86 · | +4.51 F | +11.28 F | · → F → F |
| `MIX283mix5` | 5400 | 52.83 | +5.14 F | +5.08 F | +2.19 · | F → F → · |
| `CMB293` | 5400 | 54.48 | +5.84 F | +5.40 F | +0.92 · | F → F → · |
| `MAXSTACK` | 5398 | 52.41 | +5.88 F | +6.23 F | +4.52 · | F → F → · |
| `G401g5` | 2662 | 52.82 | +6.65 F | +6.51 F | +3.65 · | F → F → · |

### 7.1 ⭐ THE FRAGILITY IS NOT RANDOM — IT IS ONE BOT FAMILY, AND IT DRIFTS MONOTONICALLY

**15 of the 30 fragile arms belong to the current-generation `MIX`/`CMB`/`SH`/`G4`/`TRIO` combination family**, all running against `_v223sealrepair`, and every one drifts in the **same direction**: more positive at H=250, more negative at H=400.

The mechanism is legible and is a property of the arm, not the metric: **these planks convert marginal losses and tiebreaks into SLOW wins whose kill times sit in the 300–400 band.** At H=250 those wins are censored to 250 and earn no credit; at H=400 they are credited in full. `MIX284mix3` is the only **hard sign flip** on the board — **FAIL at H=250 (+1.87), flat at H=300 (+0.21), FASTER at H=400 (−5.80)** — and `MIX280mix4`, `MIX281mix4`, `TRIO`, `CMB292`, `MIX285mix2` follow the identical shape one notch below significance at the ends.

⇒ **THE VERDICT FOR THE ENTIRE MIX/CMB FAMILY IS A PROPERTY OF WHERE THE HORIZON WAS PUT.** `PROGRAMME.md:530-531` pins the design constant at 300; that is a legitimate choice, but for this family it is **the** choice, and any prereg scoring a MIX-class plank on RMST₃₀₀ should register the H=250 and H=400 readings alongside or its verdict is one constant away from reversing.

⚠ **`TRIO` is the live instance of this.** It reads **+1.46 (H250) / −0.34 (H300) / −6.88 (H400)** — flat at the mandated horizon and FASTER at 400. This reproduces the side lane's independent recompute exactly. Its cancellation rested on two legs; the *"kills 23 rounds later"* leg is confirmed dead here at every horizon, and the power leg (could not resolve +0.55pp at n=5,808) is untouched by anything in this document.

---

## 8. DEFF SENSITIVITY (0.98 → 1.25)

**69 of 150 arms show map heterogeneity at p < 0.01 on the RMST₃₀₀ contrast** (Cochran Q over per-map means) — materially more than the 43 the superseded scan found on the binary ITT indicator, because RMST is a continuous outcome and picks up map-driven kill-time differences the indicator discards. Re-running at DEFF 1.25 changes **6 verdicts on 6 distinct arms, always toward `flat`:**

| shard | n | RMST₃₀₀ | 95% CI @0.98 | verdict @0.98 | 95% CI @1.25 | verdict @1.25 | map-het p |
|---|--:|--:|:--:|:--:|:--:|:--:|--:|
| `L4REPAIR` | 5408 | -3.12 | [-6.04, -0.21] | FASTER | [-6.42, +0.17] | flat | 3.2e-02 |
| `SR1CUR` | 5408 | -3.12 | [-5.95, -0.29] | FASTER | [-6.31, +0.08] | flat | 8.7e-01 |
| `GUNAXREP` | 5408 | -3.07 | [-5.93, -0.20] | FASTER | [-6.30, +0.17] | flat | 9.6e-01 |
| `SALTREF2` | 5400 | -3.04 | [-5.98, -0.10] | FASTER | [-6.36, +0.28] | flat | 1.7e-01 |
| `SHIPGATE0` | 3089 | +3.92 | [+0.02, +7.83] | FAIL | [-0.49, +8.33] | flat | 5.4e-03 |
| `FWDFLOOR8` | 2788 | +4.51 | [+0.33, +8.69] | FAIL | [-0.21, +9.23] | flat | 2.8e-02 |

**36 of 38 FAIL verdicts and 23 of 27 FASTER verdicts survive DEFF 1.25.** The headline counts move from 38/27 to 36/23. **No conclusion in this document depends on the DEFF choice**, and every arm affected is within ~1 round of its threshold.

Per `CLAUDE.md`'s local exemption, **0.98 is the measured local constant** (pair-weighted, ρ = −0.020 across 124 shards) and the platform constants are not imported. The 1.25 column is the cited outlier value for arms with strong map interaction and is reported for every arm in §5 and §6, not only the flippers.

---

## 9. LIMITS — WHAT THIS DOCUMENT DOES NOT ESTABLISH

### 9.1 RMST is not game share, and the bar is not the currency
`PROGRAMME.md` carries `PRIMARY_CURRENCY: game_share`. RMST₃₀₀ is the `DEFENCE_ADMISSION_BAR` estimator — an **admission gate**, not a ranking. An arm reading `FASTER` has cleared a gate; it has not been shown to win more games. Conversely the estimator **deliberately blends kill RATE with kill SPEED** (`RMST = H − rate × conditional-speed`, an exact product), so a `FASTER` reading can be bought with either factor. Both are reported per arm in the superseded scan's §3 and remain valid there.

### 9.2 The map rotation still splits the board
63 arms ran the pre-rotation 8-map array, 84 the post-rotation 15-map pool. Byte-identical nulls read **3.8% tiebreaks (`NULL114`, 8 maps) vs 31.0% (`NULL5400`, 15 maps)**. Every number here is a **within-shard** treatment-vs-control contrast on identical maps, so each contrast is clean — **but cross-arm ranking across the rotation is not, and §4's ordering must be read with §6.1's control-generation caveat, not as a league table.** `MAPFIX` (2 maps), `MAPFIX2` (2 maps) and `TINYECO62` (3 maps) have degenerate map arrays; the first two are on the FASTER list and are its two weakest members on geometry coverage.

### 9.3 Local fixture only, and no registered MDE
Local corefill batteries only; no ladder or unrated-platform games, so the two-corpus rule is not breached. `PROGRAMME.md:506-508` scores the bar against **each prereg's registered MDE**; these 150 arms predate the bar and registered none, so every verdict here is *"the CI excludes ZERO"*, which is a weaker statement than the bar will make in practice. The CI bounds are printed on every row precisely so a threshold can be tested against them when one exists.

### 9.4 No causal claim, no verdict sentence
Every label is *passes/fails **as computed** under ITT RMST₃₀₀*. Which arms are promoted, cancelled or re-queued is the builder's call, not mine. Three arms carry duplicate `(map, seed, seat, game)` keys from restarts (`LNCHERL2` 8/5,405, `NULL140B` 7/5,385, `PINRND1` 5/5,405, all ≤0.15%) — recorded, not corrected, unchanged from the superseded scan.

### 9.5 Refused arms
**59 arms refused, every one for n < 2,000 alone** (no arm lacks a declared fixture after the superseded scan's metadata recovery, which is reused verbatim here). Largest refusals:

| shard | host | n |
|---|---|--:|
| `F200SIEGELA` | work-server-1 | 1870 |
| `OSCLOCK` | local | 1867 |
| `V141VS140` | local | 1837 |
| `OSCLOCK2` | local | 1809 |
| `F258SEALMAX` | work-server-2 | 1704 |
| `NESTSHOT2` | local | 1633 |
| `LNCHERLY` | work-server-1 | 1478 |
| `V140VS145B` | work-server-1 | 1440 |
| `PAVEFIRST` | local | 1282 |
| `MAPSEAL` | local | 1201 |
| `CATSOLO` | local | 1128 |
| `X3R0V134` | local | 1116 |

**27 of the 59 refusals are under n = 500.**

---

## 10. METHOD, IN ENOUGH DETAIL TO RERUN

* **Source:** the frozen snapshot at `<session-scratch>/snap/{overnight,overnight-remote}` taken 2026-08-16T05:21:27Z by the superseded scan, reused unchanged. Mirror copies (`work-server-N` vs `worker@work-server-N`) deduped by largest file per (shard, host).
* **Fixture metadata:** `# FIXTURE` header where present (45 files), else the worklist sweep (`corefill_work.txt`, the `vps/*` lists, `loki29_spec.txt`, `fleet_queue.tsv`, each remote `worklist.txt`), plus the one prereg-only recovery (`SALTREF2` → `scratchpad/_locked_saltref2.md:4-5`). **The superseded scan's 11 recovered fixtures are reused, not re-derived.**
* **Row filter:** exactly 9 tab fields, `winner ∈ {T,C}`, `cond ∈ {core_destroyed, tiebreak}`, integer `turns`. `NOWINNER`/`-` aborts and repeated header rows dropped.
* **Estimator:** §1.1. **Variance:** one-sample variance of the per-game contrast `d_i = value(i,T) − value(i,C)`, × DEFF, ÷ n (§1.2). Z = 1.959963985.
* **Verdict labels:** `FAIL` = CI lower bound > 0 (kills later, rise excluded from zero); `FASTER` = CI upper bound < 0; `flat` = CI straddles zero (**not** an exclusion).
* **Checks run before any number was read:** win-predicate non-degeneracy in both directions (§1.1); the four required controls (§2.1); the full 9-null + 4-neg + 1-positive calibration family (§2.2); a two-branch mutation drive on three independent nulls (§2.3); the `<` vs `<=` boundary convention to 6dp (§1.3); and the arm/refusal counts reproduced against the superseded scan exactly (150 / 59).
* **Scratch artefacts** (session scratchpad, not committed): `rmst_rescan.py`, `rmst_report.py`, `mkdoc.py`, `rmst.json`.

⚠ **One clock flag, not a finding:** `RMST-ESTIMATOR-2026-08-16.md` is headed *"Written 2026-08-16T07:5xZ (`date -u`)"*, but `date -u` in this shell reads **2026-08-16T05:51:11Z** and the newest commit is `2026-08-16T07:47:04+02:00` = 05:47:04Z. The doc's header looks like local time (+02:00) labelled `Z`. **Cosmetic, and it does not touch any number — but `CLAUDE.md` records timestamp drift as a four-time repeat failure, so it is flagged rather than silently normalised.**
