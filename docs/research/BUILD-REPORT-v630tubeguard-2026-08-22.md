# BUILD REPORT — v630 TUBE GUARD (`bots/_v630tubeguard`) — SCREEN VERDICT: NOT ADVANCED

**GAME CONTEXT: everything here is in-game analysis for the Florent Code
League, a sandboxed bot-vs-bot programming competition on a simulated grid
under organiser-approved rules. "kill"/"death"/"removal" = in-engine removal
of a competing game bot's unit per the engine's documented rules.**

**PROVENANCE:** built and verdict-typed by BUILDER s57 (2026-08-22 evening).
Design read: fresh opus agent (banked in the coordination tail ~18:3xZ).
Mechanism readout E4–E6: fresh opus agent, scripts
`scratchpad/s57_v630/e46_*.py`, report banked verbatim in §3 below.
Registered expectation committed pre-readout:
`EXPECTATION-v630-tubeguard-screens-2026-08-22.md`. Tapes:
`scratchpad/s57_v630/t_{ctrl,id,on}_{f1,f2}` (fresh same-host, sequential
load discipline). Side-lane certs: registration certified; E1/E2
sample-verified independently.

---

## 1. VERDICT (typed by the builder, per registered line)

| line | bar | measured | verdict |
|---|---|---|---|
| **E1 identity** | 30/30 per fixture | **60/60 turn-identical** (rdiff driven to other verdict first) | **PASS** — the OFF tree is v628compose exactly |
| **E2 liveness** | ≥8/30 divergent per fixture ON | F1 **30/30**, F2 **28/30** | **PASS** — no weld |
| **E3 zero deaths** | 0 tracebacks | 0 across all 360 games | **HELD — but relabelled: CONCURRENT OBSERVATION, not a fulfilled prediction** (tape.sh auto-printed the count during generation, before the expectation commit; side-lane boundary catch, accepted) |
| **E4a front-side prep** | ≥1/3 of ON tube-games carry ≥1 FRONT prep | ON F1 17/30, F2 15/29 — **but CTRL reads 16/30 and 12/29: the bar as registered DOES NOT DISCRIMINATE.** The discriminating cut (per-barrier FRONT share): F1 0.298→**0.451**, F2 0.245→**0.506** | **BAR MET / BAR MIS-REGISTERED.** The steering mechanism is REAL (front share ~doubles, both fixtures) and the registered game-level bar was too weak to show it — scored as mechanism-confirmed WITH the registration defect on the record |
| **E4b heal dose** | ≥1 tube/screen heal per fixture ON | F1 ON **1** (one barrier heal, midgard_seatB r96); F2 ON **0** (nearest miss d²=9) | **FAIL — REGISTERED FALSIFIER FIRES: the heal rung is unreachable in practice.** The babysit half of the plank delivered no dose |
| **E5 life direction** | ON ≥ CTRL median life, F2, M7d | pooled 75.0→92.0 (+17) **but** cell-matched delta **+0.0**, horizon-normalised survival **+0.000 @h50 / +0.040 @h100**; game length moved 213.5→247.5 (censoring confound). F1: −0.044/−0.060 | **FLAT.** The pooled +17 is a censoring artifact; the honest read is no survival gain on F2 and mild negative on F1 |
| **E6 timely-checkmate guard** | ON F1 by-r300 core-kills within −2 of CTRL | CTRL **12** → ON **6** (**−6**); total wins F1 14→9, F2 8→5 | **FAIL — far outside the envelope.** The composite costs checkmates |

**⇒ v630.0 IS NOT ADVANCED TO THE POWERED READ.** Per the expectation's own
falsifier branches: E4b's failure alone sends the row back to design
regardless of levels, and E6's −6 (three times the envelope) makes the
composite off-programme in its current form (DEFENCE_ADMISSION_BAR
direction). Screens are 30-cell mechanism instruments (registered MDE ≈35pp)
— **no level sentence is typed**, but a mechanism that delivers no dose and
a guard that halves fixture checkmates is a design refusal, not a noise
question. This is a cheap, informative null: one flag, ~2 hours, and the two
defects are NAMED (below).

## 2. WHAT SURVIVES AND WHAT GOES BACK

**SURVIVES (mechanism confirmed):** the seat-bias steering. Front share of
prep barriers ~doubles on both fixtures with `_prep_barrier` itself
unchanged — the "orienting the screen = choosing where the engineer stands"
design fact is validated in-engine at screen scale.

**GOES BACK TO DESIGN, with measured defect hypotheses:**
1. **The heal rung is gated behind a branch the engineer rarely occupies at
   damage time** (hold branch requires `live >= want`; after a first tube
   death the engineer is in the siting path, where no heal rung exists) —
   F2 ON: 39 removals, 0 tube/screen heals. v630.1 must make the heal
   reachable from the siting path and from the prep-phase seat stand.
2. **The "on station: stand" returns are new terminal-idle states** (the
   parked-raider class, queue #48's own lesson): when prep is
   funding-blocked or cooldown-blocked the engineer now stands doing
   NOTHING where v628 wandered-but-acted. Suspected main contributor to
   E6's −6 alongside anomaly (2) below — attribution diagnostic
   commissioned before v630.1 is designed.
   **⛔ RIDER, added after the diagnostic ran (D14 closure): this hypothesis
   is REFUTED.** The E6 attribution (coordination tail 2026-08-22T19:11:10Z;
   scripts `scratchpad/s57_v630/e46_attrib*.py`) measured idle share
   FALLING under the guard (0.267→0.259 all bots, 0.445→0.421 engineer
   bodies; longest still-run 664→381) and offensive tempo unchanged
   (median rounds-to-500 enemy-core damage 121.0 in both arms). The real
   E6 mechanism is the HOME KEEPER relocating forward and ceasing core
   heals (core-footprint heals 398→80, the entire drop after r100; our
   core died in 21 ON cells vs 16 CTRL). The stand states remain in the
   code and remain a design smell, but they are not what cost the
   checkmates. Error direction logged at retro Q2: the refuted hypothesis
   was the one that flattered my own design instinct.
3. **Anomalies from the readout needing attribution:** ON builds **~25%
   fewer barriers overall** (F1 347→260, F2 320→246) while re-siting them
   frontward; F1 ON total team heals collapse 497→155; F2 ON adds 2 r1000
   games (defeats by doctrine). None of these was predicted.

## 3. READOUT AGENT REPORT (banked verbatim)

*The full agent report — instrument controls (§0: 10 controls, every
classifier driven to both verdicts, 180/180 seat-mapping agreement with
wrong-seat mutation flipping all 180), M-E4a/M-E4b/M-E5/M-E6 tables, summary
and anomalies — is preserved as delivered. Key tables are reproduced in §1;
scripts and raw numbers: `scratchpad/s57_v630/e46_lib.py`, `e46_controls.py`,
`e46_readout.py`, `e46_healdiag.py`, `e46_supp.py`. Anomaly 5 (12/160
forward-turret removals with no damage event, all sentinels, plausibly our
own `destroy` relocations — unconfirmed) is flagged to research as an M7d
ledger question with the nine cell/round anchors in the agent transcript.
Anomaly 1 (ID ≡ CTRL digit-for-digit on every computed column) independently
corroborates E1.*

## 4. NEXT (the mill)

1. E6/anomaly attribution diagnostic (readout agent resumed): which cells
   lost the checkmates, what the engineer did differently there, where the
   barrier count went.
2. v630.1 design from the attribution — candidates: heal rung in the siting
   path; stand states fall through to useful verbs; barrier-count
   preservation.
3. The powered read happens only when a screen delivers dose without the E6
   regression.
