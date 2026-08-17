# SCREEN PREREG — `KLADLADDER2`: the sentinel ladder with the COMMITMENT TAX severed — does the ORDERING alone pay?

Drafted by a fresh opus subagent with no inherited session context beyond the
inputs listed under `PROVENANCE`. The builder lane ratifies the judgment lines
and types the lock commit; this agent wrote no code under `bots/`, appended no
worklist row, appended no `BARS.tsv` row, fired no game, started no shard, and
touched neither `results.tsv` nor `HANDOVER.md` nor `PROGRAMME.md` nor
`QUEUE.md`.

**STATUS: committed BEFORE the `KLADLADDER2` row is appended to
`scratchpad/corefill_work.txt`, BEFORE any file named
`scratchpad/overnight/KLADLADDER2.*` exists, and BEFORE the leg's first game.**
Drafting session wall clock at write time **`2026-08-17T07:12:01Z`** (`date -u`,
same shell call); repo HEAD at draft `12e71962` (author time
`2026-08-17T09:10:53+02:00`). Verified at draft:
`grep -c 'KLADLADDER2' scratchpad/corefill_work.txt` → **0**; same grep on
`docs/prereg/BARS.tsv` → **0**; `ls scratchpad/overnight/ | grep -i kladladder2`
→ **empty**; `grep -cE '828000' scratchpad/corefill_work.txt` → **0** (the seed
base is free, and the highest local seedbase currently in any worklist is
826000).

### SECOND CLOCK — two-clock form, primary and backstop both named now

**PRIMARY: this commit's git author time against the `# FIXTURE … start=` stamp
that `tools/overnight.sh:103` writes as the FIRST LINE (its `START=` is computed at `:99`) of
`scratchpad/overnight/KLADLADDER2.tsv`, before the first `fcode run`, on any
tape that does not already exist.** That is a START, not a first-completed-row,
and it is the tighter clock.
**BACKSTOP, registered now so no judgement is made later:** if the tape instead
carries `# FIXTURE-RESUME … start=UNKNOWN-legacy-tape` (`tools/overnight.sh:110`),
carries no `# FIXTURE` line at all, or the shard is routed to a REMOTE worker
(whose tapes carry no stamp — the SEALSENTAN Amendment 1 case), the second clock
is **the `ts` of the FIRST COMPLETED ROW**. That is conservative by construction:
the true start is strictly earlier, so the lock-to-fixture gap can only ever be
UNDERSTATED.

⚠ **The treatment tree ALREADY EXISTS and is committed** (`bots/_v482kladladder2`,
added `e2a71410`, author time `2026-08-17T07:47:17+02:00`). This document is
therefore **NOT** locked before the arm exists, only before the arm's first
screen row. Said here rather than left for a certifier to find. It is also what
makes Obligation 13's intersection **computable at lock time**.

⛔ **AND ONE FURTHER THING IS ALREADY OBSERVED AT LOCK, WHICH IS THE MOST
IMPORTANT DISCLOSURE ON THIS PAGE: THIS ARM'S DOSE BATTERY HAS ALREADY RUN.**
The n=120 `tools/dose.py` read is recorded in the treatment commit's own message
(`e2a71410`) and predates this registration. Under the obligations doc's
Obligation 1 (the `Leg A is not a blind control` rule) it is labelled
**OBSERVABLE-AT-LOCK and is NEVER presented as pre-registered**. Every number it
produced is reprinted below as a PRIOR, and the bands in `READING,
PRE-COMMITTED` are not shaped to accommodate it.

---

## ⛔ READ BEFORE RATIFYING — SIX THINGS THE LANE OWNS

**1. THE CONTROL IS NOT THE HOLDER.** `bots/_v468kladturbo` is Sleipnir v1,
pinned as the corefill control at `scratchpad/CONTROL_PIN`
(`a9228ccb56ed9a65dd7d72ad1cb96068 bots/_v468kladturbo`), per Magnus's benchmark
ruling that our arms compete against Sleipnir during core shards. **The LADDER
holder is Odin (x3r0 v157), not Sleipnir.** So 50.0 on this page means "adds
nothing to the BENCHMARK", and converting that into a statement about the ladder
requires the `ODINVSSLEIP` calibration cell, which is exactly what that cell is
for. **A reader who transplants a 61-shaped intuition from the KLADTURBO-vs-v140
read onto this page has misread the fixture: the same bot measured against itself
reads 50.**

**2. ⛔⛔ THE REGISTERED QUESTION IS NARROW, AND IT IS NARROW BECAUSE THE DOSE
ALREADY CAME BACK.** `_v473kladladder` (iteration 1) shipped the ladder TOGETHER
with a commitment tax — the priority plant waived the bank reserve floor
(`ti_floor = 0`). This tree deletes that waiver **and nothing else**. With the
waiver gone the arm has **NO funding path the base lacks**, and its measured dose
says so:

| quantity, n=120 paired (`e2a71410`) | `_v482kladladder2` | control `_v468kladturbo` | ratio |
|---|---|---|---|
| forward sentinels / game | **1.23** | **1.49** | **0.82x** |
| builder deaths / game | **1.70** | **1.73** | **0.98x** |

paired diff on delivery **−0.267/game, 2×SE 0.476 ⇒ 95% band [−0.743, +0.209]**
— **NOT elevated, and the interval contains zero.**
⚠ **CORRECTION TO THE DRAFTING BRIEF, made rather than copied:** my brief quoted
this interval as `[-0.733, +0.200]`. **The committed figures are diff −0.267 and
2×SE 0.476, which give [−0.743, +0.209].** The brief's numbers do not reproduce
from the commit body; the commit body is the citation of record and is what is
registered here.
⇒ **THE HYPOTHESIS UNDER TEST IS THEREFORE NOT "MORE SENTINELS". It is: does the
ORDERING alone — a priority reordering inside the raider's OWN act ladder, step 3
when below target and step 8 (after peck AND salt) when at or above it — pay on
GAME SHARE, at a delivery count that is at or slightly below control?**

