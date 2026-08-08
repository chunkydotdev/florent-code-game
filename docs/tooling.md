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

Second measured instance with VERDICT-FLIPPING stakes (archb residual decode,
2026-08-08): counting paved seats as blocked inverts a heal-seat free-count
1-free vs 5-free (2,313 co-located tile-rounds in the two archipelago-b
replays) — the archb owner verdict ("idle reserve", not seat starvation)
depends on getting this right. Independently corroborated the same day by the
ouro re-freeze spec's damage-target law (builders take hits while standing on
conveyors). This is now a standing decoder self-check: any free-seat or
denial count in a deliverable should state which impassable set it used.

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

## Predictions on homeostatic machinery must be stated as ratios (research method rule, builder-placed 2026-08-08)

A fix to self-regulating machinery (heal loops, conscription, budget governors)
changes the EQUILIBRIUM, not the throughput: a working conscription fix can
show LOWER staffing and LOWER heal totals because the core stops bleeding and
the machinery stands itself down. Absolute-form predictions ("staffing ≥3",
"heal/100r ≥1200") produced 4 false FAILs in the archb signature check that a
naive reader would have scored as model-refuted; the ratio forms (heal ÷
incoming, rounds-at-full-HP) all PASSED. Rule: pre-stated replay signatures on
homeostatic mechanisms use ratios or equilibrium observables, never absolute
staffing/throughput. (archb-residual-owner addendum §A.)

## Paired SHAPE corpora need NOISE_OFF, same as identity claims (research find, builder-placed 2026-08-08)

NOISE_ON draws spawn_salt from OS entropy per process — paired-seed runs
diverge at r0-r3 before any candidate mechanism can fire (kladde addendum:
29/30 pairs diverged pre-r3; the 1/30 byte-identical pair confirms the harness
is otherwise sound). A noisy paired corpus supports NO per-game ΔT or shape
claims — only pooled distributions at ≥20 seeds/cell. Rule: game-shape or
length-distribution corpora run NOISE_OFF (or accept pooled-only reads).
Extends the existing NOISE_ON identity-claim rule; same root cause.

## Platform version binding is at match CREATION, not activation — read the meta before claiming a row (builder, 2026-08-08, s18)

Ladder matches are created on a fixed cadence — **`:x2:43` every ten minutes**
in every archived meta — and a match's `teamXVersion` is bound at
`createdAt`, not at completion. A ship that activates inside a ten-minute
window therefore leaves the NEXT completed match ambiguous: it may still
belong to the outgoing version.

Measured case (the one that produced this rule): `b4287ac4` completed at
13:46:52Z and was credited to v80 in the ship note written at 13:47; its
meta stamps **v79**, because `createdAt` was 13:42:43Z — four minutes
before activation. Correcting it moved v79's final record from −43.9/7 to
−38.1/8 and v80's baseline from 1557.1@396 to 1562.9@397.

**Rule: after any activation, read the next completed match's meta version
stamp before claiming it for the new version.** Baselines and window
arithmetic both depend on it, and the swap rule's holder-window prices only
the current holder's matches, so a misattributed row shifts a slot decision.

**Corollary — the cadence is a side channel.** Ladder creations are
clock-regular and challenge creations are ad hoc, so wall-clock time
discriminates rated from unrated play. We do not build against it; noting it
because our own timing-derived inferences (this rule included) rely on the
same regularity, and because an opponent could in principle read it.

## Unrated results carry DIFFERENT version stamps than ladder results — because of creation-time binding, not challenge-time selection (corrected 2026-08-08, s18)

**Corrected claim.** An earlier version of this entry said a team could choose
which of its own submissions an unrated challenge runs. It cannot: `fcode match
unrated OPPONENT_ID` exposes only `--match` (which picks the OPPONENT's
submission from a given match) and `--map` — verified against the CLI. Our own
side always runs the ACTIVE submission.

**What actually produces the spread**, and it is the rule from the entry above:
version binds at match CREATION. A team that re-activates frequently (measured:
Jython v102→v103 inside an hour) leaves older ladder matches stamped with older
versions than a challenge fired minutes later. Same regularity, different
mechanism.

**The practical rule is unchanged: version-stamp both sides from the match meta
before comparing any unrated result to a ladder result.** Stamps genuinely
differ across time; just not because anyone selected them. Unrated legs also
flip seats between challenges (older trap, still live).

Related refuted claim, kept as the worked example: a "rated detector"
accusation (team loses unrated, wins rated) was refuted from the match list —
same version v102 on all four matches, two of three unrated series actually
WON, single loss screenshotted. Series variance at 5 games is wide; demand
the version stamps and the full series before believing a behavioural claim
about an opponent.

## Platform CPU headroom is THIN for both heads — measured, not assumed (builder, 2026-08-08, s18)

`fcode match test BOT_A BOT_B` runs a remote 5-game match between two LOCAL
bot dirs with real TLE enforcement (AWS Graviton3), no submission and no
ladder exposure. **Its replays carry `BotOutput.execTimeUs` and `tled`
populated — local `fcode run` replays do not** (field absent, measured), so
this is the ONLY way to profile per-turn CPU without shipping.

First real measurement (match `80d351e6`, `_v95e1` = E1+M2b+FT2 head vs
`_v94fb` = staged head, 5 games / ~14k unit-turns per side):

| head | median execUs | p95 | max | TLED |
|---|--:|--:|--:|--:|
| `_v95e1` | 104-277 | 1,033-6,044 | **9,333** | **0** |
| `_v94fb` | 118-466 | 1,646-7,859 | **9,264** | **0** |

