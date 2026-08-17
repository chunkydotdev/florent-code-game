# SCREEN PREREG — `KLADLADDER3`: the UNTESTED MIDDLE of the funding ladder (`LOKI_FWD_TI_FLOOR` 40 → 16)

Drafted by a fresh opus subagent with no inherited session context beyond the
inputs listed under `PROVENANCE`. The builder lane ratifies the judgment lines
and types the lock commit; this agent wrote no code under `bots/`, appended no
worklist row, appended no `BARS.tsv` row, fired no game, started no shard, and
touched neither `results.tsv` nor `HANDOVER.md` nor `PROGRAMME.md` nor
`QUEUE.md`.

**STATUS: committed BEFORE the `KLADLADDER3` row is appended to
`scratchpad/corefill_work.txt`, BEFORE any file named
`scratchpad/overnight/KLADLADDER3.*` exists, and BEFORE the leg's first game.**
Drafting session wall clock at write time **`2026-08-17T07:12:01Z`** (`date -u`,
same shell call); repo HEAD at draft `12e71962` (author time
`2026-08-17T09:10:53+02:00`). Verified at draft:
`grep -c 'KLADLADDER3' scratchpad/corefill_work.txt` → **0**; same grep on
`docs/prereg/BARS.tsv` → **0**; `ls scratchpad/overnight/ | grep -i kladladder3`
→ **empty**; `grep -cE '830000' scratchpad/corefill_work.txt` → **0** (the seed
base is free; the highest local seedbase currently in any worklist is 826000).

### SECOND CLOCK — two-clock form, primary and backstop both named now

**PRIMARY: this commit's git author time against the `# FIXTURE … start=` stamp
that `tools/overnight.sh:103` writes as the first line of
`scratchpad/overnight/KLADLADDER3.tsv` (its `START=` is computed at `:99`),
before the first `fcode run`, on any tape that does not already exist.**
**BACKSTOP, registered now so no judgement is made later:** if the tape carries
`# FIXTURE-RESUME … start=UNKNOWN-legacy-tape` (`tools/overnight.sh:110`), no
`# FIXTURE` line at all, or the shard is routed to a REMOTE worker (whose tapes
carry no stamp), the second clock is **the `ts` of the FIRST COMPLETED ROW** —
conservative by construction, since the true start is strictly earlier.

⚠ **The treatment tree ALREADY EXISTS and is committed** (`bots/_v485kladladder3`,
added `e9e40548`, author time `2026-08-17T07:53:59+02:00`), and **so has its dose
battery** (n=160, `scratchpad/kladladder3_dose.log`, per-game TSV
`scratchpad/dose_v485.tsv`, 160 rows, completed 07:58). Under the obligations
doc's Obligation 1 both are **OBSERVABLE-AT-LOCK and are NEVER presented as
pre-registered.** Every number they produced is reprinted below as a PRIOR, and no
band in `READING, PRE-COMMITTED` is shaped to accommodate them. This is also what
makes Obligation 13's intersection computable at lock time.

---

## ⛔ READ BEFORE RATIFYING — SIX THINGS THE LANE OWNS

**1. THE CONTROL IS NOT THE HOLDER.** `bots/_v468kladturbo` is Sleipnir v1, pinned
as the corefill control at `scratchpad/CONTROL_PIN`
(`a9228ccb56ed9a65dd7d72ad1cb96068 bots/_v468kladturbo`), per Magnus's benchmark
ruling. **The LADDER holder is Odin (x3r0 v157), not Sleipnir**, so 50.0 here
means "adds nothing to the BENCHMARK" and the `ODINVSSLEIP` cell is the converter
into ladder units. A 61-shaped intuition from the KLADTURBO-vs-v140 read does not
transplant onto this page.

**2. ⛔⛔ THIS ARM IS *NOT* A ONE-CONSTANT DIFFERENCE FROM THE CONTROL. IT IS A
ONE-CONSTANT DIFFERENCE FROM ITS SIBLING, AND THE PRIMARY BAR IS AGAINST THE
CONTROL.** Two diffs, both verified at draft, and confusing them would
mis-attribute every band on this page:
* **vs `bots/_v482kladladder2` (the sibling): EXACTLY ONE LINE.**
  `diff -r bots/_v482kladladder2 bots/_v485kladladder3` returns a single hunk,
  `doctrine.py:1264`, `LOKI_FWD_TI_FLOOR = 40` → `LOKI_FWD_TI_FLOOR = 16`.
  `eco.py`, `main.py` and `raid.py` are byte-identical between the two trees.
* **vs `bots/_v468kladturbo` (the control, and the PRIMARY comparison):
  `doctrine.py` AND `raid.py`.** This tree carries the ENTIRE KLADLADDER2 plank —
  the `fwd_priority` computation, the step-3 guard and the step-8 opportunistic
  slot — **plus** the lower floor.
⇒ **THE PRIMARY BAR THEREFORE PRICES ORDERING-PLUS-CHEAPER-FUNDING, NOT THE FLOOR
ALONE. The floor alone is isolated ONLY by the registered contrast against
`KLADLADDER2` (S1 below), and no readout sentence may attribute a band on the
primary to the floor by itself.**

**3. ⛔ THE PRE-NAMED DELIVERY BAR ALREADY FAILED, AND THIS PAGE REGISTERS THE
HONEST WEAK-MECHANISM PRIOR RATHER THAN A HOPEFUL ONE.** The n=160 dose
(`scratchpad/kladladder3_dose.log`, 07:58) reads:

| quantity, n=160 paired | `_v485kladladder3` | control `_v468kladturbo` | ratio |
|---|---|---|---|
| sentinels built / game | 2.88 | 2.89 | 1.00x |
| **forward sentinels / game** | **1.50** | **1.44** | **1.04x** |
| builder deaths / game | 1.76 | 1.61 | 1.09x |
| forward builder deaths / game | 1.43 | 1.32 | 1.08x |

