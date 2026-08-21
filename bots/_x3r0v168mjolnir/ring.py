"""WAVE 22, TRACK 3 -- PLANK RING.  Master flag `RING_ON`.

Implements the arm `analysis/wave22/0033_losses.md` 3.1 registers, on top of
`bots/loki_leap16` (PLAN.md 1.2 else-branch base), as ONE flag with ONE OFF
twin:

  * ARM 1 RING-CLAIM (reactive).  When an enemy NON-BUILDER is seen forward
    of the midline, or any enemy BUILDING lands within 4.0 of our core, claim
    our remaining FREE sockets with OUR OWN CONVEYORS -- cheapest first,
    budget-capped so it never starves the trunk.  Behind it an unconditional
    floor of `RING_FLOOR_OWN` own buildings on the ring by `RING_FLOOR_RND`,
    and only if the bank allows.  The ring opens past that floor only once the
    harvester shell exists (`RING_ECO_HARV`) -- 0033 plugs eight sockets by
    r10 and also runs eight harvesters; the plugs are paid for by an economy,
    they are not a substitute for one.
  * ARM 2 EVICT-AND-REPLACE.  An enemy building on one of our eight sockets
    is pecked by at most `RING_EVICT_BODIES` adjacent bodies, and the round
    it dies our conveyor goes back on the tile.  CLEAR + RETAKE only: the
    peck is refused unless the refill is funded, because a socket cleared and
    not refilled inside the 5-round window is simply re-bricked.
  * ARM 3 THE BODY BAN.  SEATHOLD stations on FILLED sockets only.  A body on
    an empty socket blocks our own claim and our own feeder (wave-20 M3), and
    it is 260 body-turns a game.  SOFT: if no filled socket is available the
    parent's choice stands, because shipping the ban without arm 1 hands the
    seat over faster (0033_losses.md 3.1(3)).

  * ARM 4 BELT EVICT (WAVE 30, flag `BELT_EVICT_ON`).  An enemy
    building standing ON or ORTHOGONALLY ADJACENT to one of OUR
    conveyor-chain tiles within `BELT_EVICT_DSQ` of our Core is the
    same kind of target as a brick on a socket, and until this arm
    nothing in the tree could see it: `RING_EVICT`'s target set is
    `sg_socket(...)`, i.e. `dsq_core` 1-2, and kladde v126's apron
    sits at 2.2-6.4 (`results/wave29/EMERGENCY_BLEED.md` 2).  Same
    ballot, same per-tile clock, same walk budget; NO refill, because
    the tile is not one of our sockets and there is nothing to retake.

CONVEYORS ONLY, ON OUR OWN SOCKETS.  OPENING.md 4 (contradiction X2) settles
it from the engine and from a 60-game measurement: a socket carrying our own
conveyor is a delivery terminus, a tile the enemy can never build on (E3),
AND a live heal seat -- 772 of 2 332 own-socket core heals came from a body
standing on its own conveyor and 0 from a body on its own barrier, harvester
or turret, all three of which are impassable.  Nothing in this file ever
places a barrier, a harvester or a turret on one of our eight sockets.

CARRIER HYGIENE (PLAN.md 1.5).  Every occupancy test uses
`get_tile_building_id` / `get_tile_builder_bot_id`, never `is_tile_empty`
(P0-B).  NO new comm slot: the eviction cap is an id ballot among the bodies
that can see the target, the claim ledger is CENSUSED off the buildings that
are standing, and the refill intent is per-unit.  Sandbox style: no bare
`except`, no `try`/`finally`, every handler is `except Exception:` and every
`ct.*` call that can fail has a typed fallback.
"""

from fcode import Direction, EntityType, Position

from doctrine import *  # noqa: F401,F403
from eco import (
    BELT_TYPES, SG_SOCKET_FACE, dsq_core, nearest_cardinal,
    nearest_core_tile, sg_socket, sg_socket_index,
)


