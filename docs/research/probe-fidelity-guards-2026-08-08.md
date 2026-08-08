# Guard-probe class fidelity: `kladde_probe` and `band_probe`

**Written 2026-08-08 19:23 CEST** (research arm, read-only; no bot edits, no arena runs, no downloads).

| Thing | Version / provenance |
| --- | --- |
| Live bot | v80 "Eir 9b" = `bots/_v89sh/main.py`, md5 `e12f8585` |
| `bots/kladde_probe/main.py` | md5 `42fa9f50`, mtime 2026-08-07 00:01. Docstring: replica of **"kladde chatte tville (och oss)"** (1718 at extraction), extracted 2026-08-07 from platform match `36f5e137` games 1 and 5 (which beat our live v51) |
| `bots/band_probe/main.py` | md5 `33cd3c14`, mtime 2026-08-06 22:24. Docstring: replica of **"Banminary"** (1711 at extraction), extracted 2026-08-06 from platform match `82bc1754` game 1 (core-killed us on r42) |
| Wild corpus | `replay_archive/`, 32 matches × 5 games = **160 games / 320 team-sides**. kladde v60/63/65/71/75/78/79/80; Banminary v39/40/41. Dates 2026-08-07T12:29 → 2026-08-08T11:45 |
| Measurement code | `scratchpad/probe_fidelity.py` (scratchpad only — nothing written into the repo but this file) |

**Neither extraction source match is in `replay_archive/`.** `36f5e137` and `82bc1754` are absent, so the probes cannot be checked against the literal games they were frozen from. Control cohorts are the nearest archived wild games by version/date; this is stated again under each verdict because it bounds the confidence.

---

## 0. Self-checks before any finding

| Check | Result |
| --- | --- |
| Proto3 team-default trap | `team` initialised to `0` (TEAM_A) in every entity/convert decode path, never `None` — inherited from `tools/replay_census.py:parse_entity` and re-asserted in the new walker |
| End-to-end parse validation: `core_deliv × 10 == titaniumCollected`, per team-side per game | **320/320 team-sides, 0 mismatches** (160 games) |
| Launch-detection instrument (builder-bot position jump with d² > 2 == launcher throw) | **120/120** team-sides showing a jump were in games where a launcher existed on some side; **0** jumps in any launcher-free game. 131 team-sides built ≥1 launcher |
| Debug-print dependence | **None.** Every predicate is measured from `placeEntity` / `moveBuilderBot` / `removeEntity` / `coreConvertAmmo` / `builderAttack` / `builderHeal` / `fireTurret` / `updateHp` events. No instrument reads bot stdout, so nothing here is dev-build-only |
| Home-vs-forward turret bands | First pass used raw `d²≤20` (own core) and `d²≤32` (enemy core), which **overlap on small-gap maps** and double-counted builds on the gap 4.2/6.0/7.0/8.0 maps (76/320 sides). Reclassified **disjoint** (a turret belongs to the core it is nearer to) and all tables below are the disjoint numbers. This flipped one apparent finding — "kladde v80 plants 3 forward turrets by r45" — to 0, i.e. it was a measurement artefact, not behaviour |
| Control-cohort reproduction | Reported per probe below. Both control cohorts reproduce the docstring signature, so the method is validated before the recent cohort is read |

Map-gap distribution across the corpus (core-to-core, tiles): 4.2 ×16, 6.0 ×28, 7.0 ×20, 8.0 ×12, 9.9 ×22, 11.0 ×70, 15.6 ×20, 17.0 ×14, 18.4 ×94, 24.1 ×24.

---

## 1. Wild corpus inventory

All archived matches involving either team. `triggeredBy` and our participation noted.

### kladde chatte tville (och oss) — 16 matches, 80 team-sides

