# R300 BAR — BOARD SCAN OF EVERY COMPLETED LOCAL ARM

**Written 2026-08-16T05:28:07Z (`date -u`, same shell). Data frozen by snapshot at
2026-08-16T05:21:27Z** — `scratchpad/overnight/*.tsv` and
`scratchpad/overnight-remote/*/*.tsv` were copied to a scratch snapshot before any
number was computed, because corefill is live and two consecutive reads of the
unfrozen tree disagreed. Every figure below is as-of that instant.

**Read-only scan. No bot, no match, no queue/programme/results file touched.**

---

## 0. WHAT THE BAR SAYS — THEIR WORDS, NOT MINE

`PROGRAMME.md:21` parses `DEFENCE_ADMISSION_BAR: r300_crossing_non_regression`.
The operational form (`PROGRAMME.md:422-434`, re-priced 2026-08-16T05:15:45Z on
Magnus's direct ruling, mirrored in `CLAUDE.md:390-398`):

> a plank is off-programme if it pushes kills PAST r300 — operationally, the share
> of its kill-wins landing after r300 must not rise vs control (each prereg
> registers its own n/MDE for this, and per the exclusion-restatement rule the
> claim is scored as "the CI excludes the registered rise", never as a bare
> fail-to-find), with median-kill-round-crosses-300 as a gross backstop. **Drift
> inside r200-300 is REPORTED, no longer DISQUALIFYING.**

**This matches the task brief I was given.** One documentation flag, not a
disagreement: `PROGRAMME.md:410` still says in prose *"declared in the parsed block
at the top of this file as `DEFENCE_ADMISSION_BAR: kill_round_non_regression`"*.
That sentence is stale — it is superseded twelve lines later by the re-pricing
block, and it is inline prose (not four-space indented) so `gate.py` does not parse
it as a second field declaration. **Cosmetic, but it is exactly the failure mode
`PROGRAMME.md:411-414` warns about, one indent away from being live.**

---

## 1. HEADLINE

**150 arms scored** (n ≥ 2,000 each, **741,902 clean games** total). **59 arms refused.**

| | AS-WRITTEN | ITT |
|---|--:|--:|
| **FAIL** (rise established at 95%) | **46** | **58** |
| PASS (fall established at 95%) | 7 | 17 |
| PASS(nd) (CI straddles zero — *no rise detected*, **not** an exclusion) | 97 | 75 |

**26 of 150 arms (17.3%) FLIP between the two readings of the same sentence.**
A further 13 change verdict *strength* without crossing the pass/fail line.
**39 arms FAIL both forms; 85 pass both.**

**Gross backstop: 1 arm of 150 has any median kill round past r300** —
`NOAPPROACH` (medT 270, med**C** 325; it is the *control* leg,
`bots/_v171late160ammo`, that crosses). Max median kill round across all 150
treatment arms is **270**. **The backstop is essentially never the binding
constraint on this board; the share test is.**

### THE FLIP LIST (the single most useful output — full table in §3)

**19 arms: AS-WRITTEN PASS → ITT FAIL.** Mean win share **57.2%**.
`SALT` · `SALTNOBLOCK` · `SALTREP` · `SALTIDLE2` · `SEALREPAIR` · `SEALREPAIRR` ·
`MAPFIX` · `MAPFIX2` · `MAPCODE` · `IDLEVSALT` · `IDLEVSALT2` · `BODYAWRR` ·
`SALTCLEAR` · `AWRLNCH` · `RND1SOLO` · `NULLSALT` · `GUNAXREP` · `L4REPAIR2` ·
`APPRLAUNCH2`

**7 arms: AS-WRITTEN FAIL → ITT PASS.** Mean win share **39.2%**.
`NEG114` · `NEG125` · `NEG169` · `SALTOFF` · `F232SEALTEM` · `SCREEN4` · `GBNS`

(Board mean win share: 50.6%.)

**⭐ THE FLIP IS NOT NOISE AND IT IS NOT SYMMETRIC. IT IS SORTED BY WIN SHARE.**
Everything that flips *into* failure under ITT is a **winning** arm; everything
that flips *out of* failure under ITT is a **losing** arm — and that second group
contains **three of this repo's four deliberately-degraded NEG calibration cells**
(the fourth, `NEG123`, does not flip only because it never reached `FAIL` under
AS-WRITTEN — it too scores an established `PASS` under ITT).
§2 measures why.

---

## 2. THE TWO FORMS MEASURE DIFFERENT THINGS, AND ONE OF THEM IS MOSTLY WIN RATE

### 2.1 The identity

Write, per arm, over the same n games:

* **p** = kill-wins / n — *how often this side kills at all* (VOLUME)
* **q** = share of those kill-wins landing after r300 — *the timing shape* (SHAPE)

Then:

```
AS-WRITTEN difference  =  Δq                                  (pure SHAPE)
ITT difference         =  Δ(p·q)  =  q̄·Δp  +  p̄·Δq            (VOLUME + SHAPE)
                                     └VOLUME┘  └SHAPE┘
```

The decomposition is exact (asserted to 1e-12 for all 150 arms) and both channels
are printed in the tables below.

### 2.2 What that means empirically — correlation with the arm's own win share, across 150 arms

| quantity | r with treatment win share |
|---|--:|
| **ITT difference** | **+0.776** |
| VOLUME channel | +0.949 |
| AS-WRITTEN difference | **+0.113** |
| SHAPE channel | +0.077 |
| AS-WRITTEN vs ITT (each other) | +0.690 |

**⛔ THE ITT FORM IS 60% EXPLAINED BY HOW MUCH THE ARM WINS (r² = 0.60). It is
dominated by its VOLUME channel, which is a win-rate proxy (r = +0.949).** An arm
that wins +10pp more games mechanically produces more late kill-wins per game even
if its kill-time distribution is byte-for-byte unchanged. **The ITT form as literally
worded penalises winning.**

**The collider objection to AS-WRITTEN is real and I am not dismissing it.** Δq is
computed on the set of games each side happened to win, and that set is downstream
of the treatment. `NEG114` is the clean demonstration: it loses **26.2pp** of its
early kill-wins, so the wins it still has are the slow grinding tail, and its Δq
reads **+11.09pp (FAIL)** partly through selection. **Both forms are confounded.
They are confounded in opposite directions and the arms where that matters are
exactly the 26 flips.**

### 2.3 The complement that adjudicates the direction

`EARLY` = share of ALL games that are a kill-win at **turns ≤ 300**, treatment minus
control. It is an algebraic re-expression, not independent evidence
(`EARLY_diff + ITT_diff = Δp`, asserted exactly) — its value is that it puts the
volume channel in the same units and makes the sign legible. **A plank that is
genuinely "pushing kills past r300" must LOSE early kill-wins.**

| shard | host | EARLY Δpp (kill-win ≤ r300) | 95% CI | EARLY reads | AS-WRITTEN | ITT |
|---|---|--:|:--:|:--:|:--:|:--:|
| `SALTOFF` | local | -34.54 | [-37.50, -31.58] | FAIL | FAIL | PASS |
| `SALT` | local | +15.24 | [+13.11, +17.37] | PASS | PASS(nd) | FAIL |
| `SALTNOBLOCK` | local | +15.87 | [+13.73, +18.00] | PASS | PASS(nd) | FAIL |
| `SALTREP` | local | +14.92 | [+12.79, +17.05] | PASS | PASS(nd) | FAIL |
| `SALTIDLE2` | local | +23.21 | [+21.09, +25.33] | PASS | PASS | FAIL |
| `SEALREPAIR` | local | +13.51 | [+11.33, +15.69] | PASS | PASS(nd) | FAIL |
| `MAPFIX2` | local | +11.95 | [+8.76, +15.14] | PASS | PASS(nd) | FAIL |
| `NEG125` | local | -45.03 | [-48.13, -41.94] | FAIL | FAIL | PASS |
| `SEALREPAIRR` | work-server-1 | +9.58 | [+7.41, +11.76] | PASS | PASS(nd) | FAIL |
| `MAPFIX` | local | +9.40 | [+6.22, +12.57] | PASS | PASS(nd) | FAIL |
| `BODYAWRR` | work-server-2 | +6.19 | [+3.98, +8.39] | PASS | PASS(nd) | FAIL |
| `IDLEVSALT` | local | +9.17 | [+7.08, +11.26] | PASS | PASS(nd) | FAIL |
| `MAPCODE` | local | +42.63 | [+40.38, +44.88] | PASS | PASS | FAIL |
| `SALTCLEAR` | local | +2.48 | [+0.40, +4.56] | PASS | PASS(nd) | FAIL |
| `AWRLNCH` | local | +6.96 | [+4.74, +9.19] | PASS | PASS(nd) | FAIL |
| `RND1SOLO` | local | +1.52 | [-0.69, +3.73] | PASS(nd) | PASS(nd) | FAIL |
| `NEG169` | local | -18.36 | [-20.50, -16.22] | FAIL | FAIL | PASS |
| `IDLEVSALT2` | local | +11.71 | [+9.21, +14.21] | PASS | PASS | FAIL |
| `NULLSALT` | local | +1.02 | [-1.03, +3.07] | PASS(nd) | PASS(nd) | FAIL |
| `NEG114` | local | -26.16 | [-28.32, -24.01] | FAIL | FAIL | PASS |
| `GUNAXREP` | local | +3.20 | [+0.94, +5.45] | PASS | PASS(nd) | FAIL |
| `GBNS` | local | -2.07 | [-4.88, +0.73] | PASS(nd) | FAIL | PASS(nd) |
| `L4REPAIR2` | local | +7.10 | [+4.96, +9.24] | PASS | PASS(nd) | FAIL |
| `APPRLAUNCH2` | local | +3.96 | [+1.79, +6.13] | PASS | PASS(nd) | FAIL |
| `SCREEN4` | local | -2.76 | [-4.96, -0.55] | FAIL | FAIL | PASS(nd) |
| `F232SEALTEM` | work-server-1 | -8.43 | [-10.67, -6.19] | FAIL | FAIL | PASS(nd) |

**Every one of the 19 "AS-WRITTEN PASS → ITT FAIL" arms has a POSITIVE early
difference (17 of 19 significantly so).** They deliver *more* kills before r300 than
control — `MAPCODE` +42.6pp, `SALTIDLE2` +23.2pp, `SALTNOBLOCK` +15.9pp. **They are
not pushing kills past r300 by any reading; the ITT form flags them because it
counts only the late bucket of a larger total.**

**Every one of the 7 "AS-WRITTEN FAIL → ITT PASS" arms has a negative or
non-significant early difference (6 of 7 significantly negative).** `NEG125`
−45.0pp, `SALTOFF` −34.5pp, `NEG114` −26.2pp. **These are the arms losing early
kills — the actual signature the bar is written to catch — and the ITT form calls
them PASS.**

**⛔ THIS IS A SIGN INVERSION ON THE ARMS WHOSE DIRECTION WE ALREADY KNOW.** A bar
that PASSES all four deliberately-degraded NEG calibration cells while FAILING the
four highest-winning arms on the board (`MAPCODE` 73.3%, `SALTIDLE2` 64.6%,
`SALTNOBLOCK` 61.4%, `SALT` 61.0%) is reading backwards on this data.
**I am computing, not ruling. The verdict sentence — which form the programme
adopts, or whether it adopts the SHAPE column instead — is the builder's.**

---

## 3. THE FLIP TABLE

`VOLUME` and `SHAPE` are the exact decomposition of the ITT difference (§2.1); they
sum to the ITT Δ in every row.

| shard | host | n | win share | kill-wins T / C | AS-WRITTEN Δpp | 95% CI | AS-WRITTEN | ITT Δpp | 95% CI | ITT | med kill T / C | VOLUME pp | SHAPE pp |
|---|---|--:|--:|--:|--:|:--:|:--:|--:|:--:|:--:|--:|--:|--:|
| `SALTOFF` | local | 2794 | 28.85% | 768 / 1921 | +3.81 | [+0.41, +7.22] | **FAIL** | -6.73 | [-8.32, -5.14] | **PASS** | 188.0 / 196 | -8.56 | +1.83 |
| `SALT` | local | 5408 | 61.00% | 3116 / 1936 | +1.21 | [-1.29, +3.72] | **PASS(nd)** | +6.58 | [+5.25, +7.91] | **FAIL** | 218.0 / 210.0 | +6.02 | +0.57 |
| `SALTNOBLOCK` | local | 5408 | 61.35% | 3128 / 1936 | +0.40 | [-2.09, +2.90] | **PASS(nd)** | +6.18 | [+4.85, +7.50] | **FAIL** | 212.0 / 208.0 | +5.99 | +0.19 |
| `SALTREP` | local | 5408 | 60.56% | 3098 / 1962 | +0.51 | [-2.00, +3.02] | **PASS(nd)** | +6.08 | [+4.75, +7.42] | **FAIL** | 216.0 / 207.0 | +5.85 | +0.24 |
| `SALTIDLE2` | local | 5408 | 64.57% | 3292 / 1760 | -4.67 | [-7.20, -2.15] | **PASS** | +5.12 | [+3.85, +6.39] | **FAIL** | 212.0 / 212.0 | +7.31 | -2.18 |
| `SEALREPAIR` | local | 5396 | 59.30% | 3024 / 2020 | +0.79 | [-1.63, +3.22] | **PASS(nd)** | +5.10 | [+3.81, +6.38] | **FAIL** | 205.0 / 204.0 | +4.73 | +0.37 |
| `MAPFIX2` | local | 2159 | 57.53% | 1159 / 795 | -1.80 | [-6.03, +2.44] | **PASS(nd)** | +4.91 | [+2.61, +7.21] | **FAIL** | 230 / 240 | +5.72 | -0.81 |
| `NEG125` | local | 2225 | 24.94% | 495 / 1601 | +13.04 | [+8.75, +17.34] | **FAIL** | -4.67 | [-6.37, -2.98] | **PASS** | 213 / 164 | -10.82 | +6.14 |
| `SEALREPAIRR` | work-server-1 | 5394 | 56.77% | 2888 / 2167 | +0.45 | [-1.99, +2.89] | **PASS(nd)** | +3.78 | [+2.46, +5.10] | **FAIL** | 210.0 / 208 | +3.57 | +0.21 |
| `MAPFIX` | local | 2160 | 55.65% | 1110 / 837 | -2.63 | [-6.87, +1.61] | **PASS(nd)** | +3.24 | [+0.91, +5.58] | **FAIL** | 238.0 / 243 | +4.42 | -1.18 |
| `BODYAWRR` | work-server-2 | 5400 | 54.89% | 2794 / 2286 | +1.78 | [-0.60, +4.16] | **PASS(nd)** | +3.22 | [+1.93, +4.51] | **FAIL** | 206.5 / 209.0 | +2.38 | +0.84 |
| `IDLEVSALT` | local | 5408 | 55.99% | 2807 / 2146 | -1.55 | [-4.12, +1.02] | **PASS(nd)** | +3.05 | [+1.66, +4.45] | **FAIL** | 227 / 226.5 | +3.76 | -0.71 |
| `MAPCODE` | local | 4328 | 73.27% | 3031 / 1057 | -15.95 | [-18.99, -12.92] | **PASS** | +2.98 | [+1.73, +4.23] | **FAIL** | 165 / 217 | +10.52 | -7.53 |
| `SALTCLEAR` | local | 5408 | 52.83% | 2621 / 2359 | +1.75 | [-0.82, +4.32] | **PASS(nd)** | +2.37 | [+0.93, +3.80] | **FAIL** | 237 / 228 | +1.56 | +0.80 |
| `AWRLNCH` | local | 5399 | 53.95% | 2786 / 2283 | +0.23 | [-2.11, +2.57] | **PASS(nd)** | +2.35 | [+1.10, +3.61] | **FAIL** | 205.0 / 208 | +2.24 | +0.11 |
| `RND1SOLO` | local | 5400 | 51.30% | 2636 / 2447 | +2.32 | [-0.05, +4.69] | **PASS(nd)** | +1.98 | [+0.69, +3.27] | **FAIL** | 215.0 / 205 | +0.89 | +1.09 |
| `NEG169` | local | 5408 | 40.53% | 1954 / 3046 | +7.37 | [+4.89, +9.85] | **FAIL** | -1.83 | [-3.10, -0.56] | **PASS** | 216.0 / 199.5 | -5.24 | +3.41 |
| `IDLEVSALT2` | local | 2545 | 56.82% | 988 / 644 | -8.21 | [-12.84, -3.58] | **PASS** | +1.81 | [+0.07, +3.55] | **FAIL** | 219.0 / 250.5 | +4.44 | -2.63 |
| `NULLSALT` | local | 5408 | 51.09% | 2536 / 2384 | +1.87 | [-0.74, +4.49] | **PASS(nd)** | +1.79 | [+0.34, +3.25] | **FAIL** | 232.0 / 230.0 | +0.94 | +0.85 |
| `NEG114` | local | 5408 | 36.32% | 1850 / 3355 | +11.09 | [+8.62, +13.56] | **FAIL** | -1.66 | [-2.92, -0.41] | **PASS** | 226.0 / 194 | -7.00 | +5.34 |
| `GUNAXREP` | local | 5408 | 52.31% | 2732 / 2477 | +0.79 | [-1.51, +3.09] | **PASS(nd)** | +1.52 | [+0.25, +2.79] | **FAIL** | 210.0 / 206 | +1.14 | +0.38 |
| `GBNS` | local | 3133 | 49.70% | 1419 / 1438 | +3.59 | [+0.33, +6.85] | **FAIL** | +1.47 | [-0.28, +3.22] | **PASS(nd)** | 213 / 205.0 | -0.17 | +1.64 |
| `L4REPAIR2` | local | 5395 | 54.88% | 2709 / 2249 | -2.09 | [-4.57, +0.40] | **PASS(nd)** | +1.43 | [+0.09, +2.76] | **FAIL** | 205 / 211 | +2.39 | -0.96 |
| `APPRLAUNCH2` | local | 5400 | 52.39% | 2630 / 2344 | -0.14 | [-2.57, +2.29] | **PASS(nd)** | +1.33 | [+0.03, +2.64] | **FAIL** | 212.0 / 212.0 | +1.40 | -0.07 |
| `SCREEN4` | local | 5408 | 48.85% | 2469 / 2583 | +2.52 | [+0.15, +4.89] | **FAIL** | +0.65 | [-0.63, +1.93] | **PASS(nd)** | 213 / 200 | -0.53 | +1.18 |
| `F232SEALTEM` | work-server-1 | 5400 | 45.54% | 2303 / 2787 | +3.24 | [+0.94, +5.55] | **FAIL** | -0.54 | [-1.76, +0.69] | **PASS(nd)** | 206 / 200 | -2.07 | +1.53 |

**⚠ Six of these 26 flips are within one DEFF-choice of not being flips** — see §6.
`SALTOFF`, `SCREEN4`, `GBNS`, `IDLEVSALT2`, `L4REPAIR2` and `APPRLAUNCH2` change
verdict between DEFF 0.98 and 1.25 on one of the two forms.

---

## 4. CALIBRATION CELLS — THE CONTROLS THAT MUST COME OUT THE OTHER WAY

### 4.1 NULL cells (byte-identical arms — must read ~zero, must PASS both forms)

Six NULL cells were found, and **byte-identity was verified, not assumed** (md5 of
the concatenated `*.py` of each arm pair): `_v146null`≡`_v146gunaxis`,
`_v264nullalpha`≡`_v264nullbeta`, `_v151seatrel`≡`_v151null`,
`_v152seatrel2`≡`_v152null`, `_v148null`≡`_v148ferryfirst`.

| shard | host | n | win share | kill-wins T / C | AS-WRITTEN Δpp | 95% CI | AS-WRITTEN | ITT Δpp | 95% CI | ITT | med kill T / C | VOLUME pp | SHAPE pp |
|---|---|--:|--:|--:|--:|:--:|:--:|--:|:--:|:--:|--:|--:|--:|
| `NULL114` | local | 5408 | 49.98% | 2595 / 2608 | -0.19 | [-2.46, +2.07] | **PASS(nd)** | -0.15 | [-1.39, +1.09] | **PASS(nd)** | 206 / 205.0 | -0.06 | -0.09 |
| `NULL5400` | local | 5400 | 49.94% | 1868 / 1857 | +1.56 | [-1.25, +4.37] | **PASS(nd)** | +0.59 | [-0.54, +1.72] | **PASS(nd)** | 211.0 / 210 | +0.05 | +0.54 |
| `NULL140B` | work-server-2 | 5385 | 50.88% | 2575 / 2458 | -0.91 | [-3.26, +1.45] | **PASS(nd)** | +0.11 | [-1.16, +1.38] | **PASS(nd)** | 204 / 205.0 | +0.53 | -0.42 |
| `SR1NULL` | local | 5408 | 49.37% | 2577 / 2639 | -0.34 | [-2.65, +1.96] | **PASS(nd)** | -0.44 | [-1.72, +0.83] | **PASS(nd)** | 205 / 208 | -0.28 | -0.17 |
| `SR2NULL` | local | 5408 | 49.54% | 2603 / 2642 | +1.63 | [-0.69, +3.94] | **PASS(nd)** | +0.61 | [-0.68, +1.90] | **PASS(nd)** | 213 / 212.0 | -0.18 | +0.79 |
| `SRNULL0` | local | 5408 | 50.17% | 2625 / 2586 | +2.04 | [-0.22, +4.30] | **PASS(nd)** | +1.15 | [-0.09, +2.39] | **PASS(nd)** | 206 / 202.0 | +0.17 | +0.98 |

**All six PASS both forms.** Win shares 49.37–50.88%. |Δ| ≤ **2.04pp** AS-WRITTEN,
≤ **1.15pp** ITT; every CI straddles zero. **The pipeline does not manufacture an
effect where there is none.**

**Note for anyone setting a future MDE:** the AS-WRITTEN CI is roughly **twice as
wide** as the ITT CI at the same n (±2.3pp vs ±1.25pp on a 5,400-game shard),
because AS-WRITTEN spends its n on the kill-win subset (~48% of games per side)
while ITT is a paired multinomial contrast over all n. **The AS-WRITTEN form needs
about 4× the games for the same resolution.**

### 4.2 NEG cells (deliberately degraded arms — the known-bad direction)

| shard | host | n | win share | kill-wins T / C | AS-WRITTEN Δpp | 95% CI | AS-WRITTEN | ITT Δpp | 95% CI | ITT | med kill T / C | VOLUME pp | SHAPE pp |
|---|---|--:|--:|--:|--:|:--:|:--:|--:|:--:|:--:|--:|--:|--:|
| `NEG114` | local | 5408 | 36.32% | 1850 / 3355 | +11.09 | [+8.62, +13.56] | **FAIL** | -1.66 | [-2.92, -0.41] | **PASS** | 226.0 / 194 | -7.00 | +5.34 |
| `NEG123` | local | 2529 | 43.26% | 657 / 1004 | +3.77 | [-0.57, +8.12] | **PASS(nd)** | -2.49 | [-4.11, -0.88] | **PASS** | 224 / 214.5 | -3.73 | +1.24 |
| `NEG125` | local | 2225 | 24.94% | 495 / 1601 | +13.04 | [+8.75, +17.34] | **FAIL** | -4.67 | [-6.37, -2.98] | **PASS** | 213 / 164 | -10.82 | +6.14 |
| `NEG169` | local | 5408 | 40.53% | 1954 / 3046 | +7.37 | [+4.89, +9.85] | **FAIL** | -1.83 | [-3.10, -0.56] | **PASS** | 216.0 / 199.5 | -5.24 | +3.41 |

**All four NEG cells score `PASS` under ITT — three of them as an *established*
fall (CI entirely below zero), i.e. the strongest possible pass the bar can
issue.** Their medians move the wrong way at the same time (NEG114 226 vs control
194; NEG125 213 vs 164). **A calibration cell built to be worse should not collect
the bar's strongest pass.**

### 4.3 Mutation test (per-guard: each guard driven to the other verdict)

On each of `NULL5400`, `NULL114`, `NULL140B`, with everything else held fixed:

| perturbation | AS-WRITTEN | ITT |
|---|:--:|:--:|
| none (baseline) | PASS(nd), Δ +1.56 / −0.19 / −0.91 pp | PASS(nd), Δ +0.59 / −0.15 / +0.11 pp |
| **treatment `turns` +200** | **FAIL** (Δ +0.70 / +0.74 / +0.70) | **FAIL** (Δ +0.24 / +0.35 / +0.34) |
| **control `turns` +200** | **PASS** (Δ −0.69 / −0.75 / −0.71) | **PASS** (Δ −0.24 / −0.36 / −0.32) |

**All three verdict labels are reachable, in the correct direction, on both forms.**

### 4.4 Degeneracy control on the win predicate

The side lane's first pass scored `winner == seat` and got a constant 0.00%.
**Reproduced here: `winner == seat` is 0 / 859,461 rows — exactly 0.0000, a
constant column.** The predicate actually used, `winner == "T"`, reads **0.5086**
(437,148 T / 422,313 C / 289 `NOWINNER` / 44 repeated header rows). Non-degenerate,
and centred where a balanced board should sit.

### 4.5 Statistical primitives validated against published values

No scipy in the venv, so the χ² survival function is hand-rolled and was checked
against table values before use: `χ²_sf(3.8415,1)=0.049999`, `(6.6349,1)=0.010000`,
`(18.3070,10)=0.050001`, `(23.2093,10)=0.010000`, `(14.0671,7)=0.050001`,
`(1.0,3)=0.801252` (table 0.8013), `(0,5)=1.0`. Both CI functions were checked
against hand-computed cases, and the DEFF scaling was checked to reproduce
`√(1.25/0.98)` exactly.

### 4.6 Win-share cross-reference against `corefill_status.sh`

**Required by the brief: my figure must reproduce `corefill_status.sh`'s. It does,
for all 150 arms, exactly — 0 mismatches** (its awk, `NR>1{n++; if($7=="T") w++}`,
run against the same snapshot files).

**Two accounting notes, neither a mismatch:**
1. `corefill_status.sh` counts **every** line after the first, so it includes the
   289 `NOWINNER` aborted games and the 44 repeated header rows left by shard
   restarts. My clean denominator drops them. **The two agree to ≤0.20pp on 39 of
   40 affected arms; the worst is `SEALFLOOR0R` at 0.53pp (53 `NOWINNER` rows).**
2. For the 4 shards carrying a `# FIXTURE` header line, `corefill_status.sh`'s
   `NR>1` skips the fixture line and then counts the *column header* row as a game
   — off by exactly +1. Cosmetic, flagged for completeness.

---

## 5. INSTRUMENT CAVEATS THAT CHANGE HOW THESE NUMBERS MAY BE COMPARED

### ⛔ 5.1 THE MAP ROTATION SPLITS THIS BOARD IN TWO AND CROSS-ARM r300 COMPARISON IS NOT VALID ACROSS IT

63 arms ran the pre-rotation 8-map array; 84 ran the post-rotation 15-map pool
(2 arms ran 2 maps, 1 ran 3 — see §5.2). Measured on the **byte-identical** NULL
cells, which differ in nothing but the map pool:

| | maps | n | tiebreak rate |
|---|--:|--:|--:|
| `NULL114` (pre-rotation) | 8 | 5,408 | **3.8%** |
| `NULL5400` (post-rotation) | 15 | 5,400 | **31.0%** |

**Same bot on both sides, same code, and the r1000 rate is 8× higher on the new
pool.** Across the board: 8-map shards average **5.4%** tiebreaks, 15-map shards
**8.7%**; mean late-kill share among treatment kill-wins is 25.0% (8-map) vs 28.4%
(15-map).

⇒ **A kill-win denominator on a post-rotation shard is a materially different thing
from one on a pre-rotation shard. Every number in this document is a WITHIN-shard
treatment-vs-control contrast, where both arms see identical maps, so the contrast
is clean. Ranking arms against each other on the raw late-share is NOT clean and I
have not done it.** 63 arms carry 50% retired-geometry games (one carries 33%).

### 5.2 Three arms have a degenerate map array

`MAPFIX` (2 maps, n=2,160) and `MAPFIX2` (2 maps, n=2,159) — **both are in the flip
list** — and `TINYECO62` (3 maps, n=2,700). They clear the n floor but their
geometry coverage does not resemble the rest of the board. **Treat their flips as
the weakest two on that list.**

### 5.3 Duplicate rows

Three arms carry duplicate `(map, seed, seat, game)` keys from restarts:
`LNCHERL2` (8 of 5,405), `NULL140B` (7 of 5,385), `PINRND1` (5 of 5,405). All
≤0.15% of their n. Recorded, not corrected.

### 5.4 What DEFF was used and why

**DEFF = 0.98 throughout**, per `CLAUDE.md`: local corefill/arena batteries are
balanced-by-construction and read pair-weighted DEFF 0.98 (ρ = −0.020) across 124
shards. **The platform constants (1.529 rated / 1.833 unrated) are NOT imported** —
they would widen these intervals 24–35% for correlation that is not in this
fixture. §6 gives the 1.25 sensitivity for the outlier case.

### ⛔ 5.5 `PASS(nd)` IS NOT AN EXCLUSION AND MUST NOT BE BANKED AS ONE

`PROGRAMME.md:429-432` requires this claim be scored as *"the CI excludes the
registered rise"*, never as a bare fail-to-find — and `CLAUDE.md`'s
direction clause states plainly that widening an interval makes a
fail-to-exclude claim **easier**. **97 of 150 arms read `PASS(nd)` under
AS-WRITTEN and 75 under ITT, and NONE of those is an exclusion.** These arms
predate the r300 bar, so none of them registered a rise threshold; the CI upper
bound is printed in every row precisely so the builder can test it against a
threshold when one exists. **`PASS` (7 / 17 arms) is the only label here that is
a properly restated exclusion.**

---

## 6. DEFF SENSITIVITY (0.98 vs 1.25)

43 of 150 arms show map heterogeneity at p < 0.01 on the ITT indicator (Cochran Q).
Re-running both forms at DEFF 1.25 — the outlier value `CLAUDE.md` cites for arms
with strong map interaction — changes **9 verdicts on 9 distinct arms**, always
from FAIL/PASS to PASS(nd) (i.e. always toward "not detected"):

| shard | host | form | verdict @DEFF 0.98 | verdict @DEFF 1.25 | map-heterogeneity p |
|---|---|:--:|:--:|:--:|--:|
| `SALTOFF` | local | AS-WRITTEN | FAIL | PASS(nd) | 1.4e-03 |
| `IDLEVSALT2` | local | ITT | FAIL | PASS(nd) | 9.7e-02 |
| `GBNS` | local | AS-WRITTEN | FAIL | PASS(nd) | 8.4e-01 |
| `L4REPAIR2` | local | ITT | FAIL | PASS(nd) | 2.7e-01 |
| `APPRLAUNCH2` | local | ITT | FAIL | PASS(nd) | 4.2e-01 |
| `SCREEN4` | local | AS-WRITTEN | FAIL | PASS(nd) | 2.4e-01 |
| `SALTCUTONLY` | local | AS-WRITTEN | FAIL | PASS(nd) | 5.8e-04 |
| `BODYAWR` | local | AS-WRITTEN | FAIL | PASS(nd) | 3.5e-02 |
| `LATE160AMMO` | local | AS-WRITTEN | PASS | PASS(nd) | 1.5e-01 |

Only `SALTOFF` and `SALTCUTONLY` combine a verdict change with genuinely strong
heterogeneity (p < 1e-3). **The other 141 arms are DEFF-insensitive across this
range, and the flip count moves from 26 to 22 at DEFF 1.25 — the headline finding
does not depend on the DEFF choice.**

---

## 7. WHAT I DID NOT COMPUTE, AND WHY

* **No ladder / unrated-platform arms.** This is a scan of local batteries only.
  Platform surfaces carry DEFF 1.529 / 1.833 and a different denominator rule
  (`ladder_games.tsv` for rated); mixing them into this board would breach the
  two-corpus rule. The 15.1% / 7.8% rated-tape figures in the brief are the
  research arm's and are not re-derived here.
* **No per-arm registered-rise threshold, therefore no true exclusion test.** These
  arms were run before the r300 bar existed. §5.5.
* **No cross-arm ranking of the raw late-kill share.** Blocked by §5.1.
* **No re-scoring of the 59 refused arms.** Per the brief, n < 2,000 is refused
  rather than printed wide. The largest refusals are `F200SIEGELA` (1,870),
  `OSCLOCK` (1,867), `V141VS140` (1,837), `OSCLOCK2` (1,809), `F258SEALMAX`
  (1,704), `NESTSHOT2` (1,633), `LNCHERLY` (1,478), `V140VS145B` (1,440),
  `PAVEFIRST` (1,282), `MAPSEAL` (1,201), `CATSOLO` (1,128); 27 of the 59 are
  under n=500. **All 59 are refused for n alone — after the metadata sweep below,
  zero arms lack a declared fixture.**
* **No causal claim about any plank.** Both forms are confounded (§2.2) and the
  decomposition is descriptive, not an identification strategy.
* **No verdict sentence.** Every label in this document is "passes/fails **as
  computed** under the named form". **Which form the programme adopts is the
  builder's call.**

### Fixture-metadata sweep (a side finding worth keeping)

11 arms at n ≥ 5,400 had no treatment/control declaration in
`scratchpad/corefill_work.txt` or any remote worklist. All were recovered:
7 from `scratchpad/loki29_spec.txt` (`SR1NULL` `SR2NULL` `SR1CUR` `SR2CUR`
`SRNULL0` `GUNAXTB` `GUNAXREP`), 3 from `scratchpad/fleet_queue.tsv`
(`F250HOMEEAR` `F253CATAPUL` `F257CATMAX`), and 1 from its committed prereg
(`SALTREF2` → `scratchpad/_locked_saltref2.md:4-5`). **Three of the seven from
`loki29_spec.txt` turned out to be byte-identical NULL cells — half of this
document's calibration set was sitting outside the worklist the status tool
reads.** A fixture declared only in a spec file the read-out never opens is a
fixture the read-out does not have.

---

## 8. FULL BOARD — THE 124 NON-FLIPPING ARMS

| shard | host | n | win share | kill-wins T / C | AS-WRITTEN Δpp | 95% CI | AS-WRITTEN | ITT Δpp | 95% CI | ITT | med kill T / C | VOLUME pp | SHAPE pp |
|---|---|--:|--:|--:|--:|:--:|:--:|--:|:--:|:--:|--:|--:|--:|
| `NOAPPROACH` | local | 2264 | 18.55% | 40 / 1693 | -29.52 | [-43.01, -16.03] | **PASS** | -40.33 | [-42.36, -38.29] | **PASS** | 270.0 / 325 | -29.03 | -11.30 |
| `V120` | local | 5408 | 36.15% | 1893 / 3209 | -7.19 | [-9.72, -4.67] | **PASS** | -10.50 | [-11.88, -9.12] | **PASS** | 213 / 227 | -7.11 | -3.39 |
| `SH287` | local | 5400 | 55.20% | 2834 / 2219 | +10.70 | [+8.21, +13.18] | **FAIL** | +8.43 | [+7.03, +9.82] | **FAIL** | 250.0 / 209 | +3.42 | +5.00 |
| `SH289` | local | 5400 | 52.07% | 2664 / 2374 | +13.09 | [+10.56, +15.62] | **FAIL** | +7.85 | [+6.40, +9.30] | **FAIL** | 260.0 / 208.0 | +1.75 | +6.11 |
| `CMB293` | local | 5400 | 54.48% | 2780 / 2225 | +9.96 | [+7.44, +12.47] | **FAIL** | +7.76 | [+6.36, +9.16] | **FAIL** | 252.0 / 209 | +3.14 | +4.61 |
| `CMB298` | local | 4442 | 51.76% | 2148 / 1969 | +13.50 | [+10.77, +16.23] | **FAIL** | +7.45 | [+5.93, +8.97] | **FAIL** | 259.0 / 201 | +1.20 | +6.26 |
| `IDLECULL` | local | 3774 | 33.55% | 1141 / 2408 | -2.44 | [-5.05, +0.18] | **PASS(nd)** | -6.97 | [-8.24, -5.70] | **PASS** | 171 / 195.0 | -5.82 | -1.15 |
| `MIX282mix5` | local | 5400 | 54.65% | 2792 / 2205 | +8.45 | [+6.02, +10.87] | **FAIL** | +6.83 | [+5.52, +8.15] | **FAIL** | 231.0 / 203 | +2.92 | +3.91 |
| `MIX283mix5` | local | 5400 | 52.83% | 2729 / 2308 | +10.09 | [+7.68, +12.51] | **FAIL** | +6.83 | [+5.50, +8.16] | **FAIL** | 232 / 198.0 | +2.13 | +4.71 |
| `SALTCUTONLY` | local | 5408 | 60.80% | 3099 / 1967 | +2.51 | [+0.06, +4.95] | **FAIL** | +6.62 | [+5.32, +7.92] | **FAIL** | 214 / 204 | +5.44 | +1.17 |
| `MIX281mix4` | local | 5400 | 55.07% | 2827 / 2203 | +6.84 | [+4.36, +9.31] | **FAIL** | +6.50 | [+5.14, +7.86] | **FAIL** | 236 / 212 | +3.32 | +3.18 |
| `MAXSTACK` | local | 5398 | 52.41% | 2676 / 2318 | +9.30 | [+6.82, +11.77] | **FAIL** | +6.22 | [+4.86, +7.59] | **FAIL** | 243.0 / 201.5 | +1.92 | +4.30 |
| `G401g5` | local | 2662 | 52.82% | 1339 / 1143 | +8.49 | [+5.04, +11.95] | **FAIL** | +5.97 | [+4.08, +7.87] | **FAIL** | 233 / 197 | +2.01 | +3.96 |
| `CMB299` | local | 4372 | 54.25% | 2216 / 1834 | +7.43 | [+4.67, +10.18] | **FAIL** | +5.97 | [+4.45, +7.49] | **FAIL** | 229.0 / 203.0 | +2.53 | +3.44 |
| `CMB291` | local | 5400 | 53.78% | 2760 / 2296 | +7.64 | [+5.22, +10.06] | **FAIL** | +5.91 | [+4.58, +7.24] | **FAIL** | 235.0 / 204.0 | +2.33 | +3.58 |
| `MIX284mix3` | local | 5400 | 54.56% | 2811 / 2248 | +6.35 | [+3.91, +8.79] | **FAIL** | +5.85 | [+4.51, +7.19] | **FAIL** | 234 / 207.0 | +2.88 | +2.97 |
| `G400g4` | local | 3545 | 52.95% | 1797 / 1525 | +7.66 | [+4.62, +10.69] | **FAIL** | +5.78 | [+4.10, +7.47] | **FAIL** | 233 / 207 | +2.20 | +3.59 |
| `MIX280mix4` | local | 5400 | 55.24% | 2842 / 2209 | +4.85 | [+2.37, +7.33] | **FAIL** | +5.63 | [+4.26, +7.00] | **FAIL** | 236.0 / 209 | +3.36 | +2.27 |
| `CMB290` | local | 5400 | 51.96% | 2602 / 2417 | +9.22 | [+6.71, +11.73] | **FAIL** | +5.33 | [+3.93, +6.74] | **FAIL** | 249.0 / 213 | +1.05 | +4.29 |
| `SH288` | local | 5400 | 53.61% | 2693 / 2334 | +7.09 | [+4.64, +9.54] | **FAIL** | +5.17 | [+3.82, +6.52] | **FAIL** | 232 / 204.0 | +1.87 | +3.30 |
| `AWRSPAWN` | work-server-2 | 5400 | 55.06% | 2831 / 2239 | +4.32 | [+1.88, +6.76] | **FAIL** | +5.06 | [+3.71, +6.40] | **FAIL** | 229 / 208 | +3.03 | +2.03 |
| `RNDSPAWN` | work-server-2 | 5400 | 51.87% | 2656 / 2378 | +7.48 | [+5.02, +9.94] | **FAIL** | +4.96 | [+3.60, +6.33] | **FAIL** | 235.0 / 213.0 | +1.48 | +3.49 |
| `TRIO` | local | 5807 | 54.35% | 3008 / 2436 | +4.78 | [+2.43, +7.14] | **FAIL** | +4.96 | [+3.66, +6.25] | **FAIL** | 232.0 / 209.0 | +2.72 | +2.24 |
| `SEALFLOOR0` | local | 5396 | 54.78% | 2730 / 2206 | +4.48 | [+1.99, +6.97] | **FAIL** | +4.78 | [+3.44, +6.12] | **FAIL** | 217.0 / 204.0 | +2.73 | +2.05 |
| `MIX285mix2` | local | 5400 | 54.39% | 2736 / 2301 | +4.61 | [+2.14, +7.07] | **FAIL** | +4.44 | [+3.08, +5.81] | **FAIL** | 226.0 / 212 | +2.30 | +2.15 |
| `CMB294` | local | 2723 | 50.68% | 1288 / 1245 | +8.51 | [+4.97, +12.05] | **FAIL** | +4.44 | [+2.46, +6.43] | **FAIL** | 249.5 / 209 | +0.49 | +3.96 |
| `ECORAID` | local | 5400 | 53.22% | 2672 / 2295 | +5.01 | [+2.52, +7.49] | **FAIL** | +4.30 | [+2.94, +5.65] | **FAIL** | 225.0 / 208 | +1.99 | +2.30 |
| `CMB292` | local | 5400 | 54.07% | 2712 / 2304 | +4.44 | [+1.99, +6.89] | **FAIL** | +4.15 | [+2.81, +5.49] | **FAIL** | 228.0 / 210.0 | +2.09 | +2.06 |
| `SEALFLOOR0R` | work-server-1 | 5347 | 53.66% | 2631 / 2202 | +3.53 | [+0.98, +6.08] | **FAIL** | +3.96 | [+2.59, +5.33] | **FAIL** | 217 / 214.0 | +2.37 | +1.60 |
| `CMB296` | local | 5400 | 51.85% | 2693 / 2380 | +4.76 | [+2.42, +7.09] | **FAIL** | +3.65 | [+2.38, +4.91] | **FAIL** | 216 / 194.0 | +1.41 | +2.23 |
| `ECORAID2` | local | 5400 | 52.91% | 2642 / 2320 | +3.76 | [+1.30, +6.22] | **FAIL** | +3.37 | [+2.04, +4.70] | **FAIL** | 224.0 / 208.0 | +1.64 | +1.73 |
| `LNCHRND1` | work-server-1 | 5400 | 51.93% | 2672 / 2392 | +3.63 | [+1.25, +6.01] | **FAIL** | +3.04 | [+1.74, +4.33] | **FAIL** | 216.0 / 206.0 | +1.33 | +1.70 |
| `COMBO` | local | 5400 | 52.30% | 2608 / 2331 | +3.33 | [+0.85, +5.82] | **FAIL** | +2.98 | [+1.64, +4.33] | **FAIL** | 227.0 / 208 | +1.46 | +1.52 |
| `LAUNCH3` | local | 5408 | 43.73% | 2280 / 2945 | +0.27 | [-2.07, +2.61] | **PASS(nd)** | -2.92 | [-4.21, -1.63] | **PASS** | 207.0 / 211 | -3.05 | +0.13 |
| `CATRND1L` | local | 5400 | 51.19% | 2628 / 2441 | +3.89 | [+1.51, +6.28] | **FAIL** | +2.72 | [+1.42, +4.02] | **FAIL** | 219.0 / 204 | +0.89 | +1.83 |
| `CATRND1` | work-server-1 | 4620 | 50.95% | 2254 / 2099 | +3.94 | [+1.40, +6.47] | **FAIL** | +2.68 | [+1.31, +4.06] | **FAIL** | 213.0 / 202 | +0.83 | +1.85 |
| `BODYAWR` | local | 10800 | 53.70% | 5441 / 4671 | +1.87 | [+0.19, +3.54] | **FAIL** | +2.66 | [+1.75, +3.56] | **FAIL** | 205 / 207 | +1.78 | +0.87 |
| `F257CATMAX` | work-server-2 | 5400 | 50.65% | 2615 / 2479 | +3.93 | [+1.56, +6.30] | **FAIL** | +2.50 | [+1.20, +3.80] | **FAIL** | 214 / 202 | +0.65 | +1.85 |
| `NEG123` | local | 2529 | 43.26% | 657 / 1004 | +3.77 | [-0.57, +8.12] | **PASS(nd)** | -2.49 | [-4.11, -0.88] | **PASS** | 224 / 214.5 | -3.73 | +1.24 |
| `HOMEMAX` | local | 5400 | 51.24% | 2642 / 2431 | +2.88 | [+0.47, +5.30] | **FAIL** | +2.41 | [+1.08, +3.74] | **FAIL** | 217.0 / 210 | +1.05 | +1.35 |
| `UNDERECO` | local | 5400 | 51.56% | 2547 / 2364 | +3.07 | [+0.58, +5.56] | **FAIL** | +2.35 | [+1.01, +3.69] | **FAIL** | 226 / 206.0 | +0.96 | +1.40 |
| `FWDFLOOR8` | local | 2788 | 45.88% | 1166 / 1390 | -0.31 | [-3.69, +3.06] | **PASS(nd)** | -2.22 | [-4.01, -0.44] | **PASS** | 197.0 / 205.5 | -2.08 | -0.14 |
| `AMMO0` | local | 5400 | 46.22% | 2251 / 2673 | -0.07 | [-2.51, +2.37] | **PASS(nd)** | -2.07 | [-3.36, -0.79] | **PASS** | 202 / 205 | -2.04 | -0.03 |
| `ROUTEONLY` | local | 3632 | 47.60% | 1111 / 1260 | -2.62 | [-6.18, +0.94] | **PASS(nd)** | -1.98 | [-3.35, -0.62] | **PASS** | 199 / 222.0 | -1.13 | -0.85 |
| `SPAWNLK` | work-server-1 | 5400 | 49.74% | 2510 / 2542 | +4.51 | [+2.06, +6.97] | **FAIL** | +1.94 | [+0.59, +3.30] | **FAIL** | 224.0 / 210.0 | -0.17 | +2.11 |
| `SPAWNLKL` | local | 3646 | 49.70% | 1706 / 1722 | +4.36 | [+1.34, +7.38] | **FAIL** | +1.92 | [+0.23, +3.61] | **FAIL** | 232.0 / 214.0 | -0.13 | +2.05 |
| `GUNAX0` | local | 5408 | 48.00% | 2433 / 2667 | -1.72 | [-4.08, +0.64] | **PASS(nd)** | -1.90 | [-3.19, -0.62] | **PASS** | 205 / 206 | -1.09 | -0.81 |
| `MINHARV1` | local | 5408 | 47.24% | 2236 / 2690 | +1.04 | [-1.45, +3.52] | **PASS(nd)** | -1.85 | [-3.17, -0.53] | **PASS** | 216.0 / 212.0 | -2.32 | +0.47 |
| `DIGOUT` | local | 5400 | 48.67% | 2379 / 2537 | -2.10 | [-4.59, +0.39] | **PASS(nd)** | -1.78 | [-3.11, -0.44] | **PASS** | 212 / 218 | -0.82 | -0.96 |
| `PINRND1` | work-server-2 | 5405 | 47.59% | 2426 / 2629 | +5.78 | [+3.43, +8.13] | **FAIL** | +1.78 | [+0.51, +3.04] | **FAIL** | 215.0 / 199 | -0.93 | +2.70 |
| `NULL123` | local | 2602 | 48.58% | 800 / 887 | -2.01 | [-6.43, +2.41] | **PASS(nd)** | -1.73 | [-3.47, +0.01] | **PASS(nd)** | 220.0 / 233 | -1.08 | -0.65 |
| `MAPSALT` | local | 2363 | 50.40% | 1122 / 1079 | -4.43 | [-8.01, -0.85] | **PASS** | -1.61 | [-3.53, +0.32] | **PASS(nd)** | 205.0 / 207 | +0.46 | -2.06 |
| `LAUNCH2` | local | 5408 | 44.67% | 2316 / 2904 | +2.15 | [-0.16, +4.46] | **PASS(nd)** | -1.57 | [-2.84, -0.31] | **PASS** | 203.0 / 205.0 | -2.61 | +1.04 |
| `BOTH0` | local | 5408 | 46.43% | 2419 / 2800 | +0.25 | [-2.05, +2.56] | **PASS(nd)** | -1.57 | [-2.84, -0.30] | **PASS** | 206 / 208.0 | -1.69 | +0.12 |
| `SEALFLOOR6` | local | 2737 | 47.61% | 1219 / 1349 | -0.33 | [-3.69, +3.04] | **PASS(nd)** | -1.39 | [-3.22, +0.44] | **PASS(nd)** | 211 / 198 | -1.24 | -0.15 |
| `APPRLAUNCH` | local | 5400 | 52.94% | 2644 / 2336 | -0.52 | [-2.96, +1.93] | **PASS(nd)** | +1.30 | [-0.02, +2.61] | **PASS(nd)** | 211.0 / 213.0 | +1.54 | -0.24 |
| `LAUNCHRES0` | local | 5408 | 48.63% | 2471 / 2614 | -1.25 | [-3.66, +1.15] | **PASS(nd)** | -1.29 | [-2.62, +0.03] | **PASS(nd)** | 205 / 213.0 | -0.70 | -0.59 |
| `BODYBLK` | local | 3574 | 47.26% | 1585 / 1736 | -0.33 | [-3.32, +2.66] | **PASS(nd)** | -1.29 | [-2.91, +0.33] | **PASS(nd)** | 204 / 208.0 | -1.13 | -0.15 |
| `BLANKBORDER` | local | 5408 | 51.29% | 2693 / 2544 | +1.25 | [-1.00, +3.51] | **PASS(nd)** | +1.24 | [-0.00, +2.48] | **PASS(nd)** | 204 / 202.5 | +0.63 | +0.61 |
| `LAUNCHLATE160` | local | 5408 | 51.42% | 2588 / 2552 | +2.23 | [-0.08, +4.54] | **PASS(nd)** | +1.22 | [-0.04, +2.48] | **PASS(nd)** | 210.0 / 202.0 | +0.16 | +1.06 |
| `F254COLLARS` | work-server-1 | 3740 | 47.62% | 1670 / 1824 | -0.20 | [-3.07, +2.67] | **PASS(nd)** | -1.15 | [-2.70, +0.40] | **PASS(nd)** | 215.0 / 205.0 | -1.06 | -0.09 |
| `SRNULL0` | local | 5408 | 50.17% | 2625 / 2586 | +2.04 | [-0.22, +4.30] | **PASS(nd)** | +1.15 | [-0.09, +2.39] | **PASS(nd)** | 206 / 202.0 | +0.17 | +0.98 |
| `GBNOSHIELD` | local | 5408 | 51.02% | 2596 / 2510 | +1.44 | [-0.91, +3.78] | **PASS(nd)** | +1.07 | [-0.20, +2.35] | **PASS(nd)** | 206.0 / 200.0 | +0.39 | +0.68 |
| `SEALFIRST` | local | 2018 | 49.55% | 897 / 916 | -1.69 | [-5.86, +2.49] | **PASS(nd)** | -1.04 | [-3.28, +1.20] | **PASS(nd)** | 217 / 222.0 | -0.28 | -0.76 |
| `RAIDDL` | local | 5400 | 50.43% | 2495 / 2404 | +1.27 | [-1.20, +3.74] | **PASS(nd)** | +1.04 | [-0.28, +2.35] | **PASS(nd)** | 212 / 206.0 | +0.46 | +0.58 |
| `AMMO115` | local | 5408 | 51.16% | 2611 / 2544 | +1.47 | [-0.84, +3.78] | **PASS(nd)** | +1.00 | [-0.27, +2.26] | **PASS(nd)** | 211 / 199.0 | +0.30 | +0.70 |
| `SENTTHR` | local | 5400 | 49.80% | 2507 / 2539 | -1.62 | [-3.99, +0.75] | **PASS(nd)** | -0.91 | [-2.19, +0.37] | **PASS(nd)** | 204 / 209 | -0.15 | -0.76 |
| `F253CATAPUL` | work-server-2 | 5400 | 50.02% | 2534 / 2539 | -1.88 | [-4.25, +0.48] | **PASS(nd)** | -0.91 | [-2.19, +0.38] | **PASS(nd)** | 204.0 / 211 | -0.02 | -0.88 |
| `SALTREF2` | work-server-1 | 5400 | 51.78% | 2620 / 2427 | +0.06 | [-2.30, +2.41] | **PASS(nd)** | +0.91 | [-0.36, +2.17] | **PASS(nd)** | 209.0 / 203 | +0.88 | +0.03 |
| `GUNFERRY` | local | 5408 | 50.20% | 2611 / 2609 | +1.86 | [-0.36, +4.08] | **PASS(nd)** | +0.91 | [-0.31, +2.12] | **PASS(nd)** | 205 / 203 | +0.01 | +0.90 |
| `SHIPGATE160` | local | 3048 | 49.41% | 1393 / 1446 | +2.80 | [-0.31, +5.90] | **PASS(nd)** | +0.89 | [-0.77, +2.54] | **PASS(nd)** | 210 / 196.0 | -0.42 | +1.30 |
| `GUNAXTB` | local | 5408 | 49.82% | 2593 / 2626 | -1.48 | [-3.72, +0.77] | **PASS(nd)** | -0.85 | [-2.08, +0.38] | **PASS(nd)** | 205 / 206.0 | -0.14 | -0.71 |
| `SALTROUTE` | local | 5408 | 48.74% | 2369 / 2534 | +0.38 | [-2.24, +2.99] | **PASS(nd)** | -0.85 | [-2.30, +0.60] | **PASS(nd)** | 236 / 233.0 | -1.02 | +0.17 |
| `GUNEARLY150` | local | 5408 | 50.68% | 2644 / 2579 | -2.24 | [-4.53, +0.05] | **PASS(nd)** | -0.80 | [-2.06, +0.47] | **PASS(nd)** | 204.0 / 209 | +0.29 | -1.08 |
| `DELVSDEF` | local | 5408 | 50.20% | 2534 / 2490 | -2.07 | [-4.36, +0.22] | **PASS(nd)** | -0.78 | [-1.99, +0.43] | **PASS(nd)** | 197.0 / 199.5 | +0.18 | -0.96 |
| `GUNBLANK` | local | 5408 | 52.11% | 2713 / 2496 | -0.40 | [-2.65, +1.86] | **PASS(nd)** | +0.72 | [-0.51, +1.96] | **PASS(nd)** | 203 / 200.0 | +0.91 | -0.19 |
| `L4REPAIR` | local | 5408 | 51.28% | 2614 / 2483 | +0.19 | [-2.16, +2.53] | **PASS(nd)** | +0.68 | [-0.59, +1.96] | **PASS(nd)** | 202.0 / 206 | +0.60 | +0.09 |
| `LAUNCH0` | local | 5408 | 52.77% | 2663 / 2472 | -0.19 | [-2.43, +2.05] | **PASS(nd)** | +0.68 | [-0.52, +1.89] | **PASS(nd)** | 206 / 197.0 | +0.77 | -0.09 |
| `CAP6B` | local | 5408 | 49.00% | 2560 / 2680 | -0.31 | [-2.58, +1.95] | **PASS(nd)** | -0.67 | [-1.92, +0.58] | **PASS(nd)** | 206.0 / 208.0 | -0.51 | -0.15 |
| `EXILE0` | local | 5408 | 47.02% | 2453 / 2768 | +1.51 | [-0.78, +3.80] | **PASS(nd)** | -0.65 | [-1.91, +0.61] | **PASS(nd)** | 211 / 206.0 | -1.38 | +0.73 |
| `HEALERFIRST` | local | 5408 | 50.80% | 2561 / 2497 | +0.76 | [-1.59, +3.11] | **PASS(nd)** | +0.65 | [-0.62, +1.91] | **PASS(nd)** | 198 / 197 | +0.29 | +0.36 |
| `ZEROAMMO` | local | 5408 | 52.90% | 2656 / 2432 | -0.68 | [-2.98, +1.62] | **PASS(nd)** | +0.65 | [-0.59, +1.88] | **PASS(nd)** | 204.0 / 200.0 | +0.97 | -0.32 |
| `STEPOFF` | local | 2782 | 48.96% | 1224 / 1297 | +0.19 | [-3.28, +3.67] | **PASS(nd)** | -0.65 | [-2.50, +1.21] | **PASS(nd)** | 215.0 / 215 | -0.73 | +0.09 |
| `GUNBORDER` | local | 5408 | 50.48% | 2630 / 2580 | +0.83 | [-1.42, +3.08] | **PASS(nd)** | +0.61 | [-0.62, +1.85] | **PASS(nd)** | 206.0 / 207.0 | +0.21 | +0.40 |
| `GUNPEN4` | local | 5408 | 49.93% | 2604 / 2609 | +1.31 | [-0.97, +3.60] | **PASS(nd)** | +0.61 | [-0.65, +1.87] | **PASS(nd)** | 211.5 / 205 | -0.02 | +0.63 |
| `SR2NULL` | local | 5408 | 49.54% | 2603 / 2642 | +1.63 | [-0.69, +3.94] | **PASS(nd)** | +0.61 | [-0.68, +1.90] | **PASS(nd)** | 213 / 212.0 | -0.18 | +0.79 |
| `NULL5400` | local | 5400 | 49.94% | 1868 / 1857 | +1.56 | [-1.25, +4.37] | **PASS(nd)** | +0.59 | [-0.54, +1.72] | **PASS(nd)** | 211.0 / 210 | +0.05 | +0.54 |
| `GUNBLANKREP` | local | 5408 | 50.30% | 2628 / 2582 | +0.78 | [-1.49, +3.05] | **PASS(nd)** | +0.57 | [-0.68, +1.82] | **PASS(nd)** | 209.0 / 206.0 | +0.20 | +0.38 |
| `GUNAXABL` | local | 5400 | 48.69% | 2475 / 2618 | +0.28 | [-2.09, +2.64] | **PASS(nd)** | -0.54 | [-1.82, +0.75] | **PASS(nd)** | 206 / 206.0 | -0.67 | +0.13 |
| `GUNFIRST` | local | 5408 | 49.61% | 2585 / 2626 | +1.48 | [-0.80, +3.76] | **PASS(nd)** | +0.54 | [-0.72, +1.79] | **PASS(nd)** | 208 / 208.0 | -0.18 | +0.71 |
| `NULL125` | local | 5400 | 51.04% | 2502 / 2390 | -0.25 | [-2.73, +2.24] | **PASS(nd)** | +0.46 | [-0.86, +1.79] | **PASS(nd)** | 211.5 / 208.5 | +0.57 | -0.11 |
| `SR2CUR` | local | 5408 | 50.98% | 2660 / 2568 | +0.11 | [-2.18, +2.40] | **PASS(nd)** | +0.46 | [-0.81, +1.73] | **PASS(nd)** | 208.0 / 209.0 | +0.41 | +0.05 |
| `SR1NULL` | local | 5408 | 49.37% | 2577 / 2639 | -0.34 | [-2.65, +1.96] | **PASS(nd)** | -0.44 | [-1.72, +0.83] | **PASS(nd)** | 205 / 208 | -0.28 | -0.17 |
| `BURST64B` | local | 5408 | 51.04% | 2573 / 2500 | -1.60 | [-3.92, +0.73] | **PASS(nd)** | -0.43 | [-1.68, +0.83] | **PASS(nd)** | 194 / 203.0 | +0.32 | -0.75 |
| `SALTREF` | work-server-1 | 5400 | 49.11% | 2470 / 2558 | +0.02 | [-2.33, +2.37] | **PASS(nd)** | -0.39 | [-1.65, +0.87] | **PASS(nd)** | 204.0 / 205.0 | -0.40 | +0.01 |
| `SHIPGATENULL` | local | 5408 | 49.56% | 2530 / 2565 | -0.48 | [-2.84, +1.88] | **PASS(nd)** | -0.39 | [-1.67, +0.90] | **PASS(nd)** | 206.0 / 199 | -0.16 | -0.23 |
| `F251PINAIM` | work-server-1 | 5400 | 49.30% | 2492 / 2562 | -0.12 | [-2.46, +2.23] | **PASS(nd)** | -0.37 | [-1.63, +0.89] | **PASS(nd)** | 207.0 / 204.0 | -0.32 | -0.05 |
| `LAUNCHRES20` | local | 5408 | 48.95% | 2483 / 2599 | +0.40 | [-1.99, +2.80] | **PASS(nd)** | -0.37 | [-1.68, +0.94] | **PASS(nd)** | 205 / 210 | -0.56 | +0.19 |
| `AIMTHROW2` | local | 4005 | 50.11% | 1831 / 1828 | +0.67 | [-2.20, +3.53] | **PASS(nd)** | +0.32 | [-1.22, +1.86] | **PASS(nd)** | 210 / 217.0 | +0.02 | +0.30 |
| `TWORAID` | local | 5400 | 50.63% | 2500 / 2418 | -0.22 | [-2.69, +2.25] | **PASS(nd)** | +0.31 | [-1.00, +1.63] | **PASS(nd)** | 205.0 / 210.0 | +0.42 | -0.10 |
| `BESTFITB` | local | 5408 | 49.08% | 2534 / 2667 | +0.58 | [-1.70, +2.86] | **PASS(nd)** | -0.30 | [-1.55, +0.96] | **PASS(nd)** | 207.0 / 208 | -0.58 | +0.28 |
| `FERRY0` | local | 5408 | 50.15% | 2619 / 2593 | +0.37 | [-1.95, +2.69] | **PASS(nd)** | +0.30 | [-0.99, +1.59] | **PASS(nd)** | 204 / 211 | +0.12 | +0.18 |
| `LNCHERL2` | work-server-2 | 5405 | 50.32% | 2542 / 2484 | -1.16 | [-3.56, +1.24] | **PASS(nd)** | -0.26 | [-1.56, +1.04] | **PASS(nd)** | 208.0 / 204.0 | +0.28 | -0.54 |
| `GUNAXIS0` | local | 2752 | 49.45% | 1221 / 1265 | +0.37 | [-3.06, +3.81] | **PASS(nd)** | -0.25 | [-2.06, +1.55] | **PASS(nd)** | 208 / 205 | -0.42 | +0.17 |
| `GUNPEN16` | local | 5408 | 50.72% | 2626 / 2573 | +0.03 | [-2.24, +2.30] | **PASS(nd)** | +0.24 | [-1.01, +1.49] | **PASS(nd)** | 208.0 / 205 | +0.23 | +0.01 |
| `GUNSEAT` | local | 5408 | 51.04% | 2655 / 2551 | -0.48 | [-2.77, +1.80] | **PASS(nd)** | +0.22 | [-1.04, +1.48] | **PASS(nd)** | 209 / 206 | +0.45 | -0.23 |
| `GUNEARLY60` | local | 5408 | 49.83% | 2597 / 2619 | +0.62 | [-1.67, +2.92] | **PASS(nd)** | +0.20 | [-1.06, +1.47] | **PASS(nd)** | 207 / 208 | -0.10 | +0.30 |
| `F232COLLARM` | work-server-2 | 5400 | 49.94% | 2533 / 2546 | +0.52 | [-1.85, +2.89] | **PASS(nd)** | +0.19 | [-1.10, +1.47] | **PASS(nd)** | 205 / 209.0 | -0.06 | +0.25 |
| `LAUNCHLATE80` | local | 5408 | 50.74% | 2545 / 2571 | +0.63 | [-1.68, +2.95] | **PASS(nd)** | +0.18 | [-1.07, +1.44] | **PASS(nd)** | 207 / 202 | -0.12 | +0.30 |
| `SENTSAFE2` | local | 5408 | 49.83% | 2548 / 2548 | +0.39 | [-1.96, +2.74] | **PASS(nd)** | +0.18 | [-1.09, +1.46] | **PASS(nd)** | 202.0 / 204.0 | +0.00 | +0.18 |
| `STANDOFF` | local | 5400 | 50.56% | 2511 / 2398 | -0.94 | [-3.41, +1.53] | **PASS(nd)** | +0.15 | [-1.17, +1.47] | **PASS(nd)** | 212 / 210.0 | +0.57 | -0.43 |
| `TINYECO62` | local | 2700 | 50.93% | 1243 / 1215 | -0.35 | [-3.93, +3.23] | **PASS(nd)** | +0.15 | [-1.79, +2.09] | **PASS(nd)** | 224 / 228 | +0.31 | -0.16 |
| `NULL114` | local | 5408 | 49.98% | 2595 / 2608 | -0.19 | [-2.46, +2.07] | **PASS(nd)** | -0.15 | [-1.39, +1.09] | **PASS(nd)** | 206 / 205.0 | -0.06 | -0.09 |
| `NULL140B` | work-server-2 | 5385 | 50.88% | 2575 / 2458 | -0.91 | [-3.26, +1.45] | **PASS(nd)** | +0.11 | [-1.16, +1.38] | **PASS(nd)** | 204 / 205.0 | +0.53 | -0.42 |
| `GUNAXABLR` | work-server-2 | 5400 | 50.61% | 2556 / 2501 | -0.33 | [-2.73, +2.07] | **PASS(nd)** | +0.11 | [-1.19, +1.42] | **PASS(nd)** | 205.0 / 207 | +0.27 | -0.15 |
| `SHIPGATE0` | local | 3089 | 49.27% | 1416 / 1486 | +1.39 | [-1.71, +4.49] | **PASS(nd)** | +0.10 | [-1.58, +1.77] | **PASS(nd)** | 204.0 / 195.0 | -0.56 | +0.65 |
| `LATE160AMMO` | local | 5408 | 53.31% | 2681 / 2404 | -2.44 | [-4.78, -0.11] | **PASS** | +0.09 | [-1.17, +1.35] | **PASS(nd)** | 198 / 204.0 | +1.24 | -1.15 |
| `BURST32B` | local | 5408 | 50.33% | 2550 / 2521 | -0.47 | [-2.77, +1.84] | **PASS(nd)** | -0.09 | [-1.33, +1.14] | **PASS(nd)** | 197.0 / 197 | +0.13 | -0.22 |
| `F250HOMEEAR` | work-server-2 | 5400 | 50.48% | 2546 / 2486 | -0.76 | [-3.14, +1.62] | **PASS(nd)** | -0.07 | [-1.35, +1.21] | **PASS(nd)** | 209.5 / 207.0 | +0.28 | -0.35 |
| `SENTTHRR` | work-server-2 | 5400 | 48.30% | 2457 / 2623 | +1.50 | [-0.87, +3.87] | **PASS(nd)** | -0.07 | [-1.36, +1.22] | **PASS(nd)** | 205 / 207 | -0.78 | +0.71 |
| `SCREEN` | local | 5408 | 48.84% | 2460 / 2598 | +1.20 | [-1.16, +3.56] | **PASS(nd)** | -0.07 | [-1.35, +1.20] | **PASS(nd)** | 207.5 / 202.0 | -0.64 | +0.56 |
| `SEATREL` | local | 2752 | 50.40% | 1240 / 1234 | -0.30 | [-3.82, +3.22] | **PASS(nd)** | -0.07 | [-1.94, +1.80] | **PASS(nd)** | 210.0 / 214.0 | +0.06 | -0.13 |
| `CAP12B` | local | 5408 | 48.93% | 2566 / 2658 | +0.73 | [-1.53, +2.98] | **PASS(nd)** | -0.04 | [-1.28, +1.20] | **PASS(nd)** | 202.0 / 203.0 | -0.39 | +0.35 |
| `SR1CUR` | local | 5408 | 51.37% | 2686 / 2537 | -1.40 | [-3.66, +0.87] | **PASS(nd)** | -0.04 | [-1.28, +1.21] | **PASS(nd)** | 209.0 / 208 | +0.64 | -0.67 |

---

## 9. METHOD, IN ENOUGH DETAIL TO RERUN

* **Source:** every `*.tsv` under `scratchpad/overnight/` and
  `scratchpad/overnight-remote/*/`, snapshotted 2026-08-16T05:21:27Z. Mirror copies
  (`work-server-N` vs `worker@work-server-N` are the same host) deduped by taking
  the largest file per (shard, host).
* **Row filter:** exactly 9 tab fields, `winner ∈ {T,C}`, `cond ∈ {core_destroyed,
  tiebreak}`, integer `turns`. `NOWINNER`/`-` aborted games and repeated header
  rows from restarts are dropped (§4.6).
* **kill-win** = `winner == <side> AND cond == core_destroyed`. **late** =
  `turns > 300`. Both arms of a shard share the same n games, so the ITT contrast
  is paired.
* **AS-WRITTEN CI:** unpooled two-proportion Wald on disjoint denominators
  (`lateT/nkwT` vs `lateC/nkwC`), variance × DEFF.
* **ITT CI:** paired multinomial — for disjoint indicators A and B over the same n,
  `Var(p_A − p_B) = [p_A + p_B − (p_A − p_B)²] / n`, × DEFF. **The independent
  two-sample formula is wrong here and understates the variance**, since A and B
  are negatively correlated within a game.
* **Verdict labels:** `FAIL` = CI lower bound > 0 (rise established at 95%);
  `PASS` = CI upper bound < 0 (fall established); `PASS(nd)` = CI straddles zero
  (no rise detected — **not an exclusion**, §5.5).
* **Assertions enforced on all 150 arms:** `VOLUME + SHAPE == ITT Δ`,
  `early + late == kill-wins` per side, `EARLY Δ + ITT Δ == Δp`, and the re-read
  row count equals the scan's n — all to 1e-12 / exact. Two full runs on the frozen
  snapshot produced byte-identical output (md5 match).

**Scratch artefacts** (scratchpad, not committed): `r300scan.py`, `verdict.py`,
`mkfinal.py`, `scan.json`, `final.json`, and the frozen `snap/` tree.
