# SCREEN PREREG — `FREEROUND`: the chase-oscillation detector, generalised into `_nav`

Drafted by a fresh opus subagent with no inherited session context beyond the
inputs listed under `PROVENANCE`. The builder lane ratifies the judgment lines
and types the lock commit; this agent wrote no code under `bots/`, appended no
worklist row, appended no `BARS.tsv` row, fired no game, started no shard, and
touched neither `results.tsv` nor `HANDOVER.md` nor `PROGRAMME.md` nor
`QUEUE.md`.

**STATUS: committed BEFORE the `FREEROUND` row is appended to
`scratchpad/corefill_work.txt`, BEFORE any file named
`scratchpad/overnight/FREEROUND.*` exists, and BEFORE the leg's first game.**
Drafting session wall clock at write time **`2026-08-17T05:36:44Z`** (`date -u`,
same shell call); repo HEAD at draft `7bcf0e5e` (author time
`2026-08-17T07:35:55+02:00`). Verified at draft:
`grep -c 'FREEROUND' scratchpad/corefill_work.txt` → **0**; same grep on
`docs/prereg/BARS.tsv` → **0**; `ls scratchpad/overnight/ | grep -i freeround` →
**empty**; `grep -cE '8(16|18|20)000' scratchpad/corefill_work.txt` → **0** (the
seed base is free).

### SECOND CLOCK — registered in the CONSERVATIVE form

**REGISTERED SECOND CLOCK: the `ts` of the FIRST COMPLETED ROW of
`scratchpad/overnight/FREEROUND.tsv`.** Conservative by construction: the shard's
true start is strictly earlier than its first completed row, so the reported
lock-to-fixture gap can only be UNDERSTATED. ⚠ **The brief's stated reason for
avoiding the tighter clock did NOT survive my check and is corrected rather than
repeated:** `tools/overnight.sh:99-104` computes `START=$(date -u …)` and writes
`# FIXTURE\t…\tstart=$START` as the tape's FIRST LINE before the first
`fcode run`; the heartbeat is a SEPARATE file and overwrites nothing on the tape.
⇒ **that stamp WILL exist on this local shard and is registered as a
CORROBORATING clock, not the primary.** If the tape instead carries
`# FIXTURE-RESUME … start=UNKNOWN-legacy-tape` or no `# FIXTURE` line, the
registered first-completed-row clock stands alone and nothing changes.

⚠ **The treatment tree ALREADY EXISTS and is committed** (`bots/_v478freeround`,
added `2bf5f9e3`, author time `2026-08-17T07:29:53+02:00`). This document is
therefore **NOT** locked before the arm exists, only before the arm's first
screen row. It is also what makes Obligation 13's intersection **computable at
lock time**.

---

## ⛔ READ BEFORE RATIFYING — SIX THINGS THE LANE OWNS

**1. THE CONTROL IS THE LIVE INCUMBENT, SO 50.0 MEANS "ADDS NOTHING".**
`bots/_v468kladturbo` is Sleipnir v1, pinned at `scratchpad/CONTROL_PIN`
(`a9228ccb56ed9a65dd7d72ad1cb96068 bots/_v468kladturbo`) per Magnus's benchmark
ruling. **A reader carrying a 61-shaped intuition from the KLADTURBO-vs-v140 read
onto this page has misread the fixture: the same bot measured against itself
reads 50.**

**2. TWO ARMS IN THIS FAMILY ARE ALREADY DEAD, AND THAT IS WHY THE PLANK'S SHAPE
IS DIFFERENT.** `OSCLOCK` **48.53% @ n = 1,867** and `OSCLOCK2` **46.49% @
n = 1,809** — both detect-and-**RE-PICK** arms, both cancelled by the gate below
the null (`docs/research/CLOSURES-s43-2026-08-15.md:40`; the numbers are
CANCELLATION checkpoints, not full-n verdicts, and are quoted as such). The
standing ruling out of that family is explicit: **any successor must change
NAVIGATION or DESTINATION, not detection** (`BUILDER-TACTICS-ATLAS-2026-08-14.md:165`).
**This arm changes MOVE LEGALITY and never touches the target.** ⇒ The prior for
this family is BAD and the mechanism has been re-shaped in the direction the
closure demanded; both halves of that sentence belong in the readout.

**3. ⚠ THE PLANK IS NOT PURE NAVIGATION AND MUST NOT BE DESCRIBED AS IF IT WERE.**
A trip also executes `self.stuck += 1` (`bots/_v478freeround/eco.py:1512`), and
the forced-step path does the same (`eco.py:1566`). That feeds the PARENT'S OWN
escape hatch at the PARENT'S OWN threshold (`stuck >= 5` → re-pick a different
ore, in `_expand`). **It is bounded by that threshold and it is still a
BEHAVIOUR CHANGE BEYOND NAVIGATION: re-picks become more frequent, which is
exactly the lever the two dead arms pulled directly.** Named here, before the
data, so a negative cannot be re-described afterwards as "we only changed
movement".

