# Thread 3 — kladde v62 fresh decode → probe-refresh spec

**Date:** 2026-08-07 · **Analyst:** read-only replay thread · **Target:** `kladde chatte tville (och oss)`
team id `c7571c87-f960-4c88-a13d-14340bb3200f`, rating 1798–1821 across the v62 window.

**Deliverable:** the exact behaviours a frozen `bots/kladde_probe_v2` must reproduce, plus where v62 is
harsher/softer than the live `bots/kladde_probe` (frozen from match `36f5e137` g1/g5, kladde @1718 ≈ v56 era).

Every claim below carries `matchid8 gN` ids. Raw decodes: `SCRATCH/dec_a.txt`, `dec_b.txt`, `dec_c.txt`,
`pass2/3/4/5.py`. All replays are in the shared cache `SCRATCH/replay_cache/replays/`.

---

## 0. When v62 went live, and the sample

From `SCRATCH/replay_cache/team_kladde.json` (last 100 ladder series, `teamAVersion`/`teamBVersion`):

| version | first seen (UTC) | last seen | n series |
| --- | --- | --- | --- |
| v56 | 2026-08-06T17:42:43 | 19:42:43 | 13 |
| v57 | 19:52:43 | 21:12:43 | 9 |
| v58 | 21:22:43 | 23:22:43 | 13 |
| v59 | 23:32:43 | 2026-08-07T06:02:43 | 40 |
| v60 | 06:12:43 | 06:32:43 | 3 |
| v61 | 06:42:43 | 09:02:43 | 15 |
| **v62** | **2026-08-07T09:12:43** | 10:12:43 (cache edge) | **7** |

**v62 went live 2026-08-07 09:12 UTC.** Exactly 7 v62 series exist in the window and all 7 are complete,
so the sample below is the *entire* v62 ladder record, not a selection:

| match | opp | opp Elo | result | maps |
| --- | --- | --- | --- | --- |
| `225f2360` | Erebus v49 | 1812 | kladde **W 3-2** | atoll, meander, drumlin, moonrise, jackpot |
| `665d1208` | Banminary v39 | 1749 | kladde **W 4-1** | nordkap, lighthouse, drumlin, saga, snowflake |
| `69a0c821` | not adgato v15 | 1917 | kladde **L 1-4** | eider, nordkap, antler, hive, lighthouse |
| `4ece8a7a` | The Flotte Experience v35 | 1904 | kladde **L 2-3** | fjordgate, moonrise, hive, archipelago, lighthouse |
| `31c83aff` | Besvikomat v16 | 1790 | kladde **L 0-5** | moonrise, atoll, archipelago, antler, drumlin |
| `c23600fc` | Landers v62 | 1683 | kladde **W 3-2** | fjordgate, nordkap, eider, heart, meander |
| `73624f1b` | O(1) v8 | 1729 | kladde **W 3-2** | saga, drumlin, nordkap, fjordgate, lighthouse |

None involve OpenSverige (we never face them rated), as required.

### Games decoded

**v62 (6 games, 5 opponents, 3 W / 3 L):**

| # | replay id | game | map | seed | rounds | kladde side | result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `225f2360-c7fc-4486-9f87-80923d480530` | g5 | **jackpot** | 2032336915 | 1000 | B | **W** (titanium_collected) |
| 2 | `225f2360-c7fc-4486-9f87-80923d480530` | g2 | **meander** | 1001816144 | 247 | B | **W** (core_destroyed) |
| 3 | `c23600fc-79e6-477b-afde-ceb4062ca48d` | g3 | **eider** | 1446722484 | 480 | A | **W** (core_destroyed) |
| 4 | `c23600fc-79e6-477b-afde-ceb4062ca48d` | g5 | **meander** | 570830940 | 989 | A | **L** (core_destroyed) |
| 5 | `69a0c821-9487-43bc-a3dd-8e4f6a88da34` | g4 | **hive** | 593543234 | 674 | A | **L** (core_destroyed) |
| 6 | `31c83aff-1223-4c3b-b720-25c837409a0d` | g5 | **drumlin** | 1967968115 | 936 | A | **L** (core_destroyed) |
| + | `73624f1b-4c04-4eb8-9353-77e60096550e` | g1 | **saga** | 1935768979 | 352 | A | **W** (core_destroyed) |

**Baselines for the DIFF** — the probe's literal freeze source (`36f5e137`) is not recoverable (it appears
nowhere in `our_ladder_all.json` or any cache; only the docstring cites it), so the closest available
baseline is v56, whose rating band 1703–1733 brackets the docstring's "1718-rated":

