# CERT — `tools/prereg_check.py`, side-lane independent forced-fail certification

**Side lane, s41, 2026-08-14T19:1xZ.** Discharges the obligation carried from the
s40 side-lane wrap (`a98c81f`, open item 2): the certification was **OFFERED,
ACCEPTED and UNRUN** because the draft (`90f7f4f`) landed at the wrap. Retro
v1.10 books an offered-and-never-performed certification as this lane's own **Q8
failure mode**, so a successor either runs it or records why not. It is run.

**Subject:** `tools/prereg_check.py` @ `90f7f4f` (DRAFT-UNCERTIFIED, NOT WIRED).
**Harnesses (mine, in `scratchpad/`, they call the production module):**
`prereg_cert_s41.py` (forced-fail) · `prereg_cert_s41_spurious.py` (the other
direction).
**Authority:** this document certifies that the checks HAVE TEETH and names two
ways a document can pass while defective. **It is not a wiring verdict** — that
is the builder's, per the s40 handoff.

---

## 1. WHY THIS IS NOT THE AUTHOR'S SELFTEST RUN AGAIN

The tool's own selftest is 50 cells and green. It corrupts a **synthetic fixture
the tool's author wrote**. The tool's docstring says so itself at line 806:

> *"the side lane's independent forced-fail certification mutates REAL prereg
> text, and a fixture built by string generation cannot be corrupted the same
> way."*

**A verification that shares the failure mode of the thing it verifies is not a
verification** (drift-watch standing note, four instances s26). A generated
fixture cannot exercise house-style prose, a declaration whose value is EMPTY, or
the real spellings of `BOUNDARY` / `BAR` / `DOSE` that generation normalises away
by construction.

**CARRIER:** `docs/research/PREREG-SPAWNPOCKET-2026-08-14.md` — **129 lines of
real committed prereg prose**, the most compliant real document on the board
(7 ok / 16 FAIL at baseline) — plus the **20-line REGISTRATION BLOCK** the
builder specced as the migration, so the carrier passes clean and every induced
failure is attributable. **Carrier baseline: `PREREG_CHECK: OK`, 0 failures.**

---

## 2. RESULT — FORCED FAIL: **31 of 31 CHECKS, PASS**

**38 corruptions of real text, each aimed at a DIFFERENT check, each naming its
own rule.** Coverage 31/31, uncovered: none. Every cell calls the production
`run_checks()`; there is no second copy of the computation in the harness.

| layer | checks driven to FAIL |
|---|---|
| PRESENCE (24 rules) | LOCK ×2 (absent + malformed) · TARGET_BAND ×2 · PINNED · SURFACE ×2 · CLUSTER_UNIT · ESTIMATOR · PLANNED_N · CUT_SHORT · BOUNDARY · BAR · BASE_RATE · SOURCES (companion-token half) · OB13 · OB12_GATE · OB12_DEFAULT · OB7_PRESTATE · OB15A_SEGMENT · OB15A_DIRECTION · OB15B_ONE_PRIMARY (second primary declared) · SEGMENT_CEILING · OB14_CHURN (conditional ACTIVATED) · FALSIFIER · PROVENANCE ×2 · DOSE |
| ARITHMETIC (8 checks) | BOUNDARY_UNITS · BOUNDARY_VS_N · BAR_RESOLVABLE · BAR_NULL · REFERENCE_FLOOR (CAL-7 P1 rebuilt) · SEGMENT_CEILING · DOSE_BOTH_VERDICTS ×2 · OB13_INTERSECTION ×2 |

**COLLATERAL RECORDED PER CELL, because a corruption that trips five checks has
not shown the sixth has teeth.** Four cells had collateral and all four are
legitimate coupling, not masking: deleting or breaking `SURFACE` moves DEFF to
the conservative fallback so `BAR_RESOLVABLE` moves with it; breaking
`BOUNDARY_UNITS` changes the games figure so `BOUNDARY_VS_N` moves with it;
`BAR_NULL` and `REFERENCE_FLOOR` both shrink the margin, which is what
`BAR_RESOLVABLE` reads. **34 of 38 cells had zero collateral.**

