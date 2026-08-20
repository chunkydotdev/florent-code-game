#!/usr/bin/env python3
"""Harvesters at LATE rounds -- the eco falsifier that can actually move.

⛔ WHY r30 IS THE WRONG WINDOW FOR THIS PLANK.  `hv30` was v526 M6's falsifier
because M6 moved an eco SEAT in the OPENING.  v527's `FS_V527_PSURV_EXTRA`
spends bodies only once the collar is published SEALED, which cannot happen by
r30 -- so hv30 is STRUCTURALLY UNABLE to register this plank's cost and reading
it as a pass would be reading a constant column.  (Measured: 2.42 vs 2.42,
identical to two decimals.)  The windows below are where the spend lands.
"""
import re, sys
from pathlib import Path
L = re.compile(r"V527I SEALNT (\d+) ph (\d+) fwd (\d+) hv (\d+)")
def at(txt, r0):
    last = -1
    for m in L.finditer(txt):
        if int(m.group(1)) >= r0:
            return int(m.group(4))
        last = int(m.group(4))
    return last
for d in sys.argv[1:]:
    fs = sorted(Path(d).glob("*.err"))
    cols = {}
    for r0 in (30, 100, 150, 300, 500):
        vals = [at(f.read_text(), r0) for f in fs]
        vals = [v for v in vals if v >= 0]
        cols[r0] = sum(vals)/len(vals) if vals else -1
    print("%-10s games %3d | " % (Path(d).name, len(fs))
          + " ".join("hv@r%-4d %5.2f" % (r, cols[r]) for r in (30,100,150,300,500)))
