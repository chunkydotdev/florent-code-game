import json, statistics, collections
rows=[m for m in json.load(open('scratchpad/band/matches.json')) if m['delta'] is not None]
rows.sort(key=lambda m:m['created'])
for m in rows:
    m['gap']=m['oppbef']-m['ourbef']; m['day']=m['created'][:10]; m['v']=int(m['ourver'])

print('OUR RATING TAPE (ourbef), by day:')
for d in sorted(set(m['day'] for m in rows)):
    s=[m for m in rows if m['day']==d]
    print('  %s n=%3d  our rating %.0f -> %.0f   opp rating mean %.0f  min %.0f max %.0f'%(
        d,len(s),s[0]['ourbef'],s[-1]['ourbef'],
        statistics.mean(m['oppbef'] for m in s),min(m['oppbef'] for m in s),max(m['oppbef'] for m in s)))

print('\nSIMPLE SPLIT: opponent BELOW us (gap<0) vs ABOVE us (gap>=0), per day')
print('%-11s %19s %19s'%('day','opp BELOW us','opp ABOVE us'))
for d in sorted(set(m['day'] for m in rows)):
    out=[]
    for lo,hi in ((-1e9,0),(0,1e9)):
        s=[m for m in rows if m['day']==d and lo<=m['gap']<hi]
        if not s: out.append('%19s'%'-'); continue
        net=sum(m['delta'] for m in s)
        gs=sum(m['gw'] for m in s)/sum(m['gw']+m['gl'] for m in s)
        out.append('%19s'%('n=%d g%.0f%% net%+.0f'%(len(s),100*gs,net)))
    print('%-11s'%d+''.join(out))

print('\nBY OUR SUBMISSION VERSION (>=15 matches only), gap<0 = opp below us:')
print('%-6s %-17s %5s %6s %6s %8s | %s'%('ver','window','n','below','above','netTOT','below-band detail'))
vs=collections.defaultdict(list)
for m in rows: vs[m['v']].append(m)
for v in sorted(vs):
    s=vs[v]
    if len(s)<15: continue
    b=[m for m in s if m['gap']<0]; a=[m for m in s if m['gap']>=0]
    f=lambda x:('g%.0f%%'%(100*sum(m['gw'] for m in x)/sum(m['gw']+m['gl'] for m in x)) if x else '-')
    nb=sum(m['delta'] for m in b); na=sum(m['delta'] for m in a)
    print('v%-5d %-17s %5d %6s %6s %+8.0f | below n=%d net%+.1f (%+.2f/m)  above n=%d net%+.1f (%+.2f/m)'%(
        v, s[0]['created'][5:16]+'..'+s[-1]['created'][11:16], len(s), f(b), f(a), nb+na,
        len(b), nb, nb/len(b) if b else 0, len(a), na, na/len(a) if a else 0))