| replay id | game | map | rounds | result | version |
| --- | --- | --- | --- | --- | --- |
| `691f2554-3e2e-4320-a55d-2c7d99c06eb3` | g1 | meander | 268 | W | **v56** |
| `691f2554-3e2e-4320-a55d-2c7d99c06eb3` | g3 | hive | 283 | L | **v56** |
| `691f2554-3e2e-4320-a55d-2c7d99c06eb3` | g5 | eider | 315 | L | **v56** |
| `f0c33e9e-2551-40cf-a730-a30acbef2297` | g1 | jackpot | 440 | W | **v61** |

Same three map names as the v62 picks, so the diff is like-for-like.

---

## 1. Master table (11 games, v56 / v61 / v62)

`cc_d2` = core-to-core distance²; `fwd1` = round of the first turret built **forward** (d²≤45 of the enemy
core AND closer to the enemy core than to its own); `hCore%` = share of heals spent on kladde's own core.

| game | cc_d2 | 1stHarv | 1stConv | 1stGun | 1stSent | fwd1 | fwdD2 | nSent | nGun | bots | harv | conv | heals | hCore% | ammoConvN | ammoTot |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| v62 meander W `225f2360 g2` | 49 | 28 | 1 | 177 | **3** | 3 | 16 | 4 | 2 | 7 | 14 | 59 | 53 | 62% | 96 | 1600 |
| v62 jackpot W `225f2360 g5` | 392 | 6 | 2 | 11 | 92 | **186** | 25 | **68** | 3 | 24 | 8 | 47 | 833 | 23% | 443 | 5336 |
| v62 eider W `c23600fc g3` | 144 | 7 | 1 | 25 | 16 | **235** | 41 | 15 | 1 | 9 | 19 | 94 | 521 | 69% | 187 | 2644 |
| v62 meander L `c23600fc g5` | 49 | 10 | 2 | 220 | 284 | — | — | 2 | 6 | 10 | 10 | 90 | 1096 | 88% | 143 | 894 |
| v62 hive L `69a0c821 g4` | 650 | 7 | 1 | 38 | 67 | **never** | — | 4 | 6 | 10 | 4 | 24 | 956 | **97%** | 94 | 484 |
| v62 drumlin L `31c83aff g5` | 338 | 9 | 1 | 26 | 314 | **314** | 25 | 1 | 6 | **69** | 24 | 250 | 224 | 35% | 69 | 662 |
| v62 saga W `73624f1b g1` | 392 | 11 | 1 | 81 | 120 | **173** | 45 | 7 | 3 | 9 | 14 | 68 | 4 | 0% | 139 | 1736 |
| v61 jackpot W `f0c33e9e g1` | 392 | 6 | 2 | 11 | 99 | **137** | 16 | 5 | 3 | 17 | 6 | 34 | 57 | 80% | 182 | 1908 |
| v56 meander W `691f2554 g1` | 49 | 13 | 1 | 28 | **3** | 260 | 1 | 11 | 4 | 6 | 13 | 62 | 170 | 84% | 105 | 1564 |
| v56 hive L `691f2554 g3` | 650 | 8 | 2 | 54 | 122 | **never** | — | 7 | 2 | 5 | 5 | 55 | 144 | 84% | 21 | 520 |
| v56 eider L `691f2554 g5` | 144 | 7 | 2 | 10 | 44 | 133 | 34 | 8 | 2 | 6 | 21 | 92 | 141 | 69% | 66 | 868 |

---

## 2. What kladde v62 actually does

### 2.1 Opening — identical in v56 and v62, and it is NOT the probe's opening

Every game, both versions, without exception:

- **r0, r1, r2: three builders**, one per round, on tiles adjacent to the core. (`225f2360 g5`,
  `c23600fc g3`, `69a0c821 g4`, `31c83aff g5`, `73624f1b g1`, `691f2554 g1/g3/g5`.)
- **First conveyor lands r1–r2**, *before* the first harvester, always. The chain is laid **outward from
  the core toward the ore**, one conveyor every ~2 rounds, and the harvester is planted at the far end when
  the chain arrives. Example `c23600fc g3` (eider): `r1 conv(7,8) · r3 conv(7,7) · r5 conv(7,6) · r7 harv(6,6)`.
- **First harvester r6–r13** on every map except close-core meander (r28 in `225f2360 g2`, because the
  three opening builders were spent on turrets instead — see §2.2).
