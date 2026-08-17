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
from eco import (
    core_corners, core_tiles, dsq_core, enemy_core_for, heal_seats,
    nearest_core_tile, sge_centre_q4, unpack_pos,
)

# Hoisted: `_raid_peck` rebuilt its if-chain per tile and `_salt_turn` its
# tuple per tile.  Same membership, same priorities.
BELT_TYPES = frozenset((EntityType.CONVEYOR, EntityType.SPLITTER))
TURRET_TYPES = frozenset((EntityType.GUNNER, EntityType.SENTINEL))


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
            # LOKI-TURBO: `_raid_station` concatenated these two lists on every
            # call, including the once-per-round far-phase lookup.
            self.raid_stations = self.raid_corners + self.raid_seats
        return self.raid_corners, self.raid_seats

    # --- the turn ----------------------------------------------------------

    def _raid_beat(self, ct, rnd, E=None):
        """The raid heartbeat, the collar ledger and the siege band, one write.

        ONE write to slot 15 per raider per round, from the only two places in
        the tree that write it.  Bits 0-9 are the heartbeat exactly as they have
        always been; bits 10-27 are three six-bit lanes and this body owns
        `raid_slot % COLLAR_LANES` of them.  A body republishes ITS OWN lane
        with its own exact cumulative spend every round, so a write lost to
        another raider in the same round costs one round of latency and repairs
        itself -- which is the property the fork's slot-13 counter did not have
        and could not be given (doctrine.py, "WHERE THE COUNTER LIVES").

        FIX B: bits 28-29 now carry the enemy-Core HP band for the same reason,
        arrived at from the other direction.  The band's PUBLISHED copy lived in
        slot 13, was written only on a TRANSITION, and lost its race with
        `_arch_note` in 2 of 4 audited games -- so `SGE mass3` fired 0.04 times
        a game and the collar surge with it.  Here it rides the heartbeat: one
        writer, republished whole every round.  A raider WITH eyes on a Core
        tile publishes what it sees; a raider without publishes what it READ, so
        a blind body is a no-op on the field rather than an eraser.

        With COLLAR_ON and both band consumers down, the lane and band terms are
        both 0 and this writes `rnd + 1`, the parent's statement unchanged.
        """
        v = rnd + 1
        if COLLAR_ON and COLLAR_BUDGET_SHARED:
            try:
                lanes = ct.read_store(COLLAR_SPENT_SLOT) >> COLLAR_LANE_SHIFT
            except Exception:
                lanes = 0
            # FIX B: the band now sits ABOVE the lanes in the same word, so the
            # read has to stop at the lane field or bits 28-29 would ride round
            # again on the shift back and never be refreshed.
            lanes &= (1 << (COLLAR_LANE_BITS * COLLAR_LANES)) - 1
            sh = COLLAR_LANE_BITS * (self.raid_slot % COLLAR_LANES)
            mine = self.col_spent
            if mine > COLLAR_LANE_MASK:
                mine = COLLAR_LANE_MASK
            lanes = (lanes & ~(COLLAR_LANE_MASK << sh)) | (mine << sh)
            v |= lanes << COLLAR_LANE_SHIFT
        if E is not None and SIEGE_BAND_SAFE_ON and self._sge_band_armed():
            # Memoised on the round, so for an established raider this is the
            # same call `_sge_mass_ok` and the collar surge already make.
            band = self._sge_core_band(ct, E) & SIEGE_HPBAND_MASK
            v |= band << SIEGE_BAND15_SHIFT
        ct.write_store(COLLAR_SPENT_SLOT, v)

    def _sge_band_armed(self):
        """Does anything consume the enemy-Core HP band on this build?

        Two consumers: `_sge_mass_ok`'s third tube and the collar's terminal
        surge.  With both down nothing derives, publishes or reads the band, and
        slot 15 is the parent's plain heartbeat.
        """
        return SIEGE_MASS_ON or (COLLAR_ON and COLLAR_SURGE_ON)

    def _foothold_live(self, ct, rnd):
        """Is some raider still ACTING at the enemy ring right now?

        The heartbeat is written below by any raider inside LOKI_ESTABLISH_DSQ
        of an enemy Core tile.  It is the one signal that separates the state
        the winning 319 raiders were in ("established") from the state the
        r200+ corpus says is dead ("thrown, six rounds to live").
        """
        # MERGE: bits 10-27 of this slot are the collar's per-body ledger
        # (COLLAR_SPENT_SLOT, doctrine.py).  The heartbeat is round+1 <= 1001
        # and has always fitted in the low ten bits, so the mask is a no-op
        # with COLLAR_ON down and the whole field is zero there anyway.
        beat = ct.read_store(SLOT_RAID_LIVE) & COLLAR_BEAT_MASK
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
                if dsq_core(ct.get_position(), E) <= LOKI_ESTABLISH_DSQ:
                    self._raid_beat(ct, rnd, E)
            except Exception:
                pass
        if E is None or rnd < self.raid_pause_until:
            # STATE-BASED stand-down: with no anchor there is nothing to raid,
            # and a raider that cannot reach the ring is worth more on ore than
            # oscillating against a wall.
            self._expand(ct)
            return

        p = ct.get_position()
        # One distance to the enemy footprint, reused by the establishment
        # test and the approach test (LOKI computed it twice, each time
        # building four Position objects first).
        core_dsq = dsq_core(p, E)
        established = core_dsq <= LOKI_ESTABLISH_DSQ
        if established:
            # PLANK P3.  A raider at the ring is the body most likely to be able
            # to see their Core HP, and publishing it is what lets a tube-siting
            # raider five tiles out gate on it.  FIX B folded that publish INTO
            # the heartbeat -- one write, one writer, every round -- so the
            # separate `_sge_core_band` call that stood here is now made by
            # `_raid_beat` itself, before the word is assembled.
            # MERGE: PLANK P2's terminal surge reads the SAME field from the
            # SAME publisher, so either consumer's flag arms the publish.
            self._raid_beat(ct, rnd, E)
            if not SIEGE_BAND_SAFE_ON and self._sge_band_armed():
                # The pre-FIX-B publish, kept reachable so the fix is a flag
                # flip like every other plank in this tree and the control leg
                # of its own measurement is a stamped variant rather than a
                # hand edit: a SEPARATE, transition-latched slot-13 write, made
                # by established raiders only.
                self._sge_core_band(ct, E)
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

        near = established or core_dsq <= LOKI_APPROACH_DSQ

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

        # 0. PLANK P2 -- THE COLLAR.  Above the peck and above the parent's own
        # seal, because a held seat is worth more than two damage a round and
        # every round a seat is open is +4 HP per titanium back onto the Core we
        # are shooting.  Engaged only once the raid is established; out of
        # budget it declines and everything below this line is loki_turbo7's
        # ranking, untouched.
        if COLLAR_ON:
            rnd = ct.get_current_round()
            if self._collar_live(ct, E, p, rnd) and self._collar_act(ct, E, p, ti, rnd):
                return True

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
            for dx, dy in CARD_DELTAS:
                tx, ty = p.x + dx, p.y + dy
                if (tx, ty) not in seatkeys:
                    continue
                try:
                    t = Position(tx, ty)
                    if ct.can_build_barrier(t):
                        ct.build_barrier(t)
                        return True
                except Exception:
                    continue

        # 3. THE FORWARD SENTINEL.  Built on the approach, before the ring is
        # reached, because that is where the 5-tile band is.
        if self._try_forward_sentinel(ct, E):
            return True

        # 3b. THE NEST GUNNER (T5 plank G(a)).  Strictly after the pair, so it
        # can never be the reason the second tube was unaffordable.
        if self._t5_try_fwd_gunner(ct, E):
            return True

        # 3c. PLANK P3, THE SCREEN.  Same placement in the ranking and for the
        # same reason: it is tried only after the tube it exists to protect.
        if self._sge_screen(ct, E):
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
            for dx, dy in CARD_DELTAS:
                tx, ty = p.x + dx, p.y + dy
                if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                    continue
                t = Position(tx, ty)
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
            for dx, dy in CARD_DELTAS:
                tx, ty = p.x + dx, p.y + dy
                if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                    continue
                t = Position(tx, ty)
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
        for dx, dy in CARD_DELTAS:
            tx, ty = p.x + dx, p.y + dy
            if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                continue
            t = Position(tx, ty)
            if not self._salt_forward(t, E):
                continue
            try:
                bid = ct.get_tile_building_id(t)
                if bid is None or ct.get_team(bid) == self.team:
                    continue
                et = ct.get_entity_type(bid)
            except Exception:
                continue
            if et in BELT_TYPES:
                marks[(tx, ty)] = rnd
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
            for dx, dy in CARD_DELTAS:
                k = (p.x + dx, p.y + dy)
                m = marks.get(k)
                if m is None or rnd - m > LOKI_SALT_MEMORY:
                    continue
                t = Position(k[0], k[1])
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
            for dx, dy in CARD_DELTAS:
                tx, ty = p.x + dx, p.y + dy
                if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                    continue
                t = Position(tx, ty)
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
        for dx, dy in CARD_DELTAS:
            qx, qy = t.x + dx, t.y + dy
            if not (0 <= qx < self.mw and 0 <= qy < self.mh):
                continue
            try:
                bid = ct.get_tile_building_id(Position(qx, qy))
                if bid is None or ct.get_team(bid) == self.team:
                    continue
                if ct.get_entity_type(bid) in BELT_TYPES:
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
        for dx, dy in CARD_DELTAS:
            tx, ty = p.x + dx, p.y + dy
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
            if et == EntityType.CORE:
                pr = 0
            elif (tx, ty) in seatkeys and et in BELT_TYPES:
                pr = 1
            elif et == EntityType.LAUNCHER:
                pr = 2
            elif et in TURRET_TYPES:
                pr = 3
            elif et == EntityType.HARVESTER:
                pr = 4
            elif et in BELT_TYPES:
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

    # --- LOKI-TURBO5: THE BATTERY ------------------------------------------

    def _t5_nest_sites(self, ct, E):
        """Ranked standoff (site, facing, core tile) triples, cached on the anchor.

        A Sentinel at S facing d covers S + d*1..5 cardinally and S + d*1..4
        diagonally (engine_mechanics.md D), so the site that hits Core tile C
        along d is exactly `C - d*k`.  Keeping k at the FAR end of the pattern
        is the whole of plank B's placement half: d^2 >= T5_STANDOFF_MIN_DSQ is
        outside the reach of a Gunner built on their own Core (r^2 = 13), and
        62 % of our forward turrets currently stand INSIDE that reach against
        the top-5's 33 % (resource_gap.md G3).

        Pure geometry plus one `can_fire_from` per surviving candidate -- the
        hypothetical-turret predicate, which by contract ignores ammo and
        cooldown, and which for a Sentinel ignores walls and occupancy too.  At
        most 4 core tiles x 8 facings x 2 ranks = 64 probes, once per anchor.
        """
        # The wall count is in the key because the terrain decode lands on a
        # builder's FIRST turn: a nest list computed before it would be a cache
        # of a blind guess held for the rest of the match.
        key = (E.x, E.y, len(self.map_walls))
        if self.t5_nest_key == key:
            return self.t5_nests
        self.t5_nest_key = key
        self.t5_nests = ()
        if not (self.mw and self.mh):
            return self.t5_nests
        walls = self.map_walls
        out = []
        seen = set()
        for c in core_tiles(E):
            for d in DIRECTIONS:
                dx, dy = DELTA[d]
                ranks = T5_NEST_CARD if (dx == 0 or dy == 0) else T5_NEST_DIAG
                for k in ranks:
                    sx, sy = c.x - dx * k, c.y - dy * k
                    if not (0 <= sx < self.mw and 0 <= sy < self.mh):
                        continue
                    if (sx, sy) in seen:
                        continue
                    if walls and (sx, sy) in walls:
                        continue
                    s = Position(sx, sy)
                    if dsq_core(s, E) < T5_STANDOFF_MIN_DSQ:
                        continue
                    try:
                        if not ct.can_fire_from(s, d, EntityType.SENTINEL, c):
                            continue
                    except Exception:
                        continue
                    seen.add((sx, sy))
                    out.append((s, d, c))
        if self.core is not None:
            # Nearer OUR Core first: a nest a raider cannot reach is a nest we
            # do not own.  (x, y) last so the order is identical on every unit.
            cx, cy = self.core.x, self.core.y
            out.sort(key=lambda t: (abs(t[0].x - cx) + abs(t[0].y - cy),
                                    t[0].x, t[0].y))
        self.t5_nests = tuple(out)
        return self.t5_nests

    def _t5_swept(self, ct):
        """Tiles a VISIBLE enemy turret's current facing already covers.

        A nest planted on someone's existing firing line is a nest that dies
        before its second shot; `get_attackable_tiles_from` is the same
        predicate LOKI-25 already uses to score raid stations down for Gunner
        axes.  Memoised on the round because two callers ask in one turn.
        """
        rnd = ct.get_current_round()
        if self.t5_swept_rnd == rnd:
            return self.t5_swept
        self.t5_swept_rnd = rnd
        out = set()
        try:
            for bid in ct.get_nearby_buildings():
                et = ct.get_entity_type(bid)
                if et not in TURRET_TYPES:
                    continue
                if ct.get_team(bid) == self.team:
                    continue
                for t in ct.get_attackable_tiles_from(
                        ct.get_position(bid), ct.get_direction(bid), et):
                    out.add((t.x, t.y))
        except Exception:
            pass
        self.t5_swept = frozenset(out)
        return self.t5_swept

    def _t5_nest_pick(self, ct, E, n):
        """The nest this raider should be planting, given `n` tubes already up.

        The picks are chosen TOGETHER, up front, so the pair is dispersed by
        construction: no two nests inside T5_NEST_MIN_SEP_DSQ of each other,
        which is the separation that stops one defensive Gunner answering both.
        Assignment is by the live census -- tube 0 takes pick 0, tube 1 pick 1 --
        so two raiders never contend for the same tile without the engine's own
        occupancy check settling it.
        """
        sites = self._t5_nest_sites(ct, E)
        if not sites:
            return None
        swept = self._t5_swept(ct) if T5_NEST_AXIS_PENALTY else frozenset()
        for avoid_swept in (True, False):
            picks = []
            for s, d, c in sites:
                if avoid_swept and (s.x, s.y) in swept:
                    continue
                ok = True
                for q, _qd, _qc in picks:
                    if s.distance_squared(q) < T5_NEST_MIN_SEP_DSQ:
                        ok = False
                        break
                if not ok:
                    continue
                picks.append((s, d, c))
                if len(picks) > n:
                    return picks[n]
            if not avoid_swept:
                # Fewer legal nests than tubes: reuse the last one rather than
                # refuse to build at all.
                return picks[-1] if picks else None
        return None

    def _t5_battery_gate(self, ct, n, cost, ti, ti_floor):
        """May a forward turret be bought this round?  (resource_gap.md change 1)

        NEVER ALONE.  With no tube standing the bank must cover TWO plus the
        magazine to feed them; that single test is also the "after a pair dies
        do not re-poke solo" rule, because a dead pair puts the live census
        back at zero and re-arms exactly this gate.  With one standing the
        second is the cheapest titanium on the board and is bought down to a
        token floor inside T5_PAIR_WINDOW rounds.  A third waits until the pair
        has actually STOOD for T5_TRIPLE_AFTER rounds -- if they are dying on
        arrival, a third body dies with them.
        """
        rnd = ct.get_current_round()
        # Slot 13 is the archetype detector's evidence slot whenever
        # T5_BATTERY_GATE_ON is off, which is how this file ships.  The flag
        # guard is a no-op in that case (this read returned 0 anyway) and it is
        # what makes the reclamation safe rather than lucky.
        raw = ct.read_store(SLOT_T5_BATT) if T5_BATTERY_GATE_ON else 0
        last = (raw - 1) if raw else None
        if n <= 0:
            if not T5_GATE_2X_ON:
                # FOLLOW-THROUGH ONLY.  The first tube is priced exactly as it
                # always was; the gate keeps only its second half, which makes
                # the SECOND tube nearly free for T5_PAIR_WINDOW rounds.  See
                # the verdict block: the 2x hold is a floor that is unmeetable
                # precisely when it binds, which is the third time this lineage
                # has measured that shape (GUARD_RESERVE_ON, POP_FLOOR_ON).
                return ti >= cost + ti_floor
            if ti < 2 * cost + ti_floor:
                return False
            ammo = ct.get_global_ammo()
            if ammo < T5_BATTERY_AMMO and (ti - 2 * cost) < (T5_BATTERY_AMMO - ammo):
                return False
            return True
        if n == 1:
            if last is not None and rnd - last <= T5_PAIR_WINDOW:
                return ti >= cost + T5_PAIR_TI_FLOOR
            return ti >= cost + ti_floor
        if last is None or rnd - last < T5_TRIPLE_AFTER:
            return False
        return ti >= cost + ti_floor + T5_TRIPLE_TI_FLOOR

    def _t5_note_fwd_build(self, ct, live):
        if LOKI2B_LIVE_CAP_ON:
            # Publish the live count INCLUDING the one just built, so a second
            # raider in the same round does not double-spend the cap before the
            # census refreshes next turn.
            ct.write_store(SLOT_FWD_GUN, (live or 0) + 1)
        else:
            ct.write_store(SLOT_FWD_GUN, ct.read_store(SLOT_FWD_GUN) + 1)
        if T5_BATTERY_GATE_ON:
            ct.write_store(SLOT_T5_BATT, ct.get_current_round() + 1)

    def _t5_fwd_sentinels(self, ct, E):
        """Live friendly Sentinels near the enemy Core, as positions."""
        out = []
        try:
            for bid in ct.get_nearby_buildings():
                if ct.get_entity_type(bid) != EntityType.SENTINEL:
                    continue
                if ct.get_team(bid) != self.team:
                    continue
                bp = ct.get_position(bid)
                if dsq_core(bp, E) <= LOKI2B_CENSUS_DSQ:
                    out.append(bp)
        except Exception:
            return out
        return out

    def _t5_try_fwd_gunner(self, ct, E):
        """A Gunner beside the nest, once the pair stands.  (change 3a)

        We have built ZERO gunners in every version ever deployed and fire 51
        shots a game against Pivot's 164 (resource_gap.md G2).  A Gunner is 20
        Ti base against the Sentinel's 30 and fires EVERY round against the
        Sentinel's every second, so beside a nest it covers precisely the
        reload round on which a counter-attacking builder walks in -- facing
        coreward, which is the only direction that walk can come from.
        """
        if not (T5_FWD_GUNNER_ON and T5_NEST_ON):
            return False
        sents = self._t5_fwd_sentinels(ct, E)
        if len(sents) < 2:
            return False
        cost = ct.get_gunner_cost()
        if ct.get_global_resources() < cost + T5_FWD_GUNNER_TI_FLOOR:
            return False
        n_gun = 0
        try:
            for bid in ct.get_nearby_buildings():
                if ct.get_entity_type(bid) != EntityType.GUNNER:
                    continue
                if ct.get_team(bid) != self.team:
                    continue
                if dsq_core(ct.get_position(bid), E) <= LOKI2B_CENSUS_DSQ:
                    n_gun += 1
        except Exception:
            return False
        if n_gun >= T5_FWD_GUNNER_CAP or n_gun >= len(sents):
            return False
        p = ct.get_position()
        for dx, dy in CARD_DELTAS:
            bx, by = p.x + dx, p.y + dy
            if not (0 <= bx < self.mw and 0 <= by < self.mh):
                continue
            bp = Position(bx, by)
            beside = False
            for s in sents:
                if bp.distance_squared(s) <= 2:
                    beside = True
                    break
            if not beside:
                continue
            facing = bp.direction_to(nearest_core_tile(bp, E))
            if facing == Direction.CENTRE:
                continue
            try:
                if not ct.can_build_gunner(bp, facing):
                    continue
            except Exception:
                continue
            ct.build_gunner(bp, facing)
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

        PLANK P3 SIEGE adds two things and removes none.  SIEGE_SITE_ON makes
        the post pass the measured band [2.5, 5.7] to the Core CENTRE and then
        RANKS the survivors instead of taking the first one the scan happens to
        reach; SIEGE_MASS_ON discounts the second and third tube.  With both
        flags off every branch below is the parent's, statement for statement.

        SIEGE_SITE_FALLBACK is what makes "adds two things and removes none"
        true of the SITING arm as well.  As first shipped the band was a
        `continue`, i.e. a VETO, and it cost 0.24 tubes a game against turbo4
        (doctrine.py, section 1b).  It is now a PREFERENCE: in-band posts are
        ranked and win outright, and only if NOT ONE in-band post is admissible
        does the parent's own first-come choice get built, logged `SGE
        fallback`.  builds(SITE on) >= builds(SITE off), always.
        """
        if not LOKI_FWD_SENTINEL_ON:
            return False
        rnd = ct.get_current_round()
        live = self._live_fwd_guns(ct, E) if LOKI2B_LIVE_CAP_ON else None
        n = live if live is not None else ct.read_store(SLOT_FWD_GUN)
        if SIEGE_MASS_ON:
            # The age clock for tube 2, per unit.  There is no free slot to
            # publish a build round in (see the SIEGE block in doctrine.py), so
            # each raider times the tube from when IT first saw one standing --
            # which for the raider that built it is the build round itself, and
            # for a late arrival is conservative in the safe direction.
            if n >= 1:
                if self.sge_fwd_since is None:
                    self.sge_fwd_since = rnd
            else:
                self.sge_fwd_since = None
        if n >= LOKI_FWD_GUN_CAP:
            return False
        rush = LOKI2_RUSH_ON and rnd < LOKI2_RUSH_RND
        min_harv = LOKI2_RUSH_MIN_HARV if rush else LOKI_FWD_MIN_HARV
        ti_floor = LOKI2_RUSH_TI_FLOOR if rush else LOKI_FWD_TI_FLOOR
        if ct.read_store(SLOT_HARVESTERS) < min_harv:
            return False
        cost = ct.get_sentinel_cost()
        ti = ct.get_global_resources()
        disc = 0
        # PLANK B, THE GATE.  With the battery gate on this REPLACES the bank
        # test rather than adding to it -- the gate's own arithmetic is
        # strictly tighter for the first tube and deliberately looser for the
        # second, which is the point of the pair.
        if T5_BATTERY_GATE_ON:
            if not self._t5_battery_gate(ct, n, cost, ti, ti_floor):
                return False
        else:
            # PLANK P3, MASSING.  A DISCOUNT, never a veto: the floor only ever
            # moves down, so this arm cannot refuse a tube the parent bought.
            # `disc` records whether it was BINDING -- i.e. whether the parent's
            # floor would have refused this tube -- so the replay marker
            # separates "the plank bought this" from "the plank watched".
            if SIEGE_MASS_ON and n >= 1 and self._sge_mass_ok(ct, E, n, rnd):
                if SIEGE_MASS_TI_FLOOR < ti_floor:
                    if ti < cost + ti_floor:
                        disc = 1
                    ti_floor = SIEGE_MASS_TI_FLOOR
            if ti < cost + ti_floor:
                return False
        p = ct.get_position()
        # A Sentinel reaches r^2 = 32; a build site is one step from here, so
        # anything past ~50 cannot possibly align and the scan is skipped.
        if dsq_core(p, E) > 50:
            return False
        if self._cpu_exhausted(ct):
            return False
        # PLANK B, THE PLACEMENT.  The assigned nest first: it was chosen up
        # front, in the standoff band, dispersed from its partner and off every
        # visible enemy firing line, and the only thing left to do is stand
        # beside it.
        nests = self._t5_nest_sites(ct, E) if T5_NEST_ON else ()
        if nests:
            pick = self._t5_nest_pick(ct, E, n)
            if pick is not None:
                s, d, _c = pick
                if abs(s.x - p.x) + abs(s.y - p.y) == 1:
                    try:
                        ok = ct.can_build_sentinel(s, d)
                    except Exception:
                        ok = False
                    if ok:
                        ct.build_sentinel(s, d)
                        self._t5_note_fwd_build(ct, live)
                        self._sge_note_build(ct, s, E, n, disc)
                        return True
        tiles = core_tiles(E)
        # PLANK P3, SITING.  `guns` is the visible enemy Gunner census, used as
        # a PREFERENCE below; empty (and unscanned) with the flag off.
        guns = self._sge_enemy_guns(ct) if SIEGE_SITE_ON else ()
        best = best_key = None
        # THE PARENT'S CHOICE, kept beside the ranked one.  `par` is the first
        # (post, facing) in CARD_DELTAS order that passes the parent's own two
        # tests and happens to be out of band -- which is exactly what the
        # parent would have built, because the parent takes the first
        # admissible post it reaches.  Built only if the ranked in-band search
        # comes back empty (SIEGE_SITE_FALLBACK, doctrine.py 1b).
        par = None
        for dx, dy in CARD_DELTAS:
            bx, by = p.x + dx, p.y + dy
            if not (0 <= bx < self.mw and 0 <= by < self.mh):
                continue
            bp = Position(bx, by)
            # The opportunistic fallback keeps the standoff band too, or it
            # would quietly re-create the 2.50-3.61 habit the nest exists to
            # break.  Waived only where the map offers no standoff site at all.
            if nests and dsq_core(bp, E) < T5_STANDOFF_MIN_DSQ:
                continue
            q4 = 0
            in_band = True
            if SIEGE_SITE_ON:
                # ERROR 1: 35.1 % of our sentinels stand where they can never
                # reach the Core and another 20.3 % in the 5.7-6.4 shell.  This
                # is that test, in exact integers -- see `sge_centre_q4`.
                q4 = sge_centre_q4(bp, E)
                in_band = SIEGE_BAND_MIN_Q4 <= q4 <= SIEGE_BAND_MAX_Q4
                if not in_band and (not SIEGE_SITE_FALLBACK or par is not None):
                    # Vetoed outright with the fallback down; and with it up,
                    # once the parent's first choice is in hand a second
                    # out-of-band post has nothing left to tell us.
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
                if not SIEGE_SITE_ON:
                    # The parent's first-come placement, untouched.  The marker
                    # call still runs so SIEGE_MASS_ON stays auditable when it
                    # is ablated on its own.
                    ct.build_sentinel(bp, facing)
                    self._t5_note_fwd_build(ct, live)
                    self._sge_note_build(ct, bp, E, n, disc)
                    return True
                if not in_band:
                    # Reached only with SIEGE_SITE_FALLBACK up.  Record and
                    # stop: this is the parent's pick, not a ranked candidate,
                    # and it loses to any in-band post found anywhere.
                    par = (bp, facing)
                    break
                # The score depends on the POST, not the facing, so the first
                # legal facing for this post settles it and the target loop
                # stops -- at most four posts x four Core tiles per attempt.
                exposed = 0
                for g in guns:
                    if bp.distance_squared(g) <= SIEGE_GUN_REACH_DSQ:
                        exposed = 1
                        break
                key = (exposed, abs(q4 - SIEGE_BAND_MID_Q4), bx, by)
                if best_key is None or key < best_key:
                    best, best_key = (bp, facing, q4), key
                break
        if best is not None:
            bp, facing, _q4 = best
            ct.build_sentinel(bp, facing)
            self._t5_note_fwd_build(ct, live)
            self._sge_note_build(ct, bp, E, n, disc)
            return True
        if par is not None:
            # NO in-band post was admissible and the parent would have built.
            # Build where it would have.  A tube in the 5.7-6.4 shell is a poor
            # tube; NO tube is worth 0.24 of one a game (doctrine.py 1b).
            bp, facing = par
            ct.build_sentinel(bp, facing)
            self._t5_note_fwd_build(ct, live)
            self._sge_note_build(ct, bp, E, n, disc, fallback=True)
            return True
        return False

    # --- PLANK P3 SIEGE ----------------------------------------------------

    def _sge_enemy_guns(self, ct):
        """Positions of VISIBLE enemy Gunners, memoised on the round.

        A Gunner on their Core reaches r^2 = 13 and fires every round; a
        Sentinel cannot rotate and cannot answer one.  Where the band offers a
        choice this is what decides it.  Only Gunners: a Sentinel of theirs
        reaches 32 and no post inside the band escapes that, so ranking on it
        would only add noise.
        """
        rnd = ct.get_current_round()
        if self.sge_gun_rnd == rnd:
            return self.sge_guns
        self.sge_gun_rnd = rnd
        out = []
        try:
            for bid in ct.get_nearby_buildings():
                if ct.get_entity_type(bid) != EntityType.GUNNER:
                    continue
                if ct.get_team(bid) == self.team:
                    continue
                out.append(ct.get_position(bid))
        except Exception:
            pass
        self.sge_guns = tuple(out)
        return self.sge_guns

    def _sge_note_build(self, ct, bp, E, n, disc, fallback=False):
        """Replay markers for a forward Sentinel.  Events only, never a stream.

        `n` is the live census BEFORE this build, so n == 1 means this is tube
        two.  `disc` is 1 when the MASS discount was BINDING -- the parent's
        bank floor would have refused this tube -- which is the difference
        between the plank buying a tube and the plank watching one go up.
        A game that fields the full battery logs four lines.

        `fallback` swaps `SGE site` for `SGE fallback`: same event, same one
        line per tube, but a tube the BAND would have refused and the parent
        bought.  Tubes built with the siting arm on are therefore
        `site + fallback`, and `fallback` alone is the size of the veto that
        section 1b of doctrine.py measured.
        """
        if not SIEGE_LOG_ON:
            return
        if SIEGE_SITE_ON:
            print("SGE %s (%d,%d) d=%.2f"
                  % ("fallback" if fallback else "site",
                     bp.x, bp.y, sge_centre_q4(bp, E) ** 0.5 / 2.0))
        if SIEGE_MASS_ON:
            if n == 1:
                print("SGE mass2 (%d,%d) disc=%d" % (bp.x, bp.y, disc))
            elif n == 2:
                print("SGE mass3 (%d,%d) disc=%d" % (bp.x, bp.y, disc))

    def _sge_mass_ok(self, ct, E, n, rnd):
        """May tube `n + 1` be bought at the discounted floor?

        Tube 2 on SURVIVORSHIP -- the first has stood SIEGE_MASS2_AGE rounds,
        so it is not being answered on arrival and a second body will not just
        die with it.  Tube 3 on the ASSAULT CLOCK -- their Core below
        SIEGE_MASS3_HP is the exact window we miss (23 % of our wins add a
        sentinel after 400 against 51 % of theirs) and the window in which the
        400->0 grind is worth 63 rounds of two tubes and a gunner.
        """
        if n == 1:
            since = self.sge_fwd_since
            return since is not None and rnd - since >= SIEGE_MASS2_AGE
        if n == 2:
            return self._sge_core_band(ct, E) == SIEGE_HP_LOW
        return False

    def _sge_band_read(self, ct):
        """The PUBLISHED band: the writer-safe copy first, the legacy one second.

        Slot 15 bits 28-29 are republished whole every round by `_raid_beat`,
        which is the only writer of that slot in the tree, so what is read there
        is at worst one round old.  Slot 13 bits 26-27 are the pre-FIX-B copy:
        still written on a transition by any body with eyes, still read here,
        but only when the safe copy says nobody has looked -- it is the field
        that loses its race with `_arch_note` and it is now a hint, not the
        source of truth (doctrine.py, section 2b).
        """
        band = SIEGE_HP_UNKNOWN
        try:
            if SIEGE_BAND_SAFE_ON:
                band = (ct.read_store(COLLAR_SPENT_SLOT)
                        >> SIEGE_BAND15_SHIFT) & SIEGE_HPBAND_MASK
            if band == SIEGE_HP_UNKNOWN:
                band = (ct.read_store(SLOT_ARCH_SEEN)
                        >> SIEGE_HPBAND_SHIFT) & SIEGE_HPBAND_MASK
        except Exception:
            band = SIEGE_HP_UNKNOWN
        return band

    def _sge_core_band(self, ct, E):
        """Enemy-Core HP band: own eyes first, the shared store second.

        A builder sees r^2 = 20, so the raider siting a tube at d = 5.5 cannot
        read the HP it is gating on; a raider parked on one of their heal seats
        can.

        FIX B, and the doc comment this replaces was the defect: publishing was
        one write per TRANSITION into slot 13, which `_arch_note` overwrites
        from a stale read every round against a busy opponent -- so the
        transition was simply lost, and lost until the next one.  The
        authoritative publish is now bits 28-29 of slot 15, made by `_raid_beat`
        (sole writer) every round, and the slot-13 write below is kept
        transition-latched purely for backward compatibility.  Every body that
        can SEE a Core tile now calls this every round, not just established
        raiders -- `main._builder` gates the wider call on builder vision.

        Two consumers ask the same yes/no question of it -- `_sge_mass_ok`
        (tube 3) and COLLAR_SURGE_ON -- so UNKNOWN and HIGH behave alike.  The
        third state is kept anyway because it costs nothing and it is what tells
        a decode "nobody ever looked" apart from "looked, and it was healthy".

        MEMOISED ON THE ROUND.  In the siege fork this ran once per established
        raider per round; the merge adds the collar's budget path, which asks
        the same question up to three more times in the same turn.  The vision
        scan and the publish therefore happen on the FIRST caller of the round
        and every later one reads the answer off the body.
        """
        rnd = ct.get_current_round()
        if self.sge_band_rnd == rnd:
            return self.sge_band_val
        self.sge_band_rnd = rnd
        band = SIEGE_HP_UNKNOWN
        try:
            for c in core_tiles(E):
                if not ct.is_in_vision(c):
                    continue
                bid = ct.get_tile_building_id(c)
                if bid is None or ct.get_team(bid) == self.team:
                    continue
                if ct.get_entity_type(bid) != EntityType.CORE:
                    continue
                band = (SIEGE_HP_LOW if ct.get_hp(bid) < SIEGE_MASS3_HP
                        else SIEGE_HP_HIGH)
                break
        except Exception:
            band = SIEGE_HP_UNKNOWN
        if band != SIEGE_HP_UNKNOWN:
            # Published in BOTH directions -- HIGH as well as LOW.  A latch that
            # only ever set LOW would leave every blind raider surging on a Core
            # their teammate had watched heal back to 900.
            #
            # THE LEGACY COPY, unchanged and deliberately still transition-only.
            # Slot 13's real writer is `_arch_note`, and a per-round band write
            # built from a stale read would stomp the DETECTOR's fresh evidence
            # every round -- the same race, aimed the other way.  The copy that
            # has to survive is the one `_raid_beat` publishes into slot 15.
            try:
                v = ct.read_store(SLOT_ARCH_SEEN)
                nv = ((v & ~(SIEGE_HPBAND_MASK << SIEGE_HPBAND_SHIFT))
                      | (band << SIEGE_HPBAND_SHIFT))
                if nv != v:
                    ct.write_store(SLOT_ARCH_SEEN, nv)
            except Exception:
                pass
            self.sge_band_val = band
            return band
        band = self._sge_band_read(ct)
        self.sge_band_val = band
        return band

    def _sge_screen(self, ct, E):
        """ONE forward Gunner behind the forward Sentinel(s).  (SCREEN_ON)

        Their core-hitting sentinels survive to the end 74 % of the time and
        ours 45 %, and the visible difference at the moment of their kill is
        one gunner inside 6 tiles.  A builder cannot be touched by a builder --
        `can_fire` is False on a bot -- so a turret is the ONLY answer to the
        defender walking out to peck our tube.

        Refused unless the ray verifiably covers a peck seat of the sentinel
        and verifiably does NOT cover the sentinel itself: a Gunner ray stops
        at the nearest occupant and buildings block, so the naive "directly
        behind, facing their Core" post is a gun aimed into its own wall.
        """
        if not SCREEN_ON or self.sge_screen_done:
            return False
        # The two GLOBAL reads first: this runs in every raider's action phase
        # for the whole match, and the two building scans below are the only
        # expensive things in it.
        cost = ct.get_gunner_cost()
        if ct.get_global_resources() < cost + SCREEN_TI_FLOOR:
            return False
        if dsq_core(ct.get_position(), E) > LOKI2B_CENSUS_DSQ:
            return False
        rnd = ct.get_current_round()
        if rnd - self.sge_screen_rnd < SCREEN_TRY_EVERY:
            return False
        self.sge_screen_rnd = rnd
        sents = self._t5_fwd_sentinels(ct, E)
        if not sents:
            return False
        n_gun = 0
        try:
            for bid in ct.get_nearby_buildings():
                if ct.get_entity_type(bid) != EntityType.GUNNER:
                    continue
                if ct.get_team(bid) != self.team:
                    continue
                if dsq_core(ct.get_position(bid), E) <= LOKI2B_CENSUS_DSQ:
                    n_gun += 1
        except Exception:
            return False
        if n_gun >= SCREEN_CAP:
            # Someone already screens this battery; latch off for this life.
            self.sge_screen_done = True
            return False
        if self._cpu_exhausted(ct):
            return False
        p = ct.get_position()
        for dx, dy in CARD_DELTAS:
            bx, by = p.x + dx, p.y + dy
            if not (0 <= bx < self.mw and 0 <= by < self.mh):
                continue
            bp = Position(bx, by)
            bd = dsq_core(bp, E)
            s, skey = None, None
            for q in sents:
                d = bp.distance_squared(q)
                if d < SCREEN_MIN_DSQ or d > SCREEN_MAX_DSQ:
                    continue
                if bd <= dsq_core(q, E):
                    continue        # not BEHIND it: that is their side
                if skey is None or d < skey:
                    s, skey = q, d
            if s is None:
                continue
            seats = frozenset(((s.x + 1, s.y), (s.x - 1, s.y),
                               (s.x, s.y + 1), (s.x, s.y - 1)))
            # The defender walks in from their Core, so that facing is tried
            # first and the rest only as a fallback.
            dirs = []
            try:
                d0 = bp.direction_to(nearest_core_tile(bp, E))
                if d0 != Direction.CENTRE:
                    dirs.append(d0)
            except Exception:
                pass
            for d in DIRECTIONS:
                if d not in dirs:
                    dirs.append(d)
            for d in dirs:
                try:
                    ray = ct.get_attackable_tiles_from(bp, d, EntityType.GUNNER)
                except Exception:
                    continue
                covers, blocked = False, False
                for t in ray:
                    if t.x == s.x and t.y == s.y:
                        blocked = True
                        break
                    if (t.x, t.y) in seats:
                        covers = True
                if blocked or not covers:
                    continue
                try:
                    if not ct.can_build_gunner(bp, d):
                        continue
                except Exception:
                    continue
                ct.build_gunner(bp, d)
                self.sge_screen_done = True
                if SIEGE_LOG_ON:
                    print("SGE screen (%d,%d)" % (bp.x, bp.y))
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
            if dsq_core(p, E) > LOKI2B_CENSUS_DSQ * 2:
                return None
            me = ct.get_team()
            n = 0
            for eid in ct.get_nearby_buildings():
                if ct.get_entity_type(eid) != EntityType.SENTINEL:
                    continue
                if ct.get_team(eid) != me:
                    continue
                if dsq_core(ct.get_position(eid), E) <= LOKI2B_CENSUS_DSQ:
                    n += 1
            return n
        except Exception:
            return None

    def _t5_nest_walk_target(self, ct, E):
        """A tile orthogonally adjacent to this raider's assigned nest, or None.

        A Sentinel is built on a tile ORTHOGONALLY ADJACENT to the builder, so
        owning a standoff site means standing next to it.  Refused whenever the
        battery is not the thing to be doing: outside the neighbourhood, over
        the cap, or with no titanium the gate would release.
        """
        if not (T5_NEST_ON and T5_NEST_WALK_ON):
            return None
        p = ct.get_position()
        if dsq_core(p, E) > T5_NEST_APPROACH_DSQ:
            return None
        live = self._live_fwd_guns(ct, E) if LOKI2B_LIVE_CAP_ON else None
        n = live if live is not None else ct.read_store(SLOT_FWD_GUN)
        if n >= LOKI_FWD_GUN_CAP:
            return None
        cost = ct.get_sentinel_cost()
        ti = ct.get_global_resources()
        ti_floor = LOKI_FWD_TI_FLOOR
        if T5_BATTERY_GATE_ON:
            # Walk on the gate's own arithmetic, not on a guess: a raider that
            # walks to a nest the gate will refuse has left the collar for
            # nothing.  One cheap allowance -- the walk opens at HALF the
            # opening bank, because the walk itself takes rounds the harvesters
            # are still earning through.
            if n <= 0:
                need = 2 * cost + ti_floor if T5_GATE_2X_ON else cost + ti_floor
                if ti * 2 < need:
                    return None
            if n > 0 and not self._t5_battery_gate(ct, n, cost, ti, ti_floor):
                return None
        elif ti < cost + ti_floor:
            return None
        pick = self._t5_nest_pick(ct, E, n)
        if pick is None:
            return None
        s, d, _c = pick
        if abs(s.x - p.x) + abs(s.y - p.y) == 1:
            # Already in place; hold here so `_raid_act` can lay the tube.
            return p
        try:
            if not ct.is_tile_passable(s) and not ct.can_build_sentinel(s, d):
                # Something already stands on the nest -- ours or theirs.
                if ct.is_in_vision(s):
                    return None
        except Exception:
            pass
        best, best_key = None, None
        for dx, dy in CARD_DELTAS:
            tx, ty = s.x + dx, s.y + dy
            if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                continue
            if (tx, ty) in self.map_walls:
                continue
            key = (abs(tx - p.x) + abs(ty - p.y), tx, ty)
            if best_key is None or key < best_key:
                best, best_key = Position(tx, ty), key
        return best

    # --- PLANK P2: THE COLLAR ----------------------------------------------
    # Spec: analysis/leap_design.md P2; constants and the full rationale in the
    # COLLAR block at the end of doctrine.py.  Three behaviours, one flag:
    # RESEAL/TEND/BRICK claims the action at the top of _raid_act, corners that
    # carry our bricks become TEND stations instead of finished ones, and the
    # whole thing runs out of one shared titanium budget.

    def _collar_live(self, ct, E, p, rnd):
        """Is the raid ESTABLISHED, so this body belongs to the collar?

        No new state machine: these are the raid layer's own establishment
        signals.  This body inside LOKI_ESTABLISH_DSQ is the "raider within ~6
        of their Core" of the design; the heartbeat is a teammate holding the
        ring; SLOT_FWD_GUN is the forward Sentinel whose damage the collar
        exists to make permanent.
        """
        if not COLLAR_ON:
            return False
        try:
            if dsq_core(p, E) <= COLLAR_ENGAGE_DSQ:
                return True
            if self._foothold_live(ct, rnd):
                return True
            return ct.read_store(SLOT_FWD_GUN) > 0
        except Exception:
            return False

    def _collar_squat(self, ct):
        """MACRO / MACRO_WEAK: their bodies cannot shoot ours, so seats are free.

        READ-ONLY on slot 9 -- only the Core writes the classification.  Both
        codes, because the detector puts I Stone in MACRO_WEAK 4/5 and never in
        MACRO (S3 blocks it: 36 builders means someone is always within d<=8).
        """
        if not (COLLAR_ON and COLLAR_SQUAT_ON):
            return False
        try:
            a = self._archetype(ct)
        except Exception:
            return False
        return a == ARCH_MACRO or a == ARCH_MACRO_WEAK

    def _collar_spent(self, ct):
        """Titanium the whole collar has been charged, as far as this body can tell.

        Its OWN lane is read off `self.col_spent`, which is exact and current;
        the other lanes come out of slot 15 and are at most one round stale,
        which is what COLLAR_RACE_MARGIN is reserved against.  See the
        "WHERE THE COUNTER LIVES" block in doctrine.py for why this is a sum of
        per-body ledgers rather than one shared total.
        """
        total = self.col_spent
        if not COLLAR_BUDGET_SHARED:
            return total
        try:
            v = ct.read_store(COLLAR_SPENT_SLOT)
        except Exception:
            return total
        mine = self.raid_slot % COLLAR_LANES
        for k in range(COLLAR_LANES):
            if k == mine:
                continue
            total += (v >> (COLLAR_LANE_SHIFT + COLLAR_LANE_BITS * k)) & COLLAR_LANE_MASK
        return total

    def _collar_budget(self, ct, E):
        """The cap in force this round: doubled inside the terminal window.

        COLLAR_SURGE_ON, doctrine.py.  The window is the SAME signal, from the
        SAME source, that SIEGE_MASS_ON's third tube gates on -- so the damage
        and the denial peak together, which is the whole point of merging them.
        """
        if COLLAR_SURGE_ON and self._collar_surge(ct, E):
            return COLLAR_TI_BUDGET * COLLAR_SURGE_MULT
        return COLLAR_TI_BUDGET

    def _collar_surge(self, ct, E):
        """Is the enemy Core inside the terminal window (< SIEGE_MASS3_HP)?

        Marked on the EDGE, not per round: this is asked several times a turn
        by `_collar_afford` and the answer only ever changes when the band
        does.  Without the marker the surge is the one arm of the merge with no
        replay evidence at all, which is how FIX B's defect survived (the band
        was not landing and nothing said so).
        """
        if not COLLAR_SURGE_ON:
            return False
        try:
            on = self._sge_core_band(ct, E) == SIEGE_HP_LOW
        except Exception:
            return False
        if on != self.col_surge_in:
            self.col_surge_in = on
            if COLLAR_LOG_ON:
                print("COL surge %s r=%d" % ("on" if on else "off",
                                             ct.get_current_round()))
        return on

    def _collar_afford(self, ct, E, cost):
        """May this body spend `cost` on the collar THIS round?

        PESSIMISTIC RESERVATION, and this is the collar fork's one measured
        defect (results/leap/loki_collar.md: mean 13.5 / MAX 46 titanium a game
        against a 40 cap).  Store writes are buffered one round, so two raiders
        spending in the same round both read last round's total and one update
        is lost -- the counter reads at or below the truth, always.  A body that
        cannot CONFIRM headroom at (observed + COLLAR_RACE_MARGIN) declines, so
        the failure is a brick not laid rather than a cap sailed past.
        """
        return (self._collar_spent(ct) + COLLAR_RACE_MARGIN + cost
                <= self._collar_budget(ct, E))

    def _collar_spend(self, ct, amount):
        """Charge the collar budget.  Local and exact; published by `_raid_beat`.

        There is deliberately no store write here.  The ledger is this body's
        own running total and it is republished, whole, at the top of every one
        of this body's raid turns -- so nothing has to survive a concurrent
        writer, only be re-stated.  Teammates therefore see this spend one round
        late, which is the entire job of COLLAR_RACE_MARGIN.
        """
        self.col_spent += amount

    def _collar_denied(self, ct, extra=None):
        """Enemy heal seats denied right now, as far as THIS body can see.

        A building of either team on a seat denies it (a builder cannot stand
        on an occupied tile, so their own delivery conveyor costs them a heal
        seat too -- measured, probe Q2.1).  One of OUR bodies denies it while
        it stands there.  One of THEIRS does not: they can heal from under it.
        `extra` is the tile just built on, counted unconditionally so the
        number does not depend on when the engine makes a fresh building
        visible.
        """
        n = 0
        for s in self.raid_seats:
            if extra is not None and s.x == extra.x and s.y == extra.y:
                n += 1
                continue
            try:
                if not ct.is_in_vision(s):
                    continue
                if ct.get_tile_building_id(s) is not None:
                    n += 1
                    continue
                bid = ct.get_tile_builder_bot_id(s)
                if bid is not None and ct.get_team(bid) == self.team:
                    n += 1
            except Exception:
                continue
        return n

    def _collar_log(self, kind, t, rnd):
        """De-duplicate a marker: transitions and re-entries only, never rounds."""
        if not COLLAR_LOG_ON:
            return False
        key = (kind, t.x, t.y)
        last = self.col_log.get(key)
        if last is not None and rnd - last < COLLAR_LOG_GAP:
            return False
        self.col_log[key] = rnd
        return True

    def _collar_heal(self, ct, t, rnd):
        """+4 HP for 1 Ti against their 2 dmg for 2 Ti -- the 4:1 exchange."""
        try:
            if not ct.can_heal(t):
                return False
            ct.heal(t)
        except Exception:
            return False
        self._collar_spend(ct, 1)
        if self._collar_log("tend", t, rnd):
            print("COL tend (%d,%d)" % (t.x, t.y))
        return True

    def _collar_act(self, ct, E, p, ti, rnd):
        """RESEAL / TEND / BRICK / squat-support, ranked.  True = action spent.

        One pass over the four cardinals classifies every adjacent SEAT, then
        the ladder picks.  A corner is orthogonally adjacent to exactly two
        seats, which is why a corner is the tender's post: heal is d^2 == 1, so
        there is no diagonal way to cover a brick.

        MERGE (loki_leap): every arm is now gated on `_collar_afford` with ITS
        OWN cost rather than on one budget test at the top, because the fork's
        single test could pass on a 1-Ti reading and then spend 5 on a barrier.
        And inside the terminal window (COLLAR_SURGE_ON) ordinary TEND is
        promoted above BRICK -- breadth of denial while there is time, depth of
        it when there is not.
        """
        seatkeys = self.raid_seatkeys
        if not seatkeys:
            return False
        squat = self._collar_squat(ct)
        if squat and (p.x, p.y) in seatkeys and (p.x, p.y) not in self.col_squatted:
            # Bodily denial.  Unremovable while they have no turret, and it is
            # a spawn tile as well as a heal seat.  Announced above the budget
            # test because it costs nothing: the station is the seal.
            self.col_squatted.add((p.x, p.y))
            if COLLAR_LOG_ON:
                print("COL squat (%d,%d)" % (p.x, p.y))
        if not self._collar_afford(ct, E, 1):
            # Not even a heal fits under the reservation.  DECLINE the action
            # rather than suppress it: the parent's own seal and heal steps
            # still run below, so the floor of this plank is loki_turbo7 and
            # never less.
            return False
        surge = COLLAR_SURGE_ON and self._collar_surge(ct, E)
        free = []
        hurt = hurt_hp = None
        mate = mate_hp = None
        for dx, dy in CARD_DELTAS:
            tx, ty = p.x + dx, p.y + dy
            if (tx, ty) not in seatkeys:
                continue
            t = Position(tx, ty)
            try:
                bid = ct.get_tile_building_id(t)
            except Exception:
                continue
            if bid is None:
                # is_tile_empty() would say True here even with a bot standing
                # on the tile (measured, probe Q2.0), so the body test is
                # explicit and the build is gated on can_build_barrier below.
                try:
                    oid = ct.get_tile_builder_bot_id(t)
                except Exception:
                    oid = None
                if oid is None:
                    free.append(t)
                elif squat:
                    try:
                        if ct.get_team(oid) != self.team:
                            continue
                        hp, mx = ct.get_hp(oid), ct.get_max_hp(oid)
                    except Exception:
                        continue
                    if hp <= mx - COLLAR_SQUAT_HEAL_GAP and (mate_hp is None or hp < mate_hp):
                        mate, mate_hp = t, hp
                continue
            try:
                if ct.get_team(bid) != self.team:
                    continue            # their conveyor: denies the seat for us
                hp, mx = ct.get_hp(bid), ct.get_max_hp(bid)
            except Exception:
                continue
            # Ours.  Remember it, so a rebuild after it falls reads as a RESEAL
            # even when the body that laid it is long dead.  `mx` is read but
            # not compared: the gate is an absolute HP, because what matters is
            # how many more pecks the brick can take, not how dented it looks.
            self.col_bricks.add((tx, ty))
            if hp <= COLLAR_TEND_HP and (hurt_hp is None or hp < hurt_hp):
                hurt, hurt_hp = t, hp

        # 1. A BRICK ABOUT TO FALL outranks opening a new seat: the seat is
        # already ours and re-taking it costs a fresh barrier plus every heal
        # that lands through the gap.
        if hurt is not None and hurt_hp <= COLLAR_CRIT_HP and self._collar_heal(ct, hurt, rnd):
            return True

        # 1b. TERMINAL WINDOW: ordinary TEND jumps the brick.  Their Core is
        # under SIEGE_MASS3_HP and every round a seat we already own re-opens
        # is +4 HP per titanium straight back onto the thing our tubes are
        # shooting.  Holding it is 1 Ti; retaking it is a whole barrier.
        if surge and hurt is not None and self._collar_heal(ct, hurt, rnd):
            return True

        # 2. BRICK or RESEAL.  can_build_barrier is the whole occupancy gate:
        # a seat under any body, ours or theirs, is refused and simply polled
        # again next round -- vacancies are taken the round they appear, and
        # their Core re-spawning onto a seat costs them 36+ scaled titanium
        # against our 3.
        if (free and ti >= ct.get_barrier_cost() + LOKI_SEAL_TI_FLOOR
                and self._collar_afford(ct, E, ct.get_barrier_cost())):
            cost = ct.get_barrier_cost()
            for t in free:
                try:
                    if not ct.can_build_barrier(t):
                        continue
                    ct.build_barrier(t)
                except Exception:
                    continue
                self._collar_spend(ct, cost)
                key = (t.x, t.y)
                reseal = key in self.col_bricks
                self.col_bricks.add(key)
                if COLLAR_LOG_ON:
                    if reseal:
                        print("COL reseal (%d,%d)" % (t.x, t.y))
                    else:
                        print("COL brick (%d,%d) n=%d"
                              % (t.x, t.y, self._collar_denied(ct, t)))
                return True

        # 3. TEND.  Healing a brick beats rebuilding it 29-38 : 0.8 barriers
        # lost per 100 rounds (probe Q2.3).
        if hurt is not None and self._collar_heal(ct, hurt, rnd):
            return True

        # 4. SQUAT SUPPORT.  Two healers pinned a squatter at 33/40 for 28
        # consecutive gunner shots and the gunner ran out of ammo first.
        if mate is not None and self._collar_heal(ct, mate, rnd):
            return True
        return False

    def _collar_seats_by(self, ct, corner):
        """(seats still open, OUR bricks below COLLAR_TEND_HP) beside a corner.

        Same pessimism as `_open_seats_by`: a seat out of vision counts as
        OPEN, because walking to a corner that turns out to be finished costs
        one rescan and refusing to walk to one that is not costs the seal.  An
        undamaged brick counts as NEITHER -- it needs nothing, and a corner
        with only those is the parent's "finished" case.
        """
        open_n = 0
        hurt = 0
        for dx, dy in CARD_DELTAS:
            tx, ty = corner.x + dx, corner.y + dy
            if (tx, ty) not in self.raid_seatkeys:
                continue
            t = Position(tx, ty)
            try:
                if not ct.is_in_vision(t):
                    open_n += 1
                    continue
                bid = ct.get_tile_building_id(t)
                if bid is None:
                    open_n += 1
                elif ct.get_team(bid) == self.team and ct.get_hp(bid) <= COLLAR_TEND_HP:
                    hurt += 1
            except Exception:
                open_n += 1
        return open_n, hurt

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
        stations = self.raid_stations
        if not stations:
            return None
        # T5 NEST WALK.  Before the ring, the battery: a raider that never
        # walks to a standoff tile can only ever plant a Sentinel on whatever
        # tile the collar route happened to take it past, which is exactly how
        # 62 % of our forward turrets ended up inside a defensive Gunner's
        # reach (resource_gap.md G3).  It only engages once the raider is
        # already in the neighbourhood, so the long approach is untouched, and
        # it yields to the ring the moment the nest tile is no longer buildable.
        nest = self._t5_nest_walk_target(ct, E)
        if nest is not None:
            return nest
        if not near:
            return stations[self.raid_slot % len(stations)]
        if self.raid_station is not None and rnd < self.raid_rescan:
            return self.raid_station
        self.raid_rescan = rnd + LOKI_RAID_RESCAN

        p = ct.get_position()
        me = ct.get_id()
        # PLANK P2.  Which game the station scoring is playing, resolved once
        # per rescan rather than per candidate tile.
        collar = COLLAR_ON and self._collar_live(ct, E, p, rnd)
        squat = collar and self._collar_squat(ct)
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
                if collar:
                    # PLANK P2.  The parent's two cases are kept EXACTLY -- the
                    # +12 is what spreads the seal around the ring, and the
                    # first build of this plank lost two seats a game by
                    # replacing it (doctrine.py, the TENDING note).  The collar
                    # adds one case the parent does not have: a corner whose
                    # brick is under COLLAR_TEND_HP is a TEND station, and it
                    # outranks opening a new seat because a body is already
                    # invested in that seat and the alternative is losing it.
                    open_n, hurt_n = self._collar_seats_by(ct, s)
                    if hurt_n:
                        score -= COLLAR_TEND_BONUS
                    elif open_n:
                        score -= COLLAR_BRICK_BONUS
                        # SPREAD.  Every other term here is a distance, so all
                        # the bodies converge on the corners nearest the
                        # approach and the far side of the ring is never
                        # sealed at all (traced on antler: four seats free for
                        # the whole game).  One corner per raid slot, worth
                        # more than the walk, is the cheapest dispersion that
                        # reuses the seat issuer the raid already runs.
                        if COLLAR_SPREAD_ON and i == self.raid_slot % ncorner:
                            score -= COLLAR_SPREAD_BONUS
                    else:
                        score += 12
                elif self._open_seats_by(ct, s) == 0:
                    score += 12
                else:
                    score -= 6
            else:
                # A seat is a PECK station: two damage a round plus denial.
                score -= 3
                if squat:
                    # ...and against a turret-less opponent it is also a tile
                    # they can never take back, so the body itself is the seal.
                    score -= COLLAR_SQUAT_BONUS
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
        for dx, dy in CARD_DELTAS:
            tx, ty = corner.x + dx, corner.y + dy
            if (tx, ty) not in self.raid_seatkeys:
                continue
            t = Position(tx, ty)
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

        # Reachable throw sites: r^2 <= 26 from the launcher.  LOKI rebuilt
        # this ~81-Position list EVERY ROUND for the launcher's whole life
        # (loki_analysis.md 5.2) even on the rounds it threw nothing.  A
        # launcher is a building and never moves, so it is built once.
        skey = (lp, w, h)
        if self._launch_key != skey:
            sites = []
            for dx in range(-5, 6):
                for dy in range(-5, 6):
                    if dx * dx + dy * dy > 26:
                        continue
                    tx, ty = lp.x + dx, lp.y + dy
                    if 0 <= tx < w and 0 <= ty < h:
                        sites.append(Position(tx, ty))
            self._launch_sites = sites
            self._launch_key = skey
            self._launch_far_key = None
            self._launch_near_key = None
        sites = self._launch_sites

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
            # Same order as LOKI's per-intruder sort: sorted() is stable and
            # reverse=True keeps equal keys in their original order, so sorting
            # the identical list once gives the identical sequence.
            fkey = (lp, self.core)
            if self._launch_far_key != fkey:
                self._launch_far = sorted(
                    sites, key=lambda t: t.distance_squared(self.core), reverse=True)
                self._launch_far_key = fkey
            for site in self._launch_far:
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
        nkey = (lp, dest)
        if self._launch_near_key != nkey:
            self._launch_near = sorted(sites, key=lambda t: t.distance_squared(dest))
            self._launch_near_key = nkey
        near_first = self._launch_near
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
