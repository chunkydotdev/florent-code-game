# Handover — 2026-08-06

Written as the first session's context closed. Start here, then read
[README.md](README.md) → [docs/game-model.md](docs/game-model.md) →
[docs/strategy-log.md](docs/strategy-log.md).

## Where we are

Everything is set up and **we can run and measure matches offline**. What we can't do is
touch the actual competition.

- `fcode` 2.3.6 in `.venv` (Python 3.13). Project scaffolded, `bots/starter` untouched as the
  reference opponent.
- **`bots/v1` is the current best bot.** Robustness fix only, measured at **59.4%** against
  starter over 256 matches, CI [53.3%, 65.2%], crashes 515 → 0.
- All 23 official docs pages and 24 tutorial steps scraped and vendored in `docs/reference/`.
  The model derived from them is in `docs/game-model.md`, with facts verified in a real match
  marked `[measured]`.
- `tools/make_map.py` generates `.map26` maps offline; `tools/arena.py` runs statistically
  honest bot-vs-bot evaluation; `program.md` is the protocol for running improvement
  unattended (adapted from karpathy/autoresearch, with a statistical accept gate).

## The one blocker

**Nobody has registered at https://game.code.florent.vc.** Sign-in is *Continue with Discord*,
and approval is not automatic (there are `/application-pending` and `/application-denied`
routes). Until that happens there is no `fcode login`, no ladder, no submissions, and — most
importantly — **no real map pool**.

This is a human task. It gates more than it looks like it does.

## Do these first, in this order

1. **Register.** Everything below is better after it.
2. **`fcode maps sync`**, then re-run `tools/arena.py v1 starter --seeds 16` on the real pool.
   Our eight maps are inventions; some conclusions may not survive contact with the real
   distribution. Check the map-size histogram — it determines how much the small-map case
   matters, and small maps are where bugs are most punishing.
3. **Submit v1** and get a ladder baseline. It's robustness-only and safe.
4. **Then** start strategy work, either by hand or via `program.md`.

Distribution-independent work that can be done *before* registration, if you'd rather not
wait: a CPU-budget guard using `ct.get_cpu_time_elapsed()`. Exceeding 10 ms silently truncates
a unit's turn, and `fcode run` doesn't enforce it unless you pass `--tle 10` (always pass it).

## Traps that will waste your time

- **The default `python3` is 3.14 — `fcode` does not support it.** Use `.venv/bin/python`.
- **`fcode run` enforces no CPU limit by default.** Always `--tle 10` or you'll develop a bot
  that dies on the ladder.
- **`print()` does not go to stdout** — it's captured into the replay. Use `stderr`.
- **Never evaluate on one seat ordering, and never pool the per-map numbers.** On some maps
  seat decides the winner outright (`mid20`: seat A lost 0/32 even with a non-crashing bot).
  A single-ordering test produces confident nonsense. `tools/arena.py` handles both; don't
  hand-roll a comparison.
- **One match proves nothing.** Identical bots have finished 0-units vs 10.
- **When scraping the docs, enumerate from the `/docs` index page, not the JS bundle.** The
  bundle lists only 13 of 23 routes. This cost the first session 10 pages, including the ones
  answering questions it had filed as unknowns. `docs/reference/scrape.py` has the right list
  and a comment about it.
- **`AGENTS.md` / `CLAUDE.md` are the organisers' own context file** and are mostly excellent,
  but contain two known errors: cost scale "starts at 1.0" (the API returns 100.0, measured),
  and a Core spawn radius that contradicts the rules page. `docs/game-model.md` wins on
  conflicts — it's the only document reconciled against measurement.

## Strategy state

`docs/strategy-notes.md` has the reasoning; the headlines:

- **Economy is the win condition in practice.** Every match so far ended at the round-1000
  tiebreak, never by Core destruction, and the first tiebreak key is titanium collected.
- **Builder Bots cost +20% cost scale each** — same as a Sentinel, 4× a Harvester. The starter
  bot's spawn-every-round habit is the most expensive thing it does. Bot count is a strategic
  decision. This is the biggest untested lever we know of.
- **Healing (4 HP / 1 Ti) badly out-economies damage.** Sabotage only works on undefended
  infrastructure.
- **`destroy()` is free, uncooldowned, unlimited per round**, refunds in-transit stacks, and
  hands back cost scale. Nothing in the tutorials or starter bot uses it.

## Open questions, ranked

Full list with methods in [docs/open-questions.md](docs/open-questions.md). Most valuable:

1. **Why does seat decide some maps?** Engine turn order, or absolute-direction bias in the
   bot? Discriminating test is written up: run a mirror with a direction-neutral bot. Matters
   beyond the harness — if the ladder doesn't alternate seats across a best-of-five, seat draw
   could swing whole series.
2. **What are the prize categories?** €20K goes to "category winners", so raw ladder rank may
   not be the only target. Could change what we optimise for.
3. **What exactly does tiebreak #1 count** — titanium *collected* or *delivered to core*? The
   docs say both. If delivered, an unrouted Harvester scores nothing.
4. **Core spawn radius r²=2 or r²=8?** Docs contradict. Affects a boxed-in Core.

## Commands

```bash
.venv/bin/fcode run v1 starter maps/mid20.map26 --tle 10        # one match
.venv/bin/python tools/arena.py v1 starter --seeds 16           # 256 matches, ~30s
.venv/bin/python tools/make_map.py                              # regenerate maps
.venv/bin/fcode watch replay.replay26                           # visualiser
```

## Not done

- No `git remote` — the repo is local only.
- `results.tsv` is deliberately untracked (per `program.md`), so it lives only on this machine.
- The `~/Projects/dev-knowledge` vault has **not** been updated for this session. Two lessons
  from today are meta-level and belong there rather than here: *enumerate documentation from
  its index, not from a JS bundle*, and *when a metric is noisy, the accept rule must be an
  interval, not a comparison*. A daily retro note may also be due.
