# BUILD REPORT + FIDELITY READ — `bots/_v603skalman` (kill planks, tape602-autopsy-grounded)

**Builder s54, 2026-08-21 ~20:5xZ.** Copy of `_v602skalman` + 8 flags (~600 net lines).
Fresh opus build agent; artifacts `scratchpad/s54_v603/` (incl. the full ablation matrix
and the 30-game comparison tape `tape_FINAL2/`, whose outcome column the builder
re-derived independently: 8 core-kills + 1 tiebreak, matching). Instrument `sig603.py`
reproduces the tape602 autopsy digit-for-digit before any v603 read (875 shots / kills
6-30 with identical rounds / collar pecks 2,158 vs 2,179). No submit, no platform
matches, no game-share claim; fixture = the authored NOISE_OFF benchmark copy throughout.

## Shipped fixes (each single-flag ablatable; ablations RE-RUN on the shipped chassis)
* **SK_NEST_PAIR** — second band sentinel, drip-funded (no burst-bank). Slot 7 extended
  in-slot (second site as dx/dy relative to first; one writer preserved).
* **SK_TRUNK_NEAR** — near-trunk (d²≤13) + terminus tiles INCLUDED in gun coverage
  (inverting SK_TRUNK_DSQ's exclusion — 55/63 of tape602's belt deaths lived there).
* **SK_EVICT_ARMED** — the `not empty_seals` interlock dropped; enemy delivery conveyors
  on seal seats are evictable. **Produced the line's first FULL SEALS (icefloe 8/8 both
  seats on an intermediate tape; tape602 read 0/30 ever).**
* **SK_COLLAR_GUNS** — collar pecking stopped at the source: `_home_defence` skips
  barriers (the driver), peck budget capped 15/barrier with the healing-race rule.
* FIX 6 (lap-never-ran diagnosis, 3 classes): B (period-6-10 lap livelock) and C (enemy
  spawn-box; `can_spawn` is legality not liveness) FIXED (SK_LAP_ADJ_SEAL /
  SK_SPAWN_EXIT / SK_IDLE_ACT); **class A (danger-veto throat) DEFERRED to v604** —
  needs danger-as-path-cost inside BFS.

## Shipped OFF — two measured negatives, recorded with their reversals
* **SK_COLLAR_ROUTE_GATE off:** as briefed it LOST kills and delivery (bifrost A 2,470 →
  400 Ti) — the terminus pecks were BUYING delivery; root cause: `belt_built` is
  per-unit state, so a replacement keeper misreads the chain. ⚠ The ablation's SIGN
  FLIPPED after FIX 6 repaired the walker (collar_off now costs 5 kills) — **ablation
  direction was chassis-dependent; re-run, never reuse.**
* **SK_CAGE_CEIL off:** the dynamic ceiling works mechanically (at-bar rounds 52→1,062)
  and COSTS 2 kills/30 — the tape's own two findings predict it (walker pecks = 0% of
  core damage; the cage's worth is healer denial, heal-tax 0.49 vs 0.71). One line from
  live if evidence changes.

## The 30-game read (builder-verified outcome column; v602 same fixture in brackets)
Kills **8/30 [6/30]**, by-r300 6/30 [5/30], median kill round r256 [r198 — LATER; the
KILL_TARGET median-r180 gap is real and named] · our core destroyed 21/30 [23/30] ·
near-trunk coverage 14.4% [2.0%] · belt deaths 34 [60], terminus deaths 26 [50] · collar
pecks 12.0/game [71.9] · seal evictions 30 [6] · sentinel shots 1,144 [875], ≥2-sentinel
share 53.3% [53.3%] · M1 41.9/34.4 [17.5/33.3] · drip lattice 100.0 both seats · M4
band 95.8/96.0, point-blank 0 · M2d ring held median 3 [3]. Deviation noted: M3e
first-convert r14/15 (target r27.5) — FIX 2 buys guns earlier.

## Ablation matrix (all both-ways on the shipped chassis)
nestpair_off: ≥2-share 53.3→13.3%, kills 8→4 · trunknear_off: coverage 23/160→5/139,
belt deaths 34→53, kills 8→4 · evict_off: evictions 30→1, kills 8→5 · collar_off: pecks
359→1,544, kills 8→3 · lapadj_off: held 3→2, belt deaths 34→57 · spawnexit_off: kills
8→6 · ceil_on: kills 8→6 · **idleact_off: EXACT NULL (pre-empted by spawn-exit; kept as
insurance, reported as a null).**

## FIRST-CONTACT GATE: **NOT MET.** 8/30 does not beat the local screen. Trend across
the founding day: 0 → 0 → 6 → 8 core-kills on the identical fixture.

## v604 queue (agent-named, evidence-priced)
1. Danger as a PATH COST in `_bfs_direction` (class A throat; the veto+detour form
   measurably cannot cross a covered row). 2. Period-k cycle detection (class B stalls
   are period 6-10; SK_CYCLE_BREAK sees only 2). 3. ONE lap cursor — `_cage_walker`
   carries two targeting systems that disagree by construction. 4. A `belt_built`
   estimator that survives body replacement (re-opens SK_COLLAR_ROUTE_GATE honestly).
Owed before ANY exposure: platform CPU `match test` (local CPU blind; wall-clock proxy
+0.1% vs v602).