| match | date (UTC) | v | opponent | score (kladde first) | trigger |
| --- | --- | --- | --- | --- | --- |
| `d58e000e` | 08-07 12:29 | 60 | Powered by SmartFridge | 4-1 | unrated |
| `c07ad814` | 08-07 13:02 | 63 | Erebus | 4-1 | unrated |
| `fc6168fd` | 08-07 13:03 | 63 | sporks | 0-5 | unrated |
| `b931fb65` | 08-07 13:04 | 63 | HTTP 418 | 1-4 | unrated |
| `490622a4` | 08-07 14:05 | 65 | O(1) | 4-1 | ladder |
| `780059e5` | 08-07 14:35 | 65 | The Flotte Experience | 4-1 | ladder |
| `8e26ff60` | 08-07 15:05 | 65 | Erebus | 1-4 | ladder |
| `ac14e1a0` | 08-07 15:36 | 65 | Leviathan | 3-2 | ladder |
| `5d218d08` | 08-07 19:42 | 71 | Besvikomat | 0-5 | unrated |
| `98e2c1fc` | 08-08 00:35 | 75 | **OpenSverige (v72)** | **5-0** | ladder |
| `3de9f5e0` | 08-08 03:06 | 75 | **OpenSverige (v72)** | **4-1** | ladder |
| `234a77b8` | 08-08 04:35 | 75 | Coreflood | 1-4 | ladder |
| `2c68603d` | 08-08 05:41 | 78 | Pivot | 1-4 | unrated |
| `2cb93283` | 08-08 06:12 | 65 | Lorem Ipsum | 1-4 | unrated (old version re-run) |
| `c9b29070` | 08-08 07:45 | 79 | Pivot | 0-5 | ladder |
| `ebe7e0a9` | 08-08 10:45 | 80 | I Stone | 4-1 | ladder |

Cohorts: **CONTROL = v60–71** (50 games, all 08-07, the extraction era) · **RECENT = v75–80** (30 games, 08-08). `2cb93283` is v65 played on 08-08 and is scored into control by version.

### Banminary — 16 matches, 80 team-sides

| match | date (UTC) | v | opponent | score (Ban first) | trigger |
| --- | --- | --- | --- | --- | --- |
| `b284da85` | 08-07 13:34 | 40 | O(1) | 1-4 | ladder |
| `7d89fdda` | 08-07 14:04 | 39 | Powered by SmartFridge | 3-2 | ladder |
| `c9f0d4e9` | 08-07 14:35 | 39 | Leviathan | 4-1 | ladder |
| `1c38bfed` | 08-07 15:05 | 39 | Coreflood | 4-1 | ladder |
| `5bda8c64` | 08-07 15:36 | 39 | Pivot | 3-2 | ladder |
| `f844a445` | 08-07 22:28 | 41 | Besvikomat | 1-4 | ladder |
| `ebd900b1` | 08-07 23:37 | 41 | **OpenSverige (v71)** | 1-4 | ladder |
| `86e91e86` | 08-08 01:45 | 41 | **OpenSverige (v72)** | 0-5 | ladder |
| `130c5ac3` | 08-08 03:34 | 41 | Powered by SmartFridge | 4-1 | ladder |
| `040920f5` | 08-08 05:12 | 41 | Lunds Stallions | 2-3 | unrated |
| `41f6513a` | 08-08 05:14 | 41 | **OpenSverige (v73)** | 1-4 | ladder |
| `e055de81` | 08-08 06:47 | 41 | **OpenSverige (v74)** | 0-5 | ladder |
| `3311f968` | 08-08 08:26 | 39 | **OpenSverige (v75)** | 1-4 | ladder |
| `9db6a45d` | 08-08 09:58 | 41 | **OpenSverige (v75)** | **4-1** | ladder |
| `f0196705` | 08-08 10:45 | 41 | Big O | 1-4 | ladder |
| `37e4f4ee` | 08-08 11:45 | 41 | **OpenSverige (v77)** | 1-4 | ladder |

Cohorts: **CONTROL = v39–40** (30 games, all 08-07 ≤15:36 — nearest archived to the 08-06 extraction) · **RECENT = v41** (50 games). `3311f968` is v39 replayed on 08-08 against us, which gives a within-opponent v39-vs-v41 comparison.

