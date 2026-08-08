# E1 — CAD-family incoming-side plank: design pass (builder arm, s18, 2026-08-08)

STATUS: DESIGN ONLY. Build is deliberately sequenced behind research's
fjordgate-collapse read (same under-siege subsystem; one gated change).
Machinery inventory landed (§5); design shape proposed (§6); acceptance §7.

## 1. The problem, in the tape's numbers

- Eir 8 production read §2.4 (primary): vs CAD-family our staffing is FINE
  (bodies/damage-round 3.32, heal/incoming 0.82–0.97) and cores die anyway.
  Incoming 18.06 HP/r (highest sustained in the rated corpus) vs heal 11.55
  HP/r = **6.5 HP/r structural deficit**. Eight staffed heal seats would be
  32 HP/r but we seat 3.3 — and the read's verdict stands: this class is a
  **damage-suppression problem wearing a heal-line costume**.
- Therefore the lever is killing/suppressing the source turrets, not more heal.

## 2. The decoded asymmetry that makes suppression cheap (refreeze spec §4.2)

- CAD answers turrets planted within **d²≤36 of THEIR core**: counter-gunner
  at d²≤13 of our turret, 100% coverage, median latency 15.5 r, 76% killed,
  median lifespan 16.5 r. Sentinels specifically: 76% killed, life 27 r.
- **Beyond d²≈64 of their core CAD does essentially nothing**: our turrets
  survive 237–377 r median, 11–19% killed, counter "hits" incidental.
- CAD's siege turrets shelling OUR core are, by construction, far from THEIR
  core — i.e., **inside the zone where CAD structurally cannot answer our
  counter-battery**. Anything we plant or do near our own core is unanswered
  by the decoded mechanism (95.6% of counter-damage is gunner counter-plants,
  and those only trigger near their core).
- Decay assessment (exploit brief item 4): moderate — CAD oscillates between
  decoded endpoints; opening byte-stable across all three archived stamps
  (v107/v116/v117); the book transfers across their churn.

## 3. Arithmetic targets for the design

A CAD gunner does 7 dmg / reload 1 ≈ 7 HP/r on one lane; their sentinel 18
dmg / reload 2 = 9 HP/r. The measured 18.06 HP/r ≈ 2–3 active shellers.
To close a 6.5 HP/r deficit we need EITHER:
- (a) kill one median sheller and keep it dead (denies 7–9 HP/r), or
- (b) suppress ~1 sheller-equivalent continuously.

Counter-battery math near our core:
- Our gunner (7 dmg/r) kills a 25 HP gunner in 4 r, a 40 HP sentinel in 6 r —
  ammo cost 16 / 24. At 1:1 Ti:ammo that is 16–24 Ti per killed sheller —
  vs the heal-side answer (6.5 HP/r deficit ≈ 1.6+ Ti/r forever). Suppression
  is an order of magnitude cheaper per HP when it connects.
- Builder attack: 2 dmg / 2 Ti, adjacency-gated. Killing a 25 HP gunner by
  builders alone = 13 builder-turns + 26 Ti, no ammo. Slower but ammo-free;
  pairs with the "a turret shelling the core does not shoot back at its
  attacker" standing fact (traps list).

## 4. Prior art to consume or retire (verdicted rows only)

- **C1b home ring** (_v83c1b, KEEP-dev, s15 tape): arming+supply proven, 85%
  at wild-median load (KCM farm-recovery number). Mechanism summary pending
  diagnostic agent; candidate = its ring siting + supply agreement, re-cut
  for the CAD envelope.
- **S1 intercept own-building guard** (shipped in v73 content; in the v80
  base lineage): scope check pending inventory.
- **wb reserve agreement** (_v93wb, parked): its archb evidence (r732 loss →
  r1000 WIN with RA-off control byte-reproducing the loss) shows ammo
  LIQUIDITY gates the home response class-wide. Whatever E1 plants must not
  starve at the moment of contact — the RA idea returns here as a component,
  not as the wb branch (which failed its re-gate 0/24 vs cad_probe).

## 5. Machinery inventory (diagnostic agent, landed 2026-08-08 ~17:1x;
##    line numbers = _v89sh/main.py unless noted)

What v80 already has, and why it loses the 18 HP/r race anyway:

