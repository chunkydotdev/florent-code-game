#!/usr/bin/env python3
"""Opponent profile: team lazy. Built on tools/replay_census.py primitives."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import (  # noqa: E402
    fields, read_pos, parse_entity, scalars, WIRE_LEN, WIRE_VARINT,
)

U64 = 1 << 64
DIRN = {0: "C", 1: "N", 2: "NE", 3: "E", 4: "SE", 5: "S", 6: "SW", 7: "W", 8: "NW"}


def signed(v):
    return v - U64 if v >= (1 << 63) else v


def d2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


class Ent:
    __slots__ = ("id", "team", "pos", "kind", "born", "dirn", "maxhp", "hp")

    def __init__(self, eid, team, pos, kind, born, dirn, maxhp):
        self.id, self.team, self.pos, self.kind = eid, team, pos, kind
        self.born, self.dirn, self.maxhp = born, dirn, maxhp
        self.hp = maxhp


def parse(path: Path):
    data = path.read_bytes()
    map_buf, turn_bufs, winner, wincond = None, [], None, ""
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
        elif num == 4 and wire == WIRE_VARINT:
            winner = value
        elif num == 6 and wire == WIRE_LEN:
            wincond = value.decode("utf-8", "replace")
    w = h = 0
    cores, tiles = [], []
    for num, wire, value in fields(map_buf):
        if num == 1:
            w = value
        elif num == 2:
            h = value
        elif num == 3:
            row = []
            for rn, rw, rv in fields(value):
                if rn == 1:
                    if rw == WIRE_LEN:
                        i = 0
                        while i < len(rv):
                            r = s = 0
                            while True:
                                b = rv[i]; i += 1
                                r |= (b & 0x7F) << s
                                if not (b & 0x80):
                                    break
                                s += 7
                            row.append(r)
                    else:
                        row.append(rv)
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
    corepos = {c["team"]: c["pos"] for c in cores}
    coreid = {c["team"]: c["id"] for c in cores}
    foot = {t: {(p[0] + dx, p[1] + dy) for dx in (0, 1) for dy in (0, 1)}
            for t, p in corepos.items()}

    ents = {c["id"]: Ent(c["id"], c["team"], c["pos"], "core", 0, None, 500) for c in cores}
    dead = {}                     # id -> Ent (last known)
    builds, deaths, hpev = [], [], []
    fires, batks, bheals = [], [], []
    tled = {0: 0, 1: 0}
    execmax = {0: 0, 1: 0}
    execsum = {0: 0, 1: 0}
    execn = {0: 0, 1: 0}
    moves = []
    ammo_hist = []
    for rnd, turn_buf in enumerate(turn_bufs):
        for _n, _w2, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        if e.id in ents:
                            ents[e.id].pos = e.pos
                            ents[e.id].dirn = e.direction
                            continue
                        ents[e.id] = Ent(e.id, e.team, e.pos, e.kind, rnd, e.direction, e.max_hp)
                        builds.append((rnd, e.team, e.kind, e.pos, e.direction, e.id))
                elif unum == 2:
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    e = ents.get(eid)
                    if e is not None and to is not None:
                        frm = e.pos
                        e.pos = to
                        moves.append((rnd, e.team, eid, frm, to))
                elif unum == 3:
                    for rn, _rw, rv in fields(ubuf):
                        e = ents.pop(rv, None)
                        if e is None:
                            continue
                        dead[rv] = e
                        deaths.append((rnd, e.team, e.kind, e.pos, rv, e.born))
                elif unum == 5:
                    d = scalars(ubuf)
                    eid, delta = d.get(1), signed(d.get(2, 0))
                    e = ents.get(eid) or dead.get(eid)
                    if e is not None:
                        e.hp += delta
                        hpev.append((rnd, eid, e.team, e.kind, tuple(e.pos), delta))
                elif unum == 6:
                    for pn, _pw, pv in fields(ubuf):
                        if pn != 1:
                            continue
                        row = {}
                        for tn, _tw, tv in fields(pv):
                            if tn in (1, 2):
                                dd = scalars(tv)
                                row[tn - 1] = (dd.get(1, 0), dd.get(4, 0), dd.get(7, 0))
                        ammo_hist.append((rnd, row))
                elif unum == 9:
                    d = scalars(ubuf)
                    e = ents.get(d.get(1))
                    if e is not None:
                        t = e.team
                        execsum[t] += d.get(3, 0)
                        execn[t] += 1
                        execmax[t] = max(execmax[t], d.get(3, 0))
                        if d.get(4):
                            tled[t] += 1
                elif unum == 12:
                    frm = to = None
                    for fn, _fw, fv in fields(ubuf):
                        if fn == 1:
                            frm = read_pos(fv)
                        elif fn == 2:
                            to = read_pos(fv)
                    sh = None
                    for e in ents.values():
                        if e.kind in ("gunner", "sentinel") and tuple(e.pos) == frm:
                            sh = e
                            break
                    fires.append((rnd, frm, to, sh.team if sh else None,
                                  sh.kind if sh else "?", sh.id if sh else None))
                elif unum == 13:
                    d = scalars(ubuf)
                    aid = d.get(1)
                    tgt = read_pos(d.get(2)) if isinstance(d.get(2), bytes) else None
                    a = ents.get(aid)
                    batks.append((rnd, a.team if a else None, aid,
                                  tuple(a.pos) if a else None, tgt))
                elif unum == 15:
                    d = scalars(ubuf)
                    aid = d.get(1)
                    tgt = read_pos(d.get(2)) if isinstance(d.get(2), bytes) else None
                    a = ents.get(aid)
                    bheals.append((rnd, a.team if a else None, aid, tgt))
    return dict(name=path.name, w=w, h=h, rounds=len(turn_bufs), winner=winner,
                wincond=wincond, corepos=corepos, coreid=coreid, foot=foot,
                tiles=tiles, builds=builds, deaths=deaths, hpev=hpev, fires=fires,
                batks=batks, bheals=bheals, tled=tled, execmax=execmax,
                execsum=execsum, execn=execn, moves=moves, ents=ents, dead=dead,
                ammo_hist=ammo_hist)


SEAT = {}  # file -> lazy team index
for i in range(1, 6):
    SEAT[f"1ef56244-84a5-4136-ad8f-cf063b9fd3fe_game_{i}.replay26"] = 0
    SEAT[f"b9f3fab5-483a-443c-a2a3-695d69a8e915_game_{i}.replay26"] = 1


def report(g):
    L = SEAT[g["name"]]
    U = 1 - L
    lc, uc = g["corepos"][L], g["corepos"][U]
    lfoot, ufoot = g["foot"][L], g["foot"][U]
    P = print
    tag = g["name"].split("_game_")[0][:8] + " g" + g["name"].split("_game_")[1][0]
    P(f"\n########## {tag}  {g['w']}x{g['h']}  rounds={g['rounds']}  "
      f"winner={'AB'[g['winner']] if g['winner'] is not None else '-'} "
      f"cond={g['wincond']}  LAZY=seat {'AB'[L]} core@{lc}  US=seat {'AB'[U]} core@{uc} "
      f"lazy_won={g['winner']==L}")

    # ---- 1. opening ----
    P("-- LAZY opening (first build per kind; rel = pos - own core NW) --")
    seen = set()
    for rnd, t, kind, pos, dirn, eid in g["builds"]:
        if t != L or kind in seen:
            continue
        seen.add(kind)
        rel = (pos[0] - lc[0], pos[1] - lc[1])
        P(f"   r{rnd:<4d} {kind:<11s} @{tuple(pos)} rel={rel} d2own={d2(pos,lc)} "
          f"d2enemy={d2(pos,uc)} dir={DIRN.get(dirn,'-') if dirn is not None else '-'}")
    bb = [b[0] for b in g["builds"] if b[1] == L and b[2] == "builder_bot"]
    P(f"   builder spawns lazy: n={len(bb)} rounds={bb[:14]}{'...' if len(bb)>14 else ''}")
    bbu = [b[0] for b in g["builds"] if b[1] == U and b[2] == "builder_bot"]
    P(f"   builder spawns us  : n={len(bbu)} rounds={bbu[:14]}{'...' if len(bbu)>14 else ''}")

    # ---- turret placements ----
    P("-- LAZY turrets (all) --")
    for rnd, t, kind, pos, dirn, eid in g["builds"]:
        if t != L or kind not in ("gunner", "sentinel", "launcher"):
            continue
        do, de = d2(pos, lc), d2(pos, uc)
        P(f"   r{rnd:<4d} {kind:<8s} #{eid:<4d} @{tuple(pos)} d2own={do:<5d} d2enemy={de:<5d} "
          f"{'FWD' if de < do else 'HOME'} dir={DIRN.get(dirn,'-')}")
    P("-- US turrets (all) --")
    for rnd, t, kind, pos, dirn, eid in g["builds"]:
        if t != U or kind not in ("gunner", "sentinel", "launcher"):
            continue
        do, de = d2(pos, uc), d2(pos, lc)
        P(f"   r{rnd:<4d} {kind:<8s} #{eid:<4d} @{tuple(pos)} d2own={do:<5d} d2enemy={de:<5d} "
          f"{'FWD' if de < do else 'HOME'} dir={DIRN.get(dirn,'-')}")

    # ---- 2. core damage ledger by source (HP-verified) ----
    for victim, vlabel in ((L, "LAZY"), (U, "US")):
        cid = g["coreid"][victim]
        dmg = [(r, dl) for r, eid, _t, _k, _p, dl in g["hpev"] if eid == cid and dl < 0]
        heal = sum(dl for r, eid, _t, _k, _p, dl in g["hpev"] if eid == cid and dl > 0)
        tot = -sum(dl for _r, dl in dmg)
        if tot == 0:
            P(f"-- core {vlabel}: untouched (0 dmg, heal +{heal})")
            continue
        first = dmg[0][0]
        # attribute by delta size
        by = {}
        for _r, dl in dmg:
            by[-dl] = by.get(-dl, 0) + 1
        P(f"-- core {vlabel}: dmg={tot} heal=+{heal} first_dmg=r{first} "
          f"delta_histogram={dict(sorted(by.items()))}")
        # who was firing at the core footprint
        vf = g["foot"][victim]
        shooters = {}
        for rnd, frm, to, tteam, kind, sid in g["fires"]:
            if to in vf:
                shooters[(kind, sid, frm)] = shooters.get((kind, sid, frm), 0) + 1
        for (kind, sid, frm), n in sorted(shooters.items(), key=lambda kv: -kv[1]):
            P(f"      fire->core: {kind} #{sid} from {frm} x{n} "
              f"(d2 to victim core={d2(frm, g['corepos'][victim])})")
        atk = {}
        for rnd, at, aid, apos, tgt in g["batks"]:
            if tgt in vf:
                atk[(at, aid)] = atk.get((at, aid), 0) + 1
        for (at, aid), n in sorted(atk.items(), key=lambda kv: -kv[1])[:8]:
            P(f"      builder_attack->core: bot #{aid} team {'AB'[at] if at is not None else '?'} x{n}")
        rds = sorted(r for r, _ in dmg)
        P(f"      dmg rounds: r{rds[0]}..r{rds[-1]} n={len(rds)}")

    # ---- 3. economy over time ----
    P("-- economy (lazy) --")
    for kind in ("harvester", "conveyor", "splitter", "barrier"):
        bl = [(b[0], tuple(b[3])) for b in g["builds"] if b[1] == L and b[2] == kind]
        dl = [(d[0], tuple(d[3])) for d in g["deaths"] if d[1] == L and d[2] == kind]
        alive = []
        for chk in (50, 100, 150, 200, 300, 500, 999):
            if chk > g["rounds"]:
                break
            n = len([1 for r, _ in bl if r <= chk]) - len([1 for r, _ in dl if r <= chk])
            alive.append(f"r{chk}:{n}")
        P(f"   {kind:<10s} built={len(bl):<3d} died={len(dl):<3d} alive[{' '.join(alive)}]")
    # rebuild latency at the same tile
    for kind in ("harvester", "conveyor", "splitter"):
        dl = [(d[0], tuple(d[3])) for d in g["deaths"] if d[1] == L and d[2] == kind]
        bl = [(b[0], tuple(b[3])) for b in g["builds"] if b[1] == L and b[2] == kind]
        reb, lat = 0, []
        for dr, dp in dl:
            cand = [r for r, p in bl if p == dp and r > dr]
            if cand:
                reb += 1
                lat.append(min(cand) - dr)
        if dl:
            P(f"   REBUILD {kind}: {reb}/{len(dl)} same-tile rebuilds, "
              f"latencies={sorted(lat)[:12]}")
    # heals on own buildings
    lb_tiles = {}
    for rnd, t, kind, pos, dirn, eid in g["builds"]:
        if t == L:
            lb_tiles.setdefault(tuple(pos), []).append(kind)
    hb = [(r, tgt) for r, t, aid, tgt in g["bheals"] if t == L]
    hcore = len([1 for r, tgt in hb if tgt in lfoot])
    hecon = len([1 for r, tgt in hb if tgt in lb_tiles and
                 any(k in ("harvester", "conveyor", "splitter", "barrier")
                     for k in lb_tiles[tuple(tgt)])])
    P(f"   builderHeal lazy total={len(hb)} on_own_core={hcore} on_own_econ_tiles={hecon}")
    hbu = [(r, tgt) for r, t, aid, tgt in g["bheals"] if t == U]
    P(f"   builderHeal us   total={len(hbu)}")

    # ---- 4. defense reaction ----
    # our arrival: first of (our build within d2<=36 of lazy core) or (our builderAttack on a lazy building) or (our bot within d2<=8 of lazy core)
    ev = []
    for rnd, t, kind, pos, dirn, eid in g["builds"]:
        if t == U and kind != "builder_bot" and d2(pos, lc) <= 36:
            ev.append((rnd, f"our {kind} built @{tuple(pos)} d2={d2(pos,lc)}"))
    lazy_bldg_tiles = set()
    for rnd, t, kind, pos, dirn, eid in g["builds"]:
        if t == L and kind != "builder_bot":
            lazy_bldg_tiles.add(tuple(pos))
    for rnd, at, aid, apos, tgt in g["batks"]:
        if at == U and (tgt in lazy_bldg_tiles or tgt in lfoot):
            ev.append((rnd, f"our builder #{aid} attacked {tgt}"))
    for rnd, t, eid, frm, to in g["moves"]:
        if t == U and d2(to, lc) <= 8:
            ev.append((rnd, f"our bot #{eid} stepped to {to} d2={d2(to,lc)}"))
    ev.sort()
    P("-- defence reaction --")
    if ev:
        P(f"   our first intrusion: r{ev[0][0]} {ev[0][1]}")
        arr = ev[0][0]
        resp = [(b[0], b[2], tuple(b[3]), d2(b[3], lc)) for b in g["builds"]
                if b[1] == L and b[2] in ("gunner", "sentinel", "launcher", "barrier")
                and b[0] >= arr and d2(b[3], lc) <= 60]
        if resp:
            P(f"   lazy first home-defence build after: r{resp[0][0]} {resp[0][1]} "
              f"@{resp[0][2]} d2own={resp[0][3]}  LATENCY={resp[0][0]-arr} rounds")
        else:
            P("   lazy home-defence build after intrusion: NONE")
        prior = [(b[0], b[2], tuple(b[3])) for b in g["builds"]
                 if b[1] == L and b[2] in ("gunner", "sentinel", "launcher", "barrier")
                 and b[0] < arr and d2(b[3], lc) <= 60]
        P(f"   lazy home-defence builds BEFORE intrusion: {prior[:6]}")
    else:
        P("   our units never intruded")
    # teardown of own turrets (no-damage removal)
    hp_ids = {eid for _r, eid, _t, _k, _p, _d in g["hpev"]}
    for team, lbl in ((L, "lazy"), (U, "us")):
        nod = [(d[0], d[2], tuple(d[3])) for d in g["deaths"]
               if d[1] == team and d[4] not in hp_ids]
        if nod:
            P(f"   {lbl} no-damage removals (crash / self_destruct / teardown): {nod}")

    # ---- 6. cpu ----
    P(f"-- cpu: tled lazy={g['tled'][L]} us={g['tled'][U]}  "
      f"execmax lazy={g['execmax'][L]}us us={g['execmax'][U]}us  "
      f"execmean lazy={g['execsum'][L]//max(1,g['execn'][L])}us "
      f"us={g['execsum'][U]//max(1,g['execn'][U])}us")

    # ---- ammo / titanium end ----
    if g["ammo_hist"]:
        last = g["ammo_hist"][-1][1]
        P(f"-- final players: lazy ti={last.get(L,(0,0,0))[0]} coll={last.get(L,(0,0,0))[1]} "
          f"ammo={last.get(L,(0,0,0))[2]} | us ti={last.get(U,(0,0,0))[0]} "
          f"coll={last.get(U,(0,0,0))[1]} ammo={last.get(U,(0,0,0))[2]}")


def main(argv):
    for p in argv:
        report(parse(Path(p)))


if __name__ == "__main__":
    main(sys.argv[1:])
