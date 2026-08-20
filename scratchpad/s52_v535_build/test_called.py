#!/usr/bin/env python3
"""v535 build instrument #6 -- CALLED, NOT RE-DERIVED (D21d).

The side lane's audit question, asked of the shipped tree and answered on the
tree rather than in prose: is the ferry-siege's refusal verdict **CALLED** from
the existing verified function, or **RE-DERIVED** as a copy?

Three checks, each able to come out the other way:

1. **STRUCTURAL (AST).** `_v535_map_refuses` must CONTAIN calls to
   `_fs_map_gated` and `_fs_enemy_anchor`, and must NOT contain the tokens a
   re-derivation would need (`FS_MAP_SKIP`, the min-dim/min-dsq constants, the
   cripple lists, `known_map_for`, `read_store`, `enemy_core_for`). Driven the
   other way on `_fs_map_gated` itself, which MUST contain them -- otherwise
   the scanner is just reporting on an empty function.

2. **THE EXTRACTION IS BEHAVIOUR-PRESERVING.** `_fs_enemy_anchor` was pulled
   out of `_fs_gate` for this build, so `_fs_gate` itself changed. Its verdict
   is compared against the PARENT `_v534maptrust._fs_gate` over the whole map
   pool x both seats x three anchor states (own `self.enemy` set / only
   `SLOT_ENEMY_CORE` published / neither, i.e. the mirror fallback) -- the
   three branches the extraction spans. Any mismatch is a FAIL. Driven the
   other way by a stub whose anchor is deliberately wrong.

3. **THE READER AGREES WITH THE ORIGINAL.** On every pool cell,
   `_v535_map_refuses(ct)` must equal `not _fs_gate(ct)`. And BOTH verdicts
   must occur in that comparison, or an "always agrees" report would be a
   report about a constant.

  .venv/bin/python .../test_called.py
"""
import ast
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from harness import FakeCt, REPO, grid_of_map, load_tree, make_player  # noqa: E402
from gatemap import CORE_VIS, maps_in_pool  # noqa: E402
from fcode import Environment, Position  # noqa: E402

CHILD = "_v535cornergate"
PARENT = "_v534maptrust"
# tokens a RE-DERIVATION of the gate would necessarily contain
DERIVE_TOKENS = {"FS_MAP_SKIP", "FS_V525_MIN_MAP_DIM", "FS_V525_MIN_CORE_DSQ",
                 "FS_MIN_MAP_DIM", "FS_MIN_CORE_DSQ", "FS_V525_CRIPPLE_MAPS",
                 "FS_V519_CRIPPLE_MAPS", "FS_V524_CRIPPLE_GRIDS",
                 "known_map_for", "distance_squared"}
ANCHOR_TOKENS = {"read_store", "enemy_core_for", "unpack_pos",
                 "SLOT_ENEMY_CORE"}


def fn_source(path, name):
    tree = ast.parse(Path(path).read_text())
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name:
            return n
    raise KeyError(name)


def names_in(node):
    out = set()
    for sub in ast.walk(node):
        if isinstance(sub, ast.Name):
            out.add(sub.id)
        elif isinstance(sub, ast.Attribute):
            out.add(sub.attr)
    return out


def calls_in(node):
    out = set()
    for sub in ast.walk(node):
        if isinstance(sub, ast.Call):
            f = sub.func
            if isinstance(f, ast.Attribute):
                out.add(f.attr)
            elif isinstance(f, ast.Name):
                out.add(f.id)
    return out


def strip_docstring(node):
    """The function's BODY minus its docstring -- prose must not score."""
    body = list(node.body)
    if body and isinstance(body[0], ast.Expr) and \
            isinstance(body[0].value, ast.Constant) and \
            isinstance(body[0].value.value, str):
        body = body[1:]
    m = ast.Module(body=body, type_ignores=[])
    return m


def anchor_states(mods, w, h, ours, theirs, grid, state):
    """A (player, ct) pair in one of the three anchor states."""
    D = mods["doctrine"]
    if state == "self":
        p_enemy, store = Position(*theirs), {}
    elif state == "store":
        p_enemy, store = None, {D.SLOT_ENEMY_CORE:
                                mods["eco"].pack_pos(Position(*theirs))}
    else:                                     # mirror fallback
        p_enemy, store = None, {}
    ct = FakeCt(grid, ours, CORE_VIS, Position, Environment, store=store)
    p = make_player(mods, w, h, Position(*ours), p_enemy)
    return p, ct


