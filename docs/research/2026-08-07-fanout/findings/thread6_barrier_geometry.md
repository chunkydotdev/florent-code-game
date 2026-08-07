# Thread 6 — BARRIER SIEGE-RING GEOMETRY (geometry half)

Research session 2026-08-07. Read-only; no repo files edited, no runs, no platform calls.
Toolkit: `scratchpad/toolkit/siege_geometry.py` (reusable by the cross-check wave).
Raw table: `scratchpad/findings/siege_table.tsv` (30 rows = 15 maps x 2 seats).

**Headline: the 40-60 Ti claim is FALSE on 15/15 maps.** Denying every plantable
sentinel-plant tile costs **75-240 Ti** at the round-0 barrier price (median 168), and
the cheap alternative — a min vertex cut — is **15-75 Ti** but is a *map-halving wall*,
not a siege ring: it leaves 100% of the plant tiles plantable inside the pocket and is
launcher-bypassable at dsq 2 on **every map, both seats**.

---

## 0. Conventions, stated explicitly

* **Distance convention: `dsq` from the NEAREST core-footprint tile.** The core is 2x2
  and the map header stores the **NW corner**; every number below is
  `min over the 4 footprint tiles`. The NW-corner numbers are also reported
  (`nw_dsq`) because they differ materially — see §2.
* **Threat = the turret can hit the core**, not "the tile is in a distance band".
* All 15 maps are **rotational** symmetry, and every computed quantity is **identical
  for seat A and seat B on all 15 maps** — a free end-to-end validation of the parse.
  Only seat-A rows are shown; seat B is the same number.

## 1. Rule verifications done before computing anything

| Question | Answer | Evidence |
| --- | --- | --- |
| Can a Barrier sit on **ORE**? | **YES — measured** | 376 cached replays decoded: 370 barriers alive at end of game, **44 of them standing on `ENV_ORE_TITANIUM`**. e.g. `6a72565c-…_game_2.replay26` (15,10) built r59, (16,3) r61, (15,12) r62; `0a88ca71-…_game_3.replay26` (16,6) r144. `bots/_v70sm/main.py:259-270` shipped this as an *unverified* assumption with a self-shutoff; the shutoff was never needed. **Ore is in the deny-set.** |
| Does a turret threaten every tile in its radius? | **NO — alignment is required** | Gunner and Sentinel both fire a *single-tile-wide ray along their facing* (`docs/game-model.md:242-257`, `docs/reference/official-docs.md:238,253`). Facing is one of 8 directions. A tile is only a threat if it is row-, column- or diagonal-aligned with **some** core footprint tile. This removes **7-40 tiles per map (18-33%)** from the naive radius band — see `band_r32` vs `sent_threat` in §3. Any deny rule written off `dsq <= 32` alone over-buys by up to 40 barriers. |
| Do walls protect against a Sentinel? | **NO** | A Sentinel's line is "never blocked by walls or units in the way". A sentinel planted **behind a wall** still shells the core. Walls only constrain the **Gunner** (r²=13, ray stops at the first targetable tile). Consequence: `sent_plant_reach == sent_threat` on all 15 maps — terrain never isolates a single sentinel plant tile. |
| Effective reach | Sentinel 5 cardinal / 4 diagonal steps (r²=32); Gunner 3 cardinal / 2 diagonal (r²=13) | dsq arithmetic |
| Is 3 Ti the real barrier price? | **Only at round 0** | Cost is `floor(scale x 3)` and conveyor/splitter/barrier each add **+1%** (`docs/game-model.md:362`). The deny-set is built *reactively*, mid-game, when our own scale is already inflated — `docs/spitball.md` records **201 conveyor builds on meander**, i.e. scale ~3.0, i.e. **9 Ti per barrier**. Every Ti figure below is a round-0 floor; multiply by 1.3-3.0 for the realistic build window. |

## 2. Where the observed "core-dsq 10-41" band came from

