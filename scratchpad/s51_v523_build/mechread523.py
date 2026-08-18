#!/usr/bin/env python3
"""v523 MECHANISM-ARM READER -- zero-vs-nonzero per sub-flag, off the stderr
tapes, with EVERY COLUMN'S DENOMINATOR BESIDE IT.

Columns, and each is paired with the denominator that makes its zero readable:
  ph_lines    PH523 records (one per at-ring round).  THE DENOMINATOR.
  ph_own      ...where THIS body's own eyes saw orth_open == 0
  ph_merged   ...where the MERGED (crew-union) verdict said sealed
  ph_sealpub  ...where FS_PH_SEALED was actually PUBLISHED
  ph_arccl    ...where this body published the ARC-CLOSED code
  ⭐ ph_gain   = ph_merged - ph_own.  THE SEALED-RATE MOVEMENT, per arm.
  salt_union  SALT523 records: closure gates answered by the UNION alone
  arc_credit  ARC523 CREDIT records: a peer's arc attestation was believed
  crew_reads  CREW523 records (Core-side phase reads).  THE DENOMINATOR.
  crew_win    ...where a NON-SLOT_FS slot carried the merged phase
  fund_q      FUND523 records (funding questions).  THE DENOMINATOR.
  fund_flip   ...where sustained and spare-shot DISAGREED
  PARSE_BAD   malformed records.  Must be 0, and a malformed line must be
              REPORTED rather than silently dropped -- a parser that eats what
              it cannot read returns a clean zero for a broken tape.

GUARDS (`--selftest`), each driven to the OTHER verdict:
  G1 a synthetic tape reads its known values
  G2 FULL mutation: every record removed -> every column 0, PARSE_BAD 0
  G3 SINGLE-COLUMN mutation: only CREW523 removed -> crew columns 0, the rest
     UNCHANGED (a shared-state bug would move them all)
  G4 FIELD mutation: `merged 1` -> `merged 0` zeroes ph_merged ALONE
  G5 a malformed record must be REPORTED as PARSE_BAD, not dropped
  G6 an EMPTY tape returns all zeroes with PARSE_BAD 0 (the vacuous case must
     not be indistinguishable from a parse failure)
"""
from __future__ import annotations

import os
import sys

KEYS = ("ph_lines", "ph_own", "ph_merged", "ph_sealpub", "ph_arccl",
        "salt_union", "arc_credit", "crew_reads", "crew_win",
        "fund_q", "fund_flip", "PARSE_BAD")
FS_PH_SEALED = 3


def _kv(tok):
    """['a','1','b','2'] -> {'a':'1','b':'2'}; odd length is malformed."""
    if len(tok) % 2:
        return None
    return dict(zip(tok[0::2], tok[1::2]))


def read_tape(text: str) -> dict:
    c = {k: 0 for k in KEYS}
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        p = line.split()
        tag = p[0]
        if tag == "PH523":
            d = _kv(p[2:])
            if d is None or "merged" not in d or "ph" not in d:
                c["PARSE_BAD"] += 1
                continue
            c["ph_lines"] += 1
            c["ph_own"] += 1 if d.get("own") == "1" else 0
            c["ph_merged"] += 1 if d.get("merged") == "1" else 0
            c["ph_arccl"] += 1 if d.get("arcclosed") == "1" else 0
            try:
                c["ph_sealpub"] += 1 if int(d["ph"]) == FS_PH_SEALED else 0
            except ValueError:
                c["PARSE_BAD"] += 1
        elif tag == "SALT523":
            c["salt_union"] += 1
        elif tag == "ARC523":
            if len(p) > 1 and p[1] == "CREDIT":
                c["arc_credit"] += 1
        elif tag == "CREW523":
            d = _kv(p[2:])
            if d is None or "won" not in d:
                c["PARSE_BAD"] += 1
                continue
            c["crew_reads"] += 1
            c["crew_win"] += 1 if d.get("won") == "1" else 0
        elif tag == "FUND523":
            d = _kv(p[2:])
            if d is None or "spare" not in d or "sust" not in d:
                c["PARSE_BAD"] += 1
                continue
            c["fund_q"] += 1
            if d["spare"] != d["sust"]:
                c["fund_flip"] += 1
    return c


def read_dir(d: str) -> dict:
    tot = {k: 0 for k in KEYS}
    n = 0
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".log") and not fn.endswith(".err"):
            continue
        n += 1
        r = read_tape(open(os.path.join(d, fn), errors="replace").read())
        for k in KEYS:
            tot[k] += r[k]
    tot["_files"] = n
    return tot


