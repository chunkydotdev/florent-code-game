#!/usr/bin/env python3
"""QUEUE FLOOR ALARM — is there anything the builder can start TODAY?

⛔⛔ THIS FILE IS EXECUTED BY THE `SessionStart` HOOK IN `.claude/settings.json`,
SO ITS BLAST RADIUS IS EVERY LANE'S BOOT, NOT YOUR TERMINAL. A crash here does
not read as "tool broken" -- the hook branches on a non-zero exit and prints a
DIRECTIVE naming the research lane, so a SyntaxError makes every booting session
be told the queue is below floor while it is full. That happened for 22 seconds
on 2026-08-12 (2eae63f -> 0f2632c). ⇒ RUN `--selftest` BEFORE EVERY PUSH of this
file; nothing else in it warns you what it is wired into.

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

⛔ WHAT COUNTS AS BLOCKED — STRUCTURAL SINCE 2026-08-12 (s33). A row is blocked
only if it carries an explicit `STATUS: <reason>` token, or sits under a dead
section heading (`## FIRING NOW` / `## BLOCKED` / `## DEAD` / `## DONE`).
Prose may say anything. A row must be affirmatively startable to count.

⛔⛔ THE PARAGRAPH THAT USED TO SIT HERE IS OVERTURNED, AND IT IS KEPT IN SUMMARY
BECAUSE THE OVERTURNING IS THE POINT. It read: *"THE MATCHER UNDERCOUNTS, AND
THAT IS THE SAFE DIRECTION… it errs toward raising the alarm early, never toward
a false OK… the correct response is to GENERATE, not to loosen the matcher."*
It even named the exact case that finally broke it -- item #10's grep stamp
citing `eco.py:pave_blocked_by_ore` -- and prescribed generating more items.

**BOTH HALVES OF THAT ARGUMENT ARE FALSE, AND IT PREDICTED ITS OWN FAILURE AND
PRESCRIBED THE WRONG RESPONSE:**

1. **"Never toward a false OK" was the wrong axis.** Under `QUEUE_OWNER: research`
   and Magnus's *"if the queue runs empty we go stale"*, an UNDERCOUNT pressures
   research to MANUFACTURE items while finished, audited ones sit unread. An
   overcount pads the floor; an undercount creates busywork AND hides work. Both
   are Goodhart, opposite signs -- only one was priced.
2. **It is biased against quality, not noisy around it.** A row acquires the words
   *withdrawn* / *refuted* / *blocked* precisely BECAUSE it was audited and the
   correction was recorded inline with its provenance -- the house style. So the
   filter removed the rows carrying the MOST scrutiny. Measured 2026-08-12: the
   count read 8 where 11 were startable; #5 (GREP: PASS) died to "withdrawn" in a
   sentence continuing *"BUT NOT CLOSED"*, #3 to "refuted" in its own title, #10
   to a symbol name quoted as the evidence it IS startable. **The builder started
   #5 while this tool reported it unstartable.**

⚠ THE NEW RISK, NAMED RATHER THAN ASSUMED AWAY: a genuinely blocked row whose
author forgets the `STATUS:` token now COUNTS -- a false OK, which is the failure
the old caution feared. **Mitigation, and why this is not a straight trade:**
`legacy_warnings()` prints every counted row still carrying a blocker word in
prose, on every run. A forgotten STATUS on a row that reads as blocked is
therefore VISIBLE each time, where the old scheme's false negatives were SILENT.
A wrong count you can see beats a wrong count you cannot.

    ⇒ Still true, and unchanged: this is a floor alarm, not an inventory. Do not
      tune it to hit a number. The repair here was to make status STRUCTURAL, not
      to loosen a threshold -- and rewording QUEUE.md around the matcher (which
      this lane did once, `withdrawn` -> `RETRACTED`) is the repair this file
      already warns against and is NOT the fix.
"""
from __future__ import annotations

import argparse
import re
import sys
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
QUEUE = ROOT / "QUEUE.md"
FLOOR = 3

