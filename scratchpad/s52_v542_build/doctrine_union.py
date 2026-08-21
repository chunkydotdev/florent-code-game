#!/usr/bin/env python3
r"""doctrine_union.py — RESOLVE THE ONE TEXTUAL CONFLICT OF THE v542 MERGE.

    doctrine_union.py --base B --side S1 [--side S2 ...] --out OUT
    doctrine_union.py --selftest

THE CONFLICT.  All three planks (v538, v539, v541) append their constant block
to the END of `doctrine.py`, at the identical anchor line.  `git merge-file`
CANNOT resolve a both-added-at-EOF hunk — there is no context after it to
disambiguate the order — so it conflicts, correctly.  The conflict is TEXTUAL
POSITION ONLY; the three blocks assign disjoint names.

⛔ THE RESOLUTION IS NOT "CONCATENATE AND HOPE".  This script REFUSES unless it
can prove, for each side:

  P1  the side's file is EXACTLY `base` followed by a tail — i.e. the side did
      not touch a single byte of the shared region.  (If a side ever edits a
      base line, P1 fails and the merge must be arbitrated by hand.)
  P2  the tail parses, at module level, to ASSIGNMENTS ONLY (comments and
      blank lines are not statements).  A tail containing a def/if/import
      would make ORDER load-bearing and this resolution invalid.
  P3  the tails' assigned NAMES are pairwise DISJOINT.
  P4  no tail SHADOWS a name already bound at module level in `base`.

and then, on the produced union:

  P5  union bytes == base ++ tail1 ++ tail2 ++ ...  (trivially true by
      construction; asserted anyway so a future edit to the writer is caught)
  P6  union's module-level AST == base's ++ each tail's, statement for
      statement, in order.
  P7  union's module-level NAMESPACE == base's ∪ every tail's, and each name's
      VALUE NODE is the one its own side wrote (dumped and compared).

⭐ P7 IS THE ONE THAT MATTERS AND P3 ALONE DOES NOT IMPLY IT.  Disjoint names
say no side overwrites another's constant; P7 says the union actually CARRIES
each side's value rather than the base's or a sibling's.

SELFTEST — every guard driven to its OTHER verdict, per guard, per branch
(`--selftest`).  A check that has never failed has not been seen to check.
"""
import argparse
import ast
import sys


def read(p):
    with open(p, "rb") as fh:
        return fh.read()


def split_tail(base_b, side_b, name):
    """P1: side must be base ++ tail.  Returns tail bytes."""
    if not side_b.startswith(base_b):
        raise SystemExit(
            "P1 FAIL %s: side is not a pure append onto base "
            "(first %d bytes differ somewhere)" % (name, len(base_b)))
    return side_b[len(base_b):]


def module_stmts(src_b):
    return ast.parse(src_b.decode()).body


def assign_names(stmts):
    """Module-level names bound by Assign/AnnAssign/Aug... plus def/class."""
    out = []
    for s in stmts:
        if isinstance(s, ast.Assign):
            for t in s.targets:
                if isinstance(t, ast.Name):
                    out.append(t.id)
                else:
                    out.append("<non-name-target>")
        elif isinstance(s, ast.AnnAssign) and isinstance(s.target, ast.Name):
            out.append(s.target.id)
        elif isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            out.append(s.name)
        elif isinstance(s, (ast.Import, ast.ImportFrom)):
            for a in s.names:
                out.append(a.asname or a.name.split(".")[0])
    return out


def check_tail_assign_only(stmts, name):
    """P2."""
    bad = [type(s).__name__ for s in stmts if not isinstance(s, ast.Assign)]
    if bad:
        raise SystemExit("P2 FAIL %s: tail has non-Assign statements %r" % (name, bad))


def value_map(stmts):
    m = {}
    for s in stmts:
        if isinstance(s, ast.Assign):
            for t in s.targets:
                if isinstance(t, ast.Name):
                    m[t.id] = ast.dump(s.value)
    return m


def build(base_p, side_ps, out_p, verbose=True):
    base_b = read(base_p)
    base_stmts = module_stmts(base_b)
    base_names = set(assign_names(base_stmts))

    tails, tail_stmts, tail_names, tail_vals = [], [], [], []
    for sp in side_ps:
        tb = split_tail(base_b, read(sp), sp)                       # P1
        st = module_stmts(base_b + tb)[len(base_stmts):]
        check_tail_assign_only(st, sp)                              # P2
        tails.append(tb)
        tail_stmts.append(st)
        tail_names.append(assign_names(st))
        tail_vals.append(value_map(st))
        if verbose:
            print("P1/P2 ok  %-28s tail %5d bytes  %2d assigns"
                  % (sp, len(tb), len(st)))

    # P3 pairwise disjoint
    for i in range(len(side_ps)):
        for j in range(i + 1, len(side_ps)):
            ov = sorted(set(tail_names[i]) & set(tail_names[j]))
            if ov:
                raise SystemExit("P3 FAIL: %s and %s both assign %r"
                                 % (side_ps[i], side_ps[j], ov))
    if verbose:
        print("P3 ok     tails pairwise disjoint")

    # P4 no shadowing of base
    for sp, nm in zip(side_ps, tail_names):
        sh = sorted(set(nm) & base_names)
        if sh:
            raise SystemExit("P4 FAIL: %s shadows base names %r" % (sp, sh))
    if verbose:
        print("P4 ok     no tail shadows a base name")

    union_b = base_b
    for tb in tails:
        union_b = union_b + tb

    # P5
    exp = base_b + b"".join(tails)
    if union_b != exp:
        raise SystemExit("P5 FAIL: union bytes != base ++ tails")

    # P6 statement-for-statement
    u_stmts = module_stmts(union_b)
    want = list(base_stmts)
    for st in tail_stmts:
        want += st
    if len(u_stmts) != len(want):
        raise SystemExit("P6 FAIL: union has %d module statements, expected %d"
                         % (len(u_stmts), len(want)))
    for k, (a, b) in enumerate(zip(u_stmts, want)):
        if ast.dump(a) != ast.dump(b):
            raise SystemExit("P6 FAIL: union statement %d differs" % k)
    if verbose:
        print("P6 ok     union AST == base ++ tails, %d statements" % len(u_stmts))

    # P7 namespace + per-name value provenance
    u_vals = value_map(u_stmts)
    b_vals = value_map(base_stmts)
    for sp, tv in zip(side_ps, tail_vals):
        for k, v in tv.items():
            if k not in u_vals:
                raise SystemExit("P7 FAIL: %s's name %s missing from union" % (sp, k))
            if u_vals[k] != v:
                raise SystemExit("P7 FAIL: union's %s is not %s's value" % (k, sp))
    for k, v in b_vals.items():
        if u_vals.get(k) != v:
            raise SystemExit("P7 FAIL: union changed base name %s" % k)
    if verbose:
        print("P7 ok     every name carries its own side's value "
              "(%d base + %d tail names)"
              % (len(b_vals), sum(len(t) for t in tail_vals)))

    if out_p:
        with open(out_p, "wb") as fh:
            fh.write(union_b)
        if verbose:
            print("WROTE     %s  %d bytes" % (out_p, len(union_b)))
    return union_b


