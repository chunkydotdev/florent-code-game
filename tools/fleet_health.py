#!/usr/bin/env python3
"""FLEET HEALTH — what is SUPPOSED to be running, and is it?

    .venv/bin/python tools/fleet_health.py            # report; exit 1 if anything is wrong
    .venv/bin/python tools/fleet_health.py --quiet     # one line unless something is wrong
    .venv/bin/python tools/fleet_health.py --selftest  # every verdict driven both ways

===== WHY THIS EXISTS =====
`corefill_status.sh` reports SHARDS. `now.py` reports STATE. **Nothing reported
SUPERVISORS** -- and on 2026-08-15 an audit found, in one pass:

  * `corefill_forever.sh` DEAD FOR 22 HOURS. It paused on `COREFILL_STOP`, the
    session that would have resumed it ended, and NOTHING WAS RESPONSIBLE FOR
    NOTICING. The live runner carried a 12h deadline, so the box was set to stop
    launching at ~03:40Z with 55 items unstarted and 8 cores idle -- a replay of
    the 2026-08-13 outage that supervisor was written to prevent.
  * `auto_gate.py --apply` running TWICE. That is the tool that CANCELS
    BATTERIES; two armed copies is the one duplication with a destructive edge.
  * `holder_watch.sh` running TWICE.

⭐ EVERY ONE OF THOSE IS INVISIBLE TO A HEALTHY-LOOKING SYSTEM. Eight shards were
running, the load was at ceiling, the logs said `hold: running=8/8`. The defect
was one layer up, and no instrument looked there.

===== THE DESIGN RULE =====
**A COUNT IS THE VERDICT, NOT PRESENCE.** The historical instinct is to check
"is X running?" -- which is blind to the duplicate, and duplicates are how this
repo loses data (two `corefill.sh` runners each enforce MAX_SHARDS separately,
and `--tle 10` is WALL-CLOCK, so oversubscription corrupts every row both
produce). So every row below declares an EXACT expected count and reports
MISSING and EXTRA as distinct failures.

**AND BLIND IS NOT HEALTHY.** If the process table cannot be read we exit 2 and
say UNKNOWN rather than reporting everything missing -- the repo's most-repeated
defect is an alarm that cannot tell it is blind.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (label, match-substring, expected, why it matters, how to bring it back)
# `expected=None` means "one or more, count is informational" (worker shards).
SPEC = [
    ("corefill_forever", "corefill_forever.sh", 1,
     "THE SUPERVISOR. corefill.sh has two terminal exits and neither re-arms "
     "anything; without this the box goes idle and stays idle.",
     "nohup zsh tools/corefill_forever.sh scratchpad/corefill_work.txt 8 "
     ">> scratchpad/corefill_forever.log 2>&1 &"),
    ("corefill runner", "corefill.sh scratchpad", 1,
     "Launches shards. TWO runners each enforce MAX_SHARDS separately -> 2x "
     "oversubscription -> --tle 10 is wall-clock -> corrupted rows.",
     "(the supervisor relaunches it within one poll; do not start it by hand)"),
    ("auto_gate --apply", "auto_gate.py --apply", 1,
     "CANCELS BATTERIES. Two armed copies is the one duplication with a "
     "destructive edge.",
     "zsh -c 'while true; do .venv/bin/python tools/auto_gate.py --apply "
     ">> scratchpad/auto_gate.log 2>&1; sleep 600; done' &"),
    ("fleet_dispatch", "fleet_dispatch.py", 1,
     "Hands queued rows to whichever host has a free slot. Built once and left "
     "unstarted for 3h06m on 2026-08-14; ws2 idled 39 min for it.",
     "zsh -c 'while true; do .venv/bin/python tools/fleet_dispatch.py --once "
     "--remote-mode live >> scratchpad/fleet_dispatch.log 2>&1; sleep 300; done' &"),
    ("keeper", "corpus/keeper.py", 1,
     "Keeps the replay corpus current. A stale corpus makes an ABSENCE look "
     "like evidence.", "see tools/corpus/keeper.py docstring"),
    ("elo_logger", "monitors/elo_logger.py", 1,
     "Writes the rating tape.", "see tools/monitors/ docstrings"),
    ("match_watcher", "monitors/match_watcher.py", 1,
     "Rated match ingest.", "see tools/monitors/ docstrings"),
    ("opp_watcher", "monitors/opp_watcher.py", 1,
     "Opponent version timeline -- the authority for THEIR ships.",
     "see tools/monitors/ docstrings"),
    ("replay_archiver", "monitors/replay_archiver.py", 1,
     "Pulls replays. If it dies the archive silently stops growing.",
     "see tools/monitors/ docstrings"),
    ("ship_watch", "monitors/ship_watch.py", 1,
     "Slot/stop-loss trend. NOT the holder -- it is a 10-min poller.",
     "see tools/monitors/ docstrings"),
    ("cores_idle", "monitors/cores_idle.py", 1,
     "Idle-core alarm. Watches the LOCAL box only; remote idle is invisible "
     "to every instrument we own.", "see tools/monitors/ docstrings"),
    ("holder_watch", "monitors/holder_watch.sh", 1,
     "Alarms when the ladder slot changes hands. It EXITS on first change, so "
     "a leg's own activation consumes it.", "see tools/monitors/ docstrings"),
    ("shard runners", "overnight.sh ", None,
     "The actual batteries. Count is informational -- the supervisor and the "
     "load ceiling govern it.", "(started by corefill.sh)"),
]


def _ancestors() -> set[int]:
    """PIDs we are descended from.

    ⛔ NOT COSMETIC. A first draft of the sibling guard in `corefill.sh` matched
    its OWN INVOKING SHELL, because this process's argv contains the very
    strings being searched for. Any ps-scanning check in this repo must exclude
    its own ancestry or it will report a phantom duplicate of itself.
    """
    out, pid = set(), os.getpid()
    while pid and pid > 1:
        out.add(pid)
        try:
            r = subprocess.run(["ps", "-o", "ppid=", "-p", str(pid)],
                               capture_output=True, text=True, timeout=10)
            pid = int((r.stdout or "0").strip() or 0)
        except (OSError, ValueError, subprocess.TimeoutExpired):
            break
    return out


def scan() -> list[tuple[int, str]] | None:
    """[(pid, command)] or None when the process table cannot be read."""
    # `etime` is captured so duplicates can be ordered OLDEST FIRST. That is not
    # cosmetic: the kill advice must name the NEWER copy. `ps` output order is
    # neither age nor pid order, and a first version of this tool would have told
    # you to kill the ESTABLISHED daemon (pid 61319, up 6h39m) and keep the one
    # started 2h32m ago -- the wrong one, stated with full confidence.
    try:
        r = subprocess.run(["ps", "ax", "-o", "pid=,etime=,command="],
                           capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if not (r.stdout or "").strip():
        return None
    rows, anc = [], _ancestors()
    for line in r.stdout.splitlines():
        parts = line.strip().split(None, 2)
        if len(parts) < 3:
            continue
        try:
            pid = int(parts[0])
        except ValueError:
            continue
        if pid in anc:
            continue
        rows.append((pid, parts[2], _etime_s(parts[1])))
    return rows


def _etime_s(e: str) -> int:
    """`ps` etime -> seconds. Forms: SS, MM:SS, HH:MM:SS, D-HH:MM:SS."""
    try:
        days, _, rest = e.partition("-")
        if not rest:
            rest, days = days, "0"
        bits = [int(x) for x in rest.split(":")]
        while len(bits) < 3:
            bits.insert(0, 0)
        return int(days) * 86400 + bits[0] * 3600 + bits[1] * 60 + bits[2]
    except (ValueError, IndexError):
        return 0


def evaluate(procs: list[tuple[int, str]]):
    """-> (results, n_bad). A result is (label, state, found, expected, why, fix, pids)."""
    results, bad = [], 0
    for label, needle, expected, why, fix in SPEC:
        # OLDEST FIRST, so `pids[expected:]` is always the newcomers -- keep the
        # established daemon, kill what arrived after it.
        hits = sorted([(p, c, age) for p, c, age in procs if needle in c],
                      key=lambda t: -t[2])
        pids = [p for p, _c, _a in hits]
        found = len(pids)
        if expected is None:
            state = "info"
        elif found == expected:
            state = "ok"
        elif found < expected:
            state = "MISSING"
            bad += 1
        else:
            state = "DUPLICATE"
            bad += 1
        results.append((label, state, found, expected, why, fix, pids))
    return results, bad


def render(quiet: bool = False) -> int:
    procs = scan()
    if procs is None:
        print("⛔ UNKNOWN — cannot read the process table. This is BLIND, not healthy.")
        print("   Refusing to report anything as MISSING on an unreadable table.")
        return 2

    results, bad = evaluate(procs)

    if quiet and not bad:
        n = sum(1 for r in results if r[1] == "ok")
        print(f"fleet OK — {n} expected daemon(s) present, no duplicates.")
        return 0

    print("FLEET HEALTH — what is supposed to be running, and is it?\n")
    for label, state, found, expected, why, fix, pids in results:
        exp = "1+" if expected is None else str(expected)
        mark = {"ok": "  ok", "info": "info", "MISSING": "⛔ MISSING",
                "DUPLICATE": "⛔ DUPLICATE"}[state]
        print(f"  [{mark:>12}] {label:<18} found={found} expected={exp}"
              + (f"  pids={','.join(map(str, pids))}" if pids and state != "ok" else ""))
        if state in ("MISSING", "DUPLICATE"):
            print(f"                 WHY IT MATTERS: {why}")
            if state == "MISSING":
                print(f"                 RESTART: {fix}")
            else:
                extra = pids[expected:] if expected else pids[1:]
                print(f"                 KILL THE EXTRAS: kill {' '.join(map(str, extra))}")
    print()
    if bad:
        print(f"*** {bad} PROBLEM(S). A healthy shard count does NOT cover this layer: ***")
        print("    on 2026-08-15 eight shards were running at the load ceiling while the")
        print("    SUPERVISOR had been dead 22 hours and two cancellers were armed.")
        return 1
    print("OK — every expected daemon present, exactly once.")
    return 0


# ===================== SELFTEST =====================
def selftest() -> int:
    bad = 0

    def check(label, got, want):
        nonlocal bad
        ok = got == want
        bad += (not ok)
        print(f"  [{'ok' if ok else 'FAIL'}] {label:<58} got={got} want={want}")

    # (pid, command, age_s). Ages ascend so the ORDERING claim is testable.
    full = [(100 + i, f"zsh {n[1]}", 10_000 + i)
            for i, n in enumerate(SPEC) if n[2] is not None]
    full.append((999, "zsh tools/overnight.sh SHARD a b 5400 1", 500))

    res, nbad = evaluate(full)
    check("all present exactly once -> 0 problems", nbad, 0)
    check("...and no row is MISSING", any(r[1] == "MISSING" for r in res), False)

    # MISSING must fire, and on the RIGHT row.
    without = [p for p in full if "corefill_forever" not in p[1]]
    res, nbad = evaluate(without)
    check("supervisor absent -> 1 problem", nbad, 1)
    check("...and it is the supervisor row that is MISSING",
          [r[0] for r in res if r[1] == "MISSING"], ["corefill_forever"])

    # DUPLICATE must fire, and be distinguished from MISSING.
    # the duplicate is YOUNGER (age 5) than the original, so a correct tool
    # must nominate 555 for the kill, not the established one.
    dup = full + [(555, "zsh -c while true; do auto_gate.py --apply; done", 5)]
    res, nbad = evaluate(dup)
    check("second auto_gate -> 1 problem", nbad, 1)
    check("...classified DUPLICATE, not MISSING",
          [r[1] for r in res if r[0] == "auto_gate --apply"], ["DUPLICATE"])
    # ⭐ THE ORDERING CLAIM: the ESTABLISHED daemon is kept, the NEWCOMER is
    # nominated for the kill. Reversed advice would take down the working one.
    row = [r for r in res if r[0] == "auto_gate --apply"][0]
    check("oldest-first: established pid is listed first", row[6][0] != 555, True)
    check("oldest-first: the NEWCOMER is the one nominated to kill",
          row[6][1:], [555])

    # The real 2026-08-15 state: supervisor dead AND two cancellers.
    real = [p for p in without] + [(555, "zsh -c while true; do auto_gate.py --apply; done", 5)]
    _, nbad = evaluate(real)
    check("the ACTUAL 2026-08-15 fault state -> 2 problems", nbad, 2)

    # Informational rows must never count as failures.
    noshards = [p for p in full if "overnight.sh" not in p[1]]
    res, nbad = evaluate(noshards)
    check("zero shard runners -> informational, NOT a problem", nbad, 0)

    # BLIND must not read as "everything missing".
    import unittest.mock as m
    with m.patch(f"{__name__}.scan", return_value=None):
        check("unreadable process table -> rc 2 (UNKNOWN), not rc 1", render(), 2)

    print("\nPASS: MISSING and DUPLICATE are distinct and land on the right row; "
          "\nan unreadable table is UNKNOWN, not a pile of failures."
          if not bad else f"\n*** {bad} case(s) wrong ***")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="What is supposed to be running, and is it? Counts are the "
                    "verdict: MISSING and DUPLICATE are both failures.")
    ap.add_argument("--quiet", action="store_true",
                    help="one line unless something is wrong (for hooks)")
    ap.add_argument("--selftest", action="store_true",
                    help="drive every verdict both ways and exit")
    a = ap.parse_args()
    return selftest() if a.selftest else render(quiet=a.quiet)


if __name__ == "__main__":
    sys.exit(main())
