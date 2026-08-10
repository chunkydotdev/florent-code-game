"""Settles whether `Player` is one instance per UNIT or one per TEAM.

Both lanes parked a forward-path inference on this: Eir's cap is
`self.forward_guns`, a counter on the Player object, so whether that is a
per-BUILDER budget or a per-TEAM budget changes what "cap 3" means entirely.
Prints id(self) with the unit id; identical ids across different units means
one shared instance.
"""
import sys
from fcode import Direction, EntityType


class Player:
    def run(self, ct) -> None:
        try:
            if not hasattr(self, "seen"):
                self.seen = set()
            uid = ct.get_id()
            if ct.get_current_round() < 8:
                print(f"IDENT r={ct.get_current_round()} unit={uid} "
                      f"kind={ct.get_entity_type().name:<11} id(self)={id(self)} "
                      f"units_seen_by_this_instance={sorted(self.seen)}",
                      file=sys.stderr)
            self.seen.add(uid)
            if ct.get_entity_type() == EntityType.CORE and ct.get_action_cooldown() == 0:
                p = ct.get_position()
                for d in Direction:
                    if d != Direction.CENTRE and ct.can_spawn(p.add(d)):
                        ct.spawn_builder(p.add(d)); return
        except Exception as exc:
            print(f"IDENT ERROR {exc}", file=sys.stderr)
