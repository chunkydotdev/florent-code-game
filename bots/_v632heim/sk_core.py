"""SKALMAN v1 -- the CORE turn: the four-builder spawn plan and the drip.

ALL-NEW CODE.  Two verbs live here:

  SK_ROLES  COPY 8 -- exactly four builders, spawned r0-r3, never a fifth
                      while four live; a dead role body is REPLACED, not
                      supplemented.                       `_spawn_plan`
  SK_DRIP   COPY 7 -- the drip clock, implemented against the measured spec
                      verbatim.                           `_drip`
  SK_DOOR   COPY 6 -- the core is the SENSOR of the door verb: it publishes
                      the under-attack latch and the newest home threat, which
                      the home keeper answers and the turrets shoot.
                                                          `_threat_scan`
"""

from fcode import Direction, EntityType, Position

from sk_common import core_tiles_xy, dsq_core, pack_pos, pack_tile, unpack_pos
from sk_maps import (
    DIRECTIONS, SK_AMMO_FLOOR, SK_AMMO_GUNNER, SK_AMMO_SENTINEL, SK_BEAT_STALE,
    SK_DOOR, SK_DRIP, SK_HOME_RING_DSQ, SK_N_ROLES, SK_ROLES, SK_SLOT_BEAT,
    SK_SLOT_DRIP, SK_SLOT_ENEMY_CORE, SK_SLOT_SEATS, SK_SLOT_THREAT_POS,
    SK_SLOT_UNDER, TURRET_TYPES, enemy_core_for,
    SK_SPAWN_EXIT,
    SK_COREFIRE, SK_SLOT_COREFIRE, SK_DANGER_GUNNER_REACH,
    SK_DANGER_SENT_REACH,
    # --- v632 HEIMDALL PLANK 3 (THE TURRET RING) --------------------------
    SK_FORT_RING, SK_FORT_AMMO_BY, SK_FORT_AMMO_FLOOR,
    # --- v632 HEIMDALL -- THE FUNDING PRIORITY (SK_ROTATE_FUND) -----------
    SK_ROTATE, SK_ROTATE_FUND, SK_ROTATE_FUND_FROM, SK_ROTATE_FUND_KEEP,
    SK_ROTATE_WANT, SK_SLOT_NEST,
)
from sk_roles import (
    DRIP_GUN_MASK, DRIP_SENT_FIELD, SEAT_MASK,
    CF_HIT_MASK, CF_TILE_FIELD, CF_TILE_MASK, CF_HP_FIELD, CF_HP_MASK,
    CF_HP_UNIT, CF_SENT_BIT, CF_RAY_BIT,
)


def lattice_floor(n):
    """The largest sum of 4s and 10s not exceeding n.

    COPY 7's acceptance test is that >= 97.3% of converted amounts are exact
    sums of 4s and 10s -- "a drip implementation that does not produce a 4/10
    lattice is not implementing the drip".  Every such sum is even and no odd
    value is reachable, so a deficit we cannot fully afford is floored ONTO the
    lattice rather than converted raw.
    """
    if n < 4:
        return 0
    if n < 8:
        return 4
    return n - (n & 1)


