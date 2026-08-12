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

print('(4) VERSION-BOUNDARY SCAN: every opponent version change with >=6 matches on BOTH sides.')
print('    (their version increments -> did our game share drop?)  se(diff) shown.')
byopp=collections.defaultdict(list)
for m in rows: byopp[m['oppname']].append(m)
found=[]
for name,ms in byopp.items():
    vs=sorted(set(int(m['oppver']) for m in ms))
    for cut in vs[1:]:
        a=[m for m in ms if int(m['oppver'])<cut]; b=[m for m in ms if int(m['oppver'])>=cut]
        if len(a)<6 or len(b)<6: continue
        d=(statistics.mean(m['S'] for m in b)-statistics.mean(m['E'] for m in b))-(statistics.mean(m['S'] for m in a)-statistics.mean(m['E'] for m in a))
        sd=SE*math.sqrt(1/len(a)+1/len(b))
        found.append((d/sd,d,sd,name,cut,a,b))
found.sort()
for t,d,sd,name,cut,a,b in found:
    mark='  <-- DECLINE' if t<-1.5 else ('  <-- improvement' if t>1.5 else '')
    print('  %-22s at their v%-4s  before n=%-3d S-E=%+.3f | after n=%-3d S-E=%+.3f | diff %+.3f (%.1f sigma)%s'%(
        name,cut,len(a),statistics.mean(m['S'] for m in a)-statistics.mean(m['E'] for m in a),
        len(b),statistics.mean(m['S'] for m in b)-statistics.mean(m['E'] for m in b),d,t,mark))
if not found: print('   NONE — no opponent has >=6 rated matches on both sides of any single version boundary.')

print('\n(5) TOTAL ELO ACCOUNTING, all %d rated ladder matches 08-05..08-10'%len(rows))
pos=sum(m['delta'] for m in rows if m['delta']>0); neg=sum(m['delta'] for m in rows if m['delta']<0)
print('    points WON %+.0f   points LOST %+.0f   NET %+.0f   (rating 1500 start -> 1669 live)'%(pos,neg,pos+neg))
for lab,f in (('opp CURRENT rank 1-23 (above us)',lambda m:m['rank']<24),
              ('opp CURRENT rank 25-40',lambda m:24<m['rank']<=40),
              ('opp CURRENT rank 41+',lambda m:m['rank']>40)):
    s=[m for m in rows if f(m)]
    p=sum(m['delta'] for m in s if m['delta']>0); n=sum(m['delta'] for m in s if m['delta']<0)
    print('    %-34s n=%-3d (%4.1f%%)  won %+7.1f  lost %+7.1f  NET %+7.1f (%+.2f/m)'%(lab,len(s),100*len(s)/len(rows),p,n,p+n,(p+n)/len(s)))

print('\n(6) CURRENT-STATE LEDGER: net Elo per opponent SINCE 08-09 00:00 (n>=6), the live bleed list')
rec=[m for m in rows if m['created']>='2026-08-09']
bo=collections.defaultdict(list)
for m in rec: bo[m['oppname']].append(m)
L=[]
for n,ms in bo.items():
    if len(ms)<6: continue
    L.append((sum(m['delta'] for m in ms),n,ms))
L.sort()
print('    (%d matches since 08-09; %d opponents with n>=6 cover %d of them)'%(len(rec),len(L),sum(len(x[2]) for x in L)))
for net,n,ms in L:
    t=live.get(ms[0]['oppid'])
    S=statistics.mean(m['S'] for m in ms); E=statistics.mean(m['E'] for m in ms)
    print('    %-24s rank%-4s rating%-6s n=%-3d S=%.2f E=%.2f S-E=%+.3f+-%.3f  net %+7.1f (%+.2f/m)'%(
        n,t['_r'] if t else '?',('%.0f'%t['rating']) if t else '?',len(ms),S,E,S-E,SE/math.sqrt(len(ms)),net,net/len(ms)))
print('    ...others (n<6 each): net %+.1f over %d matches'%(
    sum(m['delta'] for m in rec)-sum(x[0] for x in L), len(rec)-sum(len(x[2]) for x in L)))
print('    TOTAL since 08-09: net %+.1f over %d matches (%+.2f/m)'%(sum(m['delta'] for m in rec),len(rec),sum(m['delta'] for m in rec)/len(rec)))