**4. THE DEMO'S OSCILLATION NUMBER MOVED ITS OWN DENOMINATOR, AND THE READOUT
MUST CARRY BOTH TERMS.** Pooled two-cycle share 23.2% (2,661 / 11,448) vs control
44.5% (6,610 / 14,860) over 16 sides each. **The arm's total builder moves are
23% LOWER than the control's** (11,448 vs 14,860), so part of the share
improvement is a denominator change. **The absolute count fell further than the
share did (−60% vs −48%), so the direction survives the correction — but a
readout quoting only the share is quoting a ratio whose bottom half also moved.**

**5. THE SHARD TAPE CANNOT SEE THE MECHANISM, SO A FIRINGS READ IS MANDATORY
BEFORE THE PRIMARY.** `tools/overnight.sh:138-139` runs every game with
`--replay /dev/null`; the tape's columns are
`ts shard game map seed seat winner cond turns` — **no movement, position or
stdout information exists on it, in either arm.** The mechanism is CONDITIONAL (a
detector that trips, then a bounded ban), so `docs/prereg/BARS.tsv`'s
FIRINGS-BEFORE-PRIMARY rule (adopted 2026-08-16T13:27:33Z) binds: **F1-F3 run on
a SEPARATE battery that keeps replays and are read BEFORE the primary sentence is
typed.** What the tape CAN answer is the kill-clock question (`cond`, `turns`,
`winner`), which is why D1-D3 are shard-native and F1-F3 are not.

**6. THIS FIXTURE PRODUCES LARGE NEGATIVES AND HAS JUST DONE SO.** `KLADLADDER`,
demo-clean on this same base with this same flag-off SHA method and its dose
confirmed delivered, finished **41.86% [40.20, 43.52] at n = 3,404**
(`results.tsv`, `kladladder-n-final-correction`, 2026-08-17T05:18:10Z). **A clean
demo predicts FIRING and predicts nothing about SHARE.**

---

## RATIFY: Hypothesis

**Generalising `_t4_chase_ok`'s last-K-position oscillation detector from the home
defender's chase into `_nav`, and consuming the detection as a bounded MOVE ban
rather than a re-pick, raises our LOCAL pooled game share against
`bots/_v468kladturbo` itself to 51.33% or higher at n = 5,400 games across all 15
corefill maps and both seats.**

**The mechanism claim, stated so it can be wrong** — three effects, and the
hypothesis is that the first outweighs the other two:
* **IT RETURNS WASTED BUILDER-ROUNDS.** In the parent, `_move` returning True is
  `_nav`'s only notion of success, so a REVERSE counts as a successful move;
  inside a two-cycle every round "succeeds", `self.stuck` never increments, and
  the `stuck >= 5` escape hatch is unreachable from inside the very condition it
  was written for. The ban breaks the cycle at move level.
* **⚠ IT RAISES THE RE-PICK RATE** via the `stuck` feed (point 3 above). Re-picks
  are what killed the two prior arms in this family. Bounded at five trips, but
  not zero.
* **⚠ AND IT CAN COST A ROUND IN A CORRIDOR.** When the banned tile is the only
  legal step it is still taken (`eco.py:1563-1571`, the negative control written
  into the code), but the preference order is re-walked first, so a dead-end
  builder pays an extra scan and is counted stuck.

**⇒ A flat result is INFORMATIVE and is not a null about "oscillation".** It would
say the returned rounds and the extra re-picks cancel — which is a different
finding from "the two-cycle does not cost us anything".

---

## REGISTRATION BLOCK

