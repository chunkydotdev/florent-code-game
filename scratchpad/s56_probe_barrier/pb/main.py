from fcode import Controller, EntityType, Direction
class Player:
    def run(self, ct):
        try:
            if ct.get_entity_type() == EntityType.CORE and ct.get_current_round() == 0:
                for d in Direction:
                    if d == Direction.CENTRE: continue
                    t = ct.get_position().add(d)
                    if ct.can_spawn(t):
                        ct.spawn_builder(t); return
        except Exception:
            pass
