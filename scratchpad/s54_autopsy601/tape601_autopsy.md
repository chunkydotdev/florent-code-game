# tape601 AUTOPSY — cage-barrier collapse (Q1) and the 42-builder respawn storm (Q2)

**Builder s54, 2026-08-21. Read-only decode agent. No repo edits, no matches, no commits.**
Subject: `bots/_v601skalman` vs a NOISE_OFF `_v542wave` copy, 30 games
(`scratchpad/s54_fidtape/replays_tape601/`, `*_A` = we are side 0, `*_B` = side 1).
Comparison: `bots/_v600skalman1` on the same 15 maps, seat A only
(`scratchpad/s54_fidtape/replays_tape30/*_s11.replay26`; the `_s12` files are
duplicate pairs and are excluded throughout).

## 0. Instruments and their validation

| instrument | provenance | validation run here |
|---|---|---|
| `tools/skalman_fidelity.py::scan_replay` | the same code that produced the published M2a/M5 rows | used unmodified for per-game barrier/ring/builder counts |
| `scratchpad/s54_autopsy/tape30_deaths.py` | prior autopsy, damage-signature attribution, 0/246 self-check | attribution logic replicated in the walker decoder below |
| **NEW** `…/scratchpad/walker.py` | this session; per-builder role/lap/action tracker | **cross-validated 45/45 games**: per-bot ring-barrier sums equal `skalman_fidelity`'s independent `barriers_on_enemy_ring` in every one of the 45 games |
| **NEW** heuristic role inference (simulates `_claim_role`) | `sk_roles.py:158-183`, `SK_BEAT_STALE=3` (`sk_maps.py:137`) | **13/13** agreement with `skalman_fidelity._roles`' independent ring-barrier recogniser wherever it names a walker; and **52/52** ring barriers across all 45 games are attributed to inferred role 1, **0** to roles 0/2/3 — the attributor *can* assign to other roles (it does so for conveyor/harvester/gunner builds) and never does for ring barriers |

**Both-ways drive for the walker-action counter** (the counter this analysis rests on):
run on `glacierkeep_s11` (v600) it reads **6 barrier builds / 0 core pecks** for walker
id 5 over rounds 28-44 — the case where the walker demonstrably built ring barriers;
run on `glacierkeep_A` (v601) for the *same* id 5 over the *same* rounds it reads
**0 builds / 41 core pecks**. The counter produces both verdicts.

⚠ **DENOMINATOR CORRECTION TO THE BRIEF.** "80 barriers on tape30" double-counts the
`_s11`/`_s12` duplicate pair. The distinct-game figures are **v600: 40 barriers / 29 on
the enemy ring = 72.5% over 15 games**; v601 seat A **20 / 10 = 50.0%**, seat B
**23 / 13 = 56.5%** — 15 games each. Every number below uses distinct games.

---

# Q1 — why cage barrier volume collapsed

## 1.1 The answer in one line

**The walker was not absent, not late and not dead. Its ACTIONS were redirected.**
`_peck_priority` was inserted into `_cage_walker` at **`bots/_v601skalman/sk_roles.py:1534`**,
between the seal-behind and the lap advance. The enemy core footprint is orthogonally
adjacent to **every** seal tile by construction (`cage_lap`, `sk_roles.py:78-96`;
`LAP_SEAL_IDX`, `sk_roles.py:99`), and `_target_pri` scores `CORE` at the top of the
ladder (`SK_PRI_CORE = 6`, `sk_maps.py:250`; `sk_roles.py:1385-1386`). So from any seal
tile `_peck_priority` returns True **every round**, `return`s, and the `step_to` lap
advance at `sk_roles.py:1555-1560` is never reached. A builder cannot act and move in the
same round, so **the lap stops dead at the first seal tile the walker steps on.**

## 1.2 The measured decomposition (walker = inferred role 1; 15 v600 games vs 30 v601 games)

| | v600 (15 g) | v601 A+B (30 g) | ratio |
|---|---|---|---|
| cage bodies | 26 | 62 | — |
| cage-role builder-rounds | 4,026 | 6,009 | — |
| **lap-rounds** (walker standing on the enemy 12-tile lap) | **311** | **756** | — |
| lap-rounds **per game** | 20.73 | 25.20 | **×1.215** |
| lap ACTIONS (build+peck+heal while on the lap) | 42 | 309 | — |
| actions per lap-round | 0.135 | 0.409 | **×3.026** |
| of those actions: **barrier builds** | **29** (69.0%) | **23** (7.4%) | ×0.108 |
| of those actions: **pecks** | 13 (31.0%) | 286 (92.6%) | ×8.9 |
| **ring barriers per game** | **1.933** | **0.767** | **×0.397** |
| ring barriers **per lap-round** | 0.0932 | 0.0304 | **×0.326** |

