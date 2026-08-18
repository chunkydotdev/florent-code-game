#!/usr/bin/env python3
"""s51 closure autopsy -- hypotheses (e) FERRY-AS-EVICTOR and (f) RAIDER GAPS.

(e)  `siege.py:1819` counts ANY of our launchers inside `FS_RING_DSQ` of the
     enemy core as the live evictor, so a FERRY launcher that happened to land
     in-ring (`_fs_launcher_turn:2182` re-roles it eviction-only, forever)
     permanently suppresses the rung-2 purchase.  A ferry launcher is sited by
     the HOP (a step toward the target), a rung-2 evictor by healer-observation
     COVERAGE.  This tool measures the difference in the only currency that
     matters: which of the enemy core's 8 orthogonal heal SEATS fall inside the
     launcher's pickup envelope (d^2 <= 2).

     Emitted per in-ring launcher of ours:
       birth/death round, position, seats_covered, ring_covered,
       body_seat_rounds_covered (enemy-body-on-seat rounds inside its envelope
       during its life), and the counterfactual BEST siting: the maximum the
       same quantities reach over every tile inside the evictor build envelope
       (dsq_core <= FS_RING_DSQ), i.e. what a purpose-sited rung-2 evictor
       could have reached from the same map position.

     Throws are classified from `FS EVICT <r> from (x,y) to (x,y)`:
       ON_SEAT   the victim stood on one of the 8 orthogonal heal seats
       ON_RING   on a core corner (diagonal ring tile)
       OFF_RING  anywhere else inside the pickup envelope

(f)  RAIDER GAPS: rounds between first and last at-ring round with NO FS DL
     line at all -- no live body at the ring.  Reported with the seat-state
     delta across each gap (seats denied before vs after).

Writes ferry_launchers.tsv, ferry_throws.tsv, gaps.tsv.
"""
from __future__ import annotations

import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import fields, parse_entity, read_pos  # noqa: E402
from map_encode import parse_map26  # noqa: E402
from closure import read_log  # noqa: E402

LOGS = ROOT / "scratchpad/s51_evict_autopsy/logs"
FS_RING_DSQ = 8
PICKUP_DSQ = 2
BLOCKING = {"barrier", "harvester", "gunner", "sentinel", "launcher", "core"}
BUILDINGS = BLOCKING | {"conveyor", "splitter"}


def dsq_core(p, o):
    dx = abs(p[0] - o[0])
    dx = dx - 1 if dx > 1 else (0 if p[0] in (o[0], o[0] + 1) else dx)
    dy = abs(p[1] - o[1])
    dy = dy - 1 if dy > 1 else (0 if p[1] in (o[1], o[1] + 1) else dy)
    return dx * dx + dy * dy


def geom(mapname, seat):
    w, h, rows, cores = parse_map26(ROOT / "maps" / f"{mapname}.map26")
    an = {c[0]: (c[1], c[2]) for c in cores}
    ours = 0 if seat == "A" else 1
    ox, oy = an[1 - ours]
    seats = [(ox, oy - 1), (ox + 1, oy - 1), (ox + 2, oy), (ox + 2, oy + 1),
             (ox + 1, oy + 2), (ox, oy + 2), (ox - 1, oy + 1), (ox - 1, oy)]
    corners = [(ox - 1, oy - 1), (ox + 2, oy - 1), (ox - 1, oy + 2),
               (ox + 2, oy + 2)]
    ok = lambda t: (0 <= t[0] < w and 0 <= t[1] < h  # noqa: E731
                    and rows[t[1]][t[0]] != 1)
    return (w, h, rows, ours, (ox, oy),
            [t for t in seats if ok(t)], [t for t in corners if ok(t)])


def walk(replay, ourteam):
    data = Path(replay).read_bytes()
    mb, turns = None, []
    for n, wt, v in fields(data):
        if n == 1 and wt == 2:
            mb = v
        elif n == 3 and wt == 2:
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
                    ents[cid] = ["core", team, pos, 0]
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
                            ents[e.id] = [e.kind, e.team, e.pos, rnd]
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
        yield rnd, {k: tuple(v) for k, v in ents.items()}


