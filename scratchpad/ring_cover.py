#!/usr/bin/env python3
"""DOES A SAFE FORWARD STATION EXIST?

LOKI-25 (gunner-axis penalty) cut forward deaths 24% and forward presence 23% --
deaths per forward build were FLAT (-2.3%). The builder's read: a penalty term
subtracts score from a bad station and never proposes a good one. The design they
want next PROPOSES a destination.

That design has a precondition nobody has measured: **are there tiles adjacent to
the enemy core that no enemy gunner covers?** If the ring is saturated by gunner
rays, no routing solution exists and the plank is dead on geometry rather than on
implementation.

Gunner: facing turret, straight-line shot, BLOCKED BY OBSTACLES, attack r^2 <= 13.
So a cardinal ray reaches d^2 = 1,4,9 (3 tiles); a diagonal ray d^2 = 2,8 (2 tiles).
The ray stops at the first occupied tile -- and that tile is itself covered.

Read-only. Research scratch instrument.
"""
from __future__ import annotations
import sys, json, glob, statistics as st
from pathlib import Path
from collections import defaultdict
ROOT = Path("/Users/junghard/Projects/Work/florent-code-game")
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import fields, read_pos, parse_entity, WIRE_LEN   # noqa
from peck_read import core_footprint                                  # noqa

DELTA = {0:(0,-1),1:(1,-1),2:(1,0),3:(1,1),4:(0,1),5:(-1,1),6:(-1,0),7:(-1,-1)}

def ray(pos, dirn, occupied, w, h):
    """Tiles a gunner at pos facing dirn can hit: along the ray, r^2<=13,
    stopping AT the first occupied tile (which is hit)."""
    d = DELTA.get(dirn)
    if d is None: return set()
    out=set(); x,y=pos
    for step in range(1,4):
        nx,ny = x+d[0]*step, y+d[1]*step
        if not (0<=nx<w and 0<=ny<h): break
        if (nx-x)**2+(ny-y)**2 > 13: break
        out.add((nx,ny))
        if (nx,ny) in occupied: break
    return out

def decode(path: Path, our_team: int, sample_every: int = 10):
    data=path.read_bytes(); mb=None; tbs=[]
    for n,w,v in fields(data):
        if n==1 and w==WIRE_LEN: mb=v
        elif n==3 and w==WIRE_LEN: tbs.append(v)
    if mb is None: return None
    W=H=None; cores=[]
    for n,w,v in fields(mb):
        if n==1: W=v
        elif n==2: H=v
        elif n==4 and w==WIRE_LEN:
            d={a:b for a,_,b in fields(v)}; cores.append((d.get(1,0),d.get(2,0),read_pos(d[3])))
    th=[c for c in cores if c[1]!=our_team]
    if not th or W is None: return None
    foot=core_footprint(th[0][2])
    ring={(x+dx,y+dy) for x,y in foot for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))}-foot
    ring={t for t in ring if 0<=t[0]<W and 0<=t[1]<H}
    ent={}
    samples=[]; our_fwd_rounds=0
    for rnd,tb in enumerate(tbs):
        for _n,_w,ub in fields(tb):
            for un,_uw,ubuf in fields(ub):
                if un==1:
                    for en,_ew,eb in fields(ubuf):
                        if en==1:
                            e=parse_entity(eb,rnd)
                            if e is not None: ent[e.id]=[e.team,e.kind,e.pos,e.direction]
                elif un==2:
                    aid=to=None
                    for a,_w2,v in fields(ubuf):
                        if a==1: aid=v
                        elif a==2: to=read_pos(v)
                    if aid in ent and to: ent[aid][2]=to
                elif un==3:
                    for a,_w2,v in fields(ubuf): ent.pop(v,None)
        if rnd % sample_every: continue
        occupied={e[2] for e in ent.values()}
        guns=[e for e in ent.values() if e[0]!=our_team and e[1]=="gunner" and e[3] is not None]
        ours_fwd=[e for e in ent.values() if e[0]==our_team and e[1]=="builder_bot"
                  and min((abs(e[2][0]-t[0])+abs(e[2][1]-t[1])) for t in ring)<=4]
        if not ours_fwd: continue
        our_fwd_rounds+=1
        covered=set()
        for g in guns: covered |= ray(g[2],g[3],occupied,W,H)
        samples.append((len(ring), len(ring & covered), len(guns)))
    if not samples: return None
    return dict(rounds=len(samples), fwd_rounds=our_fwd_rounds,
                ring=st.mean(s[0] for s in samples),
                cov=st.mean(s[1] for s in samples),
                guns=st.mean(s[2] for s in samples),
                zero_free=sum(1 for s in samples if s[0]-s[1]==0)/len(samples))

if __name__ == "__main__":
    meta={}
    for p in glob.glob("replay_archive/*.meta.json"):
        try: d=json.load(open(p))
        except Exception: continue
        a,b=d.get("teamAName"),d.get("teamBName")
        if a=="OpenSverige": meta[d["id"]]=0
        elif b=="OpenSverige": meta[d["id"]]=1
    import random; random.seed(0)
    mids=list(meta); random.shuffle(mids)
    res=[]
    for mid in mids[:220]:
        g=ROOT/f"replay_archive/{mid}_game_1.replay26"
        if not g.exists(): continue
        try: r=decode(g, meta[mid])
        except Exception: continue
        if r: res.append(r)
    print(f"games with a forward presence sampled: {len(res)}")
    print(f"  enemy-core ring tiles in bounds (mean): {st.mean(r['ring'] for r in res):.2f}")
    print(f"  ring tiles COVERED by an enemy gunner ray (mean): {st.mean(r['cov'] for r in res):.2f}")
    frac=st.mean(r['cov']/r['ring'] for r in res if r['ring'])
    print(f"  => COVERED FRACTION: {frac*100:.1f}%   FREE: {100-frac*100:.1f}%")
    print(f"  enemy gunners alive near ring (mean): {st.mean(r['guns'] for r in res):.2f}")
    print(f"  share of sampled rounds with ZERO free ring tiles: {st.mean(r['zero_free'] for r in res)*100:.1f}%")
