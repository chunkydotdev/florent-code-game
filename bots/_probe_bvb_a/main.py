"""bvb probe A (s57): spawns one builder that hunts the enemy builder and, when
orthogonally adjacent, logs can_fire and attempts fire() on the body's tile.
STDERR channel per the dead-stdout rule. In-game league fixture."""
import sys
from fcode import Controller, EntityType, Direction


class Player:
    def run(self, ct: Controller) -> None:
        try:
            kind = ct.get_entity_type()
            if ct.get_current_round() < 3:
                print(f"BVBDBG r{ct.get_current_round()} kind={kind} pos={ct.get_position()}", file=sys.stderr)
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
            p = ct.get_position()
            target = None
            for eid in ct.get_nearby_units():
                try:
                    if (ct.get_team(eid) != ct.get_team()
                            and ct.get_entity_type(eid) == EntityType.BUILDER_BOT):
                        target = ct.get_position(eid)
                        break
                except Exception:
                    continue
            if target is None:
                if ct.get_move_cooldown() == 0:
                    for d in (Direction.EAST, Direction.SOUTH, Direction.NORTH, Direction.WEST):
                        try:
                            if ct.can_move(d):
                                ct.move(d)
                                return
                        except Exception:
                            pass
                return
            dsq = p.distance_squared(target)
            if dsq == 1:
                r = ct.get_current_round()
                try:
                    cf = ct.can_fire(target)
                except Exception as e:
                    cf = f"RAISED:{type(e).__name__}"
                print(f"BVBPROBE r{r} adjacent can_fire={cf}", file=sys.stderr)
                fired = "no-attempt"
                try:
                    ct.fire(target)
                    fired = "FIRE-OK"
                except Exception as e:
                    fired = f"FIRE-RAISED:{type(e).__name__}"
                print(f"BVBPROBE r{r} fire_result={fired}", file=sys.stderr)
                return
            if ct.get_move_cooldown() == 0:
                d = p.cardinal_direction_to(target)
                try:
                    if d != Direction.CENTRE and ct.can_move(d):
                        ct.move(d)
                except Exception:
                    pass
        except Exception as e:
            print(f"BVBPROBE toplevel {type(e).__name__}: {e}", file=sys.stderr)
