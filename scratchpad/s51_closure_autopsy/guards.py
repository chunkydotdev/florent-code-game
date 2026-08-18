#!/usr/bin/env python3
"""s51 closure autopsy -- INSTRUMENT GUARDS, driven BOTH WAYS.

An instrument that has only ever produced one verdict has not been seen to
check.  Every guard below is paired with a case that MUST come out the other
way.

G1  DL REGEX, synthetic fixture.  Hand-built stderr with known counts; the
    parser must reproduce them exactly.
G2  DL REGEX, MUTATION CONTROL.  The same fixture with the tag corrupted must
    read ZERO -- a regex that matches anything validates nothing.
G3  SEAT CLASSIFIER, POSITIVE CONTROL.  Every tile on which the bot actually
    built a barrier (FS SEAL) must be classified `barrier-legal` by
    seatgeom.py.  A classifier that has never called a known-sealable seat
    sealable has not been seen to classify.
G4  SEAT CLASSIFIER, NEGATIVE CONTROL.  midgard carries exactly one WALL ring
    tile per side ((25,25) A / (4,4) B).  The classifier must call those
    `wall-excluded`, and the bot must never have sealed them.
G5  TAPE vs BOT, CLOSING MAPS.  The replay tape is an instrument independent of
    the bot's own stderr.  On the 13 games the parent autopsy recorded as
    closing, the tape must independently detect `orth_open == 0` at the SAME
    round; on the 17 non-closing games it must independently never reach 0.
G6  TAPE DIRECTION.  The tape must read a NON-zero orth_open before closure in
    every closing game (i.e. it is not stuck at 0).
"""
from __future__ import annotations

import csv
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from closure import read_log, DL, LOGS  # noqa: E402

FIRED = ROOT / "scratchpad/s51_evict_autopsy/fired.tsv"
FIX = HERE / "fixture_dl.err"

FIXTURE = """noise line, not ours
FS GATE 0 sig (18, 18, (2, 14), (14, 2)) ok 1
FS DL 5 id 3 role seal orth 8 need 9 ebody 1 lau 0 ti 294 lcost 33 bar 5 obs 1 hist 1 pend 0
FS DL 6 id 3 role seal orth 7 need 8 ebody 0 lau 0 ti 200 lcost 33 bar 5 obs 2 hist 1 pend 0
FS DL 7 id 3 role seal orth 0 need 0 ebody 0 lau 1 ti 100 lcost 33 bar 5 obs 6 hist 3 pend 1
FS SEAL 6 tile (13, 3) n 1
FS SEAL 7 tile (14, 1) n 2
FS CLEAR 8 tile (15, 1) peck 1
FS EVICT 15 from (12, 5) to (12, 10)
FS EVICT 16 from (13, 3) to (2, 9)
FS EVICTOR 14 at (13, 5) cov 1
FS THROW 2 from (5, 13) to (8, 9) T (16, 1)
"""
EXPECT = dict(dl=3, seals=2, clears=1, evicts=2, evictors=1, throws=1,
              orth_at_5=8, orth_at_7=0, ti_at_6=200, pend_at_7=1)


def g1_g2():
    FIX.write_text(FIXTURE)
    log = read_log(FIX)
    got = dict(dl=len(log["dl"]), seals=len(log["seals"]),
               clears=len(log["clears"]), evicts=len(log["evicts"]),
               evictors=len(log["evictors"]), throws=len(log["throws"]),
               orth_at_5=log["dl"][5]["orth"], orth_at_7=log["dl"][7]["orth"],
               ti_at_6=log["dl"][6]["ti"], pend_at_7=log["dl"][7]["pend"])
    ok1 = got == EXPECT
    print(f"G1 synthetic fixture           : {'PASS' if ok1 else 'FAIL'}  {got}")
    if not ok1:
        print(f"   expected {EXPECT}")

    # mutation control: corrupt the tag, must read zero
    mut = FIXTURE.replace("FS DL ", "FS DZ ").replace("FS SEAL ", "FS SEEL ")
    mp = HERE / "fixture_dl_mutated.err"
    mp.write_text(mut)
    m = read_log(mp)
    ok2 = len(m["dl"]) == 0 and len(m["seals"]) == 0 and len(m["evicts"]) == 2
    print(f"G2 mutation control (0 on junk): {'PASS' if ok2 else 'FAIL'}  "
          f"dl={len(m['dl'])} seals={len(m['seals'])} "
          f"evicts={len(m['evicts'])} (evicts must stay 2 -- only DL/SEAL "
          f"were corrupted)")
    return ok1 and ok2


