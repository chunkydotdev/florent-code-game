import json, statistics, collections, math
rows=json.load(open('scratchpad/band/matches2.json')); rows.sort(key=lambda m:m['created'])
for m in rows:
    m['gap']=m['oppbef']-m['ourbef']; m['E']=1/(1+10**(m['gap']/400.0)); m['S']=m['gw']/5.0; m['day']=m['created'][:10]
live={r['teamId']:r for r in json.load(open('scratchpad/ladder_live.json'))}
lr=sorted(live.values(),key=lambda r:-r['rating'])
for i,r in enumerate(lr,1): r['_r']=i
for m in rows:
    t=live.get(m['oppid']); m['rank']=t['_r'] if t else None; m['currbelow']= (m['rank'] is not None and m['rank']>24)

def se_of_S(ms):  # per-match sd of S=gw/5 empirically
    return statistics.pstdev([m['S'] for m in ms])/math.sqrt(len(ms))

print('NOISE FLOOR: per-match sd of game share S = %.3f (n=678). '
      'So se(mean S-E) = 0.%03d/sqrt(n).'%(statistics.pstdev([m['S'] for m in rows]),
      int(1000*statistics.pstdev([m['S'] for m in rows]))))
print('  n=30 -> se 0.040 (=1.3 Elo/match) ; n=50 -> se 0.031 ; n=75 -> se 0.025 ; n=150 -> se 0.018')
print('  MDE (2se) for a 50-match block = 0.062 game-share = 2.0 Elo/match.')

print('\n(1) AGGREGATE by day: opponents CURRENTLY ranked below us (rank 25-116) vs above (1-23)')
print('%-11s %34s %30s'%('day','opp currently BELOW us','opp currently ABOVE us'))
for d in sorted(set(m['day'] for m in rows)):
    o=[]
    for sel,w in ((True,34),(False,30)):
        s=[m for m in rows if m['day']==d and m['currbelow']==sel]
        if not s: o.append('%*s'%(w,'-')); continue
        S=statistics.mean(m['S'] for m in s); E=statistics.mean(m['E'] for m in s); net=sum(m['delta'] for m in s)
        o.append('%*s'%(w,'n=%-3d S-E=%+.3f+-%.3f net%+.0f'%(len(s),S-E,se_of_S(s),net)))
    print('%-11s'%d+''.join(o))

print('\n(2) TIGHT-PAIRING ERA ONLY (08-07 00:00 onward; excludes the 08-05/06 climb).')
era=[m for m in rows if m['created']>='2026-08-07']
print('    n=%d matches, %d distinct opponents'%(len(era),len(set(m['oppname'] for m in era))))
for lab,sel in (('gap<0 (opp rated below us AT THE TIME)',[m for m in era if m['gap']<0]),
                ('opp CURRENTLY ranked below us',[m for m in era if m['currbelow']])):
    s=sel
    # OLS of S-E on time index
    x=list(range(len(s))); y=[m['S']-m['E'] for m in s]
    mx=statistics.mean(x); my=statistics.mean(y)
    b=sum((a-mx)*(c-my) for a,c in zip(x,y))/sum((a-mx)**2 for a in x)
    resid=[c-(my+b*(a-mx)) for a,c in zip(x,y)]
    sb=math.sqrt(sum(r*r for r in resid)/(len(s)-2)/sum((a-mx)**2 for a in x))
    print('    %-40s n=%-3d mean S-E=%+.3f  slope/100matches=%+.4f +- %.4f (t=%+.2f)'%(
        lab,len(s),my,100*b,100*sb,b/sb))
    h=len(s)//2
    for nm,ss in (('first half',s[:h]),('second half',s[h:])):
        S=statistics.mean(m['S'] for m in ss); E=statistics.mean(m['E'] for m in ss)
        print('        %-12s %s..%s n=%-3d S-E=%+.3f +- %.3f  net %+.1f (%+.2f/m)'%(
            nm,ss[0]['created'][5:10],ss[-1]['created'][5:10],len(ss),S-E,se_of_S(ss),
            sum(m['delta'] for m in ss),sum(m['delta'] for m in ss)/len(ss)))

print('\n(3) THE FIVE BIGGEST BLEEDERS, chronological halves (are they getting WORSE for us?)')
byopp=collections.defaultdict(list)
for m in rows: byopp[m['oppname']].append(m)
tot=[(sum(m['delta'] for m in ms),n,ms) for n,ms in byopp.items() if len(ms)>=12]
tot.sort()
for net,name,ms in tot[:6]:
    t=live.get(ms[0]['oppid']); h=len(ms)//2
    a,b2=ms[:h],ms[h:]
    fa=lambda s:'n=%-2d %s..%s S-E=%+.3f+-%.3f net%+.0f'%(len(s),s[0]['created'][5:10],s[-1]['created'][5:10],
        statistics.mean(m['S'] for m in s)-statistics.mean(m['E'] for m in s),se_of_S(s),sum(m['delta'] for m in s))
    d1=statistics.mean(m['S'] for m in a)-statistics.mean(m['E'] for m in a)
    d2=statistics.mean(m['S'] for m in b2)-statistics.mean(m['E'] for m in b2)
    sd=math.sqrt(se_of_S(a)**2+se_of_S(b2)**2)
    print('  %-22s rank%-4s net%+7.1f | H1 %s | H2 %s | delta %+.3f (%.1f sigma)'%(
        name,t['_r'] if t else '?',net,fa(a),fa(b2),d2-d1,(d2-d1)/sd))