# ⛔⛔ THE SUBSTRING ERA IS OVER — REPLACED 2026-08-12 (s33) AFTER IT WAS MEASURED
# HIDING THREE STARTABLE ITEMS AT ONCE.
#
# Scanning the whole row for words like "blocked"/"withdrawn"/"refuted" fails in
# NORMAL PROSE, not in edge cases, and it fails SYSTEMATICALLY IN ONE DIRECTION:
#
#   #5  CRASH INDUCTION AT SCALE  GREP: PASS  killed by "withdrawn"
#         -- from "...IS WITHDRAWN AS A RANKING CLAIM. BUT NOT CLOSED"
#   #3  CLEAR MORE ENEMY TURRETS              killed by "withdrawn","refuted"
#         -- from its own title: '(was "we go forward late" -- refuted; ...)'
#   #10 BLIND THEIR GUN WITH THEIR OWN BODY  GREP: PASS  killed by "blocked"
#         -- from a SYMBOL NAME in its grep stamp: `eco.py:pave_blocked_by_ore`
#
# The count read 8; the true count was 11. #10 is the purest case: excluded by a
# function name in our own codebase, quoted as the evidence that it IS startable.
# This file had ALREADY removed "shipped" for firing on "NOT shipped" and wrote
# the caution down -- and the replacement inherited the same defect (D68).
#
# ⭐ AND IT IS BIASED AGAINST QUALITY, NOT NOISY AROUND IT. A row acquires the
# words "withdrawn"/"refuted"/"blocked" precisely BECAUSE it has been audited and
# the correction was recorded inline with its provenance -- which is the house
# style. So the filter removed the rows carrying the MOST scrutiny.
#
# ⛔ AND "the undercount is the safe direction" -- asserted in this file's own
# docstring -- IS FALSE HERE. Under QUEUE_FLOOR=3 and "if the queue runs empty we
# go stale", an undercount pressures RESEARCH (the queue owner) to manufacture new
# items while finished thinking sits unread. An overcount pads the floor; an
# undercount creates busywork AND hides work. Both are Goodhart, opposite signs.
#
# ⇒ STATUS IS NOW STRUCTURAL. A row is not startable only if it carries an
#   explicit `STATUS: <reason>` token, or sits under a dead section heading.
#   Prose can say anything. Diagnosis and the `## DONE` design: side lane.
# `note` added s33: a SCOPING row (context a builder must read, with nothing to
# build) was counting toward the floor. It declared `GREP: N/A`, metric `n/a` and
# fixture `n/a` and still counted -- the first row to declare N/A on all three and
# be admitted. The floor means "startable TODAY", so a note is not floor material
# even when it is one of the most useful rows on the queue.
# ⚠ `demoted` is RETAINED but is ambiguous and both readings are live: as a STATUS
# token it means BLOCKED (#12, waiting on a control) and in prose it has meant
# DEPRIORITISED-but-startable (#20). Prefer STATUS: BLOCKED for the first sense;
# the same word must not read the same and behave differently.
# A `grep:` whose VALUE is a promise rather than a result does not satisfy the gate.
UNMET_GREP_RE = re.compile(r"grep:\s*\**\s*(todo|tbd|not run|not yet|pending|n/a)", re.I)

STATUS_RE = re.compile(
    r"status:\s*(blocked|done|answered|note|demoted|withdrawn|refuted"
    r"|superseded|waiting|shipped)",
    re.I,
)

# Kept ONLY to emit a migration warning, never to exclude a row. A row containing
# one of these in prose with no STATUS token is COUNTED and flagged, so the change
# surfaces rows rather than silently flipping them. Empty this list once QUEUE.md
# is fully migrated.
LEGACY_MARKERS = (
    "blocked", "blocker", "gated", "needs a number", "settles it first",
    "do not re-queue", "waiting on",
    # "shipped" and "dead" were REMOVED as text markers on 2026-08-11. Both are
    # already handled by DEAD_SECTIONS (## FIRING NOW / ## DEAD), and as
    # substrings they fired on legitimate rows: an incumbent-grep stamp reading
    # "NOT shipped" -- i.e. the very evidence that an item IS startable -- was
    # excluding it. The undercount is the safe direction but it was wrong here,
    # and rewording the queue around a tool's bug is the wrong repair.
    # Added 2026-08-11 after a WITHDRAWN row padded the floor: a plank that has
    # been refuted still parses as a numbered row, so the withdrawal has to be
    # read off the TEXT. Same false-positive class as the decomposition table.
    "withdrawn", "refuted",
    # Added 2026-08-11 (third false positive of the day): a row DEMOTED pending a
    # control still parses as numbered and unblocked. Every one of these three
    # false positives inflated the count -- the UNSAFE direction -- while the
    # documented undercount deflates it. Padding the floor is the failure mode
    # the GREP gate exists to stop, so each gets a regression cell.
    "do not build", "demoted",
)
# Section headings whose rows never count toward the floor.
# `## DONE` is deliberately SEPARATE from `## DEAD`: `## DEAD` means the road was
# REFUTED ("do not re-queue without new evidence"); `## DONE` means the item
# DELIVERED ITS NUMBER. Merging them corrupts the history a successor reads --
# #15 (answered, with a document) is exactly the row that would be misfiled.
DEAD_SECTIONS = ("## FIRING NOW", "## BLOCKED", "## DEAD", "## DONE")


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


