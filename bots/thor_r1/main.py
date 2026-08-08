"""THOR R1 — gunner rush. A SLOT CANDIDATE, not a sparring partner.

Named per the project convention (Thor was reserved for offence; this is the
first offensive bot the project has built).

WHY THIS EXISTS (2026-08-09, session 20). Our line is a ~5,000-line economic
grinder that is the most extreme outlier on the ladder: 50% core-kill at a
median of 982 turns, in a field where every other team runs 55-100% at 129-446.
`diverge` sits 87 rating points BELOW us and closes its games in 129 turns.

Research decoded 20 top-tier replays. On early-game events, which game length
cannot confound:

                    TOP TIER      US
    1st harvester       5          6
    1st conveyor        6          8
    1st GUNNER         19         53      <-- 34 rounds earlier
    1st sentinel       25         14
    launchers        0/20      69% of games
    harvesters @r150  3.0        5.0      <-- we out-economy them and lose

This bot is that build order, and nothing else. It is deliberately small (~300
lines against 5,077) because the whole point is to test a DOCTRINE, not to
accumulate clauses. If it needs a special case to beat a specific opponent,
that special case belongs in a different experiment.

HOW IT MUST BE JUDGED, and this is the part that matters:
  - It is a CANDIDATE for the slot. It competes against our eco line on the
    SAME vs-field battery, and whichever wins the field ships.
  - Head-to-head against our own eco bot is ATTRIBUTION ONLY, never a gate.
    Tuning either bot until it beats the other optimises against a replica we
    built ourselves. That is exactly how a 1,080-match battery returned p=1e-11
    on 2026-08-08 and was contradicted by the ladder inside an hour: every
    opponent in it was a replica we already beat 87-93%.
  - If this bot beats our eco line, the finding is "our defence has a hole the
    field is already through" — the response is to build an answer to early
    gunner pressure, NOT to add clause #109 that counters this specific opening.

DOCTRINE, in one line: three harvesters, then guns forward, and close the game
before the grind starts.
"""
from fcode import (
    Controller,
    Direction,
    EntityType,
    Environment,
    GameConstants,
    Position,
)

CARDINALS = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)
DIRECTIONS = [d for d in Direction if d != Direction.CENTRE]

# Top tier sits flat at ~3 harvesters from r50 to r150 while we grow to 5 and
# lose. Three is not a budget compromise, it is the measured number.
HARVESTER_TARGET = 3

# Their first gunner lands at round 19. Ours at 53. This bot stops economic
# work and starts military work the moment the harvester target is met.
GUN_PUSH_ROUND = 12

# A gunner costs 4 ammo per shot and there is no passive ammo income, so the
# core must convert titanium 1:1 or every gun we build is an ornament.
AMMO_FLOOR = 40
AMMO_CHUNK = 20

# Builders that push forward: the rest hold and feed economy.
RUSH_SHARE = 0.6

# Store slots (16 available, team-private, writes visible next round).
SLOT_HARVESTERS = 0
SLOT_GUNNERS = 1
SLOT_ENEMY_CORE_X = 2
SLOT_ENEMY_CORE_Y = 3


