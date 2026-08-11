#!/usr/bin/env python3
"""RATE BUDGET METER — how much of the 5-per-20-minutes is left, measured.

    .venv/bin/python tools/rate_budget.py              # human read
    .venv/bin/python tools/rate_budget.py --wait       # seconds to wait, one int
    .venv/bin/python tools/rate_budget.py --selftest   # prove it reads both ways

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


def spend(now: datetime | None = None) -> tuple[int, list[datetime], bool]:
    """(spent, sorted challenge times inside the window, meter_ok)."""
    now = now or _OVERRIDE.get("now") or datetime.now(timezone.utc)
    matches = _fetch()
    if matches is None:
        return 0, [], False
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
    if unattributed:
        print(f"  ** {len(unattributed)} unrated match(es) in-window could NOT be "
              f"attributed to any scratchpad/arm_*.txt. Either an opponent "
              f"challenged us, or A RUNNER OF OURS IS NOT WRITING arm_*.txt "
              f"and this meter is UNDERCOUNTING. Check before trusting it. **")
    return len(hits), sorted(hits), True


def wait_seconds(now: datetime | None = None) -> int:
    """Seconds until at least one slot frees. 0 if a slot is free NOW."""
    now = now or _OVERRIDE.get("now") or datetime.now(timezone.utc)
    n, times, ok = spend(now)
    if not ok:
        return WINDOW_MIN * 60          # meter blind -> assume the worst
    if n < LIMIT:
        return 0
    free_at = times[0] + timedelta(minutes=WINDOW_MIN)
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
        ("OPPONENT-INITIATED unrated must NOT count",
         [mk(1), mk(2), mk(3, ours=False), mk(4, ours=False), mk(5, ours=False)], 2, 0),
    ]
    bad = 0
    for label, matches, want_n, want_wait in cases:
        _OVERRIDE.clear()
        _OVERRIDE.update({"matches": matches, "now": now,
                          "our_ids": {m["id"] for m in matches
                                      if m["id"].startswith("ours")}})
        n, _t, ok = spend()
        w = wait_seconds()
        good = (n == want_n) and (w == want_wait) and ok
        print(f"  [{'ok' if good else 'FAIL'}] {label:<34} spent={n} wait={w}s")
        if not good:
            bad += 1
            print(f"          expected spent={want_n} wait={want_wait}s")

    # BLIND STATE: an unreadable body must NOT read as "budget free".
    _OVERRIDE.clear()
    _OVERRIDE.update({"matches": None, "now": now, "our_ids": set()})
    n, _t, ok = spend()
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
    print("PASS: reads spent/free/blocked/aged-out, ignores ladder matches, and a "
          "blind meter refuses rather than permits.")
    return 0


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    n, times, ok = spend()
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
    print(f"  wait {w}s before the next challenge"
          if w else "  a slot is free NOW")
    print("  ** LOWER BOUND: rejected attempts count against the limit and "
          "create no match, so they are invisible here. **")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
