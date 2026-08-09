"""LOKI-1 raid layer -- THE COLLAR.  Ablatable as a unit: delete this module's
call sites in main.py and what remains is a plain economy bot.

THE PROBLEM THIS EXISTS FOR (pre-registered target).  Against opponents rated
>=1550 our per-window kill hazard runs 15.1 / 5.9 / 7.7 / 9.8 % over r0-150,
r150-200, r200-300, r300+, while theirs runs 9.8 / 5.9 / 12.5 / 40.9 %.  The
ratio is 1.54 early and 0.62 by r200-300.  We START kills fine -- 29.8% of
games produce one, median r148 -- and then fail to CLOSE about 70% of them.
So the job is CLOSING, and TIME IS THEIR ASSET: any design that merely
lengthens games moves us into the window where they convert four times better.

WHY SIEGES DON'T CLOSE, in one number.  A builder heals +4 HP for 1 Ti, every
round, from any of the eight tiles orthogonally adjacent to the 2x2 footprint.
That is 0.25 Ti per HP against roughly 0.56 for any attacker.  Measured over 14
decoded ladder games the NET HP to kill a Core is a stable 500-512 while the
RAW hits landed ranged from 28 to 1206 -- a 43x spread that is entirely the
defender's heal line.  A siege that is not out-healing the defender is not
making progress however long it runs, and ours was not.

THE MECHANISM.  Those same eight tiles are ALSO the only tiles a conveyor can
deliver into a Core from, and eight of the twelve tiles it can spawn a builder
onto.  They are a single chokepoint for healing, income and reinforcement.  A
BARRIER is 3 Ti for 30 HP and is bot-impassable; breaking one costs 15 builder
pecks at 2 Ti each, i.e. 30 Ti and 15 rounds of a body -- a 10:1 exchange in
our favour, and every round they spend pecking is a round they are not healing.
A raider standing on one of the four DIAGONAL ring tiles is orthogonally
adjacent to exactly the two seats flanking it and to no Core tile, so four
corner raiders can seal all eight seats.  Sealed, the defender's heal rate is
zero and every point of damage we land is permanent.

The damage itself then comes from a forward SENTINEL.  This is not a turret
preference, it is forced: barriers block line of sight, so a Gunner ray dies on
our own collar, while the Sentinel line ignores obstacles and shoots THROUGH
it.  18 damage on a 2-round reload is 6 HP/round against a defender who can no
longer repair -- 500 HP in ~84 rounds.  Opened at the median kill-attempt round
of r148 that lands inside r200-300, which is the window we are trying to move.

COLD INSERTION vs FOOTHOLD REINFORCEMENT.  This file was first written with no
round gate at all, on a brief that turned out to rest on a refuted premise.
The corpus that refuted it (11,895 forward throws) shows median raider life
after a throw collapsing 43 -> 6 rounds at exactly r150 and only 2.34% of
r200+ throws ever landing one attack -- so sending a FRESH body on a long walk
into intact defences is measurably dead late, and the incumbent's r180 cutoff
was a correct constant justified by a wrong reason.  The other half of the same
corpus is why this module still exists: of the 528 raiders that did land
attacks, 25 produced half of all 40,114 attacks and 319 were on the WINNING
team.  Establishment wins games; the throw does not.

So the two are separated.  COLD INSERTION -- a raider that holds nothing
walking at an undamaged ring -- is open only until LOKI_COLD_INSERT_RND.
FOOTHOLD REINFORCEMENT -- any round in which some raider is still acting at the
ring, published as a heartbeat in SLOT_RAID_LIVE -- has no cutoff at all,
because that is precisely the state the winning raiders were in.  Everything
this file does at the destination is a survival package for that state:
barriers deposited on the first action after landing (value that outlives the
body), those same barriers as LOS cover against Gunner rays, arrival spread
across twelve stations rather than one, stations covered by a visible enemy
Launcher scored down and banned after a throw, mutual healing between adjacent
raiders, and a forward Sentinel -- a 40 HP BUILDING that keeps firing after
every body in the raid is dead.
"""
from fcode import Direction, EntityType, Position

from doctrine import *  # noqa: F401,F403
from eco import core_corners, core_tiles, enemy_core_for, heal_seats, unpack_pos


