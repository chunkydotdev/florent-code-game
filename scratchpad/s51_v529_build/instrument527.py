#!/usr/bin/env python3
"""Inject the v527 SEALED-AND-TURRETLESS tape into a COPY of a bot tree.

THE METRIC THIS EXISTS FOR.  Magnus's markers 6 and 14 both show one signature:
a SEALED enemy core with NO turret on it, held for hundreds of rounds.  The
tape counts, once per round, from the CORE (which runs exactly once per round,
so the count is rounds and not body-rounds):

    V527I SEALNT <rnd> ph <phase> fwd <SLOT_FWD_GUN> hv <harvesters>

    sealed   = FS_PH_SEALED <= ph <= FS_PH_KILL_NEAR
    turretless = fwd == 0          (monotone; survives the buyer)
    ⇒ the metric is the count of rounds with sealed AND turretless.

`hv` rides along because `FS_V527_PSURV_EXTRA` spends BODIES, and the v526 M6
lesson is that buying anything with an eco seat costs `harv30` (2.34 -> 1.98)
and -10.83pp on `k<=200`.  The non-regression check is this plank's own
falsifier, so it is measured on the same line rather than in a separate battery.

⛔ EVERY substitution asserts its own match count (the v526 lesson: a patcher
that silently matched nothing produced a tape that read 0 and looked like a
finding).  The anchor is chosen to exist IDENTICALLY in the parent and the
child -- `_core`'s opening, which neither tree touches.

Usage: instrument527.py <tree-dir>
"""
import sys
from pathlib import Path

MARK = "# --- s51 v527 SEALNT TAPE ---"

ANCHOR = """        rnd = ct.get_current_round()

        # --- threat latch -------------------------------------------------
"""

INJECT = """        rnd = ct.get_current_round()

        if V527I:
            try:
                _i_b, _i_ph, _i_r = self._fs_state(ct)
                print('V527I SEALNT', rnd,
                      'ph', _i_ph,
                      'fwd', ct.read_store(SLOT_FWD_GUN),
                      'hv', ct.read_store(SLOT_HARVESTERS),
                      file=sys.stderr)
            except Exception as _e:
                print('V527I ERR', rnd, repr(_e), file=sys.stderr)

        # --- threat latch -------------------------------------------------
"""


def sub(s, old, new, n=1):
    got = s.count(old)
    assert got == n, "expected %d matches, got %d for:\n%r" % (n, got, old[:160])
    return s.replace(old, new)


def patch(tree):
    tree = Path(tree)
    assert tree.is_dir(), tree

    d = (tree / "doctrine.py").read_text()
    assert MARK not in d, "already instrumented: %s" % tree
    d += "\n\n" + MARK + "\nV527I = True\n"
    (tree / "doctrine.py").write_text(d)

    m = (tree / "main.py").read_text()
    m = sub(m, ANCHOR, INJECT)
    (tree / "main.py").write_text(m)

    # ⛔ THE TAPE MUST NOT BE SWALLOWED.  main.py imports sys at module level in
    # both trees; assert it rather than assuming it (the v526 WALK tape emitted
    # 0 lines for exactly this reason -- a NameError inside a bare except).
    assert "\nimport sys" in m or m.startswith("import sys"), \
        "main.py does not import sys; the tape would be swallowed"
    print("instrumented:", tree)


if __name__ == "__main__":
    patch(sys.argv[1])
