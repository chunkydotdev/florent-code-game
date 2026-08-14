"""Side-aware, terrain-only deterministic opening router.

The seven experts differ only in spawn-order salt.  Selection uses public map
terrain and the bot's own core position; it never reads opponent identity.
"""

from fcode import EntityType

import p92h_doctrine as map_doctrine
import p92h_eco as map_eco
import p07router
import p22router
import p24router
import p25router
import p37router
import p85router
import p92router
import counter_main
import dirty_main
import j3_main
import rush_main


ROUTERS = {
    "07": p07router.Player,
    "22": p22router.Player,
    "24": p24router.Player,
    "25": p25router.Player,
    "37": p37router.Player,
    "85": p85router.Player,
    "92": p92router.Player,
}

OPENINGS = {
    "antler":       {"A": "25", "B": "85"},
    "archipelago":  {"A": "07", "B": "24"},
    "drakkarfjord": {"A": "24", "B": "25"},
    "drumlin":      {"A": "25", "B": "24"},
    "fjordgate":    {"A": "37", "B": "37"},
    "frostgate":    {"A": "37", "B": "85"},
    "glacierkeep":  {"A": "37", "B": "07"},
    "icefloe":      {"A": "92", "B": "22"},
    "midgard":      {"A": "92", "B": "24"},
    "nordkap":      {"A": "85", "B": "24"},
    "ragnarok":     {"A": "85", "B": "37"},
    "royale":       {"A": "85", "B": "37"},
    "valkyrie":     {"A": "24", "B": "24"},
    "yulerune":     {"A": "24", "B": "92"},
}

SIGNATURES = {
    (14, 18, ((6, 4), (6, 12))): "antler",
    (26, 26, ((5, 5), (19, 19))): "archipelago",
    (30, 30, ((2, 24), (26, 4))): "drakkarfjord",
    (25, 25, ((5, 5), (18, 18))): "drumlin",
    (10, 10, ((2, 2), (6, 6))): "fjordgate",
    (30, 30, ((14, 2), (14, 26))): "glacierkeep",
    (20, 20, ((1, 16), (17, 2))): "icefloe",
    (20, 26, ((9, 6), (9, 18))): "nordkap",
    (20, 20, ((9, 2), (9, 16))): "royale",
    (30, 30, ((2, 14), (26, 14))): "valkyrie",
}

A_CORES = {
    "antler": (6, 4), "archipelago": (5, 5),
    "drakkarfjord": (2, 24), "drumlin": (5, 5),
    "fjordgate": (2, 2), "frostgate": (2, 9),
    "glacierkeep": (14, 2), "icefloe": (1, 16),
    "midgard": (2, 2), "nordkap": (9, 6),
    "ragnarok": (2, 2), "royale": (9, 16),
    "valkyrie": (2, 14), "yulerune": (2, 9),
}

COUNTER_ROUTES = {
    ("antler", "B"), ("archipelago", "B"), ("fjordgate", "B"),
    ("icefloe", "A"), ("nordkap", "B"),
}
DIRTY_ROUTES = {
    ("drumlin", "B"), ("glacierkeep", "B"), ("nordkap", "A"),
}
RUSH_ROUTES = {
    ("drakkarfjord", "A"), ("drakkarfjord", "B"), ("ragnarok", "A"),
}
J3_ROUTES = {("yulerune", "A")}


def _decode_grid(w, h, code):
    cells = []
    for ch in code:
        value = map_doctrine.MAP_ALPHABET.index(ch)
        for _ in range(3):
            cells.append(value % 3)
            value //= 3
    cells = cells[: w * h]
    return tuple(
        "".join(".#o"[cells[y * w + x]] for x in range(w))
        for y in range(h)
    )


COLLISION_GRIDS = {}
for _key, _code in map_doctrine.EXTRA_MAP_CODES:
    if _key == (20, 20, 2, 9, 16, 9):
        if _code.startswith("NBAAAMNN"):
            COLLISION_GRIDS[_decode_grid(20, 20, _code)] = "frostgate"
        elif _code.startswith("AAAAAAAAAAAAAACAY"):
            COLLISION_GRIDS[_decode_grid(20, 20, _code)] = "yulerune"
    elif _key == (30, 30, 2, 2, 26, 26):
        if _code.startswith("AAAAAAAAAAAAAAAAAAAAAAC"):
            COLLISION_GRIDS[_decode_grid(30, 30, _code)] = "midgard"
        elif _code.startswith("AAAAAAAAAAAAAAAAAAAAAAO"):
            COLLISION_GRIDS[_decode_grid(30, 30, _code)] = "ragnarok"


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
        enemy = map_eco.unpack_pos(ct.read_store(map_doctrine.SLOT_ENEMY_CORE))
        if enemy is not None:
            return map_eco.enemy_core_for(
                ct.get_map_width(), ct.get_map_height(), enemy
            )
        return None

    def run(self, ct):
        if self.inner is None:
            core = self._own_core(ct)
            if core is None:
                self.inner = p92router.Player()
            else:
                w, h = ct.get_map_width(), ct.get_map_height()
                enemy = map_eco.enemy_core_for(w, h, core)
                pair = tuple(sorted(((core.x, core.y), (enemy.x, enemy.y))))
                label = SIGNATURES.get((w, h, pair))
                if label is None:
                    grid = map_eco.known_map_for(w, h, core, ct)
                    label = COLLISION_GRIDS.get(grid)
                side = "A" if label and (core.x, core.y) == A_CORES[label] else "B"
                route = (label, side)
                if route in COUNTER_ROUTES:
                    self.inner = counter_main.Player()
                elif route in DIRTY_ROUTES:
                    self.inner = dirty_main.Player()
                elif route in RUSH_ROUTES:
                    self.inner = rush_main.Player()
                elif route in J3_ROUTES:
                    self.inner = j3_main.Player()
                else:
                    salt = OPENINGS.get(label, {}).get(side, "92")
                    self.inner = ROUTERS[salt]()
        self.inner.run(ct)
