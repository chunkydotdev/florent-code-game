#!/usr/bin/env python3
"""v543 INSTRUMENT #1 -- THE FLAG-OFF AUDIT (static half).

ADAPTED VERBATIM from `scratchpad/s53_v543_build/flagoff_audit.py` -- only the
MASTER / SUBORDINATE / FAMILY_PREFIX table and the selftest cases are renamed.
The three rules, the short-circuit semantics and the "what this cannot do"
caveat are that file's and are unchanged.

THE CLAIM UNDER TEST, stated so it can fail: with `LOKI_FS_V543 = False`,
`bots/_v543burst` must behave EXACTLY as `bots/_v542wave`.  The EMPIRICAL
half of that proof is the identity battery (flag-off arm vs frozen parent, same
seeds, NOISE_OFF, expect 0 rows differing); this file is the STATIC half, and
it exists because the identity battery can only ever exercise the boards it
happens to reach.  A subordinate flag read on a branch no fixture visits is
invisible to the battery and visible here.

THREE RULES, each mechanically checkable and each driven to BOTH verdicts by
`--selftest`:

  R1  NO DERIVED MODULE-LEVEL CONSTANT.  No module-level assignment anywhere in
      the tree may read an FS_V543_* name on its right-hand side.
      WHY IT IS NOT PARANOIA: arm construction in this repo APPENDS overrides
      to the end of doctrine.py (`mkarm.sh`), so a module-level `X = f(FLAG)`
      is evaluated against the value the module BODY saw, not the arm's -- the
      flag would read False and the derived constant would still carry the True
      value.  v515 found one real instance of this shape.

  R2  EVERY SUBORDINATE READ IS DOMINATED BY THE MASTER.  Each read of
      FS_V543_LOG / _TI_FLOOR / _KEEP_SENT / _MAX_PECKS / _RAID_ON /
      _NEED_SENTINEL must sit either
        (a) lexically inside a `def _v543_*` method (whose callers R3 checks),
            or
        (b) inside an `if`/boolean chain in which LOKI_FS_V543 appears as an
            EARLIER operand of the same `and` (Python short-circuits, so an
            earlier False operand means the later one is never evaluated), or
        (c) inside an `If` statement whose test mentions LOKI_FS_V543.

  R3  EVERY CALL INTO THE FAMILY IS GUARDED.  Every call site of a `_v543_*`
      method that is NOT itself inside a `_v543_*` method must have
      LOKI_FS_V543 as an earlier operand of the same `and` chain.
      ⛔ THIS IS THE RULE THAT MATTERS MOST, and R2(a) is worthless without it:
      "the read is inside a _v543_ method" only helps if no _v543_ method can
      run with the master off.  `_v543_supp_idle_ok` WRITES `self.fs_supp_seat`
      -- a field the PARENT reads -- so a single unguarded call would break
      identity even though it fires no weapon.

⛔ WHAT THIS FILE CANNOT DO, said plainly.  It is a LEXICAL/short-circuit
argument, not a reachability proof.  It would not catch a guard hidden behind
an intermediate variable (`g = LOKI_FS_V543; if g:`), and it does not look at
`main.py`'s unconditional per-body state INITIALISATION (three fields set to
0/-1/None), which is deliberate and is argued in the build report rather than
here: writing a field nobody reads cannot change behaviour, and the read sites
are exactly what R2/R3 enumerate.  The identity battery is the check that
covers what this one does not.

    .venv/bin/python scratchpad/s53_v543_build/flagoff_audit.py --selftest
    .venv/bin/python scratchpad/s53_v543_build/flagoff_audit.py bots/_v543burst
"""
from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

