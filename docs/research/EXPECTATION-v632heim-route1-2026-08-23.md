# REGISTERED EXPECTATION — ROUTE arm 1: ROUTE-HOME REPAIR (SK_ROUTE_HOME)

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition. All terms are in-engine mechanics.**

**PROVENANCE:** BUILDER s57, committed before the build agent runs. Plank:
THE ROUTE (three-plank lock). Inputs: LOSSAUT-f1f2 (13 zero-delivery
cells; harvester/conveyor BUILD counts identical wins vs losses — the
difference is the ROUTE; mine rate 1.21 loss / 2.39 win; out-mined
38/41; all 4 r1000 games lost on key 1), Magnus's own observation ("we
don't seem to rebuild a disconnected conveyor belt"), baseline t_cs_*.

**MECHANISM (diagnose-first, then fix):** the build agent first traces
WHY the 13 cells deliver zero — never-routed (harvester built, line never
laid) vs cut-and-never-rebuilt (enemy removed a segment; nothing re-lays
it) — with per-cell classification, then builds the fix the classification
names: a route-audit rung that detects a harvester with no conveyor path
to the core and lays/re-lays the missing segments, budget-gated,
siege-aware (never at the stand's expense).

**Bars:** R1 identity OFF ≡ t_cs_* 30/30 ×3. R2 mechanism: zero-delivery
cells fall vs measured 13 (F1+F2); routed-harvester share rises. R3
execution quality: delivered Ti / emitted Ti per harvester reported both
arms (the achievable reference is emission). R4 currency: ≤r300 ITT
non-fall; tiebreak-decided cells reported (key-1 margin). R5 guards:
alive-sum [53,−2] deaths [49,+4] harv [212,−10%]; eco-sum EXPECTED TO
RISE — reported. Adoption per bars; a fail routes to ROUTE arm 2.
