# AUTOPSY — v174's two 1-4 losses (kladde v168, team lazy v253), 2026-08-21

## Provenance

| field | value |
|---|---|
| written | 2026-08-21T08:01:36Z (`date -u`, same shell) |
| repo HEAD at write time | `4a7ef651e` |
| lane | research / autopsy agent, DECODE-ONLY (no bot edits, no arena, no submissions) |
| our bot | v174 "Baltsars banditer v1" = `bots/_v537socket` (read-only) |
| matches | `d4566d49-803c-4c6a-bfb4-d4683e177257` vs **kladde chatte tville (och oss)** v168, rated ladder, created 2026-08-21T06:52:59.688Z, **1-4**, eloDelta **−9.977**, we are **seat A** all 5 games<br>`097976e0-117b-4b76-8604-7f59c6812698` vs **team lazy** v253, rated ladder, created 2026-08-21T07:12:59.754Z, **1-4**, eloDelta **−12.343**, we are **seat B** all 5 games |
| extra games pulled for §4 | `717140d8…_game_5` (frostgate vs farming_200s v19), `9d2247c3…_game_5` (frostgate vs Juusto v13) — both from the same v174 25-game field-debut set |
| instruments | `tools/corpus/replay_autopsy.py` (unmodified, used as the cross-check) + a decode-only extension built on `tools/replay_census.py` primitives (session scratchpad `reel.py` — **not** committed; it is a throwaway, every number below is reproducible from the two tools named) |
| instrument cross-check | `replay_autopsy.py`'s self-checking core-damage ledger reports **MATCH** on every game read; the extension reproduces its `sentinel 612` figure on kladde g1 digit-for-digit before any other number here was trusted |
| corpus maps/results | `corpus/ladder_games.tsv` (rated authority), `corpus/meta_join.tsv` for `us_side` on the two extra frostgate games |
| discipline | every number is MEASURED off the replay wire unless marked **INFERENCE** (counterfactual) or **EYEBALL** |

**Extends, does not re-derive:** `docs/research/FIELD-DEBUT-v174-2026-08-21.md`,
`docs/research/REPLAY-STUDY-kladde-multiver-2026-08-20.md` (+ its 2 amendments),
`docs/research/REPLAY-STUDY-teamlazy-v253-2026-08-20.md`,
`docs/research/DECODE-launch-timing-v174-2026-08-21.md`.

---

## 0. THE ONE-PARAGRAPH ANSWER

We did not lose these ten games to one thing. We lost them to a **chain**, and every
link is visible on the replay:

> **Their sentinel goes up beside our core at r7–r24 and never stops firing** →
> **our belt's throat is cut or plugged at r38–r86 and our titanium income freezes for
> the rest of the game** (median holding after r50 across the 10 losses: **10–46 Ti**) →
> **we can no longer afford a siege sentinel** — in **4 of the 8 match losses we never build
> one at all**, and in **6 of the 10 losses we put ZERO damage into their core** → **the only offence we have left is a builder standing on
> their core's doorstep** → and that builder is forbidden by
> `bots/_v537socket/raid.py:290` (`not LOKI_QUIET_ON`, permanently False) from hitting
> the core, so it stands there — **healthy, executing, 7.6% of CPU budget, for up to 973
> consecutive rounds** — and does nothing.

**Builder-attack damage into the enemy core: 0 HP in 12 of 12 games decoded here.**
**Our builders attack constantly — 556 attacks across the ten match games (356 vs kladde,
200 vs lazy) — and every single one lands on an enemy conveyor, an enemy gunner, or an
empty tile. Never the core.** The verb
is not silent; it is **misdirected**. That is a sharper diagnosis than "the quiet-verb
family silences the verb" and it changes the fix.

And there is a **new, uninvited mechanism** that the banked docs do not contain:
**kladde is running a titanium pump on us** (§5.1).

---

## 1. REEL MANIFEST — read top to bottom

Replay paths are absolute; open with
`.venv/bin/python tools/replay_view.py <path>` (writes an HTML scrubber and prints its path).

