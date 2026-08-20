#!/usr/bin/env python3
"""s52 -- trace HOW a body standing on its own conveyor on a CORE RING SOCKET
got onto that tile, at the moment its core takes a heal.

Population: the RING-ENGAGEMENT study's own fixture (900 replays in
scratchpad/s51_vs_holder/rep).  For every UpdateHp heal event (delta in 1..4)
naming a CORE, we enumerate that team's builder bots standing on one of the 8
orthogonal ring sockets of that core, and bucket each by:
    WALKED   its last position mutation was a d^2<=1 step with NO launcher of
             either team within d^2<=2 of its pre-move tile
    WALKED?  same, but a launcher WAS in pickup range (cannot be separated from
             a 1-tile throw)
    THROWN   its last position mutation was d^2>=2 (a launcher throw)
    SPAWNED  it has not moved since the core spawned it there
and by what it stands on:
    own conveyor / enemy conveyor / bare tile / (impassable = decoder alarm)
"""
from __future__ import annotations
import sys, json, argparse, collections
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import fields, parse_entity, read_pos, parse_update_hp  # noqa: E402

BUILDINGS = {"conveyor", "splitter", "harvester", "barrier",
             "gunner", "sentinel", "launcher", "core"}
CONV = {"conveyor", "splitter"}
HEAL = (1, 2, 3, 4)


def ring(corepos):
    x, y = corepos
    fp = {(x + a, y + b) for a in (0, 1) for b in (0, 1)}
    out = set()
    for (cx, cy) in fp:
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            t = (cx + dx, cy + dy)
            if t not in fp:
                out.add(t)
    return out


def walk(path):
    data = Path(path).read_bytes()
    turn_bufs = []
    map_buf = None
    for num, wire, val in fields(data):
        if num == 1 and wire == 2:
            map_buf = val
        elif num == 3 and wire == 2:
            turn_bufs.append(val)
    occ, tiles_of, bots, ent = {}, {}, {}, {}
    launchers, cores = set(), {}
    # Cores are declared in the MAP (field 4), not by placeEntity.
    if map_buf is not None:
        for mn, mw, mv in fields(map_buf):
            if mn != 4 or mw != 2:
                continue
            cid = cteam = 0; cpos = None
            for cn, cw, cv in fields(mv):
                if cn == 1: cid = cv
                elif cn == 2: cteam = cv
                elif cn == 3: cpos = read_pos(cv)
            if cpos is not None:
                cores[cid] = (cteam, cpos)
                ts = [(cpos[0]+a, cpos[1]+b) for a in (0,1) for b in (0,1)]
                for t in ts: occ[t] = ("core", cteam)
                tiles_of[cid] = ts
                ent[cid] = ("core", cteam)
    arrival = {}          # bot id -> mode
    res = collections.Counter()
    for rnd, tb in enumerate(turn_bufs):
        for _n, _w, ub in fields(tb):
            for unum, _uw, u in fields(ub):
                if unum == 1:
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
                                arrival[e.id] = "SPAWNED"
                            bots[e.id] = [e.team, e.pos]
                        elif e.kind in BUILDINGS:
                            for t in tiles_of.pop(e.id, []):
                                occ.pop(t, None); launchers.discard(t)
                            ts = ([(e.pos[0] + a, e.pos[1] + b) for a in (0, 1) for b in (0, 1)]
                                  if e.kind == "core" else [e.pos])
                            for t in ts:
                                occ[t] = (e.kind, e.team)
                            tiles_of[e.id] = ts
                            if e.kind == "launcher":
                                launchers.add(e.pos)
                            if e.kind == "core":
                                cores[e.id] = (e.team, e.pos)
                elif unum == 2:
                    eid = to = None
                    for mn, _mw, mv in fields(u):
                        if mn == 1: eid = mv
                        elif mn == 2: to = read_pos(mv)
                    b = bots.get(eid)
                    if b is None or to is None:
                        continue
                    fx, fy = b[1]
                    d2 = (to[0]-fx)**2 + (to[1]-fy)**2
                    if d2 >= 2:
                        arrival[eid] = "THROWN"
                    else:
                        near = any((lx-fx)**2+(ly-fy)**2 <= 2 for (lx, ly) in launchers)
                        arrival[eid] = "WALKED?" if near else "WALKED"
                    b[1] = to
                elif unum == 3:
                    for rn, _rw, rv in fields(u):
                        if rn != 1: continue
                        bots.pop(rv, None); arrival.pop(rv, None)
                        cores.pop(rv, None)
                        for t in tiles_of.pop(rv, []):
                            occ.pop(t, None); launchers.discard(t)
                elif unum == 5:
                    try:
                        eid, delta = parse_update_hp(u)
                    except Exception:
                        continue
                    if delta not in HEAL or eid not in cores:
                        continue
                    cteam, cpos = cores[eid]
                    seats = ring(cpos)
                    for bid, (bteam, bpos) in list(bots.items()):
                        if bteam != cteam or bpos not in seats:
                            continue
                        e = occ.get(bpos)
                        if e is None:
                            stand = "bare_tile"
                        elif e[0] in CONV:
                            stand = f"{'own' if e[1] == bteam else 'enemy'}_conveyor"
                        else:
                            stand = f"ALARM_{e[0]}"
                        res[(stand, arrival.get(bid, "UNKNOWN"))] += 1
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    ps = sorted(Path(a.dir).glob("*.replay26"))
    if a.limit: ps = ps[:a.limit]
    tot = collections.Counter()
    for p in ps:
        try:
            tot += walk(p)
        except Exception as ex:
            print("ERR", p.name, ex, file=sys.stderr)
    stands = sorted({k[0] for k in tot})
    modes = ["WALKED", "WALKED?", "THROWN", "SPAWNED", "UNKNOWN"]
    print(f"files={len(ps)}  total core-heal x ring-body observations={sum(tot.values())}")
    print(f"{'standing on':18} " + " ".join(f"{m:>9}" for m in modes) + f" {'total':>9}")
    for s in stands:
        row = [tot[(s, m)] for m in modes]
        print(f"{s:18} " + " ".join(f"{v:9}" for v in row) + f" {sum(row):9}")


if __name__ == "__main__":
    main()
