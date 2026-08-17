# SCREEN PREREG — `BELTBREAK-EARLY`: the forward economy-shredder GUNNER, planted in the EXECUTOR BAND (gate opens r25)

Drafted by a fresh opus subagent with no inherited session context beyond the
inputs listed under `PROVENANCE`. The builder lane ratifies the judgment lines
and types the lock commit; this agent wrote no code under `bots/`, appended no
worklist row, appended no `BARS.tsv` row, fired no game, started no shard, and
touched neither `results.tsv` nor `HANDOVER.md` nor `PROGRAMME.md` nor
`QUEUE.md`.

**STATUS: drafted BEFORE the `BELTBREAK-EARLY` row is appended to
`scratchpad/corefill_work.txt`, BEFORE any file named
`scratchpad/overnight/BELTBREAK*` exists, and BEFORE the leg's first game.**
Drafting session wall clock at write time **`2026-08-17T05:43:29Z`** (`date -u`,
same shell call); repo HEAD at draft `7929838d` (author time
`2026-08-17T07:43:08+02:00`). Verified at draft:
`grep -c BELTBREAK scratchpad/corefill_work.txt` → **0**;
same grep on `docs/prereg/BARS.tsv` → **0**;
`ls scratchpad/overnight/ | grep -i belt` → **0 files**;
`grep -cE '81[68]000|82[0-9]000' scratchpad/corefill_work.txt` → **0** (the seed
base is free; the last two rows used 812000 and 814000).

### SECOND CLOCK
`tools/overnight.sh:99` sets `START=$(date -u …)` and **`:103` writes
`# FIXTURE\tshard=…\tstart=$START\trunner=tools/overnight.sh` as the tape's first
line, before the first `fcode run`**, on any tape that does not already exist.
⇒ **PRIMARY second clock: the lock commit's git author time against the
`BELTBREAK-EARLY.tsv` `# FIXTURE … start=` stamp** (a START, not a
first-completed-row).
**BACKSTOP, registered now so no judgement is made later:** if the tape instead
carries `# FIXTURE-RESUME … start=UNKNOWN-legacy-tape` (`:110`) or no `# FIXTURE`
line at all, the second clock is **the `ts` of the FIRST COMPLETED ROW** —
conservative, because the true start is strictly earlier, so the gap can only be
OVERSTATED, never understated. *(The stamp exists on LOCAL tapes and on 0 of 84
remote ones — the other half of why this shard is registered LOCAL.)*

