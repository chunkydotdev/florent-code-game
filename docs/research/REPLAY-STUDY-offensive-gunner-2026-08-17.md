# REPLAY STUDY: the offensive economy-shredder gunner (2026-08-17, s48)

**PROVENANCE.** Opus replay-study subagent, commissioned by the builder on
Magnus's directive, verbatim: *"Today we're experimenting with an offensive
gunner that shreds the enemy economy by cutting conveyors and everything other
than the core. A well placed gunner in a base can rotate and kill more conveyors
left and right and up. A lot of the top teams do this, look at their games and
figure out how to do it optimally."*
Method per `docs/research/PLAYBOOK-move-mining-2026-08-16.md`.
Written 2026-08-17T04:49Z (`date -u`, same shell), repo at `75b098a3`.
**Ground:** the whole local archive — 58,087 `.replay26` files, decoded fresh for
this study with a purpose-built full-state walker (not `builds.tsv`, which has no
shot attribution). Corpus manifest `built_utc 2026-08-17T04:22:55Z`.
**Incumbent diffed against:** v155 "Sleipnir v1" = `bots/_v468kladturbo`, plus a
source-tree archaeology pass over v94/v102/v116/v125/v140 (§5.1) commissioned by
this study — the replay half and the source half were run blind to each other and
agree on v94's failure mode.

Every claim below is tagged **MEASURED** (counted off decoded events, with the
denominator), **EYEBALL** (seen in ≤3 games, needs a count), or **INFERRED**
(mechanism guess from the engine rules). Seven steering updates from the research
lane arrived mid-study and are folded in; where research already measured
something corpus-wide it is CITED, not re-derived.

---

## 0. INSTRUMENTS AND THEIR CONTROLS

Four instruments were built. None was trusted before it was driven to the other
verdict.

**I1 — seat mapping (replay team index → platform team name).**
Non-circular check: the replay binary's `winner` field vs the platform's
`game_winner_side` from `meta_join.tsv` — two independent sources.
**56,660 of 56,660 agree (1.00000), 0 rows without a winner.** MEASURED.
(The usual circular check — `join.our_team` vs `meta_join.us_side`, 4,450/4,450 —
was ALSO run and is worthless: both descend from `winnerSide`, TRAP 7.)

**I2 — shot attribution.** A `fireTurret(from,to)` is credited to the entity
standing on `from` at **round start** (the S1 ordering trap in
`tools/replay_schema.md`); its victim is the round-start occupant of `to`, unit
before building (the damage-target law); a kill is credited only when that victim
id is `removeEntity`d in the SAME round AND no second shooter targeted the tile.
* **Control that must run the other way:** jitter the target tile by ±1 / ±3 and
  re-run. Econ kills per 1000 gunner shots collapse
  **137.2 → 13.8 → 2.5** (Pantheon, 6,399 shots) and **115.8 → 8.0 → 1.1**
  (O(1), 872 shots). MEASURED.
* **Independent dose check:** a gunner that killed a core did it with **72 core
  hits** in the first file inspected — 72 × 7 dmg = 504 ≥ 500 HP, i.e. the
  attribution reproduces the engine's damage constant without being told it.
* **Range check, MEASURED:** over 16,520 Pantheon gunner shots the observed
  d²(gunner,target) takes exactly the values **{1, 2, 4, 8, 9}** — cardinal to 3
  tiles (d²=9), diagonal to 2 (d²=8), nothing above 13. And **100.0%** of shots
  lie on the gunner's *current* facing ray. The facing tracker and the r²=13
  pattern validate each other.

**I3 — rotation tracking.** `placeEntity` re-emitted for a live entity id with a
CHANGED `direction` = a `rotate()`. (Re-emits with an unchanged direction are not
counted; this is conservative.) Sanity: the teams whose code obviously never
rotates read exactly 0.00 rotations/gunner (Leviathan v55 0.23, Klarum 0.00,
Part-timers 0.00), while our own v102 reads 5.27 — the instrument separates.

**I4 — throughput.** `distributeResources` moves whose `to` lands on a core
footprint tile = one 10-Ti stack delivered (`replay_schema.md` verifies this
equals `titaniumCollected` exactly on 56 team-sides).
* **Control that must run the other way:** a **placebo event study** at
  (first-forward-gunner round − 100), windows constrained not to overlap the real
  event. Reported alongside every real estimate below. It kills one of the four
  teams' claims, which is the point.

---

## 1. CENSUS — who does this, and what the payoff column says

The *forward-planting* half of the census is **already answered corpus-wide by
the research lane** (525,904 gunner BUILD events; 71-team median 5.13
gunners/game, 0.667 within d²<100 of the enemy core, 0.565 closer-to-theirs;
our v155 at the floor, 1.71/game and 0.071 closer-share). **Cited, not
re-derived.**

What that cut could not carry is the **payoff** column, because `builds.tsv` has
no shots. Here it is. **Population:** every archived replay whose
`meta_join.completedAt` ≥ 2026-08-14 (the current era), all opponents pooled,
team-games as the denominator. Teams with <100 team-games or <20 gunners in the
era are dropped. **MEASURED.**

