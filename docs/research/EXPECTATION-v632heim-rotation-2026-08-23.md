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

---

## RE-SCREEN ADDENDUM (RO-P, prestage redesign — FINAL registered attempt, committed while the build agent runs)

One change: SK_ROTATE_PRESTAGE=290 (rotation bodies walk to their band
halves from r290, build nothing before 300). Bars, blind:
**T3′ wins-sum ≥ 40** (unchanged; baseline 31, RO read 34) and the
**corrected kill channel** (owning the prior spec defect): total core-kill
wins sum ≥ **36** (baseline 29, RO read 33 — the prestage must add ≥3 more
converted wins). Per-fixture wins vs the victory bars reported (RO read
9/10/15).
**T5′ ARRIVAL (the redesign's own mechanic):** median first battery
sentinel ≤ **r310** per fixture (RO read r336/r344/r449) AND ≥ **70%** of
touchable cells field ≥1 battery sentinel (RO read 23/39 = 59%).
**T4 guards unchanged** (alive within −2 of 53, deaths +4 of 54, eco −12%
of 35.47, harvesters −10% of 208 — RO passed all with room).
**Prestage discipline:** zero builds and zero attacks by rotation bodies in
r290-299 (the doctrine's letter), from the taps/decode.
Fail on T3′ or T5′ → **PARK** (two-strikes exhausted); the campaign then
iterates the battery's other dials (funding, tube-guard survival) as NEW
planks against the parked rotation's banked numbers.

**RO-P PRE-TAPE AMENDMENT (disclosed; no tape of this arm exists — the blind
property holds; motivated by the build smoke's MECHANISM findings, which is
what smokes are for):** (1) the commute was measured too short for the
home-side raider (needs ~22-25 rounds; role-3 body already forward) —
**SK_ROTATE_PRESTAGE moves 290 → 278**, with the doctrine reasoning banked:
the walker's phase-1 job is already forward, and a commuting body builds
and attacks nothing (proxy-proven: 0 mutating verbs in 18-verb trap across
three cells). (2) **The study's §8c funding assumption is FALSIFIED on 2 of
3 smoke cells** (bank at flip 40 / 38 / 1,118 vs sentinel 88 / 72 / 81) —
the majority binding lag is FUNDING, which prestage cannot touch. Added to
the same arm as its second half: **SK_ROTATE_CHEST_FROM = 250** — in
[250, 300), the keeper's discretionary purchases (ring turrets, non-belt
barriers) refuse while the bank sits below (2 × current sentinel cost) +
the purchase price; harvesters/conveyors EXEMPT (p0), threat-active rounds
EXEMPT (defence first). Bars unchanged (T3′/T5′/T4 as registered above);
the chest's own dial reported: bank at flip per touchable cell (smoke
read 40/38/1,118). This remains the FINAL registered attempt.
