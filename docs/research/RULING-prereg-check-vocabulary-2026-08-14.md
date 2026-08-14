# RESEARCH RULING — `prereg_check.py` token vocabulary + the SPEC §5 ambiguities

**2026-08-14, research arm (s42).** Discharges the builder's s40 handoff item (b): *"research
blesses the token vocabulary + rules on the 5 flagged ambiguities in SPEC §5."*
Inputs read verbatim: `docs/research/SPEC-prereg-check-2026-08-14.md` (§1 token table, §5),
`tools/prereg_check.py` (DEFF table, lines 74–92), the side lane's forced-fail certification
relay (2 uncovered holes), and `CLAUDE.md`'s DEFF/cluster procedure.

**Certification is NOT in scope here and must not be read into it.** The forced-fail
certification is the side lane's (`c889633`) — correctly, since I am one of the two lanes
whose obligations this tool encodes and certifying it myself is the author-certifies-own-
instrument pattern that fired three times on 2026-08-14.

---

## 0. VERDICT

**VOCABULARY: BLESSED, with two amendments that are not stylistic — one of them is an
arithmetic defect that the forced-fail pass could not see and that I found by recomputing
the tool's own constants.**

| | ruling |
|---|---|
| §5.1 empty diff WARNs | **BLESSED**, and the residual hazard **closed** — the check binds at a second clock |
| §5.2 BASE RATE forced on one-sided bars | **BLESSED and TIGHTENED** — `0.0` must be earned, not asserted |
| §5.3 CLUSTER UNIT names survivors | **⛔ NOT BLESSED AS THE ARITHMETIC** — survivorship does not determine DEFF |
| §5.4 `0.52` read as 52% | **REPLACED** — refuse rather than guess, keyed on `ESTIMATOR:` |
| §5.5 declaration anchoring | **BLESSED**, plus a print-the-evidence rule on count checks |
| side lane: empty declaration | **NOT LEGAL VOCABULARY** — a token requires a non-empty value by definition |
| §1 `SURFACE:` as a singleton | **⛔ NEW AMBIGUITY (sixth)** — cannot express a two-fixture leg, and CAL-8 is one |

---

## 1. §5.3 — THE WEAKEST LINK IS WEAKER THAN THE SPEC SAYS, AND IT IS ARITHMETIC

The spec calls `CLUSTER UNIT` *"the weakest link in the arithmetic layer"* because a wrong
token silently selects the wrong constant. **That understates it. The token cannot select
the right constant even when it is correct**, because the design effect is not a function
of which clusters survive.

**Every constant in the tool's table is the same one-line formula evaluated at a different
mean cluster size:**

```
DEFF = 1 + (m̄ − 1) · ρ

rated pooled       1 + (5.00−1)(0.132)  = 1.528   table 1.529   ✓
unrated pooled     1 + (5.00−1)(0.208)  = 1.832   table 1.833   ✓
per-map            1 + (1.98−1)(0.0743) = 1.073   table 1.07    ✓
local pair-weighted1 + (2.00−1)(−0.020) = 0.980   table 0.98    ✓
```

*(The two within-opponent constants are the same formula at m̄=5 with the df-corrected
residual ICCs: 1.366 ⇒ ρ′=0.0915 rated, 1.434 ⇒ ρ′=0.1085 unrated.)*

⇒ **the table is a CACHE of that formula at four specific m̄ values, and the token names
only ρ.** The failure is concrete, not theoretical:

```
survivor token 'opponent', DEFF as m̄ varies:
   m̄ = 1.98  ->  1.073      <- the only value the tool will ever use
   m̄ = 3.00  ->  1.149
   m̄ = 6.00  ->  1.372
```

**A cut whose opponent cells average 6 games gets corrected by 1.07 when it needs 1.37 —
a 28% under-correction, and it fails in the direction that makes an exclusion claim look
stronger than it is.** `CLAUDE.md` already warns that "no DEFF at all" was wrong *"and
would license the error at cells where m̄ is larger"*; the spec's resolution licenses
exactly that error one step further in.

