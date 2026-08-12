import json, statistics, collections, math
rows=[m for m in json.load(open('scratchpad/band/matches.json')) if m['delta'] is not None]
rows.sort(key=lambda m:m['created'])
for m in rows:
    m['gap']=m['oppbef']-m['ourbef']; m['day']=m['created'][:10]
    m['E']=1/(1+10**(m['gap']/400.0)); m['S']=m['gw']/5.0
# fit K
num=sum(m['delta']*(m['S']-m['E']) for m in rows); den=sum((m['S']-m['E'])**2 for m in rows)
K=num/den
res=[m['delta']-K*(m['S']-m['E']) for m in rows]
print('Elo model check: delta = K*(S-E), S=game share, E=logistic(400).')
print('  fitted K = %.3f ; residual sd = %.4f ; max |resid| = %.4f  (n=%d)'%(K,statistics.pstdev(res),max(abs(r) for r in res),len(rows)))
print('  -> the ladder scores GAME SHARE, not match wins. A 3-2 win can be negative.')

print('\nPERFORMANCE VS ELO EXPECTATION (S-E), which is net-Elo/K. >0 = outperforming our rating.')
print('%-11s %28s %28s'%('day','opp BELOW us (gap<0)','opp ABOVE us (gap>=0)'))
for d in sorted(set(m['day'] for m in rows)):
    out=[]
    for lo,hi in ((-1e9,0),(0,1e9)):
        s=[m for m in rows if m['day']==d and lo<=m['gap']<hi]
        if not s: out.append('%28s'%'-'); continue
        S=statistics.mean(m['S'] for m in s); E=statistics.mean(m['E'] for m in s)
        out.append('%28s'%('n=%-3d S=%.3f E=%.3f  %+.3f'%(len(s),S,E,S-E)))
    print('%-11s'%d+''.join(out))

print('\nROLLING 100-MATCH BLOCKS (chronological), below-band only (gap<0):')
b=[m for m in rows if m['gap']<0]
print('  below-band matches total: %d'%len(b))
for i in range(0,len(b),50):
    s=b[i:i+50]
    if len(s)<25: 
        print('  block %3d-%3d  n=%d  INSUFFICIENT'%(i,i+len(s),len(s))); continue
    S=statistics.mean(m['S'] for m in s); E=statistics.mean(m['E'] for m in s)
    net=sum(m['delta'] for m in s)
    print('  %s .. %s  n=%d  S=%.3f E=%.3f  S-E=%+.3f  net=%+.1f (%+.2f/m)'%(
        s[0]['created'][5:16],s[-1]['created'][5:16],len(s),S,E,S-E,net,net/len(s)))

print('\nSAME, above-band (gap>=0):')
a=[m for m in rows if m['gap']>=0]
for i in range(0,len(a),50):
    s=a[i:i+50]
    if len(s)<25:
        print('  block %3d-%3d  n=%d  INSUFFICIENT'%(i,i+len(s),len(s))); continue
    S=statistics.mean(m['S'] for m in s); E=statistics.mean(m['E'] for m in s)
    net=sum(m['delta'] for m in s)
    print('  %s .. %s  n=%d  S=%.3f E=%.3f  S-E=%+.3f  net=%+.1f (%+.2f/m)'%(
        s[0]['created'][5:16],s[-1]['created'][5:16],len(s),S,E,S-E,net,net/len(s)))
