"""POSITIVE CONTROL for the crash detector -- not a competitor.

Every builder bot raises an uncaught exception on its first turn. Per the
organisers' doc, the engine prints the traceback and PERMANENTLY destroys that
unit for the rest of the match. This bot exists so the traceback detector can
be run against a case where it MUST come out the other way (s26 D17: a check
that has never produced the other verdict has not been seen to check).

The core deliberately does NOT raise, so the match still runs to a conclusion
and the replay is well-formed.
"""
from fcode import Direction, EntityType


class Player:
    def run(self, ct) -> None:
        if ct.get_entity_type() == EntityType.CORE:
            if ct.get_action_cooldown() == 0 and \
                    ct.get_global_resources() >= ct.get_builder_bot_cost():
                for d in Direction:
                    if d == Direction.CENTRE:
                        continue
                    t = ct.get_position().add(d)
                    if ct.can_spawn(t):
                        ct.spawn_builder(t)
                        return
            return
        raise ValueError("PROBE_CRASH_SENTINEL: deliberate uncaught exception")
