# THE KILL-HAZARD SCORECARD IS STALE. "TIME IS THEIR ASSET" IS FALSE FOR r150–300 ON CURRENT DATA.

**Research arm, s45. Written 2026-08-16T05:4xZ (`date -u`). Commissioned by the builder on a live
Magnus question: *should we score slightly longer games BETTER, and does the scorecard's basis
predate the 2026-08-13 map rotation?***
**Answer: the basis predates it, the rotation is real, and the premise has flipped in the window
that matters — but NOT in the way "score longer games better" would imply. The correct
re-pricing is narrower and sharper than that.**
**Source: `corpus/ladder_games.tsv` (5,426 rows). Opponents ≥1550 by `oppbef`. Live holder v152.**

---

## 0. THE ARTEFACT BEING RE-DERIVED

`raid.py`'s header carries the load-bearing table and the doctrine built on it:

> *"TIME IS THEIR ASSET: any design that merely lengthens games moves us into the window where
> they convert four times better."*
> per-window kill hazard vs opponents ≥1550 — **ours 15.1 / 5.9 / 7.7 / 9.8 %** across
> r0-150 / 150-200 / 200-300 / 300+ against **theirs 9.8 / 5.9 / 12.5 / 40.9 %**

That table is the reason `KILL_WINDOW_RND: 250` is a bar and the reason a kill-round regression
kills a plank. **Everything below re-derives it on the current map pool.**

---

## 1. THE ROTATION IS REAL — PREMISE CONFIRMED BEFORE IT IS USED AS A CUT

| | count | maps |
|---|---|---|
| **RETIRED** at rotation | 18 | aurora, bridge, crossfire, duel, fjord, longship, pinch, quarry, runestone, showdown, skerry, sprint, strait, string, sweden, twins, vase, vault |
| **INTRODUCED** | 10 | auroraveil, drakkarfjord, frostgate, glacierkeep, icefloe, midgard, ragnarok, royale, valkyrie, yulerune |
| **CARRIED THROUGH** | 15 | antler, archipelago, atoll, drumlin, eider, fjordgate, heart, hive, jackpot, lighthouse, meander, moonrise, nordkap, saga, snowflake |

**Boundary: last retired-map game 2026-08-06T09:12:43Z, first new-map game 2026-08-13T07:12:59Z.**
⇒ **more than half the pool turned over.** Magnus's suspicion that the scorecard predates it is
correct on the dates alone.

---

## 2. THE HEADLINE — BOTH ERAS, SIDE BY SIDE (opponents ≥1550)

Hazard = of games **still alive at window start**, the share ending in a kill by that side inside
the window. **Not conditioned on winning** — the denominator is games at risk, so this metric does
not carry the collider that sank the first draft of FIRE ORDER #1.

### ⛔ CONVENTION, DECLARED — IT WAS UNDECLARED IN THE FIRST VERSION AND IT SETS ONE HEADLINE
*Added after the side lane re-derived this doc and found the omission. A hazard needs two boundary
conventions and the first version stated neither.*

    CONVENTION B (USED HERE):  at risk iff turns >= lo    event counted iff lo <= t <  hi
    CONVENTION A (alternative): at risk iff turns >  lo    event counted iff lo <  t <= hi

**Sensitivity of the POST/PRE ratio to that choice, all four windows, carried-maps cut:**

| window | PRE (B/A) | POST carried (B/A) | POST pooled (B/A) | robust? |
|---|---|---|---|---|
| r0–150 | 1.28 / 1.28 | 1.16 / 1.16 | 0.97 / 0.98 | **robust** |
| r150–200 | 1.22 / 1.24 | 1.18 / 1.28 | 1.41 / 1.45 | **robust, and >1 everywhere** |
| **r200–300** | 0.85 / 0.85 | **1.05 / 0.97** | 1.32 / 1.28 | ⛔ **CROSSES 1.0 on the map-controlled cut** |
| r300+ | 0.43 / 0.42 | 0.82 / 0.82 | 0.90 / 0.90 | **robust** |

⇒ **r200–300 on the carried-maps cut is CONVENTION-SENSITIVE: 0.97–1.05, straddling parity.** The
first version's sentence *"the intervals do NOT overlap"* is true under B and **false under A**
(PRE [12.7,17.1] vs POST [16.5,33.8] overlap). **That claim is withdrawn for this cell.**
✅ **Everything else is robust under both conventions**, including r300+ (disjoint either way) and
the §3A asymmetry that is this doc's actual contribution.
⚠ `CLAUDE.md`'s exposed class is **claims that cleared a bar narrowly**. This one cleared by 0.05.

