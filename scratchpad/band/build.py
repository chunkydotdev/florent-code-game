import csv, json, collections, statistics, sys
OURID='379a5d80-9921-4c9e-949b-f9b1dcba16be'
OURNAME='OpenSverige'

# ---- 1. ladder_games.tsv -> per-match aggregate
g=collections.defaultdict(list)
for r in csv.DictReader(open('corpus/ladder_games.tsv'),delimiter='\t'):
    g[r['match']].append(r)
print('ladder matches in corpus:', len(g), file=sys.stderr)

M={}
for mid,gs in g.items():
    r0=gs[0]
    wons=[x['won'] for x in gs]
    nw=sum(1 for x in wons if x=='1')
    nl=sum(1 for x in wons if x=='0')
    M[mid]=dict(mid=mid, created=r0['created'], opp=r0['opp'],
                ourver=r0['ourver'], ourbef=float(r0['ourbef']), oppbef=float(r0['oppbef']),
                ngames=len(gs), gw=nw, gl=nl,
                mwin = 1 if nw>nl else (0 if nl>nw else None),
                versets=set(x['ourver'] for x in gs))
# sanity: ourbef/oppbef constant within match?
bad=0
for mid,gs in g.items():
    if len(set(x['ourbef'] for x in gs))>1 or len(set(x['oppbef'] for x in gs))>1: bad+=1
print('matches with varying ourbef/oppbef within match:', bad, file=sys.stderr)
print('matches with mixed ourver:', sum(1 for m in M.values() if len(m['versets'])>1), file=sys.stderr)
print('matches with tied game score:', sum(1 for m in M.values() if m['mwin'] is None), file=sys.stderr)
print('game counts per match:', collections.Counter(m['ngames'] for m in M.values()), file=sys.stderr)

# ---- 2. elo deltas from the two league tapes
delta={}; oppver={}; src={}
for r in csv.DictReader(open('corpus/league_matches.tsv'),delimiter='\t'):
    for s,o in (('A','B'),('B','A')):
        if r['team%sId'%s]==OURID:
            d=r['eloDelta%s'%s]
            if d not in ('None','','null'):
                delta[r['id']]=float(d); src[r['id']]='league_matches'
            oppver[r['id']]=r['team%sVersion'%o]
for r in csv.DictReader(open('corpus/league_elo_log.tsv'),delimiter='\t'):
    if r['triggeredBy']!='ladder': continue
    for s,o in (('A','B'),('B','A')):
        if r['team%sId'%s]==OURID:
            d=r['eloDelta%s'%s]
            if d not in ('None','','null'):
                delta[r['id']]=float(d); src.setdefault(r['id'],'elo_log')
            oppver[r['id']]=r['team%sVersion'%o]
print('elo deltas found for our ladder matches:', len(delta), file=sys.stderr)
cov=sum(1 for mid in M if mid in delta)
print('coverage of the 681 corpus matches:', cov, file=sys.stderr)

for mid,m in M.items():
    m['delta']=delta.get(mid)
    m['oppver']=oppver.get(mid)

# ---- 3. INDEPENDENT delta: consecutive ourbef diffs
rows=sorted(M.values(), key=lambda m:m['created'])
for i,m in enumerate(rows):
    m['delta_tape'] = (rows[i+1]['ourbef']-m['ourbef']) if i+1<len(rows) else None

json.dump(rows, open('scratchpad/band/matches.json','w'), default=str)
print('wrote', len(rows), file=sys.stderr)
