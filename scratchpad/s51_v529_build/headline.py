#!/usr/bin/env python3
"""v528 HEADLINE: the KILL_TARGET panel + the DELIVERY panel + per-map.

`PROGRAMME.md` KILL_TARGET: median kill <= r180 · tracked metric = share of ALL
games killed by r200 · r300 is the hard admissibility floor
(DEFENCE_ADMISSION_BAR, ITT: the share of ALL games ending in a core kill by
r300 must not FALL vs control).

⛔ THE KNOWN-ZERO ARM IS THE YARDSTICK, NOT THE ZERO.  `flagoff` is byte-
identical to `parent` (byte_identity.py, 10/10 + standdown 10/10), so every
flagoff-vs-parent number below is pure fixture noise at this n.  v526 measured
that spread at ~2x on derived kill columns at n~480, which means a v528-vs-
parent gap smaller than the flagoff-vs-parent gap is NOT a reading.  Both rows
are printed for every comparison so the reader cannot see one without the other.

⛔ LOCAL FIXTURE, NO DEFF.  The s39 audit measured a pair-weighted local DEFF of
0.98 on a balanced-by-construction shard fixture, so the PLATFORM constants
(1.529 rated / 1.833 unrated) do NOT apply and are not used.  Naive two-sample
half-widths.

⛔ THE DELIVERY PANEL'S DENOMINATORS ARE NOT THE ARM'S n.  `d300` exists only
for games that REACHED r300; a game that ended at r89 has no r300 delivery and
is excluded, not zeroed.  `n_r300` travels with every r300 cell.

⛔ CROSS-INSTRUMENT GATE.  `deliv.py`'s end-of-game delivery is compared against
the engine scoreboard's `ours_mined` for EVERY joined row.  A disagreement rate
above 0 stops the read: two instruments that disagree about a number one of them
copied verbatim means the join is wrong, and every delivery cell below inherits
that join.

SELFTEST: `--selftest` folds an all-win tape, an all-loss tape and a mixed tape
and asserts the counters differ; and folds two delivery tapes that must produce
different medians.
"""
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

HDR = ("tag map seed seat arm ours winner cond turn tracebacks "
       "ours_mined opp_mined").split()


def read(paths):
    rows = []
    for p in paths:
        for line in open(p):
            f = line.rstrip("\n").split("\t")
            if not f or f[0] == "tag" or len(f) < 10:
                continue
            rows.append(dict(zip(HDR, f)))
    return rows


