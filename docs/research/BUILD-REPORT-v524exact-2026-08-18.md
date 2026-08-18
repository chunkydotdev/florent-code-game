# BUILD REPORT — `bots/_v524exact`, s51, 2026-08-18

Micro-build, two changes, from frozen parent `bots/_v522floor` (commit
`8dd6f936`, `Tue Aug 18 15:20:31 2026 +0200`). Parent-freeze digests in
`scratchpad/s51_v524_build/PARENT_FREEZE.md5`, verified to match the digests
`docs/prereg/PREREG-PINCERPOOL-2026-08-18.md` recorded at draft (all 5
modules). Tree is uncommitted, per instruction. Wall clock at write time
`2026-08-18T15:31:53Z` (`date -u`, same shell call).

Read first: `docs/prereg/PREREG-PINCERPOOL-2026-08-18.md` findings 2 ("THE
THIRD THING", the cripple-signature collision) and blocker B1 (the
`FS_V522_FLOOR` description discrepancy).

## THE TWO CHANGES

**CHANGE 1 — the cripple list matches EXACTLY `{midgard, yulerune}`.**
`FS_V519_CRIPPLE_MAPS` keys on `(w, h, min(core), max(core))`, the same
signature `FS_MAP_SKIP` uses because no map name reaches a bot. Two OTHER
pool maps share that signature with the two the comment names:

```
(30, 30, (2,2), (26,26))  ->  midgard   AND  ragnarok
(20, 20, (2,9), (16,9))   ->  yulerune  AND  frostgate
```

Computed independently with `tools/map_encode.parse_map26` over every
`maps/*.map26`, and re-verified at this build: a fresh `encode()` of all four
maps is byte-identical to the committed `EXTRA_MAP_CODES` strings
(`doctrine.py:1164,1167,1168,1171`), and `encode(midgard) != encode(ragnarok)`,
`encode(yulerune) != encode(frostgate)` — the discriminator exists in the tile
grid even though it doesn't exist in the coarse signature.

**The fix reuses the house mechanism, no new one.** `eco.known_map_for`
already disambiguates every other same-`(w,h,anchor)` collision this tree
ships (eider/heart, the two 26×26s) by confirming a coarse candidate against
the sensed tile grid. `siege.py`'s `_fs_map_gated` now does the same: a coarse
`sig519` hit is a CANDIDATE, confirmed against `self.map_grid` (or, on the one
caller that never gets one — the v516 turret beat, whose `self.core` is None
by design — a fresh `known_map_for(mw, mh, ours, ct)` call, used locally and
**not cached**, see the correctness note below) before it's allowed to refuse
a map. The two reference grids (`FS_V524_CRIPPLE_GRIDS`, `siege.py`) are
`eco._decode_grid` applied to the exact `EXTRA_MAP_CODES` strings already
committed for `# midgard` and `# yulerune` — copied programmatically from
`doctrine.py`, not retyped, and cross-checked against a fresh `map_encode.py`
run on `maps/midgard.map26` / `maps/yulerune.map26`.

Flag: `LOKI_FS_V524` (doctrine.py, appended block). `False` reproduces the
parent's coarse-only collision exactly — this is the registered mutant, not a
hypothetical: the 15-map predicate table below drives it both ways.

**⛔ A CORRECTNESS BUG FOUND AND FIXED DURING VERIFICATION, WORTH RECORDING.**
The first draft cached the confirmed grid into `self.map_grid` from inside
`_fs_map_gated`. That attribute is *also* the guard on `main._builder`'s own
map init (`main.py:1325`, `if self.map_grid is None: self.map_grid =
known_map_for(...)`, followed by the walls/ores extraction at 1327-1341) —
and on the round a builder's `self.core` first resolves, the v521 gatefix
crew-seat read (`main.py:1283`, `_fs_gate`) runs **before** that init block.
Caching there made line 1325's guard false before the walls/ores extraction
ever ran, silently losing `self.map_walls`/`self.map_ores` for that unit for
the rest of the match — found because a midgard byte-identity spot-check
(seed 524919 vs `bots/_v488beltbreak2`) that should have been a no-op instead
diverged at r280 into a completely different, much longer game (winner
flipped, unit counts diverged 6 vs 17). Bisected to this exact interaction by
isolating Change 1 alone (Change 2 confirmed inert, see below), reproducing
it minimally, then removing the cache write — after which the byte-identity
check below passed clean. The shipped code recomputes on every early ask
rather than caching, which costs a repeat `known_map_for` call (cheap:
tile-sense + compare, no re-decode, `_decode_grid` is cache-memoised) only on
the 2 (this build) / 4 (parent) colliding-signature maps, only before the
official init resolves it.

