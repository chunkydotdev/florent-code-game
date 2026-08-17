# SCREEN PREREG — `SALTRAY`: the SALT×RAY coordination arm, scored as a **PACKAGE** head-to-head against the INCUMBENT

Drafted by a fresh opus subagent with NO inherited session context beyond the
inputs listed under `PROVENANCE`. The builder lane ratifies the judgment lines
and types the lock commit; this agent wrote no code under `bots/`, appended no
worklist row, appended no `docs/prereg/BARS.tsv` row, fired no game, started no
shard, and touched neither `results.tsv` nor `HANDOVER.md` nor `PROGRAMME.md`
nor `QUEUE.md`.

**STATUS: drafted BEFORE the `SALTRAY` row is appended to
`scratchpad/corefill_work.txt`, BEFORE any `docs/prereg/BARS.tsv` row exists,
BEFORE any file named `scratchpad/overnight/SALTRAY*` exists, and BEFORE the
leg's first game.** Drafting session wall clock at write time
**`2026-08-17T18:27:42Z`** (`date -u`, same shell call); repo HEAD at draft
`6bd92590` (author time `2026-08-17 20:26:28 +0200`). Verified at draft:
`grep -c SALTRAY docs/prereg/BARS.tsv` → **0**;
`grep -c SALTRAY scratchpad/corefill_work.txt` → **0**;
`ls scratchpad/overnight/ | grep -ci saltray` → **0**.
**Seed base 870000 verified free:** `git grep 870000` returns exactly three
files — two `league_matches` rows where the digits are a coincidental substring
of an Elo float (`0.41543898700005855`), and `docs/coordination.md:71145`, which
is the builder's own reservation of this base for this shard. No tape, worklist
row, BARS row or `results.tsv` row uses it.

### LOCK, clock 2 (local shard)
Per the obligations doc's **2026-08-17T07:24:55Z addendum**, copied from its
registered boilerplate rather than restated. **PRIMARY:** the shard tape's own
`# FIXTURE … start=` stamp (`tools/overnight.sh:99` sets `START=$(date -u …)`,
`:103` writes it to the tape before the first game). Quote it verbatim beside
the lock commit's git author time. **BACKSTOP, if the tape carries no
`# FIXTURE` line:** the tape's FIRST COMPLETED ROW `ts` — conservative by
construction (measured cost 1–2 s on the 107 stamped local tapes).
⛔ **NOT AVAILABLE: the heartbeat's `STARTING` line** (`overnight.sh:100` writes
it with `>`; every later state overwrites it). **State which clock was used.**
This shard is registered **LOCAL and SAME-HOST**, so the primary is expected.

### ⭐ COMMIT PROVENANCE — BOTH TREES ARE GIT-PINNED AND CLEAN
Unlike `RAYDISC` (whose treatment was untracked at draft and tripped
`OB13_UNTRACKED_ARM`), **both arms here are tracked with an empty porcelain**:
* **TREATMENT `bots/_v509saltray`** — `git ls-files` lists all four modules;
  `git status --porcelain bots/_v509saltray` is **empty**; digests at draft
  `doctrine.py 5b6dbb3d27ddf4ef9fb28f6c68ec6164` ·
  `eco.py e98885cfd4cb68b2c70d0764291bb2ed` ·
  `main.py a3b708156bb9a5c8262cb3aedf4bce99` ·
  `raid.py fa5cf9914e958d1bedf21b90eb9e5dde`.
* **CONTROL `bots/_v488beltbreak2`** — `git ls-files` lists all four;
  porcelain **empty**; newest commit touching it **`997bcd42`
  (2026-08-17 11:12:38 +0200)**; digests
  `doctrine.py b572a721531b77a8c27102bf64313996` ·
  `eco.py 47dc496fc0d14ba950c45c3d43a5f9d0` ·
  `main.py d7f31eedc6795956b72b541eb383c896` ·
  `raid.py c89950470aca51bfaed68712f3690220`.
⚠ **The same caveat RAYDISC carried still applies and is not repaired by
tracking:** "the control is the same bytes that produced the completed
`beltbreak2-final` 53.09% tape" is inferred from working-tree cleanliness, not
from a stamp on that tape. The tape has no tree-digest column. It is a sound
inference and it is an inference.

---

## ⛔ READ BEFORE RATIFYING — SIX THINGS THE LANE OWNS

**1. ⛔⛔ THE BIGGEST THING ON THIS PAGE: THIS ARM'S OWN FAMILY ALREADY RAN
AGAINST THIS EXACT CONTROL AND READ 48.82%. THE 54.00 ADDITIVE PREDICTION WAS
NOT REPRODUCED, SO THE `COMBO-BAR-EXEMPT` CLASS IS **NOT** CLAIMABLE HERE.**
`results.tsv:raydisc-final` / `raydisc-final-correction`: `RAYDISC`
(`_v507raydiscipline`, the FIRST generation of this stack) vs **the identical
control `bots/_v488beltbreak2`** floor-stopped at `TREND-FLOOR@1000` and its
full tape reads **48.82% [46.24, 51.40] at n = 1440** — CI containing 50 and
**EXCLUDING the 52.0 floor**. Its registered decomposition: kill-wins 601 vs
kill-losses 631 (margin **−30**), r1000 208 games.
**⇒ THE ONE ADDITIVE PREDICTION THIS FAMILY EVER REGISTERED (50.00 + 0.276 ×
14.5 = 54.00) WAS CONTRADICTED IN DIRECTION BY ITS OWN SHARD.** The exemption at
`tools/auto_gate.py:906-919` is defined for *"a MECHANISM test scored against
its own additive prediction"*; a prediction whose only instance was falsified,
re-used one generation later with two further unmeasured transfer steps (the FF
guard's dose SUPPRESSION, then this clause's dose RESTORATION), is not an honest
prediction. **This page therefore DOES NOT claim `COMBO-BAR-EXEMPT`, and
`COMBO_BAR = 55.0` BINDS on the n = 2700 prefix.** Said plainly rather than
argued around.
⚠ **AND THE SOLO RULING DOES NOT REACH HERE EITHER.** Magnus's
`BELTBREAK-EARLY` / `BELTBREAK2` grants (`docs/prereg/BARS.tsv:310,312`) rest on
*"this arm is a SOLO plank … not a combination"*. **Against this control that is
FALSE for this tree: all FOUR modules differ** (`doctrine.py` 354 diff lines,
`main.py` 266, `raid.py` 200, `eco.py` 8) and the package carries **three**
mechanisms. **The `combo_of()` classification defect is real and inherited — the
compose marker at `bots/_v509saltray/doctrine.py:2078` is byte-identical to the
carrier's at the same line — but this arm would read COMBO on the merits anyway.**
An escalation to Magnus is available to the builder; **a self-granted token is
not**, and an escalation would have to argue the opposite of the paragraph above.

**2. ⛔⛔ PRICED BEFORE THE FIRE, AND IT IS NOT FLATTERING: UNEXEMPTED, THIS
SHARD ALMOST CERTAINLY DOES NOT COMPLETE.** Prefix looks are one-shot at each
mark (`auto_gate.py`, `Tape.wins_at_mid` / `wins_at_half`); naive normal,
Z95 = 1.96, local DEFF 0.98 ⇒ no inflation. SE = 1.581pp at n=1000, 0.957pp at
n=2700 (p≈.55):

```
true share   P(TREND-FLOOR@1000   P(COMBO@2700 stop,   P(reach n=5400)
             stop, prefix<52.0)   prefix<55.0)
  49.0             0.972                ~1.000            0.000
  51.0             0.737                ~1.000            0.000
  52.0             0.500                0.9991            0.000
  53.0             0.263                0.982             0.013
  54.0             0.102                0.852             0.133
  55.0             0.028                0.500            0.486
```
**⇒ under ANY prior this family's own measurements support (48.8 – 52),
P(completion) is under 2%, and the modal outcome of firing is a
`TREND-FLOOR@1000` cancellation at ~1000–1500 games.** That is not a reason the
leg is worthless — a 1000-game prefix against the incumbent, with the F-reads
already banked, prices the package — **but it must be the builder's stated
expectation before a core is spent, not a surprise at 21:00.**
**And the ceiling arithmetic says the same thing independently** (see `SEGMENT
VALUE CEILING`): at the family's best measured on-dosed effect (+14.5pp) and its
best measured dosed fraction (27.6%), the pooled ceiling is **+4.00pp = 54.00** —
**below the 55.0 gate that binds.** ⇒ **the diversion component of this package
cannot clear its own binding gate even if every optimistic input is true.**
Anything that gets this arm past 2700 has to come from the OTHER two mechanisms.

**3. ATTRIBUTION SCOPE — STATED HONESTLY: THIS CELL MEASURES THE WHOLE RAY
STACK, NOT THE SALTRAY CLAUSE.** Treatment `_v509saltray` = incumbent
`_v488beltbreak2` **+ RAYDISC diversion (v507) + FF guard (v508) + SALTRAY
coordination (v509)**. Clause isolation for the coordination clause would be
`_v509saltray` vs `_v508raydisc2` and **is NOT being run today** — one core
only, per Magnus's one-plank directive (`docs/coordination.md:71094`).
**CONSEQUENCES, all registered:**
* **A pass promotes the STACK.** No sentence at readout may attribute a pass to
  the SALTRAY coordination clause. **The clause's own measured share delta is
  `−2.0pp ± 3.9` (fixture A, cluster-correct) and `−0.4 ± 8.4` (fixture B)** —
  point estimates NEGATIVE, both unpowered, both including 0.
