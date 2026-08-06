#!/usr/bin/env python3
"""Extract strategy signals from Florent Code League `.replay26` files.

Answers, per replay, without the platform and without the browser visualiser:

  1. First-build round + position, per team, per entity type.  First-sentinel
     timing is the headline number — the field meta is sentinel rushing and
     what we want is the *distribution* of that timing across opponents.
  2. Chain completion: how many of each team's surviving harvesters have a
     conveyor/splitter path back to their own Core at the end of the game.
  3. Building and unit counts by type, per team, at the end of the game.
  4. The match-outcome fields the replay carries: winner and win condition.

One TSV row per replay on stdout (header first unless `--no-header`), so many
replays can be censused into one table and pivoted.  `--verbose` prints a
readable per-replay breakdown instead of the row.

Usage:
    .venv/bin/python tools/replay_census.py replay.replay26
    .venv/bin/python tools/replay_census.py -v replay.replay26
    .venv/bin/python tools/replay_census.py replays/*.replay26 > census.tsv
    .venv/bin/python tools/replay_census.py --no-header r1.replay26 >> census.tsv


THE `.replay26` FORMAT
======================

Protobuf, message `battlecode.Replay`.  **The full recovered schema, the recovery
method, and the wire-level gotchas live in `tools/replay_schema.md`** — read that
before changing anything below.  The short version, because the code leans on it:

  * `Replay { Map map = 1; repeated Turn turns = 3; optional Team winner = 4;
    string winCondition = 6; }` — field 6 is undeclared in the visualiser's own
    schema and only shows up by keeping unknown fields.
  * `turns[i]` IS round `i`, and rounds are 0-based.
  * Cores are never emitted as updates; they exist only in `map.cores` and must
    be seeded before replaying turn 0.  A Core's position is the NW corner of its
    2x2 footprint.
  * `Entity.barrier` is an empty message, so kind detection tests for field
    *presence*, not content.
  * Each team's opening Builder Bot is spawned by the bot, not the engine.

Stdlib only, no protobuf dependency — same minimal-varint approach as
tools/make_map.py, but reading instead of writing.

CHAIN COMPLETION
================

`a_chain` / `b_chain` is `completed/total` over that team's harvesters alive at
the end of the game.  A harvester counts as completed when titanium can get
from it to its own Core:

  * the harvester is orthogonally adjacent to a Core footprint tile (it can
    deliver straight into the Core — no conveyor needed), or
  * one of its 4 orthogonal neighbours holds a friendly Conveyor/Splitter that
    is in a connected group of friendly Conveyors/Splitters which touches a
    Core footprint tile.

That is undirected graph reachability: it ignores which way the conveyors face,
so it measures "did they lay the road" rather than "does the road work".

`a_chain_dir` / `b_chain_dir` answers the same question *with* facing — a
Conveyor only feeds the tile it points at, a Splitter feeds the three cardinal
neighbours that are not directly behind it.  chain_dir <= chain always, and a
large gap is the interesting case: conveyors laid that don't point anywhere.
Measured over 28 replays (56 team-sides), chain_dir is the sharper predictor of
whether the team actually banked titanium — 0 false positives against 7 for the
undirected number.  Report chain, act on chain_dir.

Both are static end-of-game snapshots, so neither says whether a chain ever
*ran*; a team can bank thousands and then lose the whole network.  Two flow
columns come straight from the `distributeResources` stream instead, which is
ground truth rather than inference:

  * `a_shipped` — harvesters (of the ones alive at the end) whose tile ever
    appeared as the `from` of a resource move.
  * `a_core_deliv` — resource moves whose `to` landed on that team's Core
    footprint: actual stacks banked over the match.  One stack is 10 Ti, so
    `core_deliv * 10 == titaniumCollected` exactly — a free end-to-end check
    that the parse is sane (56/56 team-sides, 0 mismatches).

Enemy conveyors are excluded from the graph.  Titanium *can* be pushed onto an
opposing network (see docs/game-model.md), but that is a leak, not a chain.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# --- wire format -------------------------------------------------------------

WIRE_VARINT, WIRE_64, WIRE_LEN, WIRE_32 = 0, 1, 2, 5


def _varint(buf: bytes, i: int) -> tuple[int, int]:
    result = shift = 0
    while True:
        byte = buf[i]
        i += 1
        result |= (byte & 0x7F) << shift
        if not byte & 0x80:
            return result, i
        shift += 7


def fields(buf: bytes):
    """Yield (field_number, wire_type, value) for every field in a message.

    value is an int for varints and a bytes slice for length-delimited fields.
    Unknown fields come through untouched, which is how winCondition was found.
    """
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


def scalars(buf: bytes) -> dict[int, object]:
    """Flatten a message to {field_number: value}, last occurrence winning."""
    return {num: value for num, _, value in fields(buf)}


def read_pos(buf: bytes) -> tuple[int, int]:
    d = scalars(buf)
    return d.get(1, 0), d.get(2, 0)


def packed_varints(buf: bytes) -> list[int]:
    out, i, n = [], 0, len(buf)
    while i < n:
        value, i = _varint(buf, i)
        out.append(value)
    return out


# --- schema constants --------------------------------------------------------

# Entity.<kind> field number -> our short name.
KIND_FIELDS = {
    10: "builder_bot",
    11: "conveyor",
    12: "splitter",
    15: "harvester",
    18: "barrier",
    20: "core",
    21: "gunner",
    22: "sentinel",
    24: "launcher",
}
# Order used for count columns and verbose tables.
KINDS = ["builder_bot", "core", "harvester", "conveyor", "splitter",
         "barrier", "sentinel", "gunner", "launcher"]
# Types that get first-build columns in the TSV. builder_bot is left out to keep
# the row narrower — it is near-constant at round 0 — but --verbose still shows
# it, because a bot that never spawns one (probe_idle) has no round at all.
BUILD_KINDS = ["sentinel", "gunner", "launcher", "barrier",
               "harvester", "conveyor", "splitter"]

DIRECTION_DELTA = {
    0: (0, 0), 1: (0, -1), 2: (1, -1), 3: (1, 0), 4: (1, 1),
    5: (0, 1), 6: (-1, 1), 7: (-1, 0), 8: (-1, -1),
}
CARDINALS = ((0, -1), (1, 0), (0, 1), (-1, 0))
TEAM_NAME = {0: "A", 1: "B"}
ENV_EMPTY, ENV_WALL, ENV_ORE_TITANIUM, ENV_ORE_AXIONITE = 0, 1, 2, 3


class Entity:
    __slots__ = ("id", "team", "pos", "kind", "hp", "max_hp", "direction", "built_round")

    def __init__(self, eid, team, pos, kind, hp, max_hp, direction, built_round):
        self.id = eid
        self.team = team
        self.pos = pos
        self.kind = kind
        self.hp = hp
        self.max_hp = max_hp
        self.direction = direction
        self.built_round = built_round

    def __repr__(self):
        return f"<{self.kind} #{self.id} team{self.team} at {self.pos}>"


def parse_entity(buf: bytes, built_round: int) -> Entity | None:
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
            # Entity fields 1-5 are the shared scalars; anything else that is a
            # submessage is a kind we don't know — a new entity type would land
            # here. Keep it rather than dropping the entity on the floor.
            kind = f"unknown{num}"
    if kind is None or pos is None:
        return None
    return Entity(eid, team, pos, kind, hp, max_hp, direction, built_round)


# --- replay parsing ----------------------------------------------------------

class Replay:
    """A parsed replay: final entity set, first builds, outcome, flow totals."""

    def __init__(self, path: Path, track_flow: bool = True):
        self.path = path
        data = path.read_bytes()

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
        self.rounds = len(turn_bufs)
        self._replay_turns(turn_bufs, track_flow)

    # -- map --

    def _parse_map(self, buf: bytes) -> None:
        self.width = self.height = 0
        self.tiles: list[list[int]] = []
        self.cores: list[dict] = []
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
                for cnum, _cwire, cvalue in fields(value):
                    if cnum == 1:
                        core["id"] = cvalue
                    elif cnum == 2:
                        core["team"] = cvalue
                    elif cnum == 3:
                        core["pos"] = read_pos(cvalue)
                self.cores.append(core)

    def core_footprint(self, team: int) -> set[tuple[int, int]]:
        """The 2x2 tiles a team's Core occupies. Core position is the NW corner."""
        out = set()
        for core in self.cores:
            if core["team"] == team:
                x, y = core["pos"]
                out |= {(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)}
        return out

    def env(self, x: int, y: int) -> int:
        if 0 <= y < len(self.tiles) and 0 <= x < len(self.tiles[y]):
            return self.tiles[y][x]
        return 1  # off-map behaves like wall

    # -- turns --

    def _replay_turns(self, turn_bufs, track_flow: bool) -> None:
        entities: dict[int, Entity] = {}
        # Cores exist from the start; they are never emitted as placeEntity.
        for core in self.cores:
            entities[core["id"]] = Entity(core["id"], core["team"], core["pos"],
                                          "core", 500, 500, None, 0)

        first_build: dict[tuple[int, str], tuple[int, tuple[int, int]]] = {}
        build_rounds: dict[tuple[int, str], list[int]] = {}
        players = [{}, {}]
        ship_from: set[tuple[int, int]] = set()
        core_deliveries = [0, 0]
        core_tiles = {0: self.core_footprint(0), 1: self.core_footprint(1)}
        tled_rounds = [0, 0]

        for rnd, turn_buf in enumerate(turn_bufs):
            # turns[i] IS round i, and rounds are 0-based — see the docstring.
            for _num, _wire, update_buf in fields(turn_buf):
                for unum, _uwire, ubuf in fields(update_buf):
                    if unum == 1:                                   # placeEntity
                        for enum_, _ew, ebuf in fields(ubuf):
                            if enum_ != 1:
                                continue
                            ent = parse_entity(ebuf, rnd)
                            if ent is None:
                                continue
                            entities[ent.id] = ent
                            key = (ent.team, ent.kind)
                            if key not in first_build:
                                first_build[key] = (rnd, ent.pos)
                            build_rounds.setdefault(key, []).append(rnd)
                    elif unum == 2:                                 # moveBuilderBot
                        eid = None
                        to = None
                        for mnum, _mw, mval in fields(ubuf):
                            if mnum == 1:
                                eid = mval
                            elif mnum == 2:
                                to = read_pos(mval)
                        ent = entities.get(eid)
                        if ent is not None and to is not None:
                            ent.pos = to
                    elif unum == 3:                                 # removeEntity
                        for rnum, _rw, rval in fields(ubuf):
                            if rnum == 1:
                                entities.pop(rval, None)
                    elif unum == 4 and track_flow:                  # distributeResources
                        for _mnum, _mw, move_buf in fields(ubuf):
                            src = dst = None
                            for pnum, _pw, pval in fields(move_buf):
                                if pnum == 1:
                                    src = read_pos(pval)
                                elif pnum == 2:
                                    dst = read_pos(pval)
                            if src is not None:
                                ship_from.add(src)
                            if dst is not None:
                                for team in (0, 1):
                                    if dst in core_tiles[team]:
                                        core_deliveries[team] += 1
                    elif unum == 6:                                 # updatePlayers
                        for pnum, _pw, pval in fields(ubuf):
                            if pnum != 1:
                                continue
                            for tnum, _tw, tval in fields(pval):
                                if tnum in (1, 2):
                                    d = scalars(tval)
                                    players[tnum - 1] = {
                                        "titanium": d.get(1, 0),
                                        "resources_collected": d.get(3, 0),
                                        "titanium_collected": d.get(4, 0),
                                        "ammo": d.get(7, 0),
                                    }
                    elif unum == 9:                                 # botOutput
                        d = scalars(ubuf)
                        if d.get(4):                                # tled
                            ent = entities.get(d.get(1))
                            if ent is not None:
                                tled_rounds[ent.team] += 1

        self.entities = entities
        self.first_build = first_build
        self.build_rounds = build_rounds
        self.players = players
        self.ship_from = ship_from
        self.core_deliveries = core_deliveries if track_flow else [None, None]
        self.track_flow = track_flow
        self.tled_rounds = tled_rounds
        # Entity kinds this build of the parser doesn't know about. Should always
        # be empty; if the organisers add an entity type it shows up here rather
        # than quietly vanishing from the counts.
        self.unknown_kinds = {kind for _team, kind in build_rounds
                              if kind.startswith("unknown")}

    # -- derived --

    def counts(self, team: int) -> dict[str, int]:
        out = dict.fromkeys(KINDS, 0)
        for ent in self.entities.values():
            if ent.team == team and ent.kind in out:
                out[ent.kind] += 1
        return out

    def chains(self, team: int) -> dict:
        """Chain completion for one team. See CHAIN COMPLETION in the docstring."""
        core_tiles = self.core_footprint(team)
        relay: dict[tuple[int, int], Entity] = {}
        harvesters: list[Entity] = []
        for ent in self.entities.values():
            if ent.team != team:
                continue
            if ent.kind in ("conveyor", "splitter"):
                relay[ent.pos] = ent
            elif ent.kind == "harvester":
                harvesters.append(ent)

        # Undirected: which relay tiles sit in a group that touches the Core?
        connected: set[tuple[int, int]] = set()
        seen: set[tuple[int, int]] = set()
        for start in relay:
            if start in seen:
                continue
            group, stack, touches = [], [start], False
            seen.add(start)
            while stack:
                x, y = stack.pop()
                group.append((x, y))
                for dx, dy in CARDINALS:
                    n = (x + dx, y + dy)
                    if n in core_tiles:
                        touches = True
                    elif n in relay and n not in seen:
                        seen.add(n)
                        stack.append(n)
            if touches:
                connected.update(group)

        # Directed: honour conveyor/splitter facing. Walk backwards from the Core.
        def outputs(ent: Entity) -> list[tuple[int, int]]:
            x, y = ent.pos
            d = ent.direction or 0
            if ent.kind == "conveyor":
                dx, dy = DIRECTION_DELTA.get(d, (0, 0))
                return [] if (dx, dy) == (0, 0) else [(x + dx, y + dy)]
            # Splitter: input from directly behind, output to the other three.
            bdx, bdy = DIRECTION_DELTA.get(d, (0, 0))
            back = (-bdx, -bdy)
            return [(x + dx, y + dy) for dx, dy in CARDINALS if (dx, dy) != back]

        reverse: dict[tuple[int, int], list[tuple[int, int]]] = {}
        seeds = []
        for pos, ent in relay.items():
            outs = outputs(ent)
            if any(o in core_tiles for o in outs):
                seeds.append(pos)
            for o in outs:
                if o in relay:
                    reverse.setdefault(o, []).append(pos)
        delivering = set(seeds)
        stack = list(seeds)
        while stack:
            cur = stack.pop()
            for prev in reverse.get(cur, ()):
                if prev not in delivering:
                    delivering.add(prev)
                    stack.append(prev)

        rows = []
        for ent in sorted(harvesters, key=lambda e: e.id):
            x, y = ent.pos
            neighbours = [(x + dx, y + dy) for dx, dy in CARDINALS]
            direct = any(n in core_tiles for n in neighbours)
            ok = direct or any(n in connected for n in neighbours)
            ok_dir = direct or any(n in delivering for n in neighbours)
            rows.append({
                "entity": ent,
                "connected": ok,
                "directed": ok_dir,
                "direct_to_core": direct,
                "shipped": ent.pos in self.ship_from,
            })
        return {
            "harvesters": rows,
            "total": len(rows),
            "connected": sum(1 for r in rows if r["connected"]),
            "directed": sum(1 for r in rows if r["directed"]),
            "shipped": sum(1 for r in rows if r["shipped"]),
            "relays": len(relay),
            "relays_connected": len(connected),
        }