SYN = """PH523 10 id 3 body 1 arc 1 orth 2 own 0 merged 1 arcclosed 1 ph 3
PH523 11 id 3 body 1 arc 1 orth 0 own 1 merged 1 arcclosed 0 ph 3
PH523 12 id 3 body 1 arc 1 orth 3 own 0 merged 0 arcclosed 0 ph 2
SALT523 10 id 3 orth 2 own 0 union 1 n 1 ownN 0
ARC523 CREDIT 10 id 3 mine 1 other 2 orth 2 n 1
CREW523 10 site mag slotfs 2 merged 3 won 1 n 1 of 1
CREW523 11 site mag slotfs 3 merged 3 won 0 n 1 of 2
FUND523 10 ammo 4 bank 30 floor 12 need 20 spare 0 sust 1 flip 1 of 1
FUND523 11 ammo 40 bank 30 floor 12 need 20 spare 1 sust 1 flip 1 of 2
"""


def selftest() -> int:
    ok = True

    def chk(name, cond, extra=""):
        nonlocal ok
        print("  %-58s %s %s" % (name, "PASS" if cond else "FAIL", extra))
        if not cond:
            ok = False

    r = read_tape(SYN)
    chk("G1 ph_lines == 3", r["ph_lines"] == 3, r["ph_lines"])
    chk("G1 ph_own == 1", r["ph_own"] == 1, r["ph_own"])
    chk("G1 ph_merged == 2", r["ph_merged"] == 2, r["ph_merged"])
    chk("G1 ph_sealpub == 2", r["ph_sealpub"] == 2, r["ph_sealpub"])
    chk("G1 ph_arccl == 1", r["ph_arccl"] == 1, r["ph_arccl"])
    chk("G1 salt_union == 1", r["salt_union"] == 1)
    chk("G1 arc_credit == 1", r["arc_credit"] == 1)
    chk("G1 crew_reads == 2 / crew_win == 1",
        r["crew_reads"] == 2 and r["crew_win"] == 1)
    chk("G1 fund_q == 2 / fund_flip == 1",
        r["fund_q"] == 2 and r["fund_flip"] == 1)
    chk("G1 PARSE_BAD == 0", r["PARSE_BAD"] == 0)

    # G2 FULL mutation
    r2 = read_tape("\n".join(l for l in SYN.splitlines()
                             if not l.startswith(("PH523", "SALT523",
                                                  "ARC523", "CREW523",
                                                  "FUND523"))))
    chk("G2 full mutation -> every column 0",
        all(r2[k] == 0 for k in KEYS))

    # G3 SINGLE-COLUMN mutation
    r3 = read_tape("\n".join(l for l in SYN.splitlines()
                             if not l.startswith("CREW523")))
    chk("G3 CREW523 removed -> crew columns 0",
        r3["crew_reads"] == 0 and r3["crew_win"] == 0)
    chk("G3 ...and every OTHER column unchanged",
        all(r3[k] == r[k] for k in KEYS
            if k not in ("crew_reads", "crew_win")))

    # G4 FIELD mutation
    r4 = read_tape(SYN.replace("merged 1", "merged 0"))
    chk("G4 `merged 1`->`merged 0` zeroes ph_merged ALONE",
        r4["ph_merged"] == 0 and r4["ph_own"] == r["ph_own"]
        and r4["ph_sealpub"] == r["ph_sealpub"], r4["ph_merged"])

    # G5 malformed must be REPORTED
    r5 = read_tape(SYN + "PH523 13 id 3 body 1 arc\n")
    chk("G5 malformed record REPORTED as PARSE_BAD",
        r5["PARSE_BAD"] == 1, r5["PARSE_BAD"])
    chk("G5 ...and does not inflate ph_lines",
        r5["ph_lines"] == r["ph_lines"])

    # G6 empty tape
    r6 = read_tape("")
    chk("G6 empty tape -> all zero, PARSE_BAD 0",
        all(r6[k] == 0 for k in KEYS))

    print("SELFTEST:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    print("%-8s %8s %7s %8s %9s %7s %9s %9s %10s %8s %7s %9s %9s" %
          ("arm", "ph_lines", "ph_own", "ph_merg", "ph_seal", "ph_arc",
           "salt_un", "arc_cred", "crew_read", "crew_win", "fund_q",
           "fund_flip", "PARSE_BAD"))
    for d in sys.argv[1:]:
        r = read_dir(d)
        print("%-8s %8d %7d %8d %9d %7d %9d %9d %10d %8d %7d %9d %9d" %
              (os.path.basename(os.path.dirname(d.rstrip("/"))) or d,
               r["ph_lines"], r["ph_own"], r["ph_merged"], r["ph_sealpub"],
               r["ph_arccl"], r["salt_union"], r["arc_credit"],
               r["crew_reads"], r["crew_win"], r["fund_q"], r["fund_flip"],
               r["PARSE_BAD"]))


if __name__ == "__main__":
    main()
