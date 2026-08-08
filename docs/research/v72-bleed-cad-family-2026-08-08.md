# v72 bleed map — the CAD family (CtrlAltDefeat v117 / Lunds Stallions v45 / Kings College Munich v1)

**Date:** 2026-08-08. **Research arm**, read-only: 30 archived games decoded, no
downloads, no bots touched, no matches run.

**Version tags (rule 2).** Us = **OpenSverige v72 "chainwatch"** (`379a5d80-…`),
teammate x3r0's line, live on the ladder. Opponents = **CtrlAltDefeat v117**
(`74e43df6-…`), **Lunds Stallions v45** (`eceb8455-…`), **Kings College Munich
v1** (`dfa9be96-…`).

| Match | Result | Opponent | Our seat | Elo Δ (us) | Completed (Z) |
| --- | --- | --- | --- | --- | --- |
| `2b05487d-b689-45b5-abf1-cfefa9a0a3f9` | **L 2-3** | CAD v117 | A | −2.53 | 2026-08-08T00:56:59 |
| `c6383349-36c8-48ce-a7be-86c2798adc73` | **L 2-3** | CAD v117 | A | −3.71 | 2026-08-08T02:08:14 |
| `3e8bd0bf-9442-4b67-b976-cda914ae7d4b` | **L 2-3** | CAD v117 | B | −3.90 | 2026-08-08T03:17:35 |
| `e14bb335-9fd3-492f-974f-9fbb2ca0fbb1` | **L 0-5** | Lunds v45 | B | −16.63 | 2026-08-08T00:46:57 |
| `447e336c-7266-4188-95ff-a67cbaf06d18` | **L 2-3** | Lunds v45 | A | −5.34 | 2026-08-08T02:55:19 |
| `9eb8f87a-18eb-4415-b2d7-2f856139a8cf` | **W 3-2** | KCM v1 | B | +2.58 | 2026-08-08T01:06:32 |

Record in games: **11 W – 19 L**. Against CAD v117 specifically: **6 W – 9 L**
across three matches, each one lost 2-3 — i.e. **the whole CAD bleed is three
one-game margins.**

---

# SYNTHESIS — ranked mechanical changes for the replacement candidate

Every number below is parsed from the replays. Where a claim is inference rather
than measurement it is marked **UNCERTAIN**.

## L1 (highest value) — a fixed-facing SENTINEL home ring, aimed at *tiles*, not built at a *radius*

**The measurement.** Classify every enemy gunner/sentinel planted within d²≤36
of our core footprint by whether *any* live friendly turret ever had it on a
reachable firing ray (gunner: 8 rays, d²≤13, LOS-blocked; sentinel: its one
build-time ray, d²≤32, obstacles ignored):

| | n | our turrets ever shot at it | killed by our turret fire | core damage it dealt |
| --- | --- | --- | --- | --- |
| **COVERED** | **98** | **90** | **89** | 7,178 |
| **UNCOVERED** | **147** | **0** | **0** | **34,709 (82.9%)** |

**0 of 147 uncovered enemy turrets took a single shot from us, in 30 games.**
This reproduces the C1-validation law (`kcm-win-c1-validation-2026-08-07.md`:
8/8 covered killed, 0/69 uncovered shot at) on a corpus 2× the size and on
**production v72 data**. Combined corpora: **0/216**.

Restricted to the nine CAD v117 losses, **uncovered turrets did 11,935 of the
12,349 turret-damage points that killed our core — 96.6%.** In six of those nine
games it is 99–100%; the lowest is 87%.

**The proof that the fix works is already in the corpus.** `2b05487d` g4
(14×18, WIN 16,870–5,810): our **sentinel #68 @(3,6) facing SOUTHEAST**, built
r58, alive at r1000 — 102 shots, 1,820 damage, and its ray
`(4,7)→(5,8)→(6,9)→(7,10)` covered **16 of CAD's 29 near-core plants**,
including the tile **(7,10) which CAD re-planted on 13 separate times**, every
one of them dead within 2–4 rounds. One 30-Ti building turned CAD's rebuild
loop into a kill farm. The same match's three losses have no such turret.

**Spec (feeds C1c destination/age arming + the ray-coverage home ring plank).**
Do *not* specify "turrets within radius R of the core". Specify:

1. Candidate set = ring tiles at d²≤8 of the core footprint that are not wall,
   not footprint, buildable.
2. For each `(tile, facing)` precompute the sentinel ray (d²≤32, ignore
   obstacles — sentinels are never blocked).
3. Target set = every tile at d²≤13 of the core footprint **∪** the map-keyed
   CAD landing tiles and their four orthogonal neighbours (§Q3). The d²≤13 band
   is where the damage actually comes from: across all 30 games, **98 of the 116
   distinct enemy turrets that ever put a shot into our core were planted at
   d²≤13 of the footprint, and they did 39,195 of 46,539 turret damage (84%)**.
4. Greedy set-cover. **Measured cost: 2–5 sentinels per map** (the greedy cover
   over the actual killers ran 2, 2, 2, 3, 3, 3, 4, 4, 5 across the nine CAD
   losses) = **60–150 Ti at base scale.** In those same nine games we burned
   **12,720 Ti on rotations** (L2).
