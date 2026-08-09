#!/usr/bin/env python3
"""FINE-BAND builder-bot POSITION census -- collar occupancy and penetration depth.

WHY THIS EXISTS
---------------
`corpus/events.tsv` gives BUILD and DEATH with positions, so alive-counts and
build geometry are already derivable. What is NOT in the corpus is where the
MOBILE units stand each round. The builder arm named two candidate triggers that
need exactly that:

  * "enemy builders sitting on their own core's collar seats"  -> collar occupancy
  * "distance to their ring"                                   -> penetration depth

Both are runtime-observable through the Controller (a unit sees builder bots via
get_tile_builder_bot_id / get_nearby_units inside its vision radius), so they are
admissible trigger candidates -- which is why they are worth decoding.

Emits one row per file x team x 25-round band:
  bots_mean / bots_max        builder bots alive (mean over rounds in band)
  collar8_mean / collar8_max  own builder bots at d2 <= 8 of OWN core (the core's
                              action radius -- the spawn ring, i.e. "collar seats")
  collar2_mean                own builder bots orthogonally adjacent to own core
  fwd_mean                    own builder bots on the enemy's half (d2_enemy < d2_own)
  mindist_enemy               min d2 from ANY of this team's builder bots to the
                              ENEMY core, over the band (deepest penetration)
  r36_rounds                  rounds in band with >=1 of this team's builder bots
                              inside d2<=36 of the enemy core (enemy core vision)
  r20_rounds                  same at d2<=20 (builder bot vision radius)

Rotation guard applies (a build is the FIRST placeEntity for an id); positions
are then maintained from moveBuilderBot and cleared on removeEntity.

Usage: fineband_positions.py OUT.tsv FILE [FILE ...]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa: E402

BAND_W = 25
LAST = "r150+"


def band(r: int) -> str:
    if r >= 150:
        return LAST
    lo = (r // BAND_W) * BAND_W
    return f"r{lo}-{lo + BAND_W}"


COLS = ["file", "team", "band", "rounds", "bots_mean", "bots_max",
        "collar8_mean", "collar8_max", "collar2_mean", "fwd_mean",
        "mindist_enemy", "r36_rounds", "r20_rounds"]


def d2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def census(path: Path, out) -> None:
    data = path.read_bytes()
    map_buf, turn_bufs = None, []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if map_buf is None:
        return
    cores = []
    for num, _w, value in fields(map_buf):
        if num == 4:
            c = {"id": 0, "team": 0, "pos": (0, 0)}
            for cn, _cw, cv in fields(value):
                if cn == 1:
                    c["id"] = cv
                elif cn == 2:
                    c["team"] = cv
                elif cn == 3:
                    c["pos"] = read_pos(cv)
            cores.append(c)
    if len(cores) != 2:
        return
    corepos = {c["team"]: c["pos"] for c in cores}

    known: dict[int, int] = {}          # every entity id -> team (rotation guard)
    bots: dict[int, tuple[int, tuple[int, int]]] = {}   # bot id -> (team, pos)
    acc: dict[tuple[int, str], dict] = {}

    def cell(t, b):
        k = (t, b)
        if k not in acc:
            acc[k] = {"rounds": 0, "bots": 0, "bots_max": 0, "collar8": 0,
                      "collar8_max": 0, "collar2": 0, "fwd": 0,
                      "mind": 10 ** 9, "r36": 0, "r20": 0}
        return acc[k]

    for rnd, turn_buf in enumerate(turn_bufs):
        b = band(rnd)
        for _n, _w2, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        if e.id in known:                    # rotation re-emit
                            if e.id in bots:
                                bots[e.id] = (e.team, e.pos)
                            continue
                        known[e.id] = e.team
                        if e.kind == "builder_bot":
                            bots[e.id] = (e.team, e.pos)
                elif unum == 2:
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid in bots and to:
                        bots[eid] = (bots[eid][0], to)
                elif unum == 3:
                    for _rn, _rw, rv in fields(ubuf):
                        bots.pop(rv, None)
        # end-of-round snapshot
        per = {0: [0, 0, 0, 0, 10 ** 9], 1: [0, 0, 0, 0, 10 ** 9]}  # n, collar8, collar2, fwd, mind
        for _bid, (t, p) in bots.items():
            own, enemy = corepos[t], corepos[1 - t]
            do, de = d2(p, own), d2(p, enemy)
            s = per[t]
            s[0] += 1
            if do <= 8:
                s[1] += 1
            if do <= 2:
                s[2] += 1
            if de < do:
                s[3] += 1
            if de < s[4]:
                s[4] = de
        for t in (0, 1):
            c = cell(t, b)
            n, c8, c2, fw, md = per[t]
            c["rounds"] += 1
            c["bots"] += n
            c["bots_max"] = max(c["bots_max"], n)
            c["collar8"] += c8
            c["collar8_max"] = max(c["collar8_max"], c8)
            c["collar2"] += c2
            c["fwd"] += fw
            if md < c["mind"]:
                c["mind"] = md
            if md <= 36:
                c["r36"] += 1
            if md <= 20:
                c["r20"] += 1

    for (t, b), c in acc.items():
        r = max(1, c["rounds"])
        md = -1 if c["mind"] >= 10 ** 9 else c["mind"]
        out.write("\t".join(str(v) for v in (
            path.name, t, b, c["rounds"],
            f"{c['bots']/r:.4f}", c["bots_max"],
            f"{c['collar8']/r:.4f}", c["collar8_max"],
            f"{c['collar2']/r:.4f}", f"{c['fwd']/r:.4f}",
            md, c["r36"], c["r20"])) + "\n")


def main(argv):
    out = open(argv[0], "w")
    out.write("\t".join(COLS) + "\n")
    bad = 0
    files = argv[1:]
    for i, p in enumerate(Path(x) for x in files):
        try:
            census(p, out)
        except Exception as exc:                             # noqa: BLE001
            bad += 1
            print(f"ERR {p.name}: {exc}", file=sys.stderr)
        if (i + 1) % 250 == 0:
            print(f"  ...{i+1}/{len(files)} ({bad} err)", file=sys.stderr, flush=True)
    out.close()
    print(f"done {len(files)} files, {bad} errors", file=sys.stderr, flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
