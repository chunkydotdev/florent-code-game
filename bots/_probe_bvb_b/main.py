"""bvb probe B (s57): spawns one builder that walks toward the enemy core then
stands. The passive half of the builder-vs-builder fire probe. In-game league."""
from fcode import Controller, EntityType, Direction


class Player:
    def run(self, ct: Controller) -> None:
        try:
            kind = ct.get_entity_type()
            if kind == EntityType.CORE:
                if ct.get_current_round() < 5 and not getattr(self, "_spawned", False):
                    for d in Direction:
                        if d == Direction.CENTRE:
                            continue
                        q = ct.get_position().add(d)
                        try:
                            if ct.can_spawn(q):
                                ct.spawn_builder(q)
                                self._spawned = True
                                return
                        except Exception:
                            pass
                return
            if kind != EntityType.BUILDER_BOT:
                return
            if ct.get_move_cooldown() != 0:
                return
            p = ct.get_position()
            mid = type(p)(ct.get_map_width() // 2, max(2, ct.get_map_height() // 4))
            if p.distance_squared(mid) <= 2:
                return
            d = p.cardinal_direction_to(mid)
            if d != Direction.CENTRE and ct.can_move(d):
                ct.move(d)
        except Exception:
            pass
