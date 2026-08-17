# SCREEN PREREG — `KLADLADDER`: the KLADTK2 sentinel LADDER, cherry-picked onto the uncapped Sleipnir base

Drafted by a fresh opus subagent with no inherited session context beyond the
inputs listed under `PROVENANCE`. The builder lane ratifies the judgment lines
and types the lock commit; this agent wrote no code under `bots/`, appended no
worklist row, appended no `BARS.tsv` row, fired no game, started no shard, and
touched neither `results.tsv` nor `HANDOVER.md` nor `PROGRAMME.md` nor
`QUEUE.md`.

**STATUS: committed BEFORE the `KLADLADDER` row is appended to
`scratchpad/corefill_work.txt`, BEFORE any file named
`scratchpad/overnight/KLADLADDER.*` exists, and BEFORE the leg's first game.**
Two-clock form: this commit's git author time against the shard tape's own
`# FIXTURE … start=` stamp, which `tools/overnight.sh:99` writes BEFORE the
first game (a START, not a first-completed-row). Drafting session wall clock at
write time **`2026-08-17T04:37:42Z`** (`date -u`, same shell call); repo HEAD at
draft `2480152f` (author time `2026-08-17T06:36:50+02:00`). Verified at draft:
`grep -c KLADLADDER scratchpad/corefill_work.txt` → **0**;
`ls scratchpad/overnight/ | grep -i ladder` → **empty**;
`grep -c 810000 scratchpad/corefill_work.txt` → **0** (the seed base is free).

⚠ **The treatment tree ALREADY EXISTS and is committed** (`bots/_v473kladladder`,
added `e6a49fc7`, author time `2026-08-17T06:32:16+02:00`). That is legitimate —
the tree was built and demo-verified before any registration, and its commit
message says in terms *"Not registered, not submitted, no results/BARS/QUEUE
touched"* — but it means this document is **NOT** locked before the arm exists,
only before the arm's first screen row. Said here rather than left for a
certifier to find. It is also what makes Obligation 13's intersection
**computable at lock time** rather than a WARN: see `TREATMENT DIFF REFS` below.

---

## ⛔ READ BEFORE RATIFYING — FOUR THINGS THE LANE OWNS

**1. THE CONTROL IS THE LIVE INCUMBENT, SO 50.0 MEANS "ADDS NOTHING".**
`bots/_v468kladturbo` is Sleipnir v1, shipped 2026-08-16T19:38:40Z and pinned as
the corefill control at `scratchpad/CONTROL_PIN`
(`a9228ccb56ed9a65dd7d72ad1cb96068 bots/_v468kladturbo`). This is therefore a
**direct does-it-ADD contrast**, not a vs-v140 yardstick. Every number on this
page is denominated against the thing we currently ship. **A reader who
transplants a 61-shaped intuition from the KLADTURBO-vs-v140 reads onto this
page has misread the fixture: the same bot measured against itself reads 50.**

**2. THE HYPOTHESIS IS A SUBTRACTION CLAIM FROM s47, AND IT IS FALSIFIABLE HERE.**
`results.tsv:464` (KLADTK2R, n=4,880, 53.07% [51.67,54.47] on ws1) sits ~8.5pp
below KLADTURBOR's 61.57 on the same host against the same control, and
`results.tsv:461` (KLADTK2, local, 51.77% at n=1,159) agrees in direction. The
registered s47 reading was *"the cap subtracts more than the ladder pays;
cherry-pick the LADDER without the CAP as the next iteration."* **This leg is
that cherry-pick and it is the only way to tell "the cap was the whole problem"
from "the four-plank was the whole problem".** If the ladder alone also fails to
clear the band, the s47 attribution to the CAP is wrong and BOTH halves of the
four-plank are dead — which is a road closed, not a wasted shard.

