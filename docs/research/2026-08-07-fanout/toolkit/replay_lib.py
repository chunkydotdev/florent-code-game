#!/usr/bin/env python3
"""replay_lib — full-timeline decoder for Florent Code League `.replay26` files.

Stdlib only.  Complements (does not replace) `tools/replay_census.py`, which is
an end-of-game snapshot tool.  This one keeps the *whole* timeline: every build,
move, death, HP delta, turret shot, builder attack/heal/build, ammo conversion,
resource move, and bot stdout line, indexed by round, plus per-team per-round
curves.

Quick start
-----------
    import sys; sys.path.insert(0, "<SCRATCH>/toolkit")
    from replay_lib import load_replay, delivered_curve, entity_census

    r = load_replay("replay.replay26")
    print(r.width, r.height, r.n_rounds, r.winner_name, r.win_condition)
    print(delivered_curve(r, "A")[-1])          # cumulative Ti delivered
    print(entity_census(r)["A"]["built"])       # {'harvester': 6, ...}
    for d in r.damage_log(team="B"):            # damage *dealt* by B
        ...

Wire-format facts this leans on (see tools/replay_schema.md, plus the extra
traps documented in this file's README):
  * turns[i] IS round i, 0-based.
  * Cores are never emitted as placeEntity; seed them from map.cores at 500 HP.
  * UpdateHp.delta is a signed int32 -> negatives arrive as ~1.8e19 varints.
  * proto3 omits defaults: absent team == TEAM_A(0), absent x/y == 0,
    absent titaniumCollected/ammo == 0.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field as _dcfield
from pathlib import Path

# --------------------------------------------------------------------------
# wire format
# --------------------------------------------------------------------------

WIRE_VARINT, WIRE_64, WIRE_LEN, WIRE_32 = 0, 1, 2, 5
_TWO63 = 1 << 63
_TWO64 = 1 << 64


def _varint(buf: bytes, i: int):
    result = shift = 0
    while True:
        byte = buf[i]
        i += 1
        result |= (byte & 0x7F) << shift
        if not byte & 0x80:
            return result, i
        shift += 7


def fields(buf: bytes):
    """Yield (field_number, wire_type, value) for every field in a message."""
    i, n = 0, len(buf)
    while i < n:
        tag, i = _varint(buf, i)
        num, wire = tag >> 3, tag & 7
        if wire == WIRE_VARINT:
            value, i = _varint(buf, i)
            yield num, wire, value
        elif wire == WIRE_LEN:
            length, i = _varint(buf, i)
            yield num, wire, buf[i:i + length]
            i += length
        elif wire == WIRE_32:
            yield num, wire, buf[i:i + 4]
            i += 4
        elif wire == WIRE_64:
            yield num, wire, buf[i:i + 8]
            i += 8
        else:
            raise ValueError(f"unsupported wire type {wire} for field {num}")


def scalars(buf: bytes) -> dict:
    """Flatten a message to {field_number: value}, last occurrence winning."""
    return {num: value for num, _, value in fields(buf)}


def signed(v: int) -> int:
    """protobuf int32/int64: negatives are 64-bit two's complement varints."""
    return v - _TWO64 if v >= _TWO63 else v


def read_pos(buf: bytes):
    d = scalars(buf)
    return (d.get(1, 0), d.get(2, 0))


def packed_varints(buf: bytes):
    out, i, n = [], 0, len(buf)
    while i < n:
        value, i = _varint(buf, i)
        out.append(value)
    return out


# --------------------------------------------------------------------------
# schema constants
# --------------------------------------------------------------------------

KIND_FIELDS = {10: "builder_bot", 11: "conveyor", 12: "splitter",
               15: "harvester", 18: "barrier", 20: "core",
               21: "gunner", 22: "sentinel", 24: "launcher"}
KINDS = ["core", "builder_bot", "harvester", "conveyor", "splitter",
         "barrier", "gunner", "sentinel", "launcher"]
TURRET_KINDS = ("gunner", "sentinel", "launcher")
BUILDING_KINDS = ("core", "harvester", "conveyor", "splitter", "barrier",
                  "gunner", "sentinel", "launcher")

DIRECTION_NAME = {0: "CENTRE", 1: "NORTH", 2: "NORTHEAST", 3: "EAST",
                  4: "SOUTHEAST", 5: "SOUTH", 6: "SOUTHWEST", 7: "WEST",
                  8: "NORTHWEST"}
DIRECTION_DELTA = {0: (0, 0), 1: (0, -1), 2: (1, -1), 3: (1, 0), 4: (1, 1),
                   5: (0, 1), 6: (-1, 1), 7: (-1, 0), 8: (-1, -1)}
CARDINALS = ((0, -1), (1, 0), (0, 1), (-1, 0))

TEAM_A, TEAM_B = 0, 1
TEAM_NAME = {0: "A", 1: "B"}

ENV_EMPTY, ENV_WALL, ENV_ORE_TITANIUM, ENV_ORE_AXIONITE = 0, 1, 2, 3
ENV_NAME = {0: "EMPTY", 1: "WALL", 2: "ORE_TITANIUM", 3: "ORE_AXIONITE"}

STACK_SIZE = 10                      # one delivered resource stack == 10 Ti
AMMO_COST = {"gunner": 4, "sentinel": 10, "launcher": 0}


