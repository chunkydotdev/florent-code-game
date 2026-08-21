#!/usr/bin/env python3
"""v529 MERGE verification: FLAG-OFF BYTE-IDENTITY + THE TWO COMPOSITION ARMS.

Method is v524-v528's: `NOISE_ON = False` on BOTH sides (ours and the opponent
copy `eq_opp`, verified to differ from `bots/_v488beltbreak2` by that ONE line
and nothing else), `--tle 0`, replay BYTES compared.  `--seed` alone does not
pin a game (v515 finding 1) -- NOISE_ON must also be off.

⭐ WHAT IS NEW HERE, AND IT IS THE WHOLE POINT OF A MERGE BUILD.  A flag-off
arm only shows that the union stands down.  It says NOTHING about whether the
union, WITH ONE SIDE ON, still reproduces that side -- which is exactly the
failure a composition can cause (shared instance state, import-order, a
predicate one sibling widened that the other now reads).  So two more arms:

  A3  union with LOKI_FS_V528=False   must be BYTE-IDENTICAL to `_v527collar`
  A4  union with LOKI_FS_V527=False   must be BYTE-IDENTICAL to `_v528eco`

If A3/A4 hold on every cell, then any v529-vs-siblings gap in the battery is
INTERACTION between the two live planks and cannot be a merge defect.  If they
fail, the battery is unreadable and this build stops.

SIX ARMS, EACH DRIVEN TO THE OTHER VERDICT:
  A1  eq_off   vs parent   -> IDENTICAL   (the known zero)
  A2  eq_v529  vs parent   -> DIFFERS     (negative control: the union plays)
  A3  eq_u527  vs eq_527   -> IDENTICAL   (composition, v527 side)
  A3n eq_u527  vs parent   -> DIFFERS     (negative control for A3: if the
                                           v527 side were dead, A3 would pass
                                           for the wrong reason)
  A4  eq_u528  vs eq_528   -> IDENTICAL   (composition, v528 side)
  A4n eq_u528  vs parent   -> DIFFERS     (negative control for A4)

⛔ A3n/A4n EXIST BECAUSE A3 AND A4 ARE PASS-BY-DEFAULT CHECKS.  "Union with one
master off == that sibling" is also satisfied by a union in which NEITHER side
does anything.  The negative control is what makes the identity mean something.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FCODE = str(ROOT / ".venv/bin/fcode")
D = ROOT / "scratchpad/s51_v529_build"
OUT = D / "byte_check"
OUT.mkdir(parents=True, exist_ok=True)
OPP = str(D / "eq_opp")

MAPS5 = ["atoll", "drakkarfjord", "glacierkeep", "nordkap", "yulerune"]
MAPS_WALL = ["valkyrie", "ragnarok", "midgard"]
SEED = 529820


def run(arm, mapname, seat):
    tag = f"{mapname}_seat{seat}_{arm}"
    replay = OUT / f"{tag}.replay26"
    A, B = (str(D / arm), OPP) if seat == "A" else (OPP, str(D / arm))
    cmd = [FCODE, "run", A, B, str(ROOT / "maps" / f"{mapname}.map26"),
           "--seed", str(SEED), "--tle", "0", "--replay", str(replay),
           "--json"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    (OUT / f"{tag}.err").write_text(r.stderr)
    return replay.read_bytes(), ("Traceback" in r.stderr)


def cells(maps):
    for m in maps:
        for s in ("A", "B"):
            yield m, s


def main():
    fail = []
    tbs = 0
    cache = {}

    def get(arm, m, s):
        if (arm, m, s) not in cache:
            b, tb = run(arm, m, s)
            cache[(arm, m, s)] = b
            if tb:
                print("  ⛔ TRACEBACK %s %s seat%s" % (arm, m, s), flush=True)
                fail.append("TRACEBACK:%s" % arm)
        return cache[(arm, m, s)]

    def arm(tag, a, b, maps, want_identical):
        print("=== %s  %s vs %s -- must be %s ==="
              % (tag, a, b, "IDENTICAL" if want_identical else "DIFFER"),
              flush=True)
        same = 0
        n = 0
        for m, s in cells(maps):
            n += 1
            ok = get(a, m, s) == get(b, m, s)
            same += ok
            print("  %-14s seat%s  %s" % (m, s, "IDENTICAL" if ok else "DIFFERS"),
                  flush=True)
        if want_identical:
            verdict = same == n
            print("  -> %d/%d IDENTICAL   %s\n"
                  % (same, n, "PASS" if verdict else "FAIL"), flush=True)
        else:
            verdict = same < n
            print("  -> %d/%d differ       %s\n"
                  % (n - same, n, "PASS" if verdict else "FAIL (a control that "
                     "never fires)"), flush=True)
        if not verdict:
            fail.append(tag)
        return same, n

    arm("A1 ", "eq_off", "eq_parent", MAPS5 + MAPS_WALL, True)
    arm("A2 ", "eq_v529", "eq_parent", MAPS5, False)
    arm("A3 ", "eq_u527", "eq_527", MAPS5 + MAPS_WALL, True)
    arm("A3n", "eq_u527", "eq_parent", MAPS5, False)
    arm("A4 ", "eq_u528", "eq_528", MAPS5 + MAPS_WALL, True)
    arm("A4n", "eq_u528", "eq_parent", MAPS5, False)

    print("TRACEBACKS: %d" % len([f for f in fail if f.startswith("TRACE")]))
    print("RESULT:", "PASS" if not fail else "FAIL " + str(sorted(set(fail))))
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
