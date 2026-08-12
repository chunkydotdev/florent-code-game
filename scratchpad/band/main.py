import json, statistics, collections
rows=[m for m in json.load(open('scratchpad/band/matches.json')) if m['delta'] is not None]
rows.sort(key=lambda m:m['created'])
for m in rows:
    m['gap']=m['oppbef']-m['ourbef']
    m['day']=m['created'][:10]
    m['v']=int(m['ourver'])

# requested coarse bands
COARSE=[('< us-300',-1e9,-300),('us-300..-100',-300,-100),('us-100..+100',-100,100),('us+100..+400',100,400),('> us+400',400,1e9)]
# power bands (94% of exposure is inside +-100)
FINE=[('opp < us-100',-1e9,-100),('us-100..-50',-100,-50),('us-50..0',-50,0),('us 0..+50',0,50),('us+50..+100',50,100),('opp > us+100',100,1e9)]
def band(m,BS):
    for lab,lo,hi in BS:
        if lo<=m['gap']<hi: return lab
    return '?'

def table(BS,key,keys,title):
    print('\n=== %s ==='%title)
    hdr='%-14s'%'band'+''.join('%18s'%str(k) for k in keys)+'%18s'%'ALL'
    print(hdr)
    for lab,_,_ in BS:
        cells=[]
        for k in list(keys)+[None]:
            sel=[m for m in rows if band(m,BS)==lab and (k is None or key(m)==k)]
            if not sel: cells.append('%18s'%'-'); continue
            n=len(sel); mw=sum(1 for m in sel if m['mwin']==1)
            gwt=sum(m['gw'] for m in sel); gtot=sum(m['gw']+m['gl'] for m in sel)
            net=sum(m['delta'] for m in sel)
            cells.append('%18s'%('%d/%d %.0f%%g%.0f%%'%(mw,n,100*mw/n,100*gwt/gtot)))
        print('%-14s'%lab+''.join(cells))

days=sorted(set(m['day'] for m in rows))
table(COARSE,lambda m:m['day'],days,'REQUESTED BANDS - match W/n, matchwin%, game-share% BY DAY')
table(FINE,lambda m:m['day'],days,'POWER BANDS - match W/n, matchwin%, game-share% BY DAY')

def flow(BS,key,keys,title):
    print('\n=== %s ==='%title)
    print('%-14s %-10s %5s %8s %8s %8s %8s'%('band','period','n','won+','lost-','NET','net/match'))
    for lab,_,_ in BS:
        for k in list(keys)+['ALL']:
            sel=[m for m in rows if band(m,BS)==lab and (k=='ALL' or key(m)==k)]
            if not sel: continue
            pos=sum(m['delta'] for m in sel if m['delta']>0)
            neg=sum(m['delta'] for m in sel if m['delta']<0)
            print('%-14s %-10s %5d %+8.1f %+8.1f %+8.1f %+8.2f'%(lab,k,len(sel),pos,neg,pos+neg,(pos+neg)/len(sel)))
        print()
flow(FINE,lambda m:m['day'],days,'ELO FLOW by power band x day (points won / lost separately)')