| window | **PRE** ours | **PRE** theirs | **PRE ratio** | **POST** ours | **POST** theirs | **POST ratio** |
|---|---|---|---|---|---|---|
| r0–150 | 17.9% | 13.9% | **1.28** | 17.6% | 18.0% | **0.98** |
| r150–200 | 11.9% | 9.7% | **1.22** | 18.4% | 13.0% | **1.41** |
| **r200–300** | 15.0% | 17.7% | **0.85** | 28.9% | 21.5% | **1.34** |
| **r300+** | 17.7% | 41.7% | **0.43** | 39.5% | 43.4% | **0.91** |

*PRE n=2,855 games / 571 matches · POST n=1,040 games / 208 matches.*

⇒ **The r200–300 window FLIPPED, 0.85 → 1.34. The r300+ deficit MORE THAN HALVED, 0.43 → 0.91.**

---

## 3. THE DECOMPOSITION — IS IT THE MAPS OR IS IT US?

The era cut confounds the map pool with our own version (we shipped v125→v152 across it), so it
is split two ways. **95% CIs use DEFF 1.529** (rated pooled: a window×era cell can hold several
games from one match and several matches against one opponent, so **both clusters are live**).

### A. MAP HELD CONSTANT — carried-through maps only — isolates the ERA

| window | PRE ours | POST ours | PRE theirs | POST theirs | ratio PRE→POST |
|---|---|---|---|---|---|
| r0–150 | 17.9% [16.2,19.6] | 18.8% [13.6,23.9] | 13.9% | 16.1% | 1.28 → 1.16 |
| r150–200 | 11.9% [10.1,13.6] | 17.6% [11.4,23.8] | 9.7% | 14.9% | 1.22 → 1.18 |
| **r200–300** | **15.0% [12.8,17.2]** | **26.7% [17.9,35.4]** | 17.7% | 25.3% | **0.85 → 1.05** |
| **r300+** | **17.7% [14.8,20.6]** | **37.5% [23.7,51.3]** | 41.7% | 45.8% | **0.43 → 0.82** |

⭐ **OUR late-window hazard MORE THAN DOUBLED with the map pool held constant, and the intervals
do NOT overlap** — r200–300 [12.8,17.2] vs [17.9,35.4]; r300+ [14.8,20.6] vs [23.7,51.3].
**Theirs barely moved (41.7% → 45.8% at r300+).**
⇒ **THE "THEY CONVERT FOUR TIMES BETTER LATE" FACT WAS MOSTLY A STATEMENT ABOUT OUR OLD BOT, NOT
ABOUT THE FIELD.** Consistent with the `MAP_CODES` pathfinding defect fixed and shipped as v125.

### B. ERA HELD CONSTANT — post-rotation only — isolates the MAP POOL

| window | carried maps ratio | new maps ratio |
|---|---|---|
| r0–150 | 1.16 | **0.89** |
| r150–200 | 1.18 | **1.56** |
| r200–300 | 1.05 | **1.48** |
| r300+ | 0.82 | 0.94 |

⇒ **The new maps disfavour us EARLY and favour us in r150–300.** Suggestive only — the intervals
overlap heavily at these n (carried 341 games, new 704).

---

## 4. ⭐ THE ANSWER TO THE QUESTION ASKED

**"Should we score slightly longer games better?"** — **No, but the penalty is aimed at the wrong
window, and that is the correction worth making.**

* **r150–200 IS NO LONGER THEIR WINDOW, ROBUSTLY** — 1.18–1.28 carried-maps, 1.41–1.45 pooled,
  **above 1 under both conventions on both cuts.**
* ⚠ **r200–300 IS PARITY, NOT A FLIP — AND THE MAP-CONTROLLED CUT STRADDLES IT** (0.97–1.05
  depending on convention; 1.28–1.32 pooled, but the pooled cut does not control the pool).
  **The claim that survives is the NEGATIVE one: there is no 4× disadvantage here any more** —
  it was 0.85 and nothing in the current data reads worse than ~0.97. **The claim that does NOT
  survive is that it flipped in our favour.**
