#!/usr/bin/env python3
"""s54 v536trustport verification -- DRIVES SiegeMixin._fs_map_gated DIRECTLY.

This is a NEW script, parameterised by tree, NOT an edit of
`scratchpad/s52_v535_build/gatemap.py`.  Why not reuse that file as-is: it
does not take a tree argument (`table()`/`selftest()` both hardcode
`_v535cornergate`/`_v534maptrust`) and it drives `_v535_corners_on` ->
`_v535_map_refuses` -> `_fs_map_gated`, a wrapper that ONLY EXISTS in
`_v535cornergate` (verified: `grep -c _v535_corners_on` is 0 in
_v529merge/_v533home/_v534maptrust/_v536trustport, 7 in _v535cornergate's
eco.py). So it is not directly reusable across the five trees this task
compares. What IS reusable, unedited, is `scratchpad/s52_v535_build/harness.py`
-- its `load_tree`, `grid_of_map`, `FakeCt` and (unused by gatemap.py itself)
`probe_gate` helper, which calls `SiegeMixin._fs_map_gated` on a bare stand-in
object and is exactly the shipped predicate named in this task. This script
imports harness.py from its original location and does not modify it.

  .venv/bin/python gatemap_v536.py <tree> [--selftest]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
S52 = HERE.parent / "s52_v535_build"
sys.path.insert(0, str(S52))
from harness import FakeCt, REPO, grid_of_map, load_tree, probe_gate  # noqa: E402
from fcode import Environment, Position  # noqa: E402

CORE_VIS = 36

POOL_15 = sorted((
    "auroraveil", "bifrost", "fimbulwinter", "glacierkeep", "helheim",
    "holmgang", "icefloe", "jotunheim", "longhouse", "midgard",
    "paths", "skald", "stavkirke", "valkyrie", "yggdrasil",
))  # ROTATED POOL 2026-08-21 (fcode maps list)  # tools/overnight.sh:68, live 15-map pool since the 2026-08-13 rotation


def all_maps():
    return sorted(p.stem for p in (REPO / "maps").glob("*.map26"))


def one(mods, name, seat):
    """(refuse: bool) for `name` from `seat` (0 = team A anchor)."""
    w, h, grid, cores = grid_of_map(name)
    ours, theirs = (cores[0], cores[1]) if seat == 0 else (cores[1], cores[0])
    ct = FakeCt(grid, ours, CORE_VIS, Position, Environment)
    ok = probe_gate(mods, w, h, Position(*ours), Position(*theirs), ct)
    return not ok


def table(tree):
    mods = load_tree(tree, want=("doctrine", "eco", "siege", "raid", "main"))
    rows = []
    print("%-16s %4s %7s" % ("map", "seat", "refuse"))
    for name in all_maps():
        for seat in (0, 1):
            refuse = one(mods, name, seat)
            rows.append((name, seat, refuse))
            print("%-16s %4d %7s" % (name, seat, int(bool(refuse))))
    nref = sum(1 for r in rows if r[2])
    print("\nCELLS %d | refuse %d | run %d" % (len(rows), nref, len(rows) - nref))
    ref_maps = sorted({r[0] for r in rows if r[2]})
    run_maps = sorted({r[0] for r in rows if not r[2]})
    print("REFUSING MAPS (%d): %s" % (len(ref_maps), ",".join(ref_maps)))
    print("RUNNING  MAPS (%d): %s" % (len(run_maps), ",".join(run_maps)))
    split = sorted(set(ref_maps) & set(run_maps))
    print("SEAT-ASYMMETRIC: %s" % (",".join(split) if split else "none"))

    pool_rows = [r for r in rows if r[0] in POOL_15]
    pool_ref = [r for r in pool_rows if r[2]]
    pool_ref_maps = sorted({r[0] for r in pool_ref})
    print("\nPOOL CELLS %d | POOL refuse %d | POOL run %d"
          % (len(pool_rows), len(pool_ref), len(pool_rows) - len(pool_ref)))
    print("POOL REFUSING MAPS (%d of %d): %s"
          % (len(pool_ref_maps), len(POOL_15), ",".join(pool_ref_maps)))
    print("POOL REFUSING ROW FRACTION: %d/%d = %.4f%%"
          % (len(pool_ref), len(pool_rows),
             100.0 * len(pool_ref) / len(pool_rows)))
    return rows


def diff(tree_a, tree_b):
    """Cell-for-cell diff of _fs_map_gated's refuse verdict, tree_a vs tree_b."""
    mods_a = load_tree(tree_a, want=("doctrine", "eco", "siege", "raid", "main"))
    mods_b = load_tree(tree_b, want=("doctrine", "eco", "siege", "raid", "main"))
    rows = []
    for name in all_maps():
        for seat in (0, 1):
            ra = one(mods_a, name, seat)
            rb = one(mods_b, name, seat)
            rows.append((name, seat, ra, rb))
    total = len(rows)
    diffs = [r for r in rows if r[2] != r[3]]
    print("%s vs %s: %d/%d cells differ" % (tree_a, tree_b, len(diffs), total))
    for name, seat, ra, rb in diffs:
        pool_flag = "IN-POOL" if name in POOL_15 else "off-pool"
        print("  DIFF map=%-14s seat=%d  %s=refuse:%d  %s=refuse:%d  %s"
              % (name, seat, tree_a, int(ra), tree_b, int(rb), pool_flag))
    in_pool_diffs = [r for r in diffs if r[0] in POOL_15]
    print("  of which IN-POOL: %d" % len(in_pool_diffs))
    return diffs