The observed plant band (10-41) is a **NW-corner** measurement. Under the nearest-footprint
convention the same tiles are `dsq 5..32`, which is exactly the sentinel's r²=32 ceiling.
The two conventions are not interchangeable: the sentinel threat set reaches
**nw_dsq 50** on 10 of 15 maps (41 on the other 5), so an NW-corner rule capped at 41
**silently leaves the outer shell undenied**. Reported per map as `max_nwdsq` in the TSV.

## 3. Threat sets (per map, per core — seat A shown, seat B identical)

`band_r32` = naive "dsq<=32 to nearest footprint tile", no alignment.
`sent_threat` = tiles a **Sentinel** can shell the core from (aligned, r²<=32, unblockable).
`gun_threat` = tiles a **Gunner** can shell the core from (aligned, r²<=13, wall-LOS honoured).
`reach` = of those, the ones an enemy builder can plant on (plantable + an enemy-reachable
orthogonal standing tile). **On all 15 maps `reach == threat` — walls never deny a plant tile.**

| map | dims | walls | ore | core A | core B | band_r32 | **sent_threat** | gun_threat | gun-only | sent reach | gun reach |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| antler | 14x18 | 18 | 12 | 6,4 | 6,12 | 104 | **69** | 32 | 0 | 69 | 32 |
| archipelago | 26x26 | 208 | 38 | 5,5 | 19,19 | 80 | **58** | 28 | 0 | 58 | 28 |
| atoll | 18x18 | 18 | 8 | 2,14 | 14,2 | 69 | **49** | 36 | 0 | 49 | 36 |
| drumlin | 25x25 | 4 | 30 | 5,5 | 18,18 | 120 | **80** | 40 | 0 | 80 | 40 |
| eider | 28x20 | 22 | 32 | 7,9 | 19,9 | 111 | **77** | 38 | 0 | 77 | 38 |
| fjordgate | 10x10 | 10 | 6 | 2,2 | 6,6 | 62 | **44** | 35 | 0 | 44 | 35 |
| heart | 28x20 | 122 | 28 | 7,9 | 19,9 | 73 | **46** | 22 | 0 | 46 | 22 |
| hive | 25x25 | 34 | 12 | 2,20 | 21,3 | 76 | **56** | 36 | 0 | 56 | 36 |
| jackpot | 16x16 | 50 | 14 | 0,0 | 14,14 | 32 | **25** | 15 | 0 | 25 | 15 |
| lighthouse | 16x16 | 64 | 12 | 3,3 | 11,11 | 72 | **50** | 29 | 0 | 50 | 29 |
| meander | 25x15 | 8 | 24 | 11,3 | 11,10 | 99 | **68** | 36 | 0 | 68 | 36 |
| moonrise | 21x8 | 24 | 8 | 5,3 | 14,3 | 77 | **57** | 35 | 0 | 57 | 35 |
| nordkap | 20x26 | 74 | 22 | 9,6 | 9,18 | 111 | **76** | 40 | 0 | 76 | 40 |
| saga | 24x24 | 164 | 36 | 4,4 | 18,18 | 67 | **49** | 26 | 0 | 49 | 26 |
| snowflake | 26x26 | 70 | 32 | 5,5 | 19,19 | 107 | **69** | 35 | 0 | 69 | 35 |

`gun-only = 0` everywhere: the gunner threat set is a strict subset of the sentinel set on
every map. **There is exactly one geometry to defend, sized by the sentinel.**

Shell breakdown of the sentinel threat set (seat A; d = nearest-footprint dsq):

| map | d=1 | d=2 | d=4..8 | d=9..16 | d=17..32 | ore tiles in set |
| --- | --- | --- | --- | --- | --- | --- |
| antler | 8 | 4 | 15 | 23 | 19 | 2 |
| archipelago | 8 | 4 | 12 | 18 | 16 | 6 |
| atoll | 8 | 4 | 20 | 12 | 5 | 2 |
| drumlin | 8 | 4 | 20 | 24 | 24 | 3 |
| eider | 8 | 4 | 19 | 22 | 24 | 4 |
| fjordgate | 8 | 4 | 19 | 9 | 4 | 3 |
| heart | 8 | 4 | 7 | 11 | 16 | 2 |
| hive | 8 | 4 | 19 | 16 | 9 | 0 |
| jackpot | 4 | 1 | 6 | 9 | 5 | 2 |
| lighthouse | 8 | 4 | 13 | 13 | 12 | 5 |
| meander | 8 | 4 | 18 | 20 | 18 | 4 |
| moonrise | 8 | 4 | 17 | 17 | 11 | 2 |
| nordkap | 8 | 4 | 20 | 22 | 22 | 5 |
| saga | 8 | 4 | 14 | 14 | 9 | 2 |
| snowflake | 8 | 4 | 15 | 22 | 20 | 5 |

