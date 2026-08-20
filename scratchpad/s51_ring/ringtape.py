#!/usr/bin/env python3
"""s51 RING-ENGAGEMENT tape -- per-round occupancy of MJOLNIR'S OWN 8 core sockets.

Walks a local `.replay26` turn stream and, at END OF EACH ROUND, records who
occupies each of the 8 orthogonal tiles of the OPPONENT'S (Mjolnir's) core --
i.e. THEIR ring sockets, the tiles x3r0's RING-CLAIM arm claims for itself.

This is deliberately the MIRROR of scratchpad/s51_closure_autopsy/seattape.py:
that tool asks "how open is the enemy ring for OUR siege"; this one asks "how
much of their own ring have THEY claimed, with what, and when".  The socket
geometry helper is IMPORTED from seattape so the two cannot drift, and
`--crosscheck` asserts round-for-round agreement on the shared quantity.

Per socket, per round, one of:
    Mc  MJOLNIR conveyor/splitter   -- a RING-CLAIM (doctrine: conveyors only)
    Mb  MJOLNIR other building (barrier/harvester/turret/core)
    Md  MJOLNIR builder body standing on it (BODY BAN / SEATHOLD)
    Ob  OUR building  -- a BRICK on their socket (what EVICT-AND-REPLACE targets)
    Od  OUR builder body
    .   empty

Damage channel (UpdateHp, delta -2 == builder_attack) is resolved against a
never-popped id registry, so the killing peck on a brick is not lost.

Usage:
  ringtape.py --game <replay> <map> <ourseat A|B>          # per-round tape
  ringtape.py --batch <tsvfile> <repdir>                   # per-game aggregates
  ringtape.py --crosscheck <replay> <map> <ourseat>        # vs seattape.py
  ringtape.py --mutate <replay> <map> <ourseat>            # shifted-anchor control
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "scratchpad" / "s51_closure_autopsy"))
from replay_census import (  # noqa: E402
    fields, parse_entity, read_pos, parse_update_hp)
from map_encode import parse_map26  # noqa: E402
from seattape import ring_tiles  # noqa: E402  -- SHARED geometry, on purpose

CONV = {"conveyor", "splitter"}
BUILDINGS = {"barrier", "harvester", "gunner", "sentinel", "launcher", "core",
             "conveyor", "splitter"}
PECK = -2  # builder attack, from replay_census.DELTA_WEAPON


def walk(replay_path, mapname, ourseat, anchor_shift=(0, 0)):
    """Return (seats, rows, pecks, ends).

    rows  : list of (round, codes_tuple)
    pecks : list of (round, victim_team, victim_kind, seat_index) for delta -2
            events landing on an entity that is standing on one of the seats
    """
    w, h, mrows, cores = parse_map26(ROOT / "maps" / f"{mapname}.map26")
    anchors = {c[0]: (c[1], c[2]) for c in cores}
    ourteam = 0 if ourseat == "A" else 1
    mjteam = 1 - ourteam
    ox, oy = anchors[mjteam]
    ox += anchor_shift[0]
    oy += anchor_shift[1]
    seats, _corners = ring_tiles(ox, oy, w, h)
    seats = [t for t in seats if mrows[t[1]][t[0]] != 1]

    data = Path(replay_path).read_bytes()
    map_buf, turn_bufs = None, []
    for num, wire, val in fields(data):
        if num == 1 and wire == 2:
            map_buf = val
        elif num == 3 and wire == 2:
            turn_bufs.append(val)

    ents = {}          # live: id -> (kind, team, pos)
    ever = {}          # never popped: id -> (kind, team)
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
                    ever[cid] = ("core", team)

    seatset = {t: i for i, t in enumerate(seats)}
    # covariates for the trigger/gate conditions in x3r0's doctrine:
    #   RING_NEAR_DSQ = 16  -> "any enemy BUILDING within 4.0 of our core"
    #   RING_ECO_HARV = 2   -> the shell gate: ring opens past 2 harvesters
    coretiles = [(ox + dx, oy + dy) for dx in (0, 1) for dy in (0, 1)]
    dsq_core = lambda p: min((p[0] - cx) ** 2 + (p[1] - cy) ** 2  # noqa: E731
                             for cx, cy in coretiles)
    extra = {"our_near16_first": -1, "our_near36_first": -1,
             "mj_harv1": -1, "mj_harv2": -1, "mj_harv_n": 0}
    mj_harv_ids = set()
    rows, pecks = [], []
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
                        new = e.id not in ever
                        ents[e.id] = (e.kind, e.team, e.pos)
                        ever[e.id] = (e.kind, e.team)
                        if new and e.team == mjteam and e.kind == "harvester":
                            mj_harv_ids.add(e.id)
                            if extra["mj_harv1"] < 0:
                                extra["mj_harv1"] = rnd
                            if len(mj_harv_ids) == 2 and extra["mj_harv2"] < 0:
                                extra["mj_harv2"] = rnd
                        if (new and e.team == ourteam
                                and e.kind in BUILDINGS):
                            d = dsq_core(e.pos)
                            if d <= 16 and extra["our_near16_first"] < 0:
                                extra["our_near16_first"] = rnd
                            if d <= 36 and extra["our_near36_first"] < 0:
                                extra["our_near36_first"] = rnd
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
                elif unum == 5:                                 # UpdateHp
                    eid, delta = parse_update_hp(ub)
                    if delta != PECK:
                        continue
                    cur = ents.get(eid)
                    if cur is None:
                        continue
                    kind, team, pos = cur
                    si = seatset.get(pos)
                    if si is None:
                        continue
                    pecks.append((rnd, team, kind, si))
        occ = {}
        for eid, (kind, team, pos) in ents.items():
            if kind == "core":
                for dx in (0, 1):
                    for dy in (0, 1):
                        occ.setdefault((pos[0] + dx, pos[1] + dy),
                                       []).append((kind, team))
            else:
                occ.setdefault(pos, []).append((kind, team))
        codes = []
        for t in seats:
            here = occ.get(t, [])
            bld = [x for x in here if x[0] in BUILDINGS]
            bots = [x for x in here if x[0] == "builder_bot"]
            if bld:
                kind, team = bld[0]
                if team == mjteam:
                    c = "Mc" if kind in CONV else "Mb"
                else:
                    c = "Oc" if kind in CONV else "Ob"
            elif bots:
                c = "Md" if bots[0][1] == mjteam else "Od"
            else:
                c = "."
            codes.append(c)
        rows.append((rnd, tuple(codes)))
    extra["mj_harv_n"] = len(mj_harv_ids)
    return seats, rows, pecks, extra


# --------------------------------------------------------------------------
# per-game aggregation
# --------------------------------------------------------------------------

def at(rows, r, pred):
    if r >= len(rows):
        return ""
    return sum(1 for c in rows[r][1] if pred(c))


def aggregate(seats, rows, pecks, mapname, w, h, coredsq, extra=None):
    n = len(rows)
    is_claim = lambda c: c == "Mc"                       # noqa: E731
    is_mjown = lambda c: c in ("Mc", "Mb")               # noqa: E731
    is_ours = lambda c: c in ("Ob", "Oc")                # noqa: E731

    def first(pred, k=1):
        for rnd, codes in rows:
            if sum(1 for c in codes if pred(c)) >= k:
                return rnd
        return -1

    claim_series = [sum(1 for c in codes if is_claim(c)) for _r, codes in rows]
    own_series = [sum(1 for c in codes if is_mjown(c)) for _r, codes in rows]
    ours_series = [sum(1 for c in codes if is_ours(c)) for _r, codes in rows]

    # brick episodes: our building appears on seat i, later leaves; retake =
    # first round after departure at which a Mjolnir BUILDING stands there.
    episodes = []
    nseat = len(seats)
    for i in range(nseat):
        prev = "."
        start = None
        for rnd, codes in rows:
            c = codes[i]
            if c in ("Ob", "Oc") and prev not in ("Ob", "Oc"):
                start = rnd
            elif prev in ("Ob", "Oc") and c not in ("Ob", "Oc"):
                # departed at rnd
                lat = -1
                for r2 in range(rnd, min(n, rnd + 60)):
                    if rows[r2][1][i] in ("Mc", "Mb"):
                        lat = r2 - rnd
                        break
                episodes.append((i, start, rnd, lat))
                start = None
            prev = c
        if start is not None:
            episodes.append((i, start, -1, -1))   # still standing at game end

    # MIRROR: their own claim episodes on their own sockets (what our collar
    # actually removes, and how long a claim survives once laid).
    mj_epi = []
    for i in range(len(seats)):
        prev, start = ".", None
        for rnd, codes in rows:
            c = codes[i]
            if c == "Mc" and prev != "Mc":
                start = rnd
            elif prev == "Mc" and c != "Mc":
                mj_epi.append((start, rnd))
                start = None
            prev = c
        if start is not None:
            mj_epi.append((start, -1))
    mj_lives = [e[1] - e[0] for e in mj_epi if e[1] >= 0]

    lat = [e[3] for e in episodes if e[2] >= 0 and e[3] >= 0]
    # RESPONSE TEST: their claim immediately BEFORE our first building lands
    # inside RING_NEAR_DSQ (=16) of their core, and 20 rounds AFTER it.
    pre = post = -1
    if extra and extra.get("our_near16_first", -1) >= 0 and n:
        p0 = max(0, extra["our_near16_first"] - 1)
        p1 = min(n - 1, extra["our_near16_first"] + 20)
        pre = sum(1 for c in rows[p0][1] if is_claim(c))
        post = sum(1 for c in rows[p1][1] if is_claim(c))
    tail = claim_series[max(0, n - 50):]
    return {
        "map": mapname, "w": w, "h": h, "coredsq": coredsq,
        "rounds": n, "seats": nseat,
        "claim_onset": first(is_claim, 1),
        "claim2_onset": first(is_claim, 2),
        "claim3_onset": first(is_claim, 3),
        "claim5_onset": first(is_claim, 5),
        "own_onset": first(is_mjown, 1),
        "claim_r20": claim_series[20] if n > 20 else -1,
        "claim_r40": claim_series[40] if n > 40 else -1,
        "claim_r80": claim_series[80] if n > 80 else -1,
        "claim_r150": claim_series[150] if n > 150 else -1,
        "claim_max": max(claim_series) if claim_series else 0,
        "own_max": max(own_series) if own_series else 0,
        "claim_mean": round(sum(claim_series) / n, 3) if n else 0,
        "claim_tail50": round(sum(tail) / len(tail), 3) if tail else 0,
        "own_mean": round(sum(own_series) / n, 3) if n else 0,
        "ours_max": max(ours_series) if ours_series else 0,
        "ours_seatrounds": sum(ours_series),
        "ours_first": first(is_ours, 1),
        "episodes": len(episodes),
        "epi_ended": sum(1 for e in episodes if e[2] >= 0),
        "retakes": len(lat),
        "retake_lat_mean": round(sum(lat) / len(lat), 2) if lat else -1,
        "retake_lat_med": sorted(lat)[len(lat) // 2] if lat else -1,
        "pecks_total": len(pecks),
        "ourblock_seatrounds": sum(sum(1 for c in cd if c == "Ob")
                                   for _r, cd in rows),
        "ourconv_seatrounds": sum(sum(1 for c in cd if c == "Oc")
                                  for _r, cd in rows),
        "mjbody_seatrounds": sum(sum(1 for c in cd if c == "Md")
                                 for _r, cd in rows),
        "empty_seatrounds": sum(sum(1 for c in cd if c == ".")
                                for _r, cd in rows),
        "claim_w40_100": (round(sum(claim_series[40:100]) / 60, 3)
                          if n > 100 else -1),
        "block_w40_100": (round(sum(
            sum(1 for c in cd if c == "Ob") for _r, cd in rows[40:100]) / 60, 3)
            if n > 100 else -1),
        "mj_claim_epis": len(mj_epi),
        "mj_claim_ended": len(mj_lives),
        "mj_claim_life_med": (sorted(mj_lives)[len(mj_lives) // 2]
                              if mj_lives else -1),
        "claim_pre_press": pre,
        "claim_post_press": post,
    }


_MJ = None  # set per call in run_one


def run_one(replay, mapname, ourseat):
    global _MJ
    w, h, _mrows, cores = parse_map26(ROOT / "maps" / f"{mapname}.map26")
    anchors = {c[0]: (c[1], c[2]) for c in cores}
    ourteam = 0 if ourseat == "A" else 1
    _MJ = 1 - ourteam
    ax, ay = anchors[ourteam]
    bx, by = anchors[_MJ]
    coredsq = (ax - bx) ** 2 + (ay - by) ** 2
    seats, rows, pecks, extra = walk(replay, mapname, ourseat)
    agg = aggregate(seats, rows, pecks, mapname, w, h, coredsq, extra)
    agg.update(extra)
    # pecks on OUR entities standing on their sockets == their EVICT dose
    agg["pecks_on_ours"] = sum(1 for p in pecks if p[1] == ourteam)
    agg["pecks_on_theirs"] = sum(1 for p in pecks if p[1] == _MJ)
    kinds = {}
    for p in pecks:
        if p[1] == ourteam:
            kinds[p[2]] = kinds.get(p[2], 0) + 1
    agg["peck_victims"] = ",".join(f"{k}:{v}" for k, v in sorted(kinds.items()))
    return agg


def main():
    ap = sys.argv[1:]
    if not ap or ap[0] in ("-h", "--help"):
        print(__doc__)
        raise SystemExit(0)
    mode = ap[0]
    if mode == "--game":
        seats, rows, pecks, _x = walk(ap[1], ap[2], ap[3])
        print("# seats " + " ".join(f"{x},{y}" for x, y in seats))
        print("round\tcodes\tclaim\tmjown\tours")
        for rnd, codes in rows:
            print(f"{rnd}\t{'|'.join(codes)}\t"
                  f"{sum(1 for c in codes if c == 'Mc')}\t"
                  f"{sum(1 for c in codes if c in ('Mc', 'Mb'))}\t"
                  f"{sum(1 for c in codes if c in ('Ob', 'Oc'))}")
        print(f"# pecks on seats: {len(pecks)}", file=sys.stderr)
    elif mode == "--crosscheck":
        import seattape
        _s, _c, strows = seattape.tape(ap[1], ap[2], ap[3])
        seats, rows, _p, _x = walk(ap[1], ap[2], ap[3])
        bad = 0
        for (rnd, s, _d), (r2, codes) in zip(strows, rows):
            mine = sum(1 for c in codes if c in ("Mc", "Mb"))
            theirs = s.count("E")
            mine_o = sum(1 for c in codes if c in ("Ob", "Oc"))
            theirs_o = s.count("D") + s.count("o")
            if rnd != r2 or mine != theirs or mine_o != theirs_o:
                bad += 1
                if bad < 5:
                    print(f"MISMATCH r{rnd}: mine {mine}/{mine_o} "
                          f"seattape {theirs}/{theirs_o}")
        print(f"crosscheck rounds={len(rows)} mismatches={bad}")
        raise SystemExit(1 if bad else 0)
    elif mode == "--mutate":
        _s, rows, _p, _x = walk(ap[1], ap[2], ap[3])
        _s2, rows2, _p2, _x2 = walk(ap[1], ap[2], ap[3], anchor_shift=(3, 3))
        f = lambda rr: sum(sum(1 for c in cd if c == "Mc")  # noqa: E731
                           for _r, cd in rr) / max(1, len(rr))
        print(f"true-anchor mean claim = {f(rows):.3f}   "
              f"shifted-anchor mean claim = {f(rows2):.3f}")
    elif mode == "--batch":
        import csv
        import multiprocessing as mp
        tsv, repdir = ap[1], ap[2]
        jobs = []
        with open(tsv) as fh:
            for row in csv.DictReader(fh, delimiter="\t"):
                jobs.append((row["tag"], row["map"], row["seat"], row["ours"],
                             row["cond"], row["turn"],
                             str(Path(repdir) / f"{row['tag']}.replay26")))
        with mp.Pool() as pool:
            aggs = pool.starmap(_job, [(j,) for j in jobs], chunksize=8)
        cols = None
        for a in aggs:
            if a is None:
                continue
            if cols is None:
                cols = list(a.keys())
                print("\t".join(cols))
            print("\t".join(str(a[c]) for c in cols))
    else:
        raise SystemExit(f"unknown mode {mode}")


def _job(j):
    tag, mapname, seat, ours, cond, turn, path = j
    try:
        a = run_one(path, mapname, seat)
    except Exception as exc:            # noqa: BLE001
        print(f"FAIL {tag}: {exc}", file=sys.stderr)
        return None
    a["tag"] = tag
    a["seat"] = seat
    a["result"] = ours
    a["cond"] = cond
    a["turn"] = turn
    return a


if __name__ == "__main__":
    main()
