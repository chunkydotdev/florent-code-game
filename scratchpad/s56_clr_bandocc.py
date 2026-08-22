#!/usr/bin/env python
"""s56 v626 PLANK-A precondition probe: occupied band tiles on the fixture tapes.

In-game Florent Code League analysis. Per DESIGN-v626-clearance §5:
  P1  band tile (14 <= d² <= 32 to enemy core footprint, in-bounds, not WALL)
      carrying a live ENEMY building at round r
  P2  P1 tile passes the firing-face test (axial or exact-diagonal offset to
      some enemy footprint tile)
  P3  P2 tile has >=1 passable orthogonal neighbour (not wall, no building)
  P5  an OUR builder stood orthogonally adjacent to a P1 tile for >=25
      consecutive rounds while building nothing on it (orbit-then-ban proxy)
P4 (residual-candidate count) is NOT implemented — stated limitation; the
expectation binds on P1-P3 and P5.

--side wrong  runs the deliberate wrong-side control (must differ)
--band d²40-64 runs the mutation control (count must change materially)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from s54_klad_lib import Game

BUILDINGS = {"conveyor", "splitter", "harvester", "barrier", "gunner",
             "sentinel", "launcher", "core"}
def xy(p): return (p.x, p.y) if hasattr(p, "x") else tuple(p)

WRONG = "--side" in sys.argv and "wrong" in sys.argv
MUT = "--band" in sys.argv
LO, HI = (40, 64) if MUT else (14, 32)

def dsq_to_set(q, tiles):
    return min((q[0]-t[0])**2 + (q[1]-t[1])**2 for t in tiles)

def faceable(q, fp):
    # axial or exact-diagonal offset to some footprint tile
    return any(q[0] == t[0] or q[1] == t[1] or
               abs(q[0]-t[0]) == abs(q[1]-t[1]) for t in fp)

for fixdir in ("t_pb_f1", "t_pb_f2"):
    base = Path("scratchpad/s55_siteless") / fixdir
    G = dict(games=0, p1games=0, p1rounds=0, p1tiles=0, p2tiles=0, p3tiles=0,
             p5events=0, p5games=0)
    for f in sorted(base.glob("*.replay26")):
        us = 0 if "_seatA" in f.name else 1
        if WRONG: us = 1 - us
        them = 1 - us
        g = Game(f)
        efp = g.footprint(them)
        if not efp: continue
        band = [(x, y) for y in range(g.height) for x in range(g.width)
                if LO <= dsq_to_set((x, y), efp) <= HI and g.env(x, y) != 1]
        bset = set(band)
        tile_b = {}          # tile -> (eid, team)
        upos, uteam, kinds = {}, {}, {}
        adj_run = {}         # (builder id, band tile) -> consecutive rounds
        p1t = set(); p2t = set(); p3t = set()
        st = {"p1r": 0, "p5": 0}
        cur = -1
        def snap():
            occ = [t for t in bset
                   if t in tile_b and tile_b[t][1] == them]
            if occ:
                p1r_local = 1
            else:
                p1r_local = 0
            for t in occ:
                p1t.add(t)
                if faceable(t, efp):
                    p2t.add(t)
                    nb = [(t[0]+dx, t[1]+dy) for dx, dy in
                          ((1,0),(-1,0),(0,1),(0,-1))]
                    if any(0 <= n[0] < g.width and 0 <= n[1] < g.height
                           and g.env(*n) != 1 and n not in tile_b
                           for n in nb):
                        p3t.add(t)
            # P5: our builders adjacent to occupied band tiles
            seen = set()
            for i, p_ in upos.items():
                if uteam.get(i) != us or kinds.get(i) in BUILDINGS:
                    continue
                for t in occ:
                    if abs(p_[0]-t[0]) + abs(p_[1]-t[1]) == 1:
                        key = (i, t)
                        adj_run[key] = adj_run.get(key, 0) + 1
                        seen.add(key)
                        if adj_run[key] == 25:
                            st["p5"] += 1
            for key in list(adj_run):
                if key not in seen:
                    del adj_run[key]
            return p1r_local
        for rnd, k, pl in g.ev:
            if rnd != cur:
                if cur >= 0: st["p1r"] += snap()
                cur = rnd
            if k in ("BUILD", "REEMIT"):
                eid, team, ek, pos = pl
                uteam[eid] = team; kinds[eid] = ek
                if ek in BUILDINGS:
                    tile_b[xy(pos)] = (eid, team)
                else:
                    upos[eid] = xy(pos)
            elif k == "MOVE":
                upos[pl[0]] = xy(pl[2])
            elif k == "DEATH":
                rid = pl[0]
                for t, v in list(tile_b.items()):
                    if v[0] == rid: del tile_b[t]
                upos.pop(rid, None)
        if cur >= 0: st["p1r"] += snap()
        p1r = st["p1r"]; p5 = st["p5"]
        G["games"] += 1
        if p1t: G["p1games"] += 1
        G["p1rounds"] += p1r; G["p1tiles"] += len(p1t)
        G["p2tiles"] += len(p2t); G["p3tiles"] += len(p3t)
        if p5: G["p5games"] += 1
        G["p5events"] += p5
        if p5 or len(p1t) >= 4:
            print(f"  {f.name:32} P1 tiles={len(p1t):3d} rounds={p1r:4d} "
                  f"P2={len(p2t):3d} P3={len(p3t):3d} P5 events={p5}")
    tag = ("WRONG-SIDE " if WRONG else "") + ("MUT-BAND " if MUT else "")
    print(f"SUMMARY {tag}{fixdir}: games={G['games']} P1games={G['p1games']} "
          f"P1tiles={G['p1tiles']} P1rounds={G['p1rounds']} P2={G['p2tiles']} "
          f"P3={G['p3tiles']} P5events={G['p5events']} in {G['p5games']} games")
