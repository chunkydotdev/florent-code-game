# MUTATION-TEST RECORD — inert_check.py · match_ledger.py · match_diffcheck.py

**Run 2026-08-13T17:09:19Z (`date -u`), builder s37, at boot.** This document
exists because `tools/claim_check.py` (correctly) flagged all three files at
s37 boot: each claimed a mutation test whose record either lived only inside
the file itself or cited a sibling document that never names the file. Per the
check's own remedy — *"commit the record (the record IS the test)"* — every
mutation was **re-run fresh today**, not transcribed from the in-file claims.
All observed outputs below are from today's runs on scratch copies
(`mktemp -d`); `tools/` was never mutated.

## 1. `tools/inert_check.py`

Baseline (unmutated) immediately before the mutations:
`INERT_CHECK_SELFTEST: PASS` — 5 cells passed, 0 failed.

**MUTATION A** (per the recipe in the file's docstring): widen the
intersection `hit = reads_norm & touches_norm` to a union
(`|`) — the gate-that-cannot-say-no class. Observed today:

    4 cells passed, 1 failed, over 5 cells
      FAILED: NEGATIVE_loki18: expected INERT, got PASS
    INERT_CHECK_SELFTEST: FAIL

**MUTATION B**: replace the malformed-block guard (the code block at
`inert_check.py:336`, the one followed by `missing = []` — NOT the docstring
copy of the same lines at ~154, which a first attempt today edited by mistake
and which correctly changed nothing) with silent empty-list defaults.
Observed today:

    4 cells passed, 1 failed, over 5 cells
      FAILED: MALFORMED_NO_BLOCK: expected MALFORMED, got INERT
    INERT_CHECK_SELFTEST: FAIL

Both flips match the file's 2026-08-11 in-file record cell-for-cell. The
first-attempt note is kept deliberately: a mutation that edits documentation
and still "runs" is a mutation test that tested nothing, and the PASS it
produced was the alarm.

## 2. `tools/match_ledger.py`

Baseline: `MATCH_LEDGER_SELFTEST: PASS` — all cells.

**MUTATION (a)** (verbatim recipe from the file's tail comment): fabricate a
matchId when the body has none — exit-code-style acceptance. Observed today:

    [FAIL] REJECTED on bodyless response            match_id='FAKE-ACCEPTED-BY-RC'
    [FAIL] EXIT-CODE TRAP: rc=0 valid-JSON Error:True -> still REJECTED match_id='FAKE-ACCEPTED-BY-RC' (rc=0 ignored by design)
    MATCH_LEDGER_SELFTEST: FAIL

**MUTATION (b)** (verbatim recipe): flip preflight's missing-parent branch
from `return False, "BLIND: …"` to `return True, "BLIND: …"` — a refusal that
looks like a refusal in text but reports healthy. Observed today:

    [FAIL] BLIND REFUSES: missing parent dir, subprocess exit code returncode=0
    MATCH_LEDGER_SELFTEST: FAIL

Both flips match the file's 2026-08-11 in-file record.

## 3. `tools/dash/match_diffcheck.py`

Its `--selftest` is itself mutation-shaped: it corrupts one input per
comparison and asserts that comparison fires (each branch is a function so the
selftest drives *the check*, not a copy of its expectations). Run today:

    E  compare the same stamps against UTC instead of local -> 1721 mismatch(es) OK
    D  plant 'win rate … pooled' in a value  -> 2 mismatch(es) OK
    SELFTEST OK — every exercised comparison produced the other verdict
    VERDICT: PASS — the match view's values equal the TSV columns behind them

This document is the record naming that file, which is what was missing.

## Not covered here, deliberately

`tools/vps/selftest.sh` was also flagged. It is an **untracked, untested
draft** from the killed s36 VPS agent (s36 wrap: "do NOT trust them
untested"). Its claim wording was removed instead of backed — an untested
draft does not get a record, it gets its claim deleted.
