#!/usr/bin/env python3
"""BOTH-WAYS GUARD for parse.py.

Three synthetic games with KNOWN answers, plus one mutation of each.  The point
is not that the parser reports a number -- it is that it reports a DIFFERENT
number when the log says something different, and specifically that a body that
never reaches the ring comes out as -1 and NOT as round 0.

Run: .venv/bin/python scratchpad/s51_doubleferry/fixture.py
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import parse  # noqa: E402

ARM = "v513_dblferry"
OUT_WIN = ("Winner: v513_dblferry  (Core destroyed, turn 214)\n")
OUT_TIE = ("Winner: base  (Titanium collected (tiebreak), turn 1000)\n")


def game_a():
    """Both bodies arrive: b1 ring 13 adj 13, b2 ring 14 adj 14, both alive."""
    L = ["DF SPAWN 1 id 3 body 1 seat 0 at 4,23 scale 140",
         "DF SPAWN 2 id 5 body 2 seat 1 at 4,24 scale 160",
         "DF MUSTER 1 id 3 wait 1 at 4,23",
         "DF MUSTER 2 id 3 wait 1 at 4,23",
         "DF HOPBUILD 3 id 3 body 1 at 4,23 lch 5,23 cost 36 scale 190",
         "DF THROW 4 launcher 11 body 3 from 4,22 to 9,20 n 1 scale 190",
         "DF THROW 5 launcher 11 body 5 from 6,22 to 8,19 n 2 scale 200",
         "DF TEARDOWN 5 launcher 11 born 4 throws 2 scale 200",
         "DF HOPBUILD 5 id 3 body 1 at 9,20 lch 10,20 cost 38 scale 200",
         "DF ARRIVE 13 id 3 body 1 ring",
         "DF ARRIVE 13 id 3 body 1 adj",
         "DF ARRIVE 14 id 5 body 2 ring",
         "DF ARRIVE 14 id 5 body 2 adj"]
    for r in range(1, 60):
        L.append("DF POS %d id 3 body 1 at 4,23 d 808 hp 40" % r)
        L.append("DF POS %d id 5 body 2 at 4,24 d 845 hp 40" % r)
    return L, OUT_WIN


def game_b():
    """b1 arrives at 13 and DIES at 18 (< ring+10).  b2 NEVER arrives."""
    L = ["DF SPAWN 1 id 3 body 1 seat 0 at 4,23 scale 140",
         "DF SPAWN 2 id 5 body 2 seat 1 at 4,24 scale 160",
         "DF HOPBUILD 3 id 3 body 1 at 4,23 lch 5,23 cost 36 scale 190",
         "DF THROW 4 launcher 11 body 3 from 4,22 to 9,20 n 1 scale 190",
         "DF TEARDOWN 4 launcher 11 born 4 throws 1 scale 190",
         "DF ARRIVE 13 id 3 body 1 ring",
         "DF DEAD 19 id 3 body 1"]
    for r in range(1, 18):
        L.append("DF POS %d id 3 body 1 at 4,23 d 808 hp 40" % r)
    for r in range(1, 900):
        L.append("DF POS %d id 5 body 2 at 4,24 d 845 hp 40" % r)
    return L, OUT_TIE


def game_c():
    """NEITHER body is ever appointed -- an empty plank, all -1, no zeroes."""
    return [], OUT_TIE


def run(name, lines, out):
    d = tempfile.mkdtemp()
    e = os.path.join(d, name + ".err")
    o = os.path.join(d, name + ".out")
    open(e, "w").write("\n".join(lines) + ("\n" if lines else ""))
    open(o, "w").write(out)
    return dict(zip(parse.HDR, parse.row(e, o, ARM, name)))


def check(label, got, want):
    bad = [(k, got.get(k), v) for k, v in want.items() if got.get(k) != v]
    print(("PASS  " if not bad else "FAIL  ") + label)
    for k, g, w in bad:
        print("        %-12s got %-8s want %s" % (k, g, w))
    return not bad


ok = True

a = run("A", *game_a())
ok &= check("A both arrive", a, {
    "b1_spawn": "1", "b1_ring": "13", "b1_adj": "13", "b1_alive10": "1",
    "b2_spawn": "2", "b2_ring": "14", "b2_adj": "14", "b2_alive10": "1",
    "gap": "1", "links": "2", "link2": "1", "link_ti": "74",
    "muster": "2", "outcome": "win", "cond": "core_destroyed", "end_r": "214",
    "b1_throws": "1", "b2_throws": "1", "b1_repl": "0", "b2_repl": "0"})

b = run("B", *game_b())
ok &= check("B b1 dies inside +10, b2 NEVER arrives", b, {
    "b1_ring": "13", "b1_adj": "-1", "b1_alive10": "0",
    # ⛔ THE LOAD-BEARING ASSERTION: a body that never reached the ring must be
    # -1 on ring/adj and -1 (not 0, not 1) on alive10.
    "b2_ring": "-1", "b2_adj": "-1", "b2_alive10": "-1",
    "gap": "-999", "links": "1", "link2": "0", "link_ti": "36",
    "muster": "0", "outcome": "loss", "cond": "r1000", "end_r": "1000"})

c = run("C", *game_c())
ok &= check("C nothing happened at all", c, {
    "b1_spawn": "-1", "b1_ring": "-1", "b1_alive10": "-1",
    "b2_spawn": "-1", "b2_ring": "-1", "b2_alive10": "-1",
    "gap": "-999", "links": "0", "link2": "0", "link_ti": "0"})

# --- MUTATIONS: the same fixtures, changed, must move the answer -------------
la, oa = game_a()
la2 = [x.replace("DF ARRIVE 14 id 5 body 2 ring",
                 "DF ARRIVE 41 id 5 body 2 ring") for x in la]
m1 = run("M1", la2, oa)
ok &= check("M1 moving b2's ring line moves b2_ring and the gap", m1,
            {"b2_ring": "41", "gap": "28"})

la3 = [x for x in la if not x.startswith("DF ARRIVE 13 id 3 body 1 ring")]
m2 = run("M2", la3, oa)
ok &= check("M2 deleting b1's ring line makes b1 never-arrived", m2,
            {"b1_ring": "-1", "b1_alive10": "-1", "gap": "-999"})

lb, ob = game_b()
lb2 = lb + ["DF POS %d id 3 body 1 at 4,23 d 808 hp 40" % r
            for r in range(18, 40)]
m3 = run("M3", lb2, ob)
ok &= check("M3 extending b1's POS trail flips alive10 0 -> 1", m3,
            {"b1_alive10": "1"})

la4 = la + ["DF SPAWN 300 id 77 body 2 seat 6 at 4,26 scale 290"]
m4 = run("M4", la4, oa)
ok &= check("M4 a second body-2 appointment counts as a replacement", m4,
            {"b2_repl": "1", "b2_ring": "14"})

print("\nFIXTURE " + ("OK" if ok else "FAILED"))
sys.exit(0 if ok else 1)
