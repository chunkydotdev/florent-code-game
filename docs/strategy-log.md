# Strategy log

The point of this file: in a ladder game, the thing that compounds is knowing which changes
moved the rating and which didn't. Memory is unreliable and the ladder is noisy — write it down.

**One entry per deployed bot version.** Write the hypothesis *before* deploying, the result
*after* the ladder has settled. Keep dead ends — a documented failure is worth as much as a win.

Rules of thumb:
- Change one meaningful thing per version, or you can't attribute the result.
- Give the ladder enough matches to be meaningful before calling it. Note the sample size.
- If the result surprises you, that's a fact for [game-model.md](game-model.md), not a tweak.

---

## Template

### v0 — name

- **Date deployed:**
- **Commit / tag:**
- **Hypothesis:** what we believe and why we believe it
- **Change:** what's actually different from the previous version
- **Predicted effect:** stated before deploying, so we can be wrong on the record
- **Result:** rating before → after, over N matches
- **Read:** did the hypothesis hold? what did we learn regardless?
- **Next:** what this points at

---

<!-- newest entries at the top, below this line -->

### Diagnostic — aug7 on the real map rotation: 69.6%, not 80.5%, and still crash-free

- **Date:** 2026-08-07 · diagnostic only, **not** an accept/discard run and not a metric change
- **Why:** the real rotation landed in `maps/new-maps/` (f71614e) mid-session, while the
  parallel experiments were already running on the eight invented maps. Cutover is a
  between-tags operation ([runbook.md](runbook.md) §2), so the right move was to leave the
  metric alone and measure the gap explicitly rather than guess at it.
- **Setup:** `arena.py aug7 starter --maps maps/new-maps/*.map26 --seeds 8 --jobs 8`, n=224.
  Passing explicit paths means no protected file was touched and the standing metric is
  unchanged.
- **Result:** **69.6% [63.3%, 75.3%]** vs the invented pool's **80.5% [75.2%, 84.9%]** —
  intervals barely overlap, so the edge is genuine but roughly 11 points thinner than our
  headline. **0 crashes in 224 matches** (starter: 355), including `jackpot`'s literal corner
  Core and the five maps at ≥14% wall density. Weakest: `hive` 6/16, `archipelago` 8/16,
  `atoll`/`jackpot` 9/16. An earlier n=56 pass read 57.1%; that was noise, use n=224.
- **Read:** the two things this lineage was actually built on — crash-freedom and
  direction-neutrality — **transfer to the real distribution intact**, which is the outcome
  that mattered most and was genuinely in doubt (a corner Core is exactly the case the
  full-ring spawn scan was written for). What does not transfer is the size of the margin: a
  meaningful part of our 80.5% was earned against maps we invented, on which starter's
  weaknesses are presumably over-exposed. Treat 69.6% as the honest pre-ladder expectation.
- **Next:** re-baseline properly after cutover, and re-run the aimed-sentinel experiment
  specifically — a Sentinel's wall-ignoring line is worth much more at 30.8% wall density than
  at our inventions', so that null was arguably answered on the wrong distribution. Per-map
  tuning has a one-week shelf life given the weekly rotation; robust-across-maps changes keep
  their priority permanently.

### Finding — the harvester's first conveyor has never been built, in any version, ever

- **Date:** 2026-08-07 · found as a side-observation while discarding the conveyor-chain
  experiment; verified independently before being believed
- **The claim:** `_try_build_conveyor_toward_core` — the function that gives each newly built
  harvester its output conveyor toward the Core — is **dead code**, and has been since the
  organisers' shipped starter bot. The identical line is in `bots/starter/main.py:286`,
  `bots/v4/main.py:375` and `bots/aug7/main.py:379`, i.e. the entire lineage.
- **Verification:** instrumented copy (`bots/_probe_conv`), single matches across mid20,
  large30, hsym16, duel16. **24 calls, 0 legal, 0 conveyors built.** Target tile was the
  builder's own tile 18 times (`dist_sq=0`), diagonal or 2 steps away the other 6.
