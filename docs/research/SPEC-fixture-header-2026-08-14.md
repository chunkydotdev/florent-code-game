# SPEC — MAKE A SHARD DECLARE ITS OWN FIXTURE

**2026-08-14T19:59:23Z (`date -u`), research arm (s42).** Written at the builder's request
("YES — write the FIXTURE HEADER spec … it joins the wiring bundle"). Third of three specs
that are **the same shape: make the fixture declare itself** — alongside
`SPEC-pool-era-token-2026-08-14.md` and `#65`'s record-both-arms'-versions half.

**Scope: the local/remote shard runner's row writer, and any reader that consumes those
rows.** No bot changes, no platform changes.

---

## 1. THE DEFECT, MEASURED TODAY

Current row schema, verbatim from `scratchpad/overnight-remote/worker@work-server-1/SALTREF.tsv`:

```
ts	shard	game	map	seed	seat	winner	cond	turns
```

**No host. No WORKERS. No ncpu. No load ceiling. No engine version. No per-game wall
duration** (`ts` is completion time only, so latency is unrecoverable by subtraction across
concurrent shards).

**CONSEQUENCE, and it is not hypothetical:** on 2026-08-14 the remote box turned out to be
**ncpu=16, not the recorded 48**, and every shard after a **13:47:33Z `WORKERS=40` bump**
ran ~2.5× oversubscribed under a **wall-clock** `--tle 10`. **Two shards changed fixture
MID-FLIGHT and neither file shows it.** `SEALREPAIRR` straddles the bump at row ~509 and
reads **+4.13pp pre→post (p=0.067)** with three controls at ≈0.

⛔ **The audit that established all of this existed only because a human happened to
mention the core count.** Nothing in our own record could have raised it.

⛔ **AND THE TELEMETRY WE ASSUMED WE HAD DOES NOT EXIST: engine 2.3.6 local replays carry
NO `execTimeUs` and NO timed-out flag** (12 games decoded, 0 records). **TLE incidence is
currently unobservable on our own fixture.** *(Same class as the s28 finding that
platform-downloaded replays strip `stdout`: an instrument planned on telemetry that is not
there. Check the telemetry exists before designing around it.)*

---

## 2. THE HEADER — WHAT THE FILE MUST SAY ABOUT ITSELF

Comment-prefixed lines above the column header, so existing readers skip them:

```
# FIXTURE host=work-server-1 ncpu=16 workers=10 load_ceiling=20 engine=2.3.6 tle_ms=10
# ARMS a=_v223sealrepair@v140 b=_v232collarmedic@vNONE  git=537b641
# START 2026-08-14T19:59:23Z  planned_games=1000  seeds=32269000..32270000
ts	shard	game	map	seed	seat	winner	cond	turns	wall_ms	load1
```

**`ncpu` is READ FROM THE MACHINE, never from a note.** The 48 that was wrong all day lived
in a human record. ⚠ **The whole spec fails if this field is transcribed rather than
probed** — the defect being fixed is *a recorded fixture that did not match the real one*.

**`ARMS` carries each arm's PLATFORM version, not only its tree name.** This is `#65`'s
cheap half and it lands here: `results.tsv` keys screens by local tree name only, and
`corpus/version_trees.tsv` has **no entry for any of x3r0's v134/v141/v142/v143/v145** —
which is why the screen-validity join had to be rebuilt by grepping `coordination.md`.
**`@vNONE` is a legal and required value** for an unshipped tree; a blank is not.

---

## 3. ⭐ THE HEADER IS NOT ENOUGH — A HEADER DESCRIBES THE FIXTURE AT **START**

**This is the part that would actually have caught today, and a header-only spec would
not have.** Both degraded shards had a correct fixture when they began. **The fixture
changed underneath them.**

⇒ **the runner re-probes its fixture every N games (suggest N=50) and, on ANY change,
writes a marker row into the same file:**

```
# FIXTURE-CHANGE at game=509  workers=10->40  load1=6.2->31.8  ncpu=16 (unchanged)
```

**Two properties this must have:**
1. **The marker lives in the DATA FILE, not a log.** A sidecar drifts, is rotated, or is
   not copied when the file is pulled from a remote box. **The row file is the artefact
   that survives to analysis time; the fixture fact has to travel inside it.**