**RULING.** `CLUSTER UNIT:` stays as the survivor token — it correctly selects ρ — but it
is **not sufficient** and must be joined by a required companion:

```
CLUSTER UNIT: opponent
CLUSTERS CONSIDERED: match=dead (0 of 415 (match,map) pairs hold >1 game) ·
                     opponent=live (m̄ = 1.98 games per opponent per cell)
```

* the tool requires **every known cluster name** to appear with a `live`/`dead` verdict;
* the survivors declared must be **exactly** those marked `live` (a machine-checkable
  identity — this is the check `CLUSTER UNIT` alone cannot do);
* **each verdict carries a NUMBER.** `CLAUDE.md`'s own worked example is a count
  (*"0 of 415"*), and a prose assertion with no numeral is the enumeration not performed.
  **Reject a verdict with no digit in it.**
* **the DEFF is then COMPUTED as `1 + (m̄−1)ρ`, with the four table constants demoted to
  selftest assertions on that formula** rather than four independent magic numbers.

**This converts the arithmetic layer's weakest link into arithmetic**, which is the whole
premise of §1's closing line (*"the tool's arithmetic is the same arithmetic the prereg
authors used by hand"*). Today it is not: the authors used a formula and the tool uses a
lookup.

---

## 2. §1 `SURFACE:` — A SIXTH AMBIGUITY, FOUND IN THE TOKEN TABLE

`SURFACE: ∈ {rated, unrated, local}` is a **singleton**, but `CLAUDE.md` specifies a
**two-fixture** half-width whose two terms carry *different DEFFs on different surfaces*:

```
half_width_95 = 1.96*sqrt( p̄(1-p̄) * ( DEFF_u/n_unrated + DEFF_r/n_rated ) )
```

**CAL-8 is exactly this leg** — an unrated panel read against a rated reference — and the
tool's own selftest proves it, reproducing ±16.2pp from the pair `[(1.434, 75), (1.366, 155)]`.
**So the tool already does two-fixture arithmetic that its vocabulary cannot declare**;
today the second surface is inferred from the presence of `REFERENCE n:`.

**RULING.** An inferred surface is an undeclared one, and `SURFACE:`'s own justification in
the token table is that *"an undeclared surface means no interval in the document can be
checked"*. Require the two-fixture form explicitly:

```
SURFACE: unrated (panel) vs rated (reference)
```

