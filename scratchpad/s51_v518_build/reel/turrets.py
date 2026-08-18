#!/usr/bin/env python3
"""Per-turret ledger for the s51 rush autopsy, attributed via FireTurret.

`FireTurret { Pos from = 1; Pos to = 2; }` (update field 12, tools/replay_schema.md:94)
names the SHOOTER'S TILE, so every shot is attributable to a turret without
touching facing or line geometry.  Turrets are immovable, so tile -> turret is
unambiguous except across a rebuild on the same tile, which is counted and
reported (`tile_reuse`).

Per turret of ours: kind, pos, facing, built, died, life, shots, shots that
landed on the ENEMY CORE footprint, and the round of its first core hit.

Definitions used downstream:
  SIEGE turret  = one that ever put a shot on the enemy core footprint.
  DUD           = a turret that lived >= 20 rounds and never hit the enemy core
                  while its team held >= 10 ammo for >= 20 of those rounds.
                  (A sentinel cannot rotate — facing is permanent — so a dud is
                  permanent, not a phase.)

GUARD: total sentinel shots on the enemy core, summed over turrets, must equal
the count of -18 UpdateHp deltas on the enemy core id (the independent channel
used by attrib.py).  Both channels are decoded separately here.
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game")
from tools.replay_census import (  # noqa: E402
    WIRE_LEN, fields, parse_entity, parse_update_hp, read_pos, scalars,
)
from tape import dsq  # noqa: E402

DIRN = {0: "C", 1: "N", 2: "NE", 3: "E", 4: "SE", 5: "S", 6: "SW", 7: "W",
        8: "NW"}


def run(path: Path, our_team: int):
    data = path.read_bytes()
    mb = None
    turns = []
    for n, w, v in fields(data):
        if n == 1 and w == WIRE_LEN:
            mb = v
        elif n == 3 and w == WIRE_LEN:
            turns.append(v)
    cores = []
    for n, _w, v in fields(mb):
        if n == 4:
            c = {"id": 0, "team": 0, "pos": (0, 0)}
            for cn, _cw, cv in fields(v):
                if cn == 1:
                    c["id"] = cv
                elif cn == 2:
                    c["team"] = cv
                elif cn == 3:
                    c["pos"] = read_pos(cv)
            cores.append(c)
    cid = {c["team"]: c["id"] for c in cores}
    cpos = {c["team"]: c["pos"] for c in cores}
    foot = {t: {(p[0] + dx, p[1] + dy) for dx in (0, 1) for dy in (0, 1)}
            for t, p in cpos.items()}
    ctr = {t: (p[0] + .5, p[1] + .5) for t, p in cpos.items()}
    opp = 1 - our_team

    turrets = {}          # id -> record
    by_tile = {}          # pos -> live turret id
    tile_reuse = 0
    ents = {}
    ammo = {0: 0, 1: 0}
    ammo_series = []
    core_sent_hits = {0: 0, 1: 0}   # -18 deltas landing on team t's core
    for rnd, tb in enumerate(turns):
        for _n, _w, ub in fields(tb):
            for un, _uw, ubuf in fields(ub):
                if un == 1:
                    for en, _ew, eb in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(eb, rnd)
                        if e is None or e.id in ents:
                            continue
                        ents[e.id] = e
                        if e.kind in ("sentinel", "gunner", "launcher"):
                            if e.pos in by_tile:
                                tile_reuse += 1
                            by_tile[e.pos] = e.id
                            turrets[e.id] = dict(
                                id=e.id, team=e.team, kind=e.kind, pos=e.pos,
                                dir=DIRN.get(e.direction, e.direction),
                                built=rnd, died=None,
                                dsq_opp=dsq(e.pos, ctr[1 - e.team]),
                                dsq_own=dsq(e.pos, ctr[e.team]),
                                shots=0, core_shots=0, first_core=None,
                                funded_r=0)
                elif un == 3:
                    for rn, _rw, rv in fields(ubuf):
                        if rn == 1:
                            ents.pop(rv, None)
                            if rv in turrets and turrets[rv]["died"] is None:
                                turrets[rv]["died"] = rnd
                                if by_tile.get(turrets[rv]["pos"]) == rv:
                                    del by_tile[turrets[rv]["pos"]]
                elif un == 5:
                    eid, delta = parse_update_hp(ubuf)
                    if delta == -18:
                        for t in (0, 1):
                            if eid == cid[t]:
                                core_sent_hits[t] += 1
                elif un == 6:
                    for pn, _pw, pv in fields(ubuf):
                        if pn != 1:
                            continue
                        for tn, _tw, tv in fields(pv):
                            if tn in (1, 2):
                                ammo[tn - 1] = scalars(tv).get(7, 0)
                elif un == 12:
                    frm = to = None
                    for fn, _fw, fv in fields(ubuf):
                        if fn == 1:
                            frm = read_pos(fv)
                        elif fn == 2:
                            to = read_pos(fv)
                    tid = by_tile.get(frm)
                    if tid is not None:
                        t = turrets[tid]
                        t["shots"] += 1
                        if to in foot[1 - t["team"]]:
                            t["core_shots"] += 1
                            if t["first_core"] is None:
                                t["first_core"] = rnd
        ammo_series.append(dict(ammo))
        for tid in by_tile.values():
            if ammo[turrets[tid]["team"]] >= 10:
                turrets[tid]["funded_r"] += 1
    rounds = len(turns)
    for t in turrets.values():
        t["life"] = (t["died"] if t["died"] is not None else rounds) - t["built"]
    return dict(turrets=turrets, rounds=rounds, tile_reuse=tile_reuse,
                core_sent_hits=core_sent_hits, ammo=ammo_series,
                our=our_team, opp=opp)


def main():
    rows = list(csv.DictReader(open(HERE / "fired30.tsv"), delimiter="\t"))
    fails = []
    tr_out = []
    game_out = []
    for g in rows:
        our = 0 if g["seat"] == "A" else 1
        r = run(HERE / "replays" / (g["tag"] + ".replay26"), our)
        T = r["turrets"]
        # --- guard: two independent channels must agree -------------------
        for t_lbl, team in (("our", our), ("opp", r["opp"])):
            fired = sum(x["core_shots"] for x in T.values()
                        if x["team"] == team and x["kind"] == "sentinel")
            hp = r["core_sent_hits"][1 - team]
            if fired != hp:
                fails.append("%s %s: fireTurret core hits %d != UpdateHp -18 %d"
                             % (g["tag"], t_lbl, fired, hp))
        ours = [t for t in T.values() if t["team"] == our]
        siege = [t for t in ours if t["core_shots"] > 0]
        sents = [t for t in ours if t["kind"] == "sentinel"]
        # duds: sentinel, lived >=20, funded >=20, never hit the enemy core
        duds = [t for t in sents
                if t["life"] >= 20 and t["funded_r"] >= 20
                and t["core_shots"] == 0]
        dud_r = sum(t["funded_r"] for t in duds)
        for t in ours:
            tr_out.append(dict(tag=g["tag"], **{k: t[k] for k in (
                "id", "kind", "pos", "dir", "built", "died", "life",
                "dsq_opp", "dsq_own", "shots", "core_shots", "first_core",
                "funded_r")}))
        theirs = [t for t in T.values() if t["team"] == r["opp"]]
        their_siege = [t for t in theirs if t["core_shots"] > 0]
        game_out.append(dict(
            tag=g["tag"], map=g["map"], seed=g["seed"], seat=g["seat"],
            ours=g["ours"], cond=g["cond"], turn=int(g["turn"]),
            sent_n=len(sents),
            siege_n=len(siege),
            siege_first=min((t["first_core"] for t in siege), default=None),
            siege_shots=sum(t["core_shots"] for t in siege),
            siege_life=sum(t["life"] for t in siege),
            siege_funded=sum(t["funded_r"] for t in siege),
            dud_sent_n=len(duds), dud_funded_r=dud_r,
            their_siege_n=len(their_siege),
            their_siege_first=min((t["first_core"] for t in their_siege),
                                  default=None),
            their_siege_shots=sum(t["core_shots"] for t in their_siege),
            their_siege_life=sum(t["life"] for t in their_siege),
            tile_reuse=r["tile_reuse"],
        ))
    if fails:
        sys.stderr.write("GUARD FAIL (channel disagreement):\n  "
                         + "\n  ".join(fails) + "\n")
        raise SystemExit(2)
    sys.stderr.write("guard OK: fireTurret core-hit counts == UpdateHp -18 "
                     "counts for both teams in 30/30 games\n")
    for name, data in (("turret_ledger.tsv", tr_out),
                       ("turret_game.tsv", game_out)):
        cols = list(data[0].keys())
        with open(HERE / name, "w") as fh:
            fh.write("\t".join(cols) + "\n")
            for x in data:
                fh.write("\t".join("" if x[c] is None else str(x[c])
                                   for c in cols) + "\n")
        print("wrote", name, len(data), "rows")


if __name__ == "__main__":
    main()
