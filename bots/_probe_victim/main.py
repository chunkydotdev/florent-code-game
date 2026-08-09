"""PROBE VICTIM — reports, every round, whether its own 12 spawn-ring tiles are
still legal spawn targets, and what is standing on them.

THE QUESTION. LOKI-2's ring wants to occupy the 12 tiles adjacent to the enemy
2x2 core with OUR OWN BODIES. s22's `_probe_prison` refuted the BARRIER form
(build legality is stricter than is_tile_empty, and parking a friendly builder
on a ring tile defends it for free). Body-occupation by an ENEMY builder was
never tested, and the answer decides everything:

  can_spawn False on an enemy-occupied tile -> the ring is a SPAWN-LOCK (a kill)
  can_spawn True                            -> the ring is only a HEAL-LOCK

This bot NEVER SPAWNS and never moves, so the only thing that can ever occupy
its ring is the opponent. Output goes to stderr, which `fcode run` captures and
`print()` does not (print is swallowed into the replay).
"""
import sys

from fcode import Controller, EntityType, Position


class Player:
    def run(self, ct: Controller) -> None:
        try:
            self._go(ct)
        except Exception:
            import traceback
            traceback.print_exc(file=sys.stderr)

    def _go(self, ct: Controller) -> None:
        if ct.get_entity_type() != EntityType.CORE:
            return
        p = ct.get_position()
        mw, mh = ct.get_map_width(), ct.get_map_height()
        foot = {(p.x + dx, p.y + dy) for dx in (0, 1) for dy in (0, 1)}
        ring = [
            Position(x, y)
            for x in range(p.x - 1, p.x + 3)
            for y in range(p.y - 1, p.y + 3)
            if (x, y) not in foot and 0 <= x < mw and 0 <= y < mh
        ]
        # REPORT BEFORE SPAWNING. can_spawn() is False for EVERY tile once the
        # action cooldown is non-zero, so a report taken after this turn's
        # spawn reads legal=0 everywhere and says nothing about occupancy.
        # First version of this probe made exactly that mistake.
        ready = ct.get_action_cooldown() == 0
        me = ct.get_team()
        legal = enemy_bodies = own_bodies = buildings = 0
        detail = []
        for t in ring:
            ok = ready and ct.can_spawn(t)
            legal += ok
            bid = ct.get_tile_builder_bot_id(t)
            occ = "."
            if bid is not None:
                if ct.get_team(bid) == me:
                    own_bodies += 1
                    occ = "o"
                else:
                    enemy_bodies += 1
                    occ = "E"
            elif ct.get_tile_building_id(t) is not None:
                buildings += 1
                occ = "#"
            detail.append(f"{occ}{'+' if ok else '-'}")
        print(
            f"PROBE r={ct.get_current_round()} ready={int(ready)} legal={legal} "
            f"enemy_bodies={enemy_bodies} own={own_bodies} bldg={buildings} "
            f"| {' '.join(detail)}",
            file=sys.stderr,
        )
        if ready and ct.get_global_resources() >= ct.get_builder_bot_cost():
            for t in ring:
                if ct.can_spawn(t):
                    ct.spawn_builder(t)
                    return
