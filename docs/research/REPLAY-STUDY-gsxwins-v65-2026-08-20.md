# REPLAY STUDY — gsxWins v65 (move-mining candidate #2)

**PROVENANCE.** Fresh replay-study agent (opus), research arm, commissioned
2026-08-20. Method: `docs/research/PLAYBOOK-move-mining-2026-08-16.md`.
Written 2026-08-20T04:32Z at `f7e75d561` (`date -u`, same shell).

**GROUND.** gsxWins v65 — 45 rated games in 9 matches, 2026-08-18T02:12Z →
2026-08-19T11:32Z, our chassis v159/v161/v162. Comparison eras drawn from the
same opponent: v22 (105 archived games), the v39–v53 "mid" block (75), v54 (10),
v58 (15). **No prior gsxWins row exists in `move-mining-ledger.tsv`** — this is
first coverage of the opponent, so the exclusion baseline is empty and every era
below is newly read.

**INPUTS** (all snapshotted to scratchpad before reading; row counts verified
twice against the live file, all eight surfaces stable — `ladder_games` 6856,
`join` 5544, `meta_join` 77967, `league_matches` 61123, `league_games` 3706,
`unrated_games` 8272, `wincond` 44432, `version_trees` 97):
`corpus/ladder_games.tsv`, `corpus/join.tsv`, `corpus/league_matches.tsv`,
`corpus/events.tsv`, `corpus/builds.tsv`, `corpus/econ.tsv`, `corpus/flow.tsv`,
`corpus/throws.tsv`, `corpus/build_agg.tsv`, and 190 `.replay26` files already
present in `replay_archive/`. **Zero platform matches, zero replay downloads** —
every v65 game was already archived.

**INSTRUMENTS AND THEIR CONTROLS.** Three decoders were used and each was driven
to the other verdict before its output was banked:

| instrument | control | result |
|---|---|---|
| `tools/corpus/replay_autopsy.py` (core-damage ledger) | the tool's own self-check: attributed damage must equal summed `UpdateHp` deltas on the core id | **189/190 MATCH, 1 MISMATCH** — the mismatching game is excluded from every ledger figure below |
| custom lifetime/reach walker (`scratchpad/walk.py`) | per-(file, team, kind) build and death counts compared against `corpus/events.tsv`, an independently written decoder | **2146/2146 cells agree**; forced-fail control (conveyors deleted from walker output) **fires** |
| custom dwell/attack walker (`scratchpad/walk2.py`) | total `builderAttack` events per team vs the autopsy's independent count | **190/190 agree**; forced-fail (`atk[0]+1`) **fires** |

**CLUSTERING.** Every share below is a GAME share. Games cluster within matches
(5 per match, shared opponent version and ladder slice), so all confidence
intervals use the rated pooled **DEFF = 1.529** from `CLAUDE.md`; two-fixture
comparisons use the two-arm form. Match counts are stated alongside game counts
so the reader can see the true n.

---

## 0. HEADLINE

**MEASURED.** Our game share against gsxWins by their version:

| their version | games | matches | our game share | our kills | their kills | median turns |
|---|---|---|---|---|---|---|
| v16 | 20 | 4 | 70.0% | 14 | 6 | 114 |
| **v22** | **115** | **23** | **59.1%** | 67 | 42 | 145 |
| v39 | 20 | 4 | 30.0% | 5 | 13 | 210 |
| v45 | 5 | 1 | 0.0% | 0 | 5 | 170 |
| v46 | 15 | 3 | 26.7% | 3 | 10 | 210 |
| v53 | 25 | 5 | 16.0% | 4 | 21 | 165 |
| v54 | 10 | 2 | 60.0% | 6 | 4 | 280 |
| v58 | 15 | 3 | 33.3% | 5 | 10 | 174 |
| **v65** | **45** | **9** | **20.0% ±14.5%** | 8 | 34 | 256 |

Pooled eras: **v16–v22 60.7% ±10.2% (135 games / 27 matches, 20 match wins) →
v39–v53 25.3% (75 / 15, 2 match wins) → v58+v65 23.3% ±13.2% (60 / 12, ZERO
match wins).**

⛔ **THE BRIEF'S FRAMING IS WRONG IN TWO PLACES AND BOTH CORRECTIONS MATTER.**

