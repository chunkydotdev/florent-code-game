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

**Platform timestamps are UTC = local − 2h** (`fcode match list`/`match info` dates).
Verified 2026-08-07 19:10 by the research arm: the 15:58–15:59 platform rows are the
incoming-UR triple that completed ~17:58 local (session-13 coordination note). Convert
before comparing platform match times to coordination.md notes, tape rows, or `date`
output — a "two-hour-stale" match list is usually current.

**Replay-decode gotchas** (v68 read, 2026-08-07, research arm — the decode
scripts died with that session; these are the two things a rebuild must know):

- The engine **re-emits `placeEntity` with the same entity id when a gunner
  rotates**. Naive placeEntity counting inflates gunner counts 2-5x — dedupe all
  turret counts by entity id and report rotations separately. (The v68 walker
  cross-validated against `tools/replay_census.py -v` with exact agreement on one
  game, so census appears safe, but any fresh parser must dedupe.)
- **Chain-wiredness is the delivery-continuity metric**: fraction of live
  conveyors actually wired through to the core, plus cumulative delivered-Ti
  per round (`core_deliv * 10 == titaniumCollected` holds and is a good parser
  sanity check). This metric is what exposed v68's delivery-freeze defect
  (e.g. 95 conveyors alive, 1/95 wired, delivery frozen from r59) — see
  docs/research/v68-chokewall-first-read-2026-08-07.md for the reference
  numbers.
- **Per-source damage attribution: never trust `replay_lib`'s built-in
  split on multi-source rounds** (v72 bleed decode, 2026-08-08): when several
  sources damage the same entity in one round it mis-credits the total to one
  source (measured: a builder bot credited 5,359 dmg whose true figure was
  1,598). Always recompute per-turret damage from `Fire` events keyed by
  `shooter_id`; builder-attack damage is the residual after turret fire.
- **Launcher throws do NOT emit `FireTurret`** (that's gunner/sentinel shots
  only — a naive fire-count on launchers reads 0 forever). A throw appears as
  a `moveBuilderBot` whose `to` is more than one tile from `frm` (builders
  otherwise only step one cardinal tile). Attribute the thrower as the
  launcher alive at **d² ≤ 2 of the pre-throw tile — diagonals included**
  (corrected by the CAD v116 read, 2026-08-07 overnight: the original
  orthogonal-only rule returned NONE for 6 of 14 throws in one match; since
  d²≤1 is a subset of d²≤2, prior attributions are unchanged and the ferry
  ownership-inversion verdict is unaffected — the fix only adds coverage).
  Attribution matters: the ferry re-check (see cad-ferry-premortem re-check
  resolution) found every long-game throw loop belonged to the DEFENDER
  disposing of the attacker's raiders — same tiles, same counts, inverted
  ownership.

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

## Cross-batch win-rate deltas are not trustworthy at n=120 (builder measurement, overnight 2026-08-08)

Non-interleaved 120-game legs against opp_v69 spread ~10 percentage points
SAME-BINARY on this machine (measured during the piece-U anomaly diagnosis;
retro-caveat applied on the coordination tape to every cross-batch vs-parent
delta from that night). Two independent noise sources stack: opponent-side
nondeterminism (x3r0-fork spawn salt; also the tb-decode's 6-vs-1 freeze
incidence across legs, worth ~5 games alone) and batch conditions. Per-leg
Wilson intervals stand; DELTAS between separately-run batches don't resolve
10-15pp effects at n=120. Standard going forward: deterministic-paired runs
(all-sides noise-off, paired seeds, protobuf turn-differ — **tools/det.py** +
**tools/rdiff.py**, validated + promoted 2026-08-08 s16) or interleave both
variants in the same batch (**tools/pair.py**). det caveat: per-map flips are
chaos-bounded — identity results are gold, small flip counts are butterfly-
sensitive; don't over-read them as attribution.

## Determinism references for local runs (2026-08-07, session 12)

