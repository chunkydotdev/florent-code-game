"""DWELL TIME PER FORWARD BUILD — ours vs the opponent's, same games.

Research's reframing: the gunner hazard is ~2% PER FORWARD ROUND and it
ACCUMULATES, so a plank that cuts forward rounds cuts deaths proportionally and
buys nothing per unit of work. LOKI-25 is that identity exactly (deaths -24%,
presence -23%, deaths-per-build -2.3%). The lever is therefore HOW MANY ROUNDS A
RAIDER STANDS FORWARD PER BUILD IT PLACES.

Both sides measured in the SAME games, each relative to its OWN enemy core, so
this is internal and does not repeat the FIELD_vsUS population error.
"""
import json, sys
from pathlib import Path
sys.path.insert(0, "tools")
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa
AR = Path("replay_archive"); OURS = "379a5d80-9921-4c9e-949b-f9b1dcba16be"

def ids(p):
    return [json.loads(l[l.index("{"):])["matchId"] for l in Path(p).read_text().splitlines() if '"matchId"' in l]

def walk(fp, our):
    data = fp.read_bytes(); mapbuf=None; turns=[]
    for n,w,v in fields(data):
        if n==1 and w==WIRE_LEN: mapbuf=v
        elif n==3 and w==WIRE_LEN: turns.append(v)
    cores=[]
    for n,w,v in fields(mapbuf):
        if n==4 and w==WIRE_LEN:
            d={a:b for a,_c,b in fields(v)}; cores.append((d.get(2,0), read_pos(d[3])))
    if len(cores)<2: return None
    home={t:c for t,c in cores}
    d2=lambda a,b:(a[0]-b[0])**2+(a[1]-b[1])**2
    pos={}; team={}; kind={}
    rounds={0:0,1:0}; builds={0:0,1:0}
    for rnd,tb in enumerate(turns):
        for _a,_b,ub in fields(tb):
            for un,_w,ubuf in fields(ub):
                if un==1:
                    for en,_e,eb in fields(ubuf):
                        if en!=1: continue
                        e=parse_entity(eb,rnd)
                        if e is None: continue
                        new = e.id not in pos
                        pos[e.id]=e.pos; team[e.id]=e.team; kind[e.id]=e.kind
                        if new and e.kind!="builder_bot":
                            t=e.team
                            if d2(e.pos,home[1-t]) < d2(e.pos,home[t]): builds[t]+=1
                elif un==2:
                    d={k:v for k,_x,v in fields(ubuf)}
                    if 1 in d and 2 in d and d[1] in pos: pos[d[1]]=read_pos(d[2])
                elif un==3:
                    for _rn,_rw,rv in fields(ubuf):
                        pos.pop(rv,None); team.pop(rv,None); kind.pop(rv,None)
        for eid,p in pos.items():
            if kind.get(eid)=="builder_bot":
                t=team[eid]
                if d2(p,home[1-t]) < d2(p,home[t]): rounds[t]+=1
    return rounds, builds, our

def run(arm,label):
    R={0:0,1:0}; B={0:0,1:0}; G=0
    for mid in ids(arm):
        meta=json.loads((AR/f"{mid}.meta.json").read_text())
        our = 0 if meta["teamAId"]==OURS else 1
        for fp in sorted(AR.glob(f"{mid}_game_*.replay26")):
            r=walk(fp,our)
            if r is None: continue
            rr,bb,_=r
            R["us" if False else 0]+=rr[our]; R[1]+=rr[1-our]
            B[0]+=bb[our];  B[1]+=bb[1-our]
            G+=1
    print(f"  {label}  n={G} games")
    for i,who in ((0,"US"),(1,"THEM")):
        d = R[i]/max(B[i],1)
        print(f"     {who:<5} forward builder-rounds {R[i]:>7,}   forward builds {B[i]:>5}"
              f"   DWELL PER BUILD {d:7.1f} rounds")
    if B[0] and B[1]:
        print(f"     ratio ours/theirs = {(R[0]/B[0])/(R[1]/B[1]):.2f}x")
S="/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/f3c65752-78b7-402d-832f-0e9df881f736/scratchpad"
run(f"{S}/arm_ctrl_all.txt","v104 control")
run(f"{S}/arm_loki25.txt","LOKI-25")
