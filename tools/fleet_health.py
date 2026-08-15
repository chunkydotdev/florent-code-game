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
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (label, match-substring, expected, why it matters, how to bring it back, AUTO)
# `expected=None` means "one or more, count is informational" (worker shards).
#
# ⛔ THE `AUTO` COLUMN IS A SAFETY BOUNDARY, NOT A CONVENIENCE FLAG.
# `tools/watchdog.sh` will relaunch a MISSING row only when AUTO is True. The
# bar for True is: relaunching it CANNOT DESTROY WORK, even if the "it is
# missing" judgement is wrong. That bar comes straight from `corefill.sh`
# guard 1 -- on 2026-08-11 `overnight_watch.sh` restarted NINE COMPLETED shards
# from zero because a finished-and-archived run and a never-started run looked
# identical to it. **A watchdog is one bad predicate away from destroying a
# night's work**, so the blast radius is bounded here rather than trusted there.
#
# AUTO=False does NOT mean unimportant -- shard runners are the actual work.
# It means a human decides, because a wrong restart costs data.
#
# ⛔ AND NOTHING IS EVER AUTO-KILLED. A DUPLICATE is reported with the exact
# kill command and left alone: choosing which of two live daemons dies is a
# judgement about which one other things are already talking to.
SPEC = [
    ("corefill_forever", "corefill_forever.sh", 1,
     "THE SUPERVISOR. corefill.sh has two terminal exits and neither re-arms "
     "anything; without this the box goes idle and stays idle.",
     "nohup zsh tools/corefill_forever.sh scratchpad/corefill_work.txt 8 "
     ">> scratchpad/corefill_forever.log 2>&1 &", True),
    ("corefill runner", "corefill.sh scratchpad", 1,
     "Launches shards. TWO runners each enforce MAX_SHARDS separately -> 2x "
     "oversubscription -> --tle 10 is wall-clock -> corrupted rows.",
     "(the supervisor relaunches it within one poll; do not start it by hand)", False),
    ("auto_gate --apply", "auto_gate.py --apply", 1,
     "CANCELS BATTERIES. Two armed copies is the one duplication with a "
     "destructive edge.",
     "nohup zsh -c 'while true; do .venv/bin/python tools/auto_gate.py --apply "
     ">> scratchpad/auto_gate.log 2>&1; sleep 600; done' >/dev/null 2>&1 &", False),
    ("fleet_dispatch", "fleet_dispatch.py", 1,
     "Hands queued rows to whichever host has a free slot. Built once and left "
     "unstarted for 3h06m on 2026-08-14; ws2 idled 39 min for it.",
     "nohup zsh -c 'while true; do .venv/bin/python tools/fleet_dispatch.py --once "
     "--remote-mode live >> scratchpad/fleet_dispatch.log 2>&1; sleep 300; done' "
     ">/dev/null 2>&1 &", True),
    ("keeper", "corpus/keeper.py", 1,
     "Keeps the replay corpus current. A stale corpus makes an ABSENCE look "
     "like evidence.",
     "nohup .venv/bin/python tools/corpus/keeper.py >> corpus/keeper.out 2>&1 &", True),
    ("elo_logger", "monitors/elo_logger.py", 1,
     "Writes the rating tape.",
     "nohup zsh -c 'while true; do S=$(.venv/bin/fcode status --json 2>/dev/null); "
     "L=$(.venv/bin/fcode submission list --json 2>/dev/null); "
     "printf \"%s\\n---SPLIT---\\n%s\" \"$S\" \"$L\" | "
     ".venv/bin/python tools/monitors/elo_logger.py; sleep 300; done' "
     ">> scratchpad/elo_logger.log 2>&1 &", True),
    ("match_watcher", "monitors/match_watcher.py", 1,
     "Rated match ingest.",
     "nohup zsh -c 'while true; do .venv/bin/fcode match list --mine --type ladder "
     "--json --limit 20 2>/dev/null | .venv/bin/python tools/monitors/match_watcher.py; "
     "sleep 120; done' >> scratchpad/match_watcher.log 2>&1 &", True),
    ("opp_watcher", "monitors/opp_watcher.py", 1,
     "Opponent version timeline -- the authority for THEIR ships.",
     "nohup zsh -c 'while true; do .venv/bin/fcode match list --json --limit 100 "
     "2>/dev/null | .venv/bin/python tools/monitors/opp_watcher.py; sleep 600; done' "
     ">> scratchpad/opp_watcher.log 2>&1 &", True),
    ("replay_archiver", "monitors/replay_archiver.py", 1,
     "Pulls replays. If it dies the archive silently stops growing.",
     "nohup zsh -c 'while true; do .venv/bin/python tools/monitors/replay_archiver.py; "
     "sleep 1800; done' >> scratchpad/replay_archiver.log 2>&1 &", True),
    ("ship_watch", "monitors/ship_watch.py", 1,
     "Slot/stop-loss trend. NOT the holder -- it is a 10-min poller.",
     "nohup zsh -c 'while true; do .venv/bin/python tools/monitors/ship_watch.py; "
     "sleep 600; done' >> scratchpad/ship_watch.log 2>&1 &", True),
    ("cores_idle", "monitors/cores_idle.py", 1,
     "Idle-core alarm. Watches the LOCAL box only; remote idle is invisible "
     "to every instrument we own.",
     "nohup zsh -c 'while true; do .venv/bin/python tools/monitors/cores_idle.py; "
     "sleep 600; done' >> scratchpad/cores_idle.log 2>&1 &", True),
    ("holder_watch", "monitors/holder_watch.sh", 1,
     "Alarms when the ladder slot changes hands. It EXITS on first change, so "
     "a leg's own activation consumes it.",
     "(one-shot by design: re-arm deliberately, with the version you expect)", False),
    ("shard runners", "overnight.sh ", None,
     "The actual batteries. Count is informational -- the supervisor and the "
     "load ceiling govern it.", "(started by corefill.sh)", False),
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
        r = subprocess.run(["ps", "ax", "-o", "pid=,ppid=,etime=,command="],
                           capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if not (r.stdout or "").strip():
        return None
    rows, anc = [], _ancestors()
    for line in r.stdout.splitlines():
        parts = line.strip().split(None, 3)
        if len(parts) < 4:
            continue
        try:
            pid, ppid = int(parts[0]), int(parts[1])
        except ValueError:
            continue
        if pid in anc:
            continue
        rows.append((pid, parts[3], _etime_s(parts[2]), ppid))
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
    for label, needle, expected, why, fix, auto in SPEC:
        # OLDEST FIRST, so `pids[expected:]` is always the newcomers -- keep the
        # established daemon, kill what arrived after it.
        hits = sorted([(p, c, age, pp) for p, c, age, pp in procs if needle in c],
                      key=lambda t: -t[2])
        # ⛔ COLLAPSE WRAPPER+CHILD, OR EVERY LOOP DAEMON IS A FALSE DUPLICATE.
        # Monitors run as `zsh -c while true; do python X.py; sleep N; done`, and
        # the needle `monitors/X.py` matches the WRAPPER *and* the python CHILD
        # it spawns. So the count is 1 while sleeping and 2 while working --
        # i.e. the row reports DUPLICATE for the seconds the daemon is actually
        # doing its job. Measured 2026-08-15: replay_archiver read
        # `pids=19887,11546` and 11546 vanished on its own moments later.
        # ⭐ AND THAT FALSE POSITIVE COST A CORRECT CONCLUSION: it was first read
        # as "the watchdog spawned a duplicate daemon", which is evidence of harm
        # that never happened, and the watchdog was uninstalled over it.
        # Drop any hit whose PARENT is also a hit for this same row: a child of
        # the supervising loop is that loop working, not a second copy of it.
        hitpids = {p for p, _c, _a, _pp in hits}
        hits = [h for h in hits if h[3] not in hitpids]
        pids = [p for p, _c, _a, _pp in hits]
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
        results.append((label, state, found, expected, why, fix, pids, auto))
    return results, bad


def emit_json() -> int:
    """Machine-readable, for tools/watchdog.sh. Structure, never scraped text.

    A watchdog that greps a human report is one wording change away from
    silently doing nothing -- and a watchdog that silently does nothing is
    exactly the failure it exists to prevent.
    """
    procs = scan()
    if procs is None:
        print(json.dumps({"blind": True, "problems": [], "rows": []}))
        return 2
    results, bad = evaluate(procs)
    print(json.dumps({
        "blind": False,
        "problems": bad,
        "rows": [{"label": l, "state": st, "found": f, "expected": e,
                  "pids": p, "auto": bool(a), "fix": fx, "why": w}
                 for l, st, f, e, w, fx, p, a in results],
    }))
    return 1 if bad else 0


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
    for label, state, found, expected, why, fix, pids, auto in results:
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
    full = [(100 + i, f"zsh {n[1]}", 10_000 + i, 1)
            for i, n in enumerate(SPEC) if n[2] is not None]
    full.append((999, "zsh tools/overnight.sh SHARD a b 5400 1", 500, 1))

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
    dup = full + [(555, "zsh -c while true; do auto_gate.py --apply; done", 5, 1)]
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
    real = [p for p in without] + [(555, "zsh -c while true; do auto_gate.py --apply; done", 5, 1)]
    _, nbad = evaluate(real)
    check("the ACTUAL 2026-08-15 fault state -> 2 problems", nbad, 2)

    # ⭐ WRAPPER + ITS OWN CHILD MUST READ AS ONE, NOT AS A DUPLICATE.
    # This is the cell that would have prevented a false "the watchdog spawned
    # a duplicate" conclusion. pid 700's parent is the replay_archiver wrapper.
    wrapper = [p for p in full if "replay_archiver" in p[1]][0]
    child = (700, ".venv/bin/python tools/monitors/replay_archiver.py", 4, wrapper[0])
    res, nbad = evaluate(full + [child])
    check("loop wrapper + its python child -> ONE, not DUPLICATE", nbad, 0)
    check("...and the row reports found=1",
          [r[2] for r in res if r[0] == "replay_archiver"], [1])
    # ...while a genuine second WRAPPER (parent is launchd, not us) still fires.
    twin = (701, "zsh -c while true; do python tools/monitors/replay_archiver.py; done", 4, 1)
    _, nbad2 = evaluate(full + [twin])
    check("a genuine second wrapper -> still DUPLICATE", nbad2, 1)

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
    ap.add_argument("--json", action="store_true",
                    help="machine-readable output for tools/watchdog.sh")
    ap.add_argument("--selftest", action="store_true",
                    help="drive every verdict both ways and exit")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.json:
        return emit_json()
    return render(quiet=a.quiet)


if __name__ == "__main__":
    sys.exit(main())
