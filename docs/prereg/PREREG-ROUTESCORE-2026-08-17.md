# SCREEN PREREG — `ROUTESCORE`: pick ore by the route home, not by the crow

Drafted by a fresh opus subagent with no inherited session context beyond the
inputs listed under `PROVENANCE`. The builder lane ratifies the judgment lines
and types the lock commit; this agent wrote no code under `bots/`, appended no
worklist row, appended no `BARS.tsv` row, fired no game, started no shard, and
touched neither `results.tsv` nor `HANDOVER.md` nor `PROGRAMME.md` nor
`QUEUE.md`.

**STATUS: committed BEFORE the `ROUTESCORE` row is appended to
`scratchpad/corefill_work.txt`, BEFORE any file named
`scratchpad/overnight/ROUTESCORE.*` exists, and BEFORE the leg's first game.**
Drafting session wall clock at write time **`2026-08-17T05:36:44Z`** (`date -u`,
same shell call); repo HEAD at draft `7bcf0e5e` (author time
`2026-08-17T07:35:55+02:00`). Verified at draft:
`grep -c 'ROUTESCORE' scratchpad/corefill_work.txt` → **0**; same grep on
`docs/prereg/BARS.tsv` → **0**; `ls scratchpad/overnight/ | grep -i routescore`
→ **empty**; `grep -cE '8(16|18|20)000' scratchpad/corefill_work.txt` → **0**
(the seed base is free).

### SECOND CLOCK — registered in the CONSERVATIVE form

**REGISTERED SECOND CLOCK: the `ts` of the FIRST COMPLETED ROW of
`scratchpad/overnight/ROUTESCORE.tsv`.** Conservative by construction: the
shard's true start is strictly earlier than its first completed row, so the
reported lock-to-fixture gap can only be UNDERSTATED. ⚠ **The brief's stated
reason for avoiding the tighter clock did NOT survive my check and is corrected
rather than repeated:** `tools/overnight.sh:99-104` computes
`START=$(date -u …)` and writes `# FIXTURE\t…\tstart=$START` as the tape's FIRST
LINE before the first `fcode run`; the heartbeat is a SEPARATE file and
overwrites nothing on the tape. ⇒ **that stamp WILL exist on this local shard and
is registered as a CORROBORATING clock, not the primary.** If the tape instead
carries `# FIXTURE-RESUME … start=UNKNOWN-legacy-tape` or no `# FIXTURE` line,
the registered first-completed-row clock stands alone and nothing changes.

⚠ **The treatment tree ALREADY EXISTS and is committed** (`bots/_v479routescore`,
added `e97a804b`, author time `2026-08-17T07:30:13+02:00`). This document is
therefore **NOT** locked before the arm exists, only before the arm's first screen
row. It is also what makes Obligation 13's intersection **computable at lock
time**.

---

## ⛔ READ BEFORE RATIFYING — SIX THINGS THE LANE OWNS

**1. THE CONTROL IS THE LIVE INCUMBENT, SO 50.0 MEANS "ADDS NOTHING".**
`bots/_v468kladturbo` is Sleipnir v1, pinned at `scratchpad/CONTROL_PIN`
(`a9228ccb56ed9a65dd7d72ad1cb96068 bots/_v468kladturbo`) per Magnus's benchmark
ruling. **A reader carrying a 61-shaped intuition from the KLADTURBO-vs-v140 read
onto this page has misread the fixture: the same bot measured against itself
reads 50.**

