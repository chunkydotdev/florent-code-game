"""Repeated-screen terrain/side mixture for the supplied top-team map pool."""

from fcode import EntityType

import base_router
import cr_router
import d6_main
import fc_main
import gu_main
import la_main
import lc_main
import p92router
import se_main
import t130_main


# Entries are based on three fresh seeds per orientation (six games/map).
WEAK_EXPERTS = {
    "antler":       {"A": fc_main.Player,   "B": cr_router.Player},
    "drakkarfjord": {"A": t130_main.Player, "B": la_main.Player},
    "drumlin":      {"A": p92router.Player, "B": p92router.Player},
    "frostgate":    {"A": lc_main.Player,   "B": fc_main.Player},
    "midgard":      {"A": gu_main.Player,   "B": fc_main.Player},
    "nordkap":      {"A": d6_main.Player,   "B": fc_main.Player},
    "ragnarok":     {"A": se_main.Player,   "B": cr_router.Player},
    "royale":       {"A": se_main.Player,   "B": base_router.Player},
    "yulerune":     {"A": d6_main.Player,   "B": la_main.Player},
}


class Player:
    def __init__(self):
        self.inner = None

    @staticmethod
    def _own_core(ct):
        if ct.get_entity_type() == EntityType.CORE:
            return ct.get_position()
        team = ct.get_team()
        for entity_id in ct.get_nearby_buildings():
            try:
                if (ct.get_entity_type(entity_id) == EntityType.CORE
                        and ct.get_team(entity_id) == team):
                    return ct.get_position(entity_id)
            except Exception:
                continue
        enemy = base_router.map_eco.unpack_pos(
            ct.read_store(base_router.map_doctrine.SLOT_ENEMY_CORE)
        )
        if enemy is not None:
            return base_router.map_eco.enemy_core_for(
                ct.get_map_width(), ct.get_map_height(), enemy
            )
        return None

    def run(self, ct):
        if self.inner is None:
            core = self._own_core(ct)
            if core is None:
                self.inner = base_router.Player()
            else:
                w, h = ct.get_map_width(), ct.get_map_height()
                enemy = base_router.map_eco.enemy_core_for(w, h, core)
                pair = tuple(sorted(((core.x, core.y), (enemy.x, enemy.y))))
                label = base_router.SIGNATURES.get((w, h, pair))
                if label is None:
                    grid = base_router.map_eco.known_map_for(w, h, core, ct)
                    label = base_router.COLLISION_GRIDS.get(grid)
                side = (
                    "A" if label
                    and (core.x, core.y) == base_router.A_CORES[label]
                    else "B"
                )
                policy = WEAK_EXPERTS.get(label, {}).get(side, base_router.Player)
                self.inner = policy()
        self.inner.run(ct)

