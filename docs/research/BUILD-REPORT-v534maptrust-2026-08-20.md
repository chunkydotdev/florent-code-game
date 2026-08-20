# BUILD REPORT — `bots/_v534maptrust` (v534), s52, 2026-08-20

**TWO FALSE-MATCH HAZARDS CLOSED, AND THE SECOND ONE TURNED OUT TO BE FIRING
ALREADY — ON A MAP WE OWN.** Queue #99, from
`docs/research/AUDIT-map-hardcoding-2026-08-20.md`. F1 makes `known_map_for`
verify every catalogued grid against visible terrain before adopting it; F2
grid-confirms `FS_MAP_SKIP` the way v524 already confirms the cripple list.
Building F2 surfaced that **eider has been losing ferry-siege because it shares
heart's `(28,20,(7,9),(19,9))` signature**, against the closure survey that
authored the skip set and classifies eider *Marginal*, not *SKIP* (§4.2).

Parent `bots/_v533home`, **md5-frozen at `10:07:36Z` and re-verified byte-
unchanged at `10:26:53Z`** (`scratchpad/s52_v534_build/PARENT_FREEZE.md5`).
This build never wrote to `bots/_v533home`, `bots/_v488beltbreak2`,
`scratchpad/overnight/` or `scratchpad/corefill_work.txt` — the HOMEPOOL shard
(`tools/corefill_forever.sh`, PID 68004, 8 workers, alive throughout) reads all
four. **ZERO local `fcode run` invocations**; every game in this report was
played on `work-server-1` / `work-server-2` via `tools/remote_battery.py`
(`--par 1`, 4 arms ≤ ws2's 6-core allocation). PIDs in
`scratchpad/s52_v534_build/PIDS`. Wall clock from `date -u` in the same shell
call: tree copy `10:07:36Z`, code sourcing `10:12–10:14Z`, unit harness
`10:15–10:18Z`, flag-off audit `10:18Z`, remote batteries
`10:19:27–10:25:16Z`, instrument re-run `10:26:35Z`, parent re-freeze
`10:26:53Z`.

---

## ⛔ TOP LINE — FIVE SENTENCES

1. **F1 AND F2 BOTH REACH BOTH VERDICTS, AT UNIT LEVEL, WITH THE CONTROLS
   DRIVEN THE OTHER WAY.** On colliding boards the parent adopts another map's
   grid in 8 of 8 cells and v534 returns `None` in 8 of 8; on the same fixture
   the parent refuses ferry-siege in 8 of 8 and v534 runs it in 8 of 8. On the
   **15 current-pool maps** v534 is **0 regressions in 2,092 stance-cells** and
   the **10 other catalogued maps 0 in 1,120**.
2. **THE GAME-LEVEL NEGATIVE CONTROL IS EXACT: 50 of 50 remote cells
   IDENTICAL to the parent on every compared column.** 5 pool maps × 5 seeds ×
   2 seats, NOISE_OFF both sides, `opp = _v488beltbreak2` NOISE_OFF —
   `par_off` vs `v534_off` **0 rows differ**, with a byte-identical twin arm
   reading the same 0 as the fixture's own determinism control.
3. **AND THE FIX PROVABLY EXECUTED IN THOSE GAMES.** A third arm differing from
   `v534_off` in **one integer** — `FS_V534_MIN_TILES 8 → 100000`, a constant
   read only inside the new `_maptrust_pick` — changes **50 of 50 rows**. A
   flag that never ran could not do that. **0 tracebacks in all 200 games.**
4. ⭐ **F2 EXPOSED A LIVE DEFECT IN OUR OWN CATALOGUE:** eider is currently
   stood down by heart's signature. v534 flips **eider SKIP → RUN**, which is
   free on the current pool (eider is not in it) and is declared, not silent.
5. ⚠ **VERIFICATION IS OVER VISIBLE TILES, SO IT IS PARTIAL.** Measured on
   nordkap: a single differing tile is caught **100% inside the core's r²=36
   window (32/32) and 0% outside it (0/6)**. This narrows the hazard; it does
   not close it. **No currency claim of any kind is made here** — the pricing
   read belongs to the builder.

⚠ **WRITTEN DOWN BEFORE IT IS EXPLAINED AWAY (§7):** the first game-level
battery read *48 of 50 rows differ* and was **void** — a byte-identical twin
arm read 50/50 on the same fixture. The cause was the **opponent**, not our
tree. And the first draft of F1 shipped a cache that **reintroduced the
collision bug inside the collision fix**; the unit harness caught it on
archipelago, the one `FS_MAP_SKIP` map that is in the live pool.

---

## 1. ANCHORS RE-VERIFIED AGAINST `_v533home` (HAZARD 5b)

The audit's anchors were taken on `_v529merge`/`_v531fix`, two trees back.
Re-verified line by line before any design work:

| audit anchor | on `_v529merge` | on `_v533home` | moved? |
|---|---|---|---|
| `known_map_for` singleton short-circuit | eco.py:133 | **eco.py:133** | no |
| sensed-tile compare (≥2 candidates) | eco.py:135-143 | **eco.py:135-143** | no |
| `MAP_CODES` / `EXTRA_MAP_CODES` | doctrine.py:1110 / 1142 | **1110 / 1142** | no |
| `FS_MAP_SKIP` | doctrine.py:2366 | **doctrine.py:2366** | no |
| `if sig in FS_MAP_SKIP:` | siege.py:506 | **siege.py:506** | no |
| `FS_V524_CRIPPLE_GRIDS` pattern | siege.py:63-65 | **siege.py:63-65** | no |
| `_fs_map_gated` | siege.py:480 | **siege.py:480** | no |
| live-sensing ore fallback | eco.py:1742-1754 | **eco.py:2206-2214** | **+464** |
| `_bfs_direction` cardinal fallback | eco.py:1810-1819 | **eco.py:2270** | **+460** |
| ore-partition fallback | eco.py:1698 | **eco.py:2158** | **+460** |

**Why nothing in the fix's own blast radius moved, stated as a mechanism rather
than luck:** `siege.py` and `raid.py` are **byte-identical across
`_v529merge` / `_v531fix` / `_v533home`** (md5 `0ee5bb2d…` and `3b3a0456…` in
all three), and every v530/v531/v532/v533 addition to `doctrine.py` is
**appended past line 2366**, so the table and skip-set anchors are untouched
while the file grew 5,280 → 5,701 lines. **The anchors that DID move are all in
`eco.py`, which grew 2,419 → 2,939 — and they are the ones the audit uses to
claim `None` degrades sanely, i.e. the load-bearing half.** They were relocated
and read, not assumed: `if self.map_ores and self.role != "defend"` (eco.py:2158),
the live `get_tile_env(...) == ORE_TITANIUM` scan + spiral (eco.py:2206), and
`if self.map_grid is None: return p.cardinal_direction_to(target)` (eco.py:2270).
`main.py:76` initialises `self.map_walls = set()`, so a `None` grid means "no
known walls", which is the live-sensing posture, not a crash.

---

## 2. WHAT CHANGED

`main.py` and `raid.py` are **byte-identical to the parent** (md5 verified).
Three files touched, **91 functional lines added, 1 removed**:

| file | functional + | − | what |
|---|---|---|---|
| `eco.py` | 50 | 0 | `_maptrust_pick` + one guarded call in `known_map_for` |
| `siege.py` | 25 | 1 | lazy skip-grid decode + grid confirmation in `_fs_map_gated` |
| `doctrine.py` | 16 | 0 | 3 flags, 6 map-code constants, `FS_V534_SKIP_CODES` |

The single removal is `ok = False` in `_fs_map_gated`, replaced by the
`skip` computation that ends in the same assignment.

### 2.1 F1 — `eco.py`

`known_map_for` keeps the parent's candidate filter, then:

```python
if FS_V534_MAPTRUST:
    return _maptrust_pick(candidates, w, h, own, ct)
```

`_maptrust_pick` walks `ct.get_nearby_tiles()`, bounds-checks every tile
explicitly (the s50 `is_in_vision` lesson — it is *not* a bounds guard), reads
`get_tile_env`, and drops any candidate that disagrees. If the candidate set
empties, it returns `None`; if fewer than `FS_V534_MIN_TILES` tiles were
actually verified it returns `None` rather than adopt on nothing; otherwise it
returns the first survivor — which reproduces the parent's `min()` tie-break
(first minimum) exactly when the true grid scores zero.

**Two design details that are not decoration:**

* **A disagreement is only trusted on a BUILDING-FREE tile.** `get_tile_env` is
  documented as terrain and a harvester sits *on* an ore tile rather than
  replacing it, but this function can be asked at any round by a unit whose
  core resolved late. One `get_tile_building_id` call **on the mismatch path
  only** buys that out; it costs nothing on the happy path (§5 cost table).
* ⛔ **THERE IS NO CACHE, AND THE FIRST DRAFT HAD ONE.** See §7.1.

### 2.2 F2 — `siege.py`

```python
if sig in FS_MAP_SKIP:
    skip = True
    if FS_V534_MAPTRUST:
        sgrid = self.map_grid
        if sgrid is None and ct is not None:
            sgrid = known_map_for(mw, mh, ours, ct)
        skip = sgrid is not None and sgrid in _fs_v534_skip_grids(sig)
    if skip:
        ok = False
```

Signature hit but terrain unconfirmed ⇒ **no match ⇒ ferry-siege runs**, the
registered default for an unsurveyed board. The skip grids are decoded
**lazily, one signature at a time** (at most one can ever be the board being
played), unlike v524's two import-time decodes. **`self.map_grid` is not
written on any path** — the v524 lesson verbatim: `main._builder`'s own
map_grid init is guarded by `if self.map_grid is None:` and this gate can be
asked first on the same round.

### 2.3 The six map codes were not retyped

`scratchpad/s52_v534_build/gen_doctrine_block.py` emits them from
`tools/map_encode.py`'s encoder and **refuses** unless every code is also found
verbatim in the parent's own tables and the two shared-key pairs stay distinct.
Its `--selftest` drives that checker to the other verdict on three mutants
(corrupted code → rejected; `eider == heart` → rejected; map missing →
rejected). `tools/map_encode.py --selftest` itself reproduces 5 committed
entries byte-for-byte and rejects a corrupted fjordgate.

**Identification of the ambiguous entries** (both signatures hold two maps):
`heart` = the second `(28,20,7,9,19,9)` entry, `eider` the first; `archipelago`
= the first `(26,26,5,5,19,19)` entry, `snowflake` the second. Established by
encoding `maps/heart.map26` etc. and matching the string, **not** by table
position.

---

## 3. F1 — BOTH VERDICTS

`scratchpad/s52_v534_build/test_f1.py`, full tape `OUT_f1.txt`.

### 3.1 Negative control — the catalogued grid is CORRECT everywhere we can check

| population | cells | min tiles verified | **regressions** | pre-existing wrong picks |
|---|---|---|---|---|
| **15 current-pool maps** | 2,092 | 22 | **0** | 2 |
| 10 other catalogued maps | 1,120 | 22 | **0** | 0 |

A *cell* is (map, stance, vision radius, core anchor): both core anchors at
r²=36 plus a stride-3 sweep of builder stances at r²=20. A **regression** is
v534 disagreeing with the parent, or v534 rejecting a board whose catalogued
grid is right. **`FS_V534_MIN_TILES = 8` never binds: the sparsest legal stance
on any of the 25 boards still verified 22 tiles.**

⚠ **The 2 "pre-existing wrong picks" are NOT charged to this build and the
distinction was this instrument's own first bug.** On yulerune, from stance
(0,9) at builder vision, the visible window does not separate yulerune from
frostgate (they share `(20,20,(2,9),(16,9))`) and **both trees pick frostgate**.
F1 cannot fix that — both candidates verify — and it is reported because a
"0 failures" line that quietly folded it in would have been a lie.

### 3.2 Positive control — colliding boards

Real terrain, cropped from a *different* real map, relabelled with a catalogued
signature's dims and core anchors, both core footprints cleared. Two seats each:

| fixture | parent adopts | parent's grid correct | **v534 → None** |
|---|---|---|---|
| SINGLETON (20,26) nordkap sig, valkyrie terrain | 2/2 | 0/2 | **2/2** |
| SINGLETON (16,16) lighthouse sig, valkyrie terrain | 2/2 | 0/2 | **2/2** |
| PAIR (30,30) midgard/ragnarok sig, glacierkeep terrain | 2/2 | 0/2 | **2/2** |
| PAIR (26,26) snowflake/archi sig, drakkarfjord terrain | 2/2 | 0/2 | **2/2** |

The middle column is the fixture's own control: if the parent's adopted grid
had *matched* the board, the fixture would not be a collision at all.

### 3.3 Three guards, each driven the other way

| guard | control arm | v534 |
|---|---|---|
| mismatch on a **building-free** tile | — | **refutes** → `None` |
| same tile, **building on it** | — | **does not refute** → grid kept |
| degenerate ask (`vision_sq = 0`) | parent adopts a grid | **`None`** |
| `ct = None` | parent adopts a grid | **`None`** |

### 3.4 Residual, measured

Single-tile terrain difference vs squared distance from the core anchor
(nordkap, core vision r²=36):

| d² | 1 | 4 | 9 | 16 | 25 | 36 | **49** | **64** |
|---|---|---|---|---|---|---|---|---|
| caught | 4/4 | 4/4 | 4/4 | 4/4 | 12/12 | 4/4 | **0/3** | **0/3** |

**100% inside the vision window, 0% outside it** — exactly the partial-vision
boundary, stated as a number rather than a hedge.

---

## 4. F2 — BOTH VERDICTS

`scratchpad/s52_v534_build/test_f2.py`, full tape `OUT_f2.txt`. `ok=False`
means the board is refused and ferry-siege stands down.

### 4.1 Controls

| case | parent | v534 |
|---|---|---|
| **invariant**: every `FS_MAP_SKIP` signature has registered grids | — | 5 registered, 0 unregistered, 0 orphan |
| lighthouse / saga / moonrise / heart / snowflake / archipelago, both seats | `False` 12/12 | **`False` 12/12** |
| drakkarfjord / glacierkeep / nordkap / royale | `True` | **`True`** |
| **colliding** boards on 4 skip signatures | **`False` 4/4** (the exposure) | **`True` 4/4** |
| archipelago with `self.map_grid` pre-set (the no-`ct` path) | — | `False` |

### 4.2 ⭐ THE DECLARED CHANGE — eider

| case | parent | v534 |
|---|---|---|
| eider, seat 0 and seat 1 | `False` (stood down) | **`True` (runs)** |

`docs/research/BELT-ON-SEATS-SURVEY-2026-08-17.md` classifies
**"SKIP: lighthouse 0.0, saga 1.0, moonrise 2.2, heart 2.3, snowflake 3.4,
archipelago 3.9. Marginal: meander/atoll/antler/hive/EIDER 5.7-8.8"** — eider
is explicitly *not* in the skip class, and the doctrine entry is commented
`# heart`. **eider shares heart's signature exactly**, so the bare-signature
test has been standing ferry-siege down on it anyway. Confirming by grid ends
that.

**It is free on the current pool:** the live 15 are `nordkap · fjordgate ·
antler · archipelago · drumlin · midgard · glacierkeep · yulerune ·
drakkarfjord · frostgate · icefloe · ragnarok · royale · valkyrie ·
auroraveil` (`corpus/ladder_games.tsv`, last 3,000 rated rows: those 15 at
152-213 games each, every other map ≤ 38). **eider, heart, saga, lighthouse,
snowflake and moonrise are all out — archipelago is the only `FS_MAP_SKIP` map
still in the pool**, and its shared entry registers **both** snowflake's and
archipelago's grids, so that deliberate shared treatment is preserved exactly.

**If a finals pool brings eider back** and the 5.7-8.8% marginal band is judged
too thin, the fix is eider's **own** entry with eider's **own** grid — never a
signature standing in for two maps. Flagged for the builder, not decided here.

---

## 5. FLAG-OFF IS THE PARENT — THREE WAYS

`scratchpad/s52_v534_build/test_flagoff.py`, tape `OUT_flagoff.txt`.

1. **BYTES.** `raid.py` and `main.py` md5-identical to `_v533home`.
2. **AST.** **0** module-level defaults anywhere in the tree derive from a v534
   flag (the v515 finding-3 hazard, which would make an appended arm override
   silently not reach the code). The scanner is driven both ways on a synthetic
   module: offender → 1 hit, cleaned → 0. The 6 hits in the data-constant class
   (`FS_V534_SKIP_CODES` reading the six code strings) are the **v524
   precedent**, reclassified rather than suppressed. All 4 flag read-sites
   (`eco.py:207,222`, `siege.py:547,552`) are inside function bodies.
3. **BEHAVIOUR.** With `FS_V534_MAPTRUST = False` applied **at the definition
   site** (`mkarm.sh`, never appended):

| sweep | real maps (`known_map_for`) | real maps (gate) | synthetic collisions | total |
|---|---|---|---|---|
| parent vs **FLAG-OFF** | 0 | 0 | 0 | **0 / 1,958** |
| parent vs **FLAG-ON** | **0** | 2 *(= eider, both seats)* | 20 | 22 / 1,958 |

**The breakdown is the point, not the total** — a single "22 differences" number
cannot tell a fix from a regression.

### 5.1 Cost, in ENGINE CALLS — ⛔ not microseconds

This harness has no engine; **no CPU or timing claim is made or implied**
(§8.3 defers the real one).

| case | `get_tile_env` | `get_tile_building_id` | verdict |
|---|---|---|---|
| VERIFY nordkap, core r²=36 | 113 | 0 | grid |
| VERIFY nordkap, builder r²=20 | 69 | 0 | grid |
| VERIFY midgard, core (corner-clipped) | 63 | 1 | grid |
| VERIFY archipelago, core | 111 | 1 | grid |
| **REJECT** (30,30) midgard sig / glacierkeep terrain | **1** | 1 | `None` |
| **REJECT** (26,26) snowflake sig / drakkarfjord terrain | **5** | 2 | `None` |
| **REJECT** (20,26) nordkap sig / valkyrie terrain | **13** | 1 | `None` |

**The full sweep is paid only when it SUCCEEDS** — once per unit, after which
the caller caches the grid and stops asking. **A rejection exits at the first
disagreeing tile (1-13 calls).** The in-tree precedent for the magnitude is
v524's own note: `_fs_map_gated` already pays a `known_map_for` **every round**
for the v516 turret beat on colliding signatures.

### 5.2 Exposure census

**78 catalogued `(w,h,anchor)` keys, of which 70 are SINGLETONS** — that is the
surface F1 covers. Of the 9 authored `maps/invented/*` boards, **0** collide
with a catalogued signature. ⚠ **That is a floor, not a rate:** it counts how
many boards *we happen to hold* collide, and says nothing about how likely an
unannounced finals board is to.

---

## 6. GAME-LEVEL NEGATIVE CONTROL (REMOTE)

`tools/remote_battery.py`, hosts `work-server-1` + `work-server-2`, `--par 1`,
4 arms, opponent `opp_off` (= `_v488beltbreak2` with `NOISE_ON = False`), maps
`archipelago, midgard, nordkap, yulerune, drakkarfjord`, seeds 1-5, both seats
= **50 cells per arm, 200 games**, `10:23:25–10:25:16Z`.

Compared on every column except `tag`, `arm` and `winner`. ⛔ **`winner` is
excluded because it carries the winning bot's DIRECTORY NAME**, so it reads
`par_off` in one arm and `v534_off` in the other for the identical outcome;
`ours` (US/OPP/NONE) carries the same outcome team-neutrally and **is**
compared, as are `cond`, `turn`, `tracebacks`, `ours_mined`, `opp_mined`.

| pair | shared cells | **rows differing** |
|---|---|---|
| `par_off` vs **`par_twin`** *(byte-identical copy — the fixture's determinism control)* | 50 | **0** |
| `par_off` vs **`v534_off`** | 50 | **0** |
| `par_twin` vs `v534_off` | 50 | **0** |
| **`mut_off`** vs each of the three | 50 | **50** |

**`mut_off` is the dose-delivered proof.** It differs from `v534_off` in
**one integer on one line** — `FS_V534_MIN_TILES 8 → 100000`, a constant read
**only** inside `_maptrust_pick`, which forces `known_map_for` to return `None`
on every board. It moves **50 of 50 rows**. A flag that never executed in-game
could not do that, so the 0/50 above is the fix running and agreeing, not the
fix being absent.

**Tracebacks: 0 in all 200 games** (all four arms) — no unit was destroyed by
an exception escaping the new code.

⚠ **NOT A CURRENCY READ, AND THE NUMBER BELOW MUST NOT BE QUOTED AS ONE.**
`mut_off` — the always-live-sensing posture, i.e. what an unseen colliding map
now produces — won **30 of 50** against `par_off`/`v534_off`'s **25 of 50**,
with 2 r1000 games against 5. **n=50, one opponent, one NOISE_OFF fixture that
is not the shipped configuration, 5 maps, no DEFF applied, no pre-registration.**
It is recorded because it was observed, not because it means anything. The
pricing surface is busy and the read belongs to the builder.

---

## 7. ⚠ SURPRISES — WRITTEN DOWN BEFORE THEY ARE EXPLAINED AWAY

### 7.1 The first F1 draft reintroduced the collision bug inside the collision fix

`_maptrust_pick` originally memoised "grids definitively refuted" under the key
`(w, h, our anchor)`, on the argument that terrain is static so a refutation
can never un-happen. **That argument is correct about a BOARD and wrong about a
KEY** — `(w, h, anchor)` is precisely the thing this whole build exists because
it does not identify a map. `test_f2.py` caught it **on archipelago, the one
`FS_MAP_SKIP` map in the live pool**: playing snowflake refuted archipelago's
grid under the shared `(26,26,(5,5))` key, and the next archipelago board in
the same process then verified against an empty candidate set, came back
`unknown`, and **silently turned archipelago's skip OFF**. The memo is gone;
the early exit (§5.1) is what keeps the rejecting path cheap without it.

**Not yet explained:** whether an engine process ever plays two maps without
re-importing the bot module. If it never does, the defect could not have fired
in a real match and only the harness would have seen it. I did not establish
either way and did not need to — the cache bought little and cost this.

### 7.2 The first game-level battery was VOID, and the cause was the opponent

Run at `10:19:27Z` against the **stock** `_v488beltbreak2`, `par_off` vs
`v534_off` read **48 of 50 rows differ** — which looks exactly like a large
behavioural regression. A byte-identical twin arm on the same fixture then read
**50 of 50**, so the fixture carried no information at all.
`bots/_v488beltbreak2/doctrine.py:474` has `NOISE_ON = True`, and
`tools/remote_battery.py`'s own documented determinism measurement used a
**NOISE_OFF** copy of that opponent. **I made both arms NOISE_OFF and left the
opponent noisy.** Re-run with `opp_off` gives §6's 0/50. Void tape kept at
`scratchpad/s52_v534_build/grid/` and `gridctl/` as the record.
⇒ **A determinism fixture is only deterministic if EVERY bot in it is.**

### 7.3 The row comparator's first selftest was vacuous

It mutated `arms[0]` — alphabetically `mut_off`, the arm that already differs
from everything — and "passed" while proving nothing. Fixed to pick a pair that
currently reads **0** differences and corrupt one side of it; both mutants
(`turn +1`, `ours` flipped) now move exactly **1** row. Same class as §3.1's
conflation of regressions with pre-existing wrong picks. **Two of this build's
three instrument bugs were guards that could only ever print one verdict.**

### 7.4 None of the audit's fix-site anchors had moved

Two trees and 421 doctrine lines later, every anchor F1/F2 touch is at the
**same line number** (§1). Expected them to drift; they did not, because
`siege.py` is byte-frozen since v529 and doctrine additions are appended. The
anchors that *did* move by ~460 lines are the `eco.py` fallbacks the audit's
"degrades sanely" claim rests on — i.e. the drift landed on the half a
re-verification pass would have been most tempted to skip.

---

## 8. FAILURE REEL + MANIFEST

### 8.1 FAILURE REEL — ⛔ THERE IS NONE, AND HERE IS WHY

**No replay in this build exists to be reeled.** Both remote batteries ran
`--replay /dev/null` — not a choice of this build but a property of
`tools/remote_battery.py` (its own docstring: *"NO REPLAYS COME BACK. Remote
games run `--replay /dev/null`"*), and the hard constraint on this build was
**zero local `fcode run`**, which is the only path that retains a replay. So
the house convention (earliest our-core-death per map, capped at 5) cannot be
applied and is recorded as **not executed**, not as "no deaths".

**And it would carry nothing even if it existed.** The 50 remote cells for
`v534_off` are **byte-row-identical to the parent's**: any death in that arm is
the parent's death, at the same turn, in the same game. The informative arm is
`mut_off`, and what it demonstrates is a *constant* being read, not a tactical
failure.

**Exact re-run recipe for anyone who wants the replays** (local, and therefore
only once the HOMEPOOL shard is off the box):
```
.venv/bin/fcode run scratchpad/s52_v534_build/arms/v534_off \
    scratchpad/s52_v534_build/arms/opp_off maps/archipelago.map26 \
    --seed 1 --tle 10 --replay <path>
```
(swap the two bot arguments for a seat-B cell; `par_off` / `mut_off` for the
other arms; seeds 1-5; maps archipelago, midgard, nordkap, yulerune,
drakkarfjord). ⚠ Reproducible **only** with both trees NOISE_OFF — §7.2.

### 8.2 MANIFEST — the unit-harness cases

All under `scratchpad/s52_v534_build/`. Every instrument has a `--help` and a
selftest, and every selftest is driven to **both** verdicts.

| instrument | what it establishes | tape | selftest drives the other way |
|---|---|---|---|
| `gen_doctrine_block.py` | the 6 map codes come from the encoder and match the committed tables | `OUT_codes.txt` | corrupted saga code → rejected; `eider == heart` → rejected; map missing → rejected |
| `harness.py` | the fake Controller reproduces real terrain, **can lie**, and raises off-map like the engine | `OUT_harness.txt` | corrupted fixture reads WALL; `(-1,0)` raises |
| `test_f1.py` | §3, 3,212 real-map cells + 8 colliding cells + 4 guards + the residual cut | `OUT_f1.txt` | parent adopts / v534 rejects on every collision; parent adopts / v534 refuses on both degenerate guards |
| `test_f2.py` | §4, 12 skip cells + 8 non-skip + 8 colliding + eider + the pre-set-grid path | `OUT_f2.txt` | parent refuses / v534 runs on all 4 collisions |
| `test_flagoff.py` | §5, md5 + AST + 1,958-cell behavioural sweep | `OUT_flagoff.txt` | synthetic module-level offender → 1 hit, cleaned → 0; flag-on differs in 22 while flag-off differs in 0 |
| `census.py` | §5.2 exposure census + §5.1 engine-call cost | `OUT_census.txt` | — (descriptive; no verdict to invert) |
| `rowdiff.py` | §6 row identity across arms | `OUT_rowdiff.txt` | corrupts a **0-difference** pair; both mutants move exactly 1 row |

**Fixture provenance:** the colliding boards are **not synthetic noise** — each
is real terrain cropped from a *different* real pool map and relabelled with a
catalogued signature's dims and core anchors, with both core footprints
cleared. `crop_from()` in `test_f1.py`. **No `.map26` files were authored**
(§8.4).

### 8.3 MANIFEST — the remote batteries

| tape | when (`date -u`) | arms | opponent | cells/arm | status |
|---|---|---|---|---|---|
| `grid/` (`par_off`, `v534_off`, `mut_off`) | 10:19:27–10:20:38Z | 3 | `bots/_v488beltbreak2` **(NOISE_ON)** | 50 | ⛔ **VOID** — §7.2 |
| `gridctl/` (`par_off`, `par_twin`) | 10:21:28–10:22:38Z | 2 | same, NOISE_ON | 50 | ⛔ **VOID**, and it is what proved the first tape void: 50/50 on byte-identical arms |
| **`grid2/`** (`par_off`, `par_twin`, `v534_off`, `mut_off`) | **10:23:25–10:25:16Z** | 4 | `arms/opp_off` **(NOISE_OFF)** | **50** | **LIVE — §6** |

Maps `archipelago, midgard, nordkap, yulerune, drakkarfjord`, seeds 1-5, both
seats, `--block-size 1 --par 1`. Merged tapes at `<dir>/ALL.tsv` (an `arm`
column prepended; the per-arm remote tsv has none). Host preflight recorded
`ws1 nproc=16 load=0.68 corefill_workers=0`, `ws2 nproc=6 load=0.09
corefill_workers=0`, `fcode 2.3.6 (pin ok)`, both hosts CLEANED after each run.

**Map choice, stated as a rule rather than a taste:** archipelago is the only
`FS_MAP_SKIP` map in the live pool (F2's only on-pool surface); midgard and
yulerune are the two collision pairs that also feed the v524 cripple gate;
nordkap is a plain singleton; drakkarfjord is a clean control that touches
neither mechanism.

### 8.4 WHAT THIS BUILD DID **NOT** DO — deferred to the builder post-shard

1. ⛔ **A GAME-LEVEL DEMO ON A COLLIDING MAP.** `tools/remote_battery.py`
   ships maps by name from `maps/` and **refuses if the map is not present
   there** (`:506`), so a custom colliding board would have to be committed
   into the repo's shared `maps/` directory while a shard is live. Not done.
   The mechanism is established at unit level (§3.2, §4.1) and the game-level
   demo is deferred. *(This is the brief's "if it doesn't ship maps, say so and
   defer".)*
2. ⛔ **ANY CPU / TLE MEASUREMENT.** §5.1 counts **engine calls**, not time.
   The added first-turn cost on a *verifying* board (up to 113 `get_tile_env`
   on the core, ~69 on a builder) has **not** been measured against the 10 ms
   budget, because that needs local `fcode run` with per-turn telemetry. The
   in-tree precedent (v524 pays a `known_map_for` every round on colliding
   signatures) is an argument, not a measurement.
3. ⛔ **AN ENGINE PROBE OF `get_tile_env` UNDER A BUILDING.** The building
   guard (§2.1) exists precisely because this is assumed, not verified. A
   3-line probe bot would settle it.
4. ⛔ **THE GENERALISATION BATTERY** the audit's F3 asks for (head vs incumbent
   on the 9 rotated-out era-1 maps + `maps/invented/`). Out of scope here;
   still the number that would price the overfit.
5. ⛔ **ANY CURRENCY READ.** Deliberate. §6's 25/25/30 split is reported as an
   artefact of a control arm and explicitly disclaimed.

---

## 9. HONEST LIMITS

* **Verification is partial by construction.** A colliding board that also
  agrees with the catalogue across the whole visible window is still adopted.
  Measured boundary: 100% caught inside r²=36, 0% outside (§3.4).
* **Opportunistic re-verification is real but shallow.** Because no positive
  verdict is cached, a unit that asks again with wider vision re-verifies for
  free — but `main.py` caches `self.map_grid` on the first success, so in
  practice each unit verifies once, at whatever vision it had then.
* **F1 cannot disambiguate an indistinguishable pair.** The yulerune/frostgate
  cell in §3.1 picks the wrong member from one stance under both trees.
  Pre-existing, unchanged, and out of this fix's reach.
* **The census is a floor, not a rate** (§5.2).
* **The unit harness is a fake Controller.** It makes no claim about play,
  tempo or outcome — only about which grid a lookup returns for given visible
  terrain. Every game-level claim here is remote (§6) or deferred (§8.4).
* **n = 50 cells per arm on 5 maps against 1 opponent** in §6. That is an
  identity check, which needs only to be exact, not powered — it is **not** a
  performance sample and no interval is quoted for it.
* **eider's flip is a judgement, not a measurement.** It follows the survey's
  own classification; if the builder disagrees, the remedy is eider's own entry
  with eider's own grid (§4.2).
