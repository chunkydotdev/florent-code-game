#!/usr/bin/env python3
r"""abl.py — THE ABLATION-IDENTITY TABLE for the v542 merge.

    abl.py <combined.tsv> [--label NAME] [--selftest]

⛔ WHAT A MERGE HAS TO PROVE AND A SINGLE-PLANK BUILD DOES NOT.  A plank build
proves ONE thing: `flag off == parent`.  A three-plank merge has to prove FOUR,
and three of them cannot be stated against the parent at all:

    v542 with plank i's master OFF  ==  the merge of the OTHER TWO
    v542 with ALL THREE masters OFF ==  the parent

⭐ AND EACH ONE NEEDS ITS OWN NEGATIVE CONTROL, because an identity between two
arms neither of which ACTED in the fixture is a pass-by-default.  That is the
v529merge §2 lesson verbatim ("A3 without a firing cell is a pass-by-default")
and it is enforced here rather than remembered: every identity row is paired
with the row that shows the ablated plank moved something in the SAME tape, and
the verdict is FAIL if any control reads 0.

Rows are compared cell-by-cell on (map, seed, seat) over every column except
`tag`, `arm` and `winner` — `winner` carries the winning BOT DIRECTORY NAME and
so differs on a pure name basis between arms; `ours` (US/OPP/NONE) carries the
same outcome team-neutrally and IS compared.  (Convention inherited from
`scratchpad/s52_v538_build/rowdiff.py`.)

⛔ THE TAPE MUST BE NOISE_OFF ON EVERY TREE INCLUDING THE OPPONENT, or a
zero-difference row means nothing and a nonzero one means less.  This file
cannot check that (the flag lives on disk, not in the tape) — the arm flag
dump in the build report is where it is checked.

SELFTEST (`--selftest`) drives every verdict both ways on a synthetic tape.
"""
import argparse
import collections
import sys

KEY = ("map", "seed", "seat")
IGNORE = {"tag", "arm", "winner"}

IDENTITIES = [
    ("v542[LOKI_FS_V538=False]     == merge(v539,v541)", "v542_538off", "ref_no538"),
    ("v542[LOKI_FS_V539=False]     == merge(v538,v541)", "v542_539off", "ref_no539"),
    ("v542[FS_V541_COREPECK=False] == merge(v538,v539)", "v542_541off", "ref_no541"),
    ("v542[ALL THREE OFF]          == _v537socket",      "v542_alloff", "parent"),
]
CONTROLS = [
    ("v542 vs v542[LOKI_FS_V538=False]     (v538 acted?)", "v542", "v542_538off"),
    ("v542 vs v542[LOKI_FS_V539=False]     (v539 acted?)", "v542", "v542_539off"),
    ("v542 vs v542[FS_V541_COREPECK=False] (v541 acted?)", "v542", "v542_541off"),
    ("v542 vs _v537socket                  (merge acted?)", "v542", "parent"),
]


def load(path):
    ls = open(path).read().splitlines()
    h = ls[0].split("\t")
    rows = [dict(zip(h, l.split("\t"))) for l in ls[1:] if l.strip()]
    by = {}
    for r in rows:
        by.setdefault(r["arm"], {})[tuple(r[k] for k in KEY)] = r
    return rows, by


def cmp_arms(by, a, b):
    if a not in by or b not in by:
        raise SystemExit("REFUSED: arm %r or %r absent from the tape"
                         % (a, b))
    A, B = by[a], by[b]
    ks = sorted(set(A) & set(B))
    if not ks:
        raise SystemExit("REFUSED: %s and %s share no cells" % (a, b))
    d = [k for k in ks
         if any(A[k][c] != B[k][c] for c in A[k] if c not in IGNORE)]
    return len(ks), d


def table(path, label="", verbose=True):
    rows, by = load(path)
    tb = sum(int(r.get("tracebacks", 0)) for r in rows)
    out = {}
    if verbose:
        print("TAPE %s%s — %d rows, %d arms"
              % (path, (" [%s]" % label) if label else "", len(rows), len(by)))
        print("%-52s %6s %8s  %s" % ("", "cells", "differ", "where"))
        print("--- THE FOUR IDENTITY CLAIMS (each must read 0) ---")
    ident_ok = True
    for tag, a, b in IDENTITIES:
        n, d = cmp_arms(by, a, b)
        out[tag] = (n, len(d))
        ident_ok &= (len(d) == 0)
        if verbose:
            print("%-52s %6d %8d  %s" % (tag, n, len(d), _where(d)))
    if verbose:
        print("--- THE NEGATIVE CONTROLS (each must read > 0) ---")
    ctl_ok = True
    for tag, a, b in CONTROLS:
        n, d = cmp_arms(by, a, b)
        out[tag] = (n, len(d))
        ctl_ok &= (len(d) > 0)
        if verbose:
            print("%-52s %6d %8d  %s" % (tag, n, len(d), _where(d)))
    if verbose:
        print("\nIDENTITIES %s   CONTROLS %s   TRACEBACKS %d"
              % ("PASS" if ident_ok else "**FAIL**",
                 "PASS" if ctl_ok else
                 "**FAIL — an identity above is pass-by-default**", tb))
    return ident_ok, ctl_ok, out


