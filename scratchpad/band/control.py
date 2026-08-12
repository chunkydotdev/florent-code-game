import json, statistics, collections, math
rows=json.load(open('scratchpad/band/matches2.json')); rows.sort(key=lambda m:m['created'])
for m in rows:
    m['gap']=m['oppbef']-m['ourbef']; m['E']=1/(1+10**(m['gap']/400.0)); m['S']=m['gw']/5.0
SE=0.287
byopp=collections.defaultdict(list)
for m in rows: byopp[m['oppname']].append(m)

print('CONTROL for the version-boundary scan: is the "decline" pattern just MEAN REVERSION?')
print('  For each opponent with n>=12, first-half S-E vs the H1->H2 change:')
X=[];Y=[]
for n,ms in sorted(byopp.items()):
    if len(ms)<12: continue
    h=len(ms)//2; a,b=ms[:h],ms[h:]
    d1=statistics.mean(m['S'] for m in a)-statistics.mean(m['E'] for m in a)
    d2=statistics.mean(m['S'] for m in b)-statistics.mean(m['E'] for m in b)
    X.append(d1);Y.append(d2-d1)
    print('    %-22s H1 S-E=%+.3f  change %+.3f'%(n,d1,d2-d1))
mx,my=statistics.mean(X),statistics.mean(Y)
r=sum((a-mx)*(c-my) for a,c in zip(X,Y))/math.sqrt(sum((a-mx)**2 for a in X)*sum((c-my)**2 for c in Y))
print('  --> correlation r = %+.3f  (n=%d opponents).'%(r,len(X)))
print('      Strongly negative = the change is REGRESSION TOWARD PARITY, not counter-shipping.')
print('      Mechanism: E is recomputed from ratings that absorb the very results being scored,')
print('      so repeated play with one opponent drives S-E toward 0 with no bot change at all.')

print('\nRAW GAME SHARE S (no Elo adjustment) for the persistent bleeders, chronological halves:')
for n in ('Ouroboros','Lunds Stallions','Powerpuff Girls','Kings College Munich','CtrlAltDefeat','diverge'):
    ms=byopp[n]; h=len(ms)//2; a,b=ms[:h],ms[h:]
    print('  %-22s n=%-3d  S all=%.3f | H1 %.3f (n=%d) -> H2 %.3f (n=%d)  | their versions H1 %s -> H2 %s'%(
        n,len(ms),statistics.mean(m['S'] for m in ms),
        statistics.mean(m['S'] for m in a),len(a),statistics.mean(m['S'] for m in b),len(b),
        sorted(set(int(m['oppver']) for m in a)), sorted(set(int(m['oppver']) for m in b))))

print('\nOUROBOROS DETAIL — the single biggest bleed, and their bot barely moved:')
ms=byopp['Ouroboros']
print('  their versions: ',collections.Counter(m['oppver'] for m in ms))
print('  our versions:   ',sorted(set(int(m['ourver']) for m in ms)))
q=[m for m in ms if m['oppver']=='8']
for i in range(0,len(q),8):
    s=q[i:i+8]
    print('   %s..%s n=%-2d ourver %s  S=%.3f E=%.3f net%+.1f'%(s[0]['created'][5:16],s[-1]['created'][5:16],len(s),
        sorted(set(int(m['ourver']) for m in s)), statistics.mean(m['S'] for m in s),statistics.mean(m['E'] for m in s),
        sum(m['delta'] for m in s)))
mw=sum(1 for m in ms if m['mwin']==1)
print('  match record vs Ouroboros: %d-%d ; games %d-%d ; core_destroyed?'%(mw,len(ms)-mw,sum(m['gw'] for m in ms),sum(m['gl'] for m in ms)))
