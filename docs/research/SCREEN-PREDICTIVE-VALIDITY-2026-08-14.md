# DO OUR LOCAL HEAD-TO-HEAD SCREENS PREDICT LADDER FIELD PERFORMANCE?

**Research arm instrument-validation cut, 2026-08-14. READ-ONLY audit of our own
method — no bot was touched, no match fired.**
Clock: `date -u` = `2026-08-14T19:28:23Z`.
Populations: `corpus/ladder_games.tsv` (4,920 game rows / 984 five-game matches,
2026-08-05T19:42Z → 2026-08-14T18:52Z) for the RATED field side;
`results.tsv`, `docs/prereg/SCREEN-*`, `scratchpad/overnight*/`,
`scratchpad/corefill.log`, `corpus/version_trees.tsv` for the LOCAL screen side.

---

## RULING

**Unanswerable from current data, and the blocker is NOT the screen side — it is
the field side.** We have six version-pairs in all of history where a local
head-to-head screen exists between two bots that each held the ladder slot. In
**five of six the LOSING version's rated tenure is 0–15 games**, which is not a
weak measurement, it is no measurement: at 15 games the 95% half-width on a game
share is ±25pp. **Exactly ONE pair (v140 vs v139) has a field difference that is
resolved at all, and on it the screen was right (screen 59.26% for v140 at
n=5,400; field +27.2pp for v140, 95% CI [+4.2, +50.2] with DEFF=1.529, and
[+8.6, +45.8] naive).** Counting sign agreement across the four pairs whose screen
produced an informative verdict gives **k = 3 concordant of m = 4** — and **m = 4
with three of the four field sides statistically empty is not evidence of
anything.** A 3-of-4 sign count has a two-sided exact p of 0.63 against a coin.
**We have not priced the assumption, and on this evidence we cannot.** The deeper
finding is worse than sparsity: **across the 17 versions with ≥15 rated matches,
the between-version variance in mean Elo delta per match is statistically
indistinguishable from sampling noise (ANOVA F(16,612) = 0.840, p = 0.64;
variance-components estimate of the true between-version SD = 0.000).** Our rated
record, at the tenure lengths we actually grant a version, **cannot rank our own
versions** — so it cannot serve as the criterion against which a screen is
validated. **The one thing we are failing to record is a matched, equal-n field
read for BOTH arms of every screen; the ladder will never supply it, because the
slot only ever holds one arm and the loser's tenure is whatever survived until it
was displaced.**

---

## 1. WHAT A SCREEN IS AND WHAT THE LADDER PAYS — the reason this question exists

* A screen (`SCREEN-v140vs142`, `SEALREPAIR`, the `battery-n1024` arms) measures
  **P(A beats B)** on a local, balanced, seed-partitioned fixture.
* The ladder pays **`delta = 32 x (S - E)`**, `S = games won / 5` — i.e. **P(A
  beats the POOL)**, integrated over whoever the pairer supplies.
* These two coincide only under **transitivity**. Non-transitivity is normal in
  RTS pools and is actively manufactured here: three of the six pairs below are
  screens against submissions literally named *Counter Router* / *Top Team
  Router*, whose author had our tree available.
* `PROGRAMME.md:28` `X3R0_SLOT_RULE: screen_n1000_reactivate_on_51` makes the
  screen the **sole** resolution mechanism for the slot. That is a load-bearing
  assumption with no measured validity coefficient behind it. This cut was an
  attempt to supply one.

---

## 2. FIELD PERFORMANCE PER VERSION (the easy half)

Command (research recompute, stored `eloDelta` deliberately not trusted):

```
group corpus/ladder_games.tsv by `match` (984 matches, ALL exactly 5 games,
  `ourbef` constant within match in 984/984 — both verified before use)
S = games_won / 5
E = 1 / (1 + 10**((oppbef - ourbef)/400))
delta = 32 * (S - E)
```

**Versions with ≥15 rated matches (17 of 105 versions that ever appear):**

