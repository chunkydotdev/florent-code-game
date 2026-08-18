#!/usr/bin/env python3
"""v516 headline summariser: per-arm wins, k<=300, core deaths, r1000, median
kill round, per-map, per-block.

⛔ INTERVALS ARE NAIVE AND SAY SO.  These are LOCAL self-play-adjacent grid
games; the s39 audit measured local DEFF = 0.98 (pair-weighted, 124 shards), so
the platform constants do NOT apply and are not used.  What DOES apply is the
v515 one-draw law: the spawn salt is re-rolled per match from OS entropy, and
the measured same-config spread is +-3-5 games per 30-block and up to 9 per 90.

SELFTEST (`--selftest`): a synthetic table with a known answer must come out
right, and three mutations must move it.
"""
from __future__ import annotations

import csv
import math
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path


def load(paths):
    rows = []
    for p in paths:
        with open(p) as fh:
            for r in csv.DictReader(fh, delimiter="\t"):
                if r.get("tag"):
                    rows.append(r)
    return rows


def summ(rows):
    n = len(rows)
    if not n:
        return {}
    wins = sum(1 for r in rows if r["ours"] == "US")
    kills = [r for r in rows if r["ours"] == "US" and "Core" in r["cond"]]
    k300 = sum(1 for r in kills if int(r["turn"]) <= 300)
    dead = sum(1 for r in rows if r["ours"] == "OPP" and "Core" in r["cond"])
    r1000 = sum(1 for r in rows if int(r["turn"]) >= 1000)
    tb = sum(int(r["tracebacks"]) for r in rows)
    med = st.median(int(r["turn"]) for r in kills) if kills else -1
    return dict(n=n, wins=wins, winpct=100.0 * wins / n, kills=len(kills),
                k300=k300, k300pct=100.0 * k300 / n, coredead=dead,
                r1000=r1000, medkill=med, tracebacks=tb)


def hw(p, n):
    """Naive 95% half-width in percentage points (local DEFF = 0.98, unused)."""
    p = p / 100.0
    return 100.0 * 1.96 * math.sqrt(max(p * (1 - p), 1e-9) / n)


def selftest():
    ok = True
    mk = lambda o, c, t, tb=0: dict(  # noqa: E731
        tag="x", map="m", seed="1", seat="A", ours=o, winner="w", cond=c,
        turn=str(t), tracebacks=str(tb), ours_mined="0", opp_mined="0")
    rows = [mk("US", "Core destroyed", 100), mk("US", "Core destroyed", 400),
            mk("OPP", "Core destroyed", 200),
            mk("US", "Titanium collected (tiebreak)", 1000)]
    s = summ(rows)
    want = dict(n=4, wins=3, kills=2, k300=1, coredead=1, r1000=1, medkill=250)
    for k, v in want.items():
        if s[k] != v:
            print("SELFTEST FAIL %s: %s != %s" % (k, s[k], v)); ok = False
    # mutations that MUST move the answer
    m = summ([mk("US", "Core destroyed", 301)])
    if m["k300"] != 0:
        print("SELFTEST FAIL: r301 counted as k<=300"); ok = False
    m = summ([mk("US", "Titanium collected (tiebreak)", 200)])
    if m["kills"] != 0 or m["wins"] != 1:
        print("SELFTEST FAIL: tiebreak win counted as a kill"); ok = False
    m = summ([mk("OPP", "Core destroyed", 50)])
    if m["coredead"] != 1 or m["wins"] != 0:
        print("SELFTEST FAIL: our core death"); ok = False
    print("SELFTEST:", "PASS" if ok else "FAIL")
    return ok


def main():
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    if not selftest():
        sys.exit(1)
    base = Path(sys.argv[1] if len(sys.argv) > 1
                else "scratchpad/s51_v516_build/grid")
    arms = {"v516": sorted(base.glob("b*/v516.tsv")),
            "v515-parent": sorted(base.glob("b*/v515.tsv"))}
    got = {}
    for name, paths in arms.items():
        rows = load(paths)
        got[name] = rows
        s = summ(rows)
        if not s:
            continue
        print("%-12s n=%3d  WINS %3d (%.1f%% +-%.1f)  k<=300 %3d (%.1f%% "
              "+-%.1f)  ourcore_dead %3d  r1000 %3d  med_kill %s  tb %d"
              % (name, s["n"], s["wins"], s["winpct"], hw(s["winpct"], s["n"]),
                 s["k300"], s["k300pct"], hw(s["k300pct"], s["n"]),
                 s["coredead"], s["r1000"], s["medkill"], s["tracebacks"]))
    print()
    print("PER MAP (wins / n, k<=300):")
    maps = sorted({r["map"] for rs in got.values() for r in rs})
    for mp in maps:
        line = "  %-14s" % mp
        for name in arms:
            rs = [r for r in got[name] if r["map"] == mp]
            s = summ(rs)
            if s:
                line += "  %s %2d/%2d (k%2d)" % (name, s["wins"], s["n"],
                                                 s["k300"])
        print(line)
    print()
    print("PER BLOCK (wins/30):")
    for i in range(1, 40):
        d = base / ("b%d" % i)
        if not d.exists():
            continue
        line = "  b%-3d" % i
        for name, fn in (("v516", "v516.tsv"), ("v515-parent", "v515.tsv")):
            p = d / fn
            if p.exists():
                s = summ(load([p]))
                if s:
                    line += "  %s %2d/%2d" % (name, s["wins"], s["n"])
        print(line)


if __name__ == "__main__":
    main()