def row_numbers(text: str):
    """-> list of (number, kind, snippet) for every ROW IDENTIFIER in the file.

    ⛔ TWO FORMS, AND THE SECOND IS WHY THIS EXISTS. On 2026-08-12 two lanes wrote
    `#32` fifteen minutes apart: research added a TABLE ROW (`| **32** | ... |`)
    and the builder added a SECTION HEADING (`### ⭐⭐⭐ #32 — OUR SENTINELS DIE
    ...`). A checker that scanned table rows ONLY would have reported no
    duplicate on the exact incident that motivated it -- the `parse()` above is
    table-rows-only by design, so reusing it here would have been that bug.

    The cost is not cosmetic and that is why this is an alarm rather than a note:
    the side lane audited the BUILDER's #32 and routed the finding to RESEARCH,
    because the number had been research's an hour earlier. **A collided number
    silently misroutes an audit to the wrong author**, and nothing detected it.
    """
    out = []
    for line in text.splitlines():
        if line.startswith("| "):
            if line.startswith("|---") or re.match(r"\|\s*#\s*\|", line):
                continue
            first = line.strip().strip("|").split("|")[0]
            m = re.fullmatch(r"[\s*~]*(\d+)[\s*~]*", first)
            if m:
                # A struck-through id (`~~2~~`) is a TOMBSTONE, not a live row.
                tomb = "~~" in first
                out.append((int(m.group(1)),
                            "tombstone" if tomb else "table row", line[:70] + ("…" if len(line) > 70 else "")))
        elif line.startswith("#"):
            m = re.search(r"#(\d+)\s*[—-]", line)
            if m:
                out.append((int(m.group(1)), "heading", line[:70] + ("…" if len(line) > 70 else "")))
    return out


def duplicate_numbers(text: str):
    """-> sorted list of (number, [(kind, snippet), ...]) for LIVE collisions.

    ⛔ TOMBSTONES DO NOT COLLIDE, AND THIS IS NOT LENIENCY -- IT IS WHAT KEEPS THE
    ALARM READABLE. `QUEUE.md` retires a plank as `~~2~~` and reuses the number
    for a new row; that is an established convention here (two instances). Firing
    on it every run would print three "duplicates" of which one is real, and an
    alarm that is mostly noise is how the REAL collision gets scrolled past --
    the failure this check exists to catch. A group alarms only when it holds two
    or more LIVE identifiers.
    """
    seen = {}
    for num, kind, snip in row_numbers(text):
        seen.setdefault(num, []).append((kind, snip))
    out = []
    for n, uses in sorted(seen.items()):
        if sum(1 for k, _ in uses if k != "tombstone") > 1:
            out.append((n, uses))
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
    """Startable = plank row, no blocker marker, AND the incumbent grep has run.

    ⛔ THE `GREP:` REQUIREMENT EXISTS BECAUSE THIS ALARM WAS GOODHARTED BY ITS OWN
    AUTHOR, WITHIN HALF AN HOUR OF BEING WRITTEN. A floor of 3 is a TARGET, and a
    target gets met: the queue was stocked to "6 startable items" at 13:27 and by
    13:51 THREE of the six were withdrawn (ring retention, launcher delivery,
    idle-builder defence) because the disqualifying check ran AFTER admission
    rather than before it. Net effect: the file advertised work that did not
    exist -- which is precisely the "reads full and is empty" failure the alarm
    was built to catch, reproduced by the alarm.

    `CLAUDE.md` already carries the rule -- "before pre-registering any plank,
    grep the incumbent for the behaviour: the cheapest possible null is a leg
    that tests a feature we already shipped" -- but it fires at PREREG, which is
    downstream of admission. Moving it upstream costs ~2 minutes per item.

        ⇒ A row counts only if it carries `GREP:` naming what was checked and
          what was found. An honest 3 that FIRES beats a padded 6 that cannot.
          Raised by the side lane; the diagnosis is theirs.
    """
    live = []
    for section, row in rows:
        if any(section.startswith(d) for d in DEAD_SECTIONS):
            continue
        if not _is_plank_row(row):
            continue
        low = row.lower()
        if STATUS_RE.search(low):
            continue
        if "grep:" not in low:
            continue
        # ⛔ THE GATE TESTED FOR THE STRING, NOT FOR A RESULT. `GREP: TODO BEFORE
        # BUILD` passed it -- a row satisfying the gate by writing the gate's name
        # while its own text says the gate is UNMET. That is the literal form of the
        # Goodhart this gate exists to stop, and it is the same substring-for-state
        # failure as the old `blocked` matcher, one column over. The row that found
        # it (#26) was transparently honest; the COUNTER was wrong, not the author.
        # Class fixed rather than the instance: the next author writing `GREP: TODO`
        # would otherwise be counted again, and the risk is not a floor reading 17 --
        # it is a builder pulling the top item and building a plank whose incumbent
        # check was never run, which is the cheapest null this repo produces.
        if UNMET_GREP_RE.search(low):
            continue
        live.append((section, row))
    return live


