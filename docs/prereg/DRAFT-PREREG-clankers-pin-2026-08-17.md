# DRAFT PREREG — LEG `clankerspin` : is there a real v155 deficit against Clankers v17, or is 2/10 ordinary variance at a +80 gap?

**STATUS: DRAFT — NOT LOCKED. The owning lane ratifies the judgment lines and types the lock commit.**

Drafted by a FRESH research subagent with no inherited session context beyond the inputs on the
`PROVENANCE:` line. This agent wrote no code under `bots/`, fired no game, issued no challenge,
touched no platform CLI, appended no `BARS.tsv` row, and committed nothing. Drafting wall clock
**`2026-08-17T04:56:00Z`** (`date -u`, same shell session as the git read); repo HEAD at draft
**`89ae6454`** (author time `2026-08-17T06:55:48+02:00`). ⚠ HEAD had already moved to `9f20ee7a`
by the end of this drafting session — another lane is committing concurrently — so **the lane
re-stamps HEAD at the lock commit rather than inheriting the line above.**

⚠ **This document is a DRAFT and is not a lock certificate.** Every number below is reproducible
from the corpus paths named in `PROVENANCE`. Three of the facts handed to this agent did not
reproduce as stated and are corrected in §0; **one of those corrections removes the leg's
motivating anomaly**, and the lane must read §0 and §9 before deciding whether to lock anything
at all.

---

## ⛔ 0. READ BEFORE RATIFYING — FIVE THINGS THE LANE OWNS

### 0.1 THE MOTIVATING ANOMALY DOES NOT SURVIVE ARITHMETIC. 2/10 IS ONE STANDARD DEVIATION FROM EXPECTATION.

The brief frames this leg as closing a gap around a *deficit*. Measured on the corpus:

| null | value | observed 2/10 | z | one-sided p |
|---|---|---|---|---|
| Elo-implied at the two matches' own gaps (mean +79.57) | **0.3875** | 0.2000 | **−1.016** | **0.155** |
| our own measured share at gaps +60..+110, post-rotation (58/135, 27 matches) | **0.4296** | 0.2000 | **−1.225** | **0.110** |

*(sd computed with the unrated within-opponent DEFF 1.434 over n=10 — the two matches are two
clusters, so the effective n here is ≈7.)*

**There is no anomaly. A 2-of-10 at a +80 gap is inside one standard deviation of what the ladder
itself predicts, and the leg as briefed ("attribute the deficit") is registering a hypothesis about
an effect that has not been observed.** Under the obligations doc's Addendum 11 (OB16) this is the
circularity the whole obligation exists to stop, in its sharpest form: sizing an attribution leg
off a point estimate that is not distinguishable from its own null. **The leg is therefore
re-framed below as a MEASUREMENT leg (obligations doc, Addendum 7 — the upward-leg framing), not
an attribution leg.** If the lane wants the attribution framing, it must be refused: §9.

### 0.2 THE RECORD IS 2 WINS / 10 GAMES / 2 MATCHES — AND ONLY ONE OF THE THREE CORPUS SURFACES CAN SEE IT.

Verified three ways, and the surfaces disagree:

| surface | mtime (local) | newest row | v155 × Clankers v17 |
|---|---|---|---|
| `corpus/ladder_games.tsv` | 17 Aug 04:57 (02:57Z) | created `2026-08-17T02:52:59.702Z` | **5 games, 1 match** (2 wins) |
| `corpus/league_matches.tsv` | 17 Aug 06:18 (04:18Z) | created `2026-08-17T04:12:59.546Z` | **1 match** |
| `corpus/meta_join.tsv.gz` | 17 Aug 06:44 (04:44Z) | completed `2026-08-17T04:43:38.168Z` | **10 games, 2 matches** (2 wins) |

The second match is **`3eebdcf7-c165-4d71-9b36-b7a6bb32023c`**, completed `2026-08-17T03:16:41.734Z`,
**us (seat A, v155) 0 — Clankers (seat B, v17) 5**. `grep -c 3eebdcf7` returns **0** in both
`ladder_games.tsv` and `league_matches.tsv`.

⛔ **TWO INSTRUMENT FINDINGS THE LANE SHOULD CARRY OUT OF THIS DRAFT, INDEPENDENT OF WHETHER THE
LEG FIRES:**

1. **`league_matches.tsv`'s TAIL IS PARTIAL, NOT MERELY LAGGED.** Matches per pairing slot in the
   last two hours: `02:52:59 → 40`, `03:12:59 → 10`, `03:32:59 → 11`, `03:52:59 → 11`,
   `04:12:59 → 7`. A full slot is ~40. **So the file has rows created at 04:12 while missing a
   match of ours created at 03:12.** ⇒ **An ABSENCE in the last ~90 minutes of that file is not
   evidence.** Any count over the recent tail is a lower bound.
