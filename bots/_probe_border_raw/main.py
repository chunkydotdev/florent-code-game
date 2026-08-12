"""QUEUE #17 victim probe — POSITION-SENSITIVE, unguarded neighbour query.

⛔ WHY THIS FILE HAD TO BE WRITTEN, AND IT IS A FIXTURE DEFECT IN QUEUE #17 AS
WRITTEN.  #17 nominates `bots/_probe_oov_raw` as the vulnerable target for the
border-throw crash cell.  It cannot serve: that probe queries
`Position(get_map_width() - 1, get_map_height() - 1)` — a FIXED far corner that
is IN BOUNDS and IDENTICAL no matter where the unit stands.  It is
POSITION-INVARIANT, so a throw to the border changes nothing about whether it
raises, and cells (a) and (c) of #17 would return the SAME answer by
construction.  A leg run on it would read "the weapon does not fire" while
never having tested the weapon.

THE MECHANISM WE ARE ACTUALLY TESTING (CLAUDE.md, engine-source-crash-and-
launcher-2026-08-10.md): our launcher throws an ENEMY builder to a legal
MAP-BORDER tile, where THAT BOT'S OWN CODE queries a neighbour OF ITS OWN
POSITION, that neighbour is off-map, `get_tile_env` raises, the raise escapes
`run()`, and the engine permanently destroys the unit (0x1ac5c ->
Game::destroy_entity).  The trigger is therefore a query RELATIVE TO SELF.
This probe is that, with no guard at all — the shape we believe most teams ship.

PAIRED CONTROL: `bots/_probe_border_guard` — byte-identical except the query is
wrapped.  It must survive the identical throw.  If both die, the cause is not
the unguarded query; if neither dies, the throw is not reaching the border.
"""
import sys

from fcode import Direction, EntityType, Position


class Player:
    def run(self, ct) -> None:
        kind = ct.get_entity_type()
        if kind == EntityType.CORE:
            try:
                if ct.get_action_cooldown() == 0 and ct.get_unit_count() < 8:
                    p = ct.get_position()
                    for d in Direction:
                        if d != Direction.CENTRE and ct.can_spawn(p.add(d)):
                            ct.spawn_builder(p.add(d))
                            return
            except Exception as exc:
                print(f"BRAW CORE ERR {exc}", file=sys.stderr)
            return
        if kind != EntityType.BUILDER_BOT:
            return
        # Builder: NO GUARD WHATSOEVER, and the query is relative to SELF.
        # On any interior tile all four cardinal neighbours are in bounds and
        # this is a no-op.  On a border tile at least one is off-map and
        # get_tile_env raises -> the raise escapes run() -> unit destroyed.
        p = ct.get_position()
        print(f"BRAW r={ct.get_current_round()} unit={ct.get_id()} "
              f"pos=({p.x},{p.y}) alive", file=sys.stderr)
        for d in (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST):
            ct.get_tile_env(p.add(d))
        # Then behave like an ordinary builder so the game is a real game --
        # BUT NEVER STEP ONTO A BORDER TILE OF ITS OWN ACCORD.
        # ⛔ THIS FILTER IS THE WHOLE FIXTURE AND IT IS NOT COSMETIC.  Without
        # it the probe walks to y=0 by itself and dies with no throw involved
        # (measured, seed 7001: crashed at pos=(20,0) on turn ~131, having
        # walked NORTH every round).  Cells (a) and (c) would then BOTH read
        # "crashes" and the leg would credit our launcher for suicide.
        # With it, an interior tile is always safe, so ANY border arrival is
        # attributable to our throw and to nothing else.
        if ct.get_move_cooldown() == 0:
            w, h = ct.get_map_width(), ct.get_map_height()
            for d in (Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST):
                t = p.add(d)
                if t.x <= 0 or t.y <= 0 or t.x >= w - 1 or t.y >= h - 1:
                    continue
                if ct.can_move(d):
                    ct.move(d)
                    return
