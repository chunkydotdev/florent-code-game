# Handover — 2026-08-08, after session 7 (candidate endgame, tag `ladder1`)

Start here, then [docs/game-model.md](docs/game-model.md) →
[docs/strategy-log.md](docs/strategy-log.md) → [docs/opponents.md](docs/opponents.md).

## Naming, because the platform has overtaken us

**The platform's submission `v45` is x3r0's `florent-v63`, not ours** — vendored locally as
`bots/opp_v45`. Our own artifact directories (`bots/_pkg45`, `bots/_pkg45b`) were named before
that landed and are kept only because every row in `results.tsv` references those names. **Do not
call our challenger "v45" anywhere durable.** It is *the `ladder1` candidate*; the platform
assigns its number at upload.

## The decision on the table: two deliverables, both human-activated

**The bar is frozen.** x3r0 is out of tokens, so `bots/opp_v45` ("florent-v63") is the last
teammate upload and the fixed gate for everything below. It is the **active ladder submission**,
the team is at **~1310 and climbing**, and it beats our own fully-gated challenger **78/22**.

**Our line is not going to catch it, and that stopped being the question.** The deliverable is
the team's strongest bot, so the work splits in two:

### Stage 1 — the hotfix, ready to ship first

**`bots/v63guard` = `florent-v63` + our phase-boundary CPU-budget guard, and nothing else.**
The port is a verified single-mechanism delta (constant, `_cpu_exhausted()` helper, early
returns at phase boundaries, and a check every 64 iterations inside each BFS loop), and it is
**gated and clean**:

| stage-1 gate | result |
| --- | --- |
| **no-regression vs `opp_v45`, 480 matches** | **exactly 240-240 — 50.0% [45.5%, 54.5%], 0 crashes both sides** |
| forced-trip build (threshold 0, every guard fires), 120 matches | **0 crashes** — bail-outs leave no half-updated state |
| no-collapse vs `starter` / `opp_v39` | see the `v63guard` rows in `results.tsv` |

**A dead-even 240-240 is the ideal outcome here, not a disappointing one.** The guard is a no-op
locally by construction, so the gate can only demonstrate *no harm* — which it does, precisely.
The forced-trip build is the only local way to execute the new code paths at all, and it comes
back crash-free.

The active bot is losing real ladder games to a fixable timeout: a decoded replay shows
**272 CPU-truncated rounds out of 310, losing by `core_destroyed` while paralysed**. A full
source audit of their line found **no `get_cpu_time_elapsed()` call anywhere — no CPU guard at
all**, in either v58 or v63. Ours has carried one since v2. Their author cannot ship a fix.

**The validation caveat that must travel with this package: `ct.get_cpu_time_elapsed()` is inert
under `fcode run`** — it reads 0 however much CPU is burned. So the guard is a **no-op locally**,
local gates can only prove *no harm*, and its new code paths are exercised locally only by a
forced-trip build (threshold 0). **The real check is `fcode match test` on Graviton3, and that is
a human step.** Treat the local gates as an insurance-change accept, the same precedent as v2's
own CPU guard, which was kept on a no-verdict.

### Stage 2 — the integration, on their base not ours

Port our measured components onto `florent-v63`, each gated separately against pristine
`opp_v45`. What the v58→v63 source catalogue (now in [opponents.md](docs/opponents.md)) says is
actually worth porting:

| our component | status on their base |
| --- | --- |
| **CPU-budget guard** | **absent — this is stage 1** |
| top-level `try`/`except` in `run()` | **absent.** Their `run()` dispatches unwrapped; an escaping exception permanently deletes the unit. They measured 0 crashes in 480 matches, so it is latent, not active |
| trail-linked conveyor facing | their **primary** chain is a pre-planned BFS tree — bend- and cycle-safe by construction, no defect to fix. Their **secondary opportunistic-pave** path still uses the naive dominant-axis rule, and ladder replays show partial defects (`chain_dir` 4/7 and 2/3). **That path is the port target** |
| (0,0)-Core store fix | already present, identical `+1` scheme, since their v39 |
| Sentinel-first / reactive vision-triggered defense | already present and more developed than ours |

