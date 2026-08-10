import sys

from fcode import Controller, Direction, EntityType, Position


class Player:
    """Probe: what does can_fire_from ACTUALLY accept for a SENTINEL?

    Everything about sentinel aiming in this repo rests on an assumed predicate.
    raid.py builds only after can_fire_from passes, so its sentinels are
    shootable BY CONSTRUCTION -- yet an exact-ray decoder scored 287 of them
    0/287, which means the decoder's rule is not the engine's. This asks the
    engine directly instead of inferring.

    For a fixed origin and each of the 8 facings, enumerate every target within
    a generous box and record which are accepted. One turn, then silent.
    """

    done = False

    def run(self, ct: Controller) -> None:
        if Player.done:
            return
        Player.done = True
        try:
            p = ct.get_position()
            w, h = ct.get_map_width(), ct.get_map_height()
            for d in (Direction.NORTH, Direction.NORTHEAST, Direction.EAST):
                acc = []
                for dx in range(-7, 8):
                    for dy in range(-7, 8):
                        t = Position(p.x + dx, p.y + dy)
                        if not (0 <= t.x < w and 0 <= t.y < h):
                            continue
                        try:
                            if ct.can_fire_from(p, d, EntityType.SENTINEL, t):
                                acc.append((dx, dy, dx * dx + dy * dy))
                        except Exception:
                            pass
                print(file=sys.stderr, *[f"PROBE facing={d.name} origin=({p.x},{p.y}) "
                      f"accepted={sorted(acc, key=lambda a: a[2])}"])
        except Exception as exc:
            print(f"PROBE ERROR {type(exc).__name__}: {exc}", file=sys.stderr)