**Log decomposition of the −60.3% per-game collapse (total −0.925 nats):**

```
presence (lap-rounds/game)        +0.195   HELPS   (walker is at the ring MORE)
action rate (actions/lap-round)   +1.107   HELPS volume, but it is a pure PECK term
build share of actions            -2.227   THE ENTIRE LOSS
                                  ------
                                  -0.925
```
Two-term form: **builds-per-lap-round contributes +121% of the collapse; walker presence
offsets −21%.** Nothing else is in the identity.

**Robustness:** fimbulwinter contributes 0 lap-rounds and 0 ring barriers in all three
arms, so dropping it (14 v600 games / 28 v601 games) leaves every ratio unchanged
(presence ×1.216, ring barriers/game ×0.397). The decomposition is not an artefact of the
storm game.

**The total barrier drop is 100% the cage.** Barriers built by role, 15 games per arm:

| arm | cage (ring) | ore denier | siege engineer | **total** |
|---|---|---|---|---|
| v600 | **29** | 1 | 10 | **40** |
| v601 A | **10** | 1 | 9 | **20** |
| v601 B | **13** | 0 | 10 | **23** |

Non-cage barriers are flat (11 → 10 → 10). Every barrier lost is a ring barrier the cage
walker did not lay.

## 1.3 What the pecks were aimed at — the smoking gun

| arm | cage-walker pecks by target kind | cage-walker builds |
|---|---|---|
| v600 | **conveyor 13 / 13** (i.e. `_clear_tile` lap eviction) — **core 0** | barrier 29 |
| v601 A | **core 156 / 156** | barrier 10 |
| v601 B | **core 120**, conveyor 10 (of 130) | barrier 13 |

v600's walker never once pecked the enemy core (0 of 42 lap actions). v601's walker
spent 92.6% of its lap actions on it.

## 1.4 The lap froze — dwell and coverage

| | v600 | v601 A | v601 B |
|---|---|---|---|
| worst single-tile dwell (consecutive rounds on one lap tile) | **10** | **42** | **55** |
| per-game dwell on the maps where the walker laps | 2, 2, 10, 1, 2, 1, 1 | 12, 42, 13, 26, 29, 9, 8 | 12, 14, 15, 10, 6, 7, 55 |
| lap-rounds ÷ distinct lap tiles visited | **5.3** | **11.9** | 7.1 |

v600's walker moves nearly every round (dwell 1-2 = a walking lap). v601's parks.

**Where on the lap it parks is the tell.** Split the lap-rounds into SEAL tiles (the 8
face tiles — the enemy core is orthogonally adjacent to each by construction) and CORNER
tiles (the 4 pass-through tiles — the core is *diagonal*, so `_peck_priority` finds
nothing there):

| arm | seal-tile rounds | corner rounds | seal:corner | **core pecks** | core pecks per seal-tile round |
|---|---|---|---|---|---|
| v600 | 116 | **195** | 0.59 | **0** | **0.000** |
| v601 A | **368** | 61 | **6.03** | 156 | 0.424 |
| v601 B | **237** | 90 | 2.63 | 120 | 0.506 |

v600's walker spends *more* time on corners than on seal tiles — it is passing through.
v601's walker is 10× more likely to be sitting on a seal tile, which is exactly the tile
class where `_peck_priority` can find the core. (The rate is below 1.0 because
`hp_trend_ok`/`gave_up` eventually latches — see §1.8 — and because the peck needs 2 Ti.)

## 1.5 WORKED EXAMPLE — glacierkeep, walker id 5, both arms, same seed, same map

Enemy core at (14,26); lap tile index 1 = (14,25). **Both arms put walker id 5 on lap
tile 1 at exactly round 28** — everything upstream of the ring is behaviourally identical.