- **Cause — a grid-parity fact worth remembering:** `can_build_conveyor(pos, facing)` requires
  `pos` to be orthogonally adjacent to **the acting builder**, not to the harvester. The
  builder stands orthogonally adjacent to the harvester `H` (build requires that), and the
  code targets another orthogonal neighbour of `H`. The grid graph is bipartite, so **two
  tiles one step apart share no common orthogonal neighbour**: the target is either the
  builder's own tile (explicitly disallowed) or not adjacent to the builder. Always illegal.
  Generalised: **a builder adjacent to a building it just placed can never build anything
  orthogonally touching that building — it must move first.** This constrains every
  build-adjacent-to-a-building idea we might have, not just this one.
- **Why it has not hurt us — measured, not assumed.** `_try_move` lays a conveyor on the tile
  *ahead* before stepping onto it, so a builder is usually standing on a conveyor, and its own
  tile *is* orthogonally adjacent to the harvester it then builds. Instrumented across all 8
  maps, 3–4 seeds each, 30 matches: **264 harvesters built, 263 (99.6%) had an orthogonally
  adjacent friendly conveyor**, 233 of them by the earliest measurable round (the round after
  the build). One miss, on duel16. 0 lost, 0 unresolved.
- **Conclusion: do not fix it.** The bug is real, permanently non-firing, and completely
  masked. Deleting or repairing the function would change nothing measurable, and a change
  that cannot move the metric is not worth the risk of touching the submission candidate.
  This is the rare case where the correct action on a verified bug is to write it down and
  walk away.
- **Residual, unmeasured:** adjacency is necessary but not *sufficient* for delivery — a
  conveyor whose output side faces into the harvester won't accept from it. The probe measured
  presence, not accept-side correctness. Trail conveyors face toward the Core and harvesters
  round-robin across neighbours, so this is unlikely to bite, but it is a distinct question
  if anyone pushes further.
- **Note on the field:** anyone who started from the organisers' starter bot has inherited
  this same dead function. See [opponents.md](opponents.md).

### Discard — aimed sentinel placement is a perfect null, and the null is the finding

- **Date:** 2026-08-07 · tested against sentinel-first aug7 (fc53345 working tree), parallel
  session (`bots/aug7_h*`, `--jobs 3`)
- **Hypothesis:** a sentinel is 30 Ti + a 20% scale tax — the most expensive irreversible
  decision the bot makes — and its whole value is *(position, facing)*, since it fires an
  unblockable line. The incumbent takes the first legal adjacent tile and faces
  `direction_to(core).opposite()`, i.e. the builder's incidental standing position picks the
  arc. `can_fire_from()` / `get_attackable_tiles_from()` exist precisely to evaluate a
  placement before paying for it, and nothing in the tutorials or our lineage uses them.
- **Change:** score all legal (≤4 adjacent tiles × 8 facings) pairs and build the best.
  Score per covered tile = proximity to our Core + alignment with the corridor toward the
  inferred enemy Core (point-reflection of our Core through the map centre), with tiles
  already inside an existing friendly sentinel's arc down-weighted to 0.4. Ties broken by
  shuffled iteration. `_run_sentinel` targeting deliberately left unchanged.
- **Result:** screen **56.2% [42.3%, 69.3%]** (n=48) — survived, leaning positive. Confirm
  **50.0% [43.9%, 56.1%]**, exactly 128–128 (n=256), 0 crashes both sides. **No verdict,
  therefore discard.**
- **Read:** this is a stronger null than the win rate alone shows, and that is the point.
  `core_destroyed` came in at **44/256 = 17.2%** against the null-change control's
  **16/96 = 16.7%** — the change produced *no detectable effect at all* on the one axis it was
  specifically designed to move. That distinguishes "didn't clear the bar" from "did nothing",
  and the two call for different follow-ups.
  The likely structural reason, per the runner's read: by the time a builder reaches the
  sentinel gate it has navigated to within dist²≤8 of the Core, where the tiles are already
  occupied by our own economy build-out — so the candidate set frequently collapses to a
  single legal position and the scorer only refines facing among options that were already
  narrow. **This was not instrumented** — no count of how often the scorer picked differently
  from the incumbent — so the mechanism is inference, not measurement.
- **Next:** do **not** try another arc-scoring function first; the flat `core_destroyed` rate
  says arc quality isn't the binding constraint. The cheap prerequisite is to instrument how
  many legal (position, facing) pairs a builder actually has at the sentinel gate. If that
  number is usually 1, the real lever is *where sentinels get built at all* (reserving tiles,
  or building them further out on the approach) and every arc experiment downstream of it is
  measuring nothing.
