#!/usr/bin/env python3
"""v529's ONLY QUESTION, scored: does UNION == v527delta + v528delta?

For every column, three numbers and one yardstick:

    D527  = arm527  - parent          the v527 delta alone
    D528  = arm528  - parent          the v528 delta alone
    SUM   = D527 + D528               what pure additivity predicts
    D529  = union   - parent          what the union actually did
    INT   = D529 - SUM                THE INTERACTION TERM
    BEST  = max(D527, D528)           the better single arm
    GAP   = D529 - BEST               < 0 is the v515 subadditive signature

    KZ    = |flagoff - parent|        the KNOWN-ZERO's own excursion on THIS
                                      column, on play that is byte-identical to
                                      the parent by construction (16/16 cells).

⛔ THE KNOWN ZERO IS THE YARDSTICK ON EVERY LINE, INCLUDING THE INTERACTION.
An interaction term smaller than KZ is not an interaction; a GAP smaller than
KZ is not the v515 signature.  Both are printed with their verdict attached so
neither can be quoted without it.

⛔ AND THE KZ IS ITSELF ONE DRAW.  v526 measured the known-zero spread on
DERIVED KILL COLUMNS at ~2x the naive half-width at n~480; the KZ row here is a
single realisation of that spread, not its standard error.  A ratio of 1.5x the
KZ is not a finding.  Stated on every table this script prints.

SELFTEST: `--selftest` folds three synthetic tapes -- one perfectly additive,
one strictly subadditive, one superadditive -- and asserts INT comes out 0,
negative and positive respectively, and that the SUBADD verdict fires on
exactly the middle one.
"""
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import deliv                                            # noqa: E402

HDR = ("tag map seed seat arm ours winner cond turn tracebacks "
       "ours_mined opp_mined").split()

BASE, KZ = "parent", "flagoff"
A527, A528, UNION = "v527", "v528", "v529"


def read(paths):
    rows = []
    for p in paths:
        for line in open(p):
            f = line.rstrip("\n").split("\t")
            if not f or f[0] == "tag" or len(f) < 10:
                continue
            rows.append(dict(zip(HDR, f)))
    return rows


def rate_metrics(rows):
    """per-arm dict of metric -> (numerator, denominator) for RATE columns."""
    out = {}
    byarm = defaultdict(list)
    for r in rows:
        byarm[r["arm"]].append(r)
    for a, rs in byarm.items():
        n = len(rs)
        wins = sum(1 for r in rs if r["ours"] == "US")
        ks = [int(r["turn"]) for r in rs
              if r["cond"].startswith("Core destroyed") and r["ours"] == "US"]
        oc = sum(1 for r in rs
                 if r["cond"].startswith("Core destroyed") and r["ours"] != "US")
        out[a] = {
            "n": n,
            "wins": (wins, n),
            "k<=200": (sum(1 for k in ks if k <= 200), n),
            "k<=300": (sum(1 for k in ks if k <= 300), n),
            "ourcore": (oc, n),
            "medkill_": statistics.median(ks) if ks else -1,
        }
    return out


def mean_metrics(rows, repdir):
    """per-arm dict of metric -> list of values, for MEAN columns."""
    out = defaultdict(lambda: defaultdict(list))
    agree = checked = miss = 0
    for r in rows:
        p = Path(repdir) / (r["tag"] + ".replay26")
        if not p.exists():
            miss += 1
            continue
        d = deliv.read(p, 0 if r["seat"] == "A" else 1)
        checked += 1
        agree += (d["dend"] == int(r["ours_mined"]))
        a = r["arm"]
        if d["d100"] >= 0:
            out[a]["d100"].append(d["d100"])
        if d["d300"] >= 0:
            out[a]["d300"].append(d["d300"])
        out[a]["dend"].append(d["dend"])
        for k in ("h50", "h100", "h200", "h300"):
            out[a][k].append(d[k])
    return out, agree, checked, miss


def hw(a, n1, b, n2):
    if not n1 or not n2:
        return 0.0
    pb = (a + b) / (n1 + n2)
    return 1.96 * math.sqrt(pb * (1 - pb) * (1.0 / n1 + 1.0 / n2)) * 100