```
v600  r28 MOVE→(14,25)  r29 MOVE→(15,25)  r30 BUILD (14,25)   ← seals behind
      r31 MOVE (corner) r32 MOVE r33 MOVE r34 BUILD (16,26)
      r35 MOVE r36 BUILD r37 MOVE r38 MOVE r39 BUILD r40 MOVE r41 BUILD
      r42 MOVE r43 MOVE r44 BUILD (13,27)
      ⇒ 6 barriers in 17 rounds, all 12 lap tiles walked, max_seal 6 of 8

v601A r28 MOVE→(14,25)
      r29..r69  PECK (14,26) ← ENEMY CORE, 41 CONSECUTIVE ROUNDS, never moves
      r70..r90  2-tile shuttle (14,25)↔(14,24) after the give-up latch fires
      ⇒ 2 barriers in 173 lap-rounds, 12 lap tiles but max_seal 2 of 8
```
**v601A had 6× the ring presence (173 vs 29 lap-rounds) and one third the seal.**
Path: r28 leaves the walker at `here = 1`; `back = (1-1) % 12 = 0`, a CORNER index not in
`LAP_SEAL_IDX`, so the seal-behind at `sk_roles.py:1526-1528` is skipped; v600 then fell
through `_clear_tile` (False — forward tile empty) to the lap advance; v601 hits
`_peck_priority` at **`sk_roles.py:1534`** first, finds the core adjacent, fires, returns.

## 1.6 The other four candidates, measured and ranked

| rank | candidate | measurement | verdict |
|---|---|---|---|
| **1** | **`_peck_priority` preempting the lap advance** (`sk_roles.py:1534`) | 286/309 (92.6%) of v601 walker lap actions are pecks, 276 of them at the enemy core; 0/42 in v600. Dwell 2 → 42/55. Accounts for +121% of the collapse | **THE CAUSE** |
| 2 | **(b) walker deaths** | cage bodies dying, **excluding the fimbulwinter storm game**: v600 12/25 (48%), v601A 12/22 (55%), v601B 6/19 (32%). Median lifespan-of-dead 44 → 29 (A) / 33 (B). Killers: gunner/sentinel, **0 no-damage removals in any arm** (no exception-channel deaths). Sign is inconsistent across seats | **≈0 net; cannot be the cause — lap-rounds went UP 21%** |
| 3 | **`_clear_tile`'s new `_enemy_builder_adjacent` refusal** (`sk_roles.py:1672`) | forward-lap-tile-occupied lap-rounds 46 (v600) → 271 (v601); refusal predicate true on **18 of 756 v601 lap-rounds (2.4%)** — and, as a both-ways control, the same purely geometric predicate reads **2 of 311** on v600 (where the guard does not exist in code), so the counter is not stuck at zero. And every one is *downstream* of #1 — `_peck_priority` already consumed the turn | **≈0 marginal** |
| 4 | **(a) walker late / never reaching the ring** | **First-lap-arrival round is IDENTICAL v600 vs v601A on 7 of 7 maps where both arrive: 25/25, 29/29, 20/20, 31/31, 55/55, 17/17, 31/31.** Only holmgang differs (v600 r58, v601A never — that game's walker slot churned 6 bodies) | **ZERO contribution** |
| 5 | **(d) upstream — fewer walkers / role slots misfilled** | builders spawned 81 → 115 (A) / 73 (B); cage bodies 26 → 42 (A) / 20 (B); **15/15 games have ≥1 cage body in all three arms**; role tallies HOME/CAGE/ORE/SIEGE = 17/26/15/20 → 19/42/15/19 → 15/20/15/19 | **not a cause — more walkers, not fewer** |
| — | **`_belt_evict` / harvester escalation diverting the walker** | **Structurally impossible**: `_belt_evict` is reachable only from `_belt_action` (`sk_roles.py:688`) and `_escalate_target` only from `_home_keeper_move` (`sk_roles.py:1170`), both under role 0 `_home_keeper` (`sk_roles.py:244-271`). Confirmed in the data: cage-walker `build_kinds` is `{barrier: N}` in every arm — zero conveyors, zero harvesters | **REFUTED** |

## 1.7 Did the redirection buy anything?

Enemy-core pecks (2 dmg each), all our builders:

| arm | total | of which cage walker | ex-fimbulwinter | per round (ex-fimbulwinter) |
|---|---|---|---|---|
| v600 | 366 | 0 | 366 / 4,188 rds | 0.087 |
| v601 A | 1,166 | 156 | 281 / 2,297 rds | 0.122 |
| v601 B | 1,332 | 120 | 365 / 2,686 rds | 0.136 |

Outside the two fimbulwinter r1000 games (which contribute 1,852 of v601's 2,498 core
pecks without killing anything), **total core pecking is flat in absolute terms and up
~40-56% per round** — the cage walker took over core-pecking from the other roles
(non-cage core pecks 366 → 125 on seat A). **The barrier collapse did not buy a
proportionate amount of core damage.** Outcomes: 0/15 wins (v600) → 1/15 (A) → 2/15 (B),
and **all three v601 wins are r1000 tiebreaks**, which `R1000_IS_DEFEAT` scores as losses.

## 1.8 SECOND DEFECT FOUND IN THE SAME TRACE — the healing-race guard is blind to the core

`_peck_priority` refuses a target a live enemy builder is standing beside
(`sk_roles.py:1460` → `_enemy_builder_adjacent`, `sk_roles.py:1398-1420`) — the DOORWAVE
lesson. **That guard is TILE-local, and the core is a 2×2 entity.** A heal landing on any
one of the core's four tiles heals the whole core, so a healer standing beside a
*different* core tile is invisible to the guard.

Measured on the same glacierkeep v601A window (r25-95): **95 enemy heals onto the enemy
core footprint**, from exactly two builders —

| healer | standing on | heals core tile | count | orthogonally adjacent to (14,26), the tile our walker pecked? |
|---|---|---|---|---|
| id 6 | **(15,25)** — lap seal index 2, the walker's *next* lap tile | (15,26) | 49 | **No** |
| id 9 | (16,26) | (15,26) | 46 | **No** |

Enemy core HP over the walker's 41-round peck: fell 500 → 248 (mostly our sentinel's −20
and −10 shots), while the enemy healed **+6 to +8 per round against our +2 of peck**. The
core recovered to **500 by the end of the game** (min ever 136). **The walker spent 41
rounds losing precisely the race the guard exists to avoid** — and the healer was parked
on the seal tile the walker should have walked to.