**3. THE SHARD TAPE CANNOT SEE THE MECHANISM, AND A FIRINGS READ IS MANDATORY
BEFORE THE PRIMARY.** `tools/overnight.sh:138-139` runs every game with
`--replay /dev/null`, and the tape's columns are
`ts shard game map seed seat winner cond turns` — **no entity, build, or turret
information exists on it, in either arm.** The plank's mechanism is CONDITIONAL
(an eco-gated branch plus a waived floor), so `docs/prereg/BARS.tsv`'s
FIRINGS-BEFORE-PRIMARY rule (adopted 2026-08-16T13:27:33Z) binds: **a
firings-per-game read is registered below as F1/F2 and must be read BEFORE the
primary is typed.** It runs on a SEPARATE serial battery that keeps replays
(`tools/dose.py --kind sentinel`, decoder `tools/fwd_read.py`), never off the
shard tape. **What the tape CAN answer is the kill-round question** (`cond`,
`turns`), and that is why D1/D2 below are shard-native and F1/F2 are not.

**4. THE BAR SITS INSIDE THE A/A SPREAD OF THIS FIXTURE, AND THAT IS A REAL
LIMITATION, NOT A FORMALITY.** The house band 51.33 is the smallest bar a
5,400-row local shard can separate from 50.0 at 95%. But the two banked A/A
calibrations on this fixture read **IDNULL140 49.27% [47.94,50.60]** (n=5,400,
2026-08-16, same host, `results.tsv:454`) and **NULL125 51.04%** (n=5,400,
`results.tsv:346`) — i.e. a byte-identical pair has already landed **0.29pp
below the bar** once. ⇒ **A result in [51.33, 52.4] is a BAR-CLEARING result that
an A/A cell has already produced.** The prereg's response is not to move the bar
(it would become unresolvable) but to pre-commit the reading: see
`READING, PRE-COMMITTED` — a bare clearance in that band is registered in
advance as *weak, not confirmatory*, and it does not on its own license a ship
conversation.

---

## RATIFY: Hypothesis

**The eco-gated forward-sentinel commitment (`LOKI_LADDER_ON`), lifted from
`_v472kladtk2` onto the UNCAPPED `_v468kladturbo` base with no harvester budget,
raises our LOCAL pooled game share against `bots/_v468kladturbo` itself to
51.33% or higher at n = 5,400 games across all 15 corefill maps and both seats.**

**The mechanism claim, stated so it can be wrong:** the ladder does two opposite
things and the hypothesis is that the first outweighs the second.
* **It ACCELERATES the first two forward sentinels** — below the committed live
  target the plant takes the base's own step-3 slot AND the 40-Ti reserve floor
  is waived (`raid.py:770`), so a plant lands at a bank the base refuses.
* **It DEMOTES the third** — at or above target the plant drops to a NEW
  opportunistic step 8, after peck and salt, so the base is strictly more
  aggressive about sentinel #3 than the treatment is.
* **It REPLANTS** — the target is compared against the LIVE census
  (`_live_fwd_guns`), so a sentinel death re-arms priority and the waiver.
  ⚠ The base ALSO replants (its step-3 attempt is unconditional and its cap is
  live-census-based when `LOKI2B_LIVE_CAP_ON`), so **"self-healing" is NOT a
  treatment-only behaviour** and must not be reported as one. What is
  treatment-only is the *priority slot* and the *waived floor* while live <
  target.

**⇒ A flat result is INFORMATIVE here and is not a null about "sentinels".** It
would say the acceleration and the demotion cancel, which is a different finding
from "the ladder does nothing".

---

## REGISTRATION BLOCK

