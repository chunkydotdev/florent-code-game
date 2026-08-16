# LEG-fieldcal-2026-08-16 — LIVE UNRATED FALSIFICATION LEG: does `bodyaware` survive contact with real opponents?

**DRAFT for the builder's ratification. Drafted by a fresh opus subagent with no inherited session
context beyond the files on the `PROVENANCE` line.** The builder ratifies the judgment lines and
types the lock commit; the side lane certifies two-clock before the leg is created.

**⛔ ONE BLOCKING TODO BEFORE LOCK:** the `TARGET BAND:` line is a sentinel. `tools/prereg_check.py`
will FAIL on it until the builder fills it from live `fcode team search` reads. That failure is the
point — see §12.

---

## 0. WHAT THIS LEG IS FOR, IN ONE PARAGRAPH

Every decision on this line is driven by a LOCAL self-play screen against `bots/_v223sealrepair`
(v140), and **nothing links a local unit to the field.** This leg spends live unrated games to ask
the only question the local fixture structurally cannot answer: **does the `bodyaware` effect EXIST
against real opponents, or does it INVERT?** It is scoped as a **FALSIFICATION** leg because no
feasible n confirms the local magnitudes (§3). Its second product is arm-independent and durable:
the first field-anchored kill-timing read for this line, against ten PINNED opponent builds.

**AUTHORISATION.** Magnus, in-session 2026-08-16, verbatim: *"You're free to use the unrated
games"* — given in answer to the builder's go/no-go on this leg. This is the **explicit window**
that `PROGRAMME.md`'s `X3R0_SLOT_RULE` block requires (*"no leg fires until an arm clears 60±2
locally or Magnus explicitly opens a window"*). **This leg is a MEASUREMENT, not a slot move.** It
does not and cannot promote either arm: the slot pipeline is unchanged — (1) clear 60.0% with a
≤2pp half-width against the v140 control on the local screen, (2) head-to-head against the current
holder's staged artifact, (3) beat it ⇒ switch. The board's ceiling at this ruling is 55.24%, so
the standing state remains GRIND and no result here alters that.

---

## 1. REGISTRATION BLOCK

**STATUS:** committed BEFORE any challenge of this leg is created — RATIFIED AND LOCKED at the
commit carrying this line (builder s45, 2026-08-16:
TARGET_BAND filled from live reads; churn counts computed; §10.3 ruled between-windows; §10.5b
ratified; the commissioning brief preserved as `docs/prereg/BRIEF-fieldcal-2026-08-16.md`, verbatim
copy of the scratchpad path on the PROVENANCE line). This document is committed BEFORE the first
challenge of this leg is created. **Two-clock certificate, and the second clock is named because an unrated leg has no
ladder pairing to date it by:** clock 1 = the `git` author time of the lock commit of this file;
clock 2 = the **platform `createdAt` of the FIRST ACCEPTED CHALLENGE of the leg**, read off
`fcode match list --mine --type unrated`. ⛔ **NOT the first result row** — a result row is written
when a game FINISHES (~10–20 s late), and at a small gap that error decides the SIGN of "did the
prereg predate the leg?". Clock 2 must be strictly LATER than clock 1 and the gap is quoted.

