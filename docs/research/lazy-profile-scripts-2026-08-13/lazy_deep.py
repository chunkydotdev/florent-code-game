#!/usr/bin/env python3
"""Deep digs on team lazy: determinism, siege-sentinel lifecycle, escorts, no-dmg removals."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, "tools")
sys.path.insert(0, str(Path(__file__).parent))
from lazy_profile import parse, SEAT, d2, DIRN  # noqa: E402

FILES = ([f"replay_archive/1ef56244-84a5-4136-ad8f-cf063b9fd3fe_game_{i}.replay26" for i in range(1, 6)]
         + [f"replay_archive/b9f3fab5-483a-443c-a2a3-695d69a8e915_game_{i}.replay26" for i in range(1, 6)])
G = {}
for f in FILES:
    g = parse(Path(f))
    tag = ("M1" if "1ef" in f else "M2") + "g" + f.split("_game_")[1][0]
    G[tag] = g

P = print

P("===== A. MAP IDENTITY =====")
for tag, g in G.items():
    P(f"{tag}: {g['w']}x{g['h']} cores A@{g['corepos'][0]} B@{g['corepos'][1]} "
      f"ore={sum(r.count(2) for r in g['tiles'])} wall={sum(r.count(1) for r in g['tiles'])} "
      f"lazy=seat{'AB'[SEAT[g['name']]]}")

P("\n===== B. OPENING SEQUENCE, LAZY, first 22 builds (round:kind@pos rel-to-own-core) =====")
for tag, g in G.items():
    L = SEAT[g["name"]]
    lc = g["corepos"][L]
    seq = [(b[0], b[2], tuple(b[3])) for b in g["builds"] if b[1] == L][:22]
    P(f"{tag} core@{lc}: " + " ".join(
        f"r{r}:{k[:4]}@{p[0]-lc[0]},{p[1]-lc[1]}" for r, k, p in seq))

P("\n===== C. SIEGE TURRET LIFECYCLE (lazy turrets with d2 to OUR core <= 26) =====")
for tag, g in G.items():
    L = SEAT[g["name"]]; U = 1 - L
    uc = g["corepos"][U]
    ufoot = g["foot"][U]
    turrets = [(b[0], b[2], tuple(b[3]), b[5]) for b in g["builds"]
               if b[1] == L and b[2] in ("gunner", "sentinel") and d2(b[3], uc) <= 26]
    if not turrets:
        P(f"{tag}: no lazy turret within d2<=26 of our core")
        continue
    dmap = {d[4]: d[0] for d in g["deaths"]}
    hp_ids = {eid for _r, eid, _t, _k, _p, _d in g["hpev"]}
    for r, k, p, eid in turrets:
        died = dmap.get(eid)
        shots = len([1 for rr, frm, to, tt, kk, sid in g["fires"] if sid == eid])
        core_shots = len([1 for rr, frm, to, tt, kk, sid in g["fires"] if sid == eid and to in ufoot])
        heals = len([1 for rr, t, aid, tgt in g["bheals"] if t == L and tgt == p])
        # who built it: builder adjacent
        P(f"  {tag} {k:<8s} #{eid:<4d} @{p} d2ourcore={d2(p,uc):<3d} born r{r:<4d} "
          f"died {'r%d' % died if died else '-':<6s} life={died-r if died else g['rounds']-r:<4d} "
          f"shots={shots:<4d} at_core={core_shots:<4d} heals_on_tile={heals:<3d} "
          f"{'damaged' if eid in hp_ids else 'NEVER DAMAGED'}")

P("\n===== D. OUR FORWARD SENTINELS: survival + what lazy did about them =====")
for tag, g in G.items():
    L = SEAT[g["name"]]; U = 1 - L
    lc = g["corepos"][L]
    ours = [(b[0], b[2], tuple(b[3]), b[5]) for b in g["builds"]
            if b[1] == U and b[2] in ("gunner", "sentinel") and d2(b[3], lc) <= 30]
    dmap = {d[4]: d[0] for d in g["deaths"]}
    for r, k, p, eid in ours:
        died = dmap.get(eid)
        atk = [(rr, aid) for rr, at, aid, apos, tgt in g["batks"] if at == L and tgt == p]
        fired_at = [(rr, sid) for rr, frm, to, tt, kk, sid in g["fires"] if tt == L and to == p]
        first_resp = min([a[0] for a in atk] + [f[0] for f in fired_at], default=None)
        P(f"  {tag} OUR {k:<8s} #{eid:<4d} @{p} d2lazycore={d2(p,lc):<4d} born r{r:<4d} "
          f"died {'r%d' % died if died else '-':<6s} life={(died-r) if died else g['rounds']-r:<4d} "
          f"lazy_builder_attacks={len(atk):<3d} lazy_turret_shots={len(fired_at):<3d} "
          f"first_lazy_response={'r%d (+%d)' % (first_resp, first_resp-r) if first_resp else 'NONE'}")

P("\n===== E. REBUILD / REPAIR AGGREGATE (lazy) =====")
tot_d = tot_r = 0
lat_all = []
hdeaths = 0
for tag, g in G.items():
    L = SEAT[g["name"]]
    for kind in ("conveyor", "splitter", "harvester"):
        dl = [(d[0], tuple(d[3])) for d in g["deaths"] if d[1] == L and d[2] == kind]
        bl = [(b[0], tuple(b[3])) for b in g["builds"] if b[1] == L and b[2] == kind]
        if kind == "harvester":
            hdeaths += len(dl)
        for dr, dp in dl:
            tot_d += 1
            cand = [r for r, p in bl if p == dp and r > dr]
            if cand:
                tot_r += 1
                lat_all.append(min(cand) - dr)
P(f"lazy econ-building deaths across 10 games: {tot_d}; same-tile rebuilds: {tot_r} "
  f"({100*tot_r/max(1,tot_d):.0f}%); latencies={sorted(lat_all)}")
P(f"lazy HARVESTER deaths across 10 games: {hdeaths}")

P("\n===== F. HEAL TARGETING (lazy) =====")
for tag, g in G.items():
    L = SEAT[g["name"]]
    lc = g["corepos"][L]
    lfoot = g["foot"][L]
    hb = [(r, tgt) for r, t, aid, tgt in g["bheals"] if t == L]
    kinds = {}
    tiles = {}
    for rnd, t, kind, pos, dirn, eid in g["builds"]:
        if t == L:
            tiles[tuple(pos)] = kind
    for r, tgt in hb:
        if tgt in lfoot:
            kinds["core"] = kinds.get("core", 0) + 1
        else:
            kinds[tiles.get(tgt, "unit/empty")] = kinds.get(tiles.get(tgt, "unit/empty"), 0) + 1
    P(f"  {tag}: n={len(hb)} {dict(sorted(kinds.items(), key=lambda kv:-kv[1]))}")

P("\n===== G. NO-DAMAGE REMOVALS context (M1g2) =====")
g = G["M1g2"]
L = SEAT[g["name"]]; U = 1 - L
hp_ids = {eid for _r, eid, _t, _k, _p, _d in g["hpev"]}
nod = [(d[0], d[1], d[2], tuple(d[3]), d[4], d[5]) for d in g["deaths"] if d[4] not in hp_ids]
for r, t, k, p, eid, born in nod:
    near = [(e.kind, e.team, tuple(e.pos)) for e in g["ents"].values()
            if d2(e.pos, p) <= 8 and e.team == U]
    P(f"  r{r} team{'AB'[t]} {k} #{eid} @{p} born r{born} life={r-born}")
P("  our units/buildings near their base at r75-r115:")
for rnd, t, kind, pos, dirn, eid in g["builds"]:
    if t == U and d2(pos, g["corepos"][L]) <= 40 and rnd <= 115:
        P(f"    r{rnd} our {kind} @{tuple(pos)} d2lazycore={d2(pos, g['corepos'][L])}")
mv = [(r, eid, frm, to) for r, t, eid, frm, to in g["moves"]
      if t == U and 70 <= r <= 115 and d2(to, g["corepos"][L]) <= 25]
P(f"    our bot steps within d2<=25 of their core r70-115: {len(mv)}; sample {mv[:10]}")

P("\n===== H. AMMO / CONVERT (lazy) + builder attack usage =====")
for tag, g in G.items():
    L = SEAT[g["name"]]; U = 1 - L
    la = [len([1 for r, frm, to, t, k, s in g["fires"] if t == L]),
          len([1 for r, frm, to, t, k, s in g["fires"] if t == U])]
    ba = [len([1 for r, t, aid, ap, tg in g["batks"] if t == L]),
          len([1 for r, t, aid, ap, tg in g["batks"] if t == U])]
    P(f"  {tag}: lazy shots={la[0]} us shots={la[1]} | lazy builder_attacks={ba[0]} "
      f"us builder_attacks={ba[1]}")

P("\n===== I. FIRST-CONTACT TIMING: when does a lazy builder first reach our half / our core =====")
for tag, g in G.items():
    L = SEAT[g["name"]]; U = 1 - L
    uc = g["corepos"][U]
    first = None
    for r, t, eid, frm, to in g["moves"]:
        if t == L and d2(to, uc) <= 26:
            first = (r, eid, to)
            break
    firstb = None
    for rnd, t, kind, pos, dirn, eid in g["builds"]:
        if t == L and kind != "builder_bot" and d2(pos, uc) <= 26:
            firstb = (rnd, kind, tuple(pos))
            break
    P(f"  {tag} ({g['w']}x{g['h']}): first lazy bot within d2<=26 of our core: "
      f"{'r%d #%d at %s' % first if first else 'NEVER'} | first lazy build there: "
      f"{'r%d %s@%s' % firstb if firstb else 'NEVER'}")
