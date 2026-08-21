#!/usr/bin/env python3
"""v538 build instrument #3 -- FLAG-OFF IS THE PARENT, PROVED FOUR WAYS.

COPIED from `scratchpad/s52_v535_build/test_flagoff.py` (never edited in place)
and re-pointed at v538.  Same four proofs, same both-ways controls.

1. BYTES. `raid.py` is untouched (md5 vs the frozen parent). The other four
   files differ only where the diff audit enumerates.
2. READ-SITE SCAN, WITH THE HOUSE POSITIVE CONTROL. Every v538 name must be
   read INSIDE a function body, never at module scope, or an arm override
   (`mkarm.sh` edits the definition site; `gatemap._flagged_tree` pokes the
   module object) would not reach the code -- the v515 finding-3 hazard.
   ⛔ THE CONTROL: `FS_V525_LOG` is a KNOWN DEAD FLAG in THIS lineage --
   defined in doctrine.py, read nowhere in the tree (v535's control flag
   `FS_V530_MOUTH_SEATS` does not exist here: v537 descends v536trustport <-
   v529merge, which never carried the home package). The dead flag was found by
   enumerating every FS_*/LOKI_* definition and subtracting every Load site, not
   assumed. A scanner that reports "all v538 flags are read in functions"
   is worthless unless it can also report "this flag is read NOWHERE" -- so the
   same scanner is run on the dead flag and MUST return zero read sites, and on
   a live parent flag (`FS_V537_SOCKET`) and MUST return several.
3. NO DERIVED MODULE-LEVEL DEFAULT anywhere in the tree reads a v538 flag.
   Driven both ways on a synthetic module that DOES have one.
4. BEHAVIOUR. With `FS_V538_CLAIM_GATE = False` the predicate returns exactly
   `FS_V537_SOCKET` on every cell of the whole map pool -- INCLUDING the 16
   cells where flag-on deliberately differs -- and the siege helper is never
   called at all, proved by monkeypatching it to raise.

  .venv/bin/python .../test_flagoff.py
"""
import ast
import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from harness import FakeCt, REPO, grid_of_map, load_tree, make_player  # noqa: E402
from gatemap import CORE_VIS, _flagged_tree, maps_in_pool, one  # noqa: E402
from fcode import Environment, Position  # noqa: E402

CHILD = "_v538refine"
PARENT = "_v537socket"
V535_FLAGS = {"LOKI_FS_V538", "FS_V538_CLAIM_GATE", "FS_V538_LOG"}
DEAD_FLAG = "FS_V525_LOG"             # the positive control (dead in-tree)
LIVE_FLAG = "FS_V537_SOCKET"          # the negative control (live in-tree)


def md5(p):
    return hashlib.md5(Path(p).read_bytes()).hexdigest()


def scan_module_level(path, flags):
    """Module-level assignments (or module-level ifs) whose RHS reads a flag."""
    tree = ast.parse(Path(path).read_text())
    hits = []
    for node in tree.body:
        val = None
        if isinstance(node, ast.Assign):
            val = node.value
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            val = node.value
        elif isinstance(node, ast.If):
            val = node.test
        if val is None:
            continue
        for sub in ast.walk(val):
            if isinstance(sub, ast.Name) and sub.id in flags:
                hits.append((Path(path).name, node.lineno, sub.id))
    return hits


def scan_readsites(path, flags):
    """(lineno, flag, in_function) for every READ of a flag in `path`.

    A definition site (`X = True`) is a Store, not a Load, and is excluded --
    that is what lets the dead-flag control come out zero.
    """
    src = Path(path).read_text()
    tree = ast.parse(src)
    infn = set()
    for fn in ast.walk(tree):
        if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for sub in ast.walk(fn):
                if isinstance(sub, ast.Name) and sub.id in flags \
                        and isinstance(sub.ctx, ast.Load):
                    infn.add((sub.lineno, sub.id))
    out = []
    for sub in ast.walk(tree):
        if isinstance(sub, ast.Name) and sub.id in flags \
                and isinstance(sub.ctx, ast.Load):
            out.append((sub.lineno, sub.id,
                        (sub.lineno, sub.id) in infn))
    return out


SYNTH_BAD = """
FLAG = True
DERIVED = 3 if FLAG else 9
"""
SYNTH_OK = """
FLAG = True
def f():
    return 3 if FLAG else 9
"""