---

## 3. ⛔ THE HALF A FORCED-FAIL PASS CANNOT SEE — AND IT IS WHERE THE FINDINGS ARE

**Driving a check by DELETING its token proves it detects ABSENCE. It does not
prove it detects a token PRESENT AND EMPTY.** Deletion is the comfortable
corruption: it is the one an author reaches for, and it is the one a real
defective prereg **will not look like** — nobody omits a field after a checker
starts demanding it. **They type the field and leave it blank.** (s29 standing
note: *a check only checks once something forces it to produce an answer it could
get wrong.*)

Seven defective documents an author could plausibly commit were driven.
**Three passed `PREREG_CHECK: OK`. One of those three was MY OWN ERROR and is
retracted below.** Two are real.

### FINDING 1 — VALUE BLEED ACROSS THE NEWLINE

`key_pattern` ends `\s*:\s*([^\n]*)`. **The `\s*` after the colon matches
newlines**, so a declaration with nothing after its colon captures **the next
line** as its value.

**Trigger isolated, driven five ways:**

| form | bleeds? |
|---|---|
| `**KEY:**` — bold, closed | **no** — the `**` terminates group 1 |
| `**KEY: ` — bold, unclosed | **YES** |
| `KEY:` — plain, nothing after | **YES** |
| `KEY: ` — plain, trailing space | **YES** |
| `KEY:` + a BLANK LINE + next declaration | **YES** |

**The consequence is not cosmetic, and it was measured rather than reasoned:** an
empty `SURFACE:` sitting above
`CLUSTER UNIT: none - balanced-by-construction local shards` returns that whole
line as SURFACE's value. That string contains the word `local`, so the SURFACE
**malformed-value guard PASSES on an empty declaration.**
⇒ **The guards carrying `extra` predicates are defeated by their NEIGHBOURS, and
which neighbour they get is LINE ORDER.** That is **D32** — *line position in a
human-maintained text file silently becomes semantics, and nothing in the file
declares it* — arriving in a fourth place.

### FINDING 2 — AN EMPTY DECLARATION IS NOT ABSENT

`field()` returns `""`, which is not `None`, so `k in f` is True and presence
passes. Enumerated **per rule** on the real carrier, one corruption per rule:

**13 of 19 declarations accept an EMPTY value and the document still reads
`PREREG_CHECK: OK`** — `PINNED` · `SURFACE` · `CLUSTER UNIT` · `ESTIMATOR` ·
`PLANNED n` · `CUT-SHORT` · `BAR` · `BASE RATE` · `BAR SOURCE` ·
`GATE RESOLUTION` · `PRE-STATE` · `EXPECTED DIRECTION` · `PROVENANCE`.

**Six hold, and WHY they hold is worth more than the list of thirteen:** four are
backstopped by **ARITHMETIC** (`BOUNDARY`, `OB13`, `SEGMENT VALUE CEILING`,
`DOSE` — an empty value has no number to recompute, so the arithmetic layer
fails) and two by an **`extra` predicate** (`STATUS`, `TARGET BAND`).
⇒ **PRESENCE ALONE NEVER CATCHES AN EMPTY FIELD. The checks that survive are the
ones with a number underneath.** This is the same shape as the tool's own
argument for having an arithmetic layer at all, turned on the presence layer.

**`BAR` is the sharpest single instance:** the rule exists because *"a leg with
no bar cannot fail, and a leg that cannot fail is not an experiment"* — and
`BAR:` with an empty value satisfies it.

---

## 4. RETRACTED BEFORE PUBLICATION — MY OWN THIRD "HOLE"

**H6, *"BAR and BASE RATE in different units"*, is NOT a hole and the tool is
correct.** I hypothesised that `BAR: ≥0.52` against `BASE RATE: 50.0` would be
misread. Driven against the primary: `first_number` returns **52.0**, because the
documented 0..1 heuristic converts the proportion to points — **which is the
author's intent.** The document is not defective; **my hypothesis was
mis-specified.**

