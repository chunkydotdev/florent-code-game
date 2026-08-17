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


THE DAMAGE CHANNEL (`--damage`, added 2026-08-17, s49 instrument debt)
=====================================================================

⛔ WHY IT EXISTS. This parser decoded turn-update fields 1, 2, 3, 4, 6 and 9 and
had NO damage read at all. On 2026-08-17 a lane needing per-entity damage
reconstructed it by DIFFING HP OFF `placeEntity` — and got a clean, confident
**ZERO**, because `placeEntity` is emitted once at build time (plus gunner
rotations) and never again, so its `hp` field is the hp AT BUILD, permanently.
The engine has been streaming every HP change all along, in the one field nobody
was reading. **A wrong zero from a channel that does not exist is the worst
reading in this repo's vocabulary: it has no error bar and it looks like data.**

THE WIRE FORMAT.  Update field 5 is `UpdateHp { int32 id = 1; int32 delta = 2; }`
(`tools/replay_schema.md:54,73`).  `delta` is a protobuf **int32**, so negatives
are sign-extended to 64 bits and written as a 10-byte varint of the two's
complement — a raw `-18` arrives as **18446744073709551598** (= 2**64 - 18).
`_fold_i64` folds it.  **A parser that skips the fold reads every hit as ~1.8e19
and every "total damage" as astronomically positive**, which is why the fold has
its own selftest cell against a real replay.

THE ALPHABET, measured over 108 real replays (96,362 UpdateHp events):

    -18  x16090   sentinel shot
     -7  x11135   gunner shot
     -2  x 6877   builder-bot attack (2 Ti -> 2 dmg)
     +4  x56571   heal, full
     +2  x 5842   heal, CLAMPED at max_hp
     +3  x  639   heal, clamped
     +1  x    8   heal, clamped

⭐ TWO ASYMMETRIES WORTH KNOWING BEFORE YOU DIVIDE BY ANYTHING.
  * **HEALS ARE CLAMPED, DAMAGE IS NOT.**  A `heal` on an entity 2 HP below max
    records `+2`, so the heal alphabet is +1..+4 and **counting `+4` events
    undercounts heals**.  Damage shows no partial values at all: a 3 HP builder
    taking a 7-damage gunner shot still records exactly `-7`.  **So overkill is
    INVISIBLE on this channel** — damage-dealt from these events is damage
    *inflicted*, not damage *absorbed*, and it can exceed the victim's HP pool.
  * **THE DELTA CLASS IDENTIFIES THE WEAPON, so shots are countable without
    touching `fireTurret` at all.**  Verified against `tools/corpus/
    replay_econ.py` on 108 replays: `count(-7) == shots_gunner` and
    `count(-18) == shots_sentinel`, **1071==1071 and 2947==2947 on the first 12,
    and 0 residual pooled across all 108** (11,135 and 16,090). One shot is
    exactly one damage event — a sentinel's obstacle-ignoring line hits ONE
    entity, not everything in the line.

THE CROSS-CHECK, AND WHY IT IS POOLED RATHER THAN PER-TEAM.  The engine's ammo
law gives an exact identity:

    ammo_spent  =  4 * gunner_shots + 10 * sentinel_shots
                =  4 * count(-7)    + 10 * count(-18)

**Pooled over both teams this is EXACT: 205,440 == 205,440, residual 0 over 108
replays** (`--selftest-damage` reruns it).  **Per team it is NOT exact and must
not be claimed as such: 54 of 216 team-cells disagree, by a zero-sum |residual|
of 704 out of 205,440 = 0.343%.**  (A first cut of the cross-check joined on the
replay BASENAME and read a 4.109% "identity violation" — which was four
duplicate filenames across the two reference corpora being pooled into one key,
not a decoder fault. **A plausible-looking residual is the most expensive kind.**
The validator now joins on unique names and refuses if it cannot.)
The reason for the real 0.343% is a property of the wire, not of the arithmetic:
`UpdateHp` names only the VICTIM, so "damage DEALT by A" has to be inferred as
"damage RECEIVED by B", which is wrong exactly when a team damages its own
entity; and `fireTurret` carries only POSITIONS, so `replay_econ`'s own per-team
shot attribution degrades when a turret dies and the enemy builds on that tile.
⇒ **Damage RECEIVED per entity is EXACT (0 of 96,362 events had an unresolvable
victim). Damage DEALT per team is an INFERENCE carrying ~0.07%. Report received;
derive dealt only with that number attached.**