**3. THE DELIVERY SHORTFALL IS STRUCTURALLY PREDICTED, WHICH IS WHY IT IS NOT A
WIRING NULL.** The tree recorded the seam BEFORE its dose ran
(`doctrine.py:1367-1382`), and the argument is arithmetic: below target step 3
fires with the floor, exactly as the base's unconditional step 3 does ⇒
IDENTICAL; at or above target step 3 is SKIPPED and the attempt moves to step 8,
which only runs if peck and salt both declined ⇒ **STRICTLY FEWER opportunities
than the base for sentinels #2 and #3.** ⇒ **per turn at identical state, this
tree's plant-attempt SET IS A SUBSET of the base's.** ⚠ That does **not** make the
game-level COUNT a subset — the two bots diverge at round 0 (raiders gate on
`get_cpu_time_elapsed()`, so the fixture is not deterministic against itself) —
but it makes `delivery ≤ control` the honest expectation, and the observed 0.82x
is that expectation landing, not an instrument failure. **The MECHANISM FALSIFIER
below is written against a quantity that CAN still separate "fired" from "did not
fire", and it is not the count.**

**4. THE LINEAGE, WITH ITS CORRECTED HISTORY, BECAUSE THE UNCORRECTED VERSION IS
STILL QUOTABLE FROM THREE ROWS OF `results.tsv`.**
* `kladladder-manual-catastrophe-stop` (`results.tsv:470`, 2026-08-17T05:10:24Z)
  — interim stop at n≈3,121.
* `kladladder-n-final-correction` (`results.tsv:474`, 05:18:10Z) — **THE ARM'S
  CITATION OF RECORD: 41.86% [40.20, 43.52] at n = 3,404**, Band-4, ~8pp BELOW
  the null.
* ⛔ `kladladder-attribution-correction-2` (`results.tsv:475`, 05:52:34Z) — **the
  famous "DOSE DELIVERED 2.11x" DOES NOT REPRODUCE.** The n=24 control estimate
  (0.75 fwd sentinels/game) was the artifact; `dose.py`'s default `--games=24`
  is why a registered 120 silently ran as 24. **At n=120 the same base reads
  1.49-1.57 and `_v473`'s delivery is 0.87x — BELOW control — while its builder
  deaths read 1.30x with the CI EXCLUDING ZERO [+0.008, +0.925].**
⇒ **THE TAX WAS ALL COST AND NO DELIVERY**, and **this arm's 0.98x builder deaths
against `_v473`'s 1.30x on the SAME instrument at the SAME n is the tax's
disappearance measured.** ⚠ **That contrast is between two SEPARATE batteries, not
a within-battery randomised comparison; it is a PRIOR, it carries no interval on
the difference, and it is not the primary.**
⚠ **STANDING METHOD RULE, banked on `results.tsv:475` and repeated here because
this page's own priors depend on it: A DOSE READ WHOSE CONTROL RESTS ON n=24 IS
NOT A MECHANISM LICENCE.** Nothing on this page cites an n=24 dose.

**5. THE SHARD TAPE CANNOT SEE THE MECHANISM, AND A FIRINGS READ IS MANDATORY
BEFORE THE PRIMARY.** `tools/overnight.sh:138-139` runs every game with
`--tle 10 --replay /dev/null` and the tape's columns are
`ts shard game map seed seat winner cond turns` — **no entity, build or turret
information exists on it, in either arm.** The plank's mechanism is CONDITIONAL
(an eco-phase-gated priority flag with two call sites), so `docs/prereg/BARS.tsv`'s
FIRINGS-BEFORE-PRIMARY rule (adopted 2026-08-16T13:27:33Z) binds.
⛔⛔ **AND THE ORDERING IS WRITTEN OUT EXPLICITLY BECAUSE THE RULE WAS INVERTED ON
THIS EXACT FAMILY TODAY.** `results.tsv:471`
(`kladladder-verdict-amendment-f1f2-pending`) records the builder typing
KLADLADDER's Band-4 primary **before** its registered F1/F2 read, then amending.
**This prereg registers the ordering as a hard sequence:**
> **T1 and T2 (below) are READ, and their numbers written down, BEFORE any
> sentence containing the primary share is typed.** A primary typed ahead of the
> firings read is a REGISTRATION BREACH regardless of what it says, and the
> repair is the amendment chain KLADLADDER used, not a re-write.

**6. THIS FIXTURE PRODUCES LARGE NEGATIVES AND HAS JUST DONE SO ON THIS EXACT
BASE.** `KLADLADDER`, demo-clean, finished 41.86% at n=3,404. **A clean severance
argument predicts BEHAVIOUR and predicts nothing about SHARE.** No sentence on
this page may treat the tax's disappearance as a forecast of the number.

---

## RATIFY: Hypothesis

**Reordering the raider's own act ladder around a committed live-forward-sentinel
target — priority (step 3) below target, opportunistic (step 8, after peck and
salt) at or above it — with the bank reserve floor binding on EVERY path and NO
eco-deferral of any kind, raises our LOCAL pooled game share against
`bots/_v468kladturbo` itself to 51.33% or higher at n = 5,400 games across all 15
corefill maps and both seats.**

**Provenance:** Magnus, s48, verbatim — *"iterate on kladladder until it works."*
The underlying ladder is Magnus's s47 wording, still implemented unchanged:
*"If we have <enough> harvesters it should build 2 sentinels and peck and salt,
otherwise it builds 1 sentinel and pecks and salts until we have <enough>
harvesters, then we build the second sentinel and third."*

**The mechanism claim, stated so it can be wrong.** With the waiver gone the
plank does exactly two things and the hypothesis is that the first outweighs the
second:
* **IT PROMOTES THE FIRST SENTINEL AND SELF-HEALS IT.** Below target, planting
  holds step 3 ahead of salt, and because the target is compared against the LIVE
  census (`_live_fwd_guns`), a sentinel dying drops live below target and re-arms
  the priority — the base has no replant trigger of that kind.
