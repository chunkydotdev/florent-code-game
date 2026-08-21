# BUILD REPORT — `bots/_v602skalman` (navigation + cage-order fixes, tape601-autopsy-grounded)

**Builder s54, 2026-08-21 ~19:2xZ.** Copy of `_v601skalman` + 6 fixes, each tied to a
measured cause in `scratchpad/s54_autopsy601/tape601_autopsy.md`. Fresh opus build agent;
artifacts `scratchpad/s54_v602/`. No submit, no platform matches. Verification per the
established standard (static scans with DIRTY controls · aliveness with a driven
injected-error control · named regression cells · per-fix ablations · fidelity spot-read).

## Fixes
1. **SK_CAGE_FIRST** — the lap outranks `_peck_priority`; the enemy core is OFF the
   walker's peck ladder while seal tiles remain (the 1534 cause). Two disclosed
   measurement-forced extensions: off-lap eviction of an adjacent occupied seal tile,
   and lap re-entry on blocked pool target.
2. **SK_DANGER_NAV** — movement penalty over remembered enemy turret RAYS (armed_memo
   finally has a mover consumer); forbidden unless no safe step, detour budget 6.
3. **SK_CYCLE_BREAK** — A-B-A-B detection (4-entry ring), perpendicular break, hold if
   none; second trigger in `_escape` (capped 2).
4. Footprint-aware `_enemy_builder_adjacent` (2×2 core) — bugfix, no flag.
5. **SK_SENSE_NAV** — BFS floods sensed terrain instead of degrading to greedy when
   `known_map_for` is None; every role now `_ore_scan`s (walker/engineer had empty wall
   sets). **5b:** `_pick_nest` un-gated from `map_grid` (+watchdog) — rides SK_NEST.
6. `lattice_floor` unconditional in `_drip` — bugfix, no flag.

## Results on the named cells (same 6-map/both-seat aliveness fixture as v601's)
* **Storm cell (fimbulwinter A): 42 builders/39 deaths on one tile/25-round metronome →
  4 builders, 0 deaths, core-kill WIN r141** (was r1000 tiebreak).
* **Walker cell (glacierkeep A): ring barriers 2→7 (7 of 8 seats), worst dwell 42→3,
  core pecks 43→0, r311 loss → core-kill r228.**
* **Pooled 6 games: 0 kills + 1 r1000 (v601) → 3 core kills (r141/r283/r228, ALL inside
  r300), 0 r1000 games.** Builder deaths 41→7 · ring barriers/game 0→3.167 · enemy-core
  pecks 1,029→0 · 2-cycle step share 74.2%→19.7% · 0 tracebacks/0 exception removals
  (injected-NameError control fires).
* Fidelity spot-read: drip lattice 96.8→**100.0** (259/259) · M2a 0→52.8% · M7 0→10% ·
  **nest on grid-None maps 0,0,0,0 → 2,2,1,1 sentinels while grid-confirmed maps stay
  flat — the fix touches exactly the maps it should.**
* yggdrasil BFS cost: 220 µs/call worst-case stub timing (≤2 calls/turn ⇒ ≤4.4% of the
  10 ms budget); local CPU stays blind — **platform `match test` owed before exposure.**

## Ablations (one flag off each)
SK_CAGE_FIRST off → core pecks 0→15, dwell 3→14 (direction reproduces; damped because
fixes 2/3/5 remove the parking v601 had) · SK_CYCLE_BREAK off → cycle share 19.7→41.5% ·
SK_SENSE_NAV off → cycle 41.0%, ring barriers 1.167, fimbulwinter back to r1000 ·
**SK_DANGER_NAV off → NULL on the fixed chassis** (its signature needs a lingering body);
demonstrated CONDITIONALLY on the cycle-break-off chassis (deaths 3→7, all turret kills)
— reported as conditional, not clean.

## Engine fact banked (correcting the tape601 autopsy's latent note)
**A builder bot CAN walk onto a friendly CONVEYOR tile** — measured in-game (glacierkeep
r200: conveyor tile `is_tile_passable=True, can_move=True`; harvester tile False/False).
The wrong assumption cost a 250-round keeper freeze in an intermediate build; reverted
with the measurement recorded at the site. Conveyors/splitters are passable to friendly
builders; harvesters are not.

## Residuals (v603 candidates, none fixed here)
1. `_escape`'s `free_neighbours == 0` path can demolish a full-HP just-built door gunner
   (v601 residual #4, recurred and instrumented; absent from the final battery, unfixed).
2. Idle parking when a role's verb runs out of work (keeper 176-round dwell yggdrasil;
   engineer holds the nest).
3. `_threat_scan` counts a BARRIER as a home threat → the denier pecks walls (157
   barrier pecks glacierkeep).
4. Fixture caveat: one authored NOISE_OFF opponent; prioritises, does not establish
   field prevalence.