def legacy_warnings(rows):
    """Rows counted as startable that still carry a legacy marker word in prose.

    These are the rows the substring era was silently dropping. They are COUNTED
    now; this exists so the change is visible rather than a quiet reclassification.
    If one of them really is blocked, give it a `STATUS:` token -- do not reword
    the prose, which is the repair this file's own docstring warns against.
    """
    out = []
    for _, row in live_rows(rows):
        low = row.lower()
        hits = [m for m in LEGACY_MARKERS if m in low]
        if hits:
            out.append((label(row), hits))
    return out


def live_rows(rows):
    return unblocked(rows)


def label(row: str) -> str:
    cells = [c.strip() for c in row.strip().strip("|").split("|")]
    num = cells[0].strip("* ") if cells else "?"
    name = re.sub(r"[*⭐⛔]", "", cells[1]).strip() if len(cells) > 1 else "?"
    # ⛔ Ellipsis when and ONLY when cut (side lane flag, 2026-08-16): a
    # truncated title and a complete one were byte-indistinguishable, and the
    # cut lands on the tail — where scope qualifiers live. #63's "ON MIDGARD"
    # vanished at this width and a map-specific row briefed an agent as a
    # general one. A constant marker would validate anything, so the ellipsis
    # appears only on an actual cut (selftest drives both cells).
    return f"#{num} {name[:58]}" + ("…" if len(name) > 58 else "")


