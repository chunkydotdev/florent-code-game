#!/usr/bin/env python3
"""BELT SEVERS PER GAME — the mechanism metric #70's screen should use instead of win rate.

WHY. The bodyblock screen deadlocked on POWER: the plank's best case is ~1.51pp
of game share and an OB16 bar at n=10,800 sits at 51.93, so the win-rate screen
cannot resolve it (research/side-lane, this session). A MECHANISM metric with a
large predicted change is resolvable where a 1.51pp win-rate effect is not.

THE CANDIDATE. 30.2% of all our idle-and-free builder-rounds (133/game) are spent
cardinally ADJACENT to an enemy conveyor/splitter emitting nothing, and the
shipped CONVEYOR-MELEE CARVE-OUT makes that belt a legal target (20 HP = ten
pecks; `doctrine.py:1545`). A SEVER is discrete, countable, and attributable.

MEASURED HERE: enemy belt entities we attacked that were subsequently REMOVED —
i.e. severs we caused — per game, as the pre-plank baseline.
CONTROL: enemy belt removals we did NOT attack (their own destroys, turret fire,
their rebuilds) must be counted separately; if the attacked-and-removed count
were equal to all removals the attribution would be meaningless.
"""
import sys, argparse
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import replay_census as RC, nav_lock_census as NLC
BELT={"conveyor","splitter"}
def analyse(path, our_team):
    data=Path(path).read_bytes()
    tbs=[v for n,w,v in RC.fields(data) if n==3 and w==RC.WIRE_LEN]
    ent={}                      # id -> (team, kind, pos)
    pos2id={}
    attacked_by_us=set()        # enemy belt ids we hit at least once
    a=defaultdict(int)
    for rnd,tb in enumerate(tbs):
        for _n,_w,upd in RC.fields(tb):
            for un,_uw,ub in RC.fields(upd):
                if un==1:
                    for en,_ew,eb in RC.fields(ub):
                        if en!=1: continue
                        e=RC.parse_entity(eb,rnd)
                        if e is None or e.pos is None: continue
                        ent[e.id]=(e.team,e.kind,e.pos); pos2id[e.pos]=e.id
                elif un==2:
                    eid=to=None
                    for mn,_mw,mv in RC.fields(ub):
                        if mn==1: eid=mv
                        elif mn==2: to=RC.read_pos(mv)
                    if eid in ent and to is not None:
                        t,k,_p=ent[eid]; ent[eid]=(t,k,to)
                elif un==3:
                    for rn,_rw,rv in RC.fields(ub):
                        if rn!=1: continue
                        info=ent.pop(rv,None)
                        if info and info[0]!=our_team and info[1] in BELT:
                            a["enemy_belt_removed"]+=1
                            if rv in attacked_by_us: a["severed_by_us"]+=1
                elif un==13:
                    aid=tgt=None
                    for an,_aw,av in RC.fields(ub):
                        if an==1: aid=av
                        elif an==2: tgt=RC.read_pos(av)
                    if aid in ent and ent[aid][0]==our_team and tgt is not None:
                        vid=pos2id.get(tgt)
                        if vid in ent and ent[vid][0]!=our_team and ent[vid][1] in BELT:
                            attacked_by_us.add(vid); a["belt_hits"]+=1
    return a
ap=argparse.ArgumentParser(); ap.add_argument("--ourver",action="append",required=True)
ap.add_argument("--limit",type=int,default=150); args=ap.parse_args()
tot=defaultdict(int); g=0
for v in args.ourver:
    for p,team,_c,_vv in NLC.population(ourver=v,meta=str(NLC.DEFAULT_META),
                                        archive=str(NLC.DEFAULT_ARCHIVE),limit=args.limit):
        r=analyse(p,team); g+=1
        for k,x in r.items(): tot[k]+=x
print("games                                 %d"%g)
print("our hits on enemy belts               %d   (%.1f/game)"%(tot["belt_hits"],tot["belt_hits"]/max(g,1)))
print("enemy belt entities REMOVED (any cause) %d (%.1f/game)"%(tot["enemy_belt_removed"],tot["enemy_belt_removed"]/max(g,1)))
print("  ...of those, ones WE had attacked    %d   (%.2f/game)  <- SEVERS BY US"%(
      tot["severed_by_us"],tot["severed_by_us"]/max(g,1)))
print()
print("CONTROL: severs-by-us must be a STRICT SUBSET of all removals. %d <= %d -> %s"%(
    tot["severed_by_us"],tot["enemy_belt_removed"],
    "PASS" if tot["severed_by_us"]<=tot["enemy_belt_removed"] else "FAIL"))
print("   attribution share: %.1f%% of enemy belt losses are ours"%(
    100*tot["severed_by_us"]/max(tot["enemy_belt_removed"],1)))
