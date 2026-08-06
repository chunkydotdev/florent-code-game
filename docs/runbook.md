# Runbook — approval day, and every time the organisers change something

Two checklists. The first runs the moment platform approval lands. The second runs at
tournament start and again whenever a rules change is announced or suspected — the organisers
said (2026-08-06) that the **map pool has changed and stays hidden until the tournament**, and
that **other variables may be tweaked**. We can't see the changes in advance; what we can do is
make absorbing them a 15-minute procedure instead of a scramble.

The repo is already shaped for this: `docs/reference/` is vendored **so that a re-scrape
diffs**, bots read every cost from `ct.get_*_cost()` / `GameConstants` instead of hardcoding,
the maps in `maps/` were always treated as stand-ins, and no strategy tuning has been done
against them. The checklists below are how those design choices get cashed in.

## 1. The moment approval lands

1. `.venv/bin/fcode login` — browser OAuth via Discord.
2. Commit anything dirty, then **`.venv/bin/fcode maps sync`** — the real pool lands in
   `maps/`. Ours are git-tracked, so the invented set stays recoverable in history.
3. **Census the pool before anything else:** how many maps, and the size histogram
   (8×8 → 30×30). This decides how much the small-map case matters — small maps are where
   bugs are most punishing and where rushing may dominate.
4. Re-baseline on the real distribution:
   `.venv/bin/python tools/arena.py v2 starter --seeds 16`
   Read the per-map table. Note which *real* maps are seat-decided — and remember the seat
   split is only cleanly interpretable in mirror or near-mirror runs.
5. Submit the current frozen candidate — **check [HANDOVER.md](../HANDOVER.md) for which
   version that is**, and if the candidate is still a live edit target (like a `bots/<tag>`
   research dir), freeze it into the next `bots/v<N>` first (Magnus does this; `bots/v*` is
   write-protected). Then `.venv/bin/fcode submit bots/<candidate>`, activate it, and let the
   ladder schedule (first match can take ~10 min).
6. `fcode match test v2 starter` (rate limit: 5 per 10 min) — real ladder hardware
   (AWS Graviton3) with the limit enforced. This is the only way to verify the CPU guard's
   8 ms threshold fits real hardware timing before the ladder does it for us.
7. Answer the platform questions in [open-questions.md](open-questions.md): prize categories,
   team size rules, finals qualification dates, whether seats alternate within a best-of-five,
   whether a ladder API exists.
8. Watch the first few ladder replays (`fcode watch`) and start filling
   [opponents.md](opponents.md) with real observations.

## 2. Tournament-start / rules-change recalibration

Run top to bottom; each step either confirms an assumption or flags exactly what moved.

1. **Re-scrape and diff the docs:**
   `.venv/bin/python docs/reference/scrape.py && git diff docs/reference/`
   Every published rule change becomes an explicit diff. Fold changes into
   [game-model.md](game-model.md), then re-derive whatever [strategy-notes.md](strategy-notes.md)
   built on the changed facts. (Scrape from the `/docs` index, never the JS bundle — the
   bundle under-lists routes; see the comment in `scrape.py`.)
2. **Check for a new engine:** `.venv/bin/pip index versions fcode`, upgrade if bumped, and
   note the version in [tooling.md](tooling.md). The engine `.so` is where unannounced
   behaviour changes would live.
3. **Re-run the probe suite** (minutes, all offline):
   - `fcode run probe_spawn probe_spawn maps/mid20.map26 --tle 10 2>&1 | grep SPAWNPROBE`
     → re-verifies the spawn ring geometry and starting titanium in one shot.
   - `tools/arena.py v2 starter --seeds 8` → a baseline shift (v2 has sat near 56% vs
     starter) is the tripwire for a behaviour change nothing announced.
4. **`fcode maps sync` again** — the pool visible at approval time may not be the
   tournament pool.
5. **Re-verify the assumptions that are NOT queryable from the API** (grep for them; these
   are the only numbers we hardcode on purpose):
   - the 10 ms CPU limit → `CPU_BUDGET_US = 8000` in `bots/*/main.py`, and `--tle 10`
     defaults in `tools/arena.py` and every command in the docs
   - round cap, tiebreak order, Elo K-factor / fractional-series scoring
     (game-model.md "Ladder & rating") — these shape strategy, not code
6. **If `GameConstants` values changed**, update the tables in game-model.md and check every
   strategy-notes derivation that quotes them (harvester ROI, heal-vs-damage economics,
   scale-tax table).

## Standing rule while variables are uncertain

Prefer changes that are **distribution-independent** (robustness, correctness, dodging
self-imposed handicaps) over map-tuned strategy. Everything accepted so far — v1's crash
guard, v2's CPU guard — survives any map pool and any cost tweak by construction. Deep
strategy tuning starts only after the real pool is in `maps/`.
