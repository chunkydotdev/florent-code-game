#!/usr/bin/env python3
"""v538 build instrument #5 -- THE THREE-CELL TABLE + PAIRED McNEMAR.

Reads a `run_battery.py` tape (`tag map seed seat arm ours winner cond turn
tracebacks ours_mined opp_mined`) and prints, per map and per arm:

    wins/n, share, timely-kill rate (our core-kill by r300 / ALL games),
    median kill round conditioned on a kill (DIAGNOSTIC -- carries the
    collider PROGRAMME.md names), games ending at r1000, tracebacks

...then the PAIRED McNemar between every arm pair on the shared
(map, seed, seat) cells.  Pairing is the point: all arms of a cell are run
adjacent by `run_battery.py`, so the contrast is within-cell and the correct
test is discordant-pair, not two independent proportions.

⛔ BOTH VERDICTS OR IT IS NOT AN INSTRUMENT (`--selftest`): the same
aggregators are driven on synthetic tapes where the answer is known and
DIFFERENT each time -- a perfect one-way flip, two identical arms, an
all-win arm, an all-loss arm, and a tape with a deliberate NOWINNER row.
A table that has only ever printed one shape has not been seen to compute.

  .venv/bin/python .../wintab.py <tape> [--selftest]
"""
import math
import sys
from pathlib import Path

KEY = ("map", "seed", "seat")
KILL_COND = "Core destroyed"
TIMELY_BY = 300


def load(path):
    lines = Path(path).read_text().splitlines()
    head = lines[0].split("\t")
    return [dict(zip(head, l.split("\t"))) for l in lines[1:] if l.strip()]


def median(xs):
    xs = sorted(xs)
    if not xs:
        return None
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


def cell(rows):
    """Aggregate one (map, arm) bucket."""
    n = len(rows)
    wins = sum(1 for r in rows if r["ours"] == "US")
    kills = [int(r["turn"]) for r in rows
             if r["ours"] == "US" and r["cond"] == KILL_COND]
    timely = sum(1 for t in kills if t <= TIMELY_BY)
    r1000 = sum(1 for r in rows if int(r["turn"]) >= 1000)
    tb = sum(int(r["tracebacks"]) for r in rows)
    return dict(n=n, wins=wins, share=(100.0 * wins / n if n else 0.0),
                timely=timely,
                timely_rate=(100.0 * timely / n if n else 0.0),
                medkill=median(kills), r1000=r1000, tb=tb)


def mcnemar(rows, a, b):
    """(n_shared, a_only, b_only, z) on the paired cells."""
    ia = {tuple(r[k] for k in KEY): r for r in rows if r["arm"] == a}
    ib = {tuple(r[k] for k in KEY): r for r in rows if r["arm"] == b}
    shared = sorted(set(ia) & set(ib))
    ao = bo = 0
    for k in shared:
        wa, wb = ia[k]["ours"] == "US", ib[k]["ours"] == "US"
        if wa and not wb:
            ao += 1
        elif wb and not wa:
            bo += 1
    d = ao + bo
    z = (ao - bo) / math.sqrt(d) if d else 0.0
    return len(shared), ao, bo, z


def table(rows, maps=None, arms=None):
    maps = maps or sorted({r["map"] for r in rows})
    arms = arms or sorted({r["arm"] for r in rows})
    print("%-14s %-14s %5s %6s %8s %8s %8s %6s %4s"
          % ("map", "arm", "n", "wins", "share%", "timely%", "medkill",
             "r1000", "tb"))
    for mp in maps + ["POOL"]:
        for arm in arms:
            rs = [r for r in rows if r["arm"] == arm
                  and (mp == "POOL" or r["map"] == mp)]
            if not rs:
                continue
            c = cell(rs)
            print("%-14s %-14s %5d %6d %8.2f %8.2f %8s %6d %4d"
                  % (mp, arm, c["n"], c["wins"], c["share"], c["timely_rate"],
                     c["medkill"] if c["medkill"] is not None else "-",
                     c["r1000"], c["tb"]))
        print("")


