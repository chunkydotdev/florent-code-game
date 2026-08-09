#!/usr/bin/env python3
"""Per-round CAD BUILDER-TURN LEDGER, for the suppression-mechanism test.

The lockout cut (docs/research/cad-lockout-population-test-2026-08-09.md) left a
real, large, unexplained effect: after early core damage CAD's build rate over
r14-40 collapses ~7x while it still holds a median of 4 living builder bots.
This decoder asks the only question that can settle it: WHAT ARE THOSE BUILDERS
DOING INSTEAD?

For every CAD builder bot ALIVE AT THE START OF A ROUND, exactly one label is
assigned from the round's event stream, priority ordered:

    heal_core   builderHeal (Update 15) whose target tile is on CAD's own 2x2
                core footprint            <- the HEALER DISPLACEMENT hypothesis
    heal_bldg   builderHeal onto a tile holding a CAD non-core building
    heal_bot    builderHeal onto a tile holding a CAD builder bot
    heal_other  builderHeal anywhere else
    build       builderBuild (Update 16)
    attack      builderAttack (Update 13)
    thrown      moveBuilderBot whose displacement is >1 tile (launcher throw --
                NOT the bot's own choice; corpus trap 3)
    move        moveBuilderBot of exactly one tile
    died        removeEntity this round
    idle        none of the above

Acting and moving are mutually exclusive for a builder bot (official-docs.md:481,
:1455), which is exactly why the labels can be treated as a partition of the
bot's turn.  Bots BORN this round are excluded from the ledger -- a unit created
mid-round does not act that round.

Also emitted per round: collar-seat occupancy (the 8 tiles ORTHOGONALLY adjacent
to CAD's own core footprint -- the only tiles from which the core can be healed,
per the collar-heal census's ORTH8 definition), builds by type, CAD buildings
lost, titanium/ammo, and both cores' HP.

TRAPS HONOURED
  1. placeEntity is re-emitted on gunner rotate -> a build is the FIRST
     placeEntity carrying a given id.  Guarded by the `ents` id set.
  2. updateHp.delta is a 64-bit two's-complement varint; _s64() below.  The sign
     census is printed as VALIDATION -- both signs must appear.
  3. A throw is a moveBuilderBot with displacement >1; a throw landing exactly
     one tile away is indistinguishable from a step and is undercounted.
  4. Coverage is per-opponent; the caller states the N.
  botOutput is emitted at the END of a unit's turn and is NOT used for ordering.

Usage: mech_decode.py <cad_population.tsv> <replay_dir> <out.tsv>
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import (  # noqa: E402
    fields, read_pos, parse_entity, scalars, WIRE_LEN,
)

CARD = ((0, -1), (0, 1), (-1, 0), (1, 0))
TURRETS = ("gunner", "sentinel", "launcher")
LEDGER = ("heal_core", "heal_bldg", "heal_bot", "heal_other",
          "build", "attack", "thrown", "move", "died", "idle")


def _s64(v: int) -> int:
    return v - (1 << 64) if v >= (1 << 63) else v


COLS = (["file", "rnd",
         "cad_core_hp", "cad_core_dmg", "cad_core_healhp",
         "us_core_hp", "us_core_dmg",
         "cad_builds", "cad_bbuild",
         "b_conveyor", "b_splitter", "b_harvester", "b_barrier",
         "b_gunner", "b_sentinel", "b_launcher", "b_builder_bot",
         "cad_heal_ev", "cad_healcore_ev", "cad_batk", "cad_batk_core",
         "cad_moves", "cad_thrown_ev",
         "bots_start", "bots_end", "born", "died",
         "collar_seats", "collar_bots",
         "cad_ti", "cad_ammo", "cad_bldg_lost", "cad_conv_lost",
         "cad_harv_lost", "cad_turret_lost"]
        + ["L_" + k for k in LEDGER]
        + ["S_" + k for k in LEDGER]        # bots ON a collar seat at rnd start
        + ["O_" + k for k in LEDGER]        # bots OFF the collar at rnd start
        + ["n_cheb", "n_near20", "n_mid64", "n_far", "mind2_sum",
           "free_act", "free_move", "idle_free", "idle_acd", "idle_mcd",
           "bld_home20", "bld_mid64", "bld_fwd"]
        + ["out_n", "tled_n"])


def decode(path: Path, cad_team: int, out, stats):
    data = path.read_bytes()
    map_buf, turn_bufs = None, []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if map_buf is None:
        return False
    w = h = 0
    rows_env = []
    cores = []
    for num, _wr, value in fields(map_buf):
        if num == 1:
            w = value
        elif num == 2:
            h = value
        elif num == 3:
            for tn, _tw, tv in fields(value):
                if tn == 1:
                    rows_env.append(list(_packed(tv)))
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
        return False
    us_team = 1 - cad_team
    core_id = {c["team"]: c["id"] for c in cores}
    core_tiles = {}
    for c in cores:
        x, y = c["pos"]
        core_tiles[c["team"]] = {(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)}

    def is_wall(p):
        x, y = p
        if not rows_env or y >= len(rows_env) or x >= len(rows_env[y]):
            return False
        return rows_env[y][x] == 1

    # ORTH8: the 8 tiles orthogonally adjacent to CAD's own footprint -- exactly
    # the tiles a builder can heal the core from.
    ORTH = set()
    for (fx, fy) in core_tiles[cad_team]:
        for dx, dy in CARD:
            p = (fx + dx, fy + dy)
            if p in core_tiles[cad_team]:
                continue
            if 0 <= p[0] < w and 0 <= p[1] < h and not is_wall(p):
                ORTH.add(p)
    stats["orth8"] += 1 if len(ORTH) == 8 else 0
    stats["orth_trunc"] += 0 if len(ORTH) == 8 else 1

    name = path.name
    ents: dict[int, tuple[int, str]] = {c["id"]: (c["team"], "core") for c in cores}
    pos_of: dict[int, tuple[int, int]] = {}
    bot_at: dict[tuple[int, int], int] = {}
    bldg_at: dict[tuple[int, int], int] = {}
    for c in cores:
        for t in core_tiles[c["team"]]:
            bldg_at[t] = c["id"]
    hp = {core_id[0]: 500, core_id[1]: 500}
    ti = {0: 500, 1: 500}
    ammo = {0: 0, 1: 0}
    cd_a: dict[int, int] = {}
    cd_m: dict[int, int] = {}
    fp_cad = core_tiles[cad_team]

    def mind2(p):
        return min((p[0] - t[0]) ** 2 + (p[1] - t[1]) ** 2 for t in fp_cad)

    for rnd, turn_buf in enumerate(turn_bufs):
        start = {b for b, (t, k) in ents.items()
                 if t == cad_team and k == "builder_bot"}
        start_pos = {b: pos_of.get(b) for b in start}
        seats = {pos_of[b] for b in start if pos_of.get(b) in ORTH}
        collar_bots = sum(1 for b in start if pos_of.get(b) in ORTH)
        cd_a0 = {b: cd_a.get(b, 0) for b in start}
        cd_m0 = {b: cd_m.get(b, 0) for b in start}
        n_cheb = n_near = n_mid = n_far = 0
        mind2_sum = 0
        for b in start:
            p = start_pos.get(b)
            if p is None:
                continue
            d = mind2(p)
            mind2_sum += d
            if p in ORTH:
                continue
            if d <= 2:
                n_cheb += 1
            elif d <= 20:
                n_near += 1
            elif d <= 64:
                n_mid += 1
            else:
                n_far += 1

        label: dict[int, str] = {}
        dmg = {0: 0, 1: 0}
        healhp = {0: 0, 1: 0}
        builds = 0
        bbuild = 0
        by_kind = defaultdict(int)
        heal_ev = healcore_ev = batk = batk_core = 0
        moves = thrown_ev = 0
        born = died = 0
        bld_home = bld_mid = bld_fwd = 0
        lost = defaultdict(int)
        out_n = tled_n = 0

        def mark(b, lab):
            # first label wins for a given bot-turn; 'died' always overrides
            if b in start and (b not in label or lab == "died"):
                label[b] = lab

        for _n, _w2, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:                                    # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        if e.id in ents:                         # rotate re-emit
                            if e.kind == "builder_bot":
                                _relocate(pos_of, bot_at, e.id, e.pos)
                            continue
                        ents[e.id] = (e.team, e.kind)
                        hp[e.id] = e.hp
                        pos_of[e.id] = e.pos
                        if e.kind == "builder_bot":
                            bot_at[e.pos] = e.id
                            sub = {}
                            for fn2, _fw2, fv2 in fields(ebuf):
                                if fn2 == 10:
                                    sub = scalars(fv2)
                            cd_a[e.id] = sub.get(1, 0)
                            cd_m[e.id] = sub.get(2, 0)
                        else:
                            bldg_at[e.pos] = e.id
                        if e.team == cad_team:
                            builds += 1
                            by_kind[e.kind] += 1
                            dd2 = mind2(e.pos)
                            if dd2 <= 20:
                                bld_home += 1
                            elif dd2 <= 64:
                                bld_mid += 1
                            else:
                                bld_fwd += 1
                            if e.kind == "builder_bot":
                                born += 1
                elif unum == 2:                                  # moveBuilderBot
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid is None or to is None:
                        continue
                    old = pos_of.get(eid)
                    _relocate(pos_of, bot_at, eid, to)
                    if ents.get(eid, (None,))[0] != cad_team:
                        continue
                    d = 99 if old is None else max(abs(old[0] - to[0]),
                                                   abs(old[1] - to[1]))
                    if d > 1:
                        thrown_ev += 1
                        mark(eid, "thrown")
                    else:
                        moves += 1
                        mark(eid, "move")
                elif unum == 3:                                  # removeEntity
                    for rn, _rw, rv in fields(ubuf):
                        if rn != 1:
                            continue
                        info = ents.pop(rv, None)
                        p = pos_of.pop(rv, None)
                        if p is not None:
                            if bot_at.get(p) == rv:
                                del bot_at[p]
                            if bldg_at.get(p) == rv:
                                del bldg_at[p]
                        if info is None:
                            continue
                        t, k = info
                        if t != cad_team:
                            continue
                        if k == "builder_bot":
                            died += 1
                            mark(rv, "died")
                        elif k != "core":
                            lost["any"] += 1
                            if k == "conveyor":
                                lost["conv"] += 1
                            elif k == "harvester":
                                lost["harv"] += 1
                            elif k in TURRETS:
                                lost["turret"] += 1
                elif unum == 5:                                  # updateHp
                    eid, delta = None, 0
                    for hn, _hw, hv in fields(ubuf):
                        if hn == 1:
                            eid = hv
                        elif hn == 2:
                            delta = _s64(hv)
                    if eid is None:
                        continue
                    stats["hp_neg" if delta < 0 else
                          ("hp_pos" if delta > 0 else "hp_zero")] += 1
                    if eid in hp:
                        hp[eid] += delta
                    for t in (0, 1):
                        if eid == core_id[t]:
                            if delta < 0:
                                dmg[t] += -delta
                            else:
                                healhp[t] += delta
                elif unum == 6:                                  # updatePlayers
                    for pn, _pw, pv in fields(ubuf):
                        if pn != 1:
                            continue
                        for tn, _tw, tv in fields(pv):
                            if tn in (1, 2):
                                dd = scalars(tv)
                                ti[tn - 1] = dd.get(1, 0)
                                ammo[tn - 1] = dd.get(7, 0)
                elif unum == 7 or unum == 8:      # set{Action,Move}Cooldown
                    cid = None
                    cval = 0
                    for cn2, _cw2, cv2 in fields(ubuf):
                        if cn2 == 1:
                            cid = cv2
                        elif cn2 == 2:
                            cval = cv2
                    if cid is not None:
                        (cd_a if unum == 7 else cd_m)[cid] = cval
                elif unum == 9:                                  # botOutput
                    bid = None
                    tled = 0
                    for bn, _bw, bv in fields(ubuf):
                        if bn == 1:
                            bid = bv
                        elif bn == 4:
                            tled = bv
                    if ents.get(bid, (None,))[0] == cad_team:
                        out_n += 1
                        tled_n += 1 if tled else 0
                elif unum == 13:                                 # builderAttack
                    aid = tgt = None
                    for an, _aw, av in fields(ubuf):
                        if an == 1:
                            aid = av
                        elif an == 2:
                            tgt = read_pos(av)
                    if ents.get(aid, (None,))[0] != cad_team:
                        continue
                    batk += 1
                    if tgt in core_tiles[us_team]:
                        batk_core += 1
                    mark(aid, "attack")
                elif unum == 15:                                 # builderHeal
                    hid = tgt = None
                    for hn2, _hw2, hv2 in fields(ubuf):
                        if hn2 == 1:
                            hid = hv2
                        elif hn2 == 2:
                            tgt = read_pos(hv2)
                    if ents.get(hid, (None,))[0] != cad_team:
                        continue
                    heal_ev += 1
                    if tgt in core_tiles[cad_team]:
                        healcore_ev += 1
                        mark(hid, "heal_core")
                    else:
                        b = bldg_at.get(tgt)
                        u = bot_at.get(tgt)
                        if b is not None and ents.get(b, (None,))[0] == cad_team:
                            mark(hid, "heal_bldg")
                        elif u is not None and ents.get(u, (None,))[0] == cad_team:
                            mark(hid, "heal_bot")
                        else:
                            mark(hid, "heal_other")
                elif unum == 16:                                 # builderBuild
                    bid2 = None
                    for bn2, _bw2, bv2 in fields(ubuf):
                        if bn2 == 1:
                            bid2 = bv2
                    if ents.get(bid2, (None,))[0] != cad_team:
                        continue
                    bbuild += 1
                    mark(bid2, "build")

        led = dict.fromkeys(LEDGER, 0)
        seat_led = dict.fromkeys(LEDGER, 0)
        off_led = dict.fromkeys(LEDGER, 0)
        idle_free = idle_acd = idle_mcd = 0
        for b in start:
            lab = label.get(b, "idle")
            led[lab] += 1
            (seat_led if start_pos.get(b) in ORTH else off_led)[lab] += 1
            if lab in ("build", "attack", "heal_core", "heal_bldg",
                       "heal_bot", "heal_other"):
                stats["act_cd_viol"] += 1 if cd_a0.get(b, 0) else 0
                stats["act_n"] += 1
            elif lab == "move":
                stats["mov_cd_viol"] += 1 if cd_m0.get(b, 0) else 0
                stats["mov_n"] += 1
            elif lab == "idle":
                a0, m0 = cd_a0.get(b, 0), cd_m0.get(b, 0)
                if a0 == 0 and m0 == 0:
                    idle_free += 1
                elif a0 > 0 and m0 > 0:
                    idle_acd += 1
                    idle_mcd += 1
                elif a0 > 0:
                    idle_acd += 1
                else:
                    idle_mcd += 1
        free_act = sum(1 for b in start if cd_a0.get(b, 0) == 0)
        free_move = sum(1 for b in start if cd_m0.get(b, 0) == 0)
        bots_end = sum(1 for t, k in ents.values()
                       if t == cad_team and k == "builder_bot")
        # the core's own spawn shows as a placeEntity builder_bot; keep the
        # "build actions" figure comparable with the lockout cut, which counted
        # every first placeEntity except the two seeded cores.
        out.write("\t".join(str(v) for v in [
            name, rnd,
            hp[core_id[cad_team]], dmg[cad_team], healhp[cad_team],
            hp[core_id[us_team]], dmg[us_team],
            builds, bbuild,
            by_kind["conveyor"], by_kind["splitter"], by_kind["harvester"],
            by_kind["barrier"], by_kind["gunner"], by_kind["sentinel"],
            by_kind["launcher"], by_kind["builder_bot"],
            heal_ev, healcore_ev, batk, batk_core,
            moves, thrown_ev,
            len(start), bots_end, born, died,
            len(seats), collar_bots,
            ti[cad_team], ammo[cad_team],
            lost["any"], lost["conv"], lost["harv"], lost["turret"],
        ] + [led[k] for k in LEDGER] + [seat_led[k] for k in LEDGER]
            + [off_led[k] for k in LEDGER]
            + [n_cheb, n_near, n_mid, n_far, mind2_sum,
               free_act, free_move, idle_free, idle_acd, idle_mcd,
               bld_home, bld_mid, bld_fwd]
            + [out_n, tled_n]) + "\n")
        stats["rounds"] += 1
        for c in (cd_a, cd_m):
            for k in list(c):
                if c[k] > 0:
                    c[k] -= 1
    return True


def _relocate(pos_of, bot_at, eid, to):
    old = pos_of.get(eid)
    if old is not None and bot_at.get(old) == eid:
        del bot_at[old]
    pos_of[eid] = to
    bot_at[to] = eid


def _packed(buf):
    i = 0
    while i < len(buf):
        v = s = 0
        while True:
            b = buf[i]
            i += 1
            v |= (b & 0x7F) << s
            if not b & 0x80:
                break
            s += 7
        yield v


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
        if decode(p, int(r["cad_team"]), out, stats):
            n += 1
    out.close()
    print(f"decoded {n}/{len(rows)} CAD games, {stats['rounds']} rounds",
          file=sys.stderr)
    print("VALIDATION updateHp sign census: "
          f"neg={stats['hp_neg']} pos={stats['hp_pos']} zero={stats['hp_zero']}",
          file=sys.stderr)
    print(f"VALIDATION collar ring: full-8 in {stats['orth8']} games, "
          f"truncated in {stats['orth_trunc']}", file=sys.stderr)
    print("VALIDATION cooldown tracking: acting bots with action_cd>0 at round "
          f"start = {stats['act_cd_viol']}/{stats['act_n']}; moving bots with "
          f"move_cd>0 = {stats['mov_cd_viol']}/{stats['mov_n']}", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
