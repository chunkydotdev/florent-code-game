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

from fcode import Direction, EntityType, GameConstants, Position

from sk_common import core_tiles_xy, dsq_core, pack_pos, pack_tile, unpack_pos
from sk_maps import (
    DIRECTIONS, SK_AMMO_FLOOR, SK_AMMO_GUNNER, SK_AMMO_SENTINEL, SK_BEAT_STALE,
    SK_DOOR, SK_DRIP, SK_HOME_RING_DSQ, SK_N_ROLES, SK_ROLES, SK_SLOT_BEAT,
    SK_SLOT_DRIP, SK_SLOT_ENEMY_CORE, SK_SLOT_SEATS, SK_SLOT_THREAT_POS,
    SK_SLOT_UNDER, TURRET_TYPES, enemy_core_for,
    SK_SPAWN_EXIT,
    SK_COREFIRE, SK_SLOT_COREFIRE, SK_DANGER_GUNNER_REACH,
    SK_DANGER_SENT_REACH,
    # --- s57 THE SENTRY, PIECE 1 (SK_SENTRY_ALARM) ------------------------
    SK_SENTRY, SK_SENTRY_ALARM, SK_SENTRY_DSQ, SK_SENTRY_ARM_MAX,
    # --- v632 HEIMDALL PLANK 3 (THE TURRET RING) --------------------------
    SK_FORT_RING, SK_FORT_AMMO_BY, SK_FORT_AMMO_FLOOR,
    # --- v632 HEIMDALL -- THE FUNDING PRIORITY (SK_ROTATE_FUND) -----------
    SK_ROTATE, SK_ROTATE_FUND, SK_ROTATE_FUND_FROM, SK_ROTATE_FUND_KEEP,
    SK_ROTATE_WANT, SK_SLOT_NEST,
    # --- s57 LEVER 1 -- THE CONVERSION POLICY (SK_AMMO_PUSH) --------------
    SK_AMMO_PUSH, SK_AMMO_PUSH_BANK, SK_AMMO_PUSH_MAX, SK_AMMO_PUSH_RESERVE,
    # --- s57 THE KILLBOX, ARM 3 (THE SPEED / LOGISTICS PACKAGE) -----------
    SK_KILLBOX, SK_KB_CELL, SK_KILLBOX_FAST, SK_KB_FAST_SPAWN_DIR,
    SK_KB_FAST_SPAWN, SK_KB_FAST_SPAWN_N, SK_KB_FAST_SPAWN_BY,
    # --- s57 THE PUSH v3, PIECE 2b -- the warden as an ADDITIONAL body ------
    SK_PUSH, SK_PUSH_WARDEN2, SK_PUSH_W2_N, SK_PUSH_W2_FLOOR,
    # --- s57 SK_DOCTRINE: the trigger and the burst conversion --------------
    SK_DOCTRINE, SK_DOC_BANK, SK_DOC_TRIGGER_LATCH, SK_DOC_LATCH_ONCE,
    SK_DOC_WALL_N, SK_DOC_WALL_DSQ,
    SK_DOC_AMMO, SK_DOC_AMMO_MAX, SK_DOC_ANSWER_RESERVE, SK_DOC_CONVERT,
    SK_BATTERY2, SK_BATTERY2_ECO,
    # --- s57 SK_DOCTRINE, TAIL C: FUNDED / RATE / STABILITY + the re-arm ----
    SK_DOC_TAIL_A, SK_DOC_FUND_HOLD, SK_DOC_RATE, SK_DOC_RATE_PASSIVE,
    SK_DOC_PASSIVE_RATE, SK_DOC_STABLE, SK_DOC_STABLE_RNDS,
    SK_DOC_REARM, SK_DOC_REARM_RNDS, SK_DOC_REARM_TUBES,
    SK_BATTERY2_ECO_LIFE,
)
from sk_roles import (
    DRIP_GUN_MASK, DRIP_SENT_FIELD, SEAT_MASK,
    CF_HIT_MASK, CF_TILE_FIELD, CF_TILE_MASK, CF_HP_FIELD, CF_HP_MASK,
    CF_HP_UNIT, CF_SENT_BIT, CF_RAY_BIT, CF_SENTRY_BIT, CF_DOC_BIT,
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
        # ⭐⭐ s57 SK_DOCTRINE -- THE TRIGGER, EVALUATED ON THE CORE AND
        # EVALUATED **ABOVE** THE PUBLISH SO THE LATCH IS ON THE WIRE THE ROUND
        # IT FIRES rather than the round after.
        # ⛔ WHY THE CORE OWNS THIS.  The income sampler `_b2_sample` refuses
        # any gap other than exactly one round (it will not average over a hole
        # it cannot see), and its adopted host -- the siege engineer -- does not
        # exist as a running turn in phase 1 under this doctrine and restarts
        # its ring on every engineer turnover.  The core runs every round, for
        # the whole match, and cannot die without the match ending; it reads
        # `get_global_resources()` and `get_global_ammo()` for free.  ONE
        # SAMPLER, ONE WRITER, ONE LATCH.
        # ⛔ IT DOES NOT DISTURB THE ENGINEER'S OWN SAMPLER: `batt2_*` are
        # per-`Player`-instance and every unit gets its own instance, so the
        # core's ring and the engineer's ring are different objects.
        # ⛔ SK_DOCTRINE False -> one module-constant test, zero engine calls.
        self._doc_trigger(ct, rnd)
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
        # ⭐ s57 LEVER 1 (SK_AMMO_PUSH) -- THE THIRD CONVERTER, BETWEEN THE
        # BANK AND THE DRIP, and the ordering is the same one-conversion-per-
        # team-per-turn rule the bank already obeys.  It returns True only on a
        # round it actually spent that conversion for at least what the drip
        # would have spent, so the drip below is skipped only when it has been
        # SUBSUMED, never when it has been OVERRULED.  OFF: the flag is the
        # first term, so an OFF arm makes no call and reads no store.
        if SK_AMMO_PUSH and not banked:
            banked = self._ammo_push(ct, rnd, home_guns, home_sents)
        _conv_before = self.converts
        if SK_DRIP and not banked:
            self._drip(ct, rnd, home_guns, home_sents)
        # ⭐⭐ s57 SK_DOCTRINE -- THE BURST CONVERSION, AND IT IS THE **LAST**
        # CONVERTER IN THE ROUND.  `convert_ammo` is at most once per team per
        # turn; the drip is NEED-BASED off turrets that already exist and never
        # banks, this rung BANKS toward SK_DOC_AMMO.  NEED OUTRANKS BANK, so
        # the drip is asked first and this rung runs only on a round the drip
        # did not spend the conversion.
        # ⛔ THAT ORDERING IS WHY NO `_drip` ARITHMETIC IS DUPLICATED HERE.
        # SK_AMMO_PUSH sits ABOVE the drip and therefore has to reason about
        # SUBSUMING it (its own note: "it returns True only on a round it
        # actually spent that conversion for at least what the drip would have
        # spent"); a rung placed BELOW cannot overrule anything and needs no
        # such argument, and there is no second copy of `need` to drift.
        # ⛔ THE DETECTOR IS `self.converts`, THE DRIP'S OWN COUNTER, READ
        # ACROSS THE CALL -- not a return value, so `_drip` is untouched.
        # ⛔ SK_DOCTRINE False -> the snapshot is one attribute read and the
        # call returns on its first line; zero engine calls, and the drip above
        # is character-for-character the adopted one.
        # ⛔ BOTH TERMS ARE REQUIRED.  `banked` covers the two converters ABOVE
        # the drip (the ring's ammo clock and SK_AMMO_PUSH), which skip the drip
        # entirely and would leave `self.converts` unchanged; the counter
        # comparison covers the drip itself.  Either alone lets a second
        # `convert_ammo` be attempted in one team-turn.
        if not banked and self.converts == _conv_before:
            self._doc_convert(ct, rnd)

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
        # ⭐⭐ s57 THE SENTRY, PIECE 1 -- THE PRESENCE BIT, AND IT IS A BIT AND
        # NOT A SECOND ROUND-STAMP ON PURPOSE.
        # ⛔⛔ THE FIRST DRAFT OF THIS BLOCK PUBLISHED `max(damage, presence)`
        # INTO THE b0-10 HIT FIELD AND WAS WRONG, and it is written down here
        # because the error is invisible from the call sites: b0-10 is what
        # `corefire_fresh` reads, `corefire_fresh` has FIFTEEN consumers, and
        # only some of them dispatch an ANSWER.  A presence stamp in that field
        # silently hands the earlier trigger to the medic, the heal-stand, the
        # push-quiet gate and the recall as well -- planks whose bars were
        # measured against the DAMAGE latch.  So the presence latch gets its own
        # bit, `answer_fresh` is the only reader that ORs it in, and the swap
        # list in the build report is exactly the set of consumers affected.
        # ⛔ THE BIT IS THE LATCH: the core republishes it EVERY round, so it is
        # never more than one round stale and it goes to 0 the round the threat
        # dies or its episode runs out (`_sentry_commit`, the #132 expiry).  No
        # TTL is needed and none is applied.
        if SK_SENTRY and SK_SENTRY_ALARM and self.sentry_last == rnd:
            word |= CF_SENTRY_BIT
        # ⭐⭐ s57 SK_DOCTRINE -- THE BURST LATCH ON b31, THE LAST FREE BIT OF
        # THE LAST FREE SLOT.  It rides here for the same three reasons b30
        # does: the core is the ONE writer of this word, the word is written
        # WHOLE every round (never a read-modify-write, so no buffered-write
        # lost update is possible), and every existing consumer reads its own
        # field and is blind to a new bit.
        # ⛔ RE-PUBLISHED EVERY ROUND, so a body spawned at r400 reads the
        # phase on its first turn instead of re-deriving it from a bank the
        # burst has already drawn down.
        # ⛔ THE PUBLISH IS ONE-WAY BECAUSE THE LATCH IS (SK_DOC_LATCH_ONCE);
        # with that flag off `doc_fired` is re-derived each round and this bit
        # follows it in both directions, which is the ablation.
        # ⚠ DEPENDENCY, STATED: this method returns on `not SK_COREFIRE` above,
        # so SK_DOCTRINE's wire needs SK_COREFIRE (True, adopted).  The unit
        # battery asserts the conjunction rather than leaving it implied.
        if SK_DOCTRINE and self.doc_fired:
            word |= CF_DOC_BIT
        if shooter is not None:
            word |= (pack_tile(shooter[0]) & CF_TILE_MASK) << CF_TILE_FIELD
            if shooter[1]:
                word |= CF_SENT_BIT
            if shooter[2]:
                word |= CF_RAY_BIT
        elif (SK_SENTRY and SK_SENTRY_ALARM
                and (word & CF_SENTRY_BIT) and self.sentry_pos is not None):
            # ⛔ THE TILE IS A FALLBACK, NEVER AN OVERRIDE.  `_corefire_shooter`
            # already publishes a ray-confirmed or reach-covering turret and its
            # three rungs are strictly better evidence than "it is standing in
            # the fence"; this line fills the tile ONLY where those rungs found
            # nothing -- the case that otherwise leaves `_counter_target` with
            # no target at all and the answer with nothing to march at.  No
            # CF_RAY_BIT: this tile was not ray-confirmed and must not pass
            # SK_COUNTER_RAY_ONLY's filter.
            word |= (pack_tile(self.sentry_pos[0]) & CF_TILE_MASK) << CF_TILE_FIELD
            if self.sentry_pos[1]:
                word |= CF_SENT_BIT
        h = hp // CF_HP_UNIT
        if h < 0:
            h = 0
        elif h > CF_HP_MASK:
            h = CF_HP_MASK
        word |= (h & CF_HP_MASK) << CF_HP_FIELD
        self.wstore(ct, SK_SLOT_COREFIRE, word)

    # ------------------------------------------------------------------
    # s57 SK_DOCTRINE -- THE TRIGGER (writer: CORE) and THE BURST CONVERSION
    # ------------------------------------------------------------------
    # GAME CONTEXT: in-engine decisions of our own core in the Florent Code
    # League, a sandboxed bot-vs-bot competition.  "the burst" is a phase of
    # our own build order; `convert_ammo` is the engine's documented 1:1
    # titanium-to-ammunition call.

    def _doc_trigger(self, ct, rnd):
        """THE TRIGGER, evaluated on the core.  True once the burst is open.

        ⭐⭐ TAIL C (s57 doctrine iteration, 2026-08-24).  THREE TERMS, ALL
        CORE-LOCAL, ALL CONJUNCTIVE -- FUNDED and RATE and STABILITY.  The
        constants block in `sk_maps.py` carries the full provenance; in one
        paragraph, off `scratchpad/s57_heim0/w1diag_rows.json` (the w1 platform
        window, 15 cells / 3 opponents):
          * TAIL A (`bank >= SK_DOC_BANK`) FIRED 0 OF 15 and is RETIRED behind
            SK_DOC_TAIL_A.  Only one cell ever held 600 Ti at all.  The
            constant and its Focalground necessity cut are KEPT at the flag.
          * TAIL B FIRED 7 OF 15 -- median r46, earliest r20 -- on the ADOPTED
            eco latch, which certifies FLOW and says nothing about money in
            hand or about our own core surviving.  Those cells stood 0-1
            forward tubes and died at median r176.  ITS ECO-LATCH DEPENDENCY IS
            REMOVED: the core-local `batt2_eco_since` state was the 7 early
            misfires.  What survives of tail B is its FLOOR
            (`_doc_burst_floor`), now the FUNDED term's level.

        ⛔ THE THREE TERMS AND WHAT EACH REFUSES:
            FUNDED     bank >= `_doc_burst_floor()` HELD for SK_DOC_FUND_HOLD
                       consecutive rounds.  A tree that spends every round
                       touches a level; it does not hold one.
            RATE       delivered titanium per round (income proxy with the
                       engine's PASSIVE drip SUBTRACTED) >= the live-scaled
                       barrel-replacement bar.  Computed, never hardcoded.
            STABILITY  our core at max HP and its corefire damage stamp cold
                       for SK_DOC_STABLE_RNDS rounds.

        ⛔ THE SAMPLER RUNS FIRST AND UNCONDITIONALLY -- INCLUDING AFTER THE
        FIRE, WHICH IS A CHANGE.  A rate is only a rate if the sampling is
        regular (`_b2_sample` refuses any gap other than exactly one round
        rather than averaging over a hole), and under SK_DOC_REARM the trigger
        can be asked again after the burst, so a ring that stopped at the fire
        would answer the re-armed trigger with a stale window.  The core's
        `batt2_*` are per-instance and are read by nothing else on the core.
        ⛔ `_b2_eco_ready` IS NO LONGER CALLED HERE.  It was called to ADVANCE
        the latch tail B read; tail C reads no latch.  Every other caller is on
        a builder body and is untouched.
        ⛔ AN UNREADABLE SENTINEL PRICE REFUSES TO FIRE.  A floor we could
        not read is not a floor we have cleared, and committing the whole
        identity on a failed read is the one direction that cannot be undone.
        """
        if not SK_DOCTRINE:
            return False
        # THE SAMPLER, FIRST AND UNCONDITIONALLY (see the docstring).  No-op on
        # any SK_BATTERY2_ECO-off arm (one module-constant test).
        self._b2_sample(ct, rnd)
        if SK_DOC_LATCH_ONCE and self.doc_fired:
            # ⭐⭐ THE BOUNDED RE-ARM.  Returns True only on the round it drops
            # the phase; otherwise the latch stands, exactly as before.
            if not self._doc_rearm(ct, rnd):
                return True
        try:
            bank = ct.get_global_resources()
        except Exception:
            self.doc_fund_held = 0
            return False
        tail = 0
        if SK_DOC_TAIL_A and bank >= SK_DOC_BANK:
            tail = 1
        elif SK_DOC_TRIGGER_LATCH and self._doc_tail_c(ct, rnd, bank):
            tail = 3
        # --- TAIL D (iteration 8, w7): THE WALL IS THE EMERGENCY ---------
        # >=SK_DOC_WALL_N enemy turrets standing inside d²<=SK_DOC_WALL_DSQ
        # of our core means accumulation is OVER whether or not the bank is
        # fat — barrels answer barrels, and dying rich is still dying (w1-w7:
        # every sweep was a sentinel wall vs our 0-3 tubes). Minimal floor:
        # one barrel's price, so the burst is never literally empty.
        if not tail and SK_DOC_WALL_N and self.doc_wall_n >= SK_DOC_WALL_N:
            try:
                if bank >= ct.get_sentinel_cost():
                    tail = 4
                    self.doc_wall_fires += 1
            except Exception:
                pass
        if not tail:
            return False
        if self.doc_round < 0:
            self.doc_round = rnd
            self.doc_tail = tail
        self.doc_fire_round = rnd
        self.doc_fires += 1
        self.doc_tubes_peak = 0          # a NEW re-arm window opens here
        self.doc_fired = True
        return True

    def _doc_tail_c(self, ct, rnd, bank):
        """TAIL C -- FUNDED and RATE and STABILITY, evaluated on the core.

        ⛔ EVERY REFUSAL IS COUNTED SEPARATELY (`doc_hold_short`,
        `doc_rate_cold`, `doc_rate_short`, `doc_unstable`).  A conjunction that
        never fires and a conjunction whose THIRD term never fires read
        identically in the fire-round column and must not read identically in
        the trace.  ⛔ NOTHING BRANCHES ON ANY OF THEM.
        ⛔ THE TERMS ARE EVALUATED CHEAPEST-FIRST AND SHORT-CIRCUIT, so a round
        that is not funded pays one cost getter and no rate arithmetic.
        """
        # --- FUNDED: the level, HELD ------------------------------------
        res = self._doc_burst_floor(ct)
        if res is None:
            self.doc_fund_held = 0
            self.doc_hold_short += 1
            return False
        if bank >= res:
            if self.doc_fund_held < SK_DOC_FUND_HOLD:
                self.doc_fund_held += 1
        else:
            self.doc_fund_held = 0
        if self.doc_fund_held < SK_DOC_FUND_HOLD:
            self.doc_hold_short += 1
            return False
        # --- RATE: delivery, with PASSIVE SUBTRACTED --------------------
        # ⛔ THE WINDOW IS `_b2_sample`'s OWN: SK_BATTERY2_ECO_W = 40 rounds
        # with a SK_BATTERY2_ECO_WARM = 20 sample warm-up, sampled by the CORE
        # every round of the match.  ⇒ this term cannot answer before r21,
        # which is the structural floor under the autopsy's "fire at r20".
        # ⛔ `_b2_rate()` IS AN INCOME PROXY AND INCLUDES THE ENGINE'S PASSIVE
        # DRIP; `titanium_collected` excludes passive, so a bar read off the
        # raw proxy can be cleared by a bot with no economy at all.  The
        # subtraction is what makes this a DELIVERY bar.  Both of its
        # approximations are disclosed at SK_DOC_RATE_PASSIVE and both make the
        # bar HARDER to clear.
        if SK_DOC_RATE:
            r = self._b2_rate()
            if r is None:
                self.doc_rate_cold += 1
                return False
            if SK_DOC_RATE_PASSIVE:
                r -= SK_DOC_PASSIVE_RATE
            self.doc_rate_last = r
            # ITERATION 3 (w2diag): the live-scaled bar SELF-INFLATES — every
            # barrel we buy raises our own trigger's price (RATE alone blocked
            # 1,816 rounds live). Frozen at BASE cost: fires 6/10 vs 4/10,
            # ~40r earlier, still refuses the zero-economy cells.
            bar = GameConstants.SENTINEL_BASE_COST / float(SK_BATTERY2_ECO_LIFE)
            if r < bar:
                self.doc_rate_short += 1
                return False
        # --- STABILITY: our own core, core-local -------------------------
        if SK_DOC_STABLE and not self._doc_stable(ct, rnd):
            self.doc_unstable += 1
            return False
        return True

    def _doc_stable(self, ct, rnd):
        """STABILITY -- True while our core is whole and has been left alone.

        TWO CORE-LOCAL READS THAT COVER EACH OTHER'S BLIND SPOT:
          * `get_hp() < get_max_hp()` is FRESH THIS ROUND but blind to damage
            that has already been healed back;
          * `corefire_last` REMEMBERS, and is ONE ROUND STALE by construction
            -- `_doc_trigger` runs ABOVE `_corefire_report` in `_core` so the
            b31 burst latch reaches the wire the round it fires rather than the
            round after.  Disclosed rather than papered over: a hit taken THIS
            round is caught by the HP half in the same round, so the staleness
            cannot open a hole, only shorten the cold window by one round.
        ⛔ AN UNREADABLE HP IS NOT A STABLE CORE.  Same direction as the
        trigger's unreadable-price refusal: do not commit the identity on a
        number we could not read.
        ⛔ DEPENDENCY, STATED: `corefire_last` is only advanced while
        SK_COREFIRE is on (True, adopted).  With it off this degrades to the HP
        half alone, which is a weaker term and not a wrong one.
        """
        try:
            if ct.get_hp() < ct.get_max_hp():
                return False
        except Exception:
            return False
        if (self.corefire_last >= 0
                and rnd - self.corefire_last < SK_DOC_STABLE_RNDS):
            return False
        return True

    def _doc_rearm(self, ct, rnd):
        """THE BOUNDED RE-ARM.  True only on the round it drops the phase.

        Tracks the burst's HIGH-WATER forward-tube count and, if
        SK_DOC_REARM_RNDS rounds after the fire the battery has never stood
        SK_DOC_REARM_TUBES tubes, clears `doc_fired` so the trigger re-arms.

        ⛔ HIGH-WATER, NOT CURRENT.  The question is "did the burst ever
        assemble", not "is it assembled now" -- a tube that stood and was
        knocked out answers the first and not the second.
        ⛔ THE CORE IS THE ONLY AUTHORITY.  Clearing `doc_fired` here clears
        CF_DOC_BIT on this same round's publish (the word is written WHOLE
        every round, never read-modify-write), and a builder that latched off
        the wire follows the bit back down in `_doc_fired`.  One writer, one
        latch, in both directions.
        ⛔ IT CANNOT UN-FIRE A WORKING BURST: the tube high-water gate is
        checked BEFORE the clock, so a battery that reached two tubes is never
        re-armed however long it then takes.  That is exactly the regime
        SK_DOC_LATCH_ONCE's stranding argument covers.
        ⚠ THE SLOT-8 CENSUS IS THE ONE TAIL-C INPUT WHOSE WRITER IS NOT THE
        CORE.  An absent or unreadable writer reads 0, which biases toward
        re-arming -- i.e. toward phase 1, the identity's own default.
        """
        if not SK_DOC_REARM:
            return False
        try:
            drip = ct.read_store(SK_SLOT_DRIP)
        except Exception:
            drip = 0
        tubes = (drip >> DRIP_SENT_FIELD) & DRIP_GUN_MASK
        if tubes > self.doc_tubes_peak:
            self.doc_tubes_peak = tubes
        if self.doc_tubes_peak >= SK_DOC_REARM_TUBES:
            return False
        if (self.doc_fire_round < 0
                or rnd - self.doc_fire_round < SK_DOC_REARM_RNDS):
            return False
        self.doc_fired = False
        self.doc_fund_held = 0
        self.doc_rearms += 1
        return True

    def _doc_convert(self, ct, rnd):
        """THE BURST CONVERSION.  True if it spent this team-turn's conversion.

        "Conversion sized at burst": ramp the global ammunition balance to
        SK_DOC_AMMO at up to SK_DOC_AMMO_MAX titanium a round, WITHOUT eating
        the sentinels the battery still has to buy.

        ⛔ THE RESERVE IS A LIVE TEAM READ, NOT A CONSTANT.  The forward
        sentinel census arrives on slot 8 from the engineer (`_drip_report`,
        one writer, one slot) and is the same field the drip already reads.
        While the battery is short this rung holds back ONE barrel's live
        price; once SK_ROTATE_WANT stand it holds back nothing and every
        titanium is ammunition.  The measurement that sized it is at the line.
        ⛔ AND SINCE s57's w4 FIX THERE IS A **SECOND** RESERVE, a flat one:
        available funds are read as max(0, bank - SK_DOC_ANSWER_RESERVE), so
        this ramp never spends the titanium the answer sentinel needs.  The two
        stack (one live barrel price + one flat answer) and both are disclosed
        at the line.
        ⛔ THE 4/10 LATTICE IS OBEYED (`lattice_floor`, COPY 7's acceptance
        test), for the same reason `_drip` and `_fort_ammo_bank` obey it: a
        conversion off the lattice is a conversion this tree did not intend.
        ⛔ EVERY REFUSAL IS COUNTED (`doc_conv_held`).  A ramp that never
        converted and a ramp that never had room read identically in the ammo
        column and must not read identically in the trace.
        """
        if not (SK_DOCTRINE and SK_DOC_CONVERT):
            return False
        if not self.doc_fired:
            return False
        try:
            ammo = ct.get_global_ammo()
        except Exception:
            return False
        if ammo > self.doc_ammo_peak:
            self.doc_ammo_peak = ammo
        if ammo >= SK_DOC_AMMO:
            return False
        try:
            have = ct.get_global_resources()
            drip = ct.read_store(SK_SLOT_DRIP)
            sent_cost = ct.get_sentinel_cost()
        except Exception:
            return False
        fwd_sents = (drip >> DRIP_SENT_FIELD) & DRIP_GUN_MASK
        # ⛔⛔ THE RESERVE IS **ONE** BARREL, NOT THE WHOLE REMAINING BATTERY,
        # AND THE FIRST BUILD MEASURED WHY.  Reserving `(SK_ROTATE_WANT -
        # standing) x get_sentinel_cost()` reads ~400 Ti at the scales these
        # cells run, against a bank whose measured maximum is 295 -- so `room`
        # was negative on every round and the ramp converted ZERO in 988
        # sampled rounds (`asmbuild_ident/tron_*.err`, conv=0 on all three ON
        # cells including the one whose trigger fired at r120).  The burst then
        # stood barrels it could not fire: helheim r203 read 2 plants and an
        # ammunition balance of 4, against the 10 one sentinel shot costs.
        # A reserve that pre-pays the whole battery out of a bank that never
        # holds it does not protect the battery -- it silences the magazine.
        # ⇒ HOLD ONE BARREL'S PRICE WHILE THE BATTERY IS SHORT, AND NOTHING
        # ONCE IT STANDS.  That is the same quantity `_doc_burst_floor`'s first
        # term uses, so "what we keep in hand for the next barrel" means one
        # thing in this tree.  The remaining barrels are bought out of the FLOW
        # the eco latch certified, tube by tube, exactly as `_battery_open`
        # already buys them.
        # ⭐⭐ s57 THE ANSWER RESERVE (w4 autopsy, 2026-08-24), AND THIS IS ITS
        # CONSUMER (b).  AVAILABLE FUNDS FOR THE PHASE-2 RAMP ARE
        # max(0, bank - SK_DOC_ANSWER_RESERVE): a bank below the reserve reads
        # as EMPTY here, so the burst's conversion can never be the reason
        # `_stand_answer_action` finds itself unfunded when a siege lands (it
        # read bank >= 120 on 19% of armed rounds in w4).  ⛔ THIS IS THE
        # OFFENSIVE SPEND ONLY -- the answer build and `_core_medic`'s heals
        # read the TRUE bank, unchanged.  ⛔ SK_DOC_ANSWER_RESERVE = 0 restores
        # the pre-w4 arithmetic exactly.
        have -= SK_DOC_ANSWER_RESERVE
        if have < 0:
            have = 0
        room = have - (sent_cost if fwd_sents < SK_ROTATE_WANT else 0)
        amt = SK_DOC_AMMO - ammo
        if amt > SK_DOC_AMMO_MAX:
            amt = SK_DOC_AMMO_MAX
        if amt > room:
            amt = room
        amt = lattice_floor(amt)
        if amt <= 0:
            self.doc_conv_held += 1
            return False
        try:
            if ct.can_convert_ammo(amt):
                ct.convert_ammo(amt)
                self.converts += 1
                self.doc_converts += 1
                self.doc_conv_ti += amt
                return True
        except Exception:
            return False
        self.doc_conv_held += 1
        return False

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
        self.doc_wall_n = 0               # iteration 8: fresh census per scan
        best = None                       # (rank, dsq, Position, is_sent)
        sentry = None                     # (dsq, x, y, Position, is_sent, eid)
        anchor = self.core if self.core is not None else p
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
            # iteration 8: the WALL census — values already in hand.
            if dsq_core(ep, anchor) <= SK_DOC_WALL_DSQ:
                self.doc_wall_n += 1
            # ⭐ s57 THE SENTRY, PIECE 1 -- THE PRESENCE READ, AND IT IS FREE.
            # team, type and position for exactly this entity class have ALL
            # been read by the three statements above; the whole read is one
            # `dsq_core` on integers already in hand.  ⛔ TURRET_TYPES is
            # (GUNNER, SENTINEL) -- a LAUNCHER is not an alarm here, because the
            # verb this arms is the counter-peck and the autopsy's killer class
            # is 19/19 sentinel.
            if SK_SENTRY and SK_SENTRY_ALARM:
                sd = dsq_core(ep, anchor)
                if sd <= SK_SENTRY_DSQ:
                    cand = (sd, ep.x, ep.y)
                    if sentry is None or cand < sentry[0]:
                        sentry = (cand, ep, sent, eid)
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
        if SK_SENTRY and SK_SENTRY_ALARM:
            self._sentry_commit(sentry, rnd)
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

    def _sentry_commit(self, sentry, rnd):
        """s57 THE SENTRY, PIECE 1 -- turn this round's presence read into the
        latch `_corefire_report` publishes.  Writer: the CORE, same as the
        damage latch.  No engine call: `sentry` is already decided.

        GAME CONTEXT: `sentry` is a competing bot's GUNNER/SENTINEL building
        standing inside our own half of the simulated grid.  Everything here is
        bookkeeping over the engine's documented entity stream.

        ⛔⛔ THE LATCH EXPIRES, AND THAT IS THE #132 RULE, NOT A COURTESY.  A
        latch that only ever ARMS is an alarm nobody can switch off, and it
        fails in the flattering direction (an answer verb that never stands
        down looks busy on every dose column).  THREE INDEPENDENT EXITS, each
        of which drives `sentry_last` back to -1 IN THE SAME ROUND:

          (a) THE THREAT DIED, or was never there.  A turret is a BUILDING and
              cannot move, so "no enemy turret inside the fence this round" is
              conclusive for everything the core can see: `sentry is None` ->
              cleared immediately.  This is the DEATH tail and it needs no
              clock -- 24 rounds of COREFIRE-style TTL would be 24 rounds of
              answering a building that is already rubble.
          (b) THE THREAT LEFT THE FENCE.  Structurally the same read: it is not
              in the candidate set, so it is not in `sentry`.  (A building
              cannot walk; this tail is reachable in practice only if our own
              core anchor were to move, which it cannot, so it is folded into
              (a) rather than given a second code path -- and the unit battery
              drives it by moving the THREAT, which is what a test can do.)
          (c) THE EPISODE RAN OUT.  SK_SENTRY_ARM_MAX rounds after the FIRST
              round this (tile, occupant) was seen, the alarm stops arming for
              that occupant even though it is still standing.  This is the
              in-window scoping the SC lesson demands: without it a parked gun
              (the field's class D, a measured 221.5-round lease) would hold
              the answer ladder open for the rest of the match.

        ⛔ THE EPISODE KEY IS (TILE, OCCUPANT ID), the `demo_pecks` keying, for
        the same reason it has that keying: a RE-PLANT on a burnt-out tile is a
        NEW threat and must re-arm, while a key on the tile alone would concede
        that tile for the rest of the game.
        """
        if sentry is None:
            self.sentry_last = -1
            self.sentry_pos = None
            return
        (_sd, sx, sy), ep, sent, eid = sentry
        key = (sx, sy)
        prev = self.sentry_seen.get(key)
        if prev is None or prev[0] != eid:
            self.sentry_seen[key] = (eid, rnd)
            first = rnd
        else:
            first = prev[1]
        if rnd - first >= SK_SENTRY_ARM_MAX:
            self.sentry_last = -1          # (c) episode exhausted
            self.sentry_pos = None
            return
        self.sentry_last = rnd
        self.sentry_pos = (ep, sent)
        self.sentry_arms += 1

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
    # s57 LEVER 1 -- THE CONVERSION POLICY  (SK_AMMO_PUSH)
    # ------------------------------------------------------------------

    def _ammo_push(self, ct, rnd, home_guns, home_sents):
        """Convert toward a STANDING BANK while we hold firing ground.  True
        iff it spent this round's one team conversion.

        GAME CONTEXT: an in-engine resource conversion in the Florent Code
        League, a sandboxed bot-vs-bot programming competition.  `convert_ammo`
        is the engine's documented 1:1 titanium -> ammunition call, at most once
        per team per turn, usable the same turn, and it does NOT consume the
        core's action cooldown -- so this policy can run EVERY round without
        ever costing a spawn.

        ⭐⭐ WHY IT EXISTS, IN ONE MEASURED SENTENCE (the 41-loss autopsy,
        `docs/research/LOSSAUT-f1f2-2026-08-23.md`): SUSTAINED GROSS
        CORE-DAMAGE RATE ON THE ENEMY CORE = TITANIUM CONVERTED TO AMMUNITION
        AND NOTHING ELSE -- not turret placement, not in-range time (242 vs 255
        turret-rounds; we hold the ground in losses too), not facing, not
        survival, not builder count, all of which are statistically identical
        between our wins and our losses.  We run 1.47 HP/round in losses and
        4.30 in wins, and checkmate by r300 needs ~4.5-5.3.

        ⛔ WHAT THE DRIP STRUCTURALLY CANNOT DO, WHICH IS THE WHOLE DOSE.
        `_drip` is need-based off turrets that ALREADY EXIST and it NEVER
        BANKS: it converts `need + SK_AMMO_FLOOR - ammo` and no more, so the
        balance is hand-to-mouth (measured peak ~30, three sentinel shots,
        spend/convert 0.94-0.99 -- we do fire what we buy).  A round in which
        the team is short of titanium is therefore a round a turret with a
        target and a zero cooldown DOES NOT SHOOT, and that lost shot is never
        recovered.  A standing bank carries titanium from a rich round into a
        poor one; nothing else in this tree does.

        ⛔ THE THREE REFUSALS, EACH ONE A DIRECTION THIS CAN BE WRONG IN:
          * NO FIRING GROUND (`need == 0`) -- ammunition with no turret that
            can spend it is titanium taken out of the belt for nothing.  The
            read is the DRIP'S OWN `need` (home half from the core's
            `_threat_scan`, forward half from slot 8), so the two converters
            cannot disagree, and it costs zero new engine calls.
          * BELOW THE RESERVE -- `SK_AMMO_PUSH_RESERVE` plus one LIVE
            builder-bot cost stays liquid, because `_spawn_plan` simply returns
            when the bank is under that price and a role body then stays dead.
          * BELOW THE DRIP'S OWN NUMBER -- if the reserve or the per-round cap
            would make this convert LESS than `_drip` would have, it stands
            down and the drip runs unchanged.  ⭐ THIS IS THE PROPERTY THAT
            MAKES THE PLANK ADDITIVE: the flag can only ever ADD conversion,
            never remove it, so no standing turret can be silenced by it.  It
            is `_fund_floor`'s measured deadlock ("shoot with what stands",
            jotunheim ammo == 0 in 201 of 201 window rounds) refused in
            advance.
        """
        if rnd <= 0:
            return False                        # NEVER at r0 (the drip's rule)
        try:
            drip = ct.read_store(SK_SLOT_DRIP)
        except Exception:
            return False
        fwd_guns = drip & DRIP_GUN_MASK
        fwd_sents = (drip >> DRIP_SENT_FIELD) & DRIP_GUN_MASK
        need = (SK_AMMO_GUNNER * (home_guns + fwd_guns)
                + SK_AMMO_SENTINEL * (home_sents + fwd_sents))
        if need <= 0:
            return False                        # no firing ground: stand down
        try:
            ammo = ct.get_global_ammo()
            have = ct.get_global_resources()
            reserve = SK_AMMO_PUSH_RESERVE + ct.get_builder_bot_cost()
        except Exception:
            return False
        target = need + SK_AMMO_FLOOR
        if target < SK_AMMO_PUSH_BANK:
            target = SK_AMMO_PUSH_BANK          # a MAX, never a replacement
        if ammo >= target:
            return False
        # The drip's own number for this round, WITHOUT `_fund_floor`'s clamp:
        # that clamp only ever LOWERS the drip, so this is an upper bound and
        # the comparison below yields to the drip more often than strictly
        # necessary -- conservative in the direction that cannot cost a shot.
        drip_amt = need + SK_AMMO_FLOOR - ammo
        if drip_amt > have:
            drip_amt = have
        if drip_amt < 0:
            drip_amt = 0
        amt = target - ammo
        if amt > SK_AMMO_PUSH_MAX:
            amt = SK_AMMO_PUSH_MAX              # the ramp cap
        room = have - reserve
        if room < 0:
            room = 0
        if amt > room:
            amt = room                          # the reserve
        # The 4/10 lattice, floored, exactly as `_drip` and `_fort_ammo_bank`
        # do it (COPY 7's acceptance test: >= 97.3% of converted amounts are
        # exact sums of 4s and 10s).
        amt = lattice_floor(amt)
        if amt <= 0 or amt <= lattice_floor(drip_amt):
            return False                        # let the drip do its own job
        try:
            if not ct.can_convert_ammo(amt):
                return False
            ct.convert_ammo(amt)
        except Exception:
            return False
        self.converts += 1
        self.push_converts += 1
        self.push_ti += amt
        return True

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
        # ⭐⭐ s57 THE KILLBOX, ARM 3, PIECE 5 (SK_KB_FAST_SPAWN) -- ONE EXTRA
        # OPENING BUILDER FOR THE BOX, SEPARATELY ABLATABLE.  COPY 8's rule is
        # exactly four bodies and never a fifth while four live; this raises the
        # want by SK_KB_FAST_SPAWN_N inside SK_KB_FAST_SPAWN_BY and not one
        # round later.  ⛔ THE COUNTER IS NOT `live`: with five bodies alive
        # `live` still tops out at SK_N_ROLES (there are only four role beats),
        # so a want of five read off `live` would spawn for ever -- the bound is
        # this core's own `kb_fast_spawned`, incremented on the spawn below.
        # `_claim_role` gives the extra body role 0 by its existing
        # `n % SK_N_ROLES` rule once every beat is fresh, i.e. it is a SECOND
        # KEEPER: it lays barriers beside the first under the nearest-tile split
        # and then does ordinary keeper duty.
        # ⚠ THE PRICE IS 30 Ti AT THE LIVE SCALE PLUS +20% ON THE ONE GLOBAL
        # ADDITIVE COST FACTOR, and it delays the first harvester.  That is what
        # the opening-eco guard columns exist to price.
        _kbextra = (SK_KILLBOX and SK_KILLBOX_FAST and SK_KB_FAST_SPAWN
                    and rnd <= SK_KB_FAST_SPAWN_BY
                    and self.kb_fast_spawned < SK_KB_FAST_SPAWN_N)
        if _kbextra:
            want += SK_KB_FAST_SPAWN_N
        # ⭐⭐ s57 THE PUSH v3, PIECE 2b (SK_PUSH_WARDEN2) -- ONE EXTRA BODY AT
        # PUSH TIME, THE SAME COUNTER-BOUNDED PATTERN AND FOR THE SAME REASON.
        # ⛔ THE COUNTER IS NOT `live` AND CANNOT BE: with five bodies alive
        # `live` still tops out at SK_N_ROLES (four role beats, and the warden
        # deliberately writes none), so a want of five read off `live` would
        # spawn for ever.  The bound is this core's own `push_w2_spawned`,
        # incremented on the spawn below exactly as `kb_fast_spawned` is.
        # ⛔ THE TRIGGER IS THE SHARED PREDICATE, NOT A CORE-LOCAL LATCH:
        # `_push_w2_trigger` is the same slot-7 read the CLAIMING BODY will
        # make (`_claim_role`), which is how the two ends agree without a store
        # slot to talk over.
        # ⛔ THE FLOOR IS AN AFFORDABILITY READ AND BOTH VERDICTS ARE COUNTED:
        # wealthdiag's BASE bank medians are 68 (r0-100) and 42 (r100-300)
        # against a body that costs ~36-48 Ti at the live scale, i.e. the
        # median purse at push time is about one body wide -- so the extra body
        # waits for a purse that can pay for it AND still hold a barrel's
        # worth.  `push_w2_arm` counts rounds the trigger held, `push_w2_poor`
        # rounds the floor refused.
        # ⚠ THE PRICE IS 30 Ti AT THE LIVE SCALE PLUS +20% ON THE ONE GLOBAL
        # ADDITIVE COST FACTOR, which inflates every later build of every type.
        # It is the same price SK_KB_FAST_SPAWN pays and it is reported, not
        # argued away: the guard columns (harvesters, eco, first-tube round)
        # price it directly.
        _w2extra = False
        if SK_PUSH and SK_PUSH_WARDEN2 and self.push_w2_spawned < SK_PUSH_W2_N:
            if self._push_w2_trigger(ct, rnd):
                self.push_w2_arm += 1
                if ct.get_global_resources() >= cost + SK_PUSH_W2_FLOOR:
                    _w2extra = True
                    want += SK_PUSH_W2_N
                else:
                    self.push_w2_poor += 1
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
        # ⭐⭐ s57 THE KILLBOX, ARM 3, PIECE 4 (SK_KB_FAST_SPAWN_DIR) --
        # DIRECTIONAL SPAWN, AND IT IS A RE-ORDER OF THIS LOOP AND NOTHING
        # ELSE.  Both passes, v603 FIX 6(c)'s exit-liveness rule and the
        # never-veto property are untouched; only the ORDER in which the eight
        # ring tiles are offered to `can_spawn` changes, from the fixed
        # DIRECTIONS order to distance-from-the-killbox-site.  A body born on
        # the site-facing tile is 1-2 rounds nearer the thing it was spawned to
        # build.  ⛔ TOTAL-ORDERED (distance, then the tile's own DIRECTIONS
        # index) so the choice is deterministic.
        _dirs = DIRECTIONS
        if SK_KILLBOX and SK_KILLBOX_FAST and SK_KB_FAST_SPAWN_DIR:
            _tgt = self._kb_fast_spawn_target(ct, rnd)
            if _tgt is not None:
                _rank = []
                for _i, _d in enumerate(DIRECTIONS):
                    _q = p.add(_d)
                    _rank.append((_q.distance_squared(_tgt), _i, _d))
                _rank.sort()
                _dirs = [_r[2] for _r in _rank]
        for require_exit in (True, False):
            for d in _dirs:
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
                # ⛔ ONLY THE EXTRA IS COUNTED, and the discriminator is the
                # same one PIECE 5 uses: the four COPY 8 role slots were
                # already staffed when this body was spawned, so this spawn is
                # the surplus one the trigger asked for.  A round that spawns a
                # ROLE REPLACEMENT (live + in_flight < SK_N_ROLES) must not
                # burn the warden's single credit -- the replacement will find
                # a stale beat and claim that role, never the warden seat.
                # ⚠ DISCLOSED RESIDUAL, not argued away: if the killbox's extra
                # and this one were ever armed in the SAME round (it needs a
                # forward tube standing by SK_KB_FAST_SPAWN_BY = 8, which no
                # cell has produced) one spawn would tick both counters and the
                # OTHER arm would lose its credit.  The claim side is not
                # ambiguous -- the body reads the trigger itself -- so the
                # residual is a lost extra body, never a mis-roled one.
                if _w2extra and live + in_flight >= SK_N_ROLES:
                    self.push_w2_spawned += 1
                    self.push_w2_rnd = rnd
                if _kbextra and live + in_flight >= SK_N_ROLES:
                    # ⛔ ONLY THE EXTRA IS COUNTED.  The four COPY 8 bodies go
                    # through the same loop; the discriminator is that the four
                    # role slots were already staffed when this one was spawned.
                    self.kb_fast_spawned += 1
                return
            if not SK_SPAWN_EXIT:
                return
