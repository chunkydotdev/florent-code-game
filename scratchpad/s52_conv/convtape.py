#!/usr/bin/env python3
"""s52 CONVEYOR-PASSABILITY tape.  See RECONCILE doc for the question.

Classifies EVERY builder-bot arrival on a tile by what BUILDING stands there at
the moment of arrival.  Three channels, deliberately separate:
    WALK   moveBuilderBot, d^2 <= 1   (an ordinary cardinal step; 1-tile throws
           are indistinguishable and land here -- the same unfixable undercount
           post-throw-tile-dwell-2026-08-09.md names)
    THROW  moveBuilderBot, d^2 >= 2   (a launcher throw)
    SPAWN  first placeEntity of a builder_bot id (core spawn)

BOTH-VERDICTS CONTROLS (all emitted every run):
  * IMPASSABLE classes (harvester/barrier/gunner/sentinel/launcher/core) are the
    NEGATIVE control: a decoder manufacturing conveyor hits by positional
    coincidence manufactures harvester hits too.  They must read ~0.
  * WALL arrivals: independent terrain channel, must read 0.
  * --shift dx dy : mutate the destination before lookup; conveyor share must
    collapse toward the background conveyor tile density.
  * --prevround   : occupancy as of END OF PREVIOUS ROUND, so the verdict does
    not rest on intra-round event ordering.
"""
from __future__ import annotations
import sys, json, argparse, collections
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import fields, parse_entity, read_pos, packed_varints  # noqa: E402

BUILDINGS = {"conveyor", "splitter", "harvester", "barrier",
             "gunner", "sentinel", "launcher", "core"}
CONV = {"conveyor", "splitter"}


def cls(entry, bot_team):
    if entry is None:
        return "empty"
    kind, team = entry
    return f"{kind}_{'own' if team == bot_team else 'enemy'}"


