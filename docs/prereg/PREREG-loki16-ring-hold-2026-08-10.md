# PREREG — LOKI-16: HOLD the enemy ring tile instead of walking off it

**Committed BEFORE submission, activation and leg creation.** Line `loki`.
Comparator **v104 "Loki v2" = `bots/_v130loki13`**, the live incumbent and the
previous line iteration. Pinned panel, pinned maps, **pooled to n=100/arm**.

    bots/_v133loki16 = bots/_v130loki13 + LOKI16_RING_HOLD_ON (+ LOKI16_HOLD_CLAIM_RND = 250)

`main.py` and `eco.py` **byte-identical** (diff-verified). Only `raid.py` and
`doctrine.py` change; every new path is a no-op when the flag is off.

## ⚠ THE PLANK IS NOT THE THING THE EVIDENCE MEASURED. READ THIS FIRST.

The motivating figure is **presence vs absence**: over 539,000 exposed
builder-rounds at rounds < 250, **one hostile body on the enemy 12-tile ring
doubles their 25-round core-death hazard, 2.24% -> 4.77%, CIs disjoint.**

**But the incumbent ALREADY has a body on that ring in 68.8% of rounds, first
arriving around round 22.** So we are not moving from absence to presence. **We
are moving from 68.8% presence to 81.3% presence — and the dose-response between
those two points is UNMEASURED.** The hazard evidence licenses "a body on the
ring matters"; it does not license "more of it matters proportionally."

**This is stated before the leg so that a null cannot later be read as refuting
the ring-body finding.** It would refute only the extrapolation.

## What the plank actually changes — retention, not presence

`_raid_station` in the parent adds **+12** to a corner's cost once
`_open_seats_by` reaches 0, i.e. **it walks the body off a corner at exactly the
moment that corner has become pure body-denial** — and the four diagonal corners
are the ring tiles the barrier path never covers. LOKI-16 refuses that walk-off.
A refusal, which is the only shape that has gained on this line.

*(Note `LOKI_QUIET_ON = True` in the parent, so seat-pecking is already dead
code and is not part of this comparison.)*

## MECHANISM — already measured locally, and measured properly

**480 local games: 10 replicates x 16 (opponent, map) cells x 3 arms**, the third
arm being **the parent under a different label as a NULL**, cell-blocked
permutation test. The local engine is **not run-to-run deterministic** (parent vs
itself, same seed, gave 355 vs 210 turns), so single-draw pairing would have
measured nothing.

| | treatment | parent | null | T-P (p) |
|---|---|---|---|---|
| ring-body coverage | **0.813** | 0.688 | 0.698 | **+0.125 (<0.001)** |
| longest single-tile hold | **0.809** | 0.578 | 0.550 | **+0.231 (<0.001)** |
| max bodies on ring at once | 2.29 | 2.35 | 2.25 | -0.06 (0.50) |

**The null arm produced no effect on any measure** — that is what licenses
reading the treatment delta at all. Consistent on all four maps; **larger in
SHORT games** (coverage +0.129, p<0.001), which is the band the hazard evidence
covers, so **no short-to-live transfer failure of the kind that killed LOKI-13
and LOKI-11.** 0 tracebacks in 672 local matches, on a stderr instrument
validated against `bots/_probe_crash` (97 tracebacks captured).

**MECHANISM BAR FOR THE LEG: ring-body coverage in the treatment arm must exceed
the control arm's by >= +0.08, decoded from the leg's own replays.** Local
delta is +0.125; the bar is set below it because local probes die in ~136 rounds
and live games do not. **Bar missed -> the leg answered nothing.**

## VERDICT — PRIMARY `core_kill_share`, n=100 vs n=100

Per-opponent Δ column **mandatory**; seat mix printed per cell. **The panel is a
two-cell instrument** (Bisons floor, Leviathan and CtrlAltDefeat ceilings) — this
is a read on I Stone and gsxWins wearing a five-cell denominator, and it says so
here, before the data. n=100/100 resolves ~14pp at 80% power; **nothing under
that will be claimed.**

## The cost is MEASURED, not hypothesised

**Distinct enemy ring tiles on which we hold a BUILDING falls 5.14 -> 4.19
(p<0.001).** The pinned body sits on a tile `can_build_barrier` would otherwise
have taken. **So this plank trades a barrier for a body**, and a barrier is
permanent while a body can be killed. That is the specific way this loses and it
is written down before the leg rather than discovered in the autopsy.

## Falsifier

1. Coverage bar met, `core_kill_share` flat -> **LABELLED NULL**, and the honest
   reading is that the 68.8% the incumbent already achieves is sufficient —
   **not** that ring bodies do not matter.
2. Coverage bar met, `core_kill_share` DOWN -> **the body-for-barrier trade is
   bad**, which the measured building-coverage loss predicts.
3. Coverage bar met, `core_kill_share` UP -> retention beyond the incumbent's
   level pays, and the dose-response question becomes worth mapping.
4. Coverage bar missed -> answered nothing.

## Honest limits, carried from the build

* **Both arms already exceed the prescription's ONE body** — mean max
  simultaneous ring bodies ~2.3 in parent and treatment alike. Inherited
  behaviour, not introduced here, but **this leg is not a clean 1-vs-0 contrast**
  and must not be reported as one.
* The holder election is a **per-unit approximation** — the comms store is
  16/16 full, so a raider claims only if it sees no lower-id friendly builder on
  another ring tile. It can transiently pin two bodies.
* `get_cpu_time_elapsed()` returns 0 locally, so `_cpu_exhausted` is inert and
  the added <=12-tile claim scan is **untested against the 10 ms budget**. It is
  bounded and O(1) after the claim.
* "Flag off == parent" rests on **code inspection**, not a hash match — replays
  are not byte-reproducible even for identical bots.
* Local opponents are four `*_probe` bots that die in ~136 rounds and are at a
  win-rate ceiling. **Nothing local says anything about a real opponent's
  core-death hazard.** Only the live leg can.

## Cost

Zero rated exposure by the measured procedure: activate for the ~60 s it takes
to fire five challenges, roll back to v104, **verify the holder**.
`breakin_watch` (floor 1567) and `ship_watch` stay armed on v104 throughout.
