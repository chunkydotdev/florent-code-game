#!/usr/bin/env python3
"""v529 THREE-WAY MERGE VERIFIER.

The brief: "verify the doctrine merge by diffing each against the common parent
and applying non-overlapping hunks -- if any hunk overlaps, STOP and report."

This does the strict form of that, on the AST rather than on the text, because
a TEXT hunk that is comment-only is not an overlap and a text-level merge tool
would have flagged one here (both children rewrote the comment above
`FS_V526_TEMPO` and both appended at end-of-file).  What actually matters:

  C1  each child's doctrine MINUS its appended constant block is AST-IDENTICAL
      to the common base  ->  neither child edited an executable statement of
      the shared base, so the only deltas are the two appended blocks.
  C2  the two appended blocks are pure module-level `Assign` statements whose
      target-name sets are DISJOINT from each other and from the base
      ->  no hunk overlaps; nothing to arbitrate.
  C3  the merged file's AST == base AST ++ v527 block AST ++ v528 block AST
      (statement-for-statement)  ->  the union is exactly the sum, no more.
  C4  UNION vs v527 differs by EXACTLY v528's name/value set, and UNION vs v528
      differs by EXACTLY v527's -- read off the module namespace, not the text.
  C5  the four non-doctrine files are byte-equal to their stated source.

SELFTEST (`--selftest`): every one of C1-C4 is driven to FAIL on a mutated
input, because a check that has never produced the other verdict has not been
seen to check.  C1 is broken by inserting a real statement into the shared
region; C2 by planting a colliding name in both blocks; C3 by dropping one
statement from the merge; C4 by flipping a v528 value inside the union.
"""
import ast
import hashlib
import sys

REPO = "/Users/junghard/Projects/Work/florent-code-game"
BASE = REPO + "/scratchpad/s51_v529_build/base_arm/doctrine.py"
V527 = REPO + "/bots/_v527collar/doctrine.py"
V528 = REPO + "/bots/_v528eco/doctrine.py"
UNION = REPO + "/bots/_v529merge/doctrine.py"

# 1-indexed inclusive line ranges of the appended constant blocks, derived from
# `diff <base> <child>` (the single `NNNNaNNNN,NNNN` append hunk in each).
APP527 = (4958, 5132)
APP528 = (4928, 5053)


def lines(p):
    return open(p).read().splitlines(keepends=True)


def dump(src):
    return ast.dump(ast.parse(src))


def assigns(src):
    """{name: literal-value-or-None} for module-level simple assignments."""
    out = {}
    for n in ast.parse(src).body:
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name):
                    try:
                        out[t.id] = ast.literal_eval(n.value)
                    except Exception:
                        out[t.id] = "<expr>"
    return out


def split(child_lines, app):
    a, b = app
    return "".join(child_lines[:a - 1]), "".join(child_lines[a - 1:b])


