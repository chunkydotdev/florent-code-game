#!/usr/bin/env python3
"""Alignment: fatal tile vs the OTHER tile of the 2-cycle, relative to the killer."""
import collections
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from dodge import Game, d2, analyse
import feat

SENT, GUN = 32, 13


def aligned(turret, tile):
    dx, dy = tile[0] - turret[0], tile[1] - turret[1]
    return dx == 0 or dy == 0 or abs(dx) == abs(dy)


B = {r["tag"]: r for r in feat.load_batch()}
out = []
for tag in sorted(B):
    g = Game(tag, B[tag]["ord"])
    rs, _r, _s = analyse(g)
    for r in rs:
        if r["killer_pos"] is None:
            continue
        rid, fr, kp, ft = r["rid"], r["fatal_rnd"], r["killer_pos"], r["fatal_tile"]
        rng = SENT if r["killer_kind"] == "sentinel" else GUN
        win = [g.posat(rid, x) for x in range(max(g.born[rid], fr - 9), fr + 1)]
        others = [p for p in win if p != ft]
        oth = collections.Counter(others).most_common(1)
        oth = oth[0][0] if oth else None
        out.append(dict(
            tag=tag, rid=rid, raider=r["is_raider"], kind=r["killer_kind"],
            fatal_aligned=aligned(kp, ft), other=oth,
            other_aligned=aligned(kp, oth) if oth else None,
            fatal_d2=d2(ft, kp), other_d2=d2(oth, kp) if oth else None,
            both_in_range=(d2(ft, kp) <= rng and oth is not None and d2(oth, kp) <= rng),
            ncyc=len(set(win)),
            gap=r["gap_pen_fatal"], retreat=r["retreat_steps"],
        ))

A = [o for o in out if o["raider"]]
for name, sel in (("SET A raiders", A), ("UNION", out)):
    print("\n=== %s n=%d ===" % (name, len(sel)))
    print("   fatal tile ALIGNED with the killer (row/col/diagonal): %d/%d"
          % (sum(1 for o in sel if o["fatal_aligned"]), len(sel)))
    print("   the OTHER most-occupied tile of the last-10 window is aligned: %s"
          % collections.Counter(o["other_aligned"] for o in sel))
    print("   BOTH tiles of the cycle inside the killer's attack range: %d/%d"
          % (sum(1 for o in sel if o["both_in_range"]), len(sel)))
    print("   distinct tiles in the last 10 rounds: %s" % collections.Counter(o["ncyc"] for o in sel))
    print("   fatal_d2 vs other_d2 (the sidestep barely changes distance): %s"
          % [(o["fatal_d2"], o["other_d2"]) for o in sel][:40])