1. **The break is v22→v39 (2026-08-14/15), not v54→v58.** The mid block
   (v39–v53) already sits at 25.3%, statistically the same cell as v58+v65.
   v54's 60% is **n=10 in 2 matches** — a coin flip, not a version that "lost
   to us". Anyone who preregisters against "what changed at v58" is dating the
   regression four days and eight opponent versions too late.
2. **Their field share did NOT rise.** `league_matches.tsv`, gsxWins' game share
   **excluding OpenSverige**: pre-v22 **50.3% ±1.4% (n=7435)** → v39–v53
   **52.1% ±3.3% (n=1350)** → **v65 46.3% ±4.5% (n=715)**. Against the field
   their v65 is **4.0pp WORSE than their v22 era (two-arm half-width 4.7pp —
   i.e. flat, possibly slightly down).** Against us, over the same boundary,
   their share went **39.3% → 80.0%, a 40.7pp rise against a 20.9pp
   half-width.** ⇒ **There is essentially no generic component to separate. The
   whole move is matchup-specific.**

---

## 1. Q1 — WHY THEY BEAT US, AND WHY EVERY CHASSIS LOSES

### 1.1 The regression is opponent-specific, not a chassis regression (MEASURED)

Our own game share **against the rest of the field** over the same 15 days,
per day, from `ladder_games.tsv`: 27.7 / 59.7 / 50.1 / 47.6 / 50.9 / 51.5 /
49.2 / 48.7 / 55.9 / 48.9 / **53.0 / 52.5 / 53.1 / 53.2 / 50.7 / 48.3** — flat.
Our gsx-only share over the same days: 80.0 / 66.7 / 56.0 / 60.0 / 60.0 / — /
66.7 / 53.3 / — / **30.0 / 28.0 / 30.0 / 25.7 / 13.3**. The collapse is confined
to one cell.

Per chassis, archived games:

| our version | vs FIELD (excl. gsx) | vs gsxWins | gap | two-arm 95% hw |
|---|---|---|---|---|
| v155 | 55.4% ±7.9% (n=233) | 16.0% (n=25) | 39.4pp | 25.5pp ✅ |
| v159 (our line) | 57.6% ±10.7% (n=125) | 36.7% (n=30) | 20.9pp | 24.6pp ⚠ not cleared |
| v161 (x3r0) | 55.0% ±9.0% (n=180) | 40.0% (n=5) | 15.0pp | (n too small) |
| v162 (x3r0) | 52.2% ±6.2% (n=385) | 10.0% (n=30) | 42.2pp | 23.0pp ✅ |
| **pooled v155–v164** | **53.0% (n=1053, 212 matches)** | **25.3% (n=95, 19 matches)** | **27.7pp** | **13.0pp ✅** |

**MEASURED, and stated as an exclusion so the DEFF correction cuts the right
way:** the pooled interval **excludes** parity between our gsx cell and our
field cell. **INFERENCE (chassis-invariance):** the direction is identical in
all four chassis and the pooled gap clears; v159 alone does not clear on its own
n=30, so "every chassis individually loses significantly" is NOT established —
"the deficit does not depend on which chassis we ship" is.

### 1.2 The mechanism: their gunner changed job, and the volume went up 2.5x

**MEASURED — what their shots land on**, from the per-entity HP ledger
(`replay_census.py --damage`), share of shots by victim kind, per game:

| era | their GUNNER shots/game | on our builder bots | on our core | on our conveyors | on our harvesters |
|---|---|---|---|---|---|
| v22 | 35.3 | 4% | **92%** | 0% | 0% |
| v53 | 22.0 | 52% | 23% | 0% | 0% |
| v58 | 32.1 | 37% | 30% | 8% | 10% |
| **v65** | **87.7** | **31%** | 23% | **22%** | **12%** |

Their SENTINEL never changed job — 92–100% of its shots land on our core in
every era. **The gunner did.** At v22 it was a second core-sniper; at v65 it is
a general-purpose screen that spends a third of its fire on our bodies and a
third on our economy.

Consequences, all MEASURED on the same 45 games:

* **Our economy is shredded and theirs is not.** Our conveyors die at **29%**
  of built (10.4 deaths on 35.8 builds per game) and our harvesters at **32%**
  (2.1 on 6.7). Theirs: **12%** and **4%**. At v22 both sides ran 3%.
* **Our forward turret line is suppressed.** Our sentinels die at **67%** of
  built (1.9 on 2.9), our gunners at 49%. Their gunners die at **13%** (0.8 on
  6.0), their sentinels at **15%**.
* **We lose the core-damage race by arithmetic.** Sentinel core-shots per game
  = shots × share-on-core: **theirs 35.3 × 92% = 32.5 → 585 damage** against a
  500-HP core. **Ours 23.2 × 67% = 15.5 → 279 damage** against a core they heal
  by a median 142 HP. At v22 ours was **40.2 × 71% = 28.5 → 514 damage** — just
  over the line, and we won that era 59.1%. **The budget crossed 500 in one
  direction and we crossed it in the other.**

### 1.3 We arrive; we cannot convert (MEASURED — and it kills the obvious theory)

**Reach is NOT the problem.** Our builder bots get orthogonally adjacent to
their core in **96% of v65 games**, first arriving at a **median round 21**, and
sit there a **median 122 rounds (p75 248)**. Their bots reach ours at r36 and
dwell 18 rounds. **We out-position them and lose anyway.** Any plank premised
on "we cannot get there" is aimed at a problem this cell does not have.

