# AUTOPSY — what our opening/route does differently on the crater maps

**Research arm, s51, 2026-08-20.** Gates the builder's ANTI-RING build (autopsy-before-spec).
Successor to `docs/research/RING-ENGAGEMENT-mjolnir-2026-08-20.md`, whose §6.4 asked for exactly
this leg.

**Fixture:** the same 900 LOCAL replays, `scratchpad/s51_vs_holder/rep/`, our head `bots/_v525flip`
vs `bots/_x3r0v165mjolnirB`, 15 maps × 30 seeds × 2 seats. Results tape
`scratchpad/s51_vs_holder/head_vs_v165.tsv`, md5 `728a9473ccb94b58adc42e0fd6159bf8`, unchanged.
**No platform matches, no downloads, no `corpus/*.tsv` read.**

**Subjects on every number below: OUR-BOT-vs-ONE-OPPONENT, LOCAL harness, `_v525flip` vs
`_x3r0v165mjolnirB` only, 900 games, 60 per map (30 seeds × 2 seats).** Games share (map, seed,
seat) structure; the seed-pair DEFF of **1.130** measured on this fixture by the ring study is
applied to every share interval quoted here. Nothing here is a ladder read.

---

## 0. H1 and H2 — verdicts on the two named hypotheses

Magnus's mid-flight addendum, answered first and by name.

### **H1 — "RAIDERS DIE EARLY on the crater maps": REFUTED, and the sign is inverted.**

Our raiders die **later** on the craters, not earlier, and the killer mix barely moves.

| | sweep (n=120) | crater (n=180) |
|---|---|---|
| our builder deaths / game | 1.42 | 1.68 |
| **first apron death, round** | **65.3** | **144.6** |
| median apron death, round | 149.0 | 222.2 |
| **raider lifetime after arriving at their apron** | **51.1 rounds** | **127.3 rounds** |
| deaths at HOME / **MID-ROUTE** / at their apron | 0.01 / **0.02** / 1.39 | 0.01 / **0.00** / 1.67 |
| killed by sentinel / gunner / peck / unattributed | 0.70 / 0.72 / 0.00 / 0.00 | 1.01 / 0.68 / 0.00 / 0.00 |

**Censoring control** (sweep games are shorter — median 167 rounds vs 262 — so "later" could be
game length). Restricted to games still alive at r150, share with a raider already dead:

| by round | sweep (n=80) | crater (n=170) |
|---|---|---|
| **r25** | **10.0% ± 7.0** | **8.8% ± 4.5** |
| r50 | 22.5% ± 9.7 | 15.9% ± 5.8 |
| r100 | 43.8% ± 11.6 | 33.5% ± 7.5 |
| r150 | 46.2% ± 11.6 | 50.0% ± 8.0 |

**Indistinguishable at r25 and if anything WORSE on the sweeps at r50 and r100.** No early-death
signal exists to find. **Transit exposure is not a channel at all: 5 of our 1,426 builder deaths
across all 900 games (0.35%) occur between the two aprons.** *(One real crater cost that is NOT
lethal: they take **42.2 gunner hits/game vs 17.7** on the sweeps — 2.4×, and it converts to
0.68 vs 0.72 kills. The fire lands; it does not kill.)*

### **H2 — "RAIDERS GET STUCK / NEVER ESTABLISH": REFUTED, decisively.**

| | sweep (n=120) | crater (n=180) |
|---|---|---|
| **first round a body is at their ring (d² ≤ 8)** | **11.00** | **11.30** |
| first round a body is at their near band (d² ≤ 16) | 11.000 | 11.006 |
| **games where NOBODY ever reaches their ring** | **0/120** | **0/180** |
| **games where we never get a BUILDING onto their ring** | **0/120** | **0/180** |
| first building of ours at their ring | 16.35 | **12.89 (faster)** |
| at-ring presence share of the game | 0.747 | 0.689 |
| at-ring body-rounds | 213 | **331 (more)** |
| establishment share / peak buildings held | 0.887 / 9.65 | 0.839 / 6.67 |
| **stalled builders (never left home, 40+ rounds alive)** | **0.44** | **0.20 (fewer)** |
| **move-reversal rate (the livelock signature)** | **0.493** | **0.347 (lower)** |
| choke-tile step rate | 0.003 | 0.042 |

**We establish at their ring in 900 of 900 games, at the same round, and hold it for a similar
share of a longer game.** The walker-stall signatures point the wrong way — there is *more*
stalling and *more* move reversal on the maps we sweep.

### **CONSEQUENCE: the anti-ring spec is NOT a transit/survival fix.**

But it is also **not** merely "an opening-choice question", because the addendum's own test — *is
the divergence visible in rounds 1–25?* — comes back **YES, in a third channel neither H names.**

