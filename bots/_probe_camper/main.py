"""PROBE CAMPER — a heal-camp fixture for QUEUE #48's park dose.

The sitter cannot reproduce the park: v125 kills it in r63-90 and the pinned
park definition needs >=100 idle rounds (measured 2026-08-13, 12/12 control
games, parks 0). This fixture stalls the kill the way the camp class does
(Leviathan/I Stone — the teams that park us hardest in research's #48 cut):
builders sit on the core and heal it every round (+4 HP per heal vs our
sentinel's 9 HP/round each), with a barrier ring for chip absorption.

FIXTURE, NOT AN ARM. Lie direction: it heals with perfect uptime and never
leaves home — it overstates the camp, which makes parks EASIER to reproduce.
Fine for a mechanism dose whose treatment claims to spend parked rounds; the
value read stays live vs the real camp class.
"""
import sys

from fcode import Controller, Direction, EntityType, Position

CARDINALS = (Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST)
MAX_BUILDERS = 6


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

        # 3. Not adjacent to the core yet: walk to it.
        if not adj_core and ct.get_move_cooldown() == 0:
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
