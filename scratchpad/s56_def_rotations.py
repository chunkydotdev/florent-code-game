#!/usr/bin/env python
"""s56 v629 prerequisite: rotations/game instrument (none exists in the repo).

In-game Florent Code League analysis. A gunner rotation re-emits the entity
(placeEntity with an existing id => lib event REEMIT) at an unchanged position.
rotations(team) = REEMIT events of that team's GUNNERS at their build position.

Controls (run before any number is read):
  --control-sent   sentinel REEMITs must be ~0 (a sentinel cannot rotate);
                   nonzero refutes the REEMIT=rotation reading
  --control-bc     BC v68's gunner rotations on the MIRROR first-contact cell
                   must be materially nonzero (study: 8.1/game)
Default run: OUR gunner rotations on the reference tapes t_pb_f{1,2}.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from s54_klad_lib import Game
def xy(p): return (p.x, p.y) if hasattr(p, "x") else tuple(p)

def rotations(fp, team, kind="gunner"):
    g = Game(fp)
    pos0 = {}
    n = 0
    for rnd, k, pl in g.ev:
        if k == "BUILD":
            eid, tm, ek, pos = pl
            if tm == team and ek == kind:
                pos0[eid] = xy(pos)
        elif k == "REEMIT":
            eid, tm, ek, pos = pl
            if eid in pos0 and ek == kind and xy(pos) == pos0[eid]:
                n += 1
    return n

mode = sys.argv[1] if len(sys.argv) > 1 else "ours"
if mode == "--control-sent":
    tot = 0; games = 0
    for F in ("t_pb_f1", "t_pb_f2"):
        for f in sorted((Path("scratchpad/s55_siteless") / F).glob("*.replay26")):
            for team in (0, 1):
                tot += rotations(f, team, "sentinel")
            games += 1
    print(f"CONTROL sentinel-REEMIT-at-pos: {tot} across {games} games x2 teams (expect ~0)")
elif mode == "--control-bc":
    import csv
    seat = {}
    for r in csv.DictReader(open("corpus/unrated_games.tsv"), delimiter="\t"):
        seat[r["file"]] = r["our_team"]
    tot = 0; games = 0
    for f in sorted(Path("replay_archive").glob("5ee3afec*_game_*.replay26")) + \
             sorted(Path("replay_archive").glob("4bc7ed13*_game_*.replay26")):
        us = 0 if seat[f.name] == "A" else 1
        tot += rotations(f, 1 - us, "gunner")   # BC's side
        games += 1
    print(f"CONTROL BC-v68 gunner rotations: {tot} in {games} games = "
          f"{tot/max(games,1):.1f}/game (study says ~8.1)")
else:
    for F in ("t_pb_f1", "t_pb_f2"):
        tot = 0; games = 0; per = []
        for f in sorted((Path("scratchpad/s55_siteless") / F).glob("*.replay26")):
            us = 0 if "_seatA" in f.name else 1
            r = rotations(f, us, "gunner")
            tot += r; games += 1; per.append((f.stem, r))
        nz = [(c, r) for c, r in per if r]
        print(f"{F}: OUR gunner rotations total={tot} in {games} games "
              f"({tot/games:.2f}/game); nonzero cells: {nz[:8]}")
