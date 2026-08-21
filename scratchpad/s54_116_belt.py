"""CUT #116 - do Bean counters answer an enemy turret in range of their own belt?
Stimulus: an OPP gunner/sentinel whose firing DISC (r2<=13 / <=32) covers a tile
holding a LIVE BC conveyor/splitter, at any round of the turret's life.
Answer  : that turret dies (positional pairing, same kind+tile, later round).
Read-only."""
import json, csv, collections, math, statistics, sys

FR={}
for l in open('scratchpad/s53_bean_census.jsonl'):
    r=json.loads(l); FR[r['file']]=(r['bc'], r['ver'])
G=collections.defaultdict(list)
for r in csv.DictReader(open('scratchpad/s54_116_bc_events.tsv'),delimiter='\t'):
    G[r['file']].append(r)

RANGE={'gunner':13,'sentinel':32}
BELT={'conveyor','splitter'}
TUR={'gunner','sentinel'}
INF=10**9

def lives(rows, kinds, team=None):
    """-> list of (kind,x,y,build,death|None, row)"""
    builds=collections.defaultdict(list); deaths=collections.defaultdict(list)
    for r in rows:
        if r['kind'] not in kinds: continue
        if team is not None and int(r['team'])!=team: continue
        k=(r['team'],r['kind'],int(r['x']),int(r['y']))
        if r['ev']=='BUILD': builds[k].append(r)
        else: deaths[k].append(int(r['rnd']))
    out=[]
    for k,brs in builds.items():
        ds=sorted(deaths.get(k,[])); brs=sorted(brs,key=lambda r:int(r['rnd'])); di=0
        for br in brs:
            b=int(br['rnd'])
            while di<len(ds) and ds[di]<=b: di+=1
            d=ds[di] if di<len(ds) else None
            if d is not None: di+=1
            out.append((k[1],k[2],k[3],b,d,br))
    return out

rows_out=[]
for f,rows in G.items():
    bc,ver=FR[f]
    opp=1-bc
    gend=max(int(r['rnd']) for r in rows)
    belts=lives(rows,BELT,team=bc)
    beltdeaths=[(x,y,d) for (k,x,y,b,d,br) in belts if d is not None]
    turs=lives(rows,TUR,team=opp)
    for kind,x,y,b,d,br in turs:
        R=RANGE[kind]
        end = d if d is not None else gend
        # onset: earliest round in [b,end] with a live BC belt tile in the disc
        onset=None; nbelt=0
        for (bk,bx,by,bb,bd,bbr) in belts:
            if (bx-x)**2+(by-y)**2 > R: continue
            nbelt+=1
            lo=max(b,bb); hi=min(end, (bd-1) if bd is not None else end)
            if lo<=hi:
                onset = lo if onset is None else min(onset,lo)
        # belt tiles that DIED inside the disc during the turret's life
        eaten=sum(1 for (bx,by,bd) in beltdeaths
                  if (bx-x)**2+(by-y)**2<=R and b<=bd<=end)
        fwd = int(br['d2_enemy'])<int(br['d2_own'])     # in BC's half (base-study defn)
        rows_out.append(dict(file=f,ver=ver,kind=kind,x=x,y=y,build=b,death=d,
                             gend=gend,onset=onset,nbelt=nbelt,eaten=eaten,fwd=fwd,
                             d2bc=int(br['d2_enemy']),d2opp=int(br['d2_own'])))

with open('scratchpad/s54_116_turrets.tsv','w') as o:
    w=csv.DictWriter(o,fieldnames=list(rows_out[0].keys()),delimiter='\t')
    w.writeheader()
    for r in rows_out: w.writerow(r)
print('turret-lives',len(rows_out))
