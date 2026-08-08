"""Per-GAME census from the API -- no replay downloads, no parsing.

Built 2026-08-08 s19 after Magnus asked "can you inspect the data we pull so we
do not miss data points that should be pulled, not calculated". `fcode match
info <id> --json` returns a `games[]` array carrying PER GAME:

    mapName · mapSeed · winnerId · winnerSide (the SEAT) · winCondition
    · turnsPlayed · resignMessage · replayS3Key

Everything this project decoded replay binaries to derive at game level is
structured JSON on a free endpoint. REPLAYS ARE STILL REQUIRED below game
level: entity builds, turret placement, damage, titanium amounts.
"""
import json, subprocess, collections
from pathlib import Path
ROOT=Path("/Users/junghard/Projects/Work/florent-code-game"); FC=str(ROOT/".venv/bin/fcode")
OURS="379a5d80-9921-4c9e-949b-f9b1dcba16be"
ml=subprocess.run([FC,"match","list","--mine","--type","ladder","--json","--limit","40"],
                  capture_output=True,text=True,cwd=ROOT)
rows=json.loads(ml.stdout); rows=rows if isinstance(rows,list) else rows.get("matches",[])
games=[]
for m in rows:
    r=subprocess.run([FC,"match","info",m["id"],"--json"],capture_output=True,text=True,cwd=ROOT)
    try: d=json.loads(r.stdout)
    except Exception: continue
    ourside = 'a' if d['match']['teamAId']==OURS else 'b'
    for g in d.get("games",[]):
        games.append(dict(map=g["mapName"], seat=ourside, won=(g["winnerId"]==OURS),
                          cond=g["winCondition"], turns=g["turnsPlayed"],
                          opp=d['match']['teamBName'] if ourside=='a' else d['match']['teamAName']))
print(f"GAMES PULLED: {len(games)} from {len(rows)} matches, ZERO replay downloads\n")
w=sum(g['won'] for g in games)
print(f"overall game share: {w}/{len(games)} = {w/len(games):.1%}\n")
r1000=[g for g in games if g['turns']>=1000]
print(f"games reaching r1000: {len(r1000)}/{len(games)} = {len(r1000)/len(games):.1%}")
print(f"  of those, decided by titanium_collected: {sum(1 for g in r1000 if g['cond']=='titanium_collected')}/{len(r1000)}")
print()
print("BY SEAT:")
for s in ('a','b'):
    ss=[g for g in games if g['seat']==s]
    if ss: print(f"  seat {s}: {sum(x['won'] for x in ss)}/{len(ss)} = {sum(x['won'] for x in ss)/len(ss):.1%}")
print()
print("BY MAP (game share, our wins/total):")
bm=collections.defaultdict(lambda:[0,0])
for g in games: bm[g['map']][0]+=g['won']; bm[g['map']][1]+=1
for k in sorted(bm, key=lambda x:-bm[x][1]):
    a,b=bm[k]; print(f"  {k:<14}{a:>3}/{b:<4}{a/b:>7.0%}")
print()
print("WIN CONDITION mix (our WINS vs our LOSSES):")
cw=collections.Counter(g['cond'] for g in games if g['won'])
cl=collections.Counter(g['cond'] for g in games if not g['won'])
for c in set(cw)|set(cl): print(f"  {c:<22} won {cw[c]:>3}   lost {cl[c]:>3}")
print()
print("MEDIAN TURNS: wins vs losses")
import statistics
tw=[g['turns'] for g in games if g['won']]; tl=[g['turns'] for g in games if not g['won']]
print(f"  our wins  : median {statistics.median(tw):.0f}  (n={len(tw)})")
print(f"  our losses: median {statistics.median(tl):.0f}  (n={len(tl)})")
