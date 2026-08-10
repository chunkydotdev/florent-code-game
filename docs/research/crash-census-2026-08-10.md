# Crash census: who loses units to uncaught exceptions — 2026-08-10

Tool: `tools/crash_census.py` (self-test + CLI + `--json`). Read its docstring
for the full method and the false-positive class — this doc is the run
record, not a restatement.

## Why text-matching doesn't work

Replays do not contain traceback text. Positive control checked (s26,
2026-08-10): zero occurrences of the sentinel string in the bytes of a
replay where `bots/_probe_crash` crashed 16 builder bots. The only usable
signal is structural — a unit vanishes (`removeEntity`) with no `updateHp`
event ever recorded against it.

## Self-test (both controls regenerated fresh, seed 4242, `maps/fjordgate.map26`)

| control | team A crash_candidates | team B crash_candidates |
| --- | --- | --- |
| positive: `bots/_probe_crash` vs `bots/_v127loki10` | 20 | 0 |
| negative: `bots/_v127loki10` vs itself | 0 | 0 |

(The pre-supplied `scratchpad/crash_pos.replay26` independently reads 16/0 —
different from the freshly-regenerated 20/0 because match simulation is not
bit-identical run-to-run even at a fixed seed; both runs satisfy the pass
condition A>0, B=0.) `tools/crash_census.py --selftest` reproduces this and
exits 1 if either side comes out wrong.

## The false-positive class (do not drop this when quoting the numbers below)

`crash_candidate` = a core/builder_bot/gunner/sentinel/launcher (the five
kinds that execute `run()`) vanishing with no `updateHp` event ever. The
replay format has no dedicated event for `self_destruct()`, `destroy()`, or
`resign()` — all three resolve to a bare `removeEntity`, identical on the
wire to a crash. So `crash_candidate` conflates:

1. a genuine uncaught-exception crash (what we're trying to count),
2. a builder bot's own `self_destruct()`,
3. a friendly builder's `destroy()` of an allied gunner/sentinel/launcher
   (turrets are buildings too — a deliberate teardown-and-rebuild of a cheap
   turret looks identical to that turret's own code crashing),
4. (core only) `resign()`.

Buildings-only kinds (harvester/conveyor/splitter/barrier) are excluded
entirely — they never run code, so a friendly `destroy()` is the only way
they vanish undamaged. Measured on a 40-file random sample: 34/84 (40%) of
all "vanished with no damage" removals were buildings-only, i.e. definitely
not crashes — excluding them is not a rounding error.

**The kind breakdown of the league-wide crash_candidate count skews heavily
toward gunner (58.6% of all crash_candidates, see below), the cheapest and
fastest-to-rebuild turret. That skew is consistent with either "gunners
crash more" or "gunners get torn down and rebuilt more" — this tool cannot
tell those apart, and the second is a plausible non-crash explanation for a
disproportionate share of the gunner number.**

## League-wide rate

Population: **10,199 of the 10,433 files currently in `replay_archive/`**
(the archive is live — a keeper process was adding files during this run;
10,199 is what existed at run start, not a deliberately reduced sample).
0 parse errors. 4,788,813 total rounds across those files.

| metric | value |
| --- | --- |
| files with ≥1 crash_candidate | 2,926 / 10,199 (28.7%) |
| crash_candidates, team A | 6,151 |
| crash_candidates, team B | 5,088 |
| crash_candidates, total | 11,239 |
| crash_candidates per 1,000 rounds | 2.35 |
| crash_candidates per file | 1.10 |
| damage_deaths, both teams (for scale) | 346,837 |
| friendly_removed (buildings, definitely not crashes) | 17,264 |

Kind breakdown of the 11,239 crash_candidates: gunner 6,582 (58.6%),
builder_bot 2,918 (26.0%), launcher 1,298 (11.5%), sentinel 441 (3.9%),
core 0. Zero core crash_candidates across the whole archive is itself
informative: every core removal in this archive had a damage event, i.e.
`core_destroyed` matches always show combat damage on the core, never a
bare unexplained vanish.

The team A vs team B split (6,151 vs 5,088, ~1.2x) should NOT be read as "team
A crashes more" — team A/B is an arbitrary per-replay seat, not a stable
identity across files. A 60-file spot-check showed the same split driven by
a handful of high-crash-count MATCHES (one single match contributed 33 of
246 crash_candidates in a 300-file sample) rather than an even spread, so
file-level A/B totals are not independent draws and the ratio moves with
which few matches land in a given sample.

## Is OUR team (OpenSverige) losing units to crashes?

Joined against `corpus/join.tsv` (file → our_team, reconciled against the
replay's own winner field per `tools/corpus/build_corpus.py` — 1.0 agreement
rate per `corpus/manifest.json`), covering **1,855 of our own ladder games**:

| | OUR team | opponents (same 1,855 games) |
| --- | --- | --- |
| crash_candidates | **0** | 2,451 |
| files with ≥1 crash_candidate | 0 / 1,855 | — |
| friendly_removed (buildings, destroy()) | 28 | 1,059 |
| damage_deaths (for scale) | 47,717 | 24,779 |

Zero is not a broken pipeline: the same per-team split correctly finds 28
`friendly_removed` events attributed to us in these games, so the team
attribution machinery is exercised and working — it just never once finds
an OUR-side unit-kind entity vanish undamaged. **Across all 1,855 archived
ladder games, we have never lost a unit to an uncaught exception (or, per
the false-positive class above, to a `self_destruct()`/`destroy()`/`resign()`
event that looks like one).** Opponents in those same games show 2,451
crash_candidates — real evidence some opponents' bots crash routinely
against us; we don't.

## Repro

```
.venv/bin/python tools/crash_census.py --selftest
.venv/bin/python tools/crash_census.py --json replay_archive/ > /tmp/full_census.json
```

git sha at run time: `1ff1acc`. Run timestamp: 2026-08-10T06:17–06:22 CEST
(`date` in-shell).
