#!/usr/bin/env python3
"""s51 closure autopsy -- THE RESIDUAL SET.

Closure is an AND over 8 seats, so a share-of-open-seat-rounds table is the
wrong denominator: it is dominated by the early rounds when 8 seats are open.
What blocks closure is the LAST seat.  This tool answers, per game:

  * per-seat: how the seat spent the at-ring rounds, WITH the kind and owner
    of whatever building sat on it, and whether that building predates our
    arrival at the ring;
  * the RESIDUAL SET: the seats still open in the rounds where the collar was
    at its tightest (orth == min_orth), and what occupied them;
  * a per-seat closure verdict: EVER-DENIED / NEVER-DENIED, and if
    never-denied, the dominant occupant.

Writes residual_seatlife.tsv and residual_set.tsv into this directory.
"""
from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import fields, parse_entity, read_pos  # noqa: E402
from map_encode import parse_map26  # noqa: E402

LOGS = ROOT / "scratchpad/s51_evict_autopsy/logs"
BLOCKING = {"barrier", "harvester", "gunner", "sentinel", "launcher", "core"}
BUILDINGS = BLOCKING | {"conveyor", "splitter"}
DLRX = re.compile(r"^FS DL (\d+) ")


def ring_of(mapname, seat):
    w, h, rows, cores = parse_map26(ROOT / "maps" / f"{mapname}.map26")
    anchors = {c[0]: (c[1], c[2]) for c in cores}
    ours = 0 if seat == "A" else 1
    ox, oy = anchors[1 - ours]
    seats = [(ox, oy - 1), (ox + 1, oy - 1), (ox + 2, oy), (ox + 2, oy + 1),
             (ox + 1, oy + 2), (ox, oy + 2), (ox - 1, oy + 1), (ox - 1, oy)]
    seats = [t for t in seats if 0 <= t[0] < w and 0 <= t[1] < h
             and rows[t[1]][t[0]] != 1]
    return seats, ours


def walk(replay, seatlist, ourteam):
    """-> list of (round, {tile: (kind, team, built_round) or None})"""
    data = Path(replay).read_bytes()
    map_buf, turns = None, []
    for num, wire, val in fields(data):
        if num == 1 and wire == 2:
            map_buf = val
        elif num == 3 and wire == 2:
            turns.append(val)
    ents = {}
    if map_buf is not None:
        for mn, mw, mv in fields(map_buf):
            if mn == 5 and mw == 2:
                cid = team = 0
                pos = None
                for cn, cw, cv in fields(mv):
                    if cn == 1:
                        cid = cv
                    elif cn == 2:
                        team = cv
                    elif cn == 3 and cw == 2:
                        pos = read_pos(cv)
                if pos is not None:
                    ents[cid] = ["core", team, pos, 0]
    S = set(seatlist)
    out = []
    for rnd, tb in enumerate(turns):
        for _n, _w, ub0 in fields(tb):
            for unum, _uw, ub in fields(ub0):
                if unum == 1:
                    for en, _ew, eb in fields(ub):
                        if en != 1:
                            continue
                        e = parse_entity(eb, rnd)
                        if e is None:
                            continue
                        if e.id in ents:
                            ents[e.id][2] = e.pos      # rotation re-emit
                            ents[e.id][0] = e.kind
                        else:
                            ents[e.id] = [e.kind, e.team, e.pos, rnd]
                elif unum == 2:
                    eid = to = None
                    for mn, _mw, mv in fields(ub):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid in ents and to is not None:
                        ents[eid][2] = to
                elif unum == 3:
                    for rn, _rw, rv in fields(ub):
                        if rn == 1:
                            ents.pop(rv, None)
        snap = {}
        for eid, (kind, team, pos, br) in ents.items():
            if kind == "core":
                for dx in (0, 1):
                    for dy in (0, 1):
                        p = (pos[0] + dx, pos[1] + dy)
                        if p in S:
                            snap[p] = (kind, team, br, eid)
            elif pos in S:
                prev = snap.get(pos)
                # buildings win over bodies for the tile's identity
                if prev is None or (kind in BUILDINGS
                                    and prev[0] not in BUILDINGS):
                    snap[pos] = (kind, team, br, eid)
        out.append((rnd, snap))
    return out


