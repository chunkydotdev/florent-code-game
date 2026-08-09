#!/usr/bin/env python3
"""DWELL decoder -- consecutive rounds a victim stood in its killer's envelope.

DERIVED FROM `dc_decode.py` (same directory, preserved + validated).  What was
added, and nothing else was changed:

  1. Map TILES are parsed (field 3 of Map, row-major `tiles[y][x]`) -- needed
     because a WALL blocks a gunner ray.  dc_decode never needed terrain.
  2. Turret FACING is tracked (`parse_entity` already returns `direction`;
     dc_decode dropped it).  A direction-changing `placeEntity` re-emit is a
     rotate, so the facing is updated on re-emit -- corpus-howto trap 1 in its
     other half: the re-emit is not a build, but it IS a rotation.
  3. Turret ENVELOPES are reconstructed per round, from docs/game-model.md:270-296
     (measured, not assumed):
       * gunner   -- single-tile-wide forward ray along facing, d2 <= 13,
                     stops AT the first targetable tile (any builder bot or any
                     building, either team); walls block and are not targetable.
       * sentinel -- same single-tile-wide ray, d2 <= 32, never blocked.
     A RADIUS-only variant (d2 <= 13 / <= 32, facing and blocking ignored) is
     computed alongside as a strict upper bound.
  4. Per-round per-builder COVER HISTORY: which enemy turret ids covered each of
     our live builders at END of round.  Turret existence is implicit -- a turret
     that is not alive is not in the cover map, so a turret built at r100 cannot
     cover anything at r90.
  5. The killer's ENTITY ID is recorded on the death row (dc_decode kept only the
     shooter tile).  Dwell walks back by id, so a turret rebuilt on a hot tile is
     a different turret and inherits none of its predecessor's dwell.
  6. Two new outputs: a per-builder-round exposure/hazard table (the control) and
     a fireTurret-vs-envelope validation table.

Everything else -- the death classification, the S1 ordering trap handling, the
two's-complement HP varint, the band definitions -- is dc_decode.py verbatim.

Usage:  python dwell_decode.py <outdir> <join.tsv> <replay...>
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

DMG = {"gunner": 7, "sentinel": 18}
HOME_D2 = 32
GUN_R2 = 13
SEN_R2 = 32
VISION_R2 = 20          # builder bot vision radius squared
ENV_WALL = 1
TURRETS = ("gunner", "sentinel")


def s64(v):
    return v - (1 << 64) if v >= (1 << 63) else v


def d2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def ray(pos, direction, r2, w, h):
    """Tiles on a turret's single-tile-wide ray, ignoring blocking."""
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


def disc(pos, r2, w, h):
    x, y = pos
    rr = int(r2 ** 0.5)
    out = []
    for dx in range(-rr, rr + 1):
        for dy in range(-rr, rr + 1):
            if dx == 0 and dy == 0:
                continue
            if dx * dx + dy * dy > r2:
                continue
            tx, ty = x + dx, y + dy
            if 0 <= tx < w and 0 <= ty < h:
                out.append((tx, ty))
    return out


