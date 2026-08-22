# In-game Florent Code League engine probe: does a BARRIER occlude a GUNNER ray?
# Layout (all ours): gunner at G=(bx+1,y) facing EAST; conveyor at G+2E; then
# barrier at G+1E (between). get_gunner_target() = "nearest targetable tile in
# the facing line": if it moves from conveyor-tile to barrier-tile after the
# barrier lands, the barrier occludes/pre-empts the ray (protection works).
import sys
from fcode import Controller, Direction, EntityType, Position

class Player:
    def __init__(self):
        self.state = 0
        self.gunpos = None

    def run(self, ct: Controller) -> None:
        kind = ct.get_entity_type()
        rnd = ct.get_current_round()
        try:
            if kind == EntityType.CORE:
                if rnd == 0:
                    for d in Direction:
                        if d == Direction.CENTRE: continue
                        t = ct.get_position().add(d)
                        if ct.can_spawn(t):
                            ct.spawn_builder(t); return
            elif kind == EntityType.BUILDER_BOT:
                p = ct.get_position()
                mv = ct.get_move_cooldown() == 0
                act = ct.get_action_cooldown() == 0
                print(f"PROBE r{rnd} builder state={self.state} at ({p.x},{p.y}) mv={mv} act={act}", file=sys.stderr)
                if self.state == 0 and act:
                    e = p.add(Direction.EAST)
                    if ct.can_build_gunner(e, Direction.EAST):
                        self.gunpos = e
                        ct.build_gunner(e, Direction.EAST)
                        print(f"PROBE r{rnd} GUN at ({e.x},{e.y}) facing E", file=sys.stderr)
                        self.state = 1
                    elif mv and ct.can_move(Direction.SOUTH):
                        ct.move(Direction.SOUTH)
                elif self.state == 1 and mv and ct.can_move(Direction.NORTH):
                    ct.move(Direction.NORTH); self.state = 2
                elif self.state == 2 and mv and ct.can_move(Direction.EAST):
                    ct.move(Direction.EAST); self.state = 3
                elif self.state == 3 and mv and ct.can_move(Direction.EAST):
                    ct.move(Direction.EAST); self.state = 35
                elif self.state == 35 and mv and ct.can_move(Direction.EAST):
                    ct.move(Direction.EAST); self.state = 4
                elif self.state == 4 and act:
                    c = Position(self.gunpos.x + 2, self.gunpos.y)
                    if ct.can_build_conveyor(c, Direction.EAST):
                        ct.build_conveyor(c, Direction.EAST)
                        print(f"PROBE r{rnd} CONVEYOR at ({c.x},{c.y}) = G+2E", file=sys.stderr)
                        self.state = 5
                elif self.state == 5 and mv and ct.can_move(Direction.WEST):
                    ct.move(Direction.WEST); self.state = 6
                elif self.state == 6 and act:
                    b = Position(self.gunpos.x + 1, self.gunpos.y)
                    if ct.can_build_barrier(b):
                        ct.build_barrier(b)
                        print(f"PROBE r{rnd} BARRIER at ({b.x},{b.y}) = G+1E BETWEEN", file=sys.stderr)
                        self.state = 7
            elif kind == EntityType.GUNNER:
                try:
                    t = ct.get_gunner_target()
                    print(f"PROBE r{rnd} target={None if t is None else (t.x,t.y)}", file=sys.stderr)
                except Exception as e:
                    print(f"PROBE r{rnd} target raised {e}", file=sys.stderr)
        except Exception as e:
            print(f"PROBE swallow r{rnd}: {e}", file=sys.stderr)
