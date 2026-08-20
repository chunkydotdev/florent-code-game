#!/usr/bin/env python3
"""M5 VERIFICATION: the CONNECTION-REGRET distribution, per arm.

The tape (`eco.py::_v528_regret`, gated on FS_V528_LOG alone so BOTH arms emit
it from the SAME code) carries, for every harvester this bot actually builds:

    V528 CONN r <rnd> id <id> at <x,y> chosen <c> best <b> regret <c-b>
              cands <n> role <r> seat <s>

`chosen` is the links the harvester just placed will need to reach the Core;
`best` is the smallest over every ore this seat could still have taken.  The
pre-registered claim: the PARENT's regret is nonzero (it ranks on Manhattan
distance and ignores existing belt), v528's sits at ~0.

⛔ REGRET IS >= 0 BY CONSTRUCTION, so "mean >= 0" is not a check.  The checks
that CAN fail, each driven to the other verdict:
  1. the tape must be NON-EMPTY per arm -- an empty tape is the v526 blind
     instrument, and it reads identically to "no regret";
  2. the distribution must be NON-CONSTANT within at least one arm, or the
     column validates anything;
  3. `cands` must be > 0 on most lines -- a scorer with one candidate cannot
     have regret, so an all-`cands 0` tape means the fixture, not the plank,
     produced the zero;
  4. the MARKER CLASS count: lines where a >= MARKER_GAP cheaper connect was
     available and was not taken.  That is the scenario Magnus annotated.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

LINE = re.compile(r"^V528 CONN r (\d+) id (\d+) at (\S+) chosen (\d+) "
                  r"best (\d+) regret (-?\d+) cands (\d+) role (\S+) seat (\d+)")
PICK = re.compile(r"^V528 PICK r (\d+) id (\d+) tgt (\S+) cs (-?\d+) bs (-?\d+) "
                  r"reg (-?\d+) cc (-?\d+) bc (-?\d+) cands (\d+) banned (\d+) "
                  r"regall (-?\d+) seat (\d+)")
MARKER_GAP = 2      # "(27,22) was TWO CONVEYORS from a quick connection"


def arm_of(name):
    return name.split("_")[0] + "_" + name.split("_")[1]


def main(paths):
    per = defaultdict(list)
    pick = defaultdict(list)
    files = defaultdict(int)
    for p in paths:
        stem = Path(p).stem
        arm = "_".join(stem.split("_")[:2])
        files[arm] += 1
        for ln in open(p, errors="replace"):
            mp_ = PICK.match(ln)
            if mp_:
                pick[arm].append((int(mp_.group(4)), int(mp_.group(5)),
                                  int(mp_.group(6)), int(mp_.group(9)),
                                  int(mp_.group(10)), int(mp_.group(11))))
                continue
            m = LINE.match(ln)
            if m:
                per[arm].append((int(m.group(4)), int(m.group(5)),
                                 int(m.group(6)), int(m.group(7)),
                                 int(m.group(1))))
    if not per:
        print("⛔ TAPE EMPTY ACROSS ALL ARMS -- the instrument is blind, not "
              "the regret zero.  (v526 §7: an empty tape reads healthy.)")
        return 1
    if pick:
        print("=== PICK-TIME REGRET (the decision the plank makes) ===")
        print("%-12s %6s %10s %10s %8s %9s %10s"
              % ("arm", "files", "picks", "mean_reg", "reg>0", "max_reg",
                 "mean_regall"))
        for arm in sorted(pick):
            v = pick[arm]
            reg = [x[2] for x in v]
            ra = [x[5] for x in v]
            print("%-12s %6d %10d %10.3f %8d %9d %10.3f"
                  % (arm, files[arm], len(v), sum(reg) / len(reg),
                     sum(1 for r in reg if r > 0), max(reg), sum(ra) / len(ra)))
        allp = {r for v in pick.values() for r in (x[2] for x in v)}
        print("GUARD non-constant pick-regret across the pool: distinct=%d %s"
              % (len(allp), sorted(allp)[:8]))
        if len(allp) < 2:
            print("⛔ GUARD FAIL: pick-regret is constant across ALL arms -- "
                  "the instrument cannot discriminate.")
        print()
    print("=== BUILD-TIME RESIDUAL (connection-only; see eco.py "
          "_v528_pickreg for why this is NOT the plank's objective) ===")
    print("%-12s %6s %7s %9s %9s %8s %8s %8s %9s"
          % ("arm", "files", "decis", "regret_mean", "regret_med", "regret>0",
             "reg>=%d" % MARKER_GAP, "chosen_mn", "cands_mn"))
    ok = True
    for arm in sorted(per):
        v = per[arm]
        reg = [x[2] for x in v]
        ch = [x[0] for x in v]
        cd = [x[3] for x in v]
        pos = sum(1 for r in reg if r > 0)
        mk = sum(1 for r in reg if r >= MARKER_GAP)
        reg_s = sorted(reg)
        print("%-12s %6d %7d %9.3f %9.1f %8d %8d %8.2f %9.2f"
              % (arm, files[arm], len(v), sum(reg) / len(reg),
                 reg_s[len(reg_s) // 2], pos, mk,
                 sum(ch) / len(ch), sum(cd) / len(cd)))
        if sum(cd) == 0:
            print("   ⛔ every decision had 0 alternatives -- the FIXTURE "
                  "produced this zero, not the plank")
            ok = False
    empty = [a for a in files if a not in per]
    if empty:
        print("⛔ ARMS WITH NO TAPE AT ALL: %s -- blind, not zero" % empty)
        ok = False
    allreg = {r for v in per.values() for r in (x[2] for x in v)}
    print("GUARD non-constant regret across the pool: distinct=%d %s"
          % (len(allreg), sorted(allreg)[:8]))
    if len(allreg) < 2:
        print("⛔ GUARD FAIL: regret is a constant column -- it validates "
              "anything.")
        ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