- **_hunt_turret (3121-3303)** — builder-melee peck at enemy turrets,
  2 dmg / 2 Ti, TWO modes (research spot-check correction, source-verified
  3145-3175): CORE-SIEGE mode gates on round ≥ HUNT_MIN_RND=120 AND the
  core already visibly bleeding (_core_shelled, 3168), band d²≤41 from
  the core footprint; ECO-SIEGE mode runs at ANY round with NO core
  evidence when an enemy turret sits orthogonally adjacent to a friendly
  HARVESTER, any range from core (3193-3198) — prior art for "turret
  qualifies by what it is doing, not where it is." BOTH modes require
  the hunter ALREADY within HUNT_DESIGNATE_DSQ=8 of the gun (3209; no
  dispatch/recall — the load-bearing gap for E1); healer floor (3274)
  blocks hunting below the floor. 2 dmg/r vs a 7-9 HP/r sheller is not
  a suppression mechanism — it's a finisher (HUNT_FINISH_HP=8 exemption
  is the honest part of it).
  MEASURED PRECEDENT IN ITS COMMENT BLOCK (3155-3159, directly relevant
  to any ring re-cut): conveyor-adjacency triggering was REFUSED because
  ambient early hunting cost eider 8/16→0/16 AND caused a fjordgate rush
  regression — the same over-trigger risk class any E1 arming signature
  must be ablated against, and a fjordgate failure mode already on file
  pre-dating the collapse-owner read.
- **_try_counterbattery (3305-3403)** — the only home turret-plant. Fires
  only from wherever a builder ALREADY stands with a legal ray to the
  SLOT_THREAT tile (3388-3394); no walk-to-firing-position. Bootstrap
  gate: second turret blocked below 3 harvesters unless core provably
  bleeding (3332-3348).
- **Turret return-fire (4697, priorities 4746-4751)** — our standing guns
  rank enemy SENTINEL/GUNNER right behind CORE, but only reactively
  within own range; sentinels can never re-aim (no rotate()).
- **Under-siege ammo response exists (1666-1706)**: target 16→24 when
  under, ti_floor 52→12. Converts at most 16/turn — fine for gunner
  shots, thin for a sentinel duel (10/shot).
- **C1b machinery is ENTIRELY ABSENT from v80** (zero grep hits): no
  _plan_homering walk-to-position planner, no HOME_RING_CAP=3 coverage
  dedup, no arming gate (C1B_ARM_RAIDER_DSQ=64 could-not-have-walked
  insertion signature, 12/12-vs-0/12 class separation), no second-
  responder supply (C1B_SUPPLY_ON; 18/60 games zero-covered motivated it).

GAP SUMMARY (agent's §F, confirmed): v80 can only counterbattery by
coincidence of position; nothing walks a builder to a firing spot, nothing
proactively suppresses a fresh sheller before the core bleeds, nothing caps
or dedups home turret coverage. The C1b branch built exactly these three
things and its verdict was KEEP-dev (85% at wild-median load).

## 6. Proposed design shape (for the build cycle, post-fjordgate-read)

**E1 = C1b's three mechanisms grafted onto the v80 base, re-cut for the
CAD envelope**, NOT a new mechanism. Deltas vs C1b as-parked:

1. Ring planner (_plan_homering port): keep walk-to-firing-position +
   ray-covers-threat siting + HOME_RING_RETFIRE_PEN. Sentinel-first
   against CAD (their counter-damage is 95.6% gunner counter-plants that
   only trigger near THEIR core — our home ring is unanswered; and our
   sentinel two-shots their 25 HP gunner class).
2. Arming gate: keep C1b Signature 1 (insertion, could-not-have-walked)
   AND add the s14 predictor as Signature 3: ≥2 enemy turrets inside
   d²≤41 of our core footprint (the CAD-family shape is shellers, not
   raiders — Signature 1 alone may never arm vs pure standoff shelling).
   Turret-signature re-tax risk is priced by the ablation grid, not
   assumed away (C1b's Signature 2 was refuted once already — this is
   its return with a different predicate; it must re-earn its place).
3. Supply/second-responder: port as-is (C1B_SUPPLY_* constants).
4. Ammo liquidity at contact (the wb lesson, component-sized): when the
   ring is armed and a ring turret stands, raise the convert cap from 16
   so a sentinel duel is fundable same-turn. NOT the wb reserve-agreement
   branch (0/24 re-gate); just the cap.
5. FJORDGATE GUARD (pending research's read): whatever arms the ring must
   not deepen the siege-first starvation — the disc showed the under-siege
   latch already runs zero economy on gate maps, AND the _hunt_turret
   comment block records a measured fjordgate rush regression from ambient
   early hunting (§5) — two independent fjordgate failure modes for the
   arming gate to avoid. The ring build budget must come from
   _eco_spendable's siege reserve mathematics, never from the
   harvester-bootstrap budget. Final form waits on the read.

## 7. Acceptance sketch (to be finalized post-inputs)

- Class-weighted battery per standing ship policy; CAD-family legs primary
  (cad_probe attribution-only + wild-era anchors via unrated where possible).
- Ablation grid: plank on/off vs cad_probe + at least one non-CAD guard
  class (kladde, band) for the no-regression leg.
- Mechanism instrument: incoming HP/r at our core + sheller lifespan near
  our core, replay-derived (instr.py pattern from fjord_disc reusable).
- Refreeze-spec E-items (E1/E2/E3) remain the PROBE's acceptance for the
  separate CAD re-freeze work item — not this plank's gate, but the rebuilt
  probe is the preferred instrument for this plank's battery if the quiet
  window arrives first.
