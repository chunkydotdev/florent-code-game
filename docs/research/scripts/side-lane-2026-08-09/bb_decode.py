#!/usr/bin/env python3
"""Per-round BUILDER-BOT POSITION decoder (read-only; writes only to scratchpad).

Extends the s23 phase decoder with a live entity-position tracker so we can ask
*where the besieged team's builders were* while its core was taking damage.

Row file (argv[0]) — emitted only for rounds that matter to the question, i.e.
rounds where the team's own core took damage or healing, or the team put an
attacker on the enemy core:

  live_bb / live_bb0   live builder bots of this team at END / START of round
  adj / adj0           live builders on a tile orthogonally adjacent to OWN core
                       footprint (the heal-eligible slots; a 2x2 core has
                       exactly 8), at END / START of round
  onfp                 live builders standing ON an own-footprint tile (must be 0)
  near8 / near20       live builders within d2<=8 / <=20 of own core anchor
  heal_ev              builderHeal events by this team this round (any target)
  heal_core            builderHeal events by this team onto an OWN footprint tile
  heal_core_o          builderHeal events onto the ENEMY footprint (should be ~0)
  b_/d_builder_bot     builder spawns / deaths this round
  atkers_on_enemy_core distinct attackers this team put on the ENEMY core
  coredmg_taken / coreheal_taken / corehp   for THIS team's OWN core

Validation file (argv[1]) — one row per (file, team) with game totals and the
geometric invariants, so the tracker can be reconciled before use.

Traps honoured (docs/research/corpus-howto.md):
  1. build = FIRST placeEntity carrying an id (rotate re-emits).
  2. updateHp.delta is a 64-bit two's-complement varint.
  3. launcher throws are moveBuilderBot with |to-frm| > 1 (counted, not dropped).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa: E402

COLS = ["file", "rnd", "team",
        "live_bb", "live_bb0", "adj", "adj0", "onfp", "near8", "near20",
        "heal_ev", "heal_core", "heal_core_o",
        "b_builder_bot", "d_builder_bot",
        "atkers_on_enemy_core", "coredmg_taken", "coreheal_taken", "corehp"]

VCOLS = ["file", "team", "rounds", "tot_b", "tot_d", "final_live",
         "max_live", "max_adj", "max_onfp", "tot_moves", "tot_step",
         "tot_throw", "bad_pos", "tot_heal_ev", "tot_heal_core",
         "tot_heal_core_o", "tot_coreheal", "tot_coredmg", "mw", "mh",
         "d2_cores"]


def s64(v):
    return v - (1 << 64) if v >= (1 << 63) else v


def decode(path: Path, out, vout):
    data = path.read_bytes()
    map_buf, turn_bufs = None, []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if map_buf is None:
        return
    w = h = 0
    cores = []
    for num, wire, value in fields(map_buf):
        if num == 1:
            w = value
        elif num == 2:
            h = value
        elif num == 4:
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
    id2team = {c["id"]: c["team"] for c in cores}

    footprint = {}
    for t, (cx, cy) in corepos.items():
        for dx in (0, 1):
            for dy in (0, 1):
                footprint[(cx + dx, cy + dy)] = t
    ring = {0: set(), 1: set()}
    for (fx, fy), t in footprint.items():
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            p = (fx + dx, fy + dy)
            if p not in footprint:
                ring[t].add(p)
    fpset = {0: set(), 1: set()}
    for p, t in footprint.items():
        fpset[t].add(p)

    name = path.name
    pos_of = {c["id"]: c["pos"] for c in cores}
    team_of = dict(id2team)
    kind_of = {c["id"]: "core" for c in cores}
    bots = {0: set(), 1: set()}
    core_hp_left = {0: 500, 1: 500}
    V = {t: dict.fromkeys(VCOLS[2:], 0) for t in (0, 1)}

    def d2(a, b):
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

    def snapshot(t):
        live = adj = onfp = n8 = n20 = 0
        rg, fs, ca = ring[t], fpset[t], corepos[t]
        for bid in bots[t]:
            p = pos_of.get(bid)
            if p is None:
                continue
            live += 1
            if p in rg:
                adj += 1
            if p in fs:
                onfp += 1
            d = d2(p, ca)
            if d <= 8:
                n8 += 1
            if d <= 20:
                n20 += 1
        return live, adj, onfp, n8, n20

    for rnd, turn_buf in enumerate(turn_bufs):
        pre = {t: snapshot(t) for t in (0, 1)}
        acc = {}
        atkset = {0: set(), 1: set()}

        def cell(t):
            if t not in acc:
                acc[t] = dict.fromkeys(COLS[3:], 0)
            return acc[t]

        for _n, _w2, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:                                   # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        if e.id in pos_of:                      # rotate re-emit
                            pos_of[e.id] = e.pos
                            continue
                        pos_of[e.id] = e.pos
                        team_of[e.id] = e.team
                        kind_of[e.id] = e.kind
                        if e.kind == "builder_bot":
                            bots[e.team].add(e.id)
                            cell(e.team)["b_builder_bot"] += 1
                            V[e.team]["tot_b"] += 1
                            if not (0 <= e.pos[0] < w and 0 <= e.pos[1] < h):
                                V[e.team]["bad_pos"] += 1
                elif unum == 2:                                 # moveBuilderBot
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid in pos_of and to:
                        old = pos_of[eid]
                        t = team_of.get(eid, 0)
                        V[t]["tot_moves"] += 1
                        dd = abs(to[0] - old[0]) + abs(to[1] - old[1])
                        if dd == 1:
                            V[t]["tot_step"] += 1
                        else:
                            V[t]["tot_throw"] += 1
                        if not (0 <= to[0] < w and 0 <= to[1] < h):
                            V[t]["bad_pos"] += 1
                        pos_of[eid] = to
                elif unum == 3:                                 # removeEntity
                    for _rn, _rw, rv in fields(ubuf):
                        if rv not in pos_of:
                            continue
                        pos_of.pop(rv)
                        t = team_of.get(rv, 0)
                        if kind_of.get(rv) == "builder_bot":
                            bots[t].discard(rv)
                            cell(t)["d_builder_bot"] += 1
                            V[t]["tot_d"] += 1
                elif unum == 5:                                 # updateHp
                    eid = None
                    delta = 0
                    for hn, _hw, hv in fields(ubuf):
                        if hn == 1:
                            eid = hv
                        elif hn == 2:
                            delta = s64(hv)
                    if eid in id2team:
                        t = id2team[eid]
                        core_hp_left[t] += delta
                        if delta < 0:
                            cell(t)["coredmg_taken"] += -delta
                            V[t]["tot_coredmg"] += -delta
                        else:
                            cell(t)["coreheal_taken"] += delta
                            V[t]["tot_coreheal"] += delta
                elif unum == 12:                                # fireTurret
                    frm = to = None
                    for fn, _fw, fv in fields(ubuf):
                        if fn == 1:
                            frm = read_pos(fv)
                        elif fn == 2:
                            to = read_pos(fv)
                    if to is not None and to in footprint and frm is not None:
                        vt = footprint[to]
                        atkset[1 - vt].add(("T",) + frm)
                elif unum == 13:                                # builderAttack
                    eid = tgt = None
                    for an, _aw, av in fields(ubuf):
                        if an == 1:
                            eid = av
                        elif an == 2:
                            tgt = read_pos(av)
                    t = team_of.get(eid)
                    if t is not None and tgt is not None and \
                            footprint.get(tgt) == 1 - t:
                        atkset[t].add(("B", eid))
                elif unum == 15:                                # builderHeal
                    eid = tgt = None
                    for hn, _hw, hv in fields(ubuf):
                        if hn == 1:
                            eid = hv
                        elif hn == 2:
                            tgt = read_pos(hv)
                    t = team_of.get(eid)
                    if t is None:
                        continue
                    c = cell(t)
                    c["heal_ev"] += 1
                    V[t]["tot_heal_ev"] += 1
                    if tgt is not None:
                        ft = footprint.get(tgt)
                        if ft == t:
                            c["heal_core"] += 1
                            V[t]["tot_heal_core"] += 1
                        elif ft is not None:
                            c["heal_core_o"] += 1
                            V[t]["tot_heal_core_o"] += 1

        for t in (0, 1):
            live, adj, onfp, n8, n20 = snapshot(t)
            v = V[t]
            v["max_live"] = max(v["max_live"], live)
            v["max_adj"] = max(v["max_adj"], adj)
            v["max_onfp"] = max(v["max_onfp"], onfp)
            c = acc.get(t)
            na = len(atkset[t])
            if c is None and na == 0:
                continue
            if c is None:
                c = dict.fromkeys(COLS[3:], 0)
            c["atkers_on_enemy_core"] = na
            if not (c["coredmg_taken"] or c["coreheal_taken"] or na):
                continue
            c["live_bb"], c["adj"], c["onfp"] = live, adj, onfp
            c["near8"], c["near20"] = n8, n20
            c["live_bb0"], c["adj0"] = pre[t][0], pre[t][1]
            c["corehp"] = core_hp_left[t]
            out.write(f"{name}\t{rnd}\t{t}\t" +
                      "\t".join(str(c[k]) for k in COLS[3:]) + "\n")

    dc = d2(corepos[0], corepos[1])
    for t in (0, 1):
        v = V[t]
        v["rounds"] = len(turn_bufs)
        v["final_live"] = len(bots[t])
        v["mw"], v["mh"], v["d2_cores"] = w, h, dc
        vout.write(f"{name}\t{t}\t" + "\t".join(str(v[k]) for k in VCOLS[2:]) + "\n")


def main(argv):
    out = open(argv[0], "w")
    vout = open(argv[1], "w")
    out.write("\t".join(COLS) + "\n")
    vout.write("\t".join(VCOLS) + "\n")
    bad = 0
    files = [Path(x) for x in argv[2:]]
    for i, p in enumerate(files):
        try:
            decode(p, out, vout)
        except Exception as exc:                                # noqa: BLE001
            bad += 1
            print(f"ERR {p.name}: {exc}", file=sys.stderr)
        if (i + 1) % 250 == 0:
            print(f"  ...{i+1}/{len(files)} ({bad} err)", file=sys.stderr, flush=True)
    out.close()
    vout.close()
    print(f"done {len(files)} files, {bad} errors", file=sys.stderr, flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
