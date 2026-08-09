#!/usr/bin/env python3
"""Launcher-throw census v2 — outcome measured from BuilderAttack, not HP guesswork.

v1 attributed core damage by "an inserted raider was standing adjacent when the
core lost HP". That is a proxy and its sign handling was wrong (updateHp.delta is
a 64-bit two's-complement varint: 18446744073709551609 == -7). v2 drops the proxy
and uses the direct event:

    BuilderAttack { int32 id = 1; Pos target = 2; }   // Update field 13

A raider that is doing damage to the enemy core emits BuilderAttack with a target
inside the enemy core's 2x2 footprint. That is unambiguous and per-bot.

Per own-team forward throw ("INSERT") we record, from the throw until the bot
dies or is thrown again:
    life        rounds the bot stayed alive
    core_atk    BuilderAttack events aimed at the ENEMY core footprint
    any_atk     BuilderAttack events aimed at anything
    reached     did it ever stand orthogonally adjacent to the enemy core
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import fields, read_pos, parse_entity, WIRE_LEN, WIRE_VARINT  # noqa: E402


def d2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


class Ent:
    __slots__ = ("id", "team", "pos", "kind")

    def __init__(self, eid, team, pos, kind):
        self.id, self.team, self.pos, self.kind = eid, team, pos, kind


def census(path: Path):
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
    if map_buf is None:
        return []

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
    if len(corepos) != 2:
        return []
    foot = {t: {(p[0] + dx, p[1] + dy) for dx in (0, 1) for dy in (0, 1)}
            for t, p in corepos.items()}

    ents = {c["id"]: Ent(c["id"], c["team"], c["pos"], "core") for c in cores}
    recs, active = [], {}          # bot id -> rec currently being tracked
    nrounds = len(turn_bufs)

    def close(rec, rnd):
        rec["life"] = rnd - rec["rnd"]

    for rnd, turn_buf in enumerate(turn_bufs):
        for _n, _w2, update_buf in fields(turn_buf):
            for unum, _uw, ubuf in fields(update_buf):
                if unum == 1:                                    # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        if e.id in ents:
                            ents[e.id].pos = e.pos
                            continue
                        ents[e.id] = Ent(e.id, e.team, e.pos, e.kind)
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
                    frm = e.pos
                    e.pos = to
                    if abs(to[0] - frm[0]) + abs(to[1] - frm[1]) <= 1:
                        continue
                    cand = [o for o in ents.values()
                            if o.kind == "launcher" and d2(o.pos, frm) <= 2]
                    cteams = {o.team for o in cand}
                    if not cand:
                        tteam, amb = None, "none"
                    elif len(cteams) == 1:
                        tteam, amb = cand[0].team, ("one" if len(cand) == 1 else "same_team")
                    else:
                        tteam, amb = None, "both_teams"
                    bteam = e.team
                    ec = corepos[(1 - tteam) if tteam is not None else (1 - bteam)]
                    before, after = d2(frm, ec), d2(to, ec)
                    kind = ("UNATTRIB" if tteam is None else
                            "EXILE" if tteam != bteam else
                            "INSERT" if after < before else "RETREAT")
                    rec = dict(file=path.name, mw=w, mh=h, rounds=nrounds, rnd=rnd,
                               kind=kind, tteam=-1 if tteam is None else tteam,
                               bteam=bteam, amb=amb, d2_before=before, d2_after=after,
                               bot=eid, life=-1, core_atk=0, any_atk=0, reached=0,
                               winner=-1 if winner is None else winner, wincond=wincond)
                    recs.append(rec)
                    if kind == "INSERT":
                        old = active.pop(eid, None)
                        if old is not None:
                            close(old, rnd)
                        active[eid] = rec
                elif unum == 3:                                  # removeEntity
                    for rn, _rw, rv in fields(ubuf):
                        ents.pop(rv, None)
                        old = active.pop(rv, None)
                        if old is not None:
                            close(old, rnd)
                elif unum == 13:                                 # builderAttack
                    aid = tgt = None
                    for an, _aw, av in fields(ubuf):
                        if an == 1:
                            aid = av
                        elif an == 2:
                            tgt = read_pos(av)
                    rec = active.get(aid)
                    if rec is None or tgt is None:
                        continue
                    rec["any_atk"] += 1
                    b = ents.get(aid)
                    if b is not None and tgt in foot[1 - b.team]:
                        rec["core_atk"] += 1
        for bid, rec in active.items():
            b = ents.get(bid)
            if b is None:
                continue
            if any(abs(b.pos[0] - fx) + abs(b.pos[1] - fy) == 1
                   for fx, fy in foot[1 - b.team]):
                rec["reached"] = 1
    for bid, rec in active.items():                              # survived to the end
        close(rec, nrounds)
    return recs


COLS = ["file", "mw", "mh", "rounds", "rnd", "kind", "tteam", "bteam", "amb",
        "d2_before", "d2_after", "bot", "life", "core_atk", "any_atk", "reached",
        "winner", "wincond"]


def main(argv):
    out = sys.stdout
    out.write("\t".join(COLS) + "\n")
    bad = 0
    for i, p in enumerate(Path(x) for x in argv):
        try:
            for rec in census(p):
                out.write("\t".join(str(rec[c]) for c in COLS) + "\n")
        except Exception as exc:                                 # noqa: BLE001
            bad += 1
            print(f"ERR {p.name}: {exc}", file=sys.stderr)
        if (i + 1) % 500 == 0:
            print(f"  ...{i+1}/{len(argv)} ({bad} err)", file=sys.stderr, flush=True)
    print(f"done {len(argv)} files, {bad} errors", file=sys.stderr, flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
