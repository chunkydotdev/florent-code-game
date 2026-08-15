# RECORD — mutation tests on the instruments built 2026-08-15

**Written 2026-08-15 (`date -u`), non-lane usability session.** This is the
evidence file `tools/claim_check.py` requires: every tool below asserts a
mutation test in its docstring, and **the record IS the test** — a claim without
this file is an assertion.

Each entry states: the guard, the mutation applied, and **the verdict it
produced in BOTH directions**. A guard only ever watched to FIRE has not been
watched to PASS, and vice versa.

---

## `tools/now.py` — the canonical state block

**Guard: a degraded `fcode status` must go BLIND, not invent a holder.**
This is the case that exits 0 and parses as valid JSON while carrying no
`active_submission` (CLAUDE.md, measured in the 2026-08-10 outage), so neither
the exit code nor parseability can detect it.

| mutation | expected | observed |
|---|---|---|
| healthy body (holder present) | rc 0, prints `HOLDER v151`, no `BLIND` | ✅ as expected |
| `active_submission` absent | **rc 2**, prints `⛔ BLIND`, **no holder line** | ✅ as expected |

The third assertion is the one that matters: **`"HOLDER v" in output` is False**
under the degraded case. A version that fell back to `ship_watch` would still
print a holder and would pass a rc-only check.

**Guard: staleness must change the rendering on the same code path.**
Same file, two clock values: fresh → no `STALE` tag; `2026-08-01` → `STALE`.
Both verdicts observed. Selftest: **8/8**.

---

## `tools/fleet_health.py` — what is supposed to be running

**Guard: MISSING and DUPLICATE are distinct, and land on the right row.**

| mutation | expected | observed |
|---|---|---|
| all daemons present once | 0 problems, no row MISSING | ✅ |
| supervisor removed | 1 problem, and it is **`corefill_forever`** | ✅ |
| second `auto_gate` added | 1 problem, classified **DUPLICATE** not MISSING | ✅ |
| both faults at once (the real 2026-08-15 state) | **2 problems** | ✅ |
| zero shard runners | **0 problems** (informational row) | ✅ |
| process table unreadable | **rc 2 UNKNOWN**, not "everything missing" | ✅ |

**Guard: oldest-first ordering, so the kill advice names the NEWCOMER.**
Mutation: a duplicate with `age=5` against an established `age≈10,000`.
Expected `pids[0] != 555` and `pids[1:] == [555]`; both observed. ⭐ **This cell
exists because the first version ordered by `ps` output and would have told a
reader to kill the ESTABLISHED daemon (up 7h26m) and keep the 3h19m one.**

**Guard: a loop wrapper and its own child are ONE, not a duplicate.**
Mutation: inject `(pid 700, "python .../replay_archiver.py", ppid=<wrapper>)`.
Expected 0 problems and `found=1`; both observed. **Control that keeps it from
being inert:** a *genuine* second wrapper (`ppid=1`) must still read DUPLICATE —
observed 1 problem. ⛔ **Without the control this fix would have suppressed real
duplicates too.** Selftest: **14/14**.

---

## `tools/freshness.py` — the `Z`-marker rule

**Guard: an explicit `Z` overrides the caller's `assume_local`.**
The load-bearing pair uses **one clock value and one caller**, so the verdicts
cannot agree by accident (`now = 12:00Z`, limit 6h):

| row | reading | verdict |
|---|---|---|
| `2026-08-11T07:30Z` + `assume_local=True` | marker wins → 4.5h | **FRESH** ✅ |
| `2026-08-11T07:30` + `assume_local=True` | naive → CEST → 6.5h | **STALE** ✅ |

**Direct mutation, run in-process:** `_parse` was monkey-patched to discard the
marker (the pre-fix behaviour) and the same file flipped `True → False`. ⇒ the
marker is **load-bearing**, not decorative. Selftest: **16/16**.

---

## The `--help` contract (`tests/test_instruments.py::TestHelpContract`)

**Guard: `--help` must be safe, describe the tool, and exit 0 — across all 86
`tools/*.py`.**

| mutation | expected | observed |
|---|---|---|
| strip the guard from `leg_read.py` | test FAILS | ⛔ **PASSED at first** — see below |
| un-gate the guard in `freshness.py` (`if True:`) | import test FAILS | ✅ failed correctly |

⭐ **THE FIRST MUTATION EXPOSED A HOLE IN THE TEST ITSELF, and it is the reason
this section exists.** With the guard stripped, `leg_read.py --help` prints
`LEG: no completed games` — **exit 0, non-empty stdout, no file writes**. All
three original assertions stayed green. **Exit code and non-emptiness cannot
distinguish "printed its help" from "ran for real and printed a verdict", which
is exactly the defect the contract exists to prevent.**

⇒ A fourth assertion was added: the output must contain `usage:` **or** the
tool's own docstring head (read via `ast`, without importing). Re-run, the
mutation now fails with:
`leg_read.py: --help printed something that is neither a usage line nor its
docstring ('LEG: no completed games…') — it probably RAN`.

**Also mutation-relevant: the false-positive control.** The test's
filesystem-write assertion first accused `game_census`, `stub_engine` and
`triarm_read` of writing `corpus/ship_watch.log`, `corpus/vps_pull.log` and
`scratchpad/corefill.log` — **files none of them opens.** They are written by the
live daemons. Fixed with a background-churn control window plus a named
`DAEMON_WRITTEN` list. ⚠ **This is the repo's own "a measurement of a moving base
is a measurement onto a snapshot" (side-lane retro s43, Q4) landing on a test
written the same day.**

---

## `tools/audit_trigger.py` — blind ≠ healthy

**Guard: a cell that cannot evaluate is UNKNOWN, not "not tripped".**

| mutation | expected | observed |
|---|---|---|
| all cells healthy | `OK — n/6 tripped`, **rc 0** | ✅ |
| inject `raise RuntimeError` into one cell | `[BLIND]` + `UNKNOWN … Not a clean bill of health`, **rc 2** | ✅ |

**Found by accident and worth recording as such:** a real `NameError` I
introduced produced `[skip] ship cadence: name 'timezone' is not defined` and
the summary then read **`OK — 0/6 tripped; audit not indicated`**. The one cell
that *was* tripping had gone silent and **the verdict got healthier for being
blind** — inside the boot check whose job is to notice exactly that.

---

## What is NOT covered here

`tools/watchdog.sh` has **no `--selftest`** and is verified only by the live
end-to-end runs recorded in the commit message (kill the supervisor → launchd
restarts it → survives 36s past job exit). ⚠ **That is weaker than the cells
above and is stated rather than implied.** Its `AbandonProcessGroup` dependency
was found by observation, not by a test, and nothing currently fails if that key
is removed from the plist — a named gap, not a covered one.
