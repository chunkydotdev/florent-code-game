#!/usr/bin/env python3
"""DOORWAVE decode: registered readout columns per PREREG-LEG-DOORWAVE-2026-08-21.

Engine-side only (positions, BUILD/DEATH events, HP deltas, updatePlayers).
No stdout is read (platform strips it).
"""
from __future__ import annotations
import sys, json, gzip, math, statistics
from pathlib import Path

ROOT = Path("/Users/junghard/Projects/Work/florent-code-game")
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import (fields, read_pos, parse_entity, scalars,
                           WIRE_LEN, WIRE_VARINT)
try:
    from map_admits import map_facts
except Exception:
    map_facts = None

ARCHIVE = ROOT / "replay_archive"
DOOR_TYPES = {"gunner", "sentinel", "launcher"}
FS_DOOR_DSQ = 40
U64 = 1 << 64


def signed(v: int) -> int:
    return v - U64 if v >= (1 << 63) else v


def dsq_core(pos, core):
    """min squared distance to the 2x2 core footprint (eco.dsq_core, exact)."""
    ox, oy = core
    dx = pos[0] - ox
    dx = -dx if dx < 0 else (dx - 1 if dx > 1 else 0)
    dy = pos[1] - oy
    dy = -dy if dy < 0 else (dy - 1 if dy > 1 else 0)
    return dx * dx + dy * dy


class Ent:
    __slots__ = ("id", "team", "pos", "kind", "born", "hp", "max_hp")

    def __init__(self, eid, team, pos, kind, born, hp, max_hp):
        self.id, self.team, self.pos, self.kind = eid, team, pos, kind
        self.born, self.hp, self.max_hp = born, hp, max_hp


