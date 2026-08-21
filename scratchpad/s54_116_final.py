import csv, collections, statistics, math
R=list(csv.DictReader(open('scratchpad/s54_116_facing.tsv'),delimiter='\t'))
I=('eid','build','gend','fwd','d2bc','d2opp','line_kills','disc_kills','rr_none',
   'rr_disc','rr_line','rr_kill','rot','rr_cov','rr_aim','shots','batk')
N=('death','onset_disc','onset_line','onset_kill','first_cov','first_aim','first_shot','first_batk')
for r in R:
    for k in I: r[k]=int(r[k])
    for k in N: r[k]= None if r[k]=='' else int(r[k])

def hw(gm):
    n=len(gm)
    return float('nan') if n<2 else 1.96*statistics.stdev(gm)/math.sqrt(n)*math.sqrt(1.833)*100
def gmean(rows,pred):
    byg=collections.defaultdict(lambda:[0,0])
    for r in rows:
        byg[r['file']][0]+=1
        if pred(r): byg[r['file']][1]+=1
    gm=[v[1]/v[0] for v in byg.values()]
    return statistics.mean(gm)*100, hw(gm), len(gm)
def med(xs): 
    xs=[x for x in xs if x is not None]
    return statistics.median(xs) if xs else float('nan')

CELLS=[
 ('BELT-GUN  (firing line covers a live BC belt tile)', lambda r: r['onset_line'] is not None, 'onset_line'),
 ('  of which BELT-CUTTER (a belt tile died on its line)', lambda r: r['onset_kill'] is not None, 'onset_kill'),
 ('CASTLE  (forward turret in BC half) [base-study cell]', lambda r: r['fwd']==1, 'build'),
 ('PLACEBO (no BC belt ever inside its firing disc)', lambda r: r['onset_disc'] is None, 'build'),
]
for ver in ('47','68'):
    V=[r for r in R if r['ver']==ver]
    print(f"########## v{ver}  ({len(V)} opp turret-lives, {len(set(r['file'] for r in V))} games) ##########")
    for label,pred,onset in CELLS:
        S=[r for r in V if pred(r)]
        if not S: continue
        o=lambda r: (r[onset] if onset!='build' and r[onset] is not None else r['build'])
        rm,rmh,ng=gmean(S, lambda r: r['death'] is not None)
        sh,shh,_=gmean(S, lambda r: r['shots']>0)
        ba,bah,_=gmean(S, lambda r: r['batk']>0)
        any_,anyh,_=gmean(S, lambda r: r['shots']>0 or r['batk']>0)
        lat_rm=med([r['death']-o(r) for r in S if r['death'] is not None])
        lat_sh=med([r['first_shot']-o(r) for r in S if r['first_shot'] is not None])
        print(f"{label}")
        print(f"    n={len(S):<5} games={ng:<5} | REMOVED {rm:5.1f}%+-{rmh:4.1f} | SHOT AT {sh:5.1f}%+-{shh:4.1f} | BUILDER-ATTACKED {ba:5.1f}%+-{bah:4.1f} | ANSWERED(any) {any_:5.1f}%+-{anyh:4.1f}")
        print(f"          median latency from onset: first shot {lat_sh:5.1f} rnd | removal {lat_rm:5.1f} rnd | median shots taken {med([r['shots'] for r in S]):.0f}")
    print()

print("########## STRATIFIED: within BC's half (the castle cell), belt-cutter or not ##########")
for ver in ('47','68'):
    V=[r for r in R if r['ver']==ver and r['fwd']==1]
    for reach,rlab in ((False,'all'),(True,'BC turret had it in reach (rr_cov>0)')):
        S=[r for r in V if (r['rr_cov']>0 if reach else True)]
        print(f"  v{ver}  [{rlab}]  n={len(S)}")
        for lab,pred in (('  cuts the belt      ',lambda r:r['onset_kill'] is not None),
                         ('  aims at belt, no cut',lambda r:r['onset_kill'] is None and r['onset_line'] is not None),
                         ('  belt not on its line',lambda r:r['onset_line'] is None)):
            T=[r for r in S if pred(r)]
            if not T: continue
            sh,shh,ng=gmean(T,lambda r:r['shots']>0)
            rm,rmh,_=gmean(T,lambda r:r['death'] is not None)
            an,anh,_=gmean(T,lambda r:r['shots']>0 or r['batk']>0)
            print(f"    {lab} n={len(T):<5} games={ng:<5} SHOT AT {sh:5.1f}%+-{shh:4.1f}  ANSWERED {an:5.1f}%+-{anh:4.1f}  REMOVED {rm:5.1f}%+-{rmh:4.1f}  median shots {med([r['shots'] for r in T]):.0f}  median rounds in BC reach {med([r['rr_cov'] for r in T]):.0f}")
    print()

print("########## REACH -> AIM conversion (does BC turn a gun it can reach onto the belt gun?) ##########")
for ver in ('47','68'):
    V=[r for r in R if r['ver']==ver and r['rr_cov']>0]
    for lab,pred in (('belt-cutter',lambda r:r['onset_kill'] is not None),
                     ('NOT belt-cutter',lambda r:r['onset_kill'] is None)):
        T=[r for r in V if pred(r)]
        if not T: continue
        a,ah,ng=gmean(T,lambda r:r['rr_aim']>0)
        s,sh_,_=gmean(T,lambda r:r['shots']>0)
        lat=med([r['first_aim']-r['first_cov'] for r in T if r['first_aim'] is not None and r['first_cov'] is not None])
        print(f"  v{ver} {lab:<16} n={len(T):<5} ever AIMED at {a:5.1f}%+-{ah:4.1f}  ever SHOT {s:5.1f}%+-{sh_:4.1f}  median reach->aim latency {lat:.0f} rnd  median rounds in reach {med([r['rr_cov'] for r in T]):.0f}")
    print()
