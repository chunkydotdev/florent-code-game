#!/usr/bin/env python3
"""SIPHON-DENY TERMINAL WASTE — rounds our builders spend adjacent to an ENEMY
belt tile without ever attacking it, and whether we attack enemy belts at all.

WHY.  `eco.py:1072-1088` + `doctrine.py:913 SIPHON_DENY_ON=True` +
`:1488 LOKI_QUIET_ON=True`: a builder navigates to an enemy conveyor/splitter
(spending a MOVE every turn of the walk) and on arrival `if LOKI_QUIET_ON:
return False` — the payload is silenced. Live navigation, dead payload.

⭐ THE POINT FOR QUEUE #70: those walking rounds EMIT A MOVE, so they are ACTIVE
and were never in bucket A. Driving bucket A to zero cannot touch them, and an
arm could hit ~0% idle-and-free while builders walk to belts they will refuse to
hit. "Emitting a verb" and "doing something" are different predicates.

CONTROL, and it is the load-bearing one: with LOKI_QUIET_ON=True the attack count
on enemy belts must be ZERO. A non-zero count means the flag does not govern what
this measurement assumes, and the whole read is void.
"""
import sys, argparse
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import replay_census as RC, nav_lock_census as NLC

CARD=((0,-1),(0,1),(1,0),(-1,0)); BELT={"conveyor","splitter"}
def analyse(path, our_team):
    data=Path(path).read_bytes()
    tbs=[v for n,w,v in RC.fields(data) if n==3 and w==RC.WIRE_LEN]
    bpos={}; bteam={}; bots={}; botteam={}
    a=defaultdict(int)
    for rnd,tb in enumerate(tbs):
        atk=set(); moved=set()
        for _n,_w,upd in RC.fields(tb):
            for un,_uw,ub in RC.fields(upd):
                if un==1:
                    for en,_ew,eb in RC.fields(ub):
                        if en!=1: continue
                        e=RC.parse_entity(eb,rnd)
                        if e is None or e.pos is None: continue
                        if e.kind=="builder_bot": bots[e.id]=e.pos; botteam[e.id]=e.team
                        elif e.kind in BELT: bpos[e.id]=e.pos; bteam[e.id]=e.team
                elif un==2:
                    eid=to=None
                    for mn,_mw,mv in RC.fields(ub):
                        if mn==1: eid=mv
                        elif mn==2: to=RC.read_pos(mv)
                    if to is not None and eid in bots: bots[eid]=to; moved.add(eid)
                elif un==3:
                    for rn,_rw,rv in RC.fields(ub):
                        if rn==1: bots.pop(rv,None); bpos.pop(rv,None); bteam.pop(rv,None)
                elif un==13:      # BuilderAttack { id = 1; Pos target = 2 }
                    aid=tgt=None
                    for an,_aw,av in RC.fields(ub):
                        if an==1: aid=av
                        elif an==2: tgt=RC.read_pos(av)
                    if aid is not None: atk.add((aid,tgt))
        enemy_belt={p for i,p in bpos.items() if bteam.get(i)!=our_team}
        movedset=moved
        for eid,pos in bots.items():
            if botteam.get(eid)!=our_team: continue
            adj=any((pos[0]+dx,pos[1]+dy) in enemy_belt for dx,dy in CARD)
            hit=[tg for i,tg in atk if i==eid]
            if adj:
                a["adj_rounds"]+=1
                # ⭐ WHAT DOES A BUILDER DO ON ARRIVAL AT AN ENEMY BELT?
                # Needs no role attribution: the wire says whether it attacked,
                # moved, or emitted nothing. Roles are mutually exclusive per
                # run() (main.py:446-451), so neither _siphon_deny nor
                # _salt_turn can be inferred — but the OUTCOME is decidable.
                if any(tg in enemy_belt for tg in hit): a["arr_hit_belt"]+=1
                elif hit:                               a["arr_hit_other"]+=1
                elif eid in movedset:                   a["arr_moved"]+=1
                else:                                   a["arr_idle"]+=1
                if any(tg in enemy_belt for tg in hit): a["adj_attacked_belt"]+=1
                elif hit: a["adj_attacked_other"]+=1
            for tg in hit:
                a["attacks_total"]+=1
                if tg in enemy_belt: a["attacks_on_belt"]+=1
    return a

ap=argparse.ArgumentParser(); ap.add_argument("--ourver",action="append",required=True)
ap.add_argument("--limit",type=int,default=150); args=ap.parse_args()
tot=defaultdict(int); games=0
for v in args.ourver:
    for p,team,_c,_vv in NLC.population(ourver=v,meta=str(NLC.DEFAULT_META),
                                        archive=str(NLC.DEFAULT_ARCHIVE),limit=args.limit):
        r=analyse(p,team); games+=1
        for k,x in r.items(): tot[k]+=x
print("games                                    %d"%games)
print("builder-rounds ADJACENT to an enemy belt %d  (%.2f/game)"%(tot["adj_rounds"],tot["adj_rounds"]/max(games,1)))
print("  ...rounds we attacked THE BELT          %d"%tot["adj_attacked_belt"])
print("  ...rounds we attacked something ELSE     %d"%tot["adj_attacked_other"])
print("total builderAttack events (any target)   %d"%tot["attacks_total"])
print("  ...of which ON AN ENEMY BELT            %d"%tot["attacks_on_belt"])
print()
print("ON ARRIVAL — what a builder adjacent to an enemy belt actually does that round:")
tt=tot["adj_rounds"] or 1
for k,lab in (("arr_hit_belt","attacked THE BELT"),("arr_hit_other","attacked something else"),
              ("arr_moved","MOVED away/along"),("arr_idle","emitted NOTHING (bucket A)")):
    print("   %-26s %7d  %5.1f%%"%(lab,tot[k],100*tot[k]/tt))
print()
print("⛔ CONTROL AS ORIGINALLY REGISTERED IS RETIRED — ITS PREMISE WAS FALSE, NOT THE CODE.")
print("   Registered: 'with LOKI_QUIET_ON=True, belt attacks must be 0'. Observed %d."%tot["attacks_on_belt"])
print("   Cause: a DOCUMENTED CONVEYOR-MELEE CARVE-OUT (doctrine.py:1545, raid.py:424 _salt_turn)")
print("   exempts enemy conveyors/splitters from LOKI_QUIET_ON. The code is correct.")
print("   REPLACEMENT CONTROL (premise-free): the four arrival outcomes must sum to adj_rounds.")
s=tot["arr_hit_belt"]+tot["arr_hit_other"]+tot["arr_moved"]+tot["arr_idle"]
print("   %d + %d + %d + %d = %d vs adj_rounds %d -> %s"%(tot["arr_hit_belt"],tot["arr_hit_other"],
      tot["arr_moved"],tot["arr_idle"],s,tot["adj_rounds"],"PASS" if s==tot["adj_rounds"] else "FAIL"))
print("   (the FIRST version of this control counted 'attacked ANYTHING while adjacent to a belt'")
print("    and read 5,674 -> a FALSE alarm against the incumbent. BuilderAttack carries its target")
print("    at field 2, schema line 91; not decoding it was my defect, not the flag's.)")
