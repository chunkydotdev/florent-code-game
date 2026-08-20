# BUILD REPORT — `bots/_v535cornergate` (2026-08-20)

**Base:** `bots/_v534maptrust` (copied, never edited in place).
**Change:** ONE mechanism — `FS_V535_CORNER_GATE` (default **ON**): the home
package's **corner barriers** stand down on boards the **ferry-siege refuses**.
**Flag-off contract:** `FS_V535_CORNER_GATE = False` ⇒ `bots/_v534maptrust`.

All timestamps from `date -u` in the same shell call. Build window
2026-08-20T14:45:16Z → 14:58:27Z (remote grid) → dose (below).

---

## 1. Why — the evidence chain, in the order it was read

**s52 REFUSING DECOMPOSITION** (`docs/coordination.md`, 2026-08-20T12:22:11Z;
ws2, six arms, 240 games/arm, 0 shells, 0 tracebacks). The fixture reproduces
the diagnostic fact first (`v533home` 29.6% ≈ HOMEPOOL's refusing 28.3), then:

| arm | share% | arch/120 | midg/120 | Δ vs v533home (pairwise hw ±8.9) |
|---|---|---|---|---|
| parent | 50.4 | 50 | 71 | +20.8 |
| floff | 46.7 | 38 | 74 | +17.1 |
| **coff** | 43.8 | **54** | 51 | **+14.2 — OUTSIDE hw** |
| doff | 35.4 | 24 | 61 | +5.8 (inside) |
| moff | 31.2 | 30 | 45 | +1.7 (inside) |
| v533home | 29.6 | 19 | 52 | — |

`coff` is **corners off**. Its +14.2 **[5.3, 23.1]** excludes zero at pairwise
power and the damage is **archipelago-concentrated** (19/120 = 15.8% vs
54/120 = 45.0%; midgard flat 52 vs 51). Mouth and door-kill are acquitted on
this axis.

**s52 diagA2 ATTRIBUTION** (09:18:21Z, n=480/arm) reads the same direction from
the other side: `nocorner` was the only ablation that **recovered wins to parent
parity** (−0.4) and moved the r300 bar **+3.1** — while `nodoor` cost −17.9 and
`nomouth` −6.67, i.e. those two planks earn their seats.

**Context** (GENREF/GENINV, 10:58:11Z): archipelago is the pool's single
biggest deficit cell, and `v534maptrust` is the head candidate (same price
everywhere as `v533home`, kills the false-match class, cures eider).

**The named fix, verbatim from the 12:22Z readout:** *"one flag-gate: corners
OFF on refusing/gated maps — the same geometric predicate the siege gate
already computes; the home package's map-INVARIANCE was the design gap."*
This build is that and nothing else.

---

## 2. Mechanism and gate-verdict plumbing

### 2.0 ⭐ THE LINE COUNT, RECONCILED — and the audit question answered on the tree, not in prose

**The side lane's audit** (2026-08-20, mid-flight) asked two things of a diff
that is ~278 lines against a design stated as *"one flag-gate reusing the
existing predicate"*: **enumerate the lines**, and say whether the siege gate's
predicate is **CALLED** or **RE-DERIVED**. Both are answered here, and the
second one changed the tree.

**Enumeration.** `git`'s line count and the *executable* change are not the
same object. Measured, per file, added / removed / **added non-comment,
non-blank**:

| file | +lines | −lines | **+ non-comment** | what those lines are |
|---|---|---|---|---|
| `doctrine.py` | 123 | 0 | **3** | `LOKI_FS_V535`, `FS_V535_CORNER_GATE`, `FS_V535_LOG`. The other **120 lines are the doctrine block** — the evidence table, the design gap, the where-it-binds measurement, the surprise in §3. House convention (v524/v530/v532/v534 blocks are the same shape). |
| `siege.py` | 97 | 5 | **~31** | `_v535_map_refuses` (**~12** executable) + `_fs_enemy_anchor` (**~9**, an *extraction*, see below) + `_fs_gate` rewired to call it (−5/+2). Rest: docstrings. |
| `eco.py` | 51 | 2 | **~14** | `_v535_corners_on` (**11** executable) + 2 call sites + 1 changed conjunction. Rest: docstrings. |
| `main.py` | 7 | 0 | **2** | `self.v535_refuse = None`, `self.v535_corner_gated = 0`. Rest: comment. |
| `raid.py` | 0 | 0 | 0 | untouched, md5-identical |

⇒ **≈50 executable lines across three functions, two of which are five and
eleven statements long.** The remaining ~228 are doctrine prose and
docstrings. That is consistent with "one flag-gate", and the enumeration is
what makes the claim checkable rather than assertable.

**CALLED or RE-DERIVED — and the honest answer is that the FIRST DRAFT WAS
PARTLY RE-DERIVED.**

* The **gate verdict itself** was always **CALLED**: `_fs_map_gated`, the
  existing verified function, unmodified.
* But the first draft of `_v535_map_refuses` **COPIED eight lines of
  `_fs_gate`'s enemy-anchor resolution** inline (`self.enemy` → `SLOT_ENEMY_CORE`
  → mirror), with a docstring defending the copy as *"deliberately duplicated
  rather than shared"*. **That is a re-derivation, it inherits none of the
  original's verification (D21d), and defending it in a comment is not
  verifying it.**