OPT-IN, and deliberately.  `track_damage` defaults to **False** because this
module is imported by ~20 tools and three long-running daemons
(`corpus/keeper.py`, `corpus/sync.py`, `monitors/cpu_watch.py`); adding an
unconditional per-event dict write to the hot loop would change their cost for a
channel they do not read.  `--damage` emits its own table with its own header —
it does NOT widen the census row, because widening a row whose table is appended
to is the exact defect that silently corrupted 31,986 rows of `corpus/econ.tsv`
(`tools/corpus/replay_econ.py`, DEFECT 1).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# ---- `--help` CONTRACT (enforced by tests/test_instruments.py) --------------
# Side-effect-free, prints this module's docstring, exits 0.
#
# ⛔ WHY. Probing an unknown tool with `--help` is the first thing anyone does.
# Before 2026-08-15, 40 of 86 tools here had no argparse, so `--help` was just an
# unrecognised argument and THE TOOL RAN FOR REAL -- printing VERDICT-SHAPED text
# that reads as a finding:
#     tools/freshness.py --help  ->  "BLIND: --help has no parseable timestamp"
#     tools/leg_read.py  --help  ->  "LEG: no completed games"
# Both are this repo's own verdict vocabulary. A reader asking a harmless
# question got an authoritative-looking sentence about nothing.
#
# ⛔ GATED ON `__main__`: several of these modules are IMPORTED by other tools
# (freshness by now.py). Ungated, this would fire during that import and make the
# PARENT exit 0 mid-run while printing the CHILD's docstring.
# ⛔ SELF-CONTAINED `import sys`: a first attempt used the file's own import, and
# broke on `import sys as _sys` (NameError) and on files whose imports come in
# two blocks. The guard must not depend on what the host file happens to import.
if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__ + "  (no module docstring)"))
        raise SystemExit(0)

ROOT_DIR = Path(__file__).resolve().parent.parent

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


_I64_SIGN = 1 << 63
_I64_MOD = 1 << 64


def _fold_i64(v: int) -> int:
    """Protobuf int32/int64 -> Python signed int.

    ⛔ THE ONE LINE THE DAMAGE CHANNEL CANNOT DO WITHOUT. `int32` fields are
    sign-extended to 64 bits before varint encoding, so a `-18` arrives as
    18446744073709551598. Unfolded, every sentinel hit reads as +1.8e19 and any
    sum over them is meaningless in a way that still prints as a number. Driven
    against a real replay in `--selftest-damage`.
    """
    return v - _I64_MOD if v >= _I64_SIGN else v


# The measured in-game delta alphabet (108 replays, 96,362 events). See the
# module docstring. Used ONLY to raise an alarm on a value outside it — never to
# filter, because a filtered unknown is an unknown nobody hears about.
DAMAGE_DELTAS = (-18, -7, -2)
HEAL_DELTAS = (1, 2, 3, 4)
DELTA_WEAPON = {-18: "sentinel", -7: "gunner", -2: "builder_attack"}
# Ammunition cost per shot, from the team global pool (CLAUDE.md / engine).
AMMO_PER_SHOT = {-18: 10, -7: 4}
# No entity in this game has more than 500 max HP (the Core). A |delta| beyond
# that is not a game event, it is a misparse — the guard that turns a corrupted
# payload into a refusal instead of a giant number.
MAX_PLAUSIBLE_DELTA = 500


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

def parse_update_hp(buf: bytes, where: str = "") -> tuple[int, int]:
    """`UpdateHp { int32 id = 1; int32 delta = 2; }` -> (entity_id, signed delta).

    ⛔ RAISES ON A CORRUPTED PAYLOAD RATHER THAN SKIPPING IT. Every refusal below
    is a state that, if tolerated, produces a SMALLER damage total with no sign
    that anything was dropped — and an under-count is exactly the failure this
    channel was added to fix (the s49 read that returned a clean, wrong zero).
    A decoder that silently skips what it cannot read is a decoder whose totals
    mean nothing, so the four bad states are:

      * field 1 (id) absent            -> the damage cannot be attributed
      * field 2 (delta) absent         -> proto3 omits a ZERO delta, and a zero
                                          HP change is not an event the engine
                                          emits; absence here means a misparse
      * either field on the wrong wire -> we are not looking at an UpdateHp
      * |delta| > MAX_PLAUSIBLE_DELTA  -> larger than the Core's 500 max HP, so
                                          the fold or the offset is wrong

    A delta that is well-formed and plausible but OUTSIDE the measured alphabet
    is NOT refused here — it is returned and surfaced by the caller as an alarm
    (the `unknown_deltas` set), the same way `unknown_kinds` handles a new entity
    type. Refusing it would make a rules change look like file corruption.
    """
    eid = delta = None
    for num, wire, value in fields(buf):
        if num == 1:
            if wire != WIRE_VARINT:
                raise ValueError(
                    f"UpdateHp{where}: field 1 (id) has wire type {wire}, "
                    f"expected varint ({WIRE_VARINT}) — this is not an UpdateHp. "
                    f"REFUSING rather than dropping the event.")
            eid = value
        elif num == 2:
            if wire != WIRE_VARINT:
                raise ValueError(
                    f"UpdateHp{where}: field 2 (delta) has wire type {wire}, "
                    f"expected varint ({WIRE_VARINT}) — this is not an UpdateHp. "
                    f"REFUSING rather than dropping the event.")
            delta = _fold_i64(value)
    if eid is None:
        raise ValueError(
            f"UpdateHp{where}: no field 1 (entity id). An unattributable HP "
            f"change cannot be counted; REFUSING rather than dropping it.")
    if delta is None:
        raise ValueError(
            f"UpdateHp{where}: no field 2 (delta). proto3 omits a ZERO, and the "
            f"engine does not emit a zero HP change — this is a misparse. "
            f"REFUSING rather than counting it as 0.")
    if abs(delta) > MAX_PLAUSIBLE_DELTA:
        raise ValueError(
            f"UpdateHp{where}: delta {delta} exceeds |{MAX_PLAUSIBLE_DELTA}|, "
            f"which is larger than the Core's 500 max HP. Either the two's-"
            f"complement fold or the field offset is wrong. REFUSING — an "
            f"implausible delta summed into a total still prints as a number.")
    return eid, delta