**Our own challenger's remaining value is as a component donor and as a measuring rig**, not as a
submission. It is preserved, gated and documented below.

**Team etiquette, and it matters: Magnus should tell x3r0 we are building on their engine with
their bug fixed.** Their blessing keeps this collaboration healthy, and every stage-2 component
above is credited to their design except the two they are missing.

```bash
# Magnus only — bots/v* is write-protected for agents:
cp -r bots/v63guard bots/v5        # v5 is the next free LOCAL freeze slot (v1..v4 exist)
.venv/bin/fcode submit bots/v5 --name v63-cpuguard
.venv/bin/fcode match test v5 opp_v45     # REAL-HARDWARE TLE CHECK -- do this before activating
.venv/bin/fcode submission list           # note the assigned version number
.venv/bin/fcode submission activate <version-number>
```

## What is in our own challenger (`bots/_pkg45` = `bots/ladder1`)

Two changes over `bots/aug7` (`3cfa588`), each measured separately. It is fully gated and
crash-free — these numbers are what make it a credible component donor even though it is not
going to be submitted.

| gate (480 matches: 15 maps × 16 seeds × both orderings; rush runs 240) | result |
| --- | --- |
| **vs `opp_v45` (frozen primary gate)** | **22.1% [18.6%, 26.0%]** |
| vs `opp_v44` (previous teammate bot) | 44.8% [40.4%, 49.3%] |
| vs `aug7` (`3cfa588`) — the facing change alone | **58.5% [54.1%, 62.9%] — accept** |
| **vs `_incumbent` = submission `v40`, what our line last ran** | **67.1% [62.8%, 71.1%]** |
| no-collapse vs `starter` / `opp_v39` | 83.5% [80.0%, 86.6%] / 73.1% [69.0%, 76.9%] |
| rush vs `rush_probe_fast` (frozen build) | 64.2% [57.9%, 70.0%] — `aug7` 60.4%, level |
| `jackpot` mirror probe, seat A | **0/32 → 15/32 = 46.9% [31%, 64%]** |
| **crashes, our side, every run** | **0** |

**1. Trail-linked conveyor facing** (`_try_move`, `NEAR_CORE_FACING_DIST_SQ = 18`). A builder
walking *outward* faces each new trail conveyor **back at the tile it came from** — an exact
link that survives bends, staircases and detours — but only beyond dist² 18 from the Core.
Inside that radius `aug7`'s "dominant axis toward the Core" rule is kept byte-for-byte.
**58.5% [54.1%, 62.9%] over 480 vs `aug7`**, above half on 12 of 15 maps, largest margin
`heart` 26/32 — the map where zero-delivery was first observed.

**2. The (0,0)-Core store fix** (the five-liner that has been waiting on a decision since
session 6). It ships on a **correctness** argument, not a pooled win rate: those two slots have
**exactly one writer and one reader**, so the patch is **provably inert on every map whose Core
is not at (0, 0)** — `jackpot` alone in this rotation — where it takes seat A from 0/32 to
15/32 and from "exactly zero titanium, every game" to a normal economy.

## The finding that matters more than the win rate: facing is a *global* problem

**The first implementation of change 1 was refuted at the screen — 11.1% [6.1%, 19.3%], losing
on all 15 maps** — and diagnosing it produced the session's real result. It faced every outward
conveyor back down its own trail, everywhere. A 30-replay census
(`tools/replay_census.py`, plus a purpose-built cycle-detecting graph walk):

- **931 of its 2,133 non-delivering conveyors (43.6%) sat in closed cycles. `aug7` had zero.**
  Two builders crossing the same corridor in opposite directions point at each other, and
  **84% of those cycles were within Chebyshev distance 5 of the Core**, where trails converge.
- `aug7`'s rule cannot produce a cycle *by construction*: "point at the Core" is a global
  potential field and every arrow descends it. A per-builder local rule has no such guarantee.
- Secondary and as predicted: dangling heads landed on a builder's own **spawn tile 23.6%** of
  the time (`aug7`: 4.8%) — the first trail tile points back at a tile that never gets a conveyor.

