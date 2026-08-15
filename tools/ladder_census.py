import json, subprocess, collections, statistics
from pathlib import Path

# ---- `--help` CONTRACT (enforced by tests/test_instruments.py) --------------
# Side-effect-free, prints this module's docstring, exits 0.
#
# ⛔ WHY. Probing an unknown tool with `--help` is the first thing anyone does.
# Before 2026-08-15, 40 of 86 tools here had no argparse, so `--help` was just an
# unrecognised argument and THE TOOL RAN FOR REAL -- printing VERDICT-SHAPED text
# that reads as a finding:
#     tools/freshness.py --help  ->  "BLIND: --help has no parseable timestamp"
#     tools/leg_read.py  --help  ->  "LEG: no completed games"
# Both are this repo's own verdict vocabulary. A reader asking a harmless
# question got an authoritative-looking sentence about nothing.
#
# ⛔ GATED ON `__main__`: several of these modules are IMPORTED by other tools
# (freshness by now.py). Ungated, this would fire during that import and make the
# PARENT exit 0 mid-run while printing the CHILD's docstring.
# ⛔ SELF-CONTAINED `import sys`: a first attempt used the file's own import, and
# broke on `import sys as _sys` (NameError) and on files whose imports come in
# two blocks. The guard must not depend on what the host file happens to import.
if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__ + "  (no module docstring)"))
        raise SystemExit(0)
ROOT=Path("/Users/junghard/Projects/Work/florent-code-game"); FC=str(ROOT/".venv/bin/fcode")
ml=subprocess.run([FC,"match","list","--json","--limit","120"],capture_output=True,text=True,cwd=ROOT)
rows=json.loads(ml.stdout); rows=rows if isinstance(rows,list) else rows.get("matches",[])
per=collections.defaultdict(lambda: {"g":0,"kill":0,"turns":[],"rat":0})
n=0
for m in rows:
    r=subprocess.run([FC,"match","info",m["id"],"--json"],capture_output=True,text=True,cwd=ROOT)
    try: d=json.loads(r.stdout)
    except Exception: continue
    mm=d["match"]; gs=d.get("games",[])
    if not gs: continue
    n+=1
    for side,name,rat in (("a",mm["teamAName"],mm.get("teamARating")),("b",mm["teamBName"],mm.get("teamBRating"))):
        p=per[name]; p["rat"]=rat or p["rat"]
        for g in gs:
            p["g"]+=1
            if g["winCondition"]=="core_destroyed": p["kill"]+=1
            p["turns"].append(g["turnsPlayed"])
print(f"matches censused: {n}  teams seen: {len(per)}\n")
elig=[(k,v) for k,v in per.items() if v["g"]>=20 and v["rat"]]
elig.sort(key=lambda x:-x[1]["rat"])
print(f"{'team':<26}{'rating':>7}{'games':>7}{'%core-kill':>12}{'median turns':>14}")
for k,v in elig[:16]:
    print(f"  {k[:24]:<24}{v['rat']:>7.0f}{v['g']:>7}{v['kill']/v['g']:>11.0%}{statistics.median(v['turns']):>14.0f}")
print()
top=[v for k,v in elig if v["rat"]>=1750]; bot=[v for k,v in elig if v["rat"]<1650]
def agg(x): 
    g=sum(v["g"] for v in x); k=sum(v["kill"] for v in x); t=[q for v in x for q in v["turns"]]
    return g,k/g,statistics.median(t)
if top and bot:
    g1,k1,t1=agg(top); g2,k2,t2=agg(bot)
    print(f"TOP TIER (>=1750): {len(top)} teams, {g1} games -> {k1:.0%} core-kill, median {t1:.0f} turns")
    print(f"LOWER (<1650):     {len(bot)} teams, {g2} games -> {k2:.0%} core-kill, median {t2:.0f} turns")
