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
    OWNER_BELT, OWNER_CAGE, OWNER_DENY, OWNER_DOOR, OWNER_NEST, OWNER_NONE,
    adjacent_to_core, core_ring, core_seats, core_tiles, core_tiles_xy,
    dist_core, dsq_core, in_bounds, pack_pos, pack_tile, unpack_pos,
    unpack_tile,
)
from sk_maps import (
    BELT_TYPES,
    ARMED_TYPES,
    CARDINALS, CARD_DELTAS, DIRECTIONS,
    SK_AMMO_FLOOR, SK_AMMO_GUNNER, SK_AMMO_SENTINEL,
    SK_BEAT_MASK, SK_BEAT_STALE, SK_BELT, SK_BELT_COVER,
    SK_BELT_COVER_TRIGGER, SK_CAGE, SK_CAGE_ACCEPT, SK_CAGE_FIRST,
    SK_CYCLE_BREAK, SK_CYCLE_ESCAPE_BLOCKED, SK_CYCLE_ESCAPE_CAP,
    SK_CYCLE_ESCAPE_ROUNDS, SK_NEST_STUCK_ROUNDS, SK_SENSE_NAV,
    SK_NEST_STUCK_FIX, SK_NEST_STUCK_BOX, SK_NEST_STUCK_FAR,
    SK_S2_PRIORITY, SK_S2_PRIORITY_MAX, SK_S2_DEFER_GUNS,
    SK_S2_DEFER_BARRIERS,
    SK_STALL_NETDISP, SK_STALL_COMMIT,
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
    # --- v603 -------------------------------------------------------------
    SK_CAGE_ACCEPT_MIN, SK_CAGE_CEIL, SK_COLLAR_GUNS, SK_COLLAR_PECK_CAP,
    SK_COLLAR_ROUTE_GATE, SK_CORE_PECK_HEALGUARD, SK_HOMEDEF_SKIP_BARRIER,
    SK_IDLE_ACT,
    SK_LAP_ADJ_SEAL,
    SK_EVICT_ARMED, SK_NEST_PAIR, SK_NEST_PAIR_MIN_GAP, SK_NEST_PAIR_N,
    SK_TRUNK_NEAR, SK_TRUNK_SEAT_WEIGHT, SK_TRUNK_TERM_WEIGHT,
    # --- v604 -------------------------------------------------------------
    SK_BELT_EST, SK_BELT_EST_STALE_BUILT, SK_BELT_EST_TTL,
    SK_CURSOR_GIVEUP, SK_CYCLE_COMMIT_SLACK, SK_CYCLE_K, SK_ONE_CURSOR,
    # --- v605 -------------------------------------------------------------
    SK_NEST_EXIT,
    # --- v606 -------------------------------------------------------------
    SK_BELT_BAND_AVOID, SK_BELT_BAND_DROP, SK_BELT_BAND_DSQ,
    SK_CYCLE_ALL_ROLES, SK_IDLE_ACT_ENGINEER,
    # --- v608 -------------------------------------------------------------
    SK_COREFIRE, SK_COREFIRE_TTL, SK_CORE_MEDIC, SK_MEDIC_TI_FLOOR,
    SK_MEDIC_HELP_HP, SK_MEDIC_SEAT_DSQ, SK_COUNTER_PECK,
    SK_COUNTER_PECK_DSQ, SK_COUNTER_RAY_ONLY, SK_COUNTER_SENT,
    SK_COUNTER_RNDS,
    SK_COUNTER_SENT_CAP, SK_COUNTER_SENT_RESERVE,
    SK_SLOT_COREFIRE,
    # --- v609 -------------------------------------------------------------
    SK_COUNTER_YIELD_HOME, SK_COUNTER_YIELD_DSQ, SK_COUNTER_HP_MAX,
    SK_COUNTER_LIVE_TGT, SK_COUNTER_SOFT_BODIES,
    # --- v610 -------------------------------------------------------------
    SK_SEAT_CLEAR, SK_SEAT_CLEAR_N, SK_SEAT_PECK_CAP, SK_SEAT_PECK_TOTAL,
    SK_SEAT_GUN_RACE, SK_SEAT_GUNS,
    SK_TERMINATE, SK_TERM_FIRST, SK_TERM_MOVE,
    # --- v611 -------------------------------------------------------------
    SK_HOME_LAUNCHER, SK_HOME_LAUNCHER_MAX, SK_HL_MIN_ROUND, SK_HL_SITE_DSQ,
    SK_HL_SITE_MIN_COVER, SK_HL_THROW_MIN_DSQ, SK_HL_THROW_MAX_DSQ,
    SK_HL_PICKUP_DSQ, SK_HL_RESERVE, SK_HL_PROBE_CAP, SK_HL_DROP_RING_DSQ,
    SK_HL_SEAT_DENSITY, SK_HL_TEAM_CHECK, SK_HL_VICTIM_SEAT_ONLY,
    SK_HL_SITE_GIVEUP, SK_HL_SITE_TRIES, SK_HL_AFTER_S2,
    # --- v612 -------------------------------------------------------------
    SK_MARCH_TEAMCHECK, SK_HOMEDEF_TEAMCHECK,
    # --- v613 (the ANTI-APRON axis) ---------------------------------------
    SK_APRON_DENY, SK_APRON_DSQ, SK_APRON_RELAY_CAP, SK_APRON_WINDOW,
    SK_APRON_RELAY_TOTAL, SK_APRON_BELT_PREF,
    SK_TUBE_FLOOR, SK_TUBE_NOPREP, SK_TUBE_FUND, SK_TUBE_FUND_AMMO,
    SK_TUBE_GAP_RELAX, SK_TUBE_GAP_MIN,
    SK_PECK_FOCUS, SK_PECK_FOCUS_DSQ, SK_PECK_FOCUS_BODIES,
    SK_PECK_FOCUS_KEEPER,
    SK_PLUCK_AWARE, SK_PLUCK_DSQ, SK_PLUCK_RETARGET, SK_PLUCK_MEMO_TTL,
    SK_CORE_MEDIC_RIDER,
    # --- v617 (the PRODUCER FIX) ------------------------------------------
    SK_TEAM_TUBES, SK_TUBE_BEAT_MASK, SK_TUBE_SEAT_FIELDS, SK_TUBE_STALE,
    SK_TUBE_BAND_DSQ, SK_TUBE_PHASES,
    # --- v618 (the SEAT-DEFENCE PACKAGE) ----------------------------------
    SK_SEAT_CLAIM, SK_SEAT_CLAIM_UNTIL, SK_SEAT_CLAIM_MAX, SK_SEAT_CLAIM_WALK,
    SK_SEAT_CLAIM_ENEMY_FIRST,
    SK_SEAT_CLAIM_WALK_DSQ, SK_SEAT_CLAIM_SPAWN_RESERVE,
    SK_HOME_GUNNER, SK_HOME_GUN_MAX, SK_HOME_GUN_MIN_ROUND,
    SK_HOME_GUN_MAX_ROUND, SK_HOME_GUN_RESERVE, SK_HOME_GUN_SEPARATE_CAP,
    SK_HOME_GUN_ROTATE, SK_HOME_GUN_ROT_CAP,
    SK_GUN_ROUTEBLOCK, SK_ROUTEBLOCK_PRI, SK_ROUTEBLOCK_ADJ, SK_ROUTEBLOCK_DSQ,
    SK_SEAT_HEAL, SK_SEAT_HEAL_MAX, SK_SEAT_HEAL_TI_FLOOR,
    SK_SEAT_HEAL_PECK_MAX, SK_SEAT_HEAL_GUN_RACE, SK_SEAT_HEAL_WALK,
    SK_PECK_DEMOTE,
    # --- v619 (THE KILL SIDE) ---------------------------------------------
    SK_NEST_N3, SK_TUBE_ENG_SLOT7,
    SK_S2_HASTE, SK_S2_HASTE_SAME_ROUND,
    SK_TUBE_RELIGHT, SK_RELIGHT_PREP_DSQ,
    SK_RELIGHT_TRUEDEATH, SK_RELIGHT_PREP, SK_RELIGHT_CLOSE,
    SK_RENT, SK_RENT_COVER_DSQ, SK_RENT_MIN_ROUND, SK_RENT_ORPHAN_AGE,
    SK_RENT_PRE_BUY, SK_RENT_MAX_PER_TURN,
    # --- v620 (THE TWO SUCCESSOR ITEMS) ------------------------------------
    SK_TUBE_FLOOR2, SK_TUBE_FLOOR2_N, SK_TUBE_FLOOR2_GRACE,
    SK_TUBE_FLOOR2_PREPREP, SK_TUBE_FLOOR2_PREPREP_MAX, SK_TUBE_FLOOR2_STAGE,
    SK_RENT_EARLY, SK_RENT_EARLY_RESITE, SK_RENT_EARLY_AGE,
    SK_RENT_EARLY_AGE_N, SK_RENT_EARLY_WINDOW, SK_RENT_EARLY_STEP,
    SK_RENT_STEP_BUDGET,
)

# --- v611: the 8 neighbours, for a LAUNCHER's pickup disc (d^2 <= 2) --------
NEIGHBOURS8 = ((0, -1), (1, -1), (1, 0), (1, 1),
               (0, 1), (-1, 1), (-1, 0), (-1, -1))

# --- v620 PLANK 2(c): the four DIAGONALS, and the cardinal each delta names.
# ⛔ BUILT BY ITERATING `Direction`, NOT HAND-LISTED.  A hand-listed compass is
# how a delta convention drifts from the engine's ((0,-1) is NORTH), and this
# tree has already paid for one of those.  `is_cardinal()` is the engine's own
# predicate, so the two tuples partition the eight directions by definition.
DIAGONALS = tuple(d for d in Direction
                  if d != Direction.CENTRE and not d.is_cardinal())
DELTA_DIR = dict((d.delta(), d) for d in Direction
                 if d != Direction.CENTRE and d.is_cardinal())

# --- v604 FIX 4: slot 5 b24-31, the eight TERMINUS seats -------------------
BELT_TERM_FIELD = 24      # slot 5 b24-31 (8 bits, one per canonical seat)
BELT_TERM_MASK = 0xFF

