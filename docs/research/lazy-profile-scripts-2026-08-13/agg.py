import sys
from pathlib import Path
sys.path.insert(0, "tools"); sys.path.insert(0, str(Path(__file__).parent))
from lazy_profile import parse, SEAT, d2
FILES = ([f"replay_archive/1ef56244-84a5-4136-ad8f-cf063b9fd3fe_game_{i}.replay26" for i in range(1,6)]
       + [f"replay_archive/b9f3fab5-483a-443c-a2a3-695d69a8e915_game_{i}.replay26" for i in range(1,6)])
print(f"{'game':6s} {'map':7s} {'area':5s} {'lazy1stTurret':13s} {'fwd?':5s} {'siege<=d8':9s} "
      f"{'lazyTurrets':11s} {'1stHarv':8s} {'harvN':5s} {'winner':7s} {'end':6s}")
rows=[]
for f in FILES:
    g = parse(Path(f)); L = SEAT[g["name"]]; U=1-L
    tag = ("M1" if "1ef" in f else "M2")+"g"+f.split("_game_")[1][0]
    lc, uc = g["corepos"][L], g["corepos"][U]
    t1 = next(((b[0], b[2], d2(b[3],uc)<d2(b[3],lc)) for b in g["builds"]
               if b[1]==L and b[2] in ("gunner","sentinel","launcher")), None)
    siege = next((b[0] for b in g["builds"] if b[1]==L and b[2] in ("gunner","sentinel")
                  and d2(b[3],uc)<=8), None)
    nt = len([1 for b in g["builds"] if b[1]==L and b[2] in ("gunner","sentinel","launcher")])
    h1 = next((b[0] for b in g["builds"] if b[1]==L and b[2]=="harvester"), None)
    hn = len([1 for b in g["builds"] if b[1]==L and b[2]=="harvester"])
    dr = {d[4]: d[0] for d in g["deaths"]}
    print(f"{tag:6s} {g['w']}x{g['h']:<4d} {g['w']*g['h']:<5d} "
          f"r{t1[0]:<4d}{t1[1][:4]:<8s} {'FWD' if t1[2] else 'HOME':5s} "
          f"{('r%d'%siege) if siege else '-':9s} {nt:<11d} r{h1:<7d} {hn:<5d} "
          f"{'LAZY' if g['winner']==L else 'US':7s} {g['wincond'][:6]:6s}")
    rows.append((g['w']*g['h'], g['winner']==L, t1[0], siege, nt))
big = [r for r in rows if r[0]>=900]; sml = [r for r in rows if r[0]<900]
print(f"\n30x30 (n={len(big)}): lazy wins {sum(1 for r in big if r[1])}; "
      f"first turret rounds {[r[2] for r in big]}; siege arrival {[r[3] for r in big]}; "
      f"turret counts {[r[4] for r in big]}")
print(f"<900  (n={len(sml)}): lazy wins {sum(1 for r in sml if r[1])}; "
      f"first turret rounds {[r[2] for r in sml]}; siege arrival {[r[3] for r in sml]}; "
      f"turret counts {[r[4] for r in sml]}")
