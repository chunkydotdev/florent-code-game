"""Mechanics probe: does destroy() consume the builder's act-or-move?

Sequence on one builder, all in ONE turn once two conveyors stand adjacent:
destroy #1 -> destroy #2 (unlimited-per-turn claim) -> build (does an action
remain?) -> move (mutual exclusion check). Cooldowns logged before/after each
step to stderr. Everything wrapped so no exception ever kills the unit.
"""
import sys

from fcode import Controller, Direction, EntityType

CARD = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)


def log(msg):
    print(msg, file=sys.stderr, flush=True)


class Player:
    def run(self, ct):
        try:
            self._run(ct)
        except Exception as e:
            log(f"PROBE-EXC {type(e).__name__}: {e}")

    def _run(self, ct):
        kind = ct.get_entity_type()
        rnd = ct.get_current_round()
        if kind == EntityType.CORE:
            if ct.get_action_cooldown() == 0:
                for d in Direction:
                    if d == Direction.CENTRE:
                        continue
                    t = ct.get_position().add(d)
                    if ct.can_spawn(t):
                        ct.spawn_builder(t)
                        return
            return
        if kind != EntityType.BUILDER_BOT:
            return
        if not hasattr(self, "phase"):
            self.phase, self.targets, self.done = 0, [], False
        if self.done:
            return
        p = ct.get_position()

        if self.phase < 2:
            # Build two adjacent conveyors over two turns.
            if ct.get_action_cooldown() == 0:
                for d in CARD:
                    t = p.add(d)
                    if t not in self.targets and ct.can_build_conveyor(t, Direction.NORTH):
                        ct.build_conveyor(t, Direction.NORTH)
                        self.targets.append(t)
                        self.phase += 1
                        log(f"r{rnd} SETUP built conveyor #{self.phase} at {t}")
                        return
            return

        # Test turn: need clean cooldowns and both conveyors still adjacent.
        if ct.get_action_cooldown() != 0 or ct.get_move_cooldown() != 0:
            return
        c1, c2 = self.targets
        if not (ct.can_destroy(c1) and ct.can_destroy(c2)):
            log(f"r{rnd} TEST-ABORT cannot destroy both targets")
            self.done = True
            return
        log(f"r{rnd} PRE   acd=0 mcd=0 can_move={sum(ct.can_move(d) for d in CARD)}")
        ct.destroy(c1)
        log(
            f"r{rnd} D1    acd={ct.get_action_cooldown()} mcd={ct.get_move_cooldown()}"
            f" can_move={sum(ct.can_move(d) for d in CARD)} can_destroy2={ct.can_destroy(c2)}"
        )
        ct.destroy(c2)
        log(
            f"r{rnd} D2    acd={ct.get_action_cooldown()} mcd={ct.get_move_cooldown()}"
            f" can_move={sum(ct.can_move(d) for d in CARD)}"
            f" can_build={ct.can_build_conveyor(c1, Direction.NORTH)}"
        )
        try:
            ct.build_conveyor(c1, Direction.NORTH)
            log(
                f"r{rnd} BUILD OK -> destroy does NOT consume the action."
                f" acd={ct.get_action_cooldown()} mcd={ct.get_move_cooldown()}"
                f" can_move={sum(ct.can_move(d) for d in CARD)}"
            )
        except Exception as e:
            log(f"r{rnd} BUILD RAISED {type(e).__name__}: {e} -> destroy consumed the action")
        moved = False
        for d in CARD:
            if ct.can_move(d):
                try:
                    ct.move(d)
                    moved = True
                    log(f"r{rnd} MOVE OK after destroy+build -> move budget untouched")
                    break
                except Exception as e:
                    log(f"r{rnd} MOVE RAISED {type(e).__name__}: {e}")
                    break
        if not moved:
            log(f"r{rnd} MOVE unavailable after destroy(+build) (can_move all False)")
        self.done = True
        log(f"r{rnd} TEST COMPLETE")
