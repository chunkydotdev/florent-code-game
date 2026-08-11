# LEG — `tools/unrated_run.sh`: the abort guard, mutation-tested

**Written 2026-08-11 07:1x CEST by the s29 BUILDER (`date`, same shell call).**
This is the external record for the mutation-test claim in
`tools/unrated_run.sh`'s header. **The record IS the test** — that is
`tools/claim_check.py`'s rule and this document exists to satisfy it with
evidence rather than with a citation.

## WHY THIS FILE EXISTS AT ALL, WHICH IS THE INTERESTING PART

`tools/unrated_run.sh` is the **fourth copy** of the holder-assertion guard
(`fanout.sh`, `night_collector.sh`, `panel3_cal.sh` before it). The house rule,
written in `night_collector.sh`'s own header, is that **a copied guard carries a
copied CITATION and not a copied TEST.**

For its first hour this runner made **no claim**, so `claim_check.py` said
nothing about it — and the side lane pointed out, correctly, that **silence from
a checker whose predicate was never triggered is not evidence.** I then wrote the
mutation-test record into the file header, and `claim_check.py` **immediately
went red**:

```
$ .venv/bin/python -m unittest discover -s tests
FAIL: test_no_unbacked_claims_in_tools (test_instruments.TestClaimCheck)
Ran 34 tests in 0.850s
FAILED (failures=1)

$ .venv/bin/python tools/claim_check.py        # real exit, no pipe
  *** unrated_run.sh: claims a mutation test, NO record in docs/legs or
      docs/research names it
exit 1
```

**The checker fired on the same author, in the same session, within minutes of
the claim being made.** That is the loop working as designed, and it is the
reason this file is a `docs/legs` entry rather than a widening of
`claim_check.py` — **the worst day to loosen a guard is the day it first fires.**

## THE RECORD IS KEPT IN BOTH PLACES DELIBERATELY, BECAUSE THEY ARE NOT REDUNDANT

* **In the file header** — it **travels with the code**. The header says *"re-run
  it after any edit to the holder logic"*, which is read by the next person
  editing that logic. A `docs/` entry does not travel, and this repo has already
  logged what that costs: `docs/research/tactics/` reached 252 files with a
  decision-path citation rate of **zero**, and its own standing note warns that
  *"a bar assembled from three documents is one nobody re-reads before firing."*
* **Here** — it is **machine-checkable**, which is where `claim_check.py` looks.

**The usual argument for an external record is independence, and it is weak
here:** both records are written by the same author in the same commit. What
actually differs is **travel** versus **machine-checkability**, and neither
dominates — so both.

## THE TEST

**Mutation:** set `MAIN` to an incumbent that is not live, so the holder
assertion at the top of the runner must refuse. `MAIN` is overridable **solely**
so this branch is drivable.

```
2026-08-11 05:04:39Z    MAIN=999 zsh tools/unrated_run.sh 108 10
```

**Observed, verbatim:**
```
05:04:39Z UNRATED RUN  version=v108  target=10 games  incumbent=v999
05:04:39Z cells=5  outfile=scratchpad/arm_unrated_v108_20260811T050439Z.txt
05:04:40Z ABORT: expected incumbent v999, holder is 'v104 (Loki v2)'. Firing nothing.
```

**Three assertions, all checked:**

| assertion | result |
|---|---|
| prints ABORT naming both the expected and the observed holder | **yes** |
| **exit code 1** | **yes — checked WITHOUT a pipe** |
| **zero challenges fired**: the `arm_*.txt` outfile exists and is EMPTY | **yes, 0 bytes** |

**⚠ THE EXIT CODE WAS CHECKED WITHOUT A PIPE, AND THAT MATTERS.** The first
reading of this test was taken through `| tail -5` and returned **0**, because
`$?` behind a pipe is `tail`'s status. **A guard verified through a pipe reads
PASS unconditionally.** This is the same trap the repo logs against `fcode`
(`status` exits 0 while printing `Error: True`) and against
`plank_status.py --all | tail`. The real exit is **1**.

## RE-RUN AFTER THE GUARD-2/4/5 HARDENING

The rule is *"re-run after any edit to the holder logic"*, so it was applied to
its own file rather than asserted about it. After adding the numeric validation
on the rate meter's output and the bounded-wait fix to the pairing guard:

```
2026-08-11 07:0x Z   MAIN=999 zsh tools/unrated_run.sh 108 10
  -> ABORT printed, exit 1, arm file EMPTY. Same result.
```

**Also verified in the same run, both directions of the pairing guard** (guard 4,
which used to fail OPEN):
* unreadable JSON → **−1** → caller applies a bounded `GUARD_S` wait;
* healthy read → **281 s**, landing on the observed `:12:59` pairing — i.e. the
  period is **derived from recent rows, not hardcoded**, and the offset has
  shifted at least once in an 18-hour span so it must stay derived.

## WHAT THIS DOES NOT ESTABLISH

* It tests the **pre-flight** holder assertion. The **mid-run** assertion and the
  4-try `restore()` path are **not** driven by this test — they require a live
  activation to reach, and driving them costs real rated exposure.
* It says nothing about whether the runner's **pacing** is correct, only that it
  refuses to fire when the ladder is not on the expected incumbent.
* `corpus/HOLDER_ALERT` is written only on `restore()` failure, which this test
  never reaches. **That branch remains untested.**
