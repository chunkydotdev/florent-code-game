#!/usr/bin/env python3
"""Time-conditioned re-cut of §1.3: the coordinator's selection-effect check.

(1) achievement-round conditioning, (2) round-matched control,
(3) per-round hazard, (4) bodies-only, (5) phase-controlled spawn rate.
"""
import csv
import statistics as st
import sys
from collections import defaultdict

OUT, FROZ = sys.argv[1], sys.argv[2]


def rd(p):
    with open(p) as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


J = {r["file"]: r for r in rd(f"{FROZ}/join.tsv")}
ring = [r for r in rd(f"{OUT}/ars_ring.tsv") if r["file"] in J]


def pct(a, b):
    return f"{100*a/b:.2f}%" if b else "  n/a"


def hdr(t):
    print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)


def wilson(k, n):
    if n == 0:
        return (0.0, 0.0)
    import math
    z = 1.96
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (100 * max(0, c - h), 100 * min(1, c + h))


# =========================================================================== #
hdr("(1) ACHIEVEMENT-ROUND CONDITIONING — when was k reached, not whether")
KEYS = {1: "f_hst12_1", 2: "f_hst12_2", 3: "f_hst12_3", 4: "f_hst12_4",
        6: "f_hst12_6", 8: "f_hst12_8"}
BANDS = [("by r50", 0, 50), ("by r100", 50, 100), ("by r150", 100, 150),
         ("by r200", 150, 200), ("by r250", 200, 250), ("after r250", 250, 10**9)]
print("  hostile ring occupancy (ANY entity of the other team)")
print(f"  {'k':>2} {'achieved in':>12} {'n':>5} {'core died':>10} "
      f"{'died <r250':>11} {'med lag':>8}")
for k, key in KEYS.items():
    for lab, lo, hi in BANDS:
        sub = [r for r in ring if lo <= int(r[key]) < hi and int(r[key]) >= 0]
        if not sub:
            continue
        d = [r for r in sub if int(r["core_dead_rnd"]) >= 0]
        d250 = [r for r in sub if 0 <= int(r["core_dead_rnd"]) < 250]
        lags = [int(r["core_dead_rnd"]) - int(r[key]) for r in d]
        ml = f"{st.median(lags):.0f}" if lags else "-"
        print(f"  {k:>2} {lab:>12} {len(sub):>5} {len(d):>4} "
              f"{pct(len(d),len(sub)):>7} {len(d250):>4} "
              f"{pct(len(d250),len(sub)):>7} {ml:>8}")
    print()

# =========================================================================== #
hdr("(2) ROUND-MATCHED CONTROL — bodies, matched at the achievement round R")
BKEYS = {1: "f_bod_1", 2: "f_bod_2", 3: "f_bod_3", 4: "f_bod_4", 6: "f_bod_6"}


def alive_at(r, R):
    """Side still had a living core at round R, and the replay reached R."""
    cd = int(r["core_dead_rnd"])
    return int(r["rounds"]) > R and (cd < 0 or cd > R)


print("  TREATED = reached k hostile BODIES by round R.")
print("  CONTROL = alive at R, replay runs past R, had NOT reached k by R.")
print("  outcome = core dead within 250 rounds OF R (not of game start), so")
print("  both arms get the same clock.")
print(f"  {'k':>2} {'R':>5} | {'treated n':>9} {'dead<=R+250':>12} | "
      f"{'control n':>9} {'dead<=R+250':>12} | {'ratio':>6}")
for k, key in BKEYS.items():
    for R in (50, 100, 150, 200, 250):
        tre, con = [], []
        for r in ring:
            if not alive_at(r, R):
                continue
            f = int(r[key])
            (tre if 0 <= f <= R else con).append(r)

        def rate(rows):
            n = d = 0
            for r in rows:
                cd = int(r["core_dead_rnd"])
                if cd >= 0 and cd - R <= 250:
                    n += 1
                    d += 1
                elif int(r["rounds"]) > R + 250:
                    n += 1
            return d, n
        dt, nt = rate(tre)
        dc, nc = rate(con)
        if nt < 5:
            continue
        rt = (dt / nt) / (dc / nc) if nc and dc else float("nan")
        print(f"  {k:>2} {R:>5} | {nt:>9} {dt:>4} {pct(dt,nt):>7} | "
              f"{nc:>9} {dc:>4} {pct(dc,nc):>7} | {rt:>6.2f}")
    print()

# =========================================================================== #
hdr("(3) PER-ROUND HAZARD — P(core dies within H | hostile ring = j RIGHT NOW)")
haz = rd(f"{OUT}/ars_haz.tsv")
acc = defaultdict(lambda: defaultdict(int))
accb = defaultdict(lambda: defaultdict(int))
for r in haz:
    if r["file"] not in J:
        continue
    early = r["band50"] not in ("r250-500", "r500+")
    for tgt, cond in ((acc, True), (accb, early)):
        if not cond:
            continue
        d = tgt[(r["metric"], int(r["j"]))]
        for c in ("n25", "d25", "n50", "d50", "n100", "d100"):
            d[c] += int(r[c])
for metric, lab in (("occ", "hostile ring tiles, ANY entity"),
                    ("bod", "hostile BODIES on the ring")):
    for tgt, when in ((acc, "all rounds"), (accb, "rounds < 250 only")):
        print(f"\n  {lab} — {when}")
        print(f"  {'j':>3} | {'exposed rnds':>12} {'P(die<=25)':>11} "
              f"{'95% CI':>16} | {'P(die<=50)':>11} | {'P(die<=100)':>12}")
        for j in range(0, 13):
            d = tgt.get((metric, j))
            if not d or d["n25"] < 200:
                continue
            lo, hi = wilson(d["d25"], d["n25"])
            print(f"  {j:>3} | {d['n25']:>12,} {pct(d['d25'],d['n25']):>11} "
                  f"[{lo:>5.2f},{hi:>5.2f}] | {pct(d['d50'],d['n50']):>11} | "
                  f"{pct(d['d100'],d['n100']):>12}")

# =========================================================================== #
hdr("(5) SPAWN RATE, PHASE-CONTROLLED (50-round bins)")
sp = rd(f"{OUT}/ars_spawn.tsv")
cells = defaultdict(lambda: [0, 0])
for r in sp:
    if r["file"] not in J or r["atcap"] == "1":
        continue
    b = r["band50"] if "band50" in r else r["band"]
    if b in ("r250-500", "r500+"):
        continue
    c = cells[(b, 12 - int(r["freesoft"]))]
    c[0] += int(r["rounds"])
    c[1] += int(r["spawns"])
bands = ["r0-50", "r50-100", "r100-150", "r150-200", "r200-250"]
print(f"  {'blocked':>7} | " + " | ".join(f"{b:>16}" for b in bands))
for blk in range(0, 13):
    row = []
    for b in bands:
        c = cells[(b, blk)]
        row.append(f"{c[0]:>7} {c[1]/c[0]:.4f}" if c[0] >= 300 else
                   (f"{c[0]:>7}      -" if c[0] else f"{'':>7}      -"))
    if any("." in x for x in row):
        print(f"  {blk:>7} | " + " | ".join(f"{x:>16}" for x in row))
