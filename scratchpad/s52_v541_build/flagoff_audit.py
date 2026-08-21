#!/usr/bin/env python3
"""v541 INSTRUMENT #1 -- THE FLAG-OFF AUDIT (static half).

THE CLAIM UNDER TEST, stated so it can fail: with `FS_V541_COREPECK = False`,
`bots/_v541quiet` must behave EXACTLY as `bots/_v537socket`.  The EMPIRICAL
half of that proof is the identity battery (flag-off arm vs frozen parent, same
seeds, NOISE_OFF, expect 0 rows differing); this file is the STATIC half, and
it exists because the identity battery can only ever exercise the boards it
happens to reach.  A subordinate flag read on a branch no fixture visits is
invisible to the battery and visible here.

THREE RULES, each mechanically checkable and each driven to BOTH verdicts by
`--selftest`:

  R1  NO DERIVED MODULE-LEVEL CONSTANT.  No module-level assignment anywhere in
      the tree may read an FS_V541_* name on its right-hand side.
      WHY IT IS NOT PARANOIA: arm construction in this repo APPENDS overrides
      to the end of doctrine.py (`mkarm.sh`), so a module-level `X = f(FLAG)`
      is evaluated against the value the module BODY saw, not the arm's -- the
      flag would read False and the derived constant would still carry the True
      value.  v515 found one real instance of this shape.

  R2  EVERY SUBORDINATE READ IS DOMINATED BY THE MASTER.  Each read of
      FS_V541_LOG / _TI_FLOOR / _KEEP_SENT / _MAX_PECKS / _RAID_ON /
      _NEED_SENTINEL must sit either
        (a) lexically inside a `def _v541_*` method (whose callers R3 checks),
            or
        (b) inside an `if`/boolean chain in which FS_V541_COREPECK appears as an
            EARLIER operand of the same `and` (Python short-circuits, so an
            earlier False operand means the later one is never evaluated), or
        (c) inside an `If` statement whose test mentions FS_V541_COREPECK.

  R3  EVERY CALL INTO THE FAMILY IS GUARDED.  Every call site of a `_v541_*`
      method that is NOT itself inside a `_v541_*` method must have
      FS_V541_COREPECK as an earlier operand of the same `and` chain.
      ⛔ THIS IS THE RULE THAT MATTERS MOST, and R2(a) is worthless without it:
      "the read is inside a _v541_ method" only helps if no _v541_ method can
      run with the master off.  `_v541_supp_idle_ok` WRITES `self.fs_supp_seat`
      -- a field the PARENT reads -- so a single unguarded call would break
      identity even though it fires no weapon.

⛔ WHAT THIS FILE CANNOT DO, said plainly.  It is a LEXICAL/short-circuit
argument, not a reachability proof.  It would not catch a guard hidden behind
an intermediate variable (`g = FS_V541_COREPECK; if g:`), and it does not look at
`main.py`'s unconditional per-body state INITIALISATION (three fields set to
0/-1/None), which is deliberate and is argued in the build report rather than
here: writing a field nobody reads cannot change behaviour, and the read sites
are exactly what R2/R3 enumerate.  The identity battery is the check that
covers what this one does not.

    .venv/bin/python scratchpad/s52_v541_build/flagoff_audit.py --selftest
    .venv/bin/python scratchpad/s52_v541_build/flagoff_audit.py bots/_v541quiet
"""
from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

MASTER = "FS_V541_COREPECK"
SUBORDINATE = {
    "FS_V541_LOG", "FS_V541_TI_FLOOR", "FS_V541_KEEP_SENT",
    "FS_V541_MAX_PECKS", "FS_V541_RAID_ON", "FS_V541_NEED_SENTINEL",
    "FS_V541_AMMO_AWARE", "FS_V541_AMMO_MIN",
    "FS_V541_COREFIRST", "FS_V541_IDLEPECK",
    "FS_V541_FINISH_ON", "FS_V541_FINISH_HP",
}
FAMILY_PREFIX = "_v541_"


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
            hit = {n for n in _names(val) if n.startswith("FS_V541_")}
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
     "FS_V541_COREPECK = True\nDERIVED = 2 if FS_V541_MAX_PECKS else 0\n", "R1"),
    ("R1 clean: same module, constant not derived",
     "FS_V541_COREPECK = True\nDERIVED = 0\n", None),

    ("R2 dirty: bare subordinate read outside the family",
     "class C:\n    def go(self, ct):\n        if FS_V541_MAX_PECKS:\n"
     "            return 1\n", "R2"),
    ("R2 clean-b: master is an EARLIER `and` operand",
     "class C:\n    def go(self, ct):\n"
     "        if FS_V541_COREPECK and FS_V541_MAX_PECKS:\n"
     "            return 1\n", None),
    ("R2 dirty-order: master is a LATER `and` operand (no short-circuit)",
     "class C:\n    def go(self, ct):\n"
     "        if FS_V541_MAX_PECKS and FS_V541_COREPECK:\n"
     "            return 1\n", "R2"),
    ("R2 clean-c: nested inside `if FS_V541_COREPECK:`",
     "class C:\n    def go(self, ct):\n        if FS_V541_COREPECK:\n"
     "            if FS_V541_MAX_PECKS:\n                return 1\n", None),
    ("R2 clean-a: read lives inside a _v541_ method",
     "class C:\n    def _v541_x(self, ct):\n"
     "        return FS_V541_MAX_PECKS\n", None),

    ("R3 dirty: unguarded call into the family",
     "class C:\n    def go(self, ct):\n"
     "        if self._v541_core_attack(ct):\n            return 1\n", "R3"),
    ("R3 clean: guarded call into the family",
     "class C:\n    def go(self, ct):\n"
     "        if FS_V541_COREPECK and self._v541_core_attack(ct):\n"
     "            return 1\n", None),
    ("R3 clean: family calls family",
     "class C:\n    def _v541_a(self, ct):\n"
     "        return self._v541_b(ct)\n", None),
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
