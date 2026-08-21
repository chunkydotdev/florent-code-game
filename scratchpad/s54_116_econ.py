import csv, json, collections, statistics
FR={}; TI={}
for l in open('scratchpad/s53_bean_census.jsonl'):
    r=json.loads(l); FR[r['file']]=(r['bc'],r['ver'])
    TI[r['file']]=r['a_ti_collected'] if r['bc']==0 else r['b_ti_collected']
R=list(csv.DictReader(open('scratchpad/s54_116_facing.tsv'),delimiter='\t'))
for r in R:
    r['onset_kill']=None if r['onset_kill']=='' else int(r['onset_kill'])
    r['death']=None if r['death']=='' else int(r['death'])
    r['gend']=int(r['gend']); r['rr_cov']=int(r['rr_cov']); r['line_kills']=int(r['line_kills'])
byfile=collections.defaultdict(list)
for r in R: byfile[r['file']].append(r)

for ver in ('47','68'):
    files=[f for f,v in FR.items() if v[1]==ver and f in byfile]
    def dur(r): return (r['death'] if r['death'] is not None else r['gend'])-r['onset_kill']
    long_={f for f in files if any(r['onset_kill'] is not None and dur(r)>=100 for r in byfile[f])}
    none_={f for f in files if not any(r['onset_kill'] is not None for r in byfile[f])}
    mid={f for f in files if f not in long_ and f not in none_}
    print(f"v{ver}  n={len(files)} games with >=1 opp turret  (CORRELATIONAL, not causal)")
    for lab,S in (('no belt-cutter at all',none_),('belt-cutter <100 rnds',mid),('belt-cutter lives >=100 rnds after first belt kill',long_)):
        t=[TI[f] for f in S if TI[f] is not None]
        gl=[max(r['gend'] for r in byfile[f]) for f in S]
        print(f"   {lab:<52} games={len(S):<5} ({len(S)/len(files)*100:4.1f}%)  BC median ti_collected={statistics.median(t) if t else float('nan'):7.0f}  median game length={statistics.median(gl) if gl else float('nan'):5.0f}")
    # never-in-reach siting
    V=[r for r in R if r['ver']==ver]
    C=[r for r in V if r['onset_kill'] is not None]
    print(f"   belt-cutters never inside ANY live BC turret disc: {sum(1 for r in C if r['rr_cov']==0)}/{len(C)} = {sum(1 for r in C if r['rr_cov']==0)/max(len(C),1)*100:.1f}%")
    print(f"   median BC belt tiles killed on a belt-cutter's line: {statistics.median([r['line_kills'] for r in C]) if C else float('nan'):.0f}; total {sum(r['line_kills'] for r in C)}")
    print()
