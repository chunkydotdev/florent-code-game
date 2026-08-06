# Handover — 2026-08-08, after session 8 (stage 2 executed, ship candidate `_v63full`)

Start here, then [docs/game-model.md](docs/game-model.md) →
[docs/strategy-log.md](docs/strategy-log.md) → [docs/opponents.md](docs/opponents.md).

## Where the ladder stands

**Stage 1 shipped and is winning.** Magnus submitted the CPU-guard hotfix as platform
**v46 "v63guard-tle-armor"**; the real-hardware TLE check passed (5-0 vs starter on the five
heaviest maps) and it is the **active bot**: rating **1310 → ~1377** over the session, 10-0 in
its first ten. `bots/v63guard` is byte-identical to what is live.

**Naming, still:** platform v45 = x3r0's `florent-v63` = `bots/opp_v45`, the frozen primary
gate. Platform v46 = our v63guard. Our stage-2 artifacts are the `bots/_v63*` family. Never
call anything by a bare "v45"/"v46" without saying which namespace.

## SHIPPED: `bots/v5` is live as platform v47 "v63-mapfix-launcher"

**The decision below was taken and executed the same evening (2026-08-06 ~18:00 wall clock):**
Magnus submitted `bots/v5` (= `_v63full`); it went live as **platform v47** — **activation was
automatic on submit**, a platform behavior change worth knowing (v40/v46 needed explicit
`submission activate`). Real-hardware `match test` vs `opp_v45`: **4-1, no TLE deaths**.
Activation baseline for judging the 63.3% prediction: **rating 1383, rank #40 of 103, 132
matches played.** The next session's first job: compare the ladder record since this baseline
against the prediction, and log it in the strategy log. The section below is kept as the
decision record.

## The decision that was on the table: ship `bots/_v63full`

**`bots/_v63full` = v63guard + three separately-gated keeps, and it beats the active bot's
engine 63.3% [58.9%, 67.5%] over 480, 0 crashes.** Components, each gated alone vs pristine
`opp_v45` (tape rows for all of it):

| component | gate result | verdict |
| --- | --- | --- |
| crash armor (top-level try/except) | exactly 240-240, 16/32 on all 15 maps — inert-by-fingerprint | keep (insurance precedent) |
| Launcher wake-up (2 edits) | 53.3%; **eider 32/32**, dead even elsewhere; mechanism = defensive exile of their opening saboteur, not the insertion | keep |
| trail-linked facing port | **31.7% — refuted**, 0/32 on five maps; our overspend transplanted onto their lean economy | discard (`bots/_v63face` kept for reference) |
| **map-table refresh** (5 rotation maps) | **63.3%; drumlin/eider/heart/saga swept 32/32 both seats** | **keep — the headline** |
| integrated `_v63full` ship gate | 63.3%, identical to maps alone; launcher's eider win subsumed, armor inert | ship candidate |

Guards on `_v63full`: rush stress 80.0% vs `rush_probe_fast` (base 82.1%, same frozen build,
no regression); starter/opp_v39 no-collapse runs were in flight at handover — **check the last
rows of `results.tsv` before shipping; expect ~90% both, 0 crashes ours, else stop.**

```bash
# FIRST check whether this already happened: .venv/bin/fcode status
# (if the active bot is named v63-mapfix-launcher or similar, skip this block
#  and start on the queue below)
# Magnus only — bots/v* is write-protected for agents (classifier-enforced,
# verified this session):
cp -r bots/_v63full bots/v5            # v5 is still the next free LOCAL freeze slot
.venv/bin/fcode submit bots/v5 --name v63-mapfix-launcher
.venv/bin/fcode match test v5 opp_v45  # real-hardware sanity; rate-limited 5 per 10 min
.venv/bin/fcode submission list        # note assigned number
.venv/bin/fcode submission activate <version-number>
```

## The finding that explains three mysteries at once

