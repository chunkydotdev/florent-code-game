# REPLAY STUDY — Jython, match `617d4d27`, as inspiration for the ferry-siege plank

**Written** 2026-08-17T17:47:56Z (`date -u`, same shell). **Author:** builder-arm replay-study
subagent, s50. **Status:** banked observation, not a verdict. **Not committed by this agent.**

**Scope, stated up front so no number in here is read wider than it is:** this is **ONE rated
ladder match, 5 games, one opponent (`sporks`)**. Every count below is `n=5 games` or a
per-game figure. Nothing here is a population statement about Jython, about the ladder, or
about the plank's expected value. It is a mechanism read.

---

## 1. Match context

| field | value |
|---|---|
| match id | `617d4d27-9a2c-4937-bfb9-e610f1958473` |
| type | ladder, **rated** |
| created / done | 2026-08-17 17:12:59Z / 17:15:13Z |
| team A | **Jython**, submission **v157**, rating before **2174.62** (top of ladder) |
| team B | **sporks**, submission **v26**, rating before **2023.32** |
| result | **A 4–1**, eloDelta A **+3.04** |
| source | `corpus/league_matches.tsv` + `fcode match info` |

**Decoder mapping, established before any claim was made:** in every decoded replay
**team index `0` = team A = Jython**, index `1` = sporks. Verified by core-death events —
team 1's core dies in games 1/2/4/5 (the four A wins) and team 0's core dies in game 3
(the one A loss), matching `fcode match info` exactly.

Per-game:

| # | map | size | core A (Jython) | core B (sporks) | winner | turns | core died round |
|---|---|---|---|---|---|---|---|
| 1 | ragnarok | 30×30 | (2,2) | (26,26) | **A** | 163 | B @ r162 |
| 2 | midgard | 30×30 | (2,2) | (26,26) | **A** | 126 | B @ r125 |
| 3 | fjordgate | **10×10** | (2,2) | (6,6) | **B** | 337 | **A @ r336** |
| 4 | glacierkeep | 30×30 | (14,2) | (14,26) | **A** | 185 | B @ r184 |
| 5 | yulerune | 20×20 | (3,9) | (16,9) | **A** | 115 | B @ r114 |

Method: replays downloaded with `fcode match replay` into the session scratchpad (the match
was **not** yet in `replay_archive/`; corpus manifest built 17:29:08Z still had 0 rows for it).
Decoded with the repo toolchain only — `tools/corpus/replay_events.py`,
`replay_throws.py`, `replay_econ.py`, `tools/corpus/replay_autopsy.py`. **No repo tool was
modified.** One scratchpad-only raw-update dumper
(`scratchpad/jython_study/dump.py`) was written to read intra-round event ORDER, which no
existing tool emits; it is a thin wrapper over `tools/replay_census.py`'s `fields()` /
`parse_entity()` and is not banked.

**Instrument caveat, recorded rather than worked around:** `replay_autopsy.py`'s
`-- launcher throws --` section printed **nothing** for game 1, while `replay_throws.py`
decoded **174 throws** in that same file. The two disagree on game 1 only. `replay_throws.py`
is treated as the authority here (its counts reconcile with the raw `moveBuilderBot` stream I
dumped by hand for rounds 2–46). **Do not read game-1 throw counts off the autopsy.**

---

## 2. What Jython is

**Jython v157 is the ferry-siege plank, already built and running at 2174 Elo.** Not something
adjacent to it — the same four moves, in the same order, executed from round 0.

The shape, in one sentence: *spawn exactly three builders; the first one builds a launcher
beside itself, is thrown ~5 tiles forward, the launcher self-destructs, repeat until the bot is
adjacent to the enemy core in under 12 rounds; then that one bot rings the enemy core in
barriers, keeps one launcher alive to throw arriving enemy builders away, and builds one or two
**sentinels** aligned on a straight line into the core footprint, which do 96.8% of all the core
damage.*

### 2.1 Opening (identical in all 5 games)

Builder spawns at **r0, r1, r2 — exactly 3, every game**. Total builders over the whole game:
4 / 3 / 6 / 5 / 7 (games 1–5); every later spawn is economy, never a second raider.

Build attribution by `builderBuild` id (game 1 / game 5): **bot `3` — the r0 spawn — is the
raider and makes 17 / 18 builds**; bots `5`,`9` (g1) and `5`,`8` (g5) make 18/18 and 11/15 and
are pure economy (harvesters + one long conveyor line each). **One raider, two eco. The raider
builds every forward launcher, every ring barrier, and every forward turret** (the only
exception in 5 games: game 1's second sentinel at r104 was built by bot `112`, a later spawn
that walked up).

