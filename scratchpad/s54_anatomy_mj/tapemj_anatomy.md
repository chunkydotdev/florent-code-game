# EARLY-WINDOW LOSS ANATOMY — `bots/_v612skalman` vs `bots/_x3r0v168mjolnir` (tapemj)

**Decode agent, builder s54, 2026-08-22. READ-ONLY: no repo edits, no matches, no commits.**

Fixture: `scratchpad/s54_fidtape/replays_tapemj/` — 15 pool maps × both seats = 30 distinct
games (`*_A` = we are side 0, `*_B` = we are side 1, per `scratchpad/s54_fidtape/tapemj.sh`).
Opponent is the NOISE_OFF copy of the imported x3r0 v168 "Mjolnir" snapshot.

**Decoders reused, not rewritten.** `scratchpad/s54_autopsy/tape30_deaths.py` supplies the
whole entity/damage walk under its validated attribution law (FireTurret → unit-on-`to`
else building-on-`to`, dmg 7/18; BuilderAttack → building on `tgt`, dmg 2). Its self-check
— attributed damage in a death round must equal the summed negative `UpdateHp` deltas —
ran **0 mismatches on 575 checked deaths** across this tape. The four scripts written for
this read (`mjanat.py`, `mjtrace.py`, `mjthrow.py`, `mjkid.py`, `mjcollar.py`) add only
aggregation, a positional per-round trace, and three raw `UpdateHp` passes off the same
`tools/replay_census` primitives.

**Population and denominators.** All numbers below are over these 30 local games unless
stated. This is a LOCAL deterministic fixture, so no platform DEFF applies (CLAUDE.md:
local pair-weighted DEFF 0.98); equally, n = 30 games / 19 losses supports **description,
not a bar**. Nothing here is offered as a currency read.

**Outcome split (reproduces the transfer read exactly):** US 7 wins (all core kills,
r144–356); THEM 23 (19 core kills + 4 of our r1000 survivals).
Loss classes as commissioned: **FAST** ≤ r140 = 5 (61, 88, 119, 136, 138) ·
**MID** r151–241 = 9 (150, 172, 177, 179, 181, 201, 216, 232, 240) ·
**SLOW** r385+ = 5 (385, 419, 456, 487, 520) · **R1000** = 4.

---

## 0. THE HEADLINE, AND IT CORRECTS THE TRANSFER READ

