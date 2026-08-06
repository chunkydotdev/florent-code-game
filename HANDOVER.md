# Handover — 2026-08-08, after session 6 (ladder phase, tag `ladder1`)

Start here, then [README.md](README.md) → [docs/game-model.md](docs/game-model.md) →
[docs/strategy-log.md](docs/strategy-log.md).

## The one thing to decide

**Apply `bots/_fix_core00` — a five-line change — or don't.** The loop deliberately did not
promote it, because it did not clear the accept gate and promoting it changes the submission
candidate. `bots/_fix_core00` is the current `aug7` **plus** that fix, regenerated after this
session's accept, so it is directly usable as-is.

It fixes a bug that costs us **every single game on `jackpot` when we draw seat A**:

| evidence | before | after |
| --- | --- | --- |
| team A's `titanium_collected` on jackpot, 6 single matches | **0, 0, 0, 0, 0, 0** | 4970, 2480, 4970, 4960, 2480, 4970 |
| jackpot mirror seat split (identical bots both sides) | **0/48 = 0.0%** [0%, 7%] | **22/48 = 45.8%** [33%, 60%] |
| pooled confirm vs the incumbent, 480 matches | — | 51.5% [47.0%, 55.9%] — **no verdict** |
| regression vs `opp_v39`, 240 matches | 65.0% [57.8%, 71.6%] | 62.5% [56.2%, 68.4%] — no regression |

The bug: all 16 comms-store slots start at 0 and hold non-negative integers, so **0 is
indistinguishable from "nobody wrote this yet"**. The Core publishes `write_store(SLOT_CORE_X,
pos.x)`, and builders read it back behind `if x > 0 or y > 0`. On `jackpot` team A's Core sits
at exactly **(0, 0)** — the only Core in the 15-map rotation that does — so every builder on
that team reads "no data" and never learns where home is. Three things are gated on
`core_pos is not None`: the trail conveyor laid in `_try_move` (**the only mechanism that ever
delivers our titanium**), sentinel construction, and heading home. That team therefore builds
harvesters that idle with nowhere to output, lays nothing, defends nothing, and collects
nothing. The fix publishes `x + 1` / `y + 1` and subtracts the offset on read.

**Why the loop didn't just keep it:** the confirm is a no-verdict, and the standing rule is that
a no-verdict is a discard. But the no-verdict was **predicted in writing before the run** —
repairing 1 map out of 15 is worth about +1.7 points pooled, and 480 matches cannot resolve
that. The measurement came back +1.5. This is the same category as **v2's CPU guard, which was
also kept on a no-verdict** as ladder insurance. Recommended: apply. Worth deciding separately
whether `program.md`'s accept rule should gain an explicit per-map correctness clause, because
as written it is structurally blind to any defect confined to a single map.

**Free bonus:** the shipped starter bot has the identical guard, so **most of the field has this
bug too**. `starter` vs `starter` on jackpot leaves seat A with 0 collected, 0 units and 1
building. Any opponent descended from the starter hands us jackpot whenever they draw seat A.

## What changed in the bot

**One accept, promoted into `bots/aug7` (commit `3cfa588`):** the trail conveyor now picks its
facing with `cardinal_toward(src, dst)`, comparing `|dx|` and `|dy|` on the real delta, instead
of snapping an already-quantised 8-way `Direction` through `nearest_cardinal`'s table.
**57.9% [53.5%, 62.3%] over 480 matches** against the pinned previous incumbent; regression vs
`opp_v39` 65.8% [59.6%, 71.5%]; **0 challenger crashes across 1,004 matches**.

**Read the accept honestly: the hypothesis that motivated it was refuted by the same run.** The
argument was that `nearest_cardinal`'s table is a chirality rule that inverts under mirroring,
and that the six mirror maps' seat splits would move toward 50%. They did not — two got worse,
and in the confirm the challenger took **61.1% on the nine rotational maps against 53.1% on the
six mirror ones**, the opposite ordering. What paid was simply pointing trails at the Core, and
it paid most where trails are long and walls dense (archipelago, snowflake, saga are the top
three maps). **The mirror asymmetry is still unfixed**, and `heart` is now its sharpest example.
Do not treat this accept as having closed the equivariance work.

## Ladder telemetry — and the number that reframes everything

Rating **1186.17 → 1205.27** over ~40 minutes (2026-08-06 11:51 → 12:30 UTC), rank **#53 → #52
of 103**, tier crossed from Unranked into **Bronze**. Trend is up.

Four things worth more than the rating:

1. **v40 has played exactly one ladder series, ever** — `1018bf11`, a 3-2 win over Leviathan.
   The team ran 42 submission versions in ~16 hours (several people testing concurrently), so
   **essentially all ladder history describes other people's bots, not ours.** Do not read the
   97-match record as evidence about `aug7`.
2. **`fcode status`'s "Last 10" disagrees with `fcode match list`.** Status said 3W-7L;
   reconstructing the real last ten series three independent ways gives **6W-4L** every time,
   while the `rating` field in the same response is current. Trust `match list`.
3. **We lose Core fights and win economy ones: 15W-74L (17%) on `core_destroyed` across 485
   games, against 51% on the titanium tiebreak.** Against `1337` it is **0W-17L** on core
   kills, across 17 games, with kills landing anywhere from turn 188 to 737 — not a rush.
4. **The #1 team's build, from an unrated scouting replay (`91d77721`, Pivot, ~1947):
   12 harvesters, 39 conveyors, 17 gunners, and zero sentinels.** They out-collected us
   **3170 to 810**. Our bot switches builders to defense at `TARGET_HARVESTERS = 3` and then
   builds sentinels without a cap — a local probe counted **116 sentinels across 10 matches,
   66 in one**, at +20% cost scale each.

**Put (3) and (4) together and the next experiment writes itself:** we are running roughly a
quarter of the winning economy and pouring the difference into turrets that lose their fights
anyway. `TARGET_HARVESTERS` and the absent sentinel cap are the two highest-value levers in the
file, and neither has ever been tested. Note the standing caution though — every previous
attempt to trade economy for *defense* lost, and this points the opposite way, at trading
defense for economy, which is untested territory rather than a re-run.

Worst map on the current rotation: **`saga` 2W-8L (20%)** over 10 games. See
[opponents.md](docs/opponents.md) for per-opponent patterns and the full per-map ladder record.

## What else this session did

1. **Mirror seat audit of the real rotation** (240 matches, `aug7` vs itself, 0 crashes).
   Pooled seat A 51.7% — the harness still reads a no-op as a coin flip. Per map it found
   `jackpot` at **0/16**, and follow-ups at n=48 promoted three sub-threshold flags to real
   ones. The contaminated pre-cutover flags are resolved: `jackpot` confirmed and worse than
   reported, `atoll` confirmed, **`heart` (~83%) refuted outright**. Comparing two *different*
   bots cannot separate a seat split from a strength difference; a mirror run can.