Jython built **zero splitters** across all 5 games, and **one gunner** (game 3, defensive, at
home).

### 2.2 The self-ferry chain — OBSERVED, mechanism confirmed on the wire

The cadence is exact and it is 2 rounds per hop:

```
round N   (odd) : raider builds a launcher on an orthogonally adjacent tile, ~1 tile forward
round N+1 (even): that launcher throws the raider ~5 tiles forward, THEN the launcher dies
```

Raw update stream, game 1, rounds 1–6 (my scratchpad dumper, ordered as the engine emitted it):

```
1  BUILD  3 (5,4)          <- raider id 3 builds launcher (id 7)
2  MOVE   3 -> (9,7)       <- launcher 7 throws the raider, d2 25 from the launcher
2  REMOVE 7                <- launcher 7 gone, SAME round, immediately after its own throw
3  BUILD  3 (10,7)         <- raider builds the next launcher (id 12)
4  MOVE   3 -> (14,10)
4  REMOVE 12
5  BUILD  3 (15,10)
6  MOVE   3 -> (19,13)
6  REMOVE 19
```

**The removal carries no `UpdateHp` and the raider — the only friendly unit that was adjacent —
had already been thrown off the tile by the very event that precedes the removal.** The
`REMOVE` is emitted inside the launcher's own slot in the round, directly after its `launch()`.
⇒ **the launcher calls `self_destruct()` in the same `run()` as its throw.** The same pattern
appears identically in game 5 (`2 MOVE 3 -> (8,9)` / `2 REMOVE 7`) and games 2 and 4.

Ferry chains built (chain launchers → destroyed):

| game | chain launchers | destroyed | launcher tiles | raider at d²≤8 of enemy core |
|---|---|---|---|---|
| 1 ragnarok | 6 | 5 (r2,4,6,8,10) | (5,4)(10,7)(15,10)(20,13)(24,17)(26,22) | **r12** |
| 2 midgard | 6 | 6 (r2,4,6,8,10,12) | (5,3)(9,7)(13,11)(18,14)(23,17)(27,20) | **r12** |
| 3 fjordgate | 1 | 1 (r9) | (5,4) | **r2** |
| 4 glacierkeep | 4 | 3 (r2,4,6) | (14,5)(14,11)(14,17)(14,23) | **r8** |
| 5 yulerune | 3 | 2 (r2,4) | (5,9)(8,10)(13,10) | **r6** |

Across all 5 games Jython built **26 launchers and destroyed 17 of them (65%)**.

**Hop geometry, measured:** every ferry throw used **d² = 25 from the launcher** (e.g. (5,4)→(9,7);
(14,5)→(14,10)) — i.e. 5 tiles in a straight line or a (4,3) knight-ish offset, never the
legal-but-awkward d²=26. Net advance per 2-round cycle = **5 tiles of throw + ~1 tile of build
offset ≈ 6 tiles**.

