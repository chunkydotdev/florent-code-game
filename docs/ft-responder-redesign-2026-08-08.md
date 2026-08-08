# FT-responder redesign: under-siege release semantics (builder arm, s18)

STATUS: DESIGN. Build is the next registered cycle on the _v95e1 dev head.
Line refs are _v95e1/main.py at md5 of the M2b row.

## 1. The evidence base (all measured)

- Detector EXONERATED (research, 3× confirmed): ferried() precision 1.000;
  under=2 is downstream-inert (2 ≡ 1 by truthiness at every reader).
- The DEFECT is release: SLOT_ATK_RND (:2177, :2733, :2767) is refreshed by
  mere SIGHTING — any enemy turret within gun_sense=64 or builder within
  b_sense=16 of the core anchor, every round it stays visible. The 50-round
  decay (:2179-2185) therefore never fires while anything is parked in
  vision: 72/72 disc games never released; meander's parked forward
  sentinels re-trigger plain proximity forever.
- The latch length itself is LOAD-BEARING the other way (atoll decode,
  comment at :2179): a harasser parking JUST outside trigger radii let a
  35-round latch expire between pokes — ammo magazine collapsed to one shot
  on 2,782 banked Ti. Shortening the latch or requiring damage for the
  AMMO tier re-opens that hole. THE TWO LESSONS CONFLICT ONLY IF SEVERITY
  IS BINARY.
- Cost of the all-game pin, priced this session: fjordgate-B r1
  builder-SIGHTING latch → siege-first opening, zero harvesters 392 rounds
  (fixed downstream by the FB floor, but the posture tax — recalls,
  heal-over-eco, eco caps, hunt gates — runs all game); meander seat-A
  0-Ti collapses; FT r4 pin in every non-fjordgate-B disc game.

## 2. Design: severity tiers in SLOT_UNDER's existing value space

No free store slots (16/16 assigned). Encode severity in SLOT_UNDER itself,
preserving truthiness for every existing reader:

| value | meaning | written on |
|---|---|---|
| 0 | clear | decay only (existing) |
| 1 | AMBIENT — sighting-fresh | turret-in-gun_sense / builder-in-b_sense sighting (existing writers) |
| 2 | INSERTION — ferry-confirmed | ferried() (existing writer, unchanged) |
| 3 | DAMAGE — core/buildings bleeding | hp < last_hp (:2168-2170), currently folded into plain `under` |

Rules: 3 and 2 are both "severe"; no downgrade 3→1 or 2→1 within their own
freshness windows (extends the existing no-downgrade rule :2173-2176).
Truthiness intact — every current reader keeps working unmodified.

Consumers re-keyed by COST:
- CHEAP TIER (keyed ≥1, i.e. unchanged): ammo target 24, ti_floor 12,
  magazine maintenance — the atoll lesson keeps its sighting trigger.
- EXPENSIVE TIER (re-keyed ≥2): builder recalls/convergence (_expand
  :3764-class), heal-over-eco ordering, siege eco caps, map-special holds,
  launchwait sabotage prio. A parked-but-idle turret or a walking scout no
  longer pins these; a ferry, an insertion, or actual damage still does.
- SEPARATE FRESHNESS: severity decays independently — damage-freshness
  (rnd - last_damage_rnd < 50) holds tier 3; sighting-freshness holds
  tier 1 as today. Needs one packed encoding decision for ATK_RND: either
  (a) two logical clocks packed into SLOT_ATK_RND (rnd<<1 | severe) with
  its ~4 readers adapted, or (b) tier-3 freshness tracked per-instance off
  last_hp (core writes SLOT_UNDER=3; builders infer from reading 3 and
  their own damage observations). (b) touches fewer sites; (a) is exact.
  Decide at build time after counting readers.

## 3. Predicted effects (pre-stated, falsifiable at acceptance)

1. Fjordgate-B disc arm (with FB floor on): opening latch drops to tier 1
   → economy opens NORMALLY (harvester ~r5, not r24) while ammo still
   banks; the FB floor becomes the backstop it should be, not the fix.
2. Meander/disc non-fjordgate games: expensive posture releases when only
   parked sightings remain; delivery economies improve or hold.
3. Atoll magazine signature must NOT return: vs a parked harasser the ammo
   tier stays sighting-keyed (13-shots-on-2,782-Ti is the failure
   fingerprint to grep for in acceptance replays).
4. kladde/band guards at baseline (kladde sieges do damage — tier 3 holds
   there, posture unchanged in real sieges).

## 4. Acceptance sketch

- Disc-style instrumented det (fjordgate+meander, FB-on base) vs cad_probe:
  economy metrics per §3.1-3.2 + SLOT_UNDER tier trace per round.
- Atoll leg vs a parked-harasser opponent (the atoll decode's shape;
  band_probe or opp-archive era-book pick) checking shot counts.
- det 4-seed vs pre-change head over opp_v63: flips accounted, r1000
  margin-flips excluded per the standing ban.
- kladde/band n=60 guards.
- Identity: new toggle FT2_ON=False must byte-reproduce the pre-change head.

## 5. Open pricing input (routed to research, non-blocking)

Wild rate of all-game pins outside cad_probe matchups — how often does the
ladder actually park-and-sight without damage? (v78-vs-Landers
park-and-shell-zero is one wild exemplar; the era books can count more.)
This prices the expected Elo of the release, not its correctness.
