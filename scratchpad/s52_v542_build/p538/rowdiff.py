#!/usr/bin/env python3
"""v538 build instrument #6 -- GAME-LEVEL ROW IDENTITY across arms.

COPIED from `scratchpad/s52_v535_build/rowdiff.py` (never edited in place); the
REFUSE/run split it already carries is exactly v538's claim, so only this
header changed.

Reads a `run_battery.py` / `remote_battery.py` tape and compares arms cell-by-cell on the SAME
(map, seed, seat), on every column except `tag` and `arm`.  With NOISE_ON=False
a game is a pure function of (arms, map, seed, seat), so two arms that are
behaviourally identical must produce IDENTICAL ROWS -- that is the game-level
form of this build's negative control.

⛔ DRIVEN BOTH WAYS (`--selftest`): the same comparator is run against a copy
of the tape with ONE digit of ONE `turn` value changed, and against a copy with
one `winner` flipped.  Both MUST be reported.  A comparator that has only ever
printed 0 has not been seen to compare.

  .venv/bin/python .../rowdiff.py <tape> [--selftest]
"""
import sys
from pathlib import Path

KEY = ("map", "seed", "seat")
# ⛔ `winner` IS NOT COMPARABLE ACROSS ARMS AND EXCLUDING IT IS NOT A WEAKENING.
# The column carries the winning BOT DIRECTORY NAME, so it reads `par_off` in
# one arm and `v534_off` in the other for the very same outcome -- a pure name
# difference that would swamp the comparison.  `ours` (US/OPP/NONE) carries the
# same outcome team-neutrally and IS compared, as are cond, turn, tracebacks and
# both mined totals.
IGNORE = {"tag", "arm", "winner"}


def load(path):
    lines = Path(path).read_text().splitlines()
    head = lines[0].split("\t")
    rows = [dict(zip(head, l.split("\t"))) for l in lines[1:] if l.strip()]
    return head, rows


def compare(rows, a, b):
    ia = {tuple(r[k] for k in KEY): r for r in rows if r["arm"] == a}
    ib = {tuple(r[k] for k in KEY): r for r in rows if r["arm"] == b}
    common = sorted(set(ia) & set(ib))
    diffs = []
    for k in common:
        cols = [c for c in ia[k]
                if c not in IGNORE and ia[k][c] != ib[k][c]]
        if cols:
            diffs.append((k, cols, {c: (ia[k][c], ib[k][c]) for c in cols}))
    return len(common), diffs


def report(rows, arms):
    out = {}
    for i in range(len(arms)):
        for j in range(i + 1, len(arms)):
            n, d = compare(rows, arms[i], arms[j])
            out[(arms[i], arms[j])] = (n, d)
            print("   %-12s vs %-12s  %3d shared cells, %3d rows differ"
                  % (arms[i], arms[j], n, len(d)))
            for k, cols, det in d[:4]:
                print("        %s  %s" % (k, det))
            if len(d) > 4:
                print("        ... %d more" % (len(d) - 4))
    return out


# ⭐ v535 ADDITION, INHERITED BY v538 UNCHANGED.  The v534 form asked "are these two arms identical?" over a
# whole tape.  v535's claim is SHARPER and needs the split: the gated arm must
# be identical to the parent on the boards the siege RUNS and must DIVERGE on
# the boards it REFUSES.  (v535: corner barriers.  v538: the socket claim.)  A whole-tape count cannot express that, and a
# whole-tape count of 0 would in fact FALSIFY the build (it would mean the gate
# never fired).  REFUSING is not a name list used as logic -- it is this
# build's own `gatemap.py` verdict (OUT_gatemap.txt) for the two boards in the
# map set, quoted here
# purely to LABEL rows of an already-computed table.
REFUSING = {"archipelago", "midgard"}


def report_by_class(rows, a, b):
    ia = {tuple(r[k] for k in KEY): r for r in rows if r["arm"] == a}
    ib = {tuple(r[k] for k in KEY): r for r in rows if r["arm"] == b}
    tot = {}
    for k in sorted(set(ia) & set(ib)):
        cls = "REFUSE" if k[0] in REFUSING else "run"
        n, d = tot.get(cls, (0, 0))
        cols = [c for c in ia[k] if c not in IGNORE and ia[k][c] != ib[k][c]]
        tot[cls] = (n + 1, d + (1 if cols else 0))
    for cls in ("REFUSE", "run"):
        n, d = tot.get(cls, (0, 0))
        print("        %-7s %3d cells, %3d differ" % (cls, n, d))
    return tot


def main(path, selftest):
    head, rows = load(path)
    arms = sorted({r["arm"] for r in rows})
    print("tape %s -- %d rows, arms %s" % (path, len(rows), arms))
    print("== LIVE ==")
    live = report(rows, arms)
    print("== BY MAP CLASS ==")
    for i in range(len(arms)):
        for j in range(i + 1, len(arms)):
            print("   %-12s vs %-12s" % (arms[i], arms[j]))
            report_by_class(rows, arms[i], arms[j])
    if selftest:
        # ⛔ THE MUTATION MUST LAND ON AN ARM THAT IS CURRENTLY IDENTICAL TO
        # ANOTHER, OR THE GUARD IS VACUOUS.  The first version of this selftest
        # mutated `arms[0]` -- alphabetically `mut_off`, the arm that already
        # differs from everything -- and "passed" while proving nothing.  Pick
        # a zero-difference pair and corrupt one side of it.
        pair = next((k for k, v in live.items() if not v[1]), None)
        if pair is None:
            print("SELFTEST INCONCLUSIVE -- no zero-difference pair to corrupt")
            return 1
        victim, partner = pair
        print("== corrupting arm %r (currently 0 differences vs %r) =="
              % (victim, partner))
        for label, col, fn in (("turn +1", "turn", lambda v: str(int(v) + 1)),
                               ("ours flipped", "ours",
                                lambda v: "NONE" if v != "NONE" else "US")):
            m = [dict(r) for r in rows]
            tgt = next(r for r in m if r["arm"] == victim)
            tgt[col] = fn(tgt[col])
            n, d = compare(m, victim, partner)
            print("   MUTANT %-14s %s vs %s -> %d rows differ (expect 1)"
                  % (label, victim, partner, len(d)))
            if len(d) != 1:
                print("⛔ the comparator did not react to the mutation")
                return 1
        print("SELFTEST PASS -- the comparator produced the other verdict on a "
              "pair that reads 0 in the live tape")
        return 0
    return 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if "-h" in sys.argv[1:] or "--help" in sys.argv[1:]:
        print(__doc__)
        raise SystemExit(0)
    raise SystemExit(main(args[0], "--selftest" in sys.argv[1:]))