---

## 2. `band_probe` — Banminary all-in launcher rush

### 2.1 Derived class signature (read off the probe's own docstring + constants)

| # | Claimed signature element | Measurable predicate |
| --- | --- | --- |
| B1 | "convert_ammo(30) immediately" at r0 (`OPENING_AMMO = 30`) | first `coreConvertAmmo` at round 0, amount == 30 |
| B2 | "one builder, one launcher" at r1–2 | exactly 1 launcher built, first launcher round ≤ 5 |
| B3 | "one throw" at r2–4 (`LAUNCH_RANGE_SQ = 26`) | ≥1 builder-bot position jump with d² > 2, first jump round ≤ 10 |
| B4 | "no economy at all" | harvesters built by r60 ≤ 1 |
| B5 | Sentinel #1 by r28, Sentinel #2 by r36, Gunner by r42, all aligned on the enemy Core | ≥2 turrets built within d²≤32 of the enemy core (and nearer to it than to their own) by r45 |
| B6 | "no second wave" (`MAX_BUILDERS = 2`) | builder bots spawned by r60 ≤ 3 |
| B7 | "no defence" | ≤1 turret in the own-core band (d²≤20) |
| B8 | "enemy Core dead on round 42" | game length ≤ 100 rounds |
| B9 | "everything the team owns is titanium-for-ammunition" | total harvesters over the whole game ≤ 1 |
| B10 | throw + walk puts a body on the Core early | first builder bot within d²≤32 of the enemy core by r15 |
| — | `SENTINEL_TARGET=2, GUNNER_TARGET=1`, sentinel first | turret mix ≈33% gunner; **first** turret built is a sentinel |

### 2.2 Measurements

**Opening fingerprint per version** (these are decided before contact, so they are opponent-independent — medians):

| ver | n | harv 1st | harv by r60 | bots by r60 | launcher rnd | 1st jump rnd | 1st turret rnd | 1st fwd turret rnd | ammo 1st rnd | ammo 1st amt | 1st deep rnd |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| v39 | 25 | 6 | 2 | 3 | **1** | **2.0** | 5 | 9.0 | **0** | **30** | 3 |
| v40 | 5 | 8 | 0 | 3 | **1** | **2.0** | 5 | 9 | **0** | **30** | 3 |
| v41 | 50 | 7 | 2.0 | 3.0 | **1.0** | **2.0** | 9.0 | 15.0 | **0.0** | **30.0** | 9.5 |

**Predicate pass rates, control vs recent:**

| predicate | control v39–40 (n=30) | recent v41 (n=50) |
| --- | --- | --- |
| B1 r0 `convert_ammo(30)` | **30/30 = 100%** | **50/50 = 100%** |
| B2 exactly 1 launcher by r5 | **30/30 = 100%** | **50/50 = 100%** |
| B3 launch throw by r10 | 28/30 = 93% | 48/50 = 96% |
| B4 no opening economy (harv by r60 ≤1) | 15/30 = 50% | 18/50 = 36% |
| B5 ≥2 forward turrets by r45 | 25/30 = 83% | 44/50 = 88% |
| B6 ≤3 builders by r60 | 29/30 = 97% | 46/50 = 92% |
| B7 no home army (≤1 own-core turret) | 22/30 = 73% | 40/50 = 80% |
| B8 decisive early (≤100 rounds) | 16/30 = 53% | 20/50 = 40% |
| **B9 no fallback economy at all (harv ≤1)** | **15/30 = 50%** | **10/50 = 20%** |
| B10 deep presence by r15 | 23/30 = 77% | 30/50 = 60% |
| first turret built is a **sentinel** | **25/25 = 100%** | **50/50 = 100%** |
| gunner share of turret builds (median) | 0% | 25% |

**Outcome shape:**

