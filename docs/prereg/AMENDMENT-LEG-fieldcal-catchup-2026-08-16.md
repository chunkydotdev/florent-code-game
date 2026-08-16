# AMENDMENT 1 to `LEG-fieldcal-2026-08-16` — THE ZERO-ACCEPT CATCH-UP RULE

**DRAFT for the builder's ratification. Drafted by a FRESH agent with no inherited session context
beyond the files on the `PROVENANCE` line — the s40 drafting rule.** The builder ratifies; the side
lane certifies ADD-ONLY and two-clock before the rule is implemented in
`tools/fieldcal_scheduler.sh`.

**AMENDS:** `docs/prereg/LEG-fieldcal-2026-08-16.md` (locked at `43d9035f`, git author time
**2026-08-16T05:59:01Z**), per that document's §13 amendment clause: *"Corrections land as a new
dated document that names this one … Amendments must be ADD-ONLY and blind to the leg's data."*

**PROVENANCE:** docs/prereg/LEG-fieldcal-2026-08-16.md; docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md; docs/research/FIELDCAL-POOLED-READ-2026-08-16.md; tools/fieldcal_scheduler.sh

**DRAFTED AT:** 2026-08-16T08:29:21Z (`date -u`, same shell call). **The leg is LIVE at drafting
time** — `scratchpad/fieldcal_state.tsv` reads `ROUND 7`, `CLOCK2 2026-08-16T06:25:40.381Z`, and
`scratchpad/fieldcal_scheduler.log` at 08:28:34Z shows arm B firing cell `kladde` (idx 3) in a
rate-window wait. **Nothing in this document touched the scheduler, fired a match, or edited a bot.**

---

## 1. THE AMENDMENT — ADD-ONLY