def decode(path: Path, our_team: int):
    data = path.read_bytes()
    map_buf, turn_bufs = None, []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if map_buf is None:
        return None
    w = h = 0
    tiles = []
    cores = []
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
    nr = len(turn_bufs)
    enemy = 1 - our_team

    def is_wall(t):
        x, y = t
        return 0 <= y < len(tiles) and 0 <= x < len(tiles[y]) and \
            tiles[y][x] == ENV_WALL

    team_of, kind_of, pos_of, born, dir_of = {}, {}, {}, {}, {}
    bldg_at, bot_at = {}, {}
    for c in cores:
        team_of[c["id"]] = c["team"]
        kind_of[c["id"]] = "core"
        pos_of[c["id"]] = c["pos"]
        born[c["id"]] = 0
        for dx in (0, 1):
            for dy in (0, 1):
                bldg_at[(c["pos"][0] + dx, c["pos"][1] + dy)] = c["id"]

    hp_lost, hp_healed = {}, {}
    dmg_r, heal_r, shots_r, thrown_r, crashed_r, tled_n = {}, {}, {}, {}, {}, {}
    deaths = []
    death_rnd = {}

    # --- envelope machinery -------------------------------------------------
    # live ENEMY turrets only; our builders are the exposed population.
    et = {}                      # id -> dict(kind,pos,dir)
    rot_rounds = {}              # enemy turret id -> set of rounds it rotated
    rad_cover = {}               # tile -> set(turret id)   radius upper bound
    ray_cover = {}               # tile -> set(turret id) ray, blocking IGNORED
    sen_cover_ids = set()
    gun_ids = set()

    def add_disc(tid, kind, pos):
        for t in disc(pos, GUN_R2 if kind == "gunner" else SEN_R2, w, h):
            rad_cover.setdefault(t, set()).add(tid)

    def del_disc(tid, kind, pos):
        for t in disc(pos, GUN_R2 if kind == "gunner" else SEN_R2, w, h):
            s = rad_cover.get(t)
            if s:
                s.discard(tid)

    def add_ray(tid, kind, pos, direction):
        for t in ray(pos, direction,
                     SEN_R2 if kind == "sentinel" else GUN_R2, w, h):
            ray_cover.setdefault(t, set()).add(tid)

    def del_ray(tid, kind, pos, direction):
        for t in ray(pos, direction,
                     SEN_R2 if kind == "sentinel" else GUN_R2, w, h):
            s = ray_cover.get(t)
            if s:
                s.discard(tid)

    def turret_add(tid):
        e = et[tid]
        add_disc(tid, e["kind"], e["pos"])
        add_ray(tid, e["kind"], e["pos"], e["dir"])
        if e["kind"] == "sentinel":
            sen_cover_ids.add(tid)
        else:
            gun_ids.add(tid)

    def turret_del(tid):
        e = et.pop(tid)
        del_disc(tid, e["kind"], e["pos"])
        del_ray(tid, e["kind"], e["pos"], e["dir"])
        sen_cover_ids.discard(tid)
        gun_ids.discard(tid)

    def gunner_line(tid):
        """Live blocked ray for one gunner, against the CURRENT board."""
        e = et[tid]
        out = []
        for t in ray(e["pos"], e["dir"], GUN_R2, w, h):
            if is_wall(t):
                break                       # wall blocks, not targetable
            out.append(t)
            if t in bot_at or t in bldg_at:  # first targetable tile stops it
                break
        return out

    pos_hist = {}                # our builder id -> {rnd: pos} at END of round
    cov_line = {}                # our builder id -> {rnd: frozenset(turret id)}
    cov_rad = {}
    cov_ray = {}
    shotval = {"gunner_in": 0, "gunner_out": 0,
               "sentinel_in": 0, "sentinel_out": 0}

    for rnd, turn_buf in enumerate(turn_bufs):
        bot_start = dict(bot_at)
        bldg_start = dict(bldg_at)
        tile_owner = {}
        for p, b in bot_start.items():
            tile_owner.setdefault(p, set()).add(b)

        for _n, _w, ub in fields(turn_buf):
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
                            if kind_of[e.id] == "builder_bot":
                                if old != e.pos:
                                    if bot_at.get(old) == e.id:
                                        del bot_at[old]
                                    bot_at[e.pos] = e.id
                                    tile_owner.setdefault(e.pos, set()).add(e.id)
                                    pos_of[e.id] = e.pos
                            else:
                                moved = old != e.pos
                                rot = (e.id in et and
                                       et[e.id]["dir"] != e.direction)
                                if moved:
                                    if bldg_at.get(old) == e.id:
                                        del bldg_at[old]
                                    bldg_at[e.pos] = e.id
                                    pos_of[e.id] = e.pos
                                if rot and e.id in et:
                                    rot_rounds.setdefault(e.id, set()).add(rnd)
                                if e.id in et and (moved or rot):
                                    turret_del(e.id)
                                    et[e.id] = dict(kind=kind_of[e.id],
                                                    pos=e.pos, dir=e.direction)
                                    turret_add(e.id)
                                if e.id in dir_of:
                                    dir_of[e.id] = e.direction
                            continue
                        team_of[e.id] = e.team
                        kind_of[e.id] = e.kind
                        pos_of[e.id] = e.pos
                        born[e.id] = rnd
                        if e.kind == "builder_bot":
                            bot_at[e.pos] = e.id
                            hp_lost[e.id] = 0
                            hp_healed[e.id] = 0
                            dmg_r[e.id] = {}
                            shots_r[e.id] = {}
                            thrown_r[e.id] = set()
                            tled_n[e.id] = 0
                            tile_owner.setdefault(e.pos, set()).add(e.id)
                        else:
                            bldg_at[e.pos] = e.id
                            if e.kind in TURRETS:
                                dir_of[e.id] = e.direction
                                if e.team == enemy:
                                    et[e.id] = dict(kind=e.kind, pos=e.pos,
                                                    dir=e.direction)
                                    turret_add(e.id)
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
                    if max(abs(old[0] - to[0]), abs(old[1] - to[1])) > 1:
                        thrown_r.setdefault(eid, set()).add(rnd)
                    if bot_at.get(old) == eid:
                        del bot_at[old]
                    bot_at[to] = eid
                    pos_of[eid] = to
                    tile_owner.setdefault(to, set()).add(eid)
                elif unum == 3:                                 # removeEntity
                    for _rn, _rw, rv in fields(ubuf):
                        if rv not in pos_of:
                            continue
                        p = pos_of.pop(rv)
                        if kind_of.get(rv) == "builder_bot":
                            if bot_at.get(p) == rv:
                                del bot_at[p]
                            deaths.append((rv, team_of[rv], rnd, p))
                            death_rnd[rv] = rnd
                        else:
                            if bldg_at.get(p) == rv:
                                del bldg_at[p]
                            if rv in et:
                                turret_del(rv)
                elif unum == 5:                                 # updateHp
                    eid = delta = None
                    for hn, _hw, hv in fields(ubuf):
                        if hn == 1:
                            eid = hv
                        elif hn == 2:
                            delta = s64(hv)
                    if eid is None or delta is None:
                        continue
                    if kind_of.get(eid) == "builder_bot":
                        if delta < 0:
                            hp_lost[eid] = hp_lost.get(eid, 0) - delta
                            d = dmg_r.setdefault(eid, {})
                            d[rnd] = d.get(rnd, 0) - delta
                        else:
                            hp_healed[eid] = hp_healed.get(eid, 0) + delta
                            hh = heal_r.setdefault(eid, {})
                            hh[rnd] = hh.get(rnd, 0) + delta
                elif unum == 9:                                 # botOutput
                    eid, out, tled = None, b"", False
                    for bn, _bw, bv in fields(ubuf):
                        if bn == 1:
                            eid = bv
                        elif bn == 2:
                            out = bv
                        elif bn == 4:
                            tled = bool(bv)
                    if eid is None:
                        continue
                    if tled and eid in tled_n:
                        tled_n[eid] += 1
                    if out and b"Traceback" in out and eid not in crashed_r:
                        crashed_r[eid] = rnd
                elif unum == 12:                                # fireTurret
                    frm = to = None
                    for fn, _fw, fv in fields(ubuf):
                        if fn == 1:
                            frm = read_pos(fv)
                        elif fn == 2:
                            to = read_pos(fv)
                    if to is None:
                        continue
                    sid = bldg_start.get(frm)
                    if sid is None:
                        sid = bldg_at.get(frm)
                    sk = kind_of.get(sid, "?")
                    st = team_of.get(sid, -1)
                    # --- envelope validation, all shooters both teams --------
                    if sk in TURRETS and frm is not None and sid in dir_of:
                        dd = dir_of[sid]
                        if sk == "sentinel":
                            env = ray(frm, dd, SEN_R2, w, h)
                        else:
                            env = []
                            for t in ray(frm, dd, GUN_R2, w, h):
                                if is_wall(t):
                                    break
                                env.append(t)
                                if t in bot_at or t in bldg_at:
                                    break
                        shotval[sk + ("_in" if to in env else "_out")] += 1
                    cands = set(tile_owner.get(to, ()))
                    cur = bot_at.get(to)
                    if cur is not None:
                        cands.add(cur)
                    for bid in cands:
                        shots_r.setdefault(bid, {}).setdefault(rnd, []).append(
                            (sk, st, d2(frm, to) if frm else -1, sid, frm))

        # --- END OF ROUND: cover snapshot for our live builders -------------
        gcov = {}
        for tid in gun_ids:
            for t in gunner_line(tid):
                gcov.setdefault(t, set()).add(tid)
        for p, b in bot_at.items():
            if team_of.get(b) != our_team:
                continue
            pos_hist.setdefault(b, {})[rnd] = p
            rv = ray_cover.get(p)
            ln = set()
            if rv:
                ln |= (rv & sen_cover_ids)       # sentinels ignore obstacles
                cov_ray.setdefault(b, {})[rnd] = frozenset(rv)
            g = gcov.get(p)
            if g:
                ln |= g
            if ln:
                cov_line.setdefault(b, {})[rnd] = frozenset(ln)
            rd = rad_cover.get(p)
            if rd:
                cov_rad.setdefault(b, {})[rnd] = frozenset(rd)

    return dict(name=path.name, nr=nr, corepos=corepos, our_team=our_team,
                deaths=deaths, death_rnd=death_rnd, hp_lost=hp_lost,
                hp_healed=hp_healed, dmg_r=dmg_r, heal_r=heal_r,
                shots_r=shots_r,
                thrown_r=thrown_r, crashed_r=crashed_r, tled_n=tled_n,
                born=born, pos_hist=pos_hist, cov_line=cov_line,
                cov_rad=cov_rad, cov_ray=cov_ray, shotval=shotval, rot_rounds=rot_rounds, pos_of_static={},
                turret_pos={}, kind_of=kind_of, team_of=team_of)