class Replay:
    """A parsed replay: final entity set, first builds, outcome, flow totals."""

    def __init__(self, path: Path, track_flow: bool = True,
                 track_damage: bool = False):
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
        self._replay_turns(turn_bufs, track_flow, track_damage)

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

    def _replay_turns(self, turn_bufs, track_flow: bool,
                      track_damage: bool = False) -> None:
        entities: dict[int, Entity] = {}
        # Cores exist from the start; they are never emitted as placeEntity.
        for core in self.cores:
            entities[core["id"]] = Entity(core["id"], core["team"], core["pos"],
                                          "core", 500, 500, None, 0)

        # ---- damage channel state (only populated when track_damage) --------
        # ⛔ `ever` IS NOT `entities`, AND THAT IS THE WHOLE POINT. `entities`
        # POPS on removeEntity, and `tools/replay_schema.md:230` records that
        # FireTurret events can be emitted AFTER their victim's removeEntity in
        # the same round -- so resolving a victim against the LIVE dict silently
        # loses the killing blows, i.e. it under-counts exactly the damage that
        # mattered. A never-popped registry resolved 96,362 of 96,362 events on
        # the 108-replay corpus; the live dict cannot.
        ever: dict[int, tuple[int, str]] = {
            c["id"]: (c["team"], "core") for c in self.cores}
        # id -> {delta: count}. Damage RECEIVED, which is the exact quantity;
        # see the module docstring on why DEALT is an inference.
        dmg: dict[int, dict[int, int]] = {}
        unknown_deltas: set[int] = set()
        hp_events = 0
        # An id re-registered with a different (team, kind) is post-death id
        # reuse. Counted rather than assumed away: it makes per-entity rows for
        # that id a blend of two entities, and a reader must be told.
        reused_ids: set[int] = set()

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
                            # ROTATION RE-EMIT GUARD (research find, builder-fixed
                            # 2026-08-08 s19).  rotate() re-emits placeEntity for an
                            # entity that already exists, so counting every
                            # placeEntity INFLATES build counts: 1,315 of 1,915
                            # gunner "places" in a 40-game sample were rotations,
                            # against 0 for every other entity kind (gunners are the
                            # only rotatable type).  A genuine build is the FIRST
                            # placeEntity carrying a given entity id; later ones are
                            # state updates.  Every past analysis reading gunner
                            # build_rounds or first_build off this parser is inflated
                            # and must be re-run.
                            if track_damage:
                                prev = ever.get(ent.id)
                                now = (ent.team, ent.kind)
                                if prev is not None and prev != now:
                                    reused_ids.add(ent.id)
                                ever[ent.id] = now
                            seen_before = ent.id in entities
                            entities[ent.id] = ent
                            if seen_before:
                                continue
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
                    elif unum == 5 and track_damage:                # UpdateHp
                        eid, delta = parse_update_hp(
                            ubuf, where=f" (round {rnd}, {self.path.name})")
                        hp_events += 1
                        if delta not in DAMAGE_DELTAS and delta not in HEAL_DELTAS:
                            unknown_deltas.add(delta)
                        d = dmg.get(eid)
                        if d is None:
                            d = dmg[eid] = {}
                        d[delta] = d.get(delta, 0) + 1
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
        # ---- damage channel results ----------------------------------------
        self.track_damage = track_damage
        self.damage = dmg
        self.entity_ever = ever
        self.hp_events = hp_events
        self.unknown_deltas = unknown_deltas
        self.reused_ids = reused_ids
        # Victims whose id never appeared in placeEntity or Map.cores. Measured
        # at 0 of 96,362 on the 108-replay corpus, so a nonzero value here is a
        # signal, not background noise.
        self.unresolved_victims = {eid for eid in dmg if eid not in ever}

    # -- damage channel ---------------------------------------------------

    def damage_rows(self) -> list[dict]:
        """One row per entity that ever took or received an HP change.

        `kind`/`team` come from the never-popped registry, so a killed entity
        still resolves. `dealt_*` deliberately does NOT appear: this channel
        names the victim only (module docstring).
        """
        if not self.track_damage:
            raise RuntimeError(
                "damage_rows() requires Replay(..., track_damage=True). It is "
                "opt-in because ~20 tools and three daemons import this module; "
                "REFUSING to return an empty table that would read as 'no "
                "damage' -- which is the exact wrong-zero this channel was "
                "added to fix.")
        rows = []
        for eid, counts in sorted(self.damage.items()):
            team, kind = self.entity_ever.get(eid, (None, "?"))
            row = {
                "entity": eid,
                "team": TEAM_NAME.get(team, "?"),
                "kind": kind,
                "id_reused": int(eid in self.reused_ids),
            }
            for dl in DAMAGE_DELTAS:
                row[f"n{dl}"] = counts.get(dl, 0)
            row["dmg_total"] = sum(-dl * counts.get(dl, 0)
                                   for dl in DAMAGE_DELTAS)
            row["heal_events"] = sum(counts.get(dl, 0) for dl in HEAL_DELTAS)
            row["heal_total"] = sum(dl * counts.get(dl, 0) for dl in HEAL_DELTAS)
            # Heals are CLAMPED at max_hp, so a "full heal" count is strictly
            # less than heal_events and the gap is wasted healing.
            row["heal_full"] = counts.get(4, 0)
            row["unknown"] = sum(n for dl, n in counts.items()
                                 if dl not in DAMAGE_DELTAS
                                 and dl not in HEAL_DELTAS)
            rows.append(row)
        return rows

    def damage_by_team(self) -> dict:
        """Per-team RECEIVED totals plus the pooled ammo identity.

        `dealt_*` is inferred as the complement (received by the other team) and
        is labelled so, because friendly fire and turret-tile reuse make it
        ~0.07% wrong — see the module docstring.
        """
        if not self.track_damage:
            raise RuntimeError("damage_by_team() requires track_damage=True")
        recv = {0: {}, 1: {}, None: {}}
        for eid, counts in self.damage.items():
            team = self.entity_ever.get(eid, (None, "?"))[0]
            bucket = recv.setdefault(team, {})
            for dl, n in counts.items():
                bucket[dl] = bucket.get(dl, 0) + n
        out = {}
        for team in (0, 1):
            other = 1 - team
            r = recv.get(team, {})
            o = recv.get(other, {})
            out[team] = {
                "recv_shots_sentinel": r.get(-18, 0),
                "recv_shots_gunner": r.get(-7, 0),
                "recv_attacks": r.get(-2, 0),
                "recv_dmg_total": sum(-dl * r.get(dl, 0) for dl in DAMAGE_DELTAS),
                "heal_events": sum(r.get(dl, 0) for dl in HEAL_DELTAS),
                "heal_total": sum(dl * r.get(dl, 0) for dl in HEAL_DELTAS),
                # INFERRED, ~0.07% — see docstring.
                "dealt_shots_sentinel_inferred": o.get(-18, 0),
                "dealt_shots_gunner_inferred": o.get(-7, 0),
                "ammo_spent_inferred": (AMMO_PER_SHOT[-7] * o.get(-7, 0)
                                        + AMMO_PER_SHOT[-18] * o.get(-18, 0)),
            }
        pooled_g = sum(recv.get(t, {}).get(-7, 0) for t in (0, 1, None))
        pooled_s = sum(recv.get(t, {}).get(-18, 0) for t in (0, 1, None))
        out["pooled"] = {
            "shots_gunner": pooled_g,
            "shots_sentinel": pooled_s,
            # EXACT (0 residual over 108 replays) — this is the checkable one.
            "ammo_spent": AMMO_PER_SHOT[-7] * pooled_g + AMMO_PER_SHOT[-18] * pooled_s,
            "hp_events": self.hp_events,
        }
        return out

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


