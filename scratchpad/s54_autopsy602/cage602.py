#!/usr/bin/env python3
"""tape602 CAGE + BELT autopsy decoder (read-only).

Q1: per-seal-tile lifecycle on the enemy core ring (built / never-attempted /
    built-then-lost, killer class, re-lay latency, eviction engagement,
    cage state at kill time).
Q2: harvester + conveyor/splitter death table (killer class + geometry),
    coverage-at-death by OUR live turret rays, re-lay ledger, delivered Ti.

Attribution law identical to scratchpad/s54_autopsy/tape30_deaths.py:
  FireTurret{from,to} -> victim = UNIT on `to` else BUILDING on `to`; dmg 7/18.
  BuilderAttack{id,tgt} -> victim = BUILDING on tgt; dmg 2.
Self-check: attributed damage in the death round == summed negative UpdateHp.
A removal with ZERO damage events in its round and no prior HP loss is OUR OWN
`destroy()` (engine emits no event for it) -- verified below by the control that
enemy removals never show that signature for our buildings.
"""
from __future__ import annotations
import sys, json, os
from pathlib import Path

ROOT = Path("/Users/junghard/Projects/Work/florent-code-game")
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import (fields, read_pos, parse_entity, scalars,
                           WIRE_LEN, WIRE_VARINT, packed_varints)

U64 = 1 << 64
ENV_WALL = 1
ENV_ORE = 2
DMG = {"gunner": 7, "sentinel": 18}
BELTK = ("conveyor", "splitter")
DIRDELTA = {0: (0, 0), 1: (0, -1), 2: (1, -1), 3: (1, 0), 4: (1, 1),
            5: (0, 1), 6: (-1, 1), 7: (-1, 0), 8: (-1, -1)}
LAP_SEAL_IDX = (1, 2, 4, 5, 7, 8, 10, 11)
CARD = ((0, -1), (1, 0), (0, 1), (-1, 0))


def signed(v):
    return v - U64 if v >= (1 << 63) else v


def footprint(p):
    return {(p[0] + dx, p[1] + dy) for dx in (0, 1) for dy in (0, 1)}


def dsq_foot(pos, corenw):
    ox, oy = corenw
    dx = pos[0] - ox
    dx = -dx if dx < 0 else (dx - 1 if dx > 1 else 0)
    dy = pos[1] - oy
    dy = -dy if dy < 0 else (dy - 1 if dy > 1 else 0)
    return dx * dx + dy * dy


def cage_lap(o):
    ox, oy = o
    return [(ox - 1, oy - 1), (ox, oy - 1), (ox + 1, oy - 1), (ox + 2, oy - 1),
            (ox + 2, oy), (ox + 2, oy + 1), (ox + 2, oy + 2),
            (ox + 1, oy + 2), (ox, oy + 2), (ox - 1, oy + 2),
            (ox - 1, oy + 1), (ox - 1, oy)]


def ray_tiles(pos, kind, direction, w, h):
    """Tiles a turret with a KNOWN facing covers (gunner r2<=13, sent r2<=32).
    Obstacles ignored -> UPPER bound on coverage (conservative for a gap claim)."""
    rmax = 13 if kind == "gunner" else (32 if kind == "sentinel" else 0)
    if not rmax or direction is None:
        return set()
    dx, dy = DIRDELTA.get(direction, (0, 0))
    if dx == 0 and dy == 0:
        return set()
    out = set()
    k = 1
    while (dx * k) ** 2 + (dy * k) ** 2 <= rmax:
        x, y = pos[0] + dx * k, pos[1] + dy * k
        if 0 <= x < w and 0 <= y < h:
            out.add((x, y))
        k += 1
    return out


class E:
    __slots__ = ("id", "team", "kind", "pos", "born", "hp", "maxhp", "dir")
    def __init__(s, i, t, k, p, b, hp, mx, d):
        s.id, s.team, s.kind, s.pos, s.born = i, t, k, p, b
        s.hp, s.maxhp, s.dir = hp, mx, d


