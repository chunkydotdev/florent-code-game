import json, heapq, statistics as st, collections
from pathlib import Path
SP=Path("/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/86e927e3-fb77-4d74-bdfe-69717bb9a2ae/scratchpad")
D=json.loads((SP/"tape602_raw.json").read_text())
BELT=("conveyor","splitter")
def run(exclude_bots=True, block_enemy_barriers=True):
    gaps=[]; rows=[]
    for n,r in sorted(D.items()):
        side=r["side"]; them=1-side
        tiles=r["tiles"]; H=len(tiles); W=len(tiles[0])
        ox,oy=r["corepos"][str(side)]
        foot={(ox+dx,oy+dy) for dx in (0,1) for dy in (0,1)}
        ours_belt=set(); ours_harv=set(); blocked=set()
        for (eid,team,kind,pos,dr) in r["final_ents"]:
            pos=tuple(pos)
            if kind=="builder_bot":
                if not exclude_bots: blocked.add(pos)
                continue
            if kind=="core":
                if team==them:
                    for dx in (0,1):
                        for dy in (0,1): blocked.add((pos[0]+dx,pos[1]+dy))
                continue
            if team==side and kind in BELT: ours_belt.add(pos)
            elif team==side and kind=="harvester": ours_harv.add(pos)
            else:
                if team==them and kind=="barrier" and not block_enemy_barriers: continue
                blocked.add(pos)
        dist={t:0 for t in foot}; pq=[(0,t) for t in foot]; heapq.heapify(pq)
        while pq:
            d,t=heapq.heappop(pq)
            if d>dist.get(t,1e9): continue
            for dx,dy in ((0,-1),(1,0),(0,1),(-1,0)):
                q=(t[0]+dx,t[1]+dy)
                if not (0<=q[0]<W and 0<=q[1]<H): continue
                if tiles[q[1]][q[0]]==1: continue
                if q in blocked: continue
                c=0 if (q in ours_belt or q in ours_harv or q in foot) else 1
                nd=d+c
                if nd<dist.get(q,1e9):
                    dist[q]=nd; heapq.heappush(pq,(nd,q))
        gl=[dist.get(h,-1) for h in sorted(ours_harv)]
        gaps+=gl
        rows.append((n,len(ours_harv),len(ours_belt),gl))
    return gaps,rows
gaps,rows=run()
print("=== WHERE THE BELT BREAKS (end of game, 0-1 BFS; 0 = our live belt, 1 = a tile we'd have to build) ===")
for n,h,b,gl in rows:
    print(f"{n.replace('.replay26',''):22} aliveHarv={h:>2} aliveBelt={b:>3} gaps={gl}")
c=collections.Counter(gaps)
print(); print("gap distribution over", len(gaps), "alive harvesters:", dict(sorted(c.items())))
print(f"  gap 0 (route complete): {c.get(0,0)}/{len(gaps)} = {100.0*c.get(0,0)/len(gaps):.1f}%  "
      f"[replay_census undirected chain: 24/76 = 31.6%]")
print(f"  1-2 short: {sum(v for k,v in c.items() if 1<=k<=2)}   3-5: {sum(v for k,v in c.items() if 3<=k<=5)}"
      f"   6-10: {sum(v for k,v in c.items() if 6<=k<=10)}   >10: {sum(v for k,v in c.items() if k>10)}"
      f"   unreachable: {c.get(-1,0)}")
g2=[x for x in gaps if x>0]
print(f"  median missing tiles among DISCONNECTED (n={len(g2)}): {st.median(g2)}  mean {sum(g2)/len(g2):.1f}")
# CONTROL: run the same BFS with enemy barriers NOT blocking -> gap must not increase anywhere
g3,_=run(block_enemy_barriers=False)
c3=collections.Counter(g3)
print()
print("CONTROL (same BFS, enemy barriers made passable) -> gap 0 count:",
      c3.get(0,0), "vs", c.get(0,0), "  (must be >= ; enemy barriers are a real obstruction)")
print("  distribution:", dict(sorted(c3.items())))
