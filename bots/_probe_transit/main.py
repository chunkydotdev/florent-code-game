"""ENGINE PROBE — how fast does a stack travel a conveyor line?

WHY. `titanium_collected` counts DELIVERY TO THE CORE, not emission (probed
tonight). That turns "when is a harvester too late to score before r1000?" into
a real question, and the answer depends entirely on transit rate. The primary
says only "Resource distribution happens once at end of round" and never states
a rate. Two readings, differing by an order of magnitude:

  * ONE TILE PER ROUND      -> transit ~ path length in rounds. A harvester
                               built late cannot land, and a LEAD-TIME DISARM
                               ("stop building routes after round X") is a real
                               and DERIVABLE lever.
  * WHOLE LINE PER STEP     -> transit is a couple of rounds regardless of
                               length. The lever is worthless.

THE DISCRIMINATOR, and it needs no timing arithmetic. Watch the stack ITSELF.
`get_stored_resource_id(id)` returns the stack a conveyor is holding. Build a
straight line of conveyors into the core, feed it from one harvester, and print
which conveyor holds which stack id every round. A stack that appears on
conveyor 1, then 2, then 3 on consecutive rounds is one tile per round. A stack
that is never observed on an intermediate conveyor traverses in one step.

Reading the OCCUPANCY PATTERN rather than a delivery timestamp also dodges the
passive-income confound: passive adds +10 to the balance every 4 rounds and
would otherwise be indistinguishable from an arrival.

    .venv/bin/fcode run bots/_probe_transit bots/_probe_victim --tle 0
"""
import sys

from fcode import Direction, EntityType, Environment, Position

CARDS = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)


class Player:
    def run(self, ct) -> None:
        try:
            k = ct.get_entity_type()
            if k == EntityType.CORE:
                self._core(ct)
            elif k == EntityType.BUILDER_BOT:
                self._builder(ct)
        except Exception as exc:
            print(f"PROBE ERROR {type(exc).__name__}: {exc}", file=sys.stderr)

    # ---- core: spawn one builder, then just WATCH the line every round -------
    def _core(self, ct) -> None:
        # Per-unit run() does NOT share instance state across units in this
        # engine -- a sibling probe printed d2_core=-1 all game because the
        # builder never saw a value the core had set on `self`. The comm store
        # is the supported channel; writes land next round.
        cp = ct.get_position()
        if ct.read_store(0) == 0:
            ct.write_store(0, cp.x * 1000 + cp.y)
        rnd = ct.get_current_round()

        chain = []
        for bid in ct.get_nearby_buildings():
            try:
                if ct.get_team(bid) != ct.get_team():
                    continue
                if ct.get_entity_type(bid) != EntityType.CONVEYOR:
                    continue
                pos = ct.get_position(bid)
                sid = ct.get_stored_resource_id(bid)
                chain.append((pos.x, pos.y, sid))
            except Exception:
                continue
        if chain:
            chain.sort()
            occupied = [f"({x},{y})={sid}" for x, y, sid in chain if sid is not None]
            if occupied or rnd % 25 == 0:
                print(f"TRANSIT r={rnd:<4} ti={ct.get_global_resources():<5} "
                      f"conveyors={len(chain)} holding=[{' '.join(occupied)}]",
                      file=sys.stderr)

        if ct.get_unit_count() >= 2 or ct.get_action_cooldown() != 0:
            return
        if ct.get_global_resources() < ct.get_builder_bot_cost():
            return
        p = ct.get_position()
        for d in Direction:
            if d != Direction.CENTRE and ct.can_spawn(p.add(d)):
                ct.spawn_builder(p.add(d))
                return

    # ---- builder: harvester on ore, then a conveyor line back to the core ----
    def _builder(self, ct) -> None:
        if ct.get_action_cooldown() != 0:
            return
        p = ct.get_position()
        packed = ct.read_store(0)
        if packed == 0:
            return
        core = Position(packed // 1000, packed % 1000)

        if not getattr(self, "harv", False):
            for d in CARDS:
                t = p.add(d)
                if (ct.get_tile_env(t) == Environment.ORE_TITANIUM
                        and ct.can_build_harvester(t)):
                    ct.build_harvester(t)
                    self.harv = True
                    self.hpos = t
                    ct.write_store(1, t.x * 1000 + t.y)
                    print(f"TRANSIT r={ct.get_current_round()} harvester at "
                          f"({t.x},{t.y}) d2_core={t.distance_squared(core)}",
                          file=sys.stderr)
                    return
            # walk to ore
            best = None
            for tile in ct.get_nearby_tiles():
                if ct.get_tile_env(tile) != Environment.ORE_TITANIUM:
                    continue
                if best is None or p.distance_squared(tile) < p.distance_squared(best):
                    best = tile
            if best is not None and ct.get_move_cooldown() == 0:
                step = p.cardinal_direction_to(best)
                if step != Direction.CENTRE and ct.can_move(step):
                    ct.move(step)
            return

        # Lay a CHAIN anchored to the harvester. Store slot 1 holds the last
        # laid tile; the next conveyor must be orthogonally adjacent to it (or
        # to the harvester on the first link), otherwise the "chain" is a
        # scattering of disconnected conveyors that never carry anything --
        # which is exactly what the first cut of this probe produced.
        anchor_packed = ct.read_store(1)
        anchor = (Position(anchor_packed // 1000, anchor_packed % 1000)
                  if anchor_packed else getattr(self, "hpos", None))
        if anchor is None:
            return
        # The core is 2x2 and `core` is only its anchor tile. Stopping at
        # d^2 <= 2 stops DIAGONALLY adjacent, where the conveyor's output tile
        # is empty and the stack sits on it forever -- observed: stack id 11
        # parked on (7,3) from r5 to r1000 with collected = 0. Terminate only
        # when orthogonally adjacent to a FOOTPRINT tile, and face that tile.
        ctiles = [Position(core.x + dx, core.y + dy)
                  for dx in (0, 1) for dy in (0, 1)]
        if min(anchor.distance_squared(c) for c in ctiles) <= 1:
            return                                   # chain reaches the core
        best = None
        for d in CARDS:
            t = anchor.add(d)
            if (min(t.distance_squared(c) for c in ctiles)
                    >= min(anchor.distance_squared(c) for c in ctiles)):
                continue
            near = min(ctiles, key=lambda c: t.distance_squared(c))
            face = t.cardinal_direction_to(near)
            if face == Direction.CENTRE:
                continue
            if p.distance_squared(t) != 1:
                continue                             # must be adjacent to US
            if ct.can_build_conveyor(t, face):
                best = (t, face)
                break
        if best is not None:
            t, face = best
            ct.build_conveyor(t, face)
            ct.write_store(1, t.x * 1000 + t.y)
            print(f"TRANSIT r={ct.get_current_round()} conveyor ({t.x},{t.y}) "
                  f"face={face.name} d2_core={t.distance_squared(core)}",
                  file=sys.stderr)
            return
        if ct.get_move_cooldown() == 0:
            step = p.cardinal_direction_to(anchor if p.distance_squared(anchor) > 2
                                           else core)
            if step != Direction.CENTRE and ct.can_move(step):
                ct.move(step)
