# SCREEN PREREG — `SEALPIERCE`: the seat Sentinel shoots PAST the core it sits on

Drafted by a fresh opus subagent with no inherited session context beyond the
inputs listed under `PROVENANCE`. The builder lane ratifies the judgment lines
and types the lock commit; this agent wrote no code under `bots/`, appended no
worklist row, appended no `BARS.tsv` row, fired no game, started no shard, and
touched neither `results.tsv` nor `HANDOVER.md` nor `PROGRAMME.md` nor
`QUEUE.md`.

**STATUS: committed BEFORE the `SEALPIERCE` row is appended to
`scratchpad/corefill_work.txt`, BEFORE any file named
`scratchpad/overnight/SEALPIERCE.*` exists, and BEFORE the leg's first game.**
Drafting session wall clock at write time **`2026-08-17T07:12:01Z`** (`date -u`,
same shell call); repo HEAD at draft `12e71962` (author time
`2026-08-17T09:10:53+02:00`). Verified at draft:
`grep -c 'SEALPIERCE' scratchpad/corefill_work.txt` → **0**; same grep on
`docs/prereg/BARS.tsv` → **0**; `ls scratchpad/overnight/ | grep -i sealpierce`
→ **empty**; `grep -cE '832000' scratchpad/corefill_work.txt` → **0** (the seed
base is free; the highest local seedbase currently in any worklist is 826000).

### SECOND CLOCK
**PRIMARY: this commit's git author time against the `# FIXTURE … start=` stamp
`tools/overnight.sh:103` writes as the first line of
`scratchpad/overnight/SEALPIERCE.tsv` (its `START=` is computed at `:99`), before
the first `fcode run`.**
**BACKSTOP:** if the tape carries `# FIXTURE-RESUME … start=UNKNOWN-legacy-tape`
(`tools/overnight.sh:110`), no `# FIXTURE` line at all, or the shard is routed to
a REMOTE worker (whose tapes carry no stamp), the second clock is **the `ts` of
the FIRST COMPLETED ROW** — conservative by construction.

⚠ **The treatment tree ALREADY EXISTS and is committed** (`bots/_v484sealpierce`,
added `68c474dd`, author time `2026-08-17T08:16:09+02:00`), together with its
engine probe, its invented map and three demo sweep tapes. This document is
**NOT** locked before the arm exists, only before its first screen row. That is
also what makes Obligation 13's intersection computable at lock time. Every demo
number below is **OBSERVABLE-AT-LOCK** and is registered as a PRIOR, never as
pre-registered evidence.

---

## ⛔ READ BEFORE RATIFYING — SEVEN THINGS THE LANE OWNS

**1. THE CONTROL IS NOT THE HOLDER.** `bots/_v468kladturbo` is Sleipnir v1
(platform v155), pinned as the corefill control at `scratchpad/CONTROL_PIN`
(`a9228ccb56ed9a65dd7d72ad1cb96068 bots/_v468kladturbo`), per Magnus, verbatim
(`docs/coordination.md:68129`): *"All our bots should now be competing against
Sleipnir during core shards, this is our benchmark today."* **The LADDER holder is
Odin (x3r0 v157), not Sleipnir**, so 50.0 on this page means "adds nothing to the
BENCHMARK"; `ODINVSSLEIP` is the converter into ladder units.

**2. ⛔⛔ THIS IS A TWO-PLANK SCREEN AND THE PAGE SAYS SO IN ITS TITLE OF RECORD.**
The lineage is `_x3r0v152` + `_v242bodyaware` + `_v464samestop` → **`_v468kladturbo`
(Sleipnir v1)** → **`_v481sealsentAnofund`** (LOKI-SEALSENT, seat mode, N=1,
`FUND_ON=False`) → **`_v484sealpierce`** (+ LOKI-SEALPIERCE). Against the
registered control this arm carries **BOTH** the seat-sentinel plant and the pierce
ladder. `grep -c LOKI_SEALSENT bots/_v484sealpierce/*.py` → **23 doctrine, 23 raid,
4 eco, 1 main**, with `LOKI_SEALSENT_ON = True` at `doctrine.py:1423`.
⇒ **NO BAND ON THIS PAGE MAY BE ATTRIBUTED TO THE PIERCE LADDER ALONE.** The
pierce-only delta is `_v481sealsentAnofund` → `_v484sealpierce` and is much smaller
(`doctrine.py` one block, `main.py` four hunks, `raid.py` one hunk, **`eco.py`
byte-identical**).
⭐ **AND THE ALTERNATIVE DESIGN IS NAMED HERE RATHER THAN LEFT UNSAID, BECAUSE IT
IS THE ONE THAT WOULD ISOLATE THE MECHANISM: a screen with `control =
bots/_v481sealsentAnofund` is a ONE-PLANK read of the pierce ladder.** It is NOT
what this page registers, because the session's control is pinned to Sleipnir for
every arm and because the question Magnus's directive poses is a FAMILY question
("does the pierce ladder move a seat-sentinel arm toward parity"). **If the builder
prefers the isolating design, that is a DIFFERENT prereg with a different control
line, not an amendment to this one.**

**3. THE PARENT'S NUMBER IS 46.07 AND IT IS NOT A VERDICT.** `results.tsv:477-478`
(`sealsentan-autostop-1000`): **46.07% [43.15, 48.99] at n = 1,120, type
`cancellation`**, stopped 2026-08-17T05:59:42Z by `tools/auto_gate.py --apply`
under the **TREND-FLOOR@1000** clause (first-1,000 prefix 46.90% < the 52.0 house
floor), against a registered n of 5,400, on **`worker@work-server-1`**. The row's
own words: *"⛔ THIS IS NOT A VERDICT AND MUST NOT BE READ AS ONE"* and *"⛔ THIS
SHARE IS SELECTED-PESSIMISTIC AND MUST NOT BE REUSED AS THE ARM'S ESTIMATE"*
(expected regression ~**+2pp**, on an n=2 basis).
⛔⛔ **CONSEQUENCE, AND IT IS THE HARDEST CONSTRAINT ON THIS PAGE: "DOES THE PIERCE
LADDER MOVE THE ARM FROM ~46 TOWARD PARITY?" IS NOT A RESOLVABLE INFERENCE, AND NO
BAND BELOW IS DENOMINATED IN IT.** Three independent reasons, each sufficient:
(i) the reference is a **selected** stop, so its bias is toward pessimism by an
amount estimated from **two** prior cases; (ii) it ran on a **different host** and
the s42 cross-host rider forbids differencing across boxes on the 0.98 exemption;
(iii) at n=1,120 its half-width is ±2.9pp before any selection allowance. **The
46-comparison is DESCRIPTIVE on this page. Every pre-committed band is denominated
on the ABSOLUTE share against 50.00 and 51.33.**
⭐ **ONE PRE-COMMITMENT MADE NOW, BEFORE LOOKING, SO IT IS NOT A POST-HOC CHOICE:
the parent reference quoted at readout is recomputed on the FULL KEPT TAPE**
(`scratchpad/overnight-remote/worker@work-server-1/SEALSENTAN.tsv`, reported at
draft as **1,739 data rows** — i.e. ~619 rows landed after the stop mark), **not on
the 1,120 the stop was denominated on.** That is the less-selected of the two
available numbers. It is OBSERVABLE-AT-LOCK (this agent read the row count, not the
share) and it remains DESCRIPTIVE.

