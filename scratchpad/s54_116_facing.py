"""CUT #116 facing-aware probe. Read-only.

Per OPP gunner/sentinel life in the frozen Bean counters set, emits:
  - build/death round (BY ENTITY ID, not positional), game end
  - onset_disc : first round a LIVE BC conveyor/splitter sits inside the turret's
                 firing DISC (r2<=13 gunner / <=32 sentinel)
  - onset_line : first round the turret's ACTUAL FIRING LINE (facing, rotations
                 tracked via placeEntity re-emit) covers a live BC belt tile.
                 gunner: walk the facing ray, stop at the first occupied tile or
                 wall -- that tile is what get_gunner_target() would return.
                 sentinel: any belt tile on the ray (line ignores obstacles).
  - onset_kill : first round a BC belt tile that was on this turret's LINE dies.
  - rounds at risk in each state + the state at the round of death (hazard input)
Writes scratchpad/s54_116_facing.tsv
"""
import sys, json, csv, time, collections
sys.path.insert(0,'tools')
from pathlib import Path
from replay_census import fields, read_pos, parse_entity, WIRE_LEN, DIRECTION_DELTA, ENV_WALL

FR={}
for l in open('scratchpad/s53_bean_census.jsonl'):
    r=json.loads(l); FR[r['file']]=(r['bc'], r['ver'])
VERS=set(sys.argv[1].split(',')) if len(sys.argv)>1 else {'47','68'}
files=sorted(f for f,v in FR.items() if v[1] in VERS)

RANGE={'gunner':13,'sentinel':32}
BELT={'conveyor','splitter'}
TUR={'gunner','sentinel'}

out=open('scratchpad/s54_116_facing.tsv','w')
cols=['file','ver','eid','kind','x','y','build','death','gend','fwd','d2bc','d2opp',
      'onset_disc','onset_line','onset_kill','line_kills','disc_kills',
      'rr_none','rr_disc','rr_line','rr_kill','state_at_death','rot',
      'rr_cov','rr_aim','first_cov','first_aim','shots','batk','first_shot','first_batk']
out.write('\t'.join(cols)+'\n')
HZ=collections.Counter(); RRAGE=collections.Counter()
def agebucket(a):
    return '0-9' if a<10 else '10-24' if a<25 else '25-49' if a<50 else '50-99' if a<100 else '100+'
