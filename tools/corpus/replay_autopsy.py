#!/usr/bin/env python3
"""Single-game kill autopsy: build timeline + a self-checking core damage ledger.

Built on tools/replay_census.py (do not hand-roll another decoder).

Why this exists: census gives first-build rounds and end-state counts, and
replay_events gives BUILD/DEATH rows, but neither answers "what removed 500 HP
from the core, event by event". This does, and it CHECKS itself: the attributed
damage per source must equal the summed UpdateHp deltas on the core id. If the
two disagree the tool says so rather than reporting the pretty number.

Attribution rule (tools/replay_schema.md, "Damage-target law"):
  * BuilderAttack  {id, target} with target in the enemy core footprint and no
    unit standing on that tile -> 2 dmg to the core.
  * FireTurret     {from, to} with `to` in the enemy core footprint and no unit
    on that tile -> gunner 7 / sentinel 18, resolved by looking up which entity
    stands on `from`.
Unit-priority means a shot landing on a tile occupied by a builder bot hits the
bot, not the core; those events are counted separately as `absorbed`.

UpdateHp deltas are 64-bit two's-complement varints (18446744073709551609 == -7).

Usage:
    .venv/bin/python tools/corpus/replay_autopsy.py FILE [FILE...] [--upto N]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import (  # noqa: E402
    fields, read_pos, parse_entity, scalars, WIRE_LEN, WIRE_VARINT,
)

DMG = {"gunner": 7, "sentinel": 18}
U64 = 1 << 64


def signed(v: int) -> int:
    return v - U64 if v >= (1 << 63) else v


class Ent:
    __slots__ = ("id", "team", "pos", "kind", "born")

    def __init__(self, eid, team, pos, kind, born):
        self.id, self.team, self.pos, self.kind, self.born = eid, team, pos, kind, born


def autopsy(path: Path, upto: int, out):
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
    cores, w, h = [], 0, 0
    for num, _wire, value in fields(map_buf):
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
    corepos = {c["team"]: c["pos"] for c in cores}
    coreid = {c["team"]: c["id"] for c in cores}
    foot = {t: {(p[0] + dx, p[1] + dy) for dx in (0, 1) for dy in (0, 1)}
            for t, p in corepos.items()}

    ents = {c["id"]: Ent(c["id"], c["team"], c["pos"], "core", 0) for c in cores}
    occ = {}                                    # tile -> builder bot id (units only)
    builds = []                                 # (rnd, team, kind, pos)
    deaths = []                                 # (rnd, team, kind, pos)
    throws = []                                 # (rnd, thrower_team, bot_team, frm, to)
    # damage ledger: (victim_team, source_kind) -> dmg
    ledger = {}
    absorbed = {}
    hp_dmg = {0: 0, 1: 0}                       # summed NEGATIVE UpdateHp on each core
    hp_heal = {0: 0, 1: 0}                      # summed POSITIVE UpdateHp on each core
    hp_now = {0: 500, 1: 500}
    convert = {0: 0, 1: 0}                      # titanium converted to ammo
    batk_all = {0: 0, 1: 0}                     # every builderAttack, any target
    heal_all = {0: 0, 1: 0}
    firstblood = {}                             # victim_team -> first round core took dmg
    atk_by_bot = {}                             # bot id -> core attacks
    core_dmg_round = {0: {}, 1: {}}

    def bump(d, k, n=1):
        d[k] = d.get(k, 0) + n

    for rnd, turn_buf in enumerate(turn_bufs):
        for _n, _w2, update_buf in fields(turn_buf):
            for unum, _uw, ubuf in fields(update_buf):
                if unum == 1:                                    # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        if e.id in ents:                          # rotation re-emit
                            ents[e.id].pos = e.pos
                            continue
                        ents[e.id] = Ent(e.id, e.team, e.pos, e.kind, rnd)
                        if e.kind == "builder_bot":
                            occ[e.pos] = e.id
                        builds.append((rnd, e.team, e.kind, e.pos))
                elif unum == 2:                                  # moveBuilderBot
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    e = ents.get(eid)
                    if e is None or to is None:
                        continue
                    frm = e.pos
                    if occ.get(frm) == eid:
                        del occ[frm]
                    e.pos = to
                    occ[to] = eid
                    if abs(to[0] - frm[0]) + abs(to[1] - frm[1]) > 1:
                        cand = [o for o in ents.values()
                                if o.kind == "launcher" and
                                (o.pos[0] - frm[0]) ** 2 + (o.pos[1] - frm[1]) ** 2 <= 2]
                        tteams = {o.team for o in cand}
                        tteam = cand[0].team if len(tteams) == 1 else None
                        throws.append((rnd, tteam, e.team, frm, to))
                elif unum == 3:                                  # removeEntity
                    for rn, _rw, rv in fields(ubuf):
                        e = ents.pop(rv, None)
                        if e is None:
                            continue
                        if occ.get(e.pos) == rv:
                            del occ[e.pos]
                        deaths.append((rnd, e.team, e.kind, e.pos))
                elif unum == 5:                                  # updateHp
                    d = scalars(ubuf)
                    eid, delta = d.get(1), signed(d.get(2, 0))
                    for t in (0, 1):
                        if eid == coreid[t]:
                            hp_now[t] += delta
                            if delta < 0:
                                hp_dmg[t] -= delta
                                core_dmg_round[t][rnd] = core_dmg_round[t].get(rnd, 0) - delta
                                firstblood.setdefault(t, rnd)
                            else:
                                hp_heal[t] += delta
                elif unum == 12:                                 # fireTurret
                    frm = to = None
                    for fn, _fw, fv in fields(ubuf):
                        if fn == 1:
                            frm = read_pos(fv)
                        elif fn == 2:
                            to = read_pos(fv)
                    if to is None:
                        continue
                    shooter = None
                    for e in ents.values():
                        if e.kind in ("gunner", "sentinel") and e.pos == frm:
                            shooter = e
                            break
                    for t in (0, 1):
                        if to in foot[t]:
                            k = shooter.kind if shooter else "turret?"
                            if to in occ:
                                bump(absorbed, (t, k), DMG.get(k, 0))
                            else:
                                bump(ledger, (t, k), DMG.get(k, 0))
                elif unum == 13:                                 # builderAttack
                    aid = tgt = None
                    for an, _aw, av in fields(ubuf):
                        if an == 1:
                            aid = av
                        elif an == 2:
                            tgt = read_pos(av)
                    if tgt is None:
                        continue
                    a = ents.get(aid)
                    if a is not None:
                        batk_all[a.team] += 1
                    for t in (0, 1):
                        if tgt in foot[t]:
                            if tgt in occ:
                                bump(absorbed, (t, "builder_attack"), 2)
                            else:
                                bump(ledger, (t, "builder_attack"), 2)
                                bump(atk_by_bot, aid, 1)
                elif unum == 14:                                 # coreConvertAmmo
                    d = scalars(ubuf)
                    convert[d.get(1, 0)] = convert.get(d.get(1, 0), 0) + d.get(2, 0)
                elif unum == 15:                                 # builderHeal
                    d = scalars(ubuf)
                    a = ents.get(d.get(1))
                    if a is not None:
                        heal_all[a.team] += 1

    W = out.write
    W(f"\n================ {path.name} ================\n")
    W(f"map {w}x{h}  cores A@{corepos[0]} B@{corepos[1]}  "
      f"rounds={len(turn_bufs)}  winner={'AB'[winner] if winner is not None else '-'}"
      f"  cond={wincond}\n")

    W("\n-- build timeline (round <= %d) --\n" % upto)
    for team, tag in ((0, "A"), (1, "B")):
        seq = [b for b in builds if b[1] == team and b[0] <= upto]
        W(f"  {tag}: {len(seq)} builds\n")
        line = []
        for rnd, _t, kind, p in seq:
            line.append(f"r{rnd}:{kind}@{p[0]},{p[1]}")
        for i in range(0, len(line), 4):
            W("     " + "  ".join(line[i:i + 4]) + "\n")

    W("\n-- builder bot spawns --\n")
    for team, tag in ((0, "A"), (1, "B")):
        rs = [b[0] for b in builds if b[1] == team and b[2] == "builder_bot"]
        W(f"  {tag}: n={len(rs)} rounds={rs}\n")

    W("\n-- CORE DAMAGE LEDGER --\n")
    for t, tag in ((0, "A"), (1, "B")):
        rows = {k: v for (vt, k), v in ledger.items() if vt == t}
        abs_rows = {k: v for (vt, k), v in absorbed.items() if vt == t}
        tot = sum(rows.values())
        W(f"  core {tag} (hp end {hp_now[t]}): UpdateHp damage={hp_dmg[t]} "
          f"healed=+{hp_heal[t]}\n")
        W(f"     attributed: {rows}  total={tot}   "
          f"{'MATCH' if tot == hp_dmg[t] else 'MISMATCH by %+d' % (tot - hp_dmg[t])}\n")
        if abs_rows:
            W(f"     absorbed by a unit standing on the footprint: {abs_rows}\n")
        if t in firstblood:
            W(f"     first damage r{firstblood[t]}; per-round dmg: "
              f"{sorted(core_dmg_round[t].items())}\n")
    if atk_by_bot:
        W(f"  builder-attack core hits by bot id: {sorted(atk_by_bot.items())}\n")
    W(f"  builderAttack events (any target): A={batk_all[0]} B={batk_all[1]}\n")
    W(f"  builderHeal events:                A={heal_all[0]} B={heal_all[1]}\n")
    W(f"  titanium converted to ammo:        A={convert[0]} B={convert[1]}\n")

    W("\n-- launcher throws --\n")
    if not throws:
        W("  none\n")
    for rnd, tteam, bteam, frm, to in throws:
        ec = corepos[1 - bteam]
        before = (frm[0] - ec[0]) ** 2 + (frm[1] - ec[1]) ** 2
        after = (to[0] - ec[0]) ** 2 + (to[1] - ec[1]) ** 2
        W(f"  r{rnd} thrower={'AB'[tteam] if tteam is not None else '?'} "
          f"bot_team={'AB'[bteam]} {frm}->{to}  d2_to_enemy_core {before}->{after} "
          f"{'INSERT' if after < before else 'BACK'}\n")

    W("\n-- final unit positions (units only) --\n")
    for t, tag in ((0, "A"), (1, "B")):
        us = [e for e in ents.values() if e.team == t and
              e.kind in ("builder_bot", "gunner", "sentinel", "launcher")]
        ec = corepos[1 - t]
        for e in sorted(us, key=lambda e: e.id):
            d = (e.pos[0] - ec[0]) ** 2 + (e.pos[1] - ec[1]) ** 2
            W(f"  {tag} {e.kind:11s} #{e.id:<4d} at {e.pos}  born r{e.born:<3d} "
              f"d2_to_enemy_core={d}\n")

    W("\n-- deaths --\n")
    for rnd, t, kind, p in deaths:
        W(f"  r{rnd} {'AB'[t]} {kind} @{p}\n")


def main(argv):
    upto = 50
    files = []
    i = 0
    while i < len(argv):
        if argv[i] == "--upto":
            upto = int(argv[i + 1]); i += 2
        else:
            files.append(Path(argv[i])); i += 1
    for p in files:
        autopsy(p, upto, sys.stdout)


if __name__ == "__main__":
    main(sys.argv[1:])
