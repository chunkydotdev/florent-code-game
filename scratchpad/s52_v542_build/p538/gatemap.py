#!/usr/bin/env python3
"""v538 build instrument #2 -- WHERE THE GATE BINDS, over the whole map pool.

COPIED from `scratchpad/s52_v535_build/gatemap.py` (never edited in place) and
re-pointed from the v535 CORNER gate to the v538 CLAIM gate.  Same six mutants,
same both-verdicts discipline; only the consumer predicate changed.

For every `maps/*.map26`, from BOTH seats, this drives the shipped predicate
end-to-end on a real `Player` and prints:

    map            seat  refuse  claim_on(v538)  claim_on(parent)  delta

`claim_on(parent)` is `_v537socket`'s behaviour, which is the constant
`FS_V537_SOCKET` -- i.e. TRUE on every board, which is the map-INVARIANCE this
build exists to remove.  `delta` marks the cells where v535 actually changes
something, and those cells are the dose panel's population.

⛔ BOTH VERDICTS OR IT IS NOT AN INSTRUMENT.  This table is only meaningful if
the same code can print `refuse=1` AND `refuse=0`; a column that has only ever
read one value validates anything.  The table below prints both by
construction, and `--selftest` additionally drives four mutants that MUST come
out the other way:
  1. a board too small (max dim < the v525 floor)          -> refuse
  2. cores too close (d^2 < the v525 floor)                -> refuse
  3. archipelago, a grid-CONFIRMED FS_MAP_SKIP board       -> refuse
  4. archipelago's SIGNATURE with a WRONG grid             -> RUN
     (the v534 F2 property: a bare signature hit is only a candidate)
and two flag mutants:
  5. FS_V538_CLAIM_GATE = False on a refusing board        -> claim ON
  6. FS_V537_SOCKET    = False on a running board          -> claim OFF

  .venv/bin/python .../gatemap.py [--selftest]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from harness import (FakeCt, REPO, grid_of_map, load_tree,  # noqa: E402
                     make_player, probe_claim)
from fcode import Environment, Position  # noqa: E402

CORE_VIS = 36


def maps_in_pool():
    return sorted(p.stem for p in (REPO / "maps").glob("*.map26"))


def one(mods, name, seat):
    """(refuse, claim_on) for `name` from `seat` (0 = team A anchor)."""
    w, h, grid, cores = grid_of_map(name)
    ours, theirs = (cores[0], cores[1]) if seat == 0 else (cores[1], cores[0])
    ct = FakeCt(grid, ours, CORE_VIS, Position, Environment)
    on, refuse = probe_claim(mods, w, h, Position(*ours), Position(*theirs), ct)
    return refuse, on


def table(tree="_v542wave", partree="_v537socket"):
    mods = load_tree(tree)
    par = load_tree(partree)
    rows = []
    print("%-16s %4s %7s %8s %8s  %s"
          % ("map", "seat", "refuse", "v538_on", "par_on", "delta"))
    for name in maps_in_pool():
        for seat in (0, 1):
            refuse, on = one(mods, name, seat)
            par_on = par["doctrine"].FS_V537_SOCKET
            d = "GATED-OFF" if (par_on and not on) else ""
            rows.append((name, seat, refuse, on, par_on, d))
            print("%-16s %4d %7s %8s %8s  %s"
                  % (name, seat, int(bool(refuse)), int(bool(on)),
                     int(bool(par_on)), d))
    nref = sum(1 for r in rows if r[2])
    print("\nCELLS %d | refuse %d | run %d | GATED-OFF %d"
          % (len(rows), nref, len(rows) - nref,
             sum(1 for r in rows if r[5])))
    ref_maps = sorted({r[0] for r in rows if r[2]})
    run_maps = sorted({r[0] for r in rows if not r[2]})
    print("REFUSING MAPS (%d): %s" % (len(ref_maps), ",".join(ref_maps)))
    print("RUNNING  MAPS (%d): %s" % (len(run_maps), ",".join(run_maps)))
    split = sorted(set(ref_maps) & set(run_maps))
    print("SEAT-ASYMMETRIC: %s" % (",".join(split) if split else "none"))
    return rows


def _flagged_tree(base, **over):
    """Load a tree, then poke module-level flags (IN MEMORY ONLY).

    ⛔ Legitimate here and nowhere near a shipped arm: every v538 name is a
    READ-SITE-ONLY flag (test_flagoff.py's AST scan proves no module-level
    default derives from one), so poking the module object after import reaches
    the code exactly as an arm rebuild would.  Arms that PLAY are built by
    `mkarm.sh`, which edits the definition site.
    """
    mods = load_tree(base)
    for k, v in over.items():
        for m in ("doctrine", "eco", "siege", "main"):
            if hasattr(mods[m], k):
                setattr(mods[m], k, v)
    return mods


def selftest():
    ok = True
    mods = load_tree("_v542wave")
    D = mods["doctrine"]

    def check(label, got, want):
        nonlocal ok
        if got != want:
            ok = False
            print("[FAIL] %s: got %r want %r" % (label, got, want))
        else:
            print("[ok] %s: %r" % (label, got))

    # --- 1/2. the geometric floors, on synthetic boards -------------------
    tiny = tuple("." * 8 for _ in range(8))
    ct = FakeCt(tiny, (1, 1), CORE_VIS, Position, Environment)
    on, refuse = probe_claim(mods, 8, 8, Position(1, 1), Position(6, 6), ct)
    check("mutant 1 (8x8 board, under min dim) refuses", bool(refuse), True)
    check("mutant 1 claim stands down", on, False)

    big = tuple("." * 30 for _ in range(30))
    ct = FakeCt(big, (10, 10), CORE_VIS, Position, Environment)
    on, refuse = probe_claim(mods, 30, 30, Position(10, 10), Position(11, 11), ct)
    check("mutant 2 (cores d^2=2) refuses", bool(refuse), True)

    #     ... and the SAME board with the cores apart must RUN, or the floor
    #     test above would pass on a predicate that refuses everything.
    ct = FakeCt(big, (2, 2), CORE_VIS, Position, Environment)
    on, refuse = probe_claim(mods, 30, 30, Position(2, 2), Position(27, 27), ct)
    check("control (30x30 open, cores far) RUNS", bool(refuse), False)
    check("control claim stays ON", on, True)

    # --- 3. archipelago: a grid-CONFIRMED FS_MAP_SKIP board ---------------
    refuse, on = one(mods, "archipelago", 0)
    check("mutant 3 archipelago refuses", bool(refuse), True)
    check("mutant 3 archipelago claim stands down", on, False)

    # --- 4. archipelago's SIGNATURE, WRONG grid -> must RUN (v534 F2) -----
    w, h, grid, cores = grid_of_map("archipelago")
    flat = tuple("." * w for _ in range(h))
    ct = FakeCt(flat, cores[0], CORE_VIS, Position, Environment)
    on, refuse = probe_claim(mods, w, h, Position(*cores[0]),
                             Position(*cores[1]), ct)
    check("mutant 4 (arch signature, flat grid) RUNS", bool(refuse), False)
    check("mutant 4 claim stays ON", on, True)

    # --- 5. FS_V538_CLAIM_GATE = False on a REFUSING board ----------------
    off = _flagged_tree("_v542wave", FS_V538_CLAIM_GATE=False)
    refuse_off, on_off = one(off, "archipelago", 0)
    check("mutant 5 gate-off: claim ON on a refusing board", on_off, True)
    check("mutant 5 gate-off: refusal never computed (cache stays None)",
          refuse_off, None)

    # --- 6. FS_V537_SOCKET = False on a RUNNING board ---------------------
    coff = _flagged_tree("_v542wave", FS_V537_SOCKET=False)
    refuse_c, on_c = one(coff, "nordkap", 0)
    check("mutant 6 socket-off: claim OFF on a running board", on_c, False)
    check("mutant 6 socket-off: gate never consulted (cache stays None)",
          refuse_c, None)

    # --- 7. the PARENT is map-invariant: the claim is ON everywhere -------
    par = load_tree("_v537socket")
    check("parent FS_V537_SOCKET is the whole predicate",
          par["doctrine"].FS_V537_SOCKET, True)

    # --- 8. the cache is a CACHE: second call does not recompute ----------
    w, h, grid, cores = grid_of_map("archipelago")
    ct = FakeCt(grid, cores[0], CORE_VIS, Position, Environment)
    p = make_player(mods, w, h, Position(*cores[0]), Position(*cores[1]))
    p._v538_claim_on(ct)
    n1 = ct.n_env + ct.n_bld
    p._v538_claim_on(ct)
    n2 = ct.n_env + ct.n_bld
    check("mutant 8 second call costs 0 extra tile reads", n2 - n1, 0)
    check("mutant 8 first call DID read tiles (so 0 above means cached)",
          n1 > 0, True)

    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        raise SystemExit(selftest())
    table()