# --- reporting ---------------------------------------------------------------

def _columns() -> list[str]:
    cols = ["file", "map_w", "map_h", "rounds", "winner", "win_condition"]
    for metric in ("titanium", "ti_collected", "chain", "chain_dir",
                   "shipped", "core_deliv"):
        cols += [f"a_{metric}", f"b_{metric}"]
    for kind in BUILD_KINDS:
        cols += [f"a_{kind}_r", f"a_{kind}_at", f"b_{kind}_r", f"b_{kind}_at"]
    for kind in KINDS:
        cols += [f"a_n_{kind}", f"b_n_{kind}"]
    return cols


def census(replay: Replay) -> dict:
    chain = {team: replay.chains(team) for team in (0, 1)}
    counts = {team: replay.counts(team) for team in (0, 1)}
    row = {
        "file": replay.path.name,
        "map_w": replay.width,
        "map_h": replay.height,
        "rounds": replay.rounds,
        "winner": TEAM_NAME.get(replay.winner, "-"),
        "win_condition": replay.win_condition or "-",
    }
    for team, tag in ((0, "a"), (1, "b")):
        p = replay.players[team]
        row[f"{tag}_titanium"] = p.get("titanium", "")
        row[f"{tag}_ti_collected"] = p.get("titanium_collected", "")
        c = chain[team]
        row[f"{tag}_chain"] = f"{c['connected']}/{c['total']}"
        row[f"{tag}_chain_dir"] = f"{c['directed']}/{c['total']}"
        row[f"{tag}_shipped"] = f"{c['shipped']}/{c['total']}" if replay.track_flow else ""
        row[f"{tag}_core_deliv"] = "" if replay.core_deliveries[team] is None \
            else replay.core_deliveries[team]
        for kind in BUILD_KINDS:
            got = replay.first_build.get((team, kind))
            row[f"{tag}_{kind}_r"] = got[0] if got else ""
            row[f"{tag}_{kind}_at"] = f"{got[1][0]},{got[1][1]}" if got else ""
        for kind in KINDS:
            row[f"{tag}_n_{kind}"] = counts[team][kind]
    row["_chain"] = chain
    row["_counts"] = counts
    return row


