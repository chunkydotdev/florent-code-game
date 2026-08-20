#!/usr/bin/env python3
"""v530 P1 — THE SOCKET RACE AND THE DELIVERY, folded per arm.

⛔ THE INSTRUMENT IS NOT MINE.  Every column below comes from the research arm's
`scratchpad/s51_route/routetape.py`, which is the tool the crater autopsy was
measured on and which carries its own both-verdicts control table (winner-vs-
tape 900/900, a false-asymmetry bug already found and fixed in its map symmetry
check, `death_mid` driven to 0 and to nonzero on the same branch).  Re-deriving
those columns here would mean re-earning that validation; this script only folds
its output by arm.

COLUMNS, and what each one is for:
  head1  first round a conveyor OF OURS stands ON one of our 8 core-ring
         sockets.  ⭐ THIS IS THE PLANK'S PRIMARY: parent baseline r80.6 on the
         crater maps, target <= r3.
  head2  first round our belt head is one BFS step short of home (the parent's
         own clock; mouth-first should make head1 <= head2, which is the
         ordering inversion stated as a number)
  esealF first round any ENEMY entity stands on one of our 8 sockets
  margin esealF - head1.  Positive = we claimed the mouth first.
  wonrace share of games with head1 >= 0 and (esealF < 0 or head1 < esealF)
  beltfail share of games in which NO conveyor of ours EVER reached a socket
         -- the crater-class signature; 49/60 on icefloe for the parent line
  coll100 titanium DELIVERED by r100 (the engine's own counter)
  zero100 share of games with coll100 == 0  -- the icefloe 60/60 signature
  oconv30 OUR OWN CONVEYORS standing on our 8 sockets at r30 -- the ring-claim
         completeness column, and the one P1b lives or dies on.
         ⛔ DERIVED, NOT READ: routetape emits `oseal{r}` for our own NON-BELT
         buildings ("Ob") and has no column for our conveyors ("Oc").  The five
         codes it assigns are exhaustive (Oc / Ob / Ex / Eb / "."), so
         oconv = homering_n - eseal - oseal - free.  The first version of this
         script printed `oseal30` and read 0.00 for every arm INCLUDING the one
         whose whole plank is a conveyor on a socket -- a constant column, and
         the reason this note exists.
  oseal30 our own NON-belt buildings on our 8 sockets at r30
  ebar30 enemy BARRIERS on our 8 sockets at r30
"""
import statistics
import sys
from collections import defaultdict


def med(xs):
    return statistics.median(xs) if xs else -1


def mean(xs):
    return sum(xs) / len(xs) if xs else -1


