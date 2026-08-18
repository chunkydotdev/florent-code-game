#!/usr/bin/env python3
"""s51 closure autopsy -- BUILD OPPORTUNITY on open orthogonal seats.

Separates "the collar could not be closed" from "the collar was not closed".
For every at-ring round (a FS DL line exists) and every OPEN orthogonal seat of
the enemy core, classifies the seat-round on two independent axes read off the
replay tape and the DL record:

  BUILDABLE   the seat is EMPTY (no building of either team, no body)
  ADJACENT    at least one of OUR builder bots is orthogonally adjacent to it
              (manhattan == 1) -- i.e. a barrier could legally have been placed
              that round by that body
  FUNDED      ti >= barrier cost that round
  GATED       ti < len(needed)*bar + FS_SEAL_MARGIN  (the binary seal gate)

Emits opportunity.tsv (per game) and opportunity_seat.tsv (per game x seat).

Columns of interest
  osr                    open seat-rounds
  b_adj_fund             BUILDABLE & ADJACENT & FUNDED  -- a build was legally
                         available and did not happen: the gate or the
                         one-action-per-turn budget ate it
  b_adj_fund_gateopen    ...and the binary seal gate was also open
  b_noadj                BUILDABLE but no body adjacent -- a WALK problem
  notbuildable           occupied by a building/body (see residual.py for who)
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import fields, parse_entity, read_pos  # noqa: E402
from map_encode import parse_map26  # noqa: E402
from closure import read_log  # noqa: E402

LOGS = ROOT / "scratchpad/s51_evict_autopsy/logs"
BLOCKING = {"barrier", "harvester", "gunner", "sentinel", "launcher", "core"}
BUILDINGS = BLOCKING | {"conveyor", "splitter"}
FS_SEAL_MARGIN = 6


def ring_of(mapname, seat):
    w, h, rows, cores = parse_map26(ROOT / "maps" / f"{mapname}.map26")
    anchors = {c[0]: (c[1], c[2]) for c in cores}
    ours = 0 if seat == "A" else 1
    ox, oy = anchors[1 - ours]
    seats = [(ox, oy - 1), (ox + 1, oy - 1), (ox + 2, oy), (ox + 2, oy + 1),
             (ox + 1, oy + 2), (ox, oy + 2), (ox - 1, oy + 1), (ox - 1, oy)]
    return [t for t in seats if 0 <= t[0] < w and 0 <= t[1] < h
            and rows[t[1]][t[0]] != 1], ours


def walk(replay, ourteam):
    """yield (round, occ dict tile->(kind,team), our_bot_positions set)"""
    data = Path(replay).read_bytes()
    mb, turns = None, []
    for n, w, v in fields(data):
        if n == 1 and w == 2:
            mb = v
        elif n == 3 and w == 2:
            turns.append(v)
    ents = {}
    if mb is not None:
        for mn, mw, mv in fields(mb):
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
                    ents[cid] = ["core", team, pos]
    for rnd, tb in enumerate(turns):
        for _n, _w, u0 in fields(tb):
            for un, _uw, ub in fields(u0):
                if un == 1:
                    for en, _ew, eb in fields(ub):
                        if en != 1:
                            continue
                        e = parse_entity(eb, rnd)
                        if e is None:
                            continue
                        if e.id in ents:
                            ents[e.id][2] = e.pos
                            ents[e.id][0] = e.kind
                        else:
                            ents[e.id] = [e.kind, e.team, e.pos]
                elif un == 2:
                    eid = to = None
                    for mn, _mw, mv in fields(ub):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid in ents and to is not None:
                        ents[eid][2] = to
                elif un == 3:
                    for rn, _rw, rv in fields(ub):
                        if rn == 1:
                            ents.pop(rv, None)
        occ = {}
        bots = set()
        for eid, (k, t, p) in ents.items():
            if k == "core":
                for dx in (0, 1):
                    for dy in (0, 1):
                        occ[(p[0] + dx, p[1] + dy)] = (k, t)
            else:
                prev = occ.get(p)
                if prev is None or (k in BUILDINGS and prev[0] not in BUILDINGS):
                    occ[p] = (k, t)
                if k == "builder_bot" and t == ourteam:
                    bots.add(p)
        yield rnd, occ, bots


def main():
    grows, srows = [], []
    for errp in sorted(LOGS.glob("v513_log-*.err")):
        game = errp.stem
        _, mapname, _seed, seat = game.split("-")
        seats, ourteam = ring_of(mapname, seat)
        log = read_log(errp)
        dl = log["dl"]
        if not dl:
            continue
        snaps = {r: (o, b) for r, o, b in
                 walk(LOGS / f"{game}.replay26", ourteam)}
        c = defaultdict(int)
        per = {t: defaultdict(int) for t in seats}
        for r in sorted(dl):
            prev = snaps.get(r - 1)
            if prev is None:
                continue
            occ, bots = prev
            rec = dl[r]
            bar = rec["bar"] or 3
            funded = rec["ti"] >= bar
            gate_open = rec["ti"] >= rec["need"] * bar + FS_SEAL_MARGIN
            for t in seats:
                o = occ.get(t)
                if o is not None and o[1] == ourteam and o[0] in BLOCKING:
                    continue                       # denied by our building
                if o is not None and o[0] == "builder_bot" and o[1] == ourteam:
                    continue                       # denied by our body
                c["osr"] += 1
                per[t]["osr"] += 1
                buildable = o is None
                adj = any(abs(t[0] - b[0]) + abs(t[1] - b[1]) == 1
                          for b in bots)
                if not buildable:
                    c["notbuildable"] += 1
                    per[t]["notbuildable"] += 1
                    continue
                if not adj:
                    c["b_noadj"] += 1
                    per[t]["b_noadj"] += 1
                    continue
                if not funded:
                    c["b_adj_nofund"] += 1
                    per[t]["b_adj_nofund"] += 1
                    continue
                c["b_adj_fund"] += 1
                per[t]["b_adj_fund"] += 1
                if gate_open:
                    c["b_adj_fund_gateopen"] += 1
                    per[t]["b_adj_fund_gateopen"] += 1
        keys = ["osr", "notbuildable", "b_noadj", "b_adj_nofund",
                "b_adj_fund", "b_adj_fund_gateopen"]
        grows.append(dict(game=game, map=mapname,
                          **{k: c.get(k, 0) for k in keys}))
        for t in seats:
            srows.append(dict(game=game, map=mapname, tile=f"{t[0]},{t[1]}",
                              **{k: per[t].get(k, 0) for k in keys}))
    for name, rows in (("opportunity.tsv", grows),
                       ("opportunity_seat.tsv", srows)):
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