- **No splitters, no barriers, no launchers. Ever.** Zero across all 11 games, both versions
  (`pass4.py` output). kladde's entire vocabulary is: core, builder, harvester, conveyor, gunner, sentinel.

### 2.2 Map conditional: close cores ⇒ immediate sentinel rush at r3

On meander, core-to-core d² = 49 (7 tiles). Both v56 and v62 respond identically and instantly:

- `225f2360 g2` (v62): **sentinel at r3** (11,8) facing NORTH, sentinel r8 (12,8), sentinel r9 (13,9).
  **150 titanium converted to ammo at r4** in one shot. First shot at the enemy core **r4**. First
  harvester not until **r28**. Enemy core dead r246.
- `691f2554 g1` (v56): **sentinel at r3** (11,7) facing NORTH. **150 ammo converted at r4.** First shot
  at the enemy core **r4**. Enemy core dead r267.

This is a real, reproducible behaviour and it is **not in the current probe at all** — the probe's earliest
turret is gated by `EARLY_TURRET_ROUND = 150`.

The negative control is `c23600fc g5` (v62 meander, same 25x15 geometry, cores mirrored, kladde on side A):
kladde's first gunner is **r220** and first sentinel **r284**. The reason is visible in the replay — the
opponent (Landers) built the sentinel on that contested tile first, at **r6** at (11,8), and was hitting
kladde's core from **r7**. kladde lost the race for the rush tile and never recovered (core dead r988).
So the trigger is geometric-and-contested, not unconditional.

### 2.3 The home ring: 2 gunners early, then sentinels

- **Two gunners, back to back, at r10–r42** on every non-close-core map, planted at d²own ∈ {4,5,9,10}:
  hive r38+r39 `69a0c821 g4`; drumlin r26+r27 `31c83aff g5`; jackpot r11+r42 `225f2360 g5`;
  eider r25 `c23600fc g3`; v56 eider r10+r11 `691f2554 g5`.
- **Then sentinels only**, from r67–r120, filling a ring at **d²own = 1–13** (`pass2.py` home-ring block).
  Sentinels dominate the whole army thereafter: v62 eider 15 sentinels / 1 gunner; v62 saga 7/3;
  v62 jackpot 68/3.

### 2.4 The forward push — the core finding, and where the probe is wrong

**Trigger.** Across *all* 11 games and *all three* versions, the state at the round the first forward
turret goes up is startlingly tight (`pass5.py`):

| game | fwd1 | builders alive | harvesters | titanium | **ammo** | home turrets already up |
| --- | --- | --- | --- | --- | --- | --- |
| v62 jackpot | 186 | 6 | 8 | 392 | **240** | 10 |
| v62 eider | 235 | 6 | 9 | 443 | **260** | 10 |
| v62 drumlin | 314 | 5 | 7 | 201 | **150** | 5 |
| v62 saga | 173 | 6 | 13 | 216 | **150** | 5 |
| v61 jackpot | 137 | 6 | 5 | 193 | **150** | 4 |
| v56 eider | 133 | 5 | 9 | 154 | **236** | 7 |
| v56 meander | 260 | 5 | 12 | 1032 | **220** | 7 |

**Ammo ≥ 150 at fwd1 in 7 of 7 games.** 150 ammo = 15 sentinel shots. Builders are at their cap (5 in v56,
6 in v62). Home turrets ≥ 4. The probe's `STRIKE_ARMY_TRIGGER = 5` is a good match for the turret half of
this; the **ammo ≥ 150 gate is missing from the probe entirely** and is the single best predictor.

**Composition and stagger.** The wild plants forward turrets in **pairs, 1 round apart**, and then
**repeats**, rather than planting one 3-turret pack:

- `c23600fc g3` (eider): pair at **r235/r236** (d² 41, 45), then a second wave of **two pairs** at
  **r398/r399** and **r403/r404** (d² 25/29/25/41). Enemy core takes its first damage at **r399**,
  dies at **r479**. All four second-wave sentinels survive to the end.
- `73624f1b g1` (saga): r173 (d²45), r184 (d²25), r245 (d²25, dies r252), r271 (d²25). Core damage from
  **r185**, core dead r351.
- `225f2360 g2` (meander): the r3/r8/r9 rush sentinels *are* the forward turrets; a gunner pair is added
  at **r177/r181** at d² 9 and 5 to finish.
