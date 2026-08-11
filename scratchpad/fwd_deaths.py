"""LOKI-25 bar 5a/5b/5d: forward builder deaths and forward presence, ours.

5a DOSE  - forward builder deaths per game must DIFFER from control.
5b MECH  - deaths per 1,000 forward builder-rounds (exposure-normalised, the
           form that survives the pooling error research corrected).
5d FALSIFIER - forward presence must NOT fall. If raiders dodge gunner axes by
           not going forward, the plank bought survival by abandoning the
           assault. That is the most likely way this dies and it is checked
           FIRST-CLASS, not as a footnote.
"""
import csv, json, sys
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
    om=[c for t,c in cores if t==our]; em=[c for t,c in cores if t!=our]
    if not om or not em: return None
    oc, ec = om[0], em[0]
    d2=lambda a,b:(a[0]-b[0])**2+(a[1]-b[1])**2
    pos={}; team={}; kind={}
    deaths=0; fwd_rounds=0; fwd_builds=0
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
                        if new and e.team==our and e.kind!="builder_bot" and d2(e.pos,ec)<d2(e.pos,oc):
                            fwd_builds+=1
                elif un==2:
                    d={k:v for k,_x,v in fields(ubuf)}
                    if 1 in d and 2 in d and d[1] in pos: pos[d[1]]=read_pos(d[2])
                elif un==3:
                    for _rn,_rw,rv in fields(ubuf):
                        if team.get(rv)==our and kind.get(rv)=="builder_bot":
                            p=pos.get(rv)
                            if p and d2(p,ec)<d2(p,oc): deaths+=1
                        pos.pop(rv,None); team.pop(rv,None); kind.pop(rv,None)
        for eid,p in pos.items():
            if team.get(eid)==our and kind.get(eid)=="builder_bot" and d2(p,ec)<d2(p,oc):
                fwd_rounds+=1
    return deaths, fwd_rounds, fwd_builds, len(turns)

def run(arm, label):
    D=R=B=0; G=0
    for mid in ids(arm):
        meta=json.loads((AR/f"{mid}.meta.json").read_text())
        our = 0 if meta["teamAId"]==OURS else 1
        for fp in sorted(AR.glob(f"{mid}_game_*.replay26")):
            r=walk(fp,our)
            if r is None: continue
            D+=r[0]; R+=r[1]; B+=r[2]; G+=1
    print(f"  {label:<22} n={G:>3} games")
    print(f"     5a fwd builder DEATHS/game     {D/max(G,1):8.2f}   (total {D})")
    print(f"     5b deaths / 1k fwd bot-rounds  {1000*D/max(R,1):8.2f}   (exposure {R:,} rounds)")
    print(f"     5d FORWARD BUILDS/game         {B/max(G,1):8.2f}   <- must NOT fall")
S="/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/f3c65752-78b7-402d-832f-0e9df881f736/scratchpad"
run(f"{S}/arm_loki25.txt","LOKI-25 (v111)")
run(f"{S}/arm_ctrl_all.txt","v104 control")