def main(paths):
    rows = []
    for p in paths:
        with open(p) as f:
            hdr = f.readline().rstrip("\n").split("\t")
            for ln in f:
                rows.append(dict(zip(hdr, ln.rstrip("\n").split("\t"))))
    byarm = defaultdict(list)
    for r in rows:
        # `routetape.py --batch` does not carry the arm column through, and the
        # arm is the first field of the tag `run_battery.py` writes
        # ("<arm>_<map>_s<seed>_<seat>").  Derived here rather than by editing
        # the research arm's validated tool.
        arm = r.get("arm") or r.get("tag", "?").split("_", 1)[0]
        byarm[arm].append(r)

    def I(r, k, d=-1):
        try:
            return int(float(r[k]))
        except Exception:
            return d

    print("%-9s %5s | %7s %7s %7s %7s %7s %8s | %8s %7s | %7s %7s %7s %7s"
          % ("arm", "n", "head1", "head2", "esealF", "margin", "wonrace",
             "beltfail", "coll100", "zero100", "oconv30", "oconv60",
             "oseal30", "ebar30"))
    for a in sorted(byarm):
        rs = byarm[a]
        h1 = [I(r, "head1_rnd") for r in rs]
        h2 = [I(r, "head2_rnd") for r in rs]
        ef = [I(r, "eseal_first") for r in rs]
        h1p = [x for x in h1 if x >= 0]
        h2p = [x for x in h2 if x >= 0]
        efp = [x for x in ef if x >= 0]
        marg = [e - h for h, e in zip(h1, ef) if h >= 0 and e >= 0]
        won = sum(1 for h, e in zip(h1, ef) if h >= 0 and (e < 0 or h < e))
        fail = sum(1 for x in h1 if x < 0)
        c100 = [I(r, "ti_coll100", 0) for r in rs]
        z100 = sum(1 for x in c100 if x == 0)
        os30 = [I(r, "oseal30", 0) for r in rs]
        eb30 = [I(r, "ebar30", 0) for r in rs]
        oc30 = [max(0, I(r, "homering_n", 0) - I(r, "eseal30", 0)
                    - I(r, "oseal30", 0) - I(r, "free30", 0)) for r in rs]
        oc60 = [max(0, I(r, "homering_n", 0) - I(r, "eseal60", 0)
                    - I(r, "oseal60", 0) - I(r, "free60", 0)) for r in rs]
        print("%-9s %5d | %7.1f %7.1f %7.1f %7.1f %6.3f  %7.3f | %8.1f %7.3f | "
              "%7.2f %7.2f %7.2f %7.2f"
              % (a, len(rs), mean(h1p), mean(h2p), mean(efp), mean(marg),
                 won / len(rs), fail / len(rs), mean(c100), z100 / len(rs),
                 mean(oc30), mean(oc60), mean(os30), mean(eb30)))
    print()
    print("=== OPENING COST PANEL (the price side of P1 / P1b / P2) ===")
    print("⛔ spawn_n / spawn_n30 are the SELF-SPAWN-DENIAL column: our own 12")
    print("   ring tiles are also our 12 spawn tiles, and P2 barriers 3 of the")
    print("   4 corners while P1/P1b pave sockets.  A fall here is a real cost.")
    print("%-9s %5s | %7s %7s %8s | %7s %7s %8s %8s | %8s %7s"
          % ("arm", "n", "spawn_n", "spwn30", "spawn1", "harv1", "conv1",
             "harv_n30", "conv_n30", "ti_bnk30", "turrets"))
    for a in sorted(byarm):
        rs = byarm[a]
        def C(k):
            v = [I(r, k) for r in rs]
            return mean([x for x in v if x >= 0])
        print("%-9s %5d | %7.2f %7.2f %8.2f | %7.2f %7.2f %8.2f %8.2f | "
              "%8.1f %7.2f"
              % (a, len(rs), C("spawn_n"), C("spawn_n30"), C("spawn1_rnd"),
                 C("harv1_rnd"), C("conv1_rnd"), C("harv_n30"), C("conv_n30"),
                 C("ti_bank30"), C("turret_n")))
    print()
    print("=== ECO CONNECTIVITY (harvesters WITH a route home) ===")
    print("%-9s %5s | %8s %8s | %8s %8s | %9s %9s"
          % ("arm", "n", "hlive30", "hwire30", "hlive100", "hwire100",
             "convhome30", "convhome100"))
    for a in sorted(byarm):
        rs = byarm[a]
        def C(k):
            v = [I(r, k) for r in rs]
            return mean([x for x in v if x >= 0])
        print("%-9s %5d | %8.2f %8.2f | %8.2f %8.2f | %9.2f %9.2f"
              % (a, len(rs), C("harv_live30"), C("harv_wired30"),
                 C("harv_live100"), C("harv_wired100"), C("conv_home30"),
                 C("conv_home100")))
    print()
    print("PER MAP head1 mean (games where the belt EVER reached a socket) | "
          "beltfail share")
    maps = sorted({r["map"] for r in rows})
    arms = sorted(byarm)
    print("%-14s %s" % ("map", "  ".join("%-16s" % a for a in arms)))
    for m in maps:
        cells = []
        for a in arms:
            rs = [r for r in byarm[a] if r["map"] == m]
            h1 = [I(r, "head1_rnd") for r in rs]
            ok = [x for x in h1 if x >= 0]
            cells.append("%6.1f %5.2f  " % (mean(ok),
                                            sum(1 for x in h1 if x < 0)
                                            / max(1, len(rs))))
        print("%-14s %s" % (m, "  ".join(cells)))


def selftest():
    a = [{"head1_rnd": "3", "eseal_first": "9", "ti_coll100": "100",
          "map": "x", "arm": "t", "head2_rnd": "4", "oseal30": "0",
          "ebar30": "0", "homering_n": "8", "eseal30": "0", "free30": "5",
          "eseal60": "0", "oseal60": "0", "free60": "4"}]
    b = [{"head1_rnd": "-1", "eseal_first": "7", "ti_coll100": "0",
          "map": "x", "arm": "c", "head2_rnd": "20", "oseal30": "0",
          "ebar30": "4", "homering_n": "8", "eseal30": "4", "free30": "4",
          "eseal60": "4", "oseal60": "0", "free60": "4"}]
    import io
    import contextlib
    buf = io.StringIO()
    import tempfile
    import os
    fd, p = tempfile.mkstemp()
    hdr = list(a[0])
    with os.fdopen(fd, "w") as f:
        f.write("\t".join(hdr) + "\n")
        for r in a + b:
            f.write("\t".join(str(r[k]) for k in hdr) + "\n")
    with contextlib.redirect_stdout(buf):
        main([p])
    os.unlink(p)
    txt = buf.getvalue()
    # Only the FIRST panel: the later panels emit rows with the same arm
    # prefixes, and matching those too made this assertion see four rows.
    first = txt.split("=== OPENING COST PANEL")[0]
    lines = [ln for ln in first.splitlines() if ln.startswith(("t ", "c "))]
    assert len(lines) == 2, txt
    tline = [ln for ln in lines if ln.startswith("t ")][0]
    cline = [ln for ln in lines if ln.startswith("c ")][0]
    assert "1.000" in tline and "0.000" in tline, tline
    assert "0.000" in cline and "1.000" in cline, cline
    assert tline != cline, "the fold must separate a won race from a belt fail"
    # the DERIVED oconv column must separate the two rows too: 8-0-0-5 = 3
    # against 8-4-0-4 = 0.  A column that read 0 in both would be the defect
    # this selftest exists to catch.
    assert "   3.00" in tline, tline
    assert "   0.00" in cline, cline
    print("SELFTEST OK: a game with head1=3 < eseal=9 folds to wonrace=1.000 / "
          "beltfail=0.000 / zero100=0.000, and a game with head1=-1, coll100=0 "
          "folds to wonrace=0.000 / beltfail=1.000 / zero100=1.000 -- the two "
          "rows differ, so no column is a constant.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        sys.exit(selftest())
    main(sys.argv[1:])
