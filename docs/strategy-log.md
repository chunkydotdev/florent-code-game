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
