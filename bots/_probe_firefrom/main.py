import sys

from fcode import Controller, Direction, EntityType, Position


ALL_DIRS = (Direction.NORTH, Direction.NORTHEAST, Direction.EAST, Direction.SOUTHEAST,
            Direction.SOUTH, Direction.SOUTHWEST, Direction.WEST, Direction.NORTHWEST)


class Player:
    """Probe: what does can_fire_from ACTUALLY accept for a SENTINEL?

    Extended 2026-08-11 (docs/research/AUDIT-loki17-decoder-and-primary-2026-08-11.md,
    Finding Q4) from the original 3-facing version. The original sampled only
    (NORTH, NORTHEAST, EAST) -- one eighth of the compass, all in the same
    quadrant -- to certify a predicate whose only known failure mode
    (loki17_mech.py's DELTA-table bug, c91c078) is EXACTLY a one-compass-step
    rotation. Sampling one eighth of the compass to certify all of it was an
    assumption wearing a measurement's clothes. This version covers all 8.

    PART A (unchanged in method, extended in coverage): for a fixed origin
    (whichever unit runs first -- the core at round 0) and each of the 8
    facings, enumerate every target within a generous box and record which
    can_fire_from(SENTINEL) accepts.

    PART B (new): does an intervening entity on the ray change the verdict?
    Amendment 1g limit 1 in docs/prereg/PREREG-loki17-sentinel-siting-2026-08-10.md
    is still open: "Sentinel shots ignore obstacles [per CLAUDE.md], but the
    engine was not read to rule out a further predicate (minimum range,
    first-entity stop). If one exists, TRUE is still an upper bound by an
    unmeasured amount." CLAUDE.md is the organisers' doc and known-wrong in
    places, so this asks the engine directly: a builder bot settles on a
    clear tile, the NORTH ray is probed with can_fire_from at d=1..5 while
    empty, a real barrier is built at d=1 (on the ray, well inside range),
    then the same ray is re-probed. A verdict that changes at d>=2 shows the
    engine's own can_fire_from predicate checks for obstruction; unchanged
    confirms "ignores obstacles" holds for at least the legality check.
    """

    logged_a = False
    builder_id = None
    origin_b = None
    phase_b = 0        # 0=not started, 1=pre-block captured, 2=blocker built, 3=done
    pre_block = None

    def run(self, ct: Controller) -> None:
        try:
            kind = ct.get_entity_type()
            if kind == EntityType.CORE:
                self._core_turn(ct)
            elif kind == EntityType.BUILDER_BOT:
                self._builder_turn(ct)
        except Exception as exc:
            print(f"PROBE ERROR {type(exc).__name__}: {exc}", file=sys.stderr)

    def _core_turn(self, ct: Controller) -> None:
        if not Player.logged_a:
            Player.logged_a = True
            p = ct.get_position()
            w, h = ct.get_map_width(), ct.get_map_height()
            for d in ALL_DIRS:
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
                print(f"PROBE-A facing={d.name} origin=({p.x},{p.y}) "
                      f"accepted={sorted(acc, key=lambda a: a[2])}", file=sys.stderr)
        # Spawn a builder EAST of the core for PART B -- a column offset from
        # the core's own footprint, so a north/south ray from it never
        # re-enters the core and PART B is not confounded by our own building.
        if Player.builder_id is None:
            if ct.get_action_cooldown() == 0:
                tried = []
                for d in (Direction.EAST, Direction.WEST, Direction.NORTHEAST,
                          Direction.NORTHWEST, Direction.SOUTHEAST, Direction.SOUTHWEST,
                          Direction.NORTH, Direction.SOUTH):
                    target = ct.get_position().add(d)
                    ok = ct.can_spawn(target)
                    tried.append((d.name, ok))
                    if ok:
                        Player.builder_id = ct.spawn_builder(target)
                        print(f"PROBE-B spawned builder id={Player.builder_id} "
                              f"dir={d.name} at round {ct.get_current_round()}",
                              file=sys.stderr)
                        break
                if Player.builder_id is None:
                    print(f"PROBE-B spawn FAILED round={ct.get_current_round()} "
                          f"tried={tried}", file=sys.stderr)
            else:
                print(f"PROBE-B core action_cooldown={ct.get_action_cooldown()} "
                      f"round={ct.get_current_round()}", file=sys.stderr)

    def _builder_turn(self, ct: Controller) -> None:
        # NOTE: does not gate on Player.builder_id -- empirically (2026-08-11,
        # this probe) class-level "shared" state does NOT cross entities in
        # this engine. `_core_turn`'s `logged_a` flag persists fine across
        # ROUNDS because each unit appears to get its own persistent
        # execution context for its whole lifetime, but the CORE's write to
        # `Player.builder_id` is invisible from the BUILDER's own context --
        # exactly why CLAUDE.md's read_store/write_store exists as the only
        # real cross-unit channel. Harmless here: we only ever spawn one
        # builder, so "I am a BUILDER_BOT" (already dispatched on above) is
        # sufficient identification.
        if Player.origin_b is None:
            Player.origin_b = ct.get_position()
        p = Player.origin_b
        if ct.get_position() != p:
            return  # stay put; only act from the fixed PART B origin

        w, h = ct.get_map_width(), ct.get_map_height()

        if Player.phase_b == 0:
            if ct.get_action_cooldown() != 0:
                return
            acc = []
            for k in range(1, 6):
                t = Position(p.x, p.y - k)
                if not (0 <= t.x < w and 0 <= t.y < h):
                    acc.append((k, "offmap"))
                    continue
                try:
                    ok = ct.can_fire_from(p, Direction.NORTH, EntityType.SENTINEL, t)
                except Exception as exc:
                    ok = f"ERR:{type(exc).__name__}"
                acc.append((k, ok))
            Player.pre_block = acc
            Player.phase_b = 1
            print(f"PROBE-B pre-blocker  origin=({p.x},{p.y}) north-ray(d,accepted)={acc}",
                  file=sys.stderr)
            return

        if Player.phase_b == 1:
            if ct.get_action_cooldown() != 0:
                return
            blocker_pos = Position(p.x, p.y - 1)
            if ct.can_build_barrier(blocker_pos):
                ct.build_barrier(blocker_pos)
                Player.phase_b = 2
            else:
                print(f"PROBE-B cannot build blocker at ({blocker_pos.x},{blocker_pos.y}) "
                      f"-- tile occupied or illegal", file=sys.stderr)
                Player.phase_b = 3  # abandon PART B rather than loop forever
            return

        if Player.phase_b == 2:
            # One settling round after the build so the placement is reflected
            # in board state before re-querying can_fire_from.
            acc = []
            for k in range(1, 6):
                t = Position(p.x, p.y - k)
                if not (0 <= t.x < w and 0 <= t.y < h):
                    acc.append((k, "offmap"))
                    continue
                try:
                    ok = ct.can_fire_from(p, Direction.NORTH, EntityType.SENTINEL, t)
                except Exception as exc:
                    ok = f"ERR:{type(exc).__name__}"
                acc.append((k, ok))
            print(f"PROBE-B post-blocker origin=({p.x},{p.y}) north-ray(d,accepted)={acc} "
                  f"pre-blocker-was={Player.pre_block}", file=sys.stderr)
            Player.phase_b = 3
            return
        # phase_b == 3: done, stay silent.