def selftest() -> int:
    """Forced-answer cells. Each MUST come out the other way from its neighbour;
    a checker that has never returned the other verdict has not been seen to check."""
    cases = [
        # (name, markdown, expected unblocked count)
        ("empty file", "# QUEUE\n", 0),
        ("one clean row",
         "## NEXT UP\n| # | p |\n|---|---|\n| 1 | **thing** | GREP: PASS | metric |\n", 1),
        # ⛔ EVERY STATUS CELL BELOW NOW CARRIES `GREP: PASS`. THREE OF THE OLD
        # MARKER CELLS DID NOT, so they returned 0 because of the MISSING GREP and
        # never exercised the marker logic at all -- they passed for the wrong
        # reason and would have passed with the marker code deleted. Same family as
        # the effective_n ceiling cell whose PASS condition was the bug.
        ("STATUS: BLOCKED is not counted (and this cell has a grep, so it tests it)",
         "## NEXT UP\n| 1 | **thing** | GREP: PASS | STATUS: BLOCKED on a number |\n", 0),
        # --- THE THREE REGRESSION CELLS. Each is a real row the substring era
        # dropped on 2026-08-12; each must now COUNT.
        ("#5 case: 'withdrawn' in PROSE with no STATUS token still counts",
         "## NEXT UP\n| 5 | **crash induction** | GREP: PASS | the ranking claim is "
         "WITHDRAWN but the road is NOT CLOSED |\n", 1),
        ("#10 case: a SYMBOL NAME containing 'blocked' does not block the row",
         "## NEXT UP\n| 10 | **blind their gun** | GREP: PASS `eco.py:pave_blocked_by_ore` "
         "| metric |\n", 1),
        ("#3 case: 'refuted' describing the item's OWN HISTORY still counts",
         "## NEXT UP\n| 3 | **clear turrets** (was 'we go forward late' — refuted; then "
         "over-sized — corrected) | GREP: PASS | metric |\n", 1),
        ("row under ## BLOCKED is not counted",
         "## BLOCKED\n| 1 | **thing** | change |\n", 0),
        ("row under ## DEAD is not counted",
         "## DEAD\n| 1 | **thing** | change |\n", 0),
        ("shipped row is not counted",
         "## FIRING NOW\n| 1 | **thing** | SHIPPED 13:14Z |\n", 0),
        ("STATUS: WAITING is not counted (grep present, so the status does the work)",
         "## NEXT UP\n| 1 | **thing** | GREP: PASS | STATUS: WAITING on the attribution cut |\n", 0),
        # The side lane's two-way cell: the SAME row text, one heading apart.
        # Without the second half a typo'd heading is a silent no-op whose failure
        # state is indistinguishable from a legitimately open item.
        ("same row text under ## DONE does NOT count",
         "## DONE\n| 15 | **effective n** | GREP: PASS | answered |\n", 0),
        ("same row text under ## NEXT UP DOES count",
         "## NEXT UP\n| 15 | **effective n** | GREP: PASS | answered |\n", 1),
        ("header and rule rows are not rows",
         "## NEXT UP\n| # | plank |\n|---|---|\n", 0),
        ("three clean rows meet the floor",
         "## NEXT UP\n| 1 | **a** | GREP: PASS |\n| 2 | **b** | GREP: PASS |\n| 3 | **c** | GREP: PASS |\n", 3),
        # The false-positive cell. A decomposition table inside a queue section
        # padded the floor on 2026-08-11; this is the regression test for it.
        ("a non-plank table row does NOT count",
         "## NEXT UP\n| **product** | **3.36x** | = the anchor |\n", 0),
        ("a struck-through plank id still counts as a row",
         "## NEXT UP\n| ~~3~~ | **a** | GREP: PASS |\n", 1),
        ("a STATUS: WITHDRAWN row does NOT count (it still parses as a numbered row)",
         "## NEXT UP\n| ~~3~~ | ~~**a**~~ | GREP: PASS | **STATUS: WITHDRAWN — premise refuted** |\n", 0),
        # The Goodhart cell: an item with no incumbent grep does not count, even
        # though it is numbered, unblocked and reads as ready.
        ("a row with NO incumbent grep does NOT count",
         "## NEXT UP\n| 1 | **thing** | change | metric |\n", 0),
        ("the same row WITH a grep does count",
         "## NEXT UP\n| 1 | **thing** | GREP: PASS not shipped | metric |\n", 1),
        ("a STATUS: DEMOTED row does NOT count",
         "## NEXT UP\n| 12 | **thing** | GREP: PASS | STATUS: DEMOTED - do not build before the control runs |\n", 0),
        # The bias cell: an item whose prose records EVERY legacy marker word, as
        # audit history, must still count. This is the whole 2026-08-12 defect in
        # one row -- the filter was removing the rows carrying the most scrutiny.
        ("a heavily-audited row naming every legacy marker in prose still counts",
         "## NEXT UP\n| 9 | **thing** | GREP: PASS `eco.py:pave_blocked_by_ore` | was "
         "refuted, then withdrawn as a ranking claim, was gated, blocker cleared |\n", 1),
        # THE TWO-WAY CELL FOR THE UNMET GREP. Same row text, one word different.
        ("a row whose GREP is a RESULT counts",
         "## NEXT UP\n| 26 | **thing** | GREP: PASS — checked eco.py, not present | metric |\n", 1),
        ("the SAME row with GREP: TODO does NOT count",
         "## NEXT UP\n| 26 | **thing** | GREP: TODO — must be run before build | metric |\n", 0),
        ("GREP: N/A on a plank row does NOT count",
         "## NEXT UP\n| 26 | **thing** | GREP: N/A | metric |\n", 0),
        ("a DEAD-section row is still excluded without the text marker",
         "## DEAD\n| 1 | **thing** | GREP: PASS | metric |\n", 0),
    ]
    bad = 0
    for name, md, want in cases:
        got = len(unblocked(parse(md)))
        ok = got == want
        bad += not ok
        print(f"  [{'ok' if ok else 'FAIL'}] {name}: expected {want}, got {got}")
    # --- TRUNCATION-MARKER CELLS (side lane flag, 2026-08-16). The ellipsis
    # must appear on a cut title and ONLY on a cut title — a constant marker
    # validates anything, and an unmarked cut turned #63's map-scoped title
    # into a general one at every lane's boot.
    lab_long = label("| 63 | **" + "X" * 70 + "** |")
    lab_short = label("| 7 | **short title** |")
    for name, got, want in [
        ("a >58-char title carries the ellipsis", lab_long.endswith("…"), True),
        ("...and is cut at the width", len(lab_long), len("#63 ") + 59),
        ("a <=58-char title carries NO ellipsis", lab_short.endswith("…"), False),
        ("...and is intact", lab_short, "#7 short title"),
    ]:
        ok = got == want
        bad += not ok
        print(f"  [{'ok' if ok else 'FAIL'}] {name}: expected {want!r}, got {got!r}")

    # --- DUPLICATE-NUMBER CELLS. Driven both ways, and the THIRD reproduces the
    # actual 2026-08-12 incident: a TABLE ROW and a SECTION HEADING sharing #32.
    # A table-rows-only checker returns 0 on that cell -- i.e. it would have passed
    # while missing the collision it was built for. That cell is the whole point.
    dup_cases = [
        ("no duplicates -> none",
         "## NEXT UP\n| 1 | **a** |\n| 2 | **b** |\n", 0),
        ("same number twice as TABLE ROWS -> one duplicate",
         "## NEXT UP\n| 7 | **a** |\n| 7 | **b** |\n", 1),
        ("REGRESSION 2026-08-12: table row #32 + heading #32 -> one duplicate",
         "## NEXT UP\n| **32** | **ablate the flag** |\n\n### #32 — OUR SENTINELS DIE\n", 1),
        ("two headings sharing a number -> one duplicate",
         "### #9 — alpha\n### #9 — beta\n", 1),
        # ⛔ FLIPPED s34 AFTER THE LIVE RUN: a struck-through id is a TOMBSTONE and
        # reusing its number is an established convention here. Firing on it printed
        # 3 duplicates of which 1 was real -- noise that buries the real one.
        ("a struck-through id is a TOMBSTONE and does NOT collide",
         "## NEXT UP\n| ~~4~~ | **a** |\n| 4 | **b** |\n", 0),
        ("TWO tombstones plus a live row still do NOT collide",
         "## NEXT UP\n| ~~4~~ | **a** |\n| ~~4~~ | **b** |\n| 4 | **c** |\n", 0),
        ("but two LIVE rows sharing a number DO collide",
         "## NEXT UP\n| ~~4~~ | **a** |\n| 4 | **b** |\n| 4 | **c** |\n", 1),
        ("different numbers do NOT collide",
         "## NEXT UP\n| **32** | **a** |\n\n### #33 — b\n", 0),
    ]
    for name, md, want in dup_cases:
        got = len(duplicate_numbers(md))
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


