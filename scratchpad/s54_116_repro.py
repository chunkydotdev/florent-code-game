"""KNOWN-CELL REPRODUCTION: base study's forward-turret clearance (79.7% BC v47).
Definition (base study, REPLAY-STUDY-beancounters-v47v68 s6.2/s3.6):
  forward turret = gunner/sentinel built closer to the DEFENDER's core than to its own
  removal       = a death of that kind on that tile at a later round
Read-only."""
import json, csv, collections, math, statistics

FR={}
for l in open('scratchpad/s53_bean_census.jsonl'):
    r=json.loads(l); FR[r['file']]=(r['bc'], r['ver'])

G=collections.defaultdict(list)
for r in csv.DictReader(open('scratchpad/s54_116_bc_events.tsv'),delimiter='\t'):
    G[r['file']].append(r)

def pair(rows, kinds):
    """positional pairing: (team,kind,tile) build -> first later death of same key"""
    builds=collections.defaultdict(list); deaths=collections.defaultdict(list)
    for r in rows:
        if r['kind'] not in kinds: continue
        k=(r['team'],r['kind'],r['x'],r['y'])
        (builds if r['ev']=='BUILD' else deaths)[k].append(int(r['rnd']))
    out=[]
    for k,bs in builds.items():
        ds=sorted(deaths.get(k,[])); bs=sorted(bs); di=0
        for b in bs:
            while di<len(ds) and ds[di]<=b: di+=1
            d = ds[di] if di<len(ds) else None
            if d is not None: di+=1
            out.append((k,b,d))
    return out

TUR={'gunner','sentinel'}
stat=collections.defaultdict(lambda: [0,0,set()])   # key -> [n_turrets, n_removed, games]
per_game=collections.defaultdict(list)
for f,rows in G.items():
    bc,ver=FR[f]
    for (team,kind,x,y),b,d in pair(rows,TUR):
        # forward?  compare d2 to own core vs enemy core, from the BUILD row
        pass
# need d2 columns: redo pairing keeping the build row
def pair_rows(rows,kinds):
    builds=collections.defaultdict(list); deaths=collections.defaultdict(list)
    for r in rows:
        if r['kind'] not in kinds: continue
        k=(r['team'],r['kind'],r['x'],r['y'])
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
            out.append((br,b,d))
    return out

cells=collections.defaultdict(lambda: [0,0])
games=collections.defaultdict(set)
gm=collections.defaultdict(lambda: collections.defaultdict(lambda:[0,0]))
for f,rows in G.items():
    bc,ver=FR[f]
    for br,b,d in pair_rows(rows,TUR):
        t=int(br['team']); own=int(br['d2_own']); enemy=int(br['d2_enemy'])
        if enemy>=own: continue          # not forward
        defender = 'BC' if (1-t)==bc else 'OPP'
        key=(ver,defender)
        cells[key][0]+=1; cells[key][1]+= (1 if d is not None else 0)
        games[key].add(f)
        gm[key][f][0]+=1; gm[key][f][1]+= (1 if d is not None else 0)

def deff_hw(p, n, deff=1.833):
    return 1.96*math.sqrt(max(p*(1-p),1e-9)*deff/n)

print(f"{'ver':>4} {'defender':>8} {'games':>6} {'turrets':>8} {'pooled':>8} {'gamemean':>9} {'hw(games,DEFF1.833)':>20}")
for key in sorted(cells):
    n,rem=cells[key]; ng=len(games[key])
    pooled=rem/n
    gmeans=[v[1]/v[0] for v in gm[key].values()]
    gmean=statistics.mean(gmeans)
    print(f"{key[0]:>4} {key[1]:>8} {ng:>6} {n:>8} {pooled*100:>7.1f}% {gmean*100:>8.1f}% {deff_hw(gmean,ng)*100:>19.1f}")

# --- half-width estimator check: empirical sd of per-game rates ---------------
print()
for key in sorted(cells):
    gmeans=[v[1]/v[0] for v in gm[key].values()]
    n=len(gmeans); sd=statistics.stdev(gmeans)
    hw_emp=1.96*sd/math.sqrt(n)*math.sqrt(1.833)
    print(f"{key[0]:>4} {key[1]:>8} n={n:<5} sd={sd:.4f}  hw_emp_DEFF={hw_emp*100:.1f}  hw_emp_noDEFF={1.96*sd/math.sqrt(n)*100:.1f}")
