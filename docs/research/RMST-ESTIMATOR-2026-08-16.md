# THE KILL-TIMING ESTIMATOR: THREE CANDIDATES, FOUR CONTROL CASES, ONE SURVIVOR

**Research arm, s45. Written 2026-08-16T07:5xZ (`date -u`). CITABLE FORM of the in-channel relays
of 07:0x–07:4xZ, committed because `LEG-fieldcal-2026-08-16` inherits these numbers.**
**Fixture: local corefill tapes, `scratchpad/overnight/*.tsv` + `scratchpad/overnight-remote/*/*.tsv`.
DEFF 0.98 (local, balanced-by-construction, per `CLAUDE.md`). Control for every arm is its own
declared `control=` from its fixture header.**

---

## 0. WHY THIS DOC EXISTS

`PROGRAMME.md` carries `DEFENCE_ADMISSION_BAR: r300_crossing_non_regression`. **Three different
estimators were proposed for it inside four hours today, by three lanes, and two of them are
broken.** This is the record of which survives and why, with the control cases that decide it.

**It also retracts two of my own claims.** Both are marked ⛔ below.

---

## 1. THE THREE CANDIDATES

    BY     = P(kill-win AND turns <= 300)          must not FALL      <- the live bar
    AFTER  = P(kill-win AND turns >  300)          must not RISE      <- superseded wording
    RMST   = mean over ALL games of min(turns,300), non-kill scoring 300   must not RISE

⛔ **`BY` and `AFTER` are NOT complements.** Non-kills (losses, tiebreaks, r1000) are in neither, so
they are genuinely different metrics and can disagree — they do, systematically, below.

**`BY` and `AFTER` both condition on a kill-win. `RMST` conditions on nothing:** every randomised
game contributes exactly one value, so no treatment effect can move its denominator.

---

## 2. ⭐⭐ THE CONTROL MATRIX — THE WHOLE ARGUMENT IS HERE

Four cases whose correct verdict is known **before** looking at any estimator.

| case | what it is | correct verdict | **BY** | **AFTER** | **RMST₃₀₀** |
|---|---|---|---|---|---|
| `NULL114` | byte-identical copy of control | **flat** | −0.09 flat ✅ | −0.15 PASS ✅ | **+0.42 [−2.0,+2.8] flat ✅** |
| `NEG114` | deliberately degraded (36.32% win) | **slower/worse** | −26.16 FAIL ✅ | **−1.66 PASS ❌** | **+33.27 [+30.9,+35.6] SLOWER ✅** |
| `NEG125` | deliberately degraded (24.94% win) | **slower/worse** | −45.03 FAIL ✅ | **−4.67 PASS ❌** | **+64.81 [+61.1,+68.5] SLOWER ✅** |
| `MAPCODE` | our **shipped** `MAP_CODES` fix, 73.27% win | **not a timing regression** | +42.63 PASS ✅ | **+2.98 FAIL ❌** | **−60.81 [−63.5,−58.1] FASTER ✅** |

⛔ **`AFTER` IS BROKEN IN BOTH DIRECTIONS.** All four NEG cells pass it — a degraded arm has few
kill-wins at all, hence few *late* ones — and our own shipped pathfinding fix **fails** it.
⚠ **`BY` gets all four right, but by correlating with quality rather than measuring timing:** the
side lane measured, over 146 shards, `corr(win-share margin, BY-diff) = +0.9663`, **r² = 0.934**,
against `corr(SPEED-diff, BY-diff) = +0.1362`. **93% of its variance is win share**, which
`PRIMARY_CURRENCY: game_share` already scores.
✅ **`RMST` gets all four right for the right reason, and `MAPCODE` at −60.81 rounds is a powerful
positive control: a genuine shipped improvement, correctly read as killing sixty rounds earlier.**

---

## 2b. ⛔ INSTRUMENT CORRECTION — THE INTERVALS BELOW WERE ~18% TOO NARROW. FIXED.

*Found by the RMST₃₀₀ board re-scan, 2026-08-16 ~09:0xZ. Verified here before adoption.*

**RMST is a PAIRED estimator on this fixture and I computed it as an independent two-sample one.**
In a corefill shard **treatment and control play the SAME game** — one row, one winner — so `rT` and
`rC` are two values from a single observation and are strongly **negatively** correlated
(measured **corr ≈ −0.35 to −0.44**, mean −0.40, across every arm). With negative covariance
`Var(rT − rC) = Var(rT) + Var(rC) − 2·Cov` is **LARGER** than the independent sum, so the correct
intervals are **WIDER**, by a measured factor of **1.16–1.20×**.