| # | match / game | map | res | mechanism in one sentence | anchor rounds | replay path |
|---|---|---|---|---|---|---|
| **1** | kladde g1 | midgard 30×30 | **W** r117 | **CONTRAST — the defect is present in the win too:** bot #3 parks on their core's socket (25,26) for **64 consecutive rounds r53→r116** and spends 51 attacks on the *conveyor* at (25,27), **zero on the core**; we win anyway because three siege sentinels (r71/r82/r91) do all 612 damage. | **r53–r63** (park + first conveyor peck), **r82–r91** (sentinels arrive, damage starts) | `/Users/junghard/Projects/Work/florent-code-game/replay_archive/d4566d49-803c-4c6a-bfb4-d4683e177257_game_1.replay26` |
| **2** | kladde g2 | glacierkeep 30×30 | L r141 | **One sentinel, unopposed:** their sentinel at **(14,6) built r45**, d²=9 from our core, deals **all 864 HP** from r46 to r140 while we build **zero** siege sentinels and put **0 damage** into their core; our last delivery is **r43** and we finish the game on **50 Ti collected vs their 810**. | **r45–r50** (the sentinel goes up, first blood r46), **r12–r41** (our two raiders sit on their sockets for 30 rounds doing nothing), **r140** | `…/replay_archive/d4566d49-803c-4c6a-bfb4-d4683e177257_game_2.replay26` |
| **3** | kladde g3 | frostgate 20×20 | L r360 | **Misdirected verb at maximum dose:** 227 socket unit-rounds, **229 builder attacks, 226 of them into enemy conveyors and 0 into the core**; our single siege sentinel (r67) lands 234 HP and kladde heals **exactly 234** back; their guard sentinel was up at **r8**. | **r9–r15** (raider reaches socket at r9), **r67–r92** (our only damage window, fully healed), **r312–r359** (their (8,10) sentinel, built r312, deletes our core) | `…/replay_archive/d4566d49-803c-4c6a-bfb4-d4683e177257_game_3.replay26` |
| **4** | kladde g4 | auroraveil 20×20 | L r295 | **Barrier tarpit then a firing line:** **62 of our 86 turret shots** go into barriers kladde keeps replanting on tile **(10,3)** beside our core; then at **r269/r273/r275** they plant three sentinels in a row along y=1 at (15,1),(14,1),(13,1) and delete our core in 25 rounds. | **r100–r200** (the tarpit, watch (10,3) blink), **r269–r295** (the three-sentinel firing line) | `…/replay_archive/d4566d49-803c-4c6a-bfb4-d4683e177257_game_4.replay26` |
| **5** | kladde g5 | yulerune 20×20 | L r1000 (titanium) | **⭐ THE TITANIUM PUMP — the game to watch first.** kladde plugs our belt's throat at **(3,8)**, one tile from our core, and **rebuilds a 3-Ti barrier there 119 times between r42 and r962**; our lone sentinel shoots it **236 times — 100% of our turret fire, all game, all on one tile — costing 2,360 ammo, which is exactly the 2,360 Ti we converted.** Our economy dies (**last delivery r38; 130 Ti collected vs their 15,870**), we never build a siege turret, and bot #14 stands on *their* core's socket (17,8) for **973 consecutive rounds r27→r999** doing nothing. Their core finishes **500/500**. | **r38–r42** (our conveyor at (3,8) dies, first barrier lands), **r42–r120** (the pump cycle: build → 2 sentinel shots → rebuild, ~5-round period), **r27–r999** (bot #14 parked, never acts) | `…/replay_archive/d4566d49-803c-4c6a-bfb4-d4683e177257_game_5.replay26` |
| **6** | lazy g1 | royale 20×20 | L r193 | **Point-blank sentinel finishes it:** their sentinel at **(9,1) built r137 — orthogonally adjacent to our core footprint** — does 504 HP from r138 to r192; our belt's last delivery is **r42**; our raider parks at (8,17) r36→r48 and does nothing; **0 damage into their core all game.** | **r24–r35** (their first sentinel at (9,4) opens with 108), **r137–r138** (the point-blank build + first shot), **r36–r48** (our raider idle on their doorstep) | `/Users/junghard/Projects/Work/florent-code-game/replay_archive/097976e0-117b-4b76-8604-7f59c6812698_game_1.replay26` |
| **7** | lazy g2 | nordkap 20×26 | L r425 | **⭐ THE FAMINE GAME. One enemy building beats us alone:** their sentinel at **(11,19), built r158, orthogonally adjacent to our core**, fires from r159 to r423 and deals **2,394 HP — 133 shots, completely unopposed.** We fire **4 turret shots in the entire game** and convert **62 Ti to ammo vs their 2,080**; our titanium_collected freezes at **190 after r86** and our balance sits at a median of **39 Ti** for the rest of the game. **0 damage into their core.** | **r82–r86** (harvester dies, income freezes), **r158–r165** (the sentinel goes up and starts), **r300–r423** (still firing, still nothing answering it) | `…/replay_archive/097976e0-117b-4b76-8604-7f59c6812698_game_2.replay26` |
| **8** | lazy g3 | auroraveil 20×20 | L r1000 (titanium) | **Total economic shutout:** **titanium_collected = 0 over 1,000 rounds** despite 5 harvesters and 54 conveyors built (**31 lost**); we do drive their core down to **200 HP** with a sentinel at (13,6) but they heal **1,480 HP** back to 468; raider #22 reaches their socket (11,2) only at **r795** and then stands there **205 rounds** to the end doing nothing. | **r23–r42** (belt starts being chewed, never recovers), **r573–r800** (our best damage window, out-healed), **r795–r999** (raider parked, core at 468) | `…/replay_archive/097976e0-117b-4b76-8604-7f59c6812698_game_3.replay26` |
| **9** | lazy g4 | ragnarok 30×30 | L r163 | **Point-blank again, earlier:** their sentinel at **(28,26) built r52, orthogonally adjacent to our core footprint**, does 504 HP r53→r162; our first siege sentinel lands only at **r121** (252 HP); our raider doesn't reach d²≤2 until **r25**. | **r52–r55**, **r121–r130**, **r155–r162** | `…/replay_archive/097976e0-117b-4b76-8604-7f59c6812698_game_4.replay26` |
| **10** | lazy g5 | drumlin 25×25 | **W** r278 | **CONTRAST — what a win looks like:** two of our sentinels ((8,7) r105, (7,6) r240) put 504 into their core and finish it; their point-blank sentinel at (19,17) r184 manages only 180 before the game ends. **Same 0 builder damage into their core**, but the turret race went our way. | **r105–r122**, **r240–r277** | `…/replay_archive/097976e0-117b-4b76-8604-7f59c6812698_game_5.replay26` |
| **F1** | farming_200s g5 | frostgate 20×20 | L r109 | **The cleanest single frame in the whole set:** their core has **ZERO defensive turrets for the entire game**, and our bot #11 stands on its socket **(15,9) for 85 consecutive rounds r24→r108** and never touches it — while their sentinel starts eating our core at **r15** and finishes at r109. | **r15** (first blood on us), **r24–r108** (bot #11 parked at (15,9), undefended core one tile away) | `/Users/junghard/Projects/Work/florent-code-game/replay_archive/717140d8-b80b-4177-8bf0-8f12522c9fd3_game_5.replay26` |
| **F2** | Juusto g5 | frostgate 20×20 | L r462 | **446 consecutive rounds parked:** bot #11 holds socket **(15,10) from r16 to r461** — HP 40/40 the whole time, `tled=0`, exec p50 **767 µs of a 10,000 µs budget** — and their core ends **500/500**; we spend the game self-healing our own core (**3,460 HP**) and lose it anyway. | **r16–r21** (park + their first shot on us), **r145–r209** (their launchers keep replanting), **r455–r462** | `/Users/junghard/Projects/Work/florent-code-game/replay_archive/9d2247c3-b20b-46e5-9647-4de218f83109_game_5.replay26` |

---

## 2. THE MEASURED TABLES

### 2.1 Outcome, damage, and the socket ledger (12 games)

`socket-round` = one (round, bot) pair where one of OUR builder bots stood on a tile
**orthogonally adjacent to an enemy core footprint tile** — i.e. a tile from which
`ct.fire(core_tile)` is legal. `actionable` = socket-rounds in which that bot did **not**
move (moving and acting are mutually exclusive for a builder bot, so a moving round was
never available for an attack).

| game | map | res | rounds | dmg INTO their core | dmg INTO our core | socket unit-rounds | actionable | builder atks total | **on their core** |
|---|---|---|---|---|---|---|---|---|---|
| kladde g1 | midgard | W 117 | 117 | 612 (sentinel) | 0 | 157 | 153 | 56 | **0** |
| kladde g2 | glacierkeep | L 141 | 141 | **0** | 864 (sentinel) | 51 | 48 | 16 | **0** |
| kladde g3 | frostgate | L 360 | 360 | 234 (all healed) | 504 | 227 | 150 | 229 | **0** |
| kladde g4 | auroraveil | L 295 | 295 | 54 | 504 | 12 | 4 | 22 | **0** |
| kladde g5 | yulerune | L 1000 | 1000 | **0** | 126 | **1,939** | **1,935** | 33 | **0** |
| lazy g1 | royale | L 193 | 193 | **0** | 612 | 32 | 28 | 27 | **0** |
| lazy g2 | nordkap | L 425 | 425 | **0** | **2,556** | 16 | 7 | 56 | **0** |
| lazy g3 | auroraveil | L 1000 | 1000 | 1,512 | 306 | 205 | 204 | 20 | **0** |
| lazy g4 | ragnarok | L 163 | 163 | 252 | 504 | 8 | 4 | 54 | **0** |
| lazy g5 | drumlin | W 278 | 278 | 504 | 180 | 9 | 4 | 43 | **0** |
| frostgate/farming | frostgate | L 109 | 109 | **0** | 594 | 160 | 158 | 15 | **0** |
| frostgate/Juusto | frostgate | L 462 | 462 | **0** | 3,960 | 448 | 445 | 4 | **0** |

**What our builder attacks actually hit** (pooled over the 10 match games):
`enemy_conveyor` **517**, `enemy_gunner` **12**, empty tile (target already dead) **27**,
**`enemy_core` 0** — 556 total.

### 2.2 The economy clock — this is why we can't buy a weapon

| game | map | res | our Ti collected | their Ti collected | **last delivery to our core** | our Ti held, median after r50 | min after r50 | conveyors built / lost | harvesters built / lost |
|---|---|---|---|---|---|---|---|---|---|
| kladde g1 | midgard | **W** | 1,290 | 640 | **r116** (final round) | **76** | 20 | 24 / 1 | 6 / 0 |
| kladde g2 | glacierkeep | L | 50 | 810 | r43 | 10 | 1 | 12 / 2 | 1 / 0 |
| kladde g3 | frostgate | L | 520 | 3,340 | r78 | 38 | 3 | 16 / **15** | 6 / 2 |
| kladde g4 | auroraveil | L | 580 | 2,030 | r218 | 28 | 0 | 40 / 14 | 7 / 3 |
| kladde g5 | yulerune | L | **130** | **15,870** | **r38** | **12** | 4 | 9 / 1 | 4 / 0 |
| lazy g1 | royale | L | 130 | 1,380 | r42 | 12 | 2 | 11 / 10 | 2 / 2 |
| lazy g2 | nordkap | L | 190 | 3,580 | r86 | 39 | 1 | 28 / **27** | 6 / **6** |
| lazy g3 | auroraveil | L | **0** | 2,070 | **never** | 46 | 2 | 54 / **31** | 5 / 4 |
| lazy g4 | ragnarok | L | 320 | 400 | r77 | 46 | 12 | 23 / 5 | 3 / 0 |
| lazy g5 | drumlin | **W** | 130 | 230 | r35 | **57** | 6 | 8 / 8 | 2 / 2 |

**Read:** in **8 of 8 losses** the last titanium delivery to our core lands between
**r38 and r218** (median **r77**, n=7 — lazy g3 never delivered at all) and the game then
runs on for a median of **216 further rounds** with no income. The two borrowed frostgate
games repeat it: last delivery **r29** (game ran to r109) and **r37** (ran to r462), median
wallet after r50 of **12** and **10** Ti. **10 of 10 losses.** In the one clean win (kladde g1) delivery is still flowing on the
final round. A scaled sentinel costs ≥30 Ti; **the median wallet after r50 in a loss is
10–46 Ti.** We are not choosing not to build a siege turret — we cannot pay for one.

### 2.3 The turret race

| game | their first turret near their core | our first siege sentinel | their killer building (pos, built, damage, window) |
|---|---|---|---|
| kladde g1 **W** | r74 sentinel | **r71 sentinel** | — (they never damaged our core) |
| kladde g2 | **r9 sentinel** | **never** | (14,6) sentinel, built r45 → **864 HP**, r46–r140 |
| kladde g3 | **r8 sentinel** | r67 sentinel | (8,10) sentinel, built r312 → 414 HP, r313–r359 |
| kladde g4 | **r7 sentinel** | r289 sentinel | (15,1)+(14,1)+(13,1), built r269/273/275 → 504 HP, r270–r294 |
| kladde g5 | **r12 sentinel** | **never** | (3,13)/(3,15)/(2,14), built r993–995 → 126 HP |
| lazy g1 | r24 gunner | **never** | (9,1) sentinel, built r137, **adjacent to our core** → 504 HP, r138–r192 |
| lazy g2 | r12 gunner | **never** | (11,19) sentinel, built r158, **adjacent to our core** → **2,394 HP**, r159–r423 |
| lazy g3 | r473 gunner | r128 sentinel | (11,17) sentinel, built r259 → 306 HP |
| lazy g4 | r78 gunner | r121 sentinel | (28,26) sentinel, built r52, **adjacent to our core** → 504 HP, r53–r162 |
| lazy g5 **W** | r16 gunner | **r105 sentinel** | (19,17) sentinel, built r184 → 180 HP (game ended first) |

**kladde's home sentinel is up at r7–r12 in 4 of 5 games** (median r9), reproducing the
banked r11 figure. **Team lazy's kill weapon is a sentinel planted orthogonally adjacent
to our core**, confirmed in 3 of their 4 wins — the banked "point-blank d²=5 forward
sentinel" plank, here at d²=1–5.

---

## 3. §2 OF THE COMMISSION — THE KLADDE CONVERSION WALL, GAME BY GAME

### 3.1 Where the silence binds, and the mechanism is NOT what was banked

The banked reading is *"the LOKI_QUIET_ON family silences the verb"*. Decoded, that is
**half right and the wrong half is the important one**:

* `bots/_v537socket/raid.py:290` — the core-peck branch is
  `if on_seat and ti >= LOKI_PECK_TI_FLOOR and not LOKI_QUIET_ON:`. `LOKI_QUIET_ON = True`
  at `doctrine.py:1687`, unconditionally. **The branch is dead code at runtime.** Same
  gate again at `raid.py:386` on the `_raid_peck` fallback. *(Located by the source-read
  arm of this autopsy; quoted here because the field evidence lands on exactly this line.)*
* **But the attack verb itself is alive.** The conveyor-melee carve-out fires constantly:
  **556 builder attacks across the 10 match games, 517 of them into enemy conveyors.**
  So a raider standing on a socket **is permitted to chew a 20-HP conveyor and forbidden
  to touch the 500-HP core one tile away.**
* **The poverty objection is dead too.** `LOKI_PECK_TI_FLOOR = 4` and a peck costs 2 Ti.
  In kladde g5 — the worst wallet in the set — we held a median of **12 Ti** for 950
  rounds, comfortably above the floor. Money was never the block.

### 3.2 The controls that make the parked-bot claim mean something

For the two longest parks, every alternative explanation was driven to the other verdict:

| control | kladde g5 bot #14 (parked r27→r999) | Juusto frostgate bot #11 (parked r16→r461) |
|---|---|---|
| was it alive? | HP **40/40 in 984 of 984** recorded socket-rounds | alive to r461 |
| was it executing? | `BotOutput` present in **996 of 1000 rounds** | present in **458** rounds |
| did it time out? | **`tled` = 0 of 996** | **`tled` = 0 of 458** |
| was it near budget? | exec p50 **761 µs**, max **1,699 µs** of 10,000 (**7.6% of budget**) | p50 **767 µs**, max 1,092 µs |
| was the verb reachable that game? | yes — same team made **33** builder attacks (all into conveyors) | yes — 4 attacks, all conveyors |
| could it reach the core? | (17,8) → (17,9) is one orthogonal step onto their core footprint | (15,10) → (16,10) likewise |

**A healthy unit, executing every round at 7.6% of its CPU budget, one tile from a core
it is allowed to touch, doing nothing for 973 consecutive rounds.** No other explanation
survives.

### 3.3 Foregone damage and the counterfactual — **INFERENCE**

Rate: **2 damage per attack, one attack per round per bot.** MEASURED, not assumed —
bot #3 in kladde g1 attacks on every consecutive round r55, r56, r57, r58, r59, r60, r61,
r62, r63, so the action cooldown permits a sustained 1/round cadence.

`foregone = 2 × actionable socket-rounds`. Compared against the enemy core's surviving HP
at game end **plus the HP they actually healed onto it** (the reactive-heal term is a
lower bound on their response and is why this is an inference, not a result):

| game | map | res | foregone (HP) | their core end HP | their core healed | damage we did land | **flips?** |
|---|---|---|---|---|---|---|---|
| kladde g1 | midgard | W | 306 | −16 (dead) | 96 | 612 | won already |
| kladde g2 | glacierkeep | L | 96 | 500 | 0 | 0 | **no** (96 ≪ 500) |
| kladde g3 | frostgate | L | 300 | 500 | 234 | 234 | **no** — 234+300 = 534 vs 500+234 healed = 734 |
| kladde g4 | auroraveil | L | 8 | 446 | 0 | 54 | **no** |
| kladde g5 | yulerune | L | **3,870** | **500** | **0** | 0 | **YES — 3,870 vs a 500-HP core that was never healed and never touched. 7.7× the margin.** |
| lazy g1 | royale | L | 56 | 500 | 0 | 0 | **no** |
| lazy g2 | nordkap | L | 14 | 500 | 0 | 0 | **no** |
| lazy g3 | auroraveil | L | 408 | 468 | 1,480 | 1,512 | **no** (1,920 dealt vs 1,980 absorbed — 60 HP short; the closest near-miss in the set) |
| lazy g4 | ragnarok | L | 8 | 372 | 124 | 252 | **no** |
| lazy g5 | drumlin | W | 8 | −4 (dead) | 0 | 504 | won already |
| frostgate/farming | frostgate | L | **316** | **500** | **0** | 0 | **no on arithmetic** (316 < 500) — but see the caveat below |
| frostgate/Juusto | frostgate | L | **890** | **500** | **0** | 0 | **YES — 890 vs an untouched, unhealed 500-HP core.** |

**Counterfactual verdict (INFERENCE, and the honest form of it):**
**2 of the 8 losses in the two matches + extra frostgate games flip on foregone core damage
alone: kladde g5 yulerune and Juusto frostgate g5.** A third (lazy g3 auroraveil) misses by
**60 HP**. The other five do not flip — **because our raider never got enough socket-time
to matter**, not because the verb would have been useless. That is the important asymmetry:
**the games where the parked-bot defect is expensive are exactly the long games we lose slowly,
and those are the games that also breach `R1000_IS_DEFEAT`.**

**Two caveats that pull in opposite directions and must be carried together:**
1. **Pessimistic:** the enemy heals reactively. kladde healed exactly the 234 we dealt in
   frostgate g3, and team lazy healed 1,480 in auroraveil. Adding 2 dmg/round would draw
   more heal, so the exclusions above are conservative and the two flips are the robust ones
   (both had cores that were **never damaged and never healed** — no reactive term to grow).
2. **Optimistic:** the parked bot is also not doing anything *else* useful; the counterfactual
   is not "peck instead of repair", it is "peck instead of nothing" in 88–99% of the socket
   rounds recorded here.

**One number for the brief:** across the **10 losses**, **5,966 HP of core damage was
available to a verb that is switched off**, against enemy cores that finished those games
holding a combined **4,786 HP**.

---

## 4. §3 OF THE COMMISSION — FROSTGATE 0-3, DIAGNOSED (not bounded)

The three frostgate games in the v174 25-game set:

| game | opponent | replay | result | our seat |
|---|---|---|---|---|
| `d4566d49…_game_3` | kladde v168 | frostgate 20×20 | L r360 | **A** |
| `717140d8…_game_5` | farming_200s v19 | frostgate 20×20 | L r109 | **A** |
| `9d2247c3…_game_5` | Juusto v13 | frostgate 20×20 | L r462 | **A** |

**Structural fact first: all three are the same seat and the same geometry.** Our core at
**(2,9)**, theirs at **(16,9)** — same row, mirror-symmetric across x, on a 20×20 board.
**We drew seat A in 3 of 3.** (n=3; this is a draw observation, not an established seat
effect — but it is the first thing to check on the next frostgate appearance.)

**The banked call — "frostgate is a REACH crater" — is REFINED, and in the direction that
matters.** Reach was defined as *damage into their core > 0*; on that definition frostgate
scores 1/3 and looks like a transit failure. Measured on **arrival**, frostgate is our
**best** map in the set, not our worst:

| game | first raider at d²≤2 | first raider **on an orthogonal socket** | socket unit-rounds | longest unbroken park | acts while on socket | dmg into their core |
|---|---|---|---|---|---|---|
| vs kladde | r9 | **r9** | 227 | 16 rounds | 111 attacks (**226/229 into conveyors**), 7 builds, 109 nothing | 234, **healed to zero** |
| vs farming_200s | r18 | **r24** | 160 | **85 rounds** (bot #11 @ (15,9), r24→r108) | **153 of 160 = nothing**, 7 attacks (15 in the game, all conveyors) | **0** |
| vs Juusto | r14 | **r14** | 448 | **446 rounds** (bot #11 @ (15,10), r16→r461) | **446 of 448 = nothing** | **0** |

Field median arrival across the 25-game debut set is r12; frostgate arrives at **r9 / r14 /
r24** and then **holds the socket longer than on any other map** (448 and 160 socket
unit-rounds; the whole rest of the kladde+lazy set except yulerune is 8–205).

**⇒ Frostgate is not a reach crater. It is a CONVERSION crater — the purest one we have.**
The raider gets there earliest, stays longest, and converts nothing, because the verb it
would convert with is switched off.

**And the farming_200s game is the control that makes this unarguable: their core had ZERO
defensive turrets for the entire 109 rounds.** No sentinel, no gunner, no launcher anywhere
near it. There was nothing to shoot our raider, nothing to plug the socket, nothing to heal
the core. Our bot stood on the doorstep of an **undefended** core for **85 consecutive
rounds** — 170 HP of free damage on a 500 HP core, with a second raider available — and
never swung. Meanwhile their sentinel opened on our core at **r15** and finished at r109.

**What frostgate is NOT** (each checked, each negative):
* **not** a navigation/map-gate failure (contrast: the midgard/archipelago no-raid map-gate
  in `DECODE-launch-timing-v174`, where `launch_r = −1` and the raider walks in at r49–r57).
  Frostgate launches normally: throws fire from r6–r15 in all three, 48/45/7 throws.
* **not** a *total*-delivery crater in the banked sense — the banked doc noted deliveries
  were fine (52/18/11 stacks) and the totals agree (520 / 110 / 180 Ti). But the **flow**
  stops early in all three: last delivery **r78 / r29 / r37** on games running to r360 /
  r109 / r462 (§5.3).
* **not** CPU (tled = 0 of 458 on the longest-parked bot; p50 767 µs).
* **not** unit death (the parked bots hold 40/40 HP).
* **not** a poverty block on the peck (peck costs 2 Ti; floor is 4; we held 3–38 median).

---

## 5. §4 OF THE COMMISSION — SURPRISES (written before explanation)

### 5.1 ⭐⭐ SURPRISE 1 — kladde is running a titanium pump on us, and it is an exploit in exactly our own sense

**Written first, as a fact:** in kladde g5 (yulerune), **every single turret shot our team
fired all game — 236 of 236 — came from one sentinel at (6,11) and landed on one tile,
(3,8).** kladde built a **3-Ti barrier** on that tile **119 times** between r42 and r962 —
**119 of the 123 barriers they built in the entire game were on that one tile** (the other
four: (2,8), (4,8), (3,11), (5,9), all also beside our core) —
on a ~5-round cycle; our sentinel killed each one in 2 shots (18 dmg × 2 vs 30 HP), and they
rebuilt it.

The arithmetic, from two independent measurements that agree exactly:
* 236 sentinel shots × 10 ammo = **2,360 ammo**.
* `CoreConvertAmmo` events summed over the game: **2,360 titanium converted.**
* kladde's outlay: 119 barriers × 3 Ti base ≈ **357 Ti** (plus a +1% scale tick each, which
  also inflates *their* costs — cheap either way).

**Exchange rate ≈ 6.6 : 1 against us, and it consumed 100% of our offensive budget for
1,000 rounds.** We built zero siege turrets. Their core finished 500/500.

**And the tile is not arbitrary.** (3,8) is orthogonally adjacent to our core footprint tile
(3,9) **and it is where our own conveyor stood** — the throat of our northern belt (harvesters
at (6,6)/(4,3), conveyors at (3,3)–(3,7)). Our conveyor at (3,8) died at r41; **our last
titanium delivery was r38**; the first kladde barrier landed at **r42** and the tile was
never free long enough to rebuild. One 3-Ti tile denied us the entire game's economy —
**130 Ti collected against their 15,870.**

**Dose gradient across the set** (share of our turret shots landing on an enemy barrier,
and the most-shot tile):

| game | our turret shots | on an enemy barrier | most-shot tile | shots there | their barriers built | of those, within d²≤4 of OUR core |
|---|---|---|---|---|---|---|
| **kladde g5 yulerune** | 236 | **236 (100%)** | (3,8) | **236** | 123 | **123** |
| **kladde g4 auroraveil** | 86 | **69 (80%)** | (10,3) | 62 | 62 | **53** |
| lazy g1 royale | 54 | 34 (63%) | (7,1) | 24 | 22 | 9 |
| kladde g3 frostgate | 26 | 0 | (17,9) | 13 | 28 | 14 |
| kladde g2 glacierkeep | 37 | 4 | (14,6) | 31 | 7 | 5 |
| kladde g1 **W** midgard | 70 | 1 | (27,26) | 30 | 7 | 2 |
| lazy g2 nordkap | 4 | 0 | (11,15) | 3 | 32 | 12 |
| lazy g3 auroraveil | 108 | 12 | (9,2) | 51 | 19 | 5 |
| lazy g4 ragnarok | 14 | 0 | (3,2) | 14 | 11 | 6 |
| lazy g5 **W** drumlin | 29 | 0 | (5,6) | 19 | 16 | 7 |

**Two heavy doses, both kladde, both losses; the two wins are 1% and 0%.** n is far too
small to call that causal, but the mechanism is fully specified and cheap to test.

**Why this is a surprise and not just a loss:** `PROGRAMME.md`'s standing brief is to find
sequences of legal calls whose combined effect the opponent's code cannot survive. **kladde
found one against us and is running it.** Our banked read of their barrier plank
(`REPLAY-STUDY-kladde-multiver-2026-08-20` §P3) tested it as *spawn denial* (refuted, 0.0/0.0
per-100r) and as *heal denial* (refuted, 39 vs 43 HP/100r) and retired it as "intel, not a
weapon". **Both refutations tested the wrong effect.** The effect is
**turret-ammo attrition plus belt-throat occupation** — and on this evidence it is worth
**~2,400 Ti and an entire game's economy** for ~357 Ti spent. **That refutation should be
reopened.**

### 5.2 SURPRISE 2 — the verb is misdirected, not silent, and the field-debut framing understates it

`FIELD-DEBUT-v174` reports "builder core damage = 0 HP" and attributes it to the quiet-verb
family. True. What it does not say is that **our builders attacked 419 times in these ten
games while standing next to enemy cores, and 407 of those went into 20-HP conveyors.** The
raider is not idle-by-design; it is **actively spending its one action per turn on the
cheapest object in reach while the win condition sits one tile away.** That is a different
bug shape and it argues for a *target-priority* fix (core > conveyor when on a seat) rather
than a flag flip — and a target-priority fix is testable without disturbing the arrival
plank the flag was bought to protect.

### 5.3 SURPRISE 3 — the economy dies at r29–r86 in every loss, and that has not been named

**Ten losses, ten frozen income curves.** Last delivery to our core: r43, r78, r218, r38,
r42, r86, *never*, r77 (the eight match losses) and r29, r37 (the two borrowed frostgate
games) — median **r77** over the nine that delivered at all, with a median of **216 further
rounds** played on an empty wallet. **lazy g3 auroraveil collected literally zero
titanium in 1,000 rounds** while building 5 harvesters and 54 conveyors (31 of them lost).
None of the four banked docs carries a delivery-freeze number; they carry *stacks delivered*
(a total), which reads as healthy — "52 stacks", "13 stacks" — and hides that the flow
**stopped**. A total cannot show a stop. **Recommend a `last_delivery_round` column
wherever we currently bank `stacks delivered`.**

### 5.4 SURPRISE 4 — we lose the turret race but we also don't contest it

In **4 of the 8 match losses we never build a siege sentinel at all** (kladde g2, kladde g5,
lazy g1, lazy g2) and in a fifth it lands at **r289 of a game that ends at r295** (kladde g4).
Across all 10 losses, **6 finish with 0 damage into their core**. In **lazy g2 nordkap
we fired 4 turret shots in 425 rounds** while one enemy sentinel fired 133 into our core.
This is downstream of §5.3, but the size of it is new: their kill weapon in three of four
lazy wins is a **single building, planted orthogonally adjacent to our core, that nothing
ever shoots back at.**

### 5.5 SURPRISE 5 — the defect is fully present in the games we win

kladde g1 (win, r117): bot #3 held a socket for 64 consecutive rounds and spent 51 attacks
on a conveyor. lazy g5 (win, r278): 0 builder damage into their core. **Both wins were won
by sentinels.** So the parked-raider defect is not a loss-correlated artefact — it is
**constant**, and the wins are wins for an unrelated reason. Any leg that measures the fix
must not use "do we win" as its dose control.

### 5.6 SURPRISE 6 — `ti_collected` on the replay wire was being read wrong

Minor, instrument-hygiene, recorded because it would have produced a false finding: the
`UpdatePlayers` update wraps a `Players` message before the per-team `Player` — parsing
`fields(update)` as team A/B directly yields **0 for every team in every game**, which
reads as a plausible "we collected nothing" rather than as a parse failure. Caught by a
constant-column smell (0/0 in all 10 games including a game we won on `titanium_collected`).
Fixed before any number in §2.2 was written. **A constant column validates anything** —
the tables in §2.2 were re-derived after the fix, and cross-checked against
`FIELD-DEBUT-v174`'s independently-decoded stack counts (kladde g5: 13 stacks banked
there = 130 Ti here ✓; kladde g3: 52 stacks = 520 Ti ✓; kladde g4: 58 stacks = 580 Ti ✓;
kladde g1: 129 stacks = 1,290 Ti ✓). **Four independent agreements, zero mismatches.**

---

## 6. WHICH BANKED MECHANISM EACH LOSS CONFIRMS OR CONTRADICTS

| loss | banked mechanism | verdict |
|---|---|---|
| kladde g2 glacierkeep | kladde r11 home sentinel (`REPLAY-STUDY-kladde` §3.3) | **CONFIRMED** — theirs at r9. But it is **not** what killed us: their (14,6) sentinel built **r45** did all 864. The home-guard sentinel denies our raid; a *second*, forward one kills. |
| kladde g3 frostgate | sentinel = 98.6% of kladde's kill channel | **CONFIRMED** (100% here). |
| kladde g3/g4/g5 | "arrival→conversion" corrected reading (Amendment 2) | **CONFIRMED AND SHARPENED** — arrival is not the problem anywhere; conversion is, and the conversion failure is *misdirected verb*, not *absent verb* (§5.2). |
| kladde g4 auroraveil | kladde's core-ring barrier seal is "intel, not a weapon" (§P3, refuted twice) | **CONTRADICTED** — 69 of our 86 shots went into replanted barriers. The two refutations tested spawn denial and heal denial; the live effect is **ammo attrition + belt-throat occupation** (§5.1). |
| kladde g5 yulerune | ditto, plus `R1000_IS_DEFEAT` | **CONTRADICTED at full dose** — 236/236 shots, 2,360 Ti, 119 rebuilds. Also the clearest `R1000_IS_DEFEAT` game in the set: we played 1,000 rounds having stopped earning at r38. |
| lazy g1 royale | team lazy point-blank forward sentinel, median d²=5 (`REPLAY-STUDY-teamlazy` §3) | **CONFIRMED** — (9,1), built r137, orthogonally adjacent to our core, 504 HP. |
| lazy g2 nordkap | ditto | **CONFIRMED AT EXTREME** — (11,19), built r158, adjacent, **2,394 HP over 265 rounds, 133 shots, 0 return fire.** Also the map-is-the-matchup call: nordkap was 1/8 = 12.5% for us in the banked 80-game cut and lost again here. |
| lazy g3 auroraveil | ditto + map class (auroraveil 0/2 = 0% banked) | **CONFIRMED on the map class** (0/2 → 0/3). Their kill channel is present but weak; the actual loss is economic (0 Ti collected in 1,000 rounds). |
| lazy g4 ragnarok | map class (ragnarok 0/4 = 0% banked) + point-blank sentinel | **CONFIRMED both** — 0/5 now; (28,26) sentinel adjacent to our core at r52. |
| all 8 | "r113–116 sentinel clock is Flotte's, not lazy's" | **CONFIRMED** — lazy's builds land r24/r52/r137/r158/r184/r259, no r113–116 clustering. |
| all 10 | r5/r6 launch constant (`DECODE-launch-timing-v174`) | **CONFIRMED** — first throws land r6–r16 in 9 of 10; the two midgard-class refusals are not in these matches (kladde g1 midgard had 0 throws, consistent with the banked midgard refusal class, and we won it). |
| kladde g1, lazy g5 (**wins**) | `LOKI_QUIET_ON` core-peck gate | **CONFIRMED AS CONSTANT** — 0 builder core damage in the wins too (§5.5). |

---

## 7. WHAT THIS DOES AND DOES NOT LICENSE

**Licensed:**
* Naming **misdirected-verb** (not silenced-verb) as the conversion-at-destination failure,
  with a concrete testable fix shape: **on-seat target priority, core before conveyor.**
* Reopening the kladde barrier-plank refutation against the **ammo-attrition / belt-throat**
  effect (§5.1) — the two banked refutations tested different effects and do not cover this.
* Adding **`last_delivery_round`** alongside `stacks delivered` in any econ cut (§5.3).
* Treating **frostgate as a conversion crater, not a reach crater** (§4), and checking the
  seat-A draw (3/3) on its next appearance.

**NOT licensed:**
* Any win-rate or currency verdict. **n = 12 games, 2 rated matches + 2 borrowed games**,
  us-only, single-day, opponents pinned only by the fact that these are the versions they
  happened to be running. Every share here is descriptive.
* Any causal claim that the tarpit *caused* the two kladde losses — the dose gradient
  (100%, 80%, 63%, then near-zero) is suggestive and n=10.
* Flipping `LOKI_QUIET_ON`. The flag was bought for arrival, arrival is measurably fine
  (25/25 in the field set), and `DECODE-launch-timing-v174` §7 records a −10.83pp cost when
  a related muster fix was taken naively. **The finding here is a target-priority defect on
  seats, which is a narrower change than the flag.**
* Retiring any road. Per point 6 of the standing brief, closure needs live games; this is a
  decode.