5. **Sentinels cannot be re-aimed.** A mis-faced sentinel is dead weight until a
   builder `destroy()`s it (free) and pays the scaled rebuild. Choose the facing
   at build time from the table, never "face the nearest enemy".

## L2 — delete `rotate()` from the home ring entirely

**Rotate cost is now measured, not quoted.** On 118 rounds in which our team's
only event was a gunner rotation (no build, no builder action, no conversion, no
delivery, passive-drip rounds excluded), the titanium balance moved by exactly
**−10 per rotation, 112/112 single-rotation rounds and 6/6 double-rotation
rounds at −20.** No exceptions.

| CAD v117 | rotations | Ti burned | Ti collected | share of income |
| --- | --- | --- | --- | --- |
| **9 losses** | **1,272** | **12,720** | 21,980 | **58%** |
| **6 wins** | **30** | 300 | 56,410 | **0.5%** |

Per game the split is just as clean: mean rotation-share of income **49% in the
losses vs 3% in the wins**, and the losses are *shorter* (mean 341 rounds vs
760), so this is not a duration artifact.

And the rotations buy nothing. `2b05487d` g1: gunner #105 @(5,7) rotated **165
times (1,650 Ti)** and fired 13 shots for 91 damage; gunner #118 @(9,5) rotated
**181 times (1,810 Ti)** for 16 shots / 112 damage. In that same game the two
gunners that killed us — #543 @(6,2) and #577 @(5,2), both facing SOUTH,
planted r228/r238, **2,604 of 3,172 damage** — were never shot at once, and two
fixed sentinels at (5,4)N and (6,4)N (60 Ti) would have had both on-ray.

`c6383349` g2 is the pathological case: **239 rotations = 2,390 Ti against 2,690
Ti collected (89%)**, titanium balance below 10 for **526 of 672 rounds**, heal
line collapsed to 0.44, core dead r671.

**Mechanically:** a gunner pays 10 Ti + one cooldown round to re-aim an r²=13
ray. A sentinel on the same tile holds an r²=32 ray forever for free. On the
home ring the sentinel strictly dominates.

## L3 — a standing heal detail *on* the core ring, sized against measured incoming

**Core survival is bimodal in heal-rate, with no middle ground:**

| heal delivered ÷ damage taken, on our core | n | outcome |
| --- | --- | --- |
| **≥ 0.94** | 13 | core survived, **13/13** |
| **≤ 0.86** | 16 | core destroyed, **16/16** |
| 0.34 (one outlier) | 1 | survived — `c6383349` g3, only 497 damage across 1000 rounds |

So the loss is not "they out-damaged us"; it is "the heal line stopped". In the
60 rounds before each core death:

- **It is usually not a titanium problem.** `e14bb335` g1 died with **9,557–9,912
  Ti banked** and only 2 builders adjacent to the core (476 healed of 956 taken).
  `447e336c` g3 died with 487 Ti banked and **zero builders alive**.
- **It is a builder-supply-and-position problem.** Median builders standing
  orthogonally adjacent to the core footprint in the 60-round death window:
  **0 in four of the sixteen deaths** — and three of those four delivered
  **literally zero heals in those 60 rounds** (`3e8bd0bf` g3 and g5,
  `447e336c` g3; `c6383349` g4 managed 0.07/round). `3e8bd0bf` g5 is the
  sharpest: **4 builders alive, 0 of them adjacent to the core, 0 heals in 60
  rounds**, core dead r168.
- **Where it was only titanium, L2 pays for it**: `c6383349` g2 (Ti<10 for 78%
  of the game, 2,390 Ti spent on rotations).

**Spec.** Reserve N builders whose only job is stand-adjacent-and-heal.
Incoming ≈ **9 HP/round per live enemy sentinel with our core on its ray** +
**3.5 HP/round per live enemy gunner** (sentinel 18 dmg / reload 2, gunner 7 /
reload 1). One adjacent builder delivers ≈ **4 HP/round** (measured across the
death windows: **0.8–1.1 heals per adjacent builder per round**). **The measured
shortfall in all nine CAD core-death losses was 0.48–2.06 heals/round — i.e. 1
to 3 more permanently-stationed builders, or one fewer live enemy sentinel.**

## L4 — map-conditional posture: at core separation d² ≥ 144, stop building forward turrets

Against CAD v117 the result is a step function in core separation:

| core sep d² | 32 | 32 | 64 | 64 | 64 | 81 | 81 | 144 | 144 | 144 | 288 | 338 | 392 | 392 | 392 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| result | W | W | W | W | W | W | L | L | L | L | L | L | L | L | L |

**All 6 wins at d²≤81; 8 of 9 losses at d²≥144** (the ninth is the d²=81
boundary game, `3e8bd0bf` g3). Across all 30 games the medians are 64 (wins) vs
144 (losses). Seat is irrelevant: 6/15 as seat A, 5/15 as seat B.

The mechanism is visible in the forward-turret ledger. On the wide maps our
forward turrets live 3–33 rounds (`2b05487d` g3: five forward turrets, lifespans
11/3/10/119/3; `3e8bd0bf` g4: 16 and 7). Damage we put on **their** core across
the nine losses: 144, 452, 175, 252, 144, 252, 252, 126, **0** — median **175**,
i.e. never within a factor of two of a threat. That titanium buys nothing and it
is the same titanium the ring and the heal detail need.

