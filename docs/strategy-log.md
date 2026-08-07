# Strategy log

The point of this file: in a ladder game, the thing that compounds is knowing which changes
moved the rating and which didn't. Memory is unreliable and the ladder is noisy — write it down.

**One entry per deployed bot version.** Write the hypothesis *before* deploying, the result
*after* the ladder has settled. Keep dead ends — a documented failure is worth as much as a win.

Rules of thumb:
- Change one meaningful thing per version, or you can't attribute the result.
- Give the ladder enough matches to be meaningful before calling it. Note the sample size.
- If the result surprises you, that's a fact for [game-model.md](game-model.md), not a tweak.

---

## Template

### v0 — name

- **Date deployed:**
- **Commit / tag:**
- **Hypothesis:** what we believe and why we believe it
- **Change:** what's actually different from the previous version
- **Predicted effect:** stated before deploying, so we can be wrong on the record
- **Result:** rating before → after, over N matches
- **Read:** did the hypothesis hold? what did we learn regardless?
- **Next:** what this points at

---

<!-- newest entries at the top, below this line -->

### Session 10 morning — counter-battery blindness named, and v54 ships on a judgment trade

- **Date:** 2026-08-07 morning (Magnus present) · base `_v69clean` → `_v70rp` → `_v70mh` = **platform v54 "v70-respawn-convergence"**, shipped ~08:05 at 1550@197.
- **The Lunds audit (10 games decoded) unified the middle class:** one infiltrator, one
  turret near our core, 150-900 rounds of chip while we bank thousands — named
  **counter-battery blindness**. Root causes: the counterbattery eco-gate, single-slot
  SLOT_THREAT, fixed turret facings. Lunds went 0-5 lifetime against us on it.
- **Two gated keeps:** builder respawn-on-death (`self.n` was a lifetime cap — the
  eider diagnosis: 586 rounds on 2 builders, 12.3k Ti unspent; replacements gated
  ti≥250∧rnd≥60, no cap raise = the `_v69bc` lesson applied) and multi-healer
  convergence (role-2/5+ expanders in vision of a damaged core converge; +8..12/rnd
  flips the single-sentinel arithmetic).
- **Battery:** flotte 93.3 [89.4,95.9] vs 86.7 (+6.6, the wild class), band 93.3,
  kladde 71.2 flat (the probe's 3-sentinel barrage out-damages any heal rate — probes
  can be harder than their wild exemplars), guards green, opp_v50 59.2 vs 63.3
  (-4 overlapping). **Magnus called the trade: ship** — the ladder pool resembles the
  probes, not the teammate proxy.
- **Retro (Magnus-requested) adopted three process fixes** — map-targeted screens
  before full runs; pre-mortem variants against the losing replays (four
  trace-proven-but-game-flat variants motivated it); thresholded monitors. In the
  operating notes and the orchestration memory.
- **Next:** v54 before/after rematches (Lunds/Flotte legs queued at ship time),
  turret-hunting design (pre-mortemed first), the grind residual's real binding
  constraint, nemesis audits (Ouroboros 0-4 likely grind-class).

### Session 10 overnight — the autonomous loop: one ship, three honest refutations, the triad complete

- **Date:** 2026-08-10 overnight (wall clock Aug 6 23:00 → Aug 7 ~00:30+) · autonomous
  /loop while Magnus slept, policy: ≤3 submissions on the full bar · base `_v67ch2` (v52)
- **Shipped: platform v53 "v68-saboteur-escort" (`_v68si`).** The Flotte saboteur can't be
  killed (builders cannot attack units — implementation caught the spec error), so the
  interceptor became a repair escort: guard the victim building, out-heal the pecks
  (1 Ti/+4 HP vs 2 Ti/2 dmg). +10.0 on flotte_probe with separated intervals, flat on all
  four other instruments. Ladder: 7-3, peak 1557/#26.
- **Instrument triad completed:** kladde_probe (grind class) joins band_probe and
  flotte_probe. Live-bot baselines 90.0 / 86.7 / **73.8** — the grind is the open front.
  Kladde extraction's key fact: on meander they LOST the economy race the whole game and
  still won — patience + a 40-round late strike vs a core that happened to have no
  healers. Both reference games predate the heal reflex.