- **Method note:** the screen read 56.2% and the confirm read 50.0% — a textbook illustration
  of why the screen cannot promote and why "the number went up" is not an accept rule.

### Discard — deliberate harvester-to-Core conveyor chains cost more builder-rounds than they earn

- **Date:** 2026-08-07 · tested against sentinel-first aug7 (fc53345 working tree), parallel
  session (`bots/aug7_h*`, `--jobs 3`)
- **Hypothesis:** the highest-ceiling idea available. Crediting is delivery-only (measured,
  game-model.md): a harvester whose path to the Core never closes earns exactly zero, on the
  balance *and* on tiebreak #1. The incumbent has no deliberate chain-building at all — only
  incidental conveyors dropped on tiles a builder happens to walk over. Conveyors are also the
  cheapest thing in the game on cost-scale (+1% vs +20% for a builder bot), so plumbing should
  be cheap where builder-rounds are the real expense.
- **Change:** a per-builder state machine that, after placing a harvester, takes over that
  builder entirely until the chain is done: greedy staircase route toward the Core (axis with
  more distance remaining, ties random), each link's facing recomputed from its own position
  so corners stay connected, terminating on the Core / an existing building / a 200-round cap.
- **Result:** screen **54.2% [40.3%, 67.4%]** (n=48), confirm **45.3% [39.3%, 51.4%]**
  (n=256), 0 crashes both sides. **No verdict, therefore discard.**
- **Read:** the cost is builder-rounds, not titanium. Laying a chain runs ~2 rounds per tile
  (walk, then build) and monopolises one of only ~5 builders for potentially dozens of rounds,
  against an opponent spending those same rounds finding and building more harvesters. The
  `core_destroyed` rate (42/256 = 16.4%) sat right on the null-change control's 16.7%, so
  nothing about the game's character changed — this was purely an economic trade, and it lost.
  **The chains were never verified to complete**, so strictly this refutes "dedicate builders
  to plumbing", not "complete chains are worthless" — those come apart only if completion is
  measured, which it wasn't.
- **Next:** the same session's dead-code finding above (harvesters may already be served by
  incidental trail conveyors) is the cheaper way at the same underlying question, and is being
  measured directly rather than inferred. Third discard in a row for the shape "spend
  builder-rounds or economy on something else" — that pattern is now very well evidenced.

### Discard — demand-driven ammo conversion loses the same way a bigger buffer did

- **Date:** 2026-08-07 · tested against sentinel-first aug7 (fc53345 working tree), parallel
  session (three hypotheses run concurrently in scratch dirs `bots/aug7_h*`, `--jobs 3`)
- **Hypothesis:** the AMMO_BUFFER 20->50 discard refuted a bigger *standing* buffer, not
  better-*timed* conversion. `convert_ammo()` is usable the same turn and costs no action
  cooldown, so ammo can in principle be raised on demand: hold near-nothing while quiet, burst
  when a threat appears. Named as the explicit follow-up in that discard's "Next".
- **Change:** new store slot 4 carries a threat timestamp. Sentinels scan
  `get_nearby_units(dist_sq=get_vision_radius_sq())` (r²=32, same as their attack radius, so
  strictly earlier warning at no extra reach) and write `round + 1` on seeing any enemy unit.
  The Core reads it and targets 40 ammo (4 sentinel shots) if the sighting is <=5 rounds old,
  else 10 (one shot). Conversion still gated on `harvester_count >= TARGET_HARVESTERS` and
  still reserves a builder bot's cost before converting, both unchanged from the incumbent.
- **Result:** screen **41.7% [28.8%, 55.7%]** (n=48) — survived by the letter of the rule, and
  coincidentally the identical figure to the AMMO_BUFFER=50 screen. Confirm **46.1%
  [40.1%, 52.2%]** (n=256), 0 crashes both sides — **no verdict, therefore discard**.
