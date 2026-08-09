"""PROBE: can a 3 Ti barrier be built ON TOP OF an enemy builder bot?

`is_tile_empty` is documented as "no building and is not a wall" -- a builder bot
is neither. If `can_build_barrier` inherits that definition literally, then a
3 Ti barrier can be dropped onto a 30 Ti enemy builder and, since barriers are
impassable, permanently imprison it. 10:1, and because it IMPRISONS rather than
kills it refunds none of their cost scale (scale tracks live entities).

This is an argument until it is a measurement, so: ask the engine.

Q1  is_tile_empty() on a tile holding an ENEMY builder?
Q2  can_build_barrier() on that tile?
Q3  does build_barrier() actually succeed, and is the victim still there after?
Q4  (separately) what is the real spawn ring? print can_spawn for every tile
    within d^2<=8 of the core, so the 12-tile d^2<=2 claim is checked against
    behaviour and not just against GameConstants.

Both teams run this file, so the two builders walk at each other and meet.
stderr, so it lands in the console rather than the replay.
"""
import sys

from fcode import Direction, EntityType, Position

CARDINALS = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)


class Player:
    def __init__(self):
        self.spawned = 0
        self.reported_ring = False
        self.done = False
        self.jailed = None

    def run(self, ct) -> None:
        try:
            self._turn(ct)
        except Exception as exc:  # noqa: BLE001 - a probe must never die
            print(f"PRISON-ERR {type(exc).__name__}: {exc}", file=sys.stderr)

    def _turn(self, ct) -> None:
        kind = ct.get_entity_type()
        if kind == EntityType.CORE:
            self._core(ct)
        elif kind == EntityType.BUILDER_BOT:
            self._builder(ct)

    def _core(self, ct) -> None:
        # Q4: map the real spawn ring by asking can_spawn, once.
        if not self.reported_ring:
            self.reported_ring = True
            c = ct.get_position()
            legal, illegal = [], []
            for dx in range(-3, 4):
                for dy in range(-3, 4):
                    t = Position(c.x + dx, c.y + dy)
                    if not (0 <= t.x < ct.get_map_width() and 0 <= t.y < ct.get_map_height()):
                        continue
                    try:
                        (legal if ct.can_spawn(t) else illegal).append((dx, dy))
                    except Exception:
                        illegal.append((dx, dy))
            print(f"PRISON Q4 core_at={c.x},{c.y} spawnable_offsets={sorted(legal)}",
                  file=sys.stderr)

        if self.spawned < 4 and ct.get_action_cooldown() == 0:
            for d in Direction:
                if d == Direction.CENTRE:
                    continue
                t = ct.get_position().add(d)
                if ct.can_spawn(t):
                    ct.spawn_builder(t)
                    self.spawned += 1
                    return

    def _builder(self, ct) -> None:
        if self.done:
            return
        pos = ct.get_position()
        me = ct.get_team()

        # Follow up on a successful jailing.
        if self.jailed is not None:
            occupant = ct.get_tile_builder_bot_id(self.jailed)
            bid = ct.get_tile_building_id(self.jailed)
            print(
                f"PRISON Q3b after_build barrier_present={bid is not None} "
                f"victim_still_on_tile={occupant is not None}",
                file=sys.stderr,
            )
            self.done = True
            return

        # Q1/Q2/Q3: any orthogonally adjacent builder bot, EITHER TEAM.
        # The mechanic under test is whether a BUILDER BOT makes a tile
        # non-empty / non-buildable at all; a friendly body answers that just
        # as well as an enemy one and is far easier to arrange. If a friendly
        # body does NOT block the build, the enemy case is the interesting one
        # and is worth a second run.
        for d in CARDINALS:
            t = pos.add(d)
            if not (0 <= t.x < ct.get_map_width() and 0 <= t.y < ct.get_map_height()):
                continue
            bot = ct.get_tile_builder_bot_id(t)
            if bot is None:
                continue
            same = ct.get_team(bot) == me
            print(f"PRISON contact tile={t.x},{t.y} friendly={same}", file=sys.stderr)
            empty = ct.is_tile_empty(t)
            can = ct.can_build_barrier(t)
            print(
                f"PRISON Q1 enemy_builder_at={t.x},{t.y} is_tile_empty={empty}  "
                f"Q2 can_build_barrier={can}  barrier_cost={ct.get_barrier_cost()}",
                file=sys.stderr,
            )
            if can and ct.get_action_cooldown() == 0:
                try:
                    ct.build_barrier(t)
                    print("PRISON Q3 build_barrier SUCCEEDED on an occupied tile",
                          file=sys.stderr)
                    self.jailed = t
                except Exception as exc:  # noqa: BLE001
                    print(f"PRISON Q3 build_barrier RAISED {type(exc).__name__}: {exc}",
                          file=sys.stderr)
                    self.done = True
            else:
                self.done = True
            return

        if ct.get_current_round() < 15:
            return

        # Home in on the nearest VISIBLE enemy builder (vision r^2=20) rather
        # than hoping we collide at the map centre -- three maps produced no
        # contact that way.
        target, best = None, None
        for eid in ct.get_nearby_units():
            try:
                if ct.get_entity_type(eid) != EntityType.BUILDER_BOT or ct.get_team(eid) == me:
                    continue
                tp = ct.get_position(eid)
            except Exception:
                continue
            dsq = pos.distance_squared(tp)
            if best is None or dsq < best:
                best, target = dsq, tp

        rnd = ct.get_current_round()
        if rnd % 25 == 0:
            print(
                f"PRISON hb rnd={rnd} me={pos.x},{pos.y} "
                f"enemy_visible={'yes @%d,%d dsq=%d' % (target.x, target.y, best) if target else 'no'}",
                file=sys.stderr,
            )

        if ct.get_move_cooldown() != 0:
            return
        goal = target if target is not None else Position(
            ct.get_map_width() // 2, ct.get_map_height() // 2
        )
        d = pos.cardinal_direction_to(goal)
        if d != Direction.CENTRE and ct.can_move(d):
            ct.move(d)
            return
        for d in CARDINALS:
            if ct.can_move(d):
                ct.move(d)
                return