**4. ⛔⛔ THE FLAG-OFF EQUIVALENCE CLAIM HAS NO ARTIFACT ON DISK, AND THE HOUSE RULE
REQUIRES ONE.** The build record and `docs/coordination.md:69678` assert *"OFF ==
parent byte-identical on 14/14 maps (`NOISE_ON=False`, `--tle 0`), positive control
firing on 3/14"*. Checked at draft:
* the harness would be **`tools/det.py`** (deterministic-paired, `NOISE_ON=False`,
  `--tle 0`, `DET_OUT` default `./det_results.json`);
* **`det_results.json` on disk is `[]` — 2 bytes — with mtime 16 Aug 22:29, a day
  BEFORE this work.** It is not this run's output;
* the `bots/_tmp_pierceon` / `_tmp_pierceoff` / `_tmp_baseoff` trees named in
  `doctrine.py:2156` and in every sweep tape **do not exist and were never
  committed** (`git log --all --diff-filter=A -- 'bots/_tmp_*'` → empty);
* **the string `3/14` appears in no log in the repo.**
⇒ **THE POSITIVE CONTROL WAS ASSERTED, NOT SHOWN TO HAVE BEEN DRIVEN.** Per the
session's own standing rule that flag-off equivalence cites replay-SHA or AST
evidence from the build record, **this arm's equivalence is UNVERIFIED**.
**PRE-COMMITTED CONSEQUENCE: either (a) `tools/det.py` is re-run before the shard
fires and its `det_results.json` is retained and cited, or (b) the readout carries
"FLAG-OFF EQUIVALENCE UNVERIFIED" on the same line as the primary share.** ⚠ This
is the clause on this page most likely to change what somebody does; run it first.

**5. THE SHARD TAPE CANNOT SEE THE MECHANISM, AND A FIRINGS READ IS MANDATORY
BEFORE THE PRIMARY.** `tools/overnight.sh:138-139` runs every game with
`--tle 10 --replay /dev/null`; the tape's columns (written at `:104`) are
`ts shard game map seed seat winner cond turns` — **no entity, build, shot or
stdout information exists on it, in either arm.** The mechanism is CONDITIONAL in
the strongest sense on this page — its top rung fired on **4.0% of seat shots** in
the tree's own demos — so `docs/prereg/BARS.tsv`'s FIRINGS-BEFORE-PRIMARY rule
binds absolutely.
> **F1 and F2 (below) are READ, and their numbers written down, BEFORE any sentence
> containing the primary share is typed.** A primary typed ahead of the firings read
> is a REGISTRATION BREACH regardless of what it says (the precedent is
> `results.tsv:471`, this session, this repo).