- **Read:** two independent ammo-timing levers have now failed in the same direction, which
  makes this a pattern rather than one data point: at this bot's strength, ammo scheduling is
  not where the wins are. The experiment confounded two changes it shouldn't have — it both
  *lowered the quiet-phase floor* (20 -> 10) and *added a delayed burst*, so it cannot separate
  "holding too little ammo when first contact happens" from "the burst arrives a round late
  because store writes are buffered". On the mix: this session ran a **null-change control**
  (byte-identical copy of aug7 vs aug7, n=96) which gives the first real baseline for the
  win-condition mix — `core_destroyed` **16/96 = 16.7%**. Against that, the ammo run's
  **28/256 = 10.9%** is a *reduction* in decisive combat outcomes, and the H2 run in the same
  session sat at 17.2%, i.e. right on the control. So the cut ammo floor does look like it
  suppressed core kills — the CIs overlap at the edge (control [10.4%, 25.5%] vs
  [7.7%, 15.4%]) so this is suggestive, not established. Note also the mix is pooled across
  **both** bots in a match, so it can never be attributed to the challenger alone.
- **Next:** if ammo is ever revisited, the clean version is baseline held at 20 (identical to
  the incumbent) with a burst added *on top*, which isolates the burst from the floor cut.
  Low priority: two discards deep, the prior should now be that this lever is worth little.
  The general lesson generalises further than ammo — **an experiment that changes a floor and
  adds a mechanism at once is one experiment producing zero attributable answers.**

### Discard — lowering the small-map defense trigger also loses

- **Date:** 2026-08-07 · tested against sentinel-first aug7 (a9d81a1)
- **Hypothesis:** strategy-notes.md's map-size section: a 14x area range (8x8-30x30) probably
  needs branched strategies, and small maps favour rushing since economy has no time to
  compound. Tried the cheapest version: switch to sentinel-building at 1 harvester instead of
  3 on maps <=150 tiles (tiny8 64, small12 144 -- 2 of 8 maps).
- **Change:** `target_harvesters(ct)` returns 1 below the area threshold, 3 above it. Used at
  both call sites (sentinel-build gate, navigate-to-core gate). Everything else unchanged.
- **Result:** screen vs incumbent: **35.4%, CI [23.4%, 49.6%] — refuted** (upper bound just
  under 50), discarded without a confirm run.
- **Read:** same mechanism as the scout-first discard just above, in miniature — cutting
  harvesters from 3 to 1 forfeits ~2 harvesters' worth of economy (each ~2.5 Ti/round once
  delivering) in exchange for a slightly earlier sentinel, and the economy loss outweighs the
  earlier defense even on the smallest maps. Combined with the scout-first result, this is a
  second, independent data point that this bot's economy-first shape is robust across the map
  size range — "small map = rush" from strategy-notes.md is not supported so far, at least not
  via this lever.
- **Next:** map-size branching on *something other than the harvester trigger* remains
  untested (e.g. sentinel placement radius, spawn aggressiveness, MAX_BUILDERS) if this is
  revisited. Lower priority now given two discards in a row on the small-map-rush thesis.

### Discard — scout-first before building is a decisive loser

- **Date:** 2026-08-07 · tested against sentinel-first aug7 (a9d81a1)
- **Hypothesis:** open-questions.md asked whether "scout first, build later" (dodging early
  scale tax, per strategy-notes.md) beats building immediately — flagged explicitly as
  worth testing rather than assuming, against the official docs' opposite advice.
- **Change:** gate `_try_build_harvester` on `ct.get_current_round() >= SCOUT_ROUNDS` (20).
  Nothing else built (harvesters, sentinels) for the first 20 rounds either, since sentinels
  are already gated on harvester count.
- **Result:** screen vs incumbent: **8.3%, CI [3.3%, 19.6%] — decisively refuted**, discarded
  without running confirm (upper bound nowhere near 50%).
- **Read:** settles the open question outright, and confirms harvester ROI dominance
  (strategy-notes.md: payback ~8-12 rounds) beats the scale-tax-avoidance argument by a wide
  margin at 20 rounds. The official docs' "build aggressively early" was right about the
  direction, if not the reasoning given. Scale tax matters at the margin (which harvester to
  build, not whether/when to start) — it doesn't justify sitting on your hands.
- **Next:** the scale-tax discipline from strategy-notes.md (don't over-build builder bots,
  `destroy()` obsolete infrastructure) is a different claim than "delay everything" and isn't
  refuted by this result. Worth keeping separate in future tests.

### Discard — raising AMMO_BUFFER for sentinels backfired

