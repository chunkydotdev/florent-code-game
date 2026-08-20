#!/usr/bin/env python3
"""v529 SUPPLEMENT: rescue the v527-side negative control (A3n).

A3n asked `eq_u527` (union, V527 live, V528 off) to DIFFER from the parent and
it did not, on 10 cells.  That is NOT news and it is not a merge defect: v527's
OWN build report §5(a) measured the identical thing -- its as-fired arm differed
from the parent on **1 of 14** deterministic cells (antler seat A only), because
with `NOISE_ON = False` the economy gate refuses every bunker ask (5,814 armed,
3,732 asks, 0 fires on 30 cells).  My cell set simply did not contain antler.

So the supplement runs the ONE cell family that is known to separate, at v527's
own seed as well as this build's, and asks TWO things at once:

  S1  is there ANY cell where `eq_527` differs from the parent?  (if not, A3's
      identity is vacuous and the v527 side is unmeasurable on this fixture)
  S2  on every such cell, does `eq_u527` make the SAME choice as `eq_527`?
      (that is the composition claim, and it only has teeth on a cell where
      the plank actually fires)

⛔ A pass on S2 with S1 empty is NOT a pass.  It is reported as UNMEASURABLE.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FCODE = str(ROOT / ".venv/bin/fcode")
D = ROOT / "scratchpad/s51_v529_build"
OUT = D / "byte_check_supp"
OUT.mkdir(parents=True, exist_ok=True)
OPP = str(D / "eq_opp")

CELLS = [(m, s, sd)
         for m in ("antler", "fjordgate", "archipelago", "frostgate")
         for s in ("A", "B")
         for sd in (527919, 529820)]


def run(arm, mapname, seat, seed):
    tag = f"{mapname}_{seed}_seat{seat}_{arm}"
    replay = OUT / f"{tag}.replay26"
    A, B = (str(D / arm), OPP) if seat == "A" else (OPP, str(D / arm))
    r = subprocess.run(
        [FCODE, "run", A, B, str(ROOT / "maps" / f"{mapname}.map26"),
         "--seed", str(seed), "--tle", "0", "--replay", str(replay), "--json"],
        capture_output=True, text=True)
    return replay.read_bytes(), ("Traceback" in r.stderr)


def main():
    sep = []          # cells where the v527 side separates from the parent
    agree = dis = 0
    tb = 0
    print("%-13s %6s %4s   %-14s %-14s" % ("map", "seed", "seat",
                                           "eq_527 vs parent",
                                           "eq_u527 vs eq_527"))
    for m, s, sd in CELLS:
        p, t0 = run("eq_parent", m, s, sd)
        a, t1 = run("eq_527", m, s, sd)
        b, t2 = run("eq_u527", m, s, sd)
        tb += t0 + t1 + t2
        s1 = "DIFFERS" if a != p else "identical"
        s2 = "IDENTICAL" if a == b else "DIFFERS(FAIL)"
        if a != p:
            sep.append((m, s, sd))
            agree += (a == b)
            dis += (a != b)
        print("%-13s %6d %4s   %-14s %-14s" % (m, sd, s, s1, s2), flush=True)

    print("\nS1  cells where the v527 side separates from the parent: %d/%d %s"
          % (len(sep), len(CELLS), sep))
    if not sep:
        print("S2  UNMEASURABLE on this fixture -- no separating cell, so the "
              "A3 identity carries no information about a FIRING plank.")
        print("RESULT: UNMEASURABLE")
        return 0
    print("S2  on those cells, eq_u527 == eq_527 on %d, differs on %d"
          % (agree, dis))
    print("TRACEBACKS: %d" % tb)
    print("RESULT:", "PASS" if dis == 0 and tb == 0 else "FAIL")
    return 0 if dis == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
