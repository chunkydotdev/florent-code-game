import json, statistics, collections
rows=[m for m in json.load(open('scratchpad/band/matches.json')) if m['delta'] is not None]
rows.sort(key=lambda m:m['created'])
gaps=[m['oppbef']-m['ourbef'] for m in rows]
gaps.sort()
print('n=%d ladder matches (OpenSverige), %s -> %s'%(len(rows),rows[0]['created'][:16],rows[-1]['created'][:16]))
print('opp_rating - our_rating (contemporaneous, from ladder_games ourbef/oppbef):')
for q in (0,1,5,10,25,50,75,90,95,99,100):
    print('   p%-3d %+8.1f'%(q,gaps[min(len(gaps)-1,int(q/100*len(gaps)))]))
print('   mean %+.1f  sd %.1f'%(statistics.mean(gaps),statistics.pstdev(gaps)))
print()
B=[('< us-300',-1e9,-300),('us-300..-100',-300,-100),('us-100..+100',-100,100),('us+100..+400',100,400),('> us+400',400,1e9)]
c=collections.Counter()
for m in rows:
    d=m['oppbef']-m['ourbef']
    for lab,lo,hi in B:
        if lo<=d<hi: c[lab]+=1
print('EXPOSURE over all %d rated ladder matches:'%len(rows))
for lab,_,_ in B: print('   %-14s %4d  %5.1f%%'%(lab,c[lab],100*c[lab]/len(rows)))
print()
print('Elo delta vs game score (is it game-share based?):')
d=collections.defaultdict(list)
for m in rows: d[(m['gw'],m['gl'])].append(m['delta'])
for k in sorted(d): print('   %d-%d  n=%3d  mean delta %+7.3f  min %+7.3f max %+7.3f'%(k[0],k[1],len(d[k]),statistics.mean(d[k]),min(d[k]),max(d[k])))