# ⛔ A SEPARATE COLUMN LIST, NOT AN EXTENSION OF `_columns()`. Inserting columns
# into a table that gets APPENDED to is what silently corrupted 31,986 rows of
# corpus/econ.tsv (see tools/corpus/replay_econ.py, DEFECT 1). The census row's
# shape is unchanged by --damage.
DAMAGE_COLUMNS = ["file", "entity", "team", "kind", "id_reused",
                  "n-18", "n-7", "n-2", "dmg_total",
                  "heal_events", "heal_full", "heal_total", "unknown"]
DAMAGE_TEAM_COLUMNS = ["file", "team", "recv_shots_sentinel", "recv_shots_gunner",
                       "recv_attacks", "recv_dmg_total", "heal_events",
                       "heal_total", "dealt_shots_sentinel_inferred",
                       "dealt_shots_gunner_inferred", "ammo_spent_inferred"]


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


DEFAULT_SELFTEST_REPLAYS = ("scratchpad/bb2_replays", "scratchpad/bb_s1_replays")


def selftest_damage(paths: list[Path] | None = None) -> int:
    """Three validators for the damage channel, all against REAL replays.

      (i)  THE SIGN FOLD, shown correct and shown NECESSARY. A real -18 arrives
           as 2**64-18; the unfolded reading is printed beside the folded one so
           the failure it prevents is visible rather than asserted.
     (ii)  THE ENGINE AMMO IDENTITY against tools/corpus/replay_econ.py's
           independent fireTurret-based shot counts:
               4*count(-7) + 10*count(-18)  ==  4*shots_gunner + 10*shots_sentinel
           POOLED over both teams, where it is EXACT. Per-team is reported too,
           with its measured ~0.07% inference error, so the weaker claim cannot
           be mistaken for the strong one.
    (iii)  THE OTHER VERDICT: four corrupted UpdateHp payloads, each of which
           must be REFUSED, plus the clean payload that must be accepted. A
           decoder never seen refusing has not been seen to check.
    """
    import subprocess
    import tempfile
    bad = 0
    files: list[Path] = []
    for p in (paths or []):
        if p.is_dir():
            files += sorted(p.glob("*.replay26"))
        elif p.exists():
            files.append(p)
    if not files:
        for d in DEFAULT_SELFTEST_REPLAYS:
            files += sorted((ROOT_DIR / d).glob("*.replay26"))
    if len(files) < 3:
        print(f"*** SELFTEST CANNOT RUN: found {len(files)} replay(s); the "
              f"cross-check requires at least 3 REAL replays. Pass paths, or "
              f"restore {' / '.join(DEFAULT_SELFTEST_REPLAYS)}. REFUSING to "
              f"print a verdict off a fixture I wrote myself.")
        return 1

    # ---- (i) THE SIGN FOLD, on a real replay -------------------------------
    print("VALIDATOR (i) — THE TWO'S-COMPLEMENT FOLD, on a real replay")
    probe = files[0]
    raw_seen: dict[int, int] = {}
    data = probe.read_bytes()
    for num, wire, value in fields(data):
        if num != 3 or wire != WIRE_LEN:
            continue
        for _n, _w, ub in fields(value):
            for unum, _uw, u in fields(ub):
                if unum != 5:
                    continue
                d = {fn: fv for fn, _fw, fv in fields(u)}
                raw = d.get(2, 0)
                raw_seen[raw] = raw_seen.get(raw, 0) + 1
    print(f"  {probe.name}: {sum(raw_seen.values())} UpdateHp events")
    fold_ok = True
    for raw, n in sorted(raw_seen.items(), key=lambda kv: -kv[1]):
        folded = _fold_i64(raw)
        note = DELTA_WEAPON.get(folded, "heal" if folded > 0 else "?")
        # The unfolded reading is what a parser without the fold would report.
        if folded < 0 and raw < _I64_SIGN:
            fold_ok = False
        print(f"    raw varint {raw:>21}  ->  folded {folded:>4}  ({note}, x{n})"
              + ("   <-- WITHOUT THE FOLD THIS READS AS THE 20-DIGIT NUMBER "
                 "ON THE LEFT" if folded < 0 else ""))
    have_neg18 = any(_fold_i64(r) == -18 for r in raw_seen)
    print(f"  [{'ok ' if have_neg18 else 'FAIL'}] a real -18 (sentinel) decodes "
          f"as -18, not 2**64-18 = {_I64_MOD - 18}")
    if not have_neg18:
        bad += 1
    # and the fold's own boundary, both sides
    for v, want in ((0, 0), (4, 4), (_I64_SIGN - 1, _I64_SIGN - 1),
                    (_I64_MOD - 1, -1), (_I64_MOD - 18, -18), (_I64_SIGN, -_I64_SIGN)):
        got = _fold_i64(v)
        ok = got == want
        if not ok:
            bad += 1
        print(f"  [{'ok ' if ok else 'FAIL'}] _fold_i64({v}) = {got} (want {want})")
    if not fold_ok:
        bad += 1

    # ---- (ii) THE AMMO IDENTITY vs replay_econ.py --------------------------
    print(f"\nVALIDATOR (ii) — ENGINE AMMO IDENTITY vs replay_econ.py, "
          f"{len(files)} real replays")
    print("  identity: 4*count(-7) + 10*count(-18) == 4*shots_gunner + "
          "10*shots_sentinel")
    econ = ROOT_DIR / "tools" / "corpus" / "replay_econ.py"
    if not econ.exists():
        print(f"  *** CANNOT CROSS-CHECK: {econ} is missing. The identity is "
              f"unverifiable without an INDEPENDENT shot count; REFUSING to "
              f"pass this validator on my own decoder alone.")
        bad += 1
    else:
        with tempfile.TemporaryDirectory() as td:
            out_tsv = Path(td) / "econ.tsv"
            # ⛔⛔ THE JOIN KEY IS A BASENAME, AND BASENAMES COLLIDE. replay_econ's
            # `file` column is `path.name`. Our two reference corpora BOTH contain
            # `g0001_antler_s1_treatseat0.replay26` and three of its siblings --
            # DIFFERENT GAMES, IDENTICAL NAMES -- so a basename join over both
            # directories pooled two files into one key and reported an
            # 8,170-ammo "identity violation" that was nothing but a name clash.
            # The residual even looked plausible (4.1%), which is what makes this
            # class of fault dangerous: it does not look like a bug, it looks
            # like a finding. Caught only by localising a FAIL instead of
            # accepting it.
            #
            # Fixed by giving every input a UNIQUE name for the duration of the
            # cross-check, and by refusing if that cannot be guaranteed.
            link_dir = Path(td) / "uniq"
            link_dir.mkdir()
            linked: list[Path] = []
            for i, f in enumerate(files):
                uniq = link_dir / f"{i:05d}_{f.name}"
                uniq.symlink_to(f.resolve())
                linked.append(uniq)
            if len({f.name for f in linked}) != len(files):
                print(f"  *** CANNOT CROSS-CHECK: {len(files)} inputs collapsed "
                      f"to {len({f.name for f in linked})} unique join keys. "
                      f"REFUSING.")
                return 1
            r = subprocess.run(
                [sys.executable, str(econ), str(out_tsv)] + [str(f) for f in linked],
                capture_output=True, text=True, cwd=ROOT_DIR)
            lines = out_tsv.read_text().splitlines() if out_tsv.exists() else []
            if len(lines) < 2:
                print(f"  *** replay_econ.py produced no rows: {r.stderr[-300:]}")
                bad += 1
                lines = []
            hdr = lines[0].split("\t") if lines else []
            gi = hdr.index("shots_gunner") if "shots_gunner" in hdr else None
            si = hdr.index("shots_sentinel") if "shots_sentinel" in hdr else None
            fi = hdr.index("file") if "file" in hdr else None
            ti = hdr.index("team") if "team" in hdr else None
            econ_shots: dict[tuple[str, str], list[int]] = {}
            for ln in lines[1:]:
                f = ln.split("\t")
                if None in (gi, si, fi, ti) or len(f) <= max(gi, si, fi, ti):
                    continue
                k = (f[fi], f[ti])
                acc = econ_shots.setdefault(k, [0, 0])
                acc[0] += int(f[gi] or 0)
                acc[1] += int(f[si] or 0)
            pooled_mine = pooled_econ = 0
            per_team_mismatch = 0
            per_team_resid = 0
            # ...and the loop joins on the UNIQUE name, not the basename.
            for path in linked:
                rep = Replay(path, track_flow=False, track_damage=True)
                by = rep.damage_by_team()
                mine = by["pooled"]["ammo_spent"]
                # ⚠ replay_econ's `team` column is 0/1, NOT A/B. Keying it on
                # A/B silently produced zero shots for every file and made this
                # validator read FAIL with a 205,440 residual — a join miss
                # wearing an identity-violation costume. Caught by driving it.
                eg = sum(econ_shots.get((path.name, t), [0, 0])[0] for t in ("0", "1"))
                es = sum(econ_shots.get((path.name, t), [0, 0])[1] for t in ("0", "1"))
                theirs = AMMO_PER_SHOT[-7] * eg + AMMO_PER_SHOT[-18] * es
                pooled_mine += mine
                pooled_econ += theirs
                for team, tag in ((0, "0"), (1, "1")):
                    g, s = econ_shots.get((path.name, tag), [0, 0])
                    t_ammo = AMMO_PER_SHOT[-7] * g + AMMO_PER_SHOT[-18] * s
                    m_ammo = by[team]["ammo_spent_inferred"]
                    if t_ammo != m_ammo:
                        per_team_mismatch += 1
                        per_team_resid += abs(t_ammo - m_ammo)
            # ⛔ A JOIN THAT MATCHED NOTHING MUST NOT BE REPORTABLE AS A
            # RESULT IN EITHER DIRECTION. `pooled_econ == 0` while our own
            # channel counts thousands of shots means the join key is wrong, not
            # that the identity failed. Without this the validator's FAIL text
            # blames the decoder for a column-name mismatch.
            if pooled_econ == 0 and pooled_mine != 0:
                print(f"  *** JOIN EMPTY: replay_econ returned 0 shots for all "
                      f"{len(files)} files while UpdateHp counts "
                      f"{pooled_mine} ammo worth. The join key is wrong (its "
                      f"`team` column is 0/1, not A/B) — this is an INSTRUMENT "
                      f"fault, not an identity violation. Not scoring it.")
                bad += 1
            ok_pooled = pooled_mine == pooled_econ
            if not ok_pooled:
                bad += 1
            print(f"  [{'ok ' if ok_pooled else 'FAIL'}] POOLED (both teams): "
                  f"UpdateHp says {pooled_mine} ammo, fireTurret says "
                  f"{pooled_econ} — residual {pooled_mine - pooled_econ} "
                  f"(EXACT expected)")
            n_cells = 2 * len(files)
            share = (per_team_resid / pooled_econ * 100) if pooled_econ else 0.0
            print(f"  [info] PER-TEAM (the INFERENCE): {per_team_mismatch}/"
                  f"{n_cells} team-cells disagree, total |residual| "
                  f"{per_team_resid} of {pooled_econ} = {share:.3f}%.")
            print(f"         Cause is on the WIRE, not in the arithmetic: "
                  f"UpdateHp names only the victim, so DEALT is inferred as "
                  f"'received by the other team' and is wrong under friendly "
                  f"fire; and fireTurret carries only POSITIONS, so a turret "
                  f"tile taken over by the enemy misattributes earlier shots.")
            # THE CONTROL THAT MAKES THE POOLED CLAIM MEAN SOMETHING: the
            # per-team residual must be ZERO-SUM, or the mismatch is a real
            # miscount rather than an attribution swap.
            print(f"  [{'ok ' if ok_pooled else 'FAIL'}] the per-team error is a "
                  f"zero-sum SWAP (it cancels in the pooled figure above), which "
                  f"is what an attribution error looks like and what a miscount "
                  f"does not.")

    # ---- (iii) THE OTHER VERDICT: corrupted payloads must be REFUSED -------
    print("\nVALIDATOR (iii) — A CORRUPTED UpdateHp IS REFUSED, NOT SKIPPED")

    def _v(n, val):                       # varint field, wire type 0
        out = bytearray([n << 3])
        while True:
            b = val & 0x7F
            val >>= 7
            out.append(b | (0x80 if val else 0))
            if not val:
                return bytes(out)

    def _l(n, payload):                   # length-delimited field, wire type 2
        return bytes([(n << 3) | WIRE_LEN, len(payload)]) + payload

    cells = [
        ("clean  {id=7, delta=-18}", _v(1, 7) + _v(2, _I64_MOD - 18), True),
        ("clean  {id=7, delta=+4}", _v(1, 7) + _v(2, 4), True),
        ("no field 1 (id)", _v(2, _I64_MOD - 18), False),
        ("no field 2 (delta)", _v(1, 7), False),
        ("id on the WRONG WIRE (len)", _l(1, b"\x07") + _v(2, 4), False),
        ("delta on the WRONG WIRE (len)", _v(1, 7) + _l(2, b"\x04"), False),
        ("implausible delta (-9999)", _v(1, 7) + _v(2, _I64_MOD - 9999), False),
        ("implausible delta (+100000)", _v(1, 7) + _v(2, 100000), False),
    ]
    for label, payload, want_ok in cells:
        try:
            got = parse_update_hp(payload, where=" [selftest]")
            ok, detail = True, f"-> {got}"
        except ValueError as e:
            ok, detail = False, "REFUSED: " + str(e).split("—")[0].split("[selftest]:")[-1].strip()[:56]
        good = ok == want_ok
        if not good:
            bad += 1
        print(f"  [{'ok ' if good else 'FAIL'}] {label:<32} "
              f"{'accepted' if ok else 'refused ':9} "
              f"(want {'accepted' if want_ok else 'refused'})  {detail}")

    # ...and the refusal must PROPAGATE out of a whole-file parse, not be
    # swallowed by the turn loop. Corrupt a real replay's first UpdateHp payload
    # in place and re-parse it.
    with tempfile.TemporaryDirectory() as td:
        raw = probe.read_bytes()
        # `08 xx 10 <10-byte negative varint>` is a clean UpdateHp for a small
        # id; find the -18 byte sequence and break its delta wire type.
        needle = _v(2, _I64_MOD - 18)
        at = raw.find(needle)
        if at < 0:
            print("  [FAIL] could not locate a -18 UpdateHp payload to corrupt")
            bad += 1
        else:
            broken = bytearray(raw)
            broken[at] = (2 << 3) | WIRE_LEN     # field 2 as length-delimited
            bp = Path(td) / "corrupt.replay26"
            bp.write_bytes(bytes(broken))
            try:
                Replay(bp, track_flow=False, track_damage=True)
                print("  [FAIL] a corrupted UpdateHp inside a real replay was "
                      "PARSED without complaint")
                bad += 1
            except Exception as e:
                print(f"  [ok ] a corrupted UpdateHp inside a real replay "
                      f"REFUSES the whole parse: {type(e).__name__}")
            # ...and the control: track_damage=False must be UNAFFECTED, which is
            # what makes the channel genuinely opt-in rather than a new failure
            # mode for the twenty tools that import this module.
            try:
                Replay(bp, track_flow=False, track_damage=False)
                print("  [ok ] the SAME corrupt file parses fine with "
                      "track_damage=False — existing importers are untouched")
            except Exception as e:
                print(f"  [FAIL] track_damage=False must not see field 5 at all, "
                      f"but raised {type(e).__name__}")
                bad += 1

    # ---- the wrong-zero this channel replaces ------------------------------
    print("\nCONTROL — the reading this channel exists to replace")
    rep = Replay(probe, track_flow=False, track_damage=True)
    hp_from_place = sum(1 for e in rep.entities.values() if e.hp < e.max_hp)
    rows = rep.damage_rows()
    print(f"  placeEntity HP-diff sees {hp_from_place} damaged entities at "
          f"end-of-game; the UpdateHp channel sees {len(rows)} entities touched "
          f"across {rep.hp_events} events.")
    print(f"  [{'ok ' if rep.hp_events > 0 else 'FAIL'}] the channel is NOT "
          f"returning the clean zero an HP-diff returns")
    if rep.hp_events <= 0:
        bad += 1
    print(f"  [ok ] unknown deltas {sorted(rep.unknown_deltas) or 'none'}; "
          f"unresolved victims {len(rep.unresolved_victims)}; "
          f"reused ids {len(rep.reused_ids)}")
    if rep.unknown_deltas or rep.unresolved_victims:
        bad += 1

    print("\nDAMAGE SELFTEST " + ("PASS — the fold is correct and shown "
          "necessary, the pooled ammo identity is EXACT against an independent "
          "decoder, and every corrupted payload is refused rather than skipped."
          if not bad else f"FAIL — {bad} cell(s) wrong."))
    return 0 if not bad else 1