⇒ **Fix candidate:** `_enemy_builder_adjacent` should test adjacency to the target
ENTITY's whole footprint, not to the single tile passed in — resolve `bid` and, for
`EntityType.CORE`, test all four tiles of `core_tiles()`.

## 1.9 The one-line fix candidate for the lap freeze (not built, not tested)

Gate `_peck_priority` at `sk_roles.py:1534` on the walker having **nothing to advance to**
— e.g. only call it when the lap-advance loop (`sk_roles.py:1555-1560`) would return no
step, or only when `sealed >= SK_CAGE_ACCEPT` (which is already the `_attack_enemy_core`
branch at `sk_roles.py:1509-1511`, and which contains the *same* peck call at
`sk_roles.py:1705` — that one is correct because by then the cage is done). A cheaper
variant: refuse the peck when the walker stands on a lap tile and any seal tile is still
open (`empty_seals` is already computed at `sk_roles.py:1502`).

---
# SIDE-READS

## S1. Harvesters BUILT per game (our side) — SK_ORE_SENSE worked

Counted from `builderBuild`(16) events resolved to the `placeEntity`(1) they cause.

| map | v600 | v601 A | v601 B |
|---|---|---|---|
| auroraveil | 6 | 8 | 2 |
| bifrost | 2 | 1 | 1 |
| **fimbulwinter** | **0** | 7 | 5 |
| glacierkeep | 2 | 4 | 3 |
| helheim | 2 | 3 | 2 |
| **holmgang** | **0** | 2 | 2 |
| icefloe | 22 | 2 | 2 |
| **jotunheim** | **0** | 2 | 2 |
| **longhouse** | **0** | 2 | 2 |
| midgard | 9 | 5 | 5 |
| **paths** | **0** | 1 | 1 |
| skald | 2 | 6 | 2 |
| **stavkirke** | **0** | 2 | **0** |
| valkyrie | 2 | 2 | 3 |
| **yggdrasil** | **0** | 2 | 4 |
| **total (15 games)** | **47** (mean 3.1) | **49** (mean 3.3) | **36** (mean 2.4) |
| **ZERO-harvester games** | **7 / 15** | **0 / 15** | **1 / 15** |

