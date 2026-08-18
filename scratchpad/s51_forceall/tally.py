#!/usr/bin/env python3
"""Per-map tally for the s51 FORCEALL probe (rush vs 50%-mirror baseline on
the 5 stood-down maps: antler, archipelago, fjordgate, midgard, yulerune).

Reuses the SAME fold/read machinery as scratchpad/s51_v520_build/summarise.py
(the tally path validated against the banked 63.8% v520 figure) so this
report's numbers are computed the identical way as every other s51 grid.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "s51_v520_build"))
from summarise import fold, read  # noqa: E402

TSV = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "results.tsv"
MAPS = ["antler", "archipelago", "fjordgate", "midgard", "yulerune"]

rows = read([str(TSV)])
print(f"total rows read: {len(rows)}")
print()

overall = fold(rows)


def hw_one(p, n):
    return 1.96 * math.sqrt(p * (1 - p) / n) * 100 if n else float("nan")


print("=== PER MAP (n=90 target, 45/seat) ===")
print("%-14s %4s %6s %8s %8s %8s %6s %6s %6s %6s" % (
    "map", "n", "wins%", "hw95", "k<=300", "medkill", "ourcore",
    "r1000", "tb", "seatA/B"))
per_map = {}
for m in MAPS:
    rr = [r for r in rows if r["map"] == m]
    o = fold(rr)
    per_map[m] = o
    N = o["n"]
    wpct = 100.0 * o["wins"] / N if N else float("nan")
    hw = hw_one(o["wins"] / N, N) if N else float("nan")
    k300pct = 100.0 * o["k300"] / N if N else float("nan")
    seatA = sum(1 for r in rr if r["seat"] == "A")
    seatB = sum(1 for r in rr if r["seat"] == "B")
    print("%-14s %4d %5.1f%% %6.2f %5d(%.1f%%) %6d %6d %6d %6d %4d/%-4d" % (
        m, N, wpct, hw, o["k300"], k300pct, o["median_kill"], o["ourcore"],
        o["r1000"], o["tb"], seatA, seatB))

print()
print("=== HEADROOM ARITHMETIC: (S - 50) / 15 per map, for maps clearing 50% ===")
for m in MAPS:
    o = per_map[m]
    N = o["n"]
    if N == 0:
        continue
    S = 100.0 * o["wins"] / N
    if S > 50.0:
        headroom = (S - 50.0) / 15.0
        print(f"  {m:14s} S={S:5.1f}%  (S-50)/15 = {headroom:+.3f}")
    else:
        print(f"  {m:14s} S={S:5.1f}%  <=50, no headroom credit")

print()
print("=== POOLED (5 maps) ===")
N = overall["n"]
print(f"  n={N}  wins={overall['wins']} ({100.0*overall['wins']/N:.1f}%)  "
      f"k<=300={overall['k300']} ({100.0*overall['k300']/N:.1f}%)  "
      f"medkill={overall['median_kill']}  ourcore={overall['ourcore']}  "
      f"r1000={overall['r1000']}  tracebacks={overall['tb']}")

print()
print("=== TRACEBACK CHECK (must be 0) ===")
tb_rows = [r for r in rows if int(r["tracebacks"]) > 0]
if tb_rows:
    print(f"  !!! {len(tb_rows)} rows with tracebacks !!!")
    for r in tb_rows:
        print(" ", r)
else:
    print("  0 tracebacks across all rows -- clean.")
