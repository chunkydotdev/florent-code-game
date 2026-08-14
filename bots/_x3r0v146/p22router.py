"""Official-map mixture of experts: v135 generally, v134 on preregistered weak maps.

The router uses terrain only.  It does not inspect or identify the opponent.
Each policy has isolated modules so its doctrine globals cannot contaminate the
other policy inside a unit subinterpreter.
"""

from fcode import EntityType

import p22h_doctrine
import p22h_eco
import p22h_main
import p22i_main


WEAK_KEYS = {
    (25, 25, 5, 5, 18, 18),   # drumlin
    (20, 26, 2, 2, 2, 22),    # nordkap
    (30, 30, 14, 2, 14, 26),  # glacierkeep
}


def _decode_grid(w, h, code):
    cells = []
    for ch in code:
        value = p22h_doctrine.MAP_ALPHABET.index(ch)
        for _ in range(3):
            cells.append(value % 3)
            value //= 3
    cells = cells[: w * h]
    return tuple(
        "".join(".#o"[cells[y * w + x]] for x in range(w))
        for y in range(h)
    )


def _weak_grids():
    grids = set()
    for key, code in p22h_doctrine.MAP_CODES.items():
        if key in WEAK_KEYS:
            grids.add(_decode_grid(key[0], key[1], code))
    for key, code in p22h_doctrine.EXTRA_MAP_CODES:
        if key in WEAK_KEYS:
            grids.add(_decode_grid(key[0], key[1], code))
        # yulerune shares dimensions and anchors with frostgate; its encoded
        # terrain has this stable prefix in the official map table.
        if key == (20, 20, 2, 9, 16, 9) and code.startswith("AAAAAAAAAAAAAACAY"):
            grids.add(_decode_grid(key[0], key[1], code))
    return frozenset(grids)


WEAK_GRIDS = _weak_grids()


class Player:
    def __init__(self):
        self.inner = None

    def _own_core(self, ct):
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
        enemy = p22h_eco.unpack_pos(ct.read_store(p22h_doctrine.SLOT_ENEMY_CORE))
        if enemy is not None:
            return p22h_eco.enemy_core_for(ct.get_map_width(), ct.get_map_height(), enemy)
        return None

    def run(self, ct):
        if self.inner is None:
            core = self._own_core(ct)
            if core is None:
                # The first builders always see home; this fallback mainly
                # protects an exotic engine ordering and stays on v135.
                self.inner = p22h_main.Player()
            else:
                grid = p22h_eco.known_map_for(
                    ct.get_map_width(), ct.get_map_height(), core, ct
                )
                self.inner = p22i_main.Player() if grid in WEAK_GRIDS else p22h_main.Player()
        self.inner.run(ct)
