import csv,sys,statistics,os
S="/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/82720aae-f502-4b10-9dd5-ad5f55d16b94/scratchpad/v513_build"
def load(fs):
    rows=[]
    for f in fs:
        p=S+"/grid/%s.tsv"%f
        if os.path.exists(p):
            rows+=[r for r in csv.DictReader(open(p),delimiter="\t") if r.get('ours')]
    return rows
def rep(name, rows):
    n=len(rows)
    if not n: return
    w=sum(1 for r in rows if r['ours']=='US')
    ck=[int(r['turn']) for r in rows if r['ours']=='US' and 'Core' in r['cond']]
    lk=[int(r['turn']) for r in rows if r['ours']=='OPP' and 'Core' in r['cond']]
    mined=[int(r['ours_mined']) for r in rows]
    print(f"{name:11s} n={n:3d} win={w:3d}({100*w/n:4.1f}%) kill={len(ck):2d} k<=300={sum(1 for t in ck if t<=300):2d}"
          f"({100*sum(1 for t in ck if t<=300)/n:4.1f}%) died={len(lk):2d}({100*len(lk)/n:4.1f}%)"
          f" r1000={sum(1 for r in rows if int(r['turn'])>=999):2d} tic0={sum(1 for m in mined if m==0):2d}"
          f" medmine={statistics.median(mined):5.0f} medkill={statistics.median(ck) if ck else -1:4.0f} tb={sum(int(r['tracebacks']) for r in rows)}")
for name,fs in (("v513 FULL",["v513a","v513b"]),("crew_off",["crewoffFa","crewoffFb"]),
                ("nodeny",["nodenyA","nodenyB"]),("v512",["v512a","v512b"])):
    rep(name, load(fs))
