import sys, os
from pathlib import Path
sys.path.insert(0,"tools")
from replay_census import fields, read_pos, parse_entity, WIRE_LEN
AR=Path("replay_archive")
fn=sys.argv[1]
data=(AR/fn).read_bytes()
turns=[]
for n,w,v in fields(data):
    if n==3 and w==WIRE_LEN: turns.append(v)
print("turns",len(turns))
from collections import Counter
for rnd in (0,1,2,3,60,61,62,100):
    if rnd>=len(turns): continue
    c=Counter(); det=[]
    for _a,_b,ub in fields(turns[rnd]):
        for un,_w,ubuf in fields(ub):
            c[un]+=1
            if un in (7,8):
                d={k:v for k,_x,v in fields(ubuf)}
                det.append((un,d.get(1),d.get(2,0)))
            if un in (2,13,15,16):
                d={k:v for k,_x,v in fields(ubuf)}
                det.append((un,d.get(1),"pos"))
    print("r",rnd,dict(c))
    print("   ",det[:30])
