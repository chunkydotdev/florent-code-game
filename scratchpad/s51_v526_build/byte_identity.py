#!/usr/bin/env python3
"""v526 verification (b): FLAG-OFF BYTE-IDENTITY 10/10 + a NEGATIVE CONTROL.

Method: the v524/v525 method -- `NOISE_ON = False` on BOTH sides (ours and
`bots/_v488beltbreak2`), `--tle 0`, replay bytes `cmp`'d.  `--seed` alone does
not pin a game (v518 finding 1/2); NOISE_ON must also be off.

TWO ARMS, DRIVEN BOTH WAYS:
  * `eq_off`  = `bots/_v526transit` with `LOKI_FS_V526 = False`.  Against the
    TRUE parent `bots/_v525flip` this must be IDENTICAL on every map -- that is
    the known-zero claim.
  * `eq_v526` = `bots/_v526transit` as fired.  Against the same parent it must
    DIFFER on ferry-siege-active maps -- the NEGATIVE CONTROL, without which
    "identical" would also be produced by a plank that never runs.

⛔ midgard (CRIPPLE) and archipelago (GATED) are expected IDENTICAL in BOTH
arms: the ferry-siege never runs there, so v526 cannot change them.  They are
carried as the standdown assertion, not as evidence about the plank.

Usage: .venv/bin/python3 scratchpad/s51_v526_build/byte_identity.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FCODE = str(ROOT / ".venv/bin/fcode")
OUT = ROOT / "scratchpad/s51_v526_build/byte_check"
OUT.mkdir(parents=True, exist_ok=True)

OFF = str(ROOT / "scratchpad/s51_v526_build/eq_off")
V526 = str(ROOT / "scratchpad/s51_v526_build/eq_v526")
PARENT = str(ROOT / "scratchpad/s51_v526_build/eq_v525")
OPP = str(ROOT / "scratchpad/s51_v526_build/eq_opp")

# the 8-map headline panel: the 6-map panel set + antler + fjordgate
ACTIVE = ["atoll", "drakkarfjord", "glacierkeep", "nordkap", "yulerune",
          "antler", "fjordgate"]
STANDDOWN = ["midgard", "archipelago"]
SEED = 526919


def run(arm_dir, arm_name, mapname, seat):
    tag = f"{mapname}_seat{seat}_{arm_name}"
    replay = OUT / f"{tag}.replay26"
    if seat == "A":
        A, B = arm_dir, OPP
    else:
        A, B = OPP, arm_dir
    cmd = [FCODE, "run", A, B, str(ROOT / "maps" / f"{mapname}.map26"),
           "--seed", str(SEED), "--tle", "0", "--replay", str(replay),
           "--json"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    (OUT / f"{tag}.err").write_text(r.stderr)
    return replay, r.stderr


def main():
    fail = False
    same_off = diff_v526 = 0
    print("=== ARM 1: LOKI_FS_V526=False vs TRUE PARENT -- must be IDENTICAL ===")
    for mapname in ACTIVE + STANDDOWN:
        for seat in ("A", "B"):
            ro, eo = run(OFF, "off", mapname, seat)
            rp, ep = run(PARENT, "parent", mapname, seat)
            same = ro.read_bytes() == rp.read_bytes()
            tb = ("Traceback" in eo) or ("Traceback" in ep)
            same_off += 1 if same else 0
            print("  %-14s seat%s  %-9s traceback=%s"
                  % (mapname, seat, "IDENTICAL" if same else "DIFFERS(FAIL)", tb))
            if not same or tb:
                fail = True

    print("\n=== ARM 2 (NEGATIVE CONTROL): v526 AS FIRED vs TRUE PARENT ===")
    print("    ferry-active maps must DIFFER; standdown maps must be IDENTICAL")
    for mapname in ACTIVE:
        for seat in ("A", "B"):
            rv, ev = run(V526, "v526", mapname, seat)
            rp, ep = run(PARENT, "parent", mapname, seat)
            same = rv.read_bytes() == rp.read_bytes()
            tb = ("Traceback" in ev) or ("Traceback" in ep)
            diff_v526 += 0 if same else 1
            print("  %-14s seat%s  %-9s traceback=%s"
                  % (mapname, seat, "IDENTICAL(FAIL)" if same else "DIFFERS", tb))
            if same or tb:
                fail = True
    for mapname in STANDDOWN:
        for seat in ("A", "B"):
            rv, ev = run(V526, "v526", mapname, seat)
            rp, ep = run(PARENT, "parent", mapname, seat)
            same = rv.read_bytes() == rp.read_bytes()
            print("  %-14s seat%s  %-9s  (standdown assertion)"
                  % (mapname, seat, "IDENTICAL" if same else "DIFFERS(FAIL)"))
            if not same:
                fail = True

    print("\nflag-off identical: %d/%d   ·   as-fired differs on active: %d/%d"
          % (same_off, 2 * len(ACTIVE + STANDDOWN), diff_v526, 2 * len(ACTIVE)))
    print("RESULT:", "FAIL" if fail else "PASS")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
