from fcode import Controller, Direction, EntityType

CARD = None  # filled lazily to avoid import-order surprises


class Player:
    def run(self, ct: Controller) -> None:
        global CARD
        if CARD is None:
            CARD = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)
        try:
            kind = ct.get_entity_type()
            if kind == EntityType.CORE:
                if ct.get_action_cooldown() == 0 and ct.get_unit_count() < 2:
                    for d in Direction:
                        if d == Direction.CENTRE:
                            continue
                        t = ct.get_position().add(d)
                        if ct.can_spawn(t):
                            ct.spawn_builder(t)
                            return
            elif kind == EntityType.BUILDER_BOT:
                if ct.get_current_round() < 3:
                    return  # both sides in lockstep before the deed
                p = ct.get_position()
                for d in CARD:
                    t = p.add(d)
                    bid = ct.get_tile_building_id(t)
                    if bid is None:
                        continue
                    if ct.get_entity_type(bid) == EntityType.CORE and ct.get_team(bid) == ct.get_team():
                        if ct.can_destroy(t):
                            ct.destroy(t)
                            return
                        if ct.can_fire(t):
                            ct.fire(t)
                            return
        except Exception:
            pass