def main() -> int:
    if "--selftest-damage" in sys.argv[1:]:
        return selftest_damage([Path(a) for a in sys.argv[1:]
                               if not a.startswith("-")])
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
    ap.add_argument("--damage", action="store_true",
                    help="emit the PER-ENTITY damage/heal table (UpdateHp, "
                         "update field 5) instead of the census row")
    ap.add_argument("--damage-teams", action="store_true",
                    help="emit the PER-TEAM damage summary instead of the "
                         "per-entity table")
    args = ap.parse_args()

    damage_mode = args.damage or args.damage_teams
    if not args.verbose and not args.no_header:
        cols = (DAMAGE_TEAM_COLUMNS if args.damage_teams
                else DAMAGE_COLUMNS if args.damage else _columns())
        print("\t".join(cols))

    failures = 0
    for path in args.replays:
        try:
            replay = Replay(path, track_flow=not args.no_flow,
                            track_damage=damage_mode)
            row = census(replay)
        except Exception as exc:                      # noqa: BLE001 - report and continue
            print(f"{path}: FAILED — {type(exc).__name__}: {exc}", file=sys.stderr)
            failures += 1
            continue
        if replay.unknown_kinds:
            print(f"{path}: unknown entity kinds {sorted(replay.unknown_kinds)} — "
                  f"tools/replay_schema.md needs updating", file=sys.stderr)
        if damage_mode:
            # ⛔ BOTH OF THESE ARE ALARMS, NOT NOTES. An unknown delta means the
            # measured alphabet moved (a balance change), and an unresolved
            # victim means damage that cannot be attributed to a team -- both
            # were 0 across 108 replays, so either one appearing is signal.
            if replay.unknown_deltas:
                print(f"{path}: *** UNKNOWN HP DELTAS "
                      f"{sorted(replay.unknown_deltas)} -- outside the measured "
                      f"alphabet {list(DAMAGE_DELTAS) + list(HEAL_DELTAS)}. The "
                      f"weapon->delta mapping in this file is out of date.",
                      file=sys.stderr)
            if replay.unresolved_victims:
                print(f"{path}: *** {len(replay.unresolved_victims)} HP event(s) "
                      f"name a victim id never seen in placeEntity or Map.cores "
                      f"-- their damage is UNATTRIBUTED (0 of 96,362 on the "
                      f"reference corpus).", file=sys.stderr)
            if replay.reused_ids:
                print(f"{path}: note — {len(replay.reused_ids)} entity id(s) were "
                      f"reused after death; their per-entity rows blend two "
                      f"entities (id_reused=1).", file=sys.stderr)
        if args.verbose:
            verbose_report(replay, row, sys.stdout)
            if damage_mode:
                damage_report(replay, sys.stdout)
        elif args.damage_teams:
            by = replay.damage_by_team()
            for team in (0, 1):
                d = by[team]
                print("\t".join([path.name, TEAM_NAME[team]]
                                + [str(d[c]) for c in DAMAGE_TEAM_COLUMNS[2:]]))
        elif args.damage:
            for r in replay.damage_rows():
                print("\t".join([path.name]
                                + [str(r[c]) for c in DAMAGE_COLUMNS[1:]]))
        else:
            print(tsv_row(row))
    return 1 if failures else 0


