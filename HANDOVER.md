# Handover — 2026-08-08, after session 6 (ladder phase, tag `ladder1`)

Start here, then [docs/game-model.md](docs/game-model.md) →
[docs/strategy-log.md](docs/strategy-log.md) → [docs/opponents.md](docs/opponents.md).

## Read this first: the frame changed under us

`bots/aug7` got measurably better this session — one accepted change, +7.9 points against the
version we started with. It is also **no longer the strongest bot on our own team**. Our
teammate x3r0's active submission, now vendored locally as `bots/opp_v44` ("florent-v58"),
**beats `aug7` 59/41** (aug7 at 40.8% [32.5%, 49.8%], 120 matches, 38 `core_destroyed`).

**Consequences, both now standing rules:**
- **`opp_v44` is the primary confirm opponent.** A keep must clear the Wilson gate against it.
  Keep measuring vs `aug7` for lineage attribution, and vs `starter`/`opp_v39` as no-collapse
  checks — but the ladder-relevant number is vs `opp_v44`.
- **The active submission slot follows arena measurement.** A candidate that beats `opp_v44`
  takes the slot, with the numbers attached.

**And the reason it beats us is structural, not tuning.** From a full source read of
`opp_v44` (catalogued in [opponents.md](docs/opponents.md)): **`aug7` has no code path that can
kill a Core.** It never tracks the enemy Core, never moves toward it, has no `fire()` sabotage,
no forward turrets, no Launcher. It can only win a Core kill if an enemy wanders into a home
Sentinel's line. That matches the ladder record exactly: **15W-74L (17%) on `core_destroyed`,
51% on the economy tiebreak.**

## The one thing to decide

**Apply `bots/_fix_core00` — five lines — or don't.** It is the current `aug7` plus the (0,0)
Core fix, regenerated after this session's accept, so it applies cleanly.

| evidence | before | after |
| --- | --- | --- |
| team A's `titanium_collected` on jackpot, 6 matches | **0, 0, 0, 0, 0, 0** | 4970, 2480, 4970, 4960, 2480, 4970 |
| jackpot mirror seat split (identical bots) | **0/48 = 0.0%** [0%, 7%] | **22/48 = 45.8%** [33%, 60%] |
| pooled confirm, 480 matches | — | 51.5% [47.0%, 55.9%] — **no verdict** |
| regression vs `opp_v39`, 240 matches | 65.0% [57.8%, 71.6%] | 62.5% [56.2%, 68.4%] — no regression |

All 16 comms slots start at 0 and hold non-negative integers, so **0 is indistinguishable from
"unwritten"**. The Core publishes `write_store(SLOT_CORE_X, pos.x)` and builders read it behind
`if x > 0 or y > 0`. On `jackpot` team A's Core is at exactly **(0, 0)** — the only such Core in
the rotation — so its builders never learn where home is. Trail conveyors (**the only thing that
delivers our titanium**), sentinels, and heading home are all gated on that. The fix publishes
`x+1`/`y+1` and subtracts on read.

**Why the loop didn't keep it:** the confirm is a no-verdict and the standing rule says a
no-verdict is a discard. But the no-verdict was **predicted in writing before the run** —
repairing 1 map of 15 is worth ~+1.7 points, and 480 matches cannot resolve that. It came back
+1.5. Same category as **v2's CPU guard, kept on a no-verdict** as ladder insurance.
**Recommended: apply.** Separately worth deciding: whether `program.md`'s accept rule should gain
a per-map correctness clause, since as written it is structurally blind to any single-map defect.

**Confirming evidence from a completely different direction:** `opp_v44` and `opp_v39` both
publish positions through a `pack_pos`/`unpack_pos` pair with **the identical +1 offset**. The
strongest bot on the team already solved this exact problem the same way.

**Free bonus:** the organisers' `starter` has the identical guard, so **most of the field has
this bug**. `starter` vs `starter` on jackpot leaves seat A with 0 collected, 0 units, 1
building. Any starter-descended opponent hands us jackpot whenever they draw seat A.