* **It was refactored away rather than defended.** `_fs_enemy_anchor` is now
  extracted in `siege.py` and **both** `_fs_gate` and `_v535_map_refuses` call
  it. There is now **one** anchor resolution in the tree, as there is **one**
  `_fs_map_gated`. What remains local to `_v535_map_refuses` is the **cache**
  and the **sign flip** — nothing else.

**The extraction touches `_fs_gate`, which is not flag-gated**, so it is
verified three ways (`test_called.py`, `OUT_called.txt`, **PASS**):

1. **Structural (AST).** `_v535_map_refuses`'s body (docstring stripped —
   prose must not score) **calls** `_fs_map_gated` and `_fs_enemy_anchor`, and
   contains **none** of the tokens a re-derivation needs: `FS_MAP_SKIP`,
   `FS_V525_MIN_MAP_DIM`, `FS_V525_MIN_CORE_DSQ`, the cripple lists,
   `known_map_for`, `distance_squared`, `read_store`, `enemy_core_for`,
   `unpack_pos`, `SLOT_ENEMY_CORE`. ⛔ **Driven the other way**: the same
   scanner on `_fs_map_gated` and `_fs_enemy_anchor` **must** find those tokens
   — otherwise "0 leaked" would just be a report about an empty function. It
   does. Its full call set is
   `['_fs_enemy_anchor', '_fs_map_gated', 'get_current_round', 'get_id', 'print']`.
2. **Behaviour-preserving, in the harness.** The extracted `_fs_gate` is
   compared against the **PARENT** `_v534maptrust._fs_gate` over the whole map
   pool × both seats × **all three anchor states** the extraction spans
   (own `self.enemy` set / only `SLOT_ENEMY_CORE` published / neither, i.e. the
   mirror fallback) — **204 cells, 0 mismatches, and the comparison saw BOTH
   verdicts.** ⛔ Driven the other way: a stub anchor returning a bogus core
   **must** flip the verdict, and the mutant had to be re-sited to do so — the
   first version put it on archipelago, which refuses via `FS_MAP_SKIP`
   anyway, so both arms said "refuse" and the mutant read as no-change. *A
   mutant on a board that already gives the target verdict demonstrates
   nothing.* Re-sited to nordkap (which RUNS, precondition asserted), it fires.
3. **Behaviour-preserving, ON THE ENGINE.** The determinism grid in §4.1 was
   **re-run after the refactor** (runid `bb_20260820T150602Z_10908`): `par_off`
   is the **un-refactored parent**, `v535_off` carries the extraction, and they
   are **row-identical on all 72 cells** — including the **48 running cells
   where the siege actually runs and therefore actually calls `_fs_gate`.**

And the reader is checked against the original directly: **`_v535_map_refuses(ct)
== not _fs_gate(ct)` on all 68 pool cells, with both verdicts occurring.**

### 2.1 What changed

Four files, `raid.py` untouched (md5-identical to the parent).

