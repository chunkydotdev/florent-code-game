#!/usr/bin/env python3
"""ARSENAL decoder (2026-08-09, research arm, session 24) — read-only.

EXTENDS `docs/research/scripts/side-lane-2026-08-09/dwell_decode.py`.

Reused verbatim from it: the board tracker (placeEntity with the rotate-re-emit
guard, moveBuilderBot, removeEntity, updateHp two's-complement varint), the
`ray()` envelope geometry, the map/wall decode, and the multiprocessing driver.

SEVEN DOCUMENTED ADDITIONS
  A1. Turret ray cover for **both** teams (dwell tracked only the enemy's),
      plus the live BLOCKED gunner line, so "throw their bot onto their own
      gunner's line" is answerable in both the raw-ray and the blocked-line
      form.
  A2. **Core ring occupancy** per team per round: the 12-tile Chebyshev-1 spawn
      ring (CORE_SPAWNING_RADIUS_SQ = 2) and the 8-tile orthogonal sub-ring
      (the only tiles that can heal the core or deliver into it), split by
      own-building / own-body / hostile-building / hostile-body.
  A3. **Map ore tiles** decoded (dwell needed only WALL) + harvester build
      positions + ore side-of-map, for the ore-concentration read.
  A4. **Kidnap opportunity scan** for rounds < 250: for every live enemy
      builder, could we have built a launcher on a tile adjacent to it, and is
      there a legal throw target inside r^2<=26 sitting on a turret line.
  A5. **Travel / reachability**: first round each team's builders hit distance
      milestones toward the enemy core, and first round they touch enemy-side
      ore. Observed travel, never straight-line.
  A6. **Resource-move interception geometry**: distributeResources moves
      classified live (as replay_flow.py does) AND tested against the tiles the
      OPPOSING team's builders physically occupied at any point, dilated one
      step — an upper bound on what a siphon could have touched.
  A7. **Live unit count** per team (core + builders + turrets), so the 50-unit
      cap can be excluded as a confounder in the spawn-rate read.

Traps honoured (docs/research/corpus-howto.md 1-4).

Usage:  .venv/bin/python arsenal_decode.py OUTDIR [JOIN.tsv] [LIMIT]
"""
from __future__ import annotations

import csv
import os
import sys
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import (fields, read_pos, parse_entity, packed_varints,  # noqa: E402
                           WIRE_LEN, DIRECTION_DELTA)

GUN_R2 = 13
SEN_R2 = 32
LAUNCH_R2 = 26          # LAUNCHER_VISION_RADIUS_SQ == throw range
PICKUP_D2 = 2           # Chebyshev-1 pickup (corpus/replay_throws.py attributes
                        # throwers at d2<=2; validated below on real throws)
PREFILT = 43            # d2(P,T) bound: d(L,T)<=sqrt(26) and d(L,P)<=sqrt(2)
                        # => d(P,T) <= 6.51 => d2 <= 42.4
KILL_WINDOW = 250       # PROGRAMME.md KILL_WINDOW_RND
MAX_UNITS = 50
ENV_WALL = 1
ENV_ORE = 2
TURRETS = ("gunner", "sentinel")
UNIT_KINDS = ("builder_bot", "gunner", "sentinel", "launcher", "core")
CARRIERS = ("conveyor", "splitter", "harvester")
CARD = ((0, -1), (1, 0), (0, 1), (-1, 0))
CHEB = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1))


def s64(v):
    return v - (1 << 64) if v >= (1 << 63) else v


def d2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def ray(pos, direction, r2, w, h):
    """Turret ray, blocking IGNORED. Verbatim from dwell_decode.py, where it
    validated at 99.991% (gunner) / 100.000% (sentinel) on 485,925 shots."""
    dx, dy = DIRECTION_DELTA.get(direction or 0, (0, 0))
    if dx == 0 and dy == 0:
        return []
    out = []
    x, y = pos
    k = 1
    while True:
        tx, ty = x + dx * k, y + dy * k
        if (dx * k) ** 2 + (dy * k) ** 2 > r2:
            break
        if not (0 <= tx < w and 0 <= ty < h):
            break
        out.append((tx, ty))
        k += 1
    return out