2. **`CLAUDE.md`'s corpus-surface rule points at the STALE surface in this instance.** The rule
   ("`ladder_games.tsv` for any denominator question about our RATED record; NEVER `meta_join`")
   is about *pooling rated with unrated*, and it does not protect against **decode latency** —
   which is exactly Amendment 1 of the obligations doc (*"freezing from `corpus/` freezes what has
   been DECODED, not what has been PLAYED"*). The correct procedure, and the one this draft
   follows, is: **use `ladder_games.tsv` for the denominator, but sync first or state the lag.**
   This draft states the lag: **`ladder_games.tsv` is one of our own rated matches behind at
   draft time**, and the missing match is a 0-5 against the leg's own target.

### 0.3 THE RATING GAP MOVED, AND THE OBVIOUS NULL IS CONTAMINATED BY THE OBSERVATION THAT MOTIVATED THE LEG.

| clock | our rating | Clankers | gap | Elo E for us |
|---|---|---|---|---|
| before match 1 (`21f5e078`, 01:52:59Z) | 1830.674 | 1906.009 | **+75.335** | **0.3933** |
| before match 2 (`3eebdcf7`, ~03:12:59Z) | 1816.817 | 1900.617 | +83.799 | 0.3817 |
| after match 2 (derived, `delta = 32(S−E)`) | ~1804.60 | ~1912.83 | ~+108.23 | 0.3491 |

⛔ **Registering the null at the CURRENT gap would let the 0-5 that motivated the leg lower the bar
the leg has to clear.** The registered null is therefore **E₀ = 0.3933**, the Elo expectation at the
gap **before either observation entered the ratings**. The other three values are pre-committed
here as declared sensitivity points (§5), so no null is chosen after the data.

⚠ The `~+108.23` row is DERIVED from one known result and assumes no further rated matches since
03:12:59Z; `league_matches.tsv` cannot confirm that (§0.2). **The lane re-runs
`tools/target_value.py --band` at ratification** — this agent did not, because that tool reads our
live rating off `fcode status` (`tools/target_value.py:307`) and this agent is read-only with
respect to the platform. The band line in the registration block is computed arithmetically from
the ladder's own verified formula on corpus ratings.

### 0.4 THE PROGRAMME MAY HAVE PARKED THIS LEG, AND THE PARKING CLAUSE'S STATED REASON DOES NOT APPLY HERE. THIS IS A LANE/MAGNUS CALL, NOT MINE.

`PROGRAMME.md`, under `X3R0_SLOT_RULE RE-PRICED 2026-08-16`:

> *"**This also parks the live unrated leg**: an unrated window requires activating an arm into the
> slot, which this bar now governs — no leg fires until an arm clears 60±2 locally or Magnus
> explicitly opens a window."*

**The clause's stated mechanism is activation cost — and this leg has none.** Our arm IS the live
holder: `PROGRAMME.md: INCUMBENT: bots/_v468kladturbo` → `corpus/version_trees.tsv:88` →
**v155 "Sleipnir v1"**, active since `2026-08-16T19:38:41Z`. `fcode match unrated` plays our ACTIVE
submission, so this leg activates nothing, displaces nothing, and puts **zero prototype seconds on
the rated ladder**. ⇒ **The leg is outside the clause's rationale and arguably inside its letter.**
**A subagent does not get to read a Magnus-authored parking clause narrowly. The lane decides, or
asks him.**

### 0.5 WHAT THE LEG IS NOT

It has **no treatment, no arm, no code diff, and no plank**. It cannot ship anything, cannot clear
`X3R0_SLOT_RULE`'s 60±2 threshold, and cannot close a road on its own (`CLAUDE.md` point 6 governs
how a road is CLOSED; a single-cell profile is not that). Its entire product is a **calibrated
opponent profile** of one stable top-band build, plus the kill-mix diagnostics of §7. **If the lane
cannot name, in advance, what a confirmed deficit would CHANGE, this is a point rule under OB16 and
should not cost twelve windows.** That question is put explicitly in §9.

---

## REGISTRATION BLOCK