**v63's hardcoded map tables (`CORE_PAIRS`/`MAP_CODES`/`EXTRA_MAP_CODES`) predate the current
weekly rotation.** eider, heart, meander, drumlin, saga have no entry → `known_map_for`
returns None → **`_plan_siege`, the line's primary attack, is silently disabled on 5 of the 15
pool maps.** Found by a delegated source audit, confirmed by measurement. It explains:

1. **The heart zero-harvester-as-B defect** — fixed at the root by the table refresh
   (1 building / 0 mined → 75 buildings / 2450 mined, same seed). It was never strategy.
2. **Why our Launcher wake-up swept eider** — the base cannot siege there, so games decay to
   economy tiebreaks, where the Launcher's defensive exile pays.
3. A chunk of the v63 line's per-map variance.

**Corollary now in [runbook.md](docs/runbook.md) step 7: embedded map tables must be
regenerated at every weekly pool cutover.** Encoder pattern: base-3 pack, 3 cells/char,
alphabet `A..Z0`, round-trip verify against the bot's own decoder (session scratchpad script;
rebuild it from the strategy-log description in ~30 lines).

## fjordgate, solved after two sessions of wrong theories

On the 10×10 (core anchors d²=32 — closest in the pool) v63's threat machinery misfires on
*ordinary opening spawns*: absolute radii (d²≤16 builder-near-core etc.) cover the opponent's
normal operating area, the melee-recall keeps the saboteur home, and **`_try_counterbattery` —
which unlike the siege path has NO economy gate and NO cap** — spends the opening bank on
fixed-facing Sentinels aimed at transient spawn tiles by round 6. Any home gun then drops the
ammo policy's `ti_floor` to 12 and every trickle of income converts to ammo forever: **seed 1
ends 255 rounds at 0 harvesters, 0 mined, exactly 12 Ti.** Both seeds reproduce. We win 26/32
because at that separation our defensive sentinel ring reaches their core footprint.

**The fix is one gate: mirror `_plan_siege`'s ECO_NEED gate onto `_try_counterbattery`
(`opp_v45:844-883`, cf. the gate at `opp_v45:671-674`).** In mirror gates both sides bankrupt
symmetrically (the eternal 16/32); fixing our side should convert the map. **Top of the next
queue.** Full mechanism with line numbers in [opponents.md](docs/opponents.md).

## The next queue, ranked

1. **Counterbattery ECO_NEED gate** (above). Cheap, diagnosed, mechanism-confirmed twice over.
2. **Launcher warts, both measured and deliberately left out of the gated artifact:**
   the launchwait/saboteur role flip-flop every round r180-199 (the `rnd>=180` give-up and the
   `rnd<200` recruit gate fight each other — align them), and the claimed waiter circling the
   Launcher all game when the insertion path never opens (opportunity cost, empirically nil in
   mirror gates, but real vs third parties).
3. **Meander:** its table entry does no harm but siege does not convert it (16/32 while the
   other four refreshed maps swept). One diagnostic replay would say why.
4. **Mirror seat table on the new base** — still never run. The equivariance audit (summary in
   opponents.md) predicts nordkap and moonrise as the seat-gap maps; the audit's ranked list is
   the test plan.
5. **Re-tune constants on the integrated base, last** — same reasoning as ever (a full CEM
   sweep on our old line was worth exactly nothing).
6. **SPRT / early-stopping gate wrapper** (Magnus asked; assessment on the record): fixed-480
   gates waste ~2/3 of their matches on clear results — today's refutation was settled by match
   ~150. A sequential wrapper (new tool alongside protected `tools/arena.py`) is the biggest
   available workflow speedup; adopting it changes the accept criterion, so give it its own
   tape note when it lands.

## Team etiquette — Magnus, two messages to x3r0

1. **The stale map tables are their bug too, live right now in v46's engine on 5 maps.** The
   full fix is `bots/_v63maps`'s table block, ~40 lines, drop-in. Credit their disambiguation
   design — `EXTRA_MAP_CODES` handled the eider/heart dims-and-anchors collision unchanged.
