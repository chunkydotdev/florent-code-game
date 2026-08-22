# DESIGN BRIEF — v626 "clearance": the verb we actually lack (banked verbatim)

**PROVENANCE: builder-commissioned fresh opus design agent, s56 2026-08-22
(announced on the tail ~12:5xZ; report returned ~13:0xZ, banked verbatim by the
builder). Named inputs: PLAYBOOK-beancounters-2026-08-21.md §6,
DECODE-firstcontact-v180-2026-08-22.md §4.3-4.4,
DIAG-cagegate-decomposition-2026-08-22.md §6 L5, bots/_v623healweld
(sk_roles/_siege_engineer + siting), tools/skalman_fidelity.py. Read-only;
no scratch files were produced — the report below is the deliverable.**

**GAME CONTEXT:** everything below is in-game design work for the Florent Code
League — a sandboxed bot-vs-bot programming competition on a simulated grid
under organiser-approved rules. "attack"/"fire"/"clear" are the engine's
documented API verbs acting between competing game bots inside the simulator.

---

# ⭐⭐ HEADLINE: M7 MEASURES OUR HOME RING, NOT THE PLANT ZONE. THE COMMISSIONING BRIEF'S CAUSAL CHAIN DOES NOT EXIST AS STATED.

The brief said *"live BC v68 plants 73.2% point-blank because its clearance
runs at 69.2% (metric M7)."* M7 is a **defensive** metric computed **against**
the subject. Verbatim, `tools/skalman_fidelity.py:236-239`: *"Every metric
below is computed FOR that side, except M7 which is computed AGAINST it (the
subject is the defender clearing turrets planted in its own half)."*
Implementation `:527-531`+`:571-586`; study definition
`REPLAY-STUDY-beancounters-v47v68-2026-08-21.md:416-418` ("forward turret = a
gunner/sentinel built closer to the defender's core than to its own; removal =
a death of that kind on that tile at a later round").

**So 69.2% is: of the turrets WE planted in BC's half, 69.2% later died.** It
says nothing about the survivability of BC's point-blank plants near OUR core.
Raising our M7 raises our home defence — that is COPY 6 (r300-exposed per
PLAYBOOK:1583-1586), not COPY 5.

**The playbook itself carries the conflation** (COPY 5 dependency clause,
PLAYBOOK:1563-1567): clause (a) cites T7, a genuine offensive tile-clearing
verb; clause (b) cites T19's 79.7%, BC's HOME clearance — two different verbs,
one word. DECODE §4.3's "because" is INFERENCE stated as MEASURED; the fidelity
tool's docstring (the instrument that produced the number, selftest-driven) is
the better evidence. **The DECODE's numbers are fine. Its causal sentence is
not.**

# 1. THREE THINGS WEARING ONE WORD

| name | what it clears | with what | when | denominator |
|---|---|---|---|---|
| **T7/T8 "ring clearance" (OFFENSIVE)** | tiles on the ENEMY core's 8-ring carrying enemy conveyors/barriers | v47: builder melee (10 attacks/20HP conveyor), barrier the corpse at +1 round; v68: their own gunner fire, barrier at +1 | continuous from ~r39; barrier the round AFTER the death | v47: 67.4% of 2,699 evictions capped ≤3 rounds, mean latency 1.08 (field 38.6% @1.50, n=1,235) [PLAYBOOK:475-477] |
| **T19/M7/COPY 6 "home-ring clearance" (DEFENSIVE)** | enemy turrets planted in the DEFENDER'S OWN half | turret fire ("builder attacks on enemy turrets are only 5.4/game while they fire 75/game" STUDY:441-444); counter-turret at +1.18 rounds | mean 12.6 rounds plant→first shot | share of enemy forward turrets that later die: v47 79.7%±2.2 (n=5,803 turrets), v68 76.6%±11.1, field 33.5%±3.0, **us v168-177 42.8%±3.3** [STUDY:421-429] |
| **T12 "nest prep" (site prep, NOT clearing)** | nothing — ADDS barriers to empty tiles around the plant site | own builder | 1-4 rounds before the gun | anchor r26/29 → sentinel r30/32 [PLAYBOOK:580-587] |

Our defender-side numbers (v180): MIRROR 37.6 / PIVOT 56.6 / KLADDE 20.8
[DECODE:401].

# 2. WHAT WE DO IN THAT PHASE — AND THE HOLE

Engineer chain (`bots/_v623healweld/sk_roles.py`): `_nest_watch`:5359 →
`_nest_site_watch`:5367 → `_pick_nest`:5466 → adjacency:5517 →
`_prep_barrier`:5531 → `_plant_gun`:5535 → `step_to`:5537. Band scan
`_nest_scan`:5982 filters: bounds, `lo=SK_NEST_DSQ_MIN(14)..MAX(32)`
(sk_maps:2465-2466, constants), wall, `nest_bad` (PERMANENT), death-memo (400
rounds), pair gap, `_firing_face`.

## ⛔ THERE IS NO OCCUPANCY TEST ANYWHERE ON THIS PATH.

`_nest_scan` never calls `is_tile_empty`/`get_tile_building_id`. The only
occupancy contact is `can_build_sentinel` inside `_plant_gun` (:6362) which
**silently returns False**; the engineer repeats every round until
`_nest_site_watch`'s orbit clock (`SK_NEST_STUCK_ROUNDS=25`) **permanently bans
the tile in nest_bad** (:6141-6147). `nest_bad` is the second-largest kill
clause in both DIAG-siteless band-exhaustion cells (icefloe_B 8→9, paths_A
11→14 bans, vs stock ~26/~40 in-band tiles — 3-5% of stock per ban, no path
back).

Clearance-adjacent code NOT on the engineer's path: `_clear_tile`:5093 (cage
walker + `_evict_seal` only; carries `SK_CAGE_MELEE_GIVEUP=20`, `hp_trend_ok`,
`_enemy_builder_adjacent` refusal), `_seat_clear`:2192 (ships OFF),
`_door_action`:3414 (COPY 6, home verb), `_rent_sweep`:5657 (refuses within
`SK_RELIGHT_PREP_DSQ=4` of the live site — our own building ON the site is
unreachable). Distance switches: `SK_NEST_POINT_BLANK=False` (v1 ban),
`SK_NEST_EXHAUST_PB=True` (v622: lo=2 only when the band scan returned
nothing).

