#!/usr/bin/env python3
"""A minimal FAKE ENGINE implementing the Florent Code League Controller API
over a small grid, so bot code can be unit-driven without a real match.

Pure Python 3, stdlib only. Does NOT import the real `fcode` package -- the
enums/types below are local shims matching the contract in CLAUDE.md ("Core
game rules", "Entities", "Controller API reference", "Key types and
constants"), cross-checked against the installed package's type stub
(site-packages/fcode/_types.py) for field names and constants.

One deliberate divergence from that stub, load-bearing for the self-test
below: CLAUDE.md says the Sentinel "ignores obstacles (unlike Gunner)", and
"gunner line is prefix-blocked, sentinel is not" is treated as a real engine
control pair. This stub implements exactly that: get_attackable_tiles_from
stops the GUNNER line at (and including) the first occupied tile; the
SENTINEL line is never blocked. If this ever needs to match the shipped .so
bit-for-bit, re-verify against
docs/research/engine-source-crash-and-launcher-2026-08-10.md.

⛔ DO NOT "FIX" is_in_vision BY ADDING A BOUNDS CHECK. It is deliberately a
PURE RADIUS TEST with no bounds check, matching the engine: an OFF-MAP
position INSIDE the vision radius returns True, and the next get_tile_* on
that same position RAISES. That True-then-raise trap is a live hazard near map
borders and the stub exists to reproduce it, not to soften it. Ground truth:
CLAUDE.md:367-377 (CORRECTED s50, 2026-08-17) and
docs/research/PROBE-DOSSIER-ferry-siege-2026-08-17.md:186-196 (probed on atoll,
core at 2,14: is_in_vision((-1,14)) == True). The self-test drives all four
cells (off-map in/out of radius, in-map in/out of radius).

Usage:
    from tools.stub_engine import World, StubController, run_bot
    w = World(10, 10)
    core_a = w.add(EntityType.CORE, Team.A, Position(1, 1))
    ...

Self-test: .venv/bin/python tools/stub_engine.py
"""
from __future__ import annotations

import math
from enum import Enum
from typing import NamedTuple, Optional

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


# ---------------------------------------------------------------------------
# Local enum/type shims (no `fcode` import)
# ---------------------------------------------------------------------------

class GameError(Exception):
    """Raised when a player issues an invalid action."""


class Team:
    A = "A"
    B = "B"


class ResourceType:
    TITANIUM = "titanium"


class EntityType:
    BUILDER_BOT = "builder_bot"
    CORE = "core"
    GUNNER = "gunner"
    SENTINEL = "sentinel"
    LAUNCHER = "launcher"
    CONVEYOR = "conveyor"
    SPLITTER = "splitter"
    HARVESTER = "harvester"
    BARRIER = "barrier"


class Environment:
    EMPTY = "empty"
    WALL = "wall"
    ORE_TITANIUM = "ore_titanium"


class GameConstants:
    (MAX_TURNS, STACK_SIZE, STARTING_TITANIUM, MAX_TEAM_UNITS,
     PASSIVE_TITANIUM_AMOUNT, PASSIVE_TITANIUM_INTERVAL, STORE_SIZE,
     CORE_ACTION_RADIUS_SQ) = (1000, 10, 500, 50, 10, 4, 16, 8)

    # vision radius^2, by entity type
    (CORE_VISION_RADIUS_SQ, BUILDER_BOT_VISION_RADIUS_SQ,
     GUNNER_VISION_RADIUS_SQ, SENTINEL_VISION_RADIUS_SQ,
     LAUNCHER_VISION_RADIUS_SQ) = (36, 20, 13, 32, 26)

    # base build cost (Ti), by entity type, plus gunner rotate cost
    (CONVEYOR_BASE_COST, SPLITTER_BASE_COST, HARVESTER_BASE_COST,
     BARRIER_BASE_COST, GUNNER_BASE_COST, SENTINEL_BASE_COST,
     LAUNCHER_BASE_COST, BUILDER_BOT_BASE_COST, GUNNER_ROTATE_COST) = (
        3, 6, 20, 3, 20, 30, 20, 30, 10)

    # max HP, by entity type
    (CORE_MAX_HP, BUILDER_BOT_MAX_HP, CONVEYOR_MAX_HP, SPLITTER_MAX_HP,
     HARVESTER_MAX_HP, BARRIER_MAX_HP, GUNNER_MAX_HP, SENTINEL_MAX_HP,
     LAUNCHER_MAX_HP) = (500, 40, 20, 20, 30, 30, 25, 40, 30)

    BUILDER_BOT_ATTACK_DAMAGE = 2
    BUILDER_BOT_ATTACK_COST = 2
    BUILDER_BOT_HEAL_COST = 1
    HEAL_AMOUNT = 4

    GUNNER_DAMAGE, GUNNER_FIRE_COOLDOWN, GUNNER_AMMO_COST = 7, 1, 4
    SENTINEL_DAMAGE, SENTINEL_FIRE_COOLDOWN, SENTINEL_AMMO_COST = 18, 2, 10


_DELTA = {
    "NORTH": (0, -1),
    "NORTHEAST": (1, -1),
    "EAST": (1, 0),
    "SOUTHEAST": (1, 1),
    "SOUTH": (0, 1),
    "SOUTHWEST": (-1, 1),
    "WEST": (-1, 0),
    "NORTHWEST": (-1, -1),
    "CENTRE": (0, 0),
}
_LEFT = {
    "NORTH": "NORTHWEST", "NORTHWEST": "WEST", "WEST": "SOUTHWEST",
    "SOUTHWEST": "SOUTH", "SOUTH": "SOUTHEAST", "SOUTHEAST": "EAST",
    "EAST": "NORTHEAST", "NORTHEAST": "NORTH", "CENTRE": "CENTRE",
}
_RIGHT = {v: k for k, v in _LEFT.items()}
_OPPOSITE = {
    "NORTH": "SOUTH", "SOUTH": "NORTH", "EAST": "WEST", "WEST": "EAST",
    "NORTHEAST": "SOUTHWEST", "SOUTHWEST": "NORTHEAST",
    "NORTHWEST": "SOUTHEAST", "SOUTHEAST": "NORTHWEST", "CENTRE": "CENTRE",
}
_CARDINALS = {"NORTH", "EAST", "SOUTH", "WEST"}