def main():
    ok = True

    def check(label, got, want):
        nonlocal ok
        if got != want:
            ok = False
            print("[FAIL] %s: got %r want %r" % (label, got, want))
        else:
            print("[ok] %s: %r" % (label, got))

    cdir = REPO / "bots" / CHILD
    pdir = REPO / "bots" / PARENT

    # --- 1. BYTES --------------------------------------------------------
    check("raid.py byte-identical to the parent",
          md5(cdir / "raid.py"), md5(pdir / "raid.py"))
    changed = [f for f in ("doctrine.py", "eco.py", "siege.py", "main.py")
               if md5(cdir / f) != md5(pdir / f)]
    check("exactly the 4 intended files differ", sorted(changed),
          ["doctrine.py", "eco.py", "main.py", "siege.py"])

    # --- 2. READ-SITE SCAN + THE POSITIVE CONTROL ------------------------
    allsites = []
    for f in ("doctrine.py", "eco.py", "siege.py", "main.py", "raid.py"):
        allsites += [(f,) + s for s in scan_readsites(cdir / f, V535_FLAGS)]
    print("    v538 read sites: %s" % (allsites,))
    check("every v538 read site is INSIDE a function",
          all(s[3] for s in allsites), True)
    check("v538 flags are read at all (>=3 sites)", len(allsites) >= 3, True)
    got_flags = sorted({s[2] for s in allsites})
    check("all three v538 names are read somewhere",
          got_flags, sorted(V535_FLAGS))

    # ⛔ THE POSITIVE CONTROL. The scanner must be able to say ZERO.
    dead = []
    for f in ("doctrine.py", "eco.py", "siege.py", "main.py", "raid.py"):
        dead += scan_readsites(cdir / f, {DEAD_FLAG})
    check("POSITIVE CONTROL: %s (known dead flag) has 0 read sites" % DEAD_FLAG,
          len(dead), 0)
    live = []
    for f in ("doctrine.py", "eco.py", "siege.py", "main.py", "raid.py"):
        live += scan_readsites(cdir / f, {LIVE_FLAG})
    check("NEGATIVE CONTROL: %s (live flag) has read sites" % LIVE_FLAG,
          len(live) > 0, True)
    #     ...and the dead flag really IS defined, or "0 sites" would just mean
    #     "misspelled name".
    check("the dead flag is actually DEFINED in doctrine.py",
          DEAD_FLAG in (REPO / "bots" / CHILD / "doctrine.py").read_text(), True)

    # --- 3. NO DERIVED MODULE-LEVEL DEFAULT ------------------------------
    derived = []
    for f in ("doctrine.py", "eco.py", "siege.py", "main.py", "raid.py"):
        derived += scan_module_level(cdir / f, V535_FLAGS)
    check("no module-level default derives from a v538 flag", derived, [])
    #     driven both ways on a synthetic module
    tmp = Path(HERE / "_synth_bad.py"); tmp.write_text(SYNTH_BAD)
    check("mutant: scanner FINDS a derived module-level default",
          len(scan_module_level(tmp, {"FLAG"})), 1)
    tmp.write_text(SYNTH_OK)
    check("mutant: scanner passes the safe form",
          len(scan_module_level(tmp, {"FLAG"})), 0)
    tmp.unlink()

    # --- 4. BEHAVIOUR: gate-off == parent on EVERY cell ------------------
    off = _flagged_tree(CHILD, FS_V538_CLAIM_GATE=False)
    on = load_tree(CHILD)
    par = load_tree(PARENT)
    par_on = par["doctrine"].FS_V537_SOCKET
    n = diff_on = 0
    bad_off = []
    for name in maps_in_pool():
        for seat in (0, 1):
            n += 1
            _, o_off = one(off, name, seat)
            _, o_on = one(on, name, seat)
            if o_off != par_on:
                bad_off.append((name, seat, o_off))
            if o_on != par_on:
                diff_on += 1
    check("gate-off matches the parent on all %d cells" % n, bad_off, [])
    check("gate-ON differs from the parent on >0 cells (or 4 proves nothing)",
          diff_on > 0, True)
    print("    gate-ON differs on %d of %d cells" % (diff_on, n))

    #     ...and gate-off must never even CALL the siege helper.
    w, h, grid, cores = grid_of_map("archipelago")   # a refusing board
    ct = FakeCt(grid, cores[0], CORE_VIS, Position, Environment)
    p = make_player(off, w, h, Position(*cores[0]), Position(*cores[1]))

    # ⛔ THE TRAP IS A `BaseException`, NOT AN `AssertionError`, AND THAT IS A
    # FINDING ABOUT THE SHIPPED CODE, NOT A TEST DETAIL: `_v538_claim_on`
    # wraps the helper in `except Exception: return True` (the deliberate
    # "unreadable gate => parent behaviour" fallback), so an `Exception` trap
    # is SWALLOWED and the control reads as "never called" whether or not it
    # was called. The first draft of this test did exactly that and printed a
    # false pass on the control. A trap the code under test can catch is not a
    # trap.
    class Trap(BaseException):
        pass

    def boom(*a, **k):
        raise Trap("called the siege helper")
    p._v535_map_refuses = boom
    try:
        got = p._v538_claim_on(ct)
        check("gate-off never calls _v535_map_refuses (helper raises)",
              got, par_on)
    except Trap:
        ok = False
        print("[FAIL] gate-off CALLED the siege helper")
    #     ...and the same booby trap MUST fire with the gate ON, or the test
    #     above only proves the trap was never armed.
    p2 = make_player(on, w, h, Position(*cores[0]), Position(*cores[1]))
    p2._v535_map_refuses = boom
    try:
        p2._v538_claim_on(ct)
        ok = False
        print("[FAIL] CONTROL: gate-ON did not call _v535_map_refuses")
    except Trap:
        print("[ok] CONTROL: gate-ON DOES call _v535_map_refuses (trap armed)")

    print("FLAGOFF", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