RING_COLS = ["file", "team", "rounds", "core_dead_rnd", "winner", "w", "h",
             "occ12_max", "occ8_max", "hst12_max", "hst8_max",
             "hstbody12_max", "hstbldg12_max", "ownb12_max",
             "free12_min", "free12_min_rnd",
             "f_occ12_6", "f_occ12_8", "f_occ12_10", "f_occ12_12",
             "f_occ8_4", "f_occ8_6", "f_occ8_8",
             "f_hst12_1", "f_hst12_2", "f_hst12_3", "f_hst12_4",
             "f_hst12_6", "f_hst12_8", "f_hst12_12",
             "f_hst8_1", "f_hst8_2", "f_hst8_4", "f_hst8_8",
             "f_bod_1", "f_bod_2", "f_bod_3", "f_bod_4", "f_bod_6",
             "n_free0", "n_occ12_12", "n_hst_ge1", "n_hst_ge3", "n_hst_ge6",
             "corehp_end", "tot_coredmg"]

SPAWN_COLS = ["file", "team", "free", "freesoft", "band", "atcap", "rounds",
               "spawns"]

STILE_COLS = ["file", "team", "band", "tilecls", "n_spawn",
              "n_tilernd"]

KID_COLS = ["file", "team", "rounds_scanned", "opp_bot_rounds",
            "k_any", "k_reach", "k_reach_next",
            "ff_their_ray_any", "ff_their_line_any",
            "ff_their_line_reach", "ff_ours_line_reach",
            "rnds_reach", "rnds_ff", "bots_reach", "bots_ff",
            "launchers_built_lt250", "throws_made_lt250"]

ORE_COLS = ["file", "team", "x", "y", "n_built", "first_rnd", "side"]

HAZ_COLS = ["file", "team", "metric", "j", "band50",
            "n25", "d25", "n50", "d50", "n100", "d100"]

MAP_COLS = ["file", "w", "h", "c0x", "c0y", "c1x", "c1y", "n_ore",
            "ore_side0", "ore_side1", "ore_neutral",
            "near_enemy_ore_d2_t0", "near_enemy_ore_d2_t1", "d2_cores"]

TRAV_COLS = ["file", "team", "r_half", "r_d2_32", "r_d2_8", "r_d2_2",
             "r_enemy_ore_adj", "r_enemy_ore_on", "r_nearest_enemy_ore",
             "n_visited", "min_pen_d2"]

FLOW_COLS = ["file", "team", "own_core", "own_net", "enemy_core", "enemy_net",
             "ground", "own_net_reach", "own_core_reach", "moves_total",
             "own_core_lt250", "own_net_lt250", "own_net_reach_lt250",
             "own_core_reach_lt250",
             # measured on the RECEIVING team's row: the engine credits
             # titanium to whoever owns the destination core, whatever team
             # pushed it (this is why econ.ti_collected_end > own_core).
             "in_core_any", "in_core_xteam", "in_core_any_lt250",
             "in_core_xteam_lt250"]

VAL_COLS = ["file", "ring12_ok", "ring8_ok", "onfp", "throws",
            "throw_pick_ok", "throw_range_ok", "bb_built", "bb_died",
            "deliv_stacks_t0", "deliv_stacks_t1", "maxunits0", "maxunits1"]


