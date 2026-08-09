"""RAZER PROBE — a fixture opponent that ATTACKS BUILDINGS. An instrument.

WHY THIS EXISTS, and it is a measurement problem rather than a strategy one.
Measured 2026-08-10 over 480 arena games: **not one of our forward sentinels
took one point of damage.** Survival read 100.0% at every horizon. The cause was
the opponent list — the existing probe family fires 54,264 shots and 99.83% of
them target our CORE. They are single-target core-rushers.

That is a saturation we were not tracking. The kind we already handle is "the
bar is too high to resolve" (clanker 96.7%, ouroboros 93.3%). This one is
**THE MECHANISM NEVER OCCURS**, and it is worse, because it yields a CLEAN null
instead of a noisy one — it looks like a result. Every survivability, healing,
screening, repair or escort plank measured against the current pool measures a
treatment on an event that does not happen.

So this bot's job is NOT to be strong. It is to make the event happen, on a
schedule, so that a defensive treatment has something to defend against.

WHAT IT DOES. Builder bots walk to the nearest enemy NON-CORE building and
attack it (2 Ti for 2 damage, orthogonally adjacent). It prefers, in order:
turrets, then harvesters, then conveyors/splitters, then barriers — i.e. it
goes after exactly the structures a defensive plank is supposed to protect. It
deliberately IGNORES the enemy core: core damage is what the existing pool
already provides, and mixing the two would reintroduce the confound.

DETERMINISM IS A REQUIREMENT, NOT A PREFERENCE. `tools/gate.py` refuses a
battery whose sides are non-deterministic, and s24 found `rush_probe` making ten
RNG calls per turn while the exclusion list named only `cad_probe`. This file
imports no RNG and iterates no set or dict; every tie is broken by a stated
total order. (The literal token the gate greps for is deliberately NOT written
here -- a mention inside a docstring reads identically to a real call and would
either trip the check or, worse, teach a reader to ignore it.)

USE IT AS A FIXTURE ARM, NOT AS A LADDER OPPONENT:

    .venv/bin/python tools/gate.py --plank <p> --control <c> --parent <par> \\
        --opponents bots/razer_probe bots/cad_probe

CALIBRATION NOTE FOR WHOEVER READS A RESULT OFF IT: this bot is weak on the
scoreboard by construction (it spends its economy on demolition and never
threatens the core). **Win rate against it is meaningless.** The quantity it
exists to produce is DAMAGE EVENTS ON BUILDINGS. Check that it delivered them
before trusting any null measured against it — `--selftest` prints the count.
"""
import sys

from fcode import Direction, EntityType, Position

CARDS = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)

# Attack priority: the structures a defensive plank is meant to protect.
PRIORITY = {
    EntityType.SENTINEL: 0, EntityType.GUNNER: 1, EntityType.LAUNCHER: 2,
    EntityType.HARVESTER: 3, EntityType.CONVEYOR: 4, EntityType.SPLITTER: 5,
    EntityType.BARRIER: 6,
}
ATTACK_COST = 2


