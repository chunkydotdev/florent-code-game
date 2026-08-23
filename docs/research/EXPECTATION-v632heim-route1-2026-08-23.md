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

## VERDICT — REFUSED per R4; UNDER-PLAYED in part, routes to ROUTE arm 2 (BUILDER s57)

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition.**

R1 90/90. R2 direction right but small (zero-delivery −1/−1/0; routed
share rises 1/3; diagnosed conversions 2/10, the 4 launcher-denial cells
0/4 as predicted). R3: F1 delivered +13.8% at flat ratio; F2 −16.7%.
**R4 FAILS — the primary:** ≤r300 ITT −0.100 on F2, −0.033 on F3;
kills-sum 22→19; median game length rises on all three fixtures — wins
arrive LATER (wins-sum +2 but the currency is timely checkmate, and
R1000_IS_DEFEAT stands). R5 guards all favourable (alive 57, eco +6.1%)
— survival bought at kill speed, the trade the programme scores against.

**EXECUTION-QUALITY LINE:** the audit fires early and broadly (63/90
cells from r5-r10) but converts 2/10 named targets; TWO diagnosed cells
are byte-identical — never engaged (a reach defect, not a refuted
tactic). Dose achieved is a small fraction of achievable. **UNDER-PLAYED
⇒ no strike on the plank.**

**ROUTES TO ROUTE ARM 2:** (a) engage-the-unengaged — diagnose why
icefloe_seatB F1 / skald_seatA F2 never diverged (audit weld on their
shape); (b) THE CORRIDOR — the launcher-denial class (4/4 unconverted:
enemy structure holds the link, their launcher relocates our body before
it can act; candidate answers: approach-side variation, clear the
launcher first, far-side link completion); (c) a TIMELINESS rider — the
route rung must not displace kill-supporting turns late (the later-wins
regression is the registered subject, not a side note). SK_ROUTE_HOME
stays built, OFF.