MASTER = "LOKI_FS_V543"
SUBORDINATE = {
    "FS_V543_BURST", "FS_V543_BURST_TI", "FS_V543_REARM_TI",
    "FS_V543_RISE_RNDS", "FS_V543_RISE_TI", "FS_V543_PEAK",
    "FS_V543_MIN_HARV", "FS_V543_WINDOW", "FS_V543_MAX_FIRES",
    "FS_V543_PAIR_MAX", "FS_V543_JUMP", "FS_V543_RESERVE",
    "FS_V543_AMMO", "FS_V543_AMMO_FLOOR", "FS_V543_AMMO_MAX",
    "FS_V543_LOG",
}
FAMILY_PREFIX = "_v543_"


# --------------------------------------------------------------------------
# ast helpers
# --------------------------------------------------------------------------

def _parents(tree):
    """node -> parent, for the ancestry walks below."""
    out = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            out[child] = parent
    return out


def _names(node):
    return {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}


def _guarded_by_master(node, par):
    """Is `node` short-circuit-protected by MASTER?

    Two ways, and both are the real Python semantics rather than a heuristic:
      * an ancestor `BoolOp(And)` in which MASTER appears in a STRICTLY EARLIER
        operand than the one containing `node` -- `and` short-circuits, so a
        False master means the later operand is never evaluated;
      * an ancestor `If`/`IfExp` whose TEST mentions MASTER and in whose BODY
        `node` sits.
    """
    cur = node
    while cur in par:
        parent = par[cur]
        if isinstance(parent, ast.BoolOp) and isinstance(parent.op, ast.And):
            idx = parent.values.index(cur) if cur in parent.values else None
            if idx is not None:
                for earlier in parent.values[:idx]:
                    if MASTER in _names(earlier):
                        return True
        if isinstance(parent, (ast.If, ast.IfExp)):
            # `node` must be in the BODY, not in the test's else-arm
            in_body = False
            body = parent.body if isinstance(parent, ast.If) else [parent.body]
            for stmt in body:
                if cur is stmt or cur in set(ast.walk(stmt)):
                    in_body = True
                    break
            if in_body and MASTER in _names(parent.test):
                return True
        cur = parent
    return False


