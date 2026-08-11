# SPEC — the mutation harness: prove each selftest can fail for the right reason

**Side lane, 2026-08-11, commissioned by Magnus** (*"whenever we find issues that
would have been fixed by a deterministic script or harness tool, we should build
that tool so it never happens again"*). **Builder-owned to implement — `tools/`
is not this lane's surface.** This is a buildable spec, not a proposal: the
acceptance fixtures are six defects already confirmed and already mutated by
hand today (`SWEEP-green-selftests-2026-08-11.md`).

---

## 1. THE MEASURED CASE, NOT THE ARGUMENT

Of ~15 selftests under `tools/`, **six passed while the metric underneath them
was broken.** Two were live at the moment of discovery: `audit_trigger` was
suppressing its own FIRE, and `oppver_window` was returning **CLEAN** — the
verdict that certifies D18 — off a stale tape.

**Coverage is not the binding constraint. Fidelity is.** A test that has never
been shown able to fail for the right reason is a document with an exit code.

**The sweep that found all six was a MANUAL mutation test, run by hand six
times.** This spec automates exactly that and nothing more.

## 2. WHAT IT DOES

For each declared mutant: copy the module to scratch, reintroduce the specific
defect its selftest exists to prevent, run that selftest, and **assert the
selftest FAILS.** A selftest that still passes is reported as BLIND.

## 3. THE ONE DESIGN DECISION THAT MATTERS: MUTANTS ARE DECLARED, NOT GENERATED

**Do not use generic mutation testing** (operator flips, `mutmut`-style). Every
one of the six defects was **semantic — the removal of a load-bearing clause**,
not an off-by-one:

| defect | the clause removed |
|---|---|
| `ring_retention` | the entity-kind filter (barriers counted as bodies) |
| `audit_trigger` | the window on the denominator |
| `map_admits` | 12-tile ring → orthogonal-8 in `map_facts` |
| `breakin_watch` | the freshness branch in `main()` |
| `replay_throws` | `if kind == "INSERT"` gating what enters `active` |
| `oppver_window` | the tape's freshness → stale routes to CLEAN not UNKNOWN |

Generic mutation would bury these in thousands of noise mutants. **Each
instrument declares its own, and each declared mutant carries the incident that
created it** — the same standard `EXPERIMENT-METHOD-CHANGELOG.md` applies to
rules: *a mutant without an incident is a preference.*

### Declaration format

`tests/mutants/<module>.py`, beside the suite that already exists:

```python
MUTANTS = [
    {
      "target":   "tools/ring_retention.py",
      "name":     "no-entity-kind-filter",
      "incident": "s28/s29: counted barriers as bodies; 66.4% of 'occupancy' was
                   not a body and it FLIPPED THE SIGN (fjordgate -0.201 vs +0.182)",
      "find":     'if kind_of.get(eid) == "builder_bot":',
      "replace":  "if True:",
      "expect":   "SELFTEST_FAILS",
    },
]
```

Plain textual substitution on a scratch copy. **That is what worked six times by
hand; nothing cleverer is required and anything cleverer adds a failure mode.**

## 4. ALGORITHM, WITH THE TWO BRANCHES THAT ARE EASY TO GET WRONG

1. Copy the target module (and its package dir) into a scratch tree.
2. Apply the substitution.
   **⛔ If `find` does not occur exactly once → ERROR, not skip.** A mutant that
   no longer applies means the code moved underneath it. **A silently skipped
   mutant is a green light that proves nothing** — the same failure class as a
   constant column. Report as `STALE MUTANT`, exit non-zero.
3. Run that module's selftest **inside the scratch copy**.
4. **Verdict gates on BOTH a non-zero exit AND the absence of the `PASS` token**,
   never on `$?` alone — the standing `fcode status` rule (`exit 0` while
   printing `Error: True`) applies to our own tools. A selftest that crashes for
   an unrelated reason must not be scored as a catch: require the failure to
   name the mutated check where the selftest prints per-case lines.
5. Emit one line per mutant: `CAUGHT` / **`BLIND`** / `STALE MUTANT`.

## 5. THE HARNESS MUST BE RUN AGAINST A CASE IT MUST GET WRONG

**A harness that has only ever reported CAUGHT has not been seen to check.** Its
own selftest must drive both verdicts:

* **positive control — must report CAUGHT:** mutate a bucket boundary in
  `tools/score.py`, whose selftest asserts both sides of every boundary. If the
  harness reports BLIND here, the harness is broken.
* **negative control — must report BLIND:** the `map_admits` orthogonal-8 mutant
  in `map_facts()`. Its selftest builds its own ring inline and **passes**;
  confirmed by hand today. If the harness reports CAUGHT here, it is reading the
  wrong signal.

**Both fixtures already exist and both verdicts are already known.** The harness
ships with a proven ability to produce each.

## 6. ACCEPTANCE FIXTURES — the six, with their known answers

Build is complete when the harness independently reproduces these:

| # | target | mutant | expected |
|---|---|---|---|
| 1 | `ring_retention.py` | drop the entity-kind filter | **BLIND** (selftest passes; asserts only ring geometry) |
| 2 | `map_admits.py` | orthogonal-8 ring inside `map_facts()` | **BLIND** (selftest builds its own ring) |
| 3 | `breakin_watch.py` | delete the freshness branch from `main()` | **BLIND** (selftest tests a private copy) |
| 4 | `audit_trigger.py` | remove the window from the numerator | **BLIND** (one-row fixture makes both windows coincide) |
| 5 | `oppver_window.py` | force a stale tape | **BLIND** (`_OVERRIDE["timeline"]` bypasses the reader) |
| 6 | `score.py` | move a bucket edge | **CAUGHT** — the control that proves the harness works |

**Five BLIND and one CAUGHT is the acceptance signature.** A harness returning
six CAUGHT or six BLIND is wrong regardless of which looks better.

## 7. COVERAGE CENSUS — ship it in the same tool, it is three lines

Two failure states, reported separately because they are different:

* **NO SELFTEST:** 41 of 56 `__main__`-bearing modules under `tools/`, including
  `replay_census.py` (**84 doc mentions**, the wire primitives every corpus
  decoder imports — one defect there moves every number in the repo),
  `leg_read.py` (13), `corpus_sanity.py` (9), `gate.py` (an enforcement
  instrument never observed to refuse).
* **SELFTEST BUT NO DECLARED MUTANT:** untested fidelity — which is the state all
  fifteen were in this morning.

**An instrument with no test is not a smaller problem than one with a blind
test; it is the same problem without the false assurance.**

## 8. WHERE IT RUNS

The full sweep is not a boot check — it forks a process per mutant. Proposal:
**boot runs the CENSUS** (instant, and it is the number that shames the backlog),
and the **full mutation sweep runs on demand and before any instrument's output
is cited in a verdict.** The natural enforcement hook already exists:
`claim_check.py` already refuses a "mutation-tested" claim that does not point at
its own record — extend it to require a harness record for any instrument a
document cites.

## 9. TWO SIBLING TOOLS FROM THE SAME DAY, CHEAPER PER LINE THAN THIS ONE

**(a) ONE SHARED FRESHNESS ASSERTION.** `audit_trigger`, `oppver_window`,
`breakin_watch` and `ship_watch` are the same bug four times: an instrument reads
a file and never reports the age of its newest row. **CLAUDE.md already states
the rule and nothing enforces it.** One helper — `assert_fresh(path, max_age)`
returning the age and refusing past N cadences — plus one mutant per consumer.
**Highest value per line of anything in this document.**

**(b) CONTRACT ASSERTIONS THAT FAIL CLOSED.** `rate_budget.py` attributes our
spend by globbing `scratchpad/arm_*.txt`. A hand-rolled runner wrote
`loki19_ctrl_w1.txt`, the meter read *"0/5, a slot is free NOW"* twice — the
second time immediately after all five challenges had been rejected by the limit
it exists to track — and **the LOKI-19 treatment window was lost.** Renaming the
file flipped the reading to 5/5 with no code change.

**The repair landed as a printed warning, and the tool now has TWO blindnesses
routed opposite ways:** an unreadable body → `--wait` returns **1200** (fails
closed, asserted in its selftest); an unattributable in-window match → `--wait`
returns **0** (fails open), with the warning on the human path only while
`night_collector.sh` and every other runner consume the integer. **Route the
second into the first.** General form: **an implicit contract encoded in a
filename or a glob must be a named constant the producers import, and its
violation must fail CLOSED.**

## 10. WHAT NONE OF THIS CATCHES — stated so the harness is not oversold

**Most of 2026-08-11's damage was not test-shaped.** A 45° angle tolerance
compared against an exact-ray predicate; rated arrival compared against unrated;
a denominator pooling our own experiments into an opponent's record; a bar
calibrated on one granularity and read on another. **In every case both programs
were correct and were measuring different quantities.** No assertion catches
*"you compared the right number to the wrong number."*

What catches those is the in-arm rule (**measure both sides inside the arm being
tested; never size anything on a stored figure**) and another lane re-deriving
the arithmetic. **Three of today's corrections came from a peer re-deriving a
number, not from reviewing an argument.** That is an argument for duplication
between lanes, and it is not automatable by this or any harness.