- `691f2554 g1` (v56 meander): a **3-turret pack at r260/r261/r264** at d² 1/5/9 — this is exactly the
  behaviour the current probe reproduces, and it is the **v56** shape.

**Facing.** Forward sentinels always face the cardinal/diagonal step toward the enemy core, i.e. the
line-shot is pre-aligned on the core: (6,1) WEST toward (0,0); (15,12)/(18,13) SOUTH toward (18,18);
(11,8) NORTH toward (11,3). `pass3.py`.

**Standoff distance.** Forward turrets sit at **d²enemy = 25 most often**, range 16–45. Never adjacent.
Sentinel range is r²=32, so d²25 is a comfortable in-range, out-of-melee standoff.

### 2.5 The sentinel treadmill — the biggest single change to model

`225f2360 g5` (jackpot, 1000 rounds) is the clearest case. From **r186 to r871**, kladde rebuilt a sentinel
on **the same tile (6,1)** — 58 times on that one tile, 68 sentinels built and **65 lost** in the game:

- **rebuild gap = 12 rounds** (54 of 60 gaps), **sentinel lifespan = 11 rounds** (54 of 60).
  It dies, and one round later the same tile has a new one.
- **Builder id 6 placed 58 of the 60 forward turrets** and camped there the whole time.
- **614 of the game's 833 heals went to forward sentinels** in the enemy's zone (d²enemy ≤ 45) —
  the camping builder heals the sentinel to stretch its life, then rebuilds it when it dies.

The same "keep one forward sentinel alive at all costs" logic exists in v61 (`f0c33e9e g1`: one sentinel at
(5,1) d²16 planted r137 that *never died*, ground the core from r142 to r439, 160 shots, core dead r439) —
so the *intent* predates v62; what v62 exposes is the **rebuild loop when the opponent can kill it**.

A probe must model this as **"a builder is assigned to the forward tile permanently: heal the turret every
turn it is damaged, rebuild it the round after it dies, forever"** — not as a one-shot strike.

### 2.6 Economic denial: builders chew, midfield sentinels snipe

- `c23600fc g3` (eider): **46 enemy harvesters destroyed**, first at r138, steady from r196 on.
  Source split: **206 builder-melee hits, 125 sentinel line-shot hits** on enemy harvesters/conveyors.
  The sentinel snipes come from a **midfield** turret at (11,12) (66 hits) — d²own only 13 — reaching into
  the enemy economy from near home because a sentinel's line shot ignores obstacles.
- `691f2554 g5` (v56 eider): econ damage was **100% builder-melee, 0 sentinel hits**. The midfield
  economic sniping is a **v56→v62 addition**.
- Raider volume is low and constant: **1–3 kladde builders across the midline at a time**
  (`pass2.py` raider windows), never a wave. `c23600fc g5` shows the ceiling: 887 builder econ hits over
  989 rounds from a trickle of 1–2 bodies.

### 2.7 Economy shape

- **Builder cap is hard: 6 alive in v62, 5 alive in v56** (`pass4.py` `maxBotsAlive`). Every v62 game
  except saga (7 once) peaks at exactly 6; every v56 game peaks at exactly 5. Losses are replaced to
  restore the cap — `31c83aff g5` spawned **69 builders and lost 67** while never exceeding 6 alive.
- **Harvesters 8–19 built, uncapped and still growing past r300** (eider 19 built by r480,
  drumlin 24 by r936). Conveyors 47–250 built.
- **Conveyor churn is the loss signature, not the plan**: healthy games lose ~0–14 conveyors
  (jackpot 0/47, saga 5/68, meander-W 1/59); lost games lose nearly all of them
  (drumlin 222/250, meander-L 80/90).
- **Late-game builder flood, low confidence (n=1):** `225f2360 g5` spawned 16 extra builders from
  **r800–r987**, taking alive from 6 to 20, spending a 1474-Ti bank down to 342. No extra harvesters were
  built with it. This is the only game in the sample that reached r1000 in good health, so treat as
  "possible surplus dump above ~r800", not established.

### 2.8 Ammunition policy

- **One bulk opening conversion**, then a drip. Opening chunk: **150** on the close-core rush maps
  (`225f2360 g2` r4; `691f2554 g1` r4) and on saga (`73624f1b g1` r60); **60** on eider/meander
  (`c23600fc g3` r17, `c23600fc g5` r12, `691f2554 g5` r11); **20** on far maps
  (`225f2360 g5` r12, `f0c33e9e g1` r12, `31c83aff g5` r27+r28, `69a0c821 g4` r39+r40).