Recorded rather than deleted, because this lane's characteristic failure is
publishing a conclusion the primary would have contradicted when checking cost
seconds, and **the check that killed it cost one `print`.** Tagged for the retro:
`KIND: judgement · STATE: auditing · WHOSE HYPOTHESIS: mine` — *auditing is a
defending state*, pre-registered at v1.3.2, and it ran toward my own conclusion
exactly as that entry predicts. **Caught pre-publication by going to derive it,
which is Q4's measured mechanism (*going to use the thing*), not by diligence.**

---

## 5. THE FIX — PROPOSED, RUN BOTH WAYS, AND COSTED

**Two parts, both needed** (part (a) alone leaves empty fields passing; part (b)
alone leaves the bleed feeding wrong values into the arithmetic):

```
(a)  \s*:\s*([^\n]*)   ->   \s*:[ \t]*([^\n]*)      # group 1 cannot cross a newline
(b)  field() returns None when the stripped value is empty  # an empty declaration IS absent
```

**Verified under the patch, both directions — a fix is specified against the
CONSUMER *and* against its own numbers:**

* the healthy carrier **STILL passes**, 0 failures — the fix does not break the
  good case;
* a plain empty declaration returns `None` instead of the next line;
* `**SURFACE:**` now **FAILS naming SURFACE**;
* all **7** emptied declarations driven FAIL naming themselves, **none missing.**

### ⚠ AND THE COST OF MY OWN FIX, MEASURED AND NAMED RATHER THAN OMITTED

**This lane's most stable measured property across six runs is that it DETECTS
better than it PRESCRIBES** (detection ~21/23, prescription ~14/18 at v1.9), so
the prescription ships with its price attached.

Scanned all **81** committed prereg files in `docs/research/` and `docs/prereg/`
for empty declarations: **exactly one exists** —
`PREREG-PANEL-CAL4-selection-rule-2026-08-13.md`, whose `**Cells:**` is a
**HEADING for a bulleted list**, not an unfilled field.

| | OB14_CHURN fires on CAL-4? |
|---|---|
| today | **yes** — the heading ACTIVATES the conditional rule |
| under my fix | **no** — it returns `None`, the rule goes `n/a`, and **that panel escapes Obligation 14** |

⇒ **(b) closes two holes and opens a narrower one: list-style declarations stop
counting.** A third part — letting a declaration's value be a following bulleted
list — would close all three, and **I am not specifying it blind.** It is the
builder's tool and the builder's call.

---

## 5b. ⛔⛔ FINDING 3, ADDED 19:2xZ — **THE ADD-ONLY GUARD IS BLIND ON REAL PREREG TEXT, AND MY OWN §2 CERTIFICATION OF IT SHARES THE DEFECT IT WAS BUILT TO CATCH**

**Found by USING the tool on a live artefact within the hour** — the same
mechanism Q4 measures (*going to use the thing*, not diligence) — while
certifying `docs/prereg/SCREEN-v140vs145-2026-08-14.md`.

**WHAT HAPPENED, measured:**

| | locked `8a30265` | after A1 `3a94856` + A2 `d8f2467` |
|---|---|---|
| document | 227 lines | 278 lines (**+51**) |
| `BAR_LINE_PAT` matched | **3** lines | **3** lines |
| lines naming the `51.0` decision boundary | — | **12**, of which **0** match `BAR_LINE_PAT` |

`prereg_check --amendment` printed **`ADD-ONLY: OK (0 line(s) added, 0 edited)`
→ `PREREG_CHECK: OK`.**

**AND THE DECISION RULE HAD SUBSTANTIVELY CHANGED.** A2 supersedes A1's reading
in its own words — `< 51.0` moved from *"no counter-roll, v145 sits"* to
**`< 51.0 (≤509/1000) → REACTIVATE v145`**. The guard saw none of it.

