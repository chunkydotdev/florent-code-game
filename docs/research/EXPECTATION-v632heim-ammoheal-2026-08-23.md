# REGISTERED EXPECTATION — v632heim AMMO THROUGHPUT + CORE-HEAL STAND (the autopsy levers)

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition. All terms are in-engine mechanics.**

**PROVENANCE:** typed by BUILDER s57 BEFORE the build agent runs. Inputs:
LOSSAUT-f1f2-2026-08-23.md (banked; instrument controls both-verdict-driven)
and the t_cp_* baseline [alive 54 / deaths 51 / wins 34 / kills 21 / eco
36.87 / harv 216; per-fixture wins 10/9/15]. Control values all MEASURED by
the autopsy: conv median 350 loss / 726 win; conversion share 0.26 / 0.43;
gross core-damage rate 1.47 / 4.30 HP/round; our core-heal rounds median 0;
enemy absorption: net = 0.424 x gross − 0.245, sustained enemy heal ceiling
~6.5 HP/round.

**ARMS (each vs t_cp_*; composite per the plank-4 precedent — the autopsy
measured the levers COUPLED: ammo alone +2/+1 wins, heal alone +5/+1,
joint +14/+10 discounted):**
- `ap` — SK_AMMO_PUSH only: core conversion policy raised toward the win
  regime when we hold firing ground (in-range turret exists / offensive
  phase), above a spawn-and-build reserve floor. Design latitude to the
  build agent on the trigger read and floor; every constant disclosed.
- `cs` — SK_CORE_STAND only: a home body heals the core footprint under
  active enemy turret fire (the capability exists and fires in 3 of 8
  threatened wins — the build agent's first job is to find WHY it does
  not fire in the other 5 and lift THAT, not to add a parallel rung).
  Target rate ~1.65 heals/round during a siege (~1.65 Ti/round), cancels
  the measured 6.6 HP/round closing rate.
- `apcs` — both flags.

## Registered lines

**Z1 identity:** OFF ≡ t_cp_* 30/30 ×3. *Falsifier: leak; halt.*

**Z2 AP mechanism:** conversion share (conv / Ti income) rises vs measured
0.26-loss/0.43-win baseline on ≥2 fixtures; ammo-starved rounds (in-range
turret, cooldown 0, ammo < shot cost) FALL; spend/convert stays ≥0.9 (we
buy only what we fire). *Falsifier: share flat with the flag ON and
opportunity present ⇒ policy weld; halt.*

**Z3 CS mechanism (conditional seen-working):** in cells where an enemy
turret ranges our core AND a home body is alive with bank ≥1, core-heal
rounds > 0 (baseline median 0); opportunity columns reported. Our-core
survival rounds under siege extend. *Falsifier: zero heals with
opportunity present ⇒ the 5-of-8 defect uncured; halt on the cs arm.*

**Z4 THE CURRENCY (composite primary, per DEFENCE_ADMISSION_BAR):** the
by-r300 timely-checkmate ITT share must NOT FALL vs baseline (kills 21;
per-fixture ≤r300: measured at readout from t_cp_*). Gross core-damage
rate on loss-class cells rises toward the 4.5 HP/round band — reported per
band (the autopsy's <1.86 / 1.86-4.48 / ≥4.48 cells).

**Z5 GUARDS (all arms):** alive-sum within −2 of 54; deaths within +4 of
51; harv within −10% of 216; eco-sum within −20% of 36.87 (WIDENED vs the
standard −12%, disclosed now: conversion COMPETES with builds by design —
the trade is the plank; the harvester line is the one that must hold).
Wins informational with the honest hope stated: the autopsy's discounted
joint figure is +14/+10 — any wins-sum rise is the first outcome movement
of the campaign's screen series.

**Z6 tracebacks:** 0.

## Adoption rule (pre-registered)

Each single arm adopts on its own mechanism line + Z4 + Z5. The composite
ships as the new baseline if Z4 holds and wins-sum does not FALL; if the
composite beats both singles on wins-sum it is preferred outright. Map
clustering (5 maps 0/4, DEFF ~4.57) means win-count deltas under ~4 are
noise — reported, not banked as level claims.