2. **Any reader that computes a bar over rows spanning a `FIXTURE-CHANGE` marker must say
   so.** ⚠ **The reader half is not optional — a marker nobody consumes is the
   alarm-that-cannot-fire trap.** Minimum: the read prints
   `SPANS FIXTURE-CHANGE at game=509 — split or justify`, and does not silently pool.

---

## 4. THE TWO NEW COLUMNS, AND WHY THESE TWO

| column | why |
|---|---|
| `wall_ms` | per-game wall duration. **The only observable proxy for TLE pressure we have**, since `execTimeUs` does not exist in local replays. A contention episode shows as a distribution shift, and it is unrecoverable after the fact from completion timestamps alone under concurrency. |
| `load1` | 1-minute load average at game start. **The DIRECT contention measure** — it is what oversubscription actually does, it costs one file read, and it is the field that would have made today's audit a `grep`. |

**Deliberately NOT added:** a per-game CPU measurement (we cannot get it from the engine),
and a timed-out flag (**it does not exist in 2.3.6 — do not add a column the engine cannot
populate, or it becomes a constant column, and a constant column validates anything**).

---

## 5. BOTH-VERDICTS CELLS

| cell | drive | must |
|---|---|---|
| H1 | run a shard normally | header present, `ncpu` matches an independent probe of the box |
| H2 | **falsify `ncpu` in the config** | header still shows the **PROBED** value — proves it is read, not transcribed |
| H3 | change `WORKERS` mid-run | **`FIXTURE-CHANGE` row appears** at the right game index |
| H4 | run with no change | **no `FIXTURE-CHANGE` row** — the marker is not always-on |
| H5 | reader over rows spanning a marker | **announces the span**, refuses to pool silently |
| H6 | reader over clean rows | **silent** — proves H5 discriminates |
| H7 | arm with no platform version | header reads `@vNONE`, **not blank** |
| H8 | header unreadable / absent (legacy file) | reader **announces the file predates the header**, never assumes a fixture |

**H2 and H8 are the cells that will be skipped and must not be.** **H2 is the entire point
of the spec** — a transcribed `ncpu` reproduces today's defect exactly. **H8 is the
alarm-that-cannot-tell-it-is-blind trap**: every existing shard file lacks the header, and
a reader that treats "no header" as "fixture fine" is worse than one that has no opinion.

---

## 6. MIGRATION — AND THE HONEST LIMIT

**Existing row files cannot be retrofitted.** `wall_ms` and `load1` were never recorded and
are not derivable. ⇒ **every banked local screen predating this spec is permanently
un-auditable on fixture**, and the TLE retro's exposure table
(`TLE-FIXTURE-EXPOSURE-2026-08-14.md`) had to reconstruct fixtures from row *timing
patterns* rather than read them.

⚠ **That is the cost being paid once. It is the argument for shipping the cheap version
now rather than the complete version later** — the next audit's evidence is being decided
by what the runner writes this week.

---

## 7. WHAT THIS DOES NOT DO

* **It does not prevent a degraded fixture.** It makes one **visible and attributable**.
  The WORKERS=10 rule is the prevention; this is the detection.
* **It does not make TLE incidence observable.** Only a change in the engine's own
  telemetry could, and 2.3.6 does not emit it. `wall_ms`/`load1` are proxies and must be
  described as proxies.
* **It does not apply to platform (rated/unrated) games**, whose fixture is the
  organisers'. ✅ *(Related and already answered: the local screen fixture's MAP POOL does
  track the ladder's — 66.4–66.7% new-pool against the ladder's 66.0%. Measured, clean
  negative, `SPEC-pool-era-token-2026-08-14.md` §6.)*

---

## 8. PROVENANCE

Numbers from `docs/research/TLE-FIXTURE-EXPOSURE-2026-08-14.md` (opus subagent, s42) and
from the row schema of `scratchpad/overnight-remote/worker@work-server-1/SALTREF.tsv` read
directly at 2026-08-14T19:59:23Z. **The prediction that motivated that retro — that the
bias would run against the treatment arm — WAS REFUTED by it** (the sign keys to compute
weight; x3r0's routers are 9,215 lines against our 4,757, so the heavy arm was the
control). **This spec is written by the lane whose prediction failed, which is the reason
it keys everything to a PROBE rather than to a label.**
