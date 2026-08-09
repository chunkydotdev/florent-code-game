#!/usr/bin/env python3
"""Does builder melee REACH a top-tier core at all?

Q2 asks whether the quiet-melee kill line meets a stronger version of the same
defence or a different one.  The share-of-damage number alone cannot tell those
apart: melee could be a small share because it is stopped, or because nobody
tries it.  So: per victim rating band, how many side-games see ANY enemy
builderAttack land on the core footprint, and at what rate per 100 rounds.

Also reports version currency for the Q3 candidates -- which of a team's
versions the archive actually covers, so a stale profile is visible.

    python melee_reach.py <freezedir>
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
    K = list(csv.DictReader(open(f"{fz}/killmix.tsv"), delimiter="\t"))
    band_acc = defaultdict(lambda: defaultdict(float))
    for r in K:
        m = M.get(r["file"])
        if not m or m["related"] != "none":
            continue
        side = "US" if r["victim_idx"] == "0" else "THEM"
        vr = f(m[f"rating{SEAT[side]}Before"])
        if vr is None:
            continue
        tp = m["us_side"] == "none"
        if tp:
            b = ("<1550" if vr < 1550 else "1550-1699" if vr < 1700 else
                 "1700-1799" if vr < 1800 else "1800-1899" if vr < 1900 else ">=1900")
        else:
            b = "OUR CORE" if m[f"team{SEAT[side]}Name"] == "OpenSverige" else "FIELD CORE (vs us)"
        a = band_acc[b]
        a["sg"] += 1
        a["rounds"] += int(r["nr"])
        a["batk"] += int(r["batk"])
        a["gun"] += int(r["sh_gunner"])
        a["sen"] += int(r["sh_sentinel"])
        if int(r["batk"]) > 0:
            a["any_batk"] += 1
        if int(r["batk"]) >= 20:
            a["heavy_batk"] += 1
    print("MELEE REACH -- enemy builderAttack landing on the core footprint")
    print(f"{'victim band':22s} {'side-games':>10s} {'any batk':>9s} {'>=20 batk':>10s} "
          f"{'batk/100r':>10s} {'gunshots/100r':>14s} {'senshots/100r':>14s}")
    for b in ("<1550", "1550-1699", "1700-1799", "1800-1899", ">=1900",
              "OUR CORE", "FIELD CORE (vs us)"):
        a = band_acc.get(b)
        if not a:
            continue
        print(f"{b:22s} {a['sg']:10.0f} {100*a['any_batk']/a['sg']:8.1f}% "
              f"{100*a['heavy_batk']/a['sg']:9.1f}% {100*a['batk']/a['rounds']:10.3f} "
              f"{100*a['gun']/a['rounds']:14.3f} {100*a['sen']/a['rounds']:14.3f}")

    print("\nVERSION CURRENCY -- versions of each candidate the archive covers")
    ver = defaultdict(lambda: defaultdict(int))
    for m in M.values():
        for s in "AB":
            ver[m[f"team{s}Name"]][m[f"team{s}Version"]] += 1
    for nm in ("Powered by SmartFridge", "Landers", "Coreflood", "farming_200s",
               "Besvikomat", "kladde chatte tville (och oss)", "0033", "team lazy",
               "Big O", "O(1)", "HTTP 418", "Focalground", "arsonist duck",
               "sporks", "Pantheon", "Pivot", "Jython", "OpenSverige"):
        d = ver.get(nm)
        if not d:
            continue
        items = sorted(((int(k) if k.isdigit() else -1), v) for k, v in d.items())
        top = ", ".join(f"v{k}:{v}" for k, v in items[-5:])
        print(f"{nm[:32]:32s} {len(d):3d} versions, newest in archive: {top}")


if __name__ == "__main__":
    main(sys.argv[1:])
