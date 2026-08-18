#!/usr/bin/env python3
"""Flag-off behavioural read: flag-off vs a frozen copy of the parent."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from summarise import fold, read  # noqa: E402

B = Path("scratchpad/s51_v519_build")


def hw(p1, n1, p2, n2):
    pb = (p1 * n1 + p2 * n2) / (n1 + n2)
    return 1.96 * math.sqrt(pb * (1 - pb) * (1.0 / n1 + 1.0 / n2)) * 100


allp = {"flagoff": [], "parent": []}
for fx in sys.argv[1:]:
    o = {}
    for a in ("flagoff", "parent"):
        paths = sorted(str(p) for p in (B / fx).glob("b*/%s.tsv" % a))
        allp[a] += paths
        o[a] = fold(read(paths))
    f, p = o["flagoff"], o["parent"]
    d = 100 * (f["wins"] / f["n"] - p["wins"] / p["n"])
    h = hw(f["wins"] / f["n"], f["n"], p["wins"] / p["n"], p["n"])
    dk = 100 * (f["k300"] / f["n"] - p["k300"] / p["n"])
    hk = hw(f["k300"] / f["n"], f["n"], p["k300"] / p["n"], p["n"])
    print("%-6s n=%d each  flagoff %d (%.1f%%)  parent %d (%.1f%%)  "
          "dwins %+.2f pp (hw %.2f) %s  dk300 %+.2f pp (hw %.2f) %s"
          % (fx, f["n"], f["wins"], 100 * f["wins"] / f["n"], p["wins"],
             100 * p["wins"] / p["n"], d, h, "OUTSIDE" if abs(d) > h else "inside",
             dk, hk, "OUTSIDE" if abs(dk) > hk else "inside"))
f, p = fold(read(allp["flagoff"])), fold(read(allp["parent"]))
d = 100 * (f["wins"] / f["n"] - p["wins"] / p["n"])
h = hw(f["wins"] / f["n"], f["n"], p["wins"] / p["n"], p["n"])
dk = 100 * (f["k300"] / f["n"] - p["k300"] / p["n"])
hk = hw(f["k300"] / f["n"], f["n"], p["k300"] / p["n"], p["n"])
print("POOLED n=%d each  flagoff %d (%.1f%%)  parent %d (%.1f%%)  "
      "dwins %+.2f pp (hw %.2f) %s  dk300 %+.2f pp (hw %.2f) %s"
      % (f["n"], f["wins"], 100 * f["wins"] / f["n"], p["wins"],
         100 * p["wins"] / p["n"], d, h, "OUTSIDE" if abs(d) > h else "inside",
         dk, hk, "OUTSIDE" if abs(dk) > hk else "inside"))
print("  medkill %d vs %d | ourcore %d vs %d | r1000 %d vs %d | tb %d/%d"
      % (f["median_kill"], p["median_kill"], f["ourcore"], p["ourcore"],
         f["r1000"], p["r1000"], f["tb"], p["tb"]))