| cohort | wins | median win round | games past r200 | median harvesters in those |
| --- | --- | --- | --- | --- |
| control v39–40 | 16/30 | 55 (range 29–146) | 4/30 = 13% | 0 |
| recent v41 | 15/50 | 62 (range 30–1000) | 19/50 = 38% | **7** |

### 2.3 Verdict — **CLASS-VALID (opening), CLASS-EXTENDED (tail)**

The rush itself has not moved a millimetre. Across **all 80 team-sides, both cohorts, every opponent and every map**: convert_ammo(30) on round 0, exactly one launcher on round 1, a throw on round 2, sentinel first, ≥2 turrets planted in the Core's face by r45, ~3 builders. B1/B2 are 100/100 in both cohorts and the first-turret-is-a-sentinel test is 75/75. `band_probe`'s Stage A/A+/B/C/D script is a faithful description of what Banminary v41 still does today.

What **changed** between v39/40 and v41 is what happens when the rush is contained: the class acquired a **fallback economy**. B9 fell 50% → 20%; games past r200 went 13% → 38%; and in those long games Banminary now runs a median of 7 harvesters and up to 26. Two matches are pure economy games (`ebd900b1`: 13 harvesters, 39 conveyors, 359 rounds; `9db6a45d`: 8 harvesters, 28 conveyors, 373 rounds, 7,330 Ti collected, **beat us 4-1**). `band_probe` cannot produce this mode at all — its `MAX_BUILDERS = 2`, `REPLACEMENT_MIN_ROUND = 50` and total absence of harvester code make it structurally impossible.

Note the fallback is not purely a version thing: control v39 vs SmartFridge and vs Leviathan already showed 2 harvesters. v41 made it the default rather than the exception.

**Confidence: high** on the opening (80 team-sides, zero exceptions, 5 versions of our own bot as opponents), **medium-high** on the fallback characterisation (the extraction-source match is unavailable, so I cannot prove the fallback was absent on 08-06 — only that it was rarer at v39/40).

**What would change the answer:** archiving `82bc1754`; or a Banminary v42+ that reorders the opening (a different first turret type, or a launcher later than r5) — both would show up in the opening-fingerprint table immediately.

### 2.4 Guard-mechanism answer

`band_probe` guards **defensive response to an early forward-turret insertion**: a body thrown across the gap by r2, standing on our doorstep by r15, planting aligned sentinels into our Core by r28–45 while we still have almost no army. Wild Banminary v41 performs that exact sequence in 100% of games. **The probe still exercises the mechanism it exists to protect.** This is the safe case — version-stale on the tail, class-valid as a guard.

The gap is coverage, not mechanism. Splitting our 35 wild ladder games against Banminary by the mode they actually played:

| Banminary mode | n games | our game share | median rounds | their median Ti collected |
| --- | --- | --- | --- | --- |
| rush-only (≤2 harvesters) — **what the probe models** | 15 | **13/15 = 87%** | 109 | 0 |
| fallback economy (>2 harvesters) — **not modelled** | 20 | **14/20 = 70%** | 316 | 2,045 |

`band_probe` reads 83–100 in today's batteries, which sits right on top of the 87% we actually score in rush-mode wild games. It is well calibrated for the half of the matchup it covers, and silent on the other half — which is where the only series we lost to Banminary today (`9db6a45d`, 1-4 at 09:58) came from.

---

## 3. `kladde_probe` — slow grind / home army / late strike

### 3.1 Derived class signature

