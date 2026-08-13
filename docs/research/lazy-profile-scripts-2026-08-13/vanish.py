import sys
from pathlib import Path
sys.path.insert(0, "tools"); sys.path.insert(0, str(Path(__file__).parent))
from lazy_profile import parse, SEAT, d2
g = parse(Path("replay_archive/1ef56244-84a5-4136-ad8f-cf063b9fd3fe_game_2.replay26"))
L = SEAT[g["name"]]
hp_ids = {eid for _r, eid, _t, _k, _p, _d in g["hpev"]}
for d in g["deaths"]:
    if d[4] in hp_ids or d[2] != "builder_bot": continue
    r, p = d[0], tuple(d[3])
    print(f"\n#{d[4]} died r{r} @{p}")
    for rnd, t, kind, pos, dirn, eid in g["builds"]:
        if tuple(pos) == p and abs(rnd - r) <= 3:
            print(f"    build on that tile: r{rnd} team{'AB'[t]} {kind} #{eid}")
    for rnd, t, kind, pos, dirn, eid in g["builds"]:
        if d2(pos, p) <= 2 and abs(rnd - r) <= 2 and kind != "builder_bot":
            print(f"    build adjacent:     r{rnd} team{'AB'[t]} {kind}@{tuple(pos)}")
# how many lazy builds land on a tile occupied by their own bot, all 10 games
print("\n=== builds by lazy onto a tile occupied by one of their own bots (all games) ===")
FILES = ([f"replay_archive/1ef56244-84a5-4136-ad8f-cf063b9fd3fe_game_{i}.replay26" for i in range(1,6)]
       + [f"replay_archive/b9f3fab5-483a-443c-a2a3-695d69a8e915_game_{i}.replay26" for i in range(1,6)])
for f in FILES:
    gg = parse(Path(f)); LL = SEAT[gg["name"]]
    tag = ("M1" if "1ef" in f else "M2")+"g"+f.split("_game_")[1][0]
    # bot positions per round (approximate: apply moves in order)
    pos = {}
    born = {}
    hits = 0
    evs = sorted([(b[0],0,b) for b in gg["builds"]] + [(m[0],1,m) for m in gg["moves"]]
                 + [(d[0],2,d) for d in gg["deaths"]], key=lambda x:(x[0],x[1]))
    for rnd, kind_, e in evs:
        if kind_ == 0:
            r,t,k,p,dr,eid = e
            if k == "builder_bot":
                pos[eid] = (t, tuple(p))
            else:
                for bid,(bt,bp) in pos.items():
                    if bp == tuple(p) and bt == t == LL:
                        hits += 1
                        print(f"  {tag}: r{r} lazy built {k} on tile {tuple(p)} occupied by own bot #{bid}")
        elif kind_ == 1:
            r,t,eid,frm,to = e
            if eid in pos: pos[eid] = (t, tuple(to))
        else:
            pos.pop(e[4], None)
    if not hits: print(f"  {tag}: none")
