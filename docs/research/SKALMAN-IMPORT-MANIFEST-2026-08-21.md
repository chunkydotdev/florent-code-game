# SKALMAN IMPORT MANIFEST — the six curated verbatim lifts from `bots/_v542wave`

**Scope:** the six ratified infrastructure imports from the frozen benchmark tree
`bots/_v542wave/` into the new-from-scratch `bots/_v600skalman1/` *(tree renamed s54 for
LINE_DIRS conformance; this manifest's original draft said `_skalman_v1`)*.
**Read-only analysis; no file in the repo was modified.** Every line anchor below was read
in this session; function line ranges are AST-derived (`ast.FunctionDef.lineno/end_lineno`),
not eyeballed.

**Tree layout as found** (the task brief's five files are correct):

| file | lines | role |
|---|---|---|
| `doctrine.py` | 6,080 | constants only — no classes; 3 module functions (`fs_crew_on`, `fs_crew_seat`, `fs_muster_wait`) |
| `eco.py` | 2,708 | module-level map/geometry helpers (L82–437) + `class EcoMixin` (L440–end), 51 methods |
| `main.py` | 2,576 | `class Player(EcoMixin, RaidMixin, SiegeMixin)`, 26 methods |
| `raid.py` | 1,454 | `class RaidMixin`, 22 methods — **the retiring rush/two-raider line** |
| `siege.py` | 6,778 | `class SiegeMixin`, 161 methods — the ferry-siege / FS_* line |

Import graph: `doctrine` ← `eco` ← {`raid`, `siege`} ← `main`. `doctrine.py` imports nothing
from the tree; `eco.py` does `from doctrine import *`; `raid.py`/`siege.py` do
`from doctrine import *` **plus** named imports from `eco`; `main.py` imports all four.
⇒ **`doctrine.py` + the module-level half of `eco.py` is the only acyclic, raid-free layer.**

---

## VERDICT SUMMARY

| # | item | primary location | size (lines) | verdict |
|---|---|---|---|---|
| 1 | MAPTRUST / `known_map_for` (F1 + F2) | `eco.py:82–234` + `doctrine.py:1078–1172, 5386–5409` | 138 code + 95 data | **CLEAN-LIFT** (F1) / **NEEDS-CUT** (F2 — siege-only) |
| 2 | bounds discipline | *no module — an idiom, 71 sites* | n/a | **REWRITE-ADVISED** (write the helper the tree never had) |
| 3 | displacement guards | `raid.py:205–225` + `doctrine.py:1486` | 21 | **NEEDS-CUT** (~7 generic lines inside a raid method) |
| 4 | exception wrapper | `main.py:396–418` (+ `eco.py:444–464`) | 22 (+21) | **CLEAN-LIFT** |
| 5 | store idioms | `doctrine.py:931–961, 1184–1188, 2321–2339, 2792–2805, 3354–3356, 3462–3478` | ~90 (convention, not code) | **REWRITE-ADVISED** (conventions lift; the allocation must not) |
| 6 | cardinal pathing | `eco.py:2074–2335` + `902–930` + `247–299` | 194 + 13 + 51 + 28 + 25 | **NEEDS-CUT** (dead pave block; one raid-free rewrite point) |

---

## 0. ENTRY-POINT STRUCTURE (what SKALMAN must reproduce or replace)

### 0.1 Dispatch

```
main.py:396-407   Player.run(ct)        — the blanket try/except (item 4)
main.py:409-418   Player._dispatch(ct)  — the entity-type switch
```

`_dispatch` is a flat 4-way branch on `ct.get_entity_type()`:

| entity type | handler | defined in |
|---|---|---|
| `CORE` | `self._core(ct)` | `main.py:424–1252` (829 lines) |
| `BUILDER_BOT` | `self._builder(ct)` | `main.py:1282–1652` (371 lines) |
| `GUNNER`, `SENTINEL` | `self._turret(ct)` | `main.py:2103–2309` |
| `LAUNCHER` | `self._launcher_turn(ct)` | **`raid.py:1328`** |

⛔ **The dispatch table itself is 10 lines and raid-free; everything it dispatches TO is not.**
`_dispatch`'s launcher arm resolves into `RaidMixin`. Static cross-mixin call analysis of
`main.py`'s method bodies:

* calls into **`raid.py`**: `_bb_ray_clear`, `_launcher_turn`, `_raid` (3)
* calls into **`siege.py`**: 24 methods (`_fs_gate`, `_fs_turn`, `_fs_state`, `_raid_seat_take`,
  `_v517_*`, `_v518_twin_reserve`, `_v520_presence_reserve`, `_v521_core_resolve`,
  `_v522_crew_near`, `_v527_*`, `_v539_famine`, …)
* calls into **`eco.py`**: 13 methods

⇒ **`_core`, `_builder`, `_turret` are REWRITE in full.** Take the 22-line
`run`/`_dispatch` skeleton (item 4) and nothing else from `main.py`'s method bodies.

### 0.2 `__init__` — the per-unit state block

`main.py:65–394` (≈330 lines, **199 `self.*` assignments**). Sectioned by comment banner:
identity/map · movement/targeting · economy · samestop · pave trail · siphon · raid state ·
FS/siege state · report-once latches · LOKI-TURBO caches.

**The minimal subset the six imports actually need (≈20 fields):**

```python
# identity / map            (main.py:67-78)
self.n = 0; self.team = None; self.core = None; self.enemy = None
self.mw = self.mh = 0; self.idx = 0
self.map_grid = None; self.map_walls = set(); self.map_ores = []
# movement / targeting      (main.py:80-84)
self.tgt = None; self.last = None; self.stuck = 0; self.wall = None; self.ang = 0.0
# report-once latches       (main.py:361-363)
self.reported_cpu = False; self.reported_error = False
# nav cache                 (main.py:372-373)
self._nav_key = None; self._nav_tpl = None
# displacement memory       (rename from raid_prev — see item 3)
self.prev_pos = None
```

Everything else in `__init__` is rush/siege doctrine and is dropped.

### 0.3 ⭐⭐ THE CACHING MODEL — AND IT IS THE BIGGEST SURPRISE IN THIS SWEEP

**MODULE-LEVEL STATE IS NOT SHARED BETWEEN UNITS. Every unit gets its own module namespace.**
Engine-probed (`bots/_probe_modglobal`, eider seed 1), banked at
`docs/research/tactics/the-sixteen-ints-really-are-the-only-channel.md` and restated in the
tree at `doctrine.py:2146`:

> *"MODULE STATE IS NOT SHARED BETWEEN UNITS (probe surprise 3): the 16-slot store is the
> only channel and it is buffered one round."*

The probe carries its own positive control: a module counter reads `BOX_n = 4,3,2,1` for
units of decreasing age (**accumulation across ROUNDS within a unit is real**), while the
`TOUCHED` roster shows only self for every unit. Mechanism-consistent: the engine binary
contains `Py_NewInterpreterFromConfig` — one sub-interpreter per unit.

⛔ **THIS CONTRADICTS A COMMENT INSIDE THE TREE ITSELF.** `eco.py:104-107` justifies the
`_GRID_CACHE` memo as *"because up to eleven builders decode the same map in one match."*
That justification is **false** — eleven builders never share `_GRID_CACHE`. The memo is
still worth having (it de-duplicates across the *same* unit's turns and across the up-to-6
candidate grids of one signature), but **SKALMAN must not size or justify any module cache
on a cross-unit sharing assumption.** Flagging this as a live doc defect in the frozen
benchmark.

**Two cache tiers exist and both are per-unit:**

| tier | examples | keyed on | invalidation |
|---|---|---|---|
| module-level dicts | `eco._GRID_CACHE` (L112), `eco._CHAR3` (L108-111), `siege._FS_V534_SKIP_GRIDS` (L75) | `(code, w, h)` / char / signature | never (terrain is static) |
| instance caches | `self._nav_key`/`_nav_tpl`, `_link_tpl_key`/`_link_tpl`, `_pick_key`, `_home_seat_key`, `_launch_key`, … (`main.py:372–390`) | a tuple of things that cannot change mid-match (core anchor, enemy anchor, map dims, seat) | key-compare on every read |

The **instance-cache-with-explicit-key** idiom (`if self._x_key != key: rebuild`) is the
pattern SKALMAN should reproduce; it is what makes the caches safe against the enemy anchor
being refined on first sighting. It is raid-free and costs nothing to adopt.

### 0.4 Two sandbox constraints that bind the whole build

1. **`finally:`, `except BaseException:` and `except SystemExit:` are REJECTED BY THE AST
   VALIDATOR AT LOAD** (probe surprise 2, `PROBE-DOSSIER-ferry-siege-2026-08-17.md:197-198`;
   restated `doctrine.py:2142-2144`, `siege.py:44-47`). Verified: **zero real `finally:`
   blocks exist in the whole tree** — all 3 grep hits are inside comments. SKALMAN's
   exception wrapper therefore *cannot* be written with `finally` or a `BaseException`
   re-raise, and does not need one (see item 4).
2. **No code after `self_destruct()`** — it never returns and raises nothing catchable.

---

## 1. MAPTRUST / `known_map_for` — F1 terrain-verify + F2 grid-confirm

### 1.1 Location

| what | file:lines | size |
|---|---|---|
| `enemy_core_for(w, h, own)` | `eco.py:82–97` | 16 |
| `_CHAR3` base-27 expansion table | `eco.py:108–111` | 4 |
| `_GRID_CACHE` | `eco.py:112` | 1 |
| `_decode_grid(code, w, h)` | `eco.py:115–122` | 8 |
| **the "deliberately no memo" doctrine comment** | `eco.py:125–145` | 21 (import it — see risk note) |
| **`_maptrust_pick(candidates, w, h, own, ct)` — F1** | **`eco.py:147–211`** | **65** |
| `known_map_for(w, h, own, ct=None)` | `eco.py:214–234` | 21 |
| **F2 (`FS_MAP_SKIP` confirm) — lazy decode** | `siege.py:66–86` | 21 |
| F2 consumer | `siege.py:772–791` | 20 |

**Call sites in the benchmark (3):** `main.py:432-433` (Core), `main.py:1395-1415` (builder,
plus the `str.find` walls/ores extraction), `siege.py:779-781` (F2, never caches).

### 1.2 Dependency closure

**From `doctrine.py` (data, ~95 lines — verified by AST name-resolution over the block):**

```
CORE_PAIRS         doctrine.py:1081–1105   32 map-dimension/anchor tuples
MAP_ALPHABET       doctrine.py:1109        "ABCDEFGHIJKLMNOPQRSTUVWXYZ0"
MAP_CODES          doctrine.py:1110–1141   24 base-27 packed terrain strings
EXTRA_MAP_CODES    doctrine.py:1142–1172   the collision-pair list (same dims+anchors)
FS_V534_MAPTRUST   doctrine.py:5386        master flag, True
FS_V534_LOG        doctrine.py:5387        False
FS_V534_MIN_TILES  doctrine.py:5388        8 — floor below which adoption is refused
```

**F2 only (SIEGE-ENTANGLED, see cut line):**
```
FS_MAP_SKIP_ON     doctrine.py:2365
FS_MAP_SKIP        doctrine.py:2366–2372   5 coarse signatures
FS_V534_*_CODE     doctrine.py:5396–5401   6 terrain strings
FS_V534_SKIP_CODES doctrine.py:5403–5409   signature → grids
```

**From the engine API:** `get_nearby_tiles`, `get_tile_env`, `get_tile_building_id`,
`Environment.WALL/ORE_TITANIUM`, `Position`.
**Instance state:** `self.map_grid`, `self.map_walls`, `self.map_ores` (written once by the
caller, never by `known_map_for` itself).
**No store slot. No raid/siege import. `_maptrust_pick` and `known_map_for` reference zero
`SLOT_*` names.**

### 1.3 ⛔ CUT LINE

* **F1 (`_maptrust_pick` + `known_map_for` + `_decode_grid` + `enemy_core_for`) is
  CLEAN-LIFT.** Nothing in it touches raid or siege doctrine.
* **F2 is NOT generic.** `_fs_v534_skip_grids` exists to confirm `FS_MAP_SKIP` — the list of
  boards on which the **ferry-siege** plank stands down. SKALMAN has no ferry-siege.
  **Cut at `siege.py:66`** (drop `_FS_V534_SKIP_GRIDS`, `_fs_v534_skip_grids`, `FS_MAP_SKIP*`,
  `FS_V534_*_CODE`, `FS_V534_SKIP_CODES` entirely).
  **What survives from F2 is the PATTERN, not the code:** *a coarse (w,h,anchor) signature hit
  is a CANDIDATE, never a conclusion; confirm against the actual decoded grid; no match ⇒
  treat as an unsurveyed map and run the default.* Re-apply that pattern to any SKALMAN
  per-map gate (e.g. a cage-feasibility or nest-band map list) at the point that gate is
  written.
* **Also cut:** `siege.py:63-65` `FS_V524_CRIPPLE_GRIDS` (the eager-decoded two-grid cripple
  list) — same class, siege-only.

### 1.4 CPU cost

* `_decode_grid`: a dict lookup per code char + one `str.join`, memoised per `(code,w,h)`.
  Cheap. (Its predecessor did `MAP_ALPHABET.index(ch)` per char and a per-cell genexp over
  900 cells on **the first turn of every unit** — that was the measured first-turn spike.)
* `_maptrust_pick`: **the only per-turn-expensive piece, and it is bounded.** One
  `get_nearby_tiles()` (builder r²=20 ⇒ ~69 tiles; Core r²=36 ⇒ ~113), then per tile one
  `get_tile_env` + a list-comprehension filter over the *live candidate* list (≤6, usually 1–2).
  **Exits the moment the candidate set empties** — a non-matching board dies on the first
  disagreeing tile. One extra `get_tile_building_id` per MISMATCH only.
* **It is deliberately NOT memoised** (`eco.py:125-145`) and is re-run every round until the
  caller caches the result. Callers gate on `if self.map_grid is None:`, so in practice it
  runs once per unit — but a unit that never resolves its core pays it every round.
  Headroom is ample: our measured mean is **642–1,123 µs/turn against 10,000**
  (`docs/research/ammo-and-cpu-2026-08-09.md:124`).

### 1.5 Risk note

> **Import `known_map_for` without `_maptrust_pick` and you restore the v123 livelock /
> wrong-grid-adoption class verbatim** — the `FS_V534_MAPTRUST = False` branch at
> `eco.py:223-234` is the *unfixed* parent (singleton adopted with zero terrain checks;
> `>=2` returns the closest stored grid and **never None**), and a silently wrong
> `map_walls`/`map_ores` corrupts pathing for the whole match with no tell.
> **And import the L125-145 comment with it:** it records that the first draft of the fix
> added a memo keyed on `(w, h, anchor)` — *the very key that does not identify a map* —
> which reintroduced the collision bug inside the collision fix. Do not re-derive that.

---

## 2. BOUNDS DISCIPLINE

### 2.1 Location — ⚠ THERE IS NO MODULE. IT IS AN IDIOM.

**The tree ships no `in_bounds()` helper.** Grepped for `def in_bounds|_in_bounds|onmap|_inb`
across all five files: **zero hits.** The rule is instead open-coded at **71 sites**:

| file | explicit `0 <= x < mw` / `>= mw` bound tests |
|---|---|
| `eco.py` | 37 |
| `siege.py` | 22 |
| `raid.py` | 9 |
| `main.py` | 3 |
| `doctrine.py` | 0 (comment only) |

**The canonical instances** (copy these as the reference form):
* `eco.py:172-179` — inside `_maptrust_pick`, with the reason written out.
* `eco.py:2101-2107` — `_bfs_direction`'s off-map-target early return.
* `eco.py:2289-2291` — `_move`'s pre-move bound test.
* `eco.py:912-916` — `_flat_template`: **the padded-border trick, where the blocked
  1-tile border IS the bounds test**, so the inner BFS loop needs no comparison at all.

**The rule as doctrine:** `doctrine.py:2137-2140`, `siege.py:42-43`, `eco.py:174-178`,
`siege.py:900`, `siege.py:1674`, `siege.py:5308`, `siege.py:5692` — all restating the s50
correction: *`is_in_vision()` is a pure radius test with no bounds check;
`is_in_vision((-1,14))` returned **True** on atoll and the next `get_tile_*` raised.*

There are **11 `is_in_vision` call sites** in the tree. Every one of them is either (a) inside
a `try/except`, or (b) preceded by an explicit bound test — never used as the guard itself.

### 2.2 Dependency closure

`self.mw`, `self.mh` (set from `get_map_width()/get_map_height()` on first turn). Nothing else.

### 2.3 ⛔ CUT LINE / verdict: **REWRITE-ADVISED**

Nothing to lift verbatim. **SKALMAN should do the thing `_v542wave` never did: define the
helper once.**

```python
def in_bounds(self, x, y):
    return 0 <= x < self.mw and 0 <= y < self.mh
```

…and make it a build rule that **every** computed position passes through it before any
`get_tile_*` / `is_tile_*` / `can_build_*`. Two supporting rules from the benchmark worth
carrying:
* **prefer the padded-border template** (item 6) where a flood is involved — it removes the
  test from the hot loop entirely rather than making it cheap;
* **bounds BEFORE vision, always** — `is_in_vision` may follow the bound test, never replace it.

### 2.4 Risk note

> Omit the explicit bound test and rely on `is_in_vision` and the unit is **permanently
> destroyed** the first time it plans near a map edge — which is exactly where SKALMAN's cage
> walker and ore denier operate. The s50 probe agent's own probe died through this gate.

---

## 3. DISPLACEMENT GUARDS

### 3.1 Location

**`raid.py:205–225`, inside `RaidMixin._raid()` (method spans `raid.py:166–270`).**
This is the **only** position-jump self-detector in the entire tree — there is no equivalent
on the eco path (`eco.py:_expand`, L2468–2617) and none in `siege.py`. (`siege.py`'s
`self.fs_thrown` is the *launcher's* record of riders it threw, not self-detection.)

```python
212  if self.raid_prev is not None and p.distance_squared(self.raid_prev) > LOKI_TELEPORT_DSQ:
213      if (self.raid_station is not None
215              and p.distance_squared(E) > self.raid_prev.distance_squared(E)):
217          self.raid_ban[(self.raid_station.x, self.raid_station.y)] = rnd + 80
218      self.raid_station = None
219      self.raid_rescan = rnd
220      self.tgt = None
221      self.stuck = 0
222      self.pave_prev = None
223      self.pave_dir = None
224      self.pave_rnd = -2
225  self.raid_prev = p
```

**Second, independent layer for the same hazard:** `eco.py:2296–2306` — `_move` wraps the
`is_in_vision(pave_prev)` / `is_tile_empty(pave_prev)` read in try/except because *"a Launcher
throw can teleport this builder between turns, which puts pave_prev outside vision and makes
is_tile_empty raise."*

### 3.2 Dependency closure

| name | where | keep? |
|---|---|---|
| `LOKI_TELEPORT_DSQ = 4` | `doctrine.py:1486` (block header L1477-1484) | **KEEP** — d²>4 ⇒ moved >2 tiles ⇒ thrown |
| `self.tgt`, `self.stuck` | `main.py:81,83` | **KEEP** — generic nav |
| `self.pave_prev/_dir/_rnd` | `main.py:106-108` | keep only if SKALMAN paves (see item 6) |
| `self.raid_prev` | `main.py:123` | **RENAME** — the memory itself is generic |
| `self.raid_station`, `self.raid_ban`, `self.raid_rescan` | `main.py:119-122` | **CUT** |
| `LOKI_EXILE_PENALTY = 24`, `LOKI_RAID_RESCAN = 6` | `doctrine.py:1485,1489` | **CUT** — station scoring only |
| `E` (enemy anchor), `rnd` | locals of `_raid` | supply from SKALMAN's own context |

### 3.3 ⛔ CUT LINE — verdict **NEEDS-CUT**

Lines 213–219 are the two-raider ring-station model (ban a station covered by a launcher,
force a rescan). **They go with `raid.py`.** The generic residue is ~7 lines:

```python
# displacement guard — a launcher throws any adjacent builder from EITHER team,
# so a jump of more than one step since our last turn proves we were picked up.
if self.prev_pos is not None and p.distance_squared(self.prev_pos) > SK_TELEPORT_DSQ:
    self.tgt = None          # re-plan from actual position
    self.stuck = 0
    self.pave_prev = None; self.pave_dir = None; self.pave_rnd = -2
self.prev_pos = p            # unconditional, every turn
```

**SKALMAN's own version must additionally invalidate whatever per-role plan it caches.** The
benchmark's guard clears the *raid* plan; the analogue for the four Skalman roles is: the cage
walker's lap cursor, the ore denier's target-ore, the siege engineer's nest site. Note the
benchmark **does NOT clear** `self.link_queue` / `self.samestop_*` on a throw — a body thrown
mid-wiring keeps a stale build queue. **That is a latent defect, not a design; do not copy it.**

### 3.4 ⭐ Why the guard is small: routes are never cached

`main.py:184–188`, verbatim:

> *"Nothing holds a Position across rounds for a body that can be THROWN — the raider re-reads
> get_position() every turn (probe P2's stale-position hazard)."*

`_bfs_direction` reads `ct.get_position()` fresh every call and caches only the *target tile*
(`self.tgt`), never a route. **So "re-plan from actual position" is automatic and free.** The
guard's real job is invalidating *choices* (which station / which tile) and *trail bookkeeping*,
not recomputing a path. **SKALMAN must preserve that property**: if it caches a route or a
step list, the 7-line guard is no longer sufficient.

### 3.5 Risk note

> Import the guard without the **no-cached-routes** discipline (§3.4) and it under-covers: it
> clears a target but not a stale step list. Import the no-cached-routes discipline without the
> guard and a thrown body walks straight back into the same launcher.

---

## 4. THE EXCEPTION WRAPPER

### 4.1 Location — `main.py:396–407` (12 lines with comment, 9 of code)

```python
396  def run(self, ct):
397      # An exception escaping run() makes the engine PERMANENTLY delete this
398      # unit for the rest of the match.  Catching it costs one round's
399      # action instead; there is no situation where propagating is better.
400      try:
401          self._dispatch(ct)
402      except Exception:
403          if not self.reported_error:
404              self.reported_error = True
405              import sys
406              import traceback
407              traceback.print_exc(file=sys.stderr)
```

* Catches **bare `Exception`**, never `BaseException`. `SystemExit`/`KeyboardInterrupt` derive
  from `BaseException` and propagate automatically — **no explicit re-raise is needed, and no
  explicit re-raise is POSSIBLE**: `except BaseException` and `except SystemExit` are rejected
  by the sandbox AST validator at load (§0.4).
* **Exactly one layer.** There is no per-subsystem sibling wrapper. The dozens of small local
  `try/except Exception` blocks throughout the tree are per-call defensive guards (an entity
  dying mid-scan, a debug print, `is_in_vision` raising) — they keep the *round's action*
  alive; `run()`'s wrapper is the only thing between an uncaught exception and permanent
  deletion.
* **Report-once latch**: `self.reported_error` (`main.py:363`) — *"one report per unit
  lifetime, so a bug cannot flood stderr."* No `FS_*_LOG` flag gates it.
* **Mutates nothing else.** It does not mark the unit degraded; the unit loses one round's
  action and resumes next round with all state intact.

### 4.2 The companion CPU guard — `EcoMixin._cpu_exhausted`, `eco.py:444–464` (21 lines)

```
CPU_BUDGET_US = 8000        doctrine.py:1076   (rationale L1065–1075)
self.reported_cpu = False   main.py:362
```
Wraps `get_cpu_time_elapsed()` in its own inner try/except (`eco.py:451-455`) — the call can
itself raise. Called as a bail-out checkpoint at 11 sites inside long scans: `eco.py:1097`
(BFS), `1449`, `1593`, `2205`, `2581`; `main.py:1509`, `1906`; `raid.py:232`, `796`, `1011`.
⚠ **`get_cpu_time_elapsed()` reads 0 under local `fcode run`, even with `--tle`
(`doctrine.py:1072-1074`) — this guard is a NO-OP in every local arena run.** It is therefore
an instrument that has never produced the other verdict locally; treat any local screen as
un-CPU-tested.

### 4.3 Dependency closure — verdict **CLEAN-LIFT**

`self.reported_error` (init `False`); `sys` + `traceback` imported inline inside the handler,
so **no module-level import is required**. Optional companion: `CPU_BUDGET_US`,
`self.reported_cpu`, the `_cpu_exhausted` body. **Zero raid/siege entanglement** — `run`,
`_dispatch` and `_cpu_exhausted` reference no doctrine constant beyond `CPU_BUDGET_US`
(AST-verified: `run`/`_dispatch` resolve to **zero** `doctrine.py` names).

### 4.4 Risk note

> Import the wrapper without the CPU guard and a heavy turn is truncated **mid-statement at a
> boundary the engine picks, with no cleanup**, leaving instance state half-updated — the guard
> exists so the file picks the boundary instead. Import the wrapper and then write
> `except BaseException` or a `finally:` anywhere and **the bot does not load at all.**

---

## 5. STORE IDIOMS — the 16-slot map

### 5.1 ⛔ ALL SIXTEEN SLOTS ARE OCCUPIED IN `_v542wave`. FIVE ARE BIT-PACKED WITH UP TO FIVE
### SUB-FIELDS. **SKALMAN MUST NOT INHERIT THIS ALLOCATION.**

Three generations of names sit on the same 16 indices (base `_v103split` → LOKI-1 raid →
LOKI-FERRY-SIEGE `FS_*`), aliased rather than renamed:
`SLOT_DROPPED`≡`SLOT_FWD_GUN`=8 · `SLOT_LAUNCH_ID`≡`SLOT_FERRY_ID`≡`FS_SUPP_SLOT`=10 ·
`SLOT_LAUNCHED_ID`≡`SLOT_RAID_N`≡`FS_CREW_SLOT`=12 · `SLOT_DEFEND_BEAT`≡`SLOT_BELTBREAK`=13 ·
`SLOT_SIEGE`≡`SLOT_RAID_LIVE`≡`SLOT_FS`=15 · `SLOT_ROLE_N`≡`SLOT_SENT_BEAT`=0.

| # | benchmark name(s) | encoding | meaning | line-of-origin |
|---|---|---|---|---|
| 0 | `SLOT_ROLE_N` / `SLOT_SENT_BEAT` | **packed ×5**: b0-9 role counter (`FS_ROLE_N_MASK=0x3FF`) · b10-20 sentinel beat rnd+1 · b21-24 v517 PEER · b25-28 v517 VERDICT · b29-31 NETCODE | builder spawn-order seat + forward-sentinel liveness | `doctrine.py:931`, `3354-3356`, `3483-3487` |
| 1 | `SLOT_UNDER` | flag 0/1 | 50-round "core under attack" latch | `:932` |
| 2 | `SLOT_ATK_RND` | raw round | round of last threat detection (feeds the latch) | `:933` |
| 3 | `SLOT_ENEMY_CORE` | `pack_pos`, 0=unset | enemy core anchor | `:934` |
| 4 | `SLOT_HARVESTERS` | monotone ratchet | team harvester count (high-water) | `:935` |
| 5 | `SLOT_ECO_READY` / `FS_ECO_SLOT` | **packed ×5**: b0 conn · b1 deliv · b2-12 latch rnd+1 · b13-17 harv count · b18 famine · b19-29 famine rnd+1 | Core-only eco-gate word | `:936`, `2915`, `5763-5765` |
| 6 | `SLOT_LAUNCHER` | flag 0/1 | home launcher exists | `:937` |
| 7 | `SLOT_HOME_GUN` | monotone counter | home turrets ever built | `:938` |
| 8 | `SLOT_DROPPED` → `SLOT_FWD_GUN` | monotone counter ("ghost magazine") | forward sentinels ever bought | `:939`, `1184` |
| 9 | `SLOT_HEAL_BUDGET` | scalar Ti | Core damage / heal-budget beacon | `:949` |
| 10 | `SLOT_LAUNCH_ID` → `SLOT_FERRY_ID` / `FS_SUPP_SLOT` | id+1, **or** the full FS word (crew-on) | ferry hop request | `:950`, `1185`, `3010` |
| 11 | `SLOT_LAUNCH_RND` → `SLOT_FERRY_RND` | raw round | round the slot-10 request was written | `:951`, `1186` |
| 12 | `SLOT_LAUNCHED_ID` → `SLOT_RAID_N` / `FS_CREW_SLOT` | **packed ×3**: b0-7 seat counter (`FS_RAIDN_MASK`) · b8-18 sealer beat · b19-29 support beat (**dead** in shipped config) | raider seats issued | `:952`, `1187`, `2806-2808` |
| 13 | `SLOT_DEFEND_BEAT` → `SLOT_BELTBREAK` | rnd+1 heartbeat, self-staling, **non-monotone** | last round a beltbreak gun had a target | `:953-959`, `1464` |
| 14 | `SLOT_THREAT` | `pack_pos` | last threat position near home | `:960` |
| 15 | `SLOT_SIEGE` → `SLOT_RAID_LIVE` / `SLOT_FS` | **packed ×4**: b0-10 beat rnd+1 (`FS_BEAT_MASK=0x7FF`) · b11-13 phase · b14-29 raider id+1 · b30-31 v520 ARC | "a raider is established at the enemy ring" — the most overloaded slot | `:961`, `1188`, `2321-2339` |

**Free slots: NONE.** Nearest to free are fields dead *under current flags*: slot 12 b19-29
(support beat relocated to slot 10), and everything behind `FS_CREW_ON = False`
(`doctrine.py:2741`).

### 5.2 Which slots are rush/raid-line vs generic

* **RAID-LINE (retire with `raid.py`):** 8, 10, 11, 12, 13, 15.
* **SIEGE-LINE (retire with `siege.py`):** 0 upper bits (b10-31), 5, 8 (partly), 10-as-`FS_SUPP_SLOT`, 12 crew beats, 15 phase/rid/arc.
* **GENERIC infrastructure:** 1, 2, 3, 4, 6, 7, 9, 14 — and of these, **3 (`SLOT_ENEMY_CORE`)
  and 4 (`SLOT_HARVESTERS`) are read by all five files**: they are shared world-state inputs,
  not owned by either line.

⇒ **The only slot convention SKALMAN should carry over unchanged is slot 3 =
`pack_pos(enemy_core)`**, because `known_map_for`/`enemy_core_for` (item 1) and the whole map
layer are written against it. Everything else is a fresh allocation.

### 5.3 The idioms worth lifting (this is the real deliverable of item 5)

1. **`pack_pos` / `unpack_pos`** — `eco.py:237–244`, 6 lines. `((x+1)<<16) | (y+1)`; unpack
   returns `None` for 0, so **0 unambiguously means "unset"**. CLEAN-LIFT.
2. **⛔⛔ A SLOT IS AN UNSIGNED 32-BIT INT AND `write_store` RAISES `OverflowError` — NOT
   `GameError` — ON A NEGATIVE OR OVERSIZED VALUE.** Engine-probed twice, independently, with
   positive controls in both tapes (`doctrine.py:2792-2805` and `3462-3471`;
   `bots/_probe_oov_surface`): `2**32-1` round-trips exactly; `2**32`, `2**40`, `2**62`,
   `2**63-1`, `-1`, `-5`, `-2**31`, `-2**63` all raise. **A handler narrowed to `GameError`
   will not catch it, and an escaping exception destroys the unit permanently.** Every packed
   field must be masked before composition.
   Also: `read_store(16)`/`write_store(16,…)` raise `GameError: store index 16 out of range
   (0..16)` — **the engine's own message is off-by-one; the usable range is 0..15.**
3. **ONE WRITER PER SLOT.** Writes are buffered one round, so two writers in the same round is
   a silent lost update. This has bitten the tree **twice, live**: the "r197 lost-update class,
   confirmed COLLISION:True at the s51 06:24Z pre-flight" (`raid.py:1314`, `doctrine.py:3310`)
   — a module-level *derived default* re-evaluated at import gave slot 10 two writers. The
   tree's answers: (a) give each writer its own slot (slot 10 vs slot 15 for the two ferry
   bodies), (b) **evaluate flags at the READ SITE, never at module scope**
   (`raid.py:1306-1326`).
4. **BITFIELD READ-MODIFY-WRITE that preserves the other field** — `main.py:1294-1298`:
   ```python
   n = ct.read_store(S) & MASK
   ct.write_store(S, (ct.read_store(S) & ~MASK) | ((n + 1) & MASK))
   ```
   Both writers preserve each other's field; the only loss is two writes in the same round.
5. **ABSOLUTE ROUND NUMBERS, NEVER MODULAR** — beats are stored as `round + 1` in ≥11 bits
   (`MAX_TURNS = 1000 < 2047`), so 0 unambiguously means "never beaten" and **there is no
   modular-wrap window in which a dead body reads as alive** (`doctrine.py:2803-2805`). A 6-
   or 8-bit beat would reintroduce that failure mode.
6. **Staleness has to be explicit** — `FS_SENT_BEAT_STALE = 3` (`doctrine.py:3357-3361`): a
   live unit runs every round and the store lags exactly one, so a live beat is never older
   than 1; 3 gives two rounds of slack for a CPU-timeout turn.
7. **The blackboard is a one-round BUS, not a memory** (`docs/research/tactics/
   the-blackboard-is-a-one-tick-bus-not-a-memory.md`): prefer facts every unit can
   **re-derive locally** (map symmetry ⇒ enemy anchor) over facts that must be
   **communicated**; only the *elimination* result needs a bit. This is the design rule that
   makes 16 ints sufficient, and it is why item 1 (MAPTRUST) is the load-bearing import.

### 5.4 CPU cost

`read_store`/`write_store` are O(1) engine calls. The only cost pattern worth noting is the
RMW idiom's **two** `read_store` calls per write (`main.py:1297`) — negligible, but note the
second read returns the *pre-write* value, which is what makes the preservation correct.

### 5.5 Verdict **REWRITE-ADVISED** + risk note

> **The conventions (§5.3) lift; the allocation (§5.1) must not.** Import a `SLOT_*` name from
> `doctrine.py` and you inherit an index whose meaning is defined by a plank SKALMAN does not
> ship — and because *all sixteen are occupied*, there is no free index to fall back to. Write
> a fresh `SK_SLOT_*` block with a one-writer-per-slot table, keep slot 3 = `pack_pos(enemy
> core)` for the map layer, and budget slots against the seven `SK_*` verb flags up front:
> **the benchmark ran out of slots and started aliasing, and that aliasing is the origin of
> both live lost-update incidents.**

---

## 6. CARDINAL PATHING

### 6.1 Location

| what | file:lines | size |
|---|---|---|
| `EcoMixin._flat_template(blocked_xy)` | `eco.py:902–917` | 16 |
| `EcoMixin._nav_template()` | `eco.py:919–930` | 12 |
| **`EcoMixin._bfs_direction(ct, target)`** | **`eco.py:2074–2267`** | **194** |
| `EcoMixin._nav(ct, pave=True)` | `eco.py:2271–2283` | 13 |
| `EcoMixin._move(ct, d, pave=True)` | `eco.py:2285–2335` | 51 (**~10 live** — see cut) |
| `nearest_cardinal(d)` | `eco.py:247–254` | 8 |
| `ring`, `core_tiles`, `core_tiles_xy`, `adjacent_to_core`, `dist_core` | `eco.py:257–325` | 47 |
| (only if trunk chains are wanted) `_link_template`, `_link_goals` | `eco.py:932–989` | 57 |

**Design (worth reproducing, not just copying):** `_bfs_direction` returns **one exact step**,
not a route — see §3.4. It is a padded-flat-`bytearray` BFS: `w2 = mw + 2`, neighbour =
`idx ± 1` / `idx ± w2`, and **the blocked 1-tile border IS the bounds test**, so no comparison
runs in the inner loop. One byte encodes three states (0 free / 1 blocked-or-seen / 2 goal).
Two passes: pass 0 treats builder bodies (both teams) as blocked, pass 1 retries body-free if
pass 0 found no goal — **both charged to ONE node budget**.

### 6.2 Dependency closure

**`doctrine.py` (AST-verified over `eco.py:2074–2335`):**
```
CARDINALS         doctrine.py:26     [N, E, S, W]  — the movement alphabet
DELTA             doctrine.py:1912   {d: d.delta() for d in Direction}
CARD_DELTAS       doctrine.py:1913
CARD_OPPOSITE     doctrine.py:1915   (2, 3, 0, 1)
NAV_NODE_BUDGET   doctrine.py:1916   4096
PAVE_TRAIL_ON     doctrine.py:528    ⛔ False — see cut line
SLOT_HARVESTERS   doctrine.py:935    ⛔ pave block only — see cut line
CPU_BUDGET_US     doctrine.py:1076   via _cpu_exhausted
```
**`eco.py` module helpers:** `BFS_BLOCKING_TYPES` (L59-63), `core_tiles_xy` (L291-299);
pave block only: `pave_blocked` (L430-433), `pave_blocked_by_ore` (L421-427), `dist_core`
(L302-325), `nearest_core_tile` (L352-363), `nearest_cardinal` (L247-254).
**Instance state:** `self.map_grid`, `self.map_walls`, `self.mw/mh`, `self.core`, `self.enemy`,
`self.idx`, `self.tgt`, `self.stuck`, `self._nav_key`, `self._nav_tpl`, `self.reported_cpu`;
pave block only: `self.pave_prev/_dir/_rnd`.
**Methods:** `_cpu_exhausted` (item 4), `_flat_template`, `_nav_template`, `_eco_spendable`
(pave block only, `eco.py:466–534` — 69 lines, and itself a whole economy-reserve subsystem).

### 6.3 ⛔ CUT LINE — verdict **NEEDS-CUT**

1. **⭐ `PAVE_TRAIL_ON = False` in the shipped build** (`doctrine.py:528`, rationale L520-527:
   *"38 conveyors is not funding a kill at r32"*). **Both `if PAVE_TRAIL_ON:` blocks in `_move`
   (`eco.py:2292–2329` and `2330–2333`) are DEAD CODE in `_v542wave`.** Cut them and `_move`
   drops **51 → ~10 lines**, and the closure loses `_eco_spendable`, `pave_blocked`,
   `dist_core`, `nearest_core_tile`, `nearest_cardinal`, `SLOT_HARVESTERS` and the three
   `pave_*` instance fields. ⚠ Do **not** cut them silently if SKALMAN's belt verb wants
   trail-paving — but note the flag is off because it was measured off-programme, and
   SKALMAN's belt is *planned globally* (design §2.2), which is the opposite architecture.
   **Recommendation: cut, and build the belt from the global planner.**
2. **`_bfs_direction`'s `self.idx & 1` mirror (`eco.py:2147`)** — the seat-parity tie-break exists so
   two raiders spread rather than trail each other. It is a *raid* behaviour riding on a
   generic field. Keep the mechanism (it is one line and it is good), but re-key it on
   SKALMAN's role index rather than on `idx`, or the four fixed roles inherit an arbitrary
   split.
3. **`_nav_template()` blocks BOTH core footprints** (L923-928). Correct for a raider walking
   *to* the enemy ring, wrong for a cage walker that must path *around* the enemy core
   footprint at d²14-32. Re-check this against the cage lap before lifting.
4. `_link_template` / `_link_goals` / `_link_path` are the trunk-chain (belt) planner, not
   pathing. They are per-harvester by construction — **exactly the #78 defect the design doc
   §2.2 says to replace with a global plan.** Do not import them.

### 6.4 CPU cost

* `_nav_template()` — rebuilt only when `(core, enemy, mw, mh)` changes, i.e. **once**, then a
  key compare. `_flat_template` is O(w·h) once.
* `_bfs_direction` — **the hot path.** Per call: one `bytearray(tpl)` copy (~1 KB, ~0.15 µs),
  one `get_nearby_entities()` + per-entity `get_entity_type`/`get_position`, then up to two
  floods bounded together by `NAV_NODE_BUDGET = 4096` nodes. The CPU probe is asked **once per
  call, up front** (`cpu_checked`), never per pass and never mid-flood — deliberate, because
  time is frozen in the sandbox so the clock is the only one. Degrades to
  `p.cardinal_direction_to(target)` on budget exhaustion.
  Predecessor cost that this replaced: `set(self.map_walls)` rebuilt per call at 15–30 µs.
* `_move` (pave cut) — two `get_position`-class calls, O(1).

### 6.5 Risk note

> Import `_bfs_direction` without `_nav_template`/`_flat_template` and there is no padded
> border — **the bounds test that item 2 exists to enforce silently disappears from the inner
> loop** and every neighbour index runs off the array. Import `_move` without cutting the
> `PAVE_TRAIL_ON` blocks and you drag in `_eco_spendable`, `SLOT_HARVESTERS` and the whole
> conveyor-economy closure for code that never executes.

---

## 7. SURPRISES (things the builder should read before writing a line)

1. **⭐⭐ `_GRID_CACHE`'s own justification in the benchmark is false.** `eco.py:104-107` says
   the memo pays "because up to eleven builders decode the same map in one match" — but
   **module state is not shared between units** (engine-probed, positive control in the same
   tape, `doctrine.py:2146`). The memo is still correct, for a different reason. **A live doc
   defect inside the frozen benchmark.**
2. **⭐ `PAVE_TRAIL_ON = False`** — a third of `_move` is dead code in the shipped build, and
   the pave path is the *only* consumer of `SLOT_HARVESTERS` inside the pathing closure.
   Anyone lifting "cardinal pathing" naively imports the economy with it.
3. **⭐ There is no `in_bounds()` helper anywhere in 19,596 lines**, despite the rule being
   restated in seven separate comment blocks and open-coded 71 times. The benchmark enforces
   its most safety-critical invariant by repetition.
4. **⛔ `finally:`, `except BaseException:`, `except SystemExit:` do not load** — AST-rejected
   by the sandbox. Zero real uses in the tree (all 3 grep hits are comments).
5. **⛔ `write_store` raises `OverflowError`, not `GameError`.** Double-probed. A handler
   narrowed to `GameError` misses it, and it kills the unit permanently. And the engine's own
   range message is off-by-one (`0..16` for a 0..15 store).
6. **All 16 store slots are occupied and 5 are multi-field packed.** The benchmark ran out and
   started aliasing three generations of names onto the same indices — and **both live
   lost-update incidents trace to that aliasing**.
7. **The displacement guard lives inside `_raid()` and exists nowhere else.** The plain economy
   path has *no* throw detection at all, only the try/except at `eco.py:2296-2306`. Since
   SKALMAN drops the raid path (design §3), **the sole displacement guard in the benchmark is
   on the code being deleted** — it must be deliberately re-sited, not inherited.
8. **The guard does not clear `link_queue` / `samestop_*`** — a body thrown mid-wiring keeps a
   stale build queue. Latent defect; do not copy.
9. **`main.py` is unliftable beyond 22 lines.** Its methods make 3 calls into `raid.py` and
   **24 into `siege.py`**. `run` + `_dispatch` are the entire generic yield.
10. **The CPU guard has never fired locally.** `get_cpu_time_elapsed()` reads 0 under
    `fcode run` even with `--tle` (`doctrine.py:1072-1074`), so every local screen is
    un-CPU-tested. Real headroom is large (measured 642–1,123 µs/turn of 10,000,
    `docs/research/ammo-and-cpu-2026-08-09.md:124`) — but that is a *measured mean*, not a tail.

---

## 8. RECOMMENDED IMPORT ORDER

1. **`doctrine.py` slice** → new `sk_maps.py`: `CORE_PAIRS`, `MAP_ALPHABET`, `MAP_CODES`,
   `EXTRA_MAP_CODES`, `MAP_ALPHABET`, `FS_V534_MIN_TILES` (rename `SK_MAP_MIN_TILES`),
   `CARDINALS`, `DELTA`, `CARD_DELTAS`, `CARD_OPPOSITE`, `NAV_NODE_BUDGET`, `CPU_BUDGET_US`,
   `LOKI_TELEPORT_DSQ` (rename `SK_TELEPORT_DSQ`). ~95 data lines + 8 constants.
2. **`eco.py:82–234` + `237–299`** → the map layer, verbatim, minus the
   `FS_V534_MAPTRUST = False` legacy branch (`eco.py:223–234`) which should be deleted rather
   than carried dead.
3. **`main.py:396–418`** → `run` + `_dispatch`, retargeted at SKALMAN's four roles.
4. **`eco.py:444–464`** → `_cpu_exhausted`.
5. **`eco.py:902–930` + `2074–2283`** → templates + `_bfs_direction` + `_nav`; `_move` rewritten
   pave-free (~10 lines).
6. **New code:** `in_bounds()` helper (item 2), the 7-line displacement guard (item 3), the
   fresh `SK_SLOT_*` allocation table (item 5).

**Estimated verbatim import: ~430 lines of code + ~95 lines of map data.** Against the ~1.5k
from-scratch player-logic budget, that is ~22% imported, ~78% new and per-verb attributable.