* **A fail does not refute the coordination clause either**, and it does not
  refute the FF guard, which is a CORRECTNESS FIX (22.1% own-builder-hit games →
  0) whose value is not conditional on this bar.
* **The one component with a prior against it is the diversion** (`#1`).
  A pass would most plausibly mean *"the FF guard recovered what RAYDISC lost"*,
  and **this leg cannot separate that from the coordination clause.** Named now
  so it is not discovered as an explanation afterwards.

**4. ⭐ THIS ARM'S BUILD BATTERY ALREADY ANSWERED `RAYDISC`'s OPEN
DISCRIMINATOR, AND THE ANSWER MAKES THIS LEG'S PRIOR WORSE, NOT BETTER.**
`results.tsv:raydisc-final` left branch 1 (*"the dose collapsed under
`NOISE_ON`"*) vs branch 3 (*"dose present, effect ≈ 0"*) undecided and named a
~180-game NOISE-ON battery as the next step. **The v509 build report's fixture B
IS that battery's regime**: independent `NOISE_ON`, 270 games, **effective econ
dose 0.756 ± 0.178 per game with the coordination on** and refusals collapsing
**−2.185 ± 1.011 (CI clear of 0)**. ⇒ **the diversion FIRES at `NOISE_ON`.
Branch 1 is refuted; `RAYDISC`'s 48.82% is branch 3.** Banked here because it is
a cross-leg finding the family owes, and because it removes the most optimistic
reading of `#1`.

**5. THE SHARD'S REGIME IS `NOISE_ON`, AND THE BUILD REPORT'S SEED LAW DOES NOT
TRANSFER TO IT.** `bots/_v509saltray/doctrine.py:474` and
`bots/_v488beltbreak2/doctrine.py:474` are both `NOISE_ON = True`, and
`tools/overnight.sh:31` records that this is deliberate (*"NOISE_ON IS
DELIBERATELY LEFT TRUE (gate.py would FAIL it) … we want THE BEHAVIOUR WE
SHIP"*). The salt is an **unseeded** `random.Random()`, so two games at one
`--seed` are not reproducible and no two rows are a matched pair.
⛔ **THE BUILD REPORT'S NEW LAW — *"SEED INERT UNDER `NOISE_OFF` with fixed map +
deterministic bots; 35/50 (map,seat) groups produced one identical game across
9-10 seeds; intervals from this fixture MUST be clustered on (map,seat)"* —
GOVERNS FIXTURE A ONLY.** It is the reason the build report's A-fixture
intervals are cluster-corrected and it is **not applicable to this shard**.
Importing `(map,seat)` clustering here would inflate every interval on this page
for a degeneracy the shard does not have. **Registered: `CLUSTER UNIT: none`,
DEFF 0.98, naive.** The enumeration is performed in the registration block, not
asserted.

**6. ZERO-SUM SELF-LEG, AND THE CANCEL-FOR-CAPACITY POLICY, PRE-COMMITTED.**
The control is this tree's own ancestor chassis, so **"our win" and "their loss"
are the SAME EVENT** — every per-side metric is mechanically anti-correlated
with its counterpart, which is why the kill-clock reads are registered
WITHIN-ARM and the r300 bar is a one-sided safety backstop (`#`
`KILL-ROUND NON-REGRESSION`). The structural null on an unengaged game is
**exactly 50.00**, not "about 50": with no diversion and no yield the treatment's
code path IS the incumbent's (432/432 ON-undosed cells byte-identical; the three
gated `SLOT_ECO_READY` writes are provably dead — three writers, zero readers in
any ancestor).
⭐ **AND: Magnus's one-plank directive gives the ferry-siege plank priority
(`docs/coordination.md:71094`). PRE-REGISTERED NOW so it cannot be improvised
later: if the builder stops this shard to return the core to ferry-siege work,
that is an OPERATIONAL CANCELLATION FOR CAPACITY — typed `cancellation`, POLICY
AND NOT EVIDENCE.** It licenses no sentence about whether the stack pays, the
partial share is disclosed as **unselected** (a capacity stop is blind to the
share, unlike a floor stop, so the ~+2pp selected-pessimistic regression does
NOT apply to it — and saying so is required, because quoting the floor-stop
caveat on a capacity stop would understate the arm), and the rows are kept.

---

## RATIFY: Hypothesis

**HYPOTHESIS (a PACKAGE statement, not a one-mechanism statement).** *The
three-mechanism ray stack — forward-sentinel ray diversion to economy targets
(`LOKI_RAYDISC_*`, BUDGET 6/life, CORE_HP_STOP 90), the friendly-fire guard that
refuses a diversion onto a tile occupied by OUR OWN builder, and the SALT×RAY
coordination that recovers the dose that guard suppresses (publish the blocked
tile + facing on `SLOT_RAY_YIELD`; the raider seat-swaps out of the way) —
together produce a LOCAL pooled game share of **51.33% or higher** against the
incumbent `bots/_v488beltbreak2` at n = 5,400 games across all 15 corefill maps
and both seats, WITHOUT pushing our own kill past r300.* Registered direction
**POSITIVE**.

**THE ONE-PACKAGE STATEMENT, with its scope caveat inline.** This is **NOT** a
one-mechanism test and this page never calls it one. Against this control the
treatment differs in all four modules and in three mechanisms; the leg's
estimand is the STACK's share against the incumbent. **Clause isolation for the
SALTRAY coordination (vs `_v508raydisc2`) is a separate, unregistered leg that
is NOT being run** — see READ-BEFORE-RATIFYING #3.

**THE MECHANISM CHAIN, stated so it can be wrong.** v508 measured that the FF
guard fixes the friendly-fire defect cleanly (own-builder hits 0.429/game → 0)
but **SUPPRESSES rather than REDIRECTS** the dose (effective economy dose 0.695
→ 0.517/game), because the shielded tile is usually the ONLY eligible tile on
the ray (`es = 1` throughout), so a refused diversion falls back to the core.
⭐ **The builder-time discovery this arm exists for: the builder standing on the
enemy belt tile is OUR OWN SALT RAIDER, and it is CAGED THERE BY OUR OWN
`LOKI_BARRIER_SEAL` COLLAR** — at 204 published-tile events, move cooldown 0 but
`can_move` False in all four cardinals in **202 (99.0%)**; neighbours were 561
our-own-barrier (`can_destroy` True 561/561), 204 the ENEMY CORE (one per event),
47 wall, 4 passable. **A step-off plank would have fired 2/204.** The actuator is
therefore a **SEAT SWAP**: destroy one own barrier (free, no cooldown, and
measured NOT to spend the move — 54/54 in A, 18/18 in B), step into it, keep the
seat and the peck. **The tile vacated is the enemy's core-adjacent delivery
conveyor — the highest-value belt kill on the board — which v508's guard was
declining every reload for the rest of the match (same tile republished r187,
189, 191, 193, …).**
**The claim is therefore narrow and falsifiable: recovering that one tile is
worth more than the raider-round it costs, at a 4-round hold and a 2-per-life
barrier budget — and the stack that contains it beats the incumbent.**

---

## REGISTRATION BLOCK

**TARGET BAND: N/A — local corefill screen with ZERO rated ladder exposure: no submission, no activation, no unrated challenge, so `tools/target_value.py` has no input. Nothing on this page ends in a ship.**
**PINNED: N/A — local self-play against our own ancestor chassis. The opponent version is fixed by construction: the control tree is `bots/_v488beltbreak2` at commit `997bcd42`, git-tracked and working-tree clean at draft, digests quoted under COMMIT PROVENANCE. There is no opponent churn to pin against and no calibration relevance to protect. ⚠ DISCLOSED: the control is NOT the corefill `scratchpad/CONTROL_PIN` tree (`bots/_v468kladturbo`); it is deliberately the INCUMBENT and current live holder v159 Sleipnir v2, which is why every share on this page is written `X% vs _v488beltbreak2` and never bare.**
**SURFACE: local**
**CLUSTER UNIT: none** — CLAUDE.md's enumeration PERFORMED, not asserted, over FOUR candidates: (i) **MATCH** — does not exist on this surface: `tools/overnight.sh` writes one TSV row per `fcode run`, so 1 row = 1 game and no row shares a match with another; (ii) **OPPONENT** — degenerate: all 5,400 rows play the identical control tree, so the pooled stratum holds exactly one opponent and there is no between-opponent variation for a design effect to describe; (iii) **HOST** — killed by REGISTRATION, not measurement: this shard is registered SAME-HOST (LOCAL), and the obligations doc's Addendum 11 rider (the 0.98 exemption is a WITHIN-HOST measurement; cross-host pooling is not covered) makes splitting it across hosts an amendment typed BEFORE the first row; (iv) **SEED** — examined because `overnight.sh:134` advances the seed only every 16 games, so 16 rows share one engine seed. It dies for two reasons: those 16 rows span 8 distinct maps × 2 seats, so no two share a map, and `NOISE_ON = True` puts an UNSEEDED `random.Random()` in the bot (`main.py`, spawn salt), so two rows at one seed are not even reproducible let alone correlated. ⚠ **This fourth dismissal is REASONED, not separately measured** — what covers it empirically is the local constant itself, measured pair-weighted on 124 shards run by this same runner. All candidates die ⇒ DEFF = the measured local constant **0.98** (ρ = −0.020, s39 audit), i.e. **NAIVE intervals are correct and marginally conservative. The platform constants (1.529 rated / 1.833 unrated) are NOT applicable and importing them would widen every interval here by 24-35% for correlation measured absent. The build report's (map,seat) clustering law applies to its own NOISE_OFF fixture A and NOT to this shard (READ-BEFORE-RATIFYING #5).**
**ESTIMATOR: the unweighted pooled treatment game share** = (rows with `winner == T`) / (completed rows), over all 5,400 rows, both seats pooled, all 15 maps pooled, no reweighting. The shard is exactly balanced (15 maps × 2 seats × 180), so the pooled and map-stratified equal-weight shares coincide by construction; the stratified form is an arithmetic consistency check only, never a second estimator (s28 ring-hold: four estimators inside 0.010 of one bar flipped MEET/MISS among themselves). Seat A and seat B shares are reported SEPARATELY as a fixture diagnostic and are never a bar — seat is worth ~7.6pp on byte-identical arms, which is why n is a multiple of 30. **The r1000/core-kill DECOMPOSITION of the share is a MANDATORY companion read on the same rows: it cannot rescue a failed bar and it CAN downgrade a passing one (THIRD FALSIFIER).** ⛔ **The arm-name normalisation hazard the build report recorded applies to any comparator written for this tape: the shard `winner` column holds an ARM DIRECTORY NAME and a raw read gave 77/162 false non-equivalence at build time — normalise to US/OPP before scoring.** Any estimate quoted at readout arrives from `tools/cluster_ci.py` (HEAD); the pre-data half-widths here are closed-form Wald with DEFF 0.98 and their arithmetic is shown inline.
**DOSE: the SALT×RAY yield — 64 publishes → 10 step-offs + 54 cage-breaks (100% conversion) on fixture A (paired deterministic `NOISE_OFF`, 27 maps × 2 seats, `--tle 10`, n=486 games per arm), and 26 publishes → 8 + 18 (100% conversion) on fixture B (independent `NOISE_ON`, n=270 games — THE SHARD'S OWN REGIME); flag-off arm 0 publishes / 0 step-offs / 0 cage-breaks on the same `LOKI_SALTRAY_LOG = True` binary, over the matched cells (n=162 cells, all 162 identical to `_v508raydisc2`).** **BOTH VERDICTS PRESENT AND THE ZERO IS NOT A BLIND ZERO — it is the same binary, the same maps and the same seeds with `SALTRAY_COORD_ON = False`, and the flag-off tree is `_v508raydisc2` byte-for-byte across 162/162 cells (plus 432/432 ON-undosed cells identical).** **THE WELL-POWERED SIGNAL IS THE REFUSAL COLLAPSE: 2.621 → 0.255 guard-refusals per game (−90.3%); fixture B −2.185 ± 1.011, CI clear of 0.** ⛔ **AND THE DOSE ITSELF IS NOT POWERED ON THIS FIXTURE, DECLARED RATHER THAN BURIED: effective economy dose +0.163 ± 0.057 naive but +0.162 ± 0.172 cluster-correct (CI INCLUDES 0) on A, +0.130 ± 0.256 on B, because only 6 of 50 independent cells ever dose (26/270 games). The local fixture cannot power the dose.** Own-builder hits: **0/415 shots (A), 0/270 games (B), 0/336 flag-off**, against a forced `FF_GUARD = False` arm at **22.1% (38/172 games), 0.235/game** — the guard driven to its other verdict, reproducing s49's 21.8% [11.1, 38.4].
**PLANNED n: 5400 games** (= 15 maps × 2 seats × 180, exact map and seat balance; `tools/overnight.sh:68` has run a 15-map pool since the 2026-08-13 rotation and requires multiples of 30). ⛔ **5400 IS SAID EXPLICITLY because a solo shard otherwise defaults to a 2700 TARGET, and at 2700 the bar's 1.33pp margin is unreachable against a ±1.87pp half-width.**
**BOUNDARY: 5400 games** — LOCAL surface, one tape row is one game; no accept/attempt distinction and no accepts count. ⛔ **A LINE COUNT IS NOT A ROW COUNT**: the tape carries an unprefixed header line under the `# FIXTURE` line, so a naive `wc -l` over-reports n by exactly one. The registered denominator is **DictReader row count over non-`#` lines, cross-checked against the heartbeat's `n TARGET` and against `max(game id) + 1`.**
**CUT-SHORT: floor 2700 games.** Below 2,700 completed rows this arm publishes descriptive tallies (share, per-seat, per-map, per-class, kill-round, `cond` mix, the r1000/core-kill decomposition) and takes **NO bar verdict**; the one-sample half-width at 2,700 is ±1.87pp, already wider than the 1.33pp margin the bar is built on. ⛔ **AND ON THIS ARM THE SUB-FLOOR BRANCH IS THE MODAL ONE (READ-BEFORE-RATIFYING #2), so it is written first, not last.** An `auto_gate` firing at CATASTROPHE@400, MARK-1000, TREND-FLOOR@1000, COMBO-BAR@2700 or the CI rule at MARK-2700 is an **OPERATIONAL CANCELLATION, not a verdict**, typed `cancellation`; so is a builder cancel-for-capacity (READ-BEFORE-RATIFYING #6). ⭐ **ONE CARVE-OUT, PRE-COMMITTED:** a CATASTROPHE-clause cancellation (95% CI upper < 45.0 at n ≥ 400) is arithmetically INCOMPATIBLE with every band above Band 4, so a stop under that clause DOES license the Band-4 sentence at the partial n — provided the partial share is disclosed as **selected-pessimistic** (a floor stop fires on a LOW PREFIX DRAW; expect roughly +2pp of regression — side lane s47, n=2 cases, a DIRECTION with a rough size, not a calibrated correction). ⛔ **NO OTHER CLAUSE'S CANCELLATION LICENSES ANY BAND**, and a capacity stop is UNSELECTED and carries no regression caveat at all.
**BAR: 51.33. MDE: 0.00pp — THIS BAR IS A POINT RULE ONLY AND LICENSES NO EXCLUSION CLAIM ABOUT AN EFFECT SIZE** (OB16 corollary, 2026-08-15T03:52:45Z: the standard corefill band IS `50 ± half_width` at n = 5,400, so clearing 51.33 puts the CI's lower edge at exactly 50.00 — it excludes 50 and excludes no positive effect size). n for the one exclusion it CAN make (bar ≠ 50.0): **5,400**, the planned n. ⭐ **The OB16-form statement is available for free on the BAND: Band 1 requires the CI LOWER bound ≥ 51.33, which carries an implied minimum effect of +1.33pp. That is a property of the BAND, not of the BAR, and the two must not be conflated in a readout sentence.** **The r300 admission read is the OTHER bar on this page and it IS sized.**
**BASE RATE: 50.00**
**BAR SOURCE:** the house-standard corefill futility band, `50 + 1.96*sqrt(0.25/5400) = 51.33pp`, local DEFF 0.98 so naive — the identical bar carried by `docs/prereg/BARS.tsv` rows `SEALFLOOR6`, `SENTTHR`, `KLADTKILL`, `KLADTK2`, `KLADTURBOR`, `DRAINTURBO`, `KLADLADDER`, `SEALSENTAN`, `SEALSENTA`, `ROUTESCORE`, `BELTBREAK-EARLY`, `BELTBREAK2` and `RAYDISC`, which keeps this arm numerically comparable to the family it extends — **and specifically to `RAYDISC`, the same treatment family against the same control on the same bar.** **Constructed, not observed.** ⭐ Its null is STRUCTURAL here rather than merely calibrated: an unengaged game is incumbent-vs-incumbent.
**BASE RATE SOURCE:** structural A/A expectation of a seat-balanced, map-balanced self-play fixture whose control tree IS the treatment's own ancestor chassis, with the added property that the undosed complement is byte-identical (432/432 at build). Empirically calibrated on the same host and fixture by `IDNULL140` — **49.27% [47.94, 50.60] at n = 5,400** (`results.tsv:idnull140-cert-5400`) — and by `NULL125` — **51.04% at n = 5,400** (`results.tsv:null125-final`). Two A/A cells, one either side of 50.0, both intervals containing it. ⚠ **The two cells are 1.77pp apart**, so a bare clearance in [51.33, 52.4] is a band an A/A cell has already produced — which is why Band 2 is pre-registered as WEAK. **Disclosed before the data.**
**REFERENCE n: none** — the bar's comparator is a STRUCTURAL null of 50.00 generated inside this same shard. ⛔ **`RAYDISC`'s 48.82% [46.24, 51.40] at n = 1440 is NOT registered as a reference SAMPLE and no bar on this page is sized against it.** It is the same control and the same family, so it is the honest PRIOR (READ-BEFORE-RATIFYING #1) and it is quoted as one — but it is a DIFFERENT TREATMENT TREE at a different n, and naming it as a reference sample would make the checker size 51.33 as a two-fixture comparison and correctly FAIL it: a true statement about a bar nobody registered. ⛔ **The incumbent's own 53.09% vs `_v468kladturbo` (`results.tsv:beltbreak2-final`) is likewise NOT a reference here** — different fixture, different opponent, and local screens are not transitive in this repo (QUEUE #65: 3 concordant, 1 not).
**TREATMENT TREE: bots/_v509saltray**
**TREATMENT DIFF REFS: 163d8eb1^ 163d8eb1**
⚠ **THE REF PAIR AND ITS LIMITATION, stated rather than left for a certifier.** `163d8eb1` is the commit that introduced `bots/_v509saltray` (all four modules added; `git log --diff-filter=A -- bots/_v509saltray/main.py` → `163d8eb1`), and naming it is what makes the OB13 intersection machine-computable. **But an ADD-commit intersects EVERY path in the tree, so the git check is weak on its own.** The strong form is the CROSS-TREE diff, which git cannot express as a ref pair: `diff -u bots/_v488beltbreak2/<mod>.py bots/_v509saltray/<mod>.py` for all four modules, reproduced under THE CHANGE, sizes verified at draft (doctrine.py 354 changed lines, main.py 266, raid.py 200, eco.py 8; `cmp` clean on NONE of the four), with the control pinned at `997bcd42` and unchanged since (`git status --porcelain bots/_v488beltbreak2` empty). **What defeats the weak reading is the grep pair under MECHANISM METRIC READS: the metric sites read structurally 0 in the control.**
**MECHANISM METRIC READS: `bots/_v509saltray/raid.py:441` — `ct.destroy(Position(p.x + mx, p.y + my))`, inside `_sr_break_cage` (`:380-459`): the SEAT SWAP, the ONE site at which this arm physically clears a published tile. Companion sites in the same diff, both new and both absent from the control: `bots/_v509saltray/main.py:1108` — `self._sr_publish(ct, sr_blk)`, the publish, reached only when the FF guard refused a candidate AND no clean candidate survived AND the shot is about to fall back to the core (`:1104-1107`); and `bots/_v509saltray/main.py:1116` — `ct.fire(rd_best)`, the inherited RAYDISC diversion. TREATMENT DIFF TOUCHES: bots/_v509saltray/doctrine.py bots/_v509saltray/main.py bots/_v509saltray/raid.py bots/_v509saltray/eco.py. INTERSECTION: yes — every metric site is a NEW LINE in a changed file, the strongest form of the intersection, needing no import-binding argument (the constants they read also bind through `from doctrine import *`). ⚠ A path-only intersection would ALSO pass here and that reading is REFUSED: the metric sites do not exist in the control at all (`grep -c` over the control's four modules: `SALTRAY` 0, `_sr_break_cage` 0, `_sr_yield` 0, `sr_publish` 0, `RAYDISC` 0, against 40 / 2 / 3 / 2 / 32 in the treatment), so the metric CANNOT read identically in the two arms — it reads structurally 0 in the control. That is the LOKI-18 failure this obligation exists for.**
**METRIC WINDOW: r0-r1000. GATING CONSTANTS: SALTRAY_COORD_ON=True, SLOT_RAY_YIELD=5, LOKI_SALTRAY_STALE=3, LOKI_SALTRAY_HOLD=4, LOKI_SALTRAY_MAX_BREAK=2, LOKI_SALTRAY_LOG=False, LOKI_RAYDISC_ON=True, LOKI_RAYDISC_FWD_DSQ=50, LOKI_RAYDISC_MAX_HP=36, LOKI_RAYDISC_BUDGET=6, LOKI_RAYDISC_CORE_HP_STOP=90, HUNT_BAND_DSQ=41, NOISE_ON=True. MECHANISM CAN OCCUR IN WINDOW: yes** — **NOT ONE of these is a round gate.** `STALE` and `HOLD` are round DURATIONS measured from a live event, not thresholds against the absolute round; `MAX_BREAK` is a per-life count; `SLOT_RAY_YIELD` is a store index; `FWD_DSQ`/`HUNT_BAND_DSQ` are squared distances; `MAX_HP`/`CORE_HP_STOP` are hit points; `BUDGET` is a per-unit-per-life shot count; the rest are switches. ⭐ **WHAT DOES BOUND THE WINDOW IN PRACTICE, so it is not read as a promise: nothing can fire before a FORWARD SENTINEL exists and fires — measured at first-fire r137 and UNCHANGED between arms — so the observed mass lives in roughly r137-r1000 and r0-r136 is empty in BOTH arms. That is a property of the chassis, not of these clauses.** ⚠ **DISCLOSED so a green tool run with warnings under it does not launder them: `prereg_check.py` will emit `OBLIGATION 17, PARTIAL WINDOW` warns against the line above and THEY ARE CHECKER ARTEFACTS** — its `check_metric_window` arithmetic reads every declared integer as a ROUND, so a d² of 50, an HP of 36, a hold of 4 and a store index of 5 all render as "rounds r0-r<v-1> cannot contain the mechanism". The constants are declared anyway.
**PLANK CLASS: OFFENSIVE — an economy-denial shot-discipline package on a forward TURRET plus a raider-side coordination clause; not a defensive turret purchase, not a home screen, and not an economic plank in the `titanium_collected` sense.** ⭐ **AND THE r300 ADMISSION READ IS REGISTERED ANYWAY, NOT CLAIMED INAPPLICABLE.** Two of the three mechanisms are deliberate deferrals: the diversion defers core damage (arithmetically up to BUDGET 6 × reload 2 = **12 rounds per forward sentinel, hard, never resetting**), and the yield/hold forfeits a raider's peck for up to `LOKI_SALTRAY_HOLD = 4` rounds plus the round of the swap. **A plank whose mechanism is a delay must carry a delay bar whatever its class label.** Registering it is strictly stricter than the programme requires and CANNOT function as a second chance to pass: **both the share bar and the r300 bar must hold.**
**KILL-ROUND NON-REGRESSION: ITT RMST₃₀₀ is the operational estimator (PROGRAMME.md's 2026-08-16T05:36:10Z arbitration, binding on preregs locked from that date — this one is) — mean kill time censored at the r300 horizon over ALL games, a non-kill scoring 300, computed per side on the same rows; scored as an EXCLUSION: the 95% CI UPPER bound on (treatment RMST₃₀₀ − control RMST₃₀₀) must EXCLUDE +5.0 rounds (MDE +5.0; the paired per-game sd is recomputed from THIS tape at readout and the half-width with it — the sibling-family anchor is sd ≈ 89 rounds ⇒ ±2.37 at n=5,400, so the exclusion resolves). SECOND REGISTERED FORM, both required: the ITT timely-kill-by-r300 rate (share of ALL games ending `cond == core_destroyed` with `turns <= 300`, denominator every game played, per side) — its 95% CI LOWER bound on (treatment − control) must EXCLUDE a fall of 3.0pp (MDE 3.0pp; sd anchor 75.28pp ⇒ ±2.01pp at n=5,400). THIRD, a DIAGNOSTIC ONLY because it carries a collider: the kill-win-CONDITIONED share and conditioned median — reported beside the two bars, never as either. The treatment's own median kill round crossing 300 is the gross within-arm backstop. ANCHORS, quoted as anchors and not predictions: the build battery read kill≤r300 at **117/486 in BOTH arms EXACTLY** and timely-kill **+4.8 ± 7.4 (B)**; the incumbent's own completed tape (`results.tsv:beltbreak2-final`) reads timely-kill **30.80% [29.56, 32.03]** and r1000 share **11.28%**. ⚠ ZERO-SUM DISCLOSURE, registered with the bar: on a self-leg the two sides' kill counts partition one set of games, so this difference is CONFOUNDED WITH THE SHARE and a PASS in a winning arm is partly automatic — the bar is a ONE-SIDED BACKSTOP against "wins more, all added wins past r300" and licenses no claim that the arm speeds the kill.**
**PRE-STATE: the predicted-change behaviour is NOT already in the target state at lock.** Verified at draft against the control tree: `grep -c` over `bots/_v488beltbreak2/{doctrine,eco,main,raid}.py` returns **SALTRAY 0 · RAYDISC 0 · sr_publish 0 · _sr_yield 0 · _sr_break_cage 0**, against **40 · 32 · 2 · 3 · 2** in the treatment. **The incumbent has no ray-discipline path and no coordination channel at all: every forward-sentinel shot in the control goes to the highest-`TURRET_PRIO` tile on the ray, which is the CORE whenever a core tile is on it, and no raider ever vacates a tile for a turret.** ⇒ the behaviour this leg predicts to change cannot already be in the target state. The OUTCOME claim is likewise not pre-satisfied: `_v509saltray`'s share against the incumbent **does not exist on any tape** (`grep -c SALTRAY` → 0 on the worklist, the registry, `results.tsv` and every shard tape at draft), and every band below — including two sign-reversed ones — is a live, pre-named outcome.
**MAP SEGMENT: EXPECTED — terrain conditions the TRIGGER, and this is a CORRECTION of the sibling prereg, not an inheritance from it.** `PREREG-RAYDISC` registered `MAP SEGMENT: none expected`; that was **measured FALSE** (`docs/coordination.md:70829`, s49 build relay): the dosed fraction runs **frostgate 54.8% → fjordgate 4.8%, monotone, MAP DEFF 3.709**, with the funnel **58.9% of games ever fire forward · 39.6% of those dose · es ≥ 1 on 13.5% of fires**. **Registered here per OB15b as a WRITTEN-DOWN conditioning fact, not a promoted segment.** ⛔ **AND THE 3.709 IS A DEFF ON THE TRIGGER RATE ACROSS MAPS, NOT ON THE POOLED SHARE INTERVAL:** the shard is map-BALANCED, so map is a stratum and not a cluster and the pooled naive interval stands (READ-BEFORE-RATIFYING #5). What the heterogeneity bounds is what a per-map cut can resolve: 360 games/map ⇒ half-width **±5.17pp**, so no single map cell can carry a verdict. Per-map, per-seat and CQ/STD/GRAND tables (`tools/overnight_read.py:76-94 map_area_class`) are computed and reported DESCRIPTIVELY and may not rescue a failed bar.
**PRIMARY SEGMENT: the BELT-HEAVY / BELT-LIGHT map split, fixed BLIND before readout from the trigger-rate ordering already banked at `docs/coordination.md:70829` — HIGH-DOSE end anchored by `frostgate` (54.8%), LOW-DOSE end anchored by `fjordgate` (4.8%).** ⛔ **THE FULL 15-MAP ORDERING IS NOT IN THE REPO — only the two endpoints and the monotonicity are recorded — so the registered segment is the TWO NAMED ENDPOINT MAPS, not a five-map bucket that would have to be reconstructed after the data exist.** Registered prediction: **on `fjordgate` both arms read ~50.0 (the mechanism is nearly inexpressible there in BOTH arms), and whatever pooled effect exists concentrates toward the `frostgate` end.** ⚠ **MEASURED ON THE SHARD, unlike `RAYDISC`'s dose split: the map is on the tape (`ts shard game map seed seat winner cond turns`), so this segment IS shard-native — but the DOSE ITSELF IS NOT, so the segment is a PROXY for dose and is labelled one.**
**EXPECTED DIRECTION: POSITIVE overall and POSITIVE-OR-ZERO on the high-dose end; ~50.0 (no effect) on `fjordgate`.**
**SEGMENT VALUE CEILING: 27.6% × 14.5pp = 4.00pp pooled ⇒ a ceiling of 54.00 for the DIVERSION component.** The share is the dosed-game fraction (69 of 250 cells, measured IDENTICAL in both arms at build; consistent with the independent funnel 0.589 × 0.396 = 23.3%); the on-segment effect is the family's best measured on-dosed difference (+14.5pp [+6.1, +22.9]). ⇒ **the dilution is a HARD CAP on that component: 51.33 pooled needs +4.82pp on-dosed, 52.0 (the trend floor) needs +7.25pp, and 55.0 (the combo bar that binds) needs +18.1pp — above the point estimate and above most of its own CI.** ⛔ **DECLARED LIMITATION OF THIS TOKEN: it covers ONE of the package's three mechanisms.** The FF guard's correctness value (removing 0.235 own-builder hits/game across the 58.9% of games that fire forward) and the coordination clause's recovery are NOT bounded by the dosed fraction and have NO independent share measurement against the incumbent — so the package's true ceiling is unknown and is larger than 4.00pp. **A single number cannot honestly express it, and inventing one would be worse than saying so.**
**POOL ERA: post-2026-08-13-rotation** — the 15-map local pool of `tools/overnight.sh:68`. (`check_pool_era` treats this as n/a on a LOCAL surface per SPEC §6; declared anyway so the population is on the page.)
**CELL VERSION CHURN: N/A — not a panel, no `CELLS:` line, one fixed local control tree.**
**GATE RESOLUTION: three gates, sized separately.**
* **(a) THE SHARE BAR.** Margin 1.33pp against a one-sample half-width of ±1.334pp at n=5,400, DEFF 0.98 — resolvable, and only just. ⚠ **The slack is ~0.00pp, which is `GUNAXABL`'s exact failure mode (missed its keep edge by 0.0152pp — ONE GAME — on a bar with zero constructed slack). Registered consequence: a result within one game of the bar is reported as "the fixture cannot resolve the question", not as a verdict in whichever direction the rounding falls.**
* **(b) THE r300 ADMISSION BAR.** RMST₃₀₀: MDE +5.0 rounds against half-width ±2.37 → resolves. Timely-kill: MDE 3.0pp against ±2.01pp → resolves. Both scored as exclusions, both separated by construction.
* **(c) THE OPERATIONAL FLOORS, AND ON THIS ARM THEY ARE THE GATE MOST LIKELY TO DECIDE ITS FATE.** The pinned `tools/auto_gate.py` marks CATASTROPHE@400 (CI-hi < 45.0, `:244,247`), MARK-1000 / TREND-FLOOR@1000 (prefix < 52.0, `:261`), **COMBO-BAR@2700 (prefix < 55.0, `:278`) — WHICH BINDS, UNEXEMPTED (READ-BEFORE-RATIFYING #1)** — and the CI rule at MARK-2700 with its half-a-half-width margin; the bar plausibility guard (`:398-406`, `[30,70]`) admits 51.33. Their firings are OPERATIONAL CANCELLATIONS that free a core, typed `cancellation`, never `verdict`. **The floors bind REMOTE too (`a50f27ef`, s48), so the binding registration is SAME HOST — one host, LOCAL; moving it is an amendment typed BEFORE the first row.** ⛔ **PRICED IN READ-BEFORE-RATIFYING #2: P(completion) is under 2% at every true share this family's own measurements support.**
**Everything else on this page (F1, F2, F3, D3, D4, the seat / map / class splits) is DIAGNOSTIC and cannot rescue a failed bar. Any branch that does not resolve is UNRESOLVED, and an UNRESOLVED gate defaults to the RESTRICTION: no promotion, no ship conversation, no combination claim.**

---

## ⛔ RATIFICATION BLOCKERS — THREE THINGS THE BUILDER MUST SETTLE BEFORE LOCKING

**B1. RATIFY OR OVERRIDE THE NO-EXEMPTION CALL, IN WRITING.** This page declines
`COMBO-BAR-EXEMPT` (READ-BEFORE-RATIFYING #1) and therefore fires into a 55.0
gate at 2700 with a sub-2% completion probability. **Three defensible branches
and the builder must pick one on the record:** (i) fire unexempted, accepting
that the modal output is a ~1000-game prefix read; (ii) escalate to Magnus for a
grant — **noting that the escalation cannot use the `BELTBREAK` solo argument,
because all four modules and three mechanisms differ here**; (iii) do not fire,
and give the core to ferry-siege now. **Firing without choosing is not a branch.**

**B2. STATE WHETHER THE F-READS ARE SATISFIED PRE-LOCK, OR ORDER THE BATTERY.**
This page registers F1-F3 as **SATISFIED BY THE PRE-LOCK BUILD BATTERY**,
because fixture B (`NOISE_ON`, 270 games) is the shard's own regime and already
carries all three numbers — unlike `RAYDISC`, whose F1 did not exist at lock and
whose shard then died with the discriminator unanswered. **If the builder
disagrees, the battery must be ordered BEFORE the shard starts, not after**; the
FIRINGS-BEFORE-PRIMARY sequence is hard and an amendment after the fire cannot
repair a registration.

**B3. CONFIRM THE SHARD IS SAME-HOST AND SERIAL WITH THE FERRY-SIEGE WORK.**
The registration is LOCAL, SAME-HOST, one core. Magnus's directive
(`docs/coordination.md:71094`) puts ferry-siege next and this shard on one core
in the meantime. **The cancel-for-capacity policy is pre-registered
(READ-BEFORE-RATIFYING #6); what is NOT pre-registered and must be is whether a
second worker may be added mid-run** — it may not, without an amendment typed
before the first row (Addendum 11 rider: the 0.98 exemption is a WITHIN-HOST
measurement).

---

## THE DOSE EVIDENCE — FIRINGS ONLY, NO EFFECT SIZES BANKED

**⛔ THIS SECTION IS BANKED MECHANISM EVIDENCE FROM `docs/research/BUILD-REPORT-v509saltray-2026-08-17.md`. IT CONTAINS NO OUTCOME NUMBER THIS PAGE MAY USE AS ONE.**
Fixture A = paired deterministic `NOISE_OFF`, 27 maps × 2 seats, `--tle 10`;
fixture B = independent `NOISE_ON` (**the shard's regime**), 270 games;
opponent = a namespaced `_v488beltbreak2` copy.

| quantity | coord-OFF | coord-ON (this arm) |
|---|---|---|
| **own-builder hits** | 0/336 | **0/415 shots (A), 0/270 games (B)** |
| **guard refusals per game** | **2.621** | **0.255** — B Δ **−2.185 ± 1.011**, CI clear of 0 |
| **yield events** | 0 publishes / 0 / 0 | A **64 → 10 step-offs + 54 cage-breaks (100%)**; B **26 → 8 + 18 (100%)** |
| **effective econ dose** | A 0.646/g | A 0.809/g; B **0.756 ± 0.178** |
| dose Δ | — | **+0.163 ± 0.057 naive; +0.162 ± 0.172 CLUSTER-CORRECT (CI INCLUDES 0)**; B +0.130 ± 0.256 |
| **flag-off equivalence** | — | **162/162 cells identical vs `_v508raydisc2`; 432/432 ON-undosed cells identical** |
| SALT composition | 36.78 fires/g | 36.08 (A) — paired Δ **−0.680 ± 1.373**, flat |
| escape cost | 0 | 54 barriers demolished / 486 games (**0.11/g**); `MAX_BREAK` cap **never observed binding** |

* **THE GUARD IS DRIVEN BOTH WAYS:** a forced `FF_GUARD = False` arm reads
  **22.1% own-hit games (38/172), 0.235/game**, reproducing s49's 21.8%
  [11.1, 38.4]. **The 0 is not a blind zero.**
* **THE YIELD IS DRIVEN BOTH WAYS:** the flag-off arm runs the SAME
  `LOKI_SALTRAY_LOG = True` binary and reads 0/0/0.
* ⛔ **THE DOSE IS NOT POWERED HERE AND THE PAGE SAYS SO:** 6/50 independent
  cells ever dose (26/270 games). **The refusal collapse, not the dose, is the
  well-powered signal.**
* ⚠ **`MAX_BREAK = 2` NEVER BOUND**, so the rail that makes a demolition loop
  impossible is correct-by-construction and **unverified by measurement**. It is
  declared under GATING CONSTANTS and must never be quoted as a driven control.
* ⛔ **TLE / CPU CANNOT BE MEASURED LOCALLY AND THE LOCAL NUMBER IS
  UNINFORMATIVE, NOT ZERO** (obligations doc, s42 addendum: local replays carry
  no exec-time fields; `get_cpu_time_elapsed()` returns 0 on local unit-turns).
  The structural argument is what carries and it names the asymmetry: the arm
  adds, **in the treatment only**, one `read_store` per raider turn, one
  `write_store` + one `get_direction()` on a publishing sentinel, and a
  four-neighbour scan on a caged raider. `--tle 10` caps a timeout engine-side.
  `LOKI_SALTRAY_LOG = False` in the shipped tree, so the stderr instrument costs
  nothing — **and the LOG-enabled battery copy is a different tree and must
  never be the one screened.**

---

## FALSIFIER

**PRIMARY FALSIFIER: at n = 5,400 the 95% CI UPPER bound on this arm's pooled
share vs `bots/_v488beltbreak2` falls BELOW 51.33.** That excludes the arm's own
bar on the fixture whose null is structural.

**SECOND FALSIFIER (the r300 admission bar, and it can fail alone while the
share passes):** the 95% CI UPPER bound on (treatment − control) ITT RMST₃₀₀
fails to EXCLUDE +5.0 rounds, **or** the CI LOWER bound on the ITT
timely-kill-by-r300 difference fails to EXCLUDE a fall of 3.0pp. **Either is
disqualifying on its own, regardless of the share** — `PLAY_DEFENCE:
not_at_the_kill_s_expense`, and two of this package's three mechanisms ARE
bounded deferrals. Read with the zero-sum disclosure attached to the bar.

**THIRD FALSIFIER (the doctrine composition):** the share gain over 50.00 is
**majority r1000 tiebreak wins**. Then the reading is downgraded one band and
labelled `OFF-DOCTRINE COMPOSITION` — combination input only, no ship
conversation, no head-to-head. **Registered as a falsifier and not a caveat
because the family has already produced this shape: `RAYDISC`'s build battery
decomposed +4 kill-wins / −10 kill-losses / +5 r1000 (all wins) — the boundary
case — and its shard then read 208 r1000 games out of 1440.**

**SEGMENT FALSIFIER:** **`fjordgate` (the measured 4.8%-dose end) must read
50.0 ± its own half-width (±5.17pp at 360 games) in this shard.** If the
low-dose map moves hard while the high-dose end does not, the pooled effect is
not coming from the mechanism this page describes and the reading is
**ATTRIBUTION UNRESOLVED — promotes nothing EVEN IF THE BAR CLEARS.** ⚠ **Its
power is declared: at ±5.17pp this clause catches a GROSS discordance and cannot
resolve a 3pp one (OB12; the unresolved case defaults to the restriction).**

**MECHANISM FALSIFIER (independent of all of the above, and it fires FIRST):**
* if **F1** shows guard-refusals per game NOT collapsing in the shard's regime,
  the package is not in the state its build measured and the primary reads
  **NOT MEASURED**, never null;
* if **F2** shows zero yield events, the coordination clause never fired and a
  flat share is a **WIRING NULL**, not a finding about coordination;
* ⛔ **if F3 shows ANY own-builder hit, the FF guard invariant is broken. That is
  an INSTRUMENT ALARM AND A HARD STOP: the shard is cancelled, the tree is
  quarantined, and no share on this page is read at all** — a tree that shoots
  our own builders is not the tree the build report certified.

### ⭐ THE HONEST-NULL CLAUSE — pre-committed, because two of these nulls are informative

| state | evidence | pre-committed reading |
|---|---|---|
| **(1) STOPPED BY A FLOOR OR THE COMBO BAR** | prefix < 52.0 @1000 or < 55.0 @2700 | **CANCELLED — UNRESOLVED, defaults to the RESTRICTION.** The modal branch (READ-BEFORE-RATIFYING #2). Rows KEPT; the partial disclosed as **selected-pessimistic** (~+2pp expected regression; n=2 cases, a DIRECTION not a correction). ⭐ **AND IT IS NOT CONTENT-FREE: a second floor stop for this family against this control, after `RAYDISC`'s 48.82, is a repeated observation about the ray stack and is banked as one — with the caveat that a stop is a low-draw selection and two of them are still not a verdict.** |
| **(2) COMPLETED, SHARE FLAT OR NEGATIVE** | n=5,400, CI contains or sits below 50 | ⭐ **A REAL FINDING: the ray stack does not beat the chassis it sits on, even with the friendly-fire defect fixed and the dose recovered.** That closes the *"RAYDISC failed only because the FF collision suppressed the dose"* reading, which is currently the family's most attractive excuse. **Attribution bound: it does NOT price the FF guard (a correctness fix that stands regardless) and it does NOT price the coordination clause in isolation** — that needs the `_v509saltray` vs `_v508raydisc2` leg, which is NOT this one. |
| **(3) COMPLETED, SHARE CLEARS, GAIN IS MAJORITY r1000** | F-reads clean, bar clears, decomposition majority tiebreak | ⭐ **ALSO A REAL FINDING, and the shape the family has already shown once.** The stack delivered SURVIVAL, not KILLING: `OFF-DOCTRINE COMPOSITION`, combination input only, banked as a fact about the mechanism (belt denial buys longevity, not tempo). |

---

## READING, PRE-COMMITTED

**Read TOP-DOWN; the first row whose condition holds is the reading. Rows are
disjoint by construction. Every band is CONDITIONAL on F1-F3 having been read
and written down first, on the r300 admission bar having HELD, and on the
r1000/core-kill decomposition having been computed. An r300 failure overrides
every row (`OFF-PROGRAMME — kill delayed`, whatever the share). A majority-r1000
composition DOWNGRADES the row by one and appends `OFF-DOCTRINE COMPOSITION`.
An own-builder hit voids every row (hard stop).**

| # | band on the pooled share vs `bots/_v488beltbreak2` at n = 5,400 | pre-committed reading |
|---|---|---|
| **1** | **CI lower ≥ 51.33** | **THE RAY STACK BEATS THE INCUMBENT.** Real and resolved on a structural null. ⛔ **PROMOTES THE PACKAGE, NOT THE CLAUSE** (READ-BEFORE-RATIFYING #3): the next step is the clause-isolation leg `_v509saltray` vs `_v508raydisc2`, and only then a head-to-head against the holder. Report the size with its OB16 status: the BAR's MDE is 0; clearing this BAND excludes 50.00 AND 51.33, so an implied minimum effect of +1.33pp may be claimed and nothing larger. |
| **2** | **point ≥ 51.33 but CI lower < 51.33** | **REAL-BUT-SMALL, COMBINATION INPUT ONLY.** Pre-registered as WEAK: `NULL125`'s byte-identical A/A read 51.04 and the two A/A cells are 1.77pp apart. Rows KEPT; no ship conversation; a replication on fresh seeds, same host, is the price of promoting it — **reported SEPARATELY and never pooled** (GUNAXABL/SENTTHR precedent: unregistered pooling is optional stopping with extra steps). |
| **3** | **point < 51.33 AND CI contains 50.0** | **PARITY — THE STACK IS FREE.** The diversion, the guard and the coordination together pay for themselves and nothing more. ⭐ **Against `RAYDISC`'s 48.82 that is still an UPWARD move for the family and it must be reported as such — with the caveat that the two figures come from different n and different trees and the difference is not a registered estimand.** Does NOT license a ship. |
| **4** | **CI upper < 50.0** | **THE STACK SUBTRACTS ON OUR OWN CHASSIS.** `LOKI_RAYDISC_ON = True` dies as a ship candidate at this dose, and the coordination clause does not rescue it. Attribution bounded: this refutes *the three-mechanism package at BUDGET 6 / HOLD 4 / MAX_BREAK 2*, **not** *forward sentinels*, **not** *the FF guard* (a correctness fix that stands on its own evidence), **not** *the beltbreak family*, and **not** *economy denial in general*. **REGISTERED CONSEQUENCE: the core plink is confirmed as the better forward-sentinel shot on our own chassis, no further gate-order arm is written on the sentinel path, and the surviving shot-side lever is the beltbreak GUNNER.** |

⚠ **Nothing here treats 50.0 as a floor.** A share below 50 is a live outcome
with named mechanisms — up to 12 rounds of deferred core damage per forward
sentinel; a raider forfeiting its peck for up to 5 rounds per yield; a
demolished seal barrier re-opening a spawn seat for `LOKI_SALTRAY_HOLD` rounds —
and it is pre-named so a negative is not explained away as noise.

⛔ **AND ONE CROSS-BAND NOTE: an operational cancellation reaches NONE of these
rows** — floor, combo bar, or capacity. The reading is `CANCELLED — UNRESOLVED,
defaults to the RESTRICTION`.

---

## FIRINGS-BEFORE-PRIMARY — READ AND WRITTEN DOWN BEFORE THE PRIMARY IS TYPED

⛔ **THE RULE IS A HARD SEQUENCE** (`docs/prereg/BARS.tsv` header, research
2026-08-16T13:27:33Z): **F1-F3 are read, and their numbers written down, BEFORE
any sentence containing this arm's primary share is typed.** A primary typed
ahead of the firings read is a REGISTRATION BREACH regardless of what it says,
and the repair is an amendment chain, not a re-write. *(Precedent:
`results.tsv:kladladder-verdict-amendment-f1f2-pending`.)*

⛔ **THE SHARD ITSELF CANNOT SEE THE MECHANISM.** `tools/overnight.sh:138-139`
runs every game with `--replay /dev/null`; the tape's columns are
`ts shard game map seed seat winner cond turns` — **no entity, build, position,
shot, turret or store information exists on it, in either arm.** Every F-number
below comes from the PRE-LOCK BUILD BATTERY and **the shard's 5,400 rows lend
them none of their power.**

**REGISTERED AS SATISFIED PRE-LOCK (see B2), on fixture B — the shard's own
`NOISE_ON` regime, 270 games — with fixture A quoted beside it:**

* **F1 — GUARD-REFUSAL COLLAPSE (the well-powered signal).**
  **2.621 → 0.255 refusals/game (−90.3%); fixture B Δ −2.185 ± 1.011, CI clear
  of 0.** Read: **the FF guard's suppression is genuinely relieved.** This is the
  number the coordination clause exists to move and the only mechanism quantity
  this fixture can power. **A readout that omits it has not performed F1.**
* **F2 — YIELD EVENTS > 0, PUBLISH → CONVERSION.**
  **A: 64 publishes → 10 step-offs + 54 cage-breaks = 100% conversion.
  B: 26 → 8 + 18 = 100%.** Flag-off arm: **0 / 0 / 0** on the same LOG binary.
  Read: **the channel is wired end to end and the actuator that carries it is
  the SEAT SWAP (54 of 64 in A, 18 of 26 in B), not the step-off the plank was
  briefed as** — which is the build's headline surprise and is banked, not
  explained away.
* **F3 — OWN-BUILDER HITS STAY 0 (the FF invariant).**
  **0/415 shots (A), 0/270 games (B), 0/336 flag-off**, against a forced
  `FF_GUARD = False` arm at **22.1% (38/172), 0.235/game**. Read: **the
  invariant holds and the guard has been driven to its other verdict.**
  ⛔ **STOP RULE: any own-builder hit observed on this tree at any later point is
  an INSTRUMENT ALARM AND A HARD STOP — the shard is cancelled and no share is
  read.**

**NOT MEASURABLE on this leg — named, not silently dropped.**
* **DIVERSIONS, YIELDS, REFUSALS, BUDGET USE AND BARRIER DEMOLITIONS ARE NOT
  DECODABLE OFF THE SHARD** (`--replay /dev/null`; local corefill keeps TAPES,
  not REPLAYS; and `LOKI_SALTRAY_LOG = False` in the screened tree).
* **THE DOSED/UNDOSED SPLIT IS NOT COMPUTABLE ON THE SHARD.** `NOISE_ON = True`
  defeats pairing and the tape carries no dose marker. **The map split registered
  as PRIMARY SEGMENT is a shard-native PROXY for it and is labelled one.**
* **THE THREE MECHANISMS CANNOT BE SEPARATED ON THIS LEG** (READ-BEFORE-
  RATIFYING #3). No amount of tape reading recovers a decomposition the design
  does not contain.
* **PER-UNIT CPU / TLE.** Blind zero locally; labelled UNINFORMATIVE, not clean.
* **ANYTHING ABOUT THE FIELD.** The opponent is our own chassis; the 27.6%
  trigger rate is a fact about OUR belt-laying policy. `CLAUDE.md` rule 6: **this
  page closes no road.**

**D3, D4 — the outcome-shape reads. MEASURABLE, shard-native** (`cond` and
`turns` are on the tape): **D3** = the r300 admission bar, both forms, per side,
off `tools/cluster_ci.py --null`, read with the zero-sum disclosure; **D4** =
`cond` mix per arm, the treatment's own median kill round (crossing 300 is
disqualifying), and **the mandatory r1000/core-kill split of the share gain**
that the THIRD FALSIFIER is denominated in. Anchors:
`results.tsv:beltbreak2-final` timely-kill **30.80% [29.56, 32.03]**, r1000
share **11.28%**; `results.tsv:raydisc-final-correction` kill-wins 601 / losses
631, r1000 208 of 1440.

---

## THE CHANGE — `file:line`, incumbent → treatment

**TREATMENT `bots/_v509saltray`** = `bots/_v488beltbreak2` **plus three
mechanisms in four files.** Re-runnable in four commands (all four DIFFER; none
is `cmp`-clean, which is itself the honest statement of scope):

```
$ diff bots/_v488beltbreak2/doctrine.py bots/_v509saltray/doctrine.py | grep -c '^[<>]'   # 354
$ diff bots/_v488beltbreak2/main.py     bots/_v509saltray/main.py     | grep -c '^[<>]'   # 266
$ diff bots/_v488beltbreak2/raid.py     bots/_v509saltray/raid.py     | grep -c '^[<>]'   # 200
$ diff bots/_v488beltbreak2/eco.py      bots/_v509saltray/eco.py      | grep -c '^[<>]'   #   8
```

**INHERITED FROM `_v507raydiscipline` (mechanism 1 — the diversion):**
`doctrine.py:2085-2256` (RAYDISCIPLINE constants) · `main.py:167-187` per-sentinel
state · `main.py:989-1108` the two-pass sentinel scan with core→belt diversion
(`BUDGET = 6/life`, `CORE_HP_STOP = 90`) · `main.py:1112-1186` `_rd_forward` +
logging · the fire site `main.py:1116 ct.fire(rd_best)`.

**INHERITED FROM `_v508raydisc2` (mechanism 2 — the FF guard):** ONE condition —
refuse a diversion candidate when OUR builder stands on the tile; enemy-builder
tiles stay legal and are counted apart. ⭐ **BYTE-IDENTICAL v508 → v509** (the
diff of v508 `main.py:1024-1051` against v509 `main.py:1048-1075` is empty).

**NEW IN `_v509saltray` (mechanism 3 — the coordination):**
* `doctrine.py:2257-2429` — the LOKI-SALTRAY block + the CAGE block:
  `SALTRAY_COORD_ON = True` (`:2347`), `SLOT_RAY_YIELD = SLOT_ECO_READY` = slot 5
  (`:2350`), `LOKI_SALTRAY_STALE = 3`, `HOLD = 4`, `MAX_BREAK = 2`, `LOG = False`.
* `main.py:188-200` per-unit state; `main.py:1020-1026` + `:1088-1091` remember
  the refused highest-value tile; **`main.py:1104-1108` the publish site**, which
  fires ONLY when the refusal actually cost the diversion (guard refused, no
  clean candidate survived, `rd_arm`, `best_prio == 0`, core HP above the endgame
  stop); `main.py:1192-1228` `_sr_publish` (one `write_store`, the whole body in
  one `try` — an escaping exception permanently destroys the sentinel).
* `raid.py:217-246` the yield call placed AHEAD of the action ladder (after
  exile detection) with the movement freeze; `raid.py:283-459` `_sr_yield`
  (`:285`, reads `SLOT_RAY_YIELD` at `:306`) and **`_sr_break_cage` (`:380-459`,
  the seat swap, `ct.destroy(...)` at `:441`)**.
* `main.py:317-321` + `eco.py:544-546,1697-1699` — the three dead
  `SLOT_ECO_READY` writes gated OFF so slot 5 has ONE writer class. **Provably
  dead: three writers, `read_store(SLOT_ECO_READY)` returns nothing in any
  ancestor.** With the flag OFF the dead writes are restored and the tree is
  `_v508raydisc2` exactly (162/162 cells).

**THE ENCODING** (one int, `SLOT_RAY_YIELD`): bits 0-5 x, 6-11 y, 12-13 dx+1,
14-15 dy+1, 16+ round+1; **0 = no request**. The FACING is in the packet because
"step off the ray" is not computable from the tile alone — every cardinal
neighbour of a tile shares its row or its column. The one-round write buffer is
respected by design: a tile published at R is readable at R+1, inside one
sentinel reload.

---

## SEEDS, SURFACE, RUNNER

**SEEDS: base 870000**, verified free at draft (see STATUS). `tools/overnight.sh`
advances the seed every 16 games, so this shard consumes **870000-870337**.
⛔ **Any battery run against this tree must use a base OUTSIDE that range** so no
battery game can collide with a screened game.
**SURFACE: LOCAL, SAME-HOST, one worker** (`WORKERS` unset ⇒ 1).
**RUNNER:** `zsh tools/overnight.sh SALTRAY bots/_v509saltray bots/_v488beltbreak2 5400 870000`
— basenames do not collide (`_v509saltray` vs `_v488beltbreak2`), so the
substring guard at `overnight.sh:76-79` passes.
**GATE:** `tools/auto_gate.py` against the `SALTRAY` row below, **unexempted**.

---

## READY-TO-PASTE `docs/prereg/BARS.tsv` ROW

*(Tab-separated, four columns: `name`, `bar`, `cmp`, `source`. The builder types
it — BARS row BEFORE the worklist row, per the BELTBREAKR lesson. The worklist
row that follows is
`SALTRAY<TAB>bots/_v509saltray<TAB>bots/_v488beltbreak2<TAB>5400<TAB>870000`.)*

```
SALTRAY	51.33	ge	docs/prereg/PREREG-SALTRAY-2026-08-17.md — DECISION bar 51.33 ge, POINT RULE (OB16, MDE 0.00), n=5400, h2h share, LOCAL SAME-HOST seeds 870000. Locked <TS> PRE-START by the builder (s50); drafted by a fresh opus agent, judgment lines ratified by the lane. PACKAGE HEAD-TO-HEAD, NOT CLAUSE ISOLATION: TREATMENT bots/_v509saltray vs CONTROL bots/_v488beltbreak2 (the INCUMBENT and live holder v159 Sleipnir v2 — both ours; SELF-LEG: win and loss are the same event, kill-round metrics WITHIN-ARM only). THREE mechanisms differ (RAYDISC ray diversion + v508 FF guard + v509 SALT×RAY coordination) across ALL FOUR modules (doctrine 354 / main 266 / raid 200 / eco 8 diff lines) — a pass promotes the STACK and attribution to the coordination clause is CAPPED; clause isolation would be vs _v508raydisc2 and is NOT being run (one core, Magnus one-plank directive). ⛔ NO COMBO-BAR EXEMPTION CLAIMED AND COMBO_BAR=55.0 BINDS AT 2700: the token's registered purpose (auto_gate.py:906-919) is a mechanism test scored against its own ADDITIVE PREDICTION, and this family's only registered prediction (50.00+0.276x14.5=54.00) was CONTRADICTED by its own shard — RAYDISC vs this same control read 48.82% [46.24,51.40] n=1440 (results.tsv:raydisc-final-correction), kill margin −30, r1000 208. The BELTBREAK solo grants do not reach here either: this tree is a genuine COMBINATION on the merits, not only via the inherited stack.py compose marker (doctrine.py:2078). ⛔ P(COMPLETION) PRICED PRE-FIRE AND IT IS UNDER 2% at every true share this family supports (TREND-FLOOR 52.0@1000 kills a true-51 arm 74% of the time; COMBO 55.0@2700 kills a true-54 arm 85%); the diversion component's own ceiling is 27.6% x 14.5pp = 4.00pp = 54.00, BELOW the gate that binds. The modal outcome of firing is a ~1000-game prefix cancellation, which is NOT a verdict. DOSE MEASURED PRE-LOCK (fixture B = the shard's own NOISE_ON regime, 270 games): guard-refusals 2.621→0.255/game (−90.3%, Δ −2.185±1.011 CI clear of 0) is the WELL-POWERED signal; yield 26 publishes→8 step-offs+18 cage-breaks (100% conversion, flag-off 0/0/0 same LOG binary); own-builder hits 0/270 vs 22.1% (38/172) on a forced FF_GUARD=False arm. ⛔ THE DOSE ITSELF IS NOT POWERED LOCALLY: 6/50 cells ever dose, cluster-correct Δ +0.162±0.172 (CI includes 0). FIRINGS-BEFORE-PRIMARY HARD, registered SATISFIED PRE-LOCK: F1 refusal collapse, F2 yield>0 with conversion, F3 own-hits==0 — all three transcribed into the readout BEFORE any sentence containing the primary share; ANY own-builder hit is an INSTRUMENT ALARM AND A HARD STOP that voids every band. SEGMENT: MAP dependence EXPECTED (corrects RAYDISC's "none expected", measured FALSE at docs/coordination.md:70829 — dosed fraction frostgate 54.8% → fjordgate 4.8%, monotone, MAP DEFF 3.709 on the TRIGGER RATE not on the pooled interval); PRIMARY SEGMENT = the two banked endpoint maps, and fjordgate MUST read 50.0±5.17pp or the reading is ATTRIBUTION UNRESOLVED EVEN IF THE BAR CLEARS. THIRD FALSIFIER: a majority-r1000 gain downgrades one band as OFF-DOCTRINE COMPOSITION (the family has already shown that shape). r300 ADMISSION BAR carried on an offensive plank because two of three mechanisms are deliberate deferrals (12 rounds/sentinel; HOLD 4 + swap round per yield): ITT RMST300 must EXCLUDE +5.0 rounds and ITT timely-kill must EXCLUDE a 3.0pp fall, either failure disqualifying alone. LOCAL surface: DEFF 0.98, naive intervals, platform constants 1.529/1.833 NOT imported; the build report's (map,seat) clustering law governs its NOISE_OFF fixture ONLY and does NOT apply to this NOISE_ON shard. CLUSTER UNIT none (match/opponent/host/seed all enumerated and dead). SAME-HOST REQUIRED; adding a worker mid-run needs an amendment typed before the first row. ⭐ CANCEL-FOR-CAPACITY PRE-REGISTERED: if the builder returns the core to the ferry-siege plank, that is POLICY AND NOT EVIDENCE — typed cancellation, partial disclosed as UNSELECTED (no selected-pessimistic regression caveat, unlike a floor stop), licenses no sentence about whether the stack pays.
```

---

**PROVENANCE: docs/research/BUILD-REPORT-v509saltray-2026-08-17.md · docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md · docs/prereg/PREREG-RAYDISC-2026-08-17.md · docs/prereg/BARS.tsv · PROGRAMME.md**
*Read in full by the drafting agent. Additional facts verified directly against
the repo at draft and cited inline where used:
`bots/_v509saltray/{doctrine,main,raid,eco}.py`,
`bots/_v488beltbreak2/{doctrine,main,raid,eco}.py`, `tools/overnight.sh`,
`tools/auto_gate.py`, `tools/prereg_check.py`,
`results.tsv:{beltbreak2-final,raydisc-final,raydisc-final-correction,raydisc-autostop-1000,idnull140-cert-5400,null125-final}`,
`docs/coordination.md:{70829,71094,71145}`, and `git ls-files` / `git status
--porcelain` / `md5` on both arm trees.*

---

## RATIFICATION (builder s50, 2026-08-17T18:37:19Z — the lane types this, per the fresh-drafter rule)

**B1 — RATIFIED: FIRE UNEXEMPTED.** COMBO_BAR=55.0 binds at 2700 as the page states; no
exemption is claimed. Reasons, in order: (1) Magnus's direct order this session ("you can
finish the saltray shard and put it on a core") — the fire decision is his and already made;
(2) the floors adjudicate cheaply and the modal ~1000-game prefix cancellation is an
acceptable, bounded closure of the family's local question; (3) cancel-for-capacity is
pre-registered as policy, so the core returns to the ferry-siege plank the moment it is
needed. The <2% completion pricing is acknowledged and does not override a direct fire order
with bounded cost. Escalation NOT chosen: re-asking would re-litigate a decision Magnus made
with the family context in hand.

**B2 — RATIFIED: F1-F3 SATISFIED PRE-LOCK on fixture B.** Fixture B is the shard's own
NOISE_ON regime (270 games); re-running the battery would re-measure the same fixture at no
additional inferential value. The F-numbers transcribed on this page (F1 −90.3% refusal
collapse, Δ −2.185±1.011; F2 26→8+18 at 100% conversion vs 0/0/0 flag-off; F3 0/270 vs 22.1%
forced-off) are adopted as the pre-start F-reads. Any own-builder hit in the shard remains an
instrument alarm and hard stop per the registered rule.

Judgment calls 1-10 of the drafter's summary: ratified as drafted, no overrides.