**2. ⛔⛔ THE HONEST NULL, CARRIED VERBATIM FROM THE BUILD, BECAUSE IT IS THE
OPEN MECHANISM QUESTION AND NOT A FOOTNOTE.** From `e97a804b`'s own commit
message: *"⚠ HONEST NULL ON M3's OWN NAMED DEMO: median BFS route length at build
for harvesters #3-#6 is 9 (arm) vs 8 (control) on seat A and 7 vs 8 on seat B —
mixed, no clean drop at this n. Reported, not explained away."* n = 20 sides.
**The study's named demo for this plank was a DROP in route length at build, and
it did not appear.** ⇒ **The plank is demonstrated to move the PICK (220 picks
differ from the parent's cursor tile) and is NOT demonstrated to move the ROUTE
LENGTH, which is the priced quantity.** This is registered here as **THE OPEN
MECHANISM QUESTION OF THIS LEG**, and the readings for both directions are
pre-committed below.

**3. ⛔ MORE THAN HALF THE DEMONSTRATED DOSE WAS DELIVERED ON MAPS THE SCREEN
NEVER PLAYS.** The 220 differing picks split `eider 93, icefloe 88, saga 30,
drumlin 9, yulerune 0`. **`eider` and `saga` are NOT in the 15-map corefill pool**
(`tools/overnight.sh:66`), so **123 of 220 picks (55.9%) are off-pool** and only
97 are on maps the screen plays — of which one pool map in the demo (`yulerune`)
fired **zero** times. **The dose that gates this screen is therefore MOSTLY
EVIDENCE ABOUT GEOMETRY THE SHARD WILL NOT SEE.** This is the single strongest
reason the FIRINGS battery below is re-run on the full pool BEFORE the primary,
and it is why the mechanism falsifier is written as a live possibility rather
than a formality.

**4. THE SHARD TAPE CANNOT SEE THE MECHANISM, SO A FIRINGS READ IS MANDATORY
BEFORE THE PRIMARY.** `tools/overnight.sh:138-139` runs every game with
`--replay /dev/null`; the tape's columns are
`ts shard game map seed seat winner cond turns` — **no build, position or stdout
information exists on it, in either arm.** The mechanism is CONDITIONAL (it only
changes an answer when a seat's stripe holds a route/Manhattan disagreement), so
`docs/prereg/BARS.tsv`'s FIRINGS-BEFORE-PRIMARY rule (adopted
2026-08-16T13:27:33Z) binds: **F1-F3 run on a SEPARATE battery that keeps
replays and are read BEFORE the primary sentence is typed.** What the tape CAN
answer is the kill-clock question (`cond`, `turns`, `winner`), which is why D1-D3
are shard-native and F1-F3 are not.

**5. CONNECT RATE IS A MECHANISM METRIC AND MUST NEVER BE QUOTED AS THIS ARM'S
RESULT.** The demo's 74.6% (100/134) vs 68.6% (109/159) is a dose reading on 20
seat-matched sides. **Research's pre-lock check measures connect rate strongly
outcome-associated (within-map slope +0.56 [0.46, 0.66] clustered on match;
paired within-game 0.667 [0.62, 0.71]) WITH THE CAUSAL ARROW CONTAMINATED BY
REVERSE CAUSATION** — a losing side gets its belt cut (2.58x belt-death
asymmetry; 50.9% of conveyor deaths near live enemy gunners). In a randomised
two-arm shard the WIN SHARE is clean; a connect-rate bar would measure a quantity
the result partly produces. **And it is reported only as a PAIR with the
harvester COUNT** (134 vs 159 lifetime, 100 vs 109 connected here) — the rate can
rise mechanically when fewer harvesters are built, so neither number is readable
alone.

**6. THIS FIXTURE PRODUCES LARGE NEGATIVES AND HAS JUST DONE SO.** `KLADLADDER`,
demo-clean on this same base with this same flag-off SHA method and its dose
confirmed delivered, finished **41.86% [40.20, 43.52] at n = 3,404**
(`results.tsv`, `kladladder-n-final-correction`, 2026-08-17T05:18:10Z). **A clean
demo predicts FIRING and predicts nothing about SHARE.**

---

## RATIFY: Hypothesis

**Returning, from among the first four members of this seat's own unchanged ore
stripe, the tile whose `_link_path` route home is shortest — instead of the first
one the cursor reaches — raises our LOCAL pooled game share against
`bots/_v468kladturbo` itself to 51.33% or higher at n = 5,400 games across all 15
corefill maps and both seats.**

**The mechanism claim, stated so it can be wrong** — a two-step chain, and the
SECOND step is the one the demo did not demonstrate:
* **STEP 1 (DEMONSTRATED): the PICK moves.** `_pick`'s only geometry term is
  `abs(t.x - core.x) + abs(t.y - core.y)` — Manhattan distance to our core — and
  the belt the builder must then BUILD is never scored. Where a wall separates
  the core from a near deposit the two numbers disagree, and the parent always
  takes the crow's answer. 220 demo picks differ.
* **STEP 2 (NOT DEMONSTRATED, AND THIS IS THE HYPOTHESIS'S WEAK JOINT): the
  ROUTE gets shorter, and therefore the belt gets cheaper and the connect gets
  earlier.** Connect latency is ~2.00 rounds per route tile and degrades worse
  than linearly past L ≈ 8. **The demo's own route-length read was mixed
  (9 vs 8 seat A, 7 vs 8 seat B, n = 20).** A moved pick that does not shorten
  the route buys nothing this study prices.
* **⚠ AND THE PARTITION IS THE SAFETY TERM.** `_pick`'s Manhattan sort and its
  `ordered[worker::workers]` stripe are computed exactly as in the parent; the
  study's own warning is that a route-length score pulls all seats toward the
  same near cluster, and **keeping the stripe is what prevents that. It is
  load-bearing, not inherited** — if the seat-collision rate rises in the
  F-battery, that is a defect, not a nuance.

**⇒ A flat result is INFORMATIVE and is not a null about "route length".** It
would most likely say the pick moved and the route did not — a statement about
this IMPLEMENTATION, not about the study's §M3 measurement.

---

## REGISTRATION BLOCK

**TARGET BAND: N/A — local corefill screen with ZERO rated ladder exposure: no submission, no activation, no unrated challenge, so `tools/target_value.py` has no input. Nothing on this page ends in a ship; the only branch that reaches the ladder is a later, separately-registered head-to-head against the holder.**
**PINNED: N/A — local self-play. The opponent version is fixed by construction: the control tree is `bots/_v468kladturbo` at the commit this shard runs from, pinned at `scratchpad/CONTROL_PIN` (`a9228ccb56ed9a65dd7d72ad1cb96068 bots/_v468kladturbo`). There is no opponent churn to pin against and no calibration relevance to protect.**
**SURFACE: local**
**CLUSTER UNIT: none** — CLAUDE.md's enumeration PERFORMED, not asserted: (i) the **MATCH** cluster does not exist on this surface — `tools/overnight.sh` writes one TSV row per `fcode run`, so 1 row = 1 game and no row shares a match with another; (ii) the **OPPONENT** cluster is degenerate — every one of the 5,400 rows plays the identical control tree, so the pooled stratum holds exactly one opponent and there is no between-opponent variation for a design effect to describe. Both clusters die ⇒ DEFF = the measured local constant **0.98** (pair-weighted, ρ = −0.020, 124 shards, s39 audit). **The platform constants (1.529 rated / 1.833 unrated) are NOT applicable here.** ⚠ **The s42 cross-host rider is registered and does not bind: this is a WITHIN-HOST local cell and nothing on this page pools across hosts.** Any later remote replication is REPORTED SEPARATELY and NEVER POOLED (GUNAXABL/SENTTHR precedent). ⛔ **The SEGMENT bar's clusters are enumerated separately below rather than inherited.**
**ESTIMATOR: unweighted pooled treatment game share** = (rows with `winner == T`) / (completed rows), over all 5,400 rows, both seats pooled, all 15 maps pooled, no reweighting. Interval by `tools/cluster_ci.py` (v4, at HEAD) with the local constant. Seat A and seat B shares are reported SEPARATELY as a fixture diagnostic and are never the bar — seat is worth ~6.8pp on byte-identical arms, which is why the n is a multiple of 30.
**DOSE: ore picks where the shortest-route candidate is NOT the parent's cursor tile, per side — treatment 11.0 vs flag-off control 0.0 (n=20 seat-matched demo sides, `e97a804b`; both verdicts driven — with `LOKI_ROUTESCORE_ON=False` the candidate list is capped at one and the loop is the parent's exactly, and the arm's replay SHA-256 is identical to the base in sixteen of sixteen flag-off cells while differing in sixteen of sixteen flag-on cells, `scratchpad/s48_flagoff.sh`, NOISE_ON=False + `--tle 0`). ⚠ THIS IS A FIRING DEMONSTRATION AND NOT AN EFFECT SIZE — one-game cells on a fixture whose same-code seat swing was measured at 5.6%→73.7% — AND 55.9% of those picks were on off-pool maps (see point 3).**
**PLANNED n: 5400 games** (= 15 maps × 2 seats × 180, so map and seat balance is exact; `tools/overnight.sh:66` has run a 15-map pool since the 2026-08-13 rotation and its own comment requires multiples of 30).
**BOUNDARY: 5400 games** — LOCAL surface, one tape row is one game; there is no accept/attempt distinction on this fixture.
**CUT-SHORT: floor 2700 games.** Below 2,700 completed tape rows this leg publishes descriptive tallies (share, per-seat, per-map, kill-clock) and takes **NO comparative look and no bar verdict**; the half-width at 2,700 is ±1.87pp, already wider than the 1.33pp margin the bar is built on. An `auto_gate` cancellation at MARK-400, MARK-1000 or TREND-FLOOR@1000 is an OPERATIONAL STOP, not a verdict, and is typed `cancellation`.
**BAR: 51.33**
**BASE RATE: 50.00**
**BAR SOURCE:** house-standard corefill futility band, `50 + 1.96*sqrt(.25/5400) = 51.33pp`, local DEFF 0.98 so naive — the identical bar carried by `docs/prereg/BARS.tsv` rows `SEALFLOOR6`, `SENTTHR`, `KLADTKILL`, `KLADTK2`, `KLADTURBOR`, `DRAINTURBO` and `KLADLADDER`, which is what keeps this arm numerically comparable to its s48 siblings. **Constructed, not observed.** ⛔ **KIND OF BAR, per the OB16 corollary: this is a POINT RULE. The standard band is `50 ± half_width`, so its implied MDE is 0.000pp and clearing it excludes 50.0 and NO positive effect size.** It may not be quoted as having excluded an effect. Given point 2, that is the right instrument here: the question is *does moving the pick move anything at all*.
**BASE RATE SOURCE:** structural A/A expectation of a seat-balanced, map-balanced self-play fixture whose control tree is the treatment's own base. Empirically calibrated by `IDNULL140` — **49.27% [47.94, 50.60] at n = 5,400**, 2026-08-16T18:02:04Z, same host and fixture (`results.tsv:454`) — and by `NULL125` — **51.04% at n = 5,400** (`results.tsv:346`). Two A/A cells, one either side of 50.0, both intervals containing it.
**POOL ERA: post-2026-08-13-rotation** — the 15-map local pool of `tools/overnight.sh:66`. (`check_pool_era` treats this as n/a on a LOCAL surface per SPEC §6; declared anyway so the population is on the page.) ⚠ **AND ON THIS ARM IT IS THE LOAD-BEARING DISCLOSURE, NOT A FORMALITY: two of the five demo maps (`eider`, `saga`) are OUTSIDE the pool and carried 55.9% of the demonstrated dose.** See point 3.
**REFERENCE n: none** — the comparator is generated inside this same shard from the same 5,400 seeds; there is no fixed external reference sample, so no resolution floor at n→∞.
**TREATMENT TREE: bots/_v479routescore**
**TREATMENT DIFF REFS: e97a804b^ e97a804b**
**MECHANISM METRIC READS: bots/_v479routescore/eco.py:1242 — `if l < best_l:`, the single line on which a candidate displaces the parent's cursor tile; observed as F1 via the `RS3PICK` tag emitted at eco.py:1244 (logged ONLY when the winner differs from `cands[0]`, so the count is a dose and not a heartbeat), decoded by `scratchpad/s48_eco_demo.py` out of the LOCAL replay's `BotOutput.stdout`, and as F2 by `scratchpad/s48_routelen.py`, which recomputes BFS route length at build off the REPLAY with code neither bot runs. TREATMENT DIFF TOUCHES: bots/_v479routescore/eco.py bots/_v479routescore/doctrine.py bots/_v479routescore/main.py. INTERSECTION: yes — `_routescore_len`, the candidate loop and the `n_cand` insertion in `_pick` are inside the block the arm ADDS to `eco.py`; a `grep -c` for `_routescore_len` and for `rs_len_cache` over every source file of the control tree returns 0. The metric cannot read identically in both arms because the control collects no candidate list at all — it returns the first tile.**
⚠ **DIFF-REFS DISCLOSURE:** `e97a804b` ADDS the whole tree, so `git diff e97a804b^ e97a804b --name-only` returns FOUR paths including `raid.py`. The SEMANTIC diff against the control is THREE files: `diff -rq bots/_v468kladturbo bots/_v479routescore` names `doctrine.py`, `eco.py`, `main.py` only, and `raid.py` is byte-identical. `TREATMENT DIFF TOUCHES` declares the semantic three.
**METRIC WINDOW: r0-r1000. GATING CONSTANTS: ROUTESCORE_CANDIDATES=4, ROUTESCORE_TTL_RNDS=25, ROUTESCORE_FAR_TILES=12. MECHANISM CAN OCCUR IN WINDOW: yes** — **there is NO round floor in this plank.** `_pick` is called the first time a builder has no target, which is in the opening rounds of every game, and the very first harvester of the game can be re-picked by it. The window is the whole game because `_pick` is called again on arrival and on stuck, at any round.
⚠ **DISCLOSED, because a green tool run with warnings under it is how a warning stops being read: `prereg_check.py` emits three `OBLIGATION 17, PARTIAL WINDOW` warns against this line and ALL THREE ARE ARTEFACTS OF THE CHECKER.** `check_metric_window` reads every declared integer as a ROUND. `ROUTESCORE_CANDIDATES=4` is a LIST LENGTH, `ROUTESCORE_FAR_TILES=12` is a TILE budget (the saturation point past the corpus knee, above which all routes score alike), and `ROUTESCORE_TTL_RNDS=25` is a CACHE LIFETIME, not a threshold a round must exceed. They are declared anyway because they are the constants that actually gate the plank, and an undeclared gate is the failure the obligation exists for.
**PRE-STATE: the predicted-change set is NOT already in the target state at lock.** Verified at draft against the control tree: `grep -c LOKI_ROUTESCORE_ON` over every control source file → **0**; same for `rs_len_cache` and `_routescore_len` → **0**. The control's `_pick` returns the FIRST unclaimed tile its cursor reaches in this seat's stripe and scores route length nowhere; `_link_path` exists in the control but is used only by SAMESTOP and the trunk planner, never to CHOOSE a deposit. The behaviour this leg predicts to change therefore cannot already be in the target state.
**PRIMARY SEGMENT: route-discordant maps — the five pool maps with the HIGHEST `RS3PICK` rate per side in the F-battery — EXPECTED DIRECTION declared on its own line below.** Mechanism reason: the plank can only change an answer where the BFS route home and the Manhattan distance DISAGREE inside one seat's stripe, which is a terrain property (walls between the core and a near deposit), and the demo measured a 93-to-0 spread across five maps. This is a MECHANISM-SPECIFIC segment and is preferred to a size class per OB15's rule that a proxy dilutes. ⛔ **THE SEGMENT IS DEFINED BY A DOSE MEASUREMENT TAKEN BEFORE, AND BLIND TO, THE SHARD OUTCOME — never by the outcome itself.** The F-battery runs and its per-map `RS3PICK` table is written down and committed BEFORE the primary is read; the five-map set is fixed at that moment and may not be revised afterwards. **A set chosen after the shard share is visible is subgroup fishing and is refused in advance here.** ⚠ **The demo cannot pre-name the set** because 55.9% of its dose was off-pool and one of its three in-pool maps fired zero times, which is exactly why the definition is operational rather than a map list. **EXACTLY ONE primary segment is declared; every other split on this page is descriptive.**
**EXPECTED DIRECTION: POSITIVE** — the treatment's game share on the five highest-dose pool maps is expected to sit ABOVE its own all-15-map pooled share. A flat or negative on-segment reading REFUTES the segment claim; it is not a neutral result, and it would say that where the plank fires most it pays least.
**SEGMENT VALUE CEILING: 33.3% x 6.0pp = 2.00pp pooled.** Five of the fifteen pool maps is a 33.3% pairing share on this fixture (exact by construction — the shard plays each map equally), and 6.0pp is a deliberately generous on-segment effect. ⚠ **Even that ceiling pools to 2.00pp against a 1.33pp bar, i.e. the pooled screen is only a MARGINAL instrument for a conditional plank of this shape** — a realistic +2pp on-segment effect pools to +0.67pp and reads as ZERO. **Any confirmation of this segment is ON-SEGMENT, NEVER POOLED**, and per OB15c a pooled fail that clears the segment triggers a **NEW leg with its own n**: the rows that suggested the segment cannot also confirm it.
**SEGMENT CLUSTER UNIT — enumerated separately, because inheriting a constant would be the exact error OB15's units rider names:** on a per-map cut the **MATCH** cluster is already dead here (it never existed on this surface: 1 tape row = 1 game) and the **OPPONENT** cluster is degenerate (one control tree). Both clusters die on the segment cut too ⇒ **DEFF 0.98 again, NOT the platform per-map 1.07** — the 1.07 constant describes a per-map cell holding several games against the SAME opponent from DIFFERENT matches, and neither structure exists on a local self-play shard. **Half-width on the 5-map segment (n = 1,800): ±2.29pp.** Stated in advance so nobody reads a 2pp segment swing as a finding.
**CELL VERSION CHURN: N/A — not a panel, no `CELLS:` line, one fixed local control tree.**
**GATE RESOLUTION: the shard is governed by the pinned `tools/auto_gate.py` marks — n≥400 CATASTROPHE if the 95% CI upper < 45.0; at each mark from n≥1000 STOP if the CI upper < the shard's bar (51.33); TREND-FLOOR@1000 if the first-1000 prefix share < 52.0 (`tools/auto_gate.py:233-250`). Those are OPERATIONAL CANCELLATIONS that free a core — typed `cancellation`, never `verdict`, licensing NO exclusion claim, because the registered target is 5,400. The RESOLVABLE gate this document owns is the pooled primary at full n, whose margin (1.33pp) exceeds its own half-width (±1.32pp) by 0.01pp — resolvable, and only just. ⛔ **THE PRIMARY SEGMENT'S OWN RESOLUTION IS STATED AND IT IS THE WEAKER HALF: at n = 1,800 on-segment rows the half-width is ±2.29pp, so an on-segment effect between 0 and ~2.3pp is UNRESOLVABLE BY THIS LEG BY CONSTRUCTION — and the SEGMENT VALUE CEILING above shows that a realistic on-segment effect lives inside exactly that band. The pre-committed response is to SAY SO, not to re-fire** (OB16: "an unresolvable bar is a reason to state what IS resolved, not a licence to spend games until it resolves"). ⛔ **AND F2 — the route-length read — IS A GATE WITH ITS OWN RESOLUTION PROBLEM: the demo answered it with median integers 9-vs-8 and 7-vs-8 on n = 20 sides, i.e. a one-tile difference with no interval. The F-battery raises it to 60 sides per arm and its readout must carry a `tools/cluster_ci.py` interval on the DIFFERENCE, not two medians side by side.** Everything else on this page (F1, F3, D1-D3, seat splits) is DIAGNOSTIC and cannot rescue a failed primary. Any branch that does not resolve is UNRESOLVED, and an UNRESOLVED gate defaults to the RESTRICTION: no promotion, no ship conversation, no combination claim.**

---

## FALSIFIER

**PRIMARY FALSIFIER: at n = 5,400 the 95% CI UPPER bound on the treatment's
pooled game share falls BELOW 51.33.** That excludes the bar and says
route-length scoring of the pick does NOT add measurably to Sleipnir on this
fixture.

**MECHANISM FALSIFIER (independent of the primary, and it can fire first):** if F1
shows `RS3PICK` per side within noise of zero on the 15-map pool — the live
possibility flagged in point 3, since 55.9% of the demonstrated dose was off-pool
and one in-pool demo map fired zero — then the plank did not deliver its dose in
the screen fixture and **the primary is uninterpretable in either direction**. Per
FIRINGS-BEFORE-PRIMARY this is read BEFORE the primary is typed; if it fires, the
primary is reported as **NOT MEASURED**, not as a null.

---

## READING, PRE-COMMITTED — the four share bands, CROSSED WITH the open mechanism question

Registered now so no cell is chosen after the fact. The four-band form is the
`KLADLADDER` precedent; the second table is this arm's own, because point 2 makes
the share alone insufficient to say what happened.

| band at n = 5,400 | pre-committed reading |
|---|---|
| **CI lower ≥ 51.33** | **THE PICK PAYS.** Resolved on this fixture. Promotes to a combination input and to a separately-registered head-to-head against the live holder — subject to the F2 cell below, which decides what may be CLAIMED about why. |
| **point ≥ 51.33 but CI lower < 51.33** | **REAL-BUT-SMALL, COMBINATION INPUT ONLY.** Registered in advance as WEAK: `NULL125`'s byte-identical A/A read 51.04, so a bare clearance in [51.33, 52.4] is not distinguishable from fixture noise by this leg alone. Rows KEPT; NO ship conversation; a replication on fresh seeds is the price of promoting it. |
| **CI includes 50.0** | **ADDS NOTHING MEASURABLE POOLED.** Read the primary segment next, and only the primary segment; note in advance that the segment's own half-width (±2.29pp) exceeds the effect the ceiling makes plausible, so an inconclusive segment is the EXPECTED outcome of this branch and must be reported as inconclusive rather than as a second null. |
| **CI upper < 51.33** | Primary falsifier fires — see the F2 cross below for what it licenses. |

### ⭐ THE F2 CROSS — pre-committed, and it is the reason this arm has an extra table

| | **F2 shows route length DOWN (interval on the difference excludes 0)** | **F2 shows route length FLAT or UP** |
|---|---|---|
| **screen at or above bar** | **MECHANISM CONFIRMED AS DESIGNED.** The pick moved, the route shortened, the share rose. Bank the chain and promote. | **⚠ WRONG-MECHANISM-RIGHT-EFFECT. FLAGGED, NOT BANKED.** The arm won without doing the thing it was built to do, so the win is attributable to some unnamed consequence of re-ordering picks (seat spread, timing, collision). **No sentence may claim route length as the cause**, the row is promoted only as a combination candidate, and the successor is an arm that isolates whatever actually moved. |
| **screen below bar** | **THE ROUTE GOT SHORTER AND IT DID NOT PAY.** That is a finding about the STUDY's §M3 pricing, not about this implementation, and it is worth banking: route length at build would then be measurably NOT the lever the 2-rounds-per-tile model implies at this magnitude. | **THE MECHANISM NEVER BOUND.** The demo's honest null reproduces at n = 60 sides. **ITERATE OR PARK, and the choice is pre-specified: iterate ONCE on `ROUTESCORE_CANDIDATES` (4 → the seat's full stripe) because a four-tile window may simply be too narrow to contain a shorter route; if that arm also shows no route-length movement, PARK the road.** No third tuning. |

⚠ **50.0 IS NOT A FLOOR AND A NEGATIVE IS A LIVE, PRE-NAMED OUTCOME.** Pulling
seats toward a near cluster (the study's own named risk, held off by the
preserved stripe) is a plausible route to a share materially BELOW 50, and
`KLADLADDER` has just shown this fixture returning 41.86 on a demo-clean arm.
**Named here so a negative is not explained away as noise.**

---

## MECHANISM DIAGNOSTICS TO READ AT READOUT

**Measurability is declared per metric. `NOT MEASURABLE` is written where it is
true, rather than a metric being quietly renamed into something the tape carries.**

### F1-F3 — the FIRINGS read. MEASURABLE, but NOT off the shard tape.

**EXECUTING TOOLS, named per Obligation 17: `zsh scratchpad/s48_demo_battery.sh
_v479routescore antler archipelago auroraveil drakkarfjord drumlin fjordgate
frostgate glacierkeep icefloe midgard nordkap ragnarok royale valkyrie yulerune`,
decoded by `scratchpad/s48_eco_demo.py` (F1, F3) and
`scratchpad/s48_routelen.py <replay…> --seat A|B` (F2).**
**OB17 checks, run, and the clause that could have surprised is named:**
1. *Name the executing tools* — done above, and there are TWO because F2 is a
   different decoder from F1.
2. *Confirm the RUNNERS emit what is registered* — `s48_demo_battery.sh:16` is
   `if (( $# )); then MAPS=($@); else MAPS=(yulerune icefloe drumlin eider); fi`,
   so the pool override is a path the script has; it writes each cell's replay to
   a DISTINCT path (`/tmp/s48_{ctl,trA,trB}_<map>_<seed>.replay26`), which is what
   makes F2 possible at all — `s48_routelen.py` takes replay FILES, so a shared
   or discarded replay path would leave F2 with nothing to read. And
   `s48_eco_demo.py:50-53` passes `--tle 10`, matching the shard.
   ⭐ **THE CLAUSE THAT COULD HAVE GONE THE OTHER WAY AND WAS RUN FIRST IS THE
   `--tle` ONE, and on THIS arm it is the one that matters most: this plank is
   the only one of the three s48 arms that adds BFS FLOODS to the hot path
   (`_link_path` under `LINK_NODE_BUDGET = 4096`, up to three extra per `_pick`
   call). A firings battery run without the CPU limit would measure a chassis the
   screen does not use, and would hide exactly the regression this plank could
   plausibly introduce.** It passes.
3. *Consequence of silent non-execution* — omitting the map list silently falls
   back to the four-map default, **which is the off-pool evidence base this
   battery exists to replace, and which includes `eider` (93 of the 220 demo
   picks)**; nothing in the output would say so. ⇒ **the readout must print the
   map list it actually ran.**

**Registered size: 60 treatment sides + 60 control sides** (15 maps × 2 seeds ×
both seats, with a base-vs-base control run on the same map and seed — the
battery's own design, because base-vs-base seat variance was measured larger than
anything a plank is expected to move). Run BEFORE the primary is typed, and its
per-map `RS3PICK` table committed before the primary is read, because it is what
fixes the primary segment.

* **F1 — DOSE DELIVERY ON THE POOL THE SCREEN PLAYS, PER MAP.** `RS3PICK` per
  side, per map. **Pre-registered expectation: `RS3PICK` > 0 on a majority of the
  15 pool maps, with a wide per-map spread.** Demo anchor, reported as an
  anecdote and NOT as an expected effect: 220 picks over 20 sides on five maps,
  `eider 93 · icefloe 88 · saga 30 · drumlin 9 · yulerune 0`, of which `eider`
  and `saga` are off-pool. **This table also FIXES THE PRIMARY SEGMENT and is
  committed before the primary is read.**
* **F2 — THE OPEN MECHANISM QUESTION: BFS ROUTE LENGTH AT BUILD, harvesters
  #3-#6.** Treatment vs control, on the same map and seed, decoded by
  `scratchpad/s48_routelen.py` (which recomputes the route off the replay, so it
  is the same metric for both arms and is computed by code neither of them runs).
  **Reported as a DIFFERENCE WITH AN INTERVAL from `tools/cluster_ci.py`, never
  as two medians side by side** — the demo's 9-vs-8 / 7-vs-8 is exactly the shape
  that reads as a finding and is not one. **Pre-registered expectation: LOWER in
  the treatment. The demo did NOT show this and that is the registered open
  question** (see THE F2 CROSS).
* **F3 — THE SAFETY PAIR AND THE PARTITION CHECK.** (a) connect RATE and
  harvester COUNT, reported TOGETHER, never apart (per the research steering note
  — the rate rises mechanically when fewer harvesters are built); demo anchor
  74.6% (100/134) vs 68.6% (109/159), by r25 72 vs 78. (b) **SEAT COLLISION: the
  number of distinct ore tiles targeted per side and any tile targeted by two
  seats at once.** The study's named risk is that route scoring pulls all seats
  onto one near cluster; the stripe is supposed to prevent it. **DESCRIPTIVE, and
  a rise here is a DEFECT report, not a nuance.**

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
* **Whether a shorter route actually produced an earlier DELIVERY.** The shard
  tape carries no resource column and the replays are discarded; the F-battery
  gives route length and connect round but not titanium delivered. **Under
  `R1000_IS_DEFEAT` that is the correct thing to be blind to — delivery is
  instrumental — but the blindness is stated rather than glossed.**
* **Per-unit CPU, which is this arm's most plausible hidden cost.** Local replays
  zero-fill `execTimeUs` (the s42 D33 instance: `tle_census.py` returns 0 across
  1,649 local builder-turns while reading 8,847 µs on platform replays), so **no
  CPU claim is available from this leg** — the study's "p99 550 µs of 10,000" is
  a PLATFORM measurement of the PARENT and does not price the added floods. The
  only local CPU signal available is the shard's own `--tle 10` behaviour, which
  is folded into the share and not separable from it. ⚠ **Disclosed:
  `LOKI_ROUTESCORE_LOG = True` in the fired tree adds one `print()` site the
  control does not have, and that site calls `_routescore_len` a SECOND time to
  print `L0`; the cache makes it cheap but it is not free. The base already ships
  `LOKI_L4_LOG` and `LOKI_SAMESTOP_LOG` at True, so logging is in-house
  precedent — but this is an unmatched per-pick cost in the TREATMENT'S direction
  under `--tle 10`, and it is named here rather than discovered later.**
* **Seed determinism.** `NOISE_ON` pins an unseeded per-unit salt, so base-vs-base
  at one seed diverges at round 0. **No seed-matched or replay-diff equivalence
  claim is available on the SHARD fixture**; the flag-off equivalence claim rests
  on the separate `--tle 0` + `NOISE_ON=False` harness (`scratchpad/s48_flagoff.sh`)
  and on the code, never on shard rows.

---

## THE CHANGE — `file:line`, control → treatment

**TREATMENT TREE: `bots/_v479routescore`** — byte-for-byte `bots/_v468kladturbo`
apart from three files. Verified at draft: `diff -rq` names exactly
`doctrine.py`, `eco.py` and `main.py`; **`raid.py` is byte-identical.**

1. **`doctrine.py` +1878-1952** — one comment block and five constants:
   `LOKI_ROUTESCORE_ON = True`, `ROUTESCORE_CANDIDATES = 4`,
   `ROUTESCORE_TTL_RNDS = 25`, `ROUTESCORE_FAR_TILES = 12`,
   `LOKI_ROUTESCORE_LOG = True`.
2. **`main.py` +101-108** — one per-unit field, `self.rs_len_cache = {}`, kept
   deliberately separate from the SAMESTOP one-slot plan cache (that one holds a
   PLAN and is evicted on every target change; this holds LENGTHS for several
   candidates and must survive across picks). No store slot.
3. **`eco.py:1194-1213`** — `_routescore_len`: `_link_path` under the unchanged
   `LINK_NODE_BUDGET`, with a TTL cache and saturation at
   `ROUTESCORE_FAR_TILES + 1` (past the knee, all routes score alike).
4. **`eco.py:1230-1247`** — the chooser: three early returns to the parent's
   answer (plank off / one candidate; no core or grid; `_cpu_exhausted`), then
   the scan whose swap line is **:1242**, with a STRICT `<` so an equal-length
   route never displaces the parent's cursor tile, and the `RS3PICK` log at
   **:1244**.
5. **`eco.py:1280-1300`** — `_pick`'s cursor walk, kept whole: the Manhattan sort
   and the `ordered[worker::workers]` stripe are the parent's exactly, and
   `n_cand = ROUTESCORE_CANDIDATES if LOKI_ROUTESCORE_ON else 1` is the only
   insertion — **with the plank off, `n_cand <= 1` returns on the first tile and
   the loop is the parent's byte for byte.**

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
on the strength of this number.** ⛔ **And per THE F2 CROSS, a bar-clearing screen
with no route-length movement does NOT reach that step as a route-length plank —
it reaches it as an unexplained one, and says so.**

---

**PROVENANCE:** `docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md` (read in full: obligations 7, 12, 13, 14, 15a-c and its units rider, 16 + its corollary and cross-host rider, 17 + its rider) · `docs/research/SPEC-prereg-check-2026-08-14.md` · `docs/research/SPEC-prereg-check-side-lane-checks-2026-08-14.md` · `docs/research/SPEC-metric-window-2026-08-15.md` · `docs/research/RULING-prereg-check-vocabulary-2026-08-14.md` · `docs/research/ECO-STUDY-fast-connected-harvesters-2026-08-17.md` (§0, §3.2, §7 M3, and BOTH amendments — the v155 slope is RETRACTED as a measured quantity and is not quoted anywhere on this page) · `docs/prereg/PREREG-KLADLADDER-2026-08-17.md` (house template and the four-band reading precedent) · `docs/prereg/PREREG-SEALSENTAN-2026-08-17.md` (same-day house style; its second-clock finding is engaged with above) · `docs/prereg/BARS.tsv` (header, the FIRINGS-BEFORE-PRIMARY rule, and the sibling klad-family rows) · `CLAUDE.md` · `tools/prereg_check.py` (read for `RULES`, `check_arithmetic`, `check_metric_window`, `check_pool_era`, `deff_for`) · `tools/auto_gate.py:224-250` · `tools/overnight.sh` (the 15-map pool at :66, the `# FIXTURE start=` stamp at :99-104, `--tle 10` and `--replay /dev/null` at :138-139) · `tools/cluster_ci.py` (v4) · `tools/fieldcal_read.py:230-256` · `scratchpad/s48_flagoff.sh` · `scratchpad/s48_demo_battery.sh` · `scratchpad/s48_eco_demo.py` · `scratchpad/s48_routelen.py` · `bots/_v479routescore/{doctrine,eco,main,raid}.py` · `bots/_v468kladturbo/{doctrine,eco,main,raid}.py` · `scratchpad/corefill_work.txt` · `scratchpad/CONTROL_PIN` · `results.tsv` (rows 346 `null125-final`, 454 `idnull140-cert-5400`, and the three 2026-08-17 `kladladder-*` rows) · git commit `e97a804b` and `git diff --name-only e97a804b^ e97a804b` · the drafting brief supplied by the builder lane s48 and the research lane's pre-lock steering note on connect-rate mediation. No file under `bots/`, `tools/`, `scratchpad/`, `docs/prereg/BARS.tsv`, `results.tsv`, `HANDOVER.md`, `PROGRAMME.md` or `QUEUE.md` was created or modified by this agent, and no game was run.
