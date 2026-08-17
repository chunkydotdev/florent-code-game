# SCREEN PREREG — `RINGLADDER`: the ferry-siege ring-ladder PACKAGE, head-to-head against the PROGRAMME INCUMBENT, fired FOR THE MEASUREMENT

Drafted by a fresh opus subagent with NO inherited session context beyond the
inputs listed under `PROVENANCE`. The builder lane ratifies the judgment lines
and types the lock commit; this agent wrote no code under `bots/`, appended no
worklist row, appended no `docs/prereg/BARS.tsv` row, fired no game, started no
shard, and touched neither `results.tsv` nor `HANDOVER.md` nor `PROGRAMME.md`
nor `QUEUE.md`.

**⭐ THE PURPOSE LINE, AND IT IS NOT A PASS.** Magnus's instruction this session
is *"v512 on a core ASAP for the powered measurement"*
(`docs/coordination.md:71279`). **The deliverable of this shard is A CLEAN NUMBER
FOR THIS TREE ON THE POOL WE ACTUALLY PLAY, not a bar clearance** — and the
arm's own build grid says plainly that it will not clear the bar. **What makes
the leg worth a core is that the grid is nearly blind to the shard's fixture:
of the 15 maps in the corefill pool, THREE were in the build grid
(`glacierkeep`, `nordkap`, `midgard`) and TWELVE carry ZERO observation of this
tree** — two of the grid's five maps (`atoll`, `heart`) were retired from the
pool on 2026-08-13 and the shard never plays them. **80% of this shard's rows
land on geometry the plank has never been measured on.** That is the
information; the bar is the house instrument for reading it.

**STATUS: drafted BEFORE the `RINGLADDER` row is appended to
`scratchpad/corefill_work.txt`, BEFORE any `docs/prereg/BARS.tsv` row exists,
BEFORE any file named `scratchpad/overnight/RINGLADDER*` exists, and BEFORE the
leg's first game.** Drafting session wall clock at write time
**`2026-08-17T20:17:54Z`** (`date -u`, same shell call); repo HEAD at draft
`612c3562` (author time `2026-08-17 22:12:28 +0200`). Verified at draft:
`grep -c RINGLADDER docs/prereg/BARS.tsv` → **0**;
`grep -c RINGLADDER scratchpad/corefill_work.txt` → **0**;
`grep -c RINGLADDER results.tsv` → **0**;
`ls scratchpad/overnight/ | grep -ci ringladder` → **0**.
**Seed base 872000 verified free:** `git grep -l 872000` returns exactly two
files — `corpus/_rebuild/league_matches.tsv.pre-trap9-…`, where the digits are a
coincidental substring of an Elo float (`-0.5708720001729759`), and
`docs/coordination.md:71279`, which is the builder's own reservation of this
base for this shard. No tape, worklist row, BARS row, `results.tsv` row or
`elo_history.tsv` row uses it.

### LOCK, clock 2 (local shard)
Per the obligations doc's **2026-08-17T07:24:55Z addendum**, cited rather than
restated. **PRIMARY:** the shard tape's own `# FIXTURE … start=` stamp
(`tools/overnight.sh:99` sets `START=$(date -u …)`, `:103` writes it to the tape
before the first game). Quote it verbatim beside the lock commit's git author
time. **BACKSTOP, if the tape carries no `# FIXTURE` line:** the tape's FIRST
COMPLETED ROW `ts` — conservative by construction (measured cost 1–2 s on the
107 stamped local tapes). ⛔ **NOT AVAILABLE: the heartbeat's `STARTING` line**
(`overnight.sh:100` writes it with `>`; every later state overwrites it).
**State which clock was used.** This shard is registered **LOCAL and SAME-HOST**,
so the primary is expected.

