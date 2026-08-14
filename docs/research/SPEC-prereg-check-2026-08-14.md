# SPEC — `tools/prereg_check.py`: the pre-registration checklist as a tool that exits 1

**Drafted 2026-08-14T18:46:08Z** (`date -u`, same shell call as the readout below).
Implements the builder's IN-FLIGHT ask plus `SPEC-prereg-check-side-lane-checks-2026-08-14.md`
(six lane-ledger checks) plus two same-session scope additions (`PROVENANCE:`, `DOSE:`).
**Vocabulary is RESEARCH'S TO BLESS** — every token below is a proposal until it is.
Enforcement is the tool's.

---

## 0. WHY A TOOL AND NOT ANOTHER CLAUSE

The obligations doc (`PREREG-amendments-and-lock-obligations-2026-08-09.md`) is 438
lines and carries fifteen numbered obligations accreted over five days. **Every one of
them was written down because its own author broke it.** The measured half-life of a
prose rule in this repo is about one session; the durable surfaces are booted files and
tools that exit non-zero (`tools/gate.py`'s own docstring makes the same argument about
`PROGRAMME.md`).

Four incidents this tool would have caught, in the order they happened:

| incident | what it cost | the check |
|---|---|---|
| **LOKI-18** (2026-08-11): mechanism metric read `raid.py`, byte-identical between arms; diff was one hunk in `main.py:560` | 25 unrated games on a bar reading **100% in BOTH arms** | `OB13` + `OB13_INTERSECTION` (computed against a real diff) |
| **CAL-7 P1** (2026-08-14): ±8pp bar against a **retired** reference of n=155 | four preregs and five amendments before anyone computed the ±9.1pp floor | `REFERENCE_FLOOR` (closed form) |
| **s40's six preregs** (2026-08-14): none declared a map segment | a plank worth +6pp on 5 of 15 maps pools to +0.67pp — measured as ZERO, road closes | `OB15A_SEGMENT` / `OB15A_DIRECTION` |
| **CAL-8 stop** (2026-08-14): boundary counted over **attempt** lines, not accepts | the panel stopped at the wrong place | `BOUNDARY_UNITS` (games = 5 × accepts) |

**Verdict line: `PREREG_CHECK: OK|FAIL` as the last line, gate on the line and not on
`$?`** — same convention as `CORPUS_SANITY:` and for the same reason (`… | tail` makes
`$?` the status of `tail`). The exit code is still set.

---

## 1. TOKEN TABLE

Every token is a **declaration**, recognised at a line start (after up to 8 markdown /
emoji characters), at the start of a `**bold**` run, or after a sentence boundary. An
optional short parenthetical before the colon is allowed (`MAP SEGMENT (primary):` is
live usage in `PREREG-TINYECO62`).

### Presence layer