**TARGET BAND: N/A — local corefill screen with ZERO rated ladder exposure: no submission, no activation, no unrated challenge, so `tools/target_value.py` has no input. Nothing on this page ends in a ship; the only branch that reaches the ladder is a later, separately-registered head-to-head against the holder.**
**PINNED: N/A — local self-play. The opponent version is fixed by construction: the control tree is `bots/_v468kladturbo` at the commit this shard runs from, pinned at `scratchpad/CONTROL_PIN` (`a9228ccb56ed9a65dd7d72ad1cb96068 bots/_v468kladturbo`). There is no opponent churn to pin against and no calibration relevance to protect.**
**SURFACE: local**
**CLUSTER UNIT: none** — CLAUDE.md's enumeration PERFORMED, not asserted: (i) the **MATCH** cluster does not exist on this surface — `tools/overnight.sh` writes one TSV row per `fcode run`, so 1 row = 1 game and no row shares a match with another; (ii) the **OPPONENT** cluster is degenerate — every one of the 5,400 rows plays the identical control tree, so the pooled stratum holds exactly one opponent and there is no between-opponent variation for a design effect to describe. Both clusters die ⇒ DEFF = the measured local constant **0.98** (pair-weighted, ρ = −0.020, 124 shards, s39 audit), i.e. naive intervals are correct and marginally conservative. **The platform constants (1.529 rated / 1.833 unrated) are NOT applicable and applying them would widen every interval here 24-35% for correlation that has been measured absent.**
**ESTIMATOR: unweighted pooled treatment game share** = (rows with `winner == T`) / (completed rows), over all 5,400 rows, both seats pooled, all 15 maps pooled, no reweighting. Seat A and seat B shares are reported SEPARATELY as a fixture diagnostic and are never the bar — seat is worth ~6.8pp on byte-identical arms, which is why the n is a multiple of 30.
**DOSE: forward-sentinel plants at a bank inside the reserve floor — treatment 1 vs flag-off control 0 (n=4 unit-probe cells, both verdicts driven: with the bank BELOW sentinel cost both arms stay refused at zero, and with `LOKI_LADDER_ON=False` the treatment reproduces the control in every cell; unit probe recorded in commit `e6a49fc7`).**
**PLANNED n: 5400 games** (= 15 maps × 2 seats × 180, so map and seat balance is exact; `tools/overnight.sh:66` has run a 15-map pool since the 2026-08-13 rotation and its own comment requires multiples of 30).
**BOUNDARY: 5400 games** — LOCAL surface, one tape row is one game; there is no accept/attempt distinction on this fixture.
**CUT-SHORT: floor 2700 games.** Below 2,700 completed tape rows this leg publishes descriptive tallies (share, per-seat, per-map, kill-round) and takes **NO comparative look and no bar verdict**; the half-width at 2,700 is ±1.87pp, already wider than the 1.33pp margin the bar is built on, so a sub-2,700 read cannot resolve its own branches. An `auto_gate` cancellation at MARK-400 or MARK-1000 is an OPERATIONAL STOP, not a verdict, and is typed `cancellation` per the SEALQ disclosure.
**BAR: 51.33**
**BASE RATE: 50.00**
**BAR SOURCE:** house-standard corefill futility band, `50 + 1.96*sqrt(.25/5400) = 51.33pp`, local DEFF 0.98 so naive — the identical bar carried by `docs/prereg/BARS.tsv` rows `SEALFLOOR6`, `SENTTHR`, `KLADTKILL`, `KLADTK2`, `KLADTURBOR` and `DRAINTURBO`, which is what keeps this cherry-pick numerically comparable to the four-plank reads it exists to explain. **Constructed, not observed.**
**BASE RATE SOURCE:** structural A/A expectation of a seat-balanced, map-balanced self-play fixture whose control tree is the treatment's own base. Empirically calibrated by `IDNULL140` — **49.27% [47.94,50.60] at n=5,400**, 2026-08-16T18:02:04Z, same host and fixture (`results.tsv:454`, `scratchpad/overnight/IDNULL140.tsv`) — and previously by `NULL125` — **51.04% at n=5,400** (`results.tsv:346`). Two A/A cells, one either side of 50.0, both intervals containing it.
**POOL ERA: post-2026-08-13-rotation** — the 15-map local pool of `tools/overnight.sh:66`. (`check_pool_era` treats this as n/a on a LOCAL surface per SPEC §6; declared anyway so the population is on the page.)
**REFERENCE n: none** — the comparator is generated inside this same shard from the same 5,400 seeds; there is no fixed external reference sample, so no resolution floor at n→∞.
**TREATMENT TREE: bots/_v473kladladder**
**TREATMENT DIFF REFS: e6a49fc7^ e6a49fc7**
**MECHANISM METRIC READS: bots/_v473kladladder/raid.py:315 — the `fwd_priority = fwd_live_n < fwd_target` decision, the single line that selects between the prioritized (step 3, floor waived) and opportunistic (step 8, floor applied) plant slots; observed as F1 (forward-sentinel builds per game and the round of the first) and F2 (builds after the first forward-sentinel loss), both decoded off replay wire by `tools/fwd_read.py`, never from `print()`. TREATMENT DIFF TOUCHES: bots/_v473kladladder/raid.py bots/_v473kladladder/doctrine.py. INTERSECTION: yes — line 315 is inside the block the diff ADDS at 266-323, it did not exist in the control at all, and its two consumers at lines 359 and 445 of the same file are the other half of the same hunk. The metric cannot read identically in both arms because the control has no `fwd_target` to compare against.**
**METRIC WINDOW: r0-r1000. GATING CONSTANTS: LOKI_FWD_MIN_HARV=2, LOKI_LADDER_POST_HARV=3, LOKI_FWD_GUN_CAP=3, LOKI2_RUSH_RND=60. MECHANISM CAN OCCUR IN WINDOW: yes** — the PRE rung arms at 2 harvesters BUILT and the POST rung at 3, both reached in the first ~30 rounds of every demo game (first forward sentinel r16-r61 across 12/12 ladder demo games, commit `e6a49fc7`); no round floor gates the ladder at all, and `LOKI2_RUSH_ON=False` so the rush relaxation is inert in both arms. The window is the whole game because a REPLANT can occur at any round — the icefloe demo's last plant was r133.
⚠ **DISCLOSED, because a green tool run with four warnings under it is how a warning stops being read: `prereg_check.py` emits four `OBLIGATION 17, PARTIAL WINDOW` warns against this line and ALL FOUR ARE ARTEFACTS OF THE CHECKER, not defects in the window.** Three of the declared constants (`LOKI_FWD_MIN_HARV=2`, `LOKI_LADDER_POST_HARV=3`, `LOKI_FWD_GUN_CAP=3`) are HARVESTER AND TURRET COUNTS, and the checker's `_inert`/partial-window arithmetic reads every declared integer as a ROUND — so it reports "rounds r0-r2 cannot contain the mechanism" from a harvester count of 3. The fourth, `LOKI2_RUSH_RND=60`, IS a round but is inert in both arms because `LOKI2_RUSH_ON=False`. They are declared anyway because they are the constants that actually gate the ladder, and an undeclared gate is the failure the obligation exists for; the warns are answered here rather than left for a certifier to re-derive.
**GATE RESOLUTION: the shard is governed by the pinned `tools/auto_gate.py` marks (n≥400 CATASTROPHE if the 95% CI upper < 45.0; n≥1000 STOP if the CI upper < 51.33; TREND-FLOOR@1000 if the first-1000 prefix share < 52.0). Those are OPERATIONAL CANCELLATIONS that free a core — they are typed `cancellation`, never `verdict`, and they license NO exclusion claim because the registered target is 5,400. The RESOLVABLE gate this document owns is the primary at full n, whose margin (1.33pp) exceeds its own half-width (±1.32pp) by 0.01pp — i.e. it is resolvable, and only just. Everything else on this page (F1, F2, D1, D2, the seat and map splits) is DIAGNOSTIC and cannot rescue a failed primary. Any branch that does not resolve is UNRESOLVED, and an UNRESOLVED gate defaults to the RESTRICTION: no promotion, no ship conversation, no combination claim.**
**PRE-STATE: the predicted-change set is NOT already in the target state at lock.** Verified at draft against the control tree: `grep -c LOKI_LADDER_ON bots/_v468kladturbo/*.py` → **0 in every file**; `diff -rq` names exactly two differing `.py` files (`doctrine.py`, `raid.py`) and `cmp` confirms `eco.py` and `main.py` are **byte-identical**. The control has no committed sentinel target, its step-3 plant attempt is unconditional, its reserve floor `LOKI_FWD_TI_FLOOR=40` is never waived, and it has no step-8 slot. The three behaviours this leg predicts to change therefore cannot already be in the target state.
**MAP SEGMENT: none expected** — the primary is the POOLED share over all 15 maps and both seats. The plank is gated on a HARVESTER COUNT, not on terrain, and because the base's economy is uncapped the counter rises past both rungs on every map (4-14 harvesters/game across the three demo maps); the arming DELAY differs by ore spread but the arming itself does not. **No map cut may rescue this arm.** Per-map shares WILL be printed at readout as exploratory description — they are not a segment, they carry no pre-registered direction, and nothing may be banked off them without a fresh prereg.
**CELL VERSION CHURN: N/A — not a panel, no `CELLS:` line, one fixed local control tree.**

