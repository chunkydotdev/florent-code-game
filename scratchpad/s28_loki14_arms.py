#!/usr/bin/env python3
"""LOKI-14 leg read: border-vs-interior kidnap throws and undamaged removals.

Reuses tools/replay_census.py wire primitives and the DETECTION LOGIC of
tools/corpus/replay_throws.py (a moveBuilderBot whose manhattan step > 1 is a
launcher throw; the thrower is a launcher within d^2 <= 2 of the ORIGIN tile)
plus the CLASSIFICATION RULE of tools/crash_census.py (a removeEntity for an
entity that never had an updateHp event, and whose kind runs code, is a
crash_candidate).

The `LOKI14 KIDNAP arm=` print stream is NOT available: platform-downloaded
replays carry BotOutput with fields {1:id, 3:execTimeUs} only -- stdout
(field 2) is stripped. So arms are reconstructed from the DESTINATION TILE,
which is a superset of the logged arm (a fallback "F" throw that happens to
land on a border tile counts as border here).
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import fields, read_pos, parse_entity, WIRE_LEN, WIRE_VARINT  # noqa: E402

OURS = "379a5d80-9921-4c9e-949b-f9b1dcba16be"
UNIT_KINDS = {"core", "builder_bot", "gunner", "sentinel", "launcher"}
ARCH = Path("replay_archive")

# map fingerprint -> name, built from maps/*.map26 tile rows
def map_fingerprints():
    fp = {}
    for p in sorted(Path("maps").glob("*.map26")):
        d = p.read_bytes()
        w = h = None
        rows = []
        for n, _w, v in fields(d):
            if n == 1:
                w = v
            elif n == 2:
                h = v
            elif n == 3:
                rows.append(bytes(v))
        fp[(w, h, hash(tuple(rows)))] = p.stem
    return fp

FP = map_fingerprints()


def d2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


class Ent:
    __slots__ = ("id", "team", "pos", "kind")

    def __init__(self, eid, team, pos, kind):
        self.id, self.team, self.pos, self.kind = eid, team, pos, kind


def analyse(path: Path, our_wire_team: int):
    data = path.read_bytes()
    map_buf, turns = None, []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turns.append(value)
    w = h = None
    rows = []
    cores = []
    for num, _wire, value in fields(map_buf):
        if num == 1:
            w = value
        elif num == 2:
            h = value
        elif num == 3:
            rows.append(bytes(value))
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
    mapname = FP.get((w, h, hash(tuple(rows))), f"unknown_{w}x{h}")

    ents = {c["id"]: Ent(c["id"], c["team"], c["pos"], "core") for c in cores}
    seen = dict(ents)                      # id -> Ent, never popped (for post-mortem)
    damaged = set()
    removed = {}                           # id -> round
    throws = []                            # dicts

    for rnd, turn_buf in enumerate(turns):
        for _n, _w2, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:                                   # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        if e.id in ents:
                            ents[e.id].pos = e.pos
                            continue
                        ent = Ent(e.id, e.team, e.pos, e.kind)
                        ents[e.id] = ent
                        seen[e.id] = ent
                elif unum == 2:                                 # moveBuilderBot
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
                    lp = cand[0].pos if len(cand) == 1 else None
                    throws.append(dict(
                        map=mapname, w=w, h=h, rnd=rnd, victim=eid,
                        victim_team=e.team, thrower_team=(-1 if tteam is None else tteam),
                        amb=amb, to=to, frm=frm,
                        d2_launch=(d2(lp, to) if lp else -1),
                        launcher_margin=(min(lp[0], lp[1], w - 1 - lp[0], h - 1 - lp[1])
                                         if lp else -1),
                        border=int(to[0] == 0 or to[1] == 0 or to[0] == w - 1 or to[1] == h - 1),
                        ours_threw=int(tteam == our_wire_team),
                        enemy_victim=int(e.team != our_wire_team),
                    ))
                elif unum == 3:                                 # removeEntity
                    for rn, _rw, rv in fields(ubuf):
                        if rn != 1:
                            continue
                        if rv in ents:
                            ents.pop(rv, None)
                            removed[rv] = rnd
                elif unum == 5:                                 # updateHp
                    for n2, _w2b, v2 in fields(ubuf):
                        if n2 == 1:
                            damaged.add(v2)

    for t in throws:
        vid = t["victim"]
        rm = removed.get(vid)
        t["removed_rnd"] = -1 if rm is None else rm
        ent = seen.get(vid)
        kind = ent.kind if ent else "?"
        undamaged = (rm is not None and vid not in damaged and kind in UNIT_KINDS)
        t["undamaged_removal"] = int(undamaged)
        t["within3"] = int(undamaged and 0 <= rm - t["rnd"] <= 3)
        t["gap"] = -1 if rm is None else rm - t["rnd"]
    return mapname, throws, len(turns)


def main():
    ids = [l.strip() for l in open("scratchpad/s28_loki14_ids.txt")
           if l.strip() and not l.startswith("#")]
    rows = []
    seatmix = Counter()
    for mid in ids:
        meta = json.load(open(ARCH / f"{mid}.meta.json"))
        our_wire_team = 0 if meta["teamAId"] == OURS else 1
        opp = meta["teamBName"] if our_wire_team == 0 else meta["teamAName"]
        seatmix["A" if our_wire_team == 0 else "B"] += 1
        for g in range(1, 6):
            p = ARCH / f"{mid}_game_{g}.replay26"
            mapname, throws, nr = analyse(p, our_wire_team)
            for t in throws:
                t["match"] = mid
                t["game"] = g
                t["opp"] = opp
                t["rounds"] = nr
                rows.append(t)
    out = Path("scratchpad/s28_loki14_throws.tsv")
    cols = ["match", "game", "opp", "map", "w", "h", "rounds", "rnd", "victim",
            "victim_team", "thrower_team", "amb", "ours_threw", "enemy_victim",
            "border", "d2_launch", "launcher_margin", "removed_rnd", "gap",
            "undamaged_removal", "within3"]
    with out.open("w") as f:
        f.write("\t".join(cols) + "\n")
        for r in rows:
            f.write("\t".join(str(r[c]) for c in cols) + "\n")
    print(f"wrote {out} ({len(rows)} throw events, 75 games)")
    print("seat mix (our wire team by match):", dict(seatmix))
    print("all throw events by (ours_threw, enemy_victim, amb):",
          Counter((r["ours_threw"], r["enemy_victim"], r["amb"]) for r in rows).most_common())


if __name__ == "__main__":
    main()
