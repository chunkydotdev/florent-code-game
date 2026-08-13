import sys
from pathlib import Path
sys.path.insert(0, "tools"); sys.path.insert(0, str(Path(__file__).parent))
from lazy_profile import parse, SEAT, d2
g = parse(Path("replay_archive/1ef56244-84a5-4136-ad8f-cf063b9fd3fe_game_2.replay26"))
L = SEAT[g["name"]]; U = 1-L
lc = g["corepos"][L]
print("lazy core", lc, "our core", g["corepos"][U], "map", g["w"], g["h"])
# rebuild world state up to round R
def state(R):
    alive = {}
    for rnd, t, kind, pos, dirn, eid in g["builds"]:
        if rnd <= R: alive[eid] = [t, kind, tuple(pos)]
    for r, t, eid, frm, to in g["moves"]:
        if r <= R and eid in alive: alive[eid][2] = tuple(to)
    for d in g["deaths"]:
        if d[0] <= R: alive.pop(d[4], None)
    return alive
for R in (80, 81, 98, 110):
    a = state(R)
    print(f"\n--- state after r{R} near lazy core ---")
    occ = {}
    for eid, (t, k, p) in a.items():
        if d2(p, lc) <= 26: occ[p] = f"{'LU'[t==U]}{k[:4]}#{eid}"
    for y in range(max(0,lc[1]-4), min(g["h"], lc[1]+5)):
        row = []
        for x in range(max(0,lc[0]-3), min(g["w"], lc[0]+6)):
            env = g["tiles"][y][x]
            if (x,y) in occ: row.append(f"{occ[(x,y)]:<12s}")
            elif (x,y) in g["foot"][L]: row.append(f"{'CORE':<12s}")
            elif env==1: row.append(f"{'####':<12s}")
            elif env==2: row.append(f"{'ore':<12s}")
            else: row.append(f"{'.':<12s}")
        print(f"  y={y:2d} " + "".join(row))
hp_ids = {eid for _r, eid, _t, _k, _p, _d in g["hpev"]}
print("\n-- vanished bots and their last moves --")
for d in g["deaths"]:
    if d[4] in hp_ids or d[2] != "builder_bot": continue
    eid = d[4]
    mv = [(r, frm, to) for r, t, e, frm, to in g["moves"] if e == eid]
    print(f"  #{eid} died r{d[0]} @{tuple(d[3])} born r{d[5]}; moves n={len(mv)} last5={mv[-5:]}")
    acts = [(r,tg) for r,t,aid,ap,tg in g["batks"] if aid==eid]
    hl = [(r,tg) for r,t,aid,tg in g["bheals"] if aid==eid]
    print(f"      last builderAttack {acts[-3:]}  last builderHeal {hl[-3:]}")
print("\n-- our barrier builds near their core --")
for rnd, t, kind, pos, dirn, eid in g["builds"]:
    if t==U and kind=="barrier" and d2(pos, lc) <= 30:
        print(f"  r{rnd} barrier @{tuple(pos)} d2={d2(pos,lc)}")
print("\n-- lazy builds after r80 --")
n=0
for rnd, t, kind, pos, dirn, eid in g["builds"]:
    if t==L and rnd>=80:
        print(f"  r{rnd} {kind}@{tuple(pos)}"); n+=1
    if n>18: break