def walk(path, shift=(0, 0), prevround=False, keep_examples=0):
    data = Path(path).read_bytes()
    map_buf, turn_bufs = None, []
    for num, wire, val in fields(data):
        if num == 1 and wire == 2:
            map_buf = val
        elif num == 3 and wire == 2:
            turn_bufs.append(val)
    if map_buf is None:
        return None
    W = H = 0
    tiles = []
    for num, wire, val in fields(map_buf):
        if num == 1:
            W = val
        elif num == 2:
            H = val
        elif num == 3:
            row = []
            for rn, rw, rv in fields(val):
                if rn == 1:
                    row.extend(packed_varints(rv) if rw == 2 else [rv])
            tiles.append(row)

    occ = {}                 # (x,y) -> (kind, team)
    tiles_of = {}            # building id -> [tiles]
    bots = {}                # id -> [team, (x,y)]
    ent = {}                 # id -> (kind, team)
    prev_occ = {}
    out = {"WALK": collections.Counter(), "THROW": collections.Counter(),
           "SPAWN": collections.Counter(),
           "WALK_NOLAUNCHER": collections.Counter(),
           "WALK_LAUNCHERNEAR": collections.Counter()}
    launchers = set()   # live launcher tiles, either team
    walls = collections.Counter()
    dx, dy = shift
    conv_tile_rounds = total_tile_rounds = 0
    examples = []

    def lookup(pos):
        p = (pos[0] + dx, pos[1] + dy)
        return (prev_occ if prevround else occ).get(p), p

    def is_wall(p):
        return 0 <= p[1] < len(tiles) and 0 <= p[0] < len(tiles[p[1]]) and tiles[p[1]][p[0]] == 1

    for rnd, tb in enumerate(turn_bufs):
        if prevround:
            prev_occ = dict(occ)
        for _n, _w, ub in fields(tb):
            for unum, _uw, u in fields(ub):
                if unum == 1:                                  # placeEntity
                    for en, _ew, eb in fields(u):
                        if en != 1:
                            continue
                        e = parse_entity(eb, rnd)
                        if e is None:
                            continue
                        new = e.id not in ent
                        ent[e.id] = (e.kind, e.team)
                        if e.kind == "builder_bot":
                            if new:
                                entry, p = lookup(e.pos)
                                out["SPAWN"][cls(entry, e.team)] += 1
                                if is_wall(p):
                                    walls["SPAWN"] += 1
                            bots[e.id] = [e.team, e.pos]
                        elif e.kind in BUILDINGS:
                            for t in tiles_of.pop(e.id, []):
                                if occ.get(t) is not None:
                                    occ.pop(t, None)
                            ts = ([(e.pos[0] + a, e.pos[1] + b) for a in (0, 1) for b in (0, 1)]
                                  if e.kind == "core" else [e.pos])
                            for t in ts:
                                occ[t] = (e.kind, e.team)
                            tiles_of[e.id] = ts
                            if e.kind == "launcher":
                                launchers.add(e.pos)
                elif unum == 2:                                # moveBuilderBot
                    eid = to = None
                    for mn, _mw, mv in fields(u):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    b = bots.get(eid)
                    if b is None or to is None:
                        continue
                    fx, fy = b[1]
                    d2 = (to[0] - fx) ** 2 + (to[1] - fy) ** 2
                    ch = "WALK" if d2 <= 1 else "THROW"
                    entry, p = lookup(to)
                    key = cls(entry, b[0])
                    if ch == "WALK":
                        # DISCRIMINATOR for "a 1-tile launcher throw wearing a
                        # walk's costume": a throw needs a launcher of EITHER
                        # team within d^2 <= 2 of the bot's PRE-move tile.
                        near = any((lx - fx) ** 2 + (ly - fy) ** 2 <= 2
                                   for (lx, ly) in launchers)
                        out["WALK_NOLAUNCHER" if not near else "WALK_LAUNCHERNEAR"][key] += 1
                    out[ch][key] += 1
                    if is_wall(p):
                        walls[ch] += 1
                    if (ch == "WALK" and entry is not None and entry[0] in CONV
                            and len(examples) < keep_examples):
                        examples.append({"file": Path(path).name, "round": rnd,
                                         "bot": eid, "bot_team": b[0],
                                         "from": [fx, fy], "to": list(to), "d2": d2,
                                         "tile": f"{entry[0]}/team{entry[1]}",
                                         "launcher_near": any((lx-fx)**2+(ly-fy)**2 <= 2 for (lx,ly) in launchers),
                                         "launchers_alive": len(launchers)})
                    b[1] = to
                elif unum == 3:                                # removeEntity
                    for rn, _rw, rv in fields(u):
                        if rn != 1:
                            continue
                        bots.pop(rv, None)
                        for t in tiles_of.pop(rv, []):
                            occ.pop(t, None)
                            launchers.discard(t)
        conv_tile_rounds += sum(1 for v in occ.values() if v[0] in CONV)
        total_tile_rounds += W * H
    return {"out": {k: dict(v) for k, v in out.items()}, "walls": dict(walls),
            "rounds": len(turn_bufs), "conv_tile_rounds": conv_tile_rounds,
            "total_tile_rounds": total_tile_rounds, "examples": examples}


def merge(acc, r):
    for ch, c in r["out"].items():
        for k, v in c.items():
            acc["out"].setdefault(ch, collections.Counter())[k] += v
    for k, v in r["walls"].items():
        acc["walls"][k] += v
    acc["conv_tile_rounds"] += r["conv_tile_rounds"]
    acc["total_tile_rounds"] += r["total_tile_rounds"]
    acc["files"] += 1
    acc["examples"].extend(r["examples"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--list", help="file with one replay path per line")
    ap.add_argument("--shift", nargs=2, type=int, default=[0, 0])
    ap.add_argument("--prevround", action="store_true")
    ap.add_argument("--examples", type=int, default=0)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    paths = list(a.paths)
    if a.list:
        paths += [l.strip() for l in open(a.list) if l.strip()]
    acc = {"out": {}, "walls": collections.Counter(), "conv_tile_rounds": 0,
           "total_tile_rounds": 0, "files": 0, "examples": [], "errors": 0}
    for p in paths:
        try:
            r = walk(p, tuple(a.shift), a.prevround, a.examples)
        except Exception:
            acc["errors"] += 1
            continue
        if r:
            merge(acc, r)
    acc["out"] = {k: dict(v) for k, v in acc["out"].items()}
    acc["walls"] = dict(acc["walls"])
    print(json.dumps(acc, indent=1))


if __name__ == "__main__":
    main()