**v72's economy is now good enough to take the tiebreak instead**: v72
out-collected the opponent in **15 of 30 games** and **7 of 15 vs CAD**, and lost
only one game in which it out-collected (`3e8bd0bf` g4). The wide-map play is
ring + heal + economy to r1000, not a forward battery.

## L5 — arm against *re-plants*, and keep the arming alive to r1000

CAD v117 re-uses tiles; KCM v1 does not. Near-core plants over each corpus:

| opponent | games | near-core turrets | per 100 rounds | distinct tiles | **tile re-plants** |
| --- | --- | --- | --- | --- | --- |
| CAD v117 | 15 | 131 | 1.72 | 105 | **26** |
| Lunds v45 | 10 | 89 | 1.57 | 67 | **22** |
| KCM v1 | 5 | 25 | 0.77 | 25 | **0** |

`2b05487d` g4 alone: **(7,10) re-planted 13 times**. `3e8bd0bf` g3: the sentinel
that did 46% of the killing damage was planted at **r355 on (11,3) — the exact
r3 throw destination from round 3**. This is the v116 read's calibration delta
D1 ("the forward turret is re-planted on its exact old tile") confirmed in v117.

Consequences for the build: (a) a killed home-ring sentinel must be rebuilt on
the **same tile and facing**, not re-derived; (b) the arming must persist —
**seven of the nine CAD losses have their top killer planted after r130, and two
after r400** (`2b05487d` g3 at r403, `c6383349` g2 at r592); (c) the arming
target set should include every tile the opponent has already planted on in
this game.

## L6 (cheap) — the family's r3 turret type is predictable from the landing tile

> **REFUTED AS STATED, 2026-08-08 (cad-probe-refreeze-spec):** the true rate is
> **8/13, not 14/15**, and the type keys on the SITE's line-of-fire, not the
> landing tile. Do not build on the landing-tile form below.

Across the 15 CAD v117 games, the first forward turret is a **gunner when the
raider's landing tile is d²≤13 from our core footprint** and a **sentinel when
13 < d² ≤ 32** — **14/15**. The one exception (`2b05487d` g5, 16×16/50 walls,
sentinel at d²=5) is a heavy-wall map where a gunner's ray would be blocked and
a sentinel's is not, which fits the same underlying rule: *pick the turret whose
ray actually reaches our core from here.* This lets the opening arming pick the
counter-ray before the plant lands.

---

# Q1 — Loss mechanism per lost game

All numbers below are recomputed **from `FireTurret` events per shooter**
(gunner 7 dmg, sentinel 18) plus enemy builder attacks (2 dmg) — see the decode
correction in §Method. The ledger closes to **±0 in all 30 games**.

## `2b05487d` (L 2-3, CAD v117, us seat A)

| g | map | result | round | our Ti | their Ti | core dmg | our rot |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 25×25 (4w) | **LOSS** core | r471 | 5,380 | 5,990 | 3,172 | **397** |
| 2 | 10×10 | WIN Ti | r1000 | 14,210 | **0** | 0 | 0 |
| 3 | 26×26 (208w) | **LOSS** core | r463 | 4,810 | 4,940 | 1,620 | **249** |
| 4 | 14×18 | WIN Ti | r1000 | 16,870 | 5,810 | 609 | 3 |
| 5 | 16×16 (50w) | **LOSS** core | r210 | 980 | 1,820 | 1,260 | 0 |

- **g1 — core kill r471.** Killing battery = **gunner #543 @(6,2) SOUTH (r228,
  188 shots, 1,316 dmg, 41%)** and **gunner #577 @(5,2) SOUTH (r238, 184 shots,
  1,288 dmg, 41%)** — both **d²=9 north of our core (5,5)**, both alive at the
  end, **both UNCOVERED and shot at exactly zero times in 240 rounds.**
  Uncovered share of turret damage: **99%**. Home ring options existed: (5,4)N
  and (6,4)N, 60 Ti. We spent 3,970 Ti rotating.
- **g3 — core kill r463.** A **60-round endgame stack**: sentinels #1054 @(11,6)
  r403, #1087 @(9,9) r414, #1125 @(6,11) r428, #1202 @(9,2) r456, plus gunner
  #112 @(8,8) r54. **All five UNCOVERED, 1,620 of 1,620 (100%).** Greedy ring
  cover: 4 sentinels, e.g. (7,7)SE covers two of them.
- **g5 — core kill r210.** **We built nothing at home** (0 turrets at d²≤16 all
  game; our only two turrets were forward, at d²=162 and d²=269). Three CAD
  sentinels — (2,3) r20, (6,1) r149, (0,5) r164 — did **1,260 of 1,260 (100%)**,
  uncovered, unshot. Heal rate 0.60.

## `c6383349` (L 2-3, CAD v117, us seat A)

