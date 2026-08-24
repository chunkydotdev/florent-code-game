"""LOKI-1 (v105) -- a raid bot built around ESTABLISHMENT, not insertion.

Named for the trickster: this bot does not try to break the door down, it jams
the lock.  See raid.py for the doctrine and the measurements behind it, and
DESIGN.md for the short version.

Layering, so the raid is ablatable as a unit:
    doctrine.py   constants only (bots/_v103split's file, verbatim, plus a
                  LOKI block at the end)
    eco.py        the PORTED economy -- harvester bootstrap, trunk chains,
                  pave trail, navigation, siphon hygiene.  Deliberately copied
                  rather than redesigned: thor_r1 shipped a from-scratch
                  offensive bot with no harvesters and went 2 wins in 60 games
                  on zero titanium delivered.
    raid.py       NEW.  The collar, the forward Sentinel, the ferry, the
                  survival package.  Remove its four call sites in this file
                  and what is left is a plain economy bot.
    main.py       dispatch, the Core, roles, home defence, turrets.

Crash safety is not optional here: an exception that escapes run() makes the
engine PERMANENTLY delete that unit for the rest of the match, so run() is one
blanket try/except and every scan sits behind the CPU guard in eco.py.

LOKI-TURBO (2026-08-15) is loki with the hot paths rewritten and NOTHING else
changed -- see the header of eco.py for the measurement, the method and the
identity test.  Every edit in this file is one of: (a) a Position.add replaced
by integer arithmetic on a precomputed delta, (b) a per-round rebuild of a
static list moved into a cache keyed on what it depends on, (c) a dict or
tuple literal built inside a loop hoisted to module scope.
"""
import math
import sys

from fcode import Direction, EntityType, GameConstants, Position

from doctrine import *  # noqa: F401,F403
from eco import (
    EcoMixin, adjacent_to_core, core_tiles, dsq_core, enemy_core_for,
    heal_seats, known_map_for, nearest_cardinal, pack_pos, ring, unpack_pos,
)
from raid import BB_NO_FIRE, BB_SITE_VALUE, RaidMixin
from siege import SiegeMixin

# Hoisted out of the loops that used to rebuild them every iteration.
# `_sabotage_prio` built an eight-entry dict per adjacent tile; `_turret` built
# a nine-entry dict per attackable tile, and a Sentinel's ray is long.
SABOTAGE_PRIO = {
    EntityType.GUNNER: 0, EntityType.SENTINEL: 0,
    EntityType.CORE: 1, EntityType.HARVESTER: 2,
    EntityType.LAUNCHER: 3, EntityType.CONVEYOR: 4,
    EntityType.SPLITTER: 4, EntityType.BARRIER: 5,
}
TURRET_PRIO = {
    EntityType.CORE: 0, EntityType.SENTINEL: 1,
    EntityType.GUNNER: 2, EntityType.BUILDER_BOT: 3,
    EntityType.LAUNCHER: 4, EntityType.HARVESTER: 5,
    EntityType.CONVEYOR: 6, EntityType.SPLITTER: 6,
    EntityType.BARRIER: 7,
}
CORE_THREAT_TYPES = frozenset((EntityType.GUNNER, EntityType.SENTINEL))


