"""s54 kladde-v173 study: shared decoder.

Built on tools/replay_census.py primitives (fields/read_pos/parse_entity/scalars)
per corpus-howto "don't hand-roll a decoder that exists" — this is a thin event
walker over those primitives, not a second parser.

Guards carried from tools/replay_schema.md + corpus-howto TRAPS:
  * a BUILD is the FIRST placeEntity carrying a given entity id (rotate re-emits)
  * cores are never placed; seed them from map.cores at 500 HP
  * updateHp.delta is a 64-bit two's-complement varint
  * FireTurret can be emitted AFTER the victim's removeEntity -> never-popped
    registry `ever` for shooter/victim resolution
  * Barrier is an empty submessage: test field PRESENCE, not content
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import (  # noqa: E402
    fields, read_pos, parse_entity, scalars, WIRE_LEN, WIRE_VARINT,
)

U64 = 1 << 64


def signed(v: int) -> int:
    return v - U64 if v >= (1 << 63) else v


class Game:
    __slots__ = ("path", "width", "height", "cores", "tiles", "rounds",
                 "winner", "wincond", "ev", "ever", "born", "died",
                 "players_end", "players_by_round")

    def __init__(self, path: Path, want_players=False):
        self.path = Path(path)
        data = self.path.read_bytes()
        map_buf, turn_bufs = None, []
        self.winner, self.wincond = None, ""
        for num, wire, value in fields(data):
            if num == 1 and wire == WIRE_LEN:
                map_buf = value
            elif num == 3 and wire == WIRE_LEN:
                turn_bufs.append(value)
            elif num == 4 and wire == WIRE_VARINT:
                self.winner = value
            elif num == 6 and wire == WIRE_LEN:
                self.wincond = value.decode("utf-8", "replace")
        if map_buf is None:
            raise ValueError(f"{path}: no map")
        self._parse_map(map_buf)
        self.rounds = len(turn_bufs)
        self._walk(turn_bufs, want_players)

    def _parse_map(self, buf):
        self.width = self.height = 0
        self.tiles = []
        self.cores = []
        for num, wire, value in fields(buf):
            if num == 1:
                self.width = value
            elif num == 2:
                self.height = value
            elif num == 3:
                row = []
                for rnum, rwire, rvalue in fields(value):
                    if rnum == 1:
                        if rwire == WIRE_LEN:
                            from replay_census import packed_varints
                            row.extend(packed_varints(rvalue))
                        else:
                            row.append(rvalue)
                self.tiles.append(row)
            elif num == 4:
                c = {"id": 0, "team": 0, "pos": (0, 0)}
                for cnum, _cw, cv in fields(value):
                    if cnum == 1:
                        c["id"] = cv
                    elif cnum == 2:
                        c["team"] = cv
                    elif cnum == 3:
                        c["pos"] = read_pos(cv)
                self.cores.append(c)

    def core_pos(self, team):
        for c in self.cores:
            if c["team"] == team:
                return c["pos"]
        return None

    def core_id(self, team):
        for c in self.cores:
            if c["team"] == team:
                return c["id"]
        return None

    def footprint(self, team):
        p = self.core_pos(team)
        if p is None:
            return set()
        x, y = p
        return {(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)}

    def env(self, x, y):
        if 0 <= y < len(self.tiles) and 0 <= x < len(self.tiles[y]):
            return self.tiles[y][x]
        return 1

    def _walk(self, turn_bufs, want_players):
        # ev: list of (rnd, kind, payload)
        ev = []
        ever = {}          # id -> dict(team, kind, born, dir)
        born = {}          # id -> round of FIRST placeEntity
        died = {}          # id -> round of removeEntity
        pos = {}           # id -> current pos
        for c in self.cores:
            ever[c["id"]] = {"team": c["team"], "kind": "core",
                             "born": -1, "dir": None}
            born[c["id"]] = -1
            pos[c["id"]] = c["pos"]
        players_by_round = {}
        players_end = [{}, {}]

        for rnd, tbuf in enumerate(turn_bufs):
            for _n, _w, ubuf_outer in fields(tbuf):
                for unum, _uw, ubuf in fields(ubuf_outer):
                    if unum == 1:                                   # placeEntity
                        for enum_, _ew, ebuf in fields(ubuf):
                            if enum_ != 1:
                                continue
                            e = parse_entity(ebuf, rnd)
                            if e is None:
                                continue
                            first = e.id not in ever
                            if first:
                                ever[e.id] = {"team": e.team, "kind": e.kind,
                                              "born": rnd,
                                              "dir": getattr(e, "direction", None)}
                                born[e.id] = rnd
                                ev.append((rnd, "BUILD", (e.id, e.team, e.kind,
                                                          e.pos)))
                            else:
                                ev.append((rnd, "REEMIT", (e.id, e.team, e.kind,
                                                           e.pos)))
                            pos[e.id] = e.pos
                    elif unum == 2:                                 # moveBuilderBot
                        d = {}
                        for mnum, _mw, mv in fields(ubuf):
                            if mnum == 1:
                                d["id"] = mv
                            elif mnum == 2:
                                d["to"] = read_pos(mv)
                        if "id" in d and "to" in d:
                            frm = pos.get(d["id"])
                            ev.append((rnd, "MOVE", (d["id"], frm, d["to"])))
                            pos[d["id"]] = d["to"]
                    elif unum == 3:                                 # removeEntity
                        rid = None
                        for rnum, _rw, rv in fields(ubuf):
                            if rnum == 1:
                                rid = rv
                        if rid is not None:
                            if rid not in died:
                                died[rid] = rnd
                            ev.append((rnd, "DEATH", (rid,)))
                    elif unum == 5:                                 # updateHp
                        sc = {}
                        for hnum, _hw, hv in fields(ubuf):
                            sc[hnum] = hv
                        if 1 in sc:
                            ev.append((rnd, "HP", (sc[1], signed(sc.get(2, 0)))))
                    elif unum == 6 and want_players:                # updatePlayers
                        for pnum, _pw, pv in fields(ubuf):
                            if pnum != 1:
                                continue
                            for tnum, _tw, tv in fields(pv):
                                if tnum not in (1, 2):
                                    continue
                                d = {}
                                for fnum, fw, fv in fields(tv):
                                    if fw == WIRE_VARINT:
                                        d[fnum] = fv
                                players_end[tnum - 1] = d
                                players_by_round.setdefault(rnd, {})[tnum - 1] = d
                    elif unum == 12:                                # fireTurret
                        frm = to = None
                        for fnum, _fw, fv in fields(ubuf):
                            if fnum == 1:
                                frm = read_pos(fv)
                            elif fnum == 2:
                                to = read_pos(fv)
                        ev.append((rnd, "FIRE", (frm, to)))
                    elif unum == 13:                                # builderAttack
                        d = {}
                        for anum, _aw, av in fields(ubuf):
                            if anum == 1:
                                d["id"] = av
                            elif anum == 2:
                                d["t"] = read_pos(av)
                        if "id" in d:
                            ev.append((rnd, "BATK", (d["id"], d.get("t"))))
                    elif unum == 14:                                # coreConvertAmmo
                        sc = {}
                        for cnum, _cw, cv in fields(ubuf):
                            sc[cnum] = cv
                        ev.append((rnd, "AMMO", (sc.get(1, 0), sc.get(2, 0))))
                    elif unum == 15:                                # builderHeal
                        d = {}
                        for hnum, _hw, hv in fields(ubuf):
                            if hnum == 1:
                                d["id"] = hv
                            elif hnum == 2:
                                d["t"] = read_pos(hv)
                        ev.append((rnd, "HEAL", (d.get("id"), d.get("t"))))
                    elif unum == 16:                                # builderBuild
                        d = {}
                        for bnum, _bw, bv in fields(ubuf):
                            if bnum == 1:
                                d["id"] = bv
                            elif bnum == 2:
                                d["t"] = read_pos(bv)
                        ev.append((rnd, "BBUILD", (d.get("id"), d.get("t"))))
                    elif unum == 9:                                 # botOutput
                        sc = {}
                        for bnum, bw, bv in fields(ubuf):
                            sc[bnum] = bv
                        ev.append((rnd, "OUT", (sc.get(1), sc.get(3, 0),
                                                sc.get(4, 0))))
        self.ev = ev
        self.ever = ever
        self.born = born
        self.died = died
        self.players_end = players_end
        self.players_by_round = players_by_round

    # ---- convenience -------------------------------------------------------
    def positions_at(self, upto_round):
        """id -> position after replaying moves through `upto_round` (inclusive)."""
        p = {}
        for c in self.cores:
            p[c["id"]] = c["pos"]
        for rnd, kind, pl in self.ev:
            if rnd > upto_round:
                break
            if kind in ("BUILD", "REEMIT"):
                p[pl[0]] = pl[3]
            elif kind == "MOVE":
                p[pl[0]] = pl[2]
        return p


def d2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
