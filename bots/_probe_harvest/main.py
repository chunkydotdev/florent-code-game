"""ENGINE PROBE — does `titanium_collected` count EMISSION or DELIVERY-TO-CORE?

WHY IT MATTERS. `titanium_collected` is the first tiebreak key and decides 94.1%
of our r1000 games, and a probe tonight established it EXCLUDES passive income —
so it is harvester output and nothing else. The open question is WHICH harvester
output: the stack the harvester emits, or the titanium that actually reaches the
core down a conveyor line.

The difference is load-bearing for a live analysis. If EMISSION counts, a
harvester is +10 on the key the instant it is built (first stack is immediate)
and a late bank-conversion into harvesters pays instantly. If DELIVERY counts,
a harvester with no route to the core is worth ZERO on the key forever, and any
"convert the bank at r999" arithmetic is a large overestimate.

THE DISCRIMINATOR. Build ONE harvester on an ore tile and NEVER build a single
conveyor or splitter. Nothing can carry a stack home. Then:

  * `titanium_collected > 0`  -> the key counts EMISSION.
  * `titanium_collected == 0` -> the key counts DELIVERY TO CORE.

The one confound is a harvester built orthogonally adjacent to the core, which
could hand off directly. So the probe REFUSES any ore tile within d^2 <= 8 of
our own core and prints the distance it used, rather than assuming.

    .venv/bin/fcode run bots/_probe_harvest bots/_probe_victim --tle 0 --json
"""
import sys

from fcode import Direction, EntityType, Environment

CARDS = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)


class Player:
    def run(self, ct) -> None:
        try:
            if ct.get_entity_type() == EntityType.CORE:
                self._core(ct)
            elif ct.get_entity_type() == EntityType.BUILDER_BOT:
                self._builder(ct)
        except Exception as exc:
            print(f"PROBE ERROR {type(exc).__name__}: {exc}", file=sys.stderr)

    def _core(self, ct) -> None:
        if getattr(self, "core_pos", None) is None:
            self.core_pos = ct.get_position()
        if ct.get_unit_count() >= 3 or ct.get_action_cooldown() != 0:
            return
        if ct.get_global_resources() < ct.get_builder_bot_cost():
            return
        p = ct.get_position()
        for d in Direction:
            if d != Direction.CENTRE and ct.can_spawn(p.add(d)):
                ct.spawn_builder(p.add(d))
                return

    def _builder(self, ct) -> None:
        if getattr(self, "built", False):
            return                      # exactly one harvester, then nothing
        rnd = ct.get_current_round()
        p = ct.get_position()
        core = getattr(self, "core_pos", None)

        if ct.get_action_cooldown() == 0:
            for d in CARDS:
                t = p.add(d)
                if ct.get_tile_env(t) != Environment.ORE_TITANIUM:
                    continue
                # Refuse a tile that could hand off to the core directly.
                if core is not None and t.distance_squared(core) <= 8:
                    print(f"HARVEST r={rnd} SKIP ore at ({t.x},{t.y}) "
                          f"d2_core={t.distance_squared(core)} <= 8",
                          file=sys.stderr)
                    continue
                if not ct.can_build_harvester(t):
                    continue
                ct.build_harvester(t)
                self.built = True
                d2 = t.distance_squared(core) if core else -1
                print(f"HARVEST r={rnd} BUILT at ({t.x},{t.y}) d2_core={d2} "
                      f"-- NO conveyor will ever be built", file=sys.stderr)
                return

        # Walk toward ore we can see, otherwise drift. Never build anything else.
        if ct.get_move_cooldown() != 0:
            return
        target = None
        for tile in ct.get_nearby_tiles():
            if ct.get_tile_env(tile) != Environment.ORE_TITANIUM:
                continue
            if core is not None and tile.distance_squared(core) <= 8:
                continue
            if target is None or p.distance_squared(tile) < p.distance_squared(target):
                target = tile
        if target is not None:
            step = p.cardinal_direction_to(target)
            if step != Direction.CENTRE and ct.can_move(step):
                ct.move(step)
                return
        for d in CARDS:
            if ct.can_move(d):
                ct.move(d)
                return
