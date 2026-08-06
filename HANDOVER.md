# Handover — 2026-08-09, after session 9 (queue item 1 done, ship candidate `_v64cbA`)

Start here, then [docs/game-model.md](docs/game-model.md) →
[docs/strategy-log.md](docs/strategy-log.md) → [docs/opponents.md](docs/opponents.md).

## Where the ladder stands

**Platform v47 "v63-mapfix-launcher" (= `bots/v5` = `_v63full`) is live and barely tested.**
It activated at rating 1383 / rank #40 / **132 matches**. During session 9 it played exactly
**one** match: a win, **1397 / #39 / 133**. The 63.3% prediction from session 8 is still
effectively unmeasured — one match is not a sample. The ladder is scheduling us slowly; treat
"compare the record against the prediction" as a standing job needing ~30+ matches before it
means anything, not a task to force.

**Naming, still:** platform v45 = x3r0's `florent-v63` = `bots/opp_v45`, the frozen primary
gate. Platform v46 = our `v63guard`. Platform v47 = our `bots/v5`. Session 9's artifacts are
the `bots/_v64*` family. Never say a bare "v45"/"v46"/"v47" without saying which namespace.

## READY TO SHIP: `bots/_v64cbA` — 70.0% vs the live bot's own engine

**One gate, six added lines over `bots/v5`, fully validated.** This is queue item 1 from last
session, executed exactly as diagnosed. In `_try_counterbattery`, mirroring `_plan_siege`:

```python
if ct.read_store(SLOT_HOME_GUN) >= 1 and ct.read_store(SLOT_HARVESTERS) < ECO_NEED:
    return False
```

Both call sites (`_home_defend`, `_defend`) route through that one function, so one gate does it.

