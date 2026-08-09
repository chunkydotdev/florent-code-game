"""PROBE JAILER — walks every builder it has onto the ENEMY core's 12-tile ring
and parks there forever. Builds nothing, attacks nothing, heals nothing.

Paired with `_probe_victim`, which reports its own can_spawn legality each
round. The jailer's ONLY job is to put enemy bodies on those tiles so the
victim can report what that does. Deliberately does nothing else, so any change
in the victim's report is attributable to occupation and nothing else.
"""
import sys

from fcode import Controller, Direction, EntityType, Position

CARDINALS = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)


class Player:
    def __init__(self):
        self.enemy = None
        self.seat = None

    def run(self, ct: Controller) -> None:
        try:
            self._go(ct)
        except Exception:
            import traceback
            traceback.print_exc(file=sys.stderr)

    def _go(self, ct: Controller) -> None:
        kind = ct.get_entity_type()
        if kind == EntityType.CORE:
            if ct.get_action_cooldown() != 0:
                return
            if ct.get_global_resources() < ct.get_builder_bot_cost():
                return
            p = ct.get_position()
            for dx in range(-1, 3):
                for dy in range(-1, 3):
                    t = Position(p.x + dx, p.y + dy)
                    if ct.can_spawn(t):
                        ct.spawn_builder(t)
                        return
            return
        if kind != EntityType.BUILDER_BOT:
            return

        if self.enemy is None:
            mw, mh = ct.get_map_width(), ct.get_map_height()
            for eid in ct.get_nearby_buildings():
                if (ct.get_entity_type(eid) == EntityType.CORE
                        and ct.get_team(eid) != ct.get_team()):
                    self.enemy = ct.get_position(eid)
            if self.enemy is None:
                # Rotational guess, same fallback the real bot uses.
                own = None
                for eid in ct.get_nearby_buildings():
                    if ct.get_entity_type(eid) == EntityType.CORE:
                        own = ct.get_position(eid)
                if own is None:
                    return
                self.enemy = Position(max(0, mw - 2 - own.x), max(0, mh - 2 - own.y))

        # Claim a ring seat deterministically by unit id so bodies spread out.
        foot = {(self.enemy.x + dx, self.enemy.y + dy) for dx in (0, 1) for dy in (0, 1)}
        ring = [
            Position(x, y)
            for x in range(self.enemy.x - 1, self.enemy.x + 3)
            for y in range(self.enemy.y - 1, self.enemy.y + 3)
            if (x, y) not in foot
        ]
        if self.seat is None:
            self.seat = ring[ct.get_id() % len(ring)]
        p = ct.get_position()
        if (p.x, p.y) == (self.seat.x, self.seat.y):
            return                                  # parked: this IS the probe
        if ct.get_move_cooldown() != 0:
            return
        d = p.cardinal_direction_to(self.seat)
        if d in CARDINALS and ct.can_move(d):
            ct.move(d)
            return
        for alt in CARDINALS:                       # simple sidestep
            if ct.can_move(alt):
                ct.move(alt)
                return
