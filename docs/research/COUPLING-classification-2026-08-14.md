# COUPLING TEST — STEP 1: CLASSIFICATION TABLE (committed BEFORE the gap table)

**Research s38, 2026-08-14. Per `docs/prereg/TEST-coupling-hypothesis-2026-08-14.md`:
the rule is applied to MECHANISM TEXT ONLY; no outcome column appears in this
file. The gap table lands in a SEPARATE, LATER commit so the ordering is
provable in git. Honest limit acknowledged in the prereg: both lanes know most
outcomes; the mitigation is the mechanical rule + side-lane audit of each row
against the rule text, not against plausibility.**

**RULE (verbatim from the prereg):** *"coupled iff the payoff requires the
opponent to exhibit a specific behaviour (siege, repair, ladder, belt layout)
rather than being invariant to opponent identity."*

| arm | mechanism (from its own registration/worklist text) | classification | rule clause engaged |
|---|---|---|---|
| MAPCODE | "Pure-data treatment (10 EXTRA_MAP_CODES entries)" — per-map opening pool keyed on map name | **DECOUPLED** | payoff invariant to opponent identity (map knowledge only) |
| SALT | per-unit peck budget on the ENEMY BELT (LOKI_SALT_CUT_MAX; salt cuts on their conveyors) | **COUPLED** | requires opponent belt layout to exist and repair behaviour to be worth taxing — *the prereg's named hard case* |
| UNDERECO | income-lock fix: bank behaviour when the enemy ring-camp latches `under` (siege state) | **COUPLED** | payoff requires opponent SIEGE — fires only in sieged games |
| TWORAID | build sequencing toward two simultaneous forward siege sentinels | **COUPLED** (narrowly) | the BUILD is self-directed, but the registered payoff (out-damaging belt/core HEALING; the volume-not-sequence finding) requires opponent repair behaviour. By the rule's letter — payoff requires "repair" — coupled. Flagged as the classification most sensitive to wording; side lane please audit this row hardest. |
| DIGOUT | blocked-on-all-cardinals builders destroy their OWN barriers (self-unwalling) | **DECOUPLED** | own-state trigger, invariant to opponent (listed for completeness; live evidence is via COMBO/ECORAID contrast only) |
| COMBO | composition UNDERECO + TWORAID + DIGOUT | **COUPLED** | contains coupled components |
| ECORAID | composition UNDERECO + TWORAID (DIGOUT removed) | **COUPLED** | contains coupled components |
| APPRLAUNCH | launcher built on APPROACH DETECTION (enemy builder inbound), for feeder eviction | **COUPLED** | trigger and payoff require opponent creep/siege behaviour |
| GUNAXIS0 | (screened; live evidence?) `LOKI_GUNAXIS_PENALTY` ablation — our own pathing constant | **DECOUPLED** if admitted — own pathing; listed pending live evidence check in step 2; if no live surface exists it drops from the gap table |
| QUIET0 | re-enable our builder melee (constant ablation) | **DECOUPLED** by trigger (own action ladder) — but the PAYOFF (pecks trading vs heal) engages opponent repair; classified **COUPLED** by the rule's payoff clause. Second-hardest row; audit against text. |
| IDLEPECK / `_v208` | idle parked raiders peck the adjacent enemy CORE | **COUPLED** (payoff requires the parked-adjacency the camp class creates) |

Rows enter step 2's gap table ONLY where both a screen final and live/rated
evidence exist at read time; the classification above stands regardless.
