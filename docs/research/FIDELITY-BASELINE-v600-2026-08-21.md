# SKALMAN PHASE-1 FIDELITY BASELINE — `bots/_v600skalman1`, tape30

**⛔ AMENDED s54 (~17:5xZ, same session — instrument alarm from the tape30 autopsy,
`scratchpad/s54_autopsy/tape30_autopsy.md` §alarm): THE SEED AXIS IS INERT. Both trees are
deterministic, and every `_s11`/`_s12` pair is byte-identical on all decisive event kinds
(15/15 map pairs, death/birth lists hash-identical). EFFECTIVE n = 15, not 30 — every
±ci95 below is ~×1.41 too narrow.** No verdict in this doc moves (the misses are multiples
of any interval), but no v601-vs-v600 comparison may inherit this fixture as n=30.
**Fixture rule going forward: with two deterministic trees, vary MAP and SEAT, never seed
— 15 pool maps × 2 seats = 30 distinct games is this pair's ceiling** (det.py's paired
same-(map,seat) flip shape is the accepted comparison instrument). Also recorded, because
this doc chose not to tabulate outcomes: the tape is 15 losses in 15 distinct games
(core destroyed 14/15, median r180) — descriptive, still no game-share claim.

**Builder s54, 2026-08-21 ~17:4xZ.** The founding tree's first at-n mechanism read — the
reference row every v601+ iteration is measured against. **Fixture:** canonical
`bots/_v600skalman1` (seat A) vs the NOISE_OFF `_v542wave` copy (recipe:
`scratchpad/s54_fidtape/mkfixture.sh`, driven), 15 rotated-pool maps × seeds 11/12 =
30 games, 30/30 replays, 0 failures. **Gate:** CLEARED with `--allow-self-play` typed
("fidelity, not field"). **Instrument:** `tools/skalman_fidelity.py` (selftest 20/20+5/5,
full-mode digit-for-digit vs the study), `--deff 0.98` (local). Raw:
`scratchpad/s54_fidtape/tape30_fidelity.json` + replays_tape30/. **No game-share claim
anywhere in this doc; game outcomes were not even tabulated.**

## The table (value ±ci95 where emitted · BC v68 target · our old baseline)

| verb | metric | v600 | target | old us | read |
|---|---|---|---|---|---|
| DRIP | M3a lattice | **99.5%** (1480/1488) | ≥97.3 | — | **AT TARGET — the COPY-7 acceptance test passes** |
| DRIP | M3b/c/d/e calls·Ti·peak·first | 24 · 166 · 14 · r46 | 67 · 650 · 26 · r27.5 | — | ON-LATTICE BUT UNDERFED (see cluster below) |
| ORE | M6b/c/d coverage·latency | **100%/100% @ 1** (2/2 deaths) | 92.5 @ 1 | 0.0 | AT TARGET on a THIN base — only 2 enemy harvester deaths occurred |
| ORE | M6a barriers-on-ore | 5.0% (4/80) | 37.9 | 0.0 | moving off zero; volume limited by denier survival |
| NEST | M4a-d band/point-blank | **100% / 0%** (10/10) | design | — | DESIGN-CONFORM (footprint origin; anchor row 80% reproduces study-compat) |
| ROLES | M5c fourth spawn | r3 (30/30) | r3 | — | EXACT |
| CAGE | M2a ring share | 72.5 ±21.3 (58/80) | 39.6 | 75.4 | our line's habit persists (targeting is fine) |
| CAGE | M2c first ring build | r26 | r52 | r12 | earlier than BC |
| **BELT** | **M1 connectivity** | **14.3 ±12.2 (4/28 harv)** | **81.4** | **58.8** | **HEADLINE MISS, confirmed at n=30** |
| **CAGE** | **M2b full seal / M2d held** | **0/30 · median 0 of 8** | **22.2 · 6** | **12.0 · 5** | **the cage never completes** |
| **ROLES** | **M5b exactly-4** | **46.7 ±18.0 (>4 in 16, <4 in 0)** | **92.9** | — | **bodies die and are replaced; respawn works, mortality doesn't stop** |
| **ROLES** | M5f/g/h fwd-role recognisers | 26.7 / 6.7 / 6.7% | — | — | forward roles rarely live long enough to register |
| **DOOR** | **M7 removal** | **17.8 ±11.3 (12/56)** | **76.6** | **42.8** | **clearance far below even the old line** |

(M5i four-distinct-roles 0/30 — emitted-not-scored per design §6.3; BC itself reads 1.8%.)

## THE READ — one cluster, not seven misses

**The chassis executes its mechanisms correctly and nothing survives contact.** Every
precision metric is at or beyond target (lattice 99.5, denial latency 1, band 100/0,
fourth-spawn r3, ring targeting 72.5, first ring r26). Every volume/completion metric is
far under (connectivity 14.3, seal 0/30, exactly-4 46.7, removal 17.8, drip underfed at
24 calls/r46-first) — and each of those is downstream of the same thing: **harvesters,
forward bodies and turrets die under the benchmark's kill pressure faster than the verbs
can compound.** The drip is need-based, so dead turrets = no need = 166 Ti/game; the seal
needs a walker who lives a full lap; connectivity needs harvesters that survive.

⇒ **v601's commissioning surface is SURVIVABILITY, in this order: (1) belt/harvester
protection (M1 — the declared weak verb), (2) forward-body survival (M5b + the role
recognisers), (3) home-turret answer (M7 — and #116's coverage-geometry finding applies:
the measured uncovered-belt-tile gap is published on slot 5 b18-23 and unread so far).**
Mechanism-precision work (more COPY tuning) is NOT the gap and should wait.

**Caveats carried:** self-play fixture (the benchmark is our own line — the gate escape
says so; BC-target comparisons are fixture-independent mechanism signatures, but kill
pressure here is v542wave's, not the field's) · seat A only (pool maps are symmetric by
construction) · ore-denial base is 2 events · n=30 with games-as-units CIs at DEFF 0.98.