- **g1 — core kill r230 (28×20/22w).** CAD's r3 sentinel @(12,9) W was
  **covered** by our sentinel #42 @(10,7) SE and killed at r29 — the system
  working. Then CAD planted **six more sentinels between r161 and r223**
  ((12,13), (7,15), (11,5), (12,6), (10,6), (12,5)), **every one uncovered**,
  1,620 of 1,854 (87%). We had 115 rotations (1,150 Ti) on two gunners that
  fired 7 shots between them. **This is the "kill the opener, then stop
  covering" failure — L5.**
- **g2 — core kill r671 (18×18).** Killers: sentinel #686 @(0,14) EAST (r592, 40
  shots, 720 dmg) and #719 @(0,13) SE (r656, 144), plus the r9 opener #23 @(5,11)
  (396). **100% uncovered.** We *had* three home sentinels at d²=5 — #32 (1,12)
  EAST, #43 (4,12) SE, #249 (5,13) EAST — all facing east/south-east, none of
  them on the western column the killers used. **A single sentinel at (0,12)
  facing SOUTH covers both r592/r656 killers (832 dmg).** Meanwhile: 239
  rotations = 2,390 Ti of 2,690 collected; Ti < 10 for 526/672 rounds; heal rate
  0.44 in the death window.
- **g4 — core kill r268 (28×20/122w).** Shortest, most starved: 640 Ti collected
  in 269 rounds, **heal rate 0.13** (16 HP healed against 511 taken in the death
  window), **0 builders adjacent to the core**. Killers gunner #245 @(8,8) SW
  (r220) and #256 @(6,9) E (r227), both **d²=1**, both uncovered, 525 of 579
  (91%). Our one home sentinel #14 @(10,10) faced **EAST — away from our own
  core**.

## `3e8bd0bf` (L 2-3, CAD v117, us seat B)

- **g3 — core kill r403 (21×8).** Gunner #11 @(13,5) NE (r3, 62 shots, 434) and
  sentinel #513 @(11,3) EAST (**r355, on the r3 throw destination**, 24 shots,
  432). **100% uncovered.** 145 rotations = 1,450 Ti of 1,810 collected. In the
  last 60 rounds: **0 builders alive, 0 heals.**
- **g4 — core kill r172 (26×26/208w).** Our gunner #160 @(15,17) NW *did* farm
  CAD's repeated (17,17) plants (4 killed, 4 shots each) — the mechanism works
  — but the three uncovered turrets #277 @(20,17) S (r110), #342 @(15,23) NE
  (r140), #376 @(19,18) S (r156) did **736 of 834 (88%)**. **Nothing built at
  d²≤16 of our core all game.**
- **g5 — core kill r168 (28×20/122w). THE CLEANEST SINGLE-FACING FLIP IN THE
  CORPUS.** We built **three home sentinels at r5/r6/r7** — #14 @(18,10) WEST,
  #16 @(17,11) NORTHWEST, #19 @(19,11) WEST — and CAD's three killers all sat in
  the (16..17, 8..9) block: #12 @(16,9) E (r3, 406), #193 @(17,8) SE (r132, 252),
  #206 @(17,9) E (r139, 196). **Not one killer was on any of our three rays.
  854 of 854 damage, 100% uncovered, zero shots fired at any of them.** Turning
  **#16's facing from NORTHWEST to NORTH** puts (17,10),(17,9),(17,8) on its ray
  — that is **448 of 854 (52%)** for **zero extra titanium**; adding one
  sentinel at (17,8) SOUTHWEST covers the remaining 406. Total cost of the full
  fix: **30 Ti**, in a game where we collected 380.

## `e14bb335` (L 0-5, Lunds v45, us seat B) — the full sweep