2. **The jackpot wipeout, diagnosed** — see above. Two independent lines of work reached the
   same mechanism, after a plausible competing hypothesis was measured and refuted (that
   `get_position()`'s NW-corner reference is not rotation-equivariant — a real asymmetry that
   turned out not to bind; measuring both core-distance gates to the footprint centre moved no
   map's split at all).
3. **A mirror-equivariance audit of the lineage**, which found two live bugs and established
   several engine facts now in [game-model.md](docs/game-model.md).
4. **A bounded-BFS pathfinder, built and CPU-profiled** in `bots/_dev_bfs` — see below.

## The other live bug the audit found, not yet fixed

**`get_attackable_tiles()` enumerates row-major in absolute map coordinates** (y then x),
regardless of the turret's facing, and `_run_sentinel` fires at the *first* occupied tile it
meets. So **turrets facing N, NE, NW or W engage the farthest enemy on their line, and E, SE, S,
SW the nearest** — an absolute orientation bias that breaks under rotation as well as
reflection, on all 15 maps. Instrumented before committing an experiment to it: ≥2 enemies on
the ray happens in **31% of firing rounds**, but first-hit and nearest actually differ in only
**4%** of enemy-sighting rounds, and that evidence is concentrated in one map and one seat.
When they do differ the gap is large (~30% of the sentinel's range). Verdict: a legitimate cheap
try, not a clear win. Fix is a `min()` on `distance_squared`, not enumeration order.

## Where we are

- **Research bot: `bots/aug7` at `3cfa588`** — the previous incumbent plus this session's one
  accept. **Not submitted.** The ladder still runs **v40** (`a9d81a1`, "aug7-sentinel-economy").
  Freezing into `bots/v5` and submitting are Magnus-only steps.
- **`bots/_fix_core00`** — current `aug7` plus the (0,0) fix, awaiting the decision above.
- **`bots/_dev_bfs`** — a bounded-BFS wall-aware pathfinder, built and profiled but developed
  against the *previous* incumbent, so it needs the accepted change ported in before it can be
  gated attributably. Profile (via `time.process_time()`, because the engine's CPU counter is
  inert locally — see Traps): p50 71us, p99 1398us, **worst case 3785us** at `BFS_NODE_CAP =
  200`, against the 8000us guard. 34 sanity matches, zero tracebacks, and it builds *more*
  infrastructure than the incumbent (94.5 buildings vs 76.7). **Before any CPU-heavy change is
  submitted it needs `fcode match test` on real hardware** — local runs cannot verify the
  budget.
- The evaluation pool is `maps/*.map26`, the real **15-map** weekly rotation. Census is in
  [game-model.md](docs/game-model.md), including that **all 15 declare `symmetry = 0`
  (rotational) and 6 of them are lying** — eider, heart, moonrise mirror across a vertical axis;
  antler, meander, nordkap across a horizontal one. Verify against tiles, never the header.

## The biggest open question, and it is not small

**Four maps have large, reproducible seat asymmetries that nothing yet explains**, measured with
identical bots on both sides so a strength difference is excluded by construction:
**archipelago seat A ~77-88%**, **atoll ~21-31%**, **heart ~31%**, **lighthouse ~28%**. None is
the (0,0) bug, and the NW-corner reference was tested and refuted. Together they are worth
several times what jackpot was. `fjordgate` (10×10, seat A ~69-75%) is separate and is probably
the documented engine first-mover edge showing up at small map size.

**The method that cracked jackpot is the method to use:** stop reading win rates, read the
**per-team process metrics** in the end-of-match JSON, and look for a quantity that is
*structurally* different between seats rather than merely lower. On jackpot the giveaway was
`titanium_collected` being exactly **0** rather than "smaller". Then instrument the one function
that quantity flows through.

Also unexplained, from ladder replays and worth a look at our own code: in `3209e6da` game 3
(`lighthouse`, v35) our bot built **zero** structures across a 102-turn loss while the same
version built 29 conveyors in game 1 of the same series; and in `3d957a49` game 2 (`jackpot`,
v32) we had 3 harvesters alive — the documented sentinel trigger — and built no sentinel.

## Traps

All previous ones still apply (python3 is 3.14 — use `.venv/bin/`; always `--tle 10`; `print()`
goes to the replay, use stderr; `random` is not seeded by `--seed`; never single-seat or pooled
evaluation; the project `CLAUDE.md`/`AGENTS.md` is the organisers' doc with known errors —
game-model.md wins; compare against the incumbent, not `starter`). New this session:

- **The comms store cannot represent a zero.** Anything positional must be published with an
  offset. The file's own `pack_pos()` gets this right for the ore slot; the Core slots did not.
  Assume any other raw `write_store(slot, some_coordinate)` is the same bug waiting.
- **`ct.get_cpu_time_elapsed()` is inert under `fcode run`, even with `--tle 10`** — it read 0
  before and after a loop that `time.process_time()` clocked at 22 ms. Our CPU guard has never
  tripped locally *because the counter never moves*, not because we are fast. Profile with
  `time.process_time()`; only `fcode match test` on Graviton3 really verifies.
- **The bot-code validator rejects `try`/`finally` blocks.** Undocumented anywhere.
- **A pooled win rate cannot see a single-map defect.** A total wipeout on 1 of 15 maps reads as
  ~2 points of drag, inside the noise of any affordable sample. The instrument for this class is
  the **per-map mirror seat table** — re-run it every time the rotation changes.
- **When an outcome is extreme and stable, stop running matches and go read the state.** 0 wins
  in 104 was not a signal to gather more win data; six single matches with the JSON parsed
  answered it.
- **A well-argued arithmetic hypothesis can be completely wrong, and a change can win for a
  reason other than the one you proposed.** Both happened this session, in opposite directions.
  Log the mechanism separately from the number, or the next session tunes the wrong lever.
- **A per-replay observation is only evidence about the submission version that played it.**
  The team ran 42 versions in a day; a "we don't have that bug" conclusion drawn from one replay
  was wrong for exactly this reason.

## Not done

- Daily retro for 2026-08-08 in the dev-knowledge vault.
- Still no `git remote`; `results.tsv` still deliberately untracked.
- Scratch dirs on disk, all untracked and safe to delete: `bots/_incumbent` (stale pin of
  `a9d81a1`), `bots/_diag_core`, `bots/_diag_seat`, `bots/_probe_sent`, `bots/aug7_h1..h4`,
  `bots/_probe_conv`. **Keep `bots/_fix_core00`** until the decision above is made, and
  **`bots/_dev_bfs`** until the pathfinder is gated.
