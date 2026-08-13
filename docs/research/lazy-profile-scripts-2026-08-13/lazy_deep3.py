#!/usr/bin/env python3
"""Digs 3: what kills our forward turrets, their fire targeting, core-death rounds, siege tiles."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, "tools")
sys.path.insert(0, str(Path(__file__).parent))
from lazy_profile import parse, SEAT, d2  # noqa: E402

FILES = ([f"replay_archive/1ef56244-84a5-4136-ad8f-cf063b9fd3fe_game_{i}.replay26" for i in range(1, 6)]
         + [f"replay_archive/b9f3fab5-483a-443c-a2a3-695d69a8e915_game_{i}.replay26" for i in range(1, 6)])
G = {}
for f in FILES:
    g = parse(Path(f))
    G[("M1" if "1ef" in f else "M2") + "g" + f.split("_game_")[1][0]] = g
P = print

P("===== P. OUTCOME TABLE (core removals are ground truth) =====")
for tag, g in G.items():
    L = SEAT[g["name"]]; U = 1 - L
    dr = {d[4]: d[0] for d in g["deaths"]}
    lazy_core_died = dr.get(g["coreid"][L])
    our_core_died = dr.get(g["coreid"][U])
    P(f"  {tag} {g['w']}x{g['h']} rounds={g['rounds']} cond={g['wincond']} "
      f"winner={'LAZY' if g['winner']==L else 'US'} | lazy core killed "
      f"{'r%d' % lazy_core_died if lazy_core_died else '-'} | our core killed "
      f"{'r%d' % our_core_died if our_core_died else '-'}")

P("\n===== Q. WHAT KILLS OUR FORWARD TURRETS (shooter kind on the tile, last 12 rounds of life) =====")
gunkill = sent = batk = 0
lives = []
for tag, g in G.items():
    L = SEAT[g["name"]]; U = 1 - L
    lc = g["corepos"][L]
    dr = {d[4]: d[0] for d in g["deaths"]}
    for rnd, t, kind, pos, dirn, eid in g["builds"]:
        if t != U or kind not in ("gunner", "sentinel") or d2(pos, lc) > 30:
            continue
        died = dr.get(eid)
        if died is None:
            continue
        lives.append(died - rnd)
        p = tuple(pos)
        by = {}
        for r, frm, to, tt, kk, sid in g["fires"]:
            if tt == L and to == p and rnd <= r <= died:
                by[kk] = by.get(kk, 0) + 1
        na = len([1 for r, at, aid, ap, tg in g["batks"] if at == L and tg == p and rnd <= r <= died])
        if na:
            by["builder_attack"] = na
        P(f"  {tag} our {kind} @{p} life={died-rnd:<4d} killers={by}")
        if by.get("gunner"):
            gunkill += 1
        if by.get("sentinel"):
            sent += 1
        if na:
            batk += 1
P(f"  --> n={len(lives)} deaths; lives={sorted(lives)} median={sorted(lives)[len(lives)//2]}; "
  f"gunner involved {gunkill}, sentinel involved {sent}, builder_attack involved {batk}")

P("\n===== R. LAZY TURRET FIRE TARGETING: units vs buildings vs core =====")
for tag, g in G.items():
    L = SEAT[g["name"]]; U = 1 - L
    ufoot = g["foot"][U]
    ourb = {}
    for rnd, t, kind, pos, dirn, eid in g["builds"]:
        if t == U:
            ourb.setdefault(tuple(pos), set()).add(kind)
    cat = {}
    # occupancy at round start is expensive; approximate by classifying the target tile
    for r, frm, to, tt, kk, sid in g["fires"]:
        if tt != L:
            continue
        if to in ufoot:
            cat["our core"] = cat.get("our core", 0) + 1
        elif to in ourb:
            k = "/".join(sorted(ourb[to]))
            cat[k] = cat.get(k, 0) + 1
        else:
            cat["bare tile (unit/bot)"] = cat.get("bare tile (unit/bot)", 0) + 1
    P(f"  {tag}: {dict(sorted(cat.items(), key=lambda kv:-kv[1]))}")

P("\n===== S. SIEGE TILE SET: lazy turret tiles that ever shot OUR CORE, rel to our core NW =====")
allrel = []
for tag, g in G.items():
    L = SEAT[g["name"]]; U = 1 - L
    uc = g["corepos"][U]; ufoot = g["foot"][U]
    tiles = {}
    for r, frm, to, tt, kk, sid in g["fires"]:
        if tt == L and to in ufoot:
            tiles.setdefault((frm, kk), 0)
            tiles[(frm, kk)] += 1
    for (frm, kk), n in sorted(tiles.items(), key=lambda kv: -kv[1]):
        rel = (frm[0] - uc[0], frm[1] - uc[1])
        allrel.append((kk, rel, d2(frm, uc)))
        P(f"  {tag}: {kk} at {frm} rel_to_our_core={rel} d2={d2(frm,uc)} shots_at_core={n}")
P(f"  --> all siege tiles rel to our core NW: {allrel}")
P(f"  --> d2 distribution: {sorted(x[2] for x in allrel)}")

P("\n===== T. HOW LAZY REACHES OUR CORE: builder that builds the siege turret =====")
for tag, g in G.items():
    L = SEAT[g["name"]]; U = 1 - L
    uc = g["corepos"][U]
    firstsiege = None
    for rnd, t, kind, pos, dirn, eid in g["builds"]:
        if t == L and kind in ("gunner", "sentinel") and d2(pos, uc) <= 8:
            firstsiege = (rnd, kind, tuple(pos), eid)
            break
    if not firstsiege:
        P(f"  {tag}: no lazy turret within d2<=8 of our core")
        continue
    rnd, kind, pos, eid = firstsiege
    # lazy bots near that tile at that round
    near = [(e.id, tuple(e.pos)) for e in g["ents"].values()
            if e.team == L and e.kind == "builder_bot" and d2(e.pos, pos) <= 2]
    # first arrival of a lazy bot within d2<=8 of our core
    arr = None
    for r, t, bid, frm, to in g["moves"]:
        if t == L and d2(to, uc) <= 8:
            arr = (r, bid, to)
            break
    P(f"  {tag}: first siege turret r{rnd} {kind}@{pos}; first lazy bot within d2<=8 of our core "
      f"{'r%d #%d at %s' % arr if arr else 'never'}; travel->build gap="
      f"{rnd - arr[0] if arr else '-'}")

P("\n===== U. LAZY BARRIER USE (their own barriers, where) =====")
for tag, g in G.items():
    L = SEAT[g["name"]]; U = 1 - L
    lc, uc = g["corepos"][L], g["corepos"][U]
    bs = [(b[0], tuple(b[3])) for b in g["builds"] if b[1] == L and b[2] == "barrier"]
    near_us = len([1 for r, p in bs if d2(p, uc) < d2(p, lc)])
    P(f"  {tag}: barriers={len(bs)} near_our_core={near_us} sample={[(r,p,d2(p,uc)) for r,p in bs[:5]]}")
