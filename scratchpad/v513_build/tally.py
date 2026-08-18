import csv,sys,statistics
def load(fs):
    rows=[]
    for f in fs:
        for r in csv.DictReader(open(f),delimiter="\t"):
            if r.get('ours') and r['ours']!='TIMEOUT': rows.append(r)
    return rows
def rep(name, rows):
    n=len(rows); w=sum(1 for r in rows if r['ours']=='US')
    ck=[int(r['turn']) for r in rows if r['ours']=='US' and 'Core' in r['cond']]
    lk=[int(r['turn']) for r in rows if r['ours']=='OPP' and 'Core' in r['cond']]
    k300=sum(1 for t in ck if t<=300)
    r1000=sum(1 for r in rows if int(r['turn'])>=999)
    tb=sum(int(r['tracebacks']) for r in rows)
    mined=[int(r['ours_mined']) for r in rows]
    tic0=sum(1 for m in mined if m==0)
    coredeath=len(lk)
    print(f"{name:8s} n={n:3d} wins={w:3d} ({100*w/n:.1f}%) corekills={len(ck):2d} kills<=300={k300:2d} "
          f"ourcore_died={coredeath:2d} r1000={r1000:2d} tb={tb} tic0={tic0:2d} ({100*tic0/n:.0f}%) "
          f"median_mined={statistics.median(mined):.0f} med_kill={statistics.median(ck) if ck else -1:.0f} "
          f"med_death={statistics.median(lk) if lk else -1:.0f}")
    bymap={}
    for r in rows: bymap.setdefault(r['map'],[0,0])
    for r in rows:
        bymap[r['map']][1]+=1
        if r['ours']=='US': bymap[r['map']][0]+=1
    print("        per-map wins:", " ".join(f"{k}={v[0]}/{v[1]}" for k,v in sorted(bymap.items())))
rep("v513", load([f"{sys.argv[1]}/v513a.tsv",f"{sys.argv[1]}/v513b.tsv"]))
rep("v512", load([f"{sys.argv[1]}/v512a.tsv",f"{sys.argv[1]}/v512b.tsv"]))