def code_for(occ, ourteam):
    if occ is None:
        return "."
    kind, team, _br, _eid = occ
    if kind in BUILDINGS:
        if team == ourteam:
            return "D" if kind in BLOCKING else "o"
        return "E"
    return "d" if team == ourteam else "b"


def main():
    life_rows, res_rows = [], []
    for errp in sorted(LOGS.glob("v513_log-*.err")):
        game = errp.stem
        _, mapname, seedtag, seat = game.split("-")
        seats, ourteam = ring_of(mapname, seat)
        rings = set()
        with open(errp, errors="replace") as fh:
            for line in fh:
                m = DLRX.match(line)
                if m:
                    rings.add(int(m.group(1)))
        if not rings:
            continue
        arrive = min(rings)
        tapes = walk(LOGS / f"{game}.replay26", seats, ourteam)
        by = {r: s for r, s in tapes}

        rr = sorted(rings)
        per = {t: Counter() for t in seats}
        kinds = {t: Counter() for t in seats}
        pre = {t: 0 for t in seats}       # enemy bldg predating our arrival
        opens = {}
        for r in rr:
            snap = by.get(r - 1)
            if snap is None:
                continue
            codes = []
            for t in seats:
                c = code_for(snap.get(t), ourteam)
                per[t][c] += 1
                if c == "E":
                    k = snap[t][0]
                    kinds[t][k] += 1
                    if snap[t][2] < arrive:
                        pre[t] += 1
                codes.append(c)
            opens[r] = codes
        if not opens:
            continue
        mino = min(sum(1 for c in v if c not in "Dd") for v in opens.values())
        # residual set at the tightest rounds
        res = Counter()
        res_tiles = Counter()
        nmin = 0
        for r, codes in opens.items():
            if sum(1 for c in codes if c not in "Dd") != mino:
                continue
            nmin += 1
            for i, c in enumerate(codes):
                if c not in "Dd":
                    res[c] += 1
                    res_tiles[(seats[i], c)] += 1
        for t in seats:
            d = per[t]
            tot = sum(d.values())
            ever = d["D"] + d["d"] > 0
            dom = d.most_common(1)[0][0] if tot else "-"
            life_rows.append(dict(
                game=game, map=mapname, seat=seat, tile=f"{t[0]},{t[1]}",
                ring_rounds=tot, D=d["D"], d_body=d["d"], E=d["E"],
                b=d["b"], o=d["o"], empty=d["."],
                ever_denied=int(ever), dominant=dom,
                enemy_kinds=",".join(f"{k}:{v}" for k, v in
                                     kinds[t].most_common()) or "-",
                enemy_bldg_predates_arrival=pre[t]))
        res_rows.append(dict(
            game=game, map=mapname, seat=seat, arrive_r=arrive,
            ring_rounds=len(rr), min_orth=mino, rounds_at_min=nmin,
            residual_E=res["E"], residual_b=res["b"], residual_o=res["o"],
            residual_empty=res["."],
            residual_tiles=";".join(f"{t[0]},{t[1]}:{c}" for (t, c), n
                                    in res_tiles.most_common())))

    for name, rows in (("residual_seatlife.tsv", life_rows),
                       ("residual_set.tsv", res_rows)):
        cols = list(rows[0].keys())
        with open(HERE / name, "w") as fh:
            fh.write("\t".join(cols) + "\n")
            for r in rows:
                fh.write("\t".join(str(r[c]) for c in cols) + "\n")
        print(f"wrote {name} ({len(rows)} rows)")


if __name__ == "__main__":
    if "-h" in sys.argv[1:] or "--help" in sys.argv[1:]:
        print(__doc__)
        raise SystemExit(0)
    main()