* ⇒ **A design that lengthens the kill from ~170 to ~230 is not walking into a measured
  disadvantage on current data. It is walking into approximately parity.** That is weaker than
  the first version of this doc said, and it is the version the conventions both support.
* **r300+ IS STILL THEIRS**, at 0.91 pooled / 0.82 carried-maps. **Much weaker than 0.43, but
  still against us.** A design that pushes games past r300 still pays.
* ⇒ **THE RE-PRICING: the kill-round penalty should bind on crossing ~r300, not on drift inside
  r200–300.** `KILL_WINDOW_RND: 250` sits in the middle of a window that is now neutral-to-ours.

**This is NOT a licence to lengthen games.** `R1000_IS_DEFEAT` is a directive from Magnus, not an
inference from this table, and nothing here touches it. What the table changes is the *evidential
basis* for treating a +20-round drift as harmful — that basis has gone.

---

## 5. ⛔ THE CONSEQUENCE NOBODY WILL LIKE — IT LANDS ON A CANCELLATION MADE TODAY

The 55-class combos were priced as carrying **"+17–43 round kill regressions"**, and `TRIO` was
cancelled today with **"kills 23 rounds later"** as one of two stated legs. Those magnitudes move
the median kill from ~205–209 to ~226–252 — **squarely inside r200–300, the window that just read
1.34 in our favour.**

⇒ **The kill-round leg of those arguments is priced on the PRE-rotation table and does not survive
re-derivation.** ⚠ **`TRIO`'s OTHER leg is untouched and independently sufficient** — it could not
resolve +0.55pp over `bodyaware` at n=5,808, which is a power argument and stands on its own.
**So the cancellation was right; one of its two reasons was not.** That distinction matters for
the arms not yet cancelled.

⛔ **I am not re-opening any cancellation. That is the builder's call and this is the input to it.**

### ⭐ AND THE DISTINCTION THAT ACTUALLY GOVERNS — A BAR DOES NOT WEAKEN WHEN ITS RATIONALE DOES
*Sharpened by the side lane, correcting their own earlier prescription to the builder.*

**`KILL_WINDOW_RND: 250` and `DEFENCE_ADMISSION_BAR` are Magnus's DIRECTIVES, not inferences from
`raid.py`'s table.** This doc removes the *empirical* grounding for treating a +20-round drift
inside r200–300 as harmful. **It does not and cannot move the bar** — that is exactly the argument
§4 makes about `R1000_IS_DEFEAT`, and it applies identically here. **Only Magnus moves a directive.**

⇒ **The operative distinction for arms NOT yet cancelled:**

| verdict | supported today? | what it licenses |
|---|---|---|
| *"off-programme by DIRECTIVE"* | **YES** — the bar stands regardless of this doc | cancel / hold, citing `PROGRAMME.md` |
| *"empirically HARMFUL"* | **NO** — 0.97–1.05, nothing like 4× | nothing; the evidence is gone |

**Cancelling on the first is sound. Cancelling on the second, or writing the second into a
verdict, is now unsupported** — and the two were being used interchangeably this morning,
including by the lane that caught this.

---

## 6. LIMITS — STATED BECAUSE THE n IS THE WEAK PART

1. **POST-rotation n is small**: 1,040 games / 208 matches pooled; **341 games on carried maps and
   72 at risk in the r300+ cell.** The carried-maps r300+ interval is [23.7, 51.3] — wide. The
   *direction* is established (non-overlapping with PRE); the *magnitude* is not.
2. **§3A cannot separate OUR version from FIELD drift.** Both changed across the boundary. The
   claim "it was mostly us" rests on the asymmetry (our hazard doubled, theirs moved 4pp) plus the
   known v125 pathfinding fix — **that is an inference, not a measurement.**
3. **§3B's map effect is suggestive only** — intervals overlap at these n.
4. This is the **RATED** surface. Unrated legs cluster harder and would need their own constants.
5. **Cell counts, not just percentages, are printed above** so any cell can be re-derived; cells
   under 25 at risk are refused rather than reported.

---

## PROVENANCE
`corpus/ladder_games.tsv` @ 5,426 rows, synced 2026-08-16T04:50Z (4,135 new replays decoded this
session, reconciliation 100.0000% on 4,115 testable rows). Opponent filter `oppbef >= 1550`.
Era boundary derived from first/last appearance of retired and introduced maps, not assumed.
Commissioned by the builder; question originated with Magnus. Timestamps from `date -u`.