def fold(rows):
    out = {"n": len(rows), "wins": 0, "kills": 0, "k300": 0, "ourcore": 0,
           "r1000": 0, "tb": 0, "kill_rounds": []}
    for r in rows:
        turn = int(r["turn"])
        out["tb"] += int(r["tracebacks"])
        if r["ours"] == "US":
            out["wins"] += 1
        if r["cond"].startswith("Core destroyed"):
            if r["ours"] == "US":
                out["kills"] += 1
                out["kill_rounds"].append(turn)
                if turn <= 300:
                    out["k300"] += 1
            else:
                out["ourcore"] += 1
        else:
            out["r1000"] += 1
    ks = sorted(out["kill_rounds"])
    out["median_kill"] = ks[len(ks) // 2] if ks else -1
    return out


def hw(a, n1, b, n2):
    if not n1 or not n2:
        return 0.0
    pb = (a + b) / (n1 + n2)
    return 1.96 * math.sqrt(pb * (1 - pb) * (1.0 / n1 + 1.0 / n2)) * 100


def med(xs):
    return statistics.median(xs) if xs else -1


def delivery(rows, repdir):
    """Join deliv.py's replay read onto the battery rows, by tag."""
    import deliv
    out = defaultdict(list)
    miss = 0
    agree = checked = 0
    for r in rows:
        p = Path(repdir) / (r["tag"] + ".replay26")
        if not p.exists():
            miss += 1
            continue
        d = deliv.read(p, 0 if r["seat"] == "A" else 1)
        checked += 1
        agree += (d["dend"] == int(r["ours_mined"]))
        d["arm"] = r["arm"]
        d["map"] = r["map"]
        out[r["arm"]].append(d)
    return out, miss, agree, checked


def dpanel(ds):
    """One arm's delivery cells, each with its own denominator."""
    d100 = [d["d100"] for d in ds if d["d100"] >= 0]
    d300 = [d["d300"] for d in ds if d["d300"] >= 0]
    dend = [d["dend"] for d in ds]
    t1 = [d["turret1"] for d in ds if d["turret1"] >= 0]
    h1 = [d["harv1"] for d in ds if d["harv1"] >= 0]
    return {
        "n": len(ds),
        "n100": len(d100), "d100_med": med(d100),
        "d100_mean": (sum(d100) / len(d100)) if d100 else -1,
        "n300": len(d300), "d300_med": med(d300),
        "d300_mean": (sum(d300) / len(d300)) if d300 else -1,
        "dend_med": med(dend), "dend_mean": sum(dend) / len(dend) if dend else -1,
        "nt1": len(t1), "t1_med": med(t1),
        "t1_rate": len(t1) / len(ds) if ds else -1,
        "h1_med": med(h1),
        "h50": sum(d["h50"] for d in ds) / len(ds) if ds else -1,
        "h100": sum(d["h100"] for d in ds) / len(ds) if ds else -1,
        "h200": sum(d["h200"] for d in ds) / len(ds) if ds else -1,
        "h300": sum(d["h300"] for d in ds) / len(ds) if ds else -1,
        "conv": sum(d["conv_end"] for d in ds) / len(ds) if ds else -1,
    }


def main(paths, repdir=None, base_arm="parent", kz_arm="flagoff"):
    rows = read(paths)
    byarm = defaultdict(list)
    for r in rows:
        byarm[r["arm"]].append(r)
    arms = sorted(byarm, key=lambda a: (a != base_arm, a))
    pool = {a: fold(byarm[a]) for a in arms}

    print("=== THE KILL_TARGET PANEL ===")
    print("%-10s %6s %7s %9s %9s %9s %9s %9s %8s %8s %4s"
          % ("arm", "n", "wins%", "<=r150", "<=r180", "<=r200", "<=r250",
             "<=r300", "medkill", "ourcore", "tb"))
    for a in arms:
        o = pool[a]
        ks, N = o["kill_rounds"], o["n"]
        cells = []
        for r in (150, 180, 200, 250, 300):
            c = sum(1 for k in ks if k <= r)
            cells.append("%3d(%.3f)" % (c, c / N))
        print("%-10s %6d %6.1f%% %s %8d %8d %4d"
              % (a, N, 100.0 * o["wins"] / N, " ".join(cells),
                 o["median_kill"], o["ourcore"], o["tb"]))
    print()

    base = pool[base_arm]
    METRICS = (("wins", lambda x: x["wins"]),
               ("k<=200", lambda x: sum(1 for k in x["kill_rounds"] if k <= 200)),
               ("k<=300", lambda x: x["k300"]),
               ("ourcore", lambda x: x["ourcore"]))
    for a in arms:
        if a == base_arm:
            continue
        o = pool[a]
        for lab, fn in METRICS:
            A, B = fn(o), fn(base)
            d = 100.0 * (A / o["n"] - B / base["n"])
            h = hw(A, o["n"], B, base["n"])
            tag = "OUTSIDE" if abs(d) > h else "inside"
            note = ""
            if kz_arm in pool and a != kz_arm:
                kz = pool[kz_arm]
                kd = 100.0 * (fn(kz) / kz["n"] - B / base["n"])
                note = "   [known-zero on this metric: %+.2f pp]" % kd
                if abs(d) <= abs(kd):
                    note += "  << SMALLER THAN THE KNOWN ZERO"
            print("%-10s vs %-8s %-8s %+6.2f pp (hw %.2f)  %s%s"
                  % (a, base_arm, lab, d, h, tag, note))
        print("%-10s vs %-8s medkill %s vs %s   (kill-conditioned, diagnostic "
              "only -- carries the collider)"
              % (a, base_arm, med(o["kill_rounds"]), med(base["kill_rounds"])))
        print()

    if repdir:
        dd, miss, agree, checked = delivery(rows, repdir)
        print("=== THE DELIVERY PANEL ===")
        print("CROSS-INSTRUMENT GATE: deliv.dend == scoreboard ours_mined on "
              "%d/%d joined rows (%d replays missing)" % (agree, checked, miss))
        if checked and agree != checked:
            print("⛔ STOP: the two instruments disagree; every cell below "
                  "inherits a bad join.")
        print("%-10s %6s %8s %8s %8s %8s %8s %8s %7s %7s %6s %6s %6s %6s %6s"
              % ("arm", "n", "n100", "d100med", "d100mean", "n300", "d300med",
                 "d300mean", "dendmed", "t1rate", "t1med", "h50", "h100",
                 "h200", "h300"))
        dp = {}
        for a in arms:
            if a not in dd:
                continue
            q = dp[a] = dpanel(dd[a])
            print("%-10s %6d %8d %8.0f %8.1f %8d %8.0f %8.1f %7.0f %7.3f "
                  "%6.0f %6.2f %6.2f %6.2f %6.2f"
                  % (a, q["n"], q["n100"], q["d100_med"], q["d100_mean"],
                     q["n300"], q["d300_med"], q["d300_mean"], q["dend_med"],
                     q["t1_rate"], q["t1_med"], q["h50"], q["h100"],
                     q["h200"], q["h300"]))
        print()
        if base_arm in dp:
            b = dp[base_arm]
            for a in arms:
                if a == base_arm or a not in dp:
                    continue
                q = dp[a]
                for lab in ("d100_mean", "d300_mean", "dend_mean", "t1_med",
                            "h50", "h100", "h200", "h300"):
                    note = ""
                    if kz_arm in dp and a != kz_arm:
                        kzd = dp[kz_arm][lab] - b[lab]
                        note = "   [known-zero %+.2f]" % kzd
                        if abs(q[lab] - b[lab]) <= abs(kzd):
                            note += "  << SMALLER THAN THE KNOWN ZERO"
                    print("%-10s vs %-8s %-10s %10.2f vs %10.2f  (%+.2f)%s"
                          % (a, base_arm, lab, q[lab], b[lab],
                             q[lab] - b[lab], note))
                print()

    print("=== PER MAP: wins/n  [k<=300]  {k<=200} ===")
    maps = sorted({r["map"] for r in rows})
    print("%-14s %s" % ("map", "  ".join("%-22s" % a for a in arms)))
    for m in maps:
        cells = []
        for a in arms:
            o = fold([r for r in byarm[a] if r["map"] == m])
            k2 = sum(1 for k in o["kill_rounds"] if k <= 200)
            cells.append("%2d/%-3d [%2d] {%2d}     "
                         % (o["wins"], o["n"], o["k300"], k2))
        print("%-14s %s" % (m, "  ".join(cells)))


def selftest():
    import os
    import tempfile

    def mk(arm, n, ours, cond, turn):
        return ["\t".join(["t", "atoll", "1", "A", arm, ours, "x", cond,
                           str(turn), "0", "0", "0"]) for _ in range(n)]
    lines = (["\t".join(HDR)]
             + mk("allwin", 10, "US", "Core destroyed", 100)
             + mk("allloss", 10, "OPP", "Core destroyed", 100)
             + mk("mixed", 5, "US", "Core destroyed", 400)
             + mk("mixed", 5, "US", "Round limit", 1000))
    fd, p = tempfile.mkstemp()
    os.write(fd, ("\n".join(lines) + "\n").encode())
    os.close(fd)
    rows = read([p])
    f = {a: fold([r for r in rows if r["arm"] == a])
         for a in ("allwin", "allloss", "mixed")}
    assert f["allwin"]["wins"] == 10 and f["allwin"]["k300"] == 10
    assert f["allloss"]["wins"] == 0 and f["allloss"]["ourcore"] == 10
    assert f["mixed"]["wins"] == 10 and f["mixed"]["k300"] == 0 \
        and f["mixed"]["r1000"] == 5 and f["mixed"]["median_kill"] == 400
    assert f["allwin"]["k300"] != f["mixed"]["k300"]
    assert f["allwin"]["wins"] != f["allloss"]["wins"]
    assert f["mixed"]["r1000"] != f["allwin"]["r1000"]
    os.unlink(p)

    # delivery fold, driven to two different verdicts, INCLUDING the -1 rule
    lo = [{"d100": 10, "d300": 100, "dend": 100, "turret1": 40, "harv1": 4,
           "h50": 1, "h100": 1, "h200": 1, "h300": 1, "conv_end": 5}] * 5
    hi = [{"d100": 90, "d300": 900, "dend": 900, "turret1": 20, "harv1": 2,
           "h50": 3, "h100": 4, "h200": 5, "h300": 6, "conv_end": 40}] * 5
    short = [{"d100": 50, "d300": -1, "dend": 60, "turret1": -1, "harv1": 3,
              "h50": 2, "h100": 2, "h200": 0, "h300": 0, "conv_end": 9}] * 5
    a, b, c = dpanel(lo), dpanel(hi), dpanel(short)
    assert a["d100_mean"] != b["d100_mean"] and a["t1_med"] != b["t1_med"]
    assert c["n300"] == 0 and c["d300_med"] == -1, "r300 gate not applied"
    assert c["n100"] == 5 and c["nt1"] == 0 and c["t1_rate"] == 0.0
    assert a["n300"] == 5, "a full game must count in n300"
    print("SELFTEST OK: all-win / all-loss / mixed fold to different counters "
          "(wins, k300, ourcore, r1000, medkill); delivery folds low/high to "
          "different means; a game that never reached r300 is EXCLUDED from "
          "n300 (0) rather than counted as zero delivery.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        sys.exit(selftest())
    args = sys.argv[1:]
    rep = None
    if "--rep" in args:
        i = args.index("--rep")
        rep = args[i + 1]
        args = args[:i] + args[i + 2:]
    main(args, rep)