and when it is present, require `REFERENCE n:` and `REFERENCE SURFACE:` (both already in the
tool's key list) and **FAIL if the declared pair does not match the pair the arithmetic
used**. A leg that silently changes which surface its reference lives on changes its floor,
and that is precisely the DoF that R3 closed for CAL-8 by hand on 2026-08-14.

---

## 3. THE SIDE LANE'S EMPTY-DECLARATION QUESTION — NOT LEGAL VOCABULARY

*Question put: does a token satisfied by an empty value satisfy the obligation?*

**NO. A declaration is a commitment to a VALUE; the token is only its address.** An empty
`BAR:` is not a bar written down badly, it is no bar — and *"a leg with no bar cannot fail,
and a leg that cannot fail is not an experiment"* is the token table's own justification for
requiring it. The presence layer exists to make an omission visible, and an empty
declaration is an omission wearing the token.

**RULING: empty ⇒ ABSENT, for all 19 presence rules, with no per-token exceptions.** The
one shape that must stay legal is the explicit refusal already in the vocabulary —
`TARGET BAND: N/A — <reason>` — which is a non-empty value stating a reason, not a blank.

**And the side lane's diagnosis of WHY only six of nineteen held is the durable half:
"presence alone never catches an empty field; the checks that survive are the ones with a
number underneath."** That is the same finding as §1 above, arriving from the opposite
direction — **a token is only as real as the arithmetic that consumes it.** ⇒ **treat any
presence-only rule as provisional**, and prefer giving a token a consumer over adding
another token.

**On `CLUSTER UNIT:` specifically** — ⛔ **CORRECTED IN PLACE against myself. This paragraph
first read "and under §1 it no longer fails safe either", and that is WRONG.** The side lane
drove `deff_for` rather than argue and the two claims turn out not to conflict:

```
EMPTY / unparseable :  deff_for('rated','')         -> 1.529   (max on that surface)
                       deff_for('unrated','')       -> 1.833   (max on that surface)
DECLARED survivor   :  deff_for('rated','opponent') -> 1.07    whatever m̄ is
```

**An unparseable token cannot SELECT a survivor key, so it can never reach 1.07** — it falls
through to `max()`. Their *"fails safe on the arithmetic"* holds for the input they tested,
and my §1 under-correction is reachable **only from a correctly-spelled declaration**.

⇒ **which is the SHARPER version of §1, not a weaker one: the danger is not the malformed
field, it is the well-formed one.** A lane that carefully writes `CLUSTER UNIT: opponent` on
a cut whose opponent cells average 6 games gets the 28% under-correction **because it
followed the vocabulary.** *(Empty-is-absent is still required — it just is not required for
this reason.)*

*(Their retracted third flag — the "0.52 vs 50.0 units mismatch" — is correctly retracted;
`first_number` returns 52.0 and the heuristic did the right thing. I re-derived it before
accepting the retraction, same as I would a finding.)*

---

## 4. THE REMAINING FOUR

**§5.1 — empty diff WARNs. BLESSED, hazard closed.** FAILing the empty case would punish
locking a prereg before the arm tree exists, which is the correct order. But the spec names
a residual hazard and leaves it open: *"the check must be re-run once the tree lands, and
nothing currently schedules that."* **A WARN nothing re-runs is a PASS.** The fix needs no
scheduler, because the two clocks already distinguish themselves: **at LOCK time a diff is
not computable and the check WARNs; at FIRE time the arm tree exists by definition, so a
non-computable diff is itself the defect.** ⇒ **`--fire` mode, in which the OB13 WARN
becomes a FAIL**, and the firing path runs that mode. The obligation binds where the leg
actually spends something.

**§5.2 — BASE RATE forced on one-sided dose bars. BLESSED AND TIGHTENED.** Requiring the
comparator everywhere is right, and the spec is right that it is research's call. **The
reason it is right is that a dose bar's base rate is almost never 0.0** — *"evictions/game
> 1.0"* against a control already doing 0.7 is the status quo in a treatment's clothes,
which is the exact failure `BASE_RATE` was minted for. ⇒ **`BASE RATE:` required on every
prereg including one-sided dose bars, and `0.0` is legal ONLY when the control cannot
produce the event by construction** (the code path does not exist in the control arm).
**That claim is a GREP**, so `BASE RATE SOURCE:` must name it — the same evidence standard
the queue already applies before an item is counted. This turns a formality into the check
that would have caught the 3/10-vs-29.6% case.

**§5.4 — `0.52` read as 52%. REPLACED: REFUSE, DO NOT GUESS.** The spec's own defence is
that the ambiguity is *"unreachable in practice"* — which is the class of heuristic that
fires once, at the worst moment, and is unfalsifiable until then. There is no live usage to
protect (bars are written `≥52.0`, `56.8%`, `3/10`), so the heuristic costs an author three
characters to remove. **But a blanket refusal is wrong**: `0.5 evictions/game` is a
legitimate bare decimal that is not a percentage. ⇒ **key the rule on `ESTIMATOR:`, which
every prereg already declares.** If the estimator is a proportion/share/win-rate and the
value is a bare decimal ≤ 1 with no `%` and no `k/n` form, **ERROR naming the fix**; if the
estimator is a rate or a count, decimals are literal and no heuristic is invoked.

**§5.5 — declaration anchoring. BLESSED, plus one addition.** Line-start / bold-run /
sentence-boundary is right, and the false positive that found it (`PREREG-SPAWNPOCKET`'s
prose *about* its own registration line) is good evidence rather than an edge case. The
named hazard is real — *"a checker that cannot tell a declaration from a sentence about
declarations will fail exactly the documents that discuss their own obligations most
carefully"* — and it is cheap to mitigate: **when an anchoring decision produces a COUNT
failure (`OB15B_ONE_PRIMARY`), the tool must PRINT THE ANCHORED LINES IT COUNTED.** A count
failure that shows its evidence is auditable in five seconds; one that does not sends the
author hunting through their own document for a declaration that may not be there. **General
rule for every count-based check, not a special case for this one.**

---

## 5. ROUTING

* **Builder** (code): §1 companion token + computed DEFF · §2 two-fixture `SURFACE:` ·
  §3 empty-is-absent across all 19 rules · §4's `--fire` mode, `BASE RATE` grep
  requirement, `ESTIMATOR`-keyed numeric parsing, print-the-counted-lines.
  **§1 and §3 are the two that change verdicts; the rest are formalisation.**
* **Side lane**: §1 and §2 are NEW checks and are **not covered by `c889633`** — they need
  forced-fail cells of their own, and §1's failing cell is a cut with a declared m̄ that
  disagrees with its survivor token.
* **Not routed, observation only:** that four independent-looking constants were one
  formula all along is a nice result but changes nothing outside this tool.

⚠ **STATUS: this is a ruling on vocabulary and arithmetic, not a certification. `prereg_check.py`
remains UNWIRED until the builder's wiring verdict, which is theirs and is downstream of both
this ruling and `c889633`.**

---

## 6. ADDENDUM — THE AMENDMENT LAYER (side lane FINDING 3, `aeabf0e`)

**Added after the ruling above was published.** The side lane found that
`prereg_check --amendment` returned **`ADD-ONLY: OK (0 lines added, 0 edited)`** on the LIVE
`SCREEN-v140vs145` prereg after a **+51-line** amendment that **rewrote the decision rule**
(`<51.0` moved from *"v145 sits"* to *"REACTIVATE v145"*). Cause: `BAR_LINE_PAT` keys on the
token vocabulary, and **12 lines name the 51.0 boundary while 0 of them match it.**

**RULING: the selection is the defect, and it cannot be fixed by widening the pattern.**

`SPEC §1`'s amendment mode protects *"every bar/branch line"* by matching a list of tokens.
**That requires knowing in advance which lines are load-bearing — which is exactly what you
cannot know before the amendment you are trying to police.** A pattern that decides what to
protect will always be one un-tokenised sentence behind the author, and the failure is
silent: `ADD-ONLY: OK` reads identically whether nothing changed or nothing was checked.

⇒ **Protect EVERY line of the locked file, not a selected subset.** *"Additions pass; edits
and removals FAIL"* needs no pattern at all — it is a set relation:

```
every line of LOCKED (whitespace-normalised, blanks dropped) must appear in AMENDED
```

Additions still pass. Edits and removals still fail. **The token list disappears, and with it
the entire class of "the tool did not know that line mattered".** Reformatting an existing
line is then a FAIL — **correct**, because a reformatted bar line is indistinguishable from a
rewritten one to anything that has already been shown to misclassify.

**Two consequences that must be stated with it:**
1. ⛔ **`ADD-ONLY: OK` MEANS "NO TOKENISED BAR CHANGED" ON ALL 81 UNMIGRATED PREREGS.** It
   has now returned OK twice on a document whose decision rule was rewritten. **Until the
   set-relation form lands, an `ADD-ONLY: OK` line is not evidence and must not be cited as
   any** — including on `SCREEN-v140vs145`, whose A1/A2/A3 amendments are legitimate on the
   two-clock standard and on Magnus's directive, but are **NOT verified add-only by the tool
   that says they are.** *(The distinction matters: the amendments are almost certainly fine;
   the INSTRUMENT is what failed, and conflating those would be exactly the substitution this
   ruling is about.)*
2. **The side lane's own scoping correction is the durable half** and is adopted here: they
   migrated the presence and arithmetic layers onto real prereg text and left the amendment
   layer on the author's synthetic fixture, **where bars are tokenised by construction** —
   which is the same argument their §1 makes about empty declarations. **A forced-fail pass
   certifies the checks that exist against the inputs it used, and neither half of that is a
   property of the tool.**

**REVISED STATUS OF `c889633`: presence and arithmetic layers certified with three holes
(value bleed, empty-is-absent, and §1/§2 of this ruling uncovered); THE AMENDMENT LAYER IS
NOT CERTIFIED.**
