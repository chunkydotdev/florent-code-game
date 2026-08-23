# REGISTERED EXPECTATION — v632heim NAV-STALL DETECTOR (SK_NAV_STALL)

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition. All terms are in-engine mechanics.**

**PROVENANCE:** typed by BUILDER s57, committed BEFORE the build agent runs.
Inputs: diagwg_* diagnostic (banked in the survival expectation's verdict),
e46wg_* readout, the adopted-WG baseline tapes t_wg_*. Control values below
are MEASURED on t_wg_* (the new baseline), never assumed.

**MECHANISM TARGETED (measured, three specimens):** a walk selects a target,
`step_to`/`_nav` yields no step, the role falls through with NO VERB —
silently, indefinitely. Specimens: bifrost_seatA bot 237 (686r on ore, TWO
FREE NEIGHBOURS — not boxed), bifrost_seatA bot 3 (979r keeper nav-stall at
(2,4), `_hl_walk_target→_on_eligible_ore→_nav` no `_move`), midgard_seatA
bot 3 (38r, `_escalate_target→_nav` no `_move`). This is the #131 family;
the fix sits at the WALK EXECUTOR level (all walks), not per-site.

**DESIGN CONSTRAINT (registered):** detector = N consecutive rounds with
(alive, no verb emitted, no tile change, walk target unchanged-or-None) →
re-pick with the current target banned (the walk-target ban class, 20r,
precedent SK_WALK_GUARD_BAN/SK_CURSOR_GIVEUP). OFF byte-identity mandatory.
The detector must NOT fire on legitimate stationary states (parked-raider
prestage hold, keeper at post, cooldown waits) — exemptions disclosed in
the build report, each with the state it protects.

## Registered lines (arm `ns` = SK_NAV_STALL=True vs t_wg_* baseline)

**N1 identity:** OFF tree ≡ t_wg_* 30/30 ×3 (rdiff, checker driven divergent
first). *Falsifier: divergence ⇒ leak; halt.*

**N2 seen-firing (mechanism, deterministic cell traces):** env-gated stderr
tracer (the validated diagwg pattern, tracer-inert byte-check mandatory) on
bifrost_seatA F1: the stall counter fires >0, and any traced no-verb
stationary walk run terminates within N + re-pick window. *Falsifier: counter
0 in a cell with a measured stall ⇒ weld; a traced park surviving the
detector ⇒ exemption swallowed the class; halt either way.*

**N3 DOSE — the global pool IS the honest instrument now** (the guard-site
classes are extinct; the residual ≥50r mass is this class): three-fixture
stationary-runs-≥50r rounds vs baseline MEASURED **16,909** (F1 4,621 /
F2 5,950 / F3 6,338): bar **sum ≤ −25%**, per-fixture signs reported.
Censoring caveat registered: total rounds per fixture reported alongside
(baseline 8,983 / 10,861 / 10,510) — a pool fall bought by shorter games is
disclosed, a pool rise from longer games is not a fail on its own if the
per-round rate falls (rate = pool/total-rounds, baseline 0.514/0.548/0.603,
reported).

**N4 guards:** alive-sum within −2 of **53**; death-sum within +4 of **53**;
eco-sum within −12% of **36.00**; harvesters within −10% of **209**;
wins/kills informational (baseline 32 / 18; F1 8, F2 9, F3 15).

**N5 tracebacks:** 0 expected, concurrent observation.

## Adoption rule (pre-registered)

Adopts if N1, N2 pass, N3 meets the bar, N4 holds. If N2 passes and N3
misses the bar but the pool falls with rate falling on ≥2 fixtures, adoption
is hardening-grade at builder discretion with the shortfall disclosed. If
the detector's exemption list grows past 4 states, the design returns —
an exemption lattice that big is the always-true `_under_attack` lesson.
