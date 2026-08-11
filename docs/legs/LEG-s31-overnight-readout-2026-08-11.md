# s31 OVERNIGHT READ-OUT — 41,856 games, 9 shards, all COMPLETE

**Read out by the builder arm, s32, 2026-08-11 ~18:5xZ.** Data:
`scratchpad/overnight_s31/` (9 shards, 9/9 `.COMPLETE`, every shard at its exact
declared target, **zero shortfall** — the partial-pooling machinery was not
needed). Run launched 14:20Z, finished 18:38:49Z.

**⛔ READ IT WITH `--dir scratchpad/overnight_s31`. The default `--dir` is the
LIVE directory and now holds the LOKI-29 run.** See §7.

---

## 1. THE CALIBRATION CELLS PASSED, WHICH IS WHAT MAKES THE REST MEAN ANYTHING

| control | reads | what it establishes |
|---|---|---|
| `NULL` — byte-identical v112 copy | **49.20%**, z=−1.17 | the harness is unbiased; the bands stand |
| `NEGCTRL` — `_v140noseal`, a KNOWN real negative | **36.93%** | the screen still DETECTS a bad arm at this n |

⇒ **tonight's `NO-INFORMATION` verdicts mean *no effect resolved*, not *no
power*.** That distinction is the whole reason F3 was rebuilt this afternoon and
this is the first night it can be asserted rather than hoped.

**MDE at the achieved n = 1.90pp ≈ +13 Elo** (80% power, two-sided 5%).
⛔ **NOT the plan's 1.7pp/+12 — that was computed at n≈7,300 and the run is
n=5,408.** The tool's printed **±1.33pp is a 95% SIGNIFICANCE BAND, not a
detection threshold**, and the two must not be quoted as if they were the same
quantity: an arm whose TRUE effect sits exactly on the band edge reads OUTSIDE
**only 50% of the time.**

## 2. THE SEVEN ARMS — AND THE VERDICT LABELS OVERSTATE WHAT SEPARATES THEM

| arm | rate | z vs 50% | tool verdict (uncorrected) | **Bonferroni across 5 screened arms** |
|---|---:|---:|---|---|
| GUNAXIS | **51.94%** | +2.86 | OUTSIDE-ABOVE | **OUTSIDE — survives** |
| CAP12 | 51.37% | +2.01 | OUTSIDE-ABOVE | **inside — does NOT survive** |
| BESTFIT | 50.96% | +1.41 | NO-INFORMATION | inside |
| CAP6 | 50.87% | +1.28 | NO-INFORMATION | inside |
| ROSTER | **47.26%** | −4.03 | OUTSIDE-BELOW | **OUTSIDE — survives** |

*(Both figures independently reproduced by the side lane off the same archive with
a separate parser: identical in every cell.)*

**⛔ CAP12 CROSSED INTO "ESCALATE" BY 0.037pp.** Band top 51.33%, arm 51.37%. It
read `NO-INFORMATION` at 18:24Z and `OUTSIDE-ABOVE` at final n. **Bonferroni at
α=0.01 gives ±1.75pp and CAP12 falls inside it.**

**AND THE BETWEEN-ARM CONTRASTS, WHICH THE TOOL NEVER COMPUTES:**

| contrast | diff | z | p |
|---|---:|---:|---:|
| GUNAXIS vs CAP12 | +0.57pp | +0.60 | **0.55** |
| GUNAXIS vs CAP6 | +1.07pp | +1.12 | 0.26 |
| CAP12 vs CAP6 | +0.50pp | +0.52 | 0.60 |

⇒ **The tool assigns categorically different verdicts to arms that are
statistically indistinguishable from each other.** It tests each arm against 50%
independently and never computes the contrast. **Only GUNAXIS and ROSTER are
genuinely resolved, and ROSTER is the negative.**

## 3. ⭐ THE NIGHT'S REAL HEADLINE: THE STRONGEST ARM IS A PLANK WE DECLARED DEAD, AND CURRENCY AND MECHANISM DISAGREE ON THE SAME TREE

**`_v146gunaxis` IS the LOKI-25 implementation.** Verified by diff, not assumed —
its only changes to the live tree are `LOKI_GUNAXIS_PENALTY = 8` in `doctrine.py`
and a `gun_axis` set in `raid.py:501-526`, both carrying literal `LOKI-25`
comments.