def _enclosing_func(node, par):
    cur = node
    while cur in par:
        cur = par[cur]
        if isinstance(cur, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return cur.name
    return None


# --------------------------------------------------------------------------
# the three rules
# --------------------------------------------------------------------------

def audit_source(src, filename):
    """Return a list of violation strings.  Empty list == clean."""
    tree = ast.parse(src, filename=filename)
    par = _parents(tree)
    lines = src.splitlines()
    bad = []

    def loc(n):
        return f"{filename}:{getattr(n, 'lineno', '?')}"

    def text(n):
        i = getattr(n, "lineno", 0) - 1
        return lines[i].strip() if 0 <= i < len(lines) else ""

    # R1 -- module-level derived constants
    for stmt in tree.body:
        if isinstance(stmt, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            val = getattr(stmt, "value", None)
            if val is None:
                continue
            hit = {n for n in _names(val)
                   if n.startswith("FS_V543_") or n == MASTER}
            if hit:
                bad.append(f"R1 {loc(stmt)} module-level assign reads "
                           f"{sorted(hit)}: {text(stmt)}")

    # R2 -- subordinate reads
    for n in ast.walk(tree):
        if not (isinstance(n, ast.Name) and n.id in SUBORDINATE):
            continue
        if isinstance(getattr(n, "ctx", None), ast.Store):
            continue
        fn = _enclosing_func(n, par)
        if fn and fn.startswith(FAMILY_PREFIX):
            continue                       # R2(a); R3 covers its callers
        if _guarded_by_master(n, par):
            continue                       # R2(b)/(c)
        bad.append(f"R2 {loc(n)} unguarded read of {n.id} "
                   f"in {fn or '<module>'}: {text(n)}")

    # R3 -- calls into the family
    for n in ast.walk(tree):
        if not isinstance(n, ast.Call):
            continue
        f = n.func
        name = None
        if isinstance(f, ast.Attribute):
            name = f.attr
        elif isinstance(f, ast.Name):
            name = f.id
        if not (name and name.startswith(FAMILY_PREFIX)):
            continue
        enc = _enclosing_func(n, par)
        if enc and enc.startswith(FAMILY_PREFIX):
            continue                       # internal to the family
        if _guarded_by_master(n, par):
            continue
        bad.append(f"R3 {loc(n)} unguarded call to {name} "
                   f"in {enc or '<module>'}: {text(n)}")
    return bad


def audit_tree(root):
    root = Path(root)
    files = sorted(root.glob("*.py"))
    if not files:
        raise SystemExit(f"no .py files under {root}")
    allbad = []
    for f in files:
        allbad += audit_source(f.read_text(), str(f))
    return files, allbad


# --------------------------------------------------------------------------
# SELFTEST -- every rule driven to BOTH verdicts
# --------------------------------------------------------------------------

CASES = [
    # (label, source, must_fire_rule_or_None)
    ("R1 dirty: module-level derived constant",
     "LOKI_FS_V543 = True\nDERIVED = 2 if FS_V543_WINDOW else 0\n", "R1"),
    ("R1 clean: same module, constant not derived",
     "LOKI_FS_V543 = True\nDERIVED = 0\n", None),

    ("R2 dirty: bare subordinate read outside the family",
     "class C:\n    def go(self, ct):\n        if FS_V543_WINDOW:\n"
     "            return 1\n", "R2"),
    ("R2 clean-b: master is an EARLIER `and` operand",
     "class C:\n    def go(self, ct):\n"
     "        if LOKI_FS_V543 and FS_V543_WINDOW:\n"
     "            return 1\n", None),
    ("R2 dirty-order: master is a LATER `and` operand (no short-circuit)",
     "class C:\n    def go(self, ct):\n"
     "        if FS_V543_WINDOW and LOKI_FS_V543:\n"
     "            return 1\n", "R2"),
    ("R2 clean-c: nested inside `if LOKI_FS_V543:`",
     "class C:\n    def go(self, ct):\n        if LOKI_FS_V543:\n"
     "            if FS_V543_WINDOW:\n                return 1\n", None),
    ("R2 clean-a: read lives inside a _v543_ method",
     "class C:\n    def _v543_x(self, ct):\n"
     "        return FS_V543_WINDOW\n", None),

    ("R3 dirty: unguarded call into the family",
     "class C:\n    def go(self, ct):\n"
     "        if self._v543_pair(ct):\n            return 1\n", "R3"),
    ("R3 clean: guarded call into the family",
     "class C:\n    def go(self, ct):\n"
     "        if LOKI_FS_V543 and self._v543_pair(ct):\n"
     "            return 1\n", None),
    ("R3 clean: family calls family",
     "class C:\n    def _v543_a(self, ct):\n"
     "        return self._v543_b(ct)\n", None),
]


def selftest():
    ok = True
    for label, src, want in CASES:
        bad = audit_source(src, "<case>")
        fired = {b.split()[0] for b in bad}
        if want is None:
            good = not bad
        else:
            good = want in fired
        print(f"  {'PASS' if good else 'FAIL'}  {label}"
              f"  -> {sorted(fired) if fired else 'clean'}")
        ok = ok and good
    # every rule must have been driven BOTH ways
    for rule in ("R1", "R2", "R3"):
        pos = any(w == rule for _, _, w in CASES)
        neg = any(w is None for _, _, w in CASES)
        if not (pos and neg):
            print(f"  FAIL  rule {rule} not driven both ways")
            ok = False
    print("SELFTEST", "PASS" if ok else "FAIL",
          f"-- {len(CASES)} cases, 3 rules, each driven to both verdicts")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tree", nargs="?")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.tree:
        ap.error("give a tree path, or --selftest")
    files, bad = audit_tree(a.tree)
    print(f"scanned {len(files)} files under {a.tree}: "
          + ", ".join(f.name for f in files))
    if bad:
        print(f"VIOLATIONS: {len(bad)}")
        for b in bad:
            print("  " + b)
        return 1
    print("CLEAN -- R1/R2/R3 all satisfied "
          f"(master={MASTER}, {len(SUBORDINATE)} subordinate flags)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