| quantity, rounds 1–25 | sweep | crater | Δ |
|---|---|---|---|
| builders spawned by r30 | 4.75 | 4.52 | −0.23 |
| raid at their near band | 11.00 | 11.01 | +0.01 |
| raid at their ring | 11.00 | 11.30 | +0.30 |
| launcher throws by r30 | 7.13 | 8.04 | +0.91 |
| our deaths inside r1–25 | 1/120 games | 3/180 games | — |
| — *the raid channel is FLAT* — | | | |
| **ENEMY first on OUR OWN core ring** | **r80.6** | **r7.2** | **−73.4** |
| **enemy barriers on our ring @r30** | **0.46 of 8** | **4.26 of 8** | **+3.80** |
| **our belt head one step from home** | **r8.4** | **r26.0** | **+17.7** |
| **OUR titanium delivered @r30** | **99.3** | **8.3** | **−91.0** |
| their titanium delivered @r30 | 73.8 | 27.7 | −46.1 |
| first harvester / first conveyor | 4.5 / 5.8 | 7.7 / 9.7 | +3.2 / +3.9 |

⇒ **The r1–25 divergence is a contest for OUR OWN core ring and the belt terminal that has to land
on it — not transit, not survival, not establishment at theirs.** Sections 1–7 are that mechanism.

---

## 1. Headline

**THE CARRIER IS NOT THE ROUTE. IT IS A RACE FOR OUR OWN CORE RING, AND WE LOSE IT ON THE CRATERS
BECAUSE OUR BELT HAS NO SECOND PLAN.**

1. **The raid is fine. Route interdiction is REFUTED with a live instrument.** Our first body
   reaches their near band (d² ≤ 16) at **r10.0 on icefloe, r10.7 on auroraveil, r12.3 on
   yulerune** — *earlier* than on ragnarok (**r14.0**), which we sweep 60/60. Some bot reaches
   their apron in **899 of 900** games (the one exception is an archipelago game; on the sweep and crater subsets it is **0/120 and 0/180 misses** — §0 H2). And of **1,426** of our builder deaths across the fixture,
   **5 (0.35%) happen in transit** — 119 at home, **1,302 at an apron**. Nobody is being funnelled,
   blocked or farmed on the way.
2. **What fails is the last tile of our own conveyor belt.** Our belt reaches one BFS step from
   home and then stops, permanently. Games in which no conveyor of ours *ever* stands on a core-ring
   socket: **0/60 on ten of the fifteen maps**, and **icefloe 49/60 · auroraveil 45/60 ·
   glacierkeep 39/60 · yulerune 30/60 · drakkarfjord 30/60.** `titanium_collected` at r100 is
   consequently **0 in 60/60 icefloe games** against **715 on royale** and **365 on ragnarok**.
3. **It is a race, and the race margin is the strongest map-level covariate this project has found
   for this matchup.** Define `margin = eseal₁ − head₂`: the round the enemy first puts *anything*
   on one of our 8 core-ring sockets, minus the round our belt head first reaches one step from
   home. **r(margin, win%) = +0.747 at n = 15** — against the ring study's best geometry scalar of
   +0.31 and its own uncensored ring measures. **The sign threshold is clean: all 5 maps with
   margin < 0 fail the belt (30–49 of 60); all 10 maps with margin ≥ 0 finish it 60/60.**
   *(n = 15. Not significant on its own — but unlike a bare correlation this one is measured
   game-by-game with the mechanism in view, and the threshold has no exceptions.)*
4. **And the half that is OURS to fix is the absence of a re-plan.** When our head stalls, its own
   target socket is occupied by an enemy entity in **96.9–99.8%** of the rounds it sits there — but
   **another ring socket is empty and a median 2.8–4.1 Manhattan steps away** for **87.7% of those
   rounds on icefloe (256 rounds/game), 53.9% on auroraveil, 43.9% on drakkarfjord.** We never take
   it. Our own doctrine names the reason (§5).
5. **On a tile-exact symmetric board the outcome flips with the SEAT.** drakkarfjord is
   **0/900 mismatched tiles** under the rot180 that carries core A onto core B, and yet seat A wins
   **4/30** with the belt home **0/30**, while seat B wins **29/30** with the belt home **30/30**.
   Same board, same belt clock (`head₂` median 21 on both seats), same enemy clock (`eseal₁` median
   11 on both). The only difference is **which** socket their seal lands on. **A seat effect on a
   symmetric board is an asymmetry in the players, not the map.**

⚠ **What I cannot decompose, stated up front:** the +0.747 is a **between-map** association at
n = 15, and the enemy's arrival at our ring is not exogenous — a team that is winning arrives
earlier. §4 gives the two facts that constrain the direction (the ordering is fixed before any
outcome can exist, and the belt clock is set at r0 by ore distance) and the one cut that stays
confounded (§4.3, refused).

---

## 2. The instruments and their controls