- **Date:** 2026-08-07 · tested against the sentinel-first aug7 commit (a9d81a1), not v4
- **Hypothesis:** AMMO_BUFFER=20 was tuned for gunners (4 Ti/shot -> 5 shots buffered); a
  sentinel at 10 Ti/shot only gets 2 shots of reserve at the same number. Raising it to 50
  (5 shots, matching gunner's shot-count buffer) should sustain fire better in a fight.
- **Change:** `AMMO_BUFFER = 20` → `50`. Nothing else.
- **Result:** screen 41.7% [28.8%, 55.7%] (not clearly refuted by the letter of the screen
  rule, but already trending down); confirm **45.3%, CI [39.3%, 51.4%] — no-verdict**,
  leaning negative. Discarded, `git reset --hard`.
- **Read:** the mechanism assumed sustained-fire fights are common enough that a bigger
  buffer pays for itself. More likely what actually happens: most of the match nothing is in
  range, so a bigger buffer just means more Ti parked as idle ammo instead of building
  harvesters/sentinels/conveyors during the quiet phases — exactly the failure mode
  strategy-notes.md already called out for the starter bot's fixed top-up. Bigger ≠ better
  once the buffer covers a couple of shots; the quiet-phase opportunity cost dominates.
- **Next:** an adaptive buffer (top up more only when an enemy is actually visible) is the
  more promising version of this idea, per strategy-notes' "adaptive ammo" note — a fixed
  buffer at any size trades against economy growth. Left for a future experiment.

### aug7 — Sentinel-first defense: the untested strategy-notes guess held, hard

- **Date:** 2026-08-07 · `bots/aug7`, built on v4 · **Not yet submitted** (no platform account)
- **Hypothesis:** [strategy-notes.md](strategy-notes.md) flagged Sentinel as strictly better
  than Gunner for a static base defender (more dmg/round, better Ti-per-damage, more HP,
  2.5x the attack radius, unblockable by walls/units) except for 10 Ti lower entry cost and
  re-aimability — neither of which matters once a turret is placed and never moves. Marked
  "untested guess, needs a real A/B" in the notes.
- **Change:** one conceptual swap. `_try_build_gunner`/`_run_gunner` → sentinel equivalents
  at the same trigger point (`harvester_count >= TARGET_HARVESTERS`), same facing-away-from-
  core logic, same 18-tile-from-core placement gate, same `AMMO_BUFFER = 20`. The only new
  code: sentinels have no `get_gunner_target()`-style helper, so targeting scans
  `get_attackable_tiles()` for the first tile holding an enemy unit or building and fires
  there.
- **Result:**
  - **Screen vs v4 (48 matches): 64.6% [50.4%, 76.6%]** — 5 `core_destroyed` wins appeared
    where the v4-only baseline essentially never had any.
  - **Confirm vs v4 (256 matches): 68.4%, CI [62.4%, 73.7%] — clears the accept gate outright.**
  - 0 crashes both sides. Win conditions shifted hard: 24 `core_destroyed` (up from a
    background rate near zero), plus more `titanium_collected` wins too — sentinels aren't
    just killing cores, they're also denying enemy economy better.
- **Read:** the derivation held, and by a wide margin — this isn't a marginal tuning win,
  it's the biggest single-change jump since v1's crash fix. Best explanation: r²=32 vs r²=13
  means a sentinel covers a conveyor approach a gunner simply can't see, and the unblockable
  line means enemy builder bots can't screen it by standing in front of infrastructure.
  Reinforces the notes' broader point that the tutorials' Gunner-first framing is actively
  wrong for this game, not just suboptimal.
- **Next:** aug7 is now the strongest bot measured. Continue the loop from here — the ammo
  buffer (20 Ti = 2 sentinel shots) was left untouched for attribution; worth its own
  experiment now that sentinels are the default (open-questions.md: adaptive ammo).

### v4 — full direction-neutralisation: the fairness fix turned out to be a strength fix

- **Date:** 2026-08-06 · **Not yet submitted** (no platform account) · **Current best**
- **Hypothesis:** v3's ring spawn removed only part of the measured seat bias (mid20 mirror
  0/32 → 28%, not 50%); carrying over the rest of probe_neutral's neutralisations — randomised
  movement tie-break, randomised ore-scan tie-break, shuffled build/heal scans — should finish
  the job. Expected mostly a fairness change, neutral-to-slightly-positive on win rate.