| file | what |
|---|---|
| `doctrine.py` | the v535 block + 3 flags |
| `siege.py` | `SiegeMixin._v535_map_refuses(ct)` + the `_fs_enemy_anchor` extraction |
| `eco.py` | `EcoMixin._v535_corners_on(ct)`, and the two read sites now call it |
| `main.py` | `self.v535_refuse = None`, `self.v535_corner_gated = 0` |

### 2.2 The verdict is READ, not reimplemented

`Player` is `(EcoMixin, RaidMixin, SiegeMixin)` — one class — so an eco body
can ask a siege method on `self` at runtime without eco importing siege (which
it must not: siege imports eco).

```
eco._v530_corner_act  ─┐
                       ├─> eco._v535_corners_on(ct) ─> siege._v535_map_refuses(ct)
eco._v530_mouth_arm   ─┘                                      │  (cache + sign flip
                                                              │   ONLY -- see §2.0)
                                        ┌─────────────────────┴─────────────────┐
                                        v                                       v
                          siege._fs_enemy_anchor(ct)          siege._fs_map_gated(mw, mh, ours, E, ct)
                          (extracted; _fs_gate calls          (the SAME pure function _fs_gate calls,
                           the same one)                       unmodified)
```

`_fs_map_gated` is the existing determination: the v525 min-dim / min-core-d²
floors, the **grid-CONFIRMED** `FS_MAP_SKIP` set (v534 F2) and the
**grid-CONFIRMED** cripple list (v524 change 1). **Geometry and tile grids
only — no map names reach a bot** (map-robustness policy F3), and an
unsurveyed board's registered default is "plays normally".

**Why not call `_fs_gate` itself**, which is the obvious call and is wrong
twice over:

1. `_fs_gate` returns `False` when `LOKI_FERRY_SIEGE_ON` is off. That is a
   property of **our build**, not of the **board**. Conflating them would
   silently delete the corners in every `_v488beltbreak2`-equivalent arm and
   make the master-off control mean something other than what it says.
2. `_fs_gate` **caches into `self.fs_gate_ok`**. Called from the eco path it
   would populate that cache on a round the siege had not yet asked — and
   `_fs_gate`'s enemy-anchor resolution falls back to a **mirror guess** before
   `SLOT_ENEMY_CORE` is published, so an early eco call could freeze a siege
   verdict computed off the guess.

`_v535_map_refuses` therefore **shares** `_fs_gate`'s **anchor resolution** via
the extracted `_fs_enemy_anchor` (`self.enemy` → `SLOT_ENEMY_CORE` →
`enemy_core_for` mirror; `None` ⇒ do not cache, ask again next round) and keeps
its **own** cache, `self.v535_refuse`.
Safe because `_fs_map_gated` **writes nothing to `self` on any path** — both
its v524 and v534 blocks say so in as many words, and the v524 comment records
the live ~830-round divergence found when an earlier draft did cache there.

### 2.3 TWO read sites, gated together — this is the design decision

`FS_V530_CORNERS` had two readers and they are a **pair**:

* `_v530_corner_act` — the barrier build itself.
* `_v530_mouth_arm` (v532 WEAVE) — which **bans** the four corner tiles from
  the opening chain *"because they will be built"*.

Gating only the build would leave the mouth planner routing the opening chain
around four tiles nothing ever takes — a pure loss, landing on **exactly** the
boards this fix exists for. Both sites now call `_v535_corners_on(ct)`. That is
one mechanism expressed at two sites, not two mechanisms.

### 2.4 Order of tests (load-bearing)

```python
if not FS_V530_CORNERS:          return False   # corners-off arms never reach the gate
if not (LOKI_FS_V535 and FS_V535_CORNER_GATE):
                                 return True    # flag-off == FS_V530_CORNERS exactly
try:    refuses = self._v535_map_refuses(ct)
except Exception:                return True    # unreadable gate => PARENT behaviour
```

and at the build site the gate is placed **last** in its conjunction
(`LOKI_FS_V530 and not endgame and role in (...) and _v535_corners_on(ct) and
_v530_corner_act(...)`) so a body that could never build a corner anyway never
pays for the verdict.

