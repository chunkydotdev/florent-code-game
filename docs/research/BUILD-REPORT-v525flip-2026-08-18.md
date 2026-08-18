# BUILD REPORT — `bots/_v525flip`, s51, 2026-08-18

Micro-build, two changes, one master flag, from frozen parent `bots/_v524exact`
(tracked, clean at freeze). Parent-freeze digests in
`scratchpad/s51_v525_build/PARENT_FREEZE.md5`. Tree is uncommitted, per
instruction. PAR=2 throughout (the PINCERPOOL shard owns the cores). Wall
clock at write time `2026-08-18T17:53:27Z` (`date -u`, same shell call).

Read first: `docs/coordination.md` tail note ~2026-08-18T17:08:11Z
("FORCEALL banked — MAGNUS'S QUESTION FINDS +4.6 POOLED POINTS IN STALE
STANDDOWNS") and its source data, `scratchpad/s51_forceall/results.tsv`.

## THE TWO CHANGES (one flag, `LOKI_FS_V525`; `False` reproduces the parent)

**Basis, both changes.** Magnus asked whether the rush performs better than
the standdown thresholds assume, now that it carries pincer/funding/door-off/
terminal-hop the v510/v513-era thresholds were never calibrated against. The
FORCEALL probe (scratch copy of `_v524exact` with every threshold zeroed at
definition-site, n=90/map vs `bots/_v488beltbreak2`, PAR=2) answered it:

```
yulerune    91.1% [+-5.9]  n=90   (mirror 50.0; best cell anywhere)
antler      64.4%          n=90
fjordgate   63.3%          n=90   (10x10, core d^2=32; 0 tracebacks)
midgard     40.0%          n=90   -- below the mirror, correctly stays cripple
archipelago 17.8%          n=90   -- well below the mirror, gate validated
```

Three of five stood-down maps clear the 50% mirror with room; two do not.
This build flips only the three that clear it, and leaves midgard and
archipelago exactly as the parent treats them.

**CHANGE 1 — yulerune leaves the cripple list.** `FS_V519_CRIPPLE_MAPS` (the
coarse `(w,h,anchor)` signature set) carries two signatures: midgard's
(shared with ragnarok) and yulerune's (shared with frostgate). A new
`FS_V525_CRIPPLE_MAPS` (doctrine.py) contains only midgard's signature —
yulerune's is *deliberately absent*. `siege.py`'s `_fs_map_gated` selects
between the two sets at **runtime** (`FS_V525_CRIPPLE_MAPS if LOKI_FS_V525
else FS_V519_CRIPPLE_MAPS`), never at module scope, so yulerune (and
frostgate, which shares its signature and was already reclaimed by v524's
exact-grid match) never reach the CRIPPLE test at all — both play
siege-active. Midgard's signature is untouched: it still measures 40.0%
(stays crippled) and v524's exact-grid disambiguation against ragnarok is
unaffected.

**CHANGE 2 — antler + fjordgate un-gated.** `FS_MIN_MAP_DIM` (12) and
`FS_MIN_CORE_DSQ` (72) are v510-era thresholds, calibrated against a
fjordgate loss (`_fs_gate`'s own comment) the current rush does not
reproduce. Two new constants, `FS_V525_MIN_MAP_DIM` and
`FS_V525_MIN_CORE_DSQ`, are **derived from the two maps' own measured
geometry, at the tightest values that admit both** — not zeroed:

```
                    map size   core d^2   (tools/map_encode.parse_map26)
fjordgate            10x10       32       cores (2,2)/(6,6): dx=4,dy=4
antler               14x18       64       cores (6,4)/(6,12): dx=0,dy=8
```

fjordgate is the binding map on **both** axes (smaller board, closer cores),
so its own values are exactly the minimal admitting thresholds:

```
FS_V525_MIN_MAP_DIM  = 10   (fjordgate's own larger side; a 9x9 or smaller
                             board is still refused)
FS_V525_MIN_CORE_DSQ = 32   (fjordgate's own core d^2; anything closer is
                             still refused)
```

The gate's `<` comparison means fjordgate passes at its own boundary (`10 <
10` and `32 < 32` are both `False`) rather than by a margin that would also
sweep in smaller/closer maps nobody has measured — the mechanism stays
meaningful for genuinely degenerate future maps. archipelago is **unaffected**
by this change: it is refused by `FS_MAP_SKIP` (a different, closure-based
mechanism), not by the dim/dsq gate, and stays gated at 17.8%. Same runtime
selection pattern as Change 1 (`FS_V525_MIN_MAP_DIM if LOKI_FS_V525 else
FS_MIN_MAP_DIM`, read inside `_fs_map_gated`, never at module scope).

Flag: `LOKI_FS_V525` (doctrine.py, appended block after the v524 block).
`False` reproduces the true parent's standdown set exactly: GATED =
`{antler, archipelago, fjordgate}`, CRIPPLE = `{midgard, yulerune}` — the
registered mutant, driven both ways below.

Only `doctrine.py` and `siege.py` differ from the parent; `eco.py`, `main.py`,
`raid.py` are byte-identical (md5-confirmed).

## (a) THE 15-MAP PREDICATE TABLE, BOTH WAYS

`scratchpad/s51_v525_build/predicate_table.py` — imports the real
`SiegeMixin._fs_map_gated` from the built tree (monkeypatching only
`LOKI_FS_V525`), drives it against all 15 pool maps parsed fresh from
`maps/*.map26`, fake `ct` senses the whole board.

```
LOKI_FS_V525 = True  (standdown flip, shipped):
  GATED:   ['archipelago']
  CRIPPLE: ['midgard']
  (all other 13 maps, including antler/fjordgate/yulerune, siege-active)

LOKI_FS_V525 = False  (mutant: true parent bots/_v524exact):
  GATED:   ['antler', 'archipelago', 'fjordgate']
  CRIPPLE: ['midgard', 'yulerune']
```

Both verdicts hold exactly: `V525=True` stands down only `{archipelago}` (via
`FS_MAP_SKIP`, unchanged) plus `{midgard}` (via the narrowed cripple set);
`V525=False` reproduces the parent's five standdowns digit-for-digit.
`PREDICATE TABLE OK, both directions.`

## (b) DETERMINISTIC BYTE-IDENTITY + DIFFERENCE, NOISE OFF, SEED 525919

Method: the v524/v518 method — `NOISE_ON = False` on **both** sides (ours and
the opponent, `bots/_v488beltbreak2`), `--tle 0`, replay bytes `cmp`'d.
Fixtures: `scratchpad/s51_v525_build/eq_v525` (treatment), `eq_v524` (true
parent, NOISE_ON off), `eq_opp` (opponent, NOISE_ON off).
`scratchpad/s51_v525_build/byte_identity.py`.

| map | status | v525 vs true parent |
|---|---|---|
| drakkarfjord | siege-active (both trees, unaffected) | **IDENTICAL**, both seats |
| midgard | CRIPPLE (both trees, unaffected) | **IDENTICAL**, both seats |
| archipelago | GATED (both trees, via FS_MAP_SKIP, unaffected) | **IDENTICAL**, both seats |
| yulerune | was CRIPPLE, now siege-active | **DIFFERS**, both seats |
| antler | was GATED, now siege-active | **DIFFERS**, both seats |
| fjordgate | was GATED, now siege-active | **DIFFERS**, both seats |

6/6 identical on the three maps this build must not touch; 6/6 differs on the
three flipped maps, confirming the plank now actually runs there rather than
differing by coincidence. `RESULT: PASS`.

**Siege-path confirmation on the three flipped maps** (instrumented copy,
`FS_LOG=True`, `--tle 10`, seed 525919 vs `bots/_v488beltbreak2`,
`scratchpad/s51_v525_build/siegepath/`): every `FS GATE` line reads
`ok 1` with the correct signature (e.g. `sig (10, 10, (2, 2), (6, 6)) ok 1`
for fjordgate), and siege-path log lines fire abundantly on all three:

```
yulerune:  63 GATE, 22 PHASE, 11 SEAL, 8 RUNG, 4 THROW, 4 EVICT, 1 SENTINEL, 1 DODGE, ...
antler:    65 GATE, 30 EVICT, 22 RUNG, 7 SEAL, 6 PHASE, 1 SENTINEL, ...
fjordgate: 1754 GATE, 62 STAT, 6 PHASE, 5 SEAL, 3 RUNG, 2 SENTINEL, 2 DODGE, ...
```

SEAL, SENTINEL, THROW/EVICT, RUNG, PHASE all fire on all three maps. 0
tracebacks across the full `.err` sweep of every game this build ran (387
replays; predicate table, byte-identity, siege-path, direction reads,
flag-off — recursive grep for `Traceback` across all `scratchpad/s51_v525_build`
`.err`/log output: **0 hits**).

## (c) DIRECTION READ, n=60/map, THE THREE FLIPPED MAPS

`scratchpad/s51_v525_build/direction_read.py` — v525 vs
`bots/_v488beltbreak2`, PAR=2, seat-balanced (30/30), seed base 525200
(local-only, no shard collision). A direction read at ~±13pp (n=60), not a
locked battery — reported as such, per the project's one-draw-law/pooling
standard. Compared against the FORCEALL probe's n=90 basis (same rush
chassis, forced open there vs reached through the real gate here).

| map | v525 (n=60) | forceall basis (n=90) | delta |
|---|---|---|---|
| yulerune | 58/60 (96.7%) | 91.1% | **+5.6pp** |
| antler | 38/60 (63.3%) | 64.4% | **-1.1pp** |
| fjordgate | 45/60 (75.0%) | 63.3% | **+11.7pp** |

All three read inside the ±13pp band the sample size buys; no build-breakage
signal (no regression toward or below the 50% mirror on any map).
`parse-fails=0, tracebacks-in-stderr=0, total=180`. fjordgate's positive
delta (+11.7pp) sits at the edge of the band — worth a pooled re-read before
any currency claim, not a defect of this build (same one-draw caveat the
forceall numbers themselves carry).

## (d) AST DERIVED-DEFAULT SCAN AND FLAG-OFF BEHAVIOURAL CHECK

**AST scan**, `scratchpad/s51_v525_build/flagoff_ast.py` (extended from
`scratchpad/s51_v524_build/flagoff_ast.py`, same method, same guard): scans
module-level statements/conditionals reading `LOKI_FS_V525` or any v525
constant, plus every inherited flag set (v518–v524, CREW). Guard driven both
ways (positive/negative/if-form synthetic controls, all correct) plus the
known real-case positive control (`FERRY_HOME_ON` reading
`FS_CREW_ON`/`LOKI_FS_CREW`, 2 hits — confirms the scanner isn't blind to the
real defect class).

Scope is `doctrine.py` only, matching the v524 precedent tool exactly: an
initial run against `siege.py` too reproduced the SAME known false positive
v524's report already documents (`FS_V524_CRIPPLE_GRIDS` reading
`FS_V524_MIDGARD_CODE`/`FS_V524_YULERUNE_CODE` at module scope — a
cross-module constant-to-constant reference, safe by construction, not a
flag-ordering hazard). Reverted to the precedent's scope.

**Result: 0 v525 hits, 0 on every inherited flag set. PASS.**

**Flag-off behavioural check, n=90**,
`scratchpad/s51_v525_build/flagoff_battery.py`: `LOKI_FS_V525=False` arm
(`scratchpad/s51_v525_build/flagoff_arm`, definition-site override) vs
`bots/_v488beltbreak2`, interleaved with the true parent `bots/_v524exact` vs
the same opponent, full 15-map pool, 3 seeds × 2 seats/map = 90 games/arm,
PAR=2, seed base 525500 (distinct block from (c)'s).

```
flagoff      n=90  wins=62  (68.9%)
v524parent   n=90  wins=58  (64.4%)
DELTA +4.5pp   (well inside n=90 noise)  0 parse-fails, 0 tracebacks
```

Corroborates the AST scan: no dramatic behavioural split between the flag-off
arm and the true parent.

## ARTIFACTS

- Tree: `bots/_v525flip/` (uncommitted). `doctrine.py`, `siege.py` touched;
  `eco.py`, `main.py`, `raid.py` byte-identical to parent (md5-confirmed).
- `scratchpad/s51_v525_build/PARENT_FREEZE.md5` — parent digests.
- `scratchpad/s51_v525_build/predicate_table.py` — (a).
- `scratchpad/s51_v525_build/eq_v525/`, `eq_v524/`, `eq_opp/`,
  `byte_identity.py`, `byte_check/` — (b) fixtures, script, replays/err.
- `scratchpad/s51_v525_build/inst/`, `siegepath/` — (b) instrumented
  siege-path confirmation (`FS_LOG=True` copy + logs/replays).
- `scratchpad/s51_v525_build/direction_read.py`, `direction_read/`,
  `direction_read.log` — (c).
- `scratchpad/s51_v525_build/flagoff_ast.py` — (d) AST scan.
- `scratchpad/s51_v525_build/flagoff_arm/`, `flagoff_battery.py`,
  `flagoff_battery/`, `flagoff_battery.log` — (d) behavioural check.

0 tracebacks across every game this build ran (387 replays total). Ready for
builder ratification and the FLIPPOOL prereg to fire on this tree.
