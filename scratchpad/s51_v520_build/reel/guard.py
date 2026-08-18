#!/usr/bin/env python3
"""INSTRUMENT GUARD for the s51 rush-autopsy classifier — driven both ways.

Three cells, each of which MUST come out differently from the others:

  A. POSITIVE CONTROL, documented KILL.  `v513_log-atoll-s1-A` from the banked
     v513 eviction autopsy (`scratchpad/s51_evict_autopsy/fired.tsv`, produced
     by a DIFFERENT parser in a prior session): outcome `v513_log` (we won),
     cond `Core_destroyed`, end_r 277.  The classifier must read a KILLED
     offence and reproduce winner + end round.

  B. POSITIVE CONTROL, documented NO-KILL r1000.  `v513_log-glacierkeep-s3-B`:
     cond `Titanium_collected_(tiebreak)`, end_r 1000, 0 evictions, 223 rounds
     of deadlock exposure.  The classifier must NOT read KILLED and must
     reproduce end round 1000.

  C. MUTATION CONTROL.  Cell A re-run with the seat->team assignment flipped.
     Every "our"/"opp" fact transposes, so the classifier must change its
     verdict.  A classifier that survives this is reading a constant.

A pass requires: A != B on the offence axis, A and B both reproduce the banked
outcome fields, and C != A.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game")
from classify import classify  # noqa: E402
from turrets import run  # noqa: E402

BANK = Path("/Users/junghard/Projects/Work/florent-code-game/"
            "scratchpad/s51_evict_autopsy/logs")
FIRED = Path("/Users/junghard/Projects/Work/florent-code-game/"
             "scratchpad/s51_evict_autopsy/fired.tsv")


def facts(path, our_team):
    r = run(path, our_team)
    T = r["turrets"]
    ours = [t for t in T.values() if t["team"] == our_team]
    siege = [t for t in ours if t["core_shots"] > 0]
    # winner + condition straight off the replay bytes
    from tools.replay_census import WIRE_LEN, fields
    data = path.read_bytes()
    winner = None
    cond = ""
    for num, wire, value in fields(data):
        if num == 4 and wire == 0:
            winner = value
        elif num == 6 and wire == WIRE_LEN:
            cond = value.decode()
    # heal on the enemy core
    from tools.replay_census import parse_update_hp, read_pos
    heal = 0
    turns = []
    mb = None
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            mb = value
        elif num == 3 and wire == WIRE_LEN:
            turns.append(value)
    cores = []
    for num, _w, value in fields(mb):
        if num == 4:
            c = {"id": 0, "team": 0}
            for cn, _cw, cv in fields(value):
                if cn == 1:
                    c["id"] = cv
                elif cn == 2:
                    c["team"] = cv
            cores.append(c)
    oppcore = next(c["id"] for c in cores if c["team"] != our_team)
    for tb in turns:
        for _n, _w, ub in fields(tb):
            for un, _uw, ubuf in fields(ub):
                if un == 5:
                    eid, d = parse_update_hp(ubuf)
                    if eid == oppcore and 1 <= d <= 4:
                        heal += d
    return dict(
        cond=("Core destroyed" if cond == "core_destroyed"
              else "Titanium collected (tiebreak)"),
        ours=("US" if winner == our_team else "OPP"),
        turn=len(turns),
        siege_shots=sum(t["core_shots"] for t in siege),
        siege_life=sum(t["life"] for t in siege),
        siege_funded=sum(t["funded_r"] for t in siege),
        oppcore_heal=heal,
    )


def main():
    bank = {r["game"]: r for r in csv.DictReader(open(FIRED), delimiter="\t")}
    fails = []
    results = {}
    # seat: the banked grid names the seat in the tag (-A / -B); seat A = team 0
    for cell, game, seat_team, label in (
            ("A", "v513_log-atoll-s1-A", 0, "documented KILL"),
            ("B", "v513_log-glacierkeep-s3-B", 1, "documented r1000 no-kill"),
            ("C", "v513_log-atoll-s1-A", 1, "MUTATION: seat flipped")):
        p = BANK / (game + ".replay26")
        f = facts(p, seat_team)
        off, dfc, fs, hs = classify(f)
        results[cell] = (off, dfc, f)
        b = bank[game]
        print("%s  %-34s %-30s -> offence=%-12s defence=%-12s "
              "shots=%-4d life=%-4d funded=%-4d heal=%-5d turn=%d"
              % (cell, game, label, off, dfc, f["siege_shots"], f["siege_life"],
                 f["siege_funded"], f["oppcore_heal"], f["turn"]))
        if cell in ("A", "B"):
            want_turn = int(b["end_r"])
            want_us = (b["outcome"] == "v513_log")
            want_kill = b["cond"] == "Core_destroyed"
            if f["turn"] != want_turn + 1 and f["turn"] != want_turn:
                fails.append("%s: replay rounds %d vs banked end_r %d"
                             % (cell, f["turn"], want_turn))
            if (f["ours"] == "US") != want_us:
                fails.append("%s: winner %s vs banked outcome %s"
                             % (cell, f["ours"], b["outcome"]))
            if ((off == "KILLED") != (want_kill and want_us)):
                fails.append("%s: offence %s vs banked cond %s outcome %s"
                             % (cell, off, b["cond"], b["outcome"]))
    if results["A"][0] == results["B"][0]:
        fails.append("A and B got the SAME offence label — classifier is a "
                     "constant on these two documented, opposite games")
    if results["C"][0] == results["A"][0] and results["C"][1] == results["A"][1]:
        fails.append("MUTATION control C reproduced A — the classifier does "
                     "not depend on which side is ours")
    print()
    if fails:
        print("GUARD FAIL:")
        for f in fails:
            print("  " + f)
        raise SystemExit(2)
    print("GUARD PASS: A(KILLED) != B(%s); mutation C(%s/%s) != A(%s/%s); both "
          "documented cells reproduced winner, condition and end round."
          % (results["B"][0], results["C"][0], results["C"][1],
             results["A"][0], results["A"][1]))


if __name__ == "__main__":
    main()
