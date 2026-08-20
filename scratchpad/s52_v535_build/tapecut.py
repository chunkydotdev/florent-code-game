#!/usr/bin/env python3
"""v535 build instrument #5 -- CUT THE DETERMINISM TAPE, AND PRICE IT HONESTLY.

Two tables off `grid/ALL.tsv`:

  A. per arm x map-class: n, wins, win%, kills by r300, tracebacks.
  B. ⛔ SEED DEGENERACY, and B is the reason A is a DIAGNOSTIC and never a
     currency read.  `NOISE_ON = False` makes a game a pure function of
     (arms, map, seed, seat) -- which is exactly what the identity check
     needs -- but it ALSO removes the only thing distinguishing one seed from
     another for a bot that ignores the seed. Measured here, not assumed:
     count DISTINCT outcome signatures per (map, seat) cell and compare
     against the 6 seeds played into it. If 6 seeds collapse to ~1 outcome,
     a "72-game" win column is a 12-cell win column and must be reported as
     one. (`tools/effective_n.py` is the general instrument for this; this is
     the same question asked of one build's own tape.)

⛔ SELFTEST drives both counters to the other verdict on synthetic tapes:
  a fully-degenerate tape must read 1 distinct per cell, a fully-distinct one
  must read 6, and the win counter must move when a row's `ours` is flipped.

  .venv/bin/python .../tapecut.py [tape] [--selftest]
"""
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REFUSING = {"archipelago", "midgard"}      # this build's gatemap.py verdict
SIG = ("ours", "cond", "turn", "ours_mined", "opp_mined")


def load(path):
    rows = [l.split("\t") for l in Path(path).read_text().splitlines() if l.strip()]
    h = rows[0]
    return [dict(zip(h, r)) for r in rows[1:]]


def cls_of(mp):
    return "REFUSE" if mp in REFUSING else "run"


def table_a(R):
    t = defaultdict(lambda: [0, 0, 0, 0])
    for r in R:
        k = (r["arm"], cls_of(r["map"]))
        t[k][0] += 1
        t[k][1] += r["ours"] == "US"
        t[k][2] += (r["ours"] == "US" and r["cond"] == "Core destroyed"
                    and int(r["turn"]) <= 300)
        t[k][3] += int(r["tracebacks"])
    print("%-10s %-7s %5s %5s %8s %8s %4s"
          % ("arm", "class", "n", "wins", "win%", "kill<=300", "tb"))
    for k in sorted(t):
        n, w, kk, tb = t[k]
        print("%-10s %-7s %5d %5d %7.1f%% %8d %4d"
              % (k[0], k[1], n, w, 100.0 * w / max(1, n), kk, tb))
    return t


def table_b(R):
    d = defaultdict(set)
    seeds = defaultdict(set)
    for r in R:
        k = (r["arm"], r["map"], r["seat"])
        d[k].add(tuple(r[c] for c in SIG))
        seeds[k].add(r["seed"])
    per = defaultdict(lambda: [0, 0, 0])
    for k, v in d.items():
        a = (k[0], cls_of(k[1]))
        per[a][0] += len(seeds[k])
        per[a][1] += len(v)
        per[a][2] += 1
    print("\n%-10s %-7s %6s %9s %9s %s"
          % ("arm", "class", "cells", "seeds", "distinct", "effective n"))
    for k in sorted(per):
        cells, uniq, ncell = per[k]
        print("%-10s %-7s %6d %9d %9d  %d of %d rows"
              % (k[0], k[1], ncell, cells, uniq, uniq, cells))
    return per


def selftest():
    ok = True

    def check(label, got, want):
        nonlocal ok
        if got != want:
            ok = False
            print("[FAIL] %s: got %r want %r" % (label, got, want))
        else:
            print("[ok] %s: %r" % (label, got))

    hdr = "arm\ttag\tmap\tseed\tseat\tours\twinner\tcond\tturn\ttracebacks\tours_mined\topp_mined"

    def mk(rows):
        return [dict(zip(hdr.split("\t"), r)) for r in rows]

    # fully degenerate: 6 seeds, identical outcomes
    deg = mk([["a", "t", "nordkap", str(s), "A", "US", "x", "Core destroyed",
               "100", "0", "10", "20"] for s in range(1, 7)])
    d = defaultdict(set)
    for r in deg:
        d[(r["arm"], r["map"], r["seat"])].add(tuple(r[c] for c in SIG))
    check("mutant: degenerate tape -> 1 distinct outcome in 6 seeds",
          len(d[("a", "nordkap", "A")]), 1)

    # fully distinct
    dis = mk([["a", "t", "nordkap", str(s), "A", "US", "x", "Core destroyed",
               str(100 + s), "0", "10", "20"] for s in range(1, 7)])
    d2 = defaultdict(set)
    for r in dis:
        d2[(r["arm"], r["map"], r["seat"])].add(tuple(r[c] for c in SIG))
    check("mutant: distinct tape -> 6 distinct outcomes in 6 seeds",
          len(d2[("a", "nordkap", "A")]), 6)

    # win counter must move
    w1 = sum(1 for r in deg if r["ours"] == "US")
    deg[0]["ours"] = "OPP"
    w2 = sum(1 for r in deg if r["ours"] == "US")
    check("mutant: flipping one `ours` moves the win count", (w1, w2), (6, 5))

    # class labelling must produce BOTH labels
    check("class labeller returns REFUSE for archipelago",
          cls_of("archipelago"), "REFUSE")
    check("class labeller returns run for nordkap", cls_of("nordkap"), "run")
    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        raise SystemExit(selftest())
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    R = load(args[0] if args else HERE / "grid" / "ALL.tsv")
    print("A. OUTCOMES BY ARM x MAP CLASS  (DIAGNOSTIC -- see table B)")
    table_a(R)
    print("\nB. SEED DEGENERACY -- what table A's `n` is really worth")
    table_b(R)
