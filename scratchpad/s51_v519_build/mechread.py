#!/usr/bin/env python3
"""Mechanism-arm read: plants, refusals, and the MODESWITCH signature per arm.

⛔ THE WIN COLUMN OF A MECHANISM ARM IS NOT READ (v518's rule, n=36 is the
one-draw law and nothing else).  What is read is the COUNTERS.
"""
import glob
import re
import sys
from collections import Counter

B = "scratchpad/s51_v519_build/mech"
print("%-9s %7s %8s %8s %8s %9s" % ("arm", "games", "GFlines", "PLANTS",
                                    "MODE519", "modegames"))
for a in sys.argv[1:]:
    logs = sorted(glob.glob("%s/%s/log/*.err" % (B, a)))
    gf = plants = mode = 0
    modeg = set()
    for f in logs:
        for ln in open(f):
            if ln.startswith("GF519 PLANT"):
                plants += 1
            elif ln.startswith("GF519"):
                gf += 1
            elif ln.startswith("MODE519"):
                mode += 1
                modeg.add(f.split("/")[-1].split("_")[0])
    print("%-9s %7d %8d %8d %8d  %s" % (a, len(logs), gf, plants, mode,
                                        ",".join(sorted(modeg)) or "-"))
