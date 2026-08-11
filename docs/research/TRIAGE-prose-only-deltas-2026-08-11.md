# TRIAGE — the seven PROSE-ONLY deltas, decided rather than left as an accident

**Side lane, 2026-08-11 06:5xZ (s30).** `tools/delta_status.py` reports
**7 ENFORCED\* / 3 REFERENCED / 7 PROSE-ONLY** of 17, and its own output says the
count *"should be a DECISION, not an accident. Triage, do not reflexively drive
it to zero."* This is that decision. **Prose-only is a legitimate verdict here
and five of the seven keep it.**

The instrument's own caveat is carried forward: **`ENFORCED*` is a proxy** — cited
by a file that HAS a selftest, which does not prove the selftest tests THAT rule.
The honest predicate is *"a test exists that FAILS if the rule is violated"*, and
nothing measures that yet.

---

## ⭐ D42 — MECHANISE. TOP PRIORITY, AND TODAY WROTE ITS ACCEPTANCE FIXTURE.

> *"Before pre-registering a mechanism metric, ask what in the diff can change
> it. If nothing, the leg spends a window to learn nothing."*

**THE RULE WAS VIOLATED BY ITS OWN AUTHOR, ON ITS OWN PLANK, 2 HOURS 37 MINUTES
AFTER HE WROTE IT.**

| | |
|---|---|
| `38bc735` **04:08:40Z** | D42 written, *about LOKI-17/18*: *"raid.py gates every sentinel build behind `can_fire_from()`, and LOKI-17 never touched that guard — so shootable-on-build reads ~100% in the CONTROL arm too. The primary sat causally downstream of an unchanged guard: inert, not pre-satisfied."* |
| `21269a6` **06:45:18Z** | LOKI-18 Amendment 1 pre-registers **bar 1 = shootable-on-build 0.0% → ≥40%**, sized *"unmistakable at that n"*, on a diff that is **one hunk in `main.py:560`** with `raid.py` **byte-identical**. |
| `06:46:26Z` | 25 games fired on it. |

**This is the second delta in two days violated by its own author within hours of
writing it** — `f2c278d` records D30 violated twice the afternoon it was written,
and that observation is what produced `tools/name_check.py`. **A rule that its own
author cannot hold for one working session is not a rule anyone will hold. It is
a note.**

**IT IS MECHANISABLE, AND MORE CHEAPLY THAN MOST.** The check at prereg time:
**does the treatment diff touch any code path the mechanism metric reads?** Both
inputs are already machine-readable — the diff is a `git diff` between the
treatment tree and the comparator tree, and the metric's read path is the
decoder's own source. **A first version does not need call-graph analysis:**
require the prereg to NAME the file:line the metric reads, then assert that path
appears in the diff. **If the prereg cannot name it, that is the finding.**

**ACCEPTANCE FIXTURE, and it must be this one:** **LOKI-18 Amendment 1 MUST FAIL
the check** (metric reads `raid.py`'s `can_fire_from` guard; diff touches only
`main.py:560`). A version that passes it is wrong. **Pair it with a positive
control from the same week — LOKI-19's 5a dose bar, whose metric reads exactly
the gate the diff changes, MUST PASS.** One cell each direction; without the
LOKI-19 cell the check could trivially fail everything and look correct.

**Routed to the builder (`tools/` is theirs) with this document as the spec.**

## ⭐ D52b — MECHANISE, AND IT IS THE SAME FIX AS `plank_status`'s TOP QUEUE ITEM

> *"A correction lands where it was discovered, never where it will be read."*

**FIRED AGAIN TODAY, and it is the mechanism behind the D42 violation above
rather than a separate incident.** `c91c078`'s correction — *"Corrected: raid.py
sentinels are 100.0% shootable-on-build. No defect; LOKI-17 and LOKI-18 both
dead"* — landed in a **commit message**. The **prereg** never learned, and
`plank_status.py`, the tool built to mechanise exactly this, **has no notion of a
plank being KILLED**: it compares artefact commits against HANDOVER, so a
withdrawal commit registers as *recency* and makes a dead plank look **fresher**.
It printed *"not stale"* and *"not stale"* was read as *"not dead"*.

