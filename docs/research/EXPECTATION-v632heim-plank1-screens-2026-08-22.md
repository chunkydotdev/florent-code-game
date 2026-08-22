# REGISTERED EXPECTATION — v632heim PLANK 1 (citadel dispatch) screens

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition under organiser-approved rules.**

**PROVENANCE:** typed by BUILDER s57 and committed while the plank-1 build
agent is STILL RUNNING — registered blind to the produced code and to every
tape. Inputs: the banked design study (§2c plank-1 spec, §7 risks, §9 row 1),
PROGRAMME.md's doctrine fields (CITADEL_ZONE chebyshev-3, TARGET_ORDER
raiders-then-barriers, PRIO_LADDER p0-p3), the plank-0 baselines (P(core
alive@r300) = 53% F1 / 43% F2; F3 pending from the fixture agent), and the
bvb probe (builders cannot attack bodies — the dispatch body-answer is
block/deny, the kill waits for plank 3's ring).

**TREE:** `bots/_v632heim` = `_v628compose` + SK_FORTRESS/SK_CITADEL masters
(default OFF) + `_citadel_answer` dispatch + `SK_IDLE_ACT_ALL`. NOTE the base
still plays v628's full game (re-homing and the r300 flip are later planks);
this screen scores the DISPATCH alone.

**FIXTURES:** F1 Baltsars (`opp_v542wave_noiseoff`, seed 7), F2 Mjolnir
(`opp_mjolnir_noiseoff`, seed 11), F3 Sleipnir v2 (`opp_sleipnir2_noiseoff`,
seed 7) if its determinism proof lands clean — else F1/F2 and F3 joins the
next plank. Controls: fresh same-session `t_ctrl_*` per fixture (F1/F2 exist;
F3 from the fixture agent). Comparator READMEs in every stage dir (the s57
rule).

## Registered lines

**E1 identity:** flags-off tree reproduces the fresh control 30/30 per
fixture (`rdiff` per cell, checker driven to divergent verdict on a known
pair first). *Falsifier: any divergence ⇒ OFF-conjunction leak; halt.*

**E2 liveness:** ON arm diverges in ≥8/30 cells per fixture (all three
opponents raid constantly, so slot-2 fires and the dispatch reaches
behavior). *Falsifier: 0 ⇒ weld; 1–7 ⇒ under-reached; halt either way.*

**E3 tracebacks:** concurrent observation (health check, not a prediction):
expected 0 across all ON cells.

**E4 DOSE — the dispatch engages:** in ≥1/2 of ON games where ≥1 enemy unit
enters Chebyshev-3 of our core, at least one NON-DENIER body (keeper or
walker — the roles that never engaged before) performs a citadel act: a
structure-chew attack event inside the zone, or a body-block (our builder
adjacent to an intruder for ≥2 consecutive rounds where the CTRL cell shows
none). *Falsifier: below ½ ⇒ dispatch unreachable in practice — back to
code, no level reading.*

**E5 DIRECTION — intruder consequences:** enemy-structure dwell time inside
our half (build-to-destruction, censored) NON-INCREASING vs control per
fixture; intruder (enemy builder) time-in-zone reported both arms (with no
ring, plank 1 may not reduce it — reported, not gated).

**E6 GUARDS (the R1/E6 family, each within envelope vs control):**
(a) **P(our core alive @r300) NON-DECREASING per fixture** — the doctrine's
headline; falsifier: any fixture down by >2 cells ⇒ refused.
(b) core-footprint heals/game within −20% of control AND our-core-death
cells within +2 (the keeper-drift detector — the citadel must not unstaff
the core the way v630 did).
(c) eco-body-rounds/game within −15% of control (the CITADEL_ECON_RIDER:
the staffing fence holds; the zone answer must not stall the economy).
(d) by-r300 core-kill count reported per fixture with NO gate (the base tree
still kills pre-flip; under the phased doctrine kill drift is informational
for this line) — reported honestly, never hidden.

## Scope

30-cell deterministic screens; MDE ≈35pp; mechanism and guard reads only, no
level sentence. Adoption of plank 1 = E1–E4 pass + E6(a–c) inside envelopes;
E5 informs plank-2/3 sizing. The powered read waits for the plank stack
(dispatch alone is not expected to move survival much — the ring kills, the
dispatch only organizes; a flat E6(a) with clean E4 dose ADVANCES the plank).
