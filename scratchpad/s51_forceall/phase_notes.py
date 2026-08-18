#!/usr/bin/env python3
"""Phase marks (arrive/sent/funded/kill) for the 10 kept s51 FORCEALL replays,
to support qualitative notes on whether the ferry/collar degenerates on the
small-board (antler/fjordgate) geometry vs the closure-gated/cripple maps
(archipelago/midgard/yulerune).
"""
import sys
from pathlib import Path

REPO = Path("/Users/junghard/Projects/Work/florent-code-game")
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scratchpad" / "s51_rush_autopsy"))
from tape import Tape  # noqa: E402

AMMO_SHOT = 10

GAMES = [
    ("antler", "antler_s2_A", "A"), ("antler", "antler_s1_A", "A"),
    ("archipelago", "archipelago_s1_A", "A"), ("archipelago", "archipelago_s1_B", "B"),
    ("fjordgate", "fjordgate_s1_A", "A"), ("fjordgate", "fjordgate_s1_B", "B"),
    ("midgard", "midgard_s1_A", "A"), ("midgard", "midgard_s1_B", "B"),
    ("yulerune", "yulerune_s1_A", "A"), ("yulerune", "yulerune_s9_A", "A"),
]

REPDIR = REPO / "scratchpad" / "s51_forceall" / "replays"

print("%-14s %-20s %5s %6s %6s %7s %7s %7s %5s" % (
    "map", "tag", "seat", "our", "rounds", "arrive", "sent", "funded", "kill"))
for mp, tag, seat in GAMES:
    p = REPDIR / f"{tag}.replay26"
    our_team = 0 if seat == "A" else 1
    t = Tape(p, our_team)
    arrive = sent = funded = kill = -1
    for r in t.rows:
        if arrive < 0 and r["near_bot"] > 0:
            arrive = r["r"]
        if sent < 0 and r["near_sent"] > 0:
            sent = r["r"]
        if funded < 0 and r["near_sent"] > 0 and r["our_ammo"] >= AMMO_SHOT:
            funded = r["r"]
        if kill < 0 and r["opp_core_hp"] <= 0:
            kill = r["r"]
    winner_ours = (t.winner == our_team)
    print("%-14s %-20s %5s %6s %6d %7d %7d %7d %5d" % (
        mp, tag, seat, "US" if winner_ours else "OPP", t.rounds,
        arrive, sent, funded, kill))