| # | Claimed signature element | Measurable predicate |
| --- | --- | --- |
| K1 | No launcher anywhere in the recipe | launchers built == 0 |
| K2 | "almost the whole army stands at HOME, 1–4 tiles off their own Core" (`HOME_MIN_SQ=4, HOME_MAX_SQ=20, HOME_TURRET_MAX=8`) | ≥5 turret builds in the own-core band (d²≤20, nearer own core) |
| K3 | "the economy is never finished — harvesters keep going up past r300" (`HARV_INTERVAL=15`, `MAX_HARVESTERS=16`) | ≥5 harvesters and last harvester ≥ r100 |
| K4 | "builders keep being spawned as titanium allows" (`SPAWN_INTERVAL=8`, `MAX_BUILDERS_TOTAL=16`) | ≥6 builder bots and last spawn ≥ r100 |
| K5 | "opportunistic — 2+ spare builders walk into the enemy's economic footprint together, harvesters first" (`RAID_CONCURRENT=2`) | ≥30 rounds with a builder in the enemy half **and** ≥10 builder attacks landed in the enemy half |
| K6 | "one builder plants two or three turrets in the enemy Core's face" (`STRIKE_TURRETS=3`) | ≥2 turrets in the enemy-core band (d²≤32, nearer enemy core) |
| K7 | "nothing about them is a timing… no presence at all until late" | zero forward turrets before r45 |
| K8 | "ammunition banked in small conversions from r0… 100+ sitting there" (`AMMO_CHUNK=5`, `AMMO_CEILING=220`) | first conversion ≤ r30 and ≥300 Ti converted over the game |
| K9 | "being slow is the point; a win at r200–700 is on-spec" | game length ≥ 150 rounds |
| K10 | "otherwise stands at home repairing what is damaged" | ≥50 builder heal actions |
| — | "Sentinels with a Gunner every third slot" (`_home_turret_type: GUNNER if idx % 3 == 0`), strike is "sentinel-led" | turret mix ≈ **33% gunner** |
| — | "both source games went from no presence at all to a dead Core inside 50 rounds" | a burst of forward-turret builds inside a 25-round window, late, followed shortly by the Core kill |

### 3.2 Measurements

**Opening fingerprint per version** (opponent-independent, medians):

| ver | n | harv 1st | harv by r60 | bots by r60 | 1st turret rnd | 1st home turret rnd | ammo 1st rnd | ammo 1st amt | 1st raid rnd | 1st deep rnd | launchers | fwd turrets by r45 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| v60 | 5 | 7 | 5 | 6 | 12 | 12 | 13 | 60 | 59 | 120 | **0** | **0** |
| v63 | 15 | 8 | 5 | 5 | 20 | 33 | 17 | 60 | 31.5 | 29.5 | **0** | **0** |
| v65 | 25 | 7.0 | 4 | 5 | 18 | 18 | 19 | 60 | 55 | 64.0 | **0** | **0** |
| v71 | 5 | 8 | 8 | 5 | 15 | 15 | 16 | 20 | 66 | 91 | **0** | **0** |
| v75 | 15 | 8 | 4 | 5 | 26 | 26 | 24 | 60 | 44 | 51.0 | **0** | **0** |
| v78 | 5 | 8.0 | 7 | 5 | 42 | 42 | 45 | 10 | 58 | 51.5 | **0** | **0** |
| v79 | 5 | 8 | 7 | 6 | 42 | 42 | 45 | 20 | 97 | 116.5 | **0** | **0** |
| v80 | 5 | 7 | 6 | 5 | 10 | 10 | 11 | 60 | 28 | 10 | **0** | **0** |

**Predicate pass rates, control vs recent:**

| predicate | control v60–71 (n=50) | recent v75–80 (n=30) | Δ |
| --- | --- | --- | --- |
| K1 no launcher | **50/50 = 100%** | **30/30 = 100%** | 0 |
| K2 home army ≥5 turrets | 36/50 = 72% | 24/30 = 80% | +8 |
| K3 economy paced + continuing | 31/50 = 62% | 23/30 = 77% | +15 |
| K4 builders keep coming | 34/50 = 68% | 21/30 = 70% | +2 |
| K5 raiding into enemy half | 33/50 = 66% | 25/30 = 83% | +17 |
| K6 forward strike turrets ≥2 | 27/50 = 54% | 17/30 = 57% | +3 |
| K7 no forward turret before r45 | 43/50 = 86% | 26/30 = 87% | +1 |
| K8 ammo banked early + deep | 28/50 = 56% | 18/30 = 60% | +4 |
| K9 long game (≥150 rounds) | 41/50 = 82% | 29/30 = 97% | +15 |
| K10 sustained repair (≥50 heals) | 43/50 = 86% | 26/30 = 87% | +1 |