| rule id | token | obligation / source | why it is required |
|---|---|---|---|
| `LOCK` | `STATUS:` (must contain **BEFORE**) | two-clock lock standard, obligations doc addendum 16:3x | a document that does not assert it predates its own fixture is not a pre-registration |
| `TARGET_BAND` | `TARGET BAND:` (full shape, or `N/A — <reason>`) | `CLAUDE.md` target-value gate | the machinery inspects the EXPERIMENT and never asks whether the QUESTION is worth answering — s28 passed every check aimed at teams 550–860 below us |
| `PINNED` | `PINNED:` | `CLAUDE.md` pinning design rule | pin treatment legs, never pin calibration panels; churn is noise in a leg and signal in a panel |
| `SURFACE` | `SURFACE:` ∈ {rated, unrated, local} | `CLAUDE.md` DEFF block | the design effect is a property of the surface; an undeclared surface means no interval in the document can be checked |
| `CLUSTER_UNIT` | `CLUSTER UNIT:` ∈ {match+opponent, match, opponent, none} | `CLAUDE.md` cluster-enumeration procedure + side-lane #4 | the applicable DEFF is over the clusters that SURVIVE; a per-map bar carrying 1.53 is over-corrected exactly as wrongly as a pooled bar carrying 1.00 |
| `ESTIMATOR` | `ESTIMATOR:` | side-lane #4 | s28 ring-hold: four estimators within 0.010 of one bar flipped MEET/MISS among themselves |
| `PLANNED_N` | `PLANNED n: <k> games` | side-lane #5 | an unfixed n permits optional stopping; it is also the only input the resolvability arithmetic can use |
| `CUT_SHORT` | `CUT-SHORT:` | side-lane #5 | CAL-6 stopped at 75, CAL-7 at 110, both on holder changes; neither had pre-committed what a short leg may claim |
| `BOUNDARY` | `BOUNDARY: <a> accepts = <g> games` | CAL-8 stop incident | declaring ONE unit hides a miscount; declaring both makes it an identity a machine can check |
| `BAR` | `BAR:` | the iteration mill (S0–S8) | a leg with no bar cannot fail, and a leg that cannot fail is not an experiment |
| `BASE_RATE` | `BASE RATE:` | side-lane #1 (bar-null) | a 3/10 bar was once tested against a 29.6% base rate — the bar was the status quo wearing a treatment's clothes |
| `SOURCES` | `BAR SOURCE:` **and** `BASE RATE SOURCE:` | side-lane #1 + "numbers carry subjects" | an unsourced base rate is the half of the comparison nobody audits |
| `OB13` | `MECHANISM METRIC READS: <f.py:line>. TREATMENT DIFF TOUCHES: <paths>. INTERSECTION: <yes/no>.` | **OBLIGATION 13** | LOKI-18. An unnameable read path is not a measured one — that IS the finding |
| `OB12_GATE` | `GATE RESOLUTION:` | **OBLIGATION 12** | a gate is a bar and must be sized like one; LOKI-19's 1b had 10pp-wide branches answered by 19 events |
| `OB12_DEFAULT` | the word `UNRESOLVED` | **OBLIGATION 12**, pre-committed default | an unresolved gate defaults to the RESTRICTION, never the permission |
| `OB7_PRESTATE` | `PRE-STATE:` | **OBLIGATION 7** | the 15:46 prereg predicted change on three cells already in the target state and excluded the two that moved: 2/2 on excluded maps, 0/3 on named ones |
| `OB15A_SEGMENT` | `MAP SEGMENT:` (or `PRIMARY SEGMENT:`) | **OBLIGATION 15a** | a pooled screen measures a conditional plank as ZERO |
| `OB15A_DIRECTION` | `EXPECTED DIRECTION:` — **conditional**, required iff the segment is not `none expected` | **OBLIGATION 15a** | a segment without a predicted sign is unfalsifiable: whichever way it lands it "confirms" the mechanism |
| `OB15B_ONE_PRIMARY` | at most ONE primary-segment declaration | **OBLIGATION 15b** | K segments give K chances to rescue a failed arm |
| `SEGMENT_CEILING` | `SEGMENT VALUE CEILING: <share>% x <effect>pp = <pooled>pp` — **conditional**, required iff a segment is named | D1 delta | a segment's pooled value is bounded by pairing share × on-segment effect |
| `OB14_CHURN` | `CELL VERSION CHURN:` — **conditional**, required iff `CELLS:` is present | **OBLIGATION 14** | D13 selected the cell it could not measure: SmartFridge, ten versions in 24h, five defects in a day |
| `FALSIFIER` | a `FALSIFIER` heading or `FALSIFIER:` line | the iteration mill | a prereg without a falsifier is a plan, not an experiment |
| `PROVENANCE` | `PROVENANCE:` (non-empty; input file paths verbatim) | drafting rule 2026-08-14, both lane charters | a drafting agent that quietly read the result tape produces a document indistinguishable from a blind one; the line is the only thing that separates them after the fact |
| `DOSE` | `DOSE: <metric> <treatment> vs <control> (n=…)` | dose-probe gate (Magnus, 2026-08-14) | an arm reaches a screen only after a probe shows its mechanism FIRES, **and the probe carries both verdicts** |

### Arithmetic layer (recomputed; WARN where a live query would be needed)