DEATH_COLS = ["file", "team", "bid", "rnd", "x", "y", "band", "band_fp",
              "core_d2", "life", "cls", "killer", "n_shooters", "kid",
              "kx", "ky", "kkind", "kd2", "dwell_line", "dwell_rad",
              "dwell_line_vis", "vis_run", "seen_before", "thrown",
              "silent_pre", "kfire_rounds", "dmg_rounds", "heal_rounds",
              "kborn", "krot_now", "victim_moved", "dwell_ray", "ray_prev",
              "entry_d2"]
EXPO_COLS = ["file", "team", "band", "cov", "cov_ray", "cov_rad",
             "died_next", "n"]
VAL_COLS = ["file", "gunner_in", "gunner_out", "sentinel_in", "sentinel_out"]
RUN_COLS = ["file", "team", "band", "length", "ended_in_death", "n"]


def rows(R, kpos_of):
    us = R["our_team"]
    cp = R["corepos"][us]
    for (bid, team, rnd, pos) in R["deaths"]:
        if team != us:
            continue
        dr_hp = R["dmg_r"].get(bid, {}).get(rnd, 0)
        sh = R["shots_r"].get(bid, {}).get(rnd, [])
        sd = sum(DMG.get(s[0], 0) for s in sh)
        ng_e = sum(1 for s in sh if s[0] == "gunner" and s[1] != team)
        ns_e = sum(1 for s in sh if s[0] == "sentinel" and s[1] != team)
        ng_o = sum(1 for s in sh if s[0] == "gunner" and s[1] == team)
        ns_o = sum(1 for s in sh if s[0] == "sentinel" and s[1] == team)
        crash = R["crashed_r"].get(bid, -1)
        if dr_hp == 0 and not sh:
            cls, killer = "NO_DAMAGE", ("CRASH" if 0 <= crash <= rnd
                                        else "UNEXPLAINED")
        elif sh and sd == dr_hp and dr_hp > 0:
            cls = "ATTRIB"
            kinds = set()
            if ng_e or ns_e:
                kinds.add("ENEMY")
            if ng_o or ns_o:
                kinds.add("OWN")
            if ng_e + ng_o and ns_e + ns_o:
                tk = "MIXED"
            elif ns_e + ns_o:
                tk = "SENTINEL"
            elif ng_e + ng_o:
                tk = "GUNNER"
            else:
                tk = "OTHER"
            killer = ("ENEMY_" if kinds == {"ENEMY"} else
                      "OWN_" if kinds == {"OWN"} else "BOTH_") + tk
        else:
            cls, killer = "AMBIGUOUS", "?"

        enemy_shooters = {s[3] for s in sh if s[1] != team and s[0] in TURRETS}
        kid = kx = ky = -1
        kkind = "-"
        kd2 = -1
        dwell_l = dwell_r = dwell_v = vis_run = -1
        seen_before = -1
        silent_pre = kfire_rounds = dmg_rounds = heal_rounds = -1
        kborn = -1
        krot_now = victim_moved = -1
        dwell_ray = ray_prev = -1
        entry_d2 = -1
        if killer in ("ENEMY_GUNNER", "ENEMY_SENTINEL") and \
                len(enemy_shooters) == 1:
            kid = next(iter(enemy_shooters))
            kp = kpos_of.get(kid)
            if kp is not None:
                kx, ky = kp
                kkind = "gunner" if killer == "ENEMY_GUNNER" else "sentinel"
                kd2 = d2(pos, kp)
                kborn = R["born"].get(kid, -1)
                krot_now = 1 if rnd in R["rot_rounds"].get(kid, ()) else 0
                prev = R["pos_hist"].get(bid, {}).get(rnd - 1)
                victim_moved = -1 if prev is None else (0 if prev == pos else 1)
                cl = R["cov_line"].get(bid, {})
                cr = R["cov_rad"].get(bid, {})
                cy = R["cov_ray"].get(bid, {})
                ph = R["pos_hist"].get(bid, {})
                dwell_l = 0
                r = rnd - 1
                while r >= 0 and kid in cl.get(r, ()):
                    dwell_l += 1
                    r -= 1
                dwell_ray = 0
                r = rnd - 1
                while r >= 0 and kid in cy.get(r, ()):
                    dwell_ray += 1
                    r -= 1
                ray_prev = 1 if kid in cy.get(rnd - 1, ()) else 0
                dwell_r = 0
                r = rnd - 1
                while r >= 0 and kid in cr.get(r, ()):
                    dwell_r += 1
                    r -= 1
                # visibility over the LINE dwell window
                dwell_v = 0
                for r in range(rnd - dwell_l, rnd):
                    p = ph.get(r)
                    if p is not None and d2(p, kp) <= VISION_R2:
                        dwell_v += 1
                vis_run = 0
                r = rnd - 1
                while r >= 0 and kid in cl.get(r, ()):
                    p = ph.get(r)
                    if p is None or d2(p, kp) > VISION_R2:
                        break
                    vis_run += 1
                    r -= 1
                seen_before = 0
                for r, p in ph.items():
                    if r < rnd and d2(p, kp) <= VISION_R2:
                        seen_before = 1
                        break
                # the DECISION round: the last round before exposure began.
                # How far was the killer from the victim then?  (<= 20 means the
                # victim could see it at the moment it chose the exposing move.)
                ep = ph.get(rnd - dwell_l - 1)
                entry_d2 = -1 if ep is None else d2(ep, kp)
                # what happened DURING the dwell window: was the victim already
                # being shot by this turret, or was the exposure still silent?
                sr = R["shots_r"].get(bid, {})
                dm = R["dmg_r"].get(bid, {})
                hl = R["heal_r"].get(bid, {})
                win = range(rnd - dwell_l, rnd)
                kfire_rounds = sum(1 for r in win
                                   if any(s[3] == kid for s in sr.get(r, ())))
                dmg_rounds = sum(1 for r in win if dm.get(r, 0) > 0)
                heal_rounds = sum(1 for r in win if hl.get(r, 0) > 0)
                silent_pre = 0
                for r in win:
                    if any(s[3] == kid for s in sr.get(r, ())):
                        break
                    silent_pre += 1
        fp = min(d2(pos, (cp[0] + dx, cp[1] + dy))
                 for dx in (0, 1) for dy in (0, 1))
        yield "deaths", (R["name"], team, bid, rnd, pos[0], pos[1],
                         "HOME" if d2(pos, cp) <= HOME_D2 else "FWD",
                         "HOME" if fp <= HOME_D2 else "FWD",
                         d2(pos, cp), rnd - R["born"].get(bid, -1),
                         cls, killer, len(enemy_shooters), kid, kx, ky,
                         kkind, kd2, dwell_l, dwell_r, dwell_v, vis_run,
                         seen_before,
                         1 if rnd in R["thrown_r"].get(bid, ()) else 0,
                         silent_pre, kfire_rounds, dmg_rounds, heal_rounds,
                         kborn, krot_now, victim_moved, dwell_ray, ray_prev,
                         entry_d2)

    # control: every builder-round of OURS, covered or not, died-next or not
    acc = {}
    for bid, ph in R["pos_hist"].items():
        dr = R["death_rnd"].get(bid, -1)
        cl = R["cov_line"].get(bid, {})
        cy = R["cov_ray"].get(bid, {})
        cr = R["cov_rad"].get(bid, {})
        for r, p in ph.items():
            band = "HOME" if d2(p, cp) <= HOME_D2 else "FWD"
            cov = 1 if cl.get(r) else 0
            cvy = 1 if cy.get(r) else 0
            cvr = 1 if cr.get(r) else 0
            dn = 1 if dr == r + 1 else 0
            k = (band, cov, cvy, cvr, dn)
            acc[k] = acc.get(k, 0) + 1
    for (band, cov, cvy, cvr, dn), n in acc.items():
        yield "expo", (R["name"], R["our_team"], band, cov, cvy, cvr, dn, n)

    # control 2: maximal runs of consecutive in-envelope builder-rounds, and
    # whether the run ended in the bot's death.
    runs = {}
    for bid, ph in R["pos_hist"].items():
        dr = R["death_rnd"].get(bid, -1)
        cl = R["cov_line"].get(bid)
        if not cl:
            continue
        rs = sorted(cl)
        start = prev = rs[0]
        for r in rs[1:] + [None]:
            if r is not None and r == prev + 1:
                prev = r
                continue
            p = ph.get(prev, (0, 0))
            band = "HOME" if d2(p, cp) <= HOME_D2 else "FWD"
            died = 1 if dr == prev + 1 else 0
            k = (band, prev - start + 1, died)
            runs[k] = runs.get(k, 0) + 1
            if r is not None:
                start = prev = r
    for (band, ln, died), n in runs.items():
        yield "runs", (R["name"], R["our_team"], band, ln, died, n)
    sv = R["shotval"]
    yield "val", (R["name"], sv["gunner_in"], sv["gunner_out"],
                  sv["sentinel_in"], sv["sentinel_out"])


