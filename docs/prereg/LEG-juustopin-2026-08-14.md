# PREREG — LEG `juustopin` : who caused the Juusto collapse, us or them?

**Drafted 2026-08-14T21:18:34Z (`date -u`, same shell call as the git read below) by a FRESH
OPUS SUBAGENT with no inherited session context beyond the inputs on the `PROVENANCE:` line.
The agent prepares; the lane ratifies and types the lock commit.**

**STATUS: committed BEFORE any challenge of this leg is issued.** Zero games of this leg exist;
the cell it will fill — *(our v140, their v10)* — is **EMPTY in the corpus**, verified below.
Repo HEAD at drafting: `90f7aeda` (author time `2026-08-14T23:18:19+02:00`).
**Lock certification is the lane's:** two clocks — the lock commit's git author time versus the
platform `createdAt` of the leg's FIRST challenge. ⚠ If the runner does not stamp its own
START, the leg can only be dated by its first RESULT row, which is written at game
*completion* and is therefore one game length late; in that case the certification phrase is
**"predates first-row"**, never "predates leg creation".

---

## REGISTRATION BLOCK

**TARGET BAND: Juusto (`32087804-2dde-4265-acb2-b6ec9039fbee`), gap +114, a 5-0 pays +21.07 and a 0-5 costs −10.93, reachable YES (p99 of 414 observed pairings). ⚠ ZERO rated exposure on this leg — the payout is the RELEVANCE price of the cell, not a rating expectation from these games.**
**PINNED: YES — treatment leg. `fcode match unrated 32087804-2dde-4265-acb2-b6ec9039fbee --match 9b558b69-ac45-4f84-99cf-5620b1833e60` (their v10).**
**SURFACE: unrated**
**CLUSTER UNIT: match — enumeration performed below; the OPPONENT cluster is removed by construction (one opponent, one pinned build), the MATCH cluster survives (5 correlated games per accept) ⇒ within-opponent unrated DEFF 1.434**
**ESTIMATOR: pooled game share = (games won) / (games played), unweighted at the game level, over ACCEPTED-AND-COMPLETED matches only. With every match at 5 games this equals the mean of per-match shares; if any match returns fewer than 5 games the pooled form governs.**
**DOSE: decoded `oppver` = 10 in every pinned game vs 11 in the unpinned current-era comparator (n=175 pinned games planned; n=75 unpinned comparator games already banked, oppver ∈ {11,13})**
**PLANNED n: 175 games (35 accepted unrated matches = 7 windows of 5)**
**BOUNDARY: 35 accepts = 175 games**
**CUT-SHORT: below 100 games (20 accepts) this leg publishes descriptive per-window tallies only and takes NO attribution read**
**BAR: 52.67% — the OLD-era level (our v125 × their v7/8/9/10, unrated)**
**BASE RATE: 25.33% — the CURRENT level (our v139-142 × their v11/13, unrated)**
**BAR SOURCE: `corpus/meta_join.tsv`, cut 2026-08-14T21:1xZ by this agent. our v125 × Juusto v7,8,9,10 = 79 wins / 150 games over 30 matches, span 2026-08-13T10:32:03Z .. 23:06:54Z. ⚠ `docs/coordination.md` (research s43, 21:0xZ) quotes 52.00% over 25 matches for the same cell; the corpus has been re-ingested since (mtime 23:01 local) and MY reproduction is 52.67% / 30 matches. The number used here is mine, with its clock.**
**BASE RATE SOURCE: `corpus/meta_join.tsv`, same cut. our v139 × their v11 = 6/25, v140 × v11 = 4/25, v140 × v13 = 9/25 ⇒ 19 wins / 75 games over 15 matches, span 2026-08-14T09:36:00Z .. 19:28:37Z. This reproduces research's 25.33% (15 matches) EXACTLY.**
**POOL ERA: 2026-08-13T07:12:59Z..now — the post-rotation 15-map pool**
> *(The lane's slug for this era is the post-rotation one dated on the boundary day; it is
> written here in ISO range form because the bare date inside that slug parses as a SECOND
> boundary and fails `POOL_ERA_SINGLE`. The boundary itself is derived — never hardcoded — off
> `corpus/ladder_games.tsv`: 10 new maps entering within 24 h with 4381 prior rated games. The
> lane normalises the token if the parallel format diff lands first.)*
**REFERENCE n: none**
> *(The reason is declared and not defaulted: the registered rule compares the leg's share to a
> PRE-REGISTERED CONSTANT of 39.00pp — it is not differenced against a sample — so no reference
> term enters the primary interval. The anchors' own intervals and the two-fixture arithmetic
> are reported in §6b as DESCRIPTIVE and may never be the verdict. ⚠ Written on one line with no
> comma because `tools/prereg_check.py:341` crashes with a `ValueError` traceback on any
> `REFERENCE n` value whose first `[\d,]+` run is a bare comma — reported to the lane, not
> patched by me.)*
**MECHANISM METRIC READS: tools/triarm_read.py:55. TREATMENT DIFF TOUCHES: NONE — this leg has NO code diff; our side is the ACTIVE platform submission v140, byte-unmodified. INTERSECTION: N/A by construction — the treatment is the CLI argument `--match <id>`, which mutates exactly the field the metric reads (`teamBVersion`/`teamAVersion` by our seat), so the LOKI-18 failure (a metric reading identically in both arms) cannot arise: the metric's value IS the arm label.**
**TREATMENT DIFF REFS: HEAD HEAD**
> *(`git diff --name-only HEAD HEAD` is empty by construction — the literal expression of "this
> leg has no treatment diff", not an evasion. It is declared explicitly because the DEFAULT
> (`git diff HEAD`) picks up whatever unrelated `.py` edits happen to sit in the working tree —
> at drafting time another lane's `tools/era_guard.py` was modified — and that stray file would
> then be treated as THIS leg's treatment diff and produce a spurious `OB13_INTERSECTION` FAIL.
> ⛔ **`prereg_check` will therefore always report `OB13_INTERSECTION CANNOT-COMPUTE` + WARN for
> this leg, permanently, and that is CORRECT: there is no arm tree and none will ever land.
> `--fire` mode is NOT APPLICABLE here — do not "fix" the warning by naming a diff this leg does
> not have.** The substantive Obligation-13 question is answered instead by the sentence above:
> the metric's value IS the arm label.)*
**TREATMENT TREE: N/A — no arm tree exists. `fcode status` at 2026-08-14T21:07Z reads `Active bot: v140 (Loki v10)`; that is our arm.**
**GATE RESOLUTION: the three-branch gate below discriminates its branches at n ≥ 75 games (half-width ±13.22pp at the midpoint against the ±13.67pp the separation requires) and reaches ≥85% power on BOTH sharp branches only at n ≥ 175. At n=25 (±22.90pp) and n=50 (±16.19pp) it cannot discriminate at all. UNRESOLVED ⇒ THE RESTRICTION, never the permission: neither explanation is granted, both roads stay open, and no ship, de-prioritisation or road-closure may cite this leg.**
**PRE-STATE: the predicted-change set is NOT already in the target state at lock. Verified on `corpus/meta_join.tsv`: across every archived game against Juusto v10, the ONLY version of ours that has ever met it is v125 (25 games). Games of (our v134+ × their v10) = 0. The cell this leg fills is empty.**
**MAP SEGMENT: none expected — the outcome variable is an attribution between two OPPONENT SUBMISSIONS. No plank of ours is toggled and no terrain property enters the mechanism, so there is nothing map-conditional to segment. The leg and BOTH anchors draw from the SAME 15-map pool (boundary 2026-08-13T07:12:59Z, derived off `corpus/ladder_games.tsv`: 10 new maps, 4,381 prior games; all anchor games post-date it), so map mix is not a confound between leg and anchors. Map mix is reported DESCRIPTIVELY under §7.**
**CELLS: one — Juusto (`32087804-2dde-4265-acb2-b6ec9039fbee`), pinned to their v10.**
**CELL VERSION CHURN: Juusto ran 4 distinct versions (9, 10, 11, 13) across 71 matches in the 24 h to 2026-08-14T21:10Z (`corpus/league_matches.tsv`) — HIGH churn against a league median of 1 across 80 teams. ⭐ Obligation 14's "reportable but not poolable" would normally bar this cell; THE PIN IS THE EXEMPTION AND IS THE ENTIRE POINT OF THE LEG — pinning holds the opponent build fixed so churn cannot enter the leg's own games. It DOES enter the unpinned ANCHORS, and that is disclosed in §6. ⚠ Obligation 14's normalisation premise is FALSE TODAY and I re-checked rather than inheriting it: it records "every team played EXACTLY 87 matches in the window"; measured now the range is 7..71 across 80 teams, so raw version counts are NOT comparable between teams and Juusto's 4 must be read against its 71 matches.**
**PROVENANCE: CLAUDE.md · docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md · docs/research/SPEC-prereg-check-2026-08-14.md · docs/research/SPEC-opponent-pinning-2026-08-13.md · tools/prereg_check.py · tools/triarm_read.py · tools/target_value.py (executed) · docs/coordination.md (grep only, Juusto rows + fire order, lines ~47029–53560) · corpus/meta_join.tsv · corpus/league_matches.tsv · corpus/ladder_games.tsv · live read-only CLI: `fcode status`, `fcode team search Juusto`, `fcode match info 9b558b69-ac45-4f84-99cf-5620b1833e60`**

---

## 1. HYPOTHESIS

**Holding Juusto's submission fixed at v10 while our side is the shipped v140, our pooled game
share will land at the OLD-era level (≈52.67%) rather than the CURRENT level (≈25.33%) —
i.e. the −26.67pp collapse in the Juusto cell was caused by THEIR v11/v13 ship, not by our
v125→v139-142 ship.**

Falsifiable in one number, in both directions, with a pre-registered constant separating them.

## 2. WHY THIS LEG EXISTS, AND WHY NO CORPUS CUT CAN REPLACE IT

Our unrated share against Juusto moved **52.67% (30 matches) → 25.33% (15 matches)** across a
boundary where **their** version went v7/8/9/10 → v11/13 **and ours** went v125 → v139-142.
The two ships are collinear in calendar time, so *"our version regressed"* and *"their version
improved"* fit the archive identically. **`fcode match unrated <team> --match <past_match_id>`
plays the submission they had in that past match** — it is the only instrument that breaks the
collinearity, because it is the only way to place a NEW bot of ours against an OLD bot of theirs.

**Bounding the alternative, so this leg is not asked to carry it:** a *general* v140-family
regression is already excluded — paired within opponent across 12 opponents faced by both v125
and v139-142, **mean −4.34pp, se 4.88, p=0.37, 95% CI [−13.90, +5.21]** (research s43). A −26pp
league-wide effect is far outside that interval. This leg is about the Juusto cell specifically.

### ⚠ A CORRECTION TO THE PREMISE, FOUND WHILE SETTING THE ANCHORS — the "zero overlap" claim is not quite true here

`docs/coordination.md` states that opponent-version overlap is structurally ZERO and that "no
retrospective cut of this corpus can EVER separate" the two explanations. **On the current
corpus that is over-stated for Juusto.** Their **v11** was faced by BOTH eras:

| cell | wins/games | share |
|---|---|---|
| our v125 × their **v11** | 7/15 (3 matches) | **46.67%** |
| our v139+v140 × their **v11** | 10/50 (10 matches) | **20.00%** |

That is a genuine same-opponent-version overlap pointing at **our** side, and it sits in neither
of the two cells research defined (old = v7-10, new = v11+13) — it was excluded from both.
**It is also badly underpowered: the two-fixture 95% half-width is ±30.37pp against a 26.67pp
difference, so it CONTAINS zero.** It is a prior worth writing down, not a finding, and it is
recorded here because the leg's result should be read beside it rather than against a premise
that says no such cut exists.

## 3. THE POWER ARITHMETIC — THE LEG AS ORDERED (5 GAMES) IS UNDERPOWERED BY A LARGE FACTOR

One match is **5 games**. At p=0.5267 the expected wins are 2.63; at p=0.2533, 1.27. The two
distributions overlap almost completely: a single match cannot distinguish them, and the leg
must be sized in *windows*, not matches. The platform allows **5 test/unrated matches per 20
minutes** (shared across `match unrated` and `match test`; **rejected attempts appear to
count**), so **one window = 5 accepts = 25 games**.

### Cluster enumeration (performed, not asserted) — CLAUDE.md's scope procedure

1. **Clusters this data has: MATCH and OPPONENT.** (No window effect has been shown to bind;
   none is claimed.)
2. **MATCH — SURVIVES.** The stratum is the single pooled share over all 175 games, and every
   accepted challenge contributes exactly 5 games to it. Verified structurally on the pin
   target itself: `fcode match info 9b558b69…` returns 5 game rows. The stratum can therefore
   hold more than one member of a match cluster.
3. **OPPONENT — DIES.** Every game in the stratum is against Juusto, pinned to one build. The
   stratum holds exactly one member of the opponent cluster, so there is no between-opponent
   variance for it to contain. ⚠ **This survives only if the pin takes.** If some games return
   v11/v13 the stratum holds two opponent builds and the enumeration changes — a second,
   independent reason the pin-take check in §5 is a PRE-CONDITION on the read and not a
   footnote.
4. **Applicable DEFF = over the survivors = unrated within-opponent = 1.434.**
   Over-correcting to the pooled 1.833 would widen every interval by **×1.1306** for
   between-opponent variance this cut cannot contain, and it fails in the flattering direction
   for a "could not separate" verdict. Under-correcting to 1.000 would narrow them ×0.836.
   **Both are errors and only the enumeration catches either.**

### Half-widths, `1.96·sqrt(p(1−p)·DEFF/n)`, DEFF = 1.434

The two hypotheses are 52.67% and 25.33%; their **midpoint is 39.00pp**, so separating them
with a CI that excludes the midpoint requires a half-width **≤ 13.67pp**.

| n (games) | accepts | windows | hw @ midpoint 39.00 | hw @ 52.67 | hw @ 25.33 | separates? |
|---|---|---|---|---|---|---|
| **25** | 5 | 1 | **±22.90pp** | ±23.44pp | ±20.42pp | **NO** — the interval is 1.7× the whole gap |
| **50** | 10 | 2 | **±16.19pp** | ±16.57pp | ±14.44pp | **NO** |
| **75** | 15 | 3 | **±13.22pp** | ±13.53pp | ±11.79pp | **YES, but by 0.45pp** |
| 100 | 20 | 4 | ±11.45pp | ±11.72pp | ±10.21pp | yes |
| 150 | 30 | 6 | ±9.35pp | ±9.57pp | ±8.33pp | yes |
| **175** | **35** | **7** | **±8.65pp** | ±8.86pp | ±7.72pp | **yes, with headroom** |

⇒ **n=75 games (3 windows) is the smallest of the three that can separate 52.67 from 25.33 with
the CI excluding the midpoint — and it clears by 0.45pp, which is not a margin.** It is
sensitive to which old-era figure is used: against research's 52.00% the requirement tightens
to ±13.34pp and **n=75 FAILS** at p=0.52 (±13.53pp). n=25 and n=50 cannot separate under any
version of the anchor.

**Clearing a threshold is not the same as being powered to clear it.** The operating
characteristic of the registered rule (§4), computed before the fire:

| n | THEIRS branch fires if | OURS branch fires if | truth 52.67 → | truth 44.00 → | truth 25.33 → |
|---|---|---|---|---|---|
| 75 | wins ≥ 40 (53.33%) | wins ≤ 20 (26.67%) | T 50.0 / D 50.0 / O 0.0 | T 10.3 / D 88.9 / O 0.8 | T 0.0 / D 37.0 / O 63.0 |
| 100 | ≥ 51 (51.00%) | ≤ 28 (28.00%) | T 64.2 / D 35.8 / O 0.0 | T 13.7 / D 85.8 / O 0.5 | T 0.0 / D 27.1 / O 72.9 |
| 150 | ≥ 73 (48.67%) | ≤ 45 (30.00%) | T 81.3 / D 18.7 / O 0.0 | T 18.6 / D 81.2 / O 0.2 | T 0.0 / D 12.0 / O 88.0 |
| **175** | **≥ 84 (48.00%)** | **≤ 53 (30.29%)** | **T 86.4 / D 13.6 / O 0.0** | T 20.4 / D 79.4 / O 0.1 | **T 0.0 / D 9.2 / O 90.8** |

(T = THEIRS, D = DROP, O = OURS; normal approximation with the DEFF-inflated sd and a
continuity correction. The 44.00 column is explained in §6.)

⇒ **PLANNED n = 175 games (35 accepts, 7 windows).** It is the smallest multiple of a window
that reaches ≥85% on both sharp branches, and it costs ~2h20m on a surface Magnus has declared
free. **Unrated windows are free, so pooling windows is the default, not a luxury.**

## 4. DECISION RULE

Let **ŝ** = pooled game share over the leg and **hw(ŝ) = 1.96·sqrt(ŝ(1−ŝ)·1.434/n)** evaluated
at the observed ŝ (this formula is pre-registered so no estimator choice remains after the
data). The threshold **T = 39.00pp** is the midpoint of the two registered levels and is a
CONSTANT, fixed now.

| verdict | rule | at n=175 | what it licenses |
|---|---|---|---|
| **THEIRS (KEEP)** | `ŝ − hw(ŝ) > 39.00` | **wins ≥ 84 / 175 (ŝ ≥ 48.00%)** | The Juusto collapse is exogenous — THEIR v11/v13 ship caused it. No v140 remediation is ordered on this cell; the cell stops being evidence about our bot. |
| **OURS (REAL NEGATIVE)** | `ŝ + hw(ŝ) < 39.00` | **wins ≤ 53 / 175 (ŝ ≤ 30.29%)** | A real negative on v140 **for this cell**: our v125→v139-142 ship caused it. Orders a v125-vs-v140 diff hunt against Juusto's tactics, and the overlap cell in §2 becomes corroboration rather than a curiosity. |
| **DROP — COULD NOT SEPARATE** | `30.29% < ŝ < 48.00%` | wins 54–83 | ⛔ **NOTHING.** This is "could not separate", **NEVER** "the effect is zero", never "both contributed", never "our version is probably fine". Per Obligation 12 an UNRESOLVED gate defaults to the RESTRICTION: neither branch's permission is granted, both roads stay open, and no downstream decision may cite this leg. |

**Both sharp branches are EXCLUSION claims** (the CI excludes 39.00 from one side), which is
deliberate: DEFF widening makes an exclusion HARDER, which is the direction that cannot launder
a result. The alternative formulation — *"the leg is consistent with anchor X"* — is a
FAIL-TO-EXCLUDE claim that the DEFF correction makes EASIER, exactly the laundering
`CLAUDE.md`'s DIRECTION clause names. It is therefore **descriptive only in §6 and may never be
the verdict.**

### Stopping rule, registered before the first look

* Fire **7 windows** of 5 accepted challenges. A window that is rate-limited is **waited out and
  retried on the same cell**; a rejected attempt does not advance the accept counter but does
  consume the platform budget. (Cell rotation is moot here — there is one cell.)
* **The boundary is counted over ACCEPTS, never over attempt lines.** `games = 5 × accepts` is a
  platform identity: 35 accepts = 175 games. Any window whose two counts disagree is a runner
  fault and the leg pauses until it is reconciled.
* **NO INTERIM VERDICT.** Per-window tallies may be printed and are **descriptive only — a
  direction/dose read**, because a single window's CI is ±22.90pp and cannot separate anything.
  **The verdict is read ONCE, at the pre-registered stopping point (175 games).**
* **No early stop on a favourable look.** The only permitted early stops are (a) an INSTRUMENT
  ALARM under §5, or (b) a platform failure — and **both stop with NO attribution read**.
* **CUT-SHORT:** below **100 games** the leg publishes descriptive tallies only and takes no
  attribution read at all. Between 100 and 174 games the rule in the table above may be applied
  with the half-width recomputed at the achieved n, and the readout must state the achieved
  power from the table in §3.

## 5. INSTRUMENT ALARMS — REGISTERED AS PRE-CONDITIONS ON THE READ

**None of the outcome column may be read until all four pass.**

1. **PIN-TAKE (the dose, and it carries both verdicts).** Decode `oppver` for every game of the
   leg — `tools/triarm_read.py:55`, `oppver = r["teamBVersion"] if r["us_side"] == "a" else
   r["teamAVersion"]`, off `corpus/meta_join.tsv`. **Required: every game reads `oppver == 10`.**
   ⛔ **If the decoded values DIFFER across the leg's games, or any game reads 11/13 or anything
   else, the pin did not take (or the decode is wrong). That is an INSTRUMENT ALARM: report it
   and DO NOT READ THE CELL.** The other verdict is not hypothetical — the same decoder on the
   already-banked current-era games returns 11 and 13, which is what makes a reading of 10
   meaningful.
2. **A `--match` fire that ERRORS is not a pinned fire** (`SPEC-opponent-pinning`, failure mode
   1). Log it verbatim, abort the window, and **never silently substitute an unpinned
   challenge** — an unpinned game in this leg is not a weaker data point, it is a different
   experiment.
3. ⛔ **NO `print()` READS, ANYWHERE IN THIS METHOD.** Our own stdout is **stripped from
   platform-downloaded replays** — 30,664 `BotOutput` events carried only `{id, execTimeUs}`,
   and a leg that logged 314 kidnaps had its literal strings appear **0 times in 1.8 MB**. Every
   quantity in this document is engine-side: game winner, `turns`, map, seat, and the two
   version fields.
4. **TAPE FRESHNESS.** The decode reads `corpus/meta_join.tsv`, written by the archive keeper.
   Before any read, assert the newest row's `completedAt` is not older than the leg's last
   accepted challenge, **and print that age beside the verdict**. A stale tape renders missing
   games as absent rows, which is indistinguishable from lost games in a share denominator —
   the failure mode where a healthy line and a blind line are byte-identical.

**`R1000_IS_DEFEAT` read (unconditional).** Report, per game, `turns` — and count r1000 games as
**`turns == 1000`, never the `cond` string**. r1000 wins still count in game share (that is what
the ladder pays and what this leg measures), **but the readout must state the r1000 count in
both the leg and the anchors, and the result may NOT be described as a kill-rate or
kill-speed finding.** A tiebreak win is not banked as a kill.

## 6. LIMITATIONS — NAMED IN ADVANCE, EACH WITH ITS NUMBER

**⚠ 6a. THE OLD ERA IS NOT HOMOGENEOUS, AND THIS IS THE LEG'S BIGGEST WEAKNESS.** Our share
declined across THEIR versions *within* the old era, before v11 existed:

| their version | our v125's share | games |
|---|---|---|
| v7 | 60.00% | 95 |
| v8 | 40.00% | 15 |
| v9 | 33.33% | 15 |
| **v10 — the pinned build** | **44.00%** | **25** |

The pooled 52.67% anchor is dominated by v7 (95 of 150 games). **If their v10 was already worse
for us than the old-era average, the leg's true level under H_THEIRS is ~44%, not ~52.67%, and
the rule in §4 lands in the DROP band ~79% of the time (§3 table).** ⛔ **That outcome MUST be
read as "could not separate". It is more likely under a their-ship-but-gradual world than under
either sharp hypothesis, and converting it into support for H_OURS is the specific error this
clause exists to forbid.**

**Why the v10-matched cell is not used as the anchor, stated as arithmetic rather than
preference:** it is n=25 games, **95% CI 44.00% ± 23.30pp = [20.70, 67.30]** — an interval that
contains BOTH candidate levels. It cannot discriminate anything and cannot set a threshold. And
if the leg were *differenced* against it as a two-fixture comparison, the reference floor at leg
n→∞ is **±22.34pp against an 18.67pp margin ⇒ unresolvable BY CONSTRUCTION at any leg length**,
which is CAL-7's P1 exactly. It is reported, never used.

**6b. Anchor intervals (descriptive; the primary rule uses a constant, not these).**
old pooled 52.67% ±9.57pp (n=150) · new 25.33% ±11.79pp (n=75) · v10-matched 44.00% ±23.30pp
(n=25). Two-fixture half-widths at n=175: **±12.74pp** against the old anchor, **±15.80pp**
against the new. **These are reported beside every read so nobody mistakes the primary ±8.65pp
for the full uncertainty on the underlying levels — and, per §4, "consistent with anchor X" is
never a verdict.**

**6c. The anchors are UNPINNED and pool opponent churn** — the old anchor spans their v7/8/9/10,
the new one their v11/13. The pin removes churn from the LEG, not from its comparators.

**6d. `meta_join` covers the ARCHIVED subset.** Unrated games are absent from
`ladder_games.tsv` by construction, so `meta_join` is the correct and only surface for this cut
— this is not a breach of the "never `meta_join` for a denominator" rule, which governs RATED
win-rate denominators. The caveat that does apply is archive coverage, and the freshness assert
in §5.4 is how it is bounded.

**6e. The pinned build ages.** It is pinned to a build last seen 2026-08-13T23:06Z; at fire time
that is roughly a day old. **The leg measures the v10 matchup, not today's Juusto.** State the
pin's age in the readout.

**6f. What an OURS verdict does NOT separate.** The pin fixes their version; it does not fix the
map pool. Both anchors and the leg sit inside the same post-2026-08-13 era (verified in the
`MAP SEGMENT` line), so the pool is matched here — but if the archive's era boundary is later
revised, an OURS verdict would inherit the pool as an unexcluded co-explanation.

**6g. Our own version is not pinned.** `unrated` always plays our ACTIVE submission. If the lane
activates anything else before the leg completes, every game after that point is a different arm
and the leg is void. **The holder must be asserted (`Active bot:` line, never `$?`) before the
first window and after the last.**

## 7. IMBALANCE DISCLOSURE — ONE HEADING, ALL FIXTURE AXES

Reported together and **disclosed rather than corrected** (a matched estimator chosen after the
data is the fault this clause exists to catch): **seat mix** (a/b) of the leg versus each
anchor · **map mix** across the 15-map pool · **opponent version** (must be uniformly 10 in the
leg, per §5.1) · **our version** (must be uniformly 140). Any axis whose leg/anchor distribution
differs materially is named in the readout under this one heading, because a future pooled
reading inherits all of them and is likelier to carry one named confound than four scattered
ones.

## 8. COST

**ZERO.** Our active submission is **already v140** (`fcode status`, 2026-08-14T21:07Z:
`Active bot: v140 (Loki v10)`), so this leg needs **no submit, no activation, no rollback, and
no timing against the ladder's ~20-minute pairing cadence.** `fcode submit` auto-activates and
that hazard is simply not reachable here. **The ~−8 Elo per leaked rated match budget does not
apply: there is nothing to leak.** The only cost is ~2h20m of wall clock on a free surface.

**On the pinning design rule** (`SPEC-opponent-pinning-2026-08-13`): *pin treatment legs, never
pin calibration panels.* This is unambiguously a **treatment leg** — the comparison is between
our arms across time with the opponent held fixed, and opponent variation is pure noise the
design cannot absorb. It is the opposite of a calibration panel, whose whole rationale is
relevance and for which churn is signal. **The pin is not an accessory here; it is the
instrument.**

## FALSIFIER

**The hypothesis is falsified if the leg's pooled game share over 175 games lands at or below
53 wins (ŝ ≤ 30.29%), i.e. the upper 95% bound excludes 39.00pp.** That is our v140 performing
against Juusto's OLD build exactly as it performs against their new one, which leaves our
v125→v139-142 ship as the cause of the −26.67pp cell and makes this a REAL NEGATIVE on the
shipped bot.

**And the leg is falsified as an INSTRUMENT — with no verdict in either direction — if:** the
decoded `oppver` is not uniformly 10 (§5.1) · any `--match` fire errors and is silently
replaced (§5.2) · our active submission changes mid-leg (§6g) · or the tape is stale at read
time (§5.4).

⛔ **A result inside 30.29% < ŝ < 48.00% falsifies NOTHING and confirms NOTHING.** It is
recorded as *could not separate*, the gate is UNRESOLVED, and the restriction stands.
