#!/usr/bin/env python3
"""tape30 death-cause autopsy decoder (read-only).

Attribution method replicated from scratchpad/s54_doorwave_decode/doorwave_decode.py
(per-round shadow index for removeEntity-before-killing-blow) plus the
tools/replay_schema.md damage-target law:
  * FireTurret {from,to}  -> victim = UNIT on `to` if any, else BUILDING on `to`
                             dmg 7 (gunner) / 18 (sentinel), shooter looked up on `from`
  * BuilderAttack {id,tgt}-> victim = BUILDING on `tgt` (never the unit), dmg 2
Self-check: for every death, attributed damage in the death round must equal the
summed NEGATIVE UpdateHp deltas on that id in that round.
"""
from __future__ import annotations
import sys, json
from pathlib import Path

ROOT = Path("/Users/junghard/Projects/Work/florent-code-game")
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import (fields, read_pos, parse_entity, scalars,
                           WIRE_LEN, WIRE_VARINT)

U64 = 1 << 64
DMG = {"gunner": 7, "sentinel": 18}
TURRETS = ("gunner", "sentinel", "launcher")
BELT = ("conveyor", "splitter", "harvester")
DIRDELTA = {0: (0, 0), 1: (0, -1), 2: (1, -1), 3: (1, 0), 4: (1, 1),
            5: (0, 1), 6: (-1, 1), 7: (-1, 0), 8: (-1, -1)}


def signed(v):
    return v - U64 if v >= (1 << 63) else v


def dsq_foot(pos, corenw):
    ox, oy = corenw
    dx = pos[0] - ox
    dx = -dx if dx < 0 else (dx - 1 if dx > 1 else 0)
    dy = pos[1] - oy
    dy = -dy if dy < 0 else (dy - 1 if dy > 1 else 0)
    return dx * dx + dy * dy


class E:
    __slots__ = ("id", "team", "kind", "pos", "born", "hp", "maxhp", "dir")

    def __init__(s, i, t, k, p, b, hp, mx, d):
        s.id, s.team, s.kind, s.pos, s.born = i, t, k, p, b
        s.hp, s.maxhp, s.dir = hp, mx, d


def reach_tiles(pos, kind, direction, w, h, any_facing=False):
    """Tiles a turret covers. gunner r2<=13 along facing ray (obstacles ignored ->
    UPPER bound); sentinel r2<=32 along facing ray (truly ignores obstacles)."""
    if kind == "gunner":
        rmax = 13
    elif kind == "sentinel":
        rmax = 32
    else:
        return set()
    dirs = list(DIRDELTA.values())[1:] if any_facing else \
        ([DIRDELTA.get(direction, (0, 0))] if direction else [])
    out = set()
    for dx, dy in dirs:
        if dx == 0 and dy == 0:
            continue
        k = 1
        while True:
            x, y = pos[0] + dx * k, pos[1] + dy * k
            if (x - pos[0]) ** 2 + (y - pos[1]) ** 2 > rmax:
                break
            if 0 <= x < w and 0 <= y < h:
                out.add((x, y))
            k += 1
    return out