**The transferable rule: a local facing rule is only safe when anchored to a global one.** That
is exactly what the near-Core zone does in the shipped version, and the census confirms it —
**0 cycles in 1,891 non-delivering conveyors.**

## Three corrections to things we believed yesterday

1. **The rush probe is weak, and one number was relayed inverted.** `aug7` beats `rush_probe`
   **96.2% [93.0%, 98.0%]**; the defense-carrying `ladder1` scored **94.2% [90.4%, 96.5%]** —
   overlapping, if anything *worse*. The belief that reactive defense had "inverted a 95/5 rush
   matchup" came from reading the defender's win rate as the rusher's. **Standing rule now:
   every metric report names both sides — "X beats Y at N%", never "the baseline is N%".**
   `arena.py` reports the **first-named** bot's rate.
2. **The reactive-defense port's "violently bimodal per map" split was never its own.** The
   candidate carries no defense change and collapses on the *same* maps against v44 (`atoll`
   1/32, `hive` 4/32, `jackpot` 6, `drumlin` 6, `meander` 9) while winning the same ones
   (`fjordgate` 32/32, `archipelago` 28/32, `heart` 22/32). **It is a property of the
   aug7-lineage-vs-v44 matchup.** The ore-starvation story was explaining a pattern that was
   already there.