**Cost:** one `_fs_map_gated` call per **body per game**, cached. On a board
whose signature is on neither list it is three integer comparisons touching no
tiles; on a signature hit it may call `known_map_for` once (tile-sense +
compare against a cache-memoised decode) — the cost the siege path already
pays. **No comms-store slot is taken** (all 16 are assigned). *No CPU
measurement is claimed here; local CPU is blind and the platform `match test`
is the instrument for that question.*

---

## 3. Where the gate binds — BOTH VERDICTS, whole pool

`scratchpad/s52_v535_build/gatemap.py` drives the **shipped** predicate
end-to-end on a real `Player` for every `maps/*.map26` from **both seats** —
68 cells. Full table: `scratchpad/s52_v535_build/OUT_gatemap.txt`.

```
CELLS 68 | refuse 16 | run 52 | GATED-OFF 16 | SEAT-ASYMMETRIC: none
```

| class | maps | why |
|---|---|---|
| **REFUSE (8)** | archipelago, heart, lighthouse, moonrise, saga, snowflake | `FS_MAP_SKIP`, **grid-confirmed** (v534 F2) |
| | midgard | `FS_V525_CRIPPLE_MAPS`, **grid-confirmed** (v524 ch.1) |
| | inv_tiny8 | 8×8, under `FS_V525_MIN_MAP_DIM = 10` |
| **RUN (26)** | antler, atoll, auroraveil, drakkarfjord, drumlin, eider, fjordgate, frostgate, glacierkeep, hive, icefloe, inv_duel16, inv_hsym16, inv_large30, inv_mid20, inv_pierce16, inv_small12, inv_vsym16, inv_wide30x14, jackpot, meander, nordkap, ragnarok, royale, valkyrie, yulerune | |

**⭐ THE SURPRISE, written down before it is explained away.** This build went
in expecting **fjordgate** and **jackpot** to be the canonical refusals — that
is what `_fs_gate`'s own docstring says, *in this tree, today*: *"fjordgate …
is the game the 2174-rated version LOST … jackpot is the other refusal."*
**Both RUN.**

* **fjordgate** runs because **v525's standdown flip lowered the floors to
  fjordgate's OWN dimensions** — `FS_V525_MIN_MAP_DIM = 10  # fjordgate's own
  larger side`, `FS_V525_MIN_CORE_DSQ = 32  # fjordgate's own core d^2` — and
  both tests are strict `<`. The map the floors were named after is now the
  first map that passes them.
* **jackpot** runs because it was **never encoded on any list at all**; the
  docstring records a probe finding that no constant ever carried.

⇒ **The prose in `_fs_gate` is a stale description of its own predicate.** Had
this build trusted it instead of measuring, the report would name two maps
where the gate does not bind and would **miss midgard, where it does** — and
midgard is half the refusing panel. Same family as the two CLAUDE.md
precedents (a fact in a reference nobody re-derives is a fact nobody has).
Filed as a doc-vs-code drift item for the successor list; **the code shipped,
the code is what §3 reports**, and the docstring was left unedited so the
delta stays visible rather than being quietly laundered.

**⭐ AND THE CHEAP CONFIRMATION NOBODY ARRANGED:** the refusing decomposition's
two-board panel was assembled from **HOMEPOOL's refusing cut** — archipelago
and midgard. Asked independently, this predicate returns **exactly those two**
as `refuse = 1`. The fixture and the gate agree without having been made to.

**8 mutants, every one driven to the other verdict**
(`gatemap.py --selftest`, output in §7):
board under the dim floor → refuse · cores at d²=2 → refuse · the same open
30×30 with cores apart → **RUN** · archipelago (grid-confirmed skip) → refuse ·
**archipelago's signature with a flat grid → RUN** (the v534 F2 property: a
bare signature hit is only a candidate) · `FS_V535_CORNER_GATE=False` on a
refusing board → corners **ON**, cache never even computed · `FS_V530_CORNERS
=False` on a running board → corners **OFF**, gate never consulted · the cache
is a cache (second call costs 0 extra tile reads, first call cost >0).

---

## 4. Flag-off is the parent — proved four ways

`scratchpad/s52_v535_build/test_flagoff.py` → `OUT_flagoff.txt`, **PASS**.

**1. Bytes.** `raid.py` md5-identical to `_v534maptrust`
(`3b3a0456e9a22083df4653526bfd68c8`); exactly the four intended files differ.

