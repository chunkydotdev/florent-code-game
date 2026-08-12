#!/usr/bin/env python3
"""Throw census with DESTINATION TILES, so 'thrown to the map border' is testable.

A throw is a moveBuilderBot whose manhattan step > 1.  Attributed to the launcher
adjacent (d2<=2) to the FROM tile.  Records: thrower team, bot team, from/to,
whether `to` is a border tile, and how long the bot lived afterwards.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, "tools")
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa: E402


def d2(a, b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2


def census(path: Path):
    data = path.read_bytes()
    map_buf, turn_bufs = None, []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if map_buf is None:
        return None
    w = h = 0
    cores = []
    for num, wire, value in fields(map_buf):
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
    if len(cores) != 2:
        return None
    corepos = {c["team"]: c["pos"] for c in cores}
    ents = {c["id"]: [c["team"], "core", c["pos"]] for c in cores}
    throws = []          # dicts
    pending = {}         # botid -> throw record index
    for rnd, turn_buf in enumerate(turn_bufs):
        for _n, _w2, ub in fields(turn_buf):
            for unum, uw, ubuf in fields(ub):
                if unum == 1 and uw == WIRE_LEN:
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        if e.id in ents:
                            ents[e.id][2] = e.pos
                            continue
                        ents[e.id] = [e.team, e.kind, e.pos]
                elif unum == 2 and uw == WIRE_LEN:
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    e = ents.get(eid)
                    if e is None or to is None:
                        continue
                    frm = e[2]
                    e[2] = to
                    if abs(to[0]-frm[0]) + abs(to[1]-frm[1]) <= 1:
                        continue
                    cand = [v for v in ents.values()
                            if v[1] == "launcher" and d2(v[2], frm) <= 2]
                    tt = {v[0] for v in cand}
                    tteam = cand[0][0] if len(tt) == 1 else -1
                    rec = {"rnd": rnd, "tteam": tteam, "bteam": e[0],
                           "fx": frm[0], "fy": frm[1], "tx": to[0], "ty": to[1],
                           "border": int(to[0] in (0, w-1) or to[1] in (0, h-1)),
                           "d2_ownc_before": d2(frm, corepos[e[0]]),
                           "d2_ownc_after": d2(to, corepos[e[0]]),
                           "life": -1}
                    pending[eid] = len(throws)
                    throws.append(rec)
                elif unum == 3 and uw == WIRE_LEN:
                    for rn, _rw, rv in fields(ubuf):
                        e = ents.pop(rv, None)
                        i = pending.pop(rv, None)
                        if i is not None:
                            throws[i]["life"] = rnd - throws[i]["rnd"]
    return {"file": path.name, "w": w, "h": h, "turns": len(turn_bufs),
            "corepos": {str(t): list(p) for t, p in corepos.items()},
            "throws": throws}


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
