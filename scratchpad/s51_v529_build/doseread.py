#!/usr/bin/env python3
"""v529 DOSE READER: fold the dose battery's stderr tapes per ARM.

Emits, per arm:
  * the v527 funnel  -- BUNKER FIRE / RESEAL / HOLD-by-reason, PSURV ARM /
    DISPATCH, SELFCUT, SWITCH, DEFHIT
  * the v527 M2 SIGNATURE -- [sealed & no-turret] rounds/game and the longest
    run (via `sealnt_read.fold_text`, which is self-tested against three
    synthetic tapes including one that catches a reader blind to the turret
    column)
  * the v528 M5 metric -- pick-time connection regret (via connread's regex)
  * a TRACEBACK count and a TAPE-EMPTY guard per arm

⛔ GUARDS, because every column here can lie in the flattering direction:
  1. an arm whose SEALNT tape is EMPTY is reported BLIND, not zero;
  2. every counter is printed for the two ABLATION arms as well, so a column
     that never reaches the other verdict is visible as a constant;
  3. the run-to-run instability of NOISE_ON=True is stated, not hidden --
     these are magnitudes.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "s51_v527_build"))
from sealnt_read import fold_text                       # noqa: E402

PICK = re.compile(r"^V528 PICK r (\d+) id (\d+) tgt (\S+) cs (-?\d+) "
                  r"bs (-?\d+) reg (-?\d+)")
BUNK = re.compile(r"V527 BUNKER (FIRE|RESEAL|HOLD)(?:.*blk (\w+))?")

COUNTERS = ("PSURV ARM", "PSURV DISPATCH", "SELFCUT", "SWITCH", "DEFHIT",
            "LASTSEAT", "TFIRST")


def main(d):
    d = Path(d)
    arms = defaultdict(list)
    for f in sorted(d.glob("*.err")):
        # tags are <arm>_<map>_s<seed>_<seat>.err  and every arm is dose_*
        arm = "_".join(f.stem.split("_")[:2])
        arms[arm].append(f)

    print("=== v527 FUNNEL + M2 SIGNATURE + v528 M5, per arm ===")
    print("⚠ NOISE_ON=True re-rolls the spawn salt per process: these are "
          "MAGNITUDES, not constants (v527 read BUNKER FIRE 5/3/2 on three "
          "runs of identical cells).\n")
    hdr = ("%-13s %5s %4s | %5s %6s %6s | %5s %5s %6s %6s | %8s %7s %6s | "
           "%7s %8s %6s")
    print(hdr % ("arm", "games", "tb", "FIRE", "RESEAL", "HOLD",
                 "PSARM", "PSDIS", "SLFCUT", "SWITCH",
                 "sealnt/g", "runmax", "run>=50", "picks", "mean_reg",
                 "reg>0"))
    blind = []
    for arm in sorted(arms):
        files = arms[arm]
        tb = 0
        fire = reseal = hold = 0
        cnt = defaultdict(int)
        seal_tot = seal_best = 0
        seal_over = 0
        seal_lines = 0
        regs = []
        for f in files:
            txt = f.read_text(errors="replace")
            tb += txt.count("Traceback")
            for m in BUNK.finditer(txt):
                if m.group(1) == "FIRE":
                    fire += 1
                elif m.group(1) == "RESEAL":
                    reseal += 1
                else:
                    hold += 1
            for c in COUNTERS:
                cnt[c] += txt.count("V527 " + c)
            t, best, _hv, n = fold_text(txt)
            seal_tot += t
            seal_best = max(seal_best, best)
            seal_over += (best >= 50)
            seal_lines += n
            for ln in txt.splitlines():
                m = PICK.match(ln)
                if m:
                    regs.append(int(m.group(6)))
        g = len(files)
        if seal_lines == 0:
            blind.append(arm)
        print(hdr % (arm, g, tb, fire, reseal, hold,
                     cnt["PSURV ARM"], cnt["PSURV DISPATCH"], cnt["SELFCUT"],
                     cnt["SWITCH"],
                     "BLIND" if seal_lines == 0 else "%.1f" % (seal_tot / g),
                     seal_best, seal_over,
                     len(regs),
                     "%.3f" % (sum(regs) / len(regs)) if regs else "-",
                     sum(1 for r in regs if r > 0) if regs else "-"))
    if blind:
        print("\n⛔ ARMS WITH AN EMPTY SEALNT TAPE (BLIND, not zero): %s"
              % blind)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
