"""ITERATION 12 RELEASE SMOKE decoder — GAME CONTEXT: in-game Florent Code
League fixture work (self-play fixture => execution debugger for DOSE only,
never a level/identity verdict; the unrated window judges the level).

Per replay: denier away-rounds (top-bot), away ore seals (count + rounds),
our barrier builds anywhere (decode control). Usage:
    smoke_decode.py <dir> <ourseat A|B>
Registered expectation (BEFORE first read, commit message is the record):
ON arm away-rounds >> OFF arm and ON away-seals > 0 in >=2 of 4 games;
falsifier: ON ~= OFF => the recall hypothesis is wrong, revert the gates.
"""
import sys, pathlib
from collections import Counter

sys.path.insert(0, "tools"); sys.path.insert(0, "scratchpad")
from s54_klad_lib import Game

ENV_ORE = 2
RDIR, SEAT = sys.argv[1], sys.argv[2]
US = 0 if SEAT == "A" else 1


def d2(a, b): return (a[0]-b[0])**2 + (a[1]-b[1])**2


for p in sorted(pathlib.Path(RDIR).glob("*.replay26")):
    g = Game(p)
    them = 1 - US
    oc, ec = g.core_pos(US), g.core_pos(them)
    occ = (oc[0]+.5, oc[1]+.5); ecc = (ec[0]+.5, ec[1]+.5)
    away = lambda q: d2(q, ecc) < d2(q, occ)
    ore = {(x, y) for y in range(g.height) for x in range(g.width)
           if g.env(x, y) == ENV_ORE}

    seals_away = [(r, pa[3]) for r, k, pa in g.ev
                  if k == "BUILD" and pa[1] == US and pa[2] == "barrier"
                  and pa[3] in ore and away(pa[3])]
    bar_all = sum(1 for _r, k, pa in g.ev
                  if k == "BUILD" and pa[1] == US and pa[2] == "barrier")

    ourbots = {i for i, m in g.ever.items()
               if m["team"] == US and m["kind"] == "builder_bot"}
    ev_by_round = {}
    for r, k, pa in g.ev:
        ev_by_round.setdefault(r, []).append((k, pa))
    pos_now = {}; away_by_bot = Counter(); R = g.rounds
    for r in range(R):
        for k, pa in ev_by_round.get(r, ()):
            if k in ("BUILD", "REEMIT"):
                if pa[0] in ourbots: pos_now[pa[0]] = pa[3]
            elif k == "MOVE":
                if pa[0] in ourbots: pos_now[pa[0]] = pa[2]
            elif k == "DEATH":
                pos_now.pop(pa[0], None)
        for bid, q in pos_now.items():
            if away(q): away_by_bot[bid] += 1
    top = away_by_bot.most_common(1)
    top = top[0][1] if top else 0
    print(f"{p.stem:24s} R={R:4d} topAwayR={top:4d} "
          f"awaySeals={len(seals_away):2d} sealRounds={[r for r,_ in seals_away][:8]} "
          f"barriersAnywhere={bar_all}")
