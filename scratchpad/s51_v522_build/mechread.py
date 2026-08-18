#!/usr/bin/env python3
"""v522 mechanism-arm reader: zero-vs-nonzero per sub-flag, off the stderr tapes.

⛔ EVERY COLUMN IS A COUNT OF A LINE THE BOT ONLY EMITS WHEN A SPECIFIC CLAUSE
IS EVALUATED OR FIRES, so a sub-flag that is OFF must drive its own column to
exactly 0 and leave the others standing.

⭐ AND UNLIKE v518-v520, `mOff`'s ZEROES ARE REAL RATHER THAN VOID.  Both log
flags are gated on THEMSELVES, not on the master, so with LOKI_FS_V522 = False
the tape still emits a PH522 line per eligible ring round (`on 0 pub 0`) and a
MAG522 line per magazine round (`on 0 ... bind 0`).  The denominator is visible,
so the zero means something.

COLUMNS
  ph_lines   PH522 lines: rounds the RAIDER was at the ring with a live turret
             and 1..NEAR seats open -- the mechanism's eligibility denominator
  ph_pub     ...of which it actually published FS_PH_KILL_NEAR
  ph_body2   ...published by BODY 2 (the FS_SUPP_SLOT channel correction (2)
             exists for; a nonzero here with CREW_READ off is dose thrown away)
  mag_lines  MAG522 lines: Core magazine rounds inside the crew/salt branch
  mag_near   ...of which the Core READ a NEAR code (SLOT_FS or, under
             CREW_READ, any fresh crew slot)
  mag_fund   ...of which the Core's OWN ammo read passed FS_V522_FUND_AMMO
  mag_bind   ...of which the floor was actually RAISED.  ⛔ THE MECHANISM.
  PARSE_BAD  lines that looked like ours and did not parse -- REPORTED, never
             swallowed

GUARDS (--selftest), each driven to the other verdict:
  S1 a synthetic tape through every counter        -> exact expected row
  S2 FULL MUTATION CONTROL: retag every line       -> every column 0
  S3 SINGLE-COLUMN MUTATION: retag only PH522      -> ph_* 0, mag_* intact
  S4 MALFORMED LINE                                -> PARSE_BAD, not swallowed
  S5 FIELD MUTATION: flip every `bind 1` to `bind 0` -> mag_bind 0 alone
"""
import sys
from collections import Counter
from pathlib import Path

COLS = ["ph_lines", "ph_pub", "ph_body2", "mag_lines", "mag_near",
        "mag_fund", "mag_bind", "PARSE_BAD"]


def _kv(fields):
    """`TAG rnd k v k v ...` -> {k: v}.  Raises on a malformed tail."""
    body = fields[2:]
    if len(body) % 2:
        raise ValueError("odd key/value tail")
    return dict(zip(body[0::2], body[1::2]))


def count(text):
    c = Counter()
    bad = 0
    for line in text.splitlines():
        f = line.split()
        if not f or f[0] not in ("PH522", "MAG522"):
            continue
        try:
            int(f[1])                      # the round, always field 1
            d = _kv(f)
            if f[0] == "PH522":
                c["ph_lines"] += 1
                c["ph_pub"] += (d["pub"] == "1")
                c["ph_body2"] += (d["pub"] == "1" and d["body"] == "2")
            else:
                c["mag_lines"] += 1
                c["mag_near"] += (d["near"] == "1")
                c["mag_fund"] += (d["fund"] == "1")
                c["mag_bind"] += (d["bind"] == "1")
        except (IndexError, ValueError, KeyError):
            bad += 1
    c["PARSE_BAD"] = bad
    return c


SYNTH = "\n".join([
    "PH522 36 orth 2 bar 6 price 18 allow 12 on 1 pub 1 body 1",
    "PH522 40 orth 1 bar 6 price 12 allow 12 on 1 pub 0 body 1",
    "PH522 41 orth 2 bar 6 price 18 allow 12 on 1 pub 1 body 2",
    "MAG522 37 ph 6 on 1 near 1 fund 1 fuse 1 ttl 1 ti 22 ammo 25 bar 6 "
    "want 18 floor 18 bind 1 nbind 1 nnear 1",
    "MAG522 38 ph 4 on 1 near 0 fund 0 fuse 1 ttl 1 ti 12 ammo 2 bar 6 "
    "want 18 floor 12 bind 0 nbind 1 nnear 1",
    "FS PHASE 36 id 3 ph 6 d 8 at (29, 7)",     # a foreign line: ignored
])
EXPECT = {"ph_lines": 3, "ph_pub": 2, "ph_body2": 1, "mag_lines": 2,
          "mag_near": 1, "mag_fund": 1, "mag_bind": 1, "PARSE_BAD": 0}


def selftest():
    fails = []

    def chk(name, cond, detail=""):
        print(("  ok   " if cond else "  FAIL ") + name +
              ("" if cond else "  " + detail))
        if not cond:
            fails.append(name)

    got = count(SYNTH)
    chk("S1 synthetic tape", all(got[k] == v for k, v in EXPECT.items()),
        str({k: got[k] for k in COLS}))

    mut = "\n".join("X" + l for l in SYNTH.splitlines())
    g2 = count(mut)
    chk("S2 full mutation -> all zero", all(g2[k] == 0 for k in COLS),
        str({k: g2[k] for k in COLS}))

    mut3 = SYNTH.replace("PH522", "ZZ522")
    g3 = count(mut3)
    chk("S3 single-column mutation (PH522 only)",
        g3["ph_lines"] == 0 and g3["mag_lines"] == 2 and g3["mag_bind"] == 1,
        str({k: g3[k] for k in COLS}))

    g4 = count(SYNTH + "\nMAG522 99 ph\n")
    chk("S4 malformed line -> PARSE_BAD", g4["PARSE_BAD"] == 1,
        str({k: g4[k] for k in COLS}))

    g5 = count(SYNTH.replace("bind 1", "bind 0"))
    chk("S5 field mutation (bind) -> mag_bind 0 alone",
        g5["mag_bind"] == 0 and g5["mag_near"] == 1 and g5["ph_pub"] == 2,
        str({k: g5[k] for k in COLS}))

    print("SELFTEST:", "PASS" if not fails else "FAIL " + ",".join(fails))
    return 0 if not fails else 1


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        sys.exit(selftest())
    print("%-10s %9s %7s %8s %10s %9s %9s %9s %10s" %
          (("arm",) + tuple(COLS)))
    for d in sys.argv[1:]:
        p = Path(d)
        text = "".join(open(f, errors="replace").read()
                       for f in sorted(p.glob("log/*.err")))
        c = count(text)
        print("%-10s %9d %7d %8d %10d %9d %9d %9d %10d" %
              ((p.name,) + tuple(c[k] for k in COLS)))


if __name__ == "__main__":
    main()