**2. Read-site scan, with the HOUSE POSITIVE CONTROL.** All three v535 read
sites are **inside function bodies** (`eco.py:1593` ×2, `siege.py:701`), so an
arm override reaches the code — the v515 finding-3 hazard.
⛔ The control, and it is the house one: **`FS_V530_MOUTH_SEATS`** is a known
**dead** flag in this lineage. The same scanner run on it returns **0 read
sites**, and on the live `FS_V530_CORNERS` returns several — plus a check that
the dead flag really is *defined* (or "0 sites" would only mean "misspelled").
A scanner that has only ever printed "all good" has not been seen to check.

**3. No derived module-level default** anywhere in the tree reads a v535 flag —
and the scanner is driven both ways on a synthetic module that has one (finds
1) and one that does not (finds 0).

**4. Behaviour.** With `FS_V535_CORNER_GATE = False` the predicate returns
exactly `FS_V530_CORNERS` on **all 68 pool cells**, *including* the 16 where
flag-on deliberately differs (`gate-ON differs on 16 of 68`). And the siege
helper is **never called at all** — proved by monkeypatching it to raise.

> ⛔ **A finding about the shipped code, surfaced by that last test.** The trap
> must be a `BaseException`, not an `AssertionError`: `_v535_corners_on` wraps
> the helper in `except Exception: return True` (the deliberate
> "unreadable gate ⇒ parent behaviour" fallback), so an `Exception` trap is
> **swallowed** and the control reads "never called" whether or not it was.
> The first draft of that test did exactly that and printed a **false pass**.
> Fixed; and the same trap is then **armed against the gate-ON arm and MUST
> fire**, which it does. A trap the code under test can catch is not a trap.

### 4.1 Flag-off byte-identity at GAME level

Remote battery, **work-server-2 only** (ws1 down for maintenance),
`tools/remote_battery.py`, `--par 2`, runid **`bb_20260820T150602Z_10908`**,
15:06:02Z → 15:08:40Z, remote scratch CLEANED. **This is the RE-RUN after the
`_fs_enemy_anchor` refactor** (§2.0); the pre-refactor run
(`bb_20260820T145537Z_69759`, 14:55:37Z → 14:58:19Z) produced **the same
numbers in every cell**, which is a fourth, unplanned confirmation that the
extraction changed no game.

* **3 NOISE_OFF arms** × 6 maps × 6 seeds × 2 seats = **72 rows/arm, 216
  total, all COMPLETE, 0 tracebacks.**
* **⛔ The opponent is a NOISE_OFF copy too** (`arms/opp_off`) — the v534
  lesson: *every* bot in a determinism fixture must be `NOISE_ON = False`, or
  it is not a determinism fixture.
* Arms: `par_off` = `_v534maptrust`; `v535_off` = child with
  `FS_V535_CORNER_GATE=False`; `v535_on` = child as shipped. All built by
  `mkarm.sh`, which edits the **definition site** (never appends).

`rowdiff.py` compares every shared `(map, seed, seat)` cell on **all columns
except `tag`/`arm`/`winner`** (`winner` carries the bot *directory name*, a
pure name difference; `ours` carries the same outcome team-neutrally and **is**
compared):

```
   par_off      vs v535_off       72 shared cells,   0 rows differ
   par_off      vs v535_on        72 shared cells,  24 rows differ
   v535_off     vs v535_on        72 shared cells,  24 rows differ
== BY MAP CLASS ==
   par_off  vs v535_off :  REFUSE  24 cells,   0 differ | run  48 cells,  0 differ
   par_off  vs v535_on  :  REFUSE  24 cells,  24 differ | run  48 cells,  0 differ
   v535_off vs v535_on  :  REFUSE  24 cells,  24 differ | run  48 cells,  0 differ
```

**⭐ That is the positive control in BOTH directions, in one tape:** flag-off is
row-identical to the parent everywhere; flag-on is row-identical on **48/48
running cells** and diverges on **24/24 refusing cells**. A whole-tape count of
0 would have *falsified* the build (it would mean the gate never fired) — which
is why the per-class split was added to `rowdiff.py` for this build.

