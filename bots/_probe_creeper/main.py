"""PROBE CREEPER — a point-blank siege-ladder fixture for QUEUE #45.

Mimics the shape measured in OPP-lingling40-profile + OPP-team-lazy-profile
(both 2026-08-13): builders walk to the enemy core, plant GUNNERS at
point-blank range (median d²=5 in the profiles), stand beside them as
feeders, and REBUILD a destroyed turret immediately (measured field latency
1-2 rounds). The core converts ammo continuously so the ladder always fires.

⛔ FIXTURE, NOT AN ARM. It exists so a treatment (feeder-first targeting) and
its control can be dosed against the ladder shape locally. Per FIXTURE_OF_
RECORD this proves MECHANISM only; the currency read is a live pinned leg
vs the real ladder teams (CAL-3 cells C1/C4).

Known direction of lie: this fixture rebuilds unconditionally and never
retreats, which OVERSTATES rebuild persistence vs a real team — fine for a
dose (it makes the renewable-turret premise maximally true), stated so a
null cannot be blamed on the fixture being too soft.
"""
import sys

from fcode import Controller, Direction, EntityType, Environment, Position

CARDINALS = (Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST)
MAX_BUILDERS = 6
CREEP_DSQ = 5          # plant when a core tile is within this of the builder


class Player:
    spawned = 0
    enemy_core_est = None   # reflected own-core position, computed once

    def run(self, ct: Controller) -> None:
        try:
            kind = ct.get_entity_type()
            if kind == EntityType.CORE:
                self._core_turn(ct)
            elif kind == EntityType.BUILDER_BOT:
                self._builder_turn(ct)
            elif kind == EntityType.GUNNER:
                self._gunner_turn(ct)
        except Exception:
            import traceback
            traceback.print_exc(file=sys.stderr)

    # ------------------------------------------------------------- core
    def _core_turn(self, ct: Controller) -> None:
        if Player.enemy_core_est is None:
            p = ct.get_position()
            Player.enemy_core_est = Position(
                ct.get_map_width() - 1 - p.x, ct.get_map_height() - 1 - p.y)
        # Feed the ladder: 1:1 conversion, keep a build float of ~60 Ti.
        bank = ct.get_global_resources()
        if bank > 60 and ct.can_convert_ammo(20):
            ct.convert_ammo(20)
        if ct.get_action_cooldown() != 0:
            return
        if Player.spawned >= MAX_BUILDERS:
            return
        if ct.get_global_resources() < ct.get_builder_bot_cost():
            return
        p = ct.get_position()
        for d in Direction:
            if d == Direction.CENTRE:
                continue
            t = p.add(d)
            if ct.can_spawn(t):
                ct.spawn_builder(t)
                Player.spawned += 1
                return

    # ---------------------------------------------------------- builder
    def _visible_enemy_core_tile(self, ct, me):
        best, best_d = None, 10 ** 9
        p = ct.get_position()
        for bid in ct.get_nearby_buildings():
            try:
                if (ct.get_team(bid) != me
                        and ct.get_entity_type(bid) == EntityType.CORE):
                    q = ct.get_position(bid)
                    d = p.distance_squared(q)
                    if d < best_d:
                        best, best_d = q, d
            except Exception:
                continue
        return best

    def _builder_turn(self, ct: Controller) -> None:
        me = ct.get_team()
        p = ct.get_position()
        core = self._visible_enemy_core_tile(ct, me)
        target = core or Player.enemy_core_est

        # 1. FEEDER DUTY: if a core tile is in creep range, keep exactly one
        #    gunner alive on an adjacent tile, rebuilding the instant it dies.
        if (core is not None and p.distance_squared(core) <= CREEP_DSQ + 4
                and ct.get_action_cooldown() == 0):
            has_own_gun = False
            for d in CARDINALS:
                t = p.add(d)
                try:
                    bid = ct.get_tile_building_id(t)
                    if (bid is not None and ct.get_team(bid) == me
                            and ct.get_entity_type(bid) == EntityType.GUNNER):
                        has_own_gun = True
                        break
                except Exception:
                    continue
            if not has_own_gun:
                for d in CARDINALS:
                    t = p.add(d)
                    try:
                        facing = t.direction_to(core)
                        if ct.can_build_gunner(t, facing):
                            ct.build_gunner(t, facing)
                            print(f"CREEP45 plant r={ct.get_current_round()} "
                                  f"d2={t.distance_squared(core)}")
                            return
                    except Exception:
                        continue
            else:
                return          # stand fast beside the gun: the feeder shape

        # 2. Otherwise creep toward the enemy core.
        if ct.get_move_cooldown() == 0 and target is not None:
            d = p.cardinal_direction_to(target)
            if d != Direction.CENTRE:
                try:
                    if ct.can_move(d):
                        ct.move(d)
                        return
                except Exception:
                    pass
            for d2 in CARDINALS:      # slide around obstacles
                try:
                    if ct.can_move(d2) and p.add(d2).distance_squared(target) \
                            < p.distance_squared(target) + 3:
                        ct.move(d2)
                        return
                except Exception:
                    continue

    # ----------------------------------------------------------- gunner
    def _gunner_turn(self, ct: Controller) -> None:
        if ct.get_action_cooldown() != 0:
            return
        try:
            tgt = ct.get_gunner_target()
            if tgt is not None and ct.can_fire(tgt):
                me = ct.get_team()
                bid = ct.get_tile_building_id(tgt)
                bot = ct.get_tile_builder_bot_id(tgt)
                hostile = ((bid is not None and ct.get_team(bid) != me)
                           or (bot is not None and ct.get_team(bot) != me))
                if hostile:
                    ct.fire(tgt)
        except Exception:
            pass
