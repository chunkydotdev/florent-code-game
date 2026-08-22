#!/usr/bin/env python
"""s56 v624 L1 precondition probe on the DETERMINISTIC FIXTURE tapes.

In-game Florent Code League analysis. L1 (SK_CAGE_REACH_BAR) admits the
walker's core peck when the ring-wide seal census has NO empty seat and the
body stands on a seal seat. Before any screen is read as mechanism evidence,
measure whether the fixture opponents (t_pb_f1 = NOISE_OFF _v542wave, t_pb_f2 =
NOISE_OFF Mjolnir) ever produce that state at all (s29 precondition rule).

empty mirrors _cage_survey: a seal seat is non-empty if off-map, WALL (env==1),
or carries any building of either team. Builder-on-seal is approximated from
MOVE/BUILD positions (cooldown ignored -> upper bound on opportunity rounds).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from s54_klad_lib import Game

BUILDINGS = {"conveyor", "splitter", "harvester", "barrier", "gunner",
             "sentinel", "launcher", "core"}
def xy(p): return (p.x, p.y) if hasattr(p, "x") else tuple(p)

for fixdir, opp in (("t_pb_f1", "NOISE_OFF _v542wave"),
                    ("t_pb_f2", "NOISE_OFF Mjolnir")):
    base = Path("scratchpad/s55_siteless") / fixdir
    print(f"== {fixdir} (opp {opp}) ==")
    tot_games = fire_games = 0
    tot_opp_rounds = tot_e0_rounds = tot_s7_rounds = 0
    for f in sorted(base.glob("*.replay26")):
        us = 0 if "_seatA" in f.name else 1
        them = 1 - us
        g = Game(f)
        ecp = g.core_pos(them)
        if ecp is None:
            print(f"  {f.name}: no enemy core decoded, SKIP")
            continue
        ox, oy = ecp
        LAP = [(ox-1,oy-1),(ox,oy-1),(ox+1,oy-1),(ox+2,oy-1),(ox+2,oy),
               (ox+2,oy+1),(ox+2,oy+2),(ox+1,oy+2),(ox,oy+2),(ox-1,oy+2),
               (ox-1,oy+1),(ox-1,oy)]
        SEALS = [LAP[i] for i in (1,2,4,5,7,8,10,11)]
        # a seat that is off-map or WALL is permanently non-empty
        def open_seat(t):
            x, y = t
            if not (0 <= x < g.width and 0 <= y < g.height):
                return False
            return g.env(x, y) != 1
        open_seats = [t for t in SEALS if open_seat(t)]
        tile_b = {}            # tile -> (eid, team)
        upos = {}              # entity id -> tile (anything that moves/spawns)
        uteam = {}
        cur = -1
        st = {"e0": 0, "opp": 0, "s7": 0}
        def snap():
            empties = sum(1 for t in open_seats if t not in tile_b)
            sealed = sum(1 for t in SEALS if not open_seat(t)) + \
                sum(1 for t in open_seats if t in tile_b and tile_b[t][1] == us)
            if sealed >= 7: st["s7"] += 1
            if empties == 0:
                st["e0"] += 1
                if any(uteam.get(i) == us and pos in SEALS
                       for i, pos in upos.items()):
                    st["opp"] += 1
        for rnd, kind, pl in g.ev:
            if rnd != cur:
                if cur >= 0: snap()
                cur = rnd
            if kind in ("BUILD", "REEMIT"):
                eid, team, ek, pos = pl
                if ek in BUILDINGS:
                    tile_b[xy(pos)] = (eid, team)
                else:
                    upos[eid] = xy(pos); uteam[eid] = team
            elif kind == "MOVE":
                eid, frm, to = pl
                upos[eid] = xy(to)
            elif kind == "DEATH":
                rid = pl[0]
                for t, v in list(tile_b.items()):
                    if v[0] == rid: del tile_b[t]
                upos.pop(rid, None)
        if cur >= 0: snap()
        tot_games += 1
        e0, opp_r, s7 = st["e0"], st["opp"], st["s7"]
        tot_e0_rounds += e0; tot_opp_rounds += opp_r; tot_s7_rounds += s7
        if opp_r:
            fire_games += 1
            print(f"  {f.name:32} empty0_rounds={e0:4d} "
                  f"L1_opportunity={opp_r:4d} sealed7_rounds={s7:4d}")
    print(f"  SUMMARY {fixdir}: games={tot_games} games_with_L1_opportunity="
          f"{fire_games} L1_opportunity_rounds={tot_opp_rounds} "
          f"empty0_rounds={tot_e0_rounds} sealed7_rounds={tot_s7_rounds}")
