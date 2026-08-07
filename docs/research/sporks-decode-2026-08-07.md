# sporks v2 — screen decode

**Thread 1 of `docs/research-brief-2026-08-07b.md`.** Read-only decode of all 25 census-cited
sporks v2 games. Zero replay downloads: all five series were already in `replay_archive/` with
`.meta.json` sidecars. Decoded exclusively with
`docs/research/2026-08-07-fanout/toolkit/replay_lib.py`; self-checks green on every file
(e.g. `ed29909b` g1: delivery 1588×10 == titaniumCollected 15880, ammo 1930−1874 == 56,
1255/1255 damage events attributed).

**Version tag: sporks v2 throughout.** sporks has shipped twice ever (v2 at 1960, #2), so these
findings have long shelf life — unlike Pivot, which shipped twice inside the census window.
sporks is Team A in all five series (confirmed per sidecar).

**Decode validated against the census:** my independent pass reproduces the census's headline
numbers exactly — median first aggression r20, 6.1 tiles from sporks' own core, 9.2 from the
enemy's. Where I disagree below, it is not a measurement difference; it is an interpretation of
the same numbers with more of the distribution in view.

---

## 0. TL;DR — the census's "mid-map sentinel screen" does not exist

The census reads sporks as *"economy-first + defensive combat"* with a *"mid-map sentinel screen
at 0.61 of core separation"*. The 25-game replay evidence says something materially different,
and the difference changes what we should copy.

| Census claim | What the replays show | Verdict |
|---|---|---|
| Sentinel screen at 0.61 of core separation | Turret forward-fraction is **bimodal**, p25 0.45 / p75 0.92, spanning a home ring (0.11–0.38) and a forward line (0.9–1.9). 0.61 is the median of a two-humped distribution, not a placement rule. | **Corrected** |
| Defensive combat line (35% damage on units/turrets) | **91% of sporks' damage lands in the enemy half** (median target forward-fraction **1.00**; only 9% at fwd<0.5). The unit/turret damage is enemy *builders and gunners shot at the enemy's own base*. | **Corrected** |
| The screen protects the farms through the raid window | Farms are **not raided**: median **1** harvester lost in the entire r63-390 window, **0 losses in 12 of 25 games**. Nothing needs intercepting. | **Corrected** |
| Economy-first, 88% core-kill wins | Confirmed. Economy is the engine; the kill is by **gunners in 12/12 core-kill wins**. | **Confirmed** |

**The actual mechanism is a territorial land-grab, not a screen.** sporks pushes its *conveyor
network* across midfield first, plants harvesters on the **enemy's** ore, and puts gunners beside
them to hold the ground it has taken. The single cleanest discriminator in the whole decode:

> **Share of enemy-half ore tiles that sporks farms: 83% in wins, 30% in losses.**

Everything else — the "defensive" damage share, the 0.61 fraction, the high harvester count — is
downstream of that one behaviour.

---

## 1. The screen rule — what it actually is

### 1.1 There is no fixed screen fraction

Turret forward-fraction at build, all 187 sporks gunners+sentinels across 25 games, bucketed by
build round:

| build round | n | median fwd | p25 | p75 | sentinels | gunners |
|---|---|---|---|---|---|---|
| r0-29 | 28 | 0.38 | 0.25 | 0.59 | 17 | 11 |
| r30-59 | 13 | 0.46 | 0.35 | 0.71 | 3 | 10 |
| r60-99 | 21 | 0.87 | 0.64 | 0.93 | 7 | 14 |
| r100-199 | 44 | 0.56 | 0.45 | 0.82 | 27 | 17 |
| r200-399 | 48 | 0.75 | 0.48 | 1.09 | 25 | 23 |
| r400+ | 33 | 0.83 | 0.61 | 1.10 | 15 | 18 |

Pooled median 0.67, p25 0.45, p75 0.92. The census's 0.61 is real as an average and useless as a
rule. The per-game build sequences show the two humps directly
(`ed29909b` g1, forward-fraction in build order):

```
0.24 0.25 0.30 0.19 | 0.75 0.51 1.11 0.75 1.27 1.19 0.82 0.75 0.58 1.10 1.25 0.84 1.42
        home ring   |                    forward line (breakout at r172)
```

### 1.2 The rule: turrets sit at ~2/3 the depth of sporks' own conveyor network

Correlating each turret's forward-fraction against the forward-fraction of sporks' own
economy frontier (furthest-out live conveyor/harvester) at the moment it was built, n=185:

- corr(turret fwd, **own economy frontier** fwd) = **0.510**
- **81% of turrets (149/185) are built at or behind the economy frontier** — the conveyors go out
  first, the guns follow
- median ratio turret_fwd / economy_frontier_fwd = **0.67** (p25 0.46, p75 0.91)

Because sporks routinely runs its economy frontier to ~1.0 and beyond, 0.67 of that frontier lands
at ≈0.61 — which is exactly the number the census measured. **The generating rule is "two-thirds
of the way out along ground my conveyors already own", not "0.61 of core separation".** The
reference object is sporks' own network, not the midline, not the ore line, not a chokepoint, and
not threat bearing.

Secondary confirmation, same dataset: distance from a new turret to the nearest **own conveyor**
is median 2.00 (53% within 2 tiles, 81% within 5), while distance to the nearest **own harvester**
is a looser median 3.61. Turrets track the *trunk*, not individual farms.

### 1.3 Turrets are planted at contact, but the contact is static infrastructure

Distance from a new turret to the nearest **enemy** entity at the moment of build, versus a null
model (random non-wall tile in the same distance-from-own-core band, same round):

| | median | p25 | p75 | ≤2 tiles |
|---|---|---|---|---|
| real turret placements (n=187) | **1.41** | 1.00 | 2.24 | **70%** |
| null model (n=187) | 3.16 | 1.41 | 6.08 | 33% |

The effect is real, but it is not a reaction to raiders. The nearest enemy entity had already been
sitting within 5 tiles for a **median of 79 rounds** (83% for ≥5 rounds; only 5% arrived the same
round), and 81% of those "nearest enemies" are static buildings — 73 conveyors, 51 gunners, 20
harvesters, 8 barriers versus only 27 builder bots. sporks is not intercepting anything; it is
**planting turrets on top of enemy infrastructure it has walked up to.**

### 1.4 Count, facing, rebuild policy

- **Count:** median 3 sentinels + 3 gunners built per game, but the range is 1–17 turrets and
  tracks game length and income, not a target count.
- **Facing:** no fixed facing rule found. Facings are spread across all eight directions, including
  diagonals, and often point along the local conveyor lane rather than at the enemy core.
- **Rebuild:** sporks **never recycles its own turrets** — 0 of 46 turret deaths across 25 games
  were self-`destroy()`; all 46 were killed by enemy damage. Only **7 of 187** turrets were rebuilt
  on a tile that had previously held one. **The line does not get repaired or re-formed; it gets
  extended.** 25% of turrets die and are simply abandoned in place.

### 1.5 The map rule that beats all of the above

| map geometry | sporks record |
|---|---|
| cores offset on a **cardinal** axis (dx==0 or dy==0) | **9W-0L** |
| cores offset **diagonally** | **6W-10L** |
| core separation ≤12 | 10W-1L |
| core separation ≥17 | 5W-9L |

Every sporks loss in the 25-game sample is on a diagonal map (`ed29909b` g2/g4/g5, `27e06fce`
g2/g5, `73afd924` g3/g4/g5, `abb34d36` g3/g4). Nine of nine cardinal-axis games are wins. This is
a stronger predictor than any turret-placement statistic in this document, and it is the direct
consequence of §1.2: a conveyor trunk pushed down a single cardinal lane is defensible and short;
the same trunk on a diagonal is longer, forks into two approach lanes, and the turret line at 0.67
depth cannot cover both.

---

## 2. Advance / retreat triggers

**The line never retreats.** No self-destroy, no rebuilding rearward (§1.4). The only motion is
forward extension by adding turrets.

**The advance trigger is ammo at cap with the core repaired to full.** State at the round each game
plants its first turret past 0.9 forward-fraction:

| game | round | fwd | Ti | **ammo** | harvesters | our core HP |
|---|---|---|---|---|---|---|
| `ed29909b` g1 | 194 | 1.11 | 82 | **60** | 12 | 500 |
| `ed29909b` g3 | 174 | 1.25 | 33 | 41 | 9 | 312 |
| `27e06fce` g3 | 22 | 0.92 | 141 | 40 | 2 | 407 |
| `73afd924` g1 | 716 | 1.13 | 84 | **60** | 18 | 500 |
| `c96904fa` g2 | 78 | 1.36 | 55 | 56 | 8 | 500 |
| `c96904fa` g3 | 92 | 0.93 | 124 | **60** | 14 | 500 |
| `c96904fa` g4 | 64 | 0.92 | 86 | 41 | 5 | 500 |
| `c96904fa` g5 | 65 | 1.17 | 60 | 55 | 6 | 499 |
| `abb34d36` g1 | 279 | 0.97 | 77 | **60** | 6 | 499 |
| `abb34d36` g2 | 258 | 1.17 | 174 | **60** | 13 | 500 |
| `abb34d36` g5 | 98 | 0.93 | 61 | 56 | 9 | 500 |

Ammo at the advance is 40-60 (median 56) against a hard cap of 60; titanium is *low* (median 77).
**sporks advances on a full ammo bank, not on a titanium surplus** — it spends titanium down to
near zero and treats banked ammo as the go/no-go.

The clearest single instance is `ed29909b` g1, where the trigger fires visibly:

| round | harv | conv | Ti | ammo | delivered | **core HP** | eco frontier | **turret frontier** |
|---|---|---|---|---|---|---|---|---|
| 24 | 4 | 15 | 10 | 27 | 80 | 475 | 0.65 | 0.24 |
| 96 | 4 | 27 | 102 | 60 | 800 | 469 | 0.90 | 0.25 |
| 144 | 7 | 32 | 263 | 60 | 1530 | **387** | 0.90 | 0.30 |
| 168 | 10 | 36 | 343 | 60 | 2110 | **500** | 0.90 | 0.30 |
| 192 | 12 | 41 | 182 | 60 | 2770 | 500 | 0.90 | **0.51** |
| 216 | 15 | 46 | 171 | 50 | 3510 | 500 | 0.90 | **0.75** |
| 240 | 17 | 58 | 163 | 60 | 4330 | 500 | **1.51** | **1.27** |

The core is chipped to 387 by r144, healed back to 500 by r168, and the turret line advances on the
very next sample. It then locks at 1.27 — past the enemy core — for the remaining 288 rounds while
the economy frontier creeps to 1.77 and delivery runs to 15880.

---

## 3. Defensive damage share — who, where, at what range

Pooled damage sporks **dealt**, 25 games, 36 592 HP:

| source | HP | share | | target | HP | share |
|---|---|---|---|---|---|---|
| gunner | 19 520 | **53.3%** | | core | 11 075 | 30.3% |
| sentinel | 11 817 | 32.3% | | conveyor | 9 221 | 25.2% |
| builder melee | 5 255 | 14.4% | | builder_bot | 8 217 | 22.5% |
| | | | | gunner | 3 898 | 10.7% |
| | | | | harvester | 2 580 | 7.1% |
| | | | | barrier / launcher / sentinel | 1 601 | 4.4% |

Bucketed: core 30% / economy 34% / military 35% — reproducing the census exactly. **But the
location tells a different story than the label.** Forward-fraction of the *target* of every
damage event:

| | median | p10 | p25 | p75 | p90 | share landing at fwd<0.5 |
|---|---|---|---|---|---|---|
| all sporks damage | **1.00** | 0.51 | 0.75 | 1.01 | 1.25 | **9%** |

By round bucket:

| bucket | n | median target fwd | share in own half | core% | builder% | eco% |
|---|---|---|---|---|---|---|
| r0-49 | 310 | 0.64 | 27% | 4% | 35% | 23% |
| r50-99 | 806 | 0.93 | 12% | 25% | 14% | 45% |
| r100-199 | 1483 | **1.00** | 9% | 34% | 17% | 31% |
| r200-399 | 2049 | **1.00** | 8% | 27% | 21% | 45% |
| r400+ | 1373 | **1.00** | 8% | 40% | 29% | 22% |

The "35% defensive damage share" is an artefact of *what* is being shot, not *where*. From r100
onward sporks is shooting **at the enemy's base** — the 22.5% of damage on enemy builder bots is
sporks' forward gunners killing the enemy's construction crews on their own ground.

**Engagement ranges** confirm the class of each weapon:

| source | n hits | median range | max range |
|---|---|---|---|
| gunner | 2 782 | **2.00** | 3.61 (= r²13 ✓) |
| sentinel | 665 | **4.00** | 5.66 (= r²32 ✓) |
| builder melee | 2 574 | 1.00 | 1.00 |

**Counterbattery does exist, and it is the sentinels' job.** Of 4 730 HP sporks put onto enemy
turrets, sentinels supplied 3 078 (65%) and 47% of it landed in sporks' own half. Of 106 enemy
turrets planted inside sporks' half, sporks destroyed **60 (57%)** — but took a **median 49 rounds**
to do it. That is not interception; it is slow grinding while the heal line keeps the core alive.

**The role split falls straight out of the win/loss damage mix:**

| source | share in WINS (15) | share in LOSSES (10) |
|---|---|---|
| gunner | **55.7%** | 27.9% |
| sentinel | 30.9% | **47.9%** |
| builder melee | 13.5% | 24.2% |

**Sentinels = home counterbattery. Gunners = the forward land-grab escort and the core kill.**
A sentinel-heavy damage profile is the signature of sporks being *pinned at home and losing*.

---

## 4. Economy scaling behind the line

**Hard opening constants — 25/25 games, standard deviation 0:**

- **`convert_ammo(17)` on round 0.** Every game. 17 Ti → 17 ammo, before anything else.
- **Five builder bots spawned on rounds 0, 1, 2, 3, 4.** Every game, no exceptions.
- First harvester r2-r10; first conveyor r3-r9.
- **Zero splitters built in all 25 games.**

**Builder population is a two-stage function.** Five builders always; a second wave only in long
games (`ed29909b` g1: +21 from r153; `27e06fce` g1: 39 total, second wave from r244). Nine of ten
losses ran on the opening five and never spawned a sixth — but two wins did too (`73afd924` g2,
`abb34d36` g5), so builder count is a *consequence* of income, not an independent lever.

**Conveyor topology is long trunk lines, not short manifolds.** 6-7 conveyors per harvester in
every deep game (`ed29909b` g1: 222 conveyors / 32 harvesters = 6.9; `27e06fce` g4: 6.0;
`c96904fa` g4: 6.2), with median conveyor distance from own core 9.2-9.8 and **max 20.9-21.9 on
maps whose whole core separation is 12-19.8**. The network crosses the map.

**Harvester cadence is opportunistic, in waves keyed to territory, not to a fixed schedule.**
`ed29909b` g1 builds at r2, 8, 12, 17, 38 — then nothing until **r127**, then 27 more. The pause
r38-127 is exactly the pinned phase; the second wave starts when the line advances.

**Where the harvesters go is the whole story:**

| | median harvester fwd | harvesters beyond midfield | **share of enemy-half ore farmed** |
|---|---|---|---|
| **WINS (15)** | **0.71** | 15 | **83%** |
| **LOSSES (10)** | 0.45 | 4 | **30%** |

In `ed29909b` g1, **22 of 32 harvesters sit past midfield** and 9 sit past forward-fraction 0.9,
with a maximum of 1.77 — well behind the enemy core. sporks farms the enemy's ore.
(Caveat: the share can exceed 100% where a forward harvester died and was rebuilt on the same
tile — `c96904fa` g2 reads 104%. Treat it as a capture *rate*, not a strict share.)

---

## 5. THE KEY QUESTION — how it survives the farm-death window (r63-390)

**It survives because its farms are never attacked.** Harvesters lost by sporks in the entire
r63-390 window, per game across all 25:

```
0 0 0 0 0  3 2 0 0 0  2 0 1 1 4  0 1 1 0 9  1 0 1 2 2      median 1, zero in 12/25 games
```

Total across 25 games: 387 harvesters built, 46 lost (12%), of which 30 fell inside the window.
There is no interception mechanism because there is nothing to intercept. **Two structural reasons:**

**(a) The two sides pass each other.** sporks farms forward (median harvester fwd 0.71); the
battery/picket classes walk to sporks' *core*. They cross without engaging the thing that matters.
In `ed29909b` g1, only **10 enemy entities ever came within 6 tiles of sporks' core** in 528 rounds,
the last at r225 — and 22 of sporks' 32 harvesters were past midfield, behind the enemy's advance.

**(b) Conveyor mass is ablative armour, and it is repaired.** Against team lazy v88 in `ed29909b`
g1, team lazy dealt 5 768 HP and spent it like this:

> **conveyor 3 794 (66%)**, core 1 176 (20%), sentinel 371 (6%), builder_bot 329 (6%),
> **harvester 49 (1%)**, barrier 49 (1%)

Two thirds of the enemy battery's entire output went into 3-Ti conveyors. Only 1% touched a
harvester. sporks lost 101 conveyors in that game and kept building; the network absorbed the raid.

### 5.1 The answer to "does sporks just tank it and out-economy?" — yes, and it heals

**`ed29909b` g1 (vs team lazy v88, 28x20, sep 12, sporks W by core kill @r528).** team lazy's
gunners reached sporks' core early — gunner id40 at (10,7) dist 3.6 on **r12**, id51 r15, id79
r23, id137 r44, id146 r47 (sporks core at (7,9)). sporks' core HP response:

> r0 500 → r50 461 → r100 466 → **r150 369** → **r200 500** → and 500 for every sample through r527.

sporks healed **1 176 HP back onto its own core** and **1 496 HP onto its conveyors** — 723 heal
actions, 2 892 HP total, at 1 Ti per action = **723 Ti, i.e. 4.6% of the 15 880 Ti it delivered
that game.** Survivability cost it under a twentieth of its income.

It also counterbatteried, slowly: 57% of enemy turrets planted in its half died, median 49 rounds.
The heal outran the damage; the counterbattery merely cleaned up afterwards.

**The contrast game is `ed29909b` g4** (16x16, diagonal, sep 19.8, sporks **L** @r64). team lazy
dealt 504 HP, **100% of it to the core**. sporks had 4 harvesters, 26 conveyors, **zero heal
actions all game**, and ammo starved to 1. Core 500 → 178 (r50) → 0 (r63). No conveyor mass to
soak, no heal line, no ammo. The identical opponent, 464 rounds shorter.

### 5.2 Heal and ammo are the survival discriminators, and they are cheap

| | WINS (15) | LOSSES (10) |
|---|---|---|
| median heal actions | **290** | 84 |
| median core HP healed back | **188** | 42 |
| median core minimum HP | 378 | 0 |
| median ammo converted | **1 142** | 125 |
| median `convert_ammo` calls | **170** | 13 |
| median conveyors built | 118 | 72 |

The ammo cadence is not a game-length artefact: per-round conversion rate is 0.18-0.64 calls/round
in wins versus 0.04-0.21 in losses.

**Ammo policy, pooled (2 622 conversions, 18 947 Ti):**
- **Hard cap 60.** Max ammo held is exactly 60 in 24 of 25 games; pooled median holding 54.
- **Top-ups of 4** — 1 311 of 2 622 calls (50%), i.e. **exactly one gunner shot at a time**,
  then 10 (337), 8 (226), 14 (145).
- Median titanium *held* is 97 while median ammo held is 54: sporks keeps the bank empty and the
  magazine full.

Two extreme survivals worth citing: `27e06fce` g1 healed **4 444 HP onto its own core** over 1 000
rounds (1 195 heal actions) and won on titanium; `ed29909b` g3 took its core to **9 HP**, healed
3 492 HP back, and won at r1000 on titanium with 35 harvesters and 10 910 Ti.

---

## 6. Screen-to-kill transition

**The kill is always gunners, always slow, and always begins from an already-won economy.** All 12
core-kill wins in the sample:

| game | end | first core dmg | sustained kill starts | kill duration | harv alive | conv alive | Ti | **ammo** | turrets within 6 of enemy core | killers |
|---|---|---|---|---|---|---|---|---|---|---|
| `ed29909b` g1 | 528 | 456 | 456 | 72 | 29 | 115 | 1031 | 56 | 4 | gunner 72 |
| `27e06fce` g3 | 657 | 26 | 597 | 60 | 8 | 34 | 196 | 56 | 5 | gunner 57 |
| `73afd924` g1 | 770 | 723 | 723 | 47 | 18 | 81 | 86 | 46 | 2 | gunner 47, sentinel 11 |
| `73afd924` g2 | 218 | 78 | 78 | 140 | 2 | 7 | 52 | 13 | 3 | gunner 138 |
| `c96904fa` g1 | 162 | 66 | 66 | 96 | 4 | 16 | 53 | 56 | 2 | gunner 72 |
| `c96904fa` g2 | 421 | 283 | 283 | 138 | 22 | 98 | 178 | 46 | 6 | gunner 116 |
| `c96904fa` g3 | 181 | 95 | 95 | 86 | 14 | 47 | 107 | 46 | 2 | gunner 86 |
| `c96904fa` g4 | 485 | 66 | 384 | 101 | 23 | 132 | 78 | 46 | 6 | gunner 101 |
| `c96904fa` g5 | 296 | 67 | 214 | 82 | 11 | 61 | 221 | 56 | 2 | gunner 78 |
| `abb34d36` g1 | 423 | 285 | 285 | 138 | 6 | 69 | 60 | 56 | 1 | gunner 138 |
| `abb34d36` g2 | 591 | 317 | 317 | 274 | 13 | 73 | 203 | 56 | 5 | gunner 274 |
| `abb34d36` g5 | 279 | 59 | 59 | 220 | 6 | 28 | 44 | 52 | 1 | gunner 211 |

**What flips it:**

1. **Ammo at the cap, titanium near zero.** Ammo at kill-start is 46-56 in 11 of 12 games; titanium
   is 44-221 (median ~100). Same trigger as the advance (§2) — sporks does not distinguish
   "advance" from "kill", it just keeps extending until the enemy core is inside gunner range.
2. **There is no kill squad.** Median **2.5 turrets** within 6 tiles of the enemy core at kill-start
   (range 1-6). One or two gunners parked at r²13 grind 500 HP down over **47-274 rounds**
   (median 98.5). At 7 damage per shot on reload 1, two gunners need ~36 rounds of uninterrupted
   fire per 500 HP — the long durations are firing gaps, not a burst.
3. **It is the conveyor trunk arriving, not a raid being launched.** Kill-start correlates with the
   economy frontier having reached ≈1.0 (`ed29909b` g1: turret frontier locked at 1.27 from r240,
   core damage starts r456). The gunners were already there, escorting harvesters; the enemy core
   simply ends up inside their arc.

**The 88% core-kill share is therefore not an offensive mode at all.** It is the land-grab running
to completion. The three r1000 games are the same behaviour on maps where the grab stalled
(`27e06fce` g1 and g4 both hold a static frontier for 900+ rounds and win on titanium; g4's core
never drops below 500 for the whole 1 000 rounds).

---

## 7. Portability verdict per mechanism

Cross-referenced against our shipped/queued pieces: **D** duel discipline, **J** heal-dispatch
reorder / counterbattery, **B'** population floor, **H** endgame spend-switch.

| # | sporks mechanism | Evidence | Portable to Eir? | Relation to our pieces |
|---|---|---|---|---|
| **1** | **Ammo cap 60, top up 4 Ti/round, advance only when full** | 25/25 `convert_ammo(17)` at r0; cap 60 in 24/25; 50% of 2 622 calls are size 4; ammo 40-60 at every advance and 46-56 at 11/12 kill-starts | **YES — highest value, lowest cost.** A standalone core-side policy: ~15 lines, no architecture dependency. | **Contradicts piece I's premise indirectly**: our measured 4 460 Ti of *rotation* thrash (56.5% of income worst case) versus sporks' entire 18 947 Ti of ammo across 25 games. Composes with **H** — H's endgame spend-switch needs a spend target, and "ammo to cap" is a measured-good one. |
| **2** | **Heal the core and the trunk, continuously, as an income line-item** | `ed29909b` g1: 723 heals = 723 Ti = 4.6% of income, core restored 369→500 and held 328 rounds; wins 290 heals vs losses 84 | **YES — this is piece J's real target.** | **J approximates it but is scoped too narrowly.** J reorders heal above role dispatch so someone reaches counterbattery. sporks says the *heal itself* is the survival mechanism and counterbattery is the slow cleanup (median 49 rounds to kill an intruding turret). Recommend J's spec widen from "unblock counterbattery" to "sustain core+trunk HP as a standing budget of ~5% of income". |
| **3** | **Conveyor mass as ablative armour** | 66% of team lazy's entire 5 768 HP output went into 3-Ti conveyors; 1% touched a harvester (`ed29909b` g1); 101 conveyors lost, network kept building | **YES, cheaply** — and it is nearly free, since we want the conveyors anyway. | Nothing in our line covers this. It is the structural answer to the r63-390 farm-death window that **B'** only treats symptomatically. |
| **4** | **Farm the enemy's ore (land-grab)** | Wins take 83% of enemy-half ore, losses 30%; 22/32 harvesters past midfield in `ed29909b` g1 | **NO — requires their whole architecture.** | Needs the trunk network, the escort doctrine, and the heal line all at once. **Contradicts D**: D forbids solo melee into a live gun's ray, and forward farming means builders working permanently inside enemy turret arcs. Do not attempt piecemeal. |
| **5** | **Turrets at 0.67 of own-network depth, never repaired, only extended** | corr 0.51 with economy frontier; 81% built at/behind it; 0/46 self-recycled; 7/187 rebuilt on-tile | **NO — dependent on #4.** The rule is meaningless without a network to measure depth against. | **Contradicts our SLOT_HOME_GUN monotone fix** (rubble counting as a live gun): sporks deliberately abandons dead turrets rather than rebuilding the slot. Worth noting as an alternative doctrine, not a port. |
| **6** | **Sentinel = home counterbattery, gunner = forward escort + kill** | Sentinels 65% of anti-turret damage, 47% in own half; gunners 12/12 of core kills; wins gunner 55.7% / losses sentinel 47.9% | **PARTIAL — the role split ports, the geography does not.** | Directly relevant to **J**. Our profile is a *sentinel* core battery (census §3.1: sentinel at (9,3) shooting the enemy core on r3). sporks uses sentinels defensively and gunners offensively — the exact inverse of our shipped line. Flag as a hypothesis to test, not a confirmed win. |
| **7** | **Five builders at r0-4, second wave only when income allows** | 25/25 at rounds 0,1,2,3,4; 9/10 losses never spawned a sixth | **PARTIAL.** | **B' is aimed at the right symptom with the wrong constant.** Our floor is REPLACE_TI_FLOOR=250, unmeetable mid-strangle; sporks' effective floor is 5 and it only expands on realised income. Recommend B' re-spec: floor of 5, expansion gated on delivered-Ti rate rather than a titanium threshold. |

### 7.1 Top recommendation

**Port mechanism #1 (ammo cap 60 / top-up 4 / advance-on-full) and re-scope piece J toward
mechanism #2 (heal as a standing ~5% income budget).** Both are core-side or dispatch-side policies
with no dependency on sporks' land-grab architecture, both are measured across 25 games with
standard deviation 0 on the opening constants, and together they are the entire difference between
`ed29909b` g1 (723 heals, 231 ammo conversions, core held at 500 for 328 rounds, win) and
`ed29909b` g4 (0 heals, 5 conversions, core dead at r63, loss) — **against the identical opponent
in the same series.** That opponent class, point-blank gunner core battery, is 44% of our matched
pool.

### 7.2 Do not copy

The land-grab (#4) and the network-relative turret rule (#5) are one indivisible mechanism and
**they are why sporks loses 10 of its 16 diagonal-map games.** The census's "study it, do not
imitate it" is correct, and now has a specific reason: sporks' architecture buys a 9W-0L record on
cardinal maps at the price of 6W-10L on diagonal ones. We do not get to choose the map.

---

## 8. Caveats and not-run list

- **Sample:** 25 games, five opponents, all top-8, all with sporks in **seat A**. No seat-B sporks
  games exist in the archive, so any seat asymmetry in its behaviour is unmeasured.
- The 9W-0L cardinal split rests on 9 games; the direction of the effect is unambiguous but the
  magnitude is one sample's worth. Cardinal maps in this sample are also the low-separation ones
  (12.0 and below except `c96904fa` g5), so **axis and separation are confounded** and this decode
  cannot separate them.
- Damage `source_*` attribution is `replay_lib`'s documented heuristic (trap 10), not a file field.
  It reconciles exactly against ammo conservation on every game here, but the per-source splits in
  §3 inherit that heuristic.
- **The comms store is invisible in replays** (trap 9), so the role split in §3 and §7 is inferred
  from behaviour, not read from sporks' coordination channel. sporks emitted no stdout.
- **Not run:** no fresh `match info`/`match replay` calls were needed (0 of the 8-download budget
  used). No decode of sporks against mid-pool opponents — the census cites only top-8 series, so
  how sporks behaves against the battery/picket classes *we* actually face is untested outside
  `ed29909b`. No cross-check of the cardinal/diagonal finding against other teams' records on the
  same maps, which would tell us whether it is a sporks property or a map property.

---

*Read-only: no bot edits, no submissions, no activations, no arena runs, no unrated challenges.
All 25 games decoded from `replay_archive/` with `toolkit/replay_lib.py`; zero replay downloads.*