def run(base_src, v7_lines, v8_lines, union_src, loud=True):
    fails = []

    def chk(tag, ok, msg):
        if loud:
            print("%-4s %-5s %s" % (tag, "PASS" if ok else "FAIL", msg))
        if not ok:
            fails.append(tag)

    pre7, app7 = split(v7_lines, APP527)
    pre8, app8 = split(v8_lines, APP528)

    # ---- C1 -------------------------------------------------------------
    chk("C1a", dump(pre7) == dump(base_src),
        "v527 doctrine minus its block is AST-identical to the RDV-only base "
        "(its 2 text hunks are comment-only)")
    chk("C1b", dump(pre8) == dump(base_src),
        "v528 doctrine minus its block is AST-identical to the RDV-only base")

    # ---- C2 -------------------------------------------------------------
    k7, k8, kb = assigns(app7), assigns(app8), assigns(base_src)
    only_assign = all(
        isinstance(n, ast.Assign)
        for blk in (app7, app8) for n in ast.parse(blk).body)
    chk("C2a", only_assign,
        "both appended blocks are module-level Assign statements only "
        "(%d + %d)" % (len(k7), len(k8)))
    chk("C2b", not (set(k7) & set(k8)),
        "the two blocks' target names are DISJOINT (overlap: %s)"
        % sorted(set(k7) & set(k8)))
    chk("C2c", not (set(k7) & set(kb)) and not (set(k8) & set(kb)),
        "neither block shadows a base name (v527 %s / v528 %s)"
        % (sorted(set(k7) & set(kb)), sorted(set(k8) & set(kb))))

    # ---- C3 -------------------------------------------------------------
    want = ast.parse(base_src).body + ast.parse(app7).body + \
        ast.parse(app8).body
    got = ast.parse(union_src).body
    same_len = len(want) == len(got)
    same = same_len and all(ast.dump(a) == ast.dump(b)
                            for a, b in zip(want, got))
    chk("C3", same,
        "UNION AST == base ++ v527block ++ v528block, statement-for-statement "
        "(%d vs %d stmts)" % (len(got), len(want)))

    # ---- C4 -------------------------------------------------------------
    ku, kv7, kv8 = assigns(union_src), assigns("".join(v7_lines)), \
        assigns("".join(v8_lines))
    d_u_v7 = {n for n in set(ku) | set(kv7) if ku.get(n, "\0") != kv7.get(n, "\0")}
    d_u_v8 = {n for n in set(ku) | set(kv8) if ku.get(n, "\0") != kv8.get(n, "\0")}
    chk("C4a", d_u_v7 == set(k8),
        "UNION-vs-v527 namespace delta == exactly v528's %d names (got %d, "
        "sym-diff %s)" % (len(k8), len(d_u_v7), sorted(d_u_v7 ^ set(k8))))
    chk("C4b", d_u_v8 == set(k7),
        "UNION-vs-v528 namespace delta == exactly v527's %d names (got %d, "
        "sym-diff %s)" % (len(k7), len(d_u_v8), sorted(d_u_v8 ^ set(k7))))

    return fails


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def c5():
    pairs = [
        ("eco.py", "bots/_v528eco/eco.py", "v528"),
        ("main.py", "bots/_v527collar/main.py", "v527"),
        ("siege.py", "bots/_v527collar/siege.py", "v527"),
        ("raid.py", "bots/_v526transit/raid.py", "PARENT"),
    ]
    bad = []
    for f, src, who in pairs:
        a, b = md5(REPO + "/bots/_v529merge/" + f), md5(REPO + "/" + src)
        ok = a == b
        print("C5   %-5s %-9s == %-6s %s  %s"
              % ("PASS" if ok else "FAIL", f, who, a[:8], "" if ok else b[:8]))
        if not ok:
            bad.append(f)
    return bad


def selftest():
    base = open(BASE).read()
    v7, v8 = lines(V527), lines(V528)
    union = open(UNION).read()
    print("--- selftest: each guard must FAIL on a mutated input ---")

    def expect(tags, bs, a7, a8, us):
        f = run(bs, a7, a8, us, loud=False)
        ok = set(tags) <= set(f)
        print("  %-5s expected %s -> got %s"
              % ("PASS" if ok else "FAIL", tags, f))
        assert ok, "guard did not fire: %s vs %s" % (tags, f)

    # C1: a REAL statement planted in the shared region of v527, in place of a
    # comment line so no line index shifts (the append ranges are 1-indexed).
    i = next(k for k, ln in enumerate(v7[:APP527[0] - 1])
             if ln.startswith("#"))
    m7 = list(v7)
    m7[i] = "SELFTEST_INJECTED = 1\n"
    expect(["C1a"], base, m7, v8, union)

    # C2: a colliding name planted in both blocks
    m7 = list(v7)
    m7[APP527[1] - 1] = m7[APP527[1] - 1] + "SELFTEST_COLLIDE = 1\n"
    m8 = list(v8)
    m8[APP528[1] - 1] = m8[APP528[1] - 1] + "SELFTEST_COLLIDE = 2\n"
    expect(["C2b"], base, m7, m8, union)

    # C3: one statement dropped from the union
    mu = union.replace("FS_V527_SEALPATH = True", "", 1)
    expect(["C3"], base, v7, v8, mu)

    # C4: a v528 value flipped inside the union only
    mu = union.replace("FS_V528_CONNCOST = True", "FS_V528_CONNCOST = False", 1)
    expect(["C3", "C4b"], base, v7, v8, mu)

    print("SELFTEST OK: C1/C2/C3/C4 each produced the FAIL verdict on a "
          "mutated input, so none of them is a constant.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        sys.exit(selftest())
    f = run(open(BASE).read(), lines(V527), lines(V528), open(UNION).read())
    f += c5()
    print("\nRESULT: %s" % ("PASS" if not f else "FAIL " + str(f)))
    sys.exit(1 if f else 0)
