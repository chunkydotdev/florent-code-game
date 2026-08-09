#!/usr/bin/env python3
"""Is the top tier's empty collar a CHOICE or an absence of bots?

Low collar occupancy has two readings: they decline to garrison, or they have no
builder bots to garrison with.  `live0` (builders alive at start of round) from
the shipped collar decoder separates them, and the conditional occupancy
(occupancy among rounds with >=1 live bot, and seats-per-live-bot) prices the
choice directly.

    python bots_and_collar.py <freezedir>
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
    acc = defaultdict(lambda: defaultdict(float))
    for r in csv.DictReader(open(f"{fz}/collar/collar_rounds.tsv"), delimiter="\t"):
        m = M.get(r["file"])
        if not m or m["related"] != "none":
            continue
        side = r["side"]
        rr = f(m[f"rating{SEAT[side]}Before"])
        if rr is None:
            continue
        tp = m["us_side"] == "none"
        if tp:
            b = ("<1550" if rr < 1550 else "1550-1699" if rr < 1700 else
                 "1700-1799" if rr < 1800 else "1800-1899" if rr < 1900 else ">=1900")
        else:
            b = "OpenSverige" if m[f"team{SEAT[side]}Name"] == "OpenSverige" else "field (vs us)"
        a = acc[b]
        a["n"] += 1
        live = int(r["live0"])
        a["live"] += live
        occ = 1 if int(r["orth_seats0"]) >= 1 else 0
        a["occ"] += occ
        a["seats"] += int(r["orth_seats0"])
        if live > 0:
            a["nlive"] += 1
            a["occ_live"] += occ
            a["seats_live"] += int(r["orth_seats0"])
        a["free"] += int(r["free_orth"])
    print(f"{'band':22s} {'rounds':>10s} {'bots alive':>11s} {'collar occ':>11s} "
          f"{'occ|bots>0':>11s} {'seats':>7s} {'seats/bot':>10s} {'free seats':>11s}")
    for b in ("<1550", "1550-1699", "1700-1799", "1800-1899", ">=1900",
              "field (vs us)", "OpenSverige"):
        a = acc.get(b)
        if not a:
            continue
        print(f"{b:22s} {a['n']:10.0f} {a['live']/a['n']:11.2f} "
              f"{100*a['occ']/a['n']:10.2f}% {100*a['occ_live']/a['nlive']:10.2f}% "
              f"{a['seats']/a['n']:7.3f} {a['seats']/max(a['live'],1):10.4f} "
              f"{a['free']/a['n']:11.2f}")


if __name__ == "__main__":
    main(sys.argv[1:])
