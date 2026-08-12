#!/usr/bin/env python3
"""Fast-kill mechanism extractor.

Per replay, per team, reconstructs:
  * build order (first placeEntity per entity id) with round + position
  * builder-bot trajectories (placeEntity seed + moveBuilderBot), so we can ask
    "when did a body of team T first stand within d2 X of team (1-T)'s core"
  * every fireTurret / builderAttack, attributed to a team by looking up the
    entity that occupies the firing tile
  * core HP trace from updateHp on the two core ids
  * per-round economy from updatePlayers (titanium, titaniumCollected, ammo)

Emits one JSON object per replay on stdout (ndjson).

Team byte -> seat: validated in this session on 13,440 archived games with a
core death, 13,440/13,440 consistent: winner side 'a' <=> dead core team 1,
winner side 'b' <=> dead core team 0.  So TEAM_A == 0, TEAM_B == 1.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa: E402


def _packed(buf):
    out, i = [], 0
    while i < len(buf):
        r = s = 0
        while True:
            b = buf[i]
            i += 1
            r |= (b & 0x7F) << s
            if not (b & 0x80):
                break
            s += 7
        out.append(r)
    return out


def d2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def census(path: Path):
    data = path.read_bytes()
    map_buf, turn_bufs, wincond, winner = None, [], "", None
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
        elif num == 4:
            winner = value
        elif num == 6 and wire == WIRE_LEN:
            wincond = value.decode("utf8", "replace")
    if map_buf is None:
        return None
    w = h = 0
    cores, tiles = [], []
    for num, wire, value in fields(map_buf):
        if num == 1:
            w = value
        elif num == 2:
            h = value
        elif num == 3:
            row = []
            for rn, rw, rv in fields(value):
                if rn == 1:
                    row.extend(_packed(rv) if rw == WIRE_LEN else [rv])
            tiles.append(row)
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
    if len(cores) != 2:
        return None
    corepos = {c["team"]: c["pos"] for c in cores}
    coreid = {c["team"]: c["id"] for c in cores}
    foot = {t: {(p[0] + dx, p[1] + dy) for dx in (0, 1) for dy in (0, 1)}
            for t, p in corepos.items()}

    ents = {}                                   # id -> [team, kind, pos]
    for c in cores:
        ents[c["id"]] = [c["team"], "core", c["pos"]]
    occ = {}                                    # pos -> id (buildings only)
    for c in cores:
        for p in foot[c["team"]]:
            occ[p] = c["id"]

    out = {
        "file": path.name, "w": w, "h": h, "turns": len(turn_bufs),
        "wincond": wincond, "winner": winner,
        "corepos": {str(t): list(p) for t, p in corepos.items()},
        "core_d2": d2(corepos[0], corepos[1]),
        "builds": [],       # [rnd, team, kind, x, y]
        "deaths": [],       # [rnd, team, kind, x, y]
        "corehp": [],       # [rnd, team, delta]
        "core_dmg": [],     # [rnd, victim_team, src_team, src_kind, srcx, srcy, srcid]
        "atk": [],          # [rnd, team, kind, tx, ty, d2_to_enemy_core]
        "econ": [],         # [rnd, ti_a, coll_a, ammo_a, ti_b, coll_b, ammo_b]
        "reach": {},        # "team:thresh" -> first round a bot of team was within thresh of enemy core
        "botpos": [],       # [rnd, team, minimal d2 of any builder bot to enemy core]
    }
    THRESH = (2, 8, 18, 36, 100)

    for rnd, turn_buf in enumerate(turn_bufs):
        fires = []      # (srcpos, dstpos)
        battacks = []   # (botid, target)
        hpdelta = {}    # id -> delta
        for _n, _w2, ub in fields(turn_buf):
            for unum, uw, ubuf in fields(ub):
                if unum == 1 and uw == WIRE_LEN:
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        if e.id in ents:                     # rotate re-emit
                            ents[e.id][2] = e.pos
                            continue
                        ents[e.id] = [e.team, e.kind, e.pos]
                        if e.kind != "builder_bot":
                            occ[e.pos] = e.id
                        out["builds"].append([rnd, e.team, e.kind, e.pos[0], e.pos[1]])
                elif unum == 2 and uw == WIRE_LEN:
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid in ents and to:
                        ents[eid][2] = to
                elif unum == 3 and uw == WIRE_LEN:
                    for rn, _rw, rv in fields(ubuf):
                        e = ents.pop(rv, None)
                        if e is None:
                            continue
                        t, k, p = e
                        if occ.get(p) == rv:
                            del occ[p]
                        out["deaths"].append([rnd, t, k, p[0], p[1]])
                elif unum == 5 and uw == WIRE_LEN:
                    eid = delta = None
                    for hn, _hw, hv in fields(ubuf):
                        if hn == 1:
                            eid = hv
                        elif hn == 2:
                            delta = hv
                    if eid is not None and delta is not None:
                        # protobuf int32 negative -> big varint
                        if delta >= (1 << 63):
                            delta -= (1 << 64)
                        hpdelta[eid] = hpdelta.get(eid, 0) + delta
                elif unum == 6 and uw == WIRE_LEN:
                    row = {}
                    for pn, _pw, pv in fields(ubuf):
                        if pn != 1:
                            continue
                        for sn, _sw, sv in fields(pv):
                            if sn not in (1, 2):
                                continue
                            side = "a" if sn == 1 else "b"
                            for fn, _fw, fv in fields(sv):
                                if fn == 1:
                                    row[side + "_ti"] = fv
                                elif fn == 4:
                                    row[side + "_coll"] = fv
                                elif fn == 7:
                                    row[side + "_ammo"] = fv
                    if row:
                        out["econ"].append([rnd, row.get("a_ti", 0), row.get("a_coll", 0),
                                            row.get("a_ammo", 0), row.get("b_ti", 0),
                                            row.get("b_coll", 0), row.get("b_ammo", 0)])
                elif unum == 12 and uw == WIRE_LEN:
                    frm = to = None
                    for fn, _fw, fv in fields(ubuf):
                        if fn == 1:
                            frm = read_pos(fv)
                        elif fn == 2:
                            to = read_pos(fv)
                    if frm and to:
                        fires.append((frm, to))
                elif unum == 13 and uw == WIRE_LEN:
                    bid = tgt = None
                    for bn, _bw, bv in fields(ubuf):
                        if bn == 1:
                            bid = bv
                        elif bn == 2:
                            tgt = read_pos(bv)
                    if bid is not None and tgt:
                        battacks.append((bid, tgt))

        # attribute attacks
        for frm, to in fires:
            sid = occ.get(frm)
            if sid is None or sid not in ents:
                team, kind = -1, "?"
            else:
                team, kind = ents[sid][0], ents[sid][1]
            enemy = 1 - team if team in (0, 1) else 0
            out["atk"].append([rnd, team, kind, to[0], to[1], d2(to, corepos[enemy])])
            for vt in (0, 1):
                if to in foot[vt]:
                    out["core_dmg"].append([rnd, vt, team, kind, frm[0], frm[1],
                                            sid if sid is not None else -1])
        for bid, tgt in battacks:
            e = ents.get(bid)
            team = e[0] if e else -1
            enemy = 1 - team if team in (0, 1) else 0
            bp = e[2] if e else (-1, -1)
            out["atk"].append([rnd, team, "builder_atk", tgt[0], tgt[1], d2(tgt, corepos[enemy])])
            for vt in (0, 1):
                if tgt in foot[vt]:
                    out["core_dmg"].append([rnd, vt, team, "builder_atk", bp[0], bp[1], bid])
        for t in (0, 1):
            dl = hpdelta.get(coreid[t])
            if dl:
                out["corehp"].append([rnd, t, dl])

        # builder-bot proximity
        for t in (0, 1):
            best = None
            for eid, (et, ek, ep) in ents.items():
                if et != t or ek != "builder_bot":
                    continue
                dd = d2(ep, corepos[1 - t])
                if best is None or dd < best:
                    best = dd
            if best is not None:
                out["botpos"].append([rnd, t, best])
                for th in THRESH:
                    key = f"{t}:{th}"
                    if best <= th and key not in out["reach"]:
                        out["reach"][key] = rnd
    return out


def main(argv):
    for a in argv:
        try:
            r = census(Path(a))
        except Exception as exc:                             # noqa: BLE001
            print(json.dumps({"file": Path(a).name, "err": str(exc)}))
            continue
        if r:
            print(json.dumps(r))


if __name__ == "__main__":
    main(sys.argv[1:])