**6. THE DEMO EVIDENCE IS REAL, IS COMMITTED, AND CARRIES FOUR DEFECTS THAT TRAVEL
WITH EVERY NUMBER TAKEN FROM IT.** The three sweep tapes (`scratchpad/sweep_kladde3.txt`,
`sweep_v78c.txt`, `sweep_base2.txt`, all committed at `68c474dd`, 72 games, 3,652
seat rounds) reconcile exactly against `doctrine.py:2161-2173`. But:
* **the 24 belt kills are ASSIST-INCLUSIVE by the tree's own note**
  (`doctrine.py:2171-2172`: *"removal within one round of a seat shot, **assists
  included** — our raiders peck the same targets"*) — **not a clean
  pierce-attributable count;**
* **"the whole 14-map new-maps pool" is a UNION across THREE DIFFERENT OPPONENTS**
  (kladde 8 maps, v78 6, base 8), not a pool any single fixture covered — and
  **none of those 14 is the 15-map corefill pool the screen plays;**
* **SEED DEGENERACY: 14 of the 72 demo rows are exact duplicates of another row in
  the same fixture** (same map, same seat, different seed, every summary column
  identical — 13 in `sweep_kladde3.txt`, 1 in `sweep_v78c.txt`). **Effective
  distinct games ≈ 58, not 72.** `tools/effective_n.py` exists for exactly this and
  was not run;
* **the shipped `raid.py:869-874` docstring CONTRADICTS the shipped tape**: it cites
  *"0 of 1,190 live seat-Sentinel rounds had a belt behind the Core on the CHOSEN
  facing, against 218 counterfactual"* from a **superseded, uncommitted** sweep,
  while the committed replacement reads **124 of 634 against 364**. ⇒ **a reader of
  this tree's own comments gets a number the tree's own tape refutes.** Flagged for
  the builder as a pre-fire fix; it changes no behaviour and is not a reason to hold
  the lock.
**Two further prose-vs-artifact defects, recorded so nobody quotes them:**
`doctrine.py:2084` and the commit body say *"100+ real shots"* on the engine probe
while **the only tape on disk (`scratchpad/pierce_probe.err`, UNTRACKED) carries
20**; and the jitter figure *"the kladde/parent fixtures' 22 → 5"*
(`doctrine.py:2183-2187`) **does not reconstruct** from the committed tapes (they
give 22 → 1 on MOUTH alone, or 42 → 9 on MOUTH+APRON). The `opp_v78` half
(*"11 → 28"*) does reconstruct exactly.

**7. THIS FIXTURE PRODUCES LARGE NEGATIVES AND HAS JUST DONE SO ON THIS ARM'S OWN
PARENT.** `SEALSENTAN` stopped at 46.07 and `KLADLADDER` finished 41.86% at
n = 3,404 — both demo-clean on the same base. **A clean probe and a clean demo
predict FIRING and predict nothing about SHARE.** No sentence on this page may
treat the 20/20 probe as a forecast of the number.

---

## RATIFY: Hypothesis

**Adding a pierce-aware target ladder and a pierce-aware siting term to a
seat-planted Sentinel — so that a turret whose line already contains an enemy CORE
tile prefers, when one is available, the far-side conveyor / apron belt / healing
builder BEHIND that core, and so that the build-time facing choice is scored for
far-side belt exposure — raises our LOCAL pooled game share against
`bots/_v468kladturbo` itself to 51.33% or higher at n = 5,400 games across all 15
corefill maps and both seats.**

**Provenance of the idea, verbatim (Magnus, s48;
`bots/_v484sealpierce/doctrine.py:2074-2078`):** *"what if the sentinels placed
around their core also shoot whatever is on the other side of the core? If it's a
conveyor it can break the enemy eco by just keeping one killed and then keep
hammering the core. Also if it can shoot a builder that is healing the core, would
it be beneficial to kill it?"*
⚠ **PROVENANCE DEFECT, disclosed: this quote exists in exactly one place in the
repo — the tree's own doctrine comment.** Magnus's three other s48 directives are
logged verbatim in `docs/coordination.md` (`:68034`, `:68098`, `:68158`); this one
is not. **The tree comment is its own sole provenance**, and the builder should
confirm the wording before it is quoted anywhere else.
**Release provenance:** the screen was HELD on family evidence
(`docs/coordination.md:69678`) and released under Magnus's cores directive —
`docs/retro-builder-s48-2026-08-17.md:42`: *"SEALPIERCE hold→screen — held on
family evidence, released under Magnus's cores directive with honest priors on the
page."*

**THE ENGINE FACT THE PLANK RESTS ON, AND IT IS CONFIRMED, NOT INFERRED.**
`bots/_probe_pierce/main.py` on `maps/invented/pierce16.map26` (both committed at
`68c474dd`; tape `scratchpad/pierce_probe.err`, ⚠ **UNTRACKED**): a Sentinel at
`(9,7)` facing EAST has attack pattern `[(10,7),(11,7),(12,7),(13,7),(14,7)]` — two
enemy core tiles and **three far-side tiles**. Over **20 fired shots**, the enemy
core reads **`hp 500 → 500` on 20 of 20** while the far-side belt takes damage.
⇒ **PIERCE, NOT BEAM: the shot damages the TARGET TILE only, and an intervening core
takes nothing.** ⚠ **PRECISION, corrected against the brief: the explicit
18-damage transition `20 → 2` appears on **10** of the 20 shots; the other 10 are
overkills on a 2 HP belt where the ledger reads the same-round rebuild.** The
core-takes-zero result is 20 of 20. The probe also demonstrates the **re-kill farm**:
11 `built CONVEYOR` lines = the original plus **10 rebuilds on one relaid tile**.

**The mechanism claim, stated so it can be wrong** — three effects, and the
hypothesis is that the first two outweigh the third:
* **IT SPENDS SHOTS THAT WOULD HAVE HIT A 500 HP CORE ON A 20 HP BELT.** A seat
  Sentinel's ordinary target is the core; a far-side conveyor dies to one shot and
  costs the enemy a rebuild plus the delivery it was carrying.
* **IT CAN KILL A CORE-HEALING BUILDER THROUGH THE CORE** — the healer rung, gated
  on a dwell of `LOKI_SEALPIERCE_HEAL_DWELL = 1` ("seen twice").
* **⚠ AND EVERY SHOT SPENT ON THE FAR SIDE IS A SHOT NOT SPENT ON THE CORE, AT 10
  AMMO EACH, ON A TEAM MAGAZINE THE PLANK DELIBERATELY DOES NOT TOP UP**
  (`doctrine.py:2144-2150`: *"AMMO IS DELIBERATELY UNTOUCHED"*). **Under
  `R1000_IS_DEFEAT` the core is the only thing that scores**, so a ladder that
  reorders shots away from it is buying eco damage with kill tempo. **That is the
  named cost channel and D1 below is where it would show.**

**⇒ A flat result is INFORMATIVE.** It would say a rung that fires on 4.0% of seat
shots cannot move a 5,400-game share either way — which, given the rung is FREE in
titanium and free in ammo, makes the pierce logic a candidate free rider on any
core-adjacent turret rather than a plank of its own.

**PRICE, quoted per house rule via `tools/scale_trace.py --price 20` (the seat
Sentinel this ladder rides on carries +20pp of cost scale): READING 1 (as a total,
20pp) = p0.0 SMALL; READING 2 (on top of the r100 median of 180pp, i.e. 200pp) =
p65.4 ORDINARY — inside the range teams routinely carry. READING 2 is the primary
per the tool's own instruction.** ⇒ **the PIERCE LADDER ITSELF costs ZERO scale and
zero ammo** — it re-ranks shots an already-bought turret was going to fire. The
priced 20pp belongs to the SEALSENT plank underneath it, which this screen carries
and does not isolate.

---

## REGISTRATION BLOCK

**TARGET BAND: N/A — local corefill screen with ZERO rated ladder exposure: no submission, no activation, no unrated challenge, so `tools/target_value.py` has no input. Nothing on this page ends in a ship; the only branch that reaches the ladder is a later, separately-registered head-to-head against the live holder.**
**PINNED: N/A — local self-play. The opponent version is fixed by construction: the control tree is `bots/_v468kladturbo` at the commit this shard runs from, pinned at `scratchpad/CONTROL_PIN` (`a9228ccb56ed9a65dd7d72ad1cb96068 bots/_v468kladturbo`). There is no opponent churn to pin against and no calibration relevance to protect.**
**SURFACE: local**
**PLANK CLASS: offensive — a turret sited on the ENEMY core's heal-seat ring, re-ranking its shots at targets behind the enemy core. Nothing in the diff touches home defence, so the `DEFENCE_ADMISSION_BAR`'s r300 clause does not formally bind. ⛔ D1 IS READ AS AN EXCLUSION ANYWAY AND IS THIS PAGE'S MOST LOAD-BEARING DIAGNOSTIC: the plank deliberately re-ranks shots AWAY from the enemy core, which is the only thing that scores under `R1000_IS_DEFEAT`.**
**KILL-ROUND NON-REGRESSION: ITT timely-kill rate over ALL 5,400 games (share ending `cond == core_destroyed` in our favour with `turns <= 300`), treatment vs control, scored as an EXCLUSION — the 95% CI on the difference must EXCLUDE a fall of more than 2.0pp. ITT RMST300 (mean of `min(turns,300)`, every non-kill scoring the full 300, `tools/fieldcal_read.py:239`) is read beside it on the same 5,400 rows. Median-crossing-300 is the gross backstop and the kill-win-conditioned share is a DIAGNOSTIC only — it carries a collider. ⛔⛔ THIS IS THE BINDING DIAGNOSTIC ON THIS PAGE, NOT A FORMALITY: the plank deliberately re-ranks shots AWAY from the enemy core at 10 ammo each, and under `R1000_IS_DEFEAT` the core is the only thing that scores. A positive share with a timely-kill regression is a plank trading kill tempo for eco damage and is off-programme regardless of the share.**
**CLUSTER UNIT: none** — CLAUDE.md's enumeration PERFORMED, not asserted: (i) the **MATCH** cluster does not exist on this surface — `tools/overnight.sh` writes one TSV row per `fcode run`, so 1 row = 1 game and no row shares a match with another; (ii) the **OPPONENT** cluster is degenerate — every one of the 5,400 rows plays the identical control tree, so the pooled stratum holds exactly one opponent and there is no between-opponent variation for a design effect to describe. Both clusters die ⇒ DEFF = the measured local constant **0.98** (pair-weighted, ρ = −0.020, 124 shards, s39 audit); naive intervals are correct and marginally conservative. **The platform constants (1.529 rated / 1.833 unrated) are NOT applicable.** ⚠ **The s42 cross-host rider is registered and BINDS ON THE PARENT COMPARISON: `SEALSENTAN` ran on `worker@work-server-1` and this shard's host is a builder decision, so the parent reference is CROSS-HOST and may be quoted DESCRIPTIVELY and never differenced.**
**ESTIMATOR: unweighted pooled treatment game share** = (rows with `winner == T`) / (completed rows), over all 5,400 rows, both seats pooled, all 15 maps pooled, no reweighting. Interval by `tools/cluster_ci.py` with the local constant. Seat A and seat B shares are reported SEPARATELY as a fixture diagnostic and are never the bar — seat is worth ~6.8pp on byte-identical arms, which is why the n is a multiple of 30.
**DOSE: pierce-rung shots per demo fixture — treatment 57 (MOUTH 33 + APRON 24, i.e. 57/1,409 = 4.0% of seat-Sentinel shots) vs flag-off control 0 by construction, n=72 demo games / 3,652 seat rounds on `maps/new-maps/` (`scratchpad/sweep_kladde3.txt`, `sweep_v78c.txt`, `sweep_base2.txt`, all committed at `68c474dd`; decoder `scratchpad/sp_shots.py`). ⚠ FOUR DISCLOSURES TRAVEL WITH THIS NUMBER: (a) the denominator EXCLUDES `OTHER = 2` — all shots are 1,411 — and the numerator EXCLUDES the HEALER rung, so ALL THREE pierce rungs together are 76/1,409 = 5.4% and `CORE` is 1,333/1,409 = 94.6%; (b) 14 of the 72 rows are exact seed duplicates ⇒ effective distinct games ≈ 58; (c) none of the 14 demo maps is in the 15-map corefill pool the screen plays; (d) the control arm's zero is STRUCTURAL (`LOKI_SEALPIERCE_ON = False` ⇒ the parent exactly), not measured at lock. ⛔ THIS IS A FIRING DEMONSTRATION AND NOT AN EFFECT SIZE. The registered F1 battery below is what converts it into a measured dose on the pool the screen plays.**
**PLANNED n: 5400 games** (= 15 maps × 2 seats × 180, so map and seat balance is exact; `tools/overnight.sh:68` has carried the 15-map pool since the 2026-08-13 rotation and the runner's own comment requires multiples of 30).
**BOUNDARY: 5400 games** — LOCAL surface, one tape row is one game; there is no accept/attempt distinction on this fixture. ⛔ **A LINE COUNT IS NOT A ROW COUNT**: this tape carries an unprefixed column header (`tools/overnight.sh:104`), and a naive `wc -l` / `awk '!/^#/'` over-reports n by exactly one (measured on KLADLADDER, `results.tsv:474`). The registered denominator is **DictReader row count, cross-checked against the heartbeat and against `max(game id) + 1`.**
**CUT-SHORT: floor 2700 games.** Below 2,700 completed tape rows this leg publishes descriptive tallies (share, per-seat, per-map, kill-clock) and takes **NO comparative look and no bar verdict**; the half-width at 2,700 is ±1.87pp, already wider than the 1.33pp margin the bar is built on. An `auto_gate` cancellation at CATASTROPHE@400, MARK-1000 or TREND-FLOOR@1000 is an **OPERATIONAL STOP, not a verdict**, typed `cancellation`. ⭐ **ONE CARVE-OUT, PRE-COMMITTED:** a CATASTROPHE-clause cancellation (95% CI upper < 45.0 at n ≥ 400) is arithmetically INCOMPATIBLE with every band above Band 4, so a stop under that clause DOES license the Band-4 sentence at the partial n — **provided F1/F2 have been read first**, and provided the partial share is disclosed as **selected-pessimistic** with the ~+2pp allowance the parent's own row carries. ⚠ **A TREND-FLOOR@1000 stop is the SPECIFIC outcome this arm's parent produced.** It is the most likely stop clause here and its share is the MOST selected of the three; if it fires, the readout quotes the FULL KEPT TAPE, not the mark, and says so.
**BAR: 51.33. MDE: 0.00pp — THIS IS A POINT RULE ONLY AND LICENSES NO EXCLUSION CLAIM ABOUT AN EFFECT SIZE.** Per the OB16 corollary (obligations doc, 2026-08-15T03:52:45Z): the standard corefill band IS `50 ± half_width` at n=5,400, so clearing 51.33 puts the CI's lower edge at exactly 50.00 — it excludes 50 and excludes **no positive effect size whatsoever**. n for the exclusion it CAN make (bar ≠ 50.0): **5,400**, the planned n.
**BASE RATE: 50.00**
**BAR SOURCE:** house-standard corefill futility band, `50 + 1.96*sqrt(.25/5400) = 51.33pp`, local DEFF 0.98 so naive — the identical bar carried by `docs/prereg/BARS.tsv` rows `SEALFLOOR6`, `SENTTHR`, `KLADTKILL`, `KLADTK2`, `KLADTURBOR`, `DRAINTURBO`, `KLADLADDER`, `SEALSENTAN`, `SEALSENTA` and `ECOMMIT`. **Constructed, not observed.** ⛔ **AND THE BAR IS DELIBERATELY *NOT* SET AT THE PARENT'S 46.07**, for the three reasons in READ-BEFORE-RATIFYING #3: a bar anchored on a selected, cross-host, n=1,120 cancellation would be a bar whose reference cannot be pinned, and OB16's whole point is that a bar must state what it can exclude.
**BASE RATE SOURCE:** structural A/A expectation of a seat-balanced, map-balanced self-play fixture whose control tree is an ancestor of the treatment. Empirically calibrated by `IDNULL140` — **49.27% [47.94, 50.60] at n = 5,400**, 2026-08-16T18:02:04Z, same fixture (`results.tsv:454`, type `cert`) — and by `NULL125` — **51.04% at n = 5,400** (`results.tsv:346`, type `verdict`; ⚠ that row's share FIELD reads `0.510` with EMPTY CI columns while its prose reads 51.04% — the prose is the citation and the row is not a source of an interval). Two A/A cells, one either side of 50.0. ⇒ **a bare clearance in [51.33, 52.4] is a band an A/A cell has already produced**, which is why Band 2 is pre-registered as WEAK.
**POOL ERA: post-2026-08-13-rotation** — the 15-map local pool of `tools/overnight.sh:68` (`antler archipelago auroraveil drakkarfjord drumlin fjordgate frostgate glacierkeep icefloe midgard nordkap ragnarok royale valkyrie yulerune`). (`check_pool_era` treats this as n/a on a LOCAL surface per SPEC §6; declared anyway so the population is on the page.) ⛔ **AND IT IS THE SHARPEST POOL DEFECT ON ANY OF TODAY'S PAGES: ALL 72 DEMO GAMES RAN ON `maps/new-maps/`, AND NOT ONE OF THOSE 14 MAPS IS IN THE 15-MAP COREFILL POOL.** The entire dose evidence for this plank was measured on geometry the screen never plays, against three opponents the screen never meets. **F1 exists to fix exactly that and is not optional.**
**REFERENCE n: none** — the comparator is generated inside this same shard from the same 5,400 seeds; there is no fixed external reference sample, so no resolution floor at n→∞. **(The parent's 46.07 is NOT a reference sample in this sense: it is a descriptive cross-host cancellation, per READ-BEFORE-RATIFYING #3.)**
**TREATMENT TREE: bots/_v484sealpierce**
**TREATMENT DIFF REFS: 68c474dd^ 68c474dd**
**MECHANISM METRIC READS: bots/_v484sealpierce/main.py:960 — `prio = self._pierce_prio(pierce, t, et, prio)`, inside `_turret` (defined at `main.py:898`). This is the ONE line where the pierce ladder overrides the base's `TURRET_PRIO`; the shot itself (`ct.fire(best)` at `:968`) is shared with the base and is therefore NOT the discriminating line. Arming gate: `main.py:933`. Build-time siting term: `raid.py:838-839` (the `W_BELT*pbelt` additive and the `-pfar` tie-break) plus `_pierce_site_term`. Observed as F1 (pierce-rung shot share on the SCREEN pool, split MOUTH / APRON / HEALER / CORE / OTHER) and F2 (far-side exposure: chosen-facing vs any-legal-facing). TREATMENT DIFF TOUCHES: bots/_v484sealpierce/doctrine.py bots/_v484sealpierce/eco.py bots/_v484sealpierce/main.py bots/_v484sealpierce/raid.py. INTERSECTION: yes — `main.py:960` is inside the hunk the diff ADDS at `main.py:942-970`, and every pierce identifier is absent from the control: `_pierce_prio`, `_pierce_anchor`, `_pierce_watch`, `_pierce_dwelt`, `_pierce_site_term`, `LOKI_SEALPIERCE`, `pierce_seat`, `pierce_dwell` each occur **0 times in all four files of `bots/_v468kladturbo`** — and, for the record, **0 times in all four files of `bots/_v481sealsentAnofund`** too, verified at draft. The metric CANNOT read identically in both arms.**
⚠ **DIFF-REFS DISCLOSURE:** `68c474dd` carries **12 paths**, including the probe bot, an invented map, three scratchpad scripts and three sweep tapes. The SEMANTIC treatment surface vs the control is the FOUR bot files declared above (`diff -rq`), of which `eco.py` differs **only** because of the inherited SEALSENT reserve hunk — **`eco.py` is byte-identical between `_v481sealsentAnofund` and `_v484sealpierce`, i.e. the pierce plank touches no economy code at all.**
**METRIC WINDOW: r0-r1000. GATING CONSTANTS: LOKI_SEALPIERCE_BAND_MAX=2, LOKI_SEALPIERCE_BELT_DSQ=8, LOKI_SEALPIERCE_HEAL_DWELL=1, LOKI_SEALPIERCE_W_BELT=4, LOKI_SEALSENT_MIN_HARV=2, LOKI_SEALSENT_MAX=1, LOKI_SEALSENT_HOLD_MAX=12. MECHANISM CAN OCCUR IN WINDOW: yes** — **NOT ONE of these is a ROUND FLOOR.** `BAND_MAX` and `BELT_DSQ` are SQUARED DISTANCES, `HEAL_DWELL` is a per-target sighting count, `W_BELT` is a siting WEIGHT, `MIN_HARV` is a harvester count, `SEALSENT_MAX` a turret count, `HOLD_MAX` a per-raider round BUDGET. The plank has **no round gate**: it arms the first turn a seat Sentinel exists with `dsq_core ≤ 2`, and the seat Sentinel itself is gated only on establishment and harvester count (the parent tree's demo planted at r24 on drumlin). ⚠ **The plank has NO ammo floor of its own — `doctrine.py:2144-2150` states ammo is deliberately untouched — so the window in which it can fire is bounded in practice by the team magazine, which this leg does not control and cannot read.**
⚠ **AND ONE NAMED CONSTANT DOES NOT EXIST: `LOKI_SEALPIERCE_W_FAR` is referenced in the doctrine prose at `:2137` and `:2211` but is NEVER DEFINED.** Depth is implemented as the `-pfar` tie-break slot at `raid.py:839`, not as a weight. **It is not declared above because declaring a constant that does not exist would be worse than omitting it**, and it is flagged here for the builder.
⚠ **DISCLOSED, because a green tool run with warnings under it is how a warning stops being read: `prereg_check.py` will emit `OBLIGATION 17, PARTIAL WINDOW` warns against the line above and THEY ARE ARTEFACTS OF THE CHECKER.** Its `check_metric_window` arithmetic reads every declared integer as a ROUND, so a squared distance of 2 is reported as "rounds r0-r1 cannot contain the mechanism".
**PRE-STATE: the predicted-change set is NOT already in the target state at lock.** Verified at draft against the control tree: every pierce identifier listed under MECHANISM METRIC READS returns **0** in all four files of `bots/_v468kladturbo`. The control has no pierce anchor, no dwell watch, no ladder override and no far-side siting term; it also has no seat-Sentinel machinery at all (`LOKI_SEALSENT` → 0 in all four control files). **The behaviour this leg predicts to change cannot already be in the target state.** ⚠ **AND THE FAMILY CLAIM IS LIKEWISE NOT PRE-SATISFIED**: the parent measured 46.07 (selected), so "a seat-sentinel arm at parity or better" is a genuinely open outcome and Bands 3 and 4 are live.
**MAP SEGMENT: none expected — and the reason is that I CANNOT SIGN one, which under Obligation 15a is a reason to declare none rather than to declare an unfalsifiable segment.** The rung fires when a far-side belt or a healing builder sits behind the enemy core on the seat Sentinel's PERMANENT facing. **That depends on where the ENEMY chooses to run its belts and station its healers — an opponent-policy property, not a terrain property** — and the control here is our own bot, whose belt geometry is itself map-varying in a direction nobody has measured on the corefill pool. **No measurement of far-side exposure exists on any of the 15 pool maps**; the 28.8% figure (`447/1,550`) is from `maps/new-maps/` against three other opponents. **A segment declared without a predicted sign "confirms" the mechanism whichever way it lands, which is exactly what 15a forbids.** Per-map and per-size-class shares WILL be printed at readout as **DESCRIPTIVE** material whose declared purpose is to feed F2's exposure diagnostic — **not to rescue a failed pooled primary. No map cut may rescue this arm**, and nothing may be banked off those shares without a fresh prereg. ⚠ **One candidate is named and DELIBERATELY NOT REGISTERED**: the five 900-area maps, where longer belt runs plausibly mean more far-side belt. Registering it would hand this arm a second chance to pass — OB15b's exact prohibition.
**CELL VERSION CHURN: N/A — not a panel, no `CELLS:` line, one fixed local control tree.**
**GATE RESOLUTION: the shard is governed by the pinned `tools/auto_gate.py` marks — CATASTROPHE@400 (STOP if the 95% CI upper < 45.0, `auto_gate.py:236`), MARK-1000 (STOP if the CI upper < the registered BAR 51.33), TREND-FLOOR@1000 (STOP if the first-1,000 prefix share < 52.0, `auto_gate.py:250` — RAISED from 51.0 by Magnus 2026-08-16), and the same floors again at MARK-2700 (`auto_gate.py:233-236`). Their firings are OPERATIONAL CANCELLATIONS that free a core — typed `cancellation`, never `verdict`, licensing NO exclusion claim (with the single CATASTROPHE carve-out in CUT-SHORT). ⭐ The remote report-only limitation at `auto_gate.py:113` is DEAD since `a50f27ef` (`tools/remote_cancel.py` gives `--apply` a guarded remote stop path), so the strict floors bind on ws1/ws2 too; this shard may run LOCAL or REMOTE, and a remote route switches the second clock to the registered first-completed-row backstop. The RESOLVABLE gate this document owns is the primary at full n, whose margin (1.33pp) exceeds its own half-width (±1.32pp) by 0.01pp — resolvable, and only just. ⛔ **THE COMPARISON TO THE PARENT'S 46.07 IS REGISTERED AS UNRESOLVABLE BY CONSTRUCTION** (selected stop, cross-host, n=1,120) **and therefore defaults to the RESTRICTION: it is quoted descriptively and licenses no inference in either direction.** Everything else on this page (F1, F2, D1-D3, seat and map splits) is DIAGNOSTIC and cannot rescue a failed primary. Any branch that does not resolve is UNRESOLVED, and an UNRESOLVED gate defaults to the RESTRICTION: no promotion, no ship conversation, no combination claim.**

---

## FALSIFIER

**PRIMARY FALSIFIER: at n = 5,400 the 95% CI UPPER bound on the treatment's pooled
game share falls BELOW 51.33.** That excludes the bar and says the seat-Sentinel
plant WITH the pierce ladder does not add measurably to Sleipnir.
**Consequence, registered in advance and split by how far it falls:**
* **CI upper < 51.33 but CI contains 50.0** → the two-plank arm is at PARITY with
  the benchmark. See Band 3 — and note that a parity read here, against a parent
  whose own (selected) read was 46.07, is the branch in which the pierce ladder is
  most plausibly doing work; **but it is NOT a licensed attribution**, because the
  parent comparison is unresolvable.
* **CI upper < 50.0** → **the two-plank arm subtracts**, and the honest attribution
  is *"the seat-sentinel plant costs, and the pierce ladder did not repay it"* —
  never *"the pierce ladder costs"*.

**MECHANISM FALSIFIER (independent of the primary, and it can fire first):** if
**F1** shows the pierce rungs firing at or near zero on the 15-map corefill pool —
i.e. the 4.0% measured on `maps/new-maps/` against three other opponents does not
reproduce on the pool and opponent the screen actually plays — then the plank did
not deliver its dose in this fixture and **the primary is uninterpretable in either
direction with respect to the PIERCE half**: a flat share would mean "the rung
never fired", not "the rung fired and did not pay". Per FIRINGS-BEFORE-PRIMARY this
is read BEFORE the primary is typed, and if it fires the primary is reported as
**PIERCE NOT MEASURED** — the SEALSENT half is still measured, and the leg then
becomes a second (and this time full-n, same-host) read of the parent plank, which
is a genuinely useful thing to have and should be banked as such. **This is not
hypothetical: s47's delta D2 records a wiring null escaping demos to a 436-game
shard, and this arm's demo pool shares ZERO maps with its screen pool.**

---

## READING, PRE-COMMITTED — four bands, written before the data

Registered now so no band is chosen after the fact. **Read TOP-DOWN; the first row
whose condition holds is the reading. The rows are disjoint by construction.**
⛔ **Every band is denominated on the ABSOLUTE share.** The "46-class" language of
the drafting brief is deliberately NOT used as a band boundary, for the reasons in
READ-BEFORE-RATIFYING #3; the parent's number appears only as a descriptive line in
the readout.

| # | band at n = 5,400 | pre-committed reading |
|---|---|---|
| **1** | **CI lower ≥ 51.33** | **THE PIERCING SEAT SENTINEL ADDS.** Real and resolved on this fixture. Promotes to a combination input and to a separately-registered head-to-head against the live holder. ⛔ Attribution is capped by READ-BEFORE-RATIFYING #2: this credits SEALSENT+PIERCE together. ⚠ OB16: the standard band has MDE 0 — this branch may claim "we can exclude 50" and may NOT claim any minimum effect size. |
| **2** | **point ≥ 51.33 but CI lower < 51.33** | **REAL-BUT-SMALL, COMBINATION INPUT ONLY.** Registered in advance as WEAK: `NULL125`'s byte-identical A/A read 51.04, so a bare clearance in [51.33, 52.4] is not distinguishable from fixture noise by this leg alone. Rows KEPT; no ship conversation; a replication on fresh seeds is the price of promotion. |
| **3** | **point < 51.33 AND CI contains 50.0** | **PARITY — THE PLANK IS FREE, AND THE PIERCE LOGIC IS PROMOTED AS A FREE RIDER, NOT AS A PLANK.** A seat Sentinel that also strips far-side belt, at parity with the benchmark, means the rung costs nothing measurable while doing something an opponent has to repair. **Pre-committed action: PARK the SEALSENT family as a standalone plank and carry `_pierce_*` forward as a candidate for ANY core-adjacent turret**, which is a cheaper and better-aimed use of it than a seat-plant screen. It does NOT license a ship. ⚠ The tempting sentence *"the rung moved us up from 46"* is FORBIDDEN here — see #3 above. |
| **4** | **CI upper < 50.0** | **THE TWO-PLANK ARM SUBTRACTS.** With the parent already at 46.07 (selected) the honest reading is that the SEAT PLANT is the cost and the pierce ladder did not repay it. **The SEALSENT family dies as a ship candidate; the PIERCE logic does NOT — it is untested apart from the plant and its isolating screen (control = `bots/_v481sealsentAnofund`) is the registered successor if anyone wants it.** ⛔ No readout sentence may attribute this band to the pierce ladder. |

⚠ **Rows 3 and 4 both fire the PRIMARY FALSIFIER**; the band decides which half of
its consequence applies.
⚠ **Nothing here treats 50.0 as a floor.** A share below 50 is a live outcome with a
named mechanism (a seat plant that costs 42-81 Ti at live scale, plus shots
re-ranked off the enemy core under `R1000_IS_DEFEAT`) and it is pre-named so a
negative is not explained away as noise.

---

## MECHANISM DIAGNOSTICS TO READ AT READOUT

**Measurability is declared per metric. `NOT MEASURABLE` is written where it is
true, rather than a metric being quietly renamed into something the tape carries.**

### ⛔ ORDERING, REGISTERED AS A HARD SEQUENCE
**F1 and F2 run and are written down BEFORE any sentence containing the primary
share is typed.** See READ-BEFORE-RATIFYING #5.

### F0 — THE FLAG-OFF EQUIVALENCE, WHICH IS OWED BEFORE THE SHARD FIRES.
**EXECUTING TOOL: `tools/det.py`** (deterministic-paired, `NOISE_ON=False`,
`--tle 0`, output `DET_OUT`, default `./det_results.json`).
**Registered requirement:** `bots/_v484sealpierce` with `LOKI_SEALPIERCE_ON = False`
against `bots/_v481sealsentAnofund`, **replay-SHA identical on every cell**, with
the **positive control** (`LOKI_SEALPIERCE_ON = True`) **differing on at least one
cell** — a check that can only confirm is decoration (OB17's rider).
**STATE AT LOCK: NOT SATISFIED.** `det_results.json` is `[]`, 2 bytes, mtime 16 Aug
22:29 — a day before this work; the `bots/_tmp_*` trees the claimed run used do not
exist and were never committed; the claimed `3/14` positive-control figure appears
in no log.
**PRE-COMMITTED CONSEQUENCE:** run it and retain the JSON, **or** the readout
carries **"FLAG-OFF EQUIVALENCE UNVERIFIED"** on the same line as the primary
share. ⛔ **The tree also removes a behaviour the parent had in a way the flag
cannot restore by itself: `main.py:942-970` REORDERS the dwell-watch to run before
`can_fire`. The builder should confirm that reorder is inside the flag guard; if it
is not, "flag off == parent exactly" (`doctrine.py:2197`) is false and F0 is the
only thing that would catch it.**

### F1 — THE RUNG READ ON THE POOL THE SCREEN PLAYS. MEASURABLE, but NOT off the shard tape.
`tools/overnight.sh:138-139` passes `--replay /dev/null`, so the SEALPIERCE shard
produces no shot events. F1 runs on a **separate serial battery that keeps
replays**, decoded by the tree's own shot decoder:
```
# battery: bots/_v484sealpierce vs bots/_v468kladturbo, --tle 10, --replay <unique path>
#          on the 15 COREFILL POOL MAPS, both seats, ≥2 DISTINCT seeds per cell
.venv/bin/python scratchpad/sp_shots.py <replays…>
```
**REGISTERED SIZE: 60 games = 15 maps × 2 seats × 2 seeds, SERIAL.**
**Pre-registered expectation, with its sign:** pierce-rung shots (MOUTH + APRON +
HEALER) are **> 0 on a majority of the 15 pool maps**, and the pooled rung share is
**within a factor of 2 of the demo's 5.4% of seat shots**. **A rung share
indistinguishable from 0 on the pool is the MECHANISM FALSIFIER firing.**
⛔ **SEED DISTINCTNESS IS A REGISTERED REQUIREMENT, NOT A DETAIL: 14 of the 72 demo
rows were exact duplicates of another row in the same fixture. `tools/effective_n.py`
is run on the F1 battery and its effective-n figure is printed beside the rung
share.** A battery whose effective n is materially below its nominal n has not
delivered its registered size.
**OB17 checks, and the one that can surprise is named:**
1. *Name the executing tool* — `scratchpad/sp_shots.py`, committed at `68c474dd`.
2. *Confirm the RUNNER emits what is registered* — ⚠ **`scratchpad/sp_demo.py`
   emits per-game ROLLUPS only; the per-shot detail lives in `sp_shots.py`'s own
   output and was NEVER SAVED in the demo runs** (which is why the *"mouth-cut kill
   at r98"* anecdote in `docs/coordination.md:69678` has no artifact and must not be
   quoted). ⇒ **the F1 battery must retain `sp_shots.py`'s output, not just the
   rollup.**
3. *Consequence of silent non-execution* — if the battery is run on `sp_demo.py`'s
   default map list it silently falls back to `maps/new-maps/`, **which is the exact
   off-pool defect this battery exists to repair, and nothing in the output would
   say so.** ⇒ **the readout must print the map list it actually ran.**

### F2 — FAR-SIDE EXPOSURE AND THE PERMANENT-FACING COST. MEASURABLE on the same battery.
Per seat-Sentinel round: does a far-side belt sit behind the core on **our chosen**
facing, and would one have sat there on **any legal** facing? Demo anchor, reported
as an ANECDOTE and NOT as an expected effect: **447 / 1,550 = 28.8%**
(`doctrine.py:2163-2167`, rolled up from the three committed tapes).
**Pre-registered expectation, with its sign: the chosen-facing exposure rate on the
pool is BELOW the any-legal-facing rate**, because `rotate()` is gunner-only so a
Sentinel's facing is permanent and the siting term must guess at build time.
**F2 is DESCRIPTIVE and cannot rescue the primary** — its declared purpose is to say
how much of the rung's ceiling the siting term is actually capturing, which is the
number a successor plank would need.
⚠ **AND F2 HAS A KNOWN CONTRADICTION IN THE TREE TO RESOLVE:** `raid.py:869-874`'s
docstring says **0 of 1,190** on the chosen facing while the committed tape says
**124 of 634**. **F2's readout states which of the two the pool reproduces.**

### D1-D3 — the kill-clock read. MEASURABLE, shard-native (`cond`, `turns`, `winner`).
* **D1 — TIMELY-KILL RATE (the `DEFENCE_ADMISSION_BAR` primary), ITT.** Share of ALL
  treatment-seat games ending `cond == core_destroyed` in our favour with
  `turns ≤ 300`, treatment vs control, both on the same 5,400 rows.
  **Non-regression is the bar and it is stated as an EXCLUSION, per CLAUDE.md's
  fail-to-exclude clause: the 95% CI on the difference must EXCLUDE a fall of more
  than 2.0pp.** A "no significant rise" phrasing is not admissible.
  ⭐⭐ **D1 IS THE MOST LOAD-BEARING DIAGNOSTIC ON THIS PAGE AND IT IS WHERE THE
  PLANK'S NAMED COST WOULD APPEAR.** Under `R1000_IS_DEFEAT` the enemy core is the
  only thing that scores; this plank deliberately re-ranks shots AWAY from it, at 10
  ammo each, on a magazine it does not top up. **A positive share with a D1
  regression is a plank that trades kill tempo for eco damage, and that is
  off-programme regardless of the share.**
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
* **Whether the pierce ladder ALONE pays.** The arm carries SEALSENT and PIERCE
  under one screen and **they are NOT SEPARABLE here.** The isolating design
  (control = `bots/_v481sealsentAnofund`) is named in READ-BEFORE-RATIFYING #2 and is
  a different prereg. **No readout sentence may attribute any band to one half.**
* **Whether a belt kill is pierce-attributable.** The demo's 24 belt kills are
  **assist-inclusive by the tree's own note** and our raiders peck the same targets.
  Nothing on either surface separates a pierce kill from a peck kill in the same
  round. **The plank's headline demo number is not a clean attribution and cannot be
  made one by this leg.**
* **Titanium the enemy lost to a cut belt.** The shard tape carries no resource
  column and the replays are discarded; the F-battery decodes shots and builds, not
  delivery. **Under `R1000_IS_DEFEAT` this is the correct thing to be blind to** —
  eco damage is instrumental — but the blindness is stated rather than glossed.
* **Team ammo at the moment of a pierce shot.** The plank spends 10 ammo a shot and
  tops up nothing; no shipped tool reads the magazine at a shot event. **The
  opportunity cost this page names as its main risk is therefore UNOBSERVED except
  through D1.**
* **Per-unit CPU.** Local replays zero-fill `execTimeUs` (the s42 D33 instance:
  `tle_census.py` returns 0 across 1,649 local builder-turns while reading 8,847 µs on
  platform replays), so **no CPU claim is available from this leg.** ⚠ Disclosed:
  `LOKI_SEALPIERCE_LOG` is **False** in the fired tree (`doctrine.py:2214`), so unlike
  ECOMMIT this arm adds no unmatched `print()` cost.
* **Seed determinism.** `NOISE_ON` pins an unseeded per-unit salt, so base-vs-base at
  one seed diverges at round 0. **No seed-matched or replay-diff equivalence claim is
  available on the SHARD fixture**; the flag-off equivalence claim belongs to F0's
  `--tle 0` + `NOISE_ON=False` harness and, as of lock, **has no artifact.**

---

## THE CHANGE — `file:line`, control → treatment

**TREATMENT TREE: `bots/_v484sealpierce`.** Two planks vs the control; ONE vs its
parent. Verified at draft with both diffs.

**A. THE PIERCE PLANK (the delta from `bots/_v481sealsentAnofund`):**
1. **`doctrine.py:2071-2214`** — the doctrine block (prose `:2074-2195`) and **eight**
   constants: `LOKI_SEALPIERCE_ON = True` (`:2197`, *"False == `_v481sealsentAnofund`
   exactly"*), `LOKI_SEALPIERCE_BAND_MAX = 2` (`:2198`),
   `LOKI_SEALPIERCE_BELT_DSQ = 8` (`:2202`), `LOKI_SEALPIERCE_HEALER_ON = True`
   (`:2205`), `LOKI_SEALPIERCE_HEAL_DWELL = 1` (`:2206`),
   `LOKI_SEALPIERCE_SITE_ON = True` (`:2209`), `LOKI_SEALPIERCE_W_BELT = 4` (`:2210`),
   `LOKI_SEALPIERCE_LOG = False` (`:2214`). ⚠ **`LOKI_SEALPIERCE_W_FAR` is named in
   the prose and does not exist.**
2. **`main.py:139-156`** — per-turret state (`pierce_seat`, `pierce_dwell`, …).
3. **`main.py:923-937`** — `pierce = self._pierce_anchor(…)` and the arming gate at
   `:933`.
4. **`main.py:942-970`** — the dwell-watch reorder (now BEFORE `can_fire`) and the
   ladder override at **`:960`**. The shot is `ct.fire(best)` at `:968`, shared with
   the base.
5. **`main.py:981-1079`** — `_pierce_anchor`, `_pierce_prio`, `_pierce_watch`,
   `_pierce_dwelt`.
6. **`raid.py:818-902`** — the siting key gains an additive `W_BELT*pbelt` term and a
   `-pfar` tie-break (`:838-839`), plus `_pierce_site_term`. ⚠ **`:869-874`'s
   docstring cites a superseded uncommitted sweep and contradicts the committed
   tape.**
7. **`eco.py` — BYTE-IDENTICAL to the parent. The pierce plank touches no economy
   code.**

**B. THE INHERITED SEALSENT PLANK (present in this screen, absent from the
control):** `doctrine.py:1263-1451` (block + 17 constants incl.
`LOKI_SEALSENT_ON = True`, `LOKI_SEALSENT_FUND_ON = False`, `MODE = "seat"`,
`MAX = 1`, `TI_FLOOR = 0`, `HOLD_MAX = 12`, `SLOT_SEALSENT = 13`);
`eco.py:367-417` (`_sealsent_reserve` + its call site — **inert while
`FUND_ON=False`**); `raid.py:104-117`, `:283-302`, `:304-311` (cached keysets, step
2a before the barrier, the `hold` skip); `raid.py:672-988` (the `_sealsent_*`
family); `main.py:133-138` (hold/want counters).

---

## WHAT THIS LEG COSTS AND WHAT IT DOES NOT

**Cost: one core to n = 5,400, plus ~60 serial games for F1/F2 and one `tools/det.py`
pass for F0.** ZERO rated ladder exposure, zero submissions, zero unrated challenges
— nothing on this page touches the platform, which is why `TARGET BAND` is N/A.

**It does NOT decide a ship.** The strongest branch promotes the arm to (a) a
combination input and (b) a separately-registered head-to-head against the live
holder — Magnus's procedure verbatim (*"we start by testing it against the current
slot, If it beats it we can switch"*), templated by `SLEIPH2H`. **Gate-1-to-gate-2
transitivity is UNVALIDATED in this repo (QUEUE #65: 3 concordant, 1 not)**, and the
benchmark is not the holder, so `ODINVSSLEIP` is the converter into ladder units.

**AND THE MOST LIKELY USEFUL OUTCOME IS NOT A SHIP.** Band 3 promotes the
`_pierce_*` logic as a FREE RIDER for any core-adjacent turret — zero titanium, zero
ammo, no economy code touched — which is a cheaper thing to own than the seat plant
it is currently welded to. **That is stated before the data so it does not read as a
consolation prize afterwards.**

---

**PROVENANCE:** `docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md` (read in full: OB1, OB7, OB12, OB13, OB14, OB15a/b/c, OB16 + its corollary and cross-host rider, OB17 + its rider) · `docs/prereg/PREREG-SEALSENTAN-2026-08-17.md` and `docs/prereg/PREREG-ECOMMIT-2026-08-17.md` (today's house style, both read in full) · `docs/prereg/BARS.tsv` (header, the FIRINGS-BEFORE-PRIMARY rule, rows `SEALSENTAN`:302 and `SEALSENTA`:303) · `CLAUDE.md` · `tools/prereg_check.py` (`RULES`, `DEFF`, `check_metric_window`, `check_pool_era`) · `tools/auto_gate.py:113,233-236,250` · `tools/overnight.sh:68,99,103,104,110,118-120,138-139` · `tools/det.py` · `tools/effective_n.py` · `tools/cluster_ci.py` · `tools/fieldcal_read.py:239` · `tools/scale_trace.py --price 20` (run at draft; READING 2 = p65.4 ORDINARY) · `bots/_v484sealpierce/{doctrine,eco,main,raid}.py` · `bots/_v481sealsentAnofund/{doctrine,eco,main,raid}.py` · `bots/_v468kladturbo/{doctrine,eco,main,raid}.py` · `bots/_probe_pierce/main.py` · `maps/invented/pierce16.map26` · `scratchpad/{sp_shots.py,sp_demo.py,mk_pierce_map.py}` · `scratchpad/{sweep_kladde3.txt,sweep_v78c.txt,sweep_base2.txt}` (the three committed demo tapes) · `scratchpad/pierce_probe.err` (⚠ UNTRACKED) · `det_results.json` (empty, stale — the F0 finding) · git commit `68c474dd` and `git diff --name-only 68c474dd^ 68c474dd` · `docs/coordination.md:68129` (Magnus's benchmark ruling), `:68158` (the seat-sentinel directive), `:69678` (the hold entry) · `docs/retro-builder-s48-2026-08-17.md:42` (the release) · `scratchpad/corefill_work.txt` · `scratchpad/CONTROL_PIN` · `results.tsv` (rows 346 `null125-final`, 454 `idnull140-cert-5400`, 466 `kladturbo-local-confirm-5400`, 471 the FIRINGS-BEFORE-PRIMARY precedent, 474 `kladladder-n-final-correction`, 477-478 `sealsentan-autostop-1000`, 479 `sealsenta-retired-preclause`) · `scratchpad/auto_gate_cancelled.tsv:73-74` · the drafting brief supplied by the builder lane s48. No file under `bots/`, `tools/`, `scratchpad/`, `docs/prereg/BARS.tsv`, `results.tsv`, `HANDOVER.md`, `PROGRAMME.md` or `QUEUE.md` was created or modified by this agent, and no game was run.