| shard | diff | independent 95% (WRONG) | **paired 95% (CORRECT)** | corr | width × |
|---|---|---|---|---|---|
| `NULL114` | +0.42 | [−1.96, +2.81] ns | **[−2.43, +3.28] ns** | −0.43 | 1.20 |
| `BODYAWR` | −6.84 | [−8.61, −5.08] sig | **[−8.93, −4.75] sig** | −0.40 | 1.18 |
| `AWRLNCH` | −6.43 | [−8.88, −3.99] sig | **[−9.34, −3.53] sig** | −0.40 | 1.19 |
| `MIX280mix4` | −0.87 | [−3.18, +1.43] ns | **[−3.56, +1.82] ns** | −0.36 | 1.17 |
| `MIX281mix4` | −0.29 | [−2.56, +1.99] ns | **[−2.94, +2.36] ns** | −0.35 | 1.16 |
| `MIX284mix3` | +0.21 | [−2.09, +2.51] ns | **[−2.48, +2.90] ns** | −0.37 | 1.17 |
| `NEG114` | +33.27 | [+30.93, +35.61] sig | **[+30.51, +36.03] sig** | −0.41 | 1.18 |
| `EXILE0` | +6.23 | [+3.85, +8.61] sig | **[+3.38, +9.07] sig** | −0.43 | 1.19 |
| **`GUNBLANK`** | −2.78 | [−5.21, −0.36] **sig** | **[−5.70, +0.13] ns** | −0.44 | 1.20 |

⇒ **EXACTLY ONE VERDICT IN THIS DOC CHANGES: `GUNBLANK` goes from significantly FASTER to NOT
SIGNIFICANT.** Every other conclusion — both retractions, the four-case control matrix, `BODYAWR`
and `AWRLNCH` faster, the 55-class flat, `NEG114` slower — **survives the correction unchanged**,
because those effects are far from their boundaries.
⚠ **The direction of the error is the unflattering one: I published intervals that were too narrow,
i.e. too easy to call significant.** ⭐ **The point estimates were never affected** — pairing changes
the variance, not the mean — **which is why the re-scan reproduced my numbers digit-for-digit and
still had to correct me. A reproduction is not a validation of the interval.**
**USE THE PAIRED FORM: `hw = 1.96 · sd(rT − rC) · sqrt(DEFF/n)`.**

## 3. THE BOARD UNDER RMST — AND ⛔ MY FIRST RETRACTION

| shard | n | **RMST₃₀₀ diff** | 95% (DEFF 0.98) | `SPEED` (biased) | verdict |
|---|---|---|---|---|---|
| `NULL114` | 5,408 | +0.42 | [−1.96, +2.81] | +0.19 | flat |
| `BODYAWR` | 10,800 | **−6.84** | [−8.61, −5.08] | −1.87 | **FASTER** |
| `AWRLNCH` | 5,400 | **−6.43** | [−8.88, −3.99] | −0.23 | **FASTER** |
| `MIX280mix4` | 5,400 | −0.87 | [−3.18, +1.43] | −4.85 | flat |
| `MIX281mix4` | 5,400 | −0.29 | [−2.56, +1.99] | −6.84 | flat |
| `MIX284mix3` | 5,400 | +0.21 | [−2.09, +2.51] | −6.35 | flat |
| `RND1SOLO` | 5,400 | +0.40 | [−2.02, +2.82] | −2.32 | flat |
| `GUNBLANK` | 5,408 | −2.78 | [−5.21, −0.36] | +0.40 | FASTER |
| `LAUNCH0` | 5,408 | −1.16 | [−3.59, +1.28] | +0.19 | flat |
| `EXILE0` | 5,408 | +6.23 | [+3.85, +8.61] | −1.51 | SLOWER |
| `NEG114` | 5,408 | +33.27 | [+30.93, +35.61] | −11.09 | SLOWER |
| `TRIO` | 5,808 | **−0.34** | (side lane, independent) | — | **flat** |

*(`TRIO` added by the side lane's independent recompute: H250 **+1.46**, H300 **−0.34**, H400
**−6.88** — flat, against a **conditioned median of +23**. ⛔ **`TRIO` was cancelled today with
"kills 23 rounds later" as one of two stated legs. That leg is the artefact. Its other leg — it
could not resolve +0.55pp over `bodyaware` at n=5,808 — is a power argument and stands
independently, so the cancellation holds and one of its reasons does not.*)

⛔ **RETRACTION 1 — "THE 55-CLASS KILLS +17–43 ROUNDS LATER" IS A CONDITIONING ARTEFACT.**
Under the unbiased estimator the leaders are **FLAT** (−0.87 to +0.21), and `BODYAWR`/`AWRLNCH` are
**significantly FASTER**. **RMST scores a loss as the full horizon, so converting a loss into a slow
win is correctly an IMPROVEMENT** — which is exactly what the MIX arms do, and why every
kill-win-conditioned metric read them as slowing.
**This framing cancelled `TRIO`, sits in `QUEUE #71`'s amendment, drove the bar re-pricing, and I
relayed it to the builder and to Magnus. It does not survive.**

