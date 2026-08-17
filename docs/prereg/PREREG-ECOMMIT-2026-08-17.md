# SCREEN PREREG — `ECOMMIT`: commit to the route before you dig, and adopt the orphans

Drafted by a fresh opus subagent with no inherited session context beyond the
inputs listed under `PROVENANCE`. The builder lane ratifies the judgment lines
and types the lock commit; this agent wrote no code under `bots/`, appended no
worklist row, appended no `BARS.tsv` row, fired no game, started no shard, and
touched neither `results.tsv` nor `HANDOVER.md` nor `PROGRAMME.md` nor
`QUEUE.md`.

**STATUS: committed BEFORE the `ECOMMIT` row is appended to
`scratchpad/corefill_work.txt`, BEFORE any file named
`scratchpad/overnight/ECOMMIT.*` exists, and BEFORE the leg's first game.**
Drafting session wall clock at write time **`2026-08-17T05:36:44Z`** (`date -u`,
same shell call); repo HEAD at draft `7bcf0e5e` (author time
`2026-08-17T07:35:55+02:00`). Verified at draft:
`grep -c 'ECOMMIT' scratchpad/corefill_work.txt` → **0**; same grep on
`docs/prereg/BARS.tsv` → **0**; `ls scratchpad/overnight/ | grep -i ecommit` →
**empty**; `grep -cE '8(16|18|20)000' scratchpad/corefill_work.txt` → **0** (the
seed base is free).

### SECOND CLOCK — registered in the CONSERVATIVE form, and the brief's own boilerplate is amended here rather than copied

**REGISTERED SECOND CLOCK: the `ts` of the FIRST COMPLETED ROW of
`scratchpad/overnight/ECOMMIT.tsv`.** This is conservative by construction: the
shard's true start is strictly EARLIER than its first completed row, so the
lock-to-fixture gap this clock reports can only ever be UNDERSTATED, never
overstated — a certification that passes on it passes on any tighter clock.

⚠ **AND THE BRIEF'S STATED REASON FOR AVOIDING THE OTHER CLOCK DID NOT SURVIVE
MY CHECK, so it is corrected rather than repeated.** My drafting brief said the
`# FIXTURE … start=` stamp "names an artifact remote tapes lack and heartbeats
overwrite". **Checked at `tools/overnight.sh:99-104`: the runner computes
`START=$(date -u …)` and writes `# FIXTURE\t…\tstart=$START` as the tape's FIRST
LINE, before the first `fcode run`, on any tape that does not already exist.**
The heartbeat is a SEPARATE file (`$HB`), not the tape, so nothing overwrites the
stamp; and the remote-tape objection is real but does not bind here — this is a
LOCAL shard started by `tools/overnight.sh`. ⇒ **the stamp WILL exist and is the
tighter clock; it is registered as a CORROBORATING second clock, not as the
primary.** If the tape instead carries `# FIXTURE-RESUME … start=UNKNOWN-legacy-tape`
(`tools/overnight.sh:105`) or no `# FIXTURE` line at all, the registered
first-completed-row clock is the only one and nothing changes.

⚠ **The treatment tree ALREADY EXISTS and is committed** (`bots/_v477ecommit`,
added `d67eb98e`, author time `2026-08-17T07:29:33+02:00`). That is legitimate —
built and demo-verified before any registration — but it means this document is
**NOT** locked before the arm exists, only before the arm's first screen row.
Said here rather than left for a certifier to find. It is also what makes
Obligation 13's intersection **computable at lock time**.

---

## ⛔ READ BEFORE RATIFYING — SIX THINGS THE LANE OWNS

**1. THE CONTROL IS THE LIVE INCUMBENT, SO 50.0 MEANS "ADDS NOTHING".**
`bots/_v468kladturbo` is Sleipnir v1, pinned as the corefill control at
`scratchpad/CONTROL_PIN` (`a9228ccb56ed9a65dd7d72ad1cb96068 bots/_v468kladturbo`),
per Magnus's benchmark ruling that our arms compete against Sleipnir during core
shards. **A reader who transplants a 61-shaped intuition from the
KLADTURBO-vs-v140 read onto this page has misread the fixture: the same bot
measured against itself reads 50.**

