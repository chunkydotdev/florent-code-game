"""PROBE: does cost scale track LIVE entities or CUMULATIVE builds?

The whole LOKI-2 doctrine rests on the answer. Our docs assert "LIVE"
(game-model.md:357-358) and an older note asserted "CUMULATIVE" (+201% from 201
conveyor builds). Those cannot both be true, and a doc is not a measurement.

Method: one builder bot builds conveyors as fast as it can, logging
get_scale_percent() and get_conveyor_cost() each round. At PHASE_B it destroys
them again, logging the same two numbers.

  LIVE      => scale falls back down as we destroy
  CUMULATIVE=> scale stays at its high-water mark

Output goes to stderr so it lands in the console rather than the replay.
"""
import sys

from fcode import Direction, EntityType

PHASE_B = 60          # start destroying here
CARDINALS = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)


class Player:
    def __init__(self):
        self.built = []
        self.spawned = False

    def run(self, ct) -> None:
        # A raise inside run() permanently destroys the unit, which would end
        # the probe silently. Everything is wrapped.
        try:
            self._turn(ct)
        except Exception as exc:  # noqa: BLE001 - probe must never die
            print(f"PROBE-ERR {type(exc).__name__}: {exc}", file=sys.stderr)

    def _turn(self, ct) -> None:
        kind = ct.get_entity_type()
        rnd = ct.get_current_round()

        if kind == EntityType.CORE:
            if not self.spawned and ct.get_action_cooldown() == 0:
                for d in Direction:
                    if d == Direction.CENTRE:
                        continue
                    tgt = ct.get_position().add(d)
                    if ct.can_spawn(tgt):
                        ct.spawn_builder(tgt)
                        self.spawned = True
                        return
            return

        if kind != EntityType.BUILDER_BOT:
            return

        if ct.get_team(ct.get_id()) is None:
            return

        # One line per round: the two numbers that settle the question.
        # Log one getter per CATEGORY. If scale is per-category, only the
        # conveyor price may move as we build conveyors. If it is a single
        # global multiplier, every one of these moves together.
        print(
            f"PROBE rnd={rnd} live_built={len(self.built)} "
            f"scale={ct.get_scale_percent():.3f} conv={ct.get_conveyor_cost()} "
            f"harv={ct.get_harvester_cost()} gun={ct.get_gunner_cost()} "
            f"sent={ct.get_sentinel_cost()} bot={ct.get_builder_bot_cost()} "
            f"launch={ct.get_launcher_cost()}",
            file=sys.stderr,
        )

        if rnd < PHASE_B:
            self._build(ct)
        else:
            self._destroy(ct)

    def _build(self, ct) -> None:
        if ct.get_action_cooldown() != 0:
            return
        pos = ct.get_position()
        for d in CARDINALS:
            tgt = pos.add(d)
            if ct.can_build_conveyor(tgt, Direction.NORTH):
                ct.build_conveyor(tgt, Direction.NORTH)
                self.built.append(tgt)
                return
        # Boxed in by our own conveyors: step somewhere new.
        if ct.get_move_cooldown() == 0:
            for d in CARDINALS:
                if ct.can_move(d):
                    ct.move(d)
                    return

    def _destroy(self, ct) -> None:
        # destroy() is free and unlimited per turn, so tear down everything
        # reachable this round and let the next log line show the effect.
        for tgt in list(self.built):
            if ct.can_destroy(tgt):
                ct.destroy(tgt)
                self.built.remove(tgt)
        if ct.get_move_cooldown() == 0 and self.built:
            for d in CARDINALS:
                if ct.can_move(d):
                    ct.move(d)
                    return