class Direction(Enum):
    """A compass direction on the map grid. (0,0) is the map's NW corner: x
    grows EAST, y grows SOUTH, so NORTH is (0,-1). A real stdlib Enum (not a
    hand-rolled shim) so `for d in Direction:`, equality, and hashing all
    work exactly as bot code expects."""

    NORTH = "north"
    NORTHEAST = "northeast"
    EAST = "east"
    SOUTHEAST = "southeast"
    SOUTH = "south"
    SOUTHWEST = "southwest"
    WEST = "west"
    NORTHWEST = "northwest"
    CENTRE = "centre"

    def delta(self) -> tuple:
        return _DELTA[self.name]

    def rotate_left(self) -> "Direction":
        return Direction[_LEFT[self.name]]

    def rotate_right(self) -> "Direction":
        return Direction[_RIGHT[self.name]]

    def opposite(self) -> "Direction":
        return Direction[_OPPOSITE[self.name]]

    def is_cardinal(self) -> bool:
        return self.name in _CARDINALS


_COMPASS_ORDER = [
    Direction.EAST, Direction.NORTHEAST, Direction.NORTH, Direction.NORTHWEST,
    Direction.WEST, Direction.SOUTHWEST, Direction.SOUTH, Direction.SOUTHEAST,
]


class Position(NamedTuple):
    x: int
    y: int

    def add(self, d: "Direction") -> "Position":
        dx, dy = d.delta()
        return Position(self.x + dx, self.y + dy)

    def distance_squared(self, other: "Position") -> int:
        dx = self.x - other.x
        dy = self.y - other.y
        return dx * dx + dy * dy

    def direction_to(self, other: "Position") -> "Direction":
        dx = other.x - self.x
        dy = other.y - self.y
        if dx == 0 and dy == 0:
            return Direction.CENTRE
        angle = math.atan2(-dy, dx)
        sector = int((angle + 2 * math.pi + math.pi / 8) / (math.pi / 4)) % 8
        return _COMPASS_ORDER[sector]

    def cardinal_direction_to(self, other: "Position") -> "Direction":
        dx = other.x - self.x
        dy = other.y - self.y
        if dx == 0 and dy == 0:
            return Direction.CENTRE
        if abs(dx) >= abs(dy):
            return Direction.EAST if dx > 0 else Direction.WEST
        return Direction.SOUTH if dy > 0 else Direction.NORTH


# ---------------------------------------------------------------------------
# World
# ---------------------------------------------------------------------------

_GC = GameConstants
_BASE_COST = {
    EntityType.CONVEYOR: _GC.CONVEYOR_BASE_COST, EntityType.SPLITTER: _GC.SPLITTER_BASE_COST,
    EntityType.HARVESTER: _GC.HARVESTER_BASE_COST, EntityType.BARRIER: _GC.BARRIER_BASE_COST,
    EntityType.GUNNER: _GC.GUNNER_BASE_COST, EntityType.SENTINEL: _GC.SENTINEL_BASE_COST,
    EntityType.LAUNCHER: _GC.LAUNCHER_BASE_COST, EntityType.BUILDER_BOT: _GC.BUILDER_BOT_BASE_COST,
}
# scale-factor contribution per build: conveyor/splitter/barrier +1,
# harvester +5, launcher +10, builder_bot/gunner/sentinel +20 (additive, team-global)
_SCALE_CONTRIB = {
    EntityType.CONVEYOR: 1.0, EntityType.SPLITTER: 1.0, EntityType.BARRIER: 1.0,
    EntityType.HARVESTER: 5.0, EntityType.LAUNCHER: 10.0,
    EntityType.BUILDER_BOT: 20.0, EntityType.GUNNER: 20.0, EntityType.SENTINEL: 20.0,
}
_MAX_HP = {
    EntityType.CORE: _GC.CORE_MAX_HP, EntityType.BUILDER_BOT: _GC.BUILDER_BOT_MAX_HP,
    EntityType.CONVEYOR: _GC.CONVEYOR_MAX_HP, EntityType.SPLITTER: _GC.SPLITTER_MAX_HP,
    EntityType.HARVESTER: _GC.HARVESTER_MAX_HP, EntityType.BARRIER: _GC.BARRIER_MAX_HP,
    EntityType.GUNNER: _GC.GUNNER_MAX_HP, EntityType.SENTINEL: _GC.SENTINEL_MAX_HP,
    EntityType.LAUNCHER: _GC.LAUNCHER_MAX_HP,
}
_VISION_SQ = {
    EntityType.CORE: _GC.CORE_VISION_RADIUS_SQ, EntityType.BUILDER_BOT: _GC.BUILDER_BOT_VISION_RADIUS_SQ,
    EntityType.GUNNER: _GC.GUNNER_VISION_RADIUS_SQ, EntityType.SENTINEL: _GC.SENTINEL_VISION_RADIUS_SQ,
    EntityType.LAUNCHER: _GC.LAUNCHER_VISION_RADIUS_SQ,
    EntityType.CONVEYOR: 0, EntityType.SPLITTER: 0, EntityType.HARVESTER: 0, EntityType.BARRIER: 0,
}
_ATTACK_SQ = {EntityType.GUNNER: _GC.GUNNER_VISION_RADIUS_SQ, EntityType.SENTINEL: _GC.SENTINEL_VISION_RADIUS_SQ}
_UNIT_TYPES = {EntityType.CORE, EntityType.BUILDER_BOT, EntityType.GUNNER,
               EntityType.SENTINEL, EntityType.LAUNCHER}
_BUILDING_TYPES = {EntityType.CORE, EntityType.GUNNER, EntityType.SENTINEL, EntityType.LAUNCHER,
                   EntityType.CONVEYOR, EntityType.SPLITTER, EntityType.HARVESTER, EntityType.BARRIER}
_DIRECTIONAL_BUILD = {EntityType.CONVEYOR, EntityType.SPLITTER, EntityType.GUNNER, EntityType.SENTINEL}