**CHANGE 2 — `FS_V522_FLOOR = False` at its definition site (doctrine.py).**
Description-alignment only. The v522 build's own `KILL_TARGET` panel measured
`FS_V522_FLOOR` ON vs OFF at 733/1080 == 733/1080 (+0.00pp,
`BUILD-REPORT-v522floor-2026-08-18.md:282,293`) — **measured indifferent**,
not a plank that pays or costs. This aligns the tree with the commissioning
brief's own description ("pincer + leakfix + PHASE_HONEST, sync/floor off")
that `_v522floor` itself shipped contradicting (PREREG blocker B1). Verified
inert on the fixture that matters here too: an isolated floor-only arm
(`LOKI_FS_V524` absent, `FS_V522_FLOOR=False`) played byte-identical to the
true parent on midgard, same seed (`scratchpad/s51_v524_build/dbg/midgard_floorfalse.replay26`)
— the flag is gated behind `fs_ph == FS_PH_KILL_NEAR`, which a refusing/gated
map's raider never publishes, so it cannot fire there regardless of its
value.

No master flag needed beyond `LOKI_FS_V524` (Change 1); Change 2 is a
constant, documented, not flagged.

## (a) THE 15-MAP PREDICATE TABLE, BOTH WAYS

`scratchpad/s51_v524_build/predicate_table.py` — imports the real
`SiegeMixin._fs_map_gated` from the built tree (monkeypatching only
`LOKI_FS_V524`), drives it against all 15 pool maps parsed fresh from
`maps/*.map26`, with a fake `ct` that senses the WHOLE board (the strongest
offline test the harness can give the disambiguation).

```
LOKI_FS_V524 = True  (exact match, shipped):
  antler         GATED       archipelago    GATED       fjordgate      GATED
  auroraveil     siege-active  drakkarfjord siege-active  drumlin      siege-active
  frostgate      siege-active  glacierkeep  siege-active  icefloe      siege-active
  midgard        CRIPPLE       nordkap      siege-active  ragnarok     siege-active
  royale         siege-active  valkyrie     siege-active  yulerune     CRIPPLE
  CRIPPLE-refused (excl. GATED): [midgard, yulerune]   <- EXACT MATCH, as required

LOKI_FS_V524 = False (mutant, parent's coarse-only match):
  same GATED set; CRIPPLE-refused (excl. GATED): [frostgate, midgard, ragnarok, yulerune]
  <- re-selects all 4, reproducing the registered bug
```

Both verdicts hold: exact-match selects `{midgard, yulerune}` only; the mutant
re-selects the 4-map collision. Full per-map table in the script's stdout.

## (b) DETERMINISTIC BYTE-IDENTITY, NOISE OFF, SEED 524919

Method: the v518 method (`BUILD-REPORT-v518fastsent-2026-08-18.md` finding
2) — `NOISE_ON = False` on **both** sides (ours and the opponent,
`bots/_v488beltbreak2`; `--seed` alone does not pin a game, s515/v518
finding), `--tle 0`, replay bytes `cmp`'d. Opponent: a `NOISE_ON=False` copy
of `bots/_v488beltbreak2` (`scratchpad/s51_v524_build/eq_opp`), both seats.

| map | status | v524 vs parent |
|---|---|---|
| midgard | CRIPPLE (both trees) | **IDENTICAL**, both seats |
| yulerune | CRIPPLE (both trees) | **IDENTICAL**, both seats |
| archipelago | GATED (both trees, unaffected by Change 1) | **IDENTICAL**, both seats |
| ragnarok | was CRIPPLE (bug), now siege-active | **DIFFERS**, both seats |
| frostgate | was CRIPPLE (bug), now siege-active | **DIFFERS**, both seats |

6/6 on the three maps where the plank's behaviour must not move. 4/4 differs
on the two reclaimed maps, confirming the plank now actually runs there
rather than differing by coincidence. Re-run against the final shipped tree
(`scratchpad/s51_v524_build/byte_check_final/`) after the correctness fix
above, same result.

**Siege-path confirmation on the reclaimed maps** (instrumented copy,
`FS_LOG=FS_V519_MODE_LOG=FS_V524_LOG=True`, `--tle 10`, seed 524919 vs
`bots/_v488beltbreak2`): `V524 ... confirmed False` on every gate ask on both
maps (correctly NOT cripple), and siege-path log lines fire abundantly —
ragnarok: 11 SEAL, 1 SENTINEL, 10 THROW, 1 EVICT, 11 RUNG, 5 PHASE; frostgate:
9 SEAL, 1 SENTINEL, 1 THROW, 25 EVICT, 32 RUNG, 6 PHASE. The plank runs.

`.err` sweep across all games this build ran (byte-identity, instrumented,
outcome, flag-off — 400+ games): 0 tracebacks.

## (c) OUTCOME READ ON THE TWO RECLAIMED MAPS, n=60/map

