#!/usr/bin/env python3
"""Fold the v517 stderr instruments over an arm's log directory.

Bot-side counters ONLY -- the zero-vs-nonzero mutant check.  Every currency
claim in the report is read off the REPLAY (sentrace.py); this file exists to
show the mechanism runs in one arm and does not in the other.

Emits, per arm:
  fd_lines / fd_games   FIREDISC517 rounds and the games carrying them
  hold_r                rounds the discipline suppressed a core shot
  twin_r                rounds the sentinel saw/knew a twin
  code1_r               rounds the published verdict was HELD
  viol                  ⛔ holds taken inside the fresh-contact window: MUST BE 0
  resets                TTL re-probes
  held / heldfund / heldonly   the end-of-life save counters (max per game)
  bank_lines / bank_games      TWINBANK517 (change 2b)
  gate_lines / gate_games      TWINGATE517 (a raider alive at the ring during a
                               hold -- change 2's REACHABILITY ceiling)
  buys / buys_hold             TWIN517 purchases, and those made under a hold
"""
import re
import sys
from pathlib import Path


def kv(line):
    f = line.split()
    d = {}
    for i in range(1, len(f) - 1):
        d.setdefault(f[i], f[i + 1])
    return d


def main():
    name = sys.argv[1]
    fd = hold = twin = code1 = viol = resets = 0
    held = heldf = heldo = 0
    bank = gate = buys = buysh = 0
    gfd = set()
    gbank = set()
    ggate = set()
    gtwin = set()
    per_game_max = {}
    for d in sys.argv[2:]:
        for p in sorted(Path(d).glob("*.err")):
            tag = p.stem
            for line in p.read_text(errors="replace").splitlines():
                if line.startswith("FIREDISC517"):
                    fd += 1
                    gfd.add(tag)
                    k = kv(line)
                    hold += int(k.get("hold", 0))
                    twin += int(k.get("twin", 0))
                    code1 += 1 if k.get("code") == "1" else 0
                    m = per_game_max.setdefault(tag, [0, 0, 0, 0, 0])
                    m[0] = max(m[0], int(k.get("held", 0)))
                    m[1] = max(m[1], int(k.get("heldfund", 0)))
                    m[2] = max(m[2], int(k.get("resets", 0)))
                    m[3] = max(m[3], int(k.get("viol", 0)))
                elif line.startswith("TWINBANK517"):
                    bank += 1
                    gbank.add(tag)
                elif line.startswith("TWINGATE517"):
                    gate += 1
                    ggate.add(tag)
                elif line.startswith("TWIN517"):
                    buys += 1
                    gtwin.add(tag)
                    if kv(line).get("hold") == "1":
                        buysh += 1
    for m in per_game_max.values():
        held += m[0]
        heldf += m[1]
        resets += m[2]
        viol += m[3]
    print("%-10s FD=%5d/%2dg hold_r=%5d twin_r=%4d code1_r=%5d VIOL=%d "
          "resets=%3d held=%5d heldfund=%5d ammo_saved=%6d | bank=%5d/%2dg "
          "| gate=%4d/%2dg | buys=%3d (hold %d)"
          % (name, fd, len(gfd), hold, twin, code1, viol, resets, held, heldf,
             10 * heldf, bank, len(gbank), gate, len(ggate), buys, buysh))


main()
