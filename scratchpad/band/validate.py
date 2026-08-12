import json, statistics, collections
rows=json.load(open('scratchpad/band/matches.json'))
both=[m for m in rows if m['delta'] is not None and m['delta_tape'] is not None]
err=[abs(m['delta']-m['delta_tape']) for m in both]
print('A) official eloDelta vs consecutive-ourbef tape, n=%d'%len(both))
print('   median |err| %.4f  p90 %.4f  max %.4f'%(statistics.median(err),sorted(err)[int(.9*len(err))],max(err)))
print('   within 0.01: %d (%.1f%%)'%(sum(1 for e in err if e<0.01),100*sum(1 for e in err if e<0.01)/len(err)))
big=[m for m in both if abs(m['delta']-m['delta_tape'])>0.5]
print('   mismatches >0.5:',len(big))
for m in big[:6]: print('    ',m['created'],m['opp'],'off=%.2f tape=%.2f'%(m['delta'],m['delta_tape']))

print()
print('B) FALSIFIER: does sign of delta track the result? (a constant/garbage column would not)')
c=collections.Counter()
for m in rows:
    if m['delta'] is None: continue
    c[(m['mwin'], m['delta']>0)]+=1
print('  ',dict(c))
print('   wins with delta>0: %d/%d ; losses with delta<0: %d/%d'%(
    c[(1,True)], c[(1,True)]+c[(1,False)], c[(0,False)], c[(0,False)]+c[(0,True)]))

print()
print('C) FALSIFIER: does |delta| track rating gap the right way? (Elo arithmetic)')
w=[m for m in rows if m['delta'] is not None and m['mwin']==1]
l=[m for m in rows if m['delta'] is not None and m['mwin']==0]
def bucket(ms,lab):
    lo=[m for m in ms if m['oppbef']-m['ourbef']<-200]
    hi=[m for m in ms if m['oppbef']-m['ourbef']>200]
    f=lambda x:('n=%d mean=%.2f'%(len(x),statistics.mean(m['delta'] for m in x)) if x else 'n=0')
    print('   %s vs much-weaker(-200): %s | vs much-stronger(+200): %s'%(lab,f(lo),f(hi)))
bucket(w,'WIN '); bucket(l,'LOSS')
