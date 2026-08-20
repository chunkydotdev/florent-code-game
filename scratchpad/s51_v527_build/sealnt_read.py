#!/usr/bin/env python3
"""Fold the v527 SEALNT tape: [sealed & no-turret] ROUNDS, per arm.

THE CLAIM THIS TESTS.  Magnus's marker games hold a SEALED enemy core with NO
turret on it for hundreds of rounds.  The plank's promise is that such long
stretches cannot reproduce -- so the discriminating statistic is not the mean
(a few rounds of sealed-and-turretless are normal while a body walks to a site)
but the LONG-STRETCH tail: games with a run of >= THRESH consecutive such
rounds, and the longest run seen.

Also folds `hv` at r30 -- the v526 M6 lesson's falsifier for a plank that
spends BODIES (`FS_V527_PSURV_EXTRA`).

⛔ SELF-TESTED: `--selftest` folds three synthetic tapes (never-sealed,
sealed-and-converted, sealed-and-turretless-forever) and asserts the three
disagree.  A reader that has produced one verdict has not been seen to read.

Usage:
  sealnt_read.py <dir-of-.err> [<dir2> ...]
  sealnt_read.py --selftest
"""
import re
import sys
from pathlib import Path

PH_SEALED, PH_KILL_NEAR = 3, 6
THRESH = 50

LINE = re.compile(
    r"V527I SEALNT (\d+) ph (\d+) fwd (\d+) hv (\d+)")


def fold_text(txt):
    """-> (rounds_sealnt, longest_run, hv30, n_rounds)"""
    cur = best = tot = n = 0
    hv30 = None
    for m in LINE.finditer(txt):
        rnd, ph, fwd, hv = (int(m.group(i)) for i in (1, 2, 3, 4))
        n += 1
        if hv30 is None and rnd >= 30:
            hv30 = hv
        sealnt = (PH_SEALED <= ph <= PH_KILL_NEAR) and fwd == 0
        if sealnt:
            tot += 1
            cur += 1
            best = max(best, cur)
        else:
            cur = 0
    return tot, best, (hv30 if hv30 is not None else -1), n


def fold_dir(d):
    rows = []
    for f in sorted(Path(d).glob("*.err")):
        rows.append((f.name,) + fold_text(f.read_text()))
    return rows


def report(name, rows):
    if not rows:
        print("%-10s NO GAMES" % name)
        return
    g = len(rows)
    tot = sum(r[1] for r in rows)
    longest = [r[2] for r in rows]
    hv = [r[3] for r in rows if r[3] >= 0]
    over = sum(1 for x in longest if x >= THRESH)
    print("%-10s games %3d | sealnt rounds/game %7.1f | longest run: "
          "max %4d mean %6.1f | games with run>=%d: %2d (%4.1f%%) | "
          "hv30 mean %4.2f"
          % (name, g, tot / g, max(longest), sum(longest) / g, THRESH,
             over, 100.0 * over / g, (sum(hv) / len(hv)) if hv else -1))


def selftest():
    def tape(rows):
        return "\n".join(
            "V527I SEALNT %d ph %d fwd %d hv %d" % r for r in rows)
    never = tape([(i, 2, 0, 2) for i in range(200)])          # never sealed
    conv = tape([(i, 3, 0, 2) for i in range(10)]
                + [(i, 4, 1, 2) for i in range(10, 200)])     # converted fast
    stuck = tape([(i, 3, 0, 2) for i in range(200)])          # the marker game
    a, b, c = fold_text(never), fold_text(conv), fold_text(stuck)
    print("never-sealed        :", a)
    print("sealed-then-bought  :", b)
    print("sealed-turretless   :", c)
    ok = True
    if not (a[0] == 0 and a[1] == 0):
        print("SELFTEST FAIL: never-sealed must fold to 0/0"); ok = False
    if not (b[0] == 10 and b[1] == 10):
        print("SELFTEST FAIL: sealed-then-bought must fold to 10/10"); ok = False
    if not (c[0] == 200 and c[1] == 200):
        print("SELFTEST FAIL: sealed-turretless must fold to 200/200"); ok = False
    if len({a[1], b[1], c[1]}) != 3:
        print("SELFTEST FAIL: the three tapes did not disagree"); ok = False
    # a reader that ignores `fwd` would score `conv` == `stuck`
    if b[1] == c[1]:
        print("SELFTEST FAIL: reader is blind to the turret column"); ok = False
    print("SELFTEST:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    for d in sys.argv[1:]:
        report(Path(d).name, fold_dir(d))


if __name__ == "__main__":
    main()
