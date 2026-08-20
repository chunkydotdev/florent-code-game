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
    core_corners, core_tiles, core_tiles_xy, dsq_core, enemy_core_for,
    heal_seats, nearest_core_tile, sge_centre_q4, unpack_pos,
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
            # PLANK CAGE.  ring12 == corners + seats, in that order, so an
            # index below len(corners) is a diagonal and everything above it is
            # a heal seat -- which is the only thing `_cg_seal` needs to tell
            # the ring8 subset apart from the whole.
            self.raid_ringkeys = frozenset(
                (t.x, t.y) for t in self.raid_stations)
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
        if TW_ON and TW_GUN_ON:
            # TERMINAL WEAPONS: bit 30, one bit above the band, on exactly the
            # same re-derive-or-republish discipline and for exactly the same
            # reason -- the consumer (the Core's ammunition JIT) can never see
            # the thing it has to budget for.  Contributes 0 with the flag down,
            # so the word written by the flag-off fork is bit-identical to
            # bots/loki_leap's.
            v |= self._tw_beat_gun(ct, E)
        if CAGE_ON and CAGE_BEFORE_SIEGE:
            # PLANK CAGE arm 3: bit 31, the top of the same word, on exactly
            # the same re-derive-or-republish discipline as the two fields
            # below it.  This method is the ONLY writer of slot 15 in the tree,
            # and that is the property which makes a shared latch survivable
            # here and did not make it survivable in slot 13 -- see the CAGE
            # block in doctrine.py for the game that measured the difference.
            v |= self._cg_beat_bit(ct, E, rnd)
        ct.write_store(COLLAR_SPENT_SLOT, v)

    def _sge_band_armed(self):
        """Does anything consume the enemy-Core HP band on this build?

        Two consumers: `_sge_mass_ok`'s third tube and the collar's terminal
        surge.  With both down nothing derives, publishes or reads the band, and
        slot 15 is the parent's plain heartbeat.

        WAVE 22 ARM A5 is a THIRD consumer: the endgame's stall clock reads the
        published band and nothing else, so the band must be derived and
        published for the trigger to exist at all.  A no-op on this carrier --
        `SIEGE_MASS_ON` is already True -- and it is here so that an unrelated
        ablation of the siege planks cannot silently starve the endgame.
        """
        return (SIEGE_MASS_ON or (COLLAR_ON and COLLAR_SURGE_ON)
                or (END_ON and END_BAND_ON))

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
        # WAVE 22 ARM A5, ARM 1 -- QUIT THE SIEGE, PERMANENTLY.  ABOVE the
        # heartbeat publish, and that placement is the whole hook: a quitting
        # body must stop asserting the foothold as well as stop working it, or
        # the cold-insert gate stays open for every teammate behind it.  One
        # test at the top of one method retires the entire forward tree --
        # forward sentinels, the screen gunner, the collar, the cage, the ferry
        # rungs, the launcher pluck -- without a flag apiece and without
        # touching a line of any of them.  Doctrine: the WAVE 22 TRACK 2 block
        # at the end of doctrine.py, sections 2(c) and 4.
        if END_ON and END_QUIT_ON and self._end_fired(ct):
            if self._end_come_home(ct, rnd):
                return
            self._expand(ct)
            return
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
        # WAVE 22, ARM A1 -- BAND A'S PAYLOAD SWITCH, and it is above every
        # other raid action because it is a five-round window: turrets are the
        # ONLY unit that can damage a builder (engine E), so a live sentinel
        # pair standing before their ferry converts is a mechanistic hard
        # counter to the whole cage doctrine, and it is the one thing in the
        # corpus with a winning record against the #1.  Refuses itself in one
        # boolean outside band A, outside r5-r7 and on every body that is not
        # one of the two lowest raid seats.
        if OPEN_ON and self._op_pair(ct, E, rnd):
            return
        # One distance to the enemy footprint, reused by the establishment
        # test and the approach test (LOKI computed it twice, each time
        # building four Position objects first).
        core_dsq = dsq_core(p, E)
        established = core_dsq <= LOKI_ESTABLISH_DSQ
        if SPR_ON and established:
            # WAVE 18: the arrival stamp, taken HERE and not in the ferry,
            # because a rider whose post succeeds on the arrival round returns
            # from `_cg_ferry_try` before its "there" refusal is ever reached
            # and would never stamp one.  A latch and a print; no decision.
            self._spr_arrive(ct, rnd)
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
            # PLANK CAGE.  The sequencing arm lives entirely here: an
            # established raider is the only body that can SEE the twelve
            # tiles, so it is the only body that can say whether the cage is
            # built.  Above every action, because holding fire is a decision
            # the forward Sentinels make three frames later off the store.
            if CAGE_ON:
                self._cg_tick(ct, E, rnd)
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
            # PLANK CAGE.  A jump TOWARD their Core is our own ferry landing,
            # not an exile: the wait is discharged and the body resumes at once
            # rather than standing three more rounds beside a launcher that is
            # five tiles behind it.
            self.cg_wait_until = 0
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

        # PLANK CAGE arm 1.  THE ONE ROUND THE RIDER MUST NOT WALK.  The
        # launcher was created after this body and therefore acts after it
        # every round; a rider that steps out of the r^2<=2 pickup disc before
        # the launcher's turn has bought a 20-Ti building for nothing.  Below
        # the action phase, so the wait costs no ACTION -- only the move.
        if (CAGE_ON and CAGE_FERRY and rnd < self.cg_wait_until
                and self._cg_ferry_wait(ct, p)):
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
        rnd = ct.get_current_round()
        self._ring(E)
        seatkeys = self.raid_seatkeys
        on_seat = (p.x, p.y) in seatkeys
        # PLANK CAGE arm 3.  Resolved ONCE per turn and consulted by two arms
        # below (the peck and the clear-the-way peck), because the answer is a
        # store read plus a heartbeat read and both are memoised on the round.
        # PLANK PAIRS arm 2 shares that moment -- the two gates are OR'd and the
        # Core is legal only when BOTH are open -- but it is NOT resolved here.
        # Its 30-round release clock is denominated in "rounds since this body
        # could have hit their Core", so it is asked lazily, by
        # `_hold_core_fire` at the two peck sites below, and a raider that never
        # reaches their footprint never starts one.
        hold = CAGE_ON and self._cg_hold(ct, rnd)

        # 0a. PLANK CAGE arm 1 -- THE FERRY.  Above everything, and it can only
        # fire while this body is still further than CAGE_FERRY_STOP_DSQ from
        # their footprint, so it competes with nothing at the ring: the arms
        # below are all destination work and this one is transport.  20 Ti buys
        # 5.7 tiles at once against a walk's 1.0 tile a round, and the scale it
        # costs comes back when the launcher disposes of itself.
        if CAGE_ON and CAGE_FERRY and self._cg_ferry_try(ct, E, p, ti, rnd):
            return True

        # 0. PLANK P2 -- THE COLLAR.  Above the peck and above the parent's own
        # seal, because a held seat is worth more than two damage a round and
        # every round a seat is open is +4 HP per titanium back onto the Core we
        # are shooting.  Engaged only once the raid is established; out of
        # budget it declines and everything below this line is loki_turbo7's
        # ranking, untouched.
        if COLLAR_ON:
            if self._collar_live(ct, E, p, rnd) and self._collar_act(ct, E, p, ti, rnd):
                return True

        # 1. STANDING ON A SEAT: peck the Core.  Two damage a round that the
        # collar makes permanent, plus the seat itself is denied by our body.
        # PLANK CAGE arm 3 WITHHOLDS IT while the cage is short of the gate --
        # this peck is very often the FIRST damage our side does to their Core,
        # and doing it 27 rounds before the seal exists is precisely the
        # ordering the corpus prices at -46 points of win rate.
        if (on_seat and ti >= LOKI_PECK_TI_FLOOR and not LOKI_QUIET_ON
                and not self._hold_core_fire(ct, rnd, hold)):
            for c in core_tiles(E):
                if abs(p.x - c.x) + abs(p.y - c.y) != 1:
                    continue
                try:
                    # WAVE 28, F6.
                    if ct.can_fire(c) and self._f6_ok(ct, c):
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

        # 3d. TERMINAL WEAPONS.  Below every tube arm above, on purpose: the
        # tube is the measured plank and the damage half of the inequality, and
        # both weapons here additionally hold the tube's own bank floor
        # (LOKI_FWD_TI_FLOOR), so neither can ever be the reason a Sentinel was
        # unaffordable.  W3 (the launcher, free per round) outranks W1 (the
        # gunner, 4 Ti/round of the ammunition H3 says we do not have): the
        # launcher denies 8 HP/round for nothing and the gunner denies ~4 for
        # a recurring bill, so the free one is bought first every time.
        if TW_ON:
            if self._tw_try_launcher(ct, E, p, ti, rnd):
                return True
            if self._tw_try_gunner(ct, E, p, ti, rnd):
                return True

        # 3e. PLANK FIN -- THE ESCORT PECK.  Two damage a round on their Core
        # for 2 Ti at zero cost scale, taken ONLY inside the seal window, where
        # their heal is ~0 and the damage is therefore permanent.  It sits here
        # -- below the collar, below the parent's seal, below every purchase --
        # because every one of those is worth more than 2 damage, and it
        # refuses again on its own account if a ring tile beside this body
        # needs a brick or a tend (`_fin_seal_pending`): SEAL INTEGRITY FIRST.
        if self._fin_peck(ct, E, p, ti, rnd):
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

        # 6. Otherwise clear whatever is in the way.  `hold` travels with it:
        # the Core is this peck's top priority and it is the same shot step 1
        # withholds, taken from a tile that is not a seat.
        if (ti >= LOKI_PECK_TI_FLOOR and not LOKI_QUIET_ON
                and self._raid_peck(ct, seatkeys, hold)):
            return True

        # 7. LOKI-48: SALT, AND ONLY ON A ROUND THE PARENT SPENT IDLE.
        # Last in the ACTION ranking, as in _v178salt -- and additionally
        # gated on the MOVE the parent would have made this round.  That
        # second gate is the whole arm; see _salt_idle_ok.
        if LOKI_SALTIDLE_ON and self._op_salt_ok(ct):
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

    def _op_salt_ok(self, ct):
        """WAVE 22, ARM A1: band A lays no barriers before r30 (F7.1)."""
        if not OPEN_ON:
            return True
        try:
            return self._op_cage_ok(ct, ct.get_current_round())
        except Exception:
            return True

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
                    # WAVE 28, F6.
                    if not self._f6_ok(ct, t):
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

    def _raid_peck(self, ct, seatkeys, hold=False):
        """Melee the best adjacent enemy building.  `hold` skips their Core.

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
                if self._hold_core_fire(ct, ct.get_current_round(), hold):
                    continue
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
            # WAVE 28, F6.
            if not self._f6_ok(ct, best):
                return False
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
            # WAVE 22 ARM A2.  This arm had no ray test at all -- it picked a
            # bearing and bought.  "Facing coreward" is a direction, not a
            # target.
            if not self._gd_gun_ok(ct, bp, facing):
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

        PLANK PAIRS hangs its own event off the same call, ABOVE the SIEGE_LOG
        guard so the two instruments stay independent flags: `PR pair` names the
        two tubes that now stand within 6 tiles of their Core, which is the
        exact quantity meta_pipeline_diff.md gap 2 splits on.
        """
        if PAIR_ON and PAIR_LOG and n >= 1:
            near = self._pr_near(ct, E, bp)
            if near:
                q = near[0]
                print("PR pair (%d,%d)+(%d,%d)" % (bp.x, bp.y, q.x, q.y))
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
            # PLANK PAIRS arm 1.  The 20-round survivorship wait is what makes
            # the solo tube solo; with PAIR_ON the discount arms the round tube
            # 1 is sited (PAIR_MASS2_AGE = 0).  Still a DISCOUNT and still
            # one-directional -- the floor only ever moves down -- so a looser
            # age here can never refuse a tube the parent would have bought.
            age = PAIR_MASS2_AGE if PAIR_ON else SIEGE_MASS2_AGE
            return since is not None and rnd - since >= age
        if n == 2:
            if self._sge_core_band(ct, E) == SIEGE_HP_LOW:
                return True
            # PLANK FIN (c).  THE WINDOW IS THE ASSAULT CLOCK.  The band turns
            # LOW only after the grind this plank exists to shorten; a sealed
            # ring is the same statement made 63 rounds earlier, and a sited
            # post left unbought while the seal holds is the trade wave 9 lost.
            return bool(FIN_ON and FIN_TUBE3_ON) and self._fin_live(ct, E, rnd)
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
                if not self._gd_gun_ok(ct, bp, d, ray):    # WAVE 22 ARM A2
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
        # WAVE 22, ARM A1.  Band A does not build the barrier cage before r30:
        # `rb30 <= 2` is the registered bar F7.1, and the band-A counter-book
        # is a live turret pair before their ferry lands, not a seal.  The cage
        # is a mid-to-long-map doctrine and a measured liability below the
        # boundary -- 49 % at c2c <= 12 against 88 % at 16-24, for the #1
        # itself (OPENING.md 1.2).
        if OPEN_ON and not self._op_cage_ok(ct, rnd):
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
        b = COLLAR_TI_BUDGET
        if (CAGE_ON and CAGE_SEAL and CAGE_SEAL_TI_BUDGET > b
                and self._cg_active(ct)):
            # PLANK CAGE arm 2.  The 32-Ti cap was written for a collar that
            # targets eight tiles and takes six of them; ring12 is twelve, our
            # bricks die at 41% against Jython's 7%, and the corpus reads
            # 10-11 sealed at 81% against 12/12 at 93%.  Twelve barriers is 36
            # Ti at the base price before a single reseal, so the cap and the
            # target set have to move together or the arm is a no-op.
            b = CAGE_SEAL_TI_BUDGET
        if COLLAR_SURGE_ON and self._collar_surge(ct, E):
            b *= COLLAR_SURGE_MULT
        if (TW_ON and TW_PLUCK_ON and TW_COLLAR_BONUS_ON
                and self._tw_launch_live(ct, E)):
            # THE RATCHET'S BILL.  A pluck makes a seat free the same round and
            # the collar's BRICK arm already takes free seats -- but a 32 Ti cap
            # written for 2.6 bricks a game cannot pay for a seat that reopens
            # every round the launcher throws.  The bonus is what turns a
            # temporary vacancy into a permanent one; without it the launcher
            # buys rounds and the collar cannot bank them.  Contributes 0 with
            # either flag down.
            b += TW_COLLAR_BONUS
        return b

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

        PLANK CAGE arm 2 widens the TARGET SET only: `keys` becomes all twelve
        ring tiles instead of the eight seats, and a diagonal corner is
        additionally gated on `_cg_corner_ok` (six seats held first, one corner
        kept free for the launcher).  Everything below -- the ranking, the
        per-arm affordability tests, the reseal memory -- is untouched, which
        is why the whole arm is a target set and a budget and not a rewrite.
        """
        seatkeys = self.raid_seatkeys
        if not seatkeys:
            return False
        cage = CAGE_ON and CAGE_SEAL and self._cg_active(ct)
        # PLANK RATCHET.  Resolved once per call: one memoised store read.
        # LEAP16 CONSOLIDATION, REMOVAL 3.  RAT_ON has been False since wave 12
        # (REFUTED, 2.9% handoff conversion) and this was the plank's one
        # UNCONDITIONAL call: every collar turn of every raider paid a call and
        # a store read for an arm that cannot fire.  The flag now short-circuits
        # it, exactly as the plank's other two call sites already did.
        rat = RAT_ON and self._rat_live(ct, rnd)
        keys = self.raid_ringkeys if cage else seatkeys
        corner_ok = self._cg_corner_ok(ct, E, rnd) if cage else False
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
            if (tx, ty) not in keys:
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
                    # PLANK CAGE, FINISHER GUARD (ii).  A diagonal is a SPAWN
                    # tile and nothing else; a seat is a HEAL tile.  Sealing
                    # spawn before heal is `eed95e8e_g3` -- 12/12 held for 228
                    # rounds at heal ratio 1.00, and lost.
                    if (cage and not corner_ok
                            and (tx, ty) not in seatkeys):
                        continue
                    free.append(t)
                else:
                    # PLANK RATCHET (3).  A SEAT UNDER ONE OF THEIRS is the
                    # tile wave 9 could never claim -- `can_build_barrier` is
                    # False on an occupied tile, so the collar was sealing the
                    # empty half of the ring and calling it a cage.  Remember
                    # it: when the launcher throws that body off, this arm's
                    # own poll takes the vacancy, and RAT_WATCH_RNDS is what
                    # tells a brick laid there from an ordinary one.
                    if rat and (tx, ty) in seatkeys and self._rat_theirs(ct, oid):
                        self.rat_watch[(tx, ty)] = rnd
                    if not squat:
                        continue
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
        cost0 = ct.get_barrier_cost()
        # PLANK RATCHET (3).  Tiles we watched one of THEIR bodies sit on
        # inside RAT_WATCH_RNDS: the eviction has landed and this is the round
        # it becomes permanent.  They go to the FRONT of the list, and the
        # collar's titanium budget -- written for a different arm, against a
        # ring that was free to begin with -- cannot refuse them.
        ratfree, ratkeys = (), None
        if rat and free and self.rat_watch:
            ratkeys = set()
            picked = []
            for t in free:
                k = (t.x, t.y)
                seen = self.rat_watch.get(k)
                if seen is not None and rnd - seen <= RAT_WATCH_RNDS:
                    ratkeys.add(k)
                    picked.append(t)
            ratfree = picked
            if not ratfree:
                ratkeys = None
        if (free and ti >= cost0 + LOKI_SEAL_TI_FLOOR
                and (self._collar_afford(ct, E, cost0)
                     or (RAT_BRICK_WAIVE and ratfree))):
            cost = cost0
            order = free
            if ratfree:
                rest = [t for t in free if (t.x, t.y) not in ratkeys]
                order = list(ratfree) + rest
            for t in order:
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
                if ratkeys is not None and key in ratkeys:
                    self.rat_n += 1
                    self.rat_watch.pop(key, None)
                    if RAT_LOG:
                        print("RAT brick (%d,%d)" % (t.x, t.y))
                        print("RAT ratchet n=%d" % self.rat_n)
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

        PLANK KEYSTONE (leap16).  A SEAT UNDER ONE OF THEIR BODIES IS NOT AN
        OPEN SEAT, and the whole plank is that sentence.  `get_tile_building_id`
        is None under a builder bot, so the incumbent counts such a seat as
        open, hands the corner beside it COLLAR_BRICK_BONUS, and PINS a body
        there -- waiting, every round, on a tile `can_build_barrier` will refuse
        for as long as their healer chooses to stand on it.  The measured cost
        is the whole of wave 19 track 2: over 120 decoded jython games our
        forward bodies were ever cardinally adjacent to a median of 3 of the 8
        seats, an empty buildable seat existed somewhere on their ring in 63.9 %
        of post-r50 rounds but was adjacent to a body in only 7.9 % of those,
        and the seal therefore plateaus at 4.87/8 while ~1.9 seats stay live
        under the heal line (tools/wave19_reach.py, tools/wave19_seatcensus.py).
        Discounting the blocked seat releases the body to a corner where a
        brick can actually be laid.  The seat is not abandoned: it is scored
        again at the next rescan, and the eviction arms above are what take it.
        """
        open_n = 0
        hurt = 0
        blocked = 0
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
                    if KC_ON:
                        # One extra tile read, on the OPEN seats only, at the
                        # rescan cadence -- at most two per corner per rescan.
                        oid = ct.get_tile_builder_bot_id(t)
                        if oid is not None and ct.get_team(oid) != self.team:
                            blocked += 1
                            continue
                    open_n += 1
                elif ct.get_team(bid) == self.team and ct.get_hp(bid) <= COLLAR_TEND_HP:
                    hurt += 1
            except Exception:
                open_n += 1
        if KC_LOG and blocked and open_n == 0 and hurt == 0:
            # The case the plank exists for, and the only one worth a line: a
            # corner whose every remaining seat is under one of their bodies.
            # Deduplicated per round per body -- `_raid_station` asks this once
            # per corner and there are four.
            rnd = ct.get_current_round()
            if self.kc_log != rnd:
                self.kc_log = rnd
                print("KC free (%d,%d) b=%d" % (corner.x, corner.y, blocked))
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
        # TERMINAL WEAPONS W3, and it sits here for the reason the nest walk
        # sits here: a building that can only be laid from one specific tile
        # needs a body ON that tile, and no amount of opportunism supplies one.
        # Below the nest because the nest is a tube and the tube is the damage.
        if TW_ON:
            tw = self._tw_launch_walk(ct, E)
            if tw is not None:
                return tw
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
        # PLANK RATCHET (2).  OUR launchers, gathered in the pass that is
        # already walking this list: a seat is only worth staging beside if a
        # launcher of ours can actually reach into it.
        # WAVE 11, FIX 3(c).  THE BONUS FOLLOWS THE EVICTOR, NOT THE CAP READ.
        # `ours_launch` below already requires one of OUR launchers within
        # d^2 <= 2 of the seat -- an eviction that is OBSERVED rather than
        # predicted -- and wave 10 measured the arm at 0.107 ratchets/game
        # because no launcher stood when it was wanted.  The pluck (arm 1) and
        # the budget waive (arm 3) keep `_rat_live`: those spend.  This one
        # only chooses where a body that was walking anyway stands.
        rat_stage = (RAT_ON and RAT_STAGE_ON and collar
                     and (RAT_STAGE_ANY_EVICTOR or self._rat_live(ct, rnd)))
        ours_launch = [] if rat_stage else None
        try:
            for bid in ct.get_nearby_buildings():
                if ct.get_team(bid) == self.team:
                    if (rat_stage
                            and ct.get_entity_type(bid) == EntityType.LAUNCHER):
                        ours_launch.append(ct.get_position(bid))
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
            if rat_stage and ours_launch and self._rat_stage_by(
                    ct, s, ours_launch):
                # PLANK RATCHET (2).  BE THERE BEFORE THE PLUCK.  Worth more
                # than COLLAR_TEND_BONUS: a tend holds a seat we already own,
                # this one takes a seat we have never been able to touch.
                score -= RAT_STAGE_BONUS
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
        if best is None and CAGE_ON:
            # PLANK CAGE arm 2, THE SUCCESS CASE.  A finished cage is twelve
            # impassable tiles, and OUR OWN bricks are impassable too -- so the
            # better the seal, the more certainly this loop returns nothing and
            # the raid walks at the anchor until `_raid` pauses it.  One tile
            # further out every ring tile is still orthogonally in reach, which
            # is all a reseal or a tend needs.
            best = self._cg_outer_station(ct, E, p, rnd)
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

    # --- TERMINAL WEAPONS (TW) ---------------------------------------------
    # Spec: analysis/heal_wall_diagnosis.md sections 3-4; constants and the
    # full rationale in the TERMINAL WEAPONS block at the end of doctrine.py.
    # Two buildings, one gate.  Neither buys damage; both buy SEATS, because
    # the wall's rate is 4 x manned seats and H3 prices the damage lever out.

    def _tw_turret_seen(self, ct):
        """Has this body ever seen an enemy turret?  Latches, never clears.

        The whole arithmetic of both weapons rests on "nothing they own can
        damage a building at range".  One enemy Gunner or Sentinel anywhere in
        this body's vision falsifies that, and a latch is the right shape
        because the evidence is a building: it does not walk away, the raider
        does.  Stricter than the diagnosis's "within d <= 8 of their Core" and
        deliberately so -- a raider IS at the ring, so its vision disc already
        covers that shell, and the extra reach only ever refuses.
        """
        if self.tw_turret:
            return True
        try:
            for bid in ct.get_nearby_buildings():
                if ct.get_entity_type(bid) not in TURRET_TYPES:
                    continue
                if ct.get_team(bid) == self.team:
                    continue
                self.tw_turret = True
                return True
        except Exception:
            return self.tw_turret
        return False

    def _tw_manned(self, ct):
        """Their bodies on THEIR eight heal seats, seen right now.

        The seat set is the raid layer's own (`_ring`), so this is eight
        `is_in_vision` probes from a body that is standing on the ring -- every
        seat of a 2x2 footprint is inside a builder's r^2 = 20 disc from any
        other ring tile (worst pair d^2 = 10).  The MAX is latched: the wall
        mans up when the Core is hurt and stays manned (H1), so a momentary dip
        while we are throwing bodies off it must not disarm the weapon that
        caused the dip.
        """
        n = 0
        for s in self.raid_seats:
            try:
                if not ct.is_in_vision(s):
                    continue
                bid = ct.get_tile_builder_bot_id(s)
                if bid is not None and ct.get_team(bid) != self.team:
                    n += 1
            except Exception:
                continue
        if n > self.tw_manned_max:
            self.tw_manned_max = n
        return n

    def _tw_gate(self, ct, E, p, rnd):
        """The six-term gate both weapons share.  Memoised on the round.

        Ordered cheapest-first: the round, then a store read, then the turret
        latch, then geometry, then the eight seat probes.  With TW_ON down the
        first line returns and nothing below it is ever evaluated -- which is
        what makes the flag-off fork bit-identical to bots/loki_leap.
        """
        if not TW_ON or E is None:
            return False
        if self.tw_gate_rnd == rnd:
            return self.tw_gate_val
        self.tw_gate_rnd = rnd
        self.tw_gate_val = False
        if rnd < TW_MIN_RND:
            return False
        try:
            a = self._archetype(ct)
        except Exception:
            return False
        if a != ARCH_MACRO and a != ARCH_MACRO_WEAK:
            return False
        if self._tw_turret_seen(ct):
            return False
        if dsq_core(p, E) > LOKI_ESTABLISH_DSQ:
            return False
        if not self._foothold_live(ct, rnd):
            return False
        seen = False
        for c in core_tiles(E):
            try:
                if ct.is_in_vision(c):
                    seen = True
                    break
            except Exception:
                continue
        if not seen:
            return False
        self._ring(E)
        m = self._tw_manned(ct)
        if self.tw_manned_max < TW_MIN_MANNED:
            return False
        self.tw_gate_val = True
        if TW_LOG_ON and not self.tw_gate_logged:
            self.tw_gate_logged = True
            print("TW gate r=%d m=%d" % (rnd, m))
        return True

    def _tw_census(self, ct, E):
        """(our launchers, our gunners) standing at THEIR ring, or (None, None).

        RE-DERIVED from vision every round, never accumulated -- so it needs no
        comm-store field at all and cannot go stale the way the collar's lane
        ledger can (DOCTRINE.md section 4).  None means "this body cannot see
        the ring", which every caller reads as a REFUSAL, not as a free cap.
        One scan serves both weapons, the collar's budget bonus and the
        heartbeat's gunner bit, so it is memoised on the round.
        """
        rnd = ct.get_current_round()
        if self.tw_cen_rnd == rnd:
            return self.tw_cen_val
        self.tw_cen_rnd = rnd
        self.tw_cen_val = (None, None)
        try:
            if dsq_core(ct.get_position(), E) > TW_CENSUS_DSQ * 2:
                return self.tw_cen_val
            nl = ng = 0
            for bid in ct.get_nearby_buildings():
                et = ct.get_entity_type(bid)
                if et != EntityType.LAUNCHER and et != EntityType.GUNNER:
                    continue
                if ct.get_team(bid) != self.team:
                    continue
                if dsq_core(ct.get_position(bid), E) > TW_CENSUS_DSQ:
                    continue
                if et == EntityType.LAUNCHER:
                    nl += 1
                else:
                    ng += 1
            self.tw_cen_val = (nl, ng)
        except Exception:
            self.tw_cen_val = (None, None)
        return self.tw_cen_val

    def _tw_beat_gun(self, ct, E):
        """Slot 15 bit 30: "a TW gunner stands at their ring", for the Core.

        Same discipline as the HP band two bits below it (FIX B): a body that
        can COUNT publishes what it counted, a body that cannot republishes
        what it read, so a blind raider is a no-op on the field rather than an
        eraser.  The Core cannot see a gunner five tiles from THEIR Core and
        `SLOT_HOME_GUN` is a home-band counter that this gunner must not be
        added to -- without this bit the JIT budgets 0 ammunition for it.
        """
        if not (TW_ON and TW_GUN_ON):
            return 0
        if E is not None:
            _nl, ng = self._tw_census(ct, E)
            if ng is not None:
                return TW_BEAT_GUN_BIT if ng > 0 else 0
        try:
            return ct.read_store(COLLAR_SPENT_SLOT) & TW_BEAT_GUN_BIT
        except Exception:
            return 0

    def _tw_launch_live(self, ct, E):
        """Does this body see one of our launchers at their ring?"""
        if not (TW_ON and TW_PLUCK_ON):
            return False
        nl, _ng = self._tw_census(ct, E)
        return bool(nl)

    def _tw_core_hp(self, ct, E):
        """Their Core's HP if a footprint tile is in vision, else None."""
        rnd = ct.get_current_round()
        if self.tw_hp_rnd == rnd:
            return self.tw_hp_val
        self.tw_hp_rnd = rnd
        self.tw_hp_val = None
        for c in core_tiles(E):
            try:
                if not ct.is_in_vision(c):
                    continue
                bid = ct.get_tile_building_id(c)
                if bid is None:
                    continue
                self.tw_hp_val = ct.get_hp(bid)
                break
            except Exception:
                continue
        return self.tw_hp_val

    def _tw_tubes(self, ct, E):
        """Forward Sentinels STANDING, or None if this body cannot count them.

        The live census first (`_live_fwd_guns`, which returns None rather than
        zero when blind) and the monotone store as the fallback -- exactly the
        two-step the gunner's TW_GUN_MIN_TUBES test already performs.
        """
        n = self._live_fwd_guns(ct, E) if LOKI2B_LIVE_CAP_ON else None
        if n is not None:
            return n
        try:
            return ct.read_store(SLOT_FWD_GUN)
        except Exception:
            return None

    def _tw_reserve(self, ct, E, rnd, ti, cost, burn_extra=0):
        """TW_RESERVE_ON -- the per-weapon reservation.  True = may be built.

        doctrine.py, TW_RESERVE_ON.  Section 12.6 measured the weapons being
        paid for out of the tubes (forward Sentinels at terminal 2.53 -> 2.17)
        and the bank floors the weapons hold could not have caught it: a floor
        prices a ONE-OFF and what a tube costs is a RECURRING 5 Ti/round of
        ammunition.  So the reservation is stated over a horizon.

        (a) TW_RESERVE_MIN_TUBES tubes standing -- the damage half of the
            inequality has to exist before we spend on the ceiling half.  A body
            that cannot count refuses: an unknown tube census must not read as
            "the reservation is satisfied".
        (b) the bank projected AFTER this purchase still covers what the JIT
            pipe must convert to keep those tubes firing TW_RESERVE_RNDS
            rounds.  Same arithmetic as `_sge_jit`'s burn term
            (SIEGE_JIT_SENT_BURN a round a firing Sentinel) at 1 Ti -> 1 ammo,
            with the magazine already standing credited against it, so a full
            magazine costs this gate nothing.  `burn_extra` is the weapon's OWN
            per-round consumption: TW_GUN_BURN for the gunner, zero for the
            launcher, which is the free-per-round distinction step 3d's ranking
            already makes, priced rather than merely ordered.

        WHO CALLS IT is the whole difference from wave 4, and it is decided by
        the CALLER, not here: launcher #1 never reaches this method, launcher
        #2 and the gunner always do.  See doctrine.py for the measurement that
        split them.

        Refusals are probe grade (`TW why w=tubes` / `w=pipe`, TW_LOG_WHY); the
        first RELEASE prints one line per body.
        """
        if not (TW_ON and TW_RESERVE_ON):
            return True
        tubes = self._tw_tubes(ct, E)
        if tubes is None or tubes < TW_RESERVE_MIN_TUBES:
            self._tw_why(ct, rnd, "tubes", ti, cost, -1 if tubes is None else tubes)
            return False
        if tubes > LOKI_FWD_GUN_CAP:
            tubes = LOKI_FWD_GUN_CAP
        need = TW_RESERVE_RNDS * (SIEGE_JIT_SENT_BURN * tubes + burn_extra)
        try:
            need -= ct.get_global_ammo()
        except Exception:
            return False
        if need < 0:
            need = 0
        if ti - cost < need:
            self._tw_why(ct, rnd, "pipe", ti, cost + need, tubes)
            return False
        if TW_LOG_ON and not self.tw_resv_logged:
            self.tw_resv_logged = True
            print("TW resv r=%d t=%d need=%d" % (rnd, tubes, need))
        return True

    def _tw_reserve_gated(self, n):
        """Does a launcher build at census `n` have to pass the reservation?

        `n` is the number of OUR launchers standing BEFORE this build, i.e. the
        same census the cap and the survivorship clock use, so build number
        n+1 is gated exactly when n >= TW_RESERVE_FREE_LAUNCHERS.  With the
        constant at 1: #1 (n=0) free, #2 (n=1) gated.
        """
        return bool(TW_ON and TW_RESERVE_ON and n >= TW_RESERVE_FREE_LAUNCHERS)

    def _tw_corner_keys(self, E):
        """{(x, y)} of the four ring corners, cached on the anchor."""
        key = (E.x, E.y)
        if self.tw_corner_key != key:
            self.tw_corner_key = key
            self.tw_corner_xy = frozenset(
                (c.x, c.y) for c in core_corners(E, self.mw, self.mh))
        return self.tw_corner_xy

    # --- W3: the launcher ---------------------------------------------------

    def _tw_try_launcher(self, ct, E, p, ti, rnd):
        """Plant a Launcher on one of THEIR ring corners.  True = action spent.

        A corner holds two of their heal seats inside the launcher's d^2 <= 2
        pickup disc and is not itself a seat, so it is outside
        `mimic_istones._fouled_seats` (which scans seats only) and it does not
        consume a tile a 3-Ti brick could have held.  -8 HP/round of their heal
        for ~20-30 Ti ONCE and zero per round, against a 4.9 Ti/round ammunition
        budget that buys 9 HP/round of damage.

        The cap is the LIVE CENSUS, so a launcher that dies is replaced and one
        that stands is never duplicated; a body that cannot see the ring refuses
        rather than guesses.  The second launcher waits TW_LAUNCH_AGE rounds of
        survivorship, exactly as the second tube does, and the third and fourth
        additionally require their Core to still be worth breaking.
        """
        if not (TW_ON and TW_PLUCK_ON):
            return False
        # PLANK CAGE arm 4.  EITHER gate opens the launcher: TW's six-term
        # defensive read, or the cage's four-term "a raider is established at
        # their ring by r20".  The gunner below keeps TW's gate alone.
        if not (self._tw_gate(ct, E, p, rnd) or self._cg_gate(ct, E, p, rnd)):
            return False
        # WAVE 11, FIX 3(b).  THE CAGE'S EVICTOR REGIME.  Inside it the cap is
        # CAGE_EVICT_CAP and the survivorship clock is CAGE_EVICT_AGE.  The
        # 20-round clock was written for a DEFENSIVE plucker bought late out of
        # a MACRO read -- "has the first one been answered yet" -- and against a
        # raid that establishes for a window it simply means the second evictor
        # is never sited at all: one launcher per game, two of eight seats
        # reachable, 0.107 ratchets/game (wave-10 verdict).
        cage_ev = self._cg_evict_live(ct, E, p, rnd)
        cap = CAGE_EVICT_CAP if cage_ev else TW_LAUNCH_CAP
        n, _ng = self._tw_census(ct, E)
        if n is None or n >= cap:
            self._tw_why(ct, rnd, "cap", 0, 0, -1 if n is None else n)
            return False
        # SURVIVORSHIP, per unit and per census level: the clock restarts every
        # time the number standing changes, so "the first has stood 20 rounds"
        # is asked of the launcher that is actually up rather than of a count.
        if self.tw_launch_n != n:
            self.tw_launch_n = n
            self.tw_launch_since = rnd
        age = CAGE_EVICT_AGE if cage_ev else TW_LAUNCH_AGE
        if n >= 1 and rnd - self.tw_launch_since < age:
            self._tw_why(ct, rnd, "age", ti, 0, n)
            return False
        if n >= 2:
            hp = self._tw_core_hp(ct, E)
            if hp is not None and hp <= TW_LAUNCH_HP_FLOOR:
                self._tw_why(ct, rnd, "hp", ti, 0, n)
                return False
        cost = ct.get_launcher_cost()
        if ti < cost + TW_LAUNCH_TI_FLOOR:
            self._tw_why(ct, rnd, "bank", ti, cost, n)
            return False
        # TW_RESERVE_ON (doctrine.py).  Launcher #1 does NOT reach this line:
        # it is the cheap half of the mechanism (a scaled one-off, zero per
        # round) and wave 4 measured that gating it is what emptied the fixture.
        # #2 does: it buys the same -8 HP/r for a second scaled price out of the
        # bank the tubes' ammunition comes from.  Last of the cheap refusals and
        # above the only expensive one, the corner scan below.  burn_extra = 0
        # -- a launcher costs nothing per round, which is the whole reason it
        # outranks the gunner in step 3d.
        # PLANK CAGE arm 3 WAIVES IT while the cage is short of its gate.  The
        # reservation asks for TW_RESERVE_MIN_TUBES forward Sentinels standing;
        # this plank's whole thesis is that the tubes come AFTER the cage, so
        # inside that window the reservation is a test the design guarantees
        # will fail.  It resumes the moment fire is opened.
        if (self._tw_reserve_gated(n) and not self._cg_hold(ct, rnd)
                and not self._tw_reserve(ct, E, rnd, ti, cost)):
            return False
        corners = self._tw_corner_keys(E)
        cands = []
        for dx, dy in CARD_DELTAS:
            tx, ty = p.x + dx, p.y + dy
            if (tx, ty) not in corners:
                continue
            cands.append(Position(tx, ty))
        # WAVE 11, FIX 3(b).  SPREAD.  A body standing between two free corners
        # takes the one FARTHEST from the evictors we already hold -- the four
        # corners cover four DISJOINT pairs of heal seats, so a second launcher
        # beside the first buys nothing the first did not already have.  With
        # nothing of ours at their ring every candidate ranks 0 and this is the
        # parent's cardinal order exactly.
        if len(cands) > 1 and cage_ev and CAGE_EVICT_SPREAD and n >= 1:
            dec = []
            for t in cands:
                d = self._cg_evict_far(ct, E, t)
                dec.append((-(d if d is not None else 0), t.x, t.y, t))
            dec.sort()
            cands = [r[3] for r in dec]
        for t in cands:
            try:
                if not ct.can_build_launcher(t):
                    continue
                ct.build_launcher(t)
            except Exception:
                continue
            self.cg_launch_n += 1   # WAVE 12: the ONE budget, all arms
            if TW_LOG_ON:
                print("TW launch (%d,%d) n=%d" % (t.x, t.y, n))
            if CAGE_LOG and cage_ev and n >= 1:
                print("CG evictor2 (%d,%d)" % (t.x, t.y))
            return True
        self._tw_why(ct, rnd, "site", ti, cost, n)
        return False

    def _tw_why(self, ct, rnd, why, ti, cost, n):
        """Probe-grade refusal marker for the launcher arm.  Off by default."""
        if not (TW_LOG_ON and TW_LOG_WHY):
            return
        if rnd - self.tw_why_rnd.get(why, -10 ** 9) < TW_WHY_GAP:
            return
        self.tw_why_rnd[why] = rnd
        print("TW why r=%d w=%s ti=%d c=%d n=%d" % (rnd, why, ti, cost, n))

    def _tw_launch_walk(self, ct, E):
        """A tile orthogonally adjacent to a FREE ring corner, or None.

        The launcher is built on a corner and a builder builds only on an
        ORTHOGONALLY adjacent tile -- but every corner is DIAGONAL to every
        other corner, so a raider parked on a corner (which is exactly where
        `_raid_station`'s COLLAR_BRICK_BONUS puts it) can never lay one.  This
        is the same walk-to `_t5_nest_walk_target` gives the Sentinel nest, on
        the same terms: it engages only when the purchase is actually available
        (gate open, under the cap, past the survivorship clock, bank in hand)
        and it yields the moment any of those stops being true, so it cannot
        park a body off the collar indefinitely.

        Refused pessimistically: a corner out of vision, holding a building of
        either team, or holding any body is not a site, and neither is the tile
        this body is standing on if that tile IS the corner.
        """
        if not (TW_ON and TW_PLUCK_ON and TW_LAUNCH_WALK_ON):
            return None
        p = ct.get_position()
        if dsq_core(p, E) > TW_LAUNCH_WALK_DSQ:
            return None
        rnd = ct.get_current_round()
        if not (self._tw_gate(ct, E, p, rnd) or self._cg_gate(ct, E, p, rnd)):
            return None
        # WAVE 11, FIX 3(b), mirrored from `_tw_try_launcher` for the reason the
        # docstring gives: this walk-to engages only while the purchase is
        # ACTUALLY available, so it has to ask the cap and the clock the same
        # way the purchase does or it parks a body off the collar for nothing.
        cage_ev = self._cg_evict_live(ct, E, p, rnd)
        cap = CAGE_EVICT_CAP if cage_ev else TW_LAUNCH_CAP
        n, _ng = self._tw_census(ct, E)
        if n is None or n >= cap:
            return None
        if self.tw_launch_n != n:
            self.tw_launch_n = n
            self.tw_launch_since = rnd
        age = CAGE_EVICT_AGE if cage_ev else TW_LAUNCH_AGE
        if n >= 1 and rnd - self.tw_launch_since < age:
            return None
        if n >= 2:
            hp = self._tw_core_hp(ct, E)
            if hp is not None and hp <= TW_LAUNCH_HP_FLOOR:
                return None
        ti = ct.get_global_resources()
        cost = ct.get_launcher_cost()
        if ti < cost + TW_LAUNCH_TI_FLOOR:
            return None
        # TW_RESERVE_ON, mirrored here for the reason the docstring gives: this
        # walk-to engages only while the purchase is ACTUALLY available, and a
        # purchase the reservation would refuse is not available.  Without this
        # line the raider would walk off the collar to a corner and then be
        # declined at step 3d every round it stood there.  Gated on the same
        # census, so the walk for launcher #1 is untouched, and waived inside
        # PLANK CAGE's pre-siege window for the reason given at the same line
        # in `_tw_try_launcher`.
        if (self._tw_reserve_gated(n) and not self._cg_hold(ct, rnd)
                and not self._tw_reserve(ct, E, rnd, ti, cost)):
            return None
        corners, _seats = self._ring(E)
        spread = cage_ev and CAGE_EVICT_SPREAD and n >= 1
        best, best_key = None, None
        for c in corners:
            try:
                if not ct.is_in_vision(c):
                    continue
                if ct.get_tile_building_id(c) is not None:
                    continue
                if ct.get_tile_builder_bot_id(c) is not None:
                    continue
            except Exception:
                continue
            # WAVE 11, FIX 3(b).  SPREAD, the walk-to half: the corner FARTHEST
            # from the evictor we already hold outranks the nearest free one,
            # because the nearest is usually the pair of seats that launcher
            # already covers.  Zero for every corner when we hold none, which
            # makes the key below the parent's key exactly.
            crank = 0
            if spread:
                d = self._cg_evict_far(ct, E, c)
                if d is not None:
                    crank = -d
            for dx, dy in CARD_DELTAS:
                tx, ty = c.x + dx, c.y + dy
                if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                    continue
                if (tx, ty) in self.map_walls:
                    continue
                if self.raid_ban.get((tx, ty), 0) > rnd:
                    continue
                # STANDING STILL IS A CANDIDATE, NOT AN EARLY RETURN.  The
                # parent returned `p` here the moment it found the body already
                # beside ANY free corner; with the spread rank that would pin
                # the second evictor onto the corner the first one covers.  It
                # is scored instead, at walk distance 0 -- which wins outright
                # whenever the rank is flat, i.e. in every case the parent had.
                cand = p if (tx == p.x and ty == p.y) else Position(tx, ty)
                key = (crank, abs(tx - p.x) + abs(ty - p.y), tx, ty)
                if best_key is None or key < best_key:
                    best, best_key = cand, key
        return best

    def _tw_throw_sites(self, ct, lp, E):
        """Every legal throw tile, FARTHEST from THEIR Core first.

        A launcher is a building and never moves, so the 88-tile disc and its
        ordering are built once per (launcher, anchor) pair and reused for the
        rest of the match -- the same fix `_launcher_turn` already applies to
        its own two orderings (loki_analysis.md 5.2).
        """
        w, h = self.mw, self.mh
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
            self.tw_far_key = None
        fkey = (lp, E)
        if self.tw_far_key != fkey:
            self.tw_far_key = fkey
            self.tw_far = sorted(self._launch_sites,
                                 key=lambda t: -dsq_core(t, E))
        return self.tw_far

    def _tw_launcher(self, ct, lp, E):
        """THE PLUCK.  One enemy body off the ring, every round, for 0 Ti.

        Pickup is team-blind (engine_mechanics F), and our own squatters sit on
        the two seats this corner covers -- so the team test below is the
        difference between a weapon and a self-inflicted exile.  A body
        standing on one of their seats is preferred over one merely passing:
        that is the body worth 4 HP/round to them.

        The landing tile is the farthest legal tile from THEIR Core, which is
        what converts one free action into several rounds of their walk-back
        (their bodies move one tile per round).  Two refusals: never inside
        TW_THROW_MIN_DSQ of their Core -- a free seat is a LEGAL throw target
        and dropping a warden from one seat onto another is a gift -- and never
        within TW_THROW_CLEAR_DSQ of one of our own buildings, because a warden
        dropped beside our forward Sentinel pecks it for the rest of the game.
        """
        if not (TW_ON and TW_PLUCK_ON):
            return
        try:
            if ct.get_action_cooldown() != 0:
                return
        except Exception:
            return
        self._ring(E)
        # PLANK CAGE arm 4.  The victim PREFERENCE widens from their eight heal
        # seats to all twelve ring tiles: a body on a diagonal is one move from
        # two seats and is standing on a tile their Core would otherwise spawn
        # onto, and the corpus prices the whole eviction at +22/+37 by driving
        # their seat occupancy to 0.09.  Nothing else about the pluck changes.
        seatkeys = (self.raid_ringkeys
                    if (CAGE_ON and CAGE_EVICT and self._cg_active(ct))
                    else self.raid_seatkeys)
        rnd0 = ct.get_current_round()
        # PLANK RATCHET (1).  THE PLUCK IS AIMED.  CAGE arm 4's widening made a
        # corner-squatter and a seated HEALER worth the same throw; inside the
        # ratchet a SEAT outranks a corner, and among seats the one one of our
        # bodies is already standing beside outranks the rest -- because that
        # is the seat that gets bricked the round it empties.  An eviction we
        # cannot follow with a brick is a shove, and they walk back.
        rat = (RAT_ON and RAT_SEAT_FIRST and self._rat_live(ct, rnd0))
        victim = vkey = vrank = None
        try:
            ents = ct.get_nearby_entities()
        except Exception:
            return
        for eid in ents:
            try:
                if ct.get_entity_type(eid) != EntityType.BUILDER_BOT:
                    continue
                if ct.get_team(eid) == self.team:
                    continue
                bp = ct.get_position(eid)
                d = bp.distance_squared(lp)
                if d > 2:
                    continue
            except Exception:
                continue
            if rat:
                if (bp.x, bp.y) in self.raid_seatkeys:
                    rank = 0 if self._rat_bricker_by(ct, bp) else 1
                else:
                    rank = 2
            else:
                rank = 0 if (bp.x, bp.y) in seatkeys else 1
            key = (rank, d, bp.x, bp.y)
            if vkey is None or key < vkey:
                victim, vkey, vrank = bp, key, rank
        if victim is None:
            # PLANK CAGE, THE TANGENTIAL HOP.  Nothing of theirs to evict this
            # round, so the free action goes to moving one of OURS around their
            # Core instead -- which is the arm the corpus says nobody but
            # Jython owns, and the reason `ph`'s launchers are worth nothing.
            self._cg_hop(ct, lp, E)
            return
        # Our own buildings near the drop zone, once per throw.  The launcher
        # sees r^2 = 26, which is exactly its own throw disc, so this list can
        # never miss a building a victim could be dropped beside.
        mine = []
        try:
            for bid in ct.get_nearby_buildings():
                if ct.get_team(bid) == self.team:
                    mine.append(ct.get_position(bid))
        except Exception:
            mine = []
        for site in self._tw_throw_sites(ct, lp, E):
            if dsq_core(site, E) < TW_THROW_MIN_DSQ:
                break               # sorted farthest-first: the rest are worse
            near_ours = False
            for m in mine:
                if site.distance_squared(m) <= TW_THROW_CLEAR_DSQ:
                    near_ours = True
                    break
            if near_ours:
                continue
            try:
                if not ct.can_launch(victim, site):
                    continue
                ct.launch(victim, site)
            except Exception:
                continue
            self.tw_plucks += 1
            rnd = rnd0
            if rat and RAT_LOG and vrank is not None and vrank <= 1:
                # PLANK RATCHET (1).  Every aimed eviction, because the arm's
                # whole measurement is a RATE against their seat occupancy.
                print("RAT pluck (%d,%d)" % (victim.x, victim.y))
            if CAGE_LOG and CAGE_ON and CAGE_EVICT:
                # Every eviction, not one per gap: this is the arm whose whole
                # measurement is a RATE (their seat occupancy per round), and
                # `tools/cage_mechanism.py` counts these lines.
                print("CG evict (%d,%d)->(%d,%d)"
                      % (victim.x, victim.y, site.x, site.y))
            if TW_LOG_ON and (TW_PLUCK_LOG_ALL
                              or rnd - self.tw_pluck_log >= TW_PLUCK_LOG_GAP):
                self.tw_pluck_log = rnd
                print("TW pluck (%d,%d)->(%d,%d) n=%d"
                      % (victim.x, victim.y, site.x, site.y, self.tw_plucks))
            return
        # In range but no legal landing tile for them -- the free action is
        # still worth a hop of ours.
        self._cg_hop(ct, lp, E)
        return

    # --- W1: the gunner -----------------------------------------------------

    def _tw_owned_at(self, ct, x, y):
        """Is one of OUR buildings or bodies standing on (x, y)?

        `_turret` refuses to fire on our own team, so a gunner whose FIRST ray
        tile holds one of ours is not a friendly-fire risk -- it is simply
        mute, for as long as that thing stands there.  Both our bricks and our
        squatters are permanent by design, so both disqualify a facing.
        """
        t = Position(x, y)
        try:
            bid = ct.get_tile_building_id(t)
            if bid is not None and ct.get_team(bid) == self.team:
                return True
            oid = ct.get_tile_builder_bot_id(t)
            return oid is not None and ct.get_team(oid) == self.team
        except Exception:
            return False

    def _tw_foe_at(self, ct, x, y):
        """Is one of THEIR builder bots standing on (x, y)?"""
        try:
            oid = ct.get_tile_builder_bot_id(Position(x, y))
            return oid is not None and ct.get_team(oid) != self.team
        except Exception:
            return False

    def _tw_try_gunner(self, ct, E, p, ti, rnd):
        """One Gunner at their ring, aimed down a manned side.  True = spent.

        The only unit we field that can REMOVE a body: a builder cannot fire on
        a builder (engine_mechanics E), so every other arm in this tree can
        only wait for a seat to be vacated.  7 damage a round kills a 40 HP
        warden in six; the ray resolves to the NEAREST occupant (D, N.3, N.8),
        which beside a manned wall is a seated healer.

        The ray is 3 tiles cardinal, 2 diagonal, and walls stop it.  A ring
        corner facing ALONG the ring covers the two seats on that side -- that
        is the 2-seat post the diagnosis asks for -- and the same corner facing
        the footprint diagonal puts a Core tile first with nothing able to
        stand between it and the barrel.  Ranked: bodies of theirs in the ray
        first (a post with no live target is a post that spends 10 Ti rotating
        later), then seats covered, then a Core tile, then the nearer post.
        """
        if not (TW_ON and TW_GUN_ON):
            return False
        if not self._tw_gate(ct, E, p, rnd):
            return False
        _nl, ng = self._tw_census(ct, E)
        if ng is None or ng >= TW_GUN_CAP:
            return False
        # NEVER BEFORE A TUBE.  This arm draws on the same starved conversion
        # budget the tubes do (H3), so it may not be the first thing bought at
        # the ring under any circumstances.
        tubes = self._live_fwd_guns(ct, E) if LOKI2B_LIVE_CAP_ON else None
        if tubes is None:
            try:
                tubes = ct.read_store(SLOT_FWD_GUN)
            except Exception:
                return False
        if tubes < TW_GUN_MIN_TUBES:
            return False
        cost = ct.get_gunner_cost()
        if ti < cost + TW_GUN_TI_FLOOR:
            return False
        # TW_RESERVE_ON (doctrine.py).  ALWAYS gated, and above the ray scan,
        # which is the expensive part of this arm.  The gunner is the other
        # half of the expensive pair: it pays a scaled one-off AND TW_GUN_BURN
        # a round of the same conversion budget the tubes draw on (H3), so its
        # own bill is reserved alongside theirs.  TW_GUN_MIN_TUBES asked whether
        # a tube EXISTS; this asks whether it will still be firing in ten rounds.
        if (TW_RESERVE_GUN
                and not self._tw_reserve(ct, E, rnd, ti, cost,
                                         burn_extra=TW_GUN_BURN)):
            return False
        seatkeys = self.raid_seatkeys
        corekeys = core_tiles_xy(E)
        best = best_key = None
        for dx, dy in CARD_DELTAS:
            bx, by = p.x + dx, p.y + dy
            if not (0 <= bx < self.mw and 0 <= by < self.mh):
                continue
            if (bx, by) in seatkeys:
                continue            # a seat is worth a brick, never a turret
            bp = Position(bx, by)
            bd = dsq_core(bp, E)
            if bd > TW_GUN_MAX_DSQ:
                continue
            for d in DIRECTIONS:
                ddx, ddy = DELTA[d]
                span = TW_GUN_RAY_CARD if (ddx == 0 or ddy == 0) else TW_GUN_RAY_DIAG
                seats = core = foes = 0
                mute = False
                aim = None
                for k in range(1, span + 1):
                    rx, ry = bx + ddx * k, by + ddy * k
                    if not (0 <= rx < self.mw and 0 <= ry < self.mh):
                        break
                    if (rx, ry) in self.map_walls:
                        break       # a gunner ray IS blocked by walls (D)
                    if self._tw_owned_at(ct, rx, ry):
                        if k == 1:
                            mute = True
                        break
                    if (rx, ry) in seatkeys:
                        seats += 1
                        if self._tw_foe_at(ct, rx, ry):
                            foes += 1
                            if aim is None:
                                aim = Position(rx, ry)
                    elif (rx, ry) in corekeys:
                        core = 1
                        if aim is None:
                            aim = Position(rx, ry)
                        break       # nothing behind a Core tile is reachable
                    elif self._tw_foe_at(ct, rx, ry):
                        foes += 1
                        if aim is None:
                            aim = Position(rx, ry)
                if mute or aim is None or (seats == 0 and core == 0):
                    continue
                # The engine's own predicate has the last word on the ray: it
                # knows the walls this body has not explored and the
                # nearest-occupant rule the geometry above only approximates.
                try:
                    if not ct.can_fire_from(bp, d, EntityType.GUNNER, aim):
                        continue
                    if not ct.can_build_gunner(bp, d):
                        continue
                except Exception:
                    continue
                if not self._gd_gun_ok(ct, bp, d):    # WAVE 22 ARM A2
                    continue
                key = (-foes, -seats, -core, bd, bx, by)
                if best_key is None or key < best_key:
                    best, best_key = (bp, d, seats), key
            # end facings
        if best is None:
            return False
        bp, d, seats = best
        try:
            ct.build_gunner(bp, d)
        except Exception:
            return False
        if TW_LOG_ON:
            ddx, ddy = DELTA[d]
            print("TW gun (%d,%d) f=%d,%d s=%d" % (bp.x, bp.y, ddx, ddy, seats))
        return True

    def _tw_note_gun_shot(self, ct, t, et):
        """`TW gunkill` -- a shot that takes an enemy builder bot to <= 0.

        Called from `_turret` BEFORE the shot, because after it the entity is
        gone and its HP is unreadable.  Gated on the gunner standing at THEIR
        ring so that a home gunner (CB / T5, both shipped off) could never
        borrow the marker.
        """
        if not (TW_ON and TW_GUN_ON and TW_LOG_ON):
            return
        if et != EntityType.BUILDER_BOT:
            return
        try:
            e = unpack_pos(ct.read_store(SLOT_ENEMY_CORE))
            if e is None or dsq_core(ct.get_position(), e) > TW_CENSUS_DSQ:
                return
            bid = ct.get_tile_builder_bot_id(t)
            if bid is None or ct.get_hp(bid) > TW_GUN_DMG:
                return
        except Exception:
            return
        print("TW gunkill (%d,%d)" % (t.x, t.y))

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
        if CAGE_ON and CAGE_FERRY and ct.get_current_round() < self.cg_wait_until:
            # PLANK CAGE.  This body already has a TAGGED claim out on
            # SLOT_FERRY_ID/SLOT_FERRY_RND and the tag is what licenses the
            # launcher beside it to self-destruct.  An untagged re-ping in the
            # same window would strip it and retire the ferry to an ordinary
            # LOKI hop -- correct, but 20 Ti of permanent scale dearer.
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
        # TERMINAL WEAPONS W3.  A launcher standing at THEIR ring is a PLUCKER
        # and nothing else, and the branch has to come first for two separate
        # reasons.  (1) `SLOT_LAUNCHER` is the home-launcher latch: a forward
        # launcher that claims it stops the Core ever buying the home one, which
        # is our cheapest home defence.  (2) Everything below needs `self.core`,
        # and a forward launcher sees r^2 = 26 -- it can never see our own Core,
        # so it would return here and do nothing for the rest of the match.
        # The exile ordering below is wrong for it as well: "farthest from OUR
        # Core" points deeper into THEIRS.
        if TW_ON and TW_PLUCK_ON:
            E = self._enemy_anchor(ct)
            if E is not None and dsq_core(ct.get_position(), E) <= TW_FWD_LAUNCH_DSQ:
                self._tw_launcher(ct, ct.get_position(), E)
                return
        # PLANK CAGE arm 1, THE FERRY, and it sits here for the two reasons the
        # plucker above does.  (1) A ferry launcher stands mid-map and can
        # never see our own Core, so the `self.core is None` return below would
        # retire it on its first turn.  (2) It must not claim SLOT_LAUNCHER --
        # that latch is what stops the Core buying the home launcher, and a
        # disposable relay two rounds from self-destructing is not our home
        # defence.  A launcher that has ALREADY ferried keeps the same
        # exemption for the rest of its life.
        if CAGE_ON and CAGE_FERRY:
            E = self._enemy_anchor(ct)
            if E is not None and self._cg_ferry_launch(
                    ct, ct.get_position(), E, ct.get_current_round()):
                return
            if self.cg_threw:
                return
        else:
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
        if CAGE_ON and CAGE_FERRY:
            # THE HOME-LAUNCHER LATCH, MOVED BELOW THE CORE LOOKUP -- and only
            # under this plank's flag, so the flag-off fork writes it on the
            # same line leap6 does.  A launcher sees r^2 = 26; before the cage
            # every launcher we built stood at home and always resolved
            # `self.core`, so claiming first cost nothing.  A ferry relay never
            # resolves it, and a claim from one of those permanently stops the
            # Core buying the home launcher it is not.
            ct.write_store(SLOT_LAUNCHER, 1)
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
            # PLANK SOCKET-GUARD arm 4, THE EVICTION.  Same mechanism, two
            # corrections that only matter for a launcher sitting on our own
            # ring -- which is where leap6's never sat.
            #   * NEVER BESIDE ONE OF OUR OWN BUILDINGS.  A builder is dropped
            #     with its action free; dropped next to our feeder conveyor it
            #     simply pecks that instead, 2 Ti for 2 damage against a 20 HP
            #     belt, and we have handed it a shorter walk to the thing it
            #     came for.  Same refusal `_tw_launcher` makes at their ring.
            #   * NEVER BACK ONTO OUR OWN DOORSTEP.  Our ring tiles are LEGAL
            #     throw targets and the naive "farthest from the anchor" order
            #     will happily use one when the geometry is awkward.
            # Then: farthest from our Core, and among ties the site on THEIR
            # side, which is the longest walk back for a body that moves one
            # tile a round.
            if SG_ON and SG_CORNER_LAUNCHER and dsq_core(lp, self.core) <= 2:
                fkey = (lp, self.core, dest)
                if self.sg_far_key != fkey:
                    if dest is not None and SG_THROW_TOWARD_ENEMY:
                        self.sg_far = sorted(
                            sites,
                            key=lambda t: (-dsq_core(t, self.core),
                                           dsq_core(t, dest), t.y, t.x))
                    else:
                        self.sg_far = sorted(
                            sites, key=lambda t: (-dsq_core(t, self.core), t.y, t.x))
                    self.sg_far_key = fkey
                mine = []
                try:
                    for bid in ct.get_nearby_buildings():
                        if ct.get_team(bid) == self.team:
                            mine.append(ct.get_position(bid))
                except Exception:
                    mine = []
                for site in self.sg_far:
                    if dsq_core(site, self.core) < SG_THROW_MIN_DSQ:
                        break       # sorted farthest-first: the rest are worse
                    near_ours = False
                    for m in mine:
                        if site.distance_squared(m) <= SG_THROW_CLEAR_DSQ:
                            near_ours = True
                            break
                    if near_ours:
                        continue
                    try:
                        if not ct.can_launch(bp, site):
                            continue
                        ct.launch(bp, site)
                    except Exception:
                        continue
                    self.sg_evicts += 1
                    if SG_LOG:
                        print("SG evict (%d,%d)->(%d,%d) n=%d"
                              % (bp.x, bp.y, site.x, site.y, self.sg_evicts))
                    return
                # Nothing clean in range: fall through to leap6's order rather
                # than leave an intruder standing on our ring.
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

    # ------------------------------------------------------------------
    # PLANK CAGE (CG).  Spec, constants and the corpus behind every number:
    # the PLANK CAGE block at the end of doctrine.py.  Four arms, one master
    # flag, and every method here returns a falsy no-op with CAGE_ON down.
    # ------------------------------------------------------------------

    def _cg_eyes(self, ct, E):
        """Can this body SEE a tile of their Core footprint right now?

        The publish/republish split, exactly as FIX B drew it for the HP band:
        a body with eyes states what it derived, a body without restates what
        it read, so a raider standing six tiles out on the blind side of the
        ring is a no-op on the field rather than an eraser.
        """
        for c in core_tiles(E):
            try:
                if ct.is_in_vision(c):
                    return True
            except Exception:
                continue
        return False

    def _cg_gate_n(self):
        """CAGE_SEAL_GATE, clamped to the ring this Core actually has.

        A Core against a map edge loses ring tiles to `heal_seats` /
        `core_corners`' bounds filters, and a gate it can never reach would
        hold our fire until the timeout.
        """
        n = len(self.raid_stations)
        if n and CAGE_SEAL_GATE > n:
            return n
        return CAGE_SEAL_GATE

    def _cg_opened(self, rnd, n, why):
        """Latch OPEN on this body and announce it once."""
        if self.cg_open:
            return
        self.cg_open = True
        if CAGE_LOG:
            print("CG open r=%d n=%d w=%s" % (rnd, n, why))

    def _cg_beat_bit(self, ct, E, rnd):
        """Slot 15 bit 31, assembled by `_raid_beat` -- the ONE published bit.

        Returns CAGE_HOLD_BIT while the cage is unfinished and 0 once it is.
        Three ways out of the hold, and the second and third are what keep a
        dead raid from muting our guns for the rest of the match:

          * THIS body's own ring census reached the gate;
          * the clock ran out (CAGE_SEQ_TIMEOUT -- `73867571_g4`, a full seal
            held 855 rounds into a titanium loss);
          * the published bit went 1 -> 0, i.e. a teammate opened and won the
            round's last write.  Slot 15 is last-write-wins within a round, so
            the raiders converge over a round or two rather than instantly;
            they are all looking at the same twelve tiles, so they converge.

        NOTE. A BLIND ESTABLISHED RAIDER PUBLISHES THE HOLD, IT DOES NOT
        REPUBLISH WHAT IT READ, and that is the opposite of what the HP band
        two bits below does.  MEASURED, nordkap seed 2: with the band's
        republish rule the bit could never bootstrap -- the first eyed raider
        publishes 1 into a word that still reads 0, a blind raider later in the
        SAME round republishes that 0, and the eyed raider reads its own 1 back
        as a 0 next round and opens fire at r4 on a 4/12 seal.  The band can
        republish because its zero state means "nobody has looked"; this bit's
        zero state means "shoot", which is the answer that must never be
        arrived at by accident.  `cg_saw` exists for the same reason: the peer
        clear needs a 1 that was actually OBSERVED, never merely one this body
        believes it wrote.
        """
        if not (CAGE_ON and CAGE_BEFORE_SIEGE) or self.cg_open:
            return 0
        # WAVE 12, ARM A.  NO EVICTOR, NO HOLD.  This method is the ONLY writer
        # of the hold bit, so refusing here mutes the whole team's hold-fire
        # with no new store field: `_cg_hold` reads a bit that is simply never
        # set and every gun answers "shoot" -- which is the leap6 attack, and
        # the fallback this batch is designed around.  Placed ABOVE the clock
        # and the census on purpose: neither `cg_since` nor `cg_saw` may be
        # advanced by a body that is not holding, or the INHERIT branch below
        # would read this body's silence as a teammate's open.
        if CAGE_EVGATE_HOLD and not self._cg_evgate(ct, E, rnd):
            return 0
        if rnd > CAGE_SEQ_TIMEOUT:
            self._cg_opened(rnd, -1, "clock")
            return 0
        word = 0
        try:
            word = ct.read_store(CAGE_BEAT_SLOT)
        except Exception:
            word = 0
        seen = word & CAGE_HOLD_BIT
        if seen:
            self.cg_saw = True
        if self.cg_since < 0:
            self.cg_since = rnd
        elif not seen and not self.cg_saw:
            # INHERIT.  A raider that joins a raid ALREADY IN PROGRESS must not
            # restart the hold: measured on midgard seed 2, a body that reached
            # the ring at r120 -- long after the team opened at r58 -- re-held
            # our guns from r135 to r155 because its own census was short of
            # the gate.  A live heartbeat stamped BEFORE this body's first
            # published round is a teammate who was established first and is
            # not holding, which can only mean the team has already opened.
            beat = word & COLLAR_BEAT_MASK
            if (beat and rnd - (beat - 1) <= LOKI_FOOTHOLD_STALE
                    and (beat - 1) < self.cg_since):
                self._cg_opened(rnd, -1, "join")
                return 0
        n12 = -1
        if E is not None and self._cg_eyes(ct, E):
            # WAVE 11, FIX 1.  THE STRICT CENSUS OPENS FIRE, NOT THE LOOSE ONE.
            # This is the gate DOCTRINE 19.7 risk 5 named: "the CAGE hold gate
            # still opens on a ring full of their healers".  `_cg_seal`'s loose
            # count reads one of THEIR bodies on one of THEIR seats as SEALED
            # (19.2 (i)), so the hold released on a phantom cage -- own census
            # 10 of 12 against a board of 4-8.  `_fin_seal` is the same pass
            # with their bodies excluded.  Opening LATER off the strict count
            # is the point: the sequencing arm exists to make us shoot only
            # once the ring is actually shut.
            n12, _n8 = self._cg_census(ct, E)
            if n12 >= self._cg_gate_n():
                self._cg_opened(rnd, n12, "seal")
                return 0
        if self.cg_saw and not seen:
            self._cg_opened(rnd, n12, "peer")
            return 0
        return CAGE_HOLD_BIT

    def _cg_active(self, ct):
        """Is the cage running?  False once finisher guard (i) has fired.

        A per-unit latch and not a store field, because the quantity it is
        derived from -- the enemy-Core HP band -- is ALREADY published
        team-wide in slot 15 bits 28-29, so every body reaches the same answer
        from the same evidence without a second shared field to lose races in.
        """
        return bool(CAGE_ON) and not self.cg_disarm

    def _cg_hold(self, ct, rnd):
        """CAGE_BEFORE_SIEGE: must this unit withhold fire on their CORE?

        One store read, memoised, and it decodes two fields of the same word:
        bit 31 is the hold and bits 0-9 are the raid heartbeat.  The heartbeat
        term is not decoration -- the hold bit is only ever REFRESHED by a
        raider at the ring, so without it a raid that was wiped out would leave
        a stale 1 muting every gun we own.
        """
        if not (CAGE_ON and CAGE_BEFORE_SIEGE) or self.cg_open:
            return False
        if rnd > CAGE_SEQ_TIMEOUT:
            return False
        if self.cg_hold_rnd == rnd:
            return self.cg_hold_val
        self.cg_hold_rnd = rnd
        self.cg_hold_val = False
        try:
            v = ct.read_store(CAGE_BEAT_SLOT)
        except Exception:
            return False
        if not (v & CAGE_HOLD_BIT):
            return False
        beat = v & COLLAR_BEAT_MASK
        if not beat or rnd - (beat - 1) > LOKI_FOOTHOLD_STALE:
            return False
        self.cg_hold_val = True
        return True

    def _cg_hold_log(self, ct, rnd):
        """`CG hold r=N`, at most once per CAGE_HOLD_LOG_GAP rounds per unit."""
        if not CAGE_LOG:
            return
        if rnd - self.cg_hold_log < CAGE_HOLD_LOG_GAP:
            return
        self.cg_hold_log = rnd
        print("CG hold r=%d" % rnd)

    def _cg_seal(self, ct, E):
        """(ring12 held, ring8 held) as THIS body can see it.  Round-memoised.

        HELD means the tile cannot be used by them: terrain, a building of
        either team (their own conveyor on a seat costs them the seat too --
        measured, probe Q2.1), or one of our bodies standing on it.  A tile out
        of vision counts as NOT held, which is the pessimistic direction for
        every consumer: it delays opening fire and it delays spending on
        corners, and both of those are the cheap error.
        """
        rnd = ct.get_current_round()
        if self.cg_seal_rnd == rnd:
            return self.cg_seal_val
        self.cg_seal_rnd = rnd
        self._ring(E)
        ncorner = len(self.raid_corners)
        n12 = n8 = 0
        s12 = s8 = 0
        i = -1
        for t in self.raid_stations:
            i += 1
            held = False
            # PLANK FIN, THE STRICT SEAL, taken in the SAME pass so it costs no
            # extra tile reads.  `held` above is resolved through
            # `is_tile_passable`, which engine_mechanics.md N.6 measures as
            # FALSE under a builder bot OF EITHER TEAM -- so one of THEIR
            # healers sitting on one of THEIR heal seats reads to us as SEALED.
            # Measured, wave-10 probe vs mimic_istones: own census 10/12, board
            # 4-8, their seat occupancy 6.45/8, enemy heal ratio 1.000.  A ring
            # full of their healers is the OPPOSITE of a cage.  `strict` counts
            # a tile only for terrain, a building of either team, or one of OUR
            # bodies -- the definition tools/fin_mechanism.py measures from the
            # board -- and PLANK FIN is its only consumer.  `held` is left
            # exactly as it was: it gates the CAGE hold, and tightening that
            # would hold our fire far longer against the very opponents wave 8
            # measured the hold-fire stretch on.
            strict = False
            try:
                if not ct.is_in_vision(t):
                    held = False
                elif ct.get_tile_building_id(t) is not None:
                    held = True
                    strict = True
                elif not ct.is_tile_passable(t):
                    held = True
                    oid = ct.get_tile_builder_bot_id(t)
                    strict = oid is None or ct.get_team(oid) == self.team
                else:
                    oid = ct.get_tile_builder_bot_id(t)
                    held = oid is not None and ct.get_team(oid) == self.team
                    strict = held
            except Exception:
                held = False
                strict = False
            if held:
                n12 += 1
                if i >= ncorner:
                    n8 += 1
            if strict:
                s12 += 1
                if i >= ncorner:
                    s8 += 1
        self.cg_strict_val = (s12, s8)
        self.cg_seal_val = (n12, n8)
        return self.cg_seal_val

    def _fin_seal(self, ct, E):
        """(ring12, ring8) held STRICTLY -- their bodies do not count.

        Computed as a by-product of `_cg_seal`, which is round-memoised, so
        this is one dict lookup on every call after the first of the round.
        """
        self._cg_seal(ct, E)
        return self.cg_strict_val

    def _cg_census(self, ct, E):
        """(ring12, ring8) as every CAGE **GATE** reads it.  WAVE 11, FIX 1.

        One accessor, so there is exactly one place the loose/strict choice is
        made and exactly one flag that reverts the whole change
        (`CAGE_STRICT_SEAL = False` == loki_leap8 branch for branch).  Both
        halves come out of the SAME memoised pass, so this costs nothing.

        The loose count is not deleted -- it is demoted to the one question it
        answers correctly, "which ring tiles cannot be built on right now",
        which is a SCOUTING question about tiles needing an eviction and not a
        statement about whether their Core is caged.  Its one surviving caller
        is `_cg_corner_ok`'s free-corner arithmetic.
        """
        if CAGE_STRICT_SEAL:
            return self._fin_seal(ct, E)
        return self._cg_seal(ct, E)

    def _cg_tick(self, ct, E, rnd):
        """Once per established raider per round: the census and guard (i).

        The PUBLISH half of the sequencing arm is not here -- it rides
        `_raid_beat`'s single write (`_cg_beat_bit`).  What is left is the
        instrument (`CG seal`, which is the whole mechanism measurement and
        must keep running after fire is opened) and the finisher guard, which
        is a per-unit latch off an already-published quantity.
        """
        if not CAGE_ON or self.cg_disarm:
            return
        # WAVE 11, FIX 1.  The instrument reports what the GATES read, with the
        # loose count carried alongside as `l=` so the two are comparable in
        # one line and the wave-10 replays stay readable.  Every tool that
        # consumes this matches `^CG (\w+)` and takes the seal off the BOARD
        # (tools/cage_mechanism.py, tools/fin_mechanism.py), so the extra field
        # breaks nothing.
        n12, n8 = self._cg_census(ct, E)
        l12, _l8 = self._cg_seal(ct, E)
        if CAGE_LOG and (n12, n8) != self.cg_seal_log:
            self.cg_seal_log = (n12, n8)
            print("CG seal n=%d/12 r8=%d/8 l=%d" % (n12, n8, l12))
        # PLANK FIN.  Published from the census this body just took, and ONLY
        # by a body that can actually see their Core: `_cg_seal` counts a tile
        # out of vision as NOT held, so a blind raider publishing would shut
        # the window on a ring it never looked at.
        if FIN_ON and E is not None and self._cg_eyes(ct, E):
            s12, s8 = self._fin_seal(ct, E)
            # WAVE 12, ARM B.  The window's surge and pecks are the second
            # expensive arm, and this is its ONE publisher.  The census is
            # published honestly and the GATE rides beside it, so `FIN close`
            # still names the round the window shut and the seal numbers in the
            # replay stay the board's numbers and not the gate's.
            gate = True
            if CAGE_EVGATE_FIN:
                gate = self._cg_evgate(ct, E, rnd)
            self._fin_publish(ct, rnd, s12, s8, gate)
        if rnd <= CAGE_SEQ_TIMEOUT + CAGE_FINISH_GRACE:
            return
        # FINISHER GUARD (i).  `73867571_g4`: a full seal held 855 rounds, the
        # game hit the r1000 cap and Jython lost on titanium_collected.  HIGH
        # means SEEN and still at or above CAGE_FINISH_HP; an UNKNOWN band is
        # never grounds to tear the cage down, and the band is republished
        # every round by whichever raider has eyes, so this is the same
        # evidence for every body that evaluates it.
        try:
            band = self._sge_core_band(ct, E)
        except Exception:
            return
        if band != SIEGE_HP_HIGH:
            return
        self.cg_disarm = True
        if CAGE_LOG:
            print("CG off r=%d" % rnd)

    def _cg_evict_sited(self, lp, E):
        """Can a launcher standing at `lp` reach INTO their ring?  WAVE 11.

        True when any of the twelve ring tiles falls inside the engine's
        d^2 <= 2 pickup disc, which is the whole test for "this building is an
        evictor".  Pure geometry off the cached ring, no tile reads, no store
        traffic -- it is called once per ferry throw and once per launcher
        siting decision.
        """
        if E is None:
            return False
        try:
            self._ring(E)
            for t in self.raid_stations:
                if t.distance_squared(lp) <= CAGE_FERRY_CONVERT_DSQ:
                    return True
        except Exception:
            return False
        return False

    def _cg_ev_seen(self, ct, E, rnd):
        """Is an EVICTOR of ours standing on their ring RIGHT NOW?  WAVE 12.

        One pass over the nearby-building cache -- the same pass `_cg_evict_far`
        and `_tw_census` already make -- filtered to LAUNCHERS of ours whose own
        pickup disc touches a ring tile (`_cg_evict_sited`).  Round-memoised,
        because three arms ask it in the same turn and the answer cannot change
        inside one.

        A body that cannot SEE the ring answers False, and that is a REFUSAL
        and not a fact.  Which is why every consumer is either a raider at the
        ring or a reader of a field such a raider published -- see the wiring
        paragraph in the CAGE EVICTOR GATE block of doctrine.py.
        """
        if self.cg_ev_rnd == rnd:
            return self.cg_ev_val
        self.cg_ev_rnd = rnd
        self.cg_ev_val = False
        if E is None:
            return False
        try:
            me = self.team if self.team is not None else ct.get_team()
            for bid in ct.get_nearby_buildings():
                if ct.get_entity_type(bid) != EntityType.LAUNCHER:
                    continue
                if ct.get_team(bid) != me:
                    continue
                bp = ct.get_position(bid)
                # Cheap reject first: the 12-tile disc walk below is only
                # reached by a launcher that is already AT their Core.
                if dsq_core(bp, E) > TW_CENSUS_DSQ:
                    continue
                if not self._cg_evict_sited(bp, E):
                    continue
                self.cg_ev_val = True
                self.cg_ev_last = rnd
                self.cg_gate_log = False
                if self.cg_ev_first < 0:
                    self.cg_ev_first = rnd
                    if CAGE_LOG:
                        print("CG evictor r=%d (%d,%d)" % (rnd, bp.x, bp.y))
                return True
        except Exception:
            return False
        return False

    def _cg_evgate(self, ct, E, rnd):
        """WAVE 12.  May the cage's EXPENSIVE arms run for this body?

        Hold-fire, the FIN window and the diagonal-corner spend are the three
        arms that cost titanium or forgone damage, and wave 11 measured them at
        +4.4 pp where an evictor stood and -9.0 pp where none did.  This is the
        precondition, and it is the SAME geometry the +4.4 pp cells were
        selected on -- not a proxy for it.

        Three states and two latches.  SEEN is the gate, open.  SEEN RECENTLY
        (CAGE_EVGATE_HYST) is still open, because an evictor that is shot and
        rebuilt is the normal case and flapping a ONE-WAY latch like `cg_open`
        is worse than either state.  NEVER SEEN past CAGE_EVGATE_DEADLINE is
        dead for the game: the ferry's own clock has stopped and nothing is
        coming.  With the flag down every answer is True and this fork is
        loki_leap9 exactly.
        """
        if not (CAGE_ON and CAGE_EVGATE_ON):
            return True
        if self.cg_ev_dead:
            return False
        if self._cg_ev_seen(ct, E, rnd):
            return True
        if self.cg_ev_first >= 0:
            if rnd - self.cg_ev_last <= CAGE_EVGATE_HYST:
                return True
            if CAGE_LOG and not self.cg_gate_log:
                self.cg_gate_log = True
                print("CG evgate r=%d off" % rnd)
            return False
        # The deadline is only evidence when this body could actually have SEEN
        # one.  `E is None` is "we have not found their Core yet", which is a
        # blindness and not a verdict -- latching the cage dead on it would
        # retire the plank on the one map where the raid took 90 rounds to
        # arrive.  Note the ordering above: a body that sees an evictor is
        # never asked this question, so a raider that spawns at r120 into a
        # live evictor still runs the cage.  What the latch kills is the body
        # that watched the whole ferry window go by with nothing in it.
        if E is not None and rnd > CAGE_EVGATE_DEADLINE:
            self.cg_ev_dead = True
            if CAGE_LOG:
                print("CG evgate r=%d dead" % rnd)
        return False

    def _cg_chain_dead(self, ct, E, rnd):
        """WAVE 13, ARM D.  Has this body's ferry chain been abandoned?

        The gate above retires the cage for a body that watched the whole ferry
        window go by with no evictor in it.  This is the same verdict applied
        to the TRANSPORT: once `cg_ev_dead` is latched there is no cage left
        for a rider to be carried to, so the chain stops being REBUILT.

        READ-ONLY ON THE GATE'S LATCH, and that is the whole subtlety.  The
        obvious implementation -- call `_cg_evgate` and return `cg_ev_dead` --
        is WRONG, and it is wrong in a way that would not show up in a marker
        census.  `cg_ev_dead` is a ONE-WAY latch and `_cg_evgate` is what sets
        it, so asking the gate from the ferry path would set it for a rider
        still walking at r81.  Under leap10_est that rider's FIRST gate call
        happens when it reaches the ring -- and if an evictor stands there at
        r95, `_cg_ev_seen` answers before the deadline branch is ever reached
        and the cage runs (DOCTRINE 21.5 risk 6, deliberate).  Latching from
        here would retire that body's cage at r81 for a game it was about to
        win.  So this reads the same condition and writes none of it.

        `_cg_ev_seen` is still consulted, because it is round-memoised, the
        gate is asking it anyway, and it can only move the answer to NOT dead:
        a rider that can see an evictor past the deadline has a chain worth
        keeping.  It records a sighting (`cg_ev_first`); it never records a
        death.  `E is None` -- their Core not found yet -- is blindness and not
        a verdict, exactly as it is one method up.
        """
        if not (CAGE_ON and CAGE_FERRY and CAGE_EVGATE_ON
                and CAGE_CHAIN_DEADLINE_ON):
            return False
        if self.cg_ev_dead:
            return True
        if E is None or rnd <= CAGE_EVGATE_DEADLINE:
            return False
        if self.cg_ev_first >= 0:
            return False
        return not self._cg_ev_seen(ct, E, rnd)

    def _cg_chaincut(self, rnd, why):
        """WAVE 13.  Marker for a rebuild arm D refused that the CLOCK allowed.

        Deliberately NOT a marker for every refusal past the deadline: the
        ferry's own `CAGE_FERRY_MAX_RND` refuses those already, and counting
        them would read as a saving this arm did not make.  It fires only
        where arm D is load-bearing -- which, at the shipped constants
        (`CAGE_FERRY_MAX_RND == CAGE_EVGATE_DEADLINE == 80`), is nowhere.  One
        line per body per reason; the state costs a dict this class already
        carries for `_cg_why`.
        """
        if not CAGE_LOG or self.cg_chain_log.get(why):
            return False
        self.cg_chain_log[why] = True
        print("CG chaincut r=%d w=%s" % (rnd, why))
        return False

    def _cg_evict_live(self, ct, E, p, rnd):
        """Is the CAGE's evictor regime running for this body?  WAVE 11, 3(b).

        The cap, the survivorship waiver and the spread preference all key off
        one predicate, and it is the SAME four-term gate that already replaces
        `_tw_gate` for the launcher (`_cg_gate`): the flag, the clock,
        establishment, a live foothold.  Nothing here loosens who may buy a
        launcher -- only how many and where.
        """
        if not (CAGE_ON and CAGE_EVICT):
            return False
        try:
            return bool(self._cg_gate(ct, E, p, rnd))
        except Exception:
            return False

    def _cg_evict_far(self, ct, E, t):
        """d^2 from ring tile `t` to the NEAREST evictor of ours, or None.

        The spread key of FIX 3(b).  The four ring corners partition the eight
        heal seats into four disjoint pairs, so a second launcher is worth a
        second pair of seats only if it goes somewhere the first one is not --
        and the corner that maximises this number is the diagonal opposite.
        None means "we see no launcher of ours at their ring", which every
        caller reads as "no preference", not as "far".
        """
        best = None
        try:
            for bid in ct.get_nearby_buildings():
                if ct.get_entity_type(bid) != EntityType.LAUNCHER:
                    continue
                if ct.get_team(bid) != self.team:
                    continue
                bp = ct.get_position(bid)
                if dsq_core(bp, E) > TW_CENSUS_DSQ:
                    continue
                d = t.distance_squared(bp)
                if best is None or d < best:
                    best = d
        except Exception:
            return None
        return best

    # --- arm 1: the launcher ferry -----------------------------------------

    def _cg_near_sites(self, ct, lp, E):
        """This launcher's throw disc, NEAREST their Core first.

        Shares `_launch_sites` with the other three orderings a launcher can
        hold, on the same terms: a launcher is a building and never moves, so
        the 88-tile disc is built once per launcher and each ordering is
        re-sorted only when the anchor it is keyed to changes.
        """
        w, h = self.mw, self.mh
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
            self.tw_far_key = None
            self.cg_near_key = None
        nkey = (lp, E)
        if self.cg_near_key != nkey:
            self.cg_near_key = nkey
            self.cg_near = sorted(self._launch_sites, key=lambda t: dsq_core(t, E))
        return self.cg_near

    def _cg_ferry_floor(self):
        """Titanium the ferry must leave in the bank, sized to the trunk.

        The one number this arm gets wrong destroys the game rather than
        degrading it -- see the paragraph at CAGE_FERRY_TI_FLOOR and the
        glacierkeep trace behind it.  The discriminator is the length of the
        chain the opening bank still has to pay for, and a raider can read that
        straight off the decoded terrain it already holds: the d^2 from OUR
        Core to the nearest ore.  Computed once per body; `map_ores` is fixed
        for the match and `self.core` never moves.
        """
        if self.cg_floor is not None:
            return self.cg_floor
        near = False
        if self.core is not None and self.map_ores:
            best = None
            for o in self.map_ores:
                d = dsq_core(o, self.core)
                if best is None or d < best:
                    best = d
                    if best <= CAGE_FERRY_ORE_NEAR:
                        break
            near = best is not None and best <= CAGE_FERRY_ORE_NEAR
        self.cg_floor = (CAGE_FERRY_TI_FLOOR_NEAR if near
                         else CAGE_FERRY_TI_FLOOR)
        return self.cg_floor

    def _spr_live(self, ct, E, p, ti, rnd):
        """WAVE 18, PLANK SPRINT: is THIS rung a sprint rung?  True/False.

        Asked once per rider turn, by `_cg_ferry_try` and nowhere else, and it
        answers only the question "which ladder are we on" -- every actual
        refusal is left where it already was so the `CG why` instrument keeps
        naming reasons rather than a single conflated "sprint said no".

        Three terms and no state:  the flag; the WINDOW (their last ladder rung
        is r12 and their cage launchers are a separate t28 population, so a
        window that ends at SPR_MAX_RND cannot be the thing that buys the late
        launchers arm 4 buys); and the plank being armed at all.  The rider
        seat is NOT tested here because `_cg_ferry_try` has already refused
        every body that is not the rider before it reaches this call.

        Note what is deliberately absent: the CAP and the two MONEY tests.
        They stay in `_cg_ferry_try` as ordinary refusals, because a sprint
        that has run out of rungs or out of budget must NOT silently become a
        parent-ferry hop at the parent's 220 floor -- inside the window that is
        a strictly worse trade (it cannot afford one either) and it would spend
        the budget wave 12 reserved for the evictor post.
        """
        if not (SPR_ON and CAGE_ON and CAGE_FERRY):
            return False
        if rnd > SPR_MAX_RND:
            return False
        return bool(self._cg_active(ct))

    def _spr_collect(self, ti):
        """WAVE 19, FIX 1.  Tick the REALIZED-COLLECTION meter.  No decision.

        Called once per rider turn from the top of `_cg_ferry_try`, before any
        refusal, so the meter keeps running through every round the rung gate
        says no -- which is the whole point of it: the gate is waiting for this
        number to move.

        THE METER IS THE CUMULATIVE SUM OF POSITIVE BANK DELTAS between this
        body's own consecutive turns.  There is no `titanium_collected` reader
        in the API (docs 155/206 -- `get_global_resources()` is the only one),
        and this is the closest honest proxy a unit can compute:

          * MONOTONE by construction, so a rung can be priced against it;
          * an UNDERCOUNT, because another body's spend between two of our
            turns hides the income that paid for it.  Conservative in the
            direction this fix wants -- it errs toward refusing a rung;
          * it includes the 10 Ti / 4 rounds of passive income (docs 145),
            which is deliberate: it is the floor of the gate.  See the FIX 1
            block in doctrine.py.

        The first turn only seeds `spr_bank` -- a first delta measured against
        nothing would credit the whole 500 Ti opening bank as collection.
        """
        if not (SPR_ON and SPR_COLLECT_ON):
            return
        prev = self.spr_bank
        self.spr_bank = ti
        if prev is not None and ti > prev:
            self.spr_coll += ti - prev

    def _spr_gate(self, ct, ti, rnd):
        """WAVE 19, FIX 1.  May the sprint buy THIS rung?  True = yes.

        Two free passes and then the meter:
          * the OPENING is free -- any rung before SPR_FREE_RND, because the
            wave-18 trace is right that a 430 Ti bank at r2 is idle money and
            the defect was never the first rung;
          * RUNG ONE is free unconditionally, for the same reason and so that
            a leg whose economy dies still gets the one rung that proves the
            ladder was armed (it is also what keeps the inertness leg
            readable);
          * every later rung waits for SPR_COLLECT_STEP of realized
            collection since the rung before it.

        `spr_mark` is the meter's value at the previous rung and is written by
        `_cg_ferry_try` on a successful build, never here: a gate that moved
        its own watermark would let a refused rung reset the clock.
        """
        if not (SPR_ON and SPR_COLLECT_ON):
            return True
        if rnd < SPR_FREE_RND or self.spr_n < 1:
            return True
        mark = self.spr_mark
        if mark is None:
            return True
        return (self.spr_coll - mark) >= SPR_COLLECT_STEP

    def _spr_arrive(self, ct, rnd):
        """One-shot `SPR arrive` marker.  Latched per body, never a decision.

        The plank's headline number is a ROUND, and a round is exactly the sort
        of thing our own logs get wrong and a replay gets right -- so this
        marker exists to be CHECKED against `tools/leap14_delay.py`'s
        replay-side arrival, not to be trusted instead of it.
        """
        if self.spr_arr:
            return
        self.spr_arr = True
        # SPR_ON is tested HERE and not only at the two call sites, because one
        # of those sites is the ferry's "there" refusal, which the flags-off
        # fork can still reach whenever its own cap gate happens not to fire
        # first.  A flags-off leg that prints an SPR marker is not inert, and
        # the inertness leg is the only thing standing between this plank and
        # an unfalsifiable claim.
        if SPR_ON and CAGE_LOG and SPR_LOG:
            print("SPR arrive r=%d s=%d n=%d" % (rnd, self.raid_slot, self.spr_n))

    def _cg_ferry_try(self, ct, E, p, ti, rnd):
        """THE RIDER'S HALF.  Build the next ferry launcher.  True = action spent.

        One rider (CAGE_FERRY_SEATS), because SLOT_FERRY_ID is a single
        last-write-wins field and because Jython's ladder is one builder
        crossing the map, not a convoy.  The site is the adjacent tile NEAREST
        their Core: the throw disc is measured from the LAUNCHER, so a site one
        tile forward is one free tile of range.

        After this the rider must not walk (`_cg_ferry_wait`): the launcher is
        created AFTER this body, therefore acts AFTER it every round, and a
        rider that steps out of the r^2<=2 pickup disc on the throw round has
        bought a 20-Ti building for nothing.
        """
        if not (CAGE_ON and CAGE_FERRY):
            return False
        if self.cg_seat is None:
            # LATCHED ON THE FIRST RAID TURN, never re-read.  `raid_slot` is
            # not a constant: `_raid`'s navigation-stall handler INCREMENTS it
            # to rotate the far-phase station assignment, so a rider that ever
            # bumps a wall silently stops being the rider -- which is what
            # capped the first build of this arm at one hop a game.
            self.cg_seat = (self.role == "raid"
                            and self.raid_slot < CAGE_FERRY_SEATS)
        if not self.cg_seat:
            return False
        # WAVE 19, FIX 1.  THE METER TICKS ABOVE EVERY REFUSAL, because the
        # gate below is waiting for it to move and a meter that only ran on
        # rounds we were already allowed to build would never move at all.
        # It is a read of `ti` we already have and one comparison; no API call.
        self._spr_collect(ti)
        # WAVE 13, ARM D -- THE CHAIN BILL.  Above the post and above the cap,
        # because once the gate has retired the cage for this body there is no
        # destination left: the post exists to establish an evictor the gate
        # will no longer act on, and a hop exists to carry a rider to it.  The
        # marker fires only if the ferry's own clock would have said yes, so
        # this line is free at the shipped constants and is an invariant the
        # moment they drift -- see THE CHAIN BILL in doctrine.py.
        if self._cg_chain_dead(ct, E, rnd):
            if rnd <= CAGE_FERRY_MAX_RND:
                self._cg_chaincut(rnd, "lift")
            return self._cg_why(ct, rnd, "chaindead", ti)
        # WAVE 12, ESTABLISHMENT EFFORT (1).  THE POST OUTRANKS A HOP, and it
        # has to be asked HERE rather than at the "there" refusal below: the
        # ferry's own cap is the next test, and the first smoke measured the
        # consequence -- riders spent all three builds on transport, arrived,
        # and had no budget left for the thing the transport existed to
        # deliver (`CG post` fired once in thirteen legs).  A hop is a means; a
        # sited launcher is the end, and when the rider is already AT the ring
        # the means is worth nothing.
        if (CAGE_EST_RETRY and E is not None
                and dsq_core(p, E) <= CAGE_FERRY_STOP_DSQ
                and self._cg_est_post(ct, E, p, ti, rnd)):
            return True
        # ...and one build of the budget is RESERVED for that post, which is
        # the same lesson from the other side: three hops and no post is a
        # rider that walked the map to stand still.
        #
        # WAVE 12, MEASURED AND UNRESOLVED (results/wave12/smoke.txt, DOCTRINE
        # 21.3).  The reserve is a TRADE and the smoke priced both sides of it:
        # on the short-trunk cells (`nordkap`) it establishes at r5-r7 against
        # the base fork's r33-r35, and on the big-map cells it costs the THIRD
        # HOP, which is what carries the rider to the ring at all -- istones
        # `TW launch` 9 -> 6, `CG evict` 656 -> 27.  `CAGE_EST_RESERVE` is the
        # flag that ablates it (`bots/leap10_noresv`); the panel decides.
        # WAVE 18, PLANK SPRINT.  Resolved ONCE, here, and then consulted by
        # the four gates below -- because the four of them have to agree about
        # which ladder this rung belongs to.  A rung that passed the sprint's
        # cap and then paid the parent's bank floor would be neither ladder.
        spr = self._spr_live(ct, E, p, ti, rnd)
        # WAVE 22, ARM A1 -- THE RUNG BUDGET.  Exactly `need_eff` rungs, where
        # `need_eff` is computed at r0 from the BFS walk distance between the
        # two Core rings, and INSIDE that budget the rungs are UNCONDITIONAL:
        # the sprint's total-spend cap, its per-rung bank floor and the
        # wave-19 collection gate are all bypassed, because the ladder is what
        # the 3-builder cap was bought to pay for.  The price is flat
        # `floor(20*scale)` (engine E4): `destroy` is free and removes the
        # launcher's +10 % the same round, the rungs already self-destruct
        # (CAGE_FERRY_DISPOSABLE), and the measured 28/38/44/50/56/62
        # escalation was our own five opening builders at +20 % of scale EACH
        # -- exactly what the cap removes.  Band A-1 gets a budget of ZERO: it
        # needs no transport at all (OPENING.md 1.3).
        op_rungs = self._op_rungs(ct) if OPEN_ON else None
        op_uncond = bool(OPEN_ON and OPEN_RUNG_UNCOND and op_rungs
                         and self.spr_n < op_rungs)
        cap = ((CAGE_EST_LAUNCH_CAP - 1)
               if (CAGE_EST_RETRY and CAGE_EST_RESERVE) else CAGE_FERRY_CAP)
        if spr:
            # THE SPRINT KEEPS ITS OWN BOOKS.  `spr_n` is not `cg_ferry_n` and
            # not `cg_launch_n`, so when the window closes the parent's two
            # hops and the reserved evictor post are still there unspent --
            # see (1) in the PLANK SPRINT block in doctrine.py.
            if op_rungs is not None:
                if self.spr_n >= op_rungs:
                    return self._cg_why(ct, rnd, "opcap", ti)
            elif self.spr_n >= SPR_CAP:
                return self._cg_why(ct, rnd, "sprcap", ti)
        elif self.cg_ferry_n >= cap:
            return self._cg_why(ct, rnd, "cap", ti)
        lo = SPR_MIN_RND if spr else CAGE_FERRY_MIN_RND
        if rnd < lo or rnd > CAGE_FERRY_MAX_RND:
            return self._cg_why(ct, rnd, "clock", ti)
        if rnd < self.cg_wait_until:
            return self._cg_why(ct, rnd, "wait", ti)
        stop = SPR_STOP_DSQ if spr else CAGE_FERRY_STOP_DSQ
        if dsq_core(p, E) <= stop:
            # ARRIVED is where leap9 hands the whole problem to arm 4 and its
            # four corners.  The post that replaces that hand-off is tried at
            # the TOP of this method (establishment effort (1)); by here it has
            # already refused, so this is loki_leap9's refusal exactly.
            self._spr_arrive(ct, rnd)
            return self._cg_why(ct, rnd, "there", ti)
        if not self._cg_active(ct):
            return self._cg_why(ct, rnd, "off", ti)
        try:
            cost = ct.get_launcher_cost()
        except Exception:
            return False
        if spr and op_uncond:
            # THE UNCONDITIONAL RUNGS.  One money test and it is the engine's:
            # can we pay for it at all.  Everything else the sprint asks is a
            # brake on a budget the opening has already sized.
            if ti < cost:
                return self._cg_why(ct, rnd, "opti", ti)
        elif spr:
            # TWO BRAKES, both cheap, and the TOTAL one is checked against the
            # price of THIS rung so the cap is a ceiling on spend and not on
            # spend-so-far.  Below the floor the rung is simply not bought:
            # the trunk's next build outranks the ladder, every round.
            if self.spr_ti + cost > SPR_TI_CAP:
                return self._cg_why(ct, rnd, "sprti", ti)
            if ti < cost + SPR_TI_FLOOR:
                return self._cg_why(ct, rnd, "sprbank", ti)
            # WAVE 19, FIX 1 -- THE ECO GATE, and it is the LAST money test so
            # that `CG why` keeps naming the cheapest true reason first.  A
            # rung the bank could afford but the TRUNK has not earned is the
            # one wave 18 measured and the one this refuses.
            if not self._spr_gate(ct, ti, rnd):
                if (CAGE_LOG and SPR_LOG and SPR_COLLECT_LOG
                        and self.spr_gate_log != rnd):
                    self.spr_gate_log = rnd
                    print("SPR gate r=%d c=%d m=%d need=%d"
                          % (rnd, self.spr_coll, self.spr_mark or 0,
                             SPR_COLLECT_STEP))
                return self._cg_why(ct, rnd, "sprcoll", ti)
        elif ti < cost + self._cg_ferry_floor():
            return self._cg_why(ct, rnd, "bank", ti)
        best, best_d = None, None
        for dx, dy in CARD_DELTAS:
            tx, ty = p.x + dx, p.y + dy
            if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                continue
            t = Position(tx, ty)
            d = dsq_core(t, E)
            if best_d is not None and d >= best_d:
                continue
            try:
                if not ct.can_build_launcher(t):
                    continue
            except Exception:
                continue
            best, best_d = t, d
        if best is None:
            return self._cg_why(ct, rnd, "site", ti)
        try:
            ct.build_launcher(best)
        except Exception:
            return self._cg_why(ct, rnd, "build", ti)
        if spr:
            self.spr_n += 1
            self.spr_ti += cost
            # WAVE 19, FIX 1.  The watermark moves HERE and only here -- on a
            # rung that was actually bought.  `_spr_gate` never writes it: a
            # refusal that reset its own clock would be a gate that opens by
            # being closed.
            self.spr_mark = self.spr_coll
            if CAGE_LOG and SPR_LOG:
                print("SPR rung n=%d r=%d ti=%d d=%d c=%d"
                      % (self.spr_n, rnd, self.spr_ti, best_d, self.spr_coll))
        else:
            self.cg_ferry_n += 1
            self.cg_launch_n += 1    # WAVE 12: the ONE budget, all arms
        # WAVE 22, ARM A1 -- THE CADENCE.  A launcher built on round R is
        # created after this body, so it first acts on R+1 and throws then;
        # this body's own R+1 turn comes BEFORE it (creation order, engine H),
        # so the earliest round the rider can be somewhere else and buy the
        # next rung is R+2.  The parent's 3 is one wasted round per rung, which
        # on a need-6 map is six rounds of arrival.
        self.cg_wait_until = rnd + (OPEN_RUNG_WAIT if op_uncond
                                    else CAGE_FERRY_WAIT)
        try:
            ct.write_store(SLOT_FERRY_ID, ct.get_id() + 1)
            # CAGE_FERRY_TAG marks the claim as a CAGE claim, which is what
            # licenses the launcher to self-destruct afterwards.  Without it a
            # SOCKET-GUARD corner launcher at our own Core would read an
            # ordinary LOKI ferry ping and dispose of our home defence.
            ct.write_store(SLOT_FERRY_RND, rnd | CAGE_FERRY_TAG)
        except Exception:
            self.cg_wait_until = 0
        if CAGE_LOG:
            print("CG lift (%d,%d) n=%d" % (best.x, best.y, self.cg_ferry_n))
        return True

    def _cg_est_post(self, ct, E, p, ti, rnd):
        """CAGE_EST_RETRY: the ARRIVED rider buys the EVICTOR POST.  WAVE 12.

        Wave 11 established an evictor in about half its games, and wave 12's
        gate turns that number into the whole win: on the other half the bot
        falls back to leap6.  This is the arm that buys attempts, and it exists
        because of where leap9 stops -- the ferry refuses on "there" the moment
        the rider is inside CAGE_FERRY_STOP_DSQ and hands establishment to arm
        4, whose site set is the four ring CORNERS and which therefore fails
        outright when all four are occupied, bricked or unreachable.

        The site set here is every adjacent tile whose OWN pickup disc touches
        a ring tile -- strictly larger, and ranked by SEATS covered first,
        because the heal seats are what the evictor is for (ring12 is the spawn
        seal, ring8 is the heal seal, and only the second one is what "their
        heal is ~0" means).

        NO FERRY CLAIM IS WRITTEN, and that is the whole difference between
        this launcher and a relay: with SLOT_FERRY_ID unset `_cg_ferry_launch`
        returns at its first test, so the post never throws and never disposes
        of itself.  It stands, and `_launcher_turn` evicts off it every round
        for free.

        THE BUDGET is `cg_launch_n`, which counts every launcher this body has
        bought through any arm.  Three, for the game.
        """
        if not (CAGE_ON and CAGE_EST_RETRY and CAGE_EVICT) or E is None:
            return False
        if rnd > CAGE_EST_RETRY_RND:
            return self._cg_why(ct, rnd, "postclock", ti)
        if self.cg_launch_n >= CAGE_EST_LAUNCH_CAP:
            return self._cg_why(ct, rnd, "postcap", ti)
        if rnd < self.cg_wait_until:
            # A launcher of ours was bought within the last CAGE_FERRY_WAIT
            # rounds and is owed a throw.  Buying a second one beside it is how
            # the budget evaporates without an evictor to show for it.
            return self._cg_why(ct, rnd, "postwait", ti)
        if not self._cg_active(ct):
            return False
        # An evictor already stands.  A second one is arm 4's business
        # (CAGE_EVICT_CAP, and it sites the spread), not this arm's.
        if self._cg_ev_seen(ct, E, rnd):
            return self._cg_why(ct, rnd, "posthave", ti)
        try:
            cost = ct.get_launcher_cost()
        except Exception:
            return False
        if ti < cost + CAGE_EST_TI_FLOOR:
            return self._cg_why(ct, rnd, "postbank", ti)
        try:
            self._ring(E)
        except Exception:
            return False
        seats = self.raid_seatkeys
        best, bkey = None, None
        for dx, dy in CARD_DELTAS:
            tx, ty = p.x + dx, p.y + dy
            if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                continue
            t = Position(tx, ty)
            ns, nr = 0, 0
            for s in self.raid_stations:
                if s.distance_squared(t) > CAGE_EVGATE_DSQ:
                    continue
                nr += 1
                if (s.x, s.y) in seats:
                    ns += 1
            if not nr:
                continue            # not a post: it cannot reach the ring
            try:
                if not ct.can_build_launcher(t):
                    continue
            except Exception:
                continue
            key = (-ns, -nr, dsq_core(t, E), t.x, t.y)
            if bkey is None or key < bkey:
                best, bkey = t, key
        if best is None:
            return self._cg_why(ct, rnd, "postsite", ti)
        try:
            ct.build_launcher(best)
        except Exception:
            return self._cg_why(ct, rnd, "postbuild", ti)
        self.cg_launch_n += 1
        if CAGE_LOG:
            print("CG post (%d,%d)" % (best.x, best.y))
        return True

    def _cg_why(self, ct, rnd, why, ti):
        """Probe-grade refusal marker for the ferry.  Always returns False.

        Off by default (CAGE_LOG_WHY) and throttled per reason, exactly as
        `_tw_why` is: the ferry window is 80 rounds long and the rider walks
        through it every round, so an unthrottled marker is a real CPU line
        item on the one body whose CPU budget matters most.
        """
        if not (CAGE_LOG and CAGE_LOG_WHY):
            return False
        if rnd - self.cg_why_rnd.get(why, -10 ** 9) < CAGE_WHY_GAP:
            return False
        self.cg_why_rnd[why] = rnd
        print("CG why r=%d w=%s ti=%d n=%d" % (rnd, why, ti, self.cg_ferry_n))
        return False

    def _cg_ferry_wait(self, ct, p):
        """Is one of our launchers inside its own pickup disc of this body?

        Called only while `cg_wait_until` is in the future.  A False answer
        clears the wait as well as returning it: the launcher was shot, or the
        build never landed, and standing still for two more rounds beside
        nothing is exactly the `launchwait` failure the ferry ping was written
        to avoid.
        """
        if not (CAGE_ON and CAGE_FERRY):
            return False
        try:
            for bid in ct.get_nearby_buildings():
                if ct.get_team(bid) != self.team:
                    continue
                if ct.get_entity_type(bid) != EntityType.LAUNCHER:
                    continue
                if ct.get_position(bid).distance_squared(p) <= 2:
                    return True
        except Exception:
            self.cg_wait_until = 0
            return False
        self.cg_wait_until = 0
        return False

    def _cg_ferry_launch(self, ct, lp, E, rnd):
        """THE LAUNCHER'S HALF.  Throw the claimed rider forward.  True = done.

        The rider is identified by SLOT_FERRY_ID (its id + 1), written on the
        round it built this launcher -- which is exactly one round before this
        launcher's first turn, so the store's one-round buffer lines up with
        the engine's "a building does not act on the round it is built".

        Disposal is `self_destruct()`, measured on `bots/probe_ferry`: it works
        on a LAUNCHER, refunds the +10% scale, is legal in the same round as
        the throw, and ENDS THE TURN -- nothing after it runs, so it is the
        last statement in this method by necessity, not by style.  It is
        withheld when another of our builders is already inside the pickup
        disc: that launcher is a relay with a customer waiting.
        """
        if not (CAGE_ON and CAGE_FERRY):
            return False
        try:
            want = ct.read_store(SLOT_FERRY_ID)
            raw = ct.read_store(SLOT_FERRY_RND)
        except Exception:
            return False
        if not want or not (raw & CAGE_FERRY_TAG):
            return False
        stamp = raw & CAGE_FERRY_STAMP_MASK
        if rnd - stamp > CAGE_FERRY_STALE:
            return False
        # WAVE 13, ARM D, THE LAUNCHER'S HALF.  "An existing standing launcher
        # may finish its CURRENT throw" is a statement about the CLAIM, not
        # about this building: a launcher is blind to their ring by
        # construction (it is why the gate is published by raiders), so asking
        # it `_cg_chain_dead` would answer "dead" for every relay in every
        # game, evictor or not, and retire the transport wholesale.  The claim
        # carries the round it was written, so the round is what is tested.
        # `_cg_ferry_try` cannot write one past the deadline, which makes this
        # the belt to that brace and, at the shipped constants, unreachable.
        if (CAGE_EVGATE_ON and CAGE_CHAIN_DEADLINE_ON
                and stamp > CAGE_EVGATE_DEADLINE):
            self._cg_chaincut(rnd, "ferry")
            return False
        rider = None
        others = 0
        try:
            for eid in ct.get_nearby_entities():
                if ct.get_entity_type(eid) != EntityType.BUILDER_BOT:
                    continue
                if ct.get_team(eid) != self.team:
                    continue
                bp = ct.get_position(eid)
                if bp.distance_squared(lp) > 2:
                    continue
                if eid + 1 == want:
                    rider = bp
                else:
                    others += 1
        except Exception:
            return False
        if rider is None:
            return False
        here = dsq_core(rider, E)
        best = None
        for site in self._cg_near_sites(ct, lp, E):
            if dsq_core(site, E) + CAGE_FERRY_MIN_GAIN > here:
                break           # sorted nearest-first: everything after is worse
            try:
                if not ct.can_launch(rider, site):
                    continue
                ct.launch(rider, site)
            except Exception:
                continue
            best = site
            break
        if best is None:
            return False
        self.cg_threw = True
        try:
            ct.write_store(SLOT_FERRY_ID, 0)
            ct.write_store(SLOT_FERRY_RND, 0)
        except Exception:
            best = best
        if CAGE_LOG:
            print("CG ferry (%d,%d)->(%d,%d)" % (rider.x, rider.y, best.x, best.y))
        # WAVE 11, FIX 3(a).  A RELAY INSIDE PICKUP RANGE OF THEIR RING IS AN
        # EVICTOR, NOT SCRAP.  The chain's last launcher is frequently already
        # standing where arm 4 would have paid 20-30 scaled titanium to build
        # one, and the disposal refunds ~2 Ti for it.  Keeping it costs the
        # refund and buys a free pluck every round for the rest of the game --
        # which is the exact constraint the wave-10 verdict named as binding on
        # the ratchet (0.107 ratchets/game, "no launcher stood when needed").
        # Two terms: SITED (a ring tile inside its own d^2 <= 2 pickup disc)
        # and ESTABLISHED (the rider we just threw landed inside the raid's own
        # establishment radius, or a foothold is already live).  Anything that
        # fails either one self-destructs exactly as before.
        conv = False
        if CAGE_FERRY_CONVERT and CAGE_EVICT and E is not None:
            try:
                est = (dsq_core(best, E) <= LOKI_ESTABLISH_DSQ
                       or self._foothold_live(ct, rnd))
            except Exception:
                est = False
            # WAVE 12, ESTABLISHMENT EFFORT (2).  SITED ALONE CONVERTS.  The
            # establishment term is a second-guess about the RIDER, priced at
            # the ~2 Ti of scale refund disposal returns -- and a sited relay
            # is, by definition, the exact object wave 12's gate is waiting
            # for.  Under CAGE_EST_RETRY we stop second-guessing it.  Flag
            # down: `est` is required exactly as in loki_leap9.
            conv = self._cg_evict_sited(lp, E) and (est or CAGE_EST_RETRY)
        if conv:
            if CAGE_LOG:
                print("CG convert (%d,%d)" % (lp.x, lp.y))
            return True
        home = self.core is not None and dsq_core(lp, self.core) <= 2
        if not (CAGE_FERRY_DISPOSABLE and others == 0) or home:
            if CAGE_LOG:
                print("CG relay (%d,%d)" % (lp.x, lp.y))
            return True
        if CAGE_LOG:
            # BEFORE the call: self_destruct ends the turn and this print would
            # never be reached from the other side of it.
            print("CG sd (%d,%d)" % (lp.x, lp.y))
        try:
            ct.self_destruct()
        except Exception:
            return True
        return True

    # --- arm 2: the twelve-tile seal ---------------------------------------

    def _cg_corner_ok(self, ct, E, rnd):
        """May titanium be spent on a DIAGONAL corner of their ring yet?

        FINISHER GUARD (ii), and it is the difference between Jython's wins and
        `eed95e8e_g3`, which held 12/12 for 228 rounds at heal ratio 1.00 and
        lost: a corner denies a SPAWN tile, a seat denies HEALING, and sealing
        spawn before heal is a cage around a Core that repairs itself.

        The second term protects arms 3 and 4 from arm 2: our launcher is built
        ON a ring corner, so bricking the last free one removes the eviction
        and the hop.  A blind census (None) reads as a refusal.
        """
        if not (CAGE_ON and CAGE_SEAL):
            return False
        if not self._cg_active(ct):
            return False
        # WAVE 12, ARM C.  A CORNER IS A SPAWN DENIAL, AND A SPAWN DENIAL WITH
        # NO EVICTOR IS A CAGE AROUND A CORE THAT HEALS FASTER THAN WE SHOOT
        # IT -- `eed95e8e_g3` exactly, 12/12 held for 228 rounds at heal ratio
        # 1.00, lost.  This is the ONLY seal arm that takes the gate: a barrier
        # laid on a SEAT by an escort already standing beside it is 3 Ti, no
        # walk and no scaled purchase, and it stays free (the caller's `keys`
        # set is untouched).  What is refused here is the ranged, rationed,
        # scale-priced half that finisher guard (ii) already ekes out.
        if CAGE_EVGATE_CORNER and not self._cg_evgate(ct, E, rnd):
            return False
        # WAVE 11, FIX 1.  THE SPEND GATE IS STRICT; THE ARITHMETIC BELOW IS
        # NOT, AND THE SPLIT IS DELIBERATE.  Finisher guard (ii) asks "are
        # their HEAL seats actually shut yet" -- a seat under one of their
        # healers is the opposite of shut, so that term takes the strict
        # census.  The free-corner term asks a different question: "is there
        # still a corner our launcher could be BUILT on", and a corner with one
        # of their bodies standing on it is not one, whoever it belongs to.
        # That is the scouting question `is_tile_passable` answers correctly
        # and it is the loose count's one surviving job.
        _n12, n8 = self._cg_census(ct, E)
        l12, l8 = self._cg_seal(ct, E)
        if n8 < CAGE_RING8_FLOOR:
            return False
        free_corners = len(self.raid_corners) - (l12 - l8)
        if free_corners <= CAGE_CORNER_KEEP:
            nl, _ng = self._tw_census(ct, E)
            if not nl:
                return False
        return True

    def _cg_outer_station(self, ct, E, p, rnd):
        """A station OFF the ring that still touches a ring tile, or None.

        The endgame of a successful cage is that all twelve ring tiles are
        impassable -- our own bricks are impassable too -- and `_raid_station`
        scores exactly those twelve tiles.  Without this the raid arrives at a
        finished cage, finds no station, walks at the anchor and stalls into
        the pause; with it the body stands one tile out, where heal and
        build are both still orthogonally in reach and the reseal continues.
        """
        if not (CAGE_ON and CAGE_SEAL and CAGE_OUTER_STATION):
            return None
        if not self._cg_active(ct):
            return None
        ring = self.raid_ringkeys
        best, best_k = None, None
        for t in self.raid_stations:
            for dx, dy in CARD_DELTAS:
                tx, ty = t.x + dx, t.y + dy
                if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                    continue
                key = (tx, ty)
                if key in ring:
                    continue
                if key in self.map_walls:
                    continue
                if self.raid_ban.get(key, 0) > rnd:
                    continue
                s = Position(tx, ty)
                if dsq_core(s, E) == 0:
                    continue        # a footprint tile: never a station
                standing = (p.x == tx and p.y == ty)
                if not standing:
                    try:
                        if ct.is_in_vision(s):
                            if not ct.is_tile_passable(s):
                                continue
                            if ct.get_tile_builder_bot_id(s) is not None:
                                continue
                    except Exception:
                        continue
                k = (abs(p.x - tx) + abs(p.y - ty) - (2 if standing else 0), ty, tx)
                if best_k is None or k < best_k:
                    best, best_k = s, k
        return best

    # --- arm 4: eviction and the tangential hop ----------------------------

    def _cg_hop(self, ct, lp, E):
        """Throw one of OURS from a finished station to one that still wants work.

        The novel half of meta_2000 #5: to brick a ring tile a body must stand
        ORTHOGONALLY adjacent to it, the 2x2 footprint blocks the short path
        across, and walking the shell against a move cooldown is ~12 rounds
        where the throw is one.  Sides with 1-2 of these brick 7.5 ring tiles
        and win 79%; sides with none brick 3 and win 47%.

        The refusal that keeps it from being a taxi service: the rider must
        have NOTHING to do where it stands (no unheld ring tile orthogonally
        beside it), and the landing tile must be inside CAGE_HOP_MAX_DSQ of
        their footprint AND orthogonally beside a ring tile that is unheld.
        """
        if not (CAGE_ON and CAGE_HOP):
            return False
        rnd = ct.get_current_round()
        if rnd - self.cg_hop_rnd < CAGE_HOP_GAP:
            return False
        # The SCAN is throttled separately from the hop: a launcher whose
        # neighbours are all busy would otherwise re-run a 12-tile census and
        # an 88-tile site walk every round it declined, on a unit whose whole
        # job is one free throw.
        if rnd - self.cg_hop_try < CAGE_HOP_RETRY:
            return False
        self.cg_hop_try = rnd
        if not self._cg_active(ct):
            return False
        unheld = []
        for t in self.raid_stations:
            try:
                if not ct.is_in_vision(t):
                    continue
                if ct.get_tile_building_id(t) is not None:
                    continue
                if not ct.is_tile_passable(t):
                    continue
                oid = ct.get_tile_builder_bot_id(t)
                if oid is not None and ct.get_team(oid) == self.team:
                    continue
            except Exception:
                continue
            unheld.append(t)
        if not unheld:
            return False
        rider = None
        try:
            for eid in ct.get_nearby_entities():
                if ct.get_entity_type(eid) != EntityType.BUILDER_BOT:
                    continue
                if ct.get_team(eid) != self.team:
                    continue
                bp = ct.get_position(eid)
                if bp.distance_squared(lp) > 2:
                    continue
                busy = False
                for t in unheld:
                    if abs(bp.x - t.x) + abs(bp.y - t.y) == 1:
                        busy = True
                        break
                if busy:
                    continue
                rider = bp
                break
        except Exception:
            return False
        if rider is None:
            return False
        for site in self._cg_near_sites(ct, lp, E):
            if dsq_core(site, E) > CAGE_HOP_MAX_DSQ:
                break           # sorted nearest-first: everything after is worse
            good = False
            for t in unheld:
                if abs(site.x - t.x) + abs(site.y - t.y) == 1:
                    good = True
                    break
            if not good:
                continue
            try:
                if not ct.can_launch(rider, site):
                    continue
                ct.launch(rider, site)
            except Exception:
                continue
            self.cg_hop_rnd = rnd
            if CAGE_LOG:
                print("CG hop (%d,%d)->(%d,%d)"
                      % (rider.x, rider.y, site.x, site.y))
            return True
        return False

    def _cg_gate(self, ct, E, p, rnd):
        """PLANK CAGE's replacement gate, for the LAUNCHER ONLY.

        `_tw_gate`'s six terms were written for a DEFENSIVE plucker bought late
        out of a MACRO read.  The fresh corpus says the launcher at their ring
        is the DELIVERY and EVICTION system and has to exist by ~r20: Jython
        sites 43% of its launchers within d^2<=2 of the enemy spawn ring by
        median turn 8 and wins 80%, while our own 73 launchers went up at a
        median turn 255 and threw 8 times in total.

        Four terms survive -- the flag, the clock, establishment, a live
        foothold.  The archetype, the enemy-turret latch and the manned-seat
        count are dropped, and they are exactly what kept 85% of our games
        launcher-free.  The GUNNER keeps all six: it costs 4 ammo a round and
        this plank buys nothing that needs it.
        """
        if not (CAGE_ON and CAGE_EVICT) or E is None:
            return False
        if rnd < CAGE_LAUNCH_MIN_RND:
            return False
        if not self._cg_active(ct):
            return False
        try:
            if dsq_core(p, E) > LOKI_ESTABLISH_DSQ:
                return False
            return self._foothold_live(ct, rnd)
        except Exception:
            return False

    # ------------------------------------------------------------------
    # PLANK PAIRS (PR).  Spec, constants and the corpus behind every number:
    # the PLANK PAIRS block at the end of doctrine.py.  Four arms, three of
    # which are rewires: arm 1 lives in `_sge_mass_ok`, arm 3 in `main._sge_jit`
    # and the marker in `_sge_note_build`.  What is left here is the HOLD.
    # ------------------------------------------------------------------

    def _pr_near(self, ct, E, skip=None):
        """Live friendly Sentinels within 6 tiles of their Core CENTRE.

        The 6-tile predicate of meta_pipeline_diff.md gap 2, in the exact
        integers `sge_centre_q4` already gives the SIEGE band -- quarter-scale
        squared distance to the 2x2 centre, so (6*2)^2 = 144 with no floats.
        Nearest first, so the marker names the tube this one actually paired
        with.  `skip` drops the tile we are about to build on, which may or may
        not already be enumerable depending on when in the turn we are asked.

        Raider-side only.  A TURRET is never made to depend on this: it cannot
        be allowed to hold its fire forever because fog hid its partner, so the
        gate below reads the published census instead.
        """
        out = []
        if E is None:
            return out
        try:
            me = self.team if self.team is not None else ct.get_team()
            for bid in ct.get_nearby_buildings():
                if ct.get_entity_type(bid) != EntityType.SENTINEL:
                    continue
                if ct.get_team(bid) != me:
                    continue
                bp = ct.get_position(bid)
                if skip is not None and bp.x == skip.x and bp.y == skip.y:
                    continue
                q4 = sge_centre_q4(bp, E)
                if q4 <= PAIR_CENTRE_Q4:
                    out.append((q4, bp.x, bp.y, bp))
        except Exception:
            pass
        out.sort()
        return [r[3] for r in out]

    def _pr_hold(self, ct, rnd):
        """PLANK PAIRS arm 2: must this body withhold fire on their CORE?

        Answered off ONE store read (SLOT_FWD_GUN, the published forward-tube
        census) plus a per-unit clock, and memoised on the round because the
        turret path asks it up to three times a turn.

        THE CLOCK STARTS ON THE FIRST ASK, not on a build round.  This body is
        only ever asked when it has their Core in a line it could fire down, so
        the first ask IS the round this tube became able to shoot -- which is
        the quantity arm 4's 30-round release is denominated in, and it needs no
        store field to carry it.

        THE LATCH IS ONE-WAY.  Once `pr_open` is set -- by the pair arriving or
        by the release firing -- this body never holds again, even if the census
        falls back to 1 because a partner died.  The measured lever is PEAK
        sentinels within 6, and a tube that re-mutes itself on its partner's
        death stops being the 14-shot half of 28.
        """
        if not PAIR_ON or self.pr_open:
            return False
        if self.pr_hold_rnd == rnd:
            return self.pr_hold_val
        self.pr_hold_rnd = rnd
        self.pr_hold_val = False
        if self.pr_since is None:
            self.pr_since = rnd
        n = 0
        try:
            n = ct.read_store(SLOT_FWD_GUN)
        except Exception:
            n = 0
        if n >= PAIR_MIN:
            # The pair stands.  `PR pair` was already printed by the raider that
            # sited tube 2; this is the consumer side and it is silent.
            self.pr_open = True
            return False
        if rnd - self.pr_since >= PAIR_RELEASE_RNDS:
            self.pr_open = True
            if PAIR_LOG:
                print("PR release-solo r=%d" % rnd)
            return False
        self.pr_hold_val = True
        return True

    def _pr_hold_log(self, rnd):
        """`PR hold r=N`, at most once per PAIR_HOLD_LOG_GAP rounds per unit."""
        if not (PAIR_ON and PAIR_LOG):
            return
        if rnd - self.pr_hold_log < PAIR_HOLD_LOG_GAP:
            return
        self.pr_hold_log = rnd
        print("PR hold r=%d" % rnd)

    def _pr_core_hold(self, rnd, fwd_guns):
        """CORE side of arm 3: is a forward tube currently holding its fire?

        The Core cannot see the band and has no business scanning it, so it
        infers the hold from the same published census the tubes gate on plus
        its own latch on when that census first went positive -- which is the
        build round of tube 1 to within the round it takes slot 8 to be read
        back.  Deliberately CONSERVATIVE in the direction that matters: if it
        guesses "holding" when the tube has already opened, the only cost is a
        slightly fatter bank for at most PAIR_RELEASE_RNDS rounds.
        """
        if not (PAIR_ON and PAIR_JIT_RESERVE):
            return False
        if not fwd_guns:
            # No tube on the books at all: re-arm the clock for the next one.
            self.pr_solo_since = None
            return False
        if fwd_guns >= PAIR_MIN:
            return False
        if self.pr_solo_since is None:
            self.pr_solo_since = rnd
        return rnd - self.pr_solo_since < PAIR_RELEASE_RNDS
    # ------------------------------------------------------------------
    # PLANK FIN (the seal-window finisher) and PLANK RATCHET (evict, then
    # brick).  Spec, constants and the corpus behind every number: the two
    # blocks at the end of doctrine.py.  Every method here returns a falsy
    # no-op with FIN_ON / RAT_ON down.
    # ------------------------------------------------------------------

    def _fin_ok(self, n12, n8, was):
        """BOTH halves of the seal, with the hysteresis this body is holding.

        ring12 is the SPAWN seal and ring8 is the HEAL seal, and only the second
        one is what "their heal is ~0" means -- see the seat-term paragraph in
        the PLANK FIN block of doctrine.py and the 1,666-Ti game behind it.
        """
        if was:
            return n12 >= FIN_DROP and n8 >= FIN_SEAT_DROP
        return n12 >= FIN_GATE and n8 >= FIN_SEAT_GATE

    def _fin_publish(self, ct, rnd, n12, n8, gate=True):
        """Latch and publish the window.  EYED raiders only.

        The hysteresis lives here rather than in the readers so that every
        consumer -- the Core's ammunition pipe, a tube-siting raider, an escort
        on a seat -- is answering the same question from the same evidence.
        One brick shot out must not flicker the whole ammunition policy.

        WAVE 12: `gate` False publishes SHUT whatever the census says, and it
        is a publish and not a skip -- a stale OPEN left in slot 13 by the round
        before would go on surging the bank into a window that no longer has an
        evictor holding it.  Default True, so every other caller is unchanged.
        """
        if not FIN_ON:
            return
        was = self.fin_open
        now = bool(gate) and self._fin_ok(n12, n8, was)
        if now != was:
            self.fin_open = now
            if FIN_LOG:
                if now:
                    print("FIN open r=%d seal=%d r8=%d" % (rnd, n12, n8))
                else:
                    print("FIN close r=%d" % rnd)
        try:
            v = ct.read_store(FIN_PUB_SLOT)
            nv = ((v & FIN_PUB_KEEP)
                  | ((FIN_PUB_OPEN if now else FIN_PUB_SHUT) << FIN_PUB_SHIFT))
            if nv != v:
                ct.write_store(FIN_PUB_SLOT, nv)
        except Exception:
            return

    def _fin_window(self, ct, rnd):
        """The PUBLISHED window, as any blind body reads it.  Round-memoised.

        Two terms, and the second is not decoration: the field is only ever
        REFRESHED by a raider at the ring, so without the heartbeat a raid that
        was wiped out would leave a stale OPEN surging the bank into an empty
        battlefield -- the same failure `_cg_hold` guards with the same read.
        """
        if not FIN_ON:
            return False
        if self.fin_rnd == rnd:
            return self.fin_val
        self.fin_rnd = rnd
        self.fin_val = False
        try:
            beat = ct.read_store(CAGE_BEAT_SLOT) & COLLAR_BEAT_MASK
            if not beat or rnd - (beat - 1) > FIN_STALE:
                return False
            v = (ct.read_store(FIN_PUB_SLOT) >> FIN_PUB_SHIFT) & FIN_PUB_MASK
        except Exception:
            return False
        self.fin_val = (v == FIN_PUB_OPEN)
        return self.fin_val

    def _fin_live(self, ct, E, rnd):
        """Is the window open FOR THIS BODY?  Own eyes first, the store second.

        A raider standing on their ring has the fact first-hand and one round
        fresher than the store; anything else borrows the published copy.  Same
        split, same reason, as `_sge_core_band`.
        """
        if not FIN_ON:
            return False
        if E is not None:
            try:
                eyes = self._cg_eyes(ct, E)
            except Exception:
                eyes = False
            if eyes:
                # WAVE 12, ARM B.  The first-hand branch bypasses the store, so
                # it has to take the gate directly or an escort standing on a
                # seat would peck inside a window the publisher shut.  It is
                # asked BEFORE the census: with no evictor the answer cannot
                # be True and the 12-tile pass is not worth taking.
                if CAGE_EVGATE_FIN and not self._cg_evgate(ct, E, rnd):
                    return False
                n12, n8 = self._fin_seal(ct, E)
                return self._fin_ok(n12, n8, self.fin_open)
        return self._fin_window(ct, rnd)

    def _fin_seal_pending(self, ct, p, ti):
        """Is there SEAL WORK on a ring tile beside this body right now?

        The peck's own refusal, and it is the reason this arm cannot cost the
        cage anything: a brickable ring tile or one of our bricks below full HP
        beside this body outranks 2 damage by an order of magnitude (+4 HP per
        titanium of THEIR heal denied, against 2 damage for 2 Ti of ours).  The
        collar above would normally have taken it -- this test catches the
        rounds where it declined on budget rather than on merit.
        """
        keys = self.raid_ringkeys
        if not keys:
            return False
        try:
            cost = ct.get_barrier_cost()
        except Exception:
            cost = 3
        for dx, dy in CARD_DELTAS:
            k = (p.x + dx, p.y + dy)
            if k not in keys:
                continue
            t = Position(k[0], k[1])
            try:
                bid = ct.get_tile_building_id(t)
                if bid is not None:
                    if (ct.get_team(bid) == self.team
                            and ct.get_hp(bid) < ct.get_max_hp(bid)):
                        return True
                    continue
                if ti >= cost and ct.can_build_barrier(t):
                    return True
            except Exception:
                continue
        return False

    def _fin_peck(self, ct, E, p, ti, rnd):
        """PLANK FIN (b).  One escort action -> 2 damage on their Core.

        Zero cost scale, no ammunition, no cooldown beyond the action itself
        (engine_mechanics C), and inside the window their heal is ~0 -- so with
        two or three spare escorts this is +4-6 HP a round on top of tube fire,
        for titanium the ammunition pipe was not going to convert anyway.
        """
        if not (FIN_ON and FIN_PECK_ON) or E is None:
            return False
        if ti < FIN_PECK_TI_FLOOR:
            return False
        # WAVE 11, FIX 2.  MACRO ONLY.  The peck spends an ACTION, and its
        # premise -- "inside the window their heal is ~0, so 2 damage sticks"
        # -- only holds against an opponent that cannot answer with a body.
        # The wave-10 A/B priced the ungated version at -8.1 pp/game vs
        # mimic_juusto (p = 0.0013), which the detector reads as PRESSURE /
        # DEFAULT, at 116 Ti/game of pecks.  Same population as RAT_CAP_ONLY,
        # read from the same published detector verdict (slot 9, upper bits);
        # a read that fails is a REFUSAL, as everywhere else in this tree.
        if FIN_PECK_MACRO_ONLY:
            try:
                if self._archetype(ct) not in (ARCH_MACRO, ARCH_MACRO_WEAK):
                    return False
            except Exception:
                return False
        if not self._fin_live(ct, E, rnd):
            return False
        if self._fin_seal_pending(ct, p, ti):
            return False
        for c in core_tiles(E):
            if abs(p.x - c.x) + abs(p.y - c.y) != 1:
                continue
            try:
                if not ct.can_fire(c):
                    continue
                # WAVE 28, F6.
                if not self._f6_ok(ct, c):
                    continue
                ct.fire(c)
            except Exception:
                continue
            if FIN_LOG:
                print("FIN peck (%d,%d)" % (p.x, p.y))
            return True
        return False

    # --- PLANK RATCHET -----------------------------------------------------

    def _rat_live(self, ct, rnd):
        """RAT_CAP_ONLY: may the ratchet run against THIS opponent?

        The exploit is that a side at the 50-unit cap cannot respawn an evicted
        body, so the seat stays empty long enough for 3 Ti to close it.  Two
        ways to believe that, both already published and both read for free:
        the detector's MACRO / MACRO_WEAK verdict, and S5 -- the most enemy
        builders any of our bodies has seen at once near their Core (slot 13
        bits 21-25, saturating at 31).  Against a low-count opponent an evicted
        builder is respawned for nothing and we have paid a launcher action and
        a barrier for a shove.
        """
        if not RAT_ON:
            return False
        if self.rat_rnd == rnd:
            return self.rat_val
        self.rat_rnd = rnd
        if not RAT_CAP_ONLY:
            self.rat_val = True
            return True
        ok = False
        try:
            if self._archetype(ct) in (ARCH_MACRO, ARCH_MACRO_WEAK):
                ok = True
            elif ((ct.read_store(SLOT_ARCH_SEEN) >> 21) & 0x1F) >= RAT_CAP_N:
                ok = True
        except Exception:
            ok = False
        self.rat_val = ok
        return ok

    def _rat_theirs(self, ct, oid):
        """Is builder-bot id `oid` one of THEIRS?  Pessimistic on failure."""
        try:
            return ct.get_team(oid) != self.team
        except Exception:
            return False

    def _rat_bricker_by(self, ct, bp):
        """Is one of OUR builder bots orthogonally beside seat `bp`?

        This is the whole difference between a ratchet and a shove: the body
        standing here is the one that will poll `can_build_barrier` on the
        vacated tile on its next turn, and our launcher throws LATE in the
        round (high entity id), so the tile is already empty when that turn
        comes round.
        """
        for dx, dy in CARD_DELTAS:
            tx, ty = bp.x + dx, bp.y + dy
            if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                continue
            try:
                oid = ct.get_tile_builder_bot_id(Position(tx, ty))
                if oid is not None and ct.get_team(oid) == self.team:
                    return True
            except Exception:
                continue
        return False

    def _rat_stage_by(self, ct, s, launchers):
        """Is station `s` beside a SEATED enemy builder a launcher can reach?

        Cheap by construction: at most four tile reads, and only for stations
        that survived the ban / passability filters, and only while the ratchet
        gate is open at all.
        """
        keys = self.raid_seatkeys
        if not keys:
            return False
        for dx, dy in CARD_DELTAS:
            tx, ty = s.x + dx, s.y + dy
            if (tx, ty) not in keys:
                continue
            t = Position(tx, ty)
            reach = False
            for lp in launchers:
                if t.distance_squared(lp) <= RAT_STAGE_DSQ:
                    reach = True
                    break
            if not reach:
                continue
            try:
                oid = ct.get_tile_builder_bot_id(t)
            except Exception:
                continue
            if oid is not None and self._rat_theirs(ct, oid):
                return True
        return False