def decode(path: Path):
    data = path.read_bytes()
    map_buf, turn_bufs, winner = None, [], -1
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
        elif num == 4 and wire == 0:
            winner = value
    if map_buf is None:
        return None
    w = h = 0
    tiles, cores = [], []
    for num, wire, value in fields(map_buf):
        if num == 1:
            w = value
        elif num == 2:
            h = value
        elif num == 3:
            row = []
            for rnum, rwire, rvalue in fields(value):
                if rnum == 1:
                    row.extend(packed_varints(rvalue) if rwire == WIRE_LEN
                               else [rvalue])
            tiles.append(row)
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
        return None
    corepos = {c["team"]: c["pos"] for c in cores}
    id2team = {c["id"]: c["team"] for c in cores}
    nr = len(turn_bufs)

    def envt(t):
        x, y = t
        if 0 <= y < len(tiles) and 0 <= x < len(tiles[y]):
            return tiles[y][x]
        return ENV_WALL

    def is_wall(t):
        return envt(t) == ENV_WALL

    # --- A2 rings ---------------------------------------------------------- #
    footprint, fpset = {}, {0: set(), 1: set()}
    for t, (cx, cy) in corepos.items():
        for dx in (0, 1):
            for dy in (0, 1):
                footprint[(cx + dx, cy + dy)] = t
                fpset[t].add((cx + dx, cy + dy))
    r12, r8 = {0: set(), 1: set()}, {0: set(), 1: set()}
    for t in (0, 1):
        for (fx, fy) in fpset[t]:
            for dx, dy in CHEB:
                p = (fx + dx, fy + dy)
                if p not in footprint:
                    r12[t].add(p)
            for dx, dy in CARD:
                p = (fx + dx, fy + dy)
                if p not in footprint:
                    r8[t].add(p)
    ring12 = {t: sorted(r12[t]) for t in (0, 1)}
    ring8s = {t: set(r8[t]) for t in (0, 1)}
    # permanently unusable ring tiles (off-map or wall)
    blocked = {t: {p for p in ring12[t]
                   if not (0 <= p[0] < w and 0 <= p[1] < h) or is_wall(p)}
               for t in (0, 1)}

    # --- A3 ore ------------------------------------------------------------ #
    ore = [(x, y) for y in range(len(tiles)) for x in range(len(tiles[y]))
           if tiles[y][x] == ENV_ORE]
    oreset = set(ore)
    ore_side = {}
    for p in ore:
        a, b = d2(p, corepos[0]), d2(p, corepos[1])
        ore_side[p] = 0 if a < b else (1 if b < a else -1)
    enemy_ore = {t: [p for p in ore if ore_side[p] == 1 - t] for t in (0, 1)}
    near_eo = {t: min((d2(p, corepos[t]) for p in enemy_ore[t]), default=-1)
               for t in (0, 1)}
    near_eo_tile = {t: (min(enemy_ore[t], key=lambda p: d2(p, corepos[t]))
                        if enemy_ore[t] else None) for t in (0, 1)}

    # --- state ------------------------------------------------------------- #
    team_of, kind_of, pos_of, dir_of = dict(id2team), {}, {}, {}
    bldg_at, bot_at = {}, {}
    launcher_at = {0: set(), 1: set()}
    for c in cores:
        kind_of[c["id"]] = "core"
        pos_of[c["id"]] = c["pos"]
        for p in fpset[c["team"]]:
            bldg_at[p] = c["id"]
    bots = {0: set(), 1: set()}
    units = {0: 1, 1: 1}                       # cores count toward the cap
    maxunits = {0: 1, 1: 1}
    core_hp = {0: 500, 1: 500}
    core_dead = {0: -1, 1: -1}
    tot_dmg = {0: 0, 1: 0}

    tur = {}                                   # id -> dict(kind,pos,dir,team)
    ray_cover = {0: {}, 1: {}}

    def add_ray(tid):
        e = tur[tid]
        rc = ray_cover[e["team"]]
        for t in ray(e["pos"], e["dir"],
                     SEN_R2 if e["kind"] == "sentinel" else GUN_R2, w, h):
            rc.setdefault(t, 0)
            rc[t] += 1

    def del_ray(tid):
        e = tur[tid]
        rc = ray_cover[e["team"]]
        for t in ray(e["pos"], e["dir"],
                     SEN_R2 if e["kind"] == "sentinel" else GUN_R2, w, h):
            if t in rc:
                rc[t] -= 1
                if rc[t] <= 0:
                    del rc[t]

    ring_acc = {}
    for t in (0, 1):
        a = dict.fromkeys(RING_COLS[7:], 0)
        a["free12_min"] = 99
        a["free12_min_rnd"] = -1
        for k in RING_COLS:
            if k.startswith("f_"):
                a[k] = -1
        ring_acc[t] = a
    spawn_acc = {}
    stile = {}
    stexp = {}
    ser12 = {0: [], 1: []}
    serbod = {0: [], 1: []}
    kid = {t: dict.fromkeys(KID_COLS[2:], 0) for t in (0, 1)}
    kid_rnds = {0: set(), 1: set()}
    kid_rnds_ff = {0: set(), 1: set()}
    kid_bots = {0: set(), 1: set()}
    kid_bots_ff = {0: set(), 1: set()}
    prev_reach = {0: set(), 1: set()}          # (bid) with a reachable L last rnd
    harv = {}
    visited = {0: {}, 1: {}}   # tile -> FIRST round a builder of that team stood there
    trav = {t: {k: -1 for k in TRAV_COLS[2:]} for t in (0, 1)}
    for t in (0, 1):
        trav[t]["min_pen_d2"] = 10 ** 9
        trav[t]["n_visited"] = 0
    flow_acc = {t: dict.fromkeys(FLOW_COLS[2:], 0) for t in (0, 1)}
    moves_keep = []                            # (team, cls, dest)
    val = dict.fromkeys(VAL_COLS[1:], 0)
    val["ring12_ok"] = int(len(ring12[0]) == 12 and len(ring12[1]) == 12)
    val["ring8_ok"] = int(len(ring8s[0]) == 8 and len(ring8s[1]) == 8)

    def band(r):
        if r < 250:
            return f"r{50*(r//50)}-{50*(r//50)+50}"
        return "r250-500" if r < 500 else "r500+"

    for rnd, turn_buf in enumerate(turn_bufs):
        spawned = {0: 0, 1: 0}
        free_start, freesoft_start, atcap_start = {}, {}, {}
        ring_state = {}
        for t in (0, 1):
            f = fs = 0
            stt = {}
            for p in ring12[t]:
                b = bldg_at.get(p)
                u = bot_at.get(p)
                if p in blocked[t]:
                    stt[p] = "WALL"
                elif u is not None:
                    stt[p] = "BOT_OWN" if team_of.get(u) == t else "BOT_ENEMY"
                elif b is None:
                    stt[p] = "EMPTY"
                    f += 1
                    fs += 1
                else:
                    bt, bk = team_of.get(b), kind_of.get(b)
                    if bt == t and bk in ("conveyor", "splitter"):
                        stt[p] = "OWN_CONV"
                        fs += 1
                    elif bt == t:
                        stt[p] = "OWN_BLDG_" + (bk or "?")
                    elif bk in ("conveyor", "splitter"):
                        stt[p] = "ENEMY_CONV"
                    else:
                        stt[p] = "ENEMY_BLDG_" + (bk or "?")
            free_start[t] = f
            freesoft_start[t] = fs
            ring_state[t] = stt
            bb = band(rnd)
            for cl in stt.values():
                k2 = (t, bb, cl)
                stexp[k2] = stexp.get(k2, 0) + 1
            atcap_start[t] = int(units[t] >= MAX_UNITS)

        for _n, _w2, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:                                   # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        if e.id in pos_of:                      # re-emit
                            old = pos_of[e.id]
                            if kind_of.get(e.id) == "builder_bot":
                                if old != e.pos:
                                    if bot_at.get(old) == e.id:
                                        del bot_at[old]
                                    bot_at[e.pos] = e.id
                                    pos_of[e.id] = e.pos
                                    visited[e.team].setdefault(e.pos, rnd)
                                continue
                            moved = old != e.pos
                            rot = (e.id in tur and tur[e.id]["dir"] != e.direction)
                            if moved:
                                if bldg_at.get(old) == e.id:
                                    del bldg_at[old]
                                bldg_at[e.pos] = e.id
                                pos_of[e.id] = e.pos
                                if kind_of.get(e.id) == "launcher":
                                    launcher_at[e.team].discard(old)
                                    launcher_at[e.team].add(e.pos)
                            if e.id in tur and (moved or rot):
                                del_ray(e.id)
                                tur[e.id] = dict(kind=kind_of[e.id], pos=e.pos,
                                                 dir=e.direction, team=e.team)
                                add_ray(e.id)
                            if e.id in dir_of:
                                dir_of[e.id] = e.direction
                            continue
                        team_of[e.id] = e.team
                        kind_of[e.id] = e.kind
                        pos_of[e.id] = e.pos
                        if e.kind in UNIT_KINDS:
                            units[e.team] += 1
                            if units[e.team] > maxunits[e.team]:
                                maxunits[e.team] = units[e.team]
                        if e.kind == "builder_bot":
                            bot_at[e.pos] = e.id
                            bots[e.team].add(e.id)
                            visited[e.team].setdefault(e.pos, rnd)
                            val["bb_built"] += 1
                            spawned[e.team] += 1
                            cls = ring_state[e.team].get(e.pos, "OFFRING")
                            stile[(e.team, band(rnd), cls)] = \
                                stile.get((e.team, band(rnd), cls), 0) + 1
                            if e.pos in footprint:
                                val["onfp"] += 1
                        else:
                            bldg_at[e.pos] = e.id
                            if e.kind == "harvester":
                                k = (e.team, e.pos)
                                if k in harv:
                                    harv[k][0] += 1
                                else:
                                    harv[k] = [1, rnd]
                            elif e.kind == "launcher":
                                launcher_at[e.team].add(e.pos)
                                if rnd < KILL_WINDOW:
                                    kid[e.team]["launchers_built_lt250"] += 1
                            elif e.kind in TURRETS:
                                dir_of[e.id] = e.direction
                                tur[e.id] = dict(kind=e.kind, pos=e.pos,
                                                 dir=e.direction, team=e.team)
                                add_ray(e.id)
                elif unum == 2:                                 # moveBuilderBot
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid not in pos_of or to is None:
                        continue
                    old = pos_of[eid]
                    t = team_of.get(eid, 0)
                    if max(abs(old[0] - to[0]), abs(old[1] - to[1])) > 1:
                        val["throws"] += 1
                        okp = okr = 0
                        for tm in (0, 1):
                            for lp in launcher_at[tm]:
                                if d2(lp, old) <= PICKUP_D2:
                                    okp = 1
                                    if d2(lp, to) <= LAUNCH_R2:
                                        okr = 1
                        val["throw_pick_ok"] += okp
                        val["throw_range_ok"] += okr
                        if rnd < KILL_WINDOW:
                            kid[1 - t]["throws_made_lt250"] += 1
                    if bot_at.get(old) == eid:
                        del bot_at[old]
                    bot_at[to] = eid
                    pos_of[eid] = to
                    visited[t].setdefault(to, rnd)
                elif unum == 3:                                 # removeEntity
                    for _rn, _rw, rv in fields(ubuf):
                        if rv not in pos_of:
                            continue
                        p = pos_of.pop(rv)
                        k = kind_of.get(rv)
                        t = team_of.get(rv, 0)
                        if k in UNIT_KINDS:
                            units[t] -= 1
                        if k == "builder_bot":
                            if bot_at.get(p) == rv:
                                del bot_at[p]
                            bots[t].discard(rv)
                            val["bb_died"] += 1
                        else:
                            if bldg_at.get(p) == rv:
                                del bldg_at[p]
                            if k == "launcher":
                                launcher_at[t].discard(p)
                            if rv in tur:
                                del_ray(rv)
                                del tur[rv]
                            if k == "core":
                                if core_dead[t] < 0:
                                    core_dead[t] = rnd
                                for q in fpset[t]:
                                    bldg_at.pop(q, None)
                elif unum == 4:                                 # distributeResources
                    for rn, _rw, rv in fields(ubuf):
                        if rn != 1:
                            continue
                        frm = to = None
                        for mn, _mw, mv in fields(rv):
                            if mn == 1:
                                frm = read_pos(mv)
                            elif mn == 2:
                                to = read_pos(mv)
                        if frm is None or to is None:
                            continue
                        src = bldg_at.get(frm)
                        st = team_of.get(src)
                        if st is None:
                            continue
                        ft = footprint.get(to)
                        if ft is not None:
                            flow_acc[ft]["in_core_any"] += 1
                            if rnd < KILL_WINDOW:
                                flow_acc[ft]["in_core_any_lt250"] += 1
                            if ft != st:
                                flow_acc[ft]["in_core_xteam"] += 1
                                if rnd < KILL_WINDOW:
                                    flow_acc[ft]["in_core_xteam_lt250"] += 1
                            cls = "own_core" if ft == st else "enemy_core"
                        else:
                            db = bldg_at.get(to)
                            if db is not None and kind_of.get(db) in CARRIERS:
                                cls = "own_net" if team_of.get(db) == st \
                                    else "enemy_net"
                            else:
                                cls = "ground"
                        flow_acc[st][cls] += 1
                        flow_acc[st]["moves_total"] += 1
                        if cls in ("own_net", "own_core"):
                            if rnd < KILL_WINDOW:
                                flow_acc[st][cls + "_lt250"] += 1
                            moves_keep.append((st, cls, to, rnd))
                elif unum == 5:                                 # updateHp
                    eid = delta = None
                    for hn, _hw, hv in fields(ubuf):
                        if hn == 1:
                            eid = hv
                        elif hn == 2:
                            delta = s64(hv)
                    if eid in id2team and delta is not None:
                        t = id2team[eid]
                        core_hp[t] += delta
                        if delta < 0:
                            tot_dmg[t] += -delta
                        if core_hp[t] <= 0 and core_dead[t] < 0:
                            core_dead[t] = rnd

        # ---- END OF ROUND ------------------------------------------------- #
        for t in (0, 1):
            occ12 = occ8 = h12 = h8 = hb12 = hg12 = ob12 = 0
            for p in ring12[t]:
                b = bldg_at.get(p)
                u = bot_at.get(p)
                if b is None and u is None:
                    continue
                occ12 += 1
                orth = p in ring8s[t]
                if orth:
                    occ8 += 1
                if b is not None and team_of.get(b) == 1 - t:
                    h12 += 1
                    hg12 += 1
                    if orth:
                        h8 += 1
                elif u is not None and team_of.get(u) == 1 - t and b is None:
                    h12 += 1
                    hb12 += 1
                    if orth:
                        h8 += 1
                elif b is not None:
                    ob12 += 1
            a = ring_acc[t]
            a["occ12_max"] = max(a["occ12_max"], occ12)
            a["occ8_max"] = max(a["occ8_max"], occ8)
            a["hst12_max"] = max(a["hst12_max"], h12)
            a["hst8_max"] = max(a["hst8_max"], h8)
            a["hstbody12_max"] = max(a["hstbody12_max"], hb12)
            a["hstbldg12_max"] = max(a["hstbldg12_max"], hg12)
            a["ownb12_max"] = max(a["ownb12_max"], ob12)
            freev = 0
            for p in ring12[t]:
                if p in blocked[t] or p in bldg_at or p in bot_at:
                    continue
                freev += 1
            if freev < a["free12_min"]:
                a["free12_min"] = freev
                a["free12_min_rnd"] = rnd
            ser12[t].append(h12)
            serbod[t].append(hb12)
            for key, cond in (
                    ("f_bod_1", hb12 >= 1), ("f_bod_2", hb12 >= 2),
                    ("f_bod_3", hb12 >= 3), ("f_bod_4", hb12 >= 4),
                    ("f_bod_6", hb12 >= 6),
                    ("f_occ12_6", occ12 >= 6), ("f_occ12_8", occ12 >= 8),
                    ("f_occ12_10", occ12 >= 10), ("f_occ12_12", occ12 >= 12),
                    ("f_occ8_4", occ8 >= 4), ("f_occ8_6", occ8 >= 6),
                    ("f_occ8_8", occ8 >= 8),
                    ("f_hst12_1", h12 >= 1), ("f_hst12_2", h12 >= 2),
                    ("f_hst12_3", h12 >= 3), ("f_hst12_4", h12 >= 4),
                    ("f_hst12_6", h12 >= 6), ("f_hst12_8", h12 >= 8),
                    ("f_hst12_12", h12 >= 12),
                    ("f_hst8_1", h8 >= 1), ("f_hst8_2", h8 >= 2),
                    ("f_hst8_4", h8 >= 4), ("f_hst8_8", h8 >= 8)):
                if cond and a[key] < 0:
                    a[key] = rnd
            if freev <= 0:
                a["n_free0"] += 1
            if occ12 >= 12:
                a["n_occ12_12"] += 1
            if h12 >= 1:
                a["n_hst_ge1"] += 1
            if h12 >= 3:
                a["n_hst_ge3"] += 1
            if h12 >= 6:
                a["n_hst_ge6"] += 1
            key = (t, free_start[t], freesoft_start[t], band(rnd),
                   atcap_start[t])
            s = spawn_acc.setdefault(key, [0, 0])
            s[0] += 1
            s[1] += spawned[t]

        # ---- A5 travel ---------------------------------------------------- #
        for t in (0, 1):
            ec, oc = corepos[1 - t], corepos[t]
            tr = trav[t]
            nt = near_eo_tile[t]
            for bid in bots[t]:
                p = pos_of.get(bid)
                if p is None:
                    continue
                de = d2(p, ec)
                if de < tr["min_pen_d2"]:
                    tr["min_pen_d2"] = de
                if tr["r_half"] < 0 and de < d2(p, oc):
                    tr["r_half"] = rnd
                if tr["r_d2_32"] < 0 and de <= 32:
                    tr["r_d2_32"] = rnd
                if tr["r_d2_8"] < 0 and de <= 8:
                    tr["r_d2_8"] = rnd
                if tr["r_d2_2"] < 0 and de <= 2:
                    tr["r_d2_2"] = rnd
                if tr["r_enemy_ore_on"] < 0 and p in oreset and \
                        ore_side[p] == 1 - t:
                    tr["r_enemy_ore_on"] = rnd
                if tr["r_enemy_ore_adj"] < 0 or \
                        (nt is not None and tr["r_nearest_enemy_ore"] < 0):
                    for dx, dy in CARD:
                        q = (p[0] + dx, p[1] + dy)
                        if q in oreset and ore_side[q] == 1 - t and \
                                tr["r_enemy_ore_adj"] < 0:
                            tr["r_enemy_ore_adj"] = rnd
                        if nt is not None and q == nt and \
                                tr["r_nearest_enemy_ore"] < 0:
                            tr["r_nearest_enemy_ore"] = rnd

        # ---- A4 kidnap scan ----------------------------------------------- #
        if rnd < KILL_WINDOW:
            # live blocked gunner lines + sentinel rays, per team
            line = {0: set(), 1: set()}
            for tid, e in tur.items():
                if e["kind"] == "sentinel":
                    line[e["team"]].update(ray(e["pos"], e["dir"], SEN_R2, w, h))
                else:
                    for q in ray(e["pos"], e["dir"], GUN_R2, w, h):
                        if is_wall(q):
                            break
                        line[e["team"]].add(q)
                        if q in bot_at or q in bldg_at:
                            break
            for t in (0, 1):
                en = 1 - t
                if not bots[en]:
                    prev_reach[t] = set()
                    continue
                kid[t]["rounds_scanned"] += 1
                buildable = set()
                for bid in bots[t]:
                    p = pos_of.get(bid)
                    if p is None:
                        continue
                    for dx, dy in CARD:
                        q = (p[0] + dx, p[1] + dy)
                        if not (0 <= q[0] < w and 0 <= q[1] < h):
                            continue
                        if q in bldg_at or q in bot_at or is_wall(q):
                            continue
                        buildable.add(q)
                ray_e = list(ray_cover[en].keys())
                line_e = list(line[en])
                line_t = list(line[t])
                now_reach = set()
                for bid in bots[en]:
                    P = pos_of.get(bid)
                    if P is None:
                        continue
                    kid[t]["opp_bot_rounds"] += 1
                    cand_any, cand_reach = [], []
                    for dx, dy in CHEB:
                        L = (P[0] + dx, P[1] + dy)
                        if not (0 <= L[0] < w and 0 <= L[1] < h):
                            continue
                        if L in bldg_at or L in bot_at or is_wall(L):
                            continue
                        cand_any.append(L)
                        if L in buildable:
                            cand_reach.append(L)
                    if not cand_any:
                        continue
                    kid[t]["k_any"] += 1
                    if cand_reach:
                        kid[t]["k_reach"] += 1
                        kid_rnds[t].add(rnd)
                        kid_bots[t].add(bid)
                        now_reach.add(bid)
                        if bid in prev_reach[t]:
                            kid[t]["k_reach_next"] += 1

                    def hit(tiles_, cands):
                        for T in tiles_:
                            if d2(P, T) > PREFILT:
                                continue
                            if T in bldg_at or T in bot_at or is_wall(T):
                                continue
                            for L in cands:
                                if d2(L, T) <= LAUNCH_R2:
                                    return True
                        return False

                    if hit(ray_e, cand_any):
                        kid[t]["ff_their_ray_any"] += 1
                    if hit(line_e, cand_any):
                        kid[t]["ff_their_line_any"] += 1
                    if cand_reach:
                        if hit(line_e, cand_reach):
                            kid[t]["ff_their_line_reach"] += 1
                            kid_rnds_ff[t].add(rnd)
                            kid_bots_ff[t].add(bid)
                        if hit(line_t, cand_reach):
                            kid[t]["ff_ours_line_reach"] += 1
                prev_reach[t] = now_reach

    # ---- A6 deferred interception test ------------------------------------ #
    # first round at which a builder of team t stood ON or ORTHOGONALLY NEXT TO
    # each tile -- the earliest round that team could have acted on the tile.
    arr = {}
    for t in (0, 1):
        a = {}
        for p, r in visited[t].items():
            if a.get(p, 10 ** 9) > r:
                a[p] = r
            for dx, dy in CARD:
                q = (p[0] + dx, p[1] + dy)
                if a.get(q, 10 ** 9) > r:
                    a[q] = r
        arr[t] = a
    for st, cls, to, r in moves_keep:
        if arr[1 - st].get(to, 10 ** 9) <= r:
            flow_acc[st][cls + "_reach"] += 1
            if r < KILL_WINDOW:
                flow_acc[st][cls + "_reach_lt250"] += 1

    # ---- A8 hazard panel: P(this core dies within H | hostile ring = j) ----
    haz = {}
    for t in (0, 1):
        cd = core_dead[t]
        for metric, ser in (("occ", ser12[t]), ("bod", serbod[t])):
            for r, j in enumerate(ser):
                if cd >= 0 and r >= cd:
                    break            # stop at death: no exposure afterwards
                k = (t, metric, j, band(r))
                c = haz.setdefault(k, [0, 0, 0, 0, 0, 0])
                # RIGHT-CENSORING: a round only contributes exposure for
                # horizon H if the death is observable -- either the core did
                # die within H, or the replay runs H more rounds. Otherwise the
                # round is censored and dropped from BOTH numerator and
                # denominator, rather than silently counted as a survival.
                for idx, H in ((0, 25), (2, 50), (4, 100)):
                    died = cd >= 0 and cd - r <= H
                    if died:
                        c[idx] += 1
                        c[idx + 1] += 1
                    elif r + H < nr:
                        c[idx] += 1

    for t in (0, 1):
        val[f"deliv_stacks_t{t}"] = flow_acc[t]["in_core_any"]
        val[f"maxunits{t}"] = maxunits[t]
        trav[t]["n_visited"] = len(visited[t])

    name = path.name
    out = {k: [] for k in ("ring", "spawn", "kid", "ore", "map", "trav",
                           "flow", "val", "stile", "haz")}
    for t in (0, 1):
        a = ring_acc[t]
        a["corehp_end"] = core_hp[t]
        a["tot_coredmg"] = tot_dmg[t]
        out["ring"].append([name, t, nr, core_dead[t], winner, w, h] +
                           [a[k] for k in RING_COLS[7:]])
        kid[t]["rnds_reach"] = len(kid_rnds[t])
        kid[t]["rnds_ff"] = len(kid_rnds_ff[t])
        kid[t]["bots_reach"] = len(kid_bots[t])
        kid[t]["bots_ff"] = len(kid_bots_ff[t])
        out["kid"].append([name, t] + [kid[t][k] for k in KID_COLS[2:]])
        out["trav"].append([name, t] + [trav[t][k] for k in TRAV_COLS[2:]])
        out["flow"].append([name, t] + [flow_acc[t][k] for k in FLOW_COLS[2:]])
    for (t, f, fs2, b, cp), (rr, ss) in sorted(spawn_acc.items()):
        out["spawn"].append([name, t, f, fs2, b, cp, rr, ss])
    for k2 in sorted(set(stile) | set(stexp)):
        t, b, cl = k2
        out["stile"].append([name, t, b, cl, stile.get(k2, 0),
                             stexp.get(k2, 0)])
    for (t, p), (n, fr) in sorted(harv.items()):
        out["ore"].append([name, t, p[0], p[1], n, fr, ore_side[p]])
    for (t, metric, j, b50), c in sorted(haz.items()):
        out["haz"].append([name, t, metric, j, b50] + c)
    n0 = sum(1 for p in ore if ore_side[p] == 0)
    n1 = sum(1 for p in ore if ore_side[p] == 1)
    out["map"].append([name, w, h, corepos[0][0], corepos[0][1], corepos[1][0],
                       corepos[1][1], len(ore), n0, n1, len(ore) - n0 - n1,
                       near_eo[0], near_eo[1], d2(corepos[0], corepos[1])])
    out["val"].append([name] + [val[k] for k in VAL_COLS[1:]])
    return out


