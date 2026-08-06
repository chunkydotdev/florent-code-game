# Handover — 2026-08-08, after session 6 (ladder phase, tag `ladder1`)

Start here, then [docs/game-model.md](docs/game-model.md) →
[docs/strategy-log.md](docs/strategy-log.md) → [docs/opponents.md](docs/opponents.md).

## Read this first: the game we keep losing is not the one we keep fixing

**We out-collected Albert And Einstein 4880 to 0 and lost the game** — to **3 enemy units that
were never reinforced, over 985 turns**. Not a rush that overwhelmed us. Three static pieces
that sat there all game while we had no way to remove them.

`aug7` has **no mechanism that removes an established enemy emplacement**: no enemy-Core
tracking, no movement toward it, no `fire()` sabotage, no forward turrets. So once a siege is
planted we spend the rest of the match accumulating a tiebreak we can never reach. **More
defense does not fix this.** The cheapest tool for it is one we already have and have never
used: `ct.fire()` from a builder, 2 damage for 2 Ti against buildings, orthogonally adjacent.
**Call this lane "clear the siege" and treat it as a peer of the defense lane, not a follow-up.**

Related and equally load-bearing: the Core's *net* HP-to-kill is a stable 500-512, but **raw
hits landed range from 28 to 1206** across decoded games, because healing (+4 HP for 1 Ti, every
round) absorbs the difference. **Healing is the cheapest defensive lever in the game** — 0.25
Ti/HP against ~0.56 for any attacker — and a siege that is not out-healing the defender is not
making progress no matter how long it runs.

## Read this second: the frame changed under us

`bots/aug7` got measurably better this session — one accepted change, +7.9 points against the
version we started with. Locally it is also **beaten by our teammate x3r0's active submission**,
vendored as `bots/opp_v44` ("florent-v58"), which takes it **59/41** (aug7 at 40.8%
[32.5%, 49.8%], 120 matches, 38 `core_destroyed`).

**But hold that lightly against the ladder record, which points the other way.** With real
per-match version attribution (`fcode match list --mine --json`, 181 matches): **v40 — our line
— is 8W-1L, net Elo +35.24, the strongest well-sampled version the team has.** v44 has only
**2 rated series** (+14.34) and is undefeated on the rated ladder; **all of its observed losses
are unrated, 0W-4L, and all 20 of those games ended `core_destroyed`** — to the rush archetypes
below. The 120-match local arena is far better powered than either ladder sample and its verdict
stands, but the honest summary is: *our line has not been outperformed where it counts yet, and
v44's only known weakness is exactly the one this session's lane targets.*
(An earlier entry in this handover claimed v40 played "exactly one ladder series" — that was
wrong, produced by reconstructing an activation timeline by hand. Corrected in the log.)

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
2. **Adopt v44's vision-triggered emergency defense — the rush lane's primary candidate, and
   the highest-value adoptable piece in the catalogue.** `aug7` has **zero threat detection of
   any kind**; today defense is scheduled off *our* economy and never off the *enemy's*
   behaviour. v44 computes the threat **Core-side from the Core's own vision** and triggers on
   an **enemy turret at d² ≤ 64 or an enemy builder at d² ≤ 16**, then banks ammo and raises a
   **3-turret battery facing the threat in the same round**; separately, a **`home_defend`**
   all-hands diverts nearby friendly builders when an enemy builder is at **d² ≤ 20**.
   **Port the mechanism — threat detection decoupled from own economy progress — not the
   constants**, and build Sentinels rather than their Gunners, since Sentinel-first is measured
   in our lineage. It is teammate code; adoption is the point.
   **Do not replicate one detail: v44 disables this battery on maps with `w*h <= 120`**, so
   `fjordgate` (10×10 = 100) falls through to a slow `harvesters >= 1` fallback. That is a known
   hole in our own team's active bot — and in anyone who copies the pattern. Our port should
   cover small maps, and `fjordgate` is the per-map row where that shows.
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

## The rush-defense lane — now the critical path (in flight, not finished)

**Field observation, high confidence: the sentinel rush is the COMMON ladder opening, including
among high-Elo teams.** Not one team's quirk. That makes `rush_probe` a model of the *median*
opponent, and it makes **`aug7` vs `rush_probe` the single most ladder-predictive local number
we have.** It did not complete before this session ended. **Get it first.**