def norm_team(team) -> int:
    """Accept 0/1, 'A'/'B', 'a'/'b' -> 0/1."""
    if isinstance(team, int):
        if team in (0, 1):
            return team
        raise ValueError(f"bad team {team!r}")
    t = str(team).strip().upper()
    if t in ("A", "0", "TEAM_A"):
        return 0
    if t in ("B", "1", "TEAM_B"):
        return 1
    raise ValueError(f"bad team {team!r}")


# --------------------------------------------------------------------------
# records
# --------------------------------------------------------------------------

@dataclass
class Entity:
    """One entity's whole life.

    alive_at(r) is True for spawn_round <= r < death_round.  death_round is the
    round whose `removeEntity` killed it (None if it survived to the last turn).
    """
    id: int
    kind: str
    team: int
    spawn_round: int
    spawn_pos: tuple
    max_hp: int = 0
    hp: int = 0                       # HP after the last update we saw
    direction: int | None = None      # conveyor/splitter/gunner/sentinel facing
    death_round: int | None = None
    pos: tuple = (0, 0)               # final (or death-time) position
    path: list = _dcfield(default_factory=list)      # [(round, (x, y))]
    hp_events: list = _dcfield(default_factory=list)  # [(round, delta, hp_after)]

    @property
    def team_name(self) -> str:
        return TEAM_NAME[self.team]

    @property
    def direction_name(self):
        return None if self.direction is None else DIRECTION_NAME.get(self.direction)

    @property
    def is_building(self) -> bool:
        return self.kind in BUILDING_KINDS

    def alive_at(self, rnd: int) -> bool:
        return self.spawn_round <= rnd and (self.death_round is None or rnd < self.death_round)

    def pos_at(self, rnd: int):
        """Position at end of round rnd (None if not alive then)."""
        if not self.alive_at(rnd):
            return None
        out = self.spawn_pos
        for r, p in self.path:
            if r > rnd:
                break
            out = p
        return out

    def lifespan(self, n_rounds: int) -> int:
        return (self.death_round if self.death_round is not None else n_rounds) - self.spawn_round

    def __repr__(self):
        d = f" dir={self.direction_name}" if self.direction is not None else ""
        died = "" if self.death_round is None else f" died r{self.death_round}"
        return (f"<{self.kind} #{self.id} {TEAM_NAME[self.team]} @{self.pos}"
                f" born r{self.spawn_round}{died}{d}>")


@dataclass
class Build:
    round: int
    id: int
    kind: str
    team: int
    pos: tuple
    direction: int | None
    hp: int
    max_hp: int
    builder_id: int | None = None     # builder bot that placed it (None = core spawn)


@dataclass
class EntityUpdate:
    """A `placeEntity` re-emitted for an id that is ALREADY ALIVE.

    Observed for gunner `rotate()`: same id, same position, new direction.  This
    is NOT a new build — counting it as one inflates turret counts.  Kept as its
    own event stream because a rotation log is itself a strategy signal.
    """
    round: int
    id: int
    kind: str
    team: int
    pos: tuple
    direction: int | None
    prev_direction: int | None
    hp: int


@dataclass
class Move:
    round: int
    id: int
    team: int
    frm: tuple
    to: tuple


@dataclass
class Death:
    round: int
    id: int
    kind: str
    team: int
    pos: tuple
    age: int                          # rounds it lived


@dataclass
class HpEvent:
    """One UpdateHp.  delta<0 is damage, delta>0 healing/repair.

    source_* is best-effort attribution from same-round Fire / BuilderAttack /
    BuilderHeal events matched by target position (see Replay._attribute).
    """
    round: int
    target_id: int
    target_kind: str
    target_team: int
    target_pos: tuple
    delta: int
    hp_after: int
    source_kind: str | None = None    # 'gunner'|'sentinel'|'launcher'|'builder_bot'|None
    source_id: int | None = None
    source_team: int | None = None
    source_pos: tuple | None = None

    @property
    def is_damage(self) -> bool:
        return self.delta < 0

    @property
    def amount(self) -> int:
        return abs(self.delta)


@dataclass
class Fire:
    round: int
    frm: tuple
    to: tuple
    shooter_id: int | None
    shooter_kind: str | None
    shooter_team: int | None
    ammo_cost: int


@dataclass
class BuilderAction:
    """BuilderAttack / BuilderHeal / BuilderBuild (kind says which)."""
    round: int
    kind: str                         # 'attack' | 'heal' | 'build'
    id: int
    team: int | None
    frm: tuple | None                 # builder's own position that round
    target: tuple


@dataclass
class ConvertAmmo:
    round: int
    team: int
    amount: int


@dataclass
class ResourceMove:
    round: int
    frm: tuple
    to: tuple
    resource_id: int | None
    to_core_team: int | None          # team whose core footprint `to` landed on


@dataclass
class BotOutput:
    round: int
    id: int
    team: int | None
    stdout: str
    exec_time_us: int
    tled: bool


@dataclass
class Indicator:
    round: int
    kind: str                         # 'line' | 'dot'
    id: int
    team: int | None
    pos_a: tuple
    pos_b: tuple | None
    rgb: tuple