def pairs(rows, maps=None, arms=None):
    maps = maps or sorted({r["map"] for r in rows})
    arms = arms or sorted({r["arm"] for r in rows})
    print("%-14s %-14s %-14s %6s %6s %6s %8s %8s"
          % ("map", "arm A", "arm B", "cells", "A-only", "B-only", "z",
             "delta pp"))
    for mp in maps + ["POOL"]:
        rs = [r for r in rows if mp == "POOL" or r["map"] == mp]
        for i in range(len(arms)):
            for j in range(i + 1, len(arms)):
                n, ao, bo, z = mcnemar(rs, arms[i], arms[j])
                if not n:
                    continue
                print("%-14s %-14s %-14s %6d %6d %6d %8.2f %8.2f"
                      % (mp, arms[i], arms[j], n, ao, bo, z,
                         100.0 * (ao - bo) / n))
        print("")


def _row(mp, seed, seat, arm, ours, cond="Core destroyed", turn=200, tb=0):
    return dict(tag="t", map=mp, seed=str(seed), seat=seat, arm=arm,
                ours=ours, winner="w", cond=cond, turn=str(turn),
                tracebacks=str(tb), ours_mined="0", opp_mined="0")


def selftest():
    ok = True

    def check(label, got, want):
        nonlocal ok
        if got != want:
            ok = False
            print("[FAIL] %s: got %r want %r" % (label, got, want))
        else:
            print("[ok] %s: %r" % (label, got))

    # 1. a PERFECT one-way flip: arm X wins every cell arm Y loses
    rows = []
    for s in range(10):
        rows.append(_row("m", s, "A", "X", "US"))
        rows.append(_row("m", s, "A", "Y", "OPP"))
    n, ao, bo, z = mcnemar(rows, "X", "Y")
    check("perfect flip: 10 cells, all one way", (n, ao, bo), (10, 10, 0))
    check("perfect flip z", round(z, 2), 3.16)

    # 2. two IDENTICAL arms -> 0 discordant, z = 0 (the other verdict)
    rows2 = []
    for s in range(10):
        for arm in ("X", "Y"):
            rows2.append(_row("m", s, "A", arm, "US" if s % 2 else "OPP"))
    n, ao, bo, z = mcnemar(rows2, "X", "Y")
    check("identical arms: no discordant cells", (n, ao, bo, z),
          (10, 0, 0, 0.0))

    # 3. an all-win arm and an all-loss arm read 100% / 0%
    c = cell([_row("m", s, "A", "X", "US") for s in range(7)])
    check("all-win arm share", (c["n"], c["wins"], c["share"]), (7, 7, 100.0))
    c = cell([_row("m", s, "A", "X", "OPP") for s in range(7)])
    check("all-loss arm share", (c["wins"], c["share"]), (0, 0.0))

    # 4. the TIMELY-KILL primary counts kills by r300 over ALL games, and a
    #    late kill must NOT count -- driven both ways on the same bucket.
    c = cell([_row("m", 1, "A", "X", "US", turn=299),
              _row("m", 2, "A", "X", "US", turn=301),
              _row("m", 3, "A", "X", "OPP", turn=50),
              _row("m", 4, "A", "X", "US", turn=1000, cond="titanium_collected")])
    check("timely counts only the <=r300 core-kill", c["timely"], 1)
    check("timely rate is over ALL games, not over wins",
          round(c["timely_rate"], 2), 25.0)
    check("a r1000 tiebreak win is a WIN but not a KILL",
          (c["wins"], c["medkill"]), (3, 300))
    check("r1000 games counted", c["r1000"], 1)

    # 5. a NOWINNER row is neither a win nor a kill
    c = cell([_row("m", 1, "A", "X", "NONE", cond="-", turn=1000)])
    check("NOWINNER row: 0 wins, 0 timely", (c["wins"], c["timely"]), (0, 0))

    print("WINTAB SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        raise SystemExit(selftest())
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    rows = load(args[0])
    print("tape %s -- %d rows" % (args[0], len(rows)))
    print("== PER MAP, PER ARM ==")
    table(rows)
    print("== PAIRED McNEMAR ==")
    pairs(rows)
