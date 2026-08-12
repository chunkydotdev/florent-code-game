"""Sweep 20B: the out-of-vision legality surface.

Pass 1 (r5, builders): which Controller calls are TOTAL on an unseeable tile and
which RAISE, incl. off-map tiles and over-large dist_sq.
Pass 2 (r3/25/60, builders): is a remembered entity id still a valid handle once
the entity leaves vision? (r3 is the in-vision positive control.)
Pass 3 (r3, core): store index and value bounds.
"""
import sys
from fcode import Direction, EntityType, Position, GameError


def probe(name, fn):
    try:
        return f"{name}=OK({fn()!r})"
    except GameError as exc:
        return f"{name}=RAISE({exc})"
    except Exception as exc:
        return f"{name}=OTHER({type(exc).__name__}:{exc})"


class Player:
    def run(self, ct) -> None:
        try:
            kind = ct.get_entity_type()
            r = ct.get_current_round()
            if kind == EntityType.CORE:
                if ct.get_action_cooldown() == 0 and ct.get_unit_count() < 3:
                    p = ct.get_position()
                    for d in Direction:
                        if d != Direction.CENTRE and ct.can_spawn(p.add(d)):
                            ct.spawn_builder(p.add(d))
                            return
                if r == 3:
                    for name, fn in [
                        ("read_store(0)", lambda: ct.read_store(0)),
                        ("read_store(15)", lambda: ct.read_store(15)),
                        ("read_store(16)", lambda: ct.read_store(16)),
                        ("write_store(16,1)", lambda: ct.write_store(16, 1)),
                        ("write_store(0,2**62)", lambda: ct.write_store(0, 2**62)),
                        ("write_store(0,-5)", lambda: ct.write_store(0, -5)),
                    ]:
                        print("  STORE " + probe(name, fn), file=sys.stderr)
                return
            # builder: remember own core id at r1 (in vision), walk away, re-query
            if not hasattr(self, "core_id"):
                self.core_id = None
            if self.core_id is None:
                for eid in ct.get_nearby_entities():
                    if ct.get_entity_type(eid) == EntityType.CORE:
                        self.core_id = eid
                        print(f"REMEMBER unit={ct.get_id()} core_id={eid} at r={r}", file=sys.stderr)
                        break
            if self.core_id is not None and r in (3, 25, 60):
                cid = self.core_id
                print(f"RECALL r={r} unit={ct.get_id()} pos={ct.get_position()}", file=sys.stderr)
                for name, fn in [
                    ("get_position(core)", lambda: ct.get_position(cid)),
                    ("get_hp(core)", lambda: ct.get_hp(cid)),
                    ("get_entity_type(core)", lambda: ct.get_entity_type(cid)),
                    ("get_team(core)", lambda: ct.get_team(cid)),
                    ("get_max_hp(core)", lambda: ct.get_max_hp(cid)),
                ]:
                    print("  " + probe(name, fn), file=sys.stderr)

            if r == 5:
                w, h = ct.get_map_width(), ct.get_map_height()
                far = Position(w - 1, h - 1)
                oob = Position(w + 5, h + 5)
                vr = ct.get_vision_radius_sq()
                here = ct.get_position()
                print(f"SURFACE unit={ct.get_id()} pos={here} far={far} vr_sq={vr} "
                      f"dist_sq_to_far={here.distance_squared(far)}", file=sys.stderr)
                for name, fn in [
                    ("is_in_vision(far)", lambda: ct.is_in_vision(far)),
                    ("get_tile_env(far)", lambda: ct.get_tile_env(far)),
                    ("is_tile_empty(far)", lambda: ct.is_tile_empty(far)),
                    ("is_tile_passable(far)", lambda: ct.is_tile_passable(far)),
                    ("get_tile_building_id(far)", lambda: ct.get_tile_building_id(far)),
                    ("get_tile_builder_bot_id(far)", lambda: ct.get_tile_builder_bot_id(far)),
                    ("can_build_barrier(far)", lambda: ct.can_build_barrier(far)),
                    ("can_build_conveyor(far,N)", lambda: ct.can_build_conveyor(far, Direction.NORTH)),
                    ("can_heal(far)", lambda: ct.can_heal(far)),
                    ("can_destroy(far)", lambda: ct.can_destroy(far)),
                    ("can_fire(far)", lambda: ct.can_fire(far)),
                    ("get_nearby_tiles(vr)", lambda: len(ct.get_nearby_tiles(vr))),
                    ("get_nearby_tiles(vr+1)", lambda: len(ct.get_nearby_tiles(vr + 1))),
                    ("get_nearby_tiles(9999)", lambda: len(ct.get_nearby_tiles(9999))),
                    ("get_nearby_entities(9999)", lambda: len(ct.get_nearby_entities(9999))),
                    ("is_in_vision(oob)", lambda: ct.is_in_vision(oob)),
                    ("get_tile_env(oob)", lambda: ct.get_tile_env(oob)),
                    ("is_tile_empty(oob)", lambda: ct.is_tile_empty(oob)),
                    ("get_hp(99999)", lambda: ct.get_hp(99999)),
                ]:
                    print("  " + probe(name, fn), file=sys.stderr)
            if ct.get_move_cooldown() == 0:
                for d in (Direction.EAST, Direction.SOUTH, Direction.NORTH, Direction.WEST):
                    if ct.can_move(d):
                        ct.move(d)
                        return
        except Exception as exc:
            print(f"OUTER ERR {type(exc).__name__}:{exc}", file=sys.stderr)
