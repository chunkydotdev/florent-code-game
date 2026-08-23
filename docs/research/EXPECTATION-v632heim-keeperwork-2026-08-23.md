# REGISTERED EXPECTATION — v632heim KEEPER WORK-AT-POST (SK_KEEPER_WORK)

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition. All terms are in-engine mechanics.**

**PROVENANCE:** typed by BUILDER s57, committed BEFORE the build agent runs.
Inputs: the nav-stall verdict (EX-1 keeper-ring masses 979/942/1,477
measured load-bearing — removing the hold kills our core r733 vs r1000,
n=2 unpowered), the ARM B withdrawal note (leashed keeper laid ONE conveyor
in 849 rounds), the adopted-NS baseline t_ns_* MEASURED [alive 54 / deaths
50 / wins 34 / kills 22 / eco 38.27 / harv 216].

**MECHANISM TARGETED:** a keeper holding station at the core ring (leash /
core-anchor fall-through) emits NO VERB for hundreds of rounds in
peacetime. Verbs do not move a builder — holding the post and working are
compatible. The plank adds WORK, never movement.

**DESIGN CONSTRAINTS (registered):**
- The body's POSITION LOGIC IS UNTOUCHED — no new movement, no new targets;
  the flag gates verb emission only, on rounds where the existing code
  would emit nothing.
- Work priority from post (all orthogonally adjacent only, per engine):
  (1) heal a DAMAGED adjacent friendly tile (core footprint included, 1 Ti,
  only when hp < max); (2) repair-adjacent belt need (build a conveyor on
  an adjacent tile ONLY where the belt-continuity logic already recognises
  a break — no speculative belt); (3) barrier maintenance on an adjacent
  ring seat the fort logic already claims. NOTHING speculative: every build
  verb must cite an existing need-recognition path in the tree; a new
  need-heuristic is out of scope for this flag.
- Spend cap disclosed (heals are 1 Ti; builds at scaled cost — the scale
  ratchet means idle conveyor-spam is a real hazard, +1% each, and the
  build agent states the cap and the reasoning).

## Registered lines (arm `kw` = SK_KEEPER_WORK=True vs t_ns_* baseline)

**K1 identity:** OFF ≡ t_ns_* 30/30 ×3. *Falsifier: divergence ⇒ leak; halt.*

**K2 seen-working (mechanism, deterministic traces):** on the specimen
cells (bifrost_seatA, jotunheim_seatA F1), the keeper-ring hold emits >0
verbs ON where OFF emits 0 across the hold span; the body's tile sequence
over the hold is UNCHANGED (position untouched — this is the load-bearing
half and it is a falsifier: any movement delta in the hold span ⇒ the flag
leaked into movement; halt).

**K3 DOSE:** core-footprint heals/game per fixture (baseline MEASURED at
readout time from t_ns_* — the readout states it before comparing) rises
where damage exists; AND the ≥50r no-verb stationary pool falls (verbs
break runs — the instrument's own definition; reported per fixture).
No % bar pre-set: the damage-opportunity denominator is unknown before the
readout measures it. The dose line is CONDITIONAL seen-working: where a
damaged adjacent entity coexists with a held post, the heal fires.
Opportunity itself is a reported column (the inert-guard lesson).

**K4 GUARDS (the load-bearing lines):** alive-sum within −2 of **54**
(THE bar — the hold must keep holding); death-sum within +4 of **50**;
eco-sum within −12% of **38.27**; harv within −10% of **216**; global
resources trajectory sanity-read (the spend cap holds); wins/kills
informational (34 / 22; per-fixture wins 10/9/15).

**K5 tracebacks:** 0 expected.

## Adoption rule (pre-registered)

Adopts if K1, K2 pass (including the position-unchanged falsifier), K3
shows conditional seen-working with honest opportunity columns, K4 holds.
A zero-opportunity fixture is not a fail — it is a reported zero. If the
spend cap is ever the binding constraint in >half the working rounds, the
cap design returns rather than being silently raised.
