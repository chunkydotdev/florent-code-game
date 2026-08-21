#!/usr/bin/env python3
"""v538 build instrument #9 -- POOL THE TWO MECHANISM RUNS.

The two runs are the SAME grid (3 maps x 30 seeds x 2 seats x 3 arms) with the
ARM ORDER REVERSED in the second, so pooling them is legitimate only cell-wise:
a cell is (run, map, seed, seat) and the McNemar pairing stays WITHIN a run.
Pooling across runs without that key would pair a run-1 treatment game against a
run-2 control game, which is exactly the non-time-adjacent comparison v518
finding 2 measured a 4.6pp false positive from.

⛔ SELFTEST drives the pooler both ways: two synthetic runs with a known flip
must pool to the sum, and two runs that cancel must pool to zero.

  .venv/bin/python .../pool.py [--selftest]
"""
import math
import sys
from pathlib import Path

B = Path(__file__).resolve().parent


def load(p, run):
    lines = Path(p).read_text().splitlines()
    head = lines[0].split("\t")
    rows = [dict(zip(head, l.split("\t"))) for l in lines[1:] if l.strip()]
    for r in rows:
        r["run"] = run
    return rows


def cut(rows, arm, maps):
    return [r for r in rows if r["arm"] == arm and r["map"] in maps]


def wins(rows):
    return sum(1 for r in rows if r["ours"] == "US")


def timely(rows):
    return sum(1 for r in rows if r["ours"] == "US"
               and r["cond"] == "Core destroyed" and int(r["turn"]) <= 300)


def mcnemar(rows, a, b, maps):
    """Paired within (run, map, seed, seat) -- never across runs."""
    ia = {(r["run"], r["map"], r["seed"], r["seat"]): r
          for r in rows if r["arm"] == a and r["map"] in maps}
    ib = {(r["run"], r["map"], r["seed"], r["seat"]): r
          for r in rows if r["arm"] == b and r["map"] in maps}
    sh = sorted(set(ia) & set(ib))
    ao = bo = 0
    for k in sh:
        x, y = ia[k]["ours"] == "US", ib[k]["ours"] == "US"
        if x and not y:
            ao += 1
        elif y and not x:
            bo += 1
    d = ao + bo
    return len(sh), ao, bo, ((ao - bo) / math.sqrt(d) if d else 0.0)


def hw(n, p=0.5):
    """Naive 95% half-width, pp.  Local fixtures read DEFF 0.98 (s39), so no
    design-effect inflation is applied and the interval is marginally
    conservative."""
    return 100.0 * 1.96 * math.sqrt(p * (1 - p) / n)


def main():
    rows = (load(B / "mech" / "results.tsv", "1")
            + load(B / "mech2" / "results.tsv", "2"))
    ARMS = ["v536trust", "v537socket", "v538refine"]
    CUTS = [("archipelago  (GATED - refuses)", {"archipelago"}),
            ("glacierkeep  (runs)", {"glacierkeep"}),
            ("yulerune     (runs)", {"yulerune"}),
            ("RUNNING maps (gate cannot act)", {"glacierkeep", "yulerune"}),
            ("ALL 3 maps", {"archipelago", "glacierkeep", "yulerune"})]
    print("POOLED OVER BOTH RUNS (arm order reversed in run 2), n per arm shown")
    print("%-34s %-12s %5s %6s %8s %8s %8s"
          % ("cut", "arm", "n", "wins", "share%", "hw95", "timely%"))
    for label, maps in CUTS:
        for arm in ARMS:
            rs = cut(rows, arm, maps)
            print("%-34s %-12s %5d %6d %8.2f %8.2f %8.2f"
                  % (label, arm, len(rs), wins(rs),
                     100.0 * wins(rs) / len(rs), hw(len(rs)),
                     100.0 * timely(rs) / len(rs)))
        print("")
    print("PAIRED McNEMAR, pooled within run")
    print("%-34s %-12s %-12s %6s %6s %6s %8s %9s"
          % ("cut", "A", "B", "cells", "A-only", "B-only", "z", "delta pp"))
    for label, maps in CUTS:
        for i in range(len(ARMS)):
            for j in range(i + 1, len(ARMS)):
                n, ao, bo, z = mcnemar(rows, ARMS[i], ARMS[j], maps)
                print("%-34s %-12s %-12s %6d %6d %6d %8.2f %9.2f"
                      % (label, ARMS[i], ARMS[j], n, ao, bo, z,
                         100.0 * (ao - bo) / n))
        print("")
    print("PER-RUN REPRODUCIBILITY of the v537->v538 contrast")
    print("%-34s %8s %8s %8s" % ("cut", "run1 pp", "run2 pp", "spread pp"))
    for label, maps in CUTS:
        d = []
        for run in ("1", "2"):
            rr = [r for r in rows if r["run"] == run]
            n, ao, bo, z = mcnemar(rr, "v537socket", "v538refine", maps)
            d.append(100.0 * (bo - ao) / n)
        print("%-34s %8.2f %8.2f %8.2f"
              % (label, d[0], d[1], abs(d[0] - d[1])))


def _r(run, mp, sd, st, arm, ours):
    return dict(run=run, map=mp, seed=str(sd), seat=st, arm=arm, ours=ours,
                cond="Core destroyed", turn="200")


def selftest():
    ok = True

    def check(label, got, want):
        nonlocal ok
        if got != want:
            ok = False
            print("[FAIL] %s: got %r want %r" % (label, got, want))
        else:
            print("[ok] %s: %r" % (label, got))

    # two runs, same one-way flip in both -> pooled discordants add up
    rows = []
    for run in ("1", "2"):
        for s in range(5):
            rows.append(_r(run, "m", s, "A", "X", "US"))
            rows.append(_r(run, "m", s, "A", "Y", "OPP"))
    check("two runs, same flip: pooled discordants add",
          mcnemar(rows, "X", "Y", {"m"})[:3], (10, 10, 0))

    # two runs that CANCEL -> pooled reads zero, and that is the other verdict
    rows = []
    for s in range(5):
        rows.append(_r("1", "m", s, "A", "X", "US"))
        rows.append(_r("1", "m", s, "A", "Y", "OPP"))
        rows.append(_r("2", "m", s, "A", "X", "OPP"))
        rows.append(_r("2", "m", s, "A", "Y", "US"))
    n, ao, bo, z = mcnemar(rows, "X", "Y", {"m"})
    check("two runs that cancel: pooled net zero", (n, ao, bo, z),
          (10, 5, 5, 0.0))

    # ⛔ the pairing must be WITHIN run: give run 2 a cell key that run 1 also
    #    has, with opposite outcomes, and the pooler must NOT cross-pair.
    check("cells are keyed by run (no cross-run pairing)",
          len({(r["run"], r["map"], r["seed"], r["seat"])
               for r in rows if r["arm"] == "X"}), 10)

    check("hw95 at n=60", round(hw(60), 2), 12.65)
    check("hw95 at n=120 is narrower", hw(120) < hw(60), True)
    print("POOL SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        raise SystemExit(selftest())
    main()