---

## FALSIFIER

**PRIMARY FALSIFIER: at n = 5,400 the 95% CI UPPER bound on the treatment's
pooled game share falls BELOW 51.33.** That excludes the bar, and it says the
sentinel ladder does NOT add measurably to Sleipnir. **Consequence, registered in
advance: the s47 KLADTK2R cherry-pick hypothesis — "the cap subtracts, the ladder
pays" — is DEAD**, and with it the four-plank family: the cap already read as a
subtraction, and the remaining half would then have failed on the base it was
supposed to help. The row closes and no further klad-ladder variant is queued
without a new mechanism, not a new tuning.

**MECHANISM FALSIFIER (independent of the primary, and it can fire first):** if
F1 shows the treatment's forward-sentinel builds per game are within noise of the
control's AND the round of the first forward sentinel is within noise, then the
plank did not deliver its dose in the screen fixture and **the primary is
uninterpretable in either direction** — a flat share would mean "the mechanism
never fired", not "the mechanism fired and did not pay". Per the
FIRINGS-BEFORE-PRIMARY rule this must be read BEFORE the primary is typed, and if
it fires the primary is reported as NOT MEASURED rather than as a null.

---

## READING, PRE-COMMITTED — three bands, written before the data

Registered now so no band is chosen after the fact.