Lunds v45 is a **different dialect of the same family** (see §Q3): `convert_ammo(20)`
on r0–r3, launcher at r1 that is **not** self-destroyed at r6, one throw at r3 to
mid-map, and then a very high-volume gunner economy (up to 31 gunners, 980 shots
per game, and 1,530 TLE'd unit-rounds in g1).

- **g1 (26×26, r804).** Their first turret inside d²≤36 arrives at **r232** — we
  had 230 free rounds and used none of them to arm. 10 near-core turrets,
  **all 10 uncovered, 842 of 842 turret damage.** Killers: sentinel #3196
  @(19,22) N (r735, 576) and gunner #3055 @(19,16) S (r699, 266). Died with
  **~9,900 Ti banked** and 2 builders adjacent — a pure heal-detail failure (L3).
- **g2 (18×18, r570).** 3,461 damage, heal 2,955 (0.85). Sentinel #713 @(17,6)
  NW (r373, 84 shots, 1,512) uncovered. Five of our sentinels sat at d²=4–10 of
  our own core, all facing wrong. 73% uncovered share.
- **g3 (16×16/64w, r337).** Two uncovered gunners on **(11,8)/(12,8) facing
  SOUTH** (r228/r294) did 861. We had **six home sentinels** and covered 2 of 8.
- **g4 (14×18, r381).** **Gunner #20 @(6,10) SOUTH, planted r9, fired 281 shots
  into our core over 320 rounds for 1,967 damage (57%), uncovered the whole
  time.** Our sentinel #12 @(7,10) N (r3) sat **one tile away from it** facing
  north; it was on (6,10)'s doorstep and never on its ray. 94% uncovered.
- **g5 (21×8, r1000, tiebreak 5,060–11,920).** The only game we defended
  perfectly (5 of 8 covered, uncovered share **0%**, core 500/500) — and lost the
  economy 2.4:1 while converting **5,130 ammo for 447 shots that put zero damage
  on their core**. Our sentinel #14 @(14,2) W fired 219 shots for 3,942 damage
  into their raiders. **Defence solved, offence and economy wasted.**

## `447e336c` (L 2-3, Lunds v45, us seat A)

- **g1 (28×20/122w, r333).** Gunner #176 @(8,11) NORTH, r129, **203 shots,
  1,421 damage (62%)**, d²=1 from our core, **uncovered for 204 rounds**.
  100% uncovered share.
- **g3 (18×18, r679).** Gunners #38 @(3,13) S (193 shots, 1,351) and #81 @(2,16)
  N (108 shots, 756), both d²=1. In the death window: **0 builders alive, 0
  heals, 487 Ti banked.**
- **g5 (21×8, r1000, tiebreak 5,990–6,580 — a 6-stack margin).** Lunds converted
  **6,980 ammo**, fired **1,717 shots (1,500 onto our core)** for **10,500
  damage**, plus 799 builder attacks (1,598). We healed **12,096 of 12,098** and
  finished at 498/500 — and **lost on titanium by 590.** That heal wall cost
  **3,024 heal actions = 3,024 Ti and 3,024 builder-turns**, i.e. ~50% of our
  income and most of our builder economy, to answer **two uncovered gunners**:
  #234 @(7,2) SW (792 shots) and #447 @(9,3) W (681 shots). **Two ring sentinels
  would have converted a 3,024-turn treadmill into a 60-Ti kill.** This is the
  single strongest argument for L1 in the corpus.

---

# Q2 — the margin flips: what separated our 6 CAD wins from our 9 CAD losses

Means over the 15 CAD v117 games:

| | WIN (n=6) | LOSS (n=9) |
| --- | --- | --- |
| **core separation d²** | **32–81** (all) | **81, then 144–392** (8/9 ≥144) |
| **our rotations** | **5** | **141** |
| rotation share of our income | **3%** | **49%** |
| best home-turret shot count | 38 | 17 |
| best home **sentinel** shot count | 33 | 13 |
| enemy near-core turrets **covered** | 5.8 (47.9%) | 1.8 (**27.6%**) |
| enemy near-core turrets **uncovered** | 6.3 | 4.7 |
| core damage taken | 440 | 1,376 |
| core damage dealt | 386 | 200 |
| our Ti collected | 9,402 | 2,442 |
| their Ti collected | 2,985 | 2,957 |
| game length | 760 rounds | 341 rounds |
| our ammo converted | 684 | 383 |
| their ammo converted | 1,096 | 1,160 |

**Read:** map size and seat do not separate the games; **core separation,
rotation spend, and ray coverage do.** Their behaviour is essentially identical
in wins and losses (their ammo, their shot volume, their establishment count all
overlap) — **the variance is entirely on our side.** That is good news: this is
a self-inflicted bleed, fixable without out-guessing them.

### The closest lost game per match, and the single change that flips it

| Match | Closest lost game | Why it is closest | Single mechanical flip |
| --- | --- | --- | --- |
| `2b05487d` | **g3** (26×26) | Ti 4,810 vs 4,940 (**130 apart**), and we did **452 damage to their core** — our best offensive game vs CAD. Core died r463 to a stack planted r403–r456. | Ring sentinels at **(7,7)SE + (3,8)SE + (7,4)NE**, 90 Ti. Denies 4 of the 5 killers. Game then reaches r1000 as a coin-flip tiebreak (our 1,037 Ti/100rd vs their 1,065) — **UNCERTAIN** whether the tiebreak also flips. |
| `c6383349` | **g4** (28×20/122w) | Their core at **276/500** when ours fell; only 579 damage killed us because the heal line delivered 74. | **Two ring sentinels at (5,9)E and (5,11)NE (60 Ti) + 2 builders parked on the core ring.** Both killers ((8,8), (6,9)) are at d²=1 and were up for 48 and 41 rounds. |
| `3e8bd0bf` | **g5** (28×20/122w) | We already built three home sentinels on r5–r7; all three were mis-faced. | **Change sentinel #16 @(17,11) from NORTHWEST to NORTH.** Zero titanium. Covers 448 of 854 damage. Add (17,8)SW for the rest — 30 Ti total. |

Each of these three matches was 2-3. **One flipped game per match turns
−2.53/−3.71/−3.90 Elo into +2.5/+3.7/+3.9** — roughly +13 Elo swing on the
night's CAD block alone, before any effect on Lunds.

---

# Q3 — CAD v117 vs the frozen v116 opening table

Maps keyed by SHA-1 over `WxH | sorted walls | sorted ore | core positions`.
Four of the five maps in the frozen table (`cad-v116-first-read-2026-08-07.md`
§Q3.B) recur in this corpus.

## Structural invariants — **all survive v116 → v117, 13/13 CAD games with a launcher**

```
r0  convert_ammo(8);  core spawns builder #1 toward the enemy      13/13
r1  convert_ammo(8);  builder #1 builds a LAUNCHER on an orthogonal
    neighbour of its own tile, enemy-facing                        13/13
r2  convert_ammo(8);  launcher THROWS builder #1 toward the enemy  13/13
r3-r5  further throws; first forward turret usually r3
r4  ONE variable surplus conversion                                13/13
r6  the LAUNCHER IS DESTROYED BY ITS OWN TEAM, age exactly 5       13/13
0 splitters, ever                                                  15/15
CAD's launcher never throws an enemy bot                           15/15
```

The two exceptions are the **10×10 maps** (`2b05487d` g2, `3e8bd0bf` g2), where
CAD builds **no launcher at all** and instead plants a gunner from the core at
r1 with a `8/8/24/44/8/48` conversion ladder — the small-map branch the v116
read flagged as D3, now confirmed to still exist in v117.

## Per-map rows

| Map | v117 game | seat | Rows compared | Verdict |
| --- | --- | --- | --- | --- |
| **M3** 28×20/122w, cores (7,9)–(19,9) | `3e8bd0bf` g5 | A (native) | r0/r1/r2/r3 spawns (9,10)/(9,9)/(9,11)/(9,10); launcher **(10,10)**; throws **(15,9)/(15,10)/(13,14)**; r3 **gunner (16,9) EAST**; launcher dead r6 | **BYTE-IDENTICAL to the v116 table on all 9 rows** |
| **M2** 28×20/22w, cores (7,9)–(19,9) | `c6383349` g1 | B (mirror `x→27−x`) | spawns (18,11)/(18,8); launcher **(17,11)**; throws (12,10)/(12,11)/(12,11)/(16,7); r3 **sentinel (12,9) WEST**; launcher dead r6 | **EXACT under mirror on every frozen row — including the D1 "moved" r3 sentinel.** One delta: **four throws, not three** (an extra duplicate to the (15,11)-mirror, and the (11,7)-mirror pushed to r5) |
| **M5** 16×16/50w, cores (0,0)–(14,14) | `2b05487d` g5 | B (180°) | launcher **(13,12)**; throws **(10,8)/(10,8)/(11,15)** | **All three throw destinations and the launcher tile EXACT under rotation.** First-turret row **MOVED** (v116-mirror predicts sentinel (5,4) r13; observed sentinel (2,3) r20) |
| **M1** 14×18/18w, cores (6,4)–(6,12) | `3e8bd0bf` g1 | A (native) | spawns (8,6)/(5,3) ✅; launcher **(8,7)** ✅; throw **(8,6)→(6,11)** ✅; launcher dead r6 ✅ | **6 of 8 rows byte-identical**; the **turret rows moved**: r3 **gunner (5,11) SE** (v116: gunner (7,11) SW), r5 gunner (6,11) S (v116: r4 sentinel (6,10) S) |
| **M1** same | `2b05487d` g4 / `c6383349` g5 | B (mirror `y→17−y`) | launcher **(8,10)** ✅ both | **Throw destination is NO LONGER a constant**: `c6383349` g5 → **(6,6)** (exact mirror of the frozen (6,11)); `2b05487d` g4 → **(8,5)**. Same map, same seat, same version, two hours apart |
| **M3** same | `c6383349` g4 | B (mirror) | launcher **(17,10)** ✅; throws (12,9)/(12,11)/(14,14) — r2 and r4 exact under mirror, **r3 off by one row**; r3 **sentinel (12,10) WEST** (mirror predicts gunner (11,9)) | partial |

### v117 deltas worth acting on

1. **D1 is REAL and is now confirmed as a stable v116/v117 trait, not
   threat-reactive noise.** On M2 the v116 read could not tell whether the r3
   `sentinel (15,9) E` was a code change or a reaction to a different opponent.
   v117, playing the mirror seat against us, produces the exact mirror
   (`sentinel (12,9) W`). **Freeze it.**
2. **The r3 turret type follows a rule, not a table** (L6): gunner when the
   landing tile is d²≤13 of our core, sentinel when 13<d²≤32 — 14/15.
   Both M2 and M3-seat-B land at d²=16 and get sentinels; M1 lands at d²=1–2 and
   gets gunners. This is more robust than freezing tiles.
3. **The launcher tile and the 180°/mirror throw destinations remain the most
   stable rows** (M2, M3, M5 all exact). **M1's throw destination has become
   non-deterministic** — do not freeze it. **UNCERTAIN** cause; the two observed
   destinations are both at d²=1 from our core footprint, so the *invariant*
   ("lands d²=1 from our core on M1") holds even though the tile does not. A
   plausible explanation is that the target must be bot-passable and one of our
   own builders occupied the preferred tile — not verified.
4. **The r4 surplus lump grew.** v116 observed 16/172/186/16/101; v117 shows
   **141, 167, 172, 186, 248, 254, 256**, plus an occasional r5 top-up (4, 12).
   On the 14×18 maps CAD banks **~250 ammo by r4** — 25 sentinel shots or 62
   gunner shots ready before we have converted anything.
5. **On M2, v117 throws four raiders where v116 threw three.** Same destination
   set, one duplicate.

### Lunds v45 is a *sibling table*, not the CAD one

`convert_ammo(20)` on **r0, r1, r2, r3** (10/10 games), launcher built r1 on a
core-adjacent tile (10/10), **launcher NOT self-destroyed at r6 — 0/10** (nine
survive to the final round; one dies at r437), **one throw at r3** to a mid-map
tile (9/10). Do not apply CAD's rows to Lunds.

**And Lunds' surviving launcher ferries OUR builders.** CAD's launcher throws
only CAD bots — **0 cross-team throws in 15 games**, exactly as the ferry
pre-mortem re-check predicted. Lunds' throws **8 of our builders** across three
games. Every one of the 8 moves our bot **away from Lunds' core and back toward
ours** (`e14bb335` g1: our bot #11 picked up at (9,8) and thrown to (12,10)
**four times, at r30/r35/r40/r45** — a 20-round loop that burned that builder's
entire contribution; `447e336c` g5: two bots thrown from (11,4) out to (7,5),
d²=9→50 from their core). This is the **defender's** ferry loop, not an attack
on our home ring — it does **not** threaten L3's parked-builder detail, but it
is a second reason not to send raiders at Lunds (L4).

---

# Q4 — v72 under fire, compared with v68

**The v68 economy defect is fixed. Completely.**

| | v68 vs CAD v116 (`27435b40`) | **v72 vs CAD v117** (15 games) |
| --- | --- | --- |
| last delivery round | **r199, r166** (frozen mid-game) | **r998/r999 in every 1000-round game**; ≥96% of game length in the short ones, **15/15** |
| harvesters alive at end | **0** in two of five | 3–9, **15/15 non-zero** |
| chain-wiredness | 31/78, 10/24, **0/0**, 7/40, 9/62 (~30%) | 29/41, 62/65, 34/51, 30/87, 10/53, 32/38, 20/40, 20/41, 6/7, 31/66, 30/43, 24/31, 20/29, 21/26, 8/18 (**~65%**) |
| Ti collected | 410 / … / **0** / … / 470 | mean **4,700** (380–16,870) |
| out-collected the opponent | 0 of 5 | **7 of 15** |
| our shots per game | 2 / 102 / 52 / 11 / 22 (mean 38) | mean **56**, median 43 |
| their shots per game | 286/166/129/342/287 (mean 242) | mean **210** |
| our:their shot ratio | 0.16 | **0.27** |

So v72 roughly doubled the shot ratio and turned a broken economy into a
competitive one — and still loses 9 of 15. **The bleed moved from economy to
aiming.**

**Does v72 build home coverage? Yes — and it aims it wrong.** v72 builds
**2.6 home sentinels per losing game and 2.4 per winning game** (d²≤36 of our
own core). Presence is not the problem. Coverage is: **27.6% of CAD's near-core
plants covered in the losses vs 47.9% in the wins**, and the tiles that mattered
were covered 0 times in seven of the nine losses. Concretely:

- `c6383349` g4: our only home sentinel faced **EAST, away from our own core**.
- `3e8bd0bf` g5: three home sentinels, r5/r6/r7, **zero killers on any ray**.
- `c6383349` g2: three home sentinels at d²=5, all facing east/south-east; the
  killers came down the western column.

**The C1 question, answered from production data: C1's mechanism is real and
lethal when it fires (89 of 98 covered turrets killed by our turret fire), v72
already pays for the buildings, and it is wasted because the facings are chosen
without reference to where the family actually plants.**

**New v72-specific leak not present in the v68 read: rotate-thrash at scale.**
1,272 rotations / 12,720 Ti in the nine CAD losses (58% of income), against 30
rotations in the six wins. This is the same defect the C1 doc found in v68 g5
(219 rotations), now systemic.

**Engine-health check on our side: clean.** Across all 30 games — **0 TLE rounds
for us, 0 stdout/diagnostic lines, no ancestral pave/launcher crash signature.**
(For contrast, **Lunds v45 TLE'd 1,530 unit-rounds** in `e14bb335` g1 and 15 in
`447e336c` g1.)

---

# Q5 — the KCM contrast win (`9eb8f87a`, 3-2)

Same family, opposite result. Three things differ, in order of size:

1. **KCM v1 does not re-establish.** 25 near-core turrets over 5 games
   (**0.77 per 100 rounds**, vs CAD's 1.72 and Lunds' 1.57) and **zero tile
   re-plants** (CAD: 26; Lunds: 22). When we kill an insertion, it stays dead.
   That is exactly the property L5 says we cannot rely on against CAD — **the
   KCM win is not evidence that our defence works; it is evidence that KCM's
   offence stops.**
2. **We won the games where our coverage held, and lost the two where one
   uncovered sentinel got a long lease.** g2 (21×8, tiebreak loss): sentinel
   #155 @(10,4) EAST lived **r68→r298** uncovered and put **1,710 of 1,803
   (95%)** into our core. g3 (20×26, core kill r164): sentinel #350 @(11,20) NW
   at **d²=2**, uncovered, 306 damage — and 5 of 9 near-core turrets uncovered.
   In the three wins the equivalent turrets were covered and shot.
3. **When the ring is right it is enormous.** g5 (28×20, WIN 22,930–17,080):
   sentinel **#1037 @(17,9) SOUTHWEST, built r295, d²=4 from our core — 284
   shots, 5,096 damage**, plus #13 @(16,10) S (30 shots) and #14 @(21,11) W
   (which two-shot KCM's r5 insertion at (17,11)). Our core finished 500/500.
   g4 (WIN, core kill r87): sentinel #32 @(3,9) SOUTH, 35 shots, **630 damage
   all onto their core** — one correctly-faced sentinel is the whole win.

**Actionable lever from the contrast:** the difference between our KCM record
(3-2) and our CAD record (6-9) is *not* our behaviour — it is that CAD replants
and KCM does not. **Anything we build must survive contact and stay armed for
1000 rounds**, which rules out rotating gunners (they die and cost 10 Ti a
glance) and rules in fixed sentinels rebuilt on the same tile.

---

# Method notes

**Decoder.** `docs/research/2026-08-07-fanout/toolkit/replay_lib.py` under
`.venv/bin/python` (3.13), plus scratch passes `bleed_lib.py` and
`bleed1…bleed11.py` in the session scratchpad (not committed).

**Self-checks — all 30 games pass all of them:** `delivery×10 ==
titaniumCollected`; `ammo converted − spent == engine final ammo`; no unknown
top/turn/update/entity fields; no recycled entity ids; HP within bounds;
**17,837 / 17,837 damage events attributed**; winner consistent with the dead
core.

**Turret counts deduped by entity id** (gunner `rotate()` re-emits `placeEntity`
— docs/tooling.md); rotations reported separately and used as their own signal.

**Launcher throws** detected as `moveBuilderBot` with d²(frm,to) > 1, attributed
to a live launcher at **d² ≤ 2 including diagonals** (the corrected rule).
Attribution was unambiguous for every early-game throw in the corpus.

**Ray-coverage model.** Gunner = *coverable* if the target is row/col/diagonal
aligned, d²≤13, and every intervening tile is free of walls and live buildings
at that round (rotation assumed available, per the C1 law). Sentinel = the
target is on its **build-time facing ray** at d²≤32, obstacles ignored (sentinels
cannot rotate; `rotate()` is gunner-only). "Covered" = some friendly turret
satisfied this at some point in the enemy turret's life; sampled at the first 8
rounds of its life and then on a ≤40-point stride over the rest.

## Two decode-method corrections that should land in `docs/tooling.md`

1. **`rotate()` costs exactly 10 Ti — now measured, not quoted.** 118 rounds in
   which our team's only event was a rotation (no build, no builder action, no
   ammo conversion, no delivery, passive-drip rounds excluded) show a titanium
   delta of **−10 per rotation with zero variance** (112 single, 6 double at
   −20). The C1 doc's 10 Ti/rotate estimate is confirmed; the Ti figures derived
   from it can be quoted as measured.
2. **`replay_lib`'s per-source damage attribution is unreliable when several
   sources hit the same tile in the same round; the aggregate ledger is exact.**
   In `447e336c` g5 the attributor credited **builder_bot #4 with 5,359 of
   12,098** core damage — impossible for a single bot at 2 dmg/action over 1000
   rounds. The independent ledger (`FireTurret` events onto the core footprint ×
   7/gunner, 18/sentinel, plus enemy builder attacks × 2) gives **10,500 turret +
   1,598 builder = 12,098, exact**, and it closes to **±0 in all 30 games**.
   **Recompute any per-turret damage share from `Fire` events keyed by
   `shooter_id`, never from `HpEvent.source_id`.** All per-turret figures in this
   document use the Fire-event method; the §Q1 shares are safe.

## Uncertainty register

- **UNCERTAIN — M1 throw-destination instability.** Two different destinations on
  the same map, same seat, same CAD version, two hours apart. The d²=1 invariant
  holds; the tile does not. Cause not determined (occupancy of the preferred
  tile by one of our own builders is a plausible but unverified explanation).
- **UNCERTAIN — whether flipping the closest lost game flips the match in
  `2b05487d` g3.** Denying the endgame stack pushes it to an r1000 tiebreak that
  the two collection rates (1,037 vs 1,065 Ti per 100 rounds) make a coin flip.
  The `c6383349` g4 and `3e8bd0bf` g5 flips do not have this problem — both are
  core kills against opponents whose cores were already at 276/500 and 500/500
  with the game far from r1000.
- **UNCERTAIN — the coverage classifier's gunner LOS model.** Blockers are taken
  as walls plus live buildings; whether the engine also stops a gunner ray on a
  builder bot standing in the path is not verified from the replay. This can only
  make the "covered" column too generous, so the headline result (**0/147
  uncovered turrets ever shot at**) is unaffected — a stricter model moves
  turrets *into* the uncovered column.
- **Sample size.** CAD v117 = 15 games from 3 matches inside a 2.5-hour window;
  Lunds v45 = 10 games; KCM v1 = 5. The family churns versions hourly (v107 →
  v115 → v116 → v117 within a day). The **structural** invariants have now
  survived v107 → v116 → v117 unchanged and are the safe thing to build on; the
  per-map tile rows are perishable and must be re-checked against their live
  version before anything ships against them.