* **⚠ AND IT DEMOTES THE MARGINAL SENTINEL BELOW PECK AND SALT.** At or above
  target the plant falls to step 8, which fires only if peck and salt both
  declined. **That is a REAL cost in the plank's own currency and it is the
  measured 0.82x.** The bet is that a Ti-surplus-funded first sentinel that gets
  replanted when it dies is worth more than the two marginal ones the demotion
  costs.

**⇒ A flat result is INFORMATIVE and is not a null about "sentinel ladders".** It
would say the promotion and the demotion cancel — which, combined with the two
floor arms, is what closes the family rather than leaving it open.

**PRICE OF THE THING BEING REORDERED, quoted per house rule via
`tools/scale_trace.py --price 20` (a sentinel carries +20pp of cost scale):
READING 1 (as a total, 20pp) = p0.0 SMALL; READING 2 (on top of the r100 median
of 180pp, i.e. 200pp) = p65.4 ORDINARY — inside the range teams routinely carry.
READING 2 is the primary per the tool's own instruction.** ⇒ *"expensive"* is
**not** the right adjective for the turret; the argument on this page is about
ORDERING and OPPORTUNITY, not about scale burden.

---

## REGISTRATION BLOCK

**TARGET BAND: N/A — local corefill screen with ZERO rated ladder exposure: no submission, no activation, no unrated challenge, so `tools/target_value.py` has no input. Nothing on this page ends in a ship; the only branch that reaches the ladder is a later, separately-registered head-to-head against the live holder.**
**PINNED: N/A — local self-play. The opponent version is fixed by construction: the control tree is `bots/_v468kladturbo` at the commit this shard runs from, pinned at `scratchpad/CONTROL_PIN` (`a9228ccb56ed9a65dd7d72ad1cb96068 bots/_v468kladturbo`). There is no opponent churn to pin against and no calibration relevance to protect.**
**SURFACE: local**
**PLANK CLASS: offensive — a forward-sentinel siege plank. The reorder exists to open the kill lane at the enemy ring, not to hold one at ours; nothing in the diff touches home defence, and the `DEFENCE_ADMISSION_BAR`'s r300 clause therefore does not bind. D1 (ITT timely-kill rate, stated as an EXCLUSION) is read anyway, because an offensive plank that slows the kill is still a finding.**
**KILL-ROUND NON-REGRESSION: ITT timely-kill rate over ALL 5,400 games (share ending `cond == core_destroyed` in our favour with `turns <= 300`), treatment vs control, scored as an EXCLUSION — the 95% CI on the difference must EXCLUDE a fall of more than 2.0pp. ITT RMST300 (mean of `min(turns,300)`, every non-kill scoring the full 300, `tools/fieldcal_read.py:239`) is read beside it on the same 5,400 rows. Median-crossing-300 is the gross backstop and the kill-win-conditioned share is a DIAGNOSTIC only — it carries a collider. This is D1/D2/D3 below, stated here in the registry's own vocabulary.**
**CLUSTER UNIT: none** — CLAUDE.md's enumeration PERFORMED, not asserted: (i) the **MATCH** cluster does not exist on this surface — `tools/overnight.sh` writes one TSV row per `fcode run`, so 1 row = 1 game and no row shares a match with another; (ii) the **OPPONENT** cluster is degenerate — every one of the 5,400 rows plays the identical control tree, so the pooled stratum holds exactly one opponent and there is no between-opponent variation for a design effect to describe. Both clusters die ⇒ DEFF = the measured local constant **0.98** (pair-weighted, ρ = −0.020, 124 shards, s39 audit), i.e. naive intervals are correct and marginally conservative. **The platform constants (1.529 rated / 1.833 unrated) are NOT applicable and applying them would widen every interval here 24-35% for correlation that has been measured absent.** ⚠ **The s42 cross-host rider is registered: the 0.98 exemption is a WITHIN-HOST measurement. This arm is registered as a single-host cell and nothing on this page pools across hosts; a remote replication, if stocked, is REPORTED SEPARATELY and NEVER POOLED (the GUNAXABL/SENTTHR precedent).**
**ESTIMATOR: unweighted pooled treatment game share** = (rows with `winner == T`) / (completed rows), over all 5,400 rows, both seats pooled, all 15 maps pooled, no reweighting. Interval by `tools/cluster_ci.py` with the local constant. Seat A and seat B shares are reported SEPARATELY as a fixture diagnostic and are never the bar — seat is worth ~6.8pp on byte-identical arms, which is why the n is a multiple of 30.
**DOSE: forward-sentinel plants per game — treatment 1.23 vs control 1.49 (0.82x; paired diff −0.267/game, 2×SE 0.476, n=120 paired, `tools/dose.py --kind sentinel`, recorded in `e2a71410`). ⛔ THIS DOSE IS OBSERVABLE-AT-LOCK, NOT PRE-REGISTERED, AND IT READS *NOT ELEVATED*. It is registered as the arm's honest prior and NOT as a delivered dose. The delivered-dose question for THIS arm is the TIMING/ORDERING read T2 below, because a reordering plank whose net count is flat is exactly the case a count-only dose cannot see. Companion prior, same instrument, same n: builder deaths 1.70 vs 1.73 (0.98x, paired diff −0.033) against `_v473kladladder`'s 1.30x [+0.008, +0.925] — the commitment tax is gone at the point estimate.**
**PLANNED n: 5400 games** (= 15 maps × 2 seats × 180, so map and seat balance is exact; `tools/overnight.sh:68` has carried the 15-map pool since the 2026-08-13 rotation and its own comment requires multiples of 30).
**BOUNDARY: 5400 games** — LOCAL surface, one tape row is one game; there is no accept/attempt distinction on this fixture. ⛔ **A LINE COUNT IS NOT A ROW COUNT**: this tape carries an unprefixed header line, and a naive `wc -l` / `awk '!/^#/'` over-reports n by exactly one (measured on KLADLADDER itself, `results.tsv:474`). The registered denominator is **DictReader row count, cross-checked against the heartbeat and against `max(game id) + 1`.**
**CUT-SHORT: floor 2700 games.** Below 2,700 completed tape rows this leg publishes descriptive tallies (share, per-seat, per-map, kill-clock) and takes **NO comparative look and no bar verdict**; the half-width at 2,700 is ±1.87pp, already wider than the 1.33pp margin the bar is built on, so a sub-2,700 read cannot resolve its own branches. An `auto_gate` cancellation at CATASTROPHE@400, MARK-1000 or TREND-FLOOR@1000 is an **OPERATIONAL STOP, not a verdict**, and is typed `cancellation`. ⭐ **ONE CARVE-OUT, PRE-COMMITTED, AND IT IS THE ONE KLADLADDER USED:** a CATASTROPHE-clause cancellation (95% CI upper < 45.0 at n ≥ 400) is arithmetically INCOMPATIBLE with every band above Band 4, so a stop under that clause DOES license the Band-4 falsifier sentence at the partial n — **provided T1/T2 have been read first**, and provided the partial share is disclosed as **selected-pessimistic** if the stop was taken on an interim look.
**BAR: 51.33. MDE: 0.00pp — THIS IS A POINT RULE ONLY AND LICENSES NO EXCLUSION CLAIM ABOUT AN EFFECT SIZE.** Per the OB16 corollary (obligations doc, 2026-08-15T03:52:45Z): the standard corefill band IS `50 ± half_width` at n=5,400, so clearing 51.33 puts the CI's lower edge at exactly 50.00 — it excludes 50 and excludes **no positive effect size whatsoever**. n for the exclusion it CAN make (bar ≠ 50.0): **5,400**, which is the planned n.
**BASE RATE: 50.00**
**BAR SOURCE:** house-standard corefill futility band, `50 + 1.96*sqrt(.25/5400) = 51.33pp`, local DEFF 0.98 so naive — the identical bar carried by `docs/prereg/BARS.tsv` rows `SEALFLOOR6`, `SENTTHR`, `KLADTKILL`, `KLADTK2`, `KLADTURBOR`, `DRAINTURBO`, `KLADLADDER`, `SEALSENTAN`, `SEALSENTA` and `ECOMMIT`, which is what keeps this arm numerically comparable to the sentinel-family reads it exists to extend. **Constructed, not observed.**
**BASE RATE SOURCE:** structural A/A expectation of a seat-balanced, map-balanced self-play fixture whose control tree is the treatment's own base. Empirically calibrated by `IDNULL140` — **49.27% [47.94, 50.60] at n = 5,400**, 2026-08-16T18:02:04Z, same fixture (`results.tsv:454`) — and by `NULL125` — **51.04% at n = 5,400** (`results.tsv:346`). Two A/A cells, one either side of 50.0, both intervals containing it. ⇒ **a bare clearance in [51.33, 52.4] is a band an A/A cell has already produced**, which is why Band 2 below is pre-registered as WEAK.
**POOL ERA: post-2026-08-13-rotation** — the 15-map local pool of `tools/overnight.sh:68` (`antler archipelago auroraveil drakkarfjord drumlin fjordgate frostgate glacierkeep icefloe midgard nordkap ragnarok royale valkyrie yulerune`). (`check_pool_era` treats this as n/a on a LOCAL surface per SPEC §6; declared anyway so the population is on the page.) ⚠ **AND IT IS NOT COSMETIC: the n=120 dose battery is a `tools/dose.py` run on that tool's own 8-map default rotation, NOT the 15-map screen pool.** The prior in DOSE was therefore measured partly on geometry the screen never plays — which is one of the two reasons T1 re-reads dose on the screen pool.
**REFERENCE n: none** — the comparator is generated inside this same shard from the same 5,400 seeds; there is no fixed external reference sample, so no resolution floor at n→∞.
**TREATMENT TREE: bots/_v482kladladder2**
**TREATMENT DIFF REFS: e2a71410^ e2a71410**
**MECHANISM METRIC READS: bots/_v482kladladder2/raid.py:455 — `if not fwd_priority and self._try_forward_sentinel(ct, E, live=fwd_live):`, the step-8 OPPORTUNISTIC call site. This line IS the plank: it exists nowhere in the control, it is reachable only when `fwd_priority` is False, and its existence is what demotes the marginal plant below peck and salt. Companion read line: `bots/_v482kladladder2/raid.py:370` — the step-3 call site, now guarded by `fwd_priority` where the base's is unconditional. Observed as T1 (forward-sentinel builds/game on the SCREEN pool) and T2 (the ROUND distribution of forward sentinel BUILD events, treatment vs control — the only decodable signature of a REORDERING whose net count is flat). TREATMENT DIFF TOUCHES: bots/_v482kladladder2/doctrine.py bots/_v482kladladder2/raid.py. INTERSECTION: yes — `raid.py:455` is inside the hunk the diff ADDS at `raid.py:443-455`, and `raid.py:313-332` (the whole `fwd_priority` computation) is likewise new; a `grep -c` for `fwd_priority`, `waive_floor` and `fwd_waive` over the CONTROL tree's raid module returns **0**, against 12 in the treatment, verified at draft. The metric CANNOT read identically in both arms.**
⚠ **DIFF-REFS DISCLOSURE:** `e2a71410` ADDS the whole tree plus an ADD-ONLY `--tsv` flag on `tools/dose.py`, so `git diff --name-only e2a71410^ e2a71410` returns FIVE paths. The SEMANTIC diff against the control is TWO files: `diff -rq bots/_v468kladturbo bots/_v482kladladder2` names `doctrine.py` and `raid.py` only, and **`eco.py` and `main.py` are byte-identical** (verified at draft). `TREATMENT DIFF TOUCHES` declares the semantic two.
**METRIC WINDOW: r0-r1000. GATING CONSTANTS: LOKI_LADDER_POST_HARV=3, LOKI_FWD_SENT_MIN_PRE=1, LOKI_FWD_SENT_MIN_POST=2, LOKI_FWD_MIN_HARV=2, LOKI_FWD_TI_FLOOR=40, LOKI_FWD_GUN_CAP=3, LOKI2_RUSH_MIN_HARV=0, LOKI2_RUSH_TI_FLOOR=8. MECHANISM CAN OCCUR IN WINDOW: yes** — **NOT ONE of these is a ROUND FLOOR.** `LOKI_LADDER_POST_HARV`, `LOKI_FWD_MIN_HARV` and `LOKI2_RUSH_MIN_HARV` are HARVESTER COUNTS; `LOKI_FWD_SENT_MIN_PRE/POST` and `LOKI_FWD_GUN_CAP` are TURRET COUNTS; `LOKI_FWD_TI_FLOOR` and `LOKI2_RUSH_TI_FLOOR` are TITANIUM amounts. The plank has **no round gate whatsoever**: `fwd_priority` is recomputed every raider turn from `SLOT_HARVESTERS` and the live census, so both slots are live from the first turn a raider acts, and the self-healing replant can fire at any round.
⚠ **DISCLOSED, because a green tool run with warnings under it is how a warning stops being read: `prereg_check.py` will emit `OBLIGATION 17, PARTIAL WINDOW` warns against the line above and THEY ARE ARTEFACTS OF THE CHECKER.** Its `check_metric_window` arithmetic reads every declared integer as a ROUND, so a harvester count of 3 is reported as "rounds r0-r2 cannot contain the mechanism". The constants are declared anyway because they are the gates that actually bind, and an undeclared gate is the failure the obligation exists for.
**PRE-STATE: the predicted-change set is NOT already in the target state at lock.** Verified at draft against the control tree: `grep -c LOKI_LADDER_ON bots/_v468kladturbo/*.py` → **0** in `doctrine.py`, `eco.py`, `main.py`, `raid.py`; `grep -c 'fwd_priority\|waive_floor\|fwd_waive' bots/_v468kladturbo/raid.py` → **0**. The control's step 3 is UNCONDITIONAL and it has no step-8 slot, no live-census target, no self-healing replant and no `LOKI_LADDER_*` constants. **The behaviour this leg predicts to change therefore cannot already be in the target state.** ⚠ And the comparative claim the floor family exists for — *"the ordering alone pays"* — is likewise NOT pre-satisfied: `_v473`'s 41.86 is the SAME ordering plus a waiver, so it constrains the pair and not this arm.
**MAP SEGMENT: none expected** — the mechanism is a per-turn PRIORITY decision inside one raider's act ladder, evaluated from a harvester count, a live turret census and a bank balance. **None of those three is a terrain property**, and there is no map-conditional branch anywhere in the diff (`raid.py:313-332` reads only `SLOT_HARVESTERS`, `SLOT_FWD_GUN`, the round and the live census). What terrain changes is the raider's ARRIVAL LATENCY and the eco curve's slope, i.e. WHEN the rungs arm — not WHETHER the reorder binds. **No map cut may rescue this arm.** Per-map shares WILL be printed at readout as exploratory description; they carry no pre-registered direction and nothing may be banked off them without a fresh prereg. ⚠ **One candidate segment is named here and DELIBERATELY NOT REGISTERED**: the five 900-area maps (midgard, ragnarok, valkyrie, drakkarfjord, glacierkeep), where the longest approach means the demotion bites latest. Registering it would hand this arm a second chance to pass, which is OB15b's exact prohibition; if the pooled read fails and that cut looks alive, it needs its OWN leg with its OWN n.
**CELL VERSION CHURN: N/A — not a panel, no `CELLS:` line, one fixed local control tree.**
**GATE RESOLUTION: the shard is governed by the pinned `tools/auto_gate.py` marks — CATASTROPHE@400 (STOP if the 95% CI upper < 45.0, `auto_gate.py:236`), MARK-1000 (STOP if the CI upper < the registered BAR 51.33), TREND-FLOOR@1000 (STOP if the first-1,000 prefix share < 52.0, `auto_gate.py:250` — RAISED from 51.0 by Magnus 2026-08-16), and the same floors again at MARK-2700 (`auto_gate.py:233-236`). Those are Magnus's confirmed constants and their firings are OPERATIONAL CANCELLATIONS that free a core — typed `cancellation`, never `verdict`, licensing NO exclusion claim (with the single CATASTROPHE carve-out written into CUT-SHORT above). ⭐ THE REMOTE LIMITATION IS DEAD AND THAT CHANGES THE ROUTING RULE THIS FAMILY CARRIED: `auto_gate.py:113` was REPORT-ONLY on a worker — which is why KLADLADDER ran to n≈3,404 at 41.86 with no automatic stop — but commit `a50f27ef` gave `auto_gate --apply` a guarded remote stop path (`tools/remote_cancel.py`), so THE STRICT FLOORS NOW BIND ON ws1/ws2 TOO. ⇒ this shard may be routed LOCAL or REMOTE at the builder's discretion; what is registered is that **it runs on ONE host and is never pooled across hosts** (the s42 cross-host rider), and that a remote route switches the second clock to the registered first-completed-row backstop. The RESOLVABLE gate this document owns is the primary at full n, whose margin (1.33pp) exceeds its own half-width (±1.32pp) by 0.01pp — resolvable, and only just. Everything else on this page (T1, T2, D1-D3, the seat and map splits) is DIAGNOSTIC and cannot rescue a failed primary. Any branch that does not resolve is UNRESOLVED, and an UNRESOLVED gate defaults to the RESTRICTION: no promotion, no ship conversation, no combination claim.**

