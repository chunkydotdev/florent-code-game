"""PROBE SITTER — the passive target for _probe_meleebot's melee-attack probe.

Spawns ONE builder bot. That builder walks toward the (guessed) enemy core
and, once orthogonally adjacent to any ENEMY entity (unit or building), stops
completely: no build, no attack, no further movement. It just sits there as
a stationary target so the attacker can measure can_fire()/fire() against it
across multiple rounds.

Adjacency to our OWN core (which happens immediately at spawn, since the
builder is placed on a tile adjacent to it) does NOT trigger the stop --
only enemy adjacency does. Otherwise the builder would freeze at round 0
next to its own spawn point and never approach the enemy at all.

Everything is wrapped in try/except: an escaping exception permanently
destroys the unit (per CLAUDE.md) and would silently ruin the probe.
"""
import sys

from fcode import Controller, Direction, EntityType, Position

CARDINALS = (Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST)


class Player:
    spawned = False

    def run(self, ct: Controller) -> None:
        try:
            kind = ct.get_entity_type()
            if kind == EntityType.CORE:
                self._core_turn(ct)
            elif kind == EntityType.BUILDER_BOT:
                self._builder_turn(ct)
        except Exception:
            import traceback
            traceback.print_exc(file=sys.stderr)

    def _core_turn(self, ct: Controller) -> None:
        if Player.spawned:
            return
        if ct.get_action_cooldown() != 0:
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
                Player.spawned = True
                return

    def _builder_turn(self, ct: Controller) -> None:
        p = ct.get_position()
        me = ct.get_team()

        # Stop for good once adjacent to any ENEMY entity -- become the target.
        for d in CARDINALS:
            t = p.add(d)
            try:
                bid = ct.get_tile_builder_bot_id(t)
            except Exception:
                bid = None
            if bid is not None:
                try:
                    if ct.get_team(bid) != me:
                        return
                except Exception:
                    pass
            try:
                bldg = ct.get_tile_building_id(t)
            except Exception:
                bldg = None
            if bldg is not None:
                try:
                    if ct.get_team(bldg) != me:
                        return
                except Exception:
                    pass

        if ct.get_move_cooldown() != 0:
            return

        target = self._enemy_core_guess(ct, me)
        d = p.cardinal_direction_to(target)
        if d != Direction.CENTRE:
            try:
                if ct.can_move(d):
                    ct.move(d)
                    return
            except Exception:
                pass
        for alt in CARDINALS:
            try:
                if ct.can_move(alt):
                    ct.move(alt)
                    return
            except Exception:
                continue

    # Cache: unit id -> fixed heuristic mirror-point target, computed ONCE
    # from this unit's SPAWN position. Recomputing "mirror of current
    # position" every round makes the target chase the mover itself (moving
    # east shifts the mirror target west by the same amount), oscillating
    # forever around the map's centre instead of converging.
    home_targets = {}

    def _enemy_core_guess(self, ct: Controller, me) -> Position:
        try:
            for bid in ct.get_nearby_buildings():
                if ct.get_team(bid) != me and ct.get_entity_type(bid) == EntityType.CORE:
                    return ct.get_position(bid)
        except Exception:
            pass
        uid = ct.get_id()
        cached = Player.home_targets.get(uid)
        if cached is not None:
            return cached
        # Heuristic fallback: maps are symmetric by reflection/rotation, so
        # mirroring our own position about the map centre points roughly at
        # the enemy core before it's ever been seen.
        p = ct.get_position()
        mw, mh = ct.get_map_width(), ct.get_map_height()
        target = Position(mw - 1 - p.x, mh - 1 - p.y)
        Player.home_targets[uid] = target
        return target
