#!/usr/bin/env python3
"""s51 closure autopsy -- per-round occupancy tape of the ENEMY core's ring.

Replays a local `.replay26` turn stream and, at END OF EACH ROUND, records the
occupant of each of the 8 orthogonal heal seats (and the 4 corners) of the
opponent's core, from OUR point of view.

State code per seat (mirrors `siege._fs_denied` / `can_build_barrier`):
    D  our BLOCKING building (barrier/harvester/gunner/sentinel/launcher/core)
       -> DENIED, seat closed
    d  our builder BODY standing on it -> DENIED, seat closed
    o  our NON-blocking building (conveyor/splitter)
       -> counted OPEN by _fs_denied AND unbuildable.  self-inflicted.
    E  ENEMY building of any kind -> counted OPEN and unbuildable
    b  ENEMY builder body -> counted OPEN and unbuildable this round
    .  empty -> OPEN and buildable

orth_open(tape) = count of seats whose code is not in {D, d}.
buildable(tape) = count of seats whose code == '.'

Emits (stdout, TSV): game round seatcode8 orth_open n_enemy_bldg n_enemy_body
                     n_our_bldg n_empty n_ourconv per-seat detail columns.

Usage: seattape.py <replay26> <map> <ourseat A|B> [--game NAME]
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import fields, parse_entity, read_pos, Replay  # noqa: E402
from map_encode import parse_map26  # noqa: E402

BLOCKING = {"barrier", "harvester", "gunner", "sentinel", "launcher", "core"}
BUILDINGS = {"barrier", "harvester", "gunner", "sentinel", "launcher", "core",
             "conveyor", "splitter"}


def ring_tiles(ox, oy, mw, mh):
    seats = [(ox, oy - 1), (ox + 1, oy - 1), (ox + 2, oy), (ox + 2, oy + 1),
             (ox + 1, oy + 2), (ox, oy + 2), (ox - 1, oy + 1), (ox - 1, oy)]
    corners = [(ox - 1, oy - 1), (ox + 2, oy - 1), (ox - 1, oy + 2),
               (ox + 2, oy + 2)]
    inb = lambda t: 0 <= t[0] < mw and 0 <= t[1] < mh  # noqa: E731
    return [t for t in seats if inb(t)], [t for t in corners if inb(t)]


def tape(replay_path, mapname, ourseat):
    w, h, rows, cores = parse_map26(ROOT / "maps" / f"{mapname}.map26")
    anchors = {c[0]: (c[1], c[2]) for c in cores}
    ourteam = 0 if ourseat == "A" else 1
    enemyteam = 1 - ourteam
    ox, oy = anchors[enemyteam]
    seats, corners = ring_tiles(ox, oy, w, h)
    # wall filter, exactly as _fs_ring12
    seats = [t for t in seats if rows[t[1]][t[0]] != 1]
    corners = [t for t in corners if rows[t[1]][t[0]] != 1]

    rp = Replay(replay_path, track_flow=False, parse_only=True) \
        if False else None
    # -- do our own turn walk so we can snapshot every round ------------------
    data = Path(replay_path).read_bytes()
    turn_bufs = []
    map_buf = None
    for num, wire, val in fields(data):
        if num == 1 and wire == 2:
            map_buf = val
        elif num == 3 and wire == 2:
            turn_bufs.append(val)
    ents = {}
    for c in cores:
        # core id unknown from map26; seed from replay map message
        pass
    # seed cores from the replay's own map message (has ids)
    if map_buf is not None:
        for mnum, mwire, mval in fields(map_buf):
            if mnum == 5 and mwire == 2:      # CorePosition
                cid = team = 0
                pos = None
                for cn, cw, cv in fields(mval):
                    if cn == 1:
                        cid = cv
                    elif cn == 2:
                        team = cv
                    elif cn == 3 and cw == 2:
                        pos = read_pos(cv)
                if pos is not None:
                    ents[cid] = ("core", team, pos)

    out = []
    allt = seats + corners
    for rnd, tb in enumerate(turn_bufs):
        for _n, _w, ubuf in fields(tb):
            for unum, _uw, ub in fields(ubuf):
                if unum == 1:                                   # placeEntity
                    for en, _ew, eb in fields(ub):
                        if en != 1:
                            continue
                        e = parse_entity(eb, rnd)
                        if e is None:
                            continue
                        ents[e.id] = (e.kind, e.team, e.pos)
                elif unum == 2:                                 # moveBuilderBot
                    eid = to = None
                    for mn, _mw, mv in fields(ub):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid in ents and to is not None:
                        k, t, _p = ents[eid]
                        ents[eid] = (k, t, to)
                elif unum == 3:                                 # removeEntity
                    for rn, _rw, rv in fields(ub):
                        if rn == 1:
                            ents.pop(rv, None)
        # snapshot
        occ = {}
        for eid, (kind, team, pos) in ents.items():
            if kind == "core":
                for dx in (0, 1):
                    for dy in (0, 1):
                        occ.setdefault((pos[0] + dx, pos[1] + dy), []).append(
                            (kind, team))
            else:
                occ.setdefault(pos, []).append((kind, team))
        codes = []
        for t in allt:
            here = occ.get(t, [])
            c = "."
            # buildings first (a tile holds at most one building)
            bld = [x for x in here if x[0] in BUILDINGS]
            bots = [x for x in here if x[0] == "builder_bot"]
            if bld:
                kind, team = bld[0]
                if team == ourteam:
                    c = "D" if kind in BLOCKING else "o"
                else:
                    c = "E"
            elif bots:
                c = "d" if bots[0][1] == ourteam else "b"
            codes.append(c)
        s = "".join(codes[:len(seats)])
        out.append((rnd, s, "".join(codes[len(seats):])))
    return seats, corners, out


def main():
    ap = sys.argv[1:]
    if not ap or "-h" in ap or "--help" in ap:
        print(__doc__)
        raise SystemExit(0)
    replay, mapname, seat = ap[0], ap[1], ap[2]
    game = ap[4] if len(ap) > 4 and ap[3] == "--game" else Path(replay).stem
    seats, corners, rows = tape(replay, mapname, seat)
    print("# seats " + " ".join(f"{x},{y}" for x, y in seats))
    print("game\tround\tseatcode\tdiagcode\torth_open\tn_enemy_bldg\t"
          "n_enemy_body\tn_our_conv\tn_empty")
    for rnd, s, dcode in rows:
        oo = sum(1 for c in s if c not in "Dd")
        print(f"{game}\t{rnd}\t{s}\t{dcode}\t{oo}\t{s.count('E')}\t"
              f"{s.count('b')}\t{s.count('o')}\t{s.count('.')}")


if __name__ == "__main__":
    main()