---

## FALSIFIER

**PRIMARY FALSIFIER: at n = 5,400 the 95% CI UPPER bound on the treatment's
pooled game share falls BELOW 51.33.** That excludes the bar and says the
ordering does NOT add measurably to Sleipnir **even with the commitment tax
fully severed**.
**Consequence, registered in advance and split by how far it falls:**
* **CI upper < 51.33 but CI contains 50.0** → the reordering is INERT. See
  Band 3.
* **CI upper < 50.0** → **the DEMOTION costs.** The step-8 relegation of
  sentinels #2 and #3 is a real subtraction, and the ladder-as-ordering road is
  closed on its own evidence rather than by inference from `_v473`.

**MECHANISM FALSIFIER (independent of the primary, and it can fire first).**
⛔ **IT IS DELIBERATELY NOT WRITTEN AGAINST THE COUNT, BECAUSE THE COUNT ALREADY
CAME BACK FLAT-TO-LOW AND THAT IS THE PREDICTED SHAPE.** A count-denominated
mechanism falsifier on a reordering plank would fire on the arm's OWN prediction
and would be unfalsifiable in the useful direction. **The falsifier is T2:** if
the ROUND distribution of forward-sentinel BUILD events is indistinguishable
between arms — i.e. the plants land at the same times as the control's, not just
in the same numbers — then nothing about the act ladder was actually reordered in
play, the plank did not deliver its dose, and **the primary is uninterpretable in
either direction**: a flat share would mean "the reorder never bound", not "the
reorder bound and did not pay". Per FIRINGS-BEFORE-PRIMARY this is read BEFORE the
primary is typed, and if it fires the primary is reported as **NOT MEASURED**
rather than as a null. **This is not hypothetical: s47's delta D2 records a
wiring null escaping demos to a 436-game shard.**

