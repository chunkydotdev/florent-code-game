#!/usr/bin/env python3
"""Oscillation: did the raider step OFF the fatal tile and step back onto it,
in phase with the turret's reload?  Plus the last-10-round position trace."""
import collections
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from dodge import Game, d2, analyse
import feat

B = {r["tag"]: r for r in feat.load_batch()}
rows = []
for tag in sorted(B):
    g = Game(tag, B[tag]["ord"])
    rs, raiders, setB = analyse(g)
    ecf = set(g.ecf)
    ering = set()
    for (x, y) in ecf:
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if (x + dx, y + dy) not in ecf:
                ering.add((x + dx, y + dy))
    for r in rs:
        if r["killer_pos"] is None:
            continue
        rid, fr, kp = r["rid"], r["fatal_rnd"], r["killer_pos"]
        ft = r["fatal_tile"]
        trace = []
        for x in range(max(g.born[rid], fr - 9), fr + 1):
            trace.append(g.posat(rid, x))
        # killer fire rounds in that window
        kf = sorted(set(rr for (rr, s, f, t) in g.fires if f == kp and fr - 9 <= rr <= fr))
        # did it leave and return to the fatal tile in the window?
        left_and_returned = False
        if ft in trace:
            idxs = [i for i, p in enumerate(trace) if p == ft]
            if len(idxs) >= 2 and any(trace[i] != ft for i in range(idxs[0], idxs[-1])):
                left_and_returned = True
        # was it on the enemy-core ring at death?
        on_ring = ft in ering
        # rounds the raider had spent on the ring before dying
        ring_rounds = sum(1 for x in range(g.born[rid], fr + 1)
                          if g.posat(rid, x) in ering)
        # killer fire cadence (gap between consecutive fire rounds, whole game)
        allk = sorted(set(rr for (rr, s, f, t) in g.fires if f == kp))
        cad = collections.Counter(b - a for a, b in zip(allk, allk[1:]))
        rows.append(dict(tag=tag, rid=rid, raider=r["is_raider"], kind=r["killer_kind"],
                         fatal_rnd=fr, fatal_tile=ft, killer=kp, trace=trace, kf=kf,
                         lr=left_and_returned, on_ring=on_ring, ring_rounds=ring_rounds,
                         d2ec=r["d2_to_ecore"], cad=dict(cad), nfires=len(allk),
                         gap=r["gap_pen_fatal"], same_tile=(r["pen_tile"] == r["fatal_tile"])))

A = [o for o in rows if o["raider"]]
for name, sel in (("SET A raiders", A), ("UNION", rows)):
    print("\n=== %s n=%d ===" % (name, len(sel)))
    print("   raider LEFT the fatal tile and RETURNED to it inside the last 10 rounds: %d/%d"
          % (sum(1 for o in sel if o["lr"]), len(sel)))
    print("   fatal tile is on the ENEMY CORE's orthogonal ring: %d/%d"
          % (sum(1 for o in sel if o["on_ring"]), len(sel)))
    print("   rounds the raider had already spent on that ring: median=%s max=%s"
          % (sorted(o["ring_rounds"] for o in sel)[len(sel) // 2], max(o["ring_rounds"] for o in sel)))
    print("   killer turret total shots in the game: %s" % sorted(o["nfires"] for o in sel))
    cc = collections.Counter()
    for o in sel:
        cc.update(o["cad"])
    print("   killer inter-shot gap histogram (pooled over the killers): %s" % dict(cc.most_common(8)))

print("\n-- last-10-round traces (SET A, n=%d).  * = killer fired that round" % len(A))
for o in A:
    fr = o["fatal_rnd"]
    start = fr - len(o["trace"]) + 1
    s = []
    for i, p in enumerate(o["trace"]):
        rr = start + i
        mark = "*" if rr in o["kf"] else " "
        s.append("%s%s" % (str(p), mark))
    print("  %-15s id%-4d %-8s killer%-9s fatal r%-4d %s" %
          (o["tag"], o["rid"], o["kind"], str(o["killer"]), fr, " ".join(s)))