**TARGET BAND: N/A — local corefill screen with ZERO rated ladder exposure: no submission, no activation, no unrated challenge, so `tools/target_value.py` has no input. Nothing on this page ends in a ship; the only branch that reaches the ladder is a later, separately-registered head-to-head against the holder.**
**PINNED: N/A — local self-play. The opponent version is fixed by construction: the control tree is `bots/_v468kladturbo` at the commit this shard runs from, pinned at `scratchpad/CONTROL_PIN` (`a9228ccb56ed9a65dd7d72ad1cb96068 bots/_v468kladturbo`). There is no opponent churn to pin against and no calibration relevance to protect.**
**SURFACE: local**
**CLUSTER UNIT: none** — CLAUDE.md's enumeration PERFORMED, not asserted: (i) the **MATCH** cluster does not exist on this surface — `tools/overnight.sh` writes one TSV row per `fcode run`, so 1 row = 1 game and no row shares a match with another; (ii) the **OPPONENT** cluster is degenerate — every one of the 5,400 rows plays the identical control tree, so the pooled stratum holds exactly one opponent and there is no between-opponent variation for a design effect to describe. Both clusters die ⇒ DEFF = the measured local constant **0.98** (pair-weighted, ρ = −0.020, 124 shards, s39 audit). **The platform constants (1.529 rated / 1.833 unrated) are NOT applicable here.** ⚠ **The s42 cross-host rider is registered and does not bind: this is a WITHIN-HOST local cell and nothing on this page pools across hosts.** Any later remote replication is REPORTED SEPARATELY and NEVER POOLED (GUNAXABL/SENTTHR precedent). ⛔ **AND THE SEGMENT BAR TAKES A DIFFERENT CONSTANT, enumerated separately below rather than inherited.**
**ESTIMATOR: unweighted pooled treatment game share** = (rows with `winner == T`) / (completed rows), over all 5,400 rows, both seats pooled, all 15 maps pooled, no reweighting. Interval by `tools/cluster_ci.py` (v4, at HEAD) with the local constant. Seat A and seat B shares are reported SEPARATELY as a fixture diagnostic and are never the bar — seat is worth ~6.8pp on byte-identical arms, which is why the n is a multiple of 30.
**DOSE: two-cycle reversal share of builder moves — treatment 23.2 vs flag-off control 44.5 (n=16 seat-matched demo sides, `2bf5f9e3`; both verdicts driven — with `LOKI_FREEROUND_ON=False` the arm's replay SHA-256 is identical to the base in sixteen of sixteen cells, and with the flag ON it differs in sixteen of sixteen, `scratchpad/s48_flagoff.sh`, NOISE_ON=False + `--tle 0`). ⚠ THIS IS A FIRING DEMONSTRATION AND NOT AN EFFECT SIZE — one-game cells on a fixture where a same-code BASE-vs-BASE pair on one map and seed read 18.4% oscillation on seat A against 41.3% on seat B (`scratchpad/s48_demo_battery.sh` header), i.e. the seat effect alone is larger than anything a plank is expected to move, and the ratio's own denominator moved (see point 4 above).**
**PLANNED n: 5400 games** (= 15 maps × 2 seats × 180, so map and seat balance is exact; `tools/overnight.sh:66` has run a 15-map pool since the 2026-08-13 rotation and its own comment requires multiples of 30).
**BOUNDARY: 5400 games** — LOCAL surface, one tape row is one game; there is no accept/attempt distinction on this fixture.
**CUT-SHORT: floor 2700 games.** Below 2,700 completed tape rows this leg publishes descriptive tallies (share, per-seat, per-map, kill-clock) and takes **NO comparative look and no bar verdict**; the half-width at 2,700 is ±1.87pp, already wider than the 1.33pp margin the bar is built on. An `auto_gate` cancellation at MARK-400, MARK-1000 or TREND-FLOOR@1000 is an OPERATIONAL STOP, not a verdict, and is typed `cancellation`. ⚠ **Both prior arms in this family died as cancellations at n≈1,800, so this clause is the one most likely to bind on this page.**
**BAR: 51.33**
**BASE RATE: 50.00**
**BAR SOURCE:** house-standard corefill futility band, `50 + 1.96*sqrt(.25/5400) = 51.33pp`, local DEFF 0.98 so naive — the identical bar carried by `OSCLOCK`, `OSCLOCK2`, `SEALFLOOR6`, `SENTTHR`, `KLADTK2`, `KLADTURBOR` and `KLADLADDER` in `docs/prereg/BARS.tsv`, which is what makes this arm directly comparable to the two dead siblings it is a re-shape of. **Constructed, not observed.** ⛔ **KIND OF BAR, per the OB16 corollary: this is a POINT RULE. The standard band is `50 ± half_width`, so its implied MDE is 0.000pp and clearing it excludes 50.0 and NO positive effect size.** It may not be quoted as having excluded an effect.
**BASE RATE SOURCE:** structural A/A expectation of a seat-balanced, map-balanced self-play fixture whose control tree is the treatment's own base. Empirically calibrated by `IDNULL140` — **49.27% [47.94, 50.60] at n = 5,400**, 2026-08-16T18:02:04Z, same host and fixture (`results.tsv:454`) — and by `NULL125` — **51.04% at n = 5,400** (`results.tsv:346`). Two A/A cells, one either side of 50.0, both intervals containing it.
**POOL ERA: post-2026-08-13-rotation** — the 15-map local pool of `tools/overnight.sh:66`. (`check_pool_era` treats this as n/a on a LOCAL surface per SPEC §6; declared anyway so the population is on the page.) ⚠ **AND IT IS NOT COSMETIC: the demo battery ran `yulerune icefloe drumlin eider`, and `eider` is NOT in the 15-map corefill pool.** Worse for this arm specifically, **NONE of the three lock-heavy maps that carry its primary segment (midgard, ragnarok, valkyrie) was in the demo at all.** That is precisely why F1-F3 below are re-run on the FULL pool before the primary.
**REFERENCE n: none** — the comparator is generated inside this same shard from the same 5,400 seeds; there is no fixed external reference sample, so no resolution floor at n→∞.
**TREATMENT TREE: bots/_v478freeround**
**TREATMENT DIFF REFS: 2bf5f9e3^ 2bf5f9e3**
**MECHANISM METRIC READS: bots/_v478freeround/eco.py:1488 — `if len(hist) >= FREEROUND_WINDOW and len(set(hist)) <= FREEROUND_SET_MAX:`, the trip test of `_freeround_tick`; observed as F1 via the `FR2TRIP` tag emitted at eco.py:1513, `FR2SKIP` at eco.py:1551 (logged ONLY on rounds where the ban actually changed the chosen direction, so the count is a dose and not a heartbeat) and `FR2FORCE` at eco.py:1563, all decoded by `scratchpad/s48_eco_demo.py` out of the LOCAL replay's `BotOutput.stdout` (populated locally; stripped only on platform-downloaded replays). TREATMENT DIFF TOUCHES: bots/_v478freeround/eco.py bots/_v478freeround/doctrine.py bots/_v478freeround/main.py. INTERSECTION: yes — `_freeround_tick` and the ban-aware `_nav` loop are inside the block the arm ADDS to `eco.py`; a `grep -c` for `_freeround_tick` and for `nav_osc` over every source file of the control tree returns 0, so the metric cannot read identically in both arms because the control has no detector to trip.**
⚠ **DIFF-REFS DISCLOSURE:** `2bf5f9e3` ADDS the whole tree, so `git diff 2bf5f9e3^ 2bf5f9e3 --name-only` returns FOUR paths including `raid.py`. The SEMANTIC diff against the control is THREE files: `diff -rq bots/_v468kladturbo bots/_v478freeround` names `doctrine.py`, `eco.py`, `main.py` only, and `raid.py` is byte-identical. `TREATMENT DIFF TOUCHES` declares the semantic three.
**METRIC WINDOW: r0-r1000. GATING CONSTANTS: FREEROUND_WINDOW=3, FREEROUND_SET_MAX=2, FREEROUND_COOLDOWN=4. MECHANISM CAN OCCUR IN WINDOW: yes** — **there is NO round floor in this plank.** The detector needs three CONSECUTIVE navigating rounds, so the earliest possible trip is r2; every demo game tripped inside the eco phase (`FR2TRIP` 15-110 per game). The window is the whole game because the history resets on any non-navigating round and can re-arm at any point.
⚠ **DISCLOSED, and ONE OF THESE WARNS IS REAL: `prereg_check.py` emits three `OBLIGATION 17, PARTIAL WINDOW` warns against this line.** `FREEROUND_WINDOW=3` **is genuinely a three-round warm-up** — the earliest possible trip is the third consecutive navigating round, so the checker's `rounds r0-r2 cannot contain the mechanism` is CORRECT (and negligible against a 1,000-round game). It is stated rather than argued away. The other two are checker artefacts: `FREEROUND_SET_MAX=2` is a SET SIZE (how many distinct tiles the window may hold), not a round; `FREEROUND_COOLDOWN=4` is a BAN DURATION, not a threshold a round must exceed. All three are declared because they are the constants that actually gate the plank, and an undeclared gate is the failure the obligation exists for.
**PRE-STATE: the predicted-change set is NOT already in the target state at lock.** Verified at draft against the control tree: `grep -c LOKI_FREEROUND_ON` over every control source file → **0**; same for `nav_osc` and `_freeround_tick` → **0**. The control's `_nav` falls through to (left, right, REVERSE) with no ban of any kind, and its `self.stuck` increments only when all four cardinals fail — which is the defect. ⚠ **The DETECTOR itself is NOT novel and the prereg says so: `_t4_chase_ok` in `main.py` already implements the same window mechanics in the control, for the home defender's chase. What does not exist in the control is any use of it in `_nav`, and that is the predicted change.**
**PRIMARY SEGMENT: lock-heavy maps — `midgard`, `ragnarok`, `valkyrie` — EXPECTED DIRECTION: POSITIVE (treatment share on these three maps ABOVE its own pooled share).** Mechanism reason, and it is measured rather than assumed: the `#54` builder-lock census puts our lock rate at **midgard 35.6% of builder-rounds vs 10.9% for opponents (3.3x), ragnarok 14.1%, valkyrie 12.8%**, against 3-8% on the small maps (`docs/research/BUILDER-TACTICS-ATLAS-2026-08-14.md:165`; segment vocabulary from OB15's own list). A move-legality ban can only pay where builders actually get stuck, so this is a MECHANISM-SPECIFIC segment and is preferred to a size class per OB15's rule that a proxy dilutes. **EXACTLY ONE primary segment is declared; every other split on this page is descriptive.**
**EXPECTED DIRECTION: POSITIVE** — the treatment's game share on `midgard` + `ragnarok` + `valkyrie` pooled is expected to sit ABOVE its own all-15-map pooled share. A negative or flat on-segment reading is a REFUTATION of the segment claim, not a neutral result, and it is the branch that says the lock census does not translate into recoverable rounds.
**SEGMENT VALUE CEILING: 20.0% x 8.0pp = 1.60pp pooled.** Three of the fifteen pool maps is a 20.0% pairing share on this fixture (exact by construction — the shard plays each map equally), and 8.0pp is a deliberately GENEROUS on-segment effect, larger than any single plank this project has measured on a map class. ⚠ **The consequence is registered rather than discovered: even that ceiling pools to 1.60pp against a 1.33pp bar, so the POOLED screen is a WEAK instrument for a lock-heavy-only effect, and any confirmation of this segment is ON-SEGMENT, NEVER POOLED.** Per OB15c, a pooled fail that clears the segment triggers a **NEW leg with its own n** — the rows that suggested the segment cannot also confirm it.
**SEGMENT CLUSTER UNIT — enumerated separately, because inheriting the pooled constant would be the exact error OB15's units rider names:** on a per-map cut the **MATCH** cluster is already dead here (it never existed on this surface: 1 tape row = 1 game) and the **OPPONENT** cluster is degenerate (one control tree). Both clusters die on the segment cut too ⇒ **DEFF 0.98 again, NOT the platform per-map 1.07** — the 1.07 constant describes a per-map cell holding several games against the SAME opponent from DIFFERENT matches, and neither of those structures exists on a local self-play shard. **Half-width on the 3-map segment (n = 1,080): ±2.96pp.** Stated in advance so nobody reads a 3pp segment swing as a finding.
**CELL VERSION CHURN: N/A — not a panel, no `CELLS:` line, one fixed local control tree.**
**GATE RESOLUTION: the shard is governed by the pinned `tools/auto_gate.py` marks — n≥400 CATASTROPHE if the 95% CI upper < 45.0; at each mark from n≥1000 STOP if the CI upper < the shard's bar (51.33); TREND-FLOOR@1000 if the first-1000 prefix share < 52.0 (`tools/auto_gate.py:233-250`). Those are OPERATIONAL CANCELLATIONS that free a core — typed `cancellation`, never `verdict`, licensing NO exclusion claim, because the registered target is 5,400. The RESOLVABLE gate this document owns is the pooled primary at full n, whose margin (1.33pp) exceeds its own half-width (±1.32pp) by 0.01pp — resolvable, and only just. ⛔ **THE PRIMARY SEGMENT'S OWN RESOLUTION IS STATED AND IT IS THE WEAKER HALF: at n = 1,080 on-segment rows the half-width is ±2.96pp, so the segment can only resolve an on-segment effect of about 3pp or more. An on-segment effect between 0 and 3pp is UNRESOLVABLE BY THIS LEG BY CONSTRUCTION and the pre-committed response is to say so, not to re-fire** (OB16's "an unresolvable bar is a reason to state what IS resolved, not a licence to spend games until it resolves"). Everything else on this page (F1-F3, D1-D3, seat splits) is DIAGNOSTIC and cannot rescue a failed primary. Any branch that does not resolve is UNRESOLVED, and an UNRESOLVED gate defaults to the RESTRICTION: no promotion, no ship conversation, no combination claim.**

---

## FALSIFIER

**PRIMARY FALSIFIER: at n = 5,400 the 95% CI UPPER bound on the treatment's
pooled game share falls BELOW 51.33.** That excludes the bar and says the
generalised detector does NOT add measurably to Sleipnir on this fixture.
**Consequence, registered in advance and BRANCHED:**
* **If the F-battery shows the two-cycle share DOWN and the pooled primary
  below bar, AND the primary segment ALSO fails**, then the third arm in this
  family has now failed with the third distinct consumer of the same detection
  (re-pick, re-pick, move-ban). **The road — "our builder oscillation is a
  recoverable loss" — closes on live-fixture evidence and no fourth consumer is
  queued without a new mechanism, not a new consequence.**
* **If the pooled primary fails but the primary segment CLEARS with its interval
  excluding the pooled share**, the pre-committed response is OB15c: a **NEW,
  separately-registered on-segment leg with its own n**, and a `MAP_CODES`-style
  conditional ship only if that holds. **The rows that suggested it may not
  confirm it.**

**MECHANISM FALSIFIER (independent of the primary, and it can fire first):** if F1
shows the treatment's `FR2SKIP` count — the rounds on which the ban actually
CHANGED the chosen direction — is within noise of zero on the 15-map pool, then
the plank did not deliver its dose in the screen fixture and **the primary is
uninterpretable in either direction**: a flat share would mean "the mechanism
never fired", not "it fired and did not pay". Per FIRINGS-BEFORE-PRIMARY this is
read BEFORE the primary is typed; if it fires, the primary is reported as **NOT
MEASURED**, not as a null.

---

## READING, PRE-COMMITTED — four bands, written before the data

Registered now so no band is chosen after the fact. The four-band form is the
`KLADLADDER` precedent.

| band at n = 5,400 | pre-committed reading |
|---|---|
| **CI lower ≥ 51.33** | **THE FREE ROUND IS REAL.** Resolved on this fixture, and it is the first positive in a family with two dead arms — report it with that context and with the `stuck`-feed caveat, since a win here is NOT attributable to navigation alone. Promotes to a combination input and to a separately-registered head-to-head against the live holder. |
| **point ≥ 51.33 but CI lower < 51.33** | **REAL-BUT-SMALL, COMBINATION INPUT ONLY.** Registered in advance as WEAK: `NULL125`'s byte-identical A/A read 51.04, so a bare clearance in [51.33, 52.4] is not distinguishable from fixture noise by this leg alone. Rows KEPT, arm available for combination; NO ship conversation, and a replication on fresh seeds is the price of promoting it. |
| **CI includes 50.0** | **ADDS NOTHING MEASURABLE POOLED.** Read the primary segment next, and only the primary segment. Absent a segment clear, the returned rounds and the extra re-picks cancel, or neither binds — combination input only if another arm supplies a mechanism reason. |
| **CI upper < 51.33** | Primary falsifier fires — see the two branches above. |

⚠ **50.0 IS NOT A FLOOR AND A NEGATIVE IS A LIVE, PRE-NAMED OUTCOME.** The
`stuck` feed raising the re-pick rate is a plausible route to a share materially
BELOW 50 — it is the same lever that produced 48.53 and 46.49 — and
`KLADLADDER` has just shown this fixture returning 41.86 on a demo-clean arm.
**Named here so a negative is not explained away as noise.**

---

## MECHANISM DIAGNOSTICS TO READ AT READOUT

**Measurability is declared per metric. `NOT MEASURABLE` is written where it is
true, rather than a metric being quietly renamed into something the tape carries.**

### F1-F3 — the FIRINGS read. MEASURABLE, but NOT off the shard tape.

**EXECUTING TOOL, named per Obligation 17: `zsh scratchpad/s48_demo_battery.sh
_v478freeround antler archipelago auroraveil drakkarfjord drumlin fjordgate
frostgate glacierkeep icefloe midgard nordkap ragnarok royale valkyrie yulerune`,
decoded by `scratchpad/s48_eco_demo.py`.**
**OB17 checks, run, and the clause that could have surprised is named:**
1. *Name the executing tool* — done above.
2. *Confirm the RUNNER emits what is registered* — `s48_demo_battery.sh:16` is
   `if (( $# )); then MAPS=($@); else MAPS=(yulerune icefloe drumlin eider); fi`,
   so the pool override is a path the script has; and `s48_eco_demo.py:50-53`
   passes `--replay <path>` and **`--tle 10`**, matching the shard's own
   `--tle 10`. ⭐ **THIS IS THE CLAUSE THAT COULD HAVE GONE THE OTHER WAY AND IT
   WAS RUN FIRST, and it matters MORE for this arm than for its siblings: the
   ban re-walks the preference order and can call `_move` up to four extra times
   per round, so a firings battery run WITHOUT the CPU limit would measure a
   chassis the screen does not use.** It passes.
3. *Consequence of silent non-execution* — omitting the map list silently falls
   back to the four-map default, **which contains none of the three lock-heavy
   maps this arm's primary segment is defined on**, and nothing in the output
   would say so. ⇒ **the readout must print the map list it actually ran.**

**Registered size: 60 treatment sides + 60 control sides** (15 maps × 2 seeds ×
both seats, with a base-vs-base control run on the same map and seed — the
battery's own design, because base-vs-base seat variance was measured larger
than anything a plank is expected to move). Run BEFORE the primary is typed.

* **F1 — DOSE DELIVERY ON THE POOL THE SCREEN PLAYS.** `FR2TRIP`, `FR2SKIP` and
  `FR2FORCE` per side, per map. **Pre-registered expectation: `FR2SKIP` > 0 on a
  majority of the 15 pool maps, and HIGHEST on the three lock-heavy maps.** Demo
  anchor, reported as an anecdote and NOT as an expected effect: `FR2TRIP`
  15-110/game, `FR2SKIP` up to 160, `FR2FORCE` 0-42 over 16 sides on four maps,
  one of which is off-pool.
* **F2 — THE PAIR: two-cycle SHARE and total MOVES, reported together, never
  apart.** Per side: two-cycle reversals, total builder moves, and the ratio —
  because the demo's denominator moved 23% (point 4 above) and the share alone
  is unreadable. **Pre-registered expectation: absolute reversals DOWN by more
  than the move count is down.**
* **F3 — THE COST SIDE: `FR2FORCE` rate and the re-pick rate.** `FR2FORCE` counts
  corridor/dead-end rounds where the ban was overridden, and the `stuck` feed's
  downstream effect is the re-pick rate. **DESCRIPTIVE, and it is the diagnostic
  that tells a negative apart from the two dead arms' failure mode: a negative
  with a HIGH re-pick rate is the OSCLOCK mechanism reappearing through the back
  door**, which would be a finding worth banking even though the primary failed.

### D1-D3 — the kill-clock read. MEASURABLE, shard-native (`cond`, `turns`, `winner`).

* **D1 — TIMELY-KILL RATE (the `DEFENCE_ADMISSION_BAR` primary), ITT.** Share of
  ALL treatment-seat games ending `cond == core_destroyed` in our favour with
  `turns ≤ 300`, treatment vs control, both on the same 5,400 rows.
  **Non-regression is the bar and it is stated as an EXCLUSION, per CLAUDE.md's
  fail-to-exclude clause: the 95% CI on the difference must EXCLUDE a fall of
  more than 2.0pp.** A "no significant rise" phrasing is not admissible.
* **D2 — MEDIAN KILL ROUND**, treatment vs control, as the gross backstop (a
  median crossing 300 is disqualifying), reported alongside the r1000 share since
  `R1000_IS_DEFEAT` makes an r1000 game a cost even when its tiebreak is won.
* **D3 — RMST300, ITT** — mean of `min(turns, 300)` with every game not ending in
  OUR core kill scoring the full 300 (`tools/fieldcal_read.py:239`, the registered
  estimator; the loose definition is a sensitivity column only), with its interval
  from `tools/cluster_ci.py`. **ITT over ALL rows** — the kill-conditioned form
  carries a collider, per `PROGRAMME.md`.

### NOT MEASURABLE on this leg — named, not silently dropped.
* **Whether a ban BROKE a specific two-cycle or merely displaced it.** `FR2SKIP`
  says the ban changed a direction; nothing decoded here follows the builder to
  say whether it then reached its target sooner. **The connect rate (F2 on the
  ECOMMIT battery's definition) is available as a crude proxy and the demo read
  74.1% vs 72.2% — flat, and quoted only as a SAFETY check that the eco stands
  up, never as this arm's effect.**
* **Per-unit CPU.** Local replays zero-fill `execTimeUs` (the s42 D33 instance),
  so **no CPU claim is available from this leg**; the demo's "0 TLEs in 16 games"
  is an anecdote. ⚠ **Disclosed: `LOKI_FREEROUND_LOG = True` in the fired tree
  adds three `print()` sites the control does not have. The base already ships
  `LOKI_L4_LOG` and `LOKI_SAMESTOP_LOG` at True, so this is in-house precedent
  and the cost is small — but it is an unmatched per-turn cost in the
  TREATMENT'S direction under `--tle 10`, and it is named here rather than
  discovered later.**
* **Seed determinism.** `NOISE_ON` pins an unseeded per-unit salt, so base-vs-base
  at one seed diverges at round 0. **No seed-matched or replay-diff equivalence
  claim is available on the SHARD fixture**; the flag-off equivalence claim rests
  on the separate `--tle 0` + `NOISE_ON=False` harness (`scratchpad/s48_flagoff.sh`)
  and on the code, never on shard rows.
* **Separating the BAN from the `stuck` FEED.** They ship under one flag
  (`LOKI_FREEROUND_ON`) and are **NOT SEPARABLE** by this leg. Given point 3, that
  is the single most consequential thing this leg cannot do, and separating them
  needs a further arm. **No readout sentence may attribute the result to the ban
  alone.**

---

## THE CHANGE — `file:line`, control → treatment

**TREATMENT TREE: `bots/_v478freeround`** — byte-for-byte `bots/_v468kladturbo`
apart from three files. Verified at draft: `diff -rq` names exactly
`doctrine.py`, `eco.py` and `main.py`; **`raid.py` is byte-identical**, so the
hand-merged TURBO × BODYAWARE raid path is untouched.

1. **`doctrine.py` +1878-1967** — one comment block and five constants:
   `LOKI_FREEROUND_ON = True`, `FREEROUND_WINDOW = 3`, `FREEROUND_SET_MAX = 2`,
   `FREEROUND_COOLDOWN = 4`, `LOKI_FREEROUND_LOG = True`.
2. **`main.py` +155-167** — four per-unit fields mirroring the `t4_chase` trio
   directly above them: `nav_osc_pos`, `nav_osc_since`, `nav_osc_until`, plus the
   one addition `nav_osc_ban`. No store slot.
3. **`eco.py:1475-1518`** — `_freeround_tick`: the lifted window mechanics
   (contiguity reset at :1481, the trip test at **:1488**, the ban excluding the
   tile currently occupied at :1493, the cooldown at :1494) and the `stuck` feed
   at **:1512**.
4. **`eco.py:1521-1571`** — `_nav` gains the ban: the parent's candidate order
   (BFS step, left, right, reverse) is unchanged; a step onto a banned tile is
   HELD on the first pass, and taken on the second pass only if nothing else was
   legal, with `self.stuck += 1` at **:1566**. **With the plank off, `ban` is the
   empty tuple, the membership test can never match, and the loop performs
   exactly the parent's sequence of `_move` calls** — which is what the flag-off
   SHA equivalence measures.

---

## WHAT THIS LEG COSTS AND WHAT IT DOES NOT

**Cost: one local core to n = 5,400, plus ~90 local games for the F-battery.**
ZERO rated ladder exposure, zero submissions, zero unrated challenges — nothing
on this page touches the platform, which is why `TARGET BAND` is N/A.

**It does NOT decide a ship.** The strongest branch promotes the arm to (a) a
combination input and (b) a separately-registered head-to-head against the live
holder — the pipeline step Magnus's procedure names verbatim (*"we start by
testing it against the current slot, If it beats it we can switch"*), for which
`SLEIPH2H` is the template. **Gate-1-to-gate-2 transitivity is UNVALIDATED in
this repo (QUEUE #65: 3 concordant, 1 not), so the head-to-head is not skippable
on the strength of this number.**

---

**PROVENANCE:** `docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md` (read in full: obligations 7, 12, 13, 14, 15a-c and its units rider, 16 + its corollary and cross-host rider, 17 + its rider) · `docs/research/SPEC-prereg-check-2026-08-14.md` · `docs/research/SPEC-prereg-check-side-lane-checks-2026-08-14.md` · `docs/research/SPEC-metric-window-2026-08-15.md` · `docs/research/RULING-prereg-check-vocabulary-2026-08-14.md` · `docs/research/ECO-STUDY-fast-connected-harvesters-2026-08-17.md` (§0, §7 M2, and BOTH amendments — the v155 slope is RETRACTED as a measured quantity and is not quoted anywhere on this page) · `docs/research/CLOSURES-s43-2026-08-15.md:40` (OSCLOCK 48.53 @1867, OSCLOCK2 46.49 @1809) · `docs/research/BUILDER-TACTICS-ATLAS-2026-08-14.md:165` (the lock census and the "successor must change NAVIGATION" ruling) · `docs/prereg/PREREG-KLADLADDER-2026-08-17.md` (house template and the four-band reading precedent) · `docs/prereg/PREREG-SEALSENTAN-2026-08-17.md` (same-day house style; its second-clock finding is engaged with above) · `docs/prereg/BARS.tsv` (header, the FIRINGS-BEFORE-PRIMARY rule, the OSCLOCK/OSCLOCK2 rows) · `CLAUDE.md` · `tools/prereg_check.py` (read for `RULES`, `check_arithmetic`, `check_metric_window`, `check_pool_era`, `deff_for`) · `tools/auto_gate.py:224-250` · `tools/overnight.sh` (the 15-map pool at :66, the `# FIXTURE start=` stamp at :99-104, `--tle 10` and `--replay /dev/null` at :138-139) · `tools/cluster_ci.py` (v4) · `tools/fieldcal_read.py:230-256` · `scratchpad/s48_flagoff.sh` · `scratchpad/s48_demo_battery.sh` · `scratchpad/s48_eco_demo.py` · `bots/_v478freeround/{doctrine,eco,main,raid}.py` · `bots/_v468kladturbo/{doctrine,eco,main,raid}.py` · `scratchpad/corefill_work.txt` · `scratchpad/CONTROL_PIN` · `results.tsv` (rows 346 `null125-final`, 454 `idnull140-cert-5400`, and the three 2026-08-17 `kladladder-*` rows) · git commit `2bf5f9e3` and `git diff --name-only 2bf5f9e3^ 2bf5f9e3` · the drafting brief supplied by the builder lane s48 and the research lane's pre-lock steering note. No file under `bots/`, `tools/`, `scratchpad/`, `docs/prereg/BARS.tsv`, `results.tsv`, `HANDOVER.md`, `PROGRAMME.md` or `QUEUE.md` was created or modified by this agent, and no game was run.