**2. ⛔⛔ THE PRIMARY IS POOLED GAME SHARE. CONNECT RATE IS A MECHANISM METRIC AND
MUST NEVER BE QUOTED AS THIS ARM'S RESULT.** The demo's **96.6% (57/59) vs 66.4%
(79/119)** connect rate is a DOSE reading on 16 seat-matched games. It is not a
verdict and it is not an effect size. **The reason is causal, not stylistic:
connect rate is a MEDIATOR THE OUTCOME FEEDS BACK INTO.** Research's pre-lock
check measures connect rate strongly outcome-associated (within-map slope
**+0.56 [0.46, 0.66]**, clustered on match; paired within-game **0.667
[0.62, 0.71]**) **while the arrow is contaminated by reverse causation** — a
losing side gets its belt cut, and the same read carries a **2.58x belt-death
asymmetry** with **50.9% of conveyor deaths near live enemy gunners**. In a
randomised two-arm shard the WIN SHARE is clean; a connect-rate-denominated bar
would measure a quantity the result partly produces. ⇒ **No sentence in this
leg's readout may denominate a bar, a verdict or a promotion in connect rate.**

**3. ⛔ THE MECHANISM METRIC IS A PAIR AND IT IS UNREADABLE AS A SINGLETON:
CONNECT RATE AND HARVESTER COUNT, ALWAYS TOGETHER.** The registered over-refusal
risk (below) means the RATE can rise **MECHANICALLY** — refuse enough sites and
the survivors are the easy ones, so the ratio improves with zero gain and a
smaller economy. The demo shows exactly this shape: rate 66.4% → 96.6%, and the
CONNECTED COUNT still falls, **79 → 57 over sixteen sides each (4.94 → 3.56 per
side, −28%)**, on a lifetime harvester count of **119 → 59**. **Either number
alone tells the wrong story; the pair is the metric.**

**4. ⚠ REGISTERED RISK, CARRIED FROM THE STUDY'S OWN MITIGATION AND REALISED IN
THE DEMO: OVER-REFUSAL.** Lifetime harvesters roughly HALVED (59 vs 119 over 16
sides each), **123 of the 170 demo deferrals (72.4%) were reason-coded `long`**,
and `ECOMMIT_MAX_LINK_TILES = 8` is therefore the binding constant.
**PRE-COMMITTED READING FOR A NEGATIVE, written before the data: if the screen
reads below bar, THE NAMED FIRST SUSPECT IS OVER-REFUSAL VIA THE `long` GATE, AND
THE NEXT ITERATION IS THE CONSTANT, NOT THE MECHANISM'S DEATH.** The
discriminating signature is registered in advance in `READING, PRE-COMMITTED`:
below-bar share **with** a high connect rate **and** a halved harvester count is
the over-refusal branch. A below-bar share with the connect rate NOT up is a
different finding and does not license the constant retry.

**5. THE SHARD TAPE CANNOT SEE THE MECHANISM, SO A FIRINGS READ IS MANDATORY
BEFORE THE PRIMARY.** `tools/overnight.sh:138-139` runs every game with
`--replay /dev/null`, and the tape's columns are
`ts shard game map seed seat winner cond turns` — **no entity, build, belt or
stdout information exists on it, in either arm.** The plank's mechanism is
CONDITIONAL (a reason-coded refusal gate plus a periodic adoption scan), so
`docs/prereg/BARS.tsv`'s FIRINGS-BEFORE-PRIMARY rule (adopted
2026-08-16T13:27:33Z) binds: **F1/F2/F3 below run on a SEPARATE battery that
keeps replays, and must be read BEFORE the primary sentence is typed.** What the
tape CAN answer is the kill-clock question (`cond`, `turns`, `winner`), which is
why D1-D3 are shard-native and F1-F3 are not.

**6. THIS FIXTURE PRODUCES LARGE NEGATIVES AND HAS JUST DONE SO.** `KLADLADDER`,
demo-clean on the same base with the same flag-off SHA method, finished
**41.86% [40.20, 43.52] at n = 3,404** (`results.tsv`, `kladladder-n-final-correction`,
2026-08-17T05:18:10Z) — **8 points BELOW the null**, with its dose confirmed
delivered. **A clean demo predicts FIRING and predicts nothing about SHARE.** No
sentence on this page may treat the demo as a forecast.

---

## RATIFY: Hypothesis

**Gating every harvester placement on a committed, funded, length-bounded route
home, plus adopting orphaned conveyor chains, raises our LOCAL pooled game share
against `bots/_v468kladturbo` itself to 51.33% or higher at n = 5,400 games
across all 15 corefill maps and both seats.**

**The mechanism claim, stated so it can be wrong** — three effects, and the
hypothesis is that the first two outweigh the third:
* **IT STOPS BUYING NOTHING.** A harvester that never routes home costs 20 Ti at
  scale and leaves **+5% permanent cost scale** behind it for zero delivery. The
  gate refuses those sites before the spend.
* **IT RECOVERS STRANDED BELT.** `link_queue` is per-builder instance state with
  no store slot, so a builder that dies, converges or is thrown takes its route
  plan with it, and `_l4_repair` explicitly refuses the wreckage. `_adopt_orphan`
  is the hand-off the parent tree has nowhere.
