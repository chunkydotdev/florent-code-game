#!/usr/bin/env python3
"""SLOT-10 COLLISION READBACK -- the mandatory pre-flight for any crew-ON arm.

⛔ WHY THIS EXISTS.  `FS_SUPP_SLOT = SLOT_FERRY_ID` (slot 10): with the crew ON
it is body 2's PUBLISH CHANNEL, and it is ALSO the chassis home-ferry's ping
slot (`raid.py:1216`).  Two writers on one buffered slot is the r197 lost-update
defect -- the largest timing defect this line has measured (183 rounds).  The
chassis is supposed to stand its home ferry down whenever the crew is on, via
`FERRY_HOME_ON`, and that constant is a MODULE-LEVEL DERIVED DEFAULT computed at
import from `FS_CREW_ON`.  The s51 06:24Z crewconv pre-flight found this live:
an arm that APPENDED `FS_CREW_ON = True` got `COLLISION: True`, because the
derivation had already run with the old value.

THIS SCRIPT ASSERTS THE FIX, IT DOES NOT ASSUME IT: v520 turns the crew on
through `fs_crew_on()`, a RUN-TIME read, and `_ferry_home_on()` (v516 change 1c)
consults it.  So the home ferry must read OFF whenever the crew reads ON.

GUARD, DRIVEN BOTH WAYS -- and it is the whole point of the file.  The same
predicate is evaluated on THREE configurations and must produce BOTH verdicts:
  * v520 fired (crew ON)         -> home ferry OFF, no collision      [PASS]
  * v520 master off (crew OFF)   -> home ferry ON, no collision       [PASS]
  * the KNOWN-BAD form: crew ON at the definition site with the v516 read-site
    fix disabled -> home ferry ON while the crew is ON -> COLLISION   [must be
    detected, or this script cannot see the defect it exists for]
"""
import importlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

PROBE = r'''
import sys
sys.path.insert(0, %r)
import doctrine as D
from raid import RaidMixin


class _P(RaidMixin):
    pass


crew = D.fs_crew_on()
home = _P()._ferry_home_on()
# slot 10 has two writers iff the crew publishes into it AND the chassis home
# ferry is still allowed to ping it.
collide = bool(crew and D.LOKI_FS_V514 and D.FS_V514_RELAY and home)
print("crew=%%s home=%%s COLLISION=%%s" %% (crew, home, collide))
sys.exit(2 if collide else 0)
'''


def run(tree: Path) -> tuple:
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as fh:
        fh.write(PROBE % str(tree))
        p = fh.name
    r = subprocess.run([sys.executable, p], capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def main():
    ok = True
    tmp = Path(tempfile.mkdtemp())
    cases = []

    fired = REPO / "bots/_v520pincer"
    cases.append(("v520 FIRED (crew ON)", fired, 0))

    off = tmp / "off"
    shutil.copytree(fired, off)
    with open(off / "doctrine.py", "a") as fh:
        fh.write("\nLOKI_FS_V520 = False\n")
    cases.append(("v520 master OFF (crew OFF)", off, 0))

    bad = tmp / "bad"
    shutil.copytree(fired, bad)
    with open(bad / "doctrine.py", "a") as fh:
        # the KNOWN-BAD form: crew on, read-site fix off.  This is the shape the
        # 06:24Z pre-flight caught, reconstructed so the detector is proved able
        # to produce the other verdict.
        fh.write("\nFS_V516_FERRY_READSITE = False\nFS_CREW_ON = True\n")
    cases.append(("KNOWN-BAD control (crew ON, read-site fix OFF)", bad, 2))

    for name, tree, want in cases:
        rc, out = run(tree)
        verdict = "PASS" if rc == want else "FAIL"
        if rc != want:
            ok = False
        print("%-46s rc=%d want=%d  %-40s %s"
              % (name, rc, want, out.splitlines()[-1] if out else "", verdict))
    shutil.rmtree(tmp, ignore_errors=True)
    print("RESULT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