Two new tools, both reusing the existing decoders rather than re-deriving them
(`tools/replay_census.py` for the wire, `tools/map_encode.py:parse_map26` for the map).

* **`scratchpad/s51_route/mapgeom.py`** — map LAYOUT, not scalar size: min **vertex** cut between
  the cores (= number of vertex-disjoint corridors, unit-capacity max-flow), narrowest
  shortest-path level, choke share, ore siting by BFS depth from each core.
* **`scratchpad/s51_route/routetape.py`** — one pass per replay: opening chain, per-bot tracks,
  launcher-throw hops, first contact, death ledger by basin, per-round occupancy of **our own** 8
  core-ring sockets, and the belt-head decomposition. Output:
  `scratchpad/s51_route/route_games.tsv`, 900 rows, **0 parse failures**.
* **`scratchpad/s51_route/render.py`** — ASCII board dump, used for the two worked cases in §3.

**Every guard was driven to BOTH verdicts.**

| control | PASS branch | the branch that must also exist |
|---|---|---|
| replay `winner` vs the results tape | **900/900 agree**, 0 parse failures | seat deliberately swapped: the `won` column flips and **87 columns** change |
| `min_vertex_cut` | 1-wide corridor → 1; 3-wide slab → 3; three welded rows → 3 | disconnected fixture → **0**; and the "two corridors" fixture returned **2 against the author's guessed 3 — the tool was right and the expectation was wrong**, recorded in the selftest |
| eco-connectivity ("harvester has a route home") vs the ENGINE's `titaniumCollected` | 537 games wired **and** collecting; 236 unwired **and** collecting nothing | **false positives: 0 of 900.** False negatives: 127, of which **124 were wired at an EARLIER snapshot** — `titaniumCollected` is cumulative, wiring is instantaneous. **3 residual (all fjordgate).** |
| `death_mid` (transit deaths) reads 0.00 on all 15 maps | the branch is alive: **5/900 games** fire it, `death_home` fires in 86, `death_apron` in 502 — all three computed by the same branch on the same coordinates | a dead branch would zero all three; it does not |
| no column may be FLAT across the 15 maps | `harv1_rnd` 2.0→66.7, `ti_coll100` 0→715, `head₂` 3.0→97.9, `rev_rate` 0.209→0.621 | none flat |
| map symmetry (load-bearing for §1.5) | 8 maps tested, each **0 mismatched tiles** under a symmetry carrying core A onto core B | **the first version of this test used the ANCHOR map (w−2−x) instead of the TILE map (w−1−x) and reported 56–202 mismatches — a false asymmetry.** Corrected; the wrong version is why this row exists |
| within-map both-value check | royale `harv_wired100` takes 5 distinct values; icefloe `throws_ours` takes 39 | icefloe `ti_coll100` is 0 in **60/60** — a genuine constant, cross-checked against the engine's own counter, not an instrument artefact |
| **at-ring presence vs the INDEPENDENT walker** `scratchpad/s51_rush_autopsy/tape.py` (`near_bot`) | under **matched geometry** (their radius: d² ≤ 8 from the enemy core *centre*): **2,361 of 2,361 rounds EXACT count agreement** across 6 games on 6 maps | their tool run on the **inverted seat**: 14.9% / 26.2% / 56.7%. **The first attempt agreed only 77.6% because the two tools use different radii** (centre vs footprint) — a definitional gap, not a walker defect, and it is recorded here because a 77.6% "agreement" would have been published as a weak pass |

**Reused, not re-derived:** wire parsing `tools/replay_census.py`; map decode
`tools/map_encode.py`; the DEFF constant 1.130 from the ring study's own seed-pair measurement on
this exact fixture.

---

## 3. The per-map opening / route table

`head₂` = first round a conveyor of ours stands one BFS step from the core footprint (the belt
head arrives). `eseal₁` = first round any enemy entity stands on one of our 8 core-ring sockets.
`margin = eseal₁ − head₂`. `belt fail` = games in which no conveyor of ours ever reaches a ring
socket. `ore_d1` = BFS steps from our core to the nearest ore tile. `mincut` = vertex-disjoint
corridors between the cores. Means over 60 games/map unless a column is restricted to games where
the event occurred.

