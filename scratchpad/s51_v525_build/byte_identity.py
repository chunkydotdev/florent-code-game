#!/usr/bin/env python3
"""v525 verification (b): deterministic byte-identity vs the true parent
(bots/_v524exact), NOISE_ON=False both sides, --tle 0, seed pinned, replay
bytes cmp'd. Method per BUILD-REPORT-v524exact-2026-08-18.md finding (b) /
v518 finding 2 (--seed alone does not pin a game; NOISE_ON must also be off).

UNCHANGED maps (must be IDENTICAL, both seats): drakkarfjord (siege-active,
unaffected by either change), midgard (still CRIPPLE), archipelago (still
GATED, via FS_MAP_SKIP not this build's thresholds).

FLIPPED maps (must DIFFER, both seats -- the plank now actually runs there):
yulerune, antler, fjordgate.

Usage: .venv/bin/python3 scratchpad/s51_v525_build/byte_identity.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FCODE = str(ROOT / ".venv/bin/fcode")
OUT = ROOT / "scratchpad/s51_v525_build/byte_check"
OUT.mkdir(parents=True, exist_ok=True)

V525 = str(ROOT / "scratchpad/s51_v525_build/eq_v525")
V524 = str(ROOT / "scratchpad/s51_v525_build/eq_v524")
OPP = str(ROOT / "scratchpad/s51_v525_build/eq_opp")

UNCHANGED = ["drakkarfjord", "midgard", "archipelago"]
FLIPPED = ["yulerune", "antler", "fjordgate"]
SEED = 525919


def run(arm_dir, arm_name, mapname, seat):
    tag = f"{mapname}_seat{seat}_{arm_name}"
    replay = OUT / f"{tag}.replay26"
    errfile = OUT / f"{tag}.err"
    if seat == "A":
        A, B = arm_dir, OPP
    else:
        A, B = OPP, arm_dir
    cmd = [FCODE, "run", A, B, str(ROOT / "maps" / f"{mapname}.map26"),
           "--seed", str(SEED), "--tle", "0", "--replay", str(replay), "--json"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    errfile.write_text(r.stderr)
    return replay, r.stdout, r.stderr


def main():
    fail = False
    print("=== UNCHANGED maps: v525 vs true parent v524, must be IDENTICAL ===")
    for mapname in UNCHANGED:
        for seat in ("A", "B"):
            r525, out525, err525 = run(V525, "v525", mapname, seat)
            r524, out524, err524 = run(V524, "v524", mapname, seat)
            same = r525.read_bytes() == r524.read_bytes()
            tb = ("Traceback" in err525) or ("Traceback" in err524)
            status = "IDENTICAL" if same else "DIFFERS (FAIL, expected identical)"
            print(f"  {mapname:14s} seat{seat}  {status}  traceback={tb}")
            if not same or tb:
                fail = True

    print("\n=== FLIPPED maps: v525 vs true parent v524, must DIFFER ===")
    for mapname in FLIPPED:
        for seat in ("A", "B"):
            r525, out525, err525 = run(V525, "v525", mapname, seat)
            r524, out524, err524 = run(V524, "v524", mapname, seat)
            same = r525.read_bytes() == r524.read_bytes()
            tb = ("Traceback" in err525) or ("Traceback" in err524)
            status = "DIFFERS (expected)" if not same else "IDENTICAL (FAIL, expected differ)"
            print(f"  {mapname:14s} seat{seat}  {status}  traceback={tb}")
            if same or tb:
                fail = True

    print("\nRESULT:", "FAIL" if fail else "PASS")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
