"""QUEUE #17 immune control — byte-identical to `bots/_probe_border_raw`
EXCEPT the self-relative neighbour query is wrapped.

It must survive the IDENTICAL throw.  This is the cell that makes the leg a
test rather than an observation: if the guarded probe dies too, whatever killed
the raw probe was not the unguarded query, and the mechanism claim is refuted
even if cell (a) is loud.
"""
import sys

from fcode import Direction, EntityType, GameError, Position


class Player:
    def run(self, ct) -> None:
        kind = ct.get_entity_type()
        if kind == EntityType.CORE:
            try:
                if ct.get_action_cooldown() == 0 and ct.get_unit_count() < 8:
                    p = ct.get_position()
                    for d in Direction:
                        if d != Direction.CENTRE and ct.can_spawn(p.add(d)):
                            ct.spawn_builder(p.add(d))
                            return
            except Exception as exc:
                print(f"BGRD CORE ERR {exc}", file=sys.stderr)
            return
        if kind != EntityType.BUILDER_BOT:
            return
        p = ct.get_position()
        print(f"BGRD r={ct.get_current_round()} unit={ct.get_id()} "
              f"pos=({p.x},{p.y}) alive", file=sys.stderr)
        for d in (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST):
            try:
                ct.get_tile_env(p.add(d))
            except GameError as exc:
                print(f"BGRD r={ct.get_current_round()} unit={ct.get_id()} "
                      f"caught: {exc}", file=sys.stderr)
        # Same border-avoiding movement as the raw arm -- the two probes must
        # differ ONLY in the try/except, or the control is not a control.
        if ct.get_move_cooldown() == 0:
            w, h = ct.get_map_width(), ct.get_map_height()
            for d in (Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST):
                t = p.add(d)
                if t.x <= 0 or t.y <= 0 or t.x >= w - 1 or t.y >= h - 1:
                    continue
                if ct.can_move(d):
                    ct.move(d)
                    return
