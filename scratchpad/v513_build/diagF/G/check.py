#!/usr/bin/env python3
"""Instrument checks for dodge.py: drive every guard both ways."""
import collections
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from dodge import Game, d2, on_same_ray, steps_out_of_range, analyse
import feat

B = {r["tag"]: r for r in feat.load_batch()}

# --- C1: killer team must be ENEMY for every attributed fatal shot
bad_team = 0
tot_att = 0
kinds = collections.Counter()
for tag in sorted(B):
    g = Game(tag, B[tag]["ord"])
    rows, raiders, setB = analyse(g)
    for r in rows:
        if r["killer_id"] is not None:
            tot_att += 1
            if g.ents[r["killer_id"]]["team"] == g.ourteam:
                bad_team += 1
                print("  !! FRIENDLY-FIRE ATTRIBUTION", tag, r["rid"], r["killer_id"])
            kinds[g.ents[r["killer_id"]]["kind"]] += 1
print("C1 attributed fatal shots=%d  friendly-team attributions=%d  kinds=%s" % (tot_att, bad_team, dict(kinds)))

# --- C2: the 3 unattributed deaths — dump their raw hp/fire/attack neighbourhood
print("\nC2 UNATTRIBUTED FATAL SHOTS")
for tag, rid in (("atoll_g0", 3), ("atoll_g1", 4), ("nordkap_g3", 4)):
    g = Game(tag, B[tag]["ord"])
    print("  %s id%d  hp seq: %s" % (tag, rid, g.hphist[rid]))
    drnd = g.died[rnd] if False else g.died[rid]
    for r in range(drnd - 3, drnd + 1):
        fs = [f for f in g.fires if f[0] == r]
        print("     r%-4d raiderpos=%s  fires=%s" % (r, g.posat(rid, r), fs[:8]))
    print("     jumps involving it: %s" % [j for j in g.jumps if j[1] == rid][:6])

# --- C3: control — a positive case must attribute; corrupt the fire list and it must NOT
g = Game("nordkap_g7", "B")
rows, _, _ = analyse(g)
r0 = [r for r in rows if r["rid"] == 4][0]
print("\nC3 positive control nordkap_g7 id4 killer=%s at %s (should be sentinel)" %
      (r0["killer_kind"], r0["killer_pos"]))
saved = g.fires
g.fires = []
# blank the fire stream -> ray tests must flip to False
r1 = None
import dodge
gg = Game("nordkap_g7", "B")
gg.fires = []
rr, _, _ = analyse(gg)
r1 = [r for r in rr if r["rid"] == 4][0]
print("C3 negative control (fire stream emptied): ray_same=%s ray_any=%s (should be False/False)" %
      (r1["ray_same"], r1["ray_any"]))

# --- C4: ray test must be able to return False (it does for nordkap_g4 id54) and
#         a deliberately off-ray tile must read False
gk = Game("nordkap_g6", "A" if B["nordkap_g6"]["ord"] == "A" else "B")
tp = (11, 15)
prev = [f for f in gk.fires if f[2] == tp]
print("\nC4 turret %s fired %d times; sample rays=%s" % (tp, len(prev), sorted({(f[3]) for f in prev})[:8]))
print("   on_same_ray(turret,(11,16),(11,20)) ->", on_same_ray(tp, (11, 16), (11, 20)), "(expect True)")
print("   on_same_ray(turret,(11,16),(12,20)) ->", on_same_ray(tp, (11, 16), (12, 20)), "(expect False)")
print("   on_same_ray(turret,(11,16),(11,14)) ->", on_same_ray(tp, (11, 16), (11, 14)), "(expect False, opposite side)")

# --- C5: retreat BFS both ways
print("\nC5 steps_out_of_range: start ON turret tile, r2=32 ->", steps_out_of_range(gk, (11, 15), (11, 15), 32),
      "(expect >=6)")
print("   start already outside (d2=100) ->", steps_out_of_range(gk, (11, 5), (11, 15), 32), "(expect 0)")

# --- C6: distinguish hp deltas seen on our raiders
dd = collections.Counter()
for tag in sorted(B):
    g = Game(tag, B[tag]["ord"])
    rows, raiders, setB = analyse(g)
    for r in rows:
        for (rr_, dl, af) in r["hpseq"]:
            dd[dl] += 1
print("\nC6 hp-delta alphabet on the raider ids in the union set: %s" % dict(dd))
