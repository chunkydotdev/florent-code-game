#!/usr/bin/env python3
"""s51 CRATER-vs-SWEEP autopsy -- OUR opening chain, route shape, first contact
and death ledger, per local game.

The s51 RING study (docs/research/RING-ENGAGEMENT-mjolnir-2026-08-20.md) closed
two roads: the sweep/crater split is NOT carried by Mjolnir's ring engagement
(65.7pp +/- 8.0 survives matching) and NOT by any geometry SCALAR (royale and
yulerune are the same 20x20 board at the same core separation, 92% vs 18%).
What is left is OUR opening and route, and the map LAYOUT they run through.

This walks the turn stream once and emits, for one game, from OUR seat:

  OPENING   spawn tiles + their forwardness, first harvester round/tile/BFS
            depth, harvester+conveyor counts at r30/r60, titanium banked and
            titaniumCollected at r30/60/100 for both teams (UpdatePlayers).
  ROUTE     per builder-bot tracks: departure from our apron, arrival at their
            apron (d^2 <= 36 and <= 16), move count, BFS-optimal count, detour
            ratio, IMMEDIATE-REVERSAL rate (the livelock signature that
            tools/map_encode.py exists because of), choke tiles crossed.
  CONTACT   first damage event anywhere: round, victim team, weapon, and which
            core's BFS basin it landed in; our forward presence at contact and
            20 rounds later (commit vs retreat).
  DEATHS    our builder-bot deaths by BASIN (home / mid / their apron), the
            concentration of death tiles (farmed-at-a-choke signature), damage
            received by weapon, and both cores' first-damage round / HP floor.

Usage:
  routetape.py --game <replay26> <map> <ourseat A|B>
  routetape.py --batch <results.tsv> <repdir> [--out F] [--limit N]
  routetape.py --selftest <replay26> <map> <ourseat>    # both-verdicts controls
"""
from __future__ import annotations

import sys
from collections import Counter, deque
from pathlib import Path

if __name__ == "__main__":
    import sys as _hg
    if "-h" in _hg.argv[1:] or "--help" in _hg.argv[1:]:
        print(__doc__)
        raise SystemExit(0)

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "scratchpad" / "s51_route"))
from replay_census import (  # noqa: E402
    fields, parse_entity, read_pos, parse_update_hp, DELTA_WEAPON,
    DIRECTION_DELTA)
from mapgeom import (  # noqa: E402  -- SHARED geometry, on purpose
    load, footprint, passable, bfs_from, geom, CARD)

BUILDINGS = {"barrier", "harvester", "gunner", "sentinel", "launcher", "core",
             "conveyor", "splitter"}
TURRETS = {"gunner", "sentinel", "launcher"}
DMG = (-18, -7, -2)
APRON_DSQ = 36          # "at a core" -- matches the ring study's near band
NEAR_DSQ = 16           # RING_NEAR_DSQ, x3r0's own trigger radius


def _dsq(p, tiles):
    return min((p[0] - a) ** 2 + (p[1] - b) ** 2 for a, b in tiles)


ECO_SNAPS = (30, 60, 100, 150)
CONV_KINDS = ("conveyor", "splitter")


def _ring_snapshot(ents, ourteam, ourfp, d_our):
    """Mirror of the RING study, pointed at OUR OWN core: how much of our own
    home ring is held by the ENEMY, and how close does our belt head get?"""
    ring = set()
    for a, b in ourfp:
        for dx, dy in CARD:
            t = (a + dx, b + dy)
            if t not in set(ourfp):
                ring.add(t)
    enemy_ring = 0
    conv_d = []
    harv_d = []
    conv_home = 0
    for _eid, (k, tm, pos, _d) in ents.items():
        if tm != ourteam:
            if pos in ring:
                enemy_ring += 1
            continue
        if k in CONV_KINDS:
            dd = d_our.get(pos)
            if dd is not None:
                conv_d.append(dd)
            if dd == 1:
                conv_home += 1
        elif k == "harvester":
            dd = d_our.get(pos)
            if dd is not None:
                harv_d.append(dd)
    return (enemy_ring, min(conv_d) if conv_d else -1,
            min(harv_d) if harv_d else -1, conv_home)


