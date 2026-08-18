#!/usr/bin/env python3
"""THE FAILURE REEL + its extension, selected by a STATED RULE.

SELECTION RULE (the house convention, restated because it is a choice):
  the EARLIEST our-core-death in EACH map, for the `v522` arm, across every
  complete headline block.  One per map is what stops the reel being six copies
  of one board.  Ties: lowest block -> lowest seed -> seat A.

⛔ AND THE CONVENTION IS OVERLAP-BLIND, WHICH v521 PROVED RATHER THAN GUESSED.
Its reel returned overlap_r = 0 in 6 of 6 against a population mean of 13.35 and
39.9% of games above zero -- the reel selects the tail, and the tail has no
overlap by construction.  The mandate therefore asks for an EXTENSION: the 2
LATEST-KILL WINS, which are the other tail and the one the kill-round bar
actually binds on.  They are printed as clearly-labelled extension rows, never
folded into the reel's own six.
"""
import csv
import sys
from pathlib import Path

B = Path(sys.argv[1])
ARM = sys.argv[2] if len(sys.argv) > 2 else "v522"
OVL = Path(sys.argv[3]) if len(sys.argv) > 3 else None

rows = []
for b in sorted(B.glob("b*"), key=lambda p: int(p.name[1:])):
    f = b / (ARM + ".tsv")
    if not f.exists():
        continue
    for r in csv.DictReader(open(f), delimiter="\t"):
        r["block"] = int(b.name[1:])
        r["replay"] = str(b / ("rep" + ARM) / (r["tag"] + ".replay26"))
        rows.append(r)

ovl = {}
if OVL and OVL.exists():
    for r in csv.DictReader(open(OVL), delimiter="\t"):
        ovl[r["tag"]] = r


def key(r):
    return (int(r["turn"]), r["block"], int(r["seed"]), r["seat"])


print("rows read: %d" % len(rows))
print("\n=== FAILURE REEL: earliest our-core-death per map, arm %s ===" % ARM)
print("%-24s %-14s %6s %6s %8s %9s %9s %9s" %
      ("game", "map", "block", "turn", "overlap", "sealed", "livefund",
       "net_in"))
for mp in ["atoll", "drakkarfjord", "glacierkeep", "midgard", "nordkap",
           "yulerune"]:
    cand = [r for r in rows if r["map"] == mp and r["ours"] == "OPP"]
    if not cand:
        print("%-24s %-14s  -- no our-core-death in this arm --" % ("", mp))
        continue
    r = sorted(cand, key=key)[0]
    o = ovl.get(r["tag"], {})
    print("%-24s %-14s %6s %6s %8s %9s %9s %9s" %
          (r["tag"], mp, r["block"], r["turn"], o.get("overlap_r", "?"),
           o.get("sealed_r", "?"), o.get("livefund_r", "?"),
           o.get("net_in", "?")))

print("\n=== REEL EXTENSION (mandate): the 2 LATEST-KILL WINS, arm %s ===" % ARM)
wins = [r for r in rows if r["ours"] == "US" and r["cond"].strip().lower()
        .startswith("core")]
for r in sorted(wins, key=lambda r: -int(r["turn"]))[:2]:
    o = ovl.get(r["tag"], {})
    print("%-24s %-14s %6s %6s %8s %9s %9s %9s" %
          (r["tag"], r["map"], r["block"], r["turn"], o.get("overlap_r", "?"),
           o.get("sealed_r", "?"), o.get("livefund_r", "?"),
           o.get("net_in", "?")))
print("\n(win conditions seen: %s)" %
      sorted({r["cond"] for r in rows}))