| band at n=5,400 | pre-committed reading |
|---|---|
| **CI lower ≥ 51.33** | **THE LADDER ADDS.** Real and resolved on this fixture. Promotes to a combination input and to a separately-registered head-to-head against the holder. Report the size honestly: the s47 four-plank deficit was ~8.5pp, so a +1 to +3pp ladder does not by itself explain that gap and the CAP remains the dominant term. |
| **point ≥ 51.33 but CI lower < 51.33** (includes the whole [51.33, 52.4] window an A/A cell has already produced) | **REAL-BUT-SMALL, COMBINATION INPUT ONLY.** Registered in advance as WEAK: `NULL125`'s byte-identical A/A read 51.04, so a bare clearance in this band is not distinguishable from fixture noise by this leg alone. Rows are KEPT and the arm is available for combination; it does NOT license a ship conversation, and a replication (cross-host or fresh seeds) is the price of promoting it. |
| **CI includes 50.0** | **THE LADDER ADDS NOTHING MEASURABLE.** The plank's acceleration and its step-8 demotion cancel, or neither binds. Combination input only if some other arm supplies a mechanism reason; otherwise the row closes with the primary falsifier's consequence above. |
| **CI upper < 51.33** | Primary falsifier fires — see above. |

⚠ **50.0 is not a floor: a share BELOW 50 is a live outcome and would say the
ladder SUBTRACTS from Sleipnir** — the step-8 demotion of sentinel #3 is a
plausible mechanism for exactly that, and it is pre-named here so a negative is
not explained away as noise.

---

## MECHANISM DIAGNOSTICS TO READ AT READOUT

**Measurability is declared per metric. `NOT MEASURABLE` is written where it is
true, rather than a metric being quietly renamed into something the tape happens
to carry.**

### F1, F2 — the FIRINGS read. MEASURABLE, but NOT off the shard tape.
`tools/overnight.sh:138-139` passes `--replay /dev/null`, so the KLADLADDER shard
produces **no** entity events. F1 and F2 therefore run on a **separate serial
battery** — `tools/dose.py bots/_v473kladladder --kind sentinel --ctrl
bots/_v468kladturbo`, both seats, replays kept, decoded with `tools/fwd_read.py
decode` (which carries the rotate-re-emit guard and the last-tracked-position
death classification). **Registered size: 120 games (15 maps × 2 seats × 4
seeds), serial, ~1 core-hour, run BEFORE the primary is typed.** Serial and not
parallel per `tools/dose.py`'s own D65 finding.

