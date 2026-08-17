# SCREEN PREREG — `ECOMMIT2`: the CATASTROPHE row's pre-committed over-refusal branch, executed on one constant (`ECOMMIT_MAX_LINK_TILES` 8 → 16)

Drafted by a fresh opus subagent with no inherited session context beyond the
inputs listed under `PROVENANCE`. The builder lane ratifies the judgment lines
and types the lock commit; this agent wrote no code under `bots/`, appended no
worklist row, appended no `BARS.tsv` row, fired no game, started no shard, and
touched neither `results.tsv` nor `HANDOVER.md` nor `PROGRAMME.md` nor
`QUEUE.md`.

**STATUS: committed BEFORE the `ECOMMIT2` row is appended to
`scratchpad/corefill_work.txt`, BEFORE any file named
`scratchpad/overnight/ECOMMIT2.*` exists, and BEFORE the leg's first game.**
Drafting session wall clock at write time **`2026-08-17T07:12:01Z`** (`date -u`,
same shell call); repo HEAD at draft `12e71962` (author time
`2026-08-17T09:10:53+02:00`). Verified at draft:
`grep -c 'ECOMMIT2' scratchpad/corefill_work.txt` → **0**; same grep on
`docs/prereg/BARS.tsv` → **0**; `ls scratchpad/overnight/ | grep -i ecommit2` →
**empty**; `grep -cE '834000' scratchpad/corefill_work.txt` → **0** (the seed base
is free; the highest local seedbase currently in any worklist is 826000).

### SECOND CLOCK
**PRIMARY: this commit's git author time against the `# FIXTURE … start=` stamp
`tools/overnight.sh:103` writes as the first line of
`scratchpad/overnight/ECOMMIT2.tsv` (its `START=` is computed at `:99`), before the
first `fcode run`.** The ECOMMIT tape carries exactly this line and it is quoted in
full under PROVENANCE, so the mechanism is confirmed on a live artifact rather than
assumed.
**BACKSTOP:** if the tape carries `# FIXTURE-RESUME … start=UNKNOWN-legacy-tape`
(`tools/overnight.sh:110`), no `# FIXTURE` line at all, or the shard is routed to a
REMOTE worker (whose tapes carry no stamp), the second clock is **the `ts` of the
FIRST COMPLETED ROW** — conservative by construction.

⚠ **The treatment tree ALREADY EXISTS and is committed** (`bots/_v487ecommit2`,
added `bac77d60`, author time `2026-08-17T09:06:36+02:00`). This document is **NOT**
locked before the arm exists, only before its first screen row. That is also what
makes Obligation 13's intersection computable at lock time.

---

## ⛔ READ BEFORE RATIFYING — EIGHT THINGS THE LANE OWNS

**1. THE CONTROL IS NOT THE HOLDER.** `bots/_v468kladturbo` is Sleipnir v1, pinned
as the corefill control at `scratchpad/CONTROL_PIN`
(`a9228ccb56ed9a65dd7d72ad1cb96068 bots/_v468kladturbo`), per Magnus's benchmark
ruling. **The LADDER holder is Odin (x3r0 v157), not Sleipnir**, so 50.0 here means
"adds nothing to the BENCHMARK"; `ODINVSSLEIP` is the converter into ladder units.

**2. THIS ARM IS A REGISTERED BRANCH BEING EXECUTED, NOT A NEW IDEA.**
`docs/prereg/PREREG-ECOMMIT-2026-08-17.md:90-95` pre-committed, before its data:
*"if the screen reads below bar, THE NAMED FIRST SUSPECT IS OVER-REFUSAL VIA THE
`long` GATE, AND THE NEXT ITERATION IS THE CONSTANT, NOT THE MECHANISM'S DEATH."*
The screen read below bar. **This tree is that constant, and nothing else** —
`diff -r bots/_v477ecommit bots/_v487ecommit2` returns exactly one hunk,
`doctrine.py:1940`, `ECOMMIT_MAX_LINK_TILES = 8` → `= 16`; `eco.py`, `main.py` and
`raid.py` are byte-identical between the two trees.