---

## READING, PRE-COMMITTED — four bands, written before the data

Registered now so no band is chosen after the fact. **Read TOP-DOWN; the first
row whose condition holds is the reading. The rows are disjoint by construction.**

| # | band at n = 5,400 | pre-committed reading |
|---|---|---|
| **1** | **CI lower ≥ 51.33** | **THE ORDERING ADDS.** Real and resolved on this fixture, and it adds while planting FEWER sentinels than the control — which would make this a scheduling finding, not a volume one. Promotes to a combination input and to a separately-registered head-to-head against the live holder. ⚠ Report the size with its OB16 status: the standard band has MDE 0, so this branch may claim "we can exclude 50" and may NOT claim any minimum effect size. |
| **2** | **point ≥ 51.33 but CI lower < 51.33** (includes the whole [51.33, 52.4] window an A/A cell has already produced) | **REAL-BUT-SMALL, COMBINATION INPUT ONLY.** Registered in advance as WEAK: `NULL125`'s byte-identical A/A read 51.04, so a bare clearance here is not distinguishable from fixture noise by this leg alone. Rows are KEPT and the arm is available for combination; it does NOT license a ship conversation, and a replication on fresh seeds is the price of promoting it. |
| **3** | **point < 51.33 AND CI contains 50.0** | **PARITY — THE ORDERING IS INERT, AND THAT CLOSES A CORNER RATHER THAN LEAVING ONE OPEN.** Combined with `_v473`'s 41.86 at floor 0 and with `KLADLADDER3`'s read at floor 16, the three-corner floor ladder (0 / 16 / 40) is then fully read and the FAMILY CLOSES: the waiver was the whole effect, it was negative, and the ordering underneath it is worth nothing. ⛔ **THE CLOSURE IS ONLY LICENSED WHEN ALL THREE CORNERS HAVE BEEN READ** — this arm alone licenses "the ordering is inert" and NOT "the family is closed". |
| **4** | **CI upper < 50.0** | **THE DEMOTION COSTS.** Relegating sentinels #2 and #3 below peck and salt is a net subtraction from Sleipnir. The ladder-as-ordering is dead as a ship candidate; ⛔ do NOT respond by re-adding a waiver to rescue the number — a smaller floor is a DIFFERENT plank with its own registration, and it already has one (`KLADLADDER3`). |

