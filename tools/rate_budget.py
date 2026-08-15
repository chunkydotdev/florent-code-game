#!/usr/bin/env python3
"""RATE BUDGET METER — how much of the 5-per-20-minutes is left, measured.

    .venv/bin/python tools/rate_budget.py              # human read
    .venv/bin/python tools/rate_budget.py --wait       # seconds to wait, one int
    .venv/bin/python tools/rate_budget.py --selftest   # prove it reads both ways

IMPLEMENTS: D45 (an actor must not learn its own actions by observing the
world -- the platform read is a cross-check, the actor's ledger is authority).

WHY THIS EXISTS (s28). The unrated/test rate limit is **5 per 20 minutes, shared
across every runner and every lane**, and NOTHING in `fcode status` reports how
much of it is left. So each runner models a resource it cannot observe, and the
error that follows is not a discipline failure — it is the only thing an
unobservable budget permits.

It bit immediately: PANEL2-CAL was paused at 13:45:58Z having just spent all 5,
LOKI-14b was started at 13:49:57Z, and its first challenge was rejected.
**Pausing a runner does not refund the budget it already spent.**

**THIS METER READS THE PLATFORM, NOT A LOCAL LEDGER.** `fcode match list --mine`
returns `triggeredBy` ("unrated" / "test" / "ladder") and `createdAt` per match,
so the spend is *measured on the authority that enforces the limit* rather than
tallied in a file that drifts the moment a runner dies mid-window, is restarted,
or is run from another lane. A local ledger would have been the obvious build and
would have been wrong in exactly the way this project keeps being wrong: a record
of what we THINK we fired is not evidence of what the platform COUNTED.

**⚠ THE METER IS A LOWER BOUND, AND THIS IS LOAD-BEARING.** `CLAUDE.md` records
that REJECTED attempts appear to count against the limit, and a rejected attempt
creates no match — so it is invisible here. **A reading of "2 spent" can mean 2
accepted plus an unknown number of rejects.** Treat the answer as "at least this
much is spent"; never as permission. The wait it prints is a floor.

GATING: per the s27 D26 rule, this reads the load-bearing FIELD (`matches` in the
JSON body) and never the exit code — `fcode` exits 0 while printing `Error: True`
and exits 1 on a healthy list, both observed the same day.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ---- `--help` CONTRACT (enforced by tests/test_instruments.py) --------------
# Side-effect-free, prints this module's docstring, exits 0.
#
# ⛔ WHY. Probing an unknown tool with `--help` is the first thing anyone does.
# Before 2026-08-15, 40 of 86 tools here had no argparse, so `--help` was just an
# unrecognised argument and THE TOOL RAN FOR REAL -- printing VERDICT-SHAPED text
# that reads as a finding:
#     tools/freshness.py --help  ->  "BLIND: --help has no parseable timestamp"
#     tools/leg_read.py  --help  ->  "LEG: no completed games"
# Both are this repo's own verdict vocabulary. A reader asking a harmless
# question got an authoritative-looking sentence about nothing.
#
# ⛔ GATED ON `__main__`: several of these modules are IMPORTED by other tools
# (freshness by now.py). Ungated, this would fire during that import and make the
# PARENT exit 0 mid-run while printing the CHILD's docstring.
# ⛔ SELF-CONTAINED `import sys`: a first attempt used the file's own import, and
# broke on `import sys as _sys` (NameError) and on files whose imports come in
# two blocks. The guard must not depend on what the host file happens to import.
if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__ + "  (no module docstring)"))
        raise SystemExit(0)

ROOT = Path(__file__).resolve().parent.parent
FCODE = str(ROOT / ".venv" / "bin" / "fcode")

WINDOW_MIN = 20          # measured off the CLI 2026-08-10; was 10 before that
LIMIT = 5

_OVERRIDE: dict = {}     # tests inject {"matches": [...], "now": datetime}


def _our_ids() -> set[str]:
    """Match ids WE challenged, from the runners' own outfiles.

    ATTRIBUTION IS REQUIRED AND THE PLATFORM DOES NOT SUPPLY IT. `--mine`
    returns every match we PARTICIPATED in, and opponents challenge US in
    unrated matches -- measured 2026-08-10: of 7 unrated matches in one
    20-minute window, **2 were Banminary challenging us**, which spend none of
    our budget. Without attribution the meter read 7/5, i.e. an impossible
    number, which is the only reason the flaw was visible at all. Had exactly
    one foreign challenge landed it would have read a plausible 5/5 and simply
    stalled every runner.
    `triggeredBy` is the match TYPE, not the actor, and `sourceMatch*Id` are
    null -- so the only honest attribution is the id the platform handed back
    when WE fired, which the runners append to their arm files.
    """
    if "our_ids" in _OVERRIDE:
        return _OVERRIDE["our_ids"]
    ids: set[str] = set()
    for f in (ROOT / "scratchpad").glob("arm_*.txt"):
        try:
            for m in re.findall(r'"matchId": "([0-9a-f-]+)"', f.read_text()):
                ids.add(m)
        except OSError:
            continue
    return ids


def _fetch() -> list[dict] | None:
    if "matches" in _OVERRIDE:
        return _OVERRIDE["matches"]
    r = subprocess.run([FCODE, "match", "list", "--mine", "--json", "--limit", "40"],
                       capture_output=True, text=True)
    body = r.stdout[r.stdout.find("{"):] if "{" in r.stdout else ""
    if not body:
        return None
    try:
        d = json.loads(body)
    except json.JSONDecodeError:
        return None
    # THE LOAD-BEARING FIELD, not the exit code.
    return d.get("matches") if isinstance(d.get("matches"), list) else None


def spend(now: datetime | None = None) -> tuple[int, list[datetime], bool, list]:
    """(spent, sorted challenge times inside the window, meter_ok, unattributed).

    `unattributed` is the in-window unrated matches we could not tie to any
    `scratchpad/arm_*.txt`. It is returned SEPARATELY rather than folded into
    the count, because the two readings are genuinely different -- but
    `wait_seconds()` treats it as OURS, deliberately. See there."""
    now = now or _OVERRIDE.get("now") or datetime.now(timezone.utc)
    matches = _fetch()
    if matches is None:
        return 0, [], False, []
    cutoff = now - timedelta(minutes=WINDOW_MIN)
    mine = _our_ids()
    hits = []
    unattributed: list = []
    for m in matches:
        if m.get("triggeredBy") not in ("unrated", "test"):
            continue
        if m.get("id") not in mine:
            # ⚠ UNATTRIBUTED. Two very different things land here and they look
            # identical: an opponent challenged US (spends nothing of ours), or
            # WE fired from a runner that did not write its ids to
            # `scratchpad/arm_*.txt`. The second is a SILENT UNDERCOUNT and it
            # makes the meter report free slots into a spent window.
            #
            # MEASURED s29 2026-08-11: a hand-rolled leg runner wrote its
            # outfile as `loki19_ctrl_w1.txt` instead of `arm_loki19_ctrl_w1.txt`.
            # The meter read `0/5, a slot is free NOW` twice -- once immediately
            # before the next window and once immediately after all five of its
            # challenges were REJECTED -- and the treatment window was lost.
            # Renaming the file alone flipped the reading to 5/5.
            #
            # So the count stays honest (we cannot prove it was ours) but the
            # meter now REPORTS ITS OWN BLINDNESS, per the standing rule that a
            # monitor which cannot see must not look identical to one that can.
            ts_u = m.get("createdAt")
            if ts_u:
                try:
                    w = datetime.fromisoformat(ts_u.replace("Z", "+00:00"))
                    if w >= cutoff:
                        unattributed.append(w)
                except ValueError:
                    pass
            continue                     # an opponent challenged US: not our spend
        ts = m.get("createdAt")
        if not ts:
            continue
        try:
            when = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except ValueError:
            continue
        if when >= cutoff:
            hits.append(when)
    return len(hits), sorted(hits), True, sorted(unattributed)


def wait_seconds(now: datetime | None = None) -> int:
    """Seconds until at least one slot frees. 0 if a slot is free NOW."""
    now = now or _OVERRIDE.get("now") or datetime.now(timezone.utc)
    n, times, ok, unattr = spend(now)
    if not ok:
        return WINDOW_MIN * 60          # meter blind -> assume the worst
    # ⛔ THE SECOND BLIND STATE, AND IT USED TO FAIL OPEN. An in-window unrated
    # match we cannot attribute is EITHER an opponent challenging us (spends
    # nothing of ours) OR a runner of ours not writing scratchpad/arm_*.txt.
    # Those are indistinguishable here, and only one of them is safe.
    #
    # Until s29 this branch printed a warning on the HUMAN path and left the
    # integer alone -- but `--wait` is the MACHINE path and returns before any
    # message is printed, so every runner (night_collector, panel3_cal,
    # loki14b_leg) read GO and the warning reached nobody. That is precisely the
    # asymmetry that cost the LOKI-19 treatment window: the meter said "0/5, a
    # slot is free NOW" twice, the second time immediately after all five
    # challenges had been rejected.
    #
    # So unattributed matches now COUNT AS OURS for the wait. This can over-wait
    # when an opponent really did challenge us -- measured as 2 of 7 once -- and
    # that is the trade taken deliberately: over-waiting costs latency, under-
    # waiting costs a whole window AND spends budget on rejects, which count.
    # The human read still prints both numbers separately so the split is visible.
    combined = sorted(times + unattr)
    if len(combined) < LIMIT:
        return 0
    free_at = combined[0] + timedelta(minutes=WINDOW_MIN)
    return max(0, int((free_at - now).total_seconds()) + 5)


def selftest() -> int:
    """Drive the meter to BOTH verdicts on fixtures, and to its blind state.

    A meter that has only ever said "budget free" has not been seen to meter.
    """
    print("RATE BUDGET SELFTEST\n")
    now = datetime(2026, 8, 10, 14, 0, 0, tzinfo=timezone.utc)

    seq = [0]

    def mk(mins_ago, kind="unrated", ours=True):
        t = now - timedelta(minutes=mins_ago)
        seq[0] += 1
        mid = f"{'ours' if ours else 'them'}-{seq[0]}"
        return {"id": mid, "triggeredBy": kind,
                "createdAt": t.isoformat().replace("+00:00", "Z")}

    cases = [
        ("empty -> free", [], 0, 0),
        ("4 inside window -> free", [mk(1), mk(5), mk(9), mk(19)], 4, 0),
        ("5 inside window -> BLOCKED", [mk(1), mk(5), mk(9), mk(15), mk(19)], 5, 65),
        ("5 but oldest aged out -> free", [mk(1), mk(5), mk(9), mk(15), mk(21)], 4, 0),
        ("ladder matches must NOT count", [mk(1, "ladder")], 0, 0),
        # ⚠ THIS CASE'S EXPECTED WAIT CHANGED AT s29, DELIBERATELY, AND THE
        # CHANGE IS THE POINT RATHER THAN AN ADJUSTMENT TO MAKE A TEST PASS.
        # The COUNT assertion is untouched: opponent-initiated matches still do
        # NOT count as our spend (want_n=2), because that is a fact about the
        # budget. The WAIT moved 0 -> conservative, because the meter cannot
        # tell an opponent's challenge from our own runner failing to write
        # scratchpad/arm_*.txt, and only one of those is safe to act on.
        # Over-waiting costs latency; under-waiting cost the LOKI-19 treatment
        # window and spends budget on rejects, which themselves count.
        ("OPPONENT-INITIATED: not our COUNT, but still our WAIT",
         [mk(1), mk(2), mk(3, ours=False), mk(4, ours=False), mk(5, ours=False)], 2, 905),
    ]
    bad = 0
    for label, matches, want_n, want_wait in cases:
        _OVERRIDE.clear()
        _OVERRIDE.update({"matches": matches, "now": now,
                          "our_ids": {m["id"] for m in matches
                                      if m["id"].startswith("ours")}})
        n, _t, ok, _u = spend()
        w = wait_seconds()
        good = (n == want_n) and (w == want_wait) and ok
        print(f"  [{'ok' if good else 'FAIL'}] {label:<34} spent={n} wait={w}s")
        if not good:
            bad += 1
            print(f"          expected spent={want_n} wait={want_wait}s")

    # BLIND STATE: an unreadable body must NOT read as "budget free".
    # SECOND BLIND STATE: readable body, but the in-window matches cannot be
    # attributed. Until s29 this returned 0 on the machine path -- fail-OPEN --
    # while printing a warning only a human would see. This branch is the reason
    # the LOKI-19 treatment window was lost.
    _OVERRIDE.clear()
    _OVERRIDE.update({
        "now": now, "our_ids": set(),
        "matches": [mk(i) for i in (1, 2, 3, 4, 5)],
    })
    n, _t, ok, u = spend()
    w = wait_seconds()
    unattr_ok = ok and n == 0 and len(u) == 5 and w > 0
    print(f"  [{'ok' if unattr_ok else 'FAIL'}] {'UNATTRIBUTED in-window -> must REFUSE':<34} "
          f"ours={n} unattributed={len(u)} wait={w}s")
    if not unattr_ok:
        bad += 1

    _OVERRIDE.clear()
    _OVERRIDE.update({"matches": None, "now": now, "our_ids": set()})
    n, _t, ok, _u = spend()
    w = wait_seconds()
    blind_ok = (not ok) and w == WINDOW_MIN * 60
    print(f"  [{'ok' if blind_ok else 'FAIL'}] {'unreadable body -> assume worst':<34} "
          f"meter_ok={ok} wait={w}s")
    if not blind_ok:
        bad += 1
    _OVERRIDE.clear()

    print()
    if bad:
        print(f"*** {bad} case(s) wrong -- the meter is not metering ***")
        return 1
    print("PASS: reads spent/free/blocked/aged-out, ignores ladder matches, and "
          "BOTH blind states refuse rather than permit -- unreadable body AND "
          "unattributable in-window matches.")
    return 0


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    n, times, ok, unattr = spend()
    w = wait_seconds()
    if "--wait" in argv:
        print(w)
        return 0
    if not ok:
        print("RATE BUDGET: ** METER BLIND ** (no readable `matches` field) -- "
              f"assume the full {WINDOW_MIN}-minute window, wait {w}s")
        return 0
    print(f"RATE BUDGET: {n}/{LIMIT} spent in the last {WINDOW_MIN} min "
          f"(shared across ALL runners and lanes)")
    for t in times:
        print(f"    {t.strftime('%H:%M:%SZ')}")
    if unattr:
        print(f"  ** {len(unattr)} in-window unrated match(es) UNATTRIBUTED "
              f"(not in any scratchpad/arm_*.txt):")
        for t in unattr:
            print(f"    {t.strftime('%H:%M:%SZ')}  <- counted as OURS for the wait")
        print("     Either an opponent challenged us, or A RUNNER OF OURS IS NOT "
              "WRITING arm_*.txt.\n     Indistinguishable here, so the wait "
              "assumes the unsafe one. **")
    print(f"  wait {w}s before the next challenge"
          if w else "  a slot is free NOW")
    print("  ** LOWER BOUND: rejected attempts count against the limit and "
          "create no match, so they are invisible here. **")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