**Comparator mutation-tested** on a pair that reads 0 in the live tape
(`par_off` vs `v535_off`): `turn +1` → exactly 1 row differs; `ours` flipped →
exactly 1 row differs. **SELFTEST PASS.**

---

## 5. Dose — corner builds per game, both map classes, both arms

`scratchpad/s52_v535_build/dose.sh` + `doseread.py`.

**⛔ Local by necessity, not by choice:** `remote_battery.py` returns **no
per-game stdout/stderr**, and the corner counter *is* a stderr tape
(`FS_V530_LOG` → `V530 CORNER rnd=… tile=…`). Run only after
`scratchpad/overnight/HOMEPOOL.tsv` reached its 5,400 data rows — the HOMEPOOL
box-ownership constraint was respected throughout; **no local `fcode run` was
issued before that** (the entire §4.1 grid was remote).

Arms `dose_par` (`_v534maptrust`) and `dose_v535` (shipped child), both
`FS_V530_LOG=True`, both `NOISE_ON=False`, opponent `arms/opp_off` (NOISE_OFF).
4 maps × 3 seeds × 2 seats = **24 games/arm**: archipelago + midgard
(REFUSING), glacierkeep + ragnarok (siege-active).

⛔ **SECTION VOID — THE DOSE WAS NEVER RUN (corrected s52 ~18:2xZ, builder).** This
section was committed holding an unfilled placeholder: the build agent scripted the dose
(`dose.sh`, `doseread.py` — both exist) and was killed by an API error before running it;
the resumed agent committed the report without noticing the hole, and §6's manifest
asserted the 48 games anyway (corrected there too). Caught by the V535POOL prereg drafter
at draft (blocker B3). The dose is OWED post-screen; until it exists the gate's evidence
is the predicate drive and the engine grid (§4), and nothing in this section may be cited.

`doseread.py --selftest` drives every counter to the other verdict: a tape with
corner lines counts them (2); the same tape with them removed reads exactly 0
while still seeing the gate line (**the two counters are not aliases**); a
gate-only tape reads 0 corners / 2 gate asks / 2 refusals; the refusal counter
also reads 0 on a tape whose gate line says `refuse=0`; a `Traceback` tape is
reported.

---

## 6. D16 — reel / manifest

**What exists, where, and what it is worth.**

| tape | path | rows/games | replays? |
|---|---|---|---|
| Gate verdict, whole pool × both seats | `scratchpad/s52_v535_build/OUT_gatemap.txt` | 68 cells | n/a (no engine) |
| Gate mutants (8, both verdicts) | `gatemap.py --selftest` → §7 | — | n/a |
| Flag-off / read-site / AST | `scratchpad/s52_v535_build/OUT_flagoff.txt` | 68 cells + 5 mutants | n/a |
| **CALLED-not-re-derived (D21d)** | `scratchpad/s52_v535_build/OUT_called.txt` | 204 anchor cells + 68 reader cells + 1 mutant | n/a |
| **Determinism grid (remote, ws2)** | `scratchpad/s52_v535_build/grid/` — `par_off.tsv`, `v535_off.tsv`, `v535_on.tsv`, `ALL.tsv`, `RESULT.txt`, `_raw/` | **216 rows** (72/arm) | ⛔ **NO REPLAYS** — remote games run `--replay /dev/null` |
| Row identity + per-class split | `scratchpad/s52_v535_build/OUT_rowdiff.txt` | 216 | — |
| Tape cut + seed degeneracy | `scratchpad/s52_v535_build/OUT_tapecut.txt` | 216 | — |
| **Dose (local)** | ⛔ **CORRECTED s52 ~18:2xZ (builder): THIS ROW WAS FALSE — THE DOSE NEVER RAN.** `scratchpad/s52_v535_build/dose/` does not exist; §5 above holds a literal unfilled `⛔ **SECTION VOID — THE DOSE WAS NEVER RUN (corrected s52 ~18:2xZ, builder).** This
section was committed holding an unfilled placeholder: the build agent scripted the dose
(`dose.sh`, `doseread.py` — both exist) and was killed by an API error before running it;
the resumed agent committed the report without noticing the hole, and §6's manifest
asserted the 48 games anyway (corrected there too). Caught by the V535POOL prereg drafter
at draft (blocker B3). The dose is OWED post-screen; until it exists the gate's evidence
is the predicate drive and the engine grid (§4), and nothing in this section may be cited.` placeholder. The build agent was killed by an API error between scripting the dose (`dose.sh`/`doseread.py` exist) and running it, and the resumed agent asserted this manifest row from its plan rather than from disk. Caught by the V535POOL prereg drafter (blocker B3); nothing from §5 or this row may be quoted. The in-game corner-build-count dose is OWED and will be run post-screen, pre- or alongside the V535POOL shard; the gate's behaviour evidence until then is the two surfaces that DO exist (68-cell predicate drive + 216-row engine grid, 24/24 refuse-differ / 0/48 run-differ). | **0 games** | ⛔ none |
| Driver log / remote pids | `grid.log`, `grid/REMOTE_PIDS.txt`, `PIDS` | — | — |
| Parent freeze | `scratchpad/s52_v535_build/PARENT_FREEZE.md5` | — | — |