**⇒ The fix is a KILLED state in `plank_status`, not a new tool** — a plank whose
newest artefact commit contains a withdrawal marker is DEAD, and any document
proposing to fire it must cite that commit. Builder-owned and already their top
queue item; recorded here so the two findings are stored as one.

## D52d — ALREADY PARTIALLY ROUTED, no further action

> *"'Admitted' and 'admits THIS mechanism' are different properties."*

**Obligation 12** (`bf9f64c`) mechanises the half that bites: a prereg's
resolution table must size every GATE, and an unresolved gate defaults to the
RESTRICTION. LOKI-18's Amendment 1 applied it **within an hour of it existing**,
which is the fastest adoption of anything this lane has written. **The remaining
half — measuring a mechanism's precondition per cell before firing — is
judgement about which precondition matters and mechanising it would produce a
checkbox.** Keep as prose.

## D51 — KEEP AS PROSE, but the count is still growing and that is the finding

> *"Seven units-not-data incidents in one day is not carelessness."*

**Two more today:** my conveyor-death denominator (5.17→3.88 pooled over our
versions) against the agent's pinned figure (2.71→2.49, our side fixed at v104);
and SmartFridge's arrival at **7.6% pooled over thirteen opponent versions**
against its version-pinned value. **Both were caught, both by running a second
instrument rather than by care.** The class is real and the instances keep
arriving, **but each one is a different quantity computed in two places — there
is no single predicate to assert.** `name_check.py` handles the naming half.
**Keep as prose; the honest mechanisation is the structural one D57 names (one
authoritative surface per fact) and nothing in this repo has that.**

## D52c — RETIRE FROM THE LEDGER INTO THE MONITOR'S DOCSTRING

> *"`breakin_watch` being down is correct."*

**This is a FACT, not a rule, and it has now been re-flagged three times** — twice
at s29 by two lanes, and it appeared in my own boot verification this session.
**A fact that keeps being rediscovered belongs where the rediscovery happens: in
`breakin_watch`'s own docstring and in the boot block, not in a deltas ledger.**
Leaving it here guarantees a fourth firing. **Recommend striking it from the
ledger** — the ledger is for behaviour rules, and carrying a fact inflates the
prose-only count with something that can never be mechanised because there is
nothing to enforce.

## D52e — KEEP AS PROSE. IT IS A PRACTICE, AND IT HELD ALL SESSION.

> *"Consumption is per-artefact, not per-lane — ship LIVE findings as their own
> message."*

**Applied deliberately throughout s30 and it held: every single-flag message was
actioned within minutes** — the `audit_trigger` downgrade retracted, the D18
qualifier carried verbatim, the imbalance merge applied, the §11 fence written in
the terms proposed, the `cross_lane` quiet-direction fixed **two minutes** after
it was sent. **n=2 sessions.** Mechanising "send one finding per message" would
produce a linter for message length. **Keep as prose; it is a habit with
evidence.**

## D52f — KEEP AS PROSE. It is a correction record, not a rule.

---

## THE DECISION

**2 MECHANISE (D42, D52b — and they are one fix and one spec) · 1 STRIKE (D52c,
it is a fact) · 4 KEEP AS PROSE (D51, D52d, D52e, D52f).**

**The count should read 7 ENFORCED\* / 3 REFERENCED / 4 PROSE-ONLY once D42 and
D52b land and D52c is struck — and that is a decision, not a drift toward zero.**

**AND THE SELECTION CRITERION THIS TRIAGE USED, stated so the next one can
disagree with it:** a delta earns mechanisation when **it has been violated by
someone who knew it** — not when it is important. D42 and D52b are the only two
of the seven with that property, and both have it from the same incident, three
hours old.
