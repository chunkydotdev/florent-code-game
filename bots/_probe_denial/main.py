"""PROBE: is ore-tile denial legal, and what does it cost the victim?

The trickster claim: a 3 Ti BARRIER placed on an ORE tile permanently denies a
20 Ti HARVESTER site, because harvesters may only be built on ore. If true this
is a ~7:1 exchange before you even count that destroy() is ALLIED-ONLY, so the
victim cannot remove it cheaply -- they must chew 30 HP at 2 dmg / 2 Ti, i.e.
15 attacks and 15 builder-turns, to clear 3 Ti of ours.

Asserting this from the rulebook is exactly the habit that produced the r180
error. So: ask the engine.

Q1 is_tile_empty() true on an ore tile?        (can we even target it)
Q2 can_build_barrier() true on an ore tile?
Q3 after the barrier stands, is can_build_harvester() there FALSE?
Q4 does can_build_harvester() come back TRUE after we destroy our own barrier?
    (proves the denial is the barrier, not some other gate)

stderr so it lands in the console rather than the replay.
"""
import sys

from fcode import Direction, Environment, EntityType

CARDINALS = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)


class Player:
    def __init__(self):
        self.spawned = False
        self.done = False
        self.blocked = None

    def run(self, ct) -> None:
        try:
            self._turn(ct)
        except Exception as exc:  # noqa: BLE001 - probe must never die
            print(f"DENIAL-ERR {type(exc).__name__}: {exc}", file=sys.stderr)

    def _turn(self, ct) -> None:
        kind = ct.get_entity_type()
        if kind == EntityType.CORE:
            if not self.spawned and ct.get_action_cooldown() == 0:
                for d in Direction:
                    if d == Direction.CENTRE:
                        continue
                    t = ct.get_position().add(d)
                    if ct.can_spawn(t):
                        ct.spawn_builder(t)
                        self.spawned = True
                        return
            return
        if kind != EntityType.BUILDER_BOT or self.done:
            return

        pos = ct.get_position()

        # Stage 2: the barrier from last round should now be standing.
        if self.blocked is not None:
            harv_after = ct.can_build_harvester(self.blocked)
            bid = ct.get_tile_building_id(self.blocked)
            print(
                f"DENIAL Q3 barrier_stands={bid is not None} "
                f"can_build_harvester_AFTER={harv_after}",
                file=sys.stderr,
            )
            if bid is not None and ct.can_destroy(self.blocked):
                ct.destroy(self.blocked)
                print(
                    f"DENIAL Q4 destroyed_own_barrier -> "
                    f"can_build_harvester_RESTORED={ct.can_build_harvester(self.blocked)}",
                    file=sys.stderr,
                )
            self.done = True
            return

        # Stage 1: find an adjacent ore tile and try to deny it.
        for d in CARDINALS:
            t = pos.add(d)
            if ct.get_tile_env(t) != Environment.ORE_TITANIUM:
                continue
            print(
                f"DENIAL Q1 ore tile {t.x},{t.y}  is_tile_empty={ct.is_tile_empty(t)}  "
                f"can_build_harvester_BEFORE={ct.can_build_harvester(t)}  "
                f"Q2 can_build_barrier={ct.can_build_barrier(t)}  "
                f"barrier_cost={ct.get_barrier_cost()} harvester_cost={ct.get_harvester_cost()}",
                file=sys.stderr,
            )
            if ct.can_build_barrier(t):
                ct.build_barrier(t)
                self.blocked = t
            else:
                self.done = True
            return

        # No adjacent ore: walk toward the nearest ore we can see.
        target = None
        for tile in ct.get_nearby_tiles():
            if ct.get_tile_env(tile) == Environment.ORE_TITANIUM:
                if target is None or pos.distance_squared(tile) < pos.distance_squared(target):
                    target = tile
        if target is not None and ct.get_move_cooldown() == 0:
            d = pos.cardinal_direction_to(target)
            if d != Direction.CENTRE and ct.can_move(d):
                ct.move(d)
