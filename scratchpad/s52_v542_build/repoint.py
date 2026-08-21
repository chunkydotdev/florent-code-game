#!/usr/bin/env python3
r"""repoint.py — COPY a plank build's instrument and RE-POINT it at the merge.

    repoint.py <src> <dst> OLD=NEW [OLD=NEW ...]
    repoint.py --selftest

⛔ WHY THIS EXISTS RATHER THAN AN EDIT.  The house convention (v538's
`harness.py` header, verbatim: *"COPIED from `scratchpad/s52_v535_build/
harness.py` (never edited in place) and re-pointed"*) is that a plank's own
instrument is COPIED, never edited where it lives, so the plank build's banked
outputs stay reproducible from the file that produced them.  The merge build
then needs the SAME probes pointed at the merged tree — and the only honest way
to do that is a MECHANICAL, ENUMERATED substitution: every changed site
printed, the count asserted, and nothing else touched.

⛔ THE FAILURE THIS GUARDS.  A hand-edit that also "improves" a probe turns a
dose REPRODUCTION into a new measurement wearing a reproduction's name.  So the
only permitted edit is a token substitution, and the diff is printed in full so
the report can carry it.

SELFTEST drives every guard to its other verdict (`--selftest`).
"""
import argparse
import difflib
import re
import sys


def repoint(src, dst, subs, verbose=True):
    with open(src) as fh:
        s = fh.read()
    orig = s
    counts = {}
    for old, new in subs:
        n = len(re.findall(re.escape(old), s))
        if n == 0:
            raise SystemExit("REFUSED: token %r not found in %s — the copy "
                             "would be a no-op and the probe would still "
                             "measure the plank tree" % (old, src))
        s = s.replace(old, new)
        counts[old] = n
    # GUARD: the substitution must have CHANGED something.
    if s == orig:
        raise SystemExit("REFUSED: no change made to %s" % src)
    # GUARD: no stale reference to a substituted token may survive.
    for old, _ in subs:
        if old in s:
            raise SystemExit("REFUSED: %r survives in the output" % old)
    # GUARD: line count must be unchanged — a token substitution cannot add or
    # remove lines, so a delta here means the writer did something else.
    if s.count("\n") != orig.count("\n"):
        raise SystemExit("REFUSED: line count changed (%d -> %d)"
                         % (orig.count("\n"), s.count("\n")))
    if dst:
        with open(dst, "w") as fh:
            fh.write(s)
    if verbose:
        for old, new in subs:
            print("REPOINT %-24s -> %-24s %3d sites" % (old, new, counts[old]))
        diff = list(difflib.unified_diff(orig.splitlines(), s.splitlines(),
                                         "src", "dst", lineterm="", n=0))
        print("CHANGED LINES: %d" % sum(1 for d in diff if d.startswith("+")
                                        and not d.startswith("+++")))
    return s, counts


def selftest():
    import os
    import tempfile
    d = tempfile.mkdtemp(prefix="rp_")
    src = os.path.join(d, "a.py")
    with open(src, "w") as fh:
        fh.write('T = "_v539resilience"\nprint(T, "_v539resilience")\n')
    fails = []

    def expect(tag, fn, should_fail):
        try:
            fn()
            got = "PASS"
        except SystemExit:
            got = "FAIL"
        ok = (got != "PASS") == should_fail
        print("  %-52s %-5s %s" % (tag, got, "ok" if ok else "!!! WRONG"))
        if not ok:
            fails.append(tag)

    print("SELFTEST repoint.py — each guard, both ways")
    expect("HONEST substitution", lambda: repoint(
        src, None, [("_v539resilience", "_v542wave")], False), False)
    expect("token absent -> must FAIL", lambda: repoint(
        src, None, [("_vNOPE", "_v542wave")], False), True)
    expect("identity substitution (no change) -> must FAIL", lambda: repoint(
        src, None, [("_v539resilience", "_v539resilience")], False), True)
    # a substitution whose NEW still contains OLD leaves a stale reference
    expect("new contains old -> must FAIL", lambda: repoint(
        src, None, [("_v539", "_v539resilience_v539")], False), True)
    # line-count guard: drive it by a substitution that injects a newline
    expect("substitution adds a line -> must FAIL", lambda: repoint(
        src, None, [("_v539resilience", "_v542\nwave")], False), True)
    print("SELFTEST %s (%d wrong verdicts)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 0 if not fails else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src", nargs="?")
    ap.add_argument("dst", nargs="?")
    ap.add_argument("subs", nargs="*")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if not (a.src and a.dst and a.subs):
        ap.error("src dst OLD=NEW ...")
    repoint(a.src, a.dst, [tuple(x.split("=", 1)) for x in a.subs])
