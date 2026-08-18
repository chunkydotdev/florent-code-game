#!/usr/bin/env python3
"""NO NEW DERIVED DEFAULTS: AST-scan doctrine.py for module-level assignments
whose right-hand side reads any v516 flag.

v515 finding 3: `mkarm.sh` APPENDS arm overrides to the end of doctrine.py, so
any module-level `X = f(FLAG)` is evaluated against the flag value the module
body saw, not the arm's.  The required count for the v516 flags is ZERO.

GUARD (driven both ways, per branch): a synthetic module with one such
assignment MUST be reported, and the same module with the assignment removed
MUST NOT be.  Also re-runs the scan for the v515 flag set, which is documented
to have exactly ONE remaining instance (FERRY_HOME_ON reads FS_CREW_ON) -- that
positive control is what proves the scanner is not blind to the real thing.
"""
from __future__ import annotations

import ast
import sys

V516 = {"LOKI_FS_V516", "FS_V516_TEARDOWN", "FS_V516_HOLD_GENERAL",
        "FS_V516_IDLE_ON", "FS_V516_IDLE_TTL", "FS_V516_IDLE_OWN_DSQ",
        "FS_V516_FERRY_READSITE", "FS_V516_GLOBALSENT", "FS_V516_SENTREACH"}
V515 = {"LOKI_FS_V515", "FS_V515_DOOR_OFF", "FS_V515_GATE_OR", "FS_V515_REACH"}
CREW = {"FS_CREW_ON", "LOKI_FS_CREW"}


def scan(src: str, names: set) -> list:
    tree = ast.parse(src)
    hits = []
    for node in tree.body:                       # MODULE LEVEL ONLY
        targets = None
        if isinstance(node, ast.Assign):
            targets, value = node.targets, node.value
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            targets, value = [node.target], node.value
        elif isinstance(node, (ast.If, ast.Try, ast.For, ast.While)):
            # a module-level conditional whose TEST reads a flag is the same
            # hazard even if the assignment is nested inside it
            test = getattr(node, "test", None)
            if test is not None:
                for n in ast.walk(test):
                    if isinstance(n, ast.Name) and n.id in names:
                        hits.append((node.lineno, "<conditional block>", n.id))
            continue
        else:
            continue
        for n in ast.walk(value):
            if isinstance(n, ast.Name) and n.id in names:
                tn = [t.id for t in targets if isinstance(t, ast.Name)]
                hits.append((node.lineno, ",".join(tn) or "?", n.id))
    return hits


GUARD_POS = "LOKI_FS_V516 = True\nX = LOKI_FS_V516 and 3\n"
GUARD_NEG = "LOKI_FS_V516 = True\nX = 3\n"
GUARD_IF = "LOKI_FS_V516 = True\nif LOKI_FS_V516:\n    X = 3\n"


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else \
        "bots/_v516teardown/doctrine.py"
    ok = True
    if not scan(GUARD_POS, V516):
        print("GUARD FAIL: positive control not reported"); ok = False
    if scan(GUARD_NEG, V516):
        print("GUARD FAIL: negative control reported"); ok = False
    if not scan(GUARD_IF, V516):
        print("GUARD FAIL: module-level `if FLAG:` not reported"); ok = False
    print("GUARD: pos=%s neg=%s if=%s" %
          (bool(scan(GUARD_POS, V516)), bool(scan(GUARD_NEG, V516)),
           bool(scan(GUARD_IF, V516))))
    src = open(path).read()
    h516 = scan(src, V516)
    hcrew = scan(src, CREW)
    print("v516 derived defaults: %d %s" % (len(h516), h516))
    print("REAL-CASE CONTROL (FS_CREW_ON readers, the known v515 hazard): "
          "%d %s" % (len(hcrew), hcrew))
    if h516:
        ok = False
    if not hcrew:
        print("GUARD FAIL: the known FERRY_HOME_ON instance was not found -- "
              "the scanner cannot see the real defect class")
        ok = False
    print("RESULT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