# ---------------------------------------------------------------------------
def selftest():
    import os
    import tempfile
    d = tempfile.mkdtemp(prefix="dun_")
    P = lambda n: os.path.join(d, n)

    def w(n, s):
        with open(P(n), "w") as fh:
            fh.write(s)
        return P(n)

    base = w("base.py", "A = 1\nB = 2\n")
    s1 = w("s1.py", "A = 1\nB = 2\n\n# v1\nX = 10\nY = 11\n")
    s2 = w("s2.py", "A = 1\nB = 2\n\n# v2\nZ = 20\n")
    fails = []

    def expect(tag, fn, should_fail):
        try:
            fn()
            got = "PASS"
        except SystemExit as e:
            got = "FAIL(%s)" % str(e).split(":")[0]
        ok = (got != "PASS") == should_fail
        print("  %-46s %-16s %s" % (tag, got, "ok" if ok else "!!! WRONG VERDICT"))
        if not ok:
            fails.append(tag)

    print("SELFTEST doctrine_union.py — each guard, both ways")
    # positive: the honest case must PASS
    expect("HONEST base+s1+s2", lambda: build(base, [s1, s2], None, False), False)

    # P1: a side that edits a base line
    bad1 = w("bad1.py", "A = 99\nB = 2\n\nX = 10\n")
    expect("P1 side edits a base line -> must FAIL",
           lambda: build(base, [bad1], None, False), True)

    # P1 second branch: a side SHORTER than base
    bad1b = w("bad1b.py", "A = 1\n")
    expect("P1 side shorter than base -> must FAIL",
           lambda: build(base, [bad1b], None, False), True)

    # P2: tail with a non-Assign statement
    bad2 = w("bad2.py", "A = 1\nB = 2\n\ndef f():\n    return 1\n")
    expect("P2 tail carries a def -> must FAIL",
           lambda: build(base, [bad2], None, False), True)
    bad2b = w("bad2b.py", "A = 1\nB = 2\n\nimport os\n")
    expect("P2 tail carries an import -> must FAIL",
           lambda: build(base, [bad2b], None, False), True)

    # P3: two sides assigning the same name
    bad3 = w("bad3.py", "A = 1\nB = 2\n\nX = 77\n")
    expect("P3 two tails assign X -> must FAIL",
           lambda: build(base, [s1, bad3], None, False), True)

    # P4: a tail shadowing a base name
    bad4 = w("bad4.py", "A = 1\nB = 2\n\nA = 5\n")
    expect("P4 tail shadows base A -> must FAIL",
           lambda: build(base, [bad4], None, False), True)

    # P6/P7: mutate the writer itself.  Simulated by a monkeypatched build that
    # drops a tail statement -- the union then has fewer statements than the
    # sides promised, which is exactly the class P6 exists for.
    g = globals()
    real = g["module_stmts"]

    def dropping(src_b):
        st = real(src_b)
        return st[:-1] if len(st) > 3 else st
    g["module_stmts"] = dropping
    expect("P6 writer drops a statement -> must FAIL",
           lambda: build(base, [s1, s2], None, False), True)
    g["module_stmts"] = real

    # P7: a union whose name carries the WRONG side's value.  Drive it by
    # feeding the same name from two sides is P3; instead corrupt value_map so
    # the union's recorded value differs from the tail's.
    realv = g["value_map"]
    calls = {"n": 0}

    def flipping(stmts):
        calls["n"] += 1
        m = realv(stmts)
        if calls["n"] > 2 and "X" in m:      # only the union read
            m["X"] = "CORRUPT"
        return m
    g["value_map"] = flipping
    expect("P7 union value != side value -> must FAIL",
           lambda: build(base, [s1, s2], None, False), True)
    g["value_map"] = realv

    # and the honest case again, to prove the monkeypatches were undone
    expect("HONEST again (patches reverted)",
           lambda: build(base, [s1, s2], None, False), False)

    print("SELFTEST %s (%d wrong verdicts)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 0 if not fails else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--base")
    ap.add_argument("--side", action="append", default=[])
    ap.add_argument("--out")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if not (a.base and a.side):
        ap.error("--base and at least one --side required")
    build(a.base, a.side, a.out)
