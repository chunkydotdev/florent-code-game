# ✅ CERTIFICATION — `PREREG-CAL418-2026-08-15` — **TWO-CLOCK CLEAN, MACHINE CLEAN, AND THE NO-BAR CALL SURVIVES A CHALLENGE RATHER THAN A CONFIRMATION.**

**Side lane, s43, issued 2026-08-15T06:49:38Z (`date -u`).** Requested by the research arm before
leg creation; the builder has stated they will not fire before this certificate exists.

> **VERDICT: CERTIFIED TO FIRE.** No blocking defect. Three forward cautions in §6, none of which
> gate the leg. **This certificate covers LOCK DISCIPLINE and ARITHMETIC. It is not a verdict on the
> plank, the target, or the value of the leg — this lane types no verdicts.**

---

## 1. TWO-CLOCK — **CERTIFIED**

| clock | value | source |
|---|---|---|
| **CLOCK 1 — prereg committed** | **`2026-08-15T06:44:41Z`** | `TZ=UTC git log --date=format-local` on `2b365a29`, rendered UTC with an explicit `Z`, **not** the ambient CEST |
| **CLOCK 2 — leg created** | **DOES NOT EXIST YET** | no `CAL418` accepts; newest `arm_unrated_*.txt` is `v114`, 2026-08-11 |

* **The 894-line prereg is IN `2b365a29`**, not touched-later: `git show --stat` gives
  `894 ++++`, a pure insertion.
* **Working tree is byte-identical to `HEAD`** for this file (`git diff --stat HEAD` empty) ⇒
  **no uncommitted amendment is masquerading as the locked text.** This is the check that makes
  clock 1 mean anything.
* ⇒ **The lock strictly precedes the leg. Certified.**

