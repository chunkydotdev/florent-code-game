# INCREMENTAL MOVE-MINING STUDY — 0033 v57, second pass (NEW30 window)

**BANKED by research s50, 2026-08-17 ~17:5xZ.** Agent report verbatim below, with two banking annotations by the banking lane (marked ⟦BANKING⟧). Anchors `raid.py:1009`+`raid.py:995-1000` (Piece A), `main.py:585-591`+`eco.py:458` (Piece C), `eco.py:1689` (Piece B) and the ledger's existence were **opened and verified by the banking lane** before commit; all other anchors are the agent's own (playbook-discipline, MEASURED-labelled).

⟦BANKING correction to §6⟧: `docs/research/move-mining-ledger.tsv` EXISTS (header + 4 rows); the agent's "does not yet exist" is false. Row appended in this commit.
⟦BANKING note⟧: per Magnus's s50 one-plank directive (ferry-siege), NO new queue rows are stocked from this study today. Piece A is filed as evidence-for-`#93` (already on the Magnus-approved list); Pieces B(defensive half)/C(ordering swap)/D(bait placement, `#31` family)/F(`#75` team check) are candidate rows deferred to admission after the directive lifts.

---
# INCREMENTAL MOVE-MINING STUDY — 0033 v57, second pass

## 1. PROVENANCE

**agent** = opus subagent, s50 (fresh session, no inherited context).

**Inputs, verbatim as named:** `docs/research/PLAYBOOK-move-mining-2026-08-16.md` · `docs/research/REPLAY-STUDY-0033-2026-08-16.md` (exclusion baseline) · `QUEUE.md` · `corpus/join.tsv`, `corpus/meta_join.tsv`, `corpus/ladder_games.tsv`, `corpus/version_trees.tsv`, `replay_archive/` · `tools/replay_schema.md`, `tools/replay_census.py` · `bots/_v488beltbreak2/`, `bots/_v468kladturbo/` (read-only).

**Decoder.** Full event-stream walker on `replay_census` primitives (scratchpad `walk.py`). Two nesting bugs found and fixed against the schema (`PlaceEntity{Entity entity=1}` and `UpdatePlayers{Players players=1}` each carry an extra level the flat decode skips — a decoder that misses them yields a clean, confident zero on every build and every heal). **Validated: `core_deliv × 10 == titaniumCollected` on 60 of 60 team-sides, 0 mismatches**, on the ground set itself.

**GROUND.** `corpus/join.tsv`: 210 archived games vs 0033, 90 at their v57. Prior study committed `93c8ed81` 2026-08-16T15:15:26Z; exactly 60 v57 games precede its input boundary (matching its own "last 60 games").

| window | n | matches | ourver | completedAt range | our game share |
|---|---|---|---|---|---|
| **PRIOR60** | 60 | 12 | 139(5), 151(5), 152(45), 153(5) | 08-14 → 08-16T13:35Z | **17-43 (28.3%)** |
| **NEW30** | **30** | **6** | **155 (25), 157 (5)** | 08-16T20:16Z → 08-17T11:17Z | **14-16 (46.7%)** |

New-window match ids: `b4bd82a1`, `20f922f7`, `8d26d1c4`, `cda1b60d`, `66ee570e`, `ed6ebb2c` (full ids in join.tsv). All ladder. Win conds: 28 core_destroyed, 2 titanium_collected (prior 58/2).

⚠ **INSTRUMENT ALARM ON THE GROUND SET:** ourver **155 = `_v468kladturbo`** (ours); ourver **157 = `_x3r0v157odin`** — a TEAMMATE tree. Five of 30 games are Odin and Odin dominates several pooled cells (builder attacks on 0033 sentinels: 0.00/game at v155 vs 143.40/game at v157). **Every our-side number is v155-only (25 games) unless stated; 0033-side numbers pool.** The incumbent `_v488beltbreak2` (v158/159) has **ZERO games vs 0033** — every compatibility sketch is a GREP, never a measurement.

Minor discrepancy, not load-bearing: prior report quotes 30.0% for its 60 games; join.tsv.won reads 17/60 = 28.3%.

## 2. WHAT CHANGED vs THE PRIOR STUDY

**⭐ THE HEADLINE: WE STARTED WINNING THIS MATCHUP AND STOPPED KILLING IN IT. THE GAIN IS OFF-CURRENCY.**

