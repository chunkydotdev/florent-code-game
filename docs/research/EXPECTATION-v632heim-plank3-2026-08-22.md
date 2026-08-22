# REGISTERED EXPECTATION — v632heim PLANK 3 (turret ring) screens

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition.**

**PROVENANCE:** BUILDER s57, committed while the plank-3 build agent runs —
blind to its code and all tapes. Baseline = the ADOPTED leash+demolish tree
(t_p2r tapes). Conforms to the standing-certified form; one disclosed
weakening: the baseline's intruder-death and core-damage columns were never
measured (no prior line needed them), so W3's bars are RELATIVE with the
baseline measured in the same readout — the RATIOS are fixed here, blind.

## Registered lines

**W1 identity:** flags-off ≡ t_p2r 30/30 ×3. *Falsifier: leak; halt.*

**W2 liveness:** ON (SK_FORT_RING=True) diverges ≥8/30 per fixture (the ring
purchases in a round-window; the window opens in every game).

**W3 DOSE — the weapon works, three channels, ratios fixed blind:**
(a) **intruder kills:** three-fixture SUM of enemy-builder deaths inside our
half ≥ **+30%** over the t_p2r baseline (measured same-readout). The ring is
the only new killing verb; the study prices a 40 HP intruder at 6 gunner
shots / 3 sentinel shots.
(b) **the ammo clock:** first convert lands **≤ r5 in ≥ 27/30 ON cells per
fixture** (baseline first-convert median r14+ per the drip study; the
prediction metronome — Mjolnir ladder r1-r5 — is the reason this bar exists).
(c) **ring stands:** ≥1 ring turret alive at r50 in ≥ 24/30 ON cells per
fixture (a ring that dies before the window matters delivers no dose).

**W4 GUARDS (v2.1 sums vs the new baseline, control-measured):**
G1 alive-sum within −2 of **49** · G2 death-sum within +4 of **55** ·
G3 eco-sum common-horizon within −12% of **31.60** · G4 wins-sum [**32**] +
kills-sum [**20**] informational with null floors.

**W5 SCALE FENCE (first purchasing plank — the R2 death, guarded):**
three-fixture harvesters-built SUM within −10% of baseline (measured
same-readout); scale-at-r120 reported per fixture.

**W6 tracebacks:** concurrent observation; expected 0.

## Pre-registered decision rule

W1+W2+W3(a,b,c)+W4 → ADOPT (SK_FORT_RING default ON; the citadel triad
completes). W3(a) fail with (b,c) passing → the ring stands but does not
kill: ONE redesign (siting/facing), then park — two-strikes standing.
W4 breach outside null envelopes → refused regardless of dose. W5 breach →
refused (the fortress exists for the economy; a ring that starves it
contradicts FORTRESS_GOAL).

**W3(a) DENOMINATOR FLOOR (side-lane rider, registered while still blind):**
the +30% ratio bar binds only if the baseline three-fixture intruder-death
sum ≥ **K = 20** (safely below the prediction study's expectation of ~2-2.5
raider bodies/game × 90 cells); below K the readout REPORTS both sums and
the bar re-registers on measured values before any verdict — closing the
degenerate-denominator case (0→1 trivially passes; integer quantization
trivially fails) without surrendering the blind property.

---

## RE-SCREEN ADDENDUM (p3R, registered before its build completes — FINAL ATTEMPT under standing two-strikes)

The redesigned arm (ring below economy + SK_FORT_RING_HARV_MIN=2) screens
against the SAME registered bars above — W3(a) +30% over the same t_p2r
baseline sums (floor bound at 61), W3(b) unchanged (core-side clock
untouched), W3(c) unchanged, W4 sums unchanged, W5 unchanged — with ONE
watched dial added, not gated: median first-ring round (was r8; later is
expected and acceptable IF the dose bars still clear — the registered
question is whether the dose survives the demotion). **This is the ring's
second and final registered attempt: a W3 or fence failure here PARKS the
plank**, and the measured tension between CITADEL_BAR's funding-unconstrained
clause and CITADEL_ECON_RIDER goes to Magnus with both sides' numbers
(the refused arm's +187%/51-alive dose-and-survival vs its −25%/−20% eco
cost) rather than to a third build.
