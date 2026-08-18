#!/usr/bin/env python3
"""Per-round state tape from a .replay26, for the s51 rush autopsy.

Re-walks the turn stream using tools/replay_census.py primitives (fields,
parse_entity, parse_update_hp, read_pos) and emits, per round:

  our_core_hp  opp_core_hp  our_ti  our_ammo  opp_ti  opp_ammo
  our_sent  our_gun  our_lau  our_bot   (alive counts)
  our_bots_near   (our builder bots within dsq<=8 of the ENEMY core centre)
  our_sent_near   (our sentinels within dsq<=40 of the ENEMY core)
  opp_bots_near   (their builder bots within dsq<=8 of OUR core)

plus event lists: our sentinel builds/deaths, our launcher builds/deaths,
our builder-bot deaths near the enemy core.

WHICH TEAM IS OURS.  Determined by the caller (seat A -> team 0, seat B ->
team 1) and CROSS-CHECKED against the replay's own winner field vs the grid
tsv's `ours` column; a disagreement is an instrument alarm, not a row.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game")
from tools.replay_census import (  # noqa: E402
    WIRE_LEN, Entity, fields, parse_entity, parse_update_hp, read_pos, scalars,
)

CORE_MAXHP = 500


def dsq(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


class Tape:
    def __init__(self, path: Path, our_team: int):
        self.path = Path(path)
        self.our = our_team
        self.opp = 1 - our_team
        data = self.path.read_bytes()
        map_buf = None
        turn_bufs = []
        self.winner = None
        self.win_condition = ""
        for num, wire, value in fields(data):
            if num == 1 and wire == WIRE_LEN:
                map_buf = value
            elif num == 3 and wire == WIRE_LEN:
                turn_bufs.append(value)
            elif num == 4:
                self.winner = value
            elif num == 6 and wire == WIRE_LEN:
                self.win_condition = value.decode("utf-8", "replace")
        self.width = self.height = 0
        self.tiles = []
        self.cores = []
        for num, wire, value in fields(map_buf):
            if num == 1:
                self.width = value
            elif num == 2:
                self.height = value
            elif num == 4:
                core = {"id": 0, "team": 0, "pos": (0, 0)}
                for cnum, _cw, cval in fields(value):
                    if cnum == 1:
                        core["id"] = cval
                    elif cnum == 2:
                        core["team"] = cval
                    elif cnum == 3:
                        core["pos"] = read_pos(cval)
                self.cores.append(core)
        self.core_id = {c["team"]: c["id"] for c in self.cores}
        self.core_pos = {c["team"]: c["pos"] for c in self.cores}
        # centre of the 2x2 footprint
        self.core_c = {t: (p[0] + 0.5, p[1] + 0.5) for t, p in self.core_pos.items()}
        self._walk(turn_bufs)

    def _walk(self, turn_bufs):
        ents: dict[int, Entity] = {}
        ever: dict[int, tuple[int, str]] = {}
        for c in self.cores:
            e = Entity(c["id"], c["team"], c["pos"], "core", CORE_MAXHP,
                       CORE_MAXHP, None, 0)
            ents[c["id"]] = e
            ever[c["id"]] = (c["team"], "core")
        hp = {c["id"]: CORE_MAXHP for c in self.cores}
        self.rows = []
        self.builds = []   # (rnd, team, kind, id, pos)
        self.deaths = []   # (rnd, team, kind, id, pos, built_rnd)
        self.rounds = len(turn_bufs)
        players = [{}, {}]
        for rnd, tb in enumerate(turn_bufs):
            for _n, _w, ub in fields(tb):
                for unum, _uw, ubuf in fields(ub):
                    if unum == 1:                                # placeEntity
                        for en, _ew, ebuf in fields(ubuf):
                            if en != 1:
                                continue
                            ent = parse_entity(ebuf, rnd)
                            if ent is None:
                                continue
                            seen = ent.id in ents
                            ents[ent.id] = ent
                            if not seen:
                                ever[ent.id] = (ent.team, ent.kind)
                                hp[ent.id] = ent.hp
                                self.builds.append(
                                    (rnd, ent.team, ent.kind, ent.id, ent.pos))
                    elif unum == 2:                              # moveBuilderBot
                        eid = to = None
                        for mn, _mw, mv in fields(ubuf):
                            if mn == 1:
                                eid = mv
                            elif mn == 2:
                                to = read_pos(mv)
                        e = ents.get(eid)
                        if e is not None and to is not None:
                            e.pos = to
                    elif unum == 3:                              # removeEntity
                        for rn, _rw, rv in fields(ubuf):
                            if rn == 1:
                                e = ents.pop(rv, None)
                                if e is not None:
                                    self.deaths.append(
                                        (rnd, e.team, e.kind, e.id, e.pos,
                                         e.built_round))
                                hp.pop(rv, None)
                    elif unum == 5:                              # UpdateHp
                        eid, delta = parse_update_hp(ubuf)
                        if eid in hp:
                            hp[eid] += delta
                    elif unum == 6:                              # updatePlayers
                        for pn, _pw, pv in fields(ubuf):
                            if pn != 1:
                                continue
                            for tn, _tw, tv in fields(pv):
                                if tn in (1, 2):
                                    d = scalars(tv)
                                    players[tn - 1] = {
                                        "ti": d.get(1, 0),
                                        "coll": d.get(4, 0),
                                        "ammo": d.get(7, 0),
                                    }
            oc, pc = self.core_c[self.our], self.core_c[self.opp]
            cnt = {"sent": 0, "gun": 0, "lau": 0, "bot": 0}
            near_bot = near_sent = near_lau = opp_near_bot = 0
            for e in ents.values():
                if e.kind == "core":
                    continue
                if e.team == self.our:
                    k = {"sentinel": "sent", "gunner": "gun", "launcher": "lau",
                         "builder_bot": "bot"}.get(e.kind)
                    if k:
                        cnt[k] += 1
                    d = dsq(e.pos, pc)
                    if e.kind == "builder_bot" and d <= 8:
                        near_bot += 1
                    if e.kind == "sentinel" and d <= 40:
                        near_sent += 1
                    if e.kind == "launcher" and d <= 32:
                        near_lau += 1
                else:
                    if e.kind == "builder_bot" and dsq(e.pos, oc) <= 8:
                        opp_near_bot += 1
            self.rows.append({
                "r": rnd,
                "our_core_hp": hp.get(self.core_id[self.our], 0),
                "opp_core_hp": hp.get(self.core_id[self.opp], 0),
                "our_ti": players[self.our].get("ti", 0),
                "our_ammo": players[self.our].get("ammo", 0),
                "our_coll": players[self.our].get("coll", 0),
                "opp_ti": players[self.opp].get("ti", 0),
                "opp_ammo": players[self.opp].get("ammo", 0),
                "opp_coll": players[self.opp].get("coll", 0),
                "sent": cnt["sent"], "gun": cnt["gun"], "lau": cnt["lau"],
                "bot": cnt["bot"],
                "near_bot": near_bot, "near_sent": near_sent,
                "near_lau": near_lau, "opp_near_bot": opp_near_bot,
            })
        self.final_ents = ents
        self.ever = ever


if __name__ == "__main__":
    t = Tape(Path(sys.argv[1]), int(sys.argv[2]))
    print("winner", t.winner, t.win_condition, "rounds", t.rounds)
    cols = list(t.rows[0].keys())
    print("\t".join(cols))
    step = int(sys.argv[3]) if len(sys.argv) > 3 else 25
    for row in t.rows:
        if row["r"] % step == 0 or row["r"] == t.rounds - 1:
            print("\t".join(str(row[c]) for c in cols))