- **Thereafter chunks of 10, continuously.** 10 is the modal chunk in every game:
  331/443 conversions on jackpot, 126/187 on eider, 113/139 on saga, 160/182 on v61 jackpot.
- **No ceiling.** Max ammo held: jackpot **1460**, eider 330, hive 240, saga 200. Ammo simply accumulates
  when the turrets are not spending it. The probe's `AMMO_CEILING = 220` is wrong for long games.

### 2.9 Healing is the defensive engine (and the solvency drain)

Heal volume tracks how hard kladde is being pressed, and the target follows the pressure:

- **Under siege, ~90% of heals go to their own core**: hive `69a0c821 g4` 956 heals / **97% core**;
  meander-L `c23600fc g5` 1096 heals / 88% core; v56 meander 170 / 84%.
- **When attacking, heals follow the forward sentinel**: jackpot `225f2360 g5` 833 heals, only 23% core,
  **614 on forward sentinels**.
- **When nothing is contested, heals are ~zero**: saga `73624f1b g1` 4 heals total.

At 1 Ti per heal this is a 1000-Ti-scale line item in a pressured game — the mechanism behind the known
"hive starves our solvency" finding, and kladde applies it to itself in exactly the same way.

### 2.10 Endgame

- **Win path is always the forward sentinel line grinding the core**, never a builder rush.
  Core damage sources: eider `c23600fc g3` 100% sentinel (79 shots, r399→r479); saga `73624f1b g1`
  100% sentinel (124 shots, r185→r351); jackpot v61 `f0c33e9e g1` 100% sentinel (160 shots, r142→r439).
  The only game with builder core damage is v56 meander (60 builder hits alongside 94 sentinel).
- **When the core will not fall, they settle for the tiebreaker.** `225f2360 g5`: enemy core repaired back
  to 500 despite 277 sentinel core hits; kladde won on `titanium_collected` **18800 vs 6310**.
- **Loss mode is economic, and starts early.** hive `69a0c821 g4`: 4 harvesters ever built, 3 lost, ended
  on 1; delivered 2980 vs 5810; enemy core **never touched once** in 674 rounds. drumlin `31c83aff g5`:
  one lone forward sentinel at r314 took the enemy core to 110 HP by r390, died r375, and was never
  replaced — 8830 vs 14360 delivered.

---

## 3. DIFF: v56 (probe's era) → v62

### Changed

| # | v56 (what the probe reproduces) | v62 (what it must reproduce) | evidence |
| --- | --- | --- | --- |
| 1 | **Builder cap 5 alive** | **Builder cap 6 alive**, losses replaced to restore it | `pass4.py`: v56 games max 5,5,5; v62 games max 6,6,6,6,6,7 |
| 2 | **One late strike pack of 3 turrets** at r260 (d² 1/5/9) | **Repeating waves of 2**, 1 round apart, from r137–r314, rebuilt indefinitely | `691f2554 g1` r260/261/264 vs `c23600fc g3` r235/236 then r398/399+r403/404; `73624f1b g1` r173/184/245/271 |
| 3 | Forward turret planted **once**; if it dies, that is that | **Camped and rebuilt on a 12-round cycle**, plus healed in place | `225f2360 g5`: 58 sentinels on tile (6,1), gap 12, lifespan 11, builder #6 placed all of them, 614 forward heals |
| 4 | Forward push at **r260** (meander) / r133 (eider) | Forward push at **r173–r235** on comparable maps; **r137** in v61 | fwd1 column §1 |
| 5 | Economic denial **100% builder-melee** | **Midfield sentinels snipe the enemy economy** (line shot ignores obstacles) from d²own≈13 | v56 eider `691f2554 g5` 78 builder / 0 sentinel; v62 eider `c23600fc g3` 206 builder / **125 sentinel**, shooter at (11,12) |
| 6 | Ammo bank tops out ~220–310 | **No ceiling**; banks to 1460 on a long game | max-ammo column, `pass5.py` |
| 7 | Enemy harvester kills modest | **46 enemy harvesters killed** in one game, sustained r196→r474 | `c23600fc g3` |

### Stayed the same