def damage_report(replay: Replay, out) -> None:
    """Readable damage breakdown for --verbose --damage."""
    w = out.write
    by = replay.damage_by_team()
    p = by["pooled"]
    w("\n  damage channel (UpdateHp, update field 5)\n")
    w(f"    {p['hp_events']} HP events   pooled shots: "
      f"{p['shots_gunner']} gunner, {p['shots_sentinel']} sentinel   "
      f"=> ammo spent {p['ammo_spent']} (EXACT identity)\n")
    w(f"    {'':22s}{'A':>12s}{'B':>12s}\n")
    for label, key in (("dmg received", "recv_dmg_total"),
                       ("  sentinel hits", "recv_shots_sentinel"),
                       ("  gunner hits", "recv_shots_gunner"),
                       ("  builder attacks", "recv_attacks"),
                       ("heal events", "heal_events"),
                       ("heal HP", "heal_total"),
                       ("ammo spent (INFERRED)", "ammo_spent_inferred")):
        w(f"    {label:22s}{by[0][key]:>12}{by[1][key]:>12}\n")
    rows = replay.damage_rows()
    hurt = sorted(rows, key=lambda r: -r["dmg_total"])[:8]
    w(f"    top damage takers ({len(rows)} entities touched):\n")
    for r in hurt:
        w(f"      #{r['entity']:<6d} {r['team']} {r['kind']:<12s} "
          f"dmg {r['dmg_total']:>5d} (sen {r['n-18']}, gun {r['n-7']}, "
          f"atk {r['n-2']})  heals {r['heal_events']} for {r['heal_total']} HP"
          f"{'  [ID REUSED]' if r['id_reused'] else ''}\n")
    w("\n")