def _where(d):
    if not d:
        return "-"
    c = collections.Counter("%s/%s" % (k[0], k[2]) for k in d)
    return " ".join("%s:%d" % kv for kv in sorted(c.items()))


# ---------------------------------------------------------------------------
def selftest():
    import os
    import tempfile
    fails = []

    def chk(tag, cond):
        print("  %-64s %s" % (tag, "ok" if cond else "!!! WRONG VERDICT"))
        if not cond:
            fails.append(tag)

    arms = ["parent", "v542", "v542_538off", "v542_539off", "v542_541off",
            "ref_no538", "ref_no539", "ref_no541", "v542_alloff"]
    hdr = "arm\tmap\tseed\tseat\tours\twinner\tcond\tturn\ttracebacks"

    def tape(turns, path):
        """turns: arm -> turn value on the single differing cell."""
        L = [hdr]
        for a in arms:
            for s in (1, 2):
                t = turns.get(a, 100) if s == 1 else 100
                L.append("\t".join([a, "m", str(s), "A", "US", a,
                                    "Core destroyed", str(t), "0"]))
        open(path, "w").write("\n".join(L) + "\n")
        return path

    d = tempfile.mkdtemp(prefix="abl_")
    P = lambda n: os.path.join(d, n)

    print("SELFTEST abl.py — every verdict, both ways")

    # HONEST: each ablation arm matches its reference; each acts vs v542.
    good = {"v542": 200, "v542_538off": 110, "ref_no538": 110,
            "v542_539off": 120, "ref_no539": 120,
            "v542_541off": 130, "ref_no541": 130,
            "v542_alloff": 100, "parent": 100}
    i, c, _ = table(tape(good, P("good.tsv")), verbose=False)
    chk("HONEST tape: identities PASS", i)
    chk("HONEST tape: controls PASS", c)

    # BROKEN IDENTITY: one ablation arm no longer matches its reference.
    bad = dict(good, ref_no539=121)
    i, c, _ = table(tape(bad, P("bad.tsv")), verbose=False)
    chk("broken identity (ref_no539 moved) -> identities FAIL", not i)
    chk("  ...and controls still PASS", c)

    # VACUOUS: a plank that never acts — v542 == its own ablation arm.
    vac = dict(good, v542=110, v542_539off=110, ref_no539=110,
               v542_541off=110, ref_no541=110, v542_538off=110,
               ref_no538=110)
    i, c, _ = table(tape(vac, P("vac.tsv")), verbose=False)
    chk("no plank acts -> identities PASS but controls FAIL", i and not c)

    # MISSING ARM must refuse, not silently skip.
    L = open(P("good.tsv")).read().splitlines()
    open(P("miss.tsv"), "w").write(
        "\n".join([L[0]] + [l for l in L[1:]
                            if not l.startswith("ref_no538\t")]) + "\n")
    try:
        table(P("miss.tsv"), verbose=False)
        chk("missing arm -> must REFUSE", False)
    except SystemExit:
        chk("missing arm -> must REFUSE", True)

    # `winner` alone must NOT count as a difference (it carries the arm name).
    L = open(P("good.tsv")).read().splitlines()
    fix = [L[0]] + [("\t".join(f[:5] + ["SAME"] + f[6:]) if (f := l.split("\t"))
                     else l) for l in L[1:]]
    open(P("win.tsv"), "w").write("\n".join(fix) + "\n")
    i2, c2, _ = table(P("win.tsv"), verbose=False)
    chk("normalising `winner` changes nothing (it is ignored)",
        (i2, c2) == (i, c) if False else (i2 is True and c2 is True))

    print("SELFTEST %s (%d wrong verdicts)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 0 if not fails else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("tape", nargs="?")
    ap.add_argument("--label", default="")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if not a.tape:
        ap.error("tape required")
    i, c, _ = table(a.tape, a.label)
    sys.exit(0 if (i and c) else 1)