@dataclass
class RoundEvents:
    """Everything that happened in one round, already typed."""
    round: int
    builds: list = _dcfield(default_factory=list)
    entity_updates: list = _dcfield(default_factory=list)   # gunner rotations
    moves: list = _dcfield(default_factory=list)
    deaths: list = _dcfield(default_factory=list)
    hp: list = _dcfield(default_factory=list)
    fires: list = _dcfield(default_factory=list)
    builder_actions: list = _dcfield(default_factory=list)
    convert_ammo: list = _dcfield(default_factory=list)
    resource_moves: list = _dcfield(default_factory=list)
    bot_output: list = _dcfield(default_factory=list)
    indicators: list = _dcfield(default_factory=list)
    action_cooldowns: list = _dcfield(default_factory=list)   # (id, value), opt-in
    move_cooldowns: list = _dcfield(default_factory=list)     # (id, value), opt-in

    @property
    def damage(self):
        return [h for h in self.hp if h.delta < 0]

    @property
    def heals(self):
        return [h for h in self.hp if h.delta > 0]


# --------------------------------------------------------------------------
# the replay
# --------------------------------------------------------------------------

class Replay:
    """A fully decoded `.replay26`.

    Attributes
    ----------
    path, width, height, tiles[y][x], walls, ore, cores, n_rounds
    winner (0/1/None), winner_name ('A'/'B'/None), win_condition (str)
    entities   : {id: Entity}          — every entity that ever existed
    rounds     : [RoundEvents]         — index IS the round number
    players    : [[playerA_dict, playerB_dict]] per round (forward-filled)
    unknown_top / unknown_update_kinds / unknown_entity_kinds — schema drift alarms
    """

    def __init__(self, path, *, keep_bot_output=True, keep_indicators=False,
                 keep_cooldowns=False, attribute_damage=True):
        self.path = Path(path)
        data = self.path.read_bytes()
        self.keep_bot_output = keep_bot_output
        self.keep_indicators = keep_indicators
        self.keep_cooldowns = keep_cooldowns

        map_buf = None
        turn_bufs = []
        self.winner = None
        self.win_condition = ""
        self.unknown_top = {}
        for num, wire, value in fields(data):
            if num == 1 and wire == WIRE_LEN:
                map_buf = value
            elif num == 3 and wire == WIRE_LEN:
                turn_bufs.append(value)
            elif num == 4 and wire == WIRE_VARINT:
                self.winner = value
            elif num == 6 and wire == WIRE_LEN:
                self.win_condition = value.decode("utf-8", "replace")
            else:
                self.unknown_top[num] = wire
        if map_buf is None:
            raise ValueError(f"{path}: no battlecode.Map (field 1) — not a replay?")

        self._parse_map(map_buf)
        self.n_rounds = len(turn_bufs)
        self._replay(turn_bufs)
        if attribute_damage:
            self._attribute()
        self._build_curves()

    # ---- map -------------------------------------------------------------

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
                        row.extend(packed_varints(rvalue) if rwire == WIRE_LEN else [rvalue])
                self.tiles.append(row)
            elif num == 4:
                core = {"id": 0, "team": 0, "pos": (0, 0)}
                for cnum, _cw, cvalue in fields(value):
                    if cnum == 1:
                        core["id"] = cvalue
                    elif cnum == 2:
                        core["team"] = cvalue
                    elif cnum == 3:
                        core["pos"] = read_pos(cvalue)
                self.cores.append(core)
        self.walls = {(x, y) for y, row in enumerate(self.tiles)
                      for x, t in enumerate(row) if t == ENV_WALL}
        self.ore = {(x, y) for y, row in enumerate(self.tiles)
                    for x, t in enumerate(row) if t == ENV_ORE_TITANIUM}

    def env(self, x, y) -> int:
        if 0 <= y < len(self.tiles) and 0 <= x < len(self.tiles[y]):
            return self.tiles[y][x]
        return ENV_WALL                      # off-map behaves like wall

    def env_name(self, x, y) -> str:
        return ENV_NAME.get(self.env(x, y), "?")

    def core_pos(self, team):
        """NW corner of the team's 2x2 core footprint."""
        team = norm_team(team)
        for c in self.cores:
            if c["team"] == team:
                return c["pos"]
        return None

    def core_id(self, team):
        team = norm_team(team)
        for c in self.cores:
            if c["team"] == team:
                return c["id"]
        return None

    def core_footprint(self, team) -> set:
        team = norm_team(team)
        out = set()
        for c in self.cores:
            if c["team"] == team:
                x, y = c["pos"]
                out |= {(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)}
        return out

    @property
    def winner_name(self):
        return TEAM_NAME.get(self.winner)

    # ---- the single pass -------------------------------------------------

    def _parse_entity(self, buf, rnd):
        eid = team = hp = max_hp = 0
        pos = None
        kind = None
        direction = None
        for num, wire, value in fields(buf):
            if num == 1:
                eid = value
            elif num == 2:
                team = value
            elif num == 3:
                pos = read_pos(value)
            elif num == 4:
                hp = value
            elif num == 5:
                max_hp = value
            elif num in KIND_FIELDS:
                kind = KIND_FIELDS[num]
                if wire == WIRE_LEN and value:
                    sub = scalars(value)
                    if kind in ("conveyor", "splitter", "gunner", "sentinel"):
                        direction = sub.get(1, 0)
            elif wire == WIRE_LEN:
                kind = f"unknown{num}"
                self.unknown_entity_kinds.add(kind)
        if kind is None or pos is None:
            return None
        return Entity(id=eid, kind=kind, team=team, spawn_round=rnd, spawn_pos=pos,
                      max_hp=max_hp, hp=hp, direction=direction, pos=pos)

    def _replay(self, turn_bufs):
        self.unknown_entity_kinds = set()
        self.unknown_update_kinds = {}
        self.unknown_turn_fields = {}
        self.recycled_ids = []          # (id, round) if the engine ever reuses one
        entities: dict[int, Entity] = {}
        live: dict[int, Entity] = {}

        # Cores exist from the start; they are never emitted as placeEntity.
        for c in self.cores:
            e = Entity(id=c["id"], kind="core", team=c["team"], spawn_round=0,
                       spawn_pos=c["pos"], max_hp=500, hp=500, pos=c["pos"])
            entities[e.id] = e
            live[e.id] = e

        self.rounds: list[RoundEvents] = []
        players = [{"titanium": 0, "resources_collected": 0,
                    "titanium_collected": 0, "ammo": 0} for _ in range(2)]
        self.players: list[list[dict]] = []
        # pos -> [(spawn_round, death_round_or_None, id)] for buildings, so a
        # FireTurret (which carries no shooter id) can be resolved to a turret.
        self._bpos: dict[tuple, list] = {}

        for rnd, turn_buf in enumerate(turn_bufs):
            ev = RoundEvents(round=rnd)
            for tnum, tw, update_buf in fields(turn_buf):
                if tnum != 1 or tw != WIRE_LEN:      # Turn.updates is field 1
                    self.unknown_turn_fields[tnum] = \
                        self.unknown_turn_fields.get(tnum, 0) + 1
                    continue
                for unum, _uw, ub in fields(update_buf):
                    if unum == 1:                                # placeEntity
                        for en, _ew, eb in fields(ub):
                            if en != 1:
                                continue
                            ent = self._parse_entity(eb, rnd)
                            if ent is None:
                                continue
                            old = live.get(ent.id)
                            if old is not None:
                                # Re-emission for a LIVE id == in-place update
                                # (gunner rotate()), not a new build.
                                ev.entity_updates.append(EntityUpdate(
                                    rnd, ent.id, old.kind, old.team, ent.pos,
                                    ent.direction, old.direction, ent.hp))
                                old.direction = ent.direction
                                old.hp = ent.hp
                                if ent.pos != old.pos:
                                    old.pos = ent.pos
                                    old.path.append((rnd, ent.pos))
                                continue
                            if ent.id in entities:
                                self.recycled_ids.append((ent.id, rnd))
                            entities[ent.id] = ent
                            live[ent.id] = ent
                            if ent.kind != "builder_bot":
                                self._bpos.setdefault(ent.pos, []).append(
                                    [rnd, None, ent.id])
                            ev.builds.append(Build(rnd, ent.id, ent.kind, ent.team,
                                                   ent.pos, ent.direction,
                                                   ent.hp, ent.max_hp))
                    elif unum == 2:                              # moveBuilderBot
                        eid = to = None
                        for mn, _mw, mv in fields(ub):
                            if mn == 1:
                                eid = mv
                            elif mn == 2:
                                to = read_pos(mv)
                        ent = live.get(eid)
                        if ent is not None and to is not None:
                            ev.moves.append(Move(rnd, eid, ent.team, ent.pos, to))
                            ent.pos = to
                            ent.path.append((rnd, to))
                    elif unum == 3:                              # removeEntity
                        for rn, _rw, rv in fields(ub):
                            if rn != 1:
                                continue
                            ent = live.pop(rv, None)
                            if ent is None:
                                continue
                            ent.death_round = rnd
                            ev.deaths.append(Death(rnd, ent.id, ent.kind, ent.team,
                                                   ent.pos, rnd - ent.spawn_round))
                            for rec in self._bpos.get(ent.pos, ()):
                                if rec[2] == ent.id and rec[1] is None:
                                    rec[1] = rnd
                    elif unum == 4:                              # distributeResources
                        for _mn, _mw, mb in fields(ub):
                            src = dst = None
                            rid = None
                            for pn, _pw, pv in fields(mb):
                                if pn == 1:
                                    src = read_pos(pv)
                                elif pn == 2:
                                    dst = read_pos(pv)
                                elif pn == 3:
                                    rid = pv
                            to_core = None
                            if dst is not None:
                                for t in (0, 1):
                                    if dst in self._core_tiles[t]:
                                        to_core = t
                            ev.resource_moves.append(ResourceMove(rnd, src, dst, rid, to_core))
                    elif unum == 5:                              # updateHp
                        d = scalars(ub)
                        tid = d.get(1, 0)
                        delta = signed(d.get(2, 0))
                        ent = entities.get(tid)
                        if ent is None:
                            continue
                        ent.hp += delta
                        ent.hp_events.append((rnd, delta, ent.hp))
                        ev.hp.append(HpEvent(rnd, tid, ent.kind, ent.team,
                                             ent.pos, delta, ent.hp))
                    elif unum == 6:                              # updatePlayers
                        for pn, _pw, pv in fields(ub):
                            if pn != 1:
                                continue
                            for tn, _tw, tv in fields(pv):
                                if tn in (1, 2):
                                    d = scalars(tv)
                                    players[tn - 1] = {
                                        "titanium": d.get(1, 0),
                                        "resources_collected": d.get(3, 0),
                                        "titanium_collected": d.get(4, 0),
                                        "ammo": d.get(7, 0),
                                    }
                    elif unum == 7:                              # setActionCooldown
                        if self.keep_cooldowns:
                            d = scalars(ub)
                            ev.action_cooldowns.append((d.get(1, 0), d.get(2, 0)))
                    elif unum == 8:                              # setMoveCooldown
                        if self.keep_cooldowns:
                            d = scalars(ub)
                            ev.move_cooldowns.append((d.get(1, 0), d.get(2, 0)))
                    elif unum == 9:                              # botOutput
                        if not self.keep_bot_output:
                            continue
                        d = scalars(ub)
                        bid = d.get(1, 0)
                        raw = d.get(2, b"")
                        ent = entities.get(bid)
                        ev.bot_output.append(BotOutput(
                            rnd, bid, ent.team if ent else None,
                            raw.decode("utf-8", "replace") if isinstance(raw, bytes) else "",
                            d.get(3, 0), bool(d.get(4, 0))))
                    elif unum in (10, 11):                       # indicatorLine/Dot
                        if not self.keep_indicators:
                            continue
                        d = scalars(ub)
                        iid = d.get(1, 0)
                        ent = entities.get(iid)
                        if unum == 10:
                            ev.indicators.append(Indicator(
                                rnd, "line", iid, ent.team if ent else None,
                                read_pos(d.get(2, b"")), read_pos(d.get(3, b"")),
                                (d.get(4, 0), d.get(5, 0), d.get(6, 0))))
                        else:
                            ev.indicators.append(Indicator(
                                rnd, "dot", iid, ent.team if ent else None,
                                read_pos(d.get(2, b"")), None,
                                (d.get(3, 0), d.get(4, 0), d.get(5, 0))))
                    elif unum == 12:                             # fireTurret
                        d = scalars(ub)
                        frm = read_pos(d.get(1, b""))
                        to = read_pos(d.get(2, b""))
                        ev.fires.append(Fire(rnd, frm, to, None, None, None, 0))
                    elif unum in (13, 15, 16):                   # builder attack/heal/build
                        d = scalars(ub)
                        bid = d.get(1, 0)
                        ent = entities.get(bid)
                        ev.builder_actions.append(BuilderAction(
                            rnd, {13: "attack", 15: "heal", 16: "build"}[unum], bid,
                            ent.team if ent else None, ent.pos if ent else None,
                            read_pos(d.get(2, b""))))
                    elif unum == 14:                             # coreConvertAmmo
                        d = scalars(ub)
                        # NOTE: team is omitted when TEAM_A (proto3 default).
                        ev.convert_ammo.append(ConvertAmmo(rnd, d.get(1, 0), d.get(2, 0)))
                    else:
                        self.unknown_update_kinds[unum] = \
                            self.unknown_update_kinds.get(unum, 0) + 1

            # resolve turret shooters now that this round's builds are in
            for f in ev.fires:
                sid = self._building_at(f.frm, rnd)
                if sid is not None:
                    se = entities[sid]
                    f.shooter_id, f.shooter_kind, f.shooter_team = sid, se.kind, se.team
                    f.ammo_cost = AMMO_COST.get(se.kind, 0)
            self.rounds.append(ev)
            self.players.append([dict(players[0]), dict(players[1])])

        self.entities = entities
        self.live_at_end = dict(live)

    @property
    def _core_tiles(self):
        if not hasattr(self, "_core_tiles_cache"):
            self._core_tiles_cache = {t: self.core_footprint(t) for t in (0, 1)}
        return self._core_tiles_cache

    def _building_at(self, pos, rnd):
        """Id of the (non-builder-bot) entity occupying pos during round rnd."""
        for spawn, death, eid in self._bpos.get(pos, ()):
            if spawn <= rnd and (death is None or rnd <= death):
                return eid
        # cores occupy 2x2 but are keyed at their NW corner only
        for t in (0, 1):
            if pos in self._core_tiles[t]:
                return self.core_id(t)
        return None

    # ---- damage attribution ---------------------------------------------

    def _attribute(self):
        """Best-effort: match each HpEvent to a same-round Fire / builder action
        whose target tile equals the target's position.  Greedy, one source per
        event; unmatched events keep source_kind=None."""
        for ev in self.rounds:
            if not ev.hp:
                continue
            fires = {}
            for f in ev.fires:
                fires.setdefault(f.to, []).append(f)
            atk, heal = {}, {}
            for a in ev.builder_actions:
                if a.kind == "attack":
                    atk.setdefault(a.target, []).append(a)
                elif a.kind == "heal":
                    heal.setdefault(a.target, []).append(a)
            for h in ev.hp:
                p = h.target_pos
                if h.delta < 0:
                    cand = fires.get(p) or []
                    if cand:
                        f = cand.pop(0)
                        h.source_kind = f.shooter_kind or "turret"
                        h.source_id, h.source_team, h.source_pos = \
                            f.shooter_id, f.shooter_team, f.frm
                        continue
                    cand = atk.get(p) or []
                    if cand:
                        a = cand.pop(0)
                        h.source_kind, h.source_id = "builder_bot", a.id
                        h.source_team, h.source_pos = a.team, a.frm
                    elif h.target_kind == "core":
                        # cores are 2x2: an attack/shot may target any footprint
                        # tile, not just the NW corner we store as .pos
                        foot = self._core_tiles[h.target_team]
                        for tile in foot:
                            if fires.get(tile):
                                f = fires[tile].pop(0)
                                h.source_kind = f.shooter_kind or "turret"
                                h.source_id, h.source_team, h.source_pos = \
                                    f.shooter_id, f.shooter_team, f.frm
                                break
                            if atk.get(tile):
                                a = atk[tile].pop(0)
                                h.source_kind, h.source_id = "builder_bot", a.id
                                h.source_team, h.source_pos = a.team, a.frm
                                break
                else:
                    cand = heal.get(p) or []
                    if not cand and h.target_kind == "core":
                        for tile in self._core_tiles[h.target_team]:
                            if heal.get(tile):
                                cand = heal[tile]
                                break
                    if cand:
                        a = cand.pop(0)
                        h.source_kind, h.source_id = "builder_bot", a.id
                        h.source_team, h.source_pos = a.team, a.frm

    # ---- curves ----------------------------------------------------------

    def _build_curves(self):
        n = self.n_rounds
        self._delivered = {t: [0] * n for t in (0, 1)}
        self._deliveries = {t: [0] * n for t in (0, 1)}
        self._ammo_spent = {t: [0] * n for t in (0, 1)}
        self._counts = {t: {k: [0] * n for k in KINDS} for t in (0, 1)}
        self._dmg_dealt = {t: [0] * n for t in (0, 1)}
        self._dmg_taken = {t: [0] * n for t in (0, 1)}

        alive = {t: dict.fromkeys(KINDS, 0) for t in (0, 1)}
        for c in self.cores:
            alive[c["team"]]["core"] += 1
        cum_d = [0, 0]
        cum_a = [0, 0]
        for r, ev in enumerate(self.rounds):
            for b in ev.builds:
                if b.kind in alive[b.team]:
                    alive[b.team][b.kind] += 1
            for d in ev.deaths:
                if d.kind in alive[d.team]:
                    alive[d.team][d.kind] -= 1
            for m in ev.resource_moves:
                if m.to_core_team is not None:
                    cum_d[m.to_core_team] += 1
            for f in ev.fires:
                if f.shooter_team is not None:
                    cum_a[f.shooter_team] += f.ammo_cost
            for h in ev.hp:
                if h.delta < 0:
                    self._dmg_taken[h.target_team][r] += -h.delta
                    if h.source_team is not None:
                        self._dmg_dealt[h.source_team][r] += -h.delta
            for t in (0, 1):
                self._deliveries[t][r] = cum_d[t]
                self._delivered[t][r] = cum_d[t] * STACK_SIZE
                self._ammo_spent[t][r] = cum_a[t]
                for k in KINDS:
                    self._counts[t][k][r] = alive[t][k]

    # -- public curve accessors (all length n_rounds, index == round) --

    def delivered_curve(self, team):
        """Cumulative titanium delivered into own core (deliveries x 10)."""
        return list(self._delivered[norm_team(team)])

    def deliveries_curve(self, team):
        """Cumulative *stacks* delivered into own core."""
        return list(self._deliveries[norm_team(team)])

    def titanium_curve(self, team):
        """Global titanium balance per round (exact, from updatePlayers)."""
        t = norm_team(team)
        return [p[t]["titanium"] for p in self.players]

    def ammo_curve(self, team):
        t = norm_team(team)
        return [p[t]["ammo"] for p in self.players]

    def ti_collected_curve(self, team):
        """Engine's own titaniumCollected per round (the tiebreaker stat)."""
        t = norm_team(team)
        return [p[t]["titanium_collected"] for p in self.players]

    def ammo_spent_curve(self, team):
        """Cumulative ammo spent on turret shots (gunner 4, sentinel 10)."""
        return list(self._ammo_spent[norm_team(team)])

    def count_curve(self, team, kind):
        """Alive count of `kind` at end of each round."""
        return list(self._counts[norm_team(team)][kind])

    def damage_dealt_curve(self, team):
        """Per-round (not cumulative) damage attributed to this team."""
        return list(self._dmg_dealt[norm_team(team)])

    def damage_taken_curve(self, team):
        return list(self._dmg_taken[norm_team(team)])

    def core_hp_curve(self, team):
        """Core HP at end of each round (seeded at 500)."""
        e = self.entities.get(self.core_id(team))
        if e is None:
            return [0] * self.n_rounds
        out, hp = [], 500
        idx = 0
        for r in range(self.n_rounds):
            while idx < len(e.hp_events) and e.hp_events[idx][0] <= r:
                hp = e.hp_events[idx][2]
                idx += 1
            out.append(0 if (e.death_round is not None and r >= e.death_round) else hp)
        return out

    # ---- convenience queries --------------------------------------------

    def entities_of(self, team=None, kind=None, alive_at=None):
        out = []
        t = None if team is None else norm_team(team)
        for e in self.entities.values():
            if t is not None and e.team != t:
                continue
            if kind is not None and e.kind != kind:
                continue
            if alive_at is not None and not e.alive_at(alive_at):
                continue
            out.append(e)
        return sorted(out, key=lambda e: (e.spawn_round, e.id))

    def first_build(self, team, kind):
        """(round, pos) of this team's first entity of `kind`, or None."""
        t = norm_team(team)
        for ev in self.rounds:
            for b in ev.builds:
                if b.team == t and b.kind == kind:
                    return (b.round, b.pos)
        return None

    def rotations(self, team=None):
        """Gunner rotate() calls: EntityUpdate events where the facing changed."""
        t = None if team is None else norm_team(team)
        return [u for ev in self.rounds for u in ev.entity_updates
                if (t is None or u.team == t) and u.direction != u.prev_direction]

    def state_at(self, rnd):
        """{id: (kind, team, pos, alive)} snapshot at end of round rnd."""
        return {e.id: (e.kind, e.team, e.pos_at(rnd), True)
                for e in self.entities.values() if e.alive_at(rnd)}

    def damage_log(self, team=None, dealt=True, target_kind=None):
        """All damage HpEvents.  team + dealt=True -> damage this team dealt;
        dealt=False -> damage this team took."""
        t = None if team is None else norm_team(team)
        out = []
        for ev in self.rounds:
            for h in ev.hp:
                if h.delta >= 0:
                    continue
                if target_kind is not None and h.target_kind != target_kind:
                    continue
                if t is not None:
                    if dealt and h.source_team != t:
                        continue
                    if not dealt and h.target_team != t:
                        continue
                out.append(h)
        return out

    def heal_log(self, team=None):
        t = None if team is None else norm_team(team)
        return [h for ev in self.rounds for h in ev.hp
                if h.delta > 0 and (t is None or h.target_team == t)]

    def bot_output_log(self, team=None, contains=None, tled_only=False):
        t = None if team is None else norm_team(team)
        out = []
        for ev in self.rounds:
            for b in ev.bot_output:
                if t is not None and b.team != t:
                    continue
                if tled_only and not b.tled:
                    continue
                if contains is not None and contains not in b.stdout:
                    continue
                if not tled_only and contains is None and not b.stdout:
                    continue
                out.append(b)
        return out

    def tle_rounds(self, team):
        t = norm_team(team)
        return [b.round for ev in self.rounds for b in ev.bot_output
                if b.tled and b.team == t]

    def final_players(self):
        return self.players[-1] if self.players else [{}, {}]

    # ---- self-check ------------------------------------------------------

    def check_delivery(self):
        """core-footprint deliveries x10 must equal Player.titaniumCollected."""
        out = {}
        for t in (0, 1):
            got = self._delivered[t][-1] if self.n_rounds else 0
            want = self.final_players()[t].get("titanium_collected", 0)
            out[TEAM_NAME[t]] = {"deliveries": self._deliveries[t][-1] if self.n_rounds else 0,
                                 "delivered_ti": got,
                                 "titanium_collected": want,
                                 "ok": got == want}
        return out

    def ammo_converted(self, team) -> int:
        t = norm_team(team)
        return sum(c.amount for ev in self.rounds for c in ev.convert_ammo if c.team == t)

    def check_ammo(self):
        """converted - spent must equal the engine's final ammo balance.  This
        is the end-to-end check on turret-shooter resolution and ammo costs
        (gunner 4 / sentinel 10 / launcher 0)."""
        out = {}
        for t in (0, 1):
            conv = self.ammo_converted(t)
            spent = self._ammo_spent[t][-1] if self.n_rounds else 0
            final = self.final_players()[t].get("ammo", 0)
            out[TEAM_NAME[t]] = {"converted": conv, "spent": spent,
                                 "final_engine": final, "residual": conv - spent,
                                 "ok": conv - spent == final}
        return out

    def check_all(self):
        """Every cheap internal consistency check, as {name: (ok, detail)}."""
        checks = {}
        d = self.check_delivery()
        checks["delivery_x10_eq_titanium_collected"] = (
            all(v["ok"] for v in d.values()), d)
        a = self.check_ammo()
        checks["ammo_converted_minus_spent_eq_final"] = (
            all(v["ok"] for v in a.values()), a)
        checks["no_unknown_top_fields"] = (not self.unknown_top, self.unknown_top)
        checks["no_unknown_update_kinds"] = (not self.unknown_update_kinds,
                                             self.unknown_update_kinds)
        checks["no_unknown_turn_fields"] = (not self.unknown_turn_fields,
                                            self.unknown_turn_fields)
        checks["no_unknown_entity_kinds"] = (not self.unknown_entity_kinds,
                                             sorted(self.unknown_entity_kinds))
        checks["no_recycled_entity_ids"] = (not self.recycled_ids, self.recycled_ids[:10])
        bad_hp = [e.id for e in self.entities.values()
                  if e.hp > e.max_hp or (e.death_round is None and e.hp <= 0)]
        checks["hp_within_bounds"] = (not bad_hp, bad_hp[:10])
        unattr = sum(1 for h in self.damage_log() if h.source_kind is None)
        tot = len(self.damage_log())
        checks["damage_attribution"] = (True, f"{tot - unattr}/{tot} attributed")
        # winner consistency: if a core died, winner should be the other team
        dead_cores = [e.team for e in self.entities.values()
                      if e.kind == "core" and e.death_round is not None]
        if dead_cores and self.winner is not None:
            ok = all(t != self.winner for t in dead_cores)
            checks["winner_vs_dead_core"] = (ok, f"dead cores {dead_cores}, winner {self.winner}")
        return checks

    def summary(self) -> str:
        p = self.final_players()
        lines = [
            f"{self.path.name}: {self.width}x{self.height}, {self.n_rounds} rounds, "
            f"winner={self.winner_name} ({self.win_condition or '-'})",
            f"  cores      A@{self.core_pos(0)} B@{self.core_pos(1)}   "
            f"ore={len(self.ore)} wall={len(self.walls)}",
        ]
        for t in (0, 1):
            c = {k: self._counts[t][k][-1] for k in KINDS if self._counts[t][k][-1]}
            lines.append(
                f"  team {TEAM_NAME[t]}    ti={p[t].get('titanium',0)} "
                f"collected={p[t].get('titanium_collected',0)} "
                f"ammo={p[t].get('ammo',0)} delivered={self._delivered[t][-1]} "
                f"ammo_spent={self._ammo_spent[t][-1]} "
                f"dmg_dealt={sum(self._dmg_dealt[t])} dmg_taken={sum(self._dmg_taken[t])}")
            lines.append(f"             alive: {c}")
        return "\n".join(lines)


