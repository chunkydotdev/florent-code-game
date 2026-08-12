import sys
from pathlib import Path
from collections import Counter, defaultdict
sys.path.insert(0,"tools")
from replay_census import fields, read_pos, parse_entity, WIRE_LEN
AR=Path("replay_archive")
vals=Counter(); mvals=Counter(); spawn=Counter()
gaps=Counter(); mgaps=Counter()
import itertools
files=sorted(AR.glob("*.replay26"))[:6]
for fp in files:
    data=fp.read_bytes(); turns=[]
    for n,w,v in fields(data):
        if n==3 and w==WIRE_LEN: turns.append(v)
    kind={}
    last_act=defaultdict(lambda:None); last_mv=defaultdict(lambda:None)
    for rnd,tb in enumerate(turns):
        for _a,_b,ub in fields(tb):
            for un,_w,ubuf in fields(ub):
                if un==1:
                    for en,_e,eb in fields(ubuf):
                        if en!=1: continue
                        e=parse_entity(eb,rnd)
                        if e is None: continue
                        kind[e.id]=e.kind
                        if e.kind=="builder_bot":
                            d={k:v for k,_x,v in fields(eb)}
                            sub=d.get(10,b"")
                            s={k:v for k,_x,v in fields(sub)} if sub else {}
                            spawn[(s.get(1,0),s.get(2,0))]+=1
                elif un in (7,8):
                    d={k:v for k,_x,v in fields(ubuf)}
                    i=d.get(1); v2=d.get(2,0)
                    if kind.get(i)=="builder_bot":
                        (vals if un==7 else mvals)[v2]+=1
                elif un in (13,15,16):
                    d={k:v for k,_x,v in fields(ubuf)}
                    i=d.get(1)
                    if last_act[i] is not None: gaps[rnd-last_act[i]]+=1
                    last_act[i]=rnd
                elif un==2:
                    d={k:v for k,_x,v in fields(ubuf)}
                    i=d.get(1)
                    if last_mv[i] is not None: mgaps[rnd-last_mv[i]]+=1
                    last_mv[i]=rnd
print("SetActionCooldown values (builders):",dict(vals))
print("SetMoveCooldown values (builders):",dict(mvals))
print("spawn (actionCd,moveCd):",dict(spawn))
print("gap between consecutive ACTIONS:",dict(sorted(gaps.items())[:8]))
print("gap between consecutive MOVES:",dict(sorted(mgaps.items())[:8]))
