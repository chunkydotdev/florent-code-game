"""STEP-0 PROBE (s48): does a SENTINEL's line shot pass THROUGH an enemy CORE?

Run on maps/invented/pierce16.map26 (scratchpad/mk_pierce_map.py), which puts
both cores on row y=7:

    A core (3,7)-(4,8)      seat (9,7)      B core (10,7)-(11,8)   belt (12,7)

The same tree plays BOTH seats and branches on ct.get_team():

  TEAM A  (attacker)  core converts titanium to ammo, spawns ONE builder, the
                      builder walks to (8,7) and builds a SENTINEL on (9,7)
                      facing EAST.  The sentinel then answers, every round:
                        - get_attackable_tiles(): does the raw pattern contain
                          the tiles BEHIND the enemy core?
                        - can_fire((12,7)) with two enemy CORE tiles on the ray
                        - the actual damage ledger: HP of the belt at (12,7)
                          AND HP of the core tile at (10,7), before and after
                          one real shot.  If the core also loses HP, the shot
                          damages the whole ray; if only the belt does, the
                          shot damages only the target tile.
  TEAM B  (victim)    spawns ONE builder, walks it to (12,8), builds a
                      CONVEYOR on (12,7) facing WEST (a core-mouth delivery
                      tile) and REBUILDS it whenever it dies -- which also
                      exercises the re-kill-on-rebuild case.

Everything is printed to stderr with a PIERCE prefix.  Nothing here is a bot;
it is an instrument, and it is scripted rather than reactive so that every
line it prints is attributable to one contrived position.
"""

import sys

from fcode import Controller, Direction, EntityType, Position

SEAT = Position(9, 7)          # our sentinel
BUILD_FROM = Position(8, 7)    # our builder stands here to build the seat
CORE_B_NEAR = Position(10, 7)  # first enemy core tile on the ray
CORE_B_FAR = Position(11, 7)   # second enemy core tile on the ray
BELT = Position(12, 7)         # enemy core-mouth belt tile, BEHIND the core
FAR = Position(13, 7)          # one tile further out
VICT_STAND = Position(12, 8)   # victim builder's build seat


def log(*a):
    print("PIERCE", *a, file=sys.stderr)


class Player:
    def __init__(self):
        self.state = 0
        self.logged_pattern = False
        self.shots = 0
        self.pre = None

    def run(self, ct: Controller) -> None:
        try:
            team = ct.get_team()
            kind = ct.get_entity_type()
            attacker = (team.name == "A")
            if kind == EntityType.CORE:
                self._core(ct, attacker)
            elif kind == EntityType.BUILDER_BOT:
                self._builder(ct, attacker)
            elif kind == EntityType.SENTINEL:
                self._sentinel(ct)
        except Exception as exc:  # never let the probe die mid-measurement
            log("ERROR", type(exc).__name__, exc, "r=%d" % ct.get_current_round())

    # ---- core ------------------------------------------------------------
    def _core(self, ct: Controller, attacker: bool) -> None:
        if attacker and ct.get_current_round() == 1 and ct.can_convert_ammo(200):
            ct.convert_ammo(200)
            log("r=%d converted 200 Ti -> ammo, ammo=%d"
                % (ct.get_current_round(), ct.get_global_ammo()))
        if self.state != 0 or ct.get_action_cooldown() != 0:
            return
        want = Position(5, 7) if attacker else VICT_STAND
        order = [want] + [ct.get_position().add(d) for d in Direction if d != Direction.CENTRE]
        for t in order:
            try:
                ok = ct.can_spawn(t)
            except Exception:
                continue
            if ok:
                bid = ct.spawn_builder(t)
                self.state = 1
                log("r=%d %s core spawned builder %d at (%d,%d)"
                    % (ct.get_current_round(), "A" if attacker else "B", bid, t.x, t.y))
                return

    # ---- builder ---------------------------------------------------------
    def _builder(self, ct: Controller, attacker: bool) -> None:
        stand = BUILD_FROM if attacker else VICT_STAND
        pos = ct.get_position()
        if pos != stand:
            if ct.get_move_cooldown() == 0:
                d = pos.cardinal_direction_to(stand)
                if d != Direction.CENTRE and ct.can_move(d):
                    ct.move(d)
                else:  # sidestep
                    for alt in (Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST):
                        if ct.can_move(alt):
                            ct.move(alt)
                            break
            return
        if ct.get_action_cooldown() != 0:
            return
        if attacker:
            if ct.get_tile_building_id(SEAT) is not None:
                return
            if ct.can_build_sentinel(SEAT, Direction.EAST):
                sid = ct.build_sentinel(SEAT, Direction.EAST)
                log("r=%d A built SENTINEL id=%d at (%d,%d) facing EAST"
                    % (ct.get_current_round(), sid, SEAT.x, SEAT.y))
            else:
                log("r=%d A cannot build sentinel yet ti=%d cost=%d"
                    % (ct.get_current_round(), ct.get_global_resources(),
                       ct.get_sentinel_cost()))
        else:
            if ct.get_tile_building_id(BELT) is not None:
                return
            if ct.can_build_conveyor(BELT, Direction.WEST):
                cid = ct.build_conveyor(BELT, Direction.WEST)
                log("r=%d B built CONVEYOR id=%d at (%d,%d) facing WEST (rebuild#%d)"
                    % (ct.get_current_round(), cid, BELT.x, BELT.y, self.shots))
                self.shots += 1

    # ---- the sentinel: the actual measurement ----------------------------
    def _sentinel(self, ct: Controller) -> None:
        r = ct.get_current_round()
        if not self.logged_pattern:
            self.logged_pattern = True
            tiles = ct.get_attackable_tiles()
            log("r=%d ATTACKABLE(from seat, facing EAST) = %s"
                % (r, sorted((t.x, t.y) for t in tiles)))
            log("r=%d   belt(12,7) in pattern? %s | far(13,7) in pattern? %s | "
                "coretile(10,7) in pattern? %s"
                % (r, BELT in tiles, FAR in tiles, CORE_B_NEAR in tiles))

        def bid(p):
            try:
                return ct.get_tile_building_id(p)
            except Exception as e:
                return "ERR:%s" % type(e).__name__

        def hp(p):
            i = bid(p)
            if not isinstance(i, int):
                return None
            try:
                return ct.get_hp(i)
            except Exception:
                return None

        belt_id, core_id = bid(BELT), bid(CORE_B_NEAR)
        # Post-shot ledger for the previous round's shot.
        if self.pre is not None:
            pb, pc = self.pre
            log("r=%d LEDGER after shot: belt hp %s -> %s | core hp %s -> %s"
                % (r, pb, hp(BELT), pc, hp(CORE_B_NEAR)))
            self.pre = None

        if ct.get_action_cooldown() != 0 or ct.get_global_ammo() < 10:
            return
        if not isinstance(belt_id, int):
            return  # wait for the victim to build its belt

        cf_belt = ct.can_fire(BELT)
        cf_far = ct.can_fire(FAR)
        cf_core = ct.can_fire(CORE_B_NEAR)
        if self.shots < 12:
            log("r=%d CAN_FIRE belt(12,7)=%s far(13,7)=%s coretile(10,7)=%s ammo=%d"
                % (r, cf_belt, cf_far, cf_core, ct.get_global_ammo()))
        if cf_belt:
            self.pre = (hp(BELT), hp(CORE_B_NEAR))
            ct.fire(BELT)
            self.shots += 1
            log("r=%d FIRED at belt(12,7) shot#%d (pre belt=%s core=%s)"
                % (r, self.shots, self.pre[0], self.pre[1]))