| run | result |
| --- | --- |
| **ship gate vs `opp_v45`, 480** | **70.0% [65.8%, 73.9%]**, 0 crashes both sides (live v47's own engine scores 63.3%) |
| per-map | **fjordgate 16/32 → 32/32**, **meander 16/32 → 32/32**; drumlin/eider/heart/saga held 32/32; other nine unmoved |
| no-collapse vs `starter`, 240 | 97.9% (base 98.3% — flat) |
| no-collapse vs `opp_v39`, 240 | 99.2% (base 98.3%) |
| rush stress vs `rush_probe_fast`, 240 | **95.4% [92.0%, 97.4%]** vs base 86.7% [81.8%, 90.4%] — **non-overlapping** |

```bash
# Magnus only — bots/v* is write-protected for agents (classifier-enforced):
cp -r bots/_v64cbA bots/v6            # v6 is the next free LOCAL freeze slot
.venv/bin/fcode submit bots/v6 --name v64-counterbattery-gate
.venv/bin/fcode match test v6 opp_v45  # real-hardware sanity; rate-limited 5 per 10 min
.venv/bin/fcode status                 # confirm active — v47 activated AUTOMATICALLY on submit
```

Platform behavior learned last session: **submission activated automatically**, no explicit
`submission activate` needed. Verify with `status` rather than assuming either way.

## The two things session 9 actually learned

**1. Gating home defense is what beats rushes.** The rush guard moved 86.7% → 95.4% with
non-overlapping intervals, and we were not aiming at it. Same mechanism from the other side:
a bot that has spent its opening bank on three fixed-facing Sentinels aimed at *transient
spawn tiles* has nothing left when a real attack lands. The frozen-instrument lineage now
reads aug7 60.4% → `_pkg45` 64.2% → `v63guard` 82.1% → `_v63full` 86.7% → `_v64cbA` 95.4%.

**2. Meander converted, and the honest claim is narrower than the headline.** Meander was
queue item 3 — it had its map-table entry and still sat at 16/32. The counterbattery gate
converts it **on top of** the tables (table = *can it plan a siege*, gate = *can it still
afford one*). We never measured the gate **without** the tables on meander, so "these two only
pay together" is a hypothesis, not a result. Mirror image of session 8's trap: two changes
that each gate keep and fail to stack, versus two that individually leave a map dead and
jointly convert it. Both say the same thing — **attribute per map, never from the pooled number.**

**Refuted and kept for reference:** `bots/_v64cbB`, the strict gate with no free first battery
(theory: one gun alone pins `ti_floor` at 12 forever, which is true). Fjordgate screen: pooled
16/32 but **seat A 32/32** — it converts the map into a first-mover coinflip instead of curing
the collapse. The first battery is load-bearing; the second onward is the bankruptcy. That
6-second one-map screen before a 480-match gate is the cheap move worth repeating.

## The next queue, ranked

1. **Ship `_v64cbA` as v6 — but this now collides with the Elo regression rule, and Magnus
   should make the call.** The rule (operating notes below) wants ~20 ladder matches under
   v47 before a verdict; v47 has played **one** in twelve hours. Shipping v6 now permanently
   confounds the question "was v47 better than v46?". The two readings:
   - **Ship now.** The local evidence is strong and independent of the ladder: 70.0% vs v47's
     own engine over 480, two maps converted, rush guard up 8.7 points, all guards green. At
     ~1 ladder match per session, waiting for n=20 could cost weeks of ladder time, and the
     rule exists to catch *regressions* — this is the opposite of a suspected regression.
   - **Wait.** The directive is explicit and new, and v47 is the first bot it applies to;
     spending its first application on an exception sets the precedent that it yields to any
     confident local number. Local gate strength is exactly what the rule distrusts.
   - **The compromise, if wanted:** ship v6 and accept that v46→v47 stays unattributed, but
     record v6's baseline row properly so the rule gets a clean first real application on
     v47→v6. Either way, **do not stack a third submission before v6 has a record.**
2. **Launcher warts — `bots/_v64lw` is already built and unmeasured.** The r180–199 flip-flop
   is worse than churn: `rnd >= 180` sets `saboteur`, the `rnd < 200` recruit gate sets it
   straight back to `launchwait` in the same call, every round — **the give-up at 180 is dead
   code** for any `role_n>=3` waiter while a Launcher lives. `_v64lw` gives both bounds one
   name, `LAUNCH_GIVEUP_RND = 180`. **Sequencing note that matters: this wart is invisible to
   a mirror gate by construction** (both sides carry it). Measure it on `starter` / `opp_v39` /
   `rush_probe_fast`, not with another 480 vs `opp_v45`. Second wart still unaddressed: the
   claimed waiter circling the Launcher all game when the insertion path never opens.
3. **The rest of the fjordgate fix target, still open and still live in x3r0's engine:**
   SLOT_THREAT takes *builder positions* for fixed-facing turret aiming (`opp_v45:254,257`),
   and the absolute threat radii (d²≤16 etc.) do not scale with map size — on a 10×10 they
   cover the opponent's normal operating area. The gate cured the symptom; these are the cause.
4. **Mirror seat table on the new base** — still never run, still queued since session 7. The
   equivariance audit (summary in opponents.md) predicts nordkap and moonrise as the seat-gap
   maps; its ranked list is the test plan. Note the session-9 gate already shows nine maps that
   are *fully* seat-decided (antler, atoll, hive, jackpot, lighthouse at seatA 0/32;
   archipelago, moonrise, nordkap, snowflake at 32/32) — free evidence sitting in that run.
5. **Re-tune constants on the integrated base, last** — same reasoning as ever.
6. **SPRT / early-stopping gate wrapper.** Still the biggest available workflow speedup, and
   session 9 is fresh evidence for it: the `_v64cbB` refutation cost 6 seconds as a one-map
   screen, while the fixed-480 gates each spent most of their matches confirming a settled
   result. Adopting it changes the accept criterion — give it its own tape note when it lands.

## Team etiquette — Magnus, now three messages to x3r0

1. **Stale map tables**, live in their engine on 5 maps (`bots/_v63maps`'s table block, ~40
   lines, drop-in). Credit their `EXTRA_MAP_CODES` disambiguation design — it handled the
   eider/heart dims-and-anchors collision unchanged.
2. **The fjordgate counterbattery bankruptcy — now fixed and measured, not just diagnosed.**
   Six lines, +6.7 points pooled, two maps converted, and worth +8.7 points against a rush.
   This is the highest-value single thing we can hand them.
3. **The two remaining causes** behind it (item 3 above): builder positions written into
   SLOT_THREAT for fixed-facing aiming, and unscaled absolute radii on small maps.

Everything we shipped on their base stays credited to their engine.

## Operating notes

- **Standing directive (Magnus, 2026-08-06): measure Elo over time so we never ship a worse
  bot and fail to notice.** `elo_history.tsv` (repo root, **tracked**, unlike `results.tsv`) is
  the append-only ladder tape: `timestamp, rating, matches, active_bot, note`. It is fed by the
  session monitor; **re-arm the logging variant at every session start** — it appends each
  rating change to the file as well as notifying. **Regression rule:** every activation gets a
  baseline row (rating, match count); after **~20 ladder matches** under a new bot, compare its
  rating delta against the previous bot's trajectory over its final 20. Clearly negative with
  no confound (opponent-pool shift, teammate activations) → **roll back**
  (`.venv/bin/fcode submission activate <previous>`, Magnus runs it) and log the reversal on
  both tapes. v47's baseline: **1383 @ 132 matches**.
- **The Elo logger monitor dies with its session — re-arm it** (5-min poll of `fcode status`).
  Session-9 note on a hazard this created: a **concurrent session** (the one that introduced
  `elo_history.tsv`, commit `bc583e0`) had its logging monitor live at the same time as this
  session's notify-only watcher. Both saw the 1383 → 1397 tick; only one wrote it, which is the
  correct outcome. **Run exactly one *appending* monitor at a time** — two would duplicate rows
  on a tape whose whole purpose is trend detection. If you find rows you did not write, another
  session owns the logger; keep yours notify-only.
- **Orchestration norm (Magnus, session 8): two-tier, not three-tier.** Fable inline on
  design/edits/verdicts; delegated read-only diagnostics as single subagents WITH explicit
  model tier; three-tier reserved for wide fan-outs. Session 9 needed no delegation at all —
  the diagnosis was already on paper from session 8, which is the pattern working as intended.
- **Gates stay serialized** — arena.py saturates the cores. Real speedups: the SPRT wrapper
  (queue 6) or a second machine.
- Date labels still run one day ahead of wall clock (all commits authored Aug 6). Sessions
  5–9 are logged as 08-07/08-09. Left deliberately.
- Protected paths and Magnus-only platform writes: unchanged (the `.claude/settings.json`
  `bots/v*` glob observation stands).
- `results.tsv` is the append-only tape, untracked; every number above is a row in it. Still
  no `git remote`.

## Where things live

| path | what it is |
| --- | --- |
| **`bots/_v64cbA`** | **the ship candidate: v5 + the counterbattery ECO_NEED gate, validated** |
| `bots/_v64lw` | launcher give-up/recruit bound alignment — built, **unmeasured** |
| `bots/_v64cbB` | the refuted strict gate, kept for reference |
| `bots/v5` | live submission v47 (= `_v63full`), base of everything in session 9 |
| `bots/v63guard` | live submission v46, base of the `_v63*` family |
| `bots/_v63armor` / `_v63launch` / `_v63maps` | the three session-8 keeps, individually gated |
| `bots/_v63int` / `_v63full` | intermediates (`_v63full` = `v5`) |
| `bots/_v63face` | the refuted facing port, kept for reference |
| `bots/opp_v45` | x3r0's florent-v63 (platform v45) — the frozen primary gate |
| `bots/_pkg45` / `bots/ladder1` | our old lineage's challenger, component donor, measuring rig |
| `bots/aug7`, `bots/_incumbent` | pinned incumbents of the old line |
| `bots/opp_v44`, `bots/opp_v39`, `bots/starter` | reference opponents / no-collapse guards |
| `bots/rush_probe_fast` | the rush instrument, frozen, md5 `f50ec997dd24b7721ef64f46a1a3c0b4` |
| safe to delete | `bots/_diag_launch`, `bots/_tune_*`, `bots/_diag_*`, `bots/_probe_*`, `bots/aug7_h1..h4` |

## Traps

All of sessions 7–8's still apply (`.venv/bin/` not python3; `--tle 10` always; stderr not
print; `random` unseeded by `--seed`; both-seats-both-orderings always; `get_cpu_time_elapsed`
inert under `fcode run`; validator rejects `try`/`finally`; vision-raise on tile queries; the
store cannot hold zero; pooled rates hide single-map defects; name both sides of every
percentage; pin opponents by hash; flat-uniform screen failure = mechanism defect, per-map
clustered failure = real harm; a dict cannot hold two maps with the same key; `known_map_for(…)
is None` is silent; an inert gate has a fingerprint — exactly 240-240 AND 16/32 on every map;
two changes can validly gate keep and still not stack). New this session:

- **The converse of that last one also happens.** Two changes can each leave a map at 16/32
  and jointly convert it (map tables + counterbattery gate on meander). Never infer a
  component's per-map effect from a run that contains another component.
- **Screen one diagnostic map before spending a 480-match gate.** Both session-9 variants were
  separated in 6 seconds on fjordgate alone; the strict one would otherwise have burned a full
  gate to learn it was a seat coinflip.
- **A pooled 16/32 and a one-seat 32/32 are completely different animals.** The refuted
  variant's pooled number was identical to "unmoved" — only the seat column showed it had
  changed the map's character entirely. Read the seat column on every per-map row.