`scratchpad/s51_v524_build/outcome_battery.py` — v524 vs `bots/_v488beltbreak2`
INTERLEAVED with v522floor(parent) vs the same opponent, PAR=4, seat-balanced,
seed base 524200 (local-only, no platform/shard collision). **A direction
read at ±12pp, reported as such, not a locked battery.**

| map | v524 | parent | delta |
|---|---|---|---|
| ragnarok | 39/60 (65.0%) | 41/60 (68.3%) | **-3.3pp** |
| frostgate | 37/60 (61.7%) | 31/60 (51.7%) | **+10.0pp** |

MAPSEG's registered prior (`doctrine.py:3881-3886`) classifies ragnarok as
RUSH-quadrant (rush-mode dpp +11.23 vs its tape mean) and expected reclaiming
it to read positive; frostgate was expected ≈neutral. **Observed: ragnarok
reads slightly negative rather than the expected +11, frostgate reads
positive rather than neutral — both numbers sit inside the ±12pp band this
n=60 buys, so neither is distinguishable from the MAPSEG prior or from zero
at this sample size.** Reported as a direction read only; a currency verdict
on either map needs a pooled window, not this single n=60 draw (per the
project's one-draw-law and the pooling standard).

## (d) AST DERIVED-DEFAULT SCAN AND FLAG-OFF BEHAVIOURAL CHECK

**AST scan**, `scratchpad/s51_v524_build/flagoff_ast.py` (extended from
`scratchpad/s51_v522_build/flagoff_ast.py`, same method, same guard):
scans `doctrine.py` for module-level statements (or module-level `if` tests)
reading `LOKI_FS_V524` or any v524 constant — the v515 same-file
append-ordering hazard (`mkarm.sh` appends arm overrides to the END of
doctrine.py). Guard driven both ways (positive/negative/if-form synthetic
controls, all correct) plus the known real-case positive control
(`FERRY_HOME_ON` reading `FS_CREW_ON`/`LOKI_FS_CREW`, 2 hits, confirms the
scanner isn't blind to the real defect class). **Result: 0 v524 hits, 0 on
every inherited flag set (v518-v522). PASS.**

*(Scanning the OTHER modules for the same names was tried and dropped: it
flagged `siege.py`'s `FS_V524_CRIPPLE_GRIDS = frozenset((_decode_grid(
FS_V524_MIDGARD_CODE, ...), ...))` as a false positive — a cross-file
constant reference is safe by construction, since `siege.py` only sees
`doctrine.py` after it has fully executed, override included. The v515
hazard is specifically same-file, pre-append. Scope reverted to doctrine.py
only, matching the precedent tool.)*

**Flag-off behavioural check, n=90**,
`scratchpad/s51_v524_build/flagoff_battery.py`: `LOKI_FS_V524=False` arm vs
`bots/_v488beltbreak2`, interleaved with the true parent v522floor vs the
same opponent, full 15-map pool, 3 seeds × 2 seats/map = 90 games/arm,
PAR=4, seed base 524500 (distinct block from (c)'s).

```
flagoff       n=90  wins=61  (67.8%)
v522(parent)  n=90  wins=65  (72.2%)
DELTA -4.4pp   (well inside n=90 noise)  0 parse-fails, 0 tracebacks
```

Corroborates the AST scan with a real win-rate read: no dramatic behavioural
split between the flag-off arm and the true parent.

## ARTIFACTS

- Tree: `bots/_v524exact/` (uncommitted). `doctrine.py`, `main.py`, `siege.py`
  touched; `eco.py`, `raid.py` byte-identical to parent (md5 confirmed).
- `scratchpad/s51_v524_build/PARENT_FREEZE.md5` — parent digests, matches the
  prereg's recorded values.
- `scratchpad/s51_v524_build/predicate_table.py` — (a).
- `scratchpad/s51_v524_build/eq_v524/`, `eq_v522/`, `eq_opp/`,
  `eq_v524_final/`, `byte_check/`, `byte_check_final/` — (b) fixtures and
  replays (NOISE_ON=False debug copies, not the shipped tree).
- `scratchpad/s51_v524_build/dbg/` — the bisection trail for the correctness
  bug found and fixed during (b): isolation arms (`eq_v524_onlyc1*`,
  `eq_step2`, `eq_step3`, `eq_noop`, `eq_v522_floorfalse`), instrumented logs,
  and the fixed re-run (`midgard_fixed.*`).
- `scratchpad/s51_v524_build/outcome_battery.py`, `outcome_battery/`,
  `outcome_battery.log` — (c).
- `scratchpad/s51_v524_build/flagoff_ast.py` — (d) AST scan.
- `scratchpad/s51_v524_build/flagoff_arm/`, `flagoff_battery.py`,
  `flagoff_battery_out/`, `flagoff_battery.log` — (d) behavioural check.

0 tracebacks across every game this build ran. Ready for builder ratification
and the PINCERPOOL shard to fire on this tree.
