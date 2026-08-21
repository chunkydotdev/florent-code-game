#!/usr/bin/env python3
r"""poolbind.py — WHERE THE v538 CLAIM GATE BINDS ON THE **LIVE** MAP POOL.

    poolbind.py <gatemap-output.txt> [--pool tools/overnight.sh] [--selftest]

⛔ WHY THIS IS A SEPARATE FILE AND NOT A LINE IN THE REPORT.  v538's own
report intersected its 8-map refusal set with the pool as it stood on
2026-08-21 06:0xZ and got **{archipelago, midgard}**.  The organisers rotated
the pool AGAIN the same morning (`tools/overnight.sh`, commit 99b692150,
2026-08-21 08:04Z) and **archipelago left the pool**.  An intersection typed
by hand from a report written two hours earlier would have been wrong, in the
direction of overstating where the gate acts.

⛔ AND THE POOL IS READ FROM THE FILE THAT EXECUTES IT, NOT FROM A COPY.
`tools/overnight.sh:MAPS=(...)` is the line every shard actually runs; a
hand-listed pool in an instrument is a constant that can go stale silently.
The parser refuses if it cannot find exactly one live `MAPS=(...)` assignment
(the file also carries a commented OLD pool one line up — a naive grep would
match both, and picking the wrong one inverts this whole table).

SELFTEST drives every guard to BOTH verdicts.
"""
import argparse
import re
import sys


def parse_pool(path):
    """The LIVE MAPS=(...) line — exactly one, uncommented."""
    lines = open(path).read().splitlines()
    hits = [ln for ln in lines
            if re.match(r'^\s*MAPS=\(', ln)]
    if len(hits) != 1:
        raise SystemExit("REFUSED: %d uncommented MAPS=(...) lines in %s "
                         "(need exactly 1)" % (len(hits), path))
    inner = hits[0].split("(", 1)[1].rsplit(")", 1)[0]
    pool = [m for m in inner.split() if m]
    if not pool:
        raise SystemExit("REFUSED: empty pool parsed from %s" % path)
    return pool


def parse_gatemap(path):
    """(refusing_set, running_set) from a gatemap.py table."""
    txt = open(path).read()
    ref = re.search(r'^REFUSING MAPS \(\d+\): (.+)$', txt, re.M)
    run = re.search(r'^RUNNING  MAPS \(\d+\): (.+)$', txt, re.M)
    if not ref or not run:
        raise SystemExit("REFUSED: %s has no REFUSING/RUNNING summary lines "
                         "— is it a gatemap.py table?" % path)
    R = set(ref.group(1).split(","))
    U = set(run.group(1).split(","))
    if R & U:
        raise SystemExit("REFUSED: a map is both refusing and running: %r"
                         % sorted(R & U))
    if not R or not U:
        raise SystemExit("REFUSED: one side of the gate verdict is empty — "
                         "a constant column validates anything")
    return R, U


def report(gm, pool_path, verbose=True):
    R, U = parse_gatemap(gm)
    pool = parse_pool(pool_path)
    unknown = [m for m in pool if m not in R and m not in U]
    if unknown:
        raise SystemExit("REFUSED: pool maps not covered by the gatemap "
                         "table: %r — the table is stale or the maps are "
                         "missing from maps/" % unknown)
    binds = [m for m in pool if m in R]
    claims = [m for m in pool if m in U]
    if verbose:
        print("LIVE POOL (%s): %d maps" % (pool_path, len(pool)))
        print("  %s" % ",".join(sorted(pool)))
        print("GATE REFUSES over all maps/: %d" % len(R))
        print("  %s" % ",".join(sorted(R)))
        print("")
        print("⇒ ON THE LIVE POOL THE GATE BINDS ON %d MAP(S): %s"
              % (len(binds), ",".join(sorted(binds)) or "(none)"))
        print("⇒ THE r1-r4 SOCKET CLAIM STILL RUNS ON %d: %s"
              % (len(claims), ",".join(sorted(claims))))
    return binds, claims


def selftest():
    import os
    import tempfile
    d = tempfile.mkdtemp(prefix="pb_")
    P = lambda n: os.path.join(d, n)

    def w(n, s):
        open(P(n), "w").write(s)
        return P(n)

    GM = ("map seat\nCELLS 4\n"
          "REFUSING MAPS (2): midgard,saga\n"
          "RUNNING  MAPS (2): icefloe,valkyrie\n")
    SH = ("# OLD: MAPS=(icefloe saga)\n"
          "MAPS=(midgard icefloe valkyrie)\n")
    gm, sh = w("gm.txt", GM), w("sh.sh", SH)
    fails = []

    def expect(tag, fn, should_fail, want=None):
        try:
            got = fn()
            res = "PASS"
        except SystemExit:
            got, res = None, "FAIL"
        ok = (res != "PASS") == should_fail
        if ok and want is not None:
            ok = got == want
        print("  %-58s %-5s %s" % (tag, res, "ok" if ok else "!!! WRONG"))
        if not ok:
            fails.append(tag)

    print("SELFTEST poolbind.py — each guard, both ways")
    expect("HONEST: binds on {midgard}, claims on 2",
           lambda: report(gm, sh, False), False, (["midgard"],
                                                  ["icefloe", "valkyrie"]))
    # the commented-OLD-pool trap: two uncommented MAPS= lines
    sh2 = w("sh2.sh", "MAPS=(a b)\nMAPS=(c d)\n")
    expect("two live MAPS=() lines -> must FAIL",
           lambda: report(gm, sh2, False), True)
    sh3 = w("sh3.sh", "# MAPS=(midgard)\n")
    expect("no live MAPS=() line -> must FAIL",
           lambda: report(gm, sh3, False), True)
    sh4 = w("sh4.sh", "MAPS=()\n")
    expect("empty pool -> must FAIL", lambda: report(gm, sh4, False), True)
    sh5 = w("sh5.sh", "MAPS=(midgard bifrost)\n")
    expect("pool map absent from the gatemap table -> must FAIL",
           lambda: report(gm, sh5, False), True)
    gm2 = w("gm2.txt", "REFUSING MAPS (1): midgard\n"
                       "RUNNING  MAPS (1): midgard\n")
    expect("a map both refusing and running -> must FAIL",
           lambda: report(gm2, sh, False), True)
    gm3 = w("gm3.txt", "REFUSING MAPS (0): \nRUNNING  MAPS (2): icefloe,valkyrie\n")
    expect("constant column (no refusals at all) -> must FAIL",
           lambda: report(gm3, sh, False), True)
    gm4 = w("gm4.txt", "nothing here\n")
    expect("not a gatemap table -> must FAIL",
           lambda: report(gm4, sh, False), True)
    # the OTHER verdict for the honest branch: a pool where the gate binds on
    # NOTHING must be reportable, not an error
    sh6 = w("sh6.sh", "MAPS=(icefloe valkyrie)\n")
    expect("pool with no refusing map -> binds on 0, still PASSES",
           lambda: report(gm, sh6, False), False, ([], ["icefloe", "valkyrie"]))
    print("SELFTEST %s (%d wrong verdicts)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 0 if not fails else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("gatemap", nargs="?")
    ap.add_argument("--pool", default="tools/overnight.sh")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if not a.gatemap:
        ap.error("gatemap output file required")
    report(a.gatemap, a.pool)
