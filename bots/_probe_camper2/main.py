"""PROBE CAMPER-2 — need-keyed heal-camp fixture (behaviour-library #1).

Fixture-library build per SPEC-behaviour-fixture-library-2026-08-14: the
field habit is CHRONIC HEAL-CAMP (highest loss-correlation in the repo).
KEY DESIGN CHANGE vs _probe_camper (frozen v1): healing keys on NEED, not
uptime — Leviathan's core-heal share swings 7-100% by need (research spec;
constants name their sources). v1's documented lie direction is also fixed:
its healers occupied ALL core-adjacent seats, so enemy raiders could never
reach core adjacency and the park geometry never formed. v2 caps adjacent
healers at 2 (SOURCE: leaves 6 core-orthogonal seats open, matching the
Jython-game geometry where our parked bots stood at d2<=2), holds the rest
at a second ring healing barriers.

LIE DIRECTION (stated): heal reaction is INSTANT on damage (real campers
have 1-2 round latency) and the camp never rotates bodies — both overstate
camp resilience, which is the safe side for a fixture whose treatments
claim to break camps.
"""
import sys

from fcode import Controller, Direction, EntityType, Position

CARDINALS = (Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST)
MAX_BUILDERS = 8   # SOURCE: Leviathan fields 8-25 builders (OPP profile 2026-08-13); 8 = low end, keeps scale tax bounded


class Player:
    spawned = 0

    def run(self, ct: Controller) -> None:
        try:
            kind = ct.get_entity_type()
            if kind == EntityType.CORE:
                self._core_turn(ct)
            elif kind == EntityType.BUILDER_BOT:
                self._builder_turn(ct)
        except Exception:
            import traceback
            traceback.print_exc(file=sys.stderr)

    def _core_turn(self, ct: Controller) -> None:
        if ct.get_action_cooldown() != 0 or Player.spawned >= MAX_BUILDERS:
            return
        if ct.get_global_resources() < ct.get_builder_bot_cost() + 60:
            return   # keep a heal float
        p = ct.get_position()
        for d in Direction:
            if d == Direction.CENTRE:
                continue
            t = p.add(d)
            if ct.can_spawn(t):
                ct.spawn_builder(t)
                Player.spawned += 1
                return

    def _own_core_tiles(self, ct, me):
        if getattr(self, "_ctiles", None) is None:
            for bid in ct.get_nearby_buildings():
                try:
                    if (ct.get_team(bid) == me
                            and ct.get_entity_type(bid) == EntityType.CORE):
                        c = ct.get_position(bid)
                        self._ctiles = [Position(c.x + dx, c.y + dy)
                                        for dx in (0, 1) for dy in (0, 1)]
                        self._cid = bid
                        break
                except Exception:
                    continue
        return getattr(self, "_ctiles", None)

    def _builder_turn(self, ct: Controller) -> None:
        me = ct.get_team()
        p = ct.get_position()
        ctiles = self._own_core_tiles(ct, me)
        if ctiles is None:
            return

        adj_core = [t for t in ctiles
                    if abs(p.x - t.x) + abs(p.y - t.y) == 1]

        # NEED-KEYED SEAT CAP: at most 2 healers hold core-adjacent seats
        # (leaves 6 open — the park geometry v1 destroyed). Count friendly
        # builders already orthogonal to any core tile; if >=2 others and I
        # am not adjacent, stay on the second ring.
        adj_count = 0
        for tt in ctiles:
            for dd in CARDINALS:
                nb = Position(tt.x + dd.delta()[0], tt.y + dd.delta()[1])
                try:
                    bid2 = ct.get_tile_builder_bot_id(nb)
                    if bid2 is not None and ct.get_team(bid2) == me and bid2 != ct.get_id():
                        adj_count += 1
                except Exception:
                    continue

        if ct.get_action_cooldown() == 0:
            # 1. HEAL THE CORE every round it is damaged (or just always —
            #    +4 HP for 1 Ti is the whole fixture).
            if adj_core and ct.get_global_resources() >= 1:
                try:
                    hurt = ct.get_hp(self._cid) < ct.get_max_hp(self._cid)
                except Exception:
                    hurt = True
                if hurt:
                    for t in adj_core:
                        try:
                            if ct.can_heal(t):
                                ct.heal(t)
                                return
                        except Exception:
                            continue
            # 2. BARRIER an empty neighbour tile (chip absorber / body block).
            if ct.get_global_resources() >= ct.get_barrier_cost() + 40:
                for d in CARDINALS:
                    t = p.add(d)
                    try:
                        if ct.can_build_barrier(t):
                            ct.build_barrier(t)
                            return
                    except Exception:
                        continue

        # 3. Not adjacent to the core yet: walk toward it, but STOP at the
        # second ring when 2 healers already hold seats (seat cap above).
        if not adj_core and ct.get_move_cooldown() == 0:
            if adj_count >= 2:
                near = min(abs(p.x - t.x) + abs(p.y - t.y) for t in ctiles)
                if near <= 2:
                    return          # hold the second ring, heal barriers from here
        if False and ct.get_move_cooldown() == 0:  # (structure keeper)
            pass
        elif not adj_core and ct.get_move_cooldown() == 0:
            tgt = ctiles[0]
            d = p.cardinal_direction_to(tgt)
            if d != Direction.CENTRE:
                try:
                    if ct.can_move(d):
                        ct.move(d)
                        return
                except Exception:
                    pass
            for d2 in CARDINALS:
                try:
                    if ct.can_move(d2):
                        ct.move(d2)
                        return
                except Exception:
                    continue
