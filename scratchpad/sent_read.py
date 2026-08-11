#!/usr/bin/env python3
"""INDEPENDENT sentinel-firing decoder. Written from tools/replay_schema.md only.

Does NOT import, read or derive from scratchpad/ammo_probe.py.

Classifies every SENTINEL (ours and the opponent's) in a set of replays into
exactly one of four buckets over its lifetime:

  FIRED                  emitted >=1 fireTurret from its own tile
  DIED_YOUNG             never fired, lifespan < 3 rounds
  NO_TARGET_EVER         never fired, lifespan >=3, no enemy entity ever stood
                         on a tile of its firing line (end-of-round snapshot)
  HAD_TARGET_NEVER_FIRED never fired, lifespan >=3, enemy stood in line >=1 round

Sentinel line = single-tile-wide ray along facing, d^2 <= 32, ignores obstacles.
READ-ONLY.
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[0]

# ---------------------------------------------------------------- protobuf ---


def _vi(buf, i):
    r = 0
    s = 0
    while True:
        b = buf[i]
        i += 1
        r |= (b & 0x7F) << s
        if not (b & 0x80):
            return r, i
        s += 7


def _skip(buf, i, wt):
    if wt == 0:
        _, i = _vi(buf, i)
        return i
    if wt == 2:
        n, i = _vi(buf, i)
        return i + n
    if wt == 5:
        return i + 4
    if wt == 1:
        return i + 8
    raise ValueError(f"wiretype {wt}")


def _pos(buf, i, end):
    x = y = 0
    while i < end:
        k, i = _vi(buf, i)
        f, wt = k >> 3, k & 7
        if f == 1 and wt == 0:
            x, i = _vi(buf, i)
        elif f == 2 and wt == 0:
            y, i = _vi(buf, i)
        else:
            i = _skip(buf, i, wt)
    return (x, y)


KIND = {10: "builder_bot", 11: "conveyor", 12: "splitter", 15: "harvester",
        18: "barrier", 20: "core", 21: "gunner", 22: "sentinel", 24: "launcher"}


def _entity(buf, i, end):
    """-> (id, team, pos, kind, direction|None)"""
    eid = team = 0
    pos = None
    kind = None
    direction = None
    while i < end:
        k, i = _vi(buf, i)
        f, wt = k >> 3, k & 7
        if f == 1 and wt == 0:
            eid, i = _vi(buf, i)
        elif f == 2 and wt == 0:
            team, i = _vi(buf, i)
        elif f == 3 and wt == 2:
            n, i = _vi(buf, i)
            pos = _pos(buf, i, i + n)
            i += n
        elif wt == 2 and f in KIND:
            n, i = _vi(buf, i)
            kind = KIND[f]
            if f in (11, 12, 21, 22):          # carries a Direction at field 1
                j, e2 = i, i + n
                direction = 0
                while j < e2:
                    k2, j = _vi(buf, j)
                    f2, w2 = k2 >> 3, k2 & 7
                    if f2 == 1 and w2 == 0:
                        direction, j = _vi(buf, j)
                    else:
                        j = _skip(buf, j, w2)
            i += n
        else:
            i = _skip(buf, i, wt)
    return eid, team, pos, kind, direction


DELTA = {0: (0, 0), 1: (0, -1), 2: (1, -1), 3: (1, 0), 4: (1, 1),
         5: (0, 1), 6: (-1, 1), 7: (-1, 0), 8: (-1, -1)}
DIRNAME = {0: "CENTRE", 1: "N", 2: "NE", 3: "E", 4: "SE", 5: "S", 6: "SW",
           7: "W", 8: "NW"}
SENT_RSQ = 32


def _ray(d):
    dx, dy = DELTA[d]
    if dx == 0 and dy == 0:
        return ()
    out = []
    k = 1
    while (k * dx) ** 2 + (k * dy) ** 2 <= SENT_RSQ:
        out.append((k * dx, k * dy))
        k += 1
    return tuple(out)


RAY = {d: _ray(d) for d in DELTA}


# ------------------------------------------------------------------ decode ---


def parse_replay(path):
    """-> dict(width,height,cores=[(id,team,(x,y))],turns=[[(kind,payload)...]])

    Only Update kinds 1 (placeEntity), 2 (moveBuilderBot), 3 (removeEntity)
    and 12 (fireTurret) are decoded; everything else is skipped by length.
    """
    with open(path, "rb") as fh:
        b = fh.read()
    i, n = 0, len(b)
    width = height = 0
    cores = []
    turns = []
    winner = None
    while i < n:
        k, i = _vi(b, i)
        f, wt = k >> 3, k & 7
        if f == 1 and wt == 2:                                   # Map
            ln, i = _vi(b, i)
            j, e = i, i + ln
            while j < e:
                k2, j = _vi(b, j)
                f2, w2 = k2 >> 3, k2 & 7
                if f2 == 1 and w2 == 0:
                    width, j = _vi(b, j)
                elif f2 == 2 and w2 == 0:
                    height, j = _vi(b, j)
                elif f2 == 4 and w2 == 2:                        # CorePosition
                    n2, j = _vi(b, j)
                    j2, e2 = j, j + n2
                    cid = ct = 0
                    cp = (0, 0)
                    while j2 < e2:
                        k3, j2 = _vi(b, j2)
                        f3, w3 = k3 >> 3, k3 & 7
                        if f3 == 1 and w3 == 0:
                            cid, j2 = _vi(b, j2)
                        elif f3 == 2 and w3 == 0:
                            ct, j2 = _vi(b, j2)
                        elif f3 == 3 and w3 == 2:
                            n3, j2 = _vi(b, j2)
                            cp = _pos(b, j2, j2 + n3)
                            j2 += n3
                        else:
                            j2 = _skip(b, j2, w3)
                    cores.append((cid, ct, cp))
                    j += n2
                else:
                    j = _skip(b, j, w2)
            i = e
        elif f == 3 and wt == 2:                                 # Turn
            ln, i = _vi(b, i)
            j, e = i, i + ln
            ups = []
            while j < e:
                k2, j = _vi(b, j)
                f2, w2 = k2 >> 3, k2 & 7
                if f2 != 1 or w2 != 2:
                    j = _skip(b, j, w2)
                    continue
                n2, j = _vi(b, j)
                j2, e2 = j, j + n2
                j += n2
                # Update is a oneof: exactly one field
                while j2 < e2:
                    k3, j2 = _vi(b, j2)
                    f3, w3 = k3 >> 3, k3 & 7
                    if w3 != 2:
                        j2 = _skip(b, j2, w3)
                        continue
                    n3, j2 = _vi(b, j2)
                    s, se = j2, j2 + n3
                    j2 += n3
                    if f3 == 1:                                  # placeEntity
                        # PlaceEntity{entity=1}
                        while s < se:
                            k4, s = _vi(b, s)
                            f4, w4 = k4 >> 3, k4 & 7
                            if f4 == 1 and w4 == 2:
                                n4, s = _vi(b, s)
                                ups.append(("place", _entity(b, s, s + n4)))
                                s += n4
                            else:
                                s = _skip(b, s, w4)
                    elif f3 == 2:                                # moveBuilderBot
                        eid = 0
                        to = None
                        while s < se:
                            k4, s = _vi(b, s)
                            f4, w4 = k4 >> 3, k4 & 7
                            if f4 == 1 and w4 == 0:
                                eid, s = _vi(b, s)
                            elif f4 == 2 and w4 == 2:
                                n4, s = _vi(b, s)
                                to = _pos(b, s, s + n4)
                                s += n4
                            else:
                                s = _skip(b, s, w4)
                        ups.append(("move", (eid, to)))
                    elif f3 == 3:                                # removeEntity
                        eid = 0
                        while s < se:
                            k4, s = _vi(b, s)
                            f4, w4 = k4 >> 3, k4 & 7
                            if f4 == 1 and w4 == 0:
                                eid, s = _vi(b, s)
                            else:
                                s = _skip(b, s, w4)
                        ups.append(("remove", eid))
                    elif f3 == 12:                               # fireTurret
                        fr = to = None
                        while s < se:
                            k4, s = _vi(b, s)
                            f4, w4 = k4 >> 3, k4 & 7
                            if f4 == 1 and w4 == 2:
                                n4, s = _vi(b, s)
                                fr = _pos(b, s, s + n4)
                                s += n4
                            elif f4 == 2 and w4 == 2:
                                n4, s = _vi(b, s)
                                to = _pos(b, s, s + n4)
                                s += n4
                            else:
                                s = _skip(b, s, w4)
                        ups.append(("fire", (fr, to)))
            turns.append(ups)
            i = e
        elif f == 4 and wt == 0:
            winner, i = _vi(b, i)
        else:
            i = _skip(b, i, wt)
    return {"width": width, "height": height, "cores": cores, "turns": turns,
            "winner": winner}


def analyse(path, our_team):
    """-> per-replay stats dict. our_team in {0,1}; None => label both sides."""
    R = parse_replay(path)
    turns = R["turns"]
    nrounds = len(turns)

    ent_pos = {}          # id -> pos
    ent_team = {}
    ent_kind = {}
    turret_at = {}        # pos -> id, for gunners/sentinels only
    occ = [defaultdict(int), defaultdict(int)]   # team -> pos -> count

    def add(eid, team, pos):
        occ[team][pos] += 1

    def rem(eid):
        p = ent_pos.pop(eid, None)
        if p is None:
            return
        t = ent_team.pop(eid)
        ent_kind.pop(eid, None)
        occ[t][p] -= 1
        if occ[t][p] <= 0:
            del occ[t][p]

    # cores exist only in map.cores; 2x2 footprint from NW corner
    core_ids = {}
    for cid, ct, (cx, cy) in R["cores"]:
        core_ids[cid] = (ct, [(cx, cy), (cx + 1, cy), (cx, cy + 1),
                              (cx + 1, cy + 1)])
        for p in core_ids[cid][1]:
            occ[ct][p] += 1

    # sentinel records
    sent = {}   # id -> record
    replaced = Counter()      # kind -> number of re-emitted placeEntity
    sent_dir_changes = 0
    fire_unattr = 0
    fire_total = 0
    sent_fire_online = 0
    sent_fire_offline = 0
    offline_examples = []

    for r, ups in enumerate(turns):
        dead_this_round = {}      # pos -> turret id removed earlier this round
        for kind, payload in ups:
            if kind == "place":
                eid, team, pos, k, direction = payload
                if eid in ent_pos:
                    replaced[k] += 1
                    if ent_pos[eid] != pos:
                        # position change via placeEntity (not expected)
                        p = ent_pos[eid]
                        occ[team][p] -= 1
                        if occ[team][p] <= 0:
                            del occ[team][p]
                        ent_pos[eid] = pos
                        add(eid, team, pos)
                    if k == "sentinel":
                        rec = sent[eid]
                        if direction != rec["dir"]:
                            sent_dir_changes += 1
                        rec["dir"] = direction
                        rec["dir_hist"].append((r, direction))
                else:
                    ent_pos[eid] = pos
                    ent_team[eid] = team
                    ent_kind[eid] = k
                    add(eid, team, pos)
                    if k in ("gunner", "sentinel"):
                        turret_at[pos] = eid
                    if k == "sentinel":
                        sent[eid] = {"id": eid, "team": team, "pos": pos,
                                     "dir": direction, "build": r, "end": None,
                                     "shots": 0, "first_shot": None,
                                     "opp_rounds": 0,
                                     "dir_hist": [(r, direction)]}
            elif kind == "move":
                eid, to = payload
                if eid in ent_pos:
                    t = ent_team[eid]
                    p = ent_pos[eid]
                    occ[t][p] -= 1
                    if occ[t][p] <= 0:
                        del occ[t][p]
                    ent_pos[eid] = to
                    occ[t][to] += 1
            elif kind == "remove":
                eid = payload
                if eid in core_ids:
                    ct, tiles = core_ids.pop(eid)
                    for p in tiles:
                        occ[ct][p] -= 1
                        if occ[ct][p] <= 0:
                            del occ[ct][p]
                    continue
                if eid in sent:
                    sent[eid]["end"] = r
                if ent_kind.get(eid) in ("gunner", "sentinel"):
                    p = ent_pos.get(eid)
                    if p is not None and turret_at.get(p) == eid:
                        del turret_at[p]
                        dead_this_round[p] = eid
                rem(eid)
            elif kind == "fire":
                fr, to = payload
                fire_total += 1
                # attribute by tile; the firing turret may already have been
                # removed this round -> fall back to the dead-this-round map
                owner = turret_at.get(fr)
                if owner is None:
                    owner = dead_this_round.get(fr)
                if owner is None:
                    fire_unattr += 1
                elif owner in sent:
                    rec = sent[owner]
                    rec["shots"] += 1
                    if rec["first_shot"] is None:
                        rec["first_shot"] = r
                    d = rec["dir"]
                    dx, dy = fr[0], fr[1]
                    rel = (to[0] - dx, to[1] - dy)
                    if rel in RAY[d]:
                        sent_fire_online += 1
                    else:
                        sent_fire_offline += 1
                        if len(offline_examples) < 5:
                            offline_examples.append(
                                (r, fr, to, DIRNAME.get(d)))
        # end-of-round: opportunity snapshot for every live sentinel
        for eid, rec in sent.items():
            if rec["end"] is not None or eid not in ent_pos:
                continue
            if r < rec["build"]:
                continue
            enemy = occ[1 - rec["team"]]
            if not enemy:
                continue
            px, py = rec["pos"]
            for ox, oy in RAY[rec["dir"]]:
                if (px + ox, py + oy) in enemy:
                    rec["opp_rounds"] += 1
                    break

    for rec in sent.values():
        if rec["end"] is None:
            rec["end"] = nrounds - 1
    return {"sent": list(sent.values()), "rounds": nrounds,
            "winner": R["winner"], "replaced": replaced,
            "sent_dir_changes": sent_dir_changes,
            "fire_total": fire_total, "fire_unattr": fire_unattr,
            "sent_fire_online": sent_fire_online,
            "sent_fire_offline": sent_fire_offline,
            "offline_examples": offline_examples}


def bucket(rec):
    if rec["shots"] > 0:
        return "FIRED"
    life = rec["end"] - rec["build"] + 1
    if life < 3:
        return "DIED_YOUNG"
    if rec["opp_rounds"] == 0:
        return "NO_TARGET_EVER"
    return "HAD_TARGET_NEVER_FIRED"


if __name__ == "__main__":
    for p in sys.argv[1:]:
        st = analyse(p, None)
        c = Counter()
        for rec in st["sent"]:
            c[(rec["team"], bucket(rec))] += 1
        print(p, st["rounds"], dict(c), "fire", st["fire_total"],
              "unattr", st["fire_unattr"], "online", st["sent_fire_online"],
              "offline", st["sent_fire_offline"])