def current_incumbent() -> str | None:
    """The `INCUMBENT:` field from PROGRAMME.md, as a bare tree name, or None."""
    prog = ROOT / "PROGRAMME.md"
    if not prog.exists():
        return None
    for line in prog.read_text().splitlines():
        s = line.strip()
        if s.startswith("INCUMBENT:"):
            return s.split(":", 1)[1].strip().rsplit("/", 1)[-1] or None
    return None


def grep_staleness(rows, incumbent: str | None):
    """Rows whose `GREP:` names a tree that is NOT the current incumbent.

    ⛔ WHY THIS EXISTS — THE GATE PROVES A CHECK WAS RUN, NEVER THAT ITS RESULT
    IS STILL TRUE. `PROGRAMME.md` denominates the `GREP:` gate in *"what was
    checked in the INCUMBENT"*, so **the moment the incumbent moves, every row's
    grep is potentially stale BY DEFINITION.** It moved on 2026-08-13 at
    04:45:54Z (v116 `_v169launchlate160` -> v122 `_v178salt`) and no row had been
    re-checked.

    The worked case: `#18` ("arena.py must persist per-game rows") was **honest
    when written** — `arena.py` genuinely discarded rows then — and `b4f56fa`
    shipped the fix afterwards. The row still passes admission and was sitting at
    **fire-order Tier 0**, so a repaired `cores_idle` would hand an idle builder
    a plank whose premise is false. **It was caught by a one-off manual sweep,
    which is not a gate.** This is `PROGRAMME.md`'s own *"THE FLOOR IS A TARGET
    AND TARGETS GET MET"* one layer deeper: admission makes rows honest at WRITE
    time and nothing re-checks them.

    ⚠ DELIBERATELY DOES NOT RE-RUN THE GREPS. Flagging the mismatch is what makes
    the staleness visible, and visibility is the whole gap. It also does NOT
    block a row — an unnamed tree is the common case and is reported separately
    from a WRONG tree, because "we cannot tell" and "we can tell it is stale" are
    different states and must not be summed. Spec: side lane, 2026-08-13.
    """
    named, unnamed = [], []
    if not incumbent:
        return named, unnamed
    for _section, row in rows:
        m = re.search(r"grep:\s*(.*)", row, re.I)
        if not m:
            continue
        seg = m.group(1)
        trees = set(re.findall(r"_v\d+[a-z0-9_]*", seg))
        if not trees:
            unnamed.append(label(row))
        elif incumbent not in trees:
            named.append((label(row), sorted(trees)))
    return named, unnamed


