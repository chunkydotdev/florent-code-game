#!/usr/bin/env python3
"""v528 verification: FLAG-OFF BYTE-IDENTITY + STANDDOWN + NEGATIVE CONTROLS.

Method is v524/v525/v526/v527's: `NOISE_ON = False` on BOTH sides (ours and
`bots/_v488beltbreak2`), `--tle 0`, replay bytes compared.  `--seed` alone does
NOT pin a game (v518 finding 1/2) -- NOISE_ON must also be off.

⛔ WHY v528's STANDDOWN IS NOT A MAP LIST.  Every recent build in this line
gated on the ferry-siege, so `midgard` (CRIPPLE) and `archipelago` (GATED) were
maps where the plank provably could not run and IDENTICAL was the assertion.
**v528's planks are in the ECO layer, which runs on every map** -- there is no
map where they stand down, so a map-list standdown here would be an assertion
that cannot fail.  The standdown that CAN fail is the SUB-FLAG one:

  ARM 3 `eq_master`  master ON, all three sub-flags OFF.  Must be IDENTICAL to
  the parent everywhere.  If it is not, the master is doing something on its
  own and the per-plank ablations below do not mean what they say.

FOUR ARMS, EACH DRIVEN TO THE OTHER VERDICT:
  1 `eq_off`     LOKI_FS_V528=False    vs parent -> IDENTICAL (the known-zero)
  2 `eq_v528`    as fired              vs parent -> DIFFERS   (negative control)
  3 `eq_master`  master on, planks off vs parent -> IDENTICAL (standdown)
  4 per-plank    conn / walk / wire    vs parent -> each DIFFERS on >=1 cell
    ⭐ Per-plank is reported as a COUNT, not a rate.  CONNCOST re-orders on
    every map; WALK fires only where a body parks on ore, and WIRE only where a
    second harvester is queued behind a live chain -- both are RARE by
    construction, so demanding 16/16 would be demanding the wrong thing.  What
    must not happen is 0/16: a plank that never fires anywhere is not a plank.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FCODE = str(ROOT / ".venv/bin/fcode")
D = ROOT / "scratchpad/s51_v528_build"
OUT = D / "byte_check"
OUT.mkdir(parents=True, exist_ok=True)
OPP = str(D / "eq_opp")

MAPS5 = ["atoll", "drakkarfjord", "glacierkeep", "nordkap", "yulerune"]
MAPS_WALL = ["valkyrie", "ragnarok", "midgard"]
SEED = 528919


def run(arm, name, mapname, seat):
    tag = f"{mapname}_seat{seat}_{name}"
    replay = OUT / f"{tag}.replay26"
    A, B = (str(D / arm), OPP) if seat == "A" else (OPP, str(D / arm))
    cmd = [FCODE, "run", A, B, str(ROOT / "maps" / f"{mapname}.map26"),
           "--seed", str(SEED), "--tle", "0", "--replay", str(replay), "--json"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    (OUT / f"{tag}.err").write_text(r.stderr)
    return replay.read_bytes(), ("Traceback" in r.stderr)


def cells(maps):
    for m in maps:
        for s in ("A", "B"):
            yield m, s


def main():
    fail = False
    base = {}
    for m, s in cells(MAPS5 + MAPS_WALL):
        base[(m, s)], tb = run("eq_parent", "parent", m, s)
        if tb:
            print("PARENT TRACEBACK %s %s" % (m, s), flush=True)
            fail = True

    print("=== ARM 1  LOKI_FS_V528=False vs PARENT -- must be IDENTICAL ===",
          flush=True)
    same = 0
    for m, s in cells(MAPS5):
        b, tb = run("eq_off", "off", m, s)
        ok = b == base[(m, s)]
        same += ok
        print("  %-14s seat%s  %s  traceback=%s"
              % (m, s, "IDENTICAL" if ok else "DIFFERS(FAIL)", tb), flush=True)
        if not ok or tb:
            fail = True
    print("  flag-off identical: %d/%d" % (same, 2 * len(MAPS5)), flush=True)

    print("\n=== ARM 3  STANDDOWN: master ON, all sub-flags OFF -- IDENTICAL ===",
          flush=True)
    sd = 0
    for m, s in cells(MAPS5):
        b, tb = run("eq_master", "master", m, s)
        ok = b == base[(m, s)]
        sd += ok
        print("  %-14s seat%s  %s"
              % (m, s, "IDENTICAL" if ok else "DIFFERS(FAIL)"), flush=True)
        if not ok or tb:
            fail = True
    print("  standdown identical: %d/%d" % (sd, 2 * len(MAPS5)), flush=True)

    print("\n=== ARM 2  NEGATIVE CONTROL: v528 as fired vs PARENT -- must DIFFER ===",
          flush=True)
    diff = 0
    allc = list(cells(MAPS5 + MAPS_WALL))
    for m, s in allc:
        b, tb = run("eq_v528", "v528", m, s)
        d = b != base[(m, s)]
        diff += d
        print("  %-14s seat%s  %s  traceback=%s"
              % (m, s, "DIFFERS" if d else "IDENTICAL(!)", tb), flush=True)
        if tb:
            fail = True
    print("  as-fired differs: %d/%d" % (diff, len(allc)), flush=True)
    if diff == 0:
        print("  NEGATIVE CONTROL FAIL: nothing fired anywhere", flush=True)
        fail = True

    print("\n=== ARM 4  PER-PLANK: each must DIFFER on at least one cell ===",
          flush=True)
    for arm in ("eq_conn", "eq_walk", "eq_wire"):
        n = 0
        for m, s in allc:
            b, tb = run(arm, arm, m, s)
            n += (b != base[(m, s)])
            if tb:
                print("  %s TRACEBACK %s %s" % (arm, m, s), flush=True)
                fail = True
        print("  %-9s differs on %d/%d cells  %s"
              % (arm, n, len(allc), "" if n else "<< PLANK NEVER FIRED (FAIL)"),
              flush=True)
        if n == 0:
            fail = True

    print("\nRESULT:", "FAIL" if fail else "PASS", flush=True)
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