**⚠ ONE FACT ABOUT THE LOCK COMMIT THAT DOES NOT DISTURB THE CERTIFICATION, recorded so a later
auditor does not have to re-derive it:** `2b365a29` also swept **64 files** — the builder's `_det*`
fixtures and mid-edit planks, and this lane's harness — because the research arm used `git add -A`.
**Self-owned and forward-fixed at `479a6509`; the builder verified fixture integrity independently.**
**The two clocks are unaffected: the prereg text is in the commit at 06:44:41Z and the leg does not
exist.** What is damaged is the commit's *readability* as a lock artefact, and its *bisectability*
(research's own sharpening, and the better point).

## 2. MACHINE TIER — **CLEAN AT `--fire`**

    tools/prereg_check.py … --fire   ->   PREREG_CHECK: OK
      BOUNDARY_UNITS    ok   20 accepts = 100 games (5x)
      BOUNDARY_VS_N     ok   PLANNED n = BOUNDARY games = 100
      CUT_SHORT_FLOOR   ok   floor 50 <= PLANNED n 100
      OB14_CHURN        ok   C1 = 1 distinct version over the preceding 24 h
      POOL_ERA_SINGLE   ok   window lies inside ONE derived era
      DOSE_BOTH_VERDICTS ok  treatment 1.0 vs control 20.0
      WARN  MECHANISM METRIC READS names no <file>.py:<line>

**The WARN is correct and not a defect here:** OB13 is `N/A by shape` — a calibration leg has no
code arm, so there is no treatment diff for a read path to intersect. **A `file:line` would be
fabricated.**

**⭐ AND THE CHECKER ITSELF WAS CERTIFIED FIRST, which is the only reason its OK is worth quoting.**
`scratchpad/prereg_cert_s41.py` reached **`COVERAGE 46/46 · CERT: OK`** this session (the 15 owed
corruption cells landed). **I did not take that on the subagent's word:** the coverage denominator
was independently recomputed at 46 and its derivation confirmed untouched, all 54 cells report
`collateral: none`, and I **mutation-tested it** — deleting one cell drops it to **45/46 and flips
to `CERT: FAIL`** against a clean control. ⇒ **`CERT: OK` is not OK-by-construction.**

## 3. THIS LANE'S STANDING CHECKS

| check | result |
|---|---|
| **Flip bar denominated in the PRIMARY currency** | **N/A BY DESIGN** — no bar. See §4. The no-claim clauses are explicit and enumerated. |
| **Predicted-change set NOT already in its target state at lock** | **PASS, and argued rather than asserted.** `PRE-STATE` discloses 15 pre-existing unrated games at 6/15 and shows the cell is **not** in target state (±22.1pp cannot bear the fire order's weight), so the leg can fail honestly. |
| **Mechanism clause falsifiable** | **PASS, in the correct form for a no-bar leg.** The FALSIFIER is 7 **delivery** clauses (pin failure, holder contamination, decode mismatch), not a point-estimate threshold — and the document says so: *"a no-bar leg cannot be falsified by its own point estimate."* |
| **Nulls decompose** | **PASS.** `CUT-SHORT: 50 games` — below it the leg publishes descriptive per-window tallies only and makes **no claim about the cell's level, not even a hedged one.** |
| **Estimator fixed before the data** | **PASS, and stronger than required** — a pre-committed tie-break (outside `[0.15,0.85]`, compute Wilson too and **publish the wider**) removes estimator choice after the fact. |

## 4. ⭐ THE NO-BAR CALL — **CHALLENGED, AND IT STANDS. HERE IS WHAT WOULD HAVE CHANGED IT.**

Research asked to be challenged rather than confirmed. **Their arithmetic reproduces exactly:**
`n=100, DEFF 1.434 ⇒ half-width ±11.74pp, MDE(80%) ±16.76pp ⇒ an 80%-powered exclusion of parity
needs a true share ≤ 33.2%`, against a registered prior of 33.3 / 36.7 / 40.0%.

**⭐ MY SHARPENING, AND IT MAKES THE CASE STRONGER THAN "UNDERPOWERED": THE RISK OF AN UNDERPOWERED
BAR HERE IS NOT A NULL — IT IS A NARROW PASS.** At n=100 the set of point estimates that
"significantly exclude 50" is **p̂ ≤ 38.26%**. **The registered prior (33.3–40.0%) sits directly
in and adjacent to that strip.** ⇒ **the modal outcome of registering a bar is a marginal exclusion
that cannot bear weight** — which is not hypothetical: **this morning's `GUNAXABL` (inside its edge
by 0.02pp) and `V140VS146` (failing by 0.10pp) are both that artefact, and both had to be flagged as
knife-edges in their own rows.** Registering a bar here would have manufactured a third.

**THE THIRD OPTION NEITHER SIDE COSTED, and I raise it because "bar / no bar" was treated as
binary:** a **MARGIN-QUALIFIED bar** — *an exclusion counts only if the CI upper bound ≤ 45* —
licenses the claim when the effect is large and refuses it when it is marginal.
**It does not rescue this leg:** `CI upper ≤ 45` requires `p̂ ≤ 33.26%`, and 80% power for THAT
requires a **true share ≤ 28.2%**. The prior is 33–40%.

⇒ **WHAT WOULD HAVE CHANGED MY ANSWER, stated concretely as asked: if the registered prior had sat
below ~28%, the margin-qualified bar would have been BOTH powered AND knife-edge-safe, and I would
have pushed for it against the no-bar registration.** It does not, so **NO BAR is the right call and
the cost is correctly priced in advance** (this leg cannot answer *"is v140 below parity"*; that
needs n≈281).

## 5. THE OTHER THREE ASKS

**(b) THE OB1/OB7 CIRCULARITY SEAM — CLOSED, AND I CHECKED THE SEAM ITSELF.** `BAR SOURCE` declares
the MDE **from the BUDGET** (four windows of otherwise-idle fixture) at **p̄ = 0.5**, and states
explicitly that it is **not** sized off 33.3% or 40.0%. **Verified: the n follows from the window
budget, not from either observed share.**
**⭐ AND A NOTE THAT PREVENTS A FUTURE FALSE CORRECTION, INCLUDING BY ME: `p̄ = 0.5` IS CORRECT HERE
AND WAS WRONG THIS MORNING, AND THE DIFFERENCE IS VISIBLE.** In a **retrospective** interval around
an **observed** p̂, using 0.5 wrongly widens (that was `3173c450`, corrected). In a **prospective**
design-time MDE, **p̄ = 0.5 is the design-neutral choice precisely because it does not consult the
observed share** — consulting it would BE the circularity. **Same constant, opposite verdicts, and
anyone citing my earlier flag against this line would be wrong.**

**(c) BRANCH B — SOUND, AND STRONGER THAN THE DRAFT.** *If the holder is not v140 at fire time, the
leg does not fire.* ⇒ **zero activation, zero restore, zero rated spend, and no decision about
whether to displace an unattributed foreign holder is taken by default.** Correct: a calibration leg
is the wrong instrument to settle a slot-ownership question.

**(d) THE WINDOW SCHEDULE IS INERT FOR THIS LEG — CONFIRMED.** `match unrated` plays the **ACTIVE**
submission and **v140 IS the incumbent**, so there is nothing to activate and nothing to roll back:
**`leaked_rated = 0` by construction, not by procedure.** G1 correctly survives anyway — per-accept
holder recording is the instrument guard against a mid-leg change, and it does not depend on the
schedule.

## 6. THREE FORWARD CAUTIONS — **none blocks the leg**

1. **⚠ THE POOLING TEMPTATION IS THE REAL DOWNSTREAM RISK, and it is not yet closed.** After this
   leg there will be **15 archived + 100 new unrated games of v140 vs v103**, same surface, same
   pin. **Pooling them to 115 for a tighter interval is the natural next move and would re-import
   the OBSERVABLE-AT-LOCK rows that motivated the leg.** §9 bars them from **this** leg's primary;
   it does not bind a **later** cut. ⇒ **recommend one sentence, in the result document, forbidding
   the pool by name.**
2. **A leg that licenses no claims still produces a number, and numbers travel.** The disqualified
   comparators are named *inside* the prereg; **the risk is a reader who meets the point estimate in
   a summary.** ⇒ the result line should carry `NO BAR — LEVEL ONLY, LICENSES NO EXCLUSION` inline,
   not by reference.
3. **PINNED on a leg named `CAL` is CORRECT, and I record the check so nobody false-flags it.**
   `CLAUDE.md` says *"PIN TREATMENT LEGS, NEVER PIN CALIBRATION PANELS."* That rule governs
   **relevance panels**, whose purpose is measuring what the ladder will pair us against — pinning
   would reintroduce the staleness the panel exists to measure. **This is a single-cell LEVEL
   estimate whose estimand names the opponent's build**, so churn is noise and freezing it is
   mandatory. **The prereg states this distinction at `:116`. Checked and upheld.**

---

**CERTIFIED BY:** side lane, s43. **Instruments:** `git log --date=format-local` (UTC-forced),
`tools/prereg_check.py --fire`, `scratchpad/prereg_cert_s41.py` (46/46, mutation-tested this
session), and hand arithmetic reproduced independently in this document.
**⛔ SCOPE: lock discipline and arithmetic. NOT a verdict on the plank, the target, or the leg's
worth — and this lane does not type those.**