paired diff **+0.056/game, sd 2.54, 2×SE 0.402**, informative band |diff| ≥ 0.402
(28% of the control level). **The tool's own verdict, verbatim: `DOSE_RESULT: NO
INFORMATION — 1.44 -> 1.50/game is INSIDE the band. This is NOT a delivered dose
and NOT a refutation.`**
⇒ **The delivery criterion (paired-diff CI-lower > 0) FAILED.** It is registered
here as failed, before the screen, and the arm is fired anyway on a narrower and
honestly weaker question: **does a cheaper plant pay on GAME SHARE even without an
elevated count?** A lower reserve floor at an unchanged count is a **TIMING dose**
— the same plants, bought earlier — and timing is not visible in a count.
⚠ **`NO INFORMATION` is not `NO EFFECT`.** At 2×SE = 0.402 the battery could not
have detected a delivery change smaller than ~28% of the control level. Nothing on
this page may read the flat count as evidence the floor does nothing.

**4. THE THREE-CORNER FUNDING AXIS IS THE REASON THIS ARM EXISTS, AND ITS VALUE IS
IN THE CLOSURE, NOT IN THE HOPE.** `LOKI_FWD_TI_FLOOR` on the KLADLADDER chassis:
* **0 (waived)** — `_v473kladladder`. **READ: 41.86% [40.20, 43.52] at n = 3,404**
  (`results.tsv:474`, `kladladder-n-final-correction`), Band-4. ⛔ And its
  mechanism story INVERTED under re-measurement: `results.tsv:475`
  (`kladladder-attribution-correction-2`) records that the "2.11x DOSE DELIVERED"
  reading rested on an **n=24 control** (`dose.py`'s `--games` default) and **does
  not reproduce** — at n=120 `_v473`'s delivery is **0.87x, BELOW control**, while
  its builder deaths read **1.30x with the CI excluding zero [+0.008, +0.925]**.
  **All cost, no delivery.**
* **16** — THIS ARM. The untested middle: a funding path the base lacks, without
  zeroing the reserve every other consumer budgets against.
* **40 (the base's own floor)** — `bots/_v482kladladder2`,
  `docs/prereg/PREREG-KLADLADDER2-2026-08-17.md`. Its n=120 dose reads delivery
  0.82x and builder deaths 0.98x.
⇒ **With all three read, the FUNDING AXIS OF THIS FAMILY CLOSES.** ⛔ **No single
corner closes it, and this page's Band 3 says so explicitly.**

**5. THE SHARD TAPE CANNOT SEE THE MECHANISM, AND A FIRINGS READ IS MANDATORY
BEFORE THE PRIMARY.** `tools/overnight.sh:138-139` runs every game with
`--tle 10 --replay /dev/null`; the tape's columns (written at `:104`) are
`ts shard game map seed seat winner cond turns` — **no entity, build, bank or
turret information exists on it, in either arm.** The mechanism is CONDITIONAL (a
bank threshold inside a gated plant attempt), so `docs/prereg/BARS.tsv`'s
FIRINGS-BEFORE-PRIMARY rule binds.
⛔⛔ **AND THE ORDERING IS WRITTEN OUT EXPLICITLY BECAUSE THE RULE WAS INVERTED ON
THIS EXACT FAMILY TODAY** — `results.tsv:471` records the builder typing
KLADLADDER's Band-4 primary **before** its registered F1/F2 read, then amending.
> **T1 and T2 (below) are READ, and their numbers written down, BEFORE any
> sentence containing the primary share is typed.** A primary typed ahead of the
> firings read is a REGISTRATION BREACH regardless of what it says, and the repair
> is the amendment chain KLADLADDER used, not a re-write.

**6. THIS FIXTURE PRODUCES LARGE NEGATIVES AND HAS JUST DONE SO ON THIS EXACT
CHASSIS.** `_v473kladladder` finished 41.86% at n = 3,404. **The floor at 16 sits
between a corner that was catastrophic and a corner whose dose says it plants
LESS than the base.** A monotone-interpolation intuition ("16 is halfway, so it
lands halfway") is not licensed by anything — the two endpoints differ in
mechanism, not only in magnitude — and it is named here so nobody builds a
prediction on it.

---

## RATIFY: Hypothesis

**Lowering the forward-sentinel bank reserve floor from 40 Ti to 16 Ti on the
KLADLADDER2 chassis — so a forward sentinel is bought earlier out of a smaller
surplus, with the reserve NOT zeroed and no eco-deferral of any kind — raises our
LOCAL pooled game share against `bots/_v468kladturbo` itself to 51.33% or higher
at n = 5,400 games across all 15 corefill maps and both seats.**

**Provenance:** Magnus, s48, verbatim — *"iterate on kladladder until it works."*
The design of this particular iteration is the builder's, recorded in `e9e40548`:
*"a funding path the base lacks without zeroing the reserve; the un-tested middle
of the 0/16/40 floor dose ladder."*

**The mechanism claim, stated so it can be wrong.** One constant, two effects, and
the hypothesis is that the first outweighs the second:
* **IT BUYS THE SENTINEL EARLIER.** `raid.py:788` refuses a plant unless
  `bank ≥ cost + ti_floor`. At `ti_floor = 16` instead of 40, the same plant clears
  **24 Ti sooner** on the bank curve — which, at the cost scale a mid-game sentinel
  carries, is a matter of rounds, not of whether. **The count does not have to
  move for this to be real, and per the n=160 dose it did not.**
* **⚠ AND IT LEAVES 24 Ti LESS IN THE BANK EVERY OTHER CONSUMER BUDGETS AGAINST.**
  The belt planner and the Core's ammo conversion (its own `ti_floor` of 52/12)
  spend from the same global pool. **This is a smaller version of exactly the
  mechanism that killed `_v473` at floor 0, and that is the whole reason 16 rather
  than 0 is the value under test.**

**⇒ A flat result is INFORMATIVE.** With `_v473`'s 41.86 at floor 0 and
KLADLADDER2's read at floor 40, a flat 16 says the funding axis has no interior
optimum and the family's remaining design question is not funding at all.

**PRICE OF THE THING BEING BOUGHT EARLIER, quoted per house rule via
`tools/scale_trace.py --price 20` (a sentinel carries +20pp of cost scale):
READING 1 (as a total, 20pp) = p0.0 SMALL; READING 2 (on top of the r100 median of
180pp, i.e. 200pp) = p65.4 ORDINARY — inside the range teams routinely carry.
READING 2 is the primary per the tool's own instruction.** ⇒ the argument on this
page is about the RESERVE the purchase leaves behind, not about the turret being
expensive in scale terms.

---

## REGISTRATION BLOCK

**TARGET BAND: N/A — local corefill screen with ZERO rated ladder exposure: no submission, no activation, no unrated challenge, so `tools/target_value.py` has no input. Nothing on this page ends in a ship; the only branch that reaches the ladder is a later, separately-registered head-to-head against the live holder.**
**PINNED: N/A — local self-play. The opponent version is fixed by construction: the control tree is `bots/_v468kladturbo` at the commit this shard runs from, pinned at `scratchpad/CONTROL_PIN` (`a9228ccb56ed9a65dd7d72ad1cb96068 bots/_v468kladturbo`). There is no opponent churn to pin against and no calibration relevance to protect.**
**SURFACE: local**
**PLANK CLASS: offensive — a forward-sentinel siege plank at a cheaper funding floor. The reorder and the floor exist to open the kill lane at the enemy ring, not to hold one at ours; nothing in the diff touches home defence, and the `DEFENCE_ADMISSION_BAR`'s r300 clause therefore does not bind. D1 (ITT timely-kill rate, stated as an EXCLUSION) is read anyway.**
**KILL-ROUND NON-REGRESSION: ITT timely-kill rate over ALL 5,400 games (share ending `cond == core_destroyed` in our favour with `turns <= 300`), treatment vs control, scored as an EXCLUSION — the 95% CI on the difference must EXCLUDE a fall of more than 2.0pp. ITT RMST300 (mean of `min(turns,300)`, every non-kill scoring the full 300, `tools/fieldcal_read.py:239`) is read beside it on the same 5,400 rows. Median-crossing-300 is the gross backstop and the kill-win-conditioned share is a DIAGNOSTIC only — it carries a collider. This is D1/D2/D3 below, stated here in the registry's own vocabulary. ⭐ AND IT IS UNUSUALLY LOAD-BEARING ON THIS ARM: a cheaper floor buys the sentinel EARLIER, so a positive share with a WORSE timely-kill rate would be an internally inconsistent story.**
**CLUSTER UNIT: none** — CLAUDE.md's enumeration PERFORMED, not asserted: (i) the **MATCH** cluster does not exist on this surface — `tools/overnight.sh` writes one TSV row per `fcode run`, so 1 row = 1 game and no row shares a match with another; (ii) the **OPPONENT** cluster is degenerate — every one of the 5,400 rows plays the identical control tree, so the pooled stratum holds exactly one opponent and there is no between-opponent variation for a design effect to describe. Both clusters die ⇒ DEFF = the measured local constant **0.98** (pair-weighted, ρ = −0.020, 124 shards, s39 audit); naive intervals are correct and marginally conservative. **The platform constants (1.529 rated / 1.833 unrated) are NOT applicable.** ⚠ **The s42 cross-host rider binds HARDER on this page than on most, because the registered SECONDARY is a CONTRAST with a sibling shard: KLADLADDER2 and KLADLADDER3 must run ON THE SAME HOST at the same planned n, or S1 is not computable as registered.**
**ESTIMATOR: unweighted pooled treatment game share** = (rows with `winner == T`) / (completed rows), over all 5,400 rows, both seats pooled, all 15 maps pooled, no reweighting. Interval by `tools/cluster_ci.py` with the local constant. Seat A and seat B shares are reported SEPARATELY as a fixture diagnostic and are never the bar — seat is worth ~6.8pp on byte-identical arms, which is why the n is a multiple of 30.
**DOSE: forward-sentinel plants per game — treatment 1.50 vs control 1.44 (1.04x; paired diff +0.056/game, sd 2.54, 2×SE 0.402, n=160 paired, `tools/dose.py --kind sentinel`, `scratchpad/kladladder3_dose.log`, per-game rows in `scratchpad/dose_v485.tsv`). ⛔ THE TOOL'S OWN VERDICT IS `NO INFORMATION` — INSIDE THE BAND, NOT A DELIVERED DOSE AND NOT A REFUTATION. This dose is OBSERVABLE-AT-LOCK, not pre-registered, and the pre-named delivery criterion (paired-diff CI-lower > 0) is registered here as HAVING FAILED. The delivered-dose question for this arm is therefore the BANK-AT-PLANT and TIMING read T2 below, because a floor change at an unchanged count is a timing dose and a count-only instrument is structurally blind to it. Companion priors from the same battery: sentinels built 2.88 vs 2.89 (1.00x), builder deaths 1.76 vs 1.61 (1.09x), forward builder deaths 1.43 vs 1.32 (1.08x) — all reported, none of them a bar.**
**PLANNED n: 5400 games** (= 15 maps × 2 seats × 180, so map and seat balance is exact; `tools/overnight.sh:68` has carried the 15-map pool since the 2026-08-13 rotation and the runner's own comment requires multiples of 30).
**BOUNDARY: 5400 games** — LOCAL surface, one tape row is one game; there is no accept/attempt distinction on this fixture. ⛔ **A LINE COUNT IS NOT A ROW COUNT**: this tape carries an unprefixed column header (`tools/overnight.sh:104`), and a naive `wc -l` / `awk '!/^#/'` over-reports n by exactly one (measured on KLADLADDER itself, `results.tsv:474`). The registered denominator is **DictReader row count, cross-checked against the heartbeat and against `max(game id) + 1`.**
**CUT-SHORT: floor 2700 games.** Below 2,700 completed tape rows this leg publishes descriptive tallies (share, per-seat, per-map, kill-clock) and takes **NO comparative look and no bar verdict**; the half-width at 2,700 is ±1.87pp, already wider than the 1.33pp margin the bar is built on. An `auto_gate` cancellation at CATASTROPHE@400, MARK-1000 or TREND-FLOOR@1000 is an **OPERATIONAL STOP, not a verdict**, typed `cancellation`. ⭐ **ONE CARVE-OUT, PRE-COMMITTED:** a CATASTROPHE-clause cancellation (95% CI upper < 45.0 at n ≥ 400) is arithmetically INCOMPATIBLE with every band above Band 4, so a stop under that clause DOES license the Band-4 falsifier sentence at the partial n — **provided T1/T2 have been read first**, and provided the partial share is disclosed as **selected-pessimistic**. ⛔ **ASYMMETRIC-STOP CLAUSE: a gate stop on EITHER this shard OR `KLADLADDER2` CANCELS THE S1 CONTRAST**, because the contrast needs two full-n reads on one host; a stopped pair yields the two individual bands and nothing else.
**BAR: 51.33. MDE: 0.00pp — THIS IS A POINT RULE ONLY AND LICENSES NO EXCLUSION CLAIM ABOUT AN EFFECT SIZE.** Per the OB16 corollary (obligations doc, 2026-08-15T03:52:45Z): the standard corefill band IS `50 ± half_width` at n=5,400, so clearing 51.33 puts the CI's lower edge at exactly 50.00 — it excludes 50 and excludes **no positive effect size whatsoever**. n for the exclusion it CAN make (bar ≠ 50.0): **5,400**, the planned n.
**BASE RATE: 50.00**
**BAR SOURCE:** house-standard corefill futility band, `50 + 1.96*sqrt(.25/5400) = 51.33pp`, local DEFF 0.98 so naive — the identical bar carried by `docs/prereg/BARS.tsv` rows `SEALFLOOR6`, `SENTTHR`, `KLADTKILL`, `KLADTK2`, `KLADTURBOR`, `DRAINTURBO`, `KLADLADDER`, `SEALSENTAN`, `SEALSENTA` and `ECOMMIT`, which keeps this arm numerically comparable to the family it extends. **Constructed, not observed.**
**BASE RATE SOURCE:** structural A/A expectation of a seat-balanced, map-balanced self-play fixture whose control tree is the treatment's own base. Empirically calibrated by `IDNULL140` — **49.27% [47.94, 50.60] at n = 5,400**, 2026-08-16T18:02:04Z, same fixture (`results.tsv:454`, type `cert`) — and by `NULL125` — **51.04% at n = 5,400** (`results.tsv:346`, type `verdict`; ⚠ that row's share FIELD reads `0.510` and carries EMPTY CI columns while its prose reads 51.04% — the prose is the citation, and the row is not a source of an interval). Two A/A cells, one either side of 50.0. ⇒ **a bare clearance in [51.33, 52.4] is a band an A/A cell has already produced**, which is why Band 2 is pre-registered as WEAK.
**POOL ERA: post-2026-08-13-rotation** — the 15-map local pool of `tools/overnight.sh:68` (`antler archipelago auroraveil drakkarfjord drumlin fjordgate frostgate glacierkeep icefloe midgard nordkap ragnarok royale valkyrie yulerune`). (`check_pool_era` treats this as n/a on a LOCAL surface per SPEC §6; declared anyway so the population is on the page.) ⚠ **AND IT IS NOT COSMETIC: the n=160 dose ran on `tools/dose.py`'s own 8-map default rotation, NOT the 15-map screen pool.** T1 re-reads dose on the screen pool for exactly that reason.
**REFERENCE n: none** — the comparator is generated inside this same shard from the same 5,400 seeds; there is no fixed external reference sample, so no resolution floor at n→∞. (The S1 contrast's comparator is a SEPARATE registered shard at its own n = 5,400, sized in S1 below.)
**TREATMENT TREE: bots/_v485kladladder3**
**TREATMENT DIFF REFS: e9e40548^ e9e40548**
**MECHANISM METRIC READS: bots/_v485kladladder3/raid.py:788 — `if ct.get_global_resources() < cost + ti_floor: return False`, the bank test the manipulated constant feeds (`ti_floor` is bound one line earlier at `raid.py:775`, `ti_floor = LOKI2_RUSH_TI_FLOOR if rush else LOKI_FWD_TI_FLOOR`, and `LOKI_FWD_TI_FLOOR` is set at `doctrine.py:1264`). Observed as T1 (forward-sentinel builds/game on the SCREEN pool) and T2 (the ROUND distribution of forward-sentinel BUILD events plus the team bank at plant — the only decodable signature of a threshold change at an unchanged count). TREATMENT DIFF TOUCHES: bots/_v485kladladder3/doctrine.py bots/_v485kladladder3/raid.py. INTERSECTION: yes — against the CONTROL, `raid.py` differs across the whole KLADLADDER plank (`raid.py:69-70`, `:267-332`, `:370`, `:443-455`, `:738-816`; a `grep -c` for `fwd_priority`, `waive_floor` and `fwd_waive` over the CONTROL tree's raid module returns **0** against 12 in the treatment, verified at draft), and `doctrine.py:1264` carries the manipulated value.**
⛔ **AND THE HONEST OB13 CAVEAT, WRITTEN RATHER THAN LEFT FOR A CERTIFIER: `raid.py:788` IS PRESENT IN THE CONTROL TOO** — the base also refuses a plant below `cost + ti_floor`. What differs is the VALUE (`40` vs `16`), so the LINE does not distinguish the arms; the BANK LEVEL AT PLANT does. **That is why T2 reads the bank at plant and not merely the existence of plants, and why a T2 that reports only counts has not discharged this obligation.** Against the SIBLING `bots/_v482kladladder2` the diff is `doctrine.py:1264` and nothing else — the entire S1 contrast rests on one integer, which is the design and is also its whole fragility.
⚠ **DIFF-REFS DISCLOSURE:** `e9e40548` ADDS the whole tree, so `git diff --name-only e9e40548^ e9e40548` returns FOUR paths. The SEMANTIC diff against the control is TWO files: `diff -rq bots/_v468kladturbo bots/_v485kladladder3` names `doctrine.py` and `raid.py` only, and **`eco.py` and `main.py` are byte-identical to the control** (verified at draft). `TREATMENT DIFF TOUCHES` declares the semantic two.
**METRIC WINDOW: r0-r1000. GATING CONSTANTS: LOKI_FWD_TI_FLOOR=16, LOKI2_RUSH_TI_FLOOR=8, LOKI_FWD_MIN_HARV=2, LOKI2_RUSH_MIN_HARV=0, LOKI_LADDER_POST_HARV=3, LOKI_FWD_SENT_MIN_PRE=1, LOKI_FWD_SENT_MIN_POST=2, LOKI_FWD_GUN_CAP=3. MECHANISM CAN OCCUR IN WINDOW: yes** — **NOT ONE of these is a ROUND FLOOR.** `LOKI_FWD_TI_FLOOR` and `LOKI2_RUSH_TI_FLOOR` are TITANIUM amounts; `LOKI_FWD_MIN_HARV`, `LOKI2_RUSH_MIN_HARV` and `LOKI_LADDER_POST_HARV` are HARVESTER COUNTS; `LOKI_FWD_SENT_MIN_PRE/POST` and `LOKI_FWD_GUN_CAP` are TURRET COUNTS. The plank has **no round gate whatsoever** — the floor is consulted on every plant attempt from the first turn a raider acts. **The ONE round-keyed constant on the chassis is `LOKI2_RUSH_RND`, and it does not gate the mechanism: inside the rush window `ti_floor` falls to `LOKI2_RUSH_TI_FLOOR = 8` in BOTH arms, so the manipulated constant is INERT inside the rush window and binds only outside it.** ⇒ **the window in which the two arms can differ is `r ≥ LOKI2_RUSH_RND`, and T2 must report its round histogram with that boundary marked, or a null will be read over rounds where the treatment was byte-equivalent to the control by construction.** This is the sharpest gating fact on the page and it is stated before the data.
⚠ **DISCLOSED, because a green tool run with warnings under it is how a warning stops being read: `prereg_check.py` will emit `OBLIGATION 17, PARTIAL WINDOW` warns against the line above and THEY ARE ARTEFACTS OF THE CHECKER.** Its `check_metric_window` arithmetic reads every declared integer as a ROUND, so a titanium floor of 16 is reported as "rounds r0-r15 cannot contain the mechanism". The constants are declared anyway because they are the gates that actually bind.
**PRE-STATE: the predicted-change set is NOT already in the target state at lock.** Verified at draft against the control tree: `grep -c LOKI_LADDER_ON bots/_v468kladturbo/*.py` → **0** in all four files; `grep -c 'fwd_priority\|waive_floor\|fwd_waive' bots/_v468kladturbo/raid.py` → **0**; and the control's `LOKI_FWD_TI_FLOOR` is 40, not 16. The control has no live-census target, no step-8 slot and no cheaper floor. ⚠ **The comparative claim the FAMILY exists for — "there is an interior optimum on the funding axis" — is likewise NOT pre-satisfied**: floor 0 is read at 41.86 and floor 40 is unread; 16 is genuinely open in both directions, and Bands 3 and 4 are live pre-named outcomes.
**MAP SEGMENT: none expected** — the manipulated quantity is a GLOBAL TITANIUM THRESHOLD compared against the team bank. **A bank balance is not a terrain property**, and there is no map-conditional branch anywhere in the diff. What terrain changes is the SLOPE of the bank curve (how fast 24 Ti of headroom is earned) and the raider's arrival latency — i.e. how much earlier the plant lands, not whether the threshold binds. **No map cut may rescue this arm.** Per-map shares WILL be printed at readout as exploratory description; they carry no pre-registered direction and nothing may be banked off them without a fresh prereg. ⚠ **One candidate segment is named and DELIBERATELY NOT REGISTERED**: the five 900-area maps (midgard, ragnarok, valkyrie, drakkarfjord, glacierkeep), where the slowest eco means 24 Ti of headroom is worth the most rounds. Registering it would hand this arm a second chance to pass — OB15b's exact prohibition. If the pooled read fails and that cut looks alive it needs its OWN leg with its OWN n.
**CELL VERSION CHURN: N/A — not a panel, no `CELLS:` line, one fixed local control tree.**
**GATE RESOLUTION: the shard is governed by the pinned `tools/auto_gate.py` marks — CATASTROPHE@400 (STOP if the 95% CI upper < 45.0, `auto_gate.py:236`), MARK-1000 (STOP if the CI upper < the registered BAR 51.33), TREND-FLOOR@1000 (STOP if the first-1,000 prefix share < 52.0, `auto_gate.py:250` — RAISED from 51.0 by Magnus 2026-08-16), and the same floors again at MARK-2700 (`auto_gate.py:233-236`). Their firings are OPERATIONAL CANCELLATIONS that free a core — typed `cancellation`, never `verdict`, licensing NO exclusion claim (with the single CATASTROPHE carve-out in CUT-SHORT). ⭐ THE REMOTE LIMITATION IS DEAD: `auto_gate.py:113` was REPORT-ONLY on a worker — which is why KLADLADDER ran to n≈3,404 at 41.86 with no automatic stop — but `a50f27ef` gave `auto_gate --apply` a guarded remote stop path (`tools/remote_cancel.py`), so the strict floors NOW BIND on ws1/ws2 too. ⇒ this shard may run LOCAL or REMOTE; what is registered is that **it runs on the SAME HOST as `KLADLADDER2`** (the S1 contrast requires it, per the s42 cross-host rider) and that a remote route switches the second clock to the registered first-completed-row backstop. The RESOLVABLE gates this document owns are (a) the primary at full n, margin 1.33pp against half-width ±1.32pp — resolvable, and only just — and (b) S1, whose resolution statement is written into S1 itself. Everything else (T1, T2, D1-D3, seat and map splits) is DIAGNOSTIC and cannot rescue a failed primary. Any branch that does not resolve is UNRESOLVED, and an UNRESOLVED gate defaults to the RESTRICTION: no promotion, no ship conversation, no combination claim.**

---

## FALSIFIER

**PRIMARY FALSIFIER: at n = 5,400 the 95% CI UPPER bound on the treatment's pooled
game share falls BELOW 51.33.** That excludes the bar and says the ladder at
floor 16 does NOT add measurably to Sleipnir.
**Consequence, registered in advance and split by how far it falls:**
* **CI upper < 51.33 but CI contains 50.0** → floor 16 is INERT relative to the
  benchmark. See Band 3, and note that this is a statement about
  ordering-plus-floor-16 TOGETHER; the floor's own contribution is S1's.
* **CI upper < 50.0** → **the cheaper floor costs**, i.e. the reserve drawdown that
  killed `_v473` at 0 is still net-negative at 16, and the funding axis is
  monotone-bad rather than having an interior optimum.

**MECHANISM FALSIFIER (independent of the primary, and it can fire first).**
⛔ **IT IS DELIBERATELY NOT WRITTEN AGAINST THE COUNT. THE COUNT ALREADY CAME BACK
`NO INFORMATION` AND A COUNT-DENOMINATED FALSIFIER WOULD FIRE ON THE ARM'S OWN
PREDICTION.** **The falsifier is T2:** if the ROUND distribution of
forward-sentinel BUILD events **outside the LOKI-2 rush window** is
indistinguishable between arms, AND the team bank at plant is indistinguishable,
then a 24 Ti threshold change never bound in play — the plank did not deliver its
dose and **the primary is uninterpretable in either direction**: a flat share
would mean "the floor never bound", not "the floor bound and did not pay". Per
FIRINGS-BEFORE-PRIMARY this is read BEFORE the primary is typed, and if it fires
the primary is reported as **NOT MEASURED** rather than as a null. **This is not
hypothetical: s47's delta D2 records a wiring null escaping demos to a 436-game
shard.**

---

## READING, PRE-COMMITTED — four bands, written before the data

Registered now so no band is chosen after the fact. **Read TOP-DOWN; the first row
whose condition holds is the reading. The rows are disjoint by construction.**

| # | band at n = 5,400 | pre-committed reading |
|---|---|---|
| **1** | **CI lower ≥ 51.33** | **THE LADDER AT FLOOR 16 ADDS.** Real and resolved on this fixture. Promotes to a combination input and to a separately-registered head-to-head against the live holder. ⛔ **Attribution is capped by READ-BEFORE-RATIFYING #2**: this band credits ORDERING-PLUS-FLOOR-16, and only S1 can say how much of it is the floor. ⚠ OB16 status: the standard band has MDE 0, so this branch may claim "we can exclude 50" and may NOT claim any minimum effect size. |
| **2** | **point ≥ 51.33 but CI lower < 51.33** | **REAL-BUT-SMALL, COMBINATION INPUT ONLY.** Registered in advance as WEAK: `NULL125`'s byte-identical A/A read 51.04, so a bare clearance in [51.33, 52.4] is not distinguishable from fixture noise by this leg alone. Rows are KEPT; no ship conversation; a replication on fresh seeds is the price of promotion. |
| **3** | **point < 51.33 AND CI contains 50.0** | **PARITY — AND THIS IS THE BAND THE ARM WAS FIRED TO REACH IF IT COULD NOT WIN.** Together with `_v473`'s 41.86 at floor 0 and `KLADLADDER2`'s read at floor 40, **the funding axis is then fully read at three corners and the FUNDING QUESTION CLOSES**: there is no interior optimum, the waiver's damage does not become a benefit at half strength, and the family's remaining design question is not funding. ⛔ **THE CLOSURE IS ONLY LICENSED WHEN ALL THREE CORNERS HAVE BEEN READ AT FULL n ON ONE HOST.** This arm alone licenses "floor 16 is inert", NOT "the axis is closed". |
| **4** | **CI upper < 50.0** | **THE CHEAPER FLOOR COSTS.** Drawing the reserve down by 24 Ti is net-negative even without zeroing it; the funding axis is monotone-bad and floor 40 (the base's own) is the best value on it. ⛔ Do NOT respond by trying 24 or 32 — a further point on a monotone-bad axis is not an iteration, it is a search for noise. |

⚠ **Rows 3 and 4 both fire the PRIMARY FALSIFIER**; the band decides which half of
its consequence applies.
⚠ **Nothing here treats 50.0 as a floor.** A share below 50 is a live outcome with
a named mechanism (24 Ti less reserve for the belt planner and the Core's ammo
conversion) and it is pre-named so a negative is not explained away as noise.

---

## MECHANISM DIAGNOSTICS TO READ AT READOUT

**Measurability is declared per metric. `NOT MEASURABLE` is written where it is
true, rather than a metric being quietly renamed into something the tape carries.**

### ⛔ ORDERING, REGISTERED AS A HARD SEQUENCE
**T1 and T2 run and are written down BEFORE any sentence containing the primary
share is typed.** See READ-BEFORE-RATIFYING #5.

### T1 — DOSE ON THE POOL THE SCREEN PLAYS. MEASURABLE, but NOT off the shard tape.
```
.venv/bin/python tools/dose.py bots/_v485kladladder3 --kind sentinel \
    --ctrl bots/_v468kladturbo --games 160 --tsv scratchpad/dose_v485_screenpool.tsv \
    --maps antler archipelago auroraveil drakkarfjord drumlin fjordgate frostgate \
           glacierkeep icefloe midgard nordkap ragnarok royale valkyrie yulerune
```
**REGISTERED SIZE: 160 games, SERIAL** (never parallel: D65, `tools/dose.py:26-30`).
⛔⛔ **`--games 160` IS NOT OPTIONAL AND ITS ABSENCE FROM THE SHELL HISTORY IS A
REGISTRATION BREACH.** `tools/dose.py`'s `--games` DEFAULTS TO 24, and KLADLADDER's
registered 120 silently ran as 24, producing the 2.11x artifact that stood as an
attribution for 34 minutes (`results.tsv:475`).
**Pre-registered expectation: T1 reproduces the pre-lock prior — the paired
difference stays INSIDE the tool's own 2×SE band (`NO INFORMATION`). T1 is NOT a
pass/fail gate for this arm; a flat count is the prediction.** A count that moves
OUTSIDE the band on the screen pool, in either direction, is a **SURPRISE** and must
be written down as one before it is explained (CLAUDE.md point 4).

### T2 — THE THRESHOLD READ. THIS IS THE ARM'S REAL DOSE, AND IT IS NOT YET EXECUTABLE.
A floor change at an unchanged count shows up in **WHEN** the plants land and in
**HOW MUCH BANK WAS LEFT** when they did. `tools/corpus/replay_events.py` emits one
row per build with columns `file ev rnd team kind x y d2_own d2_enemy mw mh`, so the
round half is directly available:
```
.venv/bin/python tools/corpus/replay_events.py OUT.tsv <replays…>
# rows with ev == BUILD and kind == sentinel, grouped by team:
#   (a) round of the FIRST forward sentinel, per game, treatment vs control
#   (b) the full round histogram, WITH the LOKI2_RUSH_RND boundary marked
```
**Pre-registered expectation, with its sign:** **outside the rush window**, the
treatment's forward sentinels land **EARLIER** than the control's (a 24 Ti lower
threshold is cleared sooner on the same bank curve), at a total count inside the
dose band. **Inside the rush window the two arms are byte-equivalent by
construction (`ti_floor = LOKI2_RUSH_TI_FLOOR = 8` in both) and MUST read
identical — that half is a POSITIVE CONTROL on the read itself: a T2 that shows a
difference INSIDE the rush window is measuring something other than this
constant, and the read is void.**

⛔ **OB17 — THIS READ IS NOT EXECUTABLE OFF A `tools/dose.py` RUN, AND THE BUILDER
MUST FIX THAT BEFORE THE BATTERY FIRES. THIS IS THE CLAUSE ON THIS PAGE THAT CAN
STILL SURPRISE THE PERSON RUNNING IT; RUN IT FIRST.**
1. **NAME THE EXECUTING TOOL** — `tools/dose.py` for T1;
   `tools/corpus/replay_events.py` for T2's round half.
2. **CONFIRM THE PATH EXISTS IN THAT TOOL** — for the ROUND half it does NOT.
   `tools/dose.py:157` calls `rp.unlink(missing_ok=True)` on every replay
   immediately after decoding and there is **no `--keep`** (wrap debt 20); the
   `--tsv` flag carries **counts only, no round column**, which is exactly why
   `results.tsv:476` (`kladladder-f1-timing-status`) records the timing half of
   KLADLADDER's F1 as **NOT MEASURABLE FROM RETAINED OUTPUT**. ⇒ T2 needs either
   (a) `--keep` added to `tools/dose.py`, or (b) its own serial loop passing
   `--replay <unique path>` and retaining the files.
3. ⛔ **AND THE BANK-AT-PLANT HALF IS WORSE: I COULD NOT NAME A SHIPPED TOOL THAT
   DECODES THE TEAM TITANIUM BALANCE AT A BUILD EVENT.** `replay_events.py`'s
   columns are positional and typed, not economic. **Per Obligation 13's own
   sentence — "if the prereg cannot name the file:line, that is the finding" —
   the bank half of T2 is registered as REQUIRING NEW INSTRUMENTATION, and if it
   is not built the mechanism evidence for this arm is the ROUND half alone.**
4. **CONSEQUENCE OF SILENT NON-EXECUTION** — if T2 is skipped entirely, the only
   dose evidence is a count already reported as `NO INFORMATION`, i.e. **no
   evidence at all that the manipulated constant changed behaviour.** The primary
   must then be typed with **"MECHANISM NOT VERIFIED"** attached, and Bands 3 and
   4 may NOT be attributed to the floor.

### S1 — THE FLOOR CONTRAST (registered SECONDARY; this is what isolates the constant).
**S1 = (KLADLADDER3 pooled share) − (KLADLADDER2 pooled share)**, both at n = 5,400
on the SAME HOST, computed on the pooled tapes.
**BAR: |Δ| ≥ 1.87pp, in the `null(0) + MDE(1.87)` form** — the MDE is INSIDE the
bar, per OB16's amended preferred form, and 1.87pp is the half-width of a
5,400-vs-5,400 difference at local DEFF 0.98
(`1.96*sqrt(0.98*(0.25/5400 + 0.25/5400)) = 1.87pp`). **Clearing it IS the
exclusion.**
**RESOLUTION STATEMENT (OB12):** at n = 5,400 per arm this contrast can separate a
true floor effect of ±1.87pp and NOTHING SMALLER. **If the true effect of moving
the floor 40 → 16 is under ~1.9pp, this pair CANNOT resolve it, and the
pre-committed consequence is that S1 is reported as UNRESOLVED and defaults to the
RESTRICTION — no claim in either direction about the floor.**
⚠ **A/A CREDIBILITY CAVEAT, registered before the data:** `IDNULL140` (49.27) and
`NULL125` (51.04) are **1.77pp apart on this very fixture** — just under the
smallest difference S1 is built to call real. **S1 is at the edge of what this
fixture can do, and that is said here rather than discovered at readout.**
⛔ **S1 CANNOT BE COMPUTED IF EITHER SHARD IS STOPPED BY A GATE** (asymmetric-stop
clause, CUT-SHORT), **or if the two shards run on different hosts** (s42
cross-host rider). **`docs/prereg/BARS.tsv` cannot express a contrast and
`tools/auto_gate.py` cannot enforce one** — the registry row for this shard carries
the SECONDARY bar 51.33 only, and this paragraph is the registration of the
primary-in-spirit quantity. That asymmetry is the SEALSENTA / BELTBREAK precedent
and it is disclosed, not hidden.

### D1-D3 — the kill-clock read. MEASURABLE, shard-native (`cond`, `turns`, `winner`).
* **D1 — TIMELY-KILL RATE (the `DEFENCE_ADMISSION_BAR` primary), ITT.** Share of ALL
  treatment-seat games ending `cond == core_destroyed` in our favour with
  `turns ≤ 300`, treatment vs control, both on the same 5,400 rows.
  **Non-regression is the bar and it is stated as an EXCLUSION, per CLAUDE.md's
  fail-to-exclude clause: the 95% CI on the difference must EXCLUDE a fall of more
  than 2.0pp.** A "no significant rise" phrasing is not admissible.
  ⭐ **AND D1 IS UNUSUALLY LOAD-BEARING HERE**: an earlier forward sentinel is a
  mechanism for a FASTER kill, so a positive share with a WORSE D1 would be an
  internally inconsistent story and must be reported as such.
* **D2 — MEDIAN KILL ROUND**, treatment vs control, as the gross backstop (a median
  crossing 300 is disqualifying), reported alongside the r1000 share since
  `R1000_IS_DEFEAT` makes an r1000 game a cost even when its tiebreak is won.
  Anchor: KLADTURBO's own local full read had median kill 193 (`results.tsv:466`,
  61.09% [59.79, 62.39] n = 5,400 vs `_v223sealrepair`).
* **D3 — RMST300, ITT** — mean of `min(turns, 300)` with every game not ending in OUR
  core kill scoring the full 300 (`tools/fieldcal_read.py:239`, the registered
  estimator), with its interval from `tools/cluster_ci.py`. **ITT over ALL rows, not
  over kills only** — the kill-conditioned form carries a collider, per `PROGRAMME.md`.

### NOT MEASURABLE on this leg — named, not silently dropped.
* **The team bank at plant** — see T2 clause 3. **No shipped tool reads it**, so the
  most direct signature of a THRESHOLD change is unavailable unless one is built.
* **Which consumer lost the 24 Ti.** The belt planner and the Core's ammo conversion
  spend from the same pool; nothing on either surface attributes a foregone spend to
  a consumer. **The plank's named cost channel is UNOBSERVED.**
* **Builder deaths at screen n.** The 1.09x prior is a 160-game battery figure with no
  interval published on the ratio; the shard tape has no unit events. **No readout
  sentence may claim the death rate was re-confirmed by this leg.**
* **Per-unit CPU.** Local replays zero-fill `execTimeUs` (the s42 D33 instance:
  `tle_census.py` returns 0 across 1,649 local builder-turns while reading 8,847 µs on
  platform replays), so **no CPU claim is available from this leg.**
* **Seed determinism.** `NOISE_ON` pins an unseeded per-unit salt and raiders gate on
  `get_cpu_time_elapsed()`, so base-vs-base at one seed diverges at round 0. **No
  seed-matched or replay-diff equivalence claim is available on this fixture.**
  ⭐ **The flag-off equivalence claim is made ON THE CODE, never on a replay
  comparison**: this tree inherits `bots/_v482kladladder2` unchanged apart from one
  integer, and that tree's own build record (`e2a71410`) states an AST-normalised
  (comments and docstrings stripped) diff against `_v468kladturbo` of **0
  executable-line deltas in `eco.py`, 0 in `main.py`, 26 in `raid.py`, 4 in
  `doctrine.py`**; `diff -q` confirms `eco.py` and `main.py` byte-identical to the
  control here too (verified at draft), and `diff -r` confirms the one-line
  difference from the sibling. ⚠ **The same commit records that the EMPIRICAL version
  of this check is unrunnable on this fixture and that a base-vs-base control fires
  the same "not equivalent" verdict** — the construction argument is load-bearing
  precisely because the measurement cannot be made.

---

## THE CHANGE — `file:line`, control → treatment

**TREATMENT TREE: `bots/_v485kladladder3`** — `bots/_v468kladturbo` plus the
KLADLADDER plank plus one integer. Verified at draft: `diff -rq` against the
control names exactly `doctrine.py` and `raid.py` (`eco.py`, `main.py`
byte-identical); `diff -r` against `bots/_v482kladladder2` names exactly one hunk.

1. ⭐ **`doctrine.py:1264` — `LOKI_FWD_TI_FLOOR = 40` → `LOKI_FWD_TI_FLOOR = 16`.
   THIS IS THE ONLY DIFFERENCE FROM `bots/_v482kladladder2` AND IT IS THE ARM.**
2. **`doctrine.py:1266-1391`** — the KLADLADDER + KLADLADDER2 doctrine blocks and
   four constants: `LOKI_LADDER_ON = True` (`:1324`), `LOKI_LADDER_POST_HARV = 3`
   (`:1325`), `LOKI_FWD_SENT_MIN_PRE = 1` (`:1326`), `LOKI_FWD_SENT_MIN_POST = 2`
   (`:1327`). Inherited from the sibling, byte-identical.
   ⚠ **AND THE INHERITED PROSE IS NOW STALE AGAINST THE VALUE IT ANNOTATES:
   `doctrine.py:1352-1353` still reads "requires `bank >= cost + LOKI_FWD_TI_FLOOR`
   (40, …)" and `:1492` still reads "`LOKI_FWD_TI_FLOOR = 40` Ti must remain after
   paying". The shipped value is 16.** A reader of this tree's comments gets the
   sibling's number. **Flagged for the builder as a cheap pre-fire fix; it does not
   change behaviour and it is NOT a reason to hold the lock.**
3. **`raid.py:69-70`** — `_FWD_LIVE_UNSET`. **`raid.py:267-332`** — the
   `fwd_live` / `fwd_target` / `fwd_priority` computation with the flag-off
   else-branch at `:326-332`. **`raid.py:370`** — step 3, now guarded by
   `fwd_priority`. **`raid.py:443-455`** — step 8, the opportunistic slot (absent
   from the control). All inherited from the sibling, byte-identical.
4. **`raid.py:775`** — `ti_floor = LOKI2_RUSH_TI_FLOOR if rush else LOKI_FWD_TI_FLOOR`,
   the single consumption site of the manipulated constant. **`raid.py:788`** —
   `if ct.get_global_resources() < cost + ti_floor: return False`, the test that
   binds. **`raid.py:816`** — `ct.build_sentinel(bp, facing)`, the plant.
   ⛔ **There is NO waiver on any path in this tree**; `waive_floor` was deleted, not
   defaulted off, by the sibling.

---

## WHAT THIS LEG COSTS AND WHAT IT DOES NOT

**Cost: one core to n = 5,400, plus 160 serial games for T1 and a retained-replay
battery for T2.** ZERO rated ladder exposure, zero submissions, zero unrated
challenges — nothing on this page touches the platform, which is why `TARGET BAND`
is N/A rather than a number.

**It does NOT decide a ship.** The strongest branch promotes the arm to (a) a
combination input and (b) a separately-registered head-to-head against the live
holder — Magnus's procedure verbatim (*"we start by testing it against the current
slot, If it beats it we can switch"*), templated by `SLEIPH2H`. **Gate-1-to-gate-2
transitivity is UNVALIDATED in this repo (QUEUE #65: 3 concordant, 1 not)**, and the
benchmark is not the holder, so `ODINVSSLEIP` is the converter into ladder units.

**It is one corner of a THREE-CORNER FUNDING AXIS, and its main value is the
closure.** Floor **0** = `_v473kladladder`, READ at 41.86% [40.20, 43.52] n = 3,404.
Floor **16** = this arm. Floor **40** = `bots/_v482kladladder2`,
`docs/prereg/PREREG-KLADLADDER2-2026-08-17.md`. **No single corner closes the axis;
all three read at full n on ONE host is what does** — the cross-host rider (Addendum
11, 2026-08-15) means the 0.98 local exemption is a WITHIN-HOST measurement and does
not cover pooling or differencing across boxes.

---

**PROVENANCE:** `docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md` (read in full: OB1, OB7, OB12, OB13, OB14, OB15a/b/c, OB16 + its corollary and cross-host rider, OB17 + its rider) · `docs/prereg/PREREG-SEALSENTAN-2026-08-17.md` and `docs/prereg/PREREG-ECOMMIT-2026-08-17.md` (today's house style, both read in full) · `docs/prereg/PREREG-KLADLADDER2-2026-08-17.md` (the sibling this arm contrasts against) · `docs/prereg/BARS.tsv` (header, the FIRINGS-BEFORE-PRIMARY rule, the SEALSENTA/BELTBREAK contrast-cannot-be-expressed precedent, and the sibling klad-family rows) · `CLAUDE.md` · `tools/prereg_check.py` (`RULES`, `DEFF`, `check_metric_window`, `check_pool_era`) · `tools/auto_gate.py:113,233-236,250` · `tools/overnight.sh:68` (the 15-map pool), `:99,103,110` (the FIXTURE stamp and its legacy-resume form), `:104` (the tape column header), `:118-120` (the row-count rule), `:138-139` (`--tle 10 --replay /dev/null`) · `tools/dose.py` (`:26-30` the serial rule, `:157` the replay unlink, and the `--games` default of 24) · `tools/corpus/replay_events.py` (the `rnd` column T2 needs) · `tools/fieldcal_read.py:239` · `tools/cluster_ci.py` · `tools/scale_trace.py --price 20` (run at draft; READING 2 = p65.4 ORDINARY) · `bots/_v485kladladder3/{doctrine,raid}.py` · `bots/_v482kladladder2/{doctrine,raid}.py` · `bots/_v468kladturbo/{doctrine,eco,main,raid}.py` · git commits `e9e40548` and `e2a71410` (full body, which carries the sibling's n=120 dose), `git diff --name-only e9e40548^ e9e40548`, `diff -r bots/_v482kladladder2 bots/_v485kladladder3` · `scratchpad/kladladder3_dose.log` and `scratchpad/dose_v485.tsv` (the n=160 battery) · `scratchpad/corefill_work.txt` · `scratchpad/CONTROL_PIN` · `results.tsv` (rows 346 `null125-final`, 454 `idnull140-cert-5400`, 466 `kladturbo-local-confirm-5400`, 470-476 the seven `kladladder-*` rows) · the drafting brief supplied by the builder lane s48. No file under `bots/`, `tools/`, `scratchpad/`, `docs/prereg/BARS.tsv`, `results.tsv`, `HANDOVER.md`, `PROGRAMME.md` or `QUEUE.md` was created or modified by this agent, and no game was run.