### ⚠ COMMIT PROVENANCE OF THE TREATMENT TREE — READ THIS, IT IS NOT THE OBVIOUS ONE
`bots/_v480beltbreak` **already exists and is committed.** The builder's record
commit is **`cbf67e5d`** (author time `2026-08-17T07:37:08+02:00`,
*"BUILDER s48: BELTBREAK — bots/_v480beltbreak, the forward economy-shredder
gunner the tree could not express"*) — **but `git show --stat cbf67e5d` names only
four deleted `__pycache__` blobs.** The four `.py` files first reached HEAD in
**`7bcf0e5e`** (`07:35:55+02:00`, a SIDE-LANE `git commit -a` sweep that ran
mid-demo) with the pycache dragged in by **`78f0d06b`** (`07:36:46+02:00`).
**This is a commit-hygiene near-miss the builder flagged on the coordination tape
at 05:38:51Z, not a content question:** every file is **sha1-identical between
`cbf67e5d` and the working tree**, verified at draft
(`raid.py 49b5834279d0…`, `doctrine.py 7b01697f4a2b…`). ⇒ **`cbf67e5d` is cited as
the record; `7bcf0e5e` is cited as the diff ref, because that is the commit whose
diff actually contains the tree.** A certifier grepping `cbf67e5d`'s diff for
`raid.py` will find nothing, and would be right to stop — this paragraph is why
they should not.

**This document is therefore NOT locked before the arm exists, only before the
arm's first screen row.** Said here rather than left for a certifier to find.

---

## ⛔ READ BEFORE RATIFYING — SEVEN THINGS THE LANE OWNS

**1. THIS ARM'S OWN BAR IS THE SECONDARY. THE REGISTERED PRIMARY OF THE PAIR IS
THE TIMING CONTRAST.** `BELTBREAK-EARLY` and
`docs/prereg/PREREG-BELTBREAK-LATE-2026-08-17.md` are a ONE-CONSTANT pair, and
**Δ = p̂(EARLY) − p̂(LATE)** is the quantity no other leg can produce. Both
documents register the same Δ, the same ±1.87pp half-width and the same four
bands; the contrast sentence is typed ONCE, off both tapes, and belongs to
neither arm alone.

**2. THE CONTROL IS THE LIVE INCUMBENT, SO 50.0 MEANS "ADDS NOTHING".**
`bots/_v468kladturbo` is Sleipnir v1, pinned as the corefill control at
`scratchpad/CONTROL_PIN` (`a9228ccb56ed9a65dd7d72ad1cb96068 bots/_v468kladturbo`;
the digest is produced by `tools/control_pin.py` and is quoted, not re-derived by
hand here). **Every share on this page carries its control inline —
`X% vs _v468kladturbo` — and that notation is mandatory, not decorative:** three
different 60s are live in this repo (the slot rule's 60±2-vs-v140, yesterday's
61.57-vs-v140, and Magnus's target of 60-vs-Sleipnir) and they differ by ~9pp
through the logistic. A reader who transplants a 61-shaped intuition from the
KLADTURBO-vs-v140 read onto this page has misread the fixture: **the same bot
measured against itself reads 50.0 vs `_v468kladturbo`.**

**3. ⛔ THIS IS NOT A SYMMETRIC EARLY-VS-LATE COMPARISON, AND FRAMING IT AS ONE
WOULD MISDESCRIBE WHAT IS BEING TESTED.** The LATE arm's gate round, **r70, is OUR
OWN HISTORICAL MEDIAN first in-band plant** (`docs/research/REPLAY-STUDY-offensive-gunner-2026-08-17.md`
§3.7: OpenSverige r56-85 in **every** version cell, version-STABLE, against a
field median of r37 and the best executors at r13-33). ⇒ **the registered contrast
is "THE EXECUTOR BAND vs WHAT WE ALREADY DO"**, not "early vs late" as two
arbitrary settings. **EARLY is the treatment; LATE is the incumbent timing
re-expressed inside the new plank so that the timing axis is isolated from the
plank itself.**

**4. ⛔⛔ TIMING IS THE TREATMENT *BY DESIGN*, BECAUSE THE ARCHIVE REFUSED TO PRICE
IT — AND THAT REFUSAL IS THE REASON THIS CONTRAST EXISTS.** It is cited here as
the identification argument, not as background:
* `REPLAY-STUDY-offensive-gunner-2026-08-17.md` §3.7, on 774 team-games restricted
  to 150-400 rounds: **win share by CUT COUNT is strongly monotone (0.44 → 0.90);
  win share by FIRST-CUT ROUND runs the WRONG WAY (0.72 at <r40 → 0.85 at r150+)
  and stays flat-to-reverse inside cut-count strata.** Both are hopelessly
  confounded — a losing team does not get to plant deep at r250, and a game you
  are winning lasts long enough to accumulate cuts.
* **Research's two archive designs disagreed IN SIGN on the same quantity, and
  this study's independent pipeline disagrees with the prediction's sign too.
  Three instruments, three refusals.** No natural experiment exists in the sample:
  plant round is not forced by spawn geometry in any isolable subset.
⇒ **The study's own conclusion is the design of this pair, verbatim: *"Timing is a
treatment to register in a leg, not a parameter to read off the archive."*** A
registered manipulation with a randomised seat/map fixture is the ONLY clean
instrument available for this question, which is why the pair is worth two cores.

**5. ⭐⭐ THE SCALE ASYMMETRY IS A REGISTERED READING SENTENCE, NOT A CAVEAT ADDED
AFTERWARDS. THE EARLY ARM CARRIES ITS OWN HANDICAP BY CONSTRUCTION.**
Cost scale is **ONE GLOBAL ADDITIVE team factor**: every build adds to it and it
inflates the cost of every subsequent build of every type (`CLAUDE.md`, engine-
confirmed s26). A gunner is **+20%**. ⇒ **the EARLY arm buys that +20% at r25 and
pays it across the whole remaining game; the LATE arm buys the identical +20% at
r70 and pays it across a shorter tail.** The two arms are NOT equal-cost
treatments of one knob; EARLY is *timing gain minus a longer scale tail*.
**Registered consequences, pre-committed:**
* **A NULL CONTRAST IS AMBIGUOUS AND MUST BE REPORTED AS SUCH.** Δ ≈ 0 is
  consistent with *"timing does not matter"* AND with *"the timing gain is real
  and is exactly cancelled by the scale cost of buying early"*. **This leg cannot
  separate those two, and no readout sentence may pick one.**
* **A POSITIVE EARLY RESULT IS UNUSUALLY STRONG,** because it must have overcome
  the handicap: Δ entirely above +1.87pp means the executor-band timing pays
  *after* paying a longer inflation tail on every subsequent build in the game.
* **A NEGATIVE EARLY RESULT IS CORRESPONDINGLY WEAK EVIDENCE AGAINST THE TIMING
  HYPOTHESIS,** because the scale cost is a live alternative explanation with a
  named mechanism. It closes the *shipping* question for gate-25, not the
  *timing* question.

**6. ROTATION POLICY IS HELD FIXED ACROSS BOTH ARMS, DELIBERATELY, SO THAT TIMING
IS THE ONLY MANIPULATED VARIABLE.** `LOKI_BELTBREAK_MAX_ROT = 1` (one rotation per
gunner **per life**, a hard cap that makes an A→B→A oscillation impossible by
construction) is **identical in both trees**.
⭐ **AND ROTATE-ONCE-PER-LIFETIME IS A MEASURED FIELD NORM, NOT A SIMPLIFYING
ASSUMPTION — WHICH IS WHAT MAKES HOLDING IT FIXED A STRENGTH OF THE DESIGN RATHER
THAN A LIMITATION OF IT.** The best executors mostly never rotate at all:
**Pantheon 0.65 rotations per gunner, O(1) 0.17, with 66-83% of their gunners never
rotating**; and when they do, it is **kill-TRIGGERED — 0.61-0.95 of rotations are
preceded within 4 rounds by a kill.** The mechanism is on the record from the
victim side: **the line is FARMED, not eaten — 92.5% of consecutive same-facing
shots land at the same distance**, i.e. the enemy rebuilds into the kill zone and a
fixed facing keeps harvesting it. ⇒ **both arms sit at field practice, and Δ is not
confounded by an unusual rotation policy on either side.**
**Rotation is the NAMED NEXT ITERATION AXIS and is explicitly NOT in this pair.**
Research's rotation-ceiling
cut (05:39:02Z) is why it is next rather than never: in the productive band the
median gunner has **5-6 distinct enemy belt tiles ever within its attack radius
and 62-69% have at least four**, while a gunner shoots along ONE line in its
facing — so a fixed facing leaves reachable tiles unshot. ⚠ **NO
reachable-vs-killed PERCENTAGE IS QUOTED ANYWHERE ON THIS PAGE:** research states
the numerator (belt deaths within radius, inflated by multi-gunner overlap) and
the denominator (tiles ever present, not requiring simultaneity) **are not a clean
fraction — DIRECTION ONLY.** The registered hazard for that future arm is
**GUNPIN's rotate-thrash negative (44.27 vs `_v468kladturbo`)** and v94's 4.32
rotations × 10 Ti per gunner with 62.6% of facing segments firing zero shots.

**7. THE SHARD TAPE CANNOT SEE THE MECHANISM, AND A FIRINGS READ IS MANDATORY
BEFORE THE PRIMARY.** `tools/overnight.sh:138-139` runs every game with
`--replay /dev/null`; the tape's columns are
`ts shard game map seed seat winner cond turns` — **no entity, build, position or
turret information exists on it, in either arm.**
⛔⛔ **AND THE ORDERING IS WRITTEN OUT EXPLICITLY BECAUSE THE RULE WAS INVERTED ON
ITS FIRST FIRING TODAY.** `results.tsv:kladladder-verdict-amendment-f1f2-pending`
records the builder typing KLADLADDER's Band-4 primary **before** its registered
battery read, then amending. **That is a procedural datum on the tape, and this
prereg registers the ordering as a HARD SEQUENCE:**
> **D1 and S1 (below) are RUN, and their numbers written down, BEFORE any sentence
> containing this arm's primary share or the pair's Δ is typed.** A primary typed
> ahead of the firings read is a REGISTRATION BREACH regardless of what it says,
> and the repair is an amendment chain, not a re-write.

---

## RATIFY: Hypothesis

**PRIMARY (the contrast, shared with `BELTBREAK-LATE`).** *Opening the
beltbreak-gunner plant gate at r25 — the field's executor band — rather than at
r70 — our own historical median first in-band plant — raises our LOCAL pooled game
share vs `bots/_v468kladturbo` by MORE than 1.87pp, i.e. `Δ = p̂(EARLY) − p̂(LATE)`
has a 95% CI lying entirely ABOVE +1.87pp at n = 5,400 + 5,400.* Registered
direction **POSITIVE**.

**SECONDARY (this arm alone).** *The beltbreak gunner planted from r25, on the
`bots/_v468kladturbo` base, raises our LOCAL pooled game share vs
`bots/_v468kladturbo` itself to **51.33% or higher** at n = 5,400 games across all
15 corefill maps and both seats.*

**Provenance of the idea, verbatim (Magnus's original directive that created this
plank):** *"offensive gunner that shreds the enemy economy… a lot of the top teams
do this."*

**The mechanism claim, stated so it can be wrong.** The plank adds one code path
the base tree cannot express: a raider standing in the **d² 20-100 annulus of the
ENEMY core** may plant a **GUNNER** aimed at a belt or harvester tile **that exists
right now**.
⛔ **AND THE "NEW" HAS A NARROW, CORRECTED FORM — USE IT, NOT THE OBVIOUS ONE.** The
study's §10.7 said no code path of ours can plant a forward turret in d² 20-100;
**that is REFUTED (study amendment ~2026-08-17T05:5xZ): we already place ~25% of our
SENTINELS in-band.** ⇒ **THE GAP IS TURRET TYPE, NOT THE TARGET SET.** Our forward
path builds sentinels only; **no forward path of ours has ever SELECTED A GUNNER**,
and per §6 the gunner is the turret a 20-HP belt tile wants (12 ammo vs a sentinel's
20, 0.60×; 20 Ti vs 30). **The treatment trees are unaffected — they plant gunners
through their own dedicated path with an explicit annulus check, and the demo's 15/15
in-band plants are the evidence — but every background sentence on this page uses the
TYPE-GAP form.**
* **THE ANNULUS IS ACCOUNTED FOR BY THREE MEASURED QUANTITIES PULLING IN TWO
  DIRECTIONS — it is not an asserted band.** (i) **Belt DENSITY falls with
  distance.** (ii) **Target AVAILABILITY falls with distance**: distinct enemy belt
  tiles ever within a gunner's attack radius run **8.13 (mean) at d²<20 → 7.54 at
  20-30 → 4.34 at 80-100**, monotone decreasing. (iii) **SURVIVAL RISES with
  distance**: at d²<10 the median gunner life is **66 rounds with 56.3% dead**, and
  excess belt-kills per gunner are at their WORST there (1.72-2.28) against **2.89
  at d² 20-30**. ⇒ **`20 ≤ d² < 80` is where the product is maximised, and
  POINT-BLANK FAILS ON SURVIVAL, NOT ON TARGETS** — availability at 20-30 is 92% of
  the d²<20 ceiling at nearly double the conversion. *(Research, 05:39:02Z
  coordination cut; the study's placement gradient §3.6 is the density half.)*
* **THE GUNNER IS THE RIGHT TURRET FOR A 20-HP TARGET.** A conveyor/splitter costs
  3 gunner shots = 12 ammo against a sentinel's 2 shots = 20 ammo (0.60×), and the
  gunner is 20 Ti against 30. It is the WRONG turret for a core (288 ammo vs 280 at
  1.6× less reach), which is why **CORE scores ZERO in the siting ladder.**
* **THE v94 FAILURE IS IMPOSSIBLE BY CONSTRUCTION HERE, AND THAT IS A DESIGN CLAIM
  THIS LEG DOES NOT RE-TEST.** `_v115dodge`'s `_plan_siege` scored a tile by whether
  its ray reached where the enemy core *is*, with no live-target predicate:
  measured off replays, econ on the chosen ray **0.09 against a RANDOM ray 0.11**
  (below random), **51.7% of gunners built with nothing in range**, 7.9% never
  firing. Every plant here is gated on `can_fire_from(bp, facing, GUNNER, t)` where
  `t` is a live enemy entity read out of THIS builder's vision THIS round, plus an
  explicit own-ray walk (`_bb_ray_clear`). **A tile scoring 0 is never built on.
  There is no geometric fallback and no "where belt should be".**

**⇒ A FLAT SECONDARY IS INFORMATIVE AND IS NOT A NULL ABOUT "OFFENSIVE GUNNERS".**
It would say a live-target-gated forward gunner pays for its own 20 Ti, its own
+20% scale tail and its own ammo draw — which, against an incumbent that has **no
forward-gunner path at all**, is already a non-obvious finding.

---

## REGISTRATION BLOCK

**TARGET BAND: N/A — local corefill screen with ZERO rated ladder exposure: no submission, no activation, no unrated challenge, so `tools/target_value.py` has no input. Nothing on this page ends in a ship; the only branch that reaches the ladder is a later, separately-registered head-to-head against the holder.**
**PINNED: N/A — local self-play. The opponent version is fixed by construction: the control tree is `bots/_v468kladturbo` at the commit this shard runs from, pinned at `scratchpad/CONTROL_PIN`. There is no opponent churn to pin against and no calibration relevance to protect.**
**SURFACE: local**
**CLUSTER UNIT: none** — CLAUDE.md's enumeration PERFORMED, not asserted, and performed for BOTH the single-arm bar and the contrast: (i) the **MATCH** cluster does not exist on this surface — `tools/overnight.sh` writes one TSV row per `fcode run`, so 1 row = 1 game and no row shares a match with another; (ii) the **OPPONENT** cluster is degenerate — every one of the 5,400 rows plays the identical control tree, so the pooled stratum holds exactly one opponent and there is no between-opponent variation for a design effect to describe; (iii) for the CONTRAST specifically a third candidate cluster — **HOST** — is killed by REGISTRATION rather than by measurement, because both arms are registered to the same LOCAL host below; if that registration is broken the host term is live and unmeasured, which is why breaking it voids the contrast (Addendum 11 rider: the 0.98 exemption is a WITHIN-HOST measurement). All surviving clusters die ⇒ DEFF = the measured local constant **0.98** (pair-weighted, ρ = −0.020, 124 shards, s39 audit), i.e. naive intervals are correct and marginally conservative. **The platform constants (1.529 rated / 1.833 unrated) are NOT applicable and applying them would widen every interval here 24-35% for correlation that has been measured absent.**
**ESTIMATOR: for the SECONDARY bar, the unweighted pooled treatment game share** = (rows with `winner == T`) / (completed rows), over all 5,400 rows, both seats pooled, all 15 maps pooled, no reweighting. **For the PRIMARY, the DIFFERENCE of the two arms' unweighted pooled shares, Δ = p̂(BELTBREAK-EARLY) − p̂(BELTBREAK-LATE)**, each computed by that same rule on its own 5,400 rows. Because both shards are exactly balanced on the same 15 maps × 2 seats × 180 design, the pooled difference and the map-stratified equal-weight difference coincide by construction; the stratified form is computed at readout as an **arithmetic consistency check only** and is not a second estimator (s28 ring-hold: four estimators inside 0.010 of one bar flipped MEET/MISS among themselves). Seat A and seat B shares are reported SEPARATELY as a fixture diagnostic and are never a bar — seat is worth ~6.8pp on byte-identical arms, which is why each n is a multiple of 30. **Any estimate quoted at readout arrives from `tools/cluster_ci.py` (HEAD) so that the interval and the point are produced by the same call; the pre-data half-widths on this page are closed-form Wald with DEFF 0.98 and their arithmetic is shown in `THE CONTRAST`.**
**DOSE: beltbreak gunner plants — treatment ≥1 vs control 0, to be measured at n=48 games (the registered D1 battery size below).** The control's zero is **structural, and is stated as a code claim rather than dressed up as a measurement**: `grep -c 'BELTBREAK\|_bb_\|beltbreak'` over all four `bots/_v468kladturbo` files returns **0, 0, 0, 0** (verified at draft), and the control's only gunner references are `_try_counterbattery`, home defence keyed to `HUNT_BAND_DSQ = 41` of OUR OWN core — which is not a forward build by `tools/dose.py`'s own `fwd = d2_enemy < d2_own` predicate. ⛔ **NO UNIT PROBE WAS FIRED FOR THIS LINE AT DRAFT.** The registered **D1 battery** below is what converts it into a measured claim, and D1 runs BEFORE the primary is typed.
**PLANNED n: 5400 games** (= 15 maps × 2 seats × 180, so map and seat balance is exact; `tools/overnight.sh:68` has run a 15-map pool since the 2026-08-13 rotation and its own comment requires multiples of 30). **The CONTRAST's planned n is 5,400 PER ARM, 10,800 total; the comparator arm's 5,400 is registered in `docs/prereg/PREREG-BELTBREAK-LATE-2026-08-17.md`.**
**BOUNDARY: 5400 games** — LOCAL surface, one tape row is one game; there is no accept/attempt distinction on this fixture. ⛔ **A LINE COUNT IS NOT A ROW COUNT**: this tape carries an unprefixed header line under the `# FIXTURE` line, and a naive `wc -l` / `awk '!/^#/'` over-reports n by exactly one (measured today on KLADLADDER, `results.tsv:kladladder-n-final-correction`). The registered denominator is **DictReader row count, cross-checked against the heartbeat and against `max(game id) + 1`, for BOTH arms of the contrast.**
**CUT-SHORT: floor 2700 games.** Below 2,700 completed tape rows this arm publishes descriptive tallies (share, per-seat, per-map, kill-round, cond mix) and takes **NO comparative look and no bar verdict**; the one-sample half-width at 2,700 is ±1.87pp, already wider than the 1.33pp margin the secondary bar is built on, so a sub-2,700 read cannot resolve its own branches. ⛔ **THE CONTRAST HAS ITS OWN, STRICTER FLOOR: it requires ≥ 2,700 completed rows in BOTH arms, and its half-width is recomputed on the ACTUAL two n's, never on the planned ones** — at 2,700 + 2,700 it is ±2.64pp, 41% wider than the registered 1.87pp, and that widened number is what any short readout must quote. An `auto_gate` cancellation at CATASTROPHE@400, MARK-1000 or TREND-FLOOR@1000 is an **OPERATIONAL STOP, not a verdict**, and is typed `cancellation`. ⭐ **ONE CARVE-OUT, PRE-COMMITTED, AND IT IS THE ONE KLADLADDER USED:** a CATASTROPHE-clause cancellation (95% CI upper < 45.0 at n ≥ 400) is arithmetically INCOMPATIBLE with every band above Band 4 of the secondary reading, so a stop under that clause DOES license the Band-4 sentence at the partial n — **provided D1/S1 have been read first** and provided the partial share is disclosed as **selected-pessimistic** if the stop was taken on an interim look. **It does NOT license a contrast sentence** — see the ASYMMETRIC-STOP CLAUSE below.
**BAR: 51.33 (SECONDARY — this arm's own house band). MDE: 0.00pp — THE SECONDARY BAR IS A POINT RULE ONLY AND LICENSES NO EXCLUSION CLAIM ABOUT AN EFFECT SIZE** (OB16 corollary, 2026-08-15T03:52:45Z: the standard corefill band IS `50 ± half_width` at n = 5,400, so clearing 51.33 puts the CI's lower edge at exactly 50.00 — it excludes 50 and excludes no positive effect size whatsoever). n for the one exclusion it CAN make (bar ≠ 50.0): **5,400**, the planned n. **⭐ THE PRIMARY'S BAR IS SEPARATE AND IS SIZED, NOT A POINT RULE — see `THE CONTRAST`: Δ ≥ +1.87pp, MDE 1.87pp, n for that exclusion 5,400 per arm.**
**BASE RATE: 50.00**
**BAR SOURCE:** the secondary is the house-standard corefill futility band, `50 + 1.96*sqrt(.25/5400) = 51.33pp`, local DEFF 0.98 so naive — the identical bar carried by `docs/prereg/BARS.tsv` rows `SEALFLOOR6`, `SENTTHR`, `KLADTKILL`, `KLADTK2`, `KLADTURBOR`, `DRAINTURBO`, `KLADLADDER`, `SEALSENTAN` and `SEALSENTA`, which is what keeps this arm numerically comparable to the turret-family reads it extends. **Constructed, not observed.** The PRIMARY's bar is derived in `THE CONTRAST` from the two-sample half-width at the planned n's, also constructed and also naive at DEFF 0.98.
**BASE RATE SOURCE:** structural A/A expectation of a seat-balanced, map-balanced self-play fixture whose control tree is the treatment's own base. Empirically calibrated by `IDNULL140` — **49.27% [47.94, 50.60] at n = 5,400**, 2026-08-16T18:02:04Z, same host and fixture (`results.tsv:idnull140-cert-5400`) — and by `NULL125` — **51.04% at n = 5,400** (`results.tsv:null125-final`). Two A/A cells, one either side of 50.0, both intervals containing it. ⇒ **a bare clearance of the secondary in [51.33, 52.4] is a band an A/A cell has already produced**, which is why Band 2 of the secondary reading is pre-registered as WEAK. ⚠ **AND THOSE TWO CELLS SIZE THE CONTRAST'S OWN CREDIBILITY: they are 1.77pp apart, just under the contrast's 1.87pp half-width.** Two byte-identical arms on this fixture have produced a difference nearly as large as the smallest one this pair can call real. **Disclosed before the data, and it is why the contrast's bar is not set any tighter than the arithmetic allows.**
**POOL ERA: post-2026-08-13-rotation** — the 15-map local pool of `tools/overnight.sh:68`. (`check_pool_era` treats this as n/a on a LOCAL surface per SPEC §6; declared anyway so the population is on the page.)
**REFERENCE n: none** — the SECONDARY bar's comparator is a CONSTRUCTED null of 50.00 generated inside this same shard from its own 5,400 seeds; there is no external reference SAMPLE for it. The PRIMARY's finite comparator is handled under `THE CONTRAST` and carries its own two-sample half-width. See `WHY REFERENCE n IS none` below — the alternative reading produces a real `prereg_check.py` FAIL and is answered rather than dodged.
**TREATMENT TREE: bots/_v480beltbreak**
**TREATMENT DIFF REFS: 7bcf0e5e^ 7bcf0e5e**
**MECHANISM METRIC READS: bots/_v480beltbreak/raid.py:1009 — the `ct.build_gunner(bp, facing)` call inside `_try_beltbreak_gunner`, the single line whose execution IS the dose (a live-target-gated GUNNER bought on an annulus tile — the base tree reaches that band with SENTINELS but has no path that ever selects a gunner for it (study amendment ~05:5xZ)). Observed as D1 (forward gunner builds per game, treatment vs control, `tools/dose.py --kind gunner`) and S1 (the `d2_enemy` distribution of gunner BUILD events, which is the discriminator between an ANNULUS plant and the control's home counter-battery — see MECHANISM DIAGNOSTICS). TREATMENT DIFF TOUCHES: bots/_v480beltbreak/doctrine.py bots/_v480beltbreak/main.py bots/_v480beltbreak/raid.py. INTERSECTION: yes — `raid.py:1009` is inside the block the diff ADDS at `raid.py:773-1050` (`_live_beltbreak_guns` / `_bb_ray_clear` / `_try_beltbreak_gunner` / `_bb_refuse`), called from the new step 3b at `raid.py:327`; the whole `_bb_*` / `beltbreak` family does not exist in the control at all — `grep -c 'BELTBREAK\|_bb_\|beltbreak'` returns 0 in every one of the four control files, verified at draft — so the metric CANNOT read identically in both arms. ⚠ `bots/_v480beltbreak/eco.py` is BYTE-IDENTICAL to the control's (`cmp` clean at draft): this plank does not touch the economy module, which is what makes it a disjoint-subsystem composition candidate against the eco trio.**
**METRIC WINDOW: r0-r1000. GATING CONSTANTS: LOKI_BELTBREAK_RND=25, LOKI_BELTBREAK_MIN_HARV=1, LOKI_BELTBREAK_CAP=2, LOKI_BELTBREAK_DSQ_LO=20, LOKI_BELTBREAK_DSQ_HI=100, LOKI_BELTBREAK_MAX_ROT=1, LOKI_BELTBREAK_STALE=3, LOKI_BELTBREAK_AMMO=24, LOKI_BELTBREAK_TI_FLOOR=40, LOKI_BELTBREAK_MAX_TGT=12. MECHANISM CAN OCCUR IN WINDOW: yes** — **exactly ONE of these is a round gate**, `LOKI_BELTBREAK_RND = 25`, and it is an **OPENING** round, not a window that closes: `raid.py:882-883` refuses while `rnd < 25` and never refuses above it. The rest are counts (`MIN_HARV` harvesters, `CAP` live gunners, `MAX_ROT` rotations per life, `MAX_TGT` siting candidates), distances (`DSQ_LO/HI`, d² band), a staleness budget in rounds (`STALE`) and titanium/ammo thresholds. ⇒ **the mechanism's window is r25-r1000, inside the declared r0-r1000, and a REPLANT can occur at any round because the cap is a LIVE CENSUS of friendly gunners standing in the annulus (`_live_beltbreak_guns`), so rubble cannot close this arm.** ⭐ **THE `RND=25` SEMANTICS ARE A RATIFIED JUDGMENT CALL AND MUST NOT BE READ AS "PLANTS BY r25":** our median forward ARRIVAL is r31 (`docs/research/FORWARD-ARRIVAL-BASELINE-2026-08-16.md`), so an arm gated `rnd <= 25` would be EMPTY by construction on most maps and would measure *"we cannot walk there in 25 rounds"*. The demo's observed first plants land **r25-36**, which is the executor band. *(Builder ruling, coordination tape 05:38:51Z.)*
⚠ **DISCLOSED, because a green tool run with warnings under it is how a warning stops being read: `prereg_check.py` will emit `OBLIGATION 17, PARTIAL WINDOW` warns against the line above and THEY ARE ARTEFACTS OF THE CHECKER.** Its `check_metric_window` arithmetic reads every declared integer as a ROUND, so a harvester count of 1 and a live-gunner cap of 2 are reported as "rounds r0-r2 cannot contain the mechanism". The constants are declared anyway because they are the gates that actually bind, and an undeclared gate is the failure the obligation exists for.
**GATE RESOLUTION: three gates, sized separately. (a) THE PRIMARY (the contrast) — resolvable at the planned n's: |Δ| must exceed 1.87pp, which IS the registered MDE, so the gate's branches are separated by construction; if the observed |Δ| falls inside ±1.87pp the gate is UNRESOLVED and, per the pre-committed default, defaults to the RESTRICTION — no claim in either direction that plant timing matters or does not, and specifically no claim that r25 is safe to ship. (b) THE SECONDARY (this arm's own bar) — margin 1.33pp against half-width ±1.32pp, resolvable and only just. (c) THE OPERATIONAL FLOORS — the pinned `tools/auto_gate.py` marks CATASTROPHE@400 (CI-hi < 45.0), MARK-1000 (CI-hi < BAR 51.33), TREND-FLOOR@1000 (prefix < 52.0) and the same floors again at MARK-2700, all Magnus's confirmed constants; their firings are OPERATIONAL CANCELLATIONS that free a core, typed `cancellation`, never `verdict`, licensing no exclusion claim beyond the CATASTROPHE carve-out in CUT-SHORT. ⭐ **THE FLOORS NOW BIND REMOTE TOO, AND THIS DOCUMENT SAYS SO RATHER THAN INHERITING THE BOILERPLATE.** Every sibling prereg written before today carries *"the floors bind only on LOCAL corefill — `tools/auto_gate.py:113` is REPORT-ONLY on a remote worker"*, and **that clause is STALE as of `a50f27ef` (s48, 2026-08-17): `tools/remote_cancel.py` is live and `auto_gate --apply` can now stop a remote shard.** KLADLADDER running to n≈3,404 at 41.86% vs `_v468kladturbo` with no automatic stop (`results.tsv:kladladder-manual-catastrophe-stop`) is now HISTORY of the pre-fix gap, not a live constraint. ⇒ **THE BINDING REQUIREMENT ON THIS PAIR IS NOT "LOCAL", IT IS "SAME HOST"** — the contrast's HOST cluster is killed by registration, and the Addendum 11 rider (the 0.98 exemption is a WITHIN-HOST measurement) is what makes a split pair void. **REGISTERED: both shards run on the SAME host, LOCAL by default.** Moving BOTH arms to one remote worker is an amendment that must be typed BEFORE the first row and preserves the contrast; **moving ONE arm voids the contrast outright** and no amendment can repair it after the fact. Everything else on this page (D1, S1, D2, D3, D4, the seat and map splits) is DIAGNOSTIC and cannot rescue a failed primary. Any branch that does not resolve is UNRESOLVED, and an UNRESOLVED gate defaults to the RESTRICTION: no promotion, no ship conversation, no combination claim.**
**PRE-STATE: the predicted-change set is NOT already in the target state at lock.** Verified at draft against the control tree: `grep -c 'BELTBREAK\|_bb_\|beltbreak' bots/_v468kladturbo/{doctrine,eco,main,raid}.py` → **0 / 0 / 0 / 0**. The control has **no forward-GUNNER path — and the gap is TURRET TYPE, not the target set** (study amendment ~2026-08-17T05:5xZ, which REFUTES §10.7's bare "no code path can plant a forward turret in d²20-100": we already place ~25% of our SENTINELS in-band, so the annulus is reachable — what no forward path ever does is SELECT A GUNNER for it): its forward turret path builds SENTINELS only — `raid.py:688 tiles = core_tiles(E)` plus the `d² ≤ 32` filter plus the pre-scan bail `dsq_core(p, E) > 50` shape WHERE that path may plant, and since v102 every GUNNER call site in the tree is `_try_counterbattery`, home defence keyed to `HUNT_BAND_DSQ = 41` of OUR OWN core (study §5.1, reproduced at draft: the control's only `GUNNER` references are at `raid.py:72,774,784,789`). ⇒ **the pre-state that matters is not "nothing of ours reaches the band" — it is "nothing of ours puts a GUNNER there", and a gunner is the turret the §6 ammo table says a 20-HP belt tile wants.** **The behaviour this leg predicts to change therefore cannot already be in the target state.** ⚠ And the *comparative* claim the pair exists for — "planting in the executor band beats planting at our historical median" — is likewise NOT pre-satisfied: it is the hypothesis, the archive refuses to price it (§3.7, three instruments, three refusals), and every band below including a SIGN-REVERSED one is a live, pre-named outcome.
**MAP SEGMENT: none expected** — the primary is the POOLED contrast over all 15 maps and both seats, and the secondary is the POOLED share. The manipulated variable is a ROUND NUMBER on a gate that is otherwise identical between arms; a round is not a terrain property. What terrain changes is the raider's ARRIVAL LATENCY and the belt density it finds on arrival — and **those change BOTH arms in the same direction**, which is precisely why the between-arm contrast is cleaner than either arm's own bar. **No map cut may rescue this arm or this contrast.** Per-map shares and per-map Δ WILL be printed at readout as exploratory description — they carry no pre-registered direction and nothing may be banked off them without a fresh prereg. ⚠ **Two candidate segments are named here and DELIBERATELY NOT REGISTERED**: (i) the five 900-area maps (midgard, ragnarok, valkyrie, drakkarfjord, glacierkeep), where the longest approach means the r25 gate binds least — the arm where EARLY and LATE should differ least; (ii) `fjordgate`, where the demo's live-target gate found **no reachable belt at all** and planted nothing. Registering either would hand this pair a second chance to pass, which is OB15b's exact prohibition; if the pooled contrast fails and a cut looks alive, it needs its OWN leg with its OWN n (OB15c: the rows that suggested a segment cannot also confirm it).
**CELL VERSION CHURN: N/A — not a panel, no `CELLS:` line, one fixed local control tree.**

---

## WHY `REFERENCE n` IS `none` — TWO BARS, TWO SAMPLINGS

Written out because the obvious alternative produces a `prereg_check.py` FAIL, and
a certifier should see that it was hit rather than wonder whether it was dodged.

* **The SECONDARY bar (51.33) is a ONE-SAMPLE bar** against the constructed null
  50.00, generated inside this shard from its own seeds. Its half-width is the
  one-sample ±1.32pp and its margin (1.33pp) resolves — barely, exactly as every
  house-band shard on this fixture resolves.
* **Writing `REFERENCE n: 5400`** — naming `BELTBREAK-LATE`'s shard as a reference
  SAMPLE — makes the checker size 51.33 as a TWO-FIXTURE comparison at ±1.87pp and
  **correctly FAIL it** (`BAR_RESOLVABLE FAIL — margin 1.3pp < half-width 1.9pp`,
  the same FAIL `SEALSENTA` recorded hitting on the identical structure).
* **That FAIL would be a true statement about a bar nobody registered.** 51.33 is
  never compared against `BELTBREAK-LATE`'s share. **The PRIMARY is**, and the
  primary carries its OWN two-sample bar — **1.87pp on Δ** — derived below, where
  the margin EQUALS the half-width and the gate therefore resolves by construction.
⇒ **Two bars, two samplings, and neither borrows the other's half-width.** The
contrast's comparator is `BELTBREAK-LATE`'s registered 5,400-row shard and is
finite, so the contrast's resolution does not improve without a registered n
increase in BOTH arms. Pooling extra rows into either arm after lock is an
unregistered n increase (optional stopping with extra steps) and is prohibited; a
replication is reported SEPARATELY and NEVER pooled, per the GUNAXABL/SENTTHR
precedent.

⚠ **KNOWN CHECKER DEFECT, AVOIDED RATHER THAN TRIGGERED:**
`tools/prereg_check.py:366-371`'s `int_before` uses `re.search(r"([\d,]+)\s*" + word, …)`
and `[\d,]+` matches a **bare comma**, so a `REFERENCE n:` free-text value whose
first digit-or-comma character is a comma makes `int("")` raise and the checker
**dies with a `ValueError` traceback instead of returning a verdict**. This
document's `REFERENCE n` value is deliberately written without a leading-comma
clause. *(Found and routed by the `SEALSENTA` draft; not fixed by this agent.)*

---

## THE CONTRAST — how Δ is computed, and what it can and cannot exclude

**ESTIMAND.** `Δ = p̂_EARLY − p̂_LATE`, where `p̂_EARLY` is this shard's pooled game
share vs `bots/_v468kladturbo` over its own 5,400 rows and `p̂_LATE` is
`BELTBREAK-LATE`'s over its own 5,400 rows. **Both arms share the control tree, the
15-map pool, the 2-seat balance, the 180-replicate cell design, the runner
(`tools/overnight.sh`) and the host.** They differ in the treatment tree's ONE
constant and in the seed base.

**⛔ WHAT THE ONE CONSTANT ACTUALLY IS, STATED PRECISELY BECAUSE THE OBVIOUS GREP
MISLEADS.** The twin does **not** flip `LOKI_BELTBREAK_EARLY`; that stays `True` in
both trees. It changes **`LOKI_BELTBREAK_RND` from 25 to 70** — line 1353 of
`doctrine.py`, and `diff` between the two `doctrine.py` files returns **that one
line and nothing else** (verified at draft), with `eco.py`, `main.py` and `raid.py`
**byte-identical between the arms** (`cmp` clean on all three). Both arms therefore
take the SAME branch of the ternary at `raid.py:882-883`, reading
`LOKI_BELTBREAK_RND`; `LOKI_BELTBREAK_LATE_RND = 70` is inert in both.
**A certifier who greps `LOKI_BELTBREAK_EARLY` and finds `True` in both trees has
not found a defect — they have found this paragraph's reason for existing.**

**INTERVAL.** Two independent samples, DEFF 0.98:
```
se(Δ)  = sqrt( DEFF * ( p_E(1-p_E)/n_E + p_L(1-p_L)/n_L ) )
       = sqrt( 0.98 * ( 0.25/5400 + 0.25/5400 ) )   at p ~ 0.5
       = 0.0095258         ->   half_width_95 = 1.96 * se = 1.867pp
at 2700 + 2700                                            = 2.640pp
```
**PRIMARY BAR: Δ ≥ +1.87pp.** Registered direction **POSITIVE** (the executor band
beats our incumbent timing). **MDE: 1.87pp — WE WILL CALL THE TIMING EFFECT A MISS
IF ITS TRUE MAGNITUDE IS AT OR BELOW 1.87pp. n for that exclusion: 5,400 per arm,
which is the planned n.** This is the OB16 preferred form: the bar IS
`null(0.00) + MDE(1.87)`, so clearing it IS the exclusion and the bar cannot be
quoted without its MDE.

**⛔ WHAT THIS PAIR CANNOT DO, STATED BEFORE THE DATA.** A true timing effect
smaller than ~1.9pp is **invisible to this fixture**, and sizing up to see it is
not free: excluding a 1.0pp difference would need **≈ 18,800 games per arm**. ⇒ **if
Δ lands inside ±1.87pp the registered reading is UNRESOLVED, not "timing does not
matter".** Restating the fail-to-exclude form as an exclusion is mandatory per
CLAUDE.md's DEFF direction clause: the only admissible harmlessness claim is *"the
95% interval on Δ excludes a timing effect larger than X"*, with X read off the
data, never *"no significant difference was found"*.

**⛔ AND THE SCALE ASYMMETRY IS PART OF THE ESTIMAND, NOT NOISE AROUND IT.** Per
READ-BEFORE-RATIFYING #5, Δ measures *(timing gain) − (extra global-scale tail from
buying a +20% gunner 45 rounds earlier)*. **Δ is a NET quantity and every readout
sentence must say so.** No branch of this leg estimates the timing gain alone.

**⭐ ASYMMETRIC-STOP CLAUSE — PRE-STATED BECAUSE IT IS THE MOST LIKELY WAY THIS PAIR
BREAKS.** If the `auto_gate` floors cancel ONE arm and not the other, Δ would be
computed between a full arm and a **selected-pessimistic partial**, biasing it in a
direction the fixture chose rather than the mechanism. **Registered handling: a
gate stop on EITHER arm CANCELS THE CONTRAST SENTENCE.** The contrast may then be
reported ONLY on the **COMMON PREFIX** (the first `min(n_E, n_L)` completed rows of
each tape, in tape order), explicitly labelled **PREFIX-MATCHED**, with its
half-width recomputed at that n and with the full-arm number reported beside it —
and neither presented as the other. **A prefix-matched Δ does not clear the
registered PRIMARY BAR and cannot promote anything.**

---

## FALSIFIER

**PRIMARY FALSIFIER: the 95% CI on Δ does NOT lie entirely above +1.87pp.** Two
sub-cases, both pre-named:
* **CI on Δ contains 0.00** → the timing effect is not resolvable at this n.
  **UNRESOLVED ⇒ RESTRICTION.** No sentence in any readout, wrap or QUEUE row may
  claim plant timing is cheap, free, or settled. The honest output is an upper
  bound on |Δ| plus the observation that the beltbreak family's fate is decided by
  the PLANT, not by WHEN it lands — **which is itself a finding, because it retires
  the timing axis as a tuning direction and promotes rotation (the named next axis)
  ahead of it.**
* **CI on Δ lies entirely BELOW −1.87pp** → **the hypothesis is refuted with its
  sign reversed: planting at our historical median BEATS the executor band.** The
  field-imitation premise of the whole shredder programme would then be wrong in
  direction on this base, `BELTBREAK-LATE` carries the family forward, and the
  scale-asymmetry reading (#5) becomes the leading explanation to be tested next
  rather than a caveat. **This is a live outcome and it is named here so it cannot
  be explained away as noise if it lands.**

**SECONDARY FALSIFIER: at n = 5,400 the 95% CI UPPER bound on this arm's own pooled
share vs `bots/_v468kladturbo` falls BELOW 51.33.** That excludes the arm's own
bar. It does **not** by itself decide the contrast, and a readout that reports only
this number has reported the less informative half of the leg.

**MECHANISM FALSIFIER (independent of both, and it can fire first):**
* if **D1** shows the treatment's forward gunner builds per game are not above the
  control's outside the tool's own band, **the plank did not deliver its dose** and
  both this arm's bar and the contrast are **uninterpretable**: a flat share would
  mean "the mechanism never fired", not "the mechanism fired and did not pay". The
  primary is then reported as **NOT MEASURED**, not as a null;
* if **S1** shows the treatment's gunner-build `d2_enemy` mass is not shifted into
  the annulus relative to the control's, the plants are not the plants this plank
  claims to make, and the same NOT MEASURED handling applies;
* ⭐ **AND THE PAIR HAS A THIRD, SPECIFIC WIRING FALSIFIER THE SEALSENT PAIR DID NOT
  NEED: if `S1`'s PLANT-ROUND distribution does not differ between the two arms,
  the ONE CONSTANT had no runtime effect and the contrast is measuring two
  identical bots.** A Δ near zero would then be a wiring null, not a finding about
  timing. **This is not hypothetical: s47's delta D2 records a wiring null escaping
  demos to a 436-game shard, and today's KLADLADDER amendment chain exists because
  a 42.07 could equally have been one.**
Per FIRINGS-BEFORE-PRIMARY all three are read BEFORE the primary is typed.

---

## READING, PRE-COMMITTED

Registered now so no band is chosen after the fact. **Read TOP-DOWN; the first row
whose condition holds is the reading. Rows are disjoint by construction.**

### PRIMARY — four bands on Δ at 5,400 + 5,400

| # | band on Δ | pre-committed reading |
|---|---|---|
| **A** | **CI on Δ entirely above +1.87pp** | **THE EXECUTOR BAND BEATS OUR INCUMBENT TIMING, AND THE EFFECT IS RESOLVED.** The hypothesis holds, and per READ-BEFORE-RATIFYING #5 it holds **having overcome the earlier +20% scale tail**, which makes it unusually strong. `BELTBREAK-EARLY` (subject to its OWN secondary band) promotes to a combination input and to a separately-registered head-to-head. The size is quotable, since this bar carries a real MDE. |
| **B** | **point Δ > +1.87pp but CI contains +1.87pp** | **REAL-BUT-SMALL, DIRECTIONAL ONLY.** Direction consistent with the hypothesis; magnitude not separated from the MDE. Rows are KEPT; EARLY is preferred over LATE as the family's carrier, **with no ship conversation and no closure of the timing axis.** A replication on fresh seeds, same host, is the price of promoting it. |
| **C** | **CI on Δ contains 0.00** | **UNRESOLVED ⇒ RESTRICTION.** See the primary falsifier. Report an upper bound on \|Δ\|. **The timing axis is retired as a TUNING direction** — nothing here to tune toward — without any claim that timing is harmless, and **rotation becomes the next axis by default.** |
| **D** | **CI on Δ entirely below −1.87pp** | **SIGN REVERSED — OUR HISTORICAL TIMING BEATS THE EXECUTOR BAND.** The hypothesis is refuted. `BELTBREAK-LATE` carries the family, the field-imitation premise is falsified on this base, and the next iteration tests the scale-cost explanation directly rather than tuning the gate further. |

⚠ **CROSS-BAND NOTE, registered so it is not improvised: Band A together with a
Band-4 (SUBTRACTS) secondary reading on BOTH arms means both are worse than
Sleipnir and the executor band is merely the less-bad of two losses. That
combination CLOSES the beltbreak family and promotes NOTHING, however clean Δ is.**
The contrast prices a parameter; it does not resurrect a plank that loses on its
own.

### SECONDARY — four bands on this arm's own share vs `bots/_v468kladturbo` at n = 5,400

| # | band | pre-committed reading |
|---|---|---|
| **1** | **CI lower ≥ 51.33** | **THE PLANK ADDS.** Real and resolved on this fixture. Promotes to a combination input (the plank touches `raid.py`/`main.py` only, `eco.py` byte-identical — a disjoint subsystem against the eco trio) and to a separately-registered head-to-head. ⚠ Report the size with its OB16 status: the standard band has MDE 0, so this branch may claim "we can exclude 50 vs `_v468kladturbo`" and may NOT claim any minimum effect size. |
| **2** | **point ≥ 51.33 but CI lower < 51.33** (includes the whole [51.33, 52.4] window an A/A cell has already produced) | **REAL-BUT-SMALL, COMBINATION INPUT ONLY.** Registered in advance as WEAK: `NULL125`'s byte-identical A/A read 51.04. Rows are KEPT and the arm is available for combination; it does NOT license a ship conversation, and a replication on fresh seeds is the price of promoting it. |
| **3** | **point < 51.33 AND CI contains 50.0** | **PARITY — THE PLANK IS FREE.** A live-target-gated forward gunner, its 20 Ti, its +20% scale tail and its 24-ammo magazine draw all pay for themselves against an incumbent whose forward path plants sentinels there and never a gunner. That is a bankable structural finding and it is the input the CONTRAST needs in order to price timing against something. It does NOT license a ship. |
| **4** | **CI upper < 50.0** | **THE PLANK SUBTRACTS.** The gate-25 form dies as a ship candidate on its own. Attribution is bounded: this refutes *plant + its funding shape + its scale tail at r25*, not *forward gunners in general*, and the LATE arm's own band is what says whether the plank or the timing carried it. |

⚠ **Nothing here treats 50.0 as a floor.** A share below 50 vs `_v468kladturbo` is
a live outcome with named mechanisms (a +20% scale tail bought early, a 24-ammo
magazine floor competing with the base's own turret funding, a raider spending
turns siting instead of sealing) and it is pre-named so a negative is not explained
away as noise.

---

## MECHANISM DIAGNOSTICS TO READ AT READOUT

**Measurability is declared per metric. `NOT MEASURABLE` is written where it is
true, rather than a metric being quietly renamed into something the tape happens
to carry.**

### ⛔ ORDERING, REGISTERED AS A HARD SEQUENCE
**D1 and S1 run and are written down BEFORE any sentence containing this arm's
primary share or the pair's Δ is typed.** See READ-BEFORE-RATIFYING #7 for why
this clause is in bold and who is on notice.

### D1 — THE DOSE BATTERY. MEASURABLE, but NOT off the shard tape.
`tools/overnight.sh:138-139` passes `--replay /dev/null`, so this shard produces
**no** entity events. D1 runs on a **separate serial battery**:
```
.venv/bin/python tools/dose.py bots/_v480beltbreak --kind gunner \
    --ctrl bots/_v468kladturbo --games 48 --tsv scratchpad/bb_dose_early.tsv
```
**REGISTERED SIZE: 48 games (8 maps × 2 seats × 3 seeds — `tools/dose.py:126-131`
rotates its 8-map default two games at a time and plays both seats, so 48 is
exactly balanced), SERIAL** (never parallel: D65, `tools/dose.py:26-30`).
**Pre-registered expectation: treatment `fwdbuild_gunner`/game strictly above the
control's, with the paired difference outside the tool's own 2×SE band.**

**⛔ OB17 CHECKS PERFORMED AT DRAFT, INCLUDING THE ONE THAT COULD HAVE SURPRISED
ME.** (1) **Executing tool named:** `tools/dose.py`. (2) **Path exists in that
tool:** `--kind` is a free string (`:114`) that keys `fwdbuild_{kind}` off the
shipped decoder, so `gunner` is a legal value with no code change — checked, not
assumed. (3) **⭐ THE CLAUSE THAT RETURNED AN ANSWER I DID NOT ALREADY HAVE — what
"forward" means here.** `tools/dose.py:96` defines `fwd = d2_enemy < d2_own`, i.e.
*closer to their core than to ours*, **NOT** the plank's own d² 20-100 annulus. Two
consequences, both registered: (a) **the metric is CORRECT for this plank but is
WIDER than it** — every annulus plant is forward, and so is anything else the
treatment builds past the midline; (b) **it is the right discriminator against
THIS control anyway**, because the control's only gunner path is home
counter-battery at `HUNT_BAND_DSQ = 41` of OUR core, which is `d2_own < d2_enemy`
and therefore NOT counted. ⇒ **D1 measures "gunners built past the midline", and
S1 is what proves they are in the annulus.**
⭐ **AND THE STUDY AMENDMENT (~05:5xZ) STRENGTHENS THIS RATHER THAN THREATENING IT:**
the control DOES build forward turrets in the band — ~25% of our sentinels — so a
kind-BLIND forward-build metric would be contaminated. **`--kind gunner` is
kind-SPECIFIC**, and the type gap is exactly what makes the control's
`fwdbuild_gunner` a structural zero. **A reader must not substitute a
`fwdbuild_sentinel` or an all-turret count for it.** A reader must not quote D1 as an
annulus count.
⭐ **AND ONE DECODER FACT THAT WOULD HAVE INFLATED THIS METRIC ~3×, NAMED BECAUSE
THIS PLANK ROTATES:** `rotate()` re-emits `placeEntity` for an existing entity.
`tools/corpus/replay_events.py:16,113` guards it — a build is the FIRST
`placeEntity` carrying an id — and `tools/dose.py` uses that shipped decoder. **The
guard is present; this is a check that came out clean, and it is recorded as clean
rather than as absent.**
⭐ **REGISTERED-SIZE SHORTFALL RULE, pre-committed, because KLADLADDER's battery ran
24 of its registered 120 and its diff cleared the band by only 16%:** if the
battery runs short, the readout states the shortfall factor, and **a
`DOSE DELIVERED` verdict whose |paired diff| clears its own band by less than 2× on
a short battery is UNRESOLVED** — which, per GATE RESOLUTION, defaults to the
restriction and means the primary is typed with the mechanism unverified.

### S1 — THE ANNULUS AND PLANT-ROUND READ. MEASURABLE, but it needs a battery that KEEPS replays.
The discriminators are the **`d2_enemy` distribution** and the **`rnd` distribution**
of gunner `BUILD` events, per arm. `tools/corpus/replay_events.py` emits one row per
build with columns `file ev rnd team kind x y d2_own d2_enemy mw mh` (`:157`), so:
```
.venv/bin/python tools/corpus/replay_events.py OUT.tsv <replays…>
# rows with ev == BUILD and kind == gunner, grouped by team:
#   (a) histogram d2_enemy   -> the annulus read
#   (b) histogram rnd        -> the plant-round read (EARLY vs LATE vs control)
```
**Pre-registered expectations, both directional:**
* **(a)** the treatment's gunner-build `d2_enemy` mass sits **predominantly in the
  20-100 band**, and contains a mode the control's distribution — which is home
  counter-battery — **does not reach at all**;
* **(b)** the treatment's **first** gunner-build round per game is **at or above 25
  and clusters near it**, and — read across the pair — **the EARLY arm's plant-round
  distribution is shifted DOWN relative to the LATE arm's by roughly the 45-round
  gate difference.** ⭐ **(b) is the check that the ONE CONSTANT had a runtime
  effect at all**, and it is the third mechanism falsifier above.
⚠ **THE EXACT NUMERIC CUT FOR (a) IS DELIBERATELY NOT ASSERTED AT LOCK, AND HERE IS
WHY:** `replay_events.py:95-96,113` measures `d2` to a **single core anchor
position** (`corepos[team]`, the core entity's own position off the map buffer),
while the bot's `dsq_core` measures to the **nearest tile of the 2×2 footprint**.
The two conventions differ by which footprint tile is the anchor, so a plant the bot
scored at d² = 20 can decode a few units higher. **⇒ the band edges are read with an
explicit tolerance and the CUT IS CALIBRATED FROM THE CONTROL ARM'S OWN
DISTRIBUTION at readout** — the control never plants forward, so any treatment mass
in the forward band on the same map is the plank. **The DIRECTION is registered;
only the cut point is deferred, and it is deferred to a control-derived quantity
that cannot be tuned toward a verdict.**

⛔ **OB17 — THIS READ IS NOT EXECUTABLE OFF A `tools/dose.py` RUN, AND THE BUILDER
MUST FIX THAT BEFORE THE BATTERY FIRES.** `tools/dose.py:157` calls
`rp.unlink(missing_ok=True)` on every replay immediately after decoding, and its
argparse (`:110-126`) defines only `bot`, `--ctrl`, `--kind`, `--games`, `--maps`,
`--tsv` — **there is no `--keep`.** ⇒ S1 requires either (a) a `--keep` flag added to
`tools/dose.py` before the battery runs, or (b) its own small serial loop that
passes `--replay <unique path>` and retains the files. **CONSEQUENCE OF SILENT
NON-EXECUTION, registered per OB17 clause 3: if S1 is skipped, the dose evidence is
D1's headline ALONE, which by the paragraph above measures "past the midline" and
NOT "in the annulus", and cannot see plant round at all — so the primary must then
be typed with "MECHANISM NOT VERIFIED / TIMING DELTA UNVERIFIED" attached, and no
band may be attributed to the plank's siting or to its timing.** This is the clause
that could still surprise the person running it; run it first.

### D2, D3, D4 — the outcome-shape reads. MEASURABLE, shard-native.
`cond` and `turns` are on the tape.
* **D2 — TIMELY-KILL RATE (the `DEFENCE_ADMISSION_BAR` primary).** Share of ALL
  treatment-seat games ending `cond == core_destroyed` with `turns ≤ 300`,
  treatment vs control, both computed on the same 5,400 rows, and **EARLY vs LATE
  across the pair.** **Non-regression is the bar and it is stated as an EXCLUSION,
  per CLAUDE.md's fail-to-exclude clause: the 95% CI on the difference must EXCLUDE
  a fall of more than 2.0pp.** A "no significant rise" phrasing is not admissible.
  ⚠ **This is the metric most likely to move against us on this plank and the
  reason is named in advance:** a raider that spends turns siting and paying for a
  forward gunner is a raider not sealing the enemy ring, and the study's own §7.0
  warns that the conveyor FARM is a 511-turn engine that `DEFENCE_ADMISSION_BAR`
  forbids. **The siting ladder answers it by construction — HARVESTER 100 over
  CONVEYOR/SPLITTER 40 — but that is a design intention, and D2 is the measurement.**
* **D3 — MEDIAN KILL ROUND**, treatment vs control and EARLY vs LATE, as the gross
  backstop (median crossing 300 is disqualifying). Anchor: KLADTURBO's own local
  full read had median kill 193 (`results.tsv:kladturbo-local-confirm-5400`,
  61.09% [59.79, 62.39] at n = 5,400 vs `_v223sealrepair`).
* **D4 — COND MIX**, the share of games ending `core_destroyed` / `r1000` /
  `NOWINNER`, per arm. `R1000_IS_DEFEAT` makes an r1000 share a cost even when the
  tiebreak is won, and a shredder plank is exactly the family that could trade kills
  for an economic grind.

### NOT MEASURABLE on this leg — named, not silently dropped.
* **PLANTS PER GAME, THE PLANT-ROUND DISTRIBUTION, AND GUNNER LIFESPAN ARE NOT
  DECODABLE OFF THE SHARD.** `tools/overnight.sh:138-139` runs `--replay /dev/null`:
  **local corefill keeps TAPES, not REPLAYS.** The tape can carry share, kill round,
  `cond` mix and D2's timely-kill rate, **and nothing else.** ⇒ **every mechanism
  number in this leg comes from the SEPARATE D1/S1 batteries, and the shard's n =
  5,400 lends them none of its power.** Anyone quoting a plant count "from the
  BELTBREAK shard" is quoting something that does not exist.
* **WHETHER A PLANTED GUNNER'S ROTATION WAS USED, AND WHAT IT WAS AIMED AT.**
  Facing is not in the decoded event stream, which is research's own stated limit
  (*"the archive can price the CEILING but never the CONVERSION, because facing is
  not in `events.tsv`"*). **The rotation half of Magnus's directive is UNOBSERVED by
  this pair by construction, which is why it is the next axis rather than a
  secondary here.**
* **BELT-KILL ATTRIBUTION AT SHOT LEVEL.** The demo did this off retained replays
  with jitter controls; **this shard cannot.** A Band-3 "free" result and a "we
  bought an expensive ornament" result are NOT separable off the tape.
* **Per-unit CPU** — local replays zero-fill `execTimeUs`, so no timing claim is
  available on this surface. `tools/overnight.sh:138` does pass `--tle 10`, so a
  timeout is capped engine-side; the demo battery recorded **0 TLE**. ⚠ **And
  `LOKI_BELTBREAK_LOG = True` in BOTH arms** — a `print()` per plant plus a
  rate-limited (1-in-25) refusal print. On this fixture stdout goes to
  `--replay /dev/null`, the cost is identical in both arms, and it therefore cannot
  bias the contrast; **it is named because a CPU regression is invisible on this
  surface and "identical in both arms" is a statement about the CONTRAST, not about
  the shipped bot.** If either arm is promoted toward a ship, that flag is a
  ship-blocker to be turned off and re-screened.
* **Seed determinism** — `NOISE_ON` pins an unseeded RNG, so base-vs-base at one
  seed diverges at round 0. **No seed-matched or replay-diff equivalence claim is
  available on this fixture, and the flag-off base-equivalence claim is made on the
  CODE plus the demo's flag-off battery, never on a replay comparison.**

---

## THE DEMO EVIDENCE — FIRINGS ONLY, NO EFFECT SIZES

**⛔ THIS SECTION IS BANKED MECHANISM EVIDENCE. IT CONTAINS NO OUTCOME NUMBER AND
MAY NOT BE USED AS ONE, AND THE REASON IS MEASURED: on this fixture the SAME CODE
has shown a seat swing of up to 70pp on single games.** The demo battery is small,
unbalanced and unregistered; it establishes that the plank FIRES and how, and
nothing about whether it PAYS.

Recorded by the builder on the coordination tape at **2026-08-17T05:38:51Z**:
* **Annulus siting VERIFIED — 15/15 plants at d² 20-85** (inside the registered
  20-100 band).
* **Executor-band timing — first plants r25-36**, which is what ratifies the
  gate-opens reading of `RND = 25` against the empty literal reading.
* **Shot-level belt-kill attribution** — 122 fire events from one tile, with jitter
  controls collapsing **122 → 40 → 0**; 11 conveyors + 1 harvester in the first 12
  decoded kills; the study's rebuild-farm reproduced live.
* **The live-target gate REFUSES honestly — 7 of 16 games plant NOTHING** (no belt
  in reach ⇒ no plant; `fjordgate` has no reachable belt). ⭐ **This is the honest
  zero that makes the gate a gate:** a predicate that has never produced the other
  verdict has not been seen to gate.
* **Rotate-once holds — 15/15 at n = 1.**
* **Flag-off 36/36 byte-identical WITH a 36/36 flag-on positive control.** ⭐ **The
  positive control is the half that matters:** 36/36 identical alone is equally
  consistent with a harness that cannot see any difference.
* **Economy unharmed at the gate round — 3.31 vs 3.06 harvesters at r25.**
* **0 TLE.**
* **⛔ TI IS THE MEASURED BINDING REFUSAL — 377 of 484 in-band refusals.** Magnus's
  funding warning, measured from the turret side. **REGISTERED CONSEQUENCE: the
  EARLY arm's dose is PARTLY FUNDING-LIMITED BY CONSTRUCTION, and this document
  promises no dose the bank cannot pay.** D1's expectation is *"strictly above the
  control's zero, outside the band"*, **not** a plants-per-game target. A low but
  non-zero dose is the predicted state of the world, not a delivery failure — and
  it is also the reason the EARLY arm's advantage is not guaranteed: **at r25 the
  bank is smaller than at r70, so the earlier gate opens onto a poorer treasury.**
  *(No harvester cap was added; that road is dead.)*

⛔ **AND THE SCRIPTS ARE NOT BANKED. THE FINDINGS ARE.** My drafting brief named
`scratchpad/bb_demo.py` and `scratchpad/bb_shots.py` as banked artefacts; **neither
file exists anywhere in the repo, tracked or untracked** (`find . -name 'bb_*'` at
draft returns only `docs/research/scripts/side-lane-2026-08-09/bb_decode.py`, an
unrelated 2026-08-09 tool). ⇒ **nothing on this page registers a re-run of them**,
because OB17 forbids registering a method whose executing tool does not exist. The
demo evidence above is cited as a PROSE RECORD on the coordination tape, and the
executable firings instruments this leg registers are **D1 (`tools/dose.py`) and S1
(`tools/corpus/replay_events.py`)**, both of which were checked to exist at draft.

---

## THE CHANGE — `file:line`, control → treatment

**TREATMENT TREE: `bots/_v480beltbreak`** — `bots/_v468kladturbo` plus one plank
across **three** files. Verified at draft: `diff -rq` names `doctrine.py`,
`main.py`, `raid.py` and **`eco.py` is byte-identical** (`__pycache__` entries are
build artefacts, not source).

**(1) `doctrine.py:1266-1370`** — the doctrine block and the constants:
`LOKI_BELTBREAK_ON = True`, `LOKI_BELTBREAK_EARLY = True`,
**`LOKI_BELTBREAK_RND = 25`** (`:1353` — the one line that separates this tree from
`bots/_v483beltbreaklate`), `LOKI_BELTBREAK_LATE_RND = 70` (inert in both arms),
`LOKI_BELTBREAK_DSQ_LO/HI = 20/100`, `LOKI_BELTBREAK_CAP = 2`,
`LOKI_BELTBREAK_MIN_HARV = 1`, `LOKI_BELTBREAK_AMMO = 24`,
`LOKI_BELTBREAK_TI_FLOOR = 40`, `LOKI_BELTBREAK_STALE = 3`,
`LOKI_BELTBREAK_MAX_ROT = 1`, `LOKI_BELTBREAK_MAX_TGT = 12`,
`LOKI_BELTBREAK_LOG = True`, `SLOT_BELTBREAK = 13`.

**(2) `raid.py:315-327`** — step **3b**, the new call site
`if LOKI_BELTBREAK_ON and self._try_beltbreak_gunner(ct, E): …`.

**(3) `raid.py:773-1050`** — the `_live_beltbreak_guns` / `_bb_ray_clear` /
`_try_beltbreak_gunner` / `_bb_refuse` family. **The plant lands at `:1009`.** The
gate order is: band pre-scan (silent) → round gate `:882-883` → harvester gate
`:885` → **LIVE CENSUS cap** `:888-890` → funding `:904-907` → live-target scan
`:929` → siting ladder → own-ray walk `:970` → `build_gunner` `:1009` → heartbeat
write `:1017`.

**(4) `main.py:155-166`** — five per-unit counters (`bb_plants`, `bb_refuse`,
`bb_rot`, `bb_shots`, `bb_seen`) plus the import of `BB_NO_FIRE` / `BB_SITE_VALUE`.

**(5) `main.py:362-402`** — the beltbreak MAGAZINE, placed **after** the T4 burn cap
deliberately: that cap is `min()`-ed against a target derived from `weapons_top`
(`SLOT_HOME_GUN + SLOT_FWD_GUN`), and **a beltbreak gunner is in neither counter**,
so a bump placed above the cap would be multiplied by zero and silently deleted.
`bb_live` joins the ARMING condition but **not** `ti_floor`, so the plank may open
the ammo tap and may **not** lower the harvester reserve `E1_AMMO_FLOOR` protects.

**(6) `main.py:933-945` + `:1079-1082`** — a gunner STANDING IN THE ANNULUS is
treated as a beltbreaker whoever built it (there is no per-unit tag to inherit;
the planting builder is a different `Player` instance), plus the shot counter.

**⭐ THE CAP HAZARD THIS PLANK ROUTES AROUND, worth a certifier's minute:**
`LOKI_FWD_GUN_CAP` counts `SLOT_FWD_GUN`, which is written only as `read + 1` and
never decremented — **it counts RUBBLE**, so three dead forward turrets close that
arm for the match. **BELTBREAK does not touch that counter at all**; its cap is a
LIVE CENSUS of friendly GUNNERs in the annulus, and `_live_fwd_guns` counts only
SENTINELs. **The two arms share no counter and no store slot** (`SLOT_BELTBREAK = 13`
was `SLOT_DEFEND_BEAT`, read and written by nothing else in this tree).

---

## WHAT THIS LEG COSTS AND WHAT IT DOES NOT

**Cost: one LOCAL core to n = 5,400, plus 48 serial games for D1 and the S1
battery.** ZERO rated ladder exposure, zero submissions, zero unrated challenges —
nothing on this page touches the platform, which is why `TARGET BAND` is N/A rather
than a number.

**It does NOT decide a ship.** The strongest branch promotes the arm to (a) a
combination input — and the disjointness is verified, not assumed: **`eco.py` is
byte-identical to the control's**, so this plank composes with the eco trio by
construction — and (b) a separately-registered head-to-head against the live holder,
which is the pipeline step Magnus's procedure names verbatim (*"we start by testing
it against the current slot, if it beats it we can switch"*). **A local screen
against the incumbent is gate 1; gate-1-to-gate-2 transitivity is UNVALIDATED in
this repo (QUEUE #65: 3 concordant, 1 not), so the head-to-head is not skippable on
the strength of this number.**

**It is HALF of a pair.** `docs/prereg/PREREG-BELTBREAK-LATE-2026-08-17.md` screens
`bots/_v483beltbreaklate` — one constant apart — and registers the SAME Δ as its
primary. **Neither arm's own bar is the interesting quantity; the contrast is.** For
that contrast to be computable as registered, **both shards must run LOCAL, on the
same host, at the same planned n** — see the cross-host rider in the obligations doc
(Addendum 11 rider, 2026-08-15): the 0.98 exemption is a WITHIN-HOST measurement and
does not cover cross-host pooling.

**AND IT IS ONE SOLO SCREEN FEEDING MAGNUS'S DAY TARGET: >60% vs Sleipnir v1
(`bots/_v468kladturbo`).** ⚠ **That target is a genuine stretch and this page does
not pretend otherwise: 60-vs-Sleipnir ≈ 70.6-vs-v140 through the logistic, ~9pp
past our best-ever yardstick result.** The composition plan is that disjoint
subsystems ADD; this plank's `eco.py`-identical footprint is what qualifies it, and
a Band-1 or Band-3 secondary both keep it in that pool.

---

**PROVENANCE:** `docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md` (read in full: OB7, OB12, OB13, OB14, OB15a/b/c, OB16 + its corollary and cross-host rider, OB17 + its rider) · `docs/prereg/PREREG-SEALSENTAN-2026-08-17.md` and `docs/prereg/PREREG-SEALSENTA-2026-08-17.md` (today's house style and the between-shard contrast pattern reused here, both read in full) · `docs/prereg/BARS.tsv` (registry header, the FIRINGS-BEFORE-PRIMARY rule, and the sibling klad/sealsent-family rows) · `CLAUDE.md` · `docs/research/REPLAY-STUDY-offensive-gunner-2026-08-17.md` **plus its ~2026-08-17T05:5xZ AMENDMENT refuting §10.7's no-code-path claim (the gap is TURRET TYPE, not the target set; ~25% of our sentinels already plant in-band)** (§3.6 placement gradient, §3.7 the timing refusal and the r56-85 lateness table, §5.1 the control's missing path, §6 the ammo table, §7.0/§7.1/§7.2/§7.3) · `docs/research/FORWARD-ARRIVAL-BASELINE-2026-08-16.md` (median forward arrival r31) · `docs/coordination.md` (builder 2026-08-17T05:38:51Z the BELTBREAK demo record and the gate-opens ruling; research 2026-08-17T05:39:02Z the rotation-ceiling / three-quantity annulus cut; builder 2026-08-17T05:39:22Z Magnus's day target; builder 2026-08-17T05:40:52Z the target-notation rule) · `tools/prereg_check.py` (read for `RULES`, `check_presence`, `check_arithmetic`, `check_metric_window`, `check_pool_era`, and the `:366-371` `int_before` defect) · `tools/auto_gate.py` (`MARK_CATASTROPHE=400`, `MARK_MID=1000`, `MARK_HALF=2700`, `CATASTROPHE_CI_HI=45.0`, `TREND_FLOOR=52.0`, and the `:105-125` REMOTE clause — **read at draft and found CHANGED: the remote report-only limitation every sibling prereg quotes was closed by `a50f27ef` (s48) via `tools/remote_cancel.py`**) · `tools/overnight.sh` (`:68` the 15-map pool, `:99` `START=`, `:103` the `# FIXTURE … start=` stamp, `:110` the legacy-resume form, `:138-139` `--replay /dev/null --tle 10`) · `tools/dose.py` (`:96` the `fwd` predicate, `:110-126` argparse, `:126-131` map/seat rotation, `:157` the replay unlink, `:171-205` the paired band) · `tools/corpus/replay_events.py` (`:16` and `:113` the rotation guard, `:95-96` the core anchor, `:157` the output columns) · `tools/cluster_ci.py` (`--help` read; interval-with-estimate at readout) · `tools/control_pin.py` (`:72` the pin file) · `bots/_v480beltbreak/{doctrine,eco,main,raid}.py` · `bots/_v483beltbreaklate/doctrine.py` · `bots/_v468kladturbo/{doctrine,eco,main,raid}.py` · `scratchpad/corefill_work.txt` · `scratchpad/CONTROL_PIN` · `results.tsv` (rows `null125-final`, `idnull140-cert-5400`, `kladturbo-local-confirm-5400`, `kladladder-manual-catastrophe-stop`, `kladladder-verdict-amendment-f1f2-pending`, `kladladder-n-final-correction`) · git commits `cbf67e5d`, `7bcf0e5e`, `78f0d06b`, `8bd43a75`, `git show --stat cbf67e5d`, and sha1 comparison of `git show cbf67e5d:<file>` against the working tree for all four files · the drafting brief supplied by the builder lane s48 and its two mid-task corrections. No file under `bots/`, `tools/`, `scratchpad/`, `docs/prereg/BARS.tsv`, `results.tsv`, `HANDOVER.md`, `PROGRAMME.md` or `QUEUE.md` was created or modified by this agent, and no game was run.