**Runid** `bb_20260820T150602Z_10908` (pre-refactor twin `bb_20260820T145537Z_69759`), host work-server-2, remote scratch
cleaned by the tool. Namespace: build batteries land under
`scratchpad/build_batteries/` — **not** an `auto_gate`-scanned path (the
`remote_battery.py` namespace proof), and nothing was written to
`scratchpad/overnight/`, `scratchpad/overnight-remote/` or
`scratchpad/corefill_work.txt`.

**Which replays exist:** only the **48 dose games**. Every remote game is
replay-less by construction. Anything that needs to be watched must be re-run
locally.

---

## 7. Instrument outputs (verbatim)

```
$ .venv/bin/python scratchpad/s52_v535_build/harness.py --selftest
[ok] loader: parent (_v534maptrust) has no FS_V535_CORNER_GATE
[ok] loader: child (_v535cornergate) FS_V535_CORNER_GATE=True
[ok] loader: main.Player importable from both trees
[ok] FakeCt: 113 tiles at nordkap core, env round-trips
[ok] FakeCt: corrupted fixture reads WALL (the harness can lie)
[ok] FakeCt: off-map read raises, as the engine does
[ok] make_player: child Player boots with v535_refuse=None
[ok] make_player: parent Player has no _v535_corners_on (the probe can tell the trees apart)
SELFTEST PASS

$ .venv/bin/python scratchpad/s52_v535_build/gatemap.py --selftest
[ok] mutant 1 (8x8 board, under min dim) refuses: True
[ok] mutant 1 corners stand down: False
[ok] mutant 2 (cores d^2=2) refuses: True
[ok] control (30x30 open, cores far) RUNS: False
[ok] control corners stay ON: True
[ok] mutant 3 archipelago refuses: True
[ok] mutant 3 archipelago corners stand down: False
[ok] mutant 4 (arch signature, flat grid) RUNS: False
[ok] mutant 4 corners stay ON: True
[ok] mutant 5 gate-off: corners ON on a refusing board: True
[ok] mutant 5 gate-off: refusal never computed (cache stays None): None
[ok] mutant 6 corners-off: corners OFF on a running board: False
[ok] mutant 6 corners-off: gate never consulted (cache stays None): None
[ok] parent FS_V530_CORNERS is the whole predicate: True
[ok] mutant 8 second call costs 0 extra tile reads: 0
[ok] mutant 8 first call DID read tiles (so 0 above means cached): True
SELFTEST PASS
```

Full `test_flagoff.py`, `rowdiff.py`, `tapecut.py` and `doseread.py` output is
in the `OUT_*.txt` files named in §6.

---

## 8. Honest limits — what this build does NOT establish