⚠ **Rows 3 and 4 both fire the PRIMARY FALSIFIER**; the falsifier's consequence
sentence is the one above, and the band decides which half applies.
⚠ **Nothing here treats 50.0 as a floor.** A share below 50 is a live outcome with
a named mechanism (strictly fewer plant opportunities for turrets #2 and #3) and
it is pre-named so a negative is not explained away as noise.

---

## MECHANISM DIAGNOSTICS TO READ AT READOUT

**Measurability is declared per metric. `NOT MEASURABLE` is written where it is
true, rather than a metric being quietly renamed into something the tape happens
to carry.**

### ⛔ ORDERING, REGISTERED AS A HARD SEQUENCE
**T1 and T2 run and are written down BEFORE any sentence containing the primary
share is typed.** See READ-BEFORE-RATIFYING #5 for why this clause is in bold.

### T1 — DOSE ON THE POOL THE SCREEN PLAYS. MEASURABLE, but NOT off the shard tape.
`tools/overnight.sh:138-139` passes `--replay /dev/null`, so the KLADLADDER2 shard
produces **no** entity events. T1 runs on a **separate serial battery**:
```
.venv/bin/python tools/dose.py bots/_v482kladladder2 --kind sentinel \
    --ctrl bots/_v468kladturbo --games 120 --tsv scratchpad/dose_v482_screenpool.tsv \
    --maps antler archipelago auroraveil drakkarfjord drumlin fjordgate frostgate \
           glacierkeep icefloe midgard nordkap ragnarok royale valkyrie yulerune
```
**REGISTERED SIZE: 120 games, SERIAL** (never parallel: D65, `tools/dose.py:26-30`).
⛔⛔ **AND THE REGISTERED SIZE IS WRITTEN OUT IN THE COMMAND BECAUSE OF THE EXACT
FAILURE THIS FAMILY JUST HAD: `tools/dose.py`'s `--games` DEFAULTS TO 24, and
KLADLADDER's registered 120 silently ran as 24, producing the 2.11x artifact that
stood as an attribution for 34 minutes (`results.tsv:475`). `--games 120` is not
optional on this page and its absence from the shell history is a registration
breach.**
**Pre-registered expectation: T1 reproduces the pre-lock prior — treatment
forward-sentinel builds/game AT OR BELOW control, with the paired difference
INSIDE the tool's own 2×SE band. A count ABOVE control on the screen pool is a
SURPRISE and must be written down as one before it is explained** (CLAUDE.md's
point 4). **T1 is not a pass/fail gate for this arm** — a flat count is the
prediction — but a count that moves either way changes what T2 is read against.

### T2 — THE ORDERING READ. THIS IS THE ARM'S REAL DOSE, AND IT IS NOT YET EXECUTABLE.
The discriminator for a REORDERING is **WHEN** the plants land, not how many.
`tools/corpus/replay_events.py` emits one row per build with columns
`file ev rnd team kind x y d2_own d2_enemy mw mh`, so the read is:
```
.venv/bin/python tools/corpus/replay_events.py OUT.tsv <replays…>
# rows with ev == BUILD and kind == sentinel, grouped by team:
#   (a) round of the FIRST forward sentinel, per game, treatment vs control
#   (b) the full round histogram of sentinel BUILD events
```
**Pre-registered expectation, with its sign, because a segment or a distribution
declared without a direction is unfalsifiable:** the treatment's FIRST forward
sentinel lands **NO LATER** than the control's (the priority slot at step 3, which
below target outranks salt), while its SECOND and THIRD land **LATER** than the
control's (the step-8 demotion). **Both halves in one distribution is the
signature of a reorder; a distribution identical in both arms is the MECHANISM
FALSIFIER firing.**

