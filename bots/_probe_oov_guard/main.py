"""Sweep 20B: same far-tile query, wrapped. Control arm."""
import sys
from fcode import Direction, EntityType, Position, GameError


class Player:
    def run(self, ct) -> None:
        kind = ct.get_entity_type()
        if kind == EntityType.CORE:
            try:
                print(f"GRD r={ct.get_current_round()} units={ct.get_unit_count()}", file=sys.stderr)
                if ct.get_action_cooldown() == 0 and ct.get_unit_count() < 6:
                    p = ct.get_position()
                    for d in Direction:
                        if d != Direction.CENTRE and ct.can_spawn(p.add(d)):
                            ct.spawn_builder(p.add(d))
                            return
            except Exception as exc:
                print(f"GRD CORE ERR {exc}", file=sys.stderr)
            return
        r = ct.get_current_round()
        print(f"GRD-BOT r={r} unit={ct.get_id()} alive", file=sys.stderr)
        if r >= 4:
            far = Position(ct.get_map_width() - 1, ct.get_map_height() - 1)
            try:
                ct.get_tile_env(far)
            except GameError as exc:
                print(f"GRD-BOT r={r} unit={ct.get_id()} caught: {exc}", file=sys.stderr)