| # | behaviour | evidence |
| --- | --- | --- |
| 1 | 3 builders at r0/r1/r2, one per round | all 11 games |
| 2 | Conveyor **before** harvester (r1–r2 vs r6–r13); chain laid core→ore, ~1 conveyor / 2 rounds | all 11 games |
| 3 | **Close-core (d²≈49) ⇒ sentinel at r3 + 150 ammo at r4 + shooting the core by r4** | `691f2554 g1` (v56) ≡ `225f2360 g2` (v62), identical to the round |
| 4 | Two gunners at r10–r42 at d²own 4–10, then sentinels only | all non-close-core games |
| 5 | **Ammo ≥ 150 gate on the forward push** | 7/7 games across v56/v61/v62 |
| 6 | Never builds splitters, barriers or launchers | all 11 games |
| 7 | Heals follow the pressure; ~90% to own core when besieged | v56 84–84%, v62 88–97% |
| 8 | Loses hive the same way — no forward turret ever, economy starved, core never touched | `691f2554 g3` ≡ `69a0c821 g4` |
| 9 | Sentinel-led army; gunners are a small early minority | nSent/nGun column |

---

## 4. PROBE-REFRESH SPEC — `bots/kladde_probe_v2`

Numbers are the measured wild values. Where the wild varies, the range is given and the recommended
freeze value is **bold**.

### 4.1 Constants to change from the live probe

| probe constant | current | v62 measured | change |
| --- | --- | --- | --- |
| `MAX_BUILDERS_TOTAL` | 16 (runaway guard) | **6 alive**, hard | make it a *live-alive cap of 6*, not a cumulative guard; replace losses |
| `OPENING_BUILDERS` | 3 | 3, at r0/r1/r2 | keep |
| `EARLY_TURRET_ROUND` | 150 | 2 gunners at **r10–r42**; **r3 sentinel** if close-core | replace with §4.3 |
| `STRIKE_TURRETS` | 3 | **2 per wave**, waves repeat | 2 + repeat |
| `STRIKERS` | 2 | **1 camping builder** per forward tile | 1 camper + 1 relief |
| `STRIKE_FALLBACK_ROUND` | 450 | wild fwd1 = **137–314** | **250** |
| `STRIKE_ARMY_TRIGGER` | 5 | 4–10 home turrets at fwd1 | keep 5 |
| — (missing) | — | **ammo ≥ 150 at fwd1, 7/7 games** | **add `STRIKE_AMMO_MIN = 150`** |
| `AMMO_CHUNK` | 5 | modal chunk **10** (60–75% of conversions) | **10** |
| `AMMO_CEILING` | 220 | none observed; peaked 1460 | **remove the ceiling** |
| — (missing) | — | opening bulk conversion **20 / 60 / 150** at r4–r60 | **add**; 150 on the close-core branch |
| `MAX_HARVESTERS` | 16 | 8–24 built, still growing past r300 | **24** |
| `HARV_INTERVAL` | 15 | harvesters land r6–r13 then paced | keep 15 |
| `RAID_CONCURRENT` | 2 | **1–3 builders across the midline at any time** | keep 2 |
| `HOME_TURRET_MAX` | 8 | 4–11 home turrets | **11** |
| `HOME_MIN_SQ`/`HOME_MAX_SQ` | 4 / 20 | measured d²own **1–13** | **1 / 16** (wild builds at d²own=1, tighter than the probe allows) |
| splitters/barriers/launchers | — | **never** | assert never built |

### 4.2 Opening (rounds 0–15) — unchanged from the probe's era, verify it holds

1. r0, r1, r2: spawn one builder per round (3 total).
2. Each builder walks toward the nearest reachable ore and **lays conveyors outward from the core as it
   goes**, one every ~2 rounds; the harvester goes down when the chain reaches the ore
   (first harvester **r6–r13**).
3. No splitter, ever. Chain is a plain conveyor run.

### 4.3 Map conditional — the close-core rush (NEW, must be added)

```
if core_to_core_dist_sq <= 56:            # meander-class; measured 49
    r3  build SENTINEL on the tile between the cores, facing the enemy core
    r4  convert_ammo(150)                 # one bulk conversion
    r8  build SENTINEL adjacent to the first
    r9  build SENTINEL adjacent again
    fire at the enemy core from r4 onward; first harvester slips to ~r28
```
Evidence: `225f2360 g2` (v62) and `691f2554 g1` (v56), identical round-for-round. Cutoff 56 is
interpolated — the sample only has d²=49 (rush) and d²≥144 (no rush), so anything in 50…143 is untested.

### 4.4 Home ring (rounds 10–140)

1. **Two gunners back to back** at r10–r42, at d²own ∈ {4,5,9,10}, facing the enemy side.
2. From ~r67, **sentinels only**, filling d²own = 1–13, roughly one per 10–40 rounds as titanium allows,
   up to ~11.