def main():
    lrows, trows, grows = [], [], []
    for errp in sorted(LOGS.glob("v513_log-*.err")):
        game = errp.stem
        _, mapname, _sd, seat = game.split("-")
        w, h, rows, ourteam, E, seats, corners = geom(mapname, seat)
        seatset, cornset = set(seats), set(corners)
        log = read_log(errp)
        dl = log["dl"]
        if not dl:
            continue

        # ---- full state walk -------------------------------------------------
        launchers = {}                       # eid -> dict
        body_seat = defaultdict(set)         # round -> set of seats w/ enemy body
        denied = {}                          # round -> set of denied seats
        for rnd, ents in walk(LOGS / f"{game}.replay26", ourteam):
            occ = {}
            for eid, (k, t, p, br) in ents.items():
                if k == "core":
                    for dx in (0, 1):
                        for dy in (0, 1):
                            occ[(p[0] + dx, p[1] + dy)] = (k, t)
                else:
                    prev = occ.get(p)
                    if prev is None or (k in BUILDINGS
                                        and prev[0] not in BUILDINGS):
                        occ[p] = (k, t)
                if k == "launcher" and t == ourteam:
                    d = launchers.get(eid)
                    if d is None:
                        launchers[eid] = dict(eid=eid, pos=p, birth=br,
                                              last=rnd, in_ring=dsq_core(p, E)
                                              <= FS_RING_DSQ)
                    else:
                        d["last"] = rnd
            bs = set()
            dn = set()
            for s in seats:
                o = occ.get(s)
                if o is None:
                    continue
                if o[1] != ourteam and o[0] == "builder_bot":
                    bs.add(s)
                if o[1] == ourteam and (o[0] in BLOCKING
                                        or o[0] == "builder_bot"):
                    dn.add(s)
            body_seat[rnd] = bs
            denied[rnd] = dn

        # ---- (e) launcher siting --------------------------------------------
        # counterfactual envelope: every tile a rung-2 evictor could be built on
        env = [(x, y) for x in range(w) for y in range(h)
               if rows[y][x] != 1 and dsq_core((x, y), E) <= FS_RING_DSQ
               and (x, y) != E]
        best_seats = max((sum(1 for s in seats
                              if (t[0] - s[0]) ** 2 + (t[1] - s[1]) ** 2
                              <= PICKUP_DSQ) for t in env), default=0)
        evictor_pos = {(x, y) for _r, x, y, _c in log["evictors"]}
        for eid, d in sorted(launchers.items(), key=lambda kv: kv[1]["birth"]):
            if not d["in_ring"]:
                continue
            p = d["pos"]
            cov_s = [s for s in seats
                     if (p[0] - s[0]) ** 2 + (p[1] - s[1]) ** 2 <= PICKUP_DSQ]
            cov_c = [c for c in corners
                     if (p[0] - c[0]) ** 2 + (p[1] - c[1]) ** 2 <= PICKUP_DSQ]
            life = range(d["birth"], d["last"] + 1)
            # ⛔ THE DENOMINATOR THAT MATTERS IS THE AT-RING WINDOW.  Enemy
            # bodies parking on their own seats after our raider is dead cost
            # nothing -- there is no collar left to block.
            atring = set(dl) & set(life)
            bsr = sum(len(body_seat.get(r, ()) & set(cov_s)) for r in life)
            bsr_all = sum(len(body_seat.get(r, ())) for r in life)
            bsr_ring = sum(len(body_seat.get(r, ()) & set(cov_s))
                           for r in atring)
            bsr_ring_all = sum(len(body_seat.get(r, ())) for r in atring)
            # counterfactual over the same life window
            best_bsr = max((sum(len(body_seat.get(r, ())
                                    & {s for s in seats
                                       if (t[0] - s[0]) ** 2
                                       + (t[1] - s[1]) ** 2 <= PICKUP_DSQ})
                                for r in life) for t in env), default=0)
            best_bsr_ring = max((sum(len(body_seat.get(r, ())
                                         & {s for s in seats
                                            if (t[0] - s[0]) ** 2
                                            + (t[1] - s[1]) ** 2 <= PICKUP_DSQ})
                                     for r in atring) for t in env), default=0)
            lrows.append(dict(
                game=game, map=mapname, eid=eid, pos=f"{p[0]},{p[1]}",
                birth=d["birth"], last=d["last"], life=d["last"] - d["birth"] + 1,
                origin="rung2" if p in evictor_pos else "ferry",
                seats_covered=len(cov_s), corners_covered=len(cov_c),
                best_seats_any_site=best_seats,
                body_seat_rounds_covered=bsr,
                body_seat_rounds_total=bsr_all,
                body_seat_rounds_best_site=best_bsr,
                atring_bodyseat_covered=bsr_ring,
                atring_bodyseat_total=bsr_ring_all,
                atring_bodyseat_best_site=best_bsr_ring))

        # ---- (e) throw classification ---------------------------------------
        cls = Counter()
        for r, fx, fy, tx, ty in log["evicts"]:
            f = (fx, fy)
            k = ("ON_SEAT" if f in seatset else
                 "ON_CORNER" if f in cornset else "OFF_RING")
            cls[k] += 1
            trows.append(dict(game=game, map=mapname, round=r,
                              frm=f"{fx},{fy}", to=f"{tx},{ty}", cls=k,
                              throw_dsq_from_core=dsq_core(f, E)))

        # ---- (f) raider gaps -------------------------------------------------
        rr = sorted(dl)
        first, last = rr[0], rr[-1]
        present = set(rr)
        gaps = []
        run = None
        for r in range(first, last + 1):
            if r in present:
                if run is not None:
                    gaps.append(run)
                    run = None
            else:
                run = (run[0], r) if run else (r, r)
        if run:
            gaps.append(run)
        gap_rounds = sum(b - a + 1 for a, b in gaps)
        reopened = 0
        for a, b in gaps:
            before = denied.get(a - 1, set())
            after = denied.get(b + 1, set())
            reopened += len(before - after)
        grows.append(dict(game=game, map=mapname, arrive_r=first,
                          last_ring_r=last, ring_rounds=len(rr),
                          span=last - first + 1, n_gaps=len(gaps),
                          gap_rounds=gap_rounds,
                          longest_gap=max((b - a + 1 for a, b in gaps),
                                          default=0),
                          seats_lost_across_gaps=reopened,
                          throws_on_seat=cls["ON_SEAT"],
                          throws_on_corner=cls["ON_CORNER"],
                          throws_off_ring=cls["OFF_RING"]))

    for name, rows in (("ferry_launchers.tsv", lrows),
                       ("ferry_throws.tsv", trows), ("gaps.tsv", grows)):
        if not rows:
            print(f"{name}: EMPTY")
            continue
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