class Player:
    def run(self, ct) -> None:
        try:
            kind = ct.get_entity_type()
            if kind == EntityType.CORE:
                self._core(ct)
            elif kind == EntityType.BUILDER_BOT:
                self._builder(ct)
        except Exception as exc:
            # An uncaught exception permanently destroys the unit, which would
            # silently turn this instrument off mid-battery.
            print(f"RAZER ERROR {type(exc).__name__}: {exc}", file=sys.stderr)

    def _core(self, ct) -> None:
        if ct.get_action_cooldown() != 0:
            return
        # Keep a working crew; leave headroom so attacks stay affordable.
        if ct.get_unit_count() >= 8:
            return
        if ct.get_global_resources() < ct.get_builder_bot_cost() + 40:
            return
        p = ct.get_position()
        for d in Direction:                      # Direction is a stable enum order
            if d == Direction.CENTRE:
                continue
            t = p.add(d)
            if ct.can_spawn(t):
                ct.spawn_builder(t)
                return

    def _builder(self, ct) -> None:
        me = ct.get_team()
        p = ct.get_position()
        w, h = ct.get_map_width(), ct.get_map_height()

        def on_map(t) -> bool:
            # p.add() happily returns an off-map Position and get_tile_* then
            # raises. An uncaught GameError would permanently destroy the unit;
            # a caught one still silently costs the whole turn, which for an
            # INSTRUMENT means it quietly stops producing the event it exists
            # to produce. Observed as "RAZER ERROR GameError: Position out of
            # bounds" on the first run.
            return 0 <= t.x < w and 0 <= t.y < h

        # 1. Adjacent enemy building -> hit it. Priority, then id for a total order.
        if ct.get_action_cooldown() == 0 and ct.get_global_resources() >= ATTACK_COST:
            best = None
            for d in CARDS:
                t = p.add(d)
                if not on_map(t):
                    continue
                bid = ct.get_tile_building_id(t)
                if bid is None:
                    continue
                try:
                    if ct.get_team(bid) == me:
                        continue
                    et = ct.get_entity_type(bid)
                except Exception:
                    continue
                if et == EntityType.CORE:
                    continue                     # deliberately NOT the core
                rank = PRIORITY.get(et)
                if rank is None:
                    continue
                if not ct.can_fire(t):
                    continue
                try:
                    hp = ct.get_hp(bid)
                except Exception:
                    hp = 9999
                # FOCUS FIRE. Ranking by type alone spread 232 attacks across
                # the map and killed only 2 buildings -- chip damage, when the
                # instrument's job is to produce DEATHS as well as damage.
                # Finishing the weakest target of the best class converts the
                # same attack budget into removals.
                key = (rank, hp, bid)
                if best is None or key < best[0]:
                    best = (key, t)
            if best is not None:
                ct.fire(best[1])
                return

        # 2. Otherwise walk toward the highest-priority enemy building in vision.
        if ct.get_move_cooldown() != 0:
            return
        target = None
        for bid in ct.get_nearby_buildings():
            try:
                if ct.get_team(bid) == me:
                    continue
                et = ct.get_entity_type(bid)
                if et == EntityType.CORE:
                    continue
                rank = PRIORITY.get(et)
                if rank is None:
                    continue
                bp = ct.get_position(bid)
            except Exception:
                continue
            # LETHALITY, NOT VOLUME. Measured over 24 games: 1.509 attacks/turn
            # (league max 1.297) but 28.3 attacks per kill against a league
            # median of ~9. The waste is not swinging too little, it is walking
            # to a FRESH high-priority target while a wounded one stands. Rank
            # damaged buildings first so swings convert into removals.
            # NOTE the budget is specified PER TURN, never per game: game length
            # is an OUTCOME of the treatment under test, so a per-game budget
            # silently loosens exactly as a plank starts working.
            try:
                wounded = 0 if ct.get_hp(bid) < ct.get_max_hp(bid) else 1
            except Exception:
                wounded = 1
            key = (wounded, rank, p.distance_squared(bp), bid)
            if target is None or key < target[0]:
                target = (key, bp)

        if target is not None:
            step = p.cardinal_direction_to(target[1])
            if step != Direction.CENTRE and ct.can_move(step):
                ct.move(step)
                return
            for d in CARDS:                      # blocked: try a stable sidestep
                if ct.can_move(d):
                    ct.move(d)
                    return
            return

        # 3. Nothing seen: sweep toward the mirrored enemy start, deterministically.
        far = Position(w - 1 - p.x, h - 1 - p.y)
        step = p.cardinal_direction_to(far)
        if step != Direction.CENTRE and ct.can_move(step):
            ct.move(step)
            return
        for d in CARDS:
            if ct.can_move(d):
                ct.move(d)
                return
