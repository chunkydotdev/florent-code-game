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

        # LOKI-RENTGUN.  Deliberately ABOVE the action-cooldown gate, because
        # destroy() is free and cooldown-free (engine-verified,
        # bots/_probe_rentscale): the rent is handed back the instant the
        # harvester dies, on a turn the raider could not have acted at all.
        # It owns the MOVE as well as the action -- a raider that walks away
        # from a live rental never returns it, which is the plank's main
        # failure mode -- so it is placed before the move phase too.
        if LOKI_RENTGUN_ON and self._rent_turn(ct, E, established):
            return

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
        #
        # ⭐ LOKI-RENTGUN RUNS BESIDE THIS, NOT INSTEAD OF IT.  An earlier draft
        # of this arm made the two mutually exclusive on Magnus's first framing
        # ("instead of the salt-ring"); his amendment replaced that with a ROLE
        # SPLIT -- "while another builder works on sealing their core with
        # barriers" -- so the seal is untouched and the split is by raid seat
        # (see _rent_seat).  A renter that has spent its hop budget falls
        # through to this ladder and seals like any other raider.
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

        # 7. LOKI-48: SALT, AND ONLY ON A ROUND THE PARENT SPENT IDLE.
        # Last in the ACTION ranking, as in _v178salt -- and additionally
        # gated on the MOVE the parent would have made this round.  That
        # second gate is the whole arm; see _salt_idle_ok.
        if LOKI_SALTIDLE_ON:
            self.si_reach += 1
            if self._salt_idle_ok(ct, E, p, near):
                self.si_open += 1
                if self._salt_turn(ct, E, p, ti):
                    self.si_fire += 1
                    if LOKI_SALTIDLE_LOG:
                        # Funnel, cumulative per raider: reached step 7 /
                        # gate opened / salt actually acted.  Take the MAX per
                        # unit id when reading a replay back.
                        print("S48", ct.get_id(), self.si_reach,
                              self.si_open, self.si_fire)
                    return True
            if LOKI_SALTIDLE_LOG:
                print("S48", ct.get_id(), self.si_reach,
                      self.si_open, self.si_fire)
        return False

    # --- LOKI-48: the idle gate --------------------------------------------

    def _salt_idle_ok(self, ct, E, p, near):
        """Would this raider have MOVED this round?  If yes, salt is refused.

        WHAT KILLED _v178salt, measured on 25 live games: its mechanism worked
        (20/20 salts landed on a tile the same bot had pecked to <=2 HP, median
        latency 1 round; 6.68 barriers/game against a 3.48-3.72 baseline) and
        its KILL ROUND regressed to median r179 against a pooled r129,
        Mann-Whitney p=0.008.  The diagnosis was never the mechanism: cutting a
        20 HP conveyor costs ~10 raider ACTIONS, acting and moving are mutually
        exclusive for a builder, and this whole line wins on ARRIVAL.  Salt was
        buying denial with the one currency the collar cannot spare.

        SO THE GATE IS ON THE MOVE, NOT ON THE ACTION.  Being last in
        _raid_act only proves no better ACTION existed; the parent's next move
        after a declined action is to WALK, and _v178salt's `return True`
        cancelled that walk.  This reproduces the parent's own movement
        decision, in the parent's order, and permits salt only where that
        decision was "stand still":

          * move cooldown non-zero -- the parent returns before it even picks a
            station, so the round is free by construction; and
          * already standing on the station it picked (or no station at all) --
            the parent's `p == tgt` branch, which moves nothing.

        `_raid_station` is safe to call here: it caches on `raid_rescan`, which
        it sets to `rnd + LOKI_RAID_RESCAN` on the pass that rescans, so the
        move-phase call later this round returns the same station from cache
        and the expensive scan still happens at most once per raider per round.
        `self.tgt` and `self.stuck` are updated exactly as the branch we are
        standing in would have updated them.
        """
        try:
            if ct.get_move_cooldown() != 0:
                return True
        except Exception:
            return False
        try:
            st = self._raid_station(ct, E, near)
        except Exception:
            return False
        self.tgt = st if st is not None else E
        if st is None:
            return False          # the parent walks at the anchor instead
        if p.x == st.x and p.y == st.y:
            self.stuck = 0        # the parent's own bookkeeping on this branch
            return True
        return False

    # --- LOKI-SALT ---------------------------------------------------------

    def _salt_forward(self, t, E):
        """True iff tile t is on the ENEMY side of the two Core anchors.

        A raider that has been thrown home, or one working a belt that runs
        past the midline, must never barrier our own ground or saw at a
        conveyor on our side of the map -- both of those spend the raider on
        something the economy layer owns.
        """
        if self.core is None or E is None:
            return False
        return t.distance_squared(E) < t.distance_squared(self.core)

    def _salt_turn(self, ct, E, p, ti):
        """Melee an adjacent enemy CONVEYOR/SPLITTER, and barrier the corpse.

        WHY THE CARVE-OUT IS NARROW.  LOKI_QUIET_ON silences all builder melee
        and stays on: 2 damage a round against a 500 HP Core that heals +4 for
        1 Ti is not progress, and every peck costs the step that arrival is
        made of.  A belt piece is the one adjacent target where the arithmetic
        inverts -- 20 HP is ten pecks, and the tenth severs a delivery chain.

        WHY THE BARRIER IS NOT OPTIONAL.  The field repairs 40.5% of cut
        conveyors at a median latency of 4 rounds, so a bare cut is a loan.  A
        3 Ti / 30 HP barrier on the dead tile costs them 15 pecks (30 Ti and 15
        builder-turns) to undo.

        Ordered: salt the corpse first (that is the round the cut becomes
        permanent), then cut, then -- capped separately and lower -- barrier an
        empty tile that is itself adjacent to a live belt, which denies the
        rebuild seat before the cut has even landed.
        """
        if self.core is None or E is None or self.mw == 0:
            return False
        rnd = ct.get_current_round()
        marks = self.salt_marks
        if len(marks) > 24:
            cut = rnd - LOKI_SALT_MEMORY
            self.salt_marks = marks = {k: v for k, v in marks.items() if v >= cut}

        # (0) MARK.  Record every adjacent enemy belt piece BEFORE anything is
        # pecked, so the tile that dies to this very turn's peck is already
        # remembered when we come back for it next turn.  This is also what
        # makes the salt work for a conveyor killed by our forward Sentinel.
        belt = []
        for d in CARDINALS:
            t = p.add(d)
            if not (0 <= t.x < self.mw and 0 <= t.y < self.mh):
                continue
            if not self._salt_forward(t, E):
                continue
            try:
                bid = ct.get_tile_building_id(t)
                if bid is None or ct.get_team(bid) == self.team:
                    continue
                et = ct.get_entity_type(bid)
            except Exception:
                continue
            if et in (EntityType.CONVEYOR, EntityType.SPLITTER):
                marks[(t.x, t.y)] = rnd
                try:
                    belt.append((ct.get_hp(bid), t))
                except Exception:
                    belt.append((999, t))

        try:
            bcost = ct.get_barrier_cost()
        except Exception:
            bcost = 3
        can_pay_barrier = (
            ti >= bcost + LOKI_SALT_TI_FLOOR
            and self.salt_n < LOKI_SALT_MAX_PER_UNIT
        )

        # (1) SALT THE CORPSE.  can_build_barrier enforces adjacency and
        # emptiness, so a mark whose tile is still occupied simply fails here
        # and is retried next turn until the memory window expires.
        if can_pay_barrier and marks:
            for d in CARDINALS:
                t = p.add(d)
                k = (t.x, t.y)
                m = marks.get(k)
                if m is None or rnd - m > LOKI_SALT_MEMORY:
                    continue
                if not self._salt_forward(t, E):
                    continue
                try:
                    if not ct.can_build_barrier(t):
                        continue
                    ct.build_barrier(t)
                except Exception:
                    continue
                marks.pop(k, None)
                self.salt_n += 1
                if LOKI_SALT_LOG:
                    print("SALT bar cut r=%d t=%d,%d n=%d"
                          % (rnd, t.x, t.y, self.salt_n))
                return True

        # (2) CUT.  Lowest HP first -- finishing a belt piece is what severs a
        # chain; spreading damage across three of them severs nothing.
        if belt and ti >= LOKI_PECK_TI_FLOOR and self.salt_pecks < LOKI_SALT_CUT_MAX:
            # LOKI-48 DOWNSTREAM TIEBREAK.  A conveyor has out-degree 1, so a
            # belt is a PATH and cutting one link zeroes every harvester
            # UPSTREAM of it -- the nearer their Core the cut lands, the more
            # it severs.  HP still leads (the tenth peck is the one that cuts;
            # spreading damage severs nothing), and the tiebreak is free: `E`
            # and the tile are both already in hand, so this is one extra
            # distance_squared per adjacent belt piece and no new scan.
            if LOKI_SALTIDLE_DOWNSTREAM:
                belt.sort(key=lambda hb: (hb[0], hb[1].distance_squared(E)))
            else:
                belt.sort(key=lambda hb: hb[0])
            for hp, t in belt:
                try:
                    if not ct.can_fire(t):
                        continue
                    ct.fire(t)
                except Exception:
                    continue
                self.salt_pecks += 1
                if LOKI_SALT_LOG:
                    print("SALT cut r=%d t=%d,%d hp=%d n=%d"
                          % (rnd, t.x, t.y, hp, self.salt_pecks))
                return True

        # (3) DENY THE REBUILD SEAT.  Sub-capped below the total, because this
        # one is speculative: it barriers ground next to a belt that is still
        # alive.  It pays when their repair bot arrives and finds the approach
        # tile gone, and it is the cheapest thing a raider can do with a round
        # it was going to spend standing still.
        if (LOKI_SALT_BLOCK_ON and can_pay_barrier
                and self.salt_block_n < LOKI_SALT_BLOCK_MAX):
            for d in CARDINALS:
                t = p.add(d)
                if not (0 <= t.x < self.mw and 0 <= t.y < self.mh):
                    continue
                if not self._salt_forward(t, E):
                    continue
                try:
                    if not ct.can_build_barrier(t):
                        continue
                except Exception:
                    continue
                if not self._salt_beside_belt(ct, t):
                    continue
                try:
                    ct.build_barrier(t)
                except Exception:
                    continue
                self.salt_n += 1
                self.salt_block_n += 1
                if LOKI_SALT_LOG:
                    print("SALT bar blk r=%d t=%d,%d n=%d"
                          % (rnd, t.x, t.y, self.salt_n))
                return True
        return False

    def _salt_beside_belt(self, ct, t):
        """Is t orthogonally adjacent to a live enemy conveyor/splitter?

        Four tile reads, and only for a tile can_build_barrier has already
        accepted, so the whole check runs at most four times a turn.
        """
        for d in CARDINALS:
            q = t.add(d)
            if not (0 <= q.x < self.mw and 0 <= q.y < self.mh):
                continue
            try:
                bid = ct.get_tile_building_id(q)
                if bid is None or ct.get_team(bid) == self.team:
                    continue
                if ct.get_entity_type(bid) in (EntityType.CONVEYOR, EntityType.SPLITTER):
                    return True
            except Exception:
                continue
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

        # ⭐ LOKI-AIMSITE.  THE PARENT TOOK THE FIRST (neighbour, core-tile)
        # PAIR THAT PASSED BOTH PREDICATES AND RETURNED -- no score, no argmax,
        # no tiebreak.  Siting was therefore a function of where the raider's
        # walk happened to stop, and A SENTINEL CANNOT ROTATE (rotate() is
        # gunner-only), so that accidental facing is PERMANENT for the rest of
        # the match.  We were already paying 30 Ti and +20% scale and throwing
        # the AIM away for free.
        #
        # The fix is a scorer with exactly one bonus: a site whose ray runs
        # through an enemy HARVESTER *and* an enemy CORE tile kills the
        # harvester on the way in and then keeps firing into the Core.
        #
        # ⚠ IT DEGRADES TO THE PARENT EXACTLY, BY CONSTRUCTION.  The scan keeps
        # the first site of the best score (`score > best[0]`, strictly), so
        # when no aligned site exists every candidate scores 1 and the FIRST
        # one found wins -- which is the pair the parent's loop would have
        # returned on, in the same iteration order.  That matters because the
        # alignment is MAP-CONDITIONAL: measured over the pool it exists on 8
        # of 15 maps (frostgate 12 sites, midgard 8, antler 6, archipelago 4,
        # drumlin 4, fjordgate 4, nordkap 4, ragnarok 2; 44 total) and NOT AT
        # ALL on the other seven.  On those seven this plank must be a no-op,
        # not a stall.
        harvs = [hp for _, hp in self._enemy_harvesters(ct)] if LOKI_AIMSITE_ON else []
        best = None                          # (score, build_pos, facing)
        for d in CARDINALS:
            bp = p.add(d)
            if not (0 <= bp.x < self.mw and 0 <= bp.y < self.mh):
                continue
            if LOKI_AIMSITE_ON:
                # A sentinel is opaque to our OWN gunners, whose ray is
                # prefix-blocked and team-blind.
                if self._friendly_gun_ray(ct, bp):
                    continue
                if self._cpu_exhausted(ct):
                    break
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
                if not LOKI_AIMSITE_ON:
                    best = (1, bp, facing)
                    break
                score = 1
                for hpos in harvs:
                    try:
                        if (bp.distance_squared(hpos) <= 32
                                and ct.can_fire_from(bp, facing,
                                                     EntityType.SENTINEL, hpos)):
                            score = 2
                            break
                    except Exception:
                        continue
                if best is None or score > best[0]:
                    best = (score, bp, facing)
                if score >= 2:
                    break
            if best is not None and (not LOKI_AIMSITE_ON or best[0] >= 2):
                break

        if best is None:
            return False
        score, bp, facing = best
        if LOKI_AIMSITE_ON:
            # Local catch only on the new path, so the toggle-OFF branch below
            # keeps the parent's exact control flow (a raise there propagates to
            # run()'s blanket catch, as it always did).
            try:
                ct.build_sentinel(bp, facing)
            except Exception:
                return False
        else:
            ct.build_sentinel(bp, facing)
        if LOKI2B_LIVE_CAP_ON:
            # Publish the live count INCLUDING the one just built, so a
            # second raider in the same round does not double-spend the
            # cap before the census refreshes next turn.
            ct.write_store(SLOT_FWD_GUN, (live or 0) + 1)
        else:
            ct.write_store(SLOT_FWD_GUN, ct.read_store(SLOT_FWD_GUN) + 1)
        if LOKI_AIMSITE_LOG and score >= 2:
            print("AIM313 fwd sentinel @%d,%d facing=%s ALIGNED harvester+core r=%d"
                  % (bp.x, bp.y, facing, ct.get_current_round()))
        return True

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

    # --- LOKI-RENTGUN: the rented turret -------------------------------------
    # Magnus, 2026-08-15: "Place a turret and kill enemy harvestor, then place a
    # barrier on the titanium ... turret should be rented, destroy it when it
    # has killed the harvestor.  This is our primary rush tactic, then kill the
    # core."  Full rationale, the engine probe and the sentinel-vs-gunner
    # arithmetic are in doctrine.py under LOKI-RENTGUN.

    def _rent_clear(self):
        """Forget the current rental.  Never touches rent_done/rent_stranded."""
        self.rent_harv = None
        self.rent_ore = None
        self.rent_turret = None
        self.rent_turret_pos = None
        self.rent_rnd = -1
        self.rent_walled = False
        self.rent_keep = False

    def _rent_tile_is(self, ct, pos, eid):
        """True / False / None -- is `eid` still the building standing on `pos`?

        Validated BY TILE rather than by get_hp(eid): a dead id's behaviour is
        not something this project has measured, while the tile read is exact.
        None means the tile could not be read at all (off map, or out of this
        unit's vision) and is deliberately NOT folded into False -- reading
        "unknown" as "gone" abandons a LIVE turret, which is the flattering
        direction and the one that costs us a permanent +20%.
        `is_in_vision` is the safe pre-check: it returns False off-map instead
        of raising, unlike get_tile_building_id.
        """
        if pos is None or eid is None:
            return None
        if not (0 <= pos.x < self.mw and 0 <= pos.y < self.mh):
            return None
        try:
            if not ct.is_in_vision(pos):
                return None
            return ct.get_tile_building_id(pos) == eid
        except Exception:
            return None

    def _rent_escapes(self, ct, p, t):
        """SELF-TRAP GUARD, ported from bots/_v70sb/main.py:1508-1522.

        A BARRIER and a SENTINEL are both bot-impassable and TEAM-BLIND, and
        `_bfs_direction` treats either as blocked terrain, so a raider that
        drops one onto its own last exit is stranded -- we have a field
        observation of 221 rounds of exactly that with no recovery path.
        Require at least one OTHER passable cardinal neighbour of our own tile.
        Applied to the turret site as well as the barrier, which the original
        was not: the turret is a building too.
        """
        escapes = 0
        for e in CARDINALS:
            n = p.add(e)
            if n.x == t.x and n.y == t.y:
                continue
            if not (0 <= n.x < self.mw and 0 <= n.y < self.mh):
                continue
            try:
                if ct.is_tile_passable(n):
                    escapes += 1
            except Exception:
                continue
        return escapes > 0

    def _enemy_harvesters(self, ct):
        """Every LIVE enemy harvester in this unit's vision, as [(id, Position)].

        ONE pass over get_nearby_buildings, shared by the rent path and by the
        forward-sentinel aim scorer, because the file's own rule is not to add a
        second walk of the same list in the same turn.  A harvester can ONLY
        stand on ore, so its tile IS the ore tile -- no separate ore scan and no
        map read anywhere in this plank.
        """
        out = []
        try:
            nearby = ct.get_nearby_buildings()
        except Exception:
            return out
        for eid in nearby:
            try:
                if ct.get_entity_type(eid) != EntityType.HARVESTER:
                    continue
                if ct.get_team(eid) == self.team:
                    continue
                out.append((eid, ct.get_position(eid)))
            except Exception:
                continue
        return out

    def _friendly_gun_ray(self, ct, tile):
        """Would a building on `tile` stand inside one of OUR gunners' rays?

        A gunner's ray is prefix-blocked and TEAM-BLIND -- it stops on the first
        body of either colour -- so our own barrier or turret dropped on a
        friendly firing line silently switches that gunner off for the match.
        (A SENTINEL is never affected: its line is pure arithmetic and ignores
        obstacles.  This guard is about the gunners we already own, not about
        the sentinel being planted.)
        ⛔ THE OBVIOUS IMPLEMENTATION IS A CONSTANT FALSE, AND THIS ONE IS NOT.
        The first build of this guard asked `can_fire_from(gun, dir, GUNNER,
        tile)`.  `bots/_probe_rayempty`, re-run 2026-08-15, shows a GUNNER's
        can_fire_from is FALSE ON EVERY EMPTY TILE -- 5 gunners, every empty
        step False, True only where a body already stands -- while a SENTINEL's
        is True on empties.  The tile we are about to build on is BY DEFINITION
        EMPTY, so that guard could not once have vetoed anything: a check that
        cannot produce the other verdict has not been seen to check.

        `get_attackable_tiles_from` is the RAW pattern and is the right
        question: the installed API says it "includes the full firing line
        within range, even behind walls", and the same probe confirms
        in_pattern=True on tiles whose can_fire_from is False.
        Deliberately conservative -- it also vetoes a tile further along a ray
        that something else already blocks.  That is wrong in the safe
        direction.  Fails OPEN on an unreadable entity, because a veto we
        cannot justify would silently disable the whole plank.
        """
        try:
            nearby = ct.get_nearby_buildings()
        except Exception:
            return False
        key = (tile.x, tile.y)
        for eid in nearby:
            try:
                if ct.get_entity_type(eid) != EntityType.GUNNER:
                    continue
                if ct.get_team(eid) != self.team:
                    continue
                for t in ct.get_attackable_tiles_from(
                        ct.get_position(eid), ct.get_direction(eid),
                        EntityType.GUNNER):
                    if (t.x, t.y) == key:
                        return True
            except Exception:
                continue
        return False

    def _rent_find_harvester(self, ct, p):
        """Nearest live enemy harvester in vision, as (id, Position).

        Bounded by LOKI_RENT_SEEK_DSQ (= a builder's vision r^2), so the raider
        never walks at a remembered target.  Harvesters this raider has already
        finished with are skipped by tile, which is what makes the HOP work:
        without it the raider re-targets the barrier it just planted forever.
        """
        best_id, best_pos, best_d = None, None, 10 ** 9
        done = getattr(self, "rent_seen", None) or ()
        for eid, hp in self._enemy_harvesters(ct):
            if (hp.x, hp.y) in done:
                continue
            d = p.distance_squared(hp)
            if d < best_d:
                best_d, best_id, best_pos = d, eid, hp
        if best_id is None or best_d > LOKI_RENT_SEEK_DSQ:
            return None, None
        return best_id, best_pos

    def _rent_approach(self, ct, p, target):
        """The cardinal neighbour of `target` we should stand on, or None.

        Nearest passable one; our own tile counts as passable because
        is_tile_passable is False on a tile a builder is already standing on.
        """
        best, best_d = None, 10 ** 9
        for d in CARDINALS:
            t = target.add(d)
            if not (0 <= t.x < self.mw and 0 <= t.y < self.mh):
                continue
            if t.x == p.x and t.y == p.y:
                return t
            try:
                if not ct.is_tile_passable(t):
                    continue
            except Exception:
                continue
            dd = p.distance_squared(t)
            if dd < best_d:
                best_d, best = dd, t
        return best

    def _rent_seat(self):
        """Is THIS raider a harvester-hunter, or a core-sealer?

        Magnus's amendment is a ROLE SPLIT, not a replacement -- "while another
        builder works on sealing their core with barriers".  The split is taken
        off `raid_slot`, the monotone seat this raider was issued at birth,
        which is the same source `_raid_station` already uses to spread the ring
        without a single store write.  With MOD 2 / SEAT 0 that is every other
        raider hunting and the rest running the untouched ladder -- including
        the seal, which stays ON for everybody.
        """
        if LOKI_RENT_SEAT_MOD <= 1:
            return True
        return (self.raid_slot % LOKI_RENT_SEAT_MOD) == LOKI_RENT_SEAT

    def _rent_turn(self, ct, E, established):
        """One rental, start to finish.  True == this raider's turn is spent.

        Returning True cancels BOTH the action ladder and the move for this
        round, which is how the raider pins itself beside a live rental.
        Returning False after a free destroy() is deliberate: the destroy costs
        no cooldown, so the body still gets its normal raid turn afterwards.
        """
        if not LOKI_RENTGUN_ON:
            return False
        try:
            # A raider mid-rental always finishes it, even if the seat says
            # sealer -- otherwise a mid-flight toggle strands a live turret.
            if getattr(self, "rent_turret_pos", None) is None and not self._rent_seat():
                return False
            p = ct.get_position()
            rnd = ct.get_current_round()
            if getattr(self, "rent_turret_pos", None) is not None:
                return self._rent_close(ct, p, rnd, E)
            return self._rent_open(ct, p, rnd, established, E)
        except Exception:
            # Never let the plank cost the body its turn on a surprise; the
            # blanket catch in main.run() would swallow the whole raid turn.
            return False

    def _rent_open(self, ct, p, rnd, established, E):
        """Find a harvester, get orthogonally adjacent to it, plant the turret."""
        if getattr(self, "rent_done", 0) >= LOKI_RENT_HOP_MAX:
            return False
        hid, hpos = self._rent_find_harvester(ct, p)
        if hid is None:
            return self._rent_prospect(ct, p, rnd, established, E)

        # THE WHOLE SEQUENCE RUNS FROM ONE TILE orthogonally adjacent to the
        # ore: from there the raider can reach the ore (barrier) and the turret
        # (destroy) without ever moving again.  See the geometry note in
        # doctrine.py.
        if abs(p.x - hpos.x) + abs(p.y - hpos.y) != 1:
            if established and p.distance_squared(hpos) > LOKI_RENT_NEAR_DSQ:
                # At the ring the Core is the prize, so only a step-or-two
                # detour is taken there -- never a walk back out.  It is not
                # zero, because a defender's harvesters sit INSIDE the
                # establish band (d^2 <= 40) on most maps, and refusing every
                # detour there was throwing away the commonest target.
                return False
            if ct.get_move_cooldown() != 0:
                return True
            appr = self._rent_approach(ct, p, hpos)
            if appr is None:
                return False
            self.tgt = appr
            self._nav(ct, pave=False)
            return True

        return self._rent_build(ct, p, rnd, hid, hpos, E)

    def _rent_prospect(self, ct, p, rnd, established, E):
        """Walk at enemy-half ORE when no harvester is in sight.

        ⚠ THIS IS WHAT MAKES THE HOP REAL, AND IT WAS ADDED BECAUSE THE FIRST
        BUILD MEASURED SHORT.  A builder's vision is r^2=20, so a hunter that
        only reacts to what it can already see cannot chain: after the first
        kill the next harvester is nearly always out of vision.  Six-map smoke
        on the vision-only build, `fcode run` seed 3: archipelago 4 rentals
        (its ore happens to cluster), antler 1, midgard 1, and drumlin,
        frostgate and nordkap ZERO.  Three maps where the plank could not fire
        at all is not a plank.

        The map itself is KNOWN (`known_map_for` -> self.map_ores), and a
        harvester can only ever stand on ore, so the hunter walks at the
        nearest ore tile on THEIR half of the midline and lets vision do the
        rest.  Bounded three ways: only hunters (`_rent_seat`), only until the
        hop budget is spent, and only until the raider is established at the
        ring -- past that the Core is the prize and this stops entirely.
        """
        if established or not self.map_ores:
            return False
        if ct.get_move_cooldown() != 0:
            return False
        # A prospect that cannot be reached must not hold the body for the
        # match: give it a walking budget, then retire the tile and re-pick.
        tgt = getattr(self, "rent_prospect", None)
        if tgt is not None and rnd - getattr(self, "rent_prospect_rnd", rnd) > LOKI_RENT_PROSPECT_MAX:
            if getattr(self, "rent_seen", None) is None:
                self.rent_seen = set()
            self.rent_seen.add((tgt.x, tgt.y))
            tgt = None
        if tgt is None or (tgt.x, tgt.y) in (getattr(self, "rent_seen", None) or ()):
            best, best_d = None, 10 ** 9
            done = getattr(self, "rent_seen", None) or ()
            for o in self.map_ores:
                if (o.x, o.y) in done:
                    continue
                if not self._salt_forward(o, E):
                    continue
                d = p.distance_squared(o)
                if d < best_d:
                    best_d, best = d, o
            if best is None:
                return False
            tgt = best
            self.rent_prospect = tgt
            self.rent_prospect_rnd = rnd
        appr = self._rent_approach(ct, p, tgt)
        self.tgt = appr if appr is not None else tgt
        self._nav(ct, pave=False)
        return True

    def _rent_build(self, ct, p, rnd, hid, hpos, E):
        """Plant the SENTINEL.  See doctrine.py for why not a Gunner.

        ⭐ THE SITE IS SCORED, NOT TAKEN FIRST-MATCH, and the score decides
        whether this is a RENTAL or a KEEPER.  A site whose ray runs through
        the harvester AND ON THROUGH AN ENEMY CORE TILE is not rented back:
        once the harvester dies it keeps firing into the Core for free, and
        tearing down a free core-damage engine to recover +20% scale is a bad
        trade.  Any other site is a pure rental and comes back.
        """
        if ct.get_action_cooldown() != 0:
            return True                     # hold the tile; do not wander off
        # AMMO IS THE GATE, NOT THE TITANIUM.  can_fire() returns True at 0
        # ammo on this engine and fire() RAISES, so the predicate is not an
        # affordability test -- read the pool.  A turret we cannot fire is
        # 30 Ti plus a +20% tax we would then have to walk back for.
        if ct.get_global_ammo() < LOKI_RENT_AMMO_MIN:
            return False
        if ct.get_global_resources() < ct.get_sentinel_cost() + LOKI_RENT_TI_FLOOR:
            return False
        if self._cpu_exhausted(ct):
            return False
        cores = core_tiles(E) if E is not None else ()
        best = None                          # (score, build_pos, facing)
        for d in CARDINALS:
            bp = p.add(d)
            if not (0 <= bp.x < self.mw and 0 <= bp.y < self.mh):
                continue
            if bp.x == hpos.x and bp.y == hpos.y:
                continue
            # A SENTINEL is a building: bot-impassable and team-blind, so it
            # walls its own builder in exactly as a barrier does.
            if not self._rent_escapes(ct, p, bp):
                continue
            # And it is opaque to our OWN gunners, whose ray is prefix-blocked.
            if self._friendly_gun_ray(ct, bp):
                continue
            # Two candidate facings per site: straight at the harvester, and --
            # when a core tile is collinear beyond it -- the facing that runs
            # THROUGH the harvester and on into the Core.  The second is the
            # keeper.  Both are put to can_fire_from; alignment is never
            # assumed, exactly as _try_forward_sentinel does it.
            facings = []
            f0 = bp.direction_to(hpos)
            if f0 != Direction.CENTRE:
                facings.append(f0)
            if LOKI_RENT_AIMED_KEEP_ON:
                for c in cores:
                    if bp.distance_squared(c) > 32:
                        continue
                    fc = bp.direction_to(c)
                    if fc != Direction.CENTRE and fc not in facings:
                        facings.append(fc)
            for facing in facings:
                try:
                    if bp.distance_squared(hpos) > 32:
                        continue
                    if not ct.can_fire_from(bp, facing, EntityType.SENTINEL, hpos):
                        continue
                    if not ct.can_build_sentinel(bp, facing):
                        continue
                except Exception:
                    continue
                score = 1
                if LOKI_RENT_AIMED_KEEP_ON:
                    for c in cores:
                        try:
                            if (bp.distance_squared(c) <= 32
                                    and ct.can_fire_from(bp, facing,
                                                         EntityType.SENTINEL, c)):
                                score = 2
                                break
                        except Exception:
                            continue
                if best is None or score > best[0]:
                    best = (score, bp, facing)
                if score >= 2:
                    break
            if best is not None and best[0] >= 2:
                break

        if best is None:
            return False
        score, bp, facing = best
        try:
            tid = ct.build_sentinel(bp, facing)
        except Exception:
            return False
        self.rent_harv = hid
        self.rent_ore = hpos
        self.rent_turret = tid
        self.rent_turret_pos = bp
        self.rent_rnd = rnd
        self.rent_walled = False
        # THE KEEP/RENT DECISION IS MADE HERE, AT BUILD TIME, off the site's own
        # geometry -- never re-derived later, when the harvester it was aimed
        # through is gone and the ray can no longer be reconstructed.
        self.rent_keep = (score >= 2)
        if self.rent_keep:
            # A keeper IS a forward sentinel, so it takes a forward-sentinel
            # cap slot like any other.  A RENTAL deliberately does not: that
            # slot never decrements (the LOKI-2b rubble bug, doctrine.py:1239)
            # and three rentals would close the forward arm for the match.  The
            # Core funds a rental's magazine through LOKI_RENT_AMMO_BANK.
            try:
                ct.write_store(SLOT_FWD_GUN, ct.read_store(SLOT_FWD_GUN) + 1)
            except Exception:
                pass
        if LOKI_RENT_LOG:
            print("RENT313 open turret=%d@%d,%d harv=%d@%d,%d r=%d %s"
                  % (tid, bp.x, bp.y, hid, hpos.x, hpos.y, rnd,
                     "KEEP-aimed-at-core" if self.rent_keep else "RENT"))
        return True

    def _rent_retire(self, ore):
        """Finish with this ore tile and free the raider to HOP to the next one.

        Called on EVERY exit -- kill, timeout or strand -- because
        `_rent_find_harvester` picks the nearest harvester and would otherwise
        re-target the one we just walled (or just failed on) for the rest of the
        match.  This set IS the hop.
        """
        if ore is not None:
            if getattr(self, "rent_seen", None) is None:
                self.rent_seen = set()
            self.rent_seen.add((ore.x, ore.y))
        self.rent_done = getattr(self, "rent_done", 0) + 1
        self._rent_clear()

    def _rent_close(self, ct, p, rnd, E):
        """Guard the rental, then hand the turret back and salt the ore.

        ORDER MATTERS AND IT IS NOT THE READING ORDER.  The barrier costs the
        round's ACTION; destroy() costs nothing at all -- free, no cooldown,
        unlimited per turn, and the probe destroyed and then built in one
        run().  So the barrier is attempted FIRST and the destroy runs after it
        in the SAME turn, and the destroy still runs on turns where the action
        cooldown forbids the barrier.  The other order would cost a round of
        rent for nothing.
        """
        tpos = self.rent_turret_pos
        ore = getattr(self, "rent_ore", None)
        turret = self._rent_tile_is(ct, tpos, getattr(self, "rent_turret", None))
        harv = self._rent_tile_is(ct, ore, getattr(self, "rent_harv", None))
        adj_t = abs(p.x - tpos.x) + abs(p.y - tpos.y) == 1
        age = rnd - getattr(self, "rent_rnd", rnd)

        # THE AMMO ANSWER.  If the pool empties under us the sentinel simply
        # stops and `harv` stays True forever; this clock is what turns that
        # into a BOUNDED titanium loss instead of a permanent +20%.
        finished = (harv is False) or age >= LOKI_RENT_HOLD_MAX

        if not finished:
            if turret is False:
                # They killed the turret first.  Nothing to hand back and the
                # ore is still theirs -- release the body rather than guard a
                # hole.  Its scale contribution went with it.
                self._rent_clear()
                return False
            return True                     # GUARD: pin the body, do not move

        acted = False
        keep = bool(getattr(self, "rent_keep", False))
        # 1. SALT THE ORE.  Only on a real kill, never on a timeout, or we
        # would spend 3 Ti walling a tile they still hold.  30 HP / 2 dmg per
        # builder peck = 15 of their actions to take it back.
        if (harv is False and ore is not None and not getattr(self, "rent_walled", False)
                and ct.get_action_cooldown() == 0
                and abs(p.x - ore.x) + abs(p.y - ore.y) == 1
                and ct.get_global_resources() >= ct.get_barrier_cost()
                and self._rent_escapes(ct, p, ore)
                and not self._friendly_gun_ray(ct, ore)):
            try:
                if ct.can_build_barrier(ore):
                    ct.build_barrier(ore)
                    self.rent_walled = True
                    acted = True
            except Exception:
                pass

        # 2a. A KEEPER IS NOT HANDED BACK.  Its ray runs through the dead
        # harvester's tile and on into an enemy Core tile, so it is now a free
        # forward sentinel firing for the rest of the match.  Tearing that down
        # to recover +20% scale is a bad trade -- Magnus's amendment, and it
        # reverses the original "always destroy" spec.  Note the ore barrier
        # above does NOT block it: a sentinel line ignores obstacles.
        if keep and turret is not False:
            if LOKI_RENT_LOG:
                print("RENT313 keep turret=%s r=%d age=%d walled=%s"
                      % (self.rent_turret, rnd, age, self.rent_walled))
            self._rent_retire(ore)
            return acted

        # 2b. HAND THE TURRET BACK -- free and cooldown-free, so it runs in the
        # same turn as the barrier above.
        if turret is True and adj_t:
            try:
                if ct.can_destroy(tpos):
                    ct.destroy(tpos)
                    if LOKI_RENT_LOG:
                        print("RENT313 return turret=%s r=%d age=%d walled=%s"
                              % (self.rent_turret, rnd, age, self.rent_walled))
                    self._rent_retire(ore)
                    # False when nothing but the free destroy happened: the
                    # body keeps its action AND its move this round, which is
                    # the tempo the cooldown-free destroy buys, and the HOP to
                    # the next harvester starts on the same turn.
                    return acted
            except Exception:
                pass

        if turret is False:
            # Already gone -- the ore is salted (or unreachable) and there is
            # nothing to return.  Count it: the sequence completed either way.
            self._rent_retire(ore)
            return acted

        # 3. STRANDED.  We are not beside our own live turret.  This is not
        # hypothetical -- a launcher picks up any adjacent builder from EITHER
        # team and throws it, which is exactly what the exile detector in
        # _raid exists for.  Walk back and hand it in, on a bounded clock:
        # a raider that cannot get back is worth more at the Core than orbiting
        # 30 Ti of rubble, and holding the +20% forever is the thing we are
        # buying our way out of.
        if age >= LOKI_RENT_HOLD_MAX + LOKI_RENT_RECOVER_MAX:
            if LOKI_RENT_LOG:
                print("RENT313 STRANDED turret=%s@%d,%d r=%d walled=%s"
                      % (self.rent_turret, tpos.x, tpos.y, rnd,
                         getattr(self, "rent_walled", False)))
            self.rent_stranded = getattr(self, "rent_stranded", 0) + 1
            self._rent_retire(ore)
            return acted
        if acted or ct.get_move_cooldown() != 0:
            return True
        # Prefer the ORE while it is still unsalted and the turret is only
        # unreadable (out of vision); otherwise walk at the turret itself.
        back = None
        if harv is False and not getattr(self, "rent_walled", False) and ore is not None:
            back = self._rent_approach(ct, p, ore)
        if back is None:
            back = self._rent_approach(ct, p, tpos)
        if back is None:
            self._rent_clear()
            return False
        self.tgt = back
        self._nav(ct, pave=False)
        return True

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
        gun_axis = set()
        try:
            for bid in ct.get_nearby_buildings():
                if ct.get_team(bid) == self.team:
                    continue
                if ct.get_entity_type(bid) == EntityType.LAUNCHER:
                    threats.append(ct.get_position(bid))
                # LOKI-25: GUNNER FIRING AXES.  92% of our FORWARD builder deaths
                # are enemy gunners against 42.8% for the rest of the league
                # (4,379 vs 6,830 forward deaths) -- so this is a property of
                # where our raiders stand, not of the game.  A gunner's shot is a
                # straight line that IS BLOCKED by obstacles and reaches only
                # r^2=13; a sentinel's ignores obstacles.  **We are dying almost
                # entirely to the AVOIDABLE one.**  `get_attackable_tiles_from`
                # returns a hypothetical turret's pattern and has ZERO call sites
                # anywhere in this tree -- the exact predicate this needs was
                # never once invoked.
                elif ct.get_entity_type(bid) == EntityType.GUNNER:
                    try:
                        gp = ct.get_position(bid)
                        gd = ct.get_direction(bid)
                        for t in ct.get_attackable_tiles_from(
                                gp, gd, EntityType.GUNNER):
                            gun_axis.add((t.x, t.y))
                    except Exception:
                        continue
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
            # Same penalty machinery, one more entity type. A station on a live
            # gunner's ray is a station that dies; stepping one tile off it costs
            # nothing and forces them to spend 10 Ti AND a full action cooldown
            # to rotate -- a tempo trade in our favour even when they answer it.
            if (s.x, s.y) in gun_axis:
                score += LOKI_GUNAXIS_PENALTY
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
