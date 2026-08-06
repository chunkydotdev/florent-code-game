# program.md — autonomous bot research loop

Adapted from [karpathy/autoresearch](https://github.com/karpathy/autoresearch)'s `program.md`.
Same shape: an agent edits one file, measures against a fixed harness, keeps or discards, and
repeats unattended. The structure carries over directly. **The accept rule does not** — see
"Why the accept rule is different" below, which is the whole reason this file isn't a copy.

## Who runs this — model tiering

The loop is deliberately harness-gated: the arena and the Wilson accept rule do the judging,
so the runner needs competence, not brilliance. Run it on the cheap tier by default and spend
the expensive tier only where judgment actually lives.

- **Sonnet — the default runner.** The whole loop: pick one hypothesis (strategy-notes and
  open-questions first), edit `bots/<tag>`, screen, confirm, log. Also the pre-written
  probe experiments in open-questions.md, and runbook §1 when approval lands.
- **Haiku — mechanical re-runs only.** Recalibration probe/arena re-runs (runbook §2),
  reporting numbers verbatim. Not for editing bot code.
- **Fable/Opus — on triggers, sparingly.** (1) A result that surprises or contradicts
  game-model.md — per the log's own rule, that's a fact to be understood, not a tweak.
  (2) Designing a new experiment methodology. (3) Any change to the harness, maps,
  program.md, or frozen bot versions — also permission-blocked for everyone in
  `.claude/settings.json`; changes go through Magnus. (4) The every-~10-accepts incumbent
  audit (winner's-curse retest below). (5) Post-approval pool census interpretation and any
  strategy re-derivation after a rules diff.

**Escalation triggers — stop the loop and report rather than improvise:** the baseline
sanity check fails; the harness or maps look wrong; 20+ consecutive no-accepts; a result
contradicts game-model.md; the task needs a protected file edited.

**Session hygiene for cheap runs:** one session per run tag; arena output goes to a file and
only the printed summary is read back (never full match logs into context); results.tsv is
append-only tape — never rewrite history.

## Setup

1. **Agree a run tag** with the human — e.g. `aug6`. The branch `research/<tag>` must not
   already exist.
2. `git checkout -b research/<tag>` from the current default branch.
3. **Read for context:** `AGENTS.md` (rules + API), `docs/game-model.md` (ground truth,
   including the errors in AGENTS.md), `docs/strategy-notes.md` (derived analysis and the
   hypotheses worth testing), `docs/strategy-log.md` (what's already been tried).
4. **Confirm maps exist:** `ls maps/*.map26`. If empty, `python3 tools/make_map.py`. If a
   platform account exists, prefer `fcode maps sync` — the real pool beats our guesses.
5. **Create the challenger:** `cp -r bots/starter bots/<tag>`. This is the only file you edit.
6. **Establish the baseline** before changing anything: run the harness challenger-vs-starter
   unmodified. It should come out ~50%. If it doesn't, stop and tell the human — the harness
   is broken and every subsequent result would be meaningless.

## Scope

**You may edit:** `bots/<tag>/main.py` only. Architecture, strategy, heuristics, unit
composition, build order — all fair game.

**You may NOT edit, for any reason:**
- `tools/arena.py` — the evaluation harness. This is the ground-truth metric.
- `tools/make_map.py` and `maps/` — the test distribution.
- `bots/starter/` — the reference opponent and the anchor of the whole ladder of versions.

If the harness or the maps look wrong, **stop and report it to the human**. Do not fix them
mid-run. An agent that can edit its own scoreboard will, eventually and without meaning to,
optimise the scoreboard instead of the bot. This is the single most important rule here.
(As of 2026-08-06 it is also mechanically enforced: `.claude/settings.json` denies Edit/Write
on the harness, maps, starter, frozen `bots/v*`, probe bots, and this file.)

**Never** weaken a test to make a change pass.

## The metric

```bash
.venv/bin/python tools/arena.py <tag> starter --seeds 8
```

Win rate against the opponent pool, with a Wilson 95% interval. Higher is better.

### Why the accept rule is different from autoresearch

autoresearch compares `val_bpb` floats and keeps anything lower. That works because its metric
is nearly deterministic. **Ours is not.** Two identical bots here have finished 0-units vs 10.
At 96 matches the interval is roughly ±10 points, so a genuinely neutral change reads ≥55%
about one run in six. "Keep if the number went up" would keep noise, ~17% of the time,
forever, and the branch would drift on accumulated luck while the log claimed steady progress.

**The accept rule is therefore: keep a change only when the Wilson lower bound clears 50%.**
`tools/arena.py` prints exactly this and declines to name a winner otherwise. A result of
"no verdict" is a **discard**, not a maybe.

Run it in two stages to keep the loop fast:

1. **Screen** — `--seeds 3` (~36 matches, ~15s). Discard immediately if the *upper* bound is
   below 50%: it's already refuted, don't spend more on it.
2. **Confirm** — `--seeds 16` (~192 matches, ~2 min) for anything that survives the screen.
   Only a confirm run can promote.

### Guarding against fooling yourself

- **Re-test the incumbent every ~10 accepted changes** against the version 10 steps back.
  Anything selected as "best so far" on a noisy metric is inflated by the winner's curse; this
  catches a branch that has drifted on luck rather than improved.
- **Evaluate against a pool, not just the last version.** Once 3+ versions exist, run the
  challenger against `starter` *and* two earlier versions. A bot tuned to beat exactly one
  opponent has learned that opponent, not the game — the classic self-play failure.
- **The maps are ours, not the organisers'.** Until `fcode maps sync` has run, treat
  map-specific tuning as untrustworthy. Prefer changes that are robust across all six maps
  over changes that win big on one. `arena.py` reports per-map for this reason.
- **Report per-map, never pooled.** Seat A goes 0/16 on three of our maps and ~56% on the
  others; the pooled average describes neither. See `docs/strategy-log.md`.

## Logging

Append to `results.tsv` (tab-separated; leave it untracked). Columns:

```
commit	winrate	ci_low	ci_high	n	status	description
```

`status` is `keep`, `discard`, `no-verdict`, or `crash`. Use `0` for the rate on a crash.

```
commit	winrate	ci_low	ci_high	n	status	description
a1b2c3d	0.502	0.431	0.573	192	keep	baseline, challenger == starter
b2c3d4e	0.681	0.612	0.743	192	keep	try/except in run() + bounds check
c3d4e5f	0.523	0.452	0.593	192	no-verdict	prefer Sentinels over Gunners
```

When a change is **kept**, also write a proper entry in `docs/strategy-log.md` — hypothesis,
change, result, and what it means. `results.tsv` is the raw tape; the log is the reasoning.
Discards worth remembering (a plausible idea that measurably failed) belong there too.

## The loop

```
LOOP:
  1. Check git state — current branch and commit.
  2. Pick ONE change. One per experiment, or the result isn't attributable.
     Draw from docs/strategy-notes.md and docs/open-questions.md first; those are
     already-reasoned hypotheses waiting for a measurement.
  3. Edit bots/<tag>/main.py. git commit.
  4. Screen:  .venv/bin/python tools/arena.py <tag> starter --seeds 3  > /tmp/screen.log 2>&1
     Read the summary only. Do NOT let full match output into context.
  5. Refuted by the screen (upper bound < 50%)? git reset --hard HEAD~1, log discard, next.
  6. Confirm: --seeds 16. Lower bound > 50% → keep the commit and advance.
     Otherwise git reset --hard HEAD~1 and log no-verdict.
  7. Record in results.tsv. If kept, write up docs/strategy-log.md.
```

**Crashes:** a crash is information — the engine permanently deletes a unit on any uncaught
exception, so a bot that crashes is losing units, not just erroring. Check the harness's crash
count on every run, not just the win rate. A change that improves win rate *and* raises the
crash count is suspect. Trivial bugs (typo, missing import): fix and re-run. Fundamentally
broken idea: log `crash` and move on.

**Timeout:** a `--seeds 16` run should take ~2 minutes. Kill anything past 10 and treat it as
a failure — most likely the change blew the 10 ms CPU budget, which is itself a finding worth
logging.

**Keep going.** Once the loop starts, don't pause to ask whether to continue — the human may
be asleep and expects to wake to results. If you run out of ideas: re-read
`docs/strategy-notes.md` for untested claims, re-read `docs/open-questions.md` for open
experiments, combine previous near-misses, or try something structurally radical. Two genuine
reasons to stop and wait for a human, though — this differs from autoresearch, because unlike
a fixed validation set our metric can actually go bad:

- the baseline sanity check fails, or the harness/maps look wrong (see Scope)
- 20+ consecutive experiments with no accepted change **and** no untested hypotheses left —
  at that point the bottleneck is ideas or the map distribution, and burning tokens on random
  perturbation is worse than stopping
