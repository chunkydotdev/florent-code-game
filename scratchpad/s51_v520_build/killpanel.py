#!/usr/bin/env python3
"""THE KILL_TARGET PANEL + the heal-back movement, per arm and per map.

`PROGRAMME.md` KILL_TARGET (Magnus, 2026-08-18): median kill <= r180 · tracked
metric = share of ALL games killed by r200 (baseline ~16.5%, target > 50%) ·
r300 the hard admissibility floor (DEFENCE_ADMISSION_BAR, ITT: the share of ALL
games ending in a core kill by r300 must not FALL vs control).

Two-sample naive half-widths.  ⛔ LOCAL FIXTURE: the s39 audit measured a
pair-weighted local DEFF of 0.98 on a balanced-by-construction shard fixture,
so the platform constants (1.529 rated / 1.833 unrated) do NOT apply and are
not used.  ⚠ v518 finding 2 measured a 4.6pp FALSE POSITIVE at n=810/arm on
byte-identical play from POOLING non-time-adjacent local fixtures; this grid
pools 13 time-adjacent blocks, and the msoff-vs-parent contrast is carried as
this report's own known-zero control for exactly that reason.
"""
import math
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from summarise import fold, read  # noqa: E402

B = Path(sys.argv[1])
ARMS = [("parent519", "parent.tsv"), ("v520_FIRED", "v520.tsv"),
        ("v520_flagoff", "flagoff.tsv")]
EXPECT = int(os.environ.get("BLOCKN", "36"))
MAPS = ["atoll", "drakkarfjord", "glacierkeep", "midgard", "nordkap",
        "yulerune"]


def complete(b):
    for _n, fn in ARMS:
        p = b / fn
        if not p.exists() or sum(1 for _ in open(p)) != EXPECT + 1:
            return False
    return True


blocks = [b for b in sorted(B.glob("b*"), key=lambda p: int(p.name[1:]))
          if complete(b)]
rows = {n: read([str(b / fn) for b in blocks]) for n, fn in ARMS}
pool = {n: fold(rows[n]) for n, _ in ARMS}


def hw(p1, n1, p2, n2):
    pb = (p1 * n1 + p2 * n2) / (n1 + n2)
    return 1.96 * math.sqrt(pb * (1 - pb) * (1.0 / n1 + 1.0 / n2)) * 100


print("blocks pooled: %d  (n = %d per arm)" % (len(blocks), pool[ARMS[0][0]]["n"]))
print()
print("=== THE KILL_TARGET PANEL ===")
print("%-12s %6s %7s %8s %8s %8s %8s %8s %8s %7s" % (
    "arm", "n", "wins%", "<=r150", "<=r180", "<=r200", "<=r250", "<=r300",
    "medkill", "ourcore"))
for n, _ in ARMS:
    o = pool[n]
    ks = o["kill_rounds"]
    N = o["n"]
    cells = []
    for r in (150, 180, 200, 250, 300):
        c = sum(1 for k in ks if k <= r)
        cells.append("%3d(%.3f)" % (c, c / N))
    print("%-12s %6d %6.1f%% %s %7d %7d" % (
        n, N, 100.0 * o["wins"] / N, " ".join(cells), o["median_kill"],
        o["ourcore"]))
print()
base = pool["parent519"]
for n, _ in ARMS[1:]:
    o = pool[n]
    N, M = o["n"], base["n"]
    for lab, key in (("wins", "wins"), ("k<=200", "k200x"), ("k<=300", "k300")):
        if key == "k200x":
            a = sum(1 for k in o["kill_rounds"] if k <= 200)
            b = sum(1 for k in base["kill_rounds"] if k <= 200)
        else:
            a, b = o[key], base[key]
        d = 100.0 * (a / N - b / M)
        h = hw(a / N, N, b / M, M)
        print("%-12s vs parent  %-7s %+6.2f pp (hw %.2f) %s"
              % (n, lab, d, h, "OUTSIDE" if abs(d) > h else "inside"))
    print()

print("=== PER MAP: wins/n  [k<=300]  {k<=200} ===")
print("%-14s %s" % ("map", "  ".join("%-24s" % n for n, _ in ARMS)))
for m in MAPS:
    cells = []
    for n, _ in ARMS:
        rr = [r for r in rows[n] if r["map"] == m]
        o = fold(rr)
        k2 = sum(1 for k in o["kill_rounds"] if k <= 200)
        cells.append("%2d/%2d [%2d] {%2d}      " % (o["wins"], o["n"],
                                                    o["k300"], k2))
    print("%-14s %s" % (m, "  ".join(cells)))
print()
print("=== PER BLOCK wins/%d   %s ===" % (EXPECT,
                                          " / ".join(n for n, _ in ARMS)))
out = []
for b in blocks:
    out.append("/".join(str(fold(read([str(b / fn)]))["wins"])
                        for _n, fn in ARMS))
print(" · ".join(out))
