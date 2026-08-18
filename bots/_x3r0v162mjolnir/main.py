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

from fcode import Direction, EntityType, GameConstants, Position

from doctrine import *  # noqa: F401,F403
from eco import (
    EcoMixin, core_corners, delivery_seats, dsq_core, enemy_core_for,
    heal_seats, known_map_for, nearest_cardinal, nearest_core_tile, pack_pos,
    ring, unpack_pos,
)
from opening import OpenMixin
from raid import RaidMixin
from ring import RingMixin
from sip import SipMixin

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
# PLANK SAP.  What counts as a besieger worth a builder's rounds.  The Launcher
# is in the set because it is the one that deletes our spawns (engine_mechanics
# N.7) and it is the cheapest of the three to peck out at 30 HP.
SAP_TARGET_TYPES = frozenset((EntityType.GUNNER, EntityType.SENTINEL,
                              EntityType.LAUNCHER))
# LOKI-TURBO5 plank R: what "their economy" means to a gun.  A splitter is in
# the set for completeness -- 0 have been built by anybody in 280 games.
T5_ECON_TYPES = frozenset((
    EntityType.CONVEYOR, EntityType.SPLITTER, EntityType.HARVESTER))
T5_RANK_INDEX = {name: i for i, name in enumerate(T5_RANK_ORDER)}

# LOKI-BEARING.  What a home turret is worth being pointed at, best first.  A
# creeper turret is the thing that actually kills the Core (20/20 ladder
# losses); a launcher next; a builder last, and only ever with a Gunner behind
# it, because it will have walked before a Sentinel's fixed facing is dry.
# Nothing else -- a 30 Ti Sentinel sited to shoot a 1 Ti barrier is a loss.
CB_TARGET_RANK = {
    EntityType.SENTINEL: 0, EntityType.GUNNER: 0,
    EntityType.LAUNCHER: 1,
    EntityType.BUILDER_BOT: 2,
}
CB_MOBILE_TYPES = frozenset((EntityType.BUILDER_BOT,))
# CB_TARGET_BUILDERS_ON off => the battery answers STATIC besiegers only.  An
# enemy builder near the Core is transient and a turret bought for it inflates
# the global cost scale (+20%) for the rest of the match; the thing that
# actually kills the Core in 20/20 ladder losses is a turret.
CB_RANK_ACTIVE = CB_TARGET_RANK if CB_TARGET_BUILDERS_ON else {
    k: v for k, v in CB_TARGET_RANK.items() if k not in CB_MOBILE_TYPES
}