# --------------------------------------------------------------------------
# module-level helpers (the API the task asked for)
# --------------------------------------------------------------------------

def load_replay(path, **kw) -> Replay:
    """Parse a .replay26 into a Replay.  kw: keep_bot_output, keep_indicators,
    keep_cooldowns, attribute_damage."""
    return Replay(path, **kw)


def delivered_curve(replay: Replay, team):
    return replay.delivered_curve(team)


def first_delivery_round(replay: Replay, team):
    """Round of the first stack landing on this team's core, or None."""
    t = norm_team(team)
    for ev in replay.rounds:
        for m in ev.resource_moves:
            if m.to_core_team == t:
                return ev.round
    return None


def entity_census(replay: Replay) -> dict:
    """{'A': {...}, 'B': {...}} with built/lost/alive counts by kind, first-build
    round by kind, and headline totals."""
    out = {}
    for t in (0, 1):
        built = dict.fromkeys(KINDS, 0)
        lost = dict.fromkeys(KINDS, 0)
        alive = dict.fromkeys(KINDS, 0)
        first = {}
        for e in replay.entities.values():
            if e.team != t or e.kind not in built:
                continue
            built[e.kind] += 1
            if e.death_round is not None:
                lost[e.kind] += 1
            else:
                alive[e.kind] += 1
            if e.kind not in first or e.spawn_round < first[e.kind][0]:
                first[e.kind] = (e.spawn_round, e.spawn_pos)
        p = replay.final_players()[t]
        out[TEAM_NAME[t]] = {
            "built": {k: v for k, v in built.items() if v},
            "lost": {k: v for k, v in lost.items() if v},
            "alive": {k: v for k, v in alive.items() if v},
            "first_build": first,
            "titanium": p.get("titanium", 0),
            "titanium_collected": p.get("titanium_collected", 0),
            "ammo": p.get("ammo", 0),
            "delivered": replay.delivered_curve(t)[-1] if replay.n_rounds else 0,
            "first_delivery_round": first_delivery_round(replay, t),
            "ammo_spent": replay.ammo_spent_curve(t)[-1] if replay.n_rounds else 0,
            "damage_dealt": sum(replay.damage_dealt_curve(t)),
            "damage_taken": sum(replay.damage_taken_curve(t)),
            "tle_rounds": len(replay.tle_rounds(t)),
        }
    return out


