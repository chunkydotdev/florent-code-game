#!/usr/bin/env python3
"""HEAL-BACK MOVEMENT + the income proxy, per arm (and per map), off crip.tsv.

heal_back = healing landed on the ENEMY core / damage landed on it (the rush
autopsy's ledger method; it measured EXACTLY 100.0% in 11 of 12 failed sieges).
Reported on the games where we actually landed damage -- a game with 0 damage
has no defined ratio and pooling it as 0 would read as "they healed nothing".
"""
import statistics as st
import sys
from collections import defaultdict

ARMS = sys.argv[1:]


def load(p):
    rows = []
    with open(p) as fh:
        hdr = fh.readline().rstrip("\n").split("\t")
        for ln in fh:
            f = ln.rstrip("\n").split("\t")
            if len(f) != len(hdr):
                continue
            rows.append(dict(zip(hdr, f)))
    return rows


def num(r, k, d=None):
    v = r.get(k, "")
    if v == "":
        return d
    try:
        return float(v)
    except ValueError:
        return d


print("%-10s %5s %8s %8s %9s %9s %8s %8s %8s %8s" % (
    "arm", "n", "healbk", "hb>=0.9", "oppdmg", "theirharv", "theirbelt",
    "ecokill", "fwdgun", "fwdgun_r"))
per = {}
for a in ARMS:
    rows = load("scratchpad/s51_v519_build/crip_%s.tsv" % a)
    hb = [num(r, "heal_back") for r in rows if num(r, "heal_back") is not None]
    dmg = [num(r, "oppcore_dmg", 0) for r in rows]
    hv = [num(r, "opp_harv_built", 0) for r in rows]
    bl = [num(r, "opp_belt_built", 0) for r in rows]
    ek = [num(r, "opp_eco_killed", 0) for r in rows]
    fg = [num(r, "fwd_gun_n", 0) for r in rows]
    fgr = [num(r, "fwd_gun_first") for r in rows
           if num(r, "fwd_gun_first") is not None]
    per[a] = rows
    print("%-10s %5d %8.3f %7.1f%% %9.0f %9.2f %8.2f %8.2f %8.2f %8s" % (
        a, len(rows), st.median(hb) if hb else -1,
        100.0 * sum(1 for x in hb if x >= 0.9) / max(1, len(hb)),
        st.median(dmg), st.mean(hv), st.mean(bl), st.mean(ek), st.mean(fg),
        ("%.0f" % st.median(fgr)) if fgr else "-"))
print()
print("MEDIAN heal_back PER MAP (games with damage landed)")
maps = sorted({r["map"] for r in per[ARMS[0]]})
print("%-14s %s" % ("map", "  ".join("%-16s" % a for a in ARMS)))
for m in maps:
    cells = []
    for a in ARMS:
        hb = [num(r, "heal_back") for r in per[a]
              if r["map"] == m and num(r, "heal_back") is not None]
        cells.append("%6.3f (n=%2d)   " % (st.median(hb) if hb else -1, len(hb)))
    print("%-14s %s" % (m, "  ".join(cells)))
print()
print("MODESWITCH BEHAVIOURAL SIGNATURE (engine-side): our forward launchers")
print("(d^2<=100 of THEIR core) and our collar barriers (d^2<=8) per game")
print("%-14s %s" % ("map", "  ".join("%-22s" % a for a in ARMS)))
for m in maps:
    cells = []
    for a in ARMS:
        rr = [r for r in per[a] if r["map"] == m]
        fl = st.mean([num(r, "fwd_laun_n", 0) for r in rr]) if rr else -1
        cb = st.mean([num(r, "collar_bar_n", 0) for r in rr]) if rr else -1
        cells.append("laun %5.2f bar %5.2f  " % (fl, cb))
    print("%-14s %s" % (m, "  ".join(cells)))
