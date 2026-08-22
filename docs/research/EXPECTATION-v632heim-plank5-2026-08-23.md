# REGISTERED EXPECTATION — v632heim PLANK 5 (second eco body) screens

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition.**

**PROVENANCE:** BUILDER s58, committed while the plank-5 build agent is
still running — blind to its code and all tapes. Baseline = the complete
citadel triad (t_trid tapes now generating ≡ t_p3r semantics; sums
[alive 54 / deaths 52 / wins 33 / kills 14 / eco 31.77 / harvesters 195]).

**PLANK:** SK_FORT_WALKER_ECO — the cage walker re-homes to the keeper turn
(acting, never publishing — the R5 single-writer gates are a correctness
precondition of the same plank). The doctrine basis: builders never raid
until r300; the eco gap is the largest measured lever (2.2 harvesters/game
vs 8-10 ceiling).

## Registered lines

**V1 identity:** flags-off ≡ t_trid 30/30 ×3.
**V2 liveness:** ON diverges ≥8/30 per fixture (the walker's whole turn
changes; expect ~30).
**V3 DOSE:** (a) harvesters-built three-fixture sum ≥ **+25%** over 195;
(b) eco-builds sum common-horizon ≥ **+15%** over 31.77. (A second body on
the same ladder should at minimum add its own hands; the ceilings say 3-4x
headroom exists.)
**V4 GUARDS (v2.1):** G1 alive-sum within −2 of 54 · G2 death-sum within
+4 of 52 · G3 eco is the DOSE here (no separate fence) · G4 wins-sum
informational [33] — **with the pre-registered caveat: the walker was the
kill branch, so kills-sum and wins-sum are EXPECTED to fall; under the
phased doctrine both are informational, but a wins-sum fall beyond −5
(the null floor) is reported with its per-fixture split for Magnus's
picture of what no-raid-before-r300 costs on r1000-capable fixtures.**
**V5 publisher integrity (the R5 check, screen-grade):** slot-5/14 beat
freshness on ON tapes shows NO frozen-word signature (the 291-round
precedent's detector: a published word unchanged >100 rounds while its
underlying state visibly changes). Any hit → build defect, halt.
**V6 tracebacks:** concurrent observation, 0 expected.

## Pre-registered decision

V1-V3 + V4 (G1/G2) → ADOPT. V3 fail → ONE staffing redesign (the study
names alternatives: denier-half-eco instead of walker) then park. V5 hit →
halt regardless (correctness, not performance).