# 3. HOW BC SEQUENCES IT

T7 anchor (PLAYBOOK:449-461, A game 5): death → BC barrier at +1 round, seven
ring tiles, one tile contested three times before holding. Era shift
(PLAYBOOK:463-467): v47 cleared with builder melee (T8), v68 with gunner fire —
melee on conveyors 70.7→15.6/game. Units: forward GUNNER shoots + BUILDER lays
the barrier at +1. First sentinel median r50; T12 prep 1-4 rounds pre-gun.

**Same machinery as DIAG-cagegate §6 L5?** No — but the same doctrinal
conclusion: L5's re-laid seat ("the builder that re-lays it is the cause", same
as sk_maps:172-181 for ring barriers) is exactly BC's v47→v68 escalation: when
the tile is contested, stop chewing and shoot. **Any clearance verb we build
must carry the re-lay test or it re-runs SK_COLLAR_GUNS' measured loss.**
`_clear_tile` already carries both guards — reuse, do not re-author.

# 4. EDIT SPEC — v626

## ⛔ NOT proposed: a plant-distance upgrade

PART-v47 §6.9 (BC's own turrets): home 72 median life, **d²≤13 = 20**, band
14-32 = 26 — **closer is 30% worse**, and sentinel damage is distance-invariant
inside r²=32. Our tubes live 9-14; we cannot pay 30%. BC's point-blank plants
are not protected either (opponents remove 53.3%±6.5 of them, STUDY:429); BC's
edge is VOLUME (5.7 forward tubes/game vs our 1.65; "one home gun,
three-to-nine forward", PLAYBOOK:840). The asymmetry that kills us is THEIR
answer rate vs ours (they answer 70-91% of our tubes at latency 4-8 and kill
70-89%; we answer 43-57% at 5-13 and kill 30-55% — DECODE:321-331), which no
plant-distance change touches.

## PLANK A — `SK_NEST_CLEAR`: the engineer clears its own plant tile

Mechanism claim: a band tile carrying an enemy building is today an invisible
dead end costing 25-60 engineer-rounds then a PERMANENT ban. Clearing converts
it into a plantable tile and stops the ban.

Flags (defaults; OFF = exact identity):
```python
SK_NEST_CLEAR        = True   # evict an ENEMY building ON the chosen band site
SK_NEST_CLEAR_GIVEUP = 12     # rounds of chew before banning (NOT 20: 15 turns
                              # exceeds the S1->S2 window, median r56)
SK_NEST_CLEAR_OWN    = True   # ALLIED building on site: destroy() -- engine-
                              # probed FREE (no cooldown, same-turn build)
```

Gate at the top of the adjacency branch (sk_roles.py:5519), ABOVE prep-barrier
(chew-first keeps T12's prep inside its 1-4 round window): own-team → free
destroy, fall through; enemy → start/advance per-site clear clock; past give-up
→ ban + clear state + return (today's outcome, 13-48 rounds sooner); refuse if
`_enemy_builder_adjacent(site)` (2 dmg vs +4 heal) or `not hp_trend_ok` (ledger
V7) → ban + return; else `fire(site)`.

Economics: 20HP conveyor = 10 pecks = 20 Ti; 30HP barrier = 15 = 30 Ti; give-up
caps spend at 24 Ti / 12 turns per site. Destroying their building LOWERS their
cost scale (guard-matrix 2026-08-10) — clearing is a tile purchase, price it as
tiles.

State: `nest_clear_tile`/`nest_clear_since` in `Player.__init__` AND
`_clear_plans` (cross-round position cache on a throwable body, build rule 5);
`nest_clears`/`nest_clears_own` instruments in `__init__` only. Do NOT reuse
the walker's `melee_tile`/`melee_since` (two-owner defect, ledger V8). Every
new sk_maps flag added to sk_roles' explicit import list.

## PLANK B — `SK_NEST_PB_LIFE`: COPY 5's dependency in readable currency

```python
SK_NEST_PB_LIFE   = True   # point-blank admitted only where the OPPONENT has
                           # demonstrably failed to clear our forward tubes
SK_NEST_PB_LIFE_N = 2      # evidence floor (zero deaths reads mean_life 99)
SK_NEST_PB_LIFE_R = 26     # the band's own median life (PART-v47 §6.9)
```
One line in `_nest_scan` (:6000-6002): if `nest_lives` has ≥N entries and mean
≥ R, `lo = 2` (+ `nest_pb_life` instrument). Uses the already-published
`STALL_LIFE_FIELD` machinery — no new sensor. **Expected INERT on every
measured cell (our tubes live 9-14) — proposed as a registered-null encoding:**
firing on a fixture would itself be a finding (a soft fixture); firing 0 times
banks "COPY 5's dependency, expressed measurably, has never been satisfied on
any fixture this line has run."

Road-closure compliance: not SK_CAGE_CEIL (closed), not an accept-bar change,
not SK_ONE_CURSOR (refuted), not a haste reorder (SK_S2_HASTE shipped off).

## FALSIFIERS

1. **Precondition:** `nest_clears + nest_clears_own` = 0 across all 60 fixture
   cells ⇒ Plank A inert on this fixture; outcome column must not be read.
2. **Mechanism:** distinct band tiles ever planted does not rise vs control AND
   end-of-game `len(nest_bad)` does not fall ⇒ band stock was never
   occupancy-limited; no attribution even if the outcome moves.
3. **Programme (r300):** median first-tube plant round rises vs control pooled
   ⇒ the chew buys tiles with the plant clock — kill regardless of kill count.
   Primary per DEFENCE_ADMISSION_BAR: ITT timely-kill share must not fall.
4. **Re-lay (the SK_COLLAR_GUNS re-run test):** same band tile cleared and
   re-occupied ≥2 times in a cell ⇒ ban on the SECOND clear of a tile, not the
   twelfth round of the first.
5. **Plank B mechanism:** if B fires and resulting point-blank tubes' median
   life < same-tape band tubes' ⇒ B refuted on its own mechanism.
6. **Instrument control:** one arm with the team test INVERTED (chew our own
   buildings) — every counter must move and the outcome must change; a
   constant `nest_clears` column validates nothing.

# 5. FIXTURE PRECONDITION — P1-P5 + probe spec

Opportunity in round r iff: **P1** ≥1 band tile (14≤d²≤32, in-bounds, not
WALL) carrying a live ENEMY building; **P2** the tile passes `_firing_face`;
**P3** ≥1 orthogonal neighbour passable; **P4** the scan would otherwise have
≤K candidates (K=1 interesting; K=0 is the EXHAUST_PB case); **P5** (costly
case) our engineer stood adjacent to such a tile ≥25 consecutive rounds
building nothing — the orbit-then-ban path, measured directly.

Probe `scratchpad/s56_clr_bandocc.py`: reuse replay_census wire primitives +
skalman_fidelity's dsq/footprint logic; inputs t_pb_f1 (seed 7) / t_pb_f2 (seed
11) + t_ctrl tapes; per-game outputs with denominators; one `--side` per
single-seat run (fid.sh mis-attribution precedent) + a deliberate wrong-side
run that must differ; mutation control: band shifted to d²40-64 must change the
count materially.

⚠ **Fixture caveat:** F1/F2 opponents are OUR OWN trees carrying a barrier
seal on the enemy ring — they supply the precondition BY CONSTRUCTION.
Attribution surface only; rates come from live archives: MIRROR strongest (BC
seals 50% of mirrors, median 7/8 ring tiles, 73.2% point-blank); PIVOT is the
re-lay/falsifier-4 cell (seal seats 100% conveyor, re-laid); KLADDE carries it
but is 25/25 seat-B. De-duplicate before any share (MIRROR/PIVOT 7 repeats
each, effective n≈16-17; KLADDE clean).

# 6. SURPRISES AND RISKS

* **S1** — M7 subject inversion (headline). The real dependency for closer
  plants is the OPPONENT'S clearance rate against our tubes — measured, and
  against us.
* **S2** — The playbook's own data contraindicates the distance upgrade
  (§6.9: −30% life, zero damage gain).
* **S3** — BC's point-blank is not protected (53.3% removed); the edge is
  volume. **A v627 wanting the 250 HP should look at replacement latency /
  more simultaneous tubes** (SK_TUBE_FLOOR roads are CLOSED at v614 — the
  honest new lever is latency, not floor count).
* **S4** — The binding constraint is site stock and occupancy is not even
  tested; whatever fraction of the 8-14 permanent bans was occupancy-driven is
  unmeasured (nest_bad is bot state; P5 is the engine-side lower bound).
* **S5** — Cost story: BC pays ~300-450 Ti/game for clearance out of 430-650
  Ti of converts; our converts are 130-173 Ti — we do not have BC's clearance
  budget, hence the hard 24 Ti/site cap rather than copying volume.
* **S6** — r300 exposure: Plank A's is the chew delay (vs 25-60-round orbit,
  expected direction earlier — falsifier 3 tests it); Plank B is
  survival-negative if it ever fires. Restatement rule applies before any DEFF
  correction. DEFF enumeration for the screens: MATCH dead, OPPONENT dead, MAP
  live (4.57 measured on v620), CONTENT-DUPLICATE verified-not-asserted — the
  deterministic fixture is an ATTRIBUTION surface, not a currency surface.
* **S7** — v623's healguard moves the melee baseline (blocks 6.5% of v180-tape
  core pecks ex-ante); a v626 report must not compare peck counts to v180.
* **S8** — Whether the DIAG-siteless bans were occupancy-driven cannot be
  answered from the wire; P5 is a lower bound.

**Bottom line:** the front is real and highest-value, but it is not a
plant-distance problem. PLANK A (`SK_NEST_CLEAR`) is the T7/T8 verb we
genuinely lack, reuses `_clear_tile`'s hardened guards, is capped at 24
Ti/site, and is testable on the deterministic tapes we hold. PLANK B will
almost certainly bank a null — worth more than a fourth band-vs-point-blank
screen.