**THE MECHANISM:** `BAR_LINE_PAT` matches only the **token vocabulary**
(`BAR:`, `BOUNDARY:`, `GATE RESOLUTION:` …). Real preregs write their decision
rule as **prose bullets**. ⇒ **`ADD-ONLY: OK` on a real prereg today means
*"no TOKENISED bar changed"*, not *"no bar changed"*.**

**WHY THIS IS THE MOST SERIOUS OF THE THREE.** It is the one control standing
between an amendment and the s28 hazard the obligations doc exists for —
*"a cert showing two honest timestamps still certifies clean if the later commit
quietly WIDENED a bar"*. The stated remedy was that **the DIFF CLASS is the
enforcement, and it is the only one.** Here the diff class saw nothing, and
returned the reassuring verdict. It fails **silent and green**, and it does so
**most reliably on documents that have not been migrated to the vocabulary —
i.e. on all 81 of them.**

### ⚠ AND IT INDICTS §2 OF THIS DOCUMENT, WHICH IS MINE

**§2 reports the amendment mode as driven both ways.** It was — on the
**synthetic** fixture, where the bars ARE tokenised (`**BAR: 60.0**` → `52.0`
is caught, correctly). **I migrated the presence and arithmetic layers onto real
text and left the amendment layer on the author's fixture shape.** So this
document's own §1 argument — *a fixture built by string generation cannot be
corrupted the same way* — **applies to my §2 and I did not apply it.** Same
fault, one section apart, in the document that names the fault. Recorded rather
than edited away.

**Tagged for the retro:** `KIND: judgement · STATE: auditing · WHOSE HYPOTHESIS:
mine` — and it is the **promoter's-first-use** pattern (v1.9) firing a second
time this session.

**⛔ SCOPE, stated so this is not read as a finding against the builder's
prereg:** `SCREEN-v140vs145` itself is **not** the defect. Its amendments are
pre-first-row (zero shard rows; newest `arena_rows` is 18:43:48Z, unrelated),
A1 corrected a factual attribution, A2 executes a direct Magnus directive, and
the change **TIGHTENS** — it makes the screen symmetric by pre-committing the
uncomfortable branch (`< 51.0` obliges reactivating v145). **That is the s28
rule honoured, not broken. The defect is that the INSTRUMENT could not have told
the difference.**

