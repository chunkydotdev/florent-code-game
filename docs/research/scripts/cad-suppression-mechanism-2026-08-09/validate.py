#!/usr/bin/env python3
"""Validation for the suppression-mechanism cut.

  1. SEAT.  meta.json's teamA==OpenSverige must independently predict
     join.tsv's reconciled `our_team`==0 on every game that appears in both.
     A conclusion may not consume an attribution path that has not reconciled.
  2. ALL-ZERO COLUMN SWEEP on mech_rounds.tsv -- an exact zero is a bug
     signature before it is a finding (corpus traps 5 and 6).
  3. Reproduce the published lockout landmark cells on the overlapping
     population, so the new decoder's unknown cells are usable.
  4. Cross-check the two independent build streams: first-placeEntity builds
     vs BuilderBuild (Update 16) events; the difference must be the core's own
     builder-bot spawns.

Usage: validate.py <freeze_dir>
"""
from __future__ import annotations

import csv
import statistics
import sys

from analyse import LEDGER, load, cells, wsum


def main(d):
    P = print
    pop = list(csv.DictReader(open(f"{d}/cad_population.tsv"), delimiter="\t"))
    jn = {r["file"]: r for r in csv.DictReader(open(f"{d}/join.tsv"),
                                               delimiter="\t")}
    ok = bad = 0
    for r in pop:
        j = jn.get(r["file"])
        if not j:
            continue
        # meta says CAD sits on team `cad_team`; join says which index is US.
        if int(j["our_team"]) == 1 - int(r["cad_team"]):
            ok += 1
        else:
            bad += 1
    P(f"1. SEAT reconciliation on overlapping games: {ok} agree, {bad} disagree")

    rows = list(csv.DictReader(open(f"{d}/mech_rounds.tsv"), delimiter="\t"))
    P(f"2. ALL-ZERO SWEEP over {len(rows)} rows")
    cols = [c for c in rows[0] if c not in ("file",)]
    zeros = []
    for c in cols:
        s = 0
        for r in rows:
            s += int(r[c])
        if s == 0:
            zeros.append(c)
    P(f"   all-zero columns: {zeros if zeros else 'NONE'}")

    games = load(d)
    P("3. LOCKOUT LANDMARK reproduction "
      "(published: r14-40 damaged mean 1.0 / 31% zero, undamaged 7.4 / 2%)")
    for a, b in ((14, 25), (14, 40)):
        dm, un = cells(games, a, b)
        for lbl, fs in (("damaged", dm), ("undamaged", un)):
            v = [wsum(games[f]["rs"], a, b, "cad_builds") for f in fs]
            P(f"   r{a}-{b} {lbl:<9} n={len(v):<4} mean={statistics.mean(v):.2f} "
              f"median={statistics.median(v):.0f} "
              f"zero={sum(1 for x in v if x == 0)}/{len(v)}")

    pe = bb = spawn = 0
    for r in rows:
        pe += int(r["cad_builds"])
        bb += int(r["cad_bbuild"])
        spawn += int(r["b_builder_bot"])
    P(f"4. BUILD STREAMS: first-placeEntity {pe}, BuilderBuild {bb}, "
       f"difference {pe-bb}; CAD builder_bot placements (core spawns) {spawn}; "
       f"residual {pe-bb-spawn}")

    ledger = sum(int(r["L_" + k]) for r in rows for k in LEDGER)
    bots = sum(int(r["bots_start"]) for r in rows)
    P(f"5. LEDGER partition: labelled turns {ledger} vs builder-turns {bots} "
      f"(diff {ledger-bots})")


if __name__ == "__main__":
    sys.path.insert(0, __file__.rsplit("/", 1)[0])
    main(sys.argv[1])
