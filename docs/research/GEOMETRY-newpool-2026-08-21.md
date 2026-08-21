# NEW-POOL GEOMETRY DECODE — the rotated 15, 2026-08-21

| | |
|---|---|
| **Author** | fresh **opus** decode agent, **research lane, s52** — the rotation standing commission (builder's 08:00:36Z note, `docs/coordination.md:72045`; research announce 08:17:22Z, `:72067`) |
| **Clock** | started `Fri 21 Aug 2026 08:17:57 UTC` (`date -u`, same shell); tape pulled 08:2xZ |
| **Scope** | decode / analysis only. No games fired, no bot edits, no platform mutation. `fcode match list/info` are reads. |
| **Substrate** | `maps/*.map26`, parsed with `tools/map_encode.parse_map26` |
| **Instrument** | `scratchpad/geom.py` (session scratchpad, NOT committed), `scratchpad/sig.py`, `scratchpad/f1b.py`; gate verdicts from `scratchpad/s52_rotation/gatemap_rot.py` (builder's, unmodified) over `scratchpad/s52_v535_build/harness.py` |
| **Committed?** | **NO** — banked only, per commission |

**LABELS USED THROUGHOUT.** **MEASURED** = read off a map file, a bot constant, a
driven predicate, or the platform tape. **GEOMETRY-INFERENCE** = a class assignment
made from a measured number against a banked threshold; it predicts *which gate fires*
and *which mechanism has room to bite*, **never a win rate**.

---

## 0. INSTRUMENT PROVENANCE — three controls, each capable of the other verdict

**C1 — the decoder.** `tools/map_encode.py --selftest` **PASS**: five old-pool maps
(fjordgate, antler, drumlin, nordkap, archipelago) reproduce their committed
`MAP_CODES` strings **byte-for-byte**, and a **single corrupted cell in fjordgate
fails to match**. ⇒ the 0/1/2 env mapping, row order, packing and core anchors are
proven, not assumed.

**C2 — the chain metric.** `geom.py --cal` reproduces `BUILD-REPORT-v537socket-2026-08-21.md`
§2.3 **digit for digit on all four cells it publishes, and on BOTH seats**:

```
[ok] yulerune     expect (oreman 6, chain 5)   got A=(6,5) B=(6,5)
[ok] icefloe      expect (6, 5)                got A=(6,5) B=(6,5)
[ok] drakkarfjord expect (9, 8)                got A=(9,8) B=(9,8)
[ok] glacierkeep  expect (11, 10)              got A=(11,10) B=(11,10)
CAL PASS
```
The calibration set spans **shallow (5) and deep (10)**, so the metric has been seen to
return both verdicts. auroraveil, whose report row is the loose range "7-9", reads **7**
— on the arming side of the same cap the report assigns it ("no").

**C3 — the map bytes are the PLATFORM's bytes.** `match info --json` publishes each
map's S3 object as a sha256. Local file vs platform hash, over the 8 distinct pool maps
drawn in today's two post-rotation matches: **8/8 MATCH** (auroraveil, fimbulwinter,
helheim, icefloe, jotunheim, longhouse, midgard, yggdrasil). The remaining 7 pool maps
have not yet been drawn in one of our matches and are therefore **unverified against the
platform** — they are the committed sync, nothing stronger.

⚠ **One metric defect found and fixed mid-run, disclosed:** the choke `corridor` column
originally minimised over *all* BFS layers including the two core-seat layers, so a map
whose single seat happened to sit on the unique shortest path read `corridor = 1` for a
reason that has nothing to do with terrain. Caught by **rendering stavkirke and seeing a
six-tile-wide gap** where the number said one. Seat layers are now excluded. stavkirke
still reads 1 (at layer 3 of 19) — that one is real; ragnarok's 1 was the artefact and
is now 2.

⚠ **Anchor discrepancy between two banked docs, resolved in favour of the build report.**
`DIFF-STUDY-v169-craters` §Step-5 tabulates "nearest ore (Manhattan)" as icefloe **7**,
drakkarfjord **10**; `BUILD-REPORT-v537socket` §2.3 gives **6** and **9** for the same
maps. The difference is the anchor (core *tile* vs core *footprint*). This report uses
the **footprint** anchor, because that is the one the cap-comparison doc uses and the one
that reproduces exactly. Any cross-reference to the crater study's ore column must add 1.

---

## 1. Q1 — PER-MAP GEOMETRY, ALL 15 (MEASURED)

Columns: `core-sep` = Manhattan between the two 2×2 NW anchors / `dsq` = anchor
distance² (**the quantity the ferry gate tests**) / `footsep` = closest footprint-tile
Manhattan. `ore` = nearest ore, Manhattan, from the **core footprint**. **`chain`** =
**the mouth-chain length** — the number of CONVEYOR TILES in the shortest trunk from a
tile orthogonally beside some ore to one of the 8 delivery seats beside our own 2×2 Core,
routing only over tiles that are neither WALL nor ORE (the link BFS blocks ore,
`doctrine.py:557`), endpoints inclusive. **This is the quantity `V530_MOUTH_MAX_LINKS`
is compared against** (`if not plan or len(plan) > V530_MOUTH_MAX_LINKS`). `corr` =
narrowest layer of the core-to-core shortest-path corridor (choke proxy, seat layers
excluded). `cpath` = core-ring-to-core-ring BFS distance (**transit length**).
Every map reads **identically on both seats** for ore and chain — the pool is symmetric,
so any seat asymmetry we see in play is CODE, not terrain (v537 build report §2.4).

| map | dims | coreA | coreB | core-sep (M / dsq / foot) | **ore** | **chain** | **cap6 class** | corr | cpath | ore tiles / clusters | wall% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **bifrost** ᴺ | 26×12 | 2,5 | 22,5 | 20 / 400 / 19 | 5 | **4** | SHALLOW | 2 | 25 | 20 / 9 | 9.0 |
| **fimbulwinter** ᴺ | 20×20 | 2,1 | 16,17 | 30 / 452 / 28 | 4 | **3** | SHALLOW | 2 | 26 | 14 / 10 | 19.0 |
| **helheim** ᴺ | 18×18 | 2,8 | 14,8 | 12 / 144 / 11 | 3 | **2** | SHALLOW | 2 | 13 | 16 / 10 | 18.5 |
| **holmgang** ᴺ | 12×12 | 1,1 | 9,9 | 16 / 128 / 14 | 3 | **2** | SHALLOW | 3 | 12 | 6 / 6 | 5.6 |
| **jotunheim** ᴺ | 24×24 | 4,4 | 18,18 | 28 / 392 / 26 | **11** | **10** | ⛔ **DEEP** | 3 | 24 | 20 / 7 | 4.5 |
| **longhouse** ᴺ | 28×18 | 2,8 | 24,8 | 22 / 484 / 21 | 6 | **5** | SHALLOW | 2 | 35 | 16 / 10 | 11.1 |
| **paths** ᴺ | 24×24 | 1,11 | 21,11 | 20 / 400 / 19 | 4 | **3** | SHALLOW | 2 | 23 | 28 / 18 | 31.6 |
| **skald** ᴺ | 16×16 | 7,1 | 7,13 | 12 / 144 / 11 | 3 | **2** | SHALLOW | 2 | **9** | 16 / 8 | 6.2 |
| **stavkirke** ᴺ | 22×22 | 9,2 | 9,18 | 16 / 256 / 15 | 6 | **5** | SHALLOW | **1** | 19 | 16 / 10 | 14.0 |
| **yggdrasil** ᴺ | 30×30 | 3,3 | 25,25 | 44 / 968 / 42 | 6 | **5** | SHALLOW | 3 | 40 | 22 / 15 | 9.8 |
| auroraveil ˢ | 20×20 | 9,1 | 9,17 | 16 / 256 / 15 | 7 | **7** | ⛔ **DEEP** | 2 | 17 | 16 / 13 | 17.5 |
| glacierkeep ˢ | 30×30 | 14,2 | 14,26 | 24 / 576 / 23 | **11** | **10** | ⛔ **DEEP** | 2 | 21 | 24 / 13 | 7.6 |
| icefloe ˢ | 20×20 | 1,16 | 17,2 | 30 / 452 / 28 | 6 | **5** | SHALLOW | 3 | 26 | 20 / 20 | 8.5 |
| midgard ˢ | 30×30 | 2,2 | 26,26 | 48 / 1152 / 46 | 3 | **2** | SHALLOW | 2 | **44** | 16 / 13 | 7.3 |
| valkyrie ˢ | 30×30 | 2,14 | 26,14 | 24 / 576 / 23 | 6 | **5** | SHALLOW | 2 | 23 | 16 / 14 | 6.9 |

ᴺ = new this rotation · ˢ = survivor.

**REFERENCE ROW — the maps the crater mechanism was measured on, same instrument:**

| map | dims | ore | chain | cap6 | cpath | fate |
|---|---|---|---|---|---|---|
| glacierkeep | 30×30 | 11 | **10** | DEEP | 21 | **SURVIVES** |
| drakkarfjord | 30×30 | 9 | **8** | DEEP | 40 | **ROTATED OUT** |
| auroraveil | 20×20 | 7 | **7** | DEEP | 17 | **SURVIVES** |
| yulerune | 20×20 | 6 | 5 | shallow | 25 | ROTATED OUT |
| icefloe | 20×20 | 6 | 5 | shallow | 26 | **SURVIVES** |
| royale | 20×20 | 6 | 5 | shallow | 19 | ROTATED OUT |
| frostgate | 20×20 | 3 | 2 | shallow | **11** | **ROTATED OUT** |
| ragnarok | 30×30 | 3 | 2 | shallow | 44 | ROTATED OUT |

### 1.1 THE CAP6 ANSWER

**Threshold, MEASURED from source across every tree that has it** (`grep -h
'^V530_MOUTH_MAX_LINKS' bots/*/doctrine.py`):

| tree | `V530_MOUTH_MAX_LINKS` |
|---|---|
| `_v530home`, `_v531fix`, `_v532weave` | **16** |
| `_v533home`, `_v534maptrust` | **6** — the `cap6` diagnostic arm, ADOPTED |
| `_v529merge`, `_v536trustport`, **`_v537socket` (LIVE)** | **absent — no MOUTH plank at all** |

So "cap6" is not a hypothetical: it is the value that the **home-package trees ship**,
and it is the value `BUILD-REPORT-v537socket` §2.3 tabulates against. It is **not** a
constant on our live line, which has no mouth at all (next paragraph).

**Deep-ore maps in the new pool (chain > 6): THREE — `jotunheim` (10), `glacierkeep`
(10), `auroraveil` (7).** Twelve are shallow (chain 2-5), and **eight of them sit at
chain ≤ 5, i.e. the mouth would arm with a link to spare.**

⭐ **`jotunheim` IS THE NEW `glacierkeep`, and it is the only new map in the class.**
24×24, **4.5% walls** (the emptiest board in the pool), **20 ore tiles in only 7
clusters** — and every one of them far from both cores. Its 11-Manhattan / 10-link
nearest ore ties glacierkeep's for the deepest in the pool, on a *smaller* board.
`drakkarfjord` (the other old crater) rotated OUT; **the crater class did not shrink,
it swapped a member.**

⛔ **AND THE COMMISSION'S PREMISE NEEDS ONE CORRECTION BEFORE THIS TABLE IS READ AGAINST
OUR LIVE LINE: `bots/_v537socket` HAS NO MOUTH PLANK AT ALL.** MEASURED —
`grep -c mouth bots/_v537socket/eco.py` = **0**; no `FS_V530_MOUTH`, no
`V530_MOUTH_MAX_LINKS` anywhere in the tree. v537 descends from `_v536trustport` =
`_v529merge` + MAPTRUST, and `_v529merge` is the branch that never had MOUTH. What ships
instead is the **unconditional socket claim** (`FS_V537_SOCKET = True`,
`FS_V537_BY_ROUND = 4`, `FS_V537_MAX_SOCKETS = 2`, `FS_V537_SIDE_SPREAD = True`) —
explicitly built as "MOUTH's idea with the two gates that disqualified it removed: no
route-length cap and no route at all" (§2.3 of the build report).
⇒ **the cap6 taxonomy is now DIAGNOSTIC, not a live gate on our line.** What it still
predicts is where the **underlying trunk order** (still ore-end-first in v537) leaves a
long unbuilt belt — i.e. **which maps the socket plank is load-bearing on**. Those are
exactly the three DEEP maps. On the twelve shallow maps our belt reaches the seat by
r2-r8 with or without the plank.

### 1.2 CHOKE / WALL STRUCTURE, one line each (MEASURED; renders in `geom.py --render`)

* **bifrost** 26×12 — widest-aspect board. Two `####`-bracketed pillars at x≈7 and x≈18
  split the board into three lanes; cores face each other along the middle row. Ore: a
  central 8-tile block plus corner singletons.
* **fimbulwinter** — diagonal cores, 19% walls in a lattice of 2×2 blocks; no single
  choke (corr 2), many short detours. Ore is scattered singletons/pairs.
* **helheim** — mirror-symmetric across the centre; a **4×4 solid wall block directly
  between the cores**, flanked N/S by two `oooo` 4-tile ore bands. Cores 13 apart.
* **holmgang** 12×12 — smallest board in the pool. Almost open (5.6% walls, two 2-tile
  wall stubs). **Only 6 ore tiles, all singletons.** Diagonal cores.
* **jotunheim** — emptiest board (4.5%), three small `###` blocks, no choke worth the
  name. All ore is central-or-far; **nothing within 10 links of either core.**
* **longhouse** 28×18 — two long **8-tile wall barns** at x=10 and x=17 forming a walled
  central corridor with the only central ore (two 2×2 blocks) inside it. `cpath` **35**
  — the second-longest transit in the pool despite only 28 width.
* **paths** — **31.6% walls, by far the maziest**. Ore sits in 1-tile wall pockets
  (`#o#`) and a walled central chamber. 28 ore tiles in 18 clusters. Corridor 2.
* **skald** — small, open, four `##` corner blocks and stacked central `oo` pairs.
  **`cpath` 9 — the SHORTEST transit in the pool, shorter than frostgate's 11.**
* **stavkirke** — nested-ring fortress: an outer `######` ring, an inner `########` box,
  ore both on the outer ring and inside the box. **The only `corridor = 1` in the pool**
  (layer 3 of 19) — a genuine single-tile pinch on the shortest core-to-core path.
* **yggdrasil** 30×30 — long horizontal wall bars top/bottom, two `#o.o#` ore boxes and a
  central 4×2 `oooo` block. `cpath` **40**. Sparse clusters.

---

## 2. Q2 — FIXTURE SURVIVORSHIP (MEASURED against the rotated pool list)

### 2.1 `#101` — the team-lazy BAD six / GOOD five

| set | members | **survive** | **retired** |
|---|---|---|---|
| **BAD six** (2/28 = 7.1%) | nordkap, fjordgate, ragnarok, archipelago, **auroraveil**, royale | **auroraveil ONLY (1 of 6)** | 5 of 6 |
| **GOOD five** (27/29 = 93.1%) | **icefloe**, drakkarfjord, yulerune, **glacierkeep**, drumlin | **icefloe, glacierkeep (2 of 5)** | 3 of 5 |
| **deterministic cells** | midgard/seatA r91×3, ragnarok/seatB r108×3 | **midgard/seatA ONLY** | ragnarok cell gone |

⇒ **`#101`'s cell inventory is 3 of 11 named cells.** The row's headline arithmetic
(−3.08 Elo/match, "the entire deficit is the six BAD maps") is computed over a map set
that is **83% retired**, so **the pricing does not transport** and the row needs a
re-derivation on new-pool tape before it is cited again. The builder's read ("team lazy's
BAD-map coin: 5 of 6 BAD maps GONE") is confirmed digit-for-digit here.
**One usable regression fixture survives: `midgard / seat A`, the r91-to-the-turn cell.**

### 2.2 Crater cells (`DIFF-STUDY-v169-craters`)

| cell | role in the study | fate |
|---|---|---|
| **glacierkeep** | THE crater; Gate-1 mechanism fixture (never-claim 83-90% → ~0) | **SURVIVES — Gate 1 is intact and needs no substitute** |
| **drakkarfjord** | 2nd crater; 30-34 of the recoverable games | **RETIRED** |
| **auroraveil** | 3rd latent crater (36% never-claim); **the study's built-in falsifier cell** | **SURVIVES** |
| yulerune, icefloe | the `_v529merge`-only socket regression pair | yulerune **RETIRED**; icefloe **SURVIVES** |
| ragnarok | the within-map positive control (we win 180/180 doing it to them) | **RETIRED — the study's positive control is gone** |

⇒ **Gate 1 (n=60, glacierkeep × 30 seeds × 2 seats) SURVIVES UNTOUCHED.**
⇒ **Gate 2 (n=180, glacierkeep + drakkarfjord + auroraveil) LOSES ONE OF ITS THREE
LEGS.** GEOMETRY-INFERENCE: **`jotunheim` is the drop-in replacement** — identical cap6
class, identical chain (10), same symmetric-pool structure. Substituting it makes Gate 2
a **new-pool** fixture rather than an archive one, which is what the currency read needs
anyway.
⚠ Note the study's ragnarok control has no new-pool equivalent at chain 2 + `cpath` 44;
**midgard is the nearest structural match** (chain 2, cpath 44, 30×30) — but midgard is
the one map our line REFUSES on, so it cannot serve as a ferry-siege control.

### 2.3 `#103` — the midgard refusal

**MIDGARD SURVIVES. THE ROW STAYS LIVE, AND IT IS NOW A LARGER SHARE OF THE POOL** —
1 of 15 maps instead of 1 of 15 in a pool where archipelago also refused. **MEASURED on
the live tree** by driving `SiegeMixin._fs_map_gated` (builder's `gatemap_rot.py`,
unmodified) over all 15 pool maps × 2 seats:

```
_v537socket:  POOL CELLS 30 | refuse 2 | run 28
              POOL REFUSING MAPS (1 of 15): midgard   (6.6667%)
```
Reproduces the builder's 08:00 note exactly. **The gate that fires is
`FS_V525_CRIPPLE_MAPS`** — signature `(30,30,(2,2),(26,26))`, grid-confirmed by v524's
exact-grid match (the signature is shared with ragnarok, which has now rotated out, so
the disambiguation is currently unexercised). **NOT `FS_MAP_SKIP`**, confirming the row's
own GREP note.

### 2.4 frostgate — **RETIRED. THE PUREST CONVERSION EXHIBIT IS GONE.**

`frostgate` (20×20, cores (2,9)/(16,9)) is **not in the new 15**. All three frostgate
games in the v174 field-debut set — `d4566d49…_game_3` (kladde), `717140d8…_game_5`
(farming_200s), `9d2247c3…_game_5` (Juusto) — are now **archive-only**. So is the control
that made the call unarguable: the farming_200s game where **their core had zero
defensive turrets for 109 rounds** while our bot #11 parked on their socket at (15,9) for
**85 consecutive rounds** and never swung.
⇒ **`AUTOPSY-v174-losses` §"frostgate is a CONVERSION crater" can no longer be re-run
in-pool.** The finding stands (it is a claim about our *verb*, not about the map), but the
fixture that demonstrated it must be re-sited. See §3(b) for the geometric substitutes.
⚠ **Note also: `yulerune` shares frostgate's exact signature (20,20,(2,9),(16,9)) and
also rotated out** — so both members of that signature class left together.

### 2.5 ⭐ THE SURVIVING FIXTURE SET, named for the post-rotation probes

| fixture | map(s) | what it still measures | status |
|---|---|---|---|
| **F-CRATER-1** | glacierkeep × 30 seeds × 2 seats | socket never-claim %, the Gate-1 mechanism metric (`ringtime.py`, `a_own1_r`/`b_own1_r`, `never` = −1) | **INTACT** |
| **F-CRATER-2** | glacierkeep + auroraveil **+ jotunheim** | Gate-2 currency; auroraveil remains the built-in falsifier | **REBUILT** (drakkarfjord → jotunheim) |
| **F-REFUSAL** | midgard, both seats | `#103` — deterministic refusal, 2/2 cells, discriminates at tiny n | **INTACT** |
| **F-LAZY-DET** | midgard / seat A | `#101`'s only surviving kill-to-the-turn regression cell (r91×3) | **INTACT, 1 of 11** |
| **F-SOCKET-REG** | icefloe | the `_v529merge` socket-regression cell (33% never / 8% win vs 0% / 37%) | **INTACT** (yulerune half gone) |
| ~~F-CONVERSION~~ | ~~frostgate~~ | park-without-converting, with a zero-turret control | ⛔ **RETIRED — no in-pool substitute carries the zero-turret control** |
| ~~F-CONTROL-POS~~ | ~~ragnarok~~ | the "we do it to THEM" within-map positive control | ⛔ **RETIRED** |

---

## 3. Q3 — NEW-MAP RISK RANKING FOR OUR LINE

⚠ **THIS IS A GEOMETRY READ. It says which mechanism has ROOM to bite and which gate
fires by construction. It is NOT a win-rate prediction and must not be quoted as one.**
Every threshold cited is MEASURED from `bots/_v537socket/doctrine.py`; every map number
is MEASURED from the map file; the *pairing* of the two is the inference.

### (a) SOCKET-RACE-HARD — deep ore, our trunk arrives late

Ranked by chain length (the mechanism's own dose axis; the study's dose is monotone,
0 usable seats ⇒ 0/119 games delivered anything).

1. ⛔ **jotunheim (NEW) — chain 10, ore 11, 4.5% walls.** GEOMETRY-INFERENCE: **the
   glacierkeep class exactly**, and it is the pool's *only* new member of it. The socket
   plank (claim by r4, cap-free) is the whole of our answer here, and jotunheim is the
   cell where it has never been measured.
2. **glacierkeep (survivor) — chain 10.** Known crater, known 83-90% never-claim in the
   pre-plank arms. Unchanged.
3. **auroraveil (survivor) — chain 7.** The falsifier cell. Still the third crater, still
   the one that decides whether the mechanism story is right.

*Tight core adjacency for pluggers* — the second half of (a) — does **not** co-occur with
deep ore anywhere in this pool: all three DEEP maps have `cpath` 17-24, i.e. their plug
has to travel as far as our belt does. **The pool contains no "deep ore + short transit"
map**, which is the worst possible combination and which we do not have to face.

### (b) FROSTGATE-CLASS CONVERSION TRAPS — short transit, park-prone

The frostgate mechanism, restated from the autopsy so the geometry criterion is explicit:
the raider **arrives very early** (r9-r14, vs a field median of r12), **holds the socket
longer than on any other map** (448 and 160 socket unit-rounds vs 8-205 elsewhere), and
**converts nothing**. The geometric driver is **short core-to-core transit** — a short
`cpath` buys early arrival, and early arrival with a silenced damage verb buys a long
park. frostgate's `cpath` = **11**.

New-pool maps at or below frostgate's transit, ranked:

1. ⛔ **skald (NEW) — `cpath` 9, 16×16, chain 2, 6.2% walls.** **The shortest transit in
   the pool, shorter than frostgate itself.** Shallow ore means the belt is never the
   bottleneck, so if we lose here it is a conversion loss by elimination.
   GEOMETRY-INFERENCE: **the purest frostgate analogue on the board.**
2. ⛔ **holmgang (NEW) — `cpath` 12, 12×12, chain 2, and only 6 ore tiles.** Smallest
   board; diagonal cores; almost no terrain to hide behind. Same class.
3. ⛔ **helheim (NEW) — `cpath` 13, 18×18, chain 2.** A solid 4×4 wall block sits
   *directly between* the cores with the two `oooo` ore bands hugging it, so both sides'
   economy and both sides' approach share one contested strip.
4. auroraveil (survivor) — `cpath` 17. Already carries the third-crater problem; this is
   a secondary exposure.

⇒ **The rotation traded ONE frostgate-class map for THREE, all of them new, all of them
untested by our line.** GEOMETRY-INFERENCE, and it is the single largest shift in the
table: the pool's transit distribution moved *shorter* at the bottom end.

### (c) MIDGARD-CLASS REFUSAL-BY-CONSTRUCTION

**MEASURED against the LIVE constants — and the commission's premise is superseded.**
`_fs_map_gated` (`siege.py:500-517`) reads its floors at runtime:
```
min_dim = FS_V525_MIN_MAP_DIM if LOKI_FS_V525 else FS_MIN_MAP_DIM
min_dsq = FS_V525_MIN_CORE_DSQ if LOKI_FS_V525 else FS_MIN_CORE_DSQ
```
and **`LOKI_FS_V525 = True` in the shipped tree** (`doctrine.py:4808`). ⇒ the live floors
are **`FS_V525_MIN_MAP_DIM = 10`** and **`FS_V525_MIN_CORE_DSQ = 32`**
(`doctrine.py:4818-4819`, both annotated "fjordgate's own"). **`FS_MIN_CORE_DSQ = 72` /
`FS_MIN_MAP_DIM = 12` (`doctrine.py:2347-2348`) are the v510-era values, live only if
`LOKI_FS_V525` were flipped off.**

**THE REFUSAL LIST, driving the shipped predicate over all 30 pool cells:**

| gate | threshold (live) | new-pool maps failing it |
|---|---|---|
| larger side < min_dim | **< 10** | **NONE** (smallest larger-side is holmgang's 12) |
| core dsq < min_dsq | **< 32** | **NONE** (smallest is holmgang's 128) |
| `FS_MAP_SKIP` (grid-confirmed) | 5 signatures | **NONE** — see §4, jotunheim is a *false* hit that MAPTRUST rejects |
| `FS_V525_CRIPPLE_MAPS` (grid-confirmed) | midgard sig | **midgard** |

⇒ **REFUSAL-BY-CONSTRUCTION LIST: `{midgard}`, both seats, 2/30 cells = 6.67%.**

⛔ **`holmgang` — the commission's obvious candidate — DOES NOT REFUSE, and would not
refuse under the old thresholds either.** MEASURED: larger side **12 ≥ 12** (old) and
**≥ 10** (live); core dsq **128 ≥ 72** (old) and **≥ 32** (live). It clears both floors on
both threshold sets with room. The 12×12 board is small, but the cores sit **diagonally**
at (1,1)/(9,9), which puts dsq at 128 — four times the live floor. **The intuition that a
12×12 map trips the small-map gate is wrong by a factor of four on the binding term.**

### (d) Not a risk, worth naming: **stavkirke's `corridor = 1`**

The only single-tile pinch on a shortest core-to-core path in the pool (layer 3 of 19,
nested-ring fortress). GEOMETRY-INFERENCE: a one-tile isthmus is a **launcher-ferry
opportunity** (the throw is `1 ≤ d² ≤ 26`, terrain-blind on the arc) and simultaneously a
**barrier-seal opportunity for THEM**. It is the map where a single body in the wrong
place decides the transit. Unmeasured; flagged for a probe, not asserted.

---

## 4. ⭐⭐ THE SURPRISE — WRITTEN BEFORE EXPLAINING IT

**`jotunheim` is 24×24 with cores at (4,4) and (18,18). So is `saga`. The signature
`(24, 24, (4, 4), (18, 18))` is a verbatim member of `FS_MAP_SKIP` (`doctrine.py:2368`,
comment `# saga`) — and `saga` is a map the closure survey put on the skip list because
its ring does not close.**

**MEASURED, both verdicts produced by the same unmodified instrument:**

```
gatemap_rot.py, jotunheim, seats 0 and 1:
  _v529merge      REFUSE / REFUSE     POOL REFUSING MAPS (2 of 15): jotunheim, midgard
  _v533home       REFUSE / REFUSE     POOL REFUSING MAPS (2 of 15): jotunheim, midgard
  _v536trustport  RUN    / RUN        POOL REFUSING MAPS (1 of 15): midgard
  _v537socket     RUN    / RUN        POOL REFUSING MAPS (1 of 15): midgard
```

**And it is a DOUBLE hit, not a single one.** Driving `known_map_for` directly over all
15 pool maps × 2 seats:

```
_v529merge   (pre-MAPTRUST):  jotunheim -> GRID, CORRECT=False   (both seats)
                              auroraveil/glacierkeep/icefloe/midgard/valkyrie -> GRID, CORRECT=True
_v537socket  (MAPTRUST F1):   jotunheim -> None                  (both seats)
                              the same five survivors -> GRID, CORRECT=True
```

⇒ **On a pre-MAPTRUST tree, jotunheim would have (F1) silently adopted SAGA'S TILE GRID
as its map memory — wrong walls, wrong ore, wrong pathing, cached, for the whole match —
AND (F2) refused ferry-siege outright on saga's skip entry.** Both defects, on the same
map, from the same collision.

**`tools/AUDIT-map-hardcoding-2026-08-20.md` named exactly these two hazards
(F1 singleton short-circuit, F2 un-grid-confirmed skip) on 2026-08-20. `v534maptrust`
shipped the fixes at 10:32Z the same day. The rotation that made the collision real
landed ~21 hours later.** The fix beat the hazard by under a day, and nobody knew the
hazard was going to be drawn.

Two further notes on the same mechanism, both MEASURED:
* **jotunheim is the ONLY one of the ten new maps with any `MAP_CODES` entry at all**,
  and that entry is wrong (it is saga's). The other nine return `None` and run on the
  live-sensing fallbacks — the GENPOOL regime the builder's 08:00 note describes.
* **Two more new-pool maps share signatures with maps we hold locally but that are not in
  MAP_CODES**, so they are currently harmless and will become live hazards the moment
  anyone adds an entry at those keys: **holmgang ≡ `inv_small12` (12,12,(1,1),(9,9))** and
  **yggdrasil ≡ `inv_large30` (30,30,(3,3),(25,25))**. Both invented maps.
  **`maps/invented/` is the GENPOOL out-of-pool fixture** — so any future decision to
  catalogue invented maps would inject two false-match cells into the live pool. Worth a
  one-line rule; not a defect today.

**Second, smaller surprise:** **midgard's signature is shared with ragnarok**
(`(30,30,(2,2),(26,26))`, and the doctrine comment says so), and **ragnarok has now
rotated out**. The v524 exact-grid disambiguation that existed to separate them is,
as of this morning, **guarding a collision that no longer has a second member.** Not a
defect — but if `#103` ever concludes "stop refusing midgard", the disambiguation goes
with it and nothing in the pool notices.

---

## 5. Q4 — EARLY TAPE (EYEBALL, n IS TINY, LABELLED AS SUCH)

### 5.1 The rotation boundary, read off pairing times

`corpus/ladder_games.tsv` is **STALE for this question** — its newest row is the
07:12:59Z match, before the rotation. Read live from `fcode match info --json`:

| pairing (createdAt) | match | maps drawn | pool |
|---|---|---|---|
| **07:12:59Z** | 097976e0 (team lazy) | royale, nordkap, auroraveil, ragnarok, drumlin | **OLD** |
| **07:32:59Z** | 450821bb (Erebus) | yulerune, glacierkeep, drumlin, archipelago, auroraveil | **OLD** |
| **07:52:59Z** | 9cb7d218 (farming_200s) | yggdrasil, icefloe, longhouse, auroraveil, fimbulwinter | **NEW** |
| **08:12:59Z** | 9e18ed98 (gsxWins) | helheim, jotunheim, midgard, yggdrasil, auroraveil | **NEW** |

⇒ **MEASURED: the pool rotated between the 07:32:59Z and 07:52:59Z pairings** — i.e.
inside one 20-minute pairing gap, roughly **20-25 minutes before the 08:00:36Z announce**.
Anyone dating the rotation to 08:00 will mis-classify the 07:52 match.

### 5.2 Every new-pool game on the tape so far (n = 10 games, 2 matches)

**OUR LINE (`ourver = 174`, `_v537socket`) — ONE match, 1-4 vs farming_200s (v19):**

| map | result | cond | round |
|---|---|---|---|
| yggdrasil | loss | core_destroyed | r127 |
| icefloe | loss | core_destroyed | r185 |
| **longhouse** | **WIN** | core_destroyed | **r106** | ← Magnus's marker, "executed really well"
| auroraveil | loss | core_destroyed | r289 |
| fimbulwinter | loss | core_destroyed | r137 |

**TEAMMATE'S LINE (`ourver = 175`, x3r0's carrier) — 3-2 vs gsxWins.** Not our bytes;
listed because it is the only other new-pool tape in existence:

| map | result | cond | round |
|---|---|---|---|
| helheim | WIN | core_destroyed | r86 |
| **jotunheim** | WIN | core_destroyed | **r398** |
| **midgard** | **loss** | core_destroyed | r520 |
| yggdrasil | WIN | core_destroyed | r187 |
| auroraveil | loss | core_destroyed | r339 |

**EYEBALL observations at n=10 — none of these is a finding, all are hypotheses:**
* **10 of 10 new-pool games ended `core_destroyed`. Zero r1000s.** The two matches
  immediately *before* the rotation contained two `titanium_collected` r1000 games
  (auroraveil vs team lazy, yulerune vs kladde). ⚠ Confounded with opponent and with
  auroraveil's own history; at n=10 this is a coin that came up heads ten times on a
  fixture we have not characterised.
* **jotunheim's first-ever appearance went r398 — the second-slowest of the ten.**
  Consistent with the deep-ore/late-belt geometry, on a tree (v175) that is not ours and
  whose socket behaviour I have not audited. **Do not read this as confirmation.**
* **midgard appeared in a *teammate's* match and was LOST at r520.** Our line refuses on
  midgard by construction (§2.3) — v175's posture there is unknown to me and is not
  evidence about `#103` either way.
* **auroraveil appeared in BOTH new-pool matches and was lost in both** (r289, r339), and
  in the two pre-rotation matches as well (r1000, and a v174 win at r367). It is drawn
  very often. **It is simultaneously `#101`'s only surviving BAD map, the crater study's
  falsifier cell, and a frostgate-adjacent short-transit board — and it is the highest-
  frequency map on the early tape. If one map deserves the first post-rotation probe on
  frequency alone, it is auroraveil.**
* **longhouse, the one win: `cpath` 35, the second-longest transit in the pool, and a
  walled central corridor.** r106 is fast for that transit. Untested hypothesis worth one
  line: the long walled approach may be *protecting* our raider rather than delaying it.

**POWER.** n=10 games, 5 of them ours, 1 match each. `DEFF` for platform games is
1.529 pooled / 1.366 within-opponent (rated); at n=5 within one match the effective n is
**~3.3**. **No bar, no verdict, no share is computable here and none is offered.**

---

## 6. WHAT A SUCCESSOR SHOULD DO WITH THIS

1. **`#101` is 3-of-11 alive.** Its Elo pricing must be re-derived on new-pool tape before
   the row is cited. The surviving regression cell is `midgard / seat A`.
2. **Gate 2 of the socket plank needs jotunheim in place of drakkarfjord.** Same cap6
   class, same chain, and it turns an archive fixture into an in-pool one.
3. **jotunheim is the highest-value single new-map probe** — deep-ore crater class, never
   measured by us, and the map where MAPTRUST is doing invisible work.
4. **skald / holmgang / helheim are the frostgate-class replacements.** The conversion
   defect (`AUTOPSY-v174-losses`: arrives, parks, never swings) has no in-pool exhibit
   any more; if it is still live, it will show up on those three. **Re-site the exhibit
   before the finding goes stale.**
5. **`#103` (midgard) survives intact and is now 1 of 15 refusing cells with no
   archipelago beside it.** The gate is `FS_V525_CRIPPLE_MAPS`, grid-confirmed, and its
   signature partner ragnarok has left the pool.
6. **Correct the boot-level premise**: the live ferry floors are **10 / 32**, not 12 / 72.
   `FS_MIN_CORE_DSQ = 72` / `FS_MIN_MAP_DIM = 12` at `doctrine.py:2347-2348` are dead
   constants behind `LOKI_FS_V525 = True`, and a reader who greps for them gets the
   wrong answer. Live values: `doctrine.py:4818-4819`.
8. **`cap6` is a HOME-PACKAGE constant, not a live one.** `_v533home`/`_v534maptrust`
   ship `V530_MOUTH_MAX_LINKS = 6`; `_v537socket` ships no mouth. If the home package is
   ever merged forward, the deep-ore column in §1 is the list of maps where its mouth
   would refuse to arm: jotunheim, glacierkeep, auroraveil.
7. **Verify the remaining 7 pool maps' bytes against platform hashes** as they get drawn
   (8 of 15 confirmed sha256-identical today).