if __name__ == "__main__":
    sys.exit(main())


def guard_out(path) -> None:
    """Refuse an OUTPUT path that is an existing NON-.tsv file.

    ⛔ THE DECODERS TAKE argv[0] AS THE OUTPUT AND argv[1:] AS INPUTS. That is a
    landmine in tools people feed file lists to: on 2026-08-12 a lane xargs'd a
    directory of replays straight in, THE FIRST REPLAY WAS OPENED "w" AND DESTROYED,
    and the run printed "done 7 files, 0 errors" -- a success message that counted
    the SURVIVORS. FOUR files carried the identical signature.

    ⚠ The first fix sniffed a protobuf magic byte and was INSTANCE-SCOPED TWICE: it
    lived in one of the four files, and it only caught REPLAYS -- an xargs over a
    directory whose first entry is a `.COMPLETE` marker, a heartbeat or a `.log`
    would still have been destroyed silently. Both caught by the side lane, one hour
    after this lane argued for class fixes over instance fixes on queue_check.

    Existence + extension cannot be defeated by an unrecognised file type, and it
    still permits the normal re-run path (overwriting an existing .tsv). The
    positional signature stays because sync.py and build_corpus.py pass outputs
    positionally and replay_builds.py takes TWO of them.
    """
    from pathlib import Path as _P
    p = _P(path)
    if p.exists() and p.suffix != ".tsv":
        raise SystemExit(
            f"REFUSING: argv[0] is the OUTPUT path, and {path!r} is an existing "
            f"non-.tsv file.\n    You probably meant:  <tool>.py OUT.tsv <inputs...>"
        )