The `d=1` ring is the core's **8 orthogonal input tiles** — the same 8 tiles our conveyor
lanes terminate on. Those 12 tiles (d=1 and d=2) are **36 Ti of denial we get for free if
the economy is wired**, on 14 of 15 maps (jackpot's corner core gets 5 of them, 15 Ti).

## 4. Deny-set costs (all at the 3-Ti round-0 price; multiply 1.3-3.0x for real scale)

* **occupy** = a barrier on every reachable plantable sentinel-threat tile.
* **band-occupy** = the *claim's own* reading: only the tiles inside the observed NW-corner
  10-41 band. Leaves the outer shell open, so it does not remove the class either.
* **min-cut** = minimum vertex cut (Dinic max-flow on a split-node grid; walls and both
  core footprints are free blockers; the enemy spawn ring is uncuttable) separating the
  enemy spawn ring from every plant opportunity. Verified: `--selfcheck` confirms
  **0 leaks** on all 30 map-seats.
* **ring** = the same cut restricted to within dsq 100 of our core NW (the "siege ring"
  reading, as opposed to a map-halving wall).
* `ore_before/after` = ore tiles our own builders can walk to, before and after the cut.

| map | sent threat | **occupy Ti** | band-occ Ti | undeniable | **min-cut Ti** | cut tiles | ring Ti | ore before→after | pocket threat tiles left | launcher bypass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| antler | 69 | **207** | 135 | 0 | **48** | 16 | 48 | 12→6 | 59 | Y (dsq 2) |
| archipelago | 58 | **174** | 108 | 0 | **33** | 11 | 39 | 38→15 | 58 | Y (dsq 2) |
| atoll | 49 | **147** | 75 | 0 | **39** | 13 | 39 | 8→2 | 48 | Y (dsq 2) |
| drumlin | 80 | **240** | 162 | 0 | **60** | 20 | 60 | 30→7 | 79 | Y (dsq 2) |
| eider | 77 | **231** | 156 | 0 | **54** | 18 | 54 | 32→15 | 73 | Y (dsq 2) |
| fjordgate | 44 | **132** | 66 | **3** | 24* | 8 | 24* | 6→4 | 33 | Y (dsq 2) |
| heart | 46 | **138** | 87 | 0 | **39** | 13 | 39 | 28→9 | 42 | Y (dsq 2) |
| hive | 56 | **168** | 96 | 0 | **39** | 13 | 39 | 12→1 | 56 | Y (dsq 2) |
| jackpot | 25 | **75** | 51 | 0 | **15** | 5 | 15 | 14→2 | 25 | Y (dsq 2) |
| lighthouse | 50 | **150** | 96 | 0 | **36** | 12 | 39 | 12→6 | 47 | Y (dsq 2) |
| meander | 68 | **204** | 129 | **2** | 75* | 25 | 78* | 24→12 | 58 | Y (dsq 2) |
| moonrise | 57 | **171** | 105 | 0 | **24** | 8 | 24 | 8→3 | 53 | Y (dsq 2) |
| nordkap | 76 | **228** | 150 | 0 | **36** | 12 | 36 | 22→8 | 74 | Y (dsq 2) |
| saga | 49 | **147** | 81 | 0 | **33** | 11 | 33 | 36→17 | 49 | Y (dsq 2) |
| snowflake | 69 | **207** | 138 | 0 | **24** | 8 | 30 | 32→13 | 69 | Y (dsq 2) |

`*` **fjordgate and meander cannot be denied at any price.** `undeniable` counts threat
tiles inside the **enemy's own spawn ring**: on fjordgate (cores 2,2 / 6,6, footprint
separation dsq **18**) and meander (11,3 / 11,10, separation dsq **36**) the enemy can plant
a sentinel on its own doorstep and still shell our core. The starred cut prices cover the
*remaining* tiles only; the class survives regardless.

