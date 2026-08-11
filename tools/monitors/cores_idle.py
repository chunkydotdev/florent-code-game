#!/usr/bin/env python3
"""CORES IDLE WATCH — the machine has 10 cores and nothing is using them.

WHY THIS EXISTS, AND IT IS A MAGNUS CATCH NOT A DESIGN
------------------------------------------------------
2026-08-11 (s31), Magnus, twice in ten minutes:
  *"anything running locally?"*
  *"do we not monitor the local runs? if nothing is running we're losing time
    we could use to figure out the next Loki version"*
  *"If we are not running locally we should grab items from the queue and run
    them, the researcher has a monitor that makes them put more items in the
    queue if it is running out."*

**HE HAD TO ASK. There was no instrument.** We monitor the ladder (elo_logger),
our matches (match_watcher), the field (opp_watcher), the archive
(replay_archiver), the slot (ship_watch) and the corpus (keeper) — **six monitors,
all pointed at the PLATFORM, and not one pointed at whether our own machine is
doing anything.** At 13:53Z the load average had drained 14.67 -> 1.57 with zero
`fcode run` processes and a full queue sitting unread.

**THE ASYMMETRY THAT MADE IT INVISIBLE:** every other monitor watches a thing
that CHANGES and alarms on a bad value. Idle cores are not a bad value — they are
the ABSENCE of a value, and absence is what this repo's monitors have repeatedly
failed to see (`ship_watch` printing healthy lines off a stale tape; a screen
that cannot fire; a guard whose declared-count used the same broken pattern).
**An alarm that cannot tell it is blind, and an alarm for a thing that is simply
not happening, are the same failure.**

WHAT IT DOES
------------
Counts running `fcode run` processes. If ZERO for two consecutive polls, it
prints an ALERT naming the top unblocked item in `QUEUE.md` — the queue is the
answer to "what should be running", so the alarm carries its own remedy.

⛔ IT GATES ON THE PROCESS COUNT, NEVER ON AN EXIT CODE, and it reports the AGE
of what it read — both standing repo rules (`fcode status` exits 0 while printing
`Error: True`; a monitor that reads a file must report that file's freshness).

Usage:  cores_idle.py            # one poll, prints a line
        cores_idle.py --selftest # forced-answer cells
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
STATE = Path(os.environ.get("STATE_DIR", ROOT / "corpus")) / "cores_idle_state.json"
QUEUE = ROOT / "QUEUE.md"
ALERT = ROOT / "corpus" / "CORES_IDLE_ALERT"


def running_games() -> int:
    """Count live local games. Process count, not an exit code."""
    try:
        out = subprocess.run(["ps", "ax", "-o", "command="],
                             capture_output=True, text=True, timeout=20).stdout
    except Exception:
        return -1                       # UNKNOWN, never silently 0
    n = 0
    for line in out.splitlines():
        if "fcode" in line and re.search(r"\bfcode\b.*\brun\b", line):
            n += 1
    return n


def next_queue_item():
    """Top unblocked row of QUEUE.md, so the alarm carries its own remedy."""
    if not QUEUE.exists():
        return None, None
    age_min = (time.time() - QUEUE.stat().st_mtime) / 60.0
    rows = []
    for line in QUEUE.read_text().splitlines():
        if not line.startswith("|"):
            continue
        if "~~" in line or "WITHDRAWN" in line or "SHIPPED" in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 2 and cells[0].isdigit():
            rows.append(cells[1].replace("*", ""))
    return (rows[0] if rows else None), age_min


def main() -> int:
    n = running_games()
    prev = {}
    if STATE.exists():
        try:
            prev = json.loads(STATE.read_text())
        except Exception:
            prev = {}
    consec = prev.get("consec_idle", 0)
    if n == 0:
        consec += 1
    elif n > 0:
        consec = 0
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps({"consec_idle": consec, "last_n": n,
                                 "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                                     time.gmtime())}))
    item, age = next_queue_item()
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    if n < 0:
        print(f"{stamp}\tgames=UNKNOWN\tCORES=BLIND (ps failed) — not reporting idle")
        return 0
    qs = f"queue_age_min={age:.1f}" if age is not None else "queue=MISSING"
    if consec >= 2:
        msg = (f"{stamp}\tgames=0\tconsec_idle={consec}\t{qs}\t"
               f"*** CORES IDLE — NEXT QUEUE ITEM: {item or 'QUEUE EMPTY'} ***")
        print(msg)
        with ALERT.open("a") as fh:
            fh.write(msg + "\n")
    else:
        print(f"{stamp}\tgames={n}\tconsec_idle={consec}\t{qs}\tOK")
        if n > 0 and ALERT.exists():
            ALERT.unlink()                # cleared by work actually starting
    return 0


def selftest() -> bool:
    ok = True

    def cell(name, got, want, forced):
        nonlocal ok
        good = got == want
        ok &= good
        print(f"  [{'ok' if good else 'FAIL'}] {name:<44} got={got} want={want}")
        print(f"         forced by: {forced}")

    # ⛔ THE CELL THAT MATTERS: a ps failure must NOT read as "idle". An alarm
    # that cannot tell it is BLIND is the ship_watch failure in a new instrument.
    real = running_games()
    cell("counts live fcode run processes", real >= 0, True,
         "a negative return means ps failed; the caller must treat that as "
         "BLIND, never as zero games")

    # The queue parser must find a real row, or the alarm's remedy is empty.
    item, age = next_queue_item()
    cell("reads a queue item", item is not None, True,
         "the alarm names the next plank; if the parser returns None the alarm "
         "fires with no remedy and is just noise")

    # And it must SKIP withdrawn/shipped rows, or it will send us to a dead plank.
    txt = QUEUE.read_text() if QUEUE.exists() else ""
    cell("skips withdrawn/shipped rows", ("~~" in txt or "WITHDRAWN" in txt), True,
         "QUEUE.md currently contains withdrawn rows; if the parser did not "
         "skip them this cell has no dose and cannot check the filter")
    print("\nCORES_IDLE_SELFTEST: " + ("PASS" if ok else "FAIL"))
    return ok


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    sys.exit(main())