**Late-strike shape** (games won by `core_destroyed`; "burst" = largest cluster of forward-turret builds inside any 25-round window):

| cohort | core-kill wins | burst size | burst round | burst / game length | rounds from burst to game end | fwd turrets in final 60 rounds | median game length |
| --- | --- | --- | --- | --- | --- | --- | --- |
| control v60–71 | 21 | **2** | 182 | **0.8** | **57** | **3** | 230 |
| recent v75–80 | 14 | **3** | 202 | 0.7 | 100 | **3** | 292 |

**Turret composition** (the one that fails):

| cohort | gunner share of turret builds, median | mean | games gunner-majority | first turret built |
| --- | --- | --- | --- | --- |
| control v60–71 | **62%** | 59% | 28/45 | sentinel 27 / gunner 18 |
| recent v75–80 | **70%** | 61% | 18/30 | sentinel 17 / gunner 13 |
| **`kladde_probe` by construction** | **33%** (`GUNNER if idx % 3 == 0`), strike is 2 sentinels + 1 gunner | — | — | sentinel |

**Intensity per version** (opponent-dependent — read with the opponent column in §1):

| ver | n | rounds | home turrets | fwd turrets | Ti→ammo | shots fired | own heals | raid rounds | fwd builder attacks | enemy harvesters killed | dmg dealt | Ti collected | heals **forced on the opponent** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| v60 | 5 | 204 | 13 | 3 | 658 | 52 | 144 | 66 | 45 | 0 | 1013 | 3820 | 34 |
| v63 | 15 | 335 | 8 | 1 | 660 | 57 | 86 | 178 | 104 | 2 | 1382 | 2700 | 144 |
| v65 | 25 | 219 | 5 | 1 | 590 | 58 | 100 | 96 | 10 | 1 | 969 | 1860 | 48 |
| v71 | 5 | 447 | 14 | 5 | 358 | 35 | 171 | 185 | 83 | 1 | 721 | 3680 | 96 |
| **v75** | 15 | 349 | 7 | 7 | **1308** | **153** | 227 | 244 | 132 | **5** | **3020** | 4410 | **294** |
| v78 | 5 | 273 | 6 | 0 | 171 | 42 | 119 | 49 | 39 | 0 | 699 | 1230 | 38 |
| v79 | 5 | 286 | 14 | 0 | 109 | 25 | 65 | 38 | 0 | 0 | 498 | 1200 | 45 |
| **v80** | 5 | 243 | 20 | 4 | **1517** | **194** | 161 | 142 | 106 | **4** | **2779** | 4240 | **223** |

The v75/v80 escalation is **opponent-driven, not version drift**: the same v75 build against Coreflood (`234a77b8`) reads 330 Ti→ammo / 26 shots / 818 damage, i.e. control-level, while v75 against us reads 1308–1666 / 153–210 / 3020–3591. kladde escalates when it is winning a long game; against us it always is.

### 3.3 Verdict — **CLASS-VALID on shape; one predicate was never faithful (extraction defect, not drift)**

**Not drifted.** Every shape predicate holds at control rates or better; the largest single move is K5 (raiding) at +17 points, in the direction of *more* kladde, not less. The hardest invariant — `launcher_n == 0` — is **80/80 team-sides across all eight versions**. The control cohort reproduces the docstring's central claim exactly: a **2-turret burst at 80% of the way through the game, 57 rounds before the Core dies, 3 forward turrets standing in the final 60 rounds**, which is the "no presence at all to a dead Core inside 50 rounds" the probe was written from. Recent games shift that to a 3-turret burst at 70% and 100 rounds of run-out — a longer, larger forward campaign in the same shape, not a different plan. The method is validated by that control reproduction, so the recent numbers can be read at face value.

