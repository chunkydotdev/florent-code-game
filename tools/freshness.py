#!/usr/bin/env python3
"""SHARED FRESHNESS ASSERTION — one helper, because this is one bug in four files.

    from freshness import assert_fresh, newest_row_age_h
    ok, age_h, msg = assert_fresh(ROOT/"corpus/league_matches.tsv", max_age_h=6)
    if not ok: print(msg)          # and DO NOT emit a verdict

    .venv/bin/python tools/freshness.py --selftest

IMPLEMENTS: D49 (the queue runs LIFO, so the oldest live defect survives a day
of diligent fixing -- this is the shared fix for four of them).

===== WHY THIS EXISTS =====
`CLAUDE.md` states the rule and NOTHING ENFORCED IT:

  "A monitor that reads a file must report that file's FRESHNESS. When the elo
   tape stalled, ship_watch kept printing rating=1599 armed=True RULE=held from
   rows seven minutes stale -- A HEALTHY LINE AND A BLIND LINE WERE
   BYTE-IDENTICAL."

A 2026-08-11 sweep found the same defect in four instruments, each reading a file
and none reporting its age:

  audit_trigger.py   a 24h numerator over an UNWINDOWED denominator -- the
                     `results.tsv` tail has no clock at all, so 21 "decision rows
                     in the last 24h" were all >=34 HOURS OLD. Measured on the
                     same window both sides it TRIPS. It runs on every builder
                     boot and is the mechanism that summons an audit session --
                     the one that found a 19%-power battery nobody else caught.
                     IT HAS BEEN SUPPRESSING ITS OWN ALARM ALL DAY.
  oppver_window.py   returns CLEAN off a stale tape. It HAS an UNKNOWN verdict
                     and a docstring insisting UNKNOWN is not CLEAN, and a stale
                     tape routes straight past it into CLEAN -- on Lunds
                     Stallions, its own worked example of a cell that ships
                     versions, and a live LOKI-19 cell.
  breakin_watch.py   selftest verifies a private re-implementation, not main().
  ship_watch.py      rich selftest, NO freshness assertion, fixtures dated
                     2026-01-01 -- seven months stale and all accepted as live.

===== THE DESIGN RULE THIS ENCODES =====
**STALE IS NOT A WARNING, IT IS A DIFFERENT VERDICT.** A checker that reads a
stale file must return UNKNOWN, never its healthy answer with a note attached --
because the note is on the human path and the verdict is on the machine path, and
those are not the same reader. (Measured the same day: `rate_budget` printed a
blindness warning a human would see while `--wait` returned GO to every runner.)

===== TWO CLOCKS, AND THEY DISAGREE =====
FILE MTIME says when the file was WRITTEN. The NEWEST ROW says how far the DATA
reaches. A daemon rewriting a file with nothing new keeps mtime fresh forever --
the corpus keeper logged "healthy" for 21 hours over a stale table. `assert_fresh`
reads the DATA clock by default and exposes mtime separately so a caller can
detect the divergence, which is itself the interesting signal.

⚠ AND THE ROW CLOCK IS NOT ALWAYS UTC. `elo_history.tsv` and `corpus/SHIP_ALERT`
stamp LOCAL CEST with NO ZONE MARKER, so a successor reading `05:52` as Zulu
concludes the tape is 2 HOURS FRESHER than it is -- the failure direction that
makes stale data look live. Pass `assume_local=True` for those files.
"""
from __future__ import annotations

import re
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

# Any ISO-8601-ish stamp: 2026-08-11T05:12:59.598Z, 2026-08-11T05:12, 2026-08-11 05:12:59
# Group 3 captures a trailing `Z` when the row carries one. THE MARKER IS
# AUTHORITATIVE -- see _parse.
_TS = re.compile(r"(\d{4}-\d{2}-\d{2})[T ](\d{2}:\d{2}(?::\d{2})?(?:\.\d+)?)(Z?)")
LOCAL_OFFSET_H = 2          # CEST. Only used for NAIVE rows when assume_local=True.


def _parse(day: str, clock: str, assume_local: bool,
           marker: str = "") -> datetime | None:
    """Parse one stamp. **A `Z` ON THE ROW OVERRIDES `assume_local`.**

    ⭐ WHY THE MARKER WINS (2026-08-15). `elo_history.tsv` was migrated from
    unmarked LOCAL CEST to UTC-with-`Z`. Callers pass `assume_local=True` for
    that file (`ship_watch.py:519`, `dash/serve.py:245`) because that WAS the
    right answer for every historic row. Had the writer flipped to UTC while
    those callers kept subtracting two hours, the tape would have read 2h STALE
    instead of 2h FRESH -- the same bug with the sign reversed, and reported as
    a healthy-looking alarm rather than a parse error.

    Honouring the marker makes both eras correct with NO caller change and no
    flag day: a `Z` row is UTC, a bare row falls back to the caller's
    assumption. That is also why the migration could be done at all -- there is
    no instant at which the file is half-converted and wrong.

    ⚠ `LOCAL_OFFSET_H` remains a hardcoded 2 and is WRONG for CET (+1) between
    late October and late March. It is now only reachable by NAIVE rows, i.e.
    only by historic data and by `corpus/SHIP_ALERT`. Deriving it per-row from
    the local zone is the correct fix and is left as a named debt rather than
    guessed at here.
    """
    try:
        if len(clock) == 5:
            clock += ":00"
        dt = datetime.fromisoformat(f"{day}T{clock}")
    except ValueError:
        return None
    dt = dt.replace(tzinfo=timezone.utc)
    if assume_local and marker != "Z":
        dt -= timedelta(hours=LOCAL_OFFSET_H)
    return dt


