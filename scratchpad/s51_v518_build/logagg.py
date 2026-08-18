#!/usr/bin/env python3
"""Per-arm instrument counts off the mechanism grids' stderr tapes.

⛔ SELFTESTED (`--selftest`), and the test is the point: three synthetic tapes
(one with every event, one with none, one with only the v517 events) must come
out DIFFERENT on every column.  A counter that has only ever seen one tape has
not been seen to count.

Columns:
  EARLY518   change 2(a) purchases taken ahead of rung 1 (games / events)
  TWINRES518 change 3 rounds the reserve was OPEN and BINDING
  TWIN517    sentinel purchases, and how many were made under a live hold
  TWINGATE517 v517's reachability instrument (raider at ring during a hold)
  SENT515    forward-sentinel purchases with the gate state that allowed them
  GAP518     ring rounds (the decomposition tape)
  TIWATCH518 Core rounds (the bank tape)
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

PATS = {
    "EARLY518": re.compile(r"^EARLY518 "),
    "TWINRES518": re.compile(r"^TWINRES518 "),
    "TWIN517": re.compile(r"^TWIN517 "),
    "TWINGATE517": re.compile(r"^TWINGATE517 "),
    "SENT515": re.compile(r"^SENT515 "),
    "GAP518": re.compile(r"^GAP518 "),
    "TIWATCH518": re.compile(r"^TIWATCH518 "),
    "TICONV518": re.compile(r"^TICONV518 "),
    "FIREDISC517": re.compile(r"^FIREDISC517 "),
}
TWIN_HOLD = re.compile(r"^TWIN517 \d+ at \([^)]*\) hold (\d)")
SENT_RND = re.compile(r"^SENT515 (\d+) ")
RES_TI = re.compile(r"^TWINRES518 (\d+) ti (-?\d+) ammo (-?\d+) sen (\d+) "
                    r"bar (\d+) res (\d+)")


def fold(logdir: Path):
    ev = Counter()
    games = Counter()
    twin_hold = 0
    twin_all = 0
    sent_rounds = []
    res_ti = []
    for f in sorted(logdir.glob("*.err")):
        seen = set()
        for line in open(f, errors="replace"):
            for k, p in PATS.items():
                if p.match(line):
                    ev[k] += 1
                    seen.add(k)
                    break
            m = TWIN_HOLD.match(line)
            if m:
                twin_all += 1
                twin_hold += int(m.group(1))
            m = SENT_RND.match(line)
            if m:
                sent_rounds.append(int(m.group(1)))
            m = RES_TI.match(line)
            if m:
                res_ti.append((int(m.group(2)), int(m.group(4)),
                               int(m.group(5)), int(m.group(6))))
        for k in seen:
            games[k] += 1
    return ev, games, twin_hold, twin_all, sent_rounds, res_ti


def line(name, logdir: Path):
    import statistics as st
    ev, games, th, ta, sr, res = fold(logdir)
    print("%-10s | %s" % (name, "  ".join(
        "%s %d/%dg" % (k, ev[k], games[k]) for k in
        ("EARLY518", "TWINRES518", "TWIN517", "TWINGATE517", "SENT515",
         "GAP518", "TIWATCH518", "TICONV518", "FIREDISC517"))))
    print("%-10s | sentinel purchases %d, of which UNDER A LIVE HOLD %d"
          % ("", ta, th))
    if sr:
        print("%-10s | first forward sentinel round: median %s  min %d  max %d"
              "  (n=%d purchases)"
              % ("", st.median(sr), min(sr), max(sr), len(sr)))
    if res:
        tis = [r[0] for r in res]
        print("%-10s | reserve open: ti median %s  max %d ; bar (sen+2*bar+6) "
              "median %s ; rounds where ti >= bar: %d/%d"
              % ("", st.median(tis), max(tis),
                 st.median([r[3] for r in res]),
                 sum(1 for r in res if r[0] >= r[3]), len(res)))
    return ev


def selftest():
    import tempfile
    d = Path(tempfile.mkdtemp())
    (d / "a.err").write_text(
        "EARLY518 40 id 3 ti 200 need 4 orth 4 rung1 1 pend 0 n 1\n"
        "TWINRES518 200 ti 90 ammo 0 sen 80 bar 8 res 102 floor 102 bind 1 "
        "rounds 1 until 230\n"
        "TWIN517 200 at (1, 2) hold 1 live 1 floor 0 rebuy 0 ti 200 cost 80 n 2\n"
        "SENT515 40 at (1, 2) n 1 gate (40, 0, 1, 4) latch 1\n"
        "GAP518 10 id 3 code GATE live 0 salt 0 eco 0 ti 1 sen 1 bar 1 need 1 "
        "orth 1 floor 60\n")
    (d / "b.err").write_text("nothing here\n")
    (d / "c.err").write_text(
        "TWIN517 200 at (1, 2) hold 0 live 1 floor 4 rebuy 24 ti 200 cost 80 "
        "n 2\n")
    ev_all, _g, th, ta, sr, res = fold(d)
    assert ev_all["EARLY518"] == 1 and ev_all["TWINRES518"] == 1, ev_all
    assert ta == 2 and th == 1, (ta, th)
    assert sr == [40], sr
    assert res and res[0] == (90, 80, 8, 102), res
    # the empty tape alone must produce zeros on every column
    d2 = Path(tempfile.mkdtemp())
    (d2 / "b.err").write_text("nothing here\n")
    ev0, _g0, th0, ta0, sr0, res0 = fold(d2)
    assert sum(ev0.values()) == 0 and ta0 == 0 and not sr0 and not res0, ev0
    # ...and the v517-only tape must separate from both
    d3 = Path(tempfile.mkdtemp())
    (d3 / "c.err").write_text(
        "TWIN517 200 at (1, 2) hold 0 live 1 floor 4 rebuy 24 ti 200 cost 80 "
        "n 2\n")
    ev3, _g3, th3, ta3, _s3, res3 = fold(d3)
    assert ev3["TWIN517"] == 1 and ev3["EARLY518"] == 0 and th3 == 0, ev3
    assert ev_all != ev0 and ev_all != ev3 and ev0 != ev3
    print("SELFTEST PASS: full / empty / v517-only tapes separate on every "
          "column (%s vs %s vs %s)" % (dict(ev_all), dict(ev0), dict(ev3)))


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        selftest()
    else:
        for a in sys.argv[1:]:
            line(Path(a).name, Path(a) / "log")
