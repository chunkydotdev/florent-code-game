"""ENGINE PROBE — how many facings does `can_fire_from` permit for one target?

WHY. LOKI-9 pre-registered a treatment that REORDERS the facing search inside
the existing gate: "among facings the gate already permits, prefer the one
pointing at the enemy core". A 960-game paired battery returned facing outcomes
that were IDENTICAL to the digit — 1,197 home turrets, 546 aligned, both arms.

The prereg's third falsifier branch says: when facing does not move, do NOT
conclude the diff is broken; find out whether the gate ever permitted the
preferred facing. This is that check, and the hypothesis is sharper than
"rarely permitted" — it is that **the permitted set is a SINGLETON**.

A gunner's shot is a straight line and a sentinel's is a single-tile-wide line
ignoring obstacles. For one specific target tile, at most one of eight compass
facings puts that tile on the ray. If that is right, then `can_fire_from(bp, f,
kind, threat)` is true for exactly one `f`, and reordering a one-element list is
a NO-OP BY CONSTRUCTION — no diff, however correct, could have moved the metric.

WHAT IT PRINTS. For the calling unit's own adjacent build sites and every
visible enemy entity as the target: how many of the 8 facings the gate permits.
The distribution of that count is the whole answer.

    .venv/bin/fcode run bots/_probe_facing bots/_probe_victim --tle 0
"""
import sys

from fcode import Direction, EntityType, Position

DIRS = [d for d in Direction if d != Direction.CENTRE]
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
        if ct.get_unit_count() >= 4 or ct.get_action_cooldown() != 0:
            return
        if ct.get_global_resources() < ct.get_builder_bot_cost():
            return
        p = ct.get_position()
        for d in Direction:
            if d != Direction.CENTRE and ct.can_spawn(p.add(d)):
                ct.spawn_builder(p.add(d))
                return

    def _builder(self, ct) -> None:
        rnd = ct.get_current_round()
        if getattr(self, 'done', False) or rnd < 3:
            return
        me = ct.get_team()
        p = ct.get_position()

        # `can_fire_from` is HYPOTHETICAL — it ignores ammo and cooldown and
        # takes any Position — so the geometry question needs no real enemy.
        # Probe a spread of offsets covering on-axis, on-diagonal and generic.
        offsets = [(3, 0), (0, 3), (4, 4), (3, 1), (5, 2), (2, 5), (1, 4),
                   (-3, 0), (0, -4), (-2, -5), (4, -3), (-4, 2)]
        w, h = ct.get_map_width(), ct.get_map_height()
        for kind in (EntityType.SENTINEL, EntityType.GUNNER):
            bp = p.add(Direction.NORTH)
            for dx, dy in offsets:
                tx, ty = bp.x + dx, bp.y + dy
                if not (0 <= tx < w and 0 <= ty < h):
                    continue
                tgt = Position(tx, ty)
                ok = []
                for f in DIRS:
                    try:
                        if ct.can_fire_from(bp, f, kind, tgt):
                            ok.append(f.name)
                    except Exception:
                        continue
                print(f"FACING kind={kind.name:<8} off=({dx},{dy}) "
                      f"permitted={len(ok)}/8 {','.join(ok) if ok else '-'}",
                      file=sys.stderr)
        self.done = True
