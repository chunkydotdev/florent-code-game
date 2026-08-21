import csv, collections, statistics, math
R=list(csv.DictReader(open('scratchpad/s54_116_facing.tsv'),delimiter='\t'))
for r in R:
    for k in ('eid','build','gend','fwd','d2bc','d2opp','line_kills','disc_kills',
              'rr_none','rr_disc','rr_line','rr_kill','rot','rr_cov','rr_aim'): r[k]=int(r[k])
    for k in ('death','onset_disc','onset_line','onset_kill','first_cov','first_aim'):
        r[k]= None if r[k]=='' else int(r[k])

for ver in ('47','68'):
    V=[r for r in R if r['ver']==ver]
    NG=len(set(r['file'] for r in V))
    print(f"===== v{ver} ({NG} games with >=1 opp turret) =====")
    # --- AGE-CONDITIONED HAZARD -------------------------------------------
    print("  Age-conditioned removal hazard (%/round), age = rounds since build")
    # recompute needs per-round ages; approximate with life-stage buckets is not
    # possible from aggregates -> use turret-level: survival past onset instead.
    C=[r for r in V if r['onset_kill'] is not None]
    B=[r for r in V if r['onset_line'] is not None]
    print(f"  BELT-CUTTERS n={len(C)} turrets / {len(set(r['file'] for r in C))} games")
    for N in (25,50,100,200):
        surv=[r for r in C if (r['death'] is None and r['gend']-r['onset_kill']>=N) or (r['death'] is not None and r['death']-r['onset_kill']>=N)]
        atrisk=[r for r in C if (r['death'] if r['death'] is not None else r['gend'])-r['onset_kill']>=0 and (r['gend']-r['onset_kill'])>=N]
        g=len(set(r['file'] for r in surv))
        print(f"    survives >={N:>3} rounds after first belt kill: {len(surv):>4}/{len(atrisk):>4} at-risk = {len(surv)/max(len(atrisk),1)*100:5.1f}%   in {g} games ({g/NG*100:.1f}% of games)")
    # --- never answered ---------------------------------------------------
    U=[r for r in C if r['death'] is None]
    print(f"  belt-cutters NEVER removed: {len(U)} ({len(U)/max(len(C),1)*100:.1f}%), "
          f"median rounds alive after first belt kill = {statistics.median([r['gend']-r['onset_kill'] for r in U]) if U else float('nan')}")
    # --- did BC have a shot? ---------------------------------------------
    for label,S in (('ALL opp turrets',V),('belt guns (line)',B),('belt cutters',C),('belt cutters NEVER removed',U)):
        cov=[r for r in S if r['rr_cov']>0]; aim=[r for r in S if r['rr_aim']>0]
        mc=statistics.median([r['rr_cov'] for r in cov]) if cov else 0
        ma=statistics.median([r['rr_aim'] for r in aim]) if aim else 0
        print(f"    {label:<28} n={len(S):<5} inside a live BC turret DISC: {len(cov)/max(len(S),1)*100:5.1f}% (median {mc:.0f} rnds) | on a BC turret LINE: {len(aim)/max(len(S),1)*100:5.1f}% (median {ma:.0f} rnds)")
    print()
