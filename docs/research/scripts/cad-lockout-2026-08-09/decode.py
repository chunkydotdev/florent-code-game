#!/usr/bin/env python3
"""Per-round decode of every attributed CtrlAltDefeat game, for the lockout test.

Emits ONE ROW PER (file, round) with, for BOTH teams but named from CAD's side:

  cad_core_dmg     negative updateHp deltas landing on CAD's core id this round
  cad_core_heal    positive updateHp deltas on CAD's core id this round
  cad_core_hp      running CAD core HP (500 seed, cores are never placeEntity'd)
  cad_builds       build actions by CAD this round = FIRST placeEntity per id
                   (rotation-re-emit guarded), EXCLUDING the core's own seed
  cad_bbuilds      BuilderBuild (Update field 16) events by a CAD builder bot
  cad_bots         CAD builder bots alive at end of round
  cad_bot_deaths   CAD builder bots removed this round
  cad_ti/cad_ammo  CAD global titanium / ammunition (updatePlayers)
  cad_convert      CoreConvertAmmo amount for CAD this round
  cad_launchers    CAD launchers alive at end of round
  cad_lnc_gone     CAD launchers removed this round, and whether they had taken
                   any damage before removal (dmg=combat, nodmg=self-destruct or
                   allied destroy)
  us_* mirrors for the same quantities.

THE FOUR TRAPS, honoured:
  1. placeEntity is re-emitted on gunner rotate -> a build is the FIRST
     placeEntity carrying a given entity id.  Guarded by `known` id set.
  2. updateHp.delta is a 64-bit two's-complement varint.  18446744073709551609
     is -7.  `_s64()` below.  VALIDATION prints the sign census; if we never see
     a positive delta the correction is wrong.
  3. not used here (no throw attribution).
  4. coverage is per-opponent; the caller says the N.

Usage: decode.py <join.tsv> <replay_dir> <out.tsv>
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import (  # noqa: E402
    fields, read_pos, parse_entity, scalars, WIRE_LEN, WIRE_VARINT,
)

OPP = "CtrlAltDefeat"


def _s64(v: int) -> int:
    """protobuf int32 negatives are sign-extended to 64 bits on the wire."""
    return v - (1 << 64) if v >= (1 << 63) else v


COLS = ["file", "rnd",
        "cad_core_dmg", "cad_core_heal", "cad_core_hp",
        "cad_builds", "cad_bbuilds", "cad_bots", "cad_bot_deaths",
        "cad_ti", "cad_ammo", "cad_convert", "cad_launchers", "cad_lnc_gone",
        "cad_atk_on_us_core", "cad_shots",
        "us_core_dmg", "us_core_hp", "us_builds", "us_bots", "us_ti", "us_ammo",
        "us_convert", "us_launchers", "us_lnc_gone", "us_shots"]


def decode(path: Path, cad_team: int, out, stats):
    our_team = 1 - cad_team
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
    cad_team = 1 - our_team
    core_id = {c["team"]: c["id"] for c in cores}
    core_tiles = {}
    for c in cores:
        x, y = c["pos"]
        core_tiles[c["team"]] = {(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)}

    name = path.name
    # entity id -> (team, kind); seeded with the two cores, which never appear
    # as placeEntity and so must never be counted as builds.
    ents: dict[int, tuple[int, str]] = {c["id"]: (c["team"], "core") for c in cores}
    bot_pos: dict[int, tuple[int, int]] = {}
    turret_at: dict[tuple[int, int], int] = {}   # turret tile -> owning team
    turret_pos: dict[int, tuple[int, int]] = {}  # turret id  -> tile
    hurt: set[int] = set()          # ids that have ever taken negative hp
    hp = {core_id[0]: 500, core_id[1]: 500}
    ti = {0: 500, 1: 500}
    ammo = {0: 0, 1: 0}

    for rnd, turn_buf in enumerate(turn_bufs):
        dmg = {0: 0, 1: 0}
        heal = {0: 0, 1: 0}
        builds = {0: 0, 1: 0}
        bbuilds = {0: 0, 1: 0}
        deaths = {0: 0, 1: 0}
        conv = {0: 0, 1: 0}
        shots = {0: 0, 1: 0}
        lnc_gone = {0: [], 1: []}
        atk_on_core = {0: 0, 1: 0}   # builder attacks landing on enemy core tiles

        for _n, _w, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:                                   # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        if e.id in ents:                        # rotate re-emit
                            if e.kind == "builder_bot":
                                bot_pos[e.id] = e.pos
                            continue
                        ents[e.id] = (e.team, e.kind)
                        hp[e.id] = e.hp
                        if e.kind == "builder_bot":
                            bot_pos[e.id] = e.pos
                        elif e.kind in ("gunner", "sentinel", "launcher"):
                            turret_at[e.pos] = e.team
                            turret_pos[e.id] = e.pos
                        builds[e.team] += 1
                elif unum == 2:                                 # moveBuilderBot
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid is not None and to is not None:
                        bot_pos[eid] = to
                elif unum == 3:                                 # removeEntity
                    for rn, _rw, rv in fields(ubuf):
                        if rn != 1:
                            continue
                        info = ents.pop(rv, None)
                        bot_pos.pop(rv, None)
                        if info is None:
                            continue
                        t, k = info
                        p = turret_pos.pop(rv, None)
                        if p is not None and turret_at.get(p) == t:
                            del turret_at[p]
                        if k == "builder_bot":
                            deaths[t] += 1
                        elif k == "launcher":
                            lnc_gone[t].append("dmg" if rv in hurt else "nodmg")
                elif unum == 5:                                 # updateHp
                    eid = None
                    delta = 0
                    for hn, _hw, hv in fields(ubuf):
                        if hn == 1:
                            eid = hv
                        elif hn == 2:
                            delta = _s64(hv)
                    if eid is None:
                        continue
                    stats["hp_neg" if delta < 0 else ("hp_pos" if delta > 0 else "hp_zero")] += 1
                    if delta < 0:
                        hurt.add(eid)
                    if eid in hp:
                        hp[eid] += delta
                    for t in (0, 1):
                        if eid == core_id[t]:
                            if delta < 0:
                                dmg[t] += -delta
                            else:
                                heal[t] += delta
                elif unum == 6:                                 # updatePlayers
                    for pn, _pw, pv in fields(ubuf):
                        if pn != 1:
                            continue
                        for tn, _tw, tv in fields(pv):
                            if tn in (1, 2):
                                d = scalars(tv)
                                ti[tn - 1] = d.get(1, 0)
                                ammo[tn - 1] = d.get(7, 0)
                elif unum == 12:                                # fireTurret
                    frm = None
                    for fn, _fw, fv in fields(ubuf):
                        if fn == 1:
                            frm = read_pos(fv)
                    # FireTurret carries no shooter id, only the tile it came
                    # from; attribute via the live turret-tile -> team index.
                    stats["shots_seen"] += 1
                    t = turret_at.get(frm)
                    if t is None:
                        stats["shots_unattrib"] += 1
                    else:
                        shots[t] += 1
                elif unum == 13:                                # builderAttack
                    aid = None
                    tgt = None
                    for an, _aw, av in fields(ubuf):
                        if an == 1:
                            aid = av
                        elif an == 2:
                            tgt = read_pos(av)
                    if aid in ents and tgt is not None:
                        t = ents[aid][0]
                        if tgt in core_tiles[1 - t]:
                            atk_on_core[t] += 1
                elif unum == 14:                                # coreConvertAmmo
                    t = 0
                    amt = 0
                    for cn, _cw, cv in fields(ubuf):
                        if cn == 1:
                            t = cv
                        elif cn == 2:
                            amt = cv
                    conv[t] += amt
                elif unum == 16:                                # builderBuild
                    bid = None
                    for bn, _bw, bv in fields(ubuf):
                        if bn == 1:
                            bid = bv
                    if bid in ents:
                        bbuilds[ents[bid][0]] += 1

        nbots = {0: 0, 1: 0}
        nlnc = {0: 0, 1: 0}
        for t, k in ents.values():
            if k == "builder_bot":
                nbots[t] += 1
            elif k == "launcher":
                nlnc[t] += 1
        c, u = cad_team, our_team
        out.write("\t".join(str(v) for v in [
            name, rnd,
            dmg[c], heal[c], hp[core_id[c]],
            builds[c], bbuilds[c], nbots[c], deaths[c],
            ti[c], ammo[c], conv[c], nlnc[c], ",".join(lnc_gone[c]) or "-",
            atk_on_core[c], shots[c],
            dmg[u], hp[core_id[u]], builds[u], nbots[u], ti[u], ammo[u],
            conv[u], nlnc[u], ",".join(lnc_gone[u]) or "-", shots[u],
        ]) + "\n")


def main(argv):
    pop_path, replay_dir, out_path = argv
    rows = list(csv.DictReader(open(pop_path), delimiter="\t"))
    stats = defaultdict(int)
    out = open(out_path, "w")
    out.write("\t".join(COLS) + "\n")
    n = 0
    for r in rows:
        p = Path(replay_dir) / r["file"]
        if not p.exists():
            print(f"MISSING {r['file']}", file=sys.stderr)
            continue
        decode(p, int(r["cad_team"]), out, stats)
        n += 1
    out.close()
    print(f"decoded {n}/{len(rows)} CAD games", file=sys.stderr)
    print("VALIDATION updateHp sign census: "
          f"neg={stats['hp_neg']} pos={stats['hp_pos']} zero={stats['hp_zero']}",
          file=sys.stderr)
    print(f"VALIDATION fireTurret attribution: seen={stats['shots_seen']} "
          f"unattributed={stats['shots_unattrib']}", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
