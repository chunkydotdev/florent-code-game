"""SKALMAN v1 -- the four fixed builder roles, and the turret behaviour.

ALL-NEW CODE (the from-scratch 78%).  Per-verb attributability is a build
requirement, so every method below carries the COPY or ledger row it
implements in its first docstring line, and every doctrine verb reads its own
module-level flag AT THE READ SITE:

  SK_ROLES     COPY 8   role claim + fixed assignment          `_claim_role`
  SK_BELT      COPY 8   global belt plan + repair + V1 escalation
                        `_plan_belt`, `_belt_action`, `_escalate`
  SK_CAGE      COPY 9   ring lap, seal behind, 7-of-8          `_cage_walker`
  SK_ORE_DENY  COPY 1   harvester-death -> barrier-on-T        `_ore_denier`
  SK_NEST      COPY 5   band siting + prep barriers + gun      `_siege_engineer`
  SK_DOOR      COPY 6+2 home-ring clearance, off-axis siting   `_door_action`,
                        `_turret`

⛔ ENGINE DISCIPLINE, applied without exception in this file:
  * every mutating call is gated by its `can_*()` twin;
  * every computed position passes `self.ib(...)` before any `get_tile_*`;
  * `can_fire` returns TRUE at 0 ammo and the engine RAISES inside
    finish_firing_turret, which destroys OUR turret permanently (CLAUDE.md
    guard-matrix sweep) -- so `_turret` checks `get_global_ammo()` against the
    shot price BEFORE firing, every time;
  * builder bots move in CARDINALS only, through `self.step_to`.
"""

from fcode import Direction, EntityType, Environment, Position

from sk_common import (
    OWNER_BELT, OWNER_CAGE, OWNER_DENY, OWNER_DOOR, OWNER_NEST,
    adjacent_to_core, core_tiles, core_tiles_xy, dist_core, dsq_core,
    in_bounds, pack_pos, pack_tile, unpack_pos, unpack_tile,
)
from sk_maps import (
    BELT_TYPES,
    ARMED_TYPES,
    CARDINALS, DIRECTIONS, SK_AMMO_FLOOR, SK_AMMO_GUNNER, SK_AMMO_SENTINEL,
    SK_BEAT_MASK, SK_BEAT_STALE, SK_BELT, SK_BELT_COVER,
    SK_BELT_COVER_TRIGGER, SK_CAGE, SK_CAGE_ACCEPT,
    SK_CAGE_MELEE_GIVEUP, SK_CAGE_WALKER, SK_DEATH_MEMO_ROUNDS, SK_DOOR,
    SK_DOOR_GUN_CAP, SK_HARV_BAN_ROUNDS, SK_HARV_ESCALATE,
    SK_HARV_REBUILD_ESCALATE,
    SK_HOME_KEEPER, SK_HOME_RING_DSQ, SK_KILLER_GUNNER_REACH,
    SK_KILLER_SENT_REACH, SK_NEST, SK_NEST_DSQ_MAX,
    SK_NEST_DSQ_MIN, SK_NEST_POINT_BLANK, SK_NEST_PREP_BARRIERS, SK_N_ROLES,
    SK_ORE_DENIER, SK_ORE_DENY, SK_PREEMPT_ORE_ROUND,
    SK_PRI_BARRIER, SK_PRI_BODY, SK_PRI_CORE, SK_PRI_HARVESTER,
    SK_PRI_MARKED, SK_PRI_OTHER, SK_PRI_TURRET,
    SK_REBUILD_ESCALATE,
    SK_ROLES, SK_SIEGE_ENGINEER, SK_SLOT_BEAT, SK_SLOT_BELT, SK_SLOT_CAGE,
    SK_SLOT_DRIP, SK_SLOT_ENEMY_CORE, SK_SLOT_HARV, SK_SLOT_KILLER,
    SK_SLOT_NEST,
    SK_SLOT_SEATS, SK_SLOT_STALL, SK_SLOT_THREAT_POS, SK_SLOT_UNDER,
    SK_STALL_LIFETIME, SK_STALL_ROUNDS, SK_TARGET_PRIO, SK_TRUNK_DSQ,
    TURRET_TYPES, enemy_core_for,
)

SEAT_MASK = 0xFF          # slot 0 b0-7
CAGE_SEALED_MASK = 0x1F   # slot 6 b0-4
CAGE_BEAT_FIELD = 5       # slot 6 b5-15
NEST_SITE_MASK = 0x3FF    # slot 7 b0-9   (pack_tile)
NEST_RND_FIELD = 10       # slot 7 b10-20
STALL_DEATH_FIELD = 11    # slot 9 b11-16
STALL_DEATH_MASK = 0x3F
STALL_BRANCH_BIT = 1 << 17
STALL_LIFE_FIELD = 18     # slot 9 b18-23
STALL_LIFE_MASK = 0x3F
DRIP_GUN_MASK = 0x3F      # slot 8 b0-5
DRIP_SENT_FIELD = 6       # slot 8 b6-11
BELT_GAP_FIELD = 18       # slot 5 b18-23 -- the uncovered-belt-tile gap.  v600
BELT_GAP_MASK = 0x3F      # PUBLISHED this and never read it; PLANK 2 reads it.
KILLER_TILE_MASK = 0x3FF  # slot 14 b0-9  (pack_tile)
KILLER_RND_FIELD = 10     # slot 14 b10-20
KILLER_N_FIELD = 21       # slot 14 b21-26
KILLER_N_MASK = 0x3F


def cage_lap(o):
    """The 12-tile Chebyshev ring around a 2x2 footprint, clockwise.

    COPY 9 walks a LAP, not a shuttle.  The eight orthogonally-adjacent tiles
    are the SEAL tiles; the four corners are pass-through, and they are what
    makes the lap cardinal-connected -- a builder cannot step diagonally, so a
    lap over the eight seal tiles alone is not walkable.
    """
    ox, oy = o.x, o.y
    return [
        Position(ox - 1, oy - 1),                                   # corner
        Position(ox, oy - 1), Position(ox + 1, oy - 1),             # north face
        Position(ox + 2, oy - 1),                                   # corner
        Position(ox + 2, oy), Position(ox + 2, oy + 1),             # east face
        Position(ox + 2, oy + 2),                                   # corner
        Position(ox + 1, oy + 2), Position(ox, oy + 2),             # south face
        Position(ox - 1, oy + 2),                                   # corner
        Position(ox - 1, oy + 1), Position(ox - 1, oy),             # west face
    ]


LAP_SEAL_IDX = (1, 2, 4, 5, 7, 8, 10, 11)     # indices of the 8 seal tiles