| map | size | ore_d1 | mincut | win | harv1 | conv1 | head₂ | eseal₁ | **margin** | belt fail | coll100 | oppcoll100 | arr16 | hops | 1st contact | deaths mid | deaths apron | their core hit |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ragnarok | 30x30 | 3 | 6 | 60/60 | 3.0 | 4.5 | 4.5 | 57.5 | **+53.0** | 0/60 | 365 | 201 | 14.0 | 5.0 | 12.5 | 0 | 0.0 | 100% |
| royale | 20x20 | 6 | 4 | 55/60 | 6.0 | 7.0 | 12.2 | 149.7 | **+137.5** | 0/60 | 715 | 183 | 8.0 | 2.0 | 9.8 | 2 | 2.8 | 100% |
| nordkap | 20x26 | 4 | 8 | 39/60 | 5.0 | 6.0 | 6.0 | 13.7 | **+7.7** | 0/60 | 244 | 197 | 6.0 | 1.0 | 6.0 | 0 | 1.5 | 68% |
| frostgate | 20x20 | 3 | 8 | 37/60 | 3.4 | 4.4 | 4.4 | 10.9 | **+6.5** | 0/60 | 368 | 199 | 9.8 | 1.6 | 6.0 | 0 | 0.2 | 100% |
| drakkarfjord | 30x30 | 9 | 8 | 33/60 | 9.0 | 10.0 | 21.0 | 11.0 | **−10.0** | 30/60 | 200 | 44 | 14.0 | 5.0 | 22.5 | 0 | 1.6 | 78% |
| midgard | 30x30 | 3 | 8 | 30/60 | 3.6 | 4.6 | 4.6 | 19.8 | **+15.2** | 0/60 | 596 | 634 | 41.9 | 0.0 | 14.3 | 1 | 2.0 | 65% |
| valkyrie | 30x30 | 6 | 8 | 27/60 | 7.0 | 8.0 | 13.0 | 30.9 | **+17.9** | 0/60 | 358 | 209 | 11.0 | 3.0 | 21.4 | 1 | 2.1 | 71% |
| antler | 14x18 | 2 | 8 | 26/60 | 2.0 | 3.0 | 3.0 | 8.0 | **+5.0** | 0/60 | 543 | 395 | 5.0 | 1.0 | 8.5 | 0 | 0.6 | 73% |
| archipelago | 26x26 | 4 | 6 | 25/60 | 7.0 | 8.1 | 8.4 | 8.3 | **−0.1** | 0/60 | 618 | 563 | 32.6 | 0.0 | 14.7 | 1 | 1.4 | 78% |
| fjordgate | 10x10 | 3 | 6 | 22/60 | 3.6 | 4.6 | 4.6 | 6.1 | **+1.5** | 0/60 | 295 | 250 | 0.0 | 0.0 | 3.6 | 0 | 1.7 | 65% |
| drumlin | 25x25 | 4 | 8 | 20/60 | 4.0 | 5.0 | 6.5 | 10.1 | **+3.6** | 0/60 | 182 | 140 | 11.0 | 2.0 | 10.2 | 0 | 0.5 | 96% |
| glacierkeep | 30x30 | 11 | 8 | 16/60 | 66.7 | 68.5 | 97.9 | 10.3 | **−87.6** | 39/60 | 3 | 32 | 11.0 | 3.0 | 16.2 | 0 | 2.3 | 60% |
| yulerune | 20x20 | 6 | 6 | 11/60 | 5.0 | 6.0 | 11.0 | 5.5 | **−5.5** | 30/60 | 76 | 259 | 12.3 | 2.5 | 15.0 | 0 | 1.6 | 48% |
| auroraveil | 20x20 | 8 | 5 | 10/60 | 11.0 | 15.0 | 56.9 | 6.5 | **−50.4** | 45/60 | 10 | 130 | 10.7 | 2.5 | 11.9 | 0 | 1.9 | 13% |
| icefloe | 20x20 | 6 | 7 | 8/60 | 7.0 | 8.0 | 15.8 | 9.5 | **−6.3** | 49/60 | 0 | 246 | 10.0 | 3.0 | 12.7 | 0 | 1.5 | 15% |

**Read the `margin` column top to bottom against `belt fail` and there are no exceptions.**
The only boundary case is archipelago at −0.1, which finishes 60/60 — and archipelago is one of
the two maps where `_fs_map_gated` turns the ferry-siege OFF entirely.

**Two things the table also settles, both negatives:**

* **The opening CHAIN is not late on the craters.** First harvester r5–r7 on icefloe/yulerune
  against r6 on royale; first conveyor r6–r8 against r7. Only glacierkeep (harv1 **r66.7**) and
  auroraveil (r11) open late, and glacierkeep's cause is on the board — its nearest ore is
  **11 BFS steps** from the core, the deepest in the pool.
* **Arrival is not the problem, and `hops` says why.** Our head ferries a body forward by
  successive launcher throws — engine-visible as a `moveBuilderBot` of Chebyshev step > 1. The
  first arrival at their near band takes **2–3 hops** on the craters and **5** on ragnarok. The
  ferry works everywhere.

**The belt clock is set at r0 by the board.** `r(head₂, ore_d1) = +0.833` at n = 15: ore_d1 ≤ 4 ⇒
head₂ ≤ 8.4 on every such map; ore_d1 ≥ 6 ⇒ head₂ 11.0–97.9. The enemy clock is weakly set by
corridor count, `r(eseal₁, mincut) = −0.575`.

---

## 4. The ranked failure chain on the craters