3. **Mechanism metrics and win rates keep coming apart, three times today.** The shipped facing
   change leaves the end-of-game conditional delivery rate statistically *unchanged* (52.9% vs
   `aug7`'s 53.1% head-to-head) while winning 58.5% — what moved was volume, **+29% titanium,
   +19% harvesters**. The discarded tie-break did the opposite: conditional rate **28.3% →
   74.0%**, terminal dangling conveyors **175 → 10**, and a **dead 50.0%** win rate.
   **End-of-game `chain_dir` is a snapshot; it cannot see time-to-first-delivery.** Measuring
   the round of each team's first delivery is now the highest-value instrument change.

## What is deliberately NOT in the challenger

- **The reactive home-defense port — unproven, and now moot.** `bots/_defense_port` has been
  measured on every instrument we own and has never once cleared a gate: **40.6% vs `opp_v44`**
  against a 40.8% baseline; **94.2% vs the weak `rush_probe`** against `aug7`'s 96.2%; and
  **63.7% [57.5%, 69.6%] vs `rush_probe_fast`** against `aug7`'s **60.4% [54.1%, 66.4%]** on the
  identical frozen build. Read honestly: it is **a wash everywhere, leaning very slightly
  positive against a real rush — unproven, not disproven.** An earlier reading of this as a
  regression was an artefact of comparing across two builds of the probe while its author was
  still editing it. Moot for stage 2 regardless: **`florent-v63` already ships an equivalent
  vision-triggered mechanism, more developed than ours.**
- **The deterministic trail-aware tie-break** (`bots/_tiebreak1`, and assembled as
  `bots/_pkg45b`). Screen 50.0% [39.9%, 60.1%], confirm **52.9% [48.4%, 57.3%]** — no verdict,
  therefore discard. It leans positive and its mechanism evidence is the strongest we have;
  resolving a ~3-point effect needs on the order of 1,900 matches. **Top of the next candidate's queue.**
- **Tuned constants.** A full CEM sweep of `MAX_BUILDERS` / `TARGET_HARVESTERS` / `AMMO_BUFFER`
  against v44 confirmed at **40.8% — identical to untuned `aug7`.** The gap is structural, not
  tuning. Directionally the elite distribution drifted `TARGET_HARVESTERS` 3→4 and `AMMO_BUFFER`
  20→~14. **Re-tune after the delivery economy changes, not before:**
  `.venv/bin/python tools/tune.py <candidate> opp_v45 --guards starter opp_v39`.
- **BFS pathfinding** — still discarded, code in `bots/_dev_bfs` (see session 6's entry).

## Known residual weaknesses

- **`atoll` 1/32 and `hive` 4/32 against `opp_v44`, and 0/32 on both against `opp_v45`** — the two lowest-ore maps in the pool. Single
  matches are unambiguous about the mechanism: on `hive` we finish with **125 buildings to their
  16** while collecting **400 to their 1,190**, and lose the Core at round 262. **We are
  out-delivered while spending more.** Every walked tile lays a conveyor, at +1% category scale
  each, whether or not that trail ever carries anything. A conveyor budget, a cap, or laying only
  where a trail already reaches a harvester are all cheap and untested. **This is the top
  economy lane for the next candidate.**
- **The near-Core dangling spike is unexplained.** The candidate still shows ~3× `aug7`'s dangling-head
  count at Chebyshev distance 1-2 — in a zone where its code is byte-identical to `aug7`. The
  far-zone topology is feeding the near zone differently and nobody has said how. Most likely
  place another chunk of delivery is hiding.
- **Small maps: `fjordgate` is our best map against both teammate bots — 32/32 vs v44 and
  26/32 vs v63 — and only the first has an explanation.** v44 gated its vision-triggered battery
  on `w*h > 120`, disabling it on the 10×10. **v63 removed that gate entirely** (confirmed in the
  source catalogue), so our continued 26/32 there is currently *unexplained* and worth one
  diagnostic before anyone assumes small maps are a strength of ours.
- **Mirror equivariance: still unfixed, still unmeasured this session.** Six of the 15 maps
  mirror; `cardinal_toward` is equivariant, and the new trail rule is defined relative to the
  walk (so it is equivariant under rotation *and* both reflections by construction), but no
  per-map mirror seat table was re-run for the candidate. `jackpot` is now repaired; `heart`, `lighthouse`
  and `atoll` seat asymmetries remain open.
- **`archipelago`'s seat advantage is an engine fact** (team A's Nth builder always gets the
  lower unit id, so A resolves first), not something the candidate changes.

## The next queue, ranked

**Stage 1, to finish and ship:** `bots/v63guard` gates (in flight at handover — check
`results.tsv`), then the human `fcode match test` TLE validation on real hardware, then activate.

**Stage 2, on the `florent-v63` base, one gated change at a time against pristine `opp_v45`:**

1. **Top-level `try`/`except` in their `run()`** — latent unit-loss bug, ~3 lines, same v1
   heritage as the CPU guard.
2. **Our trail-linked facing on their secondary opportunistic-pave path** — the only place their
   delivery still shows the defect (`chain_dir` 4/7 and 2/3 in ladder replays).
3. **Tell x3r0 about `heart`**: seated as team B, `florent-v63` builds **zero harvesters and
   collects zero titanium**, reproducibly (2 of 2 seeds) — we sweep that map 4-0 because of it.
   Same class of bug as the (0,0)-Core defect. Highest-value single thing in this handover after
   the CPU guard.
4. **`rush_probe_fast` stress-test on the integrated base**, then probe-hardening (more
   attackers, leaner probe economy) which was deferred out of this session.
5. **Re-tune constants on the integrated base** —
   `.venv/bin/python tools/tune.py <candidate> opp_v45 --guards starter opp_v39`. On our own line
   a full CEM sweep was worth **nothing** (40.8%, identical to untuned), so do this last.
6. **Re-run the per-map mirror seat table on the new base.** Six of fifteen maps mirror and
   nobody has checked whether their line is equivariant.

**Still true of any base:** instrument **time-to-first-delivery** (end-of-game `chain_dir` is a
snapshot and demonstrably cannot see what our accepted changes buy), and watch **conveyor spend
per delivered titanium** — we build 1,115 structures to their 651 and collect 14% less.

## Operating notes for the next session

- **The submission-watcher monitor does not survive this session.** It was a persistent monitor
  attached to the main session and dies with it. **Re-arm it** if you want submission/activation
  changes noticed automatically; nothing on the platform side reports them to us.
- **Standing norm: the team slot follows arena measurement.** A candidate that beats `opp_v44`
  takes the slot, with the numbers attached. This candidate does not, so it does not.
- **Date labels still run one day ahead of wall clock.** Every commit here is authored
  `Thu Aug 6 2026`; the log labels sessions 5-7 as `2026-08-07`/`08`. **Three logged "days" are
  one calendar day.** Left deliberately rather than silently renumbered.
- **Never reset `bots/ladder1` while an agent is measuring it** — still true, and it shaped this
  session's sequencing (the corrected variant was built in `bots/_facing_v2` precisely so a
  running census agent kept a stable artifact).
