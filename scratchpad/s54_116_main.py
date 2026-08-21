import csv, collections, statistics, math
R=list(csv.DictReader(open('scratchpad/s54_116_facing.tsv'),delimiter='\t'))
for r in R:
    for k in ('eid','build','gend','fwd','d2bc','d2opp','line_kills','disc_kills',
              'rr_none','rr_disc','rr_line','rr_kill','rot'): r[k]=int(r[k])
    for k in ('death','onset_disc','onset_line','onset_kill'):
        r[k]= None if r[k]=='' else int(r[k])

def hw(gm):
    n=len(gm)
    if n<2: return float('nan')
    return 1.96*statistics.stdev(gm)/math.sqrt(n)*math.sqrt(1.833)*100

def cell(rows,label,onset_field):
    if not rows:
        print(f"  {label:<44} n=0"); return
    byg=collections.defaultdict(lambda:[0,0]); lat=[]
    for r in rows:
        byg[r['file']][0]+=1
        if r['death'] is not None:
            byg[r['file']][1]+=1
            base=r[onset_field] if onset_field and r[onset_field] is not None else r['build']
            lat.append(r['death']-base)
    gm=[v[1]/v[0] for v in byg.values()]
    m=statistics.mean(gm)*100
    pooled=sum(v[1] for v in byg.values())/sum(v[0] for v in byg.values())*100
    lat.sort()
    med=statistics.median(lat) if lat else float('nan')
    p90=lat[int(.9*(len(lat)-1))] if lat else float('nan')
    print(f"  {label:<44} games={len(gm):<5} turrets={len(rows):<5} answered={m:5.1f}% +-{hw(gm):4.1f}  pooled={pooled:5.1f}%  medlat={med:5.1f}  p90lat={p90:5.1f}")

for ver in ('47','68'):
    V=[r for r in R if r['ver']==ver]
    print(f"===== v{ver}: {len(V)} opp turret-lives in {len(set(r['file'] for r in V))} games =====")
    cell([r for r in V if r['fwd']],'A FWD in BC half (base-study cell)',None)
    cell([r for r in V if r['onset_line'] is not None],'B BELT-GUN: line ever covers live BC belt','onset_line')
    cell([r for r in V if r['onset_line'] is not None and r['fwd']],'B1  ...and in BC half','onset_line')
    cell([r for r in V if r['onset_line'] is not None and not r['fwd']],'B2  ...and in THEIR half','onset_line')
    cell([r for r in V if r['onset_kill'] is not None],'C BELT-CUTTER: >=1 belt died on its line','onset_kill')
    cell([r for r in V if r['onset_line'] is None and r['onset_disc'] is not None],'D in disc, never on line','onset_disc')
    cell([r for r in V if r['onset_disc'] is None],'E PLACEBO: no BC belt in disc, ever',None)
    print()
    # ---- hazard per turret-round by state (immortal-time safe) ----
    print("  HAZARD per turret-round at risk (removals / rounds in that state)")
    hz=collections.Counter(); rr=collections.Counter()
    for r in V:
        for s in ('none','disc','line','kill'): rr[s]+=r['rr_'+s]
        if r['death'] is not None and r['state_at_death']: hz[r['state_at_death']]+=1
    for s in ('none','disc','line','kill'):
        h=hz[s]/rr[s] if rr[s] else float('nan')
        print(f"    state={s:<5} rounds={rr[s]:<8} removals={hz[s]:<5} hazard={h*100:6.3f}%/rnd  mean wait={1/h if h else float('inf'):7.1f} rnd")
    print()
