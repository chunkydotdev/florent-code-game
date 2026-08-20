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


class Player:
    def run(self, ct):
        et = ct.get_entity_type()
        if et == EntityType.CORE:
            self._core(ct)
        elif et == EntityType.BUILDER_BOT:
            self._builder(ct)
        elif et == EntityType.LAUNCHER:
            self._launcher(ct)

    def _core(self, ct):
        try:
            rnd = ct.get_current_round()
            if rnd >= ROUND_CUTOFF:
                try:
                    ct.resign()
                except Exception:
                    pass
                return

            h_id = ct.read_store(0)
            t_id = ct.read_store(1)
            w_id = ct.read_store(2)
            thrown = ct.read_store(4)

            if h_id == 0:
                if ct.get_action_cooldown() == 0 and ct.can_spawn(HUB):
                    nid = ct.spawn_builder(HUB)
                    ct.write_store(0, nid)
                    print(f"CORE r={rnd} spawn H id={nid} at {HUB}", file=sys.stderr)
                return

            launcher_bid = ct.get_tile_building_id(LAUNCHER_TILE)
            launcher_ready = False
            if launcher_bid is not None:
                try:
                    launcher_ready = ct.get_entity_type(launcher_bid) == EntityType.LAUNCHER
                except Exception:
                    launcher_ready = False

            if launcher_ready and t_id == 0:
                if ct.get_action_cooldown() == 0 and ct.can_spawn(T_SPAWN):
                    nid = ct.spawn_builder(T_SPAWN)
                    ct.write_store(1, nid)
                    print(f"CORE r={rnd} spawn T id={nid} at {T_SPAWN}", file=sys.stderr)
                return

            if thrown == 1 and w_id == 0:
                if ct.get_action_cooldown() == 0 and ct.can_spawn(WALK_SPAWN):
                    nid = ct.spawn_builder(WALK_SPAWN)
                    ct.write_store(2, nid)
                    print(f"CORE r={rnd} spawn W id={nid} at {WALK_SPAWN}", file=sys.stderr)
                return

            # per-round observer log (own reads, every round once launcher exists)
            tb = ct.get_tile_builder_bot_id(TARGET_TILE)
            try:
                passable = ct.is_tile_passable(TARGET_TILE)
            except Exception as e:
                passable = f"ERR {type(e).__name__} {e}"
            try:
                empty = ct.is_tile_empty(TARGET_TILE)
            except Exception as e:
                empty = f"ERR {type(e).__name__} {e}"
            print(f"OBS r={rnd} target={TARGET_TILE} builder_on_tile={tb} "
                  f"is_tile_passable={passable} is_tile_empty={empty}", file=sys.stderr)
        except Exception as e:
            print(f"CORE OUTER EXC {type(e).__name__} {e}", file=sys.stderr)

    def _builder(self, ct):
        try:
            my_id = ct.get_id()
            h_id = ct.read_store(0)
            t_id = ct.read_store(1)
            w_id = ct.read_store(2)
            rnd = ct.get_current_round()

            if my_id == h_id:
                self._hub(ct, rnd)
            elif my_id == t_id:
                self._throwaway(ct, rnd)
            elif my_id == w_id:
                self._walker(ct, rnd)
            # else: not yet registered this round (store write lag) -- idle
        except Exception as e:
            print(f"BUILDER OUTER EXC {type(e).__name__} {e}", file=sys.stderr)

    def _hub(self, ct, rnd):
        if OWNER == "own" and KIND != "empty":
            tgt_building = ct.get_tile_building_id(TARGET_TILE)
            if tgt_building is None:
                if ct.get_action_cooldown() == 0:
                    ok = try_build_kind(ct, KIND, TARGET_TILE)
                    print(f"H r={rnd} build {KIND} at {TARGET_TILE} -> {ok}", file=sys.stderr)
                return

        lb = ct.get_tile_building_id(LAUNCHER_TILE)
        launcher_exists = False
        if lb is not None:
            try:
                launcher_exists = ct.get_entity_type(lb) == EntityType.LAUNCHER
            except Exception:
                launcher_exists = False

        if not launcher_exists:
            if ct.get_action_cooldown() == 0:
                can = ct.can_build_launcher(LAUNCHER_TILE)
                print(f"H r={rnd} can_build_launcher({LAUNCHER_TILE})={can}", file=sys.stderr)
                if can:
                    try:
                        ct.build_launcher(LAUNCHER_TILE)
                        print(f"H r={rnd} build_launcher OK", file=sys.stderr)
                    except Exception as e:
                        print(f"H r={rnd} build_launcher FAIL {type(e).__name__} {e}", file=sys.stderr)
            return

        try:
            ct.self_destruct()
            print(f"H r={rnd} self_destruct (job done)", file=sys.stderr)
        except Exception as e:
            print(f"H r={rnd} self_destruct FAIL {type(e).__name__} {e}", file=sys.stderr)

    def _throwaway(self, ct, rnd):
        pos = ct.get_position()
        print(f"T r={rnd} pos={pos} hp={ct.get_hp()}", file=sys.stderr)
        if pos == PICKUP_TILE:
            if rnd > 40:
                # Never got thrown (e.g. target is a barrier -- can_launch stays False
                # forever). Free the pickup tile so W's path through it isn't blocked.
                try:
                    ct.self_destruct()
                    print(f"T r={rnd} self_destruct (never thrown, giving up pickup tile)",
                          file=sys.stderr)
                except Exception as e:
                    print(f"T r={rnd} self_destruct FAIL {type(e).__name__} {e}", file=sys.stderr)
            return
        if pos not in T_PATH:
            # Already thrown somewhere off T_PATH -- self-destruct immediately so it
            # doesn't camp on a tile the walker (W) needs to path through.
            try:
                ct.self_destruct()
                print(f"T r={rnd} self_destruct (post-throw, was at {pos})", file=sys.stderr)
            except Exception as e:
                print(f"T r={rnd} self_destruct FAIL {type(e).__name__} {e}", file=sys.stderr)
            return
        if ct.get_move_cooldown() != 0:
            return
        nxt = next_waypoint(pos, T_PATH)
        if nxt is None:
            print(f"T r={rnd} pos={pos} NO PATH (already past pickup?)", file=sys.stderr)
            return
        d = pos.cardinal_direction_to(nxt)
        try:
            can = ct.can_move(d)
        except Exception as e:
            can = f"ERR {type(e).__name__} {e}"
        if can is True:
            try:
                ct.move(d)
            except Exception as e:
                print(f"T r={rnd} MOVE FAIL {type(e).__name__} {e}", file=sys.stderr)
        else:
            print(f"T r={rnd} pos={pos} blocked toward {nxt} can_move={can}", file=sys.stderr)

    def _walker(self, ct, rnd):
        pos = ct.get_position()
        if pos == TARGET_TILE:
            print(f"W r={rnd} ALREADY ON TARGET pos={pos}", file=sys.stderr)
            return

        stage = WALK_PATH[-1]
        if pos == stage:
            d = pos.cardinal_direction_to(TARGET_TILE)
            try:
                can = ct.can_move(d)
            except Exception as e:
                can = f"ERR {type(e).__name__} {e}"
            print(f"W r={rnd} AT STAGE={stage} dir_to_target={d} can_move={can}", file=sys.stderr)
            if ct.get_move_cooldown() != 0:
                return
            try:
                ct.move(d)
                print(f"W r={rnd} MOVE OK now at {ct.get_position()}", file=sys.stderr)
            except Exception as e:
                print(f"W r={rnd} MOVE FAIL can_move_said={can} exc={type(e).__name__} {e}", file=sys.stderr)
            return

        if ct.get_move_cooldown() != 0:
            return
        nxt = next_waypoint(pos, WALK_PATH)
        if nxt is None:
            print(f"W r={rnd} pos={pos} NO PATH FOUND", file=sys.stderr)
            return
        d = pos.cardinal_direction_to(nxt)
        try:
            can = ct.can_move(d)
        except Exception as e:
            can = f"ERR {type(e).__name__} {e}"
        if can is True:
            try:
                ct.move(d)
            except Exception as e:
                print(f"W r={rnd} PATH MOVE FAIL {type(e).__name__} {e}", file=sys.stderr)
        else:
            print(f"W r={rnd} pos={pos} blocked toward {nxt} can_move={can}", file=sys.stderr)

    def _launcher(self, ct):
        try:
            rnd = ct.get_current_round()
            t_id = ct.read_store(1)
            thrown = ct.read_store(4)

            try:
                can = ct.can_launch(PICKUP_TILE, TARGET_TILE)
            except Exception as e:
                can = f"ERR {type(e).__name__} {e}"
            print(f"LNCH r={rnd} can_launch(pickup={PICKUP_TILE},target={TARGET_TILE})={can}",
                  file=sys.stderr)

            if thrown == 1 or t_id == 0:
                return

            occ = ct.get_tile_builder_bot_id(PICKUP_TILE)
            if occ != t_id:
                return
            if ct.get_action_cooldown() != 0:
                return

            try:
                ct.launch(PICKUP_TILE, TARGET_TILE)
                print(f"LNCH r={rnd} LAUNCH OK", file=sys.stderr)
            except Exception as e:
                print(f"LNCH r={rnd} LAUNCH FAIL {type(e).__name__} {e}", file=sys.stderr)
            try:
                ct.write_store(4, 1)
            except Exception as e:
                print(f"LNCH r={rnd} write_store FAIL {type(e).__name__} {e}", file=sys.stderr)
        except Exception as e:
            print(f"LNCH OUTER EXC {type(e).__name__} {e}", file=sys.stderr)