class World:
    """Holds the whole fake match state: terrain, entities, per-team economy,
    the comms store (with buffered writes), and the round counter."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.terrain = {
            Position(x, y): Environment.EMPTY
            for x in range(width) for y in range(height)
        }
        self.entities: dict = {}  # id -> dict(type, team, pos, hp, direction)
        self._next_id = 1
        self.titanium = {Team.A: GameConstants.STARTING_TITANIUM,
                          Team.B: GameConstants.STARTING_TITANIUM}
        self.ammo = {Team.A: 0, Team.B: 0}
        self.scale_pct = {Team.A: 100.0, Team.B: 100.0}
        self.store = {Team.A: [0] * GameConstants.STORE_SIZE,
                       Team.B: [0] * GameConstants.STORE_SIZE}
        self._store_pending = {Team.A: {}, Team.B: {}}
        self.round = 0
        self.cpu_us = 0
        self._ammo_converted_this_round = {Team.A: False, Team.B: False}

    # -- terrain --

    def in_bounds(self, pos: Position) -> bool:
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height

    def set_terrain(self, pos: Position, env: str) -> None:
        if not self.in_bounds(pos):
            raise GameError(f"set_terrain off-map: {pos}")
        self.terrain[pos] = env

    def get_terrain(self, pos: Position) -> str:
        if not self.in_bounds(pos):
            raise GameError(f"off-map: {pos}")
        return self.terrain[pos]

    # -- entities --

    def add(self, entity_type: str, team, pos: Position, direction=None) -> int:
        eid = self._next_id
        self._next_id += 1
        self.entities[eid] = {
            "type": entity_type,
            "team": team,
            "pos": pos,
            "hp": _MAX_HP.get(entity_type, 1),
            "direction": direction,
            "action_cd": 0,
            "move_cd": 0,
        }
        contrib = _SCALE_CONTRIB.get(entity_type)
        if contrib is not None:
            self.scale_pct[team] += contrib
        return eid

    def remove(self, eid: int) -> None:
        ent = self.entities.pop(eid, None)
        if ent is None:
            return
        contrib = _SCALE_CONTRIB.get(ent["type"])
        if contrib is not None:
            self.scale_pct[ent["team"]] -= contrib

    def cost(self, entity_type: str, team) -> int:
        base = _BASE_COST[entity_type]
        return int((self.scale_pct[team] / 100.0) * base)

    def building_at(self, pos: Position) -> Optional[int]:
        return next((eid for eid, ent in self.entities.items()
                     if ent["pos"] == pos and ent["type"] in _BUILDING_TYPES), None)

    def builder_bot_at(self, pos: Position) -> Optional[int]:
        return next((eid for eid, ent in self.entities.items()
                     if ent["pos"] == pos and ent["type"] == EntityType.BUILDER_BOT), None)

    def any_entity_at(self, pos: Position) -> Optional[int]:
        return next((eid for eid, ent in self.entities.items() if ent["pos"] == pos), None)

    # -- round lifecycle --

    def end_round(self) -> None:
        for team in (Team.A, Team.B):
            for idx, val in self._store_pending[team].items():
                self.store[team][idx] = val & 0xFFFFFFFF
            self._store_pending[team] = {}
        for ent in self.entities.values():
            if ent["action_cd"] > 0:
                ent["action_cd"] -= 1
            if ent["move_cd"] > 0:
                ent["move_cd"] -= 1
        self.round += 1
        if self.round % GameConstants.PASSIVE_TITANIUM_INTERVAL == 0:
            for team in (Team.A, Team.B):
                self.titanium[team] += GameConstants.PASSIVE_TITANIUM_AMOUNT
        self._ammo_converted_this_round = {Team.A: False, Team.B: False}
        self.cpu_us = 0


# ---------------------------------------------------------------------------
# StubController
# ---------------------------------------------------------------------------

class StubController:
    """Unit-scoped fake Controller. Mirrors the real Controller's method set
    (see CLAUDE.md "Controller API reference")."""

    def __init__(self, world: World, entity_id: int):
        self.world = world
        self._id = entity_id

    # -- internal helpers --

    def _ent(self, eid: Optional[int] = None) -> dict:
        eid = self._id if eid is None else eid
        ent = self.world.entities.get(eid)
        if ent is None:
            raise GameError(f"no such entity: {eid}")
        return ent

    def _self(self) -> dict:
        return self._ent(self._id)

    def _is_orth_adjacent(self, pos: Position) -> bool:
        me = self._self()["pos"]
        return me.distance_squared(pos) == 1

    def _vision_sq(self, eid: Optional[int] = None) -> int:
        ent = self._ent(eid)
        return _VISION_SQ.get(ent["type"], 0)

    # -- info / queries --

    def get_team(self, id: Optional[int] = None): return self._ent(id)["team"]
    def get_position(self, id: Optional[int] = None) -> Position: return self._ent(id)["pos"]
    def get_id(self) -> int: return self._id
    def get_action_cooldown(self) -> int: return self._self()["action_cd"]
    def get_move_cooldown(self) -> int: return self._self()["move_cd"]
    def can_act(self) -> bool: return self._self()["action_cd"] == 0
    def get_vision_radius_sq(self, id: Optional[int] = None) -> int: return self._vision_sq(id)
    def get_hp(self, id: Optional[int] = None) -> int: return self._ent(id)["hp"]
    def get_max_hp(self, id: Optional[int] = None) -> int: return _MAX_HP.get(self._ent(id)["type"], 1)
    def get_entity_type(self, id: Optional[int] = None): return self._ent(id)["type"]

    def get_direction(self, id: Optional[int] = None):
        d = self._ent(id)["direction"]
        if d is None:
            raise GameError("entity has no direction")
        return d

    def get_stored_resource(self, id: Optional[int] = None):
        ent = self._ent(id)
        if ent["type"] not in (EntityType.CONVEYOR, EntityType.SPLITTER):
            raise GameError("entity has no storage")
        return None

    def get_stored_resource_id(self, id: Optional[int] = None):
        ent = self._ent(id)
        if ent["type"] not in (EntityType.CONVEYOR, EntityType.SPLITTER):
            raise GameError("entity has no storage")
        return None

    def get_tile_env(self, pos: Position):
        # LOAD-BEARING: raises off-map, while is_in_vision does NOT (it is a
        # pure radius test). See CLAUDE.md:367-377 and
        # docs/research/PROBE-DOSSIER-ferry-siege-2026-08-17.md:186-196.
        return self.world.get_terrain(pos)

    def get_tile_building_id(self, pos: Position) -> Optional[int]:
        if not self.world.in_bounds(pos):
            raise GameError(f"off-map: {pos}")
        return self.world.building_at(pos)

    def get_tile_builder_bot_id(self, pos: Position) -> Optional[int]:
        if not self.world.in_bounds(pos):
            raise GameError(f"off-map: {pos}")
        return self.world.builder_bot_at(pos)

    def is_tile_empty(self, pos: Position) -> bool:
        if not self.world.in_bounds(pos):
            return False
        if self.world.terrain[pos] == Environment.WALL:
            return False
        return self.world.building_at(pos) is None

    def is_tile_passable(self, pos: Position) -> bool:
        if not self.world.in_bounds(pos):
            return False
        if self.world.terrain[pos] == Environment.WALL:
            return False
        if self.world.building_at(pos) is not None:
            return False
        if self.world.builder_bot_at(pos) is not None:
            return False
        return True

    def is_in_vision(self, pos: Position) -> bool:
        # LOAD-BEARING: the real engine's is_in_vision is a PURE RADIUS TEST with
        # NO BOUNDS CHECK. It never raises, but an OFF-MAP position inside the
        # vision radius returns True -- and the next get_tile_* on that same
        # position raises GameError. That "True-then-raise" trap is why the stub
        # must NOT bounds-check here: a bounds check would make the stub kinder
        # than the engine and hide border bugs.
        # Ground truth: CLAUDE.md:367-377 (CORRECTED s50, 2026-08-17) and
        # docs/research/PROBE-DOSSIER-ferry-siege-2026-08-17.md:186-196 --
        # probed on atoll (core at 2,14): is_in_vision((-1,14)) == True.
        me = self._self()["pos"]
        return pos.distance_squared(me) <= self._vision_sq()

    def get_nearby_tiles(self, dist_sq: Optional[int] = None) -> list:
        if dist_sq is None:
            dist_sq = self._vision_sq()
        me = self._self()["pos"]
        out = []
        r = int(math.isqrt(dist_sq)) + 1
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                if dx * dx + dy * dy > dist_sq:
                    continue
                p = Position(me.x + dx, me.y + dy)
                if self.world.in_bounds(p):
                    out.append(p)
        return out

    def _nearby(self, dist_sq: Optional[int], pred) -> list:
        if dist_sq is None:
            dist_sq = self._vision_sq()
        me = self._self()["pos"]
        return [eid for eid, ent in self.world.entities.items()
                if pred(ent) and ent["pos"].distance_squared(me) <= dist_sq]

    def get_nearby_entities(self, dist_sq: Optional[int] = None) -> list: return self._nearby(dist_sq, lambda e: True)
    def get_nearby_buildings(self, dist_sq: Optional[int] = None) -> list: return self._nearby(dist_sq, lambda e: e["type"] in _BUILDING_TYPES)
    def get_nearby_units(self, dist_sq: Optional[int] = None) -> list: return self._nearby(dist_sq, lambda e: e["type"] in _UNIT_TYPES)

    def get_map_width(self) -> int: return self.world.width
    def get_map_height(self) -> int: return self.world.height
    def get_current_round(self) -> int: return self.world.round
    def get_global_resources(self) -> int: return self.world.titanium[self._self()["team"]]
    def get_global_ammo(self) -> int: return self.world.ammo[self._self()["team"]]
    def get_scale_percent(self) -> float: return self.world.scale_pct[self._self()["team"]]
    def get_cpu_time_elapsed(self) -> int: return self.world.cpu_us

    def get_unit_count(self) -> int:
        team = self._self()["team"]
        return sum(1 for ent in self.world.entities.values()
                   if ent["team"] == team and ent["type"] in _UNIT_TYPES)

    # -- cost getters --

    def _cost(self, entity_type: str) -> int:
        return self.world.cost(entity_type, self._self()["team"])

    def get_conveyor_cost(self) -> int: return self._cost(EntityType.CONVEYOR)
    def get_splitter_cost(self) -> int: return self._cost(EntityType.SPLITTER)
    def get_harvester_cost(self) -> int: return self._cost(EntityType.HARVESTER)
    def get_barrier_cost(self) -> int: return self._cost(EntityType.BARRIER)
    def get_gunner_cost(self) -> int: return self._cost(EntityType.GUNNER)
    def get_sentinel_cost(self) -> int: return self._cost(EntityType.SENTINEL)
    def get_launcher_cost(self) -> int: return self._cost(EntityType.LAUNCHER)
    def get_builder_bot_cost(self) -> int: return self._cost(EntityType.BUILDER_BOT)

    # -- movement --

    def can_move(self, direction: "Direction") -> bool:
        me = self._self()
        return (me["type"] == EntityType.BUILDER_BOT and direction.is_cardinal()
                and me["move_cd"] == 0 and self.is_tile_passable(me["pos"].add(direction)))

    def move(self, direction: "Direction") -> None:
        if not self.can_move(direction):
            raise GameError("illegal move")
        me = self._self()
        me["pos"] = me["pos"].add(direction)
        me["move_cd"] = 1

    # -- building --

    def _can_build_common(self, position: Position) -> bool:
        me = self._self()
        return (me["type"] == EntityType.BUILDER_BOT and me["action_cd"] == 0
                and self._is_orth_adjacent(position) and self.world.in_bounds(position))

    def can_build(self, entity_type: str, position: Position, extra=None) -> bool:
        if not self._can_build_common(position):
            return False
        if self.world.builder_bot_at(position) is not None:
            return False
        env = self.world.terrain[position]
        if entity_type == EntityType.HARVESTER:
            if env != Environment.ORE_TITANIUM:
                return False
        else:
            if env == Environment.WALL:
                return False
        if self.world.building_at(position) is not None:
            return False
        if entity_type in (EntityType.GUNNER, EntityType.SENTINEL,
                            EntityType.LAUNCHER, EntityType.BUILDER_BOT):
            team = self._self()["team"]
            count = sum(1 for ent in self.world.entities.values()
                        if ent["team"] == team and ent["type"] in _UNIT_TYPES)
            if count >= GameConstants.MAX_TEAM_UNITS:
                return False
        if entity_type in _DIRECTIONAL_BUILD and extra is None:
            return False
        cost = self.world.cost(entity_type, self._self()["team"])
        return self.world.titanium[self._self()["team"]] >= cost

    def build(self, entity_type: str, position: Position, extra=None) -> int:
        if not self.can_build(entity_type, position, extra):
            raise GameError(f"illegal build: {entity_type} at {position}")
        team = self._self()["team"]
        cost = self.world.cost(entity_type, team)
        self.world.titanium[team] -= cost
        direction = extra if entity_type in _DIRECTIONAL_BUILD else None
        eid = self.world.add(entity_type, team, position, direction)
        self._self()["action_cd"] = 1
        return eid

    def can_build_conveyor(self, position: Position, direction=None) -> bool: return self.can_build(EntityType.CONVEYOR, position, direction)
    def can_build_splitter(self, position: Position, direction=None) -> bool: return self.can_build(EntityType.SPLITTER, position, direction)
    def can_build_harvester(self, position: Position) -> bool: return self.can_build(EntityType.HARVESTER, position)
    def can_build_barrier(self, position: Position) -> bool: return self.can_build(EntityType.BARRIER, position)
    def can_build_gunner(self, position: Position, direction=None) -> bool: return self.can_build(EntityType.GUNNER, position, direction)
    def can_build_sentinel(self, position: Position, direction=None) -> bool: return self.can_build(EntityType.SENTINEL, position, direction)
    def can_build_launcher(self, position: Position) -> bool: return self.can_build(EntityType.LAUNCHER, position)
    def build_conveyor(self, position: Position, direction) -> int: return self.build(EntityType.CONVEYOR, position, direction)
    def build_splitter(self, position: Position, direction) -> int: return self.build(EntityType.SPLITTER, position, direction)
    def build_harvester(self, position: Position) -> int: return self.build(EntityType.HARVESTER, position)
    def build_barrier(self, position: Position) -> int: return self.build(EntityType.BARRIER, position)
    def build_gunner(self, position: Position, direction) -> int: return self.build(EntityType.GUNNER, position, direction)
    def build_sentinel(self, position: Position, direction) -> int: return self.build(EntityType.SENTINEL, position, direction)
    def build_launcher(self, position: Position) -> int: return self.build(EntityType.LAUNCHER, position)

    # -- healing / destruction --

    def can_heal(self, position: Position) -> bool:
        me = self._self()
        if not (me["type"] == EntityType.BUILDER_BOT and me["action_cd"] == 0
                and self._is_orth_adjacent(position) and self.world.in_bounds(position)
                and self.world.titanium[me["team"]] >= GameConstants.BUILDER_BOT_HEAL_COST):
            return False
        return any(ent["pos"] == position and ent["team"] == me["team"]
                   and ent["hp"] < _MAX_HP.get(ent["type"], ent["hp"])
                   for ent in self.world.entities.values())

    def heal(self, position: Position) -> None:
        if not self.can_heal(position):
            raise GameError("illegal heal")
        me = self._self()
        self.world.titanium[me["team"]] -= GameConstants.BUILDER_BOT_HEAL_COST
        for ent in self.world.entities.values():
            if ent["pos"] == position and ent["team"] == me["team"]:
                cap = _MAX_HP.get(ent["type"], ent["hp"])
                ent["hp"] = min(cap, ent["hp"] + GameConstants.HEAL_AMOUNT)
        me["action_cd"] = 1

    def can_destroy(self, building_pos: Position) -> bool:
        me = self._self()
        if not (me["type"] == EntityType.BUILDER_BOT and self._is_orth_adjacent(building_pos)
                and self.world.in_bounds(building_pos)):
            return False
        bid = self.world.building_at(building_pos)
        return bid is not None and self.world.entities[bid]["team"] == me["team"]

    def destroy(self, building_pos: Position) -> None:
        if not self.can_destroy(building_pos):
            raise GameError("illegal destroy")
        # FREE: no titanium cost, no cooldown set, unlimited per turn.
        bid = self.world.building_at(building_pos)
        self.world.remove(bid)

    def self_destruct(self) -> None:
        self.world.remove(self._id)

    def resign(self, message: Optional[str] = None) -> None:
        team = self._self()["team"]
        for eid, ent in list(self.world.entities.items()):
            if ent["team"] == team and ent["type"] == EntityType.CORE:
                self.world.remove(eid)

    # -- communication store --

    def read_store(self, index: int) -> int:
        team = self._self()["team"]
        if not 0 <= index < GameConstants.STORE_SIZE:
            raise GameError("store index out of range")
        return self.world.store[team][index]

    def write_store(self, index: int, value: int) -> None:
        team = self._self()["team"]
        if not 0 <= index < GameConstants.STORE_SIZE:
            raise GameError("store index out of range")
        self.world._store_pending[team][index] = value

    # -- turrets --

    def _turret_attack_sq(self, entity_type) -> int:
        return _ATTACK_SQ.get(entity_type, 0)

    def get_attackable_tiles(self) -> list:
        me = self._self()
        return self.get_attackable_tiles_from(me["pos"], me["direction"], me["type"])

    def get_attackable_tiles_from(self, position: Position, direction, turret_type) -> list:
        if turret_type not in (EntityType.GUNNER, EntityType.SENTINEL):
            raise GameError("not a turret type")
        attack_sq = self._turret_attack_sq(turret_type)
        dx, dy = direction.delta()
        out = []
        x, y = position.x, position.y
        while True:
            x += dx
            y += dy
            p = Position(x, y)
            if not self.world.in_bounds(p):
                break
            if p.distance_squared(position) > attack_sq:
                break
            out.append(p)
            # ⛔ CORRECTED 2026-08-15 AGAINST THE ENGINE.  This used to stop the
            # GUNNER line at the first body, on the reading that "straight-line
            # shot" meant the TILES LIST was prefix-blocked.  It is not.  The
            # installed API says get_attackable_tiles "includes the full firing
            # line within range, even behind walls", and `bots/_probe_rayempty`
            # re-run on the real engine agrees: a gunner at (6,2) with a
            # BUILDING at (7,2) still reports in_pattern=True for (8,2) and
            # (9,2) behind it -- 3 tiles, the whole r^2<=13 line.
            # The blocking is real but it lives in can_fire/can_fire_from, not
            # here.  Keeping it here made the raw pattern useless as an
            # occupancy-independent geometry query, which is exactly what
            # RaidMixin._friendly_gun_ray needs it for.
        return out

    def can_fire(self, target: Position) -> bool:
        me = self._self()
        if me["type"] == EntityType.BUILDER_BOT:
            return (me["action_cd"] == 0 and self._is_orth_adjacent(target)
                    and self.world.in_bounds(target) and self.world.building_at(target) is not None)
        if me["type"] not in (EntityType.GUNNER, EntityType.SENTINEL) or me["action_cd"] != 0:
            return False
        # ASYMMETRY, load-bearing: True even at 0 ammo. fire() raises.
        return self._ray_reaches(me["pos"], me["direction"], me["type"], target)

    def can_fire_from(self, position: Position, direction, turret_type, target: Position) -> bool:
        return self._ray_reaches(position, direction, turret_type, target)

    def _ray_reaches(self, position: Position, direction, turret_type, target: Position) -> bool:
        """The blocking rule, measured on the engine by `bots/_probe_rayempty`.

        GUNNER: the target must be OCCUPIED and must be the FIRST occupied tile
        on the line.  Every EMPTY tile answers False -- 5 gunners in the probe,
        every empty step False, True only where a body stood.  (An earlier read
        put this blocking in get_attackable_tiles instead; it is not there, the
        raw pattern is the full line.)
        SENTINEL: any tile on the line answers True, empty or not -- the probe's
        control, which is what makes the gunner result meaningful.
        """
        line = self.get_attackable_tiles_from(position, direction, turret_type)
        if target not in line:
            return False
        if turret_type != EntityType.GUNNER:
            return True
        for t in line:
            occupied = self.world.any_entity_at(t) is not None
            if t == target:
                return occupied
            if occupied:
                return False
        return False

    def fire(self, target: Position) -> None:
        me = self._self()
        if me["type"] == EntityType.BUILDER_BOT:
            if not self.can_fire(target):
                raise GameError("illegal fire")
            bid = self.world.building_at(target)
            self.world.titanium[me["team"]] -= GameConstants.BUILDER_BOT_ATTACK_COST
            self.world.entities[bid]["hp"] -= GameConstants.BUILDER_BOT_ATTACK_DAMAGE
            if self.world.entities[bid]["hp"] <= 0:
                self.world.remove(bid)
            me["action_cd"] = 1
            return
        if not self.can_fire(target):
            raise GameError("illegal fire")
        team = me["team"]
        if me["type"] == EntityType.GUNNER:
            ammo_cost, dmg, cd = (GameConstants.GUNNER_AMMO_COST,
                                   GameConstants.GUNNER_DAMAGE,
                                   GameConstants.GUNNER_FIRE_COOLDOWN)
        else:
            ammo_cost, dmg, cd = (GameConstants.SENTINEL_AMMO_COST,
                                   GameConstants.SENTINEL_DAMAGE,
                                   GameConstants.SENTINEL_FIRE_COOLDOWN)
        if self.world.ammo[team] < ammo_cost:
            raise GameError("insufficient ammo")
        self.world.ammo[team] -= ammo_cost
        tid = self.world.any_entity_at(target)
        if tid is not None:
            self.world.entities[tid]["hp"] -= dmg
            if self.world.entities[tid]["hp"] <= 0:
                self.world.remove(tid)
        me["action_cd"] = cd

    def can_rotate(self, direction) -> bool:
        me = self._self()
        if me["type"] != EntityType.GUNNER:
            raise GameError("rotate is gunner-only")
        if me["action_cd"] != 0:
            return False
        return self.world.titanium[me["team"]] >= GameConstants.GUNNER_ROTATE_COST

    def rotate(self, direction) -> None:
        me = self._self()
        if me["type"] != EntityType.GUNNER:
            raise GameError("rotate is gunner-only")
        if not self.can_rotate(direction):
            raise GameError("illegal rotate")
        self.world.titanium[me["team"]] -= GameConstants.GUNNER_ROTATE_COST
        me["direction"] = direction
        me["action_cd"] = 1

    def get_gunner_target(self) -> Optional[Position]:
        me = self._self()
        if me["type"] != EntityType.GUNNER:
            raise GameError("gunner-only")
        for p in self.get_attackable_tiles():
            if self.world.any_entity_at(p) is not None:
                return p
        return None

    def can_launch(self, bot_pos: Position, target: Position) -> bool:
        me = self._self()
        if not (me["type"] == EntityType.LAUNCHER and me["action_cd"] == 0
                and self.world.in_bounds(bot_pos) and self.world.in_bounds(target)
                and me["pos"].distance_squared(bot_pos) <= 2
                and self.world.builder_bot_at(bot_pos) is not None):
            return False
        d2 = me["pos"].distance_squared(target)
        return 1 <= d2 <= _VISION_SQ[EntityType.LAUNCHER]

    def launch(self, bot_pos: Position, target: Position) -> None:
        if not self.can_launch(bot_pos, target):
            raise GameError("illegal launch")
        me = self._self()
        bot_id = self.world.builder_bot_at(bot_pos)
        self.world.entities[bot_id]["pos"] = target
        me["action_cd"] = 1

    # -- core --

    def can_spawn(self, position: Position) -> bool:
        me = self._self()
        if not (me["type"] == EntityType.CORE and me["action_cd"] == 0
                and self.world.in_bounds(position)
                and me["pos"].distance_squared(position) <= GameConstants.CORE_ACTION_RADIUS_SQ
                and self.is_tile_passable(position)):
            return False
        team = me["team"]
        count = sum(1 for ent in self.world.entities.values()
                    if ent["team"] == team and ent["type"] in _UNIT_TYPES)
        return (count < GameConstants.MAX_TEAM_UNITS
                and self.world.titanium[team] >= self.world.cost(EntityType.BUILDER_BOT, team))

    def spawn_builder(self, position: Position) -> int:
        if not self.can_spawn(position):
            raise GameError("illegal spawn")
        me = self._self()
        team = me["team"]
        cost = self.world.cost(EntityType.BUILDER_BOT, team)
        self.world.titanium[team] -= cost
        eid = self.world.add(EntityType.BUILDER_BOT, team, position)
        me["action_cd"] = 1
        return eid

    def can_convert_ammo(self, amount: int) -> bool:
        me = self._self()
        if me["type"] != EntityType.CORE or amount < 0:
            return False
        if self.world._ammo_converted_this_round[me["team"]]:
            return False
        return self.world.titanium[me["team"]] >= amount

    def convert_ammo(self, amount: int) -> None:
        if not self.can_convert_ammo(amount):
            raise GameError("illegal convert_ammo")
        me = self._self()
        team = me["team"]
        self.world.titanium[team] -= amount
        self.world.ammo[team] += amount
        # Does NOT touch the action cooldown.
        self.world._ammo_converted_this_round[team] = True

    # -- indicators --

    def draw_indicator_line(self, pos_a: Position, pos_b: Position, r: int, g: int, b: int) -> None: pass
    def draw_indicator_dot(self, pos: Position, r: int, g: int, b: int) -> None: pass


def run_bot(world: World, player, entity_id: int) -> None:
    """Build a StubController for entity_id and call player.run(ct)."""
    ct = StubController(world, entity_id)
    player.run(ct)


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    def _check(cond, msg):
        if not cond:
            raise AssertionError(f"SELFTEST FAILED: {msg}")

    # -- scale: additive per-build, subtracted on destroy --
    w = World(12, 12)
    core_a = w.add(EntityType.CORE, Team.A, Position(1, 1))
    bot_a = w.add(EntityType.BUILDER_BOT, Team.A, Position(2, 1))
    ct = StubController(w, bot_a)
    _check(w.scale_pct[Team.A] == 120.0,  # core has no contrib, bot +20
           f"expected scale 120 after core+bot spawn, got {w.scale_pct[Team.A]}")
    base_sentinel_cost = ct.get_sentinel_cost()
    gunner_pos = Position(3, 1)
    _check(ct.can_build_gunner(gunner_pos, Direction.NORTH),
           "expected can_build_gunner True before building")
    gunner_id = ct.build_gunner(gunner_pos, Direction.NORTH)
    _check(w.scale_pct[Team.A] == 140.0,
           f"scale should be 100+20(bot)+20(gunner)=140, got {w.scale_pct[Team.A]}")
    new_sentinel_cost = ct.get_sentinel_cost()
    _check(new_sentinel_cost > base_sentinel_cost,
           f"sentinel cost should rise with scale: {base_sentinel_cost} -> {new_sentinel_cost}")
    _check(new_sentinel_cost == int(1.40 * 30),
           f"sentinel cost at 140% should be floor(1.4*30)=42, got {new_sentinel_cost}")
    # destroy the gunner from an adjacent tile -- reset cooldown for a clean turn
    ct._self()["action_cd"] = 0
    _check(ct.can_destroy(gunner_pos), "expected can_destroy True on own gunner")
    ct.destroy(gunner_pos)
    _check(w.scale_pct[Team.A] == 120.0,
           f"scale should drop back to 120 (bot only) after destroy, got {w.scale_pct[Team.A]}")
    _check(ct.get_sentinel_cost() == base_sentinel_cost,
           "sentinel cost should return to pre-gunner value after destroy")

    # -- destroy sets no cooldown --
    _check(ct.get_action_cooldown() == 0,
           f"destroy must not set a cooldown, got {ct.get_action_cooldown()}")
    barrier_pos = Position(3, 1)
    _check(ct.can_build_barrier(barrier_pos),
           "same-turn build after destroy should be legal (destroy is free)")
    ct.build_barrier(barrier_pos)
    _check(ct.get_action_cooldown() == 1,
           "the build itself should set the cooldown to 1")

    # -- can_fire True at 0 ammo, fire() raises --
    w2 = World(12, 12)
    gpos = Position(1, 1)
    gid = w2.add(EntityType.GUNNER, Team.A, gpos, Direction.EAST)
    tpos = Position(3, 1)
    epos_builder = w2.add(EntityType.BUILDER_BOT, Team.B, tpos)
    gct = StubController(w2, gid)
    _check(w2.ammo[Team.A] == 0, "sanity: team A ammo starts at 0")
    _check(gct.can_fire(tpos) is True,
           "can_fire must return True even at 0 ammo (real-engine asymmetry)")
    threw = False
    try:
        gct.fire(tpos)
    except GameError:
        threw = True
    _check(threw, "fire() must raise GameError when ammo is insufficient")
    # negative control: give ammo, firing must now succeed and NOT raise.
    w2.ammo[Team.A] = 100
    gct.fire(tpos)  # should not raise
    _check(w2.entities.get(epos_builder) is None or
           w2.entities[epos_builder]["hp"] < GameConstants.BUILDER_BOT_MAX_HP,
           "a funded shot must actually apply damage / remove the target")

    # -- gunner prefix-blocked, sentinel not, same geometry --
    w3 = World(12, 12)
    gpos3 = Position(1, 5)
    gid3 = w3.add(EntityType.GUNNER, Team.A, gpos3, Direction.EAST)
    spos3 = Position(1, 6)
    sid3 = w3.add(EntityType.SENTINEL, Team.A, spos3, Direction.EAST)
    barrier_block = Position(3, 5)
    w3.add(EntityType.BARRIER, Team.B, barrier_block)
    barrier_block_s = Position(3, 6)
    w3.add(EntityType.BARRIER, Team.B, barrier_block_s)
    gct3 = StubController(w3, gid3)
    sct3 = StubController(w3, sid3)
    g_tiles = gct3.get_attackable_tiles()
    s_tiles = sct3.get_attackable_tiles()
    # ⛔ THIS CONTROL WAS VACUOUS UNTIL 2026-08-15 AND PASSED FOR THE WRONG
    # REASON.  It asserted Position(5, 5) was absent from the gunner line as
    # proof of prefix-blocking -- but (5,5) is d^2=16 from (1,5) and a gunner
    # reaches 13, so it was out of RANGE and the assertion could never fail.
    # The in-range tile beyond the obstacle is (4,5), d^2=9, and the engine
    # (bots/_probe_rayempty) says it IS in the raw pattern: blocking lives in
    # can_fire/can_fire_from, not in get_attackable_tiles.
    beyond_g = Position(4, 5)          # d^2 = 9 <= 13: genuinely in range
    beyond_s = Position(4, 6)
    empty_before_g = Position(2, 5)
    _check(barrier_block in g_tiles,
           "gunner line must include the blocking tile itself")
    _check(beyond_g in g_tiles,
           "gunner RAW pattern must include in-range tiles BEYOND the first "
           "obstacle (engine: 'full firing line, even behind walls')")
    _check(gct3.can_fire_from(gpos3, Direction.EAST, EntityType.GUNNER,
                              beyond_g) is False,
           "gunner can_fire_from must be False behind an obstacle "
           "(positive control: this is where blocking actually lives)")
    _check(gct3.can_fire_from(gpos3, Direction.EAST, EntityType.GUNNER,
                              barrier_block) is True,
           "gunner can_fire_from must be True on the FIRST occupied tile")
    _check(gct3.can_fire_from(gpos3, Direction.EAST, EntityType.GUNNER,
                              empty_before_g) is False,
           "gunner can_fire_from must be False on an EMPTY tile, even unblocked "
           "(probe: 5 gunners, every empty step False)")
    _check(barrier_block_s in s_tiles and beyond_s in s_tiles,
           "sentinel line must ignore the obstacle entirely "
           "(negative control on identical geometry: opposite verdict from gunner)")
    _check(sct3.can_fire_from(spos3, Direction.EAST, EntityType.SENTINEL,
                              beyond_s) is True
           and sct3.can_fire_from(spos3, Direction.EAST, EntityType.SENTINEL,
                                  Position(2, 6)) is True,
           "sentinel can_fire_from must be True behind an obstacle AND on an "
           "empty tile -- the opposite verdict from the gunner on both")

    # -- get_tile_* raises off-map; is_in_vision is RADIUS-ONLY (no bounds check)
    #
    # ⛔ CORRECTED s50, 2026-08-17. This block used to assert
    #    `is_in_vision(off_map) is False` -- the OPPOSITE of the engine, which
    #    was probed on atoll (core at 2,14): is_in_vision((-1,14)) == True and
    #    the next get_tile_* on that position raises GameError.
    #    Ground truth: CLAUDE.md:367-377 and
    #    docs/research/PROBE-DOSSIER-ferry-siege-2026-08-17.md:186-196.
    # Driven BOTH WAYS below: off-map INSIDE the radius -> True (then raise),
    # off-map OUTSIDE the radius -> False, plus the two in-map controls.
    w4 = World(16, 16)
    core4 = w4.add(EntityType.CORE, Team.A, Position(1, 1))  # vision r^2 = 36
    ct4 = StubController(w4, core4)

    # (a) THE TRAP: off-map but INSIDE the vision radius -> True, and the very
    #     same position then raises on every get_tile_* accessor.
    off_map_near = Position(-1, -1)          # d^2 = 8 <= 36
    _check(ct4.is_in_vision(off_map_near) is True,
           "is_in_vision must return True for an OFF-MAP position inside the "
           "vision radius -- it is a pure radius test, no bounds check "
           "(engine-probed s50; a stub that returns False here is kinder than "
           "the engine and hides border bugs)")
    for _name, _fn in (("get_tile_env", ct4.get_tile_env),
                       ("get_tile_building_id", ct4.get_tile_building_id),
                       ("get_tile_builder_bot_id", ct4.get_tile_builder_bot_id)):
        _raised = False
        try:
            _fn(off_map_near)
        except GameError:
            _raised = True
        _check(_raised,
               f"{_name} must raise GameError on the SAME off-map position that "
               "is_in_vision just called True -- this True-then-raise trap is "
               "the whole hazard")

    # (b) off-map AND outside the radius -> False (and still never raises).
    off_map_far = Position(-8, 1)            # d^2 = 81 > 36
    _check(ct4.is_in_vision(off_map_far) is False,
           "is_in_vision must return False off-map when ALSO outside the radius "
           "(negative control: the same call must be able to come out False)")

    # (c) in-map controls, both verdicts, so the radius test itself is checked.
    _check(ct4.is_in_vision(Position(3, 3)) is True,
           "is_in_vision must be True for an in-map tile inside the radius")
    on_map_far = Position(15, 15)            # d^2 = 392 > 36
    _check(ct4.is_in_vision(on_map_far) is False,
           "is_in_vision must be False for an in-map tile outside the radius")
    _check(ct4.get_tile_env(on_map_far) == Environment.EMPTY,
           "get_tile_env must succeed on-map even far outside vision "
           "(positive control: on-map call must not raise)")

    # -- store writes buffered until end_round --
    w5 = World(6, 6)
    core5 = w5.add(EntityType.CORE, Team.A, Position(1, 1))
    ct5 = StubController(w5, core5)
    _check(ct5.read_store(0) == 0, "store index 0 should start at 0")
    ct5.write_store(0, 42)
    _check(ct5.read_store(0) == 0,
           "a buffered write must NOT be visible before end_round "
           "(this assertion must be able to fail if buffering is broken)")
    w5.end_round()
    _check(ct5.read_store(0) == 42,
           "the write must be visible immediately after end_round")

    print("STUB-ENGINE SELFTEST OK")