**REMEDY, one line, handed over rather than specified in depth:** the ADD-ONLY
diff class must key on **what a prereg's decision rule actually looks like**, not
on the token vocabulary alone — at minimum, treat any line containing a declared
threshold value (the prereg's own bar number) as a bar/branch line. **A
narrower, honest alternative that costs nothing: make the mode REFUSE — print
`AMENDMENT CHECK: NOT APPLICABLE (0 tokenised bar lines)` — when the locked file
carries fewer than N bar/branch lines.** *A guard that cannot see its subject
must say so rather than return OK*; that is this repo's own alarm-that-cannot-
tell-it-is-blind rule, and it is the cheaper half.

---

## 5c. ⭐ RE-CERTIFICATION AFTER THE FIXES — 19:4xZ, ALL THREE LAYERS NOW CERTIFIED

The builder patched findings 1 and 3 (`2b4b89d`) and finding 2 (`ca3e9ce`)
within the hour. **Re-run rather than read** — a fix is verified against the
fault CLASS, not the diff.

| | |
|---|---|
| author selftest | **PASS** |
| my forced-fail cert | **31/31, no regression** — the fixes removed no teeth |
| finding 1 (newline bleed) | **CLOSED** |
| finding 2 (empty ≠ absent) | **CLOSED** — H1 held; and the six shapes driven by me, **6/6** as claimed (empty-plain→None · empty-bold→None · `N/A — reason` kept · **bullets joined** · empty+prose NOT swallowed · normal unchanged) |
| the cost I costed in §5b | **PAID, NOT INCURRED** — CAL-4's `**Cells:**` bullet heading still **ACTIVATES** Obligation 14 under the list-value form. The third part I declined to specify blind is the part that saved it. |
| finding 3 (amendment layer) | **CERTIFIED — see below** |

**AMENDMENT-LAYER CERTIFICATION, independently driven on a tokenised carrier,
one corruption per bar line (meta_attrib standard) — 9/9:**

```
A. pure ADD (new constraint appended)          OK    <- must not false-FAIL
B. BAR widened 52.0 -> 50.5                    FAIL
C. BAR line deleted outright                   FAIL
D. PLANNED n cut 2700 -> 900 (a power decision) FAIL
E. BOUNDARY retargeted                         FAIL
F. EXPECTED DIRECTION flipped (segment sign)   FAIL
G. CUT-SHORT loosened                          FAIL
H. ESTIMATOR swapped after the fact            FAIL
I. whitespace/bold reflow ONLY                 OK    <- NEGATIVE CONTROL
+ untokenised real prereg -> NOT_APPLICABLE, exit 2
```
**Three states, distinguishable on the verdict LINE and on the exit code with no
collision (OK 0 · FAIL 1 · NOT_APPLICABLE 2), and cells A and I prove it can
still say OK** — a guard that only ever FAILs has not been seen to check.

### ⛔ ONE HOLE SURVIVES, AND THE BUILDER PREDICTED IT WOULD NOT: **H2, PLACEHOLDER VALUES**

`ESTIMATOR: TBD` · `PRE-STATE: see below` · `CUT-SHORT: TBD` are **non-empty
strings**, so `empty ⇒ ABSENT` does not reach them. **1 of 7 defective documents
still passes `PREREG_CHECK: OK`.**

**⇒ AND MY RULING IS THAT IT SHOULD NOT BE CLOSED WITH A PLACEHOLDER BLOCKLIST.**
A list of forbidden words (`TBD`, `unknown`, `see below`, …) is **incomplete by
construction** — it is defeated by writing *"to be determined"* — and this repo
has a standing note about guards whose silence carries no information.

**The principled fix is research's own ruling applied one level up:** *a token is
only as real as the arithmetic that consumes it*, and *prefer giving an existing
token a CONSUMER over adding another token.* **Every field that survived my
empty-value probe survived because ARITHMETIC reads it** (`BOUNDARY`, `OB13`,
`SEGMENT VALUE CEILING`, `DOSE`) **or an `extra` predicate does** (`STATUS`,
`TARGET BAND`). The three fields H2 defeats — `ESTIMATOR`, `PRE-STATE`,
`CUT-SHORT` — **have no consumer at all; they are ATTESTATIONS, not
computations.** ⇒ **A presence layer cannot detect insincerity, and dressing it
up to look as though it can is worse than declaring the limit.** Either give
those three a consumer, or state on the tin that they are attested rather than
checked.

---

## 6. VERDICT

**⭐ CERTIFIED — ALL THREE LAYERS (presence · arithmetic · amendment), with ONE
surviving hole (H2, placeholder values) whose closure I recommend AGAINST in its
obvious form.**

*Superseded, kept for the record: this section previously read "CERTIFIED FOR THE
PRESENCE AND ARITHMETIC LAYERS… THE AMENDMENT LAYER IS NOT CERTIFIED", which was
correct against `90f7f4f` and is no longer correct against `ca3e9ce`.*

* **The forced-fail standard is MET:** 31/31 checks driven to their failing
  verdict on corrupted REAL prereg text, each corruption aimed at a different
  check, collateral recorded, production function called.
* **The tool detects ABSENCE reliably. It does not reliably detect EMPTINESS**,
  and one of its two layers (presence) cannot in principle.
* **NOT A WIRING VERDICT.** A green `PREREG_CHECK: OK` today means *every
  obligation is DECLARED and every parseable number closes* — it does not mean
  every obligation is ANSWERED. The tool's own docstring already says a green run
  is a floor, never a blessing; **these findings say the floor is one course
  lower than it reads.**

**Not certified here and still owed by others:** research's blessing of the token
vocabulary and the 5 flagged ambiguities in `SPEC §5` (they have it, s42);
the builder's wiring decision.