def decode(path: Path, our: int):
    data = path.read_bytes()
    map_buf, turns, winner, wincond = None, [], None, ""
    for num, wire, val in fields(data):
        if num == 1 and wire == WIRE_LEN: map_buf = val
        elif num == 3 and wire == WIRE_LEN: turns.append(val)
        elif num == 4 and wire == WIRE_VARINT: winner = val
        elif num == 6 and wire == WIRE_LEN: wincond = val.decode("utf-8", "replace")
    w = h = 0; tiles = []; cores = []
    for num, wire, val in fields(map_buf):
        if num == 1: w = val
        elif num == 2: h = val
        elif num == 3:
            row = []
            for rn, rw, rv in fields(val):
                if rn == 1:
                    row.extend(packed_varints(rv) if rw == WIRE_LEN else [rv])
            tiles.append(row)
        elif num == 4:
            c = {"id": 0, "team": 0, "pos": (0, 0)}
            for cn, _cw, cv in fields(val):
                if cn == 1: c["id"] = cv
                elif cn == 2: c["team"] = cv
                elif cn == 3: c["pos"] = read_pos(cv)
            cores.append(c)

    def env(p):
        x, y = p
        if 0 <= y < len(tiles) and 0 <= x < len(tiles[y]):
            return tiles[y][x]
        return ENV_WALL

    def ibp(p):
        return 0 <= p[0] < w and 0 <= p[1] < h

    them = 1 - our
    corepos = {c["team"]: c["pos"] for c in cores}
    coreid = {c["team"]: c["id"] for c in cores}
    foot = {t: footprint(p) for t, p in corepos.items()}

    lap = cage_lap(corepos[them])
    seal_all = [lap[i] for i in LAP_SEAL_IDX]
    seal_open = [t for t in seal_all if ibp(t) and env(t) != ENV_WALL]
    seal_set = set(seal_open)

    ents = {c["id"]: E(c["id"], c["team"], "core", c["pos"], 0, 500, 500, None)
            for c in cores}
    bld_at, bot_at = {}, {}
    for c in cores:
        for t in foot[c["team"]]:
            bld_at[t] = c["id"]

    # ---- per-seal-tile ledger
    lap_idx_of = {t: i for i, t in enumerate(lap)}
    seal = {t: {"tile": t, "env": env(t), "lap_idx": lap_idx_of[t],
                "our_builds": [], "our_losses": [],
                "enemy_bld_rounds": 0, "enemy_bld_kinds": {},
                "enemy_body_rounds": 0, "our_other_bld_rounds": 0,
                "empty_rounds": 0, "our_held_rounds": 0,
                "our_attacks": 0, "our_attack_rounds": set(),
                "walker_adj_rounds": 0, "walker_on_rounds": 0,
                "empty_and_adj_rounds": 0, "empty_and_on_rounds": 0,
                "empty_adj_funded_rounds": 0,
                "enemy_builder_adj_rounds": 0,
                "contested_and_ebadj_rounds": 0,
                "contested_rounds_walker_fwd": 0,
                "first_seen_enemy_bld": None}
            for t in seal_open}

    lap_visited = set()
    held_series = []            # held count per round
    seal_state_series = []      # (ours, enemy, empty) per round
    max_held = 0
    core_dead = {0: None, 1: None}
    core_hp = {0: 500, 1: 500}
    ti_collected = {0: 0, 1: 0}
    deliv_stacks = {0: 0, 1: 0}
    bank = {0: 500, 1: 500}
    bank_series = []
    core_dmg = {0: {}, 1: {}}        # team -> killer_kind -> total damage
    core_dmg_ev = {0: [], 1: []}     # (rnd, kind, team, pos, dmg)

    # ---- belt / harvester ledgers
    deaths = []
    our_builds_by_tile = {}     # tile -> list of (rnd, kind, id)
    harv_deaths_by_tile = {}
    belt_deaths_by_tile = {}
    our_turret_recs = {}
    checked = mismatch = 0
    nodmg_with_prior_hp = 0

    for rnd, tb in enumerate(turns):
        shadow_b, shadow_u = {}, {}
        hp_round, dmg_round = {}, {}
        removed = []
        births = []
        pend_attack = []
        pre_bld_at = dict(bld_at)
        for _n, _w2, ub0 in fields(tb):
            for un, _uw, ub in fields(ub0):
                if un == 1:
                    for en, _ew, eb in fields(ub):
                        if en != 1: continue
                        e = parse_entity(eb, rnd)
                        if e is None: continue
                        if e.id in ents:
                            old = ents[e.id]
                            if e.direction is not None: old.dir = e.direction
                            if old.pos != e.pos:
                                tbl = bot_at if old.kind == "builder_bot" else bld_at
                                if tbl.get(old.pos) == e.id: del tbl[old.pos]
                                tbl[e.pos] = e.id; old.pos = e.pos
                            continue
                        ne = E(e.id, e.team, e.kind, e.pos, rnd, e.hp, e.max_hp,
                               e.direction)
                        ents[e.id] = ne
                        if e.kind == "builder_bot":
                            bot_at[e.pos] = e.id
                        else:
                            bld_at[e.pos] = e.id
                        births.append(ne)
                        if e.team == our and e.kind != "builder_bot":
                            our_builds_by_tile.setdefault(e.pos, []).append(
                                (rnd, e.kind, e.id))
                        if e.team == our and e.kind in ("gunner", "sentinel", "launcher"):
                            our_turret_recs[e.id] = {
                                "id": e.id, "kind": e.kind, "pos": e.pos,
                                "dir": e.direction, "born": rnd, "died": None,
                                "killer": None, "shots": 0,
                                "dsq_ourcore": dsq_foot(e.pos, corepos[our]),
                                "dsq_theircore": dsq_foot(e.pos, corepos[them]),
                                "shot_victims": {}}
                        if e.team == our and e.pos in seal_set:
                            seal[e.pos]["our_builds"].append((rnd, e.kind, e.id))
                elif un == 2:
                    eid = to = None
                    for mn, _mw, mv in fields(ub):
                        if mn == 1: eid = mv
                        elif mn == 2: to = read_pos(mv)
                    e = ents.get(eid)
                    if e is None or to is None: continue
                    if bot_at.get(e.pos) == eid: del bot_at[e.pos]
                    e.pos = to; bot_at[to] = eid
                elif un == 3:
                    for _rn, _rw, rv in fields(ub):
                        e = ents.pop(rv, None)
                        if e is None: continue
                        if e.kind == "builder_bot":
                            if bot_at.get(e.pos) == rv: del bot_at[e.pos]
                            shadow_u[e.pos] = e
                        else:
                            if bld_at.get(e.pos) == rv: del bld_at[e.pos]
                            shadow_b[e.pos] = e
                        removed.append(e)
                        if rv in our_turret_recs and our_turret_recs[rv]["died"] is None:
                            our_turret_recs[rv]["died"] = rnd
                        for t in (0, 1):
                            if rv == coreid[t] and core_dead[t] is None:
                                core_dead[t] = rnd
                elif un == 4:
                    for _mn, _mw, mv in fields(ub):
                        frm = to = rid = None
                        for fn, _fw, fv in fields(mv):
                            if fn == 1: frm = read_pos(fv)
                            elif fn == 2: to = read_pos(fv)
                            elif fn == 3: rid = fv
                        if to is None: continue
                        for t in (0, 1):
                            if to in foot[t]:
                                deliv_stacks[t] += 1
                elif un == 5:
                    d = scalars(ub)
                    eid, delta = d.get(1), signed(d.get(2, 0))
                    e = ents.get(eid)
                    if e is not None: e.hp += delta
                    if delta < 0:
                        hp_round[eid] = hp_round.get(eid, 0) - delta
                    for t in (0, 1):
                        if eid == coreid[t]: core_hp[t] += delta
                elif un == 6:
                    for pn, _pw, pv in fields(ub):
                        if pn != 1: continue
                        for tn, _tw, tv in fields(pv):
                            if tn in (1, 2):
                                s = scalars(tv)
                                if 4 in s: ti_collected[tn - 1] = s[4]
                                bank[tn - 1] = s.get(1, 0)
                elif un == 12:
                    frm = to = None
                    for fn, _fw, fv in fields(ub):
                        if fn == 1: frm = read_pos(fv)
                        elif fn == 2: to = read_pos(fv)
                    if to is None: continue
                    sid = bld_at.get(frm)
                    sh = ents.get(sid) if sid is not None else shadow_b.get(frm)
                    skind = sh.kind if sh else "turret?"
                    steam = sh.team if sh else None
                    if sh is not None and sh.id in our_turret_recs:
                        our_turret_recs[sh.id]["shots"] += 1
                    vid = bot_at.get(to)
                    v = ents.get(vid) if vid is not None else None
                    if v is None: v = shadow_u.get(to)
                    if v is None:
                        b2 = bld_at.get(to)
                        v = ents.get(b2) if b2 is not None else shadow_b.get(to)
                    if v is None: continue
                    if sh is not None and sh.id in our_turret_recs:
                        k = f"{v.team}:{v.kind}"
                        d = our_turret_recs[sh.id]["shot_victims"]
                        d[k] = d.get(k, 0) + 1
                    dmg_round.setdefault(v.id, []).append(
                        (skind, sh.id if sh else None, steam, frm,
                         DMG.get(skind, 0)))
                    if v.kind == "core":
                        dd = DMG.get(skind, 0)
                        core_dmg[v.team][skind] = core_dmg[v.team].get(skind, 0) + dd
                        core_dmg_ev[v.team].append((rnd, skind, steam, frm, dd))
                elif un == 13:
                    aid = tgt = None
                    for an, _aw, av in fields(ub):
                        if an == 1: aid = av
                        elif an == 2: tgt = read_pos(av)
                    if tgt is None: continue
                    a = ents.get(aid)
                    b2 = bld_at.get(tgt)
                    v = ents.get(b2) if b2 is not None else shadow_b.get(tgt)
                    if v is not None:
                        dmg_round.setdefault(v.id, []).append(
                            ("peck", aid, a.team if a else None,
                             a.pos if a else None, 2))
                        if v.kind == "core":
                            core_dmg[v.team]["peck"] = core_dmg[v.team].get("peck", 0) + 2
                            core_dmg_ev[v.team].append(
                                (rnd, "peck", a.team if a else None,
                                 a.pos if a else None, 2))
                    pend_attack.append((aid, a.team if a else None, tgt))
        # ---- eviction engagement: OUR builder attacks on seal tiles
        for (aid, ateam, tgt) in pend_attack:
            if ateam == our and tgt in seal:
                seal[tgt]["our_attacks"] += 1
                seal[tgt]["our_attack_rounds"].add(rnd)

        # ---- deaths
        live_our_turrets = [(x.pos, x.kind, x.dir) for x in ents.values()
                            if x.team == our and x.kind in ("gunner", "sentinel")]
        cov = set()
        for (tp, tk, td) in live_our_turrets:
            cov |= ray_tiles(tp, tk, td, w, h)
        for e in removed:
            srcs = dmg_round.get(e.id, [])
            att = sum(s[4] for s in srcs)
            hpd = hp_round.get(e.id, 0)
            if srcs:
                checked += 1
                if att != hpd: mismatch += 1
            last = srcs[-1] if srcs else None
            rec = {"rnd": rnd, "id": e.id, "team": e.team, "kind": e.kind,
                   "pos": e.pos, "born": e.born, "life": rnd - e.born,
                   "killer_kind": last[0] if last else None,
                   "killer_team": last[2] if last else None,
                   "killer_pos": last[3] if last else None,
                   "nodamage": not srcs,
                   "hp_before_round": e.hp + hpd,
                   "maxhp": e.maxhp,
                   "covered_at_death": e.pos in cov,
                   "dsq_ourcore": dsq_foot(e.pos, corepos[our]),
                   "dsq_theircore": dsq_foot(e.pos, corepos[them])}
            if last and last[3] is not None:
                rec["killer_dsq_ourcore"] = dsq_foot(last[3], corepos[our])
                rec["killer_dsq_theircore"] = dsq_foot(last[3], corepos[them])
            deaths.append(rec)
            if not srcs and e.team == our and e.hp + hpd < e.maxhp:
                nodmg_with_prior_hp += 1
            if e.team == our and e.pos in seal_set:
                seal[e.pos]["our_losses"].append(rec)
            if e.team == our and e.kind == "harvester":
                harv_deaths_by_tile.setdefault(e.pos, []).append(rec)
            if e.team == our and e.kind in BELTK:
                belt_deaths_by_tile.setdefault(e.pos, []).append(rec)
            if e.id in our_turret_recs and our_turret_recs[e.id]["killer"] is None:
                our_turret_recs[e.id]["killer"] = last[0] if last else "none"

        # ---- seal occupancy snapshot (end of round)
        held = 0
        n_empty = n_enemy = 0
        bank_series.append(bank[our])
        for t in seal_open:
            s = seal[t]
            b = bld_at.get(t)
            empty_now = not (b is not None and b in ents)
            adj_now = False
            for dx, dy in CARD:
                q = (t[0] + dx, t[1] + dy)
                bb = bot_at.get(q)
                if bb is not None and bb in ents and ents[bb].team == our:
                    adj_now = True
                    break
            on_now = False
            bb = bot_at.get(t)
            if bb is not None and bb in ents and ents[bb].team == our:
                on_now = True
            eb_adj = False
            for dx, dy in CARD:
                q = (t[0] + dx, t[1] + dy)
                bb2 = bot_at.get(q)
                if bb2 is not None and bb2 in ents and ents[bb2].team == them:
                    eb_adj = True
                    break
            if eb_adj:
                s["enemy_builder_adj_rounds"] += 1
            contested_now = (not empty_now and b in ents and ents[b].team == them)
            if contested_now and eb_adj:
                s["contested_and_ebadj_rounds"] += 1
            if empty_now and adj_now:
                s["empty_and_adj_rounds"] += 1
                if bank[our] >= 6:
                    s["empty_adj_funded_rounds"] += 1
            if empty_now and on_now:
                s["empty_and_on_rounds"] += 1
            if b is not None and b in ents:
                if ents[b].team == our:
                    held += 1
                    s["our_held_rounds"] += 1
                    if ents[b].kind != "barrier":
                        s["our_other_bld_rounds"] += 1
                else:
                    s["enemy_bld_rounds"] += 1
                    n_enemy += 1
                    k = ents[b].kind
                    s["enemy_bld_kinds"][k] = s["enemy_bld_kinds"].get(k, 0) + 1
                    if s["first_seen_enemy_bld"] is None:
                        s["first_seen_enemy_bld"] = rnd
            else:
                s["empty_rounds"] += 1
                n_empty += 1
            u = bot_at.get(t)
            if u is not None and u in ents and ents[u].team == them:
                s["enemy_body_rounds"] += 1
            # our builder adjacency / standing
            for dx, dy in CARD:
                q = (t[0] + dx, t[1] + dy)
                bb = bot_at.get(q)
                if bb is not None and bb in ents and ents[bb].team == our:
                    s["walker_adj_rounds"] += 1
                    break
            bb = bot_at.get(t)
            if bb is not None and bb in ents and ents[bb].team == our:
                s["walker_on_rounds"] += 1
        for t in lap:
            bb = bot_at.get(t)
            if bb is not None and bb in ents and ents[bb].team == our:
                lap_visited.add(t)
        held_series.append(held)
        seal_state_series.append((held, n_enemy, n_empty))
        if held > max_held: max_held = held

    for s in seal.values():
        s["our_attack_rounds"] = sorted(s["our_attack_rounds"])

    return dict(file=path.name, side=our, w=w, h=h, rounds=len(turns),
                winner=winner, cond=wincond, corepos=corepos, coreid=coreid,
                lap=lap, seal_all=seal_all, seal_open=seal_open,
                seal={str(k): v for k, v in seal.items()},
                held_series=held_series, seal_state_series=seal_state_series,
                max_held=max_held,
                core_dead=core_dead, core_hp=core_hp,
                ti_collected=ti_collected, deliv_stacks=deliv_stacks,
                deaths=deaths,
                our_builds_by_tile={str(k): v for k, v in our_builds_by_tile.items()},
                harv_deaths_by_tile={str(k): v for k, v in harv_deaths_by_tile.items()},
                belt_deaths_by_tile={str(k): v for k, v in belt_deaths_by_tile.items()},
                our_turrets=our_turret_recs,
                checked=checked, mismatch=mismatch,
                core_dmg=core_dmg, core_dmg_ev=core_dmg_ev,
                bank_series=bank_series, lap_visited=sorted(lap_visited),
                tiles=tiles,
                final_ents=[(e.id, e.team, e.kind, e.pos, e.dir)
                            for e in ents.values()],
                lap_len=len(lap),
                nodmg_with_prior_hp=nodmg_with_prior_hp)


if __name__ == "__main__":
    r = decode(Path(sys.argv[1]), int(sys.argv[2]))
    print(json.dumps({k: r[k] for k in ("file", "rounds", "winner", "cond",
                                        "checked", "mismatch", "core_dead",
                                        "max_held", "ti_collected",
                                        "deliv_stacks", "nodmg_with_prior_hp")},
                     default=str))
    print("seal_open", r["seal_open"])