## What changed in the bot

**One accept, in `bots/aug7` (`3cfa588`):** the trail conveyor picks its facing with
`cardinal_toward(src, dst)`, comparing `|dx|` and `|dy|` on the real delta, instead of snapping
an already-quantised 8-way `Direction`. **57.9% [53.5%, 62.3%] over 480 matches**; regression vs
`opp_v39` 65.8% [59.6%, 71.5%]; **0 crashes in 1,004 matches**.

**Read it honestly: the hypothesis that motivated it was refuted by the same run.** The argument
was mirror-equivariance, and the prediction was that the six mirror maps would move toward a
fair seat split. They did not — two got worse, and the challenger took **61.1% on the nine
rotational maps against 53.1% on the six mirror ones**, the opposite ordering. What paid was
simply pointing trails at the Core, most on long-trail wally maps. **The mirror asymmetry is
still unfixed**; `heart` is now its sharpest example.

**One discard: wall-aware BFS pathfinding.** Confirm **45.8% [41.4%, 50.3%]**. CPU was never the
issue (worst case 3785 µs against an 8000 µs guard). The per-map prediction **inverted**: the
five walliest maps gave **35.6%**, the other ten **50.9%**, and its three worst maps in the whole
run are the three walliest. Best explanation: **the greedy walker's meandering is exploration and
a shortest path is not** — target selection picks the nearest *visible* ore, and detours sweep
vision across ground a straight line never touches. Retrying this needs an exploration mechanism
in `_pick_target`, not another movement change. Code kept in `bots/_dev_bfs`.

## The next queue, ranked — mostly adopted from `opp_v44`

Adopting a teammate's proven mechanisms into our gated line is the fastest convergence path, and
the full catalogue with line references is in [opponents.md](docs/opponents.md). In order:

1. **Track the enemy Core at all.** `aug7` has *zero* equivalent — no `SLOT_ENEMY_CORE`, no
   `self.enemy`. Add the rotational guess `(W-2-cx, H-2-cy)` on an offset-safe slot, overwritten
   the moment any unit sights the real thing. Cheap, purely additive, and a **prerequisite for
   anything offensive**. Note the guess is wrong on the 6 mirror maps — v44 keeps a 21-map table
   for exactly this reason, and we already have the census.
2. **Let the Core build its own defensive Sentinel on its own ring**, independent of whether a
   builder is nearby (~15 lines, modelled on `opp_v44:246-260`). Removes `aug7`'s single point
   of failure: today, if no builder is within dist²≤18 when the threshold trips, there is no
   defense at all. Also the natural home for **reactive** defense — build immediately when an
   enemy is visible near our Core, regardless of harvester count, which preserves economy-first
   against the passive field.
3. **Minimum-viable offense.** Once economy is up, send a fixed fraction of new builders at the
   tracked enemy Core, `fire()`-ing adjacent enemy buildings en route (2 dmg for 2 Ti, no ammo).
   The smallest change that gives us *any* Core-kill capability.
4. **Adaptive ammo buffer** — raise the target while under attack (~3 lines once (2) exists).
   This is `strategy-notes.md`'s own long-standing open item; v44 does it in one line.
5. **Sentinel targeting** — replace the first-hit scan with a full scan plus a priority table
   (v44 ranks by target *value*, which is a better answer than the "nearest" fix we had planned).
   Free and strictly correct, but **measured as probably a null against a passive pool**: across
   625 captured sentinel firings, zero were suboptimal, because rays rarely hold 2+ enemies.
   Test it against `rush_probe`, where they will.
6. **Structural, not single changes — adopt deliberately or not at all:** v44's BFS conveyor
   planner (~150 lines, a real subsystem), its exact per-map database, and its Launcher +
   role-caste + claim/heartbeat/ACK choreography. That choreography is *the* explanation for its
   Core-kill rate; adopting it means writing a comparable subsystem, not editing `aug7`.