| ver | matches | games | share | 95% hw (DEFF 1.529) | mean Elo Δ/match | SE | distinct opps | window |
|---|---|---|---|---|---|---|---|---|
| 20 | 22 | 110 | 0.636 | ±11.1pp | +1.02 | 1.35 | 12 | 08-06 03:32→07:02 |
| 53 | 46 | 230 | 0.530 | ±8.0pp | +1.09 | 1.49 | 16 | 08-06 21:02→08-07 04:32 |
| 68 | 19 | 95 | 0.453 | ±12.4pp | −1.51 | 2.30 | 12 | 08-07 17:12→20:12 |
| 72 | 27 | 135 | 0.474 | ±10.4pp | +0.68 | 1.58 | 14 | 08-08 00:02→04:22 |
| 80 | 63 | 315 | 0.495 | ±6.8pp | −0.26 | 1.02 | 19 | 08-08 13:52→08-09 03:42 |
| 90 | 16 | 80 | 0.412 | ±13.3pp | −2.79 | 2.46 | 10 | 08-09 05:42→08:12 |
| 91 | 17 | 85 | 0.506 | ±13.1pp | +0.06 | 2.79 | 13 | 08-09 08:22→11:02 |
| 92 | 16 | 80 | 0.562 | ±13.4pp | +2.15 | 1.74 | 12 | 08-09 11:12→13:42 |
| 94 | 28 | 140 | 0.507 | ±10.2pp | +0.44 | 1.70 | 11 | 08-09 13:52→18:22 |
| 102 | 78 | 390 | 0.508 | ±6.1pp | +0.42 | 0.79 | 20 | 08-09 18:42→08-10 12:32 |
| **104** | **102** | **510** | 0.524 | ±5.4pp | +0.67 | 0.75 | 21 | 08-10 07:22→08-11 13:12 |
| 112 | 18 | 90 | 0.556 | ±12.7pp | +1.51 | 1.99 | 11 | 08-11 13:32→19:12 |
| 114 | 41 | 205 | 0.468 | ±8.4pp | −0.70 | 1.07 | 15 | 08-11 19:32→08-12 08:52 |
| 115 | 15 | 75 | 0.493 | ±14.0pp | −0.12 | 1.50 | 9 | 08-12 09:12→13:52 |
| 116 | 42 | 210 | 0.495 | ±8.4pp | −0.59 | 1.23 | 17 | 08-12 14:12→08-13 04:32 |
| 125 | 61 | 305 | 0.557 | ±6.9pp | +2.24 | 0.96 | 18 | 08-13 10:32→08-14 07:52 |
| 140 | 18 | 90 | 0.622 | ±12.4pp | +3.76 | 1.71 | 10 | 08-14 11:52→18:52 |

**Versions relevant to the screens but TOO THIN TO USE** (stated explicitly, per
the brief):

| ver | matches | games | share | 95% hw | mean Elo Δ | verdict |
|---|---|---|---|---|---|---|
| 123 | 13 | 65 | 0.646 | ±15.1pp | +3.94 | marginal |
| 134 (x3r0) | 3 | 15 | 0.400 | ±31.4pp | −3.84 | **unusable** |
| 139 | 8 | 40 | 0.350 | ±18.3pp | −4.37 | **thin — the best loser we have** |
| 142 (x3r0) | 2 | 10 | 0.600 | ±37.5pp | −0.18 | **unusable** |
| 143 (x3r0) | 2 | 10 | 0.600 | ±37.5pp | +1.02 | **unusable** |
| 141 (x3r0) | 0 | 0 | — | — | — | **never played rated** |
| 145 (x3r0) | 0 | 0 | — | — | — | **0 rows in corpus** (held slot 19:08:37Z→19:17:14Z, after the corpus cut at 18:52:59Z; a live-CLI read reported one rated pairing at −10.0 Elo — **not verified by me**, not in `ladder_games.tsv`) |

**DEFF enumeration, performed rather than asserted** (the CLAUDE.md procedure):
1. Clusters present: **MATCH** and **OPPONENT**.
2. MATCH — can a per-version stratum hold >1 member of a match cluster? **Yes**:
   every match contributes 5 games to exactly one version (984/984 matches are
   5 games, verified). Cluster survives.
3. OPPONENT — can it hold >1 match against the same opponent? **Yes**: v140 has
   18 matches over 10 distinct opponents (m̄ = 1.8); v104 has 102 over 21.
   Cluster survives.
   ⇒ **Both live ⇒ pooled rated DEFF = 1.529** is the right constant here.
   Local screens use **0.98** (s39 balanced-by-construction audit); the platform
   constants are never applied to local rows.
