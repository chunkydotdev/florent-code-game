#!/usr/bin/env python3
"""Does the twin reserve ACTUALLY accumulate a bank?  (v518 change 3's own
falsifier, and v517's measured blocker: "bank pinned at 16".)

Reads the TIWATCH518 tape (one line per round from the Core) and cuts the
titanium column by the HOLD state the same line carries.  ⛔ The comparison
that matters is mF (reserve on) vs mR (reserve off) on the SAME cut, because
"the bank is low" is true of both arms all game.

⛔ GUARD, DRIVEN BOTH WAYS: a synthetic tape with a known ti series under a
known hold flag must return exactly those two medians, and swapping the hold
column must swap them.
"""
import re
import statistics as st
import sys
from pathlib import Path

L = re.compile(r"^TIWATCH518 (\d+) ti (\d+) ammo (\d+) scale (\d+) units (\d+)"
               r" sen (\d+) bar (\d+) beat (\d) hold (\d)")


def cut(logdir):
    hold, nohold, beat, scale_at_beat = [], [], [], []
    for f in sorted(Path(logdir).glob("*.err")):
        for line in open(f, errors="replace"):
            m = L.match(line)
            if not m:
                continue
            ti = int(m.group(2))
            if m.group(9) == "1":
                hold.append(ti)
            else:
                nohold.append(ti)
            if m.group(8) == "1":
                beat.append(ti)
                scale_at_beat.append(int(m.group(4)))
    return hold, nohold, beat, scale_at_beat


def guard():
    import tempfile
    d = Path(tempfile.mkdtemp())
    rows = []
    for i, (ti, h) in enumerate([(10, 1), (20, 1), (30, 1), (100, 0), (200, 0)]):
        rows.append("TIWATCH518 %d ti %d ammo 0 scale 200 units 5 sen 60 "
                    "bar 6 beat 1 hold %d" % (i, ti, h))
    (d / "a.err").write_text("\n".join(rows) + "\n")
    h, n, b, _s = cut(d)
    ok = (st.median(h) == 20 and st.median(n) == 150 and len(b) == 5)
    # swap the hold column: the two medians must swap
    (d / "a.err").write_text("\n".join(
        r.replace("hold 1", "hold X").replace("hold 0", "hold 1")
         .replace("hold X", "hold 0") for r in rows) + "\n")
    h2, n2, _b2, _s2 = cut(d)
    ok = ok and st.median(h2) == 150 and st.median(n2) == 20
    print("GUARD:", "PASS" if ok else "FAIL",
          "(hold/no-hold medians %s/%s, swapped %s/%s)"
          % (st.median(h), st.median(n), st.median(h2), st.median(n2)))
    return ok


if __name__ == "__main__":
    if not guard():
        sys.exit(1)
    print("%-10s %8s %8s %8s %8s %8s" % ("arm", "holdN", "holdMED", "holdMAX",
                                         "beatMED", "scaleMED"))
    for a in sys.argv[1:]:
        h, n, b, s = cut(Path(a) / "log")
        print("%-10s %8d %8s %8s %8s %8s"
              % (Path(a).name, len(h),
                 st.median(h) if h else "-", max(h) if h else "-",
                 st.median(b) if b else "-", st.median(s) if s else "-"))