class Player(EcoMixin, RaidMixin, SiegeMixin):

    def __init__(self):
        # --- identity / map ---
        self.n = 0
        self.team = None
        self.core = None
        self.enemy = None
        self.mw = self.mh = 0
        self.idx = 0
        self.role = "expand"
        self.role_n = 0
        self.map_grid = None
        self.map_walls = set()
        self.map_ores = []
        self.ore_cursor = 0

        # --- WAVE-LATE-SURGE (s58), per unit.  Three cheap pieces of state and
        # NOT ONE COMMS SLOT: all sixteen are allocated in this lineage, so the
        # pivot derives everything it needs from this body's own vision and the
        # round number.  `wave_ore_seen` is every ore tile this body has ever
        # seen, `wave_ore_full` the subset last observed carrying a building,
        # and `wave_pace` the short position window the unstick reads. ---
        self.wave_ore_seen = set()
        self.wave_ore_full = set()
        self.wave_pace = deque(maxlen=WAVE_SURGE_PACE_N)
        self.wave_lq_len = 0
        self.wave_lq_rnd = None

        # --- movement / targeting ---
        self.tgt = None
        self.last = None
        self.stuck = 0
        self.wall = None
        self.ang = 0.0

        # --- economy ---
        self.link_queue = []
        self.link_source = None
        self.wire_pending = []
        self.converging = False
        self.seat_ban = None
        self.seat_keep = None
        self.hs_seek_seat = None

        # --- LOKI-SAMESTOP (QUEUE #50), per unit. samestop_pending is the
        # armed second build (t_x, t_y, r_pos, facing) or None; the plan_key
        # cache exists only so the stop-tile preference does not re-run a
        # full-map BFS every round a builder is still walking toward ore. ---
        self.samestop_pending = None
        self.samestop_plan_key = None
        self.samestop_plan_cache = None

        # --- pave trail (PIECE F).  Per unit, no store slot: only this unit's
        # own _move writes it and only its own pave reads it. ---
        self.pave_prev = None
        self.pave_dir = None
        self.pave_rnd = -2

        # --- siphon hygiene ---
        self.siphon_id = None
        self.siphon_pos = None
        self.siphon_since = 0
        self.siphon_hp = None
        self.siphon_ban = {}

        # --- raid state (all per unit; the ring is a pure function of the
        # enemy anchor, so no store traffic is spent coordinating it) ---
        self.raid_slot = 0
        self.raid_station = None
        self.raid_rescan = -1
        self.raid_ban = {}
        self.raid_prev = None
        self.raid_pause_until = 0
        self.raid_stalls = 0
        self.raid_ring_key = None
        self.raid_corners = []
        self.raid_stations = []
        self.raid_seats = []
        self.raid_seatkeys = frozenset()

        # --- LOKI-SALT (v178) raid state, per unit.  salt_marks is pruned to
        # the memory window in _salt_turn, so it cannot grow with the match. ---
        self.salt_marks = {}
        self.salt_n = 0
        self.salt_pecks = 0
        self.salt_block_n = 0

        # --- LOKI-48 idle-gate funnel, per raider (see raid.py) ---
        self.si_reach = 0
        self.si_open = 0
        self.si_fire = 0

        # --- Core-only accounting ---
        self.prev_units = None
        self.lost_units = 0
        self.last_hp = None
        self.income_q = 0

        # --- LOKI-TURBO4 ---
        self.t4_ammo_prev = None        # Core: last round's global magazine
        self.t4_ammo_idle = 0           # Core: rounds since it last fell
        self.t4_chase_pos = None        # defender: where the chase started
        self.t4_chase_since = None      # defender: the round it started
        self.t4_chase_until = -10 ** 9  # defender: chases banned before this

        # --- LOKI-BELTBREAK, per unit.  On a RAIDER: plants made and the
        # refusal histogram (the live-target gate's other verdict, which is
        # the demo instrument).  On a planted GUNNER: rotations spent, hard
        # capped at LOKI_BELTBREAK_MAX_ROT for this unit's whole life, which
        # is what makes an A->B->A oscillation impossible by construction
        # rather than by cooldown tuning. ---
        self.bb_plants = 0
        self.bb_refuse = {}
        self.bb_rot = 0
        self.bb_shots = 0
        self.bb_seen = False

        # --- gunner rotation latch (PIECE I) ---
        self.rot_tgt = None
        self.rot_rnd = -10 ** 9
        self.rot_prev_dir = None
        self.rot_lock_d = 10 ** 9

        # --- LOKI-REESTABLISH (v539), per unit.  The first two are CORE-ONLY
        # (the Core is the single writer of FS_ECO_SLOT and therefore the only
        # unit that may declare or clear a famine); `v539_drafted` is
        # BUILDER-only and marks a body that took "expand" instead of "raid"
        # because famine held when its role was assigned. ---
        self.v539_last_flow = None  # round a stack was last seen on our mouth
        self.v539_eps = 0           # famine episodes declared this match
        self.v539_drafted = False   # rung B: this body was diverted to eco

        # --- LOKI-FERRY-SIEGE (s50), per unit.  Every field here is either a
        # cache keyed on something that cannot change during a match, or a
        # latch that only ever moves one way.  Nothing holds a Position across
        # rounds for a body that can be THROWN -- the raider re-reads
        # get_position() every turn (probe P2's stale-position hazard). ---
        self.fs_gate_ok = None      # None = not yet computable; else bool
        # --- v538 CLAIM GATE, per unit.  `v535_refuse` is this unit's cached
        # copy of `SiegeMixin._fs_map_gated`'s verdict, published to a
        # non-siege plank by `_v535_map_refuses` (ported from
        # `bots/_v535cornergate`, same name).  None = not yet asked or not yet
        # computable (no core / no dims), which is the "ask again next round"
        # state, NOT "runs".  Deliberately SEPARATE from `fs_gate_ok` --
        # siege.py `_v535_map_refuses` says why in full.
        self.v535_refuse = None
        self.v538_claim_gated = 0   # INSTRUMENT: claim branches stood down
        self.fs_off = False         # this body has degraded to incumbent raid
        self.fs_raider = False      # role tag; the role string stays "raid"
        self.fs_role_done = False   # the role decision is one-shot per body
        self.fs_best = None         # best dsq_core to the enemy seen so far
        self.fs_best_rnd = 0        # ...and the round it was seen (no-route)
        self.fs_ring = None
        self.fs_seats = None
        self.fs_ring_key = None
        self.fs_park = None
        self.fs_park_key = None
        self.fs_seal_started = False
        self.fs_barriers = 0
        self.fs_last_phase = None
        self.fs_arrived = False
        self.fs_tile_builds = {}
        self.fs_tile_pecks = {}     # (x, y) -> pecks spent clearing that tile
        # v541: per-BODY state for the enemy-core attack carve-out.  With
        # FS_V541_COREPECK = False not one of these fields is ever read or
        # written -- every read site sits inside the branch that flag guards.
        self.v541_pecks = 0         # lifetime pecks this body has landed
        self.v541_st_rnd = -1       # round the idle probe cached a station for
        self.v541_st = None         # that cached station (mirrors _fs_walk)
        self.fs_blocked_now = frozenset()
        self.fs_evictors = 0
        self.fs_healer_hist = {}    # (x, y) -> times an enemy body sat there
        self.fs_healer_obs = 0
        # LOKI-FS-RING-LADDER (s50).  All of it is per-BODY state; with
        # LOKI_FS_RING_LADDER = False not one of these fields is ever read.
        self.fs_last_hp = None      # HP at our previous turn (dodge trigger)
        self.fs_threat = {}         # (x, y) -> (round last seen, n turrets)
        self.fs_dodges = 0
        self.fs_tile_peck_rnd = {}  # (x, y) -> round of the last peck there
        self.fs_tile_visits = {}    # (x, y) -> peck-budget refills spent there
        self.fs_cleared = {}        # (x, y) -> round the squatter came off it
        self.fs_cleared_n = 0
        self.fs_sentinels = 0       # sentinels this body has bought
        # LOKI-FS-CREW (v513).  Per body; nothing here is read with
        # LOKI_FS_CREW = False.
        self.fs_role = "seal"       # "seal" | "supp" -- the crew's verb split
        self.fs_sealed_rnd = None   # last round the orthogonal-8 read closed
        self.fs_door_tgt = None     # (x, y) of the door turret being answered
        self.fs_door_since = -10 ** 9
        self.fs_door_pecks = 0
        self.fs_retreat = False     # this body is walking out of turret reach
        self.fs_supp_seat = None    # the seat the support is body-denying
        self.fs_sray = {}           # (x, y) -> on a SENTINEL ray, PERMANENT
        self.fs_hit_tiles = {}      # (x, y) -> we have taken damage here
        # LOKI-FS-V514 (s51).  Per body; nothing here is read with
        # LOKI_FS_V514 = False.
        self.fs_gray = {}           # (x, y) -> round last seen on a GUNNER ray
        self.fs_my_sents = []       # [x, y, dead?] per sentinel WE built
        self.fs_dead_sents = []     # (x, y) tiles a sentinel of ours died on
        self.fs_sent_lost = 0
        self.fs_cov_denied = 0      # census seats denied by launcher coverage
        self.fs_body = 1            # 1 = sealer/lead, 2 = support.  Fixed at
                                    # appointment; survives a PROMOTE, because
                                    # it selects this body's PUBLISH SLOT.
        self.fs_body_born = None    # first round this body ran the ferry
        self.fs_ring_rnd = None     # first round this body reached the ring
        self.fs_ride_rnd = None     # last round a link picked this body up
        self.fs_thrown = None       # launcher side: rider ids this link threw
        # launcher-only
        self.fs_born = None
        self.fs_ferry_seen = False
        self.fs516_last_throw = None    # v516 change 1b: last round THIS
                                        # launcher threw anything, ferry hop or
                                        # home-doctrine exile alike
        self.fs516_sent_ids = []        # v516 change 2: Core-side memory of
                                        # forward sentinel ids (see doctrine --
                                        # kept for the log only; get_hp cannot
                                        # read them out of vision)
        # --- v517: the forward sentinel's own fire-discipline state.  ALL of
        # it is per-BODY (each unit gets its own Player instance), which is
        # correct here: the window is a property of one turret's shots.
        self.v517_win = []              # core HP sampled at each of the last
                                        # FS_V517_NET_W core shots
        self.v517_shots = 0             # core shots this body has ever taken
        self.v517_hold_since = None     # round the current hold began
        self.v517_hold_now = False      # this round's fire decision
        self.v517_twin_now = False      # >= 2 forward sentinels alive
        self.v517_hp_now = None         # enemy core HP read this round
        self.v517_net_now = None        # net damage over the window
        self.v517_held = 0              # rounds a core shot was suppressed
        self.v517_held_fund = 0         # ...of which we could have PAID for it
        self.v517_held_only = 0         # ...and fired at nothing else either
        self.v517_resets = 0            # TTL re-probes
        self.v517_viol = 0             # holds taken inside the fresh-contact
                                        # window.  ⛔ MUST BE 0.
        self.v517_bank_until = -1       # Core-only: round the twin bank latch
                                        # expires (change 2b)
        # --- v518 state.  Written under the v518 flags, read only under them.
        self.v518_early = 0             # change 2(a): first-sentinel purchases
                                        # taken ahead of rung 1 (<= 1 per game
                                        # by construction)
        self.v518_res_until = -1        # change 3, Core-only: round the twin
                                        # RESERVE latch expires
        self.v518_res_rounds = 0        # rounds the reserve was open
        self.v518_res_bind = 0          # ...of which it actually RAISED the
                                        # floor above what the parent would
                                        # have used (zero-vs-nonzero falsifier)
        # --- v519 state.  Written under the v519 flags, read only under them.
        self.v519_gf_plants = 0         # change 1: beltbreak shredders this
                                        # BODY planted from the ferry path
        self.v519_gf_rnd = -1           # ...and the round of the last one
        # --- v520 state.  Written under the v520 flags, read only under them.
        self.v520_arc = FS_V520_ARC_NONE    # change 1: this body's claimed arc
        self.v520_arc_rnd = -1          # round the arc was claimed (sticky)
        self.v520_arc_collide = 0       # claim-time conflicts RESOLVED (the
                                        # peer already held the arc I landed
                                        # on, so I took the other) -- may be
                                        # non-zero; it is the deconfliction
                                        # working, not the alarm.
        self.v520_arc_dup = 0           # ⛔ THE ALARM: rounds in which a LIVE
                                        # peer was publishing MY arc after both
                                        # claims settled, i.e. two bodies on one
                                        # half.  Must be 0.
        self.v520_split_n = 0           # launcher side: split throws made
        self.v520_term = False          # launcher side: this launcher was sited
                                        # by the TERMINAL rule (derived, not
                                        # tagged -- see `_v520_term_launcher`)
        self.v520_term_conflict = 0     # body side: terminal sitings where
                                        # objective (a) and (b) disagreed
        self.v520_pres_until = -1       # change 2, Core-only: round the presence
                                        # RESERVE latch expires
        self.v520_pres_seen = {}        # seat -> 1 once it has EVER reported.
                                        # The opening exemption: unborn != dead.
        self.v520_pres_vacant = 0       # rounds a seat read vacant
        self.v520_pres_rounds = 0       # rounds the reserve was open
        self.v520_pres_bind = 0         # ...of which it RAISED the floor
        self.v520_gf_near = 0           # change 3: plants taken under the
                                        # lowered annulus floor
        self.v520_appt_rnd = -1         # round this body CLAIMED the support
                                        # seat (-1 = never)
        self.v520_appt_yield = 0        # ⛔ ALARM: races this body LOST on the
                                        # readback.  A non-zero total is the
                                        # race still happening -- but now it is
                                        # RESOLVED rather than silent.
        # --- v522 state.  Written under the v522 flags, read only under them.
        # Both are CORE-side counters and both exist so the mechanism reads
        # zero-vs-nonzero rather than being inferred from an outcome column.
        self.v522_bind = 0              # rounds the NEAR floor actually RAISED
                                        # ti_floor above what the parent would
                                        # have used.  ⛔ This is also the TTL
                                        # counter (FS_V522_MAX_RNDS) -- rounds
                                        # BOUND, not rounds eligible, so a NEAR
                                        # window that costs nothing does not
                                        # spend the budget.
        self.v522_near_rnds = 0         # rounds the Core READ FS_PH_KILL_NEAR
                                        # off the channel.  The denominator that
                                        # makes `v522_bind == 0` readable.
        self.fs516_reach = None         # v516 change 3: (Position|None, rnd)
        self.fs516_reach_key = None
        self.fs516_reach_since = 0
        self.fs_sites = None
        self.fs_sites_key = None
        self.fs_dump = None
        self.fs_dump_key = None
        self.fs_evicts = 0
        # Core-only
        self.fs_replaced = 0
        self.fs_repl_rnd = -10 ** 9

        # --- one report per unit lifetime, so a bug cannot flood stderr ---
        self.reported_cpu = False
        self.reported_error = False

        # --- LOKI-TURBO caches.  Every one of these holds a value that is a
        # pure function of things that do not change during a match (the
        # decoded terrain, our Core anchor, the enemy anchor, this unit's seat)
        # and that LOKI rebuilt on every call.  None of them is read before it
        # is written, and each carries the key it was built for so a change in
        # its inputs -- the enemy anchor being refined on first sighting, say
        # -- rebuilds it rather than serving a stale answer. ---
        self._nav_key = None            # (core, enemy, mw, mh)
        self._nav_tpl = None            # padded blocked template, _bfs_direction
        self._link_tpl_key = None       # (core, mw, mh)
        self._link_tpl = None           # padded blocked template, _link_path
        self._link_ore_only = None      # tiles blocked ONLY by being ore
        self._link_goal_key = None      # (core, mw, mh, ban)
        self._link_goals_set = None     # the Core delivery ring
        self._pick_key = None           # (core, role_n)
        self._pick_assigned = None      # this seat's ore partition, sorted
        self._home_seat_key = None      # (core, mw, mh)
        self._home_seat_keys = None     # {(x, y)} of our own eight heal seats
        self._spawn_ring_key = None     # core anchor
        self._spawn_ring = None         # ring(core, 2)
        self._launch_key = None         # (launcher pos, mw, mh)
        self._launch_sites = None       # every reachable throw site
        self._launch_far_key = None     # (launcher pos, our core)
        self._launch_far = None         # sites, farthest from home first
        self._launch_near_key = None    # (launcher pos, enemy anchor)
        self._launch_near = None        # sites, nearest the enemy first

    # ------------------------------------------------------------------
    # entry
    # ------------------------------------------------------------------

    def run(self, ct):
        # An exception escaping run() makes the engine PERMANENTLY delete this
        # unit for the rest of the match.  Catching it costs one round's
        # action instead; there is no situation where propagating is better.
        try:
            self._dispatch(ct)
        except Exception:
            if not self.reported_error:
                self.reported_error = True
                import sys
                import traceback
                traceback.print_exc(file=sys.stderr)

    def _dispatch(self, ct):
        e = ct.get_entity_type()
        if e == EntityType.CORE:
            self._core(ct)
        elif e == EntityType.BUILDER_BOT:
            self._builder(ct)
        elif e in (EntityType.GUNNER, EntityType.SENTINEL):
            self._turret(ct)
        elif e == EntityType.LAUNCHER:
            self._launcher_turn(ct)

    # ------------------------------------------------------------------
    # the Core
    # ------------------------------------------------------------------

    def _core(self, ct):
        p = ct.get_position()
        w, h = ct.get_map_width(), ct.get_map_height()
        self.mw, self.mh = w, h
        if self.team is None:
            self.team = ct.get_team()
        if self.core is None:
            self.core = p
        if self.map_grid is None:
            self.map_grid = known_map_for(w, h, p, ct)
        if ct.read_store(SLOT_ENEMY_CORE) == 0:
            ct.write_store(SLOT_ENEMY_CORE, pack_pos(enemy_core_for(w, h, p)))

        rnd = ct.get_current_round()

        # --- threat latch -------------------------------------------------
        under = False
        for eid in ct.get_nearby_entities():
            try:
                if ct.get_team(eid) == ct.get_team():
                    continue
                d = p.distance_squared(ct.get_position(eid))
                et = ct.get_entity_type(eid)
            except Exception:
                continue
            if (et in CORE_THREAT_TYPES and d <= 64) or (
                et == EntityType.BUILDER_BOT and d <= 16
            ):
                under = True
                ct.write_store(SLOT_THREAT, pack_pos(ct.get_position(eid)))
                break
        hp = ct.get_hp()
        if self.last_hp is not None and hp < self.last_hp:
            under = True
        self.last_hp = hp
        if under:
            ct.write_store(SLOT_UNDER, 1)
            ct.write_store(SLOT_ATK_RND, rnd)
        else:
            last = ct.read_store(SLOT_ATK_RND)
            # 50-round latch: a harasser that parks just outside every trigger
            # radius let a shorter latch expire between pokes, which collapsed
            # the ammo magazine to one Sentinel shot on a four-figure bank.
            under = bool(last and rnd - last < 50)
            ct.write_store(SLOT_UNDER, 1 if under else 0)

        harv = ct.read_store(SLOT_HARVESTERS)
        if LOKI_FS_V514 and FS_V514_ECOGATE:
            # ⭐⭐ v514 CHANGE A -- MAGNUS RULING 2.  Slot 5 stops being a dead
            # write (3 writes, 0 reads in the parent) and becomes the CORE'S
            # OWN eco-gate word, single writer.  Everything the sentinel gate
            # and the magazine now depend on is published from here.
            self._fs_eco_publish(ct, rnd, harv)
        elif harv >= ECO_NEED:
            ct.write_store(SLOT_ECO_READY, 1)

        # Income meter, in quarter-titanium so passive (10 Ti / 4 rounds) and
        # harvester output (a 10-stack / 4 rounds) are both exact integers.
        self.income_q += 10 + K_HEAL_HARV_Q * harv
        # T4 BLEED BEACON.  Slot 9 was written every round and read by NOBODY
        # (loki_analysis.md 1.3), so the Core spends it on the one fact a
        # builder outside its own r^2=20 vision cannot obtain: how hurt we are.
        # `_core_shelled` reads it when the Core is not in view.
        if T4_BLEED_BEACON_ON:
            ct.write_store(SLOT_HEAL_BUDGET, ct.get_max_hp() - hp)
        elif K_HEAL_BUDGET_ON:
            ct.write_store(SLOT_HEAL_BUDGET, (self.income_q // 4) * K_HEAL_RATE_PCT // 100)

        ti, ammo = ct.get_global_resources(), ct.get_global_ammo()
        if LOKI_FS_V518 and FS_V518_TIWATCH:
            # ⭐ THE BANK-DRAIN INSTRUMENT.  `scale` is the attribution: the
            # cost scale is ONE GLOBAL ADDITIVE team factor and every build adds
            # a KNOWN increment to it (barrier/conveyor/splitter +1, harvester
            # +5, launcher +10, builder bot/gunner/sentinel +20 percentage
            # points), so a round-over-round scale delta says WHAT was bought
            # out of the bank without touching a single build site.  Read at the
            # Core's turn, which runs before the raider's in unit order, so the
            # delta covers the PREVIOUS round's spending in full.
            try:
                print("TIWATCH518", rnd, "ti", ti, "ammo", ammo,
                      "scale", int(round(ct.get_scale_percent())),
                      "units", ct.get_unit_count(),
                      "sen", ct.get_sentinel_cost(),
                      "bar", ct.get_barrier_cost(),
                      "beat", 1 if self._fs_sent_beat_live(ct) else 0,
                      "hold", 1 if self._fs_hold_live(ct) else 0,
                      file=sys.stderr)
            except Exception:
                pass
        home_guns = ct.read_store(SLOT_HOME_GUN)
        fwd_guns = ct.read_store(SLOT_FWD_GUN)
        weapons = home_guns + fwd_guns

        # T4 GHOST MAGAZINE BRAKE.  Both gun slots are monotone -- written only
        # as `read + 1`, never decremented -- so `weapons` counts rubble, and
        # rubble is what buys the magazine: one dead forward Sentinel still
        # asks for `min(120, 40 + 20*1) = 60` ammunition and still drops
        # `ti_floor` from 52 to 12.  The Core cannot see the forward ring, so it
        # censuses the AMMUNITION instead, which is a free global read: a
        # magazine that has not FALLEN in T4_AMMO_IDLE_RNDS rounds is not being
        # fired by anything alive.  One shot clears the brake.
        # It brakes the ROUND-BY-ROUND top-up only; the r960 dump keeps the raw
        # `weapons` count, because a gun that has had nothing in range for
        # twelve rounds may still have something in range at r999 and the dump
        # is capped by burnable rounds already.
        if T4_AMMO_IDLE_ON:
            if self.t4_ammo_prev is None or ammo < self.t4_ammo_prev:
                self.t4_ammo_idle = 0
            else:
                self.t4_ammo_idle += 1
            self.t4_ammo_prev = ammo
            if weapons and ammo >= T4_AMMO_IDLE_MIN \
                    and self.t4_ammo_idle >= T4_AMMO_IDLE_RNDS:
                home_guns = fwd_guns = weapons_top = 0
            else:
                weapons_top = weapons
        else:
            weapons_top = weapons

        # --- ammunition ----------------------------------------------------
        # convert_ammo is action-free, once per team per turn, usable the same
        # turn, so none of this ever costs a spawn.
        endgame_dumped = False
        if ENDGAME_SWITCH_ON and rnd >= ENDGAME_RND and weapons:
            # Ammunition scores in NO tiebreak and stored titanium is #3, so
            # convert only what the guns can plausibly BURN before r1000 and
            # leave the rest banked.  Reserve two harvesters: one built at r999
            # is alive at r1000 and outranks stored titanium (tiebreak #2).
            endgame_dumped = True
            cap = (LAST_RND - rnd) * 5 * weapons
            amt = min(ti - 2 * ct.get_harvester_cost(), cap - ammo)
            if amt > 0 and ct.can_convert_ammo(amt):
                ct.convert_ammo(amt)
                ti, ammo = ct.get_global_resources(), ct.get_global_ammo()

        if not endgame_dumped:
            ammo_target = 24 if under else AMMO_FLOOR
            if weapons_top:
                ammo_target = max(ammo_target, min(48, 4 * weapons_top))
            # A forward Sentinel is 10 ammo every 3 rounds; it is the only
            # sustained damage the raid has once the collar is up, so it gets
            # its own magazine floor rather than sharing the home one.
            if fwd_guns:
                ammo_target = max(ammo_target, min(120, 40 + 20 * fwd_guns))
            # T4 BURN CAP.  Never bank more magazine than the guns we believe we
            # own could fire in T4_BURN_RNDS rounds at T4_AMMO_PER_RND each --
            # the Sentinel floor above asks for 60 on ONE turret, which is six
            # shots held in reserve, and the decoded game bought that 60 with
            # 35% of everything it mined all match.
            if T4_BURN_CAP_ON and weapons_top:
                ammo_target = min(
                    ammo_target, T4_BURN_RNDS * T4_AMMO_PER_RND * weapons_top)
            # LOKI-BELTBREAK MAGAZINE.  ⛔ PLACED AFTER THE T4 BURN CAP AND
            # NOT BEFORE IT, DELIBERATELY.  That cap is `min()`-ed against a
            # target derived from `weapons_top`, which is SLOT_HOME_GUN +
            # SLOT_FWD_GUN -- home counter-battery and forward SENTINELs.  A
            # beltbreak gunner is in neither counter (it writes no gun slot at
            # all, see the doctrine block), so `weapons_top` can be 0 while a
            # gunner is standing in the enemy's belt asking for 4 ammo a round;
            # a bump placed above the cap would be multiplied by that 0 and
            # silently deleted.  This is study §7.3's closed loop: our ammo
            # target is keyed to turrets we already count, so a turret nothing
            # counts is a turret nothing funds.
            #
            # The signal is a HEARTBEAT, not a count: SLOT_BELTBREAK carries
            # round+1 from the last raider that planted one or the last
            # beltbreak gunner that had a live target on its ray.  It goes
            # stale on its own in LOKI_BELTBREAK_STALE rounds, which is exactly
            # what the monotone SLOT_FWD_GUN could not do -- the ghost magazine
            # that converted 146 Ti against 170 mined all match.
            if LOKI_BELTBREAK_ON:
                beat = ct.read_store(SLOT_BELTBREAK)
                if beat and rnd - (beat - 1) <= LOKI_BELTBREAK_STALE:
                    bb_live = True
                    ammo_target = max(ammo_target, LOKI_BELTBREAK_AMMO)
                else:
                    bb_live = False
            else:
                bb_live = False
            # LOKI-FERRY-SIEGE MAGAZINE.  ⛔ PLACED AFTER THE T4 BURN CAP FOR
            # THE SAME REASON THE BELTBREAK BUMP IS: that cap is min()-ed
            # against `weapons_top`, and a forward sentinel that has not fired
            # yet because it has no ammunition is exactly the turret the cap
            # reads as rubble.  A bump above it would be multiplied by zero.
            #
            # WHY 300 AND NOT 120.  500 core HP / 18 damage = 28 sentinel shots
            # = 280 ammunition, and that is the arithmetic FLOOR, not a target.
            # The one decoded game that converted exactly 280 degraded from one
            # shot per 2 rounds to one per 4 after r88 and took until r184 to
            # finish an otherwise-perfect 12/12 ring; the game that converted
            # 300 killed at r114.  Ammunition, not titanium, is the clock on
            # this plank -- and one of those games won with
            # `titanium_collected` = 0 for BOTH teams, financed entirely by the
            # starting 500 plus passive income.
            fs_ph = FS_PH_NONE
            fs_live = False
            if LOKI_FERRY_SIEGE_ON:
                _fb, fs_ph, _fr = self._fs_state(ct)
                # ⭐⭐ v513 CHANGE A -- MAGNUS'S RULE, ON THE CORE SIDE: THE
                # SIEGE MAGAZINE DOES NOT ARM BEFORE THE SALT IS DOWN.  Under
                # v512 the siege ammunition target engaged at FS_PH_RING, which
                # the s50 diagnostic measured arriving at ROUND 6-12 -- so the
                # opening bank the harvesters and the belt are bought out of was
                # being converted into ammunition for a collar that was not
                # closed, and the autopsy then measured that fire netting ZERO
                # (88.6% of all damage healed back; exact to the hit point in
                # eight games).  Post-salt only: SEALED or KILL.
                if LOKI_FS_V514 and FS_V514_ECOGATE and not FS_V514_MAGGATE:
                    # The magazine keeps v513's salt rule while the TURRET
                    # runs on Magnus's new gate.  Phase 5 (turret up, collar
                    # open) is deliberately excluded here -- that is the whole
                    # difference between the two settings.
                    armed = FS_PH_SEALED <= fs_ph <= FS_PH_KILL
                elif LOKI_FS_V514 and FS_V514_ECOGATE and FS_V514_MAGGATE:
                    # ⭐⭐ v514 CHANGE A, CORE SIDE.  MAGNUS RULING 2 moved the
                    # SENTINEL gate off the salt and onto "2 harvesters built
                    # and connected"; BUILDER DEFAULT, flagged for his veto:
                    # the magazine that feeds that sentinel follows the SAME
                    # gate.  Arming on the salt was v513's change A and it is
                    # superseded -- on atoll and midgard the collar closed 0 of
                    # 12 times, so the salt form armed the magazine NEVER on
                    # exactly the two maps we lose.
                    # ⛔ The phase term stays: ammunition is worth nothing
                    # before a body is at their ring.  What is removed is the
                    # SEALED requirement, not the RING one.
                    # ⛔ v522 PARITY, AND IT IS A DEAD BRANCH IN THE FIRED
                    # CONFIG (FS_V514_MAGGATE ships False).  It is extended
                    # anyway because FS_PH_KILL_NEAR = 6 is a strict refinement
                    # of FS_PH_KILL_OPEN = 5 and this is one of exactly two
                    # sites in the tree where the two codes would otherwise
                    # separate -- an arm that turns MAGGATE on must not read a
                    # silent semantic change it never asked for.
                    armed = ((FS_PH_RING <= fs_ph <= FS_PH_KILL_OPEN
                              or (LOKI_FS_V522 and FS_V522_FLOOR
                                  and fs_ph == FS_PH_KILL_NEAR))
                             and self._fs_eco_gate_ok(ct))
                elif LOKI_FS_CREW and FS_SALT_GATE:
                    armed = FS_PH_SEALED <= fs_ph <= FS_PH_KILL
                else:
                    armed = FS_PH_RING <= fs_ph <= FS_PH_KILL
                # ⭐⭐ v516 CHANGE 2, CORE SIDE -- THE MAGAZINE ARMS ON A LIVE
                # FORWARD SENTINEL, FULL STOP.  Every branch above reads
                # `fs_ph`, which is published by the RAIDER; when the raider is
                # dead the phase decays and the magazine disarms UNDER A TURRET
                # THAT IS STILL FIRING AT THEIR CORE.  Autopsy #1: armed in
                # 21.2% of core-hitting-sentinel rounds, ammo < 10 in 78.3%,
                # exemplar midgard_s1_A pinned at 80 Ti and 4 ammo for 57
                # rounds while their core went 500 -> 158 and our turret died
                # with the bank unspent.  The beat is the sentinel's OWN
                # heartbeat and needs nobody's eyes.
                # ⛔ A DISJUNCT, NOT A REPLACEMENT.  The phase branches also arm
                # BEFORE any turret exists (RING/SEALED), which is how the
                # ammunition is there when the turret is bought; this term only
                # adds the state they miss.
                if LOKI_FS_V516 and FS_V516_GLOBALSENT \
                        and self._fs_sent_beat_live(ct):
                    armed = True
                if armed:
                    fs_live = True
                    ammo_target = max(ammo_target, FS_AMMO_TARGET)
            ti_floor = 12 if (under or weapons_top) else 52
            if E1_AMMO_FLOOR_ON and not under:
                ti_floor = max(
                    ti_floor,
                    min(ct.get_harvester_cost(), E1_RESERVE_CAP) + E1_HARV_RESERVE_MARGIN,
                )
            # `bb_live` joins the ARMING condition but NOT `ti_floor`: the
            # beltbreak gunner may open the tap, it may not lower the harvester
            # reserve E1_AMMO_FLOOR exists to protect.  Magnus's s48 warning
            # ("if we allow unlimited harvesters they will take the titanium
            # from our offensive builders") has a symmetric failure and this is
            # the side of it a turret plank is likely to commit.
            # The siege reserve, and it runs in BOTH directions.  Before the
            # ring is sealed the magazine may only be filled out of surplus
            # ABOVE the whole remaining collar plus the sentinel -- a bank
            # converted to ammunition cannot buy the barriers, and a partial
            # seal is measurably worse than no seal.  Once sealed, the bank has
            # nothing left to buy and the floor drops out of the way.
            chunk = 16
            if fs_live:
                chunk = FS_AMMO_CHUNK
                try:
                    bar = ct.get_barrier_cost()
                    sen = ct.get_sentinel_cost()
                except Exception:
                    bar, sen = 3, 30
                # v516 change 2: the KILL-state RESERVE follows the same beat.
                # Arming the magazine while leaving `ti_floor` at the collar
                # price is the midgard_s1_A exemplar exactly -- bank pinned at
                # 80 Ti, ammo 4, a sentinel firing -- so the two have to move
                # together or the fix is half a fix.
                _v516_kill = (LOKI_FS_V516 and FS_V516_GLOBALSENT
                              and self._fs_sent_beat_live(ct))
                # ⛔ v522 PARITY, second and last site.  The third disjunct is
                # dead in the fired config (FS_V514_MAGGATE ships False) and the
                # branch is reached through `_v516_kill` -- which is the same
                # route the PARENT takes in these rounds, because the parent
                # publishes FS_PH_KILL_OPEN = 5 in exactly them and 5 does not
                # match `== FS_PH_KILL` either.  ⇒ SWAPPING 5 FOR 6 CHANGES
                # NOTHING ABOUT BRANCH ENTRY, and the PHASE_ONLY mutant is the
                # measurement of that claim rather than the argument for it.
                if _v516_kill or fs_ph == FS_PH_KILL \
                        or (fs_ph == FS_PH_KILL_OPEN
                            and LOKI_FS_V514
                            and FS_V514_MAGGATE) \
                        or (LOKI_FS_V522 and FS_V522_FLOOR
                            and fs_ph == FS_PH_KILL_NEAR
                            and LOKI_FS_V514
                            and FS_V514_MAGGATE):
                    # A SENTINEL IS STANDING: ammunition IS the clock now, and
                    # everything above the eight orthogonal barriers still owed
                    # belongs to it.  18 damage per 10 ammo on a 2-round reload
                    # is 5 ammo a round of burn; a magazine that cannot keep up
                    # degrades the cadence to one shot per four rounds, which is
                    # the difference between a r114 kill and a r184 one.
                    ti_floor = max(FS_AMMO_TI_FLOOR, 8 * bar)
                    if LOKI_FS_CREW and FS_SALT_GATE:
                        # ⭐⭐ v513 CHANGE F -- THE MAGAZINE LOCK, TRACED RATHER
                        # THAN RE-TUNED.  The lock is this line: `8 * bar` at
                        # the live 2.5-3x scale is 56-72 titanium, and
                        # glacierkeep_g5 held 48-58 for two hundred consecutive
                        # rounds with ammo = 1 and an aligned sentinel standing
                        # -- the bank NEVER crossed the floor, so `ti >
                        # ti_floor` was False every round and conversion was
                        # arithmetically unreachable.  73.9% of all
                        # live-sentinel rounds across 24 games were in exactly
                        # that state.
                        # ⛔ AND UNDER CHANGE A THE EIGHT-BARRIER TERM PRICES A
                        # PURCHASE THAT CANNOT BE PENDING: a sentinel only
                        # exists once the orthogonal-8 was CLOSED, so what the
                        # collar still needs at KILL is a REPAIR allowance, not
                        # a fresh collar.  What replaces it is that allowance
                        # plus the economy's lifeline, which is the invariant
                        # that stops these two reserves crossing again (change
                        # C: the Core's floor stays FS_ECO_HEADROOM above the
                        # level the economy can still spend at).
                        # ⛔⛔ AND THE SHAPE IS WHY TWO RE-TUNES FAILED, NOT THE
                        # VALUE.  In this state `convert_ammo` is the ONLY
                        # consumer of surplus, so THE BANK EQUILIBRATES TO
                        # EXACTLY `ti_floor` AND STAYS THERE: measured median
                        # bank across all 24 games = 48.0 = 8 x bar at the modal
                        # live scale, and the gate `ti > ti_floor` was False in
                        # 74.4% / 77.9% / 83.7% of KILL rounds on three
                        # instrumented re-runs, with the median bank equal to
                        # the floor to the titanium.  ANY constant reproduces
                        # that.  What breaks it is a floor small enough that the
                        # equilibrium still leaves change on the table -- the
                        # repair allowance -- combined with the economy's own
                        # lifeline (change C), which is what stops a low floor
                        # from starving the belt instead.
                        ti_floor = max(FS_AMMO_TI_FLOOR,
                                       FS_MAG_REPAIR_BARRIERS * bar)
                        # ⭐⭐⭐ v522 -- THE NEAR FLOOR.  THE ONE MECHANISM OF
                        # THIS BUILD, AND IT IS THREE LINES BECAUSE THE
                        # DIAGNOSIS WAS THE EXPENSIVE PART.
                        #
                        # The line directly above is what `_v521_why` caught in
                        # the act: with a forward turret live the bank
                        # equilibrates to EXACTLY `FS_MAG_REPAIR_BARRIERS * bar`
                        # and stays there (v513 change F measured the
                        # equilibrium and wrote it down), which is 12-16
                        # titanium at the live scale, against a collar asking
                        # 18-22 in the modal NEAR round.  We are one barrier and
                        # a hop margin short, every round, by construction.
                        #
                        # ⛔ WHAT IS DIFFERENT FROM v521 CHANGE 1d, WHICH IS THE
                        # SAME DIAGNOSIS AND A MEASURED -9.83 pp: 1d raised the
                        # floor to `8 * bar + 6` in EVERY open-collar round and
                        # took `funded -> kill` from 69 rounds to 100.  This
                        # raises it to `FS_V522_SEATS * bar + FS_SEAL_MARGIN`
                        # -- one barrier and a margin above the allowance, not a
                        # fresh collar -- and only in rounds the RAIDER has
                        # published as NEAR, only while the magazine is FUNDED,
                        # and only for FS_V522_MAX_RNDS rounds a match.
                        #
                        # ⛔ THE FUNDING TERM IS READ HERE, NOT PUBLISHED, AND
                        # THE DIRECTION MATTERS: below FS_V522_FUND_AMMO the
                        # magazine is the binding constraint and holding
                        # titanium back from it is exactly v521's failure.  The
                        # raider's own check is one round stale (the store is
                        # buffered); this one is not, and it is the one that
                        # decides.
                        #
                        # ⛔ RESERVE, NOT SPEND: it enters through `max()`, so no
                        # floor already computed in this block -- E1_AMMO_FLOOR's
                        # harvester guarantee included -- can be lowered by it.
                        # ⭐ THE LOG IS GATED ON ITSELF, NOT ON THE MASTER
                        # (v521 surprise 7), so `mOff`'s zero has a denominator.
                        if (LOKI_FS_V522 and FS_V522_FLOOR) or FS_V522_MAG_LOG:
                            _v522_on = LOKI_FS_V522 and FS_V522_FLOOR
                            _v522_near = (fs_ph == FS_PH_KILL_NEAR)
                            if FS_V522_CREW_READ and not _v522_near:
                                _v522_near = self._v522_crew_near(ct, rnd)
                            # correction (1): the funding term is the RAIDER's
                            # publish-time check, not this one.  The raw read is
                            # kept so the MAG522 tape still reports what the
                            # Core's own round would have said.
                            _v522_fund_raw = ammo >= FS_V522_FUND_AMMO
                            _v522_fund = (_v522_fund_raw
                                          or not FS_V522_CORE_FUND)
                            _v522_ttl = (self.v522_bind
                                         < FS_V522_MAX_RNDS)
                            _v522_want = min(
                                FS_V522_SEATS * bar + FS_SEAL_MARGIN,
                                FS_V522_FLOOR_CAP)
                            _v522_bind = (_v522_on and _v522_near and _v522_fund
                                          and _v522_ttl
                                          and not FS_V522_PHASE_ONLY
                                          and _v522_want > ti_floor)
                            if _v522_bind:
                                self.v522_bind += 1
                                ti_floor = _v522_want
                            if _v522_near:
                                self.v522_near_rnds += 1
                            if FS_V522_MAG_LOG:
                                try:
                                    print("MAG522", rnd, "ph", fs_ph,
                                          "on", 1 if _v522_on else 0,
                                          "near", 1 if _v522_near else 0,
                                          "fund", 1 if _v522_fund_raw else 0,
                                          "fuse", 1 if _v522_fund else 0,
                                          "ttl", 1 if _v522_ttl else 0,
                                          "ti", ti, "ammo", ammo, "bar", bar,
                                          "want", _v522_want,
                                          "floor", ti_floor,
                                          "bind", 1 if _v522_bind else 0,
                                          "nbind", self.v522_bind,
                                          "nnear", self.v522_near_rnds,
                                          file=sys.stderr)
                                except Exception:
                                    pass
                        # ⭐⭐⭐ v521 CHANGE 1d -- THE MAGAZINE IS EATING THE
                        # COLLAR'S MONEY IN EXACTLY THE STATE THE COLLAR NEEDS
                        # TO CLOSE, AND THAT IS THE SEAL-SHOT DISJOINTNESS ONE
                        # LEVEL DOWN.
                        #
                        # ⛔ THIS WAS NOT DESIGNED, IT WAS DIAGNOSED.  The two
                        # ladder-reorder designs above it were both measured
                        # INERT (0 of 18 deterministic games changed a byte on
                        # the three maps where the sync state fires), so
                        # `_v521_why` was written to ask, in each NEAR round,
                        # what actually stopped the collar.  The tape is not
                        # ambiguous -- across drakkarfjord / glacierkeep /
                        # nordkap at seed 7 the modal NEAR round reads
                        # `ti=12 price=18`, `ti=14 price=20`, `ti=16 price=22`:
                        # THE BANK IS BELOW THE REMAINING COLLAR'S PRICE IN
                        # ESSENTIALLY EVERY ROUND, and it is pinned there BY
                        # THIS LINE.  v513 change F measured the equilibrium
                        # itself and wrote it down five comment-lines above:
                        # "THE BANK EQUILIBRATES TO EXACTLY `ti_floor` AND STAYS
                        # THERE".  With FS_MAG_REPAIR_BARRIERS = 2 that
                        # equilibrium is 2 x bar = 12-14 titanium against a
                        # collar asking 18-24.
                        #
                        # ⛔⛔ AND THE PREMISE THAT LICENSED THE REPAIR ALLOWANCE
                        # IS FALSE ON THIS CHASSIS.  Its stated argument is "a
                        # sentinel only exists once the collar was CLOSED, so
                        # what the collar still needs at KILL is a REPAIR
                        # allowance, not a fresh collar".  That was true under
                        # v513's salt-only gate.  It stopped being true at v515,
                        # whose GATE_OR eco disjunct buys a sentinel with the
                        # collar OPEN -- `FS_PH_KILL_OPEN` exists for exactly
                        # that state -- and at v516, whose GLOBALSENT beat arms
                        # this branch off turret LIVENESS with no closure term
                        # at all.  In both, the collar genuinely does still need
                        # a whole collar's worth of barriers and is being priced
                        # as if it did not.
                        #
                        # ⇒ WHILE A TURRET IS LIVE AND THE COLLAR IS KNOWN OPEN,
                        # THE FULL COLLAR PRICE IS HELD BACK -- the `8 * bar`
                        # the line four above already computed for this state.
                        # ⛔ NOTHING IS SPENT AND NO GATE IS OPENED: this is a
                        # RESERVE, it only ever RAISES a floor, and the moment
                        # the collar reads closed the repair allowance is back.
                        # The salt latch is what says "closed": `fs_ph` is the
                        # crew's shared published answer and SEALED/KILL both
                        # mean some body of ours saw the orthogonal-8 shut this
                        # round, while KILL_OPEN means it explicitly did not.
                        if LOKI_FS_V521 and FS_V521_COLLARFIRST \
                                and fs_ph not in (FS_PH_SEALED, FS_PH_KILL):
                            ti_floor = max(ti_floor,
                                           FS_V521_COLLAR_BARRIERS * bar
                                           + FS_SEAL_MARGIN)
                            if FS_V521_MAG_LOG:
                                try:
                                    print("MAG521", rnd, "ph", fs_ph, "ti", ti,
                                          "floor", ti_floor, "bar", bar,
                                          "ammo", ammo, file=sys.stderr)
                                except Exception:
                                    pass
                        if FS_MAG_TRACE:
                            print("MAG", rnd, "ti", ti, "ammo", ammo,
                                  "floor", ti_floor, "bar", bar,
                                  file=sys.stderr)
                    if LOKI_FS_SEAL_ONLY and LOKI_FS_RING_LADDER:
                        # ⛔⛔ THE SEAL-ONLY CLAUSE BELOW IS *NOT* SAFE ONCE THE
                        # RAIDER OWNS A SENTINEL, AND THE FIRST LADDER GRID
                        # MEASURED IT.  Under v511 the raider never bought a
                        # turret, so FS_PH_KILL was a rare state (3 sentinels in
                        # 30 games) and dropping the floor to 8 cost nothing.
                        # Under the ladder KILL is the DOMINANT state, and a
                        # floor of 8 means the core converts every titanium
                        # above 8 into ammunition while the collar is still
                        # open: the 30-game v512 grid read `ti 8` on STAT line
                        # after STAT line, the seal gate (`need * bar + 6`)
                        # never cleared, and orthogonal-8 closures fell 9/30 ->
                        # 1/30 while shots on their core rose 84 -> 1,187.  We
                        # were out-shooting a defender who simply healed it back
                        # (5,761 on-core heals against 1,076).  A COLLAR IS
                        # WORTH MORE THAN A MAGAZINE: hold the eight barriers
                        # back and let ammunition have everything above them --
                        # which is the ORIGINAL non-seal-only line, restored
                        # here for the arm that has an offensive turret again.
                        #
                        # ⭐ AND ONE HOLD-BACK ON TOP, NARROW ON PURPOSE: Magnus
                        # asked for TWO sentinels and rung 4 buys the second out
                        # of this bank.  A sentinel-sized floor at KILL is the
                        # shape of the autopsy's magazine lock (398 rounds at 2
                        # ammo), so it engages only once the magazine is already
                        # HALF FULL -- 150 ammunition is 15 sentinel shots, more
                        # than the plank can burn before the bank refills.
                        # ⭐⭐ v517 CHANGE 2b -- THE FUNDING LINK.  The
                        # `ammo >= 150` precondition exists so the hold-back
                        # cannot starve a magazine the sentinel is burning.  A
                        # HOLDING sentinel is not burning it, which is the one
                        # state where the precondition is provably vacuous --
                        # and the smoke grid measured the bank PINNED AT 16 for
                        # 25 consecutive rounds of a live hold because of it
                        # (TWINGATE517 r207-231, ammo cycling 12->8->4->0 into
                        # OTHER turrets).  Without this line change 1 saves
                        # ammunition and funds nothing.
                        if ammo >= FS_AMMO_TARGET // 2 \
                                or self._v517_bank_open(ct):
                            try:
                                if ct.read_store(SLOT_FWD_GUN) < FS_SENTINEL_MAX:
                                    ti_floor = max(ti_floor,
                                                   sen + FS_SENTINEL_TI_FLOOR)
                            except Exception:
                                pass
                        # ⭐⭐ v518 CHANGE 3 -- THE TWIN RESERVE, PRICED AT THE
                        # PURCHASE'S OWN BAR AND GATED ON LIVENESS.  See
                        # `_v518_twin_reserve` for the two arithmetic defects in
                        # the v517 reserve above that this replaces (it is
                        # priced sen+4 against a bar of sen+2*bar, and it reads
                        # the MONOTONE SLOT_FWD_GUN for a liveness question).
                        # ⛔ COMPOSES, DOES NOT REPLACE: it enters through
                        # max(), so with FS_V518_TWINRES off every other floor
                        # -- E1_AMMO_FLOOR, the harvester reserve, the collar
                        # reserve, v517's own -- is exactly what it was.
                        if LOKI_FS_V518 and FS_V518_TWINRES:
                            _v518_res = self._v518_twin_reserve(ct, sen, bar)
                            if _v518_res > ti_floor:
                                self.v518_res_bind += 1
                                ti_floor = _v518_res
                            if FS_V518_RES_LOG and _v518_res:
                                try:
                                    print("TWINRES518", rnd, "ti", ti,
                                          "ammo", ammo, "sen", sen, "bar", bar,
                                          "res", _v518_res, "floor", ti_floor,
                                          "bind", self.v518_res_bind,
                                          "rounds", self.v518_res_rounds,
                                          "until", self.v518_res_until,
                                          file=sys.stderr)
                                except Exception:
                                    pass
                    elif LOKI_FS_SEAL_ONLY:
                        # ⛔ A LIVE ALIGNED SENTINEL CLEARS THE RESERVE
                        # OUTRIGHT.  Autopsy of the v510 demo: team ammo sat at
                        # 2 for 398 rounds while a proven-aligned sentinel stood
                        # silent and 19 shots would have won the game.  Once the
                        # turret exists, ammunition IS the clock and a barrier
                        # it is holding titanium for is worth less than a shot.
                        ti_floor = FS_AMMO_TI_FLOOR
                elif fs_ph == FS_PH_SEALED:
                    if LOKI_FS_SEAL_ONLY and LOKI_FS_RING_LADDER:
                        # ⛔ THE MAGAZINE LOCK, MIRRORED -- AND IT WOULD HAVE
                        # BEEN A NEW BUG, NOT AN INHERITED ONE.  v511's raider
                        # never bought a turret, so dropping the floor to 8 the
                        # moment the collar closed was free.  Under the ladder
                        # rung 4 buys a SENTINEL out of this bank, and a floor of
                        # 8 converts every titanium above it into ammunition for
                        # a turret that therefore never gets bought: a sealed
                        # collar, a full magazine and nothing to fire it.  Hold
                        # one sentinel's price back until one is standing (at
                        # which point the phase is KILL and the clause above
                        # takes over).
                        ti_floor = max(FS_AMMO_TI_FLOOR,
                                       sen + FS_SENTINEL_TI_FLOOR)
                    else:
                        ti_floor = min(ti_floor, FS_AMMO_TI_FLOOR)
                # ⛔ THIS RESERVE MUST STRICTLY EXCEED the raider's own seal
                # gate (`_fs_seal_ok`), or the two reserves deadlock against
                # each other on the same bank -- measured on the first
                # integrated run, where the seal sat a few titanium short of its
                # bar for the whole match and placed nothing.
                elif LOKI_FS_SEAL_ONLY:
                    # ⛔ RE-PRICED FOR SEAL-ONLY, AND THE OLD NUMBER WAS
                    # ARITHMETICALLY UNREACHABLE.  The v510 form prices
                    # `sentinel + 12 barriers + margin + 24`; the autopsy
                    # measured live scale at 2.58-3.08x (not the build report's
                    # 1.7-2.5), which puts that floor at 191-230 Ti against a
                    # bank that cleared 189 on 0 of 376 rounds -- i.e. ammunition
                    # conversion was OFF for the whole siege.  Reproduced here
                    # on midgard seed 21: `ammo 0` on every STAT line from r60
                    # to r940.  Under seal-only the two inflated terms are also
                    # simply WRONG: this raider never buys a SENTINEL, so the
                    # `sen` term prices a purchase that cannot happen.  What
                    # stays is the collar itself plus 6, which is the smallest
                    # figure that still STRICTLY EXCEEDS `_fs_seal_ok`'s own bar
                    # (`len(needed) * bar + FS_SEAL_MARGIN`, at most 12 tiles
                    # before the gate latches) -- the non-negotiable constraint,
                    # because two reserves that can meet on the same bank
                    # deadlock and a full match passed with zero barriers the
                    # first time that happened.
                    ti_floor = max(ti_floor, 12 * bar + FS_SEAL_MARGIN + 6)
                else:
                    ti_floor = max(ti_floor,
                                   sen + 12 * bar + FS_SEAL_MARGIN + 24)
            # ⭐⭐ v520 CHANGE 2 -- THE PRESENCE RESERVE.  Placed HERE, outside
            # every phase branch, because a ring seat can fall vacant in any
            # phase and the v513 measurement (median 90 rounds to replace, 0 of
            # 14 inside Magnus's ~15-round cap) is not a KILL-phase fact.
            # ⛔ COMPOSES, DOES NOT REPLACE: it enters through a `>` test on
            # `ti_floor`, i.e. max() semantics, so E1_AMMO_FLOOR, the harvester
            # reserve, the collar reserve and v517/v518's own floors are exactly
            # what they were.  It can only ever RAISE the bar `convert_ammo`
            # has to clear, and it is capped (FS_V520_PRES_CAP) so it cannot
            # become the magazine lock in a new costume.
            if LOKI_FS_V520 and FS_V520_PRESENCE:
                _v520_res = self._v520_presence_reserve(ct, rnd)
                if _v520_res > ti_floor:
                    self.v520_pres_bind += 1
                    ti_floor = _v520_res
                if FS_V520_PRES_LOG and _v520_res:
                    try:
                        print("PRES520", rnd, "ti", ti, "res", _v520_res,
                              "floor", ti_floor, "bind", self.v520_pres_bind,
                              "rounds", self.v520_pres_rounds,
                              "vacant", self.v520_pres_vacant,
                              "until", self.v520_pres_until, file=sys.stderr)
                    except Exception:
                        pass
            # ⭐ WAVE-LATE-SURGE (k) -- THE ECONOMY'S OWN RESERVE ON THE
            # MAGAZINE.  Composes exactly like every reserve above it: a
            # `max()` on `ti_floor`, so it can only RAISE the bar conversion
            # must clear and cannot lower E1_AMMO_FLOOR, the harvester
            # reserve, the collar reserve or v517/v518/v520's floors.  It
            # exists because none of those five represents the DIG, and the
            # decoded tape says the magazine took 620 Ti in 86 rounds while
            # the expanders stood still for want of eight.  Off before r250,
            # off the moment the ratchet reaches WAVE_SURGE_HARV_TARGET.
            if WAVE_LATE_SURGE and wave_surge_short(ct):
                if WAVE_SURGE_AMMO_FLOOR > ti_floor:
                    ti_floor = WAVE_SURGE_AMMO_FLOOR
            if (under or weapons_top or bb_live or fs_live or harv >= 2) \
                    and ammo < ammo_target and ti > ti_floor:
                amt = min(chunk, ammo_target - ammo, ti - ti_floor)
                # ⭐ v513: the minimum conversion drops to 1 while the siege is
                # live.  `convert_ammo` is action-free and costs the Core
                # nothing, and the 4-titanium minimum blocked 40 of 211 rounds
                # (19%) on the instrumented atoll game -- rounds in which the
                # bank was 1-3 titanium above the floor and the sentinel was
                # standing empty.  Outside the siege the incumbent number
                # stands.
                _min_amt = 1 if (LOKI_FS_CREW and FS_SALT_GATE
                                 and fs_live) else 4
                if amt >= _min_amt and ct.can_convert_ammo(amt):
                    ct.convert_ammo(amt)
                    if LOKI_FS_V518 and FS_V518_TIWATCH:
                        try:
                            print("TICONV518", rnd, "amt", amt,
                                  "floor", ti_floor, file=sys.stderr)
                        except Exception:
                            pass
                    ti = ct.get_global_resources()

        # --- population -----------------------------------------------------
        # The raid is a consumable and the cost scale is refunded when a body
        # dies (destroying an entity removes its contribution), so surplus bank
        # is turned into bodies instead of into tiebreak #3.
        units = ct.get_unit_count()
        if self.prev_units is not None and units < self.prev_units:
            self.lost_units += self.prev_units - units
        self.prev_units = units

        budget = LOKI_BASE_BUILDERS
        if harv >= 1 and ti >= LOKI_SURPLUS_TI:
            budget += LOKI_SURPLUS_EXTRA
        if ti >= LOKI_RICH_TI:
            budget += LOKI_RICH_EXTRA
        budget = min(budget, LOKI_MAX_BUILDERS)
        budget += min(REPLACEMENT_MAX, self.lost_units)

        # --- LOKI-FERRY-SIEGE: the three-builder opening and the raider
        # replacement.  ⛔ Both are applied with min(), never max(): this block
        # can only ever LOWER the incumbent curve, so a bug here starves the
        # opening rather than inflating it.
        if LOKI_FERRY_SIEGE_ON and self._fs_gate(ct):
            beat, ph, _rid = self._fs_state(ct)
            stale = (not beat) or (rnd - (beat - 1) > FS_BEAT_STALE)
            # ⛔⛔ v520 CHANGE 2 -- THE BUDGET DOOR WAS READING THE BROKEN BEAT.
            # This clause pays for a replacement body, and it computes `stale`
            # INLINE off SLOT_FS with FS_BEAT_STALE = 12 -- the shared slot
            # `raid.py:174/:191` refresh for ANY established body of ours, i.e.
            # exactly the defect `_fs_stale` diagnoses at siege.py:303-319 as
            # "backwards by construction".  v513 fixed the APPOINTMENT door to
            # read the dedicated crew bits (`main.py` further down) and left
            # this one on the old channel, so with the crew on a dead SUPPORT
            # was noticed by the door that hands out the seat and by NOTHING
            # that pays for the body.  Two doors, two beats, one of them wrong.
            if LOKI_FS_V520 and FS_V520_PRESENCE and FS_V520_PRES_SEATS:
                _seats = (0, 1) if fs_crew_on() else (0,)
                stale = any(self._fs_crew_age(ct, _s, rnd) > FS_CREW_STALE
                            and self.v520_pres_seen.get(_s)
                            for _s in _seats)
            if ph != FS_PH_DEGRADE:
                # RAIDER REPLACEMENT.  Jython runs ONE raider in 60/60 games and
                # never replaces it; Erebus v143 lost 69 rounds of offence to
                # the same defect while holding 470-620 Ti (AUTOPSY Finding 6).
                # Double-sourced, so it is worth the two bodies it can cost.
                # ⭐⭐ v527 M2(a) -- THE PURCHASE SURVIVES THE RAIDER.  Magnus,
                # markers 6 and 14: a SEALED enemy core with NO turret on it,
                # held for hundreds of rounds.  The clause that would buy it
                # (`_v518_early_sentinel`, above rung 1) is correct and funded;
                # `FS_MAX_REPLACE = 2` is a WHOLE-MATCH cap, so in the marker
                # games both replacements were long spent and THE CLAUSE HAD
                # NOBODY TO RUN IT.  ⇒ the cap is lifted by exactly
                # FS_V527_PSURV_EXTRA, and ONLY inside the state that names the
                # defect: the crew publishes a sealed-or-better collar, no
                # forward turret was EVER bought (`SLOT_FWD_GUN` is monotone
                # and survives the buyer), and no forward sentinel beat is
                # live.  Outside that state this expression is the parent's.
                _v527_cap = FS_MAX_REPLACE
                if LOKI_FS_V527 and FS_V527_PSURV and FS_V527_PSURV_DISPATCH \
                        and self._v527_psurv_state(ct, rnd):
                    _v527_cap += FS_V527_PSURV_EXTRA
                    if not getattr(self, "v527_psurv_seen", False):
                        self.v527_psurv_seen = True
                        self._v527_log("PSURV ARM", rnd, "ph", ph,
                                       "repl", self.fs_replaced,
                                       "cap", _v527_cap)
                if (stale and rnd >= FS_BEAT_STALE and self.n >= FS_OPEN_BUILDERS
                        and self.fs_replaced < _v527_cap
                        and rnd - self.fs_repl_rnd > FS_BEAT_STALE):
                    self.fs_replaced += 1
                    self.fs_repl_rnd = rnd
                    if self.fs_replaced > FS_MAX_REPLACE:
                        self.v527_psurv_n = \
                            getattr(self, "v527_psurv_n", 0) + 1
                        self._v527_log("PSURV DISPATCH", rnd,
                                       "repl", self.fs_replaced,
                                       "n", self.v527_psurv_n)
                # THE OPENING: three bodies, then stop until the raider is AT
                # the ring.  Jython's median builders by r30 is 3 against its
                # opponents' 5, and spawning resumes here the moment the siege
                # is on -- the economy still has to buy 280-560 ammunition.
                # The panic clause is the one thing that overrides it: a core
                # actually bleeding gets its bodies back regardless of phase,
                # because counter-siege is this plank's known killer.
                if ph <= FS_PH_FERRY and (ct.get_max_hp() - hp) < FS_PANIC_DMG:
                    # v513 change D: the opening is FOUR -- two eco, the sealer
                    # and the support -- and it is still applied with min(), so
                    # this clause can only lower the incumbent curve.
                    opening = (FS_CREW_OPEN_BUILDERS
                               if (LOKI_FS_CREW and fs_crew_on()
                                   and not FS_CREW_CONVERT)
                               else FS_OPEN_BUILDERS)
                    budget = min(budget, opening + self.fs_replaced)

        if ct.get_action_cooldown() != 0:
            return
        if self.n >= budget or units >= GameConstants.MAX_TEAM_UNITS - 2:
            return
        cost = ct.get_builder_bot_cost()
        # LOKI-FERRY-SIEGE COLLAR RESERVE, on the biggest spender on the board:
        # at our scale one body is 78-105 Ti, more than the whole collar.
        if LOKI_FERRY_SIEGE_ON and FS_SPAWN_RESERVE_ON:
            _fb, _fp, _fr = self._fs_state(ct)
            if FS_PH_RING <= _fp <= FS_PH_KILL and _fb \
                    and rnd - (_fb - 1) <= FS_BEAT_STALE:
                cost += 8 * ct.get_barrier_cost() + FS_SEAL_MARGIN
        # The opening five are unconditional (the incumbent's shipped curve);
        # anything above them keeps a reserve so a body never starves the
        # first harvesters.
        need = cost if self.n < LOKI_BASE_BUILDERS else cost + LOKI_SPAWN_RESERVE
        # ⭐ WAVE-LATE-SURGE (h).  The same reserve idea the line below it
        # already encodes ("a body never starves the first harvesters"),
        # re-priced for the round where the harvesters are the whole game.  At
        # the measured late scale a builder bot is 114 Ti -- dearer than a
        # harvester -- and adds +20% to the ONE global cost factor, so every
        # body bought here makes every later harvester dearer.  It never
        # touches the opening five (`self.n < LOKI_BASE_BUILDERS` keeps its
        # own branch) and it stands down the moment the ratchet is met.
        if (WAVE_LATE_SURGE and self.n >= LOKI_BASE_BUILDERS
                and wave_surge_short(ct)):
            need += WAVE_SURGE_SPAWN_RES
        if ti < need:
            return
        if self._spawn_ring_key != p:
            self._spawn_ring = ring(p, 2)
            self._spawn_ring_key = p
        cands = list(self._spawn_ring)
        # Stable dispersion, re-rolled once per match from OS entropy: units
        # coordinate against one fixed pattern for the whole game while
        # identical-key ladder games diverge from the first spawn.
        if not hasattr(self, "spawn_salt"):
            import random
            self.spawn_salt = random.Random().randrange(97) if NOISE_ON else 0
        cands.sort(key=lambda sp: ((sp.x * 17 + sp.y * 31 + self.n * 13 + self.spawn_salt) % 97,
                                   sp.y, sp.x))
        if LOKI_FS_CREW and FS_SPAWN_PURPOSE:
            # ⭐ v513 CHANGE H (Magnus): SPAWN THE BODY FACING ITS JOB.  The
            # seat this spawn is about to take is known here -- `self.n` is the
            # roster ordinal the new body will read out of SLOT_ROLE_N -- so a
            # raider seat is issued on the enemy-facing side of the ring and an
            # eco seat on the side its ore is.  MEASURED FIRST (autopsy, spawn
            # placement section): the raider seat is worth ~1 walk tile, which
            # the ferry mostly absorbs, and an eco seat +2.43 mean tiles -- NOT
            # the +10.5 the old chassis measured, so this is polish and the bar
            # it has to clear is "does not regress".  It re-orders the SAME
            # candidate list; the dispersion salt still breaks every tie.
            anchor = None
            # ⛔ v521 CHANGE 0 -- THE GATED-MAP LEAK, SITE 1 OF 2 (v520 open
            # item 7).  `fs_crew_on()` is a plank flag and this read site is
            # OUTSIDE the map gate, so on a board the ferry-siege refuses the
            # crew seat was still being handed an enemy-facing spawn tile.  The
            # Core has `self.core` by construction, so the gate is a plain call
            # here.  Seat 0 is untouched: it is the chassis' own raider on
            # every board, gate or no gate.
            _v521_crew_seat = fs_crew_on()
            if LOKI_FS_V521 and FS_V521_GATEFIX and _v521_crew_seat:
                _v521_crew_seat = bool(self._fs_gate(ct))
            if self.n == 0 or (_v521_crew_seat and self.n == fs_crew_seat()):
                anchor = unpack_pos(ct.read_store(SLOT_ENEMY_CORE))
                if anchor is None:
                    anchor = enemy_core_for(w, h, p)
            elif self.n in LOKI_ECO_SEATS:
                anchor = self._spawn_ore_anchor(ct, p)
            if anchor is not None:
                cands.sort(key=lambda sp: sp.distance_squared(anchor))
        for sp in cands:
            if not (0 <= sp.x < w and 0 <= sp.y < h):
                continue
            try:
                ok = ct.can_spawn(sp)
            except Exception:
                continue
            if ok:
                ct.spawn_builder(sp)
                self.n += 1
                return

    def _spawn_ore_anchor(self, ct, p):
        """The ore an eco seat should be spawned facing.  Cached per match.

        The Core already decodes the map once (`known_map_for`); this walks its
        rows with `str.find`, which is the same C scan `_builder` uses, and
        keeps the result for the rest of the game.  Nearest-to-core ore: the
        eco seats partition the deposits themselves once they are alive, so all
        this has to get right is the SIDE.
        """
        if getattr(self, "_spawn_ore_key", None) == (p.x, p.y):
            return self._spawn_ore
        best, best_d = None, None
        grid = self.map_grid
        if grid:
            for y, row in enumerate(grid):
                i = row.find("o")
                while i >= 0:
                    d = (i - p.x) ** 2 + (y - p.y) ** 2
                    if best_d is None or d < best_d:
                        best, best_d = Position(i, y), d
                    i = row.find("o", i + 1)
        self._spawn_ore_key = (p.x, p.y)
        self._spawn_ore = best
        return best

    # ------------------------------------------------------------------
    # builders
    # ------------------------------------------------------------------

    def _builder(self, ct):
        p = ct.get_position()
        if self.team is None:
            self.team = ct.get_team()
            self.mw, self.mh = ct.get_map_width(), ct.get_map_height()
            self.idx = ct.get_id() & 0xFF
            self.ang = (self.idx % 8) * (math.pi / 4)
            # v516 change 2: slot 0's low 10 bits are the role counter and bits
            # 10-20 are the forward-sentinel beat.  Both writers preserve the
            # other's field.  The mask is a NO-OP when the plank is off (the
            # counter never approaches 1023), so this line reproduces the
            # parent under LOKI_FS_V516 = False.
            n = ct.read_store(SLOT_ROLE_N) & FS_ROLE_N_MASK
            self.role_n = n
            ct.write_store(SLOT_ROLE_N,
                           (ct.read_store(SLOT_ROLE_N) & ~FS_ROLE_N_MASK)
                           | ((n + 1) & FS_ROLE_N_MASK))
            # ROSTER.  Seat 0 leaves at once -- the corpus says insertion only
            # buys survival at the destination BEFORE r150, so the earliest
            # body is the most valuable one.  Seats 1-2 are the economy, seat 4
            # is the single home defender, and every replacement joins the
            # raid (raid.py decides per round whether the raid is open).
            #
            # LOKI-2 COMMITTED OPENING.  Three turrets by r22 is more work
            # than one pair of hands can do -- a builder acts once a round and
            # has to walk between sites -- so inside the window every seat in
            # LOKI2_RUSH_SEATS leaves at once instead of just seat 0.  This is
            # an override AT THE POINT OF USE; LOKI_ECO_SEATS itself is never
            # mutated.  It sits BELOW the defend test on purpose: the home
            # defender is not part of this plank and keeps its seat even if
            # the two tuples were ever made to overlap.  The window is read
            # once, when this unit first runs, which is when the seat is
            # issued -- a seat handed out inside the window stays a raider.
            # ⛔ v521 CHANGE 0 -- THE GATED-MAP LEAK, SITE 2 OF 2, AND IT IS THE
            # ONE THAT COST THE ARCHIPELAGO CONTROL ITS MEANING.  This line
            # takes seat 3 OUT OF THE ECO POOL and makes it a raider; the FS
            # appointment further down is gated, but the SEAT is not, so on a
            # refused board seat 3 became an ordinary raider instead of the
            # economy expander it would otherwise have been.  That is a real
            # behaviour change on every gated map, and v520's own gated leg
            # measured it rather than the nothing it was designed to measure.
            #
            # ⛔ THE GATE NEEDS `self.core`, WHICH IS RESOLVED ~20 LINES BELOW.
            # The resolution is hoisted here rather than the roster block being
            # moved: same scan, same attribute, idempotent, and the
            # `if self.core is None: return` guard below stays exactly where it
            # is so a body that cannot see its Core still increments the role
            # counter in the round the parent increments it.
            _v521_seat3 = fs_crew_on()
            if LOKI_FS_V521 and FS_V521_GATEFIX and _v521_seat3 \
                    and n == fs_crew_seat():
                self._v521_core_resolve(ct)
                _v521_seat3 = bool(self._fs_gate(ct))
                if not _v521_seat3 and FS_V521_GATEFIX_LOG:
                    try:
                        print("GATEFIX521", ct.get_current_round(),
                              "seat", n, "id", ct.get_id(), file=sys.stderr)
                    except Exception:
                        pass
            if n == LOKI_DEFEND_SEAT:
                self.role = "defend"
            elif (LOKI_FS_CREW and _v521_seat3 and not FS_CREW_CONVERT
                    and n == fs_crew_seat()):
                # ⭐ v513 SEAT 3 IS THE SUPPORT RAIDER (autopsy #6/#8/#9).  Its
                # FS appointment happens further down, once the map gate is
                # computable; the seat is taken out of the eco pool here so a
                # body that the gate then refuses falls through to the ordinary
                # raid doctrine rather than to the economy it was never issued
                # for.  With FS_CREW_CONVERT the seat stays an expander and the
                # conversion happens at the gate instead.
                self.role = "raid"
            elif (
                LOKI2_RUSH_ON and n in LOKI2_RUSH_SEATS
                and ct.get_current_round() < LOKI2_RUSH_RND
            ):
                self.role = "raid"
            elif n in LOKI_ECO_SEATS:
                self.role = "expand"
            else:
                # ⭐ v539 RUNG B -- THE FAMINE DRAFT, AND IT IS THE HALF OF THE
                # PLANK NOTHING ELSE CAN DO.  Roles are assigned ONCE per body
                # off a monotone ordinal and only LOKI_ECO_SEATS = (1, 2, 3)
                # are economy, so a wipe that kills the three eco seats leaves
                # the team with NO EXPANDER for the rest of the match: every
                # replacement reads n >= 4 and lands here.  That, not the
                # ratchet, is why the measured famine never rebuilt.
                # ⛔ IT DIVERTS ONLY BODIES THAT HAVE NOT STARTED YET.  A
                # raider already walking the enemy ring keeps its role -- the
                # T4_BLEED lesson in this file, verbatim: recalling the whole
                # economy on a latch once finished a measured game with 0
                # titanium delivered.  And the diversion hands itself back the
                # moment delivery resumes (see the release below), so a
                # cleared famine costs the raid nothing but the walk home.
                # ⭐ WAVE-LATE-SURGE (e).  A body issued past WAVE_SURGE_RND
                # while the harvester ratchet is still under target joins the
                # economy instead of the raid.  ⛔ NEW BODIES ONLY -- a raider
                # already walking the enemy ring keeps its role, which is the
                # T4_BLEED lesson in doctrine.py verbatim (recalling the whole
                # economy on a latch once finished a game with 0 titanium
                # delivered).  Roles are assigned once per body at first run,
                # so a body issued before r250 is untouched by construction.
                if (WAVE_LATE_SURGE and WAVE_SURGE_SEATS
                        and wave_surge_short(ct)):
                    self.role = "expand"
                elif (LOKI_FS_V539 and FS_V539_REEST and FS_V539_DRAFT
                        and self._v539_famine(ct)):
                    self.role = "expand"
                    self.v539_drafted = True
                else:
                    self.role = "raid"
            if self.role == "raid":
                self.raid_slot = self._raid_seat_take(ct)

        if self.core is None:
            for eid in ct.get_nearby_buildings():
                try:
                    if ct.get_entity_type(eid) == EntityType.CORE and ct.get_team(eid) == self.team:
                        self.core = ct.get_position(eid)
                        break
                except Exception:
                    continue
        if self.core is None:
            return

        if self.map_grid is None:
            self.map_grid = known_map_for(self.mw, self.mh, self.core, ct)
            if self.map_grid is not None:
                # LOKI walked all 900 cells of a 30x30 grid twice in a Python
                # comprehension on this unit's FIRST TURN, which is where
                # loki_analysis.md 5.2 saw the first-turn spike.  str.find runs
                # the same scan in C and yields the same tiles in the same
                # row-major order, so map_ores keeps its order exactly.
                walls = set()
                ores = []
                for y, row in enumerate(self.map_grid):
                    i = row.find("#")
                    while i >= 0:
                        walls.add((i, y))
                        i = row.find("#", i + 1)
                    i = row.find("o")
                    while i >= 0:
                        ores.append(Position(i, y))
                        i = row.find("o", i + 1)
                self.map_walls = walls
                self.map_ores = ores

        rnd = ct.get_current_round()

        # --- sensing --------------------------------------------------------
        for eid in ct.get_nearby_entities():
            try:
                if ct.get_team(eid) == self.team:
                    continue
                et = ct.get_entity_type(eid)
                ep = ct.get_position(eid)
            except Exception:
                continue
            if et == EntityType.CORE:
                self.enemy = ep
                ct.write_store(SLOT_ENEMY_CORE, pack_pos(ep))
            d = self.core.distance_squared(ep)
            if (et in CORE_THREAT_TYPES and d <= 64) or (
                et == EntityType.BUILDER_BOT and d <= 16
            ):
                ct.write_store(SLOT_UNDER, 1)
                ct.write_store(SLOT_ATK_RND, rnd)
                ct.write_store(SLOT_THREAT, pack_pos(ep))
        if self.enemy is None:
            self.enemy = unpack_pos(ct.read_store(SLOT_ENEMY_CORE))

        self._sync_harvesters(ct)

        if self.last == p:
            self.stuck += 1
        else:
            self.stuck = 0
            self.wall = None
        self.last = p

        # ⭐ v539 RUNG B, SECOND HALF -- THE DRAFT RELEASES ITSELF.  A drafted
        # body is an expander ONLY while famine holds; the round the Core sees
        # titanium on the mouth again it goes back to the raid it was issued
        # for.  Without this the plank would quietly convert the whole roster
        # into economy over a match, which is the defence-at-the-kill's-expense
        # that PROGRAMME.md forbids.
        if (LOKI_FS_V539 and FS_V539_REEST and FS_V539_DRAFT
                and self.v539_drafted and self.role == "expand"
                and not self._v539_famine(ct)):
            self.v539_drafted = False
            self.role = "raid"
            self.raid_slot = self._raid_seat_take(ct)

        # SEAT 3 joins the raid once the harvester shell exists.  This is the
        # only role transition in the file and it is state-gated, not clocked.
        # ⭐ v539 RUNG C -- HELD SHUT DURING A FAMINE.  The condition it reads
        # is `SLOT_HARVESTERS >= ECO_NEED` on the RATCHET, i.e. on harvesters
        # that may all be dead; letting the last expander defect to the raid on
        # the strength of phantoms is how a wiped economy stays wiped.  ⛔ The
        # defection is HELD, never REVERSED: on a gated map seat 3 is the
        # ferry-siege support raider and pulling a body out of a live crew
        # mid-siege is a bigger change than this plank is allowed to be.
        if (
            self.role == "expand" and self.role_n == LOKI_LATE_RAID_SEAT
            and not self.link_queue and ct.read_store(SLOT_HARVESTERS) >= ECO_NEED
            and not (LOKI_FS_V539 and FS_V539_REEST and FS_V539_SEAT3_HOLD
                     and self._v539_famine(ct))
        ):
            self.role = "raid"
            self.raid_slot = self._raid_seat_take(ct)

        near_home = p.distance_squared(self.core) <= 25

        # UNIVERSAL ADJACENT HEAL.  Proximity work, not a role: any builder
        # standing beside a threatened Core repairs it before any other
        # short-circuit can claim the action.  can_heal() refuses a full-HP
        # Core, so the 1 Ti is only ever spent on real damage.
        if (near_home and ct.get_action_cooldown() == 0
                and ct.read_store(SLOT_UNDER) != 0
                and not (LOKI8_RAIDERS_STAY_OUT and self.role == "raid")):
            if not self._cb_over_heal(ct) and self._heal_core(ct):
                return

        # MELEE RECALL, RAIDERS ONLY.  A raider that has not left the home band
        # yet is the cheapest body to spend on an intruder.  Deliberately NOT
        # all-hands: an earlier revision recalled expanders too and it cost the
        # whole economy -- the trunk chain stalled at r16 and the game finished
        # with 0 titanium delivered, because SLOT_UNDER latches for 50 rounds
        # and every chain builder sits inside the band.
        if (near_home and self.role == "raid" and ct.read_store(SLOT_UNDER)
                and not LOKI8_RAIDERS_STAY_OUT):
            intruder = self._nearest_home_intruder(ct)
            if intruder is not None:
                self._home_defend(ct, intruder)
                return

        # Everything above is sensing and emergency defence.  If that alone
        # used the budget, skip the action/move phase rather than risk a
        # truncation mid-build inside it.
        if self._cpu_exhausted(ct):
            return

        self._wire_tick(ct)

        # --- LOKI-FERRY-SIEGE: who is THE RAIDER.  Decided here rather than in
        # the roster block above because the map gate needs `self.core`, which
        # is not resolved until a few lines up.  One-shot per unit.
        #
        # Seat 0 is the raider by construction -- the r0 spawn, the earliest
        # and therefore the most valuable body, and the seat the 2174-rated
        # implementation forks in 60/60 games.  The second door is the
        # REPLACEMENT: a body issued while the raider heartbeat is stale takes
        # over the plank.  That door is shut for the first FS_BEAT_STALE rounds
        # so the opening's own seats 1 and 2 cannot walk through it before the
        # raider has published its first beat.
        if LOKI_FERRY_SIEGE_ON and not self.fs_role_done:
            self.fs_role_done = True
            if self._fs_gate(ct):
                _b, _ph, _r = self._fs_state(ct)
                take = None
                if _ph != FS_PH_DEGRADE:
                    if self.role_n == 0:
                        take = "seal"
                    elif LOKI_FS_CREW and fs_crew_on() and (
                            (self.role_n == fs_crew_seat()
                             or (LOKI_FS_V520 and FS_V520_PROBE_DUAL_APPT
                                 and self.role_n == FS_V520_PROBE_SEAT2))
                            and (not FS_CREW_CONVERT
                                 or rnd >= FS_CREW_CONVERT_RND)):
                        # ⭐ THE SUPPORT BODY (v513 change D).  Seat 3, issued
                        # in the opening beside the sealer; verbs split so the
                        # two cannot compete for the same round (siege.py
                        # `_fs_supp_turn`).
                        take = "supp"
                    elif rnd >= FS_BEAT_STALE and self._fs_stale(ct, rnd):
                        take = "seal"          # the sealer is gone: replace it
                    elif (LOKI_FS_CREW and fs_crew_on()
                            and rnd >= FS_BEAT_STALE
                            and self._fs_crew_age(ct, 1, rnd) > FS_CREW_STALE
                            and self._fs_crew_age(ct, 0, rnd) <= FS_CREW_STALE):
                        # The sealer is alive and the support is not: a new body
                        # takes the support seat rather than duplicating the
                        # sealer's verb set.
                        take = "supp"
                # ⛔⛔ v520 CHANGE 1 -- THE DUAL-APPOINTMENT RACE, FIXED AT THE
                # LAYER IT LIVES ON.  The crewconv screen flagged it in 1 of 3
                # mechanism games: TWO LIVE UNITS BOTH HOLDING `fs_body == 2`,
                # both writing FS_SUPP_SLOT, the buffered store silently keeping
                # the higher entity id -- the r197 lost-update class one level
                # up.  v514 change D fixed the SLOT layer (one writer per slot);
                # nothing made the two SUPPORT doors above mutually exclusive,
                # and `self.fs_body = 2` below is set locally with no
                # arbitration.
                # THE FIX IS A CLAIM-AND-READBACK, which is idempotent by
                # construction: claim only a slot that is FREE (never reported,
                # or stale), then VERIFY on the next turn that the rid in it is
                # mine and stand down if it is not.  A silent winner becomes a
                # COUNTED loser, which is what makes the alarm able to fire.
                if take == "supp" and LOKI_FS_V520 and FS_V520_PINCER \
                        and FS_V520_APPT_GUARD:
                    _sb, _sp, _sr = self._fs_state_at(ct, FS_SUPP_SLOT)
                    if _sr and _sb and (rnd - (_sb - 1)) <= FS_CREW_STALE \
                            and (_sr - 1) != ct.get_id():
                        take = None          # occupied: do not duplicate it
                        if FS_V520_APPT_LOG:
                            try:
                                print("APPT520 BUSY", rnd, "id", ct.get_id(),
                                      "held", _sr - 1, file=sys.stderr)
                            except Exception:
                                pass
                # ⭐ v539 RUNG B, THIRD SITE -- AND IT IS THE ONE THE HARNESS
                # FOUND, NOT THE ONE THE DESIGN PREDICTED.  A drafted body was
                # correctly given `role = "expand"` at the roster block and
                # then CONVERTED STRAIGHT BACK by this appointment, which
                # overwrites any non-raid role when it fills a crew seat: the
                # unit-level probe read `role_n = 6, v539_drafted = True,
                # role = "raid"` -- the draft firing and being undone in the
                # same turn.  A body that has been drafted to re-establish the
                # economy is NOT ELIGIBLE for a ferry-siege seat while the
                # famine holds; it becomes eligible again the moment delivery
                # resumes and the draft releases it, so the crew loses a
                # candidate for the length of the episode and nothing more.
                if (LOKI_FS_V539 and FS_V539_REEST and FS_V539_DRAFT
                        and take is not None and self.v539_drafted
                        and self._v539_famine(ct)):
                    take = None
                if take is not None:
                    self.fs_raider = True
                    self.fs_role = take
                    if take == "supp" and LOKI_FS_V520 and FS_V520_PINCER \
                            and FS_V520_APPT_GUARD:
                        self.v520_appt_rnd = rnd
                        if FS_V520_APPT_LOG:
                            try:
                                print("APPT520 CLAIM", rnd, "id", ct.get_id(),
                                      file=sys.stderr)
                            except Exception:
                                pass
                    # v514 change D: the body identity that selects this unit's
                    # PUBLISH SLOT.  Fixed here, once, and NOT re-derived from
                    # fs_role afterwards -- a support that PROMOTEs must keep
                    # its own channel rather than start clobbering the
                    # sealer's, which is the r197 lost-update defect.
                    self.fs_body = 2 if take == "supp" else 1
                    if self.role != "raid":
                        self.role = "raid"
                        self.raid_slot = self._raid_seat_take(ct)

        # --- v513 CHANGE B: ANSWER THE TURRET AT OUR DOOR.  Ranked here, above
        # every eco verb and below the universal adjacent heal, because it is
        # the only home behaviour in this file that removes the damage source
        # rather than out-healing it: a converged healer is +4 HP a round
        # against a sentinel's -9, while ten rounds of two builders pecking
        # ends the sentinel for good.  The ferried raider never sees this
        # branch (it does not come home for anything).
        if self._door_turret_turn(ct, p, rnd):
            return

        # --- LOKI-V537 "SOCKET".  Ranked here: below every emergency (heal,
        # melee recall, door turret) and ABOVE every role dispatch, because
        # the thing it buys is a CLOCK.  Their first plug on our ring lands at
        # r13-r16 and the trunk's own ore-end-first drain reaches the seat at
        # r23 (drakkarfjord) / r230 (glacierkeep) / never (86% of glacierkeep),
        # so anything that can be out-ranked by an eco verb is too late.
        # Bounded to FS_V537_BY_ROUND and FS_V537_MAX_SOCKETS, so the most it
        # can ever cost the raid is two builder turns inside the first four
        # rounds.  Full block: doctrine.py, LOKI-V537.
        if FS_V537_SOCKET and self._v537_socket_claim(ct, rnd):
            return

        if self.fs_raider and not self.fs_off:
            self._fs_turn(ct)
        elif self.role == "raid":
            self._raid(ct)
        elif self.role == "defend":
            self._defend(ct)
        else:
            self._expand(ct)

    # ------------------------------------------------------------------
    # v513 CHANGE B -- THE DOOR-TURRET RESPONSE
    # ------------------------------------------------------------------

    def _door_turret(self, ct, p, rnd):
        """The enemy turret planted at OUR door, ranked by how much it is
        costing us right now.

        ⛔⛔ THIS IS THE #1 MEASURED KILLER AND WE ANSWERED IT ZERO TIMES.
        Across the 24-game v512 grid, ONE HUNDRED PERCENT of the 1,202 damage
        events on our own core came from enemy turrets sited nearer our core
        than theirs; 40 were planted, our builders attacked NONE of them, and 38
        of 40 were still standing at the end of the game.  Median warning from
        plant to our core's death: 56 rounds.  A sentinel is 40 HP and a builder
        peck is 2 damage for 2 titanium -- two bodies finish it in ten rounds,
        and the bank held the titanium every time.

        Returns (position, rank) or None.  Rank 0 = it is aligned on a core tile
        AND our core is bleeding, 1 = aligned, 2 = merely present (a launcher
        counts as aligned: its throw is facing-independent, and its target is
        our builders).
        """
        best, best_k = None, None
        try:
            tiles = core_tiles(self.core)
            bleeding = ct.read_store(SLOT_HEAL_BUDGET) > 0
        except Exception:
            return None
        for bid in ct.get_nearby_buildings():
            try:
                if ct.get_team(bid) == self.team:
                    continue
                kind = ct.get_entity_type(bid)
                if kind not in FS_DOOR_TYPES:
                    continue
                gp = ct.get_position(bid)
            except Exception:
                continue
            d = dsq_core(gp, self.core)
            if d > FS_DOOR_DSQ:
                continue
            aligned = kind == EntityType.LAUNCHER
            if not aligned:
                try:
                    gd = ct.get_direction(bid)
                    for t in tiles:
                        if ct.can_fire_from(gp, gd, kind, t):
                            aligned = True
                            break
                except Exception:
                    aligned = False
            rank = (0 if (aligned and bleeding) else (1 if aligned else 2))
            k = (rank, d)
            if best_k is None or k < best_k:
                best, best_k = gp, k
        if best is None:
            return None
        return best, best_k[0]

    def _door_turret_turn(self, ct, p, rnd):
        """Answer the door turret: peck it if we are beside it, else walk.

        ⭐ THIS DELIBERATELY PIERCES LOKI_QUIET_ON, and the precedent is the
        same property that earned the conveyor carve-out (doctrine.py:1744) and
        FS_CLEAR_RING_ON theirs: quiet exists because 2 damage a round buys
        nothing against a 500 HP core, and a 40 HP sentinel is the object where
        2 damage a round FINISHES.  The carve-out is the narrowest that can
        work -- enemy turrets only, inside FS_DOOR_DSQ of our own core, home
        crew only, and time-capped so one body cannot spend the match chasing
        one turret.
        """
        # ⭐ v515 CHANGE 1 -- THE DOOR RESPONSE SHIPS OFF, DECIDED HERE.
        # Evaluated at the READ site rather than as a doctrine-level derived
        # default, because `mkarm.sh` appends flag overrides to the end of
        # doctrine.py and a derived default is therefore order-dependent: the
        # first encoding left the door OFF in an arm that had set
        # `LOKI_FS_V515 = False`, so the master flag did not reproduce the
        # parent.  Two flags, read at run time, no assignment order involved.
        if not (LOKI_FS_CREW and FS_HOME_TURRET_RESPONSE):
            return False
        if LOKI_FS_V515 and FS_V515_DOOR_OFF:
            return False
        if self.core is None or self.fs_raider:
            return False
        if self.role not in ("expand", "defend"):
            return False
        try:
            if ct.get_global_resources() < FS_DOOR_TI_FLOOR:
                return False
        except Exception:
            return False
        found = self._door_turret(ct, p, rnd)
        if found is not None and self.fs_door_tgt != (found[0].x, found[0].y):
            self._fs_log("DOORSEEN", rnd, "id", ct.get_id(),
                         "at", (found[0].x, found[0].y), "rank", found[1])
        tgt = None
        if found is not None:
            tgt, rank = found
            key = (tgt.x, tgt.y)
            if self.fs_door_tgt != key:
                self.fs_door_tgt, self.fs_door_since = key, rnd
            # ⛔ ANTI-TREADMILL.  The kill needs ten rounds of pecking, not
            # forty; a body that has been on one turret this long is either
            # being out-healed or cannot reach it, and the economy is worth
            # more than a stalemate.
            if rnd - self.fs_door_since > FS_DOOR_MAX_RNDS:
                return False
            if rank >= 2 and abs(tgt.x - p.x) + abs(tgt.y - p.y) > 1:
                return False              # present but not aimed: not worth a walk
        else:
            # ⭐ THE BEACON.  A builder sees r^2 = 20 and the door turrets sit
            # at d^2 4-37 from our core, so the body that has to answer one is
            # routinely blind to it.  SLOT_THREAT already carries the position
            # the CORE (vision r^2 = 36) last saw a threat at -- the walk is
            # taken on that, and the ATTACK is never taken on it: firing only
            # ever happens against a turret this unit has confirmed in vision
            # above, so a beacon pointing at an enemy BUILDER cannot turn into
            # a peck at the wrong object.
            self.fs_door_tgt = None
            if ct.read_store(SLOT_UNDER) == 0:
                return False
            beacon = unpack_pos(ct.read_store(SLOT_THREAT))
            if beacon is None or dsq_core(beacon, self.core) > FS_DOOR_DSQ:
                return False
            if ct.read_store(SLOT_HEAL_BUDGET) <= 0:
                return False
            if ct.get_move_cooldown() == 0 and p.distance_squared(beacon) > 2:
                self.tgt = beacon
                self._nav(ct, pave=False)
                return True
            return False
        if ct.get_action_cooldown() == 0 \
                and abs(tgt.x - p.x) + abs(tgt.y - p.y) == 1:
            try:
                if ct.can_fire(tgt):
                    ct.fire(tgt)
                    self.fs_door_pecks += 1
                    self._fs_log("DOOR", rnd, "id", ct.get_id(),
                                 "at", (tgt.x, tgt.y), "n", self.fs_door_pecks)
                    return True
            except Exception:
                return False
        if ct.get_move_cooldown() == 0:
            self.tgt = tgt
            self._nav(ct, pave=False)
            return True
        return False

    # ------------------------------------------------------------------
    # home defence
    # ------------------------------------------------------------------

    def _nearest_home_intruder(self, ct):
        p = ct.get_position()
        best, best_d = None, None
        for eid in ct.get_nearby_units():
            try:
                if ct.get_team(eid) == self.team:
                    continue
                if ct.get_entity_type(eid) != EntityType.BUILDER_BOT:
                    continue
                ep = ct.get_position(eid)
            except Exception:
                continue
            if self.core.distance_squared(ep) > 36:
                continue
            d = p.distance_squared(ep)
            if best_d is None or d < best_d:
                best, best_d = ep, d
        return best

    def _home_defend(self, ct, intruder):
        if ct.get_action_cooldown() == 0:
            if self._sabotage_prio(ct):
                return
            if self._heal_adjacent(ct):
                return
            if self._heal_core(ct):
                return
        if ct.get_move_cooldown() == 0:
            self.tgt = intruder
            self._nav(ct, pave=False)

    def _sabotage_prio(self, ct):
        """Melee the best adjacent enemy building (2 Ti for 2 damage)."""
        p = ct.get_position()
        px, py = p.x, p.y
        best, best_p = None, 99
        for dx, dy in CARD_DELTAS:
            tx, ty = px + dx, py + dy
            if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                continue
            t = Position(tx, ty)
            try:
                bid = ct.get_tile_building_id(t)
                if bid is None or ct.get_team(bid) == self.team:
                    continue
                et = ct.get_entity_type(bid)
            except Exception:
                continue
            pr = SABOTAGE_PRIO.get(et, 6)
            if pr >= best_p:
                continue
            try:
                if ct.can_fire(t):
                    best_p, best = pr, t
            except Exception:
                continue
        if best is not None:
            if LOKI_QUIET_ON:
                return False          # QUIET: counterbattery melee silenced
            ct.fire(best)
            return True
        return False

    def _cb_over_heal(self, ct):
        """May the defender skip a heal to buy a counterbattery this round?

        Only in the one state where healing provably cannot win: the defender,
        a threat inside the home band, no live home turret, and a bank that
        pays for a Sentinel without touching the siege reserve.
        """
        if not CB_OVER_HEAL_ON or self.role != "defend" or self.core is None:
            return False
        threat = unpack_pos(ct.read_store(SLOT_THREAT))
        if threat is None:
            return False
        if dsq_core(threat, self.core) > HUNT_BAND_DSQ:
            return False
        if ct.get_global_resources() < ct.get_sentinel_cost() + SIEGE_HEAL_RESERVE_TI:
            return False
        return not self._live_home_gun(ct)

    def _try_counterbattery(self, ct):
        """Build only a weapon ray that already contains the reported threat."""
        threat = unpack_pos(ct.read_store(SLOT_THREAT))
        if threat is None:
            return False
        if dsq_core(threat, self.core) > HUNT_BAND_DSQ:
            return False
        if ct.read_store(SLOT_HARVESTERS) < ECO_NEED and self._live_home_gun(ct):
            # ...unless the Core is provably bleeding.  Real damage is not
            # opening noise, and holding the counterbattery shut through a
            # genuine shelling finished a measured game with zero turrets.
            if not self._core_shelled(ct):
                return False
        p = ct.get_position()
        px, py = p.x, p.y
        ban = self._seat_ban()
        choices = (
            (EntityType.SENTINEL, ct.get_sentinel_cost()),
            (EntityType.GUNNER, ct.get_gunner_cost()),
        )
        for turret_type, cost in choices:
            if ct.get_global_resources() < cost:
                continue
            for dx, dy in CARD_DELTAS:
                if self._cpu_exhausted(ct):
                    return False
                bx, by = px + dx, py + dy
                if not (0 <= bx < self.mw and 0 <= by < self.mh):
                    continue
                # A turret is impassable, so one planted on a heal seat costs
                # that seat's +4 HP/round for the rest of the match.
                if ban is not None and (bx, by) in ban:
                    continue
                bp = Position(bx, by)
                for facing in DIRECTIONS:
                    try:
                        if not ct.can_fire_from(bp, facing, turret_type, threat):
                            continue
                        if turret_type == EntityType.SENTINEL:
                            ok = ct.can_build_sentinel(bp, facing)
                        else:
                            ok = ct.can_build_gunner(bp, facing)
                    except Exception:
                        continue
                    if not ok:
                        continue
                    if turret_type == EntityType.SENTINEL:
                        ct.build_sentinel(bp, facing)
                    else:
                        ct.build_gunner(bp, facing)
                    ct.write_store(SLOT_HOME_GUN, ct.read_store(SLOT_HOME_GUN) + 1)
                    return True
        return False

    def _try_build_launcher(self, ct):
        # LOKI-42 LAUNCHER DEFERRAL -- the likely SHIPPABLE form of whatever
        # LAUNCH0 is measuring, built before the decomposition lands because it
        # is the one arm that helps under the good outcome and is inert under
        # the bad one.
        # THE COST WE ACTUALLY PAY, and it is not the 20 Ti: each launcher adds
        # +10% to the ONE GLOBAL ADDITIVE scale factor, which inflates EVERY
        # subsequent build of EVERY type -- harvesters, conveyors, turrets --
        # for the rest of the match. Bought at r10 that surcharge is levied on
        # the entire game; bought at r150 it is levied on the tail only.
        # We build ~1.17 launchers/game against five of the six teams above us
        # at essentially ZERO, so this is a premium nobody else pays.
        # ⇒ If LAUNCH0's gain is the PREMIUM, deferral captures most of it while
        # KEEPING the mechanism EXILE0 says is worth ~+3pp. If LAUNCH0's gain is
        # the FERRY, this changes nothing and reads null -- which is a clean
        # answer rather than a wasted arm.
        # ⚠ NOT a free lunch: deferring also delays the ferry, and early exile
        # is our cheapest home defence. The dose is SWEPT because I do not know
        # where that trade turns over, and a knob picked after seeing the result
        # is a fit rather than a mechanism.
        if ct.get_current_round() < LAUNCHER_MIN_RND:
            return False
        """One Launcher, near home.  ~70% of all launcher activity in the field
        is defensive disposal and ours is ~97% defensive -- so this is bought
        as home defence first and as the raid ferry second."""
        seen_launcher = False
        for eid in ct.get_nearby_buildings():
            try:
                if ct.get_team(eid) == self.team and ct.get_entity_type(eid) == EntityType.LAUNCHER:
                    seen_launcher = True
                    break
            except Exception:
                continue
        if ct.read_store(SLOT_LAUNCHER):
            if seen_launcher:
                return False
            if not LOKI6_LAUNCHER_RELEASE:
                return False
            # FIX 3. The slot is set but the Core -- which sits beside where the
            # home launcher is built -- can no longer see one. Release the latch
            # so the ferry and our cheapest home defence can be rebuilt. Without
            # this, one launcher death removes both for the rest of the match.
            ct.write_store(SLOT_LAUNCHER, 0)
        elif seen_launcher:
            ct.write_store(SLOT_LAUNCHER, 1)
            return False
        if ct.read_store(SLOT_HARVESTERS) < 1:
            return False
        if not self._eco_spendable(ct, ct.get_launcher_cost() + LAUNCHER_RESERVE):
            return False
        ct.write_store(SLOT_LAUNCHER, 1)  # claim before build so peers skip
        p = ct.get_position()
        px, py = p.x, p.y
        # Launchers are bot-impassable: never seat one on the eight
        # Core-orthogonal heal seats, delivery termini included.
        lban = self._home_seat_keys_set()
        for dx, dy in CARD_DELTAS:
            bx, by = px + dx, py + dy
            if (bx, by) in lban:
                continue
            if not (0 <= bx < self.mw and 0 <= by < self.mh):
                continue
            try:
                bp = Position(bx, by)
                if ct.can_build_launcher(bp):
                    ct.build_launcher(bp)
                    return True
            except Exception:
                continue
        ct.write_store(SLOT_LAUNCHER, 0)  # build failed -- release the claim
        return False

    def _home_seat_keys_set(self):
        """{(x, y)} of our own eight heal seats -- a fixed set, cached."""
        if self.core is None or not (self.mw and self.mh):
            return frozenset()
        key = (self.core, self.mw, self.mh)
        if self._home_seat_key != key:
            self._home_seat_keys = frozenset(
                (s.x, s.y) for s in heal_seats(self.core, self.mw, self.mh)
            )
            self._home_seat_key = key
        return self._home_seat_keys

    def _defend(self, ct):
        under = ct.read_store(SLOT_UNDER) != 0
        if ct.get_action_cooldown() == 0:
            if self._sabotage_prio(ct):
                return
            if under and self._try_counterbattery(ct):
                return
            if self._try_build_launcher(ct):
                return
            if under and self._heal_core(ct):
                return
        if under and ct.get_move_cooldown() == 0:
            shelled = self._core_shelled(ct)
            # T4 SEAT FIRST.  `can_fire()` is False on a tile holding an enemy
            # builder -- builders cannot touch builders -- so while the Core is
            # BLEEDING the chase below buys nothing at all and a free seat buys
            # +4 HP/round for 1 Ti.  Decoded: this defender and an enemy builder
            # two-cycled in lockstep for 46 rounds, r51-r96, with four seats
            # empty and the Core going 403 -> 0.  At full HP the chase is still
            # our cheapest disruption, so the swap is gated on real damage.
            if T4_SEAT_FIRST_ON and shelled:
                # Already on a seat: HOLD.  The action phase above healed if it
                # could; if it was on cooldown, moving off now throws away next
                # round's +4 as well.
                p = ct.get_position()
                if (p.x, p.y) in self._home_seat_keys_set():
                    return
                seat = self._seat_seek_target(ct)
                if seat is not None:
                    self.tgt = seat
                    self._nav(ct, pave=False)
                    return
            intruder = self._nearest_home_intruder(ct)
            if intruder is not None and self._t4_chase_ok(ct):
                self.tgt = intruder
                self._nav(ct, pave=False)
                return
            if shelled:
                seat = self._seat_seek_target(ct)
                if seat is not None:
                    self.tgt = seat
                    self._nav(ct, pave=False)
                    return
        # Nothing to defend against: the defender is an expander with a beat.
        self._expand(ct)

    def _t4_chase_ok(self, ct):
        """May we spend this move chasing an intruding builder?

        A pursuit confined to one or two tiles for T4_CHASE_MAX_RNDS
        consecutive rounds is a lockstep, not a pursuit: both bodies step the
        same way every round and neither can ever act on the other, because
        `can_fire()` is False on a builder.  The decoded case alternated
        (0,8)/(0,9) forever, so the test is on the SET of tiles held over the
        window, not on standing still.  Bank the chase for T4_CHASE_COOLDOWN
        rounds and let the rest of `_defend` -- seats, launcher, expansion --
        have the turn.
        """
        if not T4_CHASE_BREAK_ON:
            return True
        rnd = ct.get_current_round()
        if rnd < self.t4_chase_until:
            return False
        p = ct.get_position()
        hist = self.t4_chase_pos
        if hist is None or self.t4_chase_since != rnd - 1:
            hist = []
            self.t4_chase_pos = hist
        self.t4_chase_since = rnd
        hist.append((p.x, p.y))
        if len(hist) > T4_CHASE_MAX_RNDS:
            del hist[0]
        if len(hist) >= T4_CHASE_MAX_RNDS and len(set(hist)) <= 2:
            self.t4_chase_until = rnd + T4_CHASE_COOLDOWN
            self.t4_chase_pos = None
            self.t4_chase_since = None
            return False
        return True

    # ------------------------------------------------------------------
    # turrets
    # ------------------------------------------------------------------

    def _turret(self, ct):
        if self.team is None:
            self.team = ct.get_team()
            self.mw, self.mh = ct.get_map_width(), ct.get_map_height()
        p = ct.get_position()
        turret_type = ct.get_entity_type()

        # ⭐⭐ v516 CHANGE 2 -- THE FORWARD SENTINEL PUBLISHES ITS OWN LIVENESS.
        # The phase machine and the siege magazine were computed from
        # `_fs_live_sentinels`, a count off the ASKING BODY'S VISION -- and the
        # asking body is the raider, which is dead in 63.4% of the rounds a
        # sentinel of ours is actually hitting their core (autopsy #1).  The
        # magazine was armed in 21.2% of those rounds; median ammo under a
        # firing turret was 5 against 20 with nothing to shoot.
        # ⛔ THE MANDATE'S FIRST DESIGN IS FORBIDDEN BY THE ENGINE, PROBED
        # BEFORE BUILDING: `get_hp(id)` and `get_position(id)` RAISE GameError
        # for any entity outside the caller's vision, indistinguishably from a
        # destroyed id (471/471 out-of-vision probes raised, with a positive
        # control in the same tape at r2, dsq 4, hp 40).  There is no id-based
        # liveness channel.  A turret is a UNIT, so it runs every round it
        # lives and stops the round it dies -- it is its own heartbeat.
        # ⛔ A BEAT, NOT A COUNT: two sentinels writing one buffered slot in one
        # round is a lost update, but both write the IDENTICAL value here, so
        # the collision is harmless.  The beat answers ">= 1 live forward
        # sentinel" and deliberately cannot inflate the purchase cap.
        # ⛔ THE HOLD IS RE-DECIDED EVERY ROUND, NEVER INHERITED.  `_E` can read
        # None transiently (nothing has published the enemy anchor yet), which
        # skips the tick; without this reset the turret would carry last
        # round's decision into a round it did not measure.
        if LOKI_FS_V517 and FS_V517_FIREDISC:
            self.v517_hold_now = False
        if LOKI_FS_V516 and FS_V516_GLOBALSENT \
                and turret_type == EntityType.SENTINEL:
            try:
                _E = unpack_pos(ct.read_store(SLOT_ENEMY_CORE))
                # ⛔ GATED MAPS MUST NOT MOVE.  The beat is read by the Core's
                # magazine, and on a map the ferry-siege REFUSES (FS_MAP_SKIP /
                # the small-board gate) the bot plays the incumbent raid
                # doctrine -- which also plants forward sentinels.  Without
                # this test a gated game would start arming the siege magazine,
                # which is a change to play the siege leg cannot see and the
                # archipelago control is supposed to catch.  `enemy_core_for`
                # is an involution, so it recovers OUR anchor from theirs with
                # no store slot; `_fs_gate` then caches per unit.
                # ⛔ AND IT MUST NOT SET `self.core`.  `_fs_gate` reads that
                # attribute, but a turret's `self.core` is None by design and
                # `_door_turret_turn` returns early ON THAT NULL -- filling it
                # in here would silently re-open the door path this line has
                # nothing to do with.  The gate is asked with explicit anchors
                # instead (`_fs_map_gated`), which is the same three tests with
                # no shared state.  ⭐ v524 CHANGE 1: `ct` is now passed too, so
                # the exact-match confirm on a colliding cripple signature can
                # resolve `self.map_grid` here (it never gets set for a
                # turret otherwise) -- `self.map_grid` is NOT `self.core`, so
                # this does not touch the guard the paragraph above protects.
                _ours = (enemy_core_for(self.mw, self.mh, _E)
                         if (_E is not None and self.mw and self.mh) else None)
                if _E is not None and _ours is not None \
                        and self._fs_map_gated(self.mw, self.mh, _ours, _E, ct) \
                        and dsq_core(p, _E) <= FS_SENT_BEAT_DSQ:
                    _rnd = ct.get_current_round()
                    _cur = ct.read_store(SLOT_SENT_BEAT)
                    # ⭐⭐ v517 CHANGE 1 -- THE SAME WRITE CARRIES THE
                    # FIRE-DISCIPLINE CHANNEL.  `_v517_sent_tick` measures the
                    # enemy core's HP with this turret's own eyes, advances the
                    # net-damage window, decides this round's fire, and returns
                    # the bits it contributes to the v517 fields (21-31) while
                    # PRESERVING the other half of a twin's fields out of
                    # `_cur`.  With the flag off the expression below is the
                    # parent's, character for character.
                    # ⚠ DEPENDENCY, DOCUMENTED RATHER THAN HIDDEN: the channel
                    # rides the GLOBALSENT beat write, so FS_V517_FIREDISC is
                    # only reachable while FS_V516_GLOBALSENT is True.  Both
                    # ship True; the v517 mutant is FS_V517_FIREDISC = False,
                    # which is inside this block and reproduces the parent.
                    _v517bits = 0
                    if LOKI_FS_V517 and FS_V517_FIREDISC:
                        _v517bits = self._v517_sent_tick(ct, _E, p, _rnd, _cur)
                    ct.write_store(
                        SLOT_SENT_BEAT,
                        (_cur & FS_ROLE_N_MASK)
                        | (((_rnd + 1) & FS_SENT_BEAT_MASK)
                           << FS_SENT_BEAT_SHIFT)
                        | _v517bits)
                    if FS_GLOBALSENT_LOG:
                        print("SENTBEAT", _rnd, "at", (p.x, p.y),
                              "dopp", dsq_core(p, _E), file=sys.stderr)
            except Exception:
                pass

        # ⛔ FORCED-DEATH PROBE (v514 change B verification).  DEFAULT OFF and
        # it must stay off in every shipped configuration: it makes one of our
        # own forward sentinels self-destruct so the RESITE path can be driven
        # on demand.  A sentinel is a building with its own turn, and
        # self_destruct() is self-only, so this is the cheapest possible
        # forced-death instrument -- no adjacency, no bank, no opponent needed.
        if FS_PROBE_SENT_SUICIDE and turret_type == EntityType.SENTINEL:
            try:
                _E = unpack_pos(ct.read_store(SLOT_ENEMY_CORE))
                if _E is not None and dsq_core(p, _E) <= 40 \
                        and ct.get_current_round() >= FS_PROBE_SENT_RND:
                    print("PROBE SENTSUICIDE", ct.get_current_round(),
                          "at", (p.x, p.y), file=sys.stderr)
                    ct.self_destruct()
            except Exception:
                pass

        # LOKI-BELTBREAK.  A gunner STANDING IN THE ANNULUS is a beltbreaker,
        # whoever built it -- there is no per-unit tag to inherit, because the
        # builder that planted it has a different Player instance.  Position is
        # the tag, and it is the honest one: the band is what makes the role
        # (across 3,662 in-band gunners the core share of shots is 0.000, so a
        # gunner here is an economy shredder whether it meant to be or not).
        # Home counter-battery gunners sit at HUNT_BAND_DSQ=41 of OUR core and
        # never match, so this branch cannot capture them.
        if LOKI_BELTBREAK_ON and turret_type == EntityType.GUNNER \
                and self._bb_in_band(ct, p):
            self._bb_turret(ct, p)
            return

        if turret_type == EntityType.GUNNER:
            try:
                tgt = ct.get_gunner_target()
                if tgt is not None and ct.can_fire(tgt):
                    bid = ct.get_tile_building_id(tgt)
                    bot = ct.get_tile_builder_bot_id(tgt)
                    hostile = (
                        (bid is not None and ct.get_team(bid) != self.team)
                        or (bot is not None and ct.get_team(bot) != self.team)
                    )
                    if hostile:
                        ct.fire(tgt)
                        return
            except Exception:
                pass

        # Sentinels pierce intervening units, so scan the whole line.  Never
        # take the FIRST occupied tile out of get_attackable_tiles(): that
        # enumeration is row-major in absolute coordinates, so a "first hit
        # wins" scan engages the farthest enemy at four facings and the nearest
        # at the other four.  Priority is geometric/typed instead.
        # ⭐⭐ v517 CHANGE 1, THE ACTING END.  While the discipline is holding,
        # an enemy CORE tile stops being a target and everything else is
        # unchanged.
        # ⛔ THE HOLD IS SCOPED TO THE CORE SHOT, NOT TO FIRING.  Suppressing
        # every shot would also suppress fire at the HEALER, which is the one
        # thing 18 damage is unambiguously well spent on in a heal-matched
        # state (a builder has 40 HP, so two sentinel shots remove one).  The
        # measured defect is 10 ammo/shot poured into a 100.0% heal-back on the
        # CORE; that is exactly what this skips and no more.
        _v517_hold = bool(LOKI_FS_V517 and FS_V517_FIREDISC
                          and turret_type == EntityType.SENTINEL
                          and self.v517_hold_now)
        _v517_skipped = False
        try:
            best, best_prio = None, 99
            for t in ct.get_attackable_tiles():
                bid = ct.get_tile_building_id(t)
                bot = ct.get_tile_builder_bot_id(t)
                et = None
                if bid is not None and ct.get_team(bid) != self.team:
                    et = ct.get_entity_type(bid)
                elif bot is not None and ct.get_team(bot) != self.team:
                    et = EntityType.BUILDER_BOT
                if et is None or not ct.can_fire(t):
                    continue
                if _v517_hold and et == EntityType.CORE:
                    _v517_skipped = True
                    continue
                prio = TURRET_PRIO.get(et, 8)
                if prio < best_prio:
                    best_prio, best = prio, t
            if _v517_skipped:
                self._v517_count_hold(ct, best is not None)
            if best is not None:
                ct.fire(best)
                if best_prio == 0 and LOKI_FS_V517 and FS_V517_FIREDISC \
                        and turret_type == EntityType.SENTINEL:
                    # TURRET_PRIO[CORE] == 0 and nothing else scores 0, so this
                    # is "the shot just taken was at their core" without a
                    # second lookup on the tile.
                    self._v517_note_core_shot(ct)
                return
        except Exception:
            pass
        try:
            for eid in ct.get_nearby_entities():
                if ct.get_team(eid) != self.team:
                    # v517: the hold has to close BOTH doors.  This fallback
                    # fires at any hostile it can reach, the enemy core
                    # included, so a hold that only guarded the priority scan
                    # would leak the shot it exists to save.
                    if _v517_hold \
                            and ct.get_entity_type(eid) == EntityType.CORE:
                        continue
                    # LOKI called get_position twice per accepted entity.
                    ep = ct.get_position(eid)
                    if ct.can_fire(ep):
                        ct.fire(ep)
                        return
        except Exception:
            pass
        if ROTATE_DISCIPLINE_ON:
            self._idle_rotate(ct, p, turret_type)

    # --- LOKI-BELTBREAK: the planted gunner's own turn ---------------------

    def _bb_in_band(self, ct, p):
        """Is this turret standing in the d^2 20-100 annulus of the enemy Core?

        Latched once true: a turret is a BUILDING and cannot move, and the
        enemy anchor does not move either, so the answer is a constant for this
        unit's life.  Latching also means a gunner that has already identified
        as a beltbreaker keeps its no-core / no-barrier / one-rotation policy
        even in a round where the anchor slot happens to read empty.
        """
        if self.bb_seen:
            return True
        try:
            E = self.enemy or unpack_pos(ct.read_store(SLOT_ENEMY_CORE))
            if E is None:
                return False
            self.enemy = E
            if not (LOKI_BELTBREAK_DSQ_LO <= dsq_core(p, E)
                    <= LOKI_BELTBREAK_DSQ_HI):
                return False
            # ⛔ THE SMALL-MAP SEAM, and it is not hypothetical -- it was seen
            # in the s48 demo grid (a gunner rotating in band with no PLANT
            # line, i.e. one `_try_counterbattery` built at home).  Maps run
            # from 8x8 up, so on a small board a HOME counter-battery gunner
            # can satisfy the enemy-core band as pure geometry -- which is
            # study §5.1(3)'s "map-geometry accident" arriving from our side
            # for once.  A home defender must keep the base's priority scan and
            # ROTATE_DISCIPLINE, so it is excluded by the tree's OWN definition
            # of home: HUNT_BAND_DSQ, the band `_try_counterbattery` defends.
            # `enemy_core_for` is an involution (table lookup or point
            # reflection, both self-inverse), so applying it to the ENEMY
            # anchor returns OUR anchor with no store slot and no extra state.
            if self.mw and self.mh:
                ours = enemy_core_for(self.mw, self.mh, E)
                if dsq_core(p, ours) <= HUNT_BAND_DSQ:
                    return False
            self.bb_seen = True
            return True
        except Exception:
            return False

    def _bb_turret(self, ct, p):
        """Fire policy and the one-rotation guard for a beltbreak gunner.

        FIRE: whatever the ray is already pointed at, EXCEPT a CORE or a
        BARRIER.  Not a priority scan -- `get_gunner_target()` is the engine's
        own "nearest targetable tile on my facing line" and 92-96% of the
        field's consecutive shots land on the SAME tile anyway, because the
        victim rebuilds there in a median of 2 rounds (study §3.4: the line is
        not eaten, it is FARMED).  The two exclusions are the two measured
        leaks: 52.8% of v94's gunner shots went into a CORE it needed 72 shots
        to kill, and barriers are 34.1% of our gunner shots for 3 Ti of value.

        ROTATE: at most LOKI_BELTBREAK_MAX_ROT (=1) times in this unit's whole
        life, only when the current ray has nothing eligible left, and only to
        a direction that has a LIVE target this round confirmed by
        `can_fire_from` plus the own-buildings ray walk.  An A->B->A
        oscillation is impossible by construction: the counter is per-unit and
        never resets.  The field median is ZERO rotations per gunner; our v94
        averaged 4.32 at 10 Ti each with 62.6% of segments firing nothing, and
        GUNPIN's thrash arm read 44.27.
        """
        rnd = ct.get_current_round()
        try:
            tgt = ct.get_gunner_target()
        except Exception:
            tgt = None
        if tgt is not None:
            et = self._bb_hostile_type(ct, tgt)
            if et is not None and et not in BB_NO_FIRE:
                # Heartbeat BEFORE the ammo check: the Core funds a gunner that
                # HAS a target, not one that has already managed to shoot.  A
                # gunner silent for want of ammunition is exactly the state
                # this signal exists to end.
                ct.write_store(SLOT_BELTBREAK, rnd + 1)
                try:
                    if ct.can_fire(tgt):
                        ct.fire(tgt)
                        self.bb_shots += 1
                        if LOKI_BELTBREAK_LOG and self.bb_shots <= 3:
                            print("BB48 FIRE r%d at (%d,%d) %s n=%d"
                                  % (rnd, tgt.x, tgt.y, et.name, self.bb_shots))
                except Exception:
                    pass
                return

        # Nothing eligible on the current ray.
        if self.bb_rot >= LOKI_BELTBREAK_MAX_ROT:
            return
        try:
            if ct.get_action_cooldown() != 0:
                return
            if ct.get_global_resources() < 10 + LOKI_BELTBREAK_AMMO:
                return
            cur = ct.get_direction()
        except Exception:
            return

        best, best_key = None, None
        try:
            for eid in ct.get_nearby_entities():
                try:
                    if ct.get_team(eid) == self.team:
                        continue
                    et = ct.get_entity_type(eid)
                    if et in BB_NO_FIRE:
                        continue
                    ep = ct.get_position(eid)
                except Exception:
                    continue
                d2 = p.distance_squared(ep)
                if d2 > GUNNER_RANGE_DSQ:
                    continue
                facing = p.direction_to(ep)
                if facing == Direction.CENTRE or facing == cur:
                    continue
                try:
                    if not ct.can_fire_from(p, facing, EntityType.GUNNER, ep):
                        continue
                    if not self._bb_ray_clear(ct, p, facing, ep):
                        continue
                    if not ct.can_rotate(facing):
                        continue
                except Exception:
                    continue
                key = (BB_SITE_VALUE.get(et, 10), -d2)
                if best_key is None or key > best_key:
                    best, best_key = facing, key
        except Exception:
            return
        if best is None:
            return
        try:
            ct.rotate(best)
        except Exception:
            return
        self.bb_rot += 1
        ct.write_store(SLOT_BELTBREAK, rnd + 1)
        if LOKI_BELTBREAK_LOG:
            print("BB48 ROT r%d (%d,%d) %s->%s n=%d"
                  % (rnd, p.x, p.y, cur.name, best.name, self.bb_rot))

    def _bb_hostile_type(self, ct, pos):
        """EntityType of the enemy thing on `pos`, or None.  Building first."""
        try:
            bid = ct.get_tile_building_id(pos)
            if bid is not None and ct.get_team(bid) != self.team:
                return ct.get_entity_type(bid)
            bot = ct.get_tile_builder_bot_id(pos)
            if bot is not None and ct.get_team(bot) != self.team:
                return EntityType.BUILDER_BOT
        except Exception:
            return None
        return None

    def _ray_lands(self, ct, p, facing, target):
        try:
            return bool(ct.can_fire_from(p, facing, EntityType.GUNNER, target))
        except Exception:
            return False

    def _hostile_at(self, ct, pos):
        try:
            bid = ct.get_tile_building_id(pos)
            if bid is not None and ct.get_team(bid) != self.team:
                return True
            bot = ct.get_tile_builder_bot_id(pos)
            return bot is not None and ct.get_team(bot) != self.team
        except Exception:
            return False

    def _facing_has_target(self, ct):
        try:
            t = ct.get_gunner_target()
            if t is None:
                return False
            bid = ct.get_tile_building_id(t)
            if bid is not None and ct.get_team(bid) != self.team:
                return True
            bot = ct.get_tile_builder_bot_id(t)
            return bot is not None and ct.get_team(bot) != self.team
        except Exception:
            return True

    def _rotate_allowed(self, ct, p, want, tgt):
        if ct.get_current_round() - self.rot_rnd >= ROTATE_COOLDOWN_RNDS:
            return True
        if want == self.rot_prev_dir:
            return False
        if self._facing_has_target(ct):
            return False
        return p.distance_squared(tgt) * 3 <= self.rot_lock_d

    def _idle_rotate(self, ct, p, turret_type):
        """Disciplined idle re-aim for a Gunner: pay 10 Ti only for a facing
        that actually lands the ray, only when the current one does not, and
        never straight back to the facing we just left."""
        if turret_type != EntityType.GUNNER:
            return
        try:
            cur = ct.get_direction()
        except Exception:
            return

        cand, cand_d = None, 10 ** 9
        for eid in ct.get_nearby_entities():
            try:
                if ct.get_team(eid) == self.team:
                    continue
                ep = ct.get_position(eid)
                d = p.distance_squared(ep)
                if d >= cand_d:
                    continue
                # A builder past gunner range will have moved before the
                # rotation cooldown clears -- that is the measured thrash.
                if ct.get_entity_type(eid) == EntityType.BUILDER_BOT and d > GUNNER_RANGE_DSQ:
                    continue
            except Exception:
                continue
            cand, cand_d = ep, d

        tgt = cand
        prev = self.rot_tgt
        if prev is not None and self._hostile_at(ct, prev):
            prev_d = p.distance_squared(prev)
            if cand is None or cand_d * 3 > prev_d:
                tgt = prev

        if tgt is not None:
            self.rot_tgt = tgt
            if self._ray_lands(ct, p, cur, tgt):
                return
            want = p.direction_to(tgt)
            if want == Direction.CENTRE:
                return
            if not self._ray_lands(ct, p, want, tgt):
                if want.is_cardinal():
                    return
                want = nearest_cardinal(want)
                if not self._ray_lands(ct, p, want, tgt):
                    return
            try:
                if want != cur and ct.can_rotate(want):
                    if not self._rotate_allowed(ct, p, want, tgt):
                        return
                    self.rot_rnd = ct.get_current_round()
                    self.rot_prev_dir = cur
                    self.rot_lock_d = p.distance_squared(tgt)
                    ct.rotate(want)
            except Exception:
                return
            return

        self.rot_tgt = None
        if ct.get_current_round() - self.rot_rnd < ROTATE_COOLDOWN_RNDS:
            return
        anchor = unpack_pos(ct.read_store(SLOT_ENEMY_CORE))
        if anchor is None:
            return
        want = p.direction_to(anchor)
        try:
            if want != Direction.CENTRE and want != cur and ct.can_rotate(want):
                self.rot_rnd = ct.get_current_round()
                self.rot_prev_dir = cur
                self.rot_lock_d = 10 ** 9
                ct.rotate(want)
        except Exception:
            return
