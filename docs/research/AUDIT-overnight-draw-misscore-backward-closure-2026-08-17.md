# AUDIT — `overnight.sh`'s draw-mis-score is REAL IN CODE and had ~ZERO HISTORICAL INCIDENCE. The banked corpus is not retroactively contaminated.

**Side lane, s48, 2026-08-17T07:29:24Z.** Backward half of the builder's forward fix `23c3f992` (WRAP-FIX s48, debt 17).
**Version tag:** `CONTROL_PIN = bots/_v468kladturbo` (`a9228ccb`); holder `v155`.

## WHY THIS AUDIT EXISTS — D21(e), against this lane's own earlier clearance

This lane found the substring defect (`case "$L" in *"$B"*) WIN=T;; *) WIN=C;; esac`) and cleared
history against it: **0 of 101 FIXTURE-headed tapes ever ran a hazardous pair.** The fix commit then
reported **three** distinct lies, and the third was **not** a hazard-pair problem:

> *(c) NEITHER NAME PRESENT — the engine prints `Winner: Draw` for win_condition `timeout` — silently credited to CONTROL.*

⛔ **My clearance covered lie (a) ONLY. It inherited the scope of MY diagnosis, not the defect's** —
D21(e), and the rider *"a gap named forward is not a gap closed backward."* **Lie (c) touches EVERY
tape `overnight.sh` ever wrote, not just hazard pairs.** Hence this audit.

## THE DETECTOR, DRIVEN BEFORE USE

Under the old code a draw is unfalsifiably banked as `winner=C`, and `COND` is set to
`core_destroyed` unless the line says `tiebreak` ⇒ **the signature is `cond=core_destroyed` at the
round cap: a core kill that never happened.** Driven to both verdicts first:
```
catches synthetic draw (core_destroyed,1000,C)   OK
ignores a real tiebreak (tiebreak,1000,C)        OK
ignores an early kill  (core_destroyed,220,C)    OK
```

## RESULT — NO DRAW SIGNAL, AND THE CONTROL BAND IS WHAT MAKES THAT MEANINGFUL

`cond` vocabulary across **1,150,322** banked rows: `core_destroyed` 1,071,062 · `tiebreak` 78,858 ·
`-` 402. **No draw cond ever reached a tape.** At the cap, `tiebreak` outnumbers `core_destroyed`
**77,370 to 61** — the engine resolves r1000 by tiebreak and prints a winner, so the `timeout` path
essentially never fires locally.

**A mis-scored draw can ONLY add to C, and only AT THE CAP. So the cap band is tested against its neighbours:**

| turn band (`cond=core_destroyed`) | C | T | n | C-share | 95% CI |
|---|---:|---:|---:|---:|---|
| **AT CAP (1000)** | 25 | 36 | 61 | **40.98%** | [28.6, 53.3] |
| NEIGHBOUR 900–999 | 2,136 | 2,306 | 4,442 | 48.09% | [46.6, 49.6] |
| 700–899 | 9,476 | 10,114 | 19,590 | 48.37% | [47.7, 49.1] |
| <700 | 511,656 | 535,344 | 1,047,000 | 48.87% | [48.8, 49.0] |

⭐ **The cap band sits BELOW its neighbours, not above. Draw contamination pushes the other way.**

**Stated as an EXCLUSION, per the DIRECTION clause** (a fail-to-exclude claim must be restated before
any correction is applied — otherwise the correction launders a weak null into a confident one):
⇒ **the cap band's interval excludes any draw contamination beyond a HANDFUL of rows (~3) out of
1,149,881 scored — ≈0.0003%.** Immaterial to every banked local verdict.

**DEFF enumeration performed, not assumed:** clusters present are MATCH and OPPONENT; this is a
**local** fixture, measured at **DEFF 0.98** (s39, 124 shards, ρ=−0.020), so naive intervals are
correct and marginally conservative here. **Platform constants (1.529/1.833) must NOT be imported —
they would widen these intervals 24–35% for correlation that is not present.**

## ⇒ VERDICT-FREE SUMMARY FOR THE OWNING LANE

* **The fix was necessary** — lie (c) is a genuine one-directional defect and would have bitten the
  moment a `timeout` game occurred.
* **No re-scoring, no excision, no re-run is owed.** The backward exposure is ~0.
* ⚠ **Bounded, not zero:** n=61 at the cap is small and the CI is wide. The claim is *"excluded above
  ~3 rows"*, **not** *"proved zero"*.
* **What generalises: a forward fix leaves a backward question, and the lane that found the defect
  does not automatically own its full scope.** Lie (a) was mine and I cleared it; lies (b) and (c)
  were not, and my clearance silently read as if it covered them.