### 4a. Why the cheap min-cut is a mirage

The recovered cuts are **midline walls**, not core rings. Examples (seat A):

* **eider** (54 Ti, 18 tiles): a literal vertical wall down **x=13** on a 28-wide map —
  `(13,0),(13,1),(13,2),(12,3),(12,5),(13,6)…(13,13),(12,14),(12,16),(13,17),(13,18),(13,19)`.
* **hive** (39 Ti, 13 tiles): the anti-diagonal —
  `(0,8),(2,10),(3,11),(4,12),(5,13),(6,14),(8,16),(9,17),(10,18),(12,20),(13,21),(14,22),(16,24)`.
* **moonrise** (24 Ti, 8 tiles): `x=10/11` across a 21x8 map.

Three independent reasons the cut does not remove the class:

1. **It denies nothing.** `pocket threat tiles left` is 100% of the threat set on
   archipelago/hive/jackpot/snowflake and >85% everywhere. The cut blocks *walking*, not
   *planting*. One breach and the full plant menu is live.
2. **Launcher bypass on 15/15 maps, both seats, at min dsq = 2.** The cut is one barrier
   thick, so an outside tile is always *diagonally adjacent* to a pocket tile. Throw range
   is r²=26 — a Launcher built anywhere near the wall throws a builder straight over it onto
   a bot-passable pocket tile. This is not a marginal exploit: `docs/game-model.md:267-283`
   records the field **already** doing launcher delivery (sporks, Albert And Einstein, all
   5 games of ladder replay `81d83bb5`). A cut is defeated by 20 Ti and one action.
3. **It costs our own economy more than it costs them.** `ore_before→after`:
   hive **12→1**, jackpot **14→2**, atoll **8→2**, drumlin **30→7**, moonrise **8→3**.
   On hive — where our current loss mode is *farm death then 10:1 economy starvation*
   (measuring-session update, 2026-08-07) — the min-cut wall would hand the game away by
   itself. And the wall sits on the **midline**, i.e. contested ground we cannot hold.

Even ignoring launchers, a 1-thick wall is chewable: **2 sentinel shots (36 dmg > 30 HP,
20 ammo ≈ 20 Ti)** or 15 builder attacks (30 Ti). We repair at 4 HP/Ti, so we win the
attrition trade on titanium — but the wall is only ever a delay, never a structural removal.

### 4b. Cut tiles, 3 cheapest maps

| map | cut Ti | tiles (seat A) | tiles (seat B) |
| --- | --- | --- | --- |
| **jackpot** | **15** (5 barriers) | (0,10) (4,10) (7,1) (7,8) (8,7) | (7,8) (8,7) (8,14) (11,5) (15,5) |
| **snowflake** | **24** (8) | (0,17) (1,16) (11,14) (12,13) (13,12) (14,11) (16,1) (17,0) | (8,25) (9,24) (11,14) (12,13) (13,12) (14,11) (24,9) (25,8) |
| **moonrise** | **24** (8) | (10,0) (10,1) (10,2) (10,5) (10,6) (10,7) (11,3) (11,4) | (9,3) (9,4) (10,0) (10,1) (10,2) (10,5) (10,6) (10,7) |

Note every one of these is a **map bisection**, and in each case the launcher bypass flag
is set. jackpot additionally drops us from 14 reachable ore tiles to 2.

## 5. Independent validation of the parse

Cross-checked against `bots/opp_v58/main.py:1126-1155` (`_rush_deny_tiles`), a top-field
bot's **hand-derived** rush-deny table for 6 map/seat combinations. Map dimensions and core
NW corners match my parse **exactly** in all 6 cases (nordkap 20x26 @ (9,18); moonrise 21x8
@ (5,3)/(14,3); jackpot 16x16 @ (0,0)/(14,14); meander 25x15 @ (11,3)).

