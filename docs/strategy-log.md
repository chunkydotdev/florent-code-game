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