**TARGET BAND:** 10 pinned cells, gaps -33..+115, win pays 0..0, reachable YES —
unrated pays no rating by design, band is informational field-relevance. Filled
at lock from LIVE `fcode team search` reads (builder,
2026-08-16 ~06:0xZ; ours 1786 #18, live `fcode status`): Juusto 1867 (+81) ·
not adgato 1898 (+112) · Erebus 1845 (+59) · kladde chatte tville 1827 (+41) ·
gsxWins 1821 (+35) · 0033 1785 (−1) · lingling_40h 1771 (−15) · HTTP 418 1754
(−32) · The Bisons 1753 (−33) · farming_200s 1901 (+115). Gaps −33..+115, all
inside the ±125 pairing-relevance band. **Win pays 0..0 — unrated pays no
rating by design; the band is INFORMATIONAL (field-relevance), reachable YES.**
Priced off live reads on both sides, never `target_value`'s cached opponent
column (the Juusto flip incident governs).

**CELL VERSION CHURN (numeric, Obligation 14, computed at lock off
`league_matches.tsv`, distinct versions in the preceding 24h):** Juusto 1 ·
not adgato 1 · Erebus **10 (HIGH-CHURN)** · kladde chatte tville **17
(HIGH-CHURN)** · gsxWins 6 · 0033 2 · lingling_40h 3 · HTTP 418 1 · The Bisons
2 (v9 pinned, v53 also live — pin may be off the opponent's current line) ·
farming_200s 1 (pin ~16h old, carried from §1). **The pin neutralises churn for
the T-vs-C contrast by construction; what churn degrades is FIELD RELEVANCE —
the two HIGH-CHURN cells (Erebus, kladde) are REPORTABLE, NOT POOLABLE into any
relevance claim, and are named here so the read-out cannot quietly pool them.**

**PINNED:** YES — this is a TREATMENT leg (matched pairs: same opponent, same pinned opponent
build, different arm of ours), so `docs/research/SPEC-opponent-pinning-2026-08-13.md`'s design rule
binds: **pin treatment legs, never pin calibration panels.** Opponent variation is pure noise a
matched-pair design cannot absorb. Every accept fires
`fcode match unrated <team_id> --match <pin_match_id>`. Both arms use the SAME pin id per cell.

**SURFACE:** unrated (live platform challenges, `fcode match unrated`). Not rated, not local.

**CLUSTER UNIT:** match+opponent (pooled) — for the POOLED reads (§5 secondary, §6 descriptive).
Enumerated per `CLAUDE.md`'s procedure rather than asserted: **MATCH cluster — an arm's pooled
stratum holds all 5 games of each of its 120 accepts ⇒ LIVE. OPPONENT cluster — an arm's pooled
stratum holds 12 accepts against each of 10 opponents ⇒ LIVE.** Both survive ⇒ pooled unrated
constants. ⭐ **The PRIMARY (§4) takes NO design effect at all: its unit of analysis is the OPPONENT
CELL (k=10), i.e. the cluster itself, so the exact binomial over 10 independent cells governs and
there is nothing left to correct for.** A DEFF applied there would be double-counting.

**ESTIMATOR:** PRIMARY — the **exact two-sided binomial sign test** over 10 pinned opponent cells
on `sign(game_share_TREAT − game_share_CTRL)` within each cell. A cell scores `+` iff the treatment
arm's game share in that cell strictly exceeds the control arm's; `−` iff strictly less; **TIE iff
exactly equal — ties are EXCLUDED and the test recomputed at the reduced k, with the tie count
reported** (standard sign-test handling, pre-committed here so it is not a choice made after the
data). SECONDARY — pooled **ITT RMST at horizon 300**: the mean over ALL games of `min(turns, 300)`
with any game not ending in our core-kill scoring the full 300. **Mean, not median: the ITT median
pins at the horizon** (only ~39% of games kill inside it), so the median is not an estimator here
and is not used as one. Boundary convention declared: `<300`, which `RMST-ESTIMATOR-2026-08-16.md`
§3 checked against `<=300` and found identical to 2dp on every arm.

**PLANNED n:** 1,200 games total — 600 games per arm, i.e. 10 pinned cells × 60 games per arm.

**BOUNDARY:** 240 accepts = 1,200 games (120 accepts = 600 games per arm; 12 accepts = 60 games per
arm in each of the 10 cells), then stop. Declared in BOTH units so the CAL-8 miscount — a boundary
counted over ATTEMPT lines instead of ACCEPTS — is visible as a broken identity rather than
invisible.

**CUT-SHORT:** 800 games total (40 games per arm in every surviving cell) is the floor for any
comparative claim. Below it: counts only, descriptive, no sign test, no reversal claim. **A cell
that does not reach 40 games per arm is EXCLUDED from the primary and named with its counts;** the
sign test is then recomputed at the surviving k with its exact two-sided p. **At k < 8 the primary
is UNRESOLVED and defaults to the restriction (§7).**

**BAR:** 9/10 opponent cells share the sign of (treatment − control) game share. Exact two-sided
binomial p = **0.0215** ⇒ MEET. **8/10 gives p = 0.1094 and is a MISS, not a partial credit.**

**⭐⭐ IMPOTENCE CLAUSE — REGISTERED AT BAR LEVEL, NOT AS PROSE, because a prose caveat gets quoted
past: THIS LEG CANNOT CONFIRM THE LOCAL MAGNITUDE. A POOLED NULL IS THE EXPECTED RESULT AND MUST
NOT BE READ AS REFUTING THE LOCAL FINDING.** The arithmetic behind it is §3, the power behind the
bar is §4, and both were computed before any game was fired.

**BASE RATE:** 5/10 cells — the null. Under no arm difference the sign of (T − C) is a fair coin in
each cell, so the expected count is 5 of 10 and any count is symmetric about it.

**BAR SOURCE:** constructed, not observed — the exact binomial distribution at k = 10 and
α = 0.05 two-sided. 9 is the smallest count whose two-sided tail clears α (0.0215); 8 does not
(0.1094). **MDE, inside the bar's construction per OB16's preferred form: the bar has 80% power
only if the treatment's true per-cell win probability π ≥ 0.92.** ⛔ **We will call this leg a MISS
on the primary if the true π is at or below 0.92 — which, at the local effect size, IT IS (π ≈ 0.63,
§4). The bar is therefore a HIGH-EVIDENCE-IF-IT-FIRES test, not a powered one, and this sentence is
registered so that nobody later quotes the miss as a refutation.** n for the 80%-power exclusion at
π ≈ 0.63: **k ≈ 109 pinned opponents.** Ten exist. That is the honest resolution statement and it
is why the FALSIFIER (§5), not the BAR, is what this leg is really buying.

**BASE RATE SOURCE:** the exact binomial null at k=10; no empirical population, no denominator to
audit. The empirical priors this leg tests against are LOCAL and are quoted separately with their
denominators in §2 (BODYAWR: RMST₃₀₀ −6.84 rounds [−8.61,−5.08], n = 10,800 games, local corefill
tapes, DEFF 0.98, `docs/research/RMST-ESTIMATOR-2026-08-16.md` §3; game share +3.70pp, same board).
⚠ **Both carry a SIDE-LANE-AUDIT-PENDING flag** — they are research's s45 board as of
2026-08-16 ~07:5xZ and the audit had not closed when this document was drafted.

**MECHANISM METRIC READS:** bots/_v242bodyaware/eco.py:813
**TREATMENT DIFF TOUCHES:** bots/_v242bodyaware/eco.py
**INTERSECTION:** yes — `eco.py` is the ONLY file that differs between the arms.

**TREATMENT TREE:** bots/_v242bodyaware
**TREATMENT DIFF REFS:** --no-index bots/_v223sealrepair/eco.py bots/_v242bodyaware/eco.py

**METRIC WINDOW:** r0-r1000. **GATING CONSTANTS:** none — `_bfs_direction`
(`bots/_v242bodyaware/eco.py:809-905`) carries no round gate in its own enclosing block; the four
`*_MIN_RND` names elsewhere in that file (`:233` HUNT, `:241` SURGE, `:1152`/`:1155` MEDIC) are
imported from `doctrine.py` and gate hunt/surge/medic behaviour, not the step chooser.
**MECHANISM CAN OCCUR IN WINDOW:** yes — the step chooser is called on every builder move from r0,
so the mechanism is live for the whole game in both arms and the metric is not inert.

**GATE RESOLUTION:** the primary's three branches and the n at which they separate — ≥9/10 same
sign ⇒ MEET (p ≤ 0.0215); exactly 8/10 ⇒ **UNRESOLVED** (p = 0.1094); ≤7/10 ⇒ MISS on the primary,
which by the impotence clause is the EXPECTED outcome and carries no refutation. **Power against
the local effect: 7.0% on game share, 9.9% on RMST₃₀₀ (§4). The gate cannot discriminate its
branches at the effect size it is aimed at, and that is stated here in advance rather than
discovered at read-out.** ⛔ **AN UNRESOLVED GATE DEFAULTS TO THE RESTRICTION, NEVER THE
PERMISSION** — see §7 for what each branch may and may not be written down as.

**MAP SEGMENT:** none registered for this leg — **and that is NOT a claim of map-invariance.** See
§8, which declares the deviation from Obligation 15a's two canonical forms rather than hiding it.

**PRE-STATE:** the outcome is not already in its target state at lock. **(a)** No field ITT RMST₃₀₀
and no field per-cell game-share sign has ever been computed for `bodyaware` on any surface — the
predicted-change quantity is unmeasured at lock, so the prediction cannot be pre-satisfied.
**(b) Outcome type declared, per Obligation 7:** the primary is **neither** a win-condition MIX
**nor** a win-condition IN-OUR-FAVOUR claim. It is a **game-share sign per opponent cell**,
computed over ALL games of both arms — wins, losses, tiebreaks and non-kills alike. The
mix/favour ambiguity that sank the 15:46 conversion prereg does not arise. **(c)** The secondary
(RMST₃₀₀) is likewise ITT over all games with non-kills scoring 300, so no treatment effect can
move its denominator.

**CELLS:** Juusto v13 · not adgato v23 · Erebus v119 · kladde chatte tville v119 · gsxWins v46 ·
0033 v57 · lingling_40h v61 · HTTP 418 v103 · The Bisons v9 · farming_200s v15 — 10 pinned cells;
Pantheon and The Flotte Experience DROPPED (no pin available).

**CELL VERSION CHURN:** the pin NEUTRALISES churn for the matched comparison by construction —
both arms meet the same frozen opponent build in every cell, which is exactly what
`SPEC-opponent-pinning` says pinning is for. ⚠ **Obligation 14's numeric requirement is NOT
discharged by that argument and is REQUIRED AT LOCK:** the builder writes, per cell, the opponent's
distinct-version count over the preceding 24 h off `league_matches.tsv` (free), because a
high-churn cell whose pin is stale is measuring an opponent the ladder no longer runs — reportable,
not poolable. **Known already, and carried:** `farming_200s`' pin is **~16 h old** at fire time and
its age must appear in the read-out (SPEC failure mode 2). All 10 pins were corroborated 7/7 by the
side lane and research jointly — `Juusto v13` is present in `ladder_games.tsv` (5 rows; the pin
match at 05:32:59Z is newer than the archive's newest row at 04:52:59Z, pure archiver lag) and
`Erebus v119` in `league_matches.tsv` (9 observations, newest 2026-08-16T04:52:59Z; absent from
`ladder_games.tsv` BY DESIGN because the pin match is unrated). ⛔ **Corroborating that a version
EXISTS is not confirming that a given match id PLAYS it. The only detector for that is the
post-fire assertion in §9.3, which is therefore load-bearing and not good practice.**

**POOL ERA:** 2026-08-16T00:00:00Z..now
All of this leg's games are fired inside the current map era, which opened when the ten new maps
entered the rated pool (first new-map game 2026-08-13T07:12:59Z per
`docs/research/KILL-HAZARD-REDERIVED-2026-08-16.md` §1). The local board the priors come from was
run this session on the same post-rotation pool; local shards measure 66.7% new-pool against the
ladder's 66.0%. No pool boundary is crossed by the declared window.

**DOSE:** BODYAWR moves the local kill-timing estimator by -6.84 rounds [-8.61,-5.08] (n=10,800 games) vs +0.42 rounds [-1.96,+2.81] on the byte-identical-copy control (NULL114, n=5,408 games)
The probe therefore carries BOTH verdicts: the mechanism fires on the treatment arm, and the
byte-identical control returns to baseline. That is what makes the first number mean anything.

**FALSIFIER:** see §5 — a pooled REVERSAL beyond the leg's own detectable band: pooled game share
(T − C) **≤ −7.7pp**, or pooled ITT RMST₃₀₀ (T − C) **≥ +10.1 rounds**.

**PROVENANCE:** /private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/41f6d66d-d70a-4c2c-be0e-ab1dca841ae7/scratchpad/leg_brief_2026-08-16.md; PROGRAMME.md; docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md; docs/research/SPEC-opponent-pinning-2026-08-13.md; docs/research/KILL-HAZARD-REDERIVED-2026-08-16.md; docs/builder-method.md; docs/research/RMST-ESTIMATOR-2026-08-16.md; docs/coordination.md (tail only: FIRE ORDER #2 2026-08-16T08:2xZ, the 08:4xZ amendment, the side lane's 05:4xZ OB17 check, and the builder's 05:42:15Z re-scope)

---

## 2. THE ARMS

| | tree | identity | what it is |
|---|---|---|---|
| **ARM A — control** | `bots/_v223sealrepair` | v140 | the `PROGRAMME.md` `INCUMBENT`; the control every local screen on this line is denominated in |
| **ARM B — treatment** | `bots/_v242bodyaware` | BODYAWR | v140 **plus one plank**: the `#63` body-aware step chooser |

**The diff is ONE FILE.** `doctrine.py`, `main.py` and `raid.py` are byte-identical between the
arms; `eco.py` differs, and the change is confined to `_bfs_direction` (`:809-905`): builder bots of
**either team** seen in vision are collected into a `bodies` set and treated as soft obstacles by
the step chooser, with the goal-selection block hoisted (declared in the source comment as pure code
motion: `desired`/`side`/`order` depend only on `p`, `target`, `self.idx` and `CARDINALS`).

### 2.1 ⭐ THE TREATMENT-ARM DECISION — RATIFIED BY THE BUILDER, RECORDED WITH ITS ARGUMENT

The commissioning brief left the treatment arm open between `MIX280mix4` and `AWRLNCH`. **The
builder closed it on a third option, `BODYAWR`, and the reasoning is adopted here as the leg's
own:**

1. **CLEANEST ATTRIBUTION.** `MIX280mix4` is **four planks**; a live result on it is unattributable
   to any one of them, so a null teaches nothing and a hit teaches nothing about *what*. `AWRLNCH`
   is `bodyaware` + `homeearly`, and `homeearly` **measured null solo** — so `AWRLNCH` is
   `bodyaware` carrying a passenger. **`BODYAWR` is the single plank, and it is the plank the other
   two contain.**
2. **LARGEST LOCAL BASE.** n = 10,801 games behind it, twice any competitor arm's shard.
3. **KILL-POSITIVE ON THE ADOPTED ESTIMATOR AND SIGN-STABLE ACROSS HORIZONS.** RMST₃₀₀ −6.84
   [−8.61,−5.08]; H=250 −4.55, H=300 −6.84, H=400 −12.16 — **the same sign at every horizon.**
   ⛔ **This retires the brief's horizon-shopping hazard for THIS arm specifically:** the `MIX`
   family flips sign between H=250 (+1.35) and H=400 (−8.67), which would have made any field/local
   disagreement inseparable from the horizon choice and made post-hoc horizon shopping maximally
   tempting. `BODYAWR` carries no such exposure. **H=300 is registered regardless and no other
   horizon may be substituted after the data; H=250 and H=400 are reported as pre-declared
   sensitivity columns, never as the primary.**
4. **LEVERAGE ON EVERYTHING DOWNSTREAM.** `bodyaware` sits underneath the arms above it. **If it
   fails live, everything downstream re-prices; if it holds, the whole stack inherits the result.**

*For the record, since the brief commissioned the argument between its own two candidates and the
answer is now moot: on the same criteria the drafter would have chosen `AWRLNCH` over `MIX280mix4`
— `MIX280`'s local kill-axis effect is −0.87 [−3.18,+1.43], statistically indistinguishable from
zero, so it offers no kill-axis contrast to transfer and both hypotheses predict the same field
value; and `MIX280`'s admissibility is under arbitration with Magnus (the split ITT-pass /
speed-fail 55-class), so field games could not unblock it. **`BODYAWR` dominates that choice on
every one of those grounds and the builder's call is the better one.***

---

## 3. ⛔ THE POWER REALITY — WHY THIS IS A FALSIFICATION LEG AND NOT A CONFIRMATION LEG

H = 300, sd = 74.59 rounds (rated-tape analogue, n = 525 games / 105 matches,
`RMST-ESTIMATOR-2026-08-16.md` §6.1), unrated **PLANNING** DEFF, cap 75 games/h:

| n/arm | window | RMST₃₀₀ resolution | game-share resolution |
|---:|---:|---:|---:|
| 300 | 8.0 h | ±14.2 rounds | ±10.8 pp |
| **600** | **16.0 h** | **±10.1 rounds** | **±7.7 pp** |
| 900 | 24.0 h | ±8.2 rounds | ±6.3 pp |
| 1800 | 48.0 h | ±5.8 rounds | ±4.4 pp |

**The local effects to be confirmed are +3.70pp game share and −6.84 rounds RMST₃₀₀.**
⇒ ⛔ **Even 1,800 games/arm — 48 hours of saturated firing — leaves BOTH effects inside the noise.
There is no feasible unrated leg that confirms these magnitudes.** The leg is therefore designed
around the question the local fixture genuinely cannot answer: **does the effect EXIST against real
opponents, or does it INVERT?**

**⚠ TWO DIFFERENT DESIGN EFFECTS ARE IN USE ABOVE AND THAT IS DELIBERATE — DEFF IS A PROPERTY OF THE
STATISTIC, NOT ONLY OF THE SURFACE.** Game share uses the measured unrated pooled constant
**1.833**; RMST₃₀₀ uses **1.42 (PLANNING)**, which is conservative against the kill-time DEFF of
**1.145** measured on the rated tape at H=300. Naming one constant for both would understate one
band and overstate the other.

**⭐ THE DEFF RE-MEASUREMENT OBLIGATION, AND IT IS ABSOLUTE.** Every DEFF above is a **PLANNING /
ASSUMED** value used for SIZING ONLY. **It appears in NO banked interval.** The leg RE-MEASURES the
design effect on ITS OWN 1,200 games — enumerating both clusters per `CLAUDE.md`'s procedure
(MATCH: 5 games per accept ⇒ live; OPPONENT: 12 accepts per opponent per arm ⇒ live), **with the
df correction, which is required: the uncorrected form is biased LOW (1.282 against 1.434 on the
reference cut).** Every banked interval in the read-out uses the **re-measured** value, quoted
beside the planning value so the change is visible. A read-out that quotes 1.42 or 1.833 as if it
were the leg's own DEFF is off-registration.

**⛔ AND THE DIRECTION RULE, because it decides whether the correction flatters us.** Widening an
interval makes an EXCLUSION harder and a FAIL-TO-EXCLUDE **easier**. This leg's primary MISS and its
non-reversal outcome are both fail-to-exclude claims. ⇒ **Each must be RESTATED AS AN EXCLUSION
before any DEFF is applied to it:** we state *the largest reversal the leg's CI excludes*, never
*"consistent with the local finding"*. Applied to the unrestated form, the correction would launder
a weak null into a confident one.

---

## 4. PRIMARY — THE PER-CELL SIGN TEST, AND ITS POWER, PRE-COMPUTED

**Unit of analysis: the opponent cell (k = 10).** Within each cell both arms meet the SAME pinned
opponent build over the same 12 accepts each. Score `sign(share_T − share_C)`. Exact two-sided
binomial:

    10/10  p = 0.0020   MEET
     9/10  p = 0.0215   MEET   <- the registered bar
     8/10  p = 0.1094   UNRESOLVED
    <=7/10               MISS (expected; see the impotence clause)

**POWER, computed before firing.** Per cell each arm has 60 games. Under the local effect:

| axis | per-cell sd of (T−C) | implied per-cell win prob π | **P(reach 9/10)** |
|---|---:|---:|---:|
| game share (+3.70pp local, DEFF 1.833) | 10.93 pp | 0.632 | **7.0%** |
| RMST₃₀₀ (−6.84 rounds local, DEFF 1.434) | 16.31 rounds | 0.663 | **9.9%** |

⇒ **The primary has roughly 7–10% power against the effect it is aimed at.** P(reach 8/10) is 22.6%
— and 8/10 is not significant, so the outcome most likely to *look* like something is exactly the
one registered as UNRESOLVED. **This is the impotence clause in numbers, and it is why the bar is
not the leg's product.**

**EXPECTED DIRECTION of the primary, stated so it is falsifiable:** if the local effect is real and
transfers, the majority of cells are `+` (treatment share above control share). A majority of `−`
cells is evidence in the opposite direction and is read through §5's reversal machinery, not
through the bar.

---

## 5. ⭐ FALSIFIER — THE THING THIS LEG IS ACTUALLY BUYING

**THE LOCAL FIXTURE IS FALSIFIED AS A PREDICTOR OF THE FIELD, IN SIGN, IF THE POOLED FIELD RESULT
REVERSES BEYOND THE LEG'S OWN DETECTABLE BAND AT 600 GAMES/ARM:**

* **pooled game share (T − C) ≤ −7.7 pp**, or
* **pooled ITT RMST₃₀₀ (T − C) ≥ +10.1 rounds.**

Either is a 95%-level exclusion of zero **in the direction opposite the local finding** (local:
+3.70pp and −6.84 rounds). A reversal of that size means the arm the local board reads as *better
and faster* is, against real opponents, *worse and slower* — **the echo-loop failure this leg
exists to detect, and the one result at this n that is unambiguous.**

**This is correctly shaped as an EXCLUSION claim and needs no restatement.** Its complement does:
a non-reversal is a FAIL-TO-EXCLUDE and is banked as *"the leg excludes reversals larger than
X"* with X read off the leg's OWN re-measured DEFF — never as *"the local finding is confirmed"*,
and never as *"the local finding is refuted"*.

**A SECOND, WEAKER FALSIFICATION PATTERN, registered as a POINT RULE ONLY (OB16 corollary: it
licenses no effect-size exclusion):** a per-cell sign majority of `≥9/10` in the **negative**
direction (p = 0.0215) is a directional reversal even if the pooled magnitudes stay inside the
band. Reported if it occurs; it cannot rescue or damage the primary, which is direction-agnostic
by construction.

---

## 6. WHAT IS REPORTED AND AT WHAT WEIGHT — pre-committed so nothing is promoted at read-out

| # | quantity | weight |
|---|---|---|
| 1 | per-cell game-share sign test, k=10 | **PRIMARY** (bar §1, power §4) |
| 2 | pooled ITT RMST₃₀₀ (T − C) with re-measured DEFF | **SECONDARY, carries the reversal falsifier** |
| 3 | per-cell RMST₃₀₀ sign test, k=10 | SECONDARY, reported in both directions; **may not rescue a failed primary** |
| 4 | pooled game share (T − C) with its band | **DESCRIPTIVE ONLY — see §6.1** |
| 5 | the estimator TRIPLE: ITT timely-kill rate · rate factor · speed factor | DIAGNOSTIC (`PROGRAMME.md`'s resolved block) |
| 6 | kill-win-conditioned median kill round | DIAGNOSTIC ONLY — ⛔ it is the COLLIDER form; where it disagrees with the ITT form, the disagreement is itself the finding (collider size), never a verdict |
| 7 | RMST at H=250 and H=400 | pre-declared sensitivity columns; **never substitutable for H=300** |
| 8 | per-arm win/loss/tiebreak mix, kill-vs-non-kill counts | descriptive |

**6.1 WIN SHARE IS DESCRIPTIVE ONLY AND IS DECLARED UNRESOLVABLE AT THIS n.** Resolving the local
+3.70pp against the field needs **~5,258 games/arm**; this leg plans **600**. Its half-width on the
pooled arm difference is **±7.7pp** — twice the effect. **No bar, no verdict, no ship input, and it
must be quoted with its band or not at all.** The factorisation identity
`RMST = H − P(kill ≤ H) × E[H − T | kill ≤ H]` is exact and both decompositions are reported, but
neither is a verdict statistic either.

**6.2 IMBALANCE IS REPORTED ONCE, UNDER ONE HEADING, ON ALL FIXTURE AXES** (OB12's companion: two
imbalances are one defect). The axes are **seat**, **map**, **opponent pin age**, **time-of-day /
window**, and **per-cell accept counts**. **Disclose, do not correct** — a matched estimator chosen
after the data is the fault this discipline exists to catch.

---

## 7. THE BRANCH TABLE — WHAT MAY BE WRITTEN DOWN, PRE-COMMITTED

| outcome | what may be banked | what may NOT be said |
|---|---|---|
| ≥9/10 same sign, direction positive | *"the `bodyaware` effect is directionally present against 10 pinned live opponents, p ≤ 0.0215"* | any magnitude claim; any ship claim; any slot claim |
| ≥9/10 same sign, direction negative | *"directional reversal against live opponents, p ≤ 0.0215"* — a real finding, re-prices the stack | *"the plank is harmful by X"* — the magnitude is unresolved |
| pooled reversal past §5's band | **THE FALSIFICATION: the local fixture does not predict the field in sign on that axis** | that the local board is *wrong about everything*; the claim is axis-specific |
| 8/10 | **UNRESOLVED.** Defaults to the RESTRICTION: no directional claim in either direction | *"suggestive"*, *"trending"*, *"nearly significant"* |
| ≤7/10 and no pooled reversal | *"the leg excludes reversals larger than X (leg's own re-measured DEFF); the local magnitude was never in range"* | ⛔ **that the local finding is refuted. This is the EXPECTED outcome and the impotence clause governs it.** |
| any cell voided by §9.3 | the leg minus that cell, k reduced, exact p recomputed | pooling a voided cell into anything |

---

## 8. OBLIGATION 15a — DEVIATION DECLARED RATHER THAN HIDDEN

Obligation 15a offers two forms: `none expected — <why the mechanism is map-invariant>`, or a named
segment with a predicted sign. **Neither is honest here, so a third is used and flagged.**

**`bodyaware` is a NAV plank and the `#54` nav family has a measured terrain concentration**
(lock-heavy maps: midgard 35.6% of builder-rounds, ragnarok 14.1%, valkyrie 12.8%, against 3–8% on
small maps). ⇒ **`none expected` would be a false claim of map-invariance.**

**But this leg cannot read a map segment.** 60 games per arm per cell spread across the 15-map
rotation is ≈4 games per map per cell. **Declaring a primary segment the fixture cannot resolve is
exactly the OB12 failure — a gate that cannot discriminate its own branches — and declaring it
anyway would hand a failed arm a rescue route (15b's subgroup-fishing hazard) with no power to
justify it.**

⇒ **NO SEGMENT IS REGISTERED FOR THIS LEG.** Map mix is REPORTED under §6.2's single imbalance
heading. **Per OB15c the map-conditional question is routed to a NEW leg on the LOCAL fixture,
where n is free and 5,400-game shards per segment are affordable — not to a re-read of these rows.**
The rows that would suggest a segment cannot also confirm it.

---

## 9. HAZARDS CARRIED — EACH ONE COST US SOMETHING ALREADY. THESE ARE OBLIGATIONS A FIRING SESSION EXECUTES, NOT REFERENCES.

**9.1 PLATFORM REPLAYS STRIP `stdout`. ARMS ARE READ FROM ENGINE-SIDE FACTS ONLY.** Measured on the
LOKI-14 leg: 30,664 `BotOutput` events carry only `{id, execTimeUs}`; the `stdout` field is empty in
30,664 of 30,664, and a build that printed a tag on 314 confirmed throws produced **0 occurrences of
that literal string in 1.8 MB of platform replays.** ⇒ **No arm identification, dose counter or
state flag in this leg may be read out of our own printed output.** Arm identity comes from the
platform's per-match `teamAVersion`/`teamBVersion` and from the submission id we activated; kill
timing comes from `turnsPlayed` + `winCondition` (`tools/leg_read.py:105-106`). **A read-out that
reaches for a printed tag is planning on an instrument that does not exist.**

**9.2 `fcode submit` AUTO-ACTIVATES. THE SUBMIT *IS* THE SHIP.** There is no upload-now-activate-
later. Every arm flip therefore fires **only inside an OBSERVED pairing gap**, with the offset
**re-derived from recent `fcode match list` rows at fire time and NEVER hardcoded** (it has shifted
at least once inside an 18-hour span). Submissions go through `tools/submit_clean.py`, which
restores the holder itself and **confirms the restore against the `Active bot:` line, never against
the exit code** — this CLI exits 0 while printing `Error: True`. **Gate on the presence of the
load-bearing field, never on `$?`.** Every flip records: wall time, the nearest observed pairing,
the `Active bot:` line after the flip.

**9.3 ⛔⛔ THE PIN'S SILENT-UNPIN PATH — CLOSED AT THE TOOL TODAY, AND THE POST-FIRE ASSERTION IS
STILL REGISTERED AS A BAR-LEVEL OBLIGATION.**
`tools/unrated_run.sh:366` fires `fcode match unrated "$id" --match "$PIN" --json` when `$PIN` is
set. **Until 2026-08-16 the else-branch fell through to a bare unpinned call with no error and
nothing in the output to show it** — one empty-variable slip in a ten-invocation loop silently
unpinned that opponent and played their CURRENT bot, the CAL418 failure one layer in.
✅ **MECHANICAL BACKSTOP, ADDED TODAY AND CITED HERE RATHER THAN ASSUMED: `tools/unrated_run.sh:380-383`
now ABORTS (`exit 2`) when `PIN` is empty unless `UNPINNED_OK=1` is set explicitly.** Calibration
panels are the legitimate unpinned use and declare it; **a pinned design that loses its PIN variable
now dies loudly.** ⛔ **`UNPINNED_OK` MUST NEVER BE SET ANYWHERE IN THIS LEG. Setting it converts
the guard back into the silent path.**
⇒ **AND THE ASSERTION IS REGISTERED ANYWAY, because a guard covers the EMPTY pin and not the WRONG
one: for EVERY accepted match the decoded `oppver` must equal the registered `theirver` for that
cell. A mismatch VOIDS THAT CELL — it is not noted, it is removed**, k is reduced, and the exact
sign-test p is recomputed. This is `CLAUDE.md`'s instrument-alarm rule applied per-match. **It is
load-bearing on exactly the failure mode the new guard does NOT catch: a VALID pin id that points at
a different version than `theirver` claims plays the wrong bot and looks completely normal. An
INVALID id errors and is visible; that is the harmless case.**

**9.4 ⛔ THE RUNNER, AND THE SHAPE CONSTRAINT THAT FOLLOWS (Obligation 17, all three parts).**
1. **EXECUTING TOOL: `tools/unrated_run.sh`.** It is the ONLY runner with a pin path. ⛔ **The
   brief's `panel2_cal.sh` recommendation CANNOT execute this leg** — `tools/panel2_cal.sh:59` is a
   bare `fcode match unrated "$id" $MAPS --json` with no `--match`, as are `fanout.sh:102`,
   `night_collector.sh:78` and `loki14b_leg.sh:93`. Fired through any of them the registered pin
   silently does not happen. **What the brief wanted from `panel2_cal.sh` — window backoff and cell
   rotation — `unrated_run.sh` already has** (`:153 WINDOW_S=1230`; `:350 ci=$((ci+1))`, *"rotate so
   drops don't bias one cell"*).
2. **THE PATH EXISTS IN THAT TOOL — and it carries a hard constraint.** `unrated_run.sh:361-363`
   **ABORTS** if `PIN` is set with more than one cell (*"a match id pins ONE opponent"*). The runner
   is right. ⇒ **THIS LEG IS TEN INVOCATIONS PER ARM, ONE PER OPPONENT, EACH WITH ITS OWN `PIN`.**
   A single multi-cell invocation is impossible, and **the alternate-arms and rotate-starting-cell
   discipline must therefore be enforced by WHATEVER SCHEDULES THE TWENTY INVOCATIONS** — the
   runner's internal rotation now only ever sees one cell and cannot do it.
3. **CONSEQUENCE OF SILENT NON-EXECUTION:** the abort in (2) is the GOOD case, and the quiet case
   (§9.3's former fall-through) was **closed at the tool today by the `UNPINNED_OK` guard at
   `:380-383`.** ⇒ **§9.3's per-match assertion is still not optional** — the guard catches an EMPTY
   pin, not a WRONG one.
4. **THE OUTFILE IS PART OF THE METHOD, NOT A DETAIL.** `unrated_run.sh` writes to
   `scratchpad/arm_*.txt` and **`tools/rate_budget.py` attributes our spend by globbing exactly that
   name — the platform supplies no actor field, so the glob IS the contract.** A hand-rolled runner
   once wrote a differently-named outfile, the meter could not attribute five challenges, reported
   *"a slot is free NOW"* into a spent window, and the next window came back 0/5 rejected. **All 20
   invocation streams of this leg write `scratchpad/arm_*.txt` or the rate meter goes blind.**

**9.5 THE ARCHIVE LAGS. ABSENCE IN `ladder_games.tsv` OR `meta_join` IS NOT EVIDENCE.** Already
concrete on this leg: the `Juusto v13` pin match (05:32:59Z) is newer than that archive's newest row
(04:52:59Z). **No claim in the read-out may rest on a row not being present**, and any freshness
statement quotes the age of the newest row rather than asserting currency. A monitor that reads a
file must report that file's freshness or refuse to print a verdict.

**9.6 THE RATE WINDOW: 5 test/unrated matches per 20 minutes, charged to the CHALLENGER.**
Rejections count. ⇒ **The scheduler must WAIT OUT the window and RETRY THE SAME CELL, and rotate the
starting cell each window.** ⛔ **It must NOT behave like `fanout.sh`'s `fire()`, which retries three
times at 25 s and gives up — under a window it cannot outwait, that drop is systematic and always
lands on the tail of the id list, starving exactly the cells the design needs balanced.** An
opponent's own campaign against us costs us nothing (verified 2026-08-16: Hugging Farce fired at
01:02/01:28/02:03/02:43 while we fired 02:31/02:44 in the same windows, both succeeding).

**9.6a ⛔⛔ THE WINDOW IS SHARED WITH AN INVISIBLE CO-OPERATOR — REGISTERED AS A SCHEDULER
OBLIGATION.** A **TEAMMATE fires unrated matches from the same team account** (verified pattern,
side lane 2026-08-16: two matches = **40% of a single window** consumed, observed live). **The rate
limit is per ACCOUNT, so a scheduler that counts its OWN fires is systematically wrong and cannot
see why it is being rejected.**
⇒ **REGISTERED: the leg's scheduler gates on `.venv/bin/python tools/rate_budget.py` — which sees
ALL account spend — BEFORE EACH of the ten invocations, never on its own fire count.**
(`unrated_run.sh` already paces off `max(meter, own ledger)` internally at `:309`; **this obligation
binds the WRAPPER around it**, which is the layer research's shape constraint created and which
nothing else guards.)
**TWO CONSEQUENCES, both stated so no later reader treats them as surprises:**
* **The 16 h / 600-games-per-arm figure is a FLOOR ON WALL-CLOCK, NOT A PROMISE.** Shared spend can
  only lengthen it. The `CUT-SHORT` clause (§1) and the two-session registration (§10.4) are what
  absorb that, and neither needs amending when it happens.
* **A DRAINED WINDOW CAUSES A WAIT-AND-RETRY-ON-THE-SAME-CELL. NEVER A SKIP.** A skip lands
  systematically on whichever cell the scheduler happened to be on — **the `fanout.sh` starvation
  class, arriving through a different door**, and it would bias exactly the per-cell balance the
  sign test depends on.

**9.6b ⛔ AND THE SECOND HALF OF THE RUNNER RULE, WHICH 9.6a DOES NOT CONTAIN: THE SCHEDULER ROTATES
ITS STARTING CELL.** **Round `k` starts at cell `(k−1) mod 10`** — the `tools/panel2_cal.sh:53-56`
form (*"rotate the starting cell so a dropped challenge cannot keep hitting the same opponent"*),
**re-homed into the wrapper because `unrated_run.sh`'s own rotation (`:350`) is INERT here: at one
cell per invocation it has nothing to rotate.** The duty exists in exactly one place and that place
is the scheduler.
**WAIT-AND-RETRY AND ROTATION SOLVE DIFFERENT PROBLEMS AND NEITHER SUBSTITUTES FOR THE OTHER:**
wait-and-retry prevents **DROPS**; rotation prevents **ORDERING BIAS**. In a fixed order **cell #1
always fires into the freshest window and cell #10 into the most depleted**, so every truncation —
session end, the 1,200-game cap, a co-operator burst (9.6a) — lands on the same tail cells.
⛔ **With a per-opponent SIGN TEST as the primary, a systematically under-fired opponent is not
noise: it is a THIN CELL IN THE EXACT STATISTIC THE VERDICT RESTS ON**, and under §1's `CUT-SHORT`
rule it is the cell most likely to be excluded — which would make the excluded set a function of
firing order rather than of anything about the opponent.

**9.7 GAMES ARE NOT INDEPENDENT — USE THE RIGHT HALF-WIDTH FORM.** One sample:
`1.96*sqrt(p̄(1-p̄)*DEFF/n)`. Two-fixture (a leg share against a local or rated share):
`1.96*sqrt(p̄(1-p̄)*(DEFF_u/n_u + DEFF_r/n_r))`. **Any local-vs-field comparison in the read-out uses
the two-fixture form.** Reference constants: unrated pooled 1.833, unrated within-opponent 1.434,
rated pooled 1.529, rated within-opponent 1.366, per-map ≈1.07, local 0.98. ⚠ **The local 0.98
exemption is measured and real but does NOT cover cross-host pooling** — if any local figure quoted
against this leg pools shards from more than one box, the host term is named or the interval is
declared understated.

**9.8 HORIZON DISCIPLINE.** H=300 is the registered horizon, re-priced there by Magnus's ruling of
2026-08-16T05:15:45Z (`DEFENCE_ADMISSION_BAR: r300_crossing_non_regression`). **No post-hoc horizon
shopping.** H=250/H=400 are pre-declared sensitivity columns only (§6, row 7).

**9.9 EVERY NUMBER INHERITED FROM RESEARCH'S s45 RMST RELAY CARRIES A PENDING-AUDIT FLAG.** The
board figures (BODYAWR −6.84 / n=10,800, AWRLNCH −6.43, MIX280 −0.87, NULL114 +0.42, the horizon
table, sd 74.59 / DEFF 1.145) come from `docs/research/RMST-ESTIMATOR-2026-08-16.md` and the
in-channel relays of 2026-08-16 07:0x–07:4xZ, **with the side-lane audit not closed at drafting
time.** ⚠ **That document itself retracts two of its author's earlier claims from the same
morning**, which is the reason the flag is carried rather than assumed away. Any figure that moves
on audit moves this leg's priors, not its design.

---

## 10. EXECUTION PLAN

**10.1 SHAPE.** 20 invocation streams (10 cells × 2 arms), driven by a SCHEDULER above
`tools/unrated_run.sh`. Each invocation: `CELLS=<one team id>`, `PIN=<that cell's match id>`,
outfile `scratchpad/arm_*.txt`, target 12 accepts, `UNPINNED_OK` NEVER set. Both arms use the SAME
pin id in a cell. **Everything the runner cannot do at one cell per invocation — arm alternation,
starting-cell rotation, account-wide rate gating — is the SCHEDULER's duty (§9.4.2, §9.6a, §9.6b),
and the firing session inherits those three as obligations, not as suggestions.**

**10.2 CADENCE — ARMS ALTERNATE, THEY ARE NOT RUN TO COMPLETION.** ⛔ **Running arm A to completion
and then arm B confounds ARM with TIME OF DAY** — 16 hours of ladder conditions, opponent traffic
and platform load would load entirely onto the arm contrast. **Arms alternate within each 20-minute
rate window; the scheduler rotates its starting cell every round per §9.6b; and it gates on
`tools/rate_budget.py` before every invocation per §9.6a.**

**10.3 ⚠ THE COST OF 10.2, SURFACED FOR THE BUILDER TO RULE ON IN ONE LINE — NOT SILENTLY RESOLVED.**
Alternating *within* a window means **≥2 activations per window × ~48 windows ≈ 96 submits**, each
of which must land inside an observed pairing gap (§9.2). ⛔ **The arm-flip cadence (20 min) is
COMMENSURATE with the ladder pairing cadence (~20 min), so flips will tend to land at a FIXED PHASE
relative to pairings — if that phase is bad, every flip is bad, systematically.** The cheaper
alternative, offered and not adopted: **alternate arms BETWEEN consecutive windows** (A, B, A, B…),
which still breaks the arm/time confound at 20-minute granularity and halves the flips to ~48.
**BUILDER RULES: keep 10.2 as written, or adopt the between-windows form. Either is defensible;
the phase hazard must be recorded whichever is chosen.**
**⭐ RULED AT RATIFICATION (builder, 2026-08-16): THE BETWEEN-WINDOWS FORM IS ADOPTED** — arms
alternate between consecutive windows (A, B, A, B…), ~48 flips. Grounds: the submit is the leg's
riskiest primitive (every submit is an auto-activation that must land in a pairing gap), so halving
submits halves exposure to the phase hazard rather than merely documenting it; and 20-minute
interleaving preserves the arm/time balance at the same granularity the within-window form buys —
each arm still samples every hour of the leg. The phase hazard stands RECORDED for both forms:
window cadence ≈ pairing cadence, so flips tend toward a fixed phase; the per-submit observed-gap
guard (§9.2) is the active mitigation, and its offset is re-derived per submit, never cached.
§10.2's within-window sentence is superseded by this ruling; its arm/time-confound rationale
stands and is honoured at window granularity.
Related, same class: the holder (`v152`) is **restored at every HALT and at each SESSION END, not
between windows** — restoring 48 extra times triples the submit count for zero measurement gain.
**This means rated exposure is CONTINUOUS for the leg's duration and is priced as such in 10.5.**

**10.4 TWO-SESSION LEG, REGISTERED AS SUCH.** 1,200 games at the 75 games/h ceiling is **~16 hours
of saturated firing.** ⇒ **When session 1 ends this leg is LIVE, NOT ABANDONED.** The handover
carries: cells completed with per-cell per-arm accept counts, the arm currently active, the holder
restore state verified on the `Active bot:` line, the next cell in rotation, and the rated matches
recorded so far. **A successor reading a half-filled tape without this paragraph would read a
stopped leg.**

**10.5 RATED EXPOSURE — PRICED, NOT WAVED.** ~2.6–3.1 rated matches/hour are played by whichever arm
holds the slot. Over ~16 h that is **≈42–50 rated matches played by a non-holder**, priced
historically at roughly **−8 Elo per adverse leaked match** (measured: −24.67 Elo across 3 leaked
matches on 2026-08-10). **This is the largest cost this leg carries and it is not small.**
Obligations:
* **Ground truth is per-match `ourver` off `ladder_games.tsv`. NEVER `elo_history.tsv`**, which tags
  rows by the version active at POLL time and is structurally blind to exactly these matches.
* **The match COUNTER cannot answer whether a match was PAIRED while an arm held the slot** — only
  per-match `teamAVersion` at the PAIRING BOUNDARY can.
* **HALT CONDITIONS (pre-committed): (a)** Magnus or x3r0 asks for the slot — immediate, no
  negotiation, `CUT-SHORT` governs the claims. **(b)** *(DRAFTER-ADDED, for the builder to ratify or
  strike in one line — it is not in the brief)*: halt if the leg-window rated matches show a
  cumulative net **≤ −40 Elo**, read per-match off `ladder_games.tsv`.
  **RATIFIED (builder, 2026-08-16): the −40 Elo halt stands** — climbing Elo is Magnus's stated
  goal and the leg's largest cost deserves a pre-committed tripwire; a halt returns the slot to
  the holder, `CUT-SHORT` governs the claims, and resumption is Magnus's call, not the session's.

---

## 11. OB13 / OB17 SELF-CHECK, RUN BEFORE THE LOCK

Per the OB17 rider — *run the clause that can return an answer that surprises you; a check whose
verdict is already known is ceremony* — the clauses are reported with which of them could have gone
either way.

| clause | verdict | could it have surprised? |
|---|---|---|
| OB13 — metric read path names a `file:line` | `bots/_v242bodyaware/eco.py:813` | no — read off the diff minutes earlier |
| OB13 — that path is in the treatment diff | **YES**, and it is the ONLY file that differs | no |
| OB17.1 — name the executing tool | `tools/unrated_run.sh` | **YES — it surprised: the brief named `panel2_cal.sh`, which has no pin path at all** |
| OB17.2 — the runner emits `--match` | `:366` emits it | **YES — and it returned a constraint nobody had: `:361-363` REFUSES a pin across multiple cells, which changes the leg's shape to 20 invocations** |
| OB17.3 — consequence of silent non-execution | the fall-through was quiet; **`:380-383`'s `UNPINNED_OK` guard closed it today** | **YES — this is the clause that produced §9.3's bar-level assertion, and the tool fix landed because of it** |
| runner rule — does the wrapper inherit what the runner cannot do at one cell? | **NO, it did not** — arm alternation, cell rotation and account-wide rate gating all became scheduler duties the moment the shape changed to 20 invocations | **YES — §9.6a and §9.6b exist only because this was asked after the shape constraint, not before** |

---

## 12. ⛔ INSTRUMENT NOTES ON `tools/prereg_check.py` ITSELF — READ BEFORE TRUSTING ITS OUTPUT ON THIS DOCUMENT

**12.1 `TARGET BAND` IS A DELIBERATE, BLOCKING FAILURE.** The value is the sentinel
`<BUILDER-FILLS-FROM-LIVE-READS-BEFORE-LOCK>`, which satisfies neither of the checker's accepted
forms, **so `TARGET_BAND` will FAIL until it is filled.** That is intended: the drafting agent runs
no platform commands and `PROGRAMME.md`'s gate requires the number BEFORE the work, not a defence
after it. **The builder fills it from LIVE `fcode team search` reads — not from
`tools/target_value.py`'s cached column, which research measured drifting up to 24 points.**
Required form: `<opponents>, gaps <a..b>, win pays <x..y>, reachable YES/NO`. *(Those three keywords
are deliberately kept OFF the sentinel line: the checker passes any value containing all three, so
writing the format there would have made the guard pass vacuously.)*
**Informational only, NOT the line** — research's live reads at 2026-08-16 ~05:0xZ put us at
**1799** and the ten cells at 1747–1913, i.e. inside ±115 of us, **all ten clearing the 1650 floor**;
12 of 12 checked were admissible with no cached-vs-live flips. The builder re-reads and writes the
line.

**12.2 `BAR_RESOLVABLE` COMPUTES THE WRONG n ON THIS DOCUMENT.** The checker will read `BAR` 9/10 →
90.0 and `BASE RATE` 5/10 → 50.0 and compute a binomial half-width **at n = 1,200 GAMES**. **The
primary's n is 10 CELLS, not 1,200 games.** Its `ok` verdict is therefore not this leg's arithmetic;
**§4's exact binomial is.** The two happen to agree on direction, which is precisely why this note
exists — an accidental agreement reads identically to a check.

**12.3 THE OB13 COMPUTED BRANCH ONLY WORKS BECAUSE OF THE REGISTERED `TREATMENT DIFF REFS`.** Both
arm trees are committed, so a plain `git diff HEAD` is EMPTY and the intersection would render as
CANNOT-COMPUTE — **a FAIL under `--fire`**, for a leg whose arms differ perfectly well. The refs
`--no-index bots/_v223sealrepair/eco.py bots/_v242bodyaware/eco.py` make it computable; the checker
resolves them to `bots/_v242bodyaware/eco.py`, which is the metric file. **Run and confirmed:
`OB13_INTERSECTION ok — metric file bots/_v242bodyaware/eco.py IS in the 1-path diff`.**
⚠ **The general point, worth carrying: OB13's path proxy assumes a plank leg with a working-tree
hunk. A whole-tree arm substitution defeats it, and the refs line is what repairs that.**

**12.4 THE `METRIC_WINDOW` LINE RESOLVES CLEAN — AND HERE IS WHAT IT ACTUALLY SAYS, so nobody reads
a silence as an assertion.** Output: `ok — window r0-r1000 clears 0 binding gate(s) [none]; 4 more
elsewhere in bots/_v242bodyaware/eco.py`. The four are `HUNT_MIN_RND` (:233), `SURGE_MIN_RND`
(:241), `MEDIC_MIN_RND` (:1152) and `MEDIC_EARLY_MIN_RND` (:1155). **None is inside
`_bfs_direction`'s enclosing block, so none binds the metric — "0 binding gates" is a real check
returning zero, not a check that did not run.**

**12.6 THE VERIFIED PRE-LOCK STATE OF THIS DOCUMENT, so the side lane knows what "clean" looks like
here.** `prereg_check.py` was run on this draft and returns **exactly ONE unmet obligation:
`TARGET_BAND`, by design (12.1).** Every other presence rule and every arithmetic check passes,
with **zero warnings**: `BOUNDARY_UNITS ok (240 accepts = 1200 games, 5x)` · `BOUNDARY_VS_N ok` ·
`CUT_SHORT_FLOOR ok (800 <= 1200)` · `BAR_NULL ok` · `DOSE_BOTH_VERDICTS ok (-6.84 vs 0.42)` ·
`OB13_INTERSECTION ok` · `METRIC_WINDOW ok` · `POOL_ERA_SINGLE ok`. ⇒ **After the builder fills
12.1, the line must read `PREREG_CHECK: OK`. If anything ELSE has appeared by then, something moved
after drafting and must be explained, not re-run until it passes.**

**12.5 TWO FILLS ARE OWED AT LOCK AND ONLY ONE OF THEM BLOCKS THE CHECKER.** `TARGET BAND` blocks
(12.1). **`CELL VERSION CHURN`'s numeric 24 h distinct-version counts do NOT block** — the checker
verifies presence only, and the line is substantive — **so the side lane must treat it as a manual
certification item or it will pass unfilled.** A field with no consumer passes on prose; that is
recorded here rather than left to be discovered.

---

## 13. AMENDMENT CLAUSE

This document is IMMUTABLE once locked. Corrections land as a **new dated document** that names this
one, per the standing amendment discipline. **Amendments must be ADD-ONLY and blind to the leg's
data**; an amendment written after any result row exists says so on its own face and is excluded
from the primary. **The estimator, the bar, the horizon, the cells, the pins and the falsifier are
frozen at lock and may not be substituted after firing.**
