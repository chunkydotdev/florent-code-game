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

LOKI-16 -- RING-BODY DENIAL.  One thing this file did NOT do is keep a body
anywhere.  It walks raiders onto the twelve spawn-ring tiles and it seals the
eight SEATS with barriers, but it re-scores stations every LOKI_RAID_RESCAN
rounds and it explicitly pushes a raider OFF a corner (+12) the moment both
flanking seats are sealed -- which is the moment that corner has become pure
body-denial, and the four corners are the ring tiles no barrier here ever
covers.  Measured over 539,000 exposed builder-rounds with round < 250, ONE
hostile body on the ring doubles the defender's 25-round core-death hazard,
2.24% -> 4.77%, intervals disjoint; bodies 2-12 are unmeasured.  So exactly one
raider is pinned to the ring tile it stands on and never re-scored
(_ring_hold), and nothing else in the file changes.
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
            # LOKI-16.  The full twelve -- seats AND corners -- because the
            # denial measurement is about SPAWN tiles, and the four corners are
            # spawn tiles that no barrier in this file ever covers.  Set here
            # rather than in main.__init__ so that file stays untouched; _ring
            # is called before every reader of this attribute.
            self.raid_ringkeys = frozenset(
                (t.x, t.y) for t in (self.raid_corners + self.raid_seats)
            )
        return self.raid_corners, self.raid_seats

    # --- LOKI-16: the one pinned body --------------------------------------

    def _ring_hold(self, ct, E, rnd):
        """Am I the ONE raider that stays on its ring tile?  Sets self.ring_pin.

        The measurement this serves: one hostile body on the twelve-tile spawn
        ring doubles the defender's 25-round core-death hazard over rounds
        < 250 (2.24% -> 4.77%, 539k exposed builder-rounds, intervals disjoint).
        Bodies 2-12 are UNMEASURED, so this pins one and only one.

        It is a refusal, not a mechanism.  Nothing here moves, builds or fires;
        it only publishes a station that _raid_station then returns unchanged,
        which makes the movement block in _raid see target == position and do
        nothing.  Every other action in _raid_act is untouched, so the pinned
        body keeps sealing seats, buddy-healing and holding the collar.

        THE ELECTION IS A PER-UNIT APPROXIMATION and is one on purpose: the
        comms store is full (16/16 slots allocated in doctrine.py), so there is
        no slot to elect a holder in.  Instead each raider standing on a ring
        tile looks at the other eleven -- all of them inside r^2=18, well within
        a builder's r^2=20 vision -- and claims only if it sees no LOWER-id
        friendly builder bot already standing on one.  Ties cannot happen
        because entity ids are unique; the residual failure is arrival timing
        (two bodies landing in the same round each seeing an empty ring), which
        pins two for as long as it takes them to see each other.

        A tile out of vision counts as EMPTY here, which is the direction that
        claims rather than refuses.  The pessimistic alternative -- treat the
        unknown as occupied by someone better -- would refuse the pin whenever
        the ring is partly unseen, i.e. exactly on arrival, when the pin is
        worth most.
        """
        if not LOKI16_RING_HOLD_ON:
            self.ring_pin = None
            return None
        p = ct.get_position()
        corners, seats = self._ring(E)
        if (p.x, p.y) not in self.raid_ringkeys:
            # Not on the ring: no pin, and any pin we held is gone.  A launcher
            # throw lands here, which is why the claim below can re-fire.
            self.ring_hold = False
            self.ring_pin = None
            return None
        if getattr(self, "ring_hold", False):
            # Already pinned, and a pin has NO expiry -- "keep it" is the whole
            # prescription.  Re-published every round against the CURRENT tile
            # so a body that was moved and happens to still be on the ring pins
            # where it actually stands.
            self.ring_pin = p
            return p
        if rnd >= LOKI16_HOLD_CLAIM_RND:
            # The hazard was measured on rounds < 250.  A NEW pin outside that
            # band is not what was measured, so it is not claimed.
            self.ring_pin = None
            return None
        try:
            me = ct.get_id()
        except Exception:
            self.ring_pin = None
            return None
        for t in corners + seats:
            if t.x == p.x and t.y == p.y:
                continue
            try:
                if not ct.is_in_vision(t):
                    continue
                oid = ct.get_tile_builder_bot_id(t)
                if oid is None or oid >= me:
                    continue
                if ct.get_team(oid) != self.team:
                    continue
            except Exception:
                continue
            # Someone lower-numbered is already standing on the ring.  It is
            # the holder; this body goes back to being an ordinary raider.
            self.ring_pin = None
            return None
        self.ring_hold = True
        self.ring_pin = p
        return p

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
        if LOKI6_BEAT_BEFORE_PAUSE and E is not None:
            # FIX 2. Publish BEFORE any early return. A raider standing at the
            # ring is a live foothold even while its own navigation is paused,
            # and this heartbeat is the only thing that keeps the cold-insert
            # gate open for the rest of the team.
            try:
                if min(ct.get_position().distance_squared(c)
                       for c in core_tiles(E)) <= LOKI_ESTABLISH_DSQ:
                    ct.write_store(SLOT_RAID_LIVE, rnd + 1)
            except Exception:
                pass
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

        # LOKI-16.  Decide the pin BEFORE anything can consume the turn, so the
        # answer is the same whether this round ends in an action or a move --
        # _raid_station is not reached on an acting round, and the ferry guard
        # below needs the current answer rather than last round's.
        self._ring_hold(ct, E, rnd)

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
        if LOKI6_STALL_SEPARATE:
            # FIX 1. Count only THIS round's navigation failure, not the
            # position-unchanged increments that productive action also causes.
            if self.stuck > before:
                self.nav_fail = getattr(self, "nav_fail", 0) + 1
            else:
                self.nav_fail = 0
            stalled = self.nav_fail >= 8
        else:
            stalled = self.stuck > before and self.stuck >= 8
        if stalled:
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
            self.nav_fail = 0
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
        if on_seat and ti >= LOKI_PECK_TI_FLOOR and not LOKI_QUIET_ON:
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
        if (ti >= LOKI_PECK_TI_FLOOR and not LOKI_QUIET_ON
                and self._raid_peck(ct, seatkeys)):
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
        # LOKI-16.  The pinned body is not re-scored.  This single return is
        # the whole plank at the movement layer: without it, _raid_station
        # adds +12 to a corner whose flanking seats are both sealed and walks
        # the body off the one tile a barrier can never cover.
        pin = getattr(self, "ring_pin", None)
        if pin is not None:
            self.raid_station = pin
            return pin
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
        if getattr(self, "ring_pin", None) is not None:
            # LOKI-16.  A pinned body does not advertise for a hop.  The ferry
            # throws to any site strictly closer to the enemy anchor, and from
            # a ring tile that includes OTHER ring tiles -- so without this the
            # one thing the plank promises to keep could be picked up and put
            # down somewhere else by our own launcher.
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
        friendly_bots = []
        for eid in ct.get_nearby_entities():
            try:
                if ct.get_entity_type(eid) != EntityType.BUILDER_BOT:
                    continue
                bp = ct.get_position(eid)
                if bp.distance_squared(lp) > 2:
                    continue
                if ct.get_team(eid) == self.team:
                    friendly_bots.append((eid, bp))
                    continue
            except Exception:
                continue
            far = sorted(sites, key=lambda t: t.distance_squared(self.core), reverse=True)
            for site in far:
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
