# THE FIELDCAL READER — BUILT AT n=225 SO THE 800-BOUNDARY READ IS A RE-RUN, NOT A BUILD

**Research arm, s46, read-only. Written 2026-08-16T09:3xZ (`date -u`, same shell call as every
number below).** Instrument: `tools/fieldcal_read.py` (new, this document's subject).
**The leg is LIVE and unattended. Nothing here fired, edited, activated, or touched the scheduler.**

---

## 0. ⛔⛔ THE CLAUSE THAT GOVERNS EVERY SENTENCE IN THIS DOCUMENT

`docs/prereg/LEG-fieldcal-2026-08-16.md` §1 `CUT-SHORT`, verbatim:

> **800 games total (40 games per arm in every surviving cell) is the floor for any comparative
> claim. Below it: counts only, descriptive, no sign test, no reversal claim.**

**The leg holds 225 leg-arm games. 225 < 800.** ⇒ This document reports **COUNTS AND DESCRIPTIVE
STATISTICS ONLY.** No sign test is run. No treatment-vs-control difference is computed, stated,
implied, or placed where one could be read off. There is no "trending", no "on track", no
"consistent with".

⚠ **AND THE FALSIFIER TRAP, which has already fooled one reader today.** §5's `−7.7 pp` is a **95%
HALF-WIDTH AT 600 GAMES/ARM**, not a point threshold you can hold a small number up against; and it
is registered over the **POOLED** reading, so **a SINGLE CELL is a DIFFERENT STATISTIC and cannot
fire it at ANY n.** No number in this document is printed beside those thresholds.

---

## 1. WHAT THE PREREG REGISTERS, AND WHICH SECTION REGISTERS IT

Read in full before a line of code was written. The reader implements these, not reasonable-looking
substitutes.

| # | registered thing | §  | verbatim shape |
|---|---|---|---|
| PRIMARY | exact two-sided binomial **sign test over the 10 pinned opponent cells** on `sign(game_share_T − game_share_C)`; `+` iff treatment share **strictly** exceeds control, `−` iff strictly less, **TIE iff exactly equal — ties EXCLUDED, test recomputed at reduced k, tie count reported** | §1 ESTIMATOR, §4 | unit of analysis is the **CELL (k=10)** |
| SECONDARY | pooled **ITT RMST at H=300** = the mean over ALL games of `min(turns, 300)`, **"with any game not ending in our core-kill scoring the full 300"**. **Mean, not median** (the ITT median pins at the horizon). Boundary convention **`<300`** | §1 ESTIMATOR, §9.8 | no post-hoc horizon shopping; H=250/H=400 are pre-declared sensitivity columns only |
| BAR | **≥9/10** cells share the sign ⇒ MEET (exact two-sided p = **0.0215**); exactly **8/10** ⇒ **UNRESOLVED** (p = 0.1094); **≤7/10** ⇒ MISS, which the IMPOTENCE CLAUSE registers as the **EXPECTED** outcome and **not a refutation** | §1 BAR, §1 IMPOTENCE, §4, §7 | power against the local effect is **7.0% / 9.9%** |
| FALSIFIER | pooled game share (T−C) **≤ −7.7 pp**, or pooled ITT RMST₃₀₀ (T−C) **≥ +10.1 rounds** | §5 | **POOLED only**; the values are the half-widths at 600 games/arm |
| CLUSTER UNIT | match+opponent (pooled) for the pooled reads. ⭐ **The PRIMARY takes NO design effect at all** — its unit IS the cluster, so the exact binomial over 10 independent cells governs and a DEFF there is double-counting | §1 CLUSTER UNIT | |
| DEFF | **re-measure on the leg's own games, df-corrected**; planning values (1.833 share / 1.42 RMST) appear in **no banked interval** | §3 | quote re-measured beside planning |
| CELL EXCLUSION | a cell that does not reach **40 games per arm** is **EXCLUDED from the primary and NAMED WITH ITS COUNTS**; sign test recomputed at surviving k; **at k < 8 the primary is UNRESOLVED and defaults to the restriction** | §1 CUT-SHORT, §7 | |
| VOIDING | for **every** accepted match the decoded `oppver` must equal the registered `theirver`. **A mismatch VOIDS THAT CELL — it is not noted, it is removed**, k reduced, p recomputed | §9.3 | load-bearing: the `UNPINNED_OK` guard catches an EMPTY pin, never a WRONG one |
| ARM IDENTITY | engine-side / actor-side facts **only** — platform replays strip `stdout` (30,664/30,664) | §9.1 | |
| FRESHNESS | absence in the archive is **not evidence**; quote the age of the newest row | §9.5 | |
| IMBALANCE | one heading, all axes: seat, map, pin age, window, per-cell accepts. **Disclose, do not correct** | §6.2 | |

**Amendment 1** (`AMENDMENT-LEG-fieldcal-catchup-2026-08-16.md`) adds a zero-accept catch-up rule to
the SCHEDULER and its §2 table confirms **every estimator, bar, horizon, cell, pin and falsifier is
UNTOUCHED.** Nothing in the reader changes because of it.

---

## 2. WHAT THE READER IMPLEMENTS — `tools/fieldcal_read.py`

**Arm identification, derived rather than assumed (§9.1).** The authoritative map is
`scratchpad/arm_fieldcal_<arm>_<cell>.txt`, the consolidated accept ledger that
`tools/fieldcal_scheduler.sh:invoke_runner` appends every accepted challenge to (`cat "$outfile" >>
"$consolidated"`). Each accept line carries the platform's `{"matchId": ...}`, so **match id →
(arm, cell) comes from the actor side, never from our own printed output.** Arms are
`A = v140 = bots/_v223sealrepair` (CONTROL) and `B = v154 = bots/_v242bodyaware` (TREATMENT,
BODYAWR), per prereg §2 and `tools/fieldcal_scheduler.sh:137-138`.
**That mapping is then CROSS-CHECKED, not trusted:** every game's replay-meta `ourver` must equal
the ledger arm's registered version. Disagreement is an instrument alarm, reported before any
number.

**Leg era** = `createdAt >= CLOCK2` from `scratchpad/fieldcal_state.tsv`
(`2026-08-16T06:25:40.381Z`). ⛔ The state tape is cited and the scheduler log is not: that log was
**truncated at 07:40:13Z** by a nohup relaunch using `>` instead of `>>`.

**RMST₃₀₀** is implemented from the prereg's own words: `min(turns, 300)` **iff the game ended in
OUR core-kill** (`cond == core_destroyed` AND `won == 1`), **otherwise the full 300.** See §5 — this
is the one place the registered definition and a natural paraphrase come apart, and it is worth 60
rounds of level.

**Game share** = games won / games played (the ladder pays game share, not match wins).

**§1 cell exclusion, §9.3 voiding, §3 DEFF re-measurement (df-corrected, both clusters),
§6.2 imbalance, §9.5 freshness** are each implemented as named blocks in the output.

### 2.1 ⭐ THE REFUSAL IS A FEATURE OF THE TOOL, NOT A CAVEAT IN ITS OUTPUT

Two rules, and the second is the one that took a peer-lane correction to get right.

1. **Below 800 leg-arm games the reader emits NO (T−C) figure at all** — not greyed, not
   parenthesised, **absent** — and prints
   `⛔ BELOW CUT-SHORT FLOOR: 225/800 — NO COMPARATIVE CLAIM PERMITTED AT THIS n (prereg §1)`
   plus §1 verbatim. The primary/secondary/falsifier block prints `NOT COMPUTED`.
2. **Every per-cell line carries its refusal INLINE, on the same physical line**, and the refusal is
   **CATEGORICAL, not a precision argument**:
   `— CELL, NOT THE POOLED STATISTIC: A CELL NEVER FIRES THE FALSIFIER, AT ANY n (§5 is registered
   over the POOLED reading) — NO COMPARATIVE CLAIM`
   **The mechanism this defends against is real and cost us this morning: a number printed with its
   qualifier ELSEWHERE ON THE PAGE gets quoted WITHOUT the qualifier.** Headers, preambles and
   footers all detach under copy-paste. The only qualifier that survives is one on the number's own
   line. And the wording must be categorical, because a precision phrasing invites *"then at what n
   would a cell count?"* — and for a cell the honest answer is **never**.

Per-arm pooled figures are likewise printed with both arms on one line, each line carrying the
below-floor tag inline, for the same reason.

---

## 3. THE DRIVEN CONTROLS — EXPECTED VS OBSERVED, ALL FOURTEEN

**Every expectation below was written before the cell was run.** `--selftest` runs them all; the
harness is `tools/fieldcal_read.py:selftest()`. **A guard that has only ever returned one verdict
has not been seen to guard**, so each is driven to BOTH verdicts.

| # | control | expected | observed | |
|---|---|---|---|---|
| a | floor refusal **FIRES** on a synthetic n=400 | refusal printed, primary/secondary/falsifier `NOT COMPUTED`, no (T−C) value anywhere | `above_floor=False`, refusal present, `NOT COMPUTED` present | ✅ |
| b | floor refusal does **NOT** fire on a synthetic n=1200 | floor CLEARED, sign test run, 2 pooled (T−C) lines present and **free of any refusal string** | `above_floor=True`, 2 pooled lines, clean | ✅ |
| c | ⭐ **the categorical cell rule** at 60 games/arm/cell (600/arm — above every n threshold in the leg) | all 10 per-cell lines **STILL** carry the inline refusal | 10 cell lines, 10 carrying it | ✅ |
| d1 | RMST₃₀₀ unit check, hand-computable | turns 100/400/300 (all our kills) → 100/300/300, **mean 233.33** | scores `[100, 300, 300]`, mean 233.33 | ✅ |
| d2 | the registered "our core-kill" clause, driven the other way | a game the OPPONENT ends at turn 120 scores **300** registered / **120** loose | registered 300, loose 120 | ✅ |
| e1-3 | corrupt/absent/zero `turns` is **REFUSED** | `Refusal` raised for `''`, `'N/A'`, `'0'` | raised on all three | ✅ |
| e4 | ...and a valid `turns` is **not** refused | 210 scored, no refusal | 210 scored | ✅ |
| e5 | a surface **missing the `turns` column** is refused | `Refusal` raised | raised | ✅ |
| f | §9.3 pin mismatch **VOIDS** a cell — and is clean when pins hold | `voided=['Erebus']`, admitted k drops to 9; control run `voided=[]` | exactly that | ✅ |
| g | arm cross-check alarms on a ledger/`ourver` disagreement | 1 alarm on the corrupted row, 0 on the clean run | 1 / 0 | ✅ |
| h | §1 cell exclusion names the thin cell | Juusto (20/arm) EXCLUDED **and named with its count**; Erebus (60/arm) ADMITTED | exactly that | ✅ |
| i | exact two-sided binomial reproduces §4's own table | 10/10 → 0.0020, 9/10 → 0.0215, 8/10 → 0.1094 | 0.0020, 0.0215, 0.1094 | ✅ |

**`SELFTEST: OK — every guard driven to both verdicts`.**

⚠ **Cell (c) is the one that proves the categorical rule rather than a threshold on n**, and it is
the cell that would have failed a naive implementation: at 600 games/arm every sample-size objection
to a cell figure has evaporated, and the refusal must still be there because the mismatch is between
a **cell** and a **pooled** statistic, not between a small n and a large one.

**Why `turns == 0` is a refusal and not a value:** a row that cannot be scored **cannot be dropped**
without moving the ITT denominator, and **cannot be zeroed** without inventing an instant kill. Both
errors move the registered secondary in the FLATTERING direction for a fast arm.

---

## 4. TODAY'S DESCRIPTIVE OUTPUT — COUNTS ONLY

Read `2026-08-16T09:37:00Z`. State tape `ROUND=11`, age 3.2 min. **Newest corpus row
`2026-08-16T09:19:15.731Z`** — ⚠ §9.5, the archive lags and absence is not evidence.

    ⛔ BELOW CUT-SHORT FLOOR: 225/800 — NO COMPARATIVE CLAIM PERMITTED AT THIS n (prereg §1)
    ⚠ TWO CONDITIONS, NOT ONE: 225/800 games AND 0/8 cells at >=40 games/arm.

**Instrument checks, all clean:** arm cross-check CLEAN (0 ledger/`ourver` disagreements);
**§9.3 pin assertion CLEAN on every one of the 45 accepted matches** — decoded `oppver` equals the
registered `theirver` in all five fired cells (Juusto v13, not adgato v23, Erebus v119, kladde v119,
gsxWins v46); **no cell is voided.**

**Leg-era rows NOT in this leg's ledger — 35 games, excluded from every number:**
`ourver=v125 vs Hugging Farce` 30 games and `ourver=v152 vs 0033` 5 games. Neither is a leg arm.
*(Characterisation, not a check: the Hugging Farce rows are that team's own inbound campaign — §9.6
records it — and the `v125` tag is consistent with them pinning us to a past match, which plays the
submission we held then. Unverified and not load-bearing; what matters is that the ledger excludes
them by construction rather than by a name filter.)*

**PER-ARM DESCRIPTIVE** — below CUT-SHORT floor, no comparative claim permitted at this n:

| arm | | n | accepts | game share | ITT RMST₃₀₀ | our-core-kills | by r300 |
|---|---|---:|---:|---:|---:|---:|---:|
| A | CONTROL v140 | 125 | 25 | 42.4% | 249.52 | 53 | 47 |
| B | TREATMENT v154 | 100 | 20 | 46.0% | 256.11 | 46 | 39 |

ITT denominator check: every game scores exactly once; games not ending in our core-kill score the
full 300 (A: 72, B: 54).

**PER-CELL FILL** — each of these lines carries the categorical cell refusal inline in the tool's
own output; reproduced here in full so the numbers never travel without it:

```
Juusto      A 44.0% (25g) RMST 264.20 | B 36.0% (25g) RMST 266.32 | EXCLUDED (min 25 < 40/arm)  — CELL, NEVER FIRES THE FALSIFIER AT ANY n — NO COMPARATIVE CLAIM
not_adgato  A 48.0% (25g) RMST 236.68 | B 32.0% (25g) RMST 282.84 | EXCLUDED (min 25 < 40/arm)  — CELL, NEVER FIRES THE FALSIFIER AT ANY n — NO COMPARATIVE CLAIM
Erebus      A 52.0% (25g) RMST 227.28 | B 68.0% (25g) RMST 225.08 | EXCLUDED (min 25 < 40/arm)  — CELL, NEVER FIRES THE FALSIFIER AT ANY n — NO COMPARATIVE CLAIM
kladde      A 32.0% (25g) RMST 255.24 | B 48.0% (25g) RMST 250.20 | EXCLUDED (min 25 < 40/arm)  — CELL, NEVER FIRES THE FALSIFIER AT ANY n — NO COMPARATIVE CLAIM
gsxWins     A 36.0% (25g) RMST 264.20 | B  n/a  ( 0g) RMST    n/a | EXCLUDED (min  0 < 40/arm)  — CELL, NEVER FIRES THE FALSIFIER AT ANY n — NO COMPARATIVE CLAIM
0033 · lingling_40h · HTTP_418 · The_Bisons · farming_200s   UNFIRED — 0 games either arm
```

⚠ **Erebus and kladde are the two §1 HIGH-CHURN cells (10 and 17 distinct opponent versions in the
preceding 24 h) — REPORTABLE, NOT POOLABLE into any field-relevance claim.**

**§6.2 IMBALANCE, one heading, all axes.** Seat: arm A plays 60 A-seat / 65 B-seat, arm B plays
55 / 45. Accepts per cell (A/B): `Juusto 5/5 · not_adgato 5/5 · Erebus 5/5 · kladde 5/5 ·
gsxWins 5/0 · 0033 0/0 · lingling_40h 0/0 · HTTP_418 0/0 · The_Bisons 0/0 · farming_200s 0/0`.
**`gsxWins` is the live 5/0 asymmetry** and is exactly the shape Amendment 1's catch-up rule
addresses. Pin age: `farming_200s`' pin was ~16 h old at lock (unfired so far).

**§3 DEFF, RE-MEASURED ON THE LEG'S OWN GAMES, df-corrected — PROVISIONAL, USED IN NO INTERVAL AT
THIS n** (dispersion is descriptive here and does not become a comparative interval):

| arm | statistic | cluster | k | m | **DEFF** | ρ | planning |
|---|---|---|---:|---:|---:|---:|---:|
| A | game share | MATCH | 25 | 5.0 | **0.773** | −0.0569 | 1.833 |
| A | RMST₃₀₀ | MATCH | 25 | 5.0 | **0.841** | −0.0398 | 1.42 |
| B | game share | MATCH | 20 | 5.0 | **1.110** | +0.0276 | 1.833 |
| B | RMST₃₀₀ | MATCH | 20 | 5.0 | **1.335** | +0.0837 | 1.42 |

**These are 20-25 clusters and they are not a re-measurement yet** — they are the re-measurement
*machinery*, run early so that the §3 obligation at the 800 boundary is a re-run. **They must not be
quoted as the leg's DEFF**, and no interval anywhere uses them.

---

## 5. ⛔ WHERE THE REGISTERED DEFINITION AND A NATURAL PARAPHRASE COME APART — THE MOST VALUABLE THING HERE, AND IT IS BETTER FOUND NOW THAN AT THE BOUNDARY

**§1 registers:** RMST₃₀₀ = the mean over ALL games of `min(turns, 300)` **"with any game not ending
in OUR CORE-KILL scoring the full 300."**

**The paraphrase that is easy to reach for:** *"a non-kill scores 300"* — i.e. score `min(turns,300)`
whenever `cond == core_destroyed`, regardless of **whose** core fell.

**These are different estimators, and they differ by ~60 rounds of level on today's rows:**

| reading | arm A | arm B |
|---|---:|---:|
| **REGISTERED** (`our` core-kill only) | **249.52** | **256.11** |
| loose (any core kill, either team's) | 189.64 | 214.56 |

**The registered reading is the correct one and it is not a close call**, because it is what the
LOCAL prior was computed under. `RMST-ESTIMATOR-2026-08-16.md` §3, retraction 1, in its own words:
*"RMST scores a LOSS as the full horizon, so converting a loss into a slow win is correctly an
IMPROVEMENT."* A loss is a game the opponent ended by killing OUR core — under the loose reading it
would score its own turn count, and that sentence would be false. The −6.84-round `BODYAWR` prior
this leg is aimed at is denominated in the registered form, so **a field read under the loose form
would not be comparable to the thing it is testing.**

⛔ **WHY THIS IS A HAZARD AND NOT A PEDANTRY: the §5 falsifier is a threshold of ±10.1 rounds on a
pooled difference, and the clause moves each arm's LEVEL by about 60 rounds.** An estimator that
swings six falsifier-widths on a paraphrase is one where the paraphrase can decide the verdict.
**No difference is computed here under either reading** — the point is about the instrument, not
about this leg's result — but it is exactly the substitution a reader arriving at the 800 boundary
in a hurry would make, and the tool now prints the two levels side by side under a `DEFINITION FLAG`
heading every run so the substitution cannot happen silently.

### 5.1 A SECOND STRUCTURAL FINDING: 800 GAMES DOES NOT BY ITSELF RESOLVE THE PRIMARY

§1's CUT-SHORT is **two conditions wearing one number**: *"800 games total (40 games per arm in
**every surviving cell**)"*. **Crossing 800 total satisfies the first and says nothing about the
second.** With the fill concentrated as it is today (five cells fired, five unfired, one arm of
`gsxWins` at zero), a leg truncated at exactly 800 could easily carry **fewer than 8 admitted
cells — at which point §1 makes the primary UNRESOLVED and §7 defaults it to the restriction.**
The reader now prints both conditions on the floor line (`225/800 games AND 0/8 cells at ≥40
games/arm`) so a successor cannot read the game count alone as a green light.
*(Arithmetically the two are jointly satisfiable — 8 cells × 40 × 2 arms = 640 of the 800 — so this
is a fill-BALANCE requirement, not a contradiction in the registration.)*

### 5.2 SMALLER NOTES, RECORDED SO THEY ARE NOT REDISCOVERED

* **`turns` exceeds the horizon regularly and correctly.** 39 of 249 leg-era `core_destroyed` games
  ran past r300 (max 842); `titanium_collected` games are all exactly 1000. `min(turns, 300)`
  censors these by design, which is what makes RMST a censored mean rather than a kill-time average.
* **The corpus surface is sound for this leg but is NOT a verdict surface on its own** — its own
  header says so, because unrated rows pool prototypes. Every read here slices by ledger arm, which
  is stricter than slicing by `ourver`.
* **`corpus/unrated_games.tsv` is rebuilt inside every `tools/corpus/sync.py` cycle**, so the reader
  needs no build step; it reports the newest row's timestamp every run instead of assuming currency.

---

## 6. WHAT THE READER WILL PRODUCE THE MOMENT 800 IS CROSSED

Unchanged code, one command — `.venv/bin/python tools/fieldcal_read.py`. The refusal lifts by
itself and the tool emits, in this order:

1. **PRIMARY (§1, §4):** the per-cell sign vector over the **admitted** cells (`+` / `−` / `TIE`),
   ties excluded with the count reported, `k` after exclusions and voidings, the **exact two-sided
   binomial p**, and the §1/§7 verdict word — `MEET` (≥9, p ≤ 0.0215) · `UNRESOLVED` (8, p = 0.1094,
   *and* any k < 8) · `MISS` (≤7, carrying the IMPOTENCE CLAUSE's sentence that this is the expected
   outcome and not a refutation).
2. **SECONDARY (§1):** pooled ITT RMST₃₀₀ (T−C) in rounds, with both arms' levels.
3. **DESCRIPTIVE (§6 row 4, §6.1):** pooled game share (T−C) in pp, labelled *descriptive only, no
   bar, no verdict, no ship input* on its own line.
4. **FALSIFIER (§5), pooled only:** each threshold evaluated `FIRED` / `not fired`, printed with the
   reminder that −7.7 pp and +10.1 rounds are the **half-widths at 600 games/arm** and with the
   leg's actual per-arm n beside them; plus §3's **direction rule** — a non-reversal is a
   fail-to-exclude and is banked as *"the leg excludes reversals larger than X"* off the leg's own
   re-measured DEFF, never as *"the local finding is confirmed"*.
5. **§3 DEFF**, re-measured and df-corrected, quoted beside the planning values, and used for the
   intervals in (4).
6. Everything in §4 above — the per-cell lines (**still carrying their categorical refusal**), the
   §6.2 imbalance heading, the §9.3/arm instrument checks, and the DEFINITION FLAG.

**The one thing the tool will still refuse above 800:** a comparative claim at cell level. That
refusal is categorical and has no n at which it lifts.

---

## PROVENANCE

`docs/prereg/LEG-fieldcal-2026-08-16.md` (read in full) · `docs/prereg/AMENDMENT-LEG-fieldcal-catchup-2026-08-16.md` ·
`docs/research/RMST-ESTIMATOR-2026-08-16.md` §2–§3, §6 · `corpus/unrated_games.tsv` (6,046 rows;
built by `tools/corpus/unrated_games.py`) · `scratchpad/fieldcal_state.tsv` (ROUND 11, CLOCK2
2026-08-16T06:25:40.381Z) · `scratchpad/arm_fieldcal_*.txt` (45 accepts) ·
`tools/fieldcal_scheduler.sh:105,137-138` (cell order, arm→version) · `tools/unrated_run.sh`.
⛔ `scratchpad/fieldcal_scheduler.log` was NOT used: truncated 2026-08-16T07:40:13Z.
All timestamps from `date -u` in the same shell call as the read.
