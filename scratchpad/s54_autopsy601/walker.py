#!/usr/bin/env python3
"""CAGE-WALKER autopsy decoder (read-only).

Tracks, per game and per OUR builder:
  * birth/death round, heuristic ROLE (simulating _claim_role's lowest-stale-beat
    rule: sk_roles.py:158-183, SK_BEAT_STALE=3 sk_maps.py:137)
  * per-round position, action events (build/attack/heal), moves
  * lap geometry vs the ENEMY core's 12-tile Chebyshev lap (cage_lap, sk_roles.py:78)
  * the v601 PLANK-3 refusal predicate: forward lap tile holds an ENEMY BUILDING
    and an ENEMY BUILDER BOT is orthogonally adjacent to it
    (_clear_tile guard, bots/_v601skalman/sk_roles.py:1671-1672)

Wire tags per tools/replay_schema.md.  builderBuild(16) precedes its placeEntity(1);
build KIND is resolved at end of round (same buffering as skalman_fidelity.py).
"""
from __future__ import annotations
import sys, json
from pathlib import Path
ROOT = Path("/Users/junghard/Projects/Work/florent-code-game")
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import (fields, read_pos, parse_entity, scalars,
                           WIRE_LEN, WIRE_VARINT, packed_varints)

U64 = 1 << 64
ENV_WALL = 1
DMG = {"gunner": 7, "sentinel": 18}
CARD = ((0, -1), (1, 0), (0, 1), (-1, 0))
BEAT_STALE = 3
ROLE_NAME = {0: "HOME_KEEPER", 1: "CAGE_WALKER", 2: "ORE_DENIER", 3: "SIEGE_ENG"}


def signed(v):
    return v - U64 if v >= (1 << 63) else v


def footprint(p):
    return {(p[0] + dx, p[1] + dy) for dx in (0, 1) for dy in (0, 1)}


def dsq_fp(p, fp):
    return min((p[0] - a) ** 2 + (p[1] - b) ** 2 for a, b in fp)


def cage_lap(o):
    ox, oy = o
    return [(ox - 1, oy - 1), (ox, oy - 1), (ox + 1, oy - 1), (ox + 2, oy - 1),
            (ox + 2, oy), (ox + 2, oy + 1), (ox + 2, oy + 2),
            (ox + 1, oy + 2), (ox, oy + 2), (ox - 1, oy + 2),
            (ox - 1, oy + 1), (ox - 1, oy)]


LAP_SEAL_IDX = (1, 2, 4, 5, 7, 8, 10, 11)


class E:
    __slots__ = ("id", "team", "kind", "pos", "born")
    def __init__(s, i, t, k, p, b):
        s.id, s.team, s.kind, s.pos, s.born = i, t, k, p, b