t0=time.time(); nf=0; err=0
for f in files:
    try:
        data=(Path('replay_archive')/f).read_bytes()
    except Exception:
        err+=1; continue
    bc,ver=FR[f]; opp=1-bc
    map_buf=None; turns=[]
    for num,wire,val in fields(data):
        if num==1 and wire==WIRE_LEN: map_buf=val
        elif num==3 and wire==WIRE_LEN: turns.append(val)
    if map_buf is None: err+=1; continue
    W=H=0; tiles=[]; cores=[]
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
        elif num==4:
            c={'team':0,'pos':(0,0)}
            for cn,_cw,cv in fields(val):
                if cn==2: c['team']=cv
                elif cn==3: c['pos']=read_pos(cv)
            cores.append(c)
    if len(cores)!=2: err+=1; continue
    corepos={c['team']:c['pos'] for c in cores}
    def env(x,y):
        if 0<=y<len(tiles) and 0<=x<len(tiles[y]): return tiles[y][x]
        return ENV_WALL
    bcturr={}        # id -> BC turret ent (live)
    ents={}          # id -> dict(team,kind,pos,dir)
    occ={}           # pos -> id (buildings)
    bots=collections.Counter()   # pos -> n builder bots
    belts=set()      # BC belt tiles (live)
    beltid={}        # id -> pos for BC belts
    turrets={}       # id -> state dict
    fin=[]
    gend=len(turns)-1

    def ray_of(st):
        d=DIRECTION_DELTA.get(st.get('dir') or 0,(0,0))
        if d==(0,0): return []
        R=RANGE[st['kind']]; x,y=st['pos']; res=[]; k=1
        while True:
            nx,ny=x+d[0]*k,y+d[1]*k
            if (nx-x)**2+(ny-y)**2>R or not (0<=nx<W and 0<=ny<H): break
            res.append((nx,ny))
            if st['kind']=='gunner':
                if env(nx,ny)==ENV_WALL: break
                if (nx,ny) in occ or bots[(nx,ny)]: break
            k+=1
        return res

    def line_tiles(st):
        d=DIRECTION_DELTA.get(st['dir'] or 0,(0,0))
        if d==(0,0): return []
        R=RANGE[st['kind']]; x,y=st['pos']; res=[]
        k=1
        while True:
            nx,ny=x+d[0]*k, y+d[1]*k
            if (nx-x)**2+(ny-y)**2>R: break
            if not (0<=nx<W and 0<=ny<H): break
            res.append((nx,ny))
            if st['kind']=='gunner':
                if env(nx,ny)==ENV_WALL: break
                if (nx,ny) in occ or bots[(nx,ny)]: break   # first blocker = target
            k+=1
        return res

    for rnd,tb in enumerate(turns):
        occ0=dict(occ)                    # ROUND-START occupancy (replay_schema.md:217 trap)
        for _n,_w,ub in fields(tb):
            for unum,_uw,ubuf in fields(ub):
                if unum==1:
                    for en,_ew,ebuf in fields(ubuf):
                        if en!=1: continue
                        e=parse_entity(ebuf,rnd)
                        if e is None: continue
                        if e.id in ents:                        # rotate re-emit
                            st=ents[e.id]
                            if st['kind'] in TUR and e.direction is not None and e.direction!=st['dir']:
                                st['dir']=e.direction
                                if e.id in turrets:
                                    turrets[e.id]['rot']+=1
                                    turrets[e.id]['dir']=e.direction
                            continue
                        ents[e.id]={'team':e.team,'kind':e.kind,'pos':e.pos,'dir':e.direction}
                        if e.kind=='builder_bot': bots[e.pos]+=1
                        else: occ[e.pos]=e.id
                        if e.team==bc and e.kind in BELT:
                            belts.add(e.pos); beltid[e.id]=e.pos
                        if e.team==bc and e.kind in TUR:
                            bcturr[e.id]=ents[e.id]
                        if e.team==opp and e.kind in TUR:
                            own=corepos[opp]; en_=corepos[bc]
                            turrets[e.id]=dict(kind=e.kind,pos=e.pos,build=rnd,death=None,
                                d2bc=(e.pos[0]-en_[0])**2+(e.pos[1]-en_[1])**2,
                                d2opp=(e.pos[0]-own[0])**2+(e.pos[1]-own[1])**2,
                                onset_disc=None,onset_line=None,onset_kill=None,
                                line_kills=0,disc_kills=0,
                                rr={'none':0,'disc':0,'line':0,'kill':0},
                                state=None,rot=0,lineset=set(),dir=e.direction,
                                rr_cov=0,rr_aim=0,first_cov=None,first_aim=None,
                                shots=0,batk=0,first_shot=None,first_batk=None)
                elif unum==2:
                    eid=to=None
                    for mn,_mw,mv in fields(ubuf):
                        if mn==1: eid=mv
                        elif mn==2: to=read_pos(mv)
                    st=ents.get(eid)
                    if st and to:
                        if st['kind']=='builder_bot':
                            bots[st['pos']]-=1
                            if bots[st['pos']]<=0: del bots[st['pos']]
                            bots[to]+=1
                        else:
                            occ.pop(st['pos'],None); occ[to]=eid
                        st['pos']=to
                elif unum==12 or unum==13:
                    a=b_=None
                    for fn,_fw,fv in fields(ubuf):
                        if fn==1: a=fv
                        elif fn==2: b_=read_pos(fv)
                    if b_ is None: continue
                    if unum==12:
                        frm=read_pos(a) if a is not None else None
                        sh=occ0.get(frm) if frm else None
                        shooter=ents.get(sh) if sh else None
                        if shooter is None or shooter['team']!=bc: continue
                    else:
                        at=ents.get(a)
                        if at is None or at['team']!=bc: continue
                    tid=occ0.get(b_)
                    if tid in turrets and turrets[tid]['death'] is None:
                        ts=turrets[tid]
                        if unum==12:
                            ts['shots']+=1
                            if ts['first_shot'] is None: ts['first_shot']=rnd
                        else:
                            ts['batk']+=1
                            if ts['first_batk'] is None: ts['first_batk']=rnd
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
                            for tid,ts in turrets.items():
                                if ts['death'] is not None: continue
                                dd=(p[0]-ts['pos'][0])**2+(p[1]-ts['pos'][1])**2
                                if dd<=RANGE[ts['kind']]:
                                    ts['disc_kills']+=1
                                if p in ts['lineset']:
                                    ts['line_kills']+=1
                                    if ts['onset_kill'] is None: ts['onset_kill']=rnd
                        bcturr.pop(rv,None)
                        if rv in turrets:
                            turrets[rv]['death']=rnd
        # ---- end-of-round state for every live opp turret ----
        for tid,ts in turrets.items():
            if ts['death'] is not None and ts['death']<rnd: continue
            if ts['build']>rnd: continue
            R=RANGE[ts['kind']]; x,y=ts['pos']
            indisc=any((bx-x)**2+(by-y)**2<=R for (bx,by) in belts)
            lt=line_tiles(ts); ts['lineset']=set(lt)
            inline=any(t in belts for t in lt)
            if indisc and ts['onset_disc'] is None: ts['onset_disc']=rnd
            if inline and ts['onset_line'] is None: ts['onset_line']=rnd
            state = 'kill' if ts['onset_kill'] is not None else ('line' if inline else ('disc' if indisc else 'none'))
            ts['rr'][state]+=1
            ab=agebucket(rnd-ts['build'])
            RRAGE[(ver,state,ab)]+=1
            if ts['death']==rnd: HZ[(ver,state,ab)]+=1
            cov=aim=False
            for bid,bs in bcturr.items():
                if bid not in ents: continue
                bx,by=bs['pos']
                if (bx-x)**2+(by-y)**2<=RANGE[bs['kind']]:
                    cov=True
                    if (x,y) in ray_of(bs): aim=True; break
            if cov:
                ts['rr_cov']+=1
                if ts['first_cov'] is None: ts['first_cov']=rnd
            if aim:
                ts['rr_aim']+=1
                if ts['first_aim'] is None: ts['first_aim']=rnd
            if ts['death']==rnd: ts['state']=state
    for tid,ts in turrets.items():
        out.write('\t'.join(str(v) for v in [
            f,ver,tid,ts['kind'],ts['pos'][0],ts['pos'][1],ts['build'],
            '' if ts['death'] is None else ts['death'], gend,
            int(ts['d2bc']<ts['d2opp']), ts['d2bc'], ts['d2opp'],
            '' if ts['onset_disc'] is None else ts['onset_disc'],
            '' if ts['onset_line'] is None else ts['onset_line'],
            '' if ts['onset_kill'] is None else ts['onset_kill'],
            ts['line_kills'], ts['disc_kills'],
            ts['rr']['none'],ts['rr']['disc'],ts['rr']['line'],ts['rr']['kill'],
            ts['state'] or '', ts['rot'], ts['rr_cov'], ts['rr_aim'],
            '' if ts['first_cov'] is None else ts['first_cov'],
            '' if ts['first_aim'] is None else ts['first_aim'],
            ts['shots'], ts['batk'],
            '' if ts['first_shot'] is None else ts['first_shot'],
            '' if ts['first_batk'] is None else ts['first_batk']])+'\n')
    nf+=1
    if nf%200==0: print(f'  ...{nf}/{len(files)} {time.time()-t0:.0f}s',file=sys.stderr,flush=True)
out.close()
with open('scratchpad/s54_116_hazard_age.tsv','w') as h:
    h.write('ver\tstate\tage\trounds\tremovals\n')
    for k in sorted(RRAGE):
        h.write(f'{k[0]}\t{k[1]}\t{k[2]}\t{RRAGE[k]}\t{HZ[k]}\n')
print(f'files {nf} err {err} {time.time()-t0:.1f}s')