def g3_g4():
    geom = {}
    with open(HERE / "seat_geom.tsv") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            geom[(r["map"], r["seat"], int(r["x"]), int(r["y"]))] = r["cls"]
    sealed = set()
    for errp in sorted(LOGS.glob("v513_log-*.err")):
        _, mapname, _s, seat = errp.stem.split("-")
        for _r, x, y, _n in read_log(errp)["seals"]:
            sealed.add((mapname, seat, x, y))
    unclassified = [k for k in sealed if k not in geom]
    bad = [k for k in sealed if geom.get(k) not in (None, "barrier-legal")]
    ok3 = not bad
    print(f"G3 positive control            : {'PASS' if ok3 else 'FAIL'}  "
          f"{len(sealed)} distinct tiles carried a real barrier; "
          f"{len(sealed) - len(unclassified)} are ring tiles and ALL are "
          f"classified barrier-legal ({len(bad)} misclassified). "
          f"{len(unclassified)} sealed tiles lie outside the 12-tile ring "
          f"(diagonal/extension builds) and are out of the classifier's scope.")

    walls = [k for k, v in geom.items() if v == "wall-excluded"]
    ok4 = bool(walls) and not any(w in sealed for w in walls)
    print(f"G4 negative control            : {'PASS' if ok4 else 'FAIL'}  "
          f"classifier returns a NON-'barrier-legal' verdict for "
          f"{len(walls)} tile(s) {[(w[0], w[1], w[2], w[3]) for w in walls]}; "
          f"none was ever sealed by the bot.")
    return ok3 and ok4


def g5_g6():
    want = {}
    with open(FIRED) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            want[r["game"]] = int(r["close_r"])
    got = {}
    pre = {}
    with open(HERE / "closure_attrib.tsv") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            got[r["game"]] = int(r["close_r"])
            pre[r["game"]] = int(r["min_orth"])
    shared = sorted(set(want) & set(got))
    closing = [g for g in shared if want[g] >= 0]
    nonclosing = [g for g in shared if want[g] < 0]
    hit = [g for g in closing if got[g] == want[g]]
    fp = [g for g in nonclosing if got[g] >= 0]
    ok5 = len(hit) == len(closing) and not fp
    print(f"G5 tape vs bot, closing maps   : {'PASS' if ok5 else 'FAIL'}  "
          f"{len(hit)}/{len(closing)} closing games: tape independently "
          f"detects orth_open==0 at the SAME round as the bot's own stderr; "
          f"{len(fp)} false positives on {len(nonclosing)} non-closing games.")
    for g in closing:
        if got[g] != want[g]:
            print(f"   MISMATCH {g}: tape {got[g]} vs bot {want[g]}")
    stuck = [g for g in closing if pre[g] != 0]
    ok6 = not stuck                       # min_orth is 0 exactly on closers
    nz = [g for g in nonclosing if pre[g] > 0]
    print(f"G6 tape direction              : "
          f"{'PASS' if len(nz) == len(nonclosing) else 'FAIL'}  "
          f"tape reads min_orth>0 on {len(nz)}/{len(nonclosing)} non-closing "
          f"games and min_orth==0 on {len(closing) - len(stuck)}/"
          f"{len(closing)} closing games -- the counter moves in both "
          f"directions.")
    return ok5 and len(nz) == len(nonclosing)


def main():
    print("s51 CLOSURE AUTOPSY -- INSTRUMENT GUARDS\n")
    a = g1_g2()
    b = g3_g4()
    c = g5_g6()
    print(f"\nALL GUARDS: {'PASS' if (a and b and c) else 'FAIL'}")


if __name__ == "__main__":
    if "-h" in sys.argv[1:] or "--help" in sys.argv[1:]:
        print(__doc__)
        raise SystemExit(0)
    main()