Our entire local opponent pool — `starter`, `opp_v39`, our own lineage — is passive, so **every
"early aggression doesn't pay" result we have was measured against a field that never attacks.**
Those results answered a question about a distribution we do not play against.

**The counter-meta hypothesis, pre-registered in [strategy-log.md](docs/strategy-log.md) before
any measurement: defended economy farms a converged-rush field.** Three measured facts favour
the defender *if* defense triggers early enough — healing at **0.25 Ti/HP** against ~0.56 for
any attacker; **Sentinels cannot rotate**, so a rush emplacement approached off-axis is
furniture; and every rush Sentinel costs the attacker **+20% scale permanently**, so a failed
rush taxes everything they build afterwards. Our defect is not "too little defense" — it is that
defense is scheduled off *our* economy and never off the *enemy's* behaviour. `bots/ladder1`
currently holds a **reactive home defense** variant testing exactly that, with predictions
stated in advance: **a no-op against the passive pool, a material gain against aggression.** If
both halves hold, it counters the median opponent rather than patching a weakness.

**The first baseline is in, and the number is not the finding: `aug7` beats `rush_probe` 95.0%
[91.5%, 97.1%]** (`starter` beats it 93.3% while losing 221 units to its own crash bug). Since a
real 1306 opponent beat us **0-5 by Core kills**, the probe is wrong, and its own cross-tab says
how: **rush_probe's own Core died in 22 matches to `aug7`'s 5** (all-in leaves zero home
defense), and **on 7 of 15 maps neither Core died at all**.

**⚠ Direction check, because this has already been misread once:** `arena.py` reports the
**first-named** bot's win rate, and the runs were `arena.py aug7 rush_probe` and
`arena.py starter rush_probe`. **95.0% and 93.3% are the DEFENDER's win rates — the rusher lost
both, badly.** Inverted, they read as "the meta threat is quantified and severe", which is the
opposite of the measurement. **The meta threat is not yet quantified.** What is quantified is
that *this* probe is harmless. Do not size the defense work off these numbers.

**The correction that matters: three Sentinels stall on ammo, not damage.** One firing on
cooldown burns **5 Ti/round**, three burn **~15**, against **2.5 Ti/round** passive income — so
a probe with no economy fires about a sixth of the time. **The real meta is economy-PLUS-rush,
not all-in rush.** Also, walk-only delivery under-tests big maps by an order of magnitude:
measured first-Sentinel turn was 3-4 on fjordgate but **24-56 on drumlin**, against an observed
benchmark of **turn 4-15 regardless of map size**.

### The delivery bug has a mechanism: conveyors are mis-FACED, not just incomplete

`tools/replay_census.py` (new; schema in `tools/replay_schema.md`, both protected — read and run,
never edit) emits one TSV row per replay and separates two things we had been conflating:
**`chain`** = harvesters reachable from the Core through the conveyor graph, versus
**`chain_dir`** = harvesters connected by a **facing-correct** delivery path. The gap between
them is the bug.

Measured on the old lineage: `v1`-vs-`starter` showed **5 of 6 harvesters graph-connected but
only 2 of 6 facing-correct**; and one `heart` replay had **40 conveyors, `chain` 2/2,
`chain_dir` 0/2, and ZERO titanium collected**. That is the "exactly zero collected" mystery
resolved into a concrete, per-replay-diagnosable mechanism: **trail conveyors point along the
walk direction rather than the flow direction.**

**The census is done, and it names three distinct causes.** `cardinal_toward` (accepted at 57.9%)
fixed the smallest one. The isolating metric is the **conditional rate** — of harvesters that got
graph-connected, what fraction also face correctly — because raw `chain_dir%` is confounded by
overall bot strength.