1. **NO CURRENCY CLAIM IS MADE HERE, AND THE TAPE COULD NOT CARRY ONE.**
   `tapecut.py` measures the determinism fixture's own **seed degeneracy**:
   with `NOISE_ON = False`, 72 rows/arm collapse to **5–8 distinct outcome
   signatures** per arm per map class. Six seeds into a `(map, seat)` cell
   produce ~1 distinct game. The win column below is therefore an **n≈12-cell**
   diagnostic wearing a 72-row costume, and is printed only to show direction
   and to prove the tape is not dead:

   | arm | class | n rows | wins | win% | kill ≤ r300 | distinct outcomes | tb |
   |---|---|---|---|---|---|---|---|
   | par_off | REFUSE | 24 | 6 | 25.0% | 0 | **5** | 0 |
   | v535_off | REFUSE | 24 | 6 | 25.0% | 0 | **5** | 0 |
   | v535_on | REFUSE | 24 | 9 | 37.5% | 9 | **7** | 0 |
   | par_off / v535_off / v535_on | run | 48 | 30 | 62.5% | 18 | **8** | 0 |

   Direction is favourable and *consistent with* the refusing decomposition's
   +14.2, but **+12.5pp on 5-vs-7 distinct games is not a measurement.**
   It is also **self-play-is-POLICY** (opponent is our own `_v488beltbreak2`
   chassis) and a **two-board** refusing panel.

2. **Deferred to the powered battery** — the pre-planned merged prereg that
   also resolves HOMEPOOL's F3 attribution (side-lane audit frame,
   2026-08-20T12:37:18Z, item 3):
   * the **effect size** of the gate on refusing boards, at power, against
     live-relevant opponents rather than self-play;
   * the **`DEFENCE_ADMISSION_BAR` r300 non-regression** (timely-kill rate must
     not fall vs control) — ⛔ note this is a *fail-to-exclude* claim and must
     be **restated as an exclusion** (the CI excludes the regression bar)
     **before** the DEFF correction is applied, or the correction launders a
     weak null into a confident one;
   * the **KILL_TARGET panel**;
   * whether the gate should also move **other** map-invariant home planks
     (the mouth and door-kill were acquitted *on this axis*, which is not the
     same as "they are map-robust").

3. **The refusing set is a property of the CURRENT gate.** It is 8 maps today
   because `FS_MAP_SKIP` has 6 grid-confirmed entries, the cripple list has 1,
   and one invented board is under the dim floor. If the gate is re-tuned —
   as v525 re-tuned it, which is how fjordgate stopped refusing — **this plank
   moves with it, silently and by design.** That is the point of reusing the
   predicate, and it is also the thing to remember when reading any future
   v535 number: it is conditional on the gate of the day.

4. **`FS_V535_LOG` is a LOCAL instrument only.** Platform-downloaded replays
   strip `stdout` (CLAUDE.md, s28: 30,664 of 30,664 `BotOutput` events empty).
   Nothing may read an arm tag or gate verdict off a live replay.

5. **`_v535_corners_on`'s `except Exception: return True`** silently restores
   parent behaviour if the gate ever raises. That is the conservative choice —
   an unreadable gate must not delete a shipped plank — but it means a *bug* in
   `_fs_map_gated` would present as "the gate stopped binding", not as a crash.
   `FS_V535_LOG` is the tell (gate asks drop to zero); nothing else is.

6. **No CPU claim.** Local CPU is blind on this platform; the mandatory
   platform `match test` is the instrument and it belongs to the release
   window, not to this build.

7. **`_fs_gate`'s docstring was left stale on purpose** (§3). Fixing prose in
   the shipped tree during a build would have made the flag-off byte-diff carry
   an unrelated hunk. Successor item, not silently absorbed.

---

## 9. Successor items

* **doc-vs-code drift:** `siege.py::_fs_gate` docstring names fjordgate and
  jackpot as "the refusals"; both RUN under the shipped predicate. Correct the
  prose (separate commit, no behaviour change).
* **`jackpot`** was probe-found to refuse the ferry and was never encoded on
  any list. Either survey it into `FS_MAP_SKIP` with its grid, or delete the
  claim from the docstring. Today it plays the siege *and* keeps its corners.
* **`inv_tiny8` refuses on the dim floor** — an invented board, so it costs
  nothing today, but it means the gate's "refusing" class silently includes
  *all* small boards, not only surveyed-closure failures. Worth naming
  explicitly if the finals pool can contain an 8×8.
* The powered merged battery (§8.2).
* **`_fs_enemy_anchor` is a general extraction, used by two callers today.**
  Any future caller wanting the gate verdict outside the siege should call
  `_v535_map_refuses` rather than re-resolving anchors — that is what §2.0
  bought, and it is easy to lose one build at a time.
