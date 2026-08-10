#!/usr/bin/env python3
"""Pre-ship gate: refuses the "ready to ship" line until the pipeline ran.

WHY THIS EXISTS. test-process-proposal-2026-08-09.md documented two same-day
incidents (ESCALATE, SITE) where the local arena won by default because it is
frictionless and unrated has ceremony. The pipeline's S5 stage (unrated
fidelity) is protected here the same way gate.py protects batteries: a tool
that refuses, not a paragraph that asks. Adopted 2026-08-09 with the process
review (ship-gate.md amendment 4).

Usage:
    .venv/bin/python tools/preflight.py bots/_v115foo

Reads the dev dir's PREREG.md (or README.md) for the S0 pre-registration
block. Required lines (anywhere in the file, `key: value`, value non-empty):

    produces:              what the change PRODUCES + the metric pricing it
                           (output/denial/delivered-objective/win-condition —
                           never survival/persistence)
    falsifier:             the result that kills it
    treatment_occurrence:  local count / unrated count of the triggering state
    S5_unrated:            the unrated read, or a one-line reason why skipped
                           (e.g. "skip: pure refactor, parity proof suffices")

Exit 0 prints READY TO SHIP plus the tape-row template (with the join key:
version tag AND bot dir — ship-gate.md amendment 4) and the current safe-gap
countdown. Exit 1 lists what is missing. The safe-gap arithmetic is measured
(proposal SS4): rated slots fire at :X2:43 every 10.0 min and complete
~:X8:30, so the swap loop window is ~X8:30 -> next :X2:43 (~4m13s).
"""
from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path

REQUIRED = ("produces", "falsifier", "treatment_occurrence", "S5_unrated")
SURVIVAL_WORDS = re.compile(r"\bsurviv|\bpersist", re.IGNORECASE)


def prereg_text(dev_dir: Path) -> tuple[str, Path | None]:
    for name in ("PREREG.md", "README.md"):
        p = dev_dir / name
        if p.exists():
            return p.read_text(errors="replace"), p
    return "", None


def field(text: str, key: str) -> str | None:
    m = re.search(rf"^\s*[*-]?\s*`?{key}`?\s*[:=]\s*(.+)$", text,
                  re.IGNORECASE | re.MULTILINE)
    return m.group(1).strip() if m else None


def safe_gap_line(now: datetime) -> str:
    # Slots at minute % 10 == 2, second 43; completion ~ minute % 10 == 8,
    # second 30. Safe window: [X8:30, next X2:43] — it wraps the 10-min cycle.
    sec = (now.minute % 10) * 60 + now.second   # position in cycle, [0, 600)
    fire_s, open_s = 2 * 60 + 43, 8 * 60 + 30   # :X2:43 fire, ~:X8:30 complete
    if sec < fire_s:                            # tail of the wrapped gap
        return (f"safe gap OPEN NOW, ~{fire_s - sec}s until the :X2:43 slot — "
                f"rollback must land before it")
    if sec < open_s:                            # rated match in flight
        return (f"rated match in flight; safe gap opens in ~{open_s - sec}s "
                f"(window ~4m13s; submit -> 5 unrated -> submit parent)")
    return (f"safe gap OPEN NOW, ~{600 + fire_s - sec}s until the :X2:43 slot")


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    dev = Path(sys.argv[1])
    if not dev.is_dir():
        print(f"FAIL  {dev} is not a directory")
        return 1

    text, src = prereg_text(dev)
    missing, notes = [], []
    for key in REQUIRED:
        val = field(text, key)
        if not val:
            missing.append(key)
        elif key == "produces" and SURVIVAL_WORDS.search(val):
            notes.append(f"WARN  produces: names a survival/persistence metric "
                         f"('{val[:60]}') — those never carry verdict weight "
                         f"(builder-method.md §11.1, the SITE lesson)")

    if src is None:
        print(f"FAIL  no PREREG.md or README.md in {dev} — write the S0 block "
              f"before the build, not after the battery")
        return 1

    # ------------------------------------------------------------------
    # IDENTITY, not just STRUCTURE. Added 2026-08-10 after this gate printed
    # "READY TO SHIP" for bots/_v132loki15 while reading bots/_v124loki8's
    # pre-registration — inherited when the tree was copied. Every required
    # field was present and valid, because they were the SOURCE's fields.
    #
    # The gate validated the SHAPE of its input and never asked whether the
    # input was ABOUT THE BOT IT WAS BLESSING. Same instrument family as
    # ship_watch reading a stalled tape and reporting it as current: an
    # instrument that confirms the shape of its input but not its identity,
    # and emits a confident GO either way.
    #
    # Emptying each copied PREREG.md by hand is whack-a-mole — the next copy
    # re-inherits and this gate blesses it again. The check belongs HERE.
    # ------------------------------------------------------------------
    dirname = dev.name
    if dirname not in text:
        print(f"FAIL  {src.name} never mentions '{dirname}'.")
        print(f"      A pre-registration that does not name the tree it is filed")
        print(f"      under is almost certainly INHERITED FROM A COPIED BOT, and")
        print(f"      this gate would otherwise pass it — every required field is")
        print(f"      present, because they are the SOURCE bot's fields.")
        print(f"      Leg preregs live in docs/prereg/ with both clocks; a bot")
        print(f"      directory is code. Empty this file to a pointer or write")
        print(f"      the real one.")
        return 1
    for n in notes:
        print(n)
    if missing:
        print(f"NOT READY — {src.name} is missing: {', '.join(missing)}")
        print("      An empty field is visible in a way a forgotten step is not.")
        return 1

    print("READY TO SHIP — pre-registration complete.")
    print(f"  {safe_gap_line(datetime.now())}")
    print("  Tape row must carry (ship-gate.md amendment 4):")
    print(f"    join key:  vNN + {dev}   <- BOTH, or the gate<->ladder join dies")
    print(f"    S5_unrated: {field(text, 'S5_unrated')}")
    print(f"    treatment_occurrence: {field(text, 'treatment_occurrence')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