SEAT_MASK = 0xFF          # slot 0 b0-7
CAGE_SEALED_MASK = 0x1F   # slot 6 b0-4
CAGE_BEAT_FIELD = 5       # slot 6 b5-15
NEST_SITE_MASK = 0x3FF    # slot 7 b0-9   (pack_tile)
NEST_RND_FIELD = 10       # slot 7 b10-20
NEST_SITE2_BIT = 1 << 21  # slot 7 b21    second band site present   (v603)
NEST_SITE2_DX_FIELD = 22  # slot 7 b22-26 dx+15 of site2 from site1  (v603)
NEST_SITE2_DY_FIELD = 27  # slot 7 b27-31 dy+15 of site2 from site1  (v603)
STALL_DEATH_FIELD = 11    # slot 9 b11-16
STALL_DEATH_MASK = 0x3F
STALL_BRANCH_BIT = 1 << 17
STALL_LIFE_FIELD = 18     # slot 9 b18-23
STALL_LIFE_MASK = 0x3F
DRIP_GUN_MASK = 0x3F      # slot 8 b0-5
DRIP_SENT_FIELD = 6       # slot 8 b6-11
BELT_GAP_FIELD = 18       # slot 5 b18-23 -- the uncovered-belt-tile gap.  v600
BELT_GAP_MASK = 0x3F      # PUBLISHED this and never read it; PLANK 2 reads it.
# --- v608: slot 15, THE COREFIRE WORD (writer: CORE, `_corefire_report`) ----
# b0-10 last round our core LOST HP, +1 (0 = never) · b11-20 pack_tile of the
# identified shooter (0 = unknown) · b21-27 our core HP // 4 (500//4 = 125 fits
# in 7 bits) · b28 the shooter is a SENTINEL.
CF_HIT_MASK = 0x7FF
CF_TILE_FIELD = 11
CF_TILE_MASK = 0x3FF
CF_HP_FIELD = 21
CF_HP_MASK = 0x7F
CF_HP_UNIT = 4
CF_SENT_BIT = 1 << 28
CF_RAY_BIT = 1 << 29      # the shooter was identified by its FACING RAY,
                          # not by the reach-only fallback rung

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
        # ⛔ v602 FIX 5(a): EVERY ROLE SENSES TERRAIN NOW.  v601 called
        # `_ore_scan` from the HOME KEEPER and the ORE DENIER only, and it is
        # the one thing that fills `map_walls` on an unconfirmed map -- so the
        # CAGE WALKER and the SIEGE ENGINEER, the two roles that cross the whole
        # board, had an EMPTY wall set and the new flood would have paved
        # straight through the terrain it is here to respect.  The scan is
        # bounded by map area per unit (`ore_scanned`), not by rounds.
        if SK_SENSE_NAV or self.role in (SK_HOME_KEEPER, SK_ORE_DENIER):
            self._ore_scan(ct, p)
        # Liveness: ONE WRITER PER SLOT -- this body owns SK_SLOT_BEAT[role]
        # and nothing else writes it.  Absolute round+1, never modular.
        self.beat(ct, SK_SLOT_BEAT[self.role], rnd)
        self._sense(ct, rnd)
        self._corefire_tick(ct, rnd)                # v608: PLANK 3's clock
        # ⭐ v619 PLANK 5 (SK_RENT) -- AND ITS PLACEMENT IS AN ENGINE FACT, NOT
        # A PREFERENCE.  `destroy` on an adjacent allied building costs no
        # action cooldown, no move and no turn (probed this wave), so the sweep
        # is not competing with anything below it and every later cost getter in
        # this same turn reads the refunded scale.  It is the one verb in this
        # tree that can run above the whole turn without taking anything from
        # it.  Roles other than the two plan owners return 0 on the first line.
        self._rent_sweep(ct, p, rnd)

        # --- ledger V5: DENIAL yields to survival when the core is hit -----
        # ⛔ THE DENIAL ROLE ONLY.  The first cut had the cage walker yield too
        # and a local game showed it: the under-attack latch went fresh early
        # and the walker spent the whole match at home, sealing zero ring
        # tiles.  V5 is about branches that spend builder-turns on DENIAL; the
        # walker is the KILL branch, and "not at the kill's expense" cuts the
        # other way for it.
        # ⭐ v606 ITEM 4(b), HALF 1 -- THE DETECTOR RUNS FOR EVERY ROLE.
        # `period_cycle()` had exactly one caller (`_cycle_commit`) which had
        # exactly one caller (`_cage_walker`), so three of the four roles could
        # orbit forever with the detector reading the cycle correctly and no
        # window ever opening.  Measured, fimbulwinter seat A bot 8 (ORE_DENIER):
        # 188 rounds of a period-6 orbit, `period_cycle()` = 6 on 151 of them,
        # `commit_until` = -1 on all 188.  Hoisted ABOVE the V5 survival branch
        # because that branch is one of the two authorities being arbitrated.
        if SK_CYCLE_ALL_ROLES and self.role != SK_CAGE_WALKER:
            self._cycle_commit(rnd)

        # ⭐ v608 PLANKS 2 and 1, THE DENIER'S HOME ANSWER, PLACED ABOVE LEDGER
        # V5 AND NOT INSIDE IT.  V5 answers "something is on our ring"; this
        # answers "something is KILLING OUR CORE", which the anatomy says is a
        # different object 19 times in 19 (V5's slot-2 threat is the NEAREST
        # enemy building, and v603 FIX 4 already had to teach it to ignore
        # barriers).  Keeping them separate is what makes both ablatable: with
        # SK_COREFIRE off this branch cannot fire and V5 is untouched.
        # ⛔ AND IT DOES NOT WIDEN V5'S TRIGGER: the under-attack latch needs the
        # CORE to see the threat, and the shooter can sit outside the core's
        # r^2=36 vision.  The corefire alarm is the core's own HP, which cannot
        # be out of vision.
        if (SK_COREFIRE and self.role == SK_ORE_DENIER
                and self._denier_home_answer(ct, p, rnd)):
            return

        if self._under_attack(ct, rnd) and self.role == SK_ORE_DENIER:
            # ⭐ v606 ITEM 4(b), HALF 2 -- THE CONSUMER, and without it half 1 is
            # a NO-OP: a window nobody reads changes nothing.  Inside an open
            # window the denier keeps walking at the target the orbit was
            # undoing, and the V5 branch does not get to re-pick.
            if (SK_CYCLE_ALL_ROLES and SK_CYCLE_K and self.commit_until > rnd
                    and self.commit_tgt is not None
                    and self.step_to(ct, self.commit_tgt)):
                return
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

    def _s2_pending(self, ct, rnd):
        """v607 ITEM 2 (SK_S2_PRIORITY) -- True inside the S1->S2 funding window.

        Read entirely off SK_SLOT_NEST, which the SIEGE ENGINEER already
        publishes and which -- until now -- NO consumer read (`_nest_publish`
        says so in those words).  Nothing new is written, so the one-writer-per-
        slot rule is untouched and the window costs one `read_store`.
          word == 0                -> no first gun yet.  NOT the window: the
                                      measured wait class is S1->S2 (15 of 30
                                      games) and pre-S1 is 1 of 30.
          word & NEST_SITE2_BIT    -> the pair stands.  Window shut.
          b10-20                   -> the FIRST gun's plant round + 1, which is
                                      what SK_S2_PRIORITY_MAX is measured from.
        ⛔ AND THE ENGINEER MUST BE ALIVE.  Deferring a purchase for a body that
        is dead defers it for nothing; the beat slot is the liveness fact the
        role assignment already runs on.
        ⚠ DISCLOSED: if the SECOND gun dies later, b21 stays set and the window
        does not reopen for the rebuild.  That is deliberate -- the wait this
        arm is aimed at is the FIRST pair's, and a reopening window would defer
        home defence in the late game, which is the half of the programme that
        is admissible only when it does not slow the kill.
        """
        if not SK_S2_PRIORITY:
            return False
        try:
            word = ct.read_store(SK_SLOT_NEST)
        except Exception:
            return False
        if not word or (word & NEST_SITE2_BIT):
            return False
        born = ((word >> NEST_RND_FIELD) & SK_BEAT_MASK) - 1
        if born < 0 or rnd - born > SK_S2_PRIORITY_MAX:
            return False
        return self.beat_fresh(ct, SK_SLOT_BEAT[SK_SIEGE_ENGINEER], rnd,
                               SK_BEAT_STALE)

    # --- v613 PLANK 5's GATE: does the PAIR stand right now? ------------

    def _two_tubes(self, ct):
        """True while BOTH forward tubes stand.

        ⭐⭐ v617 ITEM 1 -- THE PRODUCER FIX.  Under SK_TEAM_TUBES this reads the
        TWO FORWARD-SENTINEL BEATS (slot 7 b0-9 / b22-31) that the tubes write
        for themselves, and is a TEAM fact.  With the flag off it reads b21, the
        v613 form, which is a PER-BODY LEDGER: `_nest_publish` sets b21 only
        while ONE BODY holds both `nest_turret` and `nest_turret2`, and the
        v616 probe measured that at 8.4% of core-rounds against a replay ground
        truth of 35.5% (5 of 51 publishes).  See the SK_TEAM_TUBES note in
        sk_maps.py for the two mechanisms -- engineer turnover and, the larger
        one, `get_hp(id)` raising out of vision so a walked-away-from tube is
        booked DEAD.

        Costs one `read_store` and writes nothing on either branch.
        """
        if not SK_NEST_PAIR:
            return False
        try:
            word = ct.read_store(SK_SLOT_NEST)
        except Exception:
            return False
        if not SK_TEAM_TUBES:
            return bool(word) and bool(word & NEST_SITE2_BIT)
        return self._tube_count(word, ct.get_current_round()) >= 2

    def _tube_count(self, word, rnd):
        """How many forward-tube SEATS beat recently.  0, 1 or 2.

        ⛔ PURE FUNCTION OF (word, rnd) ON PURPOSE: it is the one piece of the
        producer fix a static battery can drive BOTH WAYS without a game --
        feed it a word with neither / one / both seats fresh and a word whose
        beats are older than SK_TUBE_STALE, and every branch is reachable from
        a unit test.
        """
        n = 0
        for field in SK_TUBE_SEAT_FIELDS:
            b = (word >> field) & SK_TUBE_BEAT_MASK
            if b and rnd - (b - 1) <= SK_TUBE_STALE:
                n += 1
        return n

    # --- v620 PLANK 1 -- SK_TUBE_FLOOR2: the STANDING-tube count -----------

    def _floor_live(self, ct, rnd):
        """⭐⭐ v620 PLANK 1 -- HOW MANY FORWARD TUBES ACTUALLY STAND.

        THE WHOLE PLANK IS THE SUBJECT OF THIS NUMBER.  v619 instrumented the
        engineer's plant ledger at every purchase: `live = 0` on 60 of 69 buys
        and `live = 2` on ZERO, against a wire that shows two forward sentinels
        standing simultaneously in 38.2% of rounds.  The ledger is not a census
        of our tubes, it is a census of the tubes THIS BODY CAN CURRENTLY SEE --
        because `get_hp(id)` raises out of vision and v618 books that as a
        death.  v617 already built the honest producer (each tube writes its own
        phase-separated beat into slot 7); this reads it.

        ⛔ THE GRACE IS A CORRECTNESS REQUIREMENT AND IT IS APPLIED IN EXACTLY
        ONE DIRECTION.  A tube planted at round r cannot beat before r+1, writes
        only on its residue (up to 2 more rounds) and slot writes are buffered
        one more -- 4 rounds of legitimate invisibility.  Inside
        SK_TUBE_FLOOR2_GRACE of our newest plant the answer is
        `max(team, own ledger)`, so the count may only be too HIGH; outside it,
        the team beats stand alone.  Too high delays a replant by at most GRACE
        rounds.  Too low buys a tube we already own -- which is the loop this
        plank exists to close, so that is the failure it refuses.

        ⛔ AND IT FALLS BACK TO v619 ON ANY DOUBT.  With the flag off, the
        producer off, the pair off or the store unreadable, this returns
        `_nest_live()` -- the ledger -- so every caller reduces to v619's code
        on v619's inputs and the flag-off tape is an identity by construction
        rather than by argument.
        """
        if not (SK_TUBE_FLOOR2 and SK_TEAM_TUBES and SK_NEST_PAIR):
            return self._nest_live()
        try:
            team = self._tube_count(ct.read_store(SK_SLOT_NEST), rnd)
        except Exception:
            return self._nest_live()
        newest = None
        for t in self._nest_slots():
            if t is not None and (newest is None or t[2] > newest):
                newest = t[2]
        if newest is not None and 0 <= rnd - newest <= SK_TUBE_FLOOR2_GRACE:
            led = self._nest_live()
            if led > team:
                return led
        return team

    def _medic_armed(self, ct):
        """⭐ v613 PLANK 5 -- SK_CORE_MEDIC_RIDER.  The v608 medic, re-armed
        CONDITIONALLY.

        The anatomy prices the unconditional form honestly and it is why
        `SK_CORE_MEDIC` ships False: in 14 of 19 losses THEIR core is at 500/500
        when ours dies, so rounds bought for our core have no consumer -- the
        heal is a losing race ALONE.  With the tube floor standing they DO have
        a consumer: two tubes are 18 HP/round against their heal seats, and
        `dealt - healed` = 500-512 in 7 of 7 wins.  So the medic is armed by the
        PAIR, and by nothing else.
        """
        if SK_CORE_MEDIC:
            return True
        if not SK_CORE_MEDIC_RIDER:
            return False
        return self._two_tubes(ct)

    # ==================================================================
    # v608 -- THE HOME ANSWER: readers, then the three planks
    # ==================================================================
    # The alarm is written by the CORE (`sk_core._corefire_report`, one writer,
    # slot 15).  Everything below CONSUMES it.  Read the flag comments in
    # sk_maps.py for why rung 1 of the commissioned ladder (a body in the ray)
    # is not here: a sentinel's shot passes through entities and does not touch
    # them, so there is nothing to absorb.

    def corefire_word(self, ct):
        if not SK_COREFIRE:
            return 0
        try:
            return ct.read_store(SK_SLOT_COREFIRE)
        except Exception:
            return 0

    def corefire_fresh(self, ct, rnd):
        """True while our core has lost HP inside the last SK_COREFIRE_TTL."""
        hit = self.corefire_word(ct) & CF_HIT_MASK
        if not hit:
            return False
        age = rnd - (hit - 1)
        return 0 <= age <= SK_COREFIRE_TTL

    def corefire_hp(self, ct):
        """Our core's HP as the CORE last published it (quantised by 4)."""
        return ((self.corefire_word(ct) >> CF_HP_FIELD) & CF_HP_MASK) * CF_HP_UNIT

    def corefire_shooter(self, ct):
        w = self.corefire_word(ct)
        t = (w >> CF_TILE_FIELD) & CF_TILE_MASK
        if not t:
            return None
        if SK_COUNTER_RAY_ONLY and not (w & CF_RAY_BIT):
            return None
        q = unpack_tile(t)
        if q is None or not self.ibp(q):
            return None
        return q

    def _corefire_tick(self, ct, rnd):
        """How long this body has watched an unbroken alarm.  PLANK 3's gate.

        Per BODY, not published: 11 bits are not free on a full store and the
        home keeper dies in 2 of 30 games, so a replacement restarting the count
        costs one deferred purchase in a rare case rather than a slot.
        """
        if SK_COREFIRE and self.corefire_fresh(ct, rnd):
            self.corefire_streak += 1
        else:
            self.corefire_streak = 0

    def _core_ray_shooter(self):
        """THIS BODY's own answer when the core could not identify the shooter.

        Same durable-fact argument as `armed_memo` itself (v601 PLANK 1): a
        turret is a BUILDING, it cannot move, so the tile outlives the entity
        leaving vision.  `armed_facing` is the tile-keyed facing (v602 FIX 2).
        Ranks exactly as the core's own scan does, including the disclosed third
        rung -- a sentinel whose REACH covers a core tile with no readable
        facing, which is the 19/19 prior standing in for a fact we could not
        read.
        """
        if self.core is None:
            return None
        foot = core_tiles_xy(self.core)
        best = None
        for xy, v in self.armed_memo.items():
            et = v[0]
            if et not in TURRET_TYPES:
                continue
            sent = et != EntityType.GUNNER
            reach = SK_KILLER_SENT_REACH if sent else SK_KILLER_GUNNER_REACH
            f = self.armed_facing.get(xy)
            rank = None
            if f is not None and (f[0] or f[1]):
                dx, dy = f
                k = 1
                while k * k * (dx * dx + dy * dy) <= reach:
                    if (xy[0] + dx * k, xy[1] + dy * k) in foot:
                        rank = 0 if sent else 1
                        break
                    k += 1
            if rank is None and sent and not SK_COUNTER_RAY_ONLY:
                for (cx, cy) in foot:
                    ax, ay = cx - xy[0], cy - xy[1]
                    if ax * ax + ay * ay <= reach:
                        rank = 2
                        break
            if rank is None:
                continue
            q = Position(xy[0], xy[1])
            d = dsq_core(q, self.core)
            if best is None or (rank, d) < (best[0], best[1]):
                best = (rank, d, q)
        return None if best is None else best[2]

    def _counter_target(self, ct, rnd):
        """The tile of the thing shooting our core: published first, then this
        body's own memo.  Fenced to SK_COUNTER_PECK_DSQ of our core.
        """
        if not SK_COREFIRE or self.core is None:
            return None
        q = self.corefire_shooter(ct)
        if q is None:
            q = self._core_ray_shooter()
        if q is None:
            return None
        if dsq_core(q, self.core) > SK_COUNTER_PECK_DSQ:
            return None
        # ⭐ v609 GATE D -- a remembered tile whose building is GONE is not a
        # shooter.  ⛔ BOUNDS FIRST, THEN VISION: `is_in_vision` is a pure radius
        # test with no bounds check (CLAUDE.md, corrected s50), so `ibp` has to
        # be the outer guard or the next `get_tile_*` raises off-map.
        if SK_COUNTER_LIVE_TGT:
            try:
                if self.ibp(q) and ct.is_in_vision(q):
                    bid = ct.get_tile_building_id(q)
                    if bid is None or ct.get_team(bid) == self.team:
                        self.armed_memo.pop((q.x, q.y), None)
                        self.armed_facing.pop((q.x, q.y), None)
                        return None
            except Exception:
                pass
        return q

    # --- PLANK 1: SK_CORE_MEDIC ----------------------------------------

    def _core_medic(self, ct, p, rnd):
        """Heal OUR CORE from an orthogonally adjacent tile.  1 Ti -> +4 HP.

        ⛔ THE HEAL VERB ALREADY EXISTED (`_heal_action`) AND WOULD ALREADY HAVE
        PICKED THE CORE -- it takes the most-damaged adjacent friendly building
        and the core has 500 max HP.  It never ran because it is ordered below
        the door, the peck, the harvester and the belt, and because the keeper is
        never standing beside the core when the shooting starts.  So this method
        is ORDERING and `_medic_seat` is POSITIONING; neither is a new call.

        The exchange, from the anatomy: one sentinel is 18 damage on reload 2 =
        9 HP/round, so one medic (+4) turns the measured 54-round window into
        ~100 and two (+8) into ~500.  It is a losing race ALONE and it is not
        meant to be won alone -- it is the rung that buys the r160 kill
        machinery, and PLANK 3, the time to land.
        """
        if not self._medic_armed(ct) or self.core is None:
            return False
        if not self.corefire_fresh(ct, rnd):
            return False
        if (self.role == SK_ORE_DENIER
                and self.corefire_hp(ct) > SK_MEDIC_HELP_HP):
            return False            # the second medic is bought late, on HP
        if ct.get_global_resources() <= SK_MEDIC_TI_FLOOR:
            return False            # V10's floor: never starve the drip
        foot = core_tiles_xy(self.core)
        for d in CARDINALS:
            q = p.add(d)
            if not self.ibp(q) or (q.x, q.y) not in foot:
                continue
            try:
                bid = ct.get_tile_building_id(q)
                if bid is None or ct.get_team(bid) != self.team:
                    continue
                if ct.get_max_hp(bid) - ct.get_hp(bid) < 4:
                    return False    # a heal that overflows is 1 Ti for nothing
                if not ct.can_heal(q):
                    continue
                ct.heal(q)
            except Exception:
                continue
            self.core_heals += 1
            return True
        return False

    def _medic_seat(self, ct, p, rnd):
        """The core-ring tile this body should stand on to heal, or None.

        Returns `p` itself when this body is already orthogonally adjacent to
        the footprint, which is how the caller learns to HOLD STATION rather
        than wander back to the belt while the core is being shot.
        """
        if not self._medic_armed(ct) or self.core is None:
            return None
        if not self.corefire_fresh(ct, rnd):
            return None
        if (self.role == SK_ORE_DENIER
                and self.corefire_hp(ct) > SK_MEDIC_HELP_HP):
            return None
        if adjacent_to_core(p, self.core):
            return p
        best = None
        for q in core_ring(self.core):
            if not self.ibp(q):
                continue
            d = p.distance_squared(q)
            if d > SK_MEDIC_SEAT_DSQ:
                continue
            try:
                if not ct.is_tile_passable(q):
                    continue
                if ct.get_tile_builder_bot_id(q) is not None:
                    continue        # one medic per seat; the other takes another
            except Exception:
                continue
            if best is None or d < best[0]:
                best = (d, q)
        return None if best is None else best[1]

    def _medic_turn(self, ct, p, rnd):
        """Heal if seated, else walk to a seat.  True iff it took the turn."""
        if ct.get_action_cooldown() == 0 and self._core_medic(ct, p, rnd):
            return True
        seat = self._medic_seat(ct, p, rnd)
        if seat is None:
            return False
        if seat.x == p.x and seat.y == p.y:
            # Seated but nothing to heal (core full, or bank at the floor).
            # Fall through rather than idle -- the seat is held by the movement
            # layer, not by burning the turn.
            return False
        return bool(self.step_to(ct, seat))

    # --- v609 GATE A: the near emergency outranks the far one -----------

    def _home_threat_outranks(self, ct, rnd):
        """True while a live enemy BODY sits on our own home ring.

        ⛔ THE MEASURED MECHANISM, not an intuition.  The v609 diagnosis
        attributes v608's M1 seat-A belt fall (42.1 -> 28.9 directed
        connectivity) to exactly two games, and in BOTH the new belt death is
        an ENEMY BUILDER pecking a conveyor at d^2 1 of our core -- the killer
        standing at d^2 4 -- in rounds when the ORE DENIER was away marching at
        a gun.  v608 put the counter-peck ABOVE ledger V5 unconditionally, so
        the far threat always won the arbitration.  This restores the ordering
        only while the near one is real.

        A BARRIER is excluded on v603 FIX 4's own argument: it does not shoot
        and does not chew, so answering it is the losing arithmetic that fix
        already removed from V5's answer.
        """
        if self.core is None or not self._under_attack(ct, rnd):
            return False
        try:
            threat = unpack_pos(ct.read_store(SK_SLOT_THREAT_POS))
        except Exception:
            return False
        if threat is None or not self.ibp(threat):
            return False
        if dsq_core(threat, self.core) > SK_COUNTER_YIELD_DSQ:
            return False
        try:
            tb = ct.get_tile_building_id(threat)
            if (tb is not None
                    and ct.get_entity_type(tb) == EntityType.BARRIER):
                return False
        except Exception:
            pass
        return True

    # --- PLANK 2: SK_COUNTER_PECK --------------------------------------

    # --- v613 PLANK 3 / PLANK 4 helpers ---------------------------------

    def _friendly_adjacent(self, ct, q):
        """How many of OUR builder bots stand orthogonally adjacent to q.

        PLANK 3's whole arithmetic rests on this number: one body is 2 dmg a
        round against a healer's +4 and loses; two are 4 and hold; the measured
        heal rate on their apron shooters (450 HP across 48 shooters' entire
        lifetimes, tapemj) is far below one continuous healer, so 2 is the bar.
        Four `get_tile_builder_bot_id` reads, and only on the winner.
        """
        n = 0
        for d in CARDINALS:
            r = q.add(d)
            if not self.ibp(r):
                continue
            try:
                uid = ct.get_tile_builder_bot_id(r)
                if uid is not None and ct.get_team(uid) == self.team:
                    n += 1
            except Exception:
                continue
        return n

    def _live_launchers(self, ct, rnd):
        """Enemy LAUNCHER tiles believed live, from `armed_memo`.

        A launcher is a BUILDING and cannot move, so the TILE is the durable
        fact (the same argument `armed_memo` is tile-keyed on).  It CAN die,
        though, and a permanently-feared ghost seat is a permanent detour --
        hence SK_PLUCK_MEMO_TTL, plus an in-vision liveness check that deletes
        the memo outright when the tile is visibly empty or visibly ours.
        """
        out = []
        if not SK_PLUCK_AWARE:
            return out
        dead = None
        for xy, v in self.armed_memo.items():
            if v[0] != EntityType.LAUNCHER:
                continue
            if rnd - v[1] > SK_PLUCK_MEMO_TTL:
                continue
            q = Position(xy[0], xy[1])
            if not self.ibp(q):
                continue
            try:
                if ct.is_in_vision(q):
                    bid = ct.get_tile_building_id(q)
                    if bid is None or ct.get_team(bid) == self.team:
                        if dead is None:
                            dead = []
                        dead.append(xy)
                        continue
            except Exception:
                pass
            out.append(xy)
        if dead:
            for xy in dead:
                self.armed_memo.pop(xy, None)
                self.armed_facing.pop(xy, None)
        return out

    def _pluck_dsq(self, q, launchers):
        """min d^2 from q to any live enemy launcher (a big number if none)."""
        best = 9999
        for (lx, ly) in launchers:
            dx = q.x - lx
            dy = q.y - ly
            d = dx * dx + dy * dy
            if d < best:
                best = d
        return best

    def _pluck_retarget(self, ct, rnd, tgt, launchers):
        """⭐ PLANK 4's second half -- peck the LAUNCHER, not the seat.

        When EVERY orthogonal seat of the shooter sits inside a live launcher's
        pickup disc (engine bound: d^2 <= 2 from the launcher), the seat cannot
        be held: on `midgard_B` the same body is thrown off the same seat at
        r15, 21, 27, 33, 39, 45, 51 and 57 -- every six rounds until we die at
        r61.  The launcher itself is a 30 HP BUILDING with no defence of its
        own: 15 pecks, and its removal frees every seat it covers.
        """
        if not (SK_PLUCK_AWARE and SK_PLUCK_RETARGET) or not launchers:
            return None
        seats = 0
        plucked = 0
        for d in CARDINALS:
            r = tgt.add(d)
            if not self.ibp(r):
                continue
            seats += 1
            if self._pluck_dsq(r, launchers) <= SK_PLUCK_DSQ:
                plucked += 1
        if seats == 0 or plucked < seats:
            return None
        # The nearest covering launcher, and never the target we are already on.
        best = None
        for (lx, ly) in launchers:
            q = Position(lx, ly)
            if q.x == tgt.x and q.y == tgt.y:
                continue
            d = q.distance_squared(tgt)
            if best is None or d < best[0]:
                best = (d, q)
        return None if best is None else best[1]

    def _pluck_seat(self, ct, p, tgt, launchers):
        """PLANK 4's first half -- the orthogonal seat of `tgt` FARTHEST from
        any live enemy launcher, nearest-to-us as the tie-break.  None when the
        ranking has nothing to say (no launchers, or no legal seat).
        """
        if not SK_PLUCK_AWARE or not launchers:
            return None
        best = None
        for d in CARDINALS:
            r = tgt.add(d)
            if not self.ibp(r):
                continue
            if r.x == p.x and r.y == p.y:
                return None                 # already seated
            try:
                if not ct.is_tile_passable(r):
                    continue
            except Exception:
                continue
            score = (-self._pluck_dsq(r, launchers), p.distance_squared(r))
            if best is None or score < best[0]:
                best = (score, r)
        return None if best is None else best[1]

    def _counter_march(self, ct, p, rnd, tgt):
        """March at the gun and peck it.  40 HP / 2 damage = 20 builder-turns.

        ⭐ v613 PLANK 3 -- THE LEDGER-V7 RELAX, AND IT IS NARROW BY
        CONSTRUCTION.  `hp_trend_ok` is right in general (38 rounds and 152 Ti
        spent on a target healed +8 against 7) and it is exactly wrong on a
        POINT-BLANK shooter with two of our bodies on it: 1,053 HP was delivered
        into 48 shooter turrets on the tapemj tape and killed 12, because the
        damage was SPREAD and the veto retired targets one at a time.  Two
        adjacent bodies are 4 dmg/round against a measured heal of 450 HP over
        48 shooters' whole lifetimes.  ⛔ THE VETO IS NOT CALLED AT ALL IN THE
        RELAXED CASE -- it MUTATES the HP memo and latches a give-up, so calling
        it and ignoring the answer would still retire the target for every other
        verb.
        ⛔ AND THE COMMENT LIVES HERE, NOT AT THE READ SITE, FOR A MEASURED
        REASON: the v612 battery's S14 ordering assertion is a 900-CHARACTER
        DISTANCE REGEX between the team check and the fire call -- the exact
        "distance proxy" fragility that file's own comment warns about -- and an
        eleven-line comment at the relax site pushed the fire out of range and
        made a correct tree read FAIL.  v613's own S21 re-tests the same
        ordering BY POSITION.

        ⛔ WHY THIS IS NOT LEDGER V5.  V5 (`_home_defence`) marches the denier at
        SK_SLOT_THREAT_POS, the NEAREST enemy building within d^2 39 of our core
        -- in practice their collar barrier or their builder, and v603 FIX 4 had
        to add a guard to stop it chewing barriers.  It is essentially never the
        sentinel five tiles out that the anatomy says kills us 19 times in 19.
        This verb sits ABOVE V5 and re-points the same body at the CORE-DAMAGER;
        V5 is left exactly as it was, so the two are separately ablatable.
        """
        if not SK_COUNTER_PECK:
            return False
        # ⭐ v613 PLANK 4.  Resolved BEFORE the adjacency test so the retarget
        # changes the whole march -- the walk, the fire and the V7 bookkeeping --
        # rather than only the last step.
        launchers = self._live_launchers(ct, rnd) if SK_PLUCK_AWARE else []
        if launchers:
            alt = self._pluck_retarget(ct, rnd, tgt, launchers)
            if alt is not None:
                if (alt.x, alt.y) != self.pluck_last:
                    self.pluck_last = (alt.x, alt.y)
                    self.pluck_retargets += 1
                tgt = alt
        adj = abs(tgt.x - p.x) + abs(tgt.y - p.y) == 1
        if adj and ct.get_action_cooldown() == 0 and ct.get_global_resources() >= 2:
            tid = None
            try:
                tid = ct.get_tile_building_id(tgt)
            except Exception:
                tid = None
            if tid is None:
                return False        # the gun is gone; nothing to march at
            # ⭐⭐ v612 FIX 1 -- THE LATCHED TILE HAS NO TEAM CHECK.  Pre-existing
            # since v608 and located by the v611 driven probe (build report §5):
            # 23 pecks landed on OUR OWN conveyor/harvester across that tape
            # (bifrost B r100-111 into our conveyor at (24,3), skald A r86-92
            # into our harvester at (7,5), yggdrasil B r81-82 at (26,24)).  The
            # target is a TILE, remembered from when an enemy turret stood on
            # it; when that turret dies and our own relay is later laid on the
            # same tile, the keeper marches up and chews it.  `can_fire` is
            # team-blind, so nothing downstream stops this.
            # ⛔ THE OWNER IS RE-READ AT FIRE TIME, NOT AT LATCH TIME, because
            # the tile can change hands between the two -- that is the whole
            # defect.  An UNREADABLE owner refuses the shot as well: one turn
            # is cheaper than a conveyor, and the fail-open form is exactly
            # what produced the 23.
            if SK_MARCH_TEAMCHECK:
                own = None
                try:
                    own = ct.get_team(tid)
                except Exception:
                    own = None
                if own is None or own == self.team:
                    # The latch is cleared as well as the shot refused: leaving
                    # it set makes the body march at a tile it will never fire
                    # at, which is the v609 GATE D ping-pong in a new costume.
                    self.armed_memo.pop((tgt.x, tgt.y), None)
                    self.armed_facing.pop((tgt.x, tgt.y), None)
                    self.march_ownskip += 1
                    return False
            # ⭐ v613 PLANK 3 -- THE V7 RELAX (rationale in the docstring).
            relax = (SK_PECK_FOCUS and self.core is not None
                     and dsq_core(tgt, self.core) <= SK_PECK_FOCUS_DSQ
                     and self._friendly_adjacent(ct, tgt)
                     >= SK_PECK_FOCUS_BODIES)
            if relax:
                self.peck_relaxed += 1
            elif not self.hp_trend_ok(ct, tid, rnd):
                return False        # ledger V7: it is being healed faster
            try:
                if ct.can_fire(tgt):
                    ct.fire(tgt)
                    self.counter_pecks += 1
                    return True
            except Exception:
                return False
            return False
        if adj:
            return False
        # ⭐ v613 PLANK 4, THE SEAT RANKING.  The walk target becomes the
        # orthogonal seat of the shooter FARTHEST from any live enemy launcher
        # instead of the shooter tile itself.  It is only ever a choice among
        # tiles the body was going to end up on anyway (all four are adjacent to
        # the same target), so it cannot lengthen the march by more than the
        # geometry of the seat it picks.
        walk = tgt
        if launchers:
            seat = self._pluck_seat(ct, p, tgt, launchers)
            if seat is not None and (seat.x, seat.y) != (tgt.x, tgt.y):
                walk = seat
                self.pluck_detours += 1
        # ⭐ v609 GATE E -- soft bodies, SCOPED.  The flag is set only around
        # this one `step_to` and cleared immediately, so no other role's
        # navigation changes.  `nav_held` means "the routed tile is plugged by a
        # 1-round obstacle and we are standing our ground"; it must count as
        # taking the turn, or the lower authority drags the body away and the
        # hold is indistinguishable from the plank declining.
        if not SK_COUNTER_SOFT_BODIES:
            return bool(self.step_to(ct, walk))
        # ⛔ NO `try/finally` HERE -- THE PLATFORM SANDBOX REJECTS `finally`
        # BLOCKS OUTRIGHT (`ValueError: <bot>/sk_roles.py: 'finally' blocks are
        # not allowed`, caught by the local validator on the first arm run).
        # The plain form is equivalent for our purposes: `step_to` swallows its
        # own engine errors, and anything that did escape it would destroy this
        # unit for the rest of the match, so there is no later turn for a stale
        # flag to corrupt.  Belt and braces, the flag is also cleared on entry
        # to `_denier_home_answer`.
        self.nav_soft_bodies = True
        self.nav_held = False
        moved = bool(self.step_to(ct, walk)) or self.nav_held
        self.nav_soft_bodies = False
        return moved

    def _keeper_counter(self, ct, p, rnd):
        """⭐ v613 PLANK 3, THE CONCENTRATION HALF -- THE HOME KEEPER JOINS.

        Without this, exactly ONE body (the ORE DENIER) ever marches at the
        shooter, so "two of our bodies adjacent" is unreachable and the V7 relax
        can never fire: the two halves are one plank and neither is testable
        alone.  Fenced hard, and every fence is one the denier already pays:
          * the shooter must be POINT-BLANK (d^2 <= SK_PECK_FOCUS_DSQ of our own
            core).  28 of 48 of theirs are, at d^2 <= 5;
          * the corefire alarm must be FRESH and the v609 HP ceiling must hold,
            so the keeper is never pulled off the belt by a stale alarm.
        Returns True when it took the turn -- INCLUDING when it is already
        seated and cannot act, because a keeper that returns False here is
        walked back to the belt by `_home_keeper_move` and the seat is lost,
        which is indistinguishable from the plank declining.
        """
        if not (SK_PECK_FOCUS and SK_PECK_FOCUS_KEEPER
                and SK_COREFIRE and SK_COUNTER_PECK):
            return False
        if self.core is None or not self.corefire_fresh(ct, rnd):
            return False
        # ⛔ v609 GATE B, BORROWED -- and it is written with this comment
        # ATTACHED so the line is not TEXTUALLY IDENTICAL to the one inside
        # `_denier_home_answer`.  The v610 battery's GATE B dirty control is a
        # string substitution on that exact two-line block, and a second copy
        # of it in this file makes the mutation land in the wrong method and
        # the scan pass a tree that breaks it (observed on the first v613
        # build: S11 reported BROKEN).
        if SK_COUNTER_HP_MAX and self.corefire_hp(ct) > SK_COUNTER_HP_MAX:  # v609 GATE B
            return False
        tgt = self._counter_target(ct, rnd)
        if tgt is None or dsq_core(tgt, self.core) > SK_PECK_FOCUS_DSQ:
            return False
        if self._counter_march(ct, p, rnd, tgt):
            self.keeper_marches += 1
            return True
        if abs(tgt.x - p.x) + abs(tgt.y - p.y) == 1:
            self.keeper_holds += 1
            return True                     # seated: hold the seat, do not walk
        return False

    def _denier_home_answer(self, ct, p, rnd):
        """The ORE DENIER's v608 turn: kill the gun, else be the second medic.

        Ordered kill-first on purpose: a dead gun ends the episode PERMANENTLY,
        a heal only buys rounds.  The medic half is gated on core HP
        (SK_MEDIC_HELP_HP) because the denial verb is argued as OPENS THE LANE
        and must not be sold for a heal we do not yet need.
        """
        self.nav_soft_bodies = False      # v609 GATE E: never enter stale
        if not SK_COREFIRE or self.core is None:
            return False
        if not self.corefire_fresh(ct, rnd):
            return False
        # ⭐ v609 GATE B -- the HP ceiling.  0 is OFF and is v608's behaviour.
        if SK_COUNTER_HP_MAX and self.corefire_hp(ct) > SK_COUNTER_HP_MAX:
            return False
        # ⭐ v609 GATE A -- the NEAR emergency outranks the FAR one.  Returning
        # False here does not idle the body: the very next branch in
        # `_role_turn` is ledger V5, which marches it at the home threat.
        if SK_COUNTER_YIELD_HOME and self._home_threat_outranks(ct, rnd):
            return False
        tgt = self._counter_target(ct, rnd) if SK_COUNTER_PECK else None
        if tgt is not None and self._counter_march(ct, p, rnd, tgt):
            return True
        if self._medic_armed(ct) and self.corefire_hp(ct) <= SK_MEDIC_HELP_HP:
            return self._medic_turn(ct, p, rnd)
        return False

    # --- PLANK 3: SK_COUNTER_SENT --------------------------------------

    def _on_armed_axis(self, q):
        """`_on_enemy_axis` over the tile-keyed MEMO rather than this round's
        vision.  A sentinel cannot rotate, so a facing read once is true for its
        whole life -- and the gun we are answering is usually the one we can no
        longer see.
        """
        for xy, f in self.armed_facing.items():
            v = self.armed_memo.get(xy)
            if v is None or v[0] != EntityType.SENTINEL:
                continue
            dx, dy = f
            if dx == 0 and dy == 0:
                continue
            ax, ay = q.x - xy[0], q.y - xy[1]
            if dx == 0:
                if ax == 0 and (ay * dy) > 0:
                    return True
            elif dy == 0:
                if ay == 0 and (ax * dx) > 0:
                    return True
            elif ax * dy == ay * dx and (ax * dx) > 0:
                return True
        return False

    def _counter_sent_action(self, ct, p, rnd):
        """Plant ONE home SENTINEL, off their axis, bearing on the shooter.

        3 shots x 18 = 54 kills a 40 HP turret, and COPY 2's asymmetry is the
        whole point: a sentinel CANNOT ROTATE, so a gun sited off its firing
        line is fighting something that physically cannot answer.  Sentinel and
        not gunner because the shooter sits at the edge of r^2=32 by
        construction and a gunner reaches 13.

        ⛔ ITS OWN CAP, NOT THE DOOR BUDGET.  v606 refuted cutting door gunners
        and v607 refuted deferring them; this plank must not become a third way
        of selling the same load-bearing purchase.
        ⚠ NO PREP BARRIERS -- see SK_COUNTER_SENT_RESERVE's comment.
        """
        if not SK_COUNTER_SENT or self.core is None:
            return False
        if self.counter_sents >= SK_COUNTER_SENT_CAP:
            return False
        if self.corefire_streak < SK_COUNTER_RNDS:
            return False
        tgt = self._counter_target(ct, rnd)
        if tgt is None:
            return False
        cost = ct.get_sentinel_cost()
        if ct.get_global_resources() < cost + SK_COUNTER_SENT_RESERVE:
            return False
        best = None
        best_site = None
        best_face = None
        for d in CARDINALS:
            q = p.add(d)
            if not self.ibp(q) or not self.may_build(q, OWNER_DOOR):
                continue
            if self._on_enemy_axis(q) or self._on_armed_axis(q):
                continue                    # COPY 2: never in their line
            if self.free_neighbours(ct, p, exclude=q) < 2:
                continue                    # the self-trap guard, v601 PLANK 2
            if not self.path_arbiter_ok(ct, q, rnd):
                continue                    # v605 FIX 1: a turret is impassable
            for face in DIRECTIONS:
                if not self._ray_hits(q, face, tgt, reach=SK_KILLER_SENT_REACH):
                    continue
                score = (-q.distance_squared(tgt),)
                if best is None or score > best:
                    best = score
                    best_site = q
                    best_face = face
        if best_site is None:
            return False
        try:
            if not ct.can_build_sentinel(best_site, best_face):
                return False
            ct.build_sentinel(best_site, best_face)
        except Exception:
            return False
        self.counter_sents += 1
        return True

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
                xy = (ep.x, ep.y)
                if xy not in self.armed_memo:
                    self._armed_rev += 1        # v602 FIX 2: cache revision
                self.armed_memo[xy] = (et, rnd)
                # v602 FIX 2: the FACING, keyed on the tile as well, so the
                # danger term can price a RAY instead of a disc.  `enemy_facing`
                # already existed but is keyed on the ENTITY ID, which does not
                # survive the turret leaving vision -- the exact property
                # `armed_memo` was made tile-keyed to get.
                if et in TURRET_TYPES:
                    f = self.enemy_facing.get(eid)
                    if f is not None and self.armed_facing.get(xy) != f:
                        self.armed_facing[xy] = f
                        self._armed_rev += 1

    # ==================================================================
    # ROLE 0 -- HOME KEEPER  (harvesters, the global belt, heals, the door)
    # ==================================================================

    def _home_keeper(self, ct, p, rnd):
        # v602 FIX 5(a): the scan moved UP to `_builder`, where every role gets
        # it (it is the only writer of `map_walls` on an unconfirmed map).
        self._harv_watch(ct, p, rnd)                # v601 PLANK 1
        self._killer_report(ct, rnd)                # v601 PLANK 1 (slot 14)
        if SK_BELT:
            self._plan_belt(ct)
            self._belt_seed_store(ct, rnd)          # v604 FIX 4(c)
            self._belt_watch(ct, p)
            self._belt_report(ct, rnd)
        # ⭐ v613 PLANK 1, THE BELIEF HALF.  Bounded by this body's own vision
        # (a d^2 > 20 apron tile is skipped before any engine call), so the cost
        # is at most 32 cheap reads a round for the ONE body that stands at home.
        self._apron_watch(ct, p, rnd)
        # ⭐ v611 SK_HOME_LAUNCHER (OFF by default): the seat-occupancy density
        # that sites the launcher.  Runs ONLY while the launcher is unbuilt, so
        # it costs 8 tile reads a round for ~10-30 rounds of a 1000-round game
        # and exactly nothing after that.
        if (SK_HOME_LAUNCHER and not self.hl_gaveup
                and self.hl_built < SK_HOME_LAUNCHER_MAX):
            self._hl_seat_census(ct, rnd)
        if self._escape(ct, p, rnd):
            return
        # ⭐ v613 PLANK 3's KEEPER HALF, ABOVE the action block because the march
        # is a MOVE as often as it is a peck and `_counter_march` already
        # arbitrates the two internally (it checks the cooldown itself on the
        # fire path and falls to the walk otherwise).
        if self._keeper_counter(ct, p, rnd):
            return
        if ct.get_action_cooldown() == 0:
            # ⭐ v608 PLANK 3 then PLANK 1, ABOVE the door.  The counter-battery
            # goes first because it fires at most SK_COUNTER_SENT_CAP times in a
            # game and ENDS the episode, where a heal only buys rounds; the one
            # round of -4 HP it costs is inside the noise of a 9 HP/round stream.
            # Both sit above `_door_action` because the anatomy's channel is
            # 19/19 the gun shooting the CORE, not what is standing on the ring.
            if self._counter_sent_action(ct, p, rnd):
                return
            if self._core_medic(ct, p, rnd):
                return
            if SK_DOOR and self._door_action(ct, p, rnd):
                return
            # v601 PLANK 3: an enemy TURRET adjacent to the keeper outranks
            # everything below.  `_door_action`(a) only melees what stands on
            # our own ring; PLANK 1 marches this body at a located annulus
            # gunner, and without this it would arrive and then build a
            # conveyor next to it.
            if self._peck_priority(ct, p, rnd):
                return
            # ⭐ v618 PLANK 4.  ABOVE the generic heal, and that ordering is the
            # plank: `_heal_action` heals the most-damaged adjacent friendly
            # with NO race arithmetic, so a seat this plank refuses would be
            # healed by the rung below and the DOORWAVE guard would be
            # cosmetic.  Running first lets it publish its veto.
            if self._seat_heal_action(ct, p, rnd):
                return
            if self._heal_action(ct, p, rnd):
                return
            # ⭐ v610 PLANK 1.  Below the heal (a body about to die outranks a
            # tile) and below `_door_action`/`_peck_priority` (an enemy TURRET
            # on our ring outranks an enemy BARRIER on it), above everything
            # economic -- because a delivery seat an enemy holds is the tile
            # between a harvester and `titanium_collected`, and 180 of the 220
            # enemy barriers on the board at end of game stand on one.
            if self._seat_clear(ct, p, rnd):
                return
            # ⭐ v613 PLANK 1, THE ACTION HALF.  Above the economy and below
            # every verb that answers a body or a core about to die.  The
            # anatomy's r56 -> r58 sequence on `helheim_B` is the argument for
            # it being above the belt: the tile our conveyor died on became
            # their firing seat two rounds later, and re-laying it as a barrier
            # is the same 3 Ti the belt was going to spend anyway.
            if self._apron_action(ct, p, rnd):
                return
            # ⭐ v611 SK_HOME_LAUNCHER, OFF by default.  ONE turn, once a game.
            # It sits ABOVE the economy because the collar lands at median r11
            # and a launcher bought at r200 has missed the thing it answers;
            # it sits BELOW the heal, the door and the counter-peck because
            # every one of those is a body or a core about to die, and a
            # building that is one round late is still a building.
            if self._home_launcher_action(ct, p, rnd):
                return
            # ⭐ v610 PLANK 2, THE ACTION HALF.  While a chain is ONE tile from
            # delivering, that conveyor outranks a new harvester: a harvester
            # with no route home is worth exactly zero forever, and 30 of 68
            # alive harvesters on the v609 tape are one build from home.
            if (SK_TERMINATE and SK_TERM_FIRST and SK_BELT
                    and self._route_gaps(ct, rnd)
                    and self._belt_action(ct, p, rnd)):
                return
            if self._harvester_action(ct, p, rnd):
                return
            # ⭐ v618 PLANK 1, THE ACTION HALF.  JUST BELOW THE
            # HARVESTER-CRITICAL VERBS AND ABOVE THE GENERAL BELT, which is the
            # design's own placement: a harvester with no route home is worth
            # zero forever, but a seat is claimable only while it is still
            # EMPTY and their collar lands at median r11.  The tiles are belt
            # terminus segments with the belt's own facing, so this is not a
            # competing spend -- it is the same 3 Ti, earlier.
            if self._seat_claim_action(ct, p, rnd):
                return
            # ⭐ v618 PLANK 2, THE ACTION HALF.  Below the economy because ONE
            # round late is still a standing gun, and above nothing else: it is
            # a once-a-game purchase inside a bounded window.
            if self._home_gun_action(ct, p, rnd):
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
        # ⭐ v602 FIX 3, SECOND TRIGGER (autopsy item 3: "`_escape` needs a
        # 'same two tiles for N rounds' trigger instead of only
        # free_neighbours == 0").  The nav-level break handles the ordinary
        # 2-cycle; this answers the case where the perpendiculars are walls or
        # our OWN buildings and the shuttle is therefore unbreakable by walking
        # -- the stavkirke seat-B shape, four builders oscillating for 1000
        # rounds with a 94-99% top-2-tile share and ZERO builds between them.
        # ⛔ THREE CONDITIONS AND A CAP, because `destroy` is free, unlimited and
        # cooldown-free, which is precisely how ledger V8 reached 893 builds on
        # one tile: the cycle must be OLD, the walking break must have FAILED
        # repeatedly, and a body may buy its way out at most SK_CYCLE_ESCAPE_CAP
        # times in its life.
        boxed = self.free_neighbours(ct, p) == 0
        cycled = (SK_CYCLE_BREAK
                  and self.cycle_len >= SK_CYCLE_ESCAPE_ROUNDS
                  and self.cycle_blocked >= SK_CYCLE_ESCAPE_BLOCKED
                  and self.cycle_escapes < SK_CYCLE_ESCAPE_CAP)
        if not boxed and not cycled:
            return False
        if cycled and not boxed:
            self.cycle_escapes += 1
            self.cycle_len = 0
            self.cycle_blocked = 0
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
            self.belt_seen.pop((q.x, q.y), None)       # v604 FIX 4(b)
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
            # ⭐ v618 PLANK 4's VETO.  A seat PLANK 4 refused this round (three
            # peckers and no gun -- an arithmetically lost race) must not be
            # healed by the generic rung underneath it, or the guard is
            # decoration.  Flag off => `seat_heal_veto` is never populated and
            # this test is a no-op on an empty set.
            if SK_SEAT_HEAL and (q.x, q.y) in self.seat_heal_veto:
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
            if not self.path_arbiter_ok(ct, q, rnd):
                continue          # v605 FIX 1: a harvester is impassable
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
        # v606 ITEM 2: `self.enemy` joins the key because the BAND is derived
        # from it -- it is unset until the core reports it, and a plan cached
        # before that would never see the band at all.
        key = (self.core, self.enemy, len(self.harv_tiles), len(self.belt_ban),
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
        # v606 ITEM 2 (SK_BELT_BAND_AVOID): a THIRD pass in front of the ore
        # cascade.  The band is the enemy sentinel's reach; a trunk laid inside
        # it died 6 times out of 9 on the v604/v605 tapes against 11.7% overall.
        # It is RELAXED on exactly the condition the ore pass is relaxed on --
        # a harvester left with no route home is worth zero forever -- so the
        # "unless the tile is the only route to the ore" exception is honoured
        # by construction rather than asserted.  ⛔ FLAG OFF => `band` is None
        # in every call and the cascade is the v605 two-pass form byte for byte.
        band = self._belt_band() if SK_BELT_BAND_AVOID else None
        targets = self.harv_tiles
        parent = None
        if band:
            for av_ore in (True, False):
                p = self._belt_parents(ct, avoid_ore=av_ore, band=band)
                if p is None:
                    return                     # CPU exhausted -- keep last plan
                reach = {h for h in self.harv_tiles if h in p}
                if len(reach) == len(self.harv_tiles):
                    parent = p                 # band-free route to every seat
                    break
                if SK_BELT_BAND_DROP and reach and not av_ore:
                    # ⛔ THE HALF THAT ACTUALLY BINDS, and it is a DOCTRINE call
                    # not a bug fix: some seats are reachable only THROUGH their
                    # guns.  v605 laid that chain anyway -- 9 pieces, 6 dead, a
                    # 66.7% marginal death rate against 11.7% overall -- to serve
                    # ONE harvester whose short route `belt_ban` had escalated
                    # away.  Under R1000_IS_DEFEAT the titanium is instrumental
                    # and the builder turns are not: drop THAT seat from the plan
                    # and keep the rest of the belt band-free.  Never drop the
                    # last seat -- `reach` non-empty is the guard, and the
                    # cascade below is the fallback when it is empty.
                    parent, targets = p, reach
                    break
        if parent is None:
            parent = self._belt_parents(ct, avoid_ore=True)
            if parent is None:
                return
            if any(h not in parent for h in self.harv_tiles):
                parent = self._belt_parents(ct, avoid_ore=False)
                if parent is None:
                    return
        core_xy = set(core_tiles_xy(self.core))
        plan = {}
        # v606 ITEM 2: `targets` is `self.harv_tiles` in every case except the
        # band-drop one, where it is the band-free subset.
        for h in targets:
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

    def _belt_band(self):
        """v606 ITEM 2 -- the enemy turret band as an (x, y) set, or None.

        d^2 <= SK_BELT_BAND_DSQ (32, the sentinel's reach) of the ENEMY core
        FOOTPRINT.  None whenever the enemy core is not yet known, so the belt
        never waits on a fact it does not have; the plan re-keys when it lands.
        The band never includes a HARVESTER tile: a harvester already standing
        in the band has already paid, and excluding it would strand it.
        """
        if self.enemy is None:
            return None
        ex, ey = self.enemy.x, self.enemy.y
        r = 0
        while (r + 1) * (r + 1) <= SK_BELT_BAND_DSQ:
            r += 1
        band = set()
        for x in range(ex - r, ex + r + 2):
            for y in range(ey - r, ey + r + 2):
                if not in_bounds(x, y, self.mw, self.mh):
                    continue
                if dsq_core(Position(x, y), self.enemy) > SK_BELT_BAND_DSQ:
                    continue
                if (x, y) in self.harv_tiles:
                    continue
                band.add((x, y))
        return band or None

    def _belt_parents(self, ct, avoid_ore, band=None):
        """Single-source BFS from the core footprint; (x,y) -> next tile home.

        Ore is avoided on the first pass because a conveyor standing on ore
        consumes a harvester seat permanently.  `band` (v606 ITEM 2) is a tile
        set the trunk must not enter -- the enemy turret band; it is passed as
        None on the relaxing passes, which is what makes the flag-off cascade
        identical to v605's.

        ⭐ v613 PLANK 1(b), SK_APRON_BELT_PREF -- THE ONE PLACE THE PREFERENCE
        CAN LIVE WITHOUT CHANGING A SINGLE ROUTE'S LENGTH.  Every reachable tile
        enters `parent` whatever the order; what the order decides is WHICH
        equal-depth parent a tile gets, and therefore which tiles the chains
        actually walk through.  Expanding the apron members of each BFS level
        first makes an apron tile the preferred parent at equal depth, so the
        belt routes THROUGH the apron rather than around it -- an occupied apron
        tile is a denied plant seat, and this half pays for it with a conveyor
        the plan was going to buy anyway.  ⛔ IT IS A TIE-BREAK AND NOTHING
        MORE: the frontier is a level set, so re-ordering inside it cannot make
        any chain longer.
        """
        apron = None
        if SK_APRON_DENY and SK_APRON_BELT_PREF and self.core is not None:
            apron = set(self._apron_list())
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
                if band is not None and (qx, qy) in band:
                    continue
                if (qx, qy) in parent:
                    continue
                parent[(qx, qy)] = (cx, cy)
                frontier.append((qx, qy))
        if apron:
            frontier = ([t for t in frontier if t in apron]
                        + [t for t in frontier if t not in apron])
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
                    if band is not None and (qx, qy) in band:
                        continue
                    if (avoid_ore and self.ore_at(qx, qy)
                            and (qx, qy) not in self.harv_tiles):
                        continue
                    parent[(qx, qy)] = (x, y)
                    nxt.append((qx, qy))
            if apron:
                nxt = ([t for t in nxt if t in apron]
                       + [t for t in nxt if t not in apron])
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
            self.belt_seen[(q.x, q.y)] = rnd      # v604 FIX 4(b): our own build
                                                  # is an OBSERVATION, and dated
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
                self.belt_seen[(q.x, q.y)] = rnd   # v604 FIX 4(b)
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
                    self.belt_seen.pop((q.x, q.y), None)   # v604 FIX 4(b)
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
        # ⭐ v603 FIX 4 (SK_COLLAR_GUNS) -- THIS BRANCH IS 91.1% OF OUR ENTIRE
        # MELEE BUDGET AND IT LOSES THE EXCHANGE 4.8 TO 1.  Pooled over 30 games
        # we threw 2,179 pecks at their barriers on our own delivery ring, killed
        # 106, and left 238 standing at the end; they spent 495 pecks in total
        # and took our harvester->core connectivity from a possible 81% to 25%.
        # 2 damage a round into a 30 HP barrier they re-lay in ~1 round is
        # arithmetic we cannot win, and the budget it eats is what starved the
        # seal eviction (68 pecks) and everything else.  TWO GATES, and the third
        # (`_enemy_builder_adjacent`, the healing race) is already above:
        #   (1) peck ONLY where this tile is the BINDING gap -- the last thing
        #       between some live harvester and the core.  The autopsy's belt-gap
        #       BFS: 33 of 76 alive harvesters, and all 25 the BFS called
        #       unreachable, were exactly ONE enemy barrier from a complete route
        #       home.  That one tile is worth pecking; a tile with three gaps
        #       behind it is worth nothing yet.
        #   (2) a BUDGET of SK_COLLAR_PECK_CAP = 15 pecks per tile (30 HP / 2).
        #       A cap that FIRES means the healing race is lost on that tile, so
        #       the tile is banned and the belt re-routes -- which is the
        #       autopsy's "route the terminus to a seat they have not sealed",
        #       reached through the existing planner instead of a new one.
        # ⛔ THE SOURCE, not the symptom, is FIX 2: a terminus gunner kills the
        # BUILDER that lays the collar (their builder dies to two gunner shots,
        # and 79 of our 157 trunk-gun shots already land on builder bots).
        if SK_COLLAR_GUNS:
            n = self.collar_pecks.get((q.x, q.y), 0)
            if n >= SK_COLLAR_PECK_CAP:
                self.belt_ban.add((q.x, q.y))
                self.belt_key = None
                return False
            if (SK_COLLAR_ROUTE_GATE
                    and (q.x, q.y) not in self._route_gaps(ct, rnd)):
                return False
        # ⭐⭐ v618's RIDER -- PECK DEMOTION, and it is v610's cap tightened by
        # the thing that replaces it.  Where one of our live turrets ACTUALLY
        # BEARS on this tile the gun does 7 a round for 4 ammo; the keeper's
        # peck does 2 and costs the scarce good that all three refuted
        # builder-turn answers named.  ⛔ NO BAN: the tile is not conceded, it is
        # DELEGATED -- banning it would re-route the belt away from a tile the
        # gun is about to clear, which is the opposite of the intent.
        if SK_PECK_DEMOTE and self._gun_bears(ct, q):
            self.peck_demoted += 1
            return False
        try:
            if ct.can_fire(q):
                ct.fire(q)
                if SK_COLLAR_GUNS:
                    self.collar_pecks[(q.x, q.y)] = (
                        self.collar_pecks.get((q.x, q.y), 0) + 1)
                return True
        except Exception:
            return False
        return False

    def _route_gaps(self, ct, rnd):
        """v603 FIX 4 -- tiles that are the SOLE missing link on some live
        harvester's route home.  Cached for the round.

        The walk is `_belt_report`'s, with one difference: instead of asking "is
        this chain complete" it collects the chain's UNBUILT tiles, and a chain
        with exactly one names that tile.  `belt_built` is kept honest by
        `_belt_watch` (a planned tile seen empty is discarded), so a tile an
        enemy building occupies is by construction not in it.
        """
        if self._gap_rnd == rnd and self._gap_key == self.belt_key:
            return self._gap_set
        out = set()
        for h in self.harv_tiles:
            cur = self.belt_head.get(h)
            if cur is None:
                continue                        # feeds the core direct
            miss = []
            hops = 0
            while hops < 200:
                if cur not in self.belt_plan:
                    miss = []                   # broken plan, not a one-gap chain
                    break
                # ⭐ v604 FIX 4 CHANGES WHAT `belt_built` MEANS HERE, and this is
                # the consumer the change is FOR.  In v603 it was "tiles THIS BODY
                # laid", so a replacement keeper walked every chain and found it
                # many-gapped -- and this walk fires only on a chain with EXACTLY
                # ONE gap, so a pessimistic ledger does not make the gate cautious,
                # it SWITCHES THE GATE OFF.  That is the mechanism behind the v603
                # arm (bifrost A 2,470 -> 400 Ti with the gate on).  It is now a
                # belief fed by vision (`_belt_watch`) and by the store's terminus
                # bits (`_belt_seed_store`), and a stale PRESENT belief is kept
                # rather than deleted while SK_BELT_EST_STALE_BUILT holds.
                if cur not in self.belt_built:
                    miss.append(cur)
                    if len(miss) > 1:
                        break
                nxt = self._belt_next(cur)
                if nxt is None:
                    miss = []
                    break
                if self.core is not None and adjacent_to_core(
                        Position(cur[0], cur[1]), self.core):
                    break
                cur = nxt
                hops += 1
            if len(miss) == 1:
                out.add(miss[0])
        self._gap_rnd = rnd
        self._gap_key = self.belt_key
        self._gap_set = out
        return out

    # ------------------------------------------------------------------
    # v610 PLANK 1 -- SK_SEAT_CLEAR: the delivery seats get an owner
    # ------------------------------------------------------------------

    def _seat_targets(self, ct, rnd):
        """The enemy-held delivery seats worth contesting, best first.

        THE MEASUREMENT THIS EXISTS FOR (v609 tape, 30 games, per-episode seat
        lifecycle in `scratchpad/s54_v610/seatlife.py`): 206 enemy occupancy
        episodes on our eight seats, we ever peck 25 = 12.1%, and 84.5% of them
        sit on a seat the tree never once considers.  On the 0.80 seats a game
        we DO touch we peck 78.1% of episodes and kill them -- so the verb
        works and is simply never aimed.  It is never aimed because
        `_belt_evict` can only fire on a tile that is in `belt_plan` AND
        orthogonally adjacent to this body, and the single-source planner
        terminates on ONE seat per chain.

        RANKING, and it is the bound as much as the order:
          1. a seat `_route_gaps` names -- the SOLE missing link on some live
             harvester's route home.  That tile is worth its harvester's whole
             remaining output;
          2. a seat the current belt plan needs at all;
          3. any other enemy-held seat, nearest first.
        Only the first `SK_SEAT_CLEAR_N` are returned: we need one seat per
        live chain, not eight, and v603 measured the unbounded form at 2,179
        pecks with 238 of their barriers still standing at the end.
        """
        if not SK_SEAT_CLEAR or self.core is None:
            return []
        if self._seat_rnd == rnd:
            return self._seat_list
        gaps = self._route_gaps(ct, rnd) if SK_TERMINATE else set()
        cand = []
        for xy in core_seats(self.core):
            if not self.ib(xy[0], xy[1]):
                continue
            q = Position(xy[0], xy[1])
            try:
                bid = ct.get_tile_building_id(q)
            except Exception:
                continue                    # not in vision: no claim either way
            if bid is None:
                continue
            try:
                if ct.get_team(bid) == self.team:
                    continue
                et = ct.get_entity_type(bid)
            except Exception:
                continue
            # ⛔ NEVER a CORE tile and never something ARMED: an enemy turret on
            # our own ring is `_door_action`'s target and outranks this by a
            # long way; a 2 Ti peck into a 25-40 HP gun that is shooting is the
            # exchange v601 already priced as a loss.
            if et == EntityType.CORE or et in ARMED_TYPES:
                continue
            if self.gave_up(bid, rnd):
                continue
            if xy in gaps:
                rank = 0
            elif xy in self.belt_plan:
                rank = 1
            else:
                rank = 2
            cand.append((rank, dsq_core(q, self.core), xy, bid, et))
        cand.sort()
        self._seat_rnd = rnd
        self._seat_list = cand[:SK_SEAT_CLEAR_N]
        return self._seat_list

    def _seat_covered(self, q):
        """True if one of OUR live turrets can bear on tile q.

        The permissive disc form (a gunner may rotate for 10 Ti), matching
        `_belt_cover`.  Its only consumer is the healing-race exception, and
        being optimistic there is the direction that lets the exception fire --
        which is why it is behind its own flag and its own ablation.
        """
        for _eid, et, ep in self.vis_friend:
            if et not in TURRET_TYPES:
                continue
            reach = 13 if et == EntityType.GUNNER else 32
            dx = ep.x - q.x
            dy = ep.y - q.y
            if dx * dx + dy * dy <= reach:
                return True
        return False

    def _seat_budget_ok(self, xy, bid):
        """PER-EPISODE, not per tile.  Returns True if this peck is affordable.

        ⛔ THE DEFECT THIS REPLACES, measured live on glacierkeep seat A:
        `collar_pecks` is keyed on the TILE and never reset, so the 15 pecks
        that killed their barrier at r48 are still on the ledger when they
        re-lay the same seat at r146 -- and the tile is conceded for the rest
        of the game.  Keying on (tile, occupant id) makes a re-laid barrier a
        new contest.  The per-GAME total is the backstop that stops that from
        becoming v603's 2,179.
        """
        if self.seat_peck_total >= SK_SEAT_PECK_TOTAL:
            return False
        prev = self.seat_pecks.get(xy)
        if prev is not None and prev[0] == bid and prev[1] >= SK_SEAT_PECK_CAP:
            return False
        return True

    def _seat_charge(self, xy, bid):
        prev = self.seat_pecks.get(xy)
        n = prev[1] + 1 if (prev is not None and prev[0] == bid) else 1
        self.seat_pecks[xy] = (bid, n)
        self.seat_peck_total += 1

    def _seat_clear(self, ct, p, rnd):
        """PLANK 1's ACTION half -- peck an adjacent enemy-held delivery seat.

        True if it took the turn.  Every guard here is one the tree already
        pays for elsewhere; the plank's contribution is the AIM, not a new
        exchange.
        """
        if not SK_SEAT_CLEAR:
            return False
        if ct.get_global_resources() < 2:
            return False
        for (_rank, _d, xy, bid, _et) in self._seat_targets(ct, rnd):
            q = Position(xy[0], xy[1])
            if p.distance_squared(q) != 1:
                continue                    # orthogonal adjacency only
            if not self._seat_budget_ok(xy, bid):
                continue
            if not self.hp_trend_ok(ct, bid, rnd):      # ledger V7
                continue
            if self._enemy_builder_adjacent(ct, q):
                # DOORWAVE's lesson: 2 dmg against a +4 heal is a race we lose.
                # THE ONE EXCEPTION (SK_SEAT_GUN_RACE): with a gun of ours
                # bearing on the tile the round's damage is 2 + 7 (or 2 + 18)
                # against +4, and the race flips.
                if not (SK_SEAT_GUN_RACE and self._seat_covered(q)):
                    continue
            # ⭐ v618's RIDER, the SECOND site.  SK_SEAT_CLEAR ships OFF, so this
            # is dormant on the shipped chassis and is here for completeness of
            # the class: wherever a BUILDER pecks a collar barrier, a gun that
            # bears on the tile outranks it.  Applied at BOTH sites so the rider
            # is a property of the verb class, not of one method.
            if SK_PECK_DEMOTE and self._gun_bears(ct, q):
                self.peck_demoted += 1
                continue
            try:
                if not ct.can_fire(q):
                    continue
                ct.fire(q)
            except Exception:
                continue
            self._seat_charge(xy, bid)
            self.seat_clears += 1
            return True
        return False

    def _seat_walk(self, ct, p, rnd):
        """PLANK 1's MOVEMENT half -- the tile to stand on to peck a seat.

        Returns a Position or None.  Without this the action half fires only
        where the body already happens to stand, which is the 12.1% the census
        measured.  The walk is short by construction: a delivery seat is
        d^2 <= 2 from our own footprint, so this never pulls the keeper out of
        the home quadrant and never competes with `_medic_seat` for distance.
        """
        if not SK_SEAT_CLEAR:
            return None
        for (_rank, _d, xy, bid, _et) in self._seat_targets(ct, rnd):
            if not self._seat_budget_ok(xy, bid):
                continue
            q = Position(xy[0], xy[1])
            if p.distance_squared(q) == 1:
                return None                 # already seated; the action fires
            best = None
            for d in CARDINALS:
                r = q.add(d)
                if not self.ibp(r):
                    continue
                if r.x == p.x and r.y == p.y:
                    return None
                try:
                    if not ct.is_tile_passable(r):
                        continue
                except Exception:
                    continue
                dd = p.distance_squared(r)
                if best is None or dd < best[0]:
                    best = (dd, r)
            if best is not None:
                return best[1]
        return None

    # ==================================================================
    # v618 -- THE SEAT-DEFENCE PACKAGE
    # ==================================================================
    # Shared helpers first, then the four planks in the order they act.

    def _seat_face(self, xy):
        """The facing that makes a delivery seat DELIVER: into the footprint.

        ⛔ THIS IS NOT A SECOND OPINION ABOUT THE BELT, IT IS THE SAME ONE.
        `_plan_belt` BFSes from the core footprint, so a seat's parent is a CORE
        TILE and the plan's own `_card(cur - prev)` for that tile is exactly
        this direction.  That identity is what makes the claim zero-waste: when
        the belt plan arrives, the tile already carries a conveyor facing the
        way the plan wanted, and `_belt_evict` records it as BUILT rather than
        rebuilding it.  Returns None if the core is unknown.
        """
        if self.core is None:
            return None
        ox, oy = self.core.x, self.core.y
        x, y = xy
        # The seat touches exactly one footprint tile orthogonally; step at it.
        for cx, cy in core_tiles_xy(self.core):
            if x == cx and y == cy - 1:
                return Direction.SOUTH
            if x == cx and y == cy + 1:
                return Direction.NORTH
            if y == cy and x == cx - 1:
                return Direction.EAST
            if y == cy and x == cx + 1:
                return Direction.WEST
        return None

    def _seat_set(self):
        """OUR eight delivery seats as an (x, y) set.  Pure function of the
        anchor, so every body -- keeper, gunner, sentinel -- derives the same
        eight tiles with nothing to agree on.  That property is why
        `core_seats` is canonical (v604 FIX 4) and it is what lets PLANK 3 run
        inside a TURRET, which owns no belt plan.
        """
        if self.core is None:
            return frozenset()
        return frozenset(core_seats(self.core))

    def _gun_bears(self, ct, q):
        """True if a live turret of OURS can fire on tile q AS IT NOW FACES.

        ⛔ THE STRICT TEST, AND THE POLARITY IS THE POINT.  `_seat_covered`
        above is the permissive rotatable-DISC form and it feeds a plank
        ADMISSION (the healing-race exception), where optimism lets the
        exception fire.  This one feeds a plank VETO (the peck demotion), and a
        veto computed optimistically refuses a peck because of a gun that
        cannot presently shoot the tile at all.  `can_fire_from` is the
        engine's own hypothetical-turret predicate and it ignores ammo and
        cooldown, which is right here: the question is BEARING, not readiness.
        """
        for eid, et, ep in self.vis_friend:
            if et not in TURRET_TYPES:
                continue
            try:
                face = ct.get_direction(eid)
                if ct.can_fire_from(ep, face, et, q):
                    return True
            except Exception:
                continue
        return False

    # --- PLANK 1 -- SK_SEAT_CLAIM ---------------------------------------

    def _claim_spawn_ok(self, ct, q):
        """⛔⛔ THE SPAWN RESERVE, and it answers a SPECIFIC engine geometry.

        `_spawn_plan` offers the core `p.add(d)` over the 8 DIRECTIONS FROM THE
        ANCHOR.  Three of those land inside the 2x2 footprint; FOUR are delivery
        seats -- N (ox,oy-1), NE (ox+1,oy-1), W (ox-1,oy) and SW (ox-1,oy+1) --
        and exactly ONE, the NW corner (ox-1,oy-1), is not a seat and may be a
        wall.  Claim all four seats and a replacement builder has one candidate
        tile left in the whole spawn loop.  Builder deaths run 29 of 30 games on
        the F1 tape, so this is a routine path, not a corner case.

        Returns True iff at least SK_SEAT_CLAIM_SPAWN_RESERVE anchor-adjacent
        tiles would still be spawnable after putting a building on q.
        ⚠ AN UNREADABLE TILE COUNTS AS NOT SPAWNABLE -- the guard fails toward
        REFUSING the claim, which is the direction that cannot cost us a body.
        """
        if self.core is None:
            return True
        free = 0
        for dx, dy in NEIGHBOURS8:
            x, y = self.core.x + dx, self.core.y + dy
            if not self.ib(x, y):
                continue
            if (x, y) == (q.x, q.y):
                continue                    # the tile we are about to fill
            if (x, y) in core_tiles_xy(self.core):
                continue
            try:
                if ct.is_tile_empty(Position(x, y)):
                    free += 1
            except Exception:
                continue                    # unreadable: NOT counted as free
        return free >= SK_SEAT_CLAIM_SPAWN_RESERVE

    def _claim_targets(self, ct, rnd):
        """The EMPTY delivery seats this body may claim, nearest first.

        Empty is the whole trigger: occupancy is EXCLUSIVE on this engine (a
        build requires an empty tile), so a seat we hold cannot receive their
        barrier, and a seat they hold is `_seat_clear`'s problem, not this
        plank's.  A pre-claim never contests -- that is what makes it cheap.
        """
        if not SK_SEAT_CLAIM or self.core is None:
            return []
        if rnd > SK_SEAT_CLAIM_UNTIL or self.seat_claims >= SK_SEAT_CLAIM_MAX:
            return []
        out = []
        for xy in core_seats(self.core):
            if not self.ib(xy[0], xy[1]):
                continue
            if xy in self.seat_claimed:
                continue
            q = Position(xy[0], xy[1])
            try:
                if not ct.is_tile_empty(q):
                    continue
                # ⛔ NEVER ON ORE.  A conveyor on an ore tile consumes a
                # harvester seat permanently, and `_harvester_action` already
                # denies that tile with a building that also EARNS.
                if ct.get_tile_env(q) == Environment.ORE_TITANIUM:
                    continue
            except Exception:
                continue
            # ⭐ THE SITING RULE.  Their layer walks in from THEIR core, so the
            # enemy-facing seats are the contested ones; the far-side seats are
            # claimed against nobody and are pure keeper-turn cost whenever the
            # budget binds.  Falls back to distance-from-us while the enemy
            # anchor is still unknown -- it is derived at r0 by `enemy_core_for`
            # in practice, so the fallback is a first-turn condition only.
            if SK_SEAT_CLAIM_ENEMY_FIRST and self.enemy is not None:
                rank = dsq_core(q, self.enemy)
            else:
                rank = dsq_core(q, self.core)
            out.append((rank, xy))
        out.sort()
        return out

    def _seat_claim_action(self, ct, p, rnd):
        """PLANK 1's ACTION half -- lay OUR conveyor on an empty delivery seat.

        True if it took the turn.  Sits just BELOW the harvester-critical verbs
        and ABOVE the general belt, per the design: a harvester with no route
        home is worth zero forever, but a seat is only claimable while it is
        still empty and the collar lands at median r11.
        """
        if not SK_SEAT_CLAIM:
            return False
        cost = ct.get_conveyor_cost()
        if ct.get_global_resources() < cost:
            return False
        for (_d2, xy) in self._claim_targets(ct, rnd):
            q = Position(xy[0], xy[1])
            if p.distance_squared(q) != 1:
                continue                    # orthogonal adjacency only
            face = self._seat_face(xy)
            if face is None:
                continue
            if xy in self.belt_escalated or self.escape_ban.get(xy, -1) > rnd:
                continue
            # The arbiter: a seat is OWNER_BELT when the plan already wants it
            # and OWNER_DOOR otherwise, and this verb is entitled to both --
            # it lays the belt's own terminus, on the door's own ring.
            owner = self.tile_owner(q)
            if owner not in (OWNER_NONE, OWNER_DOOR, OWNER_BELT):
                continue
            if self.free_neighbours(ct, p, exclude=q) == 0:
                continue                    # self-trap guard
            if not self._claim_spawn_ok(ct, q):
                self.seat_claim_refused += 1
                continue
            if not self.path_arbiter_ok(ct, q, rnd):
                continue                    # a conveyor is IMPASSABLE
            try:
                if not ct.can_build_conveyor(q, face):
                    continue
                ct.build_conveyor(q, face)
            except Exception:
                continue
            self.seat_claims += 1
            self.seat_claimed[xy] = rnd
            # The claim IS a belt build when the plan wants the tile, so the
            # belt's own ledgers learn about it the way they learn about
            # `_belt_action`'s builds.  Otherwise the plan has not reached here
            # yet and `_belt_evict` will adopt the tile when it does.
            if xy in self.belt_plan:
                self.belt_built.add(xy)
                self.belt_seen[xy] = rnd
            return True
        return False

    def _seat_claim_walk(self, ct, p, rnd):
        """PLANK 1's MOVEMENT half -- the tile to stand on to claim.  Or None.

        ⛔ FENCED BY DISTANCE, and that fence is the v610 lesson: the cost of a
        home plank is measured in KEEPER ROUNDS, not in titanium.  The keeper
        only diverts at a seat it is already within SK_SEAT_CLAIM_WALK_DSQ of,
        so the claim never competes with the harvester walk for the early game.
        """
        if not (SK_SEAT_CLAIM and SK_SEAT_CLAIM_WALK):
            return None
        for (_d2, xy) in self._claim_targets(ct, rnd):
            q = Position(xy[0], xy[1])
            if p.distance_squared(q) == 1:
                return None                 # already seated; the action fires
            if p.distance_squared(q) > SK_SEAT_CLAIM_WALK_DSQ:
                continue
            best = None
            for d in CARDINALS:
                r = q.add(d)
                if not self.ibp(r):
                    continue
                if r.x == p.x and r.y == p.y:
                    return None
                try:
                    if not ct.is_tile_passable(r):
                        continue
                except Exception:
                    continue
                dd = p.distance_squared(r)
                if best is None or dd < best[0]:
                    best = (dd, r)
            if best is not None:
                return best[1]
        return None

    # --- PLANK 2 -- SK_HOME_GUNNER --------------------------------------

    def _home_gun_window(self, rnd):
        """The buy window, as one predicate so the action and the walk cannot
        disagree -- the launcher arm's own lesson ("do not walk at a buy we
        cannot make"), applied before it can bite.
        """
        if not SK_HOME_GUNNER or self.core is None:
            return False
        if self.home_guns >= SK_HOME_GUN_MAX:
            return False
        if rnd < SK_HOME_GUN_MIN_ROUND or rnd > SK_HOME_GUN_MAX_ROUND:
            return False
        if not SK_HOME_GUN_SEPARATE_CAP and self.door_guns >= SK_DOOR_GUN_CAP:
            return False
        return True

    def _home_gun_score(self, ct, q, seats):
        """(seats on the ray, apron tiles on the ray) for the best facing at q,
        with that facing.  The gun is sited by the MEASURED collar geometry: the
        v610 census found 15 distinct grabbing/laying positions and they sit on
        the apron, so a ray that sweeps seats AND apron is the objective.
        """
        best = None
        apron = set(self._apron_list())
        wseat = {xy: 3 for xy in seats}
        wapron = {xy: 1 for xy in apron if xy not in seats}
        for face in DIRECTIONS:
            if face == Direction.CENTRE:
                continue
            ns = self._ray_cover(q, face, wseat)
            na = self._ray_cover(q, face, wapron)
            if ns <= 0:
                continue                    # the plank IS the seat sweep
            # ⛔ TIE-BREAK TOWARD THE ENEMY APPROACH SIDE.  Their collar walks
            # in from their core; a facing that sweeps the same seats from the
            # far side meets the layer a round later.
            toward = 0
            if self.enemy is not None:
                dx, dy = face.delta()
                ex = self.enemy.x - q.x
                ey = self.enemy.y - q.y
                toward = 1 if (dx * ex + dy * ey) > 0 else 0
            score = (ns, toward, na)
            if best is None or score > best[0]:
                best = (score, face)
        if best is None:
            return None, None
        return best[0], best[1]

    def _home_gun_action(self, ct, p, rnd):
        """PLANK 2's ACTION half -- buy THE home gunner.  True if it took the
        turn.  Once a game, early, at low scale.
        """
        if not self._home_gun_window(rnd):
            return False
        if ct.get_global_resources() < ct.get_gunner_cost() + SK_HOME_GUN_RESERVE:
            return False
        seats = self._seat_set()
        if not seats:
            return False
        best = None
        for d in CARDINALS:
            q = p.add(d)
            if not self.ibp(q):
                continue
            # ⛔ NEVER ON A DELIVERY SEAT.  Those eight tiles are the belt's
            # terminus and PLANK 1's claims; a turret on one is a permanently
            # blocked chain, which is the exact defect `_belt_evict` exists for.
            if (q.x, q.y) in seats:
                continue
            owner = self.tile_owner(q)
            if owner not in (OWNER_NONE, OWNER_DOOR):
                continue
            if self._on_enemy_axis(q):
                continue                    # COPY 2: never in their line
            # TWO free neighbours, not one -- v601's measured lesson: a turret
            # is permanent, and a gun that takes the keeper's second-to-last
            # tile gets demolished by `_escape` at full HP the next round.
            if self.free_neighbours(ct, p, exclude=q) < 2:
                continue
            try:
                if not ct.is_tile_empty(q):
                    continue
                if ct.get_tile_env(q) == Environment.ORE_TITANIUM:
                    continue
            except Exception:
                continue
            score, face = self._home_gun_score(ct, q, seats)
            if face is None:
                continue
            if best is None or score > best[0]:
                best = (score, q, face)
        if best is None:
            return False
        _score, q, face = best
        if not self.path_arbiter_ok(ct, q, rnd):
            return False                    # a gunner is IMPASSABLE
        try:
            if not ct.can_build_gunner(q, face):
                return False
            ct.build_gunner(q, face)
        except Exception:
            return False
        self.home_guns += 1
        if not SK_HOME_GUN_SEPARATE_CAP:
            self.door_guns += 1
        return True

    def _home_gun_walk(self, ct, p, rnd):
        """PLANK 2's MOVEMENT half -- a tile from which the buy is legal.

        Bounded the same way PLANK 1's is: the site domain is the apron, which
        is d^2 <= SK_APRON_DSQ of our own footprint, so the walk is a home-lap
        step and never a tour.  ⛔ AND IT IS GATED ON THE SAME WINDOW AND THE
        SAME AFFORDABILITY AS THE BUY -- a keeper standing beside an
        unaffordable tile is the v610 cost in a new hat (the launcher arm's
        own finding, quoted so it is not re-learned).
        """
        if not self._home_gun_window(rnd):
            return None
        if ct.get_global_resources() < ct.get_gunner_cost() + SK_HOME_GUN_RESERVE:
            return None
        seats = self._seat_set()
        if not seats:
            return None
        if self.home_gun_rnd == rnd:
            site = self.home_gun_site
        else:
            best = None
            for xy in self._apron_list():
                if xy in seats:
                    continue
                q = Position(xy[0], xy[1])
                if p.distance_squared(q) <= 1:
                    continue                # adjacent already: the action fires
                try:
                    if not ct.is_tile_empty(q):
                        continue
                except Exception:
                    continue
                if self.tile_owner(q) not in (OWNER_NONE, OWNER_DOOR):
                    continue
                if self._on_enemy_axis(q):
                    continue
                score, face = self._home_gun_score(ct, q, seats)
                if face is None:
                    continue
                cand = (score, -p.distance_squared(q))
                if best is None or cand > best[0]:
                    best = (cand, q)
            site = best[1] if best is not None else None
            self.home_gun_rnd = rnd
            self.home_gun_site = site
        if site is None:
            return None
        # Stand orthogonally beside the site, not on it.
        best = None
        for d in CARDINALS:
            r = site.add(d)
            if not self.ibp(r):
                continue
            if r.x == p.x and r.y == p.y:
                return None                 # already in position
            try:
                if not ct.is_tile_passable(r):
                    continue
            except Exception:
                continue
            dd = p.distance_squared(r)
            if best is None or dd < best[0]:
                best = (dd, r)
        if best is None:
            return None
        self.home_gun_walks += 1
        return best[1]

    # --- PLANK 3 -- SK_GUN_ROUTEBLOCK -----------------------------------

    def _routeblock_tile(self, xy):
        """True if an enemy BARRIER on `xy` is a route-blocking collar barrier.

        ⛔ COMPUTED FROM THE CORE ANCHOR ALONE, because the consumer is a
        TURRET and a turret owns no belt plan, no harvester set and no
        `_route_gaps`.  That is not an approximation of the plan -- the eight
        delivery seats ARE the only tiles that can deliver into the core, so a
        barrier standing on one blocks every chain that would terminate there,
        whichever chain that turns out to be.  SK_ROUTEBLOCK_ADJ widens it by
        one ring, inside the apron, because the census's laying positions are
        15 distinct tiles and a barrier one tile off the seat still blocks the
        chain that feeds it.
        """
        if self.core is None:
            return False
        seats = self._seat_set()
        if xy in seats:
            return True
        if not SK_ROUTEBLOCK_ADJ:
            return False
        if dsq_core(Position(xy[0], xy[1]), self.core) > SK_ROUTEBLOCK_DSQ:
            return False
        for dx, dy in CARD_DELTAS:
            if (xy[0] + dx, xy[1] + dy) in seats:
                return True
        return False

    # --- PLANK 4 -- SK_SEAT_HEAL ----------------------------------------

    def _seat_peckers(self, ct, q):
        """How many ENEMY BUILDER BOTS stand orthogonally adjacent to q.

        The arithmetic this feeds is exact: a peck is 2 damage, a heal is +4,
        so one heal cancels exactly two peckers and a third makes the race
        arithmetically unwinnable.  DOORWAVE lost that race from the other side
        of the map; this is the same sum with the signs swapped.
        """
        n = 0
        for dx, dy in CARD_DELTAS:
            x, y = q.x + dx, q.y + dy
            if not self.ib(x, y):
                continue
            try:
                uid = ct.get_tile_builder_bot_id(Position(x, y))
                if uid is None:
                    continue
                if ct.get_team(uid) != self.team:
                    n += 1
            except Exception:
                continue
        return n

    def _seat_heal_ok(self, ct, q):
        """The budget clause, as its own predicate so the veto is auditable.

        Heal only while the peckers are at or below SK_SEAT_HEAL_PECK_MAX, OR
        while a gun of ours covers the tile (then the round's damage is 7 or 18
        on our side too and the count stops mattering).
        """
        if self._seat_peckers(ct, q) <= SK_SEAT_HEAL_PECK_MAX:
            return True
        return bool(SK_SEAT_HEAL_GUN_RACE and self._seat_covered(q))

    def _seat_heal_action(self, ct, p, rnd):
        """PLANK 4's ACTION half -- heal OUR building on a delivery seat that
        is losing HP.  True if it took the turn.

        ⛔ IT ALSO PUBLISHES A VETO, and that half is not decoration.  The
        generic `_heal_action` directly below it heals the most-damaged
        adjacent friendly with no race arithmetic at all, so without the veto a
        seat this plank REFUSED (three peckers, no gun) would be healed anyway
        by the next rung down and the DOORWAVE guard would be cosmetic.
        """
        if self.seat_heal_veto_rnd != rnd:
            self.seat_heal_veto = set()
            self.seat_heal_veto_rnd = rnd
        if not SK_SEAT_HEAL or self.core is None:
            return False
        if self.seat_heals >= SK_SEAT_HEAL_MAX:
            return False
        if ct.get_global_resources() <= SK_SEAT_HEAL_TI_FLOOR:
            return False
        seats = self._seat_set()
        best = None
        for d in CARDINALS:
            q = p.add(d)
            if not self.ibp(q) or (q.x, q.y) not in seats:
                continue
            try:
                bid = ct.get_tile_building_id(q)
                if bid is None or ct.get_team(bid) != self.team:
                    continue
                miss = ct.get_max_hp(bid) - ct.get_hp(bid)
            except Exception:
                continue
            if miss < 4:
                continue                    # a +4 heal that overflows is waste
            if not self._seat_heal_ok(ct, q):
                self.seat_heal_veto.add((q.x, q.y))
                self.seat_heal_refused += 1
                continue
            if best is None or miss > best[0]:
                best = (miss, q)
        if best is None:
            return False
        try:
            if not ct.can_heal(best[1]):
                return False
            ct.heal(best[1])
        except Exception:
            return False
        self.seat_heals += 1
        return True

    def _seat_heal_walk(self, ct, p, rnd):
        """PLANK 4's MOVEMENT half -- ONE STEP, never more.

        "if adjacent or 1 step away" is the design's own wording and it is also
        the fence: a heal is worth a step, it is not worth a tour.  The target
        therefore has to be a tile this body can reach THIS round.
        """
        if not (SK_SEAT_HEAL and SK_SEAT_HEAL_WALK) or self.core is None:
            return None
        if self.seat_heals >= SK_SEAT_HEAL_MAX:
            return None
        if ct.get_global_resources() <= SK_SEAT_HEAL_TI_FLOOR:
            return None
        seats = self._seat_set()
        best = None
        for d in CARDINALS:
            r = p.add(d)                    # the ONE step we are allowed
            if not self.ibp(r):
                continue
            try:
                if not ct.is_tile_passable(r):
                    continue
            except Exception:
                continue
            for d2 in CARDINALS:
                q = r.add(d2)
                if not self.ibp(q) or (q.x, q.y) not in seats:
                    continue
                if p.distance_squared(q) == 1:
                    return None             # already adjacent; the action fires
                try:
                    bid = ct.get_tile_building_id(q)
                    if bid is None or ct.get_team(bid) != self.team:
                        continue
                    miss = ct.get_max_hp(bid) - ct.get_hp(bid)
                except Exception:
                    continue
                if miss < 4:
                    continue
                if not self._seat_heal_ok(ct, q):
                    continue
                if best is None or miss > best[0]:
                    best = (miss, r)
        return best[1] if best is not None else None

    # ------------------------------------------------------------------
    # v613 PLANK 1 -- SK_APRON_DENY: the d^2 <= 5 apron gets an OWNER
    # ------------------------------------------------------------------

    def _apron_list(self):
        """The apron tiles as an (x, y) tuple, cached on the core anchor.

        d^2 <= SK_APRON_DSQ of the 2x2 footprint, in bounds, excluding the
        footprint itself.  28 of the 48 enemy turrets that ever damaged our core
        across the tapemj tape stand inside this set.
        """
        if self.core is None:
            return ()
        if self._apron_cache is not None and self._apron_key == (
                self.core.x, self.core.y, self.mw, self.mh):
            return self._apron_cache
        foot = set(core_tiles_xy(self.core))
        r = 0
        while (r + 1) * (r + 1) <= SK_APRON_DSQ:
            r += 1
        out = []
        for x in range(self.core.x - r, self.core.x + r + 2):
            for y in range(self.core.y - r, self.core.y + r + 2):
                if not self.ib(x, y) or (x, y) in foot:
                    continue
                if dsq_core(Position(x, y), self.core) <= SK_APRON_DSQ:
                    out.append((x, y))
        self._apron_key = (self.core.x, self.core.y, self.mw, self.mh)
        self._apron_cache = tuple(out)
        return self._apron_cache

    def _apron_watch(self, ct, p, rnd):
        """The BELIEF half.  Which apron tiles carried one of OUR buildings, and
        which of those are now EMPTY -- i.e. a free plant seat.

        ⛔ THIS IS THE `helheim_B` MECHANISM AND IT IS WHY THE PLANK IS A RELAY.
        Our conveyor at (14,6) is destroyed at r56; THEIR SENTINEL IS BUILT ON
        THAT TILE AT r58.  Two rounds.  Passive occupancy answers nothing --
        what the tile needs is an owner who notices it went empty.

        ⛔ AND AN UNSEEN TILE IS NOT AN EMPTY TILE (the `_hl_seat_census`
        lesson).  `get_tile_building_id` raises outside vision, so a tile this
        body cannot see contributes to neither belief; the memo simply keeps its
        last observation.  Bounds first, then vision (CLAUDE.md, corrected s50:
        `is_in_vision` is a pure radius test with no bounds check).
        """
        if not SK_APRON_DENY or self.core is None:
            return
        for xy in self._apron_list():
            q = Position(xy[0], xy[1])
            if p.distance_squared(q) > 20:      # this body's vision r^2
                continue
            try:
                if not ct.is_in_vision(q):
                    continue
                bid = ct.get_tile_building_id(q)
            except Exception:
                continue
            if bid is None:
                if xy in self.apron_ours:
                    # OURS, and now gone.  The relay queue is keyed on the tile
                    # and dated so a tile that stays empty for the rest of the
                    # game does not re-enter the queue forever -- the budget is
                    # what bounds it, and the date is what the report reads.
                    self.apron_ours.pop(xy, None)
                    if xy not in self.apron_lost:
                        self.apron_lost[xy] = rnd
                        self.apron_losses += 1
                continue
            try:
                mine = ct.get_team(bid) == self.team
            except Exception:
                continue
            if mine:
                self.apron_ours[xy] = rnd
                self.apron_lost.pop(xy, None)
            else:
                # An ENEMY building on an apron tile is somebody else's job:
                # `_door_action` for a turret on our ring, `_seat_clear` for a
                # delivery seat.  Relaying is a BUILD verb and the tile is not
                # empty, so it drops out of both memos.
                self.apron_ours.pop(xy, None)
                self.apron_lost.pop(xy, None)

    def _apron_budget_ok(self, rnd):
        """SK_APRON_RELAY_CAP relays per SK_APRON_WINDOW rounds, plus a game
        total.  ⛔ THE v610 LESSON AS A CONSTANT: the keeper's turn is the
        scarce good and the belt duty has to survive this plank.
        """
        if self.apron_relay_total >= SK_APRON_RELAY_TOTAL:
            return False
        cut = rnd - SK_APRON_WINDOW
        while self.apron_relays and self.apron_relays[0] <= cut:
            self.apron_relays.pop(0)
        return len(self.apron_relays) < SK_APRON_RELAY_CAP

    def _apron_buildable(self, ct, q, rnd):
        """True if this body may lay a relay on q THIS turn.  Owner-arbitrated."""
        xy = (q.x, q.y)
        if xy in self.belt_escalated or self.escape_ban.get(xy, -1) > rnd:
            return False
        owner = self.tile_owner(q)
        # OWNER_BELT is allowed and is laid as a CONVEYOR with the planned
        # facing, so the relay serves the belt as well as the denial.  CAGE /
        # NEST / DENY belong to verbs that are not this one.
        if owner not in (OWNER_NONE, OWNER_DOOR, OWNER_BELT):
            return False
        try:
            if not ct.is_tile_empty(q):
                return False
        except Exception:
            return False
        # ⛔ NEVER ON ORE.  A barrier on an ore tile consumes a harvester seat
        # permanently, and `_harvester_action` already denies that tile with a
        # building that also earns.
        try:
            if ct.get_tile_env(q) == Environment.ORE_TITANIUM:
                return False
        except Exception:
            return False
        return True

    def _apron_action(self, ct, p, rnd):
        """The RELAY.  True if it took the turn.

        Cheapest building that holds the tile: a CONVEYOR (3 Ti, 20 HP) when the
        tile is on the belt plan -- so the relay is the belt repair as well --
        and a BARRIER (3 Ti, 30 HP) otherwise.
        """
        if not SK_APRON_DENY or self.core is None:
            return False
        if not self._apron_budget_ok(rnd):
            return False
        best = None
        for d in CARDINALS:
            q = p.add(d)
            if not self.ibp(q):
                continue
            xy = (q.x, q.y)
            if xy not in self.apron_lost:
                continue
            if not self._apron_buildable(ct, q, rnd):
                continue
            if self.free_neighbours(ct, p, exclude=q) == 0:
                continue                        # self-trap guard, as the belt's
            d2 = dsq_core(q, self.core)
            if best is None or d2 < best[0]:
                best = (d2, q, xy)
        if best is None:
            return False
        _d2, q, xy = best
        # ⛔ v605 FIX 1's THROAT GUARD, and the S7 battery is right to demand it
        # here: a relay is an IMPASSABLE building laid in the tightest corridor
        # on the board (our own core lap), which is exactly the helheim shape
        # where our own nest sealed the map's only route.
        if not self.path_arbiter_ok(ct, q, rnd):
            return False
        face = self.belt_plan.get(xy)
        try:
            if face is not None:
                if ct.get_global_resources() < ct.get_conveyor_cost():
                    return False
                if not ct.can_build_conveyor(q, face):
                    return False
                ct.build_conveyor(q, face)
                self.belt_built.add(xy)
                self.belt_seen[xy] = rnd
            else:
                if ct.get_global_resources() < ct.get_barrier_cost():
                    return False
                if not ct.can_build_barrier(q):
                    return False
                ct.build_barrier(q)
        except Exception:
            return False
        self.apron_lost.pop(xy, None)
        self.apron_ours[xy] = rnd
        self.apron_relays.append(rnd)
        self.apron_relay_total += 1
        self.apron_relaid += 1
        return True

    def _apron_walk(self, ct, p, rnd):
        """The MOVEMENT half -- the tile to stand on to relay.  Or None.

        Short by construction: every apron tile is within d^2 5 of our own
        footprint, so this cannot pull the keeper out of the home quadrant.
        """
        if not SK_APRON_DENY or self.core is None:
            return None
        if not self._apron_budget_ok(rnd):
            return None
        best = None
        for xy in self.apron_lost:
            q = Position(xy[0], xy[1])
            if not self.ibp(q) or not self._apron_buildable(ct, q, rnd):
                continue
            for d in CARDINALS:
                r = q.add(d)
                if not self.ibp(r):
                    continue
                if r.x == p.x and r.y == p.y:
                    return None                 # already seated; the action fires
                try:
                    if not ct.is_tile_passable(r):
                        continue
                except Exception:
                    continue
                dd = p.distance_squared(r)
                if best is None or dd < best[0]:
                    best = (dd, r)
        return None if best is None else best[1]

    # ------------------------------------------------------------------
    # v611 SK_HOME_LAUNCHER -- the collar verb that is not a builder turn
    # ------------------------------------------------------------------

    def _hl_seat_census(self, ct, rnd):
        """Count rounds each delivery seat carries an ENEMY building.

        The site scorer's density term.  Eight `get_tile_building_id` reads a
        round, and ONLY while the launcher is unbuilt and the flag is on -- so
        the whole cost is bounded by SK_HL_MIN_ROUND plus however long the buy
        waits on funding, typically 10-30 rounds of a 1000-round game.

        ⛔ AN UNSEEN SEAT IS NOT AN EMPTY SEAT.  `get_tile_building_id` raises
        off-map and returns None for "nothing there", and neither answer
        distinguishes "no building" from "outside vision".  The keeper lives on
        its own doorstep and the core's r^2=36 vision covers all eight, so in
        practice this reads true; where it does not, the density term degrades
        to the geometry term, which is exactly what SK_HL_SEAT_DENSITY=False
        measures.
        """
        if self.core is None:
            return
        for xy in core_seats(self.core):
            if not self.ib(xy[0], xy[1]):
                continue
            try:
                bid = ct.get_tile_building_id(Position(xy[0], xy[1]))
                if bid is None or ct.get_team(bid) == self.team:
                    continue
            except Exception:
                continue
            self.hl_density[xy] = self.hl_density.get(xy, 0) + 1

    def _hl_victim_tiles(self):
        """The tiles an enemy builder MUST stand on to work one of our seats.

        A builder builds, attacks and heals ORTHOGONALLY ADJACENT ONLY (never
        diagonal, never its own tile), so the layer of a barrier on seat s is
        standing on one of s's four cardinal neighbours -- and this set is
        therefore not a heuristic, it is the engine's own adjacency rule read
        backwards.  Returns {(x, y): weight}.
        """
        out = {}
        if self.core is None:
            return out
        foot = set(core_tiles_xy(self.core))
        for xy in core_seats(self.core):
            if not self.ib(xy[0], xy[1]):
                continue
            w = 1 + (self.hl_density.get(xy, 0) if SK_HL_SEAT_DENSITY else 0)
            for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                r = (xy[0] + dx, xy[1] + dy)
                if not self.ib(r[0], r[1]) or r in foot:
                    continue
                if out.get(r, 0) < w:
                    out[r] = w
        return out

    def _hl_pick_site(self, ct, rnd):
        """Choose ONE launcher tile, memoised for the game once it is legal.

        THE TWO BARS ARE THE BRIEF'S, and both are checked rather than assumed:
          (a) pickup reach d^2 <= 2 to at least SK_HL_SITE_MIN_COVER distinct
              seat-adjacent tiles;
          (b) at least one throw option at SK_HL_THROW_MIN_DSQ <= d^2 <=
              SK_HL_THROW_MAX_DSQ that lies in the ENEMY half.
        Ranked by covered-tile weight (seat occupancy density), then by cover
        count, then NEAREST OUR CORE, then canonical (x, y) so two keepers on
        the same evidence pick the same tile.

        ⛔ WHAT IT REFUSES, and every refusal is a defect this line has already
        paid for once: a DELIVERY SEAT (the launcher would become the collar it
        exists to answer), a PLANNED BELT TILE (a launcher is impassable and the
        belt is the income), an ORE tile (the only tiles a harvester can ever
        use), and any tile whose env is not EMPTY.
        """
        if self.core is None or self.hl_gaveup:
            return None
        if self.hl_site is not None:
            return self.hl_site
        victims = self._hl_victim_tiles()
        if not victims:
            return None
        seats = set(core_seats(self.core))
        foot = set(core_tiles_xy(self.core))
        best = None
        cx, cy = self.core.x, self.core.y
        span = 4                       # d^2 9 -> |dx| <= 3, plus the 2x2 body
        for dx in range(-span, span + 2):
            for dy in range(-span, span + 2):
                x, y = cx + dx, cy + dy
                if not self.ib(x, y):
                    continue
                q = Position(x, y)
                if (x, y) in foot or (x, y) in seats or (x, y) in self.hl_banned:
                    continue
                if dsq_core(q, self.core) > SK_HL_SITE_DSQ:
                    continue
                if (x, y) in self.belt_plan:
                    continue
                try:
                    if ct.get_tile_env(q) != Environment.EMPTY:
                        continue        # WALL, and ORE_TITANIUM is a harvester's
                    if not ct.is_tile_empty(q):
                        continue        # something already stands here
                except Exception:
                    continue
                cover = 0
                weight = 0
                for (rx, ry) in victims:
                    ddx, ddy = rx - x, ry - y
                    if ddx * ddx + ddy * ddy <= SK_HL_PICKUP_DSQ:
                        cover += 1
                        weight += victims[(rx, ry)]
                if cover < SK_HL_SITE_MIN_COVER:
                    continue
                if not self._hl_has_throw(ct, q):
                    continue
                key = (-weight, -cover, dsq_core(q, self.core), x, y)
                if best is None or key < best[0]:
                    best = (key, q)
        if best is None:
            return None
        self.hl_site = best[1]
        self.hl_site_rnd = rnd
        self.hl_tries = 0
        return self.hl_site

    def _hl_strike(self, rnd):
        """One round of "this site is not working".  Bans it past the bound.

        Called from BOTH the action (adjacent, `can_build_launcher` False) and
        the walk (targeted, still not adjacent), because either one alone leaves
        the other free to run forever -- which is exactly how the first cut
        burned 656 keeper rounds on one tile.
        """
        self.hl_tries += 1
        if self.hl_tries < SK_HL_SITE_GIVEUP:
            return
        if self.hl_site is not None:
            self.hl_banned.add((self.hl_site.x, self.hl_site.y))
        self.hl_site = None
        self.hl_tries = 0
        if len(self.hl_banned) >= SK_HL_SITE_TRIES:
            self.hl_gaveup = True

    def _hl_toward(self, t, ref):
        """"Toward the enemy half" -- STRICTLY CLOSER TO THE ENEMY CORE than
        `ref`, which is where the launcher stands.

        ⛔ MEASURED CORRECTION, AND THE FIRST FORM READ ZERO ON EVERY MAP.  The
        first cut of this predicate was `not self.is_home_half(t)` -- a tile in
        the enemy's HALF of the board.  A launcher sited at d^2 <= 9 of our own
        core can throw at most d^2 26 (5.1 tiles), so the farthest tile it can
        ever reach is ~8 tiles from our core, and on a 26x26 pool map the
        half-line is far beyond that.  The bar was unsatisfiable by
        construction: `_hl_pick_site` returned None in every game of the first
        smoke run and the ON tape was byte-identical to OFF.  A home launcher
        cannot throw into the enemy half and was never going to; what it can do
        is move a body several tiles the wrong way for them, and that is what
        the brief's "toward the ENEMY half" has to mean here.
        """
        if self.enemy is None:
            return True
        return dsq_core(t, self.enemy) < dsq_core(ref, self.enemy)

    def _hl_has_throw(self, ct, q):
        """Bar (b): does a launcher at q have a long throw toward the enemy?

        Terrain only -- this runs at SITE time, before the launcher exists, and
        occupancy at r10 says nothing about occupancy at r400.  The FIRE rule
        re-checks passability and `can_launch` every single throw.
        """
        for dx in range(-5, 6):
            for dy in range(-5, 6):
                d = dx * dx + dy * dy
                if d < SK_HL_THROW_MIN_DSQ or d > SK_HL_THROW_MAX_DSQ:
                    continue
                t = Position(q.x + dx, q.y + dy)
                if not self.ibp(t):
                    continue
                if not self._hl_toward(t, q):
                    continue
                try:
                    if ct.get_tile_env(t) == Environment.WALL:
                        continue
                except Exception:
                    continue
                return True
        return False

    def _home_launcher_action(self, ct, p, rnd):
        """Buy THE one launcher.  True if it took the keeper's turn.

        ⛔ ONE TURN, ONCE A GAME, AND THAT IS THE WHOLE ARGUMENT FOR THE ARM.
        v610 measured the bounded aimed peck at 1,347 keeper turns for a
        confirmed mechanism and a four-point by-r300 loss; this spends ONE
        keeper turn plus a short walk and then never asks the keeper for
        anything again.  Whether that trade pays is the dose table, not a claim
        made here.
        """
        if not SK_HOME_LAUNCHER:
            return False
        if self.hl_built >= SK_HOME_LAUNCHER_MAX:
            return False
        # ⛔ THE CAP IS PER TEAM, NOT PER BODY, AND `hl_built` ALONE IS PER BODY.
        # MEASURED: skald seat B built TWO launchers because the first keeper
        # died and its successor claimed the role with a fresh counter -- 2 of
        # 25 builds across 30 games.  The store cannot carry this (v608 took the
        # last free slot), so the team-wide bound is a VISION read: a home
        # launcher sits at d^2 <= 9 of our own core and the keeper lives on that
        # doorstep, so a live one is in `vis_friend` whenever the keeper is
        # anywhere near the site.  ⚠ It is a bound, not a proof -- a keeper that
        # has wandered out of vision of an existing launcher can still buy a
        # second one, and that residual is disclosed rather than claimed away.
        for _eid, et, _ep in self.vis_friend:
            if et == EntityType.LAUNCHER:
                return False
        if rnd < SK_HL_MIN_ROUND:
            return False
        # ⭐⭐ v616 SK_HL_AFTER_S2 -- THE WAVE'S ONE ARM.  ABOVE `_hl_pick_site`
        # because the site search is the expensive half (a d^2 <= 9 tile sweep
        # with a throw-option probe per candidate) and a gate that runs AFTER it
        # pays the CPU for a build it is going to refuse.  BELOW the min-round
        # and the cap checks so the cheap constant-time refusals stay first.
        # `_two_tubes` costs one `read_store` and writes nothing.
        if SK_HL_AFTER_S2 and not self._two_tubes(ct):
            return False
        site = self._hl_pick_site(ct, rnd)
        if site is None:
            return False
        if p.distance_squared(site) != 1:
            return False                # not orthogonally adjacent: `_home_
                                        # keeper_move` walks, the action waits
        cost = ct.get_launcher_cost()
        if ct.get_global_resources() < cost + SK_HL_RESERVE:
            return False
        # ⛔ THE TWO GUARDS EVERY IMPASSABLE BUILD IN THIS TREE PAYS.  A launcher
        # is a BUILDING: it can seal this body in (ledger V2 / the (7,9) freeze)
        # and it can seal the TEAM's only lane (v605 FIX 1, the helheim throat).
        if self.free_neighbours(ct, p, exclude=site) == 0:
            self._hl_strike(rnd)
            return False
        if not self.path_arbiter_ok(ct, site, rnd):
            self._hl_strike(rnd)
            return False
        try:
            if not ct.can_build_launcher(site):
                self._hl_strike(rnd)
                return False
            ct.build_launcher(site)
        except Exception:
            self._hl_strike(rnd)
            return False
        self.hl_built += 1
        return True

    def _hl_walk_target(self, ct, p, rnd):
        """Where the keeper stands to build the launcher.  Position or None.

        THIS IS THE ARM'S ONLY RECURRING KEEPER COST and it is instrumented
        (`hl_walk_rounds`) because the brief asks for it by name.  It is bounded
        two ways: the site is inside d^2 SK_HL_SITE_DSQ of our own footprint, so
        the walk never leaves the home quadrant; and it stops the moment the
        launcher stands.
        """
        if not SK_HOME_LAUNCHER:
            return None
        if self.hl_built >= SK_HOME_LAUNCHER_MAX:
            return None
        if rnd < SK_HL_MIN_ROUND:
            return None
        # ⭐⭐ v616 SK_HL_AFTER_S2, THE WALK HALF.  Same gate, same position in
        # the ladder.  Gating the buy alone would spend keeper walk rounds from
        # r10 for a build that cannot land until the pair stands (median r68 on
        # F1, r48 on F2) -- exactly the "walking at a buy we cannot make" cost
        # the funding guard below this line already refuses to pay.
        if SK_HL_AFTER_S2 and not self._two_tubes(ct):
            return None
        site = self._hl_pick_site(ct, rnd)
        if site is None:
            return None
        if p.distance_squared(site) == 1:
            return None                 # seated; the action fires
        cost = ct.get_launcher_cost()
        if ct.get_global_resources() < cost + SK_HL_RESERVE:
            return None                 # ⛔ DO NOT WALK AT A BUY WE CANNOT MAKE.
                                        # The funding waits are 18 of 30 games;
                                        # a keeper standing beside an unaffordable
                                        # tile is the v610 cost in a new hat.
        best = None
        for d in CARDINALS:
            r = site.add(d)
            if not self.ibp(r):
                continue
            if r.x == p.x and r.y == p.y:
                return None
            try:
                if not ct.is_tile_passable(r):
                    continue
            except Exception:
                continue
            dd = p.distance_squared(r)
            if best is None or dd < best[0]:
                best = (dd, r)
        if best is None:
            self._hl_strike(rnd)
            return None
        self.hl_walk_rounds += 1
        self._hl_strike(rnd)            # ⛔ the walk is on the same clock as the
                                        # build; a site we cannot REACH is as
                                        # dead as one we cannot BUILD on
        return best[1]

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
        # ⭐ v607 ITEM 2 -- DEFER, DO NOT CUT.  Placed BELOW half (a) on purpose:
        # the melee that answers a turret already on our ring is free and stays,
        # and every gun already standing keeps firing.  Only the PURCHASE waits,
        # and only until the band pair is up or the window expires.
        if SK_S2_DEFER_GUNS and self._s2_pending(ct, rnd):
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
        if not self.path_arbiter_ok(ct, site, rnd):
            return False            # v605 FIX 1: a gunner is impassable
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
        """The live belt cover set the gun scorer is told to prefer.

        ⭐ v603 FIX 2 (SK_TRUNK_NEAR) -- THE EXCLUSION IS INVERTED, and it is the
        single largest measured channel on the tape602 autopsy.  v601 defined the
        "trunk" as our belt/harvester tiles BEYOND `SK_TRUNK_DSQ = 13` of our own
        core, on tape30's evidence that 85.7% of the belt died outside it.  On
        tape602 the killzone has MOVED HOME: 55 of 63 belt deaths (87.3%) are on
        tiles this cut EXCLUDES BY CONSTRUCTION, victim d^2 to our core has
        median 1, and 53 of 63 sit at d^2 <= 4.  The killer class moved with it --
        44 of 63 (69.8%) are THEIR BUILDER PECKING at d^2 <= 13 of our core, and
        their builder dies to two gunner shots.

        So the near half is no longer excluded, and two classes are added that
        the old set could never contain:
          * TERMINUS seats -- planned belt tiles orthogonally adjacent to our
            core footprint.  These are the delivery tiles; a harvester whose
            terminus is gone delivers nothing, and `titanium_collected` counts
            delivery.  Weight `SK_TRUNK_TERM_WEIGHT`.
          * PECKER seats -- the orthogonal neighbours of a terminus seat, i.e.
            the tiles their builder has to STAND ON to peck it.  Weight
            `SK_TRUNK_SEAT_WEIGHT`: killing the pecker is what stops the class,
            and a facing that covers seat AND stand-tile beats one that does not.

        ⛔ SK_TRUNK_NEAR = False is the ablation identity and reproduces the v601
        set exactly (the `continue`s below), so the flag maps onto one signature:
        the share of live gunner rays that cover the near trunk.
        """
        if self.core is None:
            return {}
        near = SK_TRUNK_NEAR
        out = {}
        for xy in self.belt_built:
            if not near and dsq_core(Position(xy[0], xy[1]), self.core) <= SK_TRUNK_DSQ:
                continue
            out[xy] = 1 + 2 * min(self.belt_rebuilds.get(xy, 1) - 1, 2)
        for xy in self.harv_tiles:
            if not near and dsq_core(Position(xy[0], xy[1]), self.core) <= SK_TRUNK_DSQ:
                continue
            out[xy] = 1 + 2 * min(self.harv_deaths.get(xy, 0), 2)
        for xy in self.harv_deaths:
            if xy in out:
                continue
            if not near and dsq_core(Position(xy[0], xy[1]), self.core) <= SK_TRUNK_DSQ:
                continue
            # A tile that keeps losing harvesters is exactly where the answer
            # belongs, whether or not one stands there this round.
            out[xy] = 1 + 2 * min(self.harv_deaths[xy], 2)
        if not near:
            return out
        for xy in self._terminus_tiles():
            w = out.get(xy, 0) + SK_TRUNK_TERM_WEIGHT
            out[xy] = w
            for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                q = (xy[0] + dx, xy[1] + dy)
                if not self.ib(q[0], q[1]) or q in out:
                    continue
                if adjacent_to_core(Position(q[0], q[1]), self.core):
                    continue        # another seat; it gets its own weight above
                out[q] = SK_TRUNK_SEAT_WEIGHT
        return out

    def _terminus_tiles(self):
        """v603 FIX 2 -- the DELIVERY SEATS: tiles orthogonally adjacent to our
        core footprint that the belt plan actually terminates on, plus any we
        have already built on.  These are the eight tiles their collar contests
        (median 6.5 of 8 enemy-held at end of game, >= 4 of 8 in 26 of 30 games,
        first enemy building there at median r11).
        """
        if self.core is None:
            return ()
        out = []
        for xy in self.belt_plan:
            if adjacent_to_core(Position(xy[0], xy[1]), self.core):
                out.append(xy)
        for xy in self.belt_built:
            if xy in out:
                continue
            if adjacent_to_core(Position(xy[0], xy[1]), self.core):
                out.append(xy)
        return tuple(out)

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
        # ⭐ v607 ITEM 2: the SECOND door-gunner buyer, and it spends from the
        # same cap, so deferring only `_door_action` would leave the purchase
        # class half-deferred and the arm unreadable.
        if SK_S2_DEFER_GUNS and self._s2_pending(ct, rnd):
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
        # ⭐ v603 FIX 2, DISCLOSED EXTENSION OF THE TRIGGER.  The evidence terms
        # above are all POSTHUMOUS -- they need a belt piece to have died first.
        # The tape says the collar lands on our delivery ring at median r11 and
        # reaches 4 of 8 by median r18 (29/30 games), and 100% of their entire
        # peck budget lands on our conveyors at our own core.  Waiting for the
        # first corpse buys the gun a ring too late as well as a ring too far
        # out; an enemy BUILDING on our own delivery ring IS the belt-killer
        # class arriving.  SK_TRUNK_NEAR = False restores the posthumous form.
        if not hurt and SK_TRUNK_NEAR:
            for _eid, _et, ep in self.vis_enemy:
                if dsq_core(ep, self.core) <= SK_HOME_RING_DSQ:
                    hurt = True
                    break
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
        if not self.path_arbiter_ok(ct, site, rnd):
            return False            # v605 FIX 1: a gunner is impassable
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
        # ⭐ v608 PLANK 1, THE POSITIONING HALF -- and without it the ordering
        # half is unreachable.  `_core_medic` needs this body to be orthogonally
        # adjacent to the footprint, and the keeper is on a belt tile when the
        # shooting starts.  A seated keeper HOLDS STATION (returns without
        # moving) for as long as the alarm is fresh; SK_COREFIRE_TTL is what
        # bounds that, and it is the plank's whole cost.
        seat = self._medic_seat(ct, p, rnd)
        if seat is not None:
            if seat.x != p.x or seat.y != p.y:
                self.step_to(ct, seat)
            return
        shooter = self._escalate_target(ct, p)
        if shooter is not None:
            self.step_to(ct, shooter)
            return
        self._plan_belt(ct)
        # ⭐ v610 PLANK 1, THE MOVEMENT HALF.  It sits BELOW `_medic_seat` and
        # the escalated shooter on purpose -- the v609 HP gate owns the keeper
        # while the core is under fire, and a seat is worth nothing to a dead
        # core.  It sits ABOVE the belt walk because a seat that an enemy holds
        # is not reachable by the belt walk at all: the walk targets UNBUILT
        # PLANNED tiles, and seven of our eight seats are never in the plan.
        seat = self._seat_walk(ct, p, rnd)
        if seat is not None:
            self.step_to(ct, seat)
            return
        # ⭐ v613 PLANK 1, THE MOVEMENT HALF.  Same placement argument as the
        # v610 seat walk it sits beside: below the medic seat and the escalated
        # shooter (a core under fire owns this body), above the belt walk
        # (the belt walk targets UNBUILT PLANNED tiles and an apron tile that
        # just lost its occupant is not one of them until the plan re-keys).
        apron = self._apron_walk(ct, p, rnd)
        if apron is not None:
            self.step_to(ct, apron)
            return
        # ⭐ v618 PLANK 4, THE MOVEMENT HALF -- ONE STEP.  Above the claim and
        # the gun because a seat we ALREADY hold and are ABOUT TO LOSE outranks
        # a seat we have not taken and a turret that is not yet bought; below
        # the medic seat and the escalated shooter for the reason every home
        # walk in this tree is: a core under fire owns this body.
        hseat = self._seat_heal_walk(ct, p, rnd)
        if hseat is not None:
            self.step_to(ct, hseat)
            return
        # ⭐ v618 PLANK 1, THE MOVEMENT HALF.  Fenced at
        # SK_SEAT_CLAIM_WALK_DSQ and silent after SK_SEAT_CLAIM_UNTIL, so it is
        # a bounded early detour rather than a standing duty -- the v610 finding
        # ("the keeper's turn is the scarce resource") written into the walk
        # rather than only into the action.
        cseat = self._seat_claim_walk(ct, p, rnd)
        if cseat is not None:
            self.step_to(ct, cseat)
            return
        # ⭐ v618 PLANK 2, THE MOVEMENT HALF.  Gated on the SAME window and the
        # SAME affordability as the buy -- the launcher arm's own lesson, that a
        # keeper standing beside a buy it cannot make is the v610 cost in a new
        # hat.  Terminates permanently once the gun stands.
        gsite = self._home_gun_walk(ct, p, rnd)
        if gsite is not None:
            self.step_to(ct, gsite)
            return
        # ⭐ v611 SK_HOME_LAUNCHER, THE MOVEMENT HALF (OFF by default).  Below
        # `_medic_seat`, the escalated shooter and the seat walk -- a core under
        # fire owns this body and always will.  Above the belt walk because the
        # walk is short, bounded and terminates permanently once the launcher
        # stands, where the belt walk is the keeper's whole standing job.
        # ⛔ IT IS ALSO THE ARM'S ONLY RECURRING COST and it is counted.
        hl = self._hl_walk_target(ct, p, rnd)
        if hl is not None:
            self.step_to(ct, hl)
            return
        tgt = None
        best = None
        # ⭐ v610 PLANK 2, THE MOVEMENT HALF.  Prefer a tile that COMPLETES a
        # chain over the nearest unbuilt planned tile.  `_route_gaps` is
        # already computed and memoised for this round; until v610 its only
        # consumer was a flag shipped OFF, so the set was thrown away.
        if SK_TERMINATE and SK_TERM_MOVE:
            for (x, y) in self._route_gaps(ct, rnd):
                if (x, y) in self.belt_escalated or (x, y) in self.belt_built:
                    continue
                if x == p.x and y == p.y:
                    continue
                q = Position(x, y)
                d = p.distance_squared(q)
                if best is None or d < best:
                    best = d
                    tgt = q
        if tgt is not None:
            self.step_to(ct, tgt)
            return
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

    # ------------------------------------------------------------------
    # v604 FIX 4 -- THE BELT ESTIMATOR (SK_BELT_EST)
    # ------------------------------------------------------------------

    def _belt_seed_store(self, ct, rnd):
        """FIX 4(c) -- adopt the eight TERMINUS seats from slot 5 b24-31.

        ⛔ THE DEFECT.  `belt_built` was a record of THIS BODY'S OWN BUILDS, and
        module state is not shared between units (design build rule 6), so the
        instant the keeper died its replacement believed the entire belt was
        unbuilt.  Every chain then read as many-gapped -- which is precisely when
        `_route_gaps` refuses, and the v603 report named that as the root cause
        of SK_COLLAR_ROUTE_GATE's measured negative (bifrost A 2,470 -> 400 Ti).
        A ledger that dies with the body is not a world model.

        The store is the only channel between bodies, and slot 5 has eight free
        bits, so what crosses is the eight seats whose index is canonical
        (`core_seats`).  Everything else is re-derived by vision in
        `_belt_watch`.  ⚠ DISCLOSED DEVIATION from the brief's "bits per planned
        tile": a plan index is not body-independent, so bits keyed on it would be
        worse than no bits at all.
        """
        if not SK_BELT_EST or self.core is None:
            return
        try:
            word = ct.read_store(SK_SLOT_BELT)
        except Exception:
            return
        bits = (word >> BELT_TERM_FIELD) & BELT_TERM_MASK
        self.belt_term_bits = bits
        if not bits:
            return
        seats = core_seats(self.core)
        for i in range(8):
            if not (bits >> i) & 1:
                continue
            xy = seats[i]
            if not self.ib(xy[0], xy[1]) or xy in self.belt_built:
                continue
            if xy not in self.belt_plan:
                continue        # not on OUR plan: nothing for the gap walk to do
            self.belt_built.add(xy)
            self.belt_seen[xy] = rnd
            self.belt_est_store += 1

    def _belt_seat_bits(self, ct):
        """FIX 4(c) -- the eight terminus seats as a bitmask, for slot 5.

        A seat OUT OF VISION keeps its previous bit: the store is a memory, and
        replacing an unobserved 1 with a 0 every time the keeper walks away would
        make the word oscillate with the keeper's position rather than with the
        board.  That is the same reason `cage_enemy` is remembered rather than
        re-sensed (v603 FIX 5).
        """
        if self.core is None:
            return 0
        bits = self.belt_term_bits
        for i, xy in enumerate(core_seats(self.core)):
            if not self.ib(xy[0], xy[1]):
                bits &= ~(1 << i)
                continue
            q = Position(xy[0], xy[1])
            try:
                if not ct.is_in_vision(q):
                    continue
                bid = ct.get_tile_building_id(q)
                ours = (bid is not None
                        and ct.get_team(bid) == self.team
                        and ct.get_entity_type(bid) in BELT_TYPES)
            except Exception:
                continue
            if ours:
                bits |= (1 << i)
            else:
                bits &= ~(1 << i)
        self.belt_term_bits = bits & BELT_TERM_MASK
        return self.belt_term_bits

    def belt_stale(self, xy, rnd):
        """FIX 4(b) -- is our PRESENT belief about this tile older than the TTL?

        Reported by the instrument and consulted by `_route_gaps`.  A stale tile
        counts as BUILT while SK_BELT_EST_STALE_BUILT holds; the flag exists
        because that is a judgement about which way to be wrong, and the whole
        point of this fix is that being wrong in the MISSING direction is what
        breaks the gate.
        """
        if not SK_BELT_EST:
            return False
        seen = self.belt_seen.get(xy)
        return seen is None or (rnd - seen) > SK_BELT_EST_TTL

    def _belt_watch(self, ct, p):
        """Keep `belt_built` honest: a planned tile we can SEE to be empty is
        no longer built.

        ⭐ v604 FIX 4(a) MAKES THIS SYMMETRIC.  v603 only ever REMOVED here, so
        the set could shrink toward the truth but never grow toward it, and a
        body that had laid nothing could learn nothing by looking.  A planned
        tile seen to carry a FRIENDLY conveyor or splitter is now adopted, with
        the observation round recorded -- so a replacement keeper re-derives the
        chain simply by walking the trunk, which is what it does anyway.
        """
        rnd = ct.get_current_round()
        if SK_BELT_EST:
            for xy in self.belt_plan:
                if xy in self.belt_built:
                    continue
                q = Position(xy[0], xy[1])
                if not self.ibp(q) or p.distance_squared(q) > 20:
                    continue
                try:
                    if not ct.is_in_vision(q):
                        continue
                    bid = ct.get_tile_building_id(q)
                    if bid is None:
                        continue
                    if ct.get_team(bid) != self.team:
                        continue
                    if ct.get_entity_type(bid) not in BELT_TYPES:
                        continue
                except Exception:
                    continue
                self.belt_built.add(xy)
                self.belt_seen[xy] = rnd
                self.belt_est_adopted += 1
        if SK_BELT_EST and not SK_BELT_EST_STALE_BUILT:
            # FIX 4(b), THE DECAY ARM.  A belief older than the TTL is dropped
            # back to unknown.  Shipped OFF (SK_BELT_EST_STALE_BUILT = True)
            # because unknown reads as MISSING in `_route_gaps` and missing is
            # the direction that breaks the gate -- this branch exists so that
            # claim can be ablated rather than asserted.
            for xy in list(self.belt_built):
                if self.belt_stale(xy, rnd):
                    self.belt_built.discard(xy)
                    self.belt_seen.pop(xy, None)
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
                    self.belt_seen.pop(xy, None)        # v604 FIX 4(b)
                elif SK_BELT_EST:
                    self.belt_seen[xy] = rnd            # v604 FIX 4(b): refresh
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
        if SK_BELT_EST:
            # v604 FIX 4(c): the eight terminus seats, b24-31.  ONE WRITER is
            # preserved -- this method is the keeper's and only the keeper's.
            word |= (self._belt_seat_bits(ct) & BELT_TERM_MASK) << BELT_TERM_FIELD
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
        # ⭐ v608 PLANK 2, THE CHEAP HALF.  SK_TARGET_PRIO already ranks a MARKED
        # armed building above an unmarked one (SK_PRI_MARKED 5 > SK_PRI_TURRET
        # 4) for BOTH turret fire and builder pecks -- it just never knew which
        # building was shooting the core.  Naming it here costs one store read
        # and makes every body that happens to be adjacent, and every gun that
        # can bear, prefer it.  The march (`_counter_march`) is the reach half.
        if SK_COUNTER_PECK:
            c = self.corefire_shooter(ct)
            if c is not None:
                out.add((c.x, c.y))
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

        ⛔ v602 FIX 4 -- PLAIN BUGFIX, NO FLAG.  v601 tested adjacency to the
        SINGLE TILE passed in, and the enemy CORE is a 2x2 ENTITY: a heal
        landing on any one of its four tiles heals the whole core, so a healer
        standing beside a DIFFERENT core tile was invisible to the guard.
        Measured on glacierkeep v601A r25-95 (autopsy §1.8): 95 enemy heals onto
        the core footprint from two builders, NEITHER of them orthogonally
        adjacent to the tile our walker was pecking, +6..+8 HP a round against
        our +2, and the core recovered 248 -> 500 HP.  The walker spent 41
        rounds losing exactly the race this guard exists to avoid.
        """
        tiles = (q,)
        try:
            bid = ct.get_tile_building_id(q)
            if bid is not None and ct.get_entity_type(bid) == EntityType.CORE:
                # get_position of a CORE returns its 2x2 ANCHOR.
                tiles = tuple(core_tiles(ct.get_position(bid)))
        except Exception:
            tiles = (q,)
        for t in tiles:
            for d in CARDINALS:
                r = t.add(d)
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

    def _peck_priority(self, ct, p, rnd, skip_core=False):
        """Peck the highest-class adjacent enemy.  True if it took the turn.

        ⭐ v602 FIX 1's second half: `skip_core` strikes the enemy CORE off the
        ladder for this call.  The CAGE WALKER passes it while seal tiles remain
        open -- the core is orthogonally adjacent to EVERY seal tile by
        construction, so leaving it on the ladder made a parked walker's peck
        the highest-scoring thing available on every single lap tile, forever.
        It is the DOORWAVE lesson in a second costume: 2 damage a round into a
        target being healed +6..+8 is not a race, and the core recovered to full
        HP while our walker spent 41 rounds on it.

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
            if skip_core and et == EntityType.CORE:
                continue                    # v602 FIX 1: not while the cage is open
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
        sealed, empty_seals, belt_seats = self._cage_survey(ct, lap)
        self._cage_report(ct, rnd, sealed)
        # v604 FIX 2, run BEFORE any targeting so `self.tgt` still holds last
        # round's objective.  Independent of SK_ONE_CURSOR by design.
        self._cycle_commit(rnd)

        if not SK_CAGE:
            self._attack_enemy_core(ct, p, rnd)
            return

        # V9: the stall branch flips the lap to the band's far quadrant.
        branch = (ct.read_store(SK_SLOT_STALL) & STALL_BRANCH_BIT) != 0

        # ⭐ v603 FIX 5 (SK_CAGE_CEIL) -- THE ACCEPT BAR IS THE MEASURED CEILING.
        # `SK_CAGE_ACCEPT = 7` is unreachable whenever their delivery belt holds
        # a seat, which is 30 of 30 games (contested seats median 3 of 8), so
        # every post-seal behaviour behind this line was DEAD CODE all tape --
        # including the walker's only damage channel.  The bar is now
        # 8 - (their belt seats), capped at 7 and floored at SK_CAGE_ACCEPT_MIN
        # so a ring they own six seats of is never declared complete.
        # ⛔ THE v602 RULE STANDS: the core stays OFF the peck ladder while seal
        # work remains.  It is not re-admitted by lowering the bar -- it is
        # re-admitted when the bar is MET, i.e. when every seat that is not
        # structurally theirs is ours and there is no empty seat left to build.
        accept = SK_CAGE_ACCEPT
        if SK_CAGE_CEIL:
            accept = 8 - belt_seats
            if accept > SK_CAGE_ACCEPT:
                accept = SK_CAGE_ACCEPT
            if accept < SK_CAGE_ACCEPT_MIN:
                accept = SK_CAGE_ACCEPT_MIN
        if sealed >= accept and not (SK_CAGE_CEIL and empty_seals):
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
            # ⭐ v603 FIX 6(a): then ANY adjacent empty seal seat but the one
            # ahead.  See SK_LAP_ADJ_SEAL for the two independent measurements
            # this closes (356 pooled opportunity-rounds; the midgard livelock).
            # ⛔ v604 FIX 3 RE-KEYS THE `skip`, and the reason is ledger V2 and
            # not tidiness.  The excluded seat is "the tile this body is about to
            # STAND ON", because a builder cannot stand on its own building and
            # sealing it is how the doctrine we replicate self-demolished 74% of
            # its lost ring barriers.  Under v603 that tile was `lap[here+1]` by
            # definition; under the cursor it is the cursor's target -- and ONLY
            # when the cursor is a lap advance.  A 'seal' cursor is a tile we
            # intend to build on from beside it and must NOT be skipped, which is
            # exactly the case v603 could not express.
            skip_i = (here + 1) % 12
            if SK_ONE_CURSOR:
                skip_i = self._cursor_skip_index(lap)
            if SK_LAP_ADJ_SEAL and self._seal_adjacent(ct, p, lap, rnd,
                                                      skip=skip_i):
                return
            if not SK_CAGE_FIRST:
                # ⛔ THE v601 ORDER, KEPT ONLY AS THE ABLATION IDENTITY.  v601
                # PLANK 3 put the peck here, between the seal-behind and the lap
                # advance -- and the enemy core footprint is orthogonally
                # adjacent to EVERY seal tile by construction (`cage_lap` +
                # `LAP_SEAL_IDX`), while `_target_pri` scores CORE at the top of
                # the ladder.  So from any seal tile this returned True every
                # round and the lap advance below was never reached: a builder
                # cannot act and move in the same round, so THE LAP STOPPED DEAD
                # at the first seal tile the walker stepped on.  92.6% of v601
                # walker lap actions were pecks, ring barriers/game fell 1.933 ->
                # 0.767, and one walker parked 41 consecutive rounds.
                if self._peck_priority(ct, p, rnd):
                    return
            # ⭐ v603 FIX 3 (SK_EVICT_ARMED) -- THE ONE-LINE INTERLOCK IS GONE.
            # v602 read `if not empty_seals and self._clear_tile(...)`, i.e.
            # eviction was armed ONLY in a round where NO seal tile anywhere on
            # the ring was empty.  Measured over 6,954 game-rounds: armed in
            # 7.75% of rounds and NEVER ONCE in 24 of 30 games, and the six games
            # that did arm it are exactly the six with any eviction at all -- the
            # predicate and the behaviour agree cell-for-cell.  It is also the
            # gate that made the 8 -> 5 half of the seal gap unreachable, because
            # 91 of the 137 never-attempted seal tiles carried an enemy building
            # and that census is 100% CONVEYOR (18,381 tile-rounds, zero
            # barriers): their belt must terminate adjacent to their core, so
            # those tiles are seal seats BY CONSTRUCTION and only eviction opens
            # them.  The v602 comment kept here for provenance -- it is the
            # r23 nine-round chew that motivated the gate:
            #   "without the `not empty_seals` guard the walker met one enemy
            #    conveyor on the next lap tile at r23 and chewed it for nine
            #    rounds while FOUR empty seal tiles sat unbuilt"
            # ⛔ WHAT REPLACES THE GATE, because that hazard is real: eviction
            # runs only when there is NO BUILD ACTION available this round (the
            # seal-behind above already returned if there was one), the chew is
            # still capped by SK_CAGE_MELEE_GIVEUP = 20 rounds per tile, and the
            # healing-race guard is unchanged.  Ten pecks kill a 20 HP conveyor.
            if SK_EVICT_ARMED:
                if self._evict_seal(ct, p, lap, rnd):
                    return
            else:
                fwd = (here + 1) % 12
                if not empty_seals and self._clear_tile(ct, lap[fwd], rnd):
                    return

        # ⭐⭐ v604 FIX 3 (SK_ONE_CURSOR) -- ONE TARGETING AUTHORITY.  Everything
        # from here to the end of the v603 method is MOVEMENT TARGET SELECTION,
        # and v603 ran TWO systems over it that disagree by construction:
        #   (i)  the lap skip-ahead, which walks PAST a blocked lap tile, and
        #   (ii) the off-lap nearest-empty-seal pool, which runs whenever the
        #        body is not standing on a lap tile -- i.e. EVERY round the
        #        skip-ahead's detour succeeded.
        # So (i) steps off the lap to get round an obstacle and (ii) immediately
        # steps back toward the nearest empty seat, which is the period-6-to-10
        # orbit the v603 diagnosis measured (midgard_A 41 consecutive rounds,
        # midgard_B 14).  The cursor below owns ONE objective and is advanced
        # only on COMPLETION or after SK_CURSOR_GIVEUP rounds; the empty-seal
        # pool becomes an INPUT to the choice instead of a per-round override.
        # ⛔ ACTIONS ARE UNCHANGED.  Everything above this line -- seal behind,
        # seal adjacent, eviction, the peck ladder -- still runs exactly as it
        # did; a cursor decides WHERE THE BODY WALKS, never what it does when it
        # gets there.  That is what keeps this separable from FIX 2 and from the
        # v603 fixes it sits on top of.
        if SK_ONE_CURSOR:
            self._cage_cursor_move(ct, p, lap, empty_seals, here, branch, rnd)
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
                if self.step_to(ct, step):
                    return
                break               # the nearest free lap tile, one attempt
            # ⭐ v602 FIX 1.  WE ARE HERE ONLY BECAUSE THE LAP HAD NOTHING TO
            # OFFER THIS ROUND: nothing to seal behind, nothing clearable ahead,
            # and no lap tile the body could actually step to (blocked, or the
            # move cooldown is not up).  NOW the peck is free value -- and the
            # enemy CORE stays off the ladder while seal tiles are still open,
            # because pecking a healed core is the race §1.8 measured us losing
            # 95 heals to 82 pecks.
            if (SK_CAGE_FIRST and ct.get_action_cooldown() == 0
                    and self._peck_priority(ct, p, rnd, skip_core=True)):
                return
            # ⛔ NO `return` HERE: v601 fell through to the nearest-empty-seal
            # targeting below when the lap offered no free tile, and that
            # fall-through is preserved -- the second `step_to` is a no-op once
            # a move has been spent this round (the engine gates on the move
            # cooldown), so the only cost is one extra flood on a rare branch.
        # ⭐ v602 FIX 1, DISCLOSED EXTENSION -- OFF-LAP EVICTION, and it is what
        # makes "the walker has no lap action" an honest test rather than a
        # blind spot.  MEASURED on glacierkeep seat A r362-405 with the ordering
        # fix alone: 6 of 8 seal tiles carried OUR barriers and the last two
        # carried ENEMY CONVEYORS, so `sealed`=6 never reached SK_CAGE_ACCEPT,
        # `empty_seals` was empty, the nearest pool tile was the OCCUPIED
        # (13,26), and `_bfs_direction` answers CENTRE when the target tile is
        # blocked and you already stand on one of its neighbours -- the walker
        # parked at (12,26) for the last 43 rounds of the game one step from the
        # tile it needed to clear.  `_clear_tile` was unreachable because it is
        # gated on standing ON the lap.  Same verb, same melee give-up, same
        # healing-race guard; only the reachability changes.
        # ⭐ v603 FIX 3: the SAME `not empty_seals` interlock was carried here and
        # it killed this path too -- §1.4 of the tape602 autopsy measured the
        # walker on or beside 104 of the 137 never-attempted seal tiles and
        # attacking 5 of them.  The walker REACHES THE TILE AND REFUSES.
        if here is None and ct.get_action_cooldown() == 0:
            # ⭐ v603 FIX 6(a), OFF-LAP HALF.  A body standing BESIDE the ring
            # with an empty seat next to it built nothing in v602 -- the seal
            # verb was reachable only from a lap position.  Nothing about the
            # barrier needs the builder to be on the lap.
            if SK_LAP_ADJ_SEAL and self._seal_adjacent(ct, p, lap, rnd):
                return
            if (SK_CAGE_FIRST and (SK_EVICT_ARMED or not empty_seals)
                    and self._evict_seal(ct, p, lap, rnd)):
                return

        # Not on the lap yet: COPY 9.1, take the NEAREST EMPTY ring tile first.
        # ⭐ v604 FIX 2 ON THE v603 PATH.  This re-pick IS the second targeting
        # authority; inside a commit window it is suppressed and the body keeps
        # walking at the target the orbit was undoing.  Placed here rather than
        # around the whole method because the cheap guard must be measurable with
        # SK_ONE_CURSOR OFF -- that is the arm that says whether the cursor alone
        # suffices.
        if (SK_CYCLE_K and self.commit_until > rnd
                and self.commit_tgt is not None):
            if self.step_to(ct, self.commit_tgt):
                return
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
        if self.step_to(ct, tgt if tgt is not None else self.enemy):
            return
        if not SK_CAGE_FIRST or ct.get_move_cooldown() != 0:
            return
        # ⭐ v602 FIX 1, SECOND HALF OF THE OFF-LAP CASE.  The pool target is an
        # OCCUPIED seal tile we already stand beside, so `_bfs_direction`
        # answers CENTRE (its goals are the blocked target's neighbours) and the
        # body parks.  A lap POSITION is strictly better than a parking space
        # beside one: every lap tile carries the seal / clear / advance
        # machinery.  So take the nearest lap tile this body could stand on.
        best = None
        step = None
        for q in lap:
            if not self.ibp(q) or not self._lap_free(ct, q):
                continue
            d = p.distance_squared(q)
            if best is None or d < best:
                best = d
                step = q
        if step is not None and self.step_to(ct, step):
            return
        # ⭐ v603 FIX 6(b) -- A BODY WITH NO LEGAL MOVE MUST ACT.  Two bodies on
        # the tape spent 860 and 227 rounds as paperweights, boxed by enemy
        # buildings with a full action cooldown available every single round.
        # `_peck_priority` refuses barriers by design (PLANK 3), which is right
        # everywhere except here: when NOTHING is walkable, the wall IS the path
        # the current action needs, which is `_clear_tile`'s own carve-out.
        if (SK_IDLE_ACT and ct.get_action_cooldown() == 0
                and self.free_neighbours(ct, p) == 0):
            if self._peck_priority(ct, p, rnd, skip_core=True):
                return
            self._peck_out(ct, p, rnd)

    # ------------------------------------------------------------------
    # v604 FIX 3 -- THE ONE CAGE CURSOR (SK_ONE_CURSOR)
    # ------------------------------------------------------------------

    def _cycle_commit(self, rnd):
        """v604 FIX 2 (SK_CYCLE_K) -- open a commit window on a period-k orbit.

        ⭐ THE RESPONSE IS AT THE TARGET LAYER, NOT THE STEP LAYER, and that is
        the whole content of the fix.  Every individual step of a period-6 orbit
        is the CORRECT step for the target that was current when it was taken;
        what repeats is the target.  So the guard freezes the target the body is
        already walking toward for k + SK_CYCLE_COMMIT_SLACK rounds -- strictly
        longer than the orbit -- and the competing authority cannot undo the
        detour inside that window.
        ⛔ IT COMMITS TO THE CURRENT TARGET, NEVER A FRESH PICK.  A fresh pick is
        exactly what the orbit consists of.
        ⛔ AND IT IS DELIBERATELY THE CHEAP HALF: with SK_ONE_CURSOR on there is
        only one authority and this should rarely fire.  Both flags exist so the
        tape can say whether the cursor alone suffices.
        """
        if not SK_CYCLE_K:
            return
        if self.commit_until > rnd:
            return                              # a window is already open
        k = self.period_cycle()
        # ⭐ v607 ITEM 4 -- THE SECOND DETECTOR, SAME RESPONSE.  Order matters:
        # the period detector answers FIRST because when it fires it knows the
        # actual period and can size the window to it; net displacement only
        # knows "this body has not gone anywhere", so it takes the measured
        # worst case (period 12 on the diagnosed cell) plus the same slack.
        # ⛔ IT REACHES WHAT THE CONSTANT-TARGET ORBITS ARE, AND NO FURTHER: the
        # v606 report measured 34.6% of orbit-rounds on the diagnosed cells as
        # a SINGLE unchanging target, and freezing a target that never moved is
        # a no-op by construction.  This item is aimed at the other 65%.
        stalled = False
        if not k and SK_STALL_NETDISP and self.netdisp_stall():
            k = SK_STALL_COMMIT - SK_CYCLE_COMMIT_SLACK
            stalled = True
        if not k:
            return
        self.cycle_k = k
        if stalled:
            self.stall_netdisp += 1
        # `self.tgt` is last round's movement target -- literally "what this body
        # is already walking toward" -- because `_cycle_commit` runs before this
        # round's targeting.  That is the quantity the fix is defined on.
        if self.tgt is None:
            return
        self.commit_tgt = self.tgt
        self.commit_until = rnd + k + SK_CYCLE_COMMIT_SLACK

    def _cursor_skip_index(self, lap):
        """The lap index `_seal_adjacent` must not seal, or None.

        Only a LAP-ADVANCE cursor names a tile we are going to stand on; a seal
        cursor names a tile we are going to build on from beside it.
        """
        if self.cursor_kind != "lap" or self.cursor_tile is None:
            return None
        for i in LAP_SEAL_IDX:
            q = lap[i]
            if q.x == self.cursor_tile[0] and q.y == self.cursor_tile[1]:
                return i
        return None

    def _cursor_done(self, ct, p, q, kind):
        """Has the current objective been met?  UNSEEN IS NEVER DONE -- a tile
        we cannot see has not been observed to change, and treating "no
        information" as completion is how a cursor becomes a re-pick every round,
        which is the thing this fix exists to stop.
        """
        if kind == "lap":
            return p.x == q.x and p.y == q.y
        try:
            if not ct.is_in_vision(q):
                return False
            if ct.get_tile_env(q) == Environment.WALL:
                return True             # never buildable, never walkable
            bid = ct.get_tile_building_id(q)
        except Exception:
            return False
        if kind == "seal":
            return bid is not None      # sealed by us, or taken; either way done
        if kind == "evict":
            if bid is None:
                return True
            try:
                return ct.get_team(bid) == self.team
            except Exception:
                return False
        return True

    def _cursor_target(self, ct, p, lap, empty_seals, branch, rnd):
        """The ONE movement objective, as a Position (or None).

        Order of authority, highest first:
          1. an OPEN COMMIT WINDOW (v604 FIX 2) -- a detected period-k orbit
             freezes the target for k + SK_CYCLE_COMMIT_SLACK rounds;
          2. the standing cursor, unless it is complete or has aged out;
          3. a fresh pick: nearest EMPTY seal seat (COPY 9.1's own rule), else
             an enemy-held seal seat to evict, else a lap advance.
        """
        if (SK_CYCLE_K and self.commit_until > rnd
                and self.commit_tgt is not None):
            return self.commit_tgt

        if self.cursor_tile is not None:
            q = Position(self.cursor_tile[0], self.cursor_tile[1])
            if self._cursor_done(ct, p, q, self.cursor_kind):
                self.cursor_kind = None
                self.cursor_tile = None
            elif rnd - self.cursor_since >= SK_CURSOR_GIVEUP:
                # ⛔ THE GIVE-UP BANS THE TILE FOR THIS BODY, which is ledger V1's
                # shape and the same rule the belt planner uses: a cursor that
                # simply expired and could be re-picked next round is not a
                # give-up at all, it is a one-round pause in the same livelock.
                self.cursor_ban.add(self.cursor_tile)
                self.cursor_kind = None
                self.cursor_tile = None
            else:
                return q

        pool = [q for q in empty_seals if (q.x, q.y) not in self.cursor_ban]
        if branch and len(pool) > 1:
            pool = list(reversed(pool))         # V9's far-quadrant stall branch
        kind = "seal"
        if not pool and SK_EVICT_ARMED:
            kind = "evict"
            pool = [Position(x, y) for (x, y) in sorted(self.cage_enemy)
                    if (x, y) not in self.cursor_ban]
        if not pool:
            kind = "lap"
            pool = [q for q in lap
                    if self.ibp(q) and self._lap_free(ct, q)
                    and (q.x, q.y) not in self.cursor_ban
                    and not (q.x == p.x and q.y == p.y)]
        best = None
        tgt = None
        for q in pool:
            if not self.ibp(q):
                continue
            d = p.distance_squared(q)
            if best is None or d < best:
                best = d
                tgt = q
        if tgt is None:
            self.cursor_kind = None
            self.cursor_tile = None
            return self.enemy
        self.cursor_kind = kind
        self.cursor_tile = (tgt.x, tgt.y)
        self.cursor_since = rnd
        return tgt

    def _cage_cursor_move(self, ct, p, lap, empty_seals, here, branch, rnd):
        """v604 FIX 3's movement stage, plus v604 FIX 2's commit window.

        ⭐ FIX 2 LIVES HERE AND NOT IN `_nav` ON PURPOSE.  A period-6 orbit is
        not a stepping fault -- every individual step in it is the correct step
        for the target that was current when it was taken.  The fault is that
        the target changed.  So the response is at the TARGET layer: freeze it.
        """
        tgt = self._cursor_target(ct, p, lap, empty_seals, branch, rnd)
        if tgt is not None and self.step_to(ct, tgt):
            return
        # No move happened.  v602 FIX 1's rule is unchanged: the peck is free
        # value ONLY when the lap had nothing to offer, and the enemy core stays
        # off the ladder while seal tiles are open.
        if (SK_CAGE_FIRST and ct.get_action_cooldown() == 0
                and self._peck_priority(ct, p, rnd, skip_core=True)):
            return
        if (SK_IDLE_ACT and ct.get_action_cooldown() == 0
                and self.free_neighbours(ct, p) == 0):
            if self._peck_priority(ct, p, rnd, skip_core=True):
                return
            self._peck_out(ct, p, rnd)

    def _peck_out(self, ct, p, rnd):
        """v603 FIX 6(b) -- the boxed-in body's last resort: peck ANY adjacent
        enemy building, barrier included, cheapest (lowest HP) first so the wall
        opens as early as possible.  Guarded by the same V7 give-up and healing
        race every other peck site uses.
        """
        if ct.get_global_resources() < 2:
            return False
        best = None
        best_q = None
        best_id = None
        for d in CARDINALS:
            q = p.add(d)
            if not self.ibp(q):
                continue
            try:
                bid = ct.get_tile_building_id(q)
                if bid is None or ct.get_team(bid) == self.team:
                    continue
                if ct.get_entity_type(bid) == EntityType.CORE:
                    continue            # the core is not a door
                hp = ct.get_hp(bid)
            except Exception:
                continue
            if self.gave_up(bid, rnd) or self._enemy_builder_adjacent(ct, q):
                continue
            if best is None or hp < best:
                best = hp
                best_q = q
                best_id = bid
        if best_q is None:
            return False
        if not self.hp_trend_ok(ct, best_id, rnd):
            return False
        try:
            if ct.can_fire(best_q):
                ct.fire(best_q)
                return True
        except Exception:
            return False
        return False

    def _seal_adjacent(self, ct, p, lap, rnd, skip=None):
        """v603 FIX 6(a) -- barrier ANY orthogonally adjacent EMPTY seal seat.

        `skip` is the lap index of the tile the walker is about to step onto;
        sealing that one is how ledger V2's 74% self-demolition happens, so it is
        excluded rather than merely deprioritised.  Nearest-first is meaningless
        for a set of tiles all at distance 1, so the order is the lap's own,
        which keeps the behaviour deterministic and reviewable.
        """
        for i in LAP_SEAL_IDX:
            if skip is not None and i == skip:
                continue
            q = lap[i]
            if not self.ibp(q):
                continue
            if abs(q.x - p.x) + abs(q.y - p.y) != 1:
                continue
            try:
                if ct.get_tile_building_id(q) is not None:
                    continue
            except Exception:
                continue
            if self._seal_tile(ct, q, rnd):
                return True
        return False

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
        """(sealed count, EMPTY seal tiles, enemy DELIVERY-BELT seats) as seen.

        The third term is v603 FIX 5's ceiling input.  Their belt has to
        terminate orthogonally adjacent to their own core, so every seat it
        occupies is a seat we cannot build on -- measured contested seats median
        3 of 8, i.e. a structural ceiling of 5.  `sealed >= 7` was therefore
        FALSE in 30 of 30 games and everything gated behind it was dead code.
        """
        sealed = 0
        empties = []
        belt_seats = 0
        for i in LAP_SEAL_IDX:
            q = lap[i]
            if not self.ibp(q):
                sealed += 1                     # off-map faces cannot be walked
                continue
            try:
                if not ct.is_in_vision(q):
                    if (q.x, q.y) in self.cage_sealed:
                        sealed += 1
                    elif (q.x, q.y) in self.cage_enemy:
                        belt_seats += 1
                    continue
                env = ct.get_tile_env(q)
                if env == Environment.WALL:
                    sealed += 1
                    self.cage_sealed.add((q.x, q.y))
                    self.cage_enemy.discard((q.x, q.y))
                    continue
                bid = ct.get_tile_building_id(q)
            except Exception:
                continue
            if bid is None:
                empties.append(q)
                self.cage_sealed.discard((q.x, q.y))
                self.cage_enemy.discard((q.x, q.y))
                continue
            try:
                if ct.get_team(bid) == self.team:
                    sealed += 1
                    self.cage_sealed.add((q.x, q.y))
                    self.cage_enemy.discard((q.x, q.y))
                else:
                    self.cage_sealed.discard((q.x, q.y))
                    # v603 FIX 5: ONLY the delivery belt counts toward the
                    # ceiling.  A barrier or a turret of theirs on a seal seat is
                    # a thing we could remove; a conveyor is a seat their own
                    # core geometry REQUIRES, which is why the census is 100%
                    # conveyor and why the ceiling is structural.
                    if ct.get_entity_type(bid) in BELT_TYPES:
                        belt_seats += 1
                        self.cage_enemy.add((q.x, q.y))
                    else:
                        self.cage_enemy.discard((q.x, q.y))
            except Exception:
                continue
        return sealed, empties, belt_seats

    def _seal_tile(self, ct, q, rnd):
        """Barrier one ring tile.  The build happens the round AFTER the tile
        clears (mean latency 1.08 in the doctrine we replicate) because the
        clear is a melee that consumes this turn's action.
        """
        if not self.ibp(q) or not self.may_build(q, OWNER_CAGE):
            return False
        if self.free_neighbours(ct, ct.get_position(), exclude=q) == 0:
            return False                        # self-trap guard
        if not self.path_arbiter_ok(ct, q, rnd):
            # v605 FIX 1, the SAME discipline one level up: the seal is allowed
            # to shut the enemy ring (SK_CAGE_ACCEPT takes 7 of 8), it is not
            # allowed to shut the corridor that reaches it.
            return False
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

    def _evict_seal(self, ct, p, lap, rnd):
        """v603 FIX 3 -- evict the best enemy building sitting on a seal seat.

        ONE verb for both the on-lap and the off-lap case: the candidate set is
        every seal tile orthogonally adjacent to this body (from a lap position
        that is `back` and `fwd`; from off-lap it is whichever seat we stand
        beside).  It is called only when NO BUILD ACTION was available this
        round, which is what replaces v602's `not empty_seals` interlock.

        ⛔ PRIORITY: enemy DELIVERY BELT first, everything else after, TURRETS
        LAST.  The census is the reason -- 100% of the enemy buildings ever seen
        on their own ring across 18,381 tile-rounds were CONVEYORS, a conveyor is
        20 HP (exactly ten 2-damage pecks, measured: attack counts 10/10/10/10/8
        in the six games that armed eviction), and killing one both opens a seal
        seat and cuts their delivery -- glacierkeep_A held the enemy to
        `titanium_collected = 0`.  A TURRET on a seal seat is 25-40 HP with an
        answer of its own and belongs to the gun, not to a 2-damage peck.
        """
        cands = []
        for k, i in enumerate(LAP_SEAL_IDX):
            q = lap[i]
            if not self.ibp(q):
                continue
            if abs(q.x - p.x) + abs(q.y - p.y) != 1:
                continue
            if not SK_EVICT_ARMED:
                cands.append((0, k, q))         # ABLATION: plain index order
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
            if et in BELT_TYPES:
                pri = 0
            elif et in ARMED_TYPES:
                pri = 2
            else:
                pri = 1
            cands.append((pri, k, q))
        cands.sort()
        for _pri, _k, q in cands:
            if self._clear_tile(ct, q, rnd):
                return True
        return False

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
            # ⭐ v603 FIX 5, THE GUARD THAT MAKES THE RE-ADMITTED CORE PECK
            # HONEST.  This branch fired with NO healing-race check while
            # `_peck_priority` (which shares the target class) has carried one
            # since v602 FIX 4.  Their core absorbs a median heal-tax of 0.68 of
            # everything we deal, and the v602 autopsy measured 95 enemy heals
            # onto the footprint against 82 of our pecks over 41 rounds -- 2
            # damage a round into +6..+8 is not a race, it is a donation of the
            # walker's whole game.  The guard is 2x2-aware (it takes the core's
            # four tiles, not the one we point at).
            for c in core_tiles(self.enemy):
                if abs(c.x - p.x) + abs(c.y - p.y) != 1:
                    continue
                if (SK_CAGE_CEIL and SK_CORE_PECK_HEALGUARD
                        and self._enemy_builder_adjacent(ct, c)):
                    break
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
        acted = False                               # v602: scan moved to _builder
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
        # v606 ITEM 4(b): the same window binds the denier's ordinary target
        # pick -- the orbit on fimbulwinter alternates between a deny target and
        # the enemy core, so freezing only the V5 branch would leave the other
        # authority free to keep re-picking.
        if (SK_CYCLE_ALL_ROLES and SK_CYCLE_K and self.commit_until > rnd
                and self.commit_tgt is not None
                and self.step_to(ct, self.commit_tgt)):
            return
        tgt = self._deny_target(ct, p, rnd)
        self.step_to(ct, tgt if tgt is not None else self.enemy)

    def _deny_barrier(self, ct, p, rnd):
        """The barrier half.  Only ever fires on an ORE tile -- that predicate
        is the whole verb, and its absence is our measured zero.
        """
        # ⭐ v607 ITEM 2 -- THE NON-SEAL BARRIER, DEFERRED INSIDE THE S1->S2
        # WINDOW.  3 Ti is not the point; +1% on the ONE GLOBAL ADDITIVE cost
        # scale is, because it reprices the sentinel the engineer is waiting to
        # afford.  The CAGE SEAL barrier (`_seal_tile`) and the engineer's own
        # prep barriers are NOT deferred -- the seal is the kill and the prep
        # barriers are part of the purchase being waited for.
        if SK_S2_DEFER_BARRIERS and self._s2_pending(ct, rnd):
            return False
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
            if not self.path_arbiter_ok(ct, q, rnd):
                continue           # v605 FIX 1: a barrier is impassable
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

        self._nest_site_watch(ct, p, rnd)          # v602 FIX 5(b)
        # ⭐⭐ v620 PLANK 2(a) -- THE ORDERING FIX, AND THE DEFECT IS AN
        # ORDERING ONE, NOT A POLICY ONE.  `_rent_sweep` runs at the TOP of the
        # builder turn (correct: destroy costs no cooldown, so the earliest
        # sweep is the best sweep) -- which is ABOVE `_nest_watch` and
        # `_nest_site_watch`, the two methods that put an abandoned site into
        # `nest_deaths` / `nest_bad`.  So on the ONE round the engineer is still
        # standing beside the site it just gave up, that site's prep barriers
        # are not yet classifiable as spent; by the next round the body has
        # walked, and `_rent_class` only ever sees the four tiles it is standing
        # next to.  v619 measured the consequence: sweep median r119 against an
        # S2 purchase at r76.  One extra call, after the books are current,
        # from the same position, under the same arbiter and inside the same
        # per-TURN destroy cap.
        if SK_RENT_EARLY and SK_RENT_EARLY_RESITE:
            # ⛔ THE DELTA, NOT THE RETURN.  `_rent_sweep` returns the TURN's
            # running total (v620 made the cap a turn cap), so testing its
            # return would credit this call with the top-of-turn call's work.
            _before = self.rent_turn_n if self.rent_turn_rnd == rnd else 0
            if self._rent_sweep(ct, p, rnd) > _before:
                self.rent_resite += 1
        # ⭐ v603 FIX 1 (SK_NEST_PAIR) -- THE KILL LEVER.  100% of the 14,130
        # damage dealt to the enemy core across 30 games was SENTINEL fire; the
        # walker's pecks contributed ZERO, and the only variable that separated
        # a win from a loss was HOW MANY sentinels we built: 0 wins in 14 games
        # with <= 1, 6 wins in 16 with >= 2 (Fisher 2-sided p = 0.019), and a
        # good cage with one sentinel went 0 for 6.  One sentinel at 18 damage
        # on reload 2 is 9 a round against a core absorbing a median heal-tax of
        # 0.68; two clears it.  So the engineer keeps SK_NEST_PAIR_N guns
        # standing instead of one.
        # ⭐ v619 PLANK 1 -- and the ONLY change here is where the count comes
        # from.  `SK_NEST_PAIR_N` is derived from SK_NEST_N3 (3 or 2) and
        # `_nest_live()` counts the slots the flag enables, so with the flag off
        # both sides of this comparison are v618's, character for character in
        # value.
        # ⭐⭐ v620 PLANK 1 (SK_TUBE_FLOOR2) -- THE ONE CHANGE, AND IT IS WHERE
        # THE COUNT COMES FROM.  `want` restates the number the line already
        # ships; `live` stops being "tubes this body can see" and becomes "tubes
        # the TEAM says are standing" (v617's beats, +/- a birth grace).  Both
        # branches below are v619's, unchanged in text: the one that HOLDS now
        # holds on a true pair instead of on a body that happens to be looking
        # at two, and the one that BUYS now buys only into a true deficit --
        # which is the accidental replant loop closing.
        want = SK_NEST_PAIR_N if SK_NEST_PAIR else 1
        if SK_TUBE_FLOOR2 and SK_NEST_PAIR:
            want = SK_TUBE_FLOOR2_N
        live = self._floor_live(ct, rnd)
        # ⭐ v619 PLANK 3 (SK_TUBE_RELIGHT) -- THE DOWN-CLOCK.  This is the
        # instrument the plank is scored on (tube-down rounds per game) and it
        # is read off the ENGINEER'S OWN ledger, one increment per engineer
        # round spent below target after at least one tube has ever stood.
        if SK_TUBE_RELIGHT:
            if live < want and self.nest_lives:
                if self.relight_since is None:
                    self.relight_since = rnd
                    self.relight_n += 1
                self.relight_rounds += 1
            elif live >= want:
                self.relight_since = None
        if live >= want:
            # ⭐⭐ v620 PLANK 1's SECOND HALF -- AT OR ABOVE THE FLOOR, NO TUBE
            # IS BOUGHT.  That is the loop closing, and it is the whole reason
            # the honest death signal becomes shippable: v619 measured
            # SK_RELIGHT_TRUEDEATH alone at F1 by-r300 10 against a control of
            # 12, because a ledger that stopped forgetting its tubes stopped
            # replanting them and nothing raised the target in its place.
            # ⛔ THE PRE-PREP IS A SEPARATE FLAG BECAUSE IT SPENDS.  Holding is
            # free; laying two barriers on a site we do not yet need is 6 Ti and
            # +2% on the ONE GLOBAL ADDITIVE factor, paid before there is a gun
            # to protect.  It buys replacement LATENCY -- when a tube dies the
            # replacement is a walk and 30 Ti instead of a walk, two builder
            # turns and 30 Ti -- and that trade has to be priced on its own.
            if SK_TUBE_FLOOR2:
                self.floor_hold += 1
            if (SK_TUBE_FLOOR2
                    and (SK_TUBE_FLOOR2_PREPREP or SK_TUBE_FLOOR2_STAGE)
                    and self._preprep(ct, p, rnd)):
                return
            # Both guns standing: nothing to site.  Hold station beside the
            # newest one (V3 re-sites the instant either dies).
            hold = self.nest_site
            if hold is None:
                slots = [t for t in self._nest_slots() if t is not None]
                if not slots:
                    # ⛔ v620: REACHABLE ONLY UNDER THE FLOOR, AND IT WOULD HAVE
                    # BEEN A UNIT DEATH.  v619 indexed `(nest_turret2 or
                    # nest_turret)[1]` here, safe because `live` WAS the ledger
                    # and `live >= want >= 1` guaranteed a slot.  Under
                    # SK_TUBE_FLOOR2 `live` is a TEAM fact, so this body can
                    # stand at the floor with an EMPTY ledger (its tubes are
                    # another body's beats, or its own out of vision) and the
                    # subscript would raise TypeError -- an escaping exception
                    # destroys the unit permanently.  There is nothing to hold
                    # beside, so fall through to the engineer's normal job.
                    self._attack_enemy_core(ct, p, rnd)
                    return
                hold = slots[-1][1]
            self.step_to(ct, hold)
            return
        if self.nest_site is None:
            self.nest_site = self._pick_nest(ct, p, rnd)
            if self.nest_site is not None:
                # ⭐ v607 ITEM 1, THE RE-ARM HOLE ITSELF.  Every one of the five
                # clear-sites that drops `nest_site` without banning the tile
                # (`_nest_watch` on a turret death; `_plant_gun` on a success)
                # sent the engineer straight back here, and this reset restarted
                # the stuck clock -- FROM INSIDE THE ORBIT, because `_pick_nest`
                # scores the same tile again when the body has not moved.  The
                # v606 diagnosis named that defect and shipped a halved constant
                # instead; this is the trigger fix it asked for.
                # ⛔ A SITE THAT WENT INTO `nest_bad` CANNOT COME BACK, so the
                # only way `same` is True is the benign re-site path -- the ban
                # branches are correct by construction and need no exception.
                same = (SK_NEST_STUCK_FIX and self.nest_prev_site is not None
                        and self.nest_prev_site == (self.nest_site.x,
                                                    self.nest_site.y))
                if not same:
                    self.nest_best_d = None
                    self.nest_since = rnd
                    self.nest_anchor = None
                    self.nest_anchor_rnd = rnd
                # ⭐ v620 PLANK 1: if the re-site landed on the tile we
                # pre-prepped, take the credit for the barriers already there.
                self._preprep_consume(rnd)
        if self.nest_site is None:
            # ⭐ v619 PLANK 3(c) -- NO DISCRETIONARY DETOUR WHILE A TUBE IS
            # DOWN.  `_attack_enemy_core` is the engineer's fallback job and it
            # is the right one in general; while the count is below target and
            # a tube has already died, it is the wrong one, because the reason
            # siting failed is usually that this body is standing in the wrong
            # place for the band that is left.  Close on the band instead, so
            # the NEXT `_pick_nest` runs from inside it.
            if (SK_TUBE_RELIGHT and SK_RELIGHT_CLOSE
                    and self.relight_since is not None
                    and self.enemy is not None
                    and self._relight_close(ct, p)):
                return
            self._attack_enemy_core(ct, p, rnd)
            return
        site = self.nest_site
        # ⭐ v619 PLANK 3(b) -- PREP REUSE.  A re-site zeroes `nest_prepped`,
        # so a relight pays SK_NEST_PREP_BARRIERS builder turns for cover that
        # is usually already standing (the dead site's own preps, or a
        # neighbour's).  Standing ALLIED barriers inside the same disc
        # `_prep_barrier` builds into are counted instead of rebuilt.
        if (SK_TUBE_RELIGHT and SK_RELIGHT_PREP
                and self.relight_since is not None
                and self.nest_prepped < SK_NEST_PREP_BARRIERS):
            self._relight_prep_credit(ct, site)

        if ct.get_action_cooldown() == 0:
            adj = abs(site.x - p.x) + abs(site.y - p.y) == 1
            if adj:
                # ⭐ v613 PLANK 2(a), SK_TUBE_NOPREP.  Inside the S1 -> S2 window
                # ONLY -- one tube standing, the floor not met -- the two prep
                # barriers are skipped.  COPY 5's prep is priced for a gun that
                # will stand for a while; the second tube's arrival round IS the
                # measured win precondition (6 of 7 wins reach two simultaneous
                # forward turrets, median r56; 8 of 19 losses never reach two),
                # and two builder turns in front of a gun we do not have is the
                # wrong side of that trade.  A FIRST gun keeps its prep, so the
                # flag off is an exact identity everywhere else.
                skip_prep = (SK_TUBE_FLOOR and SK_TUBE_NOPREP
                             and 0 < live < want)
                if skip_prep and self.nest_prepped < SK_NEST_PREP_BARRIERS:
                    self.tube_noprep += 1
                if not skip_prep and self.nest_prepped < SK_NEST_PREP_BARRIERS:
                    if self._prep_barrier(ct, p, site, rnd):
                        return
                if self._plant_gun(ct, p, site, rnd, live, want):
                    return
        if self.step_to(ct, site):
            return
        # ⭐ v606 ITEM 4(a2) -- SK_IDLE_ACT, FOR THE ENGINEER.  The v603 clause
        # ("a body with no legal move must act") was wired into `_cage_walker`
        # twice and into NO other role, and the paths seat A diagnosis is what
        # that costs: bot 146 pinned on {(0,10),(0,11)} in a five-tile dead-end
        # for 105 turns, 37 of them with `free_neighbours == 0` and a zero action
        # cooldown.  Identical verb, identical guards; only the caller is new.
        if (SK_IDLE_ACT_ENGINEER and SK_IDLE_ACT
                and ct.get_action_cooldown() == 0
                and self.free_neighbours(ct, p) == 0):
            if self._peck_priority(ct, p, rnd, skip_core=True):
                return
            self._peck_out(ct, p, rnd)

    # ==================================================================
    # v619 PLANK 5 -- SK_RENT: rent, do not own
    # ==================================================================

    def _rent_prebuy(self, ct, rnd):
        """True on a round where a refund lands where it pays.

        THE ENGINEER, short of its tube target, with the bank inside one
        sentinel of affording the next one.  That is the round the global
        additive factor is about to be READ, and a percentage point handed back
        before the read is worth 30 x 1% of base; the same point handed back
        after it is worth nothing until the purchase after that.
        """
        if self.role != SK_SIEGE_ENGINEER:
            return False
        try:
            # ⭐ v620 PLANK 1: the pre-buy window closes on the TEAM's tube
            # count, not on this body's ledger.  `_floor_live` returns
            # `_nest_live()` with the flag off, so v619's arithmetic is
            # unchanged there.
            if self._floor_live(ct, rnd) >= (SK_NEST_PAIR_N if SK_NEST_PAIR
                                             else 1):
                return False
            cost = ct.get_sentinel_cost()
            bank = ct.get_global_resources()
        except Exception:
            return False
        return bank < cost * 2

    def _rent_class(self, ct, q, rnd):
        """Is the allied building on q SPENT?  Returns 'belt', 'prep' or None.

        ⛔ THE REFUSALS ARE THE PLANK.  Read them as the specification: a sweep
        that widened by one class would be a different (and, on this line's
        four-axis closure, a losing) experiment.
          * TYPE.  Never the core, never a harvester, never anything ARMED.
          * ARBITER.  `tile_owner(q)` must be OWNER_NONE.  That single test is
            what puts the CAGE ring, our own DOOR ring, the live NEST disc, the
            DENY ore tiles and every tile of the CURRENT belt plan structurally
            out of reach -- the load-bearing strangle is not on a list that
            could be edited, it is unreachable.
          * COVER.  Never within SK_RENT_COVER_DSQ of a live enemy turret: down
            there a 3 Ti barrier is soaking sentinel shots and its 1% is the
            cheapest cover on the board.
          * ROLE.  A belt orphan is swept only by the HOME KEEPER and an
            abandoned prep only by the SIEGE ENGINEER -- the body that owns the
            plan is the only body whose belief about it is current.  A keeper
            sweeping the engineer's cover off a stale plan is precisely the
            build/destroy thrash LEDGER V8 exists about.
          * AGE.  A belt tile must have been off-plan for SK_RENT_ORPHAN_AGE
            rounds.  Off-plan has to be a STATE; the planner re-routes, and
            demolishing on the instant is how 3 Ti and +1% get paid twice.
        """
        try:
            bid = ct.get_tile_building_id(q)
            if bid is None or ct.get_team(bid) != self.team:
                return None
            et = ct.get_entity_type(bid)
        except Exception:
            return None
        if et == EntityType.CORE or et == EntityType.HARVESTER or et in ARMED_TYPES:
            return None
        if self.tile_owner(q) != OWNER_NONE:
            return None
        for _eid, _et, ep in self.vis_enemy:
            if _et in TURRET_TYPES and ep.distance_squared(q) <= SK_RENT_COVER_DSQ:
                return None
        xy = (q.x, q.y)
        if et in BELT_TYPES:
            if self.role != SK_HOME_KEEPER or not self.belt_plan:
                return None
            if xy in self.belt_plan:
                self.rent_offplan.pop(xy, None)
                return None
            first = self.rent_offplan.get(xy)
            if first is None:
                self.rent_offplan[xy] = rnd
                return None
            # ⭐ v620 PLANK 2(b) -- THE ORPHAN CLOCK, RELAXED WHERE THE REFUND
            # HAS A BUYER.  25 rounds is right in general and it is what pushes
            # the first belt sweep past the S2 purchase: v619 measured sweep
            # median r119 against S2 at r76, and `scaleS2` did not move.  Inside
            # the pre-floor window the clock is SK_RENT_EARLY_AGE_N, which is
            # still long enough that one `_belt_watch` revision cannot open it.
            age = SK_RENT_ORPHAN_AGE
            if (SK_RENT_EARLY and SK_RENT_EARLY_AGE
                    and self._rent_early_window(ct, rnd)):
                age = SK_RENT_EARLY_AGE_N
                if rnd - first >= age and rnd - first < SK_RENT_ORPHAN_AGE:
                    self.rent_early_age += 1
            if rnd - first < age:
                return None
            return "belt"
        if et == EntityType.BARRIER:
            if self.role != SK_SIEGE_ENGINEER:
                return None
            # never the live site's cover, and never a standing tube's cover
            if (self.nest_site is not None
                    and q.distance_squared(self.nest_site) <= SK_RELIGHT_PREP_DSQ):
                return None
            for s in self._nest_taken():
                if q.distance_squared(s) <= SK_RELIGHT_PREP_DSQ:
                    return None
            for s in self.nest_bad:
                if q.distance_squared(Position(s[0], s[1])) <= SK_RELIGHT_PREP_DSQ:
                    return "prep"
            for s in self.nest_deaths:
                if q.distance_squared(Position(s[0], s[1])) <= SK_RELIGHT_PREP_DSQ:
                    return "prep"
            return None
        return None

    def _rent_sweep(self, ct, p, rnd):
        """PLANK 5 -- hand back the scale contribution of buildings we no
        longer use.  ENGINE-PROBED (`scratchpad/s54_v619/probe_destroy`):
        `destroy` costs NO action cooldown, is unlimited per turn, leaves the
        body free to build the same turn, and refunds the entity's contribution
        to the ONE GLOBAL ADDITIVE cost factor in full (183 -> 182 -> 181 on two
        barriers, 181 -> 182 on the rebuild -- the counter-case that makes those
        readings mean something).

        ⛔ THEREFORE IT RUNS ABOVE THE TURN, NOT INSIDE IT.  It consumes neither
        the action nor the move, so there is no turn to trade and no scheduler
        to write: the earliest possible sweep is the best possible sweep, and
        SK_RENT_PRE_BUY only widens the per-turn cap on the rounds where a
        refund is about to be read by a purchase.
        """
        if not SK_RENT or rnd < SK_RENT_MIN_ROUND:
            return 0
        if self.role not in (SK_HOME_KEEPER, SK_SIEGE_ENGINEER):
            return 0
        cap = SK_RENT_MAX_PER_TURN
        if SK_RENT_PRE_BUY and self._rent_prebuy(ct, rnd):
            cap += SK_RENT_MAX_PER_TURN
            self.rent_prebuy += 1
        # ⛔ v620 PLANK 2(a) MAKES THIS METHOD RE-ENTRANT WITHIN ONE TURN, so
        # the per-turn cap has to be a TURN cap and not a CALL cap.  Without
        # this the re-site sweep would silently double SK_RENT_MAX_PER_TURN --
        # a constant the S26 battery asserts and a blast radius the plank never
        # asked to widen.  With PLANK 2 off there is exactly one call per turn
        # and this arithmetic reduces to v619's local `n`.
        if self.rent_turn_rnd != rnd:
            self.rent_turn_rnd = rnd
            self.rent_turn_n = 0
        n = self.rent_turn_n
        for d in CARDINALS:
            if n >= cap:
                break
            q = p.add(d)
            if not self.ibp(q):
                continue
            cls = self._rent_class(ct, q, rnd)
            if cls is None:
                continue
            try:
                if not ct.can_destroy(q):
                    continue
                ct.destroy(q)
            except Exception:
                continue
            n += 1
            if cls == "belt":
                self.rent_belt += 1
            else:
                self.rent_prep += 1
            # keep every belief that names this tile honest
            self.belt_built.discard((q.x, q.y))
            self.belt_seen.pop((q.x, q.y), None)
            self.rent_offplan.pop((q.x, q.y), None)
        self.rent_turn_n = n
        # ⭐⭐ v620 PLANK 2(c) -- THE 1-STEP DETOUR, AND IT IS THE ONLY PART OF
        # EITHER v620 PLANK THAT SPENDS A BUILDER TURN.  Every other clause here
        # is free by the engine probe (destroy costs no cooldown and no move).
        # It runs LAST, so a sweep that could be taken from where we stand is
        # always taken instead.
        if n == 0 and SK_RENT_EARLY and SK_RENT_EARLY_STEP:
            self._rent_step(ct, p, rnd)
        return n

    def _rent_step(self, ct, p, rnd):
        """v620 PLANK 2(c).  One cardinal step onto a tile from which a DIAGONAL
        sweep candidate becomes destroyable.  Returns True if the move was made.

        ⛔ NEVER A WALK TARGET, AND THE THREE BOUNDS ARE THE ARGUMENT:
          * DIAGONAL ONLY (d^2 <= 2).  One step reaches it or nothing does; a
            candidate two cardinals away is not a detour, it is a destination,
            and the four-axis closure says we do not buy those.
          * SK_RENT_STEP_BUDGET per BODY per GAME, hard.
          * the PRE-FLOOR WINDOW only -- a refund with no purchase behind it is
            a builder move spent on nothing.
        ⛔ AND IT DOES NOT DESTROY THIS TURN.  The step is the whole action; the
        sweep happens next turn through the ordinary cardinal path, under the
        ordinary arbiter.  That keeps the verb in exactly one place.
        """
        if self.rent_steps >= SK_RENT_STEP_BUDGET:
            return False
        if not self._rent_early_window(ct, rnd):
            return False
        try:
            if ct.get_move_cooldown() != 0:
                return False
        except Exception:
            return False
        for d in DIAGONALS:
            q = p.add(d)
            if not self.ibp(q):
                continue
            if self._rent_class(ct, q, rnd) is None:
                continue
            dx, dy = d.delta()
            for cand in ((dx, 0), (0, dy)):
                sd = DELTA_DIR.get(cand)
                if sd is None:
                    continue
                try:
                    if not ct.can_move(sd):
                        continue
                    ct.move(sd)
                except Exception:
                    continue
                self.rent_steps += 1
                return True
        return False

    def _rent_early_window(self, ct, rnd):
        """v620 PLANK 2 -- is a sentinel purchase still ahead of us?

        ⛔ READ OFF THE BEATS DIRECTLY, NOT THROUGH `_floor_live`.  PLANK 2 has
        to be measurable with PLANK 1 ablated OFF, and `_floor_live` returns the
        plant ledger in that configuration -- the ledger that v619 measured at
        live = 0 on 60 of 69 purchases, i.e. a window that would never close.
        A window that cannot close is not a scope, it is a global loosening
        wearing one.
        """
        if SK_RENT_EARLY_WINDOW is False:
            return True                      # the WIDENED mutant: must degrade
        if not (SK_TEAM_TUBES and SK_NEST_PAIR):
            return True
        try:
            return (self._tube_count(ct.read_store(SK_SLOT_NEST), rnd)
                    < SK_TUBE_FLOOR2_N)
        except Exception:
            return True

    # --- v619 PLANK 3: the relight helpers -----------------------------------

    def _out_of_vision(self, ct, q):
        """True when tile q is provably outside THIS body's vision disc.

        ⛔ NOT `is_in_vision`.  That predicate is a PURE RADIUS TEST WITH NO
        BOUNDS CHECK (engine-probed s50: `is_in_vision((-1,14))` returns True on
        atoll and the next `get_tile_*` raises), so it is the wrong instrument
        anywhere near an edge -- and the band hugs the enemy core, which sits in
        a corner on most of the pool.  The radius arithmetic is done here, on
        two positions we already hold, and it cannot raise.
        Returns False on any doubt, which routes the caller to v618's
        behaviour: a guard that fails toward SPENDING TURNS, never toward
        hiding a dead tube.
        """
        try:
            return ct.get_position().distance_squared(q) > ct.get_vision_radius_sq()
        except Exception:
            return False

    def _relight_close(self, ct, p):
        """PLANK 3(c).  While a tube is down and siting has failed, close on the
        band instead of spending the turn pecking.

        ⛔ BOUNDED ON PURPOSE, AND THE BOUND IS THE HONEST PART.  It fires ONLY
        while this body is OUTSIDE the band it is trying to plant in
        (d^2 > SK_NEST_DSQ_MAX of the enemy core).  Inside the band there is
        nothing to close on -- `_pick_nest` failed for a reason walking does not
        fix -- so the v618 fallback runs unchanged and this cannot turn into a
        blanket suppression of the engineer's other job.
        Returns True only if it consumed the turn.
        """
        try:
            if dsq_core(p, self.enemy) <= SK_NEST_DSQ_MAX:
                return False
        except Exception:
            return False
        return bool(self.step_to(ct, self.enemy))

    def _relight_prep_credit(self, ct, site):
        """PLANK 3(b).  Count STANDING allied barriers as preparation already
        done for `site`.

        The disc is `SK_RELIGHT_PREP_DSQ`, copied from `_prep_barrier`'s own
        `q.distance_squared(site) > 4` test, so the credit can never count cover
        the engineer would not itself have built.  Barriers only: a conveyor or
        a turret near the site is somebody else's plank and crediting it would
        make this counter mean two different things.
        """
        n = 0
        try:
            ids = ct.get_nearby_buildings()
        except Exception:
            return
        for bid in ids:
            try:
                if ct.get_team(bid) != self.team:
                    continue
                if ct.get_entity_type(bid) != EntityType.BARRIER:
                    continue
                q = ct.get_position(bid)
            except Exception:
                continue
            if q.x == site.x and q.y == site.y:
                continue
            if q.distance_squared(site) > SK_RELIGHT_PREP_DSQ:
                continue
            n += 1
            if n >= SK_NEST_PREP_BARRIERS:
                break
        if n > self.nest_prepped:
            self.relight_prep_credit += n - self.nest_prepped
            self.nest_prepped = n

    # --- v619 PLANK 1: the tube ledger, as a LIST of a length the flag sets ---

    def _nest_slots(self):
        """The engineer's turret ledger, in plant order.

        ⛔ THE LENGTH IS THE PLANK.  With SK_NEST_N3 off this is exactly the
        two slots v618 had and `nest_turret3` is never assigned by any path, so
        every count, promotion and site-ban below reduces to v618's code on the
        same inputs.  That is what makes the flag-off tape an exact identity
        rather than an argued one.
        """
        if SK_NEST_N3:
            return (self.nest_turret, self.nest_turret2, self.nest_turret3)
        return (self.nest_turret, self.nest_turret2)

    def _nest_slot_set(self, i, v):
        if i == 0:
            self.nest_turret = v
        elif i == 1:
            self.nest_turret2 = v
        else:
            self.nest_turret3 = v

    def _nest_live(self):
        """How many band sentinels the engineer's own ledger believes stand."""
        n = 0
        for t in self._nest_slots():
            if t is not None:
                n += 1
        return n

    def _nest_taken(self):
        """v603 FIX 1 -- the sites our own standing band sentinels occupy.

        Not `nest_bad`: that set is PERMANENT (a refuted or unreachable tile),
        and a site whose gun dies must be re-sitable there later under LEDGER
        V4's death memo, not banned forever by the fact it once worked.
        """
        out = []
        for t in self._nest_slots():
            if t is not None:
                out.append(t[1])
        return out

    def _pick_nest(self, ct, p, rnd):
        """The band, with LEDGER V4's per-tile death memory applied.

        Scored: a legal firing line onto the footprint (axial or diagonal,
        since a sentinel shoots one tile wide along its facing), then d^2 as
        close to the band maximum as possible, then proximity to us.

        ⭐ v602 FIX 5(b).  v601 read `if self.map_grid is None: return None`, so
        THE SIEGE ENGINEER PLANTED NO FORWARD TURRET ON 10 OF THE 15 POOL MAPS
        -- the nest verb has been silently inert on two thirds of the pool since
        the line was founded (v601 build report, open item 1).  The gate is now
        `wall_at`, which answers from the catalogue grid when there is one and
        from live sensing otherwise, behind the same `terrain_known()` >= 8
        sensed-tiles floor the belt planner uses.  An UNSEEN tile reads as
        non-wall, so a site is a HYPOTHESIS until walked -- `_nest_site_watch`
        is the refutation half, exactly as `_belt_watch` is for the belt plan.
        """
        if self.map_grid is None and not self.terrain_known():
            return None
        # v603 FIX 1: the SECOND gun is spread, not stacked.  Two sentinels on
        # neighbouring tiles share one answering gunner's ray and one prep
        # barrier cluster, and the 15 forward sentinels that died on this tape
        # died to enemy gunner (7) and sentinel (8) -- i.e. to answers that are
        # themselves single-tile lines.  The band d^2 14-32 is wide enough.
        taken = self._nest_taken() if SK_NEST_PAIR else ()
        # ⭐ v619 PLANK 2 (SK_S2_HASTE) -- THE FOLLOW-UP PICK LEADS WITH
        # PROXIMITY.  `taken` is non-empty exactly when at least one tube
        # already stands, i.e. exactly on a FOLLOW-UP pick, so the first tube's
        # site is chosen by v618's rule unchanged and this cannot move S1.
        haste = bool(SK_S2_HASTE and taken)
        site = self._nest_scan(ct, p, rnd, taken, SK_NEST_PAIR_MIN_GAP,
                               haste=haste)
        # ⭐ v613 PLANK 2(c), SK_TUBE_GAP_RELAX.  "The band d^2 14-32 is wide
        # enough" is true on a 30x30 and NOT on a 12x12: with one tube standing,
        # an 8-d^2 spread can empty the band outright, and the engineer then
        # sites nothing at all while the anatomy's win precondition -- TWO tubes
        # standing simultaneously -- is exactly what is missing.  An unspread
        # second tube is 18 HP/round; no second tube is 9.  Retry ONLY when the
        # spread was the thing that emptied the band, so the flag off is an
        # exact identity.
        if (site is None and SK_TUBE_FLOOR and SK_TUBE_GAP_RELAX and taken
                and SK_TUBE_GAP_MIN < SK_NEST_PAIR_MIN_GAP):
            site = self._nest_scan(ct, p, rnd, taken, SK_TUBE_GAP_MIN,
                                   haste=haste)
            if site is not None:
                self.tube_gap_relax += 1
        if site is not None:
            self.nest_face = self._firing_face(site)
            self.nest_prepped = 0
        return site

    def _nest_scan(self, ct, p, rnd, taken, gap, haste=False):
        """`_pick_nest`'s band sweep, with the pair spread as a PARAMETER.

        Extracted unchanged from v612 so PLANK 2(c) can re-run it at a relaxed
        spread without a second copy of the scoring rule.

        ⭐ v619 PLANK 2 adds `haste`, which REORDERS THE SCORE AND NOTHING ELSE.
        Every filter above it -- the band (SK_NEST_DSQ_MIN..MAX), the
        point-blank ban, walls, `nest_bad`, the V4 death memo, the pair gap, the
        firing-face requirement -- is untouched, so the legal set is identical
        and only which member of it wins changes.  That is the whole reason this
        is a cheap plank: it cannot create a plant that v618 would have refused.
        """
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
                if self.wall_at(x, y):              # v602 FIX 5(b)
                    continue
                if (x, y) in self.nest_bad:         # v602: refuted / unreachable
                    continue
                if (x, y) in self.nest_deaths and rnd - self.nest_deaths[(x, y)] < SK_DEATH_MEMO_ROUNDS:
                    continue
                if taken:
                    close = False
                    for t in taken:
                        if q.distance_squared(t) < gap:
                            close = True
                            break
                    if close:
                        continue
                face = self._firing_face(q)
                if face is None:
                    continue
                # ⛔ THE TWO ORDERINGS, SIDE BY SIDE, SO THE DIFFERENCE IS ONE
                # LINE AND NOT A REWRITE.  v618: the d^2 = MAX diagonal wins,
                # then depth, then nearness.  v619 haste: NEARNESS wins, with
                # v618's two keys as the tie-breaks -- the measured S2 gap is
                # travel, and a geometry premium bought with a cross-band walk
                # is a premium on a tube that is not standing yet.
                if haste:
                    score = (-p.distance_squared(q),
                             d == SK_NEST_DSQ_MAX and abs(dx) == abs(dy), d)
                else:
                    score = (d == SK_NEST_DSQ_MAX and abs(dx) == abs(dy), d, -p.distance_squared(q))
                if best is None or score > best:
                    best = score
                    site = q
            if self._cpu_exhausted(ct):
                break
        return site

    def _nest_site_watch(self, ct, p, rnd):
        """v602 FIX 5(b), THE REFUTATION HALF -- the stuck-engineer guard.

        Two ways a site chosen from an UNCONFIRMED board can be wrong, and the
        v601 nest verb could not notice either because it never chose one:
          * the tile is a WALL that nothing had seen yet.  Vision refutes it;
            the wall goes into `map_walls` (so the flood and the belt planner
            learn it too) and the site into `nest_bad`;
          * the tile is real but UNREACHABLE.  There is no cheap reachability
            test, so this is a progress watchdog: closest approach so far, and
            a site the engineer has not closed on in SK_NEST_STUCK_ROUNDS is
            abandoned.
        ⛔ `nest_bad` IS WHAT STOPS THE RE-PICK OSCILLATING.  Without it
        `_pick_nest` scores the same tile highest again next round, forever --
        the same defect shape as ledger V8's two-owner tile.
        """
        site = self.nest_site
        if site is None:
            return
        if not self.ibp(site):
            self.nest_site = None
            self.nest_face = None
            self.nest_prepped = 0
            return
        try:
            if ct.is_in_vision(site) and ct.get_tile_env(site) == Environment.WALL:
                self.map_walls.add((site.x, site.y))
                self.nest_bad.add((site.x, site.y))
                self.nest_site = None
                self.nest_face = None
                self.nest_prepped = 0
                self.nest_best_d = None
                return
        except Exception:
            pass
        # ⭐ v607 ITEM 1 -- REMEMBER THE SITE WE ARE HOLDING.  Recorded EVERY
        # round the site is live, so that when one of the five clear-sites drops
        # it the caller can tell "the re-pick chose the same tile" from "the
        # re-pick chose a new one".  That distinction is the whole re-arm fix.
        self.nest_prev_site = (site.x, site.y)
        d = p.distance_squared(site)
        if not SK_NEST_STUCK_FIX:
            if self.nest_best_d is None or d < self.nest_best_d:
                self.nest_best_d = d
                self.nest_since = rnd
            elif rnd - self.nest_since > SK_NEST_STUCK_ROUNDS:
                self.nest_bad.add((site.x, site.y))
                self.nest_site = None
                self.nest_face = None
                self.nest_prepped = 0
                self.nest_best_d = None
            return
        # ⭐ v607 ITEM 1 -- THE RE-ARM, REWRITTEN.  The v606 guard re-armed on a
        # PER-ROUND quantity (closest approach so far) and that is wrong in both
        # directions, which is why its sweep came out non-monotone (25/40/60 ->
        # by-r300 10/9/10) and why halving the constant flipped helheim seat A
        # from a r189 win to a loss:
        #   * on a PERSISTENT ORBIT it never fires, because every re-site event
        #     (`_nest_watch` on a turret death, `_plant_gun` on a success) clears
        #     `nest_best_d` and the re-pick then re-arms the clock on the ORBIT'S
        #     OWN minimum -- from inside the orbit.  Fixed in the caller.
        #   * on a SLOW WALK it fires spuriously, because a body legitimately
        #     walking AROUND a wall records no new closest approach for tens of
        #     rounds while covering real ground.
        # The progress test is therefore NET DISPLACEMENT, not per-round motion:
        # an anchor tile plus the round it was set, re-anchored the moment the
        # body leaves a SK_NEST_STUCK_BOX box around it.  A body that has
        # travelled is walking; a body that has not is orbiting, whatever its
        # period.  Both clocks must run out together.
        # ⛔ SK_NEST_STUCK_FAR IS THE BACKSTOP AND IT IS NOT OPTIONAL.  The guard
        # was built for an UNREACHABLE site, and a body that wanders widely and
        # never closes is exactly that case with a large net displacement -- the
        # box test alone would never fire on it.  FAR keeps the v606 pre-change
        # behaviour (60 rounds of no closest-approach improvement) as an outer
        # bound, so the swept constant only ever moves the ORBIT trigger.
        if self.nest_best_d is None or d < self.nest_best_d:
            self.nest_best_d = d
            self.nest_since = rnd
            self.nest_anchor = (p.x, p.y)
            self.nest_anchor_rnd = rnd
            return
        if self.nest_anchor is None:
            self.nest_anchor = (p.x, p.y)
            self.nest_anchor_rnd = rnd
        else:
            ax, ay = self.nest_anchor
            dx = p.x - ax
            dy = p.y - ay
            if (dx if dx >= 0 else -dx) > SK_NEST_STUCK_BOX or \
               (dy if dy >= 0 else -dy) > SK_NEST_STUCK_BOX:
                self.nest_anchor = (p.x, p.y)
                self.nest_anchor_rnd = rnd
                return
        boxed = (rnd - self.nest_since > SK_NEST_STUCK_ROUNDS
                 and rnd - self.nest_anchor_rnd > SK_NEST_STUCK_ROUNDS)
        if boxed or rnd - self.nest_since > SK_NEST_STUCK_FAR:
            self.nest_bad.add((site.x, site.y))
            self.nest_site = None
            self.nest_face = None
            self.nest_prepped = 0
            self.nest_best_d = None
            self.nest_anchor = None

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

    def _prep_barrier(self, ct, p, site, rnd):
        """COPY 5's preparation: barriers 1-4 rounds before the gun, including
        inside the firing line (sentinels ignore obstacles).

        ⭐ v605 FIX 1 TAKES `rnd` FOR THE PATH ARBITER, and this is the verb the
        helheim finding indicts: two prep barriers plus the band sentinel sealed
        the map's only throat and the cage walker reached 1 of 12 lap tiles.
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
            # ⭐ v605 FIX 3 -- BOTH TILES, and `site` is the one that was missing.
            # The gun lands on `site` the round after the last prep barrier, so a
            # guard blind to it reserves an exit that is about to stop being one.
            if SK_NEST_EXIT and self.free_neighbours(ct, p, exclude=(q, site)) == 0:
                continue                        # self-trap guard
            if not SK_NEST_EXIT and self.free_neighbours(ct, p, exclude=q) == 0:
                continue                        # v604 form, for the ablation
            if not self.path_arbiter_ok(ct, q, rnd):
                continue                        # v605 FIX 1: route guard
            try:
                if not ct.can_build_barrier(q):
                    continue
                ct.build_barrier(q)
            except Exception:
                continue
            self.nest_prepped += 1
            return True
        return False

    def _preprep(self, ct, p, rnd):
        """⭐ v620 PLANK 1's SPENDING HALF -- lay the NEXT site's cover while the
        floor is met.  Returns True only if it consumed the turn.

        ⛔ IT NEVER PLANTS.  The one thing this method may not do is buy a
        turret: at or above the floor the purchase is exactly what PLANK 1
        forbids, and a pre-prep that ended in a gun would be the replant loop
        with extra steps.  It lays SK_NEST_PREP_BARRIERS barriers and stops.

        ⛔ BOUNDED THREE WAYS, because it spends before there is anything to
        protect: SK_TUBE_FLOOR2_PREPREP_MAX sites per BODY per game; the site
        must clear the same band scoring every real site clears (`_pick_nest`,
        including the V4 death memo and the path arbiter); and it is refused
        outright if it lands inside SK_NEST_PAIR_MIN_GAP of a forward turret we
        can already see -- `_pick_nest` spreads against the LEDGER's `taken`,
        and under this plank the ledger is no longer the census.
        """
        if self.preprep_site is None:
            if self.preprep_done >= SK_TUBE_FLOOR2_PREPREP_MAX:
                return False
            s = self._pick_nest(ct, p, rnd)
            if s is None:
                return False
            for _eid, _et, ep in self.vis_friend:
                if (_et in TURRET_TYPES
                        and ep.distance_squared(s) < SK_NEST_PAIR_MIN_GAP):
                    return False
            self.preprep_site = s
            self.preprep_n = 0
        site = self.preprep_site
        if SK_TUBE_FLOOR2_STAGE:
            # ⭐⭐ STAGE MODE -- WALK, BUILD NOTHING.  The refusal partition says
            # the control's engineer is SITE-limited (648 siting refusals and
            # 150 funding refusals per 67 purchases across 30 games), so the
            # thing the broken ledger was really buying is a body that is
            # ALREADY STANDING at the next band site when a tube dies.  This
            # buys that on purpose and pays nothing for it: no barrier, no gun,
            # no Ti, no contribution to the ONE GLOBAL ADDITIVE factor.
            # ⛔ IT RETURNS `step_to`'s VERDICT, so a body already ON the site
            # falls through to v619's hold rather than burning the turn.
            return bool(self.step_to(ct, site))
        if self.preprep_n >= SK_NEST_PREP_BARRIERS:
            return False                     # done: hold, exactly as v619 does
        if (ct.get_action_cooldown() == 0
                and abs(site.x - p.x) + abs(site.y - p.y) == 1):
            # ⛔ `_prep_barrier` increments `self.nest_prepped`, which belongs to
            # the LIVE site and is zeroed by `_nest_watch` on any death.  The
            # pre-prep keeps its own counter and restores the live one, so a
            # speculative barrier can never be miscounted as preparation of a
            # site the engineer is actually about to plant on.
            before = self.nest_prepped
            if self._prep_barrier(ct, p, site, rnd):
                self.nest_prepped = before
                self.preprep_n += 1
                if self.preprep_n >= SK_NEST_PREP_BARRIERS:
                    self.preprep_done += 1
                return True
            return False
        return bool(self.step_to(ct, site))

    def _preprep_consume(self, rnd):
        """v620 PLANK 1 -- a re-site that lands ON the pre-prepped tile inherits
        its barriers, which is the entire point of having laid them early.

        ⛔ UNCONDITIONAL ON SK_RELIGHT_PREP.  That flag credits STANDING cover
        the engineer did not lay; this credits cover THIS BODY laid, on THIS
        tile, and counted as it laid it.  Coupling them would make PLANK 1's
        latency saving invisible whenever v619's PLANK 3(b) is ablated off.
        """
        if not (SK_TUBE_FLOOR2 and SK_TUBE_FLOOR2_PREPREP):
            return
        s = self.preprep_site
        if s is None or self.nest_site is None:
            return
        if s.x == self.nest_site.x and s.y == self.nest_site.y:
            if self.nest_prepped < self.preprep_n:
                self.nest_prepped = min(self.preprep_n, SK_NEST_PREP_BARRIERS)
            self.preprep_used += 1
            self.preprep_site = None
            self.preprep_n = 0

    def _plant_gun(self, ct, p, site, rnd, live=0, want=1):
        """Plant one band sentinel.  `live` is how many of ours already stand.

        ⛔ v603 FIX 1 -- THE FUNDING RHYTHM STAYS THE DRIP.  There is no
        burst-bank and no hoard: the SECOND gun waits until the bank covers its
        own cost PLUS what COPY 7's `need` will ask for the round after it fires
        (10 ammo per live sentinel plus the V10 floor).  That is the drip's own
        arithmetic quoted back at the build decision, which is the only bank
        test that cannot desynchronise from it.  A first gun is unchanged, so
        SK_NEST_PAIR OFF is an exact ablation identity.
        """
        face = self.nest_face or self._firing_face(site)
        if face is None:
            self.nest_site = None
            return False
        cost = ct.get_sentinel_cost()
        if SK_NEST_PAIR and live > 0:
            # ⭐ v613 PLANK 2(b), SK_TUBE_FUND.  v603's surcharge is the DRIP'S
            # OWN ARITHMETIC quoted back at the build decision and it is right in
            # general -- but inside the S1 -> S2 window it is 30 Ti standing
            # between us and the only configuration that has ever won on this
            # opponent (`dealt - healed` = 500-512 in 7 of 7 wins, 0 in 14 of 19
            # losses; one tube's 9 HP/round loses to their heal seats, two
            # tubes' 18 does not).  Waived DOWN to one shot of cushion, never to
            # zero, and only while the floor is unmet.
            if SK_TUBE_FLOOR and SK_TUBE_FUND and live < want:
                if not self.tube_fund_waived:
                    self.tube_fund_waived = 1
                cost += SK_TUBE_FUND_AMMO
            else:
                cost += SK_AMMO_SENTINEL * (live + 1) + SK_AMMO_FLOOR
        if ct.get_global_resources() < cost:
            return False
        if not self.path_arbiter_ok(ct, site, rnd):
            # ⭐ v605 FIX 1 -- AND THE REFUSAL HAS TO MOVE THE SITE, not merely
            # skip the turn.  `_pick_nest` scores the same tile highest again
            # next round forever (the `nest_bad` note above says so in the same
            # words), so a throat site goes into the PERMANENT refutation set
            # exactly as a wall or an unreachable site does.  The expiring
            # `path_veto` memo is the CPU cache; this is the decision.
            self.nest_bad.add((site.x, site.y))
            self.nest_site = None
            self.nest_face = None
            self.nest_prepped = 0
            self.nest_best_d = None
            return False
        try:
            if not ct.can_build_sentinel(site, face):
                return False
            tid = ct.build_sentinel(site, face)
        except Exception:
            return False
        # ⭐ v619 PLANK 1: the ledger takes the FIRST EMPTY slot the flag
        # enables.  With SK_NEST_N3 off `_nest_slots()` is (turret, turret2) and
        # this is v618's if/else exactly.
        for i, t in enumerate(self._nest_slots()):
            if t is None:
                self._nest_slot_set(i, (tid, site, rnd))
                break
        self._nest_publish(ct, rnd)
        # v603 FIX 1: if a second gun is still wanted, free the siting machinery
        # NOW -- same round -- so `_pick_nest` runs next turn with `taken`
        # populated.  Prep barriers apply to both sites (COPY 5), hence the
        # counter reset; `nest_best_d` reset re-arms the v602 stuck watchdog.
        # ⭐ v620 PLANK 1: the same substitution as the turn head -- the target
        # is the floor and the count is the team's.  Inside the birth grace
        # `_floor_live` is `max(team, ledger)` and the ledger has just taken
        # this plant, so the post-plant reading can only be >= v619's.
        want = SK_NEST_PAIR_N if SK_NEST_PAIR else 1
        if SK_TUBE_FLOOR2 and SK_NEST_PAIR:
            want = SK_TUBE_FLOOR2_N
        n = self._floor_live(ct, rnd)
        if n < want:
            self.nest_site = None
            self.nest_face = None
            self.nest_prepped = 0
            self.nest_best_d = None
            # ⭐ v619 PLANK 2(a), SK_S2_HASTE_SAME_ROUND -- "chosen before
            # leaving S1's neighbourhood", made literal.  v603 freed the siting
            # machinery here and left the PICK to next turn, so the engineer
            # spends a round standing beside the gun it just built with no
            # target.  The pick is free (no action, no move) and this body is
            # standing exactly where the haste score wants to be measured from,
            # which is the one round in the game when that is true.
            # ⛔ IT CANNOT PLANT TWICE: `_plant_gun` has already returned its
            # action for this turn; this only fills `nest_site`/`nest_face`.
            if SK_S2_HASTE and SK_S2_HASTE_SAME_ROUND and not self._cpu_exhausted(ct):
                self.nest_site = self._pick_nest(ct, p, rnd)
                if self.nest_site is not None:
                    self.nest_since = rnd
                    self.nest_anchor = None
                    self.nest_anchor_rnd = rnd
        return True

    def _nest_publish(self, ct, rnd):
        """SK_SLOT_NEST (writer: SIEGE ENGINEER).  b0-9 first site, b10-20 plant
        round+1, and -- v603 FIX 1 -- b21 set / b22-26 dx+15 / b27-31 dy+15 for
        the SECOND site.

        ⛔ WHY RELATIVE.  Two `pack_tile`s are 20 bits and the absolute round is
        11, which is 31 of 32 with nothing left for a "set" bit; a relative
        offset costs 11 bits total and the two band sites are by construction
        both within d^2 32 of the same 2x2 footprint, so |dx|,|dy| <= 11 < 15
        and the field cannot clip in a legal game.  It stays a DIAGNOSTIC (no
        consumer reads slot 7) and the writer is still exactly one role.
        """
        # ⭐⭐ v617 ITEM 1.  Under SK_TEAM_TUBES the ENGINEER no longer owns the
        # whole word: b0-9 and b22-31 are the two forward-sentinel beats and
        # this method must PRESERVE them.  The engineer keeps b10-20 (the plant
        # round `_s2_pending` reads) and b21 (its own per-body pair bit, now a
        # DIAGNOSTIC with no consumer -- kept so the flag-off tape is exact and
        # so the broken and fixed producers can be compared in one replay).
        # ⛔ WHAT IT COSTS TO PRESERVE: one extra `read_store`.  Everything else
        # about the write is unchanged, including that it lives in exactly one
        # method.
        # ⭐⭐ v619 PLANK 1 -- THE ENGINEER STOPS WRITING SLOT 7 ALTOGETHER.
        # A third 10-bit seat does not fit beside b10-20 and b21 (3x10+11+1 = 42
        # > 32), so N = 3 re-lays the word as three seats and the engineer's
        # fields cease to exist.  It is a NON-WRITER then, which is also why
        # SK_TUBE_PHASES stays 3 with three seats: one residue each.
        # ⛔ WHAT IS LOST AND WHY IT IS AFFORDABLE: b10-20 (the plant round) and
        # b21 (the per-body pair bit).  Their only reader is `_s2_pending`,
        # whose FIRST LINE is `if not SK_S2_PRIORITY: return False`, and that
        # flag is False in the shipped config and in every arm of this wave.
        # The static battery asserts that dependency (S24g) rather than trusting
        # this comment -- the fifth time prose has been the thing that was
        # checked on this line is five times too many.
        if SK_TEAM_TUBES and not SK_TUBE_ENG_SLOT7:
            return
        keep = 0
        if SK_TEAM_TUBES:
            # ⛔ THE ENGINEER'S PHASE.  It owns residue SK_TUBE_PHASES-1 and
            # writes on no other round; `_nest_watch`'s reconciler below re-runs
            # this every engineer round, so a publish deferred here lands within
            # SK_TUBE_PHASES rounds instead of being lost.
            if rnd % SK_TUBE_PHASES != SK_TUBE_PHASES - 1:
                return
            try:
                cur = ct.read_store(SK_SLOT_NEST)
            except Exception:
                cur = 0
            for field in SK_TUBE_SEAT_FIELDS:
                keep |= (cur & (SK_TUBE_BEAT_MASK << field))
        first = self.nest_turret
        if first is None:
            # ⭐ v613: NOTHING STANDS, AND THAT IS A FACT WORTH PUBLISHING.  v612
            # returned here, which is why b21 could latch ON forever -- see
            # `_nest_watch`.  ⛔ THE WRITE STAYS IN THIS ONE METHOD: slot 7 has
            # exactly one writer METHOD as well as one writer ROLE, which is
            # what the S3 battery checks and what a second `wstore` call site
            # would break.
            # ⛔ v617: `0` HERE WOULD WIPE THE TUBES' OWN BEATS.  The engineer
            # clearing ITS fields must not clear THEIRS -- that is the whole
            # point of the fix, and writing a bare 0 would reintroduce the
            # defect from the other side.
            if SK_CORE_MEDIC_RIDER:
                self.wstore(ct, SK_SLOT_NEST, keep)
            return
        word = keep
        if not SK_TEAM_TUBES:
            word |= (pack_tile(first[1]) & NEST_SITE_MASK)
        word |= ((first[2] + 1) & SK_BEAT_MASK) << NEST_RND_FIELD
        second = self.nest_turret2
        if second is not None:
            dx = second[1].x - first[1].x
            dy = second[1].y - first[1].y
            if -15 <= dx <= 15 and -15 <= dy <= 15:
                word |= NEST_SITE2_BIT
                if not SK_TEAM_TUBES:
                    word |= ((dx + 15) & 0x1F) << NEST_SITE2_DX_FIELD
                    word |= ((dy + 15) & 0x1F) << NEST_SITE2_DY_FIELD
        self.wstore(ct, SK_SLOT_NEST, word)

    def _nest_watch(self, ct, rnd):
        """LEDGER V3 -- a dead forward sentinel is an IMMEDIATE re-site
        decision, not a queue item (their replacement latency: median 33-42
        rounds, p90 111, one watched 90-round hole).  LEDGER V4 -- remember
        that a tile killed what was put on it.
        """
        # ⭐ v617 ITEM 1's ONE LOOSE END, CLOSED.  Under SK_TEAM_TUBES slot 7 has
        # more than one writer, so an ENGINEER write that lands in the same
        # round as a tube's beat is the lost update the one-writer rule exists
        # to prevent.  The beats survive it (every writer is read-modify-write
        # on a disjoint field and next round re-asserts), but the engineer's
        # b10-20 is written on EVENTS ONLY, so a lost one would stay lost.  This
        # re-asserts it whenever the store disagrees with the ledger: one
        # `read_store` per engineer round, a write only on disagreement.
        # ⚠ SCOPE: b10-20's only reader is `_s2_pending`, gated by
        # SK_S2_PRIORITY, which is False in the shipped config and in every arm
        # of this wave.  This is a landmine removal, not a live fix.
        # ⛔ v619: under SK_NEST_N3 the engineer owns no slot-7 field at all, so
        # there is nothing to reconcile and the reconciler would re-read a word
        # whose b10-20 is now a SEAT BEAT.  Reading it would compare a beat
        # against a plant round and republish forever.
        if SK_TEAM_TUBES and SK_TUBE_ENG_SLOT7:
            try:
                cur = ct.read_store(SK_SLOT_NEST)
                want = (0 if self.nest_turret is None
                        else (self.nest_turret[2] + 1) & SK_BEAT_MASK)
                if ((cur >> NEST_RND_FIELD) & SK_BEAT_MASK) != want:
                    self._nest_publish(ct, rnd)
            except Exception:
                pass
        # v603 FIX 1: both slots are watched, and a death in EITHER re-arms the
        # siting machinery -- V3 says a dead forward sentinel is an immediate
        # re-site decision, and with a pair the survivor must not suppress it.
        # ⭐ v619 PLANK 1: the loop runs over the slots the flag enables and the
        # promotion becomes a COMPACTION (slot i takes i+1, the last empties).
        # For two slots that is v618's if/else on the same inputs.
        died = False
        slots = self._nest_slots()
        k = len(slots)
        # ⭐ v619 PLANK 3(a) -- THE TEAM BEAT COUNT, READ ONCE, AS THE ARBITER
        # OF WHAT AN EXCEPTION MEANS.  `get_hp(id)` raises for any entity
        # OUTSIDE THIS BODY'S VISION and the error is INDISTINGUISHABLE from a
        # destroyed id (471 of 471 probes) -- and the engineer's whole job is to
        # walk away from the tube it just planted to plant the next one.  v618
        # calls that exception a death: it bans the tile under the V4 memo,
        # feeds `_stall_check` a short lifetime, and drops the ledger count so
        # the engineer re-sites a tube that is still standing and shooting.
        # The v617 producer already answers the question properly -- each tube
        # writes its own beat -- so an exception is a death only when the TEAM
        # count has actually fallen below what the ledger holds.  SILENCE IS NOT
        # EVIDENCE.
        beats = None
        if SK_TUBE_RELIGHT and SK_RELIGHT_TRUEDEATH and SK_TEAM_TUBES and SK_NEST_PAIR:
            try:
                beats = self._tube_count(ct.read_store(SK_SLOT_NEST), rnd)
            except Exception:
                beats = None
        ledger = self._nest_live()
        for i in range(k):
            t = self._nest_slots()[i]
            if t is None:
                continue
            tid, site, born = t
            raised = False
            try:
                alive = ct.get_hp(tid) > 0
            except Exception:
                alive = False
                raised = True
            # ⛔ TWO CONDITIONS, BOTH REQUIRED, AND THE SECOND IS THE ONE THAT
            # KEEPS THIS FROM LATCHING.  (1) the read RAISED and the site is
            # OUTSIDE this body's vision, so the exception carries no
            # information; (2) the team beat count has NOT fallen below what the
            # ledger claims, i.e. no tube has actually gone quiet.  If the count
            # HAS fallen, something died and this is the entry to charge it to,
            # so the death is booked exactly as v618 would have booked it.  With
            # `beats` unavailable (store unreadable, SK_TEAM_TUBES off) the rule
            # falls back to v618's "exception means dead", which is the
            # conservative direction: it spends turns, it never hides a hole.
            if raised and beats is not None and beats >= ledger \
                    and self._out_of_vision(ct, site):
                self.relight_phantom += 1
                continue
            if alive:
                continue
            self.nest_deaths[(site.x, site.y)] = rnd        # V4
            self.nest_lives.append(rnd - born)
            ledger -= 1
            for j in range(i, k):
                self._nest_slot_set(j, self._nest_slots()[j + 1] if j + 1 < k else None)
            died = True
        if not died:
            return
        # ⭐ v613 PLANK 5's PRECONDITION, and it is a one-line correctness fix
        # that v607 DISCLOSED and declined to make ("if the SECOND gun dies
        # later, b21 stays set", `_s2_pending`).  Slot 7 was a diagnostic then;
        # PLANK 5 makes it a GATE, and a gate that latches ON forever is not a
        # gate.  Republished on every death so b21 means "the pair stands NOW".
        # Writing 0 when nothing stands is the same statement for the no-gun
        # case, and `_s2_pending` already treats word == 0 as "no first gun".
        if SK_CORE_MEDIC_RIDER:
            self._nest_publish(ct, rnd)
        self.nest_site = None                               # V3: re-site NOW
        self.nest_face = None
        self.nest_prepped = 0
        self.nest_best_d = None                             # v602: fresh watchdog

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
        # ⭐ v603 FIX 4, THE SECOND COLLAR CHANNEL.  `_threat_scan` publishes the
        # nearest enemy BUILDER, TURRET **or BARRIER** as the home threat (v602
        # residual #3), and this branch melees whatever slot 2 names -- so a
        # collar barrier at d^2 <= 5 latches the under-attack bit and parks the
        # ORE DENIER on it, pecking 2 into 30 HP for as long as it stands.  A
        # barrier does not shoot: it is not "the core under fire", and answering
        # it here is the same losing arithmetic the belt branch just gave up.
        # ⛔ WHY NOT AT THE SENSOR: the under-attack LATCH is load-bearing for
        # ledger V5 and for the keeper's own ordering, and a barrier planted on
        # our ring genuinely is news.  What changes is the ANSWER, not the alarm.
        if SK_COLLAR_GUNS and SK_HOMEDEF_SKIP_BARRIER:
            try:
                tb = ct.get_tile_building_id(threat)
                if (tb is not None
                        and ct.get_entity_type(tb) == EntityType.BARRIER):
                    return False
            except Exception:
                pass
        if ct.get_action_cooldown() == 0 and ct.get_global_resources() >= 2:
            if abs(threat.x - p.x) + abs(threat.y - p.y) == 1:
                # ⭐ v612 FIX 1b (DEFAULT OFF) -- the same missing team check as
                # FIX 1, on the OTHER latched tile.  SK_SLOT_THREAT_POS is a
                # POSITION the core published when it last saw an enemy there;
                # the write is buffered a round and the slot is never cleared,
                # so by the time this body stands next to it our own relay may
                # own the tile.  Measured: 10 of the 17 own-pecks on the v612
                # launcher-ON tape come from HERE, not from `_counter_march`.
                # ⛔ SCOPED TO THE SHOT, NOT THE MARCH, and `tb2 is None` is
                # DELIBERATELY NOT A REFUSAL: `_threat_scan` publishes enemy
                # BUILDER BOTS as well as buildings, and a body is not a
                # building -- refusing on an empty read would disable the march
                # at exactly the threat V5 exists for.  Only a building we
                # OWN is refused; everything else is v611's behaviour.
                own2 = None
                if SK_HOMEDEF_TEAMCHECK:
                    try:
                        tb2 = ct.get_tile_building_id(threat)
                        own2 = None if tb2 is None else ct.get_team(tb2)
                    except Exception:
                        own2 = None
                if own2 is not None and own2 == self.team:
                    return False
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

    # --- v617 ITEM 1: THE PRODUCER.  A FORWARD TUBE BEATS FOR ITSELF. ------

    def _tube_forward(self, ct, p):
        """Am I a FORWARD tube -- a sentinel inside the band around THEIR core?

        True / False / None, and NONE MEANS "ASK AGAIN NEXT ROUND": latching a
        transient failure as False would silently delete a tube from the census
        for the rest of the match, which is the same class of bug this whole
        item exists to fix.

        ⛔ THE PREDICATE IS THE GROUND TRUTH'S OWN, COPIED ON PURPOSE:
        `scratchpad/s54_v613/anat613.py` counts OUR sentinels with
        `dsq_foot(pos, their core) <= BAND_MAX` (32).  A producer verified
        against a column must compute that column's definition, not a cousin of
        it.
        Two sources, cheapest first:
          1. SIGHT.  A forward tube sits d^2 14-32 from their core by
             construction (`_pick_nest`) and a sentinel sees r^2=32, so it can
             normally see the core it is aimed at.
          2. SLOT 3, written by our own core at boot from map symmetry.  This
             covers the footprint edge -- the core's ANCHOR tile can sit outside
             the vision disc while its nearest footprint tile is inside the band.
        """
        try:
            if ct.get_entity_type() != EntityType.SENTINEL:
                return False
        except Exception:
            return None
        try:
            for eid in ct.get_nearby_buildings():
                try:
                    if ct.get_entity_type(eid) != EntityType.CORE:
                        continue
                    if ct.get_team(eid) == self.team:
                        continue
                    return dsq_core(p, ct.get_position(eid)) <= SK_TUBE_BAND_DSQ
                except Exception:
                    continue
        except Exception:
            pass
        try:
            e = unpack_pos(ct.read_store(SK_SLOT_ENEMY_CORE))
        except Exception:
            return None
        if e is None:
            return None            # our core has not booted; ask again
        return dsq_core(p, e) <= SK_TUBE_BAND_DSQ

    def _tube_beat(self, ct, p, rnd):
        """⭐⭐ v617 ITEM 1.  THE SENTINEL IS ITS OWN HEARTBEAT.

        There is no id-based liveness channel in this engine (`get_hp(id)`
        raises out of vision and the error is indistinguishable from a dead id,
        471/471) -- but a turret is a UNIT, so `run()` is called for it every
        round it lives and stops the round it dies.  Each forward tube claims a
        SEAT and writes an absolute round+1 into that seat's 10 bits of slot 7;
        `_two_tubes` asks whether BOTH seats beat inside SK_TUBE_STALE.

        ⛔ SEAT CLAIM AND ITS ONE RESIDUAL.  A tube claims the first seat that
        is not beating, once, and keeps it (it cannot move, so it has no reason
        to change).  The pair is planted rounds apart -- `_plant_gun` builds at
        most one turret per turn and there is one engineer -- so two tubes
        claiming in the same round is not reachable through the normal path.
        If it ever happened, BOTH would take seat 0 and `_two_tubes` would read
        1, i.e. THE FAILURE IS AN UNDERCOUNT, NEVER AN OVERCOUNT.  That is the
        direction to fail in for a gate that buys things.
        ⛔ A THIRD forward tube (a stall-branch rebuild racing a survivor) takes
        seat 0 as well and is likewise invisible rather than inflating.
        """
        if not SK_TEAM_TUBES or not SK_NEST_PAIR:
            return
        if self.tube_fwd is None:
            self.tube_fwd = self._tube_forward(ct, p)
        if not self.tube_fwd:
            return
        try:
            word = ct.read_store(SK_SLOT_NEST)
        except Exception:
            return
        if self.tube_seat is None:
            seat = 0
            for i in range(len(SK_TUBE_SEAT_FIELDS)):
                b = (word >> SK_TUBE_SEAT_FIELDS[i]) & SK_TUBE_BEAT_MASK
                if not (b and rnd - (b - 1) <= SK_TUBE_STALE):
                    seat = i
                    break
            self.tube_seat = seat
        # ⛔ THE PHASE GATE, AND IT IS THE WHOLE CORRECTNESS ARGUMENT.  Slot 7's
        # other writers are seat 1-w and the engineer; each owns a distinct
        # residue mod SK_TUBE_PHASES, so no two writers of this slot ever share
        # a round.  Without it the RMW merge silently drops the loser's field
        # EVERY round (measured: seat 0 frozen at r80 for 291 rounds).
        if rnd % SK_TUBE_PHASES != self.tube_seat:
            return
        try:
            self.beat(ct, SK_SLOT_NEST, rnd,
                      field=SK_TUBE_SEAT_FIELDS[self.tube_seat],
                      mask=SK_TUBE_BEAT_MASK)
        except Exception:
            return

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
        # ⭐⭐ v617 ITEM 1 -- AND IT HAS TO BE HERE, ABOVE EVERY EARLY RETURN.
        # `_turret` returns on a live action cooldown and on thin ammo; a
        # heartbeat that only beats on rounds the tube could also SHOOT is a
        # census of firing tubes, not of standing ones, and the column it is
        # verified against counts standing ones.
        self._tube_beat(ct, p, rnd)
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
                rb_hit = False              # v618 PLANK 3: per CANDIDATE
                if SK_TARGET_PRIO:
                    # ⭐ v601 PLANK 3.  ⛔ NOTE WHAT THIS REPLACES: v600's top
                    # class was "anything on our home ring", BARRIERS INCLUDED,
                    # which is a large part of how 618 of our 821 turret shots
                    # landed on a wall.  A barrier is scored 0 and 0 never
                    # fires -- an enemy barrier is not what is killing us, and
                    # a shot not taken is 4 or 10 ammo the drip need not buy.
                    pri = self._target_pri(et, (q.x, q.y), marked)
                    # ⭐ v610 PLANK 1, THE TURRET HALF (SK_SEAT_GUNS, OFF by
                    # default).  `_target_pri`'s docstring says a barrier is
                    # "only ever attacked by the verb whose PATH they block" --
                    # true of PECKS and with no counterpart here at all, so no
                    # gun of ours has ever fired at a seat-blocking barrier.
                    # A delivery seat the belt needs IS path-blocking, and the
                    # gun does 7 or 18 against a peck's 2.  Scored between a
                    # harvester and a body: it is economics, not the answer to
                    # something shooting us.
                    if (SK_SEAT_GUNS and pri <= SK_PRI_BARRIER
                            and et == EntityType.BARRIER
                            and self.core is not None
                            and (q.x, q.y) in set(core_seats(self.core))):
                        pri = SK_PRI_HARVESTER
                    # ⭐⭐ v618 PLANK 3 -- SK_GUN_ROUTEBLOCK.  The same class as
                    # SK_SEAT_GUNS above and the difference is the RANK: this
                    # scores at SK_ROUTEBLOCK_PRI = SK_PRI_OTHER = 1, i.e.
                    # ABOVE IDLE and BELOW EVERYTHING ALIVE.  A builder body in
                    # the same ray is SK_PRI_BODY = 2 and still wins -- killing
                    # the LAYER is worth more than killing what it laid, and a
                    # turret that prefers the barrier is a turret that lets the
                    # layer re-lay it.  v610's form scored this class at
                    # SK_PRI_HARVESTER = 3, above the body; set
                    # SK_ROUTEBLOCK_PRI = 3 to recover that ordering exactly.
                    # ⛔ SK_GUN_ROUTEBLOCK IS CHECKED FIRST so the flag-off tree
                    # cannot even evaluate `_routeblock_tile`.
                    elif (SK_GUN_ROUTEBLOCK and pri <= SK_PRI_BARRIER
                            and et == EntityType.BARRIER
                            and self.core is not None
                            and self._routeblock_tile((q.x, q.y))):
                        pri = SK_ROUTEBLOCK_PRI
                        rb_hit = True
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
                    target = (q, eid, rb_hit)
        if target is None:
            self._rotate_toward(ct, p, kind)
            return
        q, eid, rb_hit = target
        if not self.hp_trend_ok(ct, eid, rnd):     # ledger V7
            self._rotate_toward(ct, p, kind)
            return
        try:
            if ct.can_fire(q):
                ct.fire(q)
                # ⭐ v618 PLANK 3's AMMO COLUMN.  Counted at the SHOT, not at
                # the ranking: a routeblock that was ranked and then lost the
                # comparison to a body costs nothing, and a column that counted
                # rankings would over-report the plank's price.
                if rb_hit:
                    self.rb_shots += 1
        except Exception:
            return

    # ------------------------------------------------------------------
    # v611 SK_HOME_LAUNCHER -- the LAUNCHER's own turn
    # ------------------------------------------------------------------

    def _launcher(self, ct):
        """Throw the enemy collar-layer off our delivery ring.

        ⛔ THE ENGINE HAS NO TEAM CHECK ON `can_launch` AND NO VISION GUARD.
        That asymmetry is the whole exploit and it cuts both ways: the same call
        that throws THEIR builder will cheerfully throw OURS, and `can_launch`
        will answer for a tile we cannot see.  SK_HL_TEAM_CHECK is the only
        thing standing between this method and ferrying our own keeper into the
        enemy half; it is a flag so that an ablation can prove it fires, and
        nothing ships with it False.

        ⛔ NO AMMO IS INVOLVED -- launchers do not use the team ammunition pool,
        so the `_turret` ammo guard has no counterpart here and the drip's need
        arithmetic is untouched.  `launch` adds 1 to the action cooldown, so the
        rate limit is one throw every other round and nothing else.

        ⛔ THIS IS NOT THE CRASH ARM.  The target is chosen for DISTANCE, not
        for a map border.  If a thrown body dies to its own code afterwards that
        is an observation to record, never a thing this method aims at.
        """
        p = ct.get_position()
        self._boot(ct, p)
        rnd = ct.get_current_round()
        if self.core is None or self.enemy is None:
            for eid in ct.get_nearby_buildings():
                try:
                    if ct.get_entity_type(eid) != EntityType.CORE:
                        continue
                    if ct.get_team(eid) == self.team:
                        self.core = ct.get_position(eid)
                    else:
                        self.enemy = ct.get_position(eid)
                except Exception:
                    continue
        if self.core is not None and self.enemy is None:
            self.enemy = enemy_core_for(self.mw, self.mh, self.core)
        if ct.get_action_cooldown() != 0:
            return
        victim = self._hl_pick_victim(ct, p)
        if victim is None:
            return
        vpos, _vid = victim
        target = self._hl_pick_throw(ct, p, vpos)
        if target is None:
            return
        try:
            if not ct.can_launch(vpos, target):
                return
            ct.launch(vpos, target)
        except Exception:
            return
        self.hl_throws += 1

    def _hl_pick_victim(self, ct, p):
        """The enemy BUILDER to remove, best first.  (Position, id) or None.

        Ranked: a builder standing where it can work one of OUR delivery seats
        first (that is the collar-layer, by the engine's own adjacency rule),
        then anything else enemy in the pickup disc, nearest first.
        """
        seats = set(core_seats(self.core)) if self.core is not None else set()
        best = None
        for dx, dy in NEIGHBOURS8:
            q = Position(p.x + dx, p.y + dy)
            if not self.ibp(q):
                continue
            try:
                bid = ct.get_tile_builder_bot_id(q)
            except Exception:
                continue
            if bid is None:
                continue
            try:
                if SK_HL_TEAM_CHECK and ct.get_team(bid) == self.team:
                    continue            # ⛔ THE GUARD.  The engine has none.
                if ct.get_entity_type(bid) != EntityType.BUILDER_BOT:
                    continue
            except Exception:
                continue
            on_seat = 0
            for sdx, sdy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                if (q.x + sdx, q.y + sdy) in seats:
                    on_seat = 1
                    break
            if SK_HL_VICTIM_SEAT_ONLY and not on_seat:
                continue
            key = (-on_seat, p.distance_squared(q), q.x, q.y)
            if best is None or key < best[0]:
                best = (key, q, bid)
        if best is None:
            return None
        return best[1], best[2]

    def _hl_pick_throw(self, ct, p, vpos):
        """The farthest passable tile toward the ENEMY half.  Position or None.

        `can_launch` measures 1 <= d^2 <= 26 FROM THE LAUNCHER, not from the
        victim, so the candidate set is this unit's own r^2=26 disc -- which is
        also exactly its vision, so every candidate is a tile we can legally
        query.

        ⛔ NEVER INSIDE OUR OWN HOME RING (SK_HL_DROP_RING_DSQ).  A throw that
        lands their collar-layer on the far side of our own core has moved it
        from one delivery seat to another and paid a cooldown for the privilege.
        """
        cands = []
        try:
            tiles = ct.get_nearby_tiles(SK_HL_THROW_MAX_DSQ)
        except Exception:
            return None
        for t in tiles:
            d = p.distance_squared(t)
            if d < 1 or d > SK_HL_THROW_MAX_DSQ:
                continue
            if not self.ibp(t):
                continue
            if self.core is not None and dsq_core(t, self.core) <= SK_HL_DROP_RING_DSQ:
                continue
            try:
                if not ct.is_tile_passable(t):
                    continue
            except Exception:
                continue
            # PRIMARY: toward the enemy (strictly closer to their core than we
            # stand).  SECONDARY: as far from here as the engine allows.  A
            # displaced builder pays for the walk back, and the walk back is
            # what the arm is buying.
            away = 1 if self._hl_toward(t, p) else 0
            cands.append(((-away, -d, t.x, t.y), t))
        if not cands:
            return None
        cands.sort(key=lambda c: c[0])
        for _key, t in cands[:SK_HL_PROBE_CAP]:
            try:
                if ct.can_launch(vpos, t):
                    return t
            except Exception:
                continue
        return None

    def _rotate_toward(self, ct, p, kind):
        """Gunner-only: 10 Ti and one round of cooldown to face a target that
        the current line cannot reach.  A sentinel cannot rotate at all --
        which is COPY 2 seen from our own side.
        """
        if kind != EntityType.GUNNER:
            return
        if ct.get_global_resources() < 30:
            return
        # ⭐ v618 PLANK 2's ROTATION BUDGET.  10 Ti and a round of cooldown per
        # re-aim; ledger V7's lesson is that an unbounded re-aim is how 38
        # rounds and 152 Ti went into a target that was being healed faster
        # than we damaged it.  PER TURRET, PER GAME.
        # ⛔ THE CAP IS GATED ON *EITHER* PLANK, NOT ON PLANK 2 ALONE.  Gating it
        # on SK_HOME_GUNNER only would mean the P2-off ablation removes the cap
        # while PLANK 3's rotation exception stays live -- an ablation arm that
        # is strictly LESS bounded than the ship config, which makes its result
        # unreadable.  All-off still skips the gate entirely, so the identity
        # control is untouched.
        if SK_HOME_GUN_ROTATE and (SK_HOME_GUNNER or SK_GUN_ROUTEBLOCK):
            if self.rotations >= SK_HOME_GUN_ROT_CAP:
                return
        marked = self._marked_positions(ct)
        for _eid, et, ep in self.enemy_ids_near(ct):
            if p.distance_squared(ep) > 13:
                continue
            # v601 PLANK 3: 10 Ti and a round of cooldown to turn and face a
            # BARRIER is the same error as shooting it, only more expensive.
            # ⭐ v618 PLANK 3 CARVES ONE EXCEPTION AND ONLY ONE: a ROUTE-BLOCKING
            # collar barrier.  That tile is the difference between a harvester
            # delivering and a harvester being worth zero forever, and it is
            # what the gun was bought to sweep -- so the re-aim buys the plank
            # its own ray back.  Everything else the v601 refusal still covers.
            if (SK_TARGET_PRIO
                    and self._target_pri(et, (ep.x, ep.y), marked)
                    <= SK_PRI_OTHER):
                if not (SK_GUN_ROUTEBLOCK and SK_HOME_GUN_ROTATE
                        and et == EntityType.BARRIER
                        and self._routeblock_tile((ep.x, ep.y))):
                    continue
            face = p.direction_to(ep)
            try:
                if not ct.can_fire_from(p, face, EntityType.GUNNER, ep):
                    continue
                if ct.can_rotate(face):
                    ct.rotate(face)
                    self.rotations += 1
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
