import json, statistics, collections, math
rows=json.load(open('scratchpad/band/matches2.json')); rows.sort(key=lambda m:m['created'])
for m in rows:
    m['gap']=m['oppbef']-m['ourbef']; m['E']=1/(1+10**(m['gap']/400.0)); m['S']=m['gw']/5.0
live={r['teamId']:r for r in json.load(open('scratchpad/ladder_live.json'))}
lr=sorted(live.values(),key=lambda r:-r['rating'])
for i,r in enumerate(lr,1): r['_r']=i
for m in rows:
    t=live.get(m['oppid']); m['rank']=t['_r'] if t else 999
SE=0.287
def blk(s):
    if not s: return 'n=0'
    S=statistics.mean(m['S'] for m in s);E=statistics.mean(m['E'] for m in s)
    return 'n=%-3d S-E=%+.3f+-%.3f net%+7.1f (%+.2f/m)'%(len(s),S-E,SE/math.sqrt(len(s)),sum(m['delta'] for m in s),sum(m['delta'] for m in s)/len(s))
print('DENSEST POOL (opp current rank 25-40) OVER TIME — 72%% of our matches since 08-09:')
for d in sorted(set(m['created'][:10] for m in rows)):
    s=[m for m in rows if m['created'][:10]==d and 24<m['rank']<=40]
    print('  %s  %s'%(d,blk(s)))
print('  tight-pairing era 08-07+: %s'%blk([m for m in rows if m['created']>='2026-08-07' and 24<m['rank']<=40]))
print('    first half : %s'%blk([m for m in rows if m['created']>='2026-08-07' and 24<m['rank']<=40][:sum(1 for m in rows if m['created']>='2026-08-07' and 24<m['rank']<=40)//2]))
half=[m for m in rows if m['created']>='2026-08-07' and 24<m['rank']<=40]
print('    second half: %s'%blk(half[len(half)//2:]))

print('\nWITH vs WITHOUT the five persistent bleeders (Ouroboros, Lunds, Powerpuff, KCM, diverge):')
BLEED={'Ouroboros','Lunds Stallions','Powerpuff Girls','Kings College Munich','diverge'}
rec=[m for m in rows if m['created']>='2026-08-09']
print('  since 08-09 all:          %s'%blk(rec))
print('  since 08-09 excl. those5: %s'%blk([m for m in rec if m['oppname'] not in BLEED]))
print('  since 08-09 those 5 only: %s'%blk([m for m in rec if m['oppname'] in BLEED]))
print('  those 5 = %d of %d matches (%.0f%%) since 08-09'%(sum(1 for m in rec if m['oppname'] in BLEED),len(rec),
    100*sum(1 for m in rec if m['oppname'] in BLEED)/len(rec)))
print('  lifetime cost of those 5: %+.0f Elo over %d matches'%(
    sum(m['delta'] for m in rows if m['oppname'] in BLEED), sum(1 for m in rows if m['oppname'] in BLEED)))

print('\nCROSS-CHECK vs elo_history.tsv (independent hand/monitor tape):')
import csv
h=[r for r in csv.DictReader(open('elo_history.tsv'),delimiter='\t') if r.get('rating')]
print('  elo_history last 3:',[(r['timestamp'],r['rating']) for r in h[-3:]])
print('  ladder_games last ourbef: %.1f at %s ; live snapshot 1669.0 at 14:03Z'%(rows[-1]['ourbef'],rows[-1]['created']))