def _eco_snapshot(ents, ourteam, ourfp):
    """How many of OUR harvesters have a live CONVEYOR ROUTE HOME right now?

    `titanium_collected` counts DELIVERY TO THE CORE, so an unwired harvester
    is worth zero forever (CLAUDE.md, engine-probed).  A harvester is WIRED if
    some orthogonally adjacent friendly conveyor/splitter starts a chain of
    friendly conveyors whose outputs reach the core footprint.  Splitters fan
    out, so any of their 3 non-back outputs counts -- we take the optimistic
    reading (a splitter is treated as reaching home if ANY continuation does),
    which can only OVERSTATE connectivity and therefore cannot manufacture the
    "zero collected" verdict this column exists to test.
    """
    byp = {}
    for _eid, v in ents.items():
        if v[1] != ourteam:
            continue
        byp.setdefault(v[2], []).append(v)
    core = set(ourfp)
    # reverse walk: tiles whose conveyor output eventually lands on the core
    good = set()
    frontier = set()
    for pos, vs in byp.items():
        for k, _t, _p, d in vs:
            if k not in CONV_KINDS:
                continue
            outs = []
            if k == "conveyor":
                dd = DIRECTION_DELTA.get(d or 0, (0, 0))
                outs = [(pos[0] + dd[0], pos[1] + dd[1])]
            else:                       # splitter: 3 outputs, back excluded
                dd = DIRECTION_DELTA.get(d or 0, (0, 0))
                back = (-dd[0], -dd[1])
                outs = [(pos[0] + a, pos[1] + b)
                        for a, b in DIRECTION_DELTA.values()
                        if (a, b) not in ((0, 0), back)]
            if any(o in core for o in outs):
                good.add(pos)
                frontier.add(pos)
            byp[pos] = [(k, outs)]
    changed = True
    while changed:
        changed = False
        for pos, vs in byp.items():
            if pos in good or not vs or len(vs[0]) != 2:
                continue
            _k, outs = vs[0]
            if any(o in good for o in outs):
                good.add(pos)
                changed = True
    harv = [v[2] for v in ents.values()
            if v[1] == ourteam and v[0] == "harvester"]
    wired = 0
    for hp2 in harv:
        # a harvester ORTHOGONALLY ADJACENT to the core needs no belt at all --
        # the core is itself an acceptor.  Missing this was the source of 127
        # false negatives against the engine's titaniumCollected on the first
        # pass (nordkap 25, yulerune 22, frostgate 20 ...).
        hit = any((hp2[0] + dx, hp2[1] + dy) in core for dx, dy in CARD)
        if not hit:
            hit = any((hp2[0] + dx, hp2[1] + dy) in good for dx, dy in CARD)
        wired += int(hit)
    return (len(harv), wired, len(good))