- **Refuted honestly, all on their own target instruments:** perimeter patrol (eider
  converted, then churned away on three other maps — net negative); builder-cap scaling
  as cap-8+replacements (~13-pt opp_v50 regression: cost-scale inflation where the
  economy thrives, never engages where it's suppressed); the whole `_v67hg*` battery-gate
  line (heal package absorbed its value — 40.0 vs 93.3 on band_probe).
- **Held:** defend-role succession (`_v69dr`) — mechanism proven in mock traces (death
  r36 → promote r42 → three home sentinels), inert in every instrument's games, zero
  cost. In the family base as insurance. Dead engineer branch removed (`_v69clean`,
  byte-identical verified). **`_v69clean` is the next-session base.**
- **The residuals are now MAPPED, not mysterious:** grind = we lose the 1000-round
  titanium race 13.8k vs 17.5k (uncapped economy vs our caps — leaner cap re-tune is
  queue 1, replay captured); strangle eider/meander = resisted three targeted fixes,
  needs new mechanism evidence; nemeses Powerpuff/I Stone each beat two consecutive
  versions narrowly.
- **Meta:** ~8 gated measurements, 3 implementations, 3 extractions, 2 probe builds in
  ~90 minutes of loop time; two-tier discipline held throughout (every verdict from the
  main loop's own arena runs); the ship bar rejected four candidates the local numbers
  couldn't justify — the bar working exactly as designed.

### Session 10 — the night x3r0 shipped three bots, and the mirror table came up all-lottery

- **Date:** 2026-08-09/10 (session 10; wall clock 2026-08-06 evening) · bases `bots/v6`
  (= `_v64cbA`, live as platform v48 at session start) then the `_v65*`/`_v66*` family ·
  gates `opp_v45` → `opp_v49` → `opp_v50` as x3r0 kept shipping
- **Ladder:** v48 went 1383 → 1421 over 3 matches (its "Last 10: 3W 7L" scare was unrated
  test games polluting the platform stat, not losses). Then x3r0's test window: platform
  v49 (18:17), v50 (18:48, active, ~1461 @ 140). Teammate window = named confound, no
  regression reasoning applies.

**Five gated changes measured, three kept, one refuted, one held:**

1. **`_v65lw` (KEEP):** `LAUNCH_GIVEUP_RND = 180` — the r180 give-up / r<200 re-recruit
   flip-flop made the give-up dead code. Flat on all three non-mirror instruments
   (97.9 / 99.2 / 96.7), 0 crashes. Correctness at zero cost.
2. **`_v65sb` (KEEP):** `LAUNCH_STALL_RNDS = 36` per-unit launchwait progress bound +
   12-round re-recruit block (audit: a waiter recruited at r12 could idle to r180, or
   forever in matches decided earlier — and matches ARE decided earlier). Flat-to-up
   (98.8 / 99.2 / 97.1). Zero-gain vs x3r0's engine (58.8% unchanged, per-map identical):
   insertions rarely resolve there, so the fix pays vs third parties, not him.
3. **`_v66mA` (REFUTED):** global melee-before-repair (ported from his v49's `_saboteur`
   reorder). Drumlin 0→16/32 but hive sweep lost (32→16), moonrise handed over (16→0),
   eider dented: 55.4% vs baseline 58.8%. **Repair-first is load-bearing on denser maps.**
4. **`_v66mB` (KEEP, = `bots/v7`):** the same reorder wall-gated to <1.5% wall fraction —
   only drumlin (0.64%) qualifies; next is meander (2.13%). vs v49: **62.1% [57.7, 66.3]**,
   exactly baseline + the predicted drumlin dividend, all sweeps intact. vs v50 (shipped an
   hour later): **56.7% [52.2, 61.0]** — his v50 re-took drumlin, lighthouse fell to us.
   Guards 97.5 / 100.0 / 97.5. **Frozen as v7 by Magnus, awaiting submit.**
5. **`_v66eq` (HOLD):** rotation-equivariant `_plan_siege` tie-break (raw x,y ties → map-
   center then own-core distance). Sanity-proven on synthetic mirrors (old key near-reversed
   tie blocks; non-lead engineers drew from the wrong end). vs v50: 58.8 vs 56.7,
   overlapping, per-map churn (+drumlin +snowflake −lighthouse −eider). Held as base for
   finishing the set: spawn-ring sort (:409), spawn-dispersion hash (:412, a coordinate
   hash as PRIMARY key), ore partition (:1421).

**The structural finding — queue item 4 finally ran.** `_v66mB` self-play, 480 matches:
**every one of the 15 maps is fully seat-decided** (9 to seat B, which rules out first-mover
advantage as the cause — our own asymmetries decide). `_v66eq`'s mirror: still 15/15
seat-decided, heart flipped direction. Under a deterministic engine, one residual asymmetry
re-decides everything: **the mirror table is all-or-nothing and cannot grade partial fixes.**
Judge equivariance work per-map against a different engine.

**Tooling:** `tools/sprt.py` (queue item 6) built by an Opus subagent, calibrated by us on
the settled 70% gate — H1 accepted at 40/480 matches, estimate exactly 70.0%, 15 s. Adopted
for screens/discards; ship gates stay fixed-480. The `_v66mA` refutation and both `_v66eq`
screens ran on it; the drumlin variant screens cost seconds.

**Meta:** two-tier ran at full tilt — six subagent delegations (three Opus implementations,
two Sonnet audits, one Opus toolbuild), zero measurement delegated, every verdict from the
main loop's own arena runs. Shipping rule amended by Magnus: local-battery-clean ships;
Elo trajectory check is rolling and post-hoc. x3r0 adopted our ladder1 CPU/exception guards
in his v49+; his map-pack refresh mooted message 1 to him; the counterbattery gate (his v50
still drops fjordgate AND meander 32/32 to us) is now the headline handover.

**Next:** finish the equivariance set on `_v66eq` (one sort per gated change, SPRT-screened,
judged vs `opp_v50` per-map); then the launch-insertion resolution problem; then fjordgate
root causes (shared with his engine); constants re-tune last.

### Session 9 — one gate converts two maps, and the second one was not the one we aimed at

- **Date:** 2026-08-09 (session 9; wall clock 2026-08-06, the one-day label skew stands) ·
  base `bots/v5` (= live submission **platform v47 "v63-mapfix-launcher"** = `_v63full`),
  gate `bots/opp_v45`, 480 matches
- **Ladder check first, and it is a non-result:** `fcode status` reads rating 1383, rank #40,
  **132 matches** — byte-identical to the activation baseline logged at the end of session 8.
  v47 has played **zero** ladder matches since going live. The 63.3% prediction remains
  untested; there is nothing to compare yet. Watcher re-armed.

**The change:** queue item 1, exactly as diagnosed in session 8 — mirror `_plan_siege`'s
economy gate onto `_try_counterbattery`, which had neither a forward-gun cap nor an economy
gate:

```python
if ct.read_store(SLOT_HOME_GUN) >= 1 and ct.read_store(SLOT_HARVESTERS) < ECO_NEED:
    return False
```

Six added lines over `bots/v5`, nothing else, verified by diff. Both call sites
(`_home_defend`, `_defend`) route through the one function, so one gate covers both.

**Result: 70.0% [65.8%, 73.9%] vs the live bot's own engine, up from 63.3%, 0 crashes both
sides.** +32 wins is exactly two maps converted, and the per-map table says which:

| map | `_v63full` (live) | `_v64cbA` | |
| --- | --- | --- | --- |
| fjordgate | 16/32 | **32/32** | predicted from source, twice over |
| meander | 16/32 | **32/32** | **not predicted — this was queue item 3** |
| drumlin, eider, heart, saga | 32/32 | 32/32 | held |
| the other nine | 16/32 | 16/32 | unmoved |

**Read:** fjordgate is the clean confirmation — a mechanism read off the source in session 8
(ungated counterbattery buys three fixed-facing Sentinels at *transient spawn tiles* by round
6; any home gun makes `weapons` truthy, pinning `ti_floor` at 12 forever; seed 1 ended 255
rounds at 0 harvesters and exactly 12 Ti) predicted a specific map would convert, and it
converted 32/32 both seats, every win by core kill.

**Meander is the more interesting one, and the honest version is narrower than it looks.**
Session 8 left meander as an open puzzle: it got its map-table entry, so `_plan_siege` was
enabled there, and it still sat at 16/32. What we now know is that the counterbattery gate
converts meander **on top of** the map tables — the table fixed *can it plan a siege*, the
gate fixed *can it still afford one*. What we have **not** established is the other direction:
the gate alone, without the tables, was never measured on meander, so "these two only pay
together" is a hypothesis, not a result. It is the mirror image of session 8's trap (two
changes that each gate keep and fail to stack): two changes that individually leave a map dead
and jointly convert it. Both directions argue the same thing — **attribute per map, never
reason about components from the pooled number.**

**Refuted on the way (recorded because it was the tempting fix):** `_v64cbB`, the strict gate
with no free first battery — on the theory that one gun alone is enough to pin `ti_floor`.
Fjordgate-only screen, 32 games: pooled 16/32 but **seat A 32/32**. Removing early home
defense does not cure the collapse, it converts the map into a pure first-mover coinflip. The
first battery is load-bearing; the second one onward is the bankruptcy. Screening one map for
6 seconds before spending a 480-match gate is the cheap move that made this visible.

**Guards, all three passed — and the rush guard is a second finding:**

| guard | `_v63full` (live v47) | `_v64cbA` | |
| --- | --- | --- | --- |
| vs `starter` | 98.3% | 97.9% [95.2%, 99.1%] | flat, no regression |
| vs `opp_v39` | 98.3% | 99.2% [97.0%, 99.8%] | flat/up |
| vs `rush_probe_fast` | 86.7% [81.8%, 90.4%] | **95.4% [92.0%, 97.4%]** | **intervals do not overlap** |

The rush number was not something we set out to move, and it is the same mechanism seen from
the other side: **the opening bankruptcy was also what lost to rushes.** A bot that has spent
its opening bank on three fixed-facing Sentinels aimed at spawn tiles has nothing left when a
real attack arrives; an economy that stands can afford real defense. On the one frozen rush
instrument the line now reads aug7 60.4% → `_pkg45` 64.2% → `v63guard` 82.1% → `_v63full`
86.7% → `_v64cbA` 95.4%. 0 crashes on our side in all three guards.

**Next:** `_v64cbA` is a validated ship candidate over v47 — Magnus freezes it into `bots/v6`
and submits (`bots/v*` is agent-write-protected). Prediction on the record, to be checked the
way session 8's was: it should beat v47's ladder performance, and the honest caveat is that
the 70.0% is measured against v47's *own engine* in mirror, where our six swept maps are
worth 6/15 of the pool — against a diverse ladder field the effect will be smaller.

- **Date:** 2026-08-08 (session 8; wall clock still 2026-08-06 — the one-day label skew stands) ·
  base `bots/v63guard` (= live submission **v46 "v63guard-tle-armor"**, activated by Magnus, team
  rating 1310 → ~1377 during the session), gate `bots/opp_v45`, all gates 480 matches
- **Stage 1 confirmation:** the real-hardware `fcode match test` TLE validation passed (tape row:
  5-0 vs starter on the 5 heaviest maps) and v46 is the active ladder bot, 10-0 in its first ten.
- **Four components gated separately vs pristine `opp_v45`, one at a time:**
  1. **Crash armor** (`bots/_v63armor`, top-level try/except): **exactly 240-240 and 16/32 on all
     15 maps** — the inertness fingerprint; kept on the insurance precedent. **keep**
  2. **Launcher wake-up** (`bots/_v63launch`, two edits: v58's `_try_build_launcher` call site
     restored, recruit gate `role_n >= 5 → 3`): 53.3% pooled, **eider swept 32/32, every other
     map dead 16/32**. Diagnostic replay: the payoff was NOT the insertion throw — the round-8
     Launcher **exiles the enemy's opening saboteur** (defensive throw, round 10). **keep**
  3. **Trail-linked facing port** (`bots/_v63face`, our accepted outward-pave rule on their
     expander walk): **refuted 31.7% [27.7%, 36.0%]** — 0/32 on five maps, inert elsewhere.
     The rebuilt cycle census was clean (0 cycles in 306) but showed **+65% relay spend**: the
     mechanism that bought our line 58.5% transplants our overspend weakness onto their lean
     economy. Their inward-only pave + BFS-planned links is correct for their base. **discard**
  4. **Map-table refresh** (`bots/_v63maps`, entries for eider/heart/meander/drumlin/saga):
     **63.3% [58.9%, 67.5%] — the largest accept ever measured against a gate this strong.**
     32/32 both seats on drumlin, eider, heart, saga. **keep**
- **The load-bearing discovery (subagent equivariance audit): v63's hardcoded map tables predate
  the current weekly rotation.** Five pool maps have no entry → `known_map_for` returns None →
  `_plan_siege` (their primary attack) silently disabled on 5 of 15 maps. This one fact explains:
  the **heart zero-harvester-as-B defect** (fixed at the root: 1 building/0 mined → 75
  buildings/2450 mined), the **eider launcher sweep** (base can't siege there, games decay to
  tiebreaks where our exile-defense wins), and part of the v63 line's map-shape variance.
  **Weekly-rotation corollary now in the runbook: refresh embedded map tables at every cutover.**
- **fjordgate diagnosed (subagent, both seeds reproduce):** on the 10×10 the absolute threat
  radii cover the opponent's normal opening area; economy-ungated `_try_counterbattery` spends
  the bank on Sentinels aimed at transient spawn tiles by round 6, then the home-gun ammo policy
  (`ti_floor` → 12) converts all income to ammo forever — **0 harvesters in 255 rounds.** We win
  26/32 there because at core separation d²=32 our defensive sentinel ring reaches their core.
  Fix named: mirror the siege path's ECO_NEED gate onto `_try_counterbattery`. Top of next queue.
- **Ship candidate: `bots/_v63full`** = v63guard + armor + launcher + maps. Ship gate **63.3%
  [58.9%, 67.5%]**, identical to maps alone (launcher's eider win subsumed; armor inert), 0
  crashes anywhere. Rush stress on the integrated line: 80.0% vs `rush_probe_fast` against the
  base's 82.1% — no regression, and **the v63 line concedes half what our lineage does to a
  competent rush** (their 82% vs our 60-64%, same frozen probe). No-collapse guards in flight at
  write time; numbers on the tape.
- **Read:** the biggest wins of the base-switch era are correctness-at-the-seams (stale tables,
  dead subsystems), not strategy. Both decisive finds came from reading their source against the
  current pool, not from matches — and both were found by delegated read-only audits.
- **Next:** counterbattery ECO_NEED gate; launchwait flip-flop wart (r180-199); meander (table
  entry does no harm but siege doesn't convert it); mirror seat table on the new base still unrun.

### The gate moved out from under us, and the honest endgame is a base switch

- **Date:** 2026-08-08 (session 7), late · challenger `bots/ladder1` / `bots/_pkg45`, new primary
  gate `bots/opp_v45` (x3r0's active "florent-v63")
- **What happened:** mid-session our teammate shipped five internal iterations at once.
  **`opp_v45` beats `opp_v44` 78.3% [70.1%, 84.8%] and beats `aug7` 80.0% [72.0%, 86.2%]**, so
  the primary gate moved to the stronger teammate bot, as the standing norm requires.
- **Our candidate scores 22.1% [18.6%, 26.0%] against it over 480 matches, 0 crashes.** For
  reference `aug7` scores 20.0%. **A full session of gated economy work moved this matchup by
  about two points.**
- **Their economy is better than ours, which kills the "port our fix onto their base" plan
  before it starts.** A 20-replay paired census (5 maps, both seats):

  | | ours (`_pkg45`) | `opp_v45` |
  | --- | --- | --- |
  | conditional delivery rate (`chain_dir`/`chain`) | 70.0% | **86.2%** |
  | titanium collected, pooled | 58,510 | **66,630** |
  | structures built, pooled | **1,115** | 651 |
  | conveyors | **1,038** | 552 |
  | Cores surviving, of 20 | 9 | **20** |

  **They collect 14% more while building 42% fewer structures.** They show no sign of the
  facing/termination defect we spent this session repairing — and our own candidate still throws
  one clean instance of it (`drumlin`, 1 chain, 0 `chain_dir`, 0 collected).
- **The decisive gap is combat and it is not close. Of their 15 wins over us, 11 are Core kills.
  Our Core died 11 times in 20 matches; theirs died zero.** Their first Sentinel lands at
  **median round 24 against our 51**; they field Gunners (59 built, 18 surviving) where we build
  none; they never even needed a Launcher against us in this sample. On the 9 matches that
  reached the economic tiebreak we actually won 5-4.
- **Conclusion, stated plainly because it is the deliverable: the team's strongest bot is
  `florent-v63`, not ours, and it cannot be caught from here by economy repair.** Recommend
  switching bases and carrying findings across rather than code. What our line still has to give:
  **a reproducible economy failure in `florent-v63` itself — on `heart` seated as team B it
  builds zero harvesters and collects zero titanium, 2 of 2 seeds**, which is why we sweep that
  map 4-0; the small-map area gate on their vision-triggered battery (`fjordgate` 26/32 for us
  against v63, 32/32 against v44); the (0,0)-Core store fix if their line still writes raw
  coordinates; and the instruments — `tools/replay_census.py`, `tools/arena.py`, and this tape.
- **`rush_probe_fast` landed and is a real instrument at last.** Against a frozen build:
  **`aug7` 60.4% [54.1%, 66.4%]**, matching the probe author's independent 61.7%, where the old
  walked `rush_probe` conceded only ~4%. An undefended economy bot loses ~39% of games to it.
- **The reactive-defense port, final verdict: a wash on every instrument — unproven, not
  disproven.** Against that same frozen probe it scores **63.7% [57.5%, 69.6%]** to `aug7`'s
  60.4%, and our economy candidate **64.2%**: all three overlap. **An earlier reading of the
  defense as a regression was a method defect of mine** — the two runs straddled an edit to the
  probe by its own author (file mtime mid-series), so they measured different instruments.
  Corrected on the tape, and the trap is now in HANDOVER: **pin the opponent build before a
  comparison series.** The mechanism stays unproven; it is moot for the base switch anyway,
  because `florent-v63` already ships a more developed version of it.
- **The finding that turns the base switch into something we can ship today: `florent-v63` has
  no CPU guard, and it is losing real ladder games to that.** A decoded ladder replay shows
  **272 CPU-truncated rounds out of 310, losing by `core_destroyed` while paralysed**, and a full
  source audit of their line finds **zero `get_cpu_time_elapsed()` calls** in either v58 or v63.
  Our line has carried a phase-boundary guard since v2. Their author is out of tokens.
  **So stage 1 is `bots/v63guard` — their code, our guard, nothing else** — and stage 2 is the
  rest of the integration. Their `run()` also dispatches without a top-level `try`/`except`, so
  any escaping exception permanently deletes the unit; latent today (0 crashes in 480 matches),
  but the same three lines that saved our line in v1.
- **The bar is now frozen** at `opp_v45`: no further teammate uploads are coming.

### The `ladder1` candidate's economy change — conveyor facing follows the trail, and the failed first attempt named the real constraint

- **Date:** 2026-08-08 (session 7) · challenger `bots/_facing_v2`, pinned incumbent `bots/aug7`
  (`3cfa588`), primary gate `bots/opp_v44`
- **Hypothesis, pre-specified by the previous session's census:** 71% of residual facing failures
  are path bends, where "dominant axis toward the Core" and "along the trail" disagree. Facing
  each trail conveyor at the trail's own continuation should close them.

**The first implementation was refuted at the screen, and that is where the real finding is.**
The pure rule — an outward-walking builder faces the new conveyor back at the tile it came from,
always — screened at **11.1% [6.1%, 19.3%]** over 90 matches, losing on **all 15 maps**, 0
crashes. A census of 30 fresh replays says why, and it is not what either competing hypothesis
predicted:

| terminal cause of a non-delivering conveyor | pure trail rule | `aug7` |
| --- | --- | --- |
| **closed cycle** (mutual-pointing loop, can never reach the Core) | **931 (43.6%)** | **0** |
| dangling into empty ground | 726 | 725 |
| wall / building / other | 476 | 923 |

- **Cycles are the dominant failure, and `aug7`'s rule cannot produce a single one.** "Point at the
  Core" is a *global field*: every arrow descends the same potential, so loops are impossible by
  construction. "Point back down my own trail" is *local per builder*, and two builders crossing
  the same corridor in opposite directions point at each other. **84% of the cycles sat within
  Chebyshev distance 5 of the Core**, where trails converge and cross most.
- The predicted origin gap was real but secondary: dangling heads landed on a recorded
  builder-spawn tile **23.6%** of the time against `aug7`'s **4.8%** — the first trail tile points
  back at the spawn tile, which never receives a conveyor.
- **The transferable lesson: conveyor facing is a global consistency problem.** A local rule is
  only safe if it is anchored to a global one. Conditional delivery rate collapsed **44.0% →
  7.2%**; on `drumlin`, the wall-free control where `aug7` scores best, the pure rule scored
  **0.0%**.

**The corrected rule keeps both properties and it clears the gate.** Trail linking applies only
when the builder is walking outward **and** `next_pos` is farther than
`NEAR_CORE_FACING_DIST_SQ = 18` from the Core; inside that radius `aug7`'s converging field is
kept byte-for-byte, so chains still terminate *into* the Core and the crossing-trail zone keeps
its global anchor.

| measurement | result |
| --- | --- |
| screen vs `aug7`, 90 matches | 66.7% [56.4%, 75.5%] |
| **confirm vs `aug7`, 480 matches** | **58.5% [54.1%, 62.9%] — lower bound clears, ACCEPT** |
| no-collapse vs `starter`, 480 | 75.2% [71.2%, 78.9%] (0 crashes us, 808 theirs) |
| no-collapse vs `opp_v39`, 480 | 69.0% [64.7%, 72.9%] — above the 65.8% `aug7` reference |
| primary gate vs `opp_v44`, 480 | 43.8% [39.4%, 48.2%] — **does not clear 50%** |
| cycles in 1,891 non-delivering conveyors | **0 — the failure mode is gone** |
| crashes, all 2,000+ matches | **0** |

Per map against `aug7` it is broad rather than concentrated — above half on 12 of 15, no map
collapses, and the largest margin is **`heart` 26/32**, which is exactly the map where
zero-delivery was first observed.

**Read it honestly, because this is the second facing change in a row whose win the facing
metric does not explain.** In a like-for-like census (30 matches, both seats) the conditional
delivery rate came out **52.9% for the challenger against 53.1% for `aug7` — a dead tie.** What
moved was *volume*: harvesters 165 vs 139, graph-connected chains 140 vs 113, and **titanium
collected 166,920 vs 129,630, +29%**. The change buys more economy, not a higher *fraction* of
correct facings. Two candidate explanations, both testable: end-of-game `chain_dir` is a
snapshot that cannot see **time-to-first-delivery** (a chain that completes 200 rounds earlier
scores identically), and a bot with more income simply builds more harvesters. **Next
measurement should be first-delivery round, not end-state facing.** Also unresolved and recorded
rather than explained away: the challenger still shows a **3× dangling-head spike at Chebyshev
distance 1-2** versus `aug7`, in a zone where its code is byte-identical to `aug7` — so the
far-zone topology is feeding the near zone differently, and nobody has said how.

**What went into the candidate package alongside it: the (0,0)-Core store fix**, which has been waiting
on a decision since the previous session. Inside the assembled candidate it takes **`jackpot`
seat A from 0/32 to 15/32 = 46.9% [31%, 64%]**, with 29 of 32 games now decided on titanium
collected rather than a harvester tiebreak. It has **exactly one writer and one reader** of those
two slots, so it is **provably inert on every map whose Core is not at (0, 0)** — `jackpot` alone
in this rotation. That argument, not the pooled no-verdict it produced last session, is why it
ships.

**And the gap to `opp_v44` is structural, from three independent directions.** The assembled
package scores **44.8% [40.4%, 49.3%]** against it — up from `aug7`'s 40.8% but with the upper
bound now *excluding* 50%. A full CEM constants sweep landed at **40.8%, identical to untuned
`aug7`** — tuning buys nothing. And the per-map split is the same bimodal shape as everything
else we run against v44: **`fjordgate` 32/32** — a clean sweep of the 10×10 map where v44's own
`w*h > 120` gate disables its vision-triggered battery, exactly the hole read out of its source
last session — **`archipelago` 28/32, `heart` 22/32**, against **`atoll` 1/32 and `hive` 4/32**,
the two lowest-ore maps in the pool. Single-match reads on those two are unambiguous about the
direction: we finish with **125 buildings to v44's 16** on `hive` while collecting **400 to their
1,190**, and lose the Core at round 262. **We are not out-teched there, we are out-delivered
while spending more.** That is the next lane: conveyor spend per unit of delivered titanium.

- **Date:** 2026-08-08 (session 7) · no code change; three corrections to entries below, two of
  them to claims made *today*. Date labels still run one day ahead of wall clock — see the
  standing note in HANDOVER.md; every commit here is authored Thu Aug 6 2026.

**1. `bots/rush_probe` is weak, and a number was relayed inverted.** The control run settles it:
**`aug7` beats `rush_probe` 96.2% [93.0%, 98.0%]** over 240 matches. The defense-carrying
`ladder1` scores **94.2% [90.4%, 96.5%]** against the same probe over 240 — **the intervals
overlap and the point estimate is two points lower**. So the reactive-defense port has **no
demonstrated benefit against a rush**, and a hint of cost.

For a while today the belief in circulation was the opposite — that the port had "inverted a
95/5 rush matchup". It came from reading "the 95.0% rush baseline" as *the rusher's* score. It
was always the **defender's**: the entry below already says so in bold, and the cross-tab it
reports says it twice over — **the probe's own Core died 22 times to `aug7`'s 5**. A probe that
loses its own base four times more often than it takes yours is not dominating anybody.

- **Rule, because this cost us a working session's framing: a metric report must name both
  sides.** Write "X beats Y at N%", never "the baseline is N%". `arena.py` reports the
  **first-named** bot's rate, and a bare percentage is a coin flip in prose.
- **Rule: a cross-tab that contradicts the headline is a defect to resolve before relaying, not
  colour to relay alongside it.** Both times this number went wrong, the contradicting
  cross-tab was sitting in the same log file.

**2. The defense port's "violently bimodal per map" split was mis-attributed to the port.** The
entry below reads a 0-for-32 on `hive` and 3-for-32 on `atoll` as structural evidence about the
defense mechanism, with ore starvation as the leading explanation. **Today's facing candidate
carries no defense change at all and collapses on the same maps against the same opponent:**

| vs `opp_v44`, wins /32 | `atoll` | `hive` | `jackpot` | `drumlin` | `meander` | `snowflake` |
| --- | --- | --- | --- | --- | --- | --- |
| `ladder1` + reactive defense | 3 | 0 | 6 | 7 | 9 | 3 |
| `_facing_v2`, no defense change | **0** | **0** | 5 | 5 | 9 | 11 |

The strong end matches too (`archipelago`, `lighthouse`, `moonrise`, `heart` high in both). **The
bimodality is a property of the aug7-lineage-versus-`opp_v44` matchup, not of either change.**
The ore-starvation hypothesis is not refuted as physics, but it is no longer *evidence for*
anything about defense — it was explaining a pattern that was already there.

**3. Consequence for the candidate package: the reactive defense is NOT in it.** It failed its primary
gate (40.6% vs `opp_v44` against a 40.8% baseline), it shows no benefit against either rush
instrument (see the newest entry above: 61.3% against `rush_probe_fast` where plain `aug7` scores
68.3%), and the per-map argument that kept it alive belonged to the matchup. It is
preserved intact at **`bots/_defense_port`** — the mechanism (threat detection decoupled from our
own economy) is still the right idea and the ladder rush threat is still real and independently
evidenced (the watched blowout loss, the turn-1-Launcher benchmark in opponents.md, the
first-Sentinel cluster at rounds 3-6 across 24 real replays). **What we lack is a competent local
rusher to test it against.** `bots/rush_probe_fast` — launcher insertion, with enough economy to
sustain ammo — is that instrument. **It landed the same evening, it IS genuinely dangerous
(`aug7` beats it only 68.3%, against 96.2% for the walked probe), the defense port was gated
against it, and it lost at 61.3%.** This lane is closed rather than open — see the newest entry.

### Finding — the facing bug has three distinct causes, we fixed the smallest one, and the real one is now named

- **Date:** 2026-08-08 · 28 fresh replays + 24 ladder replays, censused with
  `tools/replay_census.py`. No code change. **This retroactively re-characterises an accepted
  change, which is exactly what a mechanism measurement is for.**
- **The isolating metric.** Raw `chain_dir%` rose 36.3% → 44.7% from `v4` to `aug7`, but that is
  confounded — `aug7`'s raw `chain%` (undirected connectivity) also rose 76.5% → 91.3%, i.e. it
  is simply the stronger bot. The number that isolates *facing* is the **conditional rate**: of
  harvesters that got graph-connected, what fraction also face correctly.
  **v4 47.4% (37/78) vs aug7 48.9% (46/94) — z ≈ 0.2, not significant.**
  **Pooled, `cardinal_toward` did not measurably close the facing gap.**
- **But it did exactly what it was designed to do, and the per-map story is sharp:**
  - **The chirality bug is dead.** Non-tie wrong-cardinal picks: **8/58 for v4, 0/63 for aug7.**
    Caught live and deterministically: on `hive`, tile (22,5) is built `stored_facing=WEST` in
    two independent seeds where the correct dominant axis is NORTH — `nearest_cardinal`'s
    "NORTHWEST always snaps to WEST" defect, reproducible because it depends only on geometry.
  - **On `drumlin`, the wall-free control, the conditional rate goes 50% → 91.7%.** Where paths
    are straight, the fix is close to total.
  - **On `heart` it goes the wrong way: 37.5% → 12.5%** — and `heart` is precisely where
    zero-delivery was first observed.
- **Cause #2, and it is 71% of the residual: facing is computed per tile as "dominant axis
  toward the Core", not "toward the next tile in the actual trail".** Any path that bends —
  staircase routing around terrain — breaks the chain **even when every individual tile's facing
  is locally correct**. 45 of aug7's 63 breaks are exactly this. Worked example
  (`aug7_v4_heart_s1`, chain 4/4, `chain_dir` 0/4, **0 titanium**): tile (12,11) correctly
  computes WEST because the Core is far more west than north — but the real trail continues one
  more tile *north* to (12,10) before turning west, so the WEST-facing conveyor never meets its
  own continuation. **A conveyor should point where the trail goes, not where the Core is.**
  Straight-line and trail agree only on straight paths, which is why `drumlin` looks fixed and
  `heart` does not.
- **Cause #3, rarer but the most expensive per occurrence: exact diagonal ties cluster near the
  Core**, where many independent harvester trails converge onto a few shared trunk tiles.
  `aug7_v4_archipelago_s1`: tile (18,20) is an exact tie, resolved to NORTH instead of EAST, and
  **that single tile is the shared last hop for 8 of 12 harvesters** — all collapse together.
  `cardinal_toward` breaks ties with `random.random()`, i.e. **50/50 at precisely the tiles where
  being wrong is most expensive.** aug7 hits this on 10/63 of its breaks against v4's 29/58.
- **Zero-collected ↔ `chain_dir == 0`: 18/18 perfect** in games decided economically, on an
  independent sample. **Correct causal statement, with the qualifier the census earned:** zero
  economy **always** implies `chain_dir == 0`; the converse holds **only in economically-decided
  games** — 5 of 18 `chain_dir == 0` sides in combat-truncated ladder games had positive
  titanium, because chain/chain_dir are end-of-game snapshots and a network can be destroyed
  after banking.
- **Field-wide, and not flattering:** across 24 ladder replays, 42 team-sides, 10 distinct
  opponents — conditional rate **68.4%** against our **48.9%**. The facing gap is a
  field-wide phenomenon, **and we are below field average at it.**
- **Confound recorded honestly:** `aug7` vs `v4` differ by **two** changes (Sentinel-first *and*
  `cardinal_toward`), so this is a good proxy for the facing mechanism but not a clean
  single-change test. **The clean comparison is `aug7` vs `bots/_incumbent`** (`a9d81a1`, which
  is aug7 minus `cardinal_toward`) — cheap, and worth running before anyone concludes the accept
  was mis-attributed. The 57.9% win rate itself remains properly attributable: it *was* measured
  against a one-change baseline. What this census shows is that the win is **not** primarily
  explained by facing-correctness, which is a different and more interesting claim.
- **The next experiment, now precisely specified:** in `_try_move`, face the trail conveyor
  **toward the tile the builder is about to step onto** (the trail's own continuation) rather
  than toward the Core. One attributable change, addresses 71% of the residual breaks, and needs
  no new state — `_try_move` already knows `next_pos`. Second, separate experiment: replace the
  random tie-break with something chain-aware, since ties concentrate on shared trunk tiles.
- **Also noted:** `aug7` still calls the old `nearest_cardinal` inside
  `_try_build_conveyor_toward_core` — harmless, since that function is verified dead code, but
  the migration was not total. And one replay reported `win_condition=titanium_stored`, a value
  absent from `tools/replay_schema.md`'s documented set.

### Discard on the pooled number, but the per-map split is the finding — reactive home defense

- **Date:** 2026-08-08 · challenger `bots/ladder1`, primary gate `bots/opp_v44`
- **Hypothesis (pre-registered above):** our defense is scheduled off *our own* economy and never
  off the *enemy's* behaviour, so adopting v44's vision-triggered emergency battery — threat
  detection decoupled from harvester count — should close the gap to v44.
- **Result: 40.6% [36.3%, 45.1%], n=480, 0 crashes either side.** The `aug7` baseline against
  the same opponent is **40.8% [32.5%, 49.8%]**. Statistically indistinguishable. **Discard
  against the primary gate.**
- **And the pooled number is the least informative thing in the run.** The per-map split is
  **violently bimodal**, not flat (`ladder1` wins, out of 32 per map):

  | wins big | | collapses | |
  | --- | --- | --- | --- |
  | antler | **27** | hive | **0** |
  | lighthouse | **22** | atoll | **3** |
  | archipelago | **20** | snowflake | **3** |
  | heart | **20** | jackpot | **6** |
  | moonrise | **19** | drumlin | **7** |
  | | | meander | **9** |

  **A 0-for-32 is structural, not variance.** And `core_destroyed` came in at **120/480 = 25%**
  against this bot's usual **~17%** house rate, so the mechanism is unambiguously *engaging* —
  it is not a null. Something in it is worth a great deal on five maps and catastrophic on six,
  and averaging those into 40.6% describes neither.
- **Leading hypothesis, not yet confirmed:** economy starvation on ore-poor maps. **`atoll` has
  8 ore tiles and `hive` 12 — the two lowest in the 15-map pool** — and both collapsed, while
  ore-rich maps did fine. Diverting a builder or spending on ammo costs proportionally far more
  where there is little ore to work. This converges with the ammo arithmetic logged below:
  sustained defense **requires** delivered income, and where income is thin, defense eats the
  economy that pays for it.
- **Caveat recorded honestly:** the diff runs to ~159 changed lines, which is large for one
  mechanism, and it has not yet been confirmed that a second behaviour did not creep in
  alongside the trigger. If it did, the bimodality is unattributable between them. Diagnosis
  requested; **do not build on this result until that question is answered.**
- **What to do with it:** do **not** average this away. The five maps at 60-84% are a real
  signal. The next move is to find what distinguishes them from the six that collapse — the
  ore-density hypothesis is testable directly — and gate a variant that keeps the mechanism
  where it pays. A map-conditional defense trigger is a legitimate follow-up, but note the
  standing caution that per-map tuning has a **one-week shelf life** on a weekly rotation, so
  prefer a rule keyed to a *measurable map property* (ore count, ore density) over a map list.

### Finding — we out-collected them 4880 to 0 and still lost, to three units we never touched

- **Date:** 2026-08-08 · from a 9-replay batched digest across 6 opponents rated 1323-1965
  (full tables in [opponents.md](opponents.md)); no code change
- **The single most damning game in the archive:** an Albert And Einstein match in which we
  finished **4880 titanium collected to their 0** — total economic dominance — and **lost
  anyway**, to **3 units that were never reinforced, over 985 turns**. Not a rush that
  overwhelmed us. Three static pieces that sat there for the entire game while we had no way to
  remove them.
- **The gap this exposes is not defense, it is "clear the siege".** We can out-economy the top
  of the field and still lose, because `aug7` has **no mechanism that removes an established
  enemy emplacement**. It has no offense at all (no enemy-Core tracking, no movement toward it,
  no `fire()` sabotage, no forward turrets), so once a siege is planted, every remaining round
  is spent accumulating a tiebreak we will never reach. **Building more defense does not fix
  this; only the ability to attack a static target does.** `ct.fire()` from a builder — 2 damage
  for 2 Ti against buildings, orthogonally adjacent — is the cheapest tool we already have and
  have never used.
- **Two attacker archetypes, converged on independently across the top of the field:**
  - **"instant-Sentinel", turn 1-6.** The Launcher-thrown builder **builds the forward Sentinel
    on arrival**, so the opening is **map-size-independent**. Seen in `sporks` (1923) and all
    five AAE games. `sporks` killed a Core in **63 turns** — the fastest in this project's
    history. **This supersedes the turn 4-15 calibration target; the real number is turn 1-6.**
  - **"forward-Gunner", turn 33-39.** A separate, slower lane — `Pivot` (~1907-1965),
    `not adgato` (1897) and `Besvikomat` (1789), **three unrelated opponents converging tightly**.
    Rush defense must cover both windows, not just the early one.
- **Ring-camping is correlated with wins, not causal** — do not over-invest in blocking as a
  mechanism, and note this agrees with the local probe, where the blocker never once decided a
  game.
- **Model correction, flagged loudly:** the Core's **raw** hit-count-to-kill range widens from
  28-136 to **28-1206**, while net HP holds at 500-512. Healing dominates siege arithmetic by up
  to 43×. Now in [game-model.md](game-model.md).

### Telemetry correction — v40's ladder record was much better than we logged

- **Date:** 2026-08-08 · from `fcode match list --mine --json`, fully paginated, 181 matches
  (107 rated + 74 unrated) with per-match `teamAVersion`/`teamBVersion`, `eloDelta`,
  `ratingBefore`
- **Supersedes the earlier entry below that read "v40 played exactly one ladder series."** That
  was an artefact of reconstructing an activation timeline by hand. With real version
  attribution: **v40 ("aug7-sentinel-economy", our line) is 8W-1L, net Elo +35.24 — the
  strongest well-sampled version the team has.** Current team rating **1233.34, rank #50/103**.
- **v44 ("florent-v58") has only 2 rated series, both wins** (+14.34), and is **undefeated on
  the rated ladder**. Everything we know about v44 losing comes from the **unrated** bucket,
  where it is **0W-4L with all 20 games ending `core_destroyed`**.
- **Read carefully, because this cuts against a claim made earlier today.** The local arena says
  `opp_v44` beats `aug7` 59/41 over 120 matches — well powered, and it stands. The ladder
  samples (9 series vs 2) are far too small to contradict it. What they *do* say is that our
  line has not been outperformed on the ladder, and that **v44's only observed losses are to
  the rush archetypes above** — which is exactly the weakness our current lane targets.
- **Method note that earned its keep:** `--mine --json` carries per-match version attribution
  directly. **Never reconstruct an activation timeline by hand again** — doing so produced a
  wrong entry in this log within the same day.

### Measurement — the first rush baseline says 95%, and the number is not the finding

- **Date:** 2026-08-08 · `bots/rush_probe` v1, 240 matches vs `aug7`, 0 crashes either side
- **Headline:** **`aug7` beats `rush_probe` 95.0% [91.5%, 97.1%]**. Control: `starter` beats it
  **93.3%** — while hemorrhaging **221 units** to its own unguarded `is_tile_empty` crash bug.
  An all-in rush loses to a *crashing* economy bot.
- **⚠ Read the direction of these numbers carefully — this one has already been misread once.**
  `arena.py` reports the **first-named bot's** win rate, and the runs were
  `arena.py aug7 rush_probe` and `arena.py starter rush_probe`. So **95.0% and 93.3% are the
  DEFENDER's win rates. The rusher lost both, badly.** Inverted, these numbers read as "the
  meta threat is quantified and severe", which is the opposite of what was measured and would
  send the next session optimising against a threat level nobody has established yet. **The
  meta threat is NOT yet quantified.** What is quantified is that *this* probe — all-in,
  walk-in, ammo-starved — is harmless. A faithful probe does not exist yet.
- **Do not read this as "we are safe from rushes."** A real 1306-rated opponent beat us **0-5,
  all five by `core_destroyed`**. The probe and the ladder disagree, so the probe is wrong, and
  its own diagnostics say exactly how. A cross-tab of *who died* is what made this legible:
  - **rush_probe's own Core died in 22 matches; `aug7`'s in 5.** Going all-in leaves zero home
    defense, and on small maps `aug7`'s purely defensive Sentinels reach far enough to kill it
    (fjordgate 7/8).
  - **On 7 of 15 maps neither Core died in 1000 rounds** — three Sentinels cannot close 500 HP
    even completely unopposed.
  - When it does win it is **100% `core_destroyed`, 0% economic** — Sentinels are the only lever
    that ever wins a rush; the spawn-ring blocker never decides a game.
- **Why three Sentinels stall, and it is the most useful thing here: it is ammo, not damage.**
  A Sentinel firing on its 2-round cooldown burns **5 Ti/round**; three is **~15 Ti/round**
  against **2.5 Ti/round** of passive income. Stripped of economy, the probe can fire about a
  sixth of the time, so its theoretical ~27 dmg/round never arrives.
  **Therefore the real meta is economy-PLUS-rush, not all-in rush.** Albert And Einstein spent
  four builders on a Launcher and turrets *and* still ran enough economy to sustain fire. This
  is a genuine correction to how we framed the threat.
- **Second defect: walk-only delivery under-tests big maps by an order of magnitude.** Measured
  first-Sentinel turn ran **3-4 on fjordgate (10×10)** but **24-56 on drumlin (25×25)**, against
  an observed ladder benchmark of **turn 4-15 regardless of map size** — because the top
  execution throws its own builder 6-8 tiles with a **turn-1 Launcher**.
- **Next:** two probe modes — walked-sentinel (common meta) and launcher-insertion (top meta) —
  **both with enough economy to sustain ammo, and both keeping 1-2 home Sentinels**, since a
  probe that suicides measures its own fragility rather than our defense.
- **Method note worth keeping:** the win rate was the least informative number in this run. The
  who-died cross-tab and the per-map "neither Core died" count are what turned a misleading 95%
  into a specific, fixable list of three defects. When a result contradicts a real-world
  observation, instrument the disagreement rather than believing the cleaner number.

### Intel — a hole in our own team's active bot, on small maps

- **Date:** 2026-08-08 · from the `opp_v44` source read (full addendum in
  [opponents.md](opponents.md) under `florent-v58`)
- v44's emergency-defense battery — the mechanism we are adopting — is **disabled on maps with
  `w * h <= 120`**. **`fjordgate` is 10×10 = 100** and falls below the gate, leaving only a
  slower `harvesters >= 1` fallback to cover it.
- Worth logging twice over: it is a known weakness in the strongest bot on our own team, and it
  will be inherited by **anyone who copies this pattern**. Our own port must **not** replicate
  the gate; `fjordgate` is the per-map row where that difference should show up.

### Hypothesis, pre-registered — defended economy farms a converged-rush field

- **Date:** 2026-08-08 · **written before the measurement exists**, which is the point of writing
  it down. Experiment in flight as `bots/ladder1`; probe in flight as `bots/rush_probe`.
- **The field observation this rests on** (Magnus, from replay watching, high confidence): **the
  sentinel rush is the COMMON ladder opening, including among high-Elo teams.** Not one team's
  quirk. Canonical execution, decoded from series `81d83bb5`: builder turn 0, **Launcher turn 1
  next to their own Core**, own scout thrown 6-8 tiles in one action, camped in our Core's spawn
  ring by turn 6-27, **3-4 Sentinels 1-4 tiles from our Core, first landing turn 4-15**, four
  builders total.
- **Why this changes the evaluation set, not just the strategy.** Our entire local opponent pool
  — `starter`, `opp_v39`, our own lineage — is passive. **Every "early aggression doesn't pay"
  result this project has produced was measured against a field in which nobody ever attacks.**
  Those results are not wrong, but they answered a question about a distribution we do not play
  against. `aug7` vs `rush_probe` is therefore likely **the most ladder-predictive local number
  available**, and it does not exist yet.
- **The claim:** a bot that keeps its economy-first shape but defends *reactively* does not
  merely survive the rush — it **profits** from a field that has converged on it. Three measured
  facts favour the defender, conditional on the defense triggering early enough:
  1. **Healing costs 0.25 Ti/HP** (+4 HP for 1 Ti) against **~0.56 Ti/HP** for any attacker.
     Attrition against a healed target is a losing trade at every level; 2 builders out-heal a
     Gunner, 3 out-heal a Sentinel.
  2. **Sentinels cannot rotate** — facing is fixed at build time. A rush emplacement covers one
     line forever, so approaching off its axis turns 30 Ti of enemy investment into furniture.
  3. Every rush Sentinel costs the attacker **+20% cost scale permanently**, and scale never
     decays. A failed rush is not a neutral trade; it is a tax on everything they build after.
  So the rusher's investment is front-loaded, irreversible, and cheap to blunt — while ours is
  an economy that keeps compounding.
- **Our actual defect, and it is not "too little defense":** defense is scheduled off *our*
  economy and never off the *enemy's* behaviour. `_try_build_sentinel` is gated on 3 harvesters
  **and** on a builder happening to be within dist²≤18 of the Core. In the decoded series our
  first Sentinel landed at **turn 436** and **turn 81** with the harvester gate met at turn
  22-28, and one game never met the gate at all — zero defense, 28 unmitigated hits.
- **The change being tested:** reactive home defense — defend immediately when an enemy is
  visible near our Core, regardless of harvester count. **Purely additive by construction.**
- **Predictions, stated now:** a **no-op (~50%) against the passive pool**, because nobody
  approaches our Core early there; a **material gain against `rush_probe` and `opp_v44`**. If
  both halves hold, the change is not a patch on a weakness — it is a counter to the median
  opponent. **If the passive-pool half comes back materially negative, the change is not
  additive and the implementation is wrong, not the hypothesis.**
- **Accept rule for this lane:** clear the normal Wilson gate against `opp_v44`, **and**
  materially improve against `rush_probe`, **and** not collapse against `starter`/`opp_v39` —
  we still climb through a mostly passive field and must not overfit to rushers.

### Finding — we sometimes deliver exactly zero titanium on maps with no (0,0) Core, and nobody has explained it

- **Date:** 2026-08-08 · two independent observations converging, no code change yet
- **The observation:** `titanium_collected` comes out at **exactly 0** in games where the
  economy visibly exists. This is the same signature as the jackpot (0,0) Core bug — but on
  maps with no Core at the origin, so it is a **different, unexplained failure**.
  1. **From a ladder replay** (`81d83bb5`, vs Albert And Einstein, our own v40): games 1
     (`heart`) and 4 (`hive`) finished **0 collected for both sides**, while game 1 had
     **5 harvesters and 99 conveyors** built. Resource movement *did* occur — 33 and 12
     `distributeResources` events — so stacks were flowing and never arriving. The analyst
     specifically ruled out the enemy blocker denying our delivery tiles: we built conveyors on
     every Core-adjacent delivery tile, early, in every game, with no enemy builder on those
     tiles at build time.
  2. **From local instrumentation**, independently: on `heart`, **3 of 5** `aug7`-vs-`aug7`
     matches ended with **both sides at exactly 0 collected**, decided on the harvester
     tiebreak. `heart` was already one of the four unexplained seat-asymmetry maps and was
     flagged as "a different phenomenon" before the replay evidence existed.
- **Why this matters more than it looks:** crediting is delivery-only (measured, game-model.md),
  **78% of our games are decided on the titanium tiebreak**, and this failure mode zeroes the
  scoring quantity outright. It is not a small inefficiency — it is the economy not existing.
  A trail conveyor whose output side faces *into* the harvester will refuse that harvester's
  stack, and a chain that dead-ends carries stacks that are never credited; both were logged as
  residual unmeasured questions in the 2026-08-07 conveyor work, and this is what they look like
  when they bite.
- **Why it has stayed hidden:** it is invisible in a win rate — when *both* sides zero out, the
  game still resolves on a tiebreak and the pooled number moves by nothing.
- **Next, and this is the highest-value diagnostic left:** instrument whether a given
  harvester's stack ever reaches the Core, per match, per map — the open question
  "do the conveyor chains our builders lay actually complete a path to the Core?" has been open
  since 2026-08-07 and now has two independent pieces of evidence that the answer is sometimes
  no. `heart` is the map to run it on, because it fails ~60% of the time there.

### Intel — the launcher-assisted rush, and what actually kills us

- **Date:** 2026-08-08 · full decode of ladder series `81d83bb5`, all 5 games, no code change
- **The series:** Albert And Einstein (**1306.8**) vs OpenSverige (**1222.8**), **0-5**, ELO
  −12.21. **All five games ended `core_destroyed`.** In every game with a non-zero economy
  reading, **we out-collected them** — and lost anyway.
- **Their opening, identical turn-for-turn in all five games:** Builder Bot turn 0 → **Launcher
  turn 1, next to their own Core** → their own scout builder thrown **6-8 tiles in a single
  action** → that builder walks in and is **camped inside our Core's spawn ring by turn 6-27**,
  where it stays for **57-98% of the game**. Then **3-4 Sentinels built 1-4 tiles from our
  Core**, from turn 4-15. Total investment: exactly **4 builders**, spawned turns 0-3.
- **Verdict — the sentinels kill us, not the blocker.** 5 of 5 `core_destroyed`, 0 of 5 on any
  economy tiebreak; the Core always died first, so the blocker never got to decide anything.
  Net HP to kill our Core was 502-512 every game.
- **But the blocker is not free for us either, and the mechanism is worth naming.** Our defense
  gate (3 harvesters) was met around turn 22-28 in games 1 and 2, yet our first Sentinel did not
  land until **turn 436** and **turn 81** respectively — against near-instant responses in the
  games where ring occupancy was lower. Game 4 never met the gate at all (stuck on 1 harvester,
  zero defense, 28 unmitigated hits). Whether that is the blocker tying up our builders or our
  own build order deprioritising turrets **is not separable from this data** — it is a question,
  not a conclusion.
- **Two model corrections fell out of the decode**, both now in game-model.md:
  - **The Launcher is a rush-delivery tool**, and a large map no longer buys time. We knew
    Launchers throw builders; we had never seen one used to deliver a rush on turn 1.
  - **"28 hits of −18 kills a Core" is only true when nobody heals.** Our builders *do* heal the
    Core (+4 HP for 1 Ti, exactly as documented), offsetting **4-79%** of incoming damage; raw
    hit counts ran **28 to 136**. Only the net ~504 held constant. That is real active defense
    our bot already performs and which nothing in our own docs had noticed.
- **Read:** every "early aggression doesn't pay" result this project has ever produced was
  measured against `starter`, `opp_v39` and our own lineage — **a pool in which nobody ever
  rushes**. The 1300+ band does. That is a structural blind spot in the evaluation set, not a
  strategic conclusion, and it is why `bots/rush_probe` now exists.

### Telemetry — v40's ladder window, and the bar moving out from under us

- **Date:** 2026-08-08 · platform reads only, no code change
- **v40 ("aug7-sentinel-economy", `a9d81a1`) — the whole ladder record it ever produced:**
  rating **1182 → ~1222**, ending its window at roughly **104 matches played / ~1214 rating**,
  rank around **#52-53 of 103**, crossing from Unranked into **Bronze**. Then x3r0 activated
  **v44 ("florent-v58") at ~13:00**, so **every ladder result after that measures their bot,
  not ours.** Attribute segments accordingly; do not read the team's later trajectory as
  evidence about `aug7`.
  **Exact slot timeline** (it flipped twice, so segment carefully): v40 active until ~13:00 →
  **v44** from ~13:00 → v40 briefly re-activated for roughly **one series** (around match ~105,
  rating ~1221) → **v44** again from ~15:15, after the 59/41 head-to-head was confirmed.
  A 13:16 UTC snapshot during that window read rating **1221.23**, rank **#50 of 103**, 105
  matches, last-10 5W-5L. **Standing team norm from here: the active slot follows arena
  measurement** — a candidate that beats `opp_v44` takes the slot, with the numbers attached.
- **The sample is thinner than the match count suggests.** The team ran **42 submission
  versions in ~16 hours** across several people, and **v40 played exactly one ladder series**
  (`1018bf11`, a 3-2 win over Leviathan). The 97-match history is mostly other people's bots.
  A per-replay observation is only evidence about the version that played it — a lesson that
  cost us a wrong conclusion this session (see the opponents.md correction).
- **Trust `fcode match list`, not `fcode status`'s "Last 10".** Status reported 3W-7L;
  reconstructing the real last ten series three independent ways gives **6W-4L** every time,
  while the `rating` field in the same response is current.
- **Where we actually lose: fights.** Across 485 games, **`core_destroyed` is 15W-74L (17%)**
  against **51% on the titanium tiebreak**. Against `1337` it is **0W-17L** on Core kills over
  17 games, with kills landing anywhere from turn 188 to 737 — sustained pressure, not a rush.
  Worst map on the current rotation: **`saga` 2W-8L**.
- **What the top of the ladder builds.** Unrated scouting replay `91d77721` against **Pivot**
  (#1, ~1947): **12 harvesters, 39 conveyors, 17 Gunners, zero Sentinels**, out-collecting us
  **3170 to 810**. Our bot switches builders to defense at `TARGET_HARVESTERS = 3` and then
  builds Sentinels with no cap — a local probe counted **116 sentinels across 10 matches, 66 in
  one**, at +20% cost scale each. **We are running roughly a quarter of the winning economy and
  spending the difference on fights we lose 17% of.**
- **And the bar moved.** Our own teammate's active bot, `opp_v44`, **beats `aug7` — 40.8%
  [32.5%, 49.8%] over 120 matches**, 0 crashes both sides, **38 `core_destroyed`**. Its version
  names ("ammo-gunner", "gunners-before", "gunner-deadzone") say the line is **Gunner-focused**,
  which sits directly against our own measured Sentinel-first result (68.4% [62.4%, 73.7%]).
  That result was obtained against a **passive** opponent pool; v44 was evolved against live
  ladder opponents. **`opp_v44` is therefore the primary confirm opponent from here on** — a
  keep must clear the Wilson gate against it, with `aug7` retained for lineage attribution and
  `starter`/`opp_v39` as no-collapse checks.
- **Read:** the honest summary of this session's ladder position is that our accepted local
  improvements are real and measured, and simultaneously our bot is no longer the strongest bot
  on our own team. The single largest gap is not a bug — it is that we cap economy at 3
  harvesters and cannot win a Core fight.

### Discard — wall-aware BFS pathfinding, and it is worst exactly where it should have been best

- **Date:** 2026-08-08 · challenger `bots/ladder1`, baseline `bots/aug7` at `3cfa588`
- **Hypothesis:** the incumbent walks greedily — a productive cardinal at random, then the
  perpendiculars, then the reverse, giving up on a target after 3 stuck rounds. In a concave
  wall pocket that wanders. The rotation has five maps at ≥19% wall density (archipelago 30.8%,
  saga 28.5%, lighthouse 25.0%, heart 21.8%, jackpot 19.5%) and they are among our weakest.
  **Predicted: the walliest maps gain most, the near-empty ones (drumlin 0.6%, meander 2.1%,
  eider 3.9%) stay flat.**
- **Change:** bounded BFS over a per-unit memo of **walls only** (buildings excluded, since they
  come and go; never-seen tiles optimistically passable), node cap 200 counted on expansions,
  path cached and recomputed only when absent / target changed / consumed, neighbour order
  shuffled at every expansion, and the incumbent's greedy walker retained as the fallback when
  BFS exhausts its budget. `_try_move` still performs the step, so trail-laying is unchanged.
- **CPU:** profiled with `time.process_time()` over ~55,000 builder-rounds — p50 71 µs, p99
  1398 µs, **worst case 3785 µs** against the 8000 µs guard. (Node cap 300 measured 5813 µs and
  was rejected as too tight.) Comfortably affordable; CPU was not the problem.
- **Result:** screen 45.6% [35.7%, 55.8%] (n=90). **Confirm 45.8% [41.4%, 50.3%] (n=480) — no
  verdict, therefore discard.** 0 crashes both sides.
- **Read — the prediction did not merely fail, it inverted.** On the five walliest maps the
  challenger scored **57/160 = 35.6%**; on the other ten, **163/320 = 50.9%**, a dead heat. Its
  three worst maps in the whole run are **archipelago 11/32, lighthouse 8/32, saga 10/32** — the
  three walliest. A change that is neutral everywhere and specifically bad on exactly the maps
  it targeted is not noise; it is a mechanism pointing the other way.
  The best-supported explanation is that **the greedy walker's meandering is exploration, and
  the shortest path is not.** Target selection is unchanged and picks the nearest *visible*
  ore, so what a builder sees determines what it can go build. Detouring around a wall sweeps
  vision across ground a straight line never touches, and it lays trail conveyor over a wider
  footprint. On wally maps the detours are longest — which is exactly where the BFS bot gives up
  the most incidental discovery. Consistent with the development measurement that the BFS build
  produced *more* buildings (94.5 vs 76.7) yet still lost: it was building more efficiently in a
  smaller explored region.
- **Next:** do not retry shortest-path movement as a movement change. If it is retried at all it
  has to come with a **separate** exploration mechanism (systematic frontier targeting rather
  than nearest-visible-ore plus random walk), and that is a `_pick_target` experiment, not a
  `_move_toward_target` one. Kept in `bots/_dev_bfs` and portable.

### Finding — seat A acts first for every unit, and on contested-ore maps that is worth 2.3× the harvesters

- **Date:** 2026-08-08 · instrumented diagnosis, `bots/_diag_seat`, 30 matches, no code change
- **Question:** four maps show large seat asymmetries with identical bots on both sides —
  archipelago ~77-88% for seat A, atoll ~21-31%, heart ~31%, lighthouse ~28%. None is the (0,0)
  Core bug and the NW-corner-reference hypothesis was already refuted.
- **First result, and it reframed the search:** all four are decided on **economy**, never on
  Core kills, and never on unit attrition — the losing seat often has *more* units alive.
- **archipelago is explained.** Engine unit IDs show **team A's Nth builder always has an ID
  exactly one less than team B's Nth** — zero exceptions over 10 instrumented matches on two
  maps. Units run in spawn order, so **seat A resolves first in every round of the match**. On
  archipelago 16% of the 38 ore tiles sit in the contested band near the midline; a Harvester
  blocks movement; so seat A wins each same-round race for a contested tile and then physically
  walls seat B out of it while retargeting deeper ore. Measured: **62 harvesters for A against
  27 for B (2.3×)**, **10 of A's built on B's side of the midline**, B crossing **zero** times,
  and a 1.9× collected-titanium gap that the harvester ratio accounts for. Both sides find ore
  through `_pick_target` at ~99%, and B actually reaches its *first* harvester sooner — so this
  is not a vision or targeting difference. It is the compounding of contested-tile races.
- **The other three, honestly:** `atoll` has only 8 ore tiles with 50% contested, and lands in a
  near-tie decided by the harvester tiebreak — consistent. `lighthouse` has **0% contested ore**,
  harvesters come out 8-7, and seat B still wins both instrumented matches *despite* worse
  movement metrics on every axis (more stuck events, more move failures, 20× more
  random-exploration fallback). **Unresolved** — the likely axis is trail *completion* rather
  than harvester count, which nobody has ever instrumented. `heart` is stranger still: 3 of 5
  matches ended with **both sides at exactly 0 collected**, decided on the harvester tiebreak.
  **Unresolved, and a different phenomenon.**
- **Also refuted along the way:** the sentinel far-vs-near targeting bias was a tempting
  secondary explanation (atoll: seat A 75% far-class facings vs seat B 80% near-class). It is
  not driving this. Across **625 captured sentinel-fire events, zero were suboptimal** — rays
  essentially never held 2+ enemies at once. Lighthouse settles it outright: seat A had the
  *good* facing profile there and lost anyway.
- **Read:** this upgrades a fact in game-model.md rather than adding a bug to fix. The seat-A
  edge was recorded as "an advantage on very small maps"; it is really **an advantage
  proportional to how much ore is contested**, and small maps were a proxy for that. The
  bot-side lever, if there is one, is contesting the midline earlier instead of accepting the
  split — which is an economy-expansion question, not a fairness bug.

### ACCEPT — conveyor facing by dominant axis: 57.9%, and the reason it won is not the reason we tried it

- **Date:** 2026-08-08 · challenger `bots/ladder1`, baseline `bots/_incumbent` = `a9d81a1`.
  **Promoted into `bots/aug7`.**
- **Hypothesis, stated before measuring:** `nearest_cardinal()`'s diagonal table (NE→N, SE→E,
  SW→S, NW→W) is a **chirality rule** — each diagonal snaps to its clockwise-preceding cardinal
  — so it survives a 180° rotation and **inverts under both mirrors, on all four diagonals**.
  Six of the fifteen maps in the rotation are mirrors, which no previous audit exercised
  because the old invented pool was all-rotational. Its one live call site is the trail
  conveyor's facing in `_try_move`, and that trail is the only thing that ever delivers our
  titanium. **Predicted effect: the six mirror maps' seat splits move toward 50%.**
- **Change (one):** a new `cardinal_toward(src, dst)` picks the cardinal by comparing `|dx|`
  and `|dy|` on the real delta, breaking an exact-diagonal tie at random. `nearest_cardinal`
  and the dead `_try_build_conveyor_toward_core` left untouched, for attribution.
- **Results:** screen 53.3% [43.1%, 63.3%] (n=90). **Confirm 57.9% [53.5%, 62.3%] (n=480) —
  the lower bound clears 50%, so this is an accept.** Regression vs `opp_v39` 65.8%
  [59.6%, 71.5%] (n=240), above the `aug7` reference of 65.0% [57.8%, 71.6%]. **0 crashes for
  the challenger across all 1,004 matches.**
- **And the hypothesis was wrong.** Two independent reads say so:
  - The mirror-map self-play diagnostic (192 matches) is **mixed, not a repair**: antler
    31.2%→40.6% and eider 43.8%→53.1% improved, moonrise barely moved, but **meander
    56.2%→37.5% and heart 43.8%→21.9% got worse**, and heart is now the only mirror map the
    harness flags as seat-decided.
  - In the confirm, the split that mattered went the wrong way: the challenger took
    **176/288 = 61.1%** on the nine **rotational** maps against **102/192 = 53.1%** on the six
    **mirror** maps. If mirror-equivariance were the mechanism, that ordering would be
    reversed.
- **Read:** what actually paid is the part of the change nobody was arguing about. Snapping an
  already-quantised 8-way `Direction` throws away the magnitudes — a delta of (−2, −3) is
  mostly north, but it lands in the NORTHWEST sector and the table sent it WEST. Comparing
  `|dx|` and `|dy|` just points the trail at the Core, and that pays wherever trails are long
  and terrain is awkward: the biggest per-map gains are **archipelago 24/32 (30.8% walls),
  snowflake 24/32, saga 23/32 (28.5% walls)**. The equivariance argument was the reason we
  looked at the function; it was not the reason the change won. **Both facts are worth keeping:
  a correct hypothesis is not required for a correct change, but reporting the win without the
  refuted mechanism would leave the next session tuning the wrong lever.**
- **Next:** the mirror asymmetry itself is therefore **still unfixed and still real**, and heart
  is now the sharpest example of it. Do not treat this accept as having closed queue item 2.

### No-verdict, escalated not discarded — the (0,0) Core store fix repairs the map and the gate can't see it

- **Date:** 2026-08-08 · challenger `bots/ladder1`, baseline `bots/_incumbent` = `a9d81a1`
- **Hypothesis, stated before measuring:** publishing the Core's position with a +1 offset so
  that store slot 0 keeps meaning "unwritten" will restore delivery for a team whose Core sits
  at (0,0), repairing `jackpot` from a guaranteed seat-A loss to a fair map. **Predicted pooled
  effect: about +1.7 points** — a full repair of one map out of fifteen moves that map from
  ~50% to ~75% head-to-head (we win it outright in the seat the incumbent throws away, and play
  it evenly in the other), which is 25 points on 1/15 of the pool. **That is below what a
  480-match confirm can resolve, and it was written down before the run.**
- **Change (one, minimal):** `_run_core` writes `pos.x + 1` / `pos.y + 1`; `_read_core_pos`
  requires `x > 0 and y > 0` and subtracts the offset. Comments rewritten to explain the trap.
  Nothing else in the file touched.
- **Results:**

  | run | n | result |
  | --- | --- | --- |
  | mechanism, 6 single matches on jackpot | 6 | team A `titanium_collected` **0/0/0/0/0/0 → 4970 / 2480 / 4970 / 4960 / 2480 / 4970** |
  | jackpot mirror seat split | 48 | **0/48 = 0.0% [0%, 7%] → 22/48 = 45.8% [33%, 60%]** |
  | screen vs incumbent | 90 | 56.7% [46.4%, 66.4%] — survived |
  | **confirm vs incumbent** | **480** | **51.5% [47.0%, 55.9%] — no verdict** |
  | regression vs `opp_v39` | 240 | 62.5% [56.2%, 68.4%], clears 50%; reference `aug7` 65.0% [57.8%, 71.6%] — overlapping, no regression |

  0 crashes for the challenger in every run (opp_v39: 382). Confirm per-map: **jackpot is the
  challenger's best map at 25/32 = 78.1%**, the only map that moved, and **no map regressed**.
- **Verdict under the standing rule: no verdict, therefore not promoted.** The incumbent stays
  `bots/aug7` at `a9d81a1`. The change is preserved at `bots/_fix_core00/` rather than deleted.
- **Why it is being escalated instead of dropped on the floor.** Everything the accept rule was
  built to reject is absent here, and everything it was built to protect is satisfied:
  - The a-priori prediction was **+1.7 points**; the measurement came back **+1.5**. This is not
    a change that "looked good and shrank" — it landed on its stated number.
  - The mechanism was measured directly rather than inferred from the win rate: a team's
    `titanium_collected` moved from **exactly zero** to normal, and the map's mirror seat split
    moved from 0/48 to 45.8%. Those are p-values in the 1e-14 range, not coin flips.
  - The pooled gate is simply the wrong instrument for a defect confined to 1 map in 15. It is
    not that the evidence is weak; it is that 480 matches over 15 maps cannot resolve two
    points, and no achievable sample would — halving the interval needs ~2000 matches, and it
    would still straddle 50%.
  - This project has already made this call once, deliberately: **v2's CPU guard was kept on a
    no-verdict** (`results.tsv`: *"no-verdict as predicted for an inert-locally change; kept as
    ladder insurance"*), and [HANDOVER.md](../HANDOVER.md) states the rule outright — *the
    accept gate is for strategy changes, not insurance changes*. A guard against a measured
    total-failure mode is the same category.
  Promoting it is nonetheless a human decision, not the loop's: it changes the submission
  candidate. **Recommended: apply.** Whether the pooled gate should be extended with an explicit
  per-map correctness clause is a program.md question for Magnus.
- **What the confirm's per-map table also says:** with the (0,0) bug removed, `jackpot`'s seat
  split is *still* skewed (28.1% seat A) because the **incumbent** on the other side is still
  broken there — which is the correct signature, and a reminder that a head-to-head seat column
  measures both bots at once. The maps still flagged with both bots healthy — archipelago 78%,
  atoll 28%, heart 31%, lighthouse 28%, fjordgate 75% — are **untouched by this fix** and are
  the open work.

### Finding — a Core at (0,0) is invisible to its own builders, and it costs the whole map

- **Date:** 2026-08-08 · found by chasing the `jackpot` seat wipeout; the first hypothesis was
  wrong and the measurement that refuted it is what pointed at the real one
- **The claim:** on `jackpot`, whose team-A Core sits at **(0, 0)**, team A delivers
  **exactly zero titanium for the entire match**, every match, in every bot we have. Not
  "less" — zero.
- **The evidence, in the order it arrived:**
  1. Mirror audit: seat A **0/16** on jackpot (see the audit entry below). Repeated in a
     second run at 0/8, and again at 0/48 — **0 for 104** in total, across three different
     bot generations (`aug7`, `probe_neutral`, and a modified `aug7`).
  2. `probe_neutral` — v1 with every absolute-direction bias removed, a different code
     generation — reproduces it exactly (0/32), and **all 32 games ended on
     `titanium_collected`**. So the deficit is economic, and it is not aug7-specific.
  3. Six single matches, `aug7` vs `aug7` on jackpot, reading the end-of-match JSON:
     `a_titanium_collected` = **0, 0, 0, 0, 0, 0**, against `b_titanium_collected` ≈ 4950.
     Team A ends with 4–8 buildings against team B's 39–96, and a final balance of ~2500 —
     which is 500 starting titanium plus 1000 rounds of passive income, i.e. team A spent
     almost nothing all game because it never earned anything.
- **The mechanism, and it is three lines of code:**
  ```python
  ct.write_store(SLOT_CORE_X, pos.x)          # the Core publishes 0 and 0
  ...
  if x > 0 or y > 0:                          # ...and no builder ever believes it
      self.core_pos = Position(x, y)
  ```
  All 16 comms slots start at 0 and hold non-negative integers, so **0 is indistinguishable
  from "nobody has written this yet"**. A Core at the origin publishes its position and every
  builder on that team reads it as no-data, for the whole match. Three things are gated on
  `core_pos is not None`: laying the trail conveyor in `_try_move` — **which is the only thing
  that ever delivers our titanium** (the dedicated harvester conveyor is verified dead code,
  see the entry below) — building sentinels, and heading home in `_pick_target`. Team A
  therefore builds harvesters that idle with nowhere to output, lays no conveyors, builds no
  sentinels, and collects nothing. The existing comment even flags the ambiguity and resolves
  it the wrong way: *"we skip storing (0, 0) unless the core really is there"* — the one case
  it doesn't handle is the Core really being there.
- **The whole field has this bug.** It is inherited verbatim from the organisers' shipped
  starter bot (`bots/starter/main.py:230`). Measured directly: `starter` vs `starter` on
  jackpot, seat A finishes with `titanium_collected` **0**, `units` **0**, `buildings` **1** —
  the bare Core. See [opponents.md](opponents.md); this is exploitable metagame information,
  not just our own bug.
- **The hypothesis this replaced, and why the refutation was worth its CPU.** The first
  candidate was that `get_position()` returns the 2×2 footprint's **NW corner**, which is not
  a rotation-equivariant reference point — the centre sits half a tile SE, so every
  core-relative gate is displaced by a fixed offset that does not rotate with the map. On
  jackpot the arithmetic looked damning: 5 legal tiles inside the return-home gate for seat A
  against 12 for seat B, ~11 sentinel sites against ~30. It was wrong. A build with both gates
  measured to the footprint centre instead (`bots/_diag_core`, integer-exact in doubled
  coordinates) moved **nothing**: jackpot 0/48 (unchanged), archipelago 72.9% vs 77.1%, atoll
  20.8% vs 31.2%, fjordgate 64.6% vs 66.7% — all within noise of the incumbent. Plausible
  arithmetic about a real asymmetry, and the asymmetry simply wasn't binding. The refutation
  is what forced the question "why is *collected* exactly zero rather than merely lower",
  which is the question that has only one answer.
- **What this does not explain.** `archipelago` (seat A 77%) and `atoll` (seat A 21%) are
  still unexplained and are **not** this bug — neither has a Core at the origin. They are the
  next thing to chase, and they are worth more in aggregate than jackpot was.
- **Method note:** the win rate could never have found this. A pooled metric over 15 maps
  shows a total wipeout on one of them as a couple of points of drag. The instruments that
  found it were the **per-map mirror seat table** and the **end-of-match JSON's per-team
  `titanium_collected`** — a process metric, not an outcome metric. When an outcome is
  extreme and stable (0 for 104), stop running more matches and go read the state.

### Measurement — mirror seat audit of the real rotation: one map is a 0/16 wipeout, and it is ours

- **Date:** 2026-08-08 · measurement only, **no code change**, no accept/discard
- **Why:** the per-map seat split of a bot against *itself* is this project's standing
  regression test for orientation bias (strategy-notes.md). Every previous audit ran on the
  eight invented maps, which were all rotational and mostly small. The pool has since cut over
  to the real 15-map competition rotation, so the test had to be re-run on the distribution we
  are actually graded on. A second motive: an earlier non-mirror run had flagged `jackpot`
  (~8% seat A), `heart` (~83%) and `atoll` (~17%), but that data was contaminated — the two
  sides were different bots, so a seat split and a strength difference are not separable.
  A mirror run separates them by construction.
- **Setup:** `arena.py aug7 aug7 --seeds 8 --jobs 8` — 15 maps × 8 seeds × 2 orderings =
  **240 matches**, identical code on both sides. Under a fair map and an orientation-neutral
  bot every row should sit near 50%.
- **Result — pooled:** seat A **124/240 = 51.7%** [45.4%, 58.0%]. **0 crashes.** Win
  conditions: `titanium_collected` 188 (78.3%), `core_destroyed` 40 (**16.7%**), `harvesters`
  7, `titanium_stored` 5. The harness reads a no-op as a coin flip, so the sanity check passes;
  and the `core_destroyed` rate reproduces the invented pool's null-control 16.7% **exactly**,
  which is a useful invariant — the Core-kill rate is a property of this bot, not of the pool.
- **Result — per map** (seat A share, Wilson 95%):

  | map | seat A | flag |
  | --- | --- | --- |
  | **jackpot** | **0/16 = 0.0%** [0%, 19%] | **decisive** (two-sided p = 3.1e-5; survives Bonferroni over 15 maps, p_adj = 4.6e-4) |
  | archipelago | 14/16 = 87.5% [64%, 97%] | suggestive (p = 4.2e-3, p_adj = 0.063) |
  | fjordgate | 12/16 = 75.0% [51%, 90%] | nominal only (p = 0.077, p_adj = 1.0) |
  | atoll | 4/16 = 25.0% [10%, 49%] | nominal only (p = 0.077, p_adj = 1.0) |
  | antler | 5/16 = 31.2% | not flagged |
  | heart | 7/16 = 43.8% | not flagged |
  | the other 9 | 8–11/16 | not flagged |

  Fifteen simultaneous 95% intervals produce ~0.75 false flags by chance, so read the p-values,
  not the flag column. Only `jackpot` is decisive; `archipelago` is worth a look; `fjordgate`
  and `atoll` are what a 15-map audit looks like when nothing is wrong.
- **Verdict on the contaminated flags:** `jackpot` **confirmed and worse than reported** (~8%
  → 0%). `atoll` confirmed in direction only, and not significant once you count the
  comparisons. `heart` (~83%) is **refuted** — 43.8% [23%, 67%], no detectable seat effect.
  That is the value of the mirror design: one of three "findings" was an artefact of comparing
  two different bots.
- **Read:** `jackpot` is 16×16 and **tile-grid-exact 180° rotationally symmetric** (verified by
  parsing the `.map26`; cores A=(0,0), B=(14,14), footprints map onto each other exactly under
  the rotation). A fair map plus identical bots plus 0/16 leaves only one conclusion:
  **the bot handicaps itself in seat A.** This is not an engine effect — the known engine
  first-mover edge favours seat A, and this is the opposite sign. It is the same bug class the
  v3/v4 work was built to kill, surviving in a place that audit never reached, because the
  invented pool had no corner Core.
  The leading mechanism, from reading the code rather than from measurement: the Core publishes
  `ct.get_position()`, the footprint's **NW corner tile**, and every builder treats that single
  tile as "where the Core is". The footprint's centre is at corner + (0.5, 0.5), so the corner
  carries a fixed (−0.5, −0.5) offset **that does not rotate with the map**. On jackpot it
  points off-map for seat A and into open ground for seat B. Hand-counting the two gates that
  consume it: tiles at d²≤8 (the return-home gate) number **5** for seat A against **12** for
  seat B; at d²≤18 (the sentinel-build gate) roughly **11** against **30**. Seat A's builders
  are being told to crowd into less than half the space and have a third of the legal turret
  sites.
- **Next:** diagnosed separately before any fix is gated (see the corner-Core entry). Note the
  size of the prize is bounded: jackpot is 1/15 of the pool, so even a perfect repair is worth
  ~2 points of pooled win rate — below what a 480-match confirm can resolve. The per-map seat
  table, not the pooled win rate, is the instrument that can see this class of bug, and that is
  an argument for running this audit every time the rotation changes.

### Diagnostic — aug7 on the real map rotation: 69.6%, not 80.5%, and still crash-free

- **Date:** 2026-08-07 · diagnostic only, **not** an accept/discard run and not a metric change
- **Why:** the real rotation landed in `maps/new-maps/` (f71614e) mid-session, while the
  parallel experiments were already running on the eight invented maps. Cutover is a
  between-tags operation ([runbook.md](runbook.md) §2), so the right move was to leave the
  metric alone and measure the gap explicitly rather than guess at it.
- **Setup:** `arena.py aug7 starter --maps maps/new-maps/*.map26 --seeds 8 --jobs 8`, n=224.
  Passing explicit paths means no protected file was touched and the standing metric is
  unchanged.
- **Result:** **69.6% [63.3%, 75.3%]** vs the invented pool's **80.5% [75.2%, 84.9%]** —
  intervals barely overlap, so the edge is genuine but roughly 11 points thinner than our
  headline. **0 crashes in 224 matches** (starter: 355), including `jackpot`'s literal corner
  Core and the five maps at ≥14% wall density. Weakest: `hive` 6/16, `archipelago` 8/16,
  `atoll`/`jackpot` 9/16. An earlier n=56 pass read 57.1%; that was noise, use n=224.
- **Read:** the two things this lineage was actually built on — crash-freedom and
  direction-neutrality — **transfer to the real distribution intact**, which is the outcome
  that mattered most and was genuinely in doubt (a corner Core is exactly the case the
  full-ring spawn scan was written for). What does not transfer is the size of the margin: a
  meaningful part of our 80.5% was earned against maps we invented, on which starter's
  weaknesses are presumably over-exposed. Treat 69.6% as the honest pre-ladder expectation.
- **Next:** re-baseline properly after cutover, and re-run the aimed-sentinel experiment
  specifically — a Sentinel's wall-ignoring line is worth much more at 30.8% wall density than
  at our inventions', so that null was arguably answered on the wrong distribution. Per-map
  tuning has a one-week shelf life given the weekly rotation; robust-across-maps changes keep
  their priority permanently.

### Finding — the harvester's first conveyor has never been built, in any version, ever

- **Date:** 2026-08-07 · found as a side-observation while discarding the conveyor-chain
  experiment; verified independently before being believed
- **The claim:** `_try_build_conveyor_toward_core` — the function that gives each newly built
  harvester its output conveyor toward the Core — is **dead code**, and has been since the
  organisers' shipped starter bot. The identical line is in `bots/starter/main.py:286`,
  `bots/v4/main.py:375` and `bots/aug7/main.py:379`, i.e. the entire lineage.
- **Verification:** instrumented copy (`bots/_probe_conv`), single matches across mid20,
  large30, hsym16, duel16. **24 calls, 0 legal, 0 conveyors built.** Target tile was the
  builder's own tile 18 times (`dist_sq=0`), diagonal or 2 steps away the other 6.
- **Cause — a grid-parity fact worth remembering:** `can_build_conveyor(pos, facing)` requires
  `pos` to be orthogonally adjacent to **the acting builder**, not to the harvester. The
  builder stands orthogonally adjacent to the harvester `H` (build requires that), and the
  code targets another orthogonal neighbour of `H`. The grid graph is bipartite, so **two
  tiles one step apart share no common orthogonal neighbour**: the target is either the
  builder's own tile (explicitly disallowed) or not adjacent to the builder. Always illegal.
  Generalised: **a builder adjacent to a building it just placed can never build anything
  orthogonally touching that building — it must move first.** This constrains every
  build-adjacent-to-a-building idea we might have, not just this one.
- **Why it has not hurt us — measured, not assumed.** `_try_move` lays a conveyor on the tile
  *ahead* before stepping onto it, so a builder is usually standing on a conveyor, and its own
  tile *is* orthogonally adjacent to the harvester it then builds. Instrumented across all 8
  maps, 3–4 seeds each, 30 matches: **264 harvesters built, 263 (99.6%) had an orthogonally
  adjacent friendly conveyor**, 233 of them by the earliest measurable round (the round after
  the build). One miss, on duel16. 0 lost, 0 unresolved.
- **Conclusion: do not fix it.** The bug is real, permanently non-firing, and completely
  masked. Deleting or repairing the function would change nothing measurable, and a change
  that cannot move the metric is not worth the risk of touching the submission candidate.
  This is the rare case where the correct action on a verified bug is to write it down and
  walk away.
- **Residual, unmeasured:** adjacency is necessary but not *sufficient* for delivery — a
  conveyor whose output side faces into the harvester won't accept from it. The probe measured
  presence, not accept-side correctness. Trail conveyors face toward the Core and harvesters
  round-robin across neighbours, so this is unlikely to bite, but it is a distinct question
  if anyone pushes further.
- **Note on the field:** anyone who started from the organisers' starter bot has inherited
  this same dead function. See [opponents.md](opponents.md).

### Discard — aimed sentinel placement is a perfect null, and the null is the finding

- **Date:** 2026-08-07 · tested against sentinel-first aug7 (fc53345 working tree), parallel
  session (`bots/aug7_h*`, `--jobs 3`)
- **Hypothesis:** a sentinel is 30 Ti + a 20% scale tax — the most expensive irreversible
  decision the bot makes — and its whole value is *(position, facing)*, since it fires an
  unblockable line. The incumbent takes the first legal adjacent tile and faces
  `direction_to(core).opposite()`, i.e. the builder's incidental standing position picks the
  arc. `can_fire_from()` / `get_attackable_tiles_from()` exist precisely to evaluate a
  placement before paying for it, and nothing in the tutorials or our lineage uses them.
- **Change:** score all legal (≤4 adjacent tiles × 8 facings) pairs and build the best.
  Score per covered tile = proximity to our Core + alignment with the corridor toward the
  inferred enemy Core (point-reflection of our Core through the map centre), with tiles
  already inside an existing friendly sentinel's arc down-weighted to 0.4. Ties broken by
  shuffled iteration. `_run_sentinel` targeting deliberately left unchanged.
- **Result:** screen **56.2% [42.3%, 69.3%]** (n=48) — survived, leaning positive. Confirm
  **50.0% [43.9%, 56.1%]**, exactly 128–128 (n=256), 0 crashes both sides. **No verdict,
  therefore discard.**
- **Read:** this is a stronger null than the win rate alone shows, and that is the point.
  `core_destroyed` came in at **44/256 = 17.2%** against the null-change control's
  **16/96 = 16.7%** — the change produced *no detectable effect at all* on the one axis it was
  specifically designed to move. That distinguishes "didn't clear the bar" from "did nothing",
  and the two call for different follow-ups.
  The likely structural reason, per the runner's read: by the time a builder reaches the
  sentinel gate it has navigated to within dist²≤8 of the Core, where the tiles are already
  occupied by our own economy build-out — so the candidate set frequently collapses to a
  single legal position and the scorer only refines facing among options that were already
  narrow. **This was not instrumented** — no count of how often the scorer picked differently
  from the incumbent — so the mechanism is inference, not measurement.
- **Next:** do **not** try another arc-scoring function first; the flat `core_destroyed` rate
  says arc quality isn't the binding constraint. The cheap prerequisite is to instrument how
  many legal (position, facing) pairs a builder actually has at the sentinel gate. If that
  number is usually 1, the real lever is *where sentinels get built at all* (reserving tiles,
  or building them further out on the approach) and every arc experiment downstream of it is
  measuring nothing.
- **Method note:** the screen read 56.2% and the confirm read 50.0% — a textbook illustration
  of why the screen cannot promote and why "the number went up" is not an accept rule.

### Discard — deliberate harvester-to-Core conveyor chains cost more builder-rounds than they earn

- **Date:** 2026-08-07 · tested against sentinel-first aug7 (fc53345 working tree), parallel
  session (`bots/aug7_h*`, `--jobs 3`)
- **Hypothesis:** the highest-ceiling idea available. Crediting is delivery-only (measured,
  game-model.md): a harvester whose path to the Core never closes earns exactly zero, on the
  balance *and* on tiebreak #1. The incumbent has no deliberate chain-building at all — only
  incidental conveyors dropped on tiles a builder happens to walk over. Conveyors are also the
  cheapest thing in the game on cost-scale (+1% vs +20% for a builder bot), so plumbing should
  be cheap where builder-rounds are the real expense.
- **Change:** a per-builder state machine that, after placing a harvester, takes over that
  builder entirely until the chain is done: greedy staircase route toward the Core (axis with
  more distance remaining, ties random), each link's facing recomputed from its own position
  so corners stay connected, terminating on the Core / an existing building / a 200-round cap.
- **Result:** screen **54.2% [40.3%, 67.4%]** (n=48), confirm **45.3% [39.3%, 51.4%]**
  (n=256), 0 crashes both sides. **No verdict, therefore discard.**
- **Read:** the cost is builder-rounds, not titanium. Laying a chain runs ~2 rounds per tile
  (walk, then build) and monopolises one of only ~5 builders for potentially dozens of rounds,
  against an opponent spending those same rounds finding and building more harvesters. The
  `core_destroyed` rate (42/256 = 16.4%) sat right on the null-change control's 16.7%, so
  nothing about the game's character changed — this was purely an economic trade, and it lost.
  **The chains were never verified to complete**, so strictly this refutes "dedicate builders
  to plumbing", not "complete chains are worthless" — those come apart only if completion is
  measured, which it wasn't.
- **Next:** the same session's dead-code finding above (harvesters may already be served by
  incidental trail conveyors) is the cheaper way at the same underlying question, and is being
  measured directly rather than inferred. Third discard in a row for the shape "spend
  builder-rounds or economy on something else" — that pattern is now very well evidenced.

### Discard — demand-driven ammo conversion loses the same way a bigger buffer did

- **Date:** 2026-08-07 · tested against sentinel-first aug7 (fc53345 working tree), parallel
  session (three hypotheses run concurrently in scratch dirs `bots/aug7_h*`, `--jobs 3`)
- **Hypothesis:** the AMMO_BUFFER 20->50 discard refuted a bigger *standing* buffer, not
  better-*timed* conversion. `convert_ammo()` is usable the same turn and costs no action
  cooldown, so ammo can in principle be raised on demand: hold near-nothing while quiet, burst
  when a threat appears. Named as the explicit follow-up in that discard's "Next".
- **Change:** new store slot 4 carries a threat timestamp. Sentinels scan
  `get_nearby_units(dist_sq=get_vision_radius_sq())` (r²=32, same as their attack radius, so
  strictly earlier warning at no extra reach) and write `round + 1` on seeing any enemy unit.
  The Core reads it and targets 40 ammo (4 sentinel shots) if the sighting is <=5 rounds old,
  else 10 (one shot). Conversion still gated on `harvester_count >= TARGET_HARVESTERS` and
  still reserves a builder bot's cost before converting, both unchanged from the incumbent.
- **Result:** screen **41.7% [28.8%, 55.7%]** (n=48) — survived by the letter of the rule, and
  coincidentally the identical figure to the AMMO_BUFFER=50 screen. Confirm **46.1%
  [40.1%, 52.2%]** (n=256), 0 crashes both sides — **no verdict, therefore discard**.
- **Read:** two independent ammo-timing levers have now failed in the same direction, which
  makes this a pattern rather than one data point: at this bot's strength, ammo scheduling is
  not where the wins are. The experiment confounded two changes it shouldn't have — it both
  *lowered the quiet-phase floor* (20 -> 10) and *added a delayed burst*, so it cannot separate
  "holding too little ammo when first contact happens" from "the burst arrives a round late
  because store writes are buffered". On the mix: this session ran a **null-change control**
  (byte-identical copy of aug7 vs aug7, n=96) which gives the first real baseline for the
  win-condition mix — `core_destroyed` **16/96 = 16.7%**. Against that, the ammo run's
  **28/256 = 10.9%** is a *reduction* in decisive combat outcomes, and the H2 run in the same
  session sat at 17.2%, i.e. right on the control. So the cut ammo floor does look like it
  suppressed core kills — the CIs overlap at the edge (control [10.4%, 25.5%] vs
  [7.7%, 15.4%]) so this is suggestive, not established. Note also the mix is pooled across
  **both** bots in a match, so it can never be attributed to the challenger alone.
- **Next:** if ammo is ever revisited, the clean version is baseline held at 20 (identical to
  the incumbent) with a burst added *on top*, which isolates the burst from the floor cut.
  Low priority: two discards deep, the prior should now be that this lever is worth little.
  The general lesson generalises further than ammo — **an experiment that changes a floor and
  adds a mechanism at once is one experiment producing zero attributable answers.**

### Discard — lowering the small-map defense trigger also loses

- **Date:** 2026-08-07 · tested against sentinel-first aug7 (a9d81a1)
- **Hypothesis:** strategy-notes.md's map-size section: a 14x area range (8x8-30x30) probably
  needs branched strategies, and small maps favour rushing since economy has no time to
  compound. Tried the cheapest version: switch to sentinel-building at 1 harvester instead of
  3 on maps <=150 tiles (tiny8 64, small12 144 -- 2 of 8 maps).
- **Change:** `target_harvesters(ct)` returns 1 below the area threshold, 3 above it. Used at
  both call sites (sentinel-build gate, navigate-to-core gate). Everything else unchanged.
- **Result:** screen vs incumbent: **35.4%, CI [23.4%, 49.6%] — refuted** (upper bound just
  under 50), discarded without a confirm run.
- **Read:** same mechanism as the scout-first discard just above, in miniature — cutting
  harvesters from 3 to 1 forfeits ~2 harvesters' worth of economy (each ~2.5 Ti/round once
  delivering) in exchange for a slightly earlier sentinel, and the economy loss outweighs the
  earlier defense even on the smallest maps. Combined with the scout-first result, this is a
  second, independent data point that this bot's economy-first shape is robust across the map
  size range — "small map = rush" from strategy-notes.md is not supported so far, at least not
  via this lever.
- **Next:** map-size branching on *something other than the harvester trigger* remains
  untested (e.g. sentinel placement radius, spawn aggressiveness, MAX_BUILDERS) if this is
  revisited. Lower priority now given two discards in a row on the small-map-rush thesis.

### Discard — scout-first before building is a decisive loser

- **Date:** 2026-08-07 · tested against sentinel-first aug7 (a9d81a1)
- **Hypothesis:** open-questions.md asked whether "scout first, build later" (dodging early
  scale tax, per strategy-notes.md) beats building immediately — flagged explicitly as
  worth testing rather than assuming, against the official docs' opposite advice.
- **Change:** gate `_try_build_harvester` on `ct.get_current_round() >= SCOUT_ROUNDS` (20).
  Nothing else built (harvesters, sentinels) for the first 20 rounds either, since sentinels
  are already gated on harvester count.
- **Result:** screen vs incumbent: **8.3%, CI [3.3%, 19.6%] — decisively refuted**, discarded
  without running confirm (upper bound nowhere near 50%).
- **Read:** settles the open question outright, and confirms harvester ROI dominance
  (strategy-notes.md: payback ~8-12 rounds) beats the scale-tax-avoidance argument by a wide
  margin at 20 rounds. The official docs' "build aggressively early" was right about the
  direction, if not the reasoning given. Scale tax matters at the margin (which harvester to
  build, not whether/when to start) — it doesn't justify sitting on your hands.
- **Next:** the scale-tax discipline from strategy-notes.md (don't over-build builder bots,
  `destroy()` obsolete infrastructure) is a different claim than "delay everything" and isn't
  refuted by this result. Worth keeping separate in future tests.

### Discard — raising AMMO_BUFFER for sentinels backfired

- **Date:** 2026-08-07 · tested against the sentinel-first aug7 commit (a9d81a1), not v4
- **Hypothesis:** AMMO_BUFFER=20 was tuned for gunners (4 Ti/shot -> 5 shots buffered); a
  sentinel at 10 Ti/shot only gets 2 shots of reserve at the same number. Raising it to 50
  (5 shots, matching gunner's shot-count buffer) should sustain fire better in a fight.
- **Change:** `AMMO_BUFFER = 20` → `50`. Nothing else.
- **Result:** screen 41.7% [28.8%, 55.7%] (not clearly refuted by the letter of the screen
  rule, but already trending down); confirm **45.3%, CI [39.3%, 51.4%] — no-verdict**,
  leaning negative. Discarded, `git reset --hard`.
- **Read:** the mechanism assumed sustained-fire fights are common enough that a bigger
  buffer pays for itself. More likely what actually happens: most of the match nothing is in
  range, so a bigger buffer just means more Ti parked as idle ammo instead of building
  harvesters/sentinels/conveyors during the quiet phases — exactly the failure mode
  strategy-notes.md already called out for the starter bot's fixed top-up. Bigger ≠ better
  once the buffer covers a couple of shots; the quiet-phase opportunity cost dominates.
- **Next:** an adaptive buffer (top up more only when an enemy is actually visible) is the
  more promising version of this idea, per strategy-notes' "adaptive ammo" note — a fixed
  buffer at any size trades against economy growth. Left for a future experiment.

### aug7 — Sentinel-first defense: the untested strategy-notes guess held, hard

- **Date:** 2026-08-07 · `bots/aug7`, built on v4 · **Not yet submitted** (no platform account)
- **Hypothesis:** [strategy-notes.md](strategy-notes.md) flagged Sentinel as strictly better
  than Gunner for a static base defender (more dmg/round, better Ti-per-damage, more HP,
  2.5x the attack radius, unblockable by walls/units) except for 10 Ti lower entry cost and
  re-aimability — neither of which matters once a turret is placed and never moves. Marked
  "untested guess, needs a real A/B" in the notes.
- **Change:** one conceptual swap. `_try_build_gunner`/`_run_gunner` → sentinel equivalents
  at the same trigger point (`harvester_count >= TARGET_HARVESTERS`), same facing-away-from-
  core logic, same 18-tile-from-core placement gate, same `AMMO_BUFFER = 20`. The only new
  code: sentinels have no `get_gunner_target()`-style helper, so targeting scans
  `get_attackable_tiles()` for the first tile holding an enemy unit or building and fires
  there.
- **Result:**
  - **Screen vs v4 (48 matches): 64.6% [50.4%, 76.6%]** — 5 `core_destroyed` wins appeared
    where the v4-only baseline essentially never had any.
  - **Confirm vs v4 (256 matches): 68.4%, CI [62.4%, 73.7%] — clears the accept gate outright.**
  - 0 crashes both sides. Win conditions shifted hard: 24 `core_destroyed` (up from a
    background rate near zero), plus more `titanium_collected` wins too — sentinels aren't
    just killing cores, they're also denying enemy economy better.
- **Read:** the derivation held, and by a wide margin — this isn't a marginal tuning win,
  it's the biggest single-change jump since v1's crash fix. Best explanation: r²=32 vs r²=13
  means a sentinel covers a conveyor approach a gunner simply can't see, and the unblockable
  line means enemy builder bots can't screen it by standing in front of infrastructure.
  Reinforces the notes' broader point that the tutorials' Gunner-first framing is actively
  wrong for this game, not just suboptimal.
- **Next:** aug7 is now the strongest bot measured. Continue the loop from here — the ammo
  buffer (20 Ti = 2 sentinel shots) was left untouched for attribution; worth its own
  experiment now that sentinels are the default (open-questions.md: adaptive ammo).

### v4 — full direction-neutralisation: the fairness fix turned out to be a strength fix

- **Date:** 2026-08-06 · **Not yet submitted** (no platform account) · **Current best**
- **Hypothesis:** v3's ring spawn removed only part of the measured seat bias (mid20 mirror
  0/32 → 28%, not 50%); carrying over the rest of probe_neutral's neutralisations — randomised
  movement tie-break, randomised ore-scan tie-break, shuffled build/heal scans — should finish
  the job. Expected mostly a fairness change, neutral-to-slightly-positive on win rate.
- **Change:** v2's CPU guard + the complete neutralisation set from probe_neutral. One
  conceptual change vs v3: "remove the remaining absolute-direction tie-breaks".
- **Result:**
  - **vs v3: 60.9%, CI [54.8%, 66.7%], 256 matches — clears the accept gate outright.**
  - vs starter: **74.2%, CI [68.5%, 79.2%]** (v1 was 59.4%), 0 crashes vs 535, tiny8 32/32.
  - Mirror seat split: mid20 53.1%, small12 46.9% — **fair**. tiny8 84.4% — engine effect,
    expected, unfixable.
- **Read:** the surprise is the raw strength gain. Best explanation: v1's fixed tie-breaks
  made every builder chase the *same* first-enumerated target, colliding and shadowing each
  other; randomising de-correlates them into better map coverage. (Also: on biased maps, half
  of all games were previously started from the handicapped seat.) A fairness argument found
  a play-quality bug — absolute-direction habits were costing games everywhere, invisibly.
- **Next:** v4 is the submission candidate. On approval: re-baseline on the real pool before
  any tuning (runbook.md).

### v3 — full-ring spawn only: the decomposition step

- **Date:** 2026-08-06 · superseded by v4 the same day
- **Hypothesis:** the NW-corner spawn scan is the dominant cause of the seat wipeouts.
- **Change:** v2 + spawn candidates = whole 12-tile ring (random choice), nothing else.
- **Result:** mirror mid20 seat A 0/32 → **28.1%** [16%, 45%] — most of the wipeout, not all
  of it. vs v2: 52.0% [45.8%, 58.0%], no-verdict (expected: the fix only pays on the map
  class that exposes the handicap). 0 crashes.
- **Read:** ring spawn is necessary but not sufficient; the residual bias lives in the other
  absolute-direction tie-breaks. Kept only as the attribution step for v4.

### Experiment — seat bias dissected: it was mostly us, and partly the engine

- **Date:** 2026-08-06 · `bots/probe_neutral` (v1 with every absolute-direction bias removed)
- **Design:** if the seat-A wipeouts survive direction-neutralisation in a mirror, they're
  the engine's; if they vanish, they were ours.
- **Result (mirror, 32 matches/map):** mid20 0/32 → **53.1%** and small12 → 46.9% — *ours*.
  tiny8 → **78.1% [61%, 89%] seat-A**, confirmed at 84.4% in the v4 mirror — *the engine's*:
  a genuine first-mover advantage on the 8×8 map that survives full neutralisation.
- **Mechanism found on the way:** `get_position()` is the Core footprint's NW corner, so the
  starter bot's `pos.add(d)` spawn scan reaches only the N/W sides of the legal 12-tile ring
  (`bots/probe_spawn`, tile-by-tile). One seat spawned toward the map corner, the other
  toward the centre, every game.
- **What this changes:** (1) absolute-direction habits are a class of bug, not a style choice
  — audit for them; (2) on tight maps, seat draw is real regardless of bot quality → find out
  how the ladder assigns seats within a best-of-five; (3) our mirror-fairness check (arena
  per-map seat split) is now a standing regression test for reintroduced direction bias.

### Experiment — titanium is credited on Core delivery, and only then

- **Date:** 2026-08-06 · `bots/probe_credit` / `probe_credit_nc` / `probe_idle`
- **Design:** one harvester + one dead-end conveyor (facing away from the core, output onto
  empty ground / off-map), then idle; core logs the balance every round. NC variant: no
  conveyor at all. Passive-only slope is 2.5 Ti/round; a credited harvester would add 2.5.
- **Result:** both variants, 990+ rounds: balance slope **exactly 2.500**,
  `a_titanium_collected` **0**. A dead-end chain and no chain are *identical*: zero.
- **Read:** **"titanium collected" = titanium delivered to the Core.** The tiebreak-#1
  counter and the spendable balance both move only on delivery. An unrouted harvester
  contributes nothing to tiebreak #1 or #3 and no income — it pads tiebreak #2 (harvester
  count) while costing 20 Ti and +5% permanent scale. Chain completion isn't an optimisation,
  it's the whole game. This also closes the loop on the starter bot's economics: its walking
  trails of toward-core conveyors evidently do deliver (balance reconciliation matches), so
  hypothesis (c) from open-questions held.
- **Aside, measured:** `can_build_conveyor()` permits a facing whose output is off-map.

### v2 — CPU-budget guard: bail at phase boundaries, not mid-statement

- **Date:** 2026-08-06 · **Not yet submitted** (no platform account)
- **Hypothesis:** exceeding 10 ms CPU silently truncates the unit's round mid-statement —
  wasted round, possibly half-updated instance state. v1 never approaches the limit locally,
  so the guard should be inert here; its value is ladder hardware (Graviton3, unknown relative
  speed) and future heavier strategy code. Predicted before measuring: no local effect,
  vs v1 reads no-verdict ≈50%.
- **Change:** `_cpu_exhausted()` checks `get_cpu_time_elapsed()` ≥ 8000 µs between builder
  phases (priority: build > heal > move > share); first trip per unit reported to stderr.
  Nothing else.
- **Result:** vs v1: **52.0%, CI [45.8%, 58.0%]**, 256 matches, no-verdict — as predicted.
  vs starter: 56.6% [50.5%, 62.6%] (v1's edge retained). 0 crashes. Guard confirmed never to
  trip locally (zero CPU-GUARD lines across a full instrumented match).
- **Read / rule note:** program.md's gate (lower bound > 50%) is for changes claiming to
  improve play; applied to insurance changes it would auto-discard all of them. Accept rule
  used here, stated in advance: keep unless refuted (upper bound < 50%) or crashes appear.
  Deliberate, documented deviation — not a precedent for strategy changes.

### v1 — robustness only: don't let units delete themselves

- **Date:** 2026-08-06 · **Not yet submitted** (no platform account)
- **Hypothesis:** the starter bot's uncaught exceptions are its single biggest weakness. The
  engine permanently deletes a unit on any escaping exception, so every crash is a unit lost
  for the rest of the match — not a skipped turn.
- **Change:** two things, nothing else.
  1. `run()` wraps a `_dispatch()` in `try/except Exception`, reporting only the first
     traceback per unit to stderr (so a per-round bug can't flood the log or eat the 10 ms
     CPU budget formatting tracebacks).
  2. New `in_bounds()` helper, checked in `_try_move()` before touching the engine.
     `_move_toward_target()` tries up to four directions, and tile queries like
     `is_tile_empty()` **raise** off-map rather than returning False — so every bot standing
     on an edge tile was rolling the dice on its own life.
- **Predicted effect:** large. Stated before measuring.

**Result — 256 matches (8 maps × 16 seeds × both seat orderings):**

| | v1 | starter |
| --- | --- | --- |
| Wins | **152** | 104 |
| Win rate | **59.4%**, 95% CI [53.3%, 65.2%] | — |
| Crashes | **0** | **515** |

Lower bound clears 50%. **Keep.**

**Read:** the hypothesis held, but the effect is *smaller than the crash count suggests*.
515 crashes over 256 matches is ~2 units lost per match per side — real, but with typical
end-of-match unit counts of 5–13 it's usually a wound rather than a kill. The exception is
small maps: on `tiny8` v1 went **31/32**, where losing two bots is losing the whole economy.
So the crash bug's cost scales inversely with map size.

**Worth not over-reading:** per-map splits here are 32 matches each, so their intervals are
±17 points. v1's apparent loss on `vsym16` (13/32) is well inside noise. Only the pooled
verdict is solid.

**New evidence on the seat question:** on `mid20`, seat A lost **0/32** — and v1 took exactly
the 16 of those where it happened to be seat B. Seat decided that map regardless of which bot
sat in it. Since v1 doesn't crash at all, this rules out "crashes cause the seat effect" and
points at an engine/layout interaction. `small12` behaves the same way (2/32). The earlier
`tiny8` wipeout, by contrast, has now vanished (46.9%) — that one *was* crash-driven.

**Next:** v1 is the new baseline. Real strategy changes should wait for `fcode maps sync`;
tuning against eight invented maps risks fitting the wrong distribution. Remaining robustness
work that's distribution-independent: a CPU-budget guard using `ct.get_cpu_time_elapsed()`.

### Baseline — shipped starter bot, measured locally

- **Date:** 2026-08-06
- **Not a submission** — this is the reference opponent everything else gets measured against.
  `bots/starter/main.py` is left exactly as `fcode starter` generated it, on purpose.
- **Setup:** mirror matches, `--tle 10`, on six self-generated maps spanning the pool's
  8×8–30×30 range (see [tooling.md](tooling.md)).

**Results — 5 mirror matches, one per map:**

| Map | Winner by | Units left (A / B) | Mined (A / B) |
| --- | --- | --- | --- |
| tiny8 | Harvesters (tiebreak) | 0 / 5 | 0 / 0 |
| small12 | Titanium collected | 0 / 10 | 0 / 4960 |
| duel16 | Titanium collected | 1 / 7 | 2480 / 2470 |
| mid20 | Titanium collected | 3 / 11 | 2470 / 2480 |
| wide30x14 | Titanium collected | 4 / 13 | 4960 / 2640 |
| large30 | Titanium collected | 12 / 11 | 7450 / 4980 |

**What this establishes:**

1. **Every match went to the round-1000 tiebreak. 6 of 6.** No Core was ever destroyed, in a
   mirror match or otherwise. This is strong support for the economy-first read in
   [strategy-notes.md](strategy-notes.md) — the tiebreak *is* the win condition in practice,
   and its first key is titanium collected.
2. **The shipped starter bot crashes constantly**, 2–9 uncaught `GameError: Position out of
   bounds` per match. Each one **permanently deletes that unit**. Two matches ended with a
   side on **zero units and zero titanium mined** — a total economic wipeout caused entirely
   by its own bug, not by the opponent.
3. Identical bots produce wildly asymmetric outcomes (0 units vs 10) purely from where the
   crashes happened to land. Variance in this game is enormous; **one match proves nothing**.
   Any future comparison needs many matches across many maps and seeds.

**The bug:** `bots/starter/main.py:391` calls `ct.is_tile_empty(next_pos)` without a bounds
check. `next_pos` is off the map whenever a builder is on an edge tile, and the call raises.
`run()` has no `try/except`, so the exception escapes and the engine deletes the unit forever.

**Next:** our v1 is the starter bot plus (a) a top-level `try/except` in `run()` and (b) a
bounds check before that call. Nothing else. If the baseline read is right, that alone should
be a large improvement, and it isolates a single change so the result is attributable.

---

### Seat matters enormously on some maps — measured, cause unknown

- **Date:** 2026-08-06
- **Setup:** `tools/arena.py starter starter`, 16 mirror matches per map (8 seeds × both
  seat orderings), `--tle 10`.

With **identical bots on provably symmetric maps**, the team that acts first (seat A) wins:

| Map | seat A wins | 95% CI |
| --- | --- | --- |
| tiny8 | **0 / 16** | [0%, 19%] |
| small12 | **0 / 16** | [0%, 19%] |
| mid20 | **0 / 16** | [0%, 19%] |
| duel16 | 9 / 16 | [33%, 77%] |
| large30 | 9 / 16 | [33%, 77%] |
| wide30x14 | 10 / 16 | [39%, 82%] |

Three maps are fair. Three hand the win to the second mover **every single time**.

**Ruled out:** map asymmetry. The generator's output was verified tile-by-tile — every map is
exactly symmetric under its declared transform (`asym=0`), with equal ore near each core.

**Not yet known:** whether this is (a) an engine turn-order advantage that only bites on
certain layouts, or (b) the starter bot's absolute-direction bias — it closes the x-gap before
the y-gap and scans `CARDINALS` in a fixed order, so under 180° rotation it genuinely plays
differently from the other seat. A symmetry-type probe was inconclusive: horizontal-mirror
gave 29%, vertical-mirror 54%, and the six rotational maps split 3 fair / 3 wipeout.

**What this changes right now, regardless of cause:**

1. **Never evaluate on a single seat ordering.** On half these maps it would produce a
   perfectly confident, completely wrong answer. `tools/arena.py` plays both orderings
   always, and reports seat split per map rather than pooled.
2. **Pooled statistics lie here.** The 96-match aggregate read 20.8% seat-A — a number that
   describes none of the six maps. Always decompose.
3. **Suspect absolute-direction logic in our own bot.** Whatever the cause, a bot whose
   behaviour depends on which way is "east" is a bot that plays two different games depending
   on which corner it spawns in. Prefer core-relative reasoning to map-absolute reasoning.