Of their 27 hardcoded tiles, **24 land inside my computed sentinel threat set** (and 22 in
the gunner set). The 3 misses are informative:

* **jackpot-A (3,2) is a WALL tile** in the shipped map — a dead entry in their table; no
  building can ever exist there, so their melee-else-barrier branch is a permanent no-op.
* **moonrise-A (9,2) and (10,2)** are non-aligned (fp_dsq 10 and 17): a turret there
  **cannot hit the core at all**. They are rush-*gun staging* tiles (covering a corridor
  against builders), not core-shelling tiles — consistent with their code comment
  ("known rush gun tiles"), and consistent with my model rather than against it.

## 6. Predictive trigger spec — "a threat tile an enemy builder could REACH next turn"

The trigger must never be "we are under attack": the HP-bar signal arrives ~40 rounds late
(`docs/spitball.md`, Bahrani/ACoIaF). Spec:

**State (all computed once, in `__init__`/first `run()` of each defending unit — one
`Player` instance per unit, attributes persist for its lifetime, `docs/game-model.md:27`):**

1. `THREAT: frozenset[int]` — packed `x * H + y`. Built by **pure arithmetic**, no tile
   queries: for each of the 4 core footprint tiles, for each of the 8 directions, walk
   `k = 1..5`, keep tiles with `(dx*k)² + (dy*k)² <= 32` and in bounds. **144 candidates,
   deduping to 25-80 tiles.** Measured cost **66 µs/call** locally (~150-200 µs on
   Graviton3) against a 10,000 µs budget — a one-time 2% of one turn.
   *This is why the geometry must be arithmetic and not sensed:* `get_tile_env()`,
   `is_tile_passable()` and `get_tile_building_id()` **raise** on anything outside the
   caller's current vision (`docs/game-model.md:413-421`), and the core's r²=36 vision
   covers only **21-73 of the 25-80 threat tiles** (`core_sees` column). A map scan is not
   available; the alignment/radius geometry needs no map at all.
2. `ALERT: frozenset[int]` — every passable tile within **Manhattan 2** of a THREAT tile.
   Size **45-169 tiles** per map. Manhattan 2 is the correct radius: an enemy builder at B
   can be orthogonally adjacent to threat tile T next turn iff `manhattan(B,T) <= 2`
   (move this round, build next round); at `manhattan == 1` it can plant **this** round.
   Derivable lazily from THREAT with one 13-offset stencil.
3. Optional `PLANTED: dict[int, int]` — tile → enemy building id, for the "already there"
   branch.

**Per-round evaluation (the defender builder, and the core as a second pair of eyes):**

```
me = ct.get_team()
for uid in ct.get_nearby_units():          # ~5-15 ids
    if ct.get_team(uid) == me: continue
    if ct.get_entity_type(uid) != EntityType.BUILDER_BOT: continue
    k = pack(ct.get_position(uid))
    if k in ALERT:                          # imminent: plant this or next round
        fire the deny/intercept
```

Cost: 3 controller calls per visible enemy unit plus a set lookup — well inside budget even
at 15 enemies. **Never scans the map, never calls a tile query, never depends on HP.**
Publish the triggering tile to the comms store for the other defenders, remembering the
store cannot represent 0 (`docs/game-model.md:429-433`) — publish `x+1, y+1`.

Escalation ladder once triggered, cheapest first — the geometry says denial should be
**local and reactive**, not a prophylactic ring:
(a) **body-block**: builder bots are mutually impassable, so standing on the tile costs 0 Ti;
(b) **build anything friendly on it** — a **conveyor** (3 Ti, same price as a barrier, same
+1% scale) makes the tile non-empty and therefore unplantable, and unlike a barrier it is
**bot-passable and does not block our own LOS or movement**. Prefer conveyors on lane tiles
and barriers only for the residue;
(c) barrier;
(d) if a turret already landed: 20 builder-attacks kill a Sentinel (40 Ti, 20 rounds solo /
7 rounds with 3 builders), 13 kill a Gunner (26 Ti).