Crater trio = icefloe + auroraveil + yulerune. **151 losses, 29 wins.** Control column is
**sweep wins** (ragnarok + royale, n = 115) — the matched "this went right" fixture.

Ranked by measured separation from the control, not by narrative appeal.

| # | condition | crater LOSS | crater WIN | sweep WIN | L − sweepW |
|---|---|---|---|---|---|
| 1 | enemy on our core ring **before** our belt head | 92.7% | 100.0% | 0.0% | **+92.7pp** |
| 2 | their core NEVER damaged by us | 87.4% | 6.9% | 0.0% | **+87.4pp** |
| 3 | zero titanium delivered by r100 | 84.8% | 65.5% | 0.0% | **+84.8pp** |
| 4 | ≥3 of our 8 ring sockets carry an enemy **barrier** by r30 | 93.4% | 93.1% | 9.6% | **+83.8pp** |
| 5 | zero titanium delivered ALL GAME | 80.1% | 24.1% | 0.0% | **+80.1pp** |
| 6 | belt NEVER reaches a ring socket | 77.5% | 24.1% | 0.0% | **+77.5pp** |
| 7 | our core hit before theirs | 84.8% | 10.3% | 52.2% | +32.6pp |
| — | *REFUTED BELOW* | | | | |
| R1 | a bot of ours thrown BACKWARD (kidnapped) | 29.1% | **48.3%** | 2.6% | +26.5pp — **higher in crater WINS** |
| R2 | any of our bots died on a choke tile | 14.6% | 10.3% | 0.0% | +14.6pp, n small |
| R3 | deaths concentrated on one tile (≥40%, n≥3) | 7.3% | **27.6%** | 3.5% | +3.8pp — **higher in WINS** |
| R4 | a builder stalled at home 40+ rounds | 19.9% | 17.2% | **34.8%** | **−14.9pp** |
| R5 | raid arrival later than r20 | 0.0% | 0.0% | 0.0% | 0.0 |
| R6 | no bot ever reaches their near band | 0.0% | 0.0% | 0.0% | 0.0 |
| R7 | majority of our bot deaths mid-route | 0.0% | 0.0% | 0.0% | 0.0 |

**Rows 1 and 4 are near-universal in crater WINS too (100% and 93.1%)** — the seal is *necessary*
for a crater loss and nowhere near *sufficient*. **The rows that discriminate INSIDE the crater
trio are 2, 5 and 6:** the belt, the delivery, and whether we ever touch their core.

### 4.1 The within-map cut, and what it can carry

Restricted to the five maps that produce **both** belt outcomes (drakkarfjord, glacierkeep,
yulerune, auroraveil, icefloe), so the map is controlled by construction:

| belt ever reached home | n | win rate (95% CI, DEFF 1.130) |
|---|---|---|
| yes | 107 | **55.1% ± 10.0** |
| no | 193 | **9.8% ± 4.5** |

**Gap +45.3pp ± 12.6.** Per map: icefloe **63.6% vs 2.0%**, yulerune 30.0% vs 6.7%, auroraveil
40.0% vs 8.9%, drakkarfjord 96.7% vs 13.3%, glacierkeep 38.1% vs 20.5%.

### 4.2 The censoring probe — because the ring study's mistake is available here too

A belt that connects at r485 on a game that ran 1,000 rounds is a *consequence* of surviving.
Median `head₁` where it happens: drakkarfjord r23, yulerune r13 — but glacierkeep r383,
auroraveil r213, **icefloe r266**. So the raw cut above is partly censored.

Re-cut on **belt home by r60**, restricted to games that lasted ≥60 rounds so both cells are
observable: **63.1% ± 12.5 (n = 65) vs 15.7% ± 5.0 (n = 235), gap +47.3pp ± 14.6.** The estimate
survives.

### 4.3 ⛔ AND THEN IT FAILS A COLLINEARITY CHECK. THE ATTRIBUTION IS REFUSED.

The censoring-resistant cut is carried by two maps, and on both of them **"belt home by r60" is
the SEAT, exactly**:

| map | seat A: belt home by r60 | seat A win | seat B: belt home by r60 | seat B win |
|---|---|---|---|---|
| drakkarfjord | **0/30** | 4/30 | **30/30** | 29/30 |
| yulerune | **0/30** | 2/30 | **30/30** | 9/30 |

Perfectly collinear. *"Our belt finished"* and *"we are on the good seat"* fit the data
identically, and **no cut of this fixture can separate them** — the same hazard `CLAUDE.md`
records for The Bisons' v4. ⇒ **I do not bank +47.3pp as the causal effect of finishing the belt.**

**What survives the refusal, and it is the more interesting half:** those boards are **tile-exact
symmetric** (drakkarfjord 0/900 mismatches under rot180), our belt clock is identical on both
seats (`head₂` median 21 / 21 on drakkarfjord, 11 / 11 on yulerune) and so is theirs (`eseal₁`
median 11 / 11 and 5 / 6). **A 25-of-30 swing on a mirror-image board with identical clocks is not
a map effect and not a timing effect. It is orientation-dependence in the players' code.**