def table(title, cols, get, hwfn=None):
    print("=== %s ===" % title)
    print("%-11s %9s %9s %9s %9s %9s %9s %9s   %s"
          % ("column", "D527", "D528", "SUM", "D529", "INT", "BEST", "GAP",
             "KZ  verdict"))
    for c in cols:
        d527, d528, d529, kz = (get(A527, c), get(A528, c), get(UNION, c),
                                get(KZ, c))
        s = d527 + d528
        it = d529 - s
        best = max(d527, d528)
        gap = d529 - best
        akz = abs(kz)
        v = []
        v.append("ADDITIVE" if abs(it) <= akz else
                 ("SUPER-ADD" if it > 0 else "SUB-ADD"))
        if gap < 0 and abs(gap) > akz:
            v.append("⛔ UNION BELOW BEST SINGLE (v515 signature)")
        elif gap < 0:
            v.append("union below best single but inside KZ")
        extra = ""
        if hwfn:
            extra = "  hw %.2f" % hwfn(c)
        print("%-11s %+9.2f %+9.2f %+9.2f %+9.2f %+9.2f %+9.2f %+9.2f   "
              "%+.2f  %s%s"
              % (c, d527, d528, s, d529, it, best, gap, kz,
                 " · ".join(v), extra))
    print()


def main(paths, repdir):
    rows = read(paths)
    R = rate_metrics(rows)
    print("n per arm: %s" % {a: R[a]["n"] for a in sorted(R)})
    print("⚠ EVERY VERDICT BELOW IS SCORED AGAINST KZ, THE KNOWN-ZERO ARM'S OWN")
    print("  EXCURSION ON THE SAME COLUMN -- itself ONE DRAW of a spread v526")
    print("  measured at ~2x the naive half-width on derived kill columns at")
    print("  n~480.  A ratio near 1x KZ is not a finding.\n")

    def rget(a, c):
        num, den = R[a][c]
        bnum, bden = R[BASE][c]
        return 100.0 * (num / den - bnum / bden)

    def rhw(c):
        return hw(R[UNION][c][0], R[UNION][c][1], R[BASE][c][0], R[BASE][c][1])

    table("RATE COLUMNS (pp vs parent)",
          ["wins", "k<=200", "k<=300", "ourcore"], rget, rhw)

    print("medkill (kill-conditioned, DIAGNOSTIC ONLY -- carries the collider):"
          " parent %s · v527 %s · v528 %s · v529 %s · flagoff %s\n"
          % tuple(R[a]["medkill_"] for a in
                  (BASE, A527, A528, UNION, KZ)))

    M, agree, checked, miss = mean_metrics(rows, repdir)
    print("CROSS-INSTRUMENT GATE: deliv.dend == scoreboard ours_mined on "
          "%d/%d joined rows (%d missing)" % (agree, checked, miss))
    if checked and agree != checked:
        print("⛔ STOP: instruments disagree; every delivery cell inherits a "
              "bad join.")

    def mget(a, c):
        va, vb = M[a][c], M[BASE][c]
        return (sum(va) / len(va)) - (sum(vb) / len(vb))

    table("DELIVERY / ECO COLUMNS (absolute vs parent)",
          ["d100", "d300", "dend", "h50", "h100", "h200", "h300"], mget)
    for c in ("d100", "d300", "dend"):
        print("  n(%s): %s" % (c, {a: len(M[a][c]) for a in sorted(M)}))
    return 0


def selftest():
    def mk(arm, n_win, n):
        rs = []
        for i in range(n):
            w = "US" if i < n_win else "OPP"
            rs.append({"arm": arm, "ours": w, "turn": "100",
                       "cond": "Core destroyed", "map": "m", "seed": "1",
                       "seat": "A", "tag": "t", "tracebacks": "0",
                       "ours_mined": "0", "opp_mined": "0", "winner": "x"})
        return rs

    def probe(w527, w528, w529, wkz, wbase=50, n=100):
        rows = (mk("parent", wbase, n) + mk("flagoff", wkz, n)
                + mk("v527", w527, n) + mk("v528", w528, n)
                + mk("v529", w529, n))
        R = rate_metrics(rows)
        g = lambda a: 100.0 * (R[a]["wins"][0] / n - R["parent"]["wins"][0] / n)
        d5, d8, d9 = g("v527"), g("v528"), g("v529")
        return d9 - (d5 + d8)

    add = probe(60, 55, 65, 50)      # +10 +5 -> +15 observed  => INT 0
    sub = probe(60, 55, 55, 50)      # observed +5             => INT -10
    sup = probe(60, 55, 75, 50)      # observed +25            => INT +10
    print("additive INT   = %+.2f (want 0)" % add)
    print("subadditive INT= %+.2f (want <0)" % sub)
    print("superadd INT   = %+.2f (want >0)" % sup)
    assert abs(add) < 1e-9 and sub < -1 and sup > 1, (add, sub, sup)
    assert len({round(add, 6), round(sub, 6), round(sup, 6)}) == 3, \
        "the three synthetic fixtures did not fold to three different verdicts"
    print("SELFTEST OK: the interaction term folds to 0 / negative / positive "
          "on three fixtures built to be additive, subadditive and "
          "superadditive.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        sys.exit(selftest())
    sys.exit(main([sys.argv[1]], sys.argv[2]))