3. Convert ammo in **chunks of 10** whenever titanium is spare, from the opening bulk chunk onward,
   with **no ceiling**.

### 4.5 Forward push (the strike) — REWRITE

**Trigger** (all must hold; first satisfied round wins, fallback r250):
```
global_ammo        >= 150            # 7/7 games; the strongest predictor
builders_alive     == 6              # at cap
home_turrets       >= 5              # 4-10 observed
```

**Placement**
- Target tile: **d²enemy = 25** preferred, accept **16–45**. Never adjacent to the core.
- Facing: the compass direction from the tile toward the enemy core, so the line shot is pre-aligned.
- Type: **SENTINEL**. Gunners only appear forward on close-core maps (`225f2360 g2` r177/r181).

**Wave shape**
- **2 turrets per wave, built on consecutive rounds** (r235/r236; r398/r399; r403/r404).
- Waves repeat. Observed inter-wave gaps: 11, 26, 61, 163 rounds. On eider the second wave was **two
  pairs within 6 rounds** (r398–r404) and that wave killed the core (r399 first damage → r479 dead).

**Camp and rebuild (the treadmill)**
- **One builder is assigned to the forward tile and stays there.**
- Every turn the forward turret is damaged, **heal it** (`225f2360 g5`: 614 heals into the forward zone).
- When it dies, **rebuild on the same tile the next round**. Measured cycle: **lifespan 11 rounds,
  rebuild gap 12 rounds**, sustained for **58 consecutive rebuilds** from r186 to r871.
- Never retreat, never come home.

### 4.6 Midfield economic sniping (NEW, must be added)

Place **1–2 sentinels at d²own ≈ 13** oriented so the line shot rakes the enemy's conveyor spine /
harvester field. In `c23600fc g3` a single sentinel at (11,12) landed **66 economic hits**; the sentinel
line collectively did **125** of the 331 economic hits, and 46 enemy harvesters died. Enable from ~r220.

### 4.7 Raiding (soften — the probe is currently too aggressive)

- **1–3 builders across the midline at any time**, continuous trickle, never a wave, and they
  **never come home**. This matches the probe's `RAID_CONCURRENT = 2`; keep it.
- Their job is **melee on harvesters and conveyors** (206 hits in eider, 887 in meander-L), not the core.

### 4.8 Heal doctrine (NEW, must be added — this is a large titanium sink)

Priority order, evaluated per builder per turn:
1. Forward turret in the enemy zone, if damaged → heal (attacking posture).
2. Own core, if damaged → heal (defensive posture; **~90% of heals when besieged**).
3. Own turret / harvester / conveyor, if damaged.

Volume calibration: **0–1100 heals per game**, scaling with pressure — 4 on an uncontested win
(`73624f1b g1`), 956–1096 when besieged (`69a0c821 g4`, `c23600fc g5`).

### 4.9 Endgame

- Keep grinding the core with the sentinel line; **do not** send builders at the core.
- If round ≥ 800 and titanium banked > ~1000, spend it (observed: on builders, `225f2360 g5` r800–r987,
  6 → 20 alive). **Low confidence, n=1.**
- Accept the `titanium_collected` tiebreaker when the core will not fall (`225f2360 g5`, 18800 vs 6310).

---

## 5. Where v62 is HARSHER / SOFTER than the current `kladde_probe`

### HARSHER — the probe under-models these; a probe that adds them will beat the current one

| # | v62 behaviour | current probe | evidence |
| --- | --- | --- | --- |
| H1 | **Forward push at r137–r235**, not r450 | `STRIKE_FALLBACK_ROUND = 450` | fwd1 column; v61 jackpot r137 |
| H2 | **Forward turrets are rebuilt forever** on a 12-round cycle | plants 3 and stops | `225f2360 g5`: 58 rebuilds on one tile |
| H3 | **A builder camps forward and heals the turret** in place | probe strikers do not heal the strike | 614 forward heals `225f2360 g5` |
| H4 | **Waves repeat** — a killed wave is replaced 11–163 rounds later | `SLOT_STRIKE` is latched once | `c23600fc g3` r235 wave dies (r426/r441) after r398 wave already landed |
| H5 | **r3 sentinel + 150 ammo + core fire by r4** on close-core maps | earliest turret r150 | `225f2360 g2`, `691f2554 g1` |
| H6 | **Midfield sentinels snipe the economy** from d²own≈13 | probe turrets are home-defence only | `c23600fc g3` 125 sentinel econ hits, 46 harvester kills |
| H7 | **Ammo banks without limit** (1460 held) | `AMMO_CEILING = 220` | `225f2360 g5` |
| H8 | Home turrets built at **d²own = 1** | `HOME_MIN_SQ = 4` forbids it | `pass2.py` home ring: d²own 1 in 5 of 11 games |