**3. ⛔ THE ONE CONSTANT MOVES TWO BUDGETS, AND "ONE BEHAVIOURAL CHANGE" WOULD BE
THE WRONG SENTENCE.** `doctrine.py:1957` reads
`ECOMMIT_ADOPT_MAX_TILES = ECOMMIT_MAX_LINK_TILES`, so the edit raises **both** the
refusal gate **and** the orphan-adoption budget, 8 → 16. That is by design
(`doctrine.py:1955-1956`: *"same budget, so the two halves cannot disagree about
what wireable means"*), and it means **no readout sentence may attribute a band to
the refusal gate alone.** ⚠ **AND THE TREE'S OWN COMMENT AT `doctrine.py:1935-1939`
STILL ARGUES FOR 8** (*"degrades WORSE than linearly past L ≈ 8 … so 8 is the knee
the corpus actually shows and not a round number"*) — **a reader of the shipped tree
gets the opposite of the shipped value.** Flagged for the builder as a cheap
pre-fire fix; it changes no behaviour and is not a reason to hold the lock.

**4. ⛔⛔ THE PARENT'S DIAGNOSIS RESTS ON A DEMO, NOT ON THE SCREEN, AND THE
CONFIRMING READ THE PARENT REGISTERED WAS NEVER RUN.** Three separate things get
conflated whenever this arm is described, and they are separated here once:
* **THE SCREEN.** `results.tsv:480-481` (`ecommit-autostop-400` /
  `ecommit-catastrophe-400`): **36.58% [32.41, 40.74] at n = 514, type
  `cancellation`**, fired 2026-08-17T06:10:26Z by `tools/auto_gate.py --apply` under
  the **CATASTROPHE** clause (*"n ≥ 400 and the 95% CI UPPER bound 40.74 < 45.0 —
  the optimistic edge of its own data is still catastrophic"*), against a registered
  n of 5,400. The row's own words: *"this arm is UNDER-POWERED by construction — no
  exclusion claim is licensed by it."* ⭐ **The FULL KEPT TAPE
  (`scratchpad/overnight/ECOMMIT.tsv`, 538 game rows, heartbeat
  `2026-08-17T06:11:09Z 538 5400 ECOMMIT RUNNING`) reads 36.80% — only +0.22pp above
  the stop share, NOT the ~+2pp the selected-pessimistic allowance would predict.**
  ⇒ **quote 36.80 at n = 538, and note that the regression allowance did not
  materialise here.**
* **THE DEMO.** *"rate up, count down, 72.4% `long`"* are **one-game-per-cell demo
  numbers**, not screen numbers: `PREREG-ECOMMIT:80-88` — rate 66.4% → 96.6%,
  connected count 79 → 57 over sixteen sides each (4.94 → 3.56 per side, −28%), on a
  lifetime harvester count of 119 → 59, and **123 of 170 deferrals (72.4%)
  reason-coded `long`**. **16 sides, 4 maps, and `eider` is NOT in the 15-map
  corefill pool** — the parent's own page says so at `:161`.
* **THE CONFIRMING READ THAT NEVER HAPPENED.** `results.tsv:481` states the
  precondition: *"The F-battery (rate+count pair) is the confirming read before any
  iteration registers."* ⛔ **IT WAS NEVER RUN FOR `_v477ecommit`.** `EC1DEFER`
  occurs in exactly three files in the repo — the NEW `scratchpad/ecommit2_fbattery.log`,
  the decoder `scratchpad/s48_eco_demo.py`, and the parent prereg. **There is no
  v477 full-pool F-battery log anywhere.**
⇒ **THE OVER-REFUSAL DIAGNOSIS THIS ARM ACTS ON IS A 16-SIDE, 4-MAP DEMO WITH ONE
OFF-POOL MAP, AND THE ITERATION IS BEING REGISTERED WITHOUT THE READ ITS OWN PARENT
NAMED AS THE PRECONDITION.** That is stated on the page rather than left for a
certifier, and it is a REASON THE BUILDER MAY LEGITIMATELY DECLINE TO FIRE THIS ARM
FIRST — the alternative is to run the F-battery on `_v477ecommit` and know which
gate bound.

**5. ⛔⛔ THE F-BATTERY IS NOT RUNNING, AND ITS THREE COMPLETED CELLS POINT THE
OPPOSITE WAY TO THE PARENT'S EXPECTATION. THIS IS THE MOST IMPORTANT LIVE FACT ON
THE PAGE.** State at draft (`ps` checked twice, 09:11:07 and 09:12:59 CEST — **0
matching processes**; `scratchpad/ecommit2_fbattery.log` frozen at 1,614 bytes,
mtime 09:06):
* **3 of 24 planned cells are done — 12.5%.** Runner `scratchpad/s48_demo_battery.sh`
  plans 4 maps × 2 seeds × 3 cells; only `yulerune` seed 11 exists. **Seed 22 never
  started; icefloe, drumlin and eider never started.**
* **The dose tags across BOTH treatment cells: 7 deferrals total — `long` = 1
  (14.3%), `bank` = 6 (85.7%), `route` = 0.** At `MAX_LINK_TILES = 8` the demo read
  123/170 = 72.4% `long`. ⇒ **the `long` gate has collapsed to a single firing and
  the BINDING CONSTRAINT HAS MOVED TO THE FUNDING GATE (`ECOMMIT_FUND_BELT`), WHICH
  THIS ITERATION DOES NOT TOUCH.** The parent's F1 expectation was *"`long` the modal
  reason"*; on these three cells it is not.
* **The count-down half of the failure signature PERSISTS at 16**, with the rate
  still up. Connected COUNT beside the rate, per the pairing rule:

| cell (yulerune seed 11) | side | harv built | **connected** | rate | by r25 | result |
|---|---|---|---|---|---|---|
| control (base vs base) | base seat A | 6 | **4** | 66.7% | 4 | winner B, r116 |
| | base seat B | 6 | **5** | 83.3% | 3 | |
| treat, arm seat A | `_v487ecommit2` A | 3 | **3** | 100.0% | 3 | **arm LOST**, r231 |
| | base B | 6 | **5** | 83.3% | 3 | |
| treat, arm seat B | base A | 10 | **7** | 70.0% | 4 | **arm LOST**, r282 |
| | `_v487ecommit2` B | 4 | **3** | 75.0% | 3 | |

⚠ **DO NOT BANK ANY OF THIS.** Two treatment games, unseeded (see #6), and both
lost. It is registered here **as a pre-lock risk, not as evidence**, and it is
exactly what a registered risk is for: **if the full battery reproduces it, the
below-bar branch of this arm's falsifier points at `ECOMMIT_FUND_BELT`, not at
another notch of `MAX_LINK_TILES`.**

**6. ⚠ THE F-BATTERY AS CURRENTLY WRITTEN HAS THREE DEFECTS AND MUST BE FIXED
BEFORE IT IS READ AS THIS ARM'S FIRINGS EVIDENCE.** All three are in
`scratchpad/s48_demo_battery.sh` / `scratchpad/s48_eco_demo.py`:
* **NOISE IS NOT FORCED OFF.** `grep -n NOISE` over both files returns **nothing**.
  Contrast `scratchpad/s48_demo.sh:30-31`, which copies the trees and `sed`s
  `NOISE_ON = True` → `False` precisely because (`:6-9`) *"the spawn salt alone moves
  the first-harvester round by ±3, which is larger than the effect."* ⇒ **the three
  existing cells are not reproducible and their cell-level noise is unbounded.**
* **`eider` IS OFF-POOL.** The default map list is `(yulerune icefloe drumlin eider)`
  (`:16`) and `eider` is not in the 15-map corefill pool. **Restarting the battery
  unchanged repeats the parent prereg's own registered defect.**
* **SEEDS ARE HARDCODED `(11 22)`** (`:17`), so the battery cannot be widened without
  editing it, and `--tle 10` arrives only as a DEFAULT of the decoder
  (`s48_eco_demo.py:50`), not as a declaration in the runner. **A default is not a
  registration** — `tools/overnight.sh` runs `--tle 10` and a battery that silently
  ran without it would measure a chassis the screen does not use.

**7. THE SHARD TAPE CANNOT SEE THE MECHANISM, SO A FIRINGS READ IS MANDATORY BEFORE
THE PRIMARY — AND ON THIS ARM THE RULE IS A HARD CLAUSE, NOT A CUSTOM.**
`tools/overnight.sh:138-139` runs every game with `--tle 10 --replay /dev/null`; the
tape's columns (written at `:104`) are `ts shard game map seed seat winner cond
turns` — **no entity, build, belt, resource or stdout information exists on it, in
either arm.** The plank's mechanism is CONDITIONAL (a reason-coded refusal gate plus
a periodic adoption scan), so `docs/prereg/BARS.tsv`'s FIRINGS-BEFORE-PRIMARY rule
binds.
> **F1, F2 and F3 are READ, and their numbers written down, BEFORE any sentence
> containing the primary share is typed.** A primary typed ahead of the firings read
> is a REGISTRATION BREACH regardless of what it says (precedent: `results.tsv:471`,
> this session, this repo).

**8. ⛔⛔ CONNECT RATE IS A MEDIATOR AND MAY NEVER DENOMINATE A BAR, A VERDICT OR A
PROMOTION — AND THE PAIRING RULE STAYS.** Carried verbatim in force from
`PREREG-ECOMMIT:62-83`: connect rate is strongly outcome-associated (within-map
slope +0.56 [0.46, 0.66] clustered on match; paired within-game 0.667 [0.62, 0.71])
**while the arrow is contaminated by reverse causation** — a losing side gets its
belt cut (2.58× belt-death asymmetry; 50.9% of conveyor deaths near live enemy
gunners). **AND THE RATE CAN RISE MECHANICALLY: refuse enough sites and the
survivors are the easy ones, so the ratio improves with zero gain and a smaller
economy.** ⇒ **CONNECT RATE AND HARVESTER COUNT ARE ONE METRIC AND ARE ALWAYS
REPORTED TOGETHER.** ⚠ **This hedge was briefly a candidate for retirement on the
strength of a measured leak-rate size; THAT SIZE DIED (see the LEAK block below), so
the hedge stands. Belt and braces until someone measures the size properly.**

---

## RATIFY: Hypothesis

**Raising the committed-route tile budget from 8 to 16 — so that the route-commitment
gate refuses fewer harvester sites and the orphan-adoption scan will take longer
chains — raises our LOCAL pooled game share against `bots/_v468kladturbo` itself to
51.33% or higher at n = 5,400 games across all 15 corefill maps and both seats.**

**Provenance:** the pre-committed branch of `docs/prereg/PREREG-ECOMMIT-2026-08-17.md:90-95`
and `results.tsv:481`, executed under Magnus's s48 cores directive (*"throw more
experiments on the cores"*).

**The mechanism claim, stated so it can be wrong** — three effects, and the
hypothesis is that the first outweighs the other two:
* **IT STOPS REFUSING SITES THAT WOULD HAVE PAID.** The `long` branch
  (`eco.py:961`, guarded by `eco.py:960` `if len(plan) > ECOMMIT_MAX_LINK_TILES:`)
  was the binding gate at 8 and refused 72.4% of the parent's demo deferrals. At 16
  the parent's economy is restored toward the base's while the route commitment
  itself is kept.
* **IT ALSO RAISES THE ADOPTION BUDGET** (`doctrine.py:1957`), so a longer orphan
  chain can be adopted rather than abandoned — the same direction, a different
  half, and **not separable from the first by this leg.**
* **⚠ AND IT RE-ADMITS THE SITES THE ORIGINAL STUDY REFUSED FOR A REASON.** A
  16-tile belt costs ~16 conveyors at 3 Ti plus **+1% permanent cost scale each**,
  and the corpus knee the parent tree still argues for is at ~8. **Buying a long
  route is a real cost in the treatment's own currency, and it is why a flat or
  negative result is informative rather than a null about route commitment.**

**⇒ A flat result is INFORMATIVE.** It would say the sites recovered and the belt
bought cancel — a different finding from "route commitment does nothing", and one
that, with the parent's 36.80 at n = 538, would locate the whole family's problem
somewhere other than the tile budget.

**PRICE, quoted per house rule via `tools/scale_trace.py --price 5` (a harvester
carries +5pp of cost scale; the gate's first mechanism is harvesters NOT built):
READING 1 (as a total, 5pp) = p0.0 SMALL; READING 2 (on top of the r100 median of
180pp, i.e. 185pp) = p53.9 ORDINARY — inside the range teams routinely carry.
READING 2 is the primary per the tool's own instruction.** ⇒ *"the scale saved by
refusing a harvester"* is **not** a large quantity by field standards, which is an
argument for admitting more sites and is registered here as part of the hypothesis
rather than discovered afterwards.

---

## ⭐ THE LEAK BLOCK — REGISTERED AS DIRECTION-ONLY, SIZE UNMEASURED

**LEAK RATE = the share of our team's ARRIVING titanium stacks that arrive at the
ENEMY.** Computed from `tools/corpus/replay_flow.py`, whose header
(`replay_flow.py:144`) is `file team band class n` and whose classes are assigned at
`:130/:132/:134/:136`: `OWN_CORE` (delivered home), `OWN_NET`, **`ENEMY_CORE`**
(*"delivered into the ENEMY core — a scored own-goal"*), **`ENEMY_NET`** (*"pushed
onto enemy conveyors"*), `GROUND`. **The metric is
`(ENEMY_NET + ENEMY_CORE) / (OWN_CORE + ENEMY_NET + ENEMY_CORE)`.**

**WHY IT IS ON THIS PAGE — TWO REASONS, BOTH STRUCTURAL:**
1. **THE MECHANISM IS DEFINITIONAL, NOT ESTIMATED.** Harvester round-robin is
   **team-blind** — `CLAUDE.md`, verbatim: *"an enemy conveyor adjacent to your
   harvester is a full-rank acceptor, so an unwired harvester beside an enemy belt
   gives ~half its output away (measured 49/49), and titanium is credited to whoever
   owns the DESTINATION core."* **An unconnected harvester CAN leak by the engine's
   own rule. That is the citation, and it is the ONLY citation this page uses for the
   mechanism.**
2. **IT IS NOT A MEDIATOR.** Unlike connect rate, a leak cannot be PRODUCED by
   winning or losing in the way belt-cutting produces connect rate — it is a direct
   titanium transfer under a documented engine rule. **And it self-catches the
   failure mode the connect-rate pair exists to catch:** a mechanically inflated
   connect rate bought by refusing sites cannot also lower a leak that was never
   there.

**⛔⛔ AND ITS SIZE IS UNMEASURED. NO EXPECTED-EFFECT SENTENCE OF ANY KIND IS
REGISTERED ON THE LEAK.** The research read that proposed a size was **retracted ~10
minutes after publication** (`docs/coordination.md:70161`, commit `d11668c3`,
2026-08-17T09:07:55+02:00): the within-game paired control read **202 of 448
discordant games = 0.4509 [0.4014, 0.5000] over 240 match-clusters — DOES NOT
EXCLUDE 0.5, i.e. at or below chance.** **What died: the +0.205 slope, the
13.2%-vs-1.3% contrast, and the ~6pp ECOMMIT benefit derived from them.**
⇒ **NONE of those numbers appears anywhere on this page, and none may appear in this
leg's readout.**
⚠ **AND THE RETRACTION'S OWN DIRECTION MATTERS: A FAILED PAIRED TEST FAILS TO
SUPPORT; IT DOES NOT REFUTE.** The paired control could not distinguish the effect
from chance at that n; it did not show the effect is absent. **That is why the metric
survives as DIRECTION-ONLY and why nothing on this page is denominated in it.**
**REGISTERED FORM: LEAK RATE is reported as a DESCRIPTIVE mechanism metric with a
DIRECTION (treatment ≤ control if the gate is doing what it claims) and NO
pre-registered size, NO bar, and NO contribution to any band.**

**⛔ AND WHERE IT CAN AND CANNOT BE READ, STATED EXPLICITLY BECAUSE IT IS THE
DIFFERENCE BETWEEN A METRIC AND A WISH: LEAK RATE NEEDS REPLAY FILES.**
`replay_flow.py:65` is `data = path.read_bytes()` and its production wiring
(`tools/corpus/sync.py:45`, `("flow.tsv", "replay_flow.py", "argv")`) runs over
`.replay26` files. **The corefill shard writes none — `tools/overnight.sh:138-139`
passes `--replay /dev/null`.**
⇒ **THE SHARD CARRIES THE SHARE; THE F-BATTERY CARRIES THE MECHANISM.** Leak rate is
read **only** from the F-battery's retained replays (F4 below), never from the
5,400-row tape, and any readout sentence that quotes a leak figure "from the shard"
is quoting something that does not exist.

---

## REGISTRATION BLOCK

**TARGET BAND: N/A — local corefill screen with ZERO rated ladder exposure: no submission, no activation, no unrated challenge, so `tools/target_value.py` has no input. Nothing on this page ends in a ship; the only branch that reaches the ladder is a later, separately-registered head-to-head against the holder.**
**PINNED: N/A — local self-play. The opponent version is fixed by construction: the control tree is `bots/_v468kladturbo` at the commit this shard runs from, pinned at `scratchpad/CONTROL_PIN` (`a9228ccb56ed9a65dd7d72ad1cb96068 bots/_v468kladturbo`). There is no opponent churn to pin against and no calibration relevance to protect.**
**SURFACE: local**
**PLANK CLASS: economic — a harvester-placement gate and an orphan-belt adoption scan. Nothing in the diff touches turrets, raiders or home defence (`raid.py` is byte-identical to the control), so the `DEFENCE_ADMISSION_BAR`'s r300 clause does not bind. D1 (ITT timely-kill rate, stated as an EXCLUSION) is read anyway, because economy is instrumental under `R1000_IS_DEFEAT` and an eco plank that slows the kill is buying the wrong currency.**
**KILL-ROUND NON-REGRESSION: ITT timely-kill rate over ALL 5,400 games (share ending `cond == core_destroyed` in our favour with `turns <= 300`), treatment vs control, scored as an EXCLUSION — the 95% CI on the difference must EXCLUDE a fall of more than 2.0pp. ITT RMST300 (mean of `min(turns,300)`, every non-kill scoring the full 300, `tools/fieldcal_read.py:239`) is read beside it on the same 5,400 rows. Median-crossing-300 is the gross backstop and the kill-win-conditioned share is a DIAGNOSTIC only — it carries a collider. This is D1/D2/D3 below, stated here in the registry's own vocabulary; economy is instrumental under `R1000_IS_DEFEAT`, so an eco plank that slows the kill is buying the wrong currency.**
**CLUSTER UNIT: none** — CLAUDE.md's enumeration PERFORMED, not asserted: (i) the **MATCH** cluster does not exist on this surface — `tools/overnight.sh` writes one TSV row per `fcode run`, so 1 row = 1 game and no row shares a match with another; (ii) the **OPPONENT** cluster is degenerate — every one of the 5,400 rows plays the identical control tree, so the pooled stratum holds exactly one opponent and there is no between-opponent variation for a design effect to describe. Both clusters die ⇒ DEFF = the measured local constant **0.98** (pair-weighted, ρ = −0.020, 124 shards, s39 audit); naive intervals are correct and marginally conservative. **The platform constants (1.529 rated / 1.833 unrated) are NOT applicable.** ⚠ **The s42 cross-host rider is registered: this is a WITHIN-HOST cell and nothing on this page pools across hosts. A remote replication, if stocked, is REPORTED SEPARATELY and NEVER POOLED (the GUNAXABL/SENTTHR precedent).**
**ESTIMATOR: unweighted pooled treatment game share** = (rows with `winner == T`) / (completed rows), over all 5,400 rows, both seats pooled, all 15 maps pooled, no reweighting. Interval by `tools/cluster_ci.py` with the local constant. Seat A and seat B shares are reported SEPARATELY as a fixture diagnostic and are never the bar — seat is worth ~6.8pp on byte-identical arms, which is why the n is a multiple of 30.
**DOSE: reason-coded harvester-site refusals per side — treatment 3.5/side vs flag-off control 0.0/side (n=2 treatment sides and 4 control sides; 7 deferrals split `long` 1 / `bank` 6 / `route` 0, plus 5 adoptions, `scratchpad/ecommit2_fbattery.log`, yulerune seed 11 only). The control's zero is STRUCTURAL, not measured at lock: `_ecommit_why` occurs 0 times in all four source files of the control tree, so it has no gate that could refuse anything. ⛔ THE ONLY MEASUREMENT THAT EXISTS FOR THIS TREE AT LOCK IS 3 OF 24 F-BATTERY CELLS ON ONE MAP AND ONE SEED, AND IT READS 7 DEFERRALS TOTAL — `long` 1, `bank` 6, `route` 0 — i.e. the `long` gate this iteration exists to relax has ALREADY collapsed to a single firing and the modal reason has moved to `bank`, a gate this iteration does not touch. THAT IS A FIRING DEMONSTRATION ON TWO GAMES WITH UNSEEDED NOISE AND IT IS NOT AN EFFECT SIZE. The registered F1 battery below is what converts it into a measured dose; until it runs, the dose for this arm is UNMEASURED on the pool the screen plays.**
**PLANNED n: 5400 games** (= 15 maps × 2 seats × 180, so map and seat balance is exact; `tools/overnight.sh:68` has carried the 15-map pool since the 2026-08-13 rotation and the runner's own comment requires multiples of 30).
**BOUNDARY: 5400 games** — LOCAL surface, one tape row is one game; there is no accept/attempt distinction on this fixture. ⛔ **A LINE COUNT IS NOT A ROW COUNT**: this tape carries an unprefixed column header (`tools/overnight.sh:104`), and a naive `wc -l` / `awk '!/^#/'` over-reports n by exactly one (measured on KLADLADDER, `results.tsv:474`; the row-count rule is `tools/overnight.sh:118-120`). The registered denominator is **DictReader row count, cross-checked against the heartbeat and against `max(game id) + 1`.**
**CUT-SHORT: floor 2700 games.** Below 2,700 completed tape rows this leg publishes descriptive tallies (share, per-seat, per-map, kill-clock) and takes **NO comparative look and no bar verdict**; the half-width at 2,700 is ±1.87pp, already wider than the 1.33pp margin the bar is built on. An `auto_gate` cancellation at CATASTROPHE@400, MARK-1000 or TREND-FLOOR@1000 is an **OPERATIONAL STOP, not a verdict**, typed `cancellation`. ⭐ **ONE CARVE-OUT, PRE-COMMITTED, AND THE PARENT USED IT:** a CATASTROPHE-clause cancellation (95% CI upper < 45.0 at n ≥ 400) is arithmetically INCOMPATIBLE with every band above Band 4, so a stop under that clause DOES license the Band-4 sentence at the partial n — **provided F1/F2 have been read first**, and provided the partial share is disclosed as **selected-pessimistic**. ⭐ **AND A LESSON FROM THE PARENT IS PRE-COMMITTED HERE: THE READOUT QUOTES THE FULL KEPT TAPE, NOT THE MARK.** ECOMMIT stopped on 514 rows and its full tape carries 538 (36.58 → 36.80); the difference was small, but the mark is the SELECTED number and the tape is the arm's.
**BAR: 51.33. MDE: 0.00pp — THIS IS A POINT RULE ONLY AND LICENSES NO EXCLUSION CLAIM ABOUT AN EFFECT SIZE.** Per the OB16 corollary (obligations doc, 2026-08-15T03:52:45Z): the standard corefill band IS `50 ± half_width` at n=5,400, so clearing 51.33 puts the CI's lower edge at exactly 50.00 — it excludes 50 and excludes **no positive effect size whatsoever**. n for the exclusion it CAN make (bar ≠ 50.0): **5,400**, the planned n. **That is a deliberate choice: the question is *does raising the budget move anything at all against the incumbent*, which is exactly what a point rule is the right instrument for.**
**BASE RATE: 50.00**
**BAR SOURCE:** house-standard corefill futility band, `50 + 1.96*sqrt(.25/5400) = 51.33pp`, local DEFF 0.98 so naive — the identical bar carried by `docs/prereg/BARS.tsv` rows `SEALFLOOR6`, `SENTTHR`, `KLADTKILL`, `KLADTK2`, `KLADTURBOR`, `DRAINTURBO`, `KLADLADDER`, `SEALSENTAN`, `SEALSENTA` and `ECOMMIT` — the last of which is this arm's own parent, which keeps the pair numerically comparable. **Constructed, not observed.**
**BASE RATE SOURCE:** structural A/A expectation of a seat-balanced, map-balanced self-play fixture whose control tree is the treatment's own base. Empirically calibrated by `IDNULL140` — **49.27% [47.94, 50.60] at n = 5,400**, 2026-08-16T18:02:04Z, same fixture (`results.tsv:454`, type `cert`) — and by `NULL125` — **51.04% at n = 5,400** (`results.tsv:346`, type `verdict`; ⚠ that row's share FIELD reads `0.510` with EMPTY CI columns while its prose reads 51.04% — the prose is the citation and the row is not a source of an interval). Two A/A cells, one either side of 50.0. ⇒ **a bare clearance in [51.33, 52.4] is a band an A/A cell has already produced**, which is why Band 2 is pre-registered as WEAK.
**POOL ERA: post-2026-08-13-rotation** — the 15-map local pool of `tools/overnight.sh:68` (`antler archipelago auroraveil drakkarfjord drumlin fjordgate frostgate glacierkeep icefloe midgard nordkap ragnarok royale valkyrie yulerune`). (`check_pool_era` treats this as n/a on a LOCAL surface per SPEC §6; declared anyway so the population is on the page.) ⚠ **AND IT IS NOT COSMETIC: `eider`, one of the four maps in BOTH the parent's demo and this arm's F-battery default, IS NOT IN THE POOL.** The parent's page registered that defect and its F-battery was to repair it; that battery never ran. **F1 here must pass the 15-map list explicitly or it silently falls back to the off-pool default.**
**REFERENCE n: none** — the comparator is generated inside this same shard from the same 5,400 seeds; there is no fixed external reference sample, so no resolution floor at n→∞. **(The parent's 36.80 at n = 538 is a descriptive prior, not a reference sample, and it is a CANCELLATION.)**
**TREATMENT TREE: bots/_v487ecommit2**
**TREATMENT DIFF REFS: bac77d60^ bac77d60**
**MECHANISM METRIC READS: bots/_v487ecommit2/eco.py:961 — `return "long"`, the binding branch of the reason-coded gate `_ecommit_why` (`eco.py:908`, body `:944-970`), guarded one line above at `eco.py:960` by `if len(plan) > ECOMMIT_MAX_LINK_TILES:` — the single comparison the manipulated constant feeds. Observed as F1 via the `EC1DEFER … why=` tag printed at `eco.py:977-978` (guarded by `if LOKI_ECOMMIT_LOG:` at `:976`) and the `EC1ADOPT` tag at `eco.py:1045-1046` (guarded at `:1044`), decoded by `scratchpad/s48_eco_demo.py` out of the LOCAL replay's `BotOutput.stdout` — populated locally, stripped only on platform-downloaded replays. The gate has exactly ONE call site, `eco.py:1910`, inside the harvester-placement loop; `_adopt_orphan` (`eco.py:980`) has exactly one, `eco.py:2028`. TREATMENT DIFF TOUCHES: bots/_v487ecommit2/doctrine.py bots/_v487ecommit2/eco.py bots/_v487ecommit2/main.py. INTERSECTION: yes — `_ecommit_why`, `LOKI_ECOMMIT_ON` and `_adopt_orphan` each occur **0 times in EVERY one of the four source files of `bots/_v468kladturbo`** (verified at draft, per file), so the control has no gate to refuse anything and the metric cannot read identically in both arms.**
⚠ **DIFF-REFS DISCLOSURE:** `bac77d60` ADDS the whole tree, so `git diff --name-only bac77d60^ bac77d60` returns FOUR paths including `raid.py`. The SEMANTIC diff against the control is THREE files: `diff -rq bots/_v468kladturbo bots/_v487ecommit2` names `doctrine.py`, `eco.py`, `main.py`, and **`raid.py` is byte-identical to the control.** `TREATMENT DIFF TOUCHES` declares the semantic three. **Against the SIBLING `bots/_v477ecommit` the diff is ONE LINE, `doctrine.py:1940`.**
**METRIC WINDOW: r0-r1000. GATING CONSTANTS: ECOMMIT_MAX_LINK_TILES=16, ECOMMIT_ADOPT_MAX_TILES=16, ECOMMIT_BAN_RNDS=40, ECOMMIT_ADOPT_EVERY=6. MECHANISM CAN OCCUR IN WINDOW: yes** — **there is NO round floor anywhere in this plank.** `ECOMMIT_MAX_LINK_TILES` and `ECOMMIT_ADOPT_MAX_TILES` are TILE budgets; `ECOMMIT_BAN_RNDS` and `ECOMMIT_ADOPT_EVERY` are DURATIONS (how long a deferral ban lasts, how often the adoption scan re-arms), not thresholds a round must exceed. The gate is consulted on the first harvester placement of the game and the ban lapses after 40 rounds while the scan re-arms every 6, so both halves can fire at any round.
⚠ **DISCLOSED, because a green tool run with warnings under it is how a warning stops being read: `prereg_check.py` will emit FOUR `OBLIGATION 17, PARTIAL WINDOW` warns against the line above and ALL FOUR ARE ARTEFACTS OF THE CHECKER.** `check_metric_window` reads every declared integer as a ROUND, so a tile budget of 16 is reported as "rounds r0-r15 cannot contain the mechanism". The constants are declared anyway because they are the gates that actually bind, and an undeclared gate is the failure the obligation exists for.
**PRE-STATE: the predicted-change set is NOT already in the target state at lock.** Verified at draft against the control tree: `_ecommit_why`, `LOKI_ECOMMIT_ON` and `_adopt_orphan` → **0 in `doctrine.py`, `eco.py`, `main.py` and `raid.py`**, and the string `ECOMMIT` occurs 0 times in every one of the four. The control performs **no** route check of any kind before placing a harvester, has no ore-tile deferral ban, and has no orphan-chain adoption. ⚠ **AND THE ITERATION'S OWN CLAIM IS NOT PRE-SATISFIED EITHER**: the parent shipped the same code at budget 8 and read 36.80; the budget-16 behaviour is genuinely new and Bands 3 and 4 are live, pre-named outcomes.
**MAP SEGMENT: none expected — and the reason is that I CANNOT SIGN one, which under Obligation 15a is a reason to declare none rather than to declare an unfalsifiable segment.** The gate is keyed on ROUTE LENGTH, so it fires most on large-area maps with spread ore (the five 900-area maps). **But raising the budget cuts BOTH ways on exactly that geometry**: the same maps that produced the most `long` refusals (the cost this iteration repairs) are the maps where a newly-admitted 16-tile belt is most expensive to build and most exposed to being cut. **A segment declared without a predicted sign "confirms" the mechanism whichever way it lands, which is what 15a forbids.** Per-size-class shares WILL be printed at readout as **DESCRIPTIVE** material feeding F3, **not to rescue a failed pooled primary. No map cut may rescue this arm**, and nothing may be banked off those shares without a fresh prereg. **This is the parent prereg's own declaration, carried forward unchanged because the iteration does not change the reasoning.**
**CELL VERSION CHURN: N/A — not a panel, no `CELLS:` line, one fixed local control tree.**
**GATE RESOLUTION: the shard is governed by the pinned `tools/auto_gate.py` marks — CATASTROPHE@400 (STOP if the 95% CI upper < 45.0, `auto_gate.py:236`), MARK-1000 (STOP if the CI upper < the registered BAR 51.33), TREND-FLOOR@1000 (STOP if the first-1,000 prefix share < 52.0, `auto_gate.py:250` — RAISED from 51.0 by Magnus 2026-08-16), and the same floors again at MARK-2700 (`auto_gate.py:233-236`). Their firings are OPERATIONAL CANCELLATIONS that free a core — typed `cancellation`, never `verdict`, licensing NO exclusion claim (with the single CATASTROPHE carve-out in CUT-SHORT). ⭐ The remote report-only limitation at `auto_gate.py:113` is DEAD since `a50f27ef` (`tools/remote_cancel.py` gives `--apply` a guarded remote stop path), so the floors bind on ws1/ws2 too; a remote route switches the second clock to the registered first-completed-row backstop. ⚠ **CATASTROPHE@400 IS THE CLAUSE THAT FIRED ON THE PARENT AND IS THE MOST LIKELY OUTCOME HERE TOO — the readout must not present a second catastrophe stop as a stronger result than the first merely because it is a repeat.** The RESOLVABLE gate this document owns is the primary at full n, whose margin (1.33pp) exceeds its own half-width (±1.32pp) by 0.01pp — resolvable, and only just. Everything else on this page (F1-F4, D1-D3, the seat and map splits) is DIAGNOSTIC and cannot rescue a failed primary. Any branch that does not resolve is UNRESOLVED, and an UNRESOLVED gate defaults to the RESTRICTION: no promotion, no ship conversation, no combination claim.**

---

## FALSIFIER

**PRIMARY FALSIFIER: at n = 5,400 the 95% CI UPPER bound on the treatment's pooled
game share falls BELOW 51.33.** That excludes the bar and says raising the tile
budget does NOT rescue route commitment on this fixture.
**Consequence, registered in advance and BRANCHED THREE WAYS, because the branches
license different next moves and the third is new to this iteration:**
* **If F1 shows `long` refusals collapsed AND `bank` is the modal reason** (which is
  what the three existing F-battery cells show — 1 `long` vs 6 `bank`), then **the
  binding constraint has MOVED to the funding gate `ECOMMIT_FUND_BELT`, which this
  iteration did not touch.** The road stays open but the next arm is a DIFFERENT
  constant — **one arm, one constant, its own prereg** — and `MAX_LINK_TILES` is
  retired as the suspect.
* **If F1 shows `long` STILL modal at budget 16**, the gate is still over-refusing
  and the constant is still the suspect; **but a THIRD notch is not automatic** — a
  monotone search over one integer against a 1.33pp bar is a search for noise, and
  the successor must be a mechanism change (the `long` refusal converted from a veto
  into a preference), not 24.
* **If F1 shows refusals at or near zero on the 15-map pool**, the mechanism never
  bound in the screen fixture and **the road closes without a further constant
  retry** — a tuning pass on a gate that did not bind is the cheapest kind of null
  this repo buys.

**MECHANISM FALSIFIER (independent of the primary, and it can fire first):** if F1
shows the treatment's reason-coded refusals per side within noise of zero on the
15-map pool — i.e. the dose does not reproduce on the maps the screen plays — then
the plank did not deliver its dose and **the primary is uninterpretable in either
direction**: a flat share would mean "the gate never fired", not "the gate fired and
did not pay". Per FIRINGS-BEFORE-PRIMARY this is read BEFORE the primary is typed,
and if it fires the primary is reported as **NOT MEASURED**, not as a null.

---

## READING, PRE-COMMITTED — four bands, written before the data

Registered now so no band is chosen after the fact. **Read TOP-DOWN; the first row
whose condition holds is the reading. The rows are disjoint by construction.**

| # | band at n = 5,400 | pre-committed reading |
|---|---|---|
| **1** | **CI lower ≥ 51.33** | **THE BUDGET WAS THE PROBLEM AND ROUTE COMMITMENT ADDS.** Real and resolved on this fixture. Promotes to a combination input and to a separately-registered head-to-head against the live holder. **Report the harvester COUNT alongside the share** — a win bought while the economy shrank is a different plank from a win bought while it grew, and the pair is what says which. ⛔ Attribution capped by #3: this credits the refusal gate AND the adoption budget together. ⚠ OB16: MDE 0, so this branch may claim "we can exclude 50" and may NOT claim any minimum effect size. |
| **2** | **point ≥ 51.33 but CI lower < 51.33** | **REAL-BUT-SMALL, COMBINATION INPUT ONLY.** Registered in advance as WEAK: `NULL125`'s byte-identical A/A read 51.04, so a bare clearance in [51.33, 52.4] is not distinguishable from fixture noise by this leg alone. Rows KEPT; no ship conversation; a replication on fresh seeds is the price of promotion. |
| **3** | **point < 51.33 AND CI contains 50.0** | **THE BUDGET WAS ONE OF THE PROBLEMS AND IT WAS NOT THE ONLY ONE.** Moving 36.80 (parent, n=538, cancellation) to parity would be a large recovery and a real finding about the constant — **but the arm still adds nothing to the benchmark**, and the F1 split says where to look next (see the three falsifier branches). Combination input only. |
| **4** | **CI upper < 50.0** | **THE FAMILY'S PROBLEM IS NOT THE TILE BUDGET.** Route commitment subtracts at 8 AND at 16; the gate itself, not its threshold, is the cost. ⛔ **Do NOT try a third notch.** The registered successors are (a) the funding gate `ECOMMIT_FUND_BELT`, or (b) converting the refusal from a veto into a preference — each its own arm, its own constant, its own prereg. |

⚠ **50.0 IS NOT A FLOOR AND A NEGATIVE IS A LIVE, PRE-NAMED OUTCOME.** The parent
read 36.80 on this fixture and `KLADLADDER` read 41.86 — **this fixture returns
large negatives on arms whose demos were clean.** It is named here so a negative is
not explained away as noise, and so the constant-iteration branches are
pre-registered responses rather than rescues.

---

## MECHANISM DIAGNOSTICS TO READ AT READOUT

**Measurability is declared per metric. `NOT MEASURABLE` is written where it is
true, rather than a metric being quietly renamed into something the tape carries.**

### ⛔ ORDERING, REGISTERED AS A HARD SEQUENCE
**F1, F2 and F3 run and are written down BEFORE any sentence containing the primary
share is typed.** See READ-BEFORE-RATIFYING #7.

### F1-F4 — the FIRINGS read. MEASURABLE, but NOT off the shard tape.
**EXECUTING TOOL, named per Obligation 17: `zsh scratchpad/s48_demo_battery.sh
_v487ecommit2 antler archipelago auroraveil drakkarfjord drumlin fjordgate frostgate
glacierkeep icefloe midgard nordkap ragnarok royale valkyrie yulerune`, decoded by
`scratchpad/s48_eco_demo.py`.**
**REGISTERED SIZE: 15 maps × 2 seeds × 3 cells (control base-vs-base, arm seat A, arm
seat B) = 90 cells, i.e. 60 treatment sides + 60 control sides.** Run BEFORE the
primary is typed.
**OB17 checks, run at draft, and THE THREE THAT COULD STILL SURPRISE ARE NAMED
FIRST:**
1. ⛔ **THE BATTERY IS NOT RUNNING AND IS 3 OF 24 CELLS DONE** (see
   READ-BEFORE-RATIFYING #5). **Anyone who believes this leg's firings evidence
   exists is wrong; it has to be started.**
2. ⛔ **THE RUNNER DOES NOT FORCE `NOISE_ON = False`** (`grep -n NOISE` over
   `s48_demo_battery.sh` and `s48_eco_demo.py` → nothing), while
   `scratchpad/s48_demo.sh:30-31` does exactly that for the stated reason that the
   spawn salt moves the first-harvester round by ±3, *"larger than the effect"*. ⇒
   **the battery must either force it off or its cells are single unseeded draws and
   must be reported as such.**
3. ⛔ **`--tle 10` ARRIVES ONLY AS A DECODER DEFAULT** (`s48_eco_demo.py:50`), not as
   a runner declaration. It currently matches the shard's `--tle 10`
   (`tools/overnight.sh:138-139`) — **but a default is not a registration, and a
   firings battery run without the limit would measure a chassis the screen does not
   use** (`tools/overnight.sh` documents `_v145bestfit` winning 6/6 with the limit
   off and losing 5/6 with it on). **Assert the flag at read time.**
4. *Name the executing tool* — done above. *Confirm the pool override path exists* —
   `s48_demo_battery.sh:16` is `if (( $# )); then MAPS=($@); else MAPS=(yulerune
   icefloe drumlin eider); fi`, so the override IS a path the script has.
5. *Consequence of silent non-execution* — **if the map list is omitted the script
   silently falls back to its four-map default, one of which (`eider`) is OFF-POOL —
   the exact defect this battery exists to replace — and nothing in the output would
   say so.** ⇒ **the readout must print the map list it actually ran.**

* **F1 — DOSE DELIVERY ON THE POOL THE SCREEN PLAYS.** Reason-coded `EC1DEFER`
  refusals per side, split `route` / `long` / `bank`, and `EC1ADOPT` adoptions per
  side, per map. **Pre-registered expectation: refusals per side > 0 on a majority of
  the 15 pool maps.** ⛔ **THE PARENT'S EXPECTATION THAT `long` IS MODAL IS
  DELIBERATELY NOT CARRIED FORWARD — at budget 16 it is expected to be a MINORITY
  reason, and the registered read is the SPLIT, not a modal claim.** ⚠ **Decoder
  limitation, disclosed: `s48_eco_demo.py:303-304` prints dose tags per GAME, pooled
  across BOTH teams, with no per-seat split** — so a per-side refusal figure requires
  either a decoder change or the (safe) observation that the control emits no `EC1`
  tags at all, which makes the pooled count attributable to the arm. **Say which one
  was used.**
* **F2 — THE PAIR: connect RATE and harvester COUNT, reported together, never
  apart.** Per side: harvesters built (lifetime AND by r25), harvesters ever
  structurally connected, and the ratio. **Pre-registered expectation: rate UP
  relative to control; the COUNT is the open question and is the number the rate
  hides.** Parent demo anchor, reported as an ANECDOTE and NOT as an expected
  effect: rate 66.4% → 96.6%, connected count 4.94 → 3.56 per side, lifetime 7.44 →
  3.69 per side (16 sides, 4 maps, one off-pool).
* **F3 — OVER-REFUSAL BY MAP SIZE CLASS.** F1's split and F2's pair, by
  `small` / `mid` / `900-area`. **DESCRIPTIVE ONLY** — it tells the successor arm
  which gate to move, and it is explicitly NOT a segment and cannot rescue the
  primary (see `MAP SEGMENT`).
* **F4 — LEAK RATE. DIRECTION ONLY, SIZE UNMEASURED, NO BAR.** Off the F-battery's
  **retained replays** (the runner keeps them at `/tmp/s48_{ctl,trA,trB}_<map>_<seed>.replay26`),
  via `tools/corpus/replay_flow.py`:
  `leak = (ENEMY_NET + ENEMY_CORE) / (OWN_CORE + ENEMY_NET + ENEMY_CORE)` per side.
  **DIRECTION: treatment ≤ control if the route gate is doing what it claims.**
  ⛔ **NO SIZE IS PRE-REGISTERED AND NONE MAY BE INFERRED** — see THE LEAK BLOCK
  above; the measured slope was retracted and the within-game paired control
  (202/448 = 0.4509 [0.4014, 0.5000], 240 clusters) FAILS TO SUPPORT rather than
  refutes. **F4 contributes to no band, no bar and no verdict.** Its declared job is
  to catch the mechanically-inflated-rate failure mode from a direction the connect
  rate cannot: an arm that raised its rate purely by refusing sites has not removed a
  leak that was never there. ⛔ **F4 IS NOT READABLE FROM THE SHARD** — `--replay
  /dev/null` — **and any leak number attributed to the 5,400-row tape is fabricated.**

### D1-D3 — the kill-clock read. MEASURABLE, shard-native (`cond`, `turns`, `winner`).
* **D1 — TIMELY-KILL RATE (the `DEFENCE_ADMISSION_BAR` primary), ITT.** Share of ALL
  treatment-seat games ending `cond == core_destroyed` in our favour with
  `turns ≤ 300`, treatment vs control, both on the same 5,400 rows.
  **Non-regression is the bar and it is stated as an EXCLUSION, per CLAUDE.md's
  fail-to-exclude clause: the 95% CI on the difference must EXCLUDE a fall of more
  than 2.0pp.** A "no significant rise" phrasing is not admissible.
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
* **Titanium actually DELIVERED (`titanium_collected`).** The shard tape carries no
  resource column and its replays are discarded; the economy is observed only through
  harvester and belt structure in the F-battery (plus F4's leak direction). **Under
  `R1000_IS_DEFEAT` this is the correct thing to be blind to** — delivery is
  instrumental — but the blindness is stated rather than glossed.
* **Cost scale at any round.** The saving the gate's first mechanism buys (+5% per
  harvester not built) is **NOT READABLE** on either surface. It is inferable from
  F2's count and is not measured.
* **Which half carries the effect — the REFUSAL GATE or the ADOPTION BUDGET.** One
  constant moves both (`doctrine.py:1957`). Separating them needs an arm using
  `ECOMMIT_ADOPT_ON`, which the tree already exposes; it is NOT attempted here and
  **no readout sentence may attribute the result to one half.**
* **Per-unit CPU.** Local replays zero-fill `execTimeUs` (the s42 D33 instance:
  `tle_census.py` returns 0 across 1,649 local builder-turns while reading 8,847 µs on
  platform replays), so **no CPU claim is available from this leg.** ⚠ **Disclosed:
  `LOKI_ECOMMIT_LOG = True` (`doctrine.py:1962`) in the fired tree adds two `print()`
  sites the control does not have.** The base already ships `LOKI_L4_LOG` and
  `LOKI_SAMESTOP_LOG` at True, so this is in-house precedent and the cost is small —
  but it is an unmatched per-turn cost in the TREATMENT'S direction (against it) under
  `--tle 10`, and it is named here rather than discovered later. (The constant's own
  comment at `:1958-1961` correctly notes it is a LOCAL instrument only — platform
  replays strip stdout, 30,664 of 30,664.)
* **Seed determinism.** `NOISE_ON` pins an unseeded per-unit salt, so base-vs-base at
  one seed diverges at round 0. **No seed-matched or replay-diff equivalence claim is
  available on the SHARD fixture.** ⭐ **The flag-off equivalence claim is inherited
  from the parent's separate harness — `scratchpad/s48_flagoff.sh`, `--tle 0` +
  `NOISE_ON=False`, which drove BOTH verdicts (`LOKI_ECOMMIT_ON=False` → replay
  SHA-256 identical to the base in sixteen of sixteen cells; flag ON → differs in
  sixteen of sixteen), and it is made ON THE CODE, never on shard rows.** ⚠ **THAT
  EVIDENCE IS THE PARENT'S, NOT THIS TREE'S.** It transfers only because this tree is
  byte-identical to `bots/_v477ecommit` apart from one integer in `doctrine.py`
  (`diff -r`, verified at draft) — **and that argument is the registration; no new
  flag-off run is claimed for `_v487ecommit2`.**

---

## THE CHANGE — `file:line`, control → treatment

**TREATMENT TREE: `bots/_v487ecommit2`** — byte-for-byte `bots/_v477ecommit` apart
from ONE integer, and byte-for-byte `bots/_v468kladturbo` apart from three files.
Verified at draft: `diff -r bots/_v477ecommit bots/_v487ecommit2` → one hunk;
`diff -rq bots/_v468kladturbo bots/_v487ecommit2` → `doctrine.py`, `eco.py`,
`main.py`, with **`raid.py` byte-identical to the control.**

1. ⭐ **`doctrine.py:1940` — `ECOMMIT_MAX_LINK_TILES = 8` → `= 16`. THIS IS THE
   ONLY DIFFERENCE FROM `bots/_v477ecommit` AND IT IS THE ARM.** It propagates to
   `ECOMMIT_ADOPT_MAX_TILES` at `:1957` by assignment. ⚠ The comment block at
   `:1935-1939` still argues for 8.
2. **`doctrine.py:1881-1962`** — the LOKI-ECOMMIT block and eight constants:
   `LOKI_ECOMMIT_ON = True` (`:1934`), `ECOMMIT_MAX_LINK_TILES = 16` (`:1940`),
   `ECOMMIT_FUND_BELT = True` (`:1944`), `ECOMMIT_BAN_RNDS = 40` (`:1948`),
   `ECOMMIT_ADOPT_ON = True` (`:1950`), `ECOMMIT_ADOPT_EVERY = 6` (`:1954`),
   `ECOMMIT_ADOPT_MAX_TILES = ECOMMIT_MAX_LINK_TILES` (`:1957`),
   `LOKI_ECOMMIT_LOG = True` (`:1962`).
3. **`main.py`** — two per-unit fields, `self.ecommit_ban = {}` and
   `self.adopt_next = -1`. No store slot.
4. **`eco.py:852-1046`** — six methods: `_ecommit_banned` (`:852-867`),
   `_ecommit_route`, `_ecommit_unpaid`, **`_ecommit_why` (`:908`, body `:944-970` —
   `route` at `:959`, **`long` at `:961` guarded by `:960`**, `bank` at `:969`, with
   every exception path ADMITTING the build)**, `_ecommit_defer` (`:972`, its
   `EC1DEFER` print at `:977-978`), and `_adopt_orphan` (`:980`, its `EC1ADOPT` print
   at `:1045-1046`).
5. **`eco.py:1910` and `eco.py:2028`** — the gate's single call site (inside the
   harvester-placement loop: `if ok and LOKI_ECOMMIT_ON:` at `:1902` → `why = …` at
   `:1910` → `self._ecommit_defer(…); continue` at `:1911-1913` → `ct.build_harvester(bp)`
   at `:1914-1915`) and the adoption scan's single call site (gated
   `if not self.link_queue:` at `:2027`).

**THE GATE READS AN EXISTING CACHE, NOT A NEW ROUTER:** `_ecommit_route` asks
`_samestop_plan`, the same per-ore-tile cache the stop-tile preference already fills
one branch later in the same turn. A site in the core ring or with a live acceptor
beside it is admitted with no flood at all.

---

## WHAT THIS LEG COSTS AND WHAT IT DOES NOT

**Cost: one core to n = 5,400, plus ~90 local games for the F-battery.** ZERO rated
ladder exposure, zero submissions, zero unrated challenges — nothing on this page
touches the platform, which is why `TARGET BAND` is N/A.

**It does NOT decide a ship.** The strongest branch promotes the arm to (a) a
combination input and (b) a separately-registered head-to-head against the live
holder — Magnus's procedure verbatim (*"we start by testing it against the current
slot, If it beats it we can switch"*), templated by `SLEIPH2H`. **Gate-1-to-gate-2
transitivity is UNVALIDATED in this repo (QUEUE #65: 3 concordant, 1 not)**, and the
benchmark is not the holder, so `ODINVSSLEIP` is the converter into ladder units.

⚠ **AND THE HONEST STATEMENT OF WHAT THIS ARM IS: it is the second point on a
one-constant sweep whose FIRST point died at 36.80, registered without the
confirming read its own parent named as the precondition, on a fixture that has
returned two large negatives today.** That is a legitimate iteration under the mill
— *"a null is an iteration, not a failure"* — and it is also a legitimate thing for
the builder to reorder behind an F-battery run on `_v477ecommit`. **The choice is
the builder's; the information needed to make it is on this page.**

---

**PROVENANCE:** `docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md` (read in full: OB1, OB7, OB12, OB13, OB14, OB15a/b/c, OB16 + its corollary and cross-host rider, OB17 + its rider) · `docs/prereg/PREREG-ECOMMIT-2026-08-17.md` (this arm's parent; read in full, including its registered over-refusal branch at `:90-95`, its mediator clause at `:62-83`, its off-pool disclosure at `:161` and its F1-F3 spec at `:257-274`) · `docs/prereg/PREREG-SEALSENTAN-2026-08-17.md` (today's house style) · `docs/prereg/BARS.tsv` (header, the FIRINGS-BEFORE-PRIMARY rule, the `ECOMMIT` row) · `CLAUDE.md` (the benchmark ruling, `R1000_IS_DEFEAT`, the DEFF scope procedure, and the **team-blind harvester round-robin fact measured 49/49** — the ONLY citation used for the leak mechanism) · `tools/prereg_check.py` (`RULES`, `DEFF`, `check_metric_window`, `check_pool_era`) · `tools/auto_gate.py:113,233-236,250` · `tools/overnight.sh:68` (the 15-map pool), `:99,103,110` (the FIXTURE stamp — confirmed live on `scratchpad/overnight/ECOMMIT.tsv` line 1: `# FIXTURE shard=ECOMMIT treatment=bots/_v477ecommit control=bots/_v468kladturbo planned_n=5400 workers=8 host=MacBook-Pro start=2026-08-17T05:55:06Z runner=tools/overnight.sh`), `:104` (the tape column header), `:118-120` (the row-count rule), `:138-139` (`--tle 10 --replay /dev/null`) · `tools/corpus/replay_flow.py:65,130-136,144` and `tools/corpus/sync.py:34,45` (the leak instrument and its replay dependency) · `tools/cluster_ci.py` · `tools/fieldcal_read.py:239` · `tools/scale_trace.py --price 5` (run at draft; READING 2 = p53.9 ORDINARY) · `bots/_v487ecommit2/{doctrine,eco,main}.py` · `bots/_v477ecommit/doctrine.py` · `bots/_v468kladturbo/{doctrine,eco,main,raid}.py` · `scratchpad/s48_demo_battery.sh:11,15,16,17,22-30` · `scratchpad/s48_eco_demo.py:50,52,250,303-304` · `scratchpad/s48_flagoff.sh` (the parent's flag-off harness) · `scratchpad/ecommit2_fbattery.log` (read in full at draft; 3 of 24 cells, frozen 09:06, process absent) · `scratchpad/overnight/ECOMMIT.tsv` (538 data rows) · git commits `bac77d60`, `d67eb98e`, `d11668c3`, and `git diff --name-only bac77d60^ bac77d60`, `diff -r bots/_v477ecommit bots/_v487ecommit2` · `docs/coordination.md:70102-70112` (the per-team leak table that SURVIVES) and `:70161`,`:70191` (**the retraction of the slope, the 13.2%-vs-1.3% contrast and the ~6pp ECOMMIT estimate; within-game paired control 202/448 = 0.4509 [0.4014, 0.5000], 240 match-clusters**) · `scratchpad/corefill_work.txt` · `scratchpad/CONTROL_PIN` · `results.tsv` (rows 346 `null125-final`, 454 `idnull140-cert-5400`, 466 `kladturbo-local-confirm-5400`, 471 the FIRINGS-BEFORE-PRIMARY precedent, 474 `kladladder-n-final-correction`, 480-481 the two `ecommit-*` cancellation rows) · the drafting brief supplied by the builder lane s48 and its mid-task leak correction. No file under `bots/`, `tools/`, `scratchpad/`, `docs/prereg/BARS.tsv`, `results.tsv`, `HANDOVER.md`, `PROGRAMME.md` or `QUEUE.md` was created or modified by this agent, and no game was run.