| check id | what it recomputes | fails when |
|---|---|---|
| `BOUNDARY_UNITS` | `games == 5 × accepts` | either unit missing, or the identity does not hold — **the direct fix for the CAL-8 attempt/accept miscount** |
| `BOUNDARY_VS_N` | `PLANNED n == BOUNDARY games` | the planned n and the stop boundary are different numbers |
| `BAR_RESOLVABLE` | 95% half-width at the planned n, DEFF-corrected, one-sample or two-fixture per `CLAUDE.md` | `|bar − base rate| < half-width` — **the bar sits inside the interval the fixture can produce, so the leg cannot distinguish its own branches** |
| `BAR_NULL` | `bar != base rate` | the treatment is registered to beat the status quo by nothing |
| `REFERENCE_FLOOR` | the reference-only term at panel n → ∞ | `|bar − base| < floor` — **unresolvable BY CONSTRUCTION at any n; lengthening the leg buys nothing** (CAL-7 P1) |
| `SEGMENT_CEILING` | `share/100 × effect == declared pooled` (±0.05pp) | the declared ceiling is not the product |
| `DOSE_BOTH_VERDICTS` | two numeric values, on either side of `vs`/`→`, that DIFFER | one value only, or treatment == control — **a counter reading is not a demonstration that the mechanism fires** |
| `OB13_INTERSECTION` | `git diff --name-only [refs]` membership of the metric's file | declared `INTERSECTION: no`, or the metric's file is absent from a computable diff. **WARN (never FAIL) when no diff is computable** |

**DEFF constants**, keyed on `(surface, surviving clusters)` per `CLAUDE.md`'s scope
procedure — not on surface alone, because a table keyed only on surface is exactly what
lets someone drop the correction by deciding their cut "looks like" one of the cases:

```
rated    pooled 1.529 · within-opponent 1.366 · per-map 1.07 · none 1.000
unrated  pooled 1.833 · within-opponent 1.434 · per-map 1.07 · none 1.000
local    0.98 at every cluster key (balanced-by-construction, ρ = −0.020, 124 shards)
```

**The half-width function is auditable against four numbers already published in
committed documents**, and the selftest asserts all five:

| published in | this tool |
|---|---|
| CAL-8, panel n=75 vs ref n=155 → ±16.2pp | ±16.2pp |
| CAL-8, panel n=300 → ±11.3pp | ±11.3pp |
| CAL-8, floor at panel n=∞ → ±9.1pp | ±9.1pp |
| EVICT58, 25 games unrated within-opponent → ±23.5pp | ±23.5pp |
| SPAWNPOCKET, 2,700 local rows @ 0.98 → ±1.9pp | ±1.9pp |

**⇒ the tool's arithmetic is the same arithmetic the prereg authors used by hand.** That
is the only reason the `BAR_RESOLVABLE` and `REFERENCE_FLOOR` verdicts are worth
anything.

### Amendment mode — `--amendment LOCKED AMENDED`

Side-lane check 6. **Timestamps prove WHEN, never WHAT**: two honest clocks certify an
amendment that quietly widened a bar exactly as cleanly as one that added a constraint.
The **diff class** is the enforcement. Every bar/branch line in the locked file (`BAR:`,
`BASE RATE:`, `PLANNED n:`, `BOUNDARY:`, `TARGET BAND:`, `GATE RESOLUTION:`,
`EXPECTED DIRECTION:`, `MAP SEGMENT:`, `PRIMARY SEGMENT:`, `SEGMENT VALUE CEILING:`,
`CUT-SHORT:`, `ESTIMATOR:`, `CLUSTER UNIT:`, `SURFACE:`, `REFERENCE n:`) must still be
present, byte-for-byte after whitespace normalisation, in the amended file. Additions
pass; edits and removals FAIL.

---

## 2. COMPLIANCE READOUT — the three current preregs

Run 2026-08-14T18:46Z against the shipped tool. **All three FAIL, and that is the
measurement, not a bug** — every rule here exists because a real leg broke it, so a
green field would mean the checklist had been fitted to the documents rather than to the
incidents.

| | CAL-8 | SPAWNPOCKET | EVICT58 |
|---|---|---|---|
| presence ok | 4 | 7 | 4 |
| presence n/a (conditional, correctly skipped) | 2 | 1 | 3 |
| presence FAIL | 18 | 16 | 17 |

**What each one already satisfies** (these are the tokens current practice has converged
on, unprompted — the strongest evidence for which vocabulary is real):

* **CAL-8** — `LOCK` · `OB12_DEFAULT` · `OB15A_SEGMENT` (`none expected`) ·
  `OB15B_ONE_PRIMARY`; `OB15A_DIRECTION` and `SEGMENT_CEILING` correctly n/a.