class Player:
    def __init__(self) -> None:
        self.enemy_core: Position | None = None
        self.own_core: Position | None = None
        self.role: int | None = None
        self.next_role = 0

    # ------------------------------------------------------------------ entry
    def run(self, ct: Controller) -> None:
        # An uncaught exception PERMANENTLY destroys the unit for the rest of
        # the match, so nothing is allowed to escape run().
        try:
            kind = ct.get_entity_type()
            if kind == EntityType.CORE:
                self._core(ct)
            elif kind == EntityType.BUILDER_BOT:
                self._builder(ct)
            elif kind in (EntityType.GUNNER, EntityType.SENTINEL):
                self._turret(ct)
        except Exception:
            return

    # ------------------------------------------------------------------ core
    def _core(self, ct: Controller) -> None:
        pos = ct.get_position()
        if self.own_core is None:
            self.own_core = pos
            self._publish_enemy_core(ct, pos)

        # Ammo first: convert_ammo does NOT consume the action cooldown, so it
        # never costs a spawn. Guns without ammo are the classic dead capital.
        ammo = ct.get_global_ammo()
        if ammo < AMMO_FLOOR:
            want = min(AMMO_CHUNK, max(0, ct.get_global_resources() - 30))
            if want > 0 and ct.can_convert_ammo(want):
                ct.convert_ammo(want)

        if ct.get_action_cooldown() != 0:
            return
        if ct.get_unit_count() >= GameConstants.MAX_TEAM_UNITS:
            return
        # Keep a small builder pool. More builders is more cost scaling
        # (+20% each), and this doctrine spends titanium on guns, not bodies.
        if ct.get_global_resources() < ct.get_builder_bot_cost() + 20:
            return
        if self._count_own(ct, EntityType.BUILDER_BOT) >= 5:
            return
        for d in DIRECTIONS:
            t = pos.add(d)
            if ct.can_spawn(t):
                ct.spawn_builder(t)
                return

    def _publish_enemy_core(self, ct: Controller, own: Position) -> None:
        """Maps are symmetric by reflection or rotation, so mirror our own core."""
        w, h = ct.get_map_width(), ct.get_map_height()
        # 180-degree rotation is the symmetry that holds for both cases here;
        # the core is a 2x2 footprint, hence the -2.
        ex, ey = w - own.x - 2, h - own.y - 2
        self.enemy_core = Position(max(0, ex), max(0, ey))
        ct.write_store(SLOT_ENEMY_CORE_X, self.enemy_core.x)
        ct.write_store(SLOT_ENEMY_CORE_Y, self.enemy_core.y)

    # --------------------------------------------------------------- builder
    def _builder(self, ct: Controller) -> None:
        if self.role is None:
            self.role = ct.get_id() % 5
        if self.enemy_core is None:
            ex, ey = ct.read_store(SLOT_ENEMY_CORE_X), ct.read_store(SLOT_ENEMY_CORE_Y)
            if ex or ey:
                self.enemy_core = Position(ex, ey)

        rnd = ct.get_current_round()
        harvesters = ct.read_store(SLOT_HARVESTERS)

        # Phase 1 — economy, but only to the measured target.
        if harvesters < HARVESTER_TARGET and rnd < GUN_PUSH_ROUND * 3:
            if self._try_harvester(ct):
                return
            # SEEK the ore. The first cut of this bot only checked tiles it
            # happened to stand beside, so builders spawned by the core, walked
            # straight past the ore toward the enemy, and the bot finished a
            # smoke game with 0 titanium collected and 0 buildings. A rush still
            # has to pay for its guns.
            if self._seek_ore(ct):
                return
            # No ore in vision (r^2=20 is only ~4 tiles). Standing still here
            # was the second half of the 0-titanium bug: builders that spawned
            # out of sight of ore simply idled. Walking forward explores toward
            # the middle of the map, which is where the contested ore is.
            self._advance(ct)
            return

        # Phase 2 — push and plant guns. This is the whole doctrine.
        rushers = max(1, int(5 * RUSH_SHARE))
        if rnd >= GUN_PUSH_ROUND and self.role < rushers:
            if self._try_gun(ct):
                return
            self._advance(ct)
            return

        # Rear builders: keep the economy honest, then help.
        if self._try_harvester(ct):
            return
        if self._try_gun(ct):
            return
        self._advance(ct)

    def _try_harvester(self, ct: Controller) -> bool:
        if ct.get_action_cooldown() != 0:
            return False
        if ct.get_global_resources() < ct.get_harvester_cost():
            return False
        p = ct.get_position()
        for d in CARDINALS:
            t = p.add(d)
            try:
                if ct.get_tile_env(t) != Environment.ORE_TITANIUM:
                    continue
                if ct.can_build_harvester(t):
                    ct.build_harvester(t)
                    ct.write_store(SLOT_HARVESTERS, ct.read_store(SLOT_HARVESTERS) + 1)
                    return True
            except Exception:
                continue
        return False

    def _seek_ore(self, ct: Controller) -> bool:
        """Step toward the nearest free ore tile in vision. True if we moved."""
        if ct.get_move_cooldown() != 0:
            return False
        p = ct.get_position()
        best = None
        for t in ct.get_nearby_tiles():
            try:
                if ct.get_tile_env(t) != Environment.ORE_TITANIUM:
                    continue
                if ct.get_tile_building_id(t) is not None:
                    continue          # already harvested
                dsq = p.distance_squared(t)
                if best is None or dsq < best[0]:
                    best = (dsq, t)
            except Exception:
                continue
        if best is None:
            return False
        d = p.cardinal_direction_to(best[1])
        if d != Direction.CENTRE and ct.can_move(d):
            ct.move(d)
            return True
        for alt in CARDINALS:
            t = p.add(alt)
            if t.distance_squared(best[1]) < best[0] and ct.can_move(alt):
                ct.move(alt)
                return True
        return False

    def _try_gun(self, ct: Controller) -> bool:
        """Plant a gunner facing the enemy core, as far forward as we stand."""
        if ct.get_action_cooldown() != 0 or self.enemy_core is None:
            return False
        if ct.get_global_resources() < ct.get_gunner_cost():
            return False
        p = ct.get_position()
        # Only build forward: a gun behind us is a gun the enemy never meets.
        if p.distance_squared(self.enemy_core) > 400:
            return False
        facing = p.direction_to(self.enemy_core)
        best = None
        for d in CARDINALS:
            t = p.add(d)
            try:
                if not ct.can_build_gunner(t, facing):
                    continue
                dsq = t.distance_squared(self.enemy_core)
                if best is None or dsq < best[0]:
                    best = (dsq, t)
            except Exception:
                continue
        if best is None:
            return False
        try:
            ct.build_gunner(best[1], facing)
            ct.write_store(SLOT_GUNNERS, ct.read_store(SLOT_GUNNERS) + 1)
            return True
        except Exception:
            return False

    def _advance(self, ct: Controller) -> None:
        """Walk toward the enemy core. Builder bots move only in cardinals."""
        if ct.get_move_cooldown() != 0 or self.enemy_core is None:
            return
        p = ct.get_position()
        d = p.cardinal_direction_to(self.enemy_core)
        if d != Direction.CENTRE and ct.can_move(d):
            ct.move(d)
            return
        # Blocked: try the other axis, then anything legal, so we never stall
        # against a wall for the rest of the match.
        for alt in CARDINALS:
            if alt is d:
                continue
            t = p.add(alt)
            if t.distance_squared(self.enemy_core) < p.distance_squared(self.enemy_core):
                if ct.can_move(alt):
                    ct.move(alt)
                    return
        for alt in CARDINALS:
            if ct.can_move(alt):
                ct.move(alt)
                return

    # ---------------------------------------------------------------- turret
    def _turret(self, ct: Controller) -> None:
        if ct.get_action_cooldown() != 0:
            return
        # Prefer the natural target in our facing line.
        try:
            tgt = ct.get_gunner_target()
        except Exception:
            tgt = None
        if tgt is not None and ct.can_fire(tgt):
            ct.fire(tgt)
            return
        # Otherwise take anything hostile we can actually hit.
        me = ct.get_team()
        for t in ct.get_attackable_tiles():
            try:
                bid = ct.get_tile_building_id(t)
                uid = ct.get_tile_builder_bot_id(t)
                for ent in (bid, uid):
                    if ent is not None and ct.get_team(ent) != me and ct.can_fire(t):
                        ct.fire(t)
                        return
            except Exception:
                continue

    # ----------------------------------------------------------------- utils
    def _count_own(self, ct: Controller, kind: EntityType) -> int:
        me = ct.get_team()
        n = 0
        for uid in ct.get_nearby_units():
            try:
                if ct.get_team(uid) == me and ct.get_entity_type(uid) == kind:
                    n += 1
            except Exception:
                continue
        return n