# ---- shared match metadata (SCRATCH/replay_cache/match_info/<id>.json) ----

SCRATCH = ("/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/"
           "8c290b06-f7e1-40b4-b90c-7343eb7e2e8e/scratchpad")
MATCH_INFO_DIR = Path(SCRATCH) / "replay_cache" / "match_info"
OUR_TEAM = "OpenSverige"


def load_match_info(match_id: str) -> dict:
    """The cached `fcode match info --json` blob for a series."""
    import json
    return json.loads((MATCH_INFO_DIR / f"{match_id}.json").read_text())


def game_meta(match_id: str, game: int) -> dict:
    """One game's platform metadata: mapName, mapSeed, winnerSide, winCondition,
    turnsPlayed, plus 'our_side' (0/1) and 'opponent'."""
    info = load_match_info(match_id)
    m = info["match"]
    g = next(x for x in info["games"] if x["gameNumber"] == game)
    our = 0 if m.get("teamAName") == OUR_TEAM else 1
    g = dict(g)
    g["our_side"] = our
    g["our_side_name"] = TEAM_NAME[our]
    g["opponent"] = m["teamBName"] if our == 0 else m["teamAName"]
    g["opponent_version"] = m["teamBVersion"] if our == 0 else m["teamAVersion"]
    g["our_version"] = m["teamAVersion"] if our == 0 else m["teamBVersion"]
    g["we_won"] = (g["winnerSide"] == TEAM_NAME[our].lower())
    return g


def _main(argv):
    import json
    if len(argv) < 2:
        print(__doc__)
        return 2
    for p in argv[1:]:
        r = load_replay(p)
        print(r.summary())
        for name, (ok, detail) in r.check_all().items():
            print(f"  [{'PASS' if ok else 'FAIL'}] {name}: "
                  f"{json.dumps(detail) if not isinstance(detail, str) else detail}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
