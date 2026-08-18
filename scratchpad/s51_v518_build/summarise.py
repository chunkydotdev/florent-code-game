#!/usr/bin/env python3
"""Fold one or more run_grid TSVs into the report's headline row.

⛔ SELF-TESTED, and the test is the point: `--selftest` builds three synthetic
tapes -- an all-win tape, an all-loss tape, and a mixed tape with a known
kill-round histogram -- and asserts the counters come out DIFFERENT on each.
A summariser that has only ever seen one verdict has not been seen to count.
"""
import sys

HDR = ("tag map seed seat ours winner cond turn tracebacks "
       "ours_mined opp_mined").split()


def read(paths):
    rows = []
    for p in paths:
        for i, line in enumerate(open(p)):
            f = line.rstrip("\n").split("\t")
            if not f or f[0] == "tag" or len(f) < 9:
                continue
            rows.append(dict(zip(HDR, f)))
    return rows


def fold(rows):
    n = len(rows)
    out = {"n": n, "wins": 0, "kills": 0, "k300": 0, "k200": 0,
           "k201_300": 0, "k301_500": 0, "k500p": 0, "ourcore": 0,
           "r1000": 0, "tb": 0, "tiebreak_wins": 0, "kill_rounds": []}
    for r in rows:
        us = r["ours"] == "US"
        turn = int(r["turn"])
        cond = r["cond"]
        out["tb"] += int(r["tracebacks"])
        if us:
            out["wins"] += 1
        if cond.startswith("Core destroyed"):
            if us:
                out["kills"] += 1
                out["kill_rounds"].append(turn)
                if turn <= 200:
                    out["k200"] += 1
                elif turn <= 300:
                    out["k201_300"] += 1
                elif turn <= 500:
                    out["k301_500"] += 1
                else:
                    out["k500p"] += 1
                if turn <= 300:
                    out["k300"] += 1
            else:
                out["ourcore"] += 1
        else:
            out["r1000"] += 1
            if us:
                out["tiebreak_wins"] += 1
    ks = sorted(out["kill_rounds"])
    out["median_kill"] = ks[len(ks) // 2] if ks else -1
    return out


def line(name, o):
    return ("%-18s n=%3d wins=%3d (%.1f%%) kills=%3d k<=300=%3d (%.1f%%) "
            "k<=200=%3d k201-300=%3d k301-500=%3d k>500=%3d ourcore=%3d "
            "r1000=%3d tbwin=%3d medkill=%4d tb=%d"
            % (name, o["n"], o["wins"], 100.0 * o["wins"] / max(1, o["n"]),
               o["kills"], o["k300"], 100.0 * o["k300"] / max(1, o["n"]),
               o["k200"], o["k201_300"], o["k301_500"], o["k500p"],
               o["ourcore"], o["r1000"], o["tiebreak_wins"],
               o["median_kill"], o["tb"]))


def selftest():
    import os
    import tempfile
    d = tempfile.mkdtemp()

    def mk(name, rows):
        p = os.path.join(d, name)
        with open(p, "w") as fh:
            fh.write("\t".join(HDR) + "\n")
            for r in rows:
                fh.write("\t".join(str(x) for x in r) + "\n")
        return p

    allwin = mk("w.tsv", [("g%d" % i, "m", 1, "A", "US", "x",
                           "Core destroyed", 150, 0, 0, 0)
                          for i in range(10)])
    allloss = mk("l.tsv", [("g%d" % i, "m", 1, "A", "OPP", "y",
                            "Core destroyed", 150, 0, 0, 0)
                           for i in range(10)])
    mixed = mk("m.tsv", [("a", "m", 1, "A", "US", "x", "Core destroyed",
                          100, 0, 0, 0),
                         ("b", "m", 1, "A", "US", "x", "Core destroyed",
                          400, 0, 0, 0),
                         ("c", "m", 1, "A", "US", "x",
                          "Titanium collected (tiebreak)", 1000, 0, 0, 0),
                         ("e", "m", 1, "A", "OPP", "y", "Core destroyed",
                          250, 1, 0, 0)])
    w, l, m = fold(read([allwin])), fold(read([allloss])), fold(read([mixed]))
    assert (w["wins"], w["kills"], w["k300"], w["ourcore"]) == (10, 10, 10, 0), w
    assert (l["wins"], l["kills"], l["k300"], l["ourcore"]) == (0, 0, 0, 10), l
    assert (m["wins"], m["kills"], m["k200"], m["k301_500"], m["r1000"],
            m["tiebreak_wins"], m["ourcore"], m["tb"]) \
        == (3, 2, 1, 1, 1, 1, 1, 1), m
    assert m["median_kill"] == 400, m
    # the three verdicts differ on every column that matters
    assert w["wins"] != l["wins"] != m["wins"]
    assert w["k300"] != m["k300"]
    print("SELFTEST PASS: allwin/allloss/mixed all separate")
    print(line("allwin", w))
    print(line("allloss", l))
    print(line("mixed", m))


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        selftest()
    else:
        print(line(sys.argv[1], fold(read(sys.argv[2:]))))