class RaidMixin:

    # --- target acquisition ------------------------------------------------

    def _enemy_anchor(self, ct):
        """The enemy Core anchor, or None.

        Store first (a builder that has SEEN the Core publishes the true
        position), then map symmetry.  Never an opponent-specific tile table:
        the one we shipped was keyed to a single opponent's build and that
        opponent shipped a new version.
        """
        if self.enemy is not None:
            return self.enemy
        e = unpack_pos(ct.read_store(SLOT_ENEMY_CORE))
        if e is None and self.core is not None and self.mw and self.mh:
            e = enemy_core_for(self.mw, self.mh, self.core)
        self.enemy = e
        return e

    def _ring(self, E):
        """(corners, seats) of the enemy footprint, cached per unit.

        Both are pure functions of the anchor and the map dimensions, so every
        raider derives the same twelve tiles with no store traffic at all.
        """
        key = (E.x, E.y)
        if self.raid_ring_key != key:
            self.raid_ring_key = key
            self.raid_corners = core_corners(E, self.mw, self.mh)
            self.raid_seats = heal_seats(E, self.mw, self.mh)
            self.raid_seatkeys = frozenset((s.x, s.y) for s in self.raid_seats)
        return self.raid_corners, self.raid_seats

    # --- the turn ----------------------------------------------------------

    def _foothold_live(self, ct, rnd):
        """Is some raider still ACTING at the enemy ring right now?

        The heartbeat is written below by any raider inside LOKI_ESTABLISH_DSQ
        of an enemy Core tile.  It is the one signal that separates the state
        the winning 319 raiders were in ("established") from the state the
        r200+ corpus says is dead ("thrown, six rounds to live").
        """
        beat = ct.read_store(SLOT_RAID_LIVE)
        return bool(beat) and rnd - (beat - 1) <= LOKI_FOOTHOLD_STALE

    def _raid_open(self, ct, rnd, established):
        """May THIS raider be on the raid this round?

        Three ways in, and only the first is time-limited:
          * COLD INSERTION, open until LOKI_COLD_INSERT_RND;
          * this raider is itself established at the ring -- never withdrawn,
            because a raider that is still acting there is the asset;
          * a teammate's foothold is live, so this body is reinforcement into
            a position we already hold rather than a fresh six-round throw.
        """
        if established:
            return True
        if rnd < LOKI_COLD_INSERT_RND:
            return True
        return self._foothold_live(ct, rnd)

    def _raid(self, ct):
        E = self._enemy_anchor(ct)
        rnd = ct.get_current_round()
        if E is None or rnd < self.raid_pause_until:
            # STATE-BASED stand-down: with no anchor there is nothing to raid,
            # and a raider that cannot reach the ring is worth more on ore than
            # oscillating against a wall.
            self._expand(ct)
            return

        p = ct.get_position()
        established = min(p.distance_squared(c) for c in core_tiles(E)) <= LOKI_ESTABLISH_DSQ
        if established:
            ct.write_store(SLOT_RAID_LIVE, rnd + 1)
        elif not self._raid_open(ct, rnd, established):
            # Cold-insertion window closed and no live foothold to reinforce.
            # The body goes back to the economy; it is NOT retired, so the
            # moment a teammate re-establishes, this rejoins on the next turn.
            # The ferry ping is skipped with it, or the launcher would fling a
            # stood-down body forward and re-open cold insertion by the back
            # door -- which is the exact thing the corpus says stops working.
            self._expand(ct)
            return
        self._raid_ferry_ping(ct)

        # EXILE DETECTION.  A launcher throws any adjacent builder from EITHER
        # team, so a position that jumped more than one step since our last
        # turn means we were picked up.  If the throw moved us AWAY from the
        # target, the station we were working is covered by a launcher: ban it
        # and re-enter the ring somewhere else rather than walking back into
        # the same pickup.  Trail memory is cleared for the same reason
        # _v103split clears it on a drop -- pave_prev is now arbitrarily far.
        if self.raid_prev is not None and p.distance_squared(self.raid_prev) > LOKI_TELEPORT_DSQ:
            if (
                self.raid_station is not None
                and p.distance_squared(E) > self.raid_prev.distance_squared(E)
            ):
                self.raid_ban[(self.raid_station.x, self.raid_station.y)] = rnd + 80
            self.raid_station = None
            self.raid_rescan = rnd
            self.tgt = None
            self.stuck = 0
            self.pave_prev = None
            self.pave_dir = None
            self.pave_rnd = -2
        self.raid_prev = p

        near = established or (
            min(p.distance_squared(c) for c in core_tiles(E)) <= LOKI_APPROACH_DSQ
        )

        if ct.get_action_cooldown() == 0 and self._raid_act(ct, E, near):
            return

        if self._cpu_exhausted(ct):
            return
        if ct.get_move_cooldown() != 0:
            return

        st = self._raid_station(ct, E, near)
        self.tgt = st if st is not None else E
        if p.x == self.tgt.x and p.y == self.tgt.y:
            self.stuck = 0
            return
        before = self.stuck
        self._nav(ct, pave=False)
        if self.stuck > before and self.stuck >= 8:
            # Navigation stall.  Ban this station and take another; if the
            # whole ring is unreachable the pause below hands the body back to
            # the economy for a bounded spell instead of grinding a wall.
            if self.raid_station is not None:
                self.raid_ban[(self.raid_station.x, self.raid_station.y)] = rnd + 120
            self.raid_station = None
            self.raid_rescan = rnd
            self.stuck = 0
            # Rotate the far-phase assignment too, or an unreachable preassigned
            # station would be re-chosen for the rest of the match.
            self.raid_slot += 1
            self.raid_stalls += 1
            if self.raid_stalls >= 3:
                self.raid_stalls = 0
                self.raid_pause_until = rnd + 60

    # --- the productive action ---------------------------------------------

    def _raid_act(self, ct, E, near):
        """One action, ranked so that ARRIVING is already productive.

        The prior finding this ordering answers: every long-game launcher-throw
        loop examined in our replays belonged to the DEFENDER disposing of the
        attacker's raiders, so a lone raider beside a defended Core is food.
        The answer is not to protect the body but to make the body deposit
        something that outlives it -- a barrier is placed on the first action
        after landing and is still there after an exile.
        """
        p = ct.get_position()
        ti = ct.get_global_resources()
        self._ring(E)
        seatkeys = self.raid_seatkeys
        on_seat = (p.x, p.y) in seatkeys

        # 1. STANDING ON A SEAT: peck the Core.  Two damage a round that the
        # collar makes permanent, plus the seat itself is denied by our body.
        if on_seat and ti >= LOKI_PECK_TI_FLOOR:
            for c in core_tiles(E):
                if abs(p.x - c.x) + abs(p.y - c.y) != 1:
                    continue
                try:
                    if ct.can_fire(c):
                        ct.fire(c)
                        return True
                except Exception:
                    continue

        # 2. SEAL A FREE SEAT.  can_build_barrier enforces adjacency, emptiness
        # and occupancy, so a seat one of our own raiders is standing on is
        # refused by the engine and stays a peck station.
        if LOKI_BARRIER_SEAL_ON and ti >= ct.get_barrier_cost() + LOKI_SEAL_TI_FLOOR:
            for d in CARDINALS:
                t = p.add(d)
                if (t.x, t.y) not in seatkeys:
                    continue
                try:
                    if ct.can_build_barrier(t):
                        ct.build_barrier(t)
                        return True
                except Exception:
                    continue

        # 3. THE FORWARD SENTINEL.  Built on the approach, before the ring is
        # reached, because that is where the 5-tile band is.
        if self._try_forward_sentinel(ct, E):
            return True

        # 3b. LOKI-3: THE FORWARD LAUNCHER.  Ranked BELOW the sentinel and the
        # seal on purpose.  The sentinel is the damage and the barrier is value
        # that outlives the body; a launcher is neither -- it is denial, and
        # denial of a heal line only pays while something else is landing
        # damage on the Core.  Ranked ABOVE the heals because it is
        # opportunity-gated: it only fires at all when a live enemy builder is
        # standing in pickup range right now, and that window closes.
        if self._try_forward_launcher(ct, E):
            return True

        # 4. BUDDY HEAL -- the survival half of the package.  heal(pos) repairs
        # every friendly entity standing on pos, a friendly BUILDER BOT
        # included, at +4 HP for 1 Ti.  Against a Gunner's 7 damage on a
        # 1-round reload (3.5 HP/round) a single neighbour healing a wounded
        # raider more than cancels it, and the measured failure mode is exactly
        # this: median raider life after a throw is six rounds.  Gated on a
        # real wound (LOKI_BUDDY_HEAL_GAP) so it never outbids sealing or a
        # peck for cosmetic damage.
        if near:
            for d in CARDINALS:
                t = p.add(d)
                if not (0 <= t.x < self.mw and 0 <= t.y < self.mh):
                    continue
                try:
                    oid = ct.get_tile_builder_bot_id(t)
                    if (
                        oid is not None and ct.get_team(oid) == self.team
                        and ct.get_hp(oid) <= ct.get_max_hp(oid) - LOKI_BUDDY_HEAL_GAP
                        and ct.can_heal(t)
                    ):
                        ct.heal(t)
                        return True
                except Exception:
                    continue

        # 5. HOLD THE COLLAR.  +4 HP for 1 Ti against their 2 dmg for 2 Ti: a
        # raider parked beside its own barriers out-repairs a pecker two to one
        # on HP and eight to one on titanium, so the seal does not decay -- and
        # the same barriers are the raider's own LOS cover against Gunner rays.
        if near:
            for d in CARDINALS:
                t = p.add(d)
                if not (0 <= t.x < self.mw and 0 <= t.y < self.mh):
                    continue
                try:
                    bid = ct.get_tile_building_id(t)
                    if (
                        bid is not None and ct.get_team(bid) == self.team
                        and ct.get_hp(bid) < ct.get_max_hp(bid)
                        and ct.can_heal(t)
                    ):
                        ct.heal(t)
                        return True
                except Exception:
                    continue

        # 6. Otherwise clear whatever is in the way.
        if ti >= LOKI_PECK_TI_FLOOR and self._raid_peck(ct, seatkeys):
            return True
        return False

    def _raid_peck(self, ct, seatkeys):
        """Melee the best adjacent enemy building.

        An enemy CONVEYOR standing on one of their own seats ranks above every
        other soft target: it is 20 HP (ten pecks) and killing it converts that
        seat from theirs into a tile we can seal permanently for 3 Ti -- and it
        was carrying their delivery, which is tiebreak #1.
        """
        p = ct.get_position()
        best, best_pr = None, 99
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
            if et == EntityType.CORE:
                pr = 0
            elif (t.x, t.y) in seatkeys and et in (EntityType.CONVEYOR, EntityType.SPLITTER):
                pr = 1
            elif et == EntityType.LAUNCHER:
                pr = 2
            elif et in (EntityType.GUNNER, EntityType.SENTINEL):
                pr = 3
            elif et == EntityType.HARVESTER:
                pr = 4
            elif et in (EntityType.CONVEYOR, EntityType.SPLITTER):
                pr = 5
            else:
                pr = 6
            if pr >= best_pr:
                continue
            try:
                if ct.can_fire(t):
                    best_pr, best = pr, t
            except Exception:
                continue
        if best is not None:
            ct.fire(best)
            return True
        return False

    def _try_forward_sentinel(self, ct, E):
        """Plant a Sentinel whose line already contains an enemy Core tile.

        SENTINEL, not Gunner, and not as a preference: the collar blocks LOS,
        so a Gunner built to shoot the Core would be shooting our own barriers.
        can_fire_from is the hypothetical-turret predicate (ignores ammo and
        cooldown by contract), which is exactly the question asked here.

        LOKI-2: inside the committed-opening window the harvester prerequisite
        and the bank floor are relaxed (doctrine.py, LOKI-2 block).  99.3% of
        1,269 early Core kills are turret fire and the sub-r80 recipe is three
        turrets planted by r22 -- a rush is over before the economy the LOKI-1
        gate waits for would have paid for anything.  The cap is untouched: 3
        is already the specialists' number.
        """
        if not LOKI_FWD_SENTINEL_ON:
            return False
        live = self._live_fwd_guns(ct, E) if LOKI2B_LIVE_CAP_ON else None
        if (live if live is not None else ct.read_store(SLOT_FWD_GUN)) >= LOKI_FWD_GUN_CAP:
            return False
        rush = LOKI2_RUSH_ON and ct.get_current_round() < LOKI2_RUSH_RND
        min_harv = LOKI2_RUSH_MIN_HARV if rush else LOKI_FWD_MIN_HARV
        ti_floor = LOKI2_RUSH_TI_FLOOR if rush else LOKI_FWD_TI_FLOOR
        if ct.read_store(SLOT_HARVESTERS) < min_harv:
            return False
        cost = ct.get_sentinel_cost()
        if ct.get_global_resources() < cost + ti_floor:
            return False
        p = ct.get_position()
        tiles = core_tiles(E)
        # A Sentinel reaches r^2 = 32; a build site is one step from here, so
        # anything past ~50 cannot possibly align and the scan is skipped.
        if min(p.distance_squared(c) for c in tiles) > 50:
            return False
        if self._cpu_exhausted(ct):
            return False
        for d in CARDINALS:
            bp = p.add(d)
            if not (0 <= bp.x < self.mw and 0 <= bp.y < self.mh):
                continue
            for target in tiles:
                if bp.distance_squared(target) > 32:
                    continue
                facing = bp.direction_to(target)
                if facing == Direction.CENTRE:
                    continue
                try:
                    if not ct.can_fire_from(bp, facing, EntityType.SENTINEL, target):
                        continue
                    if not ct.can_build_sentinel(bp, facing):
                        continue
                except Exception:
                    continue
                ct.build_sentinel(bp, facing)
                if LOKI2B_LIVE_CAP_ON:
                    # Publish the live count INCLUDING the one just built, so a
                    # second raider in the same round does not double-spend the
                    # cap before the census refreshes next turn.
                    ct.write_store(SLOT_FWD_GUN, (live or 0) + 1)
                else:
                    ct.write_store(SLOT_FWD_GUN, ct.read_store(SLOT_FWD_GUN) + 1)
                return True
        return False

    def _live_fwd_guns(self, ct, E):
        """Count LIVE friendly sentinels near the enemy Core, or None if blind.

        Returns None when this unit cannot see the siege band at all, so the
        caller falls back to the monotone store rather than reading a census of
        zero as "the cap is free" and spamming turrets from across the map.
        """
        try:
            p = ct.get_position()
            tiles = core_tiles(E)
            if min(p.distance_squared(c) for c in tiles) > LOKI2B_CENSUS_DSQ * 2:
                return None
            me = ct.get_team()
            n = 0
            for eid in ct.get_nearby_buildings():
                if ct.get_entity_type(eid) != EntityType.SENTINEL:
                    continue
                if ct.get_team(eid) != me:
                    continue
                bp = ct.get_position(eid)
                if min(bp.distance_squared(c) for c in tiles) <= LOKI2B_CENSUS_DSQ:
                    n += 1
            return n
        except Exception:
            return None

    # --- LOKI-3: the kidnap plank, placement half --------------------------

    def _try_forward_launcher(self, ct, E):
        """Plant a Launcher beside a live enemy builder at their ring.

        THE HALF WE HAVE NEVER BUILT.  We build 0.64 launchers per game and not
        one of them forward, while 20.65% of enemy-builder-rounds before r250
        sit beside a tile we could physically have built a launcher on, and 0
        of 1,355 games have zero opportunity.  The machine works -- 3,126 exile
        throws before r250 off those 0.64 launchers -- it is only ever pointed
        at our own doorstep.

        WHAT IT IS FOR, precisely.  Not killing the builder: a Gunner needs six
        shots and ~11 rounds for 40 HP and the target walks off the ray in one.
        It is for throwing their HEALERS off the eight collar seats.  The heal
        line is why Cores survive (28 -> 1206 raw hits for a stable 500-512 net
        HP), so a defender in transit is a defender not repairing, and that is
        the only currency here.

        The 16.03% "still there next round" filter is why this reads the board
        rather than a plan: a turret cannot fire the round it is built, and by
        the same token a launcher cannot throw the round it is built, so the
        builder we can see now is a bet on the builder being there next turn.
        """
        if not (LOKI_KIDNAP_ON and LOKI_KIDNAP_FWD_ON):
            return False
        cost = ct.get_launcher_cost()
        if ct.get_global_resources() < cost + LOKI_KIDNAP_TI_FLOOR:
            return False
        p = ct.get_position()
        tiles = core_tiles(E)
        if min(p.distance_squared(c) for c in tiles) > LOKI_KIDNAP_CENSUS_DSQ:
            return False
        if self._cpu_exhausted(ct):
            return False
        live = self._live_fwd_launchers(ct, E)
        if live is None or live >= LOKI_KIDNAP_FWD_CAP:
            return False
        # SCORE BOTH SIGNALS.  Two cuts measured before this one, on the same
        # 24-game fixture, both below the pre-registered bars:
        #   aimed at a VISIBLE BUILDER  -> placement 50.0%, throws  8.3%
        #   aimed at the COLLAR SEATS   -> placement 33.3%, throws  0.0%
        # The seat-only cut is worse for a reason worth writing down: LOKI
        # SEALS those seats with BARRIERS, 3 Ti and permanent, so the tiles a
        # seat-aimed launcher wants are the tiles our own collar is already
        # taking -- and a sealed seat has no healer on it to throw.  A launcher
        # is 20 Ti plus 10% launcher scale and evicts ONE body per round, which
        # walks back.  On this chassis the cheaper mechanism already exists.
        # This cut is the strongest form of the plank: a seat is worth more
        # than a transient body (it recurs, ~40% occupancy against both
        # measured opponents) but a body in range is worth something now, so
        # both count and neither gates the other.
        self._ring(E)          # populates raid_seats; cheap and cached per anchor
        seats = self.raid_seats
        foes = []
        try:
            for eid in ct.get_nearby_units():
                if ct.get_entity_type(eid) != EntityType.BUILDER_BOT:
                    continue
                if ct.get_team(eid) == self.team:
                    continue
                foes.append(ct.get_position(eid))
        except Exception:
            foes = []
        best, best_n = None, 0
        for d in CARDINALS:
            bp = p.add(d)
            if not (0 <= bp.x < self.mw and 0 <= bp.y < self.mh):
                continue
            n = 2 * sum(1 for s in seats
                        if bp.distance_squared(s) <= LOKI_KIDNAP_PICKUP_DSQ)
            n += sum(1 for f in foes
                     if bp.distance_squared(f) <= LOKI_KIDNAP_PICKUP_DSQ)
            if n <= best_n:
                continue
            try:
                if not ct.can_build_launcher(bp):
                    continue
            except Exception:
                continue
            best, best_n = bp, n
        if best is None:
            return False
        try:
            ct.build_launcher(best)
        except Exception:
            return False
        return True

    def _live_fwd_launchers(self, ct, E):
        """Count LIVE friendly launchers near the enemy Core, or None if blind.

        A LIVE CENSUS, deliberately, and never a monotone store counter.  That
        counter is exactly LOKI-2b's defect: SLOT_FWD_GUN was only ever written
        as read+1, so it counted rubble, and three destroyed forward sentinels
        closed the arm PERMANENTLY for the rest of the match.  There is no
        store slot for this at all -- all 16 are in use and none is needed,
        because the caller has already established it can see a live enemy
        builder beside the site, so this census cannot be blind when consulted.
        """
        try:
            p = ct.get_position()
            tiles = core_tiles(E)
            if min(p.distance_squared(c) for c in tiles) > LOKI_KIDNAP_CENSUS_DSQ * 2:
                return None
            me = ct.get_team()
            n = 0
            for eid in ct.get_nearby_buildings():
                if ct.get_entity_type(eid) != EntityType.LAUNCHER:
                    continue
                if ct.get_team(eid) != me:
                    continue
                bp = ct.get_position(eid)
                if min(bp.distance_squared(c) for c in tiles) <= LOKI_KIDNAP_CENSUS_DSQ:
                    n += 1
            return n
        except Exception:
            return None

    # --- station choice ----------------------------------------------------

    def _raid_station(self, ct, E, near):
        """Which of the twelve ring tiles this raider is walking to.

        FAR: a deterministic seat derived from this unit's raid slot, so the
        raid spreads across the ring on the way in without a single store write
        and without four bodies funnelling onto one tile.
        NEAR: rescored from live vision every LOKI_RAID_RESCAN rounds.
        """
        rnd = ct.get_current_round()
        corners, seats = self._ring(E)
        stations = corners + seats
        if not stations:
            return None
        if not near:
            return stations[self.raid_slot % len(stations)]
        if self.raid_station is not None and rnd < self.raid_rescan:
            return self.raid_station
        self.raid_rescan = rnd + LOKI_RAID_RESCAN

        p = ct.get_position()
        me = ct.get_id()
        # One pass for the launchers that can exile us off a station.
        threats = []
        try:
            for bid in ct.get_nearby_buildings():
                if ct.get_team(bid) == self.team:
                    continue
                if ct.get_entity_type(bid) == EntityType.LAUNCHER:
                    threats.append(ct.get_position(bid))
        except Exception:
            pass

        ncorner = len(corners)
        best, best_k = None, None
        for i, s in enumerate(stations):
            key = (s.x, s.y)
            if self.raid_ban.get(key, 0) > rnd:
                continue
            standing_here = (p.x == s.x and p.y == s.y)
            try:
                if ct.is_in_vision(s) and not standing_here:
                    if not ct.is_tile_passable(s):
                        continue
                    other = ct.get_tile_builder_bot_id(s)
                    if other is not None and other != me:
                        continue
            except Exception:
                pass
            score = abs(p.x - s.x) + abs(p.y - s.y)
            if i < ncorner:
                # A corner is a BUILD station and is only worth holding while
                # it still has an unsealed seat beside it.
                if self._open_seats_by(ct, s) == 0:
                    score += 12
                else:
                    score -= 6
            else:
                # A seat is a PECK station: two damage a round plus denial.
                score -= 3
            for tp in threats:
                if s.distance_squared(tp) <= 2:
                    score += LOKI_EXILE_PENALTY
                    break
            if standing_here:
                score -= 2  # hysteresis: do not shuffle between equal tiles
            k = (score, (s.x * 17 + s.y * 31 + self.raid_slot * 7) % 97, s.y, s.x)
            if best_k is None or k < best_k:
                best, best_k = s, k
        self.raid_station = best
        return best

    def _open_seats_by(self, ct, corner):
        """How many seats orthogonally beside `corner` still need sealing.

        Unreadable (out of vision) counts as OPEN: the pessimistic direction
        here is to walk to a corner that turns out to be finished, which costs
        one rescan, against refusing to walk to one that is not, which costs
        the seal.
        """
        n = 0
        for d in CARDINALS:
            t = corner.add(d)
            if (t.x, t.y) not in self.raid_seatkeys:
                continue
            try:
                if not ct.is_in_vision(t):
                    n += 1
                    continue
                if ct.get_tile_building_id(t) is None:
                    n += 1
            except Exception:
                n += 1
        return n

    # --- the ferry ---------------------------------------------------------

    def _raid_ferry_ping(self, ct):
        """Advertise for a launcher hop -- WITHOUT waiting for one.

        _v103split had a `launchwait` role that parked a builder beside the
        launcher until it was thrown; that spends the one resource the hazard
        table says belongs to the opponent.  Here the raider simply walks, and
        publishes its id whenever it happens to be inside the launcher's
        neighbourhood.  Store writes are buffered one round, which is why the
        ping fires from r^2 <= 8 rather than from the pickup ring itself.
        """
        if not LOKI_FERRY_ON or self.enemy is None:
            return
        try:
            for bid in ct.get_nearby_buildings():
                if ct.get_team(bid) != self.team:
                    continue
                if ct.get_entity_type(bid) != EntityType.LAUNCHER:
                    continue
                if ct.get_position(bid).distance_squared(ct.get_position()) <= 8:
                    ct.write_store(SLOT_FERRY_ID, ct.get_id() + 1)
                    ct.write_store(SLOT_FERRY_RND, ct.get_current_round())
                    return
        except Exception:
            return

    def _launcher_turn(self, ct):
        """Launcher: exile intruders first, then ferry raiders forward.

        No lifetime cap and no round cutoff on the ferry -- the two gates that
        made the incumbent's insertion pipeline dead code from r180.
        """
        if self.team is None:
            self.team = ct.get_team()
            self.mw, self.mh = ct.get_map_width(), ct.get_map_height()
        ct.write_store(SLOT_LAUNCHER, 1)
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
        lp = ct.get_position()
        w, h = self.mw, self.mh
        dest = self._enemy_anchor(ct)

        # Reachable throw sites, computed once: r^2 <= 26 from the launcher.
        sites = []
        for dx in range(-5, 6):
            for dy in range(-5, 6):
                if dx * dx + dy * dy > 26:
                    continue
                t = Position(lp.x + dx, lp.y + dy)
                if 0 <= t.x < w and 0 <= t.y < h:
                    sites.append(t)

        # 1. EXILE.  Pickup is the full 8-neighbourhood at d^2 <= 2 (measured,
        # 1471/1472 wild throw events).  This is the same tool the field uses
        # against our raiders, and it is the cheapest home defence we own.
        #
        # LOKI-3 changes only WHERE the victim lands, never whether it is
        # thrown.  A launcher beside OUR Core is doing home defence and throws
        # intruders as far from OUR Core as it can reach -- LOKI-2b's rule,
        # kept verbatim.  A FORWARD launcher is the same tool pointed the other
        # way: the builders beside it are DEFENDERS, and the direction that
        # buys anything is away from THEIR Core, off the eight collar seats.
        friendly_bots = []
        enemy_bots = []
        for eid in ct.get_nearby_entities():
            try:
                if ct.get_entity_type(eid) != EntityType.BUILDER_BOT:
                    continue
                bp = ct.get_position(eid)
                if bp.distance_squared(lp) > LOKI_KIDNAP_PICKUP_DSQ:
                    continue
                if ct.get_team(eid) == self.team:
                    friendly_bots.append((eid, bp))
                else:
                    enemy_bots.append(bp)
            except Exception:
                continue

        if enemy_bots:
            away = self.core
            if LOKI_KIDNAP_ON and dest is not None:
                # Which Core is this launcher actually near?  That, not a flag,
                # decides which way the throw points.
                if lp.distance_squared(dest) < lp.distance_squared(self.core):
                    away = dest
            bonus = self._our_ray_sites(ct, sites) if LOKI_KIDNAP_ON else frozenset()
            ranked = sorted(
                sites,
                key=lambda t: t.distance_squared(away)
                + (LOKI_KIDNAP_RAY_BONUS if (t.x, t.y) in bonus else 0),
                reverse=True,
            )
            for bp in enemy_bots:
                for site in ranked:
                    try:
                        if ct.can_launch(bp, site):
                            ct.launch(bp, site)
                            return
                    except Exception:
                        continue

        # 2. FERRY.  Only the raider that pinged, only while the ping is fresh,
        # and only to a site strictly closer to the enemy Core than it stands.
        if not LOKI_FERRY_ON or dest is None or not friendly_bots:
            return
        want = ct.read_store(SLOT_FERRY_ID)
        if not want:
            return
        if ct.get_current_round() - ct.read_store(SLOT_FERRY_RND) > LOKI_FERRY_STALE_RNDS:
            return
        near_first = sorted(sites, key=lambda t: t.distance_squared(dest))
        for eid, bp in friendly_bots:
            if eid + 1 != want:
                continue
            here = bp.distance_squared(dest)
            for site in near_first:
                if site.distance_squared(dest) >= here:
                    break
                try:
                    if ct.can_launch(bp, site):
                        ct.launch(bp, site)
                        ct.write_store(SLOT_FERRY_ID, 0)
                        return
                except Exception:
                    continue
            return

    def _our_ray_sites(self, ct, sites):
        """Which of these throw sites stand on one of OUR OWN live turret lines.

        Returns a frozenset of (x, y).  Empty is the honest answer in most
        positions and the caller must survive it -- the ray bonus is a bonus,
        never a precondition for throwing.

        THREE THINGS THIS IS CAREFUL ABOUT, each of which would otherwise turn
        the bonus into a lie:

        1. AMMO.  A Gunner shot costs 4 from the team pool and we start at 0
           with no passive income.  Steering a victim onto a line we cannot
           fire is worse than not steering at all, because the sort has already
           paid distance for it.  Below LOKI_KIDNAP_MIN_AMMO this returns empty.

        2. OCCUPANCY.  get_attackable_tiles_from ignores ammo, cooldown AND
           occupancy by contract, so for a Gunner it happily reports tiles
           behind our own barriers -- and the collar is made of barriers, which
           is precisely the geometry LOKI-1 built on purpose.  So that call is
           only a cheap PREFILTER; can_fire_from is the instrument that decides,
           and it is bounded to LOKI_KIDNAP_RAY_CONFIRMS calls for the 10 ms.

        3. OUR OWN BODIES.  A site adjacent to one of our raiders is not
           steered to: we would be inviting a Gunner ray onto our own collar
           holder, and the Sentinel line pierces everything in it.
        """
        try:
            if ct.get_global_ammo() < LOKI_KIDNAP_MIN_AMMO:
                return frozenset()
            keys = {(t.x, t.y) for t in sites}
            me = self.team
            prefilter = set()
            turrets = []
            for eid in ct.get_nearby_buildings():
                et = ct.get_entity_type(eid)
                if et != EntityType.GUNNER and et != EntityType.SENTINEL:
                    continue
                if ct.get_team(eid) != me:
                    continue
                turrets.append((eid, et))
                if len(turrets) >= 4:
                    break
            if not turrets:
                return frozenset()
            for eid, et in turrets:
                try:
                    tp = ct.get_position(eid)
                    td = ct.get_direction(eid)
                    for t in ct.get_attackable_tiles_from(tp, td, et):
                        k = (t.x, t.y)
                        if k in keys:
                            prefilter.add((k, tp, td, et))
                except Exception:
                    continue
            if not prefilter:
                return frozenset()
            confirmed = set()
            n = 0
            for k, tp, td, et in prefilter:
                if n >= LOKI_KIDNAP_RAY_CONFIRMS:
                    break
                n += 1
                pos = Position(k[0], k[1])
                try:
                    if not self._would_shoot(ct, tp, td, et, pos, me):
                        continue
                    # Never steer a victim onto a tile touching one of ours.
                    mine = False
                    for d in CARDINALS:
                        a = pos.add(d)
                        oid = ct.get_tile_builder_bot_id(a)
                        if oid is not None and ct.get_team(oid) == me:
                            mine = True
                            break
                    if not mine:
                        confirmed.add(k)
                except Exception:
                    continue
            return frozenset(confirmed)
        except Exception:
            return frozenset()

    def _would_shoot(self, ct, tp, td, et, pos, me):
        """Would OUR turret at tp actually shoot a body newly standing on pos?

        MEASURED, NOT ASSUMED (probe `bots/_probe_rayempty`, s25, atoll seed 1).
        The two turret types answer this question with DIFFERENT PREDICATES, and
        using the obvious one for both is a silent no-op:

          GUNNER   -- can_fire_from is FALSE on every EMPTY tile of its own ray.
                      Measured: gunner at (3,12) facing EAST, steps 1/2/3 all
                      empty and all in_pattern=True, can_fire_from False on all
                      three; the same predicate answers True the moment a tile
                      holds anything.  So a gunner's ray CANNOT be evaluated
                      with can_fire_from against a throw destination, which is
                      empty by definition.  Had this shipped, the gunner half of
                      the bonus would have scored zero in every position, in
                      every game, while looking perfectly healthy.
                      Blocking is real and separate: gunner at (0,14), step 1
                      bot -> True, steps 2/3 (the Core behind it) -> False.
                      So the gunner test is written directly: same facing line,
                      and every tile strictly between the turret and pos empty.

          SENTINEL -- can_fire_from is TRUE on empty tiles and TRUE through
                      occupied ones (measured: sentinel at (4,13) facing EAST,
                      all five steps empty -> True; at (1,13), True through a
                      bot at step 1, a bot at step 2 and a building at step 3).
                      Its line pierces by spec, so the predicate is geometric
                      and is used as-is.

        THE SENTINEL ALSO HAS A PRIORITY PROBLEM, which is ours, not the
        engine's: our own turret code ranks CORE 0, SENTINEL 1, GUNNER 2,
        BUILDER_BOT 3 (main.py).  If a higher-priority enemy already stands on
        that ray, the sentinel shoots THAT and the kidnapped body is never
        touched -- so the bonus would be a lie.  Note we do NOT want to
        "fix" that ordering: a sentinel shooting their Core is the primary
        currency and outranks any kidnap.  We simply decline the bonus.
        """
        if et == EntityType.SENTINEL:
            if not ct.can_fire_from(tp, td, et, pos):
                return False
            # A higher-priority enemy on the same ray wins the shot.
            for t in ct.get_attackable_tiles_from(tp, td, et):
                bid = ct.get_tile_building_id(t)
                if bid is None or ct.get_team(bid) == me:
                    continue
                if ct.get_entity_type(bid) in (
                    EntityType.CORE, EntityType.SENTINEL, EntityType.GUNNER
                ):
                    return False
            return True
        # GUNNER: geometry by hand, because the predicate needs an occupant.
        dx, dy = td.delta()
        if dx == 0 and dy == 0:
            return False
        ddx, ddy = pos.x - tp.x, pos.y - tp.y
        # Must lie on the facing ray: same direction, and exactly on the line.
        if dx == 0:
            if ddx != 0 or ddy == 0 or (ddy > 0) != (dy > 0):
                return False
            steps = abs(ddy)
        elif dy == 0:
            if ddy != 0 or ddx == 0 or (ddx > 0) != (dx > 0):
                return False
            steps = abs(ddx)
        else:
            if abs(ddx) != abs(ddy) or ddx == 0:
                return False
            if (ddx > 0) != (dx > 0) or (ddy > 0) != (dy > 0):
                return False
            steps = abs(ddx)
        if steps * steps * (2 if (dx and dy) else 1) > 13:
            return False    # gunner attack r^2 = 13
        # Every tile strictly between must be clear, or the ray stops short.
        for s in range(1, steps):
            t = Position(tp.x + dx * s, tp.y + dy * s)
            if ct.get_tile_building_id(t) is not None:
                return False
            if ct.get_tile_builder_bot_id(t) is not None:
                return False
        return True
