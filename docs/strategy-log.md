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