⛔ **OB17 — THIS READ IS NOT EXECUTABLE OFF A `tools/dose.py` RUN, AND THE BUILDER
MUST FIX THAT BEFORE THE BATTERY FIRES. THIS IS THE CLAUSE ON THIS PAGE THAT CAN
STILL SURPRISE THE PERSON RUNNING IT; RUN IT FIRST.**
1. **NAME THE EXECUTING TOOL** — `tools/dose.py` for T1, `tools/corpus/replay_events.py`
   for T2.
2. **CONFIRM THE PATH EXISTS IN THAT TOOL** — it does NOT. `tools/dose.py:157`
   calls `rp.unlink(missing_ok=True)` on every replay immediately after decoding,
   and **there is no `--keep`** (this is already logged as wrap debt 20). The
   `--tsv` flag added in `e2a71410` carries **counts only, no round column** —
   which is precisely why `results.tsv:476` (`kladladder-f1-timing-status`)
   records the timing half of KLADLADDER's F1 as **NOT MEASURABLE FROM RETAINED
   OUTPUT**. ⇒ T2 requires either (a) a `--keep` flag added to `tools/dose.py`
   before the battery runs, or (b) its own small serial loop that passes
   `--replay <unique path>` and retains the files.
3. **CONSEQUENCE OF SILENT NON-EXECUTION** — if T2 is skipped, the ONLY dose
   evidence for this arm is a count that is predicted to be flat, i.e. **no
   evidence that distinguishes a working reorder from a dead one.** In that case
   the primary must be typed with **"MECHANISM NOT VERIFIED"** attached, and
   Bands 3 and 4 may NOT be attributed to the ordering.

### D1-D3 — the kill-clock read. MEASURABLE, shard-native (`cond`, `turns`, `winner`).
* **D1 — TIMELY-KILL RATE (the `DEFENCE_ADMISSION_BAR` primary), ITT.** Share of
  ALL treatment-seat games ending `cond == core_destroyed` in our favour with
  `turns ≤ 300`, treatment vs control, both on the same 5,400 rows.
  **Non-regression is the bar and it is stated as an EXCLUSION, per CLAUDE.md's
  fail-to-exclude clause: the 95% CI on the difference must EXCLUDE a fall of more
  than 2.0pp.** A "no significant rise" phrasing is not admissible.
* **D2 — MEDIAN KILL ROUND**, treatment vs control, as the gross backstop (a
  median crossing 300 is disqualifying), reported alongside the r1000 share since
  `R1000_IS_DEFEAT` makes an r1000 game a cost even when its tiebreak is won.
  Anchor: KLADTURBO's own local full read had median kill 193
  (`results.tsv:466`, 61.09% [59.79, 62.39] n = 5,400 vs `_v223sealrepair`).
* **D3 — RMST300, ITT** — mean of `min(turns, 300)` with every game not ending in
  OUR core kill scoring the full 300 (`tools/fieldcal_read.py:239`, the registered
  estimator). Reported with its interval from `tools/cluster_ci.py`. **ITT over
  ALL rows, not over kills only** — the kill-conditioned form carries a collider,
  per `PROGRAMME.md`.

### NOT MEASURABLE on this leg — named, not silently dropped.
* **Builder deaths at screen n.** The 0.98x prior is a 120-game battery figure
  with no interval published on the ratio; the shard tape has no unit events, so
  **the death tax's disappearance is NOT re-confirmed by this leg** and no readout
  sentence may claim it was. A death read requires its own retained-replay battery.
* **Whether the demoted plants would have paid.** The counterfactual "the
  sentinel step 8 declined to build" is not observable — a non-event leaves no
  row. **The plank's most plausible cost channel is therefore UNOBSERVED except
  through T2's round histogram.**
* **Per-unit CPU.** Local replays zero-fill `execTimeUs` (the s42 D33 instance:
  `tle_census.py` returns 0 across 1,649 local builder-turns while reading 8,847 µs
  on platform replays), so **no CPU claim is available from this leg.**
* **Seed determinism.** `NOISE_ON` pins an unseeded per-unit salt and raiders gate
  on `get_cpu_time_elapsed()`, so base-vs-base at one seed diverges at round 0.
  **No seed-matched or replay-diff equivalence claim is available on this
  fixture.** ⭐ **The flag-off equivalence claim is made ON THE CODE and on an
  AST-NORMALISED DIFF, never on a replay comparison**: `e2a71410`'s build record
  states the comment/docstring-stripped diff against `_v468kladturbo` at **0
  executable-line deltas in `eco.py`, 0 in `main.py`, 26 in `raid.py`, 4 in
  `doctrine.py`**, and `diff -q` confirms `eco.py` and `main.py` byte-identical
  (verified at draft). With `LOKI_LADDER_ON = False` the else-branch at
  `raid.py:326-332` sets `fwd_priority = True` and `fwd_live = _FWD_LIVE_UNSET`,
  so step 3 reduces to the base's own call and step 8 short-circuits without
  calling. ⚠ **The commit itself records that the EMPIRICAL version of this check
  is unrunnable on this fixture and that a base-vs-base control fires the same
  "not equivalent" verdict — the construction argument is load-bearing precisely
  because the measurement cannot be made.**