**No TLE trips — but both heads peak within ~7% of the 10,000 µs limit, and
the E1/FT2 additions are NOT the driver** (maxima differ by 69 µs; medians
overlap). The lineage already runs hot at peak; whatever is expensive is in
the shared base, not the new planks.

Consequences: (1) CPU headroom for future planks is close to zero at peak —
price any new per-turn scan against this table, not against intuition;
(2) the in-bot `_cpu_exhausted()` guards are load-bearing ON THE PLATFORM
and inert locally (`get_cpu_time_elapsed()` is a stub under `fcode run`), so
a plank that relies on them is untested until a test match runs;
(3) every local leg run with `--tle 0` (all deterministic-paired work, by
design) is CPU-blind — run a test match before shipping any CPU-heavy change.

## Bot validation rejects `finally` blocks (builder, 2026-08-08)

`fcode run` refuses to load a bot containing a `finally:` block —
`ValueError: <bot>/main.py:NNNN: 'finally' blocks are not allowed`. Hit while
wrapping `run()` with a timing harness. `try/except` is fine. Any
instrumentation that needs guaranteed cleanup must be restructured (in our
case the wrapped body already swallows its own exceptions, so the timing
print could simply follow the call).

## Instrumented-arm extraction does not work on wild replays (research find, builder-placed 2026-08-08)

`scratchpad/fjord_disc/instr.py` recovers per-round `SLOT_UNDER` by parsing a
debug `print()` that exists **only in instrumented dev-arm builds**. Against
the live bot or any archived wild replay it yields nothing — silently, since
absent BotOutput text is indistinguishable from a quiet round. Any wild-latch
or store-state work must reconstruct trigger state from ENTITY POSITIONS
instead (the census agent did exactly this after catching it). General form of
the trap: an instrument that rides on our own debug output measures only the
builds we compiled it into.

## Field evidence about an UNSHIPPED head is structurally unobtainable (research argument, builder-verified against the CLI, 2026-08-08 s18)

Enumerate every instrument that can be pointed at a head we have not shipped:

| instrument | reaches a real third-party opponent? | why not |
|---|---|---|
| local self-play (`tools/arena.py`, `det.py`) | no | ours vs ours |
| `bots/opp_vNN` | no | real byte-exact code, but `fcode submission download` lists/downloads **our own team's** submissions only (CLI-verified) — every opp_vNN is a teammate lineage. No fidelity problem; a **relevance** problem: class-of-one |
| frozen probes | approximately, and unreliably | hand-extracted replicas; fidelity tested once and failed once (cad, 2026-08-08) — see probe-fleet-staleness |
| `fcode match test` | no | takes two **local** bot dirs by construction |
| unrated challenges | yes — but not for an unshipped head | runs our **ACTIVE** submission; no own-side selector exists (CLI-verified) |

**Therefore: reaching the real field requires activating the head first.** Field
evidence about an unshipped candidate is not expensive or blocked on probe
maintenance — it is impossible by construction on this platform.

**Consequence for the ship gate.** The gate as written (ship on a class-weighted
vs-field battery) cannot be satisfied by any sequence of actions. What we
actually do, and what the gate should say, is: gate on the best available
**proxy** evidence — self-legs for attribution, `opp_vNN` for a real-code sanity
check, probes for class diversity *with fidelity priced* — then **ship into a
measured window and let the ladder be the field instrument, with rollback as the
control.** That is what the swap rule formalises and what v79→v80 executed today.

This does not loosen tonight's hold on the E1 family; it renames its reason.
"No field-beating case" was true but unachievable pre-ship. The honest reason is
**the proxy evidence is not strong enough to justify spending a window** — at
parity against its own parent (e1-bundle-h2h), it plainly is not. Same decision,
reason that can actually be acted on next time.

**Carry to the retro** (Magnus): the gate currently asks for a measurement the
platform cannot provide before the fact, which will recur every cycle until the
wording changes.

## "0 flips" means NO OUTCOME EFFECT MEASURED — never "no effect" (measurement-stack finding #5, 2026-08-08 s18)

`tools/det.py` accounts GAME-LEVEL FLIPS. A change that alters economy without
changing who dies first scores **exactly zero**, by construction. Measured
instance: the hive_freeze ablation doubled delivered titanium (5,260 → 11,030)
and 5×'d standing buildings (28 → 155) across 6/6 paired seeds with **0 outcome
flips**. It surfaced only as a by-product of an unrelated decode.

That blindness is expensive because of what the long-game census then measured:
delivered titanium is the **sole** deciding metric in 219/219 full-length ladder
games — 26.2% of all games, and 36.7% under the v80 line. So the det instrument
was blind to the one metric that decides a quarter of our games and a rising
share of them.

**Fix shipped in `tools/det.py`**: every run now reports a paired
delivered-titanium delta (mean / median / games-moved) plus the top per-map
economy movers, computed over data `play()` already collected — a reporting
change, not a new measurement. Validated against the known hive case: it prints
`delivered-Ti delta (off minus on): mean +2885 median +5770 games moved 6/12`
on the same leg whose flip count is 0.

**Tape convention, standing:** a "0 flips / no effect" verdict must be written as
"no OUTCOME effect measured" and paired with its economy delta. Older rows
predating this change were written under the blind instrument — re-read them
accordingly rather than trusting their silence on economy.
