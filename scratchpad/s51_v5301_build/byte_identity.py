#!/usr/bin/env python3
"""v530.1 FLAG-OFF BYTE-IDENTITY.

Method is v524-v530's, unchanged: `NOISE_ON = False` on BOTH sides (ours and
the opponent copy `eq_opp`, which differs from `bots/_v488beltbreak2` by that
ONE line), `--tle 0`, replay BYTES compared.  `--seed` alone does not pin a
game (v515 finding 1) -- NOISE_ON must also be off.

FOUR ARMS, EACH DRIVEN TO THE OTHER VERDICT.  ⛔ THE NEGATIVE CONTROLS ARE NOT
DECORATION: without B2, B1 could pass because the whole v530.1 tree is inert.

  B1  eq_bootoff   (FS_V5301_BOOTFIX False) vs eq_v530    -> IDENTICAL 10/10
  B2  eq_v531      (as fired)               vs eq_v530    -> DIFFERS
  B3  eq_masteroff (LOKI_FS_V530 False)     vs eq_parent  -> IDENTICAL 10/10
                                              (the v530 master property must
                                               SURVIVE this build: flag off is
                                               still `_v529merge` exactly)
  B4  eq_v531      (as fired)               vs eq_parent  -> DIFFERS
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FCODE = str(ROOT / ".venv/bin/fcode")
D = ROOT / "scratchpad/s51_v5301_build"
OUT = D / "byte_check"
OUT.mkdir(parents=True, exist_ok=True)
OPP = str(D / "eq_opp")

MAPS5 = ["atoll", "drakkarfjord", "glacierkeep", "nordkap", "yulerune"]
SEED = 531820


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
    cache = {}

    def get(arm, m, s):
        if (arm, m, s) not in cache:
            b, tb = run(arm, m, s)
            cache[(arm, m, s)] = b
            if tb:
                print("  TRACEBACK %s %s seat%s" % (arm, m, s), flush=True)
                fail.append("TRACEBACK:%s" % arm)
        return cache[(arm, m, s)]

    def arm(tag, a, b, maps, want_identical):
        print("=== %s  %s vs %s -- must be %s ==="
              % (tag, a, b, "IDENTICAL" if want_identical else "DIFFER"),
              flush=True)
        same = n = 0
        for m, s in cells(maps):
            n += 1
            ok = get(a, m, s) == get(b, m, s)
            same += ok
            print("  %-14s seat%s  %s"
                  % (m, s, "IDENTICAL" if ok else "DIFFERS"), flush=True)
        if want_identical:
            verdict = same == n
            print("  -> %d/%d IDENTICAL   %s\n"
                  % (same, n, "PASS" if verdict else "FAIL"), flush=True)
        else:
            verdict = same < n
            print("  -> %d/%d differ       %s\n"
                  % (n - same, n, "PASS" if verdict
                     else "FAIL (a control that never fires)"), flush=True)
        if not verdict:
            fail.append(tag)

    arm("B1 ", "eq_bootoff", "eq_v530", MAPS5, True)
    arm("B2 ", "eq_v531", "eq_v530", MAPS5, False)
    arm("B3 ", "eq_masteroff", "eq_parent", MAPS5, True)
    arm("B4 ", "eq_v531", "eq_parent", MAPS5, False)

    print("TRACEBACKS: %d" % len([f for f in fail if f.startswith("TRACE")]))
    print("RESULT:", "PASS" if not fail else "FAIL " + str(sorted(set(fail))))
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
