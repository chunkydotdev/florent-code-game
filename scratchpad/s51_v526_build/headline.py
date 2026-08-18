#!/usr/bin/env python3
"""v526 HEADLINE: the KILL_TARGET panel + per-map, per arm.

`PROGRAMME.md` KILL_TARGET: median kill <= r180 · tracked metric = share of ALL
games killed by r200 · r300 is the hard admissibility floor
(DEFENCE_ADMISSION_BAR, ITT: the share of ALL games ending in a core kill by
r300 must not FALL vs control).

⛔ LOCAL FIXTURE.  The s39 audit measured a pair-weighted local DEFF of 0.98 on
a balanced-by-construction shard fixture, so the PLATFORM constants (1.529
rated / 1.833 unrated) do NOT apply and are not used.  Naive two-sample
half-widths.

⛔ SELF-TESTED: `--selftest` folds an all-win tape, an all-loss tape and a
mixed tape and asserts the counters differ.
"""
import math
import statistics
import sys
from collections import defaultdict

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
    p1, p2 = a / n1, b / n2
    pb = (a + b) / (n1 + n2)
    return 1.96 * math.sqrt(pb * (1 - pb) * (1.0 / n1 + 1.0 / n2)) * 100


def main(paths, base_arm="parent"):
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
    for a in arms:
        if a == base_arm:
            continue
        o = pool[a]
        for lab, fn in (("wins", lambda x: x["wins"]),
                        ("k<=200", lambda x: sum(1 for k in x["kill_rounds"]
                                                 if k <= 200)),
                        ("k<=300", lambda x: x["k300"])):
            A, B = fn(o), fn(base)
            d = 100.0 * (A / o["n"] - B / base["n"])
            h = hw(A, o["n"], B, base["n"])
            print("%-10s vs %-8s %-7s %+6.2f pp (hw %.2f)  %s"
                  % (a, base_arm, lab, d, h,
                     "OUTSIDE" if abs(d) > h else "inside"))
        mk = [k for k in o["kill_rounds"]]
        bk = [k for k in base["kill_rounds"]]
        print("%-10s vs %-8s medkill %s vs %s   (kill-conditioned, diagnostic "
              "only -- carries the collider)"
              % (a, base_arm,
                 statistics.median(mk) if mk else -1,
                 statistics.median(bk) if bk else -1))
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


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        def mk(arm, n, ours, cond, turn):
            return ["\t".join(["t", "atoll", "1", "A", arm, ours, "x", cond,
                               str(turn), "0", "0", "0"]) for _ in range(n)]
        import tempfile
        import os
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
        print("SELFTEST OK: all-win / all-loss / mixed fold to different "
              "counters (wins, k300, ourcore, r1000, medkill).")
        sys.exit(0)
    main(sys.argv[1:])