* **F1 — DOSE DELIVERY.** Forward-sentinel builds per game, and the round of the
  FIRST forward sentinel, treatment vs control. **Pre-registered expectation:
  treatment's first sentinel arrives EARLIER (the waived floor) and its
  builds/game are ≥ control's.** Demo anchor, reported as an anecdote: r16-r61
  across 12/12 ladder demo games (`e6a49fc7`).
* **F2 — REPLANT RATE.** Builds occurring after the first friendly
  forward-sentinel removal, per game. **Pre-registered expectation: a positive
  difference that is SMALL**, because the control replants too — this is the
  metric where the naive "self-healing is treatment-only" reading is wrong, and
  F2 exists to keep the readout from making it.

### D1, D2 — the kill-round read. MEASURABLE, shard-native.
`cond` and `turns` are on the tape.

* **D1 — TIMELY-KILL RATE (the `DEFENCE_ADMISSION_BAR` primary).** Share of ALL
  treatment-seat games ending `cond == core_destroyed` with `turns ≤ 300`,
  treatment vs control, both computed on the same 5,400 rows. **Non-regression is
  the bar and it is stated as an EXCLUSION, per CLAUDE.md's fail-to-exclude
  clause: the 95% CI on the difference must EXCLUDE a fall of more than 2.0pp.**
  A "no significant rise" phrasing is not admissible here.
* **D2 — MEDIAN KILL ROUND**, treatment vs control, as the gross backstop
  (median crossing 300 is disqualifying). Reported alongside the r1000 rate, since
  `R1000_IS_DEFEAT` makes an r1000 share a cost even when the tiebreak is won.
  Anchor: KLADTURBO's own local full read had median kill 193 vs the v140
  control's 240 (`results.tsv:466`).

### NOT MEASURABLE on this leg — named, not silently dropped.
* **The live forward-sentinel census over time** (whether the committed target of
  2 is actually HELD, round by round). `fwd_read.py` gives builds and deaths but
  the standing occupancy series is not decoded by any shipped tool, and building
  one is out of scope for this screen.