**⛔ REFUTED IN PASSING, retained so nobody re-derives it: builder melee on the
core is not the missing channel and never was.** Median `builderAttack` events
landing on the enemy core footprint is **0 for both sides in all four eras**, and
`builder_attack` is **1–3% of all core damage** in every era including the ones
we won. Cores die to sentinels. (This is the same direction as QUEUE #85.)

### 1.4 The ammunition floor — a REPLICATION of QUEUE #89, on a new opponent

**MEASURED.** Median titanium converted to ammunition, per game, v65 cell:
**ours 174, theirs 696 — 4.0x.** By band (median, band-conditioned): r0-150 ours
136 / theirs 356; r150-200 ours **10** / theirs 131; r200-300 ours **17** /
theirs 284.

**MEASURED, and this is the shape that matters:** we are not broke, we are
**pinned**. Median titanium banked at end of r200-300 is **ours 66, theirs 46**;
median ammunition held over rounds 100–250 across all 45 games (n=5,313
round-samples) is **ours 27, theirs 60**, and we hold under 20 ammo in only 6%
of rounds. Two anchors:

* `e43017db-cf7f-40f6-8fb7-092d0a3ea4cc_game_2.replay26` (ourver 159, royale,
  256 turns, lost): our ammunition reads **24, 20, 20, 20, 24, 24** at r40, 80,
  120, 160, 200, 240 while our bank climbs to 105 Ti and theirs reaches **607 Ti
  / 108 ammo**.
* `01ab59bd-72d7-42fa-ab8d-47a7e77dcdd1_game_2.replay26` (ourver 162,
  drakkarfjord, 451 turns, lost): pinned at 20–24 to r240, then **1 ammo and 12
  Ti held for 200 consecutive rounds** (r280→r440) while theirs reaches 122.
  **12 is `ti_floor` exactly** (`bots/_v488beltbreak2/main.py:389`).

**INFERENCE (code read + observed steady state, not an end-to-end measurement).**
The incumbent's core sets `ammo_target = 24 if under else AMMO_FLOOR`
(`main.py:346`, `AMMO_FLOOR = 16` at `doctrine.py:963`), raises it only from
turret counters, and the **T4 ghost-magazine brake** zeroes `weapons_top` when
the magazine has not fallen for 12 rounds (`main.py:315-325`,
`T4_AMMO_IDLE_RNDS = 12` at `doctrine.py:1982`). v65 kills 67% of our forward
sentinels; the counters then describe rubble, the magazine stops falling, the
brake fires, and the tap closes at the floor. **The observed 20–24 plateau is
what that policy predicts.** ⚠ This is a mechanism sketch consistent with the
tape, not a driven experiment; the falsifier is a local screen with
`T4_AMMO_IDLE_ON = False` that must raise our sentinel shots/game above ~23.

**⭐ WHAT THIS STUDY ACTUALLY CONTRIBUTES TO #89, WHICH IS NOT THE FLOOR.**
Row #89 registers a null-diagnostic up front: *"the ammo channel's throughput is
TURRET-LIMITED, so this row can be fully correct and still read flat — median
NET SURVIVING turrets is 2."* **This cell resolves that fork against the ammo
lever.** Net surviving turrets per game in the v65 cell: **ours 1.6**
(gunner 1.2−0.6, sentinel 2.9−1.9); **theirs 6.7** (gunner 6.0−0.8, sentinel
1.8−0.3). **They field 4.2x our net turret count.** Buying more ammunition for
1.6 turrets cannot close a 306-damage gap. **The binding rows are #21/#22/#86,
not #89.**

---

## 2. Q2 — THE VERSION DIFF, AND WHERE IT REALLY IS

### 2.1 The real boundary is v22 → v39, and it is a rewrite (MEASURED)

Their builds in **r0-150**, per game, and the share of games containing at
least one:

| | v22 | v39–v53 | v54 | v58 | v65 |
|---|---|---|---|---|---|
| conveyor | 8.1 | 28.5 | 22.5 | 24.7 | **25.9** |
| harvester | 2.0 | 4.5 | 3.7 | 3.9 | **4.1** |
| barrier | 1.3 | 7.2 | 5.3 | 9.4 | **7.1** |
| gunner | 1.0 | 2.5 | 3.4 | 3.6 | **3.7** |
| sentinel | 2.1 | 2.3 | 0.6 | 0.9 | **1.0** |
| launcher | **1.3** | **0.0** | 0.0 | 0.0 | **0.0** |
| games with ≥1 launcher | **100%** | **0%** | 0% | 0% | **0%** |
| games with ≥1 barrier | 54% | 97% | 90% | 100% | 98% |
| games with ≥1 gunner | 65% | 92% | 100% | 100% | 96% |
| median first-gunner round | 28 | 11 | 11 | 8 | 11 |
| median first-sentinel round | 13 | 65 | 108 | 72 | 80 |

**They deleted the launcher entirely, tripled the early belt, moved the gunner
from r28 to r11 and the sentinel from r13 to r80.** Their economy follows:
median titanium collected by r150 went **360 (v22, parity with our 380) → 720
(v65, against our 560)**, and by r300 **725 → 1485 (against our 800).**

**⛔ AND OUR ECONOMY DID NOT GET WORSE.** Ours by r150 rose 380 → 560 and by
r300 685 → 800 over the same span. We lost a race we are running faster in.

### 2.2 The v54→v58→v65 diff proper: production that never stops (MEASURED)

Turret (gunner+sentinel) builds per game **conditioned on games that reached the
band** — the control that matters, because v22 games were short (median 145
turns) and would otherwise fake a late-game drop-off:

| band | THEM v22 | THEM v39-53 | THEM v54 | THEM v58 | **THEM v65** | US v65 |
|---|---|---|---|---|---|---|
| r0-150 | 3.07 (n=105) | 4.45 (75) | 4.00 (10) | 4.47 (15) | **4.67 (45)** | 2.64 |
| r150-200 | **0.06** (52) | 0.87 (55) | 0.56 (9) | 0.50 (10) | **1.18 (38)** | 0.55 |
| r200-300 | **0.03** (36) | 0.81 (37) | 1.14 (7) | 0.17 (6) | **1.69 (32)** | 0.78 |
| r300+ | 0.96 (24) | 1.00 (12) | 1.75 (4) | — | **2.33 (18)** | 1.06 |

**v22 stopped building turrets at r150 (0.06 and 0.03 per game). v65
ACCELERATES: 4.67 → 1.18 → 1.69 → 2.33.** Their gunner build rounds run p25=50,
median=120, p75=212, max=992 — against v22's p75=97 and v58's max=200. Placement
follows: forward-gunner share 27% (mid) → 34% (v54) → 48% (v58) → **54% (v65)**,
and their gunner siting is bimodal (22% within f<0.2 of their own core, 29% at
f>0.8 near ours; f = d_own/(d_own+d_enemy)).

**INFERENCE, and it is the study's most useful sentence:** what separates v65
from v54/v58 is not a new trick, it is **sustained reinforcement** — the same
gunner, bought forever, off a doubled economy. v54 and v58 already had the
composition; v65 added the volume, and the volume is where our share falls from
33.3% to 20.0%.

### 2.3 Separating generic from vs-us: the class test (MEASURED, with the honest residual)

Across every opponent-version we have ≥15 archived games against, opponents
matching the v65 profile (their r0-150: conveyor ≥18, gunner ≥2, launcher = 0):

* **IN-CLASS: our share 43.6% ±3.9% (n=940 games, 29 opponent-versions)**
* **OUT-CLASS: 51.1% ±2.1% (n=3242, 91 opponent-versions)** — gap 7.5pp against
  a 4.5pp two-arm half-width ✅
* **IN-CLASS excluding gsxWins: 46.2% ±4.2% (n=840)** — gap 4.9pp vs 4.7pp,
  cleared narrowly.

⇒ **The archetype costs us ~5pp field-wide. gsxWins v65 costs us 33pp.** The
class explains roughly a sixth of the deficit; **five sixths is gsxWins
specifically**, and this study does not identify what the remaining piece is.
That is a named open question, not a hedge.

Cutting the class into its parts, **restricted to games lasting ≥200 rounds and
excluding gsxWins** (so the cell under study is not evidence for itself):

| their r0-150 gunners | our share | n |
|---|---|---|
| 0 | 52.0% ±4.5% | 739 |
| 1–2 | 49.4% ±4.6% | 695 |
| 3–5 | 41.6% ±4.2% | 795 |
| **6+** | **35.8% ±4.9%** | 556 |

Gap 0 vs 6+: **16.2pp against a 6.8pp half-width ✅.** Joint cell: gunners ≥3
alone moves 52.5% → 39.9% (n=1236 / 1277, clean); adding barriers ≥8 on top
moves it to 28.4% but on n=74 with a ±12.7% half-width.

### ⛔ 2.4 REFUTED AND RETAINED: the enemy-barrier gradient is mostly reverse causation

The raw cut looked like the best finding of the day — our share falls
monotonically with their r0-150 barrier count: **54.7% (0) → 51.1% (1–3) →
45.9% (4–7) → 31.2% (8+)**, and it survived removing gsxWins entirely (54.3% →
34.3%, n=414 at the top bucket). **It does not survive the length control.**
A game we win at r80 mechanically denies the enemy the r0-150 window in which to
lay barriers. Re-cut on the same data, excluding gsxWins:

| minimum turns | 0 barriers | 1–3 | 4–7 | 8+ |
|---|---|---|---|---|
| any | 54.3% (2822) | 51.0% (1276) | 47.2% (781) | **34.3% (414)** |
| ≥150 | 51.2% (1809) | 49.1% (894) | 45.2% (619) | 35.0% (340) |
| ≥200 | 46.4% (1389) | 46.8% (667) | 44.2% (457) | 36.4% (272) |
| **≥250** | **42.6% (1116)** | 47.2% (506) | 46.4% (345) | **39.9% (213)** |

At turns ≥250 the gradient is **2.7pp against an 8.9pp half-width — gone.**
**The gunner cut survives the identical control; the barrier cut does not.**
⚠ Note the second control ran the other way as required: cut on OUR OWN r0-150
barrier count, our share **rises** 46.2% → 68.9%, which is the same reverse
causation with its sign flipped, and is itself not evidence that our barriers
help. ⚠ A third control (their splitter count) was **degenerate** — 0 splitters
in all 5,543 games — so it validates nothing and is reported as unusable rather
than as a passing control.

---

## 3. PIECES — counter-mechanism candidates, with what each costs

Each is one behaviour, cited at ≥2 games, priced, and checked against the
incumbent `bots/_v488beltbreak2` (v159) and against QUEUE.md.

**P1 — SUSTAINED TURRET PRODUCTION PAST r150 (⭐⭐⭐, and it is QUEUE #22 with
the best field evidence that row will ever get).** gsxWins ran the A/B on
themselves: v22 built 0.06 turrets/game in r150-200 and we beat them 59.1%; v65
builds 1.18 → 1.69 → 2.33 and beats us 80.0%, **with both sides' field share
unchanged across the boundary.** We build 0.55 / 0.78 / 1.06 in those bands.
⚠ **INFERENCE, and the confound is named:** their composition change and our
v123→v140 chassis change are same-week and **collinear**; what breaks the tie is
that neither side's FIELD share moved, which is evidence for an interaction, not
for either side's absolute change. **Cost:** the plank is a cap and a gate, not
new code — `LOKI_FWD_GUN_CAP = 3` (`doctrine.py:1219`) caps forward guns alive.
Raising it spends titanium the ammo floor is currently hoarding (median 66 Ti
idle at r200-300), and each turret adds +20% to the global cost scale while it
lives. **Against `R1000_IS_DEFEAT` this is a kill-lane plank, not defence** —
their forward gunners sit at median f=0.61, i.e. on our half, doing offence.

**P2 — MASS GUNNERS OVER FEW SENTINELS FOR THE SCREEN, KEEP THE SENTINEL FOR
THE CORE (⭐⭐, overlaps QUEUE #21/#90/#93).** Their split at v65: 6.0 gunners
(87% survive) doing bodies+economy, 1.8 sentinels (85% survive) doing 92% core.
Ours: 1.2 gunners, 2.9 sentinels of which **67% die**. Damage per ammo is
near-identical (gunner 1.75, sentinel 1.80), but a gunner is cheaper (20 vs 30
base) and reloads in 1 vs 2. **Cost:** `raid.py:386 _try_forward_sentinel`
hard-codes SENTINEL per QUEUE #21's grep; a gunner sibling is new code on the
raid hot path, so it carries the hot-turn stamp. **Hot-turn cost: ADDS** — it is
a second siting scan.

**P3 — PROTECT THE BELT, OR STOP ASSUMING IT SURVIVES (⭐⭐, new; nearest
neighbours are QUEUE #88 and #96).** 29% of our conveyors and 32% of our
harvesters die in this cell against 12%/4% of theirs, and 34% of their 87.7
gunner shots/game are aimed at that economy. QUEUE #88 already establishes our
repair path is stateless by explicit design and relays the same tile into the
same gun. **This cell is the strongest instance of that defect on record.**
**Cost:** #88's memory is cheap (a dict of dead tiles); rerouting is not.
⚠ **This is an economy plank and economy does not score** — it is admissible
only as a kill-enabler, i.e. it must show up as ammunition and turrets, not as
`titanium_collected`.

**P4 — THE GHOST-MAGAZINE BRAKE IS AN EXPLOITABLE SURFACE (⭐, and it is a
SELF-AUDIT item, not a weapon).** `T4_AMMO_IDLE` (`main.py:315-325`) closes our
ammunition tap when the magazine stops falling for 12 rounds. An opponent who
kills our forward turrets — which v65 does at 67% — makes that condition true
and holds it true. **We built a brake whose trigger an opponent controls.**
⚠ This is a mechanism sketch from the code plus the observed 20–24 plateau, not
a driven result. **Cost:** flipping `T4_AMMO_IDLE_ON` off is one constant, but
per QUEUE #89's registered diagnostic the throughput bound is turret count
(ours 1.6 net vs their 6.7), so this **should be built as a rider on P1, never
alone** — alone it is the null #89 predicts.

**⛔ P5 — NOT A PIECE: enemy barriers.** See §2.4. Do not spend a leg on it.

**⛔ P6 — NOT A PIECE: forward reach.** See §1.3. We arrive in 96% of games at
median r21 and dwell 122 rounds. Do not spend a leg on getting there.

---

## 4. WHAT THIS STUDY DID NOT ANSWER

* **Five sixths of the gsx-specific deficit is unexplained by the archetype**
  (§2.3). The class cut says the profile costs 5pp; this opponent costs 33pp.
* **The v22→v39 collinearity is not broken**, only bounded by the two flat
  field-share series (§3, P1).
* **No pinned leg was fired.** Everything here is observational on the rated
  tape. Per directive point 6, nothing above **closes** a road; the barrier
  refutation in §2.4 is a refutation of a *statistical artefact in our own
  corpus*, which is a different act from retiring a game mechanic.
* **`titanium_collected` figures are diagnostic only** — under
  `R1000_IS_DEFEAT` the economy numbers in §2.1 buy the kill and never score.