- **Change:** v2's CPU guard + the complete neutralisation set from probe_neutral. One
  conceptual change vs v3: "remove the remaining absolute-direction tie-breaks".
- **Result:**
  - **vs v3: 60.9%, CI [54.8%, 66.7%], 256 matches — clears the accept gate outright.**
  - vs starter: **74.2%, CI [68.5%, 79.2%]** (v1 was 59.4%), 0 crashes vs 535, tiny8 32/32.
  - Mirror seat split: mid20 53.1%, small12 46.9% — **fair**. tiny8 84.4% — engine effect,
    expected, unfixable.
- **Read:** the surprise is the raw strength gain. Best explanation: v1's fixed tie-breaks
  made every builder chase the *same* first-enumerated target, colliding and shadowing each
  other; randomising de-correlates them into better map coverage. (Also: on biased maps, half
  of all games were previously started from the handicapped seat.) A fairness argument found
  a play-quality bug — absolute-direction habits were costing games everywhere, invisibly.
- **Next:** v4 is the submission candidate. On approval: re-baseline on the real pool before
  any tuning (runbook.md).

### v3 — full-ring spawn only: the decomposition step

- **Date:** 2026-08-06 · superseded by v4 the same day
- **Hypothesis:** the NW-corner spawn scan is the dominant cause of the seat wipeouts.
- **Change:** v2 + spawn candidates = whole 12-tile ring (random choice), nothing else.
- **Result:** mirror mid20 seat A 0/32 → **28.1%** [16%, 45%] — most of the wipeout, not all
  of it. vs v2: 52.0% [45.8%, 58.0%], no-verdict (expected: the fix only pays on the map
  class that exposes the handicap). 0 crashes.
- **Read:** ring spawn is necessary but not sufficient; the residual bias lives in the other
  absolute-direction tie-breaks. Kept only as the attribution step for v4.

### Experiment — seat bias dissected: it was mostly us, and partly the engine

- **Date:** 2026-08-06 · `bots/probe_neutral` (v1 with every absolute-direction bias removed)
- **Design:** if the seat-A wipeouts survive direction-neutralisation in a mirror, they're
  the engine's; if they vanish, they were ours.
- **Result (mirror, 32 matches/map):** mid20 0/32 → **53.1%** and small12 → 46.9% — *ours*.
  tiny8 → **78.1% [61%, 89%] seat-A**, confirmed at 84.4% in the v4 mirror — *the engine's*:
  a genuine first-mover advantage on the 8×8 map that survives full neutralisation.
- **Mechanism found on the way:** `get_position()` is the Core footprint's NW corner, so the
  starter bot's `pos.add(d)` spawn scan reaches only the N/W sides of the legal 12-tile ring
  (`bots/probe_spawn`, tile-by-tile). One seat spawned toward the map corner, the other
  toward the centre, every game.
- **What this changes:** (1) absolute-direction habits are a class of bug, not a style choice
  — audit for them; (2) on tight maps, seat draw is real regardless of bot quality → find out
  how the ladder assigns seats within a best-of-five; (3) our mirror-fairness check (arena
  per-map seat split) is now a standing regression test for reintroduced direction bias.

### Experiment — titanium is credited on Core delivery, and only then

- **Date:** 2026-08-06 · `bots/probe_credit` / `probe_credit_nc` / `probe_idle`
- **Design:** one harvester + one dead-end conveyor (facing away from the core, output onto
  empty ground / off-map), then idle; core logs the balance every round. NC variant: no
  conveyor at all. Passive-only slope is 2.5 Ti/round; a credited harvester would add 2.5.
- **Result:** both variants, 990+ rounds: balance slope **exactly 2.500**,
  `a_titanium_collected` **0**. A dead-end chain and no chain are *identical*: zero.
- **Read:** **"titanium collected" = titanium delivered to the Core.** The tiebreak-#1
  counter and the spendable balance both move only on delivery. An unrouted harvester
  contributes nothing to tiebreak #1 or #3 and no income — it pads tiebreak #2 (harvester
  count) while costing 20 Ti and +5% permanent scale. Chain completion isn't an optimisation,
  it's the whole game. This also closes the loop on the starter bot's economics: its walking
  trails of toward-core conveyors evidently do deliver (balance reconciliation matches), so
  hypothesis (c) from open-questions held.
