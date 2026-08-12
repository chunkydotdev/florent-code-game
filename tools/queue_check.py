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
    return f"#{num} {name[:58]}"


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
        ("a DEAD-section row is still excluded without the text marker",
         "## DEAD\n| 1 | **thing** | GREP: PASS | metric |\n", 0),
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

    parsed = parse(QUEUE.read_text())
    live = unblocked(parsed)
    print(f"QUEUE FLOOR CHECK — unblocked items: {len(live)} (floor {args.floor})")
    for section, row in live:
        print(f"   {label(row)}")
    # Migration visibility: these are the rows the substring era silently dropped.
    # They COUNT now. Printed so the reclassification is auditable rather than quiet
    # -- if one is genuinely not startable, give it a STATUS: token.
    warn = legacy_warnings(parsed)
    if warn:
        print(f"   ⚠ {len(warn)} counted row(s) carry a legacy marker word in prose "
              f"(no STATUS: token, so NOT blocked):")
        for lbl, hits in warn:
            print(f"       {lbl[:52]}  [{', '.join(hits)}]")
    if len(live) < args.floor:
        print()
        print(f"*** QUEUE ALARM: {len(live)} < {args.floor}. THIS IS A RESEARCH FAILURE,")
        print("    NOT A BUILDER PAUSE. Stock it before doing anything else.")
        local_runs()
        return 1
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
