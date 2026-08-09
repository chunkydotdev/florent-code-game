#!/usr/bin/env python3
"""Ship watch — evaluate the live holder against the ladder stop-loss, and SAY SO.

WHY THIS EXISTS. Monitors in this project survive session resets; the SESSION
does not. `elo_logger` records the tape and `keeper` ingests replays, but
nothing was evaluating the SLOT DECISION on a cadence — a human or a fresh
session had to notice. "Named wake path or state there is none" is a standing
rule here, and for the v102 ship the honest answer was "there is none". This is
the fix.

WHAT IT DOES. Reads `elo_history.tsv`, isolates the CURRENT holder's run,
computes (net, k) against the activation baseline, and runs the same sequential
test as `tools/slot_sprt.py`:

    LLR = (0 - MU0)/sd^2 * (net - k * MU0/2)      sd = 9.25, MU0 = -2.0

    LLR <= -B  -> BLEEDING, the slot is free      (B = log((1-beta)/alpha))
    LLR >= +B  -> CLEARED, holder is fine
    otherwise  -> undecided, keep watching

It APPENDS every evaluation to `corpus/ship_watch.log` so the trajectory is
queryable after the fact, and writes `corpus/SHIP_ALERT` only on a BLEEDING
verdict — a file whose existence is the alarm, so a fresh session sees it at a
glance rather than having to reconstruct the run.

Cadence: 10 min is plenty; ladder slots fire every ~10 min, so a faster loop
re-tests the same data. Arm detached from the repo root:

    while true; do .venv/bin/python tools/monitors/ship_watch.py; sleep 600; done

Baseline is passed once at arm time and then persisted, because the activation
rating is NOT recoverable from the tape after the fact -- the first tape row
after a swap is already several matches old.

    SHIP_BASELINE=1577.5 SHIP_VERSION=v102 .venv/bin/python tools/monitors/ship_watch.py
"""
from __future__ import annotations

import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
TAPE = ROOT / "elo_history.tsv"
LOG = ROOT / "corpus" / "ship_watch.log"
ALERT = ROOT / "corpus" / "SHIP_ALERT"
STATE = ROOT / "corpus" / "ship_watch_state.json"

# CONSTANTS AND THE TEST ITSELF ARE IMPORTED, NEVER RE-DERIVED.
# The first cut of this file re-implemented the LLR from the docstring of
# slot_sprt.py and guessed MU0 = -2.0, ALPHA = 0.05. The calibrated values are
# MU0 = -10.0 and ALPHA = 0.15, both chosen by BACKTEST in that tool. The
# guessed version computed LLR +0.596 where the real one gives +7.246 on the
# same (net, k) -- and, fatally, a -30 Elo bleed over 12 matches produced NO
# ALARM. A stop-loss that cannot fire is worse than none, because its silence
# reads as safety. Caught by this file's own teeth test before it was armed.
sys.path.insert(0, str(ROOT / "tools"))
from slot_sprt import llr, bound          # noqa: E402  the calibrated test

BOUND = bound()


def main() -> int:
    state = {}
    if STATE.exists():
        try:
            state = json.loads(STATE.read_text())
        except Exception:
            state = {}
    version = os.environ.get("SHIP_VERSION") or state.get("version")
    baseline = os.environ.get("SHIP_BASELINE") or state.get("baseline")
    if not version or baseline is None:
        print("no SHIP_VERSION/SHIP_BASELINE (env or state) — nothing to watch",
              file=sys.stderr)
        return 2
    baseline = float(baseline)
    STATE.write_text(json.dumps({"version": version, "baseline": baseline}))

    rows = [r for r in csv.reader(TAPE.read_text().splitlines(), delimiter="\t")][1:]
    run = [r for r in rows if len(r) > 3 and r[3] == version]
    if not run:
        print(f"{version} not on the tape yet", file=sys.stderr)
        return 0
    first, last = run[0], run[-1]
    net = float(last[1]) - baseline
    k = int(last[2]) - int(first[2])
    if k <= 0:
        return 0
    L = llr(net, k)
    verdict = ("BLEEDING" if L <= -BOUND else
               "CLEARED" if L >= BOUND else "undecided")

    line = (f"{datetime.now().isoformat(timespec='seconds')}\t{version}\t"
            f"net={net:+.1f}\tk={k}\trating={last[1]}\tllr={L:+.3f}\t"
            f"bound=±{BOUND:.3f}\t{verdict}")
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a") as fh:
        fh.write(line + "\n")
    print(line)

    if verdict == "BLEEDING":
        ALERT.write_text(
            line + "\n\nThe live holder is bleeding by the sequential test.\n"
            "ROLLBACK: .venv/bin/fcode submission activate <rollback version>\n"
            "See HANDOVER.md for the current rollback target.\n")
        print("*** SHIP_ALERT WRITTEN — holder is bleeding ***", file=sys.stderr)
    elif ALERT.exists():
        ALERT.unlink()      # recovered; do not leave a stale alarm standing
    return 0


if __name__ == "__main__":
    sys.exit(main())