`bots/starter` calls unseeded `random.shuffle/choice/randrange` (main.py:167,315,372,450)
and produces different replays on identical (map, seed, tle) — measured md5-divergent at
--tle 0 with PYTHONHASHSEED=0, outcomes up to 1000 turns apart. It is UNUSABLE as a
determinism reference for any harness. Use `bots/opp_v63` (no random import, measured
byte-identical across repeat runs) as the deterministic opponent for replay-equivalence
checks.

## get_cpu_time_elapsed() is a stub under local `fcode run` (measured 2026-08-07, session 14)

The local engine returns **0** from `ct.get_cpu_time_elapsed()` on every call —
CPU metering exists only on the platform. Consequences: (1) any bot's CPU
self-guard (e.g. a `CPU_BUDGET_US` bail-out) is dead code locally and cannot be
smoke-tested; (2) local TLE behavior differences between versions are NOT
evidence of code changes (confirmed the v67-vs-v68 TLE delta was platform
variance, not a fix). To measure a routine's real cost locally, wrap it in
`time.perf_counter()` inside the bot temporarily (example: the piece-KF
live-gun scan measured median 13.7 µs / p95 18.2 µs per call this way).

## Engine stub lies about allied-core passability (research find, builder-verified 2026-08-08)

The local fcode stub `.venv/.../fcode/_types.py` (is_tile_passable docstring,
~:345-349) claims a builder can stand on "a conveyor, splitter, or the allied
core". The allied-core clause is FALSE: organiser docs, game-model.md:202, and
0/185,029 corpus bot-rounds standing on a core footprint all refute it (bleed
doc §10 ground-truth section). Conveyor/splitter passability is real and
OWNERSHIP-BLIND (18,363 bot-rounds measured standing on ENEMY conveyors).
Anyone reading the stub for movement/spawn logic inherits the core error;
also note can_spawn requires PASSABLE, not EMPTY.

## Raw occupancy ≠ blocked — apply the passability predicate before calling a tile denied (research, 2026-08-08)

A tile holding a building is not necessarily unusable by builder bots:
conveyors and splitters are bot-passable, EITHER TEAM'S (measured: 18,363
bot-rounds standing on enemy conveyors in the v72 corpus, 7,075
bot-on-conveyor observations in the v73 read, zero on any other building
type), and builders act normally from atop them (89.3% of v72 episode
core-heals fired from on a seat conveyor). Any decode counting
"blocked"/"denied" tiles must split occupancy by the impassable set — other
builders, walls, every building EXCEPT conveyor/splitter — or it overstates
blocking by up to an order of magnitude (v72 L1: raw 4.8-8.0/8 seats →
truly impassable 0-1; bleed doc §10).

## Spawn-block claims must use the passable predicate, not emptiness (research, 2026-08-08)

can_spawn requires a PASSABLE tile in the core's action range, not an EMPTY
one (official docs :138; corroborated: 244/715 observed spawns = 34% landed
on previously-paved tiles). A spawn-block measurement built on is_tile_empty
produces false "fully blocked" verdicts — v72 L2's "free==0 everywhere"
secondary trap had 1-10 truly spawnable tiles in every cited round and is
retired as an artifact (bleed doc §10.4). The 18-spawn lifetime ceiling
finding survives independently and was strengthened by the retraction.

## NOISE_ON bots are not self-identical run-to-run — pin it OFF for any identity/ablation claim (hse worker, 2026-08-08)

NOISE_ON=True seeds spawn_salt from a live random.Random(), so the same bot
on the same (map, seed) produces different games across runs (measured: same
binary vs itself, winners at turn 101 vs 77). Consequence: every toggle-off
identity check, byte-identity claim, or A/B ablation in the Eir family is
VOID unless BOTH sides are pinned NOISE_ON=False in scratch copies. The
canonical bots keep NOISE_ON=True (the ladder wants the salt); the pin
belongs in the test copies only.