**TARGET BAND: Clankers (`03ab46df-7058-49ec-a9f5-592f86e9a95a`), gaps +75.3 .. +108.2 (pre-observation .. post-loss derived), win pays +19.41 .. +20.83 for a 5-0, a 0-5 costs −12.59 .. −11.17, reachable YES — empirically, not modelled: the ladder paired us with them twice inside three hours (01:52:59Z, ~03:12:59Z), both inside the observed `us−80 .. us+125` pairing range, and Clankers at ~1901-1913 clears `RATING_FLOOR 1650` and `TARGET_MIN_PAYOUT: 10` with room. ⚠ ZERO rated exposure on this leg — the payout is the RELEVANCE price of the cell, not a rating expectation from these games (`tools/target_value.py --band` NOT executed by this agent; the lane re-runs it at ratification).**
**PINNED: YES — `PIN=21f5e078-1fb5-4d33-a62e-15ae98f43585 tools/unrated_run.sh 155 <games> 03ab46df-7058-49ec-a9f5-592f86e9a95a` (their v17). ⚠ THE PIN IS CURRENTLY A NO-OP AND IS TAKEN AS INSURANCE, NOT AS CORRECTION: Clankers' live build IS v17 (66 of 66 matches in the trailing 24 h). It is registered because a mid-leg ship by them would otherwise silently split the cell, and because `SPEC-opponent-pinning-2026-08-13.md`'s profiling corollary says a leg describing ONE BUILD pins. ⛔ CONSEQUENCE, stated so it is not quoted wrongly later: a pinned result describes Clankers v17 and may NOT be quoted as ladder RELEVANCE if they ship — that is the calibration-panel use the same spec forbids pinning for.**
**SURFACE: unrated**
**CLUSTER UNIT: match** — CLAUDE.md's enumeration PERFORMED, not asserted. (i) Clusters this data has: **MATCH** and **OPPONENT**. (ii) **MATCH — SURVIVES**: the stratum is one pooled share over all games and every accept contributes exactly 5 correlated games (`fcode match info 21f5e078…` returns 5 game rows; `GAMES_PER=5` at `tools/unrated_run.sh:158`). (iii) **OPPONENT — DIES**: every game is against Clankers pinned to one build, so the stratum holds exactly one member and contains no between-opponent variance. ⚠ **This survives only if the pin takes** — if any game decodes `oppver != 17` the stratum holds two builds and the enumeration changes; that is a second, independent reason the §6 pin-take check is a PRE-CONDITION on the read and not a footnote. (iv) **Applicable DEFF = unrated within-opponent = 1.434.** Over-correcting to the pooled 1.833 would widen every interval ×1.131 for variance this cut cannot contain and would fail in the flattering direction for a "no deficit" reading; under-correcting to 1.000 would narrow them ×0.836. Both are errors and only the enumeration catches either.
**ESTIMATOR: pooled game share = (games won) / (games played), unweighted at the game level, over ACCEPTED-AND-COMPLETED matches only, restricted to rows decoding `ourver == 155` AND `oppver == 17`. With every match at 5 games this equals the mean of per-match shares; if any match returns fewer than 5 games the pooled form governs.**
**DOSE: decoded `oppver` = 17 and `ourver` = 155 in every game of the leg. n=300 games planned. There is no treatment to dose — the "dose" here is fixture identity, and it is 100% or the leg is void (§6).**
**PLANNED n: 300 games (60 accepted unrated matches = 12 windows of 5).**
**BOUNDARY: 60 accepts = 300 games. ACCEPTS, not attempts — rejected challenges spend the rate window and create no match (`tools/unrated_run.sh:53`), so an attempt-denominated boundary would over-count by exactly the rejection rate. (This is CAL-8's 2026-08-14 defect; the identity `games = 5 × accepts` is the check.)**
**CUT-SHORT: 150 games (30 accepts, 6 windows).** Below 150 completed games this leg publishes descriptive tallies only (share, per-map, per-seat, win-condition mix, kill rounds) and takes **NO bar verdict in either direction**. Between 150 and 300 games **only the MDE-15pp reading of §5 is licensed**, and the MDE-10pp reading is reported as UNRESOLVED. This is pre-committed now so a short leg cannot pick its own bar afterwards.
**BAR: 35.95 — constructed, not observed: `E₀(39.33) − MDE(10.00pp) + half_width(6.62pp)` at n=300, DEFF 1.434.** Clearing it means the 95% interval's LOWER edge excludes a true share at or below **29.33%**, i.e. it excludes a deficit of 10pp or more against the ladder's own expectation. **The MDE is INSIDE the bar's construction, per OB16's amended preferred form — this bar cannot be quoted without its MDE because the MDE is one of its terms.**
**BASE RATE: 39.33 — E₀, the Elo-implied expected game share at gap +75.335.**
**BAR SOURCE: constructed. `E₀ = 1/(1+10^(75.335/400)) = 0.39333`, from `ratingABefore/ratingBBefore` on match `21f5e078-1fb5-4d33-a62e-15ae98f43585` (`corpus/ladder_games.tsv`, `corpus/league_matches.tsv`, `corpus/meta_join.tsv.gz` — all three agree on this match's ratings). The ladder's `delta = 32×(S−E)` with `S = games/5` is verified to max residual 0.000000 across 100 matches (builder) and 0.0000 across 678 (research), so E is an EXACT property of the two ratings, not an estimate. half_width = `1.96·sqrt(E₀(1−E₀)·1.434/300)`.**
**BASE RATE SOURCE: as above — a CONSTANT fixed at lock, deliberately taken at the gap BEFORE either observed match entered the ratings (§0.3).**
**REFERENCE n: none.** The registered rule compares the leg's share to a PRE-REGISTERED CONSTANT (39.33) — it is not differenced against a sample — so no reference term enters the primary interval and there is no resolution floor at n→∞. ⛔ **This is a deliberate design choice against a real trap:** the natural alternative reference (our own rated share at gaps +60..+110, **58/135 over 27 matches, 42.96%**) is a SAMPLE THAT CANNOT GROW ON THIS LEG, and its two-fixture floor is **±9.76pp at n_unrated = ∞** (`1.96·sqrt(p̄(1−p̄)·1.366/135)`, p̄=0.43). **A 10pp MDE registered against that reference would be unresolvable by construction** — CAL-7's exact defect, which `tools/prereg_check.py` was built to catch. The empirical band share is reported in §6b as DESCRIPTIVE with its two-fixture arithmetic and **may never be the verdict**.
**POOL ERA: 2026-08-13T07:12:59Z..now — the post-rotation 15-map pool.** All anchor cuts in this document are restricted to it.
**TREATMENT TREE: N/A — no arm tree exists. Our side is the ACTIVE platform submission v155 "Sleipnir v1" = `bots/_v468kladturbo` (`corpus/version_trees.tsv:88`, activated 2026-08-16T19:38:41Z), byte-unmodified.**
**TREATMENT DIFF REFS: HEAD HEAD** — `git diff --name-only HEAD HEAD` is empty by construction, the literal expression of "this leg has no treatment diff". Declared explicitly so the default (`git diff HEAD`) does not pick up unrelated working-tree edits and treat them as this leg's treatment. ⛔ `prereg_check` will report `OB13_INTERSECTION CANNOT-COMPUTE` + WARN permanently for this leg and **that is CORRECT** — there is no arm tree and none will ever land. Do not "fix" the warning by naming a diff this leg does not have.
**MECHANISM METRIC READS: `tools/corpus/unrated_games.py:153-155` — the two lines that assign `opp_ver` / `our_ver` from the match meta by our seat, emitting `corpus/unrated_games.tsv` (columns `oppver`, `ourver`, `cond`, `turns`, `won`; 6,597 rows at draft, mtime 2026-08-17T04:45Z). TREATMENT DIFF TOUCHES: NONE. INTERSECTION: N/A by construction — there is no treatment. The substantive Obligation-13 question is answered instead by the identity: the metric's VALUE IS THE FIXTURE LABEL, so the LOKI-18 failure (a metric that reads identically whatever the arm does) cannot arise. ⭐ This read path is named because the fixture that preceded it did NOT have one: `unrated_games.py`'s own docstring records that `join.tsv` is keyed off `ladder_games.tsv` and is RATED-ONLY BY DESIGN, so LEG-fieldcal's registered ITT RMST₃₀₀ secondary had NO computable surface at any completion fraction. That surface now exists and is the one this leg reads.**
**METRIC WINDOW: r0–r1000 for the primary (a game's `won` is defined at its end). r0–r300 for the RMST₃₀₀ diagnostic of §7, per `PROGRAMME.md`'s 2026-08-16T05:36:10Z ruling that an RMST-style kill-speed primary uses horizon 300. GATING CONSTANTS: none — no plank of ours is gated in this leg. MECHANISM CAN OCCUR IN WINDOW: yes, trivially — the fixture label is written by the platform at match creation and is present on every row.**
**GATE RESOLUTION (OB12): the three-branch rule of §5 discriminates its branches at n = 300 with 84.2% power on the DEFICIT-EXCLUDED branch against a 10pp MDE, and at n = 150 with 88.1% power against a 15pp MDE only. At n = 25 (±22.93pp) and n = 50 (±16.21pp) it cannot discriminate at all — a single window is a DOSE AND MECHANISM probe, never a currency read. UNRESOLVED ⇒ THE RESTRICTION, NEVER THE PERMISSION: no deficit is asserted, no deficit is excluded, both roads stay open, and no ship, no de-prioritisation, no opponent-specific plank and no road-closure may cite this leg.**
**PRE-STATE (OB7): the predicted-change set is NOT already in the target state at lock. Verified on `corpus/meta_join.tsv.gz`: across the entire archive the OpenSverige × Clankers cells are exactly two — `ourv 68 × oppv 1` (5 games, ladder) and `ourv 155 × oppv 17` (10 games, ladder). Games of (our v155 × their v17, UNRATED) = 0. The cell this leg fills is EMPTY. ⭐ And the OUTCOME TYPE is declared per OB7: this leg's primary is a GAME SHARE, not a win-condition mix; the win-condition mix appears only as the §7 diagnostic and is reported IN OUR FAVOUR and as a MIX separately, never conflated.**
**MAP SEGMENT: none expected — no plank of ours is toggled and no terrain property enters the estimand, which is an opponent-profile share against one fixed build. There is nothing map-conditional to declare a direction for, and OB15a's alternative branch requires a predicted sign that this design cannot honestly supply. ⛔ CONSEQUENCE, pre-committed: per-map shares WILL be printed at readout as exploratory description, they carry NO pre-registered direction, NO map cut may rescue a failed or unresolved primary, and nothing may be banked off them without a fresh prereg. The UNITS RIDER applies to any per-map table that is nonetheless printed: the MATCH cluster dies on a per-map cut (a 5-game match uses five different maps; (match, map) pairs with >1 game = 0 of 415) and the residual OPPONENT cluster is degenerate here (one opponent) ⇒ per-map descriptive intervals take DEFF ≈ 1.00, NOT 1.434.**
**CELLS: one — Clankers (`03ab46df-7058-49ec-a9f5-592f86e9a95a`), pinned to v17.**
**CELL VERSION CHURN (OB14): Clankers ran ONE distinct version (17) across 66 matches in the 24 h to 2026-08-17T04:53Z (`corpus/league_matches.tsv`) — the LEAGUE MEDIAN is 1 across 83 teams (45 of 83 teams at 1; the distribution runs 1..11). Over the longer window their v17 has stood since `2026-08-14T00:52:59.692Z` across 223 matches, own game share **0.4703 (522/1110) over 222 matches with OUR matches excluded**. This is a POOLABLE cell by OB14 and it is the best-scoring cell available. ⚠ OB14's normalisation premise is FALSE TODAY and I re-checked rather than inheriting it: it records "every team played EXACTLY 87 matches in the window"; measured now the range is 31..70 across 83 teams (median 66), so raw version counts are not perfectly comparable — Clankers' 1 must be read against its 66 matches, which sits at the median. ⛔ OUR OWN CHURN IS THE HIGH SIDE OF THIS CELL: OpenSverige ran THREE versions (152, 153, 155) over 66 matches in the same window. See §6 for the arm-identity guard that follows from it.**
**PROVENANCE: docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md · PROGRAMME.md · docs/research/SPEC-opponent-pinning-2026-08-13.md · CLAUDE.md · docs/prereg/LEG-juustopin-2026-08-14.md (format only) · docs/prereg/PREREG-KLADLADDER-2026-08-17.md (format only) · docs/prereg/PREREG-CAL418-2026-08-15.md (listing only) · corpus/ladder_games.tsv · corpus/league_matches.tsv · corpus/meta_join.tsv.gz · corpus/unrated_games.tsv · corpus/version_trees.tsv · tools/unrated_run.sh · tools/target_value.py (READ ONLY — NOT EXECUTED) · tools/prereg_check.py (docstring only) · tools/corpus/unrated_games.py · tools/panel_read.py · tools/triarm_read.py · git log -1 · date -u. ⛔ NO PLATFORM CLI WAS CALLED BY THIS AGENT — no `fcode status`, no `fcode match list`, no `fcode match info`. Every fact is off the corpus or the tree.**

---

## 1. HYPOTHESIS (as re-framed; see §0.1 and §9)

**Our shipped v155 "Sleipnir v1", playing unrated against Clankers pinned to their v17, will land a
pooled game share whose 95% interval EXCLUDES a deficit of 10 percentage points or more against the
ladder's own expectation for that matchup (E₀ = 39.33%) — i.e. there is no Clankers-specific hole
large enough to be worth a plank.**

Falsifiable in one number, in both directions, against a constant fixed before the fire.

**This is a MEASUREMENT registration, not a climb registration**, per the obligations doc's
Addendum 7: the question is *"what is our true standing and arrival/kill mix against a strong,
stable, top-band defence"*, never *"can we win upward"*. **No win prediction is made and none may
be read into a result.**

## 2. WHY THIS LEG EXISTS — AND WHAT IT CANNOT DO

**What is genuinely unmeasured:** we have **10 lifetime games** against Clankers' current build,
across 2 rated matches, in a fixture where 5 games share one opponent version and one 20-minute
ladder slice. Any statement about *"how we do against Clankers"* today rests on an effective n of
about **7**. That is not a deficit and it is not a parity claim; it is nothing.

**Why this cell and not another:** Clankers is simultaneously (a) the most version-stable opponent
on the board (1 version / 66 matches / 3 days, against a league distribution running to 11),
(b) inside the reachable pairing band and paired with us twice in three hours, (c) above
`RATING_FLOOR 1650` with a 5-0 paying ~+20, and (d) a **top-band defence**, which is what
Addendum 7 says an upward leg exists to characterise. **The stability is the whole argument: a
number measured against a build that does not move is attributable to us.**

**What it cannot do, stated so it is not over-read later:**
* It cannot close a road (`CLAUDE.md` point 6 — closure needs live-game evidence *and* a road; this
  is a profile).
* It cannot ship, promote, or authorise an activation (`X3R0_SLOT_RULE`).
* It cannot be quoted as ladder relevance if Clankers ships (the pin, §Registration).
* It cannot rescue itself on a map cut (`MAP SEGMENT`).

## 3. THE POWER ARITHMETIC

One accept is **5 games**; the platform allows **5 test/unrated matches per 20 minutes**, shared
across `match unrated` and `match test`, and **rejected attempts appear to count**. So
**one window = 5 accepts = 25 games = 20 minutes** of wall clock, plus the runner's pairing-clock
guard (`GUARD_S=150` default, `tools/unrated_run.sh:159`).

Half-widths are `1.96·sqrt(p(1−p)·DEFF/n)` at **DEFF = 1.434** and p = E₀ = 0.3933. Power is the
probability of clearing the constructed bar **when the truth is exactly E₀** — i.e. the probability
that a leg against an opponent we have no real deficit against will successfully SAY SO.

| n | accepts | windows | wall clock | half-width | BAR @ MDE 10pp | slack vs E₀ | power @ 10pp | BAR @ MDE 15pp | power @ 15pp |
|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|
| 25 | 5 | 1 | 20 min | ±22.93 | 52.26 | −12.93 | **13.5%** | 47.26 | 24.9% |
| 50 | 10 | 2 | 40 min | ±16.21 | 45.54 | −6.21 | 22.6% | 40.54 | 44.2% |
| 75 | 15 | 3 | 1 h | ±13.24 | 42.57 | −3.24 | 31.6% | 37.57 | 60.3% |
| 100 | 20 | 4 | 1 h 20 | ±11.47 | 40.80 | −1.47 | 40.1% | 35.80 | 72.7% |
| 125 | 25 | 5 | 1 h 40 | ±10.25 | 39.58 | −0.25 | 48.1% | 34.58 | 81.8% |
| **150** | **30** | **6** | **2 h** | ±9.36 | 38.69 | +0.64 | 55.3% | **33.69** | **88.1%** |
| 200 | 40 | 8 | 2 h 40 | ±8.11 | 37.44 | +1.89 | 67.6% | 32.44 | 95.2% |
| 250 | 50 | 10 | 3 h 20 | ±7.25 | 36.58 | +2.75 | 77.1% | 31.58 | 98.2% |
| **300** | **60** | **12** | **4 h** | **±6.62** | **35.95** | **+3.38** | **84.2%** | 30.95 | 99.3% |
| 350 | 70 | 14 | 4 h 40 | ±6.13 | 35.46 | +3.87 | 89.2% | 30.46 | 99.8% |
| 400 | 80 | 16 | 5 h 20 | ±5.73 | 35.06 | +4.27 | 92.8% | 30.06 | 99.9% |

**A "slack" column that is NEGATIVE means the bar sits ABOVE the null** — i.e. at n ≤ 125 the design
demands a share BETTER than expectation before it will concede that expectation is being met. That
is not a bar, it is an impossibility, and it is why the cut-short floor is 150 and not lower.

⇒ **PLANNED n = 300 games (60 accepts, 12 windows, ~4 hours).** It is the smallest multiple of a
window reaching ≥ 84% power on the 10pp exclusion, with **3.38pp of slack** between the bar and the
null. **The GUNAXABL lesson is respected deliberately:** that arm missed its keep edge by 0.0152pp —
**one game** — on a bar whose slack was zero by construction. A design with 0.25pp of slack (n=125)
is a design whose verdict is a coin flip about which single game landed where.

**⚠ COST, STATED PLAINLY: 12 twenty-minute rate-limit windows, ~4 hours of runner wall clock.**
Not 12 windows of rating: **zero**, because our arm is the live holder. The price is wall clock and
lane attention, on a surface Magnus has declared free (*"You are free to use unrated games as much
as you want"*), against a rate limit that is the entire cadence constraint.

## 4. STAGED FIRE — AND WHY THE CONTINUATION RULE MAY NOT LOOK AT THE SHARE

**STAGE 1 — one window (5 accepts, 25 games, 20 min). Registered output: DESCRIPTIVE ONLY + INSTRUMENT VERIFICATION.**
No bar, no verdict, no share claim, in either direction. Its purpose is to prove the fixture end to
end on a surface that has failed before (`unrated_games.py`'s docstring: LEG-fieldcal's registered
secondary had no computable surface at any completion fraction).

**STAGE 2 — the remaining 11 windows, fired only if all four STAGE-1 instrument checks pass (§6).**

⛔ **THE CONTINUATION RULE IS A FUNCTION OF INSTRUMENT VALIDITY AND OF NOTHING ELSE. THE STAGE-1
SHARE MAY NOT BE LOOKED AT BEFORE THE STAGE-2 DECISION IS TAKEN.** A continuation rule that reads
the outcome is optional stopping with extra steps, and it is exactly the temptation that the
GUNAXABL replication discipline refused (*"they corroborate a null they are not allowed to
rescue"*). If the lane cannot hold that line operationally, **fire the full 300 in one go or do not
fire at all** — a staged design whose gate peeks is worse than an unstaged one.

## 5. DECISION RULE

Let **ŝ** = pooled game share over the leg and **hw(ŝ) = 1.96·sqrt(ŝ(1−ŝ)·1.434/n)** evaluated at
the observed ŝ. This formula is pre-registered so that no estimator choice remains after the data.
**E₀ = 39.33** is a CONSTANT, fixed now.

| branch | fires when | reading, pre-committed |
|---|---|---|
| **NO MATERIAL DEFICIT** | `ŝ − hw > 29.33` (= E₀ − 10pp) | The 95% interval EXCLUDES a deficit of ≥10pp. Clankers v17 is an ordinary top-band opponent for v155; the 2/10 was variance. **No Clankers-specific plank is warranted.** |
| **DEFICIT CONFIRMED** | `ŝ + hw < 29.33` | The interval excludes anything better than a 10pp deficit. A real, attributable hole exists against a stable build ~+80 above us. **This is the only branch that licenses a follow-up**, and the follow-up is a MECHANISM leg (what kills us — see §7), never a share re-run. |
| **UNRESOLVED** | otherwise | **THE RESTRICTION, NEVER THE PERMISSION.** Neither claim is granted. Nothing may cite this leg. |

**Restatement discipline, required by `CLAUDE.md`'s DEFF direction clause and applied here rather
than assumed:** the NO-MATERIAL-DEFICIT branch is a **fail-to-exclude claim restated as an
EXCLUSION** — it says *the CI excludes a ≥10pp deficit*, never *we found no significant deficit*.
That restatement is what makes the DEFF correction operate in the conservative direction. **Written
in the unrestated form, the 1.434 inflation would launder a weak null into a confident one, and
this leg's most likely outcome is exactly that class of claim.**

**Pre-committed sensitivity set (all four nulls declared NOW, none chosen after the data):**
E₀ = **39.33** (registered primary, pre-observation gap) · **38.17** (gap at match 2) ·
**34.91** (post-loss derived gap) · **42.96** (our measured +60..110 band share, DESCRIPTIVE only,
§6b). The verdict is read on E₀. **If the branch flips across that set, the leg is UNRESOLVED
whatever E₀ says** — a verdict that depends on which null was picked is not a verdict.

## 6. PRE-CONDITIONS ON THE READ — FOUR INSTRUMENT CHECKS, ALL FROM `corpus/unrated_games.tsv`

1. **PIN TOOK.** Every leg game decodes `oppver == 17`. **A game decoding otherwise is an
   INSTRUMENT ALARM** (`SPEC-opponent-pinning-2026-08-13.md`), not a data point: report it, and
   stop reading the cell until resolved. It also breaks the §Registration cluster enumeration.
2. **ARM IDENTITY HELD.** Every leg game decodes `ourver == 155`. ⛔ **This is not ceremony — WE are
   the high-churn side of this cell (3 versions in 24 h), and a teammate ship into the slot mid-leg
   is a live scenario with a dated precedent** (x3r0 activated v153 mid-cycle on 2026-08-16 and
   `unrated_run.sh`'s restore un-shipped him for ~75 minutes). The runner now aborts loudly on a
   holder mismatch (`tools/unrated_run.sh:367`, `:203-208`). **Games played under any other
   `ourver` are EXCLUDED from the primary and reported separately with their version.**
3. **THE SURFACE IS POPULATED.** `corpus/unrated_games.tsv` contains the leg's matches with
   non-null `cond`/`turns`. A row count of zero for the leg's match ids is the LEG-fieldcal failure
   recurring and voids the secondary, not just delays it.
4. **ACCEPTS, NOT ATTEMPTS.** `games = 5 × accepts` must hold on the runner's own `arm_*.txt`
   ledger. A mismatch means rejected attempts were counted as accepts and the boundary is wrong.

**All four are checks that CAN come out the other way** (OB17's rider — a clause whose verdict is
already known is ceremony). Checks 1 and 2 have both fired in this repo's history; check 3 has
fired on LEG-fieldcal; check 4 is CAL-8's dated defect.

### 6b. DESCRIPTIVE ANCHORS — REPORTED BESIDE THE VERDICT, NEVER AS IT

| anchor | value | n | note |
|---|---|---|---|
| our rated share at gaps +60..+110, post-rotation, ALL versions | **42.96%** (58/135) | 135 games / 27 matches | mean Elo E over the same games = 39.24% ⇒ **we run ~+3.7pp above the Elo curve upward** |
| same, v152/153/155 only | 44.00% (22/50) | 50 / 10 | |
| same, v155 only | 40.00% (4/10) | 10 / 2 | **these are the Clankers games themselves — not an independent anchor** |
| Clankers v17 own share, our matches EXCLUDED | **47.03%** (522/1110) | 1110 / 222 | league-wide, their build's own strength |
| v155 × Clankers v17, rated | **20.00%** (2/10) | 10 / 2 | the observation, at effective n ≈ 7 |

**Two-fixture arithmetic if anyone insists on differencing the leg against the +60..110 band:**
`hw = 1.96·sqrt(p̄(1−p̄)(1.434/n_u + 1.366/135))` gives **±13.61pp at n_u=150, ±11.84pp at n_u=300,
±11.06pp at n_u=500, and a FLOOR of ±9.76pp at n_u=∞.** ⇒ **A 10pp claim against that reference is
unresolvable by construction, at any leg length.** It is printed here so nobody re-derives it as a
finding, and it is the reason the primary uses a constant.

## 7. SECONDARY DIAGNOSTICS — DESCRIPTIVE, PRE-DECLARED, AND NEVER A VERDICT

Addendum 7 says an upward leg's read is *"what does a stronger defence do to our arrival/kill
mix"*, and that is the part of this leg most likely to feed a build. All from
`corpus/unrated_games.tsv` (`cond`, `turns`):

* **D1 — ITT RMST₃₀₀**: mean kill time censored at r300 over ALL leg games (a non-kill scores 300).
  Horizon 300 per `PROGRAMME.md`'s 2026-08-16T05:36:10Z ruling. Reported beside our post-rotation
  RMST₃₀₀ against the field. **Descriptive: this leg has no control arm, so it CANNOT score
  `DEFENCE_ADMISSION_BAR` and must not be quoted as if it had.**
* **D2 — win-condition mix**, reported twice and never conflated (OB7): the MIX
  (`core_destroyed` vs r1000 tiebreak, both sides) and the share IN OUR FAVOUR.
* **D3 — timely-kill rate**: share of ALL leg games ending in a core-kill by r300 (the ITT form,
  not the collider-carrying kill-win-conditioned form).
* **D4 — r1000 count.** `R1000_IS_DEFEAT: yes` is unconditional; a tiebreak win in this leg is
  logged as a defeat in the programme's ledger even where the ladder pays for it.
* **D5 — seat and map mix**, reported under ONE heading as a single fixture-balance property
  (Addendum 8's companion: two imbalances are one defect and must be named once).

**None of D1–D5 can rescue an unresolved primary, and none may be banked without a fresh prereg.**

## 8. OBLIGATION-BY-OBLIGATION STATUS

| # | obligation | status in this draft |
|---|---|---|
| 1–4 | Ouroboros-specific (observable-at-lock control, seat confound, half-leg sizing, blind maps) | N/A — different leg; the durable half (label anything observable at lock) is honoured: §0.2's 2/10 is fully observable and is NOT presented as pre-registered evidence. |
| 7 | outcome type declared; predicted-change set not already in target state | **MET** — share not mix, declared; the (v155 × v17, unrated) cell is EMPTY. |
| 8 | denominator rule / per-opponent, Ns stated | **MET** — one cell, one opponent, every N inline. |
| 10 | closure needs identity | **N/A** — no closure test, no ledger with two sides. |
| 11 | treatment check in the experiment's causal variable | **MET by substitution** — no treatment; the causal variable is fixture identity and §6.1/6.2 verify THAT, not an implementation proxy. |
| 12 | a gate carries its resolution statement; unresolved ⇒ restriction | **MET** — `GATE RESOLUTION` line, powers stated per branch, restriction default pre-committed. |
| 13 | mechanism metric `file:line` + diff intersection | **MET in substance, WARN in tooling** — path named (`tools/corpus/unrated_games.py:153-155`); intersection N/A by construction and the permanent `prereg_check` WARN is pre-explained. |
| 14 | cell scored on version stability before selection | **MET, and it is the leg's best property** — 1 version / 66 matches / league median 1; the obligation's own normalisation premise re-checked and found false, with the correction applied. |
| 15 | map dependence declared with a direction, one primary segment | **MET via the "none expected" branch**, with the rescue explicitly forbidden and the per-map DEFF rider applied (≈1.00, not 1.434). |
| 16 | MDE inside the bar; size off what you must EXCLUDE | **MET** — `BAR = E₀ − MDE + hw = 39.33 − 10.00 + 6.62 = 35.95`, the deficit-direction mirror of OB16's preferred constructed form (`null + MDE + hw`), so clearing the bar IS the exclusion; sized off the 10pp exclusion, never off the observed 20%. ⭐ **§0.1 is this obligation biting hardest: sizing off the observed 2/10 is precisely the `#17` circularity, and it would have produced a confident-looking leg around a −1σ fluctuation.** |
| 17 | registered method executable by the executing tool | **MET, all three parts — see §8b.** |

### 8b. OBLIGATION 17 — RUN AGAINST THE RUNNER, CLAUSE 3 FIRST

Per OB17's rider, the clause that can still surprise is run first.

**Clause 3 — CONSEQUENCE OF SILENT NON-EXECUTION: CLOSED, AND LOUDLY.**
`tools/unrated_run.sh:404-406` refuses to fire when `PIN` is empty unless `UNPINNED_OK=1`:
*"ABORT: PIN is empty and UNPINNED_OK != 1. Refusing the silent-unpin fall-through — a pinned
design that loses its PIN variable must fail loudly."* ⇒ **the quiet failure mode this obligation
exists for cannot occur on this runner.** `:392-395` additionally aborts if `PIN` is given with
more than one cell. This leg has exactly one cell.

**Clause 1 — NAME THE EXECUTING TOOL:** `tools/unrated_run.sh`, invoked
`PIN=21f5e078-1fb5-4d33-a62e-15ae98f43585 tools/unrated_run.sh 155 300 03ab46df-7058-49ec-a9f5-592f86e9a95a`.

**Clause 2 — CONFIRM THE RUNNER EMITS IT:** `tools/unrated_run.sh:397` emits
`.venv/bin/fcode match unrated "$id" --match "$PIN" --json`. **This is the exact defect that killed
`PREREG-CAL418` at fire time** (the runner then fired a bare `fcode match unrated`); the pin path
was added s44 and is present at draft.

**⚠ ONE OB17 RESIDUAL THE LANE MUST RULE ON, AND IT IS NOT A BLOCKER BUT IT IS NOT NOTHING.**
The runner is built for PROTOTYPE legs: it activates `$VER` each cycle (`:369`) and restores the
holder afterwards. **With `VER == MAIN == 155` it will call `fcode submission activate 155` while
v155 is already active, once per cycle — twelve redundant platform writes on the live slot.** The
guards then pass by construction (`:367` checks the holder is `v$MAIN`; `:372-376` checks it is
`v$VER`; both are v155), so **the pre-flight guard and the post-activate guard become guards that
cannot fail for this leg** — the guard-that-cannot-fail defect, arrived at from an unusual
direction. It is benign here (there is no prototype to leak) but it should be **named in the lock
commit rather than discovered in the log**, and the lane may prefer a `--no-activate` path.

---

## 9. ⛔ WHERE THIS LEG CANNOT BE RESOLVED AS FRAMED — AND THIS AGENT'S RECOMMENDATION

**Three findings, in descending order of how much they should change the lane's mind.**

### 9.1 THE ATTRIBUTION FRAMING IS NOT RESOLVABLE AND MUST BE REFUSED.

The brief asks whether v155 *"has a real, attributable deficit"* against Clankers **or whether the
observed record is ordinary variance**. That question is **already answered by arithmetic, for
free**: 2/10 is **−1.02σ** from the ladder's own expectation (p = 0.155 one-sided). **There is
nothing to attribute.** Registering a leg to attribute a fluctuation is the `#17` circularity
(OB16) with a different subject line, and it is the failure mode the obligations doc has written up
twice.

**Further, the counterfactual arm the attribution framing would need does not exist.** *"Is v155
worse against Clankers than v152 was"* is UNMEASURABLE and **remains unmeasurable after this leg**:
we have **zero `ourver 152` rows against Clankers** at any version, `fcode match unrated` plays only
our ACTIVE submission, and there is **no flag that points it at a local tree** — so a v152 arm costs
a real activation of a superseded bot into the live slot, which `X3R0_SLOT_RULE` governs and
`SHIP_SIT_MIN_K` complicates. **A pinned-opponent leg pins THEM, never US.** ⇒ **The
v155-vs-v152-against-Clankers question is closed to this instrument, and no amount of n opens it.**

### 9.2 A SECOND CELL (JUUSTO) BUYS LESS THAN IT COSTS AND SHOULD NOT BE ADDED.

The brief offers Juusto v13 as a comparison arm. Verified: Juusto v13, stable since
`2026-08-14T14:12:59.602Z`, **183 matches**, own share **48.47% (429/885) over 177 matches** with
ours excluded, gap **+36.31**, a 5-0 pays **+17.67**. A good cell. **But:**
* **OB8 forbids pooling the two** ("bars per band, never pooled"), so it is a second bar at a
  second n — **24 windows, ~8 hours**, not 12.
* **The contrast it would provide already exists in the corpus for zero games**: our post-rotation
  share by gap band (§6b), n=135 across 27 matches, which is a wider and more relevant reference
  than one extra opponent.
* We played Juusto **2-3 at 02:52:59Z today** (v155 × their v13), so that cell is also live and
  also unremarkable.
⇒ **Recommend AGAINST. The smallest admissible design is one cell.**

### 9.3 THE LEG HAS NO REGISTERED CONSEQUENCE, AND UNDER OB16 THAT MAKES IT A POINT RULE.

**The question the s28 target-value gate exists to force is not "what does a win pay" — this cell
passes that easily — it is "what would we DO differently."** On the most likely branch (no material
deficit, ~84% probable if the truth is E₀) the answer is *nothing*. On the DEFICIT-CONFIRMED branch
the answer is *"run a mechanism leg"* — which is a different leg, not this one's output.

⇒ **THIS AGENT'S RECOMMENDATION, and the brief invited it: DO NOT LOCK THE 12-WINDOW LEG TODAY.**

**FIRE STAGE 1 ONLY — one window, 25 games, 20 minutes — registered as what it is: a
DOSE-AND-MECHANISM PROBE that takes no currency read** (`CLAUDE.md`: *"A 25-game window is a DOSE
AND MECHANISM probe. A currency read requires pooling windows"*), whose registered products are
(a) the four §6 instrument checks against a fixture that has failed before, (b) the D1–D5 kill-mix
descriptives against a top-band stable defence, which is the part Addendum 7 actually asks for and
which the local corefill fixture structurally cannot produce, and (c) the pin/arm decode path
proven end to end on `corpus/unrated_games.tsv`.

**Then let the lane decide whether the remaining 11 windows buy anything — WITHOUT looking at the
Stage-1 share (§4).** If the answer is *"we would do nothing either way"*, the honest close is to
bank the profile and stop, and this draft will have cost one window instead of twelve.

**And §0.4 stands above all of this: if the `X3R0_SLOT_RULE` parking clause binds, not even Stage 1
fires without Magnus.** This agent will not read a Magnus-authored parking clause narrowly on the
lane's behalf.

---

## 10. AMENDMENT CLAUSE

If this draft is locked, it becomes immutable at the lock commit. Corrections land as **new dated
documents**, never as edits, per the standing practice this repo adopted with
`PREREG-ouroboros-loki2-2026-08-09.md`. **ADD-only amendments** (a metric added, a caveat named)
are permitted before the first challenge is issued and must be committed before it; **no amendment
after the first accept may touch the bar, the MDE, the null, the planned n, the cut-short floor, or
the decision rule.**

**Lock certification is the lane's, on two clocks:** this document's lock-commit git author time
against the platform `createdAt` of the leg's FIRST challenge. ⚠ If the runner does not stamp its
own START, the leg can only be dated by its first RESULT row — written at game *completion* and
therefore one game length late — in which case the certification phrase is **"predates first-row"**,
never "predates leg creation".

**Before the lock commit the lane should run:**
`.venv/bin/python tools/prereg_check.py docs/prereg/<locked-name>.md` (gate on the last line,
never on `$?`) and `.venv/bin/python tools/target_value.py --band` (§0.3).
