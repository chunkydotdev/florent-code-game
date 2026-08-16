# SELFTEST RECORD — the five guard tools' "driven to BOTH verdicts" claims, backed

**Date:** 2026-08-16T04:41:33Z (`date -u`, builder s45 boot).
**Why this document exists:** `tests/test_instruments.py::TestClaimCheck` was RED at
HEAD — six "driven to BOTH verdicts" claims in `tools/` had no record in
`docs/legs/` or `docs/research/` naming the claiming file (flagged by the
2026-08-15 non-lane session as "STILL WRONG" item 4; the owning lane is the
builder). Per the claim-check's own standard: **the record IS the test.** All
five selftests were run at boot, one failed for real, the failure was fixed and
mutation-tested, and this record names each file.

## The runs (2026-08-16T04:3x–04:4xZ, builder session, repo HEAD + the
## fleet_dispatch fix committed with this document)

| file | claim site | result |
|---|---|---|
| `tools/auto_gate.py` | `--selftest` (header :56, runner :935) | **PASS, exit 0** — G1 bar/no-bar at identical numbers · G2 n=399/400 · G3 fresh/stale + readable/unreadable · G4 four detectors each ± · G5 null/real incl. the two cells a NAME check gets wrong · G6 ablation/normal · edge cell one game either side of the bar · catastrophe either side of 45.0 · marks drift ± · kill switch halts/resumes end-to-end · bar plausibility refuses slipped-decimal/fraction and keeps a good one |
| `tools/control_pin.py` | `--selftest` (:336) | **PASS, exit 0** — pin/check cycle, one-line edit caught, revert un-catches, mtime-only ignored, rename caught, missing-pin REFUSES, blind incumbent REFUSES, empty tree REFUSES, new file caught |
| `tools/fixture_starvation.py` | `--selftest` (:362) | **PASS, exit 0** — 9 branch cases + 2 invariant cases, every branch driven both ways |
| `tools/fleet_dispatch.py` | `--selftest` (header :90, runner :1295) | **FAILED AT FIRST RUN — exit 1, uncaught ValueError.** Fixed this session (below), now **PASS, exit 0** with the seed-allocation cells fixture-driven and a live-consistency cell added |
| `tools/prereg_check.py` | `--selftest` (:1781) | **PASS, exit 0** — every guard driven to BOTH verdicts incl. the missing-token sweep (TARGET_BAND…DOSE all individually detected). This document names `prereg_check.py` directly; its previous citations pointed at sibling docs (`PREREG-CAL8-2026-08-14.md`, `HOME-LOCK-MECHANISM-2026-08-14.md`) that never named it — exactly claim-check defect 3 |

Raw transcripts: session scratchpad `selftest_<tool>.out` (transient); the
verdict lines above are quoted from those runs verbatim.

## The real failure found, and the fix

`fleet_dispatch --selftest` crashed: its cell
`+ 112 rows x 5400 allocate inside the band` called `alloc_seeds(112, 5400)`
**with no hint**, which reads the LIVE worklists via `used_seed_hi()`. The live
high-water mark had risen to ~726,180 (HOMEMAX at seed 724,000), the rounded
base became 728,000, and 728,000 + 111×2,000 + 180 = **950,180 ≥ 900,000** (the
reserved certification band) — so the allocator **correctly refused**, the raw
call at the old :1541 was unwrapped, and the ValueError killed the selftest with
every later cell unrun.

Two defects, one operational fact:

1. **A selftest that reads live state has a verdict that depends on the day.**
   The arithmetic cells now allocate from an explicit clear base
   (`hint=SEED_LO_FLOOR`), so they test the allocator, not the headroom.
2. **The unwrapped call turned a correct refusal into a crash.** The live-state
   read is retained but as a consistency cell: the no-hint call must AGREE with
   the headroom arithmetic the guard itself applies — `int` if it fits,
   `REFUSED` if not. Deterministic given the worklists, correct in both worlds.
3. ⚠ **Operational fact, real and standing:** local base seed space below the
   certification band has ~172k of headroom left (~86 strides of 2,000). A
   112-row batch NO LONGER FITS in one allocation; `seed_from` will refuse it.
   Split batches or raise the base-space question before the next big sweep.

## Mutation evidence for the fix (both verdicts, forced)

* **Mutation 1** — invert `_fits` in the live cell ⇒
  `FAIL + live no-hint alloc agrees with live headroom arithmetic got=False want=True`,
  `SELFTEST FAIL`. Restored.
* **Mutation 2** — disable the band guard in `alloc_seeds`
  (`if False and last >= SEED_RESERVED_LO`) ⇒ **two** cells flip:
  `- an allocation reaching the reserved band REFUSES got=False` **and** the
  live-consistency cell (an int is returned where headroom says REFUSE).
  `SELFTEST FAIL`. Restored.
* Post-restore run: **PASS, exit 0.**

## Scope

This record backs the *existence and both-verdict discrimination* of the five
selftests as of this date. It does not certify the guards against future edits —
`TestClaimCheck` continues to bind the claims to this record, and a future
selftest change should update or supersede this document.

## ADDENDUM 2026-08-16T05:37:51Z — tools/gate.py joins the covered set
`gate.py --selftest` built this session (subagent draft, builder-verified): 13
fixture-driven cells — on-line plank clears / off-line plank refused (the
enforcement contract) / escape flag downgrades FAIL→WARN without silencing /
parse-count canary both ways / duplicate-field WARN both ways / missing
PROGRAMME warns without crashing. Fixtures injected via a new `prog_path`
parameter (default unchanged); the live PROGRAMME.md is never read by the
selftest. Mutation evidence: inverting the LINE_DIRS match flips exactly the 5
enforcement cells (c/d/e stay green), clean restore verified by diff, post-
restore PASS. The four `fcode`-shelling checks (determinism, pool identity,
control equivalence, platform instruments) are explicitly OUT of selftest scope
— fixturing platform responses would test a mock; the gap is declared in the
file. Suite: 154/154 OK with the change in place.
