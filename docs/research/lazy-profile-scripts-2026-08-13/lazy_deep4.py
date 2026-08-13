#!/usr/bin/env python3
"""Digs 4: counter-gunner geometry, rotations, opening determinism under map symmetry."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, "tools")
sys.path.insert(0, str(Path(__file__).parent))
from lazy_profile import parse, SEAT, d2  # noqa: E402
from replay_census import fields, parse_entity, WIRE_LEN  # noqa: E402

FILES = ([f"replay_archive/1ef56244-84a5-4136-ad8f-cf063b9fd3fe_game_{i}.replay26" for i in range(1, 6)]
         + [f"replay_archive/b9f3fab5-483a-443c-a2a3-695d69a8e915_game_{i}.replay26" for i in range(1, 6)])
G = {}
for f in FILES:
    g = parse(Path(f))
    G[("M1" if "1ef" in f else "M2") + "g" + f.split("_game_")[1][0]] = g
P = print

P("===== V. COUNTER-GUNNER GEOMETRY: gunner that shot our forward sentinel =====")
rows = []
for tag, g in G.items():
    L = SEAT[g["name"]]; U = 1 - L
    lc = g["corepos"][L]
    born = {b[5]: (b[0], b[2], tuple(b[3])) for b in g["builds"]}
    dr = {d[4]: d[0] for d in g["deaths"]}
    for rnd, t, kind, pos, dirn, eid in g["builds"]:
        if t != U or kind not in ("gunner", "sentinel") or d2(pos, lc) > 30:
            continue
        p = tuple(pos)
        shooters = {}
        for r, frm, to, tt, kk, sid in g["fires"]:
            if tt == L and to == p and r >= rnd and kk == "gunner":
                shooters.setdefault(sid, []).append(r)
        for sid, rs in shooters.items():
            br, bk, bp = born.get(sid, (None, "?", None))
            rows.append((d2(bp, p) if bp else None, (br - rnd) if br is not None else None))
            P(f"  {tag}: our {kind}@{p} born r{rnd} <- their gunner #{sid} @{bp} built r{br} "
              f"({'BEFORE' if br is not None and br < rnd else 'AFTER'} ours, "
              f"{br-rnd:+d} rounds) d2={d2(bp,p) if bp else '?'} shots={len(rs)} "
              f"first_shot=+{rs[0]-rnd}")
P(f"  --> counter-gunner d2 to our turret: {sorted(r[0] for r in rows if r[0] is not None)}")
pre = len([1 for r in rows if r[1] is not None and r[1] < 0])
P(f"  --> counter-gunner built BEFORE our turret in {pre}/{len(rows)} shooter-pairs "
  f"(i.e. reactive in {len(rows)-pre})")

P("\n===== W. GUNNER ROTATIONS (placeEntity re-emit with changed direction) =====")
for tag, g in G.items():
    L = SEAT[g["name"]]
    data = Path("replay_archive/" + g["name"]).read_bytes()
    turn_bufs = [v for n, w, v in fields(data) if n == 3 and w == WIRE_LEN]
    seen = {}
    rot = {0: 0, 1: 0}
    for rnd, tb in enumerate(turn_bufs):
        for _n, _w, ub in fields(tb):
            for un, _uw, ubuf in fields(ub):
                if un != 1:
                    continue
                for en, _ew, ebuf in fields(ubuf):
                    if en != 1:
                        continue
                    e = parse_entity(ebuf, rnd)
                    if e is None:
                        continue
                    if e.id in seen:
                        if seen[e.id][1] is not None and e.direction != seen[e.id][1]:
                            rot[e.team] = rot.get(e.team, 0) + 1
                    seen[e.id] = (e.kind, e.direction)
    P(f"  {tag}: rotations lazy={rot.get(L,0)} us={rot.get(1-L,0)}")

P("\n===== X. OPENING DETERMINISM: 14x18 map, seats swapped (M1g4 lazy@(6,4) vs M2g2 lazy@(6,12)) =====")
a, b = G["M1g4"], G["M2g2"]
La, Lb = SEAT[a["name"]], SEAT[b["name"]]
# map is 14x18; the two cores are (6,4) and (6,12): mirror y -> 16-y maps 4<->12
seqa = [(x[0], x[2], tuple(x[3])) for x in a["builds"] if x[1] == La][:16]
seqb = [(x[0], x[2], tuple(x[3])) for x in b["builds"] if x[1] == Lb][:16]
P("  M1g4 (lazy north core):  " + " ".join(f"r{r}:{k[:4]}@{p}" for r, k, p in seqa))
P("  M2g2 mirrored to north:  " + " ".join(
    f"r{r}:{k[:4]}@{(p[0], 16-p[1])}" for r, k, p in seqb))
sa = {(k, p) for _r, k, p in seqa}
sb = {(k, (p[0], 16 - p[1])) for _r, k, p in seqb}
P(f"  shared (kind,tile) in first 16 builds: {len(sa & sb)}/{len(sa)} -> {sorted(sa & sb)}")

P("\n===== Y. SPAWN CADENCE (lazy) =====")
for tag, g in G.items():
    L = SEAT[g["name"]]
    bb = [b[0] for b in g["builds"] if b[1] == L and b[2] == "builder_bot"]
    P(f"  {tag}: {bb[:10]}{'...' if len(bb)>10 else ''}")

P("\n===== Z. LAZY CONVERT_AMMO + ammo starvation =====")
for tag, g in G.items():
    L = SEAT[g["name"]]
    hist = [(r, row.get(L, (0, 0, 0))[2]) for r, row in g["ammo_hist"]]
    zeros = len([1 for _r, a in hist if a == 0])
    P(f"  {tag}: ammo samples={len(hist)} at_zero={zeros} ({100*zeros/max(1,len(hist)):.0f}%) "
      f"max={max(a for _r,a in hist) if hist else 0} end={hist[-1][1] if hist else 0}")