**Zero-harvester games: 7/15 → 0/15 (seat A), 1/15 (seat B).** The one remaining is
**stavkirke seat B** — see S2. This corroborates the build report's "5/6 → 0/6" on the
6-game aliveness set, on a wider 15-map denominator.
Note also `icefloe` v600's 22 harvesters built with **0 alive at the end** — rebuild churn
that v601 does not repeat (2 built, 0 alive).

## S2. stavkirke seat A parking — RESOLVED; a new seat-B pathology in its place

The v601 build report's residual #3 was "stavkirke keeper wall-pocket parking". Measured
as tile-occupancy concentration over each builder's whole life:

| game | builder (inferred role) | rounds | distinct tiles | **top-2-tile share** | builds |
|---|---|---|---|---|---|
| stavkirke v600 (r174) | id3 HOME KEEPER | 174 | 18 | **78%** — 2-tile shuttle (11,5)↔(11,4) | 1 (a gunner) |
| stavkirke v600 | id45 SIEGE (respawn) | 118 | **1** | **100%** — genuinely frozen on (8,2), 0 moves, 0 actions | 0 |
| **stavkirke v601 A (r109)** | **id3 HOME KEEPER** | 109 | **26** | **44%** | **13** (2 harvesters, 9 conveyors, 2 gunners) |
| stavkirke v601 B (r1000) | id4 HOME KEEPER | 1000 | 10 | **99%** — (15,15)↔(16,15) for 991 rounds | **0** |
| stavkirke v601 B | id9 ORE DENIER | 998 | 15 | **96%** | 0 |
| stavkirke v601 B | id12 SIEGE | 997 | 18 | **94%** | 0 |
| stavkirke v601 B | id6 CAGE WALKER | 999 | 27 | 68% | 0 |

**Seat A: fixed.** The keeper's top-2-tile share drops 78% → 44%, its build count goes
1 → 13, and stavkirke's harvester count goes 0 → 2.

⚠ **Seat B: a full-roster stall that tape30 could not have seen** (tape30 is seat A only,
so this is an observation, not a regression measurement). All four builders spend
68-99% of a 1000-round game oscillating between two adjacent tiles, building **nothing**:
0 harvesters, 0 conveyors, 0 barriers. We "won" it on `titanium_stored` at r1000 — i.e.
on passive income alone — which `R1000_IS_DEFEAT` scores as a defeat.

**The same two-tile oscillation is what the cage walker falls into after its give-up latch
fires** (glacierkeep v601A r70-90, §1.5). This looks like one shared navigation defect in
`step_to`/`_bfs_direction`, not two, and it is worth a v602 item of its own.

---

# Q2 — the 42-builder respawn storm (`fimbulwinter_A`)

Decoded with `scratchpad/s54_autopsy/tape30_deaths.py` (the validated attribution
decoder). **Self-check: 0 mismatches / 44 checked on this game; 0 mismatches / 251
checked across all 30 tape601 game-sides.** Working scripts: `storm.py`, `storm2.py`,
`storm3.py`, `storm4.py`, `storm5.py` in this scratchpad.

## 2.1 The loop signature — a period-25 cycle, 34 identical walks

| | measurement |
|---|---|
| bodies | 42 spawned, **39 died**, 3 survived to r1000 (ids 8, 11, 123) |
| lifespan | **median 22 rounds** (mean 25.1, min 19, max 93) |
| spawn tile | **(2,0) × 38**, (3,0) × 2, (1,2) × 2 — effectively one tile |
| **death tile** | **(7,6) × 39 = 100.0%** |
| distance of the death tile | d² **32** from OUR core footprint; d² **202** from the enemy's — it dies in our own half |
| path identity | **only 8 distinct position tracks among 42 bodies; the modal track is shared by 34 of 42** and is 22 tiles long |
| inter-spawn interval | **33 of 41 gaps are exactly 25 rounds** |
| death → next spawn | **36 of 38 are exactly 3 rounds** (= `SK_BEAT_STALE`) |
| period arithmetic | 3 (respawn) + 12 (walk-out) + 10 (six gunner shots at reload 2) = **25** |

`spawn (2,0) → 12-round greedy walk → lock into a 2-cycle (6,6)↔(7,6) → absorb 7 damage
every other round → die at 6 shots (42 ≥ 40 HP) → respawn 3 rounds later → repeat.`

## 2.2 What killed them — one gunner, never touched

**Enemy GUNNER `id 65`, team 1, at `(8,7)`, born r43, alive at r1000.**
* **39 of 39 builder deaths (100%)**, and **234 of 234** damage events landed on our
  builder bots in the whole match.