**Speed against the walking baseline:** builder bots move 1 **cardinal** tile per round
(observed on Jython's own eco bot `9` in game 1: (1,2)→(1,3)→(1,4)→(1,5) on r3,4,5,6). Manhattan
distance from the r0 spawn (4,4) to the enemy ring (25,25) on a 30×30 is **42 tiles ⇒ ~42
rounds walking**. **The ferry lands at r12. It buys ~30 rounds on a 30×30 map**, and it lands
before the opponent has bought a single turret.

### 2.3 The barrier ring — and it is a full 12 tiles

The enemy core is 2×2, so its adjacency ring is exactly **12 tiles**. Jython barriers them.

| game | barriers built | on the ring | **ring tiles covered** | ring sealed |
|---|---|---|---|---|
| 1 ragnarok | 7 | 7 | 7/12 (+2 covered by its own launchers on ring tiles ⇒ **9/12**) | never |
| 2 midgard | 7 | 7 | 7/12 (+2 by launchers ⇒ **9/12**) | never |
| 3 fjordgate | 9 | 6 (4 distinct) | 4/12 | never |
| 4 glacierkeep | 13 | 12 | **12/12** | **r51** |
| 5 yulerune | 15 | 13 | **12/12** | **r44** |

**Two ring tiles in games 1 and 2 are occupied by Jython's own surviving eviction launchers
((25,25)+(25,28) in g1; (28,25)+(25,28) in g2). A launcher parked on a ring tile does double
duty — it denies the tile AND evicts.** Worth copying.

**The tiles Jython leaves open are always the near face** (the x=25 column in games 1/2, i.e.
the side facing Jython's own core). That is the direct cause of the two leaks in §4.1.

### 2.4 The ring is a SPAWN LOCK — and this is the strongest single finding in the study

`sporks`' core spawned builders **only ever on ring tiles**, and its choice of tile **migrated
onto exactly the tiles Jython failed to barrier**:

* **game 1** — sporks spawn tiles, in order: (25,25) r0, (25,27) r1, (26,25) r2, (25,27) r3,
  (25,25) r16, r21, r27, then **(25,27) at r105 and r132**. Jython barriered (26,25) at r27 and
  never touched (25,25)/(25,26)/(25,27). **Every sporks spawn after Jython started barriering
  (r13) is on one of the three tiles Jython left open.**
* **game 2** — (26,25) r0, (25,26) r1, (26,25) r2, (25,26) r3, r20, r52, r55, r73, r88,
  (25,27) r103. Jython barriered (26,25) at r27; **every subsequent sporks spawn is on
  (25,26)/(25,27) — the two tiles Jython left open.**
* **games 4 and 5** — ring sealed 12/12 at r51 / r44; sporks' last spawn was **r18 / r8**, and
  in game 5 sporks' spawn tiles were (15,10),(15,8),(18,11),(18,8) — **all four are ring tiles
  that Jython later barriered.**

⇒ **OBSERVED: the enemy core's legal spawn set is the 12-tile adjacency ring, and barriering a
ring tile removes it from that set.** ⇒ **INFERRED (not proven by this match): a complete
12-barrier ring is a total spawn lock.** In games 4 and 5 the ring sealed *after* sporks had
already stopped spawning for other reasons (see §2.5 — they were broke), so the seal itself
never got to be the binding constraint. **The game-1/2 tile migration is the proof of
mechanism; the total lock is the extrapolation.**

### 2.5 The ring is ALSO an economy kill — `titanium_collected` driven to zero

A conveyor delivers into a core only from a tile adjacent to it. The ring tiles **are** those
tiles.

**Game 5, worked:** sporks ran a belt from harvester (13,6) → (14,6) → (15,6) → (16,6) → (16,7),
aiming at their core at (16,9). The last link they needed was **(16,8) — which Jython barriered
at r27.** sporks rebuilt the head of that belt **seven times** (conveyor builds at (15,6) r21,
r64, r80; (15,7) r84, r93; (16,6) r32, r48; (16,7) r40, r97; then (17,7) r104, (18,7) r112) and
**never connected**. Result: **sporks' `titaniumCollected` = 0 for the entire 115-round game,
and their titanium balance ended at 0.**

**Game 4** is the deliberate version: sporks' belt crawled to (15,23); Jython's ring sealed the
whole y=25 row by r35, and then at **r59 Jython built an OFF-ring barrier at (15,24)** — the one
tile that would have bridged (15,23) to the core. **Both teams finished game 4 with
`titaniumCollected` = 0.**

`titaniumCollected` (Jython / sporks), end of game: 770/170 · 820/580 · 290/620 · **0/0** · 640/0.

### 2.6 The eviction launcher — `can_launch` has no team check, used at scale

One launcher (occasionally two) is kept alive near the enemy core and throws arriving **enemy**
builders to a fixed dump tile, over and over.

| game | EXILE throws | distinct victims | dump tile (modal) | d² dump→enemy core | victim fates |
|---|---|---|---|---|---|
| 1 | **108** | 9 | (22,19) ×87 | 65 | 99 RETHROWN, 9 ALIVE_END |
| 2 | 21 | 9 | (20,29) ×14 | 45 | 12 RETHROWN, 2 DIED, 7 ALIVE_END |
| 3 | 13 | 11 | **(4,0) ×6 — see §4.2** | 40 | 7 DIED, 2 RETHROWN, 4 ALIVE_END |
| 4 | 20 | 6 | (11,19) ×20 | 58 | 14 RETHROWN, 6 ALIVE_END |
| 5 | 5 | 4 | (9,13) ×5 | 65 | 1 RETHROWN, 4 ALIVE_END |

**Game 1 is the fully-developed form: 108 throws against 9 bots, 99 of them re-throws of a bot
already thrown.** With two eviction launchers (built r29 and r31) the cooldown allows roughly one
throw per round. sporks' builders spent the rest of the game walking back and being thrown out
again; **Jython's core took 0 damage all game and sporks' core was healed +0.**

**Dump-tile selection looks like "maximum legal range from the launcher"** — one fixed tile per
game, at d²≈25 from the launcher. It is **not** direction-aware (§4.2), and it is **not**
crash-induction: 41 of 167 EXILE throws land on a **border** tile, but **not one victim died
with the crash signature** (all 9 EXILE deaths carry `vhp=3`, i.e. real HP events = combat
deaths; the LOKI-14 signature is `DIED` with `vhp=0`). **Jython evicts; it does not
crash-induce. Our LOKI-14 border trick is orthogonal and additive to this plank.**

Jython also throws its own builder onto a border tile **26 times** across the match and survives
every time — Jython's own code is border-safe.

### 2.7 The kill is a SENTINEL, and the sentinel must be line-aligned

Core damage dealt by Jython, all five games (`replay_autopsy.py`, self-checking ledger, MATCH on
every core):

| game | enemy core damage | attribution | first damage | dead |
|---|---|---|---|---|
| 1 | 504 | **sentinel 504 (100%)** | r108 | r162 |
| 2 | 542 | sentinel 540 + builder_attack 2 | r61 (sentinel) | r125 |
| 3 | **66** | **builder_attack 66 (100%)**, healed +64 by sporks | r60 | survived |
| 4 | 504 | **sentinel 504 (100%)** | r81 | r184 |
| 5 | 540 | **sentinel 540 (100%)**, healed +28 | r74 | r114 |

**2,088 of 2,156 HP of core damage across the match — 96.8% — came from sentinels. Builder
attacks contributed 68 HP total.**

Every core-damaging shot is on a **pure straight line — cardinal or 45° diagonal — into a tile
of the core footprint**, inside sentinel range r²≤32:

```
g1  (29,23) -> (26,26)   diagonal SW, d²=18   x28 shots   = 504
g2  (29,27) -> (26,27)   cardinal W,  d²=9    x29 shots   = 522   (+1 at (29,26)->(26,26))
g4  (15,29) -> (15,26)   cardinal N,  d²=9    x28 shots   = 504
g5  (13,9)  -> (16,9)    cardinal E,  d²=9    x21 shots
    (14,10) -> (16,10)   cardinal E,  d²=4    x9  shots   = 540 combined
```

**Game 1 shows the cost of getting alignment wrong:** Jython built two sentinels at r103/r104,
at (29,23) and (29,24). (29,23) is on the perfect diagonal and fired 28 core shots. **(29,24) is
on no line through the core footprint at all — it fired once at an unrelated target and then
never contributed to the kill.** Half the turret budget, zero core DPS. Game 5, by contrast, has
both sentinels aligned, and the core damage rate visibly steps from 18-per-2-rounds to
**18 per round** at r97 (the second sentinel came online at r96) — **kill at r114 instead of
~r140.**

**The barriers do not block the sentinel.** A sentinel's shot is single-tile-wide and resolves on
the target tile, so Jython's own 12-tile ring sits between the sentinel and the core with no
effect. **A gunner would be blocked.** That is why this plank uses sentinels, and it is the
non-obvious pairing that makes ring + turret coexist.

### 2.8 Ammunition is the real clock on the kill

| game | Jython Ti→ammo | sentinel shots | sporks Ti→ammo | kill round |
|---|---|---|---|---|
| 1 | 430 | 43 | 54 | 162 |
| 2 | **700** | 70 | 54 | 125 |
| 3 | 458 | 32 | 404 | (lost) |
| 4 | **280** | 28 | 54 | **184** |
| 5 | 300 | 30 | 30 | **114** |

500 core HP ÷ 18 = **28 sentinel shots = 280 ammo, minimum**. Game 4 converted exactly 280 and
the shot cadence degraded from every-2-rounds to **every-4-rounds after r88** — pure ammo
starvation, and it cost ~70 rounds of kill time on an otherwise-perfect 12/12 ring. **Game 5
converted 300 with a working economy and killed at r114.**

⇒ **The economy in this plank is not for the tiebreak and not for buildings. It exists to buy
280–560 ammunition by roughly r70.** Note game 4 won at r184 with `titaniumCollected` = **0** —
the whole kill was financed by the 500 starting titanium plus passive income.

**Second sentinel role, and it is not core damage:** in game 2, 27 of 70 shots went to
(24,26) — a tile sporks kept rebuilding on — and 7 went to (25,26), sporks' spawn tile. That is
**270+ ammo spent on suppression, not on the core**, and it is why game 2 needed 700.

### 2.9 Forward-sentinel churn: they are also demolition tools, then deleted

Games 1 and 2 both build an early forward sentinel pair (g1 r32+r33; g2 r19) whose shots go to
**enemy conveyors on and around the ring** — (23,25)→(26,25), (28,23)→(24,27) — clearing the
tiles the barriers then occupy. **Those sentinels are then removed with no `UpdateHp` event
(g1 r40, r44; g2 r28) — i.e. destroyed by Jython itself**, exactly like the ferry launchers.
The killing sentinels are re-bought later (g1 r103; g2 r53/54), when ammo exists.

**Read on the destroy-after-use habit** (INFERRED, but the arithmetic is not in doubt): every
build permanently adds to ONE global additive cost scale (launcher +10%, sentinel +20%) and
**destruction removes the contribution**. A 6-launcher ferry chain left standing would carry
**+60%** into the price of the sentinel that has to kill the core; self-destructing five of them
leaves **+10%**. Same for the demolition sentinels. **The self-destruct is a price control, not
tidiness.**

---

## 3. DESIGN INPUTS for the ferry-siege plank

Each tagged **[O]** = observed in these replays, **[I]** = inferred (reasoning stated).

1. **[O] The 3-builder opening is right, and it is 1 raider + 2 eco, not 2+1.** Jython spawns
   exactly 3 at r0/r1/r2 in all 5 games and the r0 bot is the raider in all 5. The raider does
   **everything** forward — launchers, ring, turrets. Do not plan a second forward builder;
   plan for the first one to survive.
2. **[O] Build the launcher, throw, self-destruct — all inside 2 rounds, and the self-destruct
   is the LAUNCHER's own call, not a builder `destroy()`.** Confirmed on intra-round event
   order (§2.2). Design consequence: the ferry logic lives in the **launcher's** `run()`
   (`launch(bot_pos, target)` then `self_destruct()`), not only in the builder's.
3. **[O] Hop at d² = 25 from the launcher, ~6 tiles of net advance per 2 rounds.** Ferry arrival
   at the enemy ring: **r12 on 30×30, r8 on a 24-tile straight axis, r6 on 20×20.** Walking the
   same 30×30 is ~42 rounds. **Budget ~30 rounds of tempo.**
4. **[O] Ring the enemy core with 12 barriers — the ring is the enemy's SPAWN SET.** sporks
   spawned only ever on ring tiles and migrated onto exactly the tiles Jython left open (§2.4).
   **A partial ring is not a partial lock; it is a funnel that tells the enemy where to spawn.**
5. **[O] The ring is simultaneously an economy kill: the ring tiles are the only tiles a
   conveyor can deliver to the core from.** sporks' `titaniumCollected` = **0** across a full
   115-round game with three harvesters and 17 conveyor builds (§2.5). **Prioritise the ring
   tile the enemy's belt is pointing at, and add the one off-ring plug tile behind it** (Jython
   did exactly this at (15,24) in game 4, r59).
6. **[O] Park a surviving launcher ON a ring tile.** It denies the tile and evicts from it.
   Jython did this twice each in games 1 and 2.
7. **[O] Eviction works and it is cheap: 0 ammo, +1 cooldown, position-only.** 108 throws in one
   game against 9 enemy builders, 99 of them re-throws. The enemy never touches the core.
   Jython's core took **0 damage** in game 1 and **0** in game 2.
8. **[O] THE KILL IS A SENTINEL ON A STRAIGHT LINE. Nothing else scales.** 96.8% of all core
   damage across the match. The line must be cardinal or 45° through a **core footprint tile**,
   at d²≤32. **A mis-aligned sentinel contributes zero** (game 1's (29,24) — 1 shot, then
   nothing). **Gate the build site on `can_fire_from(position, direction, SENTINEL, core_tile)`
   before spending 30 Ti.**
9. **[O] The barrier ring does not block your own sentinel** (single-tile-wide shot, resolves on
   the target tile). **A gunner would be blocked.** Ring + sentinel is a compatible pair;
   ring + gunner is not.
10. **[O] Two aligned sentinels double the rate: 18/2 rounds → 18/round → 500 HP in ~28 rounds.**
    Game 5's second sentinel at r96 turned a ~r140 kill into **r114**.
11. **[O] Ammo, not titanium, is the clock. 280 ammo is the floor (28 shots × 10); 300 with a
    working belt gave the fastest kill in the match.** Game 4 killed at r184 purely because it
    only ever converted 280. **Plan a `convert_ammo` ramp that has ≥280 banked by ~r70.**
12. **[O] The plank does not need a real economy to win.** Game 4: Jython's `titaniumCollected`
    = **0** for the whole game and it still killed at r184 on starting titanium + passive.
    **Under `R1000_IS_DEFEAT` this is exactly the right shape — economy is instrumental, and
    here it is instrumental to *ammo*.**
13. **[I] Self-destruct the spent launchers and the spent demolition turrets for the COST SCALE,
    not for neatness.** 5 spent launchers left standing = +50% on the price of the sentinel that
    has to finish the game. (Engine fact from CLAUDE.md; the behaviour is observed, the reason
    is inferred.)
14. **[O] Use forward sentinels as demolition first, then delete them and re-buy when ammo
    exists.** Games 1 and 2 both clear the enemy's ring-adjacent conveyors with a throwaway
    sentinel pair before barriering those tiles.
15. **[I] Approach and set up on the FAR side.** In 4 of 5 games the killing sentinel sat beyond
    the core relative to Jython's home (g1 (29,23), g2 (29,26/27), g4 (15,29)); game 5 is the
    exception (near side, (13,9)/(14,10)). The far side is where the enemy's own traffic and
    belts are not.
16. **[O] CPU headroom is thin at this level and must be designed for.** Jython's per-unit
    `cpu_max` reached **9,598 µs against a 10,000 µs budget** (game 1, r150–200 band);
    `tled = 0` in every band of every game. sporks peaked at 2,977 µs. **A siege bot that
    re-scans the ring every round will sit near the ceiling — budget it explicitly.**

---

## 4. What NOT to imitate

### 4.1 [O] The eviction launcher kidnaps its OWN raider, and it cost them the ring

`can_launch` has no team check — **including against your own units.** Jython's target selection
does not exclude them.

**Game 1: 57 `RETREAT` throws** (own bot thrown *away* from the enemy core). From r32 to ~r100
the raider oscillates on a treadmill, every 2 rounds:

```
r35  MOVE 3 -> (26,24)      <- raider walks toward the core
r35  MOVE 3 -> (28,24)      <- its OWN launcher at (25,25) throws it back out
r37  MOVE 3 -> (26,24)
r37  MOVE 3 -> (28,24)      ... repeated ~34 times
```

**Game 1's ring finished at 7/12 and game 2's at 7/12 — the two games where the raider was
juggled 57 and 28 times — while games 4 and 5, with 2 and 3 `RETREAT`s, both sealed 12/12.**
The raider could not reach the far face because its own launcher kept throwing it off.

⇒ **Our eviction launcher MUST filter `get_team(bot_id) != my_team` before launching. This is a
one-line guard that is worth ~5 ring tiles.**

### 4.2 [O] The dump tile is chosen by "maximum range", with no idea where your own core is

On fjordgate (10×10) Jython's launcher sat at (7,4), one tile from sporks' core, and threw
sporks' builders to (4,0) and (4,1) — **d² = 8 and 5 from JYTHON'S OWN CORE at (2,2)**.
**10 of 13 EXILE dumps in game 3 landed inside d²≤8 of Jython's own core.** They were
air-dropping the enemy siege team onto their own doorstep. sporks' builders then camped (4,1)
and (4,2) and pecked; Jython had to build a home gunner at r24 and home sentinels at r112/r175
to deal with them, and lost the game.

⇒ **Score dump candidates by `d²(target, MY core)` — maximise it — not by `d²(target,
launcher)`. On a small map those two objectives point in opposite directions.**

### 4.3 [O] Builder pecking at a core is worthless against a healing defender

Game 3: Jython threw **147 `builderAttack` events** and put **66 HP** onto sporks' core over
r60–r92 (2 dmg/round, 2 Ti each). sporks healed **+64** of it. **Net 2 HP in 33 rounds, for
~294 Ti of attack cost.** Meanwhile sporks' own core damage on Jython came from sentinels at
r289+ and finished the job in 47 rounds.

⇒ **Never denominate the kill in builder pecks. 2 dmg/round loses to one builder healing
+4/round. Peck only to clear 20–30 HP buildings (conveyors, barriers), never a 500 HP core.**

### 4.4 [O] The plank degenerates on a SMALL map, and game 3 is the failure mode in full

fjordgate is 10×10 with cores 32 d² apart. Every leg of the plank inverted:

* **the ferry is pointless** — one throw at r2 puts the raider adjacent; there is no tempo to buy;
* **the raider dies** (r21) because the enemy's whole army is already there — Jython's only
  builder loss in 4 of 5 games is 0, in game 3 it is 2;
* **barriers are contested, not built once**: Jython's barrier at (5,5) was destroyed at r13,
  r19 and r124 and rebuilt each time; the ring reached 4/12 and never held;
* **no replacement raider was ever sent** — Jython's last builder spawn was **r8**, then nothing
  for 328 rounds, while sporks spawned six replacements from r128 onward;
* **the eviction throws fed Jython's own base** (§4.2);
* **the game becomes a 337-round defensive slugfest, which is a defeat under
  `R1000_IS_DEFEAT`'s logic even had they won it.**

⇒ **Two required decisions our version must make that Jython's does not appear to make:
(a) a map-size / core-distance gate — below some `d²(core,core)` threshold the ferry-siege is
not the plan; (b) a raider-replacement rule — if the raider dies before the sentinel is up,
spawn and ferry another one.** Jython has neither and it is exactly what lost them the game.

### 4.5 [O] Do not leave ring tiles open on the near face

Jython's misses are always the face pointing at its own core (x=25 in games 1 and 2). That is
the face the enemy spawns from and the face the enemy walks in from. If the ring must be
partial, **seal the face the enemy actually uses**, which the replays say is the near face.

---

## 5. Surprises — written down before explaining them away

1. **Jython IS the plank, already.** The brief described a design; the top of the ladder is
   running it, at 2174 Elo, with the launcher self-destruct and the eviction launcher intact.
   This changes the plank from "invent" to "reimplement, then fix the four defects in §4".
   *(Not explained away: it also means the plank's ceiling is at least observed, not hypothetical.)*
2. **Game 4 was won at r184 with `titaniumCollected` = 0 for BOTH teams.** A core kill financed
   entirely by the 500 starting titanium and passive income. Nobody in this repo has priced the
   plank that way.
3. **`sporks`' `titaniumCollected` was 0 across a full 115-round game while running three
   harvesters and rebuilding the head of its belt seven times.** A single barrier on the last
   delivery tile zeroed a functioning economy. **This is a much sharper economy weapon than
   anything in `SIX-ROADS-STATUS`, and it is free — the ring is being built anyway.**
4. **The enemy's spawn-tile choice visibly migrated onto the tiles Jython failed to barrier.**
   I expected to have to infer spawn denial; it is legible directly in the spawn positions.
5. **41 of 167 eviction throws land on a border tile and not one victim crashed.** sporks v26 is
   border-safe. Our `crash_census` field average is not what a 2000-rated opponent looks like —
   **the crash trick and the eviction plank are additive but the crash half will not fire against
   the top of the ladder.**
6. **Jython throws its OWN builder onto a border tile 26 times and survives.** They have the same
   guard we added to `eco.py`.
7. **A mis-aligned sentinel contributes literally nothing** — game 1's (29,24) fired once at a
   non-core target across a 60-round window while its twin did all 504 damage. I expected
   degraded contribution, not zero.
8. **Jython runs at 9,598 µs of a 10,000 µs budget with `tled = 0`.** The top of the ladder is
   spending its full CPU allowance every turn. Whatever it computes each round is not cheap.
9. **Jython builds no splitters at all and exactly one gunner in 5 games** (defensive, in the
   game it lost). The entire military is sentinels and launchers.

---

## 6. Files

* Replays (scratchpad, not banked):
  `<scratchpad>/jython_study/replays/617d4d27-…_game_{1..5}.replay26`
* Derived tables (scratchpad): `events.tsv`, `throws.tsv`, `econ.tsv`, `flow.tsv`
* Scratchpad-only raw-update dumper: `<scratchpad>/jython_study/dump.py`
* Repo tools used, unmodified: `tools/corpus/replay_events.py`, `replay_throws.py`,
  `replay_econ.py`, `replay_flow.py`, `tools/corpus/replay_autopsy.py`, `tools/replay_census.py`