def tsv_row(row: dict) -> str:
    return "\t".join(str(row[c]) for c in _columns())


def verbose_report(replay: Replay, row: dict, out) -> None:
    w = out.write
    w(f"\n=== {replay.path} ===\n")
    w(f"  map          {replay.width}x{replay.height}   "
      f"cores " + "  ".join(f"{TEAM_NAME[c['team']]}@{c['pos'][0]},{c['pos'][1]}"
                            for c in sorted(replay.cores, key=lambda c: c["team"])) + "\n")
    ore = sum(r.count(ENV_ORE_TITANIUM) for r in replay.tiles)
    wall = sum(r.count(ENV_WALL) for r in replay.tiles)
    w(f"  terrain      {ore} titanium ore, {wall} wall\n")
    w(f"  outcome      winner={TEAM_NAME.get(replay.winner, 'none')}  "
      f"condition={replay.win_condition or 'none'}  rounds={replay.rounds}\n")
    if replay.unknown_top:
        w(f"  unknown top-level fields: {replay.unknown_top}\n")
    if replay.unknown_kinds:
        w(f"  UNKNOWN ENTITY KINDS: {sorted(replay.unknown_kinds)} — "
          f"the schema in tools/replay_schema.md is out of date\n")

    w("\n  final economy\n")
    w(f"    {'':14s}{'A':>12s}{'B':>12s}\n")
    for label, key in (("titanium", "titanium"),
                       ("ti collected", "titanium_collected"),
                       ("resources", "resources_collected"),
                       ("ammo", "ammo")):
        a = replay.players[0].get(key, "-")
        b = replay.players[1].get(key, "-")
        w(f"    {label:14s}{a:>12}{b:>12}\n")
    deliv = ["-" if d is None else d for d in replay.core_deliveries]
    w(f"    {'core deliv':14s}{deliv[0]:>12}{deliv[1]:>12}\n")
    if any(replay.tled_rounds):
        w(f"    {'TLE rounds':14s}{replay.tled_rounds[0]:>12}{replay.tled_rounds[1]:>12}\n")

    w("\n  first build (round, position) and total builds\n")
    w(f"    {'type':12s}{'A round':>9s}{'A at':>10s}{'A built':>9s}"
      f"{'B round':>9s}{'B at':>10s}{'B built':>9s}\n")
    for kind in BUILD_KINDS + ["builder_bot"]:
        cells = []
        for team in (0, 1):
            got = replay.first_build.get((team, kind))
            n = len(replay.build_rounds.get((team, kind), ()))
            if got:
                cells += [str(got[0]), f"{got[1][0]},{got[1][1]}", str(n)]
            else:
                cells += ["-", "-", "0"]
        w(f"    {kind:12s}{cells[0]:>9s}{cells[1]:>10s}{cells[2]:>9s}"
          f"{cells[3]:>9s}{cells[4]:>10s}{cells[5]:>9s}\n")

    w("\n  end-of-game counts\n")
    w(f"    {'type':14s}{'A':>12s}{'B':>12s}\n")
    for kind in KINDS:
        w(f"    {kind:14s}{row['_counts'][0][kind]:>12}{row['_counts'][1][kind]:>12}\n")

    w("\n  chain completion (harvester -> own Core)\n")
    for team, tag in ((0, "A"), (1, "B")):
        c = row["_chain"][team]
        shipped = (f"{c['shipped']}/{c['total']} ever shipped, "
                   if replay.track_flow else "")
        w(f"    team {tag}: {c['connected']}/{c['total']} connected, "
          f"{c['directed']}/{c['total']} facing-correct, {shipped}"
          f"{c['relays_connected']}/{c['relays']} relay tiles wired to the Core\n")
        for r in c["harvesters"]:
            e = r["entity"]
            marks = []
            if r["direct_to_core"]:
                marks.append("adjacent to Core")
            marks.append("connected" if r["connected"] else "ORPHAN")
            if r["connected"] and not r["directed"]:
                marks.append("facing wrong")
            if replay.track_flow:
                marks.append("shipped" if r["shipped"] else "never shipped")
            w(f"      #{e.id:<5d} at {e.pos[0]:>2},{e.pos[1]:<2}  built r{e.built_round:<4d}"
              f"  hp {e.hp}/{e.max_hp}  {', '.join(marks)}\n")
    w("\n")


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__.split("\n\nTHE `.replay26`")[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("replays", nargs="+", type=Path, help=".replay26 files")
    ap.add_argument("-v", "--verbose", action="store_true",
                    help="readable per-replay breakdown instead of the TSV row")
    ap.add_argument("--no-header", action="store_true",
                    help="omit the TSV header line (for appending to a table)")
    ap.add_argument("--no-flow", action="store_true",
                    help="skip distributeResources parsing (faster; blanks the "
                         "shipped/core_deliv columns)")
    args = ap.parse_args()

    if not args.verbose and not args.no_header:
        print("\t".join(_columns()))

    failures = 0
    for path in args.replays:
        try:
            replay = Replay(path, track_flow=not args.no_flow)
            row = census(replay)
        except Exception as exc:                      # noqa: BLE001 - report and continue
            print(f"{path}: FAILED — {type(exc).__name__}: {exc}", file=sys.stderr)
            failures += 1
            continue
        if replay.unknown_kinds:
            print(f"{path}: unknown entity kinds {sorted(replay.unknown_kinds)} — "
                  f"tools/replay_schema.md needs updating", file=sys.stderr)
        if args.verbose:
            verbose_report(replay, row, sys.stdout)
        else:
            print(tsv_row(row))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