* It fired **255 times** from that tile. The only other enemy turret to fire was gunner
  `id 67` @ (9,8), 9 shots, none hitting a builder.
* **We inflicted 0 damage events on id 65 in 1000 rounds.**
* Its NW ray at r²≤13 covers exactly `(7,6)` (d²=2) and `(6,5)` (d²=8); the observed
  hit-tile histogram is `{(7,6): 198, (6,5): 36}` and nothing else — the ray model
  reproduces the wire.
* Our own two forward gunners (`id 89` @(11,6) r65, dead r72; `id 91` @(10,5) r66, alive
  to r1000) fired **0 shots all game** while holding 14 banked ammo.

**Non-damage removals: 0 of 39** — every death carries an attributed damage source whose
total equals that round's negative HP delta. Population control: **0 non-damage removals
across all 30 tape601 game-sides.** The engine's exception-destroy channel never fired;
our own code did not crash a single unit.

## 2.3 What the core kept doing — solvent, and bleeding scale

* `coreConvertAmmo`: **ours 1 call / 14 Ti for 1000 rounds**; the enemy's 249 calls / 1,208 Ti.
* Our `placeEntity` by kind: `builder_bot 42, harvester 7, conveyor 12, gunner 2`.
* **Cost scale reconstructed from the build/destroy history: 100% → 219%.** Builder-bot
  cost climbs 30 → 36 → 42 → 48 → 65 and then sits at **65 Ti** for every replacement
  from r81 on.
* **Total Ti on builder bots = 2,626** (reconstructed, not a bound; the base-cost lower
  bound would be 1,260). All builds = 3,062.
* **Ledger closes exactly**: income `500 + 2,500 passive + 4,930 delivered = 7,930`;
  spend `3,062 builds + 1,772 pecks (886 × 2) + 21 heals + 14 ammo = 4,869`;
  `7,930 − 4,869 = 3,061` = the observed final `Player.titanium`. Same closure on seat B.
* **The core was never broke**: Ti minimum 282, **0 of 1000 rounds below 30 Ti**, final
  bank 3,061. **The storm's cost is opportunity and SCALE, not solvency** — 2,626 Ti burnt
  and a permanent ×2.19 on every other build. Seat B, same bot, same map: 4 builders,
  156 Ti on bodies, **5,591 Ti banked** on essentially identical collection (4,940 vs 4,930).

## 2.4 Map and loop geometry

**fimbulwinter is 20×20; our core (2,1) NW, enemy core (16,17) SE, reflection-symmetric.**
A wall pair at `(6,7),(7,7)` / `(6,8),(7,8)` sits directly south of the corridor;
`(3,5),(4,5),(3,6),(4,6)` wall the west and `(7,3),(8,3),(7,4),(8,4)` the north, so rows
5-6 between x=5 and x=9 form a narrow east-west throat with the centre ore pair at
`(9,6),(10,6)`. The enemy dropped gunner id 65 at **(8,7)** at r43, tucked *behind* the
wall pair, facing NORTHWEST; its two-tile ray `(7,6),(6,5)` covers the throat's western
mouth and nothing else. Our walker's greedy line runs `(2,0)…(5,4)→(5,5)→(6,5)→(6,6)→(7,6)`
— straight through both ray tiles — and then locks into a 2-cycle between `(6,6)` and
`(7,6)` because `(7,6)`'s south neighbour is the wall at `(7,7)`. The gunner is *diagonally*
adjacent to the trap tile (d²=2), i.e. inside the wall shadow, so a builder on `(7,6)`
cannot reach it orthogonally, and our own conveyors at `(7,5),(8,5),(9,5)` plus our
harvester at `(9,6)` seal the only bypass.

## 2.5 Code-level cause — a navigation 2-cycle, repeated by the role re-claim

**The trap (H4, the thing the data separates):**

1. `known_map_for(w,h,own,ct)` (`bots/_v601skalman/sk_maps.py:495-506`) returns **None** on
   fimbulwinter — the candidate filter yields **0 catalogue candidates** for (20×20, core
   (2,1)). `self.map_grid` stays `None` all game.
2. `_bfs_direction` therefore never floods: `bots/_v601skalman/sk_common.py:348` —
   `if self.map_grid is None: return p.cardinal_direction_to(target)`. **Navigation
   degrades to pure greedy with no wall knowledge, every call, all game.**