`QUEUE.md:210`: *"gunner-axis / LOKI-25 — **died s30 on a resolved mechanism
falsifier** (deaths −24%, presence −23%, ratio flat −2.3%). ROAD open,
implementation dead."* `HANDOVER` adds: *"the next version must hold presence at
11.00/game while cutting the rate. **A penalty term structurally cannot.**"*

⇒ **It died on a MECHANISM axis. Tonight's +1.94pp is a CURRENCY number. These do
not contradict each other and neither overturns the other:**
* the s30 falsifier was **resolved** — deaths-per-forward-build was flat;
* tonight's currency is the **largest of the night and the only arm surviving
  multiplicity correction.**

**An implementation can move game share while its mechanism metric stays flat.**
That is the anti-Goodhart case running in the *unfamiliar* direction, and this
project has no precedent for it.

**⛔ AND IT DOES NOT MEET THE SHIP RULE AS WRITTEN.** The s31 rule is *(a) a
positive point estimate, (b) a **VERIFIED MECHANISM**, (c) no programme breach.*
GUNAXIS has (a) and (c). **It fails (b) — its mechanism was falsified, at a
comparable n, on a pre-registered bar that resolved.** ⇒ **NOT SHIPPED on this
evidence, and the decision is escalated rather than taken** (§8).

## 4. PART A — DOES A LOCAL WIN RATE PREDICT THE LADDER?

Both CAL shards COMPLETE at 2,000/2,000.

| cell | local | implied Elo | ladder gap | residual | ordering |
|---|---:|---:|---:|---:|---|
| v104 vs v102 | 55.50% | +38.4 | +77 | −38.6 | **AGREE** |
| v104 vs v92 | 68.90% | +138.2 | +86 | +52.2 | **AGREE** |

**VERDICT, in the pre-registered words: FAILED TO FALSIFY. Consistent with
predicting. NOT PROOF.**

**⛔ AND TWO QUALIFICATIONS THAT MAKE IT THINNER THAN THE TOOL'S OUTPUT READS:**

1. **THE RESIDUAL CLAUSE WAS NEVER OPERATIONALISED, AND I AM NOT OPERATIONALISING
   IT NOW.** The bar was *"any inversion, **or large unsigned residuals**."*
   "Large" was never given a threshold, an estimator or a clustering unit, and the
   tool tests the inversion clause only. **I read the residuals (−38.6, +52.2) at
   boot before any threshold existed, so any number I write now is fitted.**
   ⇒ **Part A resolved on the INVERSION clause alone.** The residuals are ~50% of
   their gaps and are reported without a verdict attached.
2. **ONE OF THE TWO CELLS IS MARGINAL.** Proper difference CIs
   (`SE = √(SE₁²+SE₂²)`, not the two marginals combined at their extremes):
   **v104−v102 = +77 [+33, +121]** · **v104−v92 = +86 [−0, +172]**. Research's
   match-bootstrap on the differences — the right object and tighter — gives
   **[+29, +125]** and **[+5, +169]**; both exclude zero, the second by 5 Elo,
   driven by v92's 80-game n. ⇒ **two signed cells, one of them marginal.**
   *(I earlier told the side lane this was "one signed cell", quoting an extremes
   -method interval I relayed without deriving. That understated our own evidence
   and is corrected here.)*

⚠ **v112 has ZERO archived ladder games**, so four of the original six cells are
unscoreable at any local n and are not reported as weak evidence.

## 5. ⛔ THE MEDIAN-KILL-ROUND COLUMN IS SEAT-CONFOUNDED BY CONSTRUCTION

It is computed on games **conditioned on who won**, and seat predicts winning, so
the two subsets carry different seat mixes (+3.9 to +16.2pp across shards).
**On BYTE-IDENTICAL arms it reads TREAT 205 / CTRL 207 — a spurious 2-round
advantage to the treatment.** ⇒ four of five arms' kill-round deltas (BESTFIT −1,
CAP6 −2, CAP12 −2, GUNAXIS +2) sit **inside the null's own offset**. Only ROSTER
(−9) is outside. **Any `kill_round_non_regression` ruling taken off this column
for those four is made at finer resolution than the instrument has.**

