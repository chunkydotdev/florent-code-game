#!/usr/bin/env python3
"""QUEUE FLOOR ALARM — is there anything the builder can start TODAY?

Magnus, 2026-08-11 (s31): "please make sure there always is new items on the
list for the builder to build and test, if the queue runs empty we go stale,
that is not acceptable."

WHY THIS EXISTS, and it is a measured failure rather than a tidy idea.
`QUEUE.md` was audited at 15:2xZ on 2026-08-11 and read: 1 shipped, 2 "next up",
1 blocked, 4 dead. It LOOKED stocked. It had **zero items the builder could
start**, because #2 was blocked on a number research owed, #3 was gated on #4,
and #4 was a research cut rather than a plank. Every blocker was research's own.

    ⇒ A QUEUE CAN READ FULL AND BE EMPTY. Counting rows is the wrong check;
      counting UNBLOCKED rows is the right one.

FLOOR = 3 unblocked items. Exit 1 below it. Research runs this at boot, after
every item is consumed, and at wrap.

    .venv/bin/python tools/queue_check.py [--floor N] [--selftest]

⛔ WHAT COUNTS AS BLOCKED — deliberately generous, because the failure mode is
an item that LOOKS ready. A row is blocked if its text carries a blocker marker
(BLOCKED / gated / "needs a number" / "settles it first"), or if it sits under a
section heading naming it blocked, or if it is already shipped/dead.
A row must be affirmatively startable to count.

⚠ KNOWN AND DELIBERATE: THE MATCHER UNDERCOUNTS, AND THAT IS THE SAFE DIRECTION.
It matches substrings against the whole row INCLUDING prose, so a startable item
that merely MENTIONS a blocked or shipped sibling is excluded. Measured on the
2026-08-11 file: it reported 4 where 6 were genuinely startable — #6 was dropped
for the words "dead-list entry" and #9 for "we just shipped the other direction".

    ⇒ It errs toward RAISING THE ALARM EARLY, never toward a false OK.
      Do not "fix" it into a smarter matcher that could miss a real emptiness;
      if you want the true count, read the file. This is a floor alarm, not an
      inventory.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / "QUEUE.md"
FLOOR = 3

# Substrings that disqualify a row from counting as startable. Lowercased match.
BLOCK_MARKERS = (
    "blocked", "blocker", "gated", "needs a number", "settles it first",
    "shipped", "dead", "do not re-queue", "waiting on",
    # Added 2026-08-11 after a WITHDRAWN row padded the floor: a plank that has
    # been refuted still parses as a numbered row, so the withdrawal has to be
    # read off the TEXT. Same false-positive class as the decomposition table.
    "withdrawn", "refuted",
)
# Section headings whose rows never count toward the floor.
DEAD_SECTIONS = ("## FIRING NOW", "## BLOCKED", "## DEAD")


def parse(text: str):
    """-> list of (section, row_text). Table rows only, header/rule rows dropped."""
    out, section = [], "(none)"
    for line in text.splitlines():
        if line.startswith("## "):
            section = line.strip()
            continue
        if not line.startswith("| "):
            continue
        if line.startswith("|---") or re.match(r"\|\s*#\s*\|", line):
            continue
        out.append((section, line))
    return out


def _is_plank_row(row: str) -> bool:
    """First cell must be a plank ID -- a bare number, possibly bold/struck.

    ⛔ THIS GUARD EXISTS BECAUSE THE TOOL COUNTED A DECOMPOSITION TABLE AS A PLANK.
    On 2026-08-11 a research decomposition (`| **product** | **3.36x** | = the
    anchor |`) sat inside a queue section and was reported as an unblocked queue
    item. That is a FALSE POSITIVE -- the tool claiming the floor is met when it
    is not -- which is the UNSAFE direction and the opposite of the undercount
    documented above. A floor alarm that can be padded by a stray table is not
    a floor alarm.
    """
    cells = [c.strip() for c in row.strip().strip("|").split("|")]
    if not cells:
        return False
    head = re.sub(r"[*~`\s]", "", cells[0])
    return head.isdigit()


def unblocked(rows):
    live = []
    for section, row in rows:
        if any(section.startswith(d) for d in DEAD_SECTIONS):
            continue
        if not _is_plank_row(row):
            continue
        low = row.lower()
        if any(m in low for m in BLOCK_MARKERS):
            continue
        live.append((section, row))
    return live


def label(row: str) -> str:
    cells = [c.strip() for c in row.strip().strip("|").split("|")]
    num = cells[0].strip("* ") if cells else "?"
    name = re.sub(r"[*⭐⛔]", "", cells[1]).strip() if len(cells) > 1 else "?"
    return f"#{num} {name[:58]}"


def selftest() -> int:
    """Forced-answer cells. Each MUST come out the other way from its neighbour;
    a checker that has never returned the other verdict has not been seen to check."""
    cases = [
        # (name, markdown, expected unblocked count)
        ("empty file", "# QUEUE\n", 0),
        ("one clean row",
         "## NEXT UP\n| # | p |\n|---|---|\n| 1 | **thing** | change | metric |\n", 1),
        ("row carrying BLOCKED is not counted",
         "## NEXT UP\n| 1 | **thing** | BLOCKED on a number |\n", 0),
        ("row under ## BLOCKED is not counted",
         "## BLOCKED\n| 1 | **thing** | change |\n", 0),
        ("row under ## DEAD is not counted",
         "## DEAD\n| 1 | **thing** | change |\n", 0),
        ("shipped row is not counted",
         "## FIRING NOW\n| 1 | **thing** | SHIPPED 13:14Z |\n", 0),
        ("gated row is not counted",
         "## NEXT UP\n| 1 | **thing** | gated on the attribution cut |\n", 0),
        ("header and rule rows are not rows",
         "## NEXT UP\n| # | plank |\n|---|---|\n", 0),
        ("three clean rows meet the floor",
         "## NEXT UP\n| 1 | **a** | c |\n| 2 | **b** | c |\n| 3 | **c** | c |\n", 3),
        # The false-positive cell. A decomposition table inside a queue section
        # padded the floor on 2026-08-11; this is the regression test for it.
        ("a non-plank table row does NOT count",
         "## NEXT UP\n| **product** | **3.36x** | = the anchor |\n", 0),
        ("a struck-through plank id still counts as a row",
         "## NEXT UP\n| ~~3~~ | **a** | c |\n", 1),
        ("a WITHDRAWN row does NOT count (it still parses as a numbered row)",
         "## NEXT UP\n| ~~3~~ | ~~**a**~~ | **WITHDRAWN — premise refuted** |\n", 0),
    ]
    bad = 0
    for name, md, want in cases:
        got = len(unblocked(parse(md)))
        ok = got == want
        bad += not ok
        print(f"  [{'ok' if ok else 'FAIL'}] {name}: expected {want}, got {got}")
    # The reproduction cell: the real file must parse without raising.
    try:
        n = len(unblocked(parse(QUEUE.read_text())))
        print(f"  [ ok ] live QUEUE.md parses: {n} unblocked")
    except Exception as exc:                                  # pragma: no cover
        print(f"  [FAIL] live QUEUE.md raised: {exc}")
        bad += 1
    print("SELFTEST", "PASS" if not bad else f"FAIL ({bad})")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--floor", type=int, default=FLOOR)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()

    if not QUEUE.exists():
        print(f"QUEUE ALARM: {QUEUE} does not exist.")
        return 1

    live = unblocked(parse(QUEUE.read_text()))
    print(f"QUEUE FLOOR CHECK — unblocked items: {len(live)} (floor {args.floor})")
    for section, row in live:
        print(f"   {label(row)}")
    if len(live) < args.floor:
        print()
        print(f"*** QUEUE ALARM: {len(live)} < {args.floor}. THIS IS A RESEARCH FAILURE,")
        print("    NOT A BUILDER PAUSE. Stock it before doing anything else.")
        return 1
    print("   OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
