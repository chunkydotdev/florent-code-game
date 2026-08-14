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

---

# STEP 2: GAP TABLE (separate commit, AFTER the classification above — ordering provable in git)

**Method for legs (matched surfaces):** gap = (screen_T − 50) − (live_T −
live_control), live_control = the pinned A-arm at the same five cells
(12/25 = 48%). This removes cell hardness, which the raw screen−live
difference confounds. **For SALT and MAPCODE no matched leg exists** (prereg:
"rated break-in delta where legs don't") — their live evidence is the ship
record, incommensurable in pp; sign and rough magnitude only, said so.

| arm | class (step 1) | screen excess | live excess (vs 48% control) | GAP (flattery) |
|---|---|---|---|---|
| UNDERECO | coupled | +1.56 | 9/25 = 36% → −12 | **+13.6pp** |
| COMBO | coupled | +2.31 | 10/25 = 40% → −8 | **+10.3pp** |
| APPRLAUNCH | coupled | +2.68 (pooled 5005/9500) | 10/25 = 40% → −8 | **+10.7pp** |
| ECORAID | coupled | +3.77 (pooled 4508/8383) | 23/50 = 46% → −2 | **+5.8pp** |
| **TWORAID** | coupled | +0.63 | 13/25 = 52% → **+4** | **−3.4pp — NO FLATTERY** |
| MAPCODE | decoupled | +23.27 (⚠ control era: `_v187saltidle_f`) | ship record: zero-drawdown break-in, validated climb | **~0 — transferred** (imprecise bound) |
| SALT | coupled (hard case) | +11.00 (⚠ control era: `_v169launchlate160`) | ship record: validated on ladder | **~0 — transferred** |

## VERDICT AGAINST THE REGISTERED PREDICTIONS
* Registered: coupled mean gap ≥ +5pp; decoupled |gap| ≤ 2pp.
* **FALSIFIED-AS-UNIVERSAL, twice over: SALT (the pre-named hard case) is
  coupled-with-transfer, and TWORAID is coupled with gap −3.4pp.** Decoupled
  prediction holds on its single row (MAPCODE).

## THE PRE-NAMED REFINEMENT, SCORED
*"Coupling flatters only when the exploited behaviour DIFFERS between our
incumbent and the field."* Applied row by row:
* SALT exploits belt repair — **field-universal** (40.5%), incumbent repairs
  too → predicts transfer ✓
* TWORAID's payoff is out-damaging repair/heal — **field-universal** →
  predicts transfer ✓ *(the refinement's only genuinely out-of-sample hit —
  it was pre-named against salt, not against TWORAID)*
* UNDERECO exploits the CHRONIC-CAMP response — incumbent kills at median
  ~167 and does not chronic-camp (self-play camp exposure ≈ absent) →
  predicts flattery ✓
* APPRLAUNCH's trigger is point-blank CREEP — incumbent never creeps
  (99.7% harvester-first, no ladder) → predicts flattery ✓
* COMBO/ECORAID contain UNDERECO → predict flattery ✓ (+10.3 / +5.8, ordered
  as expected with DIGOUT removed)
* MAPCODE decoupled → transfer ✓
**7/7 signs predicted.** ⚠ Honest weight: the refinement was authored knowing
salt's outcome; TWORAID is its only clean out-of-sample success. **It is a
surviving hypothesis, not a confirmed rule — the prospective probes (GBNS,
L4REPAIR, and #8 as the decoupled contrast) are the real test, predictions
already registered in the prereg.**

## Caveats carried
Screen controls span three eras (v197 for the legs; `_v169`/`_v187` for
SALT/MAPCODE) — the excess is vs different bases where flagged. Live leg
cells are n=25-50; the A-control is n=25. SALT/MAPCODE live evidence is the
confounded ship record, sign-grade only.

---

## AMENDMENT A (ADD-only) — interpretation pinned + one audit disagreement recorded

**Race disclosed first:** the side lane's audit of the two flagged rows was
completed against the rule text before step 2 was pushed, but its message
crossed the step-2 commit in flight — so the interpretation line below lands
AFTER the gap table, not before as the audit requested. The protection the
ordering was for is intact in substance: **no classification changed after
gaps were known** (TWORAID was COUPLED in step 1 and remains COUPLED), and
this amendment formalizes the reading rather than altering any row.

1. **INTERPRETATION PINNED (side lane, upheld): "payoff" = THE PAYOFF AS
   REGISTERED IN THE ARM'S OWN PREREG/WORKLIST TEXT**, not a generic reading
   of the mechanism. TWORAID is COUPLED because its registered payoff (#42)
   is denominated on out-healing (4 HP/Ti vs 1.8 dmg/Ti); under a generic
   "double DPS vs any core" reading it would flip DECOUPLED. The registered
   text governs. *(Routed to the builder to mirror as an ADD-only line in
   the prereg itself — their file.)*
2. **QUIET0 — AUDIT DISAGREEMENT RECORDED, UNRESOLVED, AND MOOT FOR STEP 2.**
   Research classified COUPLED (payoff clause via pecks-vs-heal); the side
   lane reads DECOUPLED by the registration text (#48 joint prereg states
   the payoff as the wholesale doctrine read from builderAttack counts; the
   anti-heal framing entered later). Under the now-pinned interpretation the
   side lane's reading is the stronger one. **Both readings stand recorded;
   QUIET0 entered no gap row (no live surface — cancelled pre-live), so no
   gap tests it either way.**

---

## AMENDMENT B (ADD-only) — salt's transfer mechanism, one level deeper (repairer fixture validity run)

The `_probe_repairer` build (43.0% repair rate vs 40.5% field target, median
latency 4 = field exact) banked a fact that sharpens this table's salt row:
**SALT DENIES REPAIR BY CONSTRUCTION — 6/6 of the incumbent's cuts received
the corpse-barrier within 1-2 rounds, inside any notice delay, so the
defender never sees an empty tile.** The refinement's salt entry ("transfers
because belt repair is field-universal") therefore understates it: **salt
does not merely exploit a universal habit, it PREEMPTS the habit's counter.**
A plank that removes its own counter-play is coupling-safe in a stronger
sense than the refinement requires — worth remembering when classifying
future planks: "does the payoff survive the opponent's response" is a
different and better question than "does the opponent exhibit the behaviour."

**Test-design decision (research, as spec owner) for the refinement's
prediction test:** the salt-class plank screened vs the repairer will be the
BARE-CUT arm (`_v190saltcutonly`) against the repairer AT FIELD RATES
UNCHANGED — not a delay-widened repairer. Widening the delay to make the
test possible would degrade a measured-fidelity fixture into a convenient
one (the anti-Goodhart rule applied to test design). The bare-cut arm keeps
the repair interaction alive, which is the exposure the prediction is about.