| cause | status |
| --- | --- |
| **1. chirality mis-snap** (`nearest_cardinal`'s "NORTHWEST → WEST") | **fixed.** Non-tie wrong-cardinal picks 8/58 → **0/63**. On `drumlin` (wall-free control) the conditional rate goes **50% → 91.7%** |
| **2. facing computed toward the CORE, not toward the next trail tile** | **open — 71% of the residual.** Any bend in the path breaks the chain *even when every tile's facing is locally correct* |
| **3. exact diagonal ties on shared trunk tiles near the Core** | **open — rare but catastrophic.** One tie resolved wrong collapsed **8 of 12 harvesters at once**; `cardinal_toward` still breaks ties with `random.random()`, i.e. 50/50 exactly where it costs most |

Pooled, the conditional rate barely moved: **v4 47.4% → aug7 48.9%, z ≈ 0.2, not significant** —
and on `heart` it went the *wrong* way, 37.5% → 12.5%. So the 57.9% accept is real and properly
attributed, but **it is not explained by facing-correctness**, which is a more interesting claim
than either "it worked" or "it didn't".

**The next economy experiment, precisely specified — do this one first:** in `_try_move`, face
the trail conveyor **toward the tile the builder is about to step onto**, not toward the Core.
Straight-line-to-Core and trail-direction agree only on straight paths, which is exactly why
`drumlin` looks fixed and `heart` does not. One attributable change, addresses 71% of residual
breaks, needs no new state — `_try_move` already has `next_pos`. Then, separately, replace the
random tie-break with something chain-aware.

**Two calibration notes.** `chain_dir == 0` ⇔ zero collected is **18/18 perfect in
economically-decided games**, but the converse fails in combat-truncated ones (a network can be
destroyed after banking), so read it as: zero economy *always* implies `chain_dir == 0`. And
field-wide across 24 ladder replays and 10 opponents the conditional rate is **68.4% against our
48.9%** — **we are below field average at delivery facing.**

**Standing rule: verify any candidate's own test replays show `chain_dir == chain` before
believing any economy or ammo number it produces.** Worth also running the clean single-change
census — `aug7` vs `bots/_incumbent` (`a9d81a1`, aug7 minus `cardinal_toward`) — since the
comparison above used `v4`, which differs by two changes.

### The ammo arithmetic converges two workstreams — sequence v45 accordingly

**Sustained fire requires delivered income.** 15 Ti/round for three Sentinels against 2.5/round
passive is not a rusher's problem — it is *everyone's*, including ours the moment reactive
defense actually fires. So **vision-triggered defense and delivery/chain completion are one
workstream, not two**, and the ordering is forced:

1. **Delivery first.** Our `AMMO_BUFFER` is **20 — two Sentinel shots.** A reactive battery with
   nothing to fire is furniture, and we already know our chains sometimes deliver **exactly
   zero** (`heart` fails ~60% of the time locally; a ladder replay shows 0 collected with 99
   conveyors built). **Fixing delivery is a prerequisite for defense, not a parallel track** —
   and it is separately the highest-value diagnostic we have.
2. **Then the v44 vision-triggered defense adoption**, which can only sustain itself on top of
   (1). Adaptive ammo (raise the buffer while under threat) belongs here, not earlier.
3. **Then offense** — enemy-Core tracking and minimum-viable attack — which has the same income
   dependency, one step further out.

The already-measured pieces (`3cfa588` conveyor facing, and `bots/_fix_core00` pending your
decision) sit underneath all of this: both are delivery fixes, which is the same axis.

**Two probe modes are now in flight:** walked-sentinel (`bots/rush_probe`, preserved as the
verified baseline artifact) and launcher-insertion (`bots/rush_probe_fast`). **Both must carry
enough economy to sustain ammo, and both keep 1-2 home Sentinels** — a probe that suicides
measures its own fragility, not our defense.

**Calibration targets, corrected from 9 decoded replays across 6 opponents rated 1323-1965 —
there are TWO archetypes and the early one is faster than previously stated:**
- **"instant-Sentinel", turn 1-6.** The Launcher-thrown builder **builds the forward Sentinel on
  arrival**, making the opening **map-size-independent**. Seen in `sporks` (1923) and all five
  AAE games; `sporks` killed a Core in **63 turns**, the fastest measured here. The earlier
  "turn 4-15" target was too slow — **assume contact from turn 1**.
- **"forward-Gunner", turn 33-39.** A distinct second lane, with `Pivot`, `not adgato` and
  `Besvikomat` — three unrelated opponents — converging tightly. **Defense must cover both
  windows.**

**The timing calendar now has a distribution, not an anecdote.** Census of **24 real ladder
replays (48 team-sides)**: 28 sides built a Sentinel at all, and first-Sentinel rounds **cluster
hard at rounds 3-6** (12 of 48 sides), **median 10**. So **reactive defense must be armed from
round ~3** — which is a hard constraint on implementation, not a preference: a warm-up counter, a
target-selection delay, or a comms-store round trip (writes are visible only from the *next*
round) can each push first response past the entire cluster.

**Ring-camping is correlated with wins, not causal.** Both the replay digest and the local probe
agree the blocker never decides a game. Do not over-invest in it.

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