* **SPAWNPOCKET** — `LOCK` · `BAR` (`≥52.0 @ 2,700 continues · <50.0 drops · 50.0–52.0
  UNRESOLVED-carries`) · `OB12_DEFAULT` · `OB15A_SEGMENT` · `OB15A_DIRECTION` ·
  `OB15B_ONE_PRIMARY` · `FALSIFIER`. **The most compliant document of the three, and it
  is the one written after Obligation 15 landed** — the obligations do get adopted, they
  are just adopted one at a time and only while the incident is warm.
* **EVICT58** — `LOCK` · `OB15A_SEGMENT` · `OB15B_ONE_PRIMARY` · `FALSIFIER`.

**Missing from all three:** `TARGET_BAND`, `PINNED`, `SURFACE`, `CLUSTER_UNIT`,
`ESTIMATOR`, `PLANNED_N`, `CUT_SHORT`, `BOUNDARY`, `BASE_RATE`, `SOURCES`, `OB13`,
`OB12_GATE`, `OB7_PRESTATE`, `PROVENANCE`, `DOSE`.

**⭐ AND THE IMPORTANT PART: most of these are FORMALISATION FAILURES, NOT SUBSTANCE
FAILURES.** The distinction decides whether the fix is a one-line edit or a redesign:

| token | CAL-8 | SPAWNPOCKET | EVICT58 |
|---|---|---|---|
| `TARGET_BAND` | prose: *"zero rated exposure, zero submits ⇒ payout gate N/A"* — **satisfied in substance**, needs `TARGET BAND: N/A — …` | prose: *"Local screen: zero rated exposure"* — **satisfied**, one line | prose: *"0033 … gap +81 on our 1765, a 5-0 pays ≈ +19.7"* — **satisfied, and it is exactly the gate's output**; needs the canonical line |
| `PINNED` | prose: *"UNPINNED"* in the Design block — **satisfied**, spelling only | n/a in substance (local screen) — needs `PINNED: N/A — local` | prose: *"**PINNED** … treatment legs pin; panels never do"* — **satisfied**, spelling only |
| `SURFACE` / `CLUSTER_UNIT` | uses panel 1.434 / rated 1.366 **correctly in the ±9.1pp table** — the constants are right, the declaration is absent | uses local 0.98 and says why — **substance is right** | uses unrated within-opponent 1.434 for ±23.5pp — **right** |
| `PLANNED_N` / `BOUNDARY` | *"n=150 (30 accepts, ~2 h) OR … n≥75"* — **the numbers are there and they are consistent (150 = 5×30)**; they are prose, so nothing checked them | *"n = 2,700 primary-segment rows"* — present in prose | *"5 matches = 25 games"* — **present and consistent** |
| `CUT_SHORT` | *"panel ends at the last window fully under v140; the n≥75 clause is what makes that survivable"* — **this is the best cut-short clause in the corpus** and it is unlabelled | absent in substance too | absent in substance |
| `BASE_RATE` / `SOURCES` | v125 reference 56.8% @ n=155 **is** the base rate, sourced | `GATE-1000 < 51` cited to `c62f90c` — **sourced**; base rate itself implicit at 50.0 | `BOOK-0033` baseline 110.45 heals/100rd — sourced |
| `OB13` | **genuinely absent** — no leg in s40 named its read path | **genuinely absent** (though A1 does exactly the Obligation-13 work informally: it found the named site `eco.py:934-954` fired ZERO and moved the metric to `_build_next_link`) | **genuinely absent** |
| `OB12_GATE` | **genuinely absent as a labelled line**, though the whole document is an argument about resolution | has `## OBLIGATION 12 — RESOLUTION` **as a heading, not a `GATE RESOLUTION:` line** — the closest miss in the set | **genuinely absent** |
| `OB7_PRESTATE` | **genuinely absent** in all three |
| `FALSIFIER` | **no falsifier section**; the falsifier is P4's two-sided branch, in prose | present | present |

**⇒ the migration cost for a compliant prereg is roughly a 15-line REGISTRATION BLOCK at
the top, not a rewrite.** The tool ships with exactly such a block as its `COMPLETE`
selftest fixture.

### New rules that are NOT retroactive — flagged so a red cell is not read as a defect

