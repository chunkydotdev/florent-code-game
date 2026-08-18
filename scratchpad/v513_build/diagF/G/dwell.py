#!/usr/bin/env python3
"""Did the raider move at all in its warning window, and how long did it stand
on a tile that the killer turret had already been observed firing along?"""
import collections
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from dodge import Game, d2, on_same_ray, analyse
import feat

B = {r["tag"]: r for r in feat.load_batch()}
out = []
for tag in sorted(B):
    g = Game(tag, B[tag]["ord"])
    rows, raiders, setB = analyse(g)
    for r in rows:
        if r["killer_pos"] is None or r["fatal_rnd"] is None:
            continue
        kp = r["killer_pos"]
        fr = r["fatal_rnd"]
        rid = r["rid"]
        prev_rays = set()
        # rays the killer had been SEEN firing along strictly before round fr
        for (rr, s, f, t) in g.fires:
            if f == kp and rr < fr:
                prev_rays.add(t)
        # dwell: consecutive rounds ending at fr-1 where the raider stood on a
        # tile already on one of those rays (using rays seen before that round)
        dwell = 0
        rr = fr
        while rr - 1 >= g.born[rid]:
            rr -= 1
            p = g.posat(rid, rr)
            rays_then = [t for (r2, s2, f2, t2) in [] ] # placeholder
            seen = set(t for (r2, s2, f2, t) in g.fires if f2 == kp and r2 < rr)
            if p and any(on_same_ray(kp, t, p) for t in seen):
                dwell += 1
            else:
                break
        # movement in the warning window
        pr = r["pen_rnd"]
        moved = None
        distinct = None
        if pr is not None:
            tiles = [g.posat(rid, x) for x in range(pr, fr + 1)]
            distinct = len(set(tiles))
            moved = distinct > 1
        same_tile = (r["pen_tile"] == r["fatal_tile"]) if r["pen_tile"] else None
        # in-range dwell: rounds before the fatal shot spent within killer range
        rng2 = 32 if r["killer_kind"] == "sentinel" else 13
        inr = 0
        rr = fr
        while rr - 1 >= g.born[rid]:
            rr -= 1
            p = g.posat(rid, rr)
            if p and d2(p, kp) <= rng2:
                inr += 1
            else:
                break
        # how many rounds after the turret was BORN did the raider first enter its range
        tborn = g.born.get(r["killer_id"]) if r["killer_id"] else None
        out.append(dict(tag=tag, rid=rid, raider=r["is_raider"], kind=r["killer_kind"],
                        fatal_d2=r["fatal_d2"], dwell_on_ray=dwell, dwell_in_range=inr,
                        moved_in_window=moved, distinct_tiles=distinct, same_tile=same_tile,
                        gap=r["gap_pen_fatal"], vis=r["vis_ever"], turret_born=tborn,
                        raider_born=g.born[rid], fatal_rnd=fr, retreat=r["retreat_steps"]))

A = [o for o in out if o["raider"]]
for name, sel in (("SET A raiders", A), ("UNION", out)):
    print("\n=== %s  n=%d ===" % (name, len(sel)))
    print("   fatal shot fired from d2 > 20 (BEYOND the builder's own vision r2=20): %d/%d"
          % (sum(1 for o in sel if o["fatal_d2"] > 20), len(sel)))
    print("   fatal tile == penultimate-hit tile: %s" % collections.Counter(o["same_tile"] for o in sel))
    print("   raider MOVED between penultimate and fatal hit: %s" % collections.Counter(o["moved_in_window"] for o in sel))
    print("   distinct tiles occupied in that window: %s" % collections.Counter(o["distinct_tiles"] for o in sel))
    print("   consecutive rounds standing on a tile already on a SEEN ray of the killer, ending at the fatal shot: %s"
          % collections.Counter(o["dwell_on_ray"] for o in sel))
    print("   consecutive rounds inside the killer's attack range before the fatal shot: %s"
          % collections.Counter(min(o["dwell_in_range"], 40) for o in sel))
    print("   turret born round vs raider entering: turret_born=%s"
          % sorted(o["turret_born"] for o in sel if o["turret_born"] is not None))

print("\n-- per-death dwell table (union, n=%d)" % len(out))
print("tag             id   kind     fd2 dwellRay dwellRange moved distinctTiles sameTile gap vis retreat")
for o in out:
    print("%-15s %-4d %-8s %-3s %-8s %-10s %-5s %-13s %-8s %-3s %-3s %s" % (
        o["tag"], o["rid"], o["kind"], o["fatal_d2"], o["dwell_on_ray"], min(o["dwell_in_range"], 999),
        o["moved_in_window"], o["distinct_tiles"], o["same_tile"], o["gap"],
        "Y" if o["vis"] else "n", o["retreat"]))