* **Which of the two sub-mechanisms carries the effect** — the waived floor
  (acceleration) vs the step-8 demotion (deceleration of sentinel #3) — is
  **NOT SEPARABLE** by this leg. They ship in one flag. Separating them needs two
  further arms (`fwd_waive` alone, `fwd_priority` alone) and the tree already
  splits the flags for exactly that; it is NOT attempted here and no readout
  sentence may attribute the result to one half.
* **Per-unit CPU** — local replays zero-fill `execTimeUs`, so no timing claim is
  available. The demo's "0 TLE turns in 27 games" is the only CPU evidence and it
  is an anecdote.
* **Seed determinism** — `NOISE_ON` pins an unseeded RNG, so base-vs-base at one
  seed diverges at round 0 (measured, `e6a49fc7`). **No seed-matched or
  replay-diff equivalence claim is available on this fixture, and the flag-off
  base-equivalence claim is made on the CODE plus the unit probe, never on a
  replay comparison.**

---

## THE CHANGE — `file:line`, control → treatment

**TREATMENT TREE: `bots/_v473kladladder`** — byte-for-byte `bots/_v468kladturbo`
apart from two files. Verified at draft: `diff -rq` names exactly `doctrine.py`
and `raid.py`; `cmp` confirms `eco.py` and `main.py` are **byte-identical**
(`__pycache__` entries are build artefacts, not source).

**(1) `doctrine.py` +1267-1328** — one new comment block and four constants:
`LOKI_LADDER_ON = True`, `LOKI_LADDER_POST_HARV = 3`,
`LOKI_FWD_SENT_MIN_PRE = 1`, `LOKI_FWD_SENT_MIN_POST = 2`.

**(2) `raid.py` +266-323** — the ladder decision inside `_raid_act`: hoist the
live forward-sentinel census once per turn, compute `fwd_target` (0 below the
plant-legality threshold, PRE=1 from there, POST=2 at ≥3 harvesters BUILT), and
derive `fwd_priority`/`fwd_waive` from it. **Line 315 is the metric's read
point.**

**(3) `raid.py:359`** — step 3 becomes `if fwd_priority and
self._try_forward_sentinel(ct, E, live=fwd_live, waive_floor=fwd_waive)`.

**(4) `raid.py:445`** — a NEW step 8, `if not fwd_priority and
self._try_forward_sentinel(ct, E, live=fwd_live)`, after peck and salt.

**(5) `raid.py:728,770`** — `_try_forward_sentinel` gains `live` and
`waive_floor` parameters; `if waive_floor: ti_floor = 0`.

**ZERO CAP RESIDUE, verified at draft:** `LOKI_HARV_CAP` occurs **three times in
`bots/_v473kladladder/doctrine.py` and all three are inside COMMENTS** explaining
the deliberate non-port (lines 1270, 1293, 1946); `_my_harv` occurs **zero
times** anywhere in the tree. There is no executable harvester budget, and
`eco.py` is the base's.

---

## WHAT THIS LEG COSTS AND WHAT IT DOES NOT

**Cost: one local core to n=5,400, plus ~120 serial games for F1/F2.** ZERO
rated ladder exposure, zero submissions, zero unrated challenges — nothing on
this page touches the platform, which is why `TARGET BAND` is N/A rather than a
number.

**It does NOT decide a ship.** The strongest branch on this page promotes the arm
to (a) a combination input and (b) a separately-registered head-to-head against
the live holder, which is the pipeline step Magnus's procedure names verbatim
(*"we start by testing it against the current slot, If it beats it we can
switch"*) and which `SLEIPH2H` is the template for. **A local screen against the
incumbent is gate 1; gate-1-to-gate-2 transitivity is UNVALIDATED in this repo
(QUEUE #65: 3 concordant, 1 not), so the head-to-head is not skippable on the
strength of this number.**

---

**PROVENANCE:** `docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md` · `docs/research/SPEC-prereg-check-2026-08-14.md` (read in full: the token table, the DEFF constants, the five published half-widths, §5's five resolutions) · `docs/research/SPEC-prereg-check-side-lane-checks-2026-08-14.md` · `docs/research/SPEC-metric-window-2026-08-15.md` · `docs/research/RULING-prereg-check-vocabulary-2026-08-14.md` · `docs/builder-method.md` · `docs/prereg/SCREEN-homeearly-2026-08-15.md` (house template, most recent full-shape local screen) · `docs/prereg/BARS.tsv` (bar registry header, the FIRINGS-BEFORE-PRIMARY rule, and the sibling klad-family rows) · `docs/prereg/RULE-futility-gates-2026-08-13.md` · `CLAUDE.md` · `tools/prereg_check.py` (read for the required tokens, `RULES`, `check_arithmetic`, `check_metric_window`, `check_pool_era`, `git_diff_paths`, and the `COMPLETE` selftest fixture) · `tools/auto_gate.py` (the pinned stopping rule and the registered false-kill rates) · `tools/overnight.sh` (the 15-map pool at :66, the `--replay /dev/null` at :138-139, the START stamp at :99) · `tools/corefill.sh` · `tools/dose.py` · `tools/fwd_read.py` · `tools/corpus/replay_builds.py` · `bots/_v473kladladder/raid.py` · `bots/_v473kladladder/doctrine.py` · `bots/_v468kladturbo/raid.py` · `bots/_v468kladturbo/doctrine.py` · `scratchpad/corefill_work.txt` · `scratchpad/CONTROL_PIN` · `scratchpad/overnight/BODYAWR.tsv` (tape schema only) · `results.tsv` (rows 346 `null125-final`, 454 `idnull140-cert-5400`, 458 `kladtkill-autostop-400`, 461 `kladtk2-autostop-1000`, 464 `kladtk2r-partial-4880`, 465 `drainturbo-autostop-2700`, 466 `kladturbo-local-confirm-5400`) · git commit `e6a49fc7` (the arm tree's add and its demo record) · `git diff --name-only e6a49fc7^ e6a49fc7` · the drafting brief supplied by the builder lane s48. No file under `bots/`, `tools/`, `scratchpad/`, `docs/prereg/BARS.tsv`, `results.tsv`, `HANDOVER.md`, `PROGRAMME.md` or `QUEUE.md` was created or modified by this agent, and no game was run.