* **⚠ AND IT REFUSES SITES THAT WOULD HAVE PAID.** The `long` gate is a hard cut
  at 8 tiles and the corpus knee is a smooth degradation, not a cliff. Every
  refusal is a harvester not built, and the demo halved the lifetime count.
  **This is a REAL cost in the treatment's own currency (cost scale is saved but
  delivery is lost), and it is why a flat or negative result is informative.**

**⇒ A flat result is INFORMATIVE and is not a null about "route commitment".** It
would say the scale saved and the delivery lost cancel, which is a different
finding from "committing to the route does nothing".

---

## REGISTRATION BLOCK

**TARGET BAND: N/A — local corefill screen with ZERO rated ladder exposure: no submission, no activation, no unrated challenge, so `tools/target_value.py` has no input. Nothing on this page ends in a ship; the only branch that reaches the ladder is a later, separately-registered head-to-head against the holder.**
**PINNED: N/A — local self-play. The opponent version is fixed by construction: the control tree is `bots/_v468kladturbo` at the commit this shard runs from, pinned at `scratchpad/CONTROL_PIN` (`a9228ccb56ed9a65dd7d72ad1cb96068 bots/_v468kladturbo`). There is no opponent churn to pin against and no calibration relevance to protect.**
**SURFACE: local**
**CLUSTER UNIT: none** — CLAUDE.md's enumeration PERFORMED, not asserted: (i) the **MATCH** cluster does not exist on this surface — `tools/overnight.sh` writes one TSV row per `fcode run`, so 1 row = 1 game and no row shares a match with another; (ii) the **OPPONENT** cluster is degenerate — every one of the 5,400 rows plays the identical control tree, so the pooled stratum holds exactly one opponent and there is no between-opponent variation for a design effect to describe. Both clusters die ⇒ DEFF = the measured local constant **0.98** (pair-weighted, ρ = −0.020, 124 shards, s39 audit). **The platform constants (1.529 rated / 1.833 unrated) are NOT applicable and applying them would widen every interval here 24-35% for correlation that has been measured absent.** ⚠ **The s42 cross-host rider is registered and does not bind: this arm is a WITHIN-HOST local cell and nothing on this page pools across hosts.** If a remote replication is later stocked it is REPORTED SEPARATELY and NEVER POOLED, per the GUNAXABL/SENTTHR precedent.
**ESTIMATOR: unweighted pooled treatment game share** = (rows with `winner == T`) / (completed rows), over all 5,400 rows, both seats pooled, all 15 maps pooled, no reweighting. Interval by `tools/cluster_ci.py` (v4, at HEAD) with the local constant. Seat A and seat B shares are reported SEPARATELY as a fixture diagnostic and are never the bar — seat is worth ~6.8pp on byte-identical arms, which is why the n is a multiple of 30.
**DOSE: harvester-site refusals per side — treatment 10.6 vs flag-off control 0.0 (n=16 seat-matched demo sides, `d67eb98e`; both verdicts driven — with `LOKI_ECOMMIT_ON=False` the arm's replay SHA-256 is identical to the base in sixteen of sixteen cells, and with the flag ON it differs in sixteen of sixteen, `scratchpad/s48_flagoff.sh`, NOISE_ON=False + `--tle 0`). ⚠ THIS IS A FIRING DEMONSTRATION AND NOT AN EFFECT SIZE — one-game cells on a fixture where a same-code BASE-vs-BASE pair on one map and seed read 18.4% oscillation on seat A against 41.3% on seat B (`scratchpad/s48_demo_battery.sh` header), i.e. the seat effect alone is larger than anything a plank is expected to move.**
**PLANNED n: 5400 games** (= 15 maps × 2 seats × 180, so map and seat balance is exact; `tools/overnight.sh:66` has run a 15-map pool since the 2026-08-13 rotation and its own comment requires multiples of 30).
**BOUNDARY: 5400 games** — LOCAL surface, one tape row is one game; there is no accept/attempt distinction on this fixture.
**CUT-SHORT: floor 2700 games.** Below 2,700 completed tape rows this leg publishes descriptive tallies (share, per-seat, per-map, kill-clock) and takes **NO comparative look and no bar verdict**; the half-width at 2,700 is ±1.87pp, already wider than the 1.33pp margin the bar is built on, so a sub-2,700 read cannot resolve its own branches. An `auto_gate` cancellation at MARK-400, MARK-1000 or TREND-FLOOR@1000 is an OPERATIONAL STOP, not a verdict, and is typed `cancellation`.
**BAR: 51.33**
**BASE RATE: 50.00**
**BAR SOURCE:** house-standard corefill futility band, `50 + 1.96*sqrt(.25/5400) = 51.33pp`, local DEFF 0.98 so naive — the identical bar carried by `docs/prereg/BARS.tsv` rows `SEALFLOOR6`, `SENTTHR`, `KLADTKILL`, `KLADTK2`, `KLADTURBOR`, `DRAINTURBO` and `KLADLADDER`, which is what keeps this arm numerically comparable to its siblings. **Constructed, not observed.** ⛔ **KIND OF BAR, per the OB16 corollary: this is a POINT RULE. The standard band is `50 ± half_width`, so its implied MDE is 0.000pp and clearing it excludes 50.0 and NO positive effect size.** It may not be quoted as having excluded an effect. That is a deliberate choice: the question this leg asks is *does route commitment move anything at all against the incumbent*, which is exactly what a point rule is the right instrument for.
**BASE RATE SOURCE:** structural A/A expectation of a seat-balanced, map-balanced self-play fixture whose control tree is the treatment's own base. Empirically calibrated by `IDNULL140` — **49.27% [47.94, 50.60] at n = 5,400**, 2026-08-16T18:02:04Z, same host and fixture (`results.tsv:454`) — and by `NULL125` — **51.04% at n = 5,400** (`results.tsv:346`). Two A/A cells, one either side of 50.0, both intervals containing it.
**POOL ERA: post-2026-08-13-rotation** — the 15-map local pool of `tools/overnight.sh:66`. (`check_pool_era` treats this as n/a on a LOCAL surface per SPEC §6; declared anyway so the population is on the page.) ⚠ **AND IT IS NOT COSMETIC HERE: two of the four demo maps' worth of evidence is OFF-POOL.** The demo battery ran `yulerune icefloe drumlin eider`; **`eider` is NOT in the 15-map corefill pool.** The dose that gates this screen was therefore measured partly on geometry the screen never plays — which is precisely why F1-F3 below are re-run on the FULL pool before the primary.
**REFERENCE n: none** — the comparator is generated inside this same shard from the same 5,400 seeds; there is no fixed external reference sample, so no resolution floor at n→∞.
**TREATMENT TREE: bots/_v477ecommit**
**TREATMENT DIFF REFS: d67eb98e^ d67eb98e**
**MECHANISM METRIC READS: bots/_v477ecommit/eco.py:961 — `return "long"`, the binding branch of the reason-coded gate `_ecommit_why` (eco.py:908-970); observed as F1 via the `EC1DEFER … why=` tag emitted at eco.py:976 and the `EC1ADOPT` tag at eco.py:1044, decoded by `scratchpad/s48_eco_demo.py` out of the LOCAL replay's `BotOutput.stdout` (populated locally; stripped only on platform-downloaded replays). TREATMENT DIFF TOUCHES: bots/_v477ecommit/eco.py bots/_v477ecommit/doctrine.py bots/_v477ecommit/main.py. INTERSECTION: yes — `_ecommit_why` and `_ecommit_defer` are inside the block the arm ADDS to `eco.py` (they do not exist in the control at all — a `grep -c` for `_ecommit_why` over every source file of the control tree returns 0), and the metric cannot read identically in both arms because the control has no gate to refuse anything.**
⚠ **DIFF-REFS DISCLOSURE:** `d67eb98e` ADDS the whole tree, so `git diff d67eb98e^ d67eb98e --name-only` returns FOUR paths including `raid.py`. The SEMANTIC diff against the control is THREE files: `diff -rq bots/_v468kladturbo bots/_v477ecommit` names `doctrine.py`, `eco.py`, `main.py` only, and `raid.py` is byte-identical. `TREATMENT DIFF TOUCHES` above declares the semantic three; the extra path in the git diff is an artefact of adding a tree, not an undeclared change.
**METRIC WINDOW: r0-r1000. GATING CONSTANTS: ECOMMIT_MAX_LINK_TILES=8, ECOMMIT_BAN_RNDS=40, ECOMMIT_ADOPT_EVERY=6, ECOMMIT_ADOPT_MAX_TILES=8. MECHANISM CAN OCCUR IN WINDOW: yes** — **there is NO round floor anywhere in this plank.** The gate is consulted on the first harvester placement of the game, and the demo's first `EC1DEFER` tags land inside the opening eco phase. The window is the whole game because a deferral BAN lapses after 40 rounds and an adoption scan re-arms every 6, so both halves can fire at any round.
⚠ **DISCLOSED, because a green tool run with warnings under it is how a warning stops being read: `prereg_check.py` emits FOUR `OBLIGATION 17, PARTIAL WINDOW` warns against this line and ALL FOUR ARE ARTEFACTS OF THE CHECKER.** `check_metric_window` reads every declared integer as a ROUND, and **NONE of these four constants is a round FLOOR.** `ECOMMIT_MAX_LINK_TILES` and `ECOMMIT_ADOPT_MAX_TILES` are TILE budgets; `ECOMMIT_BAN_RNDS` and `ECOMMIT_ADOPT_EVERY` are DURATIONS (how long a ban lasts, how often a scan re-arms), not thresholds a round must exceed. They are declared anyway because they are the constants that actually gate the plank, and an undeclared gate is the failure the obligation exists for.
**PRE-STATE: the predicted-change set is NOT already in the target state at lock.** Verified at draft against the control tree: `grep -c LOKI_ECOMMIT_ON bots/_v468kladturbo/*.py` → **0 in every file**; same for `_ecommit_why` and `_adopt_orphan` → **0 in every file**. The control performs **no** route check of any kind before placing a harvester (this is the study's §3.2 finding about `_expand`), has no ore-tile deferral ban, and has no orphan-chain adoption — `_l4_repair`'s own docstring refuses dead heads. The three behaviours this leg predicts to change therefore cannot already be in the target state.
**MAP SEGMENT: none expected — and the reason is that I cannot SIGN one, which under Obligation 15a is a reason to declare none rather than to declare an unfalsifiable segment.** The mechanism is gated on ROUTE LENGTH, so it fires more on large-area maps with spread ore (the five 900-area maps: midgard, ragnarok, valkyrie, drakkarfjord, glacierkeep). **But more firing cuts BOTH ways here** — the same geometry that produces the most never-connecting harvesters (the gate's benefit) produces the most `long` refusals (the over-refusal cost), and the demo shows both effects are large. **A segment declared without a predicted sign "confirms" the mechanism whichever way it lands, which is exactly what 15a forbids.** Per-size-class shares WILL be printed at readout as **DESCRIPTIVE** material whose declared purpose is to DIAGNOSE the over-refusal risk (metric 3 below), **not to rescue a failed pooled primary**. **No map cut may rescue this arm**, and nothing may be banked off those shares without a fresh prereg.
**CELL VERSION CHURN: N/A — not a panel, no `CELLS:` line, one fixed local control tree.**
**GATE RESOLUTION: the shard is governed by the pinned `tools/auto_gate.py` marks — n≥400 CATASTROPHE if the 95% CI upper < 45.0; at each mark from n≥1000 STOP if the CI upper < the shard's bar (51.33); TREND-FLOOR@1000 if the first-1000 prefix share < 52.0 (`tools/auto_gate.py:233-250`). Those are OPERATIONAL CANCELLATIONS that free a core — they are typed `cancellation`, never `verdict`, and they license NO exclusion claim, because the registered target is 5,400. The RESOLVABLE gate this document owns is the primary at full n, whose margin (1.33pp) exceeds its own half-width (±1.32pp) by 0.01pp — resolvable, and only just. Everything else on this page (F1-F3, D1-D3, the seat and map splits) is DIAGNOSTIC and cannot rescue a failed primary. Any branch that does not resolve is UNRESOLVED, and an UNRESOLVED gate defaults to the RESTRICTION: no promotion, no ship conversation, no combination claim.**

---

## FALSIFIER

**PRIMARY FALSIFIER: at n = 5,400 the 95% CI UPPER bound on the treatment's
pooled game share falls BELOW 51.33.** That excludes the bar and says route
commitment does NOT add measurably to Sleipnir on this fixture.
**Consequence, registered in advance and BRANCHED, because the two branches
license different next moves:**
* **If the F-battery ALSO shows connect rate UP and harvester count DOWN** (the
  over-refusal signature), the CONSTANT is the named suspect. The row closes as
  written and the successor is a single-constant iteration
  (`ECOMMIT_MAX_LINK_TILES` raised, or the `long` refusal converted to a
  preference rather than a veto) — **one arm, one constant, its own prereg.**
* **If the F-battery shows the connect rate NOT up**, the mechanism did not do
  the thing it was built to do on the pool the screen plays, and **the road
  closes without a constant retry** — a tuning pass on a mechanism that did not
  bind is the cheapest kind of null this repo buys.

**MECHANISM FALSIFIER (independent of the primary, and it can fire first):** if
F1 shows the treatment's reason-coded refusals per side are within noise of zero
on the 15-map pool — i.e. the dose measured on the four demo maps does not
reproduce on the maps the screen actually plays — then the plank did not deliver
its dose in the screen fixture and **the primary is uninterpretable in either
direction**: a flat share would mean "the mechanism never fired", not "the
mechanism fired and did not pay". Per the FIRINGS-BEFORE-PRIMARY rule this is
read BEFORE the primary is typed, and if it fires the primary is reported as
**NOT MEASURED**, not as a null.

---

## READING, PRE-COMMITTED — four bands, written before the data

Registered now so no band is chosen after the fact. The four-band form is the
`KLADLADDER` precedent.

| band at n = 5,400 | pre-committed reading |
|---|---|
| **CI lower ≥ 51.33** | **ROUTE COMMITMENT ADDS.** Real and resolved on this fixture. Promotes to a combination input and to a separately-registered head-to-head against the live holder. Report the size honestly and report the harvester COUNT alongside it — a win bought while the economy shrank is a different plank from a win bought while it grew, and the pair is what says which. |
| **point ≥ 51.33 but CI lower < 51.33** | **REAL-BUT-SMALL, COMBINATION INPUT ONLY.** Registered in advance as WEAK: `NULL125`'s byte-identical A/A read 51.04, so a bare clearance in [51.33, 52.4] is not distinguishable from fixture noise by this leg alone. Rows are KEPT and the arm is available for combination; it does NOT license a ship conversation, and a replication on fresh seeds is the price of promoting it. |
| **CI includes 50.0** | **ADDS NOTHING MEASURABLE.** The scale saved and the delivery lost cancel, or neither binds. Read the F-battery pair to say which: high connect rate + halved count = the trade is real and nets to zero; flat connect rate = the gate never bound. Combination input only if another arm supplies a mechanism reason. |
| **CI upper < 51.33** | Primary falsifier fires — see the two branches above. |

⚠ **50.0 IS NOT A FLOOR AND A NEGATIVE IS A LIVE, PRE-NAMED OUTCOME.** The
over-refusal mechanism is a plausible route to a share materially BELOW 50, and
`KLADLADDER` has just demonstrated that this fixture returns 41.86 on an arm
whose demo was clean. **It is named here so a negative is not explained away as
noise, and so the constant-iteration branch is a pre-registered response rather
than a rescue.**

---

## MECHANISM DIAGNOSTICS TO READ AT READOUT

**Measurability is declared per metric. `NOT MEASURABLE` is written where it is
true, rather than a metric being quietly renamed into something the tape carries.**

### F1-F3 — the FIRINGS read. MEASURABLE, but NOT off the shard tape.

**EXECUTING TOOL, named per Obligation 17: `zsh scratchpad/s48_demo_battery.sh
_v477ecommit antler archipelago auroraveil drakkarfjord drumlin fjordgate
frostgate glacierkeep icefloe midgard nordkap ragnarok royale valkyrie yulerune`,
decoded by `scratchpad/s48_eco_demo.py`.**
**OB17 checks, run, and the one that could have surprised is named:**
1. *Name the executing tool* — done above.
2. *Confirm the RUNNER emits what is registered* — `s48_demo_battery.sh:16` is
   `if (( $# )); then MAPS=($@); else MAPS=(yulerune icefloe drumlin eider); fi`,
   so the pool override IS a path the script has; and `s48_eco_demo.py:50-53`
   passes `--replay <path>` and **`--tle 10`**, matching the shard's own
   `--tle 10`. ⭐ **THIS IS THE CLAUSE THAT COULD HAVE GONE THE OTHER WAY AND IT
   WAS RUN FIRST: a firings battery run WITHOUT `--tle` would measure a chassis
   the screen does not use** (`tools/overnight.sh` documents `_v145bestfit`
   winning 6/6 with the limit off and losing 5/6 with it on). It passes.
3. *Consequence of silent non-execution* — if the map list is omitted the script
   silently falls back to its four-map default, which is **exactly the off-pool
   evidence base this battery exists to replace**, and nothing in the output
   would say so. ⇒ **the readout must print the map list it actually ran.**

**Registered size: 60 treatment sides + 60 control sides per arm** (15 maps × 2
seeds × both seats, with a base-vs-base control run on the same map and seed —
the battery's own design, because base-vs-base seat variance was measured larger
than anything a plank is expected to move). Run BEFORE the primary is typed.

* **F1 — DOSE DELIVERY ON THE POOL THE SCREEN PLAYS.** Reason-coded `EC1DEFER`
  refusals per side, split `route` / `long` / `bank`, and `EC1ADOPT` adoptions
  per side, per map. **Pre-registered expectation: refusals per side > 0 on a
  majority of the 15 pool maps, with `long` the modal reason.** Demo anchor,
  reported as an anecdote and NOT as an expected effect: 170 deferrals (123
  `long`, 47 `bank`) and 56 adoptions over 16 sides on four maps, one of which
  is off-pool (`d67eb98e`).
* **F2 — THE PAIR: connect RATE and harvester COUNT, reported together, never
  apart.** Per side: harvesters built (lifetime AND by r25), harvesters ever
  structurally connected, and the ratio. **Pre-registered expectation: rate UP,
  count DOWN — and the readout states the CONNECTED COUNT per side, which is the
  number the rate hides.** Demo anchor (anecdote): rate 66.4% → 96.6%, connected
  count 4.94 → 3.56 per side, lifetime 7.44 → 3.69 per side.
* **F3 — OVER-REFUSAL BY MAP SIZE CLASS.** F1's refusal rate and F2's pair, split
  `small` / `mid` / `900-area`. **DESCRIPTIVE ONLY** — this is the diagnostic that
  tells the constant-iteration branch which way to move
  `ECOMMIT_MAX_LINK_TILES`, and it is explicitly NOT a segment and cannot rescue
  the primary (see `MAP SEGMENT`).

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
  OUR core kill scoring the full 300 (`tools/fieldcal_read.py:239`, the
  registered estimator; the loose definition is a sensitivity column only).
  Reported with its interval from `tools/cluster_ci.py`. **ITT over ALL rows, not
  over kills only** — the kill-conditioned form carries a collider, per
  `PROGRAMME.md`.

### NOT MEASURABLE on this leg — named, not silently dropped.
* **Titanium actually DELIVERED** (`titanium_collected`) — the shard tape carries
  no resource column and the replays are discarded. The economy is observed only
  through harvester and belt structure in the F-battery. **Under
  `R1000_IS_DEFEAT` this is the correct thing to be blind to** — delivery is
  instrumental — but the blindness is stated rather than glossed.
* **Cost scale at any round.** The saving this plank's first mechanism buys
  (+5% per harvester not built) is a headline number of the study and is **NOT
  READABLE** on either surface here. It is inferable from F2's count and is not
  measured.
* **Per-unit CPU.** Local replays zero-fill `execTimeUs` (the s42 D33 instance:
  `tle_census.py` returns 0 across 1,649 local builder-turns while reading
  8,847 µs on platform replays), so **no CPU claim is available from this leg.**
  The demo's "0 TLEs in 16 games" is an anecdote. ⚠ **Disclosed:
  `LOKI_ECOMMIT_LOG = True` in the fired tree adds two `print()` sites the
  control does not have. The base already ships `LOKI_L4_LOG` and
  `LOKI_SAMESTOP_LOG` at True, so this is in-house precedent and the cost is
  small — but it is an unmatched per-turn cost in the TREATMENT'S direction
  (against it) under `--tle 10`, and it is named here rather than discovered
  later.**
* **Seed determinism.** `NOISE_ON` pins an unseeded per-unit salt, so base-vs-base
  at one seed diverges at round 0. **No seed-matched or replay-diff equivalence
  claim is available on the SHARD fixture**; the flag-off equivalence claim is
  made on the separate `--tle 0` + `NOISE_ON=False` harness
  (`scratchpad/s48_flagoff.sh`) and on the code, never on shard rows.
* **Which half carries the effect** — the GATE vs ORPHAN ADOPTION — is **NOT
  SEPARABLE** by this leg. They ship under one flag (`LOKI_ECOMMIT_ON`), and the
  study's own instruction is not to implement them apart. Separating them needs a
  further arm using `ECOMMIT_ADOPT_ON`, which the tree already exposes; it is NOT
  attempted here and **no readout sentence may attribute the result to one half.**

---

## THE CHANGE — `file:line`, control → treatment

**TREATMENT TREE: `bots/_v477ecommit`** — byte-for-byte `bots/_v468kladturbo`
apart from three files. Verified at draft: `diff -rq` names exactly
`doctrine.py`, `eco.py` and `main.py`; **`raid.py` is byte-identical.**

1. **`doctrine.py` +1878-1963** — one comment block and eight constants:
   `LOKI_ECOMMIT_ON = True`, `ECOMMIT_MAX_LINK_TILES = 8`,
   `ECOMMIT_FUND_BELT = True`, `ECOMMIT_BAN_RNDS = 40`,
   `ECOMMIT_ADOPT_ON = True`, `ECOMMIT_ADOPT_EVERY = 6`,
   `ECOMMIT_ADOPT_MAX_TILES = ECOMMIT_MAX_LINK_TILES`, `LOKI_ECOMMIT_LOG = True`.
2. **`main.py` +101-110** — two per-unit fields, `self.ecommit_ban = {}` and
   `self.adopt_next = -1`. No store slot.
3. **`eco.py:851-1044`** — five new methods: `_ecommit_banned`, `_ecommit_route`,
   `_ecommit_unpaid`, **`_ecommit_why` (the gate, 908-970 — `route` / `long` /
   `bank`, with EVERY exception path ADMITTING the build)**, `_ecommit_defer`,
   and `_adopt_orphan`.
4. **`eco.py:1419, 1896-1910, 2028, 2052`** — the four call sites: the ban honoured
   in `_pick`'s cursor walk, in the build loop (where `_ecommit_why` is consulted
   at 1910) and in the adjacent-ore short-circuit, plus the adoption scan at 2028.

**THE GATE READS AN EXISTING CACHE, NOT A NEW ROUTER:** `_ecommit_route` asks
`_samestop_plan`, the same per-ore-tile cache the stop-tile preference already
fills one branch later in the same turn. A site in the core ring or with a live
acceptor beside it is admitted with no flood at all.

---

## WHAT THIS LEG COSTS AND WHAT IT DOES NOT

**Cost: one local core to n = 5,400, plus ~90 local games for the F-battery.**
ZERO rated ladder exposure, zero submissions, zero unrated challenges — nothing
on this page touches the platform, which is why `TARGET BAND` is N/A.

**It does NOT decide a ship.** The strongest branch promotes the arm to (a) a
combination input and (b) a separately-registered head-to-head against the live
holder, which is the pipeline step Magnus's procedure names verbatim (*"we start
by testing it against the current slot, If it beats it we can switch"*) and which
`SLEIPH2H` is the template for. **Gate-1-to-gate-2 transitivity is UNVALIDATED in
this repo (QUEUE #65: 3 concordant, 1 not), so the head-to-head is not skippable
on the strength of this number.**

---

**PROVENANCE:** `docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md` (read in full: obligations 7, 12, 13, 14, 15a-c, 16 + its corollary and cross-host rider, 17 + its rider) · `docs/research/SPEC-prereg-check-2026-08-14.md` · `docs/research/SPEC-prereg-check-side-lane-checks-2026-08-14.md` · `docs/research/SPEC-metric-window-2026-08-15.md` · `docs/research/RULING-prereg-check-vocabulary-2026-08-14.md` · `docs/research/ECO-STUDY-fast-connected-harvesters-2026-08-17.md` (§0, §3.2, §3.5, §3.6, §7 M1, and BOTH amendments — the v155 slope is RETRACTED as a measured quantity and is not quoted anywhere on this page) · `docs/prereg/PREREG-KLADLADDER-2026-08-17.md` (house template and the four-band reading precedent) · `docs/prereg/PREREG-SEALSENTAN-2026-08-17.md` (same-day house style; its second-clock finding is engaged with above) · `docs/prereg/BARS.tsv` (header, the FIRINGS-BEFORE-PRIMARY rule, and the sibling klad-family rows) · `CLAUDE.md` · `tools/prereg_check.py` (read for `RULES`, `check_arithmetic`, `check_metric_window`, `check_pool_era`, `git_diff_paths`, `deff_for`) · `tools/auto_gate.py:224-250` (the pinned marks and the trend floor) · `tools/overnight.sh` (the 15-map pool at :66, the `# FIXTURE start=` stamp at :99-104, `--tle 10` and `--replay /dev/null` at :138-139) · `tools/cluster_ci.py` (v4 docstring — the interval instrument for every estimate quoted at readout) · `tools/fieldcal_read.py:230-256` (the registered RMST estimator) · `scratchpad/s48_flagoff.sh` · `scratchpad/s48_demo_battery.sh` · `scratchpad/s48_eco_demo.py` · `bots/_v477ecommit/{doctrine,eco,main,raid}.py` · `bots/_v468kladturbo/{doctrine,eco,main,raid}.py` · `scratchpad/corefill_work.txt` · `scratchpad/CONTROL_PIN` · `results.tsv` (rows 346 `null125-final`, 454 `idnull140-cert-5400`, and the three 2026-08-17 `kladladder-*` rows) · git commit `d67eb98e` and `git diff --name-only d67eb98e^ d67eb98e` · the drafting brief supplied by the builder lane s48 and the research lane's pre-lock steering note on connect-rate mediation (within-map slope +0.56 [0.46,0.66] clustered on match; paired within-game 0.667 [0.62,0.71]; 2.58x belt-death asymmetry; 50.9% of conveyor deaths near live enemy gunners). No file under `bots/`, `tools/`, `scratchpad/`, `docs/prereg/BARS.tsv`, `results.tsv`, `HANDOVER.md`, `PROGRAMME.md` or `QUEUE.md` was created or modified by this agent, and no game was run.