⛔ **RETRACTION 2 — "THE BAR PASSES THE ARMS IT EXISTS TO CATCH" IS WITHDRAWN.** There are no such
arms among the leaders; the delay was never there. **What survives from that analysis is the
statement about the ESTIMATOR — the exact factorisation `BY = RATE × SPEED`, and the implicit
exchange rate of 1.57pp of speed per 1pp of rate (stable 1.52–1.62 across every arm). That remains
true and it no longer implicates any shipped arm.**

⚠ **HORIZON SENSITIVITY — the only thing that could revive the old reading, so it is stated:**

| arm | H=250 | H=300 | H=400 |
|---|---|---|---|
| `MIX280mix4` | +1.35 | −0.87 | −8.67 |
| `MIX281mix4` | +1.75 | −0.29 | −7.43 |
| `MIX284mix3` | +1.87 | +0.21 | −5.80 |
| `BODYAWR` | −4.55 | −6.84 | −12.16 |
| `AWRLNCH` | −3.28 | −6.43 | −14.13 |
| `NULL114` | +0.54 | +0.42 | +0.40 |
| `NEG114` | +20.72 | +33.27 | +60.65 |

**The MIX arms are marginally slower under a tight window and faster under a loose one. At NO
horizon are they +17–43 rounds slower.** `BODYAWR`, `AWRLNCH`, `NULL114` and `NEG114` are
sign-stable across all three.
✅ **BOUNDARY CONVENTION DECLARED: `<300` and `<=300` are identical to 2dp on every arm.** Checked
rather than asserted — this is the defect the side lane caught in the hazard doc earlier today,
where the analogous choice flipped a sign.

---

## 4. WHY `SPEED` WAS ALSO WRONG — AND IT WAS MY PROPOSAL

I proposed binding the bar on `SPEED` = P(kill ≤300 | won by kill). **The side lane refuted it and
they were right.** `SPEED`'s two denominators are each side's own kill-wins, which the treatment
moves:

| shard | kill-wins T | kill-wins C | denominator asymmetry | `SPEED` diff |
|---|---|---|---|---|
| `NULL114` | 2,595 | 2,608 | **−0.5%** | +0.19 |
| `BODYAWR` | 5,441 | 4,671 | +16.5% | −1.87 |
| `MIX281mix4` | 2,827 | 2,203 | **+28.3%** | −6.84 |

**`corr(denominator asymmetry, SPEED diff) = −0.79` across winning arms.** A plank converting
marginal LOSSES into WINS adds precisely the hard, slow games to its own numerator. ⇒ **a
successful plank must look slower on `SPEED` for a reason unrelated to slowing anything.**
✅ **`NULL114` is the control that proves it: −0.5% asymmetry, `SPEED` +0.19. No asymmetry, no bias.**

---

## 5. RECOMMENDATION

**Score `DEFENCE_ADMISSION_BAR` on ITT RMST₃₀₀.** It is the only candidate that is **unbiased** and
**timing-sensitive**, and the only one that gets all four control cases right. Report the `BY` rate
beside it as a descriptive volume figure.
⛔ **This instrument was built at 05:0xZ for `FIRE ORDER #1` and then reached past — twice, by me,
once toward `SPEED` and once toward defending `BY`.** The side lane's phrasing is exact: *"you built
it and then reached past it."*

---

## 6. LIMITS
1. **Local fixture only.** Platform (rated/unrated) games cluster differently; a live leg must
   re-measure DEFF on its own games. The rated-tape analogue of this metric had sd 74.59 and DEFF
   1.145 at H=300 (n=525 games / 105 matches).
2. **RMST is a mean over a censored distribution** — it deliberately blends kill RATE with kill
   SPEED, and the blend is an **exact product** (`RMST = H − rate × conditional-speed`, residual
   0.0000000000). That is a feature here: both factors are recoverable and reportable.
3. **The 150-arm board scan (`R300-BAR-BOARD-SCAN-2026-08-16.md`) scores the `AFTER` orientation**,
   because I briefed it with the then-live wording. **Its 46/58 fail counts must NOT be read
   against the current bar.** Its NULL calibration, its 11 recovered undeclared fixtures and its
   mutation drive are orientation-independent and stand.
4. Not computed: cross-arm ranking. **The map rotation puts NULL tiebreak rates at 3.8% vs 31.0%
   across eras**, so arms from different eras are not comparable on tiebreak-sensitive quantities.

## PROVENANCE
Local tapes read directly (`winner` is `T`/`C`, verified non-degenerate — `winner == seat` returns a
constant 0.00% and was the failure mode in a first pass elsewhere). Side-lane certifications:
factorisation exact to 0.0000000000 across 146 shards; `r² = 0.934`; the `SPEED` collider mechanism
and its `NULL114` control. Builder's mutation drive (+100 rounds, rate held fixed, 1,868 changed
rows) → −9.67pp [−11.18, −8.15]. Timestamps from `date -u`.
