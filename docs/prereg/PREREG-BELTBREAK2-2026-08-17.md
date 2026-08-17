# SCREEN PREREG — `BELTBREAK2`: the beltbreak-gunner plant gate moved 15 rounds EARLIER (`LOKI_BELTBREAK_RND` 25 → 10)

Drafted by a fresh opus subagent with NO inherited session context beyond the
inputs listed under `PROVENANCE`. The builder lane ratifies the judgment lines
and types the lock commit; this agent wrote no code under `bots/`, appended no
worklist row, appended no `docs/prereg/BARS.tsv` row, fired no game, started no
shard, and touched neither `results.tsv` nor `HANDOVER.md` nor `PROGRAMME.md`
nor `QUEUE.md`.

**STATUS: drafted BEFORE the `BELTBREAK2` row is appended to
`scratchpad/corefill_work.txt`, BEFORE any `docs/prereg/BARS.tsv` row exists,
BEFORE any file named `scratchpad/overnight/BELTBREAK2*` exists, and BEFORE the
leg's first game.** Drafting session wall clock at write time
**`2026-08-17T08:27:31Z`** (`date -u`, same shell call); repo HEAD at draft
`e0fb5d56` (author time `2026-08-17T10:16:03+02:00`). Verified at draft:
`grep -c BELTBREAK2 scratchpad/corefill_work.txt` → **0**;
same grep on `docs/prereg/BARS.tsv` → **0**;
`ls scratchpad/overnight/ | grep -i beltbreak2` → **0 files**.

### LOCK, clock 2 (local shard)
Per the obligations doc's **2026-08-17T07:24:55Z addendum**, which replaced the
clock-2 boilerplate that eleven preregs had copied and that was not executable as
written. **PRIMARY:** the shard tape's own `# FIXTURE … start=` stamp
(`tools/overnight.sh:99` sets `START=$(date -u …)`, `:103` writes it to the tape
before the first game). Quote it verbatim beside the lock commit's git author
time. **BACKSTOP, if the tape carries no `# FIXTURE` line** (every REMOTE tape;
107 of 238 local tapes carry it): the tape's **FIRST COMPLETED ROW `ts`** —
conservative by construction, since the true start is strictly earlier, so the
substitution can only OVERSTATE the prereg-to-start gap (measured cost 1–2 s).
⛔ **NOT AVAILABLE: the heartbeat's `STARTING` line** — `overnight.sh:100` writes
it with `>` and every later state overwrites it. **State which clock was used.**
This shard is registered LOCAL, so the primary is expected to be available.

### ⚠ COMMIT PROVENANCE OF THE TREATMENT TREE — IT IS UNTRACKED AT DRAFT
`bots/_v488beltbreak2/` **exists on disk and git does not track it**
(`git status --porcelain` → `?? bots/_v488beltbreak2/`; `git ls-files` → empty).
That is NOT the legitimate "locked before the tree exists" case, and
`tools/prereg_check.py` FAILs it by name (`OB13_UNTRACKED_ARM`): with no git
object, `git diff` returns nothing and **the one-executable-line claim below is
unverifiable *by git* for this arm.** The claim is nevertheless verified, by the
instrument that does not need git — a direct file diff against the parent tree,
reproduced in `THE CHANGE` below and re-runnable in one command. **The builder's
lock commit is what converts that into a git-checkable fact.** Recorded here
rather than left for a certifier to discover.

---

## ⛔ READ BEFORE RATIFYING — EIGHT THINGS THE LANE OWNS

**1. ⛔⛔ THE MOST LIKELY OUTCOME OF THIS LEG IS AN OPERATIONAL CANCELLATION AT
n=2700, NOT A VERDICT — AND NO EXEMPTION IS AVAILABLE.** This is priced, not
hedged. `tools/auto_gate.py:715 combo_of()` reads the `stack.py` compose marker
off the **TREATMENT** tree's own `doctrine.py`. `bots/_v488beltbreak2/doctrine.py:2078`
carries `# ---- composed by tools/stack.py from: turbo (_x3r0v152), bodyaware
(_v242bodyaware), samestop (_v464samestop)` — **inherited from the control**
(`bots/_v468kladturbo/doctrine.py:1879`), which every arm on this chassis
inherits. ⇒ **the gate will score `BELTBREAK2` as a COMBO and `COMBO_BAR = 55.0`
binds on the n=2700 prefix** (`auto_gate.py:278`, Magnus 2026-08-16).
**`COMBO-BAR-EXEMPT` tokens in the whole of `docs/prereg/BARS.tsv`: ZERO**, and
that token's registered purpose (`auto_gate.py:906-919`) is *a MECHANISM test
scored against its own additive prediction*. **This arm is a PROSPECT — a dose
iteration on a plank whose own bar is a house-band screen — so it may NOT claim
the exemption, and this document does not.**
**THE ARITHMETIC, done before the fire:** the parent `_v480beltbreak` measures
**52.90%** vs `bots/_v468kladturbo`; this arm's dose is **+28.7%** shredders per
game; if share responds linearly to dose the projection is
`50.00 + 2.90 × 1.287 = 53.73%`, i.e. **~53.7%**. Against the pinned floors, at
that true share:

```
true share   P(prefix1000 < 52.0)   P(prefix2700 < 55.0)   P(reaches n=5400)
   52.0             0.500                  0.999                0.000
   53.0             0.263                  0.981                0.014
   53.7             0.140                  0.912                0.075
   55.0             0.028                  0.500                0.486
   56.0             0.005                  0.148                0.848
```
⇒ **at the projected 53.7 this arm reaches its own registered n with probability
0.075.** **REGISTERED READING OF THAT EVENT, pre-committed so it cannot be
re-read afterwards: a COMBO-BAR@2700 cancellation with a prefix in [52.0, 55.0)
is an OPERATIONAL CANCELLATION and is NOT a refutation of the dose plank.** It
says *"this combination is not the 55-class combination we are prospecting for"*,
which is a statement about the CHASSIS TOTAL, not about the 25→10 constant. In
particular such a stop licenses **no** sentence of the form "moving the gate
earlier did not pay", **no** comparison against the parent's 52.90, and **no**
closure of the timing axis. **Whether to spend a core on a leg with a 7.5%
chance of completing is a BUILDER/MAGNUS decision and is deliberately not made
on this page** — this clause exists so the decision is made with the number in
front of it.