class RingMixin:
    """PLANK RING.  Every method is a no-op when `RING_ON` is False."""

    # ------------------------------------------------------------------
    # THE TRIGGER
    # ------------------------------------------------------------------

    def _ring_note(self, ct, rnd, et, ep):
        """Sensing hook.  Called from `_builder`'s existing entity loop, so it
        costs no extra API call: `et` and `ep` are already in hand.

        Two independent sightings, both of them NON-BUILDER by construction
        (the caller filters), i.e. an enemy BUILDING:

          near  within `RING_NEAR_DSQ` of our core FOOTPRINT -- 0033's ring
                barriers sit at median d = 2.53 and the first lands r7;
          fwd   strictly nearer our core than theirs, i.e. past the midline --
                128 of their 138 turret placements are past it, so this is the
                same warning one to twenty rounds earlier.

        `self.enemy` may still be None on the first rounds; the midline half
        then simply does not arm, and the near half does all the work.
        """
        if not (RING_ON and RING_TRIGGER_ON) or self.core is None:
            return
        dc = dsq_core(ep, self.core)
        if dc <= RING_NEAR_DSQ:
            self.ring_seen_rnd = rnd
            self.ring_seen_pos = ep
            return
        if not RING_FWD_ON or self.enemy is None:
            return
        if dc < dsq_core(ep, self.enemy):
            self.ring_seen_rnd = rnd
            if self.ring_seen_pos is None:
                self.ring_seen_pos = ep

    def _ring_trigger(self, ct, rnd):
        """Is the ring measurably under attack right now?

        Own eyes first, with `RING_TRIG_MEM` rounds of memory -- the same
        60-round window `ARCH_MEMORY` gives the shared detector, so the two
        never disagree about how stale a sighting may be.  Then the team's S1
        stamp (an enemy TURRET near our core, slot 13 bits 0-9), which any
        unit may have written.  S3 -- the enemy BUILDER stamp -- is
        deliberately NOT consulted: this trigger is about non-builder
        presence, and borrowing S3 would widen it past what was registered.
        """
        if not (RING_ON and RING_TRIGGER_ON):
            return False
        if self.ring_seen_rnd >= 0 and rnd - self.ring_seen_rnd <= RING_TRIG_MEM:
            return True
        if not RING_TEAM_SIGNAL_ON:
            return False
        return self._sh_s1_fresh(ct, rnd)

    # ------------------------------------------------------------------
    # SHARED HELPERS
    # ------------------------------------------------------------------

    def _ring_ready(self, ct):
        """The cheap head guard every arm below starts with."""
        if not RING_ON or self.core is None:
            return False
        return bool(self.mw and self.mh)

    def _ring_face(self, t):
        """The cardinal from socket `t` into the core.  A socket is
        orthogonally adjacent to the 2x2 footprint, so this is exact."""
        f = nearest_cardinal(t.direction_to(nearest_core_tile(t, self.core)))
        return None if f == Direction.CENTRE else f

    def _ring_lay(self, ct, t):
        """Lay OUR conveyor on socket `t`, facing into the core.  True = the
        action was spent.  The only building this plank ever places."""
        f = self._ring_face(t)
        if f is None:
            return False
        try:
            if not ct.can_build_conveyor(t, f):
                return False
            ct.build_conveyor(t, f)
        except Exception:
            return False
        return True

    def _ring_eco_ready(self, ct):
        """Does the harvester shell exist?  `SLOT_HARVESTERS` already has a
        writer in the base (`_expand` on every harvester build), so this costs
        one store read and adds no slot."""
        try:
            return ct.read_store(SLOT_HARVESTERS) >= RING_ECO_HARV
        except Exception:
            return False

    # ---- WAVE 31, PLANK A: THE GATE SPLIT (see doctrine.py "WAVE 31") ----

    def _ring_door_shut(self, ct):
        """Is OUR DOOR SHUT -- an enemy building on one of our eight sockets AND
        not one socket left carrying a conveyor that outputs into the Core?

        `_sg_socket_scan`'s `foe` and `feed` sets: the incumbent census, MEMOISED
        PER UNIT PER ROUND -- `_ring_evict` runs the same scan three lines later
        and `_belt_evict`'s arm shares it, so on the round this fires it costs
        nothing new and on every other round it is two set truth tests.

        BOTH HALVES, and the second one is the WAVE 31 SMOKE'S OWN CORRECTION.
        The first build de-gated on `foe` alone, i.e. on "a brick exists".  That
        is not the deadlock: `TOP3_Clankers` section 5 is *delivery needs one of
        our buildings on our ring8*, so a bricked socket while ANOTHER socket
        still feeds the Core is an ordinary nuisance the harvester shell will be
        along to deal with, and pecking it early spends 2 Ti a round out of the
        bootstrap for nothing.  Measured on `mimic_juusto`, 30 games, seed 1411:
        de-gated on `foe` alone the arm took 23.4 pre-shell pecks a game against
        the control's 3.7 and paid -6.7 pp, and `mimic_o1b` -- which bricks a
        socket but never closes the door -- went -6.7 pp where the arm is
        supposed to be inert.  With `feed` empty required, the de-gate is armed
        only in the state the plank was registered for: the door SHUT.

        Fails CLOSED: an unreadable census is "not shut", i.e. the shell gate
        keeps binding, because this may only ever arm on POSITIVE evidence.
        """
        if self.core is None:
            return False
        try:
            feed, _free, _mine, foe, _aimed, _hfed = self._sg_socket_scan(ct)
        except Exception:
            return False
        return bool(foe) and not feed

    def _ring_evict_gate_ok(self, ct, rnd, gate_on):
        """WAVE 31 PLANK A.  The shell gate, SPLIT, for the two PECKS only.

        `gate_on` is the incumbent flag of the calling arm -- `RING_ECO_GATE_ON`
        for `_ring_evict`, `BELT_EVICT_ECO_GATE` for `_belt_evict` -- so each
        arm keeps its own off switch and neither borrows the other's.

        With `RESTORE_EVICT_ON` False this returns
        `(not gate_on) or self._ring_eco_ready(ct)`, which is EXACTLY the
        expression it replaced at both call sites, and `_ring_foe_on_ring` is
        never reached.  That is the inertness proof for the OFF twin.

        With it True the harvester shell is still the ordinary licence; the ONE
        added path is "our own door is SHUT", from `RING_FLOOR_MIN_RND`.  The
        CLAIM CEILING (`_ring_want`) and BOTH WALKS are deliberately not routed
        through here: the r30 measurement in doctrine's `RING_ECO_GATE_ON` block
        priced the walk and the claim, never the peck.
        """
        if not gate_on:
            return True                       # v164: this arm's gate is off
        if self._ring_eco_ready(ct):
            return True                       # v164: the harvester shell is up
        if not RESTORE_EVICT_ON:
            return False                      # v164, byte for byte
        if rnd < RING_FLOOR_MIN_RND:
            return False                      # r1-r5 belongs to the bootstrap
        return self._ring_door_shut(ct)

    def _ring_want(self, ct, rnd, feed_n, own_n):
        """How many own buildings we want standing on our own eight sockets.

        Under the trigger: everything the ring will hold (`RING_MAX_OWN` minus
        the sockets we deliberately keep open, which is 0 -- a socket carrying
        our conveyor is STILL a heal seat and still passable, which is exactly
        what X2 settles and what makes this different from `SG_SELF_FILL`'s
        barrier).

        Untriggered, and triggered-but-poor: `RING_FLOOR_OWN` own buildings on
        the ring, ABSOLUTE.  Both relative readings were tried and both
        ratchet: a per-body "baseline + 2" ratchets because body 2 reads a
        baseline that already contains body 1's plugs, and "feed + 2" ratchets
        because `_sg_socket_scan` classifies ANY own conveyor that outputs into
        a core tile as a feeder -- which is exactly what a claim is.  The
        screen measured the second one: 182 of 230 claims in a 32-game run came
        from the supposedly-capped untriggered path, the ring was full by r30,
        and `titanium_collected@r30` was 0 against the control's 40.  An
        absolute number cannot ratchet, and 2 is the band A1 registered.
        """
        trig = self._ring_trigger(ct, rnd)
        if trig and self._ring_eco_ready(ct):
            return RING_MAX_OWN - RING_KEEP_FREE
        if trig:
            # Under attack, but the harvester shell is not up yet.  The floor
            # still applies -- two plugs is the denial we can afford before an
            # economy exists -- and nothing more.  This is the guard
            # `SG_SELF_FILL` states as "NEVER BEFORE WE ARE PLUGGED IN", moved
            # from "one live feeder" to "the shell", because this arm's own
            # claims COUNT as live feeders and would otherwise unlock
            # themselves.
            return RING_FLOOR_OWN
        if rnd < RING_FLOOR_MIN_RND or rnd > RING_FLOOR_RND:
            return own_n
        return RING_FLOOR_OWN

    def _ring_targets(self, ct, rnd):
        """The free sockets worth claiming, best first, or ().

        CHEAPEST FIRST, and "cheap" is measured in what the 3 Ti buys:

          1. a socket one of our own belts already points INTO, or that one of
             our own harvesters already touches -- laying the conveyor there
             completes a whole delivery line the same round, so the claim pays
             for itself instead of merely denying a seat;
          2. then the sockets nearest THEIR core, because the blockade arrives
             from their side and those are the seats they reach first.

        `_sg_socket_scan(deep=True)` is the incumbent census and is memoised
        per unit per round, so the two arms below share one scan.
        """
        scan = self._sg_socket_scan(ct, deep=True)
        feed, free, mine, foe, aimed, hfed = scan
        own_n = len(feed) + len(mine)
        if own_n >= self._ring_want(ct, rnd, len(feed), own_n):
            return ()
        if own_n >= RING_MAX_OWN:
            return ()
        E = self.enemy
        out = []
        for i in free:
            live = 0 if (i in aimed or i in hfed) else 1
            de = 0 if E is None else dsq_core(sg_socket(self.core, i), E)
            out.append((live, de, i))
        out.sort()
        return tuple(i for _live, _de, i in out)

    # ------------------------------------------------------------------
    # ARM 1 -- RING-CLAIM
    # ------------------------------------------------------------------

    def _ring_claim(self, ct, rnd):
        """Lay one claim from where this body already stands.  True = action.

        FOUR BUDGET BOUNDS, and they are the whole safety case, because the
        one way an arm like this loses a game is by spending the trunk's
        titanium on tiles (measured, nordkap: `SG_SELF_FILL` bricked three
        sockets at r9/17/18 while the trunk was three conveyors short and the
        game finished on 0 titanium delivered):

          * the CHAIN GUARD -- a body carrying a trunk chain never claims;
          * `_eco_spendable` plus `RING_TI_FLOOR`, so the siege reserve and a
            12 Ti working balance are both respected;
          * `RING_MAX_PER_UNIT`, which bounds the re-lay loop if a claim is
            shot out;
          * the ring census itself is the team-wide ledger -- what is standing
            IS the count, so it cannot go stale the way a buffered store
            counter can (engine J).
        """
        if not (self._ring_ready(ct) and RING_TRIGGER_ON):
            return False
        if self.ring_claims >= RING_MAX_PER_UNIT:
            return False
        if RING_CHAIN_GUARD and self.link_queue:
            return False
        if ct.get_action_cooldown() != 0:
            return False
        p = ct.get_position()
        if dsq_core(p, self.core) > 4:
            return False                      # not standing beside the ring
        try:
            cost = ct.get_conveyor_cost()
        except Exception:
            return False
        if not self._eco_spendable(ct, cost + RING_TI_FLOOR):
            return False
        for i in self._ring_targets(ct, rnd):
            t = sg_socket(self.core, i)
            if abs(t.x - p.x) + abs(t.y - p.y) != 1:
                continue
            if not self._ring_lay(ct, t):
                continue
            self.ring_claims += 1
            if RING_LOG:
                # `t=` is the TRIGGER state, and it is on the marker rather
                # than on a fourth marker name so the three registered names
                # stay three: t=1 is the reactive claim the forensics asked
                # for, t=0 is the unconditional floor.  A run in which every
                # claim is t=0 has not measured the arm at all.
                print("RING claim (%d,%d) f=%d r=%d n=%d t=%d"
                      % (t.x, t.y, SG_SOCKET_FACE[i], rnd, self.ring_claims,
                         1 if self._ring_trigger(ct, rnd) else 0))
            return True
        return False

    def _ring_claim_walk(self, ct, rnd):
        """Step toward a socket worth claiming.  True = the move was spent.

        THE THREE HARD BOUNDS `_sg_rebuild_walk` carries, for the reason it
        carries them: a body already inside the home band, never one carrying
        a trunk chain, and a per-target plus lifetime cap on rounds diverted.
        The lifetime budget is SHARED with the eviction walk, so the two arms
        together can never spend more than `RING_WALK_CAP` rounds of one
        body's life away from the economy.
        """
        if not (self._ring_ready(ct) and RING_WALK_ON and RING_TRIGGER_ON):
            return False
        if self.ring_claims >= RING_MAX_PER_UNIT:
            return False
        # THE SHELL GATE ON THE WALK, and it is the one the screen priced
        # highest: `RING_WALK_CAP` is 24 rounds per body, so five bodies can
        # spend 120 body-rounds walking home.  In the opening that is the
        # trunk.  Measured with the walks ungated: 1 harvester and 5 conveyors
        # at r30 against the control's 2 and 8, and `titanium_collected@r30`
        # of 0 against 40.
        if RING_ECO_GATE_ON and not self._ring_eco_ready(ct):
            return False
        if RING_CHAIN_GUARD and self.link_queue:
            return False
        if self.ring_walk_total >= RING_WALK_CAP:
            return False
        p = ct.get_position()
        if dsq_core(p, self.core) > RING_WALK_BAND_DSQ:
            return False
        try:
            cost = ct.get_conveyor_cost()
        except Exception:
            return False
        if not self._eco_spendable(ct, cost + RING_TI_FLOOR):
            return False
        best, bkey = None, None
        for i in self._ring_targets(ct, rnd):
            t = sg_socket(self.core, i)
            d = abs(t.x - p.x) + abs(t.y - p.y)
            if d <= 1:
                return False                  # adjacent already: build, do not walk
            # Stand BESIDE the socket, never ON it -- a body on an empty
            # socket is arm 3's ban and would block the very build it came
            # for.  Every socket is orthogonally adjacent to a core tile and
            # to two ring tiles, so a legal stand always exists off-core.
            for dx, dy in CARD_DELTAS:
                sx, sy = t.x + dx, t.y + dy
                if not (0 <= sx < self.mw and 0 <= sy < self.mh):
                    continue
                if dsq_core(Position(sx, sy), self.core) == 0:
                    continue                  # that is the core footprint
                key = (abs(sx - p.x) + abs(sy - p.y), d, sy, sx)
                if bkey is not None and key >= bkey:
                    continue
                try:
                    if not ct.is_tile_passable(Position(sx, sy)):
                        continue
                except Exception:
                    continue
                best, bkey = Position(sx, sy), key
        if best is None:
            return False
        key = (best.x, best.y)
        if self.ring_walk_key != key:
            self.ring_walk_key = key
            self.ring_walk_left = RING_WALK_RNDS
        if self.ring_walk_left <= 0:
            return False
        if ct.get_move_cooldown() != 0:
            return False
        self.ring_walk_left -= 1
        self.ring_walk_total += 1
        self.tgt = best
        self._nav(ct, pave=False)
        return True

    # ------------------------------------------------------------------
    # ARM 2 -- EVICT AND REPLACE
    # ------------------------------------------------------------------

    def _ring_refill(self, ct, rnd):
        """Put our conveyor back on the socket we just cleared.  True = action.

        RANKED FIRST of everything this plank does, and that ranking IS the
        arm: the measured truth is a five-round window -- a socket cleared and
        left open is re-bricked -- so the refill has to beat every other use
        of the action, including the peck that created it.  The intent is
        per-unit and expires after `RING_REFILL_RNDS`; it is dropped silently
        the moment the tile stops being an empty socket of ours.
        """
        if not (self._ring_ready(ct) and RING_EVICT_ON):
            return False
        k = self.ring_refill
        if k is None:
            return False
        if rnd - self.ring_refill_rnd > RING_REFILL_RNDS:
            self.ring_refill = None
            return False
        t = Position(k[0], k[1])
        try:
            bid = ct.get_tile_building_id(t)
        except Exception:
            return False
        if bid is not None:
            # Still standing (we only wounded it), or a teammate refilled it.
            try:
                if ct.get_team(bid) == self.team:
                    self.ring_refill = None
            except Exception:
                return False
            return False
        if ct.get_action_cooldown() != 0:
            return False
        p = ct.get_position()
        if abs(p.x - t.x) + abs(p.y - t.y) != 1:
            return False
        try:
            cost = ct.get_conveyor_cost()
        except Exception:
            return False
        if not self._eco_spendable(ct, cost):
            return False                      # keep the intent: try next round
        if not self._ring_lay(ct, t):
            return False
        self.ring_refill = None
        self.ring_claims += 1
        if RING_LOG:
            print("RING refill (%d,%d) r=%d" % (t.x, t.y, rnd))
        return True

    def _ring_evict_ok(self, ct, t, cap=None):
        """The id ballot that stands in for the comm slot we do not have.

        `cap` -- WAVE 30.  ARM 4 runs the SAME ballot with its own
        `BELT_EVICT_BODIES`; None keeps `RING_EVICT_BODIES`, so every
        incumbent caller is unchanged.

        At most `RING_EVICT_BODIES` of our bodies peck one brick at once.
        Only an ORTHOGONALLY adjacent body can fire at all, so the ballot only
        has to count the adjacent ones; ties are settled by entity id, which
        every body ranks identically without communicating.  Deterministic,
        converges in one round, and it cannot reproduce the SAP failure the
        parent records (three of six builders committing to one tile while the
        economy finished the game on ten titanium).
        """
        if cap is None:
            cap = RING_EVICT_BODIES
        me = ct.get_id()
        lower = 0
        try:
            for uid in ct.get_nearby_units():
                if uid == me or ct.get_team(uid) != self.team:
                    continue
                if ct.get_entity_type(uid) != EntityType.BUILDER_BOT:
                    continue
                if uid > me:
                    continue
                up = ct.get_position(uid)
                if abs(up.x - t.x) + abs(up.y - t.y) == 1:
                    lower += 1
                    if lower >= cap:
                        return False
        except Exception:
            return False
        return lower < cap

    def _ring_evict(self, ct, rnd):
        """Peck an enemy building off one of our eight sockets.  True = action.

        CLEAR + RETAKE, NEVER CLEAR ALONE.  The refill is checked BEFORE the
        peck -- if we cannot afford the 3 Ti conveyor that goes back on the
        tile, we do not spend the action opening it, because an open socket is
        what the enemy wanted.  The intent is armed on the peck that will
        finish the building (a builder peck is 2 damage), so the retake lands
        on the earliest round the engine permits: the action is already spent
        this round by the killing blow itself.
        """
        if not (self._ring_ready(ct) and RING_EVICT_ON):
            return False
        if self.ring_ev_total >= RING_EVICT_LIFE:
            return False
        # WAVE 31 PLANK A -- THE SPLIT GATE.  v164 read
        # `if RING_ECO_GATE_ON and not self._ring_eco_ready(ct): return False`,
        # which is the deadlock TOP3_Clankers section 5 measures: we may not
        # peck a brick off our own socket until two harvesters stand, and we
        # cannot deliver to build them while the socket is bricked.
        if not self._ring_evict_gate_ok(ct, rnd, RING_ECO_GATE_ON):
            return False
        if ct.get_action_cooldown() != 0:
            return False
        try:
            ti = ct.get_global_resources()
        except Exception:
            return False
        if ti < 2 + RING_EVICT_TI_FLOOR:
            return False
        try:
            refill_cost = ct.get_conveyor_cost()
        except Exception:
            return False
        if ti < 2 + refill_cost:
            return False                      # cannot retake: do not clear
        feed, free, mine, foe, aimed, hfed = self._sg_socket_scan(ct)
        if not foe:
            return False
        p = ct.get_position()
        best, bkey, bhp = None, None, None
        for i in foe:
            t = sg_socket(self.core, i)
            if abs(t.x - p.x) + abs(t.y - p.y) != 1:
                continue
            try:
                bid = ct.get_tile_building_id(t)
                if bid is None:
                    continue
                # WAVE 28, F6 -- THE DEFECT ITSELF.  MISBEHAVE_AUDIT section 6:
                # this is the ONE `ct.fire` site in the tree with no team test.
                # `foe` comes from `_sg_socket_scan`, which is MEMOISED PER
                # ROUND (`eco.py`), so a socket cleared and re-plugged by our
                # own `_ring_refill` earlier in the same round is still listed
                # as enemy-held -- and 388 corpus pecks landed on our own
                # conveyors, 31 of 91 sampled exactly on a Core socket.
                if F6_TEAM_TEST_ON and ct.get_team(bid) == self.team:
                    continue
                hp = ct.get_hp(bid)
                if not ct.can_fire(t):
                    continue
            except Exception:
                continue
            if hp is None:
                hp = 999
            key = (hp, i)
            if bkey is None or key < bkey:
                best, bkey, bhp = t, key, hp
        if best is None:
            return False
        if not self._ring_evict_ok(ct, best):
            return False
        # THE PER-TILE BUDGET.  Keyed on the TILE, not on the building id, and
        # that is the point: the failure this bounds is the opponent RE-LAYING
        # the brick, which hands us a fresh id every time and would reset any
        # id-keyed clock forever.  A body that has spent its rounds on one
        # doorway walks away from that doorway for good.
        k = (best.x, best.y)
        if self.ring_ev_key != k:
            self.ring_ev_key = k
            self.ring_ev_left = RING_EVICT_TRY_RNDS
        if self.ring_ev_left <= 0:
            return False
        # WAVE 28, F6, the uniform refusal on top of the inline test above.
        if not self._f6_ok(ct, best):
            return False
        try:
            ct.fire(best)
        except Exception:
            return False
        self.ring_ev_left -= 1
        self.ring_ev_total += 1
        # Arm the retake.  2 damage a peck, so `hp <= 2` is the killing blow;
        # arming it on every peck instead would leave a stale intent behind a
        # brick we merely wounded, and `_ring_refill` would then burn a
        # distance test a round for nothing.
        if bhp is not None and bhp <= 2:
            self.ring_refill = (best.x, best.y)
            self.ring_refill_rnd = rnd
        if RING_LOG:
            print("RING evict (%d,%d) hp=%s r=%d n=%d"
                  % (best.x, best.y, bhp, rnd, self.ring_ev_total))
        return True

    def _ring_evict_walk(self, ct, rnd):
        """Step toward a brick sitting on one of our sockets.  True = moved.

        Same three bounds and the same shared lifetime budget as the claim
        walk.  Deliberately does NOT walk when we cannot fund the retake: a
        body that walks home to open a socket it cannot refill has spent its
        rounds doing the enemy's bookkeeping.
        """
        if not (self._ring_ready(ct) and RING_EVICT_ON and RING_EVICT_WALK_ON):
            return False
        if self.ring_ev_total >= RING_EVICT_LIFE:
            return False
        if RING_ECO_GATE_ON and not self._ring_eco_ready(ct):
            return False
        if RING_CHAIN_GUARD and self.link_queue:
            return False
        if self.ring_walk_total >= RING_WALK_CAP:
            return False
        p = ct.get_position()
        if dsq_core(p, self.core) > RING_WALK_BAND_DSQ:
            return False
        try:
            ti = ct.get_global_resources()
            refill_cost = ct.get_conveyor_cost()
        except Exception:
            return False
        if ti < 2 + refill_cost:
            return False
        feed, free, mine, foe, aimed, hfed = self._sg_socket_scan(ct)
        if not foe:
            return False
        best, bkey = None, None
        for i in foe:
            t = sg_socket(self.core, i)
            d = abs(t.x - p.x) + abs(t.y - p.y)
            if d <= 1:
                return False                  # adjacent already: peck, do not walk
            for dx, dy in CARD_DELTAS:
                sx, sy = t.x + dx, t.y + dy
                if not (0 <= sx < self.mw and 0 <= sy < self.mh):
                    continue
                if dsq_core(Position(sx, sy), self.core) == 0:
                    continue
                key = (abs(sx - p.x) + abs(sy - p.y), d, sy, sx)
                if bkey is not None and key >= bkey:
                    continue
                try:
                    if not ct.is_tile_passable(Position(sx, sy)):
                        continue
                except Exception:
                    continue
                best, bkey = Position(sx, sy), key
        if best is None:
            return False
        key = (best.x, best.y)
        if self.ring_walk_key != key:
            self.ring_walk_key = key
            self.ring_walk_left = RING_WALK_RNDS
        if self.ring_walk_left <= 0:
            return False
        if ct.get_move_cooldown() != 0:
            return False
        self.ring_walk_left -= 1
        self.ring_walk_total += 1
        self.tgt = best
        self._nav(ct, pave=False)
        return True

    # ------------------------------------------------------------------
    # ARM 3 -- THE BODY BAN
    # ------------------------------------------------------------------

    def _ring_socket_filled(self, ct, s):
        """True if socket `s` carries one of OUR buildings.

        `get_tile_building_id` and never `is_tile_empty` (P0-B): the whole
        question is which TEAM owns the tile, and `is_tile_empty` cannot see a
        body at all, which is the trap wave 20 tripped on three times.
        """
        try:
            bid = ct.get_tile_building_id(s)
            if bid is None:
                return False
            return ct.get_team(bid) == self.team
        except Exception:
            return False

    def _ring_station_ok(self, ct, s, seats, feeders):
        """Arm 3 in one predicate: may a SEATHOLD body station on socket `s`?

        A body on a FILLED socket is free -- the tile is already unspawnable
        and already unbrickable, and the body still heals the core (X2: a
        conveyor is passable, so `d^2 == 1` heal is intact).  A body on an
        EMPTY socket blocks our own claim and our own feeder, and it is the
        260 body-turns a game the loss forensics measured.

        SOFT by default: if the ring holds no filled, free, non-feeder socket
        at all, the parent's choice stands.  Shipping the ban without arm 1
        having landed a single conveyor would hand the seat over FASTER, which
        is precisely the failure 0033_losses.md 3.1(3) warns about.
        """
        if not (RING_ON and RING_BODY_BAN_ON):
            return True
        if self._ring_socket_filled(ct, s):
            return True
        if not RING_BODY_BAN_SOFT:
            return False
        # Is there a filled alternative this body could stand on instead?
        for k in seats:
            if k in feeders:
                continue
            t = Position(k[0], k[1])
            if not self._ring_socket_filled(ct, t):
                continue
            try:
                if not ct.is_in_vision(t) or not ct.is_tile_passable(t):
                    continue
                if ct.get_tile_builder_bot_id(t) is not None:
                    continue
            except Exception:
                continue
            return False                      # a filled seat exists: use it
        return True

    # ------------------------------------------------------------------
    # ARM 4 -- BELT EVICT  (WAVE 30; see the BELT EVICT block in doctrine.py)
    # ------------------------------------------------------------------

    def _belt_core(self, ct):
        """OUR Core anchor, for a unit that may not be a builder.

        `self.core` is written by `_core` and by `_builder`'s own building
        scan, so a TURRET never learns it -- and the gunner half of this arm
        runs on the turret.  Looked up ONCE per turret life off
        `get_nearby_buildings` (a home gunner stands within `RG_SITE_DSQ` of
        the footprint, so our Core is inside its vision disc by construction),
        latched either way, and kept in ITS OWN field: writing `self.core` on
        a turret would change what every other turret arm reads, and this
        plank may not do that.
        """
        if self.core is not None:
            return self.core
        if self.belt_core is not None or self.belt_core_done:
            return self.belt_core
        self.belt_core_done = True
        try:
            for eid in ct.get_nearby_buildings():
                if ct.get_team(eid) != self.team:
                    continue
                if ct.get_entity_type(eid) != EntityType.CORE:
                    continue
                self.belt_core = ct.get_position(eid)
                break
        except Exception:
            return None
        return self.belt_core

    def _belt_tiles(self, ct, rnd):
        """OUR conveyor-chain tiles within `BELT_EVICT_DSQ` of our Core.

        Memoised per unit per round.  `get_nearby_buildings` is the same
        enumeration `_builder` already runs for the Core lookup, so the census
        adds no new class of API call.

        THE CHAIN FILTER, and it is one set test: a belt tile counts only if
        it touches our Core footprint or ANOTHER of our belt tiles.  A lone
        conveyor at d 6 with nothing beside it is a stray from a dead line and
        the tiles around it are not a path worth defending; a run of two or
        more, or one plugged into the Core, is.  Connectivity all the way back
        to a harvester is NOT required and must not be: the case this plank
        exists for is the chain BROKEN by their barrier, where the far segment
        is by definition unreachable from the Core -- demanding reachability
        would blind the arm exactly when it is needed (this is the F5 error,
        `results/wave28/SCREEN_CLEAN.md`, inverted).
        """
        if self.belt_tiles_rnd == rnd:
            return self.belt_tiles
        self.belt_tiles_rnd = rnd
        self.belt_tiles = ()
        c = self._belt_core(ct)
        if c is None or not (self.mw and self.mh):
            return ()
        seen = set()
        try:
            for eid in ct.get_nearby_buildings():
                if ct.get_team(eid) != self.team:
                    continue
                if ct.get_entity_type(eid) not in BELT_TYPES:
                    continue
                bp = ct.get_position(eid)
                if dsq_core(bp, c) > BELT_EVICT_DSQ:
                    continue
                seen.add((bp.x, bp.y))
                if len(seen) >= BELT_EVICT_MAX_TILES:
                    break
        except Exception:
            return ()
        out = []
        for (x, y) in seen:
            if dsq_core(Position(x, y), c) <= 1:
                out.append((x, y))            # plugged into the footprint
                continue
            for dx, dy in CARD_DELTAS:
                if (x + dx, y + dy) in seen:
                    out.append((x, y))
                    break
        self.belt_tiles = tuple(out)
        return self.belt_tiles

    def _belt_evict_targets(self, ct, rnd):
        """Enemy buildings on / beside our belt.  ((x, y, hp, n), ...), best
        first.  Memoised per unit per round.

        `n` is HOW MANY of our belt tiles the candidate touches, and it is the
        first sort key: n >= 2 is the HOLE IN THE LINE (the barrier standing
        ON the path -- see the doctrine block: a tile carrying their building
        cannot also carry our conveyor, so "on the path" is only ever
        observable as "in the gap"), n == 1 is the apron beside it.  Then the
        weakest, then the nearest our Core, then a coordinate tie-break so
        every body that can see the tile ranks it identically without
        communicating -- the same zero-comm rule `_ring_evict_ok` runs on.

        OUR EIGHT SOCKETS ARE DROPPED HERE.  They are `RING_EVICT`'s targets,
        it can fund their retake and this arm cannot, and a socket cleared and
        not refilled is re-bricked in five rounds.
        """
        if self.belt_ev_rnd == rnd:
            return self.belt_ev_tgts
        self.belt_ev_rnd = rnd
        self.belt_ev_tgts = ()
        belt = self._belt_tiles(ct, rnd)
        if not belt:
            return ()
        c = self._belt_core(ct)
        if c is None:
            return ()
        bset = set(belt)
        hits = {}
        for (x, y) in belt:
            for dx, dy in CARD_DELTAS:
                k = (x + dx, y + dy)
                if k in bset:
                    continue
                hits[k] = hits.get(k, 0) + 1
        out = []
        for (qx, qy), n in hits.items():
            if not (0 <= qx < self.mw and 0 <= qy < self.mh):
                continue
            q = Position(qx, qy)
            d = dsq_core(q, c)
            if d == 0 or d > BELT_EVICT_DSQ:
                continue
            if sg_socket_index(c, qx, qy) >= 0:
                continue                      # RING_EVICT owns our sockets
            try:
                bid = ct.get_tile_building_id(q)
                if bid is None:
                    continue
                if ct.get_team(bid) == self.team:
                    continue
                hp = ct.get_hp(bid)
            except Exception:
                continue
            if hp is None:
                hp = 999
            out.append((-n, hp, d, qy, qx))
        out.sort()
        self.belt_ev_tgts = tuple(
            (x, y, hp, -mn) for mn, hp, _d, y, x in out)
        if BELT_EVICT_LOG and self.belt_ev_tgts:
            print("BELT tgts r=%d n=%d %s"
                  % (rnd, len(self.belt_ev_tgts), self.belt_ev_tgts[:3]))
        return self.belt_ev_tgts

    def _belt_evict_keys(self, ct, rnd):
        """The target tiles as a frozenset, for the gunner half."""
        if not (RING_ON and BELT_EVICT_ON and BELT_EVICT_GUN_ON):
            return frozenset()
        return frozenset((x, y) for x, y, _hp, _n
                         in self._belt_evict_targets(ct, rnd))

    def _belt_home_ok(self, ct, p):
        """May THIS body spend a turn on the belt?  The four standing bounds.

        A HOME body only (`BELT_EVICT_HOME_DSQ`), never a raider by role, and
        NEVER a body on THEIR ring -- `_f0_plug`, verbatim, which is the wave
        27 plug rule and the one refusal in this file that is not about our
        own economy.
        """
        c = self._belt_core(ct)
        if c is None:
            return False
        if self.role == "raid":
            return False
        if self._f0_plug(ct, p):
            return False
        return dsq_core(p, c) <= BELT_EVICT_HOME_DSQ

    def _belt_evict(self, ct, rnd):
        """Peck an enemy building off our belt path.  True = action spent.

        NO REFILL AND NO RETAKE FUNDING, and that is the one place this arm
        departs from `_ring_evict`: the tile is not one of our eight sockets,
        we never wanted to build on it, and cleared it is simply passable
        again.  The peck's own 2 Ti and `BELT_EVICT_TI_FLOOR` are the whole
        spend test.
        """
        if not (RING_ON and BELT_EVICT_ON and self._ring_ready(ct)):
            return False
        if self.belt_ev_total >= BELT_EVICT_LIFE:
            return False
        # WAVE 31 PLANK A -- THE SPLIT GATE, the twin of `_ring_evict`'s.  This
        # arm never touches our eight sockets (`_belt_evict_targets` drops
        # them), so the de-gate cannot become a second peck at the same brick:
        # it clears the apron barrier standing IN the trunk one tile further
        # out, and only while the door itself is shut.  The WALK below keeps
        # the shell gate.
        if not self._ring_evict_gate_ok(ct, rnd, BELT_EVICT_ECO_GATE):
            return False
        if ct.get_action_cooldown() != 0:
            return False
        p = ct.get_position()
        if not self._belt_home_ok(ct, p):
            return False
        try:
            ti = ct.get_global_resources()
        except Exception:
            return False
        if ti < 2 + BELT_EVICT_TI_FLOOR:
            return False
        best, bkey, bhp, bn = None, None, None, 0
        for (tx, ty, hp, n) in self._belt_evict_targets(ct, rnd):
            if abs(tx - p.x) + abs(ty - p.y) != 1:
                continue
            t = Position(tx, ty)
            try:
                if not ct.can_fire(t):
                    continue
            except Exception:
                continue
            key = (-n, hp, ty, tx)
            if bkey is not None and key >= bkey:
                continue
            best, bkey, bhp, bn = t, key, hp, n
        if best is None:
            return False
        if not self._ring_evict_ok(ct, best, cap=BELT_EVICT_BODIES):
            return False
        # THE PER-TILE BUDGET, keyed on the TILE for `RING_EVICT_TRY_RNDS`'s
        # reason: a re-laid brick is a fresh building id and would reset any
        # id-keyed clock for ever.
        k = (best.x, best.y)
        if self.belt_ev_key != k:
            self.belt_ev_key = k
            self.belt_ev_left = BELT_EVICT_MAX_PECKS
        if self.belt_ev_left <= 0:
            return False
        if not self._f6_ok(ct, best):
            return False
        try:
            ct.fire(best)
        except Exception:
            return False
        self.belt_ev_left -= 1
        self.belt_ev_total += 1
        if BELT_EVICT_LOG:
            print("BELT evict (%d,%d) hp=%s n=%d r=%d t=%d"
                  % (best.x, best.y, bhp, bn, rnd, self.belt_ev_total))
        return True

    def _belt_evict_walk(self, ct, rnd):
        """Step toward a building sitting on our belt.  True = moved.

        `_ring_evict_walk`'s three bounds and ITS lifetime budget
        (`ring_walk_total` / `RING_WALK_CAP`), shared rather than doubled: the
        two eviction arms together may still never spend more than
        `RING_WALK_CAP` rounds of one body's life away from the economy.
        """
        if not (RING_ON and BELT_EVICT_ON and BELT_EVICT_WALK_ON):
            return False
        if not self._ring_ready(ct):
            return False
        if self.belt_ev_total >= BELT_EVICT_LIFE:
            return False
        if BELT_EVICT_ECO_GATE and not self._ring_eco_ready(ct):
            return False
        if RING_CHAIN_GUARD and self.link_queue:
            return False
        if self.ring_walk_total >= RING_WALK_CAP:
            return False
        p = ct.get_position()
        if not self._belt_home_ok(ct, p):
            return False
        try:
            if ct.get_global_resources() < 2 + BELT_EVICT_TI_FLOOR:
                return False
        except Exception:
            return False
        c = self._belt_core(ct)
        best, bkey = None, None
        for (tx, ty, _hp, _n) in self._belt_evict_targets(ct, rnd):
            d = abs(tx - p.x) + abs(ty - p.y)
            if d <= 1:
                return False                  # adjacent already: peck, do not walk
            for dx, dy in CARD_DELTAS:
                sx, sy = tx + dx, ty + dy
                if not (0 <= sx < self.mw and 0 <= sy < self.mh):
                    continue
                if c is not None and dsq_core(Position(sx, sy), c) == 0:
                    continue                  # that is the core footprint
                key = (abs(sx - p.x) + abs(sy - p.y), d, sy, sx)
                if bkey is not None and key >= bkey:
                    continue
                try:
                    if not ct.is_tile_passable(Position(sx, sy)):
                        continue
                except Exception:
                    continue
                best, bkey = Position(sx, sy), key
        if best is None:
            return False
        key = (best.x, best.y)
        if self.ring_walk_key != key:
            self.ring_walk_key = key
            self.ring_walk_left = RING_WALK_RNDS
        if self.ring_walk_left <= 0:
            return False
        if ct.get_move_cooldown() != 0:
            return False
        self.ring_walk_left -= 1
        self.ring_walk_total += 1
        self.tgt = best
        self._nav(ct, pave=False)
        return True
