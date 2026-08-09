"""ENGINE PROBE — does destroy() refund the cost scale in the SAME round?

WHY. `bots/_probe_scale` established that the cost scale is ONE GLOBAL ADDITIVE
team factor, so every live entity inflates every subsequent build of every type.
The organisers' rule also says the scale "decreases again when an entity is
destroyed". `destroy()` is free, has no cooldown and is unlimited per turn.

That combination implies an unused lever: DEMOLISH BEFORE YOU BUILD. If the
refund lands within the same turn, a builder can destroy a spent structure and
buy its replacement at the lower scale in that same run() call — and because the
factor is GLOBAL, the discount applies to every build in that window, not just
to the replacement. The research arm flagged this and correctly refused to price
it before the timing was probed.

It matters that this is unused rather than merely unmeasured: `_v124loki8`, the
live ladder holder, contains ZERO calls to `ct.destroy()` or `ct.self_destruct()`.

THE DISCRIMINATOR. One builder, one allied barrier, three readings in a single
turn: costs BEFORE destroy, costs AFTER destroy, same run() call. Then the
following round's reading shows whether a next-round refund happened instead.

  * SAME-ROUND refund -> the AFTER column drops immediately.
  * NEXT-ROUND refund -> AFTER == BEFORE, and the drop shows up one round later.
  * NO refund         -> neither.

Scale is first inflated with builder bots (+20% each) so the barrier's +1% step
is not swallowed by floor(): at scale 2.0, removing 1% of a 30-base sentinel is
worth a whole titanium, whereas at scale 1.0 it is worth nothing observable.
That is the same trap `_probe_scale` had to design around.

    .venv/bin/fcode run bots/_probe_refund bots/_probe_victim --tle 0
"""
import sys

from fcode import Controller, Direction, EntityType


def _costs(ct: Controller) -> dict:
    return {
        "conveyor": ct.get_conveyor_cost(), "harvester": ct.get_harvester_cost(),
        "gunner": ct.get_gunner_cost(), "sentinel": ct.get_sentinel_cost(),
        "builder": ct.get_builder_bot_cost(),
    }


def _fmt(c: dict) -> str:
    return " ".join(f"{k}={v}" for k, v in c.items())


class Player:
    def run(self, ct: Controller) -> None:
        try:
            if ct.get_entity_type() == EntityType.CORE:
                self._core(ct)
            elif ct.get_entity_type() == EntityType.BUILDER_BOT:
                self._builder(ct)
        except Exception as exc:
            print(f"PROBE ERROR {type(exc).__name__}: {exc}", file=sys.stderr)

    def _core(self, ct: Controller) -> None:
        # Inflate the scale with builder bots so a +1% barrier step is visible.
        if ct.get_unit_count() >= 6 or ct.get_action_cooldown() != 0:
            return
        if ct.get_global_resources() < ct.get_builder_bot_cost():
            return
        pos = ct.get_position()
        for d in Direction:
            if d != Direction.CENTRE and ct.can_spawn(pos.add(d)):
                ct.spawn_builder(pos.add(d))
                return

    def _builder(self, ct: Controller) -> None:
        rnd = ct.get_current_round()
        if rnd < 6 or ct.get_action_cooldown() != 0:
            return
        pos = ct.get_position()
        cards = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)

        # If one of our barriers is adjacent, do the three-reading experiment.
        for d in cards:
            t = pos.add(d)
            bid = ct.get_tile_building_id(t)
            if bid is None or ct.get_team(bid) != ct.get_team():
                continue
            if ct.get_entity_type(bid) != EntityType.BARRIER:
                continue
            if not ct.can_destroy(t):
                continue
            before, scale_b = _costs(ct), ct.get_scale_percent()
            ct.destroy(t)
            after, scale_a = _costs(ct), ct.get_scale_percent()
            print(f"REFUND r={rnd} SCALE {scale_b:.3f} -> {scale_a:.3f} "
                  f"{'SAME-ROUND' if scale_a != scale_b else 'NO CHANGE THIS ROUND'}",
                  file=sys.stderr)
            print(f"REFUND r={rnd} BEFORE {_fmt(before)}", file=sys.stderr)
            print(f"REFUND r={rnd} AFTER  {_fmt(after)}", file=sys.stderr)
            return

        # Otherwise put one barrier down so the next round has something to test.
        for d in cards:
            t = pos.add(d)
            if ct.can_build_barrier(t):
                s = ct.get_scale_percent()
                ct.build_barrier(t)
                print(f"REFUND r={rnd} built barrier, scale {s:.3f} -> "
                      f"{ct.get_scale_percent():.3f}  {_fmt(_costs(ct))}",
                      file=sys.stderr)
                return
