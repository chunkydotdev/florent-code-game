# REGISTERED EXPECTATION — ROUTEBLOCK phase-1 arm + SK_ORE_STEPOFF arm

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition.**

**PROVENANCE:** BUILDER s58, committed before any tape of either arm exists.
Baseline = the COMPLETE CITADEL TRIAD tree (t_p3r tapes; sums measured:
alive 54 / deaths 52 / wins 33 / kills 14 / eco-sum 31.77 / harvesters 195).
Two independent single-flag arms, never composed:

**ARM RB (SK_GUN_ROUTEBLOCK=True):** Magnus's targeting ruling (dee169118 —
"first we want the raider down and then remove barriers with gunners")
phase-1 re-price, the ring's registered follow-up. Dose channel is NEW by
construction (barriers score 0 to turrets today, so the baseline is ~0 —
stated, not assumed): **R1: enemy barriers within d²≤39 of our core killed
by OUR TURRET FIRE, three-fixture sum ≥ 15** (absolute floor since the
baseline channel is empty; ~24-30 collar barriers stand per game per the
prediction study, 4 shots each — 15 total is deliberately modest).
**R2: raider-first preserved** — intruder-kill sum within −20% of the
baseline's 110 (the ring must not starve its body-shots into barriers).
**R3 ammo cost:** Ti-converted sum reported; refusal only if eco guards
breach.

**ARM SO (SK_ORE_STEPOFF=True):** the #130 port. Dose: **S1: total rounds
our builders spend in ≥20-round zero-action runs ON eligible ore tiles,
three-fixture sum, ≤ 50% of baseline (measured same-readout, ratio
registered blind — the audit measured the class at 475+33 rounds in two F1
cells alone).** S2: eco builds and harvesters non-decreasing beyond noise
(an unfrozen keeper works more).

**BOTH ARMS:** identity (flags-off ≡ t_p3r 30/30 ×3 — the adopted tree IS
the p3r arm semantically); v2.1 guards vs the new baseline sums (G1 alive
within −2 of 54, G2 deaths within +4 of 52, G3 eco within −12% of 31.77,
G4 informational with null floors); W5-class harvester fence within −10%
of 195; tracebacks concurrent-observation.

## Pre-registered decisions

RB: R1+R2 pass + guards → ADOPT (the citadel's targeting doctrine
completes). R1 fail → ONE resite/rescore redesign then park. R2 fail with
R1 passing → the priority ordering needs Magnus (his two rulings would be
in measured tension).
SO: S1 pass + guards → ADOPT (bug-fix grade). S1 fail → the port missed;
back to #130's audit for the real site, no second port without it.
