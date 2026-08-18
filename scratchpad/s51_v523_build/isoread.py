#!/usr/bin/env python3
"""SINGLE-FLAG ISOLATION: four arms in the same blocks on the same seeds.

parent / iPIN (pincer only) / iPRES (presence only) / iGUN (gunnear only).
⛔ A block counts only when ALL FOUR arms wrote all 36 rows -- the run_grid
writer flushes per game, so a half-block would otherwise pool silently and
favour whichever arm got further.

⚠ THE FIXTURE'S OWN SAME-CONFIG FALSE-POSITIVE FLOOR IS ~4.7-5.6pp (v519 open
item 2, three independent instances) and this leg has NO known-zero arm of its
own -- the headline's `flagoff` is the control for that, on different seeds.
So a single-flag delta under ~6pp here is a DIRECTION, not a separation, and
that is printed with every row rather than left to the reader.
"""
import csv
import math
import sys
from pathlib import Path

B = Path(sys.argv[1])
ARMS = ["parent", "parentB", "iNOPHASE", "v522"]
EXPECT = 36


def complete(b):
    for a in ARMS:
        p = b / (a + ".tsv")
        if not p.exists() or sum(1 for _ in open(p)) != EXPECT + 1:
            return False
    return True


blocks = [b for b in sorted(B.glob("b*"), key=lambda p: int(p.name[1:]))
          if complete(b)]
print("blocks pooled: %d  (n = %d per arm)" % (len(blocks), len(blocks) * EXPECT))
if not blocks:
    sys.exit(0)

rows = {a: [] for a in ARMS}
for b in blocks:
    for a in ARMS:
        rows[a] += list(csv.DictReader(open(b / (a + ".tsv")), delimiter="\t"))


def stats(r):
    n = len(r)
    wins = sum(1 for x in r if x["ours"] == "US")
    kills = [int(x["turn"]) for x in r
             if x["ours"] == "US" and x["cond"].startswith("Core destroyed")]
    ourcore = sum(1 for x in r if x["ours"] == "OPP"
                  and x["cond"].startswith("Core destroyed"))
    k = sorted(kills)
    def by(t):
        return sum(1 for x in k if x <= t)
    med = k[len(k) // 2] if k else -1
    return dict(n=n, wins=wins, k150=by(150), k180=by(180), k200=by(200),
                k300=by(300), med=med, ourcore=ourcore,
                r1000=sum(1 for x in r if int(x["turn"]) >= 1000))


S = {a: stats(rows[a]) for a in ARMS}
print("\n%-8s %6s %7s %8s %8s %8s %8s %8s %8s"
      % ("arm", "n", "wins%", "<=150", "<=180", "<=200", "<=300", "medkill",
         "ourcore"))
for a in ARMS:
    s = S[a]
    print("%-8s %6d %6.1f%% %3d(%.3f) %3d(%.3f) %3d(%.3f) %3d(%.3f) %7d %7d"
          % (a, s["n"], 100.0 * s["wins"] / s["n"],
             s["k150"], s["k150"] / s["n"], s["k180"], s["k180"] / s["n"],
             s["k200"], s["k200"] / s["n"], s["k300"], s["k300"] / s["n"],
             s["med"], s["ourcore"]))


def hw(p1, n1, p2, n2):
    pb = (p1 * n1 + p2 * n2) / (n1 + n2)
    return 1.96 * math.sqrt(pb * (1 - pb) * (1.0 / n1 + 1.0 / n2)) * 100


print("\nvs parent (pp) -- ⚠ the same-config false-positive floor on this "
      "fixture is ~4.7-5.6pp; anything under ~6pp is a DIRECTION")
for a in ARMS[1:]:
    for lab, key in (("wins", "wins"), ("k<=200", "k200"), ("k<=300", "k300")):
        p = S[a][key] / S[a]["n"]
        q = S["parent"][key] / S["parent"]["n"]
        h = hw(p, S[a]["n"], q, S["parent"]["n"])
        d = (p - q) * 100
        print("  %-6s %-7s %+6.2f pp (hw %.2f) %s%s"
              % (a, lab, d, h, "OUTSIDE" if abs(d) > h else "inside",
                 "" if abs(d) > 6 else "  [under the floor]"))