| | PRIOR60 | NEW30 | NEW25 (v155 only) |
|---|---|---|---|
| our game share | 28.3% | **46.7%** | 48.0% |
| mean game length | 266 | **369** | **377** |
| median round their core died | **144** (n=17) | **316** (n=14) | **341** (n=12) |
| timely-kill rate (our core-kill by r300, ITT) | **16/60 = 26.7%** | 6/30 = 20.0% | 5/25 = 20.0% |
| our core dead by r300 | 50.0% | 30.0% | 32.0% |
| r1000 games | 3.3% | 6.7% | 8.0% |

⇒ **The `DEFENCE_ADMISSION_BAR` gross backstop is TRIPPED against this opponent: median kill round crossed 300 (144 → 316/341).** The timely-kill fall (26.7→20.0) is NOT excluded (±22.0pp, DEFF 1.366); the +18.4pp share gain equally inside noise (±24.3pp). The median move (144→341) is the number the programme names. **We bought this matchup by out-lasting, not by killing.**

**⭐ WE LOST FIRST BLOOD.** PRIOR60: their core first damaged median r23, ours r68 (the prior study's 37-round head start reproduced). NEW30: theirs r52 (r48 at v155), q75 blown out r42→r215/273; ours r58. The head start is down to 6-17 rounds and the tail is gone.

**Our economy roughly doubled** (v155 vs prior): conveyors 27.6→44.8/game, deliveries 89.7→176.4 stacks/game, harvesters 5.15→7.60. Per-round: us 0.337→0.467 stacks, them 0.797→0.682. **Economy is instrumental — this is the whole gain, and it bought survival, not a kill.**

**0033 ITSELF BARELY DRIFTED** (same version, numbers stable: forward-turret death 22.5→23.9%, mix 3.83:2.10, heal allocation/ammo/plug stable). Two movements only: barriers 10.13→15.83/game (+20% length-adjusted), gunner rotations 7.47→4.90. **The matchup changed because WE changed.**

## 3. NEW PIECES

### PIECE A — THE POINT-BLANK GUNNER COLLAR — MEASURED, pooled 90 games

**174 of 0033's 313 gunners (55.6%) planted within core-firing range of our core (d²≤13). 2 of our 85 (2.4%) within range of theirs.** Their gunners: **4,661 hits on our core (32,627 dmg)**; ours: **0 hits on their core out of 3,999 gunner damage events, all 90 games.**

**Control 1 (driven both ways):** the same channel resolves gunner→core 4,661 times on our side — not decoder blindness. **Control 2 (sentinel, runs the right way):** 163/250 of our sentinels (65.2%) ARE inside their core's d²≤32; our sentinels land 40.7 core hits/game. **Gunner-specific siting**, not general forwardness: median d² to enemy core — their gunners 16, ours 484.

**Outcome association with reverse-causation control** (exposure measured by r100, outcome at end): in-range 0033 gunner by r100 → we win **4/31 (12.9%)**, none by r100 → **27/59 (45.8%)**; length-matched (≥r200): **0/11 vs 15/37**. 32.9pp ±24.1pp (DEFF 1.366) — excludes zero. Residual confound retained: a game going badly by r100 may be what lets them plant. **We planted an in-range gunner by r100 in 1 of 90 games.**

**Anchors:** `20f922f7…_game_1` (fjordgate, r1000, LOSS, v155): 0033 gunner #102 at (4,1), d²=2, built r55, NEVER destroyed, **661 shots into our core (4,627 dmg) over 945 rounds**. `cda1b60d…_game_3` (frostgate, r310, LOSS): gunners #192/240/454, none destroyed, 168 core hits. `66ee570e…_game_3` (fjordgate, v157): gunner #40 built **r13 at d²=1**.

**COMPAT (<r300 kill):** directly on-currency. **ADJACENT TO `#93`, not new as a row** — new content: the 55.6-vs-2.4 siting split w/ sentinel control, the r100-exposure cut, the 0-of-3,999. **GREP vs incumbent:** `build_gunner` has TWO call sites — `main.py:754` (counter-battery) and **`raid.py:1009` (BELTBREAK forward gunner, new since v155)**. The value ladder is `harvester (100) over belt (40)` with **NO CORE TERM** (`raid.py:995-1000` comment rejects the core option). ⇒ **The plank is a value-ladder term, not new machinery.** In `_v468kladturbo` (the tree measured) the forward site does not exist (one site, main.py:708).

### PIECE B — THE HARVESTER TAP: 0033 RUNS `#37` AGAINST US; WE HAVE NO DEFENSIVE HALF — MEASURED, pooled 90

**94 of our 528 harvesters (17.8%) orthogonally adjacent to a live 0033 acceptor; 18 of their 678 (2.7%) the other way.** Stacks our harvester → their belt: **1,129 (11,290 Ti) vs 53 the other way — 21.3:1.** Tripled between windows: 7.77 → **22.52 stacks/game at v155**. Concentrated: median 0-1, 15/30 games leak nothing, top game 244.

**Control 1 (deliberateness):** 106/130 adjacency pairs (81.5%) had the 0033 piece built AFTER our harvester, median +127 rounds; their side 14/25 (56%), median +48 — coin flip. **Control 2 (alternative REFUTED):** our harvesters are LESS forward (10.6% vs 16.1% closer-to-enemy-core; median d² 232 vs 185). **Their belt reaches out to our ore.** Mechanism: 42/43 tapped harvesters had ≥1 friendly acceptor — round-robin SPLIT, matching the engine fact.

**Anchor (most expensive tile in the corpus):** `20f922f7…_game_1` (fjordgate, r1000, lost on `titanium_collected`): our harvester (8,1) r17, their conveyor (8,2) r11 — built SIX ROUNDS BEFORE our harvester. **244 stacks = 2,440 Ti into 0033's network. Final: us 240, 0033 2,740 — 89.1% of their scoring total came from our harvester, and that key decided the game.** Also `b4bd82a1…_game_3`: 191 stacks, four harvesters tapped.

**COMPAT:** economy-channel, instrumental — but also a `titanium_collected` transfer, and one game died there. **GREP vs incumbent:** `can_build_harvester` has ONE call site (`eco.py:1689`, `_expand`) — first legal ore tile, filtered only by `_seat_ban` (protects OUR heal seats). **No enemy-belt-adjacency term in either tree.** Cheap plank: deprioritise ore seats with adjacent enemy acceptors when an alternative exists. **The offensive mirror is `#37`; this is its unqueued defensive half.**

### PIECE C — BELT TRIAGE BY HEAL: THEY REPLACE 55% OF BELT DAMAGE, WE REPLACE 14% — MEASURED, both windows

Clamp-aware (summed UpdateHp deltas):

| conveyors/game | ours (v155) | 0033 (v155) | ours (PRIOR) | 0033 (PRIOR) |
|---|---|---|---|---|
| damage taken | 399.7 | 142.3 | 283.3 | 138.2 |
| **HP healed back** | **56.1 (14.0%)** | **78.7 (55.3%)** | 36.7 (12.9%) | 81.6 (59.1%) |
| destroyed | 14.64 | 3.64 | 10.43 | 3.38 |
| dmg absorbed per death | 27.3 HP (1.37×20) | **39.1 (1.95×)** | — | — |

**Our belt dies at the no-heal arithmetic; theirs absorbs ~2× its pool.** **Control (direction REVERSES by asset class — allocation, not "they heal more"):** they heal LESS in total (771 vs 1,333 HP/game); on the CORE we replace 82.0%, they 62.6%. Shares (v155): ours core 80.1%/belt 4.2%; theirs core 59.5%/belt 10.2%. Replicated in PRIOR60.

**Anchors:** `b4bd82a1…_game_3` 141 0033 conveyor-heals; `8d26d1c4…_game_3` 103 in 219 rounds; `66ee570e…_game_4` 101.

**COMPAT:** uptime plank (belt uptime = the ammo the turrets fire; our belt dies 4.0:1). **GREP names the mechanism:** `main.py:585-591` universal-adjacent-heal short-circuits into `_heal_core` unconditionally (`eco.py:458`); `_heal_adjacent` (`eco.py:468`) is purely opportunistic, no dispatch. **That IS the 80.1/4.2 split in code.** Adjacent to `#52` (barrier-scoped) and `#88` (rebuild-scoped) — neither covers belt healing. Smallest form: let `_heal_adjacent` win over `_heal_core` when core above an HP floor and adjacent belt damaged. One ordering swap.

### PIECE D — THE BARRIER PECK SINK: 30% OF THEIR MELEE ON OUR ROCKS AT ~172 Ti/KILL — MEASURED, 30 games

**29.9% of 0033's builder attacks (65.6/game at v155) land on our barriers.** NEW30 pooled: 1,808 pecks = 3,616 Ti, killing **21 of 201 barriers ≈ 172 Ti per 3-Ti barrier.** We answer 2,022 heals; net **+1,594 Ti over 30 games** before counting their 1,808 burned builder-turns. **Control (same weapon, different target):** their pecks on our conveyors: 18.7 Ti per kill — **9.2× more efficient on belt than barriers.** **Anchors:** `20f922f7…_game_1`: 836 pecks vs 5 barriers, 0 killed; `cda1b60d…_game_1`: 353 pecks, 0/10; `cda1b60d…_game_3`: 218, 1/7.

**COMPAT:** a piece we already win — `DEFENCE_ADMISSION_BAR`-clean. Buildable form is NOT volume (`#31c` weakest; sporks tops ladder on 3.02 barriers/game) but **bait placement** — where a barrier maximises peck-attraction per Ti. **`#31` family member, not a separate row.**

### PIECE E — 0033 RUNS ZERO AMMO BUFFER, HAND-TO-MOUTH — MEASURED, 90 games; REFUTES the prior kill-path attribution

| | mean ammo | rounds below 10 | rounds below 4 |
|---|---|---|---|
| us | 26.0-29.4 | 20.6-25.7% | 12.5-13.5% |
| **0033** | **6.7-8.2** | **66.9-71.7%** | **49.0-51.7%** |

Closed-arithmetic control (engine ammo law 4g+10s): their conversions 962.33 Ti/game vs 957.1 spent — residual 0.5%; ours 3.8%. **Both convert what they fire; they carry no float, we carry ~26.**

⇒ **REFUTATION of the prior study's "Ours: arrive first, then run out of ammo."** If either team is ammo-thin it is 0033 — below a gunner shot half of every game, yet firing 153.7 shots/game to our 114.0. The middle clause ("let one healed forward gunner grind") survives — Piece A measures it at 661 shots. **The mechanism was right; the ammo attribution was not.** (Refutes an attribution, not the fire-event evidence.)

**COMPAT:** kills a false lever — "more ammo" planks vs 0033 aim at a non-binding constraint.

### PIECE F — WE POINT CONVEYORS INTO THEIR NETWORK — MEASURED but SMALL; control DOWNGRADES to mutual defect

119 stacks (1,190 Ti) across 5 of 90 games. **Anchor with facing off the wire:** `ed6ebb2c…_game_3` (valkyrie, r716, WON): our conveyor #450 at (7,20), built r192, facing NORTH into 0033's #254 at (7,19) since r104 — **77 stacks (770 Ti)** until #450 died r483. **Control runs AGAINST a 0033 trick:** static sweep — NEW30: 4/2,056 theirs vs 2/1,342 ours point at enemy tiles; PRIOR60: 2 vs 4. **Symmetric and rare — a link-planner defect on BOTH sides.** Adjacent to `#75`: same call site, one `get_team` check.

## 4. REFUTED MECHANISMS — RETAINED

1. **Barrier armour does not protect turrets — extended to THEIR turrets:** armoured die 23.9% vs bare 15.9% (n=184/328) — selection, not protection. Same direction our side. (Does not touch `#41` — siting, not survival.)
2. **"We run out of ammo vs 0033"** — refuted (Piece E).
3. **"Harvesters tapped because we site forward"** — refuted (Piece B control 2).
4. **"Our conveyors feed theirs because 0033 farms the belt"** — refuted (Piece F control): symmetric mutual defect.
5. **SCOPING CORRECTION:** the prior report's "34.1% of our gunner shots end on enemy barriers" is the 180-game all-era pool; **vs 0033 v57 specifically it is 88.1%** (3,524/3,999; 85.1% prior window, 91.4% new — stable, not drift). Carrying 34.1% into a v57 plank understates the leak 2.6×.
6. Retained unchallenged: facing-geometry line-of-fire refutation; core-chew historical — **zero builder attacks on either core in all 90 games.**

## 5. CONFIRMATIONS (no new rows; trigger should not re-fire)

Forward-turret survival reproduced (theirs die 22.5→23.9%, ours 53→49%; prior 25/48). Belt-fire ratio holds 3.1:1→4.0:1. Counter-battery: ours 4.9% unchanged; theirs onto our turrets fell 19.0→13.8% (moved onto our core — Piece A). Known: mix (`#21`), forward siting (`#23`), plugs (`#31a`), 0 launchers/splitters in 90 games.

## 6. LEDGER ROW

```
2026-08-17	0033	57	30	docs/research/REPLAY-STUDY-0033-INCREMENTAL-2026-08-17.md
```
Coverage now 90/90 v57 games; trigger should not re-fire on 0033 until v58+.

## 7. THE ONE THING FOR MAGNUS

**We are 46.7% against our most-played opponent and our median kill against them moved from r144 to r341** — a defence-shaped gain on a matchup the programme says to win by killing; the gross backstop is tripped. Shortest path back to the kill currency: **Piece A** — they plant a core-range gunner in 56% of gunner builds, we did it once in ninety games; when they get one down by r100 we win 4/31 (0/11 past r200). The incumbent already has the forward-gunner machinery (`raid.py:1009`); its value ladder has **no core term. That is a constant, not a build.**
