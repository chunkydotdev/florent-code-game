"""V3: FireTurret decode validation.
  (a) known cell - BC turret shots/game (study: gunner shots 38/game v47 -> 68 v68;
      'they fire 75/game')
  (b) driven control - shots whose TARGET tile holds one of the SHOOTER's OWN
      entities. Friendly fire is not a thing any bot does; this must read ~0."""
import sys, json, time, collections
sys.path.insert(0,'tools')
from pathlib import Path
from replay_census import fields, read_pos, parse_entity, WIRE_LEN
FR={}
for l in open('scratchpad/s53_bean_census.jsonl'):
    r=json.loads(l); FR[r['file']]=(r['bc'], r['ver'])
files=sorted(f for f,v in FR.items() if v[1] in {'47','68'})
C=collections.Counter(); G=collections.Counter()
t0=time.time()
for f in files:
    data=(Path('replay_archive')/f).read_bytes()
    bc,ver=FR[f]; G[ver]+=1
    turns=[]
    for num,wire,val in fields(data):
        if num==3 and wire==WIRE_LEN: turns.append(val)
    ents={}; occ={}; bots=collections.Counter()
    for rnd,tb in enumerate(turns):
        occ0=dict(occ)
        for _n,_w,ub in fields(tb):
            for unum,_uw,ubuf in fields(ub):
                if unum==1:
                    for en,_ew,ebuf in fields(ubuf):
                        if en!=1: continue
                        e=parse_entity(ebuf,rnd)
                        if e is None or e.id in ents: continue
                        ents[e.id]={'team':e.team,'kind':e.kind,'pos':e.pos}
                        if e.kind=='builder_bot': bots[e.pos]+=1
                        else: occ[e.pos]=e.id
                elif unum==2:
                    eid=to=None
                    for mn,_mw,mv in fields(ubuf):
                        if mn==1: eid=mv
                        elif mn==2: to=read_pos(mv)
                    st=ents.get(eid)
                    if st and to:
                        if st['kind']=='builder_bot':
                            bots[st['pos']]-=1
                            if bots[st['pos']]<=0: bots.pop(st['pos'],None)
                            bots[to]+=1
                        else:
                            occ.pop(st['pos'],None); occ[to]=eid
                        st['pos']=to
                elif unum==3:
                    for rn,_rw,rv in fields(ubuf):
                        st=ents.pop(rv,None)
                        if st is None: continue
                        if st['kind']=='builder_bot':
                            bots[st['pos']]-=1
                            if bots[st['pos']]<=0: bots.pop(st['pos'],None)
                        elif occ.get(st['pos'])==rv: occ.pop(st['pos'],None)
                elif unum==12:
                    frm=to=None
                    for fn,_fw,fv in fields(ubuf):
                        if fn==1: frm=read_pos(fv)
                        elif fn==2: to=read_pos(fv)
                    sh=ents.get(occ0.get(frm)) if frm else None
                    if sh is None: C[(ver,'unattrib')]+=1; continue
                    who='BC' if sh['team']==bc else 'OPP'
                    C[(ver,who,sh['kind'])]+=1
                    tgt=ents.get(occ0.get(to)) if to else None
                    if tgt is not None and tgt['team']==sh['team']: C[(ver,who,'FRIENDLY')]+=1
for ver in ('47','68'):
    n=G[ver]
    g=C[(ver,'BC','gunner')]; s=C[(ver,'BC','sentinel')]
    print(f"v{ver} n={n} games | BC gunner shots/game {g/n:.1f}  sentinel {s/n:.1f}  total {(g+s)/n:.1f}"
          f" | OPP total/game {(C[(ver,'OPP','gunner')]+C[(ver,'OPP','sentinel')])/n:.1f}"
          f" | unattributed shooter {C[(ver,'unattrib')]}"
          f" | CONTROL friendly-fire targets: BC {C[(ver,'BC','FRIENDLY')]} OPP {C[(ver,'OPP','FRIENDLY')]}")
print('%.1fs'%(time.time()-t0))