def decode(path: Path, our_team: int) -> dict:
    data = path.read_bytes()
    map_buf, turn_bufs, winner, wincond = None, [], None, ""
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
        elif num == 4 and wire == WIRE_VARINT:
            winner = value
        elif num == 6 and wire == WIRE_LEN:
            wincond = value.decode("utf-8", "replace")
    cores, w, h = [], 0, 0
    for num, _wire, value in fields(map_buf):
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
    them = 1 - our_team
    ours_core, their_core = corepos[our_team], corepos[them]

    ents = {c["id"]: Ent(c["id"], c["team"], c["pos"], "core", 0, 500, 500)
            for c in cores}
    ever = {c["id"]: (c["team"], "core", c["pos"], 0) for c in cores}
    bld_at = {}              # tile -> building id (non-bot, non-core)
    bot_at = {}              # tile -> builder bot id
    core_hp = {0: 500, 1: 500}
    core_dead_rnd = {0: None, 1: None}
    ti = {0: 0, 1: 0}

    pecks = []               # (rnd, attacker, target_id, kind, pos)
    peck_target_hp = {}      # target id -> [(rnd, delta)]
    exposure = []            # (rnd, ti_ours, n_adjacent_pairs)
    enemy_turrets = {}       # id -> dict(kind, pos, born, died, dsq_ours)
    our_core_hp_at = {}      # rnd -> hp end of round
    all_builder_attacks = {0: 0, 1: 0}
    near = []                # our attacks on ANY enemy door-type turret (rnd, kind, dsq_ours)
    atk_on_enemy_building = 0   # our builder attacks on any enemy building

    for rnd, turn_buf in enumerate(turn_bufs):
        # ⛔ removeEntity can be emitted BEFORE the killing blow's event in the
        # same round (replay_schema: events may follow their victim's removal).
        # Resolving a target against the LIVE tile index alone drops exactly the
        # killing peck — measured on the positive control: 56 of 60. This
        # per-round shadow index restores them without resurrecting stale tiles.
        gone_this_round = {}
        for _n, _w2, ubuf0 in fields(turn_buf):
            for unum, _uw, ubuf in fields(ubuf0):
                if unum == 1:                                    # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        if e.id in ents:                          # rotation re-emit
                            old = ents[e.id]
                            if old.pos != e.pos:
                                if old.kind == "builder_bot":
                                    if bot_at.get(old.pos) == e.id:
                                        del bot_at[old.pos]
                                    bot_at[e.pos] = e.id
                                else:
                                    if bld_at.get(old.pos) == e.id:
                                        del bld_at[old.pos]
                                    bld_at[e.pos] = e.id
                                old.pos = e.pos
                            continue
                        ne = Ent(e.id, e.team, e.pos, e.kind, rnd, e.hp, e.max_hp)
                        ents[e.id] = ne
                        ever[e.id] = (e.team, e.kind, e.pos, rnd)
                        if e.kind == "builder_bot":
                            bot_at[e.pos] = e.id
                        elif e.kind != "core":
                            bld_at[e.pos] = e.id
                        if e.team == them and e.kind in DOOR_TYPES:
                            enemy_turrets[e.id] = {
                                "kind": e.kind, "pos": e.pos, "born": rnd,
                                "died": None,
                                "dsq_ours": dsq_core(e.pos, ours_core),
                                "dsq_theirs": dsq_core(e.pos, their_core)}
                elif unum == 2:                                  # moveBuilderBot
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    e = ents.get(eid)
                    if e is None or to is None:
                        continue
                    if bot_at.get(e.pos) == eid:
                        del bot_at[e.pos]
                    e.pos = to
                    bot_at[to] = eid
                elif unum == 3:                                  # removeEntity
                    for _rn, _rw, rv in fields(ubuf):
                        e = ents.pop(rv, None)
                        if e is None:
                            continue
                        if e.kind == "builder_bot":
                            if bot_at.get(e.pos) == rv:
                                del bot_at[e.pos]
                        else:
                            if bld_at.get(e.pos) == rv:
                                del bld_at[e.pos]
                            gone_this_round[e.pos] = (rv, e.team, e.kind)
                        if rv in enemy_turrets and enemy_turrets[rv]["died"] is None:
                            enemy_turrets[rv]["died"] = rnd
                        for t in (0, 1):
                            if rv == coreid[t] and core_dead_rnd[t] is None:
                                core_dead_rnd[t] = rnd
                elif unum == 5:                                  # updateHp
                    d = scalars(ubuf)
                    eid, delta = d.get(1), signed(d.get(2, 0))
                    e = ents.get(eid)
                    if e is not None:
                        e.hp += delta
                    for t in (0, 1):
                        if eid == coreid[t]:
                            core_hp[t] += delta
                            if core_hp[t] <= 0 and core_dead_rnd[t] is None:
                                core_dead_rnd[t] = rnd
                    if eid in enemy_turrets:
                        peck_target_hp.setdefault(eid, []).append((rnd, delta))
                elif unum == 6:                                  # updatePlayers
                    for pn, _pw, pv in fields(ubuf):
                        if pn != 1:
                            continue
                        for tn, _tw, tv in fields(pv):
                            if tn in (1, 2):
                                sc = scalars(tv)
                                ti[tn - 1] = sc.get(1, 0)
                elif unum == 13:                                 # builderAttack
                    aid = tgt = None
                    for an, _aw, av in fields(ubuf):
                        if an == 1:
                            aid = av
                        elif an == 2:
                            tgt = read_pos(av)
                    if tgt is None:
                        continue
                    a = ents.get(aid)
                    if a is not None:
                        all_builder_attacks[a.team] += 1
                    if a is None or a.team != our_team or a.kind != "builder_bot":
                        continue
                    vid = bld_at.get(tgt)
                    v = ents.get(vid) if vid is not None else None
                    if v is not None:
                        vteam, vkind = v.team, v.kind
                    elif tgt in gone_this_round:
                        vid, vteam, vkind = gone_this_round[tgt]
                    else:
                        continue
                    if vteam == our_team:
                        continue
                    atk_on_enemy_building += 1
                    if vkind in DOOR_TYPES:
                        near.append((rnd, vkind, dsq_core(tgt, ours_core)))
                    if vkind not in DOOR_TYPES:
                        continue
                    if dsq_core(tgt, ours_core) > FS_DOOR_DSQ:
                        continue
                    pecks.append((rnd, aid, vid, vkind, tgt))
        # --- end-of-round state: exposure + our core hp trajectory
        our_core_hp_at[rnd] = core_hp[our_team]
        adj = 0
        live_bots = [ents[i] for i in list(bot_at.values())
                     if i in ents and ents[i].team == our_team]
        if live_bots:
            for tid, t in enemy_turrets.items():
                if t["died"] is not None or tid not in ents:
                    continue
                if t["dsq_ours"] > FS_DOOR_DSQ:
                    continue
                tx, ty = t["pos"]
                for b in live_bots:
                    if abs(b.pos[0] - tx) + abs(b.pos[1] - ty) == 1:
                        adj += 1
        if adj:
            exposure.append((rnd, ti[our_team], adj))

    turns = len(turn_bufs)
    our_won = (winner == our_team) if winner is not None else None
    mapname = ""
    if map_facts is not None:
        try:
            mf = map_facts(path)
            if mf:
                mapname = mf.get("name", "") or f"{mf['w']}x{mf['h']}"
        except Exception:
            mapname = ""
    return {
        "file": path.name, "turns": turns, "winner": winner,
        "our_won": our_won, "cond": wincond, "map": mapname,
        "w": w, "h": h, "our_team": our_team,
        "our_core": ours_core, "their_core": their_core,
        "pecks": pecks, "peck_target_hp": peck_target_hp,
        "exposure": exposure, "enemy_turrets": enemy_turrets,
        "our_core_dead": core_dead_rnd[our_team],
        "their_core_dead": core_dead_rnd[them],
        "our_core_hp_at": our_core_hp_at,
        "builder_attacks": all_builder_attacks,
        "near": near, "atk_on_enemy_building": atk_on_enemy_building,
    }


if __name__ == "__main__":
    # standalone: decode(path, our_team) for a positive control
    p = Path(sys.argv[1])
    t = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    r = decode(p, t)
    print(json.dumps({k: v for k, v in r.items()
                      if k in ("file", "turns", "winner", "cond", "map",
                               "our_core", "builder_attacks")}))
    print("pecks", len(r["pecks"]), r["pecks"][:5])
    print("exposure rounds", len(r["exposure"]))