**But one signature element is wrong, and it was wrong at extraction time:**

> **CLASS-DEFECT (turret composition).** `kladde_probe` builds ~33% gunners / 67% sentinels (`_home_turret_type`: `GUNNER if idx % 3 == 0`; strike is sentinel-led). Wild kladde is **gunner-majority in both cohorts**: 62% gunner share at v60–71 (28/45 games gunner-majority) and 70% at v75–80. The control cohort — the very era the probe was frozen from — already shows this, so this is an **extraction fidelity defect, not drift**. The probe has never had the right turret mix.

This is not cosmetic. Gunner: r²=13, dmg 7, 4 ammo, **line of fire blocked by obstacles**. Sentinel: r²=32, dmg 18, 10 ammo, **ignores obstacles**. A defensive change that works by breaking line of sight — barrier placement, body-blocking, building geometry, standoff distance — is scored against a mostly-sentinel attacker on the probe and a mostly-gunner attacker in the wild. Same class name, different mechanism under test.

**Confidence: high** that the shape predicates hold (80 team-sides, 8 versions, 10 opponents). **High** that the turret mix is inverted (measured in both cohorts independently). **Low** on kladde v79/v80 specifically — 5 games each against one opponent each, and v78/v79 (both vs Pivot, 1-9 across the two matches) never got far enough into the game to exhibit K6 at all, so their zeros are "did not reach", not "does not do".

**What would change the answer:** kladde v79/v80 games against a peer opponent (the only v80 sample is 5 games vs I Stone); archiving `36f5e137` so the probe can be checked against its own source; or a kladde v81+ that builds a launcher (it would break a 80/80 invariant on the first game).

### 3.4 Guard-mechanism answer — **this is the dangerous case, on two counts**

`kladde_probe` exists to gate *pressure over time*: does a change break our repair line, our harvester defence, our ability to survive a late turret insertion? The mechanism is real and wild kladde still applies it — against us, harder than against anyone else. Our 10 ladder games vs kladde v75 (our v72), measured from the replays:

| what wild kladde v75 does to us, per game (median over 10 games) |  |
| --- | --- |
| forward turrets planted in our Core's band | 7 |
| shots fired | 178.5 |
| titanium converted to ammunition | 1,649 |
| **our harvesters destroyed** | **8.5** |
| **heal actions we were forced to spend** | **398** |
| damage put on our Core | 1,792.5 |
| **our game share** | **1/10 = 10%** |

So the mechanism is alive and the probe aims at the right one. Two things nonetheless break the guard reading:

**(a) The intensity is off by ~70 points.** `kladde_probe` reads **63.3–85.0** for us across today's batteries. Wild kladde reads **10.0%** (1-9, 10 ladder games, our v72 vs their v75). The probe is not a hard instrument that we barely survive; it is a soft one we comfortably beat, at a level 60–75 points above the matchup it names. Anything the probe reports as "protected" is, in the wild version of that class, already lost.

**(b) The mechanism under test is partly the wrong one.** Per §3.3, the probe's fire is sentinel-weighted (long-range, obstacle-ignoring); wild kladde's is gunner-weighted (short-range, blockable, ~2× the shot count). Outcome-similar, mechanism-different — precisely the case the guard must not have.

Both readings are still *discriminating*: today's kladde leg moved 63.3 → 85.0 across variants, a 21.7-point spread, so it is not saturated and its **differences between variants remain informative**. What is not supportable is reading its **level** as evidence about kladde.

---

## 4. Disposition