---

## THE CHANGE — `file:line`, control → treatment

**TREATMENT TREE: `bots/_v482kladladder2`** — `bots/_v468kladturbo` plus one plank
across two files. Verified at draft: `diff -rq` names exactly `doctrine.py` and
`raid.py`; **`eco.py` and `main.py` are byte-identical.**

1. **`doctrine.py` +1266-1391** — the KLADLADDER doctrine block, the KLADLADDER2
   severance block, and **four** constants: `LOKI_LADDER_ON = True` (`:1324`),
   `LOKI_LADDER_POST_HARV = 3` (`:1325`), `LOKI_FWD_SENT_MIN_PRE = 1` (`:1326`),
   `LOKI_FWD_SENT_MIN_POST = 2` (`:1327`). **`LOKI_FWD_TI_FLOOR` stays at its base
   value of 40 (`:1264`) — that is the constant `KLADLADDER3` manipulates and this
   arm does not.**
2. **`raid.py:69-70`** — `_FWD_LIVE_UNSET`, a private sentinel distinct from a real
   `None` (which already means "blind, fall back to the monotone store").
3. **`raid.py:267-332`** — the `fwd_live` / `fwd_target` / `fwd_priority`
   computation, once per raider turn, with the flag-off else-branch at `:326-332`.
4. **`raid.py:370`** — step 3, now `if fwd_priority and self._try_forward_sentinel(…)`
   where the base's call is unconditional.
5. **`raid.py:443-455`** — step 8, the OPPORTUNISTIC slot, after peck AND salt.
   **This block does not exist in the control at all.**
6. **`raid.py:738-816`** — `_try_forward_sentinel` gains the `live=` parameter and
   **LOSES the `waive_floor=` parameter of `_v473kladladder`, deleted rather than
   defaulted off.** `raid.py:775` computes `ti_floor` and `raid.py:788`
   (`if ct.get_global_resources() < cost + ti_floor: return False`) now binds on
   EVERY call from EVERY slot. The plant itself lands at **`raid.py:816`**.

---

## WHAT THIS LEG COSTS AND WHAT IT DOES NOT

**Cost: one core to n = 5,400, plus 120 serial games for T1 and a retained-replay
battery for T2.** ZERO rated ladder exposure, zero submissions, zero unrated
challenges — nothing on this page touches the platform, which is why `TARGET BAND`
is N/A rather than a number.

**It does NOT decide a ship.** The strongest branch promotes the arm to (a) a
combination input and (b) a separately-registered head-to-head against the live
holder, which is the pipeline step Magnus's procedure names verbatim (*"we start
by testing it against the current slot, If it beats it we can switch"*) and which
`SLEIPH2H` is the template for. **A local screen against the benchmark is gate 1;
gate-1-to-gate-2 transitivity is UNVALIDATED in this repo (QUEUE #65: 3 concordant,
1 not), so the head-to-head is not skippable on the strength of this number** —
and the benchmark is not the holder, so `ODINVSSLEIP` is the converter between
this page's units and the ladder's.

**It is one corner of a THREE-CORNER FLOOR LADDER.** `LOKI_FWD_TI_FLOOR` = **0**
(`_v473kladladder`, waived — READ, 41.86% [40.20, 43.52] at n = 3,404), **16**
(`bots/_v485kladladder3`, `docs/prereg/PREREG-KLADLADDER3-2026-08-17.md`), **40**
(this arm, the base's own floor). **No single corner closes the family; all three
read is what does.** For the corner-to-corner comparison to mean anything the two
un-read corners must run **on the same host at the same planned n** — see the
cross-host rider in the obligations doc (Addendum 11 rider, 2026-08-15): the 0.98
exemption is a WITHIN-HOST measurement and does not cover cross-host pooling.

---

**PROVENANCE:** `docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md` (read in full: OB1, OB7, OB12, OB13, OB14, OB15a/b/c, OB16 + its corollary and cross-host rider, OB17 + its rider) · `docs/prereg/PREREG-SEALSENTAN-2026-08-17.md` and `docs/prereg/PREREG-ECOMMIT-2026-08-17.md` (today's house style, both read in full) · `docs/prereg/BARS.tsv` (header, the FIRINGS-BEFORE-PRIMARY rule, and the sibling klad/sealsent/ecommit-family rows) · `CLAUDE.md` · `tools/prereg_check.py` (read for `RULES`, `DEFF`, `check_metric_window`, `check_pool_era`) · `tools/auto_gate.py:113,233-236,250` · `tools/overnight.sh:68` (the 15-map pool), `:99,103,110` (the FIXTURE stamp and its legacy-resume form), `:104` (the tape column header), `:118-120` (the row-count rule), `:138-139` (`--tle 10 --replay /dev/null`) · `tools/dose.py` (`:26-30` serial rule, `:157` the replay unlink, and the `--games` default of 24 that produced the 2.11x artifact) · `tools/corpus/replay_events.py` (the `rnd` column that T2 needs) · `tools/scale_trace.py --price 20` (run at draft; READING 2 = p65.4 ORDINARY) · `bots/_v482kladladder2/{doctrine,raid}.py` · `bots/_v468kladturbo/{doctrine,eco,main,raid}.py` · `bots/_v473kladladder/doctrine.py` · git commits `e2a71410` (full body, which carries the n=120 dose) and `e9e40548`, and `git diff --name-only e2a71410^ e2a71410` · `scratchpad/kladladder_dose.log` (the n=24 battery, quoted only as the artifact it is) · `scratchpad/corefill_work.txt` · `scratchpad/CONTROL_PIN` · `results.tsv` (rows 346 `null125-final`, 454 `idnull140-cert-5400`, 466 `kladturbo-local-confirm-5400`, 470-476 the seven `kladladder-*` rows) · the drafting brief supplied by the builder lane s48. No file under `bots/`, `tools/`, `scratchpad/`, `docs/prereg/BARS.tsv`, `results.tsv`, `HANDOVER.md`, `PROGRAMME.md` or `QUEUE.md` was created or modified by this agent, and no game was run.