- Protected from edits: `tools/arena.py`, `tools/make_map.py`, `maps/`, `bots/starter`,
  `bots/v*`, `bots/probe_*`, `bots/rush_probe*`, `bots/opp_*`, `program.md`. Platform *write*
  commands (submit / activate / rename) are Magnus-only.
- `results.tsv` is the append-only tape and stays untracked; every run above is a row in it.
  Still no `git remote`.

## Where things live

| path | what it is |
| --- | --- |
| **`bots/v63guard`** | **stage-1 hotfix: `florent-v63` + our CPU guard** |
| **`bots/_pkg45`** | our challenger, now a component donor. `bots/ladder1` is a byte-identical copy |
| `bots/_facing_v2` | the candidate minus the (0,0) fix — the artifact the accept was measured on |
| `bots/_pkg45b`, `bots/_tiebreak1` | the discarded tie-break, packaged and standalone |
| `bots/_defense_port` | the reactive home-defense port, preserved, awaiting `rush_probe_fast` |
| `bots/aug7` (`3cfa588`) | pinned incumbent |
| `bots/_incumbent` (`a9d81a1`) | submission **v40** — what the ladder last ran from our line |
| `bots/opp_v45` | **x3r0's new active bot** (platform submission v45, "florent-v63") — the primary gate |
| `bots/opp_v44`, `bots/opp_v39` | the previous teammate bot (secondary reference) and the older guard |
| `bots/rush_probe`, `bots/rush_probe_fast` | the weak walked rush, and the Launcher-insertion probe |
| `bots/_fix_core00`, `bots/_dev_bfs`, `bots/_facing_v3` | superseded / discarded, kept for reference |
| safe to delete | `bots/_tune_*`, `bots/_diag_*`, `bots/_probe_*`, `bots/aug7_h1..h4` |

## Traps

All previous ones still apply — `python3` is 3.14 so use `.venv/bin/`; always `--tle 10`;
`print()` goes to the replay, use stderr; `random` is not seeded by `--seed`; never single-seat
or pooled-only evaluation; `ct.get_cpu_time_elapsed()` is inert under `fcode run`; the validator
rejects `try`/`finally`; tile queries raise outside vision; the comms store cannot represent a
zero; a pooled win rate cannot see a single-map defect. New this session:

- **`arena.py` reports the FIRST-NAMED bot's win rate.** A bare percentage in prose is a coin
  flip. Name both sides, every time.
- **A cross-tab that contradicts the headline is a defect to resolve before relaying**, not
  colour to relay alongside it. Both times the rush number went wrong, the contradicting
  cross-tab was in the same file.
- **A screen that fails uniformly across all 15 maps is a mechanism defect, not a refuted
  hypothesis.** 11.1% on every map meant "this breaks delivery everywhere", and the fix took one
  iteration once the census named cycles. A hypothesis refutation looks patchy; a broken
  mechanism looks flat.
- **Any facing/routing rule computed per builder can create cycles.** The census's cycle count is
  the diagnostic; it is not part of `replay_census.py`, it was a throwaway graph walk over its
  parsed output. Rebuild it before trusting the next routing change.
- **In zsh here, `set -- $var` inside a loop does not populate `$1`.** Cost two failed
  diagnostic runs; write the arguments out explicitly.
- **Pin the opponent before a comparison series — hash the file.** A peer agent was still
  editing `bots/rush_probe_fast` while I gated against it (mtime 17:46:35, mid-series), which
  silently turned an A/B into a comparison across two different instruments and produced a
  "defense is worse" reading that the re-run reversed. Every number in a series must come from
  the same opponent build.
- **`ct.get_cpu_time_elapsed()` is inert under `fcode run`, so any CPU-guard code you add is
  untestable locally by ordinary means.** Force it: build a throwaway copy with the threshold at
  0 so every guard fires, and require zero crashes. Otherwise you are shipping code paths that
  have never executed.