class Player(EcoMixin, RaidMixin, OpenMixin, RingMixin, SipMixin):

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

        # --- PLANK SPLIT (wave 17b), per unit.  The plank keeps NO board
        # state: the cap is censused off our own four Core corners every time
        # it is asked.  `sp_built` only bounds the re-lay loop if a fork is
        # shot out repeatedly, and `sp_geom` dedupes the coverage marker. ---
        self.sp_built = 0
        self.sp_geom = None
        self._sp_seat_key = None
        self._sp_seats = frozenset()
        self._sp_corner_key = None
        self._sp_corners = frozenset()

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
        self.raid_ringkeys = frozenset()   # PLANK CAGE: seats + corners

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

        # --- LOKI-TURBO7 PLANK SAP (see the block at the end of doctrine.py).
        # Per unit: the besieging turret this body has committed to, the round
        # it committed, and the tiles it has written off.  sap_ban is keyed by
        # tile and pruned in `_sap`, so it cannot grow with the match. ---
        self.sap_tgt = None
        self.sap_since = 0
        self.sap_ban = {}
        self.sap_seen = None            # rank-0 threat this unit saw THIS round

        # --- WAVE 15 PLANK SEATHOLD + PLANK LPECK (the block at the end of
        # doctrine.py).  Per unit and bounded: one station key, three clocks,
        # one remembered evictor tile and one cached feeder set.  NO shared
        # state at all -- the SH_BODIES cap is settled by a local id ballot
        # (`_sh_claim_ok`), because slots 0-15 are all multiplexed already. ---
        self.sh_seat = None             # (x,y) of the station this body holds
        self.sh_since = -1              # round it took it (for the marker)
        self.sh_back = None             # (x,y) it was THROWN off and walks to
        self.sh_back_since = -10 ** 9   # round of that throw
        self.sh_evictor = None          # (x,y) of the launcher that threw it
        self.sh_ev_since = -10 ** 9     # round that evictor was identified
        self.sh_seen_rnd = -10 ** 9     # last round THIS body saw the trigger
        self.sh_seen_pos = None         # ...and where that intruder stood
        self.sh_feeder = None           # cached delivery-seat carve-out
        self.sh_feeder_key = None
        self.lp_hit = set()             # launcher tiles this body has marked;
                                        # capped at LP_MARK_MAX in `_lp_note`

        # --- PLANK REPAIR (P1) (see the block at the end of doctrine.py).
        # Per unit: which (tag, tile) events this body has already logged, the
        # damaged building it is walking to, the round it committed, and the
        # tiles it has written off.  rep_marked is capped in `_rep_mark` and
        # rep_ban is pruned in `_rep_detour_target`, so neither grows with the
        # match. ---
        self.rep_marked = set()
        self.rep_marks_n = 0
        self.rep_gap2_n = 0             # per-body ceiling on two-wide relays
        self.rep_tgt = None
        self.rep_since = 0
        self.rep_ban = {}
        self.rep_seen = frozenset()     # our belt tiles this body saw last round
        self.rep_lost = {}              # tile -> round it was watched to DIE

        # --- PLANK P3 SIEGE (see the block at the end of doctrine.py).
        # Per unit, because there is no free store slot to publish a build
        # round in and every one of these is a local decision. ---
        self.sge_fwd_since = None       # raider: round it first saw a fwd tube
        self.sge_screen_done = False    # raider: the screen gunner stands
        self.sge_screen_rnd = -10 ** 9  # raider: last round the ray search ran
        self.sge_gun_rnd = -1           # raider: round _sge_enemy_guns scanned
        self.sge_band_rnd = -1          # raider: round _sge_core_band resolved
        self.sge_band_val = 0           # raider: that round's HP band (SIEGE_HP_*)
        self.col_surge_in = False       # raider: inside the terminal window (marker)
        self.sge_guns = ()              # raider: visible enemy Gunner positions
        self.sge_ammo_prev = None       # Core: last round's magazine (JIT)
        self.sge_ammo_idle = 0          # Core: rounds since it last fell
        self.sge_jit_logged = False     # Core: the one-time "SGE jit on"

        # --- PLANK P2 COLLAR (the COLLAR block at the end of doctrine.py).
        # Per unit: titanium this body charged to the collar (the fallback
        # accounting when the shared field is unavailable), the enemy seats it
        # knows carry one of our bricks -- so a rebuild logs as a RESEAL even
        # when the body that laid the first one is dead -- the seats it has
        # already announced squatting, and the marker de-duplicator.  All three
        # collections are keyed by SEAT, of which there are eight, so none of
        # them can grow with the match. ---
        self.col_spent = 0
        self.col_bricks = set()
        self.col_squatted = set()
        self.col_log = {}
        # PLANK KEYSTONE (leap16).  One scalar: the round this body last
        # announced a corner released.  It cannot grow.
        self.kc_log = -10 ** 9

        # --- TERMINAL WEAPONS (bots/loki_leap3).  Every field is per unit and
        # bounded: two latches, one round memo per derived quantity, one anchor
        # cache and two counters.  Nothing here accumulates across units and
        # nothing here is published except the single gunner bit in slot 15,
        # so the weapons add no writer to any comm slot. ---
        self.tw_turret = False          # raider: an enemy turret was SEEN (latch)
        self.tw_manned_max = 0          # raider: most of their seats seen manned
        self.tw_gate_rnd = -1           # raider: round the gate was resolved
        self.tw_gate_val = False        # raider: that round's answer
        self.tw_gate_logged = False     # raider: the one-time "TW gate" marker
        self.tw_cen_rnd = -1            # raider: round the TW census scanned
        self.tw_cen_val = (None, None)  # raider: (launchers, gunners) at the ring
        self.tw_hp_rnd = -1             # raider: round their Core HP was read
        self.tw_hp_val = None           # raider: that HP, or None if blind
        self.tw_corner_key = None       # raider: anchor tw_corner_xy was built for
        self.tw_corner_xy = frozenset() # raider: their four ring corners
        self.tw_launch_n = -1           # raider: last census level seen standing
        self.tw_launch_since = -10 ** 9 # raider: round that level was first seen
        self.tw_far_key = None          # launcher: (pos, anchor) of the throw order
        self.tw_far = ()                # launcher: throw sites, farthest first
        self.tw_plucks = 0              # launcher: cumulative throws (marker)
        self.tw_pluck_log = -10 ** 9    # launcher: round the last marker printed
        self.tw_why_rnd = {}            # raider: reason -> round it last printed
        self.tw_resv_logged = False     # raider: the one-time "TW resv" marker

        # --- shared archetype detector, Core-side (analysis/archetype_detector.md).
        # Held per unit rather than re-read from the store because the Core is
        # the only classifier and its instance survives the whole match; the
        # store copy exists for the other units, not for this one. ---
        self.arch_code = ARCH_DEFAULT
        self.arch_set = 0

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

        # --- LOKI-TURBO5 (see the block at the end of doctrine.py) ---
        # The standoff ring is a pure function of the enemy anchor and the
        # terrain, so it is derived per unit and cached rather than published:
        # store writes are next-round-visible and last-write-wins, and every
        # raider computes the same tuple from the same anchor anyway.
        self.t5_nest_key = None         # enemy anchor the nest list was built for
        self.t5_nests = ()              # ranked (site, facing, core tile)
        self.t5_swept_rnd = -1          # round self.t5_swept was scanned
        self.t5_swept = frozenset()     # tiles under a visible enemy turret's ray
        self.t5_bar_ban = {}            # turret: barrier tile -> round last shot
        self.t5_seat_key = None         # enemy anchor self.t5_seat_xy was built for
        self.t5_seat_xy = frozenset()   # THEIR eight heal seats, as (x, y)
        self.t5_home_gun_done = False   # defender: a home gunner already stands
        self.t5_nav_rnd = -1            # last round _nav was actually attempted

        # --- PLANK SOCKET-GUARD (see the block at the end of doctrine.py) ---
        # All per-unit; the ONE shared field is the Core's 4-bit socket request
        # in slot 9 bits 28-31, and the Core is already that slot's sole writer.
        self.sg_scan = None             # memoised socket census
        self.sg_scan_rnd = -1           # round it was taken
        self.sg_scan_deep = False       # whether `aimed`/`hfed` were computed
        self.sg_fill_n = 0              # bricks THIS body has laid on sockets
        self.sg_walk_key = None         # (x, y) of the request being walked to
        self.sg_walk_left = 0           # rounds of walking left for that request
        self.sg_walk_total = 0          # lifetime rounds this body has diverted
        self.sg_gun_done = False        # defender: the ring turret stands
        self.sg_launch_walk = None      # defender: the corner it is walking to
        self.sg_far_key = None          # launcher: (pos, our core, their anchor)
        self.sg_far = ()                # launcher: eviction sites, best first

        # --- WAVE 22 TRACK 3, PLANK RING (see ring.py and the RING block at
        # the end of doctrine.py).  Per unit and bounded: two trigger fields,
        # one claim counter, one floor baseline, three walk clocks and one
        # refill intent.  The plank adds NO shared state and NO comm slot --
        # the eviction cap is an id ballot among the bodies that can see the
        # target and the claim ledger is censused off the standing
        # buildings, which is the one ledger a buffered store cannot spoil. ---
        self.ring_seen_rnd = -10 ** 9   # last round THIS body saw the trigger
        self.ring_seen_pos = None       # ...and where that non-builder stood
        self.ring_claims = 0            # sockets THIS body has claimed
        self.ring_walk_key = None       # (x, y) this body is diverting toward
        self.ring_walk_left = 0         # rounds of walking left for that tile
        self.ring_walk_total = 0        # lifetime rounds diverted (both arms)
        self.ring_ev_key = None         # (x, y) of the brick being pecked
        self.ring_ev_left = 0           # rounds of pecking left on that tile
        self.ring_ev_total = 0          # lifetime pecks this body has spent
        self.ring_refill = None         # (x, y) of a socket we just cleared
        self.ring_refill_rnd = -10 ** 9  # ...and the round we cleared it
        self.sg_evicts = 0              # launcher: cumulative evictions (marker)
        self.sg_req_bits = 0            # Core: last request published (CPU guard)

        # --- PLANK CAGE (see the block at the end of doctrine.py).  Per unit
        # and bounded: two round-memos, one latch pair, three small counters
        # and one throw ordering.  The ONLY shared state the plank adds is
        # three LATCH bits in slot 13 (28-30), whose two existing writers both
        # preserve that field already, plus a tag bit on the ferry claim that
        # SLOT_FERRY_RND already had room for. ---
        self.cg_open = False            # this body has latched "fire at will"
        self.cg_saw = False             # ...after OBSERVING a published HOLD
        self.cg_since = -1              # first round this body published the bit
        self.cg_seat = None             # is this body the ferry rider? (latched)
        self.cg_why_rnd = {}            # rider: refusal reason -> round logged
        self.cg_chain_log = {}          # wave 13 arm D: reason -> marker fired
        self.cg_floor = None            # rider: bank floor for a hop (latched)
        self.cg_hop_try = -10 ** 9      # launcher: round of its last hop SCAN
        self.cg_disarm = False          # finisher guard (i) latched on this body
        self.cg_hold_rnd = -1           # round the hold bit was decoded
        self.cg_hold_val = False        # that round's answer
        self.cg_seal_rnd = -1           # round the ring census was taken
        self.cg_seal_val = (0, 0)       # (ring12 held, ring8 held)
        self.cg_strict_val = (0, 0)     # ...and the same census with THEIR
                                        # bodies NOT counted (PLANK FIN)
        self.cg_seal_log = None         # last census this body announced
        self.cg_hold_log = -10 ** 9     # round the last `CG hold` printed

        # --- CAGE EVICTOR GATE, WAVE 12 (the block at the end of doctrine.py).
        # One round-memo, two clocks and two one-way latches.  NO shared state
        # at all: the gate is applied at the two publishers the cage already
        # has (slot 15 bit 31 and slot 13 bits 28-29), so every blind consumer
        # inherits it without a third field to lose races in. ---
        self.cg_ev_rnd = -1             # round the evictor census was taken
        self.cg_ev_val = False          # that round's answer
        self.cg_ev_first = -1           # first round one was SEEN (-1 = never)
        self.cg_ev_last = -10 ** 9      # ...and the most recent such round
        self.cg_ev_dead = False         # deadline passed with none ever seen
        self.cg_gate_log = False        # the `CG evgate off` marker has fired
        self.cg_launch_n = 0            # launcher builds by this body, ALL arms
                                        # (CAGE_EST_LAUNCH_CAP, leap10_est)

        # --- PLANK PAIRS (see the block at the end of doctrine.py).  Per unit
        # and tiny: one round-memo, one one-way latch, two clocks.  The plank
        # adds NO shared state at all -- the pair census it gates on is
        # SLOT_FWD_GUN, which `_t5_note_fwd_build` already publishes. ---
        self.pr_open = False            # this body has latched "fire at will"
        self.pr_since = None            # first round it could have shot the Core
        self.pr_hold_rnd = -1           # round the gate was resolved
        self.pr_hold_val = False        # that round's answer
        self.pr_hold_log = -10 ** 9     # round the last `PR hold` printed
        self.pr_solo_since = None       # Core: round the tube census went to 1
        self.cg_ferry_n = 0             # rider: ferry launchers bought so far
        self.cg_wait_until = 0          # rider: stand still until this round

        # --- PLANK SPRINT, WAVE 18 (the block at the end of doctrine.py).
        # THREE FIELDS, per body, and NONE of them shared: the sprint keeps its
        # own books precisely so that the parent ferry's budget and wave 12's
        # reserved evictor post are untouched when the window closes. ---
        self.spr_n = 0                  # rider: SPRINT rungs bought (SPR_CAP)
        self.spr_ti = 0                 # ...and titanium spent on them
        self.spr_arr = False            # the one-shot `SPR arrive` latch
        # --- WAVE 19, FIX 1: THE COLLECTION GATE.  The realized-collection
        # meter and the watermark the previous rung was bought at.  See
        # `_spr_collect` in raid.py and the SPR_COLLECT block in doctrine.py.
        self.spr_bank = None            # rider: bank read on its previous turn
        self.spr_coll = 0               # rider: realized collection since r0
        self.spr_mark = None            # ...its value when the last rung went up
        self.spr_gate_log = -1          # round the `SPR gate` marker printed
        self.cg_threw = False           # launcher: it has made a ferry throw
        self.cg_hop_rnd = -10 ** 9      # launcher: round of its last hop
        self.cg_near_key = None         # launcher: (pos, enemy anchor) of cg_near
        self.cg_near = ()               # launcher: throw sites, nearest THEM first

        # --- PLANK FIN + PLANK RATCHET (see the two blocks at the end of
        # doctrine.py).  Per unit and small: two round-memos, one latch, one
        # counter and a bounded dict of ring seats.  The ONLY shared state
        # either plank adds is TWO bits in slot 13 (28-29), whose two existing
        # writers already carry bits 26-31 through unchanged. ---
        self.fin_open = False           # raider: this body's own window latch
        self.fin_rnd = -1               # round the published window was decoded
        self.fin_val = False            # that round's answer
        self.fin_surged = False         # Core: the one-time `FIN surge` marker
        self.rat_rnd = -1               # round the ratchet gate was resolved
        self.rat_val = False            # that round's answer
        self.rat_watch = {}             # ring seat -> round we last saw one of
                                        # THEIR bodies sitting on it
        self.rat_n = 0                  # seats THIS body has closed by ratchet

        # --- gunner rotation latch (PIECE I) ---
        self.rot_tgt = None
        self.rot_rnd = -10 ** 9
        self.rot_prev_dir = None
        self.rot_lock_d = 10 ** 9

        # --- PLANK RG, THE REACTIVE RING GUNNER (block at the end of
        # doctrine.py).  Per unit, five scalars, no shared state at all: the
        # trigger rides the detector's existing S3 stamp and the budget rides
        # SLOT_HOME_GUN, both of which already have writers. ---
        self.rg_seen_rnd = -10 ** 9     # last round THIS body saw an enemy
                                        # BUILDER within RG_TRIGGER_DSQ
        self.rg_seen_pos = None         # ...and where it was
        self.rg_done = False            # builder: this unit has stopped trying
                                        # (the gun is up, ours or a peer's)
        self.rg_core = None             # turret: OUR Core anchor, found once
        self.rg_mine = None             # turret: am I the reactive ring gun?
        # --- WAVE 19, FIX 2: THE CHASE.  Two scalars on the GUN itself.  The
        # budget is titanium and not rotations because that is what the brake
        # is denominated in everywhere else in this tree, and because a rotate
        # is 10 Ti flat (docs 164/251) so the two are the same number anyway. ---
        self.rg_rot_ti = 0              # turret: titanium spent on chase rotates
        self.rg_chase_rnd = -10 ** 9    # turret: round of the last chase rotate

        # --- WAVE 22 ARM A2, GUN DISCIPLINE (GD block at the end of
        # doctrine.py).  FOUR SCALARS ON THE GUN ITSELF and not one byte of
        # shared state: all 16 comm slots are assigned in the base, and the
        # only unit that can ever know whether a given gunner has fired is
        # that gunner.  A builder carries them too and never reads them --
        # they cost one assignment at spawn. ---
        self.gd_shots = 0               # turret: shots THIS gun has fired
        self.gd_born = None             # turret: first round it took a turn
        self.gd_reaims = 0              # turret: CLEAR LANE rotations bought
        self.gd_reaim_rnd = -10 ** 9    # turret: round of the last one

        # --- PLANK EARLYBIRD, THE CAGE-ARRIVAL DETECTOR (block at the end of
        # doctrine.py).  The tracking dict is the only new per-unit memory in
        # the plank, it is bounded by EB_TRACK_MAX, and it is torn down the
        # moment the latch closes or the window shuts -- so on a game where
        # nothing is ever detected it holds at most EB_TRACK_MAX entries for
        # at most EB_EARLY_MAX rounds. ---
        self.eb_seen = False            # THIS body has latched the signature
        self.eb_rnd = -1                # ...on this round
        self.eb_track = {}              # enemy builder id -> (rnd, x, y)
        self.eb_win = None              # cached map-aware window
        self.eb_ec = None               # cached THEIR Core anchor (symmetry)
        self._eb_rd = -1                # per-round memo for the store read
        self._eb_val = False
        self.eb_held = False            # arm (a): the hold has printed once
        self.eb_pub_done = False        # the bit has been READ BACK set, so
                                        # this body may stop re-asserting it

        # --- LOKI-BEARING per-round memos (see _cb_target / _home_guns) ---
        self._cb_rnd = -1
        self._cb_val = (None, None)
        self._hg_rnd = -1
        self._hg_val = []

        # --- WAVE 22, ARM A1: THE INTEGRATED OPENING (see opening.py and
        # the OPEN block at the end of doctrine.py).  Per unit and bounded:
        # one pointer at the module-cached resolved geometry, one frozenset of
        # two socket keys, five latches and one stage counter.  The plank adds
        # NO shared state and NO comm slot -- every unit derives the same
        # answer from the same r0 geometry, and the only cross-body facts it
        # consults (SLOT_ROLE_N, SLOT_HARVESTERS, SLOT_FWD_GUN) already have
        # writers. ---
        self.op_geom = None             # resolved opening (module cache)
        self.op_sock_keys = None        # the two prefill sockets, as (x, y)
        self.op_seat_ban = None         # all eight sockets, for `_seat_ban`
        self.op_band_log = False        # the one-time `OP band=` marker
        self.op_prefill_done = False    # this body's socket is filled
        self.op_trunk_done = False      # ...and its feeder line is complete
        self.op_stage = 0               # marker only: 0 none, 1 socket laid
        self.op_lift = False            # Core: the cap has lifted (one-way)
        self.op_lift_log = False        # ...and `OP capliftr=` has printed
        self.op_pair_built = False      # band A: this body built its sentinel
        # --- WAVE 22 ARM A5, THE TITANIUM-TIEBREAK ENDGAME (block at the end
        # of doctrine.py).  Nine scalars, no containers, no growth: the arm's
        # whole per-unit memory.  Every one of them is inert with END_ON down
        # -- `_end_tick` returns before it writes and `_end_fired` returns
        # False on its first line. ---
        self.end_armed = False          # `END arm` has printed for this unit
        self.end_fired = False          # the one-way latch (never cleared)
        self.end_rnd = -1               # ...set on this round
        self.end_run = 0                # consecutive rounds the band was NOT
                                        # SIEGE_HP_LOW, counted from r400
        self.end_low_rnd = -1           # last round this unit read LOW, or -1
        self.end_tick_rnd = -1          # per-round guard on the clock
        self.end_recall_rnd = -1        # round ARM 1's walk home began
        self._end_rnd = -1              # per-round memo for `_end_fired`
        self._end_val = False

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

        # WAVE 22 ARM A5.  THE CORE IS THE ARBITER, because it is the only unit
        # alive from r0 and therefore the only one whose stall clock is
        # complete.  Two store reads a round from r400; nothing at all before
        # it, and nothing ever with END_ON down.
        if END_ON:
            self._end_tick(ct, rnd)

        # --- threat latch -------------------------------------------------
        # LOKI-BEARING.  LOKI broke on the FIRST qualifying enemy, so whichever
        # id came out of get_nearby_entities() first became "the threat" -- in
        # the ladder losses that was an enemy BUILDER on 1,019 rounds against
        # 1,721 for the turrets actually shelling us.  Rank instead: a turret
        # beats a builder, nearer beats farther, and the whole list is scanned
        # (this loop already ran to completion whenever no threat was present,
        # so the added cost is bounded by the rounds we are under attack).
        under = False
        thr_rank = None
        thr_pos = None
        live_turrets = 0
        arch_s1 = False
        arch_s2 = False
        arch_s3 = False
        for eid in ct.get_nearby_entities():
            try:
                if ct.get_team(eid) == self.team:
                    if ct.get_entity_type(eid) in CORE_THREAT_TYPES:
                        live_turrets += 1
                    continue
                ep = ct.get_position(eid)
                d = p.distance_squared(ep)
                et = ct.get_entity_type(eid)
            except Exception:
                continue
            # DETECTOR signals, taken off a scan that was going to run anyway.
            if ARCH_ON:
                if et in SAP_TARGET_TYPES:
                    arch_s2 = True
                    if d <= ARCH_NEAR_DSQ:
                        arch_s1 = True
                elif et == EntityType.BUILDER_BOT and d <= ARCH_NEAR_DSQ:
                    arch_s3 = True
            if et in CORE_THREAT_TYPES and d <= 64:
                rank = (0, d)
            elif et == EntityType.BUILDER_BOT and d <= 16:
                rank = (1, d)
            else:
                continue
            under = True
            if not CB_RANK_THREAT_ON:
                thr_rank, thr_pos = rank, ep
                break
            if thr_rank is None or rank < thr_rank:
                thr_rank, thr_pos = rank, ep
        if thr_pos is not None:
            ct.write_store(SLOT_THREAT, pack_pos(thr_pos))
        if ARCH_ON:
            if arch_s1 or arch_s2 or arch_s3:
                self._arch_note(ct, pressure=arch_s1, intruder=arch_s3,
                                turret_anywhere=arch_s2)
            self._arch_classify(ct, rnd, arch_s1)
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
        if harv >= ECO_NEED:
            ct.write_store(SLOT_ECO_READY, 1)

        # Income meter, in quarter-titanium so passive (10 Ti / 4 rounds) and
        # harvester output (a 10-stack / 4 rounds) are both exact integers.
        self.income_q += 10 + K_HEAL_HARV_Q * harv
        # T4 BLEED BEACON.  Slot 9 was written every round and read by NOBODY
        # (loki_analysis.md 1.3), so the Core spends it on the one fact a
        # builder outside its own r^2=20 vision cannot obtain: how hurt we are.
        # `_core_shelled` reads it when the Core is not in view.
        # The archetype rides in bits 16-27 of the same word; the beacon is a
        # damage figure <= 500, so the two never collide, and the Core is the
        # only writer of this slot in the whole file.
        # PLANK SOCKET-GUARD arm 3.  Bits 28-31 of the SAME word: the socket
        # the Core wants a feeder on, as index+1, or 0 for "stand down".  All
        # eight of our sockets are permanently inside the Core's own vision and
        # inside nobody else's, so the Core is the only unit that can census
        # them honestly -- and it is already this slot's sole writer every
        # round, so the field adds ZERO store traffic (DOCTRINE 6).  The bleed
        # beacon is a damage figure <= 500 (bits 0-15) and the archetype is
        # bits 16-27, so the three fields cannot collide.
        arch = self._arch_bits()
        if SG_ON:
            arch |= self._sg_request_bits(ct)
        # WAVE 22 ARM A5, THE PUBLISH.  Bit 28 of the SAME word, on exactly the
        # discipline doctrine.py section 2b arrived at for the HP band: ONE
        # writer, republished whole every round, so a lost write costs one
        # round and repairs itself.  No new comm slot (PLAN.md 1.5) -- bits
        # 28-31 are SOCKET-GUARD's and `SG_ON` is False on this carrier, which
        # is why the publish is guarded on it rather than assuming it.  With
        # SOCKET-GUARD on, this prints nothing and every unit falls back to its
        # own stall clock, which can only ever fire LATER.
        if END_ON and not SG_ON and self._end_fired(ct):
            arch |= END_BIT
        if T4_BLEED_BEACON_ON:
            ct.write_store(SLOT_HEAL_BUDGET, (ct.get_max_hp() - hp) | arch)
        elif K_HEAL_BUDGET_ON:
            ct.write_store(SLOT_HEAL_BUDGET,
                           ((self.income_q // 4) * K_HEAL_RATE_PCT // 100) | arch)
        elif arch:
            ct.write_store(SLOT_HEAL_BUDGET, arch)

        ti, ammo = ct.get_global_resources(), ct.get_global_ammo()
        home_guns = ct.read_store(SLOT_HOME_GUN)
        fwd_guns = ct.read_store(SLOT_FWD_GUN)
        weapons = home_guns + fwd_guns
        # TERMINAL WEAPONS W1.  The forward gunner is invisible to the Core --
        # SLOT_HOME_GUN is a home-band counter and adding it there would aim the
        # home-defence arms at a turret five tiles from THEIR Core -- so it
        # rides one bit of the raid heartbeat instead (slot 15 bit 30, sole
        # writer `_raid_beat`).  Read here for the ammunition burn ONLY: it is
        # deliberately not folded into `weapons`, which drives the bank floor
        # and the endgame dump.
        tw_guns = 0
        if TW_ON and TW_GUN_ON and ct.read_store(SLOT_RAID_LIVE) & TW_BEAT_GUN_BIT:
            tw_guns = 1

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
            # WAVE 22 ARM A5, ARM 2, THE DUMP HALF.  The parent reserves two
            # harvesters here for tiebreak #2, which has never fired in 450
            # games; under END the reserve becomes the DELIVERY price -- one
            # harvester and its first conveyors -- because the tiebreak that
            # does fire counts stacks that arrived, and a magazine moves none.
            resv = 2 * ct.get_harvester_cost()
            if END_ON and END_AMMO_SUBORD_ON and self._end_fired(ct):
                end_floor = self._end_eco_floor(ct)
                if end_floor > resv:
                    resv = end_floor
            amt = min(ti - resv, cap - ammo)
            if amt > 0 and ct.can_convert_ammo(amt):
                ct.convert_ammo(amt)
                ti, ammo = ct.get_global_resources(), ct.get_global_ammo()

        if not endgame_dumped and AMMO_JIT_ON:
            # PLANK P3, THE AMMO PIPE.  Replaces the ladder below wholesale --
            # never both, so the two policies can never argue about one round.
            self._sge_jit(ct, rnd, ti, ammo, under, home_guns, fwd_guns,
                          weapons_top, live_turrets, tw_guns)
            ti = ct.get_global_resources()
        elif not endgame_dumped:
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
            ti_floor = 12 if (under or weapons_top) else 52
            if E1_AMMO_FLOOR_ON and not under:
                ti_floor = max(
                    ti_floor,
                    min(ct.get_harvester_cost(), E1_RESERVE_CAP) + E1_HARV_RESERVE_MARGIN,
                )
            # LOKI-BEARING DRY MAGAZINE.  702 turret-rounds in the ladder
            # corpus had a hostile ON the line and less ammo than one shot
            # costs, at a MEDIAN bank of 12 Ti -- exactly this floor.  A
            # Sentinel shot is 18 damage for 10 Ti; the same 10 Ti heals 40 HP
            # of our own Core and does nothing to the thing doing the damage.
            # Gated on a turret we can actually see, so a stale monotone
            # weapons count cannot burn titanium into an empty battlefield.
            if (CB_DRY_MAG_ON and under and ammo < CB_DRY_MAG_AMMO
                    and (live_turrets or fwd_guns)):
                ti_floor = min(ti_floor, CB_DRY_MAG_TI_FLOOR)
            # MERGE (turbo5): the gate keeps T4's braked `weapons_top`, not the
            # raw monotone `weapons` turbo3 read.  The two planks cannot both
            # be live in the same round -- the brake needs ammo >= 16 and the
            # dry magazine needs ammo < 10 -- so neither is weakened.
            if (under or weapons_top or harv >= 2) and ammo < ammo_target and ti > ti_floor:
                amt = min(16, ammo_target - ammo, ti - ti_floor)
                if amt >= 4 and ct.can_convert_ammo(amt):
                    ct.convert_ammo(amt)
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

        # WAVE 22, ARM A1 -- THE BUILDER CAP, and it is the single purchase the
        # whole opening rests on.  Three builders while the ferry is live (four
        # in band A), lifted at ARRIVAL and only once the bank still clears the
        # counter-battery reserve.  OPENING.md 2.2 prices it: bank@10 is 230
        # under the cap and 95 with five builders, and band C with five
        # builders goes NEGATIVE at r11 -- which is our own measured ragnarok
        # failure, six builders by r7, ladder dead at rung 3, arrival r25
        # against their r12.  Builders #4 and #5 are not a 102-Ti decision;
        # they are 102 Ti plus a 25 % tax on every later purchase in the
        # opening.  Replacements are counted INSIDE the cap deliberately: a
        # body lost at r4 is a body the ferry budget still has to pay for.
        if OPEN_ON:
            try:
                op_cost = ct.get_builder_bot_cost()
            except Exception:
                op_cost = GameConstants.BUILDER_BOT_BASE_COST
            op_cap = self._op_cap(ct, rnd, ti, op_cost)
            if op_cap is not None and budget > op_cap:
                budget = op_cap

        if ct.get_action_cooldown() != 0:
            return
        if self.n >= budget or units >= GameConstants.MAX_TEAM_UNITS - 2:
            return
        cost = ct.get_builder_bot_cost()
        # The opening five are unconditional (the incumbent's shipped curve);
        # anything above them keeps a reserve so a body never starves the
        # first harvesters.
        need = cost if self.n < LOKI_BASE_BUILDERS else cost + LOKI_SPAWN_RESERVE
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
        # WAVE 22, ARM A1 -- THE SEAT'S OWN TILE FIRST.  Seats 1 and 2 spawn on
        # the DIAGONAL that owns their socket: a diagonal ring corner is
        # orthogonally adjacent to exactly two sockets on two DIFFERENT core
        # faces, so one body standing on one tile buys the whole "2 sockets, 2
        # faces" bar in consecutive actions with zero moves (OPENING.md 3.1
        # correction 2, traced on O(1)/nordkap).  Seat 0 -- the rider -- spawns
        # on the ring tile with the smallest BFS walk distance to their ring.
        # A PREFERENCE and nothing more: the tile is prepended, the parent's
        # entire dispersion list is still behind it, and `can_spawn` decides.
        if OPEN_ON:
            want = self._op_spawn_tile(ct, self.n)
            if want is not None:
                cands = [want] + [c for c in cands
                                  if not (c.x == want.x and c.y == want.y)]
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
            n = ct.read_store(SLOT_ROLE_N)
            self.role_n = n
            ct.write_store(SLOT_ROLE_N, n + 1)
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
            if n == LOKI_DEFEND_SEAT:
                self.role = "defend"
            elif (
                LOKI2_RUSH_ON and n in LOKI2_RUSH_SEATS
                and ct.get_current_round() < LOKI2_RUSH_RND
            ):
                self.role = "raid"
            elif n in LOKI_ECO_SEATS:
                self.role = "expand"
            else:
                self.role = "raid"
            if self.role == "raid":
                self.raid_slot = ct.read_store(SLOT_RAID_N)
                ct.write_store(SLOT_RAID_N, self.raid_slot + 1)

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

        # WAVE 22 ARM A5.  This body's OWN stall clock -- the fallback for the
        # Core's published bit (doctrine section 3, risk R4).  Two store reads
        # a round from r400 and nothing before it.  It is above the sensing
        # loop so that a body which spends its whole turn on an emergency heal
        # still keeps its clock honest.
        if END_ON:
            self._end_tick(ct, rnd)

        # --- sensing --------------------------------------------------------
        # LOKI-BEARING.  Same ranking as the Core's latch.  LOKI wrote
        # SLOT_THREAT once per qualifying enemy with no break, so the LAST id
        # in the list won -- a wandering builder routinely overwrote the
        # turret that was shelling the Core.  One write, best candidate.
        thr_rank = None
        thr_pos = None
        sh_near_d = None
        sh_near_pos = None
        lp_seen_d = None
        lp_seen_pos = None
        rg_near_d = None
        rg_near_pos = None
        arch_s1 = False
        arch_s2 = False
        arch_s3 = False
        arch_s5 = 0
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
            # PLANK SEATHOLD trigger, and it is FREE: `d` is already the exact
            # quantity the plank asks about, computed by a loop that runs every
            # round anyway.  ANY enemy entity counts -- unit or building --
            # because their first brick lands at t8 and the builder that placed
            # it and the barrier it placed are the same warning.
            if SH_ON and d <= SH_TRIGGER_DSQ and (sh_near_d is None or d < sh_near_d):
                sh_near_d, sh_near_pos = d, ep
            # PLANK LPECK, THE WALK.  Measured in the wave-15 smoke and it is
            # the whole reason this arm exists: across 8 legs vs `mimic_jython`
            # an enemy launcher was within d <= 10 of our Core for 678, 331,
            # 407... ROUNDS A GAME, and orthogonally adjacent to one of our
            # bodies for 0-5.  A 30 HP launcher needs 15 consecutive adjacent
            # rounds to die, so an adjacency-only plank can never kill one.
            # SAP already owns the only walker we trust (the defender, one
            # body, seat-first, 20 rounds of committed pecking) and
            # SAP_TARGET_TYPES has always listed LAUNCHER -- what was missing
            # is that nothing ever NOMINATED one, because CORE_THREAT_TYPES is
            # turrets only.  Nominating it here, and NOT via CORE_THREAT_TYPES,
            # keeps the 30 Ti turret bearing logic exactly where it was.
            if (LP_ON and LP_SAP_TARGET_ON and et == EntityType.LAUNCHER
                    and d <= LP_NEAR_DSQ
                    and (lp_seen_d is None or d < lp_seen_d)):
                lp_seen_d, lp_seen_pos = d, ep
            # PLANK RG, THE TRIGGER, and it is free for the same reason
            # SEATHOLD's is: `d` is already computed.  BUILDER BOTS ONLY, and
            # that is not a detail -- it is the entire safety case.  The body
            # this gun is bought for is the ONE early raider that walks to our
            # ring at t8 and bricks it, which nothing else we own can touch
            # (a builder cannot fire on a builder).  A creeper TURRET walked
            # onto our doorstep is a different animal with a different answer
            # (SAP / counter-battery), and against `mimic_0033` -- whose whole
            # opening is exactly that -- this comparison is what keeps the
            # plank silent.  `et` is tested here and nowhere else.
            if (RG_ON and et == EntityType.BUILDER_BOT and d <= RG_TRIGGER_DSQ
                    and (rg_near_d is None or d < rg_near_d)):
                rg_near_d, rg_near_pos = d, ep
            # PLANK EARLYBIRD, THE DETECTOR, and it rides the same free `d`
            # the two planks above ride.  BUILDER BOTS ONLY -- the same purity
            # argument RG makes, for the same reason: `mimic_0033`'s opening
            # is creeper TURRETS walked onto our doorstep, and a turret is not
            # a cage courier.  Everything expensive is inside `_eb_note`, and
            # `_eb_note` is not reached at all once the latch closes or the
            # window shuts, which on a non-cage opponent is by round 15.
            if (EB_ON and et == EntityType.BUILDER_BOT and not self.eb_seen
                    and d <= EB_TRIGGER_DSQ):
                self._eb_note(ct, rnd, eid, ep, d)
            # PLANK RING, THE TRIGGER, and it is free for exactly the reason
            # SEATHOLD's and RG's are: this loop already holds `et` and `ep`,
            # and the plank asks one question about them.  NON-BUILDER enemies
            # only, which is the whole registration -- 0033's weapon is a
            # BARRIER at d = 2.53 from r7 and a GUNNER at d = 5.10 from r17,
            # and 128 of its 138 turret placements are past the midline.  An
            # enemy BUILDER is a different animal with different answers (RG,
            # EARLYBIRD, SAP) and is deliberately not this trigger.
            if (RING_ON and RING_TRIGGER_ON and et != EntityType.BUILDER_BOT
                    and et != EntityType.CORE):
                self._ring_note(ct, rnd, et, ep)
            # DETECTOR signals.  S5 is the raider's contribution -- the enemy
            # builder crowd at THEIR Core is the only look anybody on our team
            # gets at a 36-body macro roster (ladder_field.md, I Stone).
            if ARCH_ON:
                if et in SAP_TARGET_TYPES:
                    arch_s2 = True
                    if d <= ARCH_NEAR_DSQ:
                        arch_s1 = True
                elif et == EntityType.BUILDER_BOT:
                    if d <= ARCH_NEAR_DSQ:
                        arch_s3 = True
                    if self.enemy is not None and dsq_core(ep, self.enemy) <= ARCH_NEAR_DSQ:
                        arch_s5 += 1
            if et in CORE_THREAT_TYPES and d <= 64:
                rank = (0, d)
            elif et == EntityType.BUILDER_BOT and d <= 16:
                rank = (1, d)
            else:
                continue
            ct.write_store(SLOT_UNDER, 1)
            ct.write_store(SLOT_ATK_RND, rnd)
            if not CB_RANK_THREAT_ON:
                ct.write_store(SLOT_THREAT, pack_pos(ep))
                continue
            if thr_rank is None or rank < thr_rank:
                thr_rank, thr_pos = rank, ep
        if thr_pos is not None:
            ct.write_store(SLOT_THREAT, pack_pos(thr_pos))
        if sh_near_pos is not None:
            self.sh_seen_rnd = rnd
            self.sh_seen_pos = sh_near_pos
        if rg_near_pos is not None:
            self.rg_seen_rnd = rnd
            self.rg_seen_pos = rg_near_pos
        # PLANK SAP.  Rank 0 IS "an enemy turret inside d^2 <= 64 of our Core"
        # -- the pattern, not an opponent name.  Seen with this unit's own eyes
        # this round, which is the only sighting that cannot be a ghost.
        self.sap_seen = (thr_pos if (SAP_ON and thr_rank is not None
                                     and thr_rank[0] == 0) else None)
        # PLANK LPECK, THE WALK (cont.).  Strictly BELOW a real turret: a
        # Sentinel is doing 9 HP a round to the Core and the launcher is not.
        # `_sap` re-checks SAP_BAND_DSQ (d <= 8) itself, so the wider
        # LP_NEAR_DSQ sighting cannot pull the defender further out than the
        # measured band; and the launcher already lifts the detector into
        # PRESSURE on its own, because SAP_TARGET_TYPES -- which is what
        # `arch_s1` tests -- has always contained LAUNCHER.
        if (SAP_ON and LP_ON and LP_SAP_TARGET_ON
                and self.sap_seen is None and lp_seen_pos is not None):
            self.sap_seen = lp_seen_pos
        # PLANK EARLYBIRD, THE PUBLISH, and it is HERE and not inside
        # `_eb_note` because of the defect the first smoke leg found -- see
        # §25.1.  Slot 13 has one canonical writer per round and it is
        # `_arch_note`; a second write from `_eb_note` inside the sensing loop
        # was silently undone by it three lines later, because `_arch_note`
        # rebuilds the word from LAST round's buffered read and the bit had
        # not landed yet.  The bit therefore travels INTO `_arch_note` as an
        # argument.  It is also RE-ASSERTED every round until this body reads
        # it back set: `_sge_core_band` and `_fin_publish` write the same slot
        # from their own stale reads, so a single write can still be lost, and
        # for a STICKY classification "eventually" is the only guarantee worth
        # having.
        eb_pub = False
        if EB_ON and EB_PUB_ON and self.eb_seen and not self.eb_pub_done:
            try:
                if ct.read_store(SLOT_ARCH_SEEN) & EB_PUB_BIT:
                    self.eb_pub_done = True
                else:
                    eb_pub = True
            except Exception:
                eb_pub = False
        if ARCH_ON and (arch_s1 or arch_s2 or arch_s3 or arch_s5):
            self._arch_note(ct, pressure=arch_s1, intruder=arch_s3,
                            turret_anywhere=arch_s2, near_count=arch_s5,
                            eb=eb_pub)
        elif eb_pub:
            self._eb_publish(ct)
        if self.enemy is None:
            self.enemy = unpack_pos(ct.read_store(SLOT_ENEMY_CORE))

        # PLANK P3 SIEGE, FIX B.  The enemy-Core HP band is RE-DERIVED by every
        # body that can actually SEE a Core tile, every round -- not latched by
        # whichever established raider happened to look on the round it changed.
        # `_sge_core_band` is memoised on the round, so for a raider this is the
        # call `_raid_beat` would make a few frames later and costs nothing
        # twice; for an expander or the home defender it is what keeps its own
        # answer honest if it ever ends up near their Core.  The gate is one
        # integer compare against builder vision (r^2 = 20) -- a body that
        # cannot possibly see the Core never runs the four vision tests.
        # `self.enemy` only, never the symmetry guess: `_enemy_anchor` would
        # cache a guessed anchor onto a body that has never seen the Core and
        # that anchor also feeds the detector's S5 signal above.
        if (SIEGE_BAND_ALLSEE_ON and self.enemy is not None
                and self._sge_band_armed()
                and dsq_core(p, self.enemy) <= SIEGE_BAND_VIS_DSQ):
            self._sge_core_band(ct, self.enemy)

        self._sync_harvesters(ct)

        # PLANK SEATHOLD, THE EVICTION DETECTOR.  Read BEFORE `self.last` is
        # overwritten, and it costs no API call at all: a builder cannot
        # displace more than a king move (d^2 <= 2) under its own power, so
        # d^2 >= SH_JUMP_DSQ against its own previous position IS a launcher
        # throw.  Same scale-free test tools/elite_loss_decode.py runs on
        # THEIR throws; nothing about it depends on map size or on seeing the
        # launcher.  Only a body that was holding a station cares.
        if (SH_ON and self.last is not None and self.sh_seat is not None
                and p.distance_squared(self.last) >= SH_JUMP_DSQ):
            self._sh_thrown(ct, rnd)

        if self.last == p:
            self.stuck += 1
        else:
            self.stuck = 0
            self.wall = None
        self.last = p

        # WAVE 22, ARM A1 -- BAND A'S SECOND TURRET RIDER (OPENING.md 5.2, B4).
        # Band A runs two economy bodies and TWO turret riders under a cap of
        # four, so seat 3 leaves at once instead of waiting on the harvester
        # shell.  Resolved here rather than in the roster block above because
        # the band is a function of `self.core`, which is not known until the
        # Core anchor has been found a few lines earlier.  Band B and band C
        # are untouched and keep the parent's state-gated transition below.
        if (OPEN_ON and self.role == "expand" and self.role_n == 3
                and not self.link_queue and self._op_band_a(ct)):
            self.role = "raid"
            self.raid_slot = ct.read_store(SLOT_RAID_N)
            ct.write_store(SLOT_RAID_N, self.raid_slot + 1)

        # SEAT 3 joins the raid once the harvester shell exists.  This is the
        # only role transition in the file and it is state-gated, not clocked.
        #
        # WAVE 22 ARM A5, ARM 1 -- AND THIS LINE IS A MEASURED DEFECT FIX, not
        # a precaution.  The rule above is stated as one-way and is not: it
        # re-reads `self.role` every round, so a body ARM 1 had just converted
        # to an expander was flipped straight back to a raider on the very next
        # turn.  `tools/worker.py` on nordkap/seed 204 printed `END home` FIFTY
        # times from one body oscillating at (7,14).  The cost is not the
        # print -- it is that `_rep_crew`, `_rep_min_dmg` and `_rep_tick`'s
        # detour all read `self.role` ABOVE the role split, so the recalled
        # body was refused the repair work ARM 1 exists to hand it.  Under a
        # fired endgame the defection is closed: the siege is over and there is
        # nothing to defect to.
        if (
            self.role == "expand" and self.role_n == LOKI_LATE_RAID_SEAT
            and not self.link_queue and ct.read_store(SLOT_HARVESTERS) >= ECO_NEED
            and not (END_ON and END_QUIT_ON and self._end_fired(ct))
        ):
            self.role = "raid"
            self.raid_slot = ct.read_store(SLOT_RAID_N)
            ct.write_store(SLOT_RAID_N, self.raid_slot + 1)

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
        # INTEGRATION NOTE (loki_leap18).  A1 OPENING and A6 RING both rank an
        # own-socket action at this point.  A1 runs FIRST, on a deadline
        # argument: the prefill's registered bar is "= 2 @r10 on >= 2 faces"
        # with the sockets occupied by r3 (PREFILL_RND), so a round lost here
        # is a bar failed outright, while RING's refill window is 5 rounds
        # (RING_REFILL_RNDS) and its evict is a 20-round peck campaign
        # (RING_EVICT_TRY_RNDS) -- a deferred round costs one peck of fifteen.
        # The pre-emption window is empty in practice: `_op_prefill` can only
        # claim the turn until the 2 sockets are filled (r0-r3), and
        # `_ring_refill`/`_ring_evict` cannot fire until an ENEMY building is
        # standing on one of our sockets, which the 0033 corpus first records
        # at r7.  Composition is by design, not by luck: RING_FLOOR_OWN is an
        # ABSOLUTE census of own buildings on own sockets, so A1's two prefill
        # conveyors ARE two ring claims and the untriggered floor is already
        # satisfied when A1 is done -- RING lays nothing further until its own
        # trigger fires.  See PLAN.md A2.4: A1 and A6 meet for the first time
        # in this build and stage 3 is where the cancellation is measured.
        # WAVE 22, ARM A1 -- THE PREFILL AND THE FEEDER, and they are ranked
        # HERE -- below the emergency Core heal, above every other economy or
        # raid action -- for the reason OPENING.md 2.3 gives: socket
        # OCCUPANCY is two builder-actions and 8 Ti, it caps the enemy's seal
        # at 6 by engine E3 whether or not a single stack ever flows, and it
        # fits in every band on every map.  The feeder behind it is built
        # CORE-OUTWARD, harvester last, so nothing is ever buffered (engine A)
        # and the socket is occupied at r2 rather than r8.  Both calls are
        # ACTION-only, never the move, and both refuse themselves in one
        # boolean on every body that does not own a line -- which is seat 0,
        # seats 3+, the defender and every raider.
        if OPEN_ON and ct.get_action_cooldown() == 0:
            if self._op_prefill(ct, rnd):
                return
            if self._op_trunk(ct, rnd):
                return
        # WAVE 22 TRACK 3, PLANK RING -- THE THREE ACTIONS, ranked HERE:
        # below the emergency Core heal (that is the game being lost this
        # round) and above LPECK, SAP, SEATHOLD, REPAIR and the whole role
        # split.  The ranking IS the arm, and the forensics price it: our
        # builders spent 974 attacks on buildings and 907 on turrets over the
        # 15 ladder games and bought 28 besiegers and THREE cleared sockets
        # out of 65, while 5 of our 8 sockets sat under an enemy building at
        # the end of the median game.  This plank re-spends a small, bounded
        # slice of exactly that budget on the doorway.
        #
        #   REFILL first, because the window is five rounds and a socket
        #     cleared and left open is simply re-bricked;
        #   EVICT second, and it REFUSES ITSELF unless the retake is funded;
        #   CLAIM last, chain-guarded and floor-funded, so the trunk is never
        #     the thing that pays for a tile.
        #
        # Each refuses itself in one or two integer tests on every body that
        # is not standing beside our own ring, which is most bodies most
        # rounds.
        if RING_ON and ct.get_action_cooldown() == 0:
            if self._ring_refill(ct, rnd):
                return
            if self._ring_evict(ct, rnd):
                return
        # THE CLAIM IS NOT HERE.  It is ranked inside `_expand`, below every
        # action that BUILDS or KEEPS the economy, in `SG_SELF_FILL`'s own slot
        # and on `SG_SELF_FILL`'s own argument: denying a seat is worth 3 Ti,
        # but it may never pre-empt a conveyor.  Ranked at this height instead
        # the screen measured `titanium_collected@r100` falling 410 -> 150
        # median -- the trunk paying for the doorway, which is the one way this
        # arm loses a game it would otherwise win.  Refill and evict stay up
        # here because they are about a tile we have ALREADY lost: the refill
        # has a five-round window and the evict refuses itself unless the
        # retake is already funded.
        # PLANK SAP.  Above the role split, below the emergency heal: a body
        # standing on a heal seat is already answering the siege the only way
        # it can (+4 HP for 1 Ti), and it should keep doing that while its
        # action is free.  Everything below this line is economy or raid, and
        # neither of them is worth more than the turret currently doing 9 HP a
        # round to the Core.
        # PLANK LPECK.  Deliberately does NOT claim the turn -- it spends the
        # ACTION only and lets the body make its normal move, because `_expand`
        # and `_raid` both re-check `get_action_cooldown()` before every build.
        # An enemy launcher orthogonally adjacent to one of our bodies is the
        # cage's delivery and eviction engine standing in melee range at 30 HP;
        # 15 pecks delete it and every one of them is otherwise-wasted action.
        # Above SAP because SAP will happily spend the same action on a 60 HP
        # Sentinel two tiles further out.
        if LP_ON:
            self._lp_peck(ct)
        # PLANK EARLYBIRD, ARM (c), THE BRICK.  Directly BELOW LPECK and on
        # exactly its terms: the ACTION only, never the move, and `_lp_peck`
        # having spent the action is caught by this one's own cooldown test.
        # Below the launcher because the launcher is what throws us off the
        # seat and the brick is what fills it; above everything else because a
        # barrier on our own collar is a delivery socket we have already lost.
        # The incumbent tree can only reach this peck from `_sh_act`, i.e. by
        # the ONE stationed body, and only after the launcher and both heals
        # have declined -- which is why the wave-16 corpus shows their bricks
        # standing on our ring for the rest of the match.
        # LEAP16 CONSOLIDATION, REMOVAL 2a.  EB_PECK_ON was killed at the
        # neutral cut (wave 19 track 1 shipped DETECTOR+GUN only) and has been
        # False ever since.  Call site removed; `_eb_peck` keeps its own head
        # guard and is now unreferenced.
        # PLANK RG, THE REACTIVE RING GUNNER.  Like LPECK it does NOT claim the
        # turn -- it spends the ACTION and lets the body walk -- and like LPECK
        # it sits ABOVE SAP, for one reason that is arithmetic rather than
        # taste: SAP's action buys 2 damage this round, and this action buys a
        # ONE-TIME 30 Ti building that then does 7 damage a round, for ever, to
        # the only class of enemy our builders physically cannot touch.  The
        # gate inside is narrow (an enemy BUILDER inside d <= 8 of our Core, a
        # window, a titanium floor and a hard cap of one gun a match), so on
        # every turn where the plank is not the answer this line costs one
        # boolean.  Raiders are excluded: LOKI-QUIET is not in dispute and the
        # gun must stand at home.
        if RG_ON and self.role != "raid" and ct.get_action_cooldown() == 0:
            self._rg_gun(ct, rnd)
        if SAP_ON and self._sap(ct):
            return
        # PLANK SEATHOLD.  BELOW SAP, on purpose and pre-registered as risk R2:
        # a besieging turret in the home band is doing 9 HP a round to the Core
        # and killing it is CT-2, which outranks any one seat -- and with
        # SH_BODIES = 3 the other stations stay manned while the defender walks.
        # ABOVE the role split and above REPAIR, because a body standing on a
        # contested delivery seat is answering the upstream cause of both.
        if SH_ON and self._sh_hold(ct, rnd):
            return
        # PLANK REPAIR (P1).  Below the emergency Core heal and below the
        # besieger peck -- both of those are the game being lost right now --
        # and ABOVE the role split, which is the whole point: turbo7's chain
        # medic lives inside `_expand`, so a `defend` body standing on a
        # bleeding harvester never healed it and neither did a raider until it
        # fell through.  Repair rate 6.8 % against a 40.5 % field is what that
        # ranking measures.  A body carrying a trunk chain is exempt
        # (REPAIR_CHAIN_GUARD) and keeps the old, lower-ranked medic instead.
        # The destroyed-tile memory runs for EVERY body, not only the eligible
        # ones: the trunk builder carrying a chain is the body that watches the
        # trunk, and it is the one `_rep_tick` refuses (chain guard) while
        # `_l4_repair` still reaches `_rep_gap2` from inside `_expand`.
        if REPAIR_ON and REPAIR_REBUILD_ON and REPAIR_GAP2_SEEN_ONLY:
            self._rep_watch(ct, rnd)
        if REPAIR_ON and self._rep_tick(ct):
            return
        # WAVE 22 ARM A4 -- THE SIPHON TAP (sip.py).  Ranked BELOW every
        # survival line above it (the emergency Core heal, the melee recall,
        # LPECK, SAP, SEATHOLD, REPAIR) and ABOVE the role split, for the same
        # reason SEATHOLD sits there: the carrier is a post-cap-lift forward
        # body whose alternative use of this round is ordinary raid work, and
        # the plank's own gates -- band, `arrival`, seat, funding, stall --
        # decide whether it is worth more than that.  It is inert in three
        # comparisons on every round it does not fire, and `SIPHON_ON = False`
        # makes it one.
        #
        # INTEGRATION NOTE (loki_leap18) -- A4 SIPHON vs A5 END, and this is a
        # REAL conflict, not a cosmetic one.  A5's ARM 1 (`END_QUIT_ON`)
        # retires the whole forward tree with ONE test at the top of `_raid`.
        # This hook is ABOVE the role split, so `_raid` is never reached when
        # the tap claims the turn -- an un-gated tapper would keep standing in
        # THEIR ore field for the last 300 rounds of the match, which is
        # precisely the body A5 exists to walk home ("a body standing at their
        # ring delivers nothing", doctrine.py A5 section 2(c)).  A5's latch is
        # quoted as one-way and permanent, so it outranks.
        #
        # The cost of yielding is close to zero and that is why this is the
        # right way round: a COMPLETED tap is a BUILDING and keeps taking its
        # 1/(n+1) of a team-blind round robin with no body present at all (83
        # of 112 corpus taps outlived their builder; median service life 110
        # rounds).  Only an INCOMPLETE chain is abandoned, and an incomplete
        # chain is a dead end that delivers nothing either way.
        #
        # Direction matters: this gate can only make A4 SMALLER in the
        # integration build, never larger, and it adds no forward behaviour of
        # its own.  With END_ON False it is one boolean and A4 is untouched;
        # with SIPHON_ON False A5 is untouched.  Stage 3 (PLAN.md 3.3.6) is
        # where the pair is measured.
        if (SIPHON_ON and not (END_ON and END_QUIT_ON and self._end_fired(ct))
                and self._sip_tick(ct)):
            return
        if self.role == "raid":
            self._raid(ct)
        elif self.role == "defend":
            self._defend(ct)
        else:
            self._expand(ct)
        # T5 PLANK Z.  One more pass for a turn that spent nothing.
        if T5_ZERO_IDLE_ON:
            self._t5_zero_idle(ct)

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

    # ------------------------------------------------------------------
    # THE SHARED ARCHETYPE DETECTOR (analysis/archetype_detector.md)
    # ------------------------------------------------------------------

    def _arch_stamp(self, rnd):
        """round+1, clamped into the ten bits the slot gives it.

        0 therefore means "never seen" rather than "seen on round 0", and
        because the game is capped at 1000 rounds the value never wraps -- so
        every age comparison below is plain subtraction, not modular.
        """
        s = rnd + 1
        return s if s < 1023 else 1023

    def _arch_note(self, ct, pressure=False, intruder=False,
                   turret_anywhere=False, near_count=0, eb=False):
        """Record evidence in SLOT_ARCH_SEEN.  Any unit may call this.

        Read-modify-write, because the slot carries four independent fields
        and a writer with fresh evidence for one of them must not zero the
        other three.  Two writers in the same round both read last round's
        value and the later one wins; the signals all repeat, so a lost update
        costs at most a round of latency on a 60-round memory.
        """
        if not ARCH_ON:
            return
        v = ct.read_store(SLOT_ARCH_SEEN)
        pr = v & 0x3FF
        it = (v >> 10) & 0x3FF
        s2 = (v >> 20) & 1
        s5 = (v >> 21) & 0x1F
        if pressure or intruder:
            st = self._arch_stamp(ct.get_current_round())
            if pressure:
                pr = st
            if intruder:
                it = st
        if turret_anywhere:
            s2 = 1
        if near_count > s5:
            s5 = near_count if near_count < 31 else 31
        # PLANK P3: carry bits 26-31 through.  This rebuild drops everything
        # above bit 25, which would erase the enemy-Core HP band a raider
        # published there.  Inert with the SIEGE flags off -- nothing else in
        # the tree ever sets a bit above 25, so the mask contributes 0 and the
        # word written is bit-identical to the parent's.
        nv = (v & ARCH_KEEP_HI) | (s5 << 21) | (s2 << 20) | (it << 10) | pr
        # PLANK EARLYBIRD rides IN, rather than writing the slot itself.  The
        # rebuild above carries bits 26-31 through from `v`, which is last
        # round's word -- so a bit set by a separate `write_store` earlier in
        # THIS round is not in `v` and is erased here.  That is exactly the
        # defect P4 SIPHON found for the HP band and it is re-found once per
        # plank that forgets it (§25.1).
        if eb and EB_ON and EB_PUB_ON:
            nv |= EB_PUB_BIT
        if nv != v:
            ct.write_store(SLOT_ARCH_SEEN, nv)

    def _arch_classify(self, ct, rnd, s1_now):
        """CORE ONLY.  Publish the archetype in SLOT_ARCHETYPE.

        `s1_now` is this round's own sighting: the store lags one round, and
        the whole point of PRESSURE winning ties is that it must not be late.
        """
        if not ARCH_ON:
            return
        v = ct.read_store(SLOT_ARCH_SEEN)
        pr = v & 0x3FF
        it = (v >> 10) & 0x3FF
        s2 = (v >> 20) & 1
        s5 = (v >> 21) & 0x1F
        now = rnd + 1
        if s1_now or (pr and now - pr <= ARCH_MEMORY):
            code = ARCH_PRESSURE
        elif rnd < ARCH_R_MACRO:
            code = ARCH_DEFAULT
        elif not s2 and not (it and now - it <= ARCH_MEMORY):
            code = ARCH_MACRO
        elif s5 >= ARCH_S5_MANY:
            code = ARCH_MACRO_WEAK
        else:
            code = ARCH_DEFAULT
        if code == self.arch_code:
            return                      # per-unit, so the log is transitions
        self.arch_code = code
        self.arch_set = self._arch_stamp(rnd)
        if ARCH_LOG_ON:
            print("ARCH %s r=%d" % (ARCH_NAMES[code], rnd))

    def _arch_bits(self):
        """The Core's classification, packed for the top half of slot 9.

        Returned rather than written, because slot 9 is written in exactly two
        places in `_core` and both of them must carry it -- a second
        `write_store` to the same slot in the same round would simply replace
        the beacon.
        """
        if not ARCH_ON:
            return 0
        return (self.arch_set << (ARCH_SHIFT + 2)) | (self.arch_code << ARCH_SHIFT)

    def _archetype(self, ct):
        """The published archetype, as read by any unit."""
        if not ARCH_ON:
            return ARCH_DEFAULT
        return (ct.read_store(SLOT_ARCHETYPE) >> ARCH_SHIFT) & 3

    # ------------------------------------------------------------------
    # PLANK P3 SIEGE -- just-in-time ammunition (CORE ONLY)
    # ------------------------------------------------------------------

    def _sge_jit(self, ct, rnd, ti, ammo, under, home_guns, fwd_guns,
                 weapons_top, live_turrets, tw_guns=0):
        """The whole ammunition policy when AMMO_JIT_ON.

        Three measured failures, one method (top5_pipeline.md (f)2):

        OPENING LATE.  100 % of top-5 sides convert on r1 (median r1, q3 r14);
        we open on r11 because every conversion in the parent is gated on
        `under or weapons_top or harv >= 2` and the second harvester is the
        first of those to be true.  The precondition is dropped and every bank
        floor is kept, so the opening build order is protected by exactly the
        reserve that protected it before.

        BANKING WHAT NOTHING CAN FIRE.  The parent asks for `min(120, 40 +
        20*fwd)` -- sixty rounds of magazine on one tube.  The target here is
        SIEGE_JIT_HORIZON rounds of what the turrets on the books actually
        consume: a Sentinel is 10 ammo on a 2-round reload and a Gunner 4 on a
        1-round reload.  The SCREEN_ON allowance is added with the tube because
        the screen gunner is invisible to the Core and to slot 8 alike, and a
        gunner nobody budgets for is a gunner with an empty magazine.

        DEAD CAPITAL.  We hold 24 unspent at r100 and 59.5 at r200 against
        their 16-20 all game.  A magazine that has not FALLEN in
        SIEGE_JIT_IDLE_RNDS rounds is not being fired by anything alive,
        whatever the comm store believes -- the same census the T4 ghost brake
        uses, on a spending window instead of a rubble window -- so above
        SIEGE_JIT_IDLE_CAP we stop buying until it moves.  Self-clearing: one
        shot resets the counter.

        `home_guns` / `fwd_guns` / `weapons_top` arrive ALREADY braked by the
        T4 ghost-magazine test in `_core`, so rubble is not fed here either.
        """
        if self.sge_ammo_prev is None or ammo < self.sge_ammo_prev:
            self.sge_ammo_idle = 0
        else:
            self.sge_ammo_idle += 1
        self.sge_ammo_prev = ammo
        if rnd < SIEGE_JIT_OPEN_RND:
            return
        if (ammo >= SIEGE_JIT_IDLE_CAP
                and self.sge_ammo_idle >= SIEGE_JIT_IDLE_RNDS):
            return
        burn = (SIEGE_JIT_SENT_BURN * fwd_guns
                + SIEGE_JIT_GUN_BURN * home_guns)
        if SCREEN_ON and fwd_guns:
            burn += SIEGE_JIT_GUN_BURN
        if TW_ON and TW_GUN_ON and tw_guns:
            # TERMINAL WEAPONS W1, and the SCREEN_ON line above is the precedent
            # for it: a forward gunner is invisible to the Core and to slot 8
            # alike, and a gunner nobody budgets for is a gunner with an empty
            # magazine.  It raises the TARGET, never the priority -- the pool is
            # global and undifferentiated, so "after the tubes" is enforced at
            # the build (raid ladder step 3d, tube bank floor) and not here.
            burn += TW_GUN_BURN * tw_guns
        target = SIEGE_JIT_HORIZON * burn
        if target < SIEGE_JIT_MIN:
            target = SIEGE_JIT_MIN
        if under and target < SIEGE_JIT_UNDER:
            target = SIEGE_JIT_UNDER
        # PLANK FIN (a), THE AMMO SURGE.  While their ring is sealed their Core
        # heals ~0, so every point a tube lands is PERMANENT -- this is the one
        # window in the game where a fat magazine is not dead capital, and the
        # measured failure of wave 9 is that the window came and the pipe kept
        # trickling.  Gated on `weapons_top` (the T4-braked census) so a
        # magazine is never bought for rubble, and the idle brake above is
        # deliberately left in front of it: a magazine that is not FALLING is
        # not being fired, window or no window.
        fin = bool(FIN_ON and FIN_AMMO_ON and weapons_top
                   and self._fin_window(ct, rnd))
        if fin and target < FIN_AMMO_TARGET:
            target = FIN_AMMO_TARGET
        if ammo >= target:
            return
        # Bank floors, unchanged from the parent -- this arm buys ammunition
        # earlier and in smaller pieces, it does not buy it out of the economy.
        ti_floor = 12 if (under or weapons_top) else 52
        if E1_AMMO_FLOOR_ON and not under:
            ti_floor = max(
                ti_floor,
                min(ct.get_harvester_cost(), E1_RESERVE_CAP) + E1_HARV_RESERVE_MARGIN,
            )
        # WAVE 22 ARM A5, ARM 2, THE PIPE HALF.  `titanium_collected` counts
        # stacks that arrived; ammunition moves none and scores in no tiebreak
        # (engine_mechanics.md A / L).  So once the endgame has fired the
        # conversion may not take the bank below the price of the next
        # harvester and its first conveyors.  A FLOOR ON THE SPEND, not a cap
        # on the target -- the magazine we want is unchanged.  SUSPENDED while
        # `under`, because a dry turret with a besieger on its ray is the one
        # case where the magazine outranks the next harvester, and the
        # `CB_DRY_MAG_ON` clause below is still free to pull the floor back
        # underneath this one.
        if (END_ON and END_AMMO_SUBORD_ON and not under
                and self._end_fired(ct)):
            end_floor = self._end_eco_floor(ct)
            if ti_floor < end_floor:
                ti_floor = end_floor
        if PAIR_ON and PAIR_JIT_RESERVE and not under and not fin \
                and self._pr_core_hold(rnd, fwd_guns):
            # PLANK PAIRS arm 3.  A HELD tube is a tube that is not shooting
            # their Core, so the pipe must stop draining the bank into a
            # magazine for it -- the titanium the hold saves is the titanium
            # arm 1 now lets tube 2 be bought with at a floor of
            # SIEGE_MASS_TI_FLOOR.  A FLOOR ON THE SPEND, not a cap on the
            # target: the magazine goal above is untouched (SIEGE_JIT_MIN, 16),
            # so the held tube still buys the shot it needs for their belts and
            # their turrets, which stay legal targets throughout.  Suspended
            # under attack, where home defence outranks the second tube.
            need = ct.get_sentinel_cost() + PAIR_JIT_MARGIN
            if ti_floor < need:
                ti_floor = need
        if (CB_DRY_MAG_ON and under and ammo < CB_DRY_MAG_AMMO
                and (live_turrets or fwd_guns)):
            ti_floor = min(ti_floor, CB_DRY_MAG_TI_FLOOR)
        # PLANK FIN (a).  The float, and it is the last word on the floor: a
        # window is 20-40 rounds long and a tube that goes quiet inside one is
        # the whole cost of the plank.  Still a FLOOR -- ~20 Ti stays banked,
        # which is a barrier, a heal and change for whatever the raid needs.
        if fin and ti_floor > FIN_TI_FLOAT:
            ti_floor = FIN_TI_FLOAT
        if ti <= ti_floor:
            return
        step = SIEGE_JIT_STEP if (weapons_top or fin) else SIEGE_JIT_TRICKLE
        amt = min(step, target - ammo, ti - ti_floor)
        if amt < SIEGE_JIT_MIN_AMT or not ct.can_convert_ammo(amt):
            return
        ct.convert_ammo(amt)
        if FIN_LOG and fin and not self.fin_surged:
            self.fin_surged = True
            print("FIN surge r=%d" % rnd)
        if SIEGE_LOG_ON and not self.sge_jit_logged:
            self.sge_jit_logged = True
            print("SGE jit on")

    # ------------------------------------------------------------------
    # PLANK SAP -- dismantle the besieging turret with builder pecks
    # ------------------------------------------------------------------

    def _sap_read(self, ct, rnd):
        """Where the besieger is: own eyes first, then the team's last word.

        There is no free slot to publish it on (see the SAP block in
        doctrine.py), and none is needed.  A unit that ranked a turret inside
        the home band THIS round has the fact first-hand.  Anything else
        borrows SLOT_THREAT, which already carries the best-RANKED enemy and
        ranks turrets above builders -- gated on the detector's S1/S4 stamp, so
        a tile named twenty rounds ago cannot be believed.
        """
        if self.sap_seen is not None:
            return self.sap_seen
        cand = unpack_pos(ct.read_store(SLOT_THREAT))
        if cand is None:
            return None
        if not (0 <= cand.x < self.mw and 0 <= cand.y < self.mh):
            return None
        pr = ct.read_store(SLOT_ARCH_SEEN) & 0x3FF
        if not pr or (rnd + 1) - pr > SAP_STALE:
            return None
        return cand

    def _sap_eligible(self, ct, cand):
        """Which bodies may be spent on the siege.

        The defender always -- that is the job, and it is the only body that
        ever WALKS to a besieger (see `_sap`).  Raiders never: LOKI-QUIET's
        evidence is about the raider's round and nothing here disputes it.
        An expander only when it is ALREADY orthogonally adjacent
        (`SAP_EXPANDER_REACH = 1`) and has no trunk chain in flight, because an
        abandoned chain is a dead end that delivers nothing at all (eco.py
        `_wire_tick`).  An adjacent peck costs it no movement and no detour.
        """
        if self.role == "defend":
            return True
        if self.role == "raid":
            return SAP_RAIDERS_ON
        if not SAP_EXPANDERS_ON:
            return False
        if SAP_CHAIN_GUARD and self.link_queue:
            return False
        p = ct.get_position()
        return abs(p.x - cand.x) + abs(p.y - cand.y) <= SAP_EXPANDER_REACH

    def _sap_seat(self, ct, tgt):
        """Which of the target's four orthogonal tiles to approach from.

        A Sentinel cannot rotate, and the one it is pointing down is the ray
        toward our Core, so the two neighbours on that axis are the two it can
        name.  Prefer the perpendicular pair; among equals, the nearest.
        Pure geometry -- no extra API calls, and it degrades to "nearest" when
        the axis is ambiguous.
        """
        p = ct.get_position()
        core = self.core
        x_axis = abs(core.x - tgt.x) >= abs(core.y - tgt.y)
        grid = self.map_grid
        best, best_key = None, None
        for dx, dy in CARD_DELTAS:
            qx, qy = tgt.x + dx, tgt.y + dy
            if not (0 <= qx < self.mw and 0 <= qy < self.mh):
                continue
            if grid is not None and grid[qy][qx] == "#":
                continue
            if core.x <= qx <= core.x + 1 and core.y <= qy <= core.y + 1:
                continue
            on_ray = (dy == 0) if x_axis else (dx == 0)
            key = (1 if on_ray else 0, abs(qx - p.x) + abs(qy - p.y))
            if best_key is None or key < best_key:
                best, best_key = Position(qx, qy), key
        return best

    def _sap(self, ct):
        """True if this body spent its turn on the siege.

        Claiming the whole turn is deliberate.  A sapper that walks away the
        moment its action is on cooldown gives the seat back, and the seat --
        not the peck -- is the scarce thing: 20 pecks kill a Sentinel and
        every round spent re-approaching is a round it shoots the Core.
        """
        if not SAP_ON or self.core is None or self.map_grid is None:
            return False
        # PLANK SAP is the PRESSURE branch of the shared detector.  The gate is
        # nearly a no-op -- SLOT_SAP is only written when S1 is true, which is
        # the same condition -- but it is what makes this plank and the MACRO
        # plank in bots/loki_macro one doctrine switch rather than two.
        if SAP_REQUIRE_PRESSURE and self._archetype(ct) != ARCH_PRESSURE:
            return False
        rnd = ct.get_current_round()
        tgt = self.sap_tgt
        if tgt is not None:
            drop = rnd - self.sap_since > SAP_MAX_RNDS
            if not drop:
                seen = False
                try:
                    seen = ct.is_in_vision(tgt)
                except Exception:
                    seen = False
                if seen and self._enemy_type_at(ct, tgt) not in SAP_TARGET_TYPES:
                    drop = True          # killed, recycled, or never there
            if drop:
                if len(self.sap_ban) > 24:
                    self.sap_ban = {k: v for k, v in self.sap_ban.items() if v > rnd}
                self.sap_ban[(tgt.x, tgt.y)] = rnd + SAP_BAN_RNDS
                self.sap_tgt = None
                tgt = None
        if tgt is None:
            cand = self._sap_read(ct, rnd)
            if cand is None:
                return False
            until = self.sap_ban.get((cand.x, cand.y))
            if until is not None and rnd < until:
                return False
            if dsq_core(cand, self.core) > SAP_BAND_DSQ:
                return False
            if not self._sap_eligible(ct, cand):
                return False
            self.sap_tgt = cand
            self.sap_since = rnd
            tgt = cand
        p = ct.get_position()
        if abs(p.x - tgt.x) + abs(p.y - tgt.y) == 1:
            if ct.get_action_cooldown() == 0:
                if ct.get_global_resources() >= 2 + SAP_TI_FLOOR:
                    try:
                        if ct.can_fire(tgt):
                            self._lp_note(ct, tgt)
                            ct.fire(tgt)
                            return True
                    except Exception:
                        pass
                # Broke: nothing to peck with.  The seat is still worth holding
                # and a hurt neighbour is worth 1 Ti.
                if self._heal_adjacent(ct):
                    return True
            return True
        # ONE WALKER, and it is the defender.  Measured on the first build of
        # this plank: with expanders allowed to walk, three of six builders
        # committed to the same besieger on nordkap, one of them oscillated
        # four tiles away for sixty rounds without ever arriving, and the
        # economy finished the game at ten titanium.  An expander therefore
        # only ever pecks a turret it is ALREADY standing next to -- free,
        # because it was going to spend that action on nothing.
        if SAP_WALK_DEFENDER_ONLY and self.role != "defend":
            self.sap_tgt = None
            return False
        if ct.get_move_cooldown() == 0:
            seat = self._sap_seat(ct, tgt)
            self.tgt = seat if seat is not None else tgt
            self._nav(ct, pave=False)
        return True

    # ------------------------------------------------------------------
    # WAVE 15 PLANK SEATHOLD -- hold OUR eight delivery/heal seats with
    # BODIES, and PLANK LPECK.  See the block at the end of doctrine.py.
    # ------------------------------------------------------------------

    def _sh_feeder_keys(self):
        """{(x,y)} of the seats our OWN conveyors deliver through.

        NEVER stationed on.  A body parked on a feeder socket blocks our own
        delivery exactly as an enemy brick does -- we would be doing the
        enemy's work for him, at 1 Ti a round.  `delivery_seats` is the same
        ore-aware chooser `_seat_ban` and the socket guard already use, so
        this plank and those two agree on which tiles are sacred by
        construction.  Cached: the answer only moves if the map memory does.
        """
        if self.core is None or not (self.mw and self.mh):
            return frozenset()
        key = (self.core, self.mw, self.mh, len(self.map_ores))
        if self.sh_feeder_key != key:
            try:
                keep = delivery_seats(self.core, self.mw, self.mh,
                                      self.map_walls, self.map_ores)
            except Exception:
                keep = ()
            self.sh_feeder = frozenset((s.x, s.y) for s in keep)
            self.sh_feeder_key = key
        return self.sh_feeder

    def _sh_ring12_keys(self):
        """{(x,y)} of our full 12-tile collar: the 8 seats + the 4 corners."""
        if self.core is None or not (self.mw and self.mh):
            return frozenset()
        seats = self._home_seat_keys_set()
        return seats | frozenset(
            (c.x, c.y) for c in core_corners(self.core, self.mw, self.mh))

    def _sh_s1_fresh(self, ct, rnd):
        """The detector's S1 stamp: an enemy TURRET seen near our own Core.

        The sibling of `_sg_s3_fresh` (which reads bits 10-19 for the enemy
        BUILDER).  Read, never re-derived -- any unit that saw one wrote it.
        """
        if not ARCH_ON:
            return False
        try:
            pr = ct.read_store(SLOT_ARCH_SEEN) & 0x3FF
        except Exception:
            return False
        return bool(pr) and (rnd + 1) - pr <= SG_S3_FRESH

    def _sh_trigger(self, ct, rnd):
        """Enemy unit or building within d <= 10 of our Core.

        Own eyes THIS round first -- `_builder`'s sensing loop already
        computed the distance -- then the team's shared S1/S3 stamps, so a
        body that has seen nothing itself still gets the Core's eyes.
        """
        if self.sh_seen_rnd == rnd:
            return True
        if not SH_TEAM_SIGNAL_ON:
            return False
        return self._sg_s3_fresh(ct, rnd) or self._sh_s1_fresh(ct, rnd)

    def _sh_cap(self, ct):
        """How many stations the roster may hold right now.

        OFF by default, and the flag exists because the wave-15 smoke MEASURED
        the cost this guard is for (pre-registered risk R1): on frostgate the
        control collected 760 Ti by r100 and the plank collected 0, because
        three of a five-body roster were standing on seats from the first
        sighting -- which on that map lands before the first harvester.  With
        SH_ECO_GATE_ON the roster is SH_BODIES_EARLY until the harvester shell
        exists and SH_BODIES after.  `bots/leap12_eco` is the A/B arm; nothing
        about the default build is changed by this method.
        """
        # PLANK EARLYBIRD, ARM (b).  The eco gate exists because on frostgate
        # a five-body roster stood on seats from the first sighting and the
        # economy finished r100 on zero titanium -- but that first sighting is
        # generic (ANY enemy entity inside d <= 10).  A CONFIRMED cage courier
        # is not that sighting: it is the one opponent whose whole plan is to
        # own these eight tiles by r50, and against it the harvester
        # precondition is the wrong way round.  HONEST NOTE, and it is
        # pre-registered in the doctrine block: with SH_BODIES ==
        # SH_BODIES_EARLY == EB_SH_BODIES == 1 this branch returns the same 1
        # the incumbent returns, so arm (b) SHIPS INERT.  It is written out
        # rather than left implicit so `bots/leap14_eb2` is a one-constant
        # change and wave 14's dose-response gets a clean re-test.
        # LEAP16 CONSOLIDATION, REMOVAL 2b.  EB_SH_ON shipped INERT by its own
        # admission (EB_SH_BODIES == SH_BODIES == 1, so the branch returned the
        # incumbent's number) and was killed with the rest of the waivers.
        # Removing it removes an `_eb_latched` call from the seat-count path.
        if not SH_ECO_GATE_ON:
            return SH_BODIES
        try:
            if ct.read_store(SLOT_HARVESTERS) < SH_ECO_HARV:
                return SH_BODIES_EARLY
        except Exception:
            return SH_BODIES_EARLY
        return SH_BODIES

    def _sh_claim_ok(self, ct, seats, feeders):
        """The id ballot that stands in for the store slot we do not have.

        Slots 0-15 are all multiplexed (see the SAP block), so the SH_BODIES
        cap is settled locally: this body may claim a station only if the
        number already ON one, plus the number of eligible home-side peers
        with a LOWER id, is under the cap.  Deterministic, converges without
        communication, and it cannot reproduce the failure the SAP block
        records -- three of six builders committing to one tile and the
        economy finishing the game on ten titanium.
        """
        cap = self._sh_cap(ct)
        if cap <= 0:
            return False
        me = ct.get_id()
        held = 0
        rank = 0
        try:
            for uid in ct.get_nearby_units():
                if uid == me or ct.get_team(uid) != self.team:
                    continue
                if ct.get_entity_type(uid) != EntityType.BUILDER_BOT:
                    continue
                up = ct.get_position(uid)
                k = (up.x, up.y)
                if k in seats and k not in feeders:
                    held += 1
                elif (uid < me
                      and self.core.distance_squared(up) <= SH_BAND_DSQ):
                    rank += 1
                if held + rank >= cap:
                    return False
        except Exception:
            return False
        return held + rank < cap

    def _op_seat_filled(self, ct, s):
        """WAVE 22, ARM A1: may a body STATION on socket `s`?

        Rule 3/4 of OPENING.md 4.3, and it is the F1.3 falsifier in code: a
        body on a FILLED socket costs zero spawn tiles (the tile is already
        unspawnable) and heals the Core; a body on an EMPTY socket blocks our
        own feeder build and is the wave-20 M3 self-seal, measured at 106-233
        own body-turns per zero-collection game.  Only the two PREFILL sockets
        are restricted -- every other seat keeps the parent's behaviour, so
        this can never leave the plank with no station at all.
        """
        if not OPEN_ON:
            return True
        keys = self._op_socket_keys(ct)
        if (s.x, s.y) not in keys:
            return True
        return self._op_filled(ct, s)

    def _sh_pick_seat(self, ct, feeders):
        """The free non-feeder seat nearest the intruder's approach.

        `_free_seats` already filters on vision, passability and "no bot
        standing there" -- which also means a seat that is ALREADY BRICKED is
        not a candidate: this plank gets there first or not at all (risk R3).
        The ordering is the whole design: their brick lands where their
        builder already is, so the seat facing the intruder is the contested
        one.  Ties go to whichever is nearest to us.
        """
        free = self._free_seats(ct)
        if not free:
            return None
        ref = self.sh_seen_pos
        if ref is None:
            cand = unpack_pos(ct.read_store(SLOT_THREAT))
            if cand is not None and 0 <= cand.x < self.mw and 0 <= cand.y < self.mh:
                ref = cand
        p = ct.get_position()
        ring_seats = self._home_seat_keys_set() if RING_ON else ()
        best, best_key = None, None
        for s in free:
            if (s.x, s.y) in feeders:
                continue
            # INTEGRATION NOTE (loki_leap18).  A1 and A6 ship the SAME body
            # ban with different scope and different softness, and both are
            # applied, because both vetoes only ever `continue`:
            #   A6 `_ring_station_ok` -- ALL 8 sockets, SOFT: it stands down
            #     if the ring carries no filled, free, non-feeder alternative.
            #   A1 `_op_seat_filled`  -- the TWO PREFILL sockets only, HARD.
            # The union is the intended composition (both arms are the same
            # wave-20 M3 finding, 106-233 own body-turns per zero-collection
            # game).  It cannot deadlock the caller: `_sh_pick_seat` already
            # returns None when no seat qualifies, and A1's hard half covers
            # only 2 of 8 sockets so A6's soft fallback keeps the other 6
            # available.  Each veto reads its own master flag internally, so
            # with either master False the other's behaviour is unchanged.
            # PLANK RING, ARM 3.  Never STATION a body on an EMPTY socket: it
            # blocks our own claim and our own feeder on the one tile the arm
            # above is trying to buy, and it is the 260 own-body-turns a game
            # the loss forensics measured.  SOFT -- if the ring carries no
            # filled seat at all the parent's choice stands, because a ban
            # shipped without a conveyor under it hands the seat over faster.
            if RING_ON and not self._ring_station_ok(ct, s, ring_seats, feeders):
                continue
            # WAVE 22, ARM A1: never a body on an EMPTY prefill socket.
            if not self._op_seat_filled(ct, s):
                continue
            dref = 0 if ref is None else abs(s.x - ref.x) + abs(s.y - ref.y)
            key = (dref, abs(s.x - p.x) + abs(s.y - p.y), s.y, s.x)
            if best_key is None or key < best_key:
                best, best_key = s, key
        return best

    def _sh_thrown(self, ct, rnd):
        """This body was just LAUNCHED off its station.  Walk straight back.

        The claim deliberately outlives SH_UNTIL: giving the seat up on a
        clock is exactly what the throw is buying.  The evictor is one of the
        eight neighbours of the seat we lost (pickup is d^2 <= 2; 99.8 % of
        4907 field throws are within 5 once the victim's own move is counted),
        so it is identified here and pecked first for SH_EVICTOR_RNDS.  It may
        already be out of vision -- we were thrown -- in which case the memory
        stays unset and PLANK LPECK's generic launcher ranking does the work.
        """
        seat = self.sh_seat
        self.sh_seat = None
        if seat is None:
            return
        self.sh_back = seat
        self.sh_back_since = rnd
        if SH_LOG:
            print("SH back (%d,%d) r=%d" % (seat[0], seat[1], rnd))
        best, best_d = None, None
        try:
            for bid in ct.get_nearby_buildings():
                if ct.get_team(bid) == self.team:
                    continue
                if ct.get_entity_type(bid) != EntityType.LAUNCHER:
                    continue
                bp = ct.get_position(bid)
                d = (bp.x - seat[0]) ** 2 + (bp.y - seat[1]) ** 2
                if d > SH_EVICT_DSQ:
                    continue
                if best_d is None or d < best_d:
                    best, best_d = (bp.x, bp.y), d
        except Exception:
            best = None
        if best is not None:
            self.sh_evictor = best
            self.sh_ev_since = rnd

    def _sh_peck(self, ct):
        """Peck the best adjacent enemy building from a station.

        The ranking is NOT `_sabotage_prio`'s, and the difference is the
        point: that table ranks a BARRIER last (5), because a raider's barrier
        is a wall in an open field.  A barrier on OUR ring12 is the brick this
        entire plank exists to stop -- 30 HP, 2 damage a peck, 15 pecks -- so
        on a station it ranks second only to the launcher that can throw us
        off it.  The LOKI-QUIET carve-out does not apply here: QUIET's evidence
        is about a RAIDER's round at THEIR ring, and this body's round is
        already committed to the tile it is standing on.
        """
        if ct.get_global_resources() < 2 + SH_TI_FLOOR:
            return False
        p = ct.get_position()
        px, py = p.x, p.y
        ring12 = self._sh_ring12_keys()
        best, best_key = None, None
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
                hp = ct.get_hp(bid)
                if not ct.can_fire(t):
                    continue
            except Exception:
                continue
            if et == EntityType.LAUNCHER:
                pr = 0
            elif et == EntityType.BARRIER and (tx, ty) in ring12:
                pr = 1
            else:
                pr = 2 + SABOTAGE_PRIO.get(et, 6)
            key = (pr, hp if hp is not None else 999)
            if best_key is None or key < best_key:
                best, best_key = t, key
        if best is None:
            return False
        self._lp_note(ct, best)
        try:
            ct.fire(best)
        except Exception:
            return False
        return True

    def _sh_act(self, ct):
        """A stationed body is not idle.  The ladder, in order.

        1. the launcher that can evict us (LPECK), 2. the Core -- 1 Ti for
        +4 HP is the band-sentinel answer and the reason the seats matter,
        3. an adjacent hurt building of ours (their decode shoots our
        CONVEYORS first: 447 conveyor shots before the first core hit),
        4. the brick.
        """
        if ct.get_action_cooldown() != 0:
            return False
        if SH_PECK_ON and LP_ON and self._lp_peck(ct):
            return True
        if SH_HEAL_ON:
            if self._heal_core(ct):
                return True
            if self._heal_adjacent(ct):
                return True
        if SH_PECK_ON and self._sh_peck(ct):
            return True
        return False

    def _sh_hold(self, ct, rnd):
        """True if this body spent its turn holding (or reclaiming) a seat."""
        if self.core is None or self.map_grid is None:
            return False
        if self.role == "raid" and not SH_RAIDERS_ON:
            return False
        # THE ECONOMY GUARD, and it is the first line for a reason (risk R1):
        # a body carrying a trunk chain is NEVER claimed by this plank.  An
        # abandoned chain is a dead end that delivers nothing at all (eco.py
        # `_wire_tick`), which is the same reasoning SAP_CHAIN_GUARD applies
        # one call site above.  A body already ON a station never has a chain,
        # because `_expand` -- the only place `link_queue` is filled -- does
        # not run while it is stationed.
        if SH_CHAIN_GUARD and self.link_queue:
            return False
        seats = self._home_seat_keys_set()
        if not seats:
            return False
        feeders = self._sh_feeder_keys()
        p = ct.get_position()
        here = (p.x, p.y)

        # 1. ON STATION.  Hold: do not move under our own power.  The trigger
        # is RE-CHECKED, which is the economy guard -- when the enemy has been
        # away for the detector's whole 60-round memory these bodies go back
        # to building instead of standing on tiles nobody wants.  The roster
        # ballot is re-run for a body that has NOT already claimed this tile,
        # so an expander that merely walked across a seat cannot pin itself
        # and push the stationed count past SH_BODIES.
        if here in seats and here not in feeders:
            # PLANK RING, ARM 3, the holding half.  A body that is standing on
            # an empty socket releases it instead of holding it -- the same
            # rule as the chooser, applied to the body that is already there,
            # because a claim latched at r12 would otherwise pin the tile for
            # the SH_UNTIL window and no conveyor could ever land on it.
            if RING_ON and not self._ring_station_ok(ct, p, seats, feeders):
                self.sh_seat = None
                return False
            if (rnd < SH_UNTIL and self._sh_trigger(ct, rnd)
                    and (self.sh_seat == here
                         or self._sh_claim_ok(ct, seats, feeders))):
                if self.sh_seat != here:
                    self.sh_seat = here
                    self.sh_since = rnd
                    if SH_LOG:
                        print("SH seat (%d,%d) r=%d" % (p.x, p.y, rnd))
                self.sh_back = None
                self._sh_act(ct)
                return True
            self.sh_seat = None
            return False

        # 2. THROWN, walking back.  Deliberately ABOVE the SH_UNTIL gate.
        if (self.sh_back is not None
                and rnd - self.sh_back_since <= SH_BACK_RNDS):
            b = Position(self.sh_back[0], self.sh_back[1])
            gone = False
            try:
                if ct.is_in_vision(b) and not ct.is_tile_passable(b):
                    gone = True          # they bricked it while we were airborne
            except Exception:
                gone = False
            if gone:
                self.sh_back = None
            else:
                if ct.get_move_cooldown() == 0:
                    self.tgt = b
                    self._nav(ct, pave=False)
                self._sh_act(ct)
                return True

        # 3. TAKE A STATION.
        if rnd >= SH_UNTIL:
            self.sh_seat = None
            return False
        if not self._sh_trigger(ct, rnd):
            self.sh_seat = None
            return False
        if not self._sh_claim_ok(ct, seats, feeders):
            return False
        seat = self._sh_pick_seat(ct, feeders)
        if seat is None:
            return False
        if ct.get_move_cooldown() == 0:
            self.tgt = seat
            self._nav(ct, pave=False)
        self._sh_act(ct)                 # the action is free on the walk in
        return True

    def _lp_note(self, ct, t):
        """Instrument every peck path that can hit an enemy LAUNCHER.

        Called immediately BEFORE the `fire`, from `_lp_peck`, `_sh_peck`,
        `_sabotage_prio` and `_sap` -- four call sites because four different
        planks can be the one standing next to it, and a kill counted in only
        one of them would misreport the plank.

          `LP hit`   once per tile per body: the DIAGNOSTIC.  The wave-15
                     smoke needed it to tell "the plank never fires" apart
                     from "the plank fires and the launcher survives".
          `LP kill`  the peck is 2 damage, so <= 2 HP means this one finishes
                     it.  Never fires on a peck that merely wounds.
        """
        if not (LP_ON and LP_LOG):
            return
        try:
            bid = ct.get_tile_building_id(t)
            if bid is None or ct.get_team(bid) == self.team:
                return
            if ct.get_entity_type(bid) != EntityType.LAUNCHER:
                return
            hp = ct.get_hp(bid)
        except Exception:
            return
        k = (t.x, t.y)
        rnd = ct.get_current_round()
        if k not in self.lp_hit and len(self.lp_hit) < LP_MARK_MAX:
            self.lp_hit.add(k)
            print("LP hit (%d,%d) r=%d" % (t.x, t.y, rnd))
        if hp is not None and hp <= 2:
            print("LP kill (%d,%d) r=%d" % (t.x, t.y, rnd))
            if self.sh_evictor is not None and k == self.sh_evictor:
                self.sh_evictor = None

    def _lp_peck(self, ct):
        """PLANK LPECK.  Peck an adjacent enemy LAUNCHER near our own Core.

        Free by construction: it spends only the ACTION and never the move, so
        an expander walking past one loses nothing.  A launcher near our base
        is the cage's delivery AND eviction engine; it is 30 HP where a
        Sentinel is 60; and unlike the enemy builder standing beside it, it is
        a BUILDING, so we can actually hit it.  The remembered evictor (the
        launcher that threw THIS body off its station) outranks any other.
        """
        if not LP_ON or self.core is None:
            return False
        if ct.get_action_cooldown() != 0:
            return False
        if ct.get_global_resources() < 2 + LP_TI_FLOOR:
            return False
        rnd = ct.get_current_round()
        ev = None
        if (self.sh_evictor is not None
                and rnd - self.sh_ev_since <= SH_EVICTOR_RNDS):
            ev = self.sh_evictor
        p = ct.get_position()
        px, py = p.x, p.y
        best, best_key = None, None
        for dx, dy in CARD_DELTAS:
            tx, ty = px + dx, py + dy
            if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                continue
            t = Position(tx, ty)
            try:
                bid = ct.get_tile_building_id(t)
                if bid is None or ct.get_team(bid) == self.team:
                    continue
                if ct.get_entity_type(bid) != EntityType.LAUNCHER:
                    continue
                if not LP_ANYWHERE_ON and dsq_core(t, self.core) > LP_NEAR_DSQ:
                    continue
                if not ct.can_fire(t):
                    continue
                hp = ct.get_hp(bid)
            except Exception:
                continue
            key = (0 if (ev is not None and (tx, ty) == ev) else 1,
                   hp if hp is not None else 999)
            if best_key is None or key < best_key:
                best, best_key = t, key
        if best is None:
            return False
        self._lp_note(ct, best)
        try:
            ct.fire(best)
        except Exception:
            return False
        return True

    # ------------------------------------------------------------------
    # PLANK EARLYBIRD -- the cage-arrival detector (block at end of doctrine)
    # ------------------------------------------------------------------

    def _eb_ecore(self):
        """THEIR Core anchor, from map symmetry.  Cached.

        `enemy_core_for` is a table of map DIMENSIONS and anchors plus a plain
        point reflection -- terrain, never opponents -- so it answers on round
        1, before any unit of ours has seen their Core, and it cannot go stale
        when somebody ships a new version.  A real sighting (`self.enemy`)
        supersedes it the moment there is one.
        """
        if self.enemy is not None:
            return self.enemy
        if self.eb_ec is None and self.core is not None and self.mw and self.mh:
            try:
                self.eb_ec = enemy_core_for(self.mw, self.mh, self.core)
            except Exception:
                return None
        return self.eb_ec

    @staticmethod
    def _eb_manh(p, o):
        """Manhattan distance from `p` to the nearest tile of a 2x2 Core at `o`.

        NOT a proxy for walking time -- it IS walking time.  A builder bot
        moves one CARDINAL tile on a 1-round move cooldown, so a body standing
        here cannot have left that Core more recently than this many rounds
        ago.  Separable in x and y exactly as `dsq_core` is, and with both
        footprints being 2x2 the same one-tile shrink on each axis measures
        Core-to-Core as well (verified against `tools/eb_probe.py`: fjordgate
        6, nordkap 11, frostgate 13, midgard/ragnarok 46).
        """
        dx = p.x - o.x
        if dx < 0:
            dx = -dx
        elif dx > 1:
            dx -= 1
        else:
            dx = 0
        dy = p.y - o.y
        if dy < 0:
            dy = -dy
        elif dy > 1:
            dy -= 1
        else:
            dy = 0
        return dx + dy

    def _eb_window(self):
        """The map-aware detection window, computed once per unit.

        window = min(EB_EARLY_MAX, max(EB_EARLY_MIN, c2c * 7 // 10)).  It
        bounds the plank's COST, not its purity -- purity is the two
        impossibility tests, which are exact -- so an off-by-one here buys a
        round of tracking, never a false positive.
        """
        if self.eb_win is not None:
            return self.eb_win
        ec = self._eb_ecore()
        if ec is None or self.core is None:
            return EB_EARLY_MIN
        w = (self._eb_manh(ec, self.core) * EB_C2C_NUM) // EB_C2C_DEN
        if w < EB_EARLY_MIN:
            w = EB_EARLY_MIN
        elif w > EB_EARLY_MAX:
            w = EB_EARLY_MAX
        self.eb_win = w
        return w

    def _eb_latched(self, ct):
        """Has the cage signature been confirmed?  Own eyes, then the team's.

        STICKY: the published bit is never cleared, because this is not a
        sighting that ages out like S1/S3 -- it is a classification of the
        opponent's doctrine, and a team that ferried a courier onto our ring
        on round 11 is a launcher-cage team for the rest of the match.  The
        store read is memoised per round; every caller is on a hot path.
        """
        if not EB_ON:
            return False
        if self.eb_seen:
            return True
        if not EB_PUB_ON:
            return False
        try:
            rnd = ct.get_current_round()
        except Exception:
            return False
        if self._eb_rd == rnd:
            return self._eb_val
        self._eb_rd = rnd
        try:
            self._eb_val = bool(ct.read_store(SLOT_ARCH_SEEN) & EB_PUB_BIT)
        except Exception:
            self._eb_val = False
        return self._eb_val

    def _eb_note(self, ct, rnd, eid, ep, d):
        """One enemy BUILDER sighting inside our band.  Latch if it FLEW.

        Called from `_builder`'s sensing loop, which has already established
        `et == EntityType.BUILDER_BOT` and `d <= EB_TRIGGER_DSQ` for free.
        Everything expensive lives here and here is not reached once the latch
        closes or the window shuts -- against an opponent that never throws,
        that is by round 15 at the latest, after which this plank costs one
        boolean a sighting for the rest of the match.
        """
        if rnd > self._eb_window():
            if self.eb_track:
                self.eb_track = {}       # window shut: drop the memory
            return
        if self._eb_latched(ct):
            self.eb_seen = True          # a peer published it; adopt and stop
            self.eb_rnd = rnd
            self.eb_track = {}
            return
        why = None
        m = None
        # SIGNATURE 1 -- THE WALK-CLOCK.  Exact, needs no memory, and it is
        # what catches the big maps: on midgard and ragnarok the first body
        # inside our band stands manhattan 39-41 from their own Core on round
        # 11, which is 28 rounds of walking it did not have.
        ec = self._eb_ecore()
        if EB_WALK_ON and ec is not None:
            m = self._eb_manh(ep, ec)
            if m > rnd + EB_WALK_SLACK:
                why = "walk"
        # SIGNATURE 2 -- THE JUMP.  What catches the SMALL maps, where the
        # walk-clock cannot: on fjordgate the two Cores are 6 manhattan apart,
        # so their opening builders are inside our band on round 1 against
        # every opponent in the pool and the clock is silent by construction.
        # What is never legitimate anywhere is displacement above one tile a
        # round, and a launcher is the only thing in this engine that does it.
        if why is None and EB_JUMP_ON:
            prev = self.eb_track.get(eid)
            if prev is not None:
                dr = rnd - prev[0]
                mv = abs(ep.x - prev[1]) + abs(ep.y - prev[2])
                if dr > 0 and mv > dr:
                    why = "jump"
            if why is None:
                if eid in self.eb_track or len(self.eb_track) < EB_TRACK_MAX:
                    self.eb_track[eid] = (rnd, ep.x, ep.y)
                return
        if why is None:
            return
        self.eb_seen = True
        self.eb_rnd = rnd
        self.eb_track = {}
        # THE PUBLISH IS NOT DONE HERE.  `self.eb_seen` is the signal; the
        # store write happens after `_arch_note`, which is the slot's one
        # canonical writer, and is re-asserted until it reads back set.  See
        # the block in `_builder` and §25.1.
        if EB_LOG:
            print("EB detect (%d,%d) m=%s d=%d why=%s r=%d" % (
                ep.x, ep.y, "?" if m is None else m, d, why, rnd))

    def _eb_publish(self, ct):
        """Set SLOT_ARCH_SEEN bit 30 directly.  The FALLBACK path only.

        Reached when `_arch_note` did not run this round -- i.e. no detector
        signal at all -- which for a body that has already latched can happen
        once the courier walks back out of ARCH_NEAR_DSQ.  A plain monotone OR
        off a stale read is safe here precisely because nothing else wrote the
        slot this round; when something did, the bit rides in as `_arch_note`'s
        `eb` argument instead.
        """
        try:
            v = ct.read_store(SLOT_ARCH_SEEN)
            if not (v & EB_PUB_BIT):
                ct.write_store(SLOT_ARCH_SEEN, v | EB_PUB_BIT)
        except Exception:
            return

    def _eb_peck(self, ct):
        """PLANK EARLYBIRD, arm (c).  Peck an adjacent enemy BARRIER standing
        on our OWN twelve-tile collar.  True = the action was spent.

        Free by construction, on PLANK LPECK's terms: the ACTION only, never
        the move, and `_expand` / `_raid` both re-check the action cooldown
        before every build, so a body walking past a brick loses nothing it
        was using.  A barrier is 30 HP and a peck is 2 damage: fifteen rounds
        for one body, eight for two.  Unlike LPECK's launcher -- which stood
        NEAR our Core for hundreds of rounds and orthogonally adjacent to one
        of our bodies for none, and so could never be killed by adjacency
        alone (§23.5) -- a brick on our collar is standing ON a tile our own
        bodies live on, which is the whole reason it hurts.
        """
        if not EB_ON or not EB_PECK_ON or self.core is None:
            return False
        if self.role == "raid" and not EB_PECK_RAIDERS_ON:
            return False
        # THE LATCH IS THE FIRST TEST, and the order is the CPU budget: this
        # is one memoised store read, it is the test that separates a cage
        # opponent from every other opponent, and against the other kind it is
        # the ONLY line of this method that ever runs.
        if not self._eb_latched(ct):
            return False
        try:
            if ct.get_action_cooldown() != 0:
                return False
            if ct.get_global_resources() < 2 + EB_PECK_TI_FLOOR:
                return False
        except Exception:
            return False
        ring12 = self._sh_ring12_keys()
        if not ring12:
            return False
        feeders = self._sh_feeder_keys()
        p = ct.get_position()
        px, py = p.x, p.y
        best, best_key, best_hp = None, None, None
        for dx, dy in CARD_DELTAS:
            tx, ty = px + dx, py + dy
            if (tx, ty) not in ring12:
                continue
            t = Position(tx, ty)
            try:
                bid = ct.get_tile_building_id(t)
                if bid is None or ct.get_team(bid) == self.team:
                    continue
                if ct.get_entity_type(bid) != EntityType.BARRIER:
                    continue
                if not ct.can_fire(t):
                    continue
                hp = ct.get_hp(bid)
            except Exception:
                continue
            # A brick on a DELIVERY socket is the economy -- a conveyor's
            # facing must be cardinal, so those are the only tiles a trunk can
            # feed the Core from, and one brick there is the whole line.  Any
            # other collar tile is a heal seat or a spawn tile, which is worth
            # less.  Inside a class, finish the wounded one.
            key = (0 if (tx, ty) in feeders else 1,
                   hp if hp is not None else 999)
            if best_key is None or key < best_key:
                best, best_key, best_hp = t, key, hp
        if best is None:
            return False
        try:
            ct.fire(best)
        except Exception:
            return False
        if EB_LOG:
            try:
                rnd = ct.get_current_round()
            except Exception:
                rnd = -1
            if best_hp is not None and best_hp <= EB_PECK_DMG:
                print("EB kill (%d,%d) r=%d" % (best.x, best.y, rnd))
            else:
                print("EB peck (%d,%d) hp=%s r=%d" % (
                    best.x, best.y, best_hp, rnd))
        return True

    # ------------------------------------------------------------------
    # PLANK RG -- the reactive ring gunner (block at the end of doctrine.py)
    # ------------------------------------------------------------------

    def _rg_trigger(self, ct, rnd):
        """An enemy BUILDER BOT within d <= 8 of our Core.  BUILDERS ONLY.

        Own eyes this round first -- `_builder`'s sensing loop already tested
        `et == EntityType.BUILDER_BOT` and the exact distance -- then the
        detector's S3 stamp (slot 13 bits 10-19), which `_arch_note` writes
        from `intruder=arch_s3` and which `_builder` sets from
        `et == EntityType.BUILDER_BOT` and from nothing else.  S1 (turrets
        near our Core) and S2 (turrets anywhere) live in different bits and
        are deliberately NOT read here: a creeper battery is not what this
        gun is for, and `mimic_0033`'s opening is exactly a creeper battery.
        """
        if self.rg_seen_rnd == rnd:
            return True
        if not RG_TEAM_SIGNAL_ON:
            return False
        return self._sg_s3_fresh(ct, rnd)

    def _rg_home_core(self, ct):
        """OUR Core anchor, for a unit that has no `self.core` -- i.e. a
        TURRET.  Found once and cached; a turret never moves, and a gunner's
        vision (r^2 = 13) covers a Core it stands within 2 tiles of."""
        if self.rg_core is not None:
            return self.rg_core
        try:
            for bid in ct.get_nearby_buildings():
                if ct.get_team(bid) != self.team:
                    continue
                if ct.get_entity_type(bid) == EntityType.CORE:
                    self.rg_core = ct.get_position(bid)
                    return self.rg_core
        except Exception:
            return None
        return None

    def _rg_is_mine(self, ct, p):
        """Is THIS turret the reactive ring gun?

        Identified by geometry rather than by a store bit, because there is no
        free slot and none is needed: a GUNNER of ours standing within
        RG_SITE_DSQ of our own Core can only be this plank's, since the two
        other home-turret arms in this tree (`T5_HOME_GUNNER_ON`,
        `SG_RING_TURRET` under `SG_ON`) are both shipped OFF, and a
        counter-battery turret is sited from wherever the defender happens to
        stand and is a SENTINEL first.  Cached: a turret does not move.
        """
        if self.rg_mine is not None:
            return self.rg_mine
        c = self._rg_home_core(ct)
        if c is None:
            return False                 # not cached: the Core may be unseen
        self.rg_mine = dsq_core(p, c) <= RG_SITE_DSQ
        return self.rg_mine

    # ------------------------------------------------------------------
    # WAVE 22 ARM A2 -- GUN DISCIPLINE  (doctrine.py, GD block)
    # ------------------------------------------------------------------
    # Two predicates and three effects, all zero-comm.  Everything here is
    # read from the ENGINE's tile map through get_tile_building_id /
    # get_tile_builder_bot_id -- never `is_tile_empty` (PLAN.md sec 1.5
    # P0-B, the trap wave 20 tripped on in three places), and never from a
    # guessed core footprint (the corrected ownInRay figure is 35.3 %; the
    # published 38.8 % came from a scanner that assumed a 3x3 core, and ours
    # is 2x2 -- reading the engine's own tile map cannot make that mistake).

    GD_FOE = 1
    GD_OWN = 2

    def _gd_ray_owner(self, ct, bp, tiles):
        """Who occupies this ray FIRST?  GD_FOE / GD_OWN / None (nobody).

        A gunner resolves to the NEAREST occupant of its line and does not
        care whose it is (engine_mechanics sec D), so "what is in the ray" is
        the wrong question and "what is FIRST in the ray" is the right one.

        `get_attackable_tiles_from` is documented tile-by-tile in the order
        (1,0),(2,0),(3,0), but this walks the list SORTED BY DISTANCE from
        the post rather than trusting that order: the no-argument
        `get_attackable_tiles()` is row-major in absolute coordinates, which
        is the exact defect `_turret` already carries a comment about, and a
        three-element sort costs nothing.

        WALLS STOP THE RAY (sec D: gunner at (5,4) facing E, wall at (7,4),
        own barrier at (8,4) -> can_fire = [], target None).  A wall tile is
        still listed by the API, so it is filtered here: a tile holding
        neither a building nor a body and refusing passage is terrain, and
        nothing behind it is reachable.

        FAILS CLOSED, and closed means GD_OWN: an unverifiable ray is
        exactly the one that turns out to be pointed at our own delivery,
        and GD_OWN is the answer that refuses the build under BOTH arms.
        """
        try:
            ray = sorted(tiles, key=lambda t: bp.distance_squared(t))
        except Exception:
            return self.GD_OWN
        for t in ray:
            try:
                bid = ct.get_tile_building_id(t)
                if bid is not None:
                    return (self.GD_OWN if ct.get_team(bid) == self.team
                            else self.GD_FOE)
                bot = ct.get_tile_builder_bot_id(t)
                if bot is not None:
                    return (self.GD_OWN if ct.get_team(bot) == self.team
                            else self.GD_FOE)
                if not ct.is_tile_passable(t):
                    return None          # terrain: nothing behind it is ours
            except Exception:
                return self.GD_OWN
        return None

    def _gd_gun_ok(self, ct, bp, facing, tiles=None):
        """May a gunner be BUILT at `bp` facing `facing`?  The A2 gate.

        NO SILENT GUN (GD_SILENT_OFF): an enemy entity must ALREADY be in
        the ray.  43 % of the gunners we built in the ranked v161 games
        never fired a shot in their entire life against Jython 0 of 90, and
        57.6 % of our gunner-rounds looked down an empty line.

        CLEAR LANE (GD_LANE): the first thing in the ray may not be ours.

        The two are separate flags because they are separately falsifiable
        (F3.1/F3.3 against F3.2), even though NO SILENT GUN subsumes CLEAR
        LANE whenever both are up.
        """
        if not GD_ON:
            return True
        if not (GD_SILENT_OFF or GD_LANE):
            return True
        if tiles is None:
            try:
                tiles = ct.get_attackable_tiles_from(
                    bp, facing, EntityType.GUNNER)
            except Exception:
                return False
        if not tiles:
            return False
        who = self._gd_ray_owner(ct, bp, tiles)
        if GD_LANE and who == self.GD_OWN:
            if GD_LOG:
                print("GD veto lane (%d,%d) f=%s" % (
                    bp.x, bp.y, getattr(facing, "name", facing)))
            return False
        if GD_SILENT_OFF and who != self.GD_FOE:
            if GD_LOG:
                print("GD veto silent (%d,%d) f=%s" % (
                    bp.x, bp.y, getattr(facing, "name", facing)))
            return False
        return True

    def _gd_note_shot(self):
        """One fired round, counted on the turret own instance state.

        Zero-comm by construction: the shot count of a given gunner is not
        knowable to any other unit without a store slot, there is no free
        slot, and the store is buffered anyway (sec J) -- so the whole
        silent-gun question is decided by the gunner itself.
        """
        self.gd_shots += 1

    def _gd_foe_in_vision(self, ct):
        """Is anything of theirs visible from this turret at all?

        The scrap rule needs BOTH halves -- zero shots AND an empty horizon.
        A gun that has not fired because the besieger is still walking in is
        not a silent gun, it is a loaded one.  Fails closed (True means
        "something is out there") so an unreadable scan can never cause a
        scrap.
        """
        try:
            for eid in ct.get_nearby_entities():
                if ct.get_team(eid) != self.team:
                    return True
        except Exception:
            return True
        return False

    def _gd_scrap(self, ct, p, turret_type, rnd):
        """NO SILENT GUN, second half.  True = this unit is GONE.

        `destroy` / `self_destruct` is free, uncapped and does not consume
        the action or the move (sec K).  It refunds no titanium but DOES
        hand back the entity cost-scale contribution immediately -- a gunner
        is +20 % on every later build of every type -- so scrapping a gun
        that has never fired is a strictly positive trade the moment we are
        sure it will not fire.

        `self_destruct()` TERMINATES THE UNIT TURN IMMEDIATELY -- nothing
        after it runs (measured on `bots/probe_ferry`, doctrine.py LOKI-42),
        so it is the last call in this method by necessity, and the marker
        is printed before it rather than after.

        Called only after every firing path in `_turret` has declined, so a
        gun with a shot available always takes the shot first.
        """
        if not (GD_ON and GD_SILENT_OFF):
            return False
        if turret_type != EntityType.GUNNER:
            return False
        if self.gd_born is None:
            self.gd_born = rnd
            return False
        if self.gd_shots > 0:
            return False
        if rnd - self.gd_born < GD_SILENT_RNDS:
            return False
        if self._gd_foe_in_vision(ct):
            return False
        if GD_LOG:
            print("GD scrap (%d,%d) age=%d r=%d" % (
                p.x, p.y, rnd - self.gd_born, rnd))
        try:
            ct.self_destruct()
        except Exception:
            return False
        return True

    def _gd_reaim(self, ct, p, turret_type, rnd):
        """CLEAR LANE, second half.  A LATER build plugged the lane.

        This is the 35.3 % column, and the incumbent has no answer to it:
        with nothing hostile in sight `_idle_rotate` deliberately HOLDS the
        reactive ring gun facing (PLANK RG -- swinging at the enemy Core
        anchor draws a line straight across our own ring), so a barrel that
        one of our own conveyors walked in front of on round 40 is still
        pointed at that conveyor on round 400.

        Budgeted, because re-aim churn is a measured defect of ours in its
        own right: 2.4 `place_entity` emissions per gunner against Pivot
        1.3 (evidence_fixes.md sec 2).  GD_REAIM_MAX rotations per life,
        GD_REAIM_MIN_GAP rounds apart, never into the bank floor.

        Ranks a facing whose first occupant is a FOE over one that is merely
        clear, and refuses any facing plugged by us as well.  If no facing
        is better than the one we are on, nothing is bought: a rotate costs
        10 Ti and a round of fire, and "pay to point somewhere else that is
        also wrong" is the churn this budget exists to stop.
        """
        if not (GD_ON and GD_LANE):
            return False
        if turret_type != EntityType.GUNNER:
            return False
        if self.gd_reaims >= GD_REAIM_MAX:
            return False
        if rnd - self.gd_reaim_rnd < GD_REAIM_MIN_GAP:
            return False
        try:
            cur = ct.get_direction()
            if ct.get_global_resources() < RG_ROT_COST + GD_REAIM_TI_FLOOR:
                return False
        except Exception:
            return False
        try:
            cur_tiles = ct.get_attackable_tiles_from(p, cur, EntityType.GUNNER)
        except Exception:
            return False
        if self._gd_ray_owner(ct, p, cur_tiles) != self.GD_OWN:
            return False                 # the lane is not plugged by us
        want, want_key = None, None
        for di, d in enumerate(DIRECTIONS):
            if d == cur:
                continue
            try:
                tiles = ct.get_attackable_tiles_from(p, d, EntityType.GUNNER)
            except Exception:
                continue
            if not tiles:
                continue
            who = self._gd_ray_owner(ct, p, tiles)
            if who == self.GD_OWN:
                continue
            # A live target beats an open lane; a cardinal beats a diagonal
            # (3 tiles against 2, sec D); enumeration order breaks the tie.
            key = (0 if who == self.GD_FOE else 1,
                   0 if d.is_cardinal() else 1, di)
            if want_key is not None and key >= want_key:
                continue
            want, want_key = d, key
        if want is None:
            return False
        try:
            if not ct.can_rotate(want):
                return False
            ct.rotate(want)
        except Exception:
            return False
        self.gd_reaims += 1
        self.gd_reaim_rnd = rnd
        # Keep the incumbent rotate bookkeeping straight: `_idle_rotate` must
        # not think the barrel has been still since round 0 after this.
        self.rot_rnd = rnd
        self.rot_prev_dir = cur
        if GD_LOG:
            print("GD reaim (%d,%d) %s->%s r=%d n=%d" % (
                p.x, p.y, getattr(cur, "name", cur),
                getattr(want, "name", want), rnd, self.gd_reaims))
        return True

    def _rg_ray_clean(self, ct, tiles, core, feeders):
        """FRATRICIDE GUARD.  Rule 9 of the mechanics table, enforced.

        "Turrets hit friendly units, including your own core and your own
        builders" -- a rotated gunner of ours killed one of our own builders
        in six shots and a misaimed sentinel ground our own Core 500 -> 212.
        A gunner hits the NEAREST occupant of its ray and does not care whose
        it is, so a facing is refused outright if its ray contains a tile of
        our own Core footprint, a tile holding one of our own buildings, or
        one of the two FEEDER seats our conveyors deliver through (a tile
        that is empty now and will hold our socket shortly).

        FAILS CLOSED.  If a tile cannot be read, the facing is refused: an
        unverifiable ray is exactly the one that ends up pointed at our
        delivery, and not building is cheaper than 30 Ti aimed at ourselves.
        """
        if not RG_NO_FRIENDLY_RAY:
            return True
        for t in tiles:
            if core is not None and dsq_core(t, core) == 0:
                return False                        # our own 2x2 footprint
            if feeders and (t.x, t.y) in feeders:
                return False                        # our own delivery socket
            try:
                bid = ct.get_tile_building_id(t)
                if bid is not None and ct.get_team(bid) == self.team:
                    return False
            except Exception:
                return False
        return True

    def _rg_gun(self, ct, rnd):
        """Build the ONE reactive ring gunner.  True = the action was spent.

        THE KILL MATH (doctrine block): an intruding builder is 40 HP and must
        stand orthogonally adjacent to a ring tile to brick it; a gunner does
        7 damage a round to the nearest occupant of its three-tile ray, with
        no cooldown, so it is dead in six rounds.  Turrets are the only thing
        in the engine that can damage a builder bot, and their LAUNCHER cannot
        answer -- a launcher throws BUILDER BOTS, and this is a building.
        """
        if not RG_ON or self.rg_done or self.core is None:
            return False
        # PLANK EARLYBIRD, ARM (a).  Three edits, and the third is the only
        # one with teeth.  (i) the opening-build-order floor is waived once
        # the cage signature is confirmed -- at that point their courier is
        # already laying bricks and RG_MIN_RND's argument no longer holds;
        # (ii) so is the titanium floor, which the probe says was never the
        # binding constraint anyway (352-470 Ti in the bank at the sighting
        # round on 8 legs of 10); (iii) THE HOLD -- before the signature, and
        # only inside EB_HOLD_UNTIL, the one-per-match gun is not spent at
        # all.  `tools/eb_probe.py` is why: on fjordgate the incumbent buys
        # it on r4 against a builder standing manhattan 0 from THEIR OWN Core
        # -- a small map, not an intruder -- and that gun then held a target
        # for 3 rounds out of 443.  Past EB_HOLD_UNTIL this method is the
        # incumbent method again, line for line.
        # `eb_latch` is the CLASSIFICATION and `eb` is the waiver.  Kept apart
        # so that turning the waivers off (`bots/leap14_ebonly`) does not
        # silently turn the hold into "hold for ever": the hold asks whether
        # the signature has been seen, never whether arm (a) is armed.
        eb_latch = EB_ON and self._eb_latched(ct)
        eb = eb_latch and EB_RG_ON
        if rnd < (EB_RG_MIN_RND if eb else RG_MIN_RND) or rnd >= RG_UNTIL:
            return False
        # LEAP16 CONSOLIDATION, REMOVAL 2c.  EB_RG_HOLD_ON -- "the arm with
        # teeth" -- was measured to be able to cost the gun outright (risk R1
        # in its own doctrine block) and was cut at the neutral cut.  Gone.
        # `eb_latch` above is KEPT: it feeds `eb`, which is the DETECTOR arm
        # (EB_RG_ON) that wave 18b shipped and that still moves RG_MIN_RND.
        if not self._rg_trigger(ct, rnd):
            return False
        try:
            cost = ct.get_gunner_cost()
        except Exception:
            return False
        # NOT BEFORE THE LINE THAT PAYS FOR IT.  Same lesson `_sg_ring_gun`
        # records: a turret defends an economy, it does not substitute for
        # one.  `_eco_spendable` also holds back the siege heal reserve.
        if not self._eco_spendable(
                ct, cost + (EB_RG_TI_FLOOR if eb else RG_TI_FLOOR)):
            return False
        # THE BUDGET, and it is ONE.  Three independent guards, because a
        # second home gunner is REFUTED TERRITORY in this lineage:
        #   (a) SLOT_HOME_GUN, the monotone home-turret counter every other
        #       turret arm here already maintains -- this is the cross-unit
        #       claim, and it is what stops two builders buying two guns in
        #       the same round.  It counts a counter-battery turret too, and
        #       that is deliberate: if we have already bought a home weapon,
        #       we do not buy a second one.  It is monotone, so a gun that
        #       DIES is not replaced either -- one a match, full stop.
        #   (b) a local scan for a live home gunner, which catches a peer's
        #       build whose store write has not landed yet;
        #   (c) this unit's own latch.
        try:
            if ct.read_store(SLOT_HOME_GUN) >= RG_MAX:
                self.rg_done = True
                return False
        except Exception:
            return False
        for _bp, et, _f in self._home_guns(ct):
            if et == EntityType.GUNNER:
                self.rg_done = True
                return False
        if self._cpu_exhausted(ct):
            return False

        p = ct.get_position()
        ring12 = self._sh_ring12_keys()
        feeders = self._sh_feeder_keys()
        ban = self._seat_ban()
        intr = self.rg_seen_pos if self.rg_seen_rnd == rnd else None
        ikey = None if intr is None else (intr.x, intr.y)
        best, best_key, best_dir = None, None, None
        best_score = 0
        best_cover = 0
        for dx, dy in CARD_DELTAS:
            bx, by = p.x + dx, p.y + dy
            if not (0 <= bx < self.mw and 0 <= by < self.mh):
                continue
            # NEVER ON THE RING.  The twelve ring tiles are our eight
            # delivery sockets / heal seats and the four corners the launcher
            # and the spawner need, and a turret is an impassable building --
            # siting one there does the enemy's sealing for him.
            if RG_OFF_RING and (bx, by) in ring12:
                continue
            if ban is not None and (bx, by) in ban:
                continue
            bp = Position(bx, by)
            dc_site = dsq_core(bp, self.core)
            if dc_site < 1 or dc_site > RG_SITE_DSQ:
                continue
            # WAVE 19, FIX 2 (i) -- COVERAGE, PRECOMPUTED, ONCE PER SITE.
            # A gunner is the only turret that can re-aim, so the property of
            # a POST worth maximizing is not the ray it opens with but the
            # UNION of the rays it can ever swing to.  eb_probe2 measured the
            # cost of getting this backwards: the gun went up at r4 aimed at
            # where the courier stood on r4 and then held a target for 0-8
            # rounds of 500.  `_rg_cover` counts DISTINCT work tiles over the
            # four cardinal facings, and only over facings that pass the same
            # rule-9 test the build itself has to pass -- a ray we would
            # refuse is not coverage we own.
            cover = self._rg_cover(ct, bp, feeders) if RG_COVER_UNION_ON else 0
            for di, d in enumerate(DIRECTIONS):
                try:
                    tiles = ct.get_attackable_tiles_from(
                        bp, d, EntityType.GUNNER)
                except Exception:
                    continue
                if not tiles:
                    continue
                # THE RAY MUST COVER THE TILES THE INTRUDER STANDS ON, WHICH
                # ARE NOT THE TILES IT BRICKS.  This is the defect the first
                # smoke leg found and it cost the plank its kill: a build
                # target must be ORTHOGONALLY ADJACENT to the builder, so a
                # body bricking one of our ring tiles is standing on the shell
                # JUST OUTSIDE the ring (dsq_core 4-8), never on the ring tile
                # it is filling.  A ray scored on ring coverage therefore aims
                # one tile behind the target: on nordkap the gun stood at
                # (7,6) covering ring tiles (8,7) and (9,8), shot both bricks
                # dead -- and the builder that laid them worked the whole
                # sequence from (8,8), (9,9), (10,9), (11,9), never once on
                # the ray.  WORK TILES are ring + shell, 1 <= dsq_core <=
                # RG_WORK_DSQ, and a cardinal facing (3 tiles) covering the
                # shell tangentially is what actually intercepts the body.
                score = 0
                for t in tiles:
                    if ikey is not None and (t.x, t.y) == ikey:
                        score += RG_INTRUDER_BONUS
                    dt = dsq_core(t, self.core)
                    if dt < 1 or dt > RG_WORK_DSQ:
                        continue
                    if intr is None:
                        score += 1
                        continue
                    # Nearer the body we can actually see is worth more: it
                    # walks a tile a round and the ray is three tiles long.
                    m = abs(t.x - intr.x) + abs(t.y - intr.y)
                    score += (RG_NEAR_M - m) if m < RG_NEAR_M else 0
                need = RG_MIN_SCORE if intr is not None else 1
                if RG_COVER_RING_ON and score < need:
                    continue
                # COVERAGE OUTRANKS THE OPENING FACING, and the opening facing
                # still decides between the facings of the winning post -- so
                # the intruder bonus is not lost, it is demoted to a
                # tie-break.  RG_COVER_UNION_ON = False restores wave 18's key
                # exactly (`cover` is then 0 for every site and drops out).
                key = (-cover, -score, dc_site, bx, by, di)
                if best_key is not None and key >= best_key:
                    continue
                if not self._rg_ray_clean(ct, tiles, self.core, feeders):
                    continue
                # WAVE 22 ARM A2.  `_rg_ray_clean` is the FRATRICIDE half and
                # it is kept verbatim; this is the half it never had -- the
                # ray must already CONTAIN one of theirs, not merely be free
                # of ours.  RG_INTRUDER_BONUS scores an intruder ON the ray,
                # but RG_MIN_SCORE can be met by work tiles alone, which is
                # how a post gets bought against a body that is not on the
                # line and never comes.
                if not self._gd_gun_ok(ct, bp, d, tiles):
                    continue
                try:
                    if not ct.can_build_gunner(bp, d):
                        continue
                except Exception:
                    continue
                best, best_key, best_dir, best_score = bp, key, d, score
                best_cover = cover
        if best is None:
            return False
        try:
            ct.build_gunner(best, best_dir)
        except Exception:
            return False
        ct.write_store(SLOT_HOME_GUN, ct.read_store(SLOT_HOME_GUN) + 1)
        self.rg_done = True
        if eb and EB_LOG:
            print("EB gun r=%d" % rnd)
        if RG_LOG:
            print("RG up (%d,%d) f=%s s=%d c=%d r=%d" % (
                best.x, best.y, getattr(best_dir, "name", best_dir),
                best_score, best_cover, rnd))
        return True

    def _rg_cover(self, ct, bp, feeders):
        """WAVE 19, FIX 2 (i).  How many WORK TILES can a gun at `bp` ever hit?

        The union, over the four CARDINAL facings, of the work tiles on each
        facing's ray -- counted DISTINCTLY, so a tile two facings share is one
        tile of coverage and not two.  Cardinals because those are the rays
        that reach three tiles (a diagonal's third tile is d^2 18, outside a
        gunner's 13), and because "cover the collar" is a cardinal question:
        the shell a bricking courier stands on runs orthogonally around us.

        A facing whose ray fails the rule-9 fratricide test contributes
        NOTHING: coverage we would refuse to use is not coverage.  That makes
        this strictly a lower bound, which is the safe direction -- it can
        undersell a post, never oversell one.

        Cost is bounded and paid ONCE, on the build round of a once-a-match
        building: four sites x four facings x <= 3 tiles.
        """
        seen = set()
        for d in CARDINALS:
            try:
                tiles = ct.get_attackable_tiles_from(bp, d, EntityType.GUNNER)
            except Exception:
                continue
            if not tiles:
                continue
            if not self._rg_ray_clean(ct, tiles, self.core, feeders):
                continue
            for t in tiles:
                dt = dsq_core(t, self.core)
                if 1 <= dt <= RG_WORK_DSQ:
                    seen.add((t.x, t.y))
        return len(seen)

    def _rg_ray_safe(self, ct, p, facing):
        """`_rg_ray_clean` for a TURRET, which has no map memory.

        Same rule 9 test, minus the feeder-seat set (that needs the decoded
        terrain a turret never loads).  It is not lost: once our conveyor is
        actually standing on the feeder socket, the own-building test below
        catches it, and before that the socket is empty and safe to shoot
        across.  Fails closed for the same reason.
        """
        if not RG_NO_FRIENDLY_RAY:
            return True
        try:
            tiles = ct.get_attackable_tiles_from(p, facing, EntityType.GUNNER)
        except Exception:
            return False
        return self._rg_ray_clean(ct, tiles, self._rg_home_core(ct), None)

    def _rg_chase(self, ct, p, turret_type):
        """WAVE 19, FIX 2 (ii).  THE CHASE.  True = the barrel moved.

        `_idle_rotate` is a forward tube's discipline and this gun is not a
        forward tube.  It has ONE job -- the enemy BUILDER laying bricks on our
        own collar, the one class of target our own builders physically cannot
        touch -- and against that job the incumbent re-aim has three defects
        eb_probe2 priced at 0-8 target-rounds out of 500:

          1. it computes ONE bearing (`p.direction_to(tgt)`), tests it, tries
             the nearest cardinal if that bearing was diagonal, and gives up.
             A courier two tiles out on a bearing that is neither is never
             chased at all.  Here: ALL EIGHT facings are enumerated and the
             ones whose ray actually CONTAINS the body are kept.
          2. ROTATE_COOLDOWN_RNDS is eight rounds of patience written against
             rotation thrash between distant siege targets.  A courier bricks
             for three or four rounds and leaves.  Here: RG_CHASE_GAP, two.
          3. it has no budget, so the only thing that ever stopped it was the
             cooldown.  Here: RG_ROT_BUDGET titanium for the whole game, on
             the one gun this lineage ever builds.

        AND THE ONE RULE THAT KEEPS THE BUDGET HONEST: no facing whose ray
        lands on the body, no rotation.  A courier standing where no ray from
        this post reaches -- the diagonal case in the brief -- is left alone.
        We do not pay 10 Ti and a round's fire to point at nothing.
        """
        if not (RG_ON and RG_CHASE_ON):
            return False
        if turret_type != EntityType.GUNNER:
            return False
        if not self._rg_is_mine(ct, p):
            return False
        rnd = ct.get_current_round()
        if rnd - self.rg_chase_rnd < RG_CHASE_GAP:
            return False
        if self.rg_rot_ti + RG_ROT_COST > RG_ROT_BUDGET:
            return False
        try:
            cur = ct.get_direction()
            if ct.get_global_resources() < RG_ROT_COST + RG_CHASE_TI_FLOOR:
                return False
        except Exception:
            return False
        # THE TARGET IS A BUILDER AND NOTHING ELSE.  A besieging turret has two
        # other answers in this tree (SAP, the counter-battery) and a barrel
        # spent on one is a collar left unwatched -- which is the ranking
        # `_idle_rotate` already inverts for this gun, kept here verbatim.
        tgt, tgt_d = None, 10 ** 9
        try:
            for eid in ct.get_nearby_entities():
                if ct.get_team(eid) == self.team:
                    continue
                if ct.get_entity_type(eid) != EntityType.BUILDER_BOT:
                    continue
                ep = ct.get_position(eid)
                d = p.distance_squared(ep)
                if d > RG_CHASE_DSQ or d >= tgt_d:
                    continue
                tgt, tgt_d = ep, d
        except Exception:
            return False
        if tgt is None:
            return False
        if self._ray_lands(ct, p, cur, tgt):
            return False                     # already on it: shoot, don't turn
        want, want_key = None, None
        for di, d in enumerate(DIRECTIONS):
            if d == cur:
                continue
            card = d.is_cardinal()
            if RG_CHASE_CARD_ONLY and not card:
                continue
            if not self._ray_lands(ct, p, d, tgt):
                continue
            key = (0 if card else 1, di)
            if want_key is not None and key >= want_key:
                continue
            # THE SAME RULE-9 TEST THE BUILD FACING GOT, and it fails closed.
            # A rotation is a NEW facing; the conveyor laid since the gun went
            # up is exactly the occupant we would be shooting.
            if not self._rg_ray_safe(ct, p, d):
                continue
            want, want_key = d, key
        if want is None:
            return False                     # unreachable: do not burn a rotate
        try:
            if not ct.can_rotate(want):
                return False
            ct.rotate(want)
        except Exception:
            return False
        self.rg_rot_ti += RG_ROT_COST
        self.rg_chase_rnd = rnd
        # Keep the incumbent discipline's books straight even though this path
        # bypasses it: if the chase ever runs out of budget, `_idle_rotate`
        # takes over and must not think the barrel has been still for 400
        # rounds.
        self.rot_rnd = rnd
        self.rot_prev_dir = cur
        self.rot_lock_d = tgt_d
        self.rot_tgt = tgt
        if RG_LOG and RG_CHASE_LOG:
            print("RG chase %s->%s (%d,%d) r=%d ti=%d" % (
                getattr(cur, "name", cur), getattr(want, "name", want),
                tgt.x, tgt.y, rnd, self.rg_rot_ti))
        return True

    def _rg_note_kill(self, ct, t, et):
        """`RG kill (x,y)` -- a shot that takes an enemy BUILDER to <= 0.

        Called from `_turret` BEFORE the shot, because afterwards the entity
        is gone and its HP is unreadable.  Gated on this gunner being the
        reactive ring gun, so a forward tube can never borrow the marker.
        """
        if not (RG_ON and RG_LOG):
            return
        if et != EntityType.BUILDER_BOT:
            return
        try:
            if not self._rg_is_mine(ct, ct.get_position()):
                return
            bid = ct.get_tile_builder_bot_id(t)
            if bid is None or ct.get_hp(bid) > RG_GUN_DMG:
                return
            print("RG kill (%d,%d) r=%d" % (t.x, t.y, ct.get_current_round()))
        except Exception:
            return

    def _sabotage_prio(self, ct):
        """Melee the best adjacent enemy building (2 Ti for 2 damage)."""
        p = ct.get_position()
        px, py = p.x, p.y
        best, best_p, best_et = None, 99, None
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
            # PLANK LPECK, the ranking half.  SABOTAGE_PRIO put the LAUNCHER at
            # 3 -- below the enemy CORE and below a HARVESTER -- which was
            # written before we knew a launcher standing on OUR ring is the
            # cage's eviction engine (609 evictions of our bodies in the decoded
            # corpus, launchers on our ring12 from t28 that never self-destruct).
            # Near our own Core it ranks above everything, per the ask "rank
            # LAUNCHER >= GUNNER near our core"; anywhere else it is unchanged.
            if (LP_ON and et == EntityType.LAUNCHER and self.core is not None
                    and (LP_ANYWHERE_ON or dsq_core(t, self.core) <= LP_NEAR_DSQ)):
                pr = LP_PRIO
            if pr >= best_p:
                continue
            try:
                if ct.can_fire(t):
                    best_p, best, best_et = pr, t, et
            except Exception:
                continue
        if best is not None:
            # PLANK SAP carve-out.  QUIET's evidence is that a RAIDER's peck
            # buys less than its round; a turret standing in our own home band
            # is the opposite case -- it is the thing doing 98.5 % of the
            # damage to our Core, it cannot walk away, and 20 pecks delete it
            # permanently for 40 Ti and no cost-scale.  Everything else stays
            # silenced.
            if LOKI_QUIET_ON:
                if not (SAP_ON and SAP_MELEE_TURRETS_ON
                        and best_et in SAP_TARGET_TYPES
                        and self.core is not None
                        and dsq_core(best, self.core) <= SAP_BAND_DSQ
                        and ct.get_global_resources() >= 2 + SAP_TI_FLOOR):
                    return False      # QUIET: counterbattery melee silenced
            self._lp_note(ct, best)
            ct.fire(best)
            return True
        return False

    def _enemy_type_at(self, ct, pos):
        """EntityType of the enemy standing on `pos` right now, else None."""
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

    def _cb_target(self, ct):
        """(position, EntityType) the home battery should bear on, or (None, None).

        Seen with this unit's own eyes THIS round.  SLOT_THREAT is at best one
        round old -- store writes land next turn -- it is never cleared when
        its subject moves or dies, and in the ladder losses the tile it named
        held no enemy at all on 893 rounds (458 empty, 435 occupied by one of
        OUR buildings).  can_fire_from() happily confirms a ray onto a ghost,
        and a Sentinel cannot rotate, so that one call froze 30 Ti of turret
        onto empty air for the rest of the match.  The store survives only as a
        fallback, and only when the tile it names still holds an enemy.
        """
        rnd = ct.get_current_round()
        if self._cb_rnd == rnd:
            return self._cb_val
        self._cb_rnd = rnd
        self._cb_val = self._cb_scan(ct)
        return self._cb_val

    def _cb_scan(self, ct):
        if self.core is None:
            return None, None
        if not CB_LIVE_TARGET_ON:
            threat = unpack_pos(ct.read_store(SLOT_THREAT))
            if threat is None or dsq_core(threat, self.core) > HUNT_BAND_DSQ:
                return None, None
            return threat, EntityType.BUILDER_BOT
        best, best_rank, best_type = None, None, None
        for eid in ct.get_nearby_entities():
            try:
                if ct.get_team(eid) == self.team:
                    continue
                et = ct.get_entity_type(eid)
            except Exception:
                continue
            r = CB_RANK_ACTIVE.get(et)
            if r is None:
                continue
            try:
                ep = ct.get_position(eid)
            except Exception:
                continue
            d = dsq_core(ep, self.core)
            if d > HUNT_BAND_DSQ:
                continue
            rank = (r, d)
            if best_rank is None or rank < best_rank:
                best, best_rank, best_type = ep, rank, et
        if best is not None:
            return best, best_type
        threat = unpack_pos(ct.read_store(SLOT_THREAT))
        if threat is None or dsq_core(threat, self.core) > HUNT_BAND_DSQ:
            return None, None
        et = self._enemy_type_at(ct, threat)
        if et is None or et not in CB_RANK_ACTIVE:
            return None, None
        return threat, et

    def _home_guns(self, ct):
        """Our live turrets inside the home band, as (pos, type, facing).

        Memoised on the round: _cb_over_heal, _try_counterbattery and the hunt
        move can all ask in the same turn, and this walks every nearby building.
        """
        rnd = ct.get_current_round()
        if self._hg_rnd == rnd:
            return self._hg_val
        out = []
        self._hg_rnd, self._hg_val = rnd, out
        if self.core is None:
            return out
        for bid in ct.get_nearby_buildings():
            try:
                if ct.get_team(bid) != self.team:
                    continue
                et = ct.get_entity_type(bid)
                if et not in CORE_THREAT_TYPES:
                    continue
                bp = ct.get_position(bid)
                if dsq_core(bp, self.core) > HUNT_BAND_DSQ:
                    continue
                out.append((bp, et, ct.get_direction(bid)))
            except Exception:
                continue
        return out

    def _home_gun_bears(self, ct, target, guns=None):
        """Does a live home turret's CURRENT facing already cover `target`?

        LOKI asked only whether a home turret EXISTED.  A Sentinel cannot
        rotate, so one built against a threat that has since walked away is
        dead weight -- and it was nevertheless suppressing its own replacement
        for the rest of the match.  Measured: 1,463 of the 1,544 besieged
        rounds in the ladder losses where we had a home turret had none that
        bore on the besieger.
        """
        if not CB_BEARING_GATE_ON:
            return self._live_home_gun(ct)
        for bp, et, facing in (self._home_guns(ct) if guns is None else guns):
            try:
                if ct.can_fire_from(bp, facing, et, target):
                    return True
            except Exception:
                continue
        return False

    def _cb_over_heal(self, ct):
        """May the defender skip a heal to buy a counterbattery this round?

        Only in the one state where healing provably cannot win: the defender,
        a threat inside the home band, no home turret BEARING on it, and a bank
        that pays for a Sentinel without touching the siege reserve.
        """
        if not CB_OVER_HEAL_ON or self.role != "defend" or self.core is None:
            return False
        target, _ = self._cb_target(ct)
        if target is None:
            return False
        if ct.get_global_resources() < ct.get_sentinel_cost() + SIEGE_HEAL_RESERVE_TI:
            return False
        return not self._home_gun_bears(ct, target)

    def _try_counterbattery(self, ct):
        """Build only a weapon ray that already contains a LIVE besieger."""
        threat, threat_type = self._cb_target(ct)
        if threat is None:
            return False
        # MERGE (turbo5): the HUNT_BAND_DSQ test turbo4 kept here is already
        # applied inside _cb_target/_cb_scan, on the live sighting AND on the
        # store fallback, so dropping it changes nothing but the call count.
        # MERGE (turbo5): every arm below is inside CB_BEARING_GATE_ON, so with
        # that flag down this function reproduces turbo4's exactly -- the cap
        # and the "already bears" refusal are BOTH new constraints and neither
        # may leak into the control leg.
        guns = self._home_guns(ct) if CB_BEARING_GATE_ON else None
        if CB_BEARING_GATE_ON:
            cap = CB_HOME_TURRET_CAP
            if CB_SMALL_MAP_CAP_ON and self.mw * self.mh < CB_SMALL_MAP_TILES:
                cap = CB_HOME_TURRET_CAP_SMALL
            if len(guns) >= cap:
                return False
            # A turret that already bears on this target makes a second one
            # waste; one that does not is the case LOKI could not tell apart.
            if self._home_gun_bears(ct, threat, guns):
                return False
        if ct.read_store(SLOT_HARVESTERS) < ECO_NEED and (
                bool(guns) if CB_BEARING_GATE_ON else self._live_home_gun(ct)):
            # ...unless the Core is provably bleeding.  Real damage is not
            # opening noise, and holding the counterbattery shut through a
            # genuine shelling finished a measured game with zero turrets.
            if not self._core_shelled(ct):
                return False
        p = ct.get_position()
        px, py = p.x, p.y
        ban = self._seat_ban()
        # A mobile target gets a Gunner or nothing: a Gunner re-aims for 10 Ti,
        # a Sentinel never re-aims at all, and 21 of the 25 home turrets built
        # in the ladder losses were Sentinels -- 11 of them born with nothing
        # on their line.  Static besiegers keep Sentinel-first: it is the only
        # home weapon whose reach (5 tiles) covers the seats a creeper uses.
        if CB_MOBILE_GUNNER_ON and threat_type in CB_MOBILE_TYPES:
            choices = ((EntityType.GUNNER, ct.get_gunner_cost()),)
        else:
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
                    # WAVE 22 ARM A2.  GUNNERS ONLY -- the sentinel branch is
                    # untouched, and so is the sentinel hold-fire path
                    # (PLAN.md sec 2.2 excludes TRIGGER-AUDIT outright).
                    if (turret_type == EntityType.GUNNER
                            and not self._gd_gun_ok(ct, bp, facing)):
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
        #
        # PLANK SOCKET-GUARD arm 4 OVERRIDES THE DEFERRAL, and only under one
        # condition: the detector's S3 signal, an enemy builder seen within
        # d<=8 of our own Core inside the last SG_S3_FRESH rounds.  That is the
        # exact precondition of the socket blockade -- every one of the 107
        # choke builds in our 15 losses was placed by an enemy builder standing
        # inside r^2<=26 of our Core centre -- and it is also the only state in
        # which a launcher at our own ring has anything to pick up.  Outside
        # it, LAUNCHER_MIN_RND (160) still holds and this file behaves as leap6.
        rnd = ct.get_current_round()
        sg = bool(SG_ON and SG_CORNER_LAUNCHER and rnd >= SG_LAUNCH_MIN_RND
                  and self.core is not None and self._sg_s3_fresh(ct, rnd))
        if not sg and rnd < LAUNCHER_MIN_RND:
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
        # Under S3 this IS the defence, not a luxury bought out of surplus, so
        # the 80 Ti deferral reserve drops to a token floor.  Outside S3 the
        # reserve is leap6's, unchanged.
        resv = SG_LAUNCH_TI_FLOOR if sg else LAUNCHER_RESERVE
        if not self._eco_spendable(ct, ct.get_launcher_cost() + resv):
            return False
        ct.write_store(SLOT_LAUNCHER, 1)  # claim before build so peers skip
        p = ct.get_position()
        px, py = p.x, p.y
        # Launchers are bot-impassable: never seat one on the eight
        # Core-orthogonal heal seats, delivery termini included.
        lban = self._home_seat_keys_set()
        # PLANK SOCKET-GUARD arm 4 -- THE SITE.  Pickup is r^2 <= 2 (re-verified
        # on 4907 field throws: 99.8% of launcher->pickup d^2 is <= 5, and the
        # extra is the victim's own move earlier in the round), so a launcher
        # can only lift a body on one of its EIGHT NEIGHBOURS.  A Core-ring
        # DIAGONAL CORNER is therefore the only site that covers delivery
        # sockets: each corner is orthogonally adjacent to the two sockets
        # flanking it and diagonally to the ring tiles beyond, and a corner is
        # not itself a socket, so it costs no delivery tile and no heal seat.
        # leap5 sited this at a median 8.3 tiles from our own Core -- outside
        # the pickup disc of anything that mattered -- and threw 8 times in 155
        # ladder sides.  Same mechanism, same code below; only the tile changed.
        if sg:
            for c in core_corners(self.core, self.mw, self.mh):
                if abs(c.x - px) + abs(c.y - py) != 1:
                    continue
                if (c.x, c.y) in lban:
                    continue        # cannot happen: a corner is not a seat
                try:
                    if not ct.can_build_launcher(c):
                        continue
                    ct.build_launcher(c)
                except Exception:
                    continue
                if SG_LOG:
                    print("SG launch (%d,%d) r=%d" % (c.x, c.y, rnd))
                return True
            # No free corner beside this body.  Do NOT fall through to the
            # generic adjacent-tile scan: a launcher one tile off the ring is
            # the leap5 defect, and `_sg_launch_walk` is already steering this
            # body onto a corner-adjacent tile.  Release the claim and wait.
            ct.write_store(SLOT_LAUNCHER, 0)
            return False
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
            # PLANK SOCKET-GUARD arm 4 before arm 5, and both before leap6's
            # home gunner (which is OFF here anyway): the corner launcher is
            # 20 Ti ONCE, zero ammunition, and may evict every round; the ring
            # gunner is 30 Ti plus a per-shot ammunition draw on the exact
            # budget the blockade is starving.  `_try_build_launcher` carries
            # the S3 gate itself and returns False outside it.
            if self._try_build_launcher(ct):
                return
            if SG_ON and SG_RING_TURRET and self._sg_ring_gun(ct):
                return
            if self._t5_home_gunner(ct):
                return
            if under and self._heal_core(ct):
                return
        # PLANK SOCKET-GUARD arm 4, the move half.  Deliberately ABOVE the
        # `under` gate: S3 is "an enemy builder within d<=8 of our Core", which
        # is a wider band than the d<=4 that latches SLOT_UNDER, and the whole
        # point of the plank is to be standing on the corner BEFORE the
        # blockade starts rather than after.
        if (SG_ON and SG_CORNER_LAUNCHER and ct.get_move_cooldown() == 0
                and self._sg_launch_walk(ct)):
            return
        if under and ct.get_move_cooldown() == 0:
            shelled = self._core_shelled(ct)
            # MERGE (turbo5).  turbo4's SEAT FIRST and turbo3's BEARING HUNT
            # both claim the defender's move in the same state, and they
            # disagree: seat = +4 HP/round for 1 Ti forever, hunt = walk to a
            # tile from which a counterbattery can be SITED on the besieger,
            # which is the only thing that stops the damage.  turbo4 is the
            # deployed ladder build, so it keeps the tie by default and the
            # order is a flag, not a decision baked into the file.
            if T5_HUNT_BEFORE_SEAT_ON and self._t5_bearing_hunt(ct):
                return
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
            if not T5_HUNT_BEFORE_SEAT_ON and self._t5_bearing_hunt(ct):
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

    def _sg_launcher_wanted(self, ct, rnd):
        """PLANK SOCKET-GUARD arm 4: should this body be siting a corner
        launcher right now?  Cheap enough to ask from the move phase."""
        if not (SG_ON and SG_CORNER_LAUNCHER) or self.core is None:
            return False
        if rnd < SG_LAUNCH_MIN_RND:
            return False
        if ct.read_store(SLOT_LAUNCHER):
            return False
        if ct.read_store(SLOT_HARVESTERS) < 1:
            return False
        return self._sg_s3_fresh(ct, rnd)

    def _sg_launch_walk(self, ct):
        """Step onto a tile from which a ring CORNER can be built.  True = the
        move was spent.

        The one thing leap5's seat-pluck never did.  A launcher is built on an
        ORTHOGONALLY adjacent tile, and every one of our eight sockets is
        orthogonally adjacent to exactly one corner -- so the walk target is
        simply "a passable tile beside a free corner", and the defender is
        usually one step from one already.  No new navigation: `self.tgt` plus
        the incumbent `_nav`.
        """
        rnd = ct.get_current_round()
        if not self._sg_launcher_wanted(ct, rnd):
            self.sg_launch_walk = None
            return False
        if not self._eco_spendable(ct, ct.get_launcher_cost() + SG_LAUNCH_TI_FLOOR):
            return False
        p = ct.get_position()
        best, bkey = None, None
        for c in core_corners(self.core, self.mw, self.mh):
            try:
                if ct.is_in_vision(c) and ct.get_tile_building_id(c) is not None:
                    continue                  # corner already taken
            except Exception:
                continue
            if abs(c.x - p.x) + abs(c.y - p.y) == 1:
                return False                  # already in place: build, do not walk
            for dx, dy in CARD_DELTAS:
                tx, ty = c.x + dx, c.y + dy
                if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                    continue
                t = Position(tx, ty)
                try:
                    if not ct.is_tile_passable(t):
                        continue
                except Exception:
                    continue
                key = (abs(tx - p.x) + abs(ty - p.y), ty, tx)
                if bkey is None or key < bkey:
                    best, bkey = t, key
        if best is None:
            return False
        self.sg_launch_walk = (best.x, best.y)
        self.tgt = best
        self._nav(ct, pave=False)
        return True

    def _sg_ring_gun(self, ct):
        """PLANK SOCKET-GUARD arm 5.  ONE gunner NEAR the ring, under S3.

        Turrets are the only thing in the game that can damage a builder bot
        (engine_mechanics E), so without one we cannot contest an intruder at
        all -- a builder of ours literally cannot fire on a builder of theirs.
        gsxWins' first gunner is turn 9; ours is turn 68.

        NEAR the ring, never ON it (SG_GUN_OFF_RING).  A turret is an
        impassable building and the twelve ring tiles are our eight delivery
        sockets / heal seats plus the four corners the launcher and the spawner
        need; a gunner's ray is three tiles cardinal, so one tile outside the
        ring still covers it.  The aim is VERIFIED with the hypothetical-turret
        call, exactly as `_t5_home_gunner` does: the facing is accepted only if
        its ray actually covers a tile on or just outside our own ring.

        This arm is separately flagged because home defence has measured
        NEGATIVE in this tree before (T5_HOME_GUNNER_ON is False right here).
        That refutation predates the socket-attack meta; the flag exists so a
        measurement can kill this one arm without touching the other four.
        """
        if not (SG_ON and SG_RING_TURRET) or self.core is None:
            return False
        if self.sg_gun_done:
            return False
        rnd = ct.get_current_round()
        if rnd < SG_GUN_MIN_RND or not self._sg_s3_fresh(ct, rnd):
            return False
        if ct.get_global_resources() < ct.get_gunner_cost() + SG_GUN_TI_FLOOR:
            return False
        # NOT BEFORE THE LINE THAT PAYS FOR IT.  MEASURED, glacierkeep (9
        # conveyors to the nearest ore): this arm bought a gunner at turn 17
        # -- 30 Ti and +10 % on every conveyor still to be laid -- while the
        # trunk was 15 links from the ring, and the bank was at 2 Ti by turn
        # 31 with nothing delivered.  A turret defends an economy; it does not
        # substitute for one.  The defender stands at home, so it can run the
        # socket census with its own eyes rather than trust a store field.
        if self.core is not None and not self._sg_socket_scan(ct)[0]:
            return False
        for _bp, et, _f in self._home_guns(ct):
            if et == EntityType.GUNNER:
                self.sg_gun_done = True       # someone already built it
                return False
        if self._cpu_exhausted(ct):
            return False
        p = ct.get_position()
        ring12 = self._home_seat_keys_set()
        corners = frozenset(
            (c.x, c.y) for c in core_corners(self.core, self.mw, self.mh))
        best, best_key, best_dir = None, None, None
        for dx, dy in CARD_DELTAS:
            bx, by = p.x + dx, p.y + dy
            if not (0 <= bx < self.mw and 0 <= by < self.mh):
                continue
            if SG_GUN_OFF_RING and ((bx, by) in ring12 or (bx, by) in corners):
                continue
            bp = Position(bx, by)
            dc_site = dsq_core(bp, self.core)
            if dc_site > SG_GUN_SITE_DSQ:
                continue
            for di, d in enumerate(DIRECTIONS):
                cover = None
                try:
                    for t in ct.get_attackable_tiles_from(bp, d, EntityType.GUNNER):
                        dc = dsq_core(t, self.core)
                        if dc < SG_GUN_NEAR_DSQ or dc > SG_GUN_FAR_DSQ:
                            continue
                        if cover is None or dc < cover:
                            cover = dc
                except Exception:
                    continue
                if cover is None:
                    continue
                # Nearest ring coverage first, then the nearer post.
                key = (cover, dc_site, bx, by, di)
                if best_key is not None and key >= best_key:
                    continue
                if not self._gd_gun_ok(ct, bp, d):    # WAVE 22 ARM A2
                    continue
                try:
                    if not ct.can_build_gunner(bp, d):
                        continue
                except Exception:
                    continue
                best, best_key, best_dir = bp, key, d
        if best is None:
            return False
        ct.build_gunner(best, best_dir)
        ct.write_store(SLOT_HOME_GUN, ct.read_store(SLOT_HOME_GUN) + 1)
        self.sg_gun_done = True
        if SG_LOG:
            print("SG gun (%d,%d) r=%d" % (best.x, best.y, rnd))
        return True

    def _t5_home_gunner(self, ct):
        """One HOME gunner by ~r20, aimed at the approach.  (change 3b)

        Opponents get a turret onto our doorstep at median r26 -- twenty rounds
        earlier than they manage it against the top-5 -- and in 48 % of our
        games we neither kill it nor answer it; our first home turret lands at
        r54 against ph's r2 and the mid-tier's r25 (resource_gap.md G7).  This
        buys the answer BEFORE the intruder rather than after it.

        The aim is verified, not assumed: `get_attackable_tiles_from` is the
        hypothetical-turret pattern, so the facing is accepted only if its
        three-tile ray actually covers a tile 2-4 tiles out from our own
        footprint ON THE ENEMY SIDE -- the straight approach from their Core,
        which is the line every creeper in the corpus walks.
        """
        if not T5_HOME_GUNNER_ON or self.core is None or self.enemy is None:
            return False
        if self.t5_home_gun_done:
            return False
        if ct.get_current_round() < T5_HOME_GUN_RND:
            return False
        cost = ct.get_gunner_cost()
        if ct.get_global_resources() < cost + T5_HOME_GUN_TI_FLOOR:
            return False
        for _bp, et, _f in self._home_guns(ct):
            if et == EntityType.GUNNER:
                # Someone already built it.  Latch off for this unit's life.
                self.t5_home_gun_done = True
                return False
        if self._cpu_exhausted(ct):
            return False
        p = ct.get_position()
        ban = self._seat_ban()
        home_far = self.core.distance_squared(self.enemy)
        best, best_key, best_dir = None, None, None
        for dx, dy in CARD_DELTAS:
            bx, by = p.x + dx, p.y + dy
            if not (0 <= bx < self.mw and 0 <= by < self.mh):
                continue
            if ban is not None and (bx, by) in ban:
                continue
            bp = Position(bx, by)
            if dsq_core(bp, self.core) > T5_HOME_GUN_SITE_DSQ:
                continue
            for di, d in enumerate(DIRECTIONS):
                cover = None
                try:
                    for t in ct.get_attackable_tiles_from(bp, d, EntityType.GUNNER):
                        dc = dsq_core(t, self.core)
                        if dc < T5_HOME_GUN_NEAR_DSQ or dc > T5_HOME_GUN_FAR_DSQ:
                            continue
                        if t.distance_squared(self.enemy) >= home_far:
                            continue    # behind us: not the approach
                        if cover is None or dc < cover:
                            cover = dc
                except Exception:
                    continue
                if cover is None:
                    continue
                key = (-cover, bx, by, di)
                if best_key is not None and key >= best_key:
                    continue
                if not self._gd_gun_ok(ct, bp, d):    # WAVE 22 ARM A2
                    continue
                try:
                    if not ct.can_build_gunner(bp, d):
                        continue
                except Exception:
                    continue
                best, best_key, best_dir = bp, key, d
        if best is None:
            return False
        ct.build_gunner(best, best_dir)
        ct.write_store(SLOT_HOME_GUN, ct.read_store(SLOT_HOME_GUN) + 1)
        self.t5_home_gun_done = True
        return True

    def _t5_zero_idle(self, ct):
        """The turn ended with neither an action nor a move.  (change 4a)

        31.6 % of our builder-turns do nothing against the top-5's 12.3 % and
        sporks' 1.8 % -- 11,548 of 36,546 turns over 30 games, which at 1 Ti a
        heal is 46,000 HP of healing never delivered (resource_gap.md G6).
        Cooldowns are set the instant an action or a move is taken, so "both
        still zero at the end of my turn" is an exact test for a wasted turn.

        Nothing new is invented here: heal an adjacent damaged friendly, re-lay
        a trunk hole beside us (`_l4_repair`, the narrow both-sides-chained
        rule that provably cannot spam), or step toward the objective we
        already hold.  A body standing on one of our own heal seats while the
        Core is under attack is left alone -- that stillness is the plan.
        """
        try:
            if ct.get_action_cooldown() != 0 or ct.get_move_cooldown() != 0:
                return
        except Exception:
            return
        if self._cpu_exhausted(ct):
            return
        p = ct.get_position()
        if T5_IDLE_HEAL_ON and ct.get_global_resources() >= T5_IDLE_HEAL_TI_FLOOR:
            for dx, dy in CARD_DELTAS:
                tx, ty = p.x + dx, p.y + dy
                if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                    continue
                t = Position(tx, ty)
                try:
                    hurt = None
                    bid = ct.get_tile_building_id(t)
                    if bid is not None and ct.get_team(bid) == self.team:
                        hurt = bid
                    else:
                        oid = ct.get_tile_builder_bot_id(t)
                        if oid is not None and ct.get_team(oid) == self.team:
                            hurt = oid
                    if hurt is None:
                        continue
                    if ct.get_hp(hurt) > ct.get_max_hp(hurt) - T5_IDLE_HEAL_GAP:
                        continue
                    if not ct.can_heal(t):
                        continue
                except Exception:
                    continue
                ct.heal(t)
                return
        if T5_IDLE_REPAIR_ON and self._l4_repair(ct):
            return
        if not T5_IDLE_STEP_ON:
            return
        if self.t5_nav_rnd == ct.get_current_round():
            return      # already tried to walk this turn and was blocked
        if self.tgt is None or (self.tgt.x == p.x and self.tgt.y == p.y):
            return
        if self.core is not None and ct.read_store(SLOT_UNDER) != 0:
            if (p.x, p.y) in self._home_seat_keys_set():
                return
        self._nav(ct, pave=False)

    def _t5_bearing_hunt(self, ct):
        """LOKI-BEARING HUNT, lifted out of `_defend` so the merge can order it.

        The only build sites this unit has are the four tiles it is standing
        next to, so a besieger it never walks toward is a besieger no
        counterbattery can ever be sited against -- 985 of the 2,529 besieged
        rounds in the ladder losses had no home turret at all.  Narrow on
        purpose: only a STATIC besieger (an enemy turret or launcher), only
        while nothing bears on it, and it stops at CB_HUNT_MOVE_DSQ so the walk
        cannot pull the defender off the Core and out of heal range forever.
        Returns True iff it spent the move.
        """
        if not CB_HUNT_MOVE_ON:
            return False
        target, ttype = self._cb_target(ct)
        if (target is not None and ttype not in CB_MOBILE_TYPES
                and ct.get_position().distance_squared(target) > CB_HUNT_MOVE_DSQ
                and not self._home_gun_bears(ct, target)):
            self.tgt = target
            self._nav(ct, pave=False)
            return True
        return False

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

    def _hold_core_fire(self, ct, rnd, cg_hold):
        """THE SHARED OPEN-FIRE MOMENT: PLANK CAGE arm 3 OR PLANK PAIRS arm 2.

        Both gates answer one question -- may this turret damage their Core yet
        -- so they are OR'd and fire opens only when BOTH are satisfied.  The
        CAGE half is a TEAM fact (the ring census, slot 15 bit 31); the PAIRS
        half is a PER-BODY fact (this tube's own clock against the published
        tube census).  Kept as two gates rather than one bit for exactly that
        reason: folding a per-body latch into a shared word is the race that
        cost this tree two rebuilds (FIX B, and the CAGE store note).

        CAGE is asked first because its answer is already memoised for the turn
        and, while it holds, the PR clock has no business starting -- a tube
        that may not shoot for cage reasons has not yet "become able to shoot",
        which is what arm 4's 30-round release counts.
        """
        if cg_hold:
            self._cg_hold_log(ct, rnd)
            return True
        if PAIR_ON and self._pr_hold(ct, rnd):
            self._pr_hold_log(rnd)
            return True
        return False

    def _turret(self, ct):
        if self.team is None:
            self.team = ct.get_team()
            self.mw, self.mh = ct.get_map_width(), ct.get_map_height()
        p = ct.get_position()
        turret_type = ct.get_entity_type()
        # PLANK CAGE arm 3.  The ordering plank's whole cost is paid here: a
        # turret that can see their Core does NOT shoot it until the cage is
        # built.  Three store reads, memoised on the round, and every other
        # target this turret has stays legal -- the tube keeps shooting their
        # belts, their turrets and their bodies on seats while it waits.
        # PLANK PAIRS arm 2 rides the same three sites.  `hold_maybe` is the
        # cheap outer guard -- once this body has opened, and for every turret
        # that never had their Core in a line at all, the whole question costs
        # one boolean and no store read.  The PR clock must NOT start here: it
        # is denominated in "rounds since this tube could shoot their Core", so
        # `_pr_hold` is asked lazily, at the three sites where a Core actually
        # appears, and a home gunner therefore never starts one.
        cg_rnd = ct.get_current_round()
        cg_hold = CAGE_ON and self._cg_hold(ct, cg_rnd)
        hold_maybe = cg_hold or (PAIR_ON and not self.pr_open)

        if turret_type == EntityType.GUNNER:
            try:
                tgt = ct.get_gunner_target()
                if tgt is not None and ct.can_fire(tgt):
                    bid = ct.get_tile_building_id(tgt)
                    bot = ct.get_tile_builder_bot_id(tgt)
                    et = None
                    if bid is not None and ct.get_team(bid) != self.team:
                        et = ct.get_entity_type(bid)
                    elif bot is not None and ct.get_team(bot) != self.team:
                        et = EntityType.BUILDER_BOT
                    if (et == EntityType.CORE and hold_maybe
                            and self._hold_core_fire(ct, cg_rnd, cg_hold)):
                        et = None
                    if et is not None and self._t5_barrier_ok(ct, tgt, et):
                        # BEFORE the shot: after it the entity is gone and its
                        # HP is unreadable, so a kill can only be recorded from
                        # the near side of the trigger.
                        self._tw_note_gun_shot(ct, tgt, et)
                        self._rg_note_kill(ct, tgt, et)
                        ct.fire(tgt)
                        self._gd_note_shot()
                        self._t5_note_shot(ct, tgt, et)
                        return
            except Exception:
                pass

        # Sentinels pierce intervening units, so scan the whole line.  Never
        # take the FIRST occupied tile out of get_attackable_tiles(): that
        # enumeration is row-major in absolute coordinates, so a "first hit
        # wins" scan engages the farthest enemy at four facings and the nearest
        # at the other four.  Priority is geometric/typed instead.
        try:
            cand = []
            core_in_line = False
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
                if et == EntityType.CORE:
                    # `core_in_line` is set EITHER WAY.  It is not a firing
                    # decision, it is the term `_t5_rank` uses to tell a
                    # forward tube from a home one when it prices their belts,
                    # and a held shot does not move this turret.
                    core_in_line = True
                    if hold_maybe and self._hold_core_fire(ct, cg_rnd, cg_hold):
                        continue
                cand.append((t, et))
            best, best_key, best_et = None, None, None
            if not T5_RETARGET_ON:
                # LOKI's exact semantics, kept bit-for-bit so the flag is a
                # true control: strictly-lower priority wins, and among equals
                # the FIRST in get_attackable_tiles()' row-major order does.
                best_prio = 99
                for t, et in cand:
                    prio = TURRET_PRIO.get(et, 8)
                    if prio < best_prio:
                        best_prio, best, best_et = prio, t, et
            else:
                for t, et in cand:
                    r = self._t5_rank(ct, t, et, core_in_line)
                    if r is None:
                        continue
                    key = (r, p.distance_squared(t), t.x, t.y)
                    if best_key is None or key < best_key:
                        best, best_key, best_et = t, key, et
            if best is None and T5_RETARGET_ON:
                # THE BARRIER, LAST.  _t5_rank refuses one outright; it comes
                # back only when the line holds nothing else at all and the
                # magazine can spare it.
                for t, et in cand:
                    if et != EntityType.BARRIER or not self._t5_barrier_ok(ct, t, et):
                        continue
                    key = (p.distance_squared(t), t.x, t.y)
                    if best_key is None or key < best_key:
                        best, best_key, best_et = t, key, et
            if best is not None:
                if turret_type == EntityType.GUNNER:
                    self._rg_note_kill(ct, best, best_et)
                ct.fire(best)
                if turret_type == EntityType.GUNNER:
                    self._gd_note_shot()
                self._t5_note_shot(ct, best, best_et)
                return
        except Exception:
            pass
        try:
            for eid in ct.get_nearby_entities():
                if ct.get_team(eid) != self.team:
                    # PLANK CAGE arm 3.  The last-resort sweep would otherwise
                    # walk straight past the two ranked paths above and land
                    # the first shot of the game on their Core.
                    if (hold_maybe
                            and ct.get_entity_type(eid) == EntityType.CORE
                            and self._hold_core_fire(ct, cg_rnd, cg_hold)):
                        continue
                    # LOKI called get_position twice per accepted entity.
                    ep = ct.get_position(eid)
                    if ct.can_fire(ep):
                        ct.fire(ep)
                        if turret_type == EntityType.GUNNER:
                            self._gd_note_shot()
                        return
        except Exception:
            pass
        # WAVE 19, FIX 2 (ii).  THE CHASE COMES FIRST AND IT IS EXCLUSIVE for
        # the reactive ring gun WHILE ITS BUDGET LASTS: if `_rg_chase` owns
        # this barrel it owns the spend too, and letting `_idle_rotate` also
        # pay 10 Ti on the same turret would make RG_ROT_BUDGET a number about
        # nothing.  It runs only after every firing path above has declined --
        # a gun with a shot takes the shot -- and it declines instantly (one
        # flag, one cached bool) for every turret that is not this one.
        #
        # THE BUDGET TEST IS ON THE OUTSIDE, and the first smoke is why.  With
        # the branch taken unconditionally, a gun that had spent its four
        # rotations never re-aimed AGAIN -- for the remaining four hundred
        # rounds the barrel was welded -- and the measured time-on-target came
        # in BELOW the control's, which still had the incumbent discipline
        # running all game (results/wave19/smoke.txt: tgt_rounds median 2 vs
        # 6).  Exhausting the chase must hand the turret BACK, not retire it.
        # LEAP16 CONSOLIDATION, REMOVAL 1.  THE CALL SITE IS GONE.  Wave 18b
        # adjudicated FIX 2's re-aim as NOISE (the chase fired 13 times in 12
        # legs against a budget of 4 rotations, and with the denominator held
        # fixed the time-on-target RATE came in BELOW the control on 11 of 12
        # cells, p=.070) -- so what it bought was a per-turret, per-round guard
        # plus an 8-facing `can_fire_from` enumeration on every gunner turn,
        # for a delta that measured the wrong way.  `_rg_chase` is left in the
        # file (its own `RG_CHASE_ON` head still returns False) so the deletion
        # cannot break a caller we did not find; nothing calls it.  The SITING
        # half of FIX 2 -- `_rg_cover`, RG_COVER_UNION_ON -- is KEPT: it is one
        # scoring term inside a scan that already runs, it is where the aim
        # delta actually came from, and it costs nothing per round.
        # WAVE 22 ARM A2.  BOTH ARMS RUN ONLY HERE, after every firing path
        # above has declined -- a gun with a shot takes the shot, always.
        #
        # SCRAP BEFORE RE-AIM, and the order is the argument: the scrap test
        # requires an EMPTY horizon, so when it fires there is by definition
        # nothing on the board worth turning towards, and paying 10 Ti to
        # re-aim a gun we are about to remove for free is the churn this arm
        # exists to stop.  `_gd_scrap` ends the unit's turn when it takes.
        if GD_ON and self._gd_scrap(ct, p, turret_type, cg_rnd):
            return
        # CLEAR LANE owns the barrel when it moves it: `_idle_rotate` would
        # otherwise pay a second 10 Ti in the same round on the same turret.
        if GD_ON and self._gd_reaim(ct, p, turret_type, cg_rnd):
            return
        if ROTATE_DISCIPLINE_ON:
            self._idle_rotate(ct, p, turret_type)

    # --- LOKI-TURBO5 plank R: what the guns are actually pointed at ---------

    def _t5_enemy_seats(self, ct):
        """THEIR eight heal seats, as (x, y).  Cached on their anchor."""
        E = self.enemy
        if E is None:
            return frozenset()
        key = (E.x, E.y)
        if self.t5_seat_key != key:
            self.t5_seat_key = key
            self.t5_seat_xy = frozenset(
                (s.x, s.y) for s in heal_seats(E, self.mw, self.mh))
        return self.t5_seat_xy

    def _t5_rank(self, ct, t, et, core_in_line):
        """resource_gap.md change 2, as a rank.  None means "do not fire here".

        (i) an enemy TURRET in line -- it is the only thing on the board that
        can damage a builder bot, and counter-battery is the cheapest exchange
        we have; (ii) an enemy LAUNCHER; (iii) an enemy CONVEYOR 8-15 tiles
        back from their Core along a trunk -- the link, not the harvester,
        because the tail strands either way and the link is the cheaper kill --
        or ANY enemy belt or harvester in line when their Core is not in line
        at all, which is every shot a home turret will ever take; (iv) an enemy
        BUILDER standing on one of their eight heal seats, which is where the
        43x heal spread in raid.py's header comes from; (v) the Core; (vi)
        anything else.  Barriers are handled separately in _t5_barrier_ok.

        We fire 82 % of our ammunition into the enemy Core and 5 % at their
        economy; ph and Pivot are 30/54 and 34/49 and win.  O(1), the only
        top-5 team with our profile (93 %/0 %), is the weakest of the five.
        """
        other = T5_RANK_INDEX["other"]
        if et in CORE_THREAT_TYPES:
            return T5_RANK_INDEX["turret"]
        if et == EntityType.LAUNCHER:
            return T5_RANK_INDEX["launcher"]
        if et in T5_ECON_TYPES:
            E = self.enemy
            if E is None:
                return other
            if not core_in_line:
                # A home turret never has their Core in its line, so every
                # belt it can see is a trunk as far as it is concerned.
                return T5_RANK_INDEX["econ"]
            if et == EntityType.HARVESTER:
                return other
            c = nearest_core_tile(t, E)
            md = abs(t.x - c.x) + abs(t.y - c.y)
            if T5_TRUNK_MIN_D <= md <= T5_TRUNK_MAX_D:
                return T5_RANK_INDEX["econ"]
            return other
        if et == EntityType.BUILDER_BOT:
            if (t.x, t.y) in self._t5_enemy_seats(ct):
                return T5_RANK_INDEX["seat"]
            return other
        if et == EntityType.CORE:
            return T5_RANK_INDEX["core"]
        if et == EntityType.BARRIER:
            return None
        return other

    def _t5_barrier_ok(self, ct, t, et):
        """A barrier is only ever worth a shot as a last resort.

        3 Ti and 30 HP: two Sentinel shots and 20 ammo to remove 3 Ti of the
        opponent's cost scale.  Allowed only with the magazine full and never
        twice on the same tile inside T5_BARRIER_REPEAT_RNDS, so a turret
        cannot spend a whole match grinding one wall.
        """
        if not T5_RETARGET_ON or et != EntityType.BARRIER:
            return True
        if ct.get_global_ammo() <= T5_BARRIER_AMMO_MIN:
            return False
        rnd = ct.get_current_round()
        last = self.t5_bar_ban.get((t.x, t.y))
        return last is None or rnd - last >= T5_BARRIER_REPEAT_RNDS

    def _t5_note_shot(self, ct, t, et):
        if et == EntityType.BARRIER and T5_RETARGET_ON:
            if len(self.t5_bar_ban) > 32:
                self.t5_bar_ban.clear()
            self.t5_bar_ban[(t.x, t.y)] = ct.get_current_round()

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

        # LOKI-BEARING.  Rank before distance: a creeper turret parked three
        # tiles out is what kills the Core, and LOKI's pure-nearest choice let
        # any passing builder hold the barrel off it.  Static targets also stay
        # put long enough for the 10 Ti rotate to pay for itself.
        #
        # PLANK RG INVERTS THAT RANKING, AND ONLY FOR ITS OWN GUN.  LOKI-BEARING
        # is right for a forward tube and wrong for the reactive ring gunner:
        # the whole reason this gun was bought is the BUILDER laying bricks on
        # our sockets, which is the one class of enemy our own builders
        # physically cannot touch, while a besieging turret already has two
        # answers in this tree (SAP and the counter-battery).  The inversion is
        # gated on `_rg_is_mine` -- a GUNNER of ours standing within
        # RG_SITE_DSQ of our own Core -- so no other turret's aim moves.  The
        # builder-out-of-range filter below is UNCHANGED and still applies: a
        # body past GUNNER_RANGE_DSQ will have walked before the rotation
        # cooldown clears, and that is the measured thrash.
        rg_aim = (RG_ON and RG_ROT_ON and turret_type == EntityType.GUNNER
                  and ct.get_current_round() < RG_ROT_UNTIL
                  and self._rg_is_mine(ct, p))
        cand, cand_key, cand_d = None, None, 10 ** 9
        for eid in ct.get_nearby_entities():
            try:
                if ct.get_team(eid) == self.team:
                    continue
                et = ct.get_entity_type(eid)
                ep = ct.get_position(eid)
                d = p.distance_squared(ep)
                # A builder past gunner range will have moved before the
                # rotation cooldown clears -- that is the measured thrash.
                if et == EntityType.BUILDER_BOT and d > GUNNER_RANGE_DSQ:
                    continue
            except Exception:
                continue
            if rg_aim:
                key = (0 if et == EntityType.BUILDER_BOT else 1, d)
            else:
                key = (0 if et in CORE_THREAT_TYPES else 1, d)
            if cand_key is not None and key >= cand_key:
                continue
            cand, cand_key, cand_d = ep, key, d

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
            # PLANK RG, THE FRATRICIDE RE-CHECK.  The build-time facing was
            # verified clean; a rotation is a NEW facing and gets the same
            # test, because the ray hits the nearest occupant and a conveyor
            # laid since the gun went up is exactly the occupant we would be
            # shooting.  Only this gun pays for the check.
            if rg_aim and not self._rg_ray_safe(ct, p, want):
                return
            try:
                if want != cur and ct.can_rotate(want):
                    if not self._rotate_allowed(ct, p, want, tgt):
                        return
                    self.rot_rnd = ct.get_current_round()
                    self.rot_prev_dir = cur
                    self.rot_lock_d = p.distance_squared(tgt)
                    ct.rotate(want)
                    if rg_aim and RG_LOG:
                        print("RG rot %s->%s r=%d" % (
                            getattr(cur, "name", cur),
                            getattr(want, "name", want),
                            ct.get_current_round()))
            except Exception:
                return
            return

        self.rot_tgt = None
        if ct.get_current_round() - self.rot_rnd < ROTATE_COOLDOWN_RNDS:
            return
        # PLANK RG.  With nothing hostile in sight the incumbent code swings
        # the barrel at the ENEMY CORE anchor.  For a gun standing two tiles
        # from OUR Core that is a line straight across our own ring, and rule
        # 9 says it will happily shoot whatever of ours is on it.  The
        # reactive ring gunner holds its last verified facing instead.
        if rg_aim:
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