* **`PROVENANCE`** — the fresh-subagent drafting rule postdates all three documents.
  **Expected fail; not a finding about them.**
* **`DOSE`** — the dose-probe gate was stated 2026-08-14 after these were written.
  SPAWNPOCKET's Amendment A1 **is** a dose probe with both verdicts (region sizes ≥40 on
  every valkyrie candidate ⇒ half (a) inert), and EVICT58's P1 **registers the dose as
  the primary metric** — so two of the three satisfy it in substance. **Required only on
  the dose-fires path**: the other legitimate probe exit is premise-refuted → no screen →
  no prereg, and a document that does not exist cannot fail a token.

---

## 3. WHAT IS DELIBERATELY **NOT** CHECKED

**A green run is a FLOOR, never a blessing**, and the tool prints that sentence on every
pass. Judgment lines are checked for PRESENCE and never for CONTENT:

* **the hypothesis** — whether the mechanism is real, or interesting;
* **the choice of bar** — whether 52.0 is the right number, only that it is not the base
  rate and that the fixture can see the difference;
* **the falsifier's content** — whether it would actually falsify. `FALSIFIER` checks
  that a section exists;
* **whether the dose is SUFFICIENT** — `DOSE` checks that the probe produced two
  different numbers, never that the gap is big enough;
* **whether the segment is the RIGHT segment** — Obligation 15's own vocabulary note
  ("a mechanism-specific segment beats a size class") is judgment;
* **whether the opponent is the right opponent** — `TARGET BAND` is a gate, not a veto,
  and `CLAUDE.md` is explicit that a low-value target can still be the right leg;
* **`PRE-STATE:`** — the tool checks the declaration exists. Verifying the predicted-change
  set is not already in the target state needs the corpus and the lock-time cut, which is
  research's work.

**One class is checked but only WARNED:** the Obligation 13 intersection when no diff is
computable. See §5.

---

## 4. WIRING POINT

1. **Runner templates and `tools/gate.py`.** A battery or leg runner that names a prereg
   refuses to fire when `prereg_check.py <that file> | tail -1` does not read
   `PREREG_CHECK: OK`. This is the same placement argument `gate.py` makes about
   `PROGRAMME.md`: *"the only surfaces that hold are builder.md and a tool that exits
   non-zero"*. **Recommended as a `--prereg <path>` argument to `gate.py`** so the
   refusal lands in front of the battery rather than in a checklist beside it.
2. **The side lane's lock certification.** Already certifies the two clocks; adding the
   token readout makes the certification say WHAT was locked, not only WHEN.
3. **`--amendment` at every amendment commit.** ADD-only is currently enforced by the
   author's own care; this makes it a diff class.