3. The walker's target is the nearest empty enemy-ring seal tile by d²
   (`sk_roles.py:1564-1574`) — from both (6,6) and (7,6) that is **(16,16)**.
4. `Position.cardinal_direction_to` breaks ties **horizontally**. Verified against the
   installed engine: from **(6,6)**→(16,16) Δ=(+10,+10), exact tie → **EAST** → (7,6);
   from **(7,6)**→(16,16) Δ=(+9,+10) → **SOUTH** → `(7,7)` is a WALL → `can_move` False.
5. `_nav`'s fallback (`sk_common.py:513-514`) for `idx = SOUTH` is `(WEST, EAST, NORTH)`
   → **WEST back to (6,6)**. **Infinite 2-cycle.**

That chain predicts the observed step pair *uniquely*: targets (16,17) and (15,17) both
yield SOUTH at both tiles, so **(16,16) is the only target consistent with the wire** —
independently confirming the role is CAGE_WALKER without leaning on the H1 simulation.

**H1 — ROLE RE-CLAIM: SUPPORTED, as the repeater.** `_claim_role` (`sk_roles.py:158-183`)
takes the lowest role id whose beat is stale; the core's `_spawn_plan`
(`sk_core.py:187-227`) spawns whenever `live + in_flight < 4`, with **no death-rate memory
and no cap other than `get_unit_count() >= 50`**. So the CAGE_WALKER slot is re-staffed 3
rounds after every death, forever. Simulating the claim rule (**HEURISTIC**) puts **38 of
39 deaths in role 1 = CAGE_WALKER**; HOME_KEEPER takes 2 bodies (1 death), ORE_DENIER and
SIEGE_ENGINEER 1 each, both surviving 996-997 rounds.

**H2 — SPAWN PLACEMENT: REFUTED.** Spawn tile (2,0) received **0 of 234** hits; minimum
lifespan is **19 rounds** (no 0-2-round body); spawn tile ≠ death tile in 39/39. The bodies
walk 12 rounds before the first hit.

**H3 — HARVESTER/BELT ESCALATION BAN: REFUTED as the cause.** `SK_HARV_ESCALATE`
(`sk_roles.py:771`, `436`, `456`) governs *ore tiles*, and no harvester died here — both
centre harvesters (`id 64` @(10,6) r43, `id 100` @(9,6) r77) were alive at r490. Nothing
escalated, so `_escalate_target` returned early at `sk_roles.py:786` all game.

⭐ **But the gap H3 gestures at is real and is the second-order cause.** `self.armed_memo`
records exactly this gunner's tile — written at `sk_roles.py:239`, keyed on the tile,
precisely so that "the gunner that ate 22 harvesters was planted at r9 and never looked at
again" cannot recur. It has **only two consumers**: `_infer_killer` (`sk_roles.py:470`) and
`_killer_dead` (`sk_roles.py:501`). **Neither `_bfs_direction` nor `_nav` nor `step_to`
ever reads it.** The bot knew where the gunner was from r43 onward, in all 42 bodies, and
walked into its ray every time. **There is no danger-tile term anywhere in the movement
layer.**

**Two latent notes:** `BFS_BLOCKING_TYPES` (`sk_maps.py:158-161`) omits CONVEYOR and
SPLITTER, so when the flood *does* run it treats our own belt as walkable and emits steps
the engine refuses — the identical `_nav` fallback then produces the same 2-cycle. Run on
the reconstructed r490 board, the flood from (7,6) returns NORTH into our own conveyor at
(7,5), the engine refuses, and the fallback again yields WEST — **flood and greedy are
collinear on this tile**; only the `known_map_for` result (0 candidates) separates them,
and it says greedy. Second: `_escape` (`sk_roles.py:275`) only fires at
`free_neighbours == 0`, and (7,6) has two, so nothing ever notices the body is stuck.

## 2.6 Why seat A stormed and seat B did not

**The 2-cycle is not the storm; it is endemic on both seats.** Share of builder steps that
revisit the tile two back: **fimbulwinter_A 2,332/2,867 = 81.3%**, **fimbulwinter_B
2,943/3,005 = 97.9%**, v600 `fimbulwinter_s11` side 0 **427/469 = 91.0%**, side 1
**352/484 = 72.7%**. Seat B's four builders oscillated *harder* and all four survived to
r1000 — their terminal 2-cycles sit on `(14,13)↔(14,14)`, `(10,11)↔(11,11)`,
`(14,18)↔(15,18)`, tiles no enemy turret covers.