def newest_row_age_h(path: Path, *, assume_local: bool = False,
                     scan_lines: int = 400, now: datetime | None = None):
    """(age_hours, newest_dt) from the DATA in the file, or (None, None).

    Scans the tail, because these files are append-ordered and a full read of a
    237 MB events table on every boot is its own defect."""
    now = now or datetime.now(timezone.utc)
    try:
        with path.open("rb") as fh:
            try:
                fh.seek(0, 2)
                size = fh.tell()
                fh.seek(max(0, size - 200_000))
            except OSError:
                pass
            tail = fh.read().decode("utf-8", "replace")
    except OSError:
        return None, None
    newest = None
    for line in tail.splitlines()[-scan_lines:]:
        m = _TS.search(line)
        if not m:
            continue
        dt = _parse(m.group(1), m.group(2), assume_local, m.group(3))
        if dt and (newest is None or dt > newest):
            newest = dt
    if newest is None:
        return None, None
    return (now - newest).total_seconds() / 3600.0, newest


def assert_fresh(path: Path, max_age_h: float, *, assume_local: bool = False,
                 now: datetime | None = None):
    """(ok, age_h, message). ok=False means DO NOT EMIT A VERDICT.

    ok is False for missing, unparseable AND stale -- all three are the same
    thing to a caller: the file cannot support a conclusion. A caller that
    distinguishes them is welcome to read age_h (None means "no clock found")."""
    now = now or datetime.now(timezone.utc)
    path = Path(path)
    if not path.exists():
        return False, None, f"BLIND: {path.name} does not exist"
    age_h, newest = newest_row_age_h(path, assume_local=assume_local, now=now)
    if age_h is None:
        return False, None, (f"BLIND: {path.name} has no parseable timestamp in its "
                             f"tail -- cannot establish freshness, so no verdict")
    if age_h < -0.05:
        # A ROW FROM THE FUTURE IS NOT FRESHNESS, IT IS A CLOCK ERROR -- and in
        # this repo it has exactly one cause. `elo_history.tsv` and
        # `corpus/SHIP_ALERT` stamp LOCAL CEST with no zone marker, so reading
        # them as UTC puts every row 2h ahead. Measured live 2026-08-11: the elo
        # tape read -2.0h "old" as UTC and 0.0h with assume_local=True.
        # Refusing here is what stops a zone error being read as a very fresh file.
        return False, age_h, (f"CLOCK ERROR: {path.name} newest row "
                              f"{newest:%Y-%m-%dT%H:%M} is {abs(age_h):.1f}h in the "
                              f"FUTURE. A future row is a zone/clock bug, not "
                              f"freshness -- if this file stamps LOCAL time, pass "
                              f"assume_local=True. NO VERDICT.")
    mtime_age_h = (now.timestamp() - path.stat().st_mtime) / 3600.0
    div = ""
    if mtime_age_h < 1.0 and age_h > max_age_h:
        # THE DAEMON-LOOKS-HEALTHY CASE, called out explicitly because it is the
        # one where every other signal says fine.
        div = (f"  ** written {mtime_age_h*60:.0f} min ago but its DATA is "
               f"{age_h:.1f}h old -- a live writer over a stale table **")
    if age_h > max_age_h:
        return False, age_h, (f"STALE: {path.name} newest row {newest:%Y-%m-%dT%H:%M}Z "
                              f"= {age_h:.1f}h old (limit {max_age_h}h). "
                              f"VERDICT IS UNKNOWN, NOT CLEAN.{div}")
    return True, age_h, (f"fresh: {path.name} newest row {newest:%Y-%m-%dT%H:%M}Z "
                         f"= {age_h:.1f}h old (limit {max_age_h}h)")