Standing caution that still applies: every previous attempt to trade economy for *defense* lost.
Items 1-3 trade defense for *offense* and add capability rather than removing economy — untested
territory, not a re-run. Note also that the top of the ladder is not economy-light: **Pivot
(#1, ~1947) runs 12 harvesters, 39 conveyors, 17 Gunners and zero Sentinels**, out-collecting us
**3170 to 810**, while we cap at `TARGET_HARVESTERS = 3` and then build sentinels with no cap —
a probe counted **66 in one match**, at +20% scale each. `TARGET_HARVESTERS` and the missing
sentinel cap are untested levers.

## The rush-defense lane (in flight, not finished)

Our entire local opponent pool — `starter`, `opp_v39`, our own lineage — is passive. **Every
"early aggression doesn't pay" result we have was measured against a field that never
attacks.** The 1300+ band does. `bots/rush_probe` is being built to close that hole: a
measurement instrument, not a competitor, replicating the observed pattern. **Its baseline run
(`aug7` vs `rush_probe`, seeds 8) had not completed when this session ended — that number is the
first thing to get.**

The pattern it replicates, decoded from ladder series `81d83bb5` (Albert And Einstein **1306.8**
vs us **1222.8**, **0-5**, all five games `core_destroyed`, and **we out-collected them in every
game with a non-zero economy**):

- **Builder turn 0 → Launcher turn 1 next to their own Core → their own scout thrown 6-8 tiles
  in one action → camped inside our Core's spawn ring by turn 6-27**, staying for 57-98% of the
  game. Then **3-4 Sentinels 1-4 tiles from our Core**, turns 4-15. Four builders, total.
- **The sentinels kill us, not the blocker** — 5 of 5 on `core_destroyed`; the Core always died
  before any economy tiebreak could matter. But our first Sentinel landed at turn 436 and turn 81
  in the two long games, against a gate met at turn 22-28, and game 4 never met the gate at all.
- Accept rule for this lane: a defense change must clear the normal gate **and** materially
  improve vs `rush_probe` **and** not collapse vs `starter`/`opp_v39` — we climb through a mostly
  passive field and must not overfit to rushers.

## The highest-value diagnostic left: we sometimes deliver exactly zero

Two independent observations converge, and this is probably worth more than anything in the queue
above. **`titanium_collected` comes out at exactly 0 on maps with no (0,0) Core:**

- Ladder replay `81d83bb5` games 1 (`heart`) and 4 (`hive`): **0 collected for both sides**,
  while game 1 had **5 harvesters and 99 conveyors** built and 33 `distributeResources` events
  fired. The analyst ruled out the enemy blocker denying our delivery tiles.
- Locally and independently: on `heart`, **3 of 5** `aug7`-vs-`aug7` matches end with **both
  sides at exactly 0**, decided on the harvester tiebreak.

Crediting is delivery-only and **78% of our games are decided on the titanium tiebreak**, so this
is not an inefficiency — it is the economy not existing. It is invisible in a win rate because
when both sides zero out the game still resolves. **Instrument whether a given harvester's stack
ever reaches the Core** — the open question "do our chains actually complete a path?" has been
open since 2026-08-07 and now has two pieces of evidence that the answer is sometimes no. Run it
on `heart`, where it fails ~60% of the time.

## Also unexplained

**Four maps have large, reproducible seat asymmetries with identical bots on both sides:**
archipelago ~77-88% for seat A, atoll ~21-31%, heart ~31%, lighthouse ~28%.

**`archipelago` is now explained and it is an engine fact, not a bug:** team A's Nth builder
always gets a unit ID exactly one less than team B's Nth (zero exceptions, 10 instrumented
matches), so **seat A resolves first every round**. Where ore is contested — 16% of
archipelago's tiles sit near the midline, and a harvester blocks movement — that compounds into
**62 harvesters for A against 27 for B**, with 10 of A's built past the midline and B never
crossing once. This upgrades game-model.md's old "advantage on very small maps": **contested ore,
not map size, is the variable.** `atoll` (8 ore tiles, 50% contested → near-tie) and `lighthouse`
(0% contested → no harvester gap) corroborate. **`lighthouse` and `heart` remain unexplained**,
and `heart` is very likely the zero-delivery bug above.