**The whole difference is opponent turret siting**, which is not mirror-symmetric because
the opponent's own behaviour differs by seat: on seat A it planted gunners at (8,7) r43
and (9,8) r44 plus a sentinel at (13,15) r111 and fired **264 shots**; on seat B it planted
four launchers and one sentinel at (5,4) on its own doorstep and fired **0 `fireTurret`
events in 1000 rounds**. Zero shots ⇒ **0 damage events on our builders on seat B vs 234
on seat A**, so the same infinite loop cost 0 bodies instead of 39.

The v600 control (`fimbulwinter_s11`, side 0, r138) is a *different* refutation: v600 also
lost 0/4 builders (0 damage events on builders) because there the opponent's sentinels at
(7,5)/(5,4) shot our belt and core instead and **killed our core at r138** — the game ended
before a storm could develop. **That is a null on duration, not evidence that v600 lacks
the bug**: its own oscillation rate is 91.0%.

## 2.7 It is not a fimbulwinter singularity

Across all 30 tape601 game-sides, builders spawned: **median 4.0, mean 6.3, min 4, max 42**.
Only three game-sides exceed 8, and **all three are the same bug class**:

| game-side | builders | deaths | single killer | death-tile pooling | oscillation rate |
|---|---|---|---|---|---|
| fimbulwinter_A | 42 | 39 | gunner @ (8,7) | (7,6) × 39 | 81.3% |
| holmgang_A | 13 | 10 of 12 | one enemy sentinel @ (8,7) | (4,3) × 6, (7,6) × 4 | 75.4% |
| paths_B | 13 | 9 of 9 | one enemy sentinel @ (2,14) | (2,9) × 7, (2,10) × 2 | 37.4% |

⭐ **The same 2-cycle is what §1.5's cage walker falls into on glacierkeep after its
give-up latch fires (r70-90, `(14,25)↔(14,24)`), and what all four stavkirke seat-B
builders sit in for 1000 rounds (§S2, top-2-tile share 94-99%, measured independently
here). One navigation defect, three symptoms: the barrier collapse's tail, the stavkirke
build-nothing stall, and the respawn storm.**

⚠ **Population caveat.** All 30 replays are local arena games against one `_v542wave` copy
with NOISE forced off (`scratchpad/s54_fidtape/mkfixture.sh`) — a fixture we authored, one
opponent, deterministic. Under `FIXTURE_OF_RECORD` this **prioritises** the fix; it does
not establish field prevalence.

---

# WHAT A v602 WOULD FIX, RANKED BY MEASURED COST

1. **Gate `_peck_priority` inside `_cage_walker` (`sk_roles.py:1534`)** so it cannot steal
   the lap advance while seal tiles are still open. Cost of not fixing: −60% ring barriers
   per game, ring share 72.5% → 50/56.5%, worst-case 41 consecutive parked rounds.
2. **Add a danger-tile term to the movement layer.** `self.armed_memo` (written
   `sk_roles.py:239`) already holds every seen enemy turret tile and **no mover reads it**.
   Cost of not fixing: 39 builder deaths, 2,626 Ti and +119pp of cost scale in one game;
   3 of 30 game-sides affected.
3. **Break the `cardinal_direction_to` 2-cycle** — `_nav`'s fallback (`sk_common.py:513`)
   needs a no-immediate-backtrack rule, or `_escape` (`sk_roles.py:275`) needs a
   "same two tiles for N rounds" trigger instead of only `free_neighbours == 0`.
   Cost of not fixing: 72.7-97.9% of all builder steps are 2-cycles; stavkirke seat B
   built nothing in 1000 rounds.
4. **Make `_enemy_builder_adjacent` (`sk_roles.py:1398`) footprint-aware** so the
   healing-race guard sees a 2×2 core. Cost of not fixing: 41 rounds pecking a core being
   healed +6..+8/round against our +2 (§1.8).
5. **`known_map_for` returns None on fimbulwinter** (0 catalogue candidates for 20×20 /
   core (2,1)) — the same root-cause family as the `SK_ORE_SENSE` bugfix, now shown to
   disable BFS navigation as well as ore sensing. This is the shared upstream of items 2-3.