def next_action(live, inc) -> int:
    """Print ONE row — the first startable item — in full, with its control.

    ⛔ WHY THIS EXISTS. The floor check prints 52 rows, every title truncated
    mid-sentence, plus two staleness warnings and a legacy-marker list. The
    charter says "read QUEUE.md and fire from the top" — but the top is not
    shown, the ordering is not stated in the output, and QUEUE.md is ~80k
    tokens. **The first decision a session must make is the one the tooling
    helped with least.**

    This does not re-rank anything: "top" is the same first-unblocked row the
    floor check already computes. It just prints it whole, once, with the
    control it will be scored against — because a truncated title and an
    unnamed control are exactly what produced the 2026-08-15 stale-treatment
    incident, where six arms ran against a control their prereg did not name.
    """
    if not live:
        print("NEXT: nothing startable. The queue is below floor — stocking it "
              "outranks starting anything.")
        return 1
    section, row = live[0]
    cells = [c.strip() for c in row.strip().strip("|").split("|")]
    print("NEXT — the top startable queue item (same ordering as the floor check)\n")
    print(f"  SECTION: {section}")
    print(f"  CONTROL: {inc or '⚠ UNKNOWN — PROGRAMME.md has no INCUMBENT field'}")
    print("           ⛔ every arm is scored against THIS, not against what is live"
          "\n              on the ladder. They diverge when a teammate ships.\n")
    for c in cells:
        if c:
            print(f"  {c}")
    print("\n  Full row text is above verbatim — nothing truncated. Before building:")
    print("    1. tools/target_value.py --band   (is the target worth the window?)")
    print("    2. grep the incumbent for the plank — the cheapest null is a leg")
    print("       testing something we already ship.")
    print("    3. the prereg is drafted by a FRESH opus subagent, ratified by you.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Build-queue floor alarm. --next prints the single top "
                    "startable item instead of the whole list.")
    ap.add_argument("--floor", type=int, default=FLOOR)
    ap.add_argument("--next", action="store_true",
                    help="print ONE row — the top startable item — in full")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()

    if not QUEUE.exists():
        print(f"QUEUE ALARM: {QUEUE} does not exist.")
        return 1

    text = QUEUE.read_text()
    if args.next:
        return next_action(unblocked(parse(text)), current_incumbent())
    dupes = duplicate_numbers(text)
    parsed = parse(text)
    live = unblocked(parsed)
    print(f"QUEUE FLOOR CHECK — unblocked items: {len(live)} (floor {args.floor})")
    for section, row in live:
        print(f"   {label(row)}")

    # --- GREP STALENESS vs the CURRENT incumbent -------------------------
    inc = current_incumbent()
    if inc:
        stale, unnamed = grep_staleness(live, inc)
        if stale:
            print(f"   ⛔ GREP STALE — incumbent is {inc}; these were checked "
                  f"against another tree ({len(stale)}):")
            for lbl, trees in stale[:8]:
                print(f"       {lbl[:52]}{'…' if len(lbl) > 52 else ''}  [checked: {', '.join(trees)}]")
        if unnamed:
            print(f"   ⚠ GREP TREE UNNAMED ({len(unnamed)} of {len(live)}) — the "
                  f"gate cannot tell whether these are stale. Incumbent: {inc}")
        if not stale and not unnamed:
            print(f"   ✅ every GREP names the current incumbent ({inc})")
    else:
        print("   ⚠ BLIND: PROGRAMME.md has no INCUMBENT field — staleness unchecked")
    # Migration visibility: these are the rows the substring era silently dropped.
    # They COUNT now. Printed so the reclassification is auditable rather than quiet
    # -- if one is genuinely not startable, give it a STATUS: token.
    warn = legacy_warnings(parsed)
    if warn:
        print(f"   ⚠ {len(warn)} counted row(s) carry a legacy marker word in prose "
              f"(no STATUS: token, so NOT blocked):")
        for lbl, hits in warn:
            print(f"       {lbl[:52]}{'…' if len(lbl) > 52 else ''}  [{', '.join(hits)}]")
    if dupes:
        print()
        print(f"*** QUEUE ALARM: {len(dupes)} DUPLICATE ROW NUMBER(S). Three lanes write")
        print("    this file and numbering is a shared counter with no lock. A collided")
        print("    number MISROUTES AN AUDIT TO THE WRONG AUTHOR (measured 2026-08-12).")
        for num, uses in dupes:
            print(f"    #{num} used {len(uses)}x:")
            for kind, snip in uses:
                print(f"        [{kind}] {snip}")
        print("    ⇒ renumber the LATER row and update every reference to it.")

    if len(live) < args.floor:
        print()
        print(f"*** QUEUE ALARM: {len(live)} < {args.floor}. THIS IS A RESEARCH FAILURE,")
        print("    NOT A BUILDER PAUSE. Stock it before doing anything else.")
        local_runs()
        # ⛔ EXIT 2 = "the floor is BREACHED". EXIT 1 is reserved for "this tool
        # FAILED and the floor is UNKNOWN". They were the same code until s33, so
        # the boot hook could not tell a real shortfall from a crash and printed
        # the same directive for both -- CLAUDE.md's own "exit code is not a health
        # signal" rule, inside our own hook. Splitting them here is the precondition;
        # the hook must still branch 2/1/0 for the fix to land. Side lane's catch.
        return 2
    if dupes:
        # ⛔ EXIT 3 = "row numbers COLLIDE". Distinct from 2 (floor breached) and 1
        # (tool broken) for the same reason those were split in s33: a caller that
        # cannot tell WHICH alarm fired prints the wrong directive. A duplicate is
        # not a shortfall -- the fix is renumbering, not stocking.
        return 3
    print("   OK")
    local_runs()
    return 0


