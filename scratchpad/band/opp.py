import json, csv, collections, statistics
rows=json.load(open('scratchpad/band/matches2.json'))
rows.sort(key=lambda m:m['created'])
for m in rows:
    m['gap']=m['oppbef']-m['ourbef']; m['E']=1/(1+10**(m['gap']/400.0)); m['S']=m['gw']/5.0
live={r['teamId']:r for r in json.load(open('scratchpad/ladder_live.json'))}
lr=sorted(live.values(),key=lambda r:-r['rating'])
for i,r in enumerate(lr,1): r['_r']=i

print('EXPOSURE by opponent CURRENT ladder rank (snapshot 2026-08-10T14:03Z, 116 teams, us #24 @1669.0)')
print('  n=%d rated ladder matches, %s..%s'%(len(rows),rows[0]['created'][:10],rows[-1]['created'][:10]))
buck=collections.Counter(); buckall=collections.Counter()
recent=[m for m in rows if m['created']>='2026-08-09']
for lab,sel in (('ALL 678',rows),('since 08-09 (n=%d)'%len(recent),recent)):
    c=collections.Counter()
    for m in sel:
        t=live.get(m['oppid'])
        r=t['_r'] if t else None
        k = 'unranked/absent' if r is None else ('rank 1-23 (above us)' if r<24 else ('rank 25-40' if r<=40 else ('rank 41-60' if r<=60 else 'rank 61+')))
        c[k]+=1
    print('  %-22s'%lab, {k:'%d (%.0f%%)'%(v,100*v/len(sel)) for k,v in sorted(c.items())})

print('\nPER-OPPONENT (>=12 rated matches), overall and by THEIR version boundary')
byopp=collections.defaultdict(list)
for m in rows: byopp[m['oppname']].append(m)
out=[]
for name,ms in byopp.items():
    if len(ms)<12: continue
    t=live.get(ms[0]['oppid'])
    S=statistics.mean(m['S'] for m in ms); E=statistics.mean(m['E'] for m in ms)
    out.append((S-E,name,ms,t))
out.sort()
for se,name,ms,t in out:
    net=sum(m['delta'] for m in ms)
    print('\n%-26s n=%-3d  currentRank=%-4s rating=%-6s | overall S=%.3f E=%.3f S-E=%+.3f net=%+.1f (%+.2f/m)'%(
        name,len(ms), t['_r'] if t else '?', ('%.0f'%t['rating']) if t else '?',
        statistics.mean(m['S'] for m in ms), statistics.mean(m['E'] for m in ms), se, net, net/len(ms)))
    vg=collections.defaultdict(list)
    for m in ms: vg[m['oppver']].append(m)
    for v in sorted(vg,key=lambda x:int(x)):
        s=vg[v]
        S=statistics.mean(m['S'] for m in s); E=statistics.mean(m['E'] for m in s)
        flag='' if len(s)>=8 else '  (thin)'
        print('     their v%-4s n=%-3d %s..%s  S=%.3f E=%.3f S-E=%+.3f net=%+.1f%s'%(
            v,len(s),s[0]['created'][5:16],s[-1]['created'][5:16],S,E,S-E,sum(m['delta'] for m in s),flag))