## Where we are

- **Research bot: `bots/aug7` at `3cfa588`.** Not submitted. Freezing to `bots/v5` and
  submitting are Magnus-only.
- **`bots/_fix_core00`** — `aug7` + the (0,0) fix, awaiting the decision above.
- **`bots/opp_v44`** — teammate's active bot, the new primary confirm opponent.
- **`bots/_dev_bfs`** — the discarded BFS pathfinder, kept and portable.
- **`bots/rush_probe`** — in flight, unfinished.
- **`bots/ladder1`** — the experiment slot, currently a clean copy of `aug7`.
- Pool is `maps/*.map26`, the real **15-map** weekly rotation. All 15 declare
  `symmetry = 0` and **6 of them are lying** (eider/heart/moonrise mirror across a vertical
  axis; antler/meander/nordkap across a horizontal one). Verify against tiles, never the header.

## Traps

Previous ones all still apply (python3 is 3.14 — use `.venv/bin/`; always `--tle 10`; `print()`
goes to the replay, use stderr; `random` is not seeded by `--seed`; never single-seat or pooled
evaluation; game-model.md beats the organisers' `CLAUDE.md`). New this session:

- **The comms store cannot represent a zero.** Anything positional needs an offset. Assume any
  raw `write_store(slot, some_coordinate)` is the same bug waiting.
- **`ct.get_cpu_time_elapsed()` is inert under `fcode run`, even with `--tle 10`** — it read 0
  before and after a loop `time.process_time()` clocked at 22 ms. Our CPU guard has never tripped
  locally *because the counter never moves*. Profile with `time.process_time()`; only
  `fcode match test` on Graviton3 verifies a CPU-heavy change.
- **The bot-code validator rejects `try`/`finally` blocks.** Undocumented anywhere.
- **Tile queries raise on anything outside current vision**, not just off-map, with the same
  message. `in_bounds()` is necessary but not sufficient.
- **A pooled win rate cannot see a single-map defect** (~2 points on 1 of 15 maps). The instrument
  is the **per-map mirror seat table** — re-run it whenever the rotation changes.
- **When an outcome is extreme and stable, stop running matches and read the state.** 0 wins in
  104 was answered by six single matches with the JSON parsed.
- **A change can win for a reason other than the one you proposed, and a well-argued arithmetic
  hypothesis can be entirely wrong.** Both happened here. Log the mechanism separately from the
  number, or the next session tunes the wrong lever.
- **A per-replay observation is only evidence about the submission version that played it.** The
  team ran 42 versions in a day. Use **`fcode match list --mine --json`**, which carries
  `teamAVersion`/`teamBVersion`, `eloDelta` and `ratingBefore` per match — never reconstruct an
  activation timeline by hand.
- **Do not reset `bots/ladder1` while an agent is measuring it.** Doing exactly that mid-run this
  session clobbered a subagent's ported file; the measurements survived only because they had
  already completed.

## Not done

- **The dated labels in our docs have drifted ahead of wall-clock and I propagated the drift
  rather than silently renumbering.** Every git commit here is authored `Thu Aug 6 2026`, and the
  platform's timestamps agree, but session 5 labelled its entries `2026-08-07` and this one
  `2026-08-08` to stay monotonic. **The three "days" in the log are one calendar day.** Worth
  fixing deliberately, and worth knowing before correlating with the dev-knowledge vault's daily
  notes, which are keyed to real dates.
- `bots/rush_probe` and its baseline; the batched UR-replay digest (both were still running).
- Daily retro in the dev-knowledge vault.
- Still no `git remote`; `results.tsv` still deliberately untracked.
- Safe to delete: `bots/_incumbent` (stale pin), `bots/_diag_core`, `bots/_diag_seat`,
  `bots/_probe_sent`, `bots/aug7_h1..h4`, `bots/_probe_conv`. **Keep** `bots/_fix_core00`,
  `bots/_dev_bfs`, `bots/opp_v44`, `bots/rush_probe`.
