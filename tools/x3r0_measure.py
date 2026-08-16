#!/usr/bin/env python3
"""Re-derive x3r0's two corpus claims on OUR decoded replays.

CLAIM A: rounds holding ammo with no live turret.
CLAIM B: damaged-core rounds with an empty heal seat.

One TSV row per (file, side). Side is US / THEM. Seat comes from meta_join
team NAMES (independent of winnerSide - see corpus-howto TRAP 7).
"""
from __future__ import annotations
import sys, os, csv
from pathlib import Path

WIRE_VARINT, WIRE_64, WIRE_LEN, WIRE_32 = 0, 1, 2, 5


def _varint(buf, i):
    r = s = 0
    while True:
        b = buf[i]; i += 1
        r |= (b & 0x7F) << s
        if not b & 0x80:
            return r, i
        s += 7


def fields(buf):
    i, n = 0, len(buf)
    while i < n:
        tag, i = _varint(buf, i)
        num, wire = tag >> 3, tag & 7
        if wire == WIRE_VARINT:
            v, i = _varint(buf, i); yield num, wire, v
        elif wire == WIRE_LEN:
            ln, i = _varint(buf, i); yield num, wire, buf[i:i+ln]; i += ln
        elif wire == WIRE_32:
            yield num, wire, buf[i:i+4]; i += 4
        elif wire == WIRE_64:
            yield num, wire, buf[i:i+8]; i += 8
        else:
            raise ValueError("wire %d" % wire)


def scalars(buf):
    return {n: v for n, _w, v in fields(buf)}


def read_pos(buf):
    d = scalars(buf)
    return d.get(1, 0), d.get(2, 0)


def packed(buf):
    out, i, n = [], 0, len(buf)
    while i < n:
        v, i = _varint(buf, i); out.append(v)
    return out


KIND = {10: "bot", 11: "conv", 12: "split", 15: "harv", 18: "barr",
        20: "core", 21: "gunner", 22: "sentinel", 24: "launcher"}
TURRET = ("gunner", "sentinel")
CORE_MAX = 500
TWO64 = 1 << 64


def s64(v):
    return v - TWO64 if v >= (1 << 63) else v


def parse_entity(buf):
    eid = team = hp = mhp = 0
    pos = None; kind = None
    for num, wire, v in fields(buf):
        if num == 1: eid = v
        elif num == 2: team = v
        elif num == 3: pos = read_pos(v)
        elif num == 4: hp = v
        elif num == 5: mhp = v
        elif num in KIND: kind = KIND[num]
        elif wire == WIRE_LEN: kind = "unknown%d" % num
    return eid, team, pos, kind, hp, mhp


COLS = ["file", "side", "team", "rounds",
        # claim A
        "a_hold", "a_hold_noturret", "a_hold_turret", "a_hold_nolauncher_either",
        "a_idle_ammo_sum", "a_ammo_sum", "a_max_ammo", "a_zero_ammo_rounds",
        "n_turret_built", "n_convert", "conv_amt",
        "conv_noturret_n", "conv_noturret_amt", "a_final_ammo",
        "a_hold10", "a_hold10_noturret", "a_hold10_turret", "a_worst_idle_hold",
        "a_idle_pre_first", "a_idle_after_dead",
        # claim B
        "b_alive_rounds", "b_dmg", "b_dmg_noseatbot", "b_dmg_seatbot",
        "b_dmg_anyseatempty", "b_dmg_allseatsfull", "b_empty_seat_sum",
        "b_seats_total", "b_dmg_nocoreheal", "b_coreheal_rounds",
        "b_hp_over_max_rounds", "b_final_hp", "b_dmg_noseatbot_nolow",
        "b_blockown_sum", "b_blockbot_sum", "b_dmg_allblockedown",
        "b_freeseat_rounds", "b_dmg_ti1", "b_dmg_nearbot", "b_x3r0_full",
        ]


