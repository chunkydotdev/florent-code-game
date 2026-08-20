import sys
from fcode import Controller, Direction, EntityType, Position

HUB = Position(3, 1)
LAUNCHER_TILE = Position(4, 1)
PICKUP_TILE = Position(4, 0)
T_SPAWN = Position(2, 0)
T_PATH = [Position(2, 0), Position(3, 0), Position(4, 0)]

OWN_TARGET = Position(3, 2)
OWN_WALK_SPAWN = Position(2, 3)
OWN_WALK_PATH = [Position(2, 3), Position(3, 3)]

ENEMY_TARGET = Position(4, 5)
ENEMY_WALK_SPAWN = Position(3, 2)
ENEMY_WALK_PATH = [
    Position(3, 2), Position(3, 1), Position(3, 0), Position(4, 0),
    Position(5, 0), Position(5, 1), Position(5, 2), Position(5, 3),
    Position(5, 4), Position(4, 4),
]

OWNER = "own"
KIND = "empty"

if OWNER == "own":
    TARGET_TILE = OWN_TARGET
    WALK_SPAWN = OWN_WALK_SPAWN
    WALK_PATH = OWN_WALK_PATH
else:
    TARGET_TILE = ENEMY_TARGET
    WALK_SPAWN = ENEMY_WALK_SPAWN
    WALK_PATH = ENEMY_WALK_PATH

ROUND_CUTOFF = 150


def try_build_kind(ct, kind, pos):
    try:
        if kind == "conveyor":
            ok = ct.can_build_conveyor(pos, Direction.SOUTH)
            print(f"BUILD can_build_conveyor({pos})={ok}", file=sys.stderr)
            if ok:
                ct.build_conveyor(pos, Direction.SOUTH)
                return True
            return False
        elif kind == "barrier":
            ok = ct.can_build_barrier(pos)
            print(f"BUILD can_build_barrier({pos})={ok}", file=sys.stderr)
            if ok:
                ct.build_barrier(pos)
                return True
            return False
        elif kind == "splitter":
            ok = ct.can_build_splitter(pos, Direction.SOUTH)
            print(f"BUILD can_build_splitter({pos})={ok}", file=sys.stderr)
            if ok:
                ct.build_splitter(pos, Direction.SOUTH)
                return True
            return False
        elif kind == "empty":
            return True
    except Exception as e:
        print(f"BUILD EXC {type(e).__name__} {e}", file=sys.stderr)
        return False
    return False


def next_waypoint(pos, path):
    for i, wp in enumerate(path):
        if pos == wp:
            if i + 1 < len(path):
                return path[i + 1]
            return None
    return path[0]


DEF_HUB = Position(4, 6)
DEF_TARGET = Position(4, 5)


class Player:
    def run(self, ct):
        try:
            et = ct.get_entity_type()
            if et == EntityType.CORE:
                self._core(ct)
            elif et == EntityType.BUILDER_BOT:
                self._builder(ct)
        except Exception as e:
            print(f"DEF OUTER EXC {type(e).__name__} {e}", file=sys.stderr)

    def _core(self, ct):
        rnd = ct.get_current_round()
        if rnd >= ROUND_CUTOFF:
            try:
                ct.resign()
            except Exception:
                pass
            return
        hid = ct.read_store(0)
        if hid == 0:
            if ct.get_action_cooldown() == 0 and ct.can_spawn(DEF_HUB):
                nid = ct.spawn_builder(DEF_HUB)
                ct.write_store(0, nid)
                print(f"DEFCORE r={rnd} spawn Hp id={nid} at {DEF_HUB}", file=sys.stderr)

    def _builder(self, ct):
        hid = ct.read_store(0)
        if ct.get_id() != hid:
            return
        rnd = ct.get_current_round()
        tgt_building = ct.get_tile_building_id(DEF_TARGET)
        if tgt_building is None:
            if ct.get_action_cooldown() == 0:
                ok = try_build_kind(ct, "barrier", DEF_TARGET)
                print(f"Hp r={rnd} build barrier at {DEF_TARGET} -> {ok}", file=sys.stderr)