def decode(path: Path, side: int):
    data = path.read_bytes()
    map_buf, turns, winner, wincond = None, [], None, ""
    for num, wire, val in fields(data):
        if num == 1 and wire == WIRE_LEN: map_buf = val
        elif num == 3 and wire == WIRE_LEN: turns.append(val)
        elif num == 4 and wire == WIRE_VARINT: winner = val
        elif num == 6 and wire == WIRE_LEN: wincond = val.decode("utf-8", "replace")
    w = h = 0; tiles = []; cores = []
    for num, wire, val in fields(map_buf):
        if num == 1: w = val
        elif num == 2: h = val
        elif num == 3:
            row = []
            for rn, rw, rv in fields(val):
                if rn == 1:
                    row.extend(packed_varints(rv) if rw == WIRE_LEN else [rv])
            tiles.append(row)
        elif num == 4:
            c = {"id": 0, "team": 0, "pos": (0, 0)}
            for cn, _cw, cv in fields(val):
                if cn == 1: c["id"] = cv
                elif cn == 2: c["team"] = cv
                elif cn == 3: c["pos"] = read_pos(cv)
            cores.append(c)

    def env(p):
        x, y = p
        if 0 <= y < len(tiles) and 0 <= x < len(tiles[y]):
            return tiles[y][x]
        return ENV_WALL

    def ibp(p):
        return 0 <= p[0] < w and 0 <= p[1] < h

    enemy = 1 - side
    corepos = {c["team"]: c["pos"] for c in cores}
    coreid = {c["team"]: c["id"] for c in cores}
    fp = {t: footprint(p) for t, p in corepos.items()}
    lap = cage_lap(corepos[enemy])
    lap_set = set(lap)
    seal_tiles = [lap[i] for i in LAP_SEAL_IDX]
    seal_open = [t for t in seal_tiles if ibp(t) and env(t) != ENV_WALL]
    seal_set = set(seal_open)   # == skalman_fidelity.ring_of() minus walls

    ents = {c["id"]: E(c["id"], c["team"], "core", c["pos"], 0) for c in cores}
    ever = {}
    bld_at, bot_at = {}, {}
    for c in cores:
        for t in fp[c["team"]]:
            bld_at[t] = c["id"]

    bots = {}     # our builder id -> record
    order = []
    role_owner = {r: None for r in range(4)}   # role -> (bid, death_round|None)
    deaths = []

    def claim_role(bid, rnd):
        """HEURISTIC replica of _claim_role (sk_roles.py:158-183)."""
        for r in range(4):
            o = role_owner[r]
            if o is None:
                role_owner[r] = [bid, None]; return r
            oid, dr = o
            if dr is not None and rnd - dr > BEAT_STALE:
                role_owner[r] = [bid, None]; return r
        return None   # all four fresh -> seat fallback n % 4 (rare)

    for rnd, tb in enumerate(turns):
        shadow_b, shadow_u = {}, {}
        hp_round, dmg_round = {}, {}
        removed = []
        pend_build = []          # (bid, tile)
        pend_attack = []         # (bid, tile)
        pend_heal = []
        births_this = []
        # snapshot the pre-round positions of our builders for lap accounting
        pre_pos = {b: bots[b]["pos"] for b in bots if bots[b]["alive"]}
        pre_bot_at = dict(bot_at)
        pre_bld_at = dict(bld_at)
        for _n, _w2, ubuf0 in fields(tb):
            for un, _uw, ub in fields(ubuf0):
                if un == 1:
                    for en, _ew, eb in fields(ub):
                        if en != 1: continue
                        e = parse_entity(eb, rnd)
                        if e is None: continue
                        if e.id in ents:
                            old = ents[e.id]
                            if old.pos != e.pos:
                                tbl = bot_at if old.kind == "builder_bot" else bld_at
                                if tbl.get(old.pos) == e.id: del tbl[old.pos]
                                tbl[e.pos] = e.id; old.pos = e.pos
                            continue
                        ne = E(e.id, e.team, e.kind, e.pos, rnd)
                        ents[e.id] = ne; ever[e.id] = ne
                        if e.kind == "builder_bot":
                            bot_at[e.pos] = e.id
                        else:
                            bld_at[e.pos] = e.id
                        births_this.append((e.id, e.team, e.kind, e.pos))
                elif un == 2:
                    eid = to = None
                    for mn, _mw, mv in fields(ub):
                        if mn == 1: eid = mv
                        elif mn == 2: to = read_pos(mv)
                    e = ents.get(eid)
                    if e is None or to is None: continue
                    if bot_at.get(e.pos) == eid: del bot_at[e.pos]
                    frm = e.pos
                    e.pos = to; bot_at[to] = eid
                    if eid in bots:
                        b = bots[eid]
                        b["pos"] = to
                        if abs(to[0]-frm[0]) + abs(to[1]-frm[1]) > 1:
                            b["thrown"] += 1
                        else:
                            b["moves"] += 1
                elif un == 3:
                    for _rn, _rw, rv in fields(ub):
                        e = ents.pop(rv, None)
                        if e is None: continue
                        if e.kind == "builder_bot":
                            if bot_at.get(e.pos) == rv: del bot_at[e.pos]
                            shadow_u[e.pos] = e
                        else:
                            if bld_at.get(e.pos) == rv: del bld_at[e.pos]
                            shadow_b[e.pos] = e
                        removed.append(e)
                elif un == 5:
                    d = scalars(ub)
                    eid, delta = d.get(1), signed(d.get(2, 0))
                    if delta < 0: hp_round[eid] = hp_round.get(eid, 0) - delta
                elif un == 12:
                    frm = to = None
                    for fn, _fw, fv in fields(ub):
                        if fn == 1: frm = read_pos(fv)
                        elif fn == 2: to = read_pos(fv)
                    if to is None: continue
                    sid = bld_at.get(frm)
                    sh = ents.get(sid) if sid is not None else shadow_b.get(frm)
                    skind = sh.kind if sh else "turret?"
                    steam = sh.team if sh else None
                    vid = bot_at.get(to)
                    v = ents.get(vid) if vid is not None else None
                    if v is None: v = shadow_u.get(to)
                    if v is None:
                        b2 = bld_at.get(to)
                        v = ents.get(b2) if b2 is not None else shadow_b.get(to)
                    if v is None: continue
                    dmg_round.setdefault(v.id, []).append(
                        (skind, sh.id if sh else None, steam, frm, DMG.get(skind, 0)))
                elif un == 13:
                    aid = tgt = None
                    for an, _aw, av in fields(ub):
                        if an == 1: aid = av
                        elif an == 2: tgt = read_pos(av)
                    if tgt is None: continue
                    a = ents.get(aid) or ever.get(aid)
                    b2 = bld_at.get(tgt)
                    v = ents.get(b2) if b2 is not None else shadow_b.get(tgt)
                    if v is not None:
                        dmg_round.setdefault(v.id, []).append(
                            ("peck", aid, a.team if a else None, a.pos if a else None, 2))
                    pend_attack.append((aid, tgt, v.kind if v else None,
                                        v.team if v else None))
                elif un == 15:
                    aid = tgt = None
                    for an, _aw, av in fields(ub):
                        if an == 1: aid = av
                        elif an == 2: tgt = read_pos(av)
                    pend_heal.append((aid, tgt))
                elif un == 16:
                    aid = tgt = None
                    for an, _aw, av in fields(ub):
                        if an == 1: aid = av
                        elif an == 2: tgt = read_pos(av)
                    pend_build.append((aid, tgt))
        # --- register OUR new builders, claim roles in birth order
        for (eid, team, kind, pos) in births_this:
            if team != side or kind != "builder_bot":
                continue
            r = claim_role(eid, rnd)
            bots[eid] = {"id": eid, "born": rnd, "died": None, "pos": pos,
                         "role": r, "spawn": pos, "alive": True,
                         "moves": 0, "thrown": 0, "builds": 0, "pecks": 0,
                         "heals": 0, "build_kinds": {}, "peck_kinds": {},
                         "ring_barriers": 0, "lap_rounds": 0,
                         "lap_action_rounds": 0, "lap_idle_rounds": 0,
                         "adj_seal_rounds": 0, "first_lap": None,
                         "min_dsq_enemy": None, "refuse_rounds": 0,
                         "fwd_occupied_rounds": 0, "track": []}
            order.append(eid)
        # --- resolve builds to kinds
        for (aid, tgt) in pend_build:
            k = None
            bid2 = bld_at.get(tgt)
            if bid2 is not None and bid2 in ents:
                k = ents[bid2].kind
            if aid in bots:
                b = bots[aid]; b["builds"] += 1
                b["build_kinds"][k] = b["build_kinds"].get(k, 0) + 1
                if k == "barrier" and tgt in seal_set:
                    b["ring_barriers"] += 1
        for (aid, tgt, vk, vt) in pend_attack:
            if aid in bots:
                b = bots[aid]; b["pecks"] += 1
                key = f"{vk}"
                b["peck_kinds"][key] = b["peck_kinds"].get(key, 0) + 1
        for (aid, tgt) in pend_heal:
            if aid in bots:
                bots[aid]["heals"] += 1
        # --- lap accounting on the PRE-round position (where the bot decided)
        acted = {}
        for (aid, _t) in pend_build: acted[aid] = True
        for (aid, _t, _k, _v) in pend_attack: acted[aid] = True
        for (aid, _t) in pend_heal: acted[aid] = True
        moved = set()
        for bid, b in bots.items():
            if not b["alive"]: continue
            pp = pre_pos.get(bid, b["pos"])
            b["track"].append((rnd, pp))
            d = dsq_fp(pp, fp[enemy])
            if b["min_dsq_enemy"] is None or d < b["min_dsq_enemy"]:
                b["min_dsq_enemy"] = d
            on_lap = pp in lap_set
            if on_lap:
                b["lap_rounds"] += 1
                if b["first_lap"] is None: b["first_lap"] = rnd
                if acted.get(bid): b["lap_action_rounds"] += 1
                else: b["lap_idle_rounds"] += 1
                # PLANK-3 refusal predicate on the FORWARD lap tile
                here = lap.index(pp)
                fwd = lap[(here + 1) % 12]
                occ = pre_bld_at.get(fwd)
                if occ is not None and occ in ents and ents[occ].team == enemy:
                    b["fwd_occupied_rounds"] += 1
                    for dx, dy in CARD:
                        r2 = (fwd[0] + dx, fwd[1] + dy)
                        u = pre_bot_at.get(r2)
                        if u is not None and u in ents and ents[u].team == enemy:
                            b["refuse_rounds"] += 1
                            break
            else:
                for t in seal_open:
                    if abs(pp[0]-t[0]) + abs(pp[1]-t[1]) == 1:
                        b["adj_seal_rounds"] += 1
                        break
        # --- deaths
        for e in removed:
            srcs = dmg_round.get(e.id, [])
            last = srcs[-1] if srcs else None
            att = sum(s[4] for s in srcs)
            hpd = hp_round.get(e.id, 0)
            rec = {"rnd": rnd, "id": e.id, "team": e.team, "kind": e.kind,
                   "pos": e.pos, "born": e.born, "life": rnd - e.born,
                   "killer_kind": last[0] if last else None,
                   "killer_team": last[2] if last else None,
                   "killer_pos": last[3] if last else None,
                   "attributed": att, "hp_delta_round": hpd,
                   "nodamage": not srcs}
            deaths.append(rec)
            if e.id in bots:
                b = bots[e.id]; b["alive"] = False; b["died"] = rnd
                b["death"] = rec
                for r in range(4):
                    if role_owner[r] and role_owner[r][0] == e.id:
                        role_owner[r][1] = rnd

    import os
    if not os.environ.get("KEEP_TRACK"):
        for b in bots.values():
            b.pop("track", None)
    return dict(file=path.name, side=side, rounds=len(turns), winner=winner,
                cond=wincond, w=w, h=h, corepos=corepos,
                lap=lap, seal_open=seal_open, seal_set=sorted(seal_set), bots=bots, order=order,
                deaths=deaths)


if __name__ == "__main__":
    r = decode(Path(sys.argv[1]), int(sys.argv[2]))
    print(json.dumps({k: r[k] for k in ("file", "rounds", "winner", "cond")}))
    for bid in r["order"]:
        b = r["bots"][bid]
        print(bid, ROLE_NAME.get(b["role"], "?"), "born", b["born"], "died", b["died"],
              "mv", b["moves"], "bld", b["builds"], "peck", b["pecks"],
              "ringbar", b["ring_barriers"], "lap", b["lap_rounds"],
              "lapidle", b["lap_idle_rounds"], "refuse", b["refuse_rounds"],
              "mindsq", b["min_dsq_enemy"], b["build_kinds"], b["peck_kinds"])
