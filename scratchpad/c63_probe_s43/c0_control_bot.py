"""C0 CONTROL for DESIGN-63 §4 -- scratchpad probe, never in bots/.

Drives the falsifier the design puts first:
  "two builder bots ordered onto one tile; assert the second can_move is False"

It also drives the OTHER verdict in the same round, which is what makes the
check a check: for the same prober bot, in the same turn, we log can_move()
toward the anchor's OCCUPIED tile *and* toward a verified-EMPTY adjacent tile.
A guard that only ever prints False validates nothing.

Output (stderr, local only):
  C0|rnd|prober|anchor_dir|cm_occupied|cm_empty|passable_occupied
"""
import sys

from fcode import Direction, EntityType, Position

CARDS = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)


class Player:
    def __init__(self):
        self.role = None

    def run(self, ct):
        try:
            self._go(ct)
        except Exception:
            import traceback
            traceback.print_exc(file=sys.stderr)

    def _go(self, ct):
        t = ct.get_entity_type()
        if t == EntityType.CORE:
            return self._core(ct)
        if t == EntityType.BUILDER_BOT:
            return self._bot(ct)

    def _core(self, ct):
        # exactly two builder bots, then nothing else, ever
        if ct.get_unit_count() >= 3 or ct.get_action_cooldown() != 0:
            return
        p = ct.get_position()
        for d in Direction:
            if d == Direction.CENTRE:
                continue
            tgt = p.add(d)
            if ct.can_spawn(tgt):
                ct.spawn_builder(tgt)
                return

    def _bot(self, ct):
        me = ct.get_id()
        p = ct.get_position()
        mates = []
        for uid in ct.get_nearby_units():
            if uid == me:
                continue
            try:
                if ct.get_team(uid) == ct.get_team() and \
                        ct.get_entity_type(uid) == EntityType.BUILDER_BOT:
                    mates.append(uid)
            except Exception:
                continue
        if not mates:
            return
        anchor = min(mates + [me])
        if anchor == me:
            return                      # the anchor never moves
        ap = ct.get_position(anchor)
        d = abs(ap.x - p.x) + abs(ap.y - p.y)
        if d != 1:
            if ct.get_move_cooldown() != 0:
                return
            step = p.cardinal_direction_to(ap)
            for cand in (step,) + CARDS:
                if cand in CARDS and ct.can_move(cand):
                    ct.move(cand)
                    return
            return
        # ---- adjacent: the measurement -----------------------------------
        toward = p.cardinal_direction_to(ap)
        cm_occ = ct.can_move(toward)
        pass_occ = ct.is_tile_passable(ap)
        cm_emp = None
        for cand in CARDS:
            if cand == toward:
                continue
            n = p.add(cand)
            if not (0 <= n.x < ct.get_map_width() and 0 <= n.y < ct.get_map_height()):
                continue
            try:
                if ct.is_tile_empty(n) and ct.get_tile_builder_bot_id(n) is None:
                    cm_emp = ct.can_move(cand)
                    break
            except Exception:
                continue
        sys.stderr.write("C0|%d|%d|%s|%s|%s|%s\n" % (
            ct.get_current_round(), me, toward.name, cm_occ, cm_emp, pass_occ))
        # deliberately do NOT move: hold the pair adjacent for the whole game
