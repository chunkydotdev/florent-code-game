# Tooling

Local setup and the two workarounds that let us develop without a platform account.

## Environment

The machine's default `python3` is **3.14, which `fcode` does not support**. Use 3.13:

```bash
python3.13 -m venv .venv
.venv/bin/pip install fcode        # 2.3.6 as of 2026-08-06
```

`fcode` ships the engine as a compiled `.so` (`fcode_engine.cpython-313-darwin.so`, exporting
one function, `run_game`) plus the CLI and visualiser in plain Python/JS. The wheel is
version-specific — a 3.13 venv gets the `cp313` wheel.

Always run local matches with `--tle 10`. Without it `fcode run` enforces **no** CPU limit,
so you can develop a bot that dies on the ladder.

## Generating maps offline

`fcode starter` leaves `maps/` empty and tells you to log in and run `fcode maps sync` — the
competition pool lives on the platform. Without an account there are no maps, and without maps
you can't run a single match.

`tools/make_map.py` fixes that. `.map26` is protobuf; the schema is recoverable from the
bundled map editor's JS (`fcode/data/visualiser/assets/map-editor-*.js`, message
`battlecode.Map`), and the script writes the format directly with a ~30-line varint encoder —
no protobuf dependency.

```bash
.venv/bin/python tools/make_map.py          # writes six maps into maps/
.venv/bin/fcode run starter starter maps/mid20.map26 --tle 10
```

The defaults deliberately span the pool's full 8×8–30×30 range, since map size is likely the
biggest single variable in strategy choice. Schema, constraints, and the symmetry rules are
documented in the script's docstring.

**These are our guesses at maps, not the real pool.** Replace them with `fcode maps sync`
output the moment we have an account — a strategy tuned against home-made maps is tuned
against the wrong distribution.

Two other routes to a map, for reference:
- `fcode map-editor` serves the real editor from `localhost` with no login, and it can export
  `.map26` — usable, but it's a GUI, so no good for scripted generation.
- The editor also imports/exports **PNG** maps, one pixel per tile, palette:
  `#000000` empty, `#44465E` wall, `#5AD4FF` titanium ore, `#FFBF40` core A, `#6EAAFF` core B.
  Handy for eyeballing or hand-drawing a map; the engine itself only reads `.map26`.

## Getting instrumentation out of a match

`print()` inside `run()` does **not** appear on stdout — it's captured into the replay and
shown in the visualiser. **Use `stderr` for console output** instead:

```python
import sys
print(f"PROBE r={ct.get_current_round()} ti={ct.get_global_resources()}", file=sys.stderr)
```

```bash
.venv/bin/fcode run mybot starter maps/duel16.map26 --tle 10 | grep PROBE
```

Prefix probe lines with a unique tag so they're greppable. This is how the turret-firing,
starting-titanium, and cost-scale questions in [game-model.md](game-model.md) got settled.

If you only have `print()` output (e.g. from a bot you don't want to modify), the replay is
protobuf with the debug strings stored plainly, so `strings replay.replay26 | grep TAG` also
works — but stderr is simpler and doesn't need the replay written at all.

Uncaught exception tracebacks, by contrast, *do* go to stderr during `fcode run` — which is
how the starter bot's crash bug was spotted (see [strategy-log.md](strategy-log.md)).

## Two traps in the local harness (both measured 2026-08-08)

- **The bot-code validator rejects `try`/`finally`.** Submitting or running a bot whose
  `main.py` contains a `finally:` block fails outright with
  `ValueError: <bot>/main.py:557: 'finally' blocks are not allowed`. Undocumented anywhere in
  the organisers' pages. Wrap-and-restore instrumentation patterns have to be written as
  call-then-report instead. `try`/`except` is fine — and mandatory, see game-model.md.
- **`ct.get_cpu_time_elapsed()` is inert under `fcode run`, even with `--tle 10`.** It read 0
  before and after a 500,000-iteration loop that `time.process_time()` clocked at ~22 ms, and
  produced zero non-zero deltas across ~55,000 sampled builder-rounds. So the shipped CPU guard
  never trips locally *because the counter never moves*, not because we are fast. **To profile
  a change's CPU cost locally, instrument with `time.process_time()`**; leave the shipped guard
  on `ct.get_cpu_time_elapsed()`, which is the real signal on ladder hardware. The only genuine
  verification of a CPU-heavy change is `fcode match test` on AWS Graviton3, where the limit is
  enforced — and that is a rate-limited platform command, so budget it.

## Self-play: `tools/arena.py`

`fcode run BOT_A BOT_B` already plays our bots against each other — that's the whole
mechanism. What it doesn't give you is a trustworthy answer, because variance in this game is
enormous (identical bots have finished 0-units vs 10) and seat matters hugely on some maps.

`tools/arena.py` wraps it:

```bash
.venv/bin/python tools/arena.py v1 starter --seeds 8      # ~96 matches, ~1 min on 8 cores
.venv/bin/python tools/arena.py starter starter           # measure the noise floor
```

- plays every (map x seed) in **both seat orderings** — non-negotiable, see below
- runs matches in parallel, reports a Wilson 95% interval, and **refuses to name a winner**
  while the interval straddles 50%
- counts uncaught-exception crashes per bot (each one permanently kills a unit)
- reports the seat split **per map**, never pooled

That last point is load-bearing. Seat A goes 0/16 on three of our six maps and ~56% on the
other three; the pooled average reads ~21%, which describes none of them. Any evaluation run
on one seat ordering, or summarised pooled, will produce confident nonsense. See
[strategy-log.md](strategy-log.md) for the measurement.

## Probe bots

Throwaway single-question bots, kept in `bots/` because the recalibration checklist
([runbook.md](runbook.md)) re-runs them whenever the organisers change anything:

- **`probe_spawn`** — logs `can_spawn()` over every tile near the Core at round 0, then
  resigns. Settled the spawn-ring geometry; re-verifies it plus starting titanium in seconds.
- **`probe_neutral`** — v1 with every absolute-direction bias removed. Mirror it through
  arena.py to measure *engine-side* seat effects with bot bias excluded.
- **`probe_credit` / `probe_credit_nc` / `probe_idle`** — one harvester plus one dead-end
  conveyor (or none), against a do-nothing opponent, with the core logging the balance every
  round. Settled delivery-only crediting.

Gotcha discovered writing them: **Python's `random` is not seeded by `--seed`** — two runs of
the same command diverge. arena.py's many-match design absorbs this; a single probe run that
depends on exploration may need a retry (probe_credit walks to the map centre until ore is
visible for this reason).

## Determinism references for local runs (2026-08-07, session 12)

`bots/starter` calls unseeded `random.shuffle/choice/randrange` (main.py:167,315,372,450)
and produces different replays on identical (map, seed, tle) — measured md5-divergent at
--tle 0 with PYTHONHASHSEED=0, outcomes up to 1000 turns apart. It is UNUSABLE as a
determinism reference for any harness. Use `bots/opp_v63` (no random import, measured
byte-identical across repeat runs) as the deterministic opponent for replay-equivalence
checks.
