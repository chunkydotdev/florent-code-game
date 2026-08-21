"""Two driven validations of the facing decode. Read-only.
V1  BC gunner rotations/game -- known cell: study says v47 2.0 -> v68 8.1.
V2  MIRROR-FACING PLACEBO: BC belt tiles that die on an opp turret's REAL line
    vs on the SAME turret's line with facing flipped 180 deg (same length, same
    geometry, wrong aim). If the decode is blind, the two must be equal."""
import sys, json, time, collections
sys.path.insert(0,'tools')
from pathlib import Path
from replay_census import fields, read_pos, parse_entity, WIRE_LEN, DIRECTION_DELTA, ENV_WALL

FR={}
for l in open('scratchpad/s53_bean_census.jsonl'):
    r=json.loads(l); FR[r['file']]=(r['bc'], r['ver'])
VERS={'47','68'}
files=sorted(f for f,v in FR.items() if v[1] in VERS)
RANGE={'gunner':13,'sentinel':32}; BELT={'conveyor','splitter'}; TUR={'gunner','sentinel'}
OPPDIR={0:0,1:5,2:6,3:7,4:8,5:1,6:2,7:3,8:4}   # 180 deg flip

rot=collections.Counter(); games=collections.Counter()
V2=collections.Counter()
t0=time.time()
for f in files:
    data=(Path('replay_archive')/f).read_bytes()
    bc,ver=FR[f]; opp=1-bc
    map_buf=None; turns=[]
    for num,wire,val in fields(data):
        if num==1 and wire==WIRE_LEN: map_buf=val
        elif num==3 and wire==WIRE_LEN: turns.append(val)
    W=H=0; tiles=[]
    for num,wire,val in fields(map_buf):
        if num==1: W=val
        elif num==2: H=val
        elif num==3:
            row=[]
            for rn,rw,rv in fields(val):
                if rn==1:
                    if rw==WIRE_LEN:
                        i=0
                        while i<len(rv):
                            r_=s=0
                            while True:
                                b=rv[i]; i+=1; r_|=(b&0x7F)<<s
                                if not (b&0x80): break
                                s+=7
                            row.append(r_)
                    else: row.append(rv)
            tiles.append(row)
    def env(x,y):
        if 0<=y<len(tiles) and 0<=x<len(tiles[y]): return tiles[y][x]
        return ENV_WALL
    ents={}; occ={}; bots=collections.Counter(); belts=set(); beltid={}; turr={}
    games[ver]+=1
    def ray(pos,kind,dirn):
        d=DIRECTION_DELTA.get(dirn or 0,(0,0))
        if d==(0,0): return []
        R=RANGE[kind]; x,y=pos; res=[]; k=1
        while True:
            nx,ny=x+d[0]*k,y+d[1]*k
            if (nx-x)**2+(ny-y)**2>R or not (0<=nx<W and 0<=ny<H): break
            res.append((nx,ny))
            if kind=='gunner':
                if env(nx,ny)==ENV_WALL: break
                if (nx,ny) in occ or bots[(nx,ny)]: break
            k+=1
        return res
    for rnd,tb in enumerate(turns):
        for _n,_w,ub in fields(tb):
            for unum,_uw,ubuf in fields(ub):
                if unum==1:
                    for en,_ew,ebuf in fields(ubuf):
                        if en!=1: continue
                        e=parse_entity(ebuf,rnd)
                        if e is None: continue
                        if e.id in ents:
                            st=ents[e.id]
                            if st['kind'] in TUR and e.direction is not None and e.direction!=st['dir']:
                                st['dir']=e.direction
                                if st['team']==bc: rot[(ver,st['kind'])]+=1
                            continue
                        ents[e.id]={'team':e.team,'kind':e.kind,'pos':e.pos,'dir':e.direction}
                        if e.kind=='builder_bot': bots[e.pos]+=1
                        else: occ[e.pos]=e.id
                        if e.team==bc and e.kind in BELT: belts.add(e.pos); beltid[e.id]=e.pos
                        if e.team==opp and e.kind in TUR: turr[e.id]=ents[e.id]
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
                        p=st['pos']
                        if st['kind']=='builder_bot':
                            bots[p]-=1
                            if bots[p]<=0: bots.pop(p,None)
                        else:
                            if occ.get(p)==rv: occ.pop(p,None)
                        if rv in beltid:
                            belts.discard(beltid.pop(rv))
                            for tid,ts in turr.items():
                                if tid not in ents: continue
                                if p in ray(ts['pos'],ts['kind'],ts['dir']): V2[(ver,'real')]+=1
                                if p in ray(ts['pos'],ts['kind'],OPPDIR.get(ts['dir'] or 0,0)): V2[(ver,'mirror')]+=1
                        turr.pop(rv,None)
print('V1 BC turret rotations per game (known cell: gunner 2.0 v47 -> 8.1 v68)')
for ver in ('47','68'):
    for k in ('gunner','sentinel'):
        print(f'   v{ver} {k}: {rot[(ver,k)]/games[ver]:.2f}/game  (n={games[ver]} games, {rot[(ver,k)]} events)')
print('V2 MIRROR-FACING PLACEBO -- BC belt deaths on an opp turret ray')
for ver in ('47','68'):
    r=V2[(ver,'real')]; m=V2[(ver,'mirror')]
    print(f'   v{ver}: real-facing {r}   mirror-facing {m}   ratio {r/max(m,1):.2f}x')
print('%.1fs'%(time.time()-t0))