### SOFTER — the probe is harsher than the wild here; a faithful v2 must be *toned down*

| # | v62 behaviour | current probe | evidence |
| --- | --- | --- | --- |
| S1 | **Only 2 forward turrets per wave** | `STRIKE_TURRETS = 3` | r235/236, r398/399, r403/404 |
| S2 | **Builder cap is 6 alive** | `MAX_BUILDERS_TOTAL = 16` | `pass4.py` |
| S3 | **Never builds barriers** | probe has barrier logic | 0 barriers in 11 games |
| S4 | **Never rotates gunners** | `ROTATE_COST` path exists | no rotations observed in any kladde game |
| S5 | **Loses hive with zero offence** — no forward turret ever, core never touched in 674 rounds | probe always eventually strikes | `69a0c821 g4`, `691f2554 g3` |

### Verdict on the headline question

**The probe's "3 sentinels, staggered, fallback r450" is no longer representative.** It is a faithful
snapshot of the **v56** endgame — `691f2554 g1` shows exactly a 3-turret pack at r260/r261/r264 — but v62
replaced the one-shot pack with a **repeating 2-turret wave that starts ~100 rounds earlier and is rebuilt
indefinitely by a camping, healing builder.** Sentinel-led is still right. The count is wrong (2, not 3),
the timing is wrong (r173–r235, not r450), and the "once" is the biggest error: the wild does it forever.

---

## 6. Representative replay list (for `kladde_probe_v2`'s provenance docstring)

| purpose | match id | game | map | seed | rounds | result |
| --- | --- | --- | --- | --- | --- | --- |
| **Treadmill / rebuild loop** (primary) | `225f2360-c7fc-4486-9f87-80923d480530` | 5 | jackpot | 2032336915 | 1000 | W tiebreak |
| **Repeating 2-turret waves + econ sniping** (primary) | `c23600fc-79e6-477b-afde-ceb4062ca48d` | 3 | eider | 1446722484 | 480 | W core |
| **Close-core r3 sentinel rush** | `225f2360-c7fc-4486-9f87-80923d480530` | 2 | meander | 1001816144 | 247 | W core |
| **Clean forward-wave core kill** | `73624f1b-4c04-4eb8-9353-77e60096550e` | 1 | saga | 1935768979 | 352 | W core |
| **Loss mode: out-rushed on close cores** | `c23600fc-79e6-477b-afde-ceb4062ca48d` | 5 | meander | 570830940 | 989 | L core |
| **Loss mode: starved, zero offence** | `69a0c821-9487-43bc-a3dd-8e4f6a88da34` | 4 | hive | 593543234 | 674 | L core |
| **Loss mode: attrition grinder** | `31c83aff-1223-4c3b-b720-25c837409a0d` | 5 | drumlin | 1967968115 | 936 | L core |
| *baseline v56* | `691f2554-3e2e-4320-a55d-2c7d99c06eb3` | 1 / 3 / 5 | meander / hive / eider | — | 268 / 283 / 315 | W / L / L |
| *baseline v61* | `f0c33e9e-2551-40cf-a730-a30acbef2297` | 1 | jackpot | 134600046 | 440 | W core |

---

## 7. Caveats

- The probe's literal freeze source `36f5e137` could not be located (absent from `our_ladder_all.json`
  and every cache). The v56 baseline is a *rating-matched proxy* (1703–1733 vs the docstring's 1718), not
  the same games. Diff items attributed to "v56→v62" are really "v56-era→v62"; a v57–v60 change would be
  attributed to v62 here.
- v62 has only 7 ladder series in existence (35 games); 7 of those games are decoded here. Behaviour seen
  once — notably the r800 builder flood — is flagged low confidence inline.
- The close-core cutoff (d²≤56) is interpolated between an observed 49 and an observed 144. Untested band.
- `kladde` TLE'd 55 rounds in `73624f1b g1` (saga) and 3 in `31c83aff g5` (drumlin); zero elsewhere. Their
  bot is occasionally over budget on large maps — worth knowing but not modelled in the probe.
- All damage attribution is the toolkit's heuristic (README trap 10): strong inference, not a file field.