# ---------------------------------------------------------------------------
# LOCAL-RUN BANNER — s32. Printed by the SessionStart hook in EVERY lane.
#
# ⛔ WHY THIS LIVES HERE AND NOT IN A DOC. `tools/corefill.sh` was built
# 2026-08-11 and appeared **6 times in HANDOVER.md and 0 times in all three
# `.claude/commands/*.md`, 0 in CLAUDE.md, 0 in PROGRAMME.md, 0 in QUEUE.md**.
# That is verbatim the s31 finding about QUEUE.md itself — a rule promoted into a
# file nobody opens — and it was found the same way both times: Magnus asked
# whether the next session would know.
#
# HANDOVER *is* read at boot, but it is the weakest durable surface in the repo:
# the next wrap rewrites its top block and the pointer silently drops out. The
# SessionStart hook already runs THIS file in every lane, harness-executed, so
# adding the banner here needs no settings change and cannot be forgotten.
#
# It reports STATE, not just existence — a pointer to a tool nobody knows is
# running is only half the problem. And it distinguishes BLIND from IDLE: if the
# process table cannot be read it says so rather than reporting zero, because an
# alarm that cannot tell it is blind is this repo's most-repeated defect.
def local_runs() -> None:
    import subprocess
    root = QUEUE.parent
    try:
        ps = subprocess.run(["ps", "ax", "-o", "command="],
                            capture_output=True, text=True, timeout=10).stdout
    except Exception:
        print("\nLOCAL RUNS: BLIND — cannot read the process table. "
              "NOT the same as idle; do not conclude the cores are free.")
        return
    shards = [l for l in ps.splitlines() if "overnight.sh " in l and "grep" not in l]
    filler = [l for l in ps.splitlines() if "corefill.sh" in l and "grep" not in l]
    out = root / "scratchpad" / "overnight"
    rows = 0
    if out.is_dir():
        for f in out.glob("*.tsv"):
            try:
                rows += max(0, sum(1 for _ in f.open()) - 1)
            except Exception:
                pass
    print()
    print(f"LOCAL RUNS: {len(shards)} shard(s) running, {rows} rows on disk, "
          f"filler {'UP' if filler else 'DOWN'}")
    if filler or shards:
        print("   STATUS:  zsh tools/corefill_status.sh          <- start here")
        print("   ADD:     append a line to scratchpad/corefill_work.txt")
        print("   CANCEL:  touch scratchpad/corefill_cancel/<SHARD>   (rows are KEPT)")
        print("   PAUSE:   touch scratchpad/COREFILL_STOP")
        print("   READ:    .venv/bin/python tools/overnight_read.py --dir scratchpad/overnight")
    if not filler and not shards:
        print("   *** NOTHING IS RUNNING LOCALLY. `ALWAYS_BE_RUNNING: yes` says that")
        print("       is a DEFECT. Start work from the queue above:")
        print("       zsh tools/corefill.sh scratchpad/corefill_work.txt 8 8")


if __name__ == "__main__":
    sys.exit(main())