def walk(replay_path, mapname, ourseat, anchor_swap=False):
    w, h, rows, anchors = load(mapname)
    ourteam = 0 if ourseat == "A" else 1
    theirteam = 1 - ourteam
    if anchor_swap:                      # MUTATION control: pretend seats flip
        ourteam, theirteam = theirteam, ourteam
    ourfp = footprint(anchors[ourteam])
    theirfp = footprint(anchors[theirteam])
    ok = passable(rows, w, h)
    d_our = bfs_from(ourfp, ok)
    d_their = bfs_from(theirfp, ok)
    bfs_cc = min((d_their[t] for t in ourfp if t in d_their), default=-1)
    choke = {t for t in ok
             if sum(1 for dx, dy in CARD if (t[0] + dx, t[1] + dy) in ok) <= 2}
    _fp = set(ourfp)
    homering = [t for t in
                [(a + dx, b + dy) for a, b in ourfp for dx, dy in CARD]
                if t not in _fp and 0 <= t[0] < w and 0 <= t[1] < h
                and rows[t[1]][t[0]] != 1]
    homering = sorted(set(homering))

    data = Path(replay_path).read_bytes()
    map_buf, turn_bufs = None, []
    winner = None
    for num, wire, val in fields(data):
        if num == 1 and wire == 2:
            map_buf = val
        elif num == 3 and wire == 2:
            turn_bufs.append(val)
        elif num == 4 and wire == 0:
            winner = val

    ents = {}                      # live id -> [kind, team, pos]
    ever = {}                      # never popped: id -> (kind, team)
    lastpos = {}                   # never popped: id -> pos
    if map_buf is not None:
        for mn, mw2, mv in fields(map_buf):
            if mn == 4 and mw2 == 2:
                cid = team = 0
                pos = None
                for cn, cw, cv in fields(mv):
                    if cn == 1:
                        cid = cv
                    elif cn == 2:
                        team = cv
                    elif cn == 3 and cw == 2:
                        pos = read_pos(cv)
                if pos is not None:
                    ents[cid] = ["core", team, pos, None]
                    ever[cid] = ("core", team)
                    lastpos[cid] = pos

    ev = {                          # accumulators
        "spawns": [], "harv": {0: [], 1: []}, "conv": {0: [], 1: []},
        "turret": {0: [], 1: []}, "bots": {0: [], 1: []},
        "players": [],              # per round: (ti_a, coll_a, ti_b, coll_b)
        "tracks": {},               # our bot id -> list[(rnd,pos)]
        "botdeath": [],             # (rnd, team, pos)
        "recv": {0: Counter(), 1: Counter()},
        "corehp": {0: [], 1: []},
        "firstdmg": None, "throws": [], "eco": {}, "ring": {}, "home": [], "headd": [], "headadj": [], "atring": [],
        "ourbuild_theirhalf": [],   # (rnd, kind, pos) our building in their basin
    }
    lasthit = {}
    corehp = {0: 500, 1: 500}
    coreid = {t: [i for i, v in ever.items() if v[1] == t][0] for t in (0, 1)}

    for rnd, tb in enumerate(turn_bufs):
        for _n, _w, ubuf in fields(tb):
            for unum, _uw, ub in fields(ubuf):
                if unum == 1:                                  # placeEntity
                    for en, _ew, eb in fields(ub):
                        if en != 1:
                            continue
                        e = parse_entity(eb, rnd)
                        if e is None:
                            continue
                        new = e.id not in ever
                        ents[e.id] = [e.kind, e.team, e.pos, e.direction]
                        ever[e.id] = (e.kind, e.team)
                        lastpos[e.id] = e.pos
                        if not new:
                            continue
                        if e.kind == "builder_bot":
                            ev["bots"][e.team].append((rnd, e.pos))
                            if e.team == ourteam:
                                ev["spawns"].append((rnd, e.pos))
                                ev["tracks"][e.id] = [(rnd, e.pos)]
                        elif e.kind == "harvester":
                            ev["harv"][e.team].append((rnd, e.pos))
                        elif e.kind in ("conveyor", "splitter"):
                            ev["conv"][e.team].append((rnd, e.pos))
                        elif e.kind in TURRETS:
                            ev["turret"][e.team].append((rnd, e.pos))
                        if (e.team == ourteam and e.kind in BUILDINGS
                                and e.kind != "core"):
                            dt = d_their.get(e.pos)
                            do = d_our.get(e.pos)
                            if dt is not None and do is not None and dt < do:
                                ev["ourbuild_theirhalf"].append(
                                    (rnd, e.kind, e.pos))
                elif unum == 2:                                # moveBuilderBot
                    eid = to = None
                    for mn2, _mw3, mv2 in fields(ub):
                        if mn2 == 1:
                            eid = mv2
                        elif mn2 == 2:
                            to = read_pos(mv2)
                    if eid in ents and to is not None:
                        frm = ents[eid][2]
                        ents[eid][2] = to
                        lastpos[eid] = to
                        # A LAUNCHER THROW is engine-visible as a
                        # moveBuilderBot of Chebyshev step > 1 (a legal walk is
                        # exactly one CARDINAL step).  This is the arm read off
                        # an ENGINE-SIDE fact, never off our own stdout.
                        step = max(abs(to[0] - frm[0]), abs(to[1] - frm[1]))
                        if step > 1:
                            ev["throws"].append(
                                (rnd, ents[eid][1], frm, to, step))
                        if eid in ev["tracks"]:
                            ev["tracks"][eid].append((rnd, to))
                elif unum == 3:                                # removeEntity
                    for rn2, _rw, rv in fields(ub):
                        if rn2 != 1:
                            continue
                        cur = ents.pop(rv, None)
                        k_t = ever.get(rv)
                        if k_t and k_t[0] == "builder_bot":
                            lh = lasthit.get(rv)
                            # KILLER CLASS: the last damage delta this body took,
                            # and only if it landed in the round it died or the
                            # one before -- otherwise the body left for another
                            # reason (self-destruct) and attributing it to an old
                            # scratch would invent a killer.
                            kc = (DELTA_WEAPON.get(lh[1], "?")
                                  if lh and rnd - lh[0] <= 1 else "none")
                            ev["botdeath"].append(
                                (rnd, k_t[1], lastpos.get(rv), kc))
                        del cur
                elif unum == 5:                                # UpdateHp
                    eid, delta = parse_update_hp(ub)
                    kt = ever.get(eid)
                    if kt is None:
                        continue
                    if delta in DMG:
                        ev["recv"][kt[1]][delta] += 1
                        lasthit[eid] = (rnd, delta)
                        if ev["firstdmg"] is None:
                            ev["firstdmg"] = (rnd, kt[1], delta,
                                              lastpos.get(eid))
                    if kt[0] == "core":
                        corehp[kt[1]] = max(0, corehp[kt[1]] + delta)
                elif unum == 6:                                # updatePlayers
                    pa = pb = None
                    for pn, _pw, pv in fields(ub):
                        if pn != 1:
                            continue
                        for sn, _sw, sv in fields(pv):
                            d = {}
                            for fn, _fw, fv in fields(sv):
                                d[fn] = fv
                            if sn == 1:
                                pa = d
                            elif sn == 2:
                                pb = d
                    if pa is not None and pb is not None:
                        ev["players"].append(
                            (pa.get(1, 0), pa.get(4, 0),
                             pb.get(1, 0), pb.get(4, 0)))
        cd = [d_our.get(v[2], 99) for v in ents.values()
              if v[1] == ourteam and v[0] in CONV_KINDS]
        ev["headd"].append(min(cd) if cd else 99)
        # THE DECOMPOSITION.  Take every one of OUR conveyors sitting exactly
        # ONE BFS step short of home (d==2) -- a dead head -- and ask what is
        # standing on the ring socket it points into.  "free" means we could
        # have finished the belt this round and did not; anything else means
        # the socket was denied.  Both branches must be observed or this column
        # is not measuring.
        occ = {}
        for v in ents.values():
            occ.setdefault(v[2], []).append(v)
        free = denied_enemy = denied_own = 0
        for v in ents.values():
            if v[1] != ourteam or v[0] not in CONV_KINDS:
                continue
            if d_our.get(v[2]) != 2:
                continue
            for dx, dy in CARD:
                t = (v[2][0] + dx, v[2][1] + dy)
                if d_our.get(t) != 1:
                    continue
                here = occ.get(t, [])
                if not here:
                    free += 1
                elif any(x[1] != ourteam for x in here):
                    denied_enemy += 1
                else:
                    denied_own += 1
        # RE-PLAN HEADROOM: the head's own socket is denied, yet some OTHER
        # ring socket is empty and would accept the belt.  This is the half of
        # the failure that is ours to fix, and it is reported with the walking
        # distance from the head to that socket so it is priced, not just
        # counted.
        heads = [v[2] for v in ents.values()
                 if v[1] == ourteam and v[0] in CONV_KINDS
                 and d_our.get(v[2]) == 2]
        freerings = [t for t in homering if not occ.get(t)]
        rd = -1
        if heads and freerings:
            rd = min(abs(a[0] - b[0]) + abs(a[1] - b[1])
                     for a in heads for b in freerings)
        ev["headadj"].append((free, denied_enemy, denied_own,
                              len(freerings), rd))
        n8 = n16 = 0
        for v in ents.values():
            if v[1] != ourteam or v[0] != "builder_bot":
                continue
            dd = _dsq(v[2], theirfp)
            if dd <= 8:
                n8 += 1
            if dd <= 16:
                n16 += 1
        est = sum(1 for v in ents.values()
                  if v[1] == ourteam and v[0] in BUILDINGS
                  and v[0] != "core" and _dsq(v[2], theirfp) <= 8)
        ev["atring"].append((n8, n16, est))
        homeocc = []
        for t in homering:
            here = [v for v in ents.values() if v[2] == t]
            bl = [v for v in here if v[0] in BUILDINGS]
            bo = [v for v in here if v[0] == "builder_bot"]
            if bl:
                k, tm = bl[0][0], bl[0][1]
                if tm == ourteam:
                    homeocc.append("Oc" if k in CONV_KINDS else "Ob")
                else:
                    homeocc.append("Ex" if k == "barrier" else "Eb")
            elif bo:
                homeocc.append("Od" if bo[0][1] == ourteam else "Ed")
            else:
                homeocc.append(".")
        ev["home"].append(tuple(homeocc))
        ev["corehp"][0].append(corehp[0])
        ev["corehp"][1].append(corehp[1])
        if rnd in ECO_SNAPS:
            ev["eco"][rnd] = _eco_snapshot(ents, ourteam, ourfp)
            ev["ring"][rnd] = _ring_snapshot(ents, ourteam, ourfp, d_our)
    ctx = dict(homering=homering, w=w, h=h, ourteam=ourteam, theirteam=theirteam, ourfp=ourfp,
               theirfp=theirfp, ok=ok, d_our=d_our, d_their=d_their,
               bfs_cc=bfs_cc, choke=choke, winner=winner,
               rounds=len(turn_bufs), coreid=coreid, mapname=mapname)
    return ctx, ev