| team (era rating) | team-games | gun/g | fwd share | shots/g | **rot/gun** | **econ kills/g** | **econ kills /1000 shots** | econ share of shots | core share of shots |
|---|---|---|---|---|---|---|---|---|---|
| Ouroboros | 415 | 24.41 | 0.57 | 371.8 | 4.38 | **38.47** | 103.5 | 0.397 | 0.191 |
| Besvikomat | 470 | 9.68 | 0.65 | 235.9 | 3.70 | 29.37 | 124.5 | 0.442 | 0.235 |
| Landers | 252 | 9.63 | 0.57 | 152.9 | 0.54 | 18.15 | 118.8 | 0.496 | 0.155 |
| **Pantheon (1988, #8)** | 529 | 8.14 | **0.89** | 120.2 | **0.61** | **16.74** | **139.2** | **0.526** | 0.254 |
| Clankers (1901, #11) | 380 | 4.19 | 0.69 | 113.7 | 3.09 | 14.00 | 123.1 | 0.509 | 0.100 |
| Pivot (2076, #4) | 1484 | 7.86 | 0.51 | 166.7 | 1.00 | 13.04 | 78.2 | 0.393 | 0.315 |
| **ph (2037, #7)** | 806 | 5.88 | 0.63 | 118.6 | 1.09 | 13.02 | 109.7 | 0.548 | 0.109 |
| team lazy (1811) | 746 | 4.57 | 0.43 | 96.3 | 0.82 | 9.85 | 102.3 | 0.442 | 0.054 |
| HTTP 418 (1805) | 681 | 6.86 | 0.60 | 142.0 | 2.16 | 9.58 | 67.5 | 0.286 | 0.257 |
| Erebus (1800) | 1698 | 8.10 | 0.57 | 194.7 | 0.58 | 9.23 | 47.4 | 0.259 | 0.298 |
| Lorem Ipsum (2077, #3) | 1290 | 5.74 | 0.67 | 95.0 | 0.99 | 7.88 | 82.9 | 0.437 | 0.351 |
| not adgato (1887) | 469 | 6.29 | 0.62 | 112.4 | 0.84 | 7.94 | 70.6 | 0.250 | 0.460 |
| Bean counters (2087, #2) | 633 | 3.44 | 0.30 | 46.1 | 0.65 | 3.46 | 75.2 | 0.357 | 0.055 |
| farming_200s (1896) | 434 | 2.06 | 0.95 | 69.7 | 0.91 | 2.15 | 30.8 | 0.119 | 0.652 |
| **sporks (2058, #5)** | 882 | 2.17 | **0.87** | 64.1 | 1.24 | 2.13 | 33.3 | 0.147 | **0.730** |
| 0033 (—) | 1621 | 2.32 | 0.60 | 35.4 | 2.09 | 1.61 | 45.4 | 0.204 | 0.452 |
| **O(1) (2038, #6)** | 948 | 0.88 | 0.93 | 8.8 | **0.13** | 1.08 | **122.9** | **0.801** | 0.087 |
| Jython (2212, #1) | 1265 | 1.33 | 0.35 | 24.6 | 2.04 | 1.02 | 41.6 | 0.205 | 0.123 |
| **OpenSverige (1817, us, v125-v155)** | 3344 | **0.70** | **0.03** | **10.7** | 2.84 | **0.19** | 17.5 | 0.095 | 0.019 |
| The Bisons (1808) | 548 | 0.40 | 0.47 | 15.6 | 0.00 | 0.18 | 11.2 | 0.078 | 0.787 |
| lingling_40h (1771) | 557 | 1.96 | 0.69 | 66.4 | 0.27 | 0.11 | 1.6 | 0.009 | 0.771 |
| diverge | 400 | 0.55 | 0.92 | 29.0 | 0.00 | 0.00 | 0.0 | 0.001 | 0.989 |

**Three things this table says that the forward-share census cannot.**

1. **"Forward gunner" and "economy shredder" are DIFFERENT PLANKS.** sporks,
   farming_200s, diverge, The Bisons and lingling_40h all plant forward at
   0.87-0.95 and put **73-99% of their shots into the enemy CORE**. Pointing at
   the belt is a separate decision, and it is the one the directive is about.
2. **The best belt-shredders are mid-table-to-high, not the #1 team.** Jython
   (2212) is at 41.6 econ kills/1000 with 1.33 gunners/game. Pantheon (#8) is the
   top-rated genuine shredder.
3. **We are at the floor on BOTH axes**: 0.70 gunners/game, 3% forward, 0.19 econ
   kills/game, and 17.5 econ kills/1000 shots — the lowest efficiency of any team
   in the table that fires at all.

⛔ **ERA CORRECTION, and it matters for subject selection.** The steering update
named **Leviathan** as the volume pole (14.18 gunners/game). That is a
**pre-v74 fact**. MEASURED per version, in the archive:

| Leviathan version | team-games | gunners/g | sentinels/g |
|---|---|---|---|
| v35 | 99 | 21.07 | 3.49 |
| v55 | 308 | 15.25 | 3.61 |
| v62 | 80 | 14.15 | 6.42 |
| **v74 (current-1)** | 344 | **0.00** | 8.58 |
| **v76 (current)** | 386 | **0.00** | 9.87 |

**Leviathan's current bot builds ZERO gunners in 386 team-games** and replaced
them 1:1 with sentinels. A rotation-policy read of Leviathan is not possible and
the request for one is void. (This is exactly the staleness the ledger's
"a new version is a new bot" rule exists to catch.)

**Subjects chosen on the payoff column instead:**
* **Clankers v17** — research's re-ranked best subject (in-band share 0.404,
  excess 3.95) and our stable-opponent deficit cell.
* **Pantheon v91** — top-rated true shredder, 139.2 econ kills/1000, 89% forward.
* **O(1) v24** — 80.1% of shots on economy, the most *selective* shredder, and
  the only one whose games look like our programme (median 147 turns).
* **sporks v24** — the core-sniper contrast (the steering update's siting-rule
  pick; kept, because it turns out to be the discriminating negative control).
* **ph v42** — replication.
* **OpenSverige v94** — our own removed forward gunner, the before/after control.

⚠ **RECONCILIATION with research's excess-belt-kill ranking, because it scores two
of these subjects the opposite way.** Research reads O(1) (0.26 excess) and
Leviathan (0.64) as anti-examples. Leviathan is not an example at all (0 gunners,
above). **O(1)'s low score is a metric artefact, not a bad bot: research's metric
counts BELT kills, and O(1) shoots HARVESTERS.** MEASURED on their in-band
gunners: conveyor kills : harvester kills = **150 : 374**, against Pantheon's
**3,359 : 0**. On a metric that counted harvesters, O(1) would rank at the top —
and its games are the ones that end at median 147 turns. **The two "anti-example"
labels are era-staleness (Leviathan) and a target-class blind spot (O(1)); only
the first is a real negative.**

---

## 2. DEEP READ — five bots, one table

**Population:** 100-120 team-games each (systematically sampled across the
version's date span so no single opponent dominates), all decoded end-to-end.
**MEASURED** unless marked.

| | **Pantheon v91** | **O(1) v24** | **ph v42** | **Clankers v17** | **sporks v24** | **OpenSverige v94 (us)** |
|---|---|---|---|---|---|---|
| team-games / gunners | 120 / 1089 | 100 / 131 | 100 / 524 | 100 / 408 | 100 / 133 | 100 / 232 |
| gunners per game | 9.07 | 1.31 | 5.24 | 4.08 | 1.33 | 2.32 |
| **median build round** | **412** | **59** | 89 | 96 | 122 | 113 |
| p10 / p90 build round | 139 / 827 | 23 / 156 | 16 / 328 | 29 / 354 | 34 / 463 | 36 / 262 |
| median dist to enemy core (tiles) | 7.1 | 5.0 | 8.1 | 6.1 | **2.2** | 4.1 |
| forward share | 0.900 | 0.924 | 0.653 | 0.699 | 0.970 | 0.530 |
| **enemy econ bldgs in r²≤13 at build (mean)** | **7.43** | 7.27 | 4.75 | 7.62 | 7.30 | **2.45** |
| — share with ≥1 | 0.980 | 0.992 | 0.744 | 0.794 | 0.917 | **0.483** |
| cardinal facing share | 0.513 | **0.229** | 0.538 | 0.554 | 0.368 | 0.586 |
| **econ on CHOSEN ray / BEST ray / RANDOM ray** | **1.41 / 1.62 / 0.39** | 1.28 / 1.64 / 0.45 | 0.77 / 1.16 / 0.30 | 1.28 / 1.58 / 0.52 | **0.35 / 1.25 / 0.35** | **0.09 / 0.48 / 0.11** |
| chosen == best ray | 0.848 | 0.702 | 0.733 | 0.782 | 0.391 | 0.724 |
| **first entity on chosen ray** | conveyor 0.84 | **harvester 0.985** | harvester 0.63 | harvester 0.42 / conveyor 0.31 | **core 0.73** | **none 0.41 / core 0.31** |
| shots per gunner | 15.2 | 11.9 | 18.9 | 25.2 | 27.3 | 18.9 |
| **rotations per gunner** | **0.65** | **0.17** | 0.85 | 3.20 | 0.83 | **4.32** |
| — share never rotating | 0.701 | 0.832 | 0.569 | 0.233 | 0.662 | 0.388 |
| — shots per facing segment (median) | 3 | 5 | 5 | 4 | 3 | **0** |
| — segments firing ZERO shots | 0.110 | **0.000** | 0.043 | 0.155 | 0.109 | **0.626** |
| shot share on enemy economy | 0.536 | **0.809** | 0.582 | 0.578 | 0.093 | 0.095 |
| shot share on enemy core | 0.263 | 0.086 | 0.047 | 0.079 | **0.825** | 0.528 |
| **econ kills / 1000 shots** | **139.2** | 114.1 | 123.0 | 133.0 | 26.5 | **24.2** |
| forward gunner median life (rounds) | 103 | **8** | 15 | 82 | 34 | 56 |
| forward gunner death share | 0.358 | 0.931 | 0.790 | 0.417 | 0.383 | 0.470 |
| duds (never fire) | 0.071 | **0.009** | 0.013 | 0.025 | 0.015 | 0.079 |
| ammo converted per game (median) | 880 | 392 | 654 | 666 | 424 | 497 |
| gunner ammo actually spent /game | 551 | 62 | 397 | 412 | 145 | 175 |
| game share / core-kill wins / median turns | .81 / .49 / 511 | **.80 / .80 / 147** | .61 / .55 / 326 | .63 / .63 / 284 | .73 / .70 / 182 | .47 / .33 / 307 |

---

## 3. THE MECHANISMS THAT MAKE IT WORK

### 3.1 SITING: plant inside the belt, not near it — and the RAY is the unit of choice

**MEASURED.** The shredders do not put the gunner "in the base"; they put it on a
tile whose *facing ray already contains a target*. The discriminator is the
three-way ray comparison, which is a control by construction:

* Pantheon: econ on the CHOSEN ray **1.41** vs a random one of the 8 rays
  **0.39** (3.6×) and vs the best available ray 1.62 — **84.8% of gunners are
  built on the best facing available from that tile.**
* O(1) 1.28 vs 0.45; Clankers 1.28 vs 0.52; ph 0.77 vs 0.30. All the same shape.
* **sporks reads 0.35 vs 0.35 — the control runs the OTHER WAY**, which is the
  proof the statistic measures intent rather than terrain: sporks aims at cores
  (ray-first = core 0.73) and their ray is exactly as econ-rich as a random one.
* **We (v94) read 0.09 chosen vs 0.11 random — BELOW random**, with 41% of
  gunners built with NOTHING on the ray at all.

Density matters too: shredders build with a mean of **7.3-7.6 enemy economy
buildings inside r²≤13** (98-99% have ≥1). Our v94: **2.45, and 51.7% had zero.**

### 3.2 FACING: cardinal ≈ diagonal, and the diagonal is not a mistake

**MEASURED.** Cardinal share is 0.51 (Pantheon), 0.55 (Clankers/ph), and only
**0.23 for O(1)** — three quarters of O(1)'s gunners face diagonally. Diagonal
rays reach only 2 tiles (d²=2, 8) against cardinal's 3 (d²=1, 4, 9), so a
diagonal facing is a *deliberate* trade of reach for a specific victim. O(1)'s
shot histogram is 51% at d²=2 and 26% at d²=8: they build the gunner **diagonally
adjacent to a harvester**. INFERRED reason: a harvester sits on ore, the
orthogonal neighbours of an ore tile are usually taken by the victim's own belt
(which would BLOCK a gunner ray — friendly-blocking is the victim's problem, but
enemy buildings block ours), and the diagonal tile is the free one.

**⇒ Never restrict the facing search to cardinals.** All 8 are legal for turret
facing; only builder *movement* is cardinal-only.

### 3.3 ROTATION: it is a KILL-TRIGGERED re-aim, and its absence is the norm

This is the half Magnus's sentence asked about and the half the corpus could not
answer. **MEASURED:**

* **Most gunners never rotate at all.** Pantheon 70.1%, O(1) 83.2%, sporks 66.2%
  never rotate. Rotations per gunner: Pantheon **0.65**, O(1) **0.17**.
  Clankers is the outlier at 3.20.
* **When they do rotate, it follows a KILL.** Share of rotations preceded within
  4 rounds by a kill by that gunner: **O(1) 0.947, ph 0.743, Clankers 0.716,
  Pantheon 0.606** — against **sporks 0.299** (core-sniper: rotation is re-aim,
  not exhaustion) and **us (v94) 0.283, with 40.0% of our rotations having NO
  SHOT AT ALL in the previous 4 rounds.**
* **Shots per facing segment** (build or rotation → next rotation): median
  **3** for Pantheon (= exactly the 3 shots that kill a 20-HP conveyor),
  **5** for O(1) and ph (= exactly the 5 that kill a 30-HP harvester),
  **4** for Clankers. **Our v94's median is 0**, and **62.6% of our facing
  segments fired zero shots** — 4.32 rotations × 10 Ti = **~43 Ti per gunner
  burned on rotate-thrash**, against Pantheon's 6.5 Ti and O(1)'s 1.7 Ti.
  This is the same failure the tape already recorded as GUNPIN 44.27.

**⇒ The rule the field actually runs: rotate only when the thing you were
shooting is dead AND the new direction has a target. Never on a timer, never as a
re-aim search.**

### 3.4 THE LINE DOES NOT GET EATEN — IT GETS FARMED. (A refutation.)

The commission's model was "a gunner fires along a belt line and eats it tile by
tile, since the nearest target refreshes". **The refresh is real; the eating is
not.** MEASURED over consecutive shot pairs inside a single facing segment:

| | shot lands FARTHER than previous | SAME distance | NEARER |
|---|---|---|---|
| Pantheon (n=6,971) | 0.048 | **0.925** | 0.027 |
| O(1) (n=1,675) | 0.028 | **0.960** | 0.012 |
| Clankers (n=3,008) | 0.085 | 0.893 | 0.022 |
| ph (n=4,176) | 0.041 | 0.934 | 0.025 |

92-96% of the time the next shot lands on the **same tile**. The reason is in the
next number: **the victim rebuilds on the same tile in a median of 2 rounds**
(Pantheon's victims: 1,222 of 1,992 econ kills rebuilt on the identical tile
within 30 rounds = 61.3%, median latency **2.0**; ph 42.4%, O(1) 33.9%,
Clankers 16.0%). Research measured the same thing league-wide (55.5% same-tile,
37.3% within 10 rounds) and correctly reads it as *"victims rebuild INTO the
kill zone"*. **Two independent pipelines, 55.5% vs 61.3% on the heaviest
executor — they agree.** ⚠ They also bound each other: research's *"68.5% of
belt cuts are never repaired"* is a league-wide figure over ALL cuts, while the
55-61% same-tile rebuild is specific to cuts made **beside a live gunner** — a
gunner's victim repairs *far more* than the average cut victim, because the
gunner is sitting on the trunk the victim cannot do without. **Do not carry the
68.5% into a gunner plank's payoff model.**

⇒ **A parked forward gunner is a REBUILD FARM, not a saw.** It converts the
victim's builder-turns and 3-Ti-times-scale rebuilds into nothing, forever, at 12
ammo per cycle. The refresh-to-the-next-target does happen — the O(1) anchor
below shows it — but it is the minority event.

**Anchor, EYEBALL** (`21cc982f-a61b-4422-b85c-81859e6729f6_game_4.replay26`,
team 0 = O(1) v24 vs Part-timers, 139 rounds, O(1) wins by core kill): gunner
built **r20 at (11,15), facing NW, d²=13 from the enemy core**, by builder #14
which walked (0 launcher displacement). r21-r25 five consecutive shots into the
harvester at (10,14) (d²=2) — it dies; r26-r31 six consecutive shots into a
builder bot at (9,13) (d²=8) — *the same ray, the next target back*. r34 the
gunner is removed **having taken 0 builder attacks and 0 enemy shots** (see 3.5).
Second anchor, same shape:
`13977126-e69c-4538-bd78-060f1a999251_game_5.replay26` team 1, gunner built r132
at (4,18) facing NE, five shots r133-r137 into the harvester at (6,16), removed
r140 undamaged.

**Also MEASURED and worth carrying: a gunner fires EVERY round.** Reload 1 sets
the cooldown to 1, which decrements at end of round, so the next round it is 0.
The anchors show r21,22,23,24,25 with no gap. **A live forward gunner is a
standing 4-ammo-per-round bill**, not 2.

### 3.5 ⭐ THE GUNNER IS RENTED, NOT OWNED — spent gunners are deleted at full HP

The single most surprising thing in the study, and it fell out of asking why 80%
of O(1)'s gunner deaths had no attacker.

**MEASURED** (HP tracked through `updateHp`, whose delta is a 64-bit two's
complement varint — TRAP 2):

| | own forward gunners removed at **FULL HP** | own builder ortho-adjacent at removal | median life |
|---|---|---|---|
| **O(1) v24** | **0.703** (n=118) | 0.246 | 8 |
| **Clankers v17** | **0.433** (n=97) | 0.588 | 30 |
| ph v42 (home gunners) | 0.654 (n=156) | 0.333 | 10 |
| ph v42 (forward) | 0.195 (n=210) | 0.138 | 14 |
| Pantheon v91 | 0.000 (n=263) | 0.722 | 4 |
| sporks v24 | 0.000 (n=50) | 0.280 | 5 |
| **OpenSverige v94 (us)** | **0.000** (n=58) | 0.259 | 8 |

**Control that must run the other way, inside the same games and the same
tracker:** O(1)'s own FORWARD SENTINELS read **0.000 at full HP (n=30)**, and
Pantheon's LAUNCHERS read **1.000 at full HP with median life 3 (n=50)**. The
instrument is not simply reporting "HP tracking is broken".

Two legal mechanisms produce this, and the adjacency column separates them:
`self_destruct()` (no adjacency needed — O(1)'s 70% full-HP with only 25%
adjacency) and an allied builder's `destroy()` (free, no cooldown — Clankers'
43.3% full-HP with 43.3% adjacency, the two numbers identical).

**Why do it (INFERRED, but the engine rule is explicit in CLAUDE.md — *"destruction
removes the contribution"*):** a gunner is **+20% on the single global additive
cost scale**, the joint-largest contribution in the game. A gunner that has
killed its harvester and has nothing left on its ray is a **permanent +20% tax on
every future build**. Deleting it refunds that tax. Secondary: it frees one of
the 50 `MAX_TEAM_UNITS` slots and denies the enemy a free kill.
**Pantheon does the same thing with launchers** — build, throw, delete, median
life 3 rounds.

⚠ NOT MEASURED: whether the removal is `self_destruct` or an allied `destroy`
per event (the replay emits the same `removeEntity` for both). The distinction
does not change the spec — `destroy` needs a builder standing there, so **prefer
`self_destruct` from the gunner's own `run()`**, which needs nothing.

---

### 3.6 THE PRODUCTIVE ANNULUS, confirmed from a second instrument

The research lane established the placement gradient corpus-wide: excess
belt-kills per gunner peak at **d² 20-30** from the enemy core, stay high through
**d²<100**, hit zero at ~d²170 and go negative past 220; deeper than d²<10 buys
half the lifetime for 60% of the output. **Cited, not re-derived.**

This study's shot-target data confirms the *mechanism* independently, and the
confirmation is close to arithmetic. **MEASURED — profile of every current-version
gunner planted in the band 20 ≤ d²_enemy ≤ 100, whole archive:**

| team | n in-band | median build round | rot/gun | shots/gun | **econ kills/gun** | conveyor : harvester kills | **econ share of shots** | **CORE share of shots** | cardinal | median life | death share |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Clankers v17 | 676 | 184 | 3.32 | 25.1 | **4.36** | 2319 : 626 | 0.707 | **0.000** | 0.53 | 128 | 0.48 |
| ph v42 | 626 | 124 | 0.98 | 20.4 | 2.86 | 1314 : 478 | 0.682 | **0.000** | 0.57 | 83 | 0.79 |
| Pantheon v91 | 1508 | 430 | 0.58 | 12.5 | 2.23 | 3359 : 0 | 0.733 | **0.000** | 0.47 | 215 | 0.40 |
| Pivot v188 | 443 | 176 | 0.58 | 9.5 | 1.40 | 415 : 206 | 0.605 | **0.000** | 0.34 | 15 | 0.98 |
| O(1) v24 | 386 | 78 | 0.03 | 11.1 | 1.36 | **150 : 374** | **0.885** | **0.000** | 0.31 | 14 | 0.97 |
| sporks v24 | 23 | 192 | 1.91 | 21.6 | 3.39 | 69 : 9 | 0.730 | **0.000** | 0.57 | 163 | 0.43 |

**The core share is 0.000 in every cell, across 3,662 in-band gunners.** That is
the annulus mechanism stated as an identity rather than a correlation: a gunner
reaches 3 tiles (r²=13); at d²≥20 (≥4.5 tiles) from the core it **cannot** shoot
the core, so every shot it fires is at something else — which is precisely
Magnus's *"everything other than the core"*, recovered from the geometry.
Note also that **sporks, whose gunners are core-snipers, has only 23 in-band
gunners in the whole archive**: they deliberately place INSIDE the annulus
(median 2.2 tiles), which is why their econ numbers are low.

**Our own deficit is VOLUME, not conversion** (research: our current-version
in-band gunners earn 1.50-1.97 excess ≈ the field median 1.82, but we plant
in-band at 0.118-0.143 share vs the field's 0.276). Everything in §7 is therefore
a *how to plant more of them without re-importing bad aim* spec, not an aiming fix.

⚠ Carry research's caveats verbatim: **no facing term (so the gradient is an
upper bound), overlapping-gunner double-count inflates dense teams, and
cross-team excess confounds with opponent belt mass — the within-team version
split is the actionable instrument, and none of it is causal.**

### 3.7 TIMING — descriptive only; the causal question is OPEN and both instruments refuse it

**MEASURED, DESCRIPTIVE, NON-CAUSAL.** Round of the **first productive in-band
plant** (a gunner built at 20 ≤ d²_enemy ≤ 100 that goes on to score ≥1 economy
kill), per current-version team, whole archive:

| team | team-games | share of games with one | p10 | **median** | p90 |
|---|---|---|---|---|---|
| ph v42 | 260 | 0.704 | 9 | **34** | 96 |
| O(1) v24 | 459 | 0.460 | 14 | **52** | 122 |
| Clankers v17 | 375 | 0.643 | 29 | **52** | 195 |
| Pivot v188 | 135 | 0.704 | 18 | **55** | 148 |
| sporks v24 | 263 | **0.061** | 57 | 100 | 435 |
| Pantheon v91 | 340 | 0.588 | 98 | **177** | 458 |
| **OpenSverige v94 (us)** | 200 | **0.070** | 34 | 75 | 180 |

⭐ **TWO INDEPENDENT DEFICITS, and they move separately.** Research's descriptive
field table puts the field's median first in-band plant at **r37**, the best
executors at **r13-33** (not adgato 13, ph 21, Leviathan 28, Jython 33), and
sporks as the late-and-selective outlier at r90. **Ours is r56-85 in every
version cell** — the lateness is version-STABLE while the volume deficit moves
with version. So we are behind on **two** axes: we plant in-band **half as
often** AND **~45 rounds later**, and a plank that fixes one leaves the other.
(The v94 row above, r75 median, is the same lateness in the era that actually
had forward gunners.)

**The outcome question does not resolve, and this study reproduces research's
refusal from a different pipeline.** Pooled over the five current-version
shredders, restricted to games of 150-400 rounds to blunt the length confound
(n=774 team-games):

```
win share by CUT COUNT      : 0 cuts 0.44 (n=155) | 1-2 0.51 (144) | 3-7 0.70 (187) | 8-19 0.90 (197) | 20+ 0.88 (91)
win share by FIRST-CUT ROUND: <40  0.72 (n=162) | 40-80 0.75 (170) | 80-150 0.81 (79) | 150+ 0.85 (47)
   within the 3-7 cut stratum : <40 0.66 | 40-80 0.67 | 80-150 0.68 | 150+ 0.86
   within the 8-19 cut stratum: <40 0.86 | 40-80 0.90 | 80-150 0.97 | 150+ 0.89
```

**Cut COUNT is strongly and monotonically associated with winning; cut ROUND runs
the WRONG WAY (later is better) and stays flat-to-reverse inside cut-count
strata.** Both are hopelessly confounded — a team that is losing does not get to
plant deep at r250, and a game you are winning lasts long enough to accumulate
cuts — so **neither number identifies anything**, and the "early cuts are worth
vastly more under permanent-cut economics" prediction is **NOT CONFIRMED HERE**
(nor refuted). Research's two designs disagreed in sign on the same quantity;
this one disagrees with the prediction's sign too. ⇒ **Timing is a treatment to
register in a leg, not a parameter to read off the archive.**
⚠ **No natural experiment found** in this sample: plant round is not forced by
spawn geometry in any subset I could isolate, so the confound has no exit here.

## 4. ESCORT, DELIVERY, SURVIVAL, AMMO

**ESCORT — two schools, MEASURED.**
Pantheon and Clankers *heal* their forward gunners: **30.1% / 26.4% of forward
gunners receive ≥1 builder heal**, and the healed ones receive ~17 heals
(+68 HP ≈ 2.7 extra gunner-lifetimes at 25 max HP). O(1), ph and sporks do
essentially none (2-3%). **We (v94) healed 0.0% of forward gunners while having a
friendly builder within d²≤2 for 73.0% of gunner-life** — the escort was
physically there and never spent 1 Ti on the +4 HP.
Barriers-as-armour is NOT what they do (already falsified for kladde in
`REPLAY-STUDY-TOPTEAM-MICRO`); the escort is a healer, not a wall.

**DELIVERY.** O(1), Clankers and sporks: **0 of 73 / 214 / 81** gunner-building
builders had ever been displaced by a launcher throw before the build — **they
walk.** Pantheon 39.8% and ph 66.2% of their gunner-builders HAD been displaced
by a >1-tile move at some point. ⚠ **NOT ATTRIBUTED:** a d²>2 move is a launcher
throw by *either* team (the corpus's own thrower rule needs a launcher within
d²≤2 of the pre-throw tile, which this pass did not compute), so this is
consistent with either "Pantheon ferries its own builders" or "Pantheon's
builders get kidnapped a lot". Do not quote it as a ferry statistic.

**WHAT KILLS THEM.** Excluding the self-deletions of 3.5, forward gunner deaths
are **overwhelmingly enemy TURRET fire, not builder pecks**: Pantheon 384 turret
vs 6 builder (98.5% turret), Clankers 97 vs 25, ph 205 vs 38. For O(1) the
residual after removing full-HP deletions is small and mixed.
⇒ **The counterplay we will face is a turret with line on the plant tile, not a
builder walking over to chew it.**

**AMMO.** All five convert continuously in small chunks rather than banking:
Pantheon **146 convert events per game** for 880 ammo (≈6 Ti per call, nearly
every round) against 551 ammo actually spent by gunners; O(1) 41 calls for 392
against 62 spent. Nobody in this sample runs a bank-then-spend policy. This
matches `REPLAY-STUDY-TOPTEAM-MICRO` Piece 5 (`convert_ammo` costs no cooldown
and works the same turn, so pre-banking has no upside) and it matters here
because a forward gunner is a **standing 4 Ti/round bill for as long as it has a
target**.

---

## 5. OUR OWN v94 — the before/after control nobody had read

**Population:** 100 OpenSverige v94 team-games, all from 2026-08-09, 232 gunners.
Research's fourth steering update establishes that the v102 break was a
**substitution** (forward-gunner closer-share 0.549→0.090, barriers/game
0.09→8.52, sentinel deep-share 0.600→0.881). The question is therefore whether
the substitution was right *for the belt-cutting role*. **It was — because v94's
forward gunners were never doing that role.** MEASURED:

* v94's gunners put **52.8% of shots into the enemy CORE and 9.5% into economy.**
  Ray-first at build: **none 0.41, core 0.31, conveyor 0.12.**
* Econ on the chosen ray **0.09, BELOW the random-ray baseline 0.11.**
* **51.7% were built with zero enemy economy buildings within r²≤13.**
* 4.32 rotations/gunner, 62.6% of facing segments firing zero shots, 7.9% duds.
* Placebo-controlled throughput: victim deliveries **+0.087 stacks/round AFTER**
  our first forward gunner (n=12) — the wrong sign. No denial at all.
* 24.2 econ kills per 1000 shots, against Pantheon's 139.2.

**⇒ The correct reading of v102: we removed a badly-aimed CORE gunner, not an
economy shredder. Nothing in the v94 tape argues against building the shredder;
the tape argues that we have never built one.** (And the sentinel we substituted
is the wrong turret for the belt — see §6.)

### 5.1 ⭐ THE TREE ANSWERS BOTH VERSION QUESTIONS — and one answer voids a framing

Code archaeology (opus subagent, commissioned by this study; version→directory
map established from the "= vNNN" ship lines in `docs/coordination.md` and
`HANDOVER-archive.md`, since the `bots/_vNNN` prefix is a LOCAL build counter
unrelated to the platform version):
**v94 ≡ v101 = `bots/_v115dodge`** (md5 77ae5c09; v95-v100 were re-submits of the
same tree) · **v102 = `bots/_v124loki8`** · **v116 = `bots/_v169launchlate160`** ·
**v125 = `bots/_v197mapcode`** · **v140 = `bots/_v223sealrepair`** ·
**v152 = `bots/_x3r0v152`** · **v155 = `bots/_v468kladturbo`**.

**(1) THE REPLAY MEASUREMENT AND THE SOURCE AGREE ON v94, INDEPENDENTLY.**
`_v115dodge/main.py:2616 _plan_siege` enumerated every tile whose weapon ray
reaches `core_tiles(self.enemy)` and rejected a ray only if it crossed a **static
map wall** (`main.py:2695-2699`). **There was no live-target predicate at all** —
the plant was speculative, aimed at where the enemy core *is*, not at anything
standing there. That is precisely the fingerprint §5 measured off the replays
without seeing the code: **econ on the chosen ray 0.09 against a random-ray 0.11,
51.7% built with nothing in range, 7.9% never firing.** Two instruments, one
verdict. (`PRIMARY_SENTINEL = True`, `main.py:984`, made only the *first* forward
turret a sentinel and **every one after it a gunner** — which is why v94 has
forward gunners at all.)

**(2) THE v94→v102 SUBSTITUTION WAS DELIBERATE, NAMED, AND REASONED IN-TREE —
and its reason is about the CORE, not the belt.** `_v105loki1/raid.py:32-37`:
*"The damage itself then comes from a forward SENTINEL. This is not a turret
preference, it is forced: barriers block line of sight, so a Gunner ray dies on
our own collar, while the Sentinel line ignores obstacles and shoots THROUGH
it."* Promoted to constants at `_v223sealrepair/doctrine.py:1231-1237`
(`LOKI_FWD_SENTINEL_ON`, `LOKI_FWD_GUN_CAP`). `_plan_siege` was **deleted**, not
tuned, in the same change that introduced the barrier collar. **The argument is
valid and it is about shooting the CORE through our own collar. It says nothing
about a gunner at d²20-100 whose target is the belt** — see §7.5, which is now a
hard constraint rather than a note.

**(3) THE v116→v140 "QUALITY-OVER-QUANTITY TRADE" IS NOT A GUNNER CHANGE. NO
GUNNER CODE CHANGED AT ALL.** `main.py` v116→v140 differs by **14 diff lines,
all of them per-raider salt/idle state in `__init__`**; `_try_counterbattery`,
`_defend` and the gunner branch of `_turret` are unchanged, and
`HUNT_BAND_DSQ = 41`, `ECO_NEED = 3`, `SIEGE_HEAL_RESERVE_TI = 16` are
**byte-identical in every `doctrine.py` from v102 to v155**.
⛔ **AND THE FRAMING THIS VOIDS IS MINE.** `grep 'ct.build_gunner\|ct.build('`
returns **exactly one gunner call site per tree from v102 to v155**:
`_try_counterbattery` — **defender role only, threat inside `HUNT_BAND_DSQ = 41`
of OUR OWN core, sentinel tried first and gunner as the fallback.** So **every
gunner we have built since v102 is HOME counter-battery.** Whether one of them
lands in "d²20-100 of the ENEMY core" is a **map-geometry accident** (true on
small maps, false on large), not a decision.
⇒ **"We already aim as well as the field once we plant" is NOT a finding about
our aim.** It is a conversion rate measured on accidental placements, and the
version axis cannot explain the share collapse because the code is constant
across it. **Any reading of that trade needs a map-size and era control first.**
The real source of our gunners' conversion is one line —
`_v468kladturbo/main.py:695`
`if not ct.can_fire_from(bp, facing, turret_type, threat): continue` —
**a target-in-ray precondition that has been there since v102.**

**(4) WHY WE PLANT LATE IN EVERY ERA: THE SITING PREDICATE, NOT A THRESHOLD.**
`raid.py:653 _try_forward_sentinel` aims **only** at enemy core tiles —
`tiles = core_tiles(E)` (`raid.py:688`), `if bp.distance_squared(target) > 32:
continue` (`raid.py:694`), with a pre-scan bail `if dsq_core(p, E) > 50: return
False` (`raid.py:684`). **No code path in the tree plants a forward turret at a
d²20-100 belt-cutting site.** The raider must walk to d²≤32 of the core footprint
before *any* forward plant is legal — which is ~20-30 rounds of walking past the
band the field plants in, and it is a **predicate, not a knob.** The knobs sit on
top of it, in the order the repo itself enumerates at `doctrine.py:1355-1382`:
`LOKI_FWD_MIN_HARV = 2` (`doctrine.py:1265`, applied `raid.py:674,676` — doctrine
calls it *"the single biggest source of delay: it structurally forbids the
r14-r22 plant every specialist makes"*), `LOKI_FWD_TI_FLOOR = 40`
(`doctrine.py:1264`), the seat roster (`main.py:444-457`, `LOKI_ECO_SEATS =
(1,2,3)`), and `_raid_act`'s ordering, which ranks core-peck (`raid.py:266`) and
**barrier-seal (`raid.py:280`) ABOVE the forward sentinel (`raid.py:295-297`)`.
The release valve exists and is **OFF**: `LOKI2_RUSH_ON = False`
(`doctrine.py:1409`) lifts all three gates inside r<60 — switched off on LOKI-4
evidence whose failure the tree attributes to the monotone rubble cap that
`LOKI2B_LIVE_CAP_ON` (`raid.py:669-671`) has since fixed, **so the rush arm is
arguably re-testable.**
**QUEUE #23 already owns this lever** (`QUEUE.md:92`, s34: our forward arm opens
at r33 vs the field's r25, in 78% of games vs 87%, at 2.28/game vs 4.54) with two
standing warnings — **the cap raise is DEAD (binds in ≤12.92% of games) and the
pooled turret figure INVERTS the sign; do not re-derive either.**

---

## 6. COST ARITHMETIC — where the gunner is the RIGHT turret, and where it is not

Straight from the constants in CLAUDE.md (gunner 7 dmg / 4 ammo, sentinel 18 dmg
/ 10 ammo). **Shots are `ceil(HP/dmg)`; ammo is Ti 1:1 via `convert_ammo`.**

| target | HP | gunner shots | **gunner ammo** | sentinel shots | **sentinel ammo** | winner |
|---|---|---|---|---|---|---|
| **conveyor / splitter** | 20 | 3 | **12** | 2 | 20 | **gunner, 0.60×** |
| harvester / barrier | 30 | 5 | 20 | 2 | 20 | tie |
| gunner | 25 | 4 | 16 | 2 | 20 | gunner |
| builder bot | 40 | 6 | 24 | 3 | 30 | gunner |
| sentinel | 40 | 6 | 24 | 3 | 30 | gunner |
| **core** | 500 | 72 | 288 | 28 | **280** | sentinel (marginal) |

Plus: gunner costs **20 Ti** to build vs sentinel **30 Ti**, both +20% scale.
Against that the sentinel buys **r²=32 reach (5.6 tiles vs 3.6)**, **40 HP vs
25**, and **shots that ignore obstacles** — decisive for reaching a core past a
collar, worthless against a belt tile you can stand next to.

**And the field builds to exactly this table.** MEASURED — first entity on the
chosen ray at build, forward turrets only, split by turret type:

| team | forward **GUNNER** ray-first | forward **SENTINEL** ray-first |
|---|---|---|
| Pantheon v91 | **conveyor 0.86**, core 0.09 (n=663) | conveyor 0.55, harvester 0.17, core 0.15 (n=232) |
| ph v42 | **harvester 0.86** (n=234) | **core 0.49**, conveyor 0.32 (n=106) |
| Clankers v17 | **harvester 0.49 / conveyor 0.48** (n=221) | **core 0.47**, conveyor 0.39 (n=109) |
| O(1) v24 | **harvester 0.99** (n=96) | **core 0.70**, conveyor 0.30 (n=101) |
| sporks v24 | core 0.76 (n=79) | core 0.61 (n=145) |
| **OpenSverige v94 (us)** | **core 0.58**, gunner 0.16 (n=76) | core 0.49 (n=47) |

Sentinels are additionally planted where more enemy **core tiles** are in range
(2.6-3.6 mean vs the gunners' 0.9-1.1). **The choice tracks target class in every
executor that fields both. We are the exception, in both columns.**

### Is the exchange positive?

**On the buildings-destroyed ledger, NO, and by a lot.** Pantheon: ~121 Ti per
gunner (20 Ti × ~3× scale + 15.2 shots × 4 ammo) for **2.11 econ kills** =
**~57 Ti per kill of a 3-Ti conveyor.** Research's raw form (12 ammo to erase 3
Ti, 55.5% rebuilt on the same tile) is the same verdict at the per-kill grain.
**Any bar denominated in buildings destroyed measures a 4:1-to-17:1 losing trade.**

**On the throughput ledger, YES for the executor that clears its own placebo.**
Placebo-controlled event study, victim stacks delivered per round, 50-round
windows either side of the team's FIRST forward gunner (one 10-Ti stack per
count):

| team | **REAL** delta | **PLACEBO** delta (event − 100 rounds) | verdict |
|---|---|---|---|
| **Pantheon v91** | **−0.190 ± 0.097** (n=58) | **+0.031 ± 0.084** (n=29) | **holds** |
| ph v42 | −0.138 ± 0.115 (n=11) | +0.010 ± 0.057 (n=6) | same sign, underpowered |
| O(1) v24 | −0.176 ± 0.242 (n=9) | +0.000 (n=3) | uninterpretable, n too small |
| **Clankers v17** | −0.117 ± 0.133 (n=15) | **−0.166 ± 0.110** (n=7) | **FAILS its own control** |

Pantheon's −0.190 stacks/round is **−1.9 Ti/round of victim income sustained over
at least the following 50 rounds ⇒ ≥95 Ti denied**, against 12 ammo per belt
cycle. Clankers' claim does not survive the placebo and is **not banked**.

The bigger association — victim delivery **0.285 stacks/round in 50-round blocks
with ≥1 live forward gunner vs 0.815 with none** (n=406 vs 508 blocks, Pantheon)
— is **CONFOUNDED** (blocks with live forward gunners are later and Pantheon is
usually winning by then) and is quoted as an upper bound, not an estimate.

### Repair rate is the target-selection variable

Research's per-victim table (cuts stay cut against The Bisons 0.008,
farming_200s 0.015, rntx 0.011; get re-paid-for against sporks 0.702, Leviathan
0.674, Clankers 0.616) **reproduces inside the executors' own games** —
MEASURED, same-tile rebuild within 10 rounds, by victim:

* Pantheon's victims: Banminary 0.845, Leviathan 0.795, gsxWins 0.432,
  Erebus 0.410, kladde 0.353, Clankers 0.228, Dino 0.090, not adgato 0.096,
  **OpenSverige 0.022** (n=46).
* ph's victims: sporks 0.677, Leviathan 0.694, Pivot 0.556, OpenSverige 0.494,
  Torsko 0.390, Erebus 0.272, **0033 0.009**, Dino 0.038.

Note our own two readings differ (0.022 vs Pantheon, 0.494 vs ph) — small n and
different eras; **do not quote a single repair rate for ourselves.**
**None of the executors visibly conditions on it** — the same siting rule is run
against every opponent. That is an opening, not a habit to copy.

---

## 7. ⭐ OPERATIONAL SPEC — "BELTBREAKER"

A concrete policy a builder can implement, written against the real API. Every
clause names the measurement behind it. Bracketed names are tunables.

### 7.0 Doctrine framing (read this first)

The engine table in §6 says the gunner is the **correct turret for the 20-HP
target class**, and the field builds to that table. We currently field **sentinels
and barriers forward and no gunners at all** — i.e. **we field the wrong turret
for the belt.** That is the falsifiable claim this spec rests on, and it holds
even if the throughput numbers are re-measured weaker.

**But the two shredder doctrines are not interchangeable, and only one of them is
ours.**

| | **CONVEYOR FARM** (Pantheon) | **HARVESTER SNIPE** (O(1), ph) |
|---|---|---|
| median build round | 412 | 59 / 89 |
| median game length | 511 turns | **147 / 326** |
| core-kill win share | 0.49 | **0.80 / 0.55** |
| gunners per game | 9.07 | 1.31 / 5.24 |
| target | belt, rebuilt in 2 rounds, farmed forever | the SOURCE, 20 Ti and must go back on ORE |
| fits `R1000_IS_DEFEAT` | **no** | **yes** |

**⇒ Build the HARVESTER SNIPE. Pantheon's conveyor farm is a long-game engine
and adopting it would push kills past r300**, which `DEFENCE_ADMISSION_BAR`
forbids. Conveyor targets are the *fallback* when no harvester is on a ray, not
the plan.

### 7.1 WHEN TO SEND — and the honest status of the timing number

* **Gate:** a raider builder is already forward (we arrive at median t=31 rounds,
  `FORWARD-ARRIVAL-BASELINE`), `get_global_resources() >= get_gunner_cost() +
  [AMMO_RESERVE=20]`, and the builder can SEE at least one enemy `HARVESTER` or
  `CONVEYOR` (builder vision r²=20).
* **Window:** first plant in **r30-r150** as an opening value —
  the field's first productive in-band plant is at median r34 (ph), r52 (O(1),
  Clankers), r55 (Pivot), r177 (Pantheon). **Do not open a new plant after
  [LAST_PLANT=250]** — past that the plank is buying a long game we do not want.
  ⛔ **TIMING IS THE REGISTERED TREATMENT OF THE FIRST LEG, NOT A SETTLED
  PARAMETER.** §3.7 shows the archive cannot price it: cut-round runs the wrong
  way, cut-count is confounded with game length, and research's two independent
  designs disagree in sign. Pick a value, register it, and let the leg move it.
  **THE TWO ARMS WRITE THEMSELVES, because the late arm is literally the
  incumbent:** *EARLY* = first in-band plant at **r ≤ 25** (the executor band:
  not adgato r13, ph r21, Jython r33) vs *LATE* = our standing **r56-85 median,
  version-stable across every cell we have**. The leg reads as **"move our first
  plant ~45 rounds earlier"** and needs no synthetic control arm.
  **AND THE KNOBS ARE NAMED (§5.1(4)), in the order they bind:** the
  `core_tiles(E)` siting predicate (`raid.py:688`, not a knob — widening it is
  the plank) → `LOKI_FWD_MIN_HARV = 2` (`doctrine.py:1265`, the tree's own
  *"single biggest source of delay"*) → `LOKI_FWD_TI_FLOOR = 40`
  (`doctrine.py:1264`) → `_raid_act` ordering, which ranks the barrier-seal above
  the forward turret (`raid.py:280` vs `295-297`) → the seat roster
  (`main.py:444-457`). **The first four move without diverting a builder the
  economy depends on; only `LOKI2_RUSH_SEATS` (`doctrine.py:1413`) does, by
  sending eco seat 1 forward.** `LOKI2_RUSH_ON = False` (`doctrine.py:1409`) is
  the existing off-switch for gates 2-4 inside r<60, disabled on LOKI-4 evidence
  whose named failure cause (the monotone rubble cap) has since been fixed by
  `LOKI2B_LIVE_CAP_ON` — **so re-testing the rush arm is cheap and pre-built.**
  ⚠ **QUEUE #23 already owns this lever** and carries two do-not-re-derive
  warnings: **the cap raise is DEAD (binds in ≤12.92% of games) and the pooled
  turret figure INVERTS the sign** (`QUEUE.md:92`, `:107-108`).
* **Count:** **[MAX_LIVE_FWD_GUN = 2]** live at once, rising later if the
  recycle rule in 7.6 is working. O(1) runs 1.31 gunners/game and wins 80% of its
  games by core kill; Pantheon's 9.07 is the long-game shape.
  Each live gunner is +20% scale on everything else we build, which is why 3.5
  exists.
* ⛔ **"THE PLANK IS VOLUME, NOT AIM" — WITHDRAWN BY THE TREE, §5.1(3).**
  Research's 1.50-1.97 excess belt-kills per in-band gunner (vs a field median
  1.82) is real but is **not a measurement of our aim**: since v102 the tree has
  exactly one gunner call site, `_try_counterbattery`, which is **home defence
  keyed to `HUNT_BAND_DSQ = 41` of OUR OWN core.** Those in-band gunners are
  **map-geometry accidents**, and the good conversion comes from that site's
  `can_fire_from(..., threat)` precondition, not from siting judgement we could
  reuse. **We have no forward-gunner aim to be good at.** The spec's job is
  therefore to build the siting rule AND the volume, and 7.6's recycle rule is
  what makes planting affordable in scale terms.

### 7.2 PLACEMENT — the selection rule, in API terms

**Band first: target d²_enemy in [20, 100], preferring [20, 60].** Research's
gradient peaks at d² 20-30, holds to d²<100, is zero by d²170 and negative past
220; d²<10 halves the gunner's life for 60% of the output. The mechanism is
arithmetic and this study confirms it from the other side: across **3,662
in-band gunners the core share of shots is 0.000** — beyond ~4.5 tiles a gunner
physically cannot reach the core, so the band *is* "everything other than the
core" (§3.6). **d² < 20 is the sporks core-sniper band and a different plank.**

Then, within the band:

For each tile `T` orthogonally adjacent to the builder (never diagonal, never the
builder's own tile) and each of the **8** directions `d`:

```
if not ct.is_in_vision(T):        continue      # is_in_vision does NOT raise off-map
if not ct.can_build_gunner(T, d): continue      # legality, incl. emptiness
score(T, d) = value of the FIRST enemy entity a gunner at T facing d would hit
```

Resolve "first entity hit" with **`ct.can_fire_from(T, d, EntityType.GUNNER,
target)`** over the enemy buildings the builder can see, taking the nearest
target for which it returns True. That predicate is the engine's own LOS+range
check. **Do not hand-roll the ray**; a hand-rolled ray misses the
friendly-blocking rule (`turret-line-blocking-2026-08-09`: a gunner's line is
blocked by *any* friendly entity, and `get_attackable_tiles()` lies about it).

⭐ **THE MACHINERY ALREADY EXISTS IN THE LIVE TREE — this is a target-set and a
turret-type change, not a new subsystem.**
`bots/_v468kladturbo/raid.py:701` is
`if not ct.can_fire_from(bp, facing, EntityType.SENTINEL, target): continue`
inside `_try_forward_sentinel` — the identical tile×facing scan, run with
`SENTINEL` and a target set of enemy **core** tiles (`raid.py:688
tiles = core_tiles(E)`). BELTBREAKER is the same loop with `EntityType.GUNNER`
and a target set of enemy **harvesters and conveyors**, plus the band filter.
(`main.py:943` / `main.py:695` already wrap `can_fire_from(..., GUNNER, threat)`
for the home counter-battery, so the gunner form of the call is live and
exercised.)

⛔ **AND THE TARGET SET IS THE WHOLE CHANGE — §5.1(4).** `core_tiles(E)` plus
`d² ≤ 32` plus the pre-scan bail `dsq_core(p, E) > 50` means **no code path in
the tree can plant a forward turret in the d²20-100 band at all**; the raider
must first walk to d²≤32 of the core footprint. **That predicate, not
`LOKI_FWD_MIN_HARV` or `LOKI_FWD_TI_FLOOR`, is why our first plant is ~45 rounds
late in every era** — the thresholds sit on top of it. Widening the target set to
enemy economy buildings *is* the timing fix and the siting fix in one edit.

⭐⭐ **THE GUARD TO CARRY, AND IT IS ONE LINE.** §5.1(1) established from source
that v94's `_plan_siege` scored tiles by **geometry against a static wall map**
with no live-target check, and §5 measured what that produced (below-random ray
score, 51.7% nothing in range). **Any tile-scoring rule of the form "the ray
points at where the belt is" re-imports that failure mode verbatim.** The
predicate that must gate every plant is the one already live at
`_v468kladturbo/main.py:695` — `can_fire_from(bp, facing, turret_type, <a target
that exists right now>)`. **Reject any (T,d) scoring 0** is the same rule stated
in this spec's vocabulary; keep them the same rule.

**Scoring ladder (MEASURED order, §6 table):**
`HARVESTER 100 > CONVEYOR/SPLITTER 40 > enemy BUILDER_BOT 25 > enemy GUNNER 20 >
enemy SENTINEL/LAUNCHER 15 > BARRIER 5 > CORE 0`.
**Core scores ZERO for a gunner** — 72 shots / 288 ammo, and a sentinel does it
for 280 with 5.6 tiles of reach. That is the single biggest correction to our v94
behaviour (52.8% of our gunner shots went at cores).

**Tie-break by belt density:** prefer the `T` with the most enemy economy
buildings inside r²≤13 (shredders average **7.3-7.6**; we averaged **2.45**).
This is what buys the rotation options in 7.4.

**Reject** any (T, d) whose best score is 0 — **51.7% of our v94 gunners were
built with nothing in range and 7.9% never fired.** Field duds: 0.9-2.5%.

**Do not restrict to cardinal facings.** 47-77% of shredder gunners face
diagonally (§3.2). A diagonal ray reaches d²∈{2,8}, a cardinal one d²∈{1,4,9}.

### 7.3 FUNDING (core)

Convert **every round**, small: `convert_ammo(min(ti_spare, 4 * live_gunners +
4 * live_sentinels_expecting_to_fire))`. `convert_ammo` costs no action cooldown
and is usable the same turn, so banking is strictly dominated
(Pantheon: 146 calls/game; nobody in the sample banks).
⛔ **Break the closed loop `REPLAY-STUDY-OUROBOROS` identified:** our ammo target
is keyed to our own live turret count (`main.py:234-236`), so a suppressed turret
count starves the ammo that would replace it. **A forward gunner about to be
built must raise the target BEFORE it exists**, or the first plant is silent.
Budget: **4 Ti per live forward gunner per round** while it has a target.

### 7.4 ROTATION — the rule, and the guard

```
rotate only if   (the entity my ray was pointed at is GONE)
           and   (some other direction d' scores > 0 by 7.2's ladder)
           and   (I have not already rotated to that target CLASS this life)
           and   (get_global_resources() >= 10 + gunner-ammo reserve)
```

* **Kill-triggered, never timed.** Field: 60-95% of rotations follow a kill
  within 4 rounds; ours (v94) 28%, with 40% of rotations having fired nothing
  at all in the previous 4 rounds.
* **Expect 3 shots per segment against a conveyor and 5 against a harvester**
  (the observed medians ARE `ceil(HP/7)`). If a segment has fired
  **[THRASH_LIMIT=6]** shots without a kill, the target is being healed —
  see 7.6, abandon rather than rotate.
* **Hard cap [MAX_ROT_PER_LIFE = 2]** (field median is 0; Pantheon 0.65 mean).
  10 Ti a rotation is half a gunner. This is the rotate-once-per-target-class
  guard the tape asked for after GUNPIN 44.27.

### 7.5 ESCORT — and the ONE HARD INCOMPATIBILITY in the live tree

Optional and cheap: if a friendly builder is already orthogonally adjacent and
idle, **heal the gunner (+4 HP for 1 Ti)** rather than parking. 30.1% of
Pantheon's and 26.4% of Clankers' forward gunners get healed; **0.0% of ours did,
while an idle builder sat within d²≤2 for 73% of gunner-life.**
Do not hold a builder in place for escort duty: the deaths are turret fire
(98.5% for Pantheon), which a builder cannot answer.

⛔⛔ **BARRIERS AND FORWARD GUNNERS ARE MUTUALLY EXCLUSIVE BY CONSTRUCTION, AND
THIS IS THE REASON v102 DELETED THE FORWARD GUNNER.** `LOKI_BARRIER_SEAL_ON`
(`raid.py:280`) puts **our own barriers** on the enemy ring, and
`doctrine.py:1231-1237` states the consequence plainly: *"barriers block line of
sight, so a Gunner ray dies on our own collar, while the Sentinel line ignores
obstacles and shoots THROUGH it."* A gunner's line is blocked by **any friendly
entity** (`turret-line-blocking-2026-08-09`). **A BELTBREAKER planted behind our
own collar fires at a barrier we paid for.** The plank is compatible only if the
gunner sits at d²20-100 — *outside* the ring the seal builds — or the seal is
suppressed on that lane. **This is a design constraint to satisfy, not an
objection to answer:** the v102 argument is about shooting the CORE **through**
the collar, which BELTBREAKER never does. Note also that `raid.py:295-297`
currently ranks the barrier-seal **above** the forward turret in `_raid_act`, so
the collar wins the builder's action in the contested rounds.
For the same reason, do **not** build a barrier ring around the gunner
(independently falsified in `REPLAY-STUDY-TOPTEAM-MICRO` and `REPLAY-STUDY-0033`).

⚠ **LATENT TRAP, check before firing:** `LOKI_FWD_GUN_CAP = 3`
(`doctrine.py:1237`) counts **rubble** — `SLOT_FWD_GUN` is only ever written as
`read + 1` and never decremented — so **three destroyed forward turrets close the
arm permanently** unless `LOKI2B_LIVE_CAP_ON`'s live census
(`raid.py:669-671`) is what is actually counting. This is the same monotone cap
the tree blames for the LOKI-2 rush smoke failure (1 turret at r8 vs the
control's 3). Verify which counter is live before reading any volume arm.

### 7.6 ABANDON / REPLANT / RECYCLE

* **RECYCLE (the rental rule, §3.5).** When no direction scores > 0 — everything
  in range is dead and not coming back, or the ray is permanently blocked —
  **`self_destruct()`**. It refunds the gunner's **+20% cost-scale contribution**
  on every future build and frees a unit slot. O(1) does this to **70.3%** of its
  forward gunners at full HP; Clankers to 43.3% (via an adjacent builder's
  `destroy()`); we have never done it once.
  ⚠ Guard: only when nothing is in range, and never while `get_hp()` is falling
  (a gunner under fire is absorbing shots that would otherwise hit the builder).
* **ABANDON without replanting** on the same tile if that tile has already lost a
  gunner. `REPLAY-STUDY-TOPTEAM-MICRO` Piece 3 measured us rebuilding into proven
  kill-tiles 2.5-4× more often than the field; the shredders replant on a used
  tile only 1.5-3.5% of the time (Pantheon 17.3% is the outlier and is the
  long-game farm).
* **REPLANT** at a new (T, d) if the gate in 7.1 still holds and the round is
  < [LAST_PLANT].
* **Target-selection preference (from research's repair table):** against
  low-repair opponents (The Bisons, farming_200s, rntx, Git Glam, SmartFridge,
  Lunds) a **cut-and-move-on** policy is right — the cut stays cut, so recycle
  early and replant elsewhere. Against high-repair opponents (sporks, Leviathan,
  Clankers, Banminary) **park-and-refire** is right — the same tile keeps paying
  out at 12 ammo a cycle and the recycle should be delayed. **None of the
  executors conditions on this today** (MEASURED: same siting rule against every
  opponent), so it is available and unclaimed.

### 7.7 SUCCESS METRIC — what a leg on this must measure

**Denominate in victim throughput, never in buildings destroyed.** The
buildings ledger is 4:1 to 17:1 against by construction. Primary read:
`distributeResources` moves landing on the VICTIM's core footprint, 50-round
windows before/after our first forward gunner, **with the (event − 100) placebo
in the same table** — the placebo is what killed Clankers' claim in §6, and it
must be run for ours too. Secondary: our own **timely-kill rate (core kill by
r300)** must not fall, per `DEFENCE_ADMISSION_BAR`.

---

## 8. THINGS NOT TO CARGO-CULT (checked against the API)

* **"A gunner rotates and kills conveyors left and right and up."** It can, but
  each rotation is **10 Ti + a lost turn**, the field median is **zero
  rotations per gunner**, and our own last attempt at rotation logic burned
  ~43 Ti/gunner on empty facings. The value is in the SITING, not the rotating.
* **"Fires along the belt and eats it tile by tile."** REFUTED, §3.4: 92-96% of
  consecutive shots hit the same tile, because the victim rebuilds there in a
  median of 2 rounds.
* **Do not shoot the core with a gunner.** 288 ammo vs a sentinel's 280 at
  1.6× the reach through obstacles.
* **Do not read the ray from `get_attackable_tiles()`.** It ignores
  friendly blocking (`turret-line-blocking-2026-08-09`). Use `can_fire_from`.
* **`get_tile_env` / `get_tile_building_id` RAISE off-map**; `is_in_vision(pos)`
  returns False and does not raise. Gate every tile scan on it — this is exactly
  the border-crash class we exploit in others.
* **Destroying enemy buildings LOWERS their cost scale.** The gunner's payoff is
  interruption and tempo; it is never scale damage.
* **Rotation is gunner-only.** A forward sentinel is committed to its facing for
  life; that is a reason to choose the gunner for a belt lane where the target
  set will change, and a reason to choose the sentinel for a core lane.
* **Splitters barely exist** (0 built in 104 team-games in the s47 micro-study).
  Score them with conveyors and move on.

## 9. NOT MEASURABLE / LIMITATIONS

* **Own-vs-enemy launcher attribution for the gunner-builder's delivery** — needs
  the launcher-proximity rule; not computed. Pantheon 39.8% / ph 66.2% displaced
  is stated unattributed.
* **`self_destruct()` vs an allied `destroy()`** — the replay emits the same
  `removeEntity` for both. Split only by the adjacency correlate (§3.5).
* **Bot stdout** is stripped from platform replays, so no team's own arm tags,
  target choices or state flags are readable — every behavioural claim here is
  reconstructed from engine-side events (positions, fires, removals).
* **The archive is not a random sample of the field** (corpus TRAP 4): it is
  dominated by our own games and by opponents we have played. Per-team era
  samples run 100-1,700 team-games and are stated inline everywhere.
* **The placebo event study is underpowered for O(1) (n=9/3) and ph (n=11/6).**
  Only Pantheon's estimate is banked.
* **Independence:** these are decoded GAMES, and games cluster in matches and
  opponents. Platform DEFF is 1.53 rated / 1.83 unrated; the census/deep-read
  numbers here are descriptive shares, but **any bar built on them must apply the
  correction and must restate a fail-to-exclude claim as an exclusion first.**

## 10. TOP SURPRISES

1. **The gunner is a RENTAL.** O(1) deletes **70.3%** of its forward gunners at
   FULL HP once the target is dead — refunding the **+20% cost-scale**
   contribution — and Clankers does it to 43.3% via an adjacent builder's
   `destroy()`. Controls inside the same games (their own sentinels: 0.000)
   say it is a policy, not a tracking artefact. We have never done it once, and
   it costs nothing to add.
2. **The line does not get eaten — it gets farmed.** 92-96% of consecutive shots
   in a facing segment land on the *same tile*, because the victim rebuilds there
   in a median of **2 rounds**. The commission's mental model was the wrong shape,
   and the right one (a parked farm) is *better*, not worse — it just has to be
   scored in throughput, never in buildings.
3. **The steering brief's two named subjects were both era-stale, in opposite
   directions.** **Leviathan's current bot builds ZERO gunners** in 386
   team-games (it swapped them 1:1 for sentinels at v74). And **sporks — the most
   selective forward planter — is not an economy shredder at all**: 82.5% of its
   gunner shots go into the enemy CORE, and its chosen-ray econ score is
   **0.35 against a random-ray baseline of 0.35**, the one team where the siting
   control runs the other way. The genuine shredders are Pantheon (139.2 econ
   kills/1000 shots) and O(1) (80.1% of shots on economy) — and **O(1)'s version,
   not Pantheon's, is the one that fits a sub-r300 kill doctrine.**

4. **The productive band is an identity, not a correlation.** Across **3,662
   current-version in-band gunners (d² 20-100), the share of shots at the enemy
   core is 0.000** — six teams, no exceptions. A gunner reaches 3 tiles; past 4.5
   it cannot see the core; so *the band is the plank*. Research found the same
   annulus from kill-excess with a completely different estimator. Magnus's
   "everything other than the core" turns out to be a geometric consequence of
   standing in the right place, not a targeting instruction.
5. **The timing prediction fails on this pipeline too.** Under permanent-cut
   economics an early cut should dominate. Measured, length-controlled, pooled
   over five shredders (n=774): win share by cut COUNT climbs 0.44 → 0.90, while
   win share by first-cut ROUND runs **backwards** (0.72 at <r40 → 0.85 at
   r150+) and stays flat-to-reverse inside cut-count strata. Both are confounded
   and neither identifies anything — which is the same verdict research reached
   from two other designs. **Three instruments, three refusals: this is a leg's
   question, not an archive's.**

6. **The replay tape and the source tree independently fingerprinted the same
   bug — and then the tree voided one of this study's own framings.** §5 measured
   off replays that v94's forward gunners scored **below a random ray** and had
   **nothing in range 51.7% of the time**; the archaeology then found the cause
   in `_v115dodge/main.py:2695-2699` — `_plan_siege` checked its ray against the
   **static wall map only**, with no live-target predicate. Two instruments, one
   verdict, neither told about the other. **But the same pass killed "we already
   aim as well as the field":** since v102 the tree has **exactly one gunner call
   site**, `_try_counterbattery`, keyed to `HUNT_BAND_DSQ = 41` of **our own**
   core — so every "in-band" gunner we have is a **map-geometry accident**, and
   the version axis cannot explain the v116→v140 share collapse because
   `main.py` differs by **14 lines, all of them raider salt state.**
7. **Our lateness is a PREDICATE, not a threshold — and nobody had looked.**
   `raid.py:688 tiles = core_tiles(E)` means **no code path in the live tree can
   plant a forward turret in the productive d²20-100 band at all**; the raider
   must walk to d²≤32 of the core footprint first. Every knob QUEUE #23 has been
   sizing (`LOKI_FWD_MIN_HARV`, `LOKI_FWD_TI_FLOOR`) sits *on top of* that. The
   timing fix and the siting fix are **the same one-line target-set edit.**

**Bonus, on us:** the v102 removal was correct and irrelevant. Our v94 "forward
gunner" put **52.8% of its shots into the core**, was built with **nothing in
range 51.7% of the time**, scored **below a random ray**, and rotated **4.32
times a life with 62.6% of its facing segments firing zero shots.** We did not
remove an economy shredder in v102. **We have never built one.**

---

## AMENDMENT (builder s48, ~05:5xZ) — two §-corrections + the control that strengthens the plank

* ⛔ §10.2's "victim rebuilds in median 2 rounds" DOES NOT REPRODUCE on research's
  unconditional decode (588,916 gunner-adjacent conveyor deaths: repaired-ever
  0.554, MEDIAN LAG 4, p75 19, mean 26.5, long-tailed; only 40.5% of repairs
  within 2). Likely definitional (shot-window conditioning); do not quote 2
  until reconciled. BELTBREAK-v2's "rebuilt within N" parameter reads this
  distribution, so N=2 vs N=4 is a live design difference.
* ⛔ §3.4's 92.5%-same-distance CANNOT corroborate farming: a facing segment
  ends at rotation, not at a kill, and the median segment (3 shots Pantheon =
  ceil(20/7); 5 O(1)/ph = ceil(30/7)) is ONE KILL — same-distance is true by
  construction with zero rebuilding. §3.4 measures shots-to-kill. The farming
  claim rests on the 55.5% rebuild-same-tile rate alone.
* ⭐ THE CONTROL (research): rebuild rate/speed is IDENTICAL near vs not-near a
  live enemy gunner (0.554/lag-4 vs 0.514/lag-3) ⇒ REBUILDING IS UNCONDITIONAL
  BELT MAINTENANCE, NOT ADAPTATION. Consequences: the farm does not degrade
  (no opponent-adaptation term needed), AND v2's N cannot be learned in-game
  (within-game rebuilds carry no information about our gunner — an adaptive
  counter would fit noise while looking like it works). N comes from the
  victim's TEAM-LEVEL repair table (0.008-0.702, median 0.296@10r) or a
  conservative constant.
