"""PROBE (s25, builder): does can_fire_from / can_fire accept an EMPTY tile?

THE QUESTION AND WHY IT DECIDES A PLANK. LOKI-3's throw scorer gives a bonus
to throw destinations that stand on one of OUR OWN live turret lines, so that
a kidnapped enemy builder lands somewhere we already shoot. The scorer must
evaluate that BEFORE the throw -- i.e. while the destination tile is still
EMPTY. If the engine's fire predicates require an occupant, every such tile
answers False, the bonus set is empty in every position, and the plank does
nothing at all while looking perfectly healthy. That is a silent failure and
no arena battery would ever name it.

Two sub-questions, both answered by the same print:
  1. can_fire_from(gunner_pos, facing, GUNNER, T) for T empty and on the ray.
  2. Whether a gunner's ray is truly prefix-blocked -- research's claim, from
     official-docs.md:440 ("Closest targetable tile in a Gunner's facing line")
     plus an s23 engine probe. If so, an empty tile BEHIND a closer occupied
     tile must answer False even though it is geometrically on the line.

CONTROL, so the answer cannot be a coincidence of one tile: the same three
predicates are printed for a SENTINEL, whose line ignores obstacles by spec.
If the gunner and sentinel disagree exactly where blocking predicts, the
mechanism is confirmed rather than assumed.

Output is stderr (console-only, not replay-captured) and deliberately
one-line-per-tile so it can be read without a decoder.
"""
import sys

from fcode import Controller, Direction, EntityType, Position


class Player:
    def __init__(self):
        self.done = set()

    def run(self, ct: Controller) -> None:
        try:
            self._run(ct)
        except Exception as exc:  # never let the probe kill its own unit
            print(f"PROBE-ERR {exc!r}", file=sys.stderr)

    def _run(self, ct: Controller) -> None:
        kind = ct.get_entity_type()
        rnd = ct.get_current_round()
        if kind == EntityType.CORE:
            self._core(ct, rnd)
        elif kind == EntityType.BUILDER_BOT:
            self._builder(ct, rnd)
        elif kind in (EntityType.GUNNER, EntityType.SENTINEL):
            self._turret(ct, rnd, kind)

    def _core(self, ct, rnd):
        if ct.get_global_ammo() < 40 and ct.can_convert_ammo(20):
            ct.convert_ammo(20)
        if ct.get_action_cooldown() != 0 or rnd > 6:
            return
        for d in Direction:
            if d == Direction.CENTRE:
                continue
            t = ct.get_position().add(d)
            if ct.can_spawn(t):
                ct.spawn_builder(t)
                return

    def _builder(self, ct, rnd):
        """Plant one gunner and one sentinel, both facing EAST, then a barrier
        two tiles east of the gunner so the BLOCKING half of the probe has a
        blocker to be blocked by."""
        if ct.get_action_cooldown() != 0:
            return
        p = ct.get_position()
        for d in (Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST):
            t = p.add(d)
            if "gun" not in self.done:
                if ct.can_build_gunner(t, Direction.EAST):
                    ct.build_gunner(t, Direction.EAST)
                    self.done.add("gun")
                    print(f"PROBE built GUNNER at {t} facing EAST", file=sys.stderr)
                    return
            elif "sent" not in self.done:
                if ct.can_build_sentinel(t, Direction.EAST):
                    ct.build_sentinel(t, Direction.EAST)
                    self.done.add("sent")
                    print(f"PROBE built SENTINEL at {t} facing EAST", file=sys.stderr)
                    return
        if ct.get_move_cooldown() == 0:
            for d in (Direction.SOUTH, Direction.EAST):
                if ct.can_move(d):
                    ct.move(d)
                    return

    def _turret(self, ct, rnd, kind):
        # Print once, a few rounds in, so the board has settled.
        key = f"{kind}-{ct.get_id()}"
        if rnd < 12 or key in self.done:
            return
        self.done.add(key)
        p = ct.get_position()
        facing = ct.get_direction()
        name = "GUNNER" if kind == EntityType.GUNNER else "SENTINEL"
        print(f"\nPROBE {name} id={ct.get_id()} at {p} facing {facing} "
              f"ammo={ct.get_global_ammo()} rnd={rnd}", file=sys.stderr)
        tiles = ct.get_attackable_tiles()
        print(f"PROBE   get_attackable_tiles -> {len(tiles)} tiles", file=sys.stderr)
        # Walk the facing line outward so "prefix" is meaningful in the output.
        dx, dy = facing.delta()
        for step in range(1, 7):
            t = Position(p.x + dx * step, p.y + dy * step)
            if not (0 <= t.x < ct.get_map_width() and 0 <= t.y < ct.get_map_height()):
                break
            try:
                empty = ct.is_tile_empty(t)
            except Exception:
                empty = "?"
            bid = ct.get_tile_building_id(t)
            bot = ct.get_tile_builder_bot_id(t)
            occ = "EMPTY" if (bid is None and bot is None) else (
                f"bld={bid}" if bid is not None else f"bot={bot}")
            try:
                cff = ct.can_fire_from(p, facing, kind, t)
            except Exception as e:
                cff = f"RAISED {e!r}"
            try:
                cf = ct.can_fire(t)
            except Exception as e:
                cf = f"RAISED {e!r}"
            inpat = any(x.x == t.x and x.y == t.y for x in tiles)
            print(f"PROBE   step={step} {t} {occ:<10} empty={empty} "
                  f"in_pattern={inpat} can_fire_from={cff} can_fire={cf}",
                  file=sys.stderr)
        if kind == EntityType.GUNNER:
            try:
                print(f"PROBE   get_gunner_target -> {ct.get_gunner_target()}",
                      file=sys.stderr)
            except Exception as e:
                print(f"PROBE   get_gunner_target RAISED {e!r}", file=sys.stderr)