def measure(path):
    data = Path(path).read_bytes()
    map_buf = None; turns = []
    for num, wire, v in fields(data):
        if num == 1 and wire == WIRE_LEN: map_buf = v
        elif num == 3 and wire == WIRE_LEN: turns.append(v)
    if map_buf is None:
        return None
    W = H = 0; tiles = []; cores = []
    for num, wire, v in fields(map_buf):
        if num == 1: W = v
        elif num == 2: H = v
        elif num == 3:
            row = []
            for rn, rw, rv in fields(v):
                if rn == 1:
                    row.extend(packed(rv) if rw == WIRE_LEN else [rv])
            tiles.append(row)
        elif num == 4:
            c = {"id": 0, "team": 0, "pos": (0, 0)}
            for cn, _cw, cv in fields(v):
                if cn == 1: c["id"] = cv
                elif cn == 2: c["team"] = cv
                elif cn == 3: c["pos"] = read_pos(cv)
            cores.append(c)

    def env(x, y):
        if 0 <= y < len(tiles) and 0 <= x < len(tiles[y]):
            return tiles[y][x]
        return 1

    seats = {}; foot = {}; core_id = {}; core_anchor = {}
    for c in cores:
        x, y = c["pos"]; t = c["team"]
        core_id[t] = c["id"]; core_anchor[t] = (x, y)
        foot[t] = {(x, y), (x+1, y), (x, y+1), (x+1, y+1)}
        s = [(x, y-1), (x+1, y-1), (x+2, y), (x+2, y+1),
             (x+1, y+2), (x, y+2), (x-1, y+1), (x-1, y)]
        seats[t] = [p for p in s if 0 <= p[0] < W and 0 <= p[1] < H]
    if 0 not in core_id or 1 not in core_id:
        return None

    # entity state
    e_team = {}; e_kind = {}; e_pos = {}
    hp = {}
    for c in cores:
        e_team[c["id"]] = c["team"]; e_kind[c["id"]] = "core"
        e_pos[c["id"]] = c["pos"]; hp[c["id"]] = CORE_MAX
    ammo = [0, 0]
    ti = [0, 0]
    acc = {t: dict.fromkeys(COLS[3:], 0) for t in (0, 1)}
    for t in (0, 1):
        acc[t]["b_seats_total"] = 0
    turret_ids = {0: set(), 1: set()}
    launcher_ids = {0: set(), 1: set()}
    seen_ids = set(e_team)

    for rnd, tb in enumerate(turns):
        heal_core = [False, False]
        for _n, _w, ub in fields(tb):
            for un, _uw, u in fields(ub):
                if un == 1:                                  # placeEntity
                    for en, _ew, eb in fields(u):
                        if en != 1: continue
                        eid, team, pos, kind, ehp, emhp = parse_entity(eb)
                        if kind is None or pos is None: continue
                        new = eid not in seen_ids
                        seen_ids.add(eid)
                        e_team[eid] = team; e_kind[eid] = kind; e_pos[eid] = pos
                        if new:
                            hp[eid] = ehp or emhp
                            if kind in TURRET:
                                turret_ids[team].add(eid)
                                acc[team]["n_turret_built"] += 1
                            elif kind == "launcher":
                                launcher_ids[team].add(eid)
                        else:
                            hp[eid] = ehp if ehp else hp.get(eid, ehp)
                elif un == 2:                                # moveBuilderBot
                    eid = None; to = None
                    for mn, _mw, mv in fields(u):
                        if mn == 1: eid = mv
                        elif mn == 2: to = read_pos(mv)
                    if eid in e_pos and to is not None:
                        e_pos[eid] = to
                elif un == 3:                                # removeEntity
                    for rn, _rw, rv in fields(u):
                        if rn == 1:
                            t = e_team.pop(rv, None)
                            e_kind.pop(rv, None); e_pos.pop(rv, None)
                            hp.pop(rv, None)
                            if t is not None:
                                turret_ids[t].discard(rv)
                                launcher_ids[t].discard(rv)
                elif un == 5:                                # updateHp
                    eid = None; d = 0
                    for hn, hw, hv in fields(u):
                        if hn == 1: eid = hv
                        elif hn == 2: d = s64(hv) if hw == WIRE_VARINT else 0
                    if eid in hp:
                        hp[eid] += d
                elif un == 6:                                # updatePlayers
                    for pn, _pw, pv in fields(u):
                        if pn != 1: continue
                        for tn, _tw, tv in fields(pv):
                            if tn in (1, 2):
                                _d = scalars(tv)
                                ammo[tn-1] = _d.get(7, 0)
                                ti[tn-1] = _d.get(1, 0)
                elif un == 14:                               # coreConvertAmmo
                    d = scalars(u)
                    tt = d.get(1, 0); amt = d.get(2, 0)
                    acc[tt]["n_convert"] += 1; acc[tt]["conv_amt"] += amt
                    if not turret_ids[tt]:
                        acc[tt]["conv_noturret_n"] += 1
                        acc[tt]["conv_noturret_amt"] += amt
                elif un == 15:                               # builderHeal
                    eid = None; tgt = None
                    for hn, _hw, hv in fields(u):
                        if hn == 1: eid = hv
                        elif hn == 2: tgt = read_pos(hv)
                    t = e_team.get(eid)
                    if t is not None and tgt is not None and tgt in foot.get(t, ()):
                        heal_core[t] = True

        # --- end-of-round snapshot ---
        occupied = {}; occupied_team = {}
        bots = {0: set(), 1: set()}
        for eid, k in e_kind.items():
            p = e_pos.get(eid)
            if p is None: continue
            if k == "bot":
                bots[e_team[eid]].add(p)
            occupied[p] = k; occupied_team[p] = e_team[eid]
        for t in (0, 1):
            a = acc[t]
            a["rounds"] += 1
            am = ammo[t]
            nt = len(turret_ids[t])
            a["a_ammo_sum"] += am
            a["a_final_ammo"] = am
            if am > a["a_max_ammo"]: a["a_max_ammo"] = am
            if am > 0:
                a["a_hold"] += 1
                if nt == 0:
                    a["a_hold_noturret"] += 1
                    a["a_idle_ammo_sum"] += am
                    if not launcher_ids[t]:
                        a["a_hold_nolauncher_either"] += 1
                else:
                    a["a_hold_turret"] += 1
            if am >= 10:
                a["a_hold10"] += 1
                if nt == 0:
                    a["a_hold10_noturret"] += 1
                    if a["n_turret_built"] == 0:
                        a["a_idle_pre_first"] += 1
                    else:
                        a["a_idle_after_dead"] += 1
                    if am > a["a_worst_idle_hold"]:
                        a["a_worst_idle_hold"] = am
                else:
                    a["a_hold10_turret"] += 1
            else:
                a["a_zero_ammo_rounds"] += 1
            cid = core_id[t]
            if cid in hp:
                a["b_alive_rounds"] += 1
                chp = hp[cid]
                a["b_final_hp"] = chp
                if chp > CORE_MAX:
                    a["b_hp_over_max_rounds"] += 1
                if heal_core[t]:
                    a["b_coreheal_rounds"] += 1
                if chp < CORE_MAX:
                    a["b_dmg"] += 1
                    st = seats[t]
                    a["b_seats_total"] += len(st)
                    onseat = sum(1 for p in st if p in bots[t])
                    empt = 0; bown = 0; bbot = 0; standable = 0
                    for p in st:
                        if env(p[0], p[1]) == 1: continue
                        standable += 1
                        k = occupied.get(p)
                        if k is None:
                            empt += 1
                        elif k == "bot":
                            bbot += 1
                        elif occupied_team.get(p) == t:
                            bown += 1
                    a["b_empty_seat_sum"] += empt
                    a["b_blockown_sum"] += bown
                    a["b_blockbot_sum"] += bbot
                    if standable and bown == standable:
                        a["b_dmg_allblockedown"] += 1
                    if onseat == 0:
                        a["b_dmg_noseatbot"] += 1
                        if empt > 0:
                            a["b_dmg_noseatbot_nolow"] += 1
                    else:
                        a["b_dmg_seatbot"] += 1
                    if empt > 0:
                        a["b_dmg_anyseatempty"] += 1
                    else:
                        a["b_dmg_allseatsfull"] += 1
                    if not heal_core[t]:
                        a["b_dmg_nocoreheal"] += 1
                    if empt > 0:
                        a["b_freeseat_rounds"] += 1
                    if ti[t] >= 1:
                        a["b_dmg_ti1"] += 1
                    cx, cy = core_anchor[t]
                    near = any((bx-cx)*(bx-cx) + (by-cy)*(by-cy) <= 25
                               for bx, by in bots[t])
                    if near:
                        a["b_dmg_nearbot"] += 1
                    if empt > 0 and ti[t] >= 1 and near and onseat == 0:
                        a["b_x3r0_full"] += 1
    return acc


def main():
    poplist = sys.argv[1]
    out = sys.argv[2]
    rows = list(csv.DictReader(open(poplist), delimiter="\t"))
    with open(out, "w") as fh:
        fh.write("\t".join(COLS) + "\n")
        for i, r in enumerate(rows):
            p = "replay_archive/" + r["file"]
            try:
                acc = measure(p)
            except Exception as e:
                sys.stderr.write("ERR %s %s\n" % (r["file"], e)); continue
            if acc is None:
                sys.stderr.write("SKIP %s\n" % r["file"]); continue
            us = int(r["our_team"])
            for t in (0, 1):
                side = "US" if t == us else "THEM"
                a = acc[t]
                fh.write("\t".join([r["file"], side, str(t)] +
                                   [str(a[c]) for c in COLS[3:]]) + "\n")
            if i % 200 == 0:
                sys.stderr.write("%d/%d\n" % (i, len(rows))); sys.stderr.flush()


if __name__ == "__main__":
    main()
