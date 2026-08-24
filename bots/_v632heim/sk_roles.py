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
    adjacent_to_core, cheb_core, core_ring, core_seats, core_tiles,
    core_tiles_xy,
    dist_core, dsq_core, in_bounds, pack_pos, pack_tile, unpack_pos,
    unpack_tile,
)
from sk_maps import (
    BELT_TYPES,
    ARMED_TYPES,
    CARDINALS, CARD_DELTAS, DIRECTIONS,
    SK_AMMO_FLOOR, SK_AMMO_GUNNER, SK_AMMO_SENTINEL,
    SK_BARREL_GUARD, SK_BG_MEDIC, SK_BG_SUCC, SK_BG_SITE,
    SK_BG_MEDIC_ROLE, SK_BG_HOME_ROLES, SK_BG_HOME_BODIES,
    SK_BG_HOME_TURRETS, SK_BG_HOME_DSQ, SK_BG_HEAL_FLOOR,
    SK_BG_SUCC_LIVE, SK_BG_SUCC_NEAR, SK_BG_SITE_MAX_GUNS,
    SK_BG_SITE_CONFIRM, SK_BG_SITE_BAN_ROUNDS, SK_BG_FACE_STAT,
    SK_BG_ENGHEAL, SK_BG_ENGHEAL_NEAR, SK_BG_ENGHEAL_STEPS,
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
    SK_NEST_CLEAR, SK_NEST_CLEAR_GIVEUP, SK_NEST_CLEAR_OWN,
    SK_NEST_PB_LIFE, SK_NEST_PB_LIFE_N, SK_NEST_PB_LIFE_R,
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
    SK_SEAT_CLEAR_ADJ,          # s57 THE STAND arm 3 (the action-half widening)
    SK_TERMINATE, SK_TERM_FIRST, SK_TERM_MOVE,
    # --- v611 -------------------------------------------------------------
    SK_HOME_LAUNCHER, SK_HOME_LAUNCHER_MAX, SK_HL_MIN_ROUND, SK_HL_SITE_DSQ,
    SK_HL_SITE_MIN_COVER, SK_HL_THROW_MIN_DSQ, SK_HL_THROW_MAX_DSQ,
    SK_HL_PICKUP_DSQ, SK_HL_RESERVE, SK_HL_PROBE_CAP, SK_HL_DROP_RING_DSQ,
    SK_HL_SEAT_DENSITY, SK_HL_TEAM_CHECK, SK_HL_VICTIM_SEAT_ONLY,
    SK_HL_SITE_GIVEUP, SK_HL_SITE_TRIES, SK_HL_AFTER_S2,
    # --- s57 THE KILLBOX, arm 1 -------------------------------------------
    SK_KILLBOX, SK_KB_LAUNCHER, SK_KB_CELL, SK_KB_MAX, SK_KB_MIN_ROUND,
    SK_KB_RESERVE, SK_KB_SITE_MIN_DSQ, SK_KB_SITE_MAX_DSQ, SK_KB_SITE_CHEB,
    SK_KB_AXIS_BAND, SK_KB_MIN_COVER, SK_KB_PICKUP_DSQ, SK_KB_THROW_MAX_DSQ,
    SK_KB_TEAM_CHECK, SK_KB_CELL_CHEB, SK_KB_CELL_CANDS, SK_KB_CELL_RESERVE,
    SK_KB_CELL_SPAWN_RESERVE, SK_KB_WALK_MAX, SK_KB_GIVEUP, SK_KB_SITE_TRIES,
    # --- s57 THE KILLBOX, ARM 2 -------------------------------------------
    SK_KILLBOX_EXEC, SK_KB_EXEC, SK_KB_CELL_INTERIOR, SK_KB_EXEC_MAX,
    SK_KB_EXEC_RESERVE, SK_KB_EXEC_SEAT_DSQ, SK_KB_EXEC_OFF_RING,
    SK_KB_EXEC_WALK,
    SK_KB_BLOCK, SK_KB_CELL_BLOCK, SK_KB_EXEC_OVERLOAD, SK_KB_EXEC_LATCH,
    # --- s57 THE KILLBOX, ARM 3 (THE SPEED / LOGISTICS PACKAGE) -----------
    SK_KILLBOX_FAST, SK_KB_FAST_PARALLEL, SK_KB_FAST_BUYER, SK_KB_FAST_UNTIL,
    SK_KB_FAST_NEAREST, SK_KB_FAST_BUDGET, SK_KB_FAST_WALK_PER,
    SK_KB_FAST_WALK_CAP, SK_KB_FAST_CORNER, SK_KB_FAST_SPAWN_DIR,
    SK_KB_BLOCK_ON, SK_KB_INTERIOR_ON,
    # --- v612 -------------------------------------------------------------
    SK_MARCH_TEAMCHECK, SK_HOMEDEF_TEAMCHECK,
    # --- v613 (the ANTI-APRON axis) ---------------------------------------
    SK_APRON_DENY, SK_APRON_DSQ, SK_APRON_RELAY_CAP, SK_APRON_WINDOW,
    SK_APRON_RELAY_TOTAL, SK_APRON_BELT_PREF,
    # --- v632 PLANK 7 (the core-apron MESH, study §4d) ---------------------
    SK_APRON_MESH, SK_APRON_MESH_MAX, SK_APRON_MESH_SPAWN_RESERVE,
    SK_TUBE_FLOOR, SK_TUBE_NOPREP, SK_TUBE_FUND, SK_TUBE_FUND_AMMO,
    SK_TUBE_GAP_RELAX, SK_TUBE_GAP_MIN,
    SK_GAP_RELAX_SOLO, SK_NEST_EXHAUST_PB,
    SK_PECK_FOCUS, SK_PECK_FOCUS_DSQ, SK_PECK_FOCUS_BODIES,
    SK_PECK_FOCUS_KEEPER,
    SK_PLUCK_AWARE, SK_PLUCK_DSQ, SK_PLUCK_RETARGET, SK_PLUCK_MEMO_TTL,
    SK_CORE_MEDIC_RIDER,
    # --- s57 LEVER 2 -- THE HEAL-STAND (SK_CORE_STAND) --------------------
    SK_CORE_STAND, SK_CORE_STAND_HP, SK_CORE_STAND_HELP_HP,
    SK_CORE_STAND_SEAT_DSQ, SK_CORE_STAND_TI_FLOOR,
    # --- s57 THE STAND, ARM 2 -- HEAL-SEAT CLEARING (SK_STAND_SEATS) -------
    SK_STAND_SEATS, SK_STAND_SEATS_BAN, SK_STAND_SEATS_FLOW_K,
    SK_STAND_SEATS_GUN_DSQ, SK_STAND_SEATS_MAX, SK_STAND_SEATS_TARGET,
    SK_STAND_SEATS_WALK,
    # --- s57 THE STAND, ARM 4 -- THE ANSWER SENTINEL (SK_STAND_ANSWER) -----
    SK_STAND_ANSWER, SK_STAND_ANSWER_SPAWN,
    # --- s57 THE STAND, ARM 5 -- THE SIEGE PECK SWARM (SK_STAND_SWARM) -----
    SK_STAND_SWARM, SK_SWARM_N, SK_SWARM_PECKS, SK_SWARM_STALL,
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
    SK_TUBE_LATENCY_SOLO,
    SK_RENT_EARLY, SK_RENT_EARLY_RESITE, SK_RENT_EARLY_AGE,
    SK_RENT_EARLY_AGE_N, SK_RENT_EARLY_WINDOW, SK_RENT_EARLY_STEP,
    SK_RENT_STEP_BUDGET,
    # --- v632 HEIMDALL PLANK 1 (THE CITADEL DISPATCH) ----------------------
    SK_FORTRESS, SK_CITADEL, SK_CITADEL_CHEB, SK_CITADEL_BODIES,
    SK_CITADEL_GIVEUP, SK_CITADEL_JOIN_DSQ, SK_CITADEL_ROLES, SK_KEEPER_LEASH, SK_LEASH_DSQ, SK_ORE_STEPOFF,
    SK_IDLE_ACT_ALL,
    # --- v632 HEIMDALL PLANK 2 (THE DEMOLITION SWEEP) ----------------------
    SK_DEMOLISH, SK_DEMOLISH_CAP, SK_DEMOLISH_DSQ, SK_DEMOLISH_WALK_DSQ,
    # --- s57 THE SENTRY (SK_SENTRY) ----------------------------------------
    SK_SENTRY, SK_SENTRY_ALARM, SK_SENTRY_FOCUS, SK_SENTRY_HP_LIFT,
    SK_SENTRY_FOCUS_MAX, SK_SENTRY_FOCUS_RNDS, SK_SENTRY_HEAL_K,
    SK_SENTRY_BAN_RNDS,
    # --- s57 THE SENTRY V2 (the DISPATCH GATE) -----------------------------
    SK_SENTRY_FROM, SK_SENTRY_IDLE_LIFT,
    # --- v632 HEIMDALL PLANK 3 (THE TURRET RING) ---------------------------
    SK_FORT_RING, SK_FORT_RING_GUNNERS, SK_FORT_RING_SENT,
    SK_FORT_RING_WINDOW, SK_FORT_RING_RESERVE, SK_FORT_RING_LANE,
    SK_FORT_RING_SENT_DSQ, SK_FORT_RING_HARV_MIN,
    # --- v632 HEIMDALL PLANK 5 (THE SECOND ECO BODY) -----------------------
    SK_FORT_WALKER_ECO, SK_PHASE_ROUND,
    # --- v632 HEIMDALL PLANKS 8+9 (THE r300 ROTATION) ----------------------
    SK_ROTATE, SK_ROTATE_CHEST_FROM, SK_ROTATE_CLUSTER_GAP, SK_ROTATE_PREPS,
    SK_ROTATE_PRESTAGE, SK_ROTATE_RAIDERS, SK_ROTATE_WANT,
    # --- v632 HEIMDALL PLANK 10 (BATTERY SURVIVAL) -------------------------
    SK_ROTATE_GUARD, SK_ROTATE_GUARD_NEAR,
    # --- s57 THE BATTERY, ARM 1 (the live ceiling) -------------------------
    SK_BATTERY_WANT,
    # s57 THE BATTERY, ARM 2 (SK_BATTERY2) -- master + the three pieces.
    SK_BATTERY2, SK_BATTERY2_WANT,
    SK_BATTERY2_LEDGER, SK_BATTERY2_LEDGER_TTL,
    SK_BATTERY2_BURST, SK_BATTERY2_BURST_HOLD,
    SK_BATTERY2_ECO, SK_BATTERY2_ECO_W, SK_BATTERY2_ECO_WARM,
    SK_BATTERY2_ECO_AMMO, SK_BATTERY2_ECO_LIFE, SK_BATTERY2_ECO_BARREL, SK_BATTERY2_SENT_BUMP,
    SK_BATTERY2_LIVE_TEAM, SK_BATTERY2_ECO_CONV,
    # --- v632 SURVIVAL FAMILY -- PLANK A (walk-terminal guards, #130) and
    # --- PLANK B (the leashed keeper's duty, #128a residual / queued 4.1) ----
    SK_WALK_GUARDS, SK_WALK_GUARD_BAN, SK_LEASH_DUTY,
    # --- the nav-stall detector (#131), read by the `_builder` wrapper only ---
    SK_NAV_STALL,
    # --- work at a held post (queued 4.1b), read by `_home_keeper` only ------
    SK_KEEPER_WORK,
    # --- the chew-clock re-key (#4.3), read by `_clear_tile` only ------------
    SK_CHEW_REKEY, SK_CHEW_CLOCK_MAX,
    # --- keeper chew persistence (#4.3b), read by `_chew_giveup` only --------
    SK_KEEPER_CHEW_ON, SK_KEEPER_CHEW_GIVEUP,
    # --- s57 THE PUSH (SK_PUSH): pair reserve + warden + engineer forward ----
    SK_PUSH, SK_PUSH_RESERVE, SK_PUSH_RES_DEFENCE,
    SK_PUSH_RES_HOLD, SK_PUSH_RES_HALF, SK_PUSH_RES_BANKAWARE,
    SK_PUSH_WARDEN, SK_PUSH_WARDEN_ROLE, SK_PUSH_WARDEN_UNTIL,
    SK_PUSH_LAUNCH_RESERVE, SK_PUSH_PICKUP_DSQ, SK_PUSH_THROW_MAX_DSQ,
    SK_PUSH_MIN_SEATS, SK_PUSH_SITE_MAX_DSQ, SK_PUSH_WALK_MAX, SK_PUSH_GIVEUP,
    SK_PUSH_SITE_TRIES, SK_PUSH_TEAM_CHECK, SK_PUSH_ACTIVE_TTL,
    SK_PUSH_HEAL_FLOOR, SK_PUSH_BARREL_DSQ, SK_PUSH_STATION_OFF,
    SK_PUSH_STATION_NEAR, SK_PUSH_PROBE_CAP, SK_PUSH_BORDER,
    SK_PUSH_ENGINEER, SK_PUSH_ENG_QUIET, SK_PUSH_ENG_PREP,
    # --- s57 THE PUSH v3 (PIECE 2b): the warden as an ADDITIONAL body -------
    SK_PUSH_WARDEN2, SK_PUSH_W2_ROLE, SK_PUSH_W2_WALK_MAX,
    SK_PUSH_STATION_DWELL, SK_PUSH_STATION_STOPS,
    # --- s57 SK_HAMMER_PRIO: the spend-ladder inversion ---------------------
    SK_HAMMER_PRIO, SK_HAMMER_PRIO_BELT, SK_HAMMER_PRIO_PAIR,
    SK_HAMMER_PRIO_BIT, SK_HAMMER_PRIO_STICKY, SK_HAMMER_HOLD,
    # --- s57 VOLUME ARM 1: the two-bot column + the cardinal siting rank ----
    SK_VOLUME, SK_VH_COLUMN, SK_VH_CARDINAL,
    SK_VH_ROLE, SK_VH_FIELD, SK_VH_STALE, SK_VH_PAIR_ONLY,
    SK_VH_WALK_MAX, SK_VH_GIVEUP, SK_VH_VACATE,
    SK_VH_CARD_AFTER_D, SK_VH_CARD_FACE,
    # --- s57 SK_DOCTRINE: THE SKALMAN IDENTITY, ASSEMBLED -------------------
    SK_DOCTRINE, SK_DOC_BANK, SK_DOC_TRIGGER_LATCH, SK_DOC_LATCH_ONCE,
    SK_DOC_VANGUARD, SK_DOC_DENIER_OUT, SK_DOC_TOURNIQUET_COMMIT,
    SK_DENY_WALK_FIX,
    SK_DOC_TAIL_A, SK_DOC_REARM,
    SK_DOC_AMMO_MAX, SK_DOC_ANSWER_RESERVE,
    SK_DOC_DSQ_MIN, SK_DOC_DSQ_MAX, SK_DOC_CARDINAL,
    SK_DOC_BOX, SK_DOC_BOX_SUBORD, SK_DOC_HOME_BOX,
    # --- s57 ITERATION 10: SK_DOC_ECO_PUSH ---------------------------------
    SK_DOC_ECO_PUSH, SK_DOC_ECO_HARV_TARGET, SK_DOC_ECO_ORE_DSQ,
    SK_DOC_ECO_NEAR_FIRST, SK_DOC_ECO_DEFER_PECK, SK_DOC_ECO_DEFER_SWEEP,
    SK_DOC_ECO_DEFER_APRON,
)

# --- v632 PLANK A 4.2: the three guarded WALKS, as ban keys.  A tile is banned
# per (SITE, TILE) because the three walks have different target semantics --
# see SK_WALK_GUARD_BAN.  Single characters keep the key tuple cheap in a dict
# that is read inside the ore patrol loop.
WG_SITE_DENY = "d"      # `_ore_denier` -> `_deny_target`
WG_SITE_ESC = "e"       # `_home_keeper_move` -> `_escalate_target` branch 2
WG_SITE_DEF = "f"       # `_home_defence` -> SK_SLOT_THREAT_POS

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

# --- v632 PLANK 10: the FORWARDNESS threshold for the guard's tube census.
# d^2 from OUR core footprint above which one of our sentinels counts as a
# FORWARD tube rather than a home turret.  50 is the same constant the banked
# tube analysis uses to split `tubes` from `all_gun` (`FWD_D2` in the s57
# readout libs), so a tube the census calls forward is the same tube the
# instrument calls forward -- reusing the number is what keeps the dose
# counter and the life reader talking about one population.  It is NOT an
# SK_ flag: it is not a knob this plank sweeps, and adding it to the flag
# family would make the conjunction grep read three masters where there are
# two.
GUARD_FWD_DSQ = 50
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
# s57 SK_HAMMER_PRIO: slot 8 b12, the ECO-READY LATCH published for the bodies
# that are NOT the engineer.  ⛔ NOT A SECOND LATCH -- it is `batt2_eco_since`
# on the wire; see the SK_HAMMER_PRIO_BIT note for why slot 8 and why b12 is
# invisible to all three existing readers of this word.
HAMMER_LATCH_BIT = 1 << SK_HAMMER_PRIO_BIT
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
# --- s57 THE SENTRY (SK_SENTRY_ALARM): b30 of the SAME word ----------------
# "the freshness in b0-10 this round came from the PRESENCE latch (an enemy
# turret STANDING inside SK_SENTRY_DSQ of our footprint), not from an HP
# delta".  b0-29 were allocated above; b30 was free, so the presence trigger
# costs no second slot and every existing consumer keeps reading b0-10 exactly
# as before.  ⛔ SET ONLY WHEN THE PRESENCE STAMP IS THE NEWER OF THE TWO, so a
# round on which our core actually lost HP never wears it.
CF_SENTRY_BIT = 1 << 30
# --- s57 SK_DOCTRINE: b31 of the SAME word, THE LAST FREE BIT --------------
# THE BURST LATCH, and the wire is chosen the way SK_VH_FIELD's was: all 16
# store slots are allocated, so a new team-wide fact rides in free bits of a
# word that already has EXACTLY ONE WRITER.  Slot 15 is the CORE's
# (`_corefire_report`), the core is the one unit that cannot die without the
# match ending, it runs every round, and it writes this word WHOLE (never a
# read-modify-write) -- so the buffered-write lost-update class cannot appear
# here any more than it can for b30.
# ⛔ b0-30 were allocated above; b31 is the last free bit of the last free
# slot, and `wstore` masks to SK_STORE_MASK = 0xFFFFFFFF so setting it is
# inside `write_store`'s documented range.
# ⛔ WHY A WIRE BIT AT ALL, when tail A (`bank >= SK_DOC_BANK`) is a GLOBAL
# quantity every unit can read for itself: tail B needs the income sampler,
# which only the core runs regularly, and a body SPAWNED AFTER the burst began
# would otherwise re-derive "not fired" from a bank the burst has already
# drawn down.  The bit is what makes the phase a TEAM fact rather than a
# per-body opinion.
# ⚠ ONE ROUND OF LAG, DISCLOSED: store writes are buffered, so the bit the
# core sets on round r is readable from r+1.  Tail A is read LOCALLY by every
# body in the same round, so the lag can only ever delay the tail-B-only case
# by one round -- never tail A, and never in the direction of firing early.
CF_DOC_BIT = 1 << 31

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
        """⭐ v632 SK_NAV_STALL (#131) -- the two-line wrapper, and it is a
        WRAPPER rather than a block inside the turn for one reason: the turn has
        five early `return`s above the role switch (the corefire answer, ledger
        V5's home defence, the citadel answer, and two guards at the top), and a
        detector that misses the rounds a body returns early is a detector with
        five silent holes.

        GAME CONTEXT: in-engine bookkeeping for our own builder bots in the
        Florent Code League, a sandboxed bot-vs-bot competition.

        ⛔ OFF IS EXACT IDENTITY: one branch on a module constant and one call
        into the unchanged turn.  ZERO engine calls are added on the OFF path,
        so the replay is byte-identical.
        ⛔ NO `try/finally`: this sandbox rejects `finally` (see
        `_counter_march`'s note), and an exception escaping the turn is already
        caught one frame up in `run()` -- that round simply does not tick, which
        leaves the run counter where it was rather than corrupting it.
        """
        if not SK_NAV_STALL:
            self._builder_turn(ct)
            return
        p0 = ct.get_position()
        self.ns_walk = False
        self.ns_tgt = None
        self.ns_stepped = False
        self._builder_turn(ct)
        self._ns_tick(ct, p0)

    def _builder_turn(self, ct):
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
        # ⭐⭐ v632 HEIMDALL PLANKS 8+9 -- THE PHASE STATE, COMPUTED ONCE PER
        # BODY PER ROUND AND READ BY EVERY ROTATION SITE.  Two facts, kept
        # apart on purpose:
        #   `rot_on`   -- THE PHASE IS OPEN.  True for EVERY body (the home
        #                 keeper reads it too, for the §8a hazard-4 belt guard).
        #   `rot_body` -- THIS BODY IS A RAIDER.  True only for the two roles
        #                 in SK_ROTATE_RAIDERS, and it is what the dispatch,
        #                 the ledger width and every siege behaviour read.
        # ⛔ WHY HERE AND NOT AT THE SWITCH: the period-K cycle gate below runs
        # ABOVE the switch and needs `rot_body` (the walker body is excluded
        # from it today because `_cage_walker` calls `_cycle_commit` itself --
        # a call a rotation body never makes).
        # ⛔ BOTH ARE FALSE FOR EVERY ROUND OF EVERY SK_ROTATE-OFF ARM, so every
        # site that reads them is unreachable and the tree is character-for-
        # character the adopted one.
        # ⭐⭐ AND A THIRD, ADDED BY THE REDESIGN:
        #   `rot_stage` -- THIS BODY IS COMMUTING.  True for a raider in
        #                  [SK_ROTATE_PRESTAGE, SK_PHASE_ROUND), and it is
        #                  mutually exclusive with `rot_body` by construction:
        #                  one is the half-open window below the flip, the other
        #                  the half-open window at and above it, so no round can
        #                  set both and no site has to arbitrate between them.
        # ⭐⭐ s57 SK_DOCTRINE -- THE PHASE STATE, AND IT REPLACES THE ROUND
        # BOUNDARY WITH THE TRIGGER.  PROGRAMME.md ECO-READY HAMMER: "We don't
        # have to lock a hard round for the sentinel barrels at r300, we should
        # probably have an economy level we look for when we're funded enough to
        # hammer the other team's core ... it must be an honest live signal
        # (bank + income trend), never a wall-clock or round constant."
        # ⛔ IT REUSES `rot_body` RATHER THAN INTRODUCING A PARALLEL FLAG, and
        # that is deliberate: `rot_body` already means "this body is a raider on
        # the battery" at ELEVEN sites (the battery target SK_ROTATE_WANT, the
        # first-battery clustering, the prep suppression, the band half-split,
        # the plant counter, the guard heal).  A second name would either
        # duplicate all eleven or ship a doctrine whose burst is not the adopted
        # rotation.  The doctrine changes WHEN the phase opens, not what it is.
        # ⛔ `rot_on = True` FOR EVERY DOCTRINE ROUND, INCLUDING PHASE 1, AND
        # THAT IS A CORRECTNESS REQUIREMENT, NOT A CONVENIENCE.  Its two
        # consumers are fences against a MISSING WRITER: `_stall_check` refuses
        # to read the cage walker's seal-advance beat when nobody is writing it,
        # and `_plan_belt` drops the enemy anchor from its re-plan key.  Under
        # SK_DOCTRINE the walker NEVER runs `_cage_walker` -- in phase 1 it is a
        # home body, in phase 2 it is on the battery -- so slot 6 has no writer
        # from r0 and the stall detector's input is undefined for the whole
        # game, which is exactly the condition its own note describes.
        # ⛔ `rot_stage = False` ALWAYS: the commute exists to pre-position for a
        # KNOWN round.  A trigger has no known round, so there is nothing to
        # commute toward; the trigger IS the release.
        if SK_DOCTRINE:
            self.doc_fired = self._doc_fired(ct, rnd)
            self.rot_on = True
            self.rot_body = bool(self.doc_fired
                                 and self.role in SK_ROTATE_RAIDERS)
            self.rot_stage = False
        else:
            self.rot_on = bool(SK_ROTATE and rnd >= SK_PHASE_ROUND)
            self.rot_body = bool(self.rot_on and self.role in SK_ROTATE_RAIDERS)
            self.rot_stage = bool(SK_ROTATE
                                  and SK_ROTATE_PRESTAGE <= rnd < SK_PHASE_ROUND
                                  and self.role in SK_ROTATE_RAIDERS)
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
        # ⭐⭐ s57 THE PUSH v3, PIECE 2b -- THE WARDEN BODY WRITES NO BEAT, and
        # the guard is a MODULE-CONSTANT CONJUNCTION FIRST so an OFF arm pays
        # one constant test and reaches the same call.  `SK_SLOT_BEAT` has
        # exactly SK_N_ROLES entries and the warden holds role SK_N_ROLES, so
        # without this line that body would raise IndexError out of `run()` --
        # which the engine answers by destroying the unit for the rest of the
        # match.  Not writing a beat is also the DESIGN (see SK_PUSH_W2_ROLE):
        # the core's `live` census must keep counting the four COPY 8 roles and
        # nothing else.
        if not (SK_PUSH and SK_PUSH_WARDEN2) or self.role < SK_N_ROLES:
            self.beat(ct, SK_SLOT_BEAT[self.role], rnd)
            # ⭐⭐ s57 VOLUME ARM 1, PIECE (a) -- THE COLUMN'S ONE WRITE, and
            # it rides in the FREE UPPER BITS OF THE BEAT THIS LINE JUST WROTE
            # (slot 13, bits 11-20) because every one of the 16 store slots is
            # already allocated.  It is here rather than inside
            # `_siege_engineer` so it runs on EVERY engineer round including
            # the early returns -- a publish that skipped a round would leave a
            # stale site standing in the word, since `beat()` preserves upper
            # bits by construction.  ⛔ ROLE-GATED, so slot 13 keeps exactly
            # ONE writer even when a rotation body runs the engineer's TURN.
            # ⛔ CALL-SITE CONJUNCTION: SK_VOLUME False -> one module-constant
            # test and zero engine calls.
            if (SK_VOLUME and SK_VH_COLUMN
                    and self.role == SK_SIEGE_ENGINEER):
                self._vh_publish(ct, rnd)
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
        # ⭐ s57 THE STAND, ARM 2 (SK_STAND_SEATS) -- SAME PLACEMENT, SAME
        # ENGINE FACT.  `destroy` costs no action cooldown, no move and no turn,
        # so opening a blocked heal seat competes with nothing below it and the
        # heal rungs -- `_core_medic` at the top of the keeper's ladder -- run
        # this same round exactly as they would have.  Roles other than the two
        # home bodies, and every round the stand is not armed, return 0 on the
        # first lines.  With the flag False the first line returns 0 and this
        # call is inert.
        self._stand_seat_sweep(ct, p, rnd)

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
        # ⭐ v632 PLANKS 8+9, HAZARD (c) -- TRAVEL.  The walker is excluded here
        # ONLY because `_cage_walker` calls `_cycle_commit` itself (`:5146`).  A
        # rotation body never runs `_cage_walker`, so without this term the
        # converted walker would cross a board that is DENSE WITH BUILDINGS at
        # r300 with the period-K orbit detector switched off -- exactly the
        # 188-round orbit v606 ITEM 4(b) was built for.  `rot_body` is False on
        # every SK_ROTATE-off round, so the gate is unchanged there.
        # ⭐ THE COMMUTE NEEDS IT TOO, AND MORE THAN THE SIEGE DOES: r290-r300 is
        # the ONE stretch where the converted walker crosses the whole board in
        # one unbroken march with no build to break an orbit.
        # ⭐ s57 SK_DOCTRINE ADDS ONE TERM, AND IT IS THE SAME ARGUMENT THE
        # ROTATION TERM CARRIES.  The walker is excluded above ONLY because
        # `_cage_walker` calls `_cycle_commit` itself; under SK_DOCTRINE the
        # walker never runs that turn in EITHER phase, so without this term the
        # doctrine walker would cross the board (phase 2) and orbit the home
        # ladder (phase 1) with the period-K detector switched off -- the
        # 188-round orbit v606 ITEM 4(b) was built for.  ⛔ SK_DOCTRINE False ->
        # one module-constant test -> today's condition, character for
        # character.
        if SK_CYCLE_ALL_ROLES and (self.role != SK_CAGE_WALKER
                                   or self.rot_body or self.rot_stage
                                   or SK_DOCTRINE):
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
                and not self._tourniquet_committed(p)
                and self._denier_home_answer(ct, p, rnd)):
            return

        if (self._under_attack(ct, rnd) and self.role == SK_ORE_DENIER
                and not self._tourniquet_committed(p)):
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

        # ⭐ v632 HEIMDALL PLANK 1 -- THE CITADEL DISPATCH, and the ONE line
        # that makes three of four roles read slot 2 at all.  v628's fence on
        # the home answer is STRUCTURAL, not numeric: `_home_defence` and
        # `_denier_home_answer` are gated `self.role == SK_ORE_DENIER` above,
        # `_keeper_counter` runs only from `_home_keeper`, and the walker
        # contains ZERO references to SK_SLOT_THREAT_POS -- so at most one body
        # ever answers an intruder standing in our own core annulus.  Magnus's
        # citadel block is "EVERY single raider destroyed that 3 squares from
        # our core"; this is where "every" enters the tree.
        # ⛔ IT SITS IMMEDIATELY ABOVE THE ROLE SWITCH AND BELOW EVERY v608
        # SURVIVAL BRANCH ON PURPOSE.  Ledger V5 and the corefire answer are
        # "our CORE is being shot", which is a strictly worse emergency than
        # "something is standing near it", and both already own the denier.
        # Below them the citadel is the first thing every admitted body asks.
        # ⛔ CALL-SITE CONJUNCTION: with SK_FORTRESS False this branch is
        # unreachable and the dispatch below is character-for-character v628.
        if (SK_FORTRESS and SK_CITADEL and self.role in SK_CITADEL_ROLES
                and not (self.role == SK_ORE_DENIER
                         and self._tourniquet_committed(p))
                and self._citadel_answer(ct, p, rnd)):
            return

        # ⭐⭐ s57 BARRELS ARM 2, PIECE (a) -- THE BARREL MEDIC'S ONE CALL SITE.
        # ⛔ WHERE IT SITS IS THE STAFFING RULE.  BELOW every survival branch
        # (the corefire answer, ledger V5, the citadel dispatch) because a core
        # that is being shot outranks a barrel that is being pecked -- and the
        # re-task's own security read refuses on exactly that alarm anyway, so
        # the two cannot disagree.  ABOVE the role switch because a re-tasked
        # body must not fall through into the home ladder from a tile in the
        # band.
        # ⛔ FLAG OFF -> False on the first line -> the switch below is
        # character-for-character the adopted tree, with zero extra engine
        # calls.
        if self._bg_turn(ct, p, rnd):
            return

        # ⭐⭐ s57 VOLUME ARM 1, PIECE (a) -- THE COLUMN TRAILER'S ONE CALL
        # SITE.  Immediately below the barrel medic's, so it inherits the same
        # placement argument: BELOW every survival branch (a core that is being
        # shot outranks a tube that is not standing yet, and the column's own
        # security read refuses on exactly that alarm), ABOVE the role switch
        # so a marching body never falls through into the denier ladder from a
        # tile in the band under a stale plan.
        # ⛔ FLAG OFF -> False on the first line -> the switch below is
        # character-for-character the adopted tree, with zero extra engine
        # calls.
        if self._vh_turn(ct, p, rnd):
            return

        # ⭐⭐ v632 HEIMDALL PLANK 5 -- THE SECOND ECO BODY (SK_FORT_WALKER_ECO).
        # The body holding role SK_CAGE_WALKER runs the KEEPER's turn instead
        # of the cage.  Under FORTRESS DOCTRINE clause (1) ("builders never
        # raid") the cage is the one role with nothing left to do -- it is
        # 100% enemy-anchored, `cage_lap(self.enemy)` IS the role -- and the
        # keeper's turn is the tree's own named scarce resource
        # (`main.py:16`), so the cheapest way to buy more of it is a second
        # body on the same ladder.  Study §1a and §9 row 5.
        # ⛔ THE ROLE ID IS NOT CHANGED, ONLY THE TURN.  `self.role` stays 1,
        # which is what keeps the slot-11 beat (written in this method ABOVE,
        # keyed on `self.role`), the role parity, the seat claim and every
        # `self.role`-reading predicate exactly as they are today.  It is also
        # what makes the publisher gate below expressible at all.
        # ⛔ THE R5 PRECONDITION SHIPS WITH IT, NOT AFTER IT: every wstore rung
        # reachable from `_home_keeper` is gated on `self.role ==
        # SK_HOME_KEEPER` (slot 5 `_belt_report`, slot 14 `_killer_report`,
        # slot 4 `_harvester_action`), so the second body ACTS and never
        # PUBLISHES.  Buffered writes make two writers of one slot a SILENT
        # lost update -- measured at 291 frozen rounds on the tube beat.
        # ⛔ CALL-SITE CONJUNCTION, OWN FLAG, NO WELD: with SK_FORT_WALKER_ECO
        # False the first arm is unreachable and this switch is
        # character-for-character the current adopted tree.  It does NOT touch
        # and does not read the PARKED SK_FORTRESS/SK_CITADEL branch above,
        # which returns before ever reaching here.
        # ⭐⭐ PHASE-GATED FROM BIRTH (Magnus 2026-08-23, PROGRAMME.md
        # 48b874bea: `HEIMDALL_TACTIC_LOCK: eco_and_defence_to_r300_then_
        # rotate_and_destroy`, `FORTRESS_PHASE_FLIP: r300_two_raiders_...`).
        # The second eco body is a PHASE-1 body: at `rnd >= SK_PHASE_ROUND`
        # this arm stops matching and the walker falls through to its ORIGINAL
        # `_cage_walker` turn below, so the kill game returns.  ⛔ THAT
        # FALL-THROUGH IS A CRUDE PLACEHOLDER, NOT THE DESIGN: Magnus's
        # rotation is a rolling four-sentinel siege by two raiders, which is
        # the NEXT plank and will REPLACE the `elif` branch.  One-plank
        # discipline holds -- the flag still controls one behaviour change and
        # the r300 boundary is doctrine, already written in PROGRAMME.md,
        # not a second mechanism.
        # ⭐⭐ v632 HEIMDALL PLANKS 8+9 -- THE r300 ROTATION (SK_ROTATE), AND IT
        # SITS FIRST IN THE SWITCH BECAUSE IT SUPERSEDES PLANK 5's PLACEHOLDER.
        # PROGRAMME.md 48b874bea `FORTRESS_PHASE_FLIP:
        # r300_two_raiders_sentinel_siege_until_enemy_core_down`.  Both bodies
        # in SK_ROTATE_RAIDERS run the ENGINEER's turn -- the rolling sentinel
        # battery -- and everything phase-specific about that turn (battery
        # size, clustering, no preps, no pecking, the band split) is gated on
        # `self.rot_body` at its own site, never here.
        #
        # ⛔ THE TRUTH TABLE FOR THE TWO PHASE FLAGS, because they compose and a
        # successor must not have to derive it:
        #
        #   SK_ROTATE | SK_FORT_WALKER_ECO | walker's turn      | engineer's turn
        #   ----------|--------------------|--------------------|----------------
        #   False     | False              | _cage_walker (all) | _siege_engineer
        #   False     | True               | _home_keeper <300  | _siege_engineer
        #             |                    | _cage_walker >=300 |   (plank 5's
        #             |                    |   (PLACEHOLDER)    |    fall-through
        #             |                    |                    |    STANDS)
        #   True      | False              | _cage_walker <300  | _siege_engineer
        #             |                    | _siege_eng.  >=300 |
        #   True      | True               | _home_keeper <300  | _siege_engineer
        #             |                    | _siege_eng.  >=300 |   <- THE FULL
        #             |                    |                    |    DOCTRINE ARM
        #
        # The two flags are ORTHOGONAL by construction: plank 5 owns rounds
        # BELOW SK_PHASE_ROUND, this plank owns rounds AT OR ABOVE it, and
        # neither arm of the switch can match in the other's half.  The engineer
        # column never changes -- only where the branch is entered from.
        # ⛔ CALL-SITE CONJUNCTION, OWN FLAG, NO WELD: `rot_body` is False on
        # every round of every SK_ROTATE-off arm, so the first arm is
        # unreachable and this switch is character-for-character the adopted
        # tree (including plank 5's own OFF-identity).
        #
        # ⭐⭐ THE REDESIGN ADDS ONE ARM ABOVE THE FLIP, NOT A SECOND MECHANISM.
        # `rot_stage` occupies [SK_ROTATE_PRESTAGE, SK_PHASE_ROUND) -- the ten
        # rounds in which a raider does nothing but walk to where the flip needs
        # it.  It takes PRECEDENCE over plank 5's `_home_keeper` arm and over
        # the plain `_cage_walker`/`_siege_engineer` arms for those two roles
        # only, so the truth table above gains one row per SK_ROTATE=True line:
        # `_rot_prestage` for rnd in [290, 300), unchanged either side.
        # ⭐⭐ s57 THE PUSH v3, PIECE 2b -- THE WARDEN'S OWN ARM OF THE SWITCH.
        # ⛔ MODULE CONSTANTS FIRST: with SK_PUSH False this arm short-circuits
        # on the first name and the switch below is character-for-character
        # v632's.  It cannot match in any OFF arm for a second, structural
        # reason as well -- `_claim_role` only ever hands out role
        # SK_PUSH_W2_ROLE under the same two constants, so no body can be
        # holding it.
        # ⛔ AND IT SITS ABOVE THE FOUR ROLE ARMS, NOT INSIDE THEM: this body
        # has no home duty, no cage lap and no rotation seat (`rot_body` and
        # `rot_stage` are False for it because role 4 is not in
        # SK_ROTATE_RAIDERS), so it must never fall through to `_home_keeper`,
        # which is what the `else` at the bottom of this switch would do.
        if SK_PUSH and SK_PUSH_WARDEN2 and self.role == SK_PUSH_W2_ROLE:
            self._push_warden2(ct, p, rnd)
        elif self.rot_body:
            self._siege_engineer(ct, p, rnd)
        elif self.rot_stage:
            self._rot_prestage(ct, p, rnd)
        # ⭐⭐ s57 SK_DOCTRINE, PHASE 1 -- **NO FORWARD BODIES**, AND THIS ARM
        # IS THE WHOLE OF THAT SENTENCE.  PROGRAMME.md, the assembly mandate:
        # "home economy + defence until the eco latch; NO forward bodies
        # pre-latch (no rush -- the line's stated identity)".  The two raider
        # roles do not walk out: they take HOME roles on the keeper's own
        # ladder -- eco building, box construction, sentry answers.
        # ⛔ THE FORWARD RUNGS ARE GATED BY NOT BEING REACHED, WHICH IS THE
        # STRONGEST FORM OF GATING AVAILABLE HERE.  `_siege_engineer` (the
        # walk-out and the forward tube) and `_cage_walker` (the enemy-ring lap)
        # are the two forward turns in this tree and neither is entered by
        # either raider before the trigger.  There is no partially-gated forward
        # turn whose remaining rungs could leak a body across the board.
        # ⛔ IT SITS BELOW EVERY SURVIVAL BRANCH AND INSIDE THE SWITCH, so the
        # mandate's "phase never blocks defence" holds STRUCTURALLY: the
        # corefire answer, ledger V5, the citadel dispatch, the barrel medic and
        # the column trailer all run ABOVE this switch and are untouched by the
        # phase, and every defensive rung the home ladder owns (`_core_medic`,
        # `_stand_answer_action`, `_stand_swarm_action`, `_door_action`,
        # `_peck_priority`, the sentry answers) is reached by this arm.
        # ⛔ ABOVE the SK_FORT_WALKER_ECO arm because that arm is plank 5's
        # phase-1 placeholder for ONE role and this is the doctrine's own answer
        # for BOTH; the two must not both match.  ⛔ SK_DOCTRINE False -> one
        # module-constant test -> the switch below is character-for-character
        # the adopted tree.
        elif (SK_DOCTRINE and SK_DOC_VANGUARD
                and self.role == SK_SIEGE_ENGINEER):
            # ITERATION 9 — THE VANGUARD PAIR (w8diag's 45-game rule:
            # 4/4 wins vs zero-sentinel builds, 4/41 vs any; the lever is
            # barrels BEFORE the wall). Phase 1 keeps the walker home but
            # the ENGINEER runs its ordinary, best-tested 2-tube standoff
            # nest from the start — deterrence, not rush: no builder
            # aggression, want stays 2 until the trigger opens the burst.
            self._siege_engineer(ct, p, rnd)
        elif (SK_DOCTRINE and SK_DOC_DENIER_OUT
                and self.role == SK_ORE_DENIER):
            # ITERATION 11 — THE TOURNIQUET (Magnus: Bean-counters are #1
            # with NO early sentinel wall — they win by strangling the
            # opponent's delivery; and phase 1 was benching our own denial
            # arm). The ore denier plays its full away game (ore seals,
            # evictions — BC's 92.5%-coverage tourniquet is this machinery's
            # own class); engineer and keepers stay home; the bank still
            # feeds the burst. Denial is defence enacted on their economy.
            self._ore_denier(ct, p, rnd)
        elif SK_DOCTRINE and self.role in SK_ROTATE_RAIDERS:
            self._doc_home_turn(ct, p, rnd)
        elif (SK_FORT_WALKER_ECO and rnd < SK_PHASE_ROUND
                and self.role == SK_CAGE_WALKER):
            self._home_keeper(ct, p, rnd)
        elif self.role == SK_CAGE_WALKER:
            self._cage_walker(ct, p, rnd)
        elif self.role == SK_ORE_DENIER:
            self._ore_denier(ct, p, rnd)
        elif self.role == SK_SIEGE_ENGINEER:
            self._siege_engineer(ct, p, rnd)
        else:
            self._home_keeper(ct, p, rnd)

    # ==================================================================
    # s57 SK_DOCTRINE -- the assembly's four builder-side helpers
    # ==================================================================
    # GAME CONTEXT: in-engine decisions of our own builder bots in the Florent
    # Code League, a sandboxed bot-vs-bot competition.  "burst", "battery",
    # "box", "raider" are the engine's documented mechanics between competing
    # game bots.
    # ⛔ NONE OF THE FOUR IS REACHED ON AN OFF ARM: every call site is a
    # `SK_DOCTRINE ...` module-constant conjunction tested before any controller
    # call, and each method also returns on its own first line.

    def _doc_fired(self, ct, rnd):
        """THE TRIGGER, as this body sees it.  True once the burst is open.

        ⭐⭐ s57 TAIL C: THIS BODY IS NOW WIRE-ONLY, IN BOTH DIRECTIONS.
          * TAIL A -- `get_global_resources() >= SK_DOC_BANK` -- is RETIRED
            behind SK_DOC_TAIL_A (0 of 15 w1 cells fired on it).  Kept, dead,
            so a banking economy can have it back with one flag.
          * TAIL W -- the core's b31 latch on slot 15, which now carries the
            core's TAIL C (FUNDED and RATE and STABILITY).  Every one of those
            terms is core-local by construction, so the wire is the only
            channel a builder can have -- and with tail A off it is also the
            only one it HAS, which is what makes the core the single authority
            and the bounded re-arm coherent across bodies.
        ⛔ THE LATCH IS ONE-WAY (SK_DOC_LATCH_ONCE) AND ITS JUSTIFICATION IS
        AT THE FLAG.  With the flag off this method re-derives the phase every
        round, which is the ablation that shows what latching buys.
        ⛔ `doc_round` / `doc_tail` ARE INSTRUMENTS, NEVER INPUTS: nothing in
        the tree branches on them, so a bug there can only mis-report.
        """
        if not SK_DOCTRINE:
            return False
        if SK_DOC_LATCH_ONCE and self.doc_fired:
            # ⭐⭐ s57 TAIL C -- THE BOUNDED RE-ARM, FOLLOWED OFF THE WIRE.
            # The CORE is the only authority: it drops its own `doc_fired` when
            # the burst never assembled (`_doc_rearm`), which clears CF_DOC_BIT
            # on the next publish.  A builder that latched off the wire follows
            # the bit back DOWN, which is what makes the re-arm a phase change
            # rather than a core-only bookkeeping edit -- `rot_body` goes False
            # on the same round and the raider takes `_doc_home_turn` again.
            # ⛔ AN UNREADABLE WIRE HOLDS THE PHASE WE ARE IN.  A failed read is
            # not evidence the core dropped the phase, and re-homing both
            # raiders on a failed read is the expensive direction.
            if not SK_DOC_REARM:
                return True
            try:
                if ct.read_store(SK_SLOT_COREFIRE) & CF_DOC_BIT:
                    return True
            except Exception:
                return True
            self.doc_fired = False
            self.doc_rearms += 1
            return False
        tail = 0
        # ⛔ TAIL A IS RETIRED (SK_DOC_TAIL_A, ships False): 0 of 15 w1 cells
        # fired on it.  The branch is kept behind a module constant so a
        # successor with a banking economy gets the local tail back with one
        # flag, and so SK_DOC_BANK keeps a reader.  With it False the builder's
        # ONLY channel is the wire, which is what makes the core the single
        # authority in BOTH latch directions.
        if SK_DOC_TAIL_A:
            try:
                if ct.get_global_resources() >= SK_DOC_BANK:
                    tail = 1
            except Exception:
                tail = 0
        if not tail:
            try:
                if ct.read_store(SK_SLOT_COREFIRE) & CF_DOC_BIT:
                    tail = 2
            except Exception:
                tail = 0
        if not tail:
            return False
        if self.doc_round < 0:
            self.doc_round = rnd
            self.doc_tail = tail
        self.doc_fired = True
        return True

    def _doc_fwd_turn_tick(self):
        """⭐⭐ THE MANDATE'S BAR-0 COLUMN, AND IT IS A **CODE-PATH** COUNT.

        "NO forward bodies pre-latch" is a claim about which TURN a raider
        runs, so the honest instrument counts exactly that: a raider body
        entering `_siege_engineer` or `_cage_walker` -- this tree's only two
        forward turns -- before the trigger has fired.  BAR: 0.

        ⛔⛔ IT REPLACES A POSITION TEST THAT WAS CONFOUNDED TWICE, AND BOTH
        FAILURES ARE RECORDED BECAUSE THEY ARE THE SAME MISTAKE AT TWO SIZES.
        v1 asked "is the body inside d^2 32 of their core" and scored a
        STATIONARY body on a small map (helheim, dsq 29 constant over r34-91)
        as forward -- an absolute band cannot tell a raid from a short map.
        v2 asked "is it nearer their core than ours" and scored the HOME LADDER
        walking to an ore tile past the midline (stavkirke, role 3 at de=53
        dh=64) as forward -- a relative band cannot tell a raid from eco work
        that happens to be on the far side.  BOTH READ A POSITION AND THE CLAIM
        IS ABOUT A BEHAVIOUR.
        ⛔ THE POSITION COLUMN IS **KEPT** (`doc_forward`) AND DEMOTED TO A
        DIAGNOSTIC -- how far the phase-1 home ladder wanders -- because it is
        real information about the economy's reach.  It is not the bar.
        ⛔ NOTHING BRANCHES ON EITHER COUNTER.
        """
        if not SK_DOCTRINE:
            return
        if self.doc_fired:
            return
        if self.role in SK_ROTATE_RAIDERS:
            self.doc_fwd_turn += 1

    def _doc_burst_floor(self, ct):
        """"THE BURST CAN OPEN", priced LIVE.  None on an unreadable cost.

        ONE BARREL STANDING plus ONE FULL BATTERY VOLLEY in the magazine, plus
        ONE ANSWER SENTINEL HELD BACK (s57 w4, SK_DOC_ANSWER_RESERVE):

            get_sentinel_cost() + SK_DOC_AMMO_MAX + SK_DOC_ANSWER_RESERVE

        ⛔ THE THIRD TERM IS THE w4 FUNDING FIX.  The burst (trigger median r47)
        drained the opening 470 before the sieges arrived (median r171), so the
        answer read bank >= 120 on only 19% of its armed rounds.  Adding the
        reserve to THIS formula means the trigger cannot fire until the bank
        covers burst entry AND one answer -- and because the box ratchet guards
        the same number, the box cannot spend into the reserve either.

        read through the cost getter rather than a base cost, because every
        opening build has already inflated the ONE GLOBAL ADDITIVE factor by
        the time this is asked.  See the flag block for the measurement that
        chose this quantity over the full 4-sentinel burst price (0 of 988
        sampled rounds reached the latter).

        ⛔ ONE FORMULA, TWO CONSUMERS, AND THAT IS THE POINT: tail B asks "may
        the burst open?" and the box ratchet asks "would this purchase stop it
        opening?".  Two numbers would let the box spend the bank down to just
        under the trigger and call it subordinate.

        ⛔ IT RETURNS None RATHER THAN A GUESS, and the two callers take
        OPPOSITE conservative directions from that -- which is why the failure
        is not resolved here:
          * the TRIGGER refuses to fire on an unreadable price (do not commit
            the identity on a number we could not read);
          * the BOX REFUSAL refuses to refuse (`_push_price`'s own rule: a
            refusal manufactured out of a failed read withholds titanium for no
            measured reason).
        """
        try:
            return (ct.get_sentinel_cost() + SK_DOC_AMMO_MAX
                    + SK_DOC_ANSWER_RESERVE)
        except Exception:
            return None

    def _doc_home_turn(self, ct, p, rnd):
        """PHASE 1's turn for a raider body: the box, then the home ladder.

        ⛔ THE BOX RUNG FIRST AND THE KEEPER'S LADDER UNDER IT.  Arm 3's
        PARALLEL construction splits the opening between a BUYER (the launcher,
        `_kb_fast_owes_launcher`) and everyone else (the cell barriers,
        `_kb_fast_owes_cell`), and the buyer's rung physically lives inside
        `_cage_walker` -- a turn no doctrine body ever runs.  Re-siting it here
        is what keeps the split alive; the rung is still role-gated to
        SK_KB_FAST_BUYER inside itself, so the siege engineer falls straight
        through and lays cell barriers on the keeper's ladder instead.
        ⛔ IT IS NOT A FORWARD RUNG: the launcher site is Chebyshev
        SK_KB_SITE_CHEB of OUR OWN core (`_kb_pick_site`), i.e. home work.

        ⚠ `doc_forward` IS A DIAGNOSTIC, **NOT** THE BAR.  It counts phase-1
        rounds in which a raider body stands nearer the enemy core than our
        own -- i.e. how far the home ladder wanders -- with `doc_home_rounds`
        as its denominator.  THE MANDATE'S BAR-0 COLUMN IS THE CODE-PATH ONE,
        `doc_fwd_turn` (see `_doc_fwd_turn_tick` for why a position test cannot
        carry that claim).

        ⛔⛔ THE FIRST FORM OF THIS TEST WAS CONFOUNDED AND THE MEASUREMENT
        CAUGHT IT, WHICH IS WHY THE DEFINITION IS RELATIVE.  v1 asked
        `dsq_core(p, enemy) <= SK_NEST_DSQ_MAX` -- an ABSOLUTE band -- and read
        7 forward rounds on f2 helheim seatA at a CONSTANT dsq of 29 across
        r34-91.  A constant distance over 57 rounds is a body that never moved:
        on a map that small our own home sits inside d^2 32 of their core, so
        the absolute form scores HOME as FORWARD and the bar could never be met
        for a reason that has nothing to do with the doctrine.  An instrument
        whose failing reading is produced by the map size is not measuring the
        plank.  Nearer-theirs-than-ours is map-size invariant and is what
        "walked out" means.
        ⚠ THE RESIDUAL IS DISCLOSED: on a perfectly symmetric map the midline
        is a tie, and this counts a tie as HOME (strict `<`).  A body loitering
        exactly on the midline would go unscored -- bounded by one tile, and in
        the direction that makes the bar HARDER to claim, never easier... which
        is the wrong direction for a bar of zero, so the raw distances are put
        in the trace and the readout can re-cut them.
        """
        self.doc_home_rounds += 1
        if self.enemy is not None and self.core is not None:
            try:
                if dsq_core(p, self.enemy) < dsq_core(p, self.core):
                    self.doc_forward += 1
            except Exception:
                pass
        if SK_DOC_HOME_BOX and self._kb_fast_buyer_turn(ct, p, rnd):
            return
        self._home_keeper(ct, p, rnd)

    def _doc_box_refuse(self, ct, rnd, kind, site):
        """SPEND SUBORDINATION -- True when a BOX purchase must stand down.

        TWO CLAUSES, EACH WITH A REACHABLE OTHER VERDICT (see
        SK_DOC_BOX_SUBORD for the argument):
          * PHASE 2 STAND-DOWN -- after the trigger the money is the battery's
            and box CONSTRUCTION buys nothing.  The box keeps WORKING: the
            launcher's throws cost zero titanium and zero ammunition, and
            `_kb_pick_throw`'s to-cell priority is untouched.
          * PHASE 1 RATCHET -- a purchase that would take the bank from AT OR
            ABOVE `_doc_burst_floor` (the level at which the burst can open) to
            BELOW it is refused.  Below the floor the box spends freely, which
            is the whole opening.  ⛔ THE FLOOR IS THE TRIGGER'S OWN NUMBER, so
            the box literally cannot be the reason the trigger is late.

        ⛔ THE `kind` IS A CONSTANT AT EVERY CALL SITE, so an OFF arm never
        evaluates a cost getter -- this method returns on its first line.
        ⛔ `site` IS CARRIED FOR THE READOUT ONLY, exactly as `_push_refuse`
        carries it: pooling the refusals would hide WHICH spend was stopped.
        """
        if not (SK_DOCTRINE and SK_DOC_BOX_SUBORD):
            return False
        if self.doc_fired:
            self.doc_box_burst += 1
            return True
        res = self._doc_burst_floor(ct)
        if res is None:
            return False
        try:
            bank = ct.get_global_resources()
        except Exception:
            return False
        if bank < res:
            return False
        if bank - self._push_price(ct, kind) >= res:
            return False
        self.doc_box_ratchet += 1
        return True

    # ==================================================================
    # s57 ITERATION 10 -- SK_DOC_ECO_PUSH: PHASE-1 DELIVERY INTENSITY
    # ==================================================================
    # GAME CONTEXT: in-game Florent Code League.  These three helpers only
    # re-order OUR OWN builder bots' turns and widen OUR OWN ore choice.
    #
    # THE LEAD (windows ledger, 2026-08-24, the largest one left): live
    # delivered median ~1.0 Ti/round against the 2.1 replacement bar.  The
    # doctrine's trigger, box and tails all execute to spec; the economy
    # under them does not fund what they open.  Every starved trigger and
    # every empty answer traces here.

    def _doc_eco_on(self):
        """True while the phase-1 eco push is live for THIS body, this round.

        ⛔ MODULE CONSTANTS FIRST and NO CONTROLLER CALL AT ALL, which is what
        makes the OFF arm exact identity: with SK_DOC_ECO_PUSH False every
        consumer below short-circuits before it reads a cost, a tile or the
        bank.  `doc_fired` is refreshed once a round for every body under
        SK_DOCTRINE (`_builder`'s phase block), so this is a field read.
        """
        return bool(SK_DOCTRINE and SK_DOC_ECO_PUSH and not self.doc_fired)

    def _doc_eco_defer(self, site):
        """(c) THE REORDER -- True when a lower-value phase-1 verb stands down.

        ⛔ IT IS A REORDER, NOT A REMOVAL, AND THAT IS THE WHOLE SAFETY
        ARGUMENT: every rung this defers has a SECOND call site immediately
        below the general belt in the SAME `_home_keeper` turn, so a round on
        which no eco rung wanted the turn runs the verb exactly as v632 does,
        at the same cost, on the same inputs.  What the arm buys is the ORDER:
        `_route_action`, the terminating belt and `_harvester_action` get the
        keeper's turn first.  "THE KEEPER'S TURN IS THE SCARCE RESOURCE"
        (`main.py:16`) is this tree's own measured finding, and v632 PLANK 3's
        redesign is the precedent -- the ring was moved BELOW the economy for
        exactly this reason after turret-for-belt substitution was measured.

        ⛔⛔ NOTHING DEFENSIVE IS IN THIS SET.  `_counter_sent_action`,
        `_stand_answer_action`, `_core_medic`, `_stand_swarm_action`,
        `_door_action`, `_seat_heal_action`, `_heal_action`, `_seat_clear`,
        the home gun, the fort ring and the cover gun all keep their rank,
        unchanged and ungated.  The three deferred verbs are the 2 Ti peck at
        an adjacent enemy turret, the opportunistic demolition sweep and the
        apron barrier re-lay -- discretionary phase-1 work by this tree's own
        descriptions of them.

        ⛔ BOTH VERDICTS ARE STRUCTURALLY REACHABLE: False on every phase-2
        round (`doc_fired`) and on every round of an OFF arm; True on a
        phase-1 round with the flag on.  Each site keeps its own counter so
        the readout can say WHICH verb yielded rather than pooling them.
        """
        if not self._doc_eco_on():
            return False
        if site == "peck":
            if not SK_DOC_ECO_DEFER_PECK:
                return False
            self.eco_defer_peck += 1
        elif site == "sweep":
            if not SK_DOC_ECO_DEFER_SWEEP:
                return False
            self.eco_defer_sweep += 1
        elif site == "apron":
            if not SK_DOC_ECO_DEFER_APRON:
                return False
            self.eco_defer_apron += 1
        else:
            return False
        return True

    def _doc_ore_ok(self, q, count=False):
        """(a) THE WIDENED ORE FENCE -- may this body work ore tile `q`?

        v632: `is_home_half(q)` alone, a Voronoi half-plane against the ENEMY
        core.  It is the BINDING cap on harvester count on the pool's smaller
        and asymmetric maps -- the live doctrine tapes stand ~2 harvesters
        where the replacement bar wants the delivery of four.

        THIS ARM: home-half OR within SK_DOC_ECO_ORE_DSQ of OUR OWN core, and
        only while this body knows of fewer than SK_DOC_ECO_HARV_TARGET
        harvester tiles.  ⛔ IT IS A HOME FENCE, NOT A FORWARD ONE: the added
        clause is a radius around our own core, so it can never admit a tile
        the body would have to cross the map for, and it self-closes the
        moment the target is met.
        ⛔ THE THREAT LEASH STILL BINDS ON TOP (v632 PLANK 4): while
        `_under_attack` is fresh the walk refuses any economy target beyond
        SK_LEASH_DSQ, and SK_DOC_ECO_ORE_DSQ is that same number -- so under
        siege this flag admits nothing the leash does not already allow.
        ⛔ EVERY OTHER FENCE IS UNTOUCHED: `belt_plan` arbitration,
        `_harv_blocked` (PLANK 1's killzone ban), `path_arbiter_ok` and the
        engine's own `can_build_harvester` all run exactly as before.

        Returns the v632 verdict unchanged whenever the flag is off, so the
        OFF arm is character-for-character identical.

        ⛔ `count` IS PASSED TRUE AT EXACTLY ONE CALL SITE -- the ore WALK's
        own loop, where `ore_list()` guarantees the tile really is ore.  The
        build-side callers scan CARDINAL NEIGHBOURS before they know the
        terrain, so counting there would inflate the dose column with tiles
        that were never candidates.  One admission, counted once.
        """
        if self.is_home_half(q):
            return True
        if not self._doc_eco_on():
            return False
        if not SK_DOC_ECO_ORE_DSQ or self.core is None:
            return False
        if len(self.harv_tiles) >= SK_DOC_ECO_HARV_TARGET:
            return False
        if dsq_core(q, self.core) > SK_DOC_ECO_ORE_DSQ:
            return False
        if count:
            self.eco_ore_widened += 1
        return True

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
        # ⭐⭐ s57 THE PUSH v3, PIECE 2b -- THE WARDEN CLAIM OVERRIDE, AND IT IS
        # KEYED ON THE SAME PUBLIC PREDICATE THE CORE SPAWNED ON.
        # ⛔ WHERE IT SITS IS THE WHOLE MECHANISM.  This point is reached only
        # by a SURPLUS body -- every one of the four COPY 8 roles has a FRESH
        # beat, so nothing is vacant and the line below would otherwise make
        # this body a DUPLICATE of role `n % SK_N_ROLES` (which is exactly what
        # SK_KB_FAST_SPAWN's extra body is: a second keeper).  A surplus body
        # can only exist because some arm raised the core's `want`, and at most
        # one such body is outstanding at a time.
        # ⛔ THE DISCRIMINATOR AGAINST THE KILLBOX'S OWN EXTRA BODY IS NOT A
        # ROUND NUMBER BUT THE TRIGGER ITSELF: `_push_w2_trigger` is the SAME
        # store read the core made when it decided to spawn this body (a
        # forward tube beats in slot 7), so the killbox's opening body -- born
        # by SK_KB_FAST_SPAWN_BY = 8, when no forward tube can yet exist --
        # reads False here and falls through to its historical second-keeper
        # claim, character for character.
        # ⛔ THE SEAT COUNTER IS STILL CLAIMED AND STILL INCREMENTED (above), so
        # the core's `in_flight = spawned - seats` arithmetic is untouched.
        if (SK_PUSH and SK_PUSH_WARDEN2
                and self._push_w2_trigger(ct, rnd)):
            self.role = SK_PUSH_W2_ROLE
            self.role_parity = SK_PUSH_W2_ROLE & 1
            self.push_w2 = True
            self.push_w2_born = rnd
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

    def _tourniquet_committed(self, p):
        """ITERATION 12 — THE RELEASE, second form: a MISSION LATCH.

        The first form gated on `not is_home_half(p)` and the probe refuted
        it (probe_holmgang: 31 away turns vs 164 home turns): the denier
        crosses early, a recall catches it in the HOME half where the
        geometric gate does not bind, and under sustained pressure the
        50-round under-attack latch stays fresh forever — the release could
        never re-engage.  Catch-22 by construction: to be released it must
        be away; the recalls keep it home.

        Second form: while the tourniquet stands, the DENIER simply does not
        answer the three home recalls, anywhere.  ROLE-SCOPED EXEMPTION from
        FORTRESS_RESPONSE, inside the ratified identity (iteration 11
        provenance, Magnus verbatim basis: the ore denier plays its FULL
        away game while everyone else stays home) — keeper + walker + turret
        ring keep the intruder-response duty.  `p` kept for call-site
        stability; cleanly ablatable via SK_DOC_TOURNIQUET_COMMIT."""
        return (SK_DOCTRINE and SK_DOC_DENIER_OUT
                and SK_DOC_TOURNIQUET_COMMIT)

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

        ⭐⭐ s57 LEVER 2 (SK_CORE_STAND) ADDS A THIRD ARMING RUNG HERE, AND
        THIS PREDICATE IS THE GATE THE LOSS AUTOPSY IS DESCRIBING.  Every part
        of the heal-stand is already built and already ordered -- the ACT
        (`_core_medic`, called at the top of the keeper's action ladder), the
        POSITIONING (`_medic_seat`, called FIRST in `_home_keeper_move`) and the
        second medic (`_medic_turn` in `_denier_home_answer`) -- and all three
        are disarmed by this one method returning False, because SK_CORE_MEDIC
        and SK_CORE_MEDIC_RIDER both ship False.  The core heals the autopsy
        does find (3 of 8 threatened wins; median 0 heal-rounds over 60 cells)
        are the GENERIC `_heal_action` landing on the core because the keeper
        HAPPENED to stand beside it, which is coincidence rather than a stand.
        """
        if SK_CORE_MEDIC:
            return True
        if SK_CORE_STAND and self._core_stand_armed(ct):
            return True
        if not SK_CORE_MEDIC_RIDER:
            return False
        return self._two_tubes(ct)

    def _core_stand_armed(self, ct):
        """s57 LEVER 2's arming test: OUR CORE IS UNDER SIEGE RIGHT NOW.

        GAME CONTEXT: an in-engine state test in the Florent Code League, a
        sandboxed bot-vs-bot programming competition; "siege" is an opposing
        bot's turret standing in range and taking HP off our core under the
        engine's documented rules.

        TWO TERMS, AND THE SECOND IS THE ONE THAT MATTERS:
          * `corefire_fresh` -- our core has ACTUALLY LOST HP inside the last
            SK_COREFIRE_TTL (24) rounds, off the core's own slot-15 HP-delta
            latch.  Damage, not proximity: the slot-1 presence latch would arm
            on anything hostile standing near home.
          * CORE HP <= SK_CORE_STAND_HP -- ⛔⛔ AND WITHOUT IT THIS IS THE
            ALWAYS-FRESH CLASS (class audit row #132), NOT A NARROW STAND.
            `_fund_refuse`'s reachability tap measured `corefire_fresh` TRUE IN
            139 OF 139 keeper-rung rounds in [275, 350] across three cells, so
            freshness alone arms from the first nick to the end of the game --
            which is the unconditional SK_CORE_MEDIC form that was built,
            measured and shipped off.

        Returns False on any unreadable word (the latch reads 0, which is not
        fresh), i.e. FAILS TOWARD NOT STANDING: an unreadable alarm must not
        take the keeper off the belt.
        """
        if not SK_COREFIRE:
            return False                # with the sensor off the word reads 0
        try:
            rnd = ct.get_current_round()
        except Exception:
            return False
        if not self.corefire_fresh(ct, rnd):
            return False
        if self.corefire_hp(ct) > SK_CORE_STAND_HP:
            return False
        self.stand_rounds += 1
        return True

    def _medic_help_hp(self):
        """The SECOND medic's (the ORE DENIER's) core-HP threshold.

        SK_MEDIC_HELP_HP (200) is the v608 value and the reason it is late is
        stated at the constant: the second body is bought out of the DENIAL
        verb, which is the plank that opens the lane.  s57 LEVER 2 raises it to
        SK_CORE_STAND_HELP_HP for one arithmetic reason, and it is an ENGINE
        fact rather than a preference: `heal` sets the action cooldown to 1 and
        cooldowns decrement at end of round, so ONE body heals at most ONCE PER
        ROUND (+4 HP/round).  The registered target is ~1.65 heals/round, which
        one body cannot reach at any setting; two bodies cap at 2.0.
        ⚠ The denier's own ladder is UNCHANGED and still puts the counter-march
        ABOVE this rung, so the second medic spends only rounds in which it had
        no shooter tile to march at.
        """
        if SK_CORE_STAND:
            return SK_CORE_STAND_HELP_HP
        return SK_MEDIC_HELP_HP

    def _medic_seat_dsq(self):
        """How far a body will walk to take a medic seat.

        SK_MEDIC_SEAT_DSQ (25, i.e. five tiles) is the v608 value and its own
        note says what it protects: "the keeper's measured forward-action share
        is 0.000 and that property is load-bearing -- this fence keeps it".
        It also, measurably, keeps the keeper from ever walking home: on
        f1/helheim_seatB at r114-r116 the keeper stood at d^2 26-73 of every
        seat while our core was being shot.  s57 LEVER 2 widens it to
        SK_CORE_STAND_SEAT_DSQ under the stand and leaves it alone otherwise.
        ⚠ The forward-action property is NOT at risk from the wider fence: the
        seats are our own core's ring, so a longer walk is a longer walk HOME.
        """
        if SK_CORE_STAND:
            return SK_CORE_STAND_SEAT_DSQ
        return SK_MEDIC_SEAT_DSQ

    def _medic_ti_floor(self):
        """The bank floor `_core_medic` heals above.

        SK_MEDIC_TI_FLOOR (12) is v608's and its note says what it protects --
        "the drip is never starved for the medic".  Under s57 LEVER 2 it is
        SK_CORE_STAND_TI_FLOOR, which is the GENERIC heal rung's own floor
        (`_heal_action` refuses below a bank of 2).  ⛔ THE MEASUREMENT that
        put it here: with the arming gate and the walk fence lifted and this
        floor still at 12, the traced cells read 67 of 79 medic declines on
        f1/midgard_seatA, 34 of 51 on f1/valkyrie_seatB and 55 of 60 on
        f1/helheim_seatB as this test -- the stand armed, walked, sat down and
        then refused to heal.
        """
        if SK_CORE_STAND:
            return SK_CORE_STAND_TI_FLOOR
        return SK_MEDIC_TI_FLOOR

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

    def sentry_bit(self, ct):
        """s57 THE SENTRY -- True when THIS round's freshness came from the
        PRESENCE latch (an enemy turret standing inside SK_SENTRY_DSQ) rather
        than from our core actually losing HP.  Slot 15 b30.

        ⛔ WITH THE MASTER OFF THIS IS ALWAYS FALSE WITHOUT READING THE STORE:
        the core never sets b30, but the flag term first means an OFF arm makes
        no extra call at all -- which is what the byte-identity gate measures.
        """
        if not (SK_SENTRY and SK_SENTRY_ALARM):
            return False
        return bool(self.corefire_word(ct) & CF_SENTRY_BIT)

    def answer_fresh(self, ct, rnd):
        """THE PREDICATE THE ANSWER-DISPATCHING CONSUMERS READ -- the damage
        latch OR the presence latch.

        ⛔ NOT A NEW SEMANTIC.  "The answer ladder is armed" is exactly what
        `corefire_fresh` has always meant to these call sites; piece 1 adds a
        SECOND, EARLIER EVENT that arms it and nothing else.  The banked defect
        is that the only arming event was our core LOSING HP, which the autopsy
        measured 43 rounds after the killer was planted.

        ⛔ WHY A SEPARATE PREDICATE rather than widening `corefire_fresh`:
        that word has FIFTEEN consumers and only some of them DISPATCH AN
        ANSWER.  Widening it would arm the medic, the heal-stand, the
        push-quiet gate and the recall on the mere PRESENCE of a turret --
        planks whose bars were measured against the damage latch and which this
        expectation did not register.  This split IS the disclosure surface:
        `corefire_fresh` keeps every one of its readers unchanged, and the swap
        list in the build report is precisely the set given the earlier
        trigger.  OFF, the second term is a module constant that short-circuits
        before any store read, so this is `corefire_fresh` verbatim.
        """
        if self.corefire_fresh(ct, rnd):
            return True
        # ⭐⭐ s57 THE SENTRY **V2** -- ARM EARLY, STRIKE LATE.  The presence
        # half now passes through the DISPATCH GATE; the damage half returned
        # one line above and is untouched, on every tree and every round.
        if not self.sentry_bit(ct):
            return False
        return self._sentry_dispatch_ok(ct, rnd)

    def _sentry_dispatch_ok(self, ct, rnd):
        """s57 THE SENTRY V2 -- MAY A PRESENCE-ARMED ROUND DISPATCH AN ANSWER?

        THE BANKED REASON THIS EXISTS (v1 disposition, same registration): v1
        delivered its dose -- the 28-round free window fell to 8-9 rounds to
        first answer, F2 pecks-before-first-shot 7 -> 21, destroyed-before-
        first-core-shot 3 -> 6 -- AND BREACHED THE GUARDS, alive@300 59 -> 52
        against a -2 bar and wins 40 -> 35.  The mechanism was traced, not
        guessed: the alarm arms at r7-8 and at r7-8 the two answering bodies
        ARE the opening economy.

        SO THE ALARM IS UNCHANGED AND THE STRIKE MOVES.  The b30 stamp still
        lands at the plant, all three expiries still run, and every consumer
        still reads the same bit; this gate only decides WHEN the two answer
        dispatches act on it.  Their killer's first core shot lands ~r34
        median, so rounds SK_SENTRY_FROM..~30 are the tail of the same free
        window with the opening already laid.

        TWO WAYS THROUGH, in cost order:
          (1) `rnd >= SK_SENTRY_FROM` -- a pure integer compare, so on every
              post-FROM round this method makes ZERO engine calls;
          (2) THE IDLE LIFT -- this body has no build/harvest/heal task
              pending, so it is not being pulled off anything.  The read is an
              EXISTING one and is disclosed in full at SK_SENTRY_IDLE_LIFT: the
              bank cannot buy the CHEAPEST economic build this round.  Under
              that bank no conveyor, harvester, barrier or turret is
              purchasable at any site, by the engine's own arithmetic.

        ⛔ OFF-PATH: unreachable.  `answer_fresh` returns before calling this
        unless `sentry_bit` was True, and `sentry_bit` short-circuits on the
        module constants with the master off, so an OFF arm never evaluates a
        line of this method.
        ⛔ THE COUNTERS TICK BOTH TAILS (a gate never seen to refuse has not
        been seen to gate).  They are per-body and unpublished; the smoke reads
        the gate off the tracer, never off these.
        """
        if rnd >= SK_SENTRY_FROM:
            self.sentry_disp_late += 1
            return True
        if not SK_SENTRY_IDLE_LIFT:
            self.sentry_disp_refused += 1
            return False
        try:
            idle = ct.get_global_resources() < ct.get_conveyor_cost()
        except Exception:
            # A read we could not make is NOT evidence of idleness.  Refusing
            # is the conservative tail: it can only ever withhold an answer
            # v632 was not making anyway.
            self.sentry_disp_refused += 1
            return False
        if idle:
            self.sentry_disp_idle += 1
            return True
        self.sentry_disp_refused += 1
        return False

    def _sentry_gate_b_ok(self, ct, rnd):
        """v609 GATE B, with the PRESENCE lift.  True == the counter-peck may
        proceed on HP grounds.

        GATE B refuses the march while our published core HP is above
        SK_COUNTER_HP_MAX (450) -- i.e. until we have already taken ~50 damage.
        That is coherent for a DAMAGE alarm and fatal for a PRESENCE one: the
        autopsy measured their core at 500/500 in 12 of 20 losses and a median
        NET core damage of 0, so a presence trigger fires at full HP by
        construction and GATE B would swallow it every time.  The lift applies
        ONLY on a round wearing CF_SENTRY_BIT -- i.e. only where the freshness
        itself is presence-derived; on any damage round this returns exactly
        what the v609 line returned.

        ⛔ s57 V2 -- THIS METHOD IS **NOT** GATED BY `_sentry_dispatch_ok`, AND
        THAT IS DELIBERATE RATHER THAN AN OMISSION.  Both consumers test
        `answer_fresh` BEFORE they reach this line (`_keeper_counter`:1 and
        `_denier_home_answer`:2), so on a pre-FROM presence round they have
        already returned False and this predicate is unreachable.  Gating it
        too would be a SECOND copy of the same clock, which is how one gate
        becomes two definitions that drift.
        """
        if not SK_COUNTER_HP_MAX:
            return True
        if self.corefire_hp(ct) <= SK_COUNTER_HP_MAX:
            return True
        return bool(SK_SENTRY and SK_SENTRY_ALARM and SK_SENTRY_HP_LIFT
                    and self.sentry_bit(ct))

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
                and self.corefire_hp(ct) > self._medic_help_hp()):
            return False            # the second medic is bought late, on HP
        if ct.get_global_resources() <= self._medic_ti_floor():
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
                and self.corefire_hp(ct) > self._medic_help_hp()):
            return None
        if adjacent_to_core(p, self.core):
            return p
        # ⭐⭐ s57 LEVER 2 -- THE TWO GATES THAT MADE THIS METHOD RETURN None
        # ROUND AFTER ROUND, BOTH MEASURED, NOT GUESSED.  With the arming gate
        # lifted and nothing else changed, the stand armed 152 times on
        # f1/yggdrasil_seatA and landed ZERO heals; the tracer says why:
        #   (1) THE WALK FENCE.  SK_MEDIC_SEAT_DSQ = 25 and the keeper measured
        #       d^2 26-73 from every seat on f1/helheim_seatB at r114-r116 --
        #       just outside it, every round, so it never walked home.
        #   (2) THE READ ITSELF.  A builder's vision is r^2 = 20, and
        #       `is_tile_passable` RAISES on a tile outside vision (observed on
        #       the same rounds).  The `except: continue` below therefore
        #       DISCARDS every seat a body is not already standing next to --
        #       so even with the fence lifted the search would still find
        #       nothing.  ⇒ Under the stand an unreadable seat is a WALK
        #       TARGET, ranked BELOW every readable free one: we cannot know it
        #       is blocked, the walk re-evaluates every round, and arriving in
        #       vision restores the normal test.  Failing OPEN costs a few
        #       rounds of walking; failing closed costs the whole capability.
        # ⛔ WHAT IS *NOT* LIFTED, and it is the larger of the two occupancy
        # problems: a seat holding OUR OWN building stays refused.  Engine-side
        # census over the 60 baseline cells (ahbuild_seatcensus.py) --
        # during the siege window only 1.54 of the 8 seats are free on average,
        # 2.63 hold one of OUR buildings and 3.82 hold one of THEIRS, and in 10
        # of 46 siege cells there is no free seat at all.  Opening those needs
        # `destroy` on our own apron/door barriers, which is v603 FIX 4's and
        # ledger V2's road (74% of lost ring barriers were self-demolished);
        # that is a separate plank, not a rider on this one.
        best = None
        for q in core_ring(self.core):
            if not self.ibp(q):
                continue
            d = p.distance_squared(q)
            if d > self._medic_seat_dsq():
                continue
            rank = 0
            try:
                if not ct.is_tile_passable(q):
                    continue
                if ct.get_tile_builder_bot_id(q) is not None:
                    continue        # one medic per seat; the other takes another
            except Exception:
                if not SK_CORE_STAND:
                    continue
                rank = 1            # unreadable: a walk target, ranked last
            if best is None or (rank, d) < (best[0], best[1]):
                best = (rank, d, q)
        return None if best is None else best[2]

    def _medic_turn(self, ct, p, rnd):
        """Heal if seated, else walk to a seat.  True iff it took the turn."""
        if ct.get_action_cooldown() == 0 and self._core_medic(ct, p, rnd):
            return True
        seat = self._medic_seat(ct, p, rnd)
        if seat is None:
            # ⭐ s57 THE STAND, ARM 2 -- the clearing station, second, exactly
            # as in `_home_keeper_move`.  Flag off -> None -> v608 behaviour.
            seat = self._stand_station(ct, p, rnd)
        if seat is None:
            return False
        if seat.x == p.x and seat.y == p.y:
            # Seated but nothing to heal (core full, or bank at the floor).
            # Fall through rather than idle -- the seat is held by the movement
            # layer, not by burning the turn.
            return False
        return bool(self.step_to(ct, seat))

    # ==================================================================
    # s57 THE STAND, ARM 2 -- HEAL-SEAT CLEARING (SK_STAND_SEATS)
    # ==================================================================
    # GAME CONTEXT: in-engine mechanics of the Florent Code League, a sandboxed
    # bot-vs-bot programming competition.  `destroy` acts on an ALLIED building
    # only -- ours -- and the engine team-checks it; nothing here touches an
    # opposing bot's pieces.
    #
    # THE MEASURED PROBLEM (`ahbuild_seatcensus.py`, engine-side, over the siege
    # windows of the 60 baseline cells): 1.54 of our core's 8 heal seats free,
    # 2.63 holding one of OUR OWN buildings, and 10 of 46 siege cells with NO
    # free seat at all.  `_medic_seat` refuses a seat holding a building, so on
    # those cells the adopted stand cannot be staffed at any arming threshold.
    #
    # THE SHAPE, in one line: same trigger as the medic (no new latch),
    # scarcity-gated, ONE destroy per body per round, in a registered safety
    # order, above the turn because `destroy` costs no part of it.

    def _stand_flow_watch(self, ct, p, rnd, seats):
        """The BELIEF half of the belt refusal: which seat belt pieces have
        carried a resource stack, and how long we have been able to say so.

        ⛔ A TILE WE HAVE NOT WATCHED IS NOT A QUIET TILE.  Both dicts are
        needed and the second is the load-bearing one: `stand_flow` alone would
        read "never seen flowing" on the first armed round for every conveyor on
        the ring -- including the live delivery terminus -- because we had not
        looked yet.  `stand_watch` dates the LOOKING.
        ⚠ PER BODY, and populated only while the stand is armed: at most 8 tile
        reads a round for at most two home bodies, inside a siege window whose
        measured median is 54 rounds.
        ⛔ BOUNDS FIRST, THEN VISION (CLAUDE.md, corrected s50: `is_in_vision`
        is a pure radius test with NO bounds check, so it cannot be the outer
        guard).
        """
        for q in seats:
            if not self.ibp(q) or p.distance_squared(q) > 20:
                continue                    # this body's vision r^2
            xy = (q.x, q.y)
            try:
                if not ct.is_in_vision(q):
                    continue
                bid = ct.get_tile_building_id(q)
            except Exception:
                continue                    # unreadable: keep the last belief
            if bid is None:
                # The tile went empty -- whatever we believed about the piece
                # that stood here is about a building that no longer exists.
                self.stand_watch.pop(xy, None)
                self.stand_flow.pop(xy, None)
                continue
            try:
                if (ct.get_team(bid) != self.team
                        or ct.get_entity_type(bid) not in BELT_TYPES):
                    continue
            except Exception:
                continue
            if xy not in self.stand_watch:
                self.stand_watch[xy] = rnd
            try:
                if ct.get_stored_resource_id(bid) is not None:
                    self.stand_flow[xy] = rnd
            except Exception:
                # An unreadable stack reads as FLOW, not as quiet: the refusal
                # must fail toward keeping the belt piece.
                self.stand_flow[xy] = rnd

    def _stand_flow_quiet(self, ct, bid, xy, rnd):
        """True only if this belt piece has been WATCHED for
        SK_STAND_SEATS_FLOW_K rounds, has carried nothing in that window, and
        is carrying nothing right now.  12 rounds is three harvester emission
        periods (a stack every 4), so a piece on the live line cannot be quiet.
        """
        first = self.stand_watch.get(xy)
        if first is None or rnd - first < SK_STAND_SEATS_FLOW_K:
            return False                    # not watched long enough to say
        last = self.stand_flow.get(xy)
        if last is not None and rnd - last <= SK_STAND_SEATS_FLOW_K:
            return False
        try:
            if ct.get_stored_resource_id(bid) is not None:
                return False
        except Exception:
            return False                    # unreadable: treat as carrying
        return True

    def _stand_gunners(self, ct):
        """[(position, facing-delta or None)] for opposing GUNNERS near our own
        core -- live in vision, plus the tile-keyed memo.

        A turret is a BUILDING and cannot move, so a remembered tile outlives
        the entity leaving vision (`armed_memo`'s own durable-fact argument,
        v601 PLANK 1).  Including the memo makes the shield test refuse MORE
        often, which is the safe direction for a destructive verb.
        ⛔ GUNNERS ONLY, AND THAT IS AN ENGINE FACT RATHER THAN A CHOICE: a
        sentinel's line IGNORES OBSTACLES (entity table), so no barrier of ours
        has ever been cover against one and refusing on a sentinel's account
        would protect nothing while costing the whole capability.
        """
        out = []
        if self.core is None:
            return out
        for eid, et, ep in self.vis_enemy:
            if et != EntityType.GUNNER:
                continue
            if dsq_core(ep, self.core) > SK_STAND_SEATS_GUN_DSQ:
                continue
            try:
                f = ct.get_direction(eid).delta()
            except Exception:
                f = None                    # unreadable facing: test every ray
            out.append((ep, f))
        for xy, v in self.armed_memo.items():
            if v[0] != EntityType.GUNNER:
                continue
            q = Position(xy[0], xy[1])
            if dsq_core(q, self.core) > SK_STAND_SEATS_GUN_DSQ:
                continue
            out.append((q, self.armed_facing.get(xy)))
        return out

    def _stand_shielded(self, ct, q):
        """True if the building on seat q stands BETWEEN an opposing gunner and
        our own core footprint -- i.e. it is the cover this verb must not take.

        The test is exact where the facing is readable (the ray must be the
        facing) and CONSERVATIVE where it is not (every ray from that gunner).
        Reach is the gunner's own SK_KILLER_GUNNER_REACH, so at most 3 tiles
        cardinally and 2 diagonally: the seat has to be genuinely in the line.
        """
        if self.core is None:
            return False
        foot = core_tiles_xy(self.core)
        for g, face in self._stand_gunners(ct):
            dx = q.x - g.x
            dy = q.y - g.y
            if dx == 0 and dy == 0:
                continue
            if dx and dy and abs(dx) != abs(dy):
                continue                    # not one of the 8 compass rays
            if dx * dx + dy * dy > SK_KILLER_GUNNER_REACH:
                continue                    # the seat is out of its reach
            sx = (dx > 0) - (dx < 0)
            sy = (dy > 0) - (dy < 0)
            if face is not None and (face[0], face[1]) != (sx, sy):
                continue                    # it is not facing this way
            k = max(abs(dx), abs(dy)) + 1   # STRICTLY BEYOND the seat
            while k * k * (sx * sx + sy * sy) <= SK_KILLER_GUNNER_REACH:
                if (g.x + sx * k, g.y + sy * k) in foot:
                    return True
                k += 1
        return False

    def _stand_seat_class(self, ct, q, rnd):
        """THE SAFETY ORDER, and the refusals ARE the plank.  Read them as the
        specification; a class added here is a different experiment.

          0  PLAIN BARRIER      -- a barrier on a seat this body has no record
                                   of the apron plank having laid.
          1  APRON/DOOR BARRIER -- one the apron relay owns (`apron_ours`), and
                                   only while it is not shielding (see below).
          2  SPENT BELT PIECE   -- a conveyor/splitter OFF the current belt plan
                                   that has been watched quiet for
                                   SK_STAND_SEATS_FLOW_K rounds.
        REFUSED, always, in this order of reading:
          * NEVER a turret (ARMED_TYPES), NEVER the core, NEVER the HARVESTER.
          * NEVER a belt piece on the CURRENT PLAN.  `titanium_collected` counts
            DELIVERY, and the belt's terminal tile is a door tile by
            construction (`tile_owner`'s own ordering note) -- so the terminus
            IS a heal seat and taking it would trade the whole economy for one
            seat.
          * NEVER a belt piece that has carried a stack inside the window, or
            that this body has not watched long enough to say.
          * NEVER a barrier that occludes a live gunner's line to our footprint.
            ⛔ APPLIED TO CLASS 0 AS WELL AS CLASS 1, and that is deliberately
            WIDER than "apron/door barriers only": occlusion is a physical fact
            about the tile, not a property of which verb laid it, and a plain
            barrier in the line is exactly as load-bearing as a registered one.
            The registry decides only the ORDER.
          * NEVER anything whose type this plank has not priced (final `None`).
        """
        try:
            bid = ct.get_tile_building_id(q)
            if bid is None or ct.get_team(bid) != self.team:
                return None                 # empty, or an opposing bot's piece
            et = ct.get_entity_type(bid)
        except Exception:
            return None                     # unreadable: never destroy blind
        if et == EntityType.CORE or et == EntityType.HARVESTER:
            return None
        if et in ARMED_TYPES:
            return None                     # NEVER a turret
        xy = (q.x, q.y)
        if et in BELT_TYPES:
            if xy in self.belt_plan:
                return None                 # the delivery line
            if not self._stand_flow_quiet(ct, bid, xy, rnd):
                return None
            return 2
        if et == EntityType.BARRIER:
            if self._stand_shielded(ct, q):
                return None
            return 1 if xy in self.apron_ours else 0
        return None

    def _stand_seat_sweep(self, ct, p, rnd):
        """Open ONE heal seat.  Returns the number of buildings destroyed
        (0 or 1).

        ⛔ IT TAKES NOTHING FROM THE TURN.  `destroy` costs no action cooldown,
        no move and no turn (organisers' entity table; engine-probed on this
        line at `_rent_sweep`), which is why this runs at the TOP of the builder
        turn beside the rent sweep instead of as a rung in the ladder.  Every
        heal rung below -- `_core_medic` first -- runs afterwards unchanged, so
        a medic that already had a seat heals in the SAME round it clears one
        for the other body.
        ⛔ NO NEW TRIGGER.  The gate is `_medic_armed` (which under this line's
        CS arm is `_core_stand_armed`: corefire_fresh AND core HP <=
        SK_CORE_STAND_HP) plus `corefire_fresh` and the ORE DENIER's own
        `_medic_help_hp` rung -- the same three tests `_core_medic` and
        `_medic_seat` read.  Row #132 (the always-fresh class) is answered once,
        upstream, and re-answering it here would be a second latch to keep in
        step.
        ⚠ SCARCITY IS THE OTHER GATE: above SK_STAND_SEATS_TARGET known-free
        seats this verb is silent, and an UNREADABLE seat counts as FREE -- so
        the count fails toward NOT destroying.
        """
        if not SK_STAND_SEATS or self.core is None:
            return 0
        if self.role != SK_HOME_KEEPER and self.role != SK_ORE_DENIER:
            return 0                        # home bodies only; never a raider
        if self.stand_clears >= SK_STAND_SEATS_MAX:
            return 0
        if not self._medic_armed(ct) or not self.corefire_fresh(ct, rnd):
            return 0
        if (self.role == SK_ORE_DENIER
                and self.corefire_hp(ct) > self._medic_help_hp()):
            return 0                        # the second medic is bought late
        seats = core_ring(self.core)
        self._stand_flow_watch(ct, p, rnd, seats)
        free = 0
        held = []
        for q in seats:
            if not self.ibp(q):
                continue
            try:
                if (ct.is_tile_passable(q)
                        and ct.get_tile_builder_bot_id(q) is None):
                    free += 1
                    continue
            except Exception:
                free += 1                   # unreadable reads as FREE
                continue
            held.append(q)
        self.stand_seat_free += free
        self.stand_seat_rounds += 1
        # The gate reading, cached for `_stand_station` -- which runs LATER in
        # the same turn (movement) and must not pay the 8 reads a second time.
        self.stand_gate_rnd = rnd
        self.stand_gate_free = free
        if free >= SK_STAND_SEATS_TARGET:
            return 0                        # the stand can seat itself
        best = None
        for q in held:
            # `destroy` needs an ORTHOGONALLY ADJACENT tile -- not diagonal,
            # not this body's own tile.  d^2 == 1 is exactly that set.
            if p.distance_squared(q) != 1:
                continue
            cls = self._stand_seat_class(ct, q, rnd)
            if cls is None:
                self.stand_seat_refused += 1
                continue
            if best is None or cls < best[0]:
                best = (cls, q)             # ring order breaks ties, so the
                                            # choice is deterministic
        if best is None:
            return 0
        cls, q = best
        try:
            if not ct.can_destroy(q):
                return 0
            ct.destroy(q)
        except Exception:
            return 0
        xy = (q.x, q.y)
        self.stand_clears += 1
        self.stand_clear_cls[cls] += 1
        # Keep every belief that names this tile honest, and shut the thrash
        # loop: `escape_ban` is the dict `_apron_buildable` already consults,
        # so the apron relay will not re-lay this barrier for
        # SK_STAND_SEATS_BAN rounds.
        self.belt_built.discard(xy)
        self.belt_seen.pop(xy, None)
        self.apron_ours.pop(xy, None)
        self.apron_lost.pop(xy, None)
        self.stand_watch.pop(xy, None)
        self.stand_flow.pop(xy, None)
        self.escape_ban[xy] = rnd + SK_STAND_SEATS_BAN
        return 1

    def _stand_station(self, ct, p, rnd):
        """The tile to stand on in order to OPEN a seat, or None.

        ⚠⚠ DISCLOSED AS AN EXTENSION OF THE BRIEF, which specifies the destroy
        verb only, AND THE REASON IS THIS BUILD'S OWN FIRST MEASUREMENT: with
        the destroy alone, three walled-in siege cells gave 380 gated rounds,
        113 candidate seats and **ZERO** destroys -- every seat the body was
        ever orthogonally adjacent to was our own GUNNER (refused, correctly) or
        an opposing bot's building (not ours to destroy).  `destroy` needs an
        ADJACENT tile; `_medic_seat` returns None when every seat is blocked; so
        the medic never walks home and is never beside the blockage.  That loop
        is the same one the CS arm's first build hit ("armed 152 times, landed
        ZERO heals") and it has the same answer.  SK_STAND_SEATS_WALK = False
        ablates this half and restores the brief as written.

        FOUR TILES, geometric and fixed: the CORNERS of the core ring.  Each is
        orthogonally adjacent to exactly two seats and diagonal to the
        footprint, so a body standing on one can clear either of two seats and
        is one step from both.  Returns `p` itself when already stationed, which
        is how the caller learns to HOLD rather than wander back to the belt.

        ⛔ IT IS OFFERED ONLY WHERE `_medic_seat` ALREADY GAVE UP -- the callers
        ask this second -- so it can never displace a real seat, and it re-uses
        the stand's own walk fence, so it can add no walk the adopted arm would
        not already have made.
        """
        if not (SK_STAND_SEATS and SK_STAND_SEATS_WALK) or self.core is None:
            return None
        if self.stand_clears >= SK_STAND_SEATS_MAX:
            return None
        # The scarcity gate, read off the sweep's own cache from earlier THIS
        # turn.  A stale or absent reading means the sweep did not run (wrong
        # role, not armed, cap reached) and there is nothing to station for.
        if self.stand_gate_rnd != rnd:
            return None
        if self.stand_gate_free >= SK_STAND_SEATS_TARGET:
            return None
        ox, oy = self.core.x, self.core.y
        best = None
        for cx, cy in ((ox - 1, oy - 1), (ox + 2, oy - 1),
                       (ox - 1, oy + 2), (ox + 2, oy + 2)):
            q = Position(cx, cy)
            if not self.ibp(q):
                continue
            d = p.distance_squared(q)
            if d == 0:
                return p                    # stationed: hold
            if d > self._medic_seat_dsq():
                continue
            rank = 0
            try:
                if not ct.is_tile_passable(q):
                    continue
                if ct.get_tile_builder_bot_id(q) is not None:
                    continue                # one body per corner
            except Exception:
                rank = 1                    # unreadable: a walk target, last
            if best is None or (rank, d) < (best[0], best[1]):
                best = (rank, d, q)
        return None if best is None else best[2]

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
            # ⭐⭐ s57 THE STAND, ARM 5 -- THE SWARM TAKES THE SAME ESCAPE, and
            # it is a DISJUNCT rather than a new branch on purpose: the relax
            # already exists, is already argued, and already skips the veto
            # WITHOUT calling it (which is the load-bearing half -- `hp_trend_ok`
            # MUTATES `hp_memo` and latches `give_up`, so calling it and
            # ignoring the answer would still retire the target for every other
            # verb).  `self.sw_relax` is written ONLY inside
            # `_stand_swarm_action`, which returns on its first line when
            # SK_STAND_SWARM is False, so on every OFF arm this reads a field
            # that is False on every round of every game and the expression is
            # the v613 one exactly.  Scoped like v609 GATE E's
            # `nav_soft_bodies`: set immediately before the call, cleared
            # immediately after, never across a round boundary.
            relax = (self.sw_relax
                     or (SK_PECK_FOCUS and self.core is not None
                         and dsq_core(tgt, self.core) <= SK_PECK_FOCUS_DSQ
                         and self._friendly_adjacent(ct, tgt)
                         >= SK_PECK_FOCUS_BODIES))
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
        # ⭐ s57 THE SENTRY, PIECE 1 -- SWAP 1 of 2 (the KEEPER's arming).
        # `answer_fresh` is `corefire_fresh` OR the presence bit; with SK_SENTRY
        # False the second term short-circuits on a module constant and this IS
        # `corefire_fresh`, evaluated identically.
        # ⭐⭐ s57 V2 -- THIS IS ONE OF THE TWO CALL SITES THE DISPATCH GATE
        # GOVERNS.  The presence half of `answer_fresh` now passes through
        # `_sentry_dispatch_ok` (post-SK_SENTRY_FROM, or an idle body), so a
        # pre-FROM keeper with an opening task in hand refuses here and stays
        # on the belt.  The DAMAGE half is untouched at this site.
        # ⛔ TWO FURTHER ANSWER DISPATCHES WERE FOUND AND DELIBERATELY NOT
        # SWAPPED, and they are named here rather than in a report nobody
        # greps: `_stand_answer_action` and `_stand_swarm_action`.  Both are
        # answers, both read `corefire_fresh` -- and both sit under masters that
        # ship False (SK_STAND_ANSWER, SK_STAND_SWARM), so a swap is
        # unreachable on every tape this arm can run, while their trigger blocks
        # carry expect-1 anchors that `s4build_mkarm.py` mutates.  Turning
        # either master on is the moment to swap them, in that arm.
        if self.core is None or not self.answer_fresh(ct, rnd):
            return False
        # ⛔ v609 GATE B, BORROWED -- and it is written with this comment
        # ATTACHED so the line is not TEXTUALLY IDENTICAL to the one inside
        # `_denier_home_answer`.  The v610 battery's GATE B dirty control is a
        # string substitution on that exact two-line block, and a second copy
        # of it in this file makes the mutation land in the wrong method and
        # the scan pass a tree that breaks it (observed on the first v613
        # build: S11 reported BROKEN).
        # ⭐ s57 THE SENTRY: the gate keeps its integer and gains the PRESENCE
        # LIFT (see `_sentry_gate_b_ok`).  OFF, the helper's first two lines
        # reproduce this test exactly.
        if not self._sentry_gate_b_ok(ct, rnd):                 # v609 GATE B
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
        # ⭐ s57 THE SENTRY, PIECE 1 -- SWAP 2 of 2 (the DENIER's own arming).
        # ⭐⭐ s57 V2 -- AND CALL SITE 2 OF 2 FOR THE DISPATCH GATE, same
        # semantics as the keeper's: pre-FROM the presence bit reaches this
        # line and is refused unless this body is idle; the damage latch is
        # answered on round 0 exactly as v632 answers it.
        if not self.answer_fresh(ct, rnd):
            return False
        # ⭐ v609 GATE B -- the HP ceiling.  0 is OFF and is v608's behaviour.
        # ⭐ s57: the ceiling is unchanged; the PRESENCE LIFT is added inside
        # `_sentry_gate_b_ok` (its own docstring carries the measurement).  This
        # block stays TEXTUALLY DISTINCT from `_keeper_counter`'s copy -- see
        # the warning attached to that one.
        if not self._sentry_gate_b_ok(ct, rnd):
            return False
        # ⭐ v609 GATE A -- the NEAR emergency outranks the FAR one.  Returning
        # False here does not idle the body: the very next branch in
        # `_role_turn` is ledger V5, which marches it at the home threat.
        if SK_COUNTER_YIELD_HOME and self._home_threat_outranks(ct, rnd):
            return False
        tgt = self._counter_target(ct, rnd) if SK_COUNTER_PECK else None
        if tgt is not None and self._counter_march(ct, p, rnd, tgt):
            return True
        # ⭐⭐ s57 THE STAND, ARM 4 -- THE ANSWER, CALL SITE 2 of 2.
        # ⛔⛔ MOVED **ABOVE** the second medic (w4 autopsy, 2026-08-24), same
        # reason and same narrowness as call site 1: the medic block below eats
        # the turn on 68% of armed rounds, so an answer ordered under it never
        # ran (0 answers in 15 platform games).  This rung returns False in a
        # few reads unless a shooter tile is published + funded + a covering
        # seat is orthogonally adjacent to THIS body, and the medic takes every
        # other siege round unchanged.  It is a second call site rather than one
        # because the build needs an ORTHOGONALLY ADJACENT covering seat, so
        # which body is standing where decides whether the answer is available
        # at all -- and under SK_CORE_STAND this body is at home for the same
        # siege.  Flag off -> False on the first line -> v632 behaviour exactly.
        if self._stand_answer_action(ct, p, rnd):
            return True
        if self._medic_armed(ct) and self.corefire_hp(ct) <= self._medic_help_hp():
            if self._medic_turn(ct, p, rnd):
                return True
        # ⭐⭐ s57 THE STAND, ARM 5 -- THE SWARM, CALL SITE 2 of 2, same slot and
        # same non-preemption as arm 4's.
        # ⚠ TWO STRUCTURAL FENCES SIT ABOVE THIS LINE AND THIS ARM DOES NOT LIFT
        # THEM, so a denier can be absent from a window the keeper is inside:
        # v609 GATE B returns above when our core's published HP is over
        # SK_COUNTER_HP_MAX, and GATE A yields the body to a nearer home threat
        # (SK_COUNTER_YIELD_HOME).  Lifting either would be a second mechanism in
        # one plank; they are named here so the readout can attribute a
        # one-body-only window to them rather than to the swarm's own cap.
        # ⚠ AND `_counter_march` HAS ALREADY RUN ONCE ABOVE (line ~1852) with the
        # ledger-V7 veto live.  Reaching this line means that march DECLINED --
        # which for an adjacent body is very often the veto itself -- so the
        # swarm's contribution on this role is precisely the relaxed retry.
        return self._stand_swarm_action(ct, p, rnd)

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

    # ==================================================================
    # s57 THE STAND, ARM 4 -- THE ANSWER SENTINEL (SK_STAND_ANSWER)
    # ==================================================================
    # GAME CONTEXT: in-engine mechanics of the Florent Code League, a sandboxed
    # bot-vs-bot programming competition.  The "shooter"/"killer" is an
    # OPPOSING BOT'S TURRET taking HP off our core under the engine's rules;
    # the answer is a legal `build_sentinel` call at a tile of our own.
    #
    # The measurement this implements (CF-2 of KILLDIAG-ring-blindness) and why
    # it is not `SK_COUNTER_SENT` renamed are both written out at the flag.
    # ⛔ EVERY GEOMETRY QUESTION HERE IS PUT TO THE ENGINE.  `can_fire_from` is
    # the engine's own hypothetical-turret predicate (it ignores ammo and
    # cooldown, which is right: the question is BEARING, not readiness).  The
    # diagnosis this plank comes from had to correct hand-rolled ray math
    # twice, and the tree's own `_ray_hits` is the form PLANK 3 used.

    def _stand_answer_ep(self, rnd):
        """The current siege EPISODE's key: the round this body's unbroken
        freshness span began.  `_corefire_tick` maintains the streak at the top
        of every builder turn, so at action time a fresh alarm has streak >= 1.
        Per body, and both consequences of that are disclosed at the flag.
        """
        return rnd - self.corefire_streak + 1

    def _stand_answer_type(self, ct):
        """What the CORE said the shooter is, as an EntityType.

        Slot 15 carries one bit (CF_SENT_BIT) and the v607 anatomy's channel is
        19/19 enemy SENTINEL fire.  A gunner reading is the conservative one for
        the lane refusal below -- its attack pattern is the shorter of the two
        -- so an unset bit is taken at face value rather than upgraded.
        """
        if self.corefire_word(ct) & CF_SENT_BIT:
            return EntityType.SENTINEL
        return EntityType.GUNNER

    def _stand_answer_lane_faces(self, ct, tgt, et):
        """The shooter's OWN facings that bear on our core footprint.

        ⛔ THIS IS THE HALF THAT KEEPS US FROM FEEDING THE KILLER A LANE.  A
        seat on one of these rays is a 40-HP building standing in the line that
        is already taking our core apart, and a sentinel's shot IGNORES
        obstacles, so it does not even absorb the round -- it just dies.
        Asked with `can_fire_from(shooter, face, <their type>, <a core tile>)`,
        i.e. from THEIR tile outward, which is the engine's own answer to "can
        that turret, so faced, hit this".
        Cached on (shooter tile, core anchor): a turret is a BUILDING and cannot
        move, so the answer is stable for the whole episode and this costs at
        most 8 x 4 engine calls ONCE per siege rather than per round.
        """
        key = (tgt.x, tgt.y, self.core.x, self.core.y, et)
        if self._sa_face_key == key:
            return self._sa_faces
        foot = [Position(x, y) for (x, y) in core_tiles_xy(self.core)]
        faces = []
        for face in DIRECTIONS:
            for q in foot:
                try:
                    if ct.can_fire_from(tgt, face, et, q):
                        faces.append(face)
                        break
                except Exception:
                    continue
        self._sa_face_key = key
        self._sa_faces = tuple(faces)
        return self._sa_faces

    def _stand_answer_in_lane(self, ct, tgt, et, faces, q):
        """True if seat q sits on one of those lanes.  Fails toward REFUSING:
        an unreadable answer counts as in-lane, because the cost of refusing a
        good seat is one round of search and the cost of accepting a bad one is
        30+ Ti of turret standing in the killer's ray.
        """
        for face in faces:
            try:
                if ct.can_fire_from(tgt, face, et, q):
                    return True
            except Exception:
                return True
        return False

    def _stand_answer_action(self, ct, p, rnd):
        """Build ONE sentinel that BEARS ON the tile shooting our core.

        Returns True iff it took this body's turn with the build.

        ⛔⛔ ORDERED **ABOVE** THE MEDIC AT BOTH CALL SITES (w4 autopsy,
        2026-08-24).  IT SHIPPED BELOW THE MEDIC AND THAT ORDERING BUILT ZERO
        ANSWERS IN 15 PLATFORM GAMES: `_core_medic` arms at core HP <= 400 and
        returns True -- eating the whole turn -- on 68% of the 856 armed
        rounds, and a besieged core does not climb back over 400, so "the turn
        the medic declined" was a turn that did not arrive.  The old note is
        kept as the record of what was traded away: the medic reads the SAME
        armed state this rung reads, so the previous order guaranteed a body
        mid-heal was never pulled off it.
        ⛔ THE PRE-EMPTION IS NARROW BY CONSTRUCTION, which is what makes the
        swap cheap: this rung returns False in a handful of reads unless a
        shooter tile is PUBLISHED and fresh, no friendly turret already bears
        on it, the bank covers sentinel (+ builder under
        SK_STAND_ANSWER_SPAWN), and a covering seat is orthogonally adjacent to
        THIS body.  It takes at most ONE turn per siege episode (`_sa_done_ep`).
        Every other armed round still falls through to the medic.  What the one
        turn buys is the rung that ENDS the episode, against +4 HP on a core
        losing 9 HP/round.
        "Prefer the body already nearest the seat" falls out of the engine
        rather than out of a ranking: a build needs an ORTHOGONALLY ADJACENT
        tile, so only a body already standing beside a covering seat can ever
        propose one.
        """
        if not SK_STAND_ANSWER or self.core is None:
            return False
        if not SK_COREFIRE:
            return False
        try:
            if ct.get_action_cooldown() != 0:
                return False
        except Exception:
            return False
        if not self.corefire_fresh(ct, rnd):
            return False
        tgt = self.corefire_shooter(ct)     # THE PUBLISHED WORD ONLY (slot 15)
        if tgt is None:
            return False
        # ⛔ A NAMED TILE WHOSE BUILDING IS GONE IS NOT A SHOOTER.  Bounds test
        # FIRST and vision second -- `is_in_vision` is a pure radius test with
        # no bounds check (CLAUDE.md, corrected s50), so `ibp` has to be the
        # outer guard or the next `get_tile_*` raises off-map.  Out of vision we
        # cannot tell, and the latch's durable-fact argument (a turret is a
        # building; it cannot move) is what we fall back on.
        try:
            if self.ibp(tgt) and ct.is_in_vision(tgt):
                held = ct.get_tile_building_id(tgt)
                if held is None or ct.get_team(held) == self.team:
                    return False
        except Exception:
            pass
        ep = self._stand_answer_ep(rnd)
        if self._sa_seen_ep != ep:
            self._sa_seen_ep = ep
            self.stand_answer_eps += 1      # SEEN-CHOOSING: episodes armed
        self.stand_answer_windows += 1      # ... and rounds armed
        if self._sa_done_ep == ep:
            self.stand_answer_have += 1
            return False                    # one answer per siege episode
        # ⛔ THE CROSS-BODY HALF OF "ONE PER EPISODE".  The store has no free
        # slot (v608 took the last one), so the shared fact is read off the
        # BOARD instead: if one of our turrets already bears on the shooter,
        # the answer is already standing and a second is a second +20% on the
        # ONE GLOBAL ADDITIVE cost scale for nothing.
        # ITERATION 7 (w6diag): the veto must come from a turret that can
        # MEANINGFULLY answer. A bearing GUNNER (7 dmg, obstacle-blocked)
        # vetoed the answer against SENTINEL shooters it cannot suppress —
        # 84/84 covered-vetoes in w6's funded windows were gunners, 0 answers
        # built. If the shooter is a sentinel, only OUR SENTINEL bearing
        # counts as covered.
        _shooter_is_sent = True
        try:
            if self.ibp(tgt) and ct.is_in_vision(tgt):
                _h = ct.get_tile_building_id(tgt)
                if _h is not None:
                    _shooter_is_sent = (ct.get_entity_type(_h) == EntityType.SENTINEL)
        except Exception:
            pass
        if self._gun_bears(ct, tgt, sentinel_only=_shooter_is_sent):
            self.stand_answer_covered += 1
            return False
        try:
            cost = ct.get_sentinel_cost()
            need = cost
            if SK_STAND_ANSWER_SPAWN:
                need += ct.get_builder_bot_cost()   # `_spawn_plan`'s own bar
            if ct.get_global_resources() < need:
                self.stand_answer_unfunded += 1
                return False
        except Exception:
            return False
        if self._sa_funded_ep != ep:
            self._sa_funded_ep = ep
            self.stand_answer_funded_eps += 1   # THE OPPORTUNITY COLUMN
        et = self._stand_answer_type(ct)
        faces = self._stand_answer_lane_faces(ct, tgt, et)
        best = None
        best_site = None
        best_face = None
        for d in CARDINALS:
            q = p.add(d)
            if not self.ibp(q) or not self.may_build(q, OWNER_DOOR):
                continue
            if self.free_neighbours(ct, p, exclude=q) < 2:
                continue                    # the self-trap guard, v601 PLANK 2
            if not self.path_arbiter_ok(ct, q, rnd):
                continue                    # v605 FIX 1: a turret is impassable
            if SK_STAND_ANSWER_SPAWN and not self._claim_spawn_ok(ct, q):
                continue                    # the TILE half of the spawn reserve
            if self._stand_answer_in_lane(ct, tgt, et, faces, q):
                self.stand_answer_lane_refuse += 1
                continue                    # never stand in the killer's lane
            for face in DIRECTIONS:
                try:
                    if not ct.can_fire_from(q, face, EntityType.SENTINEL, tgt):
                        continue
                except Exception:
                    continue
                # All four candidates are d^2 = 1 from this body, so the rank
                # that separates them is closeness to the SHOOTER; CARDINALS
                # order (N, E, S, W) breaks the remaining ties deterministically
                # because the comparison is strict.
                score = (-q.distance_squared(tgt),)
                if best is None or score > best:
                    best = score
                    best_site = q
                    best_face = face
        if best_site is None:
            self.stand_answer_noseat += 1
            return False
        try:
            if not ct.can_build_sentinel(best_site, best_face):
                return False
            ct.build_sentinel(best_site, best_face)
        except Exception:
            return False
        self._sa_done_ep = ep
        self.stand_answers += 1
        return True

    # ==================================================================
    # s57 THE STAND, ARM 5 -- THE SIEGE PECK SWARM (SK_STAND_SWARM)
    # ==================================================================
    # GAME CONTEXT: in-engine mechanics of the Florent Code League, a sandboxed
    # bot-vs-bot programming competition.  The "shooter"/"killer" is an OPPOSING
    # BOT'S TURRET taking HP off our core under the engine's documented rules;
    # the "peck" is the engine's own documented builder action (`fire` on an
    # orthogonally adjacent tile, 2 Ti for 2 damage) against that opposing bot's
    # in-game structure.  Every call below is a documented Controller method.
    #
    # The measurement (killdiag CF-3), the arm-3 STRIKE this must not repeat,
    # and the three reasons the existing marches are not this rung are all
    # written out at SK_STAND_SWARM in sk_maps.py.  What is written HERE is only
    # what a reader of the code needs at the code.
    #
    # ⛔ THIS ARM ADDS NO MOVEMENT CODE AND NO FIRE CODE.  The walk and the peck
    # are `_counter_march` -- shipped, and already reached from these same two
    # roles today.  Consequences, all deliberate and all inherited unchanged:
    #   * the walk goes through `step_to`, the tree's ONLY movement entry, so
    #     SK_NAV_STALL's stall detector and ban cover this walk at the EXECUTOR
    #     level exactly as they cover every other walk (`sk_common.py:1451`);
    #   * SK_WALK_GUARDS does NOT cover it, and does not need to: that guard
    #     answers a walk at a STANDABLE tile the body is itself standing on
    #     (`_walk_escape`'s docstring), and this walk's target is an enemy
    #     BUILDING -- impassable, never underfoot -- so the terminal state it
    #     guards is unreachable here by construction;
    #   * the v612 FIX 1 team check comes with it (never peck our own relay laid
    #     on a recycled shooter tile), as does the `bank >= 2` floor and the
    #     SK_PLUCK_AWARE retarget/seat choice.
    #   * ⚠ IT ALSO INHERITS THE CONJUNCTION: with SK_COUNTER_PECK False,
    #     `_counter_march` returns False on its first line and this whole arm is
    #     inert.  SK_COUNTER_PECK is True in the shipped tree; stated so the
    #     dependency is on the record rather than discovered by a null.

    def _stand_swarm_action(self, ct, p, rnd):
        """Hold the shooter's ring and peck it, ONLY while the siege is live.

        Returns True iff it took this body's turn (a peck, a step, or holding a
        seat it must not be walked off).

        ⛔ ORDERED BELOW THE MEDIC AT BOTH CALL SITES -- arm 4's non-preemption
        read, reused rather than re-derived.  `_core_medic` is +4 HP on a core
        losing 9 HP/round and reads the SAME armed state this rung reads; this
        line is only reached on a turn the medic DECLINED (core full, bank at
        the floor, or this body is not the medic at all), so a body mid-heal is
        never pulled off it to go pecking.

        ⛔ THE RELEASE PATH, because the arm-3 refusal makes scope the whole
        plank.  There is NO latch.  The first five statements re-test the
        trigger EVERY round: master, core known, SK_COREFIRE, `corefire_fresh`,
        `corefire_shooter`, then the liveness read.  The moment the latch goes
        stale or the named tile stops holding an enemy building, this returns
        False and the body's normal ladder runs IN THE SAME ROUND -- there is no
        wind-down, no cooldown and no memory of having been dispatched.  The
        only cross-round state the arm owns is `_sw_seen_ep` / `_sw_peck_ep` /
        `_sw_pecks` / `_sw_last_rnd`, none of which is read by anything outside
        this method, and all of which are keyed to an episode that expires with
        the streak.  ⚠ TWO PRE-EXISTING MUTATIONS DO OUTLIVE THE CALL and are
        disclosed rather than suppressed: `_counter_march` may pop `armed_memo`
        on its team check and may move `pluck_last`.  Both are the shipped
        march's own behaviour, already reachable from these two roles today.
        """
        if not SK_STAND_SWARM or self.core is None:
            return False
        if not SK_COREFIRE:
            return False
        if not self.corefire_fresh(ct, rnd):
            return False
        # ⛔ THE COMMENT ON THE NEXT LINE IS DELIBERATELY NOT ARM 4's WORDING.
        # The three lines above it would otherwise be TEXTUALLY IDENTICAL to
        # `_stand_answer_action`'s trigger, and the v613 build report's own
        # lesson is that a duplicated block makes a scratch mutation land in the
        # WRONG METHOD and a broken tree read as passing.  `s4build_mkarm.py`'s
        # M8/M9/M11 anchor on exactly that block with an expect-1 assertion.
        tgt = self.corefire_shooter(ct)     # slot 15's published tile (arm 4's)
        if tgt is None:
            return False
        # ⛔ ARM 4's LIVENESS TEST, SAME ORDER, SAME FAIL-OPEN.  Bounds FIRST and
        # vision second -- `is_in_vision` is a pure radius test with no bounds
        # check (CLAUDE.md, corrected s50), so `ibp` has to be the outer guard
        # or the next `get_tile_*` raises off-map.  Out of vision we cannot
        # tell, and the latch's durable-fact argument (a turret is a BUILDING;
        # it cannot move) is what we fall back on.  A body ADJACENT to the tile
        # always has it in vision, so the release below is never blind on the
        # one body whose turn this actually costs.
        try:
            if self.ibp(tgt) and ct.is_in_vision(tgt):
                held = ct.get_tile_building_id(tgt)
                if held is None or ct.get_team(held) == self.team:
                    self.swarm_dead_release += 1
                    return False
        except Exception:
            pass
        ep = self._stand_answer_ep(rnd)     # arm 4's episode key, verbatim
        if self._sw_seen_ep != ep:
            self._sw_seen_ep = ep
            self.swarm_eps += 1
        self.swarm_windows += 1             # THE OPPORTUNITY DENOMINATOR
        # ⭐ THE ENEMY-LAUNCHER HAZARD, COUNTED AND NOT ANSWERED (registered out
        # of scope).  `thrown_rnd` is the tree's own displacement guard
        # (`sk_common.py:352`): a jump of more than SK_TELEPORT_DSQ since our
        # last turn proves a launcher picked this body up.  Counted only when
        # this body was dispatched within the last two rounds, so it measures
        # THROWS OF SWARM BODIES DURING WINDOWS rather than throws in general.
        if self.thrown_rnd == rnd and rnd - self._sw_last_rnd <= 2:
            self.swarm_throws += 1
        if self._sw_walk_ep != ep:
            self._sw_walk_ep = ep
            self._sw_best = 1 << 30
            self._sw_stall = 0
        man = abs(tgt.x - p.x) + abs(tgt.y - p.y)
        adj = man == 1
        if adj:
            self.swarm_adj_rounds += 1
            self._sw_best = 1
            self._sw_stall = 0
        else:
            # ⭐⭐ THE WALK-PROGRESS BOUND, AND IT IS HERE BECAUSE THE TRACE PUT
            # IT HERE (s5build, f1/auroraveil_seatB, the arm's own first traced
            # cell).  The home keeper was dispatched at r148 from Manhattan 8 of
            # a shooter at (10,14) and spent 55 CONSECUTIVE armed rounds -- to
            # r202, when our core died -- cycling (6,18)->(6,17)->(5,17)->
            # (6,17)->(5,17)->(5,18)->(6,18), an 8-round loop at constant
            # distance 7-9.  It never reached the ring and never pecked.  That is
            # 55 keeper turns, and "the keeper's TURN is the scarce resource" is
            # the exact sentence STAND arm 3 was refused on.
            # ⛔⛔ AND NEITHER ADOPTED WALK GUARD SEES IT.  SK_NAV_STALL is at
            # the executor (`step_to`) and DOES cover this walk -- but its
            # predicate resets the moment the body's position changes
            # (`_ns_tick`: `if p.x != p0.x or p.y != p0.y: self.ns_run = 0`), so
            # it detects a FROZEN body and is blind to a MOVING loop.
            # SK_WALK_GUARDS answers a walk at a STANDABLE tile the body is
            # standing on; this walk's target is an enemy BUILDING, impassable
            # and never underfoot, so its terminal state cannot occur here.  The
            # bound is therefore this arm's own, on the axis those two cannot
            # see: MOTION WITHOUT PROGRESS.
            # THE THRESHOLD IS MEASURED, NOT PICKED.  Off-ring runs of
            # non-improving Manhattan distance across the 13 traced (body,
            # episode) approaches: 0,0,0,0,2,2,2,2,2,3,5 for the ELEVEN that
            # reached the ring, then 24 and 53.  SK_SWARM_STALL = 16 sits inside
            # that gap: every approach that ever arrived is untouched, and the
            # only two it truncates are the 55-round auroraveil loop and
            # stavkirke's r370 approach -- which, when it did arrive, landed 15
            # pecks on a target the enemy healed back to full every round (post-
            # peck HP 38 on all 15 lines, +30 HP healed) for 30 Ti of nothing.
            # ⚠ IT IS A PER-EPISODE BOUND ON THIS ARM'S OWN DISPATCH, NOT A
            # GIVE-UP: nothing is latched, no other verb is retired, and it
            # expires with the episode key like the peck budget.  0 disables it.
            if man < self._sw_best:
                self._sw_best = man
                self._sw_stall = 0
            else:
                self._sw_stall += 1
                if SK_SWARM_STALL and self._sw_stall > SK_SWARM_STALL:
                    self.swarm_stalled += 1
                    return False
            # ⛔ THE CAP IS ON ADMISSION, NOT TENURE.  A body already on the ring
            # is inside this census and can never be evicted by it; evicting a
            # seated body is how a cap becomes an oscillation.  Only a body that
            # would have to WALK IN is refused when the ring is full.
            if self._friendly_adjacent(ct, tgt) >= SK_SWARM_N:
                self.swarm_full += 1
                return False
        if self._sw_peck_ep != ep:
            self._sw_peck_ep = ep
            self._sw_pecks = 0              # the budget expires WITH the episode
        if self._sw_pecks >= SK_SWARM_PECKS:
            self.swarm_capped += 1
            return False
        self.swarm_dispatch += 1
        self._sw_last_rnd = rnd
        before = self.counter_pecks
        # ⭐ THE V7 RELAX, SCOPED LIKE v609 GATE E's `nav_soft_bodies`: set
        # immediately before the call, cleared immediately after, never across a
        # round boundary.  ⛔ NO `try/finally` -- THE PLATFORM SANDBOX REJECTS
        # `finally` BLOCKS OUTRIGHT (`ValueError: 'finally' blocks are not
        # allowed`, the note at `_counter_march`).  The plain form is equivalent:
        # `_counter_march` swallows its own engine errors, and anything that did
        # escape would destroy this unit for the rest of the match, so there is
        # no later turn for a stale flag to corrupt.
        self.sw_relax = True
        took = self._counter_march(ct, p, rnd, tgt)
        self.sw_relax = False
        if self.counter_pecks > before:
            self._sw_pecks += 1
            self.swarm_pecks += 1
        if took:
            return True
        # ⛔ SEATED AND WITHOUT A VERB IS STILL TAKING THE TURN -- the same call
        # `_keeper_counter` makes (`keeper_holds`).  A body that returns False
        # here is walked off the ring by `_home_keeper_move` / the denier's own
        # walk, and a lost seat is indistinguishable from the plank declining:
        # the currency CF-3 prices is ADJACENT ROUNDS, so giving one back to
        # spend the round elsewhere is the plank paying its own bar out.
        if adj:
            self.swarm_holds += 1
            return True
        self.swarm_nowalk += 1
        return False

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
            # ⭐⭐ s57 THE STAND, ARM 4 -- THE ANSWER, CALL SITE 1 of 2.
            # ⛔⛔ MOVED **ABOVE** `_core_medic` (w4 autopsy, 2026-08-24).  It
            # shipped BELOW the medic and built 0 answers in 15 platform games:
            # the medic returns True (eating the whole turn) on 68% of the 856
            # armed rounds, because it arms at core HP <= 400 and a besieged
            # core is under 400 for the rest of the game.  A rung that only runs
            # on the medic's declined turns therefore never ran at all.
            # ⛔ THE PRE-EMPTION IS NARROW AND PRICED: `_stand_answer_action`
            # returns False unless a shooter tile is PUBLISHED (slot 15, fresh),
            # the bank covers sentinel + builder, no turret already bears, and a
            # covering seat is orthogonally adjacent to THIS body.  On every
            # other siege round it falls through in a few reads and the medic
            # takes the turn exactly as before.  What it buys with the one turn
            # it does take is the rung that ENDS the episode, against +4 HP on a
            # core losing 9 HP/round.
            # Still ABOVE the door: the door is a clearance answer to what
            # stands on our ring and the anatomy's channel is 19/19 the gun
            # shooting the CORE.  Flag off -> False on the first line -> v632
            # behaviour exactly.
            if self._stand_answer_action(ct, p, rnd):
                return
            if self._core_medic(ct, p, rnd):
                return
            # ⭐⭐ s57 THE STAND, ARM 5 -- THE SWARM, CALL SITE 1 of 2.
            # IMMEDIATELY BELOW ARM 4 because the two are the same answer at two
            # prices: arm 4 BUYS a piece that ends the episode, arm 5 spends 2
            # Ti a round when that purchase is unaffordable (which arm 4's own
            # disposition measured at 567 of 604 armed rounds).  Below the medic
            # for arm 4's non-preemption reason, verbatim.  Flag off -> False on
            # the first line -> v632 behaviour exactly.
            if self._stand_swarm_action(ct, p, rnd):
                return
            if SK_DOOR and self._door_action(ct, p, rnd):
                return
            # v601 PLANK 3: an enemy TURRET adjacent to the keeper outranks
            # everything below.  `_door_action`(a) only melees what stands on
            # our own ring; PLANK 1 marches this body at a located annulus
            # gunner, and without this it would arrive and then build a
            # conveyor next to it.
            # ⭐⭐ v632 THE FUNDING PRIORITY, CALL SITE 1 of 2
            # (SK_ROTATE_FUND).  THE KEEPER'S 2 Ti PECK YIELDS while the bank
            # cannot still afford a sentinel -- unless `corefire_fresh` says
            # our core has ACTUALLY LOST HP recently (amendment 2026-08-23,
            # narrowed from the slot-1 presence latch after that latch measured
            # fresh 139/139 at this rung), in which case this rung runs exactly
            # as before.  ⛔ THE
            # REFUSAL FALLS THROUGH, it does not end the turn: the rungs below
            # are heals and clear-outs the keeper should still be doing, and
            # one of them (`_heal_action`) is gated by the same predicate at
            # call site 2.
            # ⭐⭐ s57 SK_DOC_ECO_PUSH -- DEFERRED RUNG 1 of 3 (the 2 Ti peck).
            # In phase 1 this yields to `_route_action`, the terminating belt
            # and `_harvester_action` below, and is re-called at the SAME turn
            # immediately under the general belt.  ⛔ The gate's first term is
            # a module constant, so with the flag off the rung runs exactly as
            # it does today, in the same order, at the same cost.
            if (not self._doc_eco_defer("peck")
                    and not self._fund_refuse(ct, rnd)
                    and self._peck_priority(ct, p, rnd)):
                return
            # ⭐ v618 PLANK 4.  ABOVE the generic heal, and that ordering is the
            # plank: `_heal_action` heals the most-damaged adjacent friendly
            # with NO race arithmetic, so a seat this plank refuses would be
            # healed by the rung below and the DOORWAVE guard would be
            # cosmetic.  Running first lets it publish its veto.
            if self._seat_heal_action(ct, p, rnd):
                return
            # ⭐⭐ v632 THE FUNDING PRIORITY, CALL SITE 2 of 2
            # (SK_ROTATE_FUND).  THE KEEPER'S 1 Ti GENERIC HEAL YIELDS on the
            # same predicate.  ⛔ SCOPED TO THE GENERIC RUNG ONLY: `_core_medic`
            # and `_seat_heal_action` above are NOT gated -- the first answers
            # our own core taking fire and the second is PLANK 4's race
            # arithmetic on a delivery seat, and both are the survival half the
            # `_under_attack` exemption exists to protect.  This rung heals the
            # most-damaged adjacent friendly with no such test, which is what
            # makes it the discretionary one.
            if not self._fund_refuse(ct, rnd) and self._heal_action(ct, p, rnd):
                return
            # ⭐ v610 PLANK 1.  Below the heal (a body about to die outranks a
            # tile) and below `_door_action`/`_peck_priority` (an enemy TURRET
            # on our ring outranks an enemy BARRIER on it), above everything
            # economic -- because a delivery seat an enemy holds is the tile
            # between a harvester and `titanium_collected`, and 180 of the 220
            # enemy barriers on the board at end of game stand on one.
            if self._seat_clear(ct, p, rnd):
                return
            # ⭐ v632 HEIMDALL PLANK 2 -- THE KEEPER'S HALF OF THE DEMOLITION
            # SWEEP, AND ITS PLACEMENT IS THE PLANK'S OWN MEASURED LESSON.
            # ⛔ BELOW EVERY HEAL RUNG (`_core_medic`, `_seat_heal_action`,
            # `_heal_action`) AND BELOW `_seat_clear`, ABOVE THE ECONOMY.  This
            # is the p11 finding paid for in this same session: plank 1.1's
            # citadel dispatch sat ABOVE the keeper's whole ladder, and the
            # readout (`e46p11_*`, coordination 2026-08-22T20:40:28Z) failed
            # Y2 on F1 core-footprint heals 9.60 vs >= 10.6 and Y2b on death
            # cells 21 vs <= 18 -- a keeper that chews zone structures while
            # its own core bleeds loses the game the priority ladder was
            # supposed to win.  Magnus's ladder still reads p1 destroy raiders,
            # p2 destroy their turrets; a dead core loses before any priority
            # pays, so the sweep takes the keeper's turn ONLY when no heal duty
            # and no seat duty fired this round.  THE DENIER IS THE PRIMARY
            # DEMOLISHER (above, in `_ore_denier`); the keeper is the
            # opportunistic second body, which is also what keeps Z4(d) -- the
            # sweep spends the denier's builder-turns, not the economy's.
            # ⭐⭐ s57 SK_DOC_ECO_PUSH -- DEFERRED RUNG 2 of 3 (the sweep).
            # Same reorder, same re-call below the belt.  This rung's own note
            # above already calls the keeper "the OPPORTUNISTIC second body"
            # (the denier is the primary demolisher); in phase 1 an economy
            # that funds the trigger outranks an opportunistic chew.
            if (SK_DEMOLISH and not self._doc_eco_defer("sweep")
                    and self._demolish_action(ct, p, rnd)):
                return
            # ⭐ v613 PLANK 1, THE ACTION HALF.  Above the economy and below
            # every verb that answers a body or a core about to die.  The
            # anatomy's r56 -> r58 sequence on `helheim_B` is the argument for
            # it being above the belt: the tile our conveyor died on became
            # their firing seat two rounds later, and re-laying it as a barrier
            # is the same 3 Ti the belt was going to spend anyway.
            # ⭐⭐ s57 THE PUSH, PIECE 1 -- THE PAIR RESERVE, GATED SITE 1
            # of 10.  Every rung from here down spends titanium on something
            # that is NOT a barrel, and the reserve is the registered claim
            # that the pair outranks all of it while the pair is short.  ⛔ THE
            # RUNG IS UNCHANGED: the gate is a call-site conjunction whose
            # first term is a module constant, so with SK_PUSH False the verb
            # runs exactly as it does today, in the same order, at the same
            # cost.  Each site carries its own key so the readout can say WHICH
            # spend the reserve stopped rather than pooling them.
            # ⭐⭐ s57 SK_DOC_ECO_PUSH -- DEFERRED RUNG 3 of 3 (the apron
            # re-lay).  Same reorder, same re-call below the belt.  Appended
            # AFTER `_push_refuse` so that gate's counters keep their exact
            # meaning on any PUSH-on arm.
            if (not self._push_refuse(ct, rnd, EntityType.BARRIER, "apron")
                    and not self._doc_eco_defer("apron")
                    and self._apron_action(ct, p, rnd)):
                return
            # ⭐⭐ s57 THE KILLBOX, ARM 1, PIECE 1 -- THE EXILE LAUNCHER,
            # ACTION HALF.  IMMEDIATELY ABOVE v611's rung because it is the
            # same verb with an earlier clock: their relay rung 1 lands at r5
            # (Baltsars) and r1 (Mjolnir) and 77-80% of their first bodies
            # arrive by throw, so a launcher bought on v611's r10 funding wait
            # has missed the thing it answers.  BELOW every heal, the door and
            # the counter-peck for v611's own reason, verbatim: each of those
            # is a body or a core about to die, and a building that is one
            # round late is still a building.
            # ⛔ Flag off -> False on the first line -> v632 behaviour exactly.
            # s57 THE PUSH, PIECE 1 -- GATED SITE 2 of 10 (the box's own
            # launcher; SK_KILLBOX ships False, so this gate is inherited by
            # any future arm that turns the box on rather than added then).
            # ⭐⭐ s57 SK_DOCTRINE -- SPEND SUBORDINATION, GATED BOX SITE 1 of 4.
            # Appended AFTER `_push_refuse` so that gate's counters keep their
            # exact meaning on any PUSH-on arm, and its own first term is a
            # module constant, so with SK_DOCTRINE False the rung runs exactly
            # as it does today, in the same order, at the same cost.
            if (not self._push_refuse(ct, rnd, EntityType.LAUNCHER, "box_launcher")
                    and not self._doc_box_refuse(ct, rnd, EntityType.LAUNCHER,
                                                 "box_launcher")
                    and self._kb_launcher_action(ct, p, rnd)):
                return
            # ⭐ v611 SK_HOME_LAUNCHER, OFF by default.  ONE turn, once a game.
            # It sits ABOVE the economy because the collar lands at median r11
            # and a launcher bought at r200 has missed the thing it answers;
            # it sits BELOW the heal, the door and the counter-peck because
            # every one of those is a body or a core about to die, and a
            # building that is one round late is still a building.
            # s57 THE PUSH, PIECE 1 -- GATED SITE 3 of 10.
            if (not self._push_refuse(ct, rnd, EntityType.LAUNCHER, "hl_launcher")
                    and self._home_launcher_action(ct, p, rnd)):
                return
            # ⭐ v610 PLANK 2, THE ACTION HALF.  While a chain is ONE tile from
            # delivering, that conveyor outranks a new harvester: a harvester
            # with no route home is worth exactly zero forever, and 30 of 68
            # alive harvesters on the v609 tape are one build from home.
            # ⭐⭐ THE ROUTE, ARM 1 (SK_ROUTE_HOME) -- THE ACTION HALF, and its
            # placement is the rung immediately above SK_TERM_FIRST because it
            # is SK_TERM_FIRST's own argument carried to a chain that is more
            # than one tile short.  ⛔ OFF: one `if` on a module constant.
            # s57 THE PUSH, PIECE 1 -- GATED SITE 4 of 10.
            if (SK_ROUTE_HOME
                    and not self._push_refuse(ct, rnd, EntityType.CONVEYOR, "route")
                    and self._route_action(ct, p, rnd)):
                return
            # ⭐ s57 THE PUSH, PIECE 1 -- GATED SITE 5 of 10, AND IT IS THE
            # ONE THE ARM IS MOST EXPOSED ON.  A terminating conveyor is the
            # tile between a harvester and `titanium_collected` -- the tree's
            # own founding fact -- and 3 Ti of it is refused here while the
            # pair is unfunded.  ⚠ REGISTERED AND DISCLOSED: "the reserve taxes
            # eco by design" (P5 guard, eco -15% floor).  It is gated and not
            # exempted because the currency is the CHECKMATE, not the delivery.
            if (SK_TERMINATE and SK_TERM_FIRST and SK_BELT
                    and self._route_gaps(ct, rnd)
                    and not self._push_refuse(ct, rnd, EntityType.CONVEYOR, "belt_term")
                    and self._belt_action(ct, p, rnd)):
                # ⚠ s57 SK_HAMMER_PRIO -- LEAK 1, COUNTED AND NOT ARGUED SMALL.
                # This rung is EXEMPT by design (delivery keeps flowing), but it
                # is ENTERED whenever `_route_gaps` is non-empty and then builds
                # the first adjacent PLANNED tile, which need not be the gap
                # tile -- so an extension tile can still be laid here while the
                # inversion is armed.  Read off `hammer_deferring`, which is
                # last round's verdict at this point in the ladder (the gate
                # runs lower down): a DIAGNOSTIC, one round stale by
                # construction, never a control-flow input.
                if SK_HAMMER_PRIO and self.hammer_deferring:
                    self.hammer_term_leak += 1
                return
            # s57 THE PUSH, PIECE 1 -- GATED SITE 6 of 10 (20 Ti x scale,
            # the largest ECO item and the reserve's main donor).
            # ⭐⭐ s57 SK_HAMMER_PRIO -- THE INVERSION, GATED RUNG 1 of 2, AND
            # IT IS THE COMPOSITE'S OWN RISEN COLUMN.  On the six composite
            # lost-kill cells harvesters went 13 -> 22 while barrels standing
            # inside r300 went 1.36 -> 0.39, bank and bodies ample: the
            # eco-ready latch opened the battery CEILING and the build ladder
            # went on ranking a 20 Ti x scale harvester above the battery
            # forever.  While the latch has fired and the pair is short, this
            # rung stands down.  ⛔ THE RUNG IS UNCHANGED -- the gate is a
            # call-site conjunction whose first term is a module constant, so
            # with SK_HAMMER_PRIO False the verb runs exactly as it does today,
            # in the same order, at the same cost.  ⛔ APPENDED AFTER
            # `_push_refuse` so that gate's counters keep their exact meaning
            # on any PUSH-on arm.
            if (not self._push_refuse(ct, rnd, EntityType.HARVESTER, "harv")
                    and not self._hammer_defer(ct, rnd, "harv")
                    and self._harvester_action(ct, p, rnd)):
                return
            # ⭐⭐ s57 THE KILLBOX, ARM 1, PIECE 2 -- THE CORNER CELL, ACTION
            # HALF, AND ITS PLACEMENT IS THE WORD "OPPORTUNISTIC" IN THE
            # REGISTERED DESIGN.  ⛔ BELOW `_route_action`, the terminating
            # belt AND `_harvester_action` -- a harvester with no route home is
            # worth zero on `titanium_collected` forever, and the cell is 6-9
            # Ti of barriers that can wait a round.  ABOVE the seat claim, the
            # home gun and the general belt because the cell only pays while
            # the launcher still has bodies to throw into it, and their raid
            # cadence decays after r150 on two of the three fixtures.
            # ⛔ Flag off -> False on the first line -> v632 behaviour exactly.
            # s57 THE PUSH, PIECE 1 -- GATED SITE 7 of 10 (box, OFF today).
            # ⭐⭐ s57 SK_DOCTRINE -- SPEND SUBORDINATION, GATED BOX SITE 2 of 4.
            if (not self._push_refuse(ct, rnd, EntityType.BARRIER, "box_cell")
                    and not self._doc_box_refuse(ct, rnd, EntityType.BARRIER,
                                                 "box_cell")
                    and self._kb_cell_action(ct, p, rnd)):
                return
            # ⭐⭐ s57 THE KILLBOX, ARM 2, PIECE 1 -- THE EXECUTIONER, ACTION
            # HALF.  ⛔ IMMEDIATELY BELOW THE CELL AND NOWHERE HIGHER: the
            # addendum's rule is CAPACITY BEFORE EXECUTION, and a rung order is
            # where that rule is either kept or quietly broken.  The 30 Ti tube
            # is bought out of arm 1's measured +33.8% eco surplus only after
            # the block stands, and it stays below every economy verb above for
            # the cell's own reason -- a harvester with no route home is worth
            # zero on `titanium_collected` for ever.
            # ⛔ Flag off -> False on the first line -> arm-1 behaviour exactly.
            # s57 THE PUSH, PIECE 1 -- GATED SITE 8 of 10 (box, OFF today).
            # ⭐⭐ s57 SK_DOCTRINE -- SPEND SUBORDINATION, GATED BOX SITE 3 of 4.
            # ⚠ SK_KILLBOX_EXEC ships OFF under the doctrine (see SK_DOC_BOX),
            # so this rung's own first line refuses before the gate is reached.
            # It is gated anyway so that a successor arming the executioner
            # inherits the subordination rather than adding it then.
            if (not self._push_refuse(ct, rnd, EntityType.SENTINEL, "box_exec")
                    and not self._doc_box_refuse(ct, rnd, EntityType.SENTINEL,
                                                 "box_exec")
                    and self._kb_exec_action(ct, p, rnd)):
                return
            # ⭐ v618 PLANK 1, THE ACTION HALF.  JUST BELOW THE
            # HARVESTER-CRITICAL VERBS AND ABOVE THE GENERAL BELT, which is the
            # design's own placement: a harvester with no route home is worth
            # zero forever, but a seat is claimable only while it is still
            # EMPTY and their collar lands at median r11.  The tiles are belt
            # terminus segments with the belt's own facing, so this is not a
            # competing spend -- it is the same 3 Ti, earlier.
            # s57 THE PUSH, PIECE 1 -- GATED SITE 9 of 10.
            if (not self._push_refuse(ct, rnd, EntityType.CONVEYOR, "seat_claim")
                    and self._seat_claim_action(ct, p, rnd)):
                # ⚠ s57 SK_HAMMER_PRIO -- LEAK 2, same shape as leak 1.  The
                # seat claim lays belt-terminus conveyors and is NOT gated: its
                # whole value is claiming a seat BEFORE their collar (median
                # r11) and it is the same 3 Ti the belt would have spent.  If
                # this column is large the next arm gates it; it is not asserted
                # small here.
                if SK_HAMMER_PRIO and self.hammer_deferring:
                    self.hammer_seat_leak += 1
                return
            # ⭐ v618 PLANK 2, THE ACTION HALF.  Below the economy because ONE
            # round late is still a standing gun, and above nothing else: it is
            # a once-a-game purchase inside a bounded window.
            if (not (not SK_PUSH_RES_DEFENCE
                     and self._push_refuse(ct, rnd, EntityType.GUNNER, "home_gun"))
                    and self._home_gun_action(ct, p, rnd)):
                return
            # s57 THE PUSH, PIECE 1 -- GATED SITE 10 of 10 (the general
            # belt).  ⛔ THE THREE HOME-TURRET RUNGS BELOW ARE NOT GATED and
            # that is `SK_PUSH_RES_DEFENCE`: defence sits above the reserve per
            # the registered scope.  ⚠ It is the arm's largest disclosed leak
            # -- 20-30 Ti a piece, above the pair's money -- and the flag
            # exists so an ablation can price it.
            # ⭐⭐ s57 SK_HAMMER_PRIO -- THE INVERSION, GATED RUNG 2 of 2, AND
            # THE GATE IS PER TILE RATHER THAN PER RUNG.  `hammer=True` does
            # not switch the rung off: inside `_belt_action`'s loop a tile this
            # body has never built (`belt_rebuilds == 0`) is an EXTENSION and is
            # skipped, while a REBUILD falls straight through and is laid in the
            # same turn.  That is the registered exemption -- delivery must keep
            # flowing to fund the hammer, and a hammer paid for by stopping
            # delivery is v1 RES's measured self-defeat.
            # ⛔ MODULE CONSTANTS FIRST: with the master off `_hb` is False
            # without a single controller call and `_belt_action` is called with
            # its default, i.e. v632's code on v632's inputs.
            _hb = (SK_HAMMER_PRIO and SK_HAMMER_PRIO_BELT and SK_BELT
                   and self._hammer_defer(ct, rnd, "belt"))
            if (SK_BELT
                    and not self._push_refuse(ct, rnd, EntityType.CONVEYOR, "belt")
                    and self._belt_action(ct, p, rnd, hammer=_hb)):
                return
            # ⭐⭐ s57 SK_DOC_ECO_PUSH -- THE THREE DEFERRED RUNGS, SECOND CALL
            # SITE, AND THIS BLOCK IS WHAT MAKES THE ARM A **REORDER** RATHER
            # THAN A REMOVAL.  Every verb the phase-1 push stood down above is
            # offered the turn again HERE, in the same round, with its own
            # arguments unchanged -- so a round on which no eco rung wanted the
            # keeper's turn behaves exactly as v632 does.  What the arm buys is
            # the ORDER, and the `eco_late_*` counters are the control that
            # proves it: `eco_defer_* > 0` with `eco_late_* == 0` would mean
            # the deferral silently deleted the verb, and that reading is
            # available in the trace rather than argued away.
            # ⛔ ORDER WITHIN THE BLOCK MIRRORS THE LADDER ABOVE (peck, sweep,
            # apron), so the relative rank of the three among themselves is
            # untouched.
            # ⛔ GUARDED BY `_doc_eco_on()` ONLY: with the flag off, or in
            # phase 2, this is one field read and three module-constant tests
            # -- the rungs above already ran, and running them twice is exactly
            # what must not happen.
            if self._doc_eco_on():
                if (SK_DOC_ECO_DEFER_PECK
                        and not self._fund_refuse(ct, rnd)
                        and self._peck_priority(ct, p, rnd)):
                    self.eco_late_peck += 1
                    return
                if (SK_DOC_ECO_DEFER_SWEEP and SK_DEMOLISH
                        and self._demolish_action(ct, p, rnd)):
                    self.eco_late_sweep += 1
                    return
                if (SK_DOC_ECO_DEFER_APRON
                        and not self._push_refuse(ct, rnd, EntityType.BARRIER,
                                                  "apron")
                        and self._apron_action(ct, p, rnd)):
                    self.eco_late_apron += 1
                    return
            # ⭐⭐ v632 HEIMDALL PLANK 3 -- THE TURRET RING (SK_FORT_RING), THE
            # ACTION HALF.  ⛔⛔ BELOW EVERY ECONOMY VERB -- BELOW
            # `_harvester_action` AND BELOW `_belt_action` -- AND THAT
            # PLACEMENT IS THE REDESIGN.  The first attempt put this rung ABOVE
            # the economy (disclosed as deviation 1 in its build report) and
            # the screen refused it on the pre-registered ECONOMY fences and on
            # nothing else: eco-sum -24.8% against a -12% bar and
            # harvesters-built -20.3% against -10%, while every dose bar was
            # crushed (intruder kills +187%, r1 ammo bank 90/90, ring stands
            # 87/90) and survival rose for the fourth consecutive arm
            # (alive-sum 51).  The measured mechanism is TURRET-FOR-BELT
            # SUBSTITUTION, not overspend: turrets at r120 +30-70% while
            # conveyors and harvesters fell 20-30% at ~flat total spend -- i.e.
            # the ring was taking the KEEPER'S TURN the belt wanted, exactly
            # the scarcity this tree names in `main.py:16` ("THE KEEPER'S TURN
            # IS THE SCARCE RESOURCE").  A titanium reserve cannot price a
            # turn, so the fix is the ladder, not the constant.
            # ⇒ The ring now buys only out of a round in which no heal duty, no
            # seat duty, no harvester and no belt build wanted the turn.  It
            # sits beside `_cover_gun_action` and just below `_home_gun_action`
            # -- the same rung every other once-a-game turret purchase in this
            # tree occupies, which is where they were priced.
            # ⚠ THE COST IS REAL AND IS REPORTED, NOT HIDDEN: the ring lands
            # LATER than the prediction clock wants (their ladder r1-r5, first
            # our-half plant median r5, collar median r11).  A later ring is
            # the price of an economy that still exists to defend.
            if (SK_FORT_RING
                    and not (not SK_PUSH_RES_DEFENCE
                             and self._push_refuse(ct, rnd, EntityType.SENTINEL,
                                                   "fort_ring"))
                    and self._fort_ring_action(ct, p, rnd)):
                return
            if (not (not SK_PUSH_RES_DEFENCE
                     and self._push_refuse(ct, rnd, EntityType.GUNNER, "cover_gun"))
                    and self._cover_gun_action(ct, p, rnd)):  # v601 PLANK 2
                return
        self._home_keeper_move(ct, p, rnd)
        # ⭐ v632 SURVIVAL FAMILY -- WORK AT A HELD POST (SK_KEEPER_WORK).
        # ⛔ TERMINAL, AND THAT IS THE WHOLE SAFETY ARGUMENT: it runs after the
        # entire action ladder above AND after the whole movement layer, so it
        # cannot pre-empt a single existing rung and it cannot touch a selector,
        # a walk target or a step.  `_keeper_work` re-reads the engine to
        # establish that this body neither acted nor moved this round before it
        # emits anything (`sk_roles.py`, the method below), so on any round the
        # tree already did something this call is a no-op.
        if SK_KEEPER_WORK:
            self._keeper_work(ct, p, rnd)

    def _keeper_work(self, ct, p, rnd):
        """SK_KEEPER_WORK: emit a heal on a round the held post emitted nothing.

        GAME CONTEXT: an in-engine builder action in the Florent Code League, a
        sandboxed bot-vs-bot programming competition.  `heal` is the engine's
        1 titanium -> +4 HP verb on an orthogonally adjacent tile; it heals ALL
        friendly entities standing on that tile.

        ⛔⛔ THE PRECONDITION IS READ OFF THE ENGINE, NOT ASSUMED FROM THE CALL
        SITE.  Two reads, and each closes a different hole:
          * `get_action_cooldown() == 0` -- a verb was emitted this round (or the
            ladder never ran because the cooldown was already busy).  Either way
            this rung must be silent, and this is also the legality gate: a
            builder that acted cannot act again.
          * `get_position() == p` -- this body MOVED this round.  The registered
            falsifier for this plank is any movement delta inside a hold, so the
            rung refuses to emit on a round the body moved rather than trusting
            that the movement layer returned quietly.
        A body that neither acted nor moved has a turn worth exactly zero, which
        is the only state this plank claims.

        THE SPEND CAP is documented in full at the flag (`sk_maps.py`,
        SK_KEEPER_WORK).  In one line: the FULL-VALUE heal (>= 4 missing) is
        reachable only in `_heal_action`'s complement -- a bank of 0 or 1, where
        1 titanium buys nothing else in the game -- and every other class pays
        SK_MEDIC_TI_FLOOR, the floor `_core_medic` already uses for the same
        1 titanium verb.
        """
        try:
            if ct.get_action_cooldown() != 0:
                return False
            here = ct.get_position()
            if here.x != p.x or here.y != p.y:
                return False
            bank = ct.get_global_resources()
        except Exception:
            return False
        self.kw_holds += 1
        if bank < 1:
            return False                # cannot afford the 1 Ti heal at all
        foot = core_tiles_xy(self.core) if self.core is not None else ()
        best = None                 # (key, q, on_core, partial, bot, reachable)
        for d in CARDINALS:
            q = p.add(d)
            if not self.ibp(q):
                continue
            xy = (q.x, q.y)
            # v618 PLANK 4's VETO, verbatim from `_heal_action`: a seat that
            # plank refused this round must not be healed by a rung underneath
            # it.  Flag off => `seat_heal_veto` is empty and this is a no-op.
            if SK_SEAT_HEAL and xy in self.seat_heal_veto:
                continue
            bld_miss = 0
            bot_miss = 0
            try:
                bid = ct.get_tile_building_id(q)
                if bid is not None and ct.get_team(bid) == self.team:
                    bld_miss = ct.get_max_hp(bid) - ct.get_hp(bid)
            except Exception:
                continue
            # ⛔ THE ONE CLASS `_heal_action` STRUCTURALLY CANNOT REACH: it keys
            # on `get_tile_building_id`, so a damaged friendly BUILDER BOT --
            # which is a unit and not a building -- is never healed by this
            # tree, at any bank.  `heal(pos)` heals every friendly on the tile,
            # so the same verb covers it with no new engine capability.
            try:
                uid = ct.get_tile_builder_bot_id(q)
                if uid is not None and ct.get_team(uid) == self.team:
                    bot_miss = ct.get_max_hp(uid) - ct.get_hp(uid)
            except Exception:
                pass
            miss = bld_miss if bld_miss > bot_miss else bot_miss
            if miss <= 0:
                continue
            # RANK 0 = full-value (nothing overflows), RANK 1 = partial.  The
            # ranks carry DIFFERENT floors, so they are ordered rather than
            # merged: a full-value heal outranks a partial one at equal damage.
            rank = 0 if miss >= 4 else 1
            key = (rank, -miss)
            if best is None or key < best[0]:
                # `reachable` = would `_heal_action` (`sk_roles.py:1716`) target
                # this tile at a sufficient bank?  It requires a BUILDING id and
                # >= 4 missing, so that predicate is exactly `bld_miss >= 4`.
                best = (key, q, xy in foot, rank == 1, bot_miss > 0,
                        bld_miss >= 4)
        if best is None:
            return False
        _key, q, on_core, partial, has_bot, reachable = best
        # THE FLOOR, AND IT KEYS ON REACHABILITY RATHER THAN ON THE TARGET'S
        # SHAPE.  A tile `_heal_action` would have taken at a bank of >= 2 is
        # this rung's COMPLEMENT: it can only be standing here at a bank of 0 or
        # 1, where 1 titanium buys nothing else in the game, so its floor is the
        # verb's own price and the cap is self-limiting.  Every other tile --
        # a partial (1..3 missing) heal, or a damaged friendly BUILDER BOT that
        # no rung in this tree reaches at ANY bank -- is genuinely
        # discretionary, so it pays `_core_medic`'s floor verbatim.
        if not reachable and bank <= SK_MEDIC_TI_FLOOR:
            self.kw_held += 1
            return False
        # THE SK_ROTATE_FUND STAND-DOWN, called LAST and only with a real target
        # in hand, so `fund_verb_held` counts the refusal of a verb rather than
        # a third blind tick per keeper round.  This IS the "keeper
        # discretionary 1-2 Ti verb" class that gate was written for.
        if self._fund_refuse(ct, rnd):
            self.kw_held += 1
            return False
        try:
            if not ct.can_heal(q):
                return False
            ct.heal(q)
        except Exception:
            return False
        self.kw_heals += 1
        if on_core:
            self.kw_heals_core += 1
        if partial:
            self.kw_partial += 1
        if has_bot:
            self.kw_bots += 1
        return True

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
            # ⭐⭐ s57 SK_DOC_ECO_PUSH (a) -- THE WIDENED ORE FENCE.  With the
            # flag off `_doc_ore_ok` IS `is_home_half`, evaluated in the same
            # place, so this line is character-for-character equivalent on an
            # OFF arm.  See `_doc_ore_ok` for why the added clause is a HOME
            # fence and why the threat leash still binds on top of it.
            if not self.ibp(q) or not self._doc_ore_ok(q):
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
            # ⛔⛔ v632 PLANK 5's R5 GATE (slot 4), AND IT IS THE ONE GATE THAT
            # SITS AT THE WSTORE RATHER THAN AT THE TOP OF THE RUNG.  The BUILD
            # above is exactly what the second eco body exists to do, so it
            # must run for every role; only the PUBLISH is role-0's.  The write
            # is a read-modify-write of a monotone ratchet
            # (`if len(...) > n`), which is precisely the shape the buffered
            # store loses silently: both bodies would read LAST round's word
            # and the loser's increment would be dropped, permanently, because
            # nothing re-attempts it.
            # ⚠ DISCLOSED: with the gate, slot 4 counts the KEEPER's own
            # harvesters, so `_fort_harv_live` (PLANK 3's SK_FORT_RING_HARV_MIN
            # floor) reads LOW when the second body built them.  Conservative
            # in the only direction that matters -- it delays a ring buy, it
            # never licenses one on a dead economy.  See the SK_FORT_WALKER_ECO
            # flag note in sk_maps.
            if self.role == SK_HOME_KEEPER:
                n = ct.read_store(SK_SLOT_HARV)
                if len(self.harv_tiles) > n:
                    self.wstore(ct, SK_SLOT_HARV, len(self.harv_tiles))
            else:
                self.eco_pub_blocked += 1
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
        # ⛔⛔ v632 PLANK 5's R5 GATE (slot 14).  This rung is reachable from
        # `_home_keeper`, and under SK_FORT_WALKER_ECO a SECOND body runs that
        # turn.  Two writers of one slot in one round is a SILENT LOST UPDATE
        # (writes are buffered, so both read last round's word), measured at
        # 291 frozen rounds on the tube beat.  The gate is on the ROLE, which
        # this plank deliberately does not change, so the keeper's behaviour
        # is bit-identical and the second body publishes nothing.  Inert while
        # the flag is OFF: nothing but role 0 ever calls this today.
        if self.role != SK_HOME_KEEPER:
            self.eco_pub_blocked += 1
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
        # ⛔ v632 PLANKS 8+9, HAZARD (d) -- NO BAND RE-PLAN AT THE FLIP.  Study
        # §8a hazard 4: "the keeper re-plans on a changed `self.enemy` key and
        # should not re-route a working belt at r300.  Worth an explicit
        # `rnd < SK_PHASE_ROUND` guard on band re-planning."  Dropping the enemy
        # anchor from the key at and after the flip is that guard, expressed
        # where the re-plan is actually triggered.
        # ⚠ DISPOSITION, MEASURED RATHER THAN ASSERTED: in THIS tree the hazard
        # does not bind.  SK_BELT_BAND_AVOID/_DROP are unconditional (not
        # phase-gated), so the band is already live in phase 1 and nothing about
        # it changes at r300; and `_resolve_enemy` is WRITE-ONCE (`if
        # self.enemy is None`), so the anchor cannot change mid-game either.
        # The guard is therefore a no-op today and is shipped as a FENCE against
        # a successor making the band phase-conditional -- at which point the
        # keeper would re-route a working belt on the exact round the raiders
        # leave.  It is deliberately NOT a freeze of the whole plan: harvester
        # deaths, belt bans and newly sensed walls must still re-plan, or the
        # belt stops being repaired for the last 700 rounds of the game.
        _band_key = None if self.rot_on else self.enemy
        key = (self.core, _band_key, len(self.harv_tiles), len(self.belt_ban),
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
        # ⭐ v632 PLANK 7, HALF 2 -- THE MESH, AND IT IS THE LAST THING THAT
        # TOUCHES `plan`.  It reads the finished tree for its adjacency test,
        # so a mesh tile can never become somebody's parent and no chain's
        # length, facing or termination changes.  Flag off: returns before the
        # first read (`plan` untouched, `mesh_tiles` stays the empty set from
        # `__init__`, every downstream membership test answers as it did).
        self._apron_mesh(ct, plan)
        self.belt_plan = plan

    def _apron_mesh(self, ct, plan):
        """⭐⭐ v632 HEIMDALL PLANK 7, HALF 2 -- THE CORE-APRON MESH (§4d).

        Magnus's Bean-counters observation as a plan mutation: the extra
        conveyors that wall a core's exposed faces are PAYING infrastructure
        doing triple duty -- belt-cut redundancy, plant-tile denial and fire
        occlusion -- at +1% scale each, where a barrier is deadweight at the
        same 3 Ti.

        Filters, in the order they run below:
          (b) faces a core FOOTPRINT tile (`_seat_face`), i.e. it is a TERMINAL
              conveyor that delivers rather than a stub;
          (c) UNOCCUPIED;
          (d) apron member, buildable terrain, not banned, not escalated;
          (e) the spawn reserve (`SK_APRON_MESH_SPAWN_RESERVE`).

        ⛔⛔ §4d's CLAUSE (a) -- "cardinal-adjacent to an already-planned belt
        tile" -- IS DROPPED, ON A REGISTERED AMENDMENT (pre-tape, at the
        expectation doc's tail), AND THE PROVENANCE IS THIS PLANK'S OWN BUILD
        MEASUREMENT.  It was implemented as specified first and instrumented
        with a per-seat reason histogram over 3 f1 cells
        (`scratchpad/s58_p7/diag/*.log`, 2026-08-22):

            helheim  r=3  2,7:inplan 3,7:TAKEN 4,8:notadj 4,9:notadj
                          2,10:notadj 3,10:notadj 1,8:notadj 1,9:notadj

        SIX OF EIGHT SEATS READ `notadj` IN EVERY RE-PLAN OF EVERY CELL, and
        the total dose was ONE TILE ACROSS THREE CELLS.  The mechanism is
        structural, not incidental: the trunk arrives at ONE core face, and
        footprint tiles are never in `plan` (the BFS starts from them), so a
        seat touching only the core can never satisfy (a).  Clause (a) serves
        the BELT-CUT REDUNDANCY duty and structurally defeats the other two
        §4d names -- PLANT-TILE DENIAL and FIRE OCCLUSION -- because both want
        the faces the trunk does not use.  ⇒ It cannot reproduce the thing
        Magnus actually observed: ten conveyors WALLING THE EXPOSED FACES.
        The population is now the eight seats, gated by (b)-(e).

        ⛔ (b) IS ALSO THE POPULATION, AND IT IS A SMALLER SET THAN §4d SAYS.
        A conveyor outputs to ONE cardinal neighbour, so "faces a footprint
        tile" is the same predicate as "orthogonally adjacent to the footprint"
        -- i.e. `core_seats()`, exactly EIGHT tiles.  The study's "~6-10 extra
        tiles on a 20x20" is an over-count; the ceiling is 8 minus the seats
        the belt plan already terminates on, and `SK_APRON_MESH_MAX` is a fence
        on top of that rather than the binding number.

        ⛔ NO NEW BUILD VERB.  The tiles enter `belt_plan` and are therefore
        priced, walked to, laid, watched, repaired and re-planned by exactly
        the machinery that owns every other planned tile.  That is the point of
        putting them here rather than in a rung of their own: a new rung would
        compete for the keeper's turn, which is the scarce resource in this
        tree (`main.py:16`), and PLANK 3's redesign is what that costs.

        ⚠ WITH (a) GONE, THE SPAWN RESERVE IS THE ONLY THING BETWEEN THE MESH
        AND OUR OWN CORE'S SPAWN LOOP.  It was already mandatory; it is now
        LOAD-BEARING, because the unfiltered population includes all four
        anchor-adjacent seats.  Do not weaken it without re-reading
        `sk_maps.py:4121`.
        """
        if not SK_APRON_MESH or self.core is None or not plan:
            return
        foot = set(core_tiles_xy(self.core))
        apron = set(self._apron_list())
        # ⛔⛔ THE SPAWN RING -- THE TILES `_spawn_plan` ACTUALLY OFFERS THE
        # CORE, AND THE ONLY TILES THE RESERVE HAS ANY BUSINESS REFUSING.
        # `_spawn_plan` (`sk_core.py:450`) walks `p.add(d)` over the 8
        # DIRECTIONS FROM THE ANCHOR, so this set is exactly its candidate
        # list minus the footprint.  FOUR of the eight delivery seats sit
        # inside it; the other four cannot change the count no matter what is
        # built on them.
        ring = set()
        for dx, dy in NEIGHBOURS8:
            x2, y2 = self.core.x + dx, self.core.y + dy
            if self.ib(x2, y2) and (x2, y2) not in foot:
                ring.add((x2, y2))
        taken = set()

        def _spawn_free():
            """Anchor-adjacent tiles still spawnable once `taken` is built on.

            ⛔ `plan` COUNTS AS TAKEN TOO.  The hazard is the STATE the mesh
            leaves behind, not the marginal tile: a belt that already
            terminates on one anchor seat plus three mesh tiles is the same
            self-inflicted spawn lock as four mesh tiles.  Counting both is the
            conservative direction and it is the direction that cannot cost us
            a replacement body.
            """
            free = 0
            for dx, dy in NEIGHBOURS8:
                x2, y2 = self.core.x + dx, self.core.y + dy
                if not self.ib(x2, y2) or (x2, y2) in foot:
                    continue
                if (x2, y2) in taken or (x2, y2) in plan:
                    continue
                try:
                    if ct.is_tile_empty(Position(x2, y2)):
                        free += 1
                except Exception:
                    continue          # unreadable: NOT counted as free
            return free

        for xy in core_seats(self.core):
            if len(taken) >= SK_APRON_MESH_MAX:
                break
            if xy in plan or xy in foot:
                continue                      # the belt already wants it
            x, y = xy
            if not self.ib(x, y) or xy not in apron:
                continue
            if self.wall_at(x, y):
                continue
            # ⛔ NEVER ON ORE.  A conveyor on an ore tile consumes a harvester
            # seat permanently, and `_harvester_action` already denies that
            # tile with a building that also EARNS.  Same rule as
            # `_claim_targets` and `_apron_buildable`.
            if self.ore_at(x, y) or xy in self.harv_tiles:
                continue
            if xy in self.belt_ban or xy in self.belt_escalated:
                continue
            face = self._seat_face(xy)        # (b)
            if face is None:
                continue
            # ⛔ §4d's clause (a) STOOD HERE (cardinal-adjacent to an already-
            # planned belt tile) and is dropped on the registered amendment --
            # see the docstring for the histogram that refused it: 6 of 8 seats
            # `notadj` in every re-plan, dose 1 tile in 3 cells, and the two
            # duties it defeats are the two the wall is FOR.
            # (c) UNOCCUPIED, and an UNSEEN tile is not an occupied tile -- the
            # planner is deliberately optimistic everywhere else for the same
            # reason (`_belt_watch` is the refutation half).  Bounds first,
            # then vision: `is_in_vision` is a pure radius test with NO bounds
            # check (CLAUDE.md, corrected s50), and `self.ib` above is the
            # bounds test.
            q = Position(x, y)
            try:
                if ct.is_in_vision(q) and not ct.is_tile_empty(q):
                    continue
            except Exception:
                pass
            taken.add(xy)                     # (e) is evaluated WITH this tile
            # ⛔⛔ (e) BINDS ON IN-RING CANDIDATES ONLY -- REGISTERED FIX, AND
            # THE PROVENANCE IS THIS PLANK'S OWN HISTOGRAM.  The first cut ran
            # the reserve on every seat, which asks "are N spawn tiles free
            # AFTER this addition" of tiles whose addition cannot change the
            # answer.  Measured over the 3 f1 smoke cells post-amendment
            # (`scratchpad/s58_p7/diag2/*.log`, 2026-08-22): **114 reserve
            # refusals, 62 of them (54%) on seats OUTSIDE the spawn ring** --
            # and on stavkirke it read `free=0` on all eight seats in all ten
            # re-plans, suppressing the plank to **ZERO tiles** on a cell where
            # four of the seats were never the core's to spawn on.  A
            # pre-existing `free=0` is not the mesh's doing; the guard's SENTENCE
            # said "after the addition" while its PURPOSE is "the mesh must not
            # CAUSE a spawn lock", and only in-ring candidates can.
            # ⚠ THE GUARD IS NOT WEAKENED WHERE IT MATTERS: every tile that can
            # consume a spawn candidate is still checked with `taken` and `plan`
            # counted against it, which is the whole of the musical-chairs
            # hazard at `sk_maps.py:4131`.
            if xy in ring and _spawn_free() < SK_APRON_MESH_SPAWN_RESERVE:
                taken.discard(xy)
                self.mesh_spawn_refused += 1
                continue
            plan[xy] = face
        self.mesh_planned += len(taken - self.mesh_tiles)
        self.mesh_tiles = taken

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
        # ⭐ v632 PLANK 7, HALF 1 -- THE MASTER TAKES THIS SITE WITHOUT
        # TOUCHING `SK_APRON_BELT_PREF`'s OWN CONSTANT.  DISCLOSED: the
        # sub-flag keeps the value and the meaning its own s55 screen measured
        # (ON alone: F1 by-r300 9 vs 11, 8 of 12 named cells moved); the OR
        # here is what lets PLANK 7 own the routing half as part of the mesh
        # while leaving the sub-flag independently ablatable in both
        # directions.  ⛔ THE CONJUNCTION WITH `SK_APRON_DENY` IS DELIBERATE
        # AND UNCHANGED: the apron SET is that plank's, so the tie-break can
        # only exist where the apron is defined.
        apron = None
        if (SK_APRON_DENY and (SK_APRON_BELT_PREF or SK_APRON_MESH)
                and self.core is not None):
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

    def _belt_action(self, ct, p, rnd, hammer=False):
        """SK_BELT -- lay or repair the planned belt on an adjacent tile.

        LEDGER V1 (the most expensive bug in the study: sixteen rebuilds of one
        conveyor at 6-round intervals into a stationary gun): a tile rebuilt
        SK_REBUILD_ESCALATE times WITHOUT SURVIVING stops being rebuilt and
        becomes a locate-the-shooter task.  Rebuild #4 never happens.

        ⭐⭐ s57 SK_HAMMER_PRIO: `hammer` is the EXTENSION/REPAIR fork and it
        is passed by exactly ONE of this method's two call sites (the general
        belt rung).  The SK_TERM_FIRST rung above never passes it, because that
        rung is entered only while `_route_gaps` is non-empty -- an ALREADY
        BUILT harvester whose chain is short of home -- and completing that
        chain adds no productive capacity, it makes capacity we already bought
        deliver.  ⛔ THE DEFAULT IS THE OFF IDENTITY: with the argument absent
        the loop below is v632's, line for line.
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
            # ⭐⭐ s57 SK_HAMMER_PRIO -- THE EXTENSION/REPAIR FORK, AND IT SITS
            # HERE BECAUSE `n` IS ALREADY THE ANSWER.  `belt_rebuilds[t]` is
            # this rung's own count of OUR builds on that tile and it is never
            # decremented, so n == 0 is a FIRST-EVER build (new delivery
            # capacity: EXTENSION) and n >= 1 is a rebuild of a route we already
            # laid (REPAIR).  No new memory, no second classifier.
            # ⛔ PLACED AFTER the escalate ledger and before the engine calls, so
            # a deferred tile costs one dict lookup and no controller call, and
            # the rung CONTINUES rather than returning -- a repair tile on the
            # next cardinal is still laid this turn.
            # ⚠ `belt_rebuilds` is PER BODY (disclosed in SK_HAMMER_PRIO's
            # note): a successor keeper's first build on an inherited-and-lost
            # tile reads as EXTENSION.  Both verdicts are counted so the readout
            # can show the split rather than assert it.
            if hammer:
                if n == 0:
                    self.hammer_belt_ext += 1
                    continue
                self.hammer_belt_rep += 1
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
        # ⛔⛔ v632 PLANK 7's ONE FENCE, AND IT EXISTS SO THE MESH CANNOT
        # SMUGGLE A REFUTED PLANK BACK IN.  A mesh tile is a DELIVERY SEAT, and
        # pecking an enemy building off a delivery seat is `SK_SEAT_CLEAR`'s
        # verb -- built, mechanism-confirmed and SHIPPED OFF (`sk_maps.py:1350`)
        # after v603 measured the unbounded form at 2,179 pecks.  Without this
        # line, adding eight seats to `belt_plan` would hand that verb back to
        # `_belt_evict` under a different name and with no seat budget at all,
        # and PLANK 7 would be scored with SEAT_CLEAR riding along inside it.
        # The mesh's claim is on EMPTY tiles; a tile they already hold is not
        # its business.  ⚠ FLAG OFF: `mesh_tiles` is empty for the whole game,
        # so this is a membership test against an empty set on every call and
        # the branch below is reached exactly as it was.
        if not mine and (q.x, q.y) in self.mesh_tiles:
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
        # ⭐ s57 THE STAND, arm 3.  The FULL ranked list is memoised beside the
        # truncated one: `_seat_walk` (the aim, and the thing v603's bound was
        # measured on) keeps reading the top N, while `_seat_clear` may read
        # all of it under SK_SEAT_CLEAR_ADJ.  Written below the master's own
        # early return, so a SK_SEAT_CLEAR-off tree never touches it.
        self._seat_all = cand
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
        targets = self._seat_targets(ct, rnd)
        # ⭐ s57 THE STAND, arm 3 -- THE ACTION HALF SEES EVERY ENEMY-HELD SEAT,
        # THE WALK HALF STILL SEES ONLY THE TOP N.  `dsq_core` is 1 for all
        # eight seats, so the sort has no tie-break below rank and the N=2
        # truncation keeps a FIXED pair of tiles wherever this body stands:
        # traced at 320 of 750 adjacent-seat rounds (42.7%; 288/420 on
        # jotunheim_seatA) where every seat the body was standing beside had
        # already been dropped before adjacency was tested.  A peck at a tile
        # the body is ALREADY beside costs no step, and SK_SEAT_PECK_CAP and
        # SK_SEAT_PECK_TOTAL still bound the volume unchanged.  Full argument
        # and the ablation at SK_SEAT_CLEAR_ADJ (sk_maps.py).
        if SK_SEAT_CLEAR_ADJ:
            targets = self._seat_all
        for (_rank, _d, xy, bid, _et) in targets:
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

    def _gun_bears(self, ct, q, sentinel_only=False):
        """True if a live turret of OURS can fire on tile q AS IT NOW FACES.
        sentinel_only=True restricts the claim to OUR SENTINELS (iteration 7:
        a bearing gunner is not an answer to a sentinel shooter).

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
            if sentinel_only and et != EntityType.SENTINEL:
                continue
            try:
                face = ct.get_direction(eid)
                if ct.can_fire_from(ep, face, et, q):
                    return True
            except Exception:
                continue
        return False

    # --- PLANK 1 -- SK_SEAT_CLAIM ---------------------------------------

    def _claim_spawn_ok(self, ct, q, reserve=None):
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
        # ⭐ s57 THE KILLBOX reuses this guard with its OWN bar rather than
        # copying the twelve lines above -- this tree has already paid once for
        # two clamps that had to stay in step forever (`cheb_core`'s note).
        # `reserve=None` is the shipped default and the shipped constant, so
        # every pre-KILLBOX call site is byte-identical.
        return free >= (SK_SEAT_CLAIM_SPAWN_RESERVE if reserve is None
                        else reserve)

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

    # ==================================================================
    # v632 HEIMDALL PLANK 3 -- THE TURRET RING (SK_FORT_RING)
    # ==================================================================
    # GAME CONTEXT: in-engine purchases for the Florent Code League, a
    # sandboxed bot-vs-bot competition.  "raider"/"intruder" = a competing
    # bot's builder piece standing inside our own core annulus.
    #
    # DOCTRINE: PROGRAMME.md `CITADEL_WEAPON: turret_ring` (Magnus s57
    # 2026-08-22; the launcher taxi was put to him and REFUSED).  Design study
    # `docs/research/DESIGN-fortress-heimdall-2026-08-22.md` §5b: the ring is
    # THREE turrets covering LANES, not a blanket over Chebyshev-3 -- one
    # SENTINEL on the core-to-core axis lane and SK_FORT_RING_GUNNERS flank
    # gunners.  §5a's machinery (`_home_gun_window/_score/_action/_walk`) is
    # REUSED here rather than re-derived; SK_HOME_GUNNER's own flag stays
    # False so its measured history stays attached to its own arm.
    #
    # ⛔ THE BUILDER IS A HOME BODY.  The study's "engineer's fortress duty" is
    # NOT re-homed in this tree (that is plank 1's family and it is parked), so
    # the ring is bought by the HOME KEEPER, whose leash (SK_KEEPER_LEASH,
    # ADOPTED) already holds it near the core -- and every ring site is inside
    # the apron / SK_FORT_RING_SENT_DSQ of our own footprint, i.e. inside the
    # leash's own fence.  The two do not fight; disclosed in the build report.

    def _fort_ring_next(self):
        """What the ring still owes, in BUY ORDER -- axis SENTINEL first.

        Sentinel first because it is the highest-value single turret in the
        design (study §5b item 1): its site is fixed AND the approach direction
        is fixed, its line IGNORES OBSTACLES so our own apron mesh cannot block
        it, and it reaches r^2=32 where a gunner reaches 13.  It is also the
        one that cannot be re-aimed later -- a sentinel cannot rotate -- so it
        should be placed while the lane is still empty.
        """
        if self.fort_sents < SK_FORT_RING_SENT:
            return EntityType.SENTINEL
        if self.fort_guns < SK_FORT_RING_GUNNERS:
            return EntityType.GUNNER
        return None

    def _fort_harv_live(self, ct):
        """OUR live harvester count, as this body knows it.

        ⛔ THE CENSUS IS `harv_tiles` AND THE CHOICE IS DISCLOSED, INCLUDING
        WHICH WAY IT IS WRONG.  Three censuses were available:
          (a) `len(self.harv_tiles)` -- CHOSEN.  ZERO engine calls.  It is the
              HOME KEEPER's own build ledger, maintained by the same body that
              buys the ring: a tile is added by `_harvester_action` on a
              successful build and DROPPED by `_harv_watch` when this body can
              SEE the tile is empty.  It is also the exact set the global belt
              plan routes trunks to, so "2 harvesters" here means the same two
              things the economy means.
          (b) `ct.read_store(SK_SLOT_HARV)` -- REJECTED.  Slot 4 is documented
              as a MONOTONE RATCHET (`sk_maps.py:2335`): it never falls when a
              harvester dies, so a bot whose harvesters were all killed would
              still read its high-water mark and buy turrets on an economy that
              no longer exists.  That is the exact failure this gate exists to
              prevent, and it is also a round stale (writes are buffered).
          (c) a live count over `self.vis_friend` -- REJECTED as strictly worse
              than (a) for the same price: it sees only d^2 <= 20 of this body,
              so a harvester across the home half reads as dead.
        STALENESS, BOTH DIRECTIONS, because a gate whose error direction is
        unstated is not a gate:
          * OVER-COUNT (fails toward ALLOWING the buy): a harvester killed
            outside the keeper's vision stays in the set until this body walks
            within d^2 <= 20 of the tile and `_harv_watch` reads it empty.
            `_harv_watch` also needs SK_HARV_ESCALATE, which is ON.
          * UNDER-COUNT (fails toward REFUSING the buy): a REPLACEMENT keeper
            starts from an empty set and re-learns nothing -- it only ever adds
            tiles it builds itself.  So after a keeper death the ring can be
            gated shut for the rest of the window.
        The under-count direction is the safe one for this plank (it protects
        the economy, which is what the gate is for) and the over-count is
        bounded by the keeper being the body that stands at home.

        ⛔⛔ SEMANTICS CORRECTED PRE-SCREEN (builder, registered in the p3R
        addendum): the floor reads harvesters BUILT (the slot-4 monotone
        ratchet) rather than the live set above -- the live census's two
        smokes measured our tree holding ~ONE live harvester under fire, so
        an ALIVE floor is OPPONENT-CONTROLLABLE: killing our harvester locks
        our weapon off exactly when it is needed (ring stood 3/10 vs 87/90).
        The ratchet's own danger (buying turrets on a dead economy), which
        the original rejection above correctly named, is now neutralized
        STRUCTURALLY by the ladder demotion: _harvester_action outranks the
        ring rung, so a keeper with dead harvesters rebuilds before it can
        ever reach a ring buy.  Ratchet is one round stale -- a threshold
        that only rises tolerates that.  The rejected-text above is kept as
        the record of the argument this correction answers.
        """
        try:
            return ct.read_store(SK_SLOT_HARV)
        except Exception:
            return 0

    def _fort_ring_window(self, ct, rnd):
        """The buy window, as ONE predicate so the action and the walk cannot
        disagree -- the launcher arm's lesson ("do not walk at a buy we cannot
        make"), applied before it can bite.

        ⭐⭐ THE REDESIGN'S SECOND CHANGE LIVES HERE: the ring may not be bought
        (or WALKED AT) until the economy has started -- SK_FORT_RING_HARV_MIN
        live harvesters.  It is in the WINDOW rather than in `_fort_afford` so
        that the walk half is gated by the same predicate as the buy; a keeper
        walking toward a turret site it may not buy is the v610 cost in a new
        hat, and under the refused arm's own diagnosis (turret-for-belt
        SUBSTITUTION of the keeper's turn) a wasted walk is the same currency
        as a wasted build.
        """
        if not SK_FORT_RING or self.core is None:
            return False
        lo, hi = SK_FORT_RING_WINDOW
        if rnd < lo or rnd > hi:
            return False
        if self._fort_harv_live(ct) < SK_FORT_RING_HARV_MIN:
            return False
        return self._fort_ring_next() is not None

    def _fort_afford(self, ct, kind):
        """⛔ THE R2 DEFENCE (study §7 R2).  Scale cost is REAL on this plank --
        it is the first PURCHASING plank of the Heimdall line and every turret
        is +20% on the ONE GLOBAL ADDITIVE factor, inflating every later build
        of every type.  Three planks have died to that surcharge landing before
        the economy could pay it, so no ring turret is ever bought out of the
        last SK_FORT_RING_RESERVE titanium.
        """
        try:
            if kind == EntityType.SENTINEL:
                cost = ct.get_sentinel_cost()
            else:
                cost = ct.get_gunner_cost()
            return ct.get_global_resources() >= cost + SK_FORT_RING_RESERVE
        except Exception:
            return False

    def _fort_price(self, ct, kind):
        """The scaled price of the next ring turret -- `_fort_afford`'s own two
        getters, exposed so the war chest can add the purchase's own cost to
        its reserve without a second copy of the kind->getter mapping.

        ⛔ 0 ON AN UNREADABLE COST, which weakens the chest test to "two
        sentinels" rather than strengthening it: a refusal is never manufactured
        out of a failed read.  `_chest_refuse` fails open for the same reason.
        """
        try:
            if kind == EntityType.SENTINEL:
                return ct.get_sentinel_cost()
            return ct.get_gunner_cost()
        except Exception:
            return 0

    def _fort_axis(self, q):
        """(signed cross, |axis|^2, forward dot) of tile q about the
        our-core -> enemy-core axis, or None if the axis is undefined.

        Integer-exact: the perpendicular distance of q from the lane is
        |cross| / sqrt(d2), so a lane budget of L tiles is the integer test
        `cross*cross <= L*L*d2` with no floating point anywhere.  The SIGN of
        the cross is the FLANK, which is what keeps the two gunners on
        opposite sides of the corridor (Magnus's ring covers the axis
        symmetrically -- no favoured flank).
        """
        if self.core is None or self.enemy is None:
            return None
        ax = self.enemy.x - self.core.x
        ay = self.enemy.y - self.core.y
        if ax == 0 and ay == 0:
            return None
        qx = q.x - self.core.x
        qy = q.y - self.core.y
        return (qx * ay - qy * ax, ax * ax + ay * ay, qx * ax + qy * ay)

    def _fort_on_lane(self, q):
        """True if q sits within SK_FORT_RING_LANE tiles of the axis lane."""
        a = self._fort_axis(q)
        if a is None:
            return False
        cross, d2, _fwd = a
        return cross * cross <= SK_FORT_RING_LANE * SK_FORT_RING_LANE * d2

    def _fort_lane_cover(self, q, face):
        """Lane tiles a SENTINEL at q facing `face` would sweep.

        ⛔ A RAY, NOT A DISC -- `_ray_cover`'s rule, with two differences that
        are both engine facts rather than choices: the reach is a SENTINEL's
        r^2=32 (not a gunner's 13), and the walk does NOT stop at an occupied
        tile because a sentinel's single-tile-wide line IGNORES OBSTACLES.
        Only in-bounds ends it.  A tile counts when it is on the lane AND
        forward of our own core, i.e. in the corridor the raider walks in
        along -- a ray pointing back over our own half sweeps nothing.
        """
        dx, dy = face.delta()
        if dx == 0 and dy == 0:
            return 0
        n = 0
        k = 1
        while k * k * (dx * dx + dy * dy) <= 32:
            x = q.x + dx * k
            y = q.y + dy * k
            if not self.ib(x, y):
                break
            r = Position(x, y)
            a = self._fort_axis(r)
            if a is not None:
                cross, d2, fwd = a
                if (fwd > 0
                        and cross * cross <= SK_FORT_RING_LANE * SK_FORT_RING_LANE * d2):
                    n += 1
            k += 1
        return n

    def _fort_sent_score(self, ct, q):
        """(score, facing) for THE AXIS SENTINEL at q, or (None, None).

        The site must sit ON the lane and within SK_FORT_RING_SENT_DSQ of our
        own 2x2 footprint; the FACING is chosen as the one whose ray sweeps the
        most corridor.  A sentinel CANNOT ROTATE (`_rotate_toward` is
        gunner-only, COPY 2's asymmetry seen from our own side), so this facing
        is permanent for the rest of the match and is worth choosing properly.
        """
        if self.core is None or self.enemy is None:
            return None, None
        a = self._fort_axis(q)
        if a is None:
            return None, None
        cross, d2, _fwd = a
        if cross * cross > SK_FORT_RING_LANE * SK_FORT_RING_LANE * d2:
            return None, None               # off the lane
        if dsq_core(q, self.core) > SK_FORT_RING_SENT_DSQ:
            return None, None               # outside the citadel neighbourhood
        best = None
        for face in DIRECTIONS:
            if face == Direction.CENTRE:
                continue
            n = self._fort_lane_cover(q, face)
            if n <= 0:
                continue                    # the plank IS the corridor sweep
            # Tie-break toward the enemy core: of two facings that sweep the
            # same amount of lane, the one pointing at their half meets the
            # raider a round earlier.  Same term as `_home_gun_score`'s.
            dx, dy = face.delta()
            toward = dx * (self.enemy.x - q.x) + dy * (self.enemy.y - q.y)
            score = (n, toward)
            if best is None or score > best[0]:
                best = (score, face)
        if best is None:
            return None, None
        # -abs(cross): of two legal sites, the one nearer the lane centre.
        return (best[0][0], best[0][1], -abs(cross)), best[1]

    def _fort_gun_score(self, ct, q, seats):
        """(score, facing) for a FLANK GUNNER at q -- `_home_gun_score`'s
        measured collar geometry (seats weighted 3, apron 1, enemy-approach
        tie-break), with THE OPPOSITE-FLANK REQUIREMENT in front of it.

        ⛔ THE FLANK RULE IS INERT FOR THE FIRST GUNNER by construction
        (`self.fort_flank` is 0 until one stands), so it cannot reorder the
        shipped scoring where there is nothing to balance against.  It binds on
        the SECOND gunner only.

        ⛔⛔ AND IT IS A REFUSAL, NOT A PREFERENCE, BECAUSE THE PREFERENCE FORM
        WAS MEASURED AND NEVER FIRED.  The first cut scored the flank as a
        leading tie-break term; on the 6-cell ON smoke both gunners landed on
        the SAME side of the axis in 6 of 6 cells (icefloe/glacierkeep/
        stavkirke/holmgang: cross signs -72/-48, -40/-32, +72/+120, -44/-58).
        The cause is structural, not statistical: the action's candidates are
        the keeper's FOUR cardinal neighbours, the two gunners are bought a few
        rounds apart with the keeper in nearly the same place, so no
        opposite-flank candidate is ever in the running to be preferred.  A
        term that cannot fire is not an implementation of "the ring covers the
        core-to-core axis symmetrically, no favoured flank" (Magnus's ring,
        study §5b) -- it is a comment.  Refusing the same flank makes the WALK
        half carry the body across the lane instead, which is what the walk is
        for.
        ⚠ THE COST IS DISCLOSED AND COUNTED: this can leave the ring at two
        turrets if no opposite-flank site is ever legal, and it spends keeper
        turns walking.  Both are measurable -- `fort_ring_bought` and
        `fort_ring_walks` -- and the apron surrounds the footprint, so an
        opposite-flank site with a delivery seat on its ray is the normal case
        rather than the lucky one.  A tile exactly ON the lane (cross == 0) is
        not the favoured flank and is allowed.
        """
        if self.fort_flank:
            a = self._fort_axis(q)
            if a is not None and a[0] != 0 and (a[0] > 0) == (self.fort_flank > 0):
                return None, None           # the flank we already hold
        base, face = self._home_gun_score(ct, q, seats)
        if face is None:
            return None, None
        return tuple(base), face

    def _fort_site_ok(self, ct, p, q, seats):
        """The siting guards, every one of them reused from a shipped turret
        verb rather than re-invented:
          * NEVER ON A DELIVERY SEAT -- those eight tiles are the belt's
            terminus; a turret on one is a permanently blocked chain, the exact
            defect `_belt_evict` exists for (`_home_gun_action`'s rule).
          * the tile ARBITER (`tile_owner`), so the ring cannot take a tile
            another verb has planned.
          * NEVER IN AN ENEMY SENTINEL'S LINE (`_on_enemy_axis`, COPY 2).
          * THE SELF-TRAP GUARD -- two free neighbours, not one: v601's
            measured lesson that a turret is PERMANENT and a gun taking the
            keeper's second-to-last tile gets demolished by `_escape` at full
            HP the next round.  Skipped when p is None (the WALK half, where
            the builder is not yet adjacent -- the same guard set the shipped
            `_home_gun_walk` uses).
          * never on ORE (a harvester tile is worth more than a turret tile)
            and never on a tile we cannot read.
        """
        if not self.ibp(q):
            return False
        if (q.x, q.y) in seats:
            return False
        if self.tile_owner(q) not in (OWNER_NONE, OWNER_DOOR):
            return False
        if self._on_enemy_axis(q):
            return False
        if p is not None and self.free_neighbours(ct, p, exclude=q) < 2:
            return False
        try:
            if not ct.is_tile_empty(q):
                return False
            if ct.get_tile_env(q) == Environment.ORE_TITANIUM:
                return False
        except Exception:
            return False
        return True

    def _fort_ring_action(self, ct, p, rnd):
        """PLANK 3's ACTION half -- buy the next ring turret.  True if it took
        the turn.  At most SK_FORT_RING_SENT + SK_FORT_RING_GUNNERS purchases
        in a game, each inside SK_FORT_RING_WINDOW and each behind the reserve.
        """
        if not self._fort_ring_window(ct, rnd):
            return False
        kind = self._fort_ring_next()
        if not self._fort_afford(ct, kind):
            return False
        # ⭐⭐ WAR-CHEST CALL SITE 1 of 2 -- THE RING TURRET.  Placed directly
        # below `_fort_afford` and above the site search: the kind is decided
        # (so the price is known) and nothing has been spent or scanned yet, so
        # a refusal costs one comparison.  ⛔ THE RING IS THE DISCRETIONARY BUY
        # THIS TREE ALREADY PRICES AS SUCH -- plank 3's own redesign moved it
        # BELOW every economy verb after the screen measured turret-for-belt
        # substitution, and this is the same judgement extended in time: inside
        # the last 50 rounds before the flip, a 3rd ring turret and the battery
        # that ends the game are competing for one bank.
        if self._chest_refuse(ct, rnd, self._fort_price(ct, kind)):
            return False
        seats = self._seat_set()
        if not seats:
            return False
        best = None
        for d in CARDINALS:
            q = p.add(d)
            if not self._fort_site_ok(ct, p, q, seats):
                continue
            if kind == EntityType.SENTINEL:
                score, face = self._fort_sent_score(ct, q)
            else:
                score, face = self._fort_gun_score(ct, q, seats)
            if face is None:
                continue
            if best is None or score > best[0]:
                best = (score, q, face)
        if best is None:
            return False
        _score, q, face = best
        if not self.path_arbiter_ok(ct, q, rnd):
            return False                    # v605 FIX 1: a turret is IMPASSABLE
        try:
            if kind == EntityType.SENTINEL:
                if not ct.can_build_sentinel(q, face):
                    return False
                ct.build_sentinel(q, face)
            else:
                if not ct.can_build_gunner(q, face):
                    return False
                ct.build_gunner(q, face)
        except Exception:
            return False
        if kind == EntityType.SENTINEL:
            self.fort_sents += 1
        else:
            self.fort_guns += 1
            if not self.fort_flank:
                a = self._fort_axis(q)
                if a is not None and a[0] != 0:
                    self.fort_flank = 1 if a[0] > 0 else -1
        self.fort_ring_bought += 1
        return True

    def _fort_lane_list(self):
        """The candidate SENTINEL tiles -- on the lane, inside
        SK_FORT_RING_SENT_DSQ of the footprint -- cached on the core/enemy
        anchors.  Both anchors are fixed for the match, so this is computed
        once and is a handful of tiles: the walk is a home-lap step and never
        a tour (the v610 finding, "the keeper's turn is the scarce resource",
        written into the walk and not only into the action).
        """
        if self.core is None or self.enemy is None:
            return ()
        key = (self.core.x, self.core.y, self.enemy.x, self.enemy.y,
               self.mw, self.mh)
        if self._fort_lane_cache is not None and self._fort_lane_key == key:
            return self._fort_lane_cache
        r = 0
        while (r + 1) * (r + 1) <= SK_FORT_RING_SENT_DSQ:
            r += 1
        foot = set(core_tiles_xy(self.core))
        out = []
        for x in range(self.core.x - r, self.core.x + r + 2):
            for y in range(self.core.y - r, self.core.y + r + 2):
                if (x, y) in foot:
                    continue
                if not self.ib(x, y):
                    continue
                q = Position(x, y)
                if dsq_core(q, self.core) > SK_FORT_RING_SENT_DSQ:
                    continue
                if not self._fort_on_lane(q):
                    continue
                out.append((x, y))
        self._fort_lane_cache = tuple(out)
        self._fort_lane_key = key
        return self._fort_lane_cache

    def _fort_ring_walk(self, ct, p, rnd):
        """PLANK 3's MOVEMENT half -- a tile from which the next ring buy is
        legal.  Gated on the SAME window and the SAME affordability as the buy,
        and it terminates permanently once the ring stands.

        The site domain is bounded by construction: the apron for a gunner
        (d^2 <= SK_APRON_DSQ of the footprint) and `_fort_lane_list` for the
        sentinel (d^2 <= SK_FORT_RING_SENT_DSQ, on the lane).
        """
        if not self._fort_ring_window(ct, rnd):
            return None
        kind = self._fort_ring_next()
        if not self._fort_afford(ct, kind):
            return None
        seats = self._seat_set()
        if not seats:
            return None
        if self.fort_ring_rnd == rnd:
            site = self.fort_ring_site
        else:
            domain = (self._fort_lane_list() if kind == EntityType.SENTINEL
                      else self._apron_list())
            best = None
            for xy in domain:
                q = Position(xy[0], xy[1])
                if p.distance_squared(q) <= 1:
                    continue                # adjacent already: the action fires
                if not self._fort_site_ok(ct, None, q, seats):
                    continue
                if kind == EntityType.SENTINEL:
                    score, face = self._fort_sent_score(ct, q)
                else:
                    score, face = self._fort_gun_score(ct, q, seats)
                if face is None:
                    continue
                cand = (score, -p.distance_squared(q))
                if best is None or cand > best[0]:
                    best = (cand, q)
            site = best[1] if best is not None else None
            self.fort_ring_rnd = rnd
            self.fort_ring_site = site
        if site is None:
            return None
        # Stand orthogonally beside the site, not on it -- a builder cannot
        # build on its OWN tile (ledger V2).
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
        self.fort_ring_walks += 1
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
                # ⭐⭐ WAR-CHEST CALL SITE 2 of 2 -- THE APRON BARRIER, AND IT IS
                # THIS BRANCH ONLY.  The `if face is not None` arm above is a
                # BELT-PLAN CONVEYOR and is p0-exempt by construction: the
                # exemption is the shape of the if/else, not a clause that a
                # later edit could quietly widen.  A relay that the belt plan
                # asked for is economy; a barrier on the same tile is the apron
                # MESH, which is discretionary cover.
                if self._chest_refuse(ct, rnd, ct.get_barrier_cost()):
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

    # ==================================================================
    # s57 THE KILLBOX, ARM 1 -- SK_KILLBOX
    # ==================================================================
    # PIECE 1 is the EXILE LAUNCHER (an opening buy on the measured arrival
    # band, throwing opposing builders to the cell or onto the treadmill) and
    # PIECE 2 is the CORNER CELL (2-3 barriers against the map edge).  Both
    # are in-engine moves between competing game bots; the mechanics are the
    # kbprobe's, cited per method.
    #
    # ⛔ ZERO STORE SLOTS.  Slot 15 was the last free one, so the two pieces
    # agree through GEOMETRY and through the ENGINE, never through a published
    # flag: `_kb_cell_cands` is a pure function of (map dims, our core anchor,
    # enemy core anchor) that every unit derives for itself, and the launcher
    # then verifies seal state and occupancy by direct tile query on the round
    # it wants to throw.  That is why the 1-round write-buffering surprise
    # (kbprobe, and CLAUDE.md's store note) cannot bite this plank: there is
    # no cross-unit signal to be stale.

    def _kb_perp2(self, q):
        """Squared perpendicular offset of tile q from the core-to-core axis.

        INTEGER ONLY, on DOUBLED coordinates, so two bodies on the same map
        rank tiles identically and no float rounding can make them disagree.
        Doubling puts each 2x2 core's CENTRE on a lattice point; cross^2 and
        |axis|^2 both scale by 4, so the //4 recovers tile units.
        """
        if self.core is None or self.enemy is None:
            return 0
        ax = 2 * (self.enemy.x - self.core.x)
        ay = 2 * (self.enemy.y - self.core.y)
        bx = 2 * q.x + 1 - (2 * self.core.x + 1)
        by = 2 * q.y + 1 - (2 * self.core.y + 1)
        den = ax * ax + ay * ay
        if den == 0:
            return 0
        cross = ax * by - ay * bx
        return (cross * cross) // den // 4

    def _kb_core_dsq_to_enemy(self):
        """min d^2 from OUR core footprint to the enemy core footprint."""
        best = None
        for xy in core_tiles_xy(self.core):
            d = dsq_core(Position(xy[0], xy[1]), self.enemy)
            if best is None or d < best:
                best = d
        return best if best is not None else 0

    def _kb_cell_cands(self):
        """The ordered CHAMBER candidates -- PURE GEOMETRY, no terrain read.

        ⛔ THE PURITY IS THE DESIGN, not tidiness.  The keeper builds the cell
        and the LAUNCHER throws into it, and they are different `Player`
        instances with no shared memory (kbprobe surprise 1).  A terrain-scored
        pick would let two bodies with different vision name different tiles;
        a pure geometric pick cannot.  Terrain decides only whether a candidate
        is BUILDABLE (keeper side) and whether it is SEALED (launcher side),
        and both of those are read off the engine at the moment they matter.

        THE ANCHOR IS THE BACK MAP EDGE -- the edge our core sits nearest on
        the side AWAY from the enemy core.  kbprobe STEP1's seal audit shows an
        off-map neighbour is a FREE seal, so an edge chamber costs 3 barriers
        and a true map corner costs 2; corners are ranked first for exactly
        that reason.  Chebyshev SK_KB_CELL_CHEB from our own footprint keeps
        every seal tile off the core's spawn ring (Chebyshev is 1-Lipschitz on
        an orthogonal step, so a chamber at 3 has seals at 2..4).

        ⚠ DISCLOSED LIMIT: on a map whose core is far from every edge the
        generator returns nothing and the plank runs LAUNCHER-ONLY, with
        `kb_cell_built_round` staying -1.  There is deliberately no interior
        fallback in arm 1 -- an interior chamber costs 4 barriers instead of 3
        and the registered piece is "2-3 barriers vs map edge/corner".

        ⭐⭐ s57 ARM 2, PIECE 2 (SK_KILLBOX_EXEC + SK_KB_CELL_INTERIOR) CLOSES
        EXACTLY THAT LIMIT AND NOTHING ELSE.  Arm 1's edge/corner form reached
        13 of 30 F1 cells; on the other 17 the back edge is out of Chebyshev
        SK_KB_CELL_CHEB reach of our footprint and this generator returns ().
        The fallback is the kbprobe's own INTERIOR form -- a chamber with four
        in-bounds orthogonal neighbours, i.e. 4 barriers instead of 2-3 -- sited
        in THE SAME BAND (Chebyshev SK_KB_CELL_CHEB), corners of the band
        preferred, and it inherits arm 1's fences unchanged: Chebyshev is
        1-Lipschitz on an orthogonal step, so a chamber at 3 has seals at 2..4
        and NO seal can land on the core's spawn ring at Chebyshev 1.
        ⛔ IT IS A FALLBACK, NOT A MERGE.  It runs only when the edge list is
        EMPTY, so every map that has an edge chamber keeps arm 1's list
        byte-for-byte and this flag cannot perturb the arm-1-only state.
        ⛔ AND IT IS STILL PURE GEOMETRY, which is the property the whole plank
        rests on: the keeper, the launcher and now the SENTINEL are three
        different `Player` instances agreeing through arithmetic alone.
        """
        if self._kb_cands is not None:
            return self._kb_cands
        if self.core is None or self.enemy is None or self.mw is None:
            return ()
        dx = self.core.x - self.enemy.x
        dy = self.core.y - self.enemy.y
        adx = dx if dx >= 0 else -dx
        ady = dy if dy >= 0 else -dy
        if adx >= ady:
            line = ("x", 0 if dx < 0 else self.mw - 1)
        else:
            line = ("y", 0 if dy < 0 else self.mh - 1)
        raw = []
        if line[0] == "x":
            for y in range(self.mh):
                raw.append(Position(line[1], y))
        else:
            for x in range(self.mw):
                raw.append(Position(x, line[1]))
        out = []
        for q in raw:
            if dist_core(q, self.core) != SK_KB_CELL_CHEB:
                continue
            free = 0
            for ddx, ddy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                if not self.ib(q.x + ddx, q.y + ddy):
                    free += 1
            if free < 1:
                continue                    # not actually against the edge
            out.append((-free, dsq_core(q, self.core), q.x, q.y, q))
        out.sort(key=lambda r: r[:4])
        # ⭐ ARM 3: the gate is the DERIVED constant, which is arm 2's own
        # expression `SK_KILLBOX_EXEC and SK_KB_CELL_INTERIOR` widened by
        # `or SK_KILLBOX_FAST` -- the descope makes EXEC-off the PRIMARY arm and
        # the 17/30 boards with no back-edge chamber still need this list.  With
        # SK_KILLBOX_FAST False the constant IS arm 2's expression, so neither
        # standing state moves by a character.
        if not out and SK_KB_INTERIOR_ON:
            out = self._kb_interior_cands()
            self._kb_cands_interior = bool(out)
        cands = [r[4] for r in out]
        # ⭐⭐ s57 ARM 2, PIECE 3 -- THE PREBUILT BLOCK.  The SECOND entry
        # becomes chamber 1's SHARED-WALL PARTNER rather than the next-best
        # unrelated chamber, because a partner costs only its marginal seals
        # and a second unrelated box costs a whole one.  Everything downstream
        # (the plan, the throw picker, the seat picker, the watch) reads this
        # one list, so promoting the partner here is the entire wiring.
        # ⛔ OFF (SK_KILLBOX_EXEC False, or SK_KB_BLOCK False) leaves the list
        # exactly as arm 1 built it.
        cap = SK_KB_CELL_CANDS
        if SK_KB_BLOCK_ON and cands:
            mate = self._kb_block_partner(cands[0])
            if mate is not None:
                rest = [c for c in cands[1:]
                        if (c.x, c.y) != (mate.x, mate.y)]
                cands = [cands[0], mate] + rest
                # ⛔ THE PARTNER ADDS CAPACITY, IT DOES NOT REPLACE A CHAMBER.
                # Promoting it inside a fixed cap silently DROPPED arm 1's
                # last candidate, which is a confound rather than a plank: the
                # launcher's watch, its throw picker and the cell plan all read
                # this one list, so a chamber arm 1 was detaining bodies in
                # would vanish for a reason nothing registered.  The cap grows
                # by exactly the one tile the block adds.
                cap += 1
        self._kb_cands = tuple(cands[:cap])
        return self._kb_cands

    def _kb_block_partner(self, q0):
        """s57 ARM 2, PIECE 3 -- chamber 2 of the shared-wall block, or None.

        THE FORM IS THE PROBE'S, VERBATIM: kbprobe put P at (20,7) and Q at
        (20,9) on ONE column with the barrier at (20,8) serving as BOTH boxes'
        wall -- 7 barriers for two chambers instead of 8, and STEP10 then
        proved one sentinel seat addresses both (TARGETED-TILE: it hit the far
        chamber while the near one held a body at 40 HP that stayed at 40).
        So the partner is q0 + 2*u for a CARDINAL u, with the shared wall at
        q0 + u.

        ⛔ THE SPAWN-RING FENCE IS INHERITED, NOT RE-ARGUED.  The partner is
        required to sit at Chebyshev >= SK_KB_CELL_CHEB of our own footprint;
        Chebyshev is 1-Lipschitz on an orthogonal step, so its seals cannot get
        closer than SK_KB_CELL_CHEB - 1 = 2 and the core's spawn ring at
        Chebyshev 1 stays clear -- which is the same sentence arm 1 wrote for
        chamber 1 and the reason SK_SPAWN_EXIT is in this tree.

        ORDER, pure arithmetic so three `Player` instances agree:
          1  ⭐⭐ STAY ON CHAMBER 1's OWN LINE, and this term is FIRST because
             the first cut of this method did not have it and the unit controls
             caught it: with only a band term, the partner of the west-edge
             chamber (0,11) came out as (2,11) -- an INTERIOR tile two steps off
             the edge, which needs 4 barriers instead of 2, shares no wall with
             the edge form, and is not colinear with anything.  The line is read
             off the tile itself: a chamber's OFF-MAP NEIGHBOUR COUNT is 1
             against an edge, 2 in a map corner and 0 inside, and a step ALONG
             the line preserves it.  So the partner is required to have the same
             count as chamber 1 -- which is the edge column for an edge chamber
             and the interior for an interior one, i.e. kbprobe's colinear form
             in both cases without either being special-cased.
          2  then nearest the band (|Chebyshev - SK_KB_CELL_CHEB|).  ⚠ ON AN
             EDGE THIS IS USUALLY NOT ZERO AND CANNOT BE: on a west edge the
             only band tiles in the column are y = cy-3 and cy+3, so the tile
             two steps along is off-band by construction -- exactly as kbprobe's
             P and Q sat at different distances from the core.  The term breaks
             ties, it does not gate.
          3  farther from the enemy core;
          4  canonical (x, y).
        """
        if self.core is None or self.enemy is None:
            return None
        want_free = 0
        for ddx, ddy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            if not self.ib(q0.x + ddx, q0.y + ddy):
                want_free += 1
        best = None
        for ddx, ddy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            wx, wy = q0.x + ddx, q0.y + ddy
            mx, my = q0.x + 2 * ddx, q0.y + 2 * ddy
            if not self.ib(wx, wy) or not self.ib(mx, my):
                continue
            m = Position(mx, my)
            d = dist_core(m, self.core)
            if d < SK_KB_CELL_CHEB:
                continue                    # the spawn-ring fence
            free = 0
            for ex, ey in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                if not self.ib(mx + ex, my + ey):
                    free += 1
            if free != want_free:
                continue                    # off chamber 1's own line
            band = d - SK_KB_CELL_CHEB
            key = (band, -dsq_core(m, self.enemy), mx, my)
            if best is None or key < best[0]:
                best = (key, m)
        return None if best is None else best[1]

    def _kb_interior_cands(self):
        """s57 ARM 2, PIECE 2 -- the INTERIOR chamber list, PURE GEOMETRY.

        Returns rows in `_kb_cell_cands`'s own (sortkey..., Position) shape,
        already ordered, so the caller's slice and memo are untouched.

        THE FORM IS THE PROBE'S: a chamber whose four orthogonal neighbours are
        all in bounds, sealed by 4 barriers (kbprobe STEP1 built exactly this
        and STEP5a measured `can_move` False on all four cardinals inside it).
        THE BAND IS ARM 1's: Chebyshev SK_KB_CELL_CHEB of our own footprint, so
        the spawn-ring argument transfers verbatim and no seal tile can reach
        Chebyshev 1.

        ORDER, and every term is arithmetic two bodies with different vision
        must agree on:
          1  CORNERS OF THE BAND FIRST (registered wording).  On a Chebyshev
             ring around a 2x2 footprint the corners are the four tiles that
             are at the ring distance in BOTH axes; they are the tiles with the
             most map behind them and the fewest lanes past them.
          2  AWAY FROM THE ENEMY.  A chamber on the raider side sits in the
             stream that is trying to walk through it; the back side is where
             arm 1's edge form put it, and this keeps the two forms consistent.
             ⚠ DISCLOSED TENSION: farther from the enemy is also farther from
             the launcher's band, and the engine's throw window is d^2 <= 26.
             The launcher's own site scorer already ranks CELL REACH (term 2 of
             `_kb_pick_site`) and `_kb_pick_throw` re-checks the range on the
             round it throws, so an unreachable chamber costs a treadmill throw
             and never a body dropped in the open.
          3  canonical (x, y), so the list is total-ordered.
        """
        if self.core is None or self.enemy is None or self.mw is None:
            return []
        out = []
        cx, cy = self.core.x, self.core.y
        span = SK_KB_CELL_CHEB + 2
        for dx in range(-span, span + 2):
            for dy in range(-span, span + 2):
                x, y = cx + dx, cy + dy
                if not self.ib(x, y):
                    continue
                q = Position(x, y)
                if dist_core(q, self.core) != SK_KB_CELL_CHEB:
                    continue
                inb = 0
                for ddx, ddy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                    if self.ib(x + ddx, y + ddy):
                        inb += 1
                if inb != 4:
                    continue        # against an edge: that is arm 1's form and
                                    # the edge generator already refused it
                # THE CORNER TEST, on the footprint rather than the anchor: a
                # 2x2 core spans two rows and two columns, so a ring tile is a
                # corner exactly when it is off the footprint in BOTH axes.
                offx = 0 if cx <= x <= cx + 1 else 1
                offy = 0 if cy <= y <= cy + 1 else 1
                corner = 1 if (offx and offy) else 0
                out.append((-corner, -dsq_core(q, self.enemy), x, y, q))
        out.sort(key=lambda r: r[:4])
        return out

    def _kb_seal_tiles(self, q):
        """The IN-BOUNDS orthogonal neighbours of chamber q.  Off-map ones are
        omitted because the map edge is already a wall (kbprobe STEP1)."""
        out = []
        for ddx, ddy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            x, y = q.x + ddx, q.y + ddy
            if self.ib(x, y):
                out.append(Position(x, y))
        return out

    def _kb_seal_state(self, ct, q):
        """(sealed, builder_bot_id_on_q) for chamber q.

        ⛔ `get_tile_*` RAISES OUT OF VISION AS WELL AS OFF-MAP (kbprobe STEP1
        SEAL Q read `'OOV:GameError'` on an in-bounds neighbour).  An
        unreadable neighbour therefore counts as NOT SEALED -- the direction
        whose cost is one treadmill throw, never a body dropped in the open.
        A WALL tile and a BUILDING tile seal equally and neither cares who owns
        it, which is the audit kbprobe STEP1 actually ran.
        """
        for r in self._kb_seal_tiles(q):
            try:
                if ct.get_tile_env(r) == Environment.WALL:
                    continue
                if ct.get_tile_building_id(r) is None:
                    return False, None
            except Exception:
                return False, None
        try:
            return True, ct.get_tile_builder_bot_id(q)
        except Exception:
            return False, None

    # ==================================================================
    # s57 THE KILLBOX, ARM 3 -- SK_KILLBOX_FAST (THE SPEED PACKAGE)
    # ==================================================================
    # GAME CONTEXT, stated at the verbs: everything below decides WHICH OF OUR
    # OWN BUILDER BODIES walks to WHICH OF OUR OWN TILES.  No call here touches
    # an opposing unit; it is logistics for the box arms 1-2 already build,
    # inside the Florent Code League's sandboxed bot-vs-bot competition.
    #
    # ⛔ ZERO STORE SLOTS, AND THE DIVISION IS STILL GEOMETRY.  Arm 1's whole
    # discipline is that the keeper, the launcher and the sentinel are separate
    # `Player` instances that agree through arithmetic (kbprobe surprise 1).
    # This arm adds a SECOND BUILDER to the box and keeps that property: the
    # DUTY split is keyed on the role each body already claimed for itself in
    # `_claim_role`, and the TILE split inside one duty is "nearest to ME",
    # which is a question each body answers about itself alone and therefore
    # cannot disagree about.  Nothing is published and nothing is read.

    def _kb_fast_owes_launcher(self, rnd):
        """True if THIS body owns the launcher purchase.

        ⛔ THE HAND-BACK IS A DEADLOCK FENCE.  A duty split with no expiry means
        that if the buyer dies at r4 -- and our own record has the raiders' first
        bodies arriving by r5 -- NOBODY buys the launcher and the arm is strictly
        worse than arm 1 on exactly the cells where we were hit hardest.  At
        SK_KB_FAST_UNTIL the duty returns to the keeper, i.e. the tree degrades
        to arm 2's single-body form rather than to nothing.
        """
        if not (SK_KILLBOX_FAST and SK_KB_FAST_PARALLEL):
            return True                 # arms 1-2: the keeper owns everything
        if rnd >= SK_KB_FAST_UNTIL:
            return self.role != SK_KB_FAST_BUYER
        return self.role == SK_KB_FAST_BUYER

    def _kb_fast_owes_cell(self, rnd):
        """True if THIS body owns the cell/block barriers.

        The cell sits at Chebyshev SK_KB_CELL_CHEB of OUR OWN core, i.e. it is
        home work by construction, and the keeper is the only home role.  The
        buyer never lays a seal -- it would be walking BACK through the band it
        was sent forward through.
        """
        if not (SK_KILLBOX_FAST and SK_KB_FAST_PARALLEL):
            return True
        return self.role != SK_KB_FAST_BUYER

    def _kb_fast_sites(self, rnd):
        """How many LIVE build sites THIS body still owes -- the walk budget's
        multiplier, and the arm-2 defect stated as arithmetic.

        Arm 2 sized ONE budget (SK_KB_WALK_MAX = 14, plus SK_KB_EXEC_WALK = 10)
        for a box that has a launcher tile, TWO chambers' seals and a sentinel
        seat; 17 of 30 F1 cells drove a body to the ceiling exactly and the
        executioner buy then refused with `not_adjacent` on 558 of 562 rounds.
        ⛔ COUNTED PER BODY AND PER DUTY, so the split SHRINKS each body's
        budget rather than handing every body the maximum: a keeper that no
        longer owes a launcher gets 8 fewer rounds, not 8 more.
        ⛔ AND IT IS BOUNDED BY THE GEOMETRY ON OFFER, not by the constant: a
        board with one chamber candidate counts one chamber.
        """
        n = 0
        if (SK_KB_LAUNCHER and self.kb_built < SK_KB_MAX
                and self._kb_fast_owes_launcher(rnd)):
            n += 1
        if (SK_KB_CELL and not self.kb_cell_done and not self.kb_cell_off
                and self._kb_fast_owes_cell(rnd)):
            want = SK_KB_CELL_BLOCK if SK_KB_BLOCK_ON else 1
            have = len(self._kb_cell_cands())
            n += want if have >= want else have
        if (SK_KILLBOX_EXEC and SK_KB_EXEC and not self.kb_exec_off
                and self.kb_exec_built < SK_KB_EXEC_MAX):
            n += 1
        return n

    def _kb_fast_budget(self, rnd):
        """THE WALK BUDGET, disclosed as a formula rather than a constant.

            OFF  : SK_KB_WALK_MAX (+ SK_KB_EXEC_WALK with arm 2 armed)
            ON   : min(SK_KB_FAST_WALK_CAP, SK_KB_FAST_WALK_PER * sites)

        ⛔ STILL ONE BUDGET PER BODY FOR THE WHOLE PLANK.  v610's finding is
        that the keeper's turn is the scarce resource and v611 burned 656 keeper
        rounds on one dead tile; this scales the single budget with the work,
        it does not hand any piece a private one, and the cap is a real cap.
        """
        if not (SK_KILLBOX_FAST and SK_KB_FAST_BUDGET):
            b = SK_KB_WALK_MAX
            if SK_KILLBOX_EXEC and SK_KB_EXEC:
                b += SK_KB_EXEC_WALK
            return b
        n = self._kb_fast_sites(rnd)
        b = SK_KB_FAST_WALK_PER * n
        if b > SK_KB_FAST_WALK_CAP:
            b = SK_KB_FAST_WALK_CAP
        self.kb_fast_sites = n
        self.kb_fast_budget = b
        return b

    def _kb_fast_todo_pick(self, p, todo):
        """WHICH seal tile of the current chamber THIS body walks to.

        Arm 1 takes `todo[0]` -- correct with one builder and the whole of the
        serialisation with two: both bodies would queue on the same tile, and a
        builder cannot act and move in the same round, so the second one simply
        waits.  Nearest-to-me splits the chamber between them with no signal.
        ⚠ DISCLOSED SCOPE: the split is WITHIN the plan's current chamber.  The
        plan exposes one chamber at a time (`_kb_cell_plan` returns the first
        viable one), so two bodies parallelise 2-4 tiles, not two whole boxes.
        """
        if not (SK_KILLBOX_FAST and SK_KB_FAST_NEAREST) or len(todo) < 2:
            return todo[0]
        best = None
        for r in todo:
            key = (p.distance_squared(r), r.x, r.y)
            if best is None or key < best[0]:
                best = (key, r)
        return best[1]

    def _kb_fast_exec_mine(self, ct, p, seat):
        """⭐ "THE SEAT JOINS WHICHEVER BODY IS NEARER", as an ENGINE READ.

        With two bodies eligible for the executioner seat, both walking at it
        wastes the turn the split was bought to save.  The tie is broken on
        positions read off the engine this round (`vis_friend` is filled by
        `_sense` from `get_nearby_entities`), never on a store slot:  this body
        yields if any OTHER friendly BUILDER BOT it can see is strictly nearer,
        with the entity id as the total-order tiebreak so two bodies at equal
        distance cannot both yield.
        ⚠ A BOUND, NOT A PROOF, and it is disclosed: two bodies out of each
        other's vision (builder r^2 = 20) both walk.  The cost is bounded by the
        walk budget and by `_kb_exec_covered`; the alternative -- a store slot --
        does not exist (arm 1 took the last one) and would be a round stale.
        """
        if not (SK_KILLBOX_FAST and SK_KB_FAST_PARALLEL):
            return True
        try:
            me = ct.get_id()
        except Exception:
            return True
        d = p.distance_squared(seat)
        for eid, et, ep in self.vis_friend:
            if et != EntityType.BUILDER_BOT or eid == me:
                continue
            dd = ep.distance_squared(seat)
            if dd < d or (dd == d and eid < me):
                self.kb_fast_yield += 1
                return False
        return True

    def _kb_fast_spawn_target(self, ct, rnd):
        """⭐ PIECE 4 -- the tile the CORE aims its next spawn at, or None.

        THE LAUNCHER SITE FIRST, because the buyer is the body whose walk this
        piece is trying to shorten and the site is the tile it walks to; the
        first chamber candidate is the fallback for a board that offers no site
        (pure geometry, no engine call, so it cannot fail).  None -> the loop
        keeps arm 1's fixed DIRECTIONS order, i.e. exact OFF identity.
        ⛔ RUN ON THE CORE'S OWN `Player` INSTANCE, and the disclosure that goes
        with it: the core's `tile_owner` sees an EMPTY belt plan (it is the
        keeper that plans the belt), so the site it names can differ from the
        one the keeper later picks.  That is a heuristic for a SPAWN TILE, not a
        commitment -- the buyer re-derives the site itself, and a spawn one tile
        off the ideal is exactly what arm 1 already had.
        ⛔ MEMOISED BY `_kb_pick_site` ITSELF (`self.kb_site`), so the ~144-tile
        scan runs at most once on the core and then costs one attribute read.
        """
        if not (SK_KILLBOX and SK_KILLBOX_FAST and SK_KB_FAST_SPAWN_DIR):
            return None
        try:
            s = self._kb_pick_site(ct, rnd)
        except Exception:
            s = None
        if s is not None:
            return s
        if SK_KB_CELL:
            c = self._kb_cell_cands()
            if c:
                return c[0]
        return None

    def _kb_fast_buyer_turn(self, ct, p, rnd):
        """THE BUYER'S ENTIRE KILLBOX TURN -- one rung, for a role that is not
        the keeper.  True if it spent this body's round.

        ⛔ IT IS ONE RUNG AND IT IS BOUNDED THREE WAYS, because this is the only
        place in the arm that spends a FORWARD role's opening: the role gate,
        the SK_KB_FAST_UNTIL fence, and the walk budget (which for a body owing
        only the launcher is SK_KB_FAST_WALK_PER rounds, and drops to zero the
        round the launcher stands).  ⚠ THE COST IS THE WALKER'S LAP STARTING
        LATER and it is reported, not argued away.
        """
        if not (SK_KILLBOX and SK_KILLBOX_FAST and SK_KB_FAST_PARALLEL):
            return False
        if self.role != SK_KB_FAST_BUYER or rnd >= SK_KB_FAST_UNTIL:
            return False
        try:
            if ct.get_action_cooldown() == 0:
                # ⭐⭐ s57 SK_DOCTRINE -- SPEND SUBORDINATION, GATED BOX SITE
                # 4 of 4, AND IT IS THE ONE THAT WOULD OTHERWISE ESCAPE: the
                # buyer's launcher purchase does NOT go through the keeper's
                # ladder, so gating only the three keeper rungs would leave the
                # single most expensive box item (a launcher at 20 Ti x scale)
                # outside the reserve.  ⛔ THE WALK BELOW IS DELIBERATELY NOT
                # GATED: walking is free in titanium, and a body that may not
                # buy yet should still be standing where it can buy when the
                # ratchet releases.  What the refusal must not do is SPEND.
                if (not self._doc_box_refuse(ct, rnd, EntityType.LAUNCHER,
                                             "box_buyer")
                        and self._kb_launcher_action(ct, p, rnd)):
                    self.kb_fast_buys += 1
                    return True
            if ct.get_move_cooldown() != 0:
                return False
        except Exception:
            return False
        tgt = self._kb_walk_target(ct, p, rnd)
        if tgt is None:
            return False
        if self.step_to(ct, tgt):
            self.kb_fast_steps += 1
            return True
        return False

    # --- PIECE 1, the launcher: siting ---------------------------------

    def _kb_toward(self, q):
        """True if q stands on the ENEMY side of our own core footprint."""
        if self.enemy is None or self.core is None:
            return True
        return dsq_core(q, self.enemy) < self._kb_core_dsq_to_enemy()

    def _kb_pick_site(self, ct, rnd):
        """Choose ONE launcher tile, memoised for the game once it is legal.

        THE BARS, all checked rather than assumed:
          (a) inside the study's ARRIVAL BAND, d^2 SK_KB_SITE_MIN..MAX_DSQ of
              our own footprint (Chebyshev 2-3);
          (b) on the ENEMY side of our core (`_kb_toward`);
          (c) at least SK_KB_MIN_COVER non-WALL tiles in its pickup disc;
          (d) at least one legal long throw toward the enemy -- `_hl_has_throw`
              verbatim, so the treadmill fallback provably exists before we
              spend 20 Ti and +10% scale on the tile.

        RANKED, and the order is the study read backwards:
          1  AXIS BAND: perpendicular offsets inside 2 tiles rank EQUAL
             (76.7% / 86.7% of their first crossers are inside it; flank side
             balance 44/45 and 53/75, so there is no side to prefer and no
             gradient inside the band the 90 cells can support);
          2  CELL REACH: a site that can throw into a chamber outranks one that
             can only treadmill -- this is the joint-siting term, and it is
             SECOND rather than first because the exile is the piece that pays
             even with no cell at all;
          3  the study's own ring, |Chebyshev - SK_KB_SITE_CHEB|;
          4  nearest our core (the keeper's walk is the recurring cost);
          5  canonical (x, y), so two keepers on the same evidence agree.

        REFUSED, and every refusal is a defect this line has already paid for:
        any tile the ARBITER already owns (belt, cage, door, nest, ore-deny),
        a delivery seat, our own footprint, a banned site, and any tile whose
        env is not EMPTY or that already carries something.
        """
        if self.core is None or self.enemy is None or self.kb_gaveup:
            return None
        if self.kb_site is not None:
            return self.kb_site
        cands = self._kb_cell_cands() if SK_KB_CELL else ()
        # ⭐⭐ ARM 3, PIECE 3 -- THE SEAL COST OF EACH CHAMBER, PRECOMPUTED ONCE.
        # An off-map neighbour is a FREE seal (kbprobe STEP1), so a map corner
        # costs 2 barriers, a back-edge tile 3 and an interior tile 4 -- i.e.
        # this list IS "how many keeper rounds does the box that this site can
        # throw into still need".  Precomputed outside the ~144-tile scan
        # because the alternative is 4 bounds tests per candidate per tile.
        _kbfc = bool(SK_KILLBOX_FAST and SK_KB_FAST_CORNER)
        cand_cost = [(cq, len(self._kb_seal_tiles(cq))) for cq in cands]
        seats = set(core_seats(self.core))
        foot = set(core_tiles_xy(self.core))
        best = None
        best_a2 = None                  # the key ARM 2 would have chosen, kept
                                        # ONLY so the axis-rank loss this piece
                                        # accepts is REPORTED as a number rather
                                        # than asserted to be small
        cx, cy = self.core.x, self.core.y
        span = 5                    # d^2 18 -> |dx| <= 4, plus the 2x2 body
        for dx in range(-span, span + 2):
            for dy in range(-span, span + 2):
                x, y = cx + dx, cy + dy
                if not self.ib(x, y):
                    continue
                q = Position(x, y)
                if (x, y) in foot or (x, y) in seats or (x, y) in self.kb_banned:
                    continue
                d = dsq_core(q, self.core)
                if d < SK_KB_SITE_MIN_DSQ or d > SK_KB_SITE_MAX_DSQ:
                    continue
                if self.tile_owner(q) != OWNER_NONE:
                    continue
                if not self._kb_toward(q):
                    continue
                try:
                    if ct.get_tile_env(q) != Environment.EMPTY:
                        continue    # WALL, and ORE_TITANIUM is a harvester's
                    if not ct.is_tile_empty(q):
                        continue
                except Exception:
                    continue
                cover = 0
                for ddx, ddy in NEIGHBOURS8:
                    r = Position(x + ddx, y + ddy)
                    if not self.ibp(r):
                        continue
                    if q.distance_squared(r) > SK_KB_PICKUP_DSQ:
                        continue
                    try:
                        if ct.get_tile_env(r) != Environment.WALL:
                            cover += 1
                    except Exception:
                        continue
                if cover < SK_KB_MIN_COVER:
                    continue
                if not self._hl_has_throw(ct, q):
                    continue
                reach = 0
                reach_cost = 9          # ⭐ ARM 3: the CHEAPEST reachable
                                        # chamber's barrier count; 9 = none
                for cq, cc in cand_cost:
                    dd = q.distance_squared(cq)
                    if 1 <= dd <= SK_KB_THROW_MAX_DSQ:
                        reach = 1
                        if cc < reach_cost:
                            reach_cost = cc
                        if not _kbfc:
                            break       # ⛔ ARM 2's loop, character for
                                        # character, on every OFF arm
                perp = self._kb_perp2(q)
                if perp <= SK_KB_AXIS_BAND:
                    perp = 0        # ⛔ INCLUSIVE, AND THE FIRST CUT WAS NOT.
                                    # The study's threshold is "WITHIN 2 tiles
                                    # of the axis" and d^2 = 4 IS two tiles; a
                                    # strict `<` put the f1/f2 auroraveil site
                                    # at perp=4 unclamped, i.e. ranked a
                                    # perfectly on-band tile as off-band and
                                    # let the axis term outrank cell reach for
                                    # no reason the 90 cells support.
                ring = dist_core(q, self.core) - SK_KB_SITE_CHEB
                if ring < 0:
                    ring = -ring
                key = (perp, -reach, ring, d, x, y)
                # ⭐⭐ ARM 3, PIECE 3 -- CORNER-FIRST HARD PREFERENCE, AND IT IS
                # A RE-ORDER OF EXACTLY TWO TERMS.  Arm 1's key puts the study's
                # AXIS BAND first and cell REACH second, so a site sitting on
                # the core-to-core axis that can only throw into a 3- or
                # 4-barrier chamber outranks an off-axis site that reaches the
                # 2-barrier map corner.  The registered piece is "accept
                # axis-rank loss for a 2-barrier cell": the box that needs the
                # fewest keeper rounds wins the tie, and the axis term is
                # demoted to second.  `reach_cost` subsumes `-reach` (9 = no
                # reachable chamber at all, which still ranks last).
                if _kbfc:
                    key = (reach_cost, perp, ring, d, x, y)
                    if best_a2 is None or (perp, -reach, ring, d, x, y) < best_a2[0]:
                        best_a2 = ((perp, -reach, ring, d, x, y), q, perp,
                                   reach_cost)
                if best is None or key < best[0]:
                    best = (key, q, perp, reach_cost)
        if best is None:
            return None
        self.kb_site = best[1]
        self.kb_site_rnd = rnd
        self.kb_tries = 0
        # ⭐ BOTH COUNTS, AND THEY ARE COUNTED HERE BECAUSE NOWHERE ELSE CAN:
        # the trade this piece accepts is only visible against the offer the
        # arm-2 key would have taken, and that offer stops existing the moment
        # the scan ends.  `kb_fast_cell_cost` = barriers the chosen site's
        # cheapest reachable chamber needs (2 = the corner this piece is for);
        # `kb_fast_axis_loss` = perpendicular offset given up to get it (0 when
        # the two keys agree, which is the honest "the trade never bound" case).
        if _kbfc:
            self.kb_fast_cell_cost = best[3]
            if best_a2 is not None:
                self.kb_fast_axis_loss = best[2] - best_a2[2]
                self.kb_fast_alt_cost = best_a2[3]
                if (best_a2[1].x, best_a2[1].y) != (best[1].x, best[1].y):
                    self.kb_fast_site_moved = 1
        return self.kb_site

    def _kb_strike(self, rnd):
        """One round of "this site is not working".  Bans it past the bound.

        Called from BOTH the action and the walk, because either one alone
        leaves the other free to run forever -- which is exactly how v611's
        first cut burned 656 keeper rounds on one tile.
        """
        self.kb_tries += 1
        if self.kb_tries < SK_KB_GIVEUP:
            return
        if self.kb_site is not None:
            self.kb_banned.add((self.kb_site.x, self.kb_site.y))
        self.kb_site = None
        self.kb_tries = 0
        if len(self.kb_banned) >= SK_KB_SITE_TRIES:
            self.kb_gaveup = True

    def _kb_launcher_action(self, ct, p, rnd):
        """Buy THE one exile launcher.  True if it took the keeper's turn.

        ⛔ THE TEAM-WIDE CAP IS A VISION READ, NOT A COUNTER.  `kb_built` alone
        is per body and v611 MEASURED a second launcher when a keeper died and
        its successor claimed the role with a fresh counter (2 of 25 builds).
        The store cannot carry the bound (no free slot), so a live friendly
        launcher in `vis_friend` refuses the buy.  ⚠ It is a bound, not a
        proof: a keeper out of vision of an existing launcher can still buy a
        second one, and that residual is disclosed rather than claimed away.
        """
        if not (SK_KILLBOX and SK_KB_LAUNCHER):
            return False
        # ⭐⭐ ARM 3, PIECE 1 -- THE DUTY GATE.  With the parallel build armed
        # the launcher belongs to the BUYER and the keeper's turn belongs to the
        # barriers; OFF this returns True for every body, which is arms 1-2.
        if not self._kb_fast_owes_launcher(rnd):
            return False
        if self.kb_gaveup or self.kb_built >= SK_KB_MAX:
            return False
        for _eid, et, _ep in self.vis_friend:
            if et == EntityType.LAUNCHER:
                return False
        if rnd < SK_KB_MIN_ROUND:
            return False
        site = self._kb_pick_site(ct, rnd)
        if site is None:
            return False
        if p.distance_squared(site) != 1:
            return False                # not orthogonally adjacent: the walk
        cost = ct.get_launcher_cost()
        if ct.get_global_resources() < cost + SK_KB_RESERVE:
            return False
        # ⛔ THE TWO GUARDS EVERY IMPASSABLE BUILD IN THIS TREE PAYS.  A
        # launcher is a BUILDING: it can seal this body in (ledger V2) and it
        # can seal the TEAM's only lane (v605 FIX 1, the helheim throat).
        if self.free_neighbours(ct, p, exclude=site) == 0:
            self._kb_strike(rnd)
            return False
        if not self.path_arbiter_ok(ct, site, rnd):
            self._kb_strike(rnd)
            return False
        try:
            if not ct.can_build_launcher(site):
                self._kb_strike(rnd)
                return False
            ct.build_launcher(site)
        except Exception:
            self._kb_strike(rnd)
            return False
        self.kb_built += 1
        self.kb_built_rnd = rnd
        return True

    # --- PIECE 2, the cell ---------------------------------------------

    def _kb_cell_plan(self, ct, rnd):
        """(chamber, [seal tiles still to build]) for the first VIABLE
        candidate, or None.  MEMOISED FOR THE ROUND: the action rung and the
        walk rung both ask, and the scan is ~40 engine calls.

        A candidate is viable when the chamber itself is empty EMPTY terrain
        that the arbiter does not own, and when every in-bounds seal tile is
        either already a WALL, already carries a building (ours OR theirs -- a
        seal does not care who owns it, kbprobe STEP1), or is unowned EMPTY
        terrain we may build on.  A candidate with one unusable seal tile is
        skipped WHOLE: a half-cell is 6 Ti of barriers that detains nobody.

        ⚠ An unreadable tile makes the candidate UNVIABLE this round rather
        than half-built; the read is retried next round.

        ⭐⭐ s57 ARM 2, PIECE 3 -- THE PREBUILT BLOCK, and it is exactly ONE
        behaviour change here: a chamber that is ALREADY COMPLETE no longer
        ends the scan while fewer than SK_KB_CELL_BLOCK chambers stand.  Arm 1
        returned `(q, [])` on the first finished chamber and the caller latched
        `kb_cell_done`; under the addendum the scan carries on to the partner,
        which is the whole of "capacity before execution" in the plan rung.
        ⛔ The SHARED WALL needs no special case at all: once chamber 1 is
        sealed, that tile carries a building, and the loop below already treats
        "already sealed by somebody" as a free seal.  Chamber 2's todo is
        therefore its 3 marginal tiles interior / 2 against the map edge.
        """
        if self.kb_plan_rnd == rnd:
            return self.kb_plan
        self.kb_plan_rnd = rnd
        self.kb_plan = None
        _kb_done_n = 0
        _kb_want = SK_KB_CELL_BLOCK if SK_KB_BLOCK_ON else 1
        for q in self._kb_cell_cands():
            if self.tile_owner(q) != OWNER_NONE:
                continue
            try:
                if ct.get_tile_env(q) != Environment.EMPTY:
                    continue
                if not ct.is_tile_empty(q):
                    continue
            except Exception:
                continue
            todo = []
            ok = True
            for r in self._kb_seal_tiles(q):
                try:
                    env = ct.get_tile_env(r)
                    if env == Environment.WALL:
                        continue            # free seal
                    if ct.get_tile_building_id(r) is not None:
                        continue            # already sealed by somebody
                    if env != Environment.EMPTY:
                        ok = False           # ORE is a harvester's tile
                        break
                except Exception:
                    ok = False
                    break
                if self.tile_owner(r) != OWNER_NONE:
                    ok = False
                    break
                todo.append(r)
            if not ok:
                continue
            # ⭐ ARM 2, PIECE 3: a FINISHED chamber does not end the scan until
            # SK_KB_CELL_BLOCK of them stand.  `_kb_want` is 1 with the arm-2
            # master off, which is arm 1's behaviour on the same line.
            if not todo:
                _kb_done_n += 1
                if _kb_done_n < _kb_want:
                    continue
            self.kb_plan = (q, todo)
            return self.kb_plan
        return None

    def _kb_cell_action(self, ct, p, rnd):
        """Lay ONE seal barrier.  True if it took this body's turn.

        OPPORTUNISTIC BY CONSTRUCTION: it fires only when this body is already
        orthogonally adjacent to the next seal tile and the bank clears the
        spawn reserve with SK_KB_CELL_RESERVE still standing.  The walk half
        is bounded by the plank's single SK_KB_WALK_MAX budget.
        """
        if not (SK_KILLBOX and SK_KB_CELL):
            return False
        # ⭐⭐ ARM 3, PIECE 1 -- THE DUTY GATE (see `_kb_fast_owes_cell`).  OFF
        # this returns True for every body, which is arms 1-2.
        if not self._kb_fast_owes_cell(rnd):
            return False
        if self.kb_gaveup or self.kb_cell_done or self.kb_cell_off:
            return False
        plan = self._kb_cell_plan(ct, rnd)
        if plan is None:
            # ⛔⛔ THE SCAN MUST TERMINATE, AND THIS IS THE SAME DEFECT CLASS
            # v611 PAID 656 KEEPER ROUNDS FOR.  MEASURED ON THIS ARM'S OWN
            # TRACE: `stavkirke` seat B has no chamber candidate the launcher
            # can reach, so without this bound the keeper re-runs a ~40-call
            # terrain scan every round for the rest of a 1000-round game and
            # never builds anything.  SK_KB_GIVEUP reached tries, then the
            # cell half is off FOR THIS BODY, FOR THIS GAME.
            self.kb_cell_miss += 1
            if self.kb_cell_miss >= SK_KB_GIVEUP:
                self.kb_cell_off = True
            return False
        self.kb_cell_miss = 0
        q, todo = plan
        self.kb_cell_pos = q
        if not todo:
            self.kb_cell_done = True
            self.kb_cell_built_round = rnd
            if SK_KB_INTERIOR_ON and self._kb_cands_interior:
                self.kb_cell_interior_built = 1
            return False
        # ⭐ ARM 3, PIECE 1b -- NEAREST-TO-ME, which is the whole of the
        # tile-level parallel build.  OFF -> `todo[0]`, arm 1's own line.
        r = self._kb_fast_todo_pick(p, todo)
        if p.distance_squared(r) != 1:
            return False
        cost = ct.get_barrier_cost()
        if ct.get_global_resources() < cost + SK_KB_CELL_RESERVE:
            return False
        if not self._claim_spawn_ok(ct, r, reserve=SK_KB_CELL_SPAWN_RESERVE):
            return False
        if self.free_neighbours(ct, p, exclude=r) == 0:
            return False
        if not self.path_arbiter_ok(ct, r, rnd):
            return False
        try:
            if not ct.can_build_barrier(r):
                return False
            ct.build_barrier(r)
        except Exception:
            return False
        self.kb_seals += 1
        # ⛔⛔ THE SECOND LATCH, AND IT IS THE ONE THAT ATE CHAMBER 2.  Arm 1
        # declares the cell finished the moment it lays the LAST SEAL OF THE
        # CURRENT CHAMBER, which is right when there is only ever one chamber
        # and wrong the instant there are two: the first mechanism trace of
        # this arm showed `CELL r=25 cell=0,2` after exactly 3 seals and then
        # no further build for the rest of the game, because `kb_cell_done`
        # short-circuits `_kb_cell_action` on its second line.  Under the block
        # the ONLY thing allowed to declare the cell finished is the PLAN's own
        # empty-todo path, which fires only once SK_KB_CELL_BLOCK chambers
        # stand -- and it terminates, because a completed chamber increments
        # `_kb_done_n` every round.
        if len(todo) == 1 and not SK_KB_BLOCK_ON:
            self.kb_cell_done = True
            self.kb_cell_built_round = rnd
            if SK_KB_INTERIOR_ON and self._kb_cands_interior:
                self.kb_cell_interior_built = 1
        return True

    # --- s57 ARM 2, PIECE 1: THE EXECUTIONER ---------------------------
    # ⛔ GAME CONTEXT, stated at the verb: this builds one of OUR sentinels and
    # fires it at a NAMED TILE inside our own half onto which our launcher
    # legally relocated an opposing builder.  The engine removes that piece
    # under its own documented damage rules (kbprobe STEP6: 3 shots at 18 dmg
    # against 40 HP).  Every call is a documented Controller method.

    def _kb_sealed_chambers(self, ct):
        """Every chamber candidate whose seal is INTACT right now, in list
        order, READ OFF THE ENGINE.

        ⛔ NOT `self.kb_cell_done`.  That flag is PER BODY (kbprobe surprise 1)
        and the keeper that laid the seals may be dead by the time the bank
        clears a 30 Ti sentinel; a successor with a fresh instance would then
        never buy one.  The registered timing is "after the cell completes",
        and the honest test of completion is the same one the launcher uses
        before it throws: `_kb_seal_state` says SEALED right now.
        """
        out = []
        for q in self._kb_cell_cands():
            sealed, _bid = self._kb_seal_state(ct, q)
            if sealed:
                out.append(q)
        return out

    def _kb_exec_chamber(self, ct):
        """The FIRST sealed chamber -- the seat generator's anchor."""
        cs = self._kb_sealed_chambers(ct)
        return cs[0] if cs else None

    def _kb_exec_covered(self, ct, q):
        """True if a friendly SENTINEL already in vision covers chamber q.

        THE ONE-PER-CELL BOUND, AND IT IS AN ENGINE READ RATHER THAN A COUNTER
        for arm 1's measured reason: v611 bought a second launcher when a
        keeper died and its successor claimed the role with a fresh counter.
        `can_fire_from` is the engine's own hypothetical-turret predicate and
        it ignores ammo and cooldown, so a standing tube that is merely
        reloading still counts as covering the tile.
        ⚠ A BOUND, NOT A PROOF: a keeper out of vision of the standing sentinel
        can still buy a second one.  Disclosed, not claimed away.
        """
        for eid, et, ep in self.vis_friend:
            if et != EntityType.SENTINEL:
                continue
            try:
                if ct.can_fire_from(ep, ct.get_direction(eid),
                                    EntityType.SENTINEL, q):
                    return True
            except Exception:
                continue
        return False

    def _kb_exec_seat_pick(self, ct, rnd):
        """(seat, facing, chamber) for the executioner, or None.  Round-memoed.

        THE ENUMERATION IS THE ENGINE'S GEOMETRY AND NOTHING ELSE.  A sentinel
        fires a single-tile-wide line along its FACING and cannot rotate, so
        the chamber must sit at `seat + k * delta(facing)`; the generator walks
        that relation backwards -- 8 facings x k in 1..5 -- instead of scanning
        a disc, which is 40 candidates rather than 121 and is the same order of
        engine calls as `_kb_cell_plan`'s ~40.
        ⛔ AND THE ARITHMETIC IS NEVER TRUSTED: every surviving candidate is
        confirmed with `can_fire_from(seat, facing, SENTINEL, chamber)`, the
        exact predicate kbprobe STEP2 used before it built its sentinel.
        ⛔ NO LINE-OF-SIGHT TERM, and that is a measured engine fact rather than
        an omission: the sentinel's shot IGNORES OBSTACLES and hits the TARGETED
        TILE -- kbprobe STEP6 fired through a full-HP barrier that took no
        damage, and STEP10 hit the FAR chamber while a body stood in the near
        one at 40 HP and stayed at 40.

        REFUSED, and each refusal is a defect this tree has already paid for:
        any tile the arbiter owns, a delivery seat, our own footprint, a banned
        launcher site, ANOTHER CHAMBER CANDIDATE (a sentinel there would eat the
        cell we may still want), and any tile that is not empty EMPTY terrain.

        RANKED: ⭐⭐ COVERAGE FIRST (arm 2 addendum) -- a seat that addresses
        BOTH chambers of the block outranks one that addresses either alone,
        and that is the probe's whole geometry: P and Q were colinear on ONE
        sentinel ray and STEP10 proved the shot lands on the TARGETED TILE, so
        a two-chamber block is parallel-addressable from a single 30 Ti tube.
        Then nearest OUR CORE (the keeper's walk is the recurring cost and this
        role's forward-action share is 0.000), then nearest the anchor chamber,
        then canonical (x, y) so two bodies on the same evidence agree.
        """
        if self.kb_exec_plan_rnd == rnd:
            return self.kb_exec_plan
        self.kb_exec_plan_rnd = rnd
        self.kb_exec_plan = None
        if self.core is None or self.enemy is None:
            return None
        sealed_cs = self._kb_sealed_chambers(ct)
        if not sealed_cs:
            return None
        q = sealed_cs[0]
        cands = set((c.x, c.y) for c in self._kb_cell_cands())
        seats = set(core_seats(self.core))
        foot = set(core_tiles_xy(self.core))
        # THE SPAWN RING, built from the SAME neighbour set `_spawn_plan` and
        # `_claim_spawn_ok` use, so the refusal and the engine's spawn loop
        # cannot drift apart.
        ring = set()
        for _dx, _dy in NEIGHBOURS8:
            ring.add((self.core.x + _dx, self.core.y + _dy))
        best = None
        for face in DIRECTIONS:
            ddx, ddy = face.delta()
            for k in range(1, 6):
                x, y = q.x - ddx * k, q.y - ddy * k
                if not self.ib(x, y):
                    continue
                s = Position(x, y)
                if s.distance_squared(q) > SK_KB_EXEC_SEAT_DSQ:
                    continue
                if (x, y) in foot or (x, y) in seats or (x, y) in cands:
                    continue
                if SK_KB_EXEC_OFF_RING and (x, y) in ring:
                    continue        # ⛔ never on the core's spawn ring
                if (x, y) in self.kb_banned:
                    continue
                if self.tile_owner(s) != OWNER_NONE:
                    continue
                try:
                    if ct.get_tile_env(s) != Environment.EMPTY:
                        continue
                    if not ct.is_tile_empty(s):
                        continue
                    if not ct.can_fire_from(s, face, EntityType.SENTINEL, q):
                        continue
                    cov = 0
                    for c in sealed_cs:
                        if ct.can_fire_from(s, face, EntityType.SENTINEL, c):
                            cov += 1
                except Exception:
                    continue
                key = (-cov, dsq_core(s, self.core),
                       s.distance_squared(q), x, y)
                if best is None or key < best[0]:
                    best = (key, s, face)
        if best is None:
            return None
        self.kb_exec_plan = (best[1], best[2], q)
        return self.kb_exec_plan

    def _kb_exec_action(self, ct, p, rnd):
        """Buy THE one executioner sentinel.  True if it took this body's turn.

        OPPORTUNISTIC IN THE SAME SENSE AS THE CELL: it fires only when this
        body is already orthogonally adjacent to the seat and the bank clears
        SK_KB_EXEC_RESERVE.  ⛔ It never runs before a chamber is SEALED, so the
        30 Ti and the +20% on the ONE GLOBAL ADDITIVE cost factor are spent on
        a box that already exists rather than on one we hope to finish.
        """
        if not (SK_KILLBOX and SK_KILLBOX_EXEC and SK_KB_EXEC):
            return False
        if self.kb_gaveup or self.kb_exec_off:
            return False
        if self.kb_exec_built >= SK_KB_EXEC_MAX:
            return False
        # ⭐⭐ CAPACITY BEFORE EXECUTION (arm 2 addendum).  The sentinel is not
        # bought until the block is UP -- every chamber the geometry offers, up
        # to SK_KB_CELL_BLOCK, is sealed.  Detention outvalues execution while
        # a free chamber remains, so 30 Ti and +20% on the ONE GLOBAL ADDITIVE
        # cost factor spent before the second box is spent in the wrong order.
        # ⛔ THE BAR IS THE GEOMETRY'S, NOT THE CONSTANT'S: on a map that
        # offers one chamber the block is complete at one, and the arm runs in
        # its disclosed single-chamber form rather than waiting for ever.
        if SK_KB_BLOCK:
            want = min(SK_KB_CELL_BLOCK, len(self._kb_cell_cands()))
            sealed_n = len(self._kb_sealed_chambers(ct))
            if sealed_n < want:
                # ⛔⛔ THE FALLBACK, AND THE FIRST CUT DID NOT HAVE IT: the
                # mechanism trace showed `bifrost seat A` sealing chamber 1 at
                # r22 and then NEVER buying an executioner, because the block's
                # second chamber is not buildable on that board and the gate
                # was written as "wait until SK_KB_CELL_BLOCK stand".  A gate
                # waiting on a tile the geometry cannot produce is a deadlock,
                # not a bar.  ⇒ THE GATE HOLDS ONLY WHILE THE CELL HALF STILL
                # HAS SOMETHING TO BUILD.  The registered disposition of that
                # case is the addendum's own: single chamber + the executioner
                # as recycler, and `kb_block_form` records which form each game
                # actually ended in so the coverage split is MEASURED rather
                # than assumed.
                cplan = self._kb_cell_plan(ct, rnd)
                if (not self.kb_cell_off and cplan is not None and cplan[1]):
                    return False
            self.kb_block_form = sealed_n
        plan = self._kb_exec_seat_pick(ct, rnd)
        if plan is None:
            # ⛔⛔ THE SCAN MUST TERMINATE -- the same bound, for the same
            # measured reason, as `_kb_cell_action`'s: a ~40-call scan re-run
            # every round for the rest of a 1000-round game is v611's 656
            # keeper rounds with a different verb on top.
            self.kb_exec_miss += 1
            if self.kb_exec_miss >= SK_KB_GIVEUP:
                self.kb_exec_off = True
            return False
        self.kb_exec_miss = 0
        seat, face, q = plan
        self.kb_exec_seat, self.kb_exec_face, self.kb_exec_cell = seat, face, q
        if self._kb_exec_covered(ct, q):
            return False        # one per cell; the tube standing there is fine
        if p.distance_squared(seat) != 1:
            return False        # not orthogonally adjacent: the walk's job
        cost = ct.get_sentinel_cost()
        if ct.get_global_resources() < cost + SK_KB_EXEC_RESERVE:
            return False
        # ⛔ THE TWO GUARDS EVERY IMPASSABLE BUILD IN THIS TREE PAYS.  A
        # sentinel is a BUILDING: it can seal this body in (ledger V2) and it
        # can seal the TEAM's only lane (v605 FIX 1, the helheim throat).
        if self.free_neighbours(ct, p, exclude=seat) == 0:
            return False
        if not self.path_arbiter_ok(ct, seat, rnd):
            return False
        try:
            if not ct.can_build_sentinel(seat, face):
                return False
            ct.build_sentinel(seat, face)
        except Exception:
            return False
        self.kb_exec_built += 1
        self.kb_exec_built_rnd = rnd
        return True

    # --- ARM 2, PIECE 1: the executioner sentinel's OWN turn -----------

    def _kb_exec_watch(self, ct, p, rnd):
        """Chamber bookkeeping, run on EVERY sentinel round -- ABOVE the
        cooldown and ammo gates, exactly as arm 1's `_kb_watch` runs above the
        launcher's cooldown gate and for the same reason: an occupancy integral
        counted only on rounds we could SHOOT would measure our own reload, not
        their detention.

        THE RETIREMENT SPLIT IS THE SEEN-CHOOSING HALF, and it is arm 1's split
        carried to the sentinel:
          * gone with the seal INTACT  -> a RETIREMENT (`kb_retired_in_cell`).
            kbprobe STEP5a/5b: a sealed body cannot move at all, so it did not
            walk out.
          * ... AND we had put shots into it -> `kb_retired_shot`, the half
            this arm can claim.  The remainder is the PEEL (kbprobe STEP7:
            their own unguarded `move()` raising, which the engine answers by
            destroying the unit permanently) and it is arm 1's dose, not ours.
          * gone through a BROKEN seal -> not counted as a retirement at all.
        THE RECYCLE COLUMN is the registered piece 3: a chamber that held an
        occupant, emptied, and then held ANOTHER one.  Arm 1's launcher already
        re-reads occupancy before every throw (`_kb_pick_throw`:
        `bid is not None` plus `is_tile_passable`), so recycling needs NO new
        code -- kbprobe STEP1's seal audit read `passable=False` for the
        occupied chamber and `passable=True` for the empty one.  This column
        MEASURES that rather than duplicating it.
        """
        pattern = None
        sealed_n = occ_n = 0
        for q in self._kb_cell_cands():
            key = (q.x, q.y)
            sealed, bid = self._kb_seal_state(ct, q)
            if sealed:
                sealed_n += 1
            cur = None
            if bid is not None:
                try:
                    if not (SK_KB_TEAM_CHECK
                            and ct.get_team(bid) == self.team):
                        cur = bid
                except Exception:
                    cur = None
            prev = self.kb_exec_occ.get(key)
            if cur is not None:
                if sealed:
                    occ_n += 1
                # ⭐ ARM 2 ADDENDUM: occupancy SPLIT BY CHAMBER.  With a block
                # standing, "which box is full" is the question the recycler
                # gate turns on, and a pooled count cannot answer it.
                self.kb_occ_by_cell[key] = self.kb_occ_by_cell.get(key, 0) + 1
                if prev is None or prev[0] != cur:
                    if key in self.kb_exec_used:
                        self.kb_recycles += 1
                    self.kb_exec_used.add(key)
                    self.kb_exec_occ[key] = (cur, rnd, 0)
                if pattern is None:
                    try:
                        pattern = set((t.x, t.y)
                                      for t in ct.get_attackable_tiles())
                    except Exception:
                        pattern = set()
                if key in pattern:
                    self.kb_exec_opp += 1
            elif prev is not None:
                del self.kb_exec_occ[key]
                if sealed:
                    self.kb_retired_in_cell += 1
                    self.kb_retire_rounds += rnd - prev[1]
                    if prev[2]:
                        self.kb_retired_shot += 1
        # ⭐⭐ THE CAPACITY COLUMN, AND IT IS THE ADDENDUM'S OWN DOSE: rounds in
        # which EVERY sealed chamber was full, i.e. rounds in which the box had
        # no room for the next throw.  The recycler exists to drive this to
        # zero; a tape where it is already zero says the block is big enough
        # and the executioner had nothing to do -- which is a finding, not a
        # failure, and it is only visible because the column is counted.
        self.kb_sealed_seen = sealed_n
        if sealed_n > 0 and occ_n >= sealed_n:
            self.kb_full_rounds += 1

    def _kb_exec_overload(self, ct, occupied, sealed_n):
        """⭐⭐ THE RECYCLER GATE (arm 2 addendum).  True when CAPACITY BINDS.

        THE ADDENDUM'S ARGUMENT, and it is why this gate exists at all: a
        detained opposing builder occupies one of THEIR MAX_TEAM_UNITS = 50
        slots and cannot be replaced free -- their core pays 30 Ti at base plus
        +20% on their own ONE GLOBAL ADDITIVE cost factor to spawn another. So
        DETENTION OUTVALUES EXECUTION and the sentinel's job is to free a
        chamber at the moment the next raider would find none, not to empty one
        on sight.  Ammunition not spent is THE BATTERY's.

        THE TWO CONDITIONS, both engine reads:
          (a) every SEALED chamber this tube can see is OCCUPIED -- there is no
              empty box left for the launcher's next throw;
          (b) another enemy builder is visible OUTSIDE the chambers -- there IS
              a next raider.
        ⛔ (b) IS A DISCLOSED PROXY AND ITS DIRECTION IS STATED.  The registered
        wording is "a new victim is in PICKUP range", which is the LAUNCHER's
        d^2 <= 2 disc; the sentinel is a different `Player` instance, this plank
        claims zero store slots, and there is therefore no honest way for the
        tube to read the launcher's disc.  It substitutes its OWN vision
        (r^2 = 32), which strictly CONTAINS that pickup disc for any launcher
        seat inside it, so the proxy fires EARLY rather than late -- the
        direction that leaves a chamber empty for a throw that has not happened
        yet, rather than one that misses a throw that has.
        """
        if not SK_KB_EXEC_OVERLOAD:
            return True                 # the ablation: fire on sight
        if sealed_n <= 0 or occupied < sealed_n:
            return False                # (a) a chamber is still free
        # ⛔ THE VISION READ IS DONE HERE AND NOT OFF `self.vis_enemy`: that
        # cache is filled by `_sense`, which runs on the BUILDER path only --
        # a turret's copy is permanently empty, and a gate reading it would be
        # a constant column that validates anything.
        chambers = set((q.x, q.y) for q in self._kb_cell_cands())
        try:
            ids = ct.get_nearby_units()
        except Exception:
            return False
        for eid in ids:
            try:
                if ct.get_team(eid) == self.team:
                    continue
                if ct.get_entity_type(eid) != EntityType.BUILDER_BOT:
                    continue
                ep = ct.get_position(eid)
            except Exception:
                continue
            if (ep.x, ep.y) in chambers:
                continue                # already in a box; not a NEW raider
            return True                 # (b)
        return False

    def _kb_exec_fire(self, ct, p, rnd):
        """Fire at the chamber tile an ENEMY builder stands on.  True if fired.

        ⛔ ORDERED ABOVE `_turret`'s general target ladder ON PURPOSE, and the
        ladder's own docstring says why it has to be: `_target_pri` scores a
        HARVESTER (3) above a BODY (2), so a shipped tube with a chamber and an
        enemy harvester both in its pattern would shoot the harvester for ever
        while the raider walked out of the box the moment the seal broke.  The
        registered arm is DELETION OF THE DETAINED RAIDER; that is this branch.
        ⛔ THE OCCUPANT IS TEAM-CHECKED.  `get_tile_builder_bot_id` answers for
        either team and OUR OWN body can end up in a chamber (arm 1 refuses to
        throw it there, but a body can walk into an unsealed one and be sealed
        around).  Firing at it would be a self-inflicted loss.
        ⛔ NO AMMO ARITHMETIC HERE: this runs UNDER `_turret`'s existing guard
        (`get_global_ammo() < SK_AMMO_SENTINEL -> return`), which exists because
        `can_fire` returns TRUE at 0 ammo and the raise inside
        `finish_firing_turret` destroys our own tube.  The pool is fed by the
        core drip (SK_DRIP) and THE BATTERY's latch (SK_BATTERY2_ECO); this arm
        adds no conversion machinery.
        """
        if not (SK_KILLBOX and SK_KILLBOX_EXEC and SK_KB_EXEC):
            return False
        sealed_cs = self._kb_sealed_chambers(ct)
        targets = []
        occupied = 0
        for q in sealed_cs:
            key = (q.x, q.y)
            try:
                bid = ct.get_tile_builder_bot_id(q)
            except Exception:
                continue        # out of vision or off map: not our round
            if bid is None:
                continue
            try:
                if SK_KB_TEAM_CHECK and ct.get_team(bid) == self.team:
                    continue    # ⛔ THE GUARD.  The tile read has no team.
                if ct.get_entity_type(bid) != EntityType.BUILDER_BOT:
                    continue
            except Exception:
                continue
            occupied += 1
            targets.append((q, key, bid))
        if not targets:
            return False
        # ⭐⭐ THE LATCH, ABOVE THE GATE.  A 40 HP builder needs 3 sentinel
        # shots (kbprobe STEP6, 18 dmg); stopping at 2 because the overload
        # condition lapsed has spent 20 ammo to heal nothing.  Once a shot has
        # gone into an occupant, that occupant is finished.
        pick = None
        if SK_KB_EXEC_LATCH:
            for q, key, bid in targets:
                prev = self.kb_exec_occ.get(key)
                if prev is not None and prev[0] == bid and prev[2] > 0:
                    pick = (q, key, bid, 1)
                    break
        if pick is None:
            if not self._kb_exec_overload(ct, occupied, len(sealed_cs)):
                return False
            q, key, bid = targets[0]
            pick = (q, key, bid, 0)
        q, key, bid, latched = pick
        try:
            if not ct.can_fire(q):
                return False
            ct.fire(q)
        except Exception:
            return False
        self.kb_execs += 1
        self.kb_exec_latched += latched
        prev = self.kb_exec_occ.get(key)
        if prev is not None and prev[0] == bid:
            self.kb_exec_occ[key] = (prev[0], prev[1], prev[2] + 1)
        else:
            self.kb_exec_occ[key] = (bid, rnd, 1)
            self.kb_exec_used.add(key)
        return True

    # --- the ONE walk, shared by both pieces ---------------------------

    def _kb_walk_target(self, ct, p, rnd):
        """Where this body stands to build the launcher, then the cell.

        ⛔ ONE BUDGET FOR THE WHOLE PLANK (SK_KB_WALK_MAX).  v610's finding is
        that the keeper's turn is the scarce resource and v611's own defect was
        an unbounded walk at a dead site; two independent walk budgets would be
        that lesson learned once and then halved.
        ⛔ AND IT NEVER WALKS AT A BUY IT CANNOT MAKE -- the affordability gate
        is the same one the action uses, checked before a step is spent.
        """
        if not SK_KILLBOX or self.kb_gaveup:
            return None
        # ⭐ ARM 2: ONE budget still, widened by the pieces it now has to
        # reach (SK_KB_EXEC_WALK).  Off -> exactly SK_KB_WALK_MAX.
        # ⭐⭐ ARM 3, PIECE 2: the budget is now a FUNCTION OF LIVE BUILD SITES
        # (`_kb_fast_budget`), which is the arm-2 logistics defect answered at
        # its cause.  With SK_KILLBOX_FAST off `_kb_fast_budget` returns exactly
        # the two lines it replaces.
        _budget = self._kb_fast_budget(rnd)
        if self.kb_walk_rounds >= _budget:
            return None
        if rnd < SK_KB_MIN_ROUND:
            return None
        tgt = None
        strike = False
        if (SK_KB_LAUNCHER and self.kb_built < SK_KB_MAX
                and self._kb_fast_owes_launcher(rnd)):
            live = False
            for _eid, et, _ep in self.vis_friend:
                if et == EntityType.LAUNCHER:
                    live = True
                    break
            if not live:
                site = self._kb_pick_site(ct, rnd)
                if site is not None:
                    if p.distance_squared(site) == 1:
                        return None         # seated; the action fires
                    if (ct.get_global_resources()
                            >= ct.get_launcher_cost() + SK_KB_RESERVE):
                        tgt = site
                        strike = True
        if (tgt is None and SK_KB_CELL and not self.kb_cell_done
                and not self.kb_cell_off and self._kb_fast_owes_cell(rnd)):
            plan = self._kb_cell_plan(ct, rnd)
            if plan is not None and plan[1]:
                r = self._kb_fast_todo_pick(p, plan[1])
                if p.distance_squared(r) == 1:
                    return None             # seated; the action fires
                if (ct.get_global_resources()
                        >= ct.get_barrier_cost() + SK_KB_CELL_RESERVE):
                    tgt = r
        # ⭐⭐ s57 ARM 2 -- THE EXECUTIONER'S SEAT, THE THIRD AND LAST RUNG OF
        # THE ONE WALK.  ⛔ BELOW THE CELL, WHICH IS "CAPACITY BEFORE
        # EXECUTION" EXPRESSED IN THE WALK: while a chamber of the block is
        # still unbuilt, the keeper's step belongs to the box, not to the tube
        # that recycles it.  ⛔ AND IT SPENDS THE SAME SK_KB_WALK_MAX BUDGET --
        # v610's finding is that the keeper's turn is the scarce resource, and
        # three independent walk budgets would be that lesson learned once and
        # then divided by three.
        if (tgt is None and SK_KILLBOX_EXEC and SK_KB_EXEC
                and not self.kb_exec_off
                and self.kb_exec_built < SK_KB_EXEC_MAX):
            eplan = self._kb_exec_seat_pick(ct, rnd)
            # ⭐ ARM 3, PIECE 1: "the seat joins whichever body is NEARER".  A
            # body that can see a nearer friendly builder yields the walk rather
            # than racing it; OFF -> True for every body, arm 2's own line.
            if (eplan is not None and not self._kb_exec_covered(ct, eplan[2])
                    and self._kb_fast_exec_mine(ct, p, eplan[0])):
                seat = eplan[0]
                if p.distance_squared(seat) == 1:
                    return None             # seated; the action fires
                if (ct.get_global_resources()
                        >= ct.get_sentinel_cost() + SK_KB_EXEC_RESERVE):
                    tgt = seat
        if tgt is None:
            return None
        best = None
        for d in CARDINALS:
            r = tgt.add(d)
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
            if strike:
                self._kb_strike(rnd)
            return None
        self.kb_walk_rounds += 1
        if strike:
            self._kb_strike(rnd)            # a site we cannot REACH is as dead
                                            # as one we cannot BUILD on
        return best[1]

    # --- PIECE 1, the launcher unit's own turn -------------------------

    def _kb_watch(self, ct, p, rnd):
        """Detention bookkeeping, run on EVERY launcher round (cooldown or
        not), so `kb_detain_rounds` is a residency integral and not a count of
        rounds we happened to be able to act.

        THE ESCAPE / VANISH SPLIT IS THE INSTRUMENT'S SEEN-CHOOSING HALF.
        kbprobe STEP5a and STEP5b measured that a sealed body cannot move at
        all -- `can_move` False on all four cardinals, and an unguarded
        `move()` raises and the engine retires the unit (STEP7).  So an
        occupant that disappears from an INTACT chamber was retired in place
        (`kb_vanish`, a WIN) and only a disappearance from a BROKEN seal is an
        escape (`kb_escapes`, a LOSS).  Reporting both as "escapes" would
        invert the sign of the plank's own dose column.
        """
        for q in self._kb_cell_cands():
            key = (q.x, q.y)
            if p.distance_squared(q) > SK_KB_THROW_MAX_DSQ:
                continue                    # outside our own vision disc
            sealed, bid = self._kb_seal_state(ct, q)
            cur = None
            if sealed and bid is not None:
                try:
                    if not (SK_KB_TEAM_CHECK
                            and ct.get_team(bid) == self.team):
                        cur = bid
                except Exception:
                    cur = None
            if cur is not None:
                self.kb_detain_rounds += 1
                # ⭐ ARM 2 ADDENDUM: the residency integral SPLIT BY CHAMBER.
                # With a two-chamber block the pooled figure cannot answer the
                # question the addendum asks -- whether CAPACITY binds -- and a
                # column that cannot answer its own question is decoration.
                if SK_KILLBOX_EXEC:
                    self.kb_det_by_cell[key] = (
                        self.kb_det_by_cell.get(key, 0) + 1)
                self.kb_occ[key] = cur
            elif key in self.kb_occ:
                del self.kb_occ[key]
                if sealed:
                    self.kb_vanish += 1
                else:
                    self.kb_escapes += 1

    def _kb_pick_throw(self, ct, p, vpos):
        """(target, to_cell) -- THE CELL IF ONE STANDS WITH AN EMPTY CHAMBER,
        THE TREADMILL OTHERWISE.

        The cell test is three engine facts and no belief: the chamber is in
        throw range (1 <= d^2 <= SK_KB_THROW_MAX_DSQ from THIS launcher, the
        engine's own bound), it is SEALED right now, and no builder bot stands
        in it.  An occupied chamber falls straight through to the treadmill,
        which is the registered behaviour.

        ⭐ s57 ARM 2, PIECE 3 -- WITH A BLOCK STANDING THE PICK BECOMES
        "NEAREST EMPTY CHAMBER" rather than "first empty chamber in list
        order".  With one chamber the two rules are the same sentence; with two
        the list order is a build preference and has nothing to say about which
        box this launcher can reach cheapest.  ⛔ THE OCCUPANCY TEST IS ARM 1's,
        UNCHANGED AND UNDUPLICATED -- which is also the whole of chamber
        RECYCLING: kbprobe STEP1's seal audit read `passable=False` for the
        occupied chamber and `passable=True` for the empty one, so the moment
        an occupant is retired this picker starts naming that chamber again
        with no new code at all.
        """
        if SK_KB_CELL:
            best = None
            for q in self._kb_cell_cands():
                dd = p.distance_squared(q)
                if dd < 1 or dd > SK_KB_THROW_MAX_DSQ:
                    continue
                sealed, bid = self._kb_seal_state(ct, q)
                if not sealed or bid is not None:
                    continue
                try:
                    if not ct.is_tile_passable(q):
                        continue
                except Exception:
                    continue
                if not (SK_KILLBOX_EXEC and SK_KB_BLOCK):
                    return q, 1
                key = (dd, q.x, q.y)
                if best is None or key < best[0]:
                    best = (key, q)
            if best is not None:
                return best[1], 1
        return self._hl_pick_throw(ct, p, vpos), 0

    # ==================================================================
    # s57 THE PUSH  (SK_PUSH -- pair reserve + warden + engineer forward)
    # ==================================================================
    # GAME CONTEXT: in-game build work for the Florent Code League, a
    # sandboxed bot-vs-bot competition.  "warden", "barrel", "tube", "throw"
    # and "band" are in-engine mechanics between competing game bots; the
    # throw is the engine's documented cross-team `launch` (no team check,
    # engine-probed) and the heal is the builder's documented +4 HP / 1 Ti
    # action.
    #
    # SIXTEEN HELPERS, NONE OF THEM REACHED ON AN OFF ARM: every call site is
    # a `SK_PUSH ...` module-constant conjunction tested before any controller
    # call, so with the master False the added cost is one test of a module
    # constant per rung and the control flow is v632's, character for
    # character.  The three pieces are ablatable apart (SK_PUSH_RESERVE /
    # _WARDEN / _ENGINEER) because they are coupled by ARGUMENT -- the reserve
    # funds the pair the warden nurses and the engineer succeeds -- and an
    # argument has to be measurable one piece at a time.

    # --- PIECE 1: THE PAIR RESERVE ------------------------------------

    def _push_price(self, ct, kind):
        """The scaled price of `kind` right now, 0 on any unreadable read.

        ⛔ 0 ON AN UNREADABLE COST WEAKENS THE REFUSAL, NEVER STRENGTHENS IT
        (`_fort_price`'s rule, verbatim): a refusal manufactured out of a
        failed read withholds titanium for no measured reason.
        ⛔ THE KIND IS A CONSTANT AT EVERY CALL SITE, so the OFF path never
        evaluates a cost getter -- `_push_refuse` returns on its first line
        before this method is reached.
        """
        try:
            if kind is None:
                return 0
            if kind == EntityType.HARVESTER:
                return ct.get_harvester_cost()
            if kind == EntityType.SENTINEL:
                return ct.get_sentinel_cost()
            if kind == EntityType.GUNNER:
                return ct.get_gunner_cost()
            if kind == EntityType.LAUNCHER:
                return ct.get_launcher_cost()
            if kind == EntityType.SPLITTER:
                return ct.get_splitter_cost()
            if kind == EntityType.BARRIER:
                return ct.get_barrier_cost()
            return ct.get_conveyor_cost()
        except Exception:
            return 0

    def _push_refuse(self, ct, rnd, kind, site):
        """True when a DISCRETIONARY / ECO / BOX purchase must stand down so
        the team can still afford the forward PAIR.

        THE BAR IS `_b2_pair_bar` -- `_plant_gun`'s OWN arithmetic for the two
        plants, live-read, already in the tree and already driven to both
        verdicts by the battery arm's unit controls.  Restating it here would
        be a second expression that can drift from the purchase it protects;
        calling it cannot.

        THE RELEASE IS THE PAIR STANDING, and it is a TEAM fact rather than a
        body's ledger: `_push_live_tubes` reads the two forward-tube beats each
        tube writes for itself (slot 7, v617's producer fix) -- `_two_tubes`'s
        own read, widened from a bool to its count.  A keeper cannot see the
        band, so a per-body ledger would read "no pair" for the whole game and
        the reserve would never release -- the exact failure v620 PLANK 1
        measured on the engineer's own count (`live = 2` on ZERO of 69 buys).

        ⭐⭐ V2 AMENDMENT (b) -- TWO TERMS, AND THE V1 DISPOSITION NAMED BOTH.
        v1's reserve was self-defeating on its own target column: withholding
        eco starved the income that funds the pair (DRY one-tube rounds 73.1%
        -> 87.4%, release fired in 9 of 30 cells).
          * **THE BOUNDED ESCAPE** (`_push_res_escape`, SK_PUSH_RES_HOLD = 20)
            -- `_b2_burst_hold`'s escape transplanted term for term, released
            FOR THE EPISODE and re-armed on the next tube death rather than
            disarmed for the match.
          * **THE live == 1 HALF-BAR** (`_push_res_bar`, SK_PUSH_RES_HALF) --
            at one standing tube only tube 2 is owed, so the bar is
            `_battery_bar`, not the two-barrel purse.  Exact form in that
            method's own note; it is not a literal halving.
        BOTH RELEASE TAILS ARE COUNTED SEPARATELY (`push_res_off` for the pair
        standing, `push_res_esc_pass` for the escape), because two releases
        pooled into one column cannot be told apart in the readout.

        ⭐⭐ V3 AMENDMENT (SK_PUSH_RES_BANKAWARE) -- ONE CONDITION, AND IT IS
        THE COMPOSITE SMOKE'S OWN CAUSE: **the reserve releases whenever the
        bank ALREADY clears the live pair bar.**  The hold exists to ACCUMULATE
        the bar; once the bar is in hand, holding is pure eco loss and the
        binder is the engineer's plant cadence rather than money.  On the rich
        fixture (F3) the v2.1 reserve gave back its whole bar margin (19 -> 15
        wins, kills −5, eco −15%) doing exactly that.
          * THE TEST IS `bank >= bar` -- the PURSE, not this rung's price.  The
            rung's own test (`bank - price >= bar`, above) is the STRICTER one
            and keeps its own column; this tail therefore counts ONLY the
            rounds v2.1 would have refused, so `push_res_bank_pass` is the
            amendment's incremental dose and not a re-count.
          * IT SITS BELOW THE ESCAPE ON PURPOSE.  `_push_res_escape` still runs
            first and still owns the hold clock, the episode release and the
            re-arm edge -- untouched, so every v2.1 clock column stays readable
            as banked.  (`push_res_ready` and this tail read the same predicate
            at the same moment; that is not duplication, it is the clock's
            verdict and the gate's verdict kept in separate columns.)
          * DIRECTION, DISCLOSED: this condition can only ever RELEASE what
            v2.1 refused -- one extra `return False`, no refusal path touched
            -- so v3's refused set is a SUBSET of v2.1's on identical state.
            That is why the sub-flag ships default-True under the master; it is
            still a flag because "releases more" is a claim about the CODE, and
            whether releasing more eco costs tubes is a claim about the GAME
            that only an ablation can price.

        ⛔ THREE STRUCTURAL EXEMPTIONS, AND THEY ARE THE SPECIFICATION RATHER
        THAN SOFTENING -- none of them is a clause inside this method, so none
        can be edited out by accident:
          * **THE CORE'S SPAWN AND THE AMMUNITION DRIP DO NOT PASS THROUGH
            HERE AT ALL.**  Only a BODY can plant a tube and only AMMUNITION
            makes one fire, so gating either is the funding deadlock
            `_fund_battery` already measured (jotunheim: `ammo == 0` in 201 of
            201 window rounds, because income never cleared the floor, so
            nothing converted, so the one tube that stood never fired).
          * **THE 1-2 Ti VERBS ARE NOT GATED** -- `_core_medic`,
            `_seat_heal_action`, `_heal_action`, `_peck_priority`,
            `_seat_clear`.  They are the survival half, they are already
            `_fund_refuse`'s subject under the rotation arm, and a heal
            refused to save 1 Ti is a body lost to save a conveyor.
          * **DEFENCE IS ABOVE THE RESERVE** (`SK_PUSH_RES_DEFENCE`, shipped
            True = exempt).  ⚠ DISCLOSED, AND IT IS THE ARM'S LARGEST OPEN
            LEAK: the three home-turret rungs are 20-30 Ti each and sit above
            this gate, so a cell that buys home turrets can still starve the
            pair (wealthdiag §C: HOME gunners 56 built against 65 forward
            tubes pooled).  The flag exists so an ablation can PRICE that,
            rather than the leak being asserted small.

        ⛔ IT FAILS OPEN on any unreadable number, for `_chest_refuse`'s
        reason.  ⚠ `push_res_held` counts ROUNDS THE RUNG WAS REFUSED, which
        is an UPPER BOUND on turns diverted and not a dose: the refusal is
        evaluated before the verb looks for a target, so a round with nothing
        to build still counts (`_fund_refuse`'s own caveat, verbatim).
        """
        if not (SK_PUSH and SK_PUSH_RESERVE and SK_NEST_PAIR):
            return False
        try:
            live = self._push_live_tubes(ct, rnd)
            if live >= 2:
                self._push_res_watch(live)      # keep the death edge fed
                self.push_res_off += 1          # RELEASED: the pair stands
                return False
            bar = self._push_res_bar(ct, live)
            self.push_res_bar = bar
            bank = ct.get_global_resources()
            if self._push_res_escape(rnd, live, bar, bank):
                self.push_res_esc_pass += 1     # RELEASED: the bounded escape
                return False
            if bank - self._push_price(ct, kind) >= bar:
                self.push_res_pass += 1         # armed, and this buy clears it
                return False
            if SK_PUSH_RES_BANKAWARE and bank >= bar:
                self.push_res_bank_pass += 1    # RELEASED: the bar is ALREADY
                return False                    # in hand (V3, one condition)
        except Exception:
            return False
        self.push_res_held += 1
        self.push_res_site[site] = self.push_res_site.get(site, 0) + 1
        return True

    # --- PIECE 1, V2 AMENDMENT (b): THE HALF-BAR AND THE ESCAPE --------

    def _push_live_tubes(self, ct, rnd):
        """How many forward tubes stand RIGHT NOW: 0, 1 or 2.

        ⛔ IT IS `_two_tubes`'s OWN READ, WIDENED FROM A BOOL TO ITS COUNT, and
        nothing else changes: the same slot, the same `_tube_count`, the same
        SK_TEAM_TUBES branch.  v1 asked "do BOTH stand?" and threw the middle
        answer away -- but the middle answer is the whole subject of the V2
        half-bar (54.8% of rounds are one-tube DRY rounds), so the caller now
        keeps it.  `_two_tubes` itself is untouched; every other consumer of it
        reads exactly what it read before.

        THE FLAG-OFF BRANCH REPRODUCES `_two_tubes`'s v613 form: b21 set means
        the pair stands (2); a non-zero word with b21 clear means the FIRST gun
        exists and the second does not (1, `_s2_pending`'s own reading of the
        same word); a zero word means no gun yet (0).

        Costs one `read_store` and writes nothing, exactly as `_two_tubes`
        does, and it is never reached on an OFF arm (`_push_refuse` returns on
        its first line).
        """
        if not SK_NEST_PAIR:
            return 0
        word = ct.read_store(SK_SLOT_NEST)
        if not SK_TEAM_TUBES:
            if not word:
                return 0
            return 2 if (word & NEST_SITE2_BIT) else 1
        return self._tube_count(word, rnd)

    def _push_res_bar(self, ct, live):
        """The purse the reserve is protecting, in titanium, given `live`.

        ⭐ THE V2 HALF-BAR, AND THE EXACT FORM IS THE POINT (SK_PUSH_RES_HALF).
          * live == 0 -> `_b2_pair_bar` -- BOTH barrels are owed, which is v1's
            bar unchanged, so the live == 0 arm of this method is a byte-level
            restatement of v1 behaviour and any movement at live == 0 is not
            this amendment's.
          * live >= 1 -> `_battery_bar(ct, live)` -- `_plant_gun`'s OWN
            else-branch arithmetic for the ONE plant that is actually owed:
                get_sentinel_cost() + SK_AMMO_SENTINEL * (live + 1)
                + SK_AMMO_FLOOR
        ⛔ ALGEBRAICALLY that second form is `_b2_pair_bar` MINUS
        `(get_sentinel_cost() + SK_BATTERY2_SENT_BUMP)`: minus plant #1's own
        term, which is standing, and minus the post-plant bump, which at
        live == 1 has ALREADY been paid into the one global additive scale
        factor and would be double-counted if priced again.  At the shipped
        constants and 100% scale: 96 -> 60.  It is NOT a literal halving and
        the note says so because "the bar halves" is the registration's
        shorthand, not its arithmetic.

        ⛔ BOTH BARS ARE CALLED, NEVER RESTATED, for `_b2_pair_bar`'s own
        stated reason -- a second expression drifts from the purchase it
        protects, a call cannot -- and both are already driven to both verdicts
        by the battery arm's unit controls.  Each branch makes exactly ONE
        `get_sentinel_cost()` engine call, the same count v1 made.
        """
        if SK_PUSH_RES_HALF and live >= 1:
            return self._battery_bar(ct, live)
        return self._b2_pair_bar(ct)

    def _push_res_watch(self, live):
        """The RE-ARM EDGE: a tube died since this body last looked.

        ⛔ THE EDGE IS `live` FALLING, not a death event, because there is no
        death event a keeper can see -- `get_hp(id)` raises out of vision and
        v618 booked exactly that as a death (the v620 PLANK 1 defect).  The
        team beat count falling is the one honest, team-wide statement that a
        barrel is gone, and it is the same number the release itself runs on.

        ⚠ DISCLOSED, AND IT IS A SAMPLING CAVEAT RATHER THAN A GATE: the edge
        is only seen on rounds where SOME rung asks `_push_refuse`.  A death
        and a replant inside a gap between two such rounds is invisible and the
        escape stays released for that episode.  The keeper reaches this gate
        on essentially every round it has anything discretionary to buy, so the
        gap is small -- but it is a gap, and `push_res_rearm` is reported so
        the re-arm can be seen to have fired rather than assumed.
        """
        if 0 <= live < self.push_res_live:
            self.push_res_esc = False           # a barrel fell: arm again
            self.push_res_rearm += 1
            self.push_res_hold_since = None
        self.push_res_live = live

    def _push_res_escape(self, rnd, live, bar, bank):
        """True while the BOUNDED ESCAPE has released the reserve.

        ⛔⛔ THIS IS THE V1 DISPOSITION'S NAMED CAUSE, ANSWERED WITH MACHINERY
        THAT IS ALREADY IN THE TREE.  v1's reserve was self-defeating on its
        own target column -- withholding eco starved the income that funds the
        pair, DRY one-tube rounds 73.1% -> 87.4%, release fired in 9 of 30
        cells -- which is `_fund_battery`'s DEADLOCK SHAPE: a clamp whose own
        effect removes the condition that would release it.  The answer is
        `_b2_burst_hold`'s escape, transplanted term for term: a hold clock, a
        bound (SK_PUSH_RES_HOLD = 20, the same 20 as SK_BATTERY2_BURST_HOLD),
        a release, and BOTH verdicts of that clock counted.

        ⛔ THE CLOCK RUNS ON `bank >= bar`, NOT ON THE PER-KIND PRICE, and the
        reason is that "consecutive held rounds with the pair still unfunded"
        is a TEAM condition: `_push_refuse` is called several times a round by
        different rungs at different prices, so a clock reset by a cheap
        conveyor clearing the bar would be measuring the rung, not the purse.
        `_b2_burst_hold` resets on exactly this same test.

        ⛔ AND THE ONE DIFFERENCE FROM THE BURST IS DELIBERATE: the burst
        disarms FOR THE MATCH; this releases FOR THE EPISODE and `_push_res_watch`
        re-arms it on the next tube death.  The burst's subject is a one-off
        (plant #1 of the first pair); this reserve's subject recurs every time a
        barrel is knocked out -- median tube life 42 rounds -- so a match-long
        disarm would retire the plank after its first stall.

        ⚠ `push_res_hold_rounds` is counted ONCE PER ROUND (`push_res_hold_last`
        is the round guard), because the several calls a round would otherwise
        turn a 20-round clock into a 20-CALL one in the readout while the
        release itself, which is keyed on `rnd`, kept running on rounds.  The
        two would then disagree and the disagreement would look like a bug in
        the escape rather than in its instrument.
        """
        self._push_res_watch(live)
        if self.push_res_esc:
            return True
        if bank >= bar:
            self.push_res_ready += 1            # funded: nothing is withheld
            self.push_res_hold_since = None
            return False
        if self.push_res_hold_since is None:
            self.push_res_hold_since = rnd
            self.push_res_holds += 1
        if rnd - self.push_res_hold_since >= SK_PUSH_RES_HOLD:
            self.push_res_esc = True
            self.push_res_esc_n += 1
            self.push_res_esc_rnd = rnd + 1     # round + 1, so 0 means NEVER
            self.push_res_hold_since = None
            return True
        if rnd != self.push_res_hold_last:
            self.push_res_hold_rounds += 1
            self.push_res_hold_last = rnd
        return False

    # ==================================================================
    # s57 SK_HAMMER_PRIO -- THE SPEND-LADDER INVERSION
    # ==================================================================
    # GAME CONTEXT: in-game build work for the Florent Code League, a sandboxed
    # bot-vs-bot programming competition.
    #
    # THREE METHODS AND NOTHING ELSE: `_hammer_eco_eval` EVALUATES the adopted
    # battery's readiness latch once per engineer round (V2, below),
    # `_hammer_armed` READS that latch off the wire on the other bodies, and
    # `_hammer_defer` is the refusal predicate the eco rungs are gated on.  All
    # three return on a module constant when the master is off, before any
    # controller call.

    def _hammer_eco_eval(self, ct, rnd):
        """V2 AMENDMENT -- ASK `_b2_eco_ready` EVERY ENGINEER ROUND.

        ⛔⛔ WHY THIS METHOD EXISTS, AND IT IS THE V1 BUILD'S OWN STRUCTURAL
        FINDING RATHER THAN A NEW IDEA.  `_b2_eco_ready` had EXACTLY ONE call
        site -- `_battery_open` (`sk_roles.py:12204`) -- and `_battery_open`'s
        third line is `if live < want: return False` with `want = 2`.  So the
        latch could not fire until the forward PAIR ALREADY STOOD, while
        `_hammer_defer`'s second term is "the pair does NOT yet stand": the two
        terms very nearly excluded each other.  Measured on the v1 traced tape:
        **134 of 134 deferrals were taken at exactly ONE standing tube, 0 at
        zero, and the latch never fired at all in 47 of 60 cells.**  The gate
        half was verified and stands; what was broken was WHERE the latch was
        evaluated.

        ⛔ IT IS NOT A NEW LATCH (class audit row #132).  Same predicate, same
        bar (SK_BATTERY2_ECO_AMMO), same ring (`batt2_ring`, filled by
        `_b2_sample` on this same body one line above the call site), same
        latch-once semantics (`batt2_eco_since` set once, never cleared).  The
        ONLY thing that changes is the SET OF ROUNDS on which the question is
        asked.  Nothing here recomputes a rate, re-bars a decision, or keeps a
        second piece of state that could disagree with the first.

        ⚠ THE WELD, DISCLOSED RATHER THAN HIDDEN (the v1 readout named it
        before this edit was registered): `batt2_eco_since` is now set on
        rounds where `_battery_open` is never reached, so the ADOPTED
        battery's own ceiling gate sees the latch ALREADY SET when it later
        consults it.  That is a RETIMING of an existing decision -- the same
        bar, met earlier -- not a new one, and it is screened as such: the arm
        is measured against t_b4_* whole, so any battery retiming is INSIDE the
        measured effect and is not attributed to the inversion alone.

        ⛔ THE CALL SITE IS THE TOP OF `_siege_engineer`, ABOVE
        `if self.enemy is None: return` -- the most unconditional site on the
        body that owns the latch, and immediately after `_b2_sample`, which is
        the only thing the predicate reads.  The existing `_battery_open` call
        site is LEFT IN PLACE: `_b2_eco_ready` returns True on its first line
        once latched, so the second evaluation is idempotent, and leaving it
        keeps the OFF path character-for-character identical.

        ⛔ THE COUNTERS DO NOT DOUBLE-TICK.  Two evaluations in one round would
        have ticked `batt2_eco_cold` / `batt2_eco_block` twice for one
        decision, silently doubling the adopted battery's own refusal taps.
        `_b2_eco_tick` de-duplicates them by round, and only while the master
        is ON (short-circuited away entirely when it is off).

        ⭐ BOTH VERDICTS ARE TAPPED HERE TOO: `hammer_eco_eval` counts the
        rounds the question was ASKED (zero would mean this method never runs)
        and `hammer_eco_fire` records round+1 of the fire taken AT THIS SITE
        (0 = the latch never fired here -- either it never fired at all, or
        `_battery_open` got there first).
        """
        if not SK_HAMMER_PRIO:
            return
        self.hammer_eco_eval += 1
        before = self.batt2_eco_since
        try:
            self._b2_eco_ready(ct, rnd)
        except Exception:
            return                          # fails OPEN: no latch, no inversion
        if before is None and self.batt2_eco_since is not None:
            self.hammer_eco_fire = rnd + 1  # round+1, so 0 means NEVER HERE

    def _hammer_armed(self, ct, rnd):
        """Has the ADOPTED battery's eco-ready latch fired, as seen from HERE?

        ⛔ IT IS A READ, NOT A LATCH (class audit row #132).  There is no bar,
        no window, no warm-up and no sample ring in this method: the decision
        was taken by `_b2_eco_ready` on the engineer body and published to slot
        8 b12 by `_drip_report`.  Recomputing `_b2_rate` here would have been
        the honest-looking mistake -- same formula, different body, different
        ring, a DIFFERENT fire round -- i.e. a second latch wearing the first
        one's name.

        ⭐ THE STICKY (SK_HAMMER_PRIO_STICKY) AND WHY IT IS NOT THAT MISTAKE.
        The producer can go silent for reasons that are not economic:
        `_b2_sample` is PER BODY by its own docstring, so a successor engineer
        starts with an empty ring and publishes 0 until it re-warms, and
        `_drip_report` returns early while `self.enemy is None`.  The adopted
        latch's own semantics are "once readiness is established the hammer
        stays open", so a reader that UN-fires on engineer turnover would be
        reporting something the latch does not mean.  The sticky can only ever
        repeat a decision already taken; it can never take one.
        ⛔ AND IT IS SCORED BOTH WAYS: `hammer_relapse` counts rounds the wire
        read 0 AFTER the sticky latched -- exactly the work the sticky is
        doing.  Zero relapses would mean the sticky is decoration and the
        readout is required to say so.

        ⚠ `hammer_lag` is the reader-side half of the disclosed staleness: the
        round this body first SAW the latch.  The producer's own fire round is
        not visible from here, so the two are compared in the mechanism trace,
        not inside the bot.
        """
        if not SK_HAMMER_PRIO:
            return False
        if SK_HAMMER_PRIO_STICKY and self.hammer_latched:
            try:
                if not (ct.read_store(SK_SLOT_DRIP) & HAMMER_LATCH_BIT):
                    self.hammer_relapse += 1
                    # ⭐ V2.1: the RELAPSE **ENTRY**, which is a different
                    # number from the relapse ROUND and is the one the escape's
                    # re-arm runs on.  The midgard keeper that motivated the
                    # bound saw 40 relapse rounds; re-arming the escape on each
                    # of them would restart the 20-round clock 40 times and the
                    # bound would be decoration.  `_push_res_watch`'s tube edge
                    # is an EDGE for exactly this reason; this is its twin.
                    if not self.hammer_wire_cold:
                        self.hammer_wire_cold = True
                        self.hammer_relapse_in += 1
                elif self.hammer_wire_cold:
                    self.hammer_wire_cold = False
            except Exception:
                pass
            return True
        try:
            word = ct.read_store(SK_SLOT_DRIP)
        except Exception:
            return False                    # fails OPEN: no inversion
        if not (word & HAMMER_LATCH_BIT):
            self.hammer_cold += 1
            return False
        if not self.hammer_latched:
            self.hammer_latched = True
            self.hammer_lag = rnd           # first round SEEN, not fired
        return True

    def _hammer_defer(self, ct, rnd, site):
        """True when an eco-EXPANSION build must stand down for the battery.

        ⛔ NO `kind` ARGUMENT, UNLIKE `_push_refuse`, AND THE ASYMMETRY IS THE
        DESIGN: the reserve asks "does the bank still clear the pair bar AFTER
        this purchase", so it must price the item.  This gate asks a PRIORITY
        question, not an affordability one -- while the battery is short, eco
        EXPANSION does not buy, at any price.  An affordability term here would
        re-import the reserve's measured self-defeat through the side door.

        THE CONDITION IS TWO TERMS AND NEITHER IS NEW:
          * the adopted eco latch has FIRED (`_hammer_armed`, above);
          * the forward PAIR does not yet stand -- `_push_live_tubes`, the
            TEAM's own forward-tube beats, CALLED and not restated, so this
            gate and `_push_refuse` cannot desynchronise on what "the pair
            stands" means.

        ⛔ IT IS A DEFERRAL, NOT A CANCELLATION, AND THE RELEASE IS THE POINT.
        The refusal ends the moment the pair stands, and it RE-ARMS when the
        pair is lost -- the push-reserve episode pattern (`push_res_watch`'s
        death edge), because median forward-tube life is 42 rounds and a
        match-long disarm would retire the plank after its first barrel.

        ⛔ WHY A REFUSAL GATE AND NOT A RANK SWAP.  A rank swap would have to
        move the barrel rungs UP the keeper's ladder -- but the keeper does not
        plant barrels: `_plant_gun` is the ENGINEER's verb, on another body, at
        the band.  There is no rung to lift.  What the keeper controls is
        whether its turn and the shared purse go into MORE ECONOMY while the
        battery is short, and a refusal on those rungs is exactly that
        inversion expressed on the body that can express it.  `_push_refuse` is
        the tree's own precedent for the shape, down to the per-site counter.

        ⛔ IT FAILS OPEN on any unreadable number (`_chest_refuse`'s reason).
        ⚠ `hammer_held` counts ROUNDS A RUNG WAS REFUSED -- an UPPER BOUND on
        turns diverted, not a dose: the refusal is evaluated before the verb
        looks for a target, so a round with nothing to build still counts
        (`_fund_refuse`'s own caveat, verbatim).  `hammer_rounds` is the
        DISTINCT-round count, which is the honest "deferral rounds" column.
        """
        if not SK_HAMMER_PRIO:
            return False
        try:
            if not self._hammer_armed(ct, rnd):
                return False
            live = self._push_live_tubes(ct, rnd)
            self._hammer_watch(live)
            if live >= SK_HAMMER_PRIO_PAIR:
                if self.hammer_deferring:
                    self.hammer_deferring = False
                    self.hammer_released += 1   # RELEASED: the pair stands
                self.hammer_hold_since = None   # V2.1: the run's only reset
                self.hammer_off += 1
                return False
            if self._hammer_escape(rnd):
                self.hammer_esc_pass += 1       # RELEASED: the bounded escape
                return False
        except Exception:
            return False
        if not self.hammer_deferring:
            self.hammer_deferring = True        # re-armed after a pair loss
            self.hammer_episodes += 1
            if self.hammer_first < 0:
                self.hammer_first = rnd
        self.hammer_held += 1
        if rnd != self.hammer_last_rnd:
            self.hammer_rounds += 1
            self.hammer_last_rnd = rnd
        self.hammer_site[site] = self.hammer_site.get(site, 0) + 1
        return True

    # --- V2.1 AMENDMENT: THE BOUNDED ESCAPE ---------------------------

    def _hammer_watch(self, live):
        """The RE-ARM EDGES for the bounded escape.  TWO of them, both EDGES.

        ⛔ THIS IS `_push_res_watch` TRANSPLANTED, and the first edge is that
        method's own line unchanged: `live` FALLING is the only honest,
        team-wide statement a keeper can make that a barrel is gone -- there is
        no death event out of vision (`get_hp(id)` raises, and v618 booked
        exactly that as a death: the v620 PLANK 1 defect).

        ⭐ THE SECOND EDGE IS THIS GATE'S OWN AND THE RESERVE HAS NO ANALOGUE:
        the published latch bit going COLD after the sticky latched.  The
        reserve's arming condition is a purse; this gate's arming condition is
        the hammer PHASE, so the phase lapsing is a re-arm in exactly the same
        sense.  ⛔ It is `hammer_relapse_in` (relapse ENTRIES) and NOT
        `hammer_relapse` (relapse ROUNDS): the F1 midgard keeper that motivated
        the bound saw 40 relapse rounds, and re-arming on each would restart
        the clock 40 times -- a bound that a silent producer can lift is not a
        bound.

        ⚠ `hammer_esc_rearm` counts EDGES SEEN, not escapes actually cancelled
        (an edge with the escape already un-fired still ticks) -- the reserve's
        `push_res_rearm` has the same shape and the same caveat, and it is an
        UPPER BOUND on re-arms that mattered.

        ⚠ SAMPLING CAVEAT, DISCLOSED, VERBATIM FROM `_push_res_watch`: the edge
        is only seen on rounds where some rung asks `_hammer_defer`.  A tube
        death and a replant inside a gap between two such rounds is invisible
        and the escape stays released for that episode.
        """
        if (0 <= live < self.hammer_live
                or self.hammer_relapse_in > self.hammer_relapse_seen):
            self.hammer_esc = False             # arm again
            self.hammer_esc_rearm += 1
            self.hammer_hold_since = None
        self.hammer_live = live
        self.hammer_relapse_seen = self.hammer_relapse_in

    def _hammer_escape(self, rnd):
        """True while the BOUNDED ESCAPE has released the gate this episode.

        ⛔⛔ THE V2 TRACE'S NAMED DEFECT, ANSWERED WITH MACHINERY ALREADY IN THE
        TREE.  On the V2 traced F1 tape the midgard seat-B keeper (u=4) opened
        ONE episode at r25, never closed it (`eps=1 rel=0`) and refused **968
        distinct rounds**, 949 of them belt-extension tiles.  `_hammer_defer`'s
        own docstring says the plank is *"a DEFERRAL, NOT A CANCELLATION, and
        the release is the point"* -- an episode that runs to the horizon
        falsifies that sentence.  The answer is `_push_res_escape`, transplanted
        term for term: a hold clock, a bound (SK_HAMMER_HOLD = 20, the same 20
        as SK_PUSH_RES_HOLD and SK_BATTERY2_BURST_HOLD), a release FOR THE
        EPISODE, and both verdicts of that clock counted.

        ⛔ THE CLOCK RUNS ON THE GATE'S OWN CONDITION AND NOT ON A PURSE.  The
        reserve's clock resets on `bank >= bar` because the reserve is an
        AFFORDABILITY gate; this one is a PRIORITY gate and `_hammer_defer`
        refuses an affordability term by design ("an affordability term here
        would re-import the reserve's measured self-defeat through the side
        door").  The structural map is exact: the reserve's non-refusing round
        is `bank >= bar`, this gate's non-refusing round is THE PAIR STANDING,
        and that is the round that clears `hammer_hold_since` (in the caller,
        on the same line the episode closes).

        ⛔ RELEASED FOR THE EPISODE, NOT FOR THE MATCH, exactly as the reserve
        is and for the same measured reason: median forward-tube life is 42
        rounds, so a match-long disarm retires the plank after its first stall.
        `_hammer_watch` re-arms on a tube loss or a latch relapse entry.

        ⚠ THE ARITHMETIC IS `rnd - since >= HOLD`, WHICH IS THE RESERVE'S LINE
        VERBATIM: with the run opening at round R the release lands at R + 20,
        i.e. AFTER 20 refused rounds (R..R+19) -- the registration's "after 20
        consecutive deferral rounds", not on the 20th.
        ⚠ `hammer_hold_rounds` is counted ONCE PER ROUND (`hammer_hold_last` is
        the round guard) for `_push_res_escape`'s stated reason: several rungs
        ask per round, and a 20-round clock reported as a 20-CALL one would
        disagree with the release, which is keyed on `rnd`.
        """
        if self.hammer_esc:
            return True
        if self.hammer_hold_since is None:
            self.hammer_hold_since = rnd
            self.hammer_holds += 1
        if rnd - self.hammer_hold_since >= SK_HAMMER_HOLD:
            self.hammer_esc = True
            self.hammer_esc_fired += 1
            self.hammer_esc_rnd = rnd + 1       # round + 1, so 0 means NEVER
            self.hammer_hold_since = None
            return True
        if rnd != self.hammer_hold_last:
            self.hammer_hold_rounds += 1
            self.hammer_hold_last = rnd
        return False

    # --- PIECE 2: THE WARDEN ------------------------------------------

    def _push_seats(self):
        """THEIR core's eight HEAL SEATS, as an (x, y) set.

        A seat is a tile an opposing builder must STAND ON to heal its own
        core -- the engine's own orthogonal-adjacency rule for `heal` -- so
        this set is literally "their medic chairs".  Pure geometry off
        `self.enemy`: zero engine calls, never stale.
        """
        if self.enemy is None:
            return frozenset()
        return frozenset(core_seats(self.enemy))

    def _push_site_cands(self):
        """The launcher sites, RANKED, by pure geometry.  Memoised for life.

        ⛔ GEOMETRY FIRST AND VERIFICATION SECOND, AND THE SPLIT IS AN ENGINE
        FACT: `get_tile_env` RAISES out of vision (kbprobe SURPRISE 2), and
        this site sits beside the ENEMY core -- a body at home can see none of
        it.  A picker that needed a terrain read would return None for the
        whole commute and the warden would never have a walk target.  So the
        candidate ORDER is derived from the enemy anchor alone and the
        emptiness tests are applied by `_push_pick_site` only to tiles the
        body can actually see.

        RANKED: seats covered (most first -- that IS the plank), then nearest
        our own core (the commute is the recurring cost), then canonical
        (x, y) so two bodies on the same evidence agree without talking.
        """
        if self._push_cands is not None:
            return self._push_cands
        if self.enemy is None:
            return ()
        seats = self._push_seats()
        foot = set(core_tiles_xy(self.enemy))
        out = []
        ex, ey = self.enemy.x, self.enemy.y
        for dx in range(-4, 6):
            for dy in range(-4, 6):
                x, y = ex + dx, ey + dy
                if not self.ib(x, y) or (x, y) in foot:
                    continue
                q = Position(x, y)
                d = dsq_core(q, self.enemy)
                if d < 1 or d > SK_PUSH_SITE_MAX_DSQ:
                    continue
                # ⛔⛔ THE ARBITER'S CAGE CLAIM, RESTATED GEOMETRICALLY, AND
                # WITHOUT IT THIS PLANK WALKS AT A TILE IT CAN NEVER BUY.
                # `tile_owner` gives EVERY tile orthogonally adjacent to their
                # core footprint to the CAGE verb (one map tile, one owning
                # verb -- ledger V2/V8), so the highest-coverage sites (their
                # eight heal seats themselves) are refused at the buy.  A
                # candidate list that still contained them would hand the WALK
                # a target the ACTION must refuse forever -- the body arrives,
                # stands adjacent and never builds.  The predicate here is the
                # arbiter's own (`adjacent_to_core`), so the two agree by
                # construction rather than by argument, and the full
                # `tile_owner` test still runs at verification for the terms
                # this one does not cover (belt, nest, door).
                # ⇒ THE ACHIEVABLE MAXIMUM IS TWO SEATS, on a diagonal tile off
                # a footprint corner, which is what SK_PUSH_MIN_SEATS = 2 asks
                # for: both chairs of one corner inside one pickup disc.
                if adjacent_to_core(q, self.enemy):
                    continue
                cov = 0
                for sx, sy in seats:
                    ddx = sx - x
                    ddy = sy - y
                    if ddx * ddx + ddy * ddy <= SK_PUSH_PICKUP_DSQ:
                        cov += 1
                if cov < SK_PUSH_MIN_SEATS:
                    continue
                home = dsq_core(q, self.core) if self.core is not None else 0
                out.append(((-cov, home, x, y), q, cov))
        out.sort(key=lambda c: c[0])
        self._push_cands = tuple((c[1], c[2]) for c in out)
        return self._push_cands

    def _push_pick_site(self, ct, rnd, verified=True):
        """The launcher tile.  `verified` demands the engine agrees it is free.

        The VERIFIED answer is memoised for the game the first time it is
        obtained -- it is the tile the buy will be made on.  The UNVERIFIED
        answer is a WALK TARGET and is deliberately not memoised: it is a
        hypothesis about a tile nobody has seen yet, exactly as `_pick_nest`'s
        site is a hypothesis until walked.
        """
        if self.enemy is None or self.push_gaveup:
            return None
        if self.push_site is not None:
            return self.push_site
        for q, cov in self._push_site_cands():
            if (q.x, q.y) in self.push_banned:
                continue
            if not verified:
                return q
            if self.tile_owner(q) != OWNER_NONE:
                continue
            try:
                if ct.get_tile_env(q) != Environment.EMPTY:
                    continue        # WALL, or ORE (which is a harvester's)
                if not ct.is_tile_empty(q):
                    continue
            except Exception:
                continue            # out of vision: not refuted, just unseen
            self.push_site = q
            self.push_site_rnd = rnd
            self.push_site_seats = cov
            self.push_tries = 0
            return q
        return None

    def _push_strike(self, rnd):
        """One round of "this site is not working".  Bans it past the bound.

        Called from BOTH the action and the walk, because either one alone
        leaves the other free to run forever (`_kb_strike`'s measured lesson:
        v611's first cut burned 656 keeper rounds on one tile).
        ⛔ THE PLANT HALF GIVES UP; THE HEAL HALF DOES NOT.  They are separate
        duties with separate failure modes, and a launcher we cannot site says
        nothing about a barrel we can reach.
        """
        self.push_tries += 1
        if self.push_tries < SK_PUSH_GIVEUP:
            return
        if self.push_site is not None:
            self.push_banned.add((self.push_site.x, self.push_site.y))
        self.push_site = None
        self.push_tries = 0
        if len(self.push_banned) >= SK_PUSH_SITE_TRIES:
            self.push_gaveup = True

    def _push_owes_launcher(self, rnd):
        """Is the plant still this body's duty?

        ⭐ s57 v3: SHARED BY BOTH STAFFINGS.  The predicate is about the DUTY
        (has the launcher been bought / given up / seen, and is the deadline
        past), never about WHICH body owes it -- that is the caller's own gate
        (`self.role == SK_PUSH_WARDEN_ROLE` for v1, role SK_PUSH_W2_ROLE for
        v3).  With both sub-flags off it returns False exactly as it did.
        """
        if not (SK_PUSH and (SK_PUSH_WARDEN or SK_PUSH_WARDEN2)):
            return False
        if self.push_built or self.push_gaveup or self.push_done_seen:
            return False
        return rnd < SK_PUSH_WARDEN_UNTIL

    def _push_launcher_buy(self, ct, p, rnd):
        """Buy THE one warden launcher.  True if it took this body's turn.

        ⛔ THE TEAM-WIDE CAP IS A VISION READ, NOT A COUNTER (v611 measured a
        second launcher when a keeper died and its successor claimed the role
        with a fresh counter): `push_done_seen` is set in the turn above from
        `vis_friend`.  ⚠ It is a bound, not a proof -- a warden out of vision
        of an existing launcher can still buy a second one, and that residual
        is disclosed rather than claimed away.
        """
        site = self._push_pick_site(ct, rnd)
        if site is None:
            return False
        if p.distance_squared(site) != 1:
            return False                # not orthogonally adjacent: the walk
        try:
            cost = ct.get_launcher_cost()
            if ct.get_global_resources() < cost + SK_PUSH_LAUNCH_RESERVE:
                return False
        except Exception:
            return False
        if self._push_refuse(ct, rnd, EntityType.LAUNCHER, "warden"):
            return False
        # ⛔ THE TWO GUARDS EVERY IMPASSABLE BUILD IN THIS TREE PAYS.  A
        # launcher is a BUILDING: it can seal this body in (ledger V2) and it
        # can seal the TEAM's only lane (v605 FIX 1, the helheim throat).
        if self.free_neighbours(ct, p, exclude=site) == 0:
            self._push_strike(rnd)
            return False
        if not self.path_arbiter_ok(ct, site, rnd):
            self._push_strike(rnd)
            return False
        try:
            if not ct.can_build_launcher(site):
                self._push_strike(rnd)
                return False
            ct.build_launcher(site)
        except Exception:
            self._push_strike(rnd)
            return False
        self.push_built += 1
        self.push_built_rnd = rnd
        return True

    def _push_walk_target(self, ct, p, rnd):
        """The tile to stand on to build the launcher, or None.

        ⛔ ONE BUDGET FOR THE WHOLE COMMUTE (SK_PUSH_WALK_MAX), and it is
        deliberately NOT gated on affordability the way `_kb_walk_target` is.
        The killbox site is 2-3 tiles from our own core, so waiting for money
        costs nothing; this site is a cross-board commute and the titanium
        arrives DURING it.  The budget is what bounds the duty instead.
        """
        # ⭐ s57 v3: THE DEDICATED BODY CARRIES ITS OWN BUDGET.  v1's 40 rounds
        # existed to hand the CAGE WALKER back to its lap; a body with no lap
        # to hand back to is only having its plant cancelled (measured:
        # auroraveil A, `walk = 40` with `built = 0` and a reachable site).
        # `push_w2` is False for every body in every OFF arm, so the v1 cap is
        # what every existing arm still reads.
        _cap = SK_PUSH_W2_WALK_MAX if self.push_w2 else SK_PUSH_WALK_MAX
        if self.push_gaveup or self.push_walk_rounds >= _cap:
            return None
        site = self._push_pick_site(ct, rnd, verified=False)
        if site is None:
            return None
        if p.distance_squared(site) == 1:
            return None                 # seated; the action fires
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
                # out of vision is not impassable; a far commute has to be
                # allowed to aim at tiles nobody has seen yet.
                pass
            dd = p.distance_squared(r)
            if best is None or dd < best[0]:
                best = (dd, r)
        if best is None:
            if self.push_site is not None:
                self._push_strike(rnd)  # a site we cannot REACH is as dead as
                                        # one we cannot BUILD on
            return None
        return best[1]

    def _push_barrel(self, ct, p):
        """The most damaged FORWARD friendly sentinel this body can see.

        ⛔ A VISION CENSUS, NOT A LEDGER.  Each unit gets its own `Player`, so
        the warden has never planted anything and a ledger read would be
        empty for its whole life -- the exact defect PLANK 10's
        `_near_live_tube` amendment was built for, and it cost that plank a
        measured 0-of-0 heal rate before it was found.
        ⛔ FORWARD IS `GUARD_FWD_DSQ` FROM OUR OWN CORE, the same constant the
        banked tube analysis splits `tubes` from `all_gun` on, so a barrel the
        census nurses is a barrel the instrument calls forward.
        """
        if self.core is None:
            return None
        best = None
        for eid, et, ep in self.vis_friend:
            if et != EntityType.SENTINEL:
                continue
            if ep is None or not self.ibp(ep):
                continue
            if dsq_core(ep, self.core) <= GUARD_FWD_DSQ:
                continue                # a HOME sentinel, not a tube
            if p.distance_squared(ep) > SK_PUSH_BARREL_DSQ:
                continue
            try:
                miss = ct.get_max_hp(eid) - ct.get_hp(eid)
            except Exception:
                continue
            if miss < 4:
                continue                # a heal is +4; below that it is waste
            key = (-miss, p.distance_squared(ep), ep.x, ep.y)
            if best is None or key < best[0]:
                best = (key, ep)
        if best is None:
            return None
        return best[1]

    def _push_stn_vec(self, sx, sy):
        """The current patrol stop's unit vector: `push_stn_i` quarter-turns of
        the toward-our-core vector.  Pure arithmetic, no engine call, and stop
        0 is the toward-our-core vector itself -- i.e. the FIRST stop is the
        fixed station this patrol replaces.
        """
        i = self.push_stn_i % SK_PUSH_STATION_STOPS
        for _ in range(i):
            sx, sy = sy, -sx
        return sx, sy

    def _push_station(self, ct, p, rnd):
        """WHERE THE BATTERY IS, when no damaged barrel is in sight.

        ⛔ THIS RUNG EXISTS BECAUSE THE FIRST BUILD DID NOT HAVE IT AND ITS OWN
        TRACE REFUTED THE OMISSION.  With only `_push_barrel` (a VISION census)
        the warden stayed beside the launcher it had just planted and read
        `barrel_seen == 0` for the rest of the game on 5 of 5 traced cells: a
        builder sees r^2 = 20 and the band sits at d^2 14-32 of THEIR core, so
        the tubes are simply not visible from the seat the plant is made from.
        A medic that cannot see its patients is not a medic.

        TWO ANSWERS, CHEAPEST FIRST:
          * ANY of our forward sentinels in vision -- damaged or not.  That is
            the battery, and standing at it is what makes the heal reachable
            when one of them IS damaged.
          * otherwise PURE GEOMETRY: the tile SK_PUSH_STATION_OFF from their
            core anchor in the direction of OUR OWN core.  That is where the
            engineer's band is, because the band is d^2 14-32 of their core
            (SK_NEST_DSQ_MIN..MAX) and the engineer arrives from our side.  ⚠ IT
            IS A WALK TARGET, NOT A PLANT SITE: the offset is not required to
            land inside the band exactly (`dsq_core` is asymmetric about a 2x2
            anchor by one tile), only to point the body at it -- the vision
            census takes over the moment a barrel is in sight.
        """
        best = None
        for _eid, et, ep in self.vis_friend:
            if et != EntityType.SENTINEL or ep is None or not self.ibp(ep):
                continue
            if self.core is not None and dsq_core(ep, self.core) <= GUARD_FWD_DSQ:
                continue                        # a HOME sentinel, not a tube
            d = p.distance_squared(ep)
            if best is None or d < best[0]:
                best = (d, ep)
        if best is not None:
            self.push_stn_dwell = 0     # a patient resets the patrol clock
            return best[1]
        if self.enemy is None or self.core is None:
            return None
        sx = 0
        if self.core.x > self.enemy.x:
            sx = 1
        elif self.core.x < self.enemy.x:
            sx = -1
        sy = 0
        if self.core.y > self.enemy.y:
            sy = 1
        elif self.core.y < self.enemy.y:
            sy = -1
        if sx == 0 and sy == 0:
            return None
        # ⭐⭐ s57 v3 -- THE BAND PATROL (SK_PUSH_STATION_DWELL), AND IT IS HERE
        # BECAUSE THIS RUNG'S OWN TRACE REFUTED THE FIXED STOP.  The tubes are
        # NOT reliably on the toward-our-core side of their core: measured on
        # 3 of 3 traced cells the engineer's band sites sat in another quadrant
        # entirely and the medic read `barrel = 0` for its whole life.  With
        # SK_PUSH_STATION_DWELL = 0 this block is inert and the fixed stop is
        # exactly what it was.
        q = None
        for _ in range(SK_PUSH_STATION_STOPS):
            dx, dy = self._push_stn_vec(sx, sy)
            cand = Position(self.enemy.x + dx * SK_PUSH_STATION_OFF,
                            self.enemy.y + dy * SK_PUSH_STATION_OFF)
            if self.ibp(cand):
                q = cand
                break
            # an off-map stop is not a stop: skip it now rather than send the
            # body at a tile it can never stand on.
            self.push_stn_i += 1
            self.push_stn_dwell = 0
        if q is None:
            return None
        if (SK_PUSH_STATION_DWELL
                and p.distance_squared(q) <= SK_PUSH_STATION_NEAR):
            # ⛔ DWELL, NOT TRAVEL: only rounds spent AT the stop tick, so a
            # long commute can never rotate the body past its own destination.
            self.push_stn_dwell += 1
            if self.push_stn_dwell >= SK_PUSH_STATION_DWELL:
                self.push_stn_i += 1
                self.push_stn_dwell = 0
                self.push_stn_moves += 1
        return q

    def _push_medic_turn(self, ct, p, rnd):
        """PIECE 2(c): the warden stations at the battery and heals barrels.

        `_heal_action` is the existing verb (1 Ti -> +4 HP on the most-damaged
        adjacent friendly, most-damaged-first), so the priority emerges from
        code already shipped with no new targeting.  ⚠ DISCLOSED: on a tile
        adjacent to BOTH a damaged barrel and a more damaged prep barrier the
        verb heals the barrier.  That is the same trade `_guard_heal` accepts
        and the same reason -- a screen that dies stops screening.

        ⛔ AND IT ENDS IN A FALL-THROUGH, NOT IN A PARKED BODY.  Once the body
        is standing AT the battery with nothing damaged, this rung returns
        False and the cage lap has the round -- v603 FIX 6(b)'s lesson (two
        bodies spent 860 and 227 rounds as paperweights) applies to a medic
        with no patient exactly as it does to a boxed walker.
        """
        tgt = self._push_barrel(ct, p)
        if tgt is None:
            stn = self._push_station(ct, p, rnd)
            if stn is None or p.distance_squared(stn) <= SK_PUSH_STATION_NEAR:
                return False                    # on station, nothing to heal
            try:
                if ct.get_move_cooldown() != 0:
                    return False
            except Exception:
                return False
            if self.step_to(ct, stn):
                self.push_station_walk += 1
                return True
            return False
        self.push_barrel_seen += 1
        if p.distance_squared(tgt) == 1:            # orthogonally adjacent
            self.push_heal_rounds += 1
            try:
                if (ct.get_global_resources() >= SK_PUSH_HEAL_FLOOR
                        and ct.get_action_cooldown() == 0):
                    if self._heal_action(ct, p, rnd):
                        self.push_heals += 1
                        return True
            except Exception:
                return False
            return False        # on station but nothing to heal: let the lap
                                # have the turn rather than burning it
        try:
            if ct.get_move_cooldown() != 0:
                return False
        except Exception:
            return False
        if self.step_to(ct, tgt):
            self.push_walk_rounds += 1
            return True
        return False

    def _push_warden_turn(self, ct, p, rnd):
        """THE WARDEN'S ENTIRE TURN -- one rung, for the SECOND RAIDER.

        True if it spent this body's round; False falls through to the cage
        lap unchanged, which is the failure mode this rung is designed to
        have (no site, no budget, no barrel -> today's behaviour exactly).

        THREE STAGES, IN ORDER, AND THE ORDER IS THE DOCTRINE:
          (a) travel -- the walk target is the band beside THEIR core, which
              is where the engineer's tubes stand, so "with/behind the
              engineer" is expressed as a shared destination rather than as a
              follow-the-leader coupling this tree has no channel for (16 int
              slots, all claimed; buffered one round);
          (b) plant ONE launcher covering their HEAL SEATS;
          (c) then station at our own battery and nurse the barrels.
        ⚠ THE COST IS THE CAGE LAP, and it is reported rather than argued
        away: while the warden owes a launcher this body lays no ring
        barriers.
        """
        # ⭐⭐ s57 THE PUSH v3 -- PIECE 2b SUPERSEDES THIS RUNG, IT DOES NOT
        # COMPOSE WITH IT.  v1's fatal defect was staffing: this rung takes the
        # CAGE WALKER's round, so the launcher was bought with the second siege
        # body's rounds (wins 12 -> 5, pair rounds 6.9%).  With SK_PUSH_WARDEN2
        # True the warden is a DEDICATED body and this rung must never fire --
        # one module-constant test, no body identity involved, so the cage
        # walker keeps 100% of its existing behaviour by construction rather
        # than by argument.  Both verdicts are unit-controlled.
        if not (SK_PUSH and SK_PUSH_WARDEN) or SK_PUSH_WARDEN2:
            return False
        if self.role != SK_PUSH_WARDEN_ROLE or self.enemy is None:
            return False
        if not self.push_done_seen:
            for _eid, et, ep in self.vis_friend:
                if (et == EntityType.LAUNCHER and ep is not None
                        and dsq_core(ep, self.enemy) <= SK_PUSH_SITE_MAX_DSQ):
                    self.push_done_seen = True
                    break
        if self._push_owes_launcher(rnd):
            try:
                if (ct.get_action_cooldown() == 0
                        and self._push_launcher_buy(ct, p, rnd)):
                    return True
                if ct.get_move_cooldown() != 0:
                    return False
            except Exception:
                return False
            tgt = self._push_walk_target(ct, p, rnd)
            if tgt is None:
                return False
            if self.step_to(ct, tgt):
                self.push_walk_rounds += 1
                return True
            return False
        return self._push_medic_turn(ct, p, rnd)

    # --- PIECE 2b (V3): THE WARDEN AS AN ADDITIONAL BODY --------------

    def _push_w2_trigger(self, ct, rnd):
        """PUSH TIME: does a FORWARD TUBE stand, and is the plant still worth
        buying a body for?

        ⛔⛔ ONE PREDICATE, TWO READERS, AND THAT IS THE WHOLE COORDINATION
        MECHANISM.  The CORE reads it to decide to spawn the extra body; the
        new body reads the SAME store word to decide that the surplus seat it
        just claimed is the WARDEN's and not a second keeper's.  There is no
        channel to carry the intent (all 16 slots are allocated, and slot 0's
        free high bits cannot take a second writer -- the seat counter's own
        note says two writers of one SLOT in one round is a silent lost
        update), so the two ends agree on a fact both can read instead of on a
        message one sends.
        ⛔ WHY THE FIRST TUBE AND NOT THE QUIET TERM: it is the CHEAPEST HONEST
        TRIGGER of the two offered -- one `read_store` plus `_tube_count`, a
        pure function of (word, rnd) that the v617 producer fix already drives
        both ways from a unit test, against `_push_quiet`'s corefire latch
        which is core-local state the claiming BODY cannot see.  It is also the
        right fact: this body exists to keep BARRELS standing and to empty
        their medic chairs, so the first barrel is when the job begins.
        ⛔ THE DEADLINE IS SK_PUSH_WARDEN_UNTIL, THE PLANT'S OWN: the reason to
        buy this body is the launcher, so once the plant has expired the body
        is a body, not a package.
        ⛔ FLAG-OFF IS A MODULE-CONSTANT TEST BEFORE ANY CONTROLLER CALL.
        """
        if not (SK_PUSH and SK_PUSH_WARDEN2):
            return False
        if rnd >= SK_PUSH_WARDEN_UNTIL:
            return False
        try:
            word = ct.read_store(SK_SLOT_NEST)
        except Exception:
            return False
        if not word:
            return False                # no first gun yet (`_s2_pending`'s own
                                        # reading of this word)
        if not SK_TEAM_TUBES:
            return True                 # the v613 layout has no per-seat beat:
                                        # a non-zero word IS "the first gun was
                                        # planted", `_two_tubes`'s own else-form
        return self._tube_count(word, rnd) >= 1

    def _push_warden2(self, ct, p, rnd):
        """THE WARDEN'S ENTIRE TURN, ON ITS OWN DEDICATED BODY (PIECE 2b).

        v1's THREE STAGES, unchanged in order and in mechanism -- what changed
        is WHO runs them:
          (a) travel to the band beside THEIR core (`_push_walk_target`);
          (b) plant ONE launcher covering their HEAL SEATS
              (`_push_launcher_buy` -> `_push_pick_site`, the ranking, the
              arbiter test, the two impassable-build guards, the strike bound);
          (c) then STATION IN THE BAND and nurse the barrels
              (`_push_medic_turn` -> `_push_station` / `_push_barrel`).
        ⛔ NOT ONE OF THOSE METHODS IS MODIFIED.  v1's disposition says the
        mechanics EXECUTED (80/80 border throws, the activity gate proven both
        ways); it was the STAFFING that was fatal.  Re-staffing is the plank.

        ⛔ THE ONE STRUCTURAL DIFFERENCE FROM `_push_warden_turn`, AND IT IS
        FORCED BY THE RE-STAFFING: v1 could return False and let the CAGE LAP
        have the round.  This body has no lap to fall back on, so the fall-
        through ladder is internal and ends in `_push_w2_yield` rather than in
        a parked body (v603 FIX 6(b): two bodies spent 860 and 227 rounds as
        paperweights).  The plant half falling through to the medic half is
        `_push_strike`'s own rule made structural -- "the PLANT half gives up;
        the HEAL half does not".
        """
        if not (SK_PUSH and SK_PUSH_WARDEN2):
            return
        self.push_w2_rounds += 1
        if self.enemy is None:
            return
        # THE ARRIVAL COLUMN.  The band is SK_TUBE_BAND_DSQ of their core --
        # the ground truth's own definition of "forward tube", so the round
        # this body enters the band is the round it can start seeing patients
        # (a builder's vision is r^2 = 20, which is why v1 read
        # `barrel_seen == 0` from the launcher seat).
        if (self.push_w2_arrive < 0
                and dsq_core(p, self.enemy) <= SK_TUBE_BAND_DSQ):
            self.push_w2_arrive = rnd
        # THE TEAM-WIDE LAUNCHER BOUND, v1's vision read verbatim (v611
        # measured a second launcher when a counter was re-created).
        if not self.push_done_seen:
            for _eid, et, ep in self.vis_friend:
                if (et == EntityType.LAUNCHER and ep is not None
                        and dsq_core(ep, self.enemy) <= SK_PUSH_SITE_MAX_DSQ):
                    self.push_done_seen = True
                    break
        if self._push_owes_launcher(rnd):
            acted = False
            try:
                if ct.get_action_cooldown() == 0:
                    acted = self._push_launcher_buy(ct, p, rnd)
            except Exception:
                acted = False
            if acted:
                return
            tgt = self._push_walk_target(ct, p, rnd)
            if tgt is not None:
                try:
                    if ct.get_move_cooldown() == 0 and self.step_to(ct, tgt):
                        self.push_walk_rounds += 1
                        return
                except Exception:
                    return
            self.push_w2_fall += 1      # the plant half produced nothing this
                                        # round: the medic half is not blocked
                                        # by it (they give up separately)
        if self._push_medic_turn(ct, p, rnd):
            return
        self._push_w2_yield(ct, p, rnd)

    def _push_w2_blocking(self, ct, q):
        """Is tile q one that a FRIENDLY BUILDER BOT could build on this round?

        ⛔ THE ENGINE'S OWN RULE IS THE WHOLE TEST: a building is placed on a
        tile ORTHOGONALLY ADJACENT to the builder placing it, so the four
        neighbours of any friendly builder are exactly its build menu, and a
        body parked on one of them has taken a tile off that menu.  Our
        engineer is the builder this matters for -- it is the body that plants
        the replacement tube and lays its prep barriers in the same band this
        medic stations in.
        ⛔ WHY NOT `tile_owner`'s OWNER_NEST TERM: `nest_site` is PER-BODY
        state (every unit gets its own `Player`), so the warden's copy is None
        for its whole life and an OWNER_NEST test from here would be a read of
        a field nobody wrote -- the same defect class as PLANK 10's ledger
        read. The occupancy rule is a fact this body can actually see.
        """
        try:
            me = ct.get_id()
        except Exception:
            return False
        for d in CARDINALS:
            r = q.add(d)
            if not self.ibp(r):
                continue
            try:
                uid = ct.get_tile_builder_bot_id(r)
                if uid is None or uid == me:
                    continue
                if ct.get_team(uid) != self.team:
                    continue
            except Exception:
                continue
            return True
        return False

    def _push_w2_yield(self, ct, p, rnd):
        """THE IDLE ROUND -- and it is spent NOT BLOCKING THE ENGINEER.

        Reached only when the plant is done (or not owed) AND nothing in the
        band is damaged, i.e. the medic is on station with no patient.  ⛔ THE
        HEAL OUTRANKS THE YIELD, and that is deliberate: while a barrel is
        being nursed this body stands where the heal reaches from, even if the
        engineer wanted the tile.  A screen that dies stops screening
        (`_guard_heal`'s own trade).
        ⛔ BOTH TAILS ARE COUNTED -- `push_w2_clear` is idle rounds where the
        body was already out of the way, `push_w2_yield` steps actually taken.
        A rule never seen to refuse has not been seen to be a rule.
        """
        self.push_w2_idle += 1
        if not self._push_w2_blocking(ct, p):
            self.push_w2_clear += 1
            return
        try:
            if ct.get_move_cooldown() != 0:
                return
        except Exception:
            return
        best = None
        for d in CARDINALS:
            q = p.add(d)
            if not self.ibp(q):
                continue
            try:
                if not ct.is_tile_passable(q):
                    continue
            except Exception:
                continue
            if self.tile_owner(q) not in (OWNER_NONE, OWNER_DOOR):
                continue
            if self._push_w2_blocking(ct, q):
                continue
            key = (q.x, q.y)            # canonical, so the step is
            if best is None or key < best[0]:   # deterministic
                best = (key, q)
        if best is None:
            return
        try:
            if self.step_to(ct, best[1]):
                self.push_w2_yield += 1
        except Exception:
            return

    # --- PIECE 2: THE LAUNCHER UNIT'S OWN TURN ------------------------

    def _push_watch(self, ct, p, rnd):
        """THE SLEEPING-DOGS SENSOR.  Which opposing builders are WORKING?

        TWO ENGINE-SIDE FACTS, and neither is our own stdout (CLAUDE.md
        LOKI-14: `print()` reaches no replay and no console, so an arm read
        off our own output is an instrument that does not exist):
          * A MEDIC -- THEIR CORE'S HP ROSE since last round while this body
            stood on one of its seats.  `heal` is the only way a core gains
            HP, and the seat is the only tile it can be healed from, so the
            pair (HP rose, body on a seat) names the healer.
          * A BUILDER -- a NEW opposing building appeared in vision with an
            opposing builder orthogonally beside it.  A building can only be
            placed from an orthogonally adjacent tile (the engine's own
            rule), so the neighbour is the one that placed it.
        ⛔ THE FIRST SCAN MARKS NOBODY.  On this unit's first round every
        building in vision is "new", and a sensor that fired then would call
        the whole board active -- which is the same as having no rule.
        ⛔ RUNS ABOVE THE COOLDOWN GATE, because activity is a fact about
        THEM and counting it only on rounds we could act would measure our
        own cooldown instead.
        """
        if self.enemy is None:
            return
        # --- (i) the medic test ---------------------------------------
        hp = None
        if self.ibp(self.enemy):
            try:
                cid = ct.get_tile_building_id(self.enemy)
                if (cid is not None and ct.get_team(cid) != self.team
                        and ct.get_entity_type(cid) == EntityType.CORE):
                    hp = ct.get_hp(cid)
            except Exception:
                hp = None
        if hp is not None and self.push_core_hp >= 0 and hp > self.push_core_hp:
            for sx, sy in self._push_seats():
                if not self.ib(sx, sy):
                    continue
                q = Position(sx, sy)
                try:
                    uid = ct.get_tile_builder_bot_id(q)
                    if uid is None or ct.get_team(uid) == self.team:
                        continue
                except Exception:
                    continue
                self.push_active[uid] = rnd
        if hp is not None:
            self.push_core_hp = hp
        # --- (ii) the builder test ------------------------------------
        try:
            ids = ct.get_nearby_buildings()
        except Exception:
            return
        fresh = []
        for bid in ids:
            if bid in self.push_seen_b:
                continue
            self.push_seen_b.add(bid)
            fresh.append(bid)
        if not self.push_scan0:
            self.push_scan0 = True
            return                      # the first scan marks nobody
        for bid in fresh:
            try:
                if ct.get_team(bid) == self.team:
                    continue
                bp = ct.get_position(bid)
            except Exception:
                continue
            if bp is None or not self.ibp(bp):
                continue
            for d in CARDINALS:
                q = bp.add(d)
                if not self.ibp(q):
                    continue
                try:
                    uid = ct.get_tile_builder_bot_id(q)
                    if uid is None or ct.get_team(uid) == self.team:
                        continue
                except Exception:
                    continue
                self.push_active[uid] = rnd

    def _push_active_ok(self, bid, rnd):
        """THE SLEEPING-DOGS RULE, as one predicate so it is unit-testable
        and so a mutation control can drive it to either verdict.

        A body that is merely STANDING is left where it is: the throw costs a
        cooldown, a displaced idle body walks back with a fresh plan, and the
        measured value of the arm is emptying their MEDIC CHAIRS -- their core
        absorbs 0.889 of our gross damage in no-kill cells and the healer is
        what that number is made of.
        """
        r = self.push_active.get(bid)
        return r is not None and 0 <= rnd - r <= SK_PUSH_ACTIVE_TTL

    def _push_pick_victim(self, ct, p, rnd):
        """The ACTIVE opposing builder to remove, best first, or None.

        Ranked: one standing on a HEAL SEAT first (that is the medic, by the
        engine's own adjacency rule), then nearest.  Both tails of the
        activity gate are counted here -- `push_opp` is every round with any
        opposing builder in the pickup disc, `push_opp_active` the rounds one
        of them was working, `push_sleep` the rounds we left them alone.
        """
        seats = self._push_seats()
        best = None
        any_v = False
        act = False
        for dx, dy in NEIGHBOURS8:
            q = Position(p.x + dx, p.y + dy)
            if not self.ibp(q):
                continue
            if p.distance_squared(q) > SK_PUSH_PICKUP_DSQ:
                continue
            try:
                bid = ct.get_tile_builder_bot_id(q)
            except Exception:
                continue
            if bid is None:
                continue
            try:
                if SK_PUSH_TEAM_CHECK and ct.get_team(bid) == self.team:
                    continue        # ⛔ THE GUARD.  The engine has none.
                if ct.get_entity_type(bid) != EntityType.BUILDER_BOT:
                    continue
            except Exception:
                continue
            any_v = True
            if not self._push_active_ok(bid, rnd):
                continue            # sleeping dogs
            act = True
            on_seat = 1 if (q.x, q.y) in seats else 0
            key = (-on_seat, p.distance_squared(q), q.x, q.y)
            if best is None or key < best[0]:
                best = (key, q, bid)
        if any_v:
            self.push_opp += 1
            if act:
                self.push_opp_active += 1
            else:
                self.push_sleep += 1
        if best is None:
            return None
        return best[1], best[2]

    def _push_pick_throw(self, ct, p, vpos):
        """Where to put them: a MAP-BORDER tile if one is legal, else the
        farthest legal tile.  Position or None.

        `can_launch` measures 1 <= d^2 <= 26 FROM THE LAUNCHER (kbprobe
        STEP4), not from the victim, so the candidate set is this unit's own
        r^2 = 26 disc -- which is also exactly its vision, so every candidate
        is a tile we can legally query.

        ⭐ THE BORDER PREFERENCE IS THE APPROVED CLASS AND NOT A NEW ONE: the
        throw is legal and documented; what happens next is THEIR code
        querying an off-map neighbour and the engine retiring the unit under
        its own documented rules (CLAUDE.md, the 2026-08-10 class ruling --
        "positions, plural and unqualified", so a new trigger needs no new
        question).  Distance is the tie-break and the whole fallback.
        """
        try:
            tiles = ct.get_nearby_tiles(SK_PUSH_THROW_MAX_DSQ)
        except Exception:
            return None
        cands = []
        for t in tiles:
            d = p.distance_squared(t)
            if d < 1 or d > SK_PUSH_THROW_MAX_DSQ:
                continue
            if not self.ibp(t):
                continue
            try:
                if not ct.is_tile_passable(t):
                    continue
            except Exception:
                continue
            border = 0
            if SK_PUSH_BORDER and (t.x == 0 or t.y == 0
                                   or t.x == self.mw - 1
                                   or t.y == self.mh - 1):
                border = 1
            cands.append(((-border, -d, t.x, t.y), t))
        if not cands:
            return None
        cands.sort(key=lambda c: c[0])
        for _key, t in cands[:SK_PUSH_PROBE_CAP]:
            try:
                if ct.can_launch(vpos, t):
                    return t
            except Exception:
                continue
        return None

    def _push_launcher_turn(self, ct, p, rnd):
        """THE WARDEN LAUNCHER'S OWN `run()` BRANCH.

        ⛔ THIS UNIT IS A UNIT (kbprobe surprise 1: every unit gets its own
        `Player` instance), so every counter here is THIS launcher's and the
        readout aggregates offline.  ⛔ NO AMMO IS INVOLVED -- launchers do not
        draw on the team pool, so the drip's arithmetic is untouched.
        `launch` adds 1 to the action cooldown, and the probe measured the
        cooldown back at 0 on the round after every throw, so CONSECUTIVE-ROUND
        throws are legal and this method attempts one every round.
        """
        self._push_watch(ct, p, rnd)
        victim = self._push_pick_victim(ct, p, rnd)
        try:
            if ct.get_action_cooldown() != 0:
                return
        except Exception:
            return
        if victim is None:
            return
        vpos, _vid = victim
        target = self._push_pick_throw(ct, p, vpos)
        if target is None:
            return
        try:
            if not ct.can_launch(vpos, target):
                return
            ct.launch(vpos, target)
        except Exception:
            return
        self.push_throws += 1
        self.push_throw_d2 += p.distance_squared(target)
        if (target.x == 0 or target.y == 0 or target.x == self.mw - 1
                or target.y == self.mh - 1):
            self.push_throw_border += 1

    # --- PIECE 3: THE ENGINEER FORWARD --------------------------------

    def _push_quiet(self, ct, rnd):
        """THE POST-SECURITY GATE: is home quiet enough to commit forward?

        ⛔ THE EXISTING THREAT READS, NO NEW LATCH (class audit row #132).  ONE
        term, and V2 is why it is one:
          * `corefire_fresh` AND core HP <= SK_CORE_STAND_HP -- the CORE's own
            HP-DELTA latch with the threshold `_core_stand_armed` uses.  ⛔ THE
            EXPRESSION IS RESTATED RATHER THAN CALLED, and the reason is an
            INSTRUMENT one: `_core_stand_armed` increments `stand_rounds`,
            which is LEVER 2's own dose column, and calling it from a body
            that is not standing anywhere would silently inflate another
            arm's instrument.  The weld is a unit control, not shared code.
          * Row #132 is why this term carries the HP THRESHOLD and not
            freshness alone: `corefire_fresh` alone measured TRUE in 139 of 139
            keeper-rung rounds, i.e. freshness alone is the always-fresh class
            and is not a gate at all.

        ⭐⭐ V2 AMENDMENT (a) -- `_under_attack` IS DROPPED, AND IT WAS DROPPED
        ON ITS OWN MUTATION CONTROL RATHER THAN ON AN ARGUMENT.  v1 ANDed the
        slot-1 PRESENCE latch in front of the HP term and the whole of PIECE 3
        then measured UNPLAYED: byte-identical tapes, 0 of 30 cells, `qy = 0`
        and `qn = 119` on the traced cells -- the gate refused every hold-branch
        round there was.  M8U (drop ONLY the presence term, keep the HP term)
        attributed it exactly: `qy` 0 -> 108, `qn` 119 -> 11, succession sites
        0 -> 1 and prep barriers 0 -> 2.  So the presence latch IS the row-#132
        always-fresh class on this rung -- a slot-1 beat is fresh for 50 rounds
        and something is always near our core -- while the surviving HP term
        still refuses 11 of 119.  ⇒ ONE TERM REMOVED, and the gate is still a
        gate: it is seen to refuse.  (M8, `SK_PUSH_ENG_QUIET` off, remains the
        control that drives the surviving term to `qn = 0`.)

        BOTH TAILS ARE COUNTED.  A gate that has only ever returned one
        verdict has not been seen to gate.
        """
        if not (SK_PUSH and SK_PUSH_ENGINEER):
            return False
        if not SK_PUSH_ENG_QUIET:
            self.push_quiet_yes += 1
            return True
        try:
            if (SK_COREFIRE and self.corefire_fresh(ct, rnd)
                    and self.corefire_hp(ct) <= SK_CORE_STAND_HP):
                self.push_quiet_no += 1
                return False
        except Exception:
            self.push_quiet_no += 1
            return False
        self.push_quiet_yes += 1
        return True

    def _push_succ(self, ct, p, rnd, live, want):
        """PIECE 3: OVERLAPPING SUCCESSION.  True if it took this turn.

        THE MEASURED DEFECT.  At or above the floor the engineer HOLDS STATION
        beside the newest tube (`_siege_engineer`'s hold branch) and
        `_plant_gun` leaves the just-built tile in `nest_site`.  So the
        replacement of a tube that dies starts from ZERO: re-site, walk, prep,
        then plant -- the 44-round sequential gap the wealthdiag names, against
        a median tube life of 42 rounds.  This rung spends the hold rounds on
        the NEXT site instead, so that when a barrel is knocked out the body is
        already standing on a prepared tile and the plant is one turn away.

        ⛔ IT DOES NOT PLANT AND IT DOES NOT RAISE `want`.  Plants above the
        pair stay `_battery_open`'s business under its ceiling and its eco
        latch; raising `want` here would also move `skip_prep`, `_plant_gun`'s
        SK_TUBE_FUND waiver and the post-plant re-arm -- three policies this
        arm has no mandate to change and which would make a result
        unattributable (arm 1's own note, and it applies unchanged).

        ⛔⛔ THE ONE HAZARD IT CREATES IS A PERMANENT SITE BAN, and it is the
        same one the burst rule paid for.  `_nest_site_watch` is a PROGRESS
        watchdog: a site the body has not closed on for SK_NEST_STUCK_ROUNDS
        rounds goes into `nest_bad` FOREVER, and a body that has ARRIVED and
        is deliberately standing still records no new closest approach.  So
        the arrival branch refreshes exactly the two clocks that watchdog runs
        on (`_b2_hold_clocks`, reused rather than copied -- the same two
        fields, the same reason).

        ⚠ THE COST, DISCLOSED: the body stops standing beside the standing
        tube.  On this baseline that costs nothing measurable -- the hold
        branch's only other rung is `_guard_heal`, which returns False on
        every SK_ROTATE-off round -- and PIECE 2(c) is what puts a medic
        beside the barrels instead.  On a rotation arm it would cost the
        babysit, and this rung is gated below that branch accordingly.
        """
        if not (SK_PUSH and SK_PUSH_ENGINEER):
            return False
        if self.role != SK_SIEGE_ENGINEER or self.enemy is None:
            return False
        if live < want:
            return False                # below the floor the ordinary path owns it
        if not self._push_quiet(ct, rnd):
            return False
        # (i) free a site whose tube already STANDS -- `_battery_rearm`'s own
        # ledger test, and the ledger is the right authority for the same
        # reason it gives: `get_tile_building_id` can raise out of bounds and
        # answers nothing useful out of vision.
        s = self.nest_site
        if s is not None:
            for t in self._nest_slots():
                if t is not None and t[1].x == s.x and t[1].y == s.y:
                    self._battery_rearm()
                    self.push_succ_rearm += 1
                    break
        # (ii) pick the successor site.  `_pick_nest` already excludes every
        # tile our standing tubes occupy (`_nest_taken`) and applies the pair
        # gap, so the successor cannot stack on the incumbent.
        if self.nest_site is None:
            self.nest_site = self._pick_nest(ct, p, rnd)
            if self.nest_site is None:
                return False
            self.push_succ_site += 1
            self.nest_best_d = None
            self.nest_since = rnd
            self.nest_anchor = None
            self.nest_anchor_rnd = rnd
            self._preprep_consume(rnd)
        site = self.nest_site
        # (iii) prep, hold, or walk.
        if abs(site.x - p.x) + abs(site.y - p.y) == 1:
            cd = 1
            try:
                cd = ct.get_action_cooldown()
            except Exception:
                cd = 1
            if (SK_PUSH_ENG_PREP and cd == 0
                    and self.nest_prepped < SK_NEST_PREP_BARRIERS
                    and not self._push_refuse(ct, rnd, EntityType.BARRIER,
                                              "succprep")
                    and self._prep_barrier(ct, p, site, rnd)):
                self.push_succ_prep += 1
                return True
            self.push_succ_hold += 1
            self._b2_hold_clocks(rnd)
            return True
        if self.step_to(ct, site):
            self.push_succ_walk += 1
            return True
        return False

    # ==================================================================
    # s57 BARRELS ARM 2 -- PROTECTION + SUCCESSION  (SK_BARREL_GUARD)
    #
    # GAME CONTEXT: in-engine behaviour of our own builder bots in the
    # Florent Code League, a sandboxed bot-vs-bot programming competition.
    # A "tube"/"barrel" is one of OUR sentinels standing in the band beside
    # the opposing bot's core; "knocked out" is the engine removing a piece
    # per its documented rules.
    #
    # THREE PIECES, ONE MASTER, EACH SEPARATELY ABLATABLE:
    #   (a) SK_BG_MEDIC -- the re-tasked home keeper nurses the barrels;
    #   (b) SK_BG_SUCC  -- the engineer's idle band rounds prep the SUCCESSOR;
    #   (c) SK_BG_SITE  -- the successor pick avoids their rays (addendum).
    # ==================================================================

    # --- (a) THE BARREL MEDIC -----------------------------------------

    def _bg_home_turrets(self, ct):
        """How many of OUR turrets stand AT HOME, by vision census.

        ⛔ A CENSUS, NOT A MEMORY, and PLANK 10's own disposition is why: a
        per-body ledger of what THIS body built names nothing after a
        replacement keeper walks into the role (each unit gets its own
        `Player`).  `vis_friend` is filled by `_sense` every round for every
        role, so this is an existing read with no new engine call: the keeper
        stands at home and the home turrets are what it is looking at.
        ⛔ HOME IS `GUARD_FWD_DSQ` OF OUR OWN CORE -- the same constant
        `_push_barrel` splits FORWARD tubes on, used here in the complement, so
        a turret is home to this method exactly when it is not a tube to that
        one.
        """
        if self.core is None:
            return 0
        n = 0
        for _eid, et, ep in self.vis_friend:
            if et not in TURRET_TYPES:
                continue
            if ep is None or not self.ibp(ep):
                continue
            if dsq_core(ep, self.core) <= GUARD_FWD_DSQ:
                n += 1
        return n

    def _bg_home_bodies(self, ct, rnd):
        """How many HOME-ANCHORED bodies are alive, off the beat slots.

        ⛔ THE SAME READ `_claim_role` RUNS ON (`beat_fresh` over
        `SK_SLOT_BEAT[role]`), so it is team-wide, never blind, costs one store
        read per role and adds no latch.  The CAGE WALKER is excluded on
        purpose -- its lap is enemy-anchored -- so this number is "the keeper
        plus the denier", and the bar of 2 means "the denier is alive".
        """
        n = 0
        for r in SK_BG_HOME_ROLES:
            if r >= SK_N_ROLES:
                continue
            try:
                if self.beat_fresh(ct, SK_SLOT_BEAT[r], rnd, SK_BEAT_STALE):
                    n += 1
            except Exception:
                continue
        return n

    def _bg_secure(self, ct, rnd):
        """THE POST-SECURITY READ: may the keeper leave home this round?

        THREE TERMS, EXISTING READS, NO NEW LATCH (class-audit row #132):
          * NO FRESH COREFIRE -- our core has not lost HP inside the last
            SK_COREFIRE_TTL rounds, off the core's own slot-15 HP-DELTA alarm.
            ⛔ THE HP-DELTA ALARM AND NOT THE SLOT-1 PRESENCE LATCH: the
            presence latch measured TRUE in 139 of 139 keeper-rung rounds and
            is the always-fresh class -- a term that is always true is not a
            gate.  This is also the RELEASE: the same predicate going fresh is
            what recalls the body, so the leave test and the come-home test
            cannot disagree.
          * HOME TURRET COUNT INTACT -- >= SK_BG_HOME_TURRETS of our turrets
            standing at home, by the vision census above.  Implemented as a
            FLOOR rather than a high-water mark because a remembered peak is a
            new latch (see the flag note).
          * >= SK_BG_HOME_BODIES HOME BODIES -- the beat census above.

        ⛔ BOTH TAILS ARE COUNTED, PER TERM.  A gate that has only ever
        returned one verdict has not been seen to gate, and a THREE-term gate
        that has only ever refused on one of them has two terms nobody has
        seen.
        """
        if SK_COREFIRE and self.corefire_fresh(ct, rnd):
            self.bg_sec_no_fire += 1
            return False
        if self._bg_home_turrets(ct) < SK_BG_HOME_TURRETS:
            self.bg_sec_no_turret += 1
            return False
        if self._bg_home_bodies(ct, rnd) < SK_BG_HOME_BODIES:
            self.bg_sec_no_body += 1
            return False
        self.bg_sec_yes += 1
        return True

    def _bg_claim(self, ct, p, rnd):
        """Is the re-task live THIS round?  Security AND a barrel to nurse."""
        if self.role != SK_BG_MEDIC_ROLE or self.enemy is None or self.core is None:
            return False
        try:
            live = self._push_live_tubes(ct, rnd)
        except Exception:
            return False                    # degraded read: stay home
        if live < 1:
            self.bg_no_tube += 1
            return False                    # nothing forward to nurse
        return self._bg_secure(ct, rnd)

    def _bg_medic_turn(self, ct, p, rnd):
        """Station in the band and heal the most damaged tube.  True if it
        spent the round.

        ⛔ THE SENSORS ARE THE WARDEN'S, REUSED RATHER THAN COPIED, and both
        are pure reads: `_push_barrel` (the vision census of damaged FORWARD
        sentinels) and `_push_station` (where the band is, with the patrol).
        ⛔⛔ AND `_push_station` IS WHY THIS RUNG EXISTS IN THIS SHAPE: the v3
        trace measured the medic reading `barrel = 0` for its whole life when
        it stood at the launcher seat, because a builder sees r^2 = 20 and the
        band sits at d^2 14-32 of their core.  THE STATION MUST BE IN THE BAND.
        ⛔ THE ACT IS `_heal_action`, the tree's existing verb (1 Ti -> +4 HP on
        the most-damaged adjacent friendly), so no new targeting is introduced.
        ⚠ DISCLOSED, and it is `_guard_heal`'s own trade: on a tile adjacent to
        both a damaged barrel and a MORE damaged prep barrier, the verb heals
        the barrier.  A screen that dies stops screening.
        ⛔ IT ENDS IN A FALL-THROUGH, NOT IN A PARKED BODY (v603 FIX 6(b): two
        bodies spent 860 and 227 rounds as paperweights): with nothing to heal
        and the body already on station this returns False and `_bg_yield` has
        the round.
        """
        tgt = self._push_barrel(ct, p)
        if tgt is None:
            stn = self._push_station(ct, p, rnd)
            if stn is None or p.distance_squared(stn) <= SK_PUSH_STATION_NEAR:
                return False                # on station, nothing to heal
            try:
                if ct.get_move_cooldown() != 0:
                    return False
            except Exception:
                return False
            if self.step_to(ct, stn):
                self.bg_walk += 1
                return True
            return False
        self.bg_seen += 1
        if p.distance_squared(tgt) == 1:            # orthogonally adjacent
            self.bg_heal_rounds += 1
            try:
                if ct.get_global_resources() < SK_BG_HEAL_FLOOR:
                    self.bg_poor += 1
                    return False
                if ct.get_action_cooldown() == 0 and self._heal_action(ct, p, rnd):
                    self.bg_heals += 1
                    return True
            except Exception:
                return False
            return False
        try:
            if ct.get_move_cooldown() != 0:
                return False
        except Exception:
            return False
        if self.step_to(ct, tgt):
            self.bg_walk += 1
            return True
        return False

    def _bg_yield(self, ct, p, rnd):
        """THE IDLE ROUND -- spent NOT BLOCKING THE ENGINEER.

        ⛔ THE ENGINE'S OWN RULE IS THE WHOLE TEST (`_push_w2_blocking`, reused
        verbatim): a building is placed on a tile ORTHOGONALLY ADJACENT to the
        builder placing it, so the four neighbours of a friendly builder are
        exactly its build menu, and a body parked on one has taken a tile off
        it.  The engineer is the builder this matters for -- it plants the
        replacement tube and lays its prep barriers in the band this medic
        stations in.
        ⛔ THE HEAL OUTRANKS THE YIELD (this rung is reached only when nothing
        is damaged), and BOTH TAILS ARE COUNTED: `bg_clear` is idle rounds
        already out of the way, `bg_yield` steps actually taken.
        """
        self.bg_idle += 1
        if not self._push_w2_blocking(ct, p):
            self.bg_clear += 1
            return
        try:
            if ct.get_move_cooldown() != 0:
                return
        except Exception:
            return
        best = None
        for d in CARDINALS:
            q = p.add(d)
            if not self.ibp(q):
                continue
            try:
                if not ct.is_tile_passable(q):
                    continue
            except Exception:
                continue
            if self.tile_owner(q) not in (OWNER_NONE, OWNER_DOOR):
                continue
            if self._push_w2_blocking(ct, q):
                continue
            key = (q.x, q.y)                        # canonical, so the step
            if best is None or key < best[0]:       # is deterministic
                best = (key, q)
        if best is None:
            return
        try:
            if self.step_to(ct, best[1]):
                self.bg_yield += 1
        except Exception:
            return

    def _bg_recall(self, ct, p, rnd):
        """THE RELEASE PATH, AND IT IS DISCLOSED IN FULL.

        The claim (`_bg_claim`) going False is the release -- most often
        because `corefire_fresh` went true, i.e. our core is ACTUALLY LOSING HP
        -- and it is evaluated on the SAME round, above the keeper's whole
        ladder, so "returns home immediately" is literal: the round the alarm
        fires is the round this body starts walking back.

        ⛔ WHY A WALK AND NOT A BARE FALL-THROUGH.  Handing the round straight
        to `_home_keeper` from a tile in the enemy's band would run the whole
        home ladder -- belt rungs, harvester rungs, the door -- from a position
        none of them were written for.  So while the body is outside
        SK_BG_HOME_DSQ of our core it does ONE thing, step toward the core, and
        the moment it is home the flag clears and every later round is the
        ordinary keeper turn, unchanged.
        ⛔ RETURNING False HANDS THE ROUND BACK rather than parking the body.
        """
        if self.core is None:
            self.bg_out = False
            return False
        if dsq_core(p, self.core) <= SK_BG_HOME_DSQ:
            self.bg_out = False
            self.bg_home_n += 1
            return False                # home: the ordinary keeper turn runs
        self.bg_recall_rounds += 1
        try:
            if ct.get_move_cooldown() != 0:
                return False
        except Exception:
            return False
        if self.step_to(ct, self.core):
            self.bg_recall_steps += 1
            return True
        return False

    def _bg_turn(self, ct, p, rnd):
        """PIECE (a)'s ENTIRE TURN.  True if it spent this body's round.

        ⛔ ONE CALL SITE, ABOVE THE ROLE SWITCH AND BELOW EVERY SURVIVAL
        BRANCH (the corefire answer, ledger V5, the citadel dispatch).  With
        the master off the first line returns False and the switch below is
        character-for-character the adopted tree.
        """
        if not (SK_BARREL_GUARD and SK_BG_MEDIC):
            return False
        if self.role != SK_BG_MEDIC_ROLE:
            return False
        if self._bg_claim(ct, p, rnd):
            if not self.bg_out:
                self.bg_out = True
                self.bg_out_n += 1
                self.bg_out_rnd = rnd
            self.bg_rounds += 1
            if self._bg_medic_turn(ct, p, rnd):
                return True
            self._bg_yield(ct, p, rnd)
            return True
        if self.bg_out:
            return self._bg_recall(ct, p, rnd)
        return False

    # --- (b) OVERLAPPING SUCCESSION -----------------------------------

    def _bg_succ(self, ct, p, rnd, live, want):
        """The engineer's IDLE band rounds prep the SUCCESSOR site.

        THE MEASURED DEFECT (wealthdiag): median tube life 42 rounds early and
        10 late, against a REPLACEMENT GAP of 44 rounds, and 11 overlapping
        successions against 28 sequential ones.  At or above the floor the
        engineer HOLDS STATION beside the newest tube and `_plant_gun` leaves
        the just-built tile in `nest_site`, so the replacement of a knocked-out
        tube starts from ZERO: re-site, walk, prep, then plant.  This rung
        spends the hold rounds on the NEXT site instead, so a knockout costs
        one turn and not a fresh commute.

        ⛔ IT IS A DOSE OF EXISTING MACHINERY, NOT NEW MACHINERY.  The site
        pick is `_pick_nest`, the prep is `_prep_barrier`, the watchdog refresh
        is `_b2_hold_clocks`, and THE PLANT IS NOT HERE AT ALL: when a tube
        goes down, `live` falls below `want`, the hold branch is not entered,
        and the engineer's ordinary buy path finds `nest_site` already set and
        this body already standing beside it -- so it plants THAT ROUND if the
        bank allows.  "Builds immediately if funded" is a consequence of having
        prepped, not a second code path.

        ⛔ IT DOES NOT PLANT AND IT DOES NOT RAISE `want`.  Raising `want` here
        would also move `skip_prep`, `_plant_gun`'s SK_TUBE_FUND waiver and the
        post-plant re-arm -- three policies this arm has no mandate to change
        and which would make a result unattributable.

        ⛔⛔ THE ONE HAZARD IT CREATES IS A PERMANENT SITE BAN, and it is the
        one the burst rule already paid for.  `_nest_site_watch` is a PROGRESS
        watchdog: a site the body has not closed on for SK_NEST_STUCK_ROUNDS
        rounds goes into `nest_bad` FOREVER, and a body that has ARRIVED and is
        deliberately standing still records no new closest approach.  The
        arrival branch therefore refreshes exactly the two clocks that watchdog
        runs on (`_b2_hold_clocks`, called rather than copied).

        ⚠ THE COST, DISCLOSED: the body stops standing beside the standing
        tube.  On this baseline that costs nothing measurable -- the hold
        branch's only other rung is `_guard_heal`, which returns False on every
        SK_ROTATE-off round -- and piece (a) is what puts a body beside the
        barrels instead.  On a rotation arm it would cost the babysit, which is
        why this rung is gated BELOW that branch's own call site.

        ⛔⛔ THE DEATH MEMO, AND THE DISCLOSURE IS DECIDABLE RATHER THAN
        HEDGED.  `_nest_scan` excludes a candidate tile when
        `rnd - nest_deaths[tile] < SK_DEATH_MEMO_ROUNDS`, and
        SK_DEATH_MEMO_ROUNDS is 400.  ⇒ A TILE THAT LOST A TUBE CANNOT BE
        RE-USED BY THE SUCCESSOR PICK INSIDE THE KILL WINDOW ON ANY CELL: the
        programme's window closes at r300 and 400 > 300 by construction, and on
        the adopted 30-cell f1 baseline 22 of 30 cells do not even RUN for 400
        rounds.  Re-use is therefore not a live behaviour of this piece; what
        IS live is arm 1's finding that the memo makes successive sites walk
        OUTWARD.  SK_BG_SUCC_NEAR is this piece's answer (nearness-first
        ordering, a reordering of the same legal set), and piece (c) is
        Magnus's -- prefer tiles their guns do not bear on, rather than merely
        tiles that have not yet lost a tube.  `nest_bad` (permanent) is NOT
        touched by any of it.
        """
        if not (SK_BARREL_GUARD and SK_BG_SUCC):
            return False
        if self.role != SK_SIEGE_ENGINEER or self.enemy is None:
            return False
        if live < SK_BG_SUCC_LIVE:
            self.bg_succ_low += 1
            return False
        self.bg_succ_rounds += 1
        # (i) free a site whose tube already STANDS -- `_battery_rearm`'s own
        # ledger test, and the ledger is the right authority for the reason it
        # gives: `get_tile_building_id` can raise out of bounds and answers
        # nothing useful out of vision.
        s = self.nest_site
        if s is not None:
            for t in self._nest_slots():
                if t is not None and t[1].x == s.x and t[1].y == s.y:
                    self._battery_rearm()
                    self.bg_succ_rearm += 1
                    break
        # (ii) pick the successor.  `_pick_nest` already excludes every tile our
        # standing tubes occupy (`_nest_taken`) and applies the pair gap, so the
        # successor cannot stack on the incumbent.
        if self.nest_site is None:
            self.nest_site = self._pick_nest(ct, p, rnd, near=SK_BG_SUCC_NEAR)
            if self.nest_site is None:
                self.bg_succ_nosite += 1
                return False
            self.bg_succ_site += 1
            self.nest_best_d = None
            self.nest_since = rnd
            self.nest_anchor = None
            self.nest_anchor_rnd = rnd
            self._preprep_consume(rnd)
        site = self.nest_site
        # (iii) prep, hold, or walk.
        if abs(site.x - p.x) + abs(site.y - p.y) == 1:
            try:
                cd = ct.get_action_cooldown()
            except Exception:
                cd = 1
            if (cd == 0 and self.nest_prepped < SK_NEST_PREP_BARRIERS
                    and self._prep_barrier(ct, p, site, rnd)):
                self.bg_succ_prep += 1
                return True
            self.bg_succ_hold += 1
            self._b2_hold_clocks(rnd)
            # ⭐⭐ s57 BARRELS ARM 3 (SK_BG_ENGHEAL) -- CALL SITE 1, AND IT IS
            # THE TRUE IDLE TERMINAL.  Reaching here means: a successor site is
            # picked, this body is standing orthogonally beside it, and prep is
            # either finished or declined this round -- no plant, no prep, no
            # move pending.  The hold clock is already refreshed above, so the
            # rung inherits the watchdog protection whether it heals, steps or
            # declines.  The return value is True either way (the round was
            # always a hold round and `bg_succ_hold` still counts it, so the
            # arm-2 column stays comparable to the t_bg_* baseline); what
            # changes is what the round DOES.  ⛔ Flag off -> False on the
            # rung's first line -> t_bg_* behaviour character for character.
            self._bg_engheal(ct, p, rnd, cs=1)
            return True
        if self.step_to(ct, site):
            self.bg_succ_walk += 1
            return True
        return False

    # --- ARM 3: THE ENGINEER SELF-HEAL (SK_BG_ENGHEAL, staffing form 4) ------

    def _bg_engheal(self, ct, p, rnd, cs=1, allow_step=True):
        """THE ENGINEER'S IDLE BAND ROUND BUYS +4 HP ON AN ADJACENT TUBE.

        GAME CONTEXT: in-engine mechanics of the Florent Code League, a
        sandboxed bot-vs-bot competition.  The "tube" is one of our own
        sentinels standing in the band beside the opposing bot's core; the heal
        is the engine's documented `heal()` verb (1 Ti -> +4 HP, orthogonally
        adjacent only).

        ⛔ WHY THIS BODY AND NOT ANOTHER -- STAFFING FORM 4 OF 4, AND THE THREE
        REFUSALS ARE THE ARGUMENT.  Form 1 (the cage walker) deleted the second
        siege body, wins 12 -> 5.  Form 2/3 (a fresh spawn) paid +20% on the ONE
        GLOBAL ADDITIVE cost-scale factor.  Form 3 as built (the re-tasked HOME
        KEEPER, SK_BG_MEDIC) delivered ZERO heals over the whole grid: it is a
        WALK-BOUND staffing -- 44-140 rounds walking out plus corefire recall
        round-trips -- and it is the belt publisher, whose absence measured -35%
        mined.  THE ENGINEER IS ALREADY STANDING IN THE BAND, PUBLISHES NOTHING,
        AND THE ROUNDS THIS RUNG SPENDS ARE ROUNDS IT WAS ABOUT TO SPEND
        STANDING STILL.  All three refuted costs are zero here by construction,
        which is the entire case for form 4.

        ⛔ WHERE IT IS CALLED FROM -- THE TRUE IDLE TERMINAL, AND FINDING IT IS
        HALF THE BUILD.  "Below the succession" is NOT enough: `_bg_succ`
        RETURNS TRUE on its hold branch, so a rung placed under its call site
        would be unreachable on exactly the rounds it is registered for.  The
        hold branch's own idle round (successor site picked, body standing on
        it, prep done or refused) is CALL SITE 1, and the place the main hold
        branch lands when `_bg_succ` declines is CALL SITE 2.

        ⛔⛔ AND CALL SITES 1 AND 2 ARE MEASURED EMPTY -- CALL SITE 3 IS WHERE
        THE POPULATION ACTUALLY IS, AND IT WAS FOUND BY MEASUREMENT, NOT BY
        READING.  The opportunity census (`bg2build_opp.py`, a diagnostic tree
        that taps the top of EVERY siege-engineer round on 12 population-bearing
        cells) reads 5,165 engineer rounds, 31 of them with a damaged forward
        tube ORTHOGONALLY ADJACENT, 552 of them at the sites-1-and-2 terminal --
        and **the intersection is 0 of 31**.  The anti-correlation has a stated
        cause rather than being an accident of the sample: the hold branch is
        gated on `live >= want`, a tube is damaged precisely while the opponent
        is shooting it, and a shot tube usually goes down -- which drops `live`
        BELOW `want` and puts the engineer on the buy path, not the hold branch.
        Every cell with adjacency rounds reads terminal 0 (fimbulwinter B 17/0,
        glacierkeep B 6/0, bifrost A 3/0) and every cell with a large terminal
        reads adjacency 0 (stavkirke A 0 adj / 186 term, jotunheim A 0 / 173).
        ⇒ CALL SITE 3 IS THE NO-SITE FALLBACK TERMINAL: `nest_site is None`
        after `_pick_nest` declined, i.e. nothing to site, nothing to prep,
        nothing to plant, immediately above `_attack_enemy_core`.  21 of the 31
        adjacency rounds are exactly there, and 29 of the 31 spent NO ACTION at
        all (the next round's action cooldown is still 0), so the round the heal
        takes is a round the engineer was not spending.

        ⛔ CALL SITE 3 TAKES THE ADJACENT HEAL ONLY, NEVER THE BOUNDED STEP
        (`allow_step=False`).  A step there would compete with the fallback's
        own nav for the same round, and "no walk" is the whole reason form 4
        exists.  Sites 1 and 2 keep the step because the body is holding, not
        travelling.

        ⚠ DISCLOSED, and it is the one precedence this arm takes from an
        existing rung: at call site 3 a delivered heal preempts
        `_attack_enemy_core` for that round.  It fires only when a damaged
        forward tube is already orthogonally adjacent, so the trade is one
        builder peck (2 damage to their core, 2 Ti) against +4 HP on a sentinel
        that is doing 18 a shot at that same core.  It is bounded by the same
        adjacency the verb needs and it is counted separately (`bge_h3`).

        ⛔ NO NEW SENSOR AND NO NEW VERB.  The census is `_push_barrel` (the
        warden's own vision census of damaged FORWARD friendly sentinels,
        `miss >= 4` so a +4 heal is never waste) and the act is `_heal_action`
        (the tree's existing verb, most-damaged adjacent friendly, its own
        `< 2 Ti` floor).  ⚠ DISCLOSED, and it is `_guard_heal`'s own trade
        inherited verbatim: on a tile adjacent to BOTH a damaged tube and a MORE
        damaged prep barrier the verb heals the barrier.  A screen that dies
        stops screening, so this is not obviously the wrong pick -- but it is
        not the pick the bar names, and `bge_heals` therefore counts HEALS
        DELIVERED, not tube HP restored.

        ⛔ THE BOUNDED STEP IS THE ONLY THING HERE THAT COSTS A ROUND OF
        POSITION, AND ITS BOUND IS THREE INDEPENDENT REFUSALS: the short radius
        (SK_BG_ENGHEAL_NEAR), the per-episode budget (SK_BG_ENGHEAL_STEPS,
        keyed on the target TILE so it cannot be laundered by re-targeting),
        and the BAND TEST ON THE DESTINATION TILE ITSELF -- the step is chosen
        by this method rather than by the nav precisely so the band test can be
        applied to the tile the body will actually stand on.  The hold clock is
        refreshed on every step taken, because `_nest_site_watch` is a PROGRESS
        watchdog and a body that steps sideways records no new closest approach:
        without it the successor tile goes into `nest_bad` PERMANENTLY.

        ⚠ THE COST, DISCLOSED: at the succession call site the heal takes the
        action cooldown, which is the same cooldown the NEXT round's prep
        barrier would use.  It is reached only when prep already declined this
        round (quota met, or `_prep_barrier` found no legal tile) or the
        cooldown was already busy -- in the busy case this rung refuses too --
        so the round it spends is not a round prep asked for.  Where the quota
        is met there is no future prep to delay at all.

        ⛔ FLAG OFF -> False on the first line, zero engine calls, byte-exact.
        """
        if not (SK_BARREL_GUARD and SK_BG_ENGHEAL):
            return False
        if self.role != SK_SIEGE_ENGINEER or self.enemy is None:
            return False
        self.bge_rounds += 1
        self.bge_cs[cs] += 1
        tgt = self._push_barrel(ct, p)
        if tgt is None:
            self.bge_none += 1
            self.bge_walk_tile = None       # the episode dies with its target
            self.bge_walk_n = 0
            return False
        self.bge_seen += 1
        d = p.distance_squared(tgt)
        if d == 1:                          # orthogonally adjacent: the verb
            self.bge_adj += 1
            self.bge_walk_tile = None
            self.bge_walk_n = 0
            try:
                if ct.get_global_resources() < SK_BG_HEAL_FLOOR:
                    self.bge_poor += 1
                    return False
                if ct.get_action_cooldown() != 0:
                    self.bge_busy += 1
                    return False
                if self._heal_action(ct, p, rnd):
                    self.bge_heals += 1
                    self.bge_cs_heals[cs] += 1
                    return True
            except Exception:
                return False
            self.bge_nover += 1
            return False
        if not allow_step:                  # ⛔ CALL SITE 3: the heal, no walk
            self.bge_nostep += 1
            return False
        if d > SK_BG_ENGHEAL_NEAR:          # out of the short radius: LEFT ALONE
            self.bge_far += 1
            self.bge_walk_tile = None
            self.bge_walk_n = 0
            return False
        self.bge_near += 1
        key = (tgt.x, tgt.y)
        if self.bge_walk_tile != key:       # a new target opens a new episode
            self.bge_walk_tile = key
            self.bge_walk_n = 0
        if self.bge_walk_n >= SK_BG_ENGHEAL_STEPS:
            self.bge_step_cap += 1
            return False
        try:
            if ct.get_move_cooldown() != 0:
                return False
        except Exception:
            return False
        best = None
        for dd in CARDINALS:
            q = p.add(dd)
            if not self.ibp(q):
                continue
            dq = q.distance_squared(tgt)
            if dq >= d:
                continue                    # the step must CLOSE on the target
            dband = dsq_core(q, self.enemy)
            if dband < SK_NEST_DSQ_MIN or dband > SK_NEST_DSQ_MAX:
                continue                    # ⛔ IT MAY NOT LEAVE THE BAND
            try:
                if not ct.is_tile_passable(q):
                    continue
            except Exception:
                continue
            k = (dq, q.x, q.y)              # canonical -> deterministic
            if best is None or k < best[0]:
                best = (k, q)
        if best is None:
            self.bge_step_band += 1
            return False
        if self.step_to(ct, best[1]):
            self._b2_hold_clocks(rnd)       # ⛔ NOT OPTIONAL: see the docstring
            self.bge_steps += 1
            self.bge_walk_n += 1
            return True
        return False

    # --- (c) THE SITE GUARD (Magnus's addendum) -----------------------

    def _bg_site_class(self, taken):
        """Is this pick a SUCCESSOR pick?  Both tails counted.

        ⛔ THE OPENING PLANT IS OUT OF SCOPE BY CONSTRUCTION.  A pick counts as
        a successor when a tube already stands (`taken`) or one has already been
        knocked out (`nest_deaths`); at r0 neither is true, so the first tube --
        the one every other plank depends on -- is sited exactly as today.
        """
        if not (SK_BARREL_GUARD and SK_BG_SITE):
            return False
        on = bool(taken) or bool(self.nest_deaths)
        if on:
            self.bg_site_on += 1
        else:
            self.bg_site_off += 1
        return on

    def _bg_dir(self, delta):
        """(dx, dy) -> the Direction with that delta, or None."""
        for d in DIRECTIONS:
            if d.delta() == delta:
                return d
        return None

    def _bg_guns(self, ct):
        """[(pos, Direction, EntityType)] for up to SK_BG_SITE_MAX_GUNS of the
        opposing bot's turrets, nearest THEIR core first.

        ⛔ VISIBLE TURRETS FIRST, THEN THE TILE-KEYED MEMO.  `vis_enemy` carries
        this round's sighting and `get_direction` is readable for anything in
        vision; `armed_memo` / `armed_facing` (written by `_sense` since v601,
        keyed on the TILE because a turret is a building and cannot move) carry
        the ones we have walked away from.
        ⚠ FAIL OPEN, AND IT IS THE ONLY HONEST DIRECTION: a turret we have never
        seen is unknowable, so the guard simply does not price it.  Under-
        marking costs this arm its effect on that tile; over-marking would cost
        a plant.  A gunner can also ROTATE, so a remembered facing is a
        hypothesis for a gunner and a fact for a sentinel (sentinels cannot
        rotate) -- both are used, and the confirm column measures the engine's
        own verdict on the chosen tile.
        ⛔ THE CAP IS A CPU BOUND: each unit has 10ms a turn.
        """
        out = []
        seen = set()
        for eid, et, ep in self.vis_enemy:
            if et not in TURRET_TYPES or ep is None or not self.ibp(ep):
                continue
            try:
                face = ct.get_direction(eid)
            except Exception:
                continue
            if face is None or face == Direction.CENTRE:
                continue
            out.append((ep, face, et, dsq_core(ep, self.enemy)))
            seen.add((ep.x, ep.y))
        for xy, v in self.armed_memo.items():
            if xy in seen or v[0] not in TURRET_TYPES:
                continue
            f = self.armed_facing.get(xy)
            if f is None:
                continue
            face = self._bg_dir(f)
            if face is None:
                continue
            q = Position(xy[0], xy[1])
            if not self.ibp(q):
                continue
            out.append((q, face, v[0], dsq_core(q, self.enemy)))
        out.sort(key=lambda t: (t[3], t[0].x, t[0].y))
        return [(q, f, et) for q, f, et, _d in out[:SK_BG_SITE_MAX_GUNS]]

    def _bg_cover(self, ct, guns):
        """The set of tiles those turrets bear on, from the ENGINE's own attack
        pattern.

        ⛔ `get_attackable_tiles_from(pos, facing, kind)` IS THE ENGINE'S
        HYPOTHETICAL-TURRET PATTERN -- one call per turret, not per candidate.
        The registered checker is `can_fire_from`; asking it per candidate is up
        to 256 x 4 = 1024 engine calls inside ONE `_nest_scan` sweep against a
        10ms budget, which is how a unit loses its turn.  So the SET is built
        from the pattern getter and the CHOSEN tile is re-asked with
        `can_fire_from` (`SK_BG_SITE_CONFIRM`) -- two independent engine
        predicates, with their agreement reported rather than assumed.
        """
        cover = set()
        for q, face, et in guns:
            try:
                tiles = ct.get_attackable_tiles_from(q, face, et)
            except Exception:
                continue
            for t in tiles:
                cover.add((t.x, t.y))
        self.bg_cover_guns += len(guns)
        self.bg_cover_n += len(cover)
        return cover

    def _bg_confirm(self, ct, guns, cover, site):
        """The CROSS-PREDICATE CONTROL on the chosen tile only.

        Counts agreement between `can_fire_from(turret, facing, kind, site)`
        (Magnus's named checker) and membership of `site` in the set built from
        `get_attackable_tiles_from`.  ⛔ IT TAKES NO DECISION -- a disagreement
        is a column, not a veto -- so it cannot change what is planted; what it
        can do is refute the substitution above, which is the point.
        """
        if not SK_BG_SITE_CONFIRM or site is None:
            return
        inset = (site.x, site.y) in cover
        hit = False
        for q, face, et in guns:
            try:
                if ct.can_fire_from(q, face, et, site):
                    hit = True
                    break
            except Exception:
                continue
        if hit == inset:
            self.bg_confirm_ok += 1
        else:
            self.bg_confirm_bad += 1
        if inset:
            self.bg_site_covered += 1
        else:
            self.bg_site_clear += 1

    def _bg_killer_ban(self, ct, site, rnd):
        """A tube was knocked out on `site`: ban what its KILLERS cover.

        ⛔⛔ THIS IS THE ANSWER TO SERIAL DEATH BY THE SAME GUN, and it is the
        half the DEATH MEMO cannot do: the memo bans the TILE that died, so the
        next site walks one tile outward and stands in the SAME ray.  This bans
        the RAY, for SK_BG_SITE_BAN_ROUNDS rounds.
        ⛔ THE BEARING TEST IS `can_fire_from(turret, its facing, its type,
        site)` -- the engine's own predicate, one call per consulted turret,
        once per knockout.  Only turrets that actually BEAR ON the died tile
        contribute; a gun elsewhere on the board bans nothing.
        ⛔⛔ IT IS BOUNDED AND IT NEVER WRITES `nest_bad`.  `nest_bad` is
        PERMANENT, and arm 1's refutation measured exactly what permanent bans
        do -- "loss cells plant far because the death memo bans each knocked-out
        tile and successive sites walk outward".  A ban that expires cannot
        compound into that spiral, and `_pick_nest` retries WITHOUT the ban
        before any existing fallback runs, so the guard can never empty a band
        that today would have yielded a site.
        """
        if not (SK_BARREL_GUARD and SK_BG_SITE):
            return
        guns = self._bg_guns(ct)
        if not guns:
            return
        bearing = []
        for q, face, et in guns:
            try:
                if ct.can_fire_from(q, face, et, site):
                    bearing.append((q, face, et))
            except Exception:
                continue
        if not bearing:
            return
        cover = self._bg_cover(ct, bearing)
        if not cover:
            return
        self.bg_ban_n += 1
        self.bg_ban_tiles += len(cover)
        exp = rnd + SK_BG_SITE_BAN_ROUNDS
        for xy in cover:
            if self.bg_ban.get(xy, -1) < exp:
                self.bg_ban[xy] = exp

    def _bg_ban_set(self, rnd):
        """The live half of the bounded ban, expiring entries as it goes."""
        if not self.bg_ban:
            return None
        dead = [xy for xy, e in self.bg_ban.items() if e <= rnd]
        for xy in dead:
            del self.bg_ban[xy]
        return set(self.bg_ban) if self.bg_ban else None

    # ==================================================================
    # s57 VOLUME ARM 1, PIECE (a) -- THE TWO-BOT COLUMN  (SK_VH_COLUMN)
    # ==================================================================
    # GAME CONTEXT: in-engine mechanics of the Florent Code League, a
    # sandboxed bot-vs-bot competition on a simulated grid.  "column",
    # "leader", "trailer", "handoff" are two of our own builder pieces
    # walking one behind the other and one of them placing a building on a
    # tile the other has vacated, with the engine's own `move`/`build`
    # verbs.  Nothing here reaches outside the simulated grid.
    #
    # THE PER-ROUND CHOREOGRAPHY, WRITTEN OUT, because "the same round" is
    # the whole claim and it depends on an ordering nobody chose:
    #
    #   round r   ENGINEER (leader, role 3)
    #               head: beat -> slot 13 bits 0-10
    #               head: `_vh_publish` -> slot 13 bits 0-20 (beat + site),
    #                     ONE word, whole-word write (buffered-write rule)
    #               turn: unchanged -- prep / plant / walk
    #   round r+1 DENIER (trailer, role 2)          <-- +1: writes are
    #               `_vh_turn` reads slot 13, sees beat fresh and a site         buffered
    #               security read (`_bg_secure`) -> may it leave home?
    #               orthogonally adjacent to the site?  -> `_plant_gun`
    #               otherwise -> one step toward the TRAIL SEAT (the site's
    #                            cardinal neighbour on OUR side: "one tile
    #                            behind" in column terms)
    #
    # ⛔⛔ THE UNIT-CONTROL, AND IT IS THE HALF T13 CANNOT GIVE US.  `run()`
    # is called once per living unit per round in an order the ENGINE picks.
    # T13's same-round handoff needs the LEADER's turn to run BEFORE the
    # TRAILER's.  Our two bodies are spawned r0-r3 in role order, so the
    # DENIER's entity id is the LOWER of the two -- and the measured turn
    # order on this engine is by entity id ascending (build report, the
    # ORDER column, measured from a tracer that prints `rnd,id` from both
    # bodies).  ⇒ ON THIS TREE THE TRAILER RUNS FIRST, so a leader that has
    # to vacate costs the handoff ONE round, not zero.  That is written down
    # rather than papered over, and it is why the PRIMARY path of this arm
    # does not depend on the vacate at all: our engineer plants from an
    # orthogonally adjacent tile and does not stand on its own site, so the
    # ordinary column is trailer-builds-on-arrival with no handoff needed.
    # The vacate rung (SK_VH_VACATE) exists for the one measured case where
    # the leader IS on the tile (an unfunded engineer falling through to
    # `step_to(site)`), and it is written so that the build lands the same
    # round if the order is ever the other way round.
    #
    # ⛔ FAIL-OPEN IS BY CONSTRUCTION, NOT BY POLICY.  With no eligible
    # second body -- role dead, beat stale, security refused, budget spent --
    # `_vh_turn` returns False on its own first rungs and the ENGINEER's path
    # is character-for-character the adopted tree plus one store write whose
    # bits nothing else reads.

    def _vh_pair_site(self):
        """The engineer's committed site, IF it is a PAIR site.

        ⛔ PURE: `nest_site` is this body's own field and `_nest_taken()` is
        this body's own plant ledger, so the publish costs no engine call
        beyond the single `wstore` it feeds.
        """
        s = self.nest_site
        if s is None:
            return None
        taken = self._nest_taken()
        if SK_VH_PAIR_ONLY and not taken:
            return None
        # ⛔⛔ AND THE SITE MUST NOT ALREADY CARRY A TUBE.  `_plant_gun` leaves
        # the JUST-BUILT tile in `nest_site` when the floor is met (the hold
        # branch's own documented behaviour), so the naive publish would send
        # the trailer across the map to a tile that already has our sentinel on
        # it -- a march that can only ever end in a refused build.  MEASURED
        # before this line existed: trailer claims 26 rounds, walks 25 steps,
        # reaches orthogonal adjacency 0 times, plants 0 (vh1build trace,
        # bifrost seat A).  The test is the ledger this method already holds.
        for t in taken:
            if t.x == s.x and t.y == s.y:
                return None
        return s

    def _vh_publish(self, ct, rnd):
        """WRITER: the SIEGE ENGINEER, into its OWN beat slot (13).

        ⛔⛔ WHOLE-WORD, NEVER READ-MODIFY-WRITE.  Store writes are buffered:
        `read_store` inside the same round returns LAST round's word, so a
        second same-round write that read the beat back to preserve it would
        publish a STALE beat and freeze this body's liveness signal for every
        `beat_fresh` reader in the tree.  The beat is therefore re-derived
        here -- `(rnd + 1) & SK_BEAT_MASK` is character for character what
        `beat()` wrote at the top of this same turn.
        ⛔ AND IT WRITES EVERY ROUND, SITE OR NO SITE.  A publish that only
        fired when a site existed would leave the previous site standing in
        bits 11-20 forever (the head `beat()` preserves upper bits by
        construction), and the trailer would march on a tile the engineer
        gave up ten rounds ago.
        """
        s = self._vh_pair_site()
        word = (rnd + 1) & SK_BEAT_MASK
        if s is not None:
            word |= pack_tile(s) << SK_VH_FIELD
            self.vh_pub += 1
        else:
            self.vh_pub_none += 1
        self.wstore(ct, SK_SLOT_BEAT[SK_SIEGE_ENGINEER], word)

    def _vh_lead_site(self, ct, rnd):
        """READER: the trailer's view of the leader's committed pair site.

        ⛔ THE BEAT IS THE LIVENESS TEST AND IT IS THE TREE'S OWN
        (`beat_fresh`, SK_VH_STALE = SK_BEAT_STALE): a dead or silent
        engineer publishes nothing, its beat goes stale, and the trailer
        stops marching rather than walking to a tile nobody is siting.
        ⛔ BOTH TAILS ARE COUNTED per refusal, because a gate that has only
        ever returned one verdict has not been seen to gate.
        """
        try:
            word = ct.read_store(SK_SLOT_BEAT[SK_SIEGE_ENGINEER])
        except Exception:
            return None
        b = word & SK_BEAT_MASK
        if b == 0 or rnd - (b - 1) > SK_VH_STALE:
            self.vh_stale += 1
            return None
        q = unpack_tile((word >> SK_VH_FIELD) & 0x3FF)
        if q is None or not self.ibp(q):
            self.vh_no_site += 1
            return None
        return q

    def _vh_trail_seat(self, site):
        """"ONE TILE BEHIND": the site's cardinal neighbour on OUR side.

        Pure geometry off `self.core` -- zero engine calls, never stale.  It
        is the exact complement of `_guard_seat` (the site's cardinal
        neighbour toward the ENEMY, which is where the leader ends up), so
        the two bodies stand on opposite faces of the tile and neither is in
        the other's build menu.  Returns None -- the caller then walks at the
        site itself -- when there is no core fix, no cardinal step, or the
        seat is off-map.
        """
        if site is None or self.core is None:
            return None
        try:
            d = site.cardinal_direction_to(self.core)
        except Exception:
            return None
        if d is None or not d.is_cardinal():
            return None
        q = site.add(d)
        if not self.ibp(q):
            return None
        return q

    def _vh_episode(self, site, rnd):
        """The walk budget, keyed on the SITE TILE, both verdicts counted.

        Returns True while this body may still spend rounds on `site`.  An
        episode that runs out bans the tile for THIS BODY for SK_VH_GIVEUP
        rounds and the round falls through to the ordinary denier ladder --
        the walk-budget lesson from staffing form 3, which was refused for
        44-140 rounds out of position.
        """
        xy = (site.x, site.y)
        exp = self.vh_ban.get(xy)
        if exp is not None:
            if exp > rnd:
                self.vh_banned += 1
                return False
            del self.vh_ban[xy]
        if self.vh_ep_site != xy:
            self.vh_ep_site = xy
            self.vh_ep_start = rnd
            self.vh_ep_n += 1
            return True
        if rnd - self.vh_ep_start > SK_VH_WALK_MAX:
            self.vh_ban[xy] = rnd + SK_VH_GIVEUP
            self.vh_ep_site = None
            self.vh_give += 1
            return False
        return True

    def _vh_sticky(self, rnd):
        """The LIVE episode's own site, for the rounds the publisher is silent.

        ⛔ IT ADDS NO CLOCK: the episode fields (`vh_ep_site`, `vh_ep_start`)
        and the bound (SK_VH_WALK_MAX) are `_vh_episode`'s own, already
        registered.  ⛔ AND IT CANNOT OUTLIVE THE BUDGET: past it this returns
        None and the next published read opens a fresh episode, so a body can
        never be held on a dead plan indefinitely.
        """
        xy = self.vh_ep_site
        if xy is None:
            return None
        if rnd - self.vh_ep_start > SK_VH_WALK_MAX:
            return None
        q = Position(xy[0], xy[1])
        return q if self.ibp(q) else None

    def _vh_turn(self, ct, p, rnd):
        """THE TRAILER'S ENTIRE TURN.  True if it spent this body's round.

        ⛔ ONE CALL SITE, immediately below the barrel medic's and therefore
        below every survival branch (the corefire answer, ledger V5, the
        citadel dispatch) and above the role switch.  With the master off the
        first line returns False and the switch below is
        character-for-character the adopted tree.
        ⛔ IT RETURNS False RATHER THAN PARKING THE BODY on every refusal.
        The denier's ordinary ladder is enemy-anchored and written for
        exactly the positions this rung leaves it in, so there is no recall
        walk here and no paperweight (v603 FIX 6(b): two bodies spent 860 and
        227 rounds as paperweights).
        """
        if not (SK_VOLUME and SK_VH_COLUMN):
            return False
        if self.role != SK_VH_ROLE:
            return False
        if self.enemy is None or self.core is None:
            return False
        site = self._vh_lead_site(ct, rnd)
        if site is None:
            # ⭐⭐ THE COLUMN IS STICKY FOR THE LENGTH OF ITS EPISODE, AND THIS
            # IS THE DEFECT THE FIRST TRACE MEASURED.  The engineer's published
            # field is EMPTY on most rounds (it holds a site only while it is
            # actively siting), and without this rung the trailer handed those
            # rounds back to the ordinary denier ladder -- whose target is
            # home-anchored ore -- so the two authorities fought over one body
            # and it OSCILLATED instead of travelling.  MEASURED on bifrost
            # seat A before this rung existed: 26 claimed rounds, 25 steps
            # taken, net displacement ~0 (x oscillating between 1 and 6 for
            # ~70 rounds), orthogonal adjacency reached 0 times, 0 plants.
            # ⛔ IT IS A BOUNDED LATCH AND THE BOUND IS THE ONE ALREADY
            # REGISTERED: the episode's own walk budget (SK_VH_WALK_MAX), after
            # which `_vh_episode` bans the tile and the body is released.  No
            # new clock, no new constant -- and it is what makes that budget
            # BIND rather than decorate (its mutation control M3 read SAME on
            # 5 of 5 cells before this rung, i.e. the budget was unreachable).
            site = self._vh_sticky(rnd)
            if site is None:
                return False
            self.vh_sticky += 1
        # ⛔ THE SECURITY READ IS ARM 2's, REUSED AND NOT COPIED: no fresh
        # corefire alarm, the home turret floor intact, and both home roles
        # alive.  ⚠ DISCLOSED: it increments arm 2's own `bg_sec_*` taps, and
        # this arm therefore keeps its OWN `vh_sec_*` pair so the column's
        # verdict share stays readable even though the shared taps now have a
        # second caller.  (SK_BG_MEDIC ships False, so on the adopted
        # baseline those taps are otherwise all zero.)
        if not self._bg_secure(ct, rnd):
            self.vh_no_sec += 1
            return False
        self.vh_sec_yes += 1
        if not self._vh_episode(site, rnd):
            return False
        self.vh_claim += 1
        # --- the build half: orthogonally adjacent is the engine's rule ----
        if abs(site.x - p.x) + abs(site.y - p.y) == 1:
            self.vh_adj += 1
            try:
                if ct.get_action_cooldown() == 0:
                    live = self._floor_live(ct, rnd)
                    want = SK_NEST_PAIR_N if SK_NEST_PAIR else 1
                    if self._plant_gun(ct, p, site, rnd, live, want):
                        self.vh_plant += 1
                        self.vh_ep_site = None
                        return True
                    self.vh_blocked += 1
            except Exception:
                return False
            return False
        # --- the walk half: close on the TRAIL SEAT, else on the site -----
        tgt = self._vh_trail_seat(site) or site
        try:
            if ct.get_move_cooldown() != 0:
                return False
        except Exception:
            return False
        if self.step_to(ct, tgt):
            self.vh_walk += 1
            return True
        return False

    def _vh_trailer_beside(self, ct, site):
        """Is a FRIENDLY builder bot (not us) orthogonally adjacent to `site`?

        ⛔ THE ENGINE'S OWN RULE IS THE TEST: a building is placed on a tile
        ORTHOGONALLY ADJACENT to the builder placing it, so the four cardinal
        neighbours of the site are exactly the tiles a trailer could build
        from.  ⛔ BOUNDED: at most 4 `get_tile_builder_bot_id` plus 4
        `get_team` calls, and it is reached only on the rounds the engineer is
        STANDING ON its own site -- which is the rare fall-through case, not
        the ordinary plant.
        ⛔ EVERY COMPUTED POSITION PASSES `ibp` BEFORE ANY `get_tile_*`
        (`is_in_vision` is NOT a bounds guard -- project CLAUDE.md, s50).
        """
        me = None
        try:
            me = ct.get_id()
        except Exception:
            return False
        for d in CARDINALS:
            q = site.add(d)
            if not self.ibp(q):
                continue
            try:
                bid = ct.get_tile_builder_bot_id(q)
                if bid is None or bid == me:
                    continue
                if ct.get_team(bid) == self.team:
                    return True
            except Exception:
                continue
        return False

    def _vh_vacate(self, ct, p, site, rnd):
        """T13's LITERAL RUNG -- THE LEADER STEPS OFF THE SITE TILE.

        Fires only when this body is standing ON its own committed site AND a
        friendly builder is orthogonally adjacent to that site, i.e. exactly
        when the leader's own body is what is blocking the trailer's build.
        The step is to `_guard_seat` -- the site's cardinal neighbour toward
        the enemy -- which is the tile the leader wanted anyway (between the
        new tube and their guns), so the vacate is never a wasted turn.
        ⛔ A FAILED STEP FALLS THROUGH, IT DOES NOT END THE TURN: the caller's
        own `step_to(site)` then runs unchanged.  BOTH TAILS COUNTED.
        """
        if not (SK_VOLUME and SK_VH_COLUMN and SK_VH_VACATE):
            return False
        if site is None or p.x != site.x or p.y != site.y:
            return False
        if not self._vh_trailer_beside(ct, site):
            self.vh_vac_alone += 1
            return False
        self.vh_vac_want += 1
        seat = self._guard_seat(site)
        if seat is None or (seat.x == p.x and seat.y == p.y):
            return False
        try:
            if ct.get_move_cooldown() != 0:
                return False
        except Exception:
            return False
        if self.step_to(ct, seat):
            self.vh_vacate += 1
            return True
        return False

    def _escalate_target(self, ct, p, rnd=None):
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
            # ⭐⭐ 4.2 -- THE BAN EXCLUSION, SITE 2.  Scoped to THIS branch, the
            # INFERRED one, for the same reason the audit scopes the defect
            # here: branch 1 above is a live armed enemy, i.e. a building the
            # body cannot stand on, so it is outside the class and outside the
            # ban.  With the remembered tile off the list the keeper's ladder
            # falls through to its next rung instead of re-walking at itself.
            # `rnd is None` = the ban is simply not evaluated (no caller does
            # that today; the default keeps the helper callable from a context
            # with no round).
            if (rnd is not None and self.wg_ban
                    and self._wg_banned(WG_SITE_ESC, k.x, k.y, rnd)):
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
        if seat is None:
            # ⭐ s57 THE STAND, ARM 2 -- the CLEARING STATION, and it is asked
            # SECOND on purpose: a real seat always outranks a station, so this
            # can only ever fire where the v608 positioning half had already
            # given up.  Flag off -> None, and this is one `is None` test.
            seat = self._stand_station(ct, p, rnd)
        if seat is not None:
            if seat.x != p.x or seat.y != p.y:
                self.step_to(ct, seat)
            return
        shooter = self._escalate_target(ct, p, rnd)
        # ⭐ v632 PLANK A, SITE 2 of 3 (SK_WALK_GUARDS) -- THE INFERRED-KILLER
        # FREEZE.  Audit `AUDIT-walk-terminals-2026-08-22.md` row 6b, EXPOSED
        # and UNBOUNDED, inherited from `_v628compose`.  `_escalate_target`
        # branch 1 returns a LIVE VISIBLE armed enemy -- a building, so the BFS
        # lands this body BESIDE it and the state below cannot arise.  Branch 2
        # returns `harv_killer[xy]`, an INFERRED tile from `armed_memo` that is
        # NOT re-verified here; once that remembered turret is gone the tile is
        # empty, standable, and the walk targets the ground under our own feet.
        # The escalation's own lift (`_harv_blocked` -> `_killer_dead`) never
        # runs on this path: this branch RETURNS above the ore loop that calls
        # it, and the only other caller is `_harvester_action`'s own-neighbour
        # scan.  ⇒ `shooter == p` is EXACTLY branch 2 with a vanished
        # structure, which is why no filter needs re-deriving: the state is the
        # walk's own target read against this body's own tile.
        # ⛔ A FAILED ESCAPE FALLS THROUGH TO THE UNCHANGED `step_to`, so a
        # boxed body behaves as it did before this guard existed.
        if (SK_WALK_GUARDS and shooter is not None
                and shooter.x == p.x and shooter.y == p.y):
            self.wg_state_esc += 1
            if self._walk_escape(ct, p, rnd, WG_SITE_ESC):
                self.wg_fire_esc += 1
                return
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
        # ⭐⭐ v632 HEIMDALL PLANK 3, THE MOVEMENT HALF (SK_FORT_RING).  Same
        # rung as PLANK 2's gun walk and immediately above it, for the same
        # reasons stated there: gated on the SAME window and the SAME
        # affordability as the buy, bounded to the apron / the lane list, and
        # it terminates permanently once the three ring turrets stand.  Below
        # the medic seat, the escalated shooter and the seat walks -- a core
        # under fire owns this body and always will.
        if SK_FORT_RING:
            fsite = self._fort_ring_walk(ct, p, rnd)
            if fsite is not None:
                self.step_to(ct, fsite)
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
        # ⭐⭐ s57 THE KILLBOX, ARM 1, THE MOVEMENT HALF -- ONE walk for BOTH
        # pieces, budgeted at SK_KB_WALK_MAX rounds for the whole game.  Same
        # rung as v611's launcher walk and immediately above it: below the
        # medic seat, the escalated shooter and the seat walks, because a core
        # under fire owns this body and always will; above the belt walk
        # because this walk is short, bounded, gated on the same affordability
        # as the buy, and terminates permanently once both pieces stand.
        if SK_KILLBOX:
            kbw = self._kb_walk_target(ct, p, rnd)
            if kbw is not None:
                self.step_to(ct, kbw)
                return
        hl = self._hl_walk_target(ct, p, rnd)
        if hl is not None:
            self.step_to(ct, hl)
            return
        # ⭐⭐ THE ROUTE, ARM 1 (SK_ROUTE_HOME) -- THE MOVEMENT HALF + STALL
        # BREAKER.  ABOVE the v610 gap walk because it is the same preference
        # generalised (a chain FOUR tiles short is as orphaned as one), and
        # BELOW `_medic_seat`, the escalated shooter and the home-gun walk --
        # every rung that answers a core or a body about to die keeps its
        # priority.  ⛔ IT ONLY ENDS THE TURN IF A STEP ACTUALLY HAPPENED:
        # `step_to` returns True iff it moved, so an unreachable target falls
        # through to the walks below instead of silently spending the round.
        if SK_ROUTE_HOME:
            _rt = self._route_walk(ct, p, rnd)
            if _rt is not None:
                self.route_walks += 1
                if self.step_to(ct, _rt):
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
        # ⭐ v632 BUGFIX (SK_ORE_STEPOFF) -- THE SAME DEADLOCK, ORE HALF.  The
        # v601 guard above covers BELT tiles only; the ore walk below never
        # got it, so a keeper standing ON an eligible unbuilt home-ore target
        # walks at itself (CENTRE) forever -- #129's attribution measured it
        # live: icefloe_seatB frozen 475 rounds ON an ore tile with zero
        # actions and every neighbour free; skald_seatA 33 rounds.  Latent in
        # the v628 base (any divergence shape can park a body there); exposed
        # by the dispatch arms.  Same mechanics as the belt guard verbatim.
        if SK_ORE_STEPOFF and self._on_eligible_ore(ct, p, rnd):
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
        # ⭐ v632 PLANK 4 -- THE KEEPER LEASH (#128a), THREAT-CONDITIONAL.
        # Three independent arms (v630.0, v630.1, p1) measured the same F1
        # signature: any home-duty divergence collapses the keeper's core-
        # footprint heals (398->80, ->84, ->266 raw) and our core dies more.
        # The confirmed puller is this economy walk: fenced by is_home_half
        # ONLY (a Voronoi half-plane), no d^2 term, so the keeper legally
        # ranges to the midline while the core is being shot. The leash binds
        # ONLY while the core's own threat latch is fresh (_under_attack --
        # slot 1, the CORE's writer): under threat, economy targets beyond
        # SK_LEASH_DSQ of our core are refused, keeping the body inside heal
        # range of what is being shot; in peace the walk is v628's exactly
        # (a hard fence would starve the belt build-out -- R2's trap).
        _leashed = (SK_KEEPER_LEASH and self.core is not None
                    and self._under_attack(ct, rnd))
        for (x, y) in self.belt_plan:
            if (x, y) in self.belt_escalated or (x, y) in self.belt_built:
                continue
            if x == p.x and y == p.y:
                continue
            q = Position(x, y)
            if _leashed and dsq_core(q, self.core) > SK_LEASH_DSQ:
                continue
            d = p.distance_squared(q)
            if best is None or d < best:
                best = d
                tgt = q
        # ⭐⭐ s57 SK_DOC_ECO_PUSH (d) -- THE REAL HARVESTER CAP, AND IT IS THE
        # ONE THE FIRST CUT OF THIS ARM MISSED.  The block below is entered
        # ONLY `if tgt is None`, i.e. only once EVERY unbuilt planned belt tile
        # has been laid -- so the ore patrol is strictly SECOND, not competing.
        # ⛔ THE LOOP'S OWN HEADER COMMENT SAYS THE OPPOSITE ("ORE AND BELT
        # COMPETE ON DISTANCE, NOT ON PRIORITY", with the measured failure it
        # was written for: two harvesters and 500 Ti against the benchmark's
        # six and 1,420).  The comment describes the intended design; the code
        # is belt-first.  ⇒ On any map whose belt plan is long, the keeper is
        # never free to take a second, third or fourth ore seat -- which is the
        # ledger's lead #1 written as control flow.
        # THE ARM: while this body knows of fewer than SK_DOC_ECO_HARV_TARGET
        # harvester tiles, the ore patrol RUNS ANYWAY and the two candidates
        # compete on the body's own distance, ore winning ties -- the header
        # comment's design, restored under a flag and bounded by the target.
        # ⛔ THE ORPHAN RISK THE v610 NOTE NAMES IS ANSWERED BY TWO RUNGS THAT
        # ALREADY EXIST AND RUN ABOVE THIS BLOCK: `_route_walk` (SK_ROUTE_HOME,
        # ON) targets the missing links of a live harvester's chain and returns
        # before this code is reached, and in the ACTION ladder `_route_action`
        # and the terminating belt both outrank `_harvester_action`.  A seat
        # taken here is routed by those, not left hanging.
        # ⛔ Flag off / target met -> `_ore_first` is False and the branch
        # condition is `tgt is None`, i.e. v632's exactly.
        _belt_tgt = tgt
        _belt_d = best
        _ore_first = bool(tgt is not None and self._doc_eco_on()
                          and len(self.harv_tiles) < SK_DOC_ECO_HARV_TARGET)
        if _ore_first:
            tgt = None
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
            # ⭐⭐ s57 SK_DOC_ECO_PUSH (a) + (b) -- THE ORE PATROL, AND IT IS
            # THE CAP THE LEDGER'S LEAD #1 POINTS AT.  This loop is the ONLY
            # thing in the tree that walks a keeper toward ore, so its fence
            # IS the harvester count and its ranking IS rounds-to-first-
            # delivery.
            # (a) the fence widens to home-half OR near OUR OWN core, and
            #     self-closes at SK_DOC_ECO_HARV_TARGET tiles.
            # (b) the RANK becomes d^2 to OUR CORE with the body's own
            #     distance as tie-break: the belt that has to be laid behind a
            #     harvester is what sets when its first stack lands, and a
            #     seat two tiles further from the keeper but four tiles nearer
            #     the core delivers sooner and for the rest of the game.
            # ⛔ v632 PLANK 4's threat leash is EVALUATED FIRST and unchanged,
            # so under siege neither half can admit a tile the leash refuses.
            # ⛔ Flags off -> `_doc_ore_ok` is `is_home_half` and `_key` is
            # `p.distance_squared(ore)`, i.e. this loop exactly as adopted.
            # ⛔ `best` IS RESET EXPLICITLY.  Reaching here implies `tgt is
            # None` and therefore `best is None` (the belt loop sets both
            # together), so this is a no-op today -- it is written because (b)
            # makes `best` a TUPLE, and a tuple/int comparison is a TypeError
            # escaping `run()`, which the engine answers by permanently
            # destroying the unit.  The invariant is made local rather than
            # inherited.
            best = None
            _near = bool(SK_DOC_ECO_NEAR_FIRST and self._doc_eco_on()
                         and self.core is not None)
            _v632_best = None
            _v632_tgt = None
            for ore in self.ore_list():
                if (ore.x, ore.y) in self.harv_tiles:
                    continue
                # v632 PLANK 4: same threat-conditional leash as the belt loop.
                if _leashed and dsq_core(ore, self.core) > SK_LEASH_DSQ:
                    continue
                if not self._doc_ore_ok(ore, count=True):
                    continue
                if self.belt_plan.get((ore.x, ore.y)) is not None:
                    continue
                if self._harv_blocked(ct, (ore.x, ore.y), rnd):
                    continue        # PLANK 1: do not walk to a banned killzone
                d = p.distance_squared(ore)
                if _v632_best is None or d < _v632_best:
                    _v632_best = d
                    _v632_tgt = ore
                key = (dsq_core(ore, self.core), d) if _near else d
                if best is None or key < best:
                    best = key
                    tgt = ore
            # ⚠ THE (b) DOSE COLUMN, AND IT IS A HONEST DIFF RATHER THAN A
            # FIRING COUNT: `_v632_tgt` is what the adopted ranking would have
            # picked over the SAME admitted set, so this counts rounds on
            # which the near-core rank actually CHANGED the answer.  A
            # `eco_near_repick` of 0 with the flag on means the ranking bought
            # nothing on this map and must be read that way, not argued away.
            if (_near and tgt is not None and _v632_tgt is not None
                    and (tgt.x, tgt.y) != (_v632_tgt.x, _v632_tgt.y)):
                self.eco_near_repick += 1
            # ⭐⭐ (d) THE COMPETITION ITSELF.  Reached only on an `_ore_first`
            # round, i.e. only while the flag is on and the target is unmet.
            # ⛔ FAIL-SAFE FIRST: no admissible ore -> the belt target this
            # block displaced is restored EXACTLY, so an `_ore_first` round
            # with nothing to take is v632's round.
            if _ore_first:
                if tgt is None:
                    tgt = _belt_tgt
                    best = _belt_d
                elif _belt_tgt is not None:
                    # COMPETE ON THE BODY'S OWN DISTANCE (the header comment's
                    # rule), ORE WINNING TIES: a new seat unlocks delivery that
                    # does not exist yet, where a belt tile extends delivery
                    # that already flows.  ⚠ `best` may be a TUPLE here under
                    # (b), so the ore side is re-measured in body distance
                    # rather than compared against a mixed key.
                    if _belt_d is not None and _belt_d < p.distance_squared(tgt):
                        tgt = _belt_tgt
                        best = _belt_d
                    else:
                        self.eco_ore_first += 1
        if tgt is None and not self.ore_list() and self.map_grid is None:
            # v601 BUGFIX, second half: sensing only helps a body that is ever
            # somewhere new.  Measured on stavkirke seed 11: the v600 keeper
            # oscillated between (8,3) and (8,4) beside its own core for the
            # whole match with grid=False, ores=0, harv=0.
            tgt = self.explore_step(ct, p, rnd)
        # ⭐ v632 PLANK B (SK_LEASH_DUTY) -- THE LEASHED KEEPER'S DUTY.
        # THE STATE: the leash above refused every economy target for being
        # beyond SK_LEASH_DSQ of our core, so this walk found NOTHING while the
        # core's own threat latch is fresh.  That is the banked cost of the
        # adopted leash -- jotunheim_seatA, a keeper that spent the game with
        # ZERO economy builds -- and the queue's row 4.1.
        # THE DUTY: hold the medic seat, i.e. the nearest free core-adjacent
        # tile, where `_heal_action`'s EXISTING rung already reaches a damaged
        # core.  Nothing new is bought and no new sensor is added.
        # ⛔ CONJOINED, NOT WELDED: `_leashed` already carries
        # SK_KEEPER_LEASH, so this branch is unreachable with either flag off
        # and the OFF tree is character-for-character the adopted one.
        # ⚠⚠ WHAT THE PRE-BUILD MEASUREMENT SAYS, AND IT IS DISCLOSED RATHER
        # THAN DISCOVERED AT READOUT: the state is real and common
        # (jotunheim_seatA f1: 610 leashed-no-target rounds) but the
        # `tgt = self.core` fall-through immediately below ALREADY reaches the
        # core ring in all 610 of them -- 85 walking in, 521 standing
        # core-adjacent, 4 re-seating, ZERO stuck away from the core -- because
        # `_bfs_direction` has a core-ring goal branch (`sk_common.py:968-978`).
        # ⇒ THIS BRANCH IS EXPECTED TO READ CLOSE TO IDENTITY.  What it adds is
        # the EXPLICIT seat (passable, and no other body of ours already on it)
        # in place of an incidental BFS side effect, the `duty_*` instruments,
        # and the one case the fall-through does not cover: a ring with no free
        # BFS goal.  ⛔ IT DOES NOT FIX THE ECONOMY HALF of that degenerate --
        # the same keeper laid 1 conveyor in 849 rounds and this plank does not
        # give it a build to do; that is a separate row and must not be claimed
        # here.
        if tgt is None and SK_LEASH_DUTY and _leashed:
            self.duty_state += 1
            dseat = self._leash_duty_seat(ct, p)
            if dseat is not None:
                if dseat.x == p.x and dseat.y == p.y:
                    self.duty_holds += 1
                    return          # HOLD STATION on the seat
                if self.step_to(ct, dseat):
                    self.duty_steps += 1
                    return
        if tgt is None:
            tgt = self.core
        if self.step_to(ct, tgt):
            return
        # ⭐ v632 HEIMDALL PLANK 1, R6 -- SK_IDLE_ACT FOR THE HOME KEEPER.  The
        # keeper is the only guaranteed core-adjacent body for the first ~120
        # rounds, so a keeper boxed by the enemy collar with a free action every
        # round is the most expensive instance of the class, not the cheapest.
        # IDENTICAL verb, IDENTICAL guards as the walker's and the engineer's
        # copies (`sk_roles.py:4691`, `:5610`); only the caller is new.
        if (SK_IDLE_ACT_ALL and SK_IDLE_ACT
                and ct.get_action_cooldown() == 0
                and self.free_neighbours(ct, p) == 0):
            if self._peck_priority(ct, p, rnd, skip_core=True):
                return
            self._peck_out(ct, p, rnd)

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
        # ⛔⛔ v632 PLANK 5's R5 GATE (slot 5).  Same reason as `_killer_report`
        # above, and this is the slot the study named FIRST: `_belt_seed_store`
        # READS b24-31 of it every round, so a lost update here does not just
        # drop a diagnostic -- it corrupts the terminus world model the second
        # body was added to share.  Gated at the TOP of the rung rather than at
        # the wstore because everything below it is pure computation for the
        # published word (the only side effect, `_belt_seat_bits` refreshing
        # per-body `belt_term_bits`, is re-seeded from the store each round by
        # `_belt_seed_store` anyway) -- so the gate also returns the whole
        # chain-walk to the CPU budget for a body that cannot use it.
        if self.role != SK_HOME_KEEPER:
            self.eco_pub_blocked += 1
            return
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
        self._doc_fwd_turn_tick()
        if self.enemy is None:
            return
        lap = cage_lap(self.enemy)
        sealed, empty_seals, belt_seats = self._cage_survey(ct, lap)
        self._cage_report(ct, rnd, sealed)
        # v604 FIX 2, run BEFORE any targeting so `self.tgt` still holds last
        # round's objective.  Independent of SK_ONE_CURSOR by design.
        self._cycle_commit(rnd)

        # ⭐⭐ s57 THE KILLBOX, ARM 3, PIECE 1 -- THE BUYER'S RUNG.  ⛔ ABOVE THE
        # WHOLE LAP AND ONLY INSIDE THE OPENING, and BELOW the survey/report/
        # commit bookkeeping above so that no round this rung takes leaves the
        # walker's own cursor state unwritten (v604 FIX 2's reason, verbatim).
        # The launcher site sits at Chebyshev 2-3 of OUR core on the ENEMY side,
        # i.e. on this body's own way out; buying it costs a step or two of a lap
        # that has not started, where for the keeper it is a round trip away from
        # the barriers it should be laying.  Their relay rung 1 lands at r1-r5
        # and 77-80% of their first bodies arrive by throw, so a launcher that
        # waits for the lap has missed the thing it answers.
        # ⛔ THREE FENCES: the role, the SK_KB_FAST_UNTIL hand-back, and the walk
        # budget (this body owes ONE site, so SK_KB_FAST_WALK_PER rounds, and it
        # drops to zero the round the launcher stands).
        # ⛔ Flag off -> False on the first line -> v632 behaviour exactly.
        if self._kb_fast_buyer_turn(ct, p, rnd):
            return

        # ⭐⭐ s57 THE PUSH, PIECE 2 -- THE WARDEN'S RUNG.  ⛔ ABOVE THE WHOLE
        # LAP and BELOW the survey/report/commit bookkeeping above, for v604
        # FIX 2's reason verbatim: no round this rung takes may leave the
        # walker's own cursor state unwritten.  ⛔ IT FAILS OPEN -- no site, no
        # walk budget, no damaged barrel all return False and the cage lap runs
        # exactly as it does today, so a cell the warden cannot reach is a cell
        # whose tape is v632's.  ⛔ Flag off -> False on the first line ->
        # v632 behaviour exactly.
        if self._push_warden_turn(ct, p, rnd):
            return

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
        # ⭐ v632 SK_CHEW_REKEY (#4.3).  The chew clock re-keys on the OCCUPANT
        # as well as the tile -- `_demolish_budget_ok`'s shape -- so a
        # RE-PLANTED building gets a fresh 20 rounds instead of inheriting the
        # dead occupant's expired clock (jotunheim_seatA bid=54, 124 idle
        # rounds).  The give-up itself is UNCHANGED: the same occupant past
        # SK_CAGE_MELEE_GIVEUP is still declined, per entry.
        # ⛔ OFF is the character-for-character v632 chain below, after one
        # test on a module constant and with no engine call added.
        if SK_CHEW_REKEY:
            if not self._chew_ok(q, bid, rnd):
                return False
        elif self.melee_tile != (q.x, q.y):
            self.melee_tile = (q.x, q.y)
            self.melee_since = rnd
        # ⭐ v632 SK_KEEPER_CHEW_ON (#4.3b).  THE ONLY CHANGE IS THE THRESHOLD
        # THIS SITE COMPARES AGAINST -- the branch, its position in the chain
        # and every other gate are the v632 chain verbatim.  `_chew_giveup()`
        # returns SK_CAGE_MELEE_GIVEUP for every body with the flag off and for
        # the CAGE WALKER always; only a HOME KEEPER (whose alternative turn is
        # a stand-still, so the clock's opportunity-cost premise is false) gets
        # the larger one.  Futility is NOT this clock's job and is untouched
        # above and below: the bank floor, the healing race
        # (`_enemy_builder_adjacent`) and `hp_trend_ok` (V7) all still decline.
        elif rnd - self.melee_since > self._chew_giveup():
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

    # ------------------------------------------------------------------
    # v632 SURVIVAL FAMILY -- KEEPER CHEW PERSISTENCE (SK_KEEPER_CHEW_ON, 4.3b)
    # ------------------------------------------------------------------

    def _chew_giveup(self):
        """The give-up threshold `_clear_tile`'s decline site compares against.

        GAME CONTEXT: in-engine bookkeeping for our own builder bot in the
        Florent Code League, a sandboxed bot-vs-bot programming competition.

        SK_CAGE_MELEE_GIVEUP (20) for every body, EXCEPT a HOME KEEPER while
        SK_KEEPER_CHEW_ON is set, which gets SK_KEEPER_CHEW_GIVEUP.  The full
        argument is at the flag (`sk_maps.py`); in one line: the clock prices
        OPPORTUNITY COST, the walker has a lap to get back to and the keeper at
        a held post does not.  ⛔ The keeper predicate IS the held-post read at
        this call site -- act and move are mutually exclusive in the engine, so
        a keeper that reaches the peck is standing still by construction.
        Pure: one module-constant test with the flag off, no engine call ever.
        """
        if SK_KEEPER_CHEW_ON and self.role == SK_HOME_KEEPER:
            return SK_KEEPER_CHEW_GIVEUP
        return SK_CAGE_MELEE_GIVEUP

    # ------------------------------------------------------------------
    # v632 SURVIVAL FAMILY -- THE CHEW-CLOCK RE-KEY  (SK_CHEW_REKEY, #4.3)
    # ------------------------------------------------------------------

    def _chew_ok(self, q, bid, rnd):
        """The per-(TILE, OCCUPANT) chew clock -- `_demolish_budget_ok`'s form.

        GAME CONTEXT: in-engine bookkeeping for our own builder bot in the
        Florent Code League, a sandboxed bot-vs-bot competition; `bid` is an
        opposing bot's in-engine structure standing on tile `q`.

        Returns True iff this body may keep chewing `bid` on `q` this round.
        Reachable ONLY under SK_CHEW_REKEY, which is what keeps `chew_clock`
        empty and the three counters at 0 on every OFF arm.

        `chew_clock[(x, y)] = (occupant bid, episode start round, last touch)`.
          * no entry, or a DIFFERENT occupant  -> a NEW episode arms here.
          * same occupant, within the give-up  -> allowed, touch refreshed.
          * same occupant past SK_CAGE_MELEE_GIVEUP -> declined, and the entry
            is left exactly as it is so the decline is PERMANENT for that
            occupant.  ⛔ THAT IS THE UNCHANGED HALF: a hard tile still cannot
            own a walker, and there is no keeper exemption in this flag.
        Pure state: no engine call, so an ON arm's added cost is one dict
        lookup on a path that is about to spend an engine `fire`.
        """
        xy = (q.x, q.y)
        prev = self.chew_clock.get(xy)
        if prev is None or prev[0] != bid:
            if len(self.chew_clock) >= SK_CHEW_CLOCK_MAX:
                self._chew_prune(rnd)
            self.chew_clock[xy] = (bid, rnd, rnd)
            self.chew_rearms += 1
            return True
        if rnd - prev[1] > SK_CAGE_MELEE_GIVEUP:
            self.chew_declines += 1
            return False
        self.chew_clock[xy] = (bid, prev[1], rnd)
        return True

    def _chew_prune(self, rnd):
        """Bound the chew ledger.  Called ONLY from `_chew_ok`, and only on a
        write that would take it past SK_CHEW_CLOCK_MAX.

        Two passes, cheapest first: drop every entry not TOUCHED for more than
        SK_CAGE_MELEE_GIVEUP rounds (an episode this body has walked away
        from), then, if that did not clear room, the oldest-touched entries
        down to the cap.  ⛔ A drop can only ever RE-ARM a tile, never extend a
        decline, so the bound's worst case is strictly more permissive than the
        OFF path -- which re-arms on any intervening tile already.
        """
        cc = self.chew_clock
        for xy in [k for k in cc if rnd - cc[k][2] > SK_CAGE_MELEE_GIVEUP]:
            del cc[xy]
            self.chew_pruned += 1
        if len(cc) >= SK_CHEW_CLOCK_MAX:
            order = sorted(cc, key=lambda k: cc[k][2])
            for xy in order[:len(cc) - SK_CHEW_CLOCK_MAX + 1]:
                del cc[xy]
                self.chew_pruned += 1

    def _attack_enemy_core(self, ct, p, rnd):
        """Strangle-then-KILL: the cage is a means, the core is the end."""
        if self.enemy is None:
            return
        # ⭐⭐ v632 PLANKS 8+9 -- NO PECKING POST-FLIP.  Magnus, on the s57
        # rotation demo: "no pecking, we only watch our sentinels work"
        # (coordination tail 2026-08-22 ~19:2x-19:4xZ).  The arithmetic agrees
        # and this tree already measured it: a builder peck is 2 damage a round
        # into a core absorbing a heal-tax of 0.68 (95 enemy heals against 82 of
        # our pecks over 41 rounds, v602 autopsy) -- 100% of the 14,130 damage
        # we have ever dealt an enemy core was SENTINEL fire and the walker's
        # pecks contributed ZERO (v603 FIX 1).  A raider standing at the
        # footprint is a raider not planting, and §8b's binding constraint is
        # PLANT RATE.
        # ⛔ THE TRAVEL HALF SURVIVES, CAPPED AT THE BAND EDGE.  This method is
        # the engineer's only fallback when its band half is exhausted, and a
        # body that neither plants nor moves is worse than one that repositions.
        # But walking all the way IN would park the raider at d^2 ~2, inside
        # every enemy gunner's r^2 = 13 -- the point-blank zone
        # SK_NEST_POINT_BLANK exists to refuse -- so the approach stops at
        # SK_NEST_DSQ_MAX, the outer edge of the siting band, which is where the
        # next `_pick_nest` wants to be measured from anyway.
        if self.rot_body:
            self.rot_pecks_skipped += 1
            if dsq_core(p, self.enemy) > SK_NEST_DSQ_MAX:
                self.step_to(ct, self.enemy)
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
                # ⭐ v623 HEALWELD: the guard was conjoined with SK_CAGE_CEIL
                # (permanently False since FIX 5 shipped OFF), so the shipped
                # core peck ran with NO heal-race check -- the third instance
                # of the s55 weld class.  SK_CORE_PECK_HEALGUARD's own comment
                # (sk_maps.py) says it is a separate flag precisely so it can
                # be priced on its own; now it can be.
                if (SK_CORE_PECK_HEALGUARD
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
            # ⭐ v632 HEIMDALL PLANK 2 -- THE DEMOLITION SWEEP, AND THE DENIER
            # IS THE PRIMARY DEMOLISHER.  Study §1b re-homes this role as the
            # PERIMETER BODY: it already reads the home answer (`_home_defence`,
            # `_denier_home_answer` are gated on this role), it already carries
            # the chew verbs, and it is the body that stands where our
            # harvesters are, which is where their planted structures land.
            # ABOVE `_melee_harvester` because inside SK_DEMOLISH_DSQ the CLASS
            # ordering has to win: `_melee_harvester` is an orthogonal-4 local
            # scan with no class scale, so leaving it first would let an
            # adjacent conveyor outrank a planted launcher three tiles away --
            # and the prediction study says the planted armed structure is what
            # carries the core damage (64/64 first-damage events).  BELOW
            # `_peck_priority`, which answers an enemy TURRET already adjacent
            # to this body: that is the same target class one rung earlier and
            # with a cheaper test.
            if SK_DEMOLISH and self._demolish_action(ct, p, rnd):
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
        # ITERATION 12b: the HOLD case — the goal helper returned the body's
        # own tile because it already stands beside its quarry.  Holding is
        # the intent (the verbs act from adjacency), not the WG freeze class.
        if (SK_DENY_WALK_FIX and tgt is not None
                and tgt.x == p.x and tgt.y == p.y
                and getattr(self, "_deny_hold", False)):
            return
        # ⭐ v632 PLANK A, SITE 1 of 3 (SK_WALK_GUARDS) -- THE DENIER'S
        # STAND-ON-YOUR-OWN-TARGET FREEZE.  Audit `AUDIT-walk-terminals-
        # 2026-08-22.md` row 24, EXPOSED and UNBOUNDED, inherited from
        # `_v628compose`.  Two of `_deny_target`'s three branches return a
        # STANDABLE tile: the PATROL branch always (an enemy-half ORE tile),
        # and the remembered-`enemy_harv` branch the moment that harvester is
        # gone.  The act (`_deny_barrier`) scans `p.add(d)` -- ORTHOGONAL
        # NEIGHBOURS ONLY -- so the tile underfoot is never a legal barrier
        # site; `enemy_harv` is popped and `denied_tiles` grown ONLY on a
        # successful build (`_deny_barrier`), never for the tile the body is
        # standing on.  ⇒ the body's own tile stays the nearest target at
        # d^2 = 0 forever, `_bfs_direction` answers CENTRE, and nothing
        # re-plans.  The rung below it is the WRONG gate for this defect: its
        # test is `free_neighbours == 0`, and this freeze's whole signature is
        # FREE neighbours.
        # ELIGIBILITY IS MIRRORED FROM THE WALK'S OWN FILTERS BY CONSTRUCTION:
        # the state is `_deny_target`'s own return value equal to this body's
        # tile, so no filter is re-derived and none can drift out of step.
        # ⛔ A FAILED ESCAPE FALLS THROUGH, IT DOES NOT END THE TURN: a body
        # with no passable neighbour is genuinely boxed, and that is the
        # `SK_IDLE_ACT_ALL` rung's case, not this one.  Only a step that
        # ACTUALLY EXECUTED returns.
        if (SK_WALK_GUARDS and tgt is not None
                and tgt.x == p.x and tgt.y == p.y):
            self.wg_state_deny += 1
            if self._walk_escape(ct, p, rnd, WG_SITE_DENY):
                self.wg_fire_deny += 1
                return
        if self.step_to(ct, tgt if tgt is not None else self.enemy):
            return
        # ITERATION 12b: a target whose step FAILED with the move ready is a
        # proved-dead walk this round — park-ban its SOURCE for 30 rounds so
        # the next turn re-targets instead of freezing on it (the probe
        # measured one poisoned target holding the walk r40->r297).
        if (SK_DENY_WALK_FIX and tgt is not None
                and ct.get_move_cooldown() == 0):
            bans = getattr(self, "deny_park_ban", None)
            if bans is None:
                bans = self.deny_park_ban = {}
            key = getattr(self, "_deny_src", None)
            bans[(tgt.x, tgt.y)] = rnd + 30
            if key is not None:
                bans[key] = rnd + 30
        # ⭐ v632 HEIMDALL PLANK 1, R6 -- SK_IDLE_ACT FOR THE ORE DENIER.  The
        # v603 clause ("a body with no legal move must act") is wired into the
        # cage walker twice and the engineer once, and into neither home role.
        # Under the citadel the denier is a body that stands next to things by
        # design, so a boxed denier with a free action is exactly the
        # terminal-idle class study §7 R6 names.  IDENTICAL verb, IDENTICAL
        # guards (`sk_roles.py:5610`); only the caller is new.
        if (SK_IDLE_ACT_ALL and SK_IDLE_ACT
                and ct.get_action_cooldown() == 0
                and self.free_neighbours(ct, p) == 0):
            if self._peck_priority(ct, p, rnd, skip_core=True):
                return
            self._peck_out(ct, p, rnd)

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

    def _deny_goal(self, ct, p, q, rnd):
        """ITERATION 12b (SK_DENY_WALK_FIX) — walk goal for a HARVESTER tile.

        The quarry is a LIVE building, so its own tile is a BLOCKED BFS goal
        and `_bfs_direction` answers CENTRE on it (the probe-measured park).
        Return the nearest FREE cardinal neighbour instead — arrival puts the
        body adjacent, which is where `_deny_barrier` and `_melee_harvester`
        live.  Returns the body's OWN tile when it already stands adjacent
        (the HOLD case, exempted from the WG own-tile escape by the caller),
        and None when no neighbour is known-free (caller skips the quarry).
        """
        if not SK_DENY_WALK_FIX:
            return q
        if p.distance_squared(q) == 1:
            self._deny_hold = True
            return p
        best = None; goal = None
        for d in CARDINALS:
            n = q.add(d)
            if not self.ibp(n):
                continue
            try:
                if ct.get_tile_env(n) == Environment.WALL:
                    continue
                if ct.get_tile_building_id(n) is not None:
                    continue
            except Exception:
                pass                     # out of vision: unknown reads free
            dd = p.distance_squared(n)
            if best is None or dd < best:
                best = dd; goal = n
        return goal

    def _deny_target(self, ct, p, rnd):
        # ⭐⭐ 4.2 -- THE BAN EXCLUSION, SITE 1.  A tile this body escaped from
        # is off THIS walk's target list for SK_WALK_GUARD_BAN rounds, so the
        # walk RE-TARGETS (the next-nearest enemy-half ore) instead of stepping
        # straight back on.  ⛔ APPLIED TO THE TWO STANDABLE BRANCHES ONLY --
        # the remembered `enemy_harv` tile and the PATROL ore.  The live
        # visible-harvester branch is NOT-APPLICABLE by the audit's own test (a
        # harvester is a building, so the BFS lands the body beside it and this
        # body can never have been standing on it); excluding it would refuse a
        # real quarry for a freeze that cannot occur there.
        _ban = bool(self.wg_ban)
        self._deny_hold = False
        _park = getattr(self, "deny_park_ban", None) if SK_DENY_WALK_FIX else None
        best = None
        tgt = None
        src_q = None
        for xy, seen in self.enemy_harv.items():
            q = Position(xy[0], xy[1])
            if not self.ibp(q):
                continue
            if _ban and self._wg_banned(WG_SITE_DENY, xy[0], xy[1], rnd):
                continue
            if _park and _park.get(xy, -1) > rnd:
                continue                 # 12b: park-banned, re-target
            d = p.distance_squared(q)
            if best is None or d < best:
                best = d
                tgt = q
        if tgt is not None:
            goal = self._deny_goal(ct, p, tgt, rnd)
            if goal is not None:
                self._deny_src = (tgt.x, tgt.y)
                return goal
            best = None; tgt = None      # 12b: no free neighbour, fall through
        for eid, et, ep in self.vis_enemy:
            if et != EntityType.HARVESTER:
                continue
            if _park and _park.get((ep.x, ep.y), -1) > rnd:
                continue                 # 12b
            d = p.distance_squared(ep)
            if best is None or d < best:
                best = d
                tgt = ep
        if tgt is not None:
            goal = self._deny_goal(ct, p, tgt, rnd)
            if goal is not None:
                self._deny_src = (tgt.x, tgt.y)
                return goal
            best = None; tgt = None      # 12b
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
            if _ban and self._wg_banned(WG_SITE_DENY, ore.x, ore.y, rnd):
                continue                # 4.2: re-target, do not step back on
            if _park and _park.get((ore.x, ore.y), -1) > rnd:
                continue                 # 12b
            d = p.distance_squared(ore)
            if best is None or d < best:
                best = d
                tgt = ore
        if tgt is not None:
            self._deny_src = (tgt.x, tgt.y)
        return tgt

    # ==================================================================
    # ROLE 3 -- SIEGE ENGINEER  (COPY 5 + V3 + V4 + V9)
    # ==================================================================

    def _chest_refuse(self, ct, rnd, cost):
        """⭐⭐ v632 PLANKS 8+9 AMENDMENT -- THE WAR CHEST (SK_ROTATE_CHEST_FROM).

        True when a DISCRETIONARY keeper purchase must stand down because the
        bank would not still cover two sentinels after paying for it.

        WHY IT EXISTS.  The prestage build's smoke falsified study §8c's funding
        assumption on 2 of 3 cells: bank vs sentinel cost AT THE FLIP read
        40 vs 88 (longhouse) and 38 vs 72 (jotunheim) against 1,118 vs 81
        (valkyrie).  Where that happens, the raiders arrive on time and then
        STAND THERE -- the first plant slipped to r361 and r413 with the bank at
        3 and 22 Ti.  Travel is what SK_ROTATE_PRESTAGE buys; this buys the
        other half, and neither is a substitute for the other.

        ⛔ THE TWO EXEMPTIONS ARE THE SPECIFICATION, NOT SOFTENING:
          * **p0 ECONOMY IS NEVER REFUSED.**  Harvesters and belt-plan
            conveyors do not pass through this predicate at all -- see the call
            sites; the exemption is STRUCTURAL, not a clause that could be
            edited out.  This tree's own founding fact is that a harvester with
            no route home is worth zero forever.
          * **DEFENCE FIRST.**  `_under_attack` is the slot-1 threat latch
            (SK_SLOT_UNDER, 50-round freshness) -- the SAME latch ledger V5
            arbitrates survival on.  A fortress that banks 200 Ti and loses its
            core at r280 has banked nothing, so the chest yields on exactly the
            signal the rest of the tree already yields on.

        ⛔ OFF-IDENTITY IS THE FIRST LINE.  With SK_ROTATE False the window
        predicate is False for every round of the game, this returns False
        before touching the controller, and no purchase anywhere in the tree
        changes.  `chest_blocked == 0` is the witness.
        ⛔ AND IT FAILS OPEN.  Any exception reading the bank or a cost getter
        returns False -- a refusal built on an unreadable number is a purchase
        cancelled for no measured reason, which is worse than the overspend.
        """
        if not (SK_ROTATE and SK_ROTATE_CHEST_FROM <= rnd < SK_PHASE_ROUND):
            return False
        try:
            if self._under_attack(ct, rnd):
                return False
            if ct.get_global_resources() >= 2 * ct.get_sentinel_cost() + cost:
                return False
        except Exception:
            return False
        self.chest_blocked += 1
        return True

    def _rot_prestage(self, ct, p, rnd):
        """⭐⭐ v632 PLANKS 8+9 REDESIGN -- THE COMMUTE (SK_ROTATE_PRESTAGE).

        GAME CONTEXT: in-engine movement for the Florent Code League, a
        sandboxed bot-vs-bot competition on a simulated grid.  This method
        issues `move` calls and nothing else -- no build, no fire, no spend.

        WHAT IT IS.  Attempt 1's screen passed every guard and lost on ARRIVAL:
        the first post-flip sentinel landed at a median r336/r344/r449 by
        fixture and 16 of 39 touchable cells never fielded one.  The cause is
        that travel, siting and funding were all paid IN SERIES from a standing
        start at r300.  This pays the travel EARLY and in parallel with the
        fortress's last ten eco rounds, so the flip finds both raiders standing
        in their band halves with a site already chosen and `_siege_engineer`'s
        existing adjacency test true on the first round it runs.

        ⛔⛔ IT BUILDS NOTHING AND PECKS NOTHING.  PROGRAMME.md
        `HEIMDALL_TACTIC_LOCK: eco_and_defence_to_r300_then_rotate_and_destroy`
        -- eco and defence UNTIL 300.  There is exactly one mutating engine call
        reachable from this method and it is `move`, through `step_to` ->
        `_nav`.  No `build_*`, no `fire`, no `convert_ammo`, no titanium leaves
        the bank before SK_PHASE_ROUND.  The doctrine gives up ten rounds of two
        bodies' PHASE-1 LABOUR, not one titanium of phase-1 SPENDING.

        ⛔ THE RE-HOME LATCH IS A CORRECTNESS REQUIREMENT, NOT TIDINESS.  The
        ORIGINAL engineer (role 3) has been running `_siege_engineer` all game
        against the FULL band; whatever `nest_site` it holds at r290 was chosen
        without the role-parity half split and is very likely in the OTHER
        raider's half.  Walking to it would deliver both bodies to the same arc
        and re-open hazard (b) at exactly the round the split exists for.  The
        site is therefore dropped ONCE, on the first prestage round, so the
        re-pick runs under the split.
        """
        if self.enemy is None:
            return
        if not self.rot_staged:
            self.rot_staged = True
            self.nest_site = None
            self.nest_face = None
            self.nest_prepped = 0
            self.nest_best_d = None
        # The refutation half, exactly as `_siege_engineer` runs it: a target
        # that vision proves is a WALL, or that this body has failed to close on
        # for SK_NEST_STUCK_ROUNDS, is abandoned and re-picked.  Without it a
        # ten-round commute can be spent walking at a tile that does not exist.
        self._nest_site_watch(ct, p, rnd)
        if self.nest_site is None:
            self.nest_site = self._pick_nest(ct, p, rnd)
            if self.nest_site is not None:
                self.nest_best_d = None
                self.nest_since = rnd
                self.nest_anchor = None
                self.nest_anchor_rnd = rnd
        self.rot_stage_walks += 1
        if self.nest_site is not None:
            # ⛔⛔ THE COMMUTE STOPS **BESIDE** THE SITE, NOT ON IT, AND THE
            # 22-ROUND COMMUTE IS WHAT MADE THIS BITE.  `_plant_gun` builds on
            # an ORTHOGONALLY ADJACENT tile -- `_siege_engineer`'s own gate is
            # `abs(site.x - p.x) + abs(site.y - p.y) == 1` -- so a body standing
            # ON its chosen tile cannot build there and must step off and back.
            # Measured on valkyrie at 290 (a ten-round commute that never
            # arrived) this was invisible; at 278 the body reached (21,10) at
            # r299, stepped onto its own site (22,10) at r300 and pushed the
            # first plant from r321 to r338 -- the redesign's whole gain, spent
            # on one tile.  Holding station at Manhattan 1 is what makes "at
            # r300 they are IN the band and the existing plant logic fires
            # immediately" literally true.
            if (abs(self.nest_site.x - p.x)
                    + abs(self.nest_site.y - p.y)) == 1:
                return
            self.step_to(ct, self.nest_site)
            return
        # No site yet -- the board is unconfirmed, or this body's half is
        # momentarily empty.  Close on the enemy anchor so the NEXT `_pick_nest`
        # runs from inside the band, capped at the band edge for the same reason
        # `_attack_enemy_core`'s rotation arm is capped: walking further in
        # parks the body at d^2 ~2, inside every enemy gunner's r^2 = 13.
        if dsq_core(p, self.enemy) > SK_NEST_DSQ_MAX:
            self.step_to(ct, self.enemy)

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
        self._doc_fwd_turn_tick()
        # ⭐ s57 ARM 2 (c): the purse sample, taken ONCE per engineer round and
        # ABOVE every early return, because a rate is only a rate if the
        # sampling is regular -- `_b2_sample` itself refuses any gap other than
        # exactly one round rather than averaging over a hole it cannot see.
        # No-op on every SK_BATTERY2-off arm (one module-constant test).
        self._b2_sample(ct, rnd)
        # ⭐⭐ s57 SK_HAMMER_PRIO V2 -- THE UNCONDITIONAL READINESS EVALUATION,
        # and its position is the amendment.  It sits ABOVE the `enemy is None`
        # return, i.e. on EVERY engineer round, immediately after the sample
        # that feeds it and ABOVE `_drip_report` (so a latch that fires this
        # round is on the wire this round rather than next).  v1's single call
        # site inside `_battery_open` stays where it is -- the latch-once
        # semantics make the second evaluation idempotent.  No-op on every
        # SK_HAMMER_PRIO-off arm (one module-constant test).
        self._hammer_eco_eval(ct, rnd)
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
        # ⭐⭐ v632 PLANKS 8+9 -- THE BATTERY.  "as many sentinels as necessary
        # to bring the enemy core down" (Magnus, PROGRAMME.md 48b874bea), and
        # study §8b puts the number at 4-6 CONCURRENT: two tubes is 130 rounds
        # against a core healing at the measured 0.68 tax, i.e. a stalemate;
        # four is 65 rounds, six is 44.  See SK_ROTATE_WANT's note for the
        # disclosed per-body/team distinction.
        if self.rot_body:
            want = SK_ROTATE_WANT
        live = self._floor_live(ct, rnd)
        # ⭐⭐ s57 ARM 2 (a): the cross-body half of the ledger fix.  A no-op on
        # every master-off arm and on every round the team census does not
        # exceed this body's own book.
        live = self._b2_live(ct, rnd, live)
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
        # ⭐⭐ s57 THE BATTERY, ARM 1 -- THE LIVE CEILING (SK_BATTERY_WANT), AND
        # THIS IS THE WHOLE ARM.  Study STUDY-battery-execution-2026-08-23: 62
        # of 90 cells stop at exactly the line below, and in WIN-class cells the
        # peak ACHIEVABLE against the cell's own purse and this bot's own
        # surcharge bar is 4.0 against an achieved 2.0.
        # ⛔ `want` IS NOT RAISED, AND THAT IS THE DESIGN.  Raising it here
        # would also move `skip_prep` (`0 < live < want`), `_plant_gun`'s
        # SK_TUBE_FUND waiver (`live < want`) and the post-plant re-arm
        # (`n < want`) -- three policies this arm has no mandate to change and
        # which would make a result unattributable.  Only the HOLD is skipped,
        # and only while `_battery_open` says the purse has already cleared the
        # bar the very next `_plant_gun` will charge.  So:
        #   * plants 1 and 2 run under today's conditions, character for
        #     character (this branch is not even consulted below the floor);
        #   * a cell whose purse never clears the bar never leaves the hold and
        #     its tape is byte-identical;
        #   * a plant beyond the pair pays the FULL surcharge, because with
        #     `want` still 2 and `live >= 2` the waiver's `live < want` is
        #     False and `_plant_gun` takes its else branch -- the same
        #     expression `_battery_bar` restates.
        # ⭐⭐ s57 ARM 2 JOINS AT THE SAME ONE GATE.  `want` is still NOT
        # raised (the three policies above stay arm-1's), the ceiling and the
        # eco latch live inside `_battery_open`, and the master is tested here
        # so an OFF arm reaches nothing.
        batt = False
        if SK_BATTERY_WANT or SK_BATTERY2:
            batt = self._battery_open(ct, rnd, live, want)
            if batt:
                self._battery_rearm()
        if live >= want and not batt:
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
            # ⭐⭐ s57 THE PUSH, PIECE 3 -- OVERLAPPING SUCCESSION.  ⛔ THE
            # FIRST RUNG OF THE HOLD BRANCH AND NOWHERE ELSE: this is exactly
            # the set of rounds in which the engineer has nothing to plant, and
            # spending them on the NEXT site is the whole content of the piece.
            # ⛔ BELOW nothing and ABOVE `_guard_heal` because that rung is a
            # rotation body's babysit (False on every SK_ROTATE-off round), and
            # on a rotation arm the babysit should keep winning -- the gate is
            # written so it can.  ⛔ Flag off -> False on the first line ->
            # v632 behaviour exactly.
            if self._push_succ(ct, p, rnd, live, want):
                return
            # ⭐⭐ s57 BARRELS ARM 2, PIECE (b) -- OVERLAPPING SUCCESSION.
            # ⛔ IMMEDIATELY BELOW THE PUSH'S OWN SUCCESSION RUNG so that arm,
            # if it is ever ON, keeps its behaviour character for character and
            # this one is reached exactly when that one declines.  SK_PUSH
            # ships False, so on every arm of this wave the rung above returns
            # on its first line and this is the first rung of the hold branch --
            # which is the set of rounds in which the engineer has nothing to
            # plant, and spending them on the NEXT site is the whole piece.
            # ⛔ ABOVE `_guard_heal` for that rung's own stated reason (a
            # rotation body's babysit should keep winning on a rotation arm; the
            # gate is written so it can) and flag off -> False on the first line.
            if self._bg_succ(ct, p, rnd, live, want):
                return
            # ⭐⭐ v632 PLANK 10 (SK_ROTATE_GUARD) RUNG (b) -- THE HEAL, AHEAD
            # OF THE STAGE GATE.  A rotation body standing at the battery's
            # target has nothing to plant; the turn it would spend holding buys
            # +4 HP on the most-damaged tube instead.  STAGE remains below as
            # the fallback for the undamaged case, so the babysit-vs-STAGE
            # staffing tension resolves by PRIORITY, not deletion (v630's
            # ordering, kept).  ⛔ `_guard_heal` returns False on every
            # SK_ROTATE-off round, every round below SK_PHASE_ROUND, every
            # non-raider body and every SK_ROTATE_GUARD-off arm, so this line
            # is a no-op there and the control flow below is unchanged.
            if self._guard_heal(ct, p, rnd):
                return
            # ⭐ v627/v628: the latency half is admitted by its own master too.
            if ((SK_TUBE_FLOOR2 or SK_TUBE_LATENCY_SOLO)
                    and (SK_TUBE_FLOOR2_PREPREP or SK_TUBE_FLOOR2_STAGE)
                    and self._preprep(ct, p, rnd)):
                return
            # ⭐⭐ s57 BARRELS ARM 3 (SK_BG_ENGHEAL) -- CALL SITE 2, THE SAME
            # RUNG WHERE THE HOLD BRANCH LANDS WHEN THE SUCCESSION DECLINES
            # (no successor site, or the walk to it failed).  ⛔ BELOW
            # `_guard_heal` and below `_preprep` ON PURPOSE: the first is a
            # rotation body's babysit whose precedence v630/v632 already
            # settled, and the second SPENDS on prep, which is a real task and
            # outranks an idle round by definition.  The only rung below this
            # one is the discretionary hold-station park, so this is the idle
            # terminal on this path.  ⚠ DISCLOSED: when the body is not yet AT
            # its park tile, the park is a walk and this rung outranks it -- a
            # damaged tube already orthogonally adjacent is worth more than one
            # more step toward a tile chosen only because there was nothing
            # else to do.  ⛔ Flag off -> False on the first line.
            if self._bg_engheal(ct, p, rnd, cs=2):
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
            # ⭐⭐ v632 PLANK 10 RUNG (c) -- THE BABYSIT, BY A BODY WHOSE ONLY
            # JOB IT IS.  v619's hold parks "beside the newest tube" on
            # whichever side the walk happened to arrive from -- in the common
            # case the HOME side, i.e. behind the tube, where it screens
            # nothing and cannot reach the enemy-side damage.  The guard holds
            # the FRONT SEAT instead: between the tube and the enemy core,
            # where rung (b) reaches it and where the 40 HP body itself soaks
            # the gunner ray.  ⛔ AND THIS IS THE RUNG v630 COULD NOT AFFORD:
            # there the babysitter was the ONE siege engineer and the home
            # economy paid for its absence.  Post-flip these bodies are
            # dedicated raiders with no eco job to drift away from, so the
            # cost mechanism that refuted v630 has no carrier here.
            if self._guard_walk(ct, p, hold):
                return
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
            # ⭐⭐ s57 BARRELS ARM 3 (SK_BG_ENGHEAL) -- CALL SITE 3, AND IT IS
            # THE ONE THE OPPORTUNITY CENSUS FOUND.  Reaching here means
            # `_pick_nest` returned nothing: no site, therefore no plant, no
            # prep and no successor walk -- the buy path's own idle terminal.
            # The census (`bg2build_opp.py`, 12 population-bearing cells, 5,165
            # engineer rounds) puts 21 of the 31 damaged-ADJACENT engineer
            # rounds exactly here, against 0 of 31 at call sites 1 and 2, and
            # 29 of the 31 spent no action at all.  ⛔ ADJACENT HEAL ONLY
            # (`allow_step=False`): a walk here would fight the fallback's own
            # nav, and "no walk" is the whole reason staffing form 4 exists.
            # ⚠ A delivered heal preempts `_attack_enemy_core` for this round --
            # one builder peck (2 damage) traded for +4 HP on a sentinel that
            # deals 18 a shot at the same core.  ⛔ Flag off -> False on the
            # rung's first line -> t_bg_* behaviour character for character.
            if self._bg_engheal(ct, p, rnd, cs=3, allow_step=False):
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
                # ⭐ v626 PLANK A (SK_NEST_CLEAR): _nest_scan never tests
                # occupancy, so a band tile carrying a building is an invisible
                # dead end -- 25-60 orbit rounds, then a PERMANENT ban.  Clear
                # it instead: own building -> free destroy (no cooldown, plant
                # may still run this turn); enemy building -> chew under
                # _clear_tile's guard doctrine, give-up 12 rounds, and a
                # RE-LAID tile is banned on its SECOND clear, not chewed again
                # (sk_maps.py:172-181 measured that race lost).
                if SK_NEST_CLEAR:
                    _cbid = None
                    try:
                        _cbid = ct.get_tile_building_id(site)
                    except Exception:
                        _cbid = None
                    _ckey = (site.x, site.y)
                    if _cbid is None:
                        if self.nest_clear_tile == _ckey:
                            # the chew finished: remember the tile so a re-lay
                            # bans on sight (falsifier-4 guard)
                            self.nest_cleared_once.add(_ckey)
                            self.nest_clear_tile = None
                    else:
                        _cown = False
                        try:
                            _cown = ct.get_team(_cbid) == self.team
                        except Exception:
                            _cown = False
                        if _cown:
                            if SK_NEST_CLEAR_OWN:
                                try:
                                    if ct.can_destroy(site):
                                        ct.destroy(site)
                                        self.nest_clears_own += 1
                                except Exception:
                                    pass
                            # destroy is free -- prep/plant may run this turn
                        else:
                            if _ckey in self.nest_cleared_once:
                                self._nest_clear_ban(site)
                                return
                            if self.nest_clear_tile != _ckey:
                                self.nest_clear_tile = _ckey
                                self.nest_clear_since = rnd
                            elif (rnd - self.nest_clear_since
                                    > SK_NEST_CLEAR_GIVEUP):
                                self._nest_clear_ban(site)
                                return
                            if self._enemy_builder_adjacent(ct, site):
                                self._nest_clear_ban(site)
                                return
                            if not self.hp_trend_ok(ct, _cbid, rnd):
                                self._nest_clear_ban(site)
                                return
                            try:
                                if ct.can_fire(site):
                                    ct.fire(site)
                                    self.nest_clears += 1
                                    return
                            except Exception:
                                pass
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
                # ⭐⭐ v632 PLANKS 8+9 -- NO PREP BARRIERS IN THE SIEGE, AND IT
                # IS A MEASUREMENT.  The s57 rotation demo measured checkmate
                # r374 -> r336 with the preps dropped (coordination tail
                # 2026-08-22 ~19:2x-19:4xZ).  Two builder turns per site in
                # front of a tube whose measured life is 8-10 rounds buys
                # latency the battery cannot spend; §8b's binding constraint is
                # PLANT RATE, and a prep is a plant not made.
                # ⛔ IT IS APPLIED BELOW THE v613 COUNTER ON PURPOSE, so
                # `tube_noprep` stays SK_TUBE_NOPREP's instrument and does not
                # silently absorb this plank's refusals.
                # ⛔ AND IT DOES NOT TOUCH THE PRE-FLIP CONSTANT:
                # SK_NEST_PREP_BARRIERS is unchanged and still governs every
                # round below SK_PHASE_ROUND and every SK_ROTATE-off arm.
                if self.rot_body and self.nest_prepped >= SK_ROTATE_PREPS:
                    if not skip_prep and self.nest_prepped < SK_NEST_PREP_BARRIERS:
                        self.rot_preps_skipped += 1   # the refusal tap
                    skip_prep = True
                if not skip_prep and self.nest_prepped < SK_NEST_PREP_BARRIERS:
                    if self._prep_barrier(ct, p, site, rnd):
                        return
                # ⭐⭐ s57 ARM 2 (b) -- THE BURST RULE, AND ITS PLACE IN THE
                # LADDER IS PART OF THE DESIGN.  BELOW the prep rung, so a
                # funding hold is still a productive turn (the prep barriers
                # this site needs anyway get laid while the purse fills, and
                # `_prep_barrier` returns before this line when it acts).
                # ABOVE `_plant_gun`, because the whole content of the rule is
                # NOT taking that plant yet.
                # ⛔ IT HOLDS STATION RATHER THAN FALLING THROUGH.  The
                # fall-through below is `step_to(site)` from Manhattan 1, i.e.
                # the body would walk ONTO its own site and then have to step
                # off to build -- sk_roles.py's own terminal-approach note
                # measures that at a plant pushed r321 -> r338.  A funded wait
                # that spends its turns walking on and off the tile is not a
                # wait, it is a stall, so the hold consumes the turn.
                if self._b2_burst_hold(ct, rnd, live, want):
                    self._b2_hold_clocks(rnd)
                    return
                if self._plant_gun(ct, p, site, rnd, live, want):
                    return
        # ⭐⭐ v632 PLANK 10 RUNG (b), SITING HALF -- AND IT IS THE HALF v630.1
        # HAD TO ADD.  v630.0's only heal caller sat in the `live >= want` hold
        # branch, which a body that has just lost a tube does NOT occupy: the
        # E4b falsifier measured 39 tube removals and 0 heals.  Post-flip, with
        # a four-tube target and 5-27 round lives, SITING is where this body
        # spends most of its game -- so this is where the dose actually lands.
        # Band-scoped inside `_guard_heal`; prep/plant above already returned if
        # they acted, so this fires only on their leftovers.
        if self._guard_heal(ct, p, rnd):
            return
        # ⭐⭐ v632 PLANK 10 RUNG (a) -- THE TERMINAL-APPROACH SEAT BIAS.  Walk
        # to the site's enemy-side seat rather than the site itself, so the
        # plant happens from the FRONT and the body is already standing between
        # the new tube and the enemy's guns the round it goes up.  With
        # SK_ROTATE_PREPS = 0 there is no barrier to lay -- Magnus's no-preps
        # ruling stands -- so THE BODY IS THE SCREEN, and it costs 0 Ti and 0
        # scale.  Already on the seat => STAND (the cooldown-0 block above
        # plants from here; a `step_to(site)` would wander onto the plant tile
        # itself).  Seat unreachable => exactly the un-guarded walk below.
        # ⛔ TERMINAL-ONLY, per v630.1's E6 attribution -- see
        # SK_ROTATE_GUARD_NEAR.
        if self._guard_walk(ct, p, site):
            return
        # ⭐⭐ s57 VOLUME ARM 1, PIECE (a) -- T13's VACATE RUNG, and it sits
        # HERE because this is the exact fall-through that puts the leader on
        # its own plant tile: `step_to(site)` from Manhattan 1 steps ONTO the
        # site (sk_roles.py's own terminal-approach note measures a plant
        # pushed r321 -> r338 through this line).  Above it, so the body leaves
        # rather than re-stepping onto the tile the trailer is waiting to
        # build.  Refuses and falls through whenever there is no trailer
        # beside the site, so an OFF/solo game reaches the same `step_to`.
        if self._vh_vacate(ct, p, site, rnd):
            return
        if self.step_to(ct, site):
            return
        # ⭐ v606 ITEM 4(a2) -- SK_IDLE_ACT, FOR THE ENGINEER.  The v603 clause
        # ("a body with no legal move must act") was wired into `_cage_walker`
        # twice and into NO other role, and the paths seat A diagnosis is what
        # that costs: bot 146 pinned on {(0,10),(0,11)} in a five-tile dead-end
        # for 105 turns, 37 of them with `free_neighbours == 0` and a zero action
        # cooldown.  Identical verb, identical guards; only the caller is new.
        # ⚠ v632 PLANKS 8+9, DISCLOSED SCOPE OF "NO PECKING".  The suppression
        # lives in `_attack_enemy_core` and covers the CORE peck and its
        # `_peck_priority` ladder -- the verb Magnus named ("no pecking, we only
        # watch our sentinels work") and the one that donates a raider's whole
        # game into a 0.68 heal-tax.  THIS rung survives for rotation bodies and
        # deliberately so: it fires only when the body has ZERO free
        # neighbours, i.e. it is boxed in and can neither walk nor plant this
        # turn, and it carries `skip_core=True` so it can never reach the enemy
        # footprint.  It is the v606 anti-pin verb, not a damage plan, and
        # removing it would re-open the 105-turn pin it was built for on a board
        # that is denser at r300 than at any earlier round.
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
        # ⭐⭐ v632 PLANKS 8+9 -- THE LEDGER IS AS WIDE AS THE BATTERY, AND
        # WITHOUT THIS THE `want` RAISE IS A NO-OP THAT SPENDS.  The ledger is
        # two slots; `_nest_live()` therefore CANNOT return more than 2, so a
        # `want` of 4 would be permanently unmet, `_plant_gun`'s slot loop would
        # silently find no free slot (the `break` never fires), and the engineer
        # would buy sentinels every affordable round with no book of what it
        # owns and no death memo for any of them.  Four named slots, four
        # entries, and every count / promotion / compaction below already runs
        # over `len(self._nest_slots())` (v619 wrote them generic).
        # ⛔ EXACT IDENTITY WHEN OFF: `rot_body` is False on every round of every
        # SK_ROTATE-off arm, so this returns v619's tuple unchanged and
        # `nest_turret4` is assigned by no path.
        # ⭐⭐ s57 THE BATTERY, ARM 1 (SK_BATTERY_WANT) -- THE SAME WIDENING,
        # FOR THE ARM THAT ACTUALLY RUNS.  The rot_body branch above is dead on
        # every SK_ROTATE-off arm and SK_ROTATE ships False, so the shipped
        # ledger is TWO slots and `_nest_live()` cannot return more than 2.
        # A ceiling of 4 against a 2-wide book is the failure that branch's own
        # note describes: `_plant_gun`'s slot loop finds no free slot, the
        # `break` never fires, and the engineer buys a sentinel every affordable
        # round with no book of what it owns and no death memo for any of them.
        # ⛔ EXACT IDENTITY WHEN OFF: SK_BATTERY_WANT is 0, so this returns
        # v619's tuple unchanged and `nest_turret4` is assigned by no path.
        # ⛔ AND IT IS INERT AT OR BELOW THE PAIR EVEN WHEN ON: every consumer
        # (`_nest_live`, `_nest_taken`, `_nest_watch`'s compaction,
        # `_plant_gun`'s first-empty loop) skips None entries and runs over
        # `len(self._nest_slots())`, so two extra None slots change no count,
        # no promotion and no site.
        # ⭐ s57 ARM 2: the same widening for the same reason -- the master
        # raises the ceiling to SK_BATTERY2_WANT, and a target wider than the
        # book is the failure this method's note describes.  Inert at or below
        # the pair either way (every consumer skips None entries).
        if self.rot_body or SK_BATTERY_WANT or SK_BATTERY2:
            return (self.nest_turret, self.nest_turret2,
                    self.nest_turret3, self.nest_turret4)
        if SK_NEST_N3:
            return (self.nest_turret, self.nest_turret2, self.nest_turret3)
        return (self.nest_turret, self.nest_turret2)

    def _nest_slot_set(self, i, v):
        if i == 0:
            self.nest_turret = v
        elif i == 1:
            self.nest_turret2 = v
        elif i == 2:
            # v632: was the `else` arm.  With SK_ROTATE off `_nest_slots()` is
            # at most three long, so index 3 is unreachable and this is v619's
            # branch on v619's inputs.
            self.nest_turret3 = v
        else:
            self.nest_turret4 = v

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

    # ==================================================================
    # s57 THE BATTERY, ARM 1 -- THE LIVE CEILING  (SK_BATTERY_WANT)
    # ==================================================================
    # GAME CONTEXT: in-game build work for the Florent Code League, a
    # sandboxed bot-vs-bot competition.  "battery", "tube", "plant" are
    # in-engine mechanics between competing game bots.
    #
    # THREE PURE-ISH HELPERS, AND NONE OF THEM IS REACHED ON AN OFF ARM:
    # every call site is guarded by `if SK_BATTERY_WANT:` at the ONE gate,
    # so with the flag 0 the added cost is one test of a module constant per
    # engineer round and the control flow is v632's, character for character.

    def _battery_bar(self, ct, live):
        """The purse a plant beyond the pair must clear, in titanium.

        ⛔ THIS IS `_plant_gun`'s OWN ELSE-BRANCH ARITHMETIC, RESTATED -- not a
        new policy.  There:
            cost = ct.get_sentinel_cost()
            ...
            cost += SK_AMMO_SENTINEL * (live + 1) + SK_AMMO_FLOOR
        and `SK_TUBE_FLOOR` ships False, so the SK_TUBE_FUND waiver above it is
        unreachable in this config and the else branch is the only branch a
        plant with `live > 0` can take.  Restated rather than refactored ON
        PURPOSE: making `_plant_gun` call this would add a second
        `get_sentinel_cost()` engine call to the OFF path, and the OFF path has
        to be byte-identical, which includes its CPU profile.  The weld is
        therefore a UNIT CONTROL, not shared code -- the control drives the bar
        to both verdicts (bar-1 refuses, bar accepts) THROUGH `_plant_gun`, so
        a drift between the two expressions is a failing test rather than a
        silent overspend.
        """
        return (ct.get_sentinel_cost()
                + SK_AMMO_SENTINEL * (live + 1) + SK_AMMO_FLOOR)

    def _battery_open(self, ct, rnd, live, want):
        """May the engineer buy ONE MORE tube above the pair, right now?

        FOUR CONDITIONS, AND EACH CLOSES A DIFFERENT ROAD:
          * `SK_BATTERY_WANT` -- the master.  0 = off.
          * `SK_NEST_PAIR` -- the pair machinery is what this raises the
            ceiling ON; with it off `want` is 1 and there is no battery to
            build.
          * `live >= want` -- BELOW the floor nothing changes.  This method is
            asked only about the rungs the hold branch would otherwise refuse,
            so plants 1 and 2 keep today's exact conditions by construction.
          * `live < ceiling` -- the ceiling itself, CLAMPED TO THE LEDGER
            WIDTH.  A book narrower than the target can never meet it, and an
            unmeetable target is the "buy every affordable round with no death
            memo" failure `_nest_slots()` warns about.  `len()` is read from
            the live tuple rather than assumed, so if a future flag narrows the
            book the clamp follows it.
          * the purse clears `_battery_bar` -- the affordability gate, and it
            is what makes the flag SELF-LIMITING.  Tested BEFORE the hold is
            skipped, so a cell whose purse never clears the bar never leaves
            the hold branch and its tape is unchanged.
        ⛔ IT READS, IT DOES NOT SPEND OR WRITE.  The only mutation in this
        family is `_battery_rearm`, and that one is free.

        ⭐⭐ s57 THE BATTERY, ARM 2 ADDS A FIFTH CONDITION AND SWAPS THE
        CEILING'S SOURCE.  The ECO-READY LATCH is asked LAST, AFTER the purse
        test, on purpose: `batt_unfunded` keeps meaning "the purse was short"
        and `batt2_eco_block` means "the purse was fine and the ECONOMY was
        not" -- two different refusals that a single tap would merge.  The
        ceiling reads SK_BATTERY2_WANT while the master is on so arm 1's
        constant keeps its arm-1 meaning and the two arms still run apart.
        ⛔ EXACT IDENTITY WHEN BOTH ARE OFF: SK_BATTERY_WANT is 0 and
        SK_BATTERY2 is False, so the first line returns False and nothing
        below it is reached.
        """
        if not ((SK_BATTERY_WANT or SK_BATTERY2) and SK_NEST_PAIR):
            return False
        if live < want:
            return False
        ceiling = SK_BATTERY2_WANT if SK_BATTERY2 else SK_BATTERY_WANT
        width = len(self._nest_slots())
        if ceiling > width:
            ceiling = width
        if live >= ceiling:
            self.batt_ceiling += 1
            return False
        try:
            bank = ct.get_global_resources()
        except Exception:
            return False
        # ITERATION 6 (w5diag): the reserve must be RESERVED — this gate read
        # the raw bank and barrel plants spent straight through the 120 while
        # the answer starved on 73% of its armed+targeted rounds. Under the
        # doctrine, barrels queue behind the defence's earmark.
        eff_bank = bank - (SK_DOC_ANSWER_RESERVE if SK_DOCTRINE else 0)
        if eff_bank < self._battery_bar(ct, live):
            self.batt_unfunded += 1
            return False
        # s57 ARM 2 (c): funded for ONE more barrel is not funded for the
        # HAMMER.  `_b2_eco_ready` returns True unconditionally when the piece
        # is ablated or the master is off, so this line is arm 1's behaviour
        # in both of those configurations.
        if not self._b2_eco_ready(ct, rnd):
            return False
        self.batt_open += 1
        return True

    def _battery_rearm(self):
        """Free the siting machinery when the site we are holding is SPENT.

        ⛔⛔ THIS IS THE ONE HAZARD THE CEILING CREATES AND IT WOULD HAVE BEEN
        A SELF-INFLICTED TUBE LOSS.  `_plant_gun` clears `nest_site` only when
        the post-plant count is still BELOW `want`; at the pair it leaves the
        just-built tile in `nest_site`, which is correct today because the body
        then holds station beside it forever.  With the ceiling raised the body
        falls through to the SITING branch instead, and that branch's first
        rung is SK_NEST_CLEAR: an occupied site whose building is OURS is
        cleared with a FREE `destroy` -- i.e. the engineer would demolish the
        sentinel it just built, every time, and `_nest_site_watch` would not
        stop it (it refutes WALLS and orbits, never occupancy).
        ⛔ THE TEST IS THE LEDGER, NOT THE ENGINE.  `get_tile_building_id` can
        raise out of bounds and answers nothing useful out of vision; the
        ledger is this body's own record of the tiles it has planted on, needs
        no call, and cannot raise.  A site whose tube has since died has
        already left the ledger -- and `_nest_watch` re-armed the machinery on
        that death anyway -- so this fires on exactly the spent-site case.
        ⛔ SAME FIELDS AS EVERY OTHER RE-SITE (`_nest_watch`'s V3 block,
        `_plant_gun`'s), so the re-pick that follows is the ordinary one:
        `nest_best_d = None` re-arms the v602 stuck watchdog and `nest_bad` is
        untouched, because a site that WORKED must stay re-sitable later.
        """
        s = self.nest_site
        if s is None:
            return
        for t in self._nest_slots():
            if t is not None and t[1].x == s.x and t[1].y == s.y:
                self.nest_site = None
                self.nest_face = None
                self.nest_prepped = 0
                self.nest_best_d = None
                self.batt_rearm += 1
                return

    # ==================================================================
    # s57 THE BATTERY, ARM 2  (SK_BATTERY2)
    # ==================================================================
    # GAME CONTEXT: in-game build work for the Florent Code League, a
    # sandboxed bot-vs-bot competition.  "battery", "barrel", "tube",
    # "plant", "hammer" are in-engine mechanics between competing game bots.
    #
    # SEVEN HELPERS, NONE OF THEM REACHED ON AN OFF ARM: every call site is
    # `if SK_BATTERY2 ...`, so with the master False the added cost is one
    # test of a module constant per engineer round and the control flow is
    # v632's, character for character.  The three pieces are ablatable apart
    # (SK_BATTERY2_LEDGER / _BURST / _ECO) because they are coupled by
    # ARGUMENT, and an argument has to be measurable.

    # --- (a) THE LEDGER FIX -------------------------------------------

    def _b2_phantom(self, ct, rnd, tid, site, ledger, beats):
        """Is this `get_hp` exception SILENCE rather than a death?

        THREE CONDITIONS, ALL REQUIRED, and each one is a different way this
        could go wrong (see the SK_BATTERY2_LEDGER note for the provenance):
          * the TEAM BEAT count has not fallen below what the ledger claims,
            COMPARED AT THE CENSUS CAP.  v619's rule is `beats >= ledger`;
            above the cap that is guaranteed False (the slot-7 layout has
            len(SK_TUBE_SEAT_FIELDS) seats and a third tube is invisible by
            construction), so the unclamped form books a death on the first
            out-of-vision read of barrel #3 EVERY TIME -- the exact bug this
            piece removes.  Below the cap the two forms are identical, which
            is what keeps the pair's behaviour unchanged.
          * the credit has NOT EXPIRED.  Without this the rule LATCHES above
            the cap: the beats can no longer fall, so a barrel that really
            died out of vision would be booked alive for the rest of the
            match and would block its own replacement.
          * the site is provably OUTSIDE this body's vision.
            `_out_of_vision` is radius arithmetic on two positions we already
            hold and returns False on any doubt -- so doubt routes to v632's
            behaviour (spend a turn), never to hiding a hole.  It is NOT
            `is_in_vision`, which is a pure radius test with no bounds check
            (engine-probed s50) and the band hugs a corner core.
        ⛔ READS ONLY.  The taps are counters; nothing here spends or writes.
        """
        if not (SK_BATTERY2 and SK_BATTERY2_LEDGER):
            return False
        if beats is not None:
            cap = len(SK_TUBE_SEAT_FIELDS)
            need = ledger if ledger < cap else cap
            if beats < need:
                return False          # a tube HAS gone quiet: book the death
        last = self.batt2_seen.get(tid)
        if last is None or rnd - last > SK_BATTERY2_LEDGER_TTL:
            self.batt2_expired += 1
            return False              # absence of evidence has expired
        return self._out_of_vision(ct, site)

    def _b2_live(self, ct, rnd, ledger):
        """(a)'s second half: `max(own ledger, team beats)`.

        The phantom rule repairs what THIS BODY forgot.  It cannot supply what
        this body never knew: `_nest_live()` is a per-body PLANT ledger, and a
        tube planted by a previous engineer is in nobody's book.  Measured on
        the traced f1 tape: 376 of 1,172 phantom decisions read ledger 1 while
        the team beats read 2.
        ⛔ IT CAN ONLY LIFT, NEVER LOWER -- an under-count buys a barrel we
        already own, an over-count delays a replant by at most the producer's
        own staleness bound.  And it saturates at the census width, so no rung
        above the pair can be invented by it.
        ⛔ FALLS BACK TO THE LEDGER ON ANY DOUBT (flag off, producer off, store
        unreadable), so every caller reduces to v632's code on v632's inputs.
        """
        if not (SK_BATTERY2 and SK_BATTERY2_LEDGER and SK_BATTERY2_LIVE_TEAM
                and SK_TEAM_TUBES and SK_NEST_PAIR):
            return ledger
        try:
            team = self._tube_count(ct.read_store(SK_SLOT_NEST), rnd)
        except Exception:
            return ledger
        if team > ledger:
            self.batt2_live_lift += 1
            return team
        return ledger

    # --- (b) THE BURST RULE -------------------------------------------

    def _b2_pair_bar(self, ct):
        """The purse that funds BOTH barrels of the pair, in titanium.

        ⛔ IT IS `_plant_gun`'s OWN ARITHMETIC FOR THE TWO PLANTS, RESTATED,
        exactly as `_battery_bar` restates the single-plant form and for the
        same reason (calling into `_plant_gun` would put a second
        `get_sentinel_cost()` on the OFF path, and the OFF path has to be
        byte-identical including its CPU profile).  The weld is a UNIT
        CONTROL, not shared code:
            plant #1 at live = 0 -> `cost = get_sentinel_cost()` and NOTHING
              else: the `if SK_NEST_PAIR and live > 0` branch is skipped;
            plant #2 at live = 1 -> `get_sentinel_cost()` AT THE POST-PLANT
              SCALE, plus SK_AMMO_SENTINEL x (live + 1) + SK_AMMO_FLOOR.
        The post-plant scale is the only term that cannot be read today, and
        it is a CONSTANT offset because the cost factor is ONE GLOBAL
        ADDITIVE number: SK_BATTERY2_SENT_BUMP = floor(base x 20%).
        ⚠ WHAT IT DELIBERATELY DOES NOT PRICE: the second site's prep
        barriers (2 x 3 Ti and +2% of scale).  They are paid out of income
        during the commute in every arm, and folding them in would raise the
        bar for a cost the hold does not change.
        """
        c = ct.get_sentinel_cost()
        return (c + (c + SK_BATTERY2_SENT_BUMP)
                + SK_AMMO_SENTINEL * 2 + SK_AMMO_FLOOR)

    def _b2_burst_hold(self, ct, rnd, live, want):
        """True on a round where plant #1 is WITHHELD for the pair.

        SCOPE IS THE FIRST PLANT OF THE PAIR AND NOTHING ELSE (`live == 0`
        and a target of at least two).  Barrels beyond the pair are the
        ceiling's and the latch's business; the measured defect this piece
        answers is the PAIR's spacing (wins' tightest 2-build window 9 rounds
        vs losses' 16; the arm-1 trace's worked stagger cell shows 54- and
        31-round money-blocked gaps).

        ⛔ THE ESCAPE IS PART OF THE RULE, NOT A SAFETY NET BOLTED ON.  A
        cell that can never fund two must not be held forever -- so after
        SK_BATTERY2_BURST_HOLD consecutive holding rounds the burst DISARMS
        FOR THE MATCH and plant #1 goes in under today's exact condition.
        Both verdicts of that clock are counted (`batt2_escape`,
        `batt2_hold_rounds`), because an escape that has never been seen to
        fire has not been seen to protect anything.
        """
        if not (SK_BATTERY2 and SK_BATTERY2_BURST and SK_NEST_PAIR):
            return False
        if self.batt2_burst_off:
            return False
        if live != 0 or want < 2:
            return False
        try:
            bank = ct.get_global_resources()
            bar = self._b2_pair_bar(ct)
        except Exception:
            return False              # unreadable purse -> v632 behaviour
        if bank >= bar:
            self.batt2_burst_ready += 1
            self.batt2_hold_since = None
            return False
        if self.batt2_hold_since is None:
            self.batt2_hold_since = rnd
            self.batt2_holds += 1
        if rnd - self.batt2_hold_since >= SK_BATTERY2_BURST_HOLD:
            self.batt2_burst_off = True
            self.batt2_escape = rnd + 1        # round+1, so 0 means NEVER
            self.batt2_hold_since = None
            return False
        self.batt2_hold_rounds += 1
        return True

    def _b2_hold_clocks(self, rnd):
        """⛔⛔ THE HAZARD THE HOLD CREATES, AND IT WOULD HAVE BEEN A
        PERMANENT SITE BAN.  `_nest_site_watch` is a PROGRESS watchdog: a
        site the body has not closed on for SK_NEST_STUCK_ROUNDS rounds goes
        into `nest_bad` FOREVER.  A body that has ARRIVED and is standing
        still because it is saving money records no new closest approach and
        no net displacement, so the watchdog would read the funding hold as
        an unreachable site and ban the tile the pair is waiting on.
        The hold refreshes exactly the two clocks the watchdog runs on --
        the same fields `_nest_site_watch` itself refreshes on progress --
        and nothing else: `nest_best_d` is untouched, so the moment the hold
        ends the watchdog resumes from the body's true closest approach.
        ⛔⛔ AND IT IS LOAD-BEARING, MEASURED -- THE FIRST VERSION OF THIS
        NOTE SAID THE OPPOSITE AND ITS OWN MUTATION CONTROL REFUTED IT.  The
        argument was: the hold is bounded by SK_BATTERY2_BURST_HOLD = 20,
        which is under SK_NEST_STUCK_ROUNDS = 25, so the ban could not fire
        even with this method deleted.  WRONG, and the reason is that
        `nest_since` is NOT set when the hold starts -- it is set at the
        body's last CLOSEST APPROACH, which is several rounds earlier (the
        arrival, then the prep barriers, then the hold).  Deleting this
        method (mutation M4) diverges the tape on 3 of 12 f1 cells
        (auroraveil A, bifrost A, skald A).  The suppression is still bounded
        by the hold, but the hold really can reach the watchdog, so the
        refresh is a correctness requirement rather than a belt-and-braces.
        """
        self.nest_since = rnd
        self.nest_anchor_rnd = rnd

    # --- (c) THE ECO-READY LATCH --------------------------------------

    def _b2_sample(self, ct, rnd):
        """One purse sample per engineer round -> the income proxy.

        ⛔ WHY POSITIVE DELTAS AND NOT A SPEND LEDGER.  The honest quantity
        is income, and `get_global_resources()` deltas are income MINUS the
        whole team's spend -- of which this body knows only its own share
        (the core converts ammo, the keeper builds belt, every builder
        spends).  A per-body spend ledger would therefore be a WRONG
        correction wearing a precise name.  The cheap honest proxy instead:
        a round's delta is counted only when it is POSITIVE, because only
        income can raise the purse (passive +10 every 4 rounds, a delivered
        stack +10; `destroy` refunds SCALE, not titanium).  A round that both
        earns and spends nets to <= 0 and contributes ZERO, so the proxy is a
        strict LOWER BOUND on gross income per round -- the conservative
        direction for a signal that authorises spending.
        ⛔ ROLLING MEAN, NOT EWMA: an EWMA seeded at 0 is biased low for
        about two windows, and this body's history restarts on every engineer
        turnover, so the bias would express itself as "the latch fires late
        or never" for a reason that is not economic.
        ⚠ DISCLOSED: the sampler is PER BODY.  A successor engineer starts
        with an empty ring and re-warms; the fire-round distribution is
        measured with that in it, not corrected for it.
        """
        if not (SK_BATTERY2 and SK_BATTERY2_ECO):
            return
        if rnd == self.batt2_last_rnd:
            return
        try:
            bank = ct.get_global_resources()
        except Exception:
            return
        ammo = 0
        if SK_BATTERY2_ECO_CONV:
            try:
                ammo = ct.get_global_ammo()
            except Exception:
                ammo = self.batt2_last_ammo or 0
        if self.batt2_last_bank is not None and rnd - self.batt2_last_rnd == 1:
            d = bank - self.batt2_last_bank
            # ⭐ THE CONVERTED HALF.  The ONLY ammunition source in this engine
            # is the core converting titanium 1:1 (no passive ammo income), so
            # a positive ammo delta is titanium that ARRIVED and was spent in
            # the same round -- income the bank-only form throws away, and
            # LOSSAUT measures that as the normal round (spend/convert
            # 0.94-0.99), not the exception.
            if SK_BATTERY2_ECO_CONV and self.batt2_last_ammo is not None:
                da = ammo - self.batt2_last_ammo
                if da > 0:
                    d += da
            if d < 0:
                d = 0
            self.batt2_ring.append(d)
            self.batt2_sum += d
            if len(self.batt2_ring) > SK_BATTERY2_ECO_W:
                self.batt2_sum -= self.batt2_ring.pop(0)
        self.batt2_last_bank = bank
        self.batt2_last_ammo = ammo if SK_BATTERY2_ECO_CONV else None
        self.batt2_last_rnd = rnd

    def _b2_rate(self):
        """Titanium per round of income, or None while under-sampled."""
        n = len(self.batt2_ring)
        if n < SK_BATTERY2_ECO_WARM:
            return None
        return self.batt2_sum / float(n)

    def _b2_eco_ready(self, ct, rnd):
        """PROGRAMME.md ECO-READY HAMMER, made a predicate: are we FUNDED to
        sustain the hammer, rather than able to afford one more barrel at one
        instant?

        THE BAR IS TWO TERMS AND BOTH ARE BANKED NUMBERS:
          * SK_BATTERY2_ECO_AMMO -- the ammunition stream a checkmate needs
            (LOSSAUT-f1f2: ~2.5-3.0 Ti/round buys the 4.5-5.3 HP/round that
            clears their core's heal absorption; we run 1.47 in losses,
            4.30 in wins);
          * BARREL REPLACEMENT -- `get_sentinel_cost() / SK_BATTERY2_ECO_LIFE`,
            the live-scaled price of a barrel amortised over the MEASURED
            median life of our own forward tubes.
        ⛔ IT LATCHES, AND THE LATCH IS SAFE BECAUSE IT IS NOT THE ONLY GATE.
        Once readiness is established the hammer stays open; a later collapse
        is still caught per plant by `_battery_bar`, which this predicate is
        asked AFTER.  A non-latching form would flap the battery target round
        by round, which is the behaviour `_nest_slots()`'s note warns about.
        ⛔ AND IT IS SCORED BOTH WAYS BEFORE ANY OUTCOME COLUMN (the side-lane
        rider, consumed in the arm-2 registration): the fire-round
        distribution per fixture -- median, p10, never-fired -- must show the
        latch CHOOSING.  Never firing is falsifier LOW (no hammer ever lands);
        firing at spawn-adjacent rounds is falsifier HIGH (it degenerated to
        always-true and the hammer is the rush the doctrine forbids).
        """
        if not (SK_BATTERY2 and SK_BATTERY2_ECO):
            return True
        if self.batt2_eco_since is not None:
            return True                        # latched
        r = self._b2_rate()
        if r is None:
            # ⛔ s57 SK_HAMMER_PRIO V2: ONE TICK PER ROUND, NOT ONE PER CALL.
            # With the master on this predicate is asked twice in a round (the
            # unconditional site, then `_battery_open`), and an un-guarded tap
            # would double-count ONE refusal.  Short-circuited away when the
            # master is off, so the OFF path keeps today's exact control flow.
            if not SK_HAMMER_PRIO or self._b2_eco_tick(rnd):
                self.batt2_eco_cold += 1
            return False
        # ⛔ ARM-3 CORRECTION (s57, registered before this edit): the barrel
        # term double-counted — `_battery_bar` already prices the next barrel
        # at every plant, so charging replacement here priced it twice and the
        # latch fired 1/60 (falsifier LOW, arm-2 readout). The bar is the
        # ammo stream alone; the barrel-replacement form is kept under
        # SK_BATTERY2_ECO_BARREL for the record and ships False.
        try:
            bar = SK_BATTERY2_ECO_AMMO
            if SK_BATTERY2_ECO_BARREL:
                bar += ct.get_sentinel_cost() / float(SK_BATTERY2_ECO_LIFE)
        except Exception:
            return False
        if r < bar:
            if not SK_HAMMER_PRIO or self._b2_eco_tick(rnd):   # V2, as above
                self.batt2_eco_block += 1
            return False
        self.batt2_eco_since = rnd
        return True

    def _b2_eco_tick(self, rnd):
        """s57 SK_HAMMER_PRIO V2 -- may THIS refusal tick a counter?

        A per-round de-duplicator and nothing else: the first evaluation of a
        round ticks, any further evaluation of the SAME round does not.  The
        two refusal paths in `_b2_eco_ready` are mutually exclusive per call,
        so one marker covers both.  ⛔ IT MOVES NO DECISION -- both callers use
        the predicate's return value, never this counter -- so a bug here can
        only ever mis-report, never mis-play.  Reachable only while the master
        is ON (every call site is `not SK_HAMMER_PRIO or ...`).
        """
        if rnd == self.batt2_eco_miss_rnd:
            return False
        self.batt2_eco_miss_rnd = rnd
        return True

    def _pick_nest(self, ct, p, rnd, near=False):
        """The band, with LEDGER V4's per-tile death memory applied.

        ⭐⭐ s57 BARRELS ARM 2 ADDS ONE OPTIONAL ARGUMENT AND TWO OPTIONAL
        FILTERS, ALL DEFAULTED OFF.  `near=True` (piece (b), the successor
        pick) turns on v619 PLANK 2's nearness-first ORDERING -- a reordering
        of an identical legal set.  Piece (c) adds their-ray AVOIDANCE (a score
        term, so it can never empty the band) and a BOUNDED killer-coverage BAN
        (a filter, with its own retry).  Every existing caller passes neither,
        and with the master off both are unreachable, so this method is
        character-for-character v632's on every OFF arm.

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
        # ⭐ s57 BARRELS ARM 2, PIECE (b): the successor pick leads with
        # PROXIMITY.  Same `haste` parameter, same reordering, same legal set --
        # the arm buys the ordering, not a new rule.  `near` is False on every
        # existing call site.
        if near and SK_BARREL_GUARD and SK_BG_SUCC:
            haste = True
        # ⭐⭐ s57 BARRELS ARM 2, PIECE (c) -- THE SITE GUARD, SUCCESSOR PICKS
        # ONLY.  `cover` is a SCORE term (uncovered tiles rank first) so it can
        # never empty the band; `block` is the bounded killer-coverage ban and
        # gets its own retry immediately below.
        cover = block = None
        guns = ()
        if self._bg_site_class(taken):
            guns = self._bg_guns(ct)
            cover = self._bg_cover(ct, guns) if guns else None
            block = self._bg_ban_set(rnd)
        # ⭐⭐ v632 PLANKS 8+9 -- THE FIRST BATTERY IS CLUSTERED.  Magnus,
        # direct: "put the first 4 sentinels together ... then move to the next
        # position".  `SK_NEST_PAIR_MIN_GAP = 8` is v603's answer to a
        # DIFFERENT question -- two tubes sharing one answering gunner's ray --
        # and it is priced for a PAIR whose job is to survive; a battery of four
        # is priced on damage per round onto ONE core face and on the walk it
        # costs to lay it.  Relaxed for the first SK_ROTATE_WANT plants of the
        # phase only, then v603's spread returns for REPLACEMENTS, which is what
        # "then move to the next position" asks for and what keeps the rolling
        # half of the siege from re-stacking on a tile that just lost a tube.
        # ⭐ THE COMMUTE PICKS UNDER THE SAME RULE IT WILL PLANT UNDER.  If the
        # prestage target were chosen at the spread and the r300 plant at the
        # cluster gap, the body would walk ten rounds to a tile it then declines
        # -- the arrival gain this redesign exists for, spent twice.
        gap = SK_NEST_PAIR_MIN_GAP
        if ((self.rot_body or self.rot_stage)
                and self.rot_plants < SK_ROTATE_WANT):
            gap = SK_ROTATE_CLUSTER_GAP
        site = self._nest_scan(ct, p, rnd, taken, gap, haste=haste,
                               cover=cover, block=block)
        # ⭐⭐ s57 BARRELS ARM 2, PIECE (c) -- THE ANTI-SPIRAL RETRY, AND IT IS
        # WHAT KEEPS THE BAN FROM MAKING THE WALK-OUT WORSE.  If the bounded ban
        # emptied the band, the SAME scan runs again without it, BEFORE any
        # existing fallback.  So the guard can only ever change WHICH tile the
        # primary scan returns -- never whether the relax/exhaust retries below
        # run, and never whether a site exists at all.  Counted, so "it never
        # bound" and "it bound and was relaxed" are different readings.
        if site is None and block:
            site = self._nest_scan(ct, p, rnd, taken, gap, haste=haste,
                                   cover=cover, block=None)
            if site is not None:
                self.bg_site_relax += 1
        if guns and site is not None:
            self._bg_confirm(ct, guns, cover or (), site)
        # ⭐ v613 PLANK 2(c), SK_TUBE_GAP_RELAX.  "The band d^2 14-32 is wide
        # enough" is true on a 30x30 and NOT on a 12x12: with one tube standing,
        # an 8-d^2 spread can empty the band outright, and the engineer then
        # sites nothing at all while the anatomy's win precondition -- TWO tubes
        # standing simultaneously -- is exactly what is missing.  An unspread
        # second tube is 18 HP/round; no second tube is 9.  Retry ONLY when the
        # spread was the thing that emptied the band, so the flag off is an
        # exact identity.
        if (site is None and (SK_TUBE_FLOOR or SK_GAP_RELAX_SOLO)
                and SK_TUBE_GAP_RELAX and taken
                and SK_TUBE_GAP_MIN < SK_NEST_PAIR_MIN_GAP):
            # v622 PLANK 1: `SK_GAP_RELAX_SOLO` arms this retry without the
            # floor; the conjunction is otherwise v613's, character for
            # character, so SOLO off is an exact identity.
            site = self._nest_scan(ct, p, rnd, taken, SK_TUBE_GAP_MIN,
                                   haste=haste)
            if site is not None:
                self.tube_gap_relax += 1
        # ⭐ v622 PLANK 2 (SK_NEST_EXHAUST_PB): the band -- relax included -- is
        # EMPTY.  Retry once at lo=2 (the point-blank band the v1 ban excludes)
        # and, when a pair gap exists, at the relaxed spread, because a retry
        # priced against "zero tubes forever" takes the most permissive legal
        # set it can get.  Runs only on total exhaustion, so every cell where
        # the primary scan succeeds is untouched by construction.
        if site is None and SK_NEST_EXHAUST_PB:
            site = self._nest_scan(ct, p, rnd, taken,
                                   min(SK_TUBE_GAP_MIN, SK_NEST_PAIR_MIN_GAP),
                                   haste=haste, lo=2)
            if site is not None:
                self.nest_exhaust_pb += 1
        if site is not None:
            self.nest_face = self._firing_face(site)
            self.nest_prepped = 0
        return site

    def _nest_scan(self, ct, p, rnd, taken, gap, haste=False, lo=None,
                   cover=None, block=None):
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
        # v622: an explicit `lo` (the exhaustion retry passes 2) overrides the
        # default band floor; every prior caller passes nothing and is
        # unchanged.
        if lo is None:
            lo = SK_NEST_DSQ_MIN if not SK_NEST_POINT_BLANK else 2
            # ⭐ v626 PLANK B (SK_NEST_PB_LIFE): COPY 5's dependency, readable
            # in-game -- point-blank only where the opponent has measurably
            # failed to clear our tubes.  Expected shut on every measured cell.
            if (SK_NEST_PB_LIFE and len(self.nest_lives) >= SK_NEST_PB_LIFE_N
                    and (sum(self.nest_lives) // len(self.nest_lives))
                        >= SK_NEST_PB_LIFE_R):
                lo = 2
                self.nest_pb_life += 1
        # ⭐⭐ s57 SK_DOCTRINE -- THE STANDOFF RE-BAND, AND IT IS THE FIELD'S
        # BAND, NOT OURS.  PROGRAMME.md, the identity inversion: Jython v266
        # swept us 5-0 playing "pure eco -> standoff sentinels d^2 16-25".  The
        # burst sites inside SK_DOC_DSQ_MIN..MAX instead of COPY 5's 14..32.
        # ⛔ IT SITS IMMEDIATELY BELOW THE `lo` RESOLUTION AND NOWHERE HIGHER:
        # placed above it, `lo` is still None and the floor swap cannot be
        # expressed; placed lower, the sweep has already begun.
        # ⛔ SCOPED TO A BURST BODY (`self.rot_body`, which under SK_DOCTRINE
        # means "the trigger has fired and this body is a raider").  A phase-1
        # body never reaches this method at all, and a NON-doctrine arm has
        # SK_DOCTRINE False on the first term -- so `hi` is SK_NEST_DSQ_MAX and
        # `lo` is untouched on every existing caller and every OFF arm,
        # character for character.
        # ⛔ THE FLOOR SWAP IS CONDITIONAL ON `lo` STILL BEING THE DEFAULT, so
        # the point-blank exhaustion retry (which passes lo=2 explicitly) and
        # SK_NEST_PB_LIFE keep their exact meaning: a burst body that has
        # exhausted the band still gets the permissive last-resort set rather
        # than being narrowed into nothing.
        hi = SK_NEST_DSQ_MAX
        _doc_band = bool(SK_DOCTRINE and self.rot_body)
        if _doc_band:
            hi = SK_DOC_DSQ_MAX
            if lo == SK_NEST_DSQ_MIN:
                lo = SK_DOC_DSQ_MIN
            if lo > hi:
                # ⛔ A FLOOR ABOVE THE NARROWED CEILING WOULD EMPTY THE BAND
                # OUTRIGHT.  No caller does this today (the only explicit `lo`
                # is 2), but a band whose floor exceeds its ceiling returns None
                # for a reason that has nothing to do with the board -- so the
                # ceiling yields rather than the search dying, and the yield is
                # counted.
                hi = SK_NEST_DSQ_MAX
                self.doc_band_relax += 1
        # ⭐ s57 SK_DOCTRINE -- THE CARDINAL RANK TERM, ARMED WITHOUT
        # SK_VOLUME.  The VOLUME arm measured this piece's DOSE CONFIRMED
        # (+8pp orthogonally-aligned plants) and was refused on its OTHER piece
        # (the column handoff: 0 trailer plants, staffing form 5).  The doctrine
        # takes the confirmed piece and leaves the refused one off -- SK_VOLUME
        # stays False, so `_vh_publish`, `_vh_turn` and the whole column remain
        # unreachable.  ⛔ ONE DEFINITION: this arms the SAME scoring block
        # below, it does not restate the rule.
        _card_on = bool((SK_VOLUME and SK_VH_CARDINAL and SK_VH_CARD_AFTER_D)
                        or (_doc_band and SK_DOC_CARDINAL))
        # ⭐⭐ v632 PLANKS 8+9, HAZARD (b) -- SITE COLLISION, AND THE STUDY'S OWN
        # SPLIT KEY DOES NOT WORK.  §8a hazard 2: `_nest_taken()` is a PER-BODY
        # ledger, so two raiders' spread checks see only their own tubes and
        # nothing stops them siting the same tile or fighting over one corner of
        # the band.  The study prescribes "a band half by role parity
        # (`self.role_parity`)" -- ⛔ AND role_parity CANNOT SPLIT THESE TWO
        # BODIES: it is `self.role & 1` (`_claim_role`), the raiders are roles
        # 1 and 3, and 1 & 1 == 3 & 1 == 1.  BOTH HALVES WOULD BE THE SAME HALF
        # and the hazard would ship unaddressed behind a line of prose that
        # looks like it addresses it.  The split key is therefore the role
        # IDENTITY, which does distinguish them.
        # ⛔ THE SPLIT KEY, AND ITS SIZE COST IS MEASURED, NOT ASSUMED.  Counted
        # over the scan's own sweep: `dx + dy >= 0` gives halves of 28 and 36
        # band tiles, and so does the obvious alternative `dx >= 0` -- 12%
        # imbalance either way, inherited from the asymmetric [-7, 9) sweep and
        # the 2x2 clamp in `dsq_core`, NOT from the choice of key.  ⭐ WHAT DOES
        # differ is which core faces a half touches: `dx >= 0` gives one body a
        # column that reaches three of the four faces and the other only one,
        # while the anti-diagonal cuts through opposite corners so each half is
        # an arc against two adjacent faces.  ⭐ AND BOTH HALVES CARRY THE FULL
        # BAND -- measured d^2 16..32 on each side (16, not 14, is the closest
        # value the clamp grid realises and is pre-existing) -- so the +30%
        # turret-life premium the band is bought for is intact for both raiders.
        # ⭐ THE COMMUTE IS SPLIT TOO -- and this is the half of the redesign
        # that makes the prestage worth walking: two bodies that pre-stage into
        # the SAME arc arrive early and then fight over it.
        rot_half = None
        if self.rot_body or self.rot_stage:
            rot_half = 1 if self.role == SK_SIEGE_ENGINEER else 0
        for dx in range(-7, 9):
            for dy in range(-7, 9):
                if rot_half is not None and (1 if dx + dy >= 0 else 0) != rot_half:
                    continue
                x, y = ex + dx, ey + dy
                if not self.ib(x, y):
                    continue
                q = Position(x, y)
                d = dsq_core(q, self.enemy)
                # ⭐ s57 SK_DOCTRINE: `hi` is SK_NEST_DSQ_MAX on every OFF arm
                # and on every non-burst caller, so this line is the v622 line
                # in value.
                if d < lo or d > hi:
                    continue
                if self.wall_at(x, y):              # v602 FIX 5(b)
                    continue
                if (x, y) in self.nest_bad:         # v602: refuted / unreachable
                    continue
                if (x, y) in self.nest_deaths and rnd - self.nest_deaths[(x, y)] < SK_DEATH_MEMO_ROUNDS:
                    continue
                # ⭐ s57 BARRELS ARM 2, PIECE (c) -- THE BOUNDED KILLER-COVERAGE
                # BAN.  `block` is None on every existing caller and on every
                # OFF arm, so this is one `is not None` test there.
                if block is not None and (x, y) in block:
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
                # ⭐ s57 SK_DOCTRINE: the max-range DIAGONAL bonus is keyed on
                # the LIVE ceiling `hi`, not on the module constant, or the
                # burst would rank against a d^2 its own band excludes.  `hi ==
                # SK_NEST_DSQ_MAX` on every OFF arm, so both lines are v619's in
                # value.  ⚠ AND UNDER THE DOCTRINE BAND THE TERM IS DEAD BY
                # ARITHMETIC: a diagonal has d^2 = 2k^2 and SK_DOC_DSQ_MAX = 26
                # is not of that form, so the leading key is constant-False and
                # the ordering reduces to depth-first with the cardinal term as
                # the first real tie-break.  Disclosed at SK_DOC_DSQ_MAX.
                if haste:
                    score = (-p.distance_squared(q),
                             d == hi and abs(dx) == abs(dy), d)
                else:
                    score = (d == hi and abs(dx) == abs(dy), d, -p.distance_squared(q))
                # ⭐⭐ s57 VOLUME ARM 1, PIECE (b) -- CARDINAL-FIRST SITING,
                # INSERTED IMMEDIATELY AFTER `d` IN BOTH ORDERINGS.  The
                # dossier's shortlist item 3, off the bisons autopsy: 142 of
                # 142 of their fast-kill sentinel builds are ORTHOGONALLY
                # ALIGNED with a core tile (field 56.6%, us 40.4%).  "AT EQUAL
                # REACH" is made literal by the POSITION of the key -- after
                # `d`, so it separates only sites that already tie on every key
                # above it, d^2 included.
                # ⛔ A RANK, NEVER A FILTER: the legal set is untouched, so the
                # band can never empty and this cannot create a plant v632
                # would have refused.
                # ⛔ THE TERM IS `face.is_cardinal()` ON A DIRECTION THE SCAN
                # HAS ALREADY COMPUTED -- `_firing_face` returns a cardinal
                # direction exactly when dx == 0 or dy == 0 for some footprint
                # tile, which IS the bisons' measure.  Pure Python, zero engine
                # calls, and no second definition that could drift.
                # ⚠ DISCLOSED INTERACTION: v618's LEADING key is the max-range
                # DIAGONAL bonus (T13's own d^2 = 32 site), so where such a
                # tile is legal it still wins and this term bites on every
                # other pick.  Deliberately not resolved here -- reordering
                # v618's key would be a second behaviour change under one flag.
                # ⭐ s57 SK_DOCTRINE arms this SAME block through `_card_on`
                # (see its note above): `_card_on` is exactly
                # `SK_VOLUME and SK_VH_CARDINAL and SK_VH_CARD_AFTER_D` on every
                # non-doctrine arm, so the OFF path is character-for-character
                # v632's.
                if _card_on:
                    if SK_VH_CARD_FACE:
                        try:
                            _vc = bool(face.is_cardinal())
                        except Exception:
                            _vc = False
                    else:
                        _vc = (dx == 0 or dy == 0)
                    self.vh_card_n += 1
                    if _vc:
                        self.vh_card_hit += 1
                    if haste:
                        score = score + (_vc,)
                    else:
                        score = (score[0], score[1], _vc, score[2])
                # ⭐⭐ s57 BARRELS ARM 2, PIECE (c) -- THEIR RAY, PREPENDED AS A
                # PREFERENCE AND NOT AS A FILTER.  Magnus's wording is "a term
                # PREFERRING tiles no standing visible enemy turret bears on",
                # and the distinction is load-bearing: a filter can empty the
                # band and cost us the tube outright, while a leading score key
                # takes an uncovered tile when one exists and the same tile as
                # today when none does.  Both orderings get the same prefix, so
                # the arm composes with `haste` instead of replacing it.
                if cover is not None:
                    score = ((x, y) not in cover,) + score
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

    def _nest_clear_ban(self, site):
        """v626 PLANK A: give up on an occupied site exactly the way the orbit
        watchdog does -- same fields, 13-48 rounds sooner."""
        self.nest_bad.add((site.x, site.y))
        self.nest_site = None
        self.nest_face = None
        self.nest_prepped = 0
        self.nest_best_d = None
        self.nest_anchor = None
        self.nest_clear_tile = None

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

    # ==================================================================
    # v632 PLANK 10 -- BATTERY SURVIVAL (SK_ROTATE_GUARD).  Both helpers
    # are PORTS of `bots/_v630tubeguard/sk_roles.py`, verbatim except for
    # the flag name (SK_TUBE_GUARD_NEAR -> SK_ROTATE_GUARD_NEAR).  They
    # are pure predicates: neither is reached on any SK_ROTATE_GUARD-off
    # round, and neither mutates state.
    # ==================================================================

    def _near_live_tube(self, ct, p):
        """Is this body within d^2 <= SK_ROTATE_GUARD_NEAR of a LIVE forward
        tube of ours?  (v630.1's `_near_live_tube`, WIDENED -- see below.)

        Gates the heal rung to the BAND, so a walk through home territory can
        never stall on a pecked conveyor -- the E6 lesson that behaviour
        leaking outside the band is how v630 lost checkmates.

        ⭐⭐ THE AMENDMENT (commissioned 2026-08-23,
        `docs/research/EXPECTATION-v632heim-plank10-2026-08-23.md`), AND THE
        PROVENANCE IS THIS PLANK'S OWN BUILD SMOKE.  v630's predicate read the
        body's PLANT LEDGER, and `_plant_gun`'s slot assignment is that
        ledger's only writer -- so it names only tubes THIS body planted.  Each
        unit gets its own `Player`, so post-flip a REPLACEMENT raider walks to
        a standing battery with an EMPTY ledger and its heal rung is dead for
        its whole life.  That is the normal case, not the edge one: the parked
        FUND arm's jotunheim cell cycled EIGHT raider bodies between r300 and
        r1000 (each living 47-120 rounds), and the 3-cell ON smoke measured our
        post-flip heals landing on a standing tube at 0 of 0.
        ⇒ THE BAND IS NOW A CENSUS, NOT A MEMORY: any of OUR sentinels this
        body can SEE, standing forward of `GUARD_FWD_DSQ` from our own core.

        ⛔ THE LEDGER HALF IS KEPT AND RUNS FIRST.  It is strictly cheaper (no
        engine calls) and it covers the one case the census cannot: a tube this
        body planted that has walked out of its own vision.  The census is a
        WIDENING, so the old True set is a subset of the new one.

        ⛔ BOUNDS BEFORE ANY TILE CALL (CLAUDE.md s50: `is_in_vision` is a pure
        radius test and is NOT a bounds guard; the next `get_tile_*` on an
        off-map tile RAISES, and an escaping exception destroys the unit
        permanently).  Nothing here reads a TILE -- the census reads entity
        properties by id, which the engine reports in-bounds by construction --
        but `self.ibp` is asserted on every position anyway, and every engine
        call sits under try/except, because a degraded read must cost this rung
        and never the body.
        """
        for t in self._nest_slots():
            if t is None:
                continue
            if p.distance_squared(t[1]) <= SK_ROTATE_GUARD_NEAR:
                return True
        # --- the vision census -------------------------------------------
        if self.core is None or self.team is None:
            return False
        try:
            ids = ct.get_nearby_buildings()
        except Exception:
            return False                      # degraded read: no band, no heal
        for bid in ids:
            try:
                if ct.get_team(bid) != self.team:
                    continue                  # an OPPOSING bot's turret
                if ct.get_entity_type(bid) != EntityType.SENTINEL:
                    continue                  # gunners/belts are not the tube
                q = ct.get_position(bid)
            except Exception:
                continue
            if q is None or not self.ibp(q):
                continue
            if dsq_core(q, self.core) <= GUARD_FWD_DSQ:
                continue                      # a HOME sentinel, not a tube
            if p.distance_squared(q) <= SK_ROTATE_GUARD_NEAR:
                return True
        return False

    def _guard_seat(self, site):
        """The screen/babysit seat for `site` -- its cardinal neighbour toward
        the enemy core.  (v630's `_guard_seat`, name and body unchanged.)

        Pure geometry off `self.enemy` (set at boot from map symmetry, refined
        on sight): zero engine calls, never stale, and works when `nest_face`
        is diagonal or already cleared.  Returns None -- callers fall back to
        the un-guarded walk -- when there is no enemy fix, no cardinal step, or
        the seat is off-map.

        ⭐ WHY THIS TILE IS BOTH THINGS AT ONCE, and it is a design fact of the
        engine rather than a coincidence: a builder bot may only build on an
        ORTHOGONALLY ADJACENT tile, so standing here is the only way to plant
        the tube on `site` while facing the enemy -- and the tile a body must
        occupy to plant toward the enemy IS the tile between the tube and the
        enemy's guns.  The screen and the plant seat are the same square.
        """
        if site is None or self.enemy is None:
            return None
        try:
            d = site.cardinal_direction_to(self.enemy)
        except Exception:
            return None
        if d is None or not d.is_cardinal():
            return None
        q = site.add(d)
        if not self.ibp(q):
            return None
        return q

    def _guard_heal(self, ct, p, rnd):
        """PLANK 10 rung (b): the band-scoped heal, with the counter.

        `_heal_action` is the existing verb (1 Ti -> +4 HP on the most-damaged
        adjacent friendly building, most-damaged-first).  With SK_ROTATE_PREPS
        = 0 there are no prep barriers post-flip, so the most-damaged adjacent
        friendly building is naturally the SENTINEL -- the right priority
        emerges from the verb we already ship, with no new targeting code.

        ⛔ THE COOLDOWN TEST IS EXPLICIT HERE and not left to `_heal_action`:
        `ct.heal` is cooldown-gated and `can_heal` is the only guard inside the
        verb, so a rung that fires on a non-zero cooldown burns the turn's
        `return` for nothing.  v630 got this by placement (its callers already
        sat under a cooldown-0 test); the hold-branch caller here does not, so
        the test moves into the rung.
        """
        if not (self.rot_body and SK_ROTATE_GUARD):
            return False
        try:
            if ct.get_action_cooldown() != 0:
                return False
        except Exception:
            return False
        if not self._near_live_tube(ct, p):
            return False
        if not self._heal_action(ct, p, rnd):
            return False
        self.guard_heals += 1
        return True

    def _guard_walk(self, ct, p, target):
        """PLANK 10 rungs (a) + (c): walk to / stand on `target`'s front seat.

        Returns True when this rung consumed the turn (standing on station, or
        a step taken toward the seat), False when the caller must fall through
        to its own un-guarded walk.  ⛔ A BIAS, NEVER A REFUSAL STATE: no enemy
        fix, no cardinal step, off-map seat or an unreachable seat all return
        False and the caller's original `step_to` runs unchanged.
        """
        if not (self.rot_body and SK_ROTATE_GUARD) or target is None:
            return False
        if p.distance_squared(target) > SK_ROTATE_GUARD_NEAR:
            return False                       # v630.1: TERMINAL APPROACH ONLY
        seat = self._guard_seat(target)
        if seat is None:
            return False
        if p.x == seat.x and p.y == seat.y:
            self.guard_seats += 1              # on station: STAND (the screen)
            return True
        return self.step_to(ct, seat)

    def _on_eligible_ore(self, ct, p, rnd):
        """v632 SK_ORE_STEPOFF: is this body STANDING ON an unbuilt home-ore
        tile the ore walk would target?  Mirrors the ore loop's own filters so
        the step-off fires exactly when the deadlock would (#129 attribution:
        icefloe 475 frozen rounds, skald 33)."""
        xy = (p.x, p.y)
        try:
            if ct.get_tile_env(p) != Environment.ORE_TITANIUM:
                return False
        except Exception:
            return False
        # ⭐⭐ s57 SK_DOC_ECO_PUSH (a): this predicate MIRRORS the ore walk's
        # filters by construction (that is what makes the step-off fire
        # exactly when the deadlock would), so the widened fence has to be
        # mirrored here too or the guard goes blind on a widened tile.
        if xy in self.harv_tiles or not self._doc_ore_ok(p):
            return False
        if self.belt_plan.get(xy) is not None:
            return False
        if self._harv_blocked(ct, xy, rnd):
            return False
        return True

    # ------------------------------------------------------------------
    # v632 PLANK A -- THE WALK-TERMINAL ESCAPE  (SK_WALK_GUARDS, #130)
    # ------------------------------------------------------------------

    def _wg_banned(self, site, x, y, rnd):
        """4.2: is (site, tile) off THIS walk's target list right now?

        Read pattern mirrored verbatim from the tree's existing bans
        (`escape_ban.get(xy, -1) > rnd`, `sk_roles.py:2353/:2927/:3922`).
        Callers guard with `if self.wg_ban and ...` so an OFF arm -- where the
        dict is empty because only `_walk_escape` ever writes it, and
        `_walk_escape` is reachable only under SK_WALK_GUARDS -- pays one
        truthiness test and no dict lookup in the ore patrol's hot loop.
        """
        return self.wg_ban.get((site, x, y), -1) > rnd

    def _walk_escape(self, ct, p, rnd, site):
        """Step off the tile this body is standing on and targeting, and take
        that tile off THIS walk's target list for SK_WALK_GUARD_BAN rounds.

        GAME CONTEXT: an in-engine cardinal move by one of our own builder bots
        in the Florent Code League's simulated grid.

        ⛔ THE ENGINE FACT THIS ANSWERS.  A builder bot cannot build on, attack
        or heal ITS OWN TILE (orthogonal adjacency only), and `_bfs_direction`
        answers CENTRE when the goal is underfoot (`sk_common.py:987-988`), so
        `_nav` returns False without moving.  A walk at a STANDABLE act-target
        therefore has a terminal state with no legal act and no motion, and the
        only thing that breaks it is a re-plan.  One cardinal step restores the
        legal act stance: next round the target is orthogonally adjacent.

        THE SHAPE IS NOT NEW -- it is the v601 belt guard and the v632
        SK_ORE_STEPOFF guard (`_home_keeper_move`), the two sites the research
        audit reads as the positive controls, factored so the three remaining
        exposed sites get exactly the same verb rather than three copies.

        ⚠ ONE DELIBERATE DIVERGENCE FROM THOSE TWO, and it is in the strict
        direction: they call `step_to` on the FIRST passable neighbour and
        return regardless of the verdict.  This tries the next neighbour when a
        step does not execute, and returns the verdict -- so the caller's
        counter records a MOVE THAT HAPPENED rather than an attempt, and a
        guard that has never actually moved a body reads zero instead of
        reading like a success.

        ⭐⭐ 4.2 -- THE BAN IS WHAT MAKES THIS TERMINATE, and it is written
        HERE, on the executed step, so the escape and its ban can never come
        apart.  Without it the guard converts a freeze into a two-tile
        oscillation (the midgard_seatA wire trace in SK_WALK_GUARD_BAN's note):
        the body steps off, the walk re-picks the same tile, and it steps back
        on for as long as the state lasts.  ⛔ ONLY AN EXECUTED STEP BANS -- a
        refused escape has not moved the body, so banning there would blind the
        walk to a tile it is still standing on.

        Returns True iff a move was executed.
        """
        for d in CARDINALS:
            q = p.add(d)
            if not self.ibp(q):
                continue
            try:
                if not ct.is_tile_passable(q):
                    continue
            except Exception:
                continue
            if self.step_to(ct, q):
                self.wg_ban[(site, p.x, p.y)] = rnd + SK_WALK_GUARD_BAN
                return True
        return False

    # ------------------------------------------------------------------
    # v632 PLANK B -- THE LEASHED KEEPER'S DUTY  (SK_LEASH_DUTY)
    # ------------------------------------------------------------------

    def _leash_duty_seat(self, ct, p):
        """The core-adjacent tile a LEASHED, TARGETLESS keeper should hold.

        Returns `p` itself when this body is already orthogonally adjacent to
        our own core footprint -- which is how the caller learns to HOLD
        STATION rather than take another step -- else the nearest free
        core-ring tile, else None.

        ⛔ SAME SELECTION AS `_medic_seat`, MINUS ITS ARMING GATES, and that is
        the whole point: `_medic_seat` fires only while `corefire_fresh` says
        the core is ACTUALLY LOSING HP, but the leash binds on the much wider
        slot-1 threat latch (`_under_attack`, 50-round TTL).  The window this
        duty covers is exactly the difference between those two -- threat
        latched, core not currently taking damage, every economy target refused
        by the leash.  `SK_MEDIC_SEAT_DSQ` is deliberately NOT applied: this is
        the fall-through, so there is no competing duty for a distance fence to
        protect, and refusing a far seat here would put the body back in the
        state this plank exists to remove.
        """
        if self.core is None:
            return None
        if adjacent_to_core(p, self.core):
            return p
        best = None
        for q in core_ring(self.core):
            if not self.ibp(q):
                continue
            try:
                if not ct.is_tile_passable(q):
                    continue
                if ct.get_tile_builder_bot_id(q) is not None:
                    continue        # one body per seat; another takes the next
            except Exception:
                continue
            d = p.distance_squared(q)
            if best is None or d < best[0]:
                best = (d, q)
        return None if best is None else best[1]

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
        if not ((SK_TUBE_FLOOR2 or SK_TUBE_LATENCY_SOLO)
                and SK_TUBE_FLOOR2_PREPREP):
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
        # ⭐ s57 ARM 2 (a): the CONFIRMED-ALIVE stamp starts at the plant --
        # the one round this body is certain the barrel stands.  The TTL runs
        # from here, so a barrel planted and walked away from is credited for
        # one commute and no longer.  ⛔ SEPARATE DICT, NOT A FOURTH TUPLE
        # FIELD: every consumer in this file unpacks `tid, site, born = t`, and
        # widening the ledger tuple would be a change to code this arm has no
        # mandate to touch.
        # ⭐ s57 ARM 2 (b): a plant ENDS the funding hold, whatever it was.
        if SK_BATTERY2:
            if SK_BATTERY2_LEDGER:
                self.batt2_seen[tid] = rnd
            self.batt2_hold_since = None
        # ⭐ s57 BARRELS ARM 2, INSTRUMENT (3) -- THE PLANT'S FACING CLASS.
        # Magnus's diagonal question, answered by column: a sentinel's line is
        # single-tile-wide and may be axial or exactly diagonal
        # (`_firing_face`), and the two classes are not obviously equal in
        # survival.  ⛔ NO ENGINE CALL, NO DECISION -- `is_cardinal()` is pure
        # Python on a Direction -- so the tape is unchanged and this runs on
        # BOTH arms.
        if SK_BG_FACE_STAT:
            try:
                _card = bool(face.is_cardinal())
            except Exception:
                _card = None
            if _card is not None:
                self.bg_face[(site.x, site.y)] = _card
                if _card:
                    self.bg_plant_card += 1
                else:
                    self.bg_plant_diag += 1
        # ⭐ v632 PLANKS 8+9 -- THE PHASE PLANT COUNTER.  It drives the FIRST
        # battery's clustering in `_pick_nest` ("put the first 4 sentinels
        # together ... then move to the next position") and it is the arm's
        # plant-rate instrument (§8b names plant rate as the binding
        # constraint).  Counted at the SUCCESSFUL build, so a refused or
        # unaffordable site never advances it.
        if self.rot_body:
            self.rot_plants += 1
        # ⛔⛔ s57 VOLUME ARM 1, PIECE (a) -- THE TRAILER PLANTS BUT DOES NOT
        # PUBLISH.  `_nest_publish` writes slot 7's ENGINEER fields (b10-20,
        # b21); a second writer of a buffered slot is a SILENT LOST UPDATE
        # (measured at 291 frozen rounds on the tube beat), so the column body
        # takes the plant and leaves the word alone.  ⛔ WHAT IS LOST IS
        # NOTHING LIVE: those fields' only reader is `_s2_pending`, whose FIRST
        # LINE is `if not SK_S2_PRIORITY: return False`, and that flag ships
        # False.  ⛔ THE TUBE ITSELF STILL PUBLISHES: under SK_TEAM_TUBES the
        # forward sentinel writes its OWN phase-separated beat into b0-9 /
        # b22-31 from `_turret`, which is what `_floor_live` counts -- so a
        # trailer-planted tube is visible team-wide exactly like any other.
        # ⛔ CALL-SITE CONJUNCTION: SK_VOLUME False -> the conjunction is False
        # -> this publishes as today, character for character.
        if not (SK_VOLUME and SK_VH_COLUMN and self.role == SK_VH_ROLE):
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
        # v632 PLANKS 8+9: the SAME substitution as the turn head.  The two must
        # agree or the same-round re-arm would stop one plant short of the
        # battery.
        if self.rot_body:
            want = SK_ROTATE_WANT
        n = self._floor_live(ct, rnd)
        # s57 ARM 2 (a): the post-plant re-arm reads the SAME count as the turn
        # head.  The two must agree or the same-round re-arm would free a site
        # the turn head thinks is still wanted.
        n = self._b2_live(ct, rnd, n)
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
        # ⛔⛔ v632 PLANKS 8+9, HAZARD (a) -- THE SLOT-7 WRITER COLLISION, AND
        # THIS IS THE FIX THAT SHIPPED.  Study §8a hazard 1 offers two: (a) gate
        # this method on the body's ORIGINAL role, (b) flip SK_NEST_N3 = True,
        # which sets SK_TUBE_ENG_SLOT7 = False and removes the engineer from
        # slot 7 altogether.  The study prefers (b).  ⭐ (b) IS NOT AVAILABLE
        # HERE AND THE REASON IS THE WELD RULE, NOT TASTE: SK_NEST_N3 is a
        # module constant with NO phase term -- flipping it also re-lays slot 7,
        # raises SK_NEST_PAIR_N 2 -> 3 and changes the tube target from ROUND
        # ZERO, i.e. it changes PRE-flip behaviour and welds a second, already
        # REFUTED axis (-1.22pp game share, n=1800/side, `sk_maps.py` SK_NEST_N3)
        # onto this master.  The arm would then measure flip+battery+N3 and be
        # unable to say which moved.  (a) is a strict correctness gate with an
        # exact OFF identity, so (a) it is.
        # ⛔ WHY IT IS AN EXACT IDENTITY: every call path into this method comes
        # from `_siege_engineer`, which the dispatch reaches only for
        # `self.role == SK_SIEGE_ENGINEER` on any SK_ROTATE-off arm.  The gate
        # therefore never refuses there, and `rot_pub_blocked` == 0 is the
        # witness.  ⭐ IT IS ALSO THE INSTRUMENT: the failure it prevents is
        # SILENT (a lost buffered write leaves no trace and no exception), so a
        # gate that has never been seen to refuse has not been seen to work.
        if self.role != SK_SIEGE_ENGINEER:
            self.rot_pub_blocked += 1
            return
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
        # ⭐⭐ s57 ARM 2 (a) READS THE SAME PRODUCER UNDER ITS OWN MASTER.  It
        # is a SECOND read rather than a widened condition on the first because
        # SK_TUBE_RELIGHT ships False, so the v619 arbiter above is dead code in
        # this config and re-arming it would ship two planks under one flag.
        # One extra `read_store` per engineer round while the master is on;
        # nothing at all while it is off.
        b2beats = None
        if (SK_BATTERY2 and SK_BATTERY2_LEDGER
                and SK_TEAM_TUBES and SK_NEST_PAIR):
            try:
                b2beats = self._tube_count(ct.read_store(SK_SLOT_NEST), rnd)
            except Exception:
                b2beats = None
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
            # ⭐⭐ s57 ARM 2 (a) -- THE LEDGER FIX ITSELF, AT ITS SOURCE.  The
            # arm-1 trace measured 204 of 222 plants happening at ledger-live
            # 0 while the wire showed the barrels standing: the ledger is not a
            # census of our tubes, it is a census of the tubes THIS BODY CAN
            # SEE.  `_b2_phantom` carries the three conditions and is a no-op
            # on every master-off arm.
            if raised and self._b2_phantom(ct, rnd, tid, site, ledger, b2beats):
                self.batt2_phantom += 1
                continue
            if alive:
                # the CONFIRMED sighting: this is the only place the TTL clock
                # is refreshed, so a credit can never outlive a real read.
                if SK_BATTERY2 and SK_BATTERY2_LEDGER:
                    self.batt2_seen[tid] = rnd
                continue
            self.nest_deaths[(site.x, site.y)] = rnd        # V4
            self.nest_lives.append(rnd - born)
            # ⭐⭐ s57 BARRELS ARM 2, PIECE (c) -- THE KILLER-COVERAGE BAN, at
            # the one place in the tree that knows a tube has just gone down.
            # No-op on every master-off arm (first line of the callee).
            self._bg_killer_ban(ct, site, rnd)
            # ⭐ s57 BARRELS ARM 2, INSTRUMENT (3) -- TUBE LIFE BY FACING CLASS.
            # ⛔ NO LOGIC AND NO ENGINE CALL: a dict pop and two adds, so it is
            # inert on the tape and runs on BOTH arms (an OFF arm with no column
            # is half a comparison).  ⚠ UNCENSORED ONLY -- a tube still standing
            # at the end contributes no life, the same convention the banked
            # `life_med_uncens` uses.
            if SK_BG_FACE_STAT:
                _c = self.bg_face.pop((site.x, site.y), None)
                if _c is True:
                    self.bg_life_card += rnd - born
                    self.bg_life_card_n += 1
                elif _c is False:
                    self.bg_life_diag += rnd - born
                    self.bg_life_diag_n += 1
            if SK_BATTERY2 and SK_BATTERY2_LEDGER:
                self.batt2_seen.pop(tid, None)
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

        ⛔⛔ v632 PLANKS 8+9, HAZARD (a) EXTENDED -- SLOT 8 IS THE SAME DEFECT AS
        SLOT 7 AND THE STUDY DOES NOT NAME IT.  §8a hazard 1 names slot 7; the
        transitive wstore audit from `_siege_engineer` (the same AST-reachability
        audit plank 5 ran from `_home_keeper`) returns THREE rungs, not one:
            slot 7  SK_SLOT_NEST   `_nest_publish`  -> gated
            slot 8  SK_SLOT_DRIP   `_drip_report`   -> gated (here)
            slot 12 SK_SLOT_STALL  `_stall_check`   -> gated
        And slot 8 is WORSE than slot 7, because this write is a plain
        OVERWRITE rather than a read-modify-write on a disjoint field: two
        raider bodies would each publish the tube census THEY can see and the
        loser's word is dropped whole, every round.
        ⚠ DISCLOSED COST OF GATING RATHER THAN MERGING: the surviving writer is
        the ORIGINAL engineer, which counts only the tubes inside ITS vision
        (r^2 = 20), so the other raider's tubes are under-reported and the
        core's ammo `need` reads LOW.  Three reasons that is the right failure
        direction: (1) the first battery is CLUSTERED by
        SK_ROTATE_CLUSTER_GAP, so both raiders and the whole battery sit inside
        one vision disc for most of the phase; (2) `_turret` refuses to fire
        below its shot price (`:8098-8101`), so an ammo shortfall costs SHOTS
        and never a unit -- `can_fire` returns True at 0 ammo and firing would
        RAISE, which destroys our own turret, and that is the hazard this
        refusal already closes; (3) the drip re-evaluates every round and never
        banks.  A merged two-writer census needs a slot re-lay and is a separate
        plank.
        """
        if self.role != SK_SIEGE_ENGINEER:
            self.rot_pub_blocked += 1
            return
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
        word = ((min(guns, 63) & DRIP_GUN_MASK)
                | ((min(sents, 63) & DRIP_GUN_MASK) << DRIP_SENT_FIELD))
        # ⭐⭐ s57 SK_HAMMER_PRIO -- THE CHANNEL, AND THIS IS THE WHOLE
        # PUBLISHER.  b12 carries the ADOPTED battery's own eco-ready latch
        # (`batt2_eco_since`, set by `_b2_eco_ready`) to the bodies that cannot
        # see it: module state is not shared between units (one sub-interpreter
        # each, `main.py:653`), the eco-expansion rungs run on the KEEPER and
        # the latch lives on the ENGINEER.  ⛔ NOTHING IS RECOMPUTED HERE -- no
        # bar, no ring, no warm-up; the bit is the latch's own state read off
        # `self`, which is what keeps this out of class-audit row #132.
        # ⛔ WHY IT CANNOT DISTURB THE DRIP: this write is a plain OVERWRITE by
        # ONE role from ONE method, and all three readers of slot 8
        # (`sk_core.py:327-329`, `:434-438`, `:526`) mask their own 6-bit field,
        # so b12 is invisible to every one of them.  With the master off the
        # word is bit-for-bit what it is today.
        # ⚠ THE LAG IS STRUCTURAL AND DISCLOSED.  V1: this method ran at the
        # TOP of the engineer's turn while `_b2_eco_ready` was evaluated later
        # in the same turn (inside `_battery_open`), and the store is buffered
        # one round -- so a reader saw the latch up to TWO rounds late.  V2
        # evaluates readiness ABOVE this method (`_hammer_eco_eval`), so the
        # bit is published the round it fires and the remaining lag is the
        # store's own ONE buffered round.  Late is still the safe direction for
        # a gate that must never touch the opening.
        if SK_HAMMER_PRIO and self.batt2_eco_since is not None:
            word |= HAMMER_LATCH_BIT
            self.hammer_pub += 1
        self.wstore(ct, SK_SLOT_DRIP, word)

    def _stall_check(self, ct, rnd):
        """LEDGER V9 -- a plan B.  If the seal has not advanced in
        SK_STALL_ROUNDS rounds AND forward turret lifetime is below
        SK_STALL_LIFETIME, flip the doctrine branch: the nest shifts to the
        band's FAR quadrant and the walker re-routes (it reads this bit).
        391 rounds of the same four jobs, and 14 forward turrets fed to an
        adjacent-answering opponent at a median age of 7, is the measured
        alternative.

        ⛔ v632 PLANKS 8+9, HAZARD (a) EXTENDED -- slot 12 is the third rung of
        the `_siege_engineer` wstore audit (see `_drip_report`), gated on the
        original role for the same one-writer reason.
        """
        if self.role != SK_SIEGE_ENGINEER:
            self.rot_pub_blocked += 1
            return
        cage = ct.read_store(SK_SLOT_CAGE)
        adv = (cage >> CAGE_BEAT_FIELD) & SK_BEAT_MASK
        lives = self.nest_lives
        mean_life = (sum(lives) // len(lives)) if lives else 99
        stalled = (adv != 0 and rnd - (adv - 1) > SK_STALL_ROUNDS
                   and mean_life < SK_STALL_LIFETIME)
        # ⛔ v632 PLANKS 8+9 -- A WRITER THAT LEFT IS NOT A STALL.  `adv` is the
        # CAGE WALKER's seal-advance beat (slot 6, `_cage_report`), and at the
        # flip the walker stops running `_cage_walker` for the rest of the game
        # -- so `adv` freezes and `rnd - (adv - 1)` crosses SK_STALL_ROUNDS for
        # a reason that has nothing to do with a stalled seal.  The latch's
        # effect (`nest_site = None`, one forced re-site into the far quadrant)
        # would be a pure loss during the battery.  There IS no seal post-flip,
        # so the detector's input is undefined and the honest answer is False.
        # An ALREADY-LATCHED stall from phase 1 is left standing: that one was
        # measured on a live writer.
        if self.rot_on:
            stalled = False
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
        # ⭐ v632 PLANK A, SITE 3 of 3 (SK_WALK_GUARDS) -- THE THREAT-SLOT
        # FREEZE.  Audit `AUDIT-walk-terminals-2026-08-22.md` row 30, EXPOSED,
        # inherited from `_v628compose`.  SK_SLOT_THREAT_POS is a POSITION the
        # CORE published when it last saw an enemy body, turret or barrier
        # there, and the slot IS NEVER CLEARED (`_threat_scan` says so in those
        # words) -- so once that enemy walks away or its structure is removed,
        # the tile is EMPTY, STANDABLE, and this body walks onto its own
        # target.  Every tile-content test in this method lives inside the
        # `manhattan == 1` branch; at manhattan 0 nothing runs, `step_to`
        # answers CENTRE, and `return True` CONSUMES THE TURN UNCONDITIONALLY,
        # so no lower authority ever gets it.  Bounded <= 50 rounds by the
        # slot-1 latch TTL (`_under_attack` = `beat_fresh(..., 50)`), but the
        # same freeze class for every round inside that window, repeatable for
        # as long as the core keeps re-latching.
        # ⛔ THE GUARD IS THE ESCAPE ONLY.  `return True` on the no-escape path
        # is LEFT EXACTLY AS IT WAS -- yielding the turn there would be a
        # second, unregistered behaviour change on a survival rung.
        if (SK_WALK_GUARDS and threat.x == p.x and threat.y == p.y):
            self.wg_state_def += 1
            if self._walk_escape(ct, p, rnd, WG_SITE_DEF):
                self.wg_fire_def += 1
                return True
        # ⭐⭐ 4.2 -- THE BAN EXCLUSION, SITE 3, AND IT IS A DECLINE BECAUSE
        # THIS WALK HAS EXACTLY ONE TARGET.  The other two walks re-target
        # (next-nearest ore, next ladder rung); here the target IS slot 2, so
        # taking it off the list means yielding the turn -- and that is
        # precisely what the audit says is missing: `return True` consumes the
        # turn unconditionally, "so no lower authority ever gets it".
        # ⛔ PLACED BELOW THE `manhattan == 1` FIRE BRANCH ON PURPOSE.  The ban
        # vetoes the WALK ONLY.  If something real is planted on that square
        # while this body stands beside it, the melee above still answers it at
        # full priority -- the ban never suppresses the shot, only the march at
        # a tile this body has already proved is empty by standing on it.
        if self.wg_ban and self._wg_banned(WG_SITE_DEF, threat.x, threat.y,
                                           rnd):
            return False
        self.step_to(ct, threat)
        return True

    # ==================================================================
    # v632 HEIMDALL PLANK 1 -- THE CITADEL DISPATCH (SK_CITADEL)
    # ==================================================================

    def _citadel_answer(self, ct, p, rnd):
        """Every admitted body answers an intruder inside Chebyshev 3 of our
        core.  True iff it consumed this body's turn.

        GAME CONTEXT: an in-engine response to a competing bot's pieces on the
        simulated grid; "intruder" is an enemy unit inside our own core annulus.

        DOCTRINE: PROGRAMME.md's CITADEL block ("i want every single raider
        destroyed that 3 squares from our core") under the FORTRESS block ("all
        builders are to destroy them"), Magnus s57 2026-08-22.  Design study
        §2c.  ⛔ WHAT THIS PLANK IS *NOT*: it buys nothing.  `CITADEL_WEAPON:
        turret_ring` is PLANK 3; plank 1 is DISPATCH ONLY -- zero scale cost,
        zero titanium, no new sensor.

        ⛔⛔ THE ACTION LADDER IS SHAPED BY AN ENGINE FACT, NOT A PREFERENCE.
        A builder CANNOT attack an enemy builder bot -- re-proven tonight,
        `scratchpad/s57_heim0/bvb_probe4.log`: `can_fire` False 990/990 and an
        ungated `fire()` raised GameError 990/990.  So:
          * enemy BUILDING on the tile -> `_clear_tile`, the tree's complete,
            guarded chew verb (healing-race veto, per-tile give-up, V7 trend).
          * enemy BODY on the tile -> there is no damage verb.  What is left is
            TILE DENIAL: hold the ground next to it so the tiles it wants are
            not free.  A turret would end the episode; we ship none here, and
            the `_gun_bears` rung below is written so PLANK 3 arms it rather
            than having to re-open this function.

        ⛔ THE OCCUPANT IS RE-READ AT ACT TIME, NEVER AT LATCH TIME.  That is
        `SK_MARCH_TEAMCHECK`'s rule (`sk_maps.py:1092`, the v612 fix for 23
        pecks landed on our OWN conveyor) and it is doubly required here: slot 2
        is a POSITION the core published when it last saw an enemy there, the
        write is buffered a round, and the slot is NEVER CLEARED -- so by the
        time this body arrives our own relay may own the tile.

        DISENGAGE -- three independent conditions, each mirroring a pattern
        already in the tree, because an engagement with no exit is how a body
        becomes a paperweight:
          (a) the re-read shows no enemy on the tile;
          (b) `rnd - since > SK_CITADEL_GIVEUP` (`_clear_tile:5124`'s clock);
          (c) the target has left the Chebyshev zone.
        On every one of them this returns False, which does NOT idle the body:
        the caller falls straight through to the role's own turn.
        """
        if self.core is None:
            return False
        # ⭐⭐ v632 PLANK 1.1 -- THE KEEPER YIELDS TO THE MEDIC DUTY.  The p14
        # composite screen measured plank 1.0's exact defect: this dispatch
        # sits ABOVE the keeper's whole action ladder, so with a threat
        # latched the keeper chews zone structures while its own core bleeds
        # -- the five carrying F1 cells (icefloe_seatB, holmgang_seatA,
        # glacierkeep_seatB, skald_seatA, stavkirke_seatA -- the SAME set as
        # the v630 attribution) fell to 0-9 core heals WITH THE LEASH ON,
        # because the leash brings the body home and the dispatch then spends
        # its turn anyway.  While the corefire latch is fresh (the core's own
        # HP delta, cannot be out of vision), the KEEPER falls through to its
        # normal turn -- whose ladder heals -- and the denier/walker still
        # answer the zone.  Magnus's ladder is respected: destroying raiders
        # is p1, but a dead core loses before any priority pays.
        if self.role == SK_HOME_KEEPER and self.corefire_fresh(ct, rnd):
            self.citadel_tgt = None
            return False
        try:
            threat = unpack_pos(ct.read_store(SK_SLOT_THREAT_POS))
        except Exception:
            return False
        if threat is None or not self.ibp(threat):
            return False
        # (c) THE ZONE.  `cheb_core` is `dist_core`'s footprint clamp, so this
        # is board distance to the 2x2 footprint -- Magnus's "3 squares"
        # exactly.  Everything the core publishes is already inside its own
        # vision and inside `_threat_scan`'s d^2 <= 39 fence (study §0.3), so
        # this rejects, it never has to sense.
        if cheb_core(threat, self.core) > SK_CITADEL_CHEB:
            self.citadel_tgt = None
            return False
        # STAFFING, and it spends NO comms bit.  All 16 slots are allocated
        # (slot 15 was "THE LAST FREE SLOT"), so the converge rule is a STATIC
        # role priority: the first SK_CITADEL_BODIES roles of SK_CITADEL_ROLES
        # -- today's `SK_PECK_FOCUS` keeper+denier pair -- are admitted
        # unconditionally, and any role beyond that is a DISTANCE-FENCED
        # volunteer.  Deterministic, and every body computes the same answer
        # without agreeing on anything.  ⛔ The SIEGE ENGINEER is not in the
        # tuple at all: it is the body the r300 siege phase needs standing.
        if self.role not in SK_CITADEL_ROLES[:SK_CITADEL_BODIES]:
            if p.distance_squared(threat) > SK_CITADEL_JOIN_DSQ:
                return False
        # (b) THE PER-BODY ENGAGEMENT CLOCK, latched on the TARGET TILE.
        key = (threat.x, threat.y)
        if self.citadel_tgt != key:
            self.citadel_tgt = key
            self.citadel_since = rnd
        elif rnd - self.citadel_since > SK_CITADEL_GIVEUP:
            return False
        # --- OCCUPANT RE-READ (the SK_MARCH_TEAMCHECK rule) ----------------
        bid = None
        try:
            bid = ct.get_tile_building_id(threat)
        except Exception:
            bid = None
        if bid is not None:
            own = None
            try:
                own = ct.get_team(bid)
            except Exception:
                own = None
            if own is not None and own != self.team:
                # AN ENEMY BUILDING -- launchers, barriers, everything (his
                # enumeration).  `_clear_tile` owns the arithmetic and may
                # decline (healing race, its own give-up, V7); declining hands
                # the turn back to the role, which is the correct outcome.
                return self._clear_tile(ct, threat, rnd)
            # (a) OUR OWN building stands there: the published tile is stale.
            self.citadel_tgt = None
            return False
        bot = None
        try:
            bot = ct.get_tile_builder_bot_id(threat)
        except Exception:
            bot = None
        if bot is None:
            self.citadel_tgt = None         # (a) nothing there any more
            return False
        try:
            if ct.get_team(bot) == self.team:
                self.citadel_tgt = None     # (a) our own body walked onto it
                return False
        except Exception:
            self.citadel_tgt = None
            return False
        # --- AN ENEMY BODY.  TILE DENIAL, NOT DAMAGE (see the header) ------
        # PLANK 3's HOOK, WRITTEN NOW AND UNREACHABLE TODAY.  If one of our
        # turrets already BEARS on the tile, standing there adds nothing and
        # the body is worth more on its own job -- `_gun_bears` is the strict
        # can_fire_from test that feeds every other veto in this tree.  Plank 1
        # ships zero turrets, so `vis_friend` holds none and this never fires;
        # the ring that makes it fire is plank 3.
        if self._gun_bears(ct, threat):
            self.citadel_tgt = None
            return False
        if abs(threat.x - p.x) + abs(threat.y - p.y) == 1:
            # ADJACENT: HOLD.  Bodies cannot stack, so the tiles this body
            # occupies are tiles the intruder cannot take -- that is the whole
            # verb, and its effect must be MEASURED (intruder displacement /
            # actions denied), never assumed (study §7 R6).
            # ⭐ R6, AND IT IS THE REASON THIS RUNG EXISTS: "hold" with a zero
            # action cooldown is a terminal-idle state wearing a doctrine's
            # uniform.  If an enemy BUILDING is orthogonally adjacent, the free
            # action goes into it first -- same verb, same guards, no extra
            # spend.  `skip_core` keeps our own footprint off the ladder.
            self.citadel_blocks += 1
            if ct.get_action_cooldown() == 0:
                self._peck_priority(ct, p, rnd, skip_core=True)
            return True
        # NOT ADJACENT: close on it.  A failed step returns False rather than
        # burning the turn -- the role's own turn (and `SK_IDLE_ACT_ALL` at the
        # bottom of it) is strictly better than standing still, and the clock
        # keeps running so the give-up still lands.
        if self.step_to(ct, threat):
            self.citadel_walks += 1
            return True
        return False

    # ==================================================================
    # v632 HEIMDALL PLANK 2 -- THE DEMOLITION SWEEP (SK_DEMOLISH)
    # ==================================================================

    def _demolish_pri(self, et, q):
        """The sweep's OWN class ordering, highest first.

        GAME CONTEXT: `et` is a competing bot's structure planted inside our
        half of the simulated grid; the ordering decides which one our builder
        chews first.

        ⛔⛔ THIS DELIBERATELY DOES NOT REUSE `_target_pri`, AND THE REASON IS
        THE CURRENCY (study §3b).  `_target_pri` scores SK_PRI_TURRET = 4 for
        all three armed types (so a launcher and a gunner are indistinguishable
        to it) and SK_PRI_BARRIER = 0, and `_peck_priority` refuses anything
        <= SK_PRI_OTHER -- i.e. it cannot express this plank's order and would
        VETO two of its six classes outright.  That barrier-0 is not a defect:
        it exists because 1,280 of 1,712 pecks went into barriers under the
        KILL currency.  Under the r300 fortress ruling the demolition of a
        planted structure in OUR half is not a detour from the kill, it is the
        job (PROGRAMME `FORTRESS_DEMOLITION`), so the sweep needs its own scale
        and `_target_pri` keeps its.

        THE ORDER, with the study's reasoning:
          LAUNCHER  -- first, and NOT by HP.  It is a 30 HP building that
                       cannot defend itself (15 pecks), its removal frees every
                       seat it covers, and it is the ONLY enemy structure that
                       can move OUR bodies (`can_launch` has no team check).
          SENTINEL  -- 40 HP, r^2=32, ignores obstacles: the structure the
                       prediction study measures behind first core damage.
          GUNNER    -- 25 HP, r^2=13, the same class one tier cheaper.
          SEAT BARRIER -- a barrier standing on one of our eight DELIVERY SEATS
                       is the tile between a harvester and the core; 180 of the
                       220 enemy barriers standing at end of game sit on one.
          BELT      -- their conveyor/splitter: the belt-prank acceptor that
                       drinks our harvester output (round-robin is team-blind).
          BARRIER   -- a plain barrier anywhere else in the fence.
        Anything else in the fence (e.g. a harvester they planted on our ore)
        still scores 1 -- "everything", per the directive -- but never outranks
        a named class.  Their CORE is excluded by the caller.
        """
        if et == EntityType.LAUNCHER:
            return 6
        if et == EntityType.SENTINEL:
            return 5
        if et == EntityType.GUNNER:
            return 4
        if et == EntityType.BARRIER:
            # The delivery-seat set is a pure function of our own core anchor
            # (`core_seats`, canonical order), so it is computed once per body
            # and never re-derived -- no engine call, no per-round cost.
            if self.demo_seats is None and self.core is not None:
                self.demo_seats = frozenset(core_seats(self.core))
            if self.demo_seats and (q.x, q.y) in self.demo_seats:
                return 3
            return 1
        if et in BELT_TYPES:
            return 2
        return 1

    def _demolish_budget_ok(self, xy, bid):
        """The per-(tile, occupant) episode budget -- `_seat_budget_ok`'s form.

        ⛔ KEYED ON THE OCCUPANT AS WELL AS THE TILE.  A ledger keyed on the
        tile alone concedes that tile for the rest of the game the moment they
        re-plant it (`collar_pecks`, measured glacierkeep seat A r48 -> r146).
        There is no per-game total here on purpose: the sweep's other bound is
        `_clear_tile`'s own SK_CAGE_MELEE_GIVEUP chew clock, which already stops
        a hard tile from owning a body, and a second global cap would silently
        retire the verb mid-game in exactly the games where the fence is
        fullest -- the opposite of the doctrine.
        """
        prev = self.demo_pecks.get(xy)
        if prev is not None and prev[0] == bid and prev[1] >= SK_DEMOLISH_CAP:
            return False
        return True

    def _demolish_charge(self, xy, bid):
        prev = self.demo_pecks.get(xy)
        n = prev[1] + 1 if (prev is not None and prev[0] == bid) else 1
        self.demo_pecks[xy] = (bid, n)
        self.demolishes += 1

    # ------------------------------------------------------------------
    # s57 THE SENTRY, PIECE 2 -- SK_SENTRY_FOCUS: THE COMMITMENT
    # ------------------------------------------------------------------
    # GAME CONTEXT: every verb below is the engine's documented builder attack
    # ("peck") on a competing bot's structure inside our own half of the
    # simulated grid, and the "heal" being detected is that bot's own documented
    # heal verb on its own building.  No new verb is introduced anywhere in this
    # section: it is a POLICY over `_demolish_target`'s existing pick.
    #
    # THE BANKED DEFECT (MJAUT half A): we buy 85% of our checkmates -- 17.0
    # pecks per game, SPREAD over 24 distinct targets, of which only 13
    # completed.  A 40 HP sentinel costs 20 pecks; five targets at four pecks
    # each removes nothing at all.  And on the 14.3% Mjolnir defends, its heal
    # (+4 HP for 1 Ti) beats our peck (2 dmg for 2 Ti) 4:1 -- so the OTHER half
    # of commitment is knowing when to stop.

    def _focus_banned(self, xy, bid, rnd):
        """Is this (tile, occupant) inside its heal-lock ban window?

        ⛔ BOUNDED, AND THE BOUND IS THE POINT (#132).  The evidence for a ban
        is "their medic was standing here for the last K pecks", and that
        evidence EXPIRES: the medic can be knocked out, walk away, or run the
        bank to zero.  A permanent ban would concede the tile on a fact that has
        gone stale, which is the same defect `collar_pecks` measured on
        glacierkeep (seat A r48 -> r146).  The ban self-clears here rather than
        needing a sweeper.
        """
        b = self.focus_ban.get(xy)
        if b is None or b[0] != bid:
            return False
        if rnd - b[1] >= SK_SENTRY_BAN_RNDS:
            del self.focus_ban[xy]
            return False
        return True

    def _focus_release(self, why):
        self.focus_tgt = None
        self.focus_hp = []
        self.focus_since = -1
        if why == "full":
            self.focus_full += 1
        elif why == "lock":
            self.focus_locks += 1
        elif why == "stale":
            self.focus_stales += 1
        elif why == "norole":
            self.focus_norole += 1

    def _focus_pecks(self, xy, bid):
        prev = self.demo_pecks.get(xy)
        return prev[1] if (prev is not None and prev[0] == bid) else 0

    def _focus_pick(self, rnd, act_q, act_bid, act_et, walk_q,
                    foc_q, foc_bid, foc_et, foc_adj):
        """Apply the commitment to this round's (act, walk) pair.

        THREE OUTCOMES, and only the first changes anything:
          * COMMITTED AND STILL THERE -> the engaged target REPLACES the pick.
            Adjacent, it becomes the ACT pick; not adjacent, it becomes the WALK
            pick, so the body closes on the thing it is committed to instead of
            drifting to whatever happens to be beside it.  This is the whole
            "17.0 pecks over 24 targets" fix.
          * COMMITTED AND GONE -> release.  `foc_q is None` means the target
            failed the pass's OWN filters this round: destroyed, out of the
            fence, over SK_DEMOLISH_CAP, banned, or simply out of this body's
            `get_nearby_buildings`.  ⚠ THE LAST ONE IS A REAL AMBIGUITY AND IS
            DISCLOSED: a body that walks out of vision of its target releases,
            rather than marching blind at a tile it can no longer see.  That is
            the conservative direction -- it can only ever SHORTEN a commitment,
            never extend one past the evidence.
          * NOT COMMITTED -> the pair is returned exactly as the sweep formed
            it, and engagement (if any) begins in `_demolish_action` when a peck
            actually LANDS on a turret.  ⛔ ENGAGEMENT IS NEVER DECLARED AT
            SELECTION TIME: the registered rule is "once a turret target is
            engaged (first peck landed)", and charging a commitment for a target
            `_clear_tile` then declines would commit this body to something it
            never touched.
        """
        if self.focus_tgt is None:
            return act_q, act_bid, act_et, walk_q
        xy, bid = self.focus_tgt
        if foc_q is None:
            self._focus_release("gone")
            return act_q, act_bid, act_et, walk_q
        if (self.focus_since >= 0
                and rnd - self.focus_since >= SK_SENTRY_FOCUS_RNDS):
            # THE ROUND BOUND.  See SK_SENTRY_FOCUS_RNDS: the peck bound cannot
            # close on a commitment that never lands a peck.
            self._focus_release("stale")
            return act_q, act_bid, act_et, walk_q
        if not foc_adj and self.role != SK_ORE_DENIER:
            # ⛔⛔ ONLY A BODY THAT WALKS MAY HOLD A NON-ADJACENT COMMITMENT,
            # and this line is the p11 lesson applied to piece 2.  The sweep's
            # walk branch is DENIER-ONLY (`_demolish_action`: "THE DENIER WALKS;
            # THE KEEPER NEVER DOES"), so a keeper committed to a target it is
            # not standing beside can never close the distance -- it would hold
            # the commitment forever, and because the commitment SUPPRESSES the
            # sweep's own adjacent pick it would also stop chewing the structure
            # it IS beside.  A stall dressed as a policy.  The keeper releases
            # and the sweep's ordinary pick stands.
            self._focus_release("norole")
            return act_q, act_bid, act_et, walk_q
        if self._focus_pecks(xy, bid) >= SK_SENTRY_FOCUS_MAX:
            # THE PECK BOUND.  20 pecks == 40 damage == a sentinel's whole HP
            # bar, so a target still standing after 20 is not being converted by
            # this body and the commitment is spent.  (SK_DEMOLISH_CAP is the
            # sweep's own episode budget and is a different bound with the same
            # integer; this one is ablatable on its own.)
            self._focus_release("full")
            return act_q, act_bid, act_et, walk_q
        self.focus_holds += 1
        if foc_adj:
            return foc_q, foc_bid, foc_et, walk_q
        return None, None, None, foc_q

    def _focus_after_peck(self, ct, xy, bid, armed, hp_before, rnd):
        """Called ONLY on a round a peck actually LANDED.  Opens the commitment
        on first blood, extends the heal ledger, and fires the give-up.

        THE HEAL LEDGER, and it is a MEASUREMENT of their heal rather than an
        inference about their intent: `hp_before` is this target's HP read
        immediately BEFORE each of THIS body's pecks.  Over the last K pecks we
        dealt 2*K damage (the engine's builder attack is 2, fixed), so absent
        any healing the HP must have fallen by 2*K.  If it fell by LESS THAN
        HALF of that, something is putting HP back at roughly our own rate --
        the banked ~1:1 -- and every further peck is a 4:1 trade in their
        favour.

        ⚠ DISCLOSED, AND IT ONLY EVER UNDER-FIRES: the ledger is per body, so
        damage a SECOND body of ours deals inside the window is counted as
        "fall" we did not pay for and makes the lock harder to declare.  A
        two-body chew therefore reads as healthy even when it is heal-locked.
        The opposite error -- abandoning a target we are in fact converting --
        is the one that would cost checkmates, and this construction cannot
        make it.
        """
        if not armed:
            # Not a turret: the sweep's normal spread behaviour is unchanged for
            # barriers, belts and everything else.  Commitment is a TURRET
            # policy -- the registered scope -- and the autopsy's population is
            # 19/19 sentinels.
            return
        if self.focus_tgt != (xy, bid):
            self.focus_tgt = (xy, bid)
            self.focus_hp = []
            self.focus_since = rnd
            self.focus_engagements += 1
        if hp_before is not None:
            self.focus_hp.append(hp_before)
            if len(self.focus_hp) > SK_SENTRY_HEAL_K + 1:
                del self.focus_hp[0]
        if len(self.focus_hp) < SK_SENTRY_HEAL_K + 1:
            return
        fell = self.focus_hp[0] - self.focus_hp[-1]
        dealt = 2 * SK_SENTRY_HEAL_K
        if fell * 2 < dealt:
            self.focus_ban[xy] = (bid, rnd)
            self._focus_release("lock")

    def _demolish_target(self, ct, p, rnd):
        """ONE pass over `ct.get_nearby_buildings()` -> `(act_q, walk_q)`:
        the enemy structure in our own half this body can chew THIS ROUND, and
        the one it should be WALKING toward.  Either may be None.

        The enumerator the tree has never had (study §3a/§3b).  One engine
        sweep per body per round -- the same idiom `_prep_cover` and
        `_launcher` already use -- and well inside CPU_BUDGET_US.

        ⛔⛔ REDESIGN, s57 2026-08-22 -- THE SPLIT PICK.  ITS PROVENANCE IS THE
        PLANK'S OWN Z3 FAILURE, and the v1 docstring's reasoning is printed
        below as the thing that was measured wrong.

        v1 ranked `key = (-pri, distance, x, y)` over ONE pick -- class
        STRICTLY over distance -- and argued: "A pick this body cannot reach
        this round simply produces no peck (`_clear_tile` declines on
        `can_fire`) and the role's ladder continues below it; that is cheaper
        than teaching this plank a walk."  **THAT ARGUMENT IS FALSIFIED ON THE
        TAPE** (verdict 2026-08-22T20:56:05Z, readout `e46*`, registered bars
        in `docs/research/EXPECTATION-v632heim-plank2-2026-08-22.md`):

          * **Z3 destroyed-share +0.029 / -0.025 / -0.009, SUM -0.005 against a
            registered bar of >= +0.10 -- 0 of 3 fixtures, FAIL.**
          * **chews-per-destroyed UNMOVED: 7.7 -> 8.3 (F1), 10.2 -> 10.5 (F2),
            29.4 -> 29.8 (F3).**  The sweep was not converting chews into
            removals any better than the tree already did.
          * **THE CLASS MIX MOVED AGAINST THE DECLARED PRIORITY: F1
            barrier-kill share UP while launcher share went DOWN** -- the
            inversion of the ordering this plank exists to impose.

        The mechanism those three numbers name together: the strict
        class-over-distance pick selects a FAR launcher, `_clear_tile` then
        declines it (a builder attack needs an ORTHOGONALLY ADJACENT tile), the
        rung wastes, and the pecks that do land eat whatever happens to be
        adjacent -- barriers.  "The ladder continues below it" is exactly what
        did NOT happen: the rung returned False, but the round was spent
        arriving at a target the body was never going to reach, because
        **nothing in the plank ever WALKED toward a sweep target.**

        SO THE PICK SPLITS IN TWO, over the same single pass:
          (a) **ACT pick** -- highest class among candidates ORTHOGONALLY
              ADJACENT to this body (Manhattan 1: the engine's own build/
              attack/heal adjacency).  Every member of this set is reachable by
              `_clear_tile` this round, so class ordering inside it is free:
              there is no far-launcher-beats-adjacent-barrier trap left,
              because a far launcher is not in the set.
          (b) **WALK pick** -- highest class among candidates that are NOT
              adjacent, ranked (class, then distance).  Disjoint from (a) by
              construction, so a walk step is always toward something this body
              genuinely cannot act on.  `_demolish_action` turns this into ONE
              step for the DENIER only.

        Priorities, fence, episode cap and the `_clear_tile` verb are all
        UNCHANGED -- the redesign is the reachability split and the walk, and
        nothing else.

        ⛔ The occupant id of the ACT pick (only) is stashed for
        `_demolish_action`, which charges the ledger only when a peck actually
        LANDS.  Charging at selection time would count refusals (healing race,
        V7 trend) against the episode cap and retire the tile without ever
        hitting it.  The walk pick is never charged: walking is not a peck.
        """
        self.demo_pick = None
        self.demo_pick_armed = False
        if self.core is None:
            return None, None
        try:
            ids = ct.get_nearby_buildings()
        except Exception:
            return None, None
        # ⭐ s57 THE SENTRY, PIECE 2 -- the commitment's three per-pass slots.
        # Filled inside the loop below (no second pass, no second engine call);
        # read by `_focus_pick` after it.
        foc_q = None
        foc_bid = None
        foc_et = None
        foc_adj = False
        # One fence read per pass.  The act and walk fences are separate
        # constants (see sk_maps) and are EQUAL by default, so this arm moves
        # one thing; the wider of the two admits a candidate to the pass and
        # each pick re-tests its own.
        fence = SK_DEMOLISH_DSQ
        if SK_DEMOLISH_WALK_DSQ > fence:
            fence = SK_DEMOLISH_WALK_DSQ
        act_key = None
        act_q = None
        act_bid = None
        act_et = None                 # s57: the ACT pick's class, for the
                                      # commitment's "is this a turret?" test
        walk_key = None
        walk_q = None
        for bid in ids:
            try:
                if ct.get_team(bid) == self.team:
                    continue
                et = ct.get_entity_type(bid)
                q = ct.get_position(bid)
            except Exception:
                continue
            if et == EntityType.CORE:
                # Their core is the WALKER's object (`_attack_enemy_core`) and
                # under the r300 ruling it is not this phase's business at all.
                continue
            if not self.ibp(q):
                continue
            dsq = dsq_core(q, self.core)
            if dsq > fence:
                continue
            xy = (q.x, q.y)
            if not self._demolish_budget_ok(xy, bid):
                continue
            adj = abs(q.x - p.x) + abs(q.y - p.y) == 1
            # ⭐ s57 THE SENTRY, PIECE 2 -- the BAN and the COMMITMENT read,
            # both inside the pass the sweep already makes.
            if SK_SENTRY and SK_SENTRY_FOCUS:
                if self._focus_banned(xy, bid, rnd):
                    continue
                f = self.focus_tgt
                if f is not None and f[0] == xy and f[1] == bid:
                    foc_q, foc_bid, foc_et, foc_adj = q, bid, et, adj
            pri = self._demolish_pri(et, q)
            if adj:
                # (a) ACT SET.  Orthogonally adjacent == what the engine lets a
                # builder attack.  Distance is 1 for every member, so the key
                # is class then a stable tile tie-break.
                if dsq > SK_DEMOLISH_DSQ:
                    continue
                key = (-pri, q.x, q.y)
                if act_key is None or key < act_key:
                    act_key = key
                    act_q = q
                    act_bid = bid
                    act_et = et
            else:
                # (b) WALK SET.  Class first, then distance -- the ordering v1
                # applied to the WHOLE pick now applies only where distance is
                # something the body can actually do something about.
                if dsq > SK_DEMOLISH_WALK_DSQ:
                    continue
                key = (-pri, p.distance_squared(q), q.x, q.y)
                if walk_key is None or key < walk_key:
                    walk_key = key
                    walk_q = q
        # ⭐⭐ s57 THE SENTRY, PIECE 2 -- THE COMMITMENT OVERRIDES THE PICK.
        # Placed HERE, after both picks are formed and before either is
        # published, so the sweep's class ordering, fence, episode cap and walk
        # split are all completely untouched: the commitment REPLACES the pick,
        # it does not rank inside it.  With the flag off this line is a module
        # constant and the two picks below are v632's, character for character.
        if SK_SENTRY and SK_SENTRY_FOCUS:
            act_q, act_bid, act_et, walk_q = self._focus_pick(
                rnd, act_q, act_bid, act_et, walk_q,
                foc_q, foc_bid, foc_et, foc_adj)
        if act_q is not None:
            self.demo_pick = ((act_q.x, act_q.y), act_bid)
            self.demo_pick_armed = act_et in ARMED_TYPES
        return act_q, walk_q

    def _demolish_action(self, ct, p, rnd):
        """The rung: pick, feed `_clear_tile`, charge the ledger -- and, for the
        DENIER only, spend the turn WALKING toward a target it cannot reach.
        True iff it took this body's turn.

        ⚠ DISCLOSED DEVIATION FROM THE STUDY'S SKETCH (§3b writes the call site
        as `if SK_DEMOLISH and self._demolish_target(...)`): the ledger charge
        needs the OCCUPANT ID at the moment the peck lands, and `_clear_tile`
        is not to be touched (it is shared with the cage walker, the citadel
        answer and the nest clear).  So the call-site conjunction names this
        wrapper instead of the selector.  The identity property the sketch
        exists for is unchanged and is what the grep proof checks:
        `SK_DEMOLISH and self._demolish_action` at BOTH call sites, so with the
        master False neither branch is reachable and the tree is
        character-for-character the adopted-leash baseline.

        ⭐ THE WALK BRANCH (redesign, s57).  Z3 failed with
        chews-per-destroyed UNMOVED (7.7->8.3 / 10.2->10.5 / 29.4->29.8) and
        the class mix INVERTED (F1 barrier share up, launcher down) because no
        walk toward a sweep target existed anywhere in the plank: the rung
        picked a far launcher, `_clear_tile` declined on adjacency, and the
        turn was wasted.  One step, `step_to` -- the tree's ONLY movement
        entry, which already owns the flood, the danger pricing and the
        2-cycle strike-out -- is what converts that wasted rung into approach.

        ⛔⛔ THE DENIER WALKS; THE KEEPER NEVER DOES, and that is the p11
        lesson paid for in this same session (verdict 2026-08-22T20:40:28Z:
        plank 1.1's citadel dispatch sat above the keeper's ladder and failed
        Y2 on F1 core-footprint heals 9.60 vs >= 10.6 and Y2b on death cells
        21 vs <= 18).  A keeper that WALKS OFF the core footprint to chase a
        zone structure is strictly worse than one that merely wastes a rung
        standing on it: heal-first doctrine binds, and the keeper's demolition
        half stays exactly what it was -- act-only, opportunistic, below every
        heal rung.  `self.role` is the gate because both call sites are inside
        role-dispatched methods, which keeps the call-site text unchanged.

        ⚠ SECOND DISCLOSED DEVIATION, and it is deliberate: the brief reads
        "if no adjacent act target and a walk target exists".  This walks
        whenever the ACT PATH DID NOT TAKE THE TURN -- which includes the case
        where an adjacent target existed and `_clear_tile` DECLINED it (healing
        race, chew clock, affordability, `hp_trend_ok`).  A declined adjacent
        target is the very wasted rung the redesign exists to remove, and the
        act/walk sets are disjoint by construction, so the walk can never be a
        step toward a tile the body is already standing beside.

        ⚠ NAMED INTERACTION, because v606 ITEM 4(b) is the note that warns
        about exactly this shape: the walk is a SECOND MOVEMENT AUTHORITY on
        the denier, and it sits ABOVE the `SK_CYCLE_ALL_ROLES` commit freeze
        further down the role (which exists because "freezing only the V5
        branch would leave the other authority free to keep re-picking").  The
        reason it is admitted above the freeze rather than below it: the walk
        pick is STABLE BY CONSTRUCTION -- it is ranked over a fence anchored to
        OUR OWN core, so it cannot alternate between a home target and the
        enemy core the way the deny/orbit pair measured on fimbulwinter did,
        and a step toward it only shortens the distance that ranks it.  A pick
        flip needs a HIGHER-CLASS structure to appear, which is a real change
        of object, not thrash.  `_nav`'s own FIX 3 two-cycle strike-out remains
        the backstop.  If the screen shows denier step-thrash, this ordering is
        the first thing to test, not the walk itself.
        """
        if not SK_DEMOLISH:
            return False
        act_q, walk_q = self._demolish_target(ct, p, rnd)
        # ⭐ s57 THE SENTRY, PIECE 2 -- THE HP SAMPLE, READ BEFORE THE PECK.
        # It has to be before: after `_clear_tile` fires, the 2 damage is
        # already applied and the sample would price our own hit as their
        # failure to heal.  ONE `get_hp` on a round we are about to spend
        # anyway, and only on an ARMED pick.  A read that raises leaves the
        # ledger un-extended (`None`), which delays the give-up by one peck and
        # never fires it wrongly.
        hp_before = None
        if (SK_SENTRY and SK_SENTRY_FOCUS and act_q is not None
                and self.demo_pick_armed and self.demo_pick is not None):
            try:
                hp_before = ct.get_hp(self.demo_pick[1])
            except Exception:
                hp_before = None
        if act_q is not None and self._clear_tile(ct, act_q, rnd):
            pick = self.demo_pick
            if pick is not None:
                self._demolish_charge(pick[0], pick[1])
                if SK_SENTRY and SK_SENTRY_FOCUS:
                    self._focus_after_peck(ct, pick[0], pick[1],
                                           self.demo_pick_armed, hp_before, rnd)
            return True
        if walk_q is None or self.role != SK_ORE_DENIER:
            return False
        # Cheap pre-test before the flood: `_nav` refuses on a move cooldown
        # anyway, but asking first saves a BFS on the rounds it cannot use.
        try:
            if ct.get_move_cooldown() != 0:
                return False
        except Exception:
            return False
        if self.step_to(ct, walk_q):
            self.demo_walks += 1
            return True
        return False

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
        # ⭐⭐ s57 THE KILLBOX, ARM 2 -- THE EXECUTIONER'S OWN `run()` BRANCH.
        # Every unit gets its own `Player` instance (kbprobe surprise 1), so
        # THIS is where the executioner sentinel lives; there is no separate
        # class and no shared object.
        # ⛔ THE WATCH RUNS ABOVE THE COOLDOWN AND AMMO GATES, exactly as arm
        # 1's `_kb_watch` runs above the launcher's: an occupancy integral
        # counted only on rounds we could SHOOT would measure our own reload,
        # not their detention, and `kb_full_rounds` -- the capacity column the
        # whole addendum turns on -- would then be a census of firing tubes.
        if (SK_KILLBOX and SK_KILLBOX_EXEC and SK_KB_EXEC
                and kind == EntityType.SENTINEL):
            if self.enemy is None and self.core is not None:
                self.enemy = enemy_core_for(self.mw, self.mh, self.core)
            self._kb_exec_watch(ct, p, rnd)
        if ct.get_action_cooldown() != 0:
            return
        if ct.get_global_ammo() < price:
            return
        # ⭐⭐ ARM 2's SHOT, AND ITS PLACEMENT IS THE PLANK.  Above the general
        # target ladder because `_target_pri` scores a HARVESTER (3) over a
        # BODY (2): a shipped tube with a chamber and an enemy harvester both
        # in its pattern would shoot the harvester for ever while the detained
        # raider sat there.  Below the ammo guard because `can_fire` returns
        # TRUE at 0 ammo and the raise inside `finish_firing_turret` destroys
        # our own tube.
        if (SK_KILLBOX and SK_KILLBOX_EXEC and SK_KB_EXEC
                and kind == EntityType.SENTINEL
                and self._kb_exec_fire(ct, p, rnd)):
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
                # ⭐⭐ v632 HEIMDALL PLANK 3 READS THIS LADDER AND CHANGES NOT
                # ONE LINE OF IT (comment only).  The ring turrets are ordinary
                # gunners/sentinels and run this exact firing turn, so
                # `CITADEL_TARGET_ORDER: raider_first_then_gunners_remove_
                # collar_barriers` (Magnus s57 2026-08-22) maps as:
                #   * RAIDER = a BODY.  The loop above reads
                #     `get_tile_builder_bot_id`, so an enemy builder IS a
                #     candidate and `_target_pri` scores it SK_PRI_BODY = 2 --
                #     above SK_PRI_OTHER and above a barrier.  This is the only
                #     verb in the tree that reaches a body at all (a builder
                #     cannot attack one: engine-re-proven s57, `can_fire` False
                #     990/990).  ⚠ HONESTLY: a HARVESTER scores 3, so the
                #     shipped ladder puts their harvester ABOVE the raider.
                #     Re-ranking is left out of this plank on purpose -- it
                #     would move EVERY turret in the tree (door, cover,
                #     forward tubes) and is a separate one-thing arm.
                #   * A TURRET SHOOTING US is handled by the counter-battery
                #     machinery, not here: SK_PRI_TURRET = 4 / SK_PRI_MARKED =
                #     5 (an armed building on our own ring), plus
                #     `_counter_sent_action` and `_peck_priority`.
                #   * COLLAR BARRIERS score SK_PRI_BARRIER = 0 and 0 is never
                #     fired at.  The flag that would change it exists and is
                #     SK_GUN_ROUTEBLOCK, below -- it is False, PLANK 3 DOES NOT
                #     FLIP IT, and it is the named phase-1 follow-up with the
                #     refutation-transfer caveat written at its flag.
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
        # ⭐⭐ s57 THE KILLBOX, ARM 1 -- the launcher unit IS a unit and this
        # method IS its `run()` branch (kbprobe surprise 1: every unit gets its
        # own `Player` instance, so these counters are THIS launcher's).
        # ⛔ THE WATCH RUNS ABOVE THE COOLDOWN GATE.  `kb_detain_rounds` is a
        # RESIDENCY INTEGRAL over the whole game; counting it only on rounds we
        # could act would measure our own cooldown, not their detention.
        # ⭐⭐ s57 THE PUSH, PIECE 2 -- THE WARDEN LAUNCHER'S OWN TURN, AND
        # IT TAKES THE WHOLE BRANCH.  A warden launcher stands beside THEIR
        # core; `_hl_pick_victim`'s ranking is written around OUR OWN delivery
        # seats and `_hl_pick_throw` refuses tiles inside OUR home ring, so
        # running either here would be the wrong instrument pointed at the
        # right unit.  ⛔ Flag off -> one module-constant test -> the v611 /
        # killbox paths below are reached exactly as they are today.
        # ⭐ s57 v3: THE GATE WIDENS BY ONE MODULE CONSTANT AND THE BRANCH BODY
        # IS UNTOUCHED.  A warden launcher is a warden launcher whichever body
        # planted it -- the throw logic, the sleeping-dogs sensor and the
        # border preference are properties of WHERE IT STANDS (beside THEIR
        # core), not of who bought it.  With both sub-flags off this is the
        # same single test it was and the killbox / v611 paths below are
        # reached exactly as today.
        if SK_PUSH and (SK_PUSH_WARDEN or SK_PUSH_WARDEN2):
            self._push_launcher_turn(ct, p, rnd)
            return
        if SK_KILLBOX:
            self._kb_watch(ct, p, rnd)
        victim = self._hl_pick_victim(ct, p) if SK_KILLBOX else None
        if SK_KILLBOX and victim is not None:
            # THE OPPORTUNITY COLUMN, and it is the falsifier's denominator:
            # a round with an enemy builder inside the pickup disc.  Throws
            # with no opportunity rounds, and opportunity rounds with no
            # throws, are BOTH registered falsifiers.
            self.kb_opportunity += 1
        if ct.get_action_cooldown() != 0:
            return
        if not SK_KILLBOX:
            victim = self._hl_pick_victim(ct, p)
        if victim is None:
            return
        vpos, _vid = victim
        if SK_KILLBOX:
            target, to_cell = self._kb_pick_throw(ct, p, vpos)
        else:
            target, to_cell = self._hl_pick_throw(ct, p, vpos), 0
        if target is None:
            return
        try:
            if not ct.can_launch(vpos, target):
                return
            ct.launch(vpos, target)
        except Exception:
            return
        self.hl_throws += 1
        if SK_KILLBOX:
            if to_cell:
                self.kb_throws_cell += 1
            else:
                self.kb_throws_tread += 1

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

    # ==================================================================
    # ⭐⭐ THE ROUTE, ARM 1 -- SK_ROUTE_HOME.  s57 build agent 2026-08-23.
    # ==================================================================
    # GAME CONTEXT: in-engine mechanics of the Florent Code League's simulated
    # grid; "enemy", "blocked" and "clear-out" name only game pieces.
    #
    # The measured defect and the two mechanisms behind it are written out in
    # full at the tail of `sk_maps.py` (the SK_ROUTE_HOME block).  In one line:
    # 8 of the 13 zero-delivery cells on t_cs_f1/f2 have a belt that stops 1-4
    # EMPTY tiles short of our own core and is never finished, and the two
    # reasons are (1) the walk names the tile and never arrives, unbounded, and
    # (2) `_route_gaps` only sees a chain with EXACTLY ONE missing link.
    #
    # ⛔ THIS BLOCK IS ADDITIVE.  It defines three new methods and reads only
    # state the constructor already sets plus five attributes of its own.  With
    # SK_ROUTE_HOME False every one of them returns before its first read and
    # the two call sites are one `if` on a module constant.

    def _route_missing(self, ct, rnd):
        """THE ROUTE AUDIT -- every unbuilt PLANNED tile on a chain that does
        not currently deliver, as {(x, y): rank}, rank 0 = nearest the core.

        This is `_route_gaps`' walk with ONE change and it is the whole audit:
        that method collects a chain's unbuilt tiles and DISCARDS the chain the
        moment it finds a second one (`if len(miss) > 1: break`), because it
        answers "which tile is the SOLE missing link".  A harvester whose line
        stops FOUR tiles short is exactly as orphaned and is worth exactly as
        much, so this keeps all of them.

        ⛔ WHAT IT IS NOT: it is not a second opinion about the belt.  The tiles
        come from `belt_plan`, the walk from `_belt_next`, the built-ledger from
        `belt_built` (kept honest by `_belt_watch`/`_belt_seed_store`), so a
        link this names is a tile the plan already wants, with the plan's own
        facing -- "re-lay the PLANNED tile first" is true by construction.

        ⚠ A CHAIN WHOSE `belt_head` IS None FEEDS THE CORE DIRECTLY and is never
        orphaned; a chain that walks off the plan is a broken plan, not a gap,
        and is dropped exactly as `_route_gaps` drops it.

        CPU: bounded by `len(harv_tiles) x SK_ROUTE_HOPS`, memoised on
        (round, belt_key, len(belt_built)) -- the third term is required because
        our own build inside the round is what makes a link stop being missing.
        On CPU exhaustion the LAST answer is returned rather than a wrong empty
        one (an empty set would silently switch the arm off).
        """
        if not SK_ROUTE_HOME:
            return {}
        key = (rnd, self.belt_key, len(self.belt_built))
        if self._rt_key == key:
            return self._rt_links
        links = {}
        for h in self.harv_tiles:
            cur = self.belt_head.get(h)
            if cur is None:
                continue                      # feeds the core direct
            if self._cpu_exhausted(ct):
                return self._rt_links         # degrade to the last answer
            chain = []
            miss = []
            hops = 0
            ok = True
            while hops < SK_ROUTE_HOPS:
                if cur not in self.belt_plan:
                    ok = False                # broken plan, not a gap
                    break
                chain.append(cur)
                if cur not in self.belt_built:
                    miss.append(cur)
                if self.core is not None and adjacent_to_core(
                        Position(cur[0], cur[1]), self.core):
                    break
                nxt = self._belt_next(cur)
                if nxt is None:
                    ok = False
                    break
                cur = nxt
                hops += 1
            if not ok or not miss:
                continue
            n = len(chain)
            for i, t in enumerate(chain):
                if t not in self.belt_built:
                    r = n - 1 - i             # 0 = the terminal, core-ward end
                    if links.get(t, 1 << 30) > r:
                        links[t] = r
        self._rt_key = key
        self._rt_links = links
        return links

    def _route_link_ok(self, ct, p, q, rnd):
        """The build-site guards, and they are `_belt_action`'s verbatim: not
        escalated, not banned, not inside a self-trap escape, owned by the belt
        under the arbiter, and leaving this body a tile to step onto."""
        xy = (q.x, q.y)
        if xy in self.belt_escalated or xy in self.belt_ban:
            return False
        if self.escape_ban.get(xy, -1) > rnd:
            return False
        if not self.may_build(q, OWNER_BELT):
            return False
        if self.free_neighbours(ct, p, exclude=q) == 0:
            return False
        return True

    def _route_action(self, ct, p, rnd):
        """THE ACTION HALF -- lay (or clear) the CORE-WARD-most missing link
        this body is orthogonally adjacent to.  True if it took the turn.

        ⛔ PLACED BELOW EVERY HEAL, SEAT AND CLEAR-OUT RUNG in `_home_keeper`
        and immediately above SK_TERM_FIRST, which is this tree's own settled
        placement for "the belt outranks a new harvester" -- a harvester with no
        route home is worth exactly zero forever, and this rung is what makes
        that true for a chain that is FOUR tiles short as well as one.
        """
        if not (SK_ROUTE_HOME and SK_BELT):
            return False
        links = self._route_missing(ct, rnd)
        if not links:
            return False
        cost = ct.get_conveyor_cost()
        if ct.get_global_resources() - cost < SK_ROUTE_HOME_TI:
            return False
        best = None
        for d in CARDINALS:
            q = p.add(d)
            if not self.ibp(q):
                continue
            xy = (q.x, q.y)
            rank = links.get(xy)
            if rank is None:
                continue
            if self.belt_plan.get(xy) is None:
                continue
            if not self._route_link_ok(ct, p, q, rnd):
                continue
            if best is None or rank < best[0]:
                best = (rank, xy, q)
        if best is None:
            return False
        _rank, xy, q = best
        # SIEGE AWARENESS: while the core's own alarm is fresh this arm refuses
        # a link beyond the keeper leash, exactly as PLANK 4's walk does.  A
        # link INSIDE the leash is laid: that body is standing at home already.
        if (SK_ROUTE_HOME_SIEGE and self.core is not None
                and self._under_attack(ct, rnd)
                and dsq_core(q, self.core) > SK_LEASH_DSQ):
            self.route_siege_refused += 1
            return False
        try:
            bid = ct.get_tile_building_id(q)
        except Exception:
            return False
        if bid is not None:
            # Something stands on the link.  `_belt_evict` owns all three cases
            # (ours already serving it, ours in the way, theirs to clear out)
            # and keeps its own ledgers; nothing is duplicated here.
            return self._belt_evict(ct, p, q, bid, rnd)
        # THE SPAWN RESERVE -- in-ring candidates only (see SK_ROUTE_HOME_SPAWN).
        if SK_ROUTE_HOME_SPAWN and self.core is not None and xy in self._route_ring():
            if not self._claim_spawn_ok(ct, q):
                self.route_spawn_refused += 1
                return False
        n = self.belt_rebuilds.get(xy, 0)
        if n >= SK_REBUILD_ESCALATE:
            return False                     # ledger V1 owns this tile now
        face = self.belt_plan.get(xy)
        try:
            if not ct.can_build_conveyor(q, face):
                return False
            ct.build_conveyor(q, face)
        except Exception:
            return False
        self.belt_rebuilds[xy] = n + 1
        self.belt_built.add(xy)
        self.belt_seen[xy] = rnd             # our own build IS an observation
        self.route_builds += 1
        return True

    def _route_ring(self):
        """The core's 8-way spawn ring minus its footprint -- the only tiles on
        which a build can consume a spawn candidate (`_spawn_plan`'s own walk).
        """
        if self.core is None:
            return frozenset()
        if self._rt_ring is None:
            fp = set(core_tiles_xy(self.core))
            self._rt_ring = frozenset(
                (self.core.x + dx, self.core.y + dy)
                for dx, dy in NEIGHBOURS8
                if (self.core.x + dx, self.core.y + dy) not in fp)
        return self._rt_ring

    def _route_walk(self, ct, p, rnd):
        """THE MOVEMENT HALF + THE STALL BREAKER.  Returns a Position or None.

        Prefers the nearest missing link, core-ward on a tie.  ⛔ THE STALL
        BREAKER IS THE HALF THAT ANSWERS THE MEASUREMENT: on four of the eight
        never-routed cells the keeper named ONE tile for 77-908 consecutive
        rounds while an enemy structure stood on it and their launcher threw our
        body out of the corridor 31-377 times.  After SK_ROUTE_STALL rounds on
        one link the tile enters `belt_ban` -- which `_belt_parents` excludes
        from the BFS and whose length is part of `belt_key` -- so the tree's own
        planner re-routes around it on the next round.  Capped at
        SK_ROUTE_BAN_MAX because a ban is irreversible for the game.
        """
        if not (SK_ROUTE_HOME and SK_BELT):
            return None
        links = self._route_missing(ct, rnd)
        if not links:
            self.route_tgt = None
            return None
        leashed = (SK_ROUTE_HOME_SIEGE and self.core is not None
                   and self._under_attack(ct, rnd))
        tgt = None
        bestk = None
        for xy, rank in links.items():
            if xy in self.belt_escalated or xy in self.belt_ban:
                continue
            if xy == (p.x, p.y):
                continue                     # cannot build under our own feet
            q = Position(xy[0], xy[1])
            if leashed and dsq_core(q, self.core) > SK_LEASH_DSQ:
                continue
            k = (p.distance_squared(q), rank)
            if bestk is None or k < bestk:
                bestk = k
                tgt = q
        if tgt is None:
            self.route_tgt = None
            return None
        xy = (tgt.x, tgt.y)
        if self.route_tgt is None or self.route_tgt[0] != xy:
            self.route_tgt = (xy, rnd)
        elif (rnd - self.route_tgt[1] >= SK_ROUTE_STALL
              and self.route_bans < SK_ROUTE_BAN_MAX):
            self.belt_ban.add(xy)
            self.route_bans += 1
            self.route_tgt = None
            return None
        return tgt


def _card(dx, dy):
    if dx > 0:
        return Direction.EAST
    if dx < 0:
        return Direction.WEST
    if dy > 0:
        return Direction.SOUTH
    return Direction.NORTH


# ===========================================================================
# THE ROUTE, ARM 1 -- SK_ROUTE_HOME constants.  Imported HERE, at module tail,
# rather than into the banner import block at the head of this file, so the arm
# cannot collide with concurrent work on that block.  Module-level names are
# resolved from module globals at CALL time, so the placement is behaviourally
# identical to importing at the top.  GAME CONTEXT: in-game bot constants.
# ===========================================================================
from sk_maps import (                                          # noqa: E402
    SK_ROUTE_HOME, SK_ROUTE_HOME_TI, SK_ROUTE_HOME_SPAWN,
    SK_ROUTE_HOME_SIEGE, SK_ROUTE_STALL, SK_ROUTE_BAN_MAX, SK_ROUTE_HOPS,
)