class RolesMixin:

    # ==================================================================
    # BUILDER ENTRY
    # ==================================================================

    def _builder(self, ct):
        p = ct.get_position()
        self._boot(ct, p)

        if self.core is None:
            for eid in ct.get_nearby_buildings():
                try:
                    if (ct.get_entity_type(eid) == EntityType.CORE
                            and ct.get_team(eid) == self.team):
                        self.core = ct.get_position(eid)
                        break
                except Exception:
                    continue
        if self.core is None:
            return
        self._load_grid(ct)
        self._resolve_enemy(ct)

        rnd = ct.get_current_round()
        self._displacement_guard(ct, p)

        if self.role is None:
            self._claim_role(ct, rnd)
        # Liveness: ONE WRITER PER SLOT -- this body owns SK_SLOT_BEAT[role]
        # and nothing else writes it.  Absolute round+1, never modular.
        self.beat(ct, SK_SLOT_BEAT[self.role], rnd)
        self._sense(ct, rnd)

        # --- ledger V5: DENIAL yields to survival when the core is hit -----
        # ⛔ THE DENIAL ROLE ONLY.  The first cut had the cage walker yield too
        # and a local game showed it: the under-attack latch went fresh early
        # and the walker spent the whole match at home, sealing zero ring
        # tiles.  V5 is about branches that spend builder-turns on DENIAL; the
        # walker is the KILL branch, and "not at the kill's expense" cuts the
        # other way for it.
        if self._under_attack(ct, rnd) and self.role == SK_ORE_DENIER:
            if self._home_defence(ct, p, rnd):
                return

        if self.role == SK_CAGE_WALKER:
            self._cage_walker(ct, p, rnd)
        elif self.role == SK_ORE_DENIER:
            self._ore_denier(ct, p, rnd)
        elif self.role == SK_SIEGE_ENGINEER:
            self._siege_engineer(ct, p, rnd)
        else:
            self._home_keeper(ct, p, rnd)

    # --- COPY 8: the role claim ---------------------------------------

    def _claim_role(self, ct, rnd):
        """COPY 8 -- four builders, r0-r3, one fixed job each for the game.

        A role is claimed by taking the lowest role id whose liveness beat is
        unset or STALE, which is also the RE-CLAIM path when a body dies: the
        replacement the core spawns walks into the dead role rather than
        inventing a fifth job.

        ⛔ SK_ROLES OFF is the ablation identity: every body runs HOME KEEPER,
        so the forward verbs have no staffing and their signatures go to zero
        without any other behaviour changing.
        """
        n = ct.read_store(SK_SLOT_SEATS) & SEAT_MASK
        self.wstore(ct, SK_SLOT_SEATS,
                    (ct.read_store(SK_SLOT_SEATS) & ~SEAT_MASK) | ((n + 1) & SEAT_MASK))
        self.seat = n
        if not SK_ROLES:
            self.role = SK_HOME_KEEPER
            self.role_parity = n & 1
            return
        for r in range(SK_N_ROLES):
            if not self.beat_fresh(ct, SK_SLOT_BEAT[r], rnd, SK_BEAT_STALE):
                self.role = r
                self.role_parity = r & 1
                return
        self.role = n % SK_N_ROLES
        self.role_parity = self.role & 1

    def _resolve_enemy(self, ct):
        """Enemy anchor: re-derived locally from map symmetry, refined on
        sight.  The blackboard is a one-round bus, not a memory -- a fact every
        unit can re-derive beats a fact that must be communicated.
        """
        if self.enemy is None:
            e = unpack_pos(ct.read_store(SK_SLOT_ENEMY_CORE))
            if e is None:
                e = enemy_core_for(self.mw, self.mh, self.core)
            self.enemy = e

    def _under_attack(self, ct, rnd):
        return self.beat_fresh(ct, SK_SLOT_UNDER, rnd, 50)

    # --- shared sensing ------------------------------------------------

    def _sense(self, ct, rnd):
        """One pass over visible entities, feeding every role's memory."""
        self.vis_enemy = []
        self.vis_friend = []
        try:
            ids = ct.get_nearby_entities()
        except Exception:
            return
        for eid in ids:
            try:
                t = ct.get_team(eid)
                et = ct.get_entity_type(eid)
                ep = ct.get_position(eid)
            except Exception:
                continue
            if t == self.team:
                self.vis_friend.append((eid, et, ep))
                continue
            self.vis_enemy.append((eid, et, ep))
            if et == EntityType.CORE:
                self.enemy = ep
            elif et == EntityType.HARVESTER:
                # COPY 1's memory: where an ENEMY harvester was last seen.
                self.enemy_harv[(ep.x, ep.y)] = rnd
            elif et in TURRET_TYPES:
                # COPY 2 needs their AXIS, and a sentinel cannot rotate, so a
                # facing read once stays true for that turret's whole life.
                try:
                    self.enemy_facing[eid] = ct.get_direction(eid).delta()
                except Exception:
                    pass
            if et in ARMED_TYPES:
                # v601 PLANK 1/3: keyed on the TILE, not the id.  A turret is a
                # BUILDING and cannot move, so the tile is the durable fact and
                # it outlives the entity leaving vision -- which is the whole
                # point: the gunner that ate 22 harvesters on icefloe was
                # planted at r9 and never looked at again.
                self.armed_memo[(ep.x, ep.y)] = (et, rnd)

    # ==================================================================
    # ROLE 0 -- HOME KEEPER  (harvesters, the global belt, heals, the door)
    # ==================================================================

    def _home_keeper(self, ct, p, rnd):
        self._ore_scan(ct, p)                       # v601 BUGFIX SK_ORE_SENSE
        self._harv_watch(ct, p, rnd)                # v601 PLANK 1
        self._killer_report(ct, rnd)                # v601 PLANK 1 (slot 14)
        if SK_BELT:
            self._plan_belt(ct)
            self._belt_watch(ct, p)
            self._belt_report(ct, rnd)
        if self._escape(ct, p, rnd):
            return
        if ct.get_action_cooldown() == 0:
            if SK_DOOR and self._door_action(ct, p, rnd):
                return
            # v601 PLANK 3: an enemy TURRET adjacent to the keeper outranks
            # everything below.  `_door_action`(a) only melees what stands on
            # our own ring; PLANK 1 marches this body at a located annulus
            # gunner, and without this it would arrive and then build a
            # conveyor next to it.
            if self._peck_priority(ct, p, rnd):
                return
            if self._heal_action(ct, p, rnd):
                return
            if self._harvester_action(ct, p, rnd):
                return
            if SK_BELT and self._belt_action(ct, p, rnd):
                return
            if self._cover_gun_action(ct, p, rnd):  # v601 PLANK 2
                return
        self._home_keeper_move(ct, p, rnd)

    def _escape(self, ct, p, rnd):
        """Boxed in anyway (somebody else built the last tile): destroy one
        allied non-harvester building to open a step.

        `destroy` is free, costs no cooldown and is unlimited per turn -- so the
        ONLY hazard is ledger V8's build/destroy thrash (0.52 tiles/game rebuilt
        >= 5 times in the doctrine we replicate, worst 893 builds on one tile).
        The ban is what makes this a one-shot escape instead of an oscillator:
        the tile is off the build list long enough for this body to walk away.
        """
        if self.free_neighbours(ct, p) > 0:
            return False
        # v601: CHEAPEST FIRST.  v600 took the first legal neighbour, so an
        # escape could spend a 20-48 Ti turret to open a step that a 3 Ti
        # conveyor would have opened.  Ordering does not change WHETHER we
        # escape -- the loop still ends at the same candidate set.
        cheap = []
        dear = []
        for d in CARDINALS:
            q = p.add(d)
            if not self.ibp(q):
                continue
            try:
                bid = ct.get_tile_building_id(q)
                if bid is None or ct.get_team(bid) != self.team:
                    continue
                et = ct.get_entity_type(bid)
            except Exception:
                continue
            if et in (EntityType.HARVESTER, EntityType.CORE):
                continue
            if et in ARMED_TYPES:
                dear.append(q)
            else:
                cheap.append(q)
        for q in cheap + dear:
            try:
                if not ct.can_destroy(q):
                    continue
                ct.destroy(q)
            except Exception:
                continue
            self.belt_built.discard((q.x, q.y))
            self.escape_ban[(q.x, q.y)] = rnd + 30
            return True
        return False

    def _heal_action(self, ct, p, rnd):
        """1 Ti -> +4 HP on every friendly entity on an adjacent tile."""
        if ct.get_global_resources() < 2:
            return False
        best = None
        for d in CARDINALS:
            q = p.add(d)
            if not self.ibp(q):
                continue
            try:
                bid = ct.get_tile_building_id(q)
            except Exception:
                continue
            if bid is None:
                continue
            try:
                if ct.get_team(bid) != self.team:
                    continue
                miss = ct.get_max_hp(bid) - ct.get_hp(bid)
            except Exception:
                continue
            if miss >= 4 and (best is None or miss > best[0]):
                best = (miss, q)
        if best is None:
            return False
        try:
            if ct.can_heal(best[1]):
                ct.heal(best[1])
                return True
        except Exception:
            return False
        return False

    def _harvester_action(self, ct, p, rnd):
        """Harvesters on adjacent ore, home half only.  Chassis, not a verb.

        v601 PLANK 1 (SK_HARV_ESCALATE): gated by `_harv_blocked`, the harvester
        half of ledger V1.
        """
        cost = ct.get_harvester_cost()
        if ct.get_global_resources() < cost:
            return False
        for d in CARDINALS:
            q = p.add(d)
            if not self.ibp(q) or not self.is_home_half(q):
                continue
            if self.belt_plan.get((q.x, q.y)) is not None:
                continue          # arbiter: this tile belongs to the belt
            if self._harv_blocked(ct, (q.x, q.y), rnd):
                continue          # PLANK 1: this tile is a killzone, not a seat
            try:
                if ct.get_tile_env(q) != Environment.ORE_TITANIUM:
                    continue
                if not ct.can_build_harvester(q):
                    continue
                ct.build_harvester(q)
            except Exception:
                continue
            self.harv_tiles.add((q.x, q.y))
            self.belt_key = None                  # the global plan must re-run
            n = ct.read_store(SK_SLOT_HARV)
            if len(self.harv_tiles) > n:
                self.wstore(ct, SK_SLOT_HARV, len(self.harv_tiles))
            return True
        return False

    # ==================================================================
    # v601 PLANK 1 -- SK_HARV_ESCALATE: the HARVESTER half of ledger V1
    # ==================================================================
    # CAUSE 1 of the tape30 autopsy, and the fix was already written and
    # applied to the wrong entity type.  `_belt_action` carries the ledger
    # ("a tile rebuilt SK_REBUILD_ESCALATE times WITHOUT SURVIVING stops being
    # rebuilt and becomes a locate-the-shooter task; rebuild #4 never happens")
    # and it WORKS where it is wired -- the auroraveil conveyor loop stopped at
    # 3.  `_harvester_action` had no counter, no memo and no ban, and the
    # icefloe harvester loop ran to TWENTY-TWO: one enemy gunner planted at r9
    # at d^2 41 of our core, never attacked once in the remaining 337 rounds,
    # killing a fresh harvester on tile (3,11) every nine rounds.  32 of 33
    # harvester deaths sat on three tiles; 81.8% never delivered a stack.

    def _harv_watch(self, ct, p, rnd):
        """Detect a dead harvester, count it, ban the tile, name the shooter.

        The same shape as `_belt_watch` -- a tile we can SEE to be empty is no
        longer built -- which is what makes the counter count REBUILDS rather
        than builds.  Dropping the tile from `harv_tiles` also stops the global
        belt plan routing a trunk to a harvester that no longer exists.
        """
        if not SK_HARV_ESCALATE or not self.harv_tiles:
            return
        for xy in list(self.harv_tiles):
            q = Position(xy[0], xy[1])
            if not self.ibp(q) or p.distance_squared(q) > 20:
                continue
            try:
                if not ct.is_in_vision(q):
                    continue
                if ct.get_tile_building_id(q) is not None:
                    continue
            except Exception:
                continue
            self.harv_tiles.discard(xy)
            self.belt_key = None                    # the global plan must re-run
            n = self.harv_deaths.get(xy, 0) + 1
            self.harv_deaths[xy] = n
            killer = self._infer_killer(xy)
            if killer is not None:
                self.harv_killer[xy] = killer
                self.killer_pos = killer
                self.killer_rnd = rnd
            if n >= SK_HARV_REBUILD_ESCALATE:
                self.harv_escalated.add(xy)
                self.harv_ban[xy] = rnd + SK_HARV_BAN_ROUNDS

    def _harv_blocked(self, ct, xy, rnd):
        """True while an escalated ore tile is off the build list.

        Two lifts, exactly as briefed: the ban EXPIRES after
        SK_HARV_BAN_ROUNDS, or the inferred killer is CONFIRMED DEAD.  A lift
        clears the escalation but keeps the death count, so the next loss
        re-escalates immediately -- after the first escalation the tile is
        throttled to one harvester per ban window instead of one per nine
        rounds.
        """
        if not SK_HARV_ESCALATE:
            return False
        if xy not in self.harv_escalated:
            return False
        if rnd >= self.harv_ban.get(xy, 0) or self._killer_dead(ct, xy):
            self.harv_escalated.discard(xy)
            self.harv_ban.pop(xy, None)
            return False
        return True

    def _infer_killer(self, xy):
        """Which remembered enemy turret could have shot the tile at xy.

        A gunner's shot is a STRAIGHT LINE, so a shooter stands on the victim's
        row, column or exact diagonal, inside its own reach.  The tape agrees
        with the geometry from the other side: 33/33 harvester killers stood in
        the d^2 20-100 annulus of OUR core (median 41), i.e. within ~6 tiles of
        the harvester they were eating.

        ⛔ THIS IS AN INFERENCE, NOT AN OBSERVATION.  We get no damage event; a
        replay carries one and a running bot does not.  Nearest admissible
        shooter wins, and a wrong answer costs one wasted march, not a unit.
        """
        best = None
        for k, v in self.armed_memo.items():
            et = v[0]
            if et == EntityType.LAUNCHER:
                continue                            # cannot shoot anything
            dx = k[0] - xy[0]
            dy = k[1] - xy[1]
            if dx == 0 and dy == 0:
                continue
            if not (dx == 0 or dy == 0 or (dx == dy or dx == -dy)):
                continue
            d = dx * dx + dy * dy
            reach = (SK_KILLER_GUNNER_REACH if et == EntityType.GUNNER
                     else SK_KILLER_SENT_REACH)
            if d > reach:
                continue
            if best is None or d < best[0]:
                best = (d, Position(k[0], k[1]))
        return None if best is None else best[1]

    def _killer_dead(self, ct, xy):
        """True once the tile we blamed carries no enemy building any more."""
        k = self.harv_killer.get(xy)
        if k is None:
            return False
        if not self.ibp(k):
            return True
        try:
            if not ct.is_in_vision(k):
                return False
            bid = ct.get_tile_building_id(k)
            if bid is None:
                self.armed_memo.pop((k.x, k.y), None)
                return True
            return ct.get_team(bid) == self.team
        except Exception:
            return False

    def _killer_report(self, ct, rnd):
        """SK_SLOT_KILLER (writer: HOME KEEPER) -- publish the inferred belt
        killer so the door and turret verbs can consume it.  ONE WRITER.
        """
        if not SK_HARV_ESCALATE:
            return
        word = 0
        if self.killer_pos is not None and self.ibp(self.killer_pos):
            word |= pack_tile(self.killer_pos) & KILLER_TILE_MASK
            word |= ((self.killer_rnd + 1) & SK_BEAT_MASK) << KILLER_RND_FIELD
        word |= (min(len(self.harv_escalated), 63)
                 & KILLER_N_MASK) << KILLER_N_FIELD
        self.wstore(ct, SK_SLOT_KILLER, word)

    def killer_word_pos(self, ct):
        """The published killer tile, for any unit that is not the keeper."""
        if not SK_HARV_ESCALATE:
            return None
        try:
            k = unpack_tile(ct.read_store(SK_SLOT_KILLER) & KILLER_TILE_MASK)
        except Exception:
            return None
        if k is None or not self.ibp(k):
            return None
        return k

    # --- COPY 8 / defect #78: the GLOBAL belt plan ---------------------

    def _plan_belt(self, ct):
        """SK_BELT -- ONE global plan for the whole belt, not one chain per
        harvester (#78: per-harvester planning is why our harvester->core
        connectivity reads 58.8% against their 83%).

        Single-source BFS from the core over static terrain gives a parent
        tree; every harvester's chain is its parent walk, so shared trunk
        segments MERGE by construction instead of being re-planned per source.
        The chain is ALWAYS TERMINATED: the last tile is orthogonally adjacent
        to the footprint and faces it, so the belt delivers into the core --
        `titanium_collected` counts delivery, never emission.
        """
        # v601: `len(self.map_walls)` joins the key for the same reason it
        # joins the nav key -- on an unconfirmed map the wall set grows.
        key = (self.core, len(self.harv_tiles), len(self.belt_ban),
               len(self.map_walls))
        if self.belt_key == key:
            return
        self.belt_key = key
        self.belt_plan = {}
        self.belt_head = {}
        # ⛔ v601 BUGFIX: this read `self.map_grid is None`, so on any map the
        # catalogue could not confirm -- 10 of the 15 pool maps -- THERE WAS NO
        # BELT AT ALL.  Measured on stavkirke seed 11 with SK_ORE_SENSE alone:
        # two harvesters built by r13 and `plan=0` for the whole match, i.e.
        # 40 Ti spent on two units with no route home, which is worth exactly
        # zero forever.  `terrain_known()` accepts a sensed board.
        if not self.terrain_known() or not self.harv_tiles:
            return
        parent = self._belt_parents(ct, avoid_ore=True)
        if parent is None:
            return
        if any(h not in parent for h in self.harv_tiles):
            # An ore field can fence a harvester in.  Re-run allowing ore
            # rather than leave a harvester with no route home: a harvester
            # with no route home is worth exactly zero, forever.
            parent = self._belt_parents(ct, avoid_ore=False)
            if parent is None:
                return
        core_xy = set(core_tiles_xy(self.core))
        plan = {}
        for h in self.harv_tiles:
            cur = parent.get(h)
            prev = h
            hops = 0
            while cur is not None and cur not in core_xy and hops < 200:
                # `prev` feeds `cur`, so prev carries the facing toward cur.
                if prev != h:
                    plan[prev] = _card(cur[0] - prev[0], cur[1] - prev[1])
                else:
                    self.belt_head[h] = cur
                prev = cur
                cur = parent.get(cur)
                hops += 1
            if cur is not None and hops < 200 and prev != h:
                # TERMINATION: the last tile is adjacent to the footprint and
                # faces it, so the chain delivers INTO the core.
                plan[prev] = _card(cur[0] - prev[0], cur[1] - prev[1])
            elif prev == h and cur is not None:
                self.belt_head[h] = None     # harvester already touches home
        for h in self.harv_tiles:
            plan.pop(h, None)                # a harvester tile is a harvester
        self.belt_plan = plan

    def _belt_parents(self, ct, avoid_ore):
        """Single-source BFS from the core footprint; (x,y) -> next tile home.

        Ore is avoided on the first pass because a conveyor standing on ore
        consumes a harvester seat permanently.
        """
        # v601: terrain through `wall_at`/`ore_at`, which answer from the
        # confirmed grid when there is one and from SENSED tiles otherwise.
        # UNSEEN reads as passable, so the plan is optimistic -- `_belt_watch`
        # bans a planned tile as soon as vision refutes it.
        mw, mh = self.mw, self.mh
        core_xy = set(core_tiles_xy(self.core))
        parent = {}
        frontier = []
        for cx, cy in core_xy:
            for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                qx, qy = cx + dx, cy + dy
                if not in_bounds(qx, qy, mw, mh) or (qx, qy) in core_xy:
                    continue
                if self.wall_at(qx, qy) or (qx, qy) in self.belt_ban:
                    continue
                if (qx, qy) in parent:
                    continue
                parent[(qx, qy)] = (cx, cy)
                frontier.append((qx, qy))
        guard = 0
        while frontier:
            guard += 1
            if (guard & 7) == 0 and self._cpu_exhausted(ct):
                return None
            nxt = []
            for (x, y) in frontier:
                for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                    qx, qy = x + dx, y + dy
                    if not in_bounds(qx, qy, mw, mh):
                        continue
                    if (qx, qy) in parent or (qx, qy) in core_xy:
                        continue
                    if self.wall_at(qx, qy) or (qx, qy) in self.belt_ban:
                        continue
                    if (avoid_ore and self.ore_at(qx, qy)
                            and (qx, qy) not in self.harv_tiles):
                        continue
                    parent[(qx, qy)] = (x, y)
                    nxt.append((qx, qy))
            frontier = nxt
        return parent

    def _belt_action(self, ct, p, rnd):
        """SK_BELT -- lay or repair the planned belt on an adjacent tile.

        LEDGER V1 (the most expensive bug in the study: sixteen rebuilds of one
        conveyor at 6-round intervals into a stationary gun): a tile rebuilt
        SK_REBUILD_ESCALATE times WITHOUT SURVIVING stops being rebuilt and
        becomes a locate-the-shooter task.  Rebuild #4 never happens.
        """
        self._plan_belt(ct)
        if not self.belt_plan:
            return False
        cost = ct.get_conveyor_cost()
        if ct.get_global_resources() < cost:
            return False
        for d in CARDINALS:
            q = p.add(d)
            if not self.ibp(q):
                continue
            face = self.belt_plan.get((q.x, q.y))
            if face is None:
                continue
            if (q.x, q.y) in self.belt_escalated:
                continue
            if self.escape_ban.get((q.x, q.y), -1) > rnd:
                continue
            if not self.may_build(q, OWNER_BELT):
                continue
            if self.free_neighbours(ct, p, exclude=q) == 0:
                continue                        # self-trap guard
            try:
                bid = ct.get_tile_building_id(q)
            except Exception:
                continue
            if bid is not None:
                # ⛔ v601: v600 said `continue` here and that is a PERMANENT
                # BELT STALL.  Measured on stavkirke seed 11: the terminal
                # trunk tile (9,4) -- the one that faces the core, i.e. the one
                # that makes the belt DELIVER -- carried an enemy building from
                # ~r18, so four conveyors stood wired to nothing and the game
                # finished `0 mined`.  A belt tile is literally "a path the
                # current action needs", which is PLANK 3(d)'s carve-out.
                if self._belt_evict(ct, p, q, bid, rnd):
                    return True
                continue
            n = self.belt_rebuilds.get((q.x, q.y), 0)
            if n >= SK_REBUILD_ESCALATE:
                self.belt_escalated.add((q.x, q.y))
                self.belt_ban.add((q.x, q.y))
                self.belt_key = None            # re-route around the killzone
                continue
            try:
                if not ct.can_build_conveyor(q, face):
                    continue
                ct.build_conveyor(q, face)
            except Exception:
                continue
            self.belt_rebuilds[(q.x, q.y)] = n + 1
            self.belt_built.add((q.x, q.y))
            return True
        return False

    def _belt_evict(self, ct, p, q, bid, rnd):
        """Something occupies a PLANNED belt tile.  True if this took the turn.

        Three cases, and only one of them is a peck:
          * OUR OWN conveyor/splitter -- the tile is already served; record it
            as built so `_belt_report` stops calling the chain broken;
          * OUR OWN anything else (a barrier from the self-trap escape, a
            harvester the arbiter did not claim) -- `destroy` is FREE, costs no
            cooldown and is unlimited per turn, so remove it and let the next
            pass build;
          * an ENEMY building -- peck it.  This is PLANK 3(d): a barrier is a
            legal target exactly when it blocks the path the current action
            needs, and the terminal trunk tile is that path.  V7's give-up rule
            caps the chew, and a give-up BANS the tile so the plan re-routes
            instead of stalling forever, which is ledger V1's shape.
        """
        try:
            mine = ct.get_team(bid) == self.team
            et = ct.get_entity_type(bid)
        except Exception:
            return False
        if mine:
            if et in BELT_TYPES:
                self.belt_built.add((q.x, q.y))
                return False
            # ⛔ NEVER DEMOLISH OUR OWN TURRET, CORE OR HARVESTER TO LAY A
            # 3 Ti CONVEYOR.  MEASURED, in the first battery this branch ran
            # in: holmgang seat B, r70 -- a gunner of ours removed at FULL HP
            # (25/25) ONE ROUND after it was built, because the belt re-routed
            # over its tile after a harvester died and reset the plan.  That is
            # ledger V8's build/destroy thrash with a 20-48 Ti price tag.  The
            # belt is the cheap thing: BAN THE TILE and route around.
            if et in (EntityType.CORE, EntityType.HARVESTER) or et in ARMED_TYPES:
                self.belt_ban.add((q.x, q.y))
                self.belt_key = None
                return False
            try:
                if ct.can_destroy(q):
                    ct.destroy(q)
                    self.belt_built.discard((q.x, q.y))
            except Exception:
                return False
            return False
        if not SK_TARGET_PRIO:
            return False
        if ct.get_global_resources() < 2:
            return False
        if self.gave_up(bid, rnd) or self._enemy_builder_adjacent(ct, q):
            self.belt_ban.add((q.x, q.y))
            self.belt_key = None
            return False
        if not self.hp_trend_ok(ct, bid, rnd):
            self.belt_ban.add((q.x, q.y))
            self.belt_key = None
            return False
        try:
            if ct.can_fire(q):
                ct.fire(q)
                return True
        except Exception:
            return False
        return False

    def _escalate_target(self, ct, p):
        """LEDGER V1's other half -- once a tile is escalated, the answer is
        the SHOOTER, not another conveyor.  Returns the enemy turret to remove.

        v601 PLANK 1 widens this in two ways and FENCES it in one.
          * an escalated HARVESTER tile triggers it too, not only a belt tile;
          * an INFERRED killer counts even when it is not visible this round --
            it is a building, it has not moved, and the whole failure mode is a
            turret nobody looks at again after r9;
          * ⛔ THE FENCE: the target must sit inside d^2 100 of OUR core.  The
            keeper's measured forward-action share is 0.000 and that property
            is load-bearing (it is why only 2 of 22 body deaths were keepers);
            the annulus this plank exists to answer is d^2 20-100, so the fence
            costs the plank nothing and keeps the role at home.
        """
        if not self.belt_escalated and not self.harv_escalated:
            return None
        best = None
        for eid, et, ep in self.vis_enemy:
            if et not in ARMED_TYPES:
                continue
            if self.core is not None and dsq_core(ep, self.core) > 100:
                continue
            d = p.distance_squared(ep)
            if best is None or d < best[0]:
                best = (d, ep)
        if best is not None:
            return best[1]
        if not SK_HARV_ESCALATE:
            return None
        for xy in self.harv_escalated:
            k = self.harv_killer.get(xy)
            if k is None or not self.ibp(k):
                continue
            if self.core is not None and dsq_core(k, self.core) > 100:
                continue
            d = p.distance_squared(k)
            if best is None or d < best[0]:
                best = (d, k)
        return None if best is None else best[1]

    # --- COPY 6 + COPY 2: the door verb --------------------------------

    def _door_action(self, ct, p, rnd):
        """COPY 6 -- home-ring clearance.  Their 79.7% against their field's
        33.5%; ours 42.8% against ours.  Two halves, implemented separately:
        (a) melee what gets planted on our ring; (b) plant an adjacent
        counter-turret -- and COPY 2 sites that answer OFF the enemy
        sentinel's firing axis, because a sentinel cannot rotate.
        """
        threat = None
        for eid, et, ep in self.vis_enemy:
            # ⛔ TURRETS ONLY.  The first cut of this verb answered ANY enemy
            # building on our ring and bought six gunners in one local game
            # (`+20% cost scale each`, bank at 23 Ti, and the cage/nest verbs
            # starved behind it).  COPY 6 is about what SHOOTS at our door.
            if et not in TURRET_TYPES:
                continue
            if dsq_core(ep, self.core) > SK_HOME_RING_DSQ * 3:
                continue
            if self.gave_up(eid, rnd):
                continue
            if threat is None or dsq_core(ep, self.core) < dsq_core(threat[1], self.core):
                threat = (eid, ep)
        if threat is None:
            return False
        tid, tpos = threat
        # (a) melee it if we are already orthogonally adjacent
        if abs(tpos.x - p.x) + abs(tpos.y - p.y) == 1 and ct.get_global_resources() >= 2:
            if self.hp_trend_ok(ct, tid, rnd):
                try:
                    if ct.can_fire(tpos):
                        ct.fire(tpos)
                        return True
                except Exception:
                    pass
        # (b) counter-turret, sited off their sentinel's axis
        if self.door_guns >= SK_DOOR_GUN_CAP:
            return False
        gcost = ct.get_gunner_cost()
        if ct.get_global_resources() < gcost + 40:
            return False
        # ⭐ v601 PLANK 2 (SK_BELT_COVER).  v600 scored SITES on a permissive
        # DISC of planned belt tiles and then faced the gun at the threat --
        # which is how 12 of our 18 turrets ended up inside d^2 10 of our own
        # core while 85.7% of the belt that died sat outside d^2 13, and how
        # 0 of 42 dead belt pieces were in any firing line of ours at death.
        # A gunner does not shoot a disc; it shoots ONE RAY.  So the scorer
        # enumerates (site, FACING) PAIRS and requires that ray to cross live
        # belt TRUNK.  Facing is chosen, not derived.
        site, face = self._pick_gun_site(ct, p, tpos, require_cover=True)
        if site is None:
            # ⛔ THE REQUIREMENT ORDERS, IT DOES NOT VETO.  `_door_action` is
            # the instrument that produced 5 of our 6 forward-turret removals
            # in the tape (the sixth was a peck); a plank that silently
            # switches it off would trade CAUSE 2 for a regression on M7.
            # When no covering facing exists, take the v600 answer.
            site, face = self._pick_gun_site(ct, p, tpos, require_cover=False)
        if site is None:
            return False
        try:
            if not ct.can_build_gunner(site, face):
                return False
            ct.build_gunner(site, face)
        except Exception:
            return False
        self.door_guns += 1
        return True

    def _pick_gun_site(self, ct, p, tpos, require_cover):
        """(site, facing) for a home gunner, or (None, None).

        PLANK 2's scorer.  `tpos` may be None (the `_cover_gun_action` path,
        where there is no ring threat and the target is the belt itself).
        Ordering, highest first:
          1. the facing ray reaches the INFERRED BELT KILLER (PLANK 1's word);
          2. the gun can actually fire at the ring threat from there;
          3. weighted belt-trunk tiles on the ray (a tile that has ALREADY
             eaten harvesters is worth 3, per the autopsy's "32 of 33 deaths
             on three tiles" -- coverage should go where the deaths are);
          4. closeness to the threat.
        """
        if not SK_BELT_COVER:
            # ⛔ ABLATION IDENTITY.  Flag off reproduces v600's scorer exactly:
            # a permissive DISC of planned belt tiles, and a facing DERIVED
            # from the threat rather than chosen.  Nothing else in the door
            # verb changes, so the flag maps onto one signature.
            if tpos is None:
                return None, None
            best_site = None
            best_score = None
            for d in CARDINALS:
                q = p.add(d)
                if not self.ibp(q) or not self.may_build(q, OWNER_DOOR):
                    continue
                if q.distance_squared(tpos) > 13:
                    continue
                if self._on_enemy_axis(q):
                    continue
                score = (self._belt_cover(q), -q.distance_squared(tpos))
                if best_score is None or score > best_score:
                    best_score = score
                    best_site = q
            if best_site is None:
                return None, None
            return best_site, best_site.direction_to(tpos)
        trunk = self._trunk_tiles()
        killer = self.killer_pos
        if killer is None:
            killer = self.killer_word_pos(ct)
        if require_cover and not trunk:
            return None, None
        best = None
        best_site = None
        best_face = None
        for d in CARDINALS:
            q = p.add(d)
            if not self.ibp(q) or not self.may_build(q, OWNER_DOOR):
                continue
            if tpos is not None and q.distance_squared(tpos) > 13:
                continue
            if self._on_enemy_axis(q):
                continue                       # COPY 2: never in their line
            # ⛔ THE SELF-TRAP GUARD, which v600's door verb was MISSING while
            # every other build site in the tree has it.  MEASURED, in the
            # first battery this scorer ran in: holmgang seat B r70, a gunner
            # of ours removed at FULL HP one round after it was built -- the
            # gun took the keeper's last free tile, `_escape` fired next round
            # and demolished it.  PLANK 2 buys more guns near the keeper, so
            # the missing guard goes from rare to routine.
            # ⛔ TWO, NOT ONE.  A conveyor's site needs one spare neighbour;
            # a TURRET is permanent and costs 20-48 Ti, and the measured
            # failure needed only one more tile to close after the build --
            # r67 and r69 bought two door gunners on consecutive rounds, the
            # second took the keeper's second-to-last tile at (8,6), the last
            # one closed, and `_escape` demolished a full-HP gunner at r70.
            if self.free_neighbours(ct, p, exclude=q) < 2:
                continue
            for face in DIRECTIONS:
                cov = self._ray_cover(q, face, trunk)
                if require_cover and cov <= 0:
                    continue
                kill = 0
                if killer is not None and self._ray_hits(q, face, killer):
                    kill = 1
                hits = 0
                if tpos is not None:
                    try:
                        if ct.can_fire_from(q, face, EntityType.GUNNER, tpos):
                            hits = 1
                    except Exception:
                        hits = 0
                score = (kill, hits, cov,
                         0 if tpos is None else -q.distance_squared(tpos))
                if best is None or score > best:
                    best = score
                    best_site = q
                    best_face = face
        if best_site is None:
            return None, None
        return best_site, best_face

    def _trunk_tiles(self):
        """The live belt TRUNK: our belt/harvester tiles beyond SK_TRUNK_DSQ of
        our own core, weighted by how many buildings that tile has already
        lost.  This is the cluster PLANK 2 is told to prefer.
        """
        if self.core is None:
            return {}
        out = {}
        for xy in self.belt_built:
            if dsq_core(Position(xy[0], xy[1]), self.core) <= SK_TRUNK_DSQ:
                continue
            out[xy] = 1 + 2 * min(self.belt_rebuilds.get(xy, 1) - 1, 2)
        for xy in self.harv_tiles:
            if dsq_core(Position(xy[0], xy[1]), self.core) <= SK_TRUNK_DSQ:
                continue
            out[xy] = 1 + 2 * min(self.harv_deaths.get(xy, 0), 2)
        for xy in self.harv_deaths:
            if xy in out:
                continue
            if dsq_core(Position(xy[0], xy[1]), self.core) <= SK_TRUNK_DSQ:
                continue
            # A tile that keeps losing harvesters is exactly where the answer
            # belongs, whether or not one stands there this round.
            out[xy] = 1 + 2 * min(self.harv_deaths[xy], 2)
        return out

    def _ray_cover(self, q, face, trunk):
        """Weighted trunk tiles a GUNNER at q facing `face` would cover.

        ⛔ A RAY, NOT A DISC, and that is the whole plank.  `_belt_cover` below
        is the permissive disc form and it is kept -- it feeds the PUBLISHED
        gap metric, where an optimistic coverage test makes the reported gap
        conservative.  Siting must use the pessimistic form or it re-creates
        the 0/42 it is here to fix.
        """
        if not trunk:
            return 0
        dx, dy = face.delta()
        if dx == 0 and dy == 0:
            return 0
        n = 0
        k = 1
        while k * k * (dx * dx + dy * dy) <= 13:
            x = q.x + dx * k
            y = q.y + dy * k
            if not self.ib(x, y):
                break
            n += trunk.get((x, y), 0)
            k += 1
        return n

    def _ray_hits(self, q, face, target, reach=13):
        """Would a gunner at q facing `face` cover the tile `target`?"""
        dx, dy = face.delta()
        if dx == 0 and dy == 0:
            return False
        ax = target.x - q.x
        ay = target.y - q.y
        if ax * ax + ay * ay > reach:
            return False
        if ax * dy != ay * dx:
            return False
        return (ax * dx + ay * dy) > 0

    def _cover_gun_action(self, ct, p, rnd):
        """PLANK 2, SK_BELT_COVER_TRIGGER -- buy the trunk gun when PLANK 1 has
        NAMED the thing eating the belt.

        ⛔ DISCLOSED AS AN EXTENSION OF THE BRIEF, which specifies a siting
        change only.  The reason it exists: `_door_action` fires only when an
        enemy turret is planted on our OWN ring, and the tape bought a median
        of ONE turret per game -- so a pure re-siting plank has almost nothing
        to re-site and its own acceptance signature ("any dead belt piece
        covered", target > 0 against a 0/42 baseline) would read zero for want
        of a turret rather than for want of the plank.  Setting
        SK_BELT_COVER_TRIGGER = False recovers the siting-only form.

        ⛔ THE CAP IS UNCHANGED.  This spends from the same SK_DOOR_GUN_CAP = 2
        budget as the door answer; it changes WHICH gun gets bought, not how
        many.  Uncapped, the first local v600 game bought six gunners at +20%
        cost scale each and starved every other verb.
        """
        if not (SK_BELT_COVER and SK_BELT_COVER_TRIGGER):
            return False
        if self.door_guns >= SK_DOOR_GUN_CAP:
            return False
        if self.core is None:
            return False
        killer = self.killer_pos
        if killer is None:
            killer = self.killer_word_pos(ct)
        # EVIDENCE THAT SOMETHING IS EATING THE BELT.  Not only an escalated
        # tile: PLANK 1 works well enough that a tile rarely reaches two
        # deaths, so gating on escalation alone would make PLANK 2 fire least
        # often exactly when PLANK 1 is doing its job.  Any lost belt piece
        # counts.
        hurt = (killer is not None or bool(self.harv_escalated)
                or bool(self.harv_deaths)
                or any(v > 1 for v in self.belt_rebuilds.values()))
        if not hurt:
            return False
        gap = (ct.read_store(SK_SLOT_BELT) >> BELT_GAP_FIELD) & BELT_GAP_MASK
        if gap <= 0:
            return False            # §2.8(b): nothing uncovered, nothing to buy
        gcost = ct.get_gunner_cost()
        if ct.get_global_resources() < gcost + 40:
            return False
        site, face = self._pick_gun_site(ct, p, None, require_cover=True)
        if site is None:
            return False
        try:
            if not ct.can_build_gunner(site, face):
                return False
            ct.build_gunner(site, face)
        except Exception:
            return False
        self.door_guns += 1
        return True

    def _belt_cover(self, q, reach=13):
        """How many planned belt tiles a gunner at q could ever reach.

        A gunner shoots a straight line along its facing but may ROTATE
        (10 Ti), so "can ever cover" is the r^2=13 disc, not one ray.  This is
        deliberately the permissive form -- the metric it feeds is "is this
        belt tile outside EVERY live home turret's reach", and an optimistic
        coverage test makes the reported gap conservative.
        """
        n = 0
        for (x, y) in self.belt_plan:
            dx = x - q.x
            dy = y - q.y
            if dx * dx + dy * dy <= reach:
                n += 1
        return n

    def _belt_uncovered(self, ct):
        """DESIGN §2.8(b) -- the belt tiles no live home turret can ever cover.

        v1 does not re-site to fix this; it MEASURES it (published on slot 5,
        b18-23) so an unreachable annulus is a recorded gap rather than a
        silent inheritance.
        """
        if not self.belt_plan or self.core is None:
            return 0
        guns = []
        for eid, et, ep in self.vis_friend:
            if et not in TURRET_TYPES:
                continue
            if dsq_core(ep, self.core) > 200:
                continue
            guns.append((ep, 13 if et == EntityType.GUNNER else 32))
        if not guns:
            return min(len(self.belt_plan), 63)
        n = 0
        for (x, y) in self.belt_plan:
            covered = False
            for ep, reach in guns:
                dx = x - ep.x
                dy = y - ep.y
                if dx * dx + dy * dy <= reach:
                    covered = True
                    break
            if not covered:
                n += 1
        return min(n, 63)

    def _on_enemy_axis(self, q):
        """COPY 2's mirror term: is q inside a visible enemy SENTINEL's firing
        line?  A sentinel cannot rotate, so a tile off its axis is fighting
        something that physically cannot shoot back (Pantheon's 49-vs-9 trade).
        """
        for eid, et, ep in self.vis_enemy:
            if et != EntityType.SENTINEL:
                continue
            try:
                f = self.enemy_facing.get(eid)
            except Exception:
                f = None
            if f is None:
                continue
            dx, dy = f
            ax, ay = q.x - ep.x, q.y - ep.y
            if dx == 0 and dy == 0:
                continue
            if dx == 0:
                if ax == 0 and (ay * dy) > 0:
                    return True
            elif dy == 0:
                if ay == 0 and (ax * dx) > 0:
                    return True
            elif ax * dy == ay * dx and (ax * dx) > 0:
                return True
        return False

    def _home_keeper_move(self, ct, p, rnd):
        """Never leaves the home quadrant (forward-action share 0.000)."""
        shooter = self._escalate_target(ct, p)
        if shooter is not None:
            self.step_to(ct, shooter)
            return
        self._plan_belt(ct)
        tgt = None
        best = None
        # ⛔ ORE AND BELT COMPETE ON DISTANCE, NOT ON PRIORITY.  The first cut
        # walked the belt plan to completion before it would look at a second
        # ore tile, and finished a local game with TWO harvesters and 500 Ti
        # mined against the benchmark's six and 1,420.  A harvester that does
        # not exist has no belt.
        # ⛔ STEP OFF A TILE YOU ARE ABOUT TO BUILD.  A builder cannot build on
        # its OWN tile, and `_bfs_direction` answers CENTRE when the target is
        # where you already stand -- so "walk to the nearest unbuilt belt tile"
        # deadlocks the instant that tile is underfoot.  Measured: the keeper
        # stood on (7,9) with three free neighbours from r19 to the end of the
        # match, targeting itself.  This is the same engine fact as ledger V2.
        if ((p.x, p.y) in self.belt_plan and (p.x, p.y) not in self.belt_built
                and (p.x, p.y) not in self.belt_escalated):
            for d in CARDINALS:
                q = p.add(d)
                if not self.ibp(q):
                    continue
                try:
                    if not ct.is_tile_passable(q):
                        continue
                except Exception:
                    continue
                self.step_to(ct, q)
                return
        for (x, y) in self.belt_plan:
            if (x, y) in self.belt_escalated or (x, y) in self.belt_built:
                continue
            if x == p.x and y == p.y:
                continue
            q = Position(x, y)
            d = p.distance_squared(q)
            if best is None or d < best:
                best = d
                tgt = q
        if tgt is None:
            # ⛔ ORDER: FINISH THE CHAIN, THEN TAKE THE NEXT ORE.  A harvester
            # with no route home is worth exactly zero, forever -- and the
            # first cut of this ordering (nearest-of-either) left two of three
            # harvesters ORPHAN at the end of a local game.  The competing
            # failure is real too (belt-first with a `is_in_vision` freshness
            # test walked at unreachable tiles forever and finished with TWO
            # harvesters), which is why `belt_built` is a set this file
            # maintains rather than a per-round vision read.
            # v601 BUGFIX: `ore_list()` falls back to LIVE-SENSED ore when the
            # catalogue could not confirm this map.  v600 read `self.map_ores`
            # here, which is empty on 10 of the 15 pool maps -- and this loop
            # is the only thing in the tree that walks a keeper toward ore.
            for ore in self.ore_list():
                if (ore.x, ore.y) in self.harv_tiles or not self.is_home_half(ore):
                    continue
                if self.belt_plan.get((ore.x, ore.y)) is not None:
                    continue
                if self._harv_blocked(ct, (ore.x, ore.y), rnd):
                    continue        # PLANK 1: do not walk to a banned killzone
                d = p.distance_squared(ore)
                if best is None or d < best:
                    best = d
                    tgt = ore
        if tgt is None and not self.ore_list() and self.map_grid is None:
            # v601 BUGFIX, second half: sensing only helps a body that is ever
            # somewhere new.  Measured on stavkirke seed 11: the v600 keeper
            # oscillated between (8,3) and (8,4) beside its own core for the
            # whole match with grid=False, ores=0, harv=0.
            tgt = self.explore_step(ct, p, rnd)
        if tgt is None:
            tgt = self.core
        self.step_to(ct, tgt)

    def _belt_watch(self, ct, p):
        """Keep `belt_built` honest: a planned tile we can SEE to be empty is
        no longer built.  This is what makes the V1 rebuild counter count
        rebuilds rather than builds.
        """
        for xy in list(self.belt_built):
            q = Position(xy[0], xy[1])
            if not self.ibp(q) or p.distance_squared(q) > 20:
                continue
            try:
                if not ct.is_in_vision(q):
                    continue
                if ct.get_tile_building_id(q) is None:
                    self.belt_built.discard(xy)
                    # v601 PLANK 1, DISCLOSED WIDENING: the brief specifies the
                    # killer channel for HARVESTER tiles.  A conveyor dies to
                    # the same annulus gunner (37 of 37 belt kills in the tape
                    # came from a gunner at d^2 20-100 of our core, the same
                    # band as all 33 harvester kills), and PLANK 1's ledger
                    # ALREADY counts conveyor rebuilds -- it just never named
                    # the shooter.  Naming it here is what gives PLANK 2 a
                    # target to cover when PLANK 1 is working well enough that
                    # no harvester tile ever escalates.
                    if SK_HARV_ESCALATE:
                        k = self._infer_killer(xy)
                        if k is not None:
                            self.killer_pos = k
                            self.killer_rnd = ct.get_current_round()
            except Exception:
                continue
        # ⛔ v601: THE REFUTATION HALF OF AN OPTIMISTIC PLAN.  Without a
        # confirmed grid the planner treats UNSEEN as passable, so a route can
        # be laid through a wall.  A planned tile that vision shows to be WALL
        # is banned and the plan re-runs -- otherwise the keeper walks to a
        # tile it can never build on and stands there.
        if self.map_grid is not None or not self.belt_plan:
            return
        for xy in list(self.belt_plan):
            if xy in self.map_walls:
                continue
            q = Position(xy[0], xy[1])
            if not self.ibp(q) or p.distance_squared(q) > 20:
                continue
            try:
                if not ct.is_in_vision(q):
                    continue
                if ct.get_tile_env(q) != Environment.WALL:
                    continue
            except Exception:
                continue
            self.map_walls.add(xy)
            self.belt_ban.add(xy)
            self.belt_key = None

    def _belt_report(self, ct, rnd):
        """SK_SLOT_BELT (writer: HOME KEEPER) -- connectivity, the #78 metric.

        Connected = every tile of this harvester's chain, from its head to the
        tile that faces the core, has actually been built.  Fidelity target:
        83% harvester->core connectivity (ours today: 58.8%).
        """
        conn = 0
        for h in self.harv_tiles:
            cur = self.belt_head.get(h)
            if cur is None:
                conn += 1                       # harvester feeds the core direct
                continue
            ok = True
            hops = 0
            while hops < 200:
                if cur not in self.belt_plan:
                    ok = False
                    break
                if cur not in self.belt_built:
                    ok = False
                    break
                nxt = self._belt_next(cur)
                if nxt is None:
                    ok = False
                    break
                if self.core is not None and adjacent_to_core(Position(cur[0], cur[1]), self.core):
                    break
                cur = nxt
                hops += 1
            if ok:
                conn += 1
        word = (1 if conn and conn == len(self.harv_tiles) else 0)
        word |= ((rnd + 1) & SK_BEAT_MASK) << 1
        word |= (min(conn, 63) & 0x3F) << 12
        word |= (self._belt_uncovered(ct) & 0x3F) << 18   # §2.8(b) measured gap
        self.wstore(ct, SK_SLOT_BELT, word)

    def _belt_next(self, xy):
        face = self.belt_plan.get(xy)
        if face is None:
            return None
        dx, dy = face.delta()
        return (xy[0] + dx, xy[1] + dy)

    # ==================================================================
    # v601 PLANK 3 -- SK_TARGET_PRIO: ONE target ladder, guns AND pecks
    # ==================================================================
    # CAUSE 3 of the tape30 autopsy.  100% of the 9,126 damage ever landed on
    # our core came from enemy SENTINELS standing at d^2 2-25 -- zero from
    # gunners, zero from pecks.  18 of 24 enemy forward sentinels and 4 of 4
    # forward gunners were never removed.  And we are not short of output: we
    # out-peck them 1,712 to 54.  We spend it on the wrong thing --
    #   our turret shots 821: BARRIER 618 (75.3%), core 92, body 58,
    #                          sentinel 33, launcher 20, GUNNER 0
    #   our pecks      1,712: BARRIER 1,280 (74.8%), core 366, sentinel 31,
    #                          conveyor 16, harvester 15, gunner 4
    # So the door problem is TARGET SELECTION, not volume.

    def _marked_positions(self, ct):
        """Tiles carrying something that has demonstrably hurt us: the enemy
        turret the CORE published as the newest home threat (slot 2), and the
        belt killer PLANK 1 inferred (slot 14).  These are class (a).
        """
        out = set()
        if not SK_TARGET_PRIO:
            return out
        try:
            t = unpack_pos(ct.read_store(SK_SLOT_THREAT_POS))
        except Exception:
            t = None
        if t is not None and self.ibp(t):
            out.add((t.x, t.y))
        k = self.killer_pos
        if k is None:
            k = self.killer_word_pos(ct)
        if k is not None:
            out.add((k.x, k.y))
        for xy in self.harv_killer.values():
            out.add((xy.x, xy.y))
        return out

    def _target_pri(self, et, xy, marked):
        """The strict ladder.  A BARRIER scores SK_PRI_BARRIER = 0 and 0 is
        never fired at by default -- barriers are only ever attacked by the
        verb whose PATH they block (`_clear_tile`'s cage-lap eviction).
        """
        if et == EntityType.CORE:
            return SK_PRI_CORE
        if et in ARMED_TYPES:
            return SK_PRI_MARKED if xy in marked else SK_PRI_TURRET
        if et == EntityType.HARVESTER:
            return SK_PRI_HARVESTER
        if et == EntityType.BUILDER_BOT:
            return SK_PRI_BODY
        if et == EntityType.BARRIER:
            return SK_PRI_BARRIER
        return SK_PRI_OTHER

    def _enemy_builder_adjacent(self, ct, q):
        """DOORWAVE's lesson, applied to PECKS only.

        A builder peck is 2 damage; an enemy heal is +4 HP for 1 Ti on every
        friendly entity on the tile.  A peck against a target a live enemy body
        is standing next to LOSES THE HEALING RACE and every round spent on it
        is a round not spent on something that dies.  Guns do not care -- a
        gunner does 7 and a sentinel 18 -- so this guard is deliberately not
        applied in `_turret`.
        """
        for d in CARDINALS:
            r = q.add(d)
            if not self.ibp(r):
                continue
            try:
                uid = ct.get_tile_builder_bot_id(r)
                if uid is None:
                    continue
                if ct.get_team(uid) != self.team:
                    return True
            except Exception:
                continue
        return False

    def _peck_priority(self, ct, p, rnd):
        """Peck the highest-class adjacent enemy.  True if it took the turn.

        ⛔ IT NEVER PECKS A BARRIER OR A BELT PIECE.  Those are class (d) and
        belong to the verbs that need the tile cleared -- `_clear_tile` for the
        cage lap, `_melee_harvester` for the denier's own quarry.  This method
        exists to make sure that when a TURRET or the enemy CORE is within
        reach, the 2 damage goes there instead.
        """
        if not SK_TARGET_PRIO:
            return False
        if ct.get_global_resources() < 2:
            return False
        marked = self._marked_positions(ct)
        best = None
        best_q = None
        best_id = None
        for d in CARDINALS:
            q = p.add(d)
            if not self.ibp(q):
                continue
            try:
                bid = ct.get_tile_building_id(q)
            except Exception:
                continue
            if bid is None:
                continue
            try:
                if ct.get_team(bid) == self.team:
                    continue
                et = ct.get_entity_type(bid)
            except Exception:
                continue
            pri = self._target_pri(et, (q.x, q.y), marked)
            if pri <= SK_PRI_OTHER:
                continue                    # barriers and belt: not here
            if self.gave_up(bid, rnd):
                continue
            if self._enemy_builder_adjacent(ct, q):
                continue                    # the healing race, see above
            try:
                hp = ct.get_hp(bid)
            except Exception:
                continue
            score = (pri, -hp)
            if best is None or score > best:
                best = score
                best_q = q
                best_id = bid
        if best_q is None:
            return False
        # ⛔ V7 IS ASKED ONCE, ON THE WINNER.  `hp_trend_ok` MUTATES the per-unit
        # HP memo and can latch a give-up; running it over every candidate would
        # retire targets this body never even shot at.
        if not self.hp_trend_ok(ct, best_id, rnd):
            return False
        try:
            if ct.can_fire(best_q):
                ct.fire(best_q)
                return True
        except Exception:
            return False
        return False

    # ==================================================================
    # ROLE 1 -- CAGE WALKER  (COPY 9)
    # ==================================================================

    def _cage_walker(self, ct, p, rnd):
        """COPY 9 -- nearest-EMPTY ring tile first, barrier the round AFTER a
        tile clears, walk a LAP not a shuttle, and the seal closes BEHIND the
        walk (ledger V2: 74% of their lost ring barriers were self-demolished
        because a builder cannot stand on its own building).  Accept 7 of 8 --
        the eighth tile is not the plank, the gun is.

        ⛔ SK_CAGE OFF is the ablation identity: the walker still marches and
        still melees the enemy core, but places ZERO barriers on the enemy
        ring, which is exactly the metric the fidelity instrument reads.
        """
        if self.enemy is None:
            return
        lap = cage_lap(self.enemy)
        sealed, empty_seals = self._cage_survey(ct, lap)
        self._cage_report(ct, rnd, sealed)

        if not SK_CAGE:
            self._attack_enemy_core(ct, p, rnd)
            return

        # V9: the stall branch flips the lap to the band's far quadrant.
        branch = (ct.read_store(SK_SLOT_STALL) & STALL_BRANCH_BIT) != 0

        if sealed >= SK_CAGE_ACCEPT:
            self._attack_enemy_core(ct, p, rnd)
            return

        here = None
        for i, t in enumerate(lap):
            if t.x == p.x and t.y == p.y:
                here = i
                break

        if ct.get_action_cooldown() == 0 and here is not None:
            # SEAL BEHIND: the tile we just left, never the one we stand on.
            back = (here - 1) % 12
            if back in LAP_SEAL_IDX and self._seal_tile(ct, lap[back], rnd):
                return
            # ⭐ v601 PLANK 3.  AFTER the seal (COPY 9 is still the walker's
            # job) and BEFORE the eviction: if an enemy TURRET or their CORE is
            # orthogonally adjacent, the 2 damage goes there instead of into a
            # 30 HP barrier.  1,280 of our 1,712 pecks went into barriers and
            # this is the tile where most of them were spent.
            if self._peck_priority(ct, p, rnd):
                return
            # COPY 9.1: take the nearest EMPTY ring tile FIRST and come back
            # for the occupied ones by eviction.  ⛔ MEASURED: without the
            # `not empty_seals` guard the walker met one enemy conveyor on the
            # next lap tile at r23 and chewed it for nine rounds -- standing
            # inside their sentinel's reach -- while FOUR empty seal tiles sat
            # unbuilt, and died before it sealed one.  Eviction is the second
            # pass, not the first.
            fwd = (here + 1) % 12
            if not empty_seals and self._clear_tile(ct, lap[fwd], rnd):
                return

        if here is not None:
            # ⛔ SKIP-AHEAD, and it is a MEASURED fix, not a nicety: with a
            # plain `lap[here+1]` the walker froze for the rest of the match
            # the first time an enemy BODY parked on the next lap tile
            # (`_clear_tile` only answers BUILDINGS, and `_bfs_direction`
            # treats a body as blocked, so the flood returned CENTRE and the
            # lap never advanced -- 0 of 8 sealed in a 131-round local game).
            # A lap that cannot pass a tile walks PAST it and comes back.
            for k in range(1, 12):
                step = lap[(here + k) % 12]
                if not self.ibp(step) or not self._lap_free(ct, step):
                    continue
                self.step_to(ct, step)
                return
        # Not on the lap yet: COPY 9.1, take the NEAREST EMPTY ring tile first.
        tgt = None
        best = None
        pool = empty_seals if empty_seals else [lap[i] for i in LAP_SEAL_IDX]
        if branch and len(pool) > 1:
            pool = list(reversed(pool))
        for q in pool:
            if not self.ibp(q):
                continue
            d = p.distance_squared(q)
            if best is None or d < best:
                best = d
                tgt = q
        self.step_to(ct, tgt if tgt is not None else self.enemy)

    def _lap_free(self, ct, q):
        """Can the walker stand on this lap tile?  Unseen tiles read free --
        the flood will find out, and refusing to walk toward what we cannot
        see is how a lap turns into a shuttle."""
        try:
            if not ct.is_in_vision(q):
                return True
            if ct.get_tile_env(q) == Environment.WALL:
                return False
            if ct.get_tile_building_id(q) is not None:
                return False
            return ct.get_tile_builder_bot_id(q) is None
        except Exception:
            return False

    def _cage_survey(self, ct, lap):
        """(sealed count, list of EMPTY seal tiles) from what we can see."""
        sealed = 0
        empties = []
        for i in LAP_SEAL_IDX:
            q = lap[i]
            if not self.ibp(q):
                sealed += 1                     # off-map faces cannot be walked
                continue
            try:
                if not ct.is_in_vision(q):
                    if (q.x, q.y) in self.cage_sealed:
                        sealed += 1
                    continue
                env = ct.get_tile_env(q)
                if env == Environment.WALL:
                    sealed += 1
                    self.cage_sealed.add((q.x, q.y))
                    continue
                bid = ct.get_tile_building_id(q)
            except Exception:
                continue
            if bid is None:
                empties.append(q)
                self.cage_sealed.discard((q.x, q.y))
                continue
            try:
                if ct.get_team(bid) == self.team:
                    sealed += 1
                    self.cage_sealed.add((q.x, q.y))
                else:
                    self.cage_sealed.discard((q.x, q.y))
            except Exception:
                continue
        return sealed, empties

    def _seal_tile(self, ct, q, rnd):
        """Barrier one ring tile.  The build happens the round AFTER the tile
        clears (mean latency 1.08 in the doctrine we replicate) because the
        clear is a melee that consumes this turn's action.
        """
        if not self.ibp(q) or not self.may_build(q, OWNER_CAGE):
            return False
        if self.free_neighbours(ct, ct.get_position(), exclude=q) == 0:
            return False                        # self-trap guard
        cost = ct.get_barrier_cost()
        if ct.get_global_resources() < cost:
            return False
        try:
            if not ct.can_build_barrier(q):
                return False
            ct.build_barrier(q)
        except Exception:
            return False
        self.cage_sealed.add((q.x, q.y))
        self.cage_advance = rnd
        return True

    def _clear_tile(self, ct, q, rnd):
        """Evict whatever occupies the next lap tile: ten builder attacks into
        a 20 HP conveyor, fifteen into a 30 HP harvester.  SK_CAGE_MELEE_GIVEUP
        caps the chew so a hard tile cannot own the walker for the game.
        """
        if not self.ibp(q) or ct.get_global_resources() < 2:
            return False
        try:
            bid = ct.get_tile_building_id(q)
        except Exception:
            return False
        if bid is None:
            return False
        try:
            if ct.get_team(bid) == self.team:
                return False
        except Exception:
            return False
        # ⭐ v601 PLANK 3(d).  A barrier IS allowed here -- it is blocking the
        # lap, which is the "path the current action needs" carve-out.  What is
        # NOT allowed is chewing one an enemy body is standing beside: 2 damage
        # against +4 HP a round is a race we lose, and this is where the bulk
        # of the 1,280 barrier pecks went (`_v542wave`'s MAINTAINED seal).
        if SK_TARGET_PRIO and self._enemy_builder_adjacent(ct, q):
            return False
        if self.melee_tile != (q.x, q.y):
            self.melee_tile = (q.x, q.y)
            self.melee_since = rnd
        elif rnd - self.melee_since > SK_CAGE_MELEE_GIVEUP:
            return False
        if not self.hp_trend_ok(ct, bid, rnd):
            return False
        try:
            if ct.can_fire(q):
                ct.fire(q)
                return True
        except Exception:
            return False
        return False

    def _attack_enemy_core(self, ct, p, rnd):
        """Strangle-then-KILL: the cage is a means, the core is the end."""
        if self.enemy is None:
            return
        if ct.get_action_cooldown() == 0 and ct.get_global_resources() >= 2:
            for c in core_tiles(self.enemy):
                if abs(c.x - p.x) + abs(c.y - p.y) != 1:
                    continue
                try:
                    if ct.can_fire(c):
                        ct.fire(c)
                        return
                except Exception:
                    continue
            # v601 PLANK 3: not adjacent to the core -- take the highest-class
            # adjacent enemy instead of walking past a live sentinel.
            if self._peck_priority(ct, p, rnd):
                return
        self.step_to(ct, self.enemy)

    def _cage_report(self, ct, rnd, sealed):
        """SK_SLOT_CAGE (writer: CAGE WALKER) -- seal count + last advance."""
        if sealed > self.cage_best:
            self.cage_best = sealed
            self.cage_advance = rnd
        word = min(sealed, 31) & CAGE_SEALED_MASK
        adv = self.cage_advance if self.cage_advance >= 0 else -1
        word |= (((adv + 1) & SK_BEAT_MASK) << CAGE_BEAT_FIELD)
        self.wstore(ct, SK_SLOT_CAGE, word)

    # ==================================================================
    # ROLE 2 -- ORE DENIER  (COPY 1)
    # ==================================================================

    def _ore_denier(self, ct, p, rnd):
        """COPY 1 -- the trigger is MAP-FREE and needs no scouting: when an
        enemy harvester on tile T dies, build a barrier on T (their 92.5% at
        median 1-round latency against a 1.0% placebo).  Plus the pre-emptive
        half: unharvested ore in THEIR half from ~r60.

        ⛔ PROGRAMME rider: argued as OPENS THE LANE -- a starved opponent buys
        fewer turrets and fewer turrets is what lets our gun live -- never as
        economy.  Its only direct channel is their `titanium_collected`, which
        is off-currency under R1000_IS_DEFEAT.

        ⛔ SK_ORE_DENY OFF is the ablation identity: the body still hunts and
        melees enemy harvesters, but places ZERO barriers on ore tiles -- the
        exact metric on which we currently read 0 of 1,381.
        """
        self._ore_scan(ct, p)                       # v601 BUGFIX SK_ORE_SENSE
        acted = False
        if ct.get_action_cooldown() == 0:
            if SK_ORE_DENY and self._deny_barrier(ct, p, rnd):
                return
            # v601 PLANK 3: an enemy TURRET adjacent to the denier outranks
            # its own quarry -- 4 of 4 enemy forward gunners survived the tape.
            if self._peck_priority(ct, p, rnd):
                return
            acted = self._melee_harvester(ct, p, rnd)
        if acted:
            return
        tgt = self._deny_target(ct, p, rnd)
        self.step_to(ct, tgt if tgt is not None else self.enemy)

    def _deny_barrier(self, ct, p, rnd):
        """The barrier half.  Only ever fires on an ORE tile -- that predicate
        is the whole verb, and its absence is our measured zero.
        """
        cost = ct.get_barrier_cost()
        if ct.get_global_resources() < cost:
            return False
        for d in CARDINALS:
            q = p.add(d)
            if not self.ibp(q):
                continue
            try:
                if ct.get_tile_env(q) != Environment.ORE_TITANIUM:
                    continue
                if ct.get_tile_building_id(q) is not None:
                    continue
            except Exception:
                continue
            killed = (q.x, q.y) in self.enemy_harv
            preempt = (rnd >= SK_PREEMPT_ORE_ROUND and not self.is_home_half(q))
            if not killed and not preempt:
                continue
            if not self.may_build(q, OWNER_DENY):
                continue
            try:
                if not ct.can_build_barrier(q):
                    continue
                ct.build_barrier(q)
            except Exception:
                continue
            self.enemy_harv.pop((q.x, q.y), None)
            self.denied_tiles.add((q.x, q.y))
            self.denied += 1
            return True
        return False

    def _melee_harvester(self, ct, p, rnd):
        """Highest melee count of the four roles: chew enemy harvesters.
        Fifteen attacks into 30 HP -- and being adjacent when it dies is what
        buys COPY 1's 1-round barrier latency.
        """
        if ct.get_global_resources() < 2:
            return False
        for d in CARDINALS:
            q = p.add(d)
            if not self.ibp(q):
                continue
            try:
                bid = ct.get_tile_building_id(q)
                if bid is None or ct.get_team(bid) == self.team:
                    continue
                et = ct.get_entity_type(bid)
            except Exception:
                continue
            if et not in (EntityType.HARVESTER, EntityType.CONVEYOR, EntityType.SPLITTER):
                continue
            if not self.hp_trend_ok(ct, bid, rnd):
                continue
            try:
                if ct.can_fire(q):
                    ct.fire(q)
                    return True
            except Exception:
                continue
        return False

    def _deny_target(self, ct, p, rnd):
        best = None
        tgt = None
        for xy, seen in self.enemy_harv.items():
            q = Position(xy[0], xy[1])
            if not self.ibp(q):
                continue
            d = p.distance_squared(q)
            if best is None or d < best:
                best = d
                tgt = q
        if tgt is not None:
            return tgt
        for eid, et, ep in self.vis_enemy:
            if et != EntityType.HARVESTER:
                continue
            d = p.distance_squared(ep)
            if best is None or d < best:
                best = d
                tgt = ep
        if tgt is not None:
            return tgt
        # PATROL, ungated by round: their harvesters stand ON ore, so ore is
        # where the map-free trigger fires.  Only the pre-emptive BARRIER waits
        # for SK_PREEMPT_ORE_ROUND -- walking there earlier is what puts the
        # denier adjacent when a harvester dies, which is COPY 1's 1-round
        # latency.
        for ore in self.ore_list():        # v601 BUGFIX: sensed-ore fallback
            if self.is_home_half(ore):
                continue
            if (ore.x, ore.y) in self.denied_tiles:
                continue
            d = p.distance_squared(ore)
            if best is None or d < best:
                best = d
                tgt = ore
        return tgt

    # ==================================================================
    # ROLE 3 -- SIEGE ENGINEER  (COPY 5 + V3 + V4 + V9)
    # ==================================================================

    def _siege_engineer(self, ct, p, rnd):
        """COPY 5 -- band-first siting: d^2 14-32 from the enemy core
        footprint, inside sentinel reach (r^2=32) and outside every gunner's
        (r^2=13), worth a measured +30% of turret life; the extreme case is
        d^2 = 32 exactly, on a diagonal, aimed at a footprint corner.  Prepare
        with barriers 1-4 rounds before the gun, INCLUDING inside the firing
        line -- legal because sentinels ignore obstacles.

        ⛔ POINT-BLANK (d^2 <= 13) PLANTS ARE FORBIDDEN IN v1
        (`SK_NEST_POINT_BLANK = False`): their own v47 data says close plants
        die 30% faster, and v68 gets away with it only because its guns clear
        the ring first and a home gun sweeps the answer at 79.7%.  No
        point-blank until our ring clearance measures at parity.

        ⛔ SK_NEST OFF is the ablation identity: the engineer still walks out
        and still holds far ring faces, but plants NO forward turret.
        """
        if self.enemy is None:
            return
        self._nest_watch(ct, rnd)
        self._drip_report(ct, rnd)
        self._stall_check(ct, rnd)

        if not SK_NEST:
            self._attack_enemy_core(ct, p, rnd)
            return

        if self.nest_site is None:
            self.nest_site = self._pick_nest(ct, p, rnd)
        if self.nest_site is None:
            self._attack_enemy_core(ct, p, rnd)
            return
        site = self.nest_site

        if ct.get_action_cooldown() == 0:
            adj = abs(site.x - p.x) + abs(site.y - p.y) == 1
            if adj:
                if self.nest_prepped < SK_NEST_PREP_BARRIERS:
                    if self._prep_barrier(ct, p, site):
                        return
                if self._plant_gun(ct, p, site, rnd):
                    return
        self.step_to(ct, site)

    def _pick_nest(self, ct, p, rnd):
        """The band, with LEDGER V4's per-tile death memory applied.

        Scored: a legal firing line onto the footprint (axial or diagonal,
        since a sentinel shoots one tile wide along its facing), then d^2 as
        close to the band maximum as possible, then proximity to us.
        """
        if self.map_grid is None:
            return None
        ex, ey = self.enemy.x, self.enemy.y
        best = None
        site = None
        lo = SK_NEST_DSQ_MIN if not SK_NEST_POINT_BLANK else 2
        for dx in range(-7, 9):
            for dy in range(-7, 9):
                x, y = ex + dx, ey + dy
                if not self.ib(x, y):
                    continue
                q = Position(x, y)
                d = dsq_core(q, self.enemy)
                if d < lo or d > SK_NEST_DSQ_MAX:
                    continue
                if self.map_grid[y][x] == "#":
                    continue
                if (x, y) in self.nest_deaths and rnd - self.nest_deaths[(x, y)] < SK_DEATH_MEMO_ROUNDS:
                    continue
                face = self._firing_face(q)
                if face is None:
                    continue
                score = (d == SK_NEST_DSQ_MAX and abs(dx) == abs(dy), d, -p.distance_squared(q))
                if best is None or score > best:
                    best = score
                    site = q
            if self._cpu_exhausted(ct):
                break
        if site is not None:
            self.nest_face = self._firing_face(site)
            self.nest_prepped = 0
        return site

    def _firing_face(self, q):
        """The Direction whose single-tile-wide line from q crosses the enemy
        footprint, or None.  Axial or exactly diagonal offsets only.
        """
        for c in core_tiles_xy(self.enemy):
            dx, dy = c[0] - q.x, c[1] - q.y
            if dx == 0 and dy == 0:
                continue
            if dx == 0 or dy == 0 or abs(dx) == abs(dy):
                sx = (dx > 0) - (dx < 0)
                sy = (dy > 0) - (dy < 0)
                for d in DIRECTIONS:
                    if d.delta() == (sx, sy):
                        return d
        return None

    def _prep_barrier(self, ct, p, site):
        """COPY 5's preparation: barriers 1-4 rounds before the gun, including
        inside the firing line (sentinels ignore obstacles).
        """
        cost = ct.get_barrier_cost()
        if ct.get_global_resources() < cost + ct.get_sentinel_cost():
            return False
        for d in CARDINALS:
            q = p.add(d)
            if not self.ibp(q) or (q.x == site.x and q.y == site.y):
                continue
            if q.distance_squared(site) > 4:
                continue
            if not self.may_build(q, OWNER_NEST):
                continue
            if self.free_neighbours(ct, p, exclude=q) == 0:
                continue                        # self-trap guard
            try:
                if not ct.can_build_barrier(q):
                    continue
                ct.build_barrier(q)
            except Exception:
                continue
            self.nest_prepped += 1
            return True
        return False

    def _plant_gun(self, ct, p, site, rnd):
        face = self.nest_face or self._firing_face(site)
        if face is None:
            self.nest_site = None
            return False
        if ct.get_global_resources() < ct.get_sentinel_cost():
            return False
        try:
            if not ct.can_build_sentinel(site, face):
                return False
            tid = ct.build_sentinel(site, face)
        except Exception:
            return False
        self.nest_turret = (tid, site, rnd)
        word = (pack_tile(site) & NEST_SITE_MASK) | (((rnd + 1) & SK_BEAT_MASK) << NEST_RND_FIELD)
        self.wstore(ct, SK_SLOT_NEST, word)
        return True

    def _nest_watch(self, ct, rnd):
        """LEDGER V3 -- a dead forward sentinel is an IMMEDIATE re-site
        decision, not a queue item (their replacement latency: median 33-42
        rounds, p90 111, one watched 90-round hole).  LEDGER V4 -- remember
        that a tile killed what was put on it.
        """
        if self.nest_turret is None:
            return
        tid, site, born = self.nest_turret
        alive = True
        try:
            alive = ct.get_hp(tid) > 0
        except Exception:
            alive = False
        if alive:
            return
        self.nest_deaths[(site.x, site.y)] = rnd            # V4
        life = rnd - born
        self.nest_lives.append(life)
        self.nest_turret = None
        self.nest_site = None                               # V3: re-site NOW
        self.nest_face = None
        self.nest_prepped = 0

    def _drip_report(self, ct, rnd):
        """SK_SLOT_DRIP (writer: SIEGE ENGINEER) -- the FORWARD half of COPY
        7's `need`.  The core counts what it can see; forward turrets sit
        outside its vision, so the one body that stands with them reports how
        many WILL FIRE next round (a live turret with an enemy in its reach).
        """
        guns = sents = 0
        for eid, et, ep in self.vis_friend:
            if et not in TURRET_TYPES:
                continue
            if self.core is not None and dsq_core(ep, self.core) <= 36:
                continue                       # the core counts those itself
            reach = 13 if et == EntityType.GUNNER else 32
            hot = False
            for _eid, _et, epos in self.vis_enemy:
                if ep.distance_squared(epos) <= reach:
                    hot = True
                    break
            if not hot:
                continue
            if et == EntityType.GUNNER:
                guns += 1
            else:
                sents += 1
        self.wstore(ct, SK_SLOT_DRIP,
                    (min(guns, 63) & DRIP_GUN_MASK)
                    | ((min(sents, 63) & DRIP_GUN_MASK) << DRIP_SENT_FIELD))

    def _stall_check(self, ct, rnd):
        """LEDGER V9 -- a plan B.  If the seal has not advanced in
        SK_STALL_ROUNDS rounds AND forward turret lifetime is below
        SK_STALL_LIFETIME, flip the doctrine branch: the nest shifts to the
        band's FAR quadrant and the walker re-routes (it reads this bit).
        391 rounds of the same four jobs, and 14 forward turrets fed to an
        adjacent-answering opponent at a median age of 7, is the measured
        alternative.
        """
        cage = ct.read_store(SK_SLOT_CAGE)
        adv = (cage >> CAGE_BEAT_FIELD) & SK_BEAT_MASK
        lives = self.nest_lives
        mean_life = (sum(lives) // len(lives)) if lives else 99
        stalled = (adv != 0 and rnd - (adv - 1) > SK_STALL_ROUNDS
                   and mean_life < SK_STALL_LIFETIME)
        word = ((rnd + 1) & SK_BEAT_MASK)
        word |= (min(len(lives), 63) & STALL_DEATH_MASK) << STALL_DEATH_FIELD
        if stalled or self.stall_latched:
            self.stall_latched = True
            word |= STALL_BRANCH_BIT
            if self.nest_site is not None and not self.stall_shifted:
                self.stall_shifted = True
                self.nest_site = None          # re-site into the far quadrant
        word |= (min(mean_life, 63) & STALL_LIFE_MASK) << STALL_LIFE_FIELD
        self.wstore(ct, SK_SLOT_STALL, word)

    # ==================================================================
    # SURVIVAL BRANCH (ledger V5)
    # ==================================================================

    def _home_defence(self, ct, p, rnd):
        """LEDGER V5 -- denial verbs yield to survival when the core is under
        fire (three ore barriers in seventeen rounds, in a game lost at r116).
        Returns True when it consumed the turn.
        """
        if self.core is None:
            return False
        if dsq_core(p, self.core) > 200:
            return False
        threat = unpack_pos(ct.read_store(SK_SLOT_THREAT_POS))
        if threat is None or not self.ibp(threat):
            return False
        if ct.get_action_cooldown() == 0 and ct.get_global_resources() >= 2:
            if abs(threat.x - p.x) + abs(threat.y - p.y) == 1:
                try:
                    if ct.can_fire(threat):
                        ct.fire(threat)
                        return True
                except Exception:
                    pass
        self.step_to(ct, threat)
        return True

    # ==================================================================
    # TURRETS  (COPY 6a: shoot what gets planted -- their 61.9%)
    # ==================================================================

    def _turret(self, ct):
        """Gunner / sentinel.

        ⛔ THE AMMO GUARD IS NOT OPTIONAL.  `can_fire` returns TRUE at 0 ammo
        (can_fire@0x16280 has no ammo reference); the check lives in
        finish_firing_turret@0x26eac and RAISES, and an escaping exception
        destroys this turret permanently.  So the price is checked against the
        team's global balance before every shot.
        """
        p = ct.get_position()
        self._boot(ct, p)
        rnd = ct.get_current_round()
        if self.core is None:
            for eid in ct.get_nearby_buildings():
                try:
                    if (ct.get_entity_type(eid) == EntityType.CORE
                            and ct.get_team(eid) == self.team):
                        self.core = ct.get_position(eid)
                        break
                except Exception:
                    continue
        kind = ct.get_entity_type()
        price = SK_AMMO_SENTINEL if kind == EntityType.SENTINEL else SK_AMMO_GUNNER
        if ct.get_action_cooldown() != 0:
            return
        if ct.get_global_ammo() < price:
            return
        try:
            tiles = ct.get_attackable_tiles()
        except Exception:
            return
        best = None
        target = None
        marked = self._marked_positions(ct)
        for q in tiles:
            if not self.ibp(q):
                continue
            try:
                bid = ct.get_tile_building_id(q)
                uid = ct.get_tile_builder_bot_id(q)
            except Exception:
                continue
            for eid in (bid, uid):
                if eid is None:
                    continue
                try:
                    if ct.get_team(eid) == ct.get_team():
                        continue
                    et = ct.get_entity_type(eid)
                except Exception:
                    continue
                if self.gave_up(eid, rnd):
                    continue
                if SK_TARGET_PRIO:
                    # ⭐ v601 PLANK 3.  ⛔ NOTE WHAT THIS REPLACES: v600's top
                    # class was "anything on our home ring", BARRIERS INCLUDED,
                    # which is a large part of how 618 of our 821 turret shots
                    # landed on a wall.  A barrier is scored 0 and 0 never
                    # fires -- an enemy barrier is not what is killing us, and
                    # a shot not taken is 4 or 10 ammo the drip need not buy.
                    pri = self._target_pri(et, (q.x, q.y), marked)
                    if pri <= SK_PRI_BARRIER:
                        continue
                    if (pri == SK_PRI_TURRET and self.core is not None
                            and dsq_core(q, self.core) <= SK_HOME_RING_DSQ):
                        pri = SK_PRI_MARKED    # on OUR door: class (a) as well
                else:
                    # COPY 6a's priority: what got planted on our door first,
                    # then their turrets, then bodies, then anything.
                    pri = 0
                    if self.core is not None and dsq_core(q, self.core) <= SK_HOME_RING_DSQ:
                        pri = 4
                    elif et in TURRET_TYPES:
                        pri = 3
                    elif et == EntityType.BUILDER_BOT:
                        pri = 2
                    elif et == EntityType.CORE:
                        pri = 5
                    else:
                        pri = 1
                score = (pri, -p.distance_squared(q))
                if best is None or score > best:
                    best = score
                    target = (q, eid)
        if target is None:
            self._rotate_toward(ct, p, kind)
            return
        q, eid = target
        if not self.hp_trend_ok(ct, eid, rnd):     # ledger V7
            self._rotate_toward(ct, p, kind)
            return
        try:
            if ct.can_fire(q):
                ct.fire(q)
        except Exception:
            return

    def _rotate_toward(self, ct, p, kind):
        """Gunner-only: 10 Ti and one round of cooldown to face a target that
        the current line cannot reach.  A sentinel cannot rotate at all --
        which is COPY 2 seen from our own side.
        """
        if kind != EntityType.GUNNER:
            return
        if ct.get_global_resources() < 30:
            return
        marked = self._marked_positions(ct)
        for _eid, et, ep in self.enemy_ids_near(ct):
            if p.distance_squared(ep) > 13:
                continue
            # v601 PLANK 3: 10 Ti and a round of cooldown to turn and face a
            # BARRIER is the same error as shooting it, only more expensive.
            if (SK_TARGET_PRIO
                    and self._target_pri(et, (ep.x, ep.y), marked)
                    <= SK_PRI_OTHER):
                continue
            face = p.direction_to(ep)
            try:
                if not ct.can_fire_from(p, face, EntityType.GUNNER, ep):
                    continue
                if ct.can_rotate(face):
                    ct.rotate(face)
                    return
            except Exception:
                continue


def _card(dx, dy):
    if dx > 0:
        return Direction.EAST
    if dx < 0:
        return Direction.WEST
    if dy > 0:
        return Direction.SOUTH
    return Direction.NORTH