def work(args):
    p, ot = args
    try:
        R = decode(Path(p), ot)
    except Exception as exc:                                    # noqa: BLE001
        return ("ERR", str(p), repr(exc))
    if R is None:
        return ("ERR", str(p), "no map/cores")
    # turret positions are fixed for the life of an id; recover them from the
    # shot records (frm tile) so a dead turret is still locatable at analysis.
    kpos = {}
    for bid, per in R["shots_r"].items():
        for rn, lst in per.items():
            for s in lst:
                if s[3] is not None and s[4] is not None:
                    kpos[s[3]] = s[4]
    out = {"deaths": [], "expo": [], "val": [], "runs": []}
    for tbl, row in rows(R, kpos):
        out[tbl].append("\t".join(str(v) for v in row))
    return ("OK", out)


def main(argv):
    outdir, joinp = argv[0], argv[1]
    J = {r["file"]: int(r["our_team"])
         for r in csv.DictReader(open(joinp), delimiter="\t")
         if r["our_team"] not in ("", "None")}
    files = argv[2:]
    if len(files) == 1 and files[0].startswith("@"):
        files = [l.strip() for l in open(files[0][1:]) if l.strip()]
    tasks = [(f, J[os.path.basename(f)]) for f in files
             if os.path.basename(f) in J]
    fh = {"deaths": open(os.path.join(outdir, "dwell_deaths.tsv"), "w"),
          "expo": open(os.path.join(outdir, "dwell_expo.tsv"), "w"),
          "val": open(os.path.join(outdir, "dwell_val.tsv"), "w"),
          "runs": open(os.path.join(outdir, "dwell_runs.tsv"), "w")}
    fh["deaths"].write("\t".join(DEATH_COLS) + "\n")
    fh["expo"].write("\t".join(EXPO_COLS) + "\n")
    fh["val"].write("\t".join(VAL_COLS) + "\n")
    fh["runs"].write("\t".join(RUN_COLS) + "\n")
    bad = 0
    with Pool(8) as pool:
        for i, res in enumerate(pool.imap_unordered(work, tasks, chunksize=4)):
            if res[0] == "ERR":
                bad += 1
                print("ERR", res[1], res[2], file=sys.stderr)
                continue
            for k, lines in res[1].items():
                if lines:
                    fh[k].write("\n".join(lines) + "\n")
            if (i + 1) % 200 == 0:
                print(f"  ...{i+1}/{len(tasks)} ({bad} err)", file=sys.stderr,
                      flush=True)
    for f in fh.values():
        f.close()
    print(f"done {len(tasks)} files, {bad} errors", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
