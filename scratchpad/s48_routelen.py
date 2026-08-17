#!/usr/bin/env python3
"""M3's own one-game demo: the BFS ROUTE LENGTH of each harvester, measured at
the round it was BUILT, by ordinal.

The study's demo for LOKI-ROUTESCORE is "the arm's harvesters #3-#6 must have
strictly lower median BFS route length than the parent's on the same map and
seed". Connect RATE and connect LATENCY are downstream of that number; this
reads the number itself.

Route length is the shortest path from the harvester tile to a tile
orthogonally beside its own Core footprint, over the terrain as the bot's own
`_link_path` sees it: walls blocked, OTHER ore blocked (a conveyor on ore costs
that harvester site, and `_link_path` blocks every ore except the start),
non-belt buildings blocked, own-Core footprint blocked. Reading it off the
replay rather than off the bot means it is the same metric for the arm and for
the control, computed by code neither of them runs.

Usage: python3 scratchpad/s48_routelen.py <replay...>  [--seat A|B]
"""
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import fields, read_pos, packed_varints, parse_entity  # noqa: E402

CARD = ((0, -1), (1, 0), (0, 1), (-1, 0))
BELT = ("conveyor", "splitter", "harvester")


def route_len(hx, hy, w, h, walls, ores, blocked, core_tiles):
    goals = set()
    for (cx, cy) in core_tiles:
        for dx, dy in CARD:
            t = (cx + dx, cy + dy)
            if t in core_tiles or not (0 <= t[0] < w and 0 <= t[1] < h):
                continue
            goals.add(t)
    if (hx, hy) in goals:
        return 0
    seen = {(hx, hy)}
    q = deque([((hx, hy), 0)])
    while q:
        (x, y), d = q.popleft()
        for dx, dy in CARD:
            t = (x + dx, y + dy)
            if t in seen or not (0 <= t[0] < w and 0 <= t[1] < h):
                continue
            if t in goals:
                return d          # d tiles of belt between harvester and ring
            if t in walls or t in ores or t in core_tiles or t in blocked:
                continue
            seen.add(t)
            q.append((t, d + 1))
    return None


def scan(path):
    data = Path(path).read_bytes()
    map_buf, turns = None, []
    for num, wire, val in fields(data):
        if num == 1 and wire == 2:
            map_buf = val
        elif num == 3 and wire == 2:
            turns.append(val)
    w = h = 0
    rows, cores = [], []
    for num, wire, val in fields(map_buf):
        if num == 1:
            w = val
        elif num == 2:
            h = val
        elif num == 3 and wire == 2:
            for rn, rw, rv in fields(val):
                if rn == 1:
                    rows.append(packed_varints(rv))
        elif num == 4 and wire == 2:
            d = {}
            for cn, cw, cv in fields(val):
                if cn == 1:
                    d["id"] = cv
                elif cn == 2:
                    d["team"] = cv
                elif cn == 3:
                    d["pos"] = read_pos(cv)
            d.setdefault("team", 0)
            cores.append(d)
    walls = {(x, y) for y, r in enumerate(rows) for x, v in enumerate(r) if v == 1}
    ores = {(x, y) for y, r in enumerate(rows) for x, v in enumerate(r) if v == 2}
    ct = {}
    for c in cores:
        x, y = c["pos"]
        ct[c["team"]] = {(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)}

    ent = {}                       # id -> (team, kind, pos)
    blockers = {0: {}, 1: {}}      # team -> {pos: kind} non-belt buildings
    out = {0: [], 1: []}
    for rnd, tb in enumerate(turns):
        for _n, _wi, ub in fields(tb):
            for un, _uw, uv in fields(ub):
                if un == 1:
                    for en, _ew, eb in fields(uv):
                        if en != 1:
                            continue
                        e = parse_entity(eb, rnd)
                        if e is None:
                            continue
                        new = e.id not in ent
                        ent[e.id] = (e.team, e.kind, e.pos)
                        if e.kind not in BELT and e.kind != "builder_bot" and e.kind != "core":
                            for t in (0, 1):
                                blockers[t][e.pos] = e.kind
                        if new and e.kind == "harvester":
                            blk = dict(blockers[e.team])
                            blk.pop(e.pos, None)
                            L = route_len(e.pos[0], e.pos[1], w, h, walls,
                                          ores - {e.pos}, set(blk), ct.get(e.team, set()))
                            out[e.team].append((rnd, L))
                elif un == 3:
                    for rn, _rw, rv in fields(uv):
                        if rn != 1:
                            continue
                        v = ent.pop(rv, None)
                        if v is not None:
                            for t in (0, 1):
                                blockers[t].pop(v[2], None)
    return out


def med(xs):
    xs = sorted(x for x in xs if x is not None)
    return xs[len(xs) // 2] if xs else None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    seat = "A"
    for a in sys.argv[1:]:
        if a.startswith("--seat"):
            seat = a.split("=")[-1][-1].upper()
    t = 0 if seat == "A" else 1
    all36, allall = [], []
    for p in args:
        hs = scan(p)[t]
        l36 = [L for i, (r, L) in enumerate(hs) if 2 <= i <= 5]
        all36 += l36
        allall += [L for _, L in hs]
        print(f"{Path(p).name:34s} n={len(hs):3d} "
              f"median_L_all={med([L for _, L in hs])} median_L_#3-#6={med(l36)} "
              f"unroutable={sum(1 for _, L in hs if L is None)}")
    print(f"POOLED seat {seat}: n={len(allall)} median_L_all={med(allall)} "
          f"n_#3-#6={len(all36)} median_L_#3-#6={med(all36)}")


if __name__ == "__main__":
    main()