def main():
    ok = True

    def check(label, got, want):
        nonlocal ok
        if got != want:
            ok = False
            print("[FAIL] %s: got %r want %r" % (label, got, want))
        else:
            print("[ok] %s: %r" % (label, got))

    sp = REPO / "bots" / CHILD / "siege.py"

    # --- 1. STRUCTURAL ----------------------------------------------------
    refuses = strip_docstring(fn_source(sp, "_v535_map_refuses"))
    gated = strip_docstring(fn_source(sp, "_fs_map_gated"))
    anchor = strip_docstring(fn_source(sp, "_fs_enemy_anchor"))
    c = calls_in(refuses)
    check("_v535_map_refuses CALLS _fs_map_gated", "_fs_map_gated" in c, True)
    check("_v535_map_refuses CALLS _fs_enemy_anchor",
          "_fs_enemy_anchor" in c, True)
    leaked = sorted(names_in(refuses) & DERIVE_TOKENS)
    check("_v535_map_refuses re-derives NO gate logic", leaked, [])
    leaked_a = sorted(names_in(refuses) & ANCHOR_TOKENS)
    check("_v535_map_refuses re-derives NO anchor logic", leaked_a, [])
    # ⛔ the scanner must be able to say the opposite, or "[] leaked" is vacuous
    check("CONTROL: _fs_map_gated DOES contain gate logic",
          len(names_in(gated) & DERIVE_TOKENS) >= 4, True)
    check("CONTROL: _fs_enemy_anchor DOES contain anchor logic",
          len(names_in(anchor) & ANCHOR_TOKENS) >= 3, True)
    # what IS local to the reader: the cache and the sign flip, nothing else
    print("    _v535_map_refuses calls: %s" % sorted(c))

    # --- 2. THE EXTRACTION IS BEHAVIOUR-PRESERVING ------------------------
    new = load_tree(CHILD)
    par = load_tree(PARENT)
    check("PARENT has no _fs_enemy_anchor (the extraction is this build's)",
          hasattr(par["siege"].SiegeMixin, "_fs_enemy_anchor"), False)
    n = 0
    mism = []
    both = set()
    for name in maps_in_pool():
        w, h, grid, cores = grid_of_map(name)
        for seat in (0, 1):
            ours, theirs = (cores[0], cores[1]) if seat == 0 else (cores[1], cores[0])
            for state in ("self", "store", "mirror"):
                n += 1
                pa, cta = anchor_states(par, w, h, ours, theirs, grid, state)
                pb, ctb = anchor_states(new, w, h, ours, theirs, grid, state)
                va, vb = pa._fs_gate(cta), pb._fs_gate(ctb)
                both.add(va)
                if va != vb:
                    mism.append((name, seat, state, va, vb))
    check("extracted _fs_gate matches the PARENT on all %d cells" % n, mism, [])
    check("...and that comparison saw BOTH verdicts", sorted(both), [False, True])

    #     driven the other way: a stub anchor that returns the WRONG core must
    #     make the comparison FAIL, or "0 mismatches" proves nothing.
    #     ⛔ THE MUTANT HAS TO BE CHOSEN ON A **RUNNING** BOARD. The first
    #     version put the fake anchor next to our own core on ARCHIPELAGO --
    #     which refuses via FS_MAP_SKIP anyway, so both arms said "refuse" and
    #     the mutant read as no-change. A mutant on a board that already gives
    #     the target verdict cannot demonstrate anything; nordkap RUNS, and a
    #     bogus anchor one tile from our core drives it under the d^2 floor.
    w, h, grid, cores = grid_of_map("nordkap")
    pa, cta = anchor_states(par, w, h, cores[0], cores[1], grid, "mirror")
    base = pa._fs_gate(cta)
    check("MUTANT precondition: nordkap RUNS for the parent", base, True)
    pb, ctb = anchor_states(new, w, h, cores[0], cores[1], grid, "mirror")
    pb._fs_enemy_anchor = lambda ct: Position(cores[0][0] + 1, cores[0][1])
    check("MUTANT: a wrong anchor changes _fs_gate's verdict",
          pb._fs_gate(ctb) != base, True)

    # --- 3. THE READER AGREES WITH THE ORIGINAL ---------------------------
    n = 0
    dis = []
    seen = set()
    for name in maps_in_pool():
        w, h, grid, cores = grid_of_map(name)
        for seat in (0, 1):
            ours, theirs = (cores[0], cores[1]) if seat == 0 else (cores[1], cores[0])
            n += 1
            p1, ct1 = anchor_states(new, w, h, ours, theirs, grid, "self")
            p2, ct2 = anchor_states(new, w, h, ours, theirs, grid, "self")
            r = p1._v535_map_refuses(ct1)
            g = p2._fs_gate(ct2)
            seen.add(bool(r))
            if bool(r) != (not g):
                dis.append((name, seat, r, g))
    check("_v535_map_refuses == not _fs_gate on all %d cells" % n, dis, [])
    check("...and BOTH refusal verdicts occurred", sorted(seen), [False, True])

    print("CALLED_NOT_DERIVED", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
