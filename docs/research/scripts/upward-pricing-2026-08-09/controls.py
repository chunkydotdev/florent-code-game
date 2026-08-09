#!/usr/bin/env python3
"""Two controls the headline tables need.

CONTROL A -- collar occupancy is measured over ROUNDS LIVED, and top-tier games
are shorter.  Recompute occupancy inside a FIXED window (r0-250, and r0-150) so
every surviving side-game contributes the same exposure.

CONTROL B -- "team X is killed in 46% of its third-party games" is a statement
about X's OPPONENTS as much as about X.  For every candidate, report the mean
at-match rating of the killers, and the kill rate restricted to killers rated
BELOW a given threshold -- i.e. "does anyone near OUR strength ever kill this
core?"  That is the only version of the question that prices an upward leg.

    python controls.py <freezedir>
"""
from __future__ import annotations
import csv, statistics, sys
from collections import defaultdict

SEAT = {"US": "A", "THEM": "B"}


def f(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def main(argv):
    fz = argv[0]
    M = {r["file"]: r for r in csv.DictReader(open(f"{fz}/meta_join.tsv"), delimiter="\t")}
    rat = defaultdict(list)
    for m in M.values():
        for s in "AB":
            v = f(m[f"rating{s}Before"])
            if v is not None:
                rat[m[f"team{s}Name"]].append(v)
    med_of = {n: statistics.median(v) for n, v in rat.items() if v}

    # ---------- CONTROL A ----------
    win = defaultdict(lambda: defaultdict(float))
    for r in csv.DictReader(open(f"{fz}/collar/collar_rounds.tsv"), delimiter="\t"):
        m = M.get(r["file"])
        if not m or m["related"] != "none":
            continue
        tp = m["us_side"] == "none"
        nm = m[f"team{SEAT[r['side']]}Name"]
        rnd = int(r["rnd"])
        occ = 1 if int(r["orth_seats0"]) >= 1 else 0
        for lab, hi in (("r0-150", 150), ("r0-250", 250)):
            if rnd < hi:
                a = win[(nm, tp, lab)]
                a["n"] += 1
                a["occ"] += occ
                a["heal_core"] += int(r["heal_core_ev"])
    print("CONTROL A -- collar occupancy inside a FIXED window (exposure-matched)")
    print(f"{'team':30s} {'medRat':>7s} {'pop':>5s} {'r0-150 occ':>11s} {'r0-250 occ':>11s} "
          f"{'r0-250 rounds':>13s} {'chl/100r r0-250':>16s}")
    names = sorted({k[0] for k in win}, key=lambda n: -med_of.get(n, 0))
    for nm in names:
        for tp in (True, False):
            a2 = win.get((nm, tp, "r0-250"))
            a1 = win.get((nm, tp, "r0-150"))
            if not a2 or a2["n"] < 8000:
                continue
            if med_of.get(nm, 0) < 1550 and nm != "OpenSverige":
                continue
            print(f"{nm[:30]:30s} {med_of.get(nm,0):7.0f} {'tp' if tp else 'vsus':>5s} "
                  f"{100*a1['occ']/a1['n']:10.2f}% {100*a2['occ']/a2['n']:10.2f}% "
                  f"{a2['n']:13.0f} {100*a2['heal_core']/a2['n']:16.2f}")

    # ---------- CONTROL B ----------
    K = list(csv.DictReader(open(f"{fz}/killmix.tsv"), delimiter="\t"))
    prof = defaultdict(lambda: defaultdict(list))
    for r in K:
        m = M.get(r["file"])
        if not m or m["us_side"] != "none" or m["related"] != "none":
            continue
        vside = "US" if r["victim_idx"] == "0" else "THEM"
        kside = "THEM" if vside == "US" else "US"
        vn = m[f"team{SEAT[vside]}Name"]
        kr = f(m[f"rating{SEAT[kside]}Before"])
        if kr is None:
            continue
        d = int(r["death_rnd"])
        prof[vn]["kr"].append(kr)
        prof[vn]["dead"].append(d)
    print("\nCONTROL B -- who actually kills this core, and does anyone our size do it?")
    print(f"{'team':30s} {'medRat':>7s} {'sideG':>6s} {'meanKillerRat':>13s} "
          f"| {'killers<1700':>12s} {'killed%':>8s} {'<=r250%':>8s} "
          f"| {'killers<1650':>12s} {'killed%':>8s} {'<=r250%':>8s}")
    for nm in sorted(prof, key=lambda n: -med_of.get(n, 0)):
        if med_of.get(nm, 0) < 1600:
            continue
        p = prof[nm]
        if len(p["dead"]) < 60:
            continue
        rows = list(zip(p["kr"], p["dead"]))
        out = [f"{nm[:30]:30s} {med_of[nm]:7.0f} {len(rows):6d} "
               f"{statistics.mean(p['kr']):13.0f}"]
        for thr in (1700, 1650):
            sub = [d for kr, d in rows if kr < thr]
            if len(sub) < 10:
                out.append(f" | {len(sub):12d} {'--':>8s} {'--':>8s}")
                continue
            kd = [d for d in sub if d >= 0]
            fast = [d for d in kd if d <= 250]
            out.append(f" | {len(sub):12d} {100*len(kd)/len(sub):7.1f}% "
                       f"{100*len(fast)/len(sub):7.1f}%")
        print("".join(out))


if __name__ == "__main__":
    main(sys.argv[1:])
