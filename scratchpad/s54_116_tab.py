import csv, collections, statistics, math
R=[r for r in csv.DictReader(open('scratchpad/s54_116_turrets.tsv'),delimiter='\t')]
for r in R:
    r['fwd']= r['fwd']=='True'
    r['onset']= None if r['onset']=='' else int(r['onset'])
    r['death']= None if r['death']=='' else int(r['death'])
    for k in ('build','gend','nbelt','eaten','d2bc','d2opp'): r[k]=int(r[k])

def cell(rows, label):
    if not rows: 
        print(f"{label:<48} n=0"); return
    byg=collections.defaultdict(lambda:[0,0])
    lat=[]
    for r in rows:
        byg[r['file']][0]+=1
        if r['death'] is not None:
            byg[r['file']][1]+=1
            base = r['onset'] if r['onset'] is not None else r['build']
            lat.append(r['death']-base)
    gm=[v[1]/v[0] for v in byg.values()]
    n=len(gm); m=statistics.mean(gm)
    sd=statistics.stdev(gm) if n>1 else 0
    hw=1.96*sd/math.sqrt(n)*math.sqrt(1.833)*100 if n>1 else float('nan')
    pooled=sum(v[1] for v in byg.values())/sum(v[0] for v in byg.values())
    ml=statistics.median(lat) if lat else float('nan')
    print(f"{label:<48} games={n:<5} turrets={len(rows):<5} removed={m*100:5.1f}% +-{hw:4.1f}  pooled={pooled*100:5.1f}%  medlat={ml:6.1f} (n={len(lat)})")

for ver in ('47','68'):
    V=[r for r in R if r['ver']==ver]
    print(f"===== v{ver}  (opp turret-lives n={len(V)}) =====")
    cell(V,'ALL opp turrets')
    cell([r for r in V if r['fwd']],'FWD (BC half)  [base-study cell]')
    cell([r for r in V if r['fwd'] and r['onset'] is not None],'FWD & belt-in-range  (STIMULUS)')
    cell([r for r in V if r['fwd'] and r['onset'] is None],'FWD & NO belt in range')
    cell([r for r in V if not r['fwd'] and r['onset'] is not None],'HOME-half(theirs) & belt-in-range')
    cell([r for r in V if not r['fwd'] and r['onset'] is None],'HOME-half(theirs) & no belt  [PLACEBO/base]')
    cell([r for r in V if r['eaten']>0],'BELT-EATER (>=1 BC belt death in disc)')
    cell([r for r in V if r['onset'] is not None and r['eaten']==0],'in-range, ate NOTHING')
    print()
