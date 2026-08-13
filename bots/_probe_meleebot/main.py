"""PROBE MELEEBOT — answers, on the live engine, whether a builder bot's
melee attack (can_fire/fire at an orthogonally-adjacent tile) can damage an
ENEMY BUILDER BOT, which is a UNIT and not a building.

CLAUDE.md contradicts itself: one sentence says the attack deals "2 dmg to
the building on an orthogonally adjacent tile", another says builder bots
"share can_fire/fire for their orthogonally-adjacent-tile attack" (the same
call turrets use, which is not building-restricted). This bot settles it
empirically against a live opponent (_probe_sitter), with a mandatory
positive control: the same can_fire/fire sequence against an adjacent enemy
BUILDING (in practice, the enemy CORE, since the sitter never builds
anything) proves the harness can observe a hit at all.

Every round that a builder bot is orthogonally adjacent to an enemy builder
bot or an enemy building, it logs to stderr:
  round, target kind, target id, HP before, can_fire() result,
  whether fire() raised, HP after (or DEAD if the target no longer exists).

Everything is wrapped in try/except: an escaping exception permanently
destroys the unit (per CLAUDE.md) and would silently ruin the probe.
"""
import sys

from fcode import Controller, Direction, EntityType, Position

CARDINALS = (Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST)
MAX_SPAWNS = 3


class Player:
    spawned = 0

    def run(self, ct: Controller) -> None:
        try:
            kind = ct.get_entity_type()
            if kind == EntityType.CORE:
                self._core_turn(ct)
            elif kind == EntityType.BUILDER_BOT:
                self._builder_turn(ct)
        except Exception:
            import traceback
            traceback.print_exc(file=sys.stderr)

    def _core_turn(self, ct: Controller) -> None:
        if Player.spawned >= MAX_SPAWNS:
            return
        if ct.get_action_cooldown() != 0:
            return
        if ct.get_global_resources() < ct.get_builder_bot_cost():
            return
        p = ct.get_position()
        for d in Direction:
            if d == Direction.CENTRE:
                continue
            t = p.add(d)
            if ct.can_spawn(t):
                ct.spawn_builder(t)
                Player.spawned += 1
                return

    def _builder_turn(self, ct: Controller) -> None:
        me = ct.get_team()
        p = ct.get_position()

        # 1. PRIMARY QUESTION: an adjacent enemy BUILDER BOT (a unit).
        for d in CARDINALS:
            t = p.add(d)
            try:
                bid = ct.get_tile_builder_bot_id(t)
            except Exception:
                continue
            if bid is None:
                continue
            try:
                if ct.get_team(bid) != me:
                    self._probe_target(ct, t, bid, "BUILDER_BOT(unit)")
                    return
            except Exception:
                continue

        # 2. POSITIVE CONTROL: an adjacent enemy BUILDING (e.g. their core).
        for d in CARDINALS:
            t = p.add(d)
            try:
                bldg = ct.get_tile_building_id(t)
            except Exception:
                continue
            if bldg is None:
                continue
            try:
                if ct.get_team(bldg) != me:
                    kind = ct.get_entity_type(bldg)
                    self._probe_target(ct, t, bldg, f"BUILDING:{kind.name}")
                    return
            except Exception:
                continue

        # 3. Nothing adjacent to shoot at -- move toward the nearest visible
        # enemy unit, else a spotted enemy building, else the heuristic
        # mirror point (maps are symmetric by reflection/rotation).
        if ct.get_move_cooldown() != 0:
            return
        target = self._find_target(ct, me)
        d = p.cardinal_direction_to(target)
        if d != Direction.CENTRE:
            try:
                if ct.can_move(d):
                    ct.move(d)
                    return
            except Exception:
                pass
        for alt in CARDINALS:
            try:
                if ct.can_move(alt):
                    ct.move(alt)
                    return
            except Exception:
                continue

    def _probe_target(self, ct: Controller, pos: Position, target_id: int, kind: str) -> None:
        if ct.get_action_cooldown() != 0:
            print(
                f"PROBE r={ct.get_current_round()} kind={kind} id={target_id} "
                f"SKIPPED action_cooldown!=0",
                file=sys.stderr,
            )
            return
        hp_before = self._safe_hp(ct, target_id)
        try:
            can = ct.can_fire(pos)
        except Exception as exc:
            print(
                f"PROBE r={ct.get_current_round()} kind={kind} id={target_id} "
                f"hp_before={hp_before} can_fire_RAISED={type(exc).__name__}: {exc}",
                file=sys.stderr,
            )
            return
        raised = False
        err = None
        if can:
            try:
                ct.fire(pos)
            except Exception as exc:
                raised = True
                err = f"{type(exc).__name__}: {exc}"
        hp_after = self._safe_hp(ct, target_id)
        print(
            f"PROBE r={ct.get_current_round()} kind={kind} id={target_id} "
            f"hp_before={hp_before} can_fire={can} fire_raised={raised} "
            f"err={err} hp_after={hp_after}",
            file=sys.stderr,
        )

    def _safe_hp(self, ct: Controller, entity_id: int):
        try:
            return ct.get_hp(entity_id)
        except Exception:
            return "DEAD_OR_GONE"

    # Cache: unit id -> fixed heuristic mirror-point target, computed ONCE
    # from this unit's SPAWN position. Recomputing "mirror of current
    # position" every round makes the target chase the mover itself: moving
    # east shifts the mirror target west by the same amount, so the bot
    # oscillates forever around the map's centre instead of converging.
    home_targets = {}

    def _find_target(self, ct: Controller, me) -> Position:
        try:
            for uid in ct.get_nearby_units():
                if ct.get_team(uid) != me and ct.get_entity_type(uid) == EntityType.BUILDER_BOT:
                    return ct.get_position(uid)
        except Exception:
            pass
        try:
            for bid in ct.get_nearby_buildings():
                if ct.get_team(bid) != me and ct.get_entity_type(bid) == EntityType.CORE:
                    return ct.get_position(bid)
        except Exception:
            pass
        uid = ct.get_id()
        cached = Player.home_targets.get(uid)
        if cached is not None:
            return cached
        p = ct.get_position()
        mw, mh = ct.get_map_width(), ct.get_map_height()
        target = Position(mw - 1 - p.x, mh - 1 - p.y)
        Player.home_targets[uid] = target
        return target
