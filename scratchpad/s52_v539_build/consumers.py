#!/usr/bin/env python3
"""v539 build instrument #3 -- THE SLOT_HARVESTERS CONSUMER ENUMERATION.

Lists EVERY read and write of `SLOT_HARVESTERS` in a bot tree, with the file,
line, the comparison operator and the threshold it is tested against.  The
build report's consumer table is generated from this, not typed from memory:
the whole v539 design turns on which direction each of these gates moves when
the ratchet stops lying, and a hand-written list of ten sites is exactly the
kind of thing that quietly loses one.

⛔ IT IS A GREP, NOT A TYPE-CHECKER.  It finds textual read sites; a consumer
that stashed the value in a local and tested it three functions later would be
reported at the READ, not at the TEST.  Both such sites in this tree
(`main.py` `harv = ...` and `eco.py` `harv = ...`) are annotated by hand in the
report and named there as hand-annotated.

    .venv/bin/python scratchpad/s52_v539_build/consumers.py --selftest
    .venv/bin/python scratchpad/s52_v539_build/consumers.py _v539resilience
"""
import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
NAME = "SLOT_HARVESTERS"
READ = re.compile(r"read_store\(\s*" + NAME + r"\s*\)")
WRITE = re.compile(r"write_store\(\s*" + NAME + r"\s*,")
CMP = re.compile(r"read_store\(\s*" + NAME + r"\s*\)\s*(>=|<=|==|!=|<|>)\s*"
                 r"([A-Za-z_0-9]+)")


def scan_text(text, fname="<mem>"):
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        if NAME not in line:
            continue
        kind = None
        if WRITE.search(line):
            kind = "WRITE"
        elif READ.search(line):
            kind = "READ"
        else:
            continue
        m = CMP.search(line)
        out.append({
            "file": fname, "line": i, "kind": kind,
            "op": m.group(1) if m else "",
            "threshold": m.group(2) if m else "",
            "text": line.strip(),
        })
    return out


def scan_tree(tree):
    root = REPO / tree if "/" in tree else REPO / "bots" / tree
    out = []
    for f in sorted(root.glob("*.py")):
        out.extend(scan_text(f.read_text(), f.name))
    return out


def report(tree, out=sys.stdout):
    rows = scan_tree(tree)
    print("tree: %s   sites: %d  (READ %d / WRITE %d)" % (
        tree, len(rows),
        sum(1 for r in rows if r["kind"] == "READ"),
        sum(1 for r in rows if r["kind"] == "WRITE")), file=out)
    for r in rows:
        print("  %-12s %5d  %-5s %-3s %-16s | %s" % (
            r["file"], r["line"], r["kind"], r["op"], r["threshold"],
            r["text"][:90]), file=out)
    return rows


def selftest():
    fails = []

    def chk(c, m):
        print(("  ok   " if c else "  FAIL ") + m)
        if not c:
            fails.append(m)

    print("[1] it finds a read, a write, and a threshold")
    t = ("if ct.read_store(SLOT_HARVESTERS) >= ECO_NEED:\n"
         "    ct.write_store(SLOT_HARVESTERS, live)\n"
         "x = 1\n")
    rows = scan_text(t)
    chk(len(rows) == 2, "2 sites in a 3-line fixture")
    chk(rows[0]["kind"] == "READ" and rows[0]["op"] == ">="
        and rows[0]["threshold"] == "ECO_NEED", "read/op/threshold decoded")
    chk(rows[1]["kind"] == "WRITE", "the write is classified as a WRITE")

    print("[2] it returns NOTHING on text that does not use the slot")
    chk(scan_text("if ct.read_store(SLOT_UNDER) >= 1:\n") == [],
        "a different slot is not reported (the other verdict)")
    chk(scan_text("# SLOT_HARVESTERS is a monotone high-water mark\n") == [],
        "a mere mention in a COMMENT is not a site (the other verdict)")

    print("[3] mutation: rename the slot and every site must disappear")
    chk(scan_text(t.replace("SLOT_HARVESTERS", "SLOT_ZZZ")) == [],
        "0 sites after renaming the slot out of the fixture")

    print("[4] the real trees: parent and arm agree on the site count")
    p = scan_tree("_v537socket")
    a = scan_tree("_v539resilience")
    chk(len(p) >= 10, "parent has >= 10 sites (found %d)" % len(p))
    # the flagged-off honest reset is ONE branch but TWO textual sites: the
    # `live < read_store(...)` test and the `write_store(..., live)` it guards
    chk(len(a) == len(p) + 2,
        "v539 adds EXACTLY the honest-reset branch (2 sites): %d vs %d"
        % (len(a), len(p)))
    chk(sum(1 for r in a if r["kind"] == "READ")
        == sum(1 for r in p if r["kind"] == "READ") + 1,
        "and exactly ONE of the two is a new READ")

    print()
    if fails:
        print("SELFTEST FAILED: %d" % len(fails))
        return 1
    print("SELFTEST PASSED")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("tree", nargs="?", default="_v539resilience")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    report(a.tree)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