### ⭐ COMMIT PROVENANCE — BOTH TREES ARE GIT-PINNED AND CLEAN
* **TREATMENT `bots/_v512ringladder`** — `git ls-files` lists all **five**
  modules; `git status --porcelain bots/_v512ringladder` is **empty**; added
  whole in **`001a6aac`** (`2026-08-17 22:00:06 +0200`, *"BUILDER s50:
  _v512ringladder — ladder+dodge verified (0/732 inversions) …"*). Digests at
  draft `doctrine.py 687c6f9abfec83df3a1c028c0e6fe50d` ·
  `eco.py 53135a83bd62ee4621906246beda5d4f` ·
  `main.py 1bd265834ac8becaf877ee54f6dffc10` ·
  `raid.py 83d55dbd20fcd3a0e3c0a91ae2c6c713` ·
  `siege.py 0128c36a60be7d862a2be92008480c71`.
* **CONTROL `bots/_v488beltbreak2`** — `git ls-files` lists all four; porcelain
  **empty**; newest commit touching it **`997bcd42`
  (2026-08-17 11:12:38 +0200)**; digests
  `doctrine.py b572a721531b77a8c27102bf64313996` ·
  `eco.py 47dc496fc0d14ba950c45c3d43a5f9d0` ·
  `main.py d7f31eedc6795956b72b541eb383c896` ·
  `raid.py c89950470aca51bfaed68712f3690220`.
⚠ **CONTROL ≠ HOLDER, DISCLOSED IN THE FIRST PARAGRAPH THAT USES IT.**
`bots/_v488beltbreak2` is the **PROGRAMME INCUMBENT** — the tree whose own
completed shard reads 53.09% [51.76, 54.42] vs `_v468kladturbo`
(`results.tsv:beltbreak2-final`). **It is NOT the live ladder holder.** The
holder is **v160**, a teammate's ship. Every share on this page is written
`X% vs _v488beltbreak2` and never bare, and **nothing on this page prices this
tree against what is actually on the ladder.**
⚠ **The same inference caveat SALTRAY carried applies and is not repaired by
tracking:** *"the control is the same bytes that produced the completed
`beltbreak2-final` tape"* is inferred from working-tree cleanliness, not from a
stamp on that tape. The tape has no tree-digest column. It is a sound inference
and it is an inference.

---

## ⛔ READ BEFORE RATIFYING — SEVEN THINGS THE LANE OWNS

**1. ⛔⛔ THE BIGGEST THING ON THIS PAGE: THE ARM'S OWN GRID PRICES IT AT ROUGHLY
30%, THE CEILING ARITHMETIC PUTS ITS BEST CASE BELOW THE CATASTROPHE
THRESHOLD, AND THE MODAL OUTCOME OF FIRING IS A `CATASTROPHE` STOP AT ~400
GAMES.** Said first, not argued around.

The build grid (`docs/research/BUILD-REPORT-v512ringladder-2026-08-17.md`) read
**22/60 (36.7%)** pooled vs **this exact control** — and that pooled figure is
not the shard's fixture. Decomposed against the pool this shard actually plays:

| grid cell | grid result | in the 15-map corefill pool? |
|---|---|---|
| **siege maps** (`glacierkeep` `nordkap` `atoll` `midgard`) | **12/48 = 25.0%**, Wilson [14.92, 38.79] | `atoll` **RETIRED 2026-08-13**; 3 of 4 in pool |
| **`heart`** (map-gated → incumbent play) | 10/12 = 83.3% | **RETIRED 2026-08-13 — the shard NEVER plays it** |

**THE SHARD'S POOL COMPOSITION, computed at draft by running the bot's OWN gate
predicate against `maps/*.map26`** (`bots/_v512ringladder/siege.py:206-220`:
`max(w,h) < FS_MIN_MAP_DIM(12)` · `core d² < FS_MIN_CORE_DSQ(72)` ·
`sig ∈ FS_MAP_SKIP`):

```
GATED  (plank refuses; plays the incumbent raid)   3 of 15 =  20.0%
   antler        14x18  cores (6,4)/(6,12)   d^2=  64  -> DSQ<72
   archipelago   26x26  cores (5,5)/(19,19)            -> FS_MAP_SKIP (shares
                                                          snowflake's signature)
   fjordgate     10x10  cores (2,2)/(6,6)    d^2=  32  -> DIM<12 AND DSQ<72
SIEGE-ACTIVE                                      12 of 15 =  80.0%
   auroraveil drakkarfjord drumlin frostgate glacierkeep icefloe
   midgard nordkap ragnarok royale valkyrie yulerune
```

**⇒ THE COMPOSITION PRIOR: 0.80 × 25.0 + 0.20 × 50.0 = 30.0%.** Taking the
siege segment at the whole-grid rate instead of its own subset, and the gated
cells at the structural 50: 0.80 × 36.7 + 0.20 × 50.0 = **39.4%**. **No honest
composition of the arm's own numbers reaches 45.**

**2. THE CEILING ARITHMETIC SAYS THE SAME THING INDEPENDENTLY AND IS THE
REGISTERED `SEGMENT VALUE CEILING`.** Give the siege segment its measured
**upper** 95% Wilson bound and the gated segment its structural null:
**0.80 × 38.79 + 0.20 × 50.00 = 41.03pp.** **That is BELOW the CATASTROPHE
threshold of 45.0 and 10.30pp below the 51.33 bar.** Even the indefensibly
generous variant — gated cells at `heart`'s 83.3%, a rate observed on a map the
shard never plays and produced by a *different* gate predicate — reads
**0.80 × 38.79 + 0.20 × 83.33 = 47.70**, still below 50 and still below the bar.
⇒ **at every optimistic input the arm's own build measured, this package cannot
clear its own bar.**

**3. PRICED BEFORE THE FIRE.** Prefix looks are one-shot at each mark
(`tools/auto_gate.py`, `Tape.wins_at_mid` / `wins_at_half`); the CATASTROPHE
clause (`:815-824`) is **not** prefix-pinned — it reads the CI of the tape as it
stands, every time the gate runs, from n ≥ 400 onward. Naive normal, Z95 = 1.96,
local DEFF 0.98 ⇒ no inflation. The n=400 stop threshold solves
`p̂ + 1.96·√(p̂(1−p̂)/400) < 0.45` ⇒ **p̂ ≤ 160/400 = 40.00%**:

```
true share   P(CATASTROPHE stop      P(TREND-FLOOR@1000    P(reach n=5400)
             at the first look,      stop, prefix<52.0 |
             n=400)                  survived to 1000)
  25.0            ~1.0000                  ~1.000            0.000
  30.0  <- prior   0.99999                 ~1.000            0.000
  36.7             0.926                   ~1.000            0.000
  41.0  <- ceiling 0.369                   ~1.000            0.000
  45.0             0.026                   ~1.000            0.000
  50.0             0.00004                  0.897           ~0.000
  55.0            ~0.000                    0.028            0.486
```
**⇒ under ANY prior this arm's own measurements support (25 – 41), the shard
stops at the FIRST GATE LOOK PAST n=400 with probability 0.37 – 1.00, and
P(completion) is 0.000.** At ~10–20 s a game on one core that is **roughly
1.5–2.5 core-hours**, not a night. **That must be the builder's stated
expectation before a core is spent, not a surprise at 22:30.**
⚠ **The stop depends on `gate_watch` actually running against the BARS row.**
`tools/overnight.sh:47` records that **no firing path calls the gate
automatically**; if nothing polls, the shard runs on. Confirm the watcher is
live, or the "modal outcome" above is a plan and not a mechanism.

**4. ⛔⛔ THE SCREENED TREE CARRIES ITS DEMO INSTRUMENTATION SWITCHED ON, IN THE
TREATMENT ONLY, AND THAT IS A CONFOUND THAT CAN ONLY HURT IT.**
`bots/_v512ringladder/doctrine.py:2558` **`FS_DRAW_ON = True`** (per-round
`draw_indicator_*` calls) and **`:2561` `FS_LOG = True`** (per-event `print(…,
file=sys.stderr)` at `siege.py:80-86`). The control pays neither.
`tools/overnight.sh:138` runs every game with **`--tle 10`**, and that limit
BINDS locally — the runner's own comment records `_v145bestfit` winning 6/6 with
the limit off and losing 5/6 with it on. **A TLE'd turn is silently skipped**, so
instrumentation cost lands as lost raider actions, in one arm.
**SIZED HONESTLY RATHER THAN WAVED AWAY:** the `GATE` log is cached per unit
(`siege.py:178,193`), so the high-volume tag is the per-round `STAT` line from
ONE unit — bounded, small, and **unmeasured**, because
`get_cpu_time_elapsed()` is a stub locally (0 across 200,633 `BotOutput` events)
and local replays carry no exec-time fields at all.
⇒ **REGISTERED CONSEQUENCE: a Band-4 or Band-5 reading CANNOT separate *"the
plank subtracts"* from *"the plank TLEs under its own logging"*.** The build
grid embeds the same confound, so the 36.7% prior does not adjudicate it either.
**This is RATIFICATION BLOCKER B1.**
⇒ **RULED (builder s50, pre-lock): BRANCH (ii).** Both flags flipped to `False` in
the screened tree before the lock commit (the flip is IN the lock commit, so the
page and the fired bytes cannot diverge). The confound is REMOVED. Consequence
carried honestly: the n=60 build grid ran with the flags ON, so the grid prior
describes a *different configuration* than the shard fires — one more reason the
prior does not adjudicate and the shard is worth its core.

**5. ATTRIBUTION SCOPE — THIS CELL MEASURES THE WHOLE FERRY-SIEGE STACK, NOT THE
LADDER CLAUSE.** Treatment `_v512ringladder` = incumbent `_v488beltbreak2`
**+ the ferry-siege plank (v510) + barriers-only seal (v511) + the at-ring
priority ladder, eviction rung, raider sentinel and reactive dodge (v512)**.
Clause isolation for the ladder would be `_v512ringladder` vs `_v511sealonly`
and **is NOT being run today** — one core, Magnus's one-plank directive.
**CONSEQUENCES, all registered:**
* **A pass promotes the STACK.** No sentence at readout may attribute a pass to
  Magnus's rung order.
* **A fail does not refute the rung order either** — and specifically does not
  refute **P6**, the engine fact under it (enemy bodies block barriers; evict
  before clear is engine-correct), which stands on its own evidence.
* **The component with a prior against it is the collar**: closures REGRESSED
  30.0% → 13.3% from parent to this arm while wins rose 23.3% → 36.7%. **This
  leg cannot separate "the sentinel bought the wins" from "the collar loss cost
  them".**

**6. THE SHARD'S REGIME IS `NOISE_ON`, AND NO PAIRING EXISTS.**
`bots/_v512ringladder/doctrine.py:474` and `bots/_v488beltbreak2/doctrine.py:474`
are both `NOISE_ON = True`, and `tools/overnight.sh:31` records that this is
deliberate (*"we want THE BEHAVIOUR WE SHIP"*). The salt is an **unseeded**
`random.Random()`, so two games at one `--seed` are not reproducible and **no two
rows are a matched pair**. ⭐ **THE PARENT'S BUILD REPORT ESTABLISHED THIS AS A
LAW AND IT GOVERNS HOW THIS PAGE READS ITS OWN INPUTS**
(`BUILD-REPORT-v511sealonly-2026-08-17.md`, surprise 1: three runs of v510 on
`midgard` seed 7 gave r1000 / r133 / r362). **Every single-game read is ONE DRAW.
The demos on this page are illustrations, never evidence**, and the v512 report's
own surprise 4 (*"four near-identical arms spanned wins 7–9 at n=30"*) is why the
grid numbers here are quoted at n=60 and n=48, never at n=12 without saying so.
**Registered: `CLUSTER UNIT: none`, DEFF 0.98, naive.** The enumeration is
performed in the registration block, not asserted.

**7. ZERO-SUM SELF-LEG, AND THE CANCEL-FOR-CAPACITY POLICY, PRE-COMMITTED.**
The control is this tree's own ancestor chassis, so **"our win" and "their loss"
are the SAME EVENT** — every per-side metric is mechanically anti-correlated with
its counterpart, which is why the kill-clock reads are registered WITHIN-ARM and
the r300 bar is a one-sided safety backstop.
⚠ **THE STRUCTURAL NULL ON A GATED MAP IS *NEAR* 50.00, NOT EXACTLY 50.00, AND
SALTRAY'S BYTE-IDENTICAL ARGUMENT IS NOT AVAILABLE HERE.** On a gated map the
plank refuses and the bot *"plays the incumbent raid doctrine for that game,
unchanged"* (`siege.py:187`) — but the tree is not byte-identical to the control
on that path. Verified at draft: `eco.py` +14 lines gated on
`LOKI_FERRY_SIEGE_ON and FS_COLLAR_RESERVE_ON` and further conditioned on a live
`SLOT_FS` ring/kill phase that a gated map never reaches; `raid.py` +28 lines
(`beat &= FS_BEAT_MASK`, a no-op when no high bits are ever written; a
`_fs_launcher_turn` hook that returns False when the gate is off); `main.py`'s
ammo-conversion changes sit inside `if fs_live:` and behind `or fs_live` in the
conversion predicate. **⇒ the gated-map equivalence is FLAG-AND-STATE
CONDITIONED, NOT BYTE-VERIFIED, and the page says so.** The grid's one gated
cell read **10/12 = 83.3%** — P ≈ 0.019 under a true 50 — which is either a
NOISE_ON draw at n=12 (the regime's own law says single-cell reads are one draw)
or residual chassis drift. **Both readings are live and this leg's gated segment
is the thing that separates them.**
⭐ **CANCEL-FOR-CAPACITY, PRE-REGISTERED NOW so it cannot be improvised later:
if the builder stops this shard to return the core to other ferry-siege work
(a second-body arm is the build report's own named next lever), that is an
OPERATIONAL CANCELLATION FOR CAPACITY — typed `cancellation`, POLICY AND NOT
EVIDENCE.** It licenses no sentence about whether the package pays, the partial
share is disclosed as **unselected** (a capacity stop is blind to the share,
unlike a floor or catastrophe stop, so the selected-pessimistic regression caveat
does NOT apply to it — and saying so is required, because quoting it would
understate the arm), and the rows are kept.

---

## RATIFY: Hypothesis

**HYPOTHESIS (a PACKAGE statement, not a one-mechanism statement).** *The
ferry-siege ring-ladder package — the launcher ferry that delivers a raider to
the enemy ring, the barriers-only collar, Magnus's at-ring priority ladder
(1 barriers / 2 evict / 3 clear-and-replace / 4 a second sentinel outside the
ring), the eviction rung, the raider-built sentinel and the ray-triggered
reactive dodge, all behind `LOKI_FERRY_SIEGE_ON` / `LOKI_FS_SEAL_ONLY` /
`LOKI_FS_RING_LADDER` and gated off three of the pool's fifteen maps — produces
a LOCAL pooled game share of **51.33% or higher** against the incumbent
`bots/_v488beltbreak2` at n = 5,400 games across all 15 corefill maps and both
seats, WITHOUT pushing our own kill past r300.*

⛔ **REGISTERED DIRECTION, AND IT IS THE ONE PLACE THIS PAGE DEPARTS FROM THE
FAMILY TEMPLATE: the BAR is scored POSITIVE (`ge 51.33`) because that is the
house screen, but THE PRE-REGISTERED EXPECTATION IS NEGATIVE.** This page
predicts **Band 5** (CI upper < 45.0) and prices it at 0.37–1.00 (#3). **A
result at or above 50 would be a genuine surprise and is exactly what makes the
leg worth firing:** 12 of the 15 maps this shard plays carry no observation of
this tree at all.

**THE MECHANISM CHAIN, stated so it can be wrong.** The plank's currency claim
is a **collar**: eight orthogonal barriers on the enemy core's heal seats. The
parent measured the zero-law in combat — **2,069 full-seal rounds → 0 enemy
on-core heals and 0 spawns**, against 0.1122 heals/rnd and 0.0236 spawns/rnd
over 9,587 open-ring rounds **in the same games** (conditioned on STATE, not
arm, because an arm with no damage source gives the defender nothing to heal).
⭐ **The v512 discovery this leg exists to price is that the collar and the kill
are IN TENSION, measured:** adding the sentinel and eviction rungs moved wins
23.3% → 36.7% and moved closures **30.0% → 13.3%**, with enemy on-core heals
0.0923 → **0.5473 per round** — because the sentinel that wins games also pulls
defender bodies onto the ring, where **P6** says they physically block the
barriers (`can_build_barrier` on a body-held seat: **FALSE 40/40**; empty-seat
control **TRUE 383/383**, 1,438 adjacency readings). **The claim is therefore
narrow and falsifiable: under `R1000_IS_DEFEAT` the kill is worth more than the
seal, and the package that trades one for the other beats the incumbent.**

---

## REGISTRATION BLOCK

**TARGET BAND: N/A — local corefill screen with ZERO rated ladder exposure: no submission, no activation, no unrated challenge, so `tools/target_value.py` has no input. Nothing on this page ends in a ship.**
**PINNED: N/A — local self-play against our own ancestor chassis. The opponent version is fixed by construction: the control tree is `bots/_v488beltbreak2` at commit `997bcd42`, git-tracked and working-tree clean at draft, digests quoted under COMMIT PROVENANCE. There is no opponent churn to pin against and no calibration relevance to protect. ⚠ DISCLOSED TWICE, HERE AND ABOVE: the control is NOT the corefill `scratchpad/CONTROL_PIN` tree (`bots/_v468kladturbo`) AND IT IS NOT THE LIVE LADDER HOLDER (that is v160, a teammate's ship). It is deliberately the PROGRAMME INCUMBENT, which is why every share on this page is written `X% vs _v488beltbreak2` and never bare.**
**SURFACE: local**
**CLUSTER UNIT: none** — CLAUDE.md's enumeration PERFORMED, not asserted, over FIVE candidates: (i) **MATCH** — does not exist on this surface: `tools/overnight.sh:138-146` writes one TSV row per `fcode run`, so 1 row = 1 game and no row shares a match with another; (ii) **OPPONENT** — degenerate: all 5,400 rows play the identical control tree, so the pooled stratum holds exactly one opponent and there is no between-opponent variation for a design effect to describe; (iii) **HOST** — killed by REGISTRATION, not measurement: this shard is registered SAME-HOST (LOCAL), and the obligations doc's Addendum 11 rider (the 0.98 exemption is a WITHIN-HOST measurement; cross-host pooling is not covered) makes splitting it across hosts an amendment typed BEFORE the first row; (iv) **SEED** — examined because `overnight.sh:134` advances the seed only every 16 games, so 16 rows share one engine seed. It dies for two reasons: 16 does not divide the 30-game map×seat cycle, so those rows span 8 distinct maps × 2 seats and no two share a map, and `NOISE_ON = True` puts an UNSEEDED `random.Random()` spawn salt in BOTH bots, so two rows at one seed are not even reproducible let alone correlated; (v) **MAP** — examined because this plank is EXPLICITLY map-conditional (its own gate refuses 3 of 15 maps) and map heterogeneity is therefore certain. It is a **STRATUM, NOT A CLUSTER**: the runner cycles all 15 maps × 2 seats before repeating (`overnight.sh:135-137`), so the design is map-balanced by construction at every multiple of 30 and near-balanced at every partial n (at a 400-game stop the three gated maps hold 82 of 400 rows = 20.5% against the balanced 20.0%). A balanced stratum does not inflate the pooled interval. ⚠ **This fifth dismissal governs the POOLED bar only; the per-map and per-segment cuts are sized separately under GATE RESOLUTION.** All candidates die ⇒ DEFF = the measured local constant **0.98** (ρ = −0.020, s39 audit, pair-weighted over 124 shards run by this same runner), i.e. **NAIVE intervals are correct and marginally conservative. The platform constants (1.529 rated / 1.833 unrated) are NOT applicable and importing them would widen every interval here by 24-35% for correlation measured absent.**
**ESTIMATOR: the unweighted pooled treatment game share** = (rows with `winner == T`) / (completed rows), over all 5,400 rows, both seats pooled, all 15 maps pooled, no reweighting. The shard is exactly balanced (15 maps × 2 seats × 180), so the pooled and map-stratified equal-weight shares coincide by construction; the stratified form is an arithmetic consistency check only, never a second estimator (s28 ring-hold: four estimators inside 0.010 of one bar flipped MEET/MISS among themselves). Seat A and seat B shares are reported SEPARATELY as a fixture diagnostic and are never a bar — seat is worth ~7.6pp on byte-identical arms, which is why n is a multiple of 30. **The r1000/core-kill DECOMPOSITION of the share is a MANDATORY companion read on the same rows: it cannot rescue a failed bar and it CAN downgrade a passing one (THIRD FALSIFIER).** ⛔ **The arm-name normalisation hazard applies to any comparator written for this tape: the shard `winner` column holds an ARM DIRECTORY NAME — normalise to US/OPP before scoring, and note that the substring guard at `overnight.sh:76-79` passes here (`_v512ringladder` vs `_v488beltbreak2` do not collide).** Any estimate quoted at readout arrives from `tools/cluster_ci.py` (HEAD); the pre-data half-widths here are closed-form Wald with DEFF 0.98 and their arithmetic is shown inline.
**DOSE: the ring-ladder's own firings, measured on the pre-lock build grid (5 maps × 6 reps × 2 pooled grids, n=60/arm, local `--tle 10`, `NOISE_ON` — the shard's own regime) with the flag `LOKI_FS_RING_LADDER` (doctrine.py:2251) DRIVEN BOTH WAYS: FLAG ON (v512) → raider sentinels built/alive/core-shots 68 / 34 / 2,913 · evictions (≥6-tile dumps) 311 (68.8%) · seats cleared AND barriered 39 · full-seal rounds 879 · orthogonal-8 closures 8/60 · ring deaths per body-round 0.00669 · games with ≥2 sentinels 19/60. FLAG OFF (= `_v511sealonly`, verified byte-equivalent behaviour) at n=30 → 3 / 3 / 84 · 71 evictions (64.8%) · 5 seats · 2,069 full-seal rounds · 9/30 closures · 0.01160 · 0/30 games with ≥2 sentinels. THE ZERO IS NOT A BLIND ZERO: the parent's own flag-off/on pair reads 15 sentinels / 9 evictors / 244 evicts with `LOKI_FS_SEAL_ONLY` False against 0 / 0 with it True, on the same binary, and raider heals 0 vs 67 with two independent instruments agreeing (stderr CLEAR count == replay attack count, 446/446). THE MAP GATE IS ALSO DRIVEN BOTH WAYS: gate ON → 0 siege events on `heart`; a forced OFF-mutant → 94. ⛔ AND THE DOSE'S FIXTURE IS NOT THE SHARD'S FIXTURE: two of the grid's five maps (`atoll`, `heart`) were retired from the pool on 2026-08-13, so the dose was measured on 36 of 60 games' worth of in-pool geometry and NINE of the shard's twelve siege-active maps carry no dose observation at all. ⛔ THE DOSE IS NOT DECODABLE FROM THE SHARD: `overnight.sh:138-139` runs with `--replay /dev/null` and the tape's columns are `ts shard game map seed seat winner cond turns` — no entity, build, position, shot, turret or store information exists on it in either arm, and the runner discards stderr after grepping `Winner:`. Every dose number above is PRE-LOCK and the shard's 5,400 rows lend it none of their power.**
**PLANNED n: 5400 games** (= 15 maps × 2 seats × 180, exact map and seat balance; `tools/overnight.sh:68` has run a 15-map pool since the 2026-08-13 rotation and requires multiples of 30). ⛔ **5400 IS SAID EXPLICITLY because a shard otherwise defaults to a 2700 TARGET, and at 2700 the bar's 1.33pp margin is unreachable against a ±1.89pp half-width.** ⚠ **AND IT IS A PLAN, NOT A FORECAST — see #3: P(reaching it) is 0.000 at every prior this arm supports.**
**BOUNDARY: 5400 games** — LOCAL surface, one tape row is one game; no accept/attempt distinction and no accepts count. ⛔ **A LINE COUNT IS NOT A ROW COUNT**: the tape carries an unprefixed header line under the `# FIXTURE` line, so a naive `wc -l` over-reports n by exactly one. The registered denominator is **DictReader row count over non-`#` lines, cross-checked against the heartbeat's `n TARGET` and against `max(game id) + 1`.** `NOWINNER` rows are counted in n and excluded from the numerator; their count is reported.
**CUT-SHORT: floor 2700 games for the 51.33 BAR verdict.** Below 2,700 completed rows this arm publishes descriptive tallies (share, per-seat, per-map, per-segment, per-class, kill-round, `cond` mix, the r1000/core-kill decomposition) and takes **NO bar verdict**; the one-sample half-width at 2,700 is ±1.89pp, already wider than the 1.33pp margin the bar is built on. ⛔ **AND ON THIS ARM THE SUB-FLOOR BRANCH IS THE MODAL ONE (#3), SO IT IS WRITTEN FIRST, NOT LAST.** An `auto_gate` firing at CATASTROPHE@400, MARK-1000, TREND-FLOOR@1000, COMBO-BAR@2700 or the CI rule at MARK-2700 is an **OPERATIONAL CANCELLATION, not a verdict**, typed `cancellation`; so is a builder cancel-for-capacity (#7). ⭐ **ONE CARVE-OUT, PRE-COMMITTED, AND HERE IT IS THE MODAL BRANCH RATHER THAN THE EXOTIC ONE:** a CATASTROPHE-clause cancellation (95% CI upper < 45.0 at n ≥ 400) is arithmetically INCOMPATIBLE with every band above Band 5, so a stop under that clause DOES license the **Band-5** sentence at the partial n — provided the partial share is disclosed as **selected-pessimistic** (a floor stop fires on a LOW PREFIX DRAW; expect roughly +2pp of regression — side lane s47, n=2 cases, a DIRECTION with a rough size, not a calibrated correction). **THIS IS HOW THE LEG DELIVERS THE MEASUREMENT MAGNUS ASKED FOR: at a ~400-game catastrophe stop the half-width is ±4.5pp (p≈0.30), which decisively excludes parity and cannot resolve a 3pp question — and that is stated as the realistic precision of this leg, in advance.** ⛔ **NO OTHER CLAUSE'S CANCELLATION LICENSES ANY BAND**, and a capacity stop is UNSELECTED and carries no regression caveat at all.
**BAR: 51.33. MDE: 0.00pp — THIS BAR IS A POINT RULE ONLY AND LICENSES NO EXCLUSION CLAIM ABOUT AN EFFECT SIZE** (OB16 corollary, 2026-08-15T03:52:45Z: the standard corefill band IS `50 ± half_width` at n = 5,400, so clearing 51.33 puts the CI's lower edge at exactly 50.00 — it excludes 50 and excludes no positive effect size). n for the one exclusion it CAN make (bar ≠ 50.0): **5,400**, the planned n. ⭐ **The OB16-form statement is available for free on the BAND: Band 1 requires the CI LOWER bound ≥ 51.33, which carries an implied minimum effect of +1.33pp. That is a property of the BAND, not of the BAR, and the two must not be conflated in a readout sentence.** ⚠ **AND THE EXCLUSION THIS LEG WILL ACTUALLY MAKE IS THE ONE AT THE OTHER END: Band 5's `CI upper < 45.0` excludes a 5pp deficit and everything milder, and it resolves at n=400 while the bar does not resolve at 2,700.** **The r300 admission read is the OTHER bar on this page and it IS sized.**
**BASE RATE: 50.00**
**BAR SOURCE:** the house-standard corefill futility band, `50 + 1.96*sqrt(0.25/5400) = 51.33pp`, local DEFF 0.98 so naive — the identical bar carried by `docs/prereg/BARS.tsv` rows `SEALFLOOR6`, `SENTTHR`, `KLADTKILL`, `KLADTURBOR`, `DRAINTURBO`, `KLADLADDER`, `SEALSENTA`, `SEALSENTAN`, `ROUTESCORE`, `BELTBREAK-EARLY`, `BELTBREAK-LATE`, `BELTBREAK2`, `RAYDISC` and `SALTRAY`, which keeps this arm numerically comparable to the family it is screened beside — **and specifically to `SALTRAY`, the other arm run against this same control tonight.** **Constructed, not observed.**
**BASE RATE SOURCE:** structural A/A expectation of a seat-balanced, map-balanced self-play fixture whose control tree IS the treatment's own ancestor chassis. ⚠ **WEAKER HERE THAN ON `SALTRAY` AND SAID SO: the undosed complement is NOT byte-identical** (#7 — the gated-map path is flag-and-state conditioned, not `cmp`-clean), so 50.00 is the structural expectation of the SHIP BEHAVIOUR and not of a proven mirror. Empirically calibrated on the same host and fixture by `IDNULL140` — **49.27% [47.94, 50.60] at n = 5,400** (`results.tsv:idnull140-cert-5400`) — and by `NULL125` — **51.04% at n = 5,400** (`results.tsv:null125-final`). Two A/A cells, one either side of 50.0, both intervals containing it. ⚠ **The two cells are 1.77pp apart**, so a bare clearance in [51.33, 52.4] is a band an A/A cell has already produced — which is why Band 2 is pre-registered as WEAK. **Disclosed before the data.**
**REFERENCE n: none** — the bar's comparator is a STRUCTURAL null of 50.00 generated inside this same shard. ⛔ **The build grid's 22/60 and 12/48 are NOT registered as reference SAMPLES and no bar on this page is sized against them.** They are the honest PRIOR (#1) and are quoted as one; naming them as a reference sample would make the checker size 51.33 as a two-fixture comparison and correctly FAIL it. ⛔ **The incumbent's own 53.09% vs `_v468kladturbo` (`results.tsv:beltbreak2-final`) is likewise NOT a reference here** — different fixture, different opponent, and local screens are not transitive in this repo (QUEUE #65: 3 concordant, 1 not).
**TREATMENT TREE: bots/_v512ringladder**
**TREATMENT DIFF REFS: 001a6aac^ 001a6aac**
⚠ **THE REF PAIR AND ITS LIMITATION, stated rather than left for a certifier.** `001a6aac` is the commit that introduced `bots/_v512ringladder` (all FIVE modules added; `git log --diff-filter=A` returns `001a6aac` for every one of `doctrine.py eco.py main.py raid.py siege.py`), and naming it is what makes the OB13 intersection machine-computable. **But an ADD-commit intersects EVERY path in the tree, so the git check is weak on its own.** The strong form is the CROSS-TREE diff, which git cannot express as a ref pair, and it is reproduced under THE CHANGE with sizes verified at draft: `doctrine.py` 483 changed lines, `main.py` 250, `raid.py` 28, `eco.py` 14, and **`siege.py` 1,983 lines that DO NOT EXIST IN THE CONTROL AT ALL** — `cmp` clean on NONE of the five. Control pinned at `997bcd42`, unchanged since (`git status --porcelain bots/_v488beltbreak2` empty).
**MECHANISM METRIC READS: `bots/_v512ringladder/siege.py:978` — `def _fs_ladder_turn(self, ct, E, p, rnd, needed, orth_open)`, the at-ring priority ladder itself (rung dispatch at `:1034/:1040/:1049`, the in-bot inversion falsifier `_fs_rung` at `:1079`). Companion sites in the same diff, all new and all absent from the control: `bots/_v512ringladder/siege.py:219` — `if sig in FS_MAP_SKIP:`, THE MAP GATE, the single line the whole of this page's pricing rests on; `bots/_v512ringladder/siege.py:1387` — `if LOKI_FS_SEAL_ONLY and LOKI_FS_RING_LADDER and FS_DODGE_ON:`, the reactive dodge; `bots/_v512ringladder/siege.py:494` — `def _fs_body_blocked(self, ct, t)`, where P6 is recorded and where the evict-before-clear rung order becomes engine-correct. TREATMENT DIFF TOUCHES: bots/_v512ringladder/siege.py bots/_v512ringladder/doctrine.py bots/_v512ringladder/main.py bots/_v512ringladder/raid.py bots/_v512ringladder/eco.py. INTERSECTION: yes — every metric site is a NEW LINE in a NEW FILE, the strongest form of the intersection available, needing no import-binding argument (`main.py:41` is `from siege import SiegeMixin`, and the constants bind through `from doctrine import *`). ⚠ A path-only intersection would ALSO pass here and that reading is REFUSED: `grep -c` over the control's four modules returns `LOKI_FS_RING_LADDER` 0 · `FS_MAP_SKIP` 0 · `_fs_rung` 0 · `FS_DODGE_ON` 0 · `_fs_ring_turn` 0 · `LOKI_FERRY_SIEGE_ON` 0, against 17 · 5 · 6 · 5 · 2 · 14 in the treatment — and the file that holds them does not exist in the control. The metric CANNOT read identically in the two arms; it reads structurally 0 in the control. That is the LOKI-18 failure this obligation exists for.**
**METRIC WINDOW: r0-r1000. GATING CONSTANTS: LOKI_FERRY_SIEGE_ON=True, LOKI_FS_SEAL_ONLY=True, LOKI_FS_RING_LADDER=True, FS_MAP_SKIP_ON=True, FS_MIN_MAP_DIM=12, FS_MIN_CORE_DSQ=72, FS_DODGE_ON=True, FS_DODGE_ON_HIT=False, FS_CLEAR_MAX_PECKS=8, FS_AVOID_TURRET_AXIS=True, FS_OPEN_BUILDERS=3, FS_MAX_REPLACE=2, FS_BEAT_STALE=12, FS_PANIC_DMG=24, FS_HOP_DSQ=26, FS_LAUNCHER_TTL=4, FS_NOPROG_RNDS=30, FS_RING_HOLD_DSQ=50, FS_AMMO_TI_FLOOR=8, FS_LOG=False, FS_DRAW_ON=False, NOISE_ON=True. MECHANISM CAN OCCUR IN WINDOW: yes** — **NOT ONE of these is a round gate.** `FS_BEAT_STALE`, `FS_NOPROG_RNDS` and `FS_LAUNCHER_TTL` are round DURATIONS measured from a live event, not thresholds against the absolute round; `FS_MAX_REPLACE`/`FS_OPEN_BUILDERS`/`FS_CLEAR_MAX_PECKS` are counts; `FS_MIN_MAP_DIM`/`FS_MIN_CORE_DSQ`/`FS_HOP_DSQ`/`FS_RING_HOLD_DSQ` are lengths and squared distances; `FS_PANIC_DMG` is hit points; `FS_AMMO_TI_FLOOR` is titanium; the rest are switches. ⭐ **WHAT DOES BOUND THE WINDOW IN PRACTICE, so it is not read as a promise: nothing can fire before the ferry lands a raider at the enemy ring — measured at r4-r15 across the parent's grid and unchanged in this arm — so the observed mass lives in roughly r15-r1000 and r0-r14 is a ferry-only window. That is a property of the chassis, not of these clauses.** ⚠ **DISCLOSED so a green tool run with warnings under it does not launder them: `prereg_check.py` will emit `OBLIGATION 17, PARTIAL WINDOW` warns against the line above and THEY ARE CHECKER ARTEFACTS** — its `check_metric_window` arithmetic reads every declared integer as a ROUND, so a d² of 72, a dimension of 12, a peck cap of 8 and a hop range of 26 all render as *"rounds r0-r<v-1> cannot contain the mechanism"*. The constants are declared anyway. ⛔ **`FS_LOG=False` AND `FS_DRAW_ON=False` ARE DECLARED HERE DELIBERATELY: they are the instrumentation flags of RATIFICATION BLOCKER B1 (#4), flipped OFF by the builder pre-lock (branch ii) so the screened configuration is confound-free; the values above are the FIRED values.**
**PLANK CLASS: OFFENSIVE — a siege package whose entire object is a core kill: a ferry that inserts a raider into the enemy base, a collar that denies the defender its heal seats and spawn tiles, an eviction rung that removes bodies from those seats, and a raider-built sentinel that shoots the enemy core (2,913 core shots over 60 games). It is not a defensive turret purchase, not a home screen, and not an economic plank in the `titanium_collected` sense.** ⭐ **AND THE r300 ADMISSION READ IS REGISTERED ANYWAY, NOT CLAIMED INAPPLICABLE — ON THIS ARM IT IS THE BAR MOST LIKELY TO FAIL.** A collar is a SIEGE: its mechanism is holding a ring for many rounds, the parent held 2,069 full-seal rounds and posted 2/30 r1000 games, this arm posts 5/60, and its own kills-by-r300 rate is **7/60 = 11.7%** against the incumbent's completed-tape anchor of **30.80%**. **A plank whose mechanism is a siege must carry a delay bar whatever its class label.** Registering it is strictly stricter than the programme requires and CANNOT function as a second chance to pass: **both the share bar and the r300 bar must hold.**
**KILL-ROUND NON-REGRESSION: ITT RMST₃₀₀ is the operational estimator (PROGRAMME.md's 2026-08-16T05:36:10Z arbitration, binding on preregs locked from that date — this one is) — mean kill time censored at the r300 horizon over ALL games, a non-kill scoring 300, computed per side on the same rows; scored as an EXCLUSION: the 95% CI UPPER bound on (treatment RMST₃₀₀ − control RMST₃₀₀) must EXCLUDE +5.0 rounds (MDE +5.0; the paired per-game sd is recomputed from THIS tape at readout and the half-width with it — the sibling-family anchor is sd ≈ 89 rounds ⇒ ±2.37 at n=5,400). SECOND REGISTERED FORM, both required: the ITT timely-kill-by-r300 rate (share of ALL games ending `cond == core_destroyed` with `turns <= 300`, denominator every game played, per side) — its 95% CI LOWER bound on (treatment − control) must EXCLUDE a fall of 3.0pp (MDE 3.0pp; sd anchor 75.28pp ⇒ ±2.01pp at n=5,400). THIRD, a DIAGNOSTIC ONLY because it carries a collider: the kill-win-CONDITIONED share and conditioned median — reported beside the two bars, never as either. The treatment's own median kill round crossing 300 is the gross within-arm backstop. ⛔ AND THE RESOLUTION STATEMENT, which is the part that binds on this arm: BOTH FORMS RESOLVE ONLY AT FULL n. At a ~400-game CATASTROPHE stop the half-widths inflate by sqrt(5400/400) = 3.67x to ±8.71 rounds (RMST) and ±7.38pp (timely-kill), against MDEs of +5.0 and 3.0 — NEITHER RESOLVES, and per OB12 the UNRESOLVED gate DEFAULTS TO THE RESTRICTION: no promotion, no ship conversation, no combination claim, regardless of what the share did. ANCHORS, quoted as anchors and not predictions: the build grid read kills <= r300 at 7/60 (treatment) vs 1/30 (parent), and r1000 games at 5/60 vs 2/30; the incumbent's own completed tape (`results.tsv:beltbreak2-final`) reads timely-kill 30.80% [29.56, 32.03] and r1000 share 11.28%. ⚠ ZERO-SUM DISCLOSURE, registered with the bar: on a self-leg the two sides' kill counts partition one set of games, so this difference is CONFOUNDED WITH THE SHARE and a PASS in a winning arm is partly automatic — the bar is a ONE-SIDED BACKSTOP against "wins more, all added wins past r300" and licenses no claim that the arm speeds the kill.**
**PRE-STATE: the predicted-change behaviour is NOT already in the target state at lock.** Verified at draft against the control tree: `grep -c` over `bots/_v488beltbreak2/{doctrine,eco,main,raid}.py` returns **LOKI_FERRY_SIEGE_ON 0 · LOKI_FS_SEAL_ONLY 0 · LOKI_FS_RING_LADDER 0 · FS_MAP_SKIP 0 · FS_DODGE_ON 0 · _fs_rung 0 · _fs_ring_turn 0**, against **14 · (present) · 17 · 5 · 5 · 6 · 2** in the treatment, and the control has **no `siege.py` at all**. **The incumbent has no ferry, no collar, no at-ring ladder, no eviction rung, no raider sentinel, no dodge and no map gate: every builder it produces plays the incumbent raid doctrine on all 15 maps.** ⇒ the behaviour this leg predicts to change cannot already be in the target state. The OUTCOME claim is likewise not pre-satisfied: `_v512ringladder`'s share against the incumbent **does not exist on any tape** (`grep -c RINGLADDER` → 0 on the worklist, `BARS.tsv`, `results.tsv`, `elo_history.tsv` and every shard tape at draft), and every band below — including the sign-reversed ones and the one this page PREDICTS — is a live, pre-named outcome.
**MAP SEGMENT: EXPECTED, AND IT IS NOT AN INFERENCE — IT IS COMPILED INTO THE BOT.** `bots/_v512ringladder/siege.py:206-220` refuses the entire plank on a map whose `(w, h, sorted core anchors)` signature is in `FS_MAP_SKIP`, or whose larger dimension is under `FS_MIN_MAP_DIM = 12`, or whose core separation is under `FS_MIN_CORE_DSQ = 72`. **Registered per OB15a as a WRITTEN-DOWN conditioning fact and, unusually, as a DESIGNED one.** ⛔ **AND THE GATE'S BEHAVIOUR ON THIS POOL IS COMPUTED AT DRAFT, NOT INFERRED AFTER THE DATA:** running that predicate against `maps/*.map26` for the 15 pool maps gives GATED = {`antler` (d²=64), `archipelago` (signature match, shares `snowflake`'s), `fjordgate` (10×10 and d²=32)} and SIEGE-ACTIVE = the other twelve. **Note that only ONE of the three (`archipelago`) is gated by the NEW `FS_MAP_SKIP` set; `antler` and `fjordgate` are refused by the dimension/distance gate the PARENT already carried.** Per-map cells at full n hold 360 games ⇒ half-width **±5.17pp**, so no single map cell can carry a verdict; at a 400-game stop a map cell holds ~27 games ⇒ ±18.9pp, which resolves nothing. Per-map, per-seat and CQ/STD/GRAND tables (`tools/overnight_read.py:76-94 map_area_class`) are computed and reported DESCRIPTIVELY and may not rescue a failed bar.
**PRIMARY SEGMENT: the GATED vs SIEGE-ACTIVE split, fixed BLIND at draft by evaluating the bot's own gate predicate against every map file — GATED = {`antler`, `archipelago`, `fjordgate`} (3 maps, 1,080 games at full n, half-width ±2.98pp); SIEGE-ACTIVE = {`auroraveil`, `drakkarfjord`, `drumlin`, `frostgate`, `glacierkeep`, `icefloe`, `midgard`, `nordkap`, `ragnarok`, `royale`, `valkyrie`, `yulerune`} (12 maps, 4,320 games, ±1.49pp).** ⭐ **THIS SEGMENT IS SHARD-NATIVE AND EXACT, unlike the dose proxies this family has used before: the map is on the tape (`ts shard game map seed seat winner cond turns`) and the gate is a deterministic function of the map, so every row's segment is known without an instrument.** Registered prediction: **the GATED cells read 50.0 ± their own half-width (the plank is switched off there and the bot plays the incumbent chassis), and whatever the package does — in either direction — concentrates entirely on the SIEGE-ACTIVE end.** Exactly one primary; every other cut on this page is DESCRIPTIVE (OB15b).
**EXPECTED DIRECTION: NEGATIVE on the SIEGE-ACTIVE segment (below 50.0, prior 25.0% from the grid's own siege subset); NULL (~50.0) on the GATED segment; therefore NEGATIVE pooled, prior ~30.0%.** ⛔ **THE BAR IS NEVERTHELESS SCORED `ge 51.33` — that asymmetry is deliberate and is the honest shape of a MEASUREMENT leg: the house screen is the instrument, the prediction is the page's own, and the two are allowed to disagree in writing.**
**SEGMENT VALUE CEILING: 80.0% × 38.79pp = 31.03pp** — the SIEGE-ACTIVE segment's maximum contribution to the pooled share. The pairing share is the shard's EXACT map composition (12 siege-active of 15, balanced by construction); the on-segment figure is the **UPPER** 95% Wilson bound on the grid's own siege subset (12/48 = 25.0%, Wilson [14.92, 38.79]). **The GATED complement contributes at most its structural null: 20.0% × 50.00 = 10.00pp. ⇒ POOLED CEILING 41.03pp — BELOW the 45.0 catastrophe threshold and 10.30pp below the 51.33 bar.** ⇒ **the dilution is a HARD CAP: 51.33 pooled would need 51.7% on the siege-active segment, 52.0 (the trend floor) would need 52.5%, and 45.0 (merely escaping the catastrophe brake) would need 43.8% — every one of them ABOVE the upper edge of the segment's own measured CI.** ⛔ **DECLARED LIMITATION OF THIS TOKEN, AND IT CUTS BOTH WAYS: nine of the twelve siege-active maps carry ZERO observation of this tree, so the 12/48 interval describes three maps and is being extrapolated to twelve.** The ceiling is therefore a *ceiling under the assumption that the unmeasured nine behave like the measured three* — which is precisely the assumption this shard exists to test. **A single number cannot honestly express that, and inventing one would be worse than saying so.**
**POOL ERA: post-2026-08-13-rotation** — the 15-map local pool of `tools/overnight.sh:68`. (`check_pool_era` treats this as n/a on a LOCAL surface per SPEC §6; declared anyway so the population is on the page, and because the rotation is load-bearing HERE in a way it usually is not: two of the build grid's five maps are pre-rotation geometry.)
**SPANS-POOL-CHANGE: no** — the shard is fired entirely after the 2026-08-13 rotation, on a single fixed 15-map pool.
**CELL VERSION CHURN: N/A — not a panel, no `CELLS:` line, one fixed local control tree.**
**GATE RESOLUTION: four gates, sized separately.**
* **(a) THE SHARE BAR.** Margin 1.33pp against a one-sample half-width of ±1.334pp at n=5,400, DEFF 0.98 — resolvable at full n, and only just. ⚠ **The slack is ~0.00pp, which is `GUNAXABL`'s exact failure mode (missed its keep edge by 0.0152pp — ONE GAME — on a bar with zero constructed slack). Registered consequence: a result within one game of the bar is reported as "the fixture cannot resolve the question", not as a verdict in whichever direction the rounding falls.** ⛔ **AND IT DOES NOT RESOLVE AT ALL BELOW n=2,700 (±1.89pp), WHICH IS THE MODAL TERMINATION.**
* **(b) THE PRIMARY SEGMENT.** GATED cells at full n: ±2.98pp against a registered prediction of exactly 50.0 — resolves a gross discordance (the grid's 10/12 anomaly, #7) and cannot resolve a 3pp one. At a 400-game stop the gated cells hold ~82 rows ⇒ ±10.8pp — **does not resolve, defaults to the RESTRICTION.**
* **(c) THE r300 ADMISSION BAR.** RMST₃₀₀ MDE +5.0 against ±2.37 and timely-kill MDE 3.0pp against ±2.01pp — both resolve at n=5,400 and **NEITHER resolves at n=400** (±8.71 / ±7.38). Both scored as exclusions, both separated by construction, both UNRESOLVED ⇒ RESTRICTION at any sub-2,700 stop.
* **(d) THE OPERATIONAL FLOORS, AND ON THIS ARM THEY ARE THE GATE THAT DECIDES ITS FATE.** The pinned `tools/auto_gate.py` marks CATASTROPHE (CI-hi < 45.0 at n≥400, `:244,247,815-824`, checked on the running tape rather than a pinned prefix), MARK-1000 / TREND-FLOOR@1000 (prefix < 52.0, `:261`), **COMBO-BAR@2700 (prefix < 55.0, `:278`) — WHICH BINDS, UNEXEMPTED** — and the CI rule at MARK-2700; the bar plausibility guard (`:398-406`, `[30,70]`) admits 51.33. Their firings are OPERATIONAL CANCELLATIONS that free a core, typed `cancellation`, never `verdict`. **The floors bind REMOTE too (`a50f27ef`, s48), so the binding registration is SAME HOST — one host, LOCAL; moving it is an amendment typed BEFORE the first row.** ⛔ **PRICED IN #3: the CATASTROPHE brake is the expected terminator, at 0.37–1.00 depending on the true share, at the first look past n=400.**
**Everything else on this page (F1-F4, D3, D4, the seat / per-map / class splits) is DIAGNOSTIC and cannot rescue a failed bar. Any branch that does not resolve is UNRESOLVED, and an UNRESOLVED gate defaults to the RESTRICTION: no promotion, no ship conversation, no combination claim.**

---

## ⛔ NO COMBO-BAR EXEMPTION IS CLAIMED, AND THE REASONING IS THE MERITS, NOT THE MARKER

`tools/auto_gate.py:906-919` defines the exemption for *"a MECHANISM test scored
against its own additive prediction"*, opted into by the literal token
`COMBO-BAR-EXEMPT` in the BARS source column. **This page DOES NOT claim it, and
`COMBO_BAR = 55.0` BINDS on the n=2,700 prefix.** Three reasons, each sufficient:

1. **THIS TREE IS A GENUINE COMBINATION ON THE MERITS.** Against this control it
   differs in **all four shared modules** (`doctrine.py` 483 diff lines,
   `main.py` 250, `raid.py` 28, `eco.py` 14) **plus an entire 1,983-line module
   that does not exist in the control**, and it stacks **five mechanisms** — the
   launcher ferry, the barriers-only collar, the eviction rung, the raider-built
   sentinel, and the reactive dodge. The `BELTBREAK` solo grants
   (`docs/prereg/BARS.tsv:310,312`) rest on *"this arm is a SOLO plank … not a
   combination"* and **that sentence is simply false here.**
2. **NO ADDITIVE PREDICTION EXISTS TO SCORE AGAINST.** The exemption's registered
   purpose is a mechanism test that can sit ON its own registered target and
   still read under 55. **This arm has registered no additive target** — its own
   grid predicts ~30%, and a token whose premise is absent grants nothing.
3. **THE COMPOSE MARKER IS PRESENT AND IS NOT THE REASON.**
   `bots/_v512ringladder/doctrine.py:2078` carries the literal
   `# ---- composed by tools/stack.py from: turbo (_x3r0v152), bodyaware
   (_v242bodyaware), samestop (_v464samestop)` inherited from the chassis, so
   `combo_of()` will classify this arm COMBO regardless. **The inherited-marker
   classification defect is real; this arm would read COMBO on the merits
   anyway,** which is why the defect changes nothing here.

⚠ **AND IT IS MOOT IN PRACTICE, SAID PLAINLY: the shard will not reach 2,700 at
any prior this arm supports (#3), so the 55.0 gate will never be consulted. The
call is made on the record because the exemption question must be answered
before the fire, not because it will bind.** An escalation to Magnus is available
to the builder; **a self-granted token is not**, and an escalation would have to
argue the opposite of point 1.

---

## ⛔ RATIFICATION BLOCKERS — THREE THINGS THE BUILDER MUST SETTLE BEFORE LOCKING

**B1. ⛔⛔ RULE ON THE INSTRUMENTED TREE, IN WRITING — THIS IS THE ONE THAT CAN
CHANGE THE ANSWER.** `FS_LOG = True` and `FS_DRAW_ON = True` are live in
`bots/_v512ringladder/doctrine.py:2558,2561`, in the treatment only, under a
binding `--tle 10` (#4). **Three defensible branches:** (i) **fire as-is**,
accepting on the record that a Band-4/Band-5 reading cannot separate the plank
from its own instrumentation, and that the build grid embeds the same confound
so the prior does not adjudicate it; (ii) **flip both to `False`, re-digest and
screen THAT tree** — cheap, but it is a different tree from the one the build
report and the demos describe, and the drafting agent may not make it;
(iii) **fire as-is and register a follow-on `LOG-OFF` arm** as the discriminator.
**Firing without choosing is not a branch.** *(Drafter's recommendation, offered
and not decided: (i) plus a one-line disclosure at readout — Magnus asked for the
measurement ASAP and the instrumentation is bounded to one unit's per-round
stderr write; but (ii) is the only branch that removes the confound and it costs
one commit.)*

**B2. STATE WHETHER THE F-READS ARE SATISFIED PRE-LOCK, OR ORDER THE BATTERY.**
This page registers F1-F4 as **SATISFIED BY THE PRE-LOCK BUILD GRID**, because
that grid ran in the shard's own `NOISE_ON` regime at n=60/arm and already
carries all four numbers. ⛔ **BUT ITS FIXTURE IS NOT THE SHARD'S FIXTURE** —
two of five grid maps are retired geometry and nine of twelve siege-active pool
maps are unobserved (#1). **The builder must state on the record that the F-reads
are accepted at that scope**, or order a battery on in-pool maps BEFORE the shard
starts. The FIRINGS-BEFORE-PRIMARY sequence is hard and an amendment after the
fire cannot repair a registration.

**B3. CONFIRM THE SHARD IS SAME-HOST, SERIAL, AND THAT `gate_watch` IS LIVE.**
The registration is LOCAL, SAME-HOST, one core (the core freed by `SALTRAY`).
**What is NOT pre-registered and must be is whether a second worker may be added
mid-run** — it may not, without an amendment typed before the first row
(Addendum 11 rider: the 0.98 exemption is a WITHIN-HOST measurement).
**AND, specific to this arm: confirm the gate watcher actually polls this shard**
(#3) — the whole cost argument for firing a leg priced at P(completion)=0 is that
the CATASTROPHE brake stops it inside ~2 core-hours, and nothing enforces that
automatically.

---

## FIRINGS-BEFORE-PRIMARY — READ AND WRITTEN DOWN BEFORE THE PRIMARY IS TYPED

⛔ **THE RULE IS A HARD SEQUENCE** (`docs/prereg/BARS.tsv` header, research
2026-08-16T13:27:33Z): **F1-F4 are read, and their numbers written down, BEFORE
any sentence containing this arm's primary share is typed.** A primary typed
ahead of the firings read is a REGISTRATION BREACH regardless of what it says,
and the repair is an amendment chain, not a re-write. *(Precedent:
`results.tsv:kladladder-verdict-amendment-f1f2-pending`.)*

⛔ **THE SHARD ITSELF CANNOT SEE THREE OF THE FOUR.** `tools/overnight.sh:138-139`
runs every game with `--replay /dev/null`, the tape's columns are
`ts shard game map seed seat winner cond turns`, and the runner greps `Winner:`
out of a merged `2>&1` capture and discards the rest — **so no entity, build,
position, shot, turret, store or stderr information survives, in either arm.**
F2-F4 come from the PRE-LOCK BUILD GRID and **the shard's rows lend them none of
their power.** F1 alone is shard-native.

* **F1 — THE MAP GATE AND THE POOL COMPOSITION. SHARD-NATIVE AND EXACT.**
  Computed at draft by evaluating the bot's own predicate
  (`siege.py:206-220`) against `maps/*.map26`: **GATED 3 of 15** — `antler`
  (d²=64 < 72), `archipelago` (signature `(26,26,(5,5),(19,19))` ∈ `FS_MAP_SKIP`),
  `fjordgate` (10×10 < 12 **and** d²=32 < 72) — **SIEGE-ACTIVE 12 of 15**.
  Driven both ways at build: **gate ON → 0 siege events on `heart`; a forced
  OFF-mutant → 94.** Read: **the plank is switched off on exactly 20% of this
  shard's rows and that is SHIP BEHAVIOUR, not a fixture defect.**
  **A readout that omits the per-segment table has not performed F1.**
* **F2 — LADDER PRIORITY INVERSIONS. 0 of 732 logged firings.** The in-bot
  falsifier (`_fs_rung`, `siege.py:1079-1104`) re-runs every HIGHER rung's own
  predicate in probe mode after each firing, so an inversion is *"a higher rung
  was legal and funded and we fired a lower one"*. Read: **the ladder that ran is
  Magnus's ladder.** ⛔ **If this were violated, a flat or negative primary would
  be a WIRING result and not a finding about the rung order** — and the shard
  cannot re-check it.
* **F3 — DOSE AT THE RING, FLAG DRIVEN BOTH WAYS, INCLUDING THE ONE COLUMN THAT
  MOVED THE WRONG WAY.** `LOKI_FS_RING_LADDER` ON (n=60) vs OFF (= `_v511sealonly`,
  n=30): sentinels built/alive/core-shots **68/34/2,913** vs **3/3/84** ·
  evictions **311 (68.8%)** vs **71 (64.8%)** · seats cleared AND barriered
  **39** vs **5** · games with ≥2 sentinels **19/60** vs **0/30** · ring deaths
  per body-round **0.00669** vs **0.01160**. ⛔ **AND THE REGRESSION, READ FIRST
  RATHER THAN BURIED: orthogonal-8 closures 8/60 (13.3%) vs 9/30 (30.0%), full-seal
  rounds 879 vs 2,069, enemy on-core heals 0.5473/round vs 0.0923.** Dodge
  configuration is part of this read and was itself chosen on a both-ways n=60/arm
  measurement: ray-trigger ON, HP-drop trigger **OFF** (`FS_DODGE_ON_HIT=False`)
  — hit-trigger 93 deaths / 15 wins / 8 kills≤r300 against ray-only **75 / 17 / 10**,
  every column. Read: **the ladder fires hard and moves every mechanism column;
  the collar is what it spends.**
* **F4 — THE CRASH INVARIANT. 0 tracebacks in 60 games on a 1,983-line NEW
  module.** An escaping exception permanently destroys that unit for the rest of
  the match (`0x1ac5c` → `Game::destroy_entity`), and `siege.py` is the largest
  single block of new code this line has screened. ⛔ **NOT MEASURABLE ON THE
  SHARD — registered as such rather than assumed clean:** stderr is discarded by
  the runner, so a destroyed raider is invisible except as an anomalous r1000
  spike or a `NOWINNER` row. **STOP RULE: any `NOWINNER` row, or an r1000 share
  in the treatment materially above the grid's 8.3%, is an INSTRUMENT ALARM —
  the tape is inspected before any share sentence is written.**

**NOT MEASURABLE on this leg — named, not silently dropped.**
* **FERRY ARRIVALS, THROWS, SEALS, EVICTIONS, SENTINEL BUILDS, PECKS, DODGES AND
  CLOSURES ARE NOT DECODABLE OFF THE SHARD** (`--replay /dev/null`; local
  corefill keeps TAPES, not REPLAYS; stderr discarded).
* **THE FIVE MECHANISMS CANNOT BE SEPARATED ON THIS LEG** (#5). No amount of tape
  reading recovers a decomposition the design does not contain.
* **PER-UNIT CPU / TLE.** Blind zero locally (`get_cpu_time_elapsed()` is a stub;
  0 across 200,633 `BotOutput` events) — labelled **UNINFORMATIVE, NOT CLEAN**,
  and it is exactly the dimension B1 is about.
* **ANYTHING ABOUT THE FIELD.** The opponent is our own chassis. `CLAUDE.md`
  rule 6: **this page closes no road.** In particular, the field-derived
  `FS_MAP_SKIP` set (research's BELT-ON-SEATS survey, 124,536 core-sides) is an
  observation about how the FIELD's sealers behave and this shard does not test
  it — it only tests what our gate does with it.

**D3, D4 — the outcome-shape reads. MEASURABLE, shard-native** (`cond` and
`turns` are on the tape): **D3** = the r300 admission bar, both forms, per side,
off `tools/cluster_ci.py --null`, read with the zero-sum disclosure and the
resolution statement under GATE RESOLUTION (c); **D4** = `cond` mix per arm, the
treatment's own median kill round (crossing 300 is disqualifying), and **the
mandatory r1000/core-kill split of the share** that the THIRD FALSIFIER is
denominated in. Anchors: `results.tsv:beltbreak2-final` timely-kill **30.80%
[29.56, 32.03]**, r1000 share **11.28%**; build grid kills≤r300 **7/60**, r1000
**5/60**.

---

## ⚠ THE LYING-FIXTURE CAVEAT — CARRIED VERBATIM AS AN INTERPRETIVE CONSTRAINT ON THIS WHOLE PAGE

**THIS CONTROL IS A FIXTURE WE WROTE, AND ON THE ONE DIMENSION THIS PLANK
ATTACKS IT IS MEASURABLY UNLIKE THE FIELD.** The plank's entire currency is the
enemy core's collar: whether the defender's heal seats can be sealed and held.
**Local incumbent defence and field defence are not the same problem** — the
field's sealers close the ring at rates the research survey measured down to a
HARD ZERO on some geometry (`lighthouse`: **0 of 347 observed closures**), and
the field's overall clearance of this class of pressure sits at **8.6%**, which
is why `FS_MAP_SKIP` exists at all. **Our own incumbent is a different defender
with different reflexes, and every number on this page is measured against it.**
⇒ **NOTHING ON THIS PAGE — pass, fail, or catastrophe — TRANSFERS TO THE LADDER
WITHOUT A LIVE LEG.** A Band-5 reading does not establish that the ferry-siege
package is bad against real opponents; it establishes that it is bad against
`bots/_v488beltbreak2`. A Band-1 reading would not establish the converse either.
**`CLAUDE.md` rule 6 governs: a refutation without live-game backing is a
hypothesis, not a refutation, and this leg has no live-game backing by
construction.**

---

## FALSIFIER

**PRIMARY FALSIFIER: at n = 5,400 the 95% CI UPPER bound on this arm's pooled
share vs `bots/_v488beltbreak2` falls BELOW 51.33.** That excludes the arm's own
bar on the fixture whose null is structural. ⛔ **AND THIS PAGE PREDICTS THAT IT
FIRES — at the CATASTROPHE end, well before n=5,400.**

**SECOND FALSIFIER (the r300 admission bar, and it can fail alone while the
share passes):** the 95% CI UPPER bound on (treatment − control) ITT RMST₃₀₀
fails to EXCLUDE +5.0 rounds, **or** the CI LOWER bound on the ITT
timely-kill-by-r300 difference fails to EXCLUDE a fall of 3.0pp. **Either is
disqualifying on its own, regardless of the share** — `PLAY_DEFENCE:
not_at_the_kill_s_expense`, and a collar siege is a mechanism that spends
rounds. Read with the zero-sum disclosure attached to the bar, and with the
resolution statement: **at any sub-2,700 stop this falsifier is UNRESOLVED, which
under OB12 defaults to the RESTRICTION and not to a pass.**

**THIRD FALSIFIER (the doctrine composition):** the share gain over 50.00 is
**majority r1000 tiebreak wins**. Then the reading is downgraded one band and
labelled `OFF-DOCTRINE COMPOSITION` — combination input only, no ship
conversation, no head-to-head. **Registered as a falsifier and not a caveat
because this plank's mechanism IS a long hold: the parent posted 2,069 full-seal
rounds, and `R1000_IS_DEFEAT` means a share bought that way is not a win.**

**SEGMENT FALSIFIER:** **the GATED segment (`antler`, `archipelago`, `fjordgate`;
1,080 games at full n) must read 50.0 ± its own half-width (±2.98pp).** The plank
is switched OFF there, so a gated segment far from 50 means the treatment's
NON-siege chassis differs from the control in a way this page has not accounted
for (#7 — the equivalence is flag-and-state conditioned, not byte-verified, and
the grid's `heart` cell already read 10/12). **If the gated segment moves while
the siege-active segment does not, the pooled effect is not coming from the
mechanism this page describes and the reading is ATTRIBUTION UNRESOLVED —
promotes nothing, and refutes nothing, EVEN IF THE BAR CLEARS.** ⚠ **Its power is
declared: at ±2.98pp it catches a gross discordance and cannot resolve a 3pp one;
at a 400-game stop (±10.8pp) it resolves nothing at all** (OB12; the unresolved
case defaults to the restriction).

**MECHANISM FALSIFIER (independent of all of the above, and it fires FIRST):**
* if **F1**'s per-segment table shows the gated maps behaving like siege maps (or
  vice versa), the gate is not doing what the page says and the primary reads
  **NOT MEASURED**, never null;
* if **F4**'s stop rule trips — any `NOWINNER` row, or an r1000 share materially
  above the grid's 8.3% — the tape is inspected for silent unit destruction
  **before any share sentence is written**;
* ⛔ **F2 and F3 cannot be re-read on this leg. If either is later found to have
  been wrong at lock, this shard measured a tree nobody characterised and its
  number is retracted, not reinterpreted.**

### ⭐ THE HONEST-NULL CLAUSE — pre-committed, because the predicted outcome is one of these

| state | evidence | pre-committed reading |
|---|---|---|
| **(1) STOPPED BY THE CATASTROPHE BRAKE** | CI-hi < 45.0 at n ≥ 400 | ⭐ **THIS IS THE PREDICTED BRANCH AND IT IS THE DELIVERABLE, NOT A FAILURE.** Typed `cancellation`; rows KEPT; the partial share disclosed as **selected-pessimistic** (~+2pp expected regression; n=2 cases, a DIRECTION not a correction). **It LICENSES the Band-5 sentence at the partial n** (the carve-out under CUT-SHORT) and licenses nothing else: the r300 bar and the segment falsifier are both UNRESOLVED at that n and default to the RESTRICTION. **The number is what Magnus asked for; the precision is ±4.5pp, and that is stated in advance.** |
| **(2) STOPPED BY TREND-FLOOR@1000 OR COMBO@2700** | prefix < 52.0 @1000 or < 55.0 @2700 | **CANCELLED — UNRESOLVED, defaults to the RESTRICTION.** Rows KEPT; partial disclosed selected-pessimistic. ⭐ **Informative in one narrow way: surviving the catastrophe brake past 400 and dying at the trend floor puts the true share in roughly [42, 52], i.e. ABOVE this page's registered prior and above the ceiling arithmetic — which is itself a finding about the nine unmeasured maps.** |
| **(3) COMPLETED, SHARE FLAT OR NEGATIVE** | n=5,400, CI contains or sits below 50 | ⭐ **A REAL FINDING: the ferry-siege package, in its most developed form, does not beat the chassis it sits on.** It closes the *"the collar just needed the ladder"* reading, which is currently the family's most attractive excuse. **Attribution bound: it does NOT refute P6 (an engine fact), does NOT refute the ferry insertion in isolation, and does NOT price the package against the FIELD (the lying-fixture caveat).** |
| **(4) COMPLETED, SHARE CLEARS, GAIN IS MAJORITY r1000** | F-reads clean, bar clears, decomposition majority tiebreak | ⭐ **ALSO A REAL FINDING, and the shape a collar siege is most likely to produce.** The package delivered SURVIVAL, not KILLING: `OFF-DOCTRINE COMPOSITION`, combination input only, banked as a fact about the mechanism (a held collar buys longevity, not tempo). |

---

## READING, PRE-COMMITTED

**Read TOP-DOWN; the first row whose condition holds is the reading. Rows are
disjoint by construction. Every band is CONDITIONAL on F1-F4 having been read
and written down first, on the r300 admission bar having HELD (or being recorded
UNRESOLVED, which blocks promotion), and on the r1000/core-kill decomposition
having been computed. An r300 failure overrides every row
(`OFF-PROGRAMME — kill delayed`, whatever the share). A majority-r1000
composition DOWNGRADES the row by one and appends `OFF-DOCTRINE COMPOSITION`. A
gated-segment discordance appends `ATTRIBUTION UNRESOLVED` and blocks promotion
in every row.**

| # | band on the pooled share vs `bots/_v488beltbreak2` | pre-committed reading |
|---|---|---|
| **1** | **CI lower ≥ 51.33** | **THE FERRY-SIEGE PACKAGE BEATS THE INCUMBENT.** ⛔ **AND IT WOULD BE THE LARGEST SURPRISE THIS LINE HAS PRODUCED** — the arm's own grid and ceiling arithmetic both exclude it, so the FIRST question at readout is instrument integrity, not celebration. **PROMOTES THE PACKAGE, NOT MAGNUS'S RUNG ORDER** (#5): the next step is the clause-isolation leg `_v512ringladder` vs `_v511sealonly`, then a LIVE unrated leg (the lying-fixture caveat), and only then a ship conversation. Report the size with its OB16 status: the BAR's MDE is 0; clearing this BAND excludes 50.00 AND 51.33, so an implied minimum effect of +1.33pp may be claimed and nothing larger. |
| **2** | **point ≥ 51.33 but CI lower < 51.33** | **REAL-BUT-SMALL, COMBINATION INPUT ONLY.** Pre-registered as WEAK: `NULL125`'s A/A read 51.04 and the two A/A cells are 1.77pp apart. Rows KEPT; no ship conversation; a replication on fresh seeds, same host, is the price of promoting it — **reported SEPARATELY and never pooled** (GUNAXABL/SENTTHR precedent: unregistered pooling is optional stopping with extra steps). |
| **3** | **point < 51.33 AND CI contains 50.0** | **PARITY — THE PACKAGE IS FREE.** Five mechanisms and a 1,983-line module pay for themselves and nothing more. ⭐ **Against the grid's 36.7% that is an UPWARD move and must be reported as such** — with the caveat that the two figures come from different fixtures at different n and the difference is not a registered estimand. Does NOT license a ship. |
| **4** | **CI upper < 50.0 AND CI upper ≥ 45.0** | **THE PACKAGE SUBTRACTS ON OUR OWN CHASSIS.** Attribution bounded: this refutes *the five-mechanism ferry-siege package at this configuration on this map pool against this control*, **not** *P6*, **not** *the ferry insertion*, **not** *the collar as a concept*, and **not** *anything about the field*. ⛔ **AND IT CANNOT SEPARATE THE PLANK FROM ITS OWN INSTRUMENTATION** unless B1 branch (ii) or (iii) was taken. **REGISTERED CONSEQUENCE: the build report's own named lever — a SECOND BODY, because collar and turret compete for one action — is the next arm, not more ladder tuning.** |
| **5** | **CI upper < 45.0** | **THE PACKAGE IS A LARGE NET NEGATIVE ON OUR OWN CHASSIS — THE PREDICTED READING.** Licensed at a partial n by the CATASTROPHE carve-out with the selected-pessimistic disclosure. Same attribution bounds as Band 4, plus: **the closure-vs-kill trade the build report measured (30.0% → 13.3% closures for +13.4pp wins) did not pay on this pool**, and the honest open question the leg leaves is whether the nine unmeasured siege-active maps or the instrumentation confound carry it. ⛔ **A Band-5 reading does NOT retire ferry-siege** — `CLAUDE.md` rule 6, and this fixture is our own chassis. It retires THIS CONFIGURATION as a solo ship candidate and routes the line to the second-body arm. |

⚠ **Nothing here treats 50.0 as a floor, and this page predicts a share far below
it.** The mechanisms that would produce that are pre-named: a raider that spends
1,000 rounds on a ring it cannot close is a `R1000_IS_DEFEAT` game we also
usually lose; the collar regression pulls defender bodies onto the seats where
P6 says they block the very barriers the plank needs; the eviction rung and the
sentinel both compete for the one action a single body has; and 20% of the pool
is played by a chassis that is not byte-identical to the control.

⛔ **AND ONE CROSS-BAND NOTE: an operational cancellation reaches NONE of these
rows EXCEPT via the CATASTROPHE carve-out into Band 5** — a trend-floor,
combo-bar or capacity stop reads `CANCELLED — UNRESOLVED, defaults to the
RESTRICTION`.

---

## THE CHANGE — `file:line`, incumbent → treatment

**TREATMENT `bots/_v512ringladder`** = `bots/_v488beltbreak2` **plus the
ferry-siege stack in five files, one of which is entirely new.** Re-runnable in
five commands (all four shared modules DIFFER; none is `cmp`-clean, which is
itself the honest statement of scope):

```
$ diff bots/_v488beltbreak2/doctrine.py bots/_v512ringladder/doctrine.py | grep -c '^[<>]'   # 483
$ diff bots/_v488beltbreak2/main.py     bots/_v512ringladder/main.py     | grep -c '^[<>]'   # 250
$ diff bots/_v488beltbreak2/raid.py     bots/_v512ringladder/raid.py     | grep -c '^[<>]'   #  28
$ diff bots/_v488beltbreak2/eco.py      bots/_v512ringladder/eco.py      | grep -c '^[<>]'   #  14
$ ls bots/_v488beltbreak2/siege.py                            # does not exist (1,983 new lines)
```

**INHERITED FROM `_v510` (the ferry) AND `_v511sealonly` (the collar):**
`siege.py` — `_fs_gate` :177 (the dimension/distance refusal) · `_fs_park_seat`
:294 area (park on a DIAGONAL, barrier all 8 orthogonals) · `_fs_census` ·
`_fs_body_blocked` :494 · `_fs_ring_turn` (the raider's verb gates) ·
`_fs_try_clear` (peck cap 8 + defer-and-return) · `_fs_stand_target` (turret-ray
blacklist, both turret types) · `main.py` RING/KILL titanium reserves.
`eco.py:373-386` — the collar reserve, gated on `LOKI_FERRY_SIEGE_ON and
FS_COLLAR_RESERVE_ON` **and** on a live `SLOT_FS` ring/kill phase with a fresh
beat. `raid.py:139-145` — `beat &= FS_BEAT_MASK` (the shared-slot layout);
`raid.py:1222-1237` — the launcher hook, placed ABOVE the `self.core is None`
return because a ferry link past the second cannot see our own core.

**NEW IN `_v512ringladder` (Magnus's iteration 3):**
* `doctrine.py:2251` — `LOKI_FS_RING_LADDER` (False restores v511, verified).
* `doctrine.py:2365-2372` — `FS_MAP_SKIP_ON` / `FS_MAP_SKIP`, the closure-based
  skip set keyed on `(w, h, sorted core anchors)` because **no map name reaches
  a bot**. Sourced from research's BELT-ON-SEATS survey (124,536 core-sides).
  ⭐ **`midgard` is deliberately NOT in it** — field sealers close it 18.4% of
  the time and v511's 0/6 has P ≈ 30% under that rate, so a gate fitted to our
  own six games would have closed the one map Magnus watches.
* `siege.py:206-220` — the gate's third clause, `if sig in FS_MAP_SKIP`.
* `siege.py:978-1104` — `_fs_ladder_turn`, the at-ring priority ladder
  (rung 1 barriers → rung 2 evict → rung 3 clear-and-replace → rung 4 second
  sentinel outside the ring), with `_fs_rung` :1079 re-running every higher
  rung's predicate in probe mode after each firing — **the in-bot inversion
  falsifier that produced F2's 0/732**.
* `siege.py:1387-1400` — the reactive dodge, ray-triggered only
  (`FS_DODGE_ON=True`, `FS_DODGE_ON_HIT=False`), sharing the walker's blacklist
  because the two otherwise fight each other (measured: dodge r16, walker puts
  the body back on the ray, dodge r18, dead r19).
* `main.py:479-530` — the KILL-phase reserve floor `max(8, 8 × barrier_cost)`,
  the fix for the first grid's collar-lost-to-its-own-magazine failure
  (**A COLLAR IS WORTH MORE THAN A MAGAZINE**), plus the `FS_SENTINEL_MAX`
  hold-back that funds Magnus's second sentinel once the magazine is half full.

---

## SEEDS, SURFACE, RUNNER

**SEEDS: base 872000**, verified free at draft (see STATUS). `tools/overnight.sh`
advances the seed every 16 games, so a full shard consumes **872000-872337**.
⛔ **Any battery run against this tree must use a base OUTSIDE that range** so no
battery game can collide with a screened game.
**SURFACE: LOCAL, SAME-HOST, one worker** (`WORKERS` unset ⇒ 1).
**RUNNER:** `zsh tools/overnight.sh RINGLADDER bots/_v512ringladder bots/_v488beltbreak2 5400 872000`
— basenames do not collide (`_v512ringladder` vs `_v488beltbreak2`), so the
substring guard at `overnight.sh:76-79` passes (checked at draft).
**GATE:** `tools/auto_gate.py` against the `RINGLADDER` row below, **unexempted**.

---

## READY-TO-PASTE `docs/prereg/BARS.tsv` ROW

*(Tab-separated, four columns: `name`, `bar`, `cmp`, `source`. The builder types
it — BARS row BEFORE the worklist row, per the BELTBREAKR lesson. The worklist
row that follows is
`RINGLADDER<TAB>bots/_v512ringladder<TAB>bots/_v488beltbreak2<TAB>5400<TAB>872000`.)*

```
RINGLADDER	51.33	ge	docs/prereg/PREREG-RINGLADDER-2026-08-17.md — DECISION bar 51.33 ge, POINT RULE (OB16, MDE 0.00), n=5400, h2h share, LOCAL SAME-HOST seeds 872000. Locked <TS> PRE-START by the builder (s50); drafted by a fresh opus agent, judgment lines ratified by the lane. ⭐ FIRED FOR THE MEASUREMENT, NOT FOR A PASS (Magnus, docs/coordination.md:71279): 12 of the 15 pool maps carry ZERO observation of this tree — the build grid ran 5 maps of which 2 (atoll, heart) were RETIRED from the pool on 2026-08-13 — so 80% of these rows are on unmeasured geometry, and THAT is the deliverable. PACKAGE HEAD-TO-HEAD, NOT CLAUSE ISOLATION: TREATMENT bots/_v512ringladder vs CONTROL bots/_v488beltbreak2 — the PROGRAMME INCUMBENT and NOT the live holder (that is v160, a teammate's ship); SELF-LEG, win and loss are the same event, kill-round metrics WITHIN-ARM only. FIVE mechanisms differ (launcher ferry + barriers-only collar + eviction rung + raider sentinel + reactive dodge) across ALL FOUR shared modules (doctrine 483 / main 250 / raid 28 / eco 14 diff lines) PLUS a 1,983-line siege.py absent from the control; a pass promotes the STACK, clause isolation would be vs _v511sealonly and is NOT being run (one core). ⛔ NO COMBO-BAR EXEMPTION CLAIMED AND COMBO_BAR=55.0 BINDS AT 2700: this is a genuine combination on the merits, no additive prediction exists to score against, and the inherited stack.py compose marker (doctrine.py:2078) is not the reason. ⛔⛔ PRICED PRE-FIRE AND THE MODAL OUTCOME IS A CATASTROPHE STOP AT ~400 GAMES (~1.5-2.5 core-hours): the arm's own grid reads 22/60 pooled but 12/48 = 25.0% on siege maps and 10/12 on a RETIRED gated map; the shard's pool is 12 siege-active / 3 gated (antler d^2=64, archipelago in FS_MAP_SKIP, fjordgate 10x10 — computed at draft from maps/*.map26 against the bot's own predicate at siege.py:206-220), giving a composition prior of 0.80x25.0 + 0.20x50.0 = 30.0% and a SEGMENT VALUE CEILING of 0.80x38.79(Wilson hi) + 0.20x50.00 = 41.03pp — BELOW the 45.0 catastrophe threshold and 10.30pp below the bar. P(catastrophe stop at the first look past n=400) = 0.37 to 1.00 across every prior this arm supports; P(reach 5400) = 0.000. THE PREDICTED READING IS BAND 5 AND THE PAGE SAYS SO. ⛔ RATIFICATION BLOCKER B1 RULED BY THE BUILDER (s50, branch ii): FS_LOG and FS_DRAW_ON flipped to False in the screened tree BEFORE lock (doctrine.py:2558,2561) — the confound is REMOVED, not disclosed. They HAD been live under a binding --tle 10, so a Band-4/5 reading cannot separate the plank from its own instrumentation; local CPU is a blind zero (get_cpu_time_elapsed is a stub). FIRINGS-BEFORE-PRIMARY HARD, registered SATISFIED PRE-LOCK: F1 map gate + pool composition (SHARD-NATIVE; gate driven both ways, ON 0 siege events on heart vs OFF-mutant 94), F2 ladder priority inversions 0 of 732 logged firings (in-bot _fs_rung probe-mode falsifier), F3 dose flag-driven-both-ways at n=60 vs n=30 (sentinels 68/34/2913 vs 3/3/84, evictions 311 vs 71, seats 39 vs 5, ring deaths/body-round 0.00669 vs 0.01160) INCLUDING THE REGRESSION READ FIRST (orth-8 closures 8/60=13.3% vs 9/30=30.0%, full-seal rounds 879 vs 2069, enemy on-core heals 0.5473/rnd vs 0.0923), F4 crash invariant 0 tracebacks/60 on a 1,983-line new module — NOT re-readable on the shard (--replay /dev/null, stderr discarded), so a NOWINNER row or an r1000 spike above 8.3% is an INSTRUMENT ALARM. PRIMARY SEGMENT = GATED vs SIEGE-ACTIVE, fixed BLIND at draft and shard-native (map is on the tape, the gate is deterministic in the map): GATED must read 50.0 +-2.98pp at full n or the reading is ATTRIBUTION UNRESOLVED EVEN IF THE BAR CLEARS — the equivalence there is FLAG-AND-STATE CONDITIONED, NOT byte-verified, and the grid's one gated cell read 10/12. THIRD FALSIFIER: a majority-r1000 gain downgrades one band as OFF-DOCTRINE COMPOSITION (a collar siege is the shape most likely to produce it; the parent held 2,069 full-seal rounds). r300 ADMISSION BAR carried on an offensive plank because the mechanism is a SIEGE: ITT RMST300 must EXCLUDE +5.0 rounds and ITT timely-kill must EXCLUDE a 3.0pp fall, either failure disqualifying alone — and BOTH ARE UNRESOLVED below n=2700 (half-widths inflate 3.67x at a 400-game stop), which under OB12 defaults to the RESTRICTION. LOCAL surface: DEFF 0.98, naive intervals, platform constants 1.529/1.833 NOT imported. CLUSTER UNIT none (match/opponent/host/seed dead; MAP is a balanced STRATUM, not a cluster — the runner cycles all 15 maps x 2 seats before repeating, so a 400-game partial holds 82/400 = 20.5% gated against 20.0% balanced). SAME-HOST REQUIRED; adding a worker mid-run needs an amendment typed before the first row. ⚠ LYING-FIXTURE CAVEAT BINDING ON THE WHOLE PAGE: the control is our own chassis and the field's sealers close rings at rates down to 0/347 (lighthouse) with 8.6% clearance overall — NOTHING here transfers to the ladder without a live leg (CLAUDE.md rule 6); a Band-5 reading retires THIS CONFIGURATION as a solo ship candidate and routes the line to the second-body arm, it does not retire ferry-siege. ⭐ CANCEL-FOR-CAPACITY PRE-REGISTERED: if the builder returns the core to other ferry-siege work, that is POLICY AND NOT EVIDENCE — typed cancellation, partial disclosed as UNSELECTED (no selected-pessimistic caveat, unlike a floor or catastrophe stop), licenses no sentence about whether the package pays.
```

---

**PROVENANCE: docs/research/BUILD-REPORT-v512ringladder-2026-08-17.md · docs/research/BUILD-REPORT-v511sealonly-2026-08-17.md · docs/prereg/PREREG-SALTRAY-2026-08-17.md · docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md · PROGRAMME.md · docs/prereg/BARS.tsv**
*Read in full by the drafting agent. Additional facts verified directly against
the repo at draft and cited inline where used:
`bots/_v512ringladder/{doctrine,eco,main,raid,siege}.py`,
`bots/_v488beltbreak2/{doctrine,eco,main,raid}.py`, `maps/*.map26` (the 15-map
pool, parsed for `(w, h, core anchors)` and evaluated against the bot's own gate
predicate), `tools/overnight.sh`, `tools/auto_gate.py`, `tools/prereg_check.py`,
`tools/map_admits.py`, `results.tsv:{beltbreak2-final,idnull140-cert-5400,null125-final}`,
`docs/coordination.md:71279`, and `git ls-files` / `git status --porcelain` /
`git log --diff-filter=A` / `md5` on both arm trees.*

---

## RATIFICATION (builder s50 — the lane types this, per the fresh-drafter rule)

*(B1, B2, B3 to be answered here in writing before the lock commit.)*

---

## RATIFICATION (builder s50, 2026-08-17T20:30:02Z — the lane types this, per the fresh-drafter rule)

**B1 — RULED: BRANCH (ii), flags OFF.** FS_LOG and FS_DRAW_ON flipped to False in the screened
tree in this same lock commit (doctrine.py:2558,2561). A confounded Band-4/5 was the modal
outcome as drafted; the deliverable Magnus asked for is a clean measurement, so the confound is
removed rather than disclosed. The grid-prior-describes-a-different-configuration consequence
is on the page.

**B2 — RATIFIED: F1-F4 accepted at their retired-map scope, on the record.** The build grids
ran 5 maps of which 2 are retired from the pool; the F-reads are mechanism facts about the
tree, not the pool, and the shard's own F1 (gate/pool composition) is shard-native. The F4
crash invariant's shard-side alarm proxy (NOWINNER row or r1000 spike >8.3%) is accepted as
registered.

Drafter judgment calls 1-10: ratified as drafted, with B1 resolved per above. The purpose line
stands: THIS SHARD IS FIRED FOR THE MEASUREMENT — the predicted reading is Band 5 and a
catastrophe stop at ~400 games IS the deliverable, not a failure of the leg.