- **Aside, measured:** `can_build_conveyor()` permits a facing whose output is off-map.

### v2 — CPU-budget guard: bail at phase boundaries, not mid-statement

- **Date:** 2026-08-06 · **Not yet submitted** (no platform account)
- **Hypothesis:** exceeding 10 ms CPU silently truncates the unit's round mid-statement —
  wasted round, possibly half-updated instance state. v1 never approaches the limit locally,
  so the guard should be inert here; its value is ladder hardware (Graviton3, unknown relative
  speed) and future heavier strategy code. Predicted before measuring: no local effect,
  vs v1 reads no-verdict ≈50%.
- **Change:** `_cpu_exhausted()` checks `get_cpu_time_elapsed()` ≥ 8000 µs between builder
  phases (priority: build > heal > move > share); first trip per unit reported to stderr.
  Nothing else.
- **Result:** vs v1: **52.0%, CI [45.8%, 58.0%]**, 256 matches, no-verdict — as predicted.
  vs starter: 56.6% [50.5%, 62.6%] (v1's edge retained). 0 crashes. Guard confirmed never to
  trip locally (zero CPU-GUARD lines across a full instrumented match).
- **Read / rule note:** program.md's gate (lower bound > 50%) is for changes claiming to
  improve play; applied to insurance changes it would auto-discard all of them. Accept rule
  used here, stated in advance: keep unless refuted (upper bound < 50%) or crashes appear.
  Deliberate, documented deviation — not a precedent for strategy changes.

### v1 — robustness only: don't let units delete themselves

- **Date:** 2026-08-06 · **Not yet submitted** (no platform account)
- **Hypothesis:** the starter bot's uncaught exceptions are its single biggest weakness. The
  engine permanently deletes a unit on any escaping exception, so every crash is a unit lost
  for the rest of the match — not a skipped turn.
- **Change:** two things, nothing else.
  1. `run()` wraps a `_dispatch()` in `try/except Exception`, reporting only the first
     traceback per unit to stderr (so a per-round bug can't flood the log or eat the 10 ms
     CPU budget formatting tracebacks).
  2. New `in_bounds()` helper, checked in `_try_move()` before touching the engine.
     `_move_toward_target()` tries up to four directions, and tile queries like
     `is_tile_empty()` **raise** off-map rather than returning False — so every bot standing
     on an edge tile was rolling the dice on its own life.
- **Predicted effect:** large. Stated before measuring.

**Result — 256 matches (8 maps × 16 seeds × both seat orderings):**

| | v1 | starter |
| --- | --- | --- |
| Wins | **152** | 104 |
| Win rate | **59.4%**, 95% CI [53.3%, 65.2%] | — |
| Crashes | **0** | **515** |

Lower bound clears 50%. **Keep.**

**Read:** the hypothesis held, but the effect is *smaller than the crash count suggests*.
515 crashes over 256 matches is ~2 units lost per match per side — real, but with typical
end-of-match unit counts of 5–13 it's usually a wound rather than a kill. The exception is
small maps: on `tiny8` v1 went **31/32**, where losing two bots is losing the whole economy.
So the crash bug's cost scales inversely with map size.

**Worth not over-reading:** per-map splits here are 32 matches each, so their intervals are
±17 points. v1's apparent loss on `vsym16` (13/32) is well inside noise. Only the pooled
verdict is solid.

**New evidence on the seat question:** on `mid20`, seat A lost **0/32** — and v1 took exactly
the 16 of those where it happened to be seat B. Seat decided that map regardless of which bot
sat in it. Since v1 doesn't crash at all, this rules out "crashes cause the seat effect" and
points at an engine/layout interaction. `small12` behaves the same way (2/32). The earlier
`tiny8` wipeout, by contrast, has now vanished (46.9%) — that one *was* crash-driven.

**Next:** v1 is the new baseline. Real strategy changes should wait for `fcode maps sync`;
tuning against eight invented maps risks fitting the wrong distribution. Remaining robustness
work that's distribution-independent: a CPU-budget guard using `ct.get_cpu_time_elapsed()`.

### Baseline — shipped starter bot, measured locally

- **Date:** 2026-08-06
- **Not a submission** — this is the reference opponent everything else gets measured against.
  `bots/starter/main.py` is left exactly as `fcode starter` generated it, on purpose.
- **Setup:** mirror matches, `--tle 10`, on six self-generated maps spanning the pool's
  8×8–30×30 range (see [tooling.md](tooling.md)).

**Results — 5 mirror matches, one per map:**

| Map | Winner by | Units left (A / B) | Mined (A / B) |
| --- | --- | --- | --- |
| tiny8 | Harvesters (tiebreak) | 0 / 5 | 0 / 0 |
| small12 | Titanium collected | 0 / 10 | 0 / 4960 |
| duel16 | Titanium collected | 1 / 7 | 2480 / 2470 |
| mid20 | Titanium collected | 3 / 11 | 2470 / 2480 |
| wide30x14 | Titanium collected | 4 / 13 | 4960 / 2640 |
| large30 | Titanium collected | 12 / 11 | 7450 / 4980 |

**What this establishes:**

1. **Every match went to the round-1000 tiebreak. 6 of 6.** No Core was ever destroyed, in a
   mirror match or otherwise. This is strong support for the economy-first read in
   [strategy-notes.md](strategy-notes.md) — the tiebreak *is* the win condition in practice,
   and its first key is titanium collected.
2. **The shipped starter bot crashes constantly**, 2–9 uncaught `GameError: Position out of
   bounds` per match. Each one **permanently deletes that unit**. Two matches ended with a
   side on **zero units and zero titanium mined** — a total economic wipeout caused entirely
   by its own bug, not by the opponent.
3. Identical bots produce wildly asymmetric outcomes (0 units vs 10) purely from where the
   crashes happened to land. Variance in this game is enormous; **one match proves nothing**.
   Any future comparison needs many matches across many maps and seeds.

**The bug:** `bots/starter/main.py:391` calls `ct.is_tile_empty(next_pos)` without a bounds
check. `next_pos` is off the map whenever a builder is on an edge tile, and the call raises.
`run()` has no `try/except`, so the exception escapes and the engine deletes the unit forever.

**Next:** our v1 is the starter bot plus (a) a top-level `try/except` in `run()` and (b) a
bounds check before that call. Nothing else. If the baseline read is right, that alone should
be a large improvement, and it isolates a single change so the result is attributable.

---

### Seat matters enormously on some maps — measured, cause unknown

- **Date:** 2026-08-06
- **Setup:** `tools/arena.py starter starter`, 16 mirror matches per map (8 seeds × both
  seat orderings), `--tle 10`.

With **identical bots on provably symmetric maps**, the team that acts first (seat A) wins:

| Map | seat A wins | 95% CI |
| --- | --- | --- |
| tiny8 | **0 / 16** | [0%, 19%] |
| small12 | **0 / 16** | [0%, 19%] |
| mid20 | **0 / 16** | [0%, 19%] |
| duel16 | 9 / 16 | [33%, 77%] |
| large30 | 9 / 16 | [33%, 77%] |
| wide30x14 | 10 / 16 | [39%, 82%] |

Three maps are fair. Three hand the win to the second mover **every single time**.

**Ruled out:** map asymmetry. The generator's output was verified tile-by-tile — every map is
exactly symmetric under its declared transform (`asym=0`), with equal ore near each core.

**Not yet known:** whether this is (a) an engine turn-order advantage that only bites on
certain layouts, or (b) the starter bot's absolute-direction bias — it closes the x-gap before
the y-gap and scans `CARDINALS` in a fixed order, so under 180° rotation it genuinely plays
differently from the other seat. A symmetry-type probe was inconclusive: horizontal-mirror
gave 29%, vertical-mirror 54%, and the six rotational maps split 3 fair / 3 wipeout.

**What this changes right now, regardless of cause:**

1. **Never evaluate on a single seat ordering.** On half these maps it would produce a
   perfectly confident, completely wrong answer. `tools/arena.py` plays both orderings
   always, and reports seat split per map rather than pooled.
2. **Pooled statistics lie here.** The 96-match aggregate read 20.8% seat-A — a number that
   describes none of the six maps. Always decompose.
3. **Suspect absolute-direction logic in our own bot.** Whatever the cause, a bot whose
   behaviour depends on which way is "east" is a bot that plays two different games depending
   on which corner it spawns in. Prefer core-relative reasoning to map-absolute reasoning.
