#!/usr/bin/env python3
"""THE FAILURE REEL, selected by a STATED RULE (the house convention).

RULE: the EARLIEST our-core-death on EACH map, for the named arm, across the
whole headline battery.  One per map is what stops the reel being five copies
of one board.  Ties: lowest seed -> seat A.  Capped at 5 rows.

EXTENSION (labelled, never folded into the reel): the 2 LATEST-KILL WINS --
the other tail, and the one the kill-round bar actually binds on.

Usage: reel.py <battery-dir> [arm]
"""
import csv
import sys
from pathlib import Path

B = Path(sys.argv[1])
ARM = sys.argv[2] if len(sys.argv) > 2 else "v526"

rows = [r for r in csv.DictReader(open(B / "results.tsv"), delimiter="\t")
        if r["arm"] == ARM]

deaths = [r for r in rows
          if r["cond"].startswith("Core destroyed") and r["ours"] != "US"]
best = {}
for r in sorted(deaths, key=lambda r: (int(r["turn"]), int(r["seed"]),
                                       r["seat"])):
    best.setdefault(r["map"], r)

print("=== FAILURE REEL (%s): earliest our-core-death per map ===" % ARM)
print("%-14s %-6s %-4s %-6s %s" % ("map", "turn", "seed", "seat", "replay"))
for r in sorted(best.values(), key=lambda r: int(r["turn"]))[:5]:
    print("%-14s %-6s %-4s %-6s %s"
          % (r["map"], r["turn"], r["seed"], r["seat"],
             B / "rep" / (r["tag"] + ".replay26")))

wins = [r for r in rows
        if r["ours"] == "US" and r["cond"].startswith("Core destroyed")]
print("\n=== EXTENSION (labelled, NOT part of the reel): 2 latest-kill wins ===")
for r in sorted(wins, key=lambda r: -int(r["turn"]))[:2]:
    print("%-14s %-6s %-4s %-6s %s"
          % (r["map"], r["turn"], r["seed"], r["seat"],
             B / "rep" / (r["tag"] + ".replay26")))

print("\ndeaths=%d of n=%d (%.1f%%)  ·  r1000 games=%d"
      % (len(deaths), len(rows), 100.0 * len(deaths) / max(1, len(rows)),
         sum(1 for r in rows if not r["cond"].startswith("Core destroyed"))))
