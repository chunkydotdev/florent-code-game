# REGISTERED EXPECTATION — THE ROTATION (planks 8+9) screens

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition.**

**PROVENANCE:** BUILDER s58, committed while BOTH relevant agents run (the
plank-5 screen chain and the rotation build) — blind to all their outputs.
Baseline = triad+SO (t_so tapes; sums [alive 53 / deaths 54 / wins 31 /
kills 14 / eco 35.47 / harv 208]; per-fixture wins F1 9 / F2 9 / F3 13).

**ARMS:**
- **RO** (SK_ROTATE=True alone): walker cages pre-300 as today, both raiders
  rotate to the sentinel battery at r300. Isolates the rotation.
- **FD** (SK_ROTATE + SK_FORT_WALKER_ECO): the FULL DOCTRINE — eco+defence
  to r300, rotate and destroy. The victory-bar candidate arm.
  (FD composes an unscreened plank-5; its own p5-alone screen resolves in
  parallel and FD's verdict WAITS on p5's — pre-registered ordering.)

## Registered lines (both arms unless noted)

**T1 identity:** flags-off ≡ t_so 30/30 ×3.
**T2 liveness:** ON diverges ≥8/30 per fixture (FD ~30 expected).
**T3 THE WIN ENGINE (dose):** wins-sum ≥ **40** (from 31 — +9, far outside
the null spread −5..−1); kills-sum ≥ **25** (from 14). Per-fixture wins
reported against the VICTORY BARS (16/30 each) — the bars themselves are
the campaign target, not this screen's gate; median win round of won games
reported (the demo's unresisted rotation killed r336-374).
**T4 GUARDS:** G1 alive-sum within −2 of 53 (the rotation acts after r300
and must not degrade reaching it; FD's pre-300 walker-eco is the only
pre-flip change) · G2 death-sum within +4 of 54 · G3(FD only) eco-sum ≥
+10% over 35.47 (plank-5's dose migrates into this arm) · G3(RO) eco
within −12% · harvesters: FD ≥ 208, RO within −10%.
**T5 rotation mechanics (from the taps/decode):** flip at exactly r300 in
every game reaching it; ≥1 game per fixture showing the clustered first
battery (≥3 sentinels within pairwise cheb ≤3 of each other); zero
post-flip prep barriers; zero post-flip pecks by rotation bodies.
**T6 tracebacks:** concurrent observation, 0.

## Pre-registered decisions

FD passes T1-T5 with p5-alone also passing → **ADOPT THE FULL DOCTRINE**
(all flags ON — the Heimdall line reaches its intended shape) and the next
iteration cycle begins AGAINST THE VICTORY BARS with fresh baselines.
RO passes but FD fails through the p5 interaction → adopt RO, plank 5
returns to design. T3 fail on both → the rotation returns to design ONCE
(battery size / siting / timing are the study's named dials) then parks —
two-strikes standing. T5 mechanical failures → build defect, halt.