# ---------------------------------------------------------------------------

def aggregate(ctx, ev):
    ot, tt = ctx["ourteam"], ctx["theirteam"]
    ourfp, theirfp = ctx["ourfp"], ctx["theirfp"]
    d_our, d_their, choke = ctx["d_our"], ctx["d_their"], ctx["choke"]
    n = ctx["rounds"]
    out = {"map": ctx["mapname"], "rounds": n,
           "won": int(ctx["winner"] == ot) if ctx["winner"] is not None else -1}

    # -- forwardness of the spawn ring: unit vector core->enemy core --
    ocx = sum(t[0] for t in ourfp) / 4.0
    ocy = sum(t[1] for t in ourfp) / 4.0
    tcx = sum(t[0] for t in theirfp) / 4.0
    tcy = sum(t[1] for t in theirfp) / 4.0
    vx, vy = tcx - ocx, tcy - ocy
    vn = (vx * vx + vy * vy) ** 0.5 or 1.0

    def fwdness(p):
        return ((p[0] - ocx) * vx + (p[1] - ocy) * vy) / vn

    sp = ev["spawns"]
    out["spawn_n"] = len(sp)
    out["spawn1_rnd"] = sp[0][0] if sp else -1
    out["spawn4_rnd"] = sp[3][0] if len(sp) > 3 else -1
    first4 = sp[:4]
    out["spawn_fwd4"] = (round(sum(fwdness(p) for _r, p in first4) / len(first4), 3)
                         if first4 else 0)
    out["spawn_fwd_pos4"] = sum(1 for _r, p in first4 if fwdness(p) > 0)
    out["spawn_n30"] = sum(1 for r, _p in sp if r <= 30)

    # -- opening chain --
    def bydepth(lst, key):
        return [(r, p, key.get(p, -1)) for r, p in lst]

    h_ours = ev["harv"][ot]
    h_theirs = ev["harv"][tt]
    out["harv1_rnd"] = h_ours[0][0] if h_ours else -1
    out["harv1_dour"] = d_our.get(h_ours[0][1], -1) if h_ours else -1
    out["harv1_dtheir"] = d_their.get(h_ours[0][1], -1) if h_ours else -1
    out["harv_n30"] = sum(1 for r, _p in h_ours if r <= 30)
    out["harv_n60"] = sum(1 for r, _p in h_ours if r <= 60)
    out["harv_n"] = len(h_ours)
    out["opp_harv1_rnd"] = h_theirs[0][0] if h_theirs else -1
    out["opp_harv_n30"] = sum(1 for r, _p in h_theirs if r <= 30)
    out["opp_harv_n60"] = sum(1 for r, _p in h_theirs if r <= 60)
    c_ours = ev["conv"][ot]
    out["conv1_rnd"] = c_ours[0][0] if c_ours else -1
    out["conv_n30"] = sum(1 for r, _p in c_ours if r <= 30)
    out["conv_n60"] = sum(1 for r, _p in c_ours if r <= 60)
    out["opp_conv_n30"] = sum(1 for r, _p in ev["conv"][tt] if r <= 30)
    out["turret_n"] = len(ev["turret"][ot])
    out["opp_turret_n"] = len(ev["turret"][tt])
    tf = [r for r, _p in ev["turret"][tt]
          if d_their.get(_p, 99) is not None]
    del tf

    # -- economy from UpdatePlayers (ti banked, titaniumCollected) --
    pl = ev["players"]
    ai = 0 if ot == 0 else 2
    bi = 2 - ai
    for r in (30, 60, 100, 200):
        row = pl[r] if r < len(pl) else (pl[-1] if pl else (0, 0, 0, 0))
        out[f"ti_bank{r}"] = row[ai]
        out[f"ti_coll{r}"] = row[ai + 1]
        out[f"opp_coll{r}"] = row[bi + 1]
    out["ti_coll_end"] = pl[-1][ai + 1] if pl else -1
    out["opp_coll_end"] = pl[-1][bi + 1] if pl else -1

    # -- eco connectivity: harvesters WITH A ROUTE HOME --
    for r in ECO_SNAPS:
        nh, wired, ngood = ev["eco"].get(r, (0, 0, 0))
        out[f"harv_live{r}"] = nh
        out[f"harv_wired{r}"] = wired
        out[f"conv_good{r}"] = ngood
        er, cd, hd, ch = ev["ring"].get(r, (0, -1, -1, 0))
        out[f"enemy_ourring{r}"] = er
        out[f"conv_dmin{r}"] = cd
        out[f"harv_dmin{r}"] = hd
        out[f"conv_home{r}"] = ch

    # -- THE BELT-HEAD DECOMPOSITION.  Our belt "head" is the conveyor closest
    # to home, in BFS steps.  head1 = a conveyor ON the core ring (delivers);
    # head2 = one step short.  If head2 is reached and head1 never is, we ask
    # the only question that separates THEIR SEAL from OUR PLANNER: was any
    # ring socket EMPTY while the head sat there?
    hd = ev["headd"]
    hm2 = ev["home"]
    h2 = h1 = -1
    for r, v in enumerate(hd):
        if h2 < 0 and v <= 2:
            h2 = r
        if h1 < 0 and v <= 1:
            h1 = r
    out["head2_rnd"] = h2
    out["head1_rnd"] = h1
    out["head_dmin_ever"] = min(hd) if hd else -1
    if h2 >= 0 and h1 < 0:
        ha = ev["headadj"][h2:]
        nf = sum(1 for x in ha if x[0] > 0)
        ne = sum(1 for x in ha if x[0] == 0 and x[1] > 0)
        no = sum(1 for x in ha if x[0] == 0 and x[2] > 0)
        out["headadj_free_rnds"] = nf
        out["headadj_enemy_rnds"] = ne
        out["headadj_own_rnds"] = no
        out["headadj_free_share"] = round(nf / len(ha), 3) if ha else -1
        rp = [x for x in ha if x[0] == 0 and x[3] > 0]
        out["replan_rnds"] = len(rp)
        out["replan_share"] = round(len(rp) / len(ha), 3) if ha else -1
        out["replan_dist"] = (round(sum(x[4] for x in rp) / len(rp), 2)
                              if rp else -1)
        after = hm2[h2:]
        out["ringfree_rounds_after_head2"] = sum(
            1 for cd2 in after if any(c == "." for c in cd2))
        out["rounds_after_head2"] = len(after)
        out["ringfree_share_after_head2"] = (
            round(out["ringfree_rounds_after_head2"] / len(after), 3)
            if after else -1)
    else:
        for k in ("headadj_free_rnds", "headadj_enemy_rnds",
                  "headadj_own_rnds", "headadj_free_share",
                  "replan_rnds", "replan_share", "replan_dist"):
            out[k] = -1
        out["ringfree_rounds_after_head2"] = -1
        out["rounds_after_head2"] = -1
        out["ringfree_share_after_head2"] = -1

    # -- OUR OWN home ring: who holds the belt's landing sockets --
    hm = ev["home"]
    nring = len(ctx["homering"])
    out["homering_n"] = nring

    def hcount(r, pred):
        return sum(1 for c in hm[r] if pred(c)) if r < len(hm) else -1
    ENEMY = lambda c: c in ("Ex", "Eb")            # noqa: E731
    for r in ECO_SNAPS:
        out[f"eseal{r}"] = hcount(r, ENEMY)
        out[f"ebar{r}"] = hcount(r, lambda c: c == "Ex")
        out[f"oseal{r}"] = hcount(r, lambda c: c == "Ob")
        out[f"free{r}"] = hcount(r, lambda c: c == ".")
    first = -1
    for r, codes in enumerate(hm):
        if any(ENEMY(c) for c in codes):
            first = r
            break
    out["eseal_first"] = first
    firstb = -1
    for r, codes in enumerate(hm):
        if any(c == "Ex" for c in codes):
            firstb = r
            break
    out["ebar_first"] = firstb
    out["eseal_max"] = max((sum(1 for c in cd if ENEMY(c)) for cd in hm),
                           default=0)
    out["oseal_max"] = max((sum(1 for c in cd if c == "Ob") for cd in hm),
                           default=0)
    out["eseal_mean"] = (round(sum(sum(1 for c in cd if ENEMY(c))
                                   for cd in hm) / len(hm), 3) if hm else -1)

    # -- route: per-bot tracks --
    dep = arr36 = arr16 = None
    n_reach36 = n_reach16 = 0
    moves = 0
    reversals = 0
    stalls = 0
    choke_steps = 0
    best_route = None
    for bid, tr in ev["tracks"].items():
        pts = [p for _r, p in tr]
        rs = [r for r, _p in tr]
        moves += max(0, len(pts) - 1)
        for i in range(2, len(pts)):
            if pts[i] == pts[i - 2]:
                reversals += 1
        choke_steps += sum(1 for p in pts[1:] if p in choke)
        # departure: first round outside our apron
        d_i = a36 = a16 = None
        for (r, p) in tr:
            if d_i is None and _dsq(p, ourfp) > APRON_DSQ:
                d_i = r
            if a36 is None and _dsq(p, theirfp) <= APRON_DSQ:
                a36 = r
            if a16 is None and _dsq(p, theirfp) <= NEAR_DSQ:
                a16 = r
        if a36 is not None:
            n_reach36 += 1
        if a16 is not None:
            n_reach16 += 1
        if d_i is not None and (dep is None or d_i < dep):
            dep = d_i
        if a36 is not None and (arr36 is None or a36 < arr36):
            arr36 = a36
            k = [i for i, r in enumerate(rs) if r <= a36]
            best_route = (d_i, a36, len(k))
        if a16 is not None and (arr16 is None or a16 < arr16):
            arr16 = a16
        # stall: a bot alive >=40 rounds that never left our apron
        if d_i is None and rs and (rs[-1] - rs[0]) >= 40:
            stalls += 1
    out["bots_ours"] = len(ev["tracks"])
    out["bots_theirs"] = len(ev["bots"][tt])
    out["moves"] = moves
    out["rev_rate"] = round(reversals / moves, 4) if moves else -1
    out["choke_step_rate"] = round(choke_steps / moves, 4) if moves else -1
    out["dep_rnd"] = dep if dep is not None else -1
    out["arr36_rnd"] = arr36 if arr36 is not None else -1
    out["arr16_rnd"] = arr16 if arr16 is not None else -1
    out["n_reach36"] = n_reach36
    out["n_reach16"] = n_reach16
    out["reach36_share"] = (round(n_reach36 / len(ev["tracks"]), 3)
                            if ev["tracks"] else -1)
    out["stall_bots"] = stalls
    out["bfs_cc"] = ctx["bfs_cc"]
    if best_route and best_route[0] is not None:
        out["route_steps"] = best_route[2]
        out["route_detour"] = (round(best_route[2] / ctx["bfs_cc"], 3)
                               if ctx["bfs_cc"] > 0 else -1)
    else:
        out["route_steps"] = -1
        out["route_detour"] = -1

    # how the FIRST arrival at their near band got there: hops vs walks
    out["arr16_hops"] = out["arr16_walks"] = -1
    if arr16 is not None:
        for _bid, tr in ev["tracks"].items():
            hit = None
            for i, (r, p) in enumerate(tr):
                if _dsq(p, theirfp) <= NEAR_DSQ:
                    hit = (r, i)
                    break
            if hit and hit[0] == arr16:
                hops = walks = 0
                for i in range(1, hit[1] + 1):
                    st = max(abs(tr[i][1][0] - tr[i - 1][1][0]),
                             abs(tr[i][1][1] - tr[i - 1][1][1]))
                    if st > 1:
                        hops += 1
                    else:
                        walks += 1
                out["arr16_hops"], out["arr16_walks"] = hops, walks
                break

    # -- THE FERRY: launcher-thrown hops of our builder bots --
    ours_thr = [t for t in ev["throws"] if t[1] == ot]
    opp_thr = [t for t in ev["throws"] if t[1] == tt]
    out["throws_ours"] = len(ours_thr)
    out["throws_opp"] = len(opp_thr)
    out["throw1_rnd"] = ours_thr[0][0] if ours_thr else -1
    out["throws_ours30"] = sum(1 for t in ours_thr if t[0] <= 30)
    fwd = back = 0
    gain = 0
    for _r, _tm, frm, to, _s in ours_thr:
        a, b = d_their.get(frm), d_their.get(to)
        if a is None or b is None:
            continue
        gain += a - b
        if b < a:
            fwd += 1
        elif b > a:
            back += 1
    out["throw_fwd"] = fwd
    out["throw_back"] = back
    out["throw_gain"] = gain
    # launcher siting: how far along the corridor did the ferry chain reach?
    lau = [(r, p) for r, p in ev["turret"][ot]]
    lau_d = [d_their.get(p, -1) for _r, p in lau]
    lau_d = [d for d in lau_d if d >= 0]
    out["turret_dmin"] = min(lau_d) if lau_d else -1
    out["turret1_rnd"] = lau[0][0] if lau else -1
    out["turret_n30"] = sum(1 for r, _p in lau if r <= 30)
    out["turret_n_theirhalf"] = sum(
        1 for _r, p in lau
        if d_their.get(p, 10**6) < d_our.get(p, 10**6))

    # -- our buildings in THEIR basin (the siege footprint) --
    ob = ev["ourbuild_theirhalf"]
    out["fwdbuild_n"] = len(ob)
    out["fwdbuild1_rnd"] = ob[0][0] if ob else -1
    out["fwdbuild_n100"] = sum(1 for r, _k, _p in ob if r <= 100)

    # -- first contact --
    fd = ev["firstdmg"]
    if fd:
        rnd, vteam, delta, pos = fd
        out["fc_rnd"] = rnd
        out["fc_victim_ours"] = int(vteam == ot)
        out["fc_weapon"] = DELTA_WEAPON.get(delta, str(delta))
        if pos is not None and pos in d_our and pos in d_their:
            out["fc_basin"] = ("ours" if d_our[pos] < d_their[pos]
                               else "theirs" if d_their[pos] < d_our[pos]
                               else "mid")
            out["fc_dour"] = d_our[pos]
            out["fc_dtheir"] = d_their[pos]
        else:
            out["fc_basin"] = "?"
            out["fc_dour"] = out["fc_dtheir"] = -1
        # commit-vs-retreat: our bots inside their apron at fc and fc+20
        def presence(r):
            c = 0
            for _bid, tr in ev["tracks"].items():
                p = None
                for rr, pp in tr:
                    if rr <= r:
                        p = pp
                    else:
                        break
                if p is not None and tr[0][0] <= r and _dsq(p, theirfp) <= APRON_DSQ:
                    c += 1
            return c
        out["fc_pres0"] = presence(rnd)
        out["fc_pres20"] = presence(rnd + 20)
    else:
        for k in ("fc_rnd", "fc_victim_ours", "fc_dour", "fc_dtheir",
                  "fc_pres0", "fc_pres20"):
            out[k] = -1
        out["fc_weapon"] = out["fc_basin"] = "none"

    # ===================================================================
    # H1 / H2 -- the two named hypotheses, measured directly.
    # H1 RAIDERS DIE EARLY: death round + killer class of OUR bodies, split by
    #    where they died.  H2 RAIDERS NEVER ESTABLISH: at-ring presence share,
    #    first at-ring round, games with no establishment, stall signatures.
    # ===================================================================
    ar = ev["atring"]
    n = len(ar) or 1
    out["atring_first8"] = next((r for r, x in enumerate(ar) if x[0] > 0), -1)
    out["atring_first16"] = next((r for r, x in enumerate(ar) if x[1] > 0), -1)
    out["atring_rnds8"] = sum(1 for x in ar if x[0] > 0)
    out["atring_share8"] = round(sum(1 for x in ar if x[0] > 0) / n, 3)
    out["atring_share16"] = round(sum(1 for x in ar if x[1] > 0) / n, 3)
    out["atring_bodyrnds"] = sum(x[0] for x in ar)
    out["atring_peak"] = max((x[0] for x in ar), default=0)
    out["establish_first"] = next((r for r, x in enumerate(ar) if x[2] > 0), -1)
    out["establish_rnds"] = sum(1 for x in ar if x[2] > 0)
    out["establish_share"] = round(sum(1 for x in ar if x[2] > 0) / n, 3)
    out["establish_peak"] = max((x[2] for x in ar), default=0)
    # H1: raider lifetime -- rounds from a body's first at-ring round to death
    lifes = []
    for bid, tr in ev["tracks"].items():
        first_ring = next((r for r, pp in tr
                           if _dsq(pp, theirfp) <= APRON_DSQ), None)
        if first_ring is None:
            continue
        death = next((r for r, _t, _p, _k in ev["botdeath"] if _t == ot
                      and r >= first_ring), None)
        lifes.append((death - first_ring) if death is not None else -1)
    out["raider_n"] = len(lifes)
    fin = [x for x in lifes if x >= 0]
    out["raider_life_med"] = sorted(fin)[len(fin) // 2] if fin else -1

    # -- death ledger --
    ours_d = [(r, p) for r, t, p, _k in ev["botdeath"] if t == ot and p]
    theirs_d = [(r, p) for r, t, p, _k in ev["botdeath"] if t == tt and p]
    kc = Counter(k for _r, t, _p, k in ev["botdeath"] if t == ot)
    for nm in ("sentinel", "gunner", "builder_attack", "none"):
        out[f"kill_{nm}"] = kc.get(nm, 0)
    ap_d = sorted(r for r, p in ours_d if _dsq(p, theirfp) <= APRON_DSQ)
    out["apron_death_med"] = ap_d[len(ap_d) // 2] if ap_d else -1
    out["apron_death_first"] = ap_d[0] if ap_d else -1
    out["ourbot_deaths"] = len(ours_d)
    out["oppbot_deaths"] = len(theirs_d)
    zones = Counter()
    for _r, p in ours_d:
        if _dsq(p, ourfp) <= APRON_DSQ:
            zones["home"] += 1
        elif _dsq(p, theirfp) <= APRON_DSQ:
            zones["apron"] += 1
        else:
            zones["mid"] += 1
    for z in ("home", "mid", "apron"):
        out[f"death_{z}"] = zones[z]
    tilec = Counter(p for _r, p in ours_d)
    out["death_tiles"] = len(tilec)
    out["death_top1"] = tilec.most_common(1)[0][1] if tilec else 0
    out["death_conc"] = (round(out["death_top1"] / len(ours_d), 3)
                         if ours_d else -1)
    out["death_med_rnd"] = (sorted(r for r, _p in ours_d)[len(ours_d) // 2]
                            if ours_d else -1)
    out["death_choke"] = sum(1 for _r, p in ours_d if p in choke)
    rc = ev["recv"]
    for lbl, tm in (("our", ot), ("opp", tt)):
        for d, nm in ((-18, "sent"), (-7, "gun"), (-2, "peck")):
            out[f"{lbl}_recv_{nm}"] = rc[tm][d]

    # -- core clocks --
    for lbl, tm in (("our", ot), ("opp", tt)):
        hp = ev["corehp"][tm]
        first = -1
        for i in range(1, len(hp)):
            if hp[i] < hp[i - 1]:
                first = i
                break
        out[f"{lbl}core_firsthit"] = first
        out[f"{lbl}core_min"] = min(hp) if hp else -1
        out[f"{lbl}core_r150"] = hp[150] if len(hp) > 150 else (hp[-1] if hp else -1)
    return out


COLS = None


def row_for(replay, mapname, seat, **kw):
    ctx, ev = walk(replay, mapname, seat, **kw)
    return aggregate(ctx, ev)


# ---------------------------------------------------------------------------

def selftest(replay, mapname, seat):
    """BOTH VERDICTS on the load-bearing guards."""
    ok_all = True

    def chk(name, cond, detail):
        nonlocal ok_all
        ok_all &= bool(cond)
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}: {detail}")

    base = row_for(replay, mapname, seat)
    swap = row_for(replay, mapname, seat, anchor_swap=True)
    print("CONTROL 1 -- seat anchor is LOAD-BEARING (swap must change readings)")
    diff = sum(1 for k in base if base[k] != swap.get(k))
    chk("swapped seat changes >=15 columns", diff >= 15, f"{diff} columns differ")
    chk("won flips or differs", base["won"] != swap["won"],
        f"{base['won']} -> {swap['won']}")

    print("CONTROL 2 -- winner column agrees with the results tape")
    tape = {}
    for i, ln in enumerate(open(ROOT / "scratchpad" / "s51_vs_holder"
                                / "head_vs_holder.tsv", errors="ignore")
                           if False else []):
        del i, ln
    print("  (checked in --batch against head_vs_v165.tsv)")

    print("CONTROL 3 -- reversal rate SELECTS (must not be 0 or 1 everywhere)")
    chk("rev_rate strictly inside (0,1)", 0.0 < base["rev_rate"] < 1.0,
        f"rev_rate={base['rev_rate']} over {base['moves']} moves")

    print("CONTROL 4 -- economy channel is live and monotone")
    ctx, ev = walk(replay, mapname, seat)
    pl = ev["players"]
    coll = [p[1] for p in pl]
    chk("titaniumCollected present", len(pl) > 10, f"{len(pl)} player rows")
    chk("titaniumCollected non-decreasing",
        all(coll[i] <= coll[i + 1] for i in range(len(coll) - 1)),
        f"end={coll[-1] if coll else None}")
    chk("collected differs from banked",
        pl[-1][0] != pl[-1][1], f"bank={pl[-1][0]} coll={pl[-1][1]}")

    print("CONTROL 5 -- basins partition the board and are not degenerate")
    tot = len(ctx["ok"])
    mine = sum(1 for t in ctx["ok"]
               if ctx["d_our"].get(t, 10**6) < ctx["d_their"].get(t, 10**6))
    chk("our basin is 30-70% of passable", 0.3 < mine / tot < 0.7,
        f"{mine}/{tot}")

    print("CONTROL 6 -- damage alphabet is filtered, not passed through")
    alpha = Counter()
    for tm in (0, 1):
        alpha.update(ev["recv"][tm])
    chk("only the 3 weapon deltas survive", set(alpha) <= set(DMG),
        dict(alpha))
    print("SELFTEST", "PASS" if ok_all else "FAIL")
    return 0 if ok_all else 1


def batch(tapepath, repdir, out=None, limit=None):
    rows = []
    hdr = None
    src = []
    with open(tapepath) as f:
        head = f.readline().rstrip("\n").split("\t")
        for ln in f:
            src.append(dict(zip(head, ln.rstrip("\n").split("\t"))))
    if limit:
        src = src[:int(limit)]
    agree = disagree = 0
    fails = 0
    for i, r in enumerate(src):
        tag = r["tag"]
        p = Path(repdir) / f"{tag}.replay26"
        if not p.exists():
            fails += 1
            continue
        try:
            d = row_for(p, r["map"], r["seat"])
        except Exception as e:                       # noqa: BLE001
            print(f"PARSE-FAIL {tag}: {e}", file=sys.stderr)
            fails += 1
            continue
        d["tag"] = tag
        d["seed"] = r["seed"]
        d["seat"] = r["seat"]
        d["tape_ours_won"] = int(r["ours"] == "US") if "ours" in r else -1
        d["tape_turn"] = r["turn"]
        d["cond"] = r["cond"]
        # cross-check: replay winner vs results tape
        tapewon = 1 if r["ours"] == "US" else 0
        if d["won"] == tapewon:
            agree += 1
        else:
            disagree += 1
        if hdr is None:
            hdr = ["tag", "map", "seed", "seat"] + [
                k for k in d if k not in ("tag", "map", "seed", "seat")]
        rows.append(d)
        if (i + 1) % 100 == 0:
            print(f"  ... {i+1}/{len(src)}", file=sys.stderr)
    dest = open(out, "w") if out else sys.stdout
    print("\t".join(hdr), file=dest)
    for d in rows:
        print("\t".join(str(d.get(k, "")) for k in hdr), file=dest)
    if out:
        dest.close()
    print(f"GUARD winner-vs-tape: agree={agree} disagree={disagree} "
          f"parse_fail={fails}", file=sys.stderr)
    return 0


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return 0
    if a[0] == "--game":
        d = row_for(a[1], a[2], a[3])
        for k, v in d.items():
            print(f"{k:22s} {v}")
        return 0
    if a[0] == "--selftest":
        return selftest(a[1], a[2], a[3])
    if a[0] == "--batch":
        out = None
        limit = None
        if "--out" in a:
            out = a[a.index("--out") + 1]
        if "--limit" in a:
            limit = a[a.index("--limit") + 1]
        return batch(a[1], a[2], out, limit)
    print(__doc__)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