def selftest() -> int:
    """Drive it to fresh, stale, blind and the local-timezone trap."""
    import tempfile, os
    bad = 0
    now = datetime(2026, 8, 11, 12, 0, tzinfo=timezone.utc)

    def check(label, got, want):
        nonlocal bad
        ok = got == want
        if not ok:
            bad += 1
        print(f"  [{'ok' if ok else 'FAIL'}] {label:<46} got={got} want={want}")

    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        fresh = d / "fresh.tsv"
        fresh.write_text("id\tcreated\n1\t2026-08-11T11:30:00Z\n")
        check("fresh row inside the limit", assert_fresh(fresh, 6, now=now)[0], True)

        stale = d / "stale.tsv"
        stale.write_text("id\tcreated\n1\t2026-08-09T05:12:43Z\n")
        check("stale row -> NOT ok (verdict is UNKNOWN)",
              assert_fresh(stale, 6, now=now)[0], False)

        # THE CASE THAT MATTERS MOST: only just over the line must still refuse.
        edge = d / "edge.tsv"
        edge.write_text("1\t2026-08-11T05:30:00Z\n")     # 6.5h
        check("6.5h against a 6h limit -> refuses", assert_fresh(edge, 6, now=now)[0], False)
        check("6.5h against a 7h limit -> passes", assert_fresh(edge, 7, now=now)[0], True)

        noclock = d / "noclock.tsv"
        noclock.write_text("a\tb\n1\t2\n")
        check("no parseable timestamp -> BLIND, not fresh",
              assert_fresh(noclock, 6, now=now)[0], False)

        check("missing file -> BLIND", assert_fresh(d / "nope.tsv", 6, now=now)[0], False)

        # THE LOCAL-TIMEZONE TRAP: the same row is fresh read as UTC and stale
        # read as CEST. If these two agreed, the flag would be doing nothing.
        loc = d / "local.tsv"
        loc.write_text("2026-08-11T13:30\n")   # 13:30 CEST == 11:30Z
        check("local stamp read as UTC -> FUTURE row REFUSED",
              assert_fresh(loc, 6, now=now)[0], False)
        check("...and it says CLOCK ERROR, not 'fresh'",
              "CLOCK ERROR" in assert_fresh(loc, 6, now=now)[2], True)
        check("SAME row with assume_local=True -> genuinely fresh",
              assert_fresh(loc, 6, assume_local=True, now=now)[0], True)
        loc2 = d / "local2.tsv"
        loc2.write_text("2026-08-11T07:30\n")  # 07:30 CEST == 05:30Z -> 6.5h stale
        check("local stamp, assume_local=False -> WRONGLY fresh",
              assert_fresh(loc2, 6, now=now)[0], True)
        check("SAME row, assume_local=True  -> correctly STALE",
              assert_fresh(loc2, 6, assume_local=True, now=now)[0], False)

        # ===== THE MARKER OVERRIDES THE CALLER (elo_history UTC migration) =====
        # THE LOAD-BEARING PAIR: the SAME clock `07:30`, the SAME
        # `assume_local=True` caller, and OPPOSITE verdicts decided by one
        # character. now=12:00Z, limit 6h:
        #     07:30Z  -> marker wins, 4.5h -> FRESH
        #     07:30   -> naive, CEST->05:30Z, 6.5h -> STALE
        # If these two agreed, the marker would be inert and the migration
        # would be silently mis-reading one era.
        zrow = d / "z.tsv"
        zrow.write_text("2026-08-11T07:30Z\n")
        check("Z row + assume_local=True -> marker WINS, 4.5h FRESH",
              assert_fresh(zrow, 6, assume_local=True, now=now)[0], True)
        naive = d / "naive.tsv"
        naive.write_text("2026-08-11T07:30\n")
        check("SAME clock, NO marker, same caller -> 6.5h STALE (marker was load-bearing)",
              assert_fresh(naive, 6, assume_local=True, now=now)[0], False)
        # A Z row must also be immune to the flag: both callers agree.
        check("Z row + assume_local=False -> same verdict, FRESH",
              assert_fresh(zrow, 6, now=now)[0], True)
        # A mid-migration file holding BOTH eras reads the NEWEST by ITS OWN
        # marker -- 07:30Z (4.5h) beats the naive 05:00, so: fresh.
        mixed = d / "mixed.tsv"
        mixed.write_text("2026-08-11T05:00\n2026-08-11T07:30Z\n")
        check("mixed naive+Z file -> newest parsed by its own marker, FRESH",
              assert_fresh(mixed, 6, assume_local=True, now=now)[0], True)

        # The daemon-looks-healthy divergence must be NAMED, not just refused.
        live = d / "live.tsv"
        live.write_text("2026-08-09T05:12:43Z\n")
        os.utime(live, (now.timestamp(), now.timestamp()))
        msg = assert_fresh(live, 6, now=now)[2]
        check("fresh mtime + stale data -> divergence named",
              "live writer over a stale table" in msg, True)

    print("\nPASS: refuses stale, blind and missing; passes fresh; the local-zone "
          "flag changes the verdict on the SAME row; and a live writer over a "
          "stale table is named."
          if not bad else f"\n*** {bad} case(s) wrong ***")
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        raise SystemExit(selftest())
    if len(sys.argv) > 1:
        ok, age, msg = assert_fresh(Path(sys.argv[1]),
                                    float(sys.argv[2]) if len(sys.argv) > 2 else 6)
        print(msg)
        raise SystemExit(0 if ok else 1)
    print(__doc__)