**ADDED to `§9.6b` (the scheduler's rotation duty), as a further CONSTRAINT on the scheduler and on
nothing else:**

> **CATCH-UP RULE.** At the start of every round, BEFORE the round's scheduled start cell is chosen,
> the scheduler evaluates the set
>
>     Z(arm) = { cell : accepts_banked[arm, cell] == 0 }
>
> for the arm whose turn the round is. **If `Z(arm)` is non-empty, the round's FIRST invocation is
> the member of `Z(arm)` with the LOWEST CELL INDEX in the registered `CELLS` order** (§1), rather
> than the cell at the round's scheduled `start_idx`. **Ties are broken by cell index and by nothing
> else.** After that invocation the round continues in the ORDINARY rotation order from the
> scheduled `start_idx`, exactly as registered, for whatever accept budget remains.

**SCOPE, stated as four exclusions so the rule cannot be stretched:**

1. **ONLY ZERO-ACCEPT `(arm,cell)` PAIRS ARE ELIGIBLE.** A cell with one or more banked accepts for
   that arm is never promoted, never demoted, and never reordered against another cell — **however
   thin it is, and whatever its results say.** The rule is blind to fill LEVEL above zero; it sees
   only the boundary between zero and non-zero. (§3 is why this line is the load-bearing one.)
2. **IT NEVER REORDERS AMONG NON-ZERO CELLS.** The ordinary rotation among them is untouched, and
   its registered form (`§9.6b`, and as implemented `start_idx = (round/2) % 10` at
   `tools/fieldcal_scheduler.sh:669`) is unchanged. The catch-up fire is a PREPEND, not a
   permutation.
3. **EVERY EXISTING GATE STILL BINDS, UNCHANGED AND IN THE SAME ORDER.** The account-wide rate
   budget (§9.6a, `tools/rate_budget.py` before EVERY invocation), the wait-and-retry-the-same-cell
   discipline (a drained window still waits; **the catch-up cell is the cell it waits on, and it is
   never advanced past**), the `HALT` file check, the −40 Elo round gate (§10.5b), the per-flip leak
   check, the `PIN`/`UNPINNED_OK` guards, the 12-accept per-pair ceiling and the 5-accept window
   budget are all exactly as registered. **The rule chooses WHICH cell fires first. It does not
   choose WHETHER anything fires, and it can never cause a fire that a gate would have refused.**
   *"Whose gates are all armed"* means precisely this: a catch-up cell that cannot pass the gates is
   waited on, not skipped past.
4. **NO CHANGE TO THE ARM SCHEDULE.** Round parity still determines the arm (`A` on even rounds,
   `B` on odd), so the ratified BETWEEN-WINDOWS alternation of §10.3 is preserved exactly.

**SELF-HEALING PROPERTY, stated because it is why no new state is needed.** A round's 5-accept
budget is typically consumed by a single cell (§5.1 of the defect record: *one round = one cell*),
so a catch-up fire DEFERS that round's scheduled cell by one of that arm's rounds. **That deferral
cannot become a loss: a deferred cell that has banked nothing is still a zero-accept cell, so the
same rule selects it at that arm's next round.** The rule therefore closes the hole it is written
for without a rotation pointer, a retry queue, or any state the scheduler does not already persist.

**AND THE RESIDUAL IT DOES NOT CLOSE, named rather than left to be discovered.** Once every cell of
an arm has banked at least one accept, `Z(arm)` is empty and the rule goes dormant; the second and
third fill passes (5→10→12) run on the pure rotation. A cell displaced during a later pass is at
5/12 or 10/12, i.e. NOT zero-accept, and is therefore NOT protected by this rule — it waits a full
pass (~10 of that arm's rounds). **A `least-filled-cell-first` tiebreak would close that too, and it
is DELIBERATELY NOT REGISTERED HERE: it would reorder among non-zero cells, which is exactly where
the blindness argument of §3 stops being structural.** The narrow rule is the one that can be
certified blind; the broad one cannot.

**COST, so the builder rules with it in view:** each catch-up fire costs one arm-round (~20 min) of
wall clock relative to the pure rotation, because the displaced cell is re-fired later.
§9.6a already registers the 16 h / 600-per-arm figure as **a floor on wall clock, not a promise**,
and §1's `CUT-SHORT` clause absorbs the tail. **Neither needs amending for this.**

---

## 2. WHAT THIS AMENDMENT DOES **NOT** CHANGE — enumerated, because an amendment is judged by what
it leaves alone

| frozen at lock (§13) | status under this amendment |
|---|---|
| **PRIMARY** — exact two-sided binomial sign test over 10 pinned cells on `sign(share_T − share_C)` | **UNTOUCHED** |
| **BAR** — 9/10 cells share the sign, p = 0.0215; 8/10 UNRESOLVED; ≤7/10 MISS | **UNTOUCHED** |
| **IMPOTENCE CLAUSE / MDE / power (7.0% and 9.9%, π ≈ 0.63, k ≈ 109)** | **UNTOUCHED** |
| **SECONDARY** — pooled ITT RMST₃₀₀, H = 300, `<300` boundary convention | **UNTOUCHED** |
| **FALSIFIER** — pooled game share (T−C) ≤ −7.7 pp, or pooled ITT RMST₃₀₀ (T−C) ≥ +10.1 rounds | **UNTOUCHED**, including the §4.4 reading that −7.7 pp is the **half-width at 600 games/arm**, not a point-estimate threshold |
| **POOLING POINT** — pooled reads only for §5/§6; the primary's unit is the CELL (k=10) and takes NO design effect | **UNTOUCHED** |
| **CELL ADMISSION** — `CUT-SHORT` 40 games/arm per cell; leg floor 800 games; k<8 ⇒ UNRESOLVED ⇒ restriction | **UNTOUCHED.** This rule does not admit, exclude, rescue or void any cell. It changes only the ORDER in which accepts are bought |
| **±7.7 pp HALF-WIDTH SEMANTICS** and the DEFF re-measurement obligation (§3), incl. the direction rule for fail-to-exclude claims | **UNTOUCHED** |
| **CELLS, PINS, `theirver` assertions (§9.3), arms, trees, horizon (§9.8), branch table (§7)** | **UNTOUCHED** |
| **BOUNDARY** 240 accepts = 1,200 games; **PLANNED n** 600 games/arm | **UNTOUCHED** |
| **§10.3 between-windows arm alternation; §10.5 rated-exposure obligations and the −40 Elo halt** | **UNTOUCHED** |

**The only registered text this amendment interacts with is `§9.6b`, and it interacts with it in the
direction §9.6b itself asks for:** §9.6b exists to prevent *"the excluded set [being] a function of
firing order rather than of anything about the opponent."* **The catch-up rule adds a second
mechanism serving that same registered purpose.** See §5 for the one place a strict auditor can
object, stated in the open.

---

## 3. ⭐⭐ BLINDNESS — **STRUCTURAL, NOT MERELY ABSTAINED**

**This is the clause the amendment exists to make auditable, and it is written to survive an
auditor who does not trust the author.**

The standing rule (`PREREG-amendments-and-lock-obligations-2026-08-09.md`, and §13 of the locked
prereg) is that an amendment must be **blind to the leg's data**. The ordinary way to satisfy that
is an ABSTENTION: *the author declares they did not look.* **An abstention is only as good as the
author, and this leg is live and unattended — a read-out of it exists in the repo, and any drafter
could have opened it.**

**THIS AMENDMENT IS BLIND BY CONSTRUCTION, WHICH IS A STRONGER PROPERTY AND DOES NOT DEPEND ON THE
AUTHOR AT ALL:**

> **THE ONLY CELLS THE RULE CAN PRIVILEGE ARE CELLS WITH ZERO GAMES. A ZERO-ACCEPT CELL HAS NO
> RESULTS TO PEEK AT. THEREFORE NO ORDERING OF AUTHOR KNOWLEDGE — NOT READING THE TAPE, READING IT
> IN FULL, OR HAVING WRITTEN IT — CAN MAKE THE CHOICE OUTCOME-DEPENDENT.** The selection function
> `min{ cell index : accepts == 0 }` takes **no outcome as an input and has none available to take**:
> its entire domain is the accept-count vector, and the value it selects on is the one value that
> guarantees the absence of a result.

**The three properties that carry it, each checkable from the rule's own text rather than from a
declaration:**

1. **THE ELIGIBLE SET IS DEFINED BY ABSENCE OF DATA.** `accepts == 0` ⇒ no games, no game share, no
   RMST, no win condition, no sign. There is nothing about that cell for a preference to attach to.
2. **THE TIE-BREAK IS THE REGISTERED CELL INDEX** — a constant fixed at lock in §1's `CELLS` line,
   not a quantity the leg produces. **A tie-break on anything measured (fill level, share, kill
   speed, "how the cell is doing") would reintroduce the dependence this clause removes**, which is
   why §1 exclusion 1 is scoped to zero and why the least-filled-first variant is refused above.
3. **NON-ZERO CELLS ARE UNTOUCHABLE BY THE RULE.** The only cells that HAVE outcomes are precisely
   the cells the rule cannot move, in either direction.

⇒ **An auditor need not establish what the author read. The rule's domain is enough.** The
conventional declaration is made too, and is the weaker of the two: *at drafting time this agent
read the four files on the `PROVENANCE` line, one of which
(`docs/research/FIELDCAL-POOLED-READ-2026-08-16.md`) contains the leg's interim per-cell shares.*
**That is stated on the face of this document, per the standing rule that an amendment written after
result rows exist says so.** It is disclosed rather than avoided **because under the structural
argument it does not matter** — and an amendment whose validity depends on the author not having
read something is exactly the amendment that cannot be certified.

⚠ **THE SCOPE OF THE CLAIM, so it is not over-quoted:** this clause establishes that the CHOICE OF
CELL is outcome-independent. It does not and cannot establish that firing more games is
outcome-neutral in general — **a rule that changed the excluded SET on the basis of results would
fail even with a blind author, and that is the fault this construction forecloses.**

---

## 4. IMPLEMENTATION NOTE FOR `tools/fieldcal_scheduler.sh` — where the check goes and what it must log

**Not applied by this document. The leg is LIVE and unattended (round 7 at drafting time); this is a
specification for the builder or a successor.**

**WHERE.** `run_round()` at `tools/fieldcal_scheduler.sh:666-725`. The rotation is computed at
`:669` (`start_idx=$(( (round / 2) % 10 ))`) and the cell walk begins at `:672`
(`while (( budget_remaining > 0 && pos < 10 ))`) with `idx=$(( (start_idx + pos) % 10 ))` at `:673`.
**The catch-up check goes between them: after `start_idx` is computed and the round banner is
printed, and BEFORE the first iteration of the walk.** Minimal shape:

* Scan `COUNTS[$arm,$label]` over `CELL_ORDER` in index order; take the FIRST label with count 0.
* If one exists and its index differs from `start_idx`, fire it as the round's first cell — through
  the **same** code path as any other cell, so that the `halt_file_present` check (`:675-678`), the
  `budget_wait` loop with its same-cell retry (`:689-698`), `invoke_runner` (`:705`),
  `maybe_capture_clock2`, `persist_state` and `leak_check` (`:717`) all run **unchanged and in the
  same order**. ⛔ **A separate, simplified catch-up firing path would be a second door around four
  gates; the rule must reuse the walk, not duplicate it.**
* Then continue the ordinary walk from `start_idx` with whatever `budget_remaining` is left.
* `ROUND_NUM` still advances at `:748` exactly as now. No new persisted state is required — the
  self-healing property (§1) is what buys that, and the existing `COUNTS` map is the rule's whole
  input.

**LOGGING — REQUIRED, NOT OPTIONAL.** The rule must emit, via `say`, a line of the form

    CATCHUP <arm>/<cell>   (scheduled start was <arm>/<scheduled_cell>, idx <n>)

before the invocation, so **the tape distinguishes a catch-up fire from a rotation fire**. The
reason is this leg's own history: `scratchpad/fieldcal_scheduler.log` was truncated by the
07:40:13Z relaunch (`>` not `>>`, already routed as a successor item) and the round-3 skip had to be
reconstructed from three other surfaces. **An unlabelled catch-up fire would make the leg's firing
order unreadable from the state tape alone** — `COUNTS` records what was banked, never why that cell
was chosen — **and the §6.2 imbalance heading owes a per-cell accept-count disclosure that a reader
cannot interpret without knowing which fires were catch-up.** One `CATCHUP` line per occurrence, and
the read-out reports the count.

**SELFTEST CELLS OWED (the `--selftest` harness at `:769`, which must be able to return the other
verdict — OB17's rider):**
* a state with one zero-accept cell **out of rotation order** ⇒ that cell fires FIRST and a
  `CATCHUP` line is emitted;
* a state with **no** zero-accept cells ⇒ **no** `CATCHUP` line and the scheduled cell fires first
  (the rule is dormant, not always-on);
* a state where the zero-accept cell **is** the scheduled cell ⇒ no reordering, and — the cell that
  can surprise — **no spurious `CATCHUP` line**;
* the budget-refusal cell (`c`) re-run **with a catch-up cell selected** ⇒ the wait is on the
  CATCH-UP cell and it does not advance (§9.6a's same-cell retry survives the prepend);
* the `HALT` cell (`e`) re-run with a catch-up cell selected ⇒ **zero invocations** (the rule cannot
  outrank the halt).

---

## 5. ⚠ THE ONE PLACE AN AUDITOR CAN OBJECT — STATED IN THE OPEN, NOT BURIED

**§9.6b registers a FORMULA, not only an intent:** *"Round `k` starts at cell `(k−1) mod 10`."*
**This amendment changes which cell a round starts at, so it is not literally inert with respect to
registered text, and pretending otherwise would be the kind of quiet widening the ADD-ONLY rule
exists to catch.** The case that it is nevertheless admissible, laid out so the builder and the side
lane can reject it if they disagree:

1. **The frozen list in §13 is explicit and firing order is not on it:** *"The estimator, the bar,
   the horizon, the cells, the pins and the falsifier are frozen at lock."* Every one of those is
   untouched (§2).
2. **No registered claim is denominated in firing order.** The primary is a per-cell sign test; the
   secondary is a pooled ITT mean; the falsifier is a pooled exclusion. **None of them reads the
   order in which accepts were bought.** Order enters the design only through §9.6b's stated hazard —
   ordering bias in the EXCLUDED SET — and the catch-up rule reduces that hazard rather than adding
   to it.
3. **§9.6b's registered purpose is served, not defeated.** Its own words: rotation exists so that
   *"the excluded set [is not] a function of firing order rather than of anything about the
   opponent."* The defect in §6 is precisely a cell whose exclusion risk was earned by a halt.
4. **The amendment only ever ADDS a constraint on the scheduler.** It forbids the scheduler from
   starting a round on a non-zero cell while a zero-accept cell exists for that arm. It permits
   nothing that was previously forbidden, and it cannot cause a fire any registered gate would have
   refused (§1, exclusion 3).

⛔ **THE HONEST RESIDUAL, and it is the builder's call, not the drafter's:** if the side lane reads
§9.6b's formula as itself load-bearing for a claim rather than as a hazard mitigation, **this is
more than ADD-ONLY and belongs in a new prereg with its own lock, not in an addendum.** The drafter's
reading is that it is a hazard mitigation — §9.6b's own paragraph argues for the rotation entirely
in terms of drops, ordering bias and the excluded set, and never in terms of an estimator. **The
reading is recorded here so the ruling is made on the record instead of inherited by silence.**

**A SECOND, PRE-EXISTING DISCREPANCY, NOT CREATED BY THIS AMENDMENT AND FLAGGED BECAUSE IT SITS ON
THE SAME LINE.** §9.6b registers `start cell = (k−1) mod 10` — advancing EVERY round. The shipped
scheduler implements `start_idx = (round / 2) % 10` (`:669`) — advancing every SECOND round, i.e.
once per round of the SAME ARM, which is what the between-windows alternation of §10.3 requires if
both arms are to walk the same cell sequence. **The implementation is the defensible reading of the
two, and it is what has been firing since clock2; the registered text is the one that is loose.**
This amendment does not repair that and does not depend on which reading is correct — the catch-up
rule is defined relative to *"the round's scheduled start cell"*, whatever formula produces it.

---

## 6. THE TRIGGERING DEFECT — RECORDED WITH ITS NUMBERS

**Source: `docs/research/FIELDCAL-POOLED-READ-2026-08-16.md` (research arm, read-only, wall clock
`date -u` = 2026-08-16T08:00:10Z), §5.1–5.3.** ROUND 3 of the leg — arm B, cell `not_adgato` —
**consumed a round and fired zero challenges**: `scratchpad/.rate_ledger` shows exactly 25 fires in
the leg era in five bursts with a **23 m 26 s hole between 07:06:13Z and 07:29:39Z containing zero
challenge ATTEMPTS** (not five rejections — zero attempts); no `arm_unrated_v154_*` outfile exists
with a stamp between `064545Z` and `073003Z`; and `corpus/our_matches.tsv` carries no `v154` row
against `not_adgato` at any time. The round returned from `run_round` before reaching
`invoke_runner` — the only such paths are the `halt_file_present` early returns at `:675-678` and
`:694-697` — and `ROUND_NUM` then incremented at `:748` regardless. **Which halt it was is
unrecoverable: the scheduler log was truncated at 07:40:13Z by a nohup relaunch using `>` instead of
`>>`, destroying rounds 0–4.** Because `start_idx` is a pure function of the round counter, **arm
B's `not_adgato` cell is not revisited until round 23, roughly seven hours behind its arm-A
counterpart at round 2**, leaving it the only `(arm,cell)` pair on the board at **0 accepts** while
its arm-A twin sits at 5 (per-cell tape at 08:00Z: A 5/5/5 at idx 0/1/2, B 5/**0**/5). **Under §1's
`CUT-SHORT` rule — 40 games per arm or the cell is excluded from the primary — that makes
B/`not_adgato` the cell most likely to be excluded under any truncation, and it earned that position
from a halt rather than from anything about the opponent.** §9.6b names two doors to that failure
(drops, ordering) and its wait-and-retry guarantee covers **only the rate-budget gate**
(`:689-698`); **an aborted round is a THIRD door**, and it is a gap in the scheduler's
implementation of §9.6b rather than a defect in the prereg's reasoning. **The leg was still on the
pure rotation at drafting time: at 08:28:34Z round 7 (arm B, scheduled idx 3) was firing `kladde`,
not the zero-accept `not_adgato` — the exact round at which this rule, had it existed, would have
fired.**

---

## 7. ⛔ INSTRUMENT NOTE ON `tools/prereg_check.py` — BOTH MODES WERE RUN AND BOTH SAY `FAIL`, FOR REASONS THAT ARE ABOUT THE TOOL'S SHAPE, NOT THIS DOCUMENT'S CONTENT

Run at drafting time, gating on the last line as the tool's own `--help` requires (never on `$?`):

**7.1 PLAIN FILE MODE** — `prereg_check.py docs/prereg/AMENDMENT-LEG-fieldcal-catchup-2026-08-16.md`
⇒ **`PREREG_CHECK: FAIL`, 17 obligations unmet.** Every one of the 17 is a REGISTRATION-BLOCK token
that a full prereg carries and an addendum does not: `STATUS`, `TARGET BAND`, `PINNED`, `SURFACE`,
`CLUSTER UNIT`, `ESTIMATOR`, `PLANNED n`, `CUT-SHORT`, `BOUNDARY`, `BAR`, `BASE RATE`,
`BAR SOURCE`, `MECHANISM METRIC READS`, `GATE RESOLUTION`, `PRE-STATE`, `MAP SEGMENT`, `DOSE`.
**All 17 are declared in the LOCKED document and are deliberately NOT repeated here — repeating them
is how an amendment quietly restates a bar.** What DID pass is the part that applies to an
amendment: **`PROVENANCE ok`**, `FALSIFIER ok`, `OB12_DEFAULT ok`, `OB15B_ONE_PRIMARY ok (0
declared)`. One WARN: `SURFACE unreadable -- using the LARGEST platform DEFF (1.833)`, a consequence
of the same absence. ⇒ **This mode is not the right instrument for an addendum and its FAIL must not
be quoted as a defect in the amendment.**

**7.2 AMENDMENT MODE** — `prereg_check.py --amendment <locked> <this file>` ⇒ **`PREREG_CHECK:
FAIL`, "13 locked bar/branch line(s) were EDITED or REMOVED"**, listing all 13 registration lines of
the locked file. ⛔ **THE TOOL'S ADD-ONLY MODE COMPARES TWO VERSIONS OF THE SAME FILE — it expects
the amended document to be a SUPERSET COPY of the locked one, and reads every locked line absent
from a separate addendum as "removed".** The locked prereg's §13 and the standing amendment
discipline require the opposite shape: *"corrections land as a NEW DATED DOCUMENT that names this
one."* ⇒ **THE REPO'S AMENDMENT CONVENTION AND ITS AMENDMENT CHECKER DISAGREE ABOUT FILE SHAPE, so
no addendum in this repo can be machine-certified ADD-ONLY.** For this document, **ADD-ONLY is a
MANUAL certification item for the side lane** — §2's table (what is untouched) and §5 (the one place
an auditor can object) are what it certifies against. **Recorded here rather than left to be
rediscovered; routing a fix — an addendum mode that checks the LOCKED file's bar lines are absent
rather than present — is a successor item, not a blocker on this leg.**

---

## 8. AMENDMENT CLAUSE

This document is itself IMMUTABLE once ratified and locked. It amends
`docs/prereg/LEG-fieldcal-2026-08-16.md` and nothing else. Further corrections land as a new dated
document naming both. **Nothing here may be read as licence to change the estimator, the bar, the
horizon, the cells, the pins or the falsifier — all six remain frozen at the original lock.**