> **⛔ "The loss mode is the RACE" is not what this tape shows.**
> Reading their core's HP ledger at the moment ours died: **in 14 of the 19 lost games
> their core is at 500/500 or 498/500.** There was no race. In one game only
> (`midgard_A`, 80 HP left, linear ETA r98 vs our death at r88) were we within 20 rounds.
> The r184 median kill clock is the clock of the games we WIN; it does not describe the
> losses.
>
> **And their core healing is the reason.** Damage-dealt vs healed-back on THEIR core:
> in **14 of the 19 losses `healed == dealt` to the point** (auroraveil_A 342/342,
> bifrost_A 216/216, helheim_B 270/270, fimbulwinter_A 936/936, and all four r1000 games
> including `glacierkeep_A` **2104/2104** and `jotunheim_B` **2446/2446** — we dealt five
> cores' worth of damage there and every single point was healed back). The 5 losses where
> it is NOT exact are precisely the 5 where their core was not at full HP when we died
> (midgard_A net 420, valkyrie_A 198, paths_A 152, helheim_A 54, midgard_B 34). Meanwhile
> **in every one of the 7 wins `dealt − healed` = 500–512, i.e. exactly one core.**
> **We win iff we out-deal their heal by one core; we lose by not out-dealing it at all.**
>
> **Meanwhile our own core is not healed at all.** `SK_CORE_MEDIC = False`
> (`bots/_v612skalman/sk_maps.py:1009`, "BUILT, MEASURED, AND SHIPPED OFF"). Our core
> received **0 heal HP in 10 of the 19 losses** and ≤ 4 HP in 11 of 19, while taking a
> flat 504.

---

## 1. THE KILL CHANNEL — per lost game, by loss class

### 1.1 The channel is unmixed

**19 of 19 losses: 100.0% SENTINEL.** Zero gunner damage, zero peck damage, zero
launcher/unattributed damage on our core in any lost game — and the same in the 4 wins
where our core took damage. There is no "mixed" row and the classifier's other buckets
never fire on this tape. Modal total is exactly **504 = 28 × 18**, i.e. 28 sentinel shots
(11 of 19 losses read exactly 504; the rest read higher only because our generic
`_heal_action` returned some HP).

### 1.2 Geometry — it is a POINT-BLANK APRON, not a forward nest and not a gunner annulus

48 enemy turrets across the 30 games ever landed damage on our core. Their d² to our core
**footprint**:

| d² | 2 | 4 | 5 | 8 | 9 | 13 | 16 | 18 | 25 | 32 |
|---|---|---|---|---|---|---|---|---|---|---|
| n | 4 | 13 | 11 | 1 | 3 | 1 | 2 | 2 | 6 | 5 |

**28 of 48 (58.3%) sit at d² ≤ 5 — inside our own core's second ring.** 29 of 48 at
d² ≤ 8. Only 15 of 48 at d² ≥ 14. A sentinel reaches r² ≤ 32 and ignores obstacles, so it
does not *need* to be at d² 4; it comes that close because the seat is free and because
its escort has already walled the approach.

**Fate of those 48 shooters: 36 SURVIVED to the end of their game (75%).** 6 died to our
peck, 6 to our gunner. We essentially never remove the thing that kills us.

Mirror asymmetry, same census both directions: **enemy turrets planted at d² ≤ 8 of OUR
core = 63 over 30 games; OUR turrets planted at d² ≤ 8 of THEIR core = 0, in every game.**

### 1.3 Table by loss class

Counts are ENTITY-level (a tile can host successive turrets); n = 48 shooters over 30 games.

| class | n games | first core dmg, median (range) | modal killer d² | shooters/game | shooters that survived | our core heal = 0 |
|---|---|---|---|---|---|---|
| **FAST** ≤r140 | 5 | **r43** (15–93) | **4** | 2.0 (10) | **9 of 10** | 4 of 5 |
| **MID** r151–241 | 9 | **r95** (8–205) | **4** | 2.4 (22) | **16 of 22** | 3 of 9 |
| **SLOW** r385+ | 5 | **r358** (231–441) | **5** | 2.0 (10) | **7 of 10** | 3 of 5 |
| **R1000** | 4 | — (no core damage at all) | — | 0.0 (0) | — | 4 of 4 |
| *(WIN, for contrast)* | 7 | r98.5 (9–128) | 4 / 25 | 0.9 (6) | 4 of 6 | 6 of 7 |

Per-game shooter detail (tile · d² · plant round · shots · damage) is in
`mjanat.json → shooters`. Median plant round of a core-shooter is **r100.5** (min r5,
max r440); median plant → first-shot latency **9 rounds** — they wait on `convert_ammo`,
and that latency is a free window (see §6 candidate 3). *Caveat on the latency figure: it
is computed per shooter TILE, so a tile reused by a second turret can read a negative
value; the median is robust, individual extremes are not.*

### 1.4 The mechanism, named from their own tree

An independent source read of `bots/_x3r0v168mjolnir/` (file:line cited there) names each
piece, and every one of them is visible on the wire in this tape:

| their name | module:function | what it does to us | wire evidence here |
|---|---|---|---|
| **FERRY** (`_cg_ferry_try` / `_cg_ferry_launch`, `raid.py:4360,4698`) | r2–r80 | throws its own raider forward launcher-to-launcher | 246 throws of their bots, 186 attributed to a friendly launcher at d²≤2. `midgard_B` chains (4,3)→(8,7)→(11,12)→(15,16)→(19,20)→(23,24) at r2,4,6,8,10 — **24 tiles in 10 rounds** |
| **COLLAR** (`_collar_act`, `raid.py:2088-2330`) | seal our 12 core-ring tiles with barriers | denies our spawns AND the peck seat next to their sentinel | **224 enemy buildings placed on our core lap** over 30 games, first placement median **r11** (range 6–131), peak simultaneous occupancy **≥7 of 12 tiles in 22 of 30 games** (max 12); we removed **14 of 224** |
| **OPEN PAIR** (`opening._op_pair`, `opening.py:761-843`, `OPEN_PAIR_EARLIEST/DEADLINE = 5/7`, `OPEN_PAIR_MAX_DSQ = 36`) | band-A maps only | two sentinels at d ≤ 6 of our core by r7 | fires in **6 of 30** games (sentinel at d²≤36 born ≤r10: stavkirke_A r5, skald_A r5, stavkirke_B r6, skald_B r6+r7, helheim_A r7, helheim_B r7). Only `skald_B` gets the full pair by r7 |
| **SIEGE TUBE** (`_try_forward_sentinel`, `raid.py:1173-1410`; band 2.5–5.7 tiles, cap 3, `TUBE_REPLACE_ON`) | the main channel | the d²=4/5 sentinels | the modal killer; median plant r100 |
| **CAGE timeout** (`_cg_hold`, `CAGE_SEQ_TIMEOUT = 150`) | core fire is muted until seal ≥6, unconditionally released at r151 | explains the MID cluster | `auroraveil_A` first core damage r150 exactly; `skald_A` shooter planted r126, first shot r155; `stavkirke_A` shooter planted r103, first shot r125 |
| **PLUCK / kidnap** (`_tw_launcher`, `raid.py:3127-3252`) | throw our builder to the farthest legal tile | evicts our counter-peck marcher | **1,153 of our builder bots thrown across 30 games** (see §2.3) |
| **SAP** (`main.py:3469-3524`, `SAP_BAND_DSQ = 64`) | their bodies melee our forward turrets | kills our tubes | **21 of our 80 forward turrets died to `peck`** |
| **END quit** (`eco._end_fired`, r≥700 + 200 stalled rounds) | stops the siege permanently | the 4 r1000 games | see §4 |

> **The composite: FERRY (r2–10) → COLLAR (r6–46) → point-blank SENTINEL at d²2–5 planted
> inside the collar (median r100, as early as r5) → ~28 shots → dead.** In `helheim_B` the
> sequence is explicit on the wire: our conveyor at (14,6) is destroyed at r56 and **their
> sentinel is built on that same freed tile at r58.**

---

## 2. THE HOME ANSWER UNDER THEIR PROFILE

### 2.1 The gate arms. It arms in every single loss, on time.

`SK_COUNTER_HP_MAX = 450` (`sk_maps.py:1173`). Measured arming round vs first core damage,
all 19 losses: the gate arms at **first_dmg + 3 or + 4 rounds**, without exception
(500 → 446 after 3 sentinel shots). In the FAST class: `midgard_B` dmg r15 / gate r18 /
death r61 — **43 armed rounds**; `helheim_B` r86/r90/r119 — 29 armed rounds; `bifrost_B`
r93/r96/r138 — 42 armed rounds. **The gate is not the constraint and removing it buys
3 rounds.**

### 2.2 The targeting fence is not the constraint either

`SK_COUNTER_PECK_DSQ = 100` and the `_core_ray_shooter` third rung accepts any sentinel
whose reach (r² ≤ 32) covers a core tile. **All 48 observed shooters sit at d² ≤ 32**, so
every one of them is inside both the fence and the reach rung. **The premise in the task —
"tuned to a sentinel-at-d²≤25 profile their killer does not match" — is FALSIFIED on this
tape.** Their killer matches the profile precisely; it is *closer* than the plank expects,
not further.

### 2.3 What actually defeats it: the seat is taken, and the marcher is thrown off it

**Pecks landing on a tile that has shot our core, per game (19 losses):**
0 in 7 games · 1–8 in 6 games · 11–47 in 6 games. **Peck-kills of a core-shooter: 0 in 13
of 19 losses, 1 in 5, 2 in 1.** Across the whole tape we dealt **1,053 HP** to core-shooter
turrets and they healed **450 HP** back (22 of the 48 shooters received at least one heal).
48 sentinels is 1,920 HP; net 603 delivered, spread across 48 targets, killed 12.

Two named blockers, both measured:

1. **THEIR LAUNCHER PLUCKS OUR MARCHER.** Every one of our builder-bot throws in this tape
   is an enemy kidnap: **1,153 of 1,153**. This is degenerate by construction —
   `SK_HOME_LAUNCHER = False`, so **we build 0 launchers in 30 games against their 118** —
   and the classifier is disclosed as such. *(Two-way control: the same adjacency
   predicate run over THEIR 246 thrown bots attributes 186 to a friendly launcher and 0
   cross-team, so the predicate does discriminate; 60 of theirs are unattributed, a 24%
   limitation of adjacency attribution that does not touch our side's 100%.)*
   In `midgard_B` the pluck is metronomic: their launcher at (24,24) sits orthogonally
   adjacent to their sentinel at (23,23), and our marcher standing at (23,24) is thrown to
   (20,21) at **r15, 21, 27, 33, 39, 45, 51, 57** — every 6 rounds, from the exact seat the
   counter-peck needs, until we die at r61. Same signature in `icefloe_B` (91 plucks off a
   shooter seat) and `fimbulwinter_A` (13).
2. **THEIR COLLAR TAKES THE SEAT.** Peak enemy occupancy of our own 12 core-lap tiles is
   **≥7 of 12 in 22 of 30 games** (max 12), first placement median r11, and we removed only
   **14 of the 224** placements. A barrier on the tile
   orthogonally adjacent to their sentinel means there is no legal seat to peck from.
   `stavkirke_B` r8–r12: barriers at (11,18), (10,17), (8,19) — (10,17) is directly under
   the sentinel at (10,16). Our single peck lands at r8; there is never another, and the
   game runs to r136.

### 2.4 Unanswered-fire streaks (longest run of rounds after first hit with no heal, no
peck on a shooter tile, no shot on a shooter tile)

| class | longest unanswered streak per game |
|---|---|
| FAST | 46, 46, 12, **115**, 22 |
| MID | 26, 14, 23, 8, 14, 20, **1**, 19, 4 |
| SLOW | 37, 6, 1, 3, **118** |
| WIN | 2, 0, 64, 0, 10, 14, 0 |

`stavkirke_B` is the pure case: first hit r22, death r136, **115 consecutive unanswered
rounds** — one peck in the whole game, at r8, before the shooting started.

---

## 3. THE EARLY WINDOW — three of the five FAST games, round by round

### 3.1 `midgard_B` — 30×30, cores 24 tiles apart (d²=1152), dead **r61**

| round | event |
|---|---|
| r2, 4, 6, 8, 10 | THEIR ferry: bot3 thrown (4,3)→(8,7)→(11,12)→(15,16)→(19,20)→(23,24). **24 tiles in 10 rounds, 5 launcher hops** |
| r11 | THEY build launcher@(24,24), **d²=8 of our core** |
| r11–12 | WE build gunner@(27,22) d²=16 and gunner@(26,21) d²=25 — gunner reach is r²≤13, so **neither can ever reach (23,23) or (24,26)** |
| r12 | THEY build **sentinel@(23,23) d²=18**; ferry bot thrown (23,24)→(25,26), d²=1 |
| r13 | THEY build barrier@(25,27), d²=1 — collar |
| r14 | THEY build **sentinel@(24,26) d²=4** |
| **r15** | **first shot on our core.** Same round, their launcher plucks our bot9 off (23,24) |
| r15–57 | pluck repeats at r21, 27, 33, 39, 45, 51, 57. **1 peck lands all game** |
| r55 | our first forward sentinel (S1) is built — **40 rounds after their first shot**. No S2 ever |
| r61 | our core dies. **Their core: 466/500** |

**What had to hold:** at r14 the two sentinels are 9 + 9 = 18 HP/round nominal (11 HP/round
observed). Our linear ETA on their core is r746. Twenty more rounds of survival buys
nothing here — this game is not close. The only lever that changes the outcome is
**denying or removing the seat at (24,26)/(23,23) before r14**, or occupying the pluck seat
with a body that cannot be thrown (a building).

### 3.2 `stavkirke_B` — 22×22, cores 16 apart (d²=256), dead **r136**

| round | event |
|---|---|
| r2, r4 | ferry: (10,4)→(11,10)→(11,16). **16 tiles in 4 rounds, 2 hops** |
| r5 | THEY build launcher@(12,16) d²=8 |
| **r6** | THEY build **sentinel@(10,16), d²=4** — at round SIX (OPEN PAIR band A) |
| r8–12 | collar: barriers at (11,18), (10,17), (8,19) — all d²=1, and (10,17) is the peck seat under the sentinel |
| r8 | **our only peck of the entire game** lands on the sentinel |
| r15 | our S1 built (outside the 50-d² siege band; `ourMaxTubes` = **0** all game) |
| r22 | first shot (16 rounds after the plant — ammo latency) |
| r32–33 | THEY extend the collar to (9,17), (8,18) |
| r136 | our core dies, **their core 500/500 — we never damaged it once** |

**What had to hold:** the tile (10,16) had to be unavailable at r6, or the sentinel had to
take 40 HP of peck between r6 and r22 (its 16-round idle window, 20 builder-turns of peck =
2 bodies for 10 rounds, which we had). Nothing about 20 extra rounds of core HP helps: our
tube count never reaches 1 in the siege band.

### 3.3 `helheim_B` — 18×18, cores 12 apart (d²=144), dead **r119**

| round | event |
|---|---|
| r7 | THEIR first sentinel at d²=29 of our core (band-A opening, only one of the pair) |
| r18–46 | **collar**: barriers at (13,9), (14,10), (13,8), (16,8), (13,7), (16,7), (15,7), (16,10) — **10 lap placements, peak 10 of 12 tiles held at r86** |
| r24 | THEY build launcher@(13,10), **d²=2** |
| r25, 37, 64 | ferry drops a raider at d²=1 of our core, three times |
| r15 / r48 | our S1 / S2 forward sentinels — **we do get 2 tubes standing at r48** |
| r46, 56, 65 | our conveyors at (15,7), (14,6), (14,7) are destroyed — the collar chewing our belt |
| **r58** | THEY build **sentinel@(14,6), d²=4 — on the tile our conveyor died on at r56** |
| r85, r98 | two more sentinels at d²=9 and d²=4 |
| r86 | first shot; r119 our core dies, **their core 500/500** |

**What had to hold:** this is the clearest statement of the requirement. **Passive apron
occupancy is not enough — they destroy the occupant and build on the freed tile two rounds
later.** The apron has to be *held*, i.e. relaid or defended, and our belt tiles at d²≤5
are exactly the tiles they convert into firing seats.

**The general "20 more rounds" answer:** in 14 of 19 losses their core is at full HP when
we die, so buying our core 20 rounds buys nothing. **The early-window work that pays is not
core HP, it is seat denial at d²≤5 and killing the shooter inside its 9-round ammo
latency.**

---

## 4. THE COMPLEMENT — our 4 r1000 survivals

`glacierkeep_A`, `jotunheim_B`, `longhouse_A`, `longhouse_B`.

**One column separates them perfectly: enemy sentinels ever planted within d² ≤ 36 of our
core = 0, in all four.** Our core took **0 damage** in all four games. Compare: all 19
losses have ≥ 1, and 5 of the 7 wins do too.

It is **not** map class (glacierkeep_A survives while glacierkeep_B dies at r232 on the
same map, other seat) and it is **not** our cage. Two things co-occur:

* **Their FERRY still arrives** (glacierkeep_A: 106 ferry throws, arrival at r6;
  jotunheim_B: 6, r6) and **their COLLAR still lands** (9 lap buildings each, peak 8–9).
  What never happens is the sentinel. Their siege gate is `LOKI_FWD_MIN_HARV = 2`
  harvesters + `LOKI_FWD_TI_FLOOR = 40` bank; on these maps their raider never converts.
* **We out-attrit them without out-killing them.** We dealt 2,104 (glacierkeep_A) and
  2,446 (jotunheim_B) damage to their core — and **100% of it was healed**. `longhouse_A`:
  we removed 26 of our own placements from their lap being killed, our forward sentinels
  died at r152/r725. Their **END plank** (`eco._end_fired`, r ≥ 700 + 200 stalled rounds)
  then latches and they stop attacking altogether.

**What this tells us:** the thing that already works is **stopping the plant**, not
absorbing the fire. Where their sentinel never gets a seat, our core takes literally zero
damage — the collar and the ferry alone do nothing.

---

## 5. THE 7 WINS — what they share

| game | map | cores d² | our kill | max tubes standing | round 2 tubes stood | their near-sentinels | dealt − healed on their core |
|---|---|---|---|---|---|---|---|
| valkyrie_B | 30×30 | 576 | r144 | 2 | r56 | 2 (r59) | 1296 − 784 = 512 |
| skald_B | 16×16 | 144 | r160 | 3 | **r27** | 4 (r6 — full OPEN PAIR) | 810 − 306 = 504 |
| holmgang_B | 12×12 | 128 | r170 | 2 | **r17** | 1 (r76) | 2304 − 1804 = 500 |
| fimbulwinter_B | 20×20 | 452 | r183 | 2 | r62 | 2 (r119) | 846 − 336 = 510 |
| jotunheim_A | 24×24 | 338 | r247 | 1 | never | **0** | 1116 − 616 = 500 |
| yggdrasil_A | 30×30 | 882 | r264 | 3 | r77 | **0** | 1908 − 1408 = 500 |
| holmgang_A | 12×12 | 98 | r356 | 2 | **r21** | 3 (r38, killed r61) | 1656 − 1154 = 502 |

**Three shared facts, and none of them is map size** (12×12 through 30×30 all appear):

1. **`dealt − healed` = 500–512 in every win, and 0–54 in 14 of 19 losses.** The win
   condition on this opponent is *sustained* DPS above their heal rate, not peak damage.
2. **TWO TUBES STANDING SIMULTANEOUSLY.** 6 of 7 wins reach 2+ simultaneous forward turrets
   (the exception, `jotunheim_A`, faced zero enemy near-sentinels). Median round at which
   the second tube stands in wins: **r56**; in the FAST losses: r43–r49 where it happens at
   all, and **never** in `midgard_B`, `stavkirke_B`, `paths_B`. This is the same arithmetic
   Mjolnir's own doctrine states about itself (`DOCTRINE.md:1543-1553`: *"14 + 14 = 28 =
   ceil(500/18) = exactly one core. A tube that stands alone is not half a kill; it is a
   donation."*).
3. **Our tubes SURVIVE.** In 4 of 7 wins no forward turret of ours died; across the whole
   tape 21 of our 80 forward turrets died to SAP pecks and 18 to their sentinels.

---

## 6. RANKED v613 CANDIDATE LIST — early-window defence, **no launcher dependency**

Each candidate names the measured fact it answers and the falsifier that would kill it.

### 1. **APRON DENIAL — hold d² ≤ 5 around our own core** ⭐ highest measured leverage
**Fact:** 28 of 48 enemy core-shooters (58.3%) sit at d² ≤ 5; 29 of 48 at d² ≤ 8; our
core's second ring is 28 tiles and they walk into it unopposed at median r100 and as early
as r5. **Their own tree already does this to itself** (`ring.py` RING-CLAIM: plug your own
core sockets with your own conveyors, unconditional floor of 2 by r20).
**Plank:** claim the d²≤5 apron with our own cheapest buildings (barrier 3 Ti / conveyor
3 Ti), floor of N tiles by round R, prioritising tiles on the core-to-enemy axis.
**⛔ The `helheim_B` caveat is load-bearing:** they destroy the occupant and build on the
freed tile two rounds later, so the plank must include **relay on loss**, not one-shot
placement. A static seal is refuted in advance by r56→r58 on that game.
**Falsifier:** enemy core-shooters at d²≤5 do not fall below the control's 28/48 share, or
timely-kill rate by r300 regresses (`DEFENCE_ADMISSION_BAR`).

### 2. **SECOND TUBE AS A HARD FLOOR — never siege with one**
**Fact:** 6 of 7 wins reach 2 simultaneous forward turrets (median r56); 8 of 19 losses
never reach 2 at all, and `paths_B`/`stavkirke_B` never reach 1 in the siege band.
`dealt − healed` is 500–512 in every win and 0 in 14 of 19 losses — one tube's 9 HP/round
loses to their heal seats, two tubes' 18 HP/round does not.
**Plank:** gate the FIRST tube on affordability of the SECOND (their `PAIR_MIN = 2` in
mirror image); prefer holding the bank to standing one tube alone.
**Falsifier:** the 2-tube share does not rise, or median kill round crosses r300.

### 3. **PECK CONCENTRATION + relax the heal-trend veto on a POINT-BLANK shooter**
**Fact:** we delivered 1,053 HP into 48 shooter turrets and they healed 450 back; net 603 =
15 sentinels' worth, but spread over 48 targets it killed 12. Peck-kills are 0 in 13 of 19
losses. The ledger-V7 `hp_trend_ok` veto refuses to peck a target being healed faster —
correct in general, but a d²≤5 sentinel is worth committing 2–3 bodies to regardless.
**Plank:** when the published shooter is at d² ≤ 8 of our core, commit ALL idle bodies to
that one tile and suspend the heal-trend veto (or raise its threshold by the number of
committed bodies: 3 pecks = 6 HP/round beats one healer's +4).
**Falsifier:** peck-kills of core-shooters do not rise above 12/48; or drip/lattice
regresses (this spends the same bodies).

### 4. **DENY THE PLUCK SEAT — prefer peck seats not adjacent to an enemy launcher**
**Fact:** 1,153 of our builder bots were thrown in 30 games (all by their launchers; we
build none). In `midgard_B` the same body is thrown off the same seat at r15, 21, 27, 33,
39, 45, 51, 57 — every 6 rounds, from the only seat that reaches the sentinel.
**Plank:** in `_counter_march`'s seat choice, rank candidate adjacent tiles by
`min d² to any live enemy launcher` and take the farthest legal one; if all four adjacent
tiles are inside a launcher's d²≤2 pickup disc, peck the **launcher** first (30 HP =
15 pecks) — killing it un-plucks every future marcher.
**Falsifier:** plucks-off-a-shooter-seat do not fall; or the detour costs more turns than
the plucks did.

### 5. **RE-EXAMINE `SK_CORE_MEDIC = False` under THIS opponent's profile**
**Fact:** our core is healed 0 HP in 10 of 19 losses; theirs absorbs 100% of everything we
deal. The plank's own docstring prices it honestly ("a losing race ALONE"). **This is
ranked 5th and NOT 1st on purpose** — in 14 of 19 losses their core is at full HP when ours
dies, so buying our core rounds buys nothing unless a kill plank is already landing.
**Plank:** re-arm the medic only when our own tube count ≥ 2 (i.e. only when the extra
rounds are convertible), which makes it a *rider* on candidate 2 rather than a standalone.
**Falsifier:** median rounds-from-first-hit-to-death rises without the by-r300 kill share
rising with it — that is buying survival at the kill's expense and is off-programme.

### 6. **GUNNER SITING AUDIT — our home gunners cannot reach the killer**
**Fact:** `midgard_B` r11–12 places gunners at d² 16 and 25 of our own core while the
killers land at d² 18 and 4; gunner reach is r² ≤ 13 along a facing ray, so neither gunner
could ever fire at either sentinel. Across the tape only 6 of 48 shooters died to our
gunner. **Cheap correctness fix, low ceiling** — a gunner that covers the apron is 20 Ti,
but a sentinel outranges it 32 vs 13 and will simply sit at d²=25.
**Falsifier:** gunner-attributed shooter kills do not rise above 6/48.

**Explicitly NOT recommended:** widening `SK_COUNTER_PECK_DSQ` (already 100, never binds),
lowering `SK_COUNTER_HP_MAX` below 450 (arms at first_dmg+3 in 19 of 19; the ceiling is
worth 3 rounds), and anything requiring `SK_HOME_LAUNCHER` (excluded by the brief, and
their launcher is the *symptom* — the seat is the disease).

---

## Files

* This report: `/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/86e927e3-fb77-4d74-bdfe-69717bb9a2ae/scratchpad/tapemj_anatomy.md`
* Instruments (all read-only, all in the same scratchpad dir): `mjanat.py` + `mjanat.json`
  (master anatomy), `mjtrace.py` (round-by-round positional trace),
  `mjthrow.py` + `mjthrow.json` (ferry/kidnap census), `mjkid.py` + `mjkid.json`
  (kidnap attribution + two-way control), `mjcollar.py` + `mjcollar.json` (collar census,
  mirrored control), `mjband.json` (band-A signature, our tube attrition).
* Decoder of record: `scratchpad/s54_autopsy/tape30_deaths.py` (0 mismatches / 575 checked).