4. **Direction check.** My central claims are FAIL-TO-EXCLUDE ("the field cannot
   separate these versions"), which DEFF makes *easier*. Restated as exclusion
   and reported both ways in §4: every "unresolved" verdict below is unresolved
   **under the naive DEFF = 1 interval as well**, so no conclusion here is an
   artefact of the widening. Only the one RESOLVED pair (v140/v139) is affected,
   and the correction makes it *harder*, which is the conservative direction.

### 2b. THE FINDING THAT BREAKS THE STUDY: the field cannot rank our own versions

Variance decomposition of per-version **mean Elo delta per match**, restricted to
versions with ≥ MIN rated matches (`observed variance of the version means`
minus `expected variance from within-version sampling`):

| MIN matches | k versions | obs var of means | noise var | **true var** | true SD | within-version SD |
|---|---|---|---|---|---|---|
| 8 | 33 | 7.064 | 4.688 | +2.376 | **1.54** | 8.15 |
| 15 | 17 | 2.296 | 2.499 | **−0.203** | **0.00** | 8.04 |
| 20 | 10 | 0.769 | 1.500 | **−0.731** | **0.00** | 7.86 |
| 40 | 7 | 1.092 | 1.092 | **−0.000** | **0.00** | 7.83 |

ANOVA on the same cuts:

| cut | k | N matches | F | p |
|---|---|---|---|---|
| all eras, ≥15 matches | 17 | 629 | F(16,612) = 0.840 | **0.640** |
| era ≥ 2026-08-09, ≥10 matches | 14 | 488 | F(13,474) = 1.182 | 0.289 |
| era ≥ 2026-08-11, ≥8 matches | 9 | 256 | F(8,247) = 1.909 | **0.059** |

**Read this carefully, both ways.** The ≥15-match cut says the versions we grant
real tenure are field-indistinguishable. The ≥8-match recent cut is *suggestive*
(p = 0.059) but is exactly the cut where thin tenures (v139 at 8, v123 at 13)
carry the spread — and thin tenures are the ones most exposed to opponent-mix
and era confounds, since a 8-match tenure samples ~7 opponents from a churning
pool. **The positive true-SD at MIN=8 (1.54 Elo/match) is therefore an UPPER
BOUND on real version-to-version field signal, not an estimate of it.**

**Consequence for the whole question:** the criterion variable is noise-dominated
at our tenure lengths. Even a perfectly valid screen would show near-zero
correlation against it. **Any future concordance study must fix the field side
first.**

---

## 3. THE SCREEN INVENTORY (the hard half)

Exhaustive hunt across `scratchpad/`, `docs/research/`, `docs/prereg/`,
`docs/coordination.md` (grepped, never read whole), `results.tsv` and
`git log --all`. **Every local head-to-head between two bots that each held the
platform slot, with source path and n:**

| # | screen | arm A (tree = version) | arm B | A's share | n | fixture | status | source |
|---|---|---|---|---|---|---|---|---|
| S1 | **SEALREPAIR** | `_v223sealrepair` = **v140** | `_v218mapfix` = **v139** | **59.26%** (per-row 59.30 excl. 4 NOWINNER) | **5,400** | local | verdict | `results.tsv:365`; gate read 59.85%@2,717 at `results.tsv:348` |
| S1r | **SEALREPAIRR** | same | same | **56.77%** (3062/5394) | 5,394 | remote work-server-1 | verdict | `results.tsv:367` |
| S2 | **V140VS142** | `_v223sealrepair` = **v140** | `_x3r0v142` = **v142** | **56.80%** (568/1000) | 1,000 | remote | verdict, RULE FIRED | `docs/prereg/SCREEN-v140vs142-2026-08-14.md`; `results.tsv:360`; rows `scratchpad/overnight-remote/worker@work-server-1/V140VS142.tsv` |
| S2c | V140VS142 local corroboration | same | same | 54.40% | 1,000 | local | note (not the decision surface) | `results.tsv:364`; `scratchpad/overnight/V140VS142.tsv` |
| S3 | **V140VS143** | `_v223sealrepair` = **v140** | `_x3r0v143` = **v143** | **57.06%** (570/999) | 999 | remote | verdict, RULE FIRED | `docs/prereg/SCREEN-v140vs143-2026-08-14.md`; `results.tsv:366` |
| S4 | **V141VS140** | `_x3r0v141` = **v141** | `_v223sealrepair` = v140 | 46.37% for v141 (⇒ 53.63% v140) | 1,005 | local | futility-stopped per own prereg | `docs/prereg/SCREEN-v141vs140-2026-08-14.md`; `results.tsv:351`; overrun pooled 45.78%@1,837 |
| S5 | **X3R0V134** | `_x3r0_v134` = **v134** | `_v197mapcode` = **v125** | **53.05%** for v134 (gate read 53.71%@1,024) | 1,116 | local | allocation-cancelled, informational | `docs/prereg/SCREEN-x3r0v134-2026-08-14.md`; `scratchpad/overnight/X3R0V134.tsv` |
| S6 | **V140VS145** | v140 | `_x3r0v145` = **v145** | 50.6% at 160/1000 | in flight | remote | **NOT DECIDED** | `docs/prereg/SCREEN-v140vs145-2026-08-14.md` = `scratchpad/_lockedv145.md` |
| S7 | battery-n1024 **ferry-first** | `_v148ferryfirst` = **v112** | `_v130loki13` = **v104** | 50.59% (518/1024) | 1,024 | local | **NO INFORMATION** (band ≤480 / ≥543) | `results.tsv:332` |
| S8 | battery-n1024 **gunner-axis** | `_v146gunaxis` = **v114** | `_v130loki13` = **v104** | 50.39% (516/1024) | 1,024 | local | **NO INFORMATION** | `results.tsv:332` |

Tree↔version join from **`corpus/version_trees.tsv`** (71 lines; the deliberate
join file between `ladder_games.tsv.ourver` and `bots/_vNNN*`), cross-checked
against `docs/coordination.md:49482-49484`.

⚠ **S7/S8 caveat, NOT VERIFIED:** the `battery-n1024` arms are named identically
to the trees that later shipped as v112/v114, but I did **not** verify that the
shipped zips are byte-identical to the battery arms. Treat those two rows as
provisional.

⚠ **The screen's own reproducibility ceiling is wider than its nominal
interval, and this is measured twice.** Same comparison, two hosts:
SEALREPAIR local **59.30** vs remote **56.77** — delta 2.53pp against a joint
95% half-width of 1.87pp at n≈5,400 each, i.e. **real cross-fixture
heterogeneity (z ≈ 2.7), already flagged at `results.tsv:367`**; V140VS142
remote **56.80** vs local **54.40** — delta 2.40pp, inside joint noise at
n = 1,000 (±4.35pp) but the same magnitude and the **opposite** sign, so it is
fixture noise rather than a host bias.
⇒ **A screen bar set at 51.0% sits inside the fixture-to-fixture spread of the
instrument enforcing it.** At n = 1,000 the sampling interval alone is ±3.04pp,
so a reading of 51.0% has 95% CI [47.96, 54.04] — **the bar does not exclude
50.0%.** The three firings that actually happened (56.80, 57.06, 59.26) cleared
it with room; the point is that the rule as written would also fire on a
reading that carries no information.

---

## 4. THE JOIN — concordance, with m stated honestly

For each pair: does the screen's winner also have the better rated field record?

| # | pair | screen verdict | field share diff (DEFF 1.529) | naive (DEFF 1) | field Elo Δ/match diff | sign concordant? |
|---|---|---|---|---|---|---|
| **P1** | **v140 vs v139** | **v140, 59.26%@5,400 — INFORMATIVE** | **+27.2pp, CI [+4.2, +50.2] — RESOLVED** | [+8.6, +45.8] | **+8.13, CI [+1.40, +14.85] — RESOLVED** | ✅ **YES** |
| P2 | v140 vs v142 | v140, 56.80%@1,000 — informative | +2.2pp, CI [−38.2, +42.6] — unresolved | [−30.4, +34.9] | +3.95, CI [−2.69, +10.58] — unresolved | ✅ sign only |
| P3 | v140 vs v143 | v140, 57.06%@999 — informative | +2.2pp, CI [−38.2, +42.6] — unresolved | [−30.4, +34.9] | +2.74, CI [−0.81, +6.29] — unresolved | ✅ sign only |
| P4 | v134 vs v125 | **v134**, 53.05%@1,116, CI [50.2, 56.0] — informative | −15.7pp, CI [−47.8, +16.3] — unresolved | [−41.7, +10.2] | −6.08, CI [−14.59, +2.43] — unresolved | ❌ **DISCORDANT (sign)** |
| P5 | v141 vs v140 | v140, 53.63%@1,005 — informative | **v141 has 0 rated games** | — | — | **UNUSABLE** |
| P6 | v140 vs v145 | in flight | **v145 has 0 rows in the corpus** | — | — | **UNUSABLE** |
| P7 | v112 vs v104 | **NO INFORMATION** (50.59%) | +3.2pp, CI [−10.7, +17.1] — unresolved | [−8.0, +14.4] | +0.84, CI [−3.34, +5.01] | ✅ sign only, but the screen made no claim |
| P8 | v114 vs v104 | **NO INFORMATION** (50.39%) | −5.5pp, CI [−15.5, +4.5] — unresolved | [−13.6, +2.6] | −1.37, CI [−3.94, +1.19] | ❌ sign only, but the screen made no claim |

### THE COUNT, at three levels of strictness

* **STRICT — informative screen AND a field difference that is statistically
  resolved: k = 1 of m = 1.** One data point. **The question is unanswerable.**
* **SIGN — informative screen, both arms have ≥1 rated match, sign agreement
  only: k = 3 of m = 4.** Exact two-sided binomial p vs a coin = **0.625**.
  **This is consistent with a screen of zero predictive validity and equally
  consistent with a perfect one.** It must not be quoted as support.
* **ALL PAIRS including the two NO-INFORMATION screens: k = 4 of m = 6.**
  Meaningless — a screen that returned "no information" has no winner to be
  concordant with, and including it manufactures denominators.

**m = 4 (or 1). Say it plainly: our history cannot answer whether local
head-to-head screens predict field earnings.** The single resolved pair
(P1, v140/v139) is a genuine point in the screen's favour and should be recorded
as such; it is one observation.

**And note where the discordance is.** The one sign-discordant informative pair
(P4) is the one where the screened winner was a **teammate-authored bot built on
a different chassis** — precisely the non-transitive geometry the brief worries
about. Its field side is 15 games, so it proves nothing; but if a non-transitivity
signal exists in our data, that is where it would be, and it is the direction of
the concern rather than against it. **Inference, not measurement.**

### The confound that would remain even with more data

Every field record above is against a **different opponent mix over a different
era**. v140's 18 matches drew 10 opponents between 11:52Z and 18:52Z with our
rating climbing 1724 → 1795; v139's 8 drew 7 opponents between 09:12Z and 11:32Z
falling 1759 → 1734. The Elo-delta metric absorbs opponent **rating** but not
opponent **identity** — and identity is exactly what non-transitivity acts
through. **A field comparison between two versions that never faced the same
opponent set is confounded by construction**, and no version pair in our history
has a matched opponent set.

---

## 5. PIVOT — what a screen's number *predicts*, and what it would take to test it

**I am pivoting here, as instructed, because m is too small.** The rest of this
document is a specification for a measurement we cannot currently make.

### 5a. Restate the screen as a falsifiable field prediction

A head-to-head share `p` implies, **under transitivity**, an Elo gap of
`400 * log10(p / (1-p))`. This is the transitive prediction the screen is
implicitly making, and it is testable:

| screen | share @ n | implied Elo gap | 95% CI |
|---|---|---|---|
| SEALREPAIR v140/v139 | 59.26% @ 5,400 | **+65.1** | [+55.8, +74.5] |
| SEALREPAIRR (remote) | 56.77% @ 5,394 | +47.3 | [+38.1, +56.6] |
| V140VS142 | 56.80% @ 1,000 | +47.5 | [+26.2, +69.3] |
| V140VS143 | 57.06% @ 999 | +49.4 | [+28.0, +71.2] |
| V141VS140 (v140 side) | 53.63% @ 1,005 | +25.3 | [+4.0, +46.7] |
| X3R0V134 (v134 side) | 53.05% @ 1,116 | +21.2 | [+1.1, +41.5] |
| ferry-first v112/v104 | 50.59% @ 1,024 | +4.1 | [−17.0, +25.2] |
| gunner-axis v114/v104 | 50.39% @ 1,024 | +2.7 | [−18.4, +23.8] |

Two things fall out immediately.
1. **The two cross-host reads of the SAME comparison imply +65.1 and +47.3 Elo —
   an 18-point disagreement with non-overlapping intervals.** Whatever the screen
   predicts, it does not predict it to better than ~±18 Elo across fixtures.
2. **The 51.0% bar corresponds to a +7.0 Elo prediction.** For scale, one rated
   match is worth up to ±16 Elo. **The rule as codified fires on an effect
   smaller than the noise in a single rated match.**

### 5b. How big is the field effect we would need to detect, and what it costs

Two-arm 95% MDE, rated surface, DEFF = 1.529, at 72 rated matches/day:

| target MDE on game share | games/arm | matches/arm | days of exclusive tenure per arm |
|---|---|---|---|
| 10.0 pp | 294 | 59 | 0.8 |
| 5.0 pp | 1,175 | 235 | **3.3** |
| 3.0 pp | 3,263 | 653 | **9.1** |
| 2.0 pp | 7,342 | 1,468 | **20.4** |

On the Elo-delta metric (within-version SD = 8.0/match):

| target MDE (Elo/match) | matches/arm | days |
|---|---|---|
| 5 | 20 | 0.3 |
| 3 | 55 | 0.8 |
| 2 | 123 | 1.7 |
| 1 | 492 | 6.8 |

**Set against §2b's upper bound on real version-to-version field signal
(true SD ≤ 1.54 Elo/match), a typical pair differs by ~2.2 Elo/match. That needs
~123 matches per arm — 1.7 days of exclusive slot tenure EACH.** Our median
tenure is far below that: five ship decisions in the last 36 hours, v122
displaced at k=4, v139 at k=8, v142/v143 at k=2. **The ladder will never deliver
this.** Buying it would mean freezing the slot for ~3.5 days to compare one pair,
which is a worse use of the slot than shipping.

### 5c. THE SPECIFICATION — what to start recording NOW to answer this in two weeks

Three items, in priority order. Item 2 is the one that unblocks the study.

**1. A SCREEN REGISTRY WITH BOTH ARMS' PLATFORM IDENTITY (cheap, do today).**
`results.tsv` records a screen's share and n in free text; the arms are local
tree names, and `corpus/version_trees.tsv` only seeds *our* ships — x3r0's
v134/v141/v142/v143/v145 have **no entry**, and v105-111/113/117-119 are known
real submissions with no recorded tree at all (the ledger says so itself:
"absence means unknown, not guessed"). I reconstructed this join by grepping
`docs/coordination.md`, which is not a method that survives. **Add a
machine-readable row per screen: `screen_id, tree_a, ver_a, tree_b, ver_b, share_a,
n, fixture_host, implied_elo_gap, decided_at, rule_fired`** — and extend
`version_trees.tsv` to cover teammate submissions and non-shipped candidates.
Without `ver_a`/`ver_b` on both sides, **no future join can be built
retroactively, no matter how much field data accumulates.**

**2. ⭐ A MATCHED UNRATED FIELD PANEL FOR *BOTH* ARMS OF EVERY SCREEN. This is
the missing instrument, and it is the answer to "what are we failing to
record".** The ladder structurally cannot supply a field read for the losing arm
— the slot holds one bot, so the loser's tenure is whatever survived before
displacement (0, 2, 3 and 8 matches in the four cases above). But the field read
does not have to come from the ladder. `fcode match unrated <team> --match
<past_match_id>` plays a **pinned** opponent submission; unrated games are free
(5 per 20 min shared across `unrated`+`test`, ~75 games/hour) and cost zero
rating. **Spec:** a fixed six-opponent panel drawn from the versions the pairer
actually gives us, **pinned per opponent so both arms meet the identical
fixture**, ≥25 games per cell per arm = 150 games/arm ≈ 2 hours of window per
arm. That yields a two-arm 95% MDE of ~13pp on the *unrated* surface
(DEFF 1.833) — coarse, but it is a **matched** comparison against a **pool**,
which is the quantity the screen claims to predict, and it is obtainable for
**both** arms including the one that never held the slot.
**Correlate `screen_share` against `panel_share_A − panel_share_B` across
screens.** At the current rate of ~3 screens/day, two weeks yields ~40 paired
observations — enough to resolve a correlation of 0.4 or larger.
*(Amendment note: `PROGRAMME.md`'s existing rule says calibration panels must
NOT be pinned, because a panel measures RELEVANCE and pinning reintroduces
staleness. That rule is right for a calibration panel and wrong for this one:
this is a matched-pair **treatment** panel and pinning is mandatory. The two
must be registered as different instruments with different names, or the next
reader will apply the wrong rule to one of them.)*

**3. RECORD THE IMPLIED ELO GAP IN EVERY PREREG, BEFORE THE FIELD READ.**
One line: `IMPLIED TRANSITIVE GAP: +XX.X Elo (95% CI [a, b]) from share p @ n`.
This converts concordance from a **sign** question (1 bit per pair, needs ~30
pairs) into a **magnitude** question (a regression slope, informative from ~10),
and it makes the screen's prediction refutable rather than merely directional.
The natural pre-registered null is **slope = 1** (perfect transitivity) against
**slope = 0** (screen predicts nothing).

**One thing NOT to do:** do not fix this by lengthening slot tenure. §5b prices
that at ~3.5 days of frozen slot per pair, and `R1000_IS_DEFEAT`-era throughput
is worth more than the coefficient.

---

## 6. WHAT THIS CUT DOES AND DOES NOT LICENSE

**Does NOT license** — under `point 6` (a refutation needs live-game backing),
nothing here retires the screen or the `X3R0_SLOT_RULE`. This is a corpus
statistic about our own history; it may **prioritise** the road, it may not
**close** it. The rule has fired three times and the one pair with a resolved
field difference (P1) supports it.

**DOES license, and these are stated as claims about the instrument, not the
bot:**
1. **The 51.0% bar is not a resolvable threshold at n = 1,000.** Sampling
   interval ±3.04pp; cross-fixture reproducibility ±~2.5pp on top. A reading of
   exactly 51.0% is indistinguishable from 50.0%. **The bar should be restated
   as an interval condition** — e.g. *the 95% CI must exclude 50.0%*, which at
   n = 1,000 means a reading ≥ 53.1%. The three firings to date all clear that
   stricter form, so adopting it costs nothing retrospectively.
2. **`PROGRAMME.md`'s screen rule currently rests on m = 1.** That should be
   written down beside the rule, not left implicit.
3. **Any claim of the form "version X earns more on the ladder than version Y"
   at our typical tenure (k ≤ 20 matches) is unsupported.** §2b: the field cannot
   separate our own versions. This affects rows already on the tape — e.g.
   `v140-era-close` (k = 8, "net_act +31.8") and `k8-look-v123` / `k8-look-v125`
   (both explicitly self-labelled "only a disaster was detectable"). Those three
   already carry the caveat; the standing form should be that **every k ≤ 20
   rated read carries it.**

---

*Instrument note, per the standing rule that anything published is an
instrument. Every guard below was RUN, and each was driven to the other verdict:*

* *`E` at equal ratings returns **0.5 exactly**, and `delta` at S = 0.5 returns
  **0.0 exactly**.*
* *Seat-swap antisymmetry: `delta(S=0.8, 1750, 1600) = +3.09168` and
  `delta(S=0.2, 1600, 1750) = −3.09168`, sum **0.0** to 10 decimal places.*
* *Forced-fail control on the same expression — flipping the sign inside the
  `E` exponent returns **+16.1083** instead of +3.09168, so the rating term is
  demonstrably load-bearing and not an inert constant.*
* *Grouping assumptions were TESTED, not assumed: 984/984 matches have exactly
  5 games and a constant `ourbef`. **Forced-fail: corrupting a single row's
  `ourbef` flips that check to False**, so the check can produce the other
  verdict.*
* *The field side of every concordance row was recomputed from raw game rows;
  the stored `eloDelta` column was never read.*
