#!/usr/bin/env python3
"""v521 mechanism-arm reader: zero-vs-nonzero per sub-flag, off the stderr tapes.

⛔ EVERY COLUMN IS A COUNT OF A LINE THE BOT ONLY EMITS WHEN A SPECIFIC CLAUSE
FIRES, so a sub-flag that is OFF must drive its own column to exactly 0 and
leave the others standing.  `mOff`'s columns are empty BY CONSTRUCTION (the log
flags themselves live under the master) and are VOID, not zero.

GUARDS (--selftest), each driven to the other verdict:
  S1 a synthetic tape through every counter -> exact expected row
  S2 FULL MUTATION CONTROL: retag every counted line -> every column 0
  S3 SINGLE-COLUMN MUTATION: retag only SYNC521 -> that column 0, others intact
  S4 MALFORMED LINE: must be REPORTED as PARSE_BAD, never swallowed
"""
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent


def count(text):
    c = Counter()
    bad = 0
    for line in text.splitlines():
        if not line[:8].startswith(("SYNC521", "RUNG521", "MAG521", "GATEF")):
            continue
        f = line.split()
        try:
            if f[0] == "SYNC521":
                st = int(f[3])
                c["sync_rounds"] += 1
                c["st_near"] += (st == 1)
                c["st_hold"] += (st == 2)
                c["st_buyin"] += (st == 3)
            elif f[0] == "RUNG521":
                r = int(f[3])
                c["rung_fires"] += 1
                c["rung%d" % r] += 1
            elif f[0] == "MAG521":
                c["mag_reserve"] += 1
            elif f[0] == "GATEFIX521":
                c["gatefix"] += 1
        except (IndexError, ValueError):
            bad += 1
    c["PARSE_BAD"] = bad
    return c


COLS = ["sync_rounds", "st_near", "st_hold", "st_buyin", "rung_fires",
        "rung0", "rung1", "rung2", "rung3", "rung4", "mag_reserve",
        "gatefix", "PARSE_BAD"]


def selftest():
    fails = []

    def chk(n, cond, d=""):
        print(("  ok   " if cond else "  FAIL ") + n + (("  " + d) if not cond else ""))
        if not cond:
            fails.append(n)

    tape = "\n".join([
        "SYNC521 10 st 1 orth 2 live 1 ammo 40 body 1 rung -1",
        "SYNC521 11 st 2 orth 0 live 1 ammo 40 body 1 rung -1",
        "SYNC521 12 st 3 orth 1 live 0 ammo 0 body 2 rung -1",
        "SYNC521 13 st 0 orth 5 live 0 ammo 0 body 1 rung -1",
        "RUNG521 10 rung 1 st 1 body 1",
        "RUNG521 12 rung 0 st 3 body 2",
        "RUNG521 13 rung 4 st 0 body 1",
        "MAG521 14 ph 5 ti 40 floor 54 bar 6 ammo 20",
        "GATEFIX521 4 seat 3 id 9",
        "SOMETHING ELSE ENTIRELY",
    ])
    c = count(tape)
    chk("S1 sync_rounds 4", c["sync_rounds"] == 4, str(c["sync_rounds"]))
    chk("S1 st_near 1", c["st_near"] == 1)
    chk("S1 st_hold 1", c["st_hold"] == 1)
    chk("S1 st_buyin 1", c["st_buyin"] == 1)
    chk("S1 rung_fires 3", c["rung_fires"] == 3)
    chk("S1 rung0 1", c["rung0"] == 1)
    chk("S1 mag_reserve 1", c["mag_reserve"] == 1)
    chk("S1 gatefix 1", c["gatefix"] == 1)
    chk("S1 PARSE_BAD 0", c["PARSE_BAD"] == 0)

    mut = re.sub(r"^(SYNC521|RUNG521|MAG521|GATEFIX521)", "XX", tape, flags=re.M)
    cm = count(mut)
    chk("S2 full mutation -> all zero",
        all(cm[k] == 0 for k in COLS), str(dict(cm)))

    mut3 = re.sub(r"^SYNC521", "XX", tape, flags=re.M)
    c3 = count(mut3)
    chk("S3 single-column mutation zeroes SYNC only",
        c3["sync_rounds"] == 0 and c3["rung_fires"] == 3
        and c3["mag_reserve"] == 1, str(dict(c3)))

    c4 = count(tape + "\nSYNC521 broken line\n")
    chk("S4 malformed line REPORTED, not swallowed", c4["PARSE_BAD"] == 1,
        str(c4["PARSE_BAD"]))

    print("\nSELFTEST", "PASS" if not fails else "FAIL %s" % fails)
    return 0 if not fails else 1


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        sys.exit(selftest())
    arms = sys.argv[1:]
    print("%-9s %7s %6s %6s %6s | %6s %5s %5s %5s %5s %5s | %6s %5s %5s" % (
        "arm", "syncR", "NEAR", "HOLD", "BUYIN", "rungs", "r0", "r1", "r2",
        "r3", "r4", "magRes", "gfix", "BAD"))
    for a in arms:
        d = Path(a)
        text = "".join(p.read_text(errors="replace")
                       for p in sorted((d / "log").glob("*.err")))
        c = count(text)
        print("%-9s %7d %6d %6d %6d | %6d %5d %5d %5d %5d %5d | %6d %5d %5d" % (
            d.name, c["sync_rounds"], c["st_near"], c["st_hold"], c["st_buyin"],
            c["rung_fires"], c["rung0"], c["rung1"], c["rung2"], c["rung3"],
            c["rung4"], c["mag_reserve"], c["gatefix"], c["PARSE_BAD"]))


if __name__ == "__main__":
    main()