| probe | disposition | terms |
| --- | --- | --- |
| `band_probe` (md5 `33cd3c14`) | **USABLE AS A GUARD, with a stated coverage caveat** | The opening it models is 100% intact at Banminary v41 (80/80 team-sides). It covers the rush-mode half of the wild matchup and is well calibrated there (probe 83–100 vs 87% wild rush-mode game share). It does **not** model the v41 fallback economy, which is 20/35 of our wild games against them and the source of our only loss series today. Do not read a band-leg pass as covering long-game Banminary. |
| `kladde_probe` (md5 `42fa9f50`) | **NEEDS RE-FREEZE** — usable meanwhile only for *directional* comparison between variants, never for level | Class shape is valid and undrifted, so the instrument is not junk. Two fixes are needed before its level means anything: (1) **invert the turret mix** to gunner-majority (~65/35 gunner/sentinel, both home band and strike) — this is an extraction defect present since day one, provable against the control cohort; (2) **re-calibrate intensity** — wild kladde vs us converts 1,649 Ti to ammo and fires 178 shots per game while the probe is structurally capped at `HOME_TURRET_MAX=8`, `STRIKE_TURRETS=3`, `AMMO_CEILING=220`. |

**Wild games a `kladde_probe` re-freeze should be built from:** `98e2c1fc` and `3de9f5e0` (v75 vs OpenSverige, 10 games, 08-08 00:35 and 03:06) — the only wild games of this class against our own bot, and the ones exhibiting the full mechanism (5–12 of our harvesters killed per game, 398 heal actions forced, 7 forward turrets). `ebe7e0a9` (v80 vs I Stone, 08-08 10:45) for the current-version opening fingerprint. **A re-freeze against v79/v80 alone would be a mistake** — both of those matches are single-opponent, and v78/v79's zeros on K5/K6 are Pivot crushing them, not kladde behaviour.

---

## 5. Do today's acceptance verdicts inherit a caveat?

**Yes, on the kladde legs. No new caveat on the band legs.**

The kladde-leg readings recorded in `results.tsv` today, all of which inherit §3.4:

`_v79e6c` 63.3 · `_v79e6c-ext-pool` 67.5 · `_v80e6d-race` 70.0 / 68.3 · `_v82c1-gate` 68.3 · `_v82hd-gate` 75.0 · `_v83c1b-gate` 78.3 · `_v84g-slotbar` 83.3 · `_v85hs-gate` 83.3 · `_v85hsb-bar` 85.0 · `_v85hsc-acceptance` 78.3 · `_v85hsd-ablation` 76.7 · `_v86m1-acceptance` 78.3 · `_v87ad-acceptance` 76.7 · `_v89sh-acceptance` 83.3 · `_v90ft-acceptance` 85.0 · `_v92sp-acceptance` 78.3 · `_v94fb-keep` 78.3 · `_v95e1-keepdev` 85.0 · `_v95e1b-keepdev` 75.0 · `e1-bundle-h2h` 81.7 — including the 68.3 → 75.0 → 81.7 sequence the acceptance decisions were partly read off.

Precisely what is and is not caveated:

- **Not invalidated: the direction of the differences.** The class predicates hold — the probe stresses the same class it always did, so a variant scoring higher than another against `kladde_probe` genuinely handled that class's pressure better. The 21.7-point spread across today's variants shows it discriminates.
- **Caveated: the absolute level.** No kladde-leg number is evidence about the wild kladde matchup, which is 10%. `_v84g-slotbar`'s own honesty line already said "kladde gain is instrument-side (probe, not wild v75/76)"; this note supplies the magnitude — roughly a 70-point offset.
- **Caveated harder: any variant whose mechanism is line-of-sight-dependent.** Barrier/blocker placement, body-blocking, standoff geometry, anything that survives by breaking a firing line. The probe fires 67% sentinels (unblockable); wild kladde fires ~65% gunners (blockable). A change scored on that leg was scored against the wrong turret. This applies to the *comparison*, not just the level, and it is the one finding that could reverse a variant ordering.
- **Band legs: no new caveat on what they measure**, only on what they do not — the fallback-economy mode. A band-leg pass says nothing about long-game Banminary.

Independent of the probes: **we have no kladde-vs-us wild game since 08-08 03:06**, when our bot was v72. Six of our versions have shipped since. The 10% wild figure is the most recent measurement available and may already be stale in our favour; it is stated as the last measured value, not as current standing.