2. **The fjordgate counterbattery bankruptcy** (one-gate fix, above). Both are their design
   with their bug; everything we shipped on their base is credited to their engine.

## Operating notes

- **The submission-watcher monitor died with this session — re-arm it** (five-minute poll of
  `fcode status`; it caught every rating tick this session).
- **Orchestration norm (Magnus, this session): two-tier, not three-tier.** Fable inline on
  design/edits/verdicts; delegated read-only diagnostics as single subagents WITH explicit
  model tier; three-tier reserved for wide fan-outs (tournament-week recalibration). Both of
  this session's decisive finds came from delegated audits — the pattern works.
- **Gates stay serialized** — arena.py already saturates the cores; concurrent gates buy
  nothing and risk TLE distortion. Real speedups: the SPRT wrapper (queue 6) or a second
  machine (engine is a pip wheel + maps/; linear scaling).
- Date labels still run one day ahead of wall clock (all commits authored Aug 6). Sessions
  5-8 are logged as 08-07/08-08. Left deliberately.
- Protected paths and Magnus-only platform writes: unchanged from session 7 (see git history
  of this file if needed; the `.claude/settings.json` `bots/v*` glob observation stands).
- `results.tsv` is the append-only tape, untracked; every number above is a row in it. Still
  no `git remote`.

## Where things live

| path | what it is |
| --- | --- |
| **`bots/_v63full`** | **the ship candidate: v63guard + armor + Launcher + map tables** |
| `bots/v63guard` | live submission v46, byte-identical; base of everything |
| `bots/_v63armor` / `_v63launch` / `_v63maps` | the three keeps, individually gated artifacts |
| `bots/_v63int` | armor+launcher intermediate (superseded by `_v63full`) |
| `bots/_v63face` | the refuted facing port, kept for reference |
| `bots/opp_v45` | x3r0's florent-v63 (platform v45) — the frozen primary gate |
| `bots/_pkg45` / `bots/ladder1` | our old lineage's challenger, component donor, measuring rig |
| `bots/aug7`, `bots/_incumbent` | pinned incumbents of the old line |
| `bots/opp_v44`, `bots/opp_v39`, `bots/starter` | reference opponents / no-collapse guards |
| `bots/rush_probe_fast` | the rush instrument, frozen, md5 `f50ec997dd24b7721ef64f46a1a3c0b4` |
| safe to delete | `bots/_diag_launch`, `bots/_tune_*`, `bots/_diag_*`, `bots/_probe_*`, `bots/aug7_h1..h4` |

## Traps

All of session 7's still apply (`.venv/bin/` not python3; `--tle 10` always; stderr not
print; `random` unseeded by `--seed`; both-seats-both-orderings always; `get_cpu_time_elapsed`
inert under `fcode run`; validator rejects `try`/`finally`; vision-raise on tile queries; the
store cannot hold zero; pooled rates hide single-map defects; name both sides of every
percentage; pin opponents by hash; a flat-uniform screen failure is a mechanism defect, per-map
clustered failure is real harm). New this session:

- **A dict cannot hold two maps with the same key.** eider and heart share dims AND Core
  anchors; their codes must go in `EXTRA_MAP_CODES` (list, runtime terrain disambiguation),
  not `MAP_CODES`. The bot's own comment warned about exactly this; read it before adding maps.
- **`known_map_for(...) is None` is silent.** No crash, no log — the bot just plays without
  siege. After any pool change, positively verify every rotation map resolves (5-line check,
  see strategy-log session 8).
- **An "inert" gate result has a fingerprint:** exactly 240-240 pooled AND 16/32 on every map
  separately. Pooled-even with per-map spread is a different animal — read the table, always.
- **Two changes can validly gate keep and still not stack** (launcher + maps both converted
  eider). Attribute sweeps to components before predicting the integrated number.