**2. THE CONTROL IS THE LIVE LADDER HOLDER'S BOT, SO THIS LOCAL SCREEN IS ALSO A
SCREEN AGAINST WHAT IS LIVE.** `bots/_v468kladturbo` is **Sleipnir v1**, pinned
as the corefill control at `scratchpad/CONTROL_PIN`
(`a9228ccb56ed9a65dd7d72ad1cb96068 bots/_v468kladturbo` — quoted from
`tools/control_pin.py`'s output, not re-derived by hand). **Every share on this
page carries its control inline — `X% vs _v468kladturbo` — and that notation is
mandatory, not decorative:** three different 60s live in this repo and they
differ by ~9pp through the logistic. **50.0 vs `_v468kladturbo` means "adds
nothing to the bot we ship".** ⚠ **AND ONE DISCLOSURE THE PARENT'S PAGE DID NOT
NEED: the control is the SHIPPED BOT, not the CURRENT LADDER HOLDER** — x3r0's
Odin holds the slot (`ODINVSSLEIP` is the cell measuring that distance). "Also a
screen against what is live" means *against our own live-quality bot*, not
*against the incumbent of the ladder*.

**3. ⛔⛔ THE REGISTERED EARLY-vs-LATE CONTRAST OF THE PARENT PAIR IS VOID, AND
THIS ARM'S CASE MAY NOT BE BUILT ON IT.** `PREREG-BELTBREAK-EARLY` /
`PREREG-BELTBREAK-LATE` registered `Δ = p̂(EARLY) − p̂(LATE)` as their shared
PRIMARY with a cut-short floor of **2,700 rows in BOTH arms**. `BELTBREAK-LATE`
floor-stopped at **n=1,304, 47.39% [44.68, 50.10]** (TREND-FLOOR@1000,
`results.tsv:beltbreak-late-autostop-1000`), so **the comparative look is
forbidden by a clause locked before the data existed**
(`results.tsv:beltbreak-late-final`). ⇒ **the admissible statement is each
shard's OWN treatment-vs-control contrast, and nothing else.** The LATE arm's
47.39 may be cited here ONLY as the fact that it was CANCELLED, never as a term
in a difference. **The "timing gradient points EARLIER" sentence in `#4` below
is therefore stated as a MOTIVATION for choosing this axis, and is explicitly
NOT offered as evidence for it.**

**4. WHY TIMING IS THE AXIS, AND WHY THE OTHER THREE WERE REJECTED ON
MEASUREMENT RATHER THAN ON TASTE.** This is what makes "timing" a chosen axis
and not a guess, and it is the strongest section of the build agent's work:
* **`LOKI_BELTBREAK_CAP` 2→3 moved shredders/game by 0.000** on a common seed
  set (1.358 both), moved the median plant round the WRONG way (45→48), left
  shots/shredder flat (22.4→21.9) — and would have bought a permanent **+20% on
  the ONE GLOBAL ADDITIVE cost-scale factor** per extra gunner. **An
  instrumented copy of the parent with unrate-limited refusal counters (30 games)
  refuses on `CAP` 6.6×/game against `TI` 638×/game** — ⇒ **the BANK stops the
  third shredder, not the cap.** And the magazine is sized for two
  (`LOKI_BELTBREAK_AMMO = 24` = exactly two 12-ammo belt kills), so a third
  gunner under an unchanged magazine cannot complete one kill.
* **`DSQ_HI` 100→50** raised the near-band share but **cut shots/shredder
  22.6→16.7 and doubled the death rate** — the study's own survival gradient
  (§3.6: d²<10 halves gunner life for 60% of the output) reproduced locally.
* **Replace/repair was already working** — the cap is a LIVE CENSUS of friendly
  gunners in the annulus (`_live_beltbreak_guns`), not a monotone counter, so
  rubble cannot close this arm and there was nothing to fix.
* **The gate SATURATES at ~10, which is why this arm is not `RND = 1`.** `RND=10`
  puts **46 of 174 shredders (26.4%) at r10-24**, a window the parent reaches
  **0 of 163 times BY CONSTRUCTION**. Dropping to 1 adds only **8 of 186 (4.3%)
  below r10** and moves the median plant round 38→36.5 — nine more rounds of
  gate removal for nearly nothing, at nine more rounds of compounding scale
  drag. Below ~10 the binding constraint stops being the gate and becomes
  **ARRIVAL** (our median forward arrival is **r31**,
  `docs/research/FORWARD-ARRIVAL-BASELINE-2026-08-16.md`).
* **THE MOTIVATION, LABELLED AS MOTIVATION:** the parent at RND=25 measured
  52.90% and its RND=70 twin cancelled at 47.39. Per `#3` that pair cannot be
  differenced. It is why *earlier* was chosen over *later* as the direction to
  spend the next core on; it is not evidence that *earlier still* pays.
* ⚠ **AND THE STUDY'S OWN `EARLY` DEFINITION IS r ≤ 25, NOT 10.**
  `REPLAY-STUDY-offensive-gunner-2026-08-17.md` §7.1 writes the arms as *EARLY =
  first in-band plant at r ≤ 25 (the executor band: not adgato r13, ph r21,
  Jython r33)*. **A gate at 10 is BELOW the spec's own executor band and below
  every executor MEDIAN in it.** It is inside the field's earliest observed
  behaviour — §3.7's p10 column reads **ph r9, O(1) r14** — so it is not outside
  the field, but **this arm is extrapolating one step past the registered spec
  and the page says so.**

**5. ⛔⛔ SCALE DRAG IS THE NAMED HAZARD BY WHICH THIS ARM COULD SLOW OUR OWN
KILL, AND IT CARRIES A METRIC.** Cost scale is **ONE GLOBAL ADDITIVE team
factor**; every build adds to it and it inflates the cost of every subsequent
build of every type (`CLAUDE.md`, engine-confirmed s26). A gunner is **+20%**.
This arm buys **+28.7% more gunners** and buys them **EARLIER — median plant
round 49.5 → 40.0** — so the same contribution is paid across a longer tail and
inflates every later harvester, conveyor and turret. **⇒ the mechanism by which
this arm could push kills past r300 is not speculative; it is arithmetic on a
factor we have measured on the engine.** Registered metric: **D3 (RMST₃₀₀) and
D4 (median kill round)** below, and — because scale is not on the shard tape —
**F3, a `get_scale_percent()` read at fixed rounds off the retained D1/S1
replays.** ⚠ **A NULL ON THIS ARM IS THEREFORE PRE-LABELLED AMBIGUOUS IN ONE
SPECIFIC WAY: "the earlier gate paid nothing" and "the earlier gate paid and the
scale tail ate it" are NOT separable by this leg**, exactly as the parent pair
registered for its own asymmetry. No readout sentence may pick one.

**6. `shots/shredder` WAS FLAT, AND THAT IS THIS ARM'S MAIN NULL MECHANISM.**
On the larger both-seats battery **25.7 → 24.7**. The seat-A 120-game sweep read
22.4 → 31.0 and **did not reproduce**; the build agent's own doctrine comment
says so and calls the +38% seed-set noise. **⇒ the honest claim is: this arm buys
~29% MORE shredders each doing the SAME work.** And the marginal shredder is by
construction on the **worse** chain — it is the one the parent's gate refused,
i.e. the one whose target set or funding was second-best — **so declining
per-unit value with dose is the EXPECTED state of the world, not a surprise.**
A pooled share that moves less than proportionally to the dose is consistent with
the mechanism working exactly as measured.

**7. ⛔ 13% OF THE POOL CANNOT EXPRESS THE PLANK AT ANY DOSE, AND THAT CAPS THE
ACHIEVABLE POOLED EFFECT.** Measured: **antler and fjordgate produce 0 shredders
in BOTH arms, and royale ~0**, because on small maps the d²20-100 annulus of the
ENEMY core collides with our own hunt band (`HUNT_BAND_DSQ = 41` of OUR core) and
no tile satisfies both clauses. antler and fjordgate are the pool's only two
**CQ** maps (`tools/overnight_read.py:76-94 map_area_class`, area ≤ 260,
computed at draft — not a hardcoded size table). ⭐ **AND THE PARENT'S OWN TAPE
CORROBORATES IT INDEPENDENTLY OF THE DOSE INSTRUMENT: on
`scratchpad/overnight/BELTBREAK-EARLY.tsv` (n=3,053) antler reads 50.00%,
fjordgate 50.49% and royale 51.49% — the three flattest cells of fifteen, i.e.
A/A by construction** — against archipelago 68.63% and midgard 71.57%. Full
dilution arithmetic in `SEGMENT AND POPULATION` below.

**8. THE SHARD TAPE CANNOT SEE THE MECHANISM, AND A FIRINGS READ IS MANDATORY
BEFORE THE PRIMARY.** `tools/overnight.sh:138-139` runs every game with
`--replay /dev/null`; the tape's columns are `ts shard game map seed seat winner
cond turns` — **no entity, build, position or turret information exists on it, in
either arm.** The FIRINGS-BEFORE-PRIMARY rule (`docs/prereg/BARS.tsv` header,
research 2026-08-16T13:27:33Z) is registered here as a **HARD SEQUENCE**:
> **F1, F2 and F3 are RUN, and their numbers written down, BEFORE any sentence
> containing this arm's primary share is typed.** A primary typed ahead of the
> firings read is a REGISTRATION BREACH regardless of what it says, and the
> repair is an amendment chain, not a re-write. *(Precedent on the tape:
> `results.tsv:kladladder-verdict-amendment-f1f2-pending`.)*

---

## RATIFY: Hypothesis

**HYPOTHESIS.** *Opening the beltbreak-gunner plant gate at r10 instead of r25 —
one integer, `LOKI_BELTBREAK_RND` 25 → 10, on the otherwise byte-identical
`bots/_v480beltbreak` chassis — converts a measured **+28.7% shredders per game**
and a **median plant round 49.5 → 40.0** into a LOCAL pooled game share vs
`bots/_v468kladturbo` of **51.33% or higher** at n = 5,400 games across all 15
corefill maps and both seats, WITHOUT pushing our own kill past r300.*
Registered direction **POSITIVE**.

**Provenance of the idea, verbatim (Magnus's original directive that created this
plank family):** *"offensive gunner that shreds the enemy economy… a lot of the
top teams do this."*

**The mechanism claim, stated so it can be wrong.** The plank plants a **GUNNER**
in the **d² 20-100 annulus of the ENEMY core**, aimed at a belt or harvester tile
**that exists right now**, gated on
`can_fire_from(bp, facing, GUNNER, t)` where `t` is a live enemy entity read out
of THIS builder's vision THIS round, plus an explicit own-ray walk
(`_bb_ray_clear`). **This arm changes NOTHING about that selection — it changes
only the round from which the gate permits it.** The claim is therefore narrow
and falsifiable: **the r10-24 window contains plants worth having.** The parent
cannot reach that window by construction (0 of 163 / 0 of 202 plants), so the
window is genuinely new code behaviour rather than a re-weighting of existing
behaviour.

**⇒ AND A FLAT RESULT IS INFORMATIVE ABOUT THE PLANK, NOT ABOUT THE
INSTRUMENT.** The dose evidence is strong and pre-measured (§`THE DOSE
EVIDENCE`), so a flat share here says *the earliest plants are worth less than
the scale tail they buy* — which prices the timing axis rather than leaving it
open. That is the HONEST-NULL clause and it is registered in `FALSIFIER`.

---

## REGISTRATION BLOCK

**TARGET BAND: N/A — local corefill screen with ZERO rated ladder exposure: no submission, no activation, no unrated challenge, so `tools/target_value.py` has no input. Nothing on this page ends in a ship; the only branch that reaches the ladder is a later, separately-registered head-to-head against the holder.**
**PINNED: N/A — local self-play. The opponent version is fixed by construction: the control tree is `bots/_v468kladturbo` at the commit this shard runs from, pinned at `scratchpad/CONTROL_PIN`. There is no opponent churn to pin against and no calibration relevance to protect (CLAUDE.md's rule: pin treatment legs, never pin calibration panels — this is neither, it is self-play).**
**SURFACE: local**
**CLUSTER UNIT: none** — CLAUDE.md's enumeration PERFORMED, not asserted: (i) the **MATCH** cluster does not exist on this surface — `tools/overnight.sh` writes one TSV row per `fcode run`, so 1 row = 1 game and no row shares a match with another; (ii) the **OPPONENT** cluster is degenerate — every one of the 5,400 rows plays the identical control tree, so the pooled stratum holds exactly one opponent and there is no between-opponent variation for a design effect to describe; (iii) a third candidate, **HOST**, is killed by REGISTRATION rather than by measurement: this shard is registered to run on ONE host (LOCAL by default), and the Addendum 11 rider (the 0.98 exemption is a WITHIN-HOST measurement) is why splitting it across hosts would require an amendment typed BEFORE the first row. All surviving clusters die ⇒ DEFF = the measured local constant **0.98** (pair-weighted, ρ = −0.020, 124 shards, s39 audit), i.e. **NAIVE intervals are correct and marginally conservative. The platform constants (1.529 rated / 1.833 unrated) are NOT applicable here and importing them would widen every interval on this page by 24-35% for correlation that has been measured absent.**
**ESTIMATOR: the unweighted pooled treatment game share** = (rows with `winner == T`) / (completed rows), over all 5,400 rows, both seats pooled, all 15 maps pooled, no reweighting. Because the shard is exactly balanced on 15 maps × 2 seats × 180, the pooled share and the map-stratified equal-weight share coincide by construction; the stratified form is computed at readout as an **arithmetic consistency check only** and is not a second estimator (s28 ring-hold: four estimators inside 0.010 of one bar flipped MEET/MISS among themselves). Seat A and seat B shares are reported SEPARATELY as a fixture diagnostic and are never a bar — seat is worth ~7.6pp on byte-identical arms, which is why n is a multiple of 30. **Any estimate quoted at readout arrives from `tools/cluster_ci.py` (HEAD) so the interval and the point are produced by the same call; the pre-data half-widths on this page are closed-form Wald with DEFF 0.98 and their arithmetic is shown inline.**
**DOSE: shredders per game 1.444 (treatment, `LOKI_BELTBREAK_RND = 10`) vs 1.122 (control-by-flag-restore, `LOKI_BELTBREAK_RND = 25` = the parent `bots/_v480beltbreak`), n=180 games per arm, common seed set 930000-930005, 15 maps × both seats, `--tle 10`, engine-side count off retained replays.** A SHREDDER is defined engine-side as a friendly GUNNER whose FIRST `placeEntity` (rotation re-emissions skipped per `tools/corpus/replay_events.py:16,113`) lands at **d² 20-100 of the ENEMY core AND d² > `HUNT_BAND_DSQ`(41) of OUR OWN core** — the second clause is what separates this weapon from a home counter-battery gunner that satisfies the annulus as pure geometry on a small map. **BOTH VERDICTS PRESENT, and the flag-off half is the one that matters: 32/32 games byte-identical end-state vs the parent with `RND` restored to 25, WITH a flag-on positive control on the same fixture reading 20/32 games NON-identical.** 32/32 alone is equally consistent with a harness that cannot see any difference; the positive control is what makes the zero mean something. **0 tracebacks in 360 games.**
**PLANNED n: 5400 games** (= 15 maps × 2 seats × 180, so map and seat balance is exact; `tools/overnight.sh:68` has run a 15-map pool since the 2026-08-13 rotation and its own comment requires multiples of 30). ⛔ **5400 IS SAID EXPLICITLY BECAUSE A SOLO SHARD OTHERWISE DEFAULTS TO A 2700 TARGET, and at 2700 the bar arithmetic below is unreachable** (margin 1.33pp against a half-width of ±1.87pp).
**BOUNDARY: 5400 games** — LOCAL surface, one tape row is one game; there is no accept/attempt distinction on this fixture and no accepts count is declared. ⛔ **A LINE COUNT IS NOT A ROW COUNT**: the tape carries an unprefixed header line under the `# FIXTURE` line, so a naive `wc -l` over-reports n by exactly one (measured on KLADLADDER, `results.tsv:kladladder-n-final-correction`). The registered denominator is **DictReader row count over non-`#` lines, cross-checked against the heartbeat's `n TARGET` and against `max(game id) + 1`.**
**CUT-SHORT: floor 2700 games.** Below 2,700 completed rows this arm publishes descriptive tallies (share, per-seat, per-map, per-class, kill-round, `cond` mix) and takes **NO bar verdict**; the one-sample half-width at 2,700 is ±1.87pp, already wider than the 1.33pp margin the bar is built on, so a sub-2,700 read cannot resolve its own branches. An `auto_gate` firing at CATASTROPHE@400, MARK-1000, TREND-FLOOR@1000 or COMBO-BAR@2700 is an **OPERATIONAL CANCELLATION, not a verdict**, typed `cancellation`. ⭐ **ONE CARVE-OUT, PRE-COMMITTED:** a CATASTROPHE-clause cancellation (95% CI upper < 45.0 at n ≥ 400) is arithmetically INCOMPATIBLE with every band above Band 4, so a stop under that clause DOES license the Band-4 sentence at the partial n — **provided F1/F2/F3 have been read first** and provided the partial share is disclosed as **selected-pessimistic** (a floor stop fires on a LOW PREFIX DRAW, so conditional on stopping the arm's true share is HIGHER than the number that stopped it; expect roughly +2pp of regression, side lane s47, n=2 cases, a DIRECTION with a rough size and not a calibrated correction). ⛔ **AND NO OTHER CLAUSE'S CANCELLATION LICENSES ANY BAND — see READ-BEFORE-RATIFYING #1 for the COMBO-BAR case specifically, which is the likely one.**
**BAR: 51.33. MDE: 0.00pp — THIS BAR IS A POINT RULE ONLY AND LICENSES NO EXCLUSION CLAIM ABOUT AN EFFECT SIZE** (OB16 corollary, 2026-08-15T03:52:45Z: the standard corefill band IS `50 ± half_width` at n = 5,400, so clearing 51.33 puts the CI's lower edge at exactly 50.00 — it excludes 50 and excludes no positive effect size whatsoever). n for the one exclusion it CAN make (bar ≠ 50.0): **5,400**, the planned n. **The r300 admission read below is the OTHER bar on this page and it IS sized — see `KILL-ROUND NON-REGRESSION`.**
**BASE RATE: 50.00**
**BAR SOURCE:** the house-standard corefill futility band, `50 + 1.96*sqrt(0.98*0.25/5400) = 51.33pp`, local DEFF 0.98 so naive — the identical bar carried by `docs/prereg/BARS.tsv` rows `SEALFLOOR6`, `SENTTHR`, `KLADTKILL`, `KLADTK2`, `KLADTURBOR`, `DRAINTURBO`, `KLADLADDER`, `SEALSENTAN`, `SEALSENTA`, `ROUTESCORE`, `BELTBREAK-EARLY` and `BELTBREAK-LATE`, which is what keeps this arm numerically comparable to the turret-family reads it extends — **and specifically comparable to its own parent, which is the point of a dose iteration.** **Constructed, not observed.**
**BASE RATE SOURCE:** structural A/A expectation of a seat-balanced, map-balanced self-play fixture whose control tree is the treatment's own base. Empirically calibrated by `IDNULL140` — **49.27% [47.94, 50.60] at n = 5,400**, 2026-08-16T18:02:04Z, same host and fixture (`results.tsv:idnull140-cert-5400`) — and by `NULL125` — **51.04% at n = 5,400** (`results.tsv:null125-final`). Two A/A cells, one either side of 50.0, both intervals containing it. ⇒ **a bare clearance in [51.33, 52.4] is a band an A/A cell has already produced**, which is why Band 2 is pre-registered as WEAK. ⚠ **The two cells are 1.77pp apart**; on a fixture where byte-identical arms can differ by that much, a dose iteration whose projected gain over its own parent is **+0.83pp** is asking this fixture a question near its floor. **Disclosed before the data.**
**REFERENCE n: none** — the bar's comparator is a CONSTRUCTED null of 50.00 generated inside this same shard from its own 5,400 seeds; there is no external reference SAMPLE. ⛔ **AND THE PARENT'S 52.90% IS EXPLICITLY NOT A REFERENCE SAMPLE ON THIS PAGE.** Naming `BELTBREAK-EARLY`'s tape as a reference would make the checker size 51.33 as a two-fixture comparison at ±1.87pp and correctly FAIL it — a true statement about a bar nobody registered. **The parent-vs-this-arm difference is NOT a registered estimand here** (its half-width at 3,053 + 5,400 is ±2.14pp against a projected difference of 0.83pp — unresolvable, and the parent's tape is a CANCELLED, selected-pessimistic partial, which is exactly the asymmetric-stop defect the parent pair registered). **Any parent-vs-child sentence at readout is DESCRIPTIVE and carries that half-width.**
**TREATMENT TREE: bots/_v488beltbreak2**
**TREATMENT DIFF REFS: none — the arm tree is UNTRACKED at draft (`git status --porcelain` → `?? bots/_v488beltbreak2/`), so `git diff` has nothing to show and `prereg_check.py` reports OB13 as UNTRACKED-ARM. The executable diff of record is `diff -u bots/_v480beltbreak/doctrine.py bots/_v488beltbreak2/doctrine.py`, reproduced verbatim in THE CHANGE; the builder's lock commit is what makes it git-checkable.**
**MECHANISM METRIC READS: bots/_v488beltbreak2/raid.py:882 — the timing gate `if rnd < (LOKI_BELTBREAK_RND if LOKI_BELTBREAK_EARLY else LOKI_BELTBREAK_LATE_RND): return self._bb_refuse("EARLY")`, the SINGLE site at which the manipulated constant is read, inside the BELTBREAK shredder ladder and NOT on the forward-sentinel path. TREATMENT DIFF TOUCHES: bots/_v488beltbreak2/doctrine.py. INTERSECTION: yes — by IMPORT BINDING, which is the honest form and is the form the checker computes: `raid.py:64` is `from doctrine import *`, so the name `LOKI_BELTBREAK_RND` read at `raid.py:882` binds to the ONE line the diff changes (`doctrine.py:1439`). ⚠ A path-only intersection would ALSO pass here for a trivial reason — the whole tree is new to git, so every file "appears in the diff" — and that reading is REFUSED on this page: `raid.py`, `main.py` and `eco.py` are BYTE-IDENTICAL to the parent's (`cmp` clean on all three, verified at draft), so the only thing that can make the metric read differently between arms is the imported constant. **The metric therefore CANNOT read identically in the two arms, which is the LOKI-18 failure this obligation exists for.**
**METRIC WINDOW: r0-r1000. GATING CONSTANTS: LOKI_BELTBREAK_RND=10, LOKI_BELTBREAK_LATE_RND=70, LOKI_BELTBREAK_MIN_HARV=1, LOKI_BELTBREAK_CAP=2, LOKI_BELTBREAK_DSQ_LO=20, LOKI_BELTBREAK_DSQ_HI=100, LOKI_BELTBREAK_MAX_ROT=1, LOKI_BELTBREAK_STALE=3, LOKI_BELTBREAK_AMMO=24, LOKI_BELTBREAK_TI_FLOOR=40, LOKI_BELTBREAK_MAX_TGT=12. MECHANISM CAN OCCUR IN WINDOW: yes** — **exactly ONE of these is a round gate**, `LOKI_BELTBREAK_RND = 10`, and it is an **OPENING** round, not a window that closes: `raid.py:882-883` refuses while `rnd < 10` and never refuses above it (`LOKI_BELTBREAK_LATE_RND = 70` is INERT in this tree because `LOKI_BELTBREAK_EARLY = True` selects the other branch of the ternary — declared anyway, because an undeclared constant is the failure OB17 exists for). The rest are counts, distances (d²), a staleness budget in rounds, and titanium/ammo thresholds. ⇒ **the mechanism's window is r10-r1000, inside the declared r0-r1000, and a REPLANT can occur at any round because the cap is a LIVE CENSUS of friendly gunners in the annulus, so rubble cannot close this arm.** ⭐ **THE `RND=10` SEMANTICS ARE GATE-OPENS, NOT "PLANTS BY r10":** our median forward ARRIVAL is r31, so a literal "plants by r10" arm would be empty by construction; the measured effect of the change is that **26.4% of plants now land in r10-24**, a window the parent reaches zero times, while the median plant round moves 49.5 → 40.0.
⚠ **DISCLOSED, because a green tool run with warnings under it is how a warning stops being read: `prereg_check.py` will emit `OBLIGATION 17, PARTIAL WINDOW` warns against the line above and THEY ARE ARTEFACTS OF THE CHECKER.** Its `check_metric_window` arithmetic reads every declared integer as a ROUND, so a harvester count of 1 and a live-gunner cap of 2 render as "rounds r0-r1 cannot contain the mechanism". The constants are declared anyway.
**PLANK CLASS: OFFENSIVE — an economy-denial weapon (a forward GUNNER planted in the enemy's belt, aimed at conveyors and harvesters), not a defensive turret and not a home screen.** ⭐ **AND THE r300 ADMISSION READ IS REGISTERED ANYWAY, NOT CLAIMED AS INAPPLICABLE.** `PROGRAMME.md`'s `DEFENCE_ADMISSION_BAR` binds on defensive planks; the reason it is carried here regardless is READ-BEFORE-RATIFYING #5 — **this arm has a named, arithmetic mechanism for slowing our own kill (a +20% scale contribution per gunner, +28.7% more of them, bought ~10 rounds earlier), and a plank with a kill-delay mechanism must carry a kill-delay bar whatever its class label.** Registering it is strictly stricter than the programme requires and cannot function as a second chance to pass: **both the share bar and the r300 bar must hold.**
**KILL-ROUND NON-REGRESSION: ITT RMST₃₀₀ is the operational estimator (PROGRAMME.md's 2026-08-16T05:36:10Z arbitration, whose vintage rule makes it binding on preregs locked from that date — this one is) — mean kill time censored at the r300 horizon over ALL games, a non-kill scoring 300, computed per side on the same rows; the bar is scored as an EXCLUSION: the 95% CI UPPER bound on (treatment RMST₃₀₀ − control RMST₃₀₀) must EXCLUDE +5.0 rounds (MDE +5.0 rounds; paired sd on the parent's tape is 88.99 rounds ⇒ half-width ±2.37 at n=5,400, so the exclusion resolves). SECOND REGISTERED FORM, both required: the ITT timely-kill-by-r300 rate (share of ALL games ending `cond == core_destroyed` with `turns <= 300`, denominator every game played, per side) — its 95% CI LOWER bound on (treatment − control) must EXCLUDE a fall of 3.0pp (MDE 3.0pp; paired sd 75.28pp ⇒ half-width ±2.01pp at n=5,400). THIRD, and it is a DIAGNOSTIC ONLY because it carries a collider: the kill-win-CONDITIONED share (15.1% vs 7.8% ITT on the rated tape) plus the conditioned median — reported beside the two bars, never as either of them. Median kill round crossing 300 is the gross backstop.**
**PRE-STATE: the predicted-change behaviour is NOT already in the target state at lock.** Verified at draft against the control tree: `grep -c 'BELTBREAK\|_bb_\|beltbreak' bots/_v468kladturbo/{doctrine,eco,main,raid}.py` → **0 / 0 / 0 / 0** — `bots/_v468kladturbo` has no beltbreak path at all, so the whole plank is absent from the control. Against the PARENT, which is the comparison that matters for a dose iteration: the parent's gate refuses every plant while `rnd < 25`, so **the r10-24 window is EMPTY in the parent BY CONSTRUCTION — measured 0 of 163 and 0 of 202 plants on two independent batteries — and this arm puts 46 of 174 / 66 of 260 plants there.** ⇒ the behaviour this leg predicts to change cannot already be in the target state, on either comparison. ⚠ And the OUTCOME claim is likewise not pre-satisfied: the parent's 52.90% is a DIFFERENT arm's cancelled partial tape, this arm's own share does not exist, and every band below — including a sign-reversed one — is a live, pre-named outcome.
**MAP SEGMENT: plank-EXPRESSIBLE maps — the 13 of 15 excluding the two CQ maps `antler` and `fjordgate` — mechanism reason: on maps of area ≤ 260 the d²20-100 annulus of the ENEMY core overlaps our own hunt band (`HUNT_BAND_DSQ = 41` of OUR core), so no tile satisfies both clauses of the siting predicate and ZERO shredders are planted in BOTH arms (measured, both arms, both batteries) — EXPECTED DIRECTION POSITIVE on the segment, EXACTLY ZERO on its complement.** This is ONE primary segment. The `CQ`/`STD`/`GRAND` split (`tools/overnight_read.py:76-94`) and the per-map table are **DESCRIPTIVE ONLY** and carry no pre-registered direction. ⚠ **THE COMPLEMENT IS THE FALSIFIABLE HALF AND IT IS WHAT MAKES THIS A TEST RATHER THAN A RESCUE HATCH: antler and fjordgate must read ~50% vs `_v468kladturbo`.** If either moves materially, the mechanism story is wrong — either the plank is expressible there after all, or something other than the plank is moving share. **Per OB15b/15c: the pooled bar is the bar; a pooled fail that clears on-segment RE-SCREENS as a NEW leg with its own n, never as a re-read of these rows.**
**EXPECTED DIRECTION: POSITIVE on the plank-expressible segment (13 maps), and EXACTLY ZERO — A/A — on its complement (antler, fjordgate).**
**SEGMENT VALUE CEILING: 86.67% of games × 4.33pp on-segment effect = 3.75pp pooled.** The share is the segment's pairing weight, 13 of 15 maps = 86.67% of a balanced shard; the on-segment effect is the value the projected pooled 53.75% implies once the two dead cells are removed. ⇒ **the dilution is a HARD CAP on what this fixture can pay: no on-segment effect can pool at more than 0.8667× itself, so a 1.33pp pooled margin needs 1.54pp on-segment, and the projected 3.75pp pooled needs 4.33pp on-segment.** *(royale is treated as EXPRESSIBLE here despite reading ~0 dose and 51.49% on the parent's tape; moving it to the complement would tighten the ceiling to 80.00% × 4.69pp = 3.75pp and is the conservative variant. It is NOT moved, because the registered segment must be fixed on a mechanism reason — area class — and royale is STD.)*
**POOL ERA: post-2026-08-13-rotation** — the 15-map local pool of `tools/overnight.sh:68`. (`check_pool_era` treats this as n/a on a LOCAL surface per SPEC §6; declared anyway so the population is on the page.)
**CELL VERSION CHURN: N/A — not a panel, no `CELLS:` line, one fixed local control tree.**
**GATE RESOLUTION: three gates, sized separately.**
* **(a) THE SHARE BAR.** Margin 1.33pp against a one-sample half-width of ±1.32pp at n=5,400, DEFF 0.98 — resolvable, and only just. ⚠ **The slack is 0.01pp, which is `GUNAXABL`'s exact failure mode: that arm missed its keep edge by 0.0152pp — ONE GAME — on a bar with zero constructed slack.** Registered consequence: **a result within one game of the bar is reported as "the fixture cannot resolve the question", not as a verdict in whichever direction the rounding falls.**
* **(b) THE r300 ADMISSION BAR.** RMST₃₀₀: MDE +5.0 rounds against half-width ±2.37 → resolves. Timely-kill: MDE 3.0pp against ±2.01pp → resolves. Both branches separated by construction.
* **(c) THE OPERATIONAL FLOORS.** The pinned `tools/auto_gate.py` marks CATASTROPHE@400 (CI-hi < 45.0, `:244,247`), MARK-1000 / TREND-FLOOR@1000 (prefix < 52.0, `:261`), COMBO-BAR@2700 (prefix < 55.0, `:278`) and the CI rule at MARK-2700 — all Magnus's confirmed constants. Their firings are **OPERATIONAL CANCELLATIONS** that free a core, typed `cancellation`, never `verdict`, licensing no exclusion claim beyond the CATASTROPHE carve-out in CUT-SHORT. **The floors now bind REMOTE too (`a50f27ef`, s48, via `tools/remote_cancel.py`), so the binding registration on this arm is not "LOCAL" but "SAME HOST" — one host, LOCAL by default; moving it is an amendment typed BEFORE the first row.** ⛔ **AND (c) IS THE GATE MOST LIKELY TO DECIDE THIS ARM'S FATE, at a probability computed in READ-BEFORE-RATIFYING #1 — 0.925 of cancellation at the projected true share.**
**Everything else on this page (F1, F2, F3, D3, D4, the seat / map / class splits) is DIAGNOSTIC and cannot rescue a failed bar. Any branch that does not resolve is UNRESOLVED, and an UNRESOLVED gate defaults to the RESTRICTION: no promotion, no ship conversation, no combination claim.**

---

## THE DOSE EVIDENCE — FIRINGS ONLY, NO EFFECT SIZES

**⛔ THIS SECTION IS BANKED MECHANISM EVIDENCE. IT CONTAINS NO OUTCOME NUMBER AND
MAY NOT BE USED AS ONE.** The batteries are small and unregistered; they
establish that the change FIRES and how, and nothing about whether it PAYS.

**Fixture: 360 games (180 per arm), seeds 930000-930005, the full 15-map local
pool, BOTH seats, `--tle 10`, treatment vs `bots/_v468kladturbo`.**

| quantity | parent (RND=25) | this arm (RND=10) |
|---|---|---|
| shredders / game | 1.122 (202) | **1.444 (260)** — **+28.7%** |
| games with ZERO shredders | 48.3% | **28.3%** |
| median plant round | 49.5 | **40.0** |
| plants in **r10-24** | **0 / 202** — unreachable BY CONSTRUCTION | **66 / 260 (25.4%)** |
| never fired a shot | 3.5% | 1.5% |
| planted-then-died | 21.8% | 18.8% |
| **shots / shredder** | 25.7 | **24.7 — FLAT** |
| per-map direction | — | rose on **10 of 15**, fell on 3, flat on 2 |

* **FLAG-OFF: 32/32 games byte-identical end-state vs the parent** (restore
  `LOKI_BELTBREAK_RND = 25` and this tree IS the parent — there is no new flag).
  ⭐ **WITH a flag-on positive control on the same fixture: 20/32 games
  NON-identical.** The positive control is the half that matters.
* **0 tracebacks in 360 games.**
* ⚠ **THE ONE NUMBER THAT DID NOT REPRODUCE, stated because the flattering
  version exists:** `shots/shredder` read 22.4 → 31.0 on an earlier seat-A-only
  120-game sweep and 25.7 → 24.7 (flat) here. **The +38% is seed-set noise; the
  honest claim is more shredders doing the same work.**
* ⚠ **THREE MAPS CANNOT EXPRESS THE PLANK AT ANY DOSE:** antler and fjordgate
  produce **0 shredders in BOTH arms** and royale ~0.
* ⚠ **LOCAL TIMELY-KILL READS DISAGREED IN DIRECTION ACROSS TWO SEED SETS AND
  NEITHER WAS POWERED.** At n=120 the r1000 share read 0.117 (parent) vs 0.150
  (this arm) and the treatment timely-kill rate 0.367 vs 0.300 — **both point the
  WRONG way**, both are inside noise at that n (±7pp and ±9pp), and both are
  **NON-MONOTONE across the four RND probes** (r1000: 25→.117, 15→.133, 10→.150,
  1→.125). ⇒ **NO kill-clock claim is licensed pre-hoc, in either direction. The
  shard's own D3/D4 read is the one that counts, and it is registered as a BAR
  above precisely because the local probe pointed against us.**
* ⛔ **TLE COULD NOT BE MEASURED LOCALLY AND THE LOCAL NUMBER IS UNINFORMATIVE,
  NOT ZERO.** `execTimeUs` / `tled` are absent from **100%** of local `BotOutput`
  events and `get_cpu_time_elapsed()` returned 0 on **all 22,289** local
  unit-turns — the s42 addendum's blind-zero, on the dimension that silently
  destroys units. The substitute was **wall-clock timing of `_dispatch`:
  unit-turns ≥ 10,000 µs went 0.097% → 0.045%.** That is a proxy on a different
  clock and is **labelled UNINFORMATIVE as a TLE claim.** The structural argument
  is what carries: the change is a comparison against a smaller integer inside a
  gate that already ran every round in both arms — **it adds no loop, no scan and
  no allocation**, and it moves work EARLIER rather than adding any. `--tle 10`
  caps a timeout engine-side. **If this arm is ever promoted toward a ship,
  `LOKI_BELTBREAK_LOG = True` is a ship-blocker to be turned off and re-screened**
  (it is identical in both arms here, so it cannot bias this screen — a statement
  about THIS CONTRAST, not about the shipped bot).

---

## SEGMENT AND POPULATION — the split, its n, and the dilution arithmetic

**Registered per-class n at the planned 5,400** (classes from
`tools/overnight_read.py:76-94 map_area_class`, computed at draft from each map's
own `.map26` header, never a hardcoded size table):

| class | area | maps | **n** | half-width at DEFF 0.98 | status |
|---|---|---|---:|---|---|
| **CQ** | ≤ 260 | antler, fjordgate | **720** | **±3.62pp** | **DIRECTION-ONLY** — and the registered prediction here is A/A |
| **STD** | 261-676 | archipelago, auroraveil, drumlin, frostgate, icefloe, nordkap, royale, yulerune | **2,880** | ±1.81pp | DIRECTION-ONLY (cannot resolve a 1.33pp margin) |
| **GRAND** | > 676 | drakkarfjord, glacierkeep, midgard, ragnarok, valkyrie | **1,800** | ±2.29pp | DIRECTION-ONLY |
| **PRIMARY SEGMENT** (expressible, 13 maps) | — | all but antler, fjordgate | **4,680** | **±1.42pp** | the one segment carrying a registered direction |

**⇒ EVERY size class is pre-labelled DIRECTION-ONLY: none of the three can
resolve the 1.33pp margin the pooled bar is built on.** Only the pooled read
(±1.32) and the primary segment (±1.42, marginal) can, and the primary segment's
own margin would have to be 1.42pp or better. **Registered consequence: no class
cell may be quoted as a verdict, and the 13-map segment cell is the ONLY
non-pooled cell with a pre-registered direction.**

**THE DILUTION ARITHMETIC, written out because it is a HARD CAP and not a
caveat.** Two of fifteen maps are A/A by construction (the plank plants nothing
in either arm). A balanced shard gives them **2/15 = 13.33% of all games**, so:

```
pooled_effect  =  0.8667 x on_segment_effect
=> to clear the pooled bar (needs +1.33pp over 50):  on-segment >= 1.54pp
=> the projected pooled +3.75pp requires:            on-segment  = 4.33pp
=> and the CEILING: no on-segment effect can pool above 0.8667x itself
```
**A third map, `royale`, reads ~0 dose and 51.49% on the parent's tape.** It is
NOT moved into the complement, because the segment must be fixed on a mechanism
reason (area class) rather than on an outcome; the **conservative variant** is
recorded here so a later reader can price it without re-choosing anything:
`3/15 = 20.00%` dead ⇒ `pooled = 0.8000 x on_segment`, needing **1.66pp**
on-segment to clear the bar.

⭐ **INDEPENDENT CORROBORATION OF THE DEAD CELLS, off a tape that is NOT this
arm's data** — `scratchpad/overnight/BELTBREAK-EARLY.tsv`, the parent's shard,
n=3,053, treatment share vs `_v468kladturbo` per map: **antler 50.00%,
fjordgate 50.49%, royale 51.49%** — the three flattest of fifteen — against
archipelago 68.63%, midgard 71.57%, drakkarfjord 62.25%. **The dose instrument
and the outcome tape agree about which cells are dead, and they are different
instruments.** ⚠ **Disclosed: the segment was chosen using the parent's data
plus the dose battery, so it is a PRIOR-INFORMED segment, not a blind one. The
prediction it makes about THIS arm's 5,400 rows is out-of-sample, which is what
OB15c requires; the choice itself is not.**

---

## FALSIFIER

**PRIMARY FALSIFIER: at n = 5,400 the 95% CI UPPER bound on this arm's pooled
share vs `bots/_v468kladturbo` falls BELOW 51.33.** That excludes the arm's own
bar.

**SECOND FALSIFIER (the r300 admission bar, and it can fail on its own while the
share passes):** the 95% CI UPPER bound on (treatment − control) ITT RMST₃₀₀
fails to EXCLUDE +5.0 rounds, **or** the CI LOWER bound on the ITT
timely-kill-by-r300 difference fails to EXCLUDE a fall of 3.0pp. **Either failure
is disqualifying on its own, regardless of the share** — `PLAY_DEFENCE:
not_at_the_kill_s_expense`, and this arm's scale-drag mechanism is why the bar is
carried on an offensive plank. Anchors from the parent's tape, quoted as
anchors and NOT as this arm's prediction: RMST₃₀₀ **T 268.39 vs C 271.53**
(treatment 3.13 rounds FASTER, paired sd 88.99); timely-kill **30.00%
[28.39, 31.61] vs 26.76% [25.21, 28.32]**, NON-OVERLAPPING, paired diff +3.24pp.

**SEGMENT FALSIFIER (the complement, and it is the clause that can surprise the
person running it):** **antler and fjordgate must read ~50% vs
`bots/_v468kladturbo`** — the mechanism says the plank plants nothing there in
either arm. **If either CQ cell moves materially away from 50 (outside its own
±3.62pp), the mechanism story is refuted even if the pooled bar clears:** either
the plank is expressible on CQ maps after all — in which case the dose
measurement is wrong — or something other than the plank is moving share, in
which case the attribution is wrong. **Registered handling: a pooled clearance
with a moving complement is reported as ATTRIBUTION UNRESOLVED and promotes
nothing.**

**MECHANISM FALSIFIER (independent of all of the above, and it fires FIRST):**
* if **F1** shows the treatment's forward gunner builds per game are not above
  the parent-configuration control's outside the tool's own band, **the change
  did not deliver its dose** and the share is **uninterpretable**: a flat share
  would mean "the mechanism never fired", not "the mechanism fired and did not
  pay". The primary is then reported as **NOT MEASURED**, not as a null;
* ⭐ **if F2 shows NO plant mass in r10-24 for the treatment, the ONE CONSTANT
  had no runtime effect and the shard ran two identically-behaving bots.** This
  is the specific wiring null this arm is exposed to, it is cheap to check, and
  it is not hypothetical: s47's delta D2 records a wiring null escaping demos to
  a 436-game shard. **A share near 50 with an empty r10-24 window is a WIRING
  NULL, not a finding about timing.**
* if **F3** shows the treatment's `get_scale_percent()` at fixed rounds is NOT
  above the control's, the registered scale-drag hazard did not materialise —
  which is a **good** outcome and must be reported as such rather than dropped.
Per FIRINGS-BEFORE-PRIMARY all three are read BEFORE the primary is typed.

### ⭐ THE HONEST-NULL CLAUSE — pre-committed, because this null would be genuinely informative

**Two null states, and they are NOT the same finding. The registered
discriminator is F1+F2, and it is read before the share.**

| state | evidence | pre-committed reading |
|---|---|---|
| **THE DOSE DID NOT LAND** | F1 flat, and/or F2 shows no r10-24 plant mass | **NOT MEASURED.** The leg says nothing about timing. The defect is wiring or funding, the road stays open, and the repair is a probe, not a verdict. |
| **THE DOSE LANDED AND DID NOT PAY** | F1 above band, F2 shows the r10-24 window populated at ~25% of plants, and the share is flat or negative | ⭐ **A REAL FINDING ABOUT THE PLANK, and it is bankable: the earliest plants are worth LESS than the scale tail they buy.** This prices the timing axis DOWNWARD from the parent's setting, i.e. **25 is at or past the optimum and the gradient is not monotone in the earlier direction** — which is a genuine surprise against the motivation in READ-BEFORE-RATIFYING #4 and must be written down before it is explained away. ⚠ **Attribution bound, per #5: it does NOT separate "early plants are low-value" from "early plants are fine and the earlier scale tail eats them".** Naming which requires a scale-neutralised arm, which this leg is not. |

**The dose evidence is strong and pre-measured, so the second row is the likely
null and it is pre-labelled INFORMATIVE.** That is the whole reason this arm is
worth a core if it is worth one at all.

---

## READING, PRE-COMMITTED

Registered now so no band is chosen after the fact. **Read TOP-DOWN; the first
row whose condition holds is the reading. Rows are disjoint by construction.**
**Every band below is CONDITIONAL on F1/F2/F3 having been read first and on the
r300 admission bar having HELD; an r300 failure overrides every row and the
reading is `OFF-PROGRAMME — kill delayed`, whatever the share.**

| # | band on this arm's pooled share vs `bots/_v468kladturbo` at n = 5,400 | pre-committed reading |
|---|---|---|
| **1** | **CI lower ≥ 51.33** | **THE EARLIER GATE ADDS.** Real and resolved on this fixture. Promotes to a combination input (`eco.py` is byte-identical to the control's, so the plank composes with the eco trio by construction) and to a separately-registered head-to-head. ⚠ Report the size with its OB16 status: this bar's MDE is 0, so this branch may claim "we can exclude 50 vs `_v468kladturbo`" and may NOT claim any minimum effect size. |
| **2** | **point ≥ 51.33 but CI lower < 51.33** (includes the whole [51.33, 52.4] window an A/A cell has already produced) | **REAL-BUT-SMALL, COMBINATION INPUT ONLY.** Pre-registered as WEAK: `NULL125`'s byte-identical A/A read 51.04, and the two A/A cells are 1.77pp apart. Rows are KEPT; no ship conversation; a replication on fresh seeds, same host, is the price of promoting it. |
| **3** | **point < 51.33 AND CI contains 50.0** | **PARITY — THE EARLIER GATE IS FREE.** 29% more forward gunners, their 20 Ti each, their +20% scale contributions each and their ammo draw all pay for themselves. Against the PARENT that is the informative sentence: **the dose is free but not profitable, so the timing axis is flat between 10 and 25 and the family's next iteration is ROTATION, not timing.** Does NOT license a ship. |
| **4** | **CI upper < 50.0** | **THE EARLIER GATE SUBTRACTS.** `RND = 10` dies as a ship candidate. Attribution is bounded: this refutes *the r10-24 plant window plus its funding shape plus its earlier scale tail*, **not** *the beltbreak plank* (whose own arm measured 52.90 vs the same control) and **not** *forward gunners in general*. **REGISTERED CONSEQUENCE: the gradient is NOT monotone in the earlier direction, the parent's 25 stands as the family's setting, and no further gate-lowering arm is written.** |

⚠ **Nothing here treats 50.0 as a floor.** A share below 50 is a live outcome
with named mechanisms (a +20% scale contribution per gunner bought ~10 rounds
earlier and 29% more of them; a 24-ammo magazine floor competing with the base's
own turret funding; a raider spending turns siting instead of sealing) and it is
pre-named so a negative is not explained away as noise.

⛔ **AND ONE CROSS-BAND NOTE, registered so it is not improvised: a COMBO-BAR@2700
cancellation reaches NONE of these rows.** Per READ-BEFORE-RATIFYING #1 it is an
operational stop on the CHASSIS TOTAL and the reading is
`CANCELLED — combination below the 55.0 prospecting bar; the 25→10 dose question
is UNRESOLVED and defaults to the RESTRICTION`.

---

## FIRINGS-BEFORE-PRIMARY — the reads, with exact invocations

**Measurability is declared per read. `NOT MEASURABLE` is written where it is
true, rather than a metric being quietly renamed into something the tape happens
to carry.** ⛔ **NOTHING BELOW READS OUR OWN `print()` OUTPUT. Every read is a
LOCAL replay decoded by our own decoder, or the LOCAL shard tape.** Platform
replays strip `stdout` (30,664 of 30,664 events, `CLAUDE.md`) and
`LOKI_BELTBREAK_LOG`'s prints are therefore useless off any platform surface;
they are also unnecessary here, since every quantity below is an engine-side
event.

### F1 — THE DOSE BATTERY. MEASURABLE, but NOT off the shard tape.
`tools/overnight.sh:138-139` passes `--replay /dev/null`, so the shard produces
**no** entity events. F1 runs on a **separate SERIAL battery**:
```
.venv/bin/python tools/dose.py bots/_v488beltbreak2 --kind gunner \
    --ctrl bots/_v480beltbreak --registered 60 \
    --keep scratchpad/bb2_replays \
    --tsv scratchpad/bb2_dose.tsv \
    --maps antler archipelago auroraveil drakkarfjord drumlin fjordgate \
           frostgate glacierkeep icefloe midgard nordkap ragnarok royale \
           valkyrie yulerune
```
**REGISTERED SIZE: 60 games** (15 maps × 2 seats × 2 seeds — `tools/dose.py:218-219`
takes `maps[(n//2) % len(maps)]` and plays both seats, so 60 is exactly balanced
on the live pool), **SERIAL** (never parallel: D65, a 16-game parallel dose check
once reported the OPPOSITE of a serial one and both were wrong).
**⛔ THE CONTROL FOR F1 IS THE PARENT `bots/_v480beltbreak`, NOT
`bots/_v468kladturbo`.** The dose question here is *did the 25→10 change add
plants*, not *does the plank exist*; the parent is the flag-restore control and
is the only comparison that isolates the constant.
**Pre-registered expectation: treatment `fwdbuild_gunner`/game strictly above the
parent's, with the paired difference outside the tool's own 2×SE band.**

**⛔ OB17 CHECKS PERFORMED AT DRAFT, INCLUDING THE ONE THAT COULD HAVE SURPRISED
ME.**
1. **EXECUTING TOOL NAMED:** `tools/dose.py` at HEAD `e0fb5d56`.
2. **THE PATHS EXIST IN THAT TOOL — checked, not assumed.** `--kind` is a free
   string keying `fwdbuild_{kind}` off the shipped decoder, so `gunner` is legal
   with no code change. `--keep DIR` exists (`:158-161`) and retains replays as
   `g<NNNN>_<map>_s<seed>_treatseat<0|1>.replay26`, which is what makes F2/F3
   executable at all — **this flag did NOT exist when the parent's prereg was
   written, and that prereg had to register S1 as a builder to-do.** `--registered
   N` exists and **stamps the registered n into every verdict line and reports
   shortfall against it**.
3. **⭐ THE CLAUSE THAT RETURNED AN ANSWER NOBODY HAD — and it found a live
   defect, which is exactly what this clause exists for. `tools/dose.py:77`'s
   default `MAPS` is the RETIRED 8-map set** (`antler atoll drumlin fjordgate
   heart hive meander nordkap`) — **four of those eight (atoll, heart, hive,
   meander) are NOT IN THE LIVE POOL.** ⇒ **an F1 invocation that omits `--maps`
   would silently measure the dose on half-retired geometry and print the same
   verdict vocabulary as a correct run.** **CONSEQUENCE OF SILENT
   NON-EXECUTION: the read would not fail — it would quietly measure a different
   population.** **ROUTED AROUND, NOT FIXED (per the standing instruction): the
   invocation above passes all 15 live maps explicitly.** Defect named in one
   line for the builder's queue: *`tools/dose.py:77` MAPS default is the pre-
   2026-08-13 pool; every registered dose read must pass `--maps` explicitly.*
4. **A SECOND CONSEQUENCE, registered:** `tools/dose.py` walks its OWN seeds from
   1 (`:212, seed += 1`), so this battery consumes **none** of the shard's
   registered seed base and cannot collide with it.
5. **AND ONE DECODER FACT THAT WOULD HAVE INFLATED F1 ~3×, named because this
   plank rotates:** `rotate()` re-emits `placeEntity` for an existing entity.
   `tools/corpus/replay_events.py:16,113` guards it — a build is the FIRST
   `placeEntity` carrying an id — and `dose.py` uses that shipped decoder. **The
   guard is present; recorded as a check that came out clean rather than as
   absent.**
⭐ **REGISTERED-SIZE SHORTFALL RULE, pre-committed:** if the battery runs short,
the readout states the shortfall factor, and **a `DOSE DELIVERED` verdict whose
|paired diff| clears its own band by less than 2× on a short battery is
UNRESOLVED** — which defaults to the restriction and means the primary is typed
with the mechanism unverified.

### F2 — THE PLANT-ROUND AND ANNULUS READ. THIS IS THE WIRING CHECK. MEASURABLE off F1's retained replays.
```
.venv/bin/python tools/corpus/replay_events.py scratchpad/bb2_events.tsv \
    scratchpad/bb2_replays/*.replay26
# rows with ev == BUILD and kind == gunner, grouped by team:
#   (a) histogram rnd      -> THE PLANT-ROUND READ.  The r10-24 bucket is the
#                             whole point: it must be POPULATED for the
#                             treatment and EMPTY for the parent control.
#   (b) histogram d2_enemy -> the annulus read (siting unchanged between arms)
#   (c) median plant round per arm  -> expect ~40 vs ~49.5
```
`replay_events.py:157` emits `file ev rnd team kind x y d2_own d2_enemy mw mh`,
so (a), (b) and (c) are all one grouping away.
**Pre-registered expectations, both directional:**
* **(a) is the CONSTANT'S RUNTIME EFFECT and is the third mechanism falsifier:**
  treatment gunner-BUILD rounds must include mass in **r10-24** where the parent
  control has **none**, and the treatment's median plant round must sit **below**
  the parent's.
* **(b)** both arms' gunner-build `d2_enemy` mass sits predominantly in the
  20-100 band — **this arm changes siting NOT AT ALL, so a difference here is an
  INSTRUMENT ALARM, not a finding.**
⚠ **THE EXACT NUMERIC CUT FOR (b) IS DELIBERATELY NOT ASSERTED AT LOCK:**
`replay_events.py:95-96,113` measures d² to a **single core anchor position**
while the bot's `dsq_core` measures to the **nearest tile of the 2×2 footprint**,
so a plant the bot scored at d²=20 can decode a few units higher. **The band
edges are read with an explicit tolerance and the cut is CALIBRATED FROM THE
CONTROL ARM'S OWN DISTRIBUTION at readout** — a control-derived quantity that
cannot be tuned toward a verdict. **The DIRECTION is registered; only the cut
point is deferred.**

### F3 — THE SCALE-DRAG READ. MEASURABLE off the same retained replays; the registered hazard's metric.
The named hazard of READ-BEFORE-RATIFYING #5 gets a number rather than a
sentence. Off `scratchpad/bb2_replays`, per arm:
```
#   (a) count of friendly GUNNER/SENTINEL/HARVESTER/CONVEYOR BUILD events with
#       rnd <= 60, treatment vs parent-control  -> the earlier-purchase count
#   (b) cumulative additive scale contribution implied by all BUILD events with
#       rnd <= 60  (gunner/sentinel/builder +20, harvester +5, launcher +10,
#       conveyor/splitter/barrier +1, per CLAUDE.md's engine-confirmed table)
#   (c) harvester count at r25 and r40, treatment vs parent-control
```
**Pre-registered expectation, and it is a HAZARD read so the direction that
worries us is the one predicted:** (b) is **HIGHER** for the treatment by
r40-r60 — that is the drag, and the leg's job is to show the share pays for it.
**(c) is the economy-unharmed check** (the parent's demo read 3.31 vs 3.06
harvesters at r25 against `_v468kladturbo`, i.e. no early economy damage; the
same must hold for this arm against the PARENT). ⛔ **A FALL in (c) for the
treatment is a named negative and is reported as one, not folded into the share.**
⚠ **NOT MEASURABLE on this surface: the actual `get_scale_percent()` value.**
The decoded event stream carries BUILD events, not the engine's scale counter, so
(b) is a **RECONSTRUCTION from the engine-confirmed additive table**, not a read
of the engine's own field. **Labelled as a reconstruction; it is admissible
because the table is engine-confirmed (`bots/_probe_scale`, s26: observed ==
floor(scale × base) for all 8 entity types in every round), and it is the closest
executable form of the hazard's metric.**

### D3, D4 — the outcome-shape reads. MEASURABLE, shard-native.
`cond` and `turns` are on the tape.
* **D3 — THE r300 ADMISSION BAR (see `KILL-ROUND NON-REGRESSION`).** ITT RMST₃₀₀
  per side over all 5,400 rows, plus the ITT timely-kill-by-r300 rate per side,
  plus the kill-win-conditioned share and conditioned median as DIAGNOSTICS.
  Both bars scored as exclusions off `tools/cluster_ci.py --null`.
* **D4 — COND MIX**, the share of games ending `core_destroyed` / `tiebreak` /
  `NOWINNER`, per arm, and the **median kill round** as the gross backstop
  (median crossing 300 is disqualifying). Anchors from the parent's tape:
  `core_destroyed` 2,692 / `tiebreak` 361 of 3,053; median kill round 244.5 for
  the treatment's kill-wins. **`R1000_IS_DEFEAT` makes a tiebreak share a cost
  even when the tiebreak is won, and a shredder plank is exactly the family that
  could trade kills for an economic grind** — the local n=120 probe's r1000 share
  moving 0.117 → 0.150 is the unpowered signal that makes this a registered read
  rather than a formality.

### NOT MEASURABLE on this leg — named, not silently dropped.
* **PLANTS PER GAME, PLANT ROUND, ANNULUS SITING AND GUNNER LIFESPAN ARE NOT
  DECODABLE OFF THE SHARD.** `tools/overnight.sh:138-139` runs `--replay
  /dev/null`: **local corefill keeps TAPES, not REPLAYS.** The tape can carry
  share, kill round, `cond` mix and D3's rates, **and nothing else.** ⇒ **every
  mechanism number in this leg comes from the SEPARATE F1/F2/F3 batteries, and
  the shard's n = 5,400 lends them none of its power.** Anyone quoting a plant
  count "from the BELTBREAK2 shard" is quoting something that does not exist.
* **WHAT A PLANTED GUNNER WAS AIMED AT, AND WHETHER ITS ROTATION WAS USED.**
  Facing is not in the decoded event stream (research's own stated limit). The
  rotation half of Magnus's directive is UNOBSERVED by this leg by construction —
  it is the named NEXT axis, and its registered hazard is `GUNPIN`'s rotate-thrash
  negative (44.27 vs `_v468kladturbo`).
* **BELT-KILL ATTRIBUTION AT SHOT LEVEL.** The parent's demo did this off retained
  replays with jitter controls (122 fire events → 40 → 0 under three controls);
  **this shard cannot**, and a Band-3 "free" result and an "expensive ornament"
  result are NOT separable off the tape.
* **PER-UNIT CPU / TLE.** See the DOSE-EVIDENCE bullet: local replays carry no
  exec-time fields at all, so the local number is a **blind zero** and is
  labelled UNINFORMATIVE rather than clean.
* **SEED DETERMINISM.** `NOISE_ON` pins an unseeded RNG, so base-vs-base at one
  seed diverges at round 0. **No seed-matched or replay-diff equivalence claim is
  available on this fixture; the flag-restore equivalence claim is made on the
  CODE plus the 32/32 flag-off battery with its 20/32 positive control, never on
  a replay comparison of shard games.**

---

## THE CHANGE — `file:line`, parent → treatment

**TREATMENT TREE: `bots/_v488beltbreak2`** = `bots/_v480beltbreak` plus **ONE
EXECUTABLE LINE**. Verified at draft, and re-runnable in two commands:

```
$ cmp bots/_v480beltbreak/eco.py  bots/_v488beltbreak2/eco.py   # clean
$ cmp bots/_v480beltbreak/main.py bots/_v488beltbreak2/main.py  # clean
$ cmp bots/_v480beltbreak/raid.py bots/_v488beltbreak2/raid.py  # clean
$ diff bots/_v480beltbreak/doctrine.py bots/_v488beltbreak2/doctrine.py \
      | grep -E '^[<>]' | grep -vE '^[<>] *(#| *$)'
< LOKI_BELTBREAK_RND = 25         # EARLY arm: plant gate opens at this round
> LOKI_BELTBREAK_RND = 10         # EARLY arm: plant gate opens at this round.
```
⇒ **ONE non-comment changed line, at `bots/_v488beltbreak2/doctrine.py:1439`.**
The rest of the `doctrine.py` diff is an **88-line comment block** (`:1350-1437`)
recording the build agent's dose measurements, the three rejected axes, the
saturation argument for 10-over-1, and the TW-hazard direction. **`eco.py`,
`main.py` and `raid.py` are BYTE-IDENTICAL to the parent's, `cmp` clean.**

**THE READ SITE, and it is exactly one:** `bots/_v488beltbreak2/raid.py:882-884`
```python
        rnd = ct.get_current_round()
        # THE TIMING GATE -- the entire difference between the two arms.
        if rnd < (LOKI_BELTBREAK_RND if LOKI_BELTBREAK_EARLY
                  else LOKI_BELTBREAK_LATE_RND):
            return self._bb_refuse("EARLY")
```
This sits **inside the BELTBREAK shredder ladder** (`_try_beltbreak_gunner`,
`raid.py:847-1017`), whose gate order is: band pre-scan (silent) → **round gate
`:882`** → harvester gate `:885` → LIVE CENSUS cap `:888-890` → funding
`:904-907` → live-target scan → siting ladder → own-ray walk → `build_gunner`
`:1009` → heartbeat write. ⛔ **IT IS NOT ON THE FORWARD-SENTINEL PATH**
(`raid.py:688 tiles = core_tiles(E)` plus the `d² ≤ 32` filter), which builds
SENTINELs only, uses a different counter (`SLOT_FWD_GUN`) and is untouched by
this arm. `grep -n 'LOKI_BELTBREAK_RND' bots/_v488beltbreak2/raid.py` → **one
hit, `:882`.**

**⭐ THE CAP HAZARD THIS PLANK STILL ROUTES AROUND, unchanged from the parent and
worth a certifier's minute:** `LOKI_FWD_GUN_CAP` counts `SLOT_FWD_GUN`, written
only as `read + 1` and never decremented — **it counts RUBBLE**, so three dead
forward turrets close that arm for the match. **BELTBREAK does not touch that
counter**; its cap is a LIVE CENSUS of friendly GUNNERs in the annulus
(`_live_beltbreak_guns`), and `_live_fwd_guns` counts only SENTINELs. **The two
arms share no counter and no store slot** (`SLOT_BELTBREAK = 13`).

---

## THE TW HAZARD — REGISTERED AS CHECKED, WITH THE DIRECTION ARGUED

**The hazard:** x3r0's Odin carries a weapon **gated on never having seen one of
our turrets**. An arm that DELAYS our first visible turret re-enables it. This is
a live opponent capability, not a hypothetical, and it is the reason the check is
on the page.

**THE DIRECTION IS SAFE, and here is the argument rather than the assertion.**
The gate this arm moves is an **OPENING** round on a **FORWARD TURRET PURCHASE**.
Lowering it can only make the first beltbreak gunner appear **at the same round
or earlier**, never later — the gate is a `rnd <` refusal and 10 < 25, so every
round in which the parent could plant is a round in which this arm can also
plant, plus fifteen more. **Measured, not only argued: median first-plant round
49.5 → 40.0, and 26.4% of plants now land BEFORE r25 where the parent had zero.**
⇒ **first visible forward turret strictly EARLIER = the safe direction.**
**AND THE CONVERSE CASE IS ON THE RECORD, which is what makes this a check rather
than a reassurance: the LATE twin (`RND = 70`, `bots/_v483beltbreaklate`) moved
the same quantity the UNSAFE way and floor-stopped at 47.39.** ⚠ **SCOPE, so this
is not over-read: the check is that this arm does not RE-ENABLE the weapon. It is
NOT a claim that the arm defeats it — that would need a live leg against Odin,
which nothing on this page touches.**

---

## SEEDS

**SEED BASE: 840000.** Registered worklist row (**to be appended by the builder,
not by this agent**):
```
BELTBREAK2 bots/_v488beltbreak2 bots/_v468kladturbo 5400 840000
```
**FREENESS, verified at draft on four surfaces, with a POSITIVE CONTROL RUN
FIRST so the check has been seen to produce the other verdict:**
* **POSITIVE CONTROL: `grep -c '826000' scratchpad/corefill_work.txt` → 1**, the
  `ODINVSSLEIP` row. **The grep HITS when it should hit.**
* `grep -c '840000' scratchpad/corefill_work.txt` → **0**;
  `scratchpad/fleet_queue.tsv` → **0**;
  `grep -l '840000' scratchpad/overnight/*.tsv` → **no file**.
* `grep -l '840000' docs/prereg/*.md` → **one file,
  `docs/prereg/PREREG-OPENFAST-2026-08-17.md`** — ⛔ **and that hit is a
  FRESHNESS-CHECK LINE, NOT A REGISTRATION.** `PREREG-OPENFAST:314` records
  *"`grep -n '836000|838000|840000' …` → no match on any of the four surfaces"*,
  and OPENFAST's registered base is **836000** (`:309-311`). **A naive
  grep-for-collisions returns a false positive on any prereg that verified its
  own seed freeness — named here so no successor re-derives it as a conflict.**
* **Same-day drafts enumerated per file, not assumed:** 828000 (`KLADLADDER2`),
  830000 (`KLADLADDER3`), 832000 (`SEALPIERCE`), 834000 (`ECOMMIT2`), 836000
  (`OPENFAST`). **840000 is the next free base at the 2000-wide stride this
  family uses.**
* ⭐ **AND THE OVERLAP CONCERN `PREREG-OPENFAST:317` RAISED AND EXPLICITLY
  REFUSED TO BLESS IS NOW RESOLVED, BY READING THE RUNNER RATHER THAN ASSUMING
  IT.** OPENFAST worried that a 5,400-game shard at a 2,000-wide stride would
  overlap the next row's base. **`tools/overnight.sh:124` is
  `seed=$(( SEEDLO + n / 16 ))`** — sixteen games per seed — so **a 5,400-game
  shard consumes 338 distinct seeds, not 5,400.** OPENFAST at 836000 uses
  836000-836337; BELTBREAK2 at 840000 uses **840000-840337**. **No overlap, with
  1,662 seeds of headroom, and the stride is ~6× larger than it needs to be.**
* ⛔ **THE BUILD AGENT'S DEMO SEEDS 930000-930005 ARE DELIBERATELY EXCLUDED from
  the screen.** They are the fixture the dose was measured on; reusing them would
  screen the arm on the seeds that selected it.

---

## AMENDMENTS

**ADD-ONLY, and blind to the data.** Any amendment to this document is a NEW
dated section appended below this line, never an edit to anything above it; it
must be typed and committed BEFORE the number it could bear on exists, and it
must say what it is blind to. An amendment that removes, weakens or re-words a
registered bar, falsifier, band, segment or MDE is not an amendment — it is a new
pre-registration and needs a new leg. *(`tools/prereg_check.py --amendment
<locked.md> <amended.md>` is the checkable form.)*
**Pooling extra rows into this shard after lock is an unregistered n increase —
optional stopping with extra steps — and is prohibited. A replication on fresh
seeds is reported SEPARATELY and NEVER pooled** (the GUNAXABL/SENTTHR precedent:
remote replications corroborated a null they were not allowed to rescue).

---

## WHAT THIS LEG COSTS AND WHAT IT DOES NOT

**Cost: one LOCAL core to n = 5,400, plus 60 serial games for F1 and the replay
decode for F2/F3.** ZERO rated ladder exposure, zero submissions, zero unrated
challenges — nothing on this page touches the platform, which is why `TARGET
BAND` is N/A rather than a number. **⚠ AND THE EXPECTED VALUE OF THAT CORE IS
DOMINATED BY READ-BEFORE-RATIFYING #1: at the projected true share the arm
reaches its own registered n with probability 0.075.** The 2,700-prefix
cancellation is not a failure mode of this design — it is the design working as
Magnus specified it — but **it means the core most likely buys a
`cancellation` row and the F1/F2/F3 mechanism reads, not a bar verdict.** That
trade is the builder's to make and the number is here so it is made with eyes
open.

**It does NOT decide a ship.** The strongest branch promotes the arm to (a) a
combination input — and the disjointness is verified, not assumed: **`eco.py` is
byte-identical to the control's**, so this plank composes with the eco trio by
construction — and (b) a separately-registered head-to-head against the live
holder, which is the pipeline step Magnus's procedure names verbatim (*"we start
by testing it against the current slot, if it beats it we can switch"*). **A
local screen against our own shipped bot is gate 1; gate-1-to-gate-2
transitivity is UNVALIDATED in this repo (QUEUE #65: 3 concordant, 1 not), so the
head-to-head is not skippable on the strength of this number.** And
`SLOT_STOP_LOSS: off` plus the parked SWITCH step of `X3R0_SLOT_RULE` mean
**the slot changes only on Magnus's explicit word**, whatever this leg returns.

**⚠ ONE KNOWN PREFLIGHT FAIL, NAMED AND NOT FIXED:**
`.venv/bin/python tools/preflight.py bots/_v488beltbreak2` FAILs on *"no
PREREG.md or README.md"*. **The parent `bots/_v480beltbreak` has neither either,
so this is not a regression introduced by this arm** — it is a standing property
of every tree in this family. Reported in one line; not fixed by this agent.

---

**PROVENANCE:** `docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md` (read IN FULL: OB7, OB8, OB10, OB11, OB12 + its pre-committed restriction default, OB13, OB14, OB15a/b/c + the segment vocabulary and the units rider, OB16 + its `BAR = null + MDE + half_width` amendment, its zero-MDE corollary and its cross-host rider, OB17 + its "run the clause that can surprise you" rider, and the **2026-08-17T07:24:55Z addendum** that replaced the local-shard clock-2 boilerplate — quoted rather than restated) · `PROGRAMME.md` (parsed block `:6-30` — `INCUMBENT: bots/_v468kladturbo`, `PRIMARY_CURRENCY: game_share`, `WIN_RATE_IS_VERDICT: yes`, `KILL_WINDOW_RND: 250`, `R1000_IS_DEFEAT: yes`, `PLAY_DEFENCE: not_at_the_kill_s_expense`, `DEFENCE_ADMISSION_BAR: r300_crossing_non_regression`, `SLOT_STOP_LOSS: off`, `X3R0_SLOT_RULE`; the `:488-564` r300 re-pricing chain in full — the 05:15:45Z re-pricing, the 05:19:38Z collider correction, the 05:3xZ arbitration freeze, and the **05:36:10Z ITT RMST₃₀₀ resolution with its vintage rule**, which is why this page registers RMST₃₀₀ as the operational estimator alongside the ITT timely-kill rate) · `docs/prereg/PREREG-BELTBREAK-EARLY-2026-08-17.md` (**the PARENT arm's prereg, read IN FULL** — its structure, token order, registered machinery and caveat set are inherited here where they still apply; its EARLY-vs-LATE contrast is NOT, per READ-BEFORE-RATIFYING #3) · `docs/prereg/PREREG-BELTBREAK-LATE-2026-08-17.md` (cited only for the fact of its cancellation) · `docs/research/REPLAY-STUDY-offensive-gunner-2026-08-17.md` (§3.6 the productive annulus and its 3,662-gunner core-share-0.000 identity; §3.7 the timing refusal, the p10/median/p90 table including ph r9 / O(1) r14 and our own version-stable r56-85; §5.1 the control's missing forward-gunner path; §6 the ammo arithmetic making the gunner the right turret for a 20-HP tile; §7.1 the `EARLY = r ≤ 25` spec definition this arm extrapolates past; §7.2 placement) · `docs/research/FORWARD-ARRIVAL-BASELINE-2026-08-16.md` (median forward arrival r31, via the parent prereg's quotation) · `docs/prereg/BARS.tsv` (**header/format ONLY, incl. the FIRINGS-BEFORE-PRIMARY rule of 2026-08-16T13:27:33Z, the `le`-direction never-stop carve-out, and the sibling `BELTBREAK-EARLY` / `BELTBREAK-LATE` / `ROUTESCORE` / `ODINVSSLEIP` rows for bar comparability — `grep -c COMBO-BAR-EXEMPT` → 0. NO ROW WAS ADDED BY THIS AGENT**) · `CLAUDE.md` (the ONE GLOBAL ADDITIVE cost-scale factor and its engine confirmation via `bots/_probe_scale` s26; the DEFF scope procedure and its direction clause; the local 0.98 exemption; the `print()`-stripped-from-platform-replays ruling, which is why no read on this page touches our own stdout; `R1000_IS_DEFEAT`; the r300 bar's operational form) · `bots/_v488beltbreak2/{doctrine,eco,main,raid}.py` (read at draft: `doctrine.py:1350-1460` the new comment block and all eleven constants, `raid.py:875-900` the gate, `:989` and `:1009` the build calls, `:64` the `from doctrine import *` binding) · `bots/_v480beltbreak/{doctrine,eco,main,raid}.py` (the parent, `cmp`'d file-by-file) · `bots/_v468kladturbo/doctrine.py:1879` (the `stack.py` compose marker every arm on this chassis inherits) · `scratchpad/overnight/BELTBREAK-EARLY.tsv` (the parent's tape, n=3,053 non-`#` rows: pooled share 52.90% recomputed at draft, the per-map table quoted in SEGMENT AND POPULATION, the ITT timely-kill pair and its paired sd, the ITT RMST₃₀₀ pair and its paired sd, the `cond` mix, and the `# FIXTURE … start=2026-08-17T05:59:07Z` header) · `scratchpad/overnight/BELTBREAK-LATE.tsv` (row count only) · `scratchpad/auto_gate_cancelled.tsv` (`:79-80` the LATE floor stop, `:83-84` the EARLY COMBO-BAR stop) · `results.tsv` (rows `beltbreak-late-autostop-1000`, `beltbreak-late-final`, `beltbreak-early-autostop-2700`, `idnull140-cert-5400`, `null125-final`, `kladturbo-local-confirm-5400`, `kladladder-n-final-correction`, `kladladder-verdict-amendment-f1f2-pending`) · `tools/prereg_check.py` (read for `KNOWN_KEYS`, `key_pattern`/`field`, `first_number`/`raw_number`/`int_before` incl. the s48 comma fix, `RULES` in full, `check_presence`, `check_arithmetic`, `untracked_arm_paths`, `git_diff_paths`, `ROUND_GATE_RE`, `_inert`, `check_metric_window`, `check_pool_era`, `DEFF`/`CLUSTER_SYNONYM`, and the `_defence_bar_ok` predicate that enforces the r300 form) · `tools/auto_gate.py` (`:244-247` `MARK_CATASTROPHE`/`MARK_MID`/`MARK_HALF`/`CATASTROPHE_CI_HI`, `:261` `TREND_FLOOR = 52.0`, `:278` `COMBO_BAR = 55.0`, `:715-742` `combo_of` and its read of the TREATMENT tree's `doctrine.py`, `:902-960` the clause order and the COMBO-BAR-EXEMPT citation guard) · `tools/overnight.sh` (`:57-68` the live 15-map pool, `:99-103` the `START=` / `# FIXTURE` stamp, `:124` the `SEEDLO + n/16` seed walk that resolves the OPENFAST overlap question, `:138-139` `--replay /dev/null --tle 10`) · `tools/overnight_read.py` (`:76-94` `map_area_class`, run at draft to classify all 15 live maps; `:97-106` `live_pool`) · `tools/dose.py` (`--help` read in full; `:77` the RETIRED default MAPS defect routed around, `:134-172` the argparse incl. `--registered`/`--keep`/`--maps`/`--tsv` and the no-default refusal, `:175-200` the CLASS B gate, `:212-219` the seed walk and map/seat rotation, `:250-262` the `--keep` retain-and-name path) · `tools/corpus/replay_events.py` (`:16,113` the rotation guard, `:95-96` the core anchor convention, `:157` the output columns) · `tools/cluster_ci.py` (`--help` read; `--null` is the exclusion-restatement path the r300 bars use) · `tools/control_pin.py` and `scratchpad/CONTROL_PIN` (the quoted digest) · `tools/preflight.py` (run at draft; the named FAIL) · `scratchpad/corefill_work.txt` (the row format and the tail rows establishing the 812000-826000 seed sequence) · `scratchpad/fleet_queue.tsv` (seed freeness) · `docs/prereg/PREREG-OPENFAST-2026-08-17.md` (`:309-317` its seed registration and the overlap question it refused to bless) · `docs/prereg/PREREG-KLADLADDER2/3`, `PREREG-SEALPIERCE`, `PREREG-ECOMMIT2` (seed-base enumeration only) · git `e0fb5d56` (HEAD at draft), `git status --porcelain`, `git ls-files` and `git log` output quoted above · the drafting brief supplied by the builder lane s49. **No file under `bots/`, `tools/`, `scratchpad/`, `docs/prereg/BARS.tsv`, `results.tsv`, `HANDOVER.md`, `PROGRAMME.md` or `QUEUE.md` was created or modified by this agent, and no game was run. The only write was this document.**