def work(p):
    try:
        return decode(Path(p))
    except Exception as exc:                                    # noqa: BLE001
        print(f"ERR {p}: {exc}", file=sys.stderr)
        return None


def main(argv):
    outdir = Path(argv[0])
    outdir.mkdir(parents=True, exist_ok=True)
    join = argv[1] if len(argv) > 1 else "corpus/join.tsv"
    files = []
    with open(join) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            fp = Path("replay_archive") / r["file"]
            if fp.exists():
                files.append(str(fp))
    if len(argv) > 2:
        files = files[:int(argv[2])]
    print(f"{len(files)} files", file=sys.stderr, flush=True)
    cols = {"ring": RING_COLS, "spawn": SPAWN_COLS, "kid": KID_COLS,
            "ore": ORE_COLS, "map": MAP_COLS, "trav": TRAV_COLS,
            "flow": FLOW_COLS, "val": VAL_COLS, "stile": STILE_COLS,
            "haz": HAZ_COLS}
    handles = {}
    for k, c in cols.items():
        handles[k] = open(outdir / f"ars_{k}.tsv", "w")
        handles[k].write("\t".join(c) + "\n")
    n = bad = 0
    with Pool(int(os.environ.get("NPROC", "10"))) as pool:
        for res in pool.imap_unordered(work, files, chunksize=4):
            n += 1
            if res is None:
                bad += 1
            else:
                for k, rows in res.items():
                    fh = handles[k]
                    for row in rows:
                        fh.write("\t".join(str(x) for x in row) + "\n")
            if n % 200 == 0:
                print(f"  {n}/{len(files)} ({bad} bad)", file=sys.stderr,
                      flush=True)
    for fh in handles.values():
        fh.close()
    print(f"done {n} files, {bad} bad", file=sys.stderr, flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
