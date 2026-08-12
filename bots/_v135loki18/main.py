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
"""
import math

from fcode import Direction, EntityType, GameConstants, Position

from doctrine import *  # noqa: F401,F403
from eco import (
    EcoMixin, core_tiles, enemy_core_for, heal_seats, known_map_for,
    nearest_cardinal, pack_pos, ring, unpack_pos,
)
from raid import RaidMixin


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
        self.raid_seats = []
        self.raid_seatkeys = frozenset()

        # --- Core-only accounting ---
        self.prev_units = None
        self.lost_units = 0
        self.last_hp = None
        self.income_q = 0

        # --- gunner rotation latch (PIECE I) ---
        self.rot_tgt = None
        self.rot_rnd = -10 ** 9
        self.rot_prev_dir = None
        self.rot_lock_d = 10 ** 9

        # --- one report per unit lifetime, so a bug cannot flood stderr ---
        self.reported_cpu = False
        self.reported_error = False

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
            if (et in (EntityType.GUNNER, EntityType.SENTINEL) and d <= 64) or (
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
        if K_HEAL_BUDGET_ON:
            ct.write_store(SLOT_HEAL_BUDGET, (self.income_q // 4) * K_HEAL_RATE_PCT // 100)

        ti, ammo = ct.get_global_resources(), ct.get_global_ammo()
        home_guns = ct.read_store(SLOT_HOME_GUN)
        fwd_guns = ct.read_store(SLOT_FWD_GUN)
        weapons = home_guns + fwd_guns

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
            if weapons:
                ammo_target = max(ammo_target, min(48, 4 * weapons))
            # A forward Sentinel is 10 ammo every 3 rounds; it is the only
            # sustained damage the raid has once the collar is up, so it gets
            # its own magazine floor rather than sharing the home one.
            if fwd_guns:
                ammo_target = max(ammo_target, min(120, 40 + 20 * fwd_guns))
            ti_floor = 12 if (under or weapons) else 52
            if E1_AMMO_FLOOR_ON and not under:
                ti_floor = max(
                    ti_floor,
                    min(ct.get_harvester_cost(), E1_RESERVE_CAP) + E1_HARV_RESERVE_MARGIN,
                )
            if (under or weapons or harv >= 2) and ammo < ammo_target and ti > ti_floor:
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
        cands = ring(p, 2)
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
                self.map_walls = {
                    (x, y) for y, row in enumerate(self.map_grid)
                    for x, cell in enumerate(row) if cell == "#"
                }
                self.map_ores = [
                    Position(x, y) for y, row in enumerate(self.map_grid)
                    for x, cell in enumerate(row) if cell == "o"
                ]

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
            if (et in (EntityType.GUNNER, EntityType.SENTINEL) and d <= 64) or (
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
        best, best_p = None, 99
        for d in CARDINALS:
            t = p.add(d)
            if not (0 <= t.x < self.mw and 0 <= t.y < self.mh):
                continue
            try:
                bid = ct.get_tile_building_id(t)
                if bid is None or ct.get_team(bid) == self.team:
                    continue
                et = ct.get_entity_type(bid)
            except Exception:
                continue
            pr = {
                EntityType.GUNNER: 0, EntityType.SENTINEL: 0,
                EntityType.CORE: 1, EntityType.HARVESTER: 2,
                EntityType.LAUNCHER: 3, EntityType.CONVEYOR: 4,
                EntityType.SPLITTER: 4, EntityType.BARRIER: 5,
            }.get(et, 6)
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
        if min(t.distance_squared(threat) for t in core_tiles(self.core)) > HUNT_BAND_DSQ:
            return False
        if ct.get_global_resources() < ct.get_sentinel_cost() + SIEGE_HEAL_RESERVE_TI:
            return False
        return not self._live_home_gun(ct)

    def _try_counterbattery(self, ct):
        """Build only a weapon ray that already contains the reported threat."""
        threat = unpack_pos(ct.read_store(SLOT_THREAT))
        if threat is None:
            return False
        if min(t.distance_squared(threat) for t in core_tiles(self.core)) > HUNT_BAND_DSQ:
            return False
        if ct.read_store(SLOT_HARVESTERS) < ECO_NEED and self._live_home_gun(ct):
            # ...unless the Core is provably bleeding.  Real damage is not
            # opening noise, and holding the counterbattery shut through a
            # genuine shelling finished a measured game with zero turrets.
            if not self._core_shelled(ct):
                return False
        p = ct.get_position()
        ban = self._seat_ban()
        choices = (
            (EntityType.SENTINEL, ct.get_sentinel_cost()),
            (EntityType.GUNNER, ct.get_gunner_cost()),
        )
        for turret_type, cost in choices:
            if ct.get_global_resources() < cost:
                continue
            for d in CARDINALS:
                if self._cpu_exhausted(ct):
                    return False
                bp = p.add(d)
                if not (0 <= bp.x < self.mw and 0 <= bp.y < self.mh):
                    continue
                # A turret is impassable, so one planted on a heal seat costs
                # that seat's +4 HP/round for the rest of the match.
                if ban is not None and (bp.x, bp.y) in ban:
                    continue
                # LOKI-18: A FORWARD TURRET AIMS AT THE CORE, NOT AT A BODY.
                # Measured on 185 real games: 327 of our sentinels are built
                # forward (d^2 > 41 from our own core), 97.6% of them already
                # within range of the enemy core -- and 0.0% can fire at it on
                # the round they are built, because THIS site aims at
                # SLOT_THREAT, a transient enemy unit.
                # raid.py's site gates on a CORE tile and is shootable-by-
                # construction, so the 0/319 proves those forward sentinels are
                # not coming from there. This is the path that builds them.
                # Home behaviour is untouched: aiming at the threat is correct
                # beside our own core. Only when the builder is FORWARD and a
                # core tile is actually in range do we prefer the core.
                targets = [threat]
                try:
                    if min(bp.distance_squared(c) for c in core_tiles(E)) <= 32:
                        targets = [c for c in core_tiles(E)
                                   if bp.distance_squared(c) <= 32] + [threat]
                except Exception:
                    targets = [threat]
                for facing in DIRECTIONS:
                    aim = None
                    for cand in targets:
                        try:
                            if ct.can_fire_from(bp, facing, turret_type, cand):
                                aim = cand
                                break
                        except Exception:
                            continue
                    try:
                        if aim is None:
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
        # Launchers are bot-impassable: never seat one on the eight
        # Core-orthogonal heal seats, delivery termini included.
        lban = set()
        if self.core is not None and self.mw and self.mh:
            lban = {(s.x, s.y) for s in heal_seats(self.core, self.mw, self.mh)}
        for d in CARDINALS:
            bp = p.add(d)
            if (bp.x, bp.y) in lban:
                continue
            if not (0 <= bp.x < self.mw and 0 <= bp.y < self.mh):
                continue
            try:
                if ct.can_build_launcher(bp):
                    ct.build_launcher(bp)
                    return True
            except Exception:
                continue
        ct.write_store(SLOT_LAUNCHER, 0)  # build failed -- release the claim
        return False

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
            intruder = self._nearest_home_intruder(ct)
            if intruder is not None:
                self.tgt = intruder
                self._nav(ct, pave=False)
                return
            if self._core_shelled(ct):
                seat = self._seat_seek_target(ct)
                if seat is not None:
                    self.tgt = seat
                    self._nav(ct, pave=False)
                    return
        # Nothing to defend against: the defender is an expander with a beat.
        self._expand(ct)

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
                prio = {
                    EntityType.CORE: 0, EntityType.SENTINEL: 1,
                    EntityType.GUNNER: 2, EntityType.BUILDER_BOT: 3,
                    EntityType.LAUNCHER: 4, EntityType.HARVESTER: 5,
                    EntityType.CONVEYOR: 6, EntityType.SPLITTER: 6,
                    EntityType.BARRIER: 7,
                }.get(et, 8)
                if prio < best_prio:
                    best_prio, best = prio, t
            if best is not None:
                ct.fire(best)
                return
        except Exception:
            pass
        try:
            for eid in ct.get_nearby_entities():
                if ct.get_team(eid) != self.team and ct.can_fire(ct.get_position(eid)):
                    ct.fire(ct.get_position(eid))
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
