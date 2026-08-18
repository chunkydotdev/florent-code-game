#!/usr/bin/env python3
"""FLAG-OFF STRUCTURAL CHECK, part 1: constants.

Imports the parent's doctrine and a v515 arm's doctrine in separate passes and
reports every constant the parent has whose value differs.  With
`LOKI_FS_V515 = False` the answer must be EMPTY.

⛔ DRIVEN TO THE OTHER VERDICT IN THE SAME RUN by `m_door`, an arm that sets
`FS_LOG = True` (a constant the parent also has), which MUST report a
difference.  The FIRED arm is deliberately NOT the positive control: after the
door decision moved from a doctrine-level derived default to the read site in
`main.py`, the fired arm's CONSTANTS are identical to the parent's and only its
CODE PATHS differ -- so a constants check cannot see the plank at all, and using
it as the control would have made this a constant column.  That is the finding,
not a workaround.
"""
import importlib
import os
import sys


def load(d):
    sys.path.insert(0, d)
    for m in ("doctrine", "eco", "raid", "siege", "main"):
        sys.modules.pop(m, None)
    import doctrine
    importlib.reload(doctrine)
    out = {k: v for k, v in vars(doctrine).items()
           if k.isupper() and isinstance(v, (int, float, str, bool, type(None)))}
    sys.path.pop(0)
    return out


def main():
    S = os.path.abspath(sys.argv[1])
    par = load(os.path.join(S, "parent514"))
    ok = True
    for arm, expect in (("flagoff", "EMPTY"), ("v515", "EMPTY"),
                        ("m_door", "NONEMPTY")):
        a = load(os.path.join(S, arm))
        diffs = {k: (par[k], a[k]) for k in par if k in a and par[k] != a[k]}
        miss = [k for k in par if k not in a]
        verdict = "EMPTY" if (not diffs and not miss) else "NONEMPTY"
        print("%-8s vs parent: differing %d %s   missing %d   -> %s (expected %s)"
              % (arm, len(diffs), diffs if diffs else "", len(miss), verdict,
                 expect))
        ok = ok and verdict == expect
    print("GUARD DRIVEN BOTH WAYS:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
