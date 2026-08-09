import sys
sys.path.insert(0,"tools")
from pathlib import Path
from replay_census import fields, read_pos, parse_entity, WIRE_LEN
f=sys.argv[1]
data=Path("replay_archive/"+f).read_bytes()
mb=None; tb=[]
for n,w,v in fields(data):
    if n==1 and w==WIRE_LEN: mb=v
    elif n==3 and w==WIRE_LEN: tb.append(v)
cores=[]
for n,_w,v in fields(mb):
    if n==4:
        c={"id":0,"team":0,"pos":(0,0)}
        for cn,_cw,cv in fields(v):
            if cn==1: c["id"]=cv
            elif cn==2: c["team"]=cv
            elif cn==3: c["pos"]=read_pos(cv)
        cores.append(c)
fp={}
for c in cores:
    x,y=c["pos"]
    for dx in(0,1):
        for dy in(0,1): fp[(x+dx,y+dy)]=c["team"]
team_of={c["id"]:c["team"] for c in cores}; kind_of={c["id"]:"core" for c in cores}
bldg={}; pos_of={c["id"]:c["pos"] for c in cores}
for c in cores:
    for p,t in fp.items():
        if t==c["team"]: bldg[p]=c["id"]
known=0; unknown=0; unk_kinds={}
ANY={};SAME={};X={};EX=[]
for rnd,turn in enumerate(tb):
    for _n,_w,ub in fields(turn):
        for un,_uw,u in fields(ub):
            if un==1:
                for en,_ew,eb in fields(u):
                    if en!=1: continue
                    e=parse_entity(eb,rnd)
                    if e is None: continue
                    if e.id in pos_of:
                        old=pos_of[e.id]
                        if old!=e.pos and kind_of.get(e.id)!="builder_bot":
                            if bldg.get(old)==e.id: del bldg[old]
                            bldg[e.pos]=e.id; pos_of[e.id]=e.pos
                        continue
                    team_of[e.id]=e.team; kind_of[e.id]=e.kind; pos_of[e.id]=e.pos
                    if e.kind!="builder_bot": bldg[e.pos]=e.id
            elif un==3:
                for _rn,_rw,rv in fields(u):
                    if rv in pos_of:
                        p=pos_of.pop(rv)
                        if kind_of.get(rv)!="builder_bot" and bldg.get(p)==rv: del bldg[p]
            elif un==4:
                for rn,_rw,rv in fields(u):
                    if rn!=1: continue
                    frm=to=None
                    for mn,_mw,mv in fields(rv):
                        if mn==1: frm=read_pos(mv)
                        elif mn==2: to=read_pos(mv)
                    if frm is None or to is None: continue
                    src=bldg.get(frm)
                    if src is None:
                        unknown+=1
                        if to in fp: unk_kinds[("to_core",fp[to])]=unk_kinds.get(("to_core",fp[to]),0)+1
                        else: unk_kinds["to_other"]=unk_kinds.get("to_other",0)+1
                    else: known+=1
                    if to in fp:
                        tt=fp[to]; ANY[tt]=ANY.get(tt,0)+1
                        st=team_of.get(src)
                        if st==tt: SAME[tt]=SAME.get(tt,0)+1
                        else:
                            k=(kind_of.get(src),st,tt)
                            X[k]=X.get(k,0)+1
                            if len(EX)<6: EX.append((rnd,frm,to,kind_of.get(src),st,tt))
print(f"{f}: moves with known source {known}, UNKNOWN source {unknown}")
print("  into-core ANY source:",ANY," SAME-team source:",SAME)
print("  cross-team into-core by (srckind,srcteam,coreteam):",X)
print("  examples:",EX)