def _flagged_tree(base, **over):
    """Load a tree, then poke module-level flags (IN MEMORY ONLY).

    Same pattern as `scratchpad/s52_v535_build/gatemap.py`'s `_flagged_tree`:
    every LOKI_FS_*/FS_* name here is a read-site-only flag brought into
    `siege`'s namespace via `from doctrine import *`, so poking the module
    object after import reaches the code exactly as an arm rebuild would.
    """
    mods = load_tree(base, want=("doctrine", "eco", "siege", "raid", "main"))
    for k, v in over.items():
        for m in ("doctrine", "eco", "siege", "main"):
            if hasattr(mods[m], k):
                setattr(mods[m], k, v)
    return mods


def selftest(tree):
    ok = True

    def check(label, got, want):
        nonlocal ok
        if got != want:
            ok = False
            print("[FAIL] %s: got %r want %r" % (label, got, want))
        else:
            print("[ok] %s: %r" % (label, got))

    mods = load_tree(tree, want=("doctrine", "eco", "siege", "raid", "main"))

    # --- 1. tiny board (max dim < the v525 floor) -> refuse ---------------
    tiny = tuple("." * 8 for _ in range(8))
    ct = FakeCt(tiny, (1, 1), CORE_VIS, Position, Environment)
    okv = probe_gate(mods, 8, 8, Position(1, 1), Position(6, 6), ct)
    check("mutant 1 (8x8 board, under v525 min dim) refuses", not okv, True)

    # --- 2. cores at d^2=2 on a 30x30 -> refuse ----------------------------
    big = tuple("." * 30 for _ in range(30))
    ct = FakeCt(big, (10, 10), CORE_VIS, Position, Environment)
    okv = probe_gate(mods, 30, 30, Position(10, 10), Position(11, 11), ct)
    check("mutant 2 (cores d^2=2 on 30x30) refuses", not okv, True)

    # --- control: same open 30x30, cores apart -> RUN ----------------------
    ct = FakeCt(big, (2, 2), CORE_VIS, Position, Environment)
    okv = probe_gate(mods, 30, 30, Position(2, 2), Position(27, 27), ct)
    check("control (30x30 open, cores apart) RUNS", not okv, False)

    # --- 3. archipelago (grid-confirmed FS_MAP_SKIP board) -> refuse ------
    w, h, grid, cores = grid_of_map("archipelago")
    ct = FakeCt(grid, cores[0], CORE_VIS, Position, Environment)
    okv = probe_gate(mods, w, h, Position(*cores[0]), Position(*cores[1]), ct)
    check("mutant 3 archipelago refuses", not okv, True)

    # --- 4. FS_MAP_SKIP_ON=False -> archipelago RUNS -----------------------
    off = _flagged_tree(tree, FS_MAP_SKIP_ON=False)
    ct = FakeCt(grid, cores[0], CORE_VIS, Position, Environment)
    okv = probe_gate(off, w, h, Position(*cores[0]), Position(*cores[1]), ct)
    check("mutant 4 FS_MAP_SKIP_ON=False: archipelago RUNS", not okv, False)

    # --- 5. LOKI_FS_V525=False -> fjordgate REFUSES ------------------------
    w2, h2, grid2, cores2 = grid_of_map("fjordgate")
    v525off = _flagged_tree(tree, LOKI_FS_V525=False)
    ct = FakeCt(grid2, cores2[0], CORE_VIS, Position, Environment)
    okv = probe_gate(v525off, w2, h2, Position(*cores2[0]), Position(*cores2[1]), ct)
    check("mutant 5 LOKI_FS_V525=False: fjordgate REFUSES", not okv, True)

    # --- 6. LOAD-BEARING: archipelago's SIGNATURE, FLAT (non-matching) grid
    #        -> must RUN if the v534 F2 grid-confirm is live on this chassis.
    flat = tuple("." * w for _ in range(h))
    ct = FakeCt(flat, cores[0], CORE_VIS, Position, Environment)
    okv = probe_gate(mods, w, h, Position(*cores[0]), Position(*cores[1]), ct)
    check("mutant 6 (archipelago SIG + FLAT grid) RUNS [v534 F2 grid-confirm]",
          not okv, False)

    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    args = sys.argv[1:]
    do_selftest = "--selftest" in args
    positional = [a for a in args if not a.startswith("--")]
    if positional and positional[0] == "diff":
        diff(positional[1], positional[2])
    elif do_selftest:
        tree = positional[0] if positional else "_v536trustport"
        raise SystemExit(selftest(tree))
    else:
        tree = positional[0] if positional else "_v536trustport"
        table(tree)