**Reactive removal is cheaper than prophylactic denial on every map in the pool** — 40 Ti to
delete a landed Sentinel versus 75-240 Ti (×1.3-3.0 for scale) to deny the ground it could
land on.

## 7. Verdict on the "~40-60 Ti structurally removes the chip class" claim

Read literally ("denying every plantable tile in the band"), against the true threat set:

| map | tiles to deny | **cost @3 Ti** | 40-60 Ti? | band-only (nw 10-41) cost | verdict |
| --- | --- | --- | --- | --- | --- |
| antler | 69 | 207 | no (3.5x) | 135 | **FALSE** |
| archipelago | 58 | 174 | no (2.9x) | 108 | **FALSE** |
| atoll | 49 | 147 | no (2.5x) | 75 | **FALSE** |
| drumlin | 80 | 240 | no (4.0x) | 162 | **FALSE** |
| eider | 77 | 231 | no (3.9x) | 156 | **FALSE** |
| fjordgate | 44 | 132 | no (2.2x) | 66 | **FALSE** — and structurally impossible (3 undeniable tiles) |
| heart | 46 | 138 | no (2.3x) | 87 | **FALSE** |
| hive | 56 | 168 | no (2.8x) | 96 | **FALSE** |
| jackpot | 25 | **75** | no (1.25x) | **51** | **FALSE** — closest map; the 51 Ti band variant leaves 8 of 25 tiles open |
| lighthouse | 50 | 150 | no (2.5x) | 96 | **FALSE** |
| meander | 68 | 204 | no (3.4x) | 129 | **FALSE** — and structurally impossible (2 undeniable tiles) |
| moonrise | 57 | 171 | no (2.9x) | 105 | **FALSE** |
| nordkap | 76 | 228 | no (3.8x) | 150 | **FALSE** |
| saga | 49 | 147 | no (2.5x) | 81 | **FALSE** |
| snowflake | 69 | 207 | no (3.5x) | 138 | **FALSE** |

**FALSE on 15/15.** Median true cost **168 Ti** at the round-0 price, **~340-500 Ti** at the
mid-game scale the deny-set would actually be built at. The 40-60 Ti figure corresponds only
to the min *cut* (15-75 Ti, median 36), and a cut is not structural removal: it leaves every
plant tile plantable, is launcher-bypassable on 15/15 maps at dsq 2, sits on the contested
midline, and on hive/jackpot/atoll/drumlin costs us 65-86% of our own reachable ore.

**What survives of the idea, and is cheap:**

1. **Alignment, not radius.** Whatever gets built, deriving the set from turret *alignment*
   rather than `dsq <= 32` removes 18-33% of the tiles (7-40 barriers) for free.
2. **The d=1/d=2 ring is 12 tiles = 36 Ti and is already ours** if the economy is wired —
   conveyors on the core's 8 input tiles are denial we are paying for anyway.
3. **Predictive trigger + local reaction** (§6) is the shippable half: static arithmetic
   threat set, 66 µs, no map scan, and 40 Ti to delete what does land.
4. **fjordgate and meander are exempt from any denial doctrine** — the enemy shells our core
   from its own spawn ring there. Those two maps need a different answer entirely.

## 8. Not done / out of scope

* Cross-check against where **Lunds/kladde/CAD/Flotte actually planted** in decoded losses —
  explicitly a later wave. `siege_geometry.py` exposes `SeatAnalysis.sentinel_threat`,
  `.gunner_threat`, `.fp_dsq`, `.nw_dsq` and `verify_barrier_on_ore()` for exactly that.
* Launcher bypass is **flagged, not modelled** — no attempt to price the enemy's launcher
  build, nor to search for a 2-thick cut that would resist a throw.
* Whether `can_build_*` refuses a tile occupied by a **builder bot** is unverified
  (`is_tile_empty()` is documented as "no building and not a wall"); the body-block rung of
  §6's ladder depends on it and should be probed before being relied on.
* Mid-game occupancy is ignored: all reachability is computed on the **round-0 bare map**
  (only the two cores exist). Conveyors/splitters are bot-passable so they do not change
  reachability; harvesters and turrets would, in our favour.