4. **NOT in `corpus_sanity.py` / boot.** It validates a named document, not repo state —
   there is nothing for it to check at boot, and a permanently-red boot line is how an
   alarm becomes unread (that file's own fifty-hour miss).

---

## 5. AMBIGUITIES FOUND, AND THE RESOLUTION TAKEN — **research must bless these**

Five places where the obligations under-determine a machine rule. Each is flagged, not
silently decided.

1. **An EMPTY git diff is "not computable", not "empty intersection".**
   Obligation 13 says the leg may not fire on an inert bar. But two of the three s40
   preregs state in their own `STATUS:` line that they are committed **before the arm
   tree exists** — which is the correct order — and from `git diff`'s point of view that
   is indistinguishable from a treatment that changes nothing. **Resolution: an empty
   diff WARNs and says the check was not computed; only a NON-EMPTY diff that excludes
   the metric's file FAILs.** FAILing the empty case would punish the one habit the whole
   checklist exists to enforce. ⚠ **The residual hazard is real and is named here: a
   prereg written before the tree can never have its Obligation 13 line COMPUTED at lock
   time. The check must be re-run once the tree lands, and nothing currently schedules
   that.**

2. **`BAR` vs `BASE RATE` is the comparison the resolvability check reads.**
   The obligations never say what a bar is measured *against*; side-lane #1 introduces
   the comparator for the bar-null assertion. **Resolution: the same two numbers serve
   both checks** — bar-null asserts they differ, resolvability asserts they differ by
   more than the interval. This is why `BASE RATE:` is required on every prereg and not
   only on ones making a comparative claim. **If research wants a one-sided bar with no
   comparator (a dose count, e.g. EVICT58's "evictions/game > 1.0"), the current rule
   forces a base rate of 0.0 to be written down — which is arguably the honest form, but
   it is a decision and it is research's.**

3. **`CLUSTER UNIT` declares which clusters SURVIVE, not which exist.**
   `CLAUDE.md`'s procedure is "name every cluster, state whether YOUR stratum can hold
   more than one member, the DEFF is over the survivors". A single token cannot carry an
   enumeration. **Resolution: the token names the survivors (`match+opponent` /
   `match` / `opponent` / `none`) and the enumeration stays in prose beside it.** The
   tool checks the token maps to a known DEFF; it does not check the enumeration was
   performed. ⚠ **This is the weakest link in the arithmetic layer** — a wrong
   `CLUSTER UNIT` silently selects the wrong constant, and the tool cannot tell.

4. **Percentage parsing: `0.52` is read as 52%, not 0.52pp.**
   Bars in this repo are written as `≥52.0`, `56.8%` and `3/10`. A bar under 1pp is below
   every fixture's resolution, so the ambiguity is unreachable in practice — but it is a
   heuristic and it is documented in the code rather than hidden.

5. **A "declaration" is anchored; a mention is not.**
   Found by a **false positive on a real document**: `PREREG-SPAWNPOCKET` contains the
   prose sentence *"The report's registration line proposes **one primary segment: pocket
   maps {…}**"*, and a bare substring search counted that as a second primary-segment
   declaration, failing the document on Obligation 15b — **which it actually satisfies.**
   **Resolution: a token counts only at a line start (after ≤8 markdown/emoji chars), at
   the start of a bold run, or after a sentence boundary.** The bold-run form is not a
   concession — `PREREG-SPAWNPOCKET` writes two declarations on one line
   (`**PRIMARY MECHANISM: …** **EXPECTED DIRECTION: POSITIVE.**`), and the
   sentence-boundary form is required by Obligation 13's own single-line shape.
   ⚠ **The general hazard stands: a checker that cannot tell a declaration from a
   sentence about declarations will fail exactly the documents that discuss their own
   obligations most carefully.**

---

## 6. SELFTEST — every guard driven to BOTH verdicts

`.venv/bin/python tools/prereg_check.py --selftest` → last line `PREREG_SELFTEST: PASS`.

* **COMPLETE fixture passes** (0 failures) — the positive control, without which every
  forced-fail below would be satisfied by a tool that fails everything.
* **24 presence rules, one minimal corruption each**, and each must FAIL **naming its own
  rule** — not merely fail. Conditional rules are corrupted by *triggering their
  condition* (`OB14_CHURN` gets a `CELLS:` line added), because deleting a conditional
  token from a document that never triggered it leaves the rule `n/a`, which is a PASS.
* **Conditional SKIP branches exercised too** — `MAP SEGMENT: none expected` must make
  `OB15A_DIRECTION` and `SEGMENT_CEILING` go `n/a`. A rule that is always active has not
  been seen to be conditional; a rule that is never active is decoration.
* **13 arithmetic cells**, each check driven to FAIL and to OK, including CAL-7's P1
  reconstructed (±8pp bar, retired reference n=155 → FAIL) and the same bar against a
  reference of n=2000 (→ OK).
* **`OB13_INTERSECTION` computed three ways**: metric file in the diff (OK), metric file
  absent from a non-empty diff (FAIL — LOKI-18 exactly), no computable diff (WARN, never
  FAIL).
* **Amendment mode both ways**: an appended amendment passes, a quietly widened bar fails.
* **Five published half-widths reproduced** (§1).
* **Then the three real preregs are REPORTED, not asserted** — the tool must not have its
  own selftest depend on the corpus of documents it is meant to change.

**Fixtures are readable prereg text held in module-level strings**, per the side lane's
certification request: an independent forced-fail run mutates real prereg text, and a
fixture built by string generation cannot be corrupted the same way.

**Standing offer accepted:** the side lane runs the independent forced-fail certification
(each corruption aimed at a DIFFERENT check, agreement required to collapse) against this
draft. **A check that has never produced the other verdict has not been seen to check** —
this tool's own selftest is not evidence that someone else's corruption reaches it.