Worked case, `drakkarfjord_s300`, both seats, from `render.py`:

* **seat B** — belt climbs x = 26 from y = 13; at r21 the head is at (26,7), at **r23 it lays
  (26,6)**, a ring socket. At r20 that socket read `.`; the enemy held the west and north sockets
  instead. Belt home, 715-class economy, we win.
* **seat A** — belt descends x = 3 from y = 17; at r21 the head is at (3,22). Its socket is
  **(3,23) — the exact rot180 image of seat B's (26,6) — and at r20 it already reads `Ex`, an
  enemy barrier.** Three other ring sockets were empty in that round. The belt sits at (3,22) for
  the rest of the match.

### 4.4 The re-plan headroom — the half that is ours

For every round after the head arrives, in the games where the belt never gets home: is the head's
**own** socket free (we could finish and didn't), or denied — and if denied, is **another** socket
empty?

| map | belt-fail games | head's own socket free | **another socket free while ours is denied** | rounds/game | steps to it |
|---|---|---|---|---|---|
| icefloe | 49/60 | 3.1% | **87.7%** | **256.5** | 2.84 |
| auroraveil | 34/60 | 10.7% | **53.9%** | 143.4 | 3.51 |
| drakkarfjord | 30/60 | 0.3% | **43.9%** | 412.3 | 3.98 |
| glacierkeep | 37/60 | 3.3% | **27.8%** | 179.7 | 4.06 |
| yulerune | 30/60 | 0.2% | **24.1%** | 39.5 | 3.88 |

**Their seal is the trigger and it is genuinely effective — the socket we are pointed at is enemy-
held 96.9–99.8% of the time we sit next to it.** *(Inference, and it is the strong one: the enemy
building is present on that tile before our head arrives in 92.7% of crater losses, and a barrier
is by definition inert, so the direction of this particular arrow is not in doubt.)*

**Our no-re-plan is the amplifier, and it is the expensive half.** On icefloe, for 256 rounds a
game, a legal landing socket sat empty **2.84 steps away** — about three conveyors, 9 Ti at base
scale — and the belt never moved. *(Inference: the counterfactual value of those three conveyors
is not measured, only their availability and price. What is measured is that the tiles were empty,
reachable and never used.)*

---

## 5. The code, and it names this defect itself

Every line below was opened and read in `bots/_v525flip`.

* `eco.py:700` `_link_path(self, ct, hpos)` plans **one** route, a reverse multi-source BFS from
  `_link_goals` (`eco.py:669`, the 8 ring tiles minus a ban) out to the harvester.
* `eco.py:448` `_pave_ban()` returns `self._seat_ban() if HS_SEAT_BAN_CONVEYORS else None`, and
  **`HS_SEAT_BAN_CONVEYORS = False`** (`doctrine.py:646`) — so all 8 sockets are legal goals. **The
  seat-reservation road is closed; we are not banning ourselves off our own ring.** *(Checked
  because it was the first hypothesis and it is wrong.)*
* `doctrine.py:1827-1834`, the LOKI-L4 block, states the defect in our own words:

  > *"`_link_path` plans one route when a harvester is built and `_build_next_link` pops each tile
  > as it lays it; after the queue drains there is no planner left."*

  and at `doctrine.py:1866-1868`:

  > *"of the repairs the belt half fired on, only 1 tile had ever HELD a conveyor. The rest are
  > **DEAD HEADS** — chains this bot abandoned mid-walk, which `_build_next_link` never revisits
  > because it pops its queue as it lays it."*

* The repair plank we do ship is explicitly scoped **away** from this case
  (`doctrine.py:1856-1858`): *"a tile is only repaired when there is already chain on BOTH sides of
  it, which makes it a HOLE rather than a HEAD. Extending a dead head toward the Core is the pave
  trail"* — and **`PAVE_TRAIL_ON` is False** (stated at `doctrine.py:1847`). `LOKI_L4_REPAIR_ON =
  True` (`doctrine.py:1872`) repairs holes only.

⇒ **`L4` repairs HOLES. The crater failure is a HEAD. There is nothing in the shipped bot that can
ever finish a belt whose terminal socket was taken while the queue was draining.** The defect was
written down on 2026-08-12 as an economy note under `R1000_IS_DEFEAT`; this autopsy prices it as a
**map-selecting** defect worth 30–49 games in 60.

Two further map-conditional facts, from the parallel code read (verified against the map files):

* **`MAP_CODES` covers all 15 pool maps, byte-identical to a re-encode** — the s36 "no map entry ⇒
  livelock" failure is **not** live in v525flip. Consistent with `rev_rate` never degenerating
  (0.209–0.621 across maps, no map near 1.0).
* **`_fs_map_gated` (`siege.py:480-583`) turns the ferry-siege ON for 13 of 15 maps**, OFF only for
  archipelago (`FS_MAP_SKIP`) and midgard (`FS_V525_CRIPPLE_MAPS`). **v525 moved yulerune OFF→ON**,
  and `doctrine.py:3883` records its own measured reason for the previous OFF:
  *"yulerune — gunner +7.46 / rush −36.07"*. yulerune is 11/60. **icefloe and auroraveil were
  already ON in the parent, so the flip does not explain them** — it is a yulerune-specific
  suspect, not the headline.

---

## 6. royale vs yulerune — the matched pair

Both **20×20**. Both `ore_d1 = 6`. Both `narrow = 2`. Our opening is **the same bot doing the same
thing**: first harvester r6.0 / r5.0, first conveyor r7.0 / r6.0, nearest harvester 6 BFS steps
from home in both, belt head one step from home at **r12.2 / r11.0**.

| | royale | yulerune | yulerune A | yulerune B |
|---|---|---|---|---|
| win | **55/60** | **11/60** | 2/30 | 9/30 |
| first harvester | 6.0 | 5.0 | 5.0 | 5.0 |
| first conveyor | 7.0 | 6.0 | 6.0 | 6.0 |
| head₂ (belt head one step out) | 12.2 | 11.0 | 11.0 | 11.0 |
| **eseal₁ (enemy on our ring)** | **49.2** | **5.5** | 5.0 | 6.0 |
| enemy barriers on our ring @r30 | **0.0** | **5.6** | 5.5 | 5.8 |
| belt home | 60/60 | 30/60 | **0/30** | 30/30 |
| `titanium_collected` @r100 | **715** | **76** | **0** | 152 |
| their `titanium_collected` @r100 | 183 | 259 | 343 | 175 |
| our raid at their near band | r8.0 | r12.3 | r12.6 | r12.1 |
| their core min HP | **41.9** | **351.4** | 466.7 | 236.1 |
| our core min HP | **446.3** | **91.7** | 33.3 | 150.0 |

**The two boards differ in exactly one thing that matters, and it is layout, not size:
royale's `mincut = 4` is the LOWEST in the 15-map pool; yulerune's is 6.** royale's middle band is
two boxed wall clusters that pinch the board to four vertex-disjoint corridors; yulerune is open
(wall 7.0% vs 11.0%). **Their raid needs 49 rounds to touch our ring on royale and 5.5 on
yulerune.** Our belt is ready at r11–12 either way. **We win royale because the board buys our belt
37 rounds of clear air, not because we play royale better.**

*(Inference, and it is the one this pair is for: since the opening chain is numerically identical
on the two maps and the only pre-contact divergence is `eseal₁`, an opening-quality explanation of
the 92% / 18% split has nothing left to sit on.)*

---

## 7. Spec implications for the ANTI-RING build

The ring study's §6 already said: do not buy more socket denial at **their** core. **This autopsy
relocates the plank to OUR core, where the denial is happening TO us and where we have no answer
at all.**

1. **SHIP A BELT-HEAD RE-PLAN. THIS IS THE WHOLE FINDING AND IT IS CHEAP.**
   Trigger: our belt head sits at BFS distance 2 from the core footprint, its output socket is
   occupied by a non-friendly entity, and ≥1 other ring socket is empty. Action: re-run
   `_link_path` from the head against the *currently free* goal subset and lay toward it.
   **Measured availability: 87.7% of 256 rounds/game on icefloe, 53.9% on auroraveil, 43.9% on
   drakkarfjord, at a median 2.8–4.1 Manhattan steps (≈3 conveyors, ~9 Ti at base scale).**
   This is a HEAD, so `LOKI_L4_REPAIR_ON` cannot reach it by construction
   (`doctrine.py:1856-1858`) — it needs its own trigger, not a widened L4. **Do not re-enable
   `PAVE_TRAIL_ON` to get this: LOKI-13 measured that at 38.2 conveyors/game and it is a different,
   unbounded plank.** Gate the new rule on *head-adjacent, socket-denied, own-half* so it stays a
   ~3-conveyor action.

2. **DEFEND THE LANDING SOCKET, NOT THE WHOLE RING — AND ONLY THE ONE THE BELT IS AIMED AT.**
   `titanium_collected` needs exactly **one** conveyor facing a core tile. Their evict arm spends
   itself on breadth (the ring study: 54,490 pecks, 99.76% into barriers). Reserving/holding **one**
   socket with a body from the round the belt is planned is the minimal counter, and it is the one
   `_free_seats`/`HS_DELIVERY_SEATS = 2` machinery already has the vocabulary for. **Do not buy a
   ring collar at home** — §4's row 4 shows ≥3 sockets sealed by r30 in **93.1% of crater WINS**
   too, so broad home-ring denial is not what separates the outcomes.

3. **MAKE THE BELT WIN THE RACE ON THE MAPS WHERE IT CAN, BY SHORTENING IT.**
   `r(head₂, ore_d1) = +0.833`. On glacierkeep the nearest ore is **11 BFS steps** out and our
   first harvester lands at **r66.7** — the belt has already lost before it starts. On such boards
   the first harvester should be sited for **belt length**, not ore proximity to the *bot*, or the
   eco plank should be skipped in favour of putting the 500 Ti straight into the kill. **A
   non-regression note for the builder:** this is an economy change and economy is instrumental
   under `R1000_IS_DEFEAT`, so it must clear `DEFENCE_ADMISSION_BAR` on timely-kill rate, not on
   `titanium_collected`.

4. **THE MAP CLASSIFIER — AND IT DOES NOT NEED THE MAP, IT NEEDS ROUND 10.**
   * **At r0, from the map table the bot already has:** `head₂ ≈ f(ore_d1)`; `ore_d1 ≥ 6` marks
     every crater-class board (icefloe 6, yulerune 6, auroraveil 8, drakkarfjord 9, glacierkeep 11)
     and `ore_d1 ≤ 4` marks every map that finished the belt 60/60 except royale and valkyrie. A
     **cheap, correct, and sufficient** classifier for pre-committing the re-plan budget.
   * **At r5–r12, and this is the better signal because it is direct:** the core's own vision
     (r² = 36) covers all 8 ring sockets at d² ≤ 2 every round. **`eseal₁ < head₂` is readable live,
     costs one `get_tile_building_id` per socket, and separates the pool without a single
     exception** (5 maps below 0 → belt fails 30–49/60; 10 maps at or above → 0/60). Write the
     verdict to a comms slot at r12 and let the eco and siege arms branch on it.
   * ⚠ **Do NOT classify on size, core separation, path length, wall %, ore count or corridor count
     alone.** r(win%, mincut) = −0.165, r(win%, bfs) = +0.226, r(win%, wall%) = +0.089 at n = 15 —
     the ring study's negative result reproduces exactly. **Only the race margin has structure
     (+0.747), and it is a margin between two clocks, not a property of the board.**

---

## 8. What this does NOT establish

* **The +0.747 is n = 15 and between-map.** It is not a significance claim.
* **The +45.3 / +47.3pp belt-home effect is REFUSED (§4.3)** — perfectly collinear with seat on the
  two maps that carry it. **What would decompose it:** a paired local leg on drakkarfjord and
  yulerune with the re-plan of implication 1 as the ONLY delta, both seats, ≥30 seeds. If the seat
  effect is the belt, seat A's belt-home rate moves off 0/30 and its win rate moves with it; if it
  is something else in the mirror, the belt finishes and the seat gap survives. **That leg is a
  direct test of implication 1 and should be the builder's first anti-ring iteration.**
* **The enemy's arrival at our ring is not exogenous.** A team that is winning arrives earlier. The
  ordering constraint (§4, row 1: their building is on the socket *before* our head arrives in
  92.7% of crater losses, at r5.5–r10.3, before first contact at r11.9–15.0) and the r0-determined
  belt clock (r = +0.833 with ore_d1) bound the direction but do not eliminate it.
* **One opponent, one head, local harness.** `_x3r0v165mjolnirB` builds barriers on our ring early;
  a ladder opponent that does not would show none of this. **The re-plan of implication 1 is
  opponent-independent** (it fires on *any* denial, including our own bodies) — that is the reason
  to prefer it over anything tuned to x3r0's seal pattern.

---

## 9. Provenance

* **H1/H2 addendum (Magnus, mid-flight): both REFUTED — §0.** Raiders die *later* on the craters
  (first apron death r144.6 vs r65.3; indistinguishable at r25 under the censoring control) and
  establish at their ring in **900/900** games at r11.0 vs r11.3. Machinery cross-checked against
  `scratchpad/s51_rush_autopsy/tape.py` at 2,361/2,361 rounds under matched geometry.
* Instruments: `scratchpad/s51_route/mapgeom.py` (`--selftest`, `--table`),
  `scratchpad/s51_route/routetape.py` (`--game`, `--batch`, `--selftest`),
  `scratchpad/s51_route/analyse.py`, `scratchpad/s51_route/render.py`.
* Per-game output: `scratchpad/s51_route/route_games.tsv`, 900 rows, 0 parse failures,
  winner-vs-tape 900/900.
* Reused: `tools/replay_census.py`, `tools/map_encode.py`; DEFF 1.130 from
  `docs/research/RING-ENGAGEMENT-mjolnir-2026-08-20.md` §1.3.
* Bot trees read: `bots/_v525flip` (eco.py, siege.py, doctrine.py, main.py, raid.py).
* No platform call, no download, no `corpus/*.tsv` read or rewritten.
