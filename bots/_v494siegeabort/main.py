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
    EcoMixin, dsq_core, enemy_core_for, heal_seats, known_map_for,
    nearest_cardinal, pack_pos, ring, unpack_pos,
)
from raid import RaidMixin

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


class Player(EcoMixin, RaidMixin):

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

        # --- SIEGEBREAK (per unit).  Titanium this body has spent on turret
        # pecks, capped at SIEGEBREAK_MAX_TI.  No store slot: only this unit
        # writes it and only this unit reads it. ---
        self.sb_spent = 0

        # --- SIEGEABORT (per unit).  `sa_seen[tid] = (hp_at_first_peck, pecks)`
        # and `sa_ban` = turret ids this body has given up on.  Per unit for the
        # same reason sb_spent is: no store slot to clobber, and the budget the
        # abort protects is this body's own. ---
        self.sa_seen = {}
        self.sa_ban = set()
        self.sa_aborts = 0

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

        # --- gunner rotation latch (PIECE I) ---
        self.rot_tgt = None
        self.rot_rnd = -10 ** 9
        self.rot_prev_dir = None
        self.rot_lock_d = 10 ** 9

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
        if harv >= ECO_NEED:
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
            ti_floor = 12 if (under or weapons_top) else 52
            if E1_AMMO_FLOOR_ON and not under:
                ti_floor = max(
                    ti_floor,
                    min(ct.get_harvester_cost(), E1_RESERVE_CAP) + E1_HARV_RESERVE_MARGIN,
                )
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

        # SEAT 3 joins the raid once the harvester shell exists.  This is the
        # only role transition in the file and it is state-gated, not clocked.
        if (
            self.role == "expand" and self.role_n == LOKI_LATE_RAID_SEAT
            and not self.link_queue and ct.read_store(SLOT_HARVESTERS) >= ECO_NEED
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
            # SIEGEBREAK, CALL SITE 1 OF 2.  This heal-first short-circuit is
            # the documented reason the ancestor's turret peck was unreachable
            # (doctrine.py "PIECE J", the #446 decode: a living builder held
            # dist^2 = 2 from a 4/40 HP Sentinel for 283 rounds and never hit
            # it).  A turret ALREADY orthogonally adjacent to this body is a
            # removal we are one action from; +4 HP/round is not.  `_sb_live`
            # confines this to the defender seat, so no other builder's heal
            # is touched.
            if self._sb_fire(ct):
                return
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
        if self.role == "raid":
            self._raid(ct)
        elif self.role == "defend":
            self._defend(ct)
        else:
            self._expand(ct)

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

    # ------------------------------------------------------------------
    # SIEGEBREAK -- see the block at the end of doctrine.py.  Restores the
    # `_duel_safe`-gated near-Core turret peck that `_v109loki5/main.py:1326`
    # shipped and that this tree lost, scoped to the role=="defend" seat.
    # DELIBERATELY NOT ROUTED THROUGH `_sabotage_prio`: that method ranks the
    # enemy CORE, harvesters, conveyors, splitters and barriers alongside guns
    # (SABOTAGE_PRIO, main.py:45), so unsilencing it would ship core-peck and
    # belt melee in the same change.  LOKI_QUIET_ON is untouched.
    # ------------------------------------------------------------------

    def _sb_live(self, ct):
        """Cheap precondition shared by the fire path and the seat path."""
        if not SIEGEBREAK_ON or self.core is None:
            return False
        if self.role != "defend":
            return False
        if self.sb_spent >= SIEGEBREAK_MAX_TI:
            return False
        if ct.read_store(SLOT_UNDER) == 0:
            return False
        return ct.get_global_resources() >= SIEGEBREAK_MIN_BANK + HUNT_FIRE_TI

    def _duel_safe(self, ct, tx, ty, tid, mx, my):
        """True if pecking the turret at (tx, ty) from (mx, my) is winnable.

        Ported from `bots/_v109loki5/main.py:1326` (integer arithmetic here to
        match this tree's hot-path style; the three gates and their answers are
        unchanged).  Safe iff any of: (a) HUNT_FINISH_HP or fewer HP left --
        finishing always pays; (b) a second friendly builder already stands
        orthogonally on it, so the grind is shared; (c) its facing ray does not
        cover OUR tile.  An unreadable facing reads as UNSAFE.
        """
        if not DUEL_DISCIPLINE_ON:
            return True
        try:
            et = ct.get_entity_type(tid)
        except Exception:
            return False
        if et not in CORE_THREAT_TYPES:
            return False
        try:
            if ct.get_hp(tid) <= HUNT_FINISH_HP:
                return True
        except Exception:
            pass
        me = ct.get_id()
        for dx, dy in CARD_DELTAS:
            nx, ny = tx + dx, ty + dy
            if not (0 <= nx < self.mw and 0 <= ny < self.mh):
                continue
            try:
                oid = ct.get_tile_builder_bot_id(Position(nx, ny))
                if oid is not None and oid != me and ct.get_team(oid) == self.team:
                    return True
            except Exception:
                continue
        try:
            fdx, fdy = DELTA[ct.get_direction(tid)]
        except Exception:
            return False
        if fdx == 0 and fdy == 0:
            return True
        # Walk the ray from the turret outward.  Gunner r^2 = 13, Sentinel 32.
        rng = 32 if et == EntityType.SENTINEL else 13
        x, y = tx, ty
        while True:
            x += fdx
            y += fdy
            if not (0 <= x < self.mw and 0 <= y < self.mh):
                return True
            if (x - tx) ** 2 + (y - ty) ** 2 > rng:
                return True
            if x == mx and y == my:
                return False
            if et == EntityType.SENTINEL:
                # The Sentinel line ignores obstacles, so nothing between us
                # can shield the peck -- keep walking to our own tile.
                continue
            try:
                n = Position(x, y)
                blocked = (ct.get_tile_building_id(n) is not None
                           or ct.get_tile_builder_bot_id(n) is not None)
            except Exception:
                # Out of vision: assume a body eats the shot, so the Gunner's
                # ray stops before it reaches us.
                blocked = True
            if blocked:
                return True

    # ------------------------------------------------------------------
    # SIEGEABORT -- see the block at the end of doctrine.py.  ONE test, wired
    # into the two places the parent already scans candidates, so an abort
    # RE-TARGETS instead of idling.
    # ------------------------------------------------------------------

    def _sa_refuse(self, ct, tid, hp):
        """True if this body should stop paying to peck turret `tid`.

        `hp` is the target's CURRENT HP as read BEFORE this round's peck, or
        None if it could not be read.  Net progress is measured against this
        body's own pecks only: after N pecks the HP owes 2N.
        """
        if not SIEGEABORT_ON:
            return False
        # FINISH ALWAYS PAYS -- checked FIRST, so it outranks the ban.  Same
        # clause `_duel_safe` uses; see the doctrine block for why it wins.
        if hp is not None and hp <= HUNT_FINISH_HP:
            return False
        if tid in self.sa_ban:
            return True
        st = self.sa_seen.get(tid)
        if st is None or hp is None:
            return False
        hp0, pecks = st
        if pecks < SIEGEABORT_MIN_PECKS:
            return False
        if (hp0 - hp) * 100 >= SIEGEABORT_MIN_DROP_FRAC * 2 * pecks:
            return False
        self.sa_ban.add(tid)
        self.sa_aborts += 1
        if SIEGEABORT_LOG:
            try:
                import sys as _s
                print(f"SIEGEABORT id={ct.get_id()} tgt={tid} pecks={pecks} "
                      f"hp0={hp0} hp={hp} drop={hp0 - hp} rnd="
                      f"{ct.get_current_round()}", file=_s.stderr)
            except Exception:
                pass
        return True

    def _sb_fire(self, ct):
        """Peck an orthogonally adjacent, in-band, duel-safe enemy turret."""
        if not self._sb_live(ct):
            return False
        p = ct.get_position()
        px, py = p.x, p.y
        best, best_hp, best_id = None, None, None
        for dx, dy in CARD_DELTAS:
            tx, ty = px + dx, py + dy
            if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                continue
            t = Position(tx, ty)
            try:
                bid = ct.get_tile_building_id(t)
                if bid is None or ct.get_team(bid) == self.team:
                    continue
                if ct.get_entity_type(bid) not in CORE_THREAT_TYPES:
                    continue
                if dsq_core(t, self.core) > SIEGEBREAK_BAND_DSQ:
                    continue
                if not ct.can_fire(t):
                    continue
                hp = ct.get_hp(bid)
            except Exception:
                continue
            if not self._duel_safe(ct, tx, ty, bid, px, py):
                continue
            # SIEGEABORT, FILTER 1 OF 2.  A FILTER and not a post-selection
            # veto: dropping the stalled target here lets the SAME loop pick a
            # second adjacent turret, which is the cheapest possible re-target.
            if self._sa_refuse(ct, bid, hp):
                continue
            if best_hp is None or hp < best_hp:
                best, best_hp, best_id = t, hp, bid
        if best is None:
            return False
        try:
            ct.fire(best)
        except Exception:
            return False
        self.sb_spent += HUNT_FIRE_TI
        if SIEGEABORT_ON and best_id is not None:
            # `best_hp` is the PRE-peck HP, so the first peck's reading is the
            # baseline the whole test is measured against and is never re-based.
            st = self.sa_seen.get(best_id)
            self.sa_seen[best_id] = ((best_hp, 1) if st is None
                                     else (st[0], st[1] + 1))
        return True

    def _sb_seat(self, ct):
        """The duel-safe seat beside the nearest in-band enemy turret, or None."""
        if not self._sb_live(ct):
            return None
        p = ct.get_position()
        px, py = p.x, p.y
        best, best_d = None, None
        for eid in ct.get_nearby_units():
            if self._cpu_exhausted(ct):
                return None
            try:
                if ct.get_team(eid) == self.team:
                    continue
                if ct.get_entity_type(eid) not in CORE_THREAT_TYPES:
                    continue
                ep = ct.get_position(eid)
            except Exception:
                continue
            if dsq_core(ep, self.core) > SIEGEBREAK_BAND_DSQ:
                continue
            # ⛔ ITS OWN try, NOT the one above: folding get_hp into that block
            # would make a raising HP read skip a candidate the PARENT accepts,
            # which is a behaviour change at SIEGEABORT_ON = False.
            try:
                ehp = ct.get_hp(eid)
            except Exception:
                ehp = None
            # SIEGEABORT, FILTER 2 OF 2.  Without this the body would keep
            # WALKING to the seat of a turret the fire path refuses to shoot --
            # the abort would free the action and strand the move.  Filtering
            # here makes the next in-band duel-safe turret the destination, and
            # when there is none `_sb_seat` returns None and the parent's own
            # seat/chase/heal block runs unchanged.
            if self._sa_refuse(ct, eid, ehp):
                continue
            ex, ey = ep.x, ep.y
            for dx, dy in CARD_DELTAS:
                sx, sy = ex + dx, ey + dy
                if not (0 <= sx < self.mw and 0 <= sy < self.mh):
                    continue
                if sx == px and sy == py:
                    continue           # already seated: the fire path owns it
                d = (sx - px) ** 2 + (sy - py) ** 2
                if d > SIEGEBREAK_REACH_DSQ or (best_d is not None and d >= best_d):
                    continue
                s = Position(sx, sy)
                try:
                    if not ct.is_tile_passable(s):
                        continue
                except Exception:
                    continue
                if not self._duel_safe(ct, ex, ey, eid, sx, sy):
                    continue
                best, best_d = s, d
        return best

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
            # SIEGEBREAK, CALL SITE 2 OF 2.  Above `_try_counterbattery`: a
            # turret we are already adjacent to costs 2 Ti to chip and a
            # counterbattery Sentinel costs 30+ and does not remove it.
            if self._sb_fire(ct):
                return
            if self._sabotage_prio(ct):
                return
            if under and self._try_counterbattery(ct):
                return
            if self._try_build_launcher(ct):
                return
            if under and self._heal_core(ct):
                return
        if under and ct.get_move_cooldown() == 0:
            # SIEGEBREAK MOVE.  Above the seat/chase block on purpose: with
            # SIEGEBREAK_ON the defender's move is spent WALKING TO a seat the
            # duel test has already cleared, which is the only way call site 1
            # or 2 ever gets an adjacent turret to shoot at.  When no such seat
            # exists -- every neighbour on a ray, unreachable, out of band, or
            # budget spent -- `_sb_seat` returns None and the rest of this
            # method runs byte-for-byte as the control does.
            sb = self._sb_seat(ct)
            if sb is not None:
                self.tgt = sb
                self._nav(ct, pave=False)
                return
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
                prio = TURRET_PRIO.get(et, 8)
                if prio < best_prio:
                    best_prio, best = prio, t
            if best is not None:
                ct.fire(best)
                return
        except Exception:
            pass
        try:
            for eid in ct.get_nearby_entities():
                if ct.get_team(eid) != self.team:
                    # LOKI called get_position twice per accepted entity.
                    ep = ct.get_position(eid)
                    if ct.can_fire(ep):
                        ct.fire(ep)
                        return
        except Exception:
            pass
        if ROTATE_DISCIPLINE_ON:
            self._idle_rotate(ct, p, turret_type)

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