## 6. ⭐ THE SEAT EFFECT, MEASURED TONIGHT ON BYTE-IDENTICAL ARMS

`NULL`, n=5,408: **seat A 52.63% vs seat B 45.78% — gap 6.84pp, SE 1.36pp,
95% CI [4.18, 9.50].** Same A>B ordering in **all seven** shards.

**Per map** (seat-A occupant win rate): antler 61.65 (z +6.07) · fjordgate 57.25
(+3.77) · hive 55.04 (+2.62) · nordkap 55.04 (+2.62) · drumlin 55.01 (+2.61) ·
heart 50.44 (+0.23) · meander 47.33 (−1.39) · **atoll 45.58 (−2.30)**.

⇒ **TURN ORDER IS EXCLUDED AS THE SOLE CAUSE.** Turn order is map-constant and can
only push every map the same way; **atoll is individually significant BELOW 50%.**
The effect is our code interacting with map terrain. This became LOKI-29 and its
read-out is a separate document.

## 7. ⛔ THE INCIDENT — MY ARCHIVE STEP RESTARTED ALL NINE FINISHED SHARDS

At **18:39** the LOKI-29 launcher archived the finished outputs to
`scratchpad/overnight_s31/`. **`overnight_watch.sh` was still polling the s31
spec**, saw no `.COMPLETE` and no heartbeat for any shard, read `prog=none`, and
**RESTARTED ALL NINE FROM ZERO at 18:40:13Z**, inside one second. 14 shards ran
on 10 cores for ~3 minutes.

**A COMPLETED-AND-ARCHIVED RUN AND A NEVER-STARTED RUN WERE BYTE-IDENTICAL TO IT.**

* **NO DATA WAS LOST** — the archive was already complete and verified file-by-file
  (9/9 `.COMPLETE`, exact targets, seat balance within one).
* **THE DANGEROUS CONSEQUENCE WAS THE READ-OUT, NOT THE CORES:** the live dir then
  held nine ~25-row zombie shards. `overnight_read.py` on its DEFAULT `--dir`
  would have read those, printed `NO-INFORMATION` across the board at ±19.6pp
  bands, and **looked merely uninformative rather than catastrophically wrong.**
* **WHICH CHECK MISSED IT:** the s31 F13 audit asked *"does anything create the
  COMPLETE marker?"* and answered YES, empirically, correctly. **Nobody asked what
  happens when the marker is REMOVED while the watchdog still lives.** The claim
  was right, its refutation was wrong, and the failure came through a third door.

**FIXED, driven both ways:** `overnight_watch.sh` now enforces **monotonic
progress** — a row count that FALLS (or a vanished `.tsv`) is EXTERNAL
INTERFERENCE, not a dead shard; it ALERTs and REFUSES to restart. Restarting is
only ever correct when progress **stalled**, never when it went **backwards**.
And `OUT` is now `${OUT:-…}` in **both** runners — it was hardcoded, so a
throwaway fixture I believed was isolated **ran against the live run**. *That trap
had been found in the sibling script an hour earlier and worked around in the
launcher instead of fixed at the source, which protected the launcher and left the
next caller — me — exposed.*

## 8. WHAT THIS NIGHT DECIDES

1. **ROSTER is a REAL NEGATIVE** (47.26%, z=−4.03, survives correction). Dead.
2. **NEGCTRL and NULL did their jobs.** The screen has power and no bias at this n.
3. **BESTFIT, CAP6, CAP12: NO INFORMATION.** Back to the pool, **not demoted** —
   CAP12's escalate does not survive multiplicity and its own contrast against
   CAP6 is p=0.60.
4. **GUNAXIS is the only positive arm that survives correction — and it is a
   plank we killed on a mechanism falsifier.** ⇒ **ESCALATED TO MAGNUS, not
   shipped**: the standing ship rule requires a verified mechanism and this has a
   *falsified* one alongside the night's best currency. Under *"win rate decides"*
   it is a candidate; under the ship rule as written it is not. **Those two need
   reconciling by the person who set both.**
5. **Part A did NOT falsify** — local screens remain *consistent with* predicting
   the ladder, on two signed cells, one marginal, with the residual clause
   unoperationalised. **Screening continues; the falsifier is thinner than it reads.**
