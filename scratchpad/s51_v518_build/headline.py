#!/usr/bin/env python3
"""Headline tables: pooled row, kill-round CDF, per map, per block."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from summarise import fold, read  # noqa: E402

B = Path(sys.argv[1])
ARMS = [("parent517", "parent.tsv"), ("v518_f60", "f60.tsv"),
        ("v518_f45", "f45.tsv"), ("v518_f30", "f30.tsv")]
blocks = sorted(B.glob("b*"), key=lambda p: int(p.name[1:]))
print("blocks: %d" % len(blocks))
pool = {}
for name, fn in ARMS:
    paths = [str(b / fn) for b in blocks if (b / fn).exists()]
    pool[name] = fold(read(paths))
    from summarise import line
    print(line(name, pool[name]))

# ⭐ s51 KILL_TARGET directive: median kill <= r180, tracked metric = share of
# ALL games killed by r200 (baseline ~16.5%, target > 50%), r300 the hard floor.
MARKS = (150, 180, 200, 250, 300, 400, 500)
print("\nKILL-ROUND CDF (share of ALL games with a core kill by round R)")
print("%-12s " % "arm" + " ".join("%11s" % ("<=%d" % r) for r in MARKS))
for name, _ in ARMS:
    o = pool[name]
    n = o["n"]
    ks = o["kill_rounds"]
    row = [sum(1 for k in ks if k <= r) for r in MARKS]
    print("%-12s " % name + " ".join("%4d(%.3f)" % (c, c / n) for c in row))

print("\nPER MAP  wins/90 (k<=300)")
maps = ["atoll", "drakkarfjord", "glacierkeep", "midgard", "nordkap"]
for m in maps:
    cells = []
    for name, fn in ARMS:
        rows = [r for r in read([str(b / fn) for b in blocks
                                 if (b / fn).exists()]) if r["map"] == m]
        o = fold(rows)
        cells.append("%s %2d/%2d(k%2d)" % (name, o["wins"], o["n"], o["k300"]))
    print("%-14s %s" % (m, "  ".join(cells)))

print("\nPER BLOCK wins/30  " + " / ".join(n for n, _ in ARMS))
out = []
for b in blocks:
    cells = []
    for name, fn in ARMS:
        o = fold(read([str(b / fn)])) if (b / fn).exists() else {"wins": -1}
        cells.append(str(o["wins"]))
    out.append("/".join(cells))
print(" · ".join(out))
