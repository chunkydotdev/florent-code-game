#!/usr/bin/env python3
"""Digs 2: harvester tile rule, attack targets, corrected response latency, core-tank maths."""
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

P("===== J. FIRST-HARVESTER TILE RULE (is it the nearest ore to their core?) =====")
for tag, g in G.items():
    L = SEAT[g["name"]]
    lc = g["corepos"][L]
    ore = [(x, y) for y, row in enumerate(g["tiles"]) for x, v in enumerate(row) if v == 2]
    ranked = sorted(ore, key=lambda p: (d2(p, lc), p[1], p[0]))
    harv = [(b[0], tuple(b[3])) for b in g["builds"] if b[1] == L and b[2] == "harvester"]
    order = []
    for r, p in harv:
        order.append(f"r{r}:{p}#{ranked.index(p)+1 if p in ranked else '?'}")
    P(f"  {tag}: ore_n={len(ore)} nearest3={[ (p, d2(p,lc)) for p in ranked[:3]]}")
    P(f"       lazy harvesters in build order (rank by dist from own core): {' '.join(order)}")

P("\n===== K. LAZY builderAttack TARGET KINDS =====")
for tag, g in G.items():
    L = SEAT[g["name"]]; U = 1 - L
    # tile -> our kind, tracking builds (buildings persist at their tile)
    ours = {}
    for rnd, t, kind, pos, dirn, eid in g["builds"]:
        if t == U:
            ours.setdefault(tuple(pos), set()).add(kind)
    ufoot = g["foot"][U]
    kinds = {}
    for r, t, aid, apos, tgt in g["batks"]:
        if t != L:
            continue
        if tgt in ufoot:
            kinds["OUR CORE"] = kinds.get("OUR CORE", 0) + 1
        elif tgt in ours:
            for k in ours[tgt]:
                kinds[k] = kinds.get(k, 0) + 1
        else:
            kinds["other/own/empty"] = kinds.get("other/own/empty", 0) + 1
    P(f"  {tag}: n={len([1 for r,t,a,ap,tg in g['batks'] if t==L])} "
      f"{dict(sorted(kinds.items(), key=lambda kv:-kv[1]))}")

P("\n===== L. CORRECTED RESPONSE LATENCY to OUR forward turrets (response after born only) =====")
lats = []
for tag, g in G.items():
    L = SEAT[g["name"]]; U = 1 - L
    lc = g["corepos"][L]
    dmap = {d[4]: d[0] for d in g["deaths"]}
    for rnd, t, kind, pos, dirn, eid in g["builds"]:
        if t != U or kind not in ("gunner", "sentinel") or d2(pos, lc) > 30:
            continue
        p = tuple(pos)
        resp = [r for r, at, aid, ap, tg in g["batks"] if at == L and tg == p and r >= rnd]
        shots = [r for r, frm, to, tt, kk, sid in g["fires"] if tt == L and to == p and r >= rnd]
        first = min(resp + shots, default=None)
        died = dmap.get(eid)
        if first is not None:
            lats.append(first - rnd)
        P(f"  {tag} our {kind} @{p} d2lazycore={d2(p,lc)} born r{rnd} "
          f"first_response={'+%d' % (first-rnd) if first is not None else 'NONE'} "
          f"(atk={len(resp)} shots={len(shots)}) death={'+%d' % (died-rnd) if died else 'survived'}")
P(f"  --> latency distribution (rounds): {sorted(lats)}  n={len(lats)} "
  f"median={sorted(lats)[len(lats)//2] if lats else '-'}")

P("\n===== M. CORE-TANK MATHS: lazy core heal rate under fire =====")
for tag, g in G.items():
    L = SEAT[g["name"]]
    cid = g["coreid"][L]
    ev = [(r, dl) for r, eid, _t, _k, _p, dl in g["hpev"] if eid == cid]
    dmg = [(r, -dl) for r, dl in ev if dl < 0]
    heal = [(r, dl) for r, dl in ev if dl > 0]
    if not dmg:
        P(f"  {tag}: core never damaged")
        continue
    w0, w1 = dmg[0][0], dmg[-1][0]
    healers = set()
    lfoot = g["foot"][L]
    for r, t, aid, tgt in g["bheals"]:
        if t == L and tgt in lfoot:
            healers.add(aid)
    hin = sum(dl for r, dl in heal if w0 <= r <= w1)
    din = sum(dl for r, dl in dmg)
    P(f"  {tag}: window r{w0}-r{w1} ({w1-w0} rounds) dmg={din} heal_in_window={hin} "
      f"({100*hin/max(1,din):.0f}%) distinct_core_healer_bots={len(healers)} "
      f"dmg_rate={din/max(1,w1-w0):.2f}/rnd heal_rate={hin/max(1,w1-w0):.2f}/rnd "
      f"core_died={'yes' if g['winner']==1-L else 'no'}")

P("\n===== N. OUR core under their siege: heal vs dmg =====")
for tag, g in G.items():
    L = SEAT[g["name"]]; U = 1 - L
    cid = g["coreid"][U]
    ev = [(r, dl) for r, eid, _t, _k, _p, dl in g["hpev"] if eid == cid]
    dmg = [(r, -dl) for r, dl in ev if dl < 0]
    heal = sum(dl for r, dl in ev if dl > 0)
    if not dmg:
        P(f"  {tag}: our core never damaged")
        continue
    P(f"  {tag}: our core dmg={sum(d for _, d in dmg)} heal=+{heal} "
      f"window r{dmg[0][0]}-r{dmg[-1][0]} died={'yes' if g['winner']==L else 'no'}")

P("\n===== O. LAZY unit counts and MAX_TEAM_UNITS pressure =====")
for tag, g in G.items():
    L = SEAT[g["name"]]
    bb = [b[0] for b in g["builds"] if b[1] == L and b[2] == "builder_bot"]
    dd = [d[0] for d in g["deaths"] if d[1] == L and d[2] == "builder_bot"]
    P(f"  {tag}: lazy builder bots built={len(bb)} died={len(dd)} "
      f"alive_end={len(bb)-len(dd)}; turrets built="
      f"{len([1 for b in g['builds'] if b[1]==L and b[2] in ('gunner','sentinel','launcher')])}")