def decode(path: Path, our=0):
    data = path.read_bytes()
    map_buf, turns, winner, wincond = None, [], None, ""
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turns.append(value)
        elif num == 4 and wire == WIRE_VARINT:
            winner = value
        elif num == 6 and wire == WIRE_LEN:
            wincond = value.decode("utf-8", "replace")
    cores, w, h = [], 0, 0
    for num, _w2, value in fields(map_buf):
        if num == 1:
            w = value
        elif num == 2:
            h = value
        elif num == 4:
            c = {"id": 0, "team": 0, "pos": (0, 0)}
            for cn, _cw, cv in fields(value):
                if cn == 1:
                    c["id"] = cv
                elif cn == 2:
                    c["team"] = cv
                elif cn == 3:
                    c["pos"] = read_pos(cv)
            cores.append(c)
    corepos = {c["team"]: c["pos"] for c in cores}
    coreid = {c["team"]: c["id"] for c in cores}
    them = 1 - our
    foot = {t: {(p[0] + dx, p[1] + dy) for dx in (0, 1) for dy in (0, 1)}
            for t, p in corepos.items()}

    ents = {c["id"]: E(c["id"], c["team"], "core", c["pos"], 0, 500, 500, None)
            for c in cores}
    ever = {}
    bld_at, bot_at = {}, {}
    for c in cores:
        for t in foot[c["team"]]:
            bld_at[t] = c["id"]

    deaths = []          # dicts
    births = []
    core_dead = {0: None, 1: None}
    core_hp = {0: 500, 1: 500}
    core_first_dmg = {0: None, 1: None}
    # resource-chain tracking (harvester wiring)
    res_origin = {}      # resource id -> harvester entity id
    harv_delivered = {}  # harvester id -> first delivery round
    harv_emitted = {}    # harvester id -> n stacks emitted
    # timeline
    tl = {"enemy_in_our_half": None, "first_shot_our_harv": None,
          "first_shot_our_builder": None, "first_fwd_turret": None,
          "first_core_dmg": None}
    throws = []          # (rnd, bot_team, bot_id, from, to)
    fwd_turrets = {}     # enemy turret id -> dict
    our_turrets = {}     # our turret id -> dict
    damage_log = []      # every resolved damage event
    mismatch = 0
    checked = 0

    def ent_kind_at(tile, shadow):
        b = bld_at.get(tile)
        if b is not None and b in ents:
            return ents[b]
        if tile in shadow:
            return shadow[tile]
        return None

    for rnd, tb in enumerate(turns):
        shadow_b = {}       # tile -> removed building Ent (this round)
        shadow_u = {}       # tile -> removed unit Ent (this round)
        hp_round = {}       # id -> summed negative delta this round
        dmg_round = {}      # victim id -> list of (src_kind, src_id, src_team, src_pos)
        removed_this_round = []
        for _n, _w3, ub0 in fields(tb):
            for un, _uw, ub in fields(ub0):
                if un == 1:                                   # placeEntity
                    for en, _ew, eb in fields(ub):
                        if en != 1:
                            continue
                        e = parse_entity(eb, rnd)
                        if e is None:
                            continue
                        if e.id in ents:                       # re-emit (rotate/etc)
                            old = ents[e.id]
                            if e.direction is not None:
                                old.dir = e.direction
                            if old.pos != e.pos:
                                tbl = bot_at if old.kind == "builder_bot" else bld_at
                                if tbl.get(old.pos) == e.id:
                                    del tbl[old.pos]
                                tbl[e.pos] = e.id
                                old.pos = e.pos
                            continue
                        ne = E(e.id, e.team, e.kind, e.pos, rnd, e.hp, e.max_hp,
                               e.direction)
                        ents[e.id] = ne
                        ever[e.id] = ne
                        births.append((rnd, e.team, e.kind, e.id, e.pos))
                        if e.kind == "builder_bot":
                            bot_at[e.pos] = e.id
                        else:
                            bld_at[e.pos] = e.id
                        if e.kind in TURRETS:
                            d_our = dsq_foot(e.pos, corepos[our])
                            d_them = dsq_foot(e.pos, corepos[them])
                            rec = {"id": e.id, "kind": e.kind, "pos": e.pos,
                                   "born": rnd, "died": None, "killer": None,
                                   "dsq_our": d_our, "dsq_them": d_them}
                            if e.team == them:
                                if d_our < d_them:
                                    rec["fwd"] = True
                                    fwd_turrets[e.id] = rec
                                    if tl["first_fwd_turret"] is None:
                                        tl["first_fwd_turret"] = rnd
                            else:
                                our_turrets[e.id] = rec
                elif un == 2:                                 # moveBuilderBot
                    eid = to = None
                    for mn, _mw, mv in fields(ub):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    e = ents.get(eid)
                    if e is None or to is None:
                        continue
                    if bot_at.get(e.pos) == eid:
                        del bot_at[e.pos]
                    frm_p = e.pos
                    if abs(to[0] - frm_p[0]) + abs(to[1] - frm_p[1]) > 1:
                        throws.append((rnd, e.team, eid, frm_p, to))
                    e.pos = to
                    bot_at[to] = eid
                    if e.team == them and tl["enemy_in_our_half"] is None:
                        if dsq_foot(to, corepos[our]) < dsq_foot(to, corepos[them]):
                            tl["enemy_in_our_half"] = rnd
                elif un == 3:                                 # removeEntity
                    for _rn, _rw, rv in fields(ub):
                        e = ents.pop(rv, None)
                        if e is None:
                            continue
                        if e.kind == "builder_bot":
                            if bot_at.get(e.pos) == rv:
                                del bot_at[e.pos]
                            shadow_u[e.pos] = e
                        else:
                            if bld_at.get(e.pos) == rv:
                                del bld_at[e.pos]
                            shadow_b[e.pos] = e
                        removed_this_round.append(e)
                        if rv in fwd_turrets and fwd_turrets[rv]["died"] is None:
                            fwd_turrets[rv]["died"] = rnd
                        if rv in our_turrets and our_turrets[rv]["died"] is None:
                            our_turrets[rv]["died"] = rnd
                        for t in (0, 1):
                            if rv == coreid[t] and core_dead[t] is None:
                                core_dead[t] = rnd
                elif un == 4:                                 # distributeResources
                    for _mn, _mw, mv in fields(ub):
                        frm = to = rid = None
                        for fn, _fw, fv in fields(mv):
                            if fn == 1:
                                frm = read_pos(fv)
                            elif fn == 2:
                                to = read_pos(fv)
                            elif fn == 3:
                                rid = fv
                        if frm is None or to is None:
                            continue
                        src = bld_at.get(frm)
                        if src is not None and src in ents and \
                                ents[src].kind == "harvester" and ents[src].team == our:
                            if rid is not None:
                                res_origin[rid] = src
                            harv_emitted[src] = harv_emitted.get(src, 0) + 1
                        if to in foot[our] and rid is not None:
                            o = res_origin.get(rid)
                            if o is not None and o not in harv_delivered:
                                harv_delivered[o] = rnd
                elif un == 5:                                 # updateHp
                    d = scalars(ub)
                    eid, delta = d.get(1), signed(d.get(2, 0))
                    e = ents.get(eid)
                    if e is not None:
                        e.hp += delta
                    if delta < 0:
                        hp_round[eid] = hp_round.get(eid, 0) - delta
                    for t in (0, 1):
                        if eid == coreid[t]:
                            core_hp[t] += delta
                            if delta < 0 and core_first_dmg[t] is None:
                                core_first_dmg[t] = rnd
                elif un == 12:                                # fireTurret
                    frm = to = None
                    for fn, _fw, fv in fields(ub):
                        if fn == 1:
                            frm = read_pos(fv)
                        elif fn == 2:
                            to = read_pos(fv)
                    if to is None:
                        continue
                    sid = bld_at.get(frm)
                    sh = ents.get(sid) if sid is not None else None
                    if sh is None and frm in shadow_b:
                        sh = shadow_b[frm]
                    skind = sh.kind if sh is not None else "turret?"
                    steam = sh.team if sh is not None else None
                    # victim: unit first, else building
                    vid = bot_at.get(to)
                    v = ents.get(vid) if vid is not None else None
                    if v is None and to in shadow_u:
                        v = shadow_u[to]
                    if v is None:
                        v = ent_kind_at(to, shadow_b)
                    if v is None:
                        continue
                    dmg_round.setdefault(v.id, []).append(
                        (skind, sh.id if sh else None, steam,
                         frm, DMG.get(skind, 0)))
                    damage_log.append((rnd, skind, steam, frm, v.id, v.kind,
                                       v.team, to))
                    if steam == them and v.team == our:
                        if v.kind == "harvester" and tl["first_shot_our_harv"] is None:
                            tl["first_shot_our_harv"] = rnd
                        if v.kind == "builder_bot" and tl["first_shot_our_builder"] is None:
                            tl["first_shot_our_builder"] = rnd
                elif un == 13:                                # builderAttack
                    aid = tgt = None
                    for an, _aw, av in fields(ub):
                        if an == 1:
                            aid = av
                        elif an == 2:
                            tgt = read_pos(av)
                    if tgt is None:
                        continue
                    a = ents.get(aid)
                    if a is None and aid in ever:
                        a = ever[aid]
                    v = ent_kind_at(tgt, shadow_b)
                    if v is None:
                        continue
                    dmg_round.setdefault(v.id, []).append(
                        ("peck", aid, a.team if a else None,
                         a.pos if a else None, 2))
                    damage_log.append((rnd, "peck", a.team if a else None,
                                       a.pos if a else None, v.id, v.kind,
                                       v.team, tgt))
        # --- end of round: resolve deaths
        live_our_turrets = [(x.pos, x.kind, x.dir) for x in ents.values()
                            if x.team == our and x.kind in ("gunner", "sentinel")]
        for e in removed_this_round:
            srcs = dmg_round.get(e.id, [])
            attributed = sum(s[4] for s in srcs)
            hpd = hp_round.get(e.id, 0)
            if srcs:
                checked += 1
                if attributed != hpd:
                    mismatch += 1
            last = srcs[-1] if srcs else None
            deaths.append({
                "rnd": rnd, "id": e.id, "team": e.team, "kind": e.kind,
                "pos": e.pos, "born": e.born, "life": rnd - e.born,
                "killer_kind": last[0] if last else None,
                "killer_team": last[2] if last else None,
                "killer_pos": last[3] if last else None,
                "n_src": len(srcs),
                "attributed": attributed, "hp_delta_round": hpd,
                "hp_at_death": e.hp,
                "srcs": srcs,
                "our_turrets_live": list(live_our_turrets),
            })
            if e.id in fwd_turrets and fwd_turrets[e.id]["killer"] is None:
                fwd_turrets[e.id]["killer"] = last[0] if last else None
                fwd_turrets[e.id]["killer_team"] = last[2] if last else None
            if e.id in our_turrets and our_turrets[e.id]["killer"] is None:
                our_turrets[e.id]["killer"] = last[0] if last else None
                our_turrets[e.id]["killer_team"] = last[2] if last else None
        # --- per-round coverage of live enemy forward turrets by OUR turrets
        if live_our_turrets:
            cov_ray, cov_rad = set(), set()
            for (tp, tk, td) in live_our_turrets:
                cov_ray |= reach_tiles(tp, tk, td, w, h, False)
                cov_rad |= reach_tiles(tp, tk, td, w, h, True)
            for tid, rec in fwd_turrets.items():
                if rec["died"] is not None or tid not in ents:
                    continue
                if rec["pos"] in cov_ray:
                    rec["cov_ray_ever"] = True
                if rec["pos"] in cov_rad:
                    rec["cov_rad_ever"] = True
        # also: adjacency of any of our builders to a live fwd turret (peckable)
        our_bots = [x.pos for x in ents.values()
                    if x.team == our and x.kind == "builder_bot"]
        if our_bots:
            for tid, rec in fwd_turrets.items():
                if rec["died"] is not None or tid not in ents:
                    continue
                tx, ty = rec["pos"]
                for bp in our_bots:
                    if abs(bp[0] - tx) + abs(bp[1] - ty) == 1:
                        rec["adj_ever"] = True
                        break

    return dict(file=path.name, w=w, h=h, rounds=len(turns), winner=winner,
                cond=wincond, our=our, corepos=corepos, coreid=coreid,
                deaths=deaths, births=births, ents=ents, ever=ever,
                core_dead=core_dead, core_first_dmg=core_first_dmg,
                harv_delivered=harv_delivered, harv_emitted=harv_emitted,
                tl=tl, fwd_turrets=fwd_turrets, our_turrets=our_turrets,
                damage_log=damage_log, mismatch=mismatch, checked=checked,
                throws=throws)


if __name__ == "__main__":
    r = decode(Path(sys.argv[1]))
    print(json.dumps({k: r[k] for k in ("file", "rounds", "winner", "cond",
                                        "mismatch", "checked", "tl",
                                        "core_dead")}, default=str))
    print("deaths", len(r["deaths"]))