class CoreMixin:

    def _core(self, ct):
        p = ct.get_position()
        w, h = ct.get_map_width(), ct.get_map_height()
        self.mw, self.mh = w, h
        if self.team is None:
            self.team = ct.get_team()
        if self.core is None:
            self.core = p
        self._load_grid(ct)
        # slot 3 is the ONE slot convention carried over from the benchmark:
        # the whole map layer is written against pack_pos(enemy core).
        if ct.read_store(SK_SLOT_ENEMY_CORE) == 0:
            self.wstore(ct, SK_SLOT_ENEMY_CORE, pack_pos(enemy_core_for(w, h, p)))
        if self.enemy is None:
            self.enemy = enemy_core_for(w, h, p)

        rnd = ct.get_current_round()
        home_guns, home_sents = self._threat_scan(ct, p, rnd)
        self._corefire_report(ct, p, rnd)          # v608 SENSOR

        # ⭐⭐ v632 HEIMDALL PLANK 3 -- THE AMMO CLOCK, ABOVE THE DRIP.
        # `convert_ammo` is at most ONCE PER TEAM PER TURN, so the two
        # converters must not both try in the same round: the bank runs first
        # and the drip is skipped on any round the bank spent the conversion.
        # ⛔ THAT SKIP IS FREE INSIDE THE BANK'S WINDOW: the drip is
        # need-based off turrets that ALREADY EXIST, and the earliest ring
        # turret is SK_FORT_RING_WINDOW[0] = r6, i.e. after the bank has
        # finished -- so on r1..SK_FORT_AMMO_BY the drip's `need` is 0 for the
        # ring by construction.
        banked = False
        if SK_FORT_RING:
            banked = self._fort_ammo_bank(ct, rnd)
        if SK_DRIP and not banked:
            self._drip(ct, rnd, home_guns, home_sents)

        self._spawn_plan(ct, p, rnd)

    # ------------------------------------------------------------------
    # COPY 6 -- the sensor half of the door verb (writer: CORE, slots 1 & 2)
    # ------------------------------------------------------------------

    def _threat_scan(self, ct, p, rnd):
        """One pass over the core's r^2=36 vision.

        Publishes: the under-attack latch (slot 1) and the newest home threat
        (slot 2), which is what makes ledger V5's "am I losing?" gate possible
        at all -- the denial roles read it and yield.

        Returns (home gunners, home sentinels) that WILL FIRE next round --
        COPY 7's `need`, home half.  A turret "will fire" when a hostile sits
        inside its own attack reach; that is the cheapest honest predicate the
        core can evaluate, and it is why the drip is need-based rather than a
        standing balance.
        """
        guns = sents = 0
        threat = None
        try:
            ids = ct.get_nearby_entities()
        except Exception:
            return 0, 0
        enemies = []
        friends = []
        for eid in ids:
            try:
                t = ct.get_team(eid)
                et = ct.get_entity_type(eid)
                ep = ct.get_position(eid)
            except Exception:
                continue
            if t == self.team:
                friends.append((et, ep))
            else:
                enemies.append((et, ep))
                if et == EntityType.BUILDER_BOT or et in TURRET_TYPES or et == EntityType.BARRIER:
                    d = dsq_core(ep, p)
                    if threat is None or d < threat[0]:
                        threat = (d, ep)
        for et, ep in friends:
            if et not in TURRET_TYPES:
                continue
            reach = 13 if et == EntityType.GUNNER else 32
            for _et, epos in enemies:
                if ep.distance_squared(epos) <= reach:
                    if et == EntityType.GUNNER:
                        guns += 1
                    else:
                        sents += 1
                    break
        if threat is not None and threat[0] <= SK_HOME_RING_DSQ * 3:
            self.beat(ct, SK_SLOT_UNDER, rnd)
            if SK_DOOR:
                self.wstore(ct, SK_SLOT_THREAT_POS, pack_pos(threat[1]))
        return guns, sents

    # ------------------------------------------------------------------
    # v608 SENSOR -- SK_COREFIRE (writer: CORE, slot 15)
    # ------------------------------------------------------------------

    def _corefire_report(self, ct, p, rnd):
        """Publish "our core is being shot", and by what, on SK_SLOT_COREFIRE.

        ⛔ THE ALARM IS THE DAMAGE, NOT THE SHOOTER, and that ordering is the
        whole design.  The v607 anatomy's 19/19 channel is enemy SENTINEL fire,
        and a sentinel firing at a core TILE may sit at d^2 50 of the core
        ANCHOR (d^2 <= 32 measured to the far footprint corner, on a diagonal)
        -- i.e. OUTSIDE the core's own r^2=36 vision.  So the shooter tile is a
        best-effort extra and every consumer degrades to "heal" without it.
        What is never in doubt is `get_hp()` on ourselves.

        ⛔ WHY THE CORE AND NOT A BUILDER.  A builder can only INFER that the
        core is under fire (this is what `_infer_killer` does for harvesters,
        and it says so: "THIS IS AN INFERENCE, NOT AN OBSERVATION").  The core
        reads its own HP every round for free.  One writer, one slot.
        """
        if not SK_COREFIRE:
            return
        try:
            hp = ct.get_hp()
        except Exception:
            return
        prev = self.core_hp_prev
        self.core_hp_prev = hp
        if prev is not None and hp < prev:
            self.corefire_last = rnd
        shooter = self._corefire_shooter(ct, p, rnd)
        word = 0
        if self.corefire_last >= 0:
            word |= (self.corefire_last + 1) & CF_HIT_MASK
        if shooter is not None:
            word |= (pack_tile(shooter[0]) & CF_TILE_MASK) << CF_TILE_FIELD
            if shooter[1]:
                word |= CF_SENT_BIT
            if shooter[2]:
                word |= CF_RAY_BIT
        h = hp // CF_HP_UNIT
        if h < 0:
            h = 0
        elif h > CF_HP_MASK:
            h = CF_HP_MASK
        word |= (h & CF_HP_MASK) << CF_HP_FIELD
        self.wstore(ct, SK_SLOT_COREFIRE, word)

    def _corefire_shooter(self, ct, p, rnd):
        """(Position, is_sentinel, ray_confirmed) of the enemy turret bearing on
        our footprint, or None.  Latched: a turret is a BUILDING and cannot move.

        Ordering: a ray-confirmed SENTINEL, then a ray-confirmed gunner, then
        (facing unreadable) any enemy sentinel whose REACH covers a core tile.
        The third rung is disclosed as weaker than the first two -- it is the
        19/19 prior standing in for a facing we could not read -- and it is why
        the consumers that SPEND (the counter-battery) also require the alarm to
        have been continuously fresh for SK_COUNTER_RNDS.
        """
        foot = core_tiles_xy(self.core if self.core is not None else p)
        best = None                       # (rank, dsq, Position, is_sent)
        try:
            ids = ct.get_nearby_entities()
        except Exception:
            ids = []
        for eid in ids:
            try:
                if ct.get_team(eid) == self.team:
                    continue
                et = ct.get_entity_type(eid)
            except Exception:
                continue
            if et not in TURRET_TYPES:
                continue
            try:
                ep = ct.get_position(eid)
            except Exception:
                continue
            sent = et != EntityType.GUNNER
            reach = SK_DANGER_SENT_REACH if sent else SK_DANGER_GUNNER_REACH
            f = None
            try:
                f = ct.get_direction(eid).delta()
            except Exception:
                f = None
            rank = None
            if f is not None and (f[0] or f[1]):
                dx, dy = f
                k = 1
                while k * k * (dx * dx + dy * dy) <= reach:
                    if (ep.x + dx * k, ep.y + dy * k) in foot:
                        rank = 0 if sent else 1
                        break
                    k += 1
            if rank is None and sent:
                for (cx, cy) in foot:
                    ax, ay = cx - ep.x, cy - ep.y
                    if ax * ax + ay * ay <= reach:
                        rank = 2
                        break
            if rank is None:
                continue
            d = dsq_core(ep, self.core if self.core is not None else p)
            cand = (rank, d, ep, sent)
            if best is None or (cand[0], cand[1]) < (best[0], best[1]):
                best = cand
        if best is not None:
            self.cf_shooter = (best[2], best[3], best[0] <= 1)
            self.cf_shooter_rnd = rnd
            return self.cf_shooter
        # Nothing found this round: keep the latch unless we can SEE the
        # remembered tile is now clear of enemy buildings.  A turret is
        # immovable, so "not visible" is not "not there".
        held = self.cf_shooter
        if held is None:
            return None
        q = held[0]
        try:
            if ct.is_in_vision(q) and self.ibp(q):
                bid = ct.get_tile_building_id(q)
                if bid is None or ct.get_team(bid) == self.team:
                    self.cf_shooter = None
                    return None
        except Exception:
            pass
        return held

    # ------------------------------------------------------------------
    # COPY 7 -- THE DRIP CLOCK
    # ------------------------------------------------------------------

    def _drip(self, ct, rnd, home_guns, home_sents):
        """COPY 7, the measured spec, implemented as written:

            EVERY ROUND, at the core:
                need = 4 * (live gunners that will fire next round)
                     + 10 * (live sentinels that will fire next round)
                if need > current_ammo and can_convert_ammo(need - current_ammo):
                    convert_ammo(need - current_ammo)

        Calibration this is built to hit: first convert on the round the first
        turret exists (median r27.5) and NEVER at r0 (the field's median is
        r1.0 -- that is the behaviour this replaces); ~67 calls a game; peak
        balance held around 26, about two sentinel shots; NEVER BANK.

        Forward turrets are outside the core's vision, so their count arrives
        on slot 8 from the siege engineer (one writer, one slot).

        LEDGER V10: `SK_AMMO_FLOOR` is the NAMED floor -- one sentinel shot of
        cushion, so a cost-scale shock or a burst of repairs cannot silently
        cancel next round's shots.  It is a trade-off, not a bug: the drip is
        why nothing is idle.

        ⚠ Do NOT build the reverse.  There is no Controller getter for an
        opponent's ammunition or conversions; `CoreConvertAmmo` is a replay
        event and a scouting instrument only.
        """
        if rnd <= 0:
            return                              # NEVER at r0
        drip = ct.read_store(SK_SLOT_DRIP)
        fwd_guns = drip & DRIP_GUN_MASK
        fwd_sents = (drip >> DRIP_SENT_FIELD) & DRIP_GUN_MASK
        need = (SK_AMMO_GUNNER * (home_guns + fwd_guns)
                + SK_AMMO_SENTINEL * (home_sents + fwd_sents))
        if need <= 0:
            return
        need += SK_AMMO_FLOOR                   # V10 cushion
        ammo = ct.get_global_ammo()
        if need <= ammo:
            return
        amt = need - ammo
        have = ct.get_global_resources()
        if amt > have:
            amt = have
        # ⭐⭐ v632 THE FUNDING PRIORITY (SK_ROTATE_FUND) -- THE DRIP YIELDS.
        # The drip is the LARGEST measured drain in the pre-flip window and
        # nothing gated it; inside the funding window it converts ONLY the
        # surplus above one sentinel's purchase price.  ⛔ IT IS A CLAMP, NOT A
        # SKIP: every titanium above the floor is still converted the same
        # round, so a standing turret keeps being fed out of surplus and only
        # the money the battery needs is withheld.  `_fund_floor` returns 0 --
        # i.e. this block is a no-op -- on every SK_ROTATE-off round, outside
        # the window, once the battery reaches SK_ROTATE_WANT, on any round a
        # tube STANDS and the team holds under one sentinel shot (the
        # shoot-what-stands yield, amendment 2), and on any unreadable number.
        floor = self._fund_floor(ct, rnd)
        if floor > 0:
            room = have - floor
            if room < 0:
                room = 0
            if room < amt:
                amt = room
                self.fund_drip_held += 1
        # ⭐ v602 FIX 6 (the v601 build report's named one-liner).  The floor was
        # applied ONLY on the can't-afford branch, so 2 of 63 conversions in the
        # v601 tape left the 4/10 lattice -- both of them amount 6 on that very
        # branch, where `need - ammo` had already been clamped.  COPY 7's
        # acceptance test is that >= 97.3% of converted amounts are exact sums of
        # 4s and 10s; applying the floor UNCONDITIONALLY makes it 100% by
        # construction.  A 2 Ti shortfall is re-evaluated next round -- the drip
        # runs every round and never banks.
        amt = lattice_floor(amt)
        if amt <= 0:
            return
        try:
            if ct.can_convert_ammo(amt):
                ct.convert_ammo(amt)
                self.converts += 1
        except Exception:
            return

    # ------------------------------------------------------------------
    # v632 HEIMDALL -- THE FUNDING PRIORITY  (SK_ROTATE_FUND)
    # ------------------------------------------------------------------

    def _fund_battery(self, ct, rnd):
        """How many battery tubes stand right now -- the BEST AVAILABLE read,
        and its two biases are stated because neither is exact.

        GAME CONTEXT: an in-engine census of our own sentinels in the Florent
        Code League's simulated grid.

        TWO SOURCES, and the answer is their MAX because each fails LOW in a
        different place and neither can be trusted alone:
          * SLOT 8 (`SK_SLOT_DRIP`, writer: the siege engineer) -- forward
            sentinels that WILL FIRE next round.  6 bits, so it can reach 4;
            it is the read `_drip` already performs, so in the drip's own path
            it costs nothing new.  ⚠ FAILS LOW twice: it counts only tubes
            inside the ENGINEER'S vision (`_drip_report` discloses this) and
            only those with an enemy in reach.  During a clustered siege at
            their core both hold in practice -- SK_ROTATE_CLUSTER_GAP puts the
            whole battery in one vision disc and their core is itself an enemy
            entity in reach -- which is exactly the phase this gate runs in.
          * SLOT 7 (`SK_SLOT_NEST`) -- the phase-separated forward-tube BEATS,
            counted by `_tube_count`.  Standing tubes, not firing ones, so it
            is live when slot 8 is not.  ⚠ FAILS LOW HARD: the slot holds
            exactly TWO seats, so it SATURATES AT 2 and can never on its own
            report a battery of SK_ROTATE_WANT = 4.  This is the same slot
            re-lay SK_ROTATE_WANT's note already books as a separate plank.

        ⛔ THE FAILURE DIRECTION, STATED: reading LOW keeps the funding
        priority engaged LONGER than nominal -- more titanium held liquid, the
        drip clamped for more rounds.  Reading HIGH (slot 8 also counts
        forward tubes this plank did not plant) reverts the gate EARLY, i.e.
        the plank does less.  Both are bounded and neither can refuse a plant:
        nothing in this family ever blocks `build_sentinel`.
        """
        n = 0
        try:
            n = (ct.read_store(SK_SLOT_DRIP) >> DRIP_SENT_FIELD) & DRIP_GUN_MASK
        except Exception:
            n = 0
        try:
            t = self._tube_count(ct.read_store(SK_SLOT_NEST), rnd)
        except Exception:
            t = 0
        return t if t > n else n

    def _fund_floor(self, ct, rnd):
        """The titanium that must stay liquid this round, or 0 for "no floor".

        One sentinel's LIVE price plus SK_ROTATE_FUND_KEEP, read through
        `get_sentinel_cost()` because the ONE GLOBAL ADDITIVE cost scale is
        near its maximum by r285.

        `SK_ROTATE and SK_ROTATE_FUND` is the CALL-SITE CONJUNCTION that makes
        OFF an exact identity, and it is doubly guaranteed: the master ships
        False AND is reachable only under SK_ROTATE, which also ships False.
        Cheapest terms first, so an OFF arm returns before touching the
        controller and the store is never read.

        ⛔⛔ THE SHOOT-WHAT-STANDS YIELD, AND IT IS THIS BUILD'S OWN MEASURED
        DEADLOCK (amendment registered
        `docs/research/EXPECTATION-v632heim-fund-2026-08-23.md`, pre-tape,
        blind).  The first build of this clamp held the floor whenever the
        battery was short of SK_ROTATE_WANT, full stop.  On a POOR cell that is
        a closed loop: jotunheim measured `ammo == 0` in **201 of 201** window
        rounds (the unclamped control: 144/201, peak 20) -- income never
        cleared `cost + KEEP`, so nothing converted, the ONE tube that did
        stand never fired, and a battery that cannot shoot cannot grow to the
        count that would release the clamp.
        ⇒ ONCE AT LEAST ONE TUBE STANDS AND THE TEAM HOLDS LESS THAN ONE
        SENTINEL SHOT (SK_AMMO_SENTINEL), THE FLOOR LIFTS FOR THAT ROUND.
        Plant first, then shoot with what stands.  The deadlock cannot recur by
        construction: the yield's precondition is exactly the state the
        deadlock consists of.
        ⚠ THE YIELD IS THE DRIP'S ALONE.  `_fund_refuse` (the keeper's 1-2 Ti
        verbs) does NOT carry it -- those verbs do not buy ammunition, so
        releasing them would spend the same titanium on something that cannot
        end the deadlock.

        ⛔ FAILS OPEN, for `_chest_refuse`'s reason: a floor built on an
        unreadable cost withholds titanium for no measured reason, which is
        worse than the overspend it was meant to prevent.
        """
        if not (SK_ROTATE and SK_ROTATE_FUND and rnd >= SK_ROTATE_FUND_FROM):
            return 0
        try:
            batt = self._fund_battery(ct, rnd)
            if batt >= SK_ROTATE_WANT:
                return 0
            if batt >= 1 and ct.get_global_ammo() < SK_AMMO_SENTINEL:
                return 0                       # shoot with what stands
            return ct.get_sentinel_cost() + SK_ROTATE_FUND_KEEP
        except Exception:
            return 0

    def _fund_refuse(self, ct, rnd):
        """True when a KEEPER DISCRETIONARY 1-2 Ti verb must stand down.

        The measured target: `_peck_priority` (2 Ti a peck) and `_heal_action`
        (1 Ti a heal) together drained 38-44 Ti across the window -- half a
        sentinel, two titanium at a time, and neither passes through the war
        chest.

        THE TEST IS THE SPEC'S, VERBATIM: refuse while
        `bank < get_sentinel_cost() + SK_ROTATE_FUND_KEEP`.
        ⚠ DISCLOSED DIFFERENCE FROM `_chest_refuse`: the chest adds the
        purchase's OWN cost to the reserve; this does not, because the verbs it
        gates cost 1-2 Ti against a KEEP margin of 10 -- the margin already
        covers several of them and threading a cost argument through two call
        sites would buy nothing measurable.

        ⛔⛔ THE EXEMPTION IS `corefire_fresh`, NOT `_under_attack`, AND THE
        NARROWING IS THIS BUILD'S OWN MEASUREMENT (amendment registered
        `docs/research/EXPECTATION-v632heim-fund-2026-08-23.md`, pre-tape,
        blind).  The chest's exemption is the slot-1 PRESENCE latch
        (SK_SLOT_UNDER, 50-round freshness) and this method shipped with it for
        one build cycle.  A reachability tap at the gated rung then measured
        that latch FRESH IN 139 OF 139 keeper-rung rounds in [275, 350] across
        three cells (jotunheim 76/76, valkyrie 51/51, longhouse 12/12), with
        the bank below the floor in 84 of them -- i.e. the exemption swallowed
        the mechanism WHOLE, and `fund_verb_held` read 0 in play.  That it is
        the mechanism and not the gate was proven by a mutation control with
        the exemption removed: **848 refusals on jotunheim, 4 on longhouse, and
        0 on valkyrie** -- the rich cell producing the other verdict on the same
        call.  ⇒ THE SAME CAUSE THE WAR CHEST WAS MEASURED INERT BY
        (`chest_blocked == 0` in play, RO-P), which is why the fix is a
        NARROWING rather than a removal.
        `corefire_fresh` is the CORE's own HP-DELTA latch (slot 15, published
        by `_corefire_report`, `SK_COREFIRE_TTL` freshness): our core has
        ACTUALLY LOST HP recently, not merely "something hostile stands near
        home".  DEFENCE FIRST is preserved on the signal that means the core is
        dying; a keeper answering real core damage pecks and heals exactly as
        before.  ⚠ DISCLOSED: with SK_COREFIRE off the word reads 0 and this
        exemption never fires, so the gate is strictly tighter on such an arm.

        ⚠ WHAT THE COUNTER MEANS, STATED SO IT IS NOT OVER-READ:
        `fund_verb_held` counts ROUNDS THE RUNG WAS REFUSED, which is an UPPER
        BOUND on turns actually diverted -- the refusal is evaluated before the
        verb looks for a target, so a round with nothing to peck still counts.
        It is a reachability witness and a dose ceiling, not a dose.
        """
        if not (SK_ROTATE and SK_ROTATE_FUND and rnd >= SK_ROTATE_FUND_FROM):
            return False
        try:
            if self.corefire_fresh(ct, rnd):
                return False
            if self._fund_battery(ct, rnd) >= SK_ROTATE_WANT:
                return False
            if ct.get_global_resources() >= (ct.get_sentinel_cost()
                                             + SK_ROTATE_FUND_KEEP):
                return False
        except Exception:
            return False
        self.fund_verb_held += 1
        return True

    # ------------------------------------------------------------------
    # v632 HEIMDALL PLANK 3 -- THE AMMO CLOCK (SK_FORT_RING)
    # ------------------------------------------------------------------

    def _fort_ammo_bank(self, ct, rnd):
        """Bank SK_FORT_AMMO_FLOOR ammunition BY r SK_FORT_AMMO_BY.  True iff
        it spent this round's one conversion.

        GAME CONTEXT: an in-engine resource conversion in the Florent Code
        League; "kill" below is the engine's stated removal of a competing
        bot's piece.

        ⭐⭐ WHY A SECOND CONVERTER EXISTS AT ALL, AND IT IS THE PREDICTION
        STUDY'S METRONOME (banked s57, coordination tail ~20:2xZ): THEIR LADDER
        LANDS r1-r5, THE FIRST PLANT IN OUR HALF AT MEDIAN r5, THE COLLAR AT
        MEDIAN r11.  The ring's first turret can stand at r6
        (SK_FORT_RING_WINDOW) -- and `_drip` CANNOT PRE-FUND IT: the drip is
        need-based off turrets that ALREADY EXIST and it NEVER BANKS, so on the
        round the first ring turret is bought the balance is 0 and the turret
        is silent until the drip catches up a round later.  ⛔ SILENT IS THE
        BEST CASE: `can_fire` returns TRUE at 0 ammo and the engine RAISES
        inside finish_firing_turret, which would permanently destroy our own
        turret -- `_turret`'s balance guard is what turns that into silence.
        A gun that cannot shoot on the round the raider arrives is the whole
        plank missing its window.

        ⛔ THIS IS NOT A CHANGE TO `SK_AMMO_FLOOR` and must not become one:
        that constant was swept to 20/30 and is monotonically WORSE
        (sk_maps.py:2442-2461).  This is a ONE-TIME EARLY BANK inside
        r1..SK_FORT_AMMO_BY, after which the need-based drip is again the only
        converter and the standing-balance behaviour is unchanged.

        SIZE: SK_FORT_AMMO_FLOOR = 30 = one sentinel intruder-kill (study §5c:
        3 shots x 18 dmg vs a 40 HP builder, 10 ammo each), which is also
        6 gunner shots' worth minus one.  Exactly on the 4/10 lattice.
        """
        if rnd <= 0 or rnd > SK_FORT_AMMO_BY:
            return False                        # NEVER at r0 (the drip's rule)
        try:
            ammo = ct.get_global_ammo()
        except Exception:
            return False
        if ammo >= SK_FORT_AMMO_FLOOR:
            return False
        amt = SK_FORT_AMMO_FLOOR - ammo
        try:
            have = ct.get_global_resources()
        except Exception:
            return False
        if amt > have:
            amt = have
        # The 4/10 lattice, floored -- `_drip`'s v602 FIX 6 rule applied
        # unconditionally so a partial bank cannot leave the lattice either.
        amt = lattice_floor(amt)
        if amt <= 0:
            return False
        try:
            if not ct.can_convert_ammo(amt):
                return False
            ct.convert_ammo(amt)
        except Exception:
            return False
        self.converts += 1
        self.fort_ammo_banked += amt
        return True

    # ------------------------------------------------------------------
    # COPY 8 -- the four-builder cap
    # ------------------------------------------------------------------

    def _spawn_plan(self, ct, p, rnd):
        """Exactly four builders, spawned r0-r3, and never a fifth while four
        live (their measured shape: exactly 4 in 104/112 games, the fourth at
        r3, and in the modal game zero deaths and zero replacements).

        Liveness comes from the four role beats (slots 10-13), so a dead role
        is re-staffed by the next spawn rather than by inventing a fifth job:
        the replacement claims the stale role in `_claim_role`.

        `self.spawned - seats` is the IN-FLIGHT term: a builder spawned this
        round has not claimed its seat yet, and without it the core would spawn
        a second body for the same empty role next round.
        """
        if ct.get_action_cooldown() != 0:
            return
        cost = ct.get_builder_bot_cost()
        if ct.get_global_resources() < cost:
            return
        live = 0
        for r in range(SK_N_ROLES):
            if self.beat_fresh(ct, SK_SLOT_BEAT[r], rnd, SK_BEAT_STALE):
                live += 1
        seats = ct.read_store(SK_SLOT_SEATS) & SEAT_MASK
        in_flight = self.spawned - seats
        if in_flight < 0:
            in_flight = 0
        want = SK_N_ROLES if SK_ROLES else SK_N_ROLES
        if live + in_flight >= want:
            return
        if ct.get_unit_count() >= 50:
            return
        # ⭐ v603 FIX 6(c) -- NEVER SPAWN INTO A ZERO-EXIT TILE.  v602 took the
        # first direction `can_spawn` accepted, and the s54 lap diagnosis found
        # two bodies born into a box of enemy buildings and our own footprint:
        # stavkirke_B body 58 made 0 moves in 860 rounds, icefloe_A body 218 in
        # 227.  `can_spawn` is a legality test, not a liveness test.  TWO PASSES,
        # and the second is unconditional -- a body with no exit still beats no
        # body at all when every adjacent tile is boxed (it can still peck out,
        # v603 FIX 6(b)), so this ORDERS the choice, it never vetoes the spawn.
        for require_exit in (True, False):
            for d in DIRECTIONS:
                q = p.add(d)
                if not self.ib(q.x, q.y):
                    continue
                try:
                    if not ct.can_spawn(q):
                        continue
                except Exception:
                    continue
                if SK_SPAWN_EXIT and require_exit:
                    if self.free_neighbours(ct, q) == 0:
                        continue
                try:
                    ct.spawn_builder(q)
                except Exception:
                    continue
                self.spawned += 1
                return
            if not SK_SPAWN_EXIT:
                return
