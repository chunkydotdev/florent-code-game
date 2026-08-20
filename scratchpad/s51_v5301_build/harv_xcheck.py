#!/usr/bin/env python3
"""CROSS-INSTRUMENT GATE for the one column this build is judged on.

`harv1` (round of OUR first harvester) is read by TWO independent tools that
share no code: `deliv.py` (this build's reader, used by `harvread.py`) and the
research arm's `routetape.py` (`harv1_rnd`, the tool the v530 report's §5.3
table was computed with).  If the two disagree, every harvester number in this
report is unreadable -- so they are compared row by row on the SAME replays.

⛔ AND THE AGREEMENT IS DRIVEN TO THE OTHER VERDICT.  A perfect-agreement rate
proves nothing on its own: a comparison that cannot report a mismatch would
also print 100%.  `--mutate N` corrupts N rows of the tape column before
comparing and the run MUST report exactly N mismatches.

Usage: harv_xcheck.py <routetape.tsv> <repdir> [--limit N] [--mutate N]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import deliv  # noqa: E402


def main():
    a = sys.argv[1:]
    tape, repdir = a[0], a[1]
    limit = mutate = 0
    if "--limit" in a:
        limit = int(a[a.index("--limit") + 1])
    if "--mutate" in a:
        mutate = int(a[a.index("--mutate") + 1])
    rows = []
    with open(tape) as f:
        hdr = f.readline().rstrip("\n").split("\t")
        for ln in f:
            rows.append(dict(zip(hdr, ln.rstrip("\n").split("\t"))))
    if limit:
        rows = rows[:limit]
    for i in range(min(mutate, len(rows))):
        rows[i]["harv1_rnd"] = str(int(float(rows[i]["harv1_rnd"])) + 7)
    agree = mism = miss = 0
    examples = []
    for r in rows:
        p = Path(repdir) / (r["tag"] + ".replay26")
        if not p.exists():
            miss += 1
            continue
        d = deliv.read(p, 0 if r["seat"] == "A" else 1)
        t = int(float(r["harv1_rnd"]))
        if d["harv1"] == t:
            agree += 1
        else:
            mism += 1
            if len(examples) < 5:
                examples.append((r["tag"], d["harv1"], t))
    print("rows compared: %d   missing replays: %d" % (agree + mism, miss))
    print("deliv.harv1 == routetape.harv1_rnd on %d/%d rows (%d mismatch)"
          % (agree, agree + mism, mism))
    for e in examples:
        print("   MISMATCH %s deliv=%s tape=%s" % e)
    if mutate:
        print("MUTATION CONTROL: %d rows corrupted, %d mismatches reported -> %s"
              % (mutate, mism, "PASS" if mism == mutate else "FAIL"))
        return 0 if mism == mutate else 1
    return 0 if mism == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
