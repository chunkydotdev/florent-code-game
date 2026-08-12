"""COMPLEMENT CONTROL for CONTROL 4: is BotOutput.tled ever TRUE anywhere?
A constant-zero column validates anything (corpus-howto TRAP 8)."""
import sys
from pathlib import Path
from collections import Counter
sys.path.insert(0,"tools")
from replay_census import fields, WIRE_LEN
AR=Path("replay_archive")
files=sorted(AR.glob("*.replay26"))[:1200]
c=Counter(); et=[]
for fp in files:
    data=fp.read_bytes()
    for n,w,v in fields(data):
        if n!=3 or w!=WIRE_LEN: continue
        for _a,_b,ub in fields(v):
            for un,_w2,ubuf in fields(ub):
                if un!=9: continue
                d={k:x for k,_y,x in fields(ubuf)}
                c["botoutput"]+=1
                if d.get(4,0): c["tled_true"]+=1
                if 3 in d:
                    c["has_exectime"]+=1
                    et.append(d[3])
print("files scanned:",len(files))
print(dict(c))
if et:
    et.sort()
    print("execTimeUs: n=%d  median=%d  p99=%d  max=%d"%(len(et),et[len(et)//2],et[int(len(et)*.99)],et[-1]))
