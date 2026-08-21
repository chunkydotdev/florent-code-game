"""WAVE 22 ARM A4 -- THE OFFENSIVE SIPHON TAP.  One flag: `SIPHON_ON`.

Spec: `analysis/wave22/siphon.md` (mechanism, geometry, abort table, tempo
budget), `analysis/wave22/PLAN.md` 2.4 (constants, falsifiers F-S1.1-F-S1.10).
Nothing in this file is read when `SIPHON_ON` is False; `bots/leap18_sip_off`
is this directory with that one constant flipped and is the inertness leg.

THE MECHANISM, IN ONE PARAGRAPH.  A harvester pushes one 10-Ti stack every
four rounds into ONE of the buildings cardinally touching it, strict
least-recently-used and TEAM-BLIND (`engine_mechanics.md` N.1: 100 % -> 50 %
-> 33 % -> 25 % measured as taps are added).  So one conveyor of ours beside
an enemy harvester takes 1/(n+1) of that harvester for ever, and denies the
victim the same amount -- a 2x swing off a 3-Ti building.  Because the theft
happens AT THE SOURCE, no redundant downstream path can restore it; that is
the whole reason this arm exists and the reason it carries no cut-vertex gate
(siphon.md 3.1: Jython spent ~7 000 Ti of ammo destroying one redundant
conveyor 139 times and Bean's collection rate did not move).

THE FOUR THINGS THAT MAKE IT SAFE RATHER THAN CLEVER.

  1. FACING.  The tap faces AWAY from the harvester, onto the next tile of our
     own chain.  A conveyor facing the victim's line or their core credits
     THEM (`engine_mechanics.md` A, `probe_feed`: b_titanium_collected = 230
     off OUR harvester).  We never choose the facing by hand: the chain is
     routed by `_link_path`, which blocks harvesters and enemy belts and both
     core footprints outright, so tile i faces tile i+1 and tile i+1 can never
     be the victim.
  2. HEAD-FIRST.  Tap tile first, then walk home laying one conveyor every two
     rounds (build, step, build -- siphon.md 1.3's measured cadence).  A
     conveyor whose output tile is empty ground holds its stack for ever
     (`engine_mechanics.md` B), so an incomplete k-tile chain is a k-stack
     buffer: every tile laid banks 10 Ti of denial the moment it fills, and
     the arm can abort at any tile without losing what is already banked.
     There is no sunk cost anywhere in this plank.
  3. TEMPO PURITY (F-S1.3, hard fail).  Nothing before `arrival`, which is
     derived here by BFS at first call and never from a map name, and nothing
     by the rider or by E1/E2 -- see `_sip_carrier_ok`.
  4. ZERO COMM.  All 16 slots are assigned in the base.  The role lives on the
     unit; a second claimant is refused by LOWEST LIVE BUILDER ID among the
     builders that can see the same harvester, which resolves locally because
     builder vision is r^2 = 20 and two units that can both see one harvester
     are necessarily within ~9 tiles of each other.

WHAT IS DELIBERATELY NOT HERE.  No cut-value scan (siphon.md 3.2 G3 is false
for every ammo attack on a rebuildable 3-Ti conveyor, so the gate's honest
output for denial is "do not"), no `SIPHON_RECYCLE` (refuted on its own
arithmetic, siphon.md 2.3 -- and `destroy()` on a loaded conveyor annihilates
the stack for +0, N.2), no `SIPHON_COLLAR` (A4b is parked, PLAN 2.4).

CARRIER HYGIENE.  Every occupancy test below is `get_tile_building_id` /
`get_tile_builder_bot_id`; `is_tile_empty` appears nowhere (P0-B).  Every
engine call that can raise sits in its own `except Exception` with a typed
fallback -- no bare except, no try/finally.
"""
import math

from fcode import Direction, Environment, EntityType, GameConstants, Position

from doctrine import *  # noqa: F401,F403
from eco import core_tiles_xy, enemy_core_for, nearest_cardinal, nearest_core_tile

# A harvester's round robin serves buildings that ACCEPT.  Barriers, turrets
# and harvesters never accept (engine_mechanics.md B), so they are not in the
# denominator and a barrier beside a harvester is not a tap (probe P-S-D).
SIP_ACCEPTOR_TYPES = frozenset((
    EntityType.CONVEYOR, EntityType.SPLITTER, EntityType.CORE,
))
SIP_BELT_TYPES = frozenset((EntityType.CONVEYOR, EntityType.SPLITTER))


class SipMixin:
    """The tap.  Mixed into `Player`; exactly one call site in main.py."""

    # Class-level defaults instead of eleven lines in `Player.__init__`: this
    # arm must be removable by deleting one base class and one `if`, and a
    # constructor edit is not that.  Every mutable one is created lazily.
    sip_tap = None          # Position of the tap tile (queue head at claim)
    sip_harv = None         # (x, y) of the victim harvester
    sip_queue = None        # remaining tiles to lay, HEAD-FIRST; [0] is next
    sip_term = None         # tile our last conveyor must face (a known belt of
                            # ours), or None to face our own core ring
    sip_claimed = 0         # round the role was taken
    sip_last_ext = 0        # round the chain last grew (abort A6)
    sip_built = 0           # conveyors laid for the current chain
    sip_taps = 0            # chains this body has started (SIP_MAX_TAPS)
    sip_need = None         # need_eff, BFS-derived, once per unit
    sip_arrival = None      # the tempo gate, BFS-derived, once per unit
    sip_ban = None          # {(x, y): round} banned tap tiles (abort A2)
    sip_kills = None        # {(x, y): [rounds]} observed kills of our taps
    sip_stacks = None       # stack ids seen sitting on our tap (the yield)
    sip_tap_live = False    # our tap conveyor is standing, as far as we know
    sip_geom_logged = False
    sip_prospect = None     # ore tile we are walking to; False == gave up
    sip_prospect_r0 = 0     # round the prospecting budget started
    sip_ore_sites = None    # their-side ore sites, nearest-home first
    sip_ore_i = 0           # cursor into sip_ore_sites
    sip_hold_r0 = 0         # round we arrived at the current site (0 == walking)
    # Why the arm did NOT fire, counted per body and printed once when it gives
    # up.  This is the only thing that separates "the plank is wrong" from "the
    # plank was never legal", which is the distinction F-S1.8 turns on.
    sip_m_seen = 0          # enemy harvesters offered to the scan
    sip_m_n = 0             # rejected: already >= SIPHON_MAX_N acceptors
    sip_m_route = 0         # rejected: no face routes inside SIPHON_MAX_CHAIN
    sip_m_money = 0         # rejected: route found, bank short
    sip_m_rival = 0         # rejected: a lower-id builder can see it too

    # ------------------------------------------------------------------
    # geometry: need_eff and `arrival`, from a BFS, never from a map name
    # ------------------------------------------------------------------

    def _sip_pathlen(self, core, ec):
        """BFS walk distance own-core-ring -> enemy-core-ring, or None.

        PLAN 2.1's definition.  Walls block; ore does not (a builder walks over
        ore).  Both core footprints block, so the measure is ring to ring.
        ~900 cells, once per unit lifetime.
        """
        mw, mh = self.mw, self.mh
        if not mw or not mh or not self.map_walls:
            return None
        ours = set(core_tiles_xy(core))
        theirs = set(core_tiles_xy(ec))
        blocked = set(self.map_walls)
        blocked |= ours
        blocked |= theirs

        def ring_of(foot):
            out = set()
            for cx, cy in foot:
                for dx, dy in CARD_DELTAS:
                    tx, ty = cx + dx, cy + dy
                    if not (0 <= tx < mw and 0 <= ty < mh):
                        continue
                    if (tx, ty) in blocked:
                        continue
                    out.add((tx, ty))
            return out

        cur = ring_of(ours)
        goal = ring_of(theirs)
        if not cur or not goal:
            return None
        seen = set(cur)
        d = 0
        cur = list(cur)
        while cur:
            for t in cur:
                if t in goal:
                    return d
            nxt = []
            for x, y in cur:
                for dx, dy in CARD_DELTAS:
                    tx, ty = x + dx, y + dy
                    if not (0 <= tx < mw and 0 <= ty < mh):
                        continue
                    k = (tx, ty)
                    if k in seen or k in blocked:
                        continue
                    seen.add(k)
                    nxt.append(k)
            cur = nxt
            d += 1
        return None

    def _sip_geom(self, ct):
        """Fill `sip_need` / `sip_arrival` once.  True iff they are usable.

        `need_eff = max(1, ceil((pathlen - 4.5) / 5.66))` and
        `arrival = 2 * ceil(pathlen / 5.66) - 1` are PLAN 2.1's forms; the
        per-band floors (r6 / r10 / r12) are siphon.md 6.1's, and we take the
        LATER of the two because the tempo falsifier is one-sided -- firing a
        round early is a hard fail, firing a round late costs a little yield.
        """
        if self.sip_arrival is not None:
            return True
        core = self.core
        if core is None or not self.mw or not self.mh:
            return False
        try:
            ec = enemy_core_for(self.mw, self.mh, core)
        except Exception:
            return False
        pathlen = self._sip_pathlen(core, ec)
        if pathlen is None:
            pathlen = abs(core.x - ec.x) + abs(core.y - ec.y)
        need = max(1, int(math.ceil((pathlen - 4.5) / 5.66)))
        hops = max(1, int(math.ceil(pathlen / 5.66)))
        if need <= 2:
            floor_r = SIP_ARRIVAL_A
        elif need <= 4:
            floor_r = SIP_ARRIVAL_B
        else:
            floor_r = SIP_ARRIVAL_C
        self.sip_need = need
        self.sip_arrival = max(2 * hops - 1, floor_r)
        if SIPHON_LOG and not self.sip_geom_logged:
            self.sip_geom_logged = True
            print("SIP band need=%d path=%d arrival=%d" % (
                need, pathlen, self.sip_arrival))
        return True

    # ------------------------------------------------------------------
    # eligibility
    # ------------------------------------------------------------------

    def _sip_carrier_ok(self):
        """F-S1.3's carrier half: never the rider, never E1/E2.

        In this carrier the two bodies that station on filled sockets and hold
        the heal wall are the economy seats, and seat 0 is the body that leaves
        for the enemy core on round one.  `SIP_EXCLUDE_SEATS` names all of them
        plus the home defender.  What is left is the post-cap-lift work force:
        the defected late-raid seat and spawns #5 and up -- siphon.md 4.1's
        "builder #4 from the r10 cap lift".  A body still carrying an economy
        trunk chain is not spare either.
        """
        if self.role != "raid":
            return False
        if self.role_n in SIP_EXCLUDE_SEATS:
            return False
        if self.link_queue:
            return False
        return True

    def _sip_reserve(self, ct):
        """CB_RESERVE.  A3 is not in this build; the tap is junior anyway.

        PLAN 2.3 funds counter-battery from `2 x gunner cost + 30` held back
        from `r = 2 x need_eff` onward, and siphon.md 6.2 cost 3 makes the tap
        junior to it.  Honouring the reserve here, before A3 exists, is the
        only way to measure this arm against the budget it will actually have.
        """
        if not SIP_RESERVE_ON:
            return SIP_BANK_FLOOR
        try:
            return 2 * ct.get_gunner_cost() + SIP_RESERVE_PAD
        except Exception:
            return 2 * GameConstants.GUNNER_BASE_COST + SIP_RESERVE_PAD

    # ------------------------------------------------------------------
    # board reads
    # ------------------------------------------------------------------

    def _sip_free_tile(self, ct, t):
        """Buildable-looking empty ground.  P0-B: never `is_tile_empty`."""
        try:
            if ct.get_tile_building_id(t) is not None:
                return False
        except Exception:
            return False
        try:
            if ct.get_tile_builder_bot_id(t) is not None:
                return False
        except Exception:
            return False
        try:
            if ct.get_tile_env(t) == Environment.WALL:
                return False
        except Exception:
            return False
        return True

    def _sip_acceptors(self, ct, hx, hy):
        """(n, ours, ok) -- acceptors already on that harvester, both teams.

        `ok` is False whenever any of the four cardinal tiles is outside our
        vision, because `n` decides our share and a half-counted `n` is worse
        than no tap at all (siphon.md 3.5: everything we know about their graph
        is a stale union of past sightings).
        """
        n = 0
        ours = 0
        for dx, dy in CARD_DELTAS:
            tx, ty = hx + dx, hy + dy
            if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                continue
            t = Position(tx, ty)
            try:
                if not ct.is_in_vision(t):
                    return 0, 0, False
            except Exception:
                return 0, 0, False
            try:
                bid = ct.get_tile_building_id(t)
            except Exception:
                return 0, 0, False
            if bid is None:
                continue
            try:
                et = ct.get_entity_type(bid)
                team = ct.get_team(bid)
            except Exception:
                return 0, 0, False
            if et in SIP_ACCEPTOR_TYPES:
                n += 1
                if team == self.team:
                    ours += 1
        return n, ours, True

    def _sip_lowest_id(self, ct, hpos):
        """Zero-comm arbitration: lowest live builder id wins the harvester.

        No slot is read and none is written -- all 16 are assigned in the base.
        Two refinements over the bare "lowest id that can see it" rule, both
        forced by measurement, both positional so they need no comm:

          * the rival must be FORWARD (nearer their anchor than ours).  The bare
            rule hands priority to whichever of our bodies has the lowest id,
            and in this carrier those are exactly the bodies that can never tap
            -- the rider is seat 0 and E1/E2 are seats 1-2, i.e. the three
            lowest ids in the match.  Measured on nordkap: 4 of 8 offered
            harvesters were refused to a rival that was standing at home.
          * the rival must be AT LEAST AS CLOSE to the harvester as we are.  A
            body further from it is not a better claimant, and deferring to it
            loses the tap to nobody.
        """
        try:
            me = ct.get_id()
            uids = ct.get_nearby_units()
            mine_d = ct.get_position().distance_squared(hpos)
        except Exception:
            return True
        try:
            ec = enemy_core_for(self.mw, self.mh, self.core)
        except Exception:
            ec = None
        for uid in uids:
            if uid >= me:
                continue
            try:
                if ct.get_entity_type(uid) != EntityType.BUILDER_BOT:
                    continue
                if ct.get_team(uid) != self.team:
                    continue
                up = ct.get_position(uid)
            except Exception:
                continue
            if up.distance_squared(hpos) > GameConstants.BUILDER_BOT_VISION_RADIUS_SQ:
                continue
            if up.distance_squared(hpos) > mine_d:
                continue
            if ec is not None and up.distance_squared(ec) >= up.distance_squared(self.core):
                continue                      # a home body is not a claimant
            return False
        return True

    # ------------------------------------------------------------------
    # target selection
    # ------------------------------------------------------------------

    def _sip_plan(self, ct, hpos, rnd, bank, reserve, cost, budget):
        """(queue, terminus) for the cheapest legal tap on `hpos`, or None.

        The chain is routed by the incumbent trunk router, on purpose: it
        already blocks walls, ore, both core footprints, every non-belt
        building and every ENEMY belt, and it returns the path core-ward
        EXCLUDING its start tile.  So `[tap] + path` is a head-first chain
        whose every tile faces the next one, the tap included -- which is the
        facing rule, obtained by construction rather than by a special case.

        The chain is then truncated at the first tile already carrying one of
        OUR OWN belts that we can actually see: that tile is the terminus and
        everything past it is already built.  `k` therefore counts tiles we
        must BUY, which is what `SIPHON_MAX_CHAIN` and the funding test mean.
        """
        cands = []
        for dx, dy in CARD_DELTAS:
            tx, ty = hpos.x + dx, hpos.y + dy
            if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                continue
            if self.sip_ban is not None and self.sip_ban.get((tx, ty), 0) > rnd:
                continue
            d = abs(tx - self.core.x) + abs(ty - self.core.y)
            # Free pre-filter, no engine call and no flood: a BFS path is never
            # shorter than the Manhattan distance, so a face this far out cannot
            # come in under the chain cap even if the router is perfect.
            if d > SIPHON_MAX_CHAIN + SIP_CAND_SLACK:
                continue
            t = Position(tx, ty)
            if not self._sip_free_tile(ct, t):
                continue
            cands.append((d, tx, ty))
        if not cands:
            return None
        cands.sort()
        for _d, tx, ty in cands[:SIP_MAX_CAND]:
            if budget[0] <= 0:
                return None
            budget[0] -= 1
            tap = Position(tx, ty)
            try:
                path = self._link_path(ct, tap)
            except Exception:
                continue
            if not path:
                continue
            term = None
            cut = len(path)
            for i, t in enumerate(path[:20]):
                try:
                    if not ct.is_in_vision(t):
                        break
                    bid = ct.get_tile_building_id(t)
                except Exception:
                    break
                if bid is None:
                    continue
                try:
                    ours = (ct.get_team(bid) == self.team
                            and ct.get_entity_type(bid) in SIP_BELT_TYPES)
                except Exception:
                    break
                if ours:
                    term = t
                    cut = i
                break
            k = 1 + cut
            if k > SIPHON_MAX_CHAIN:
                self.sip_m_route += 1
                continue
            if bank - reserve < k * cost:
                self.sip_m_money += 1
                continue
            return [tap] + list(path[:cut]), term
        return None

    def _sip_scan(self, ct, rnd):
        """Look for a harvester worth tapping.  Never spends the turn."""
        try:
            p = ct.get_position()
            ids = ct.get_nearby_buildings()
        except Exception:
            return
        seen = []
        for bid in ids:
            try:
                if ct.get_entity_type(bid) != EntityType.HARVESTER:
                    continue
                if ct.get_team(bid) == self.team:
                    continue
                hpos = ct.get_position(bid)
            except Exception:
                continue
            d = p.distance_squared(hpos)
            if d > SIP_HARV_DSQ:
                continue
            seen.append((d, bid, hpos))
        if not seen:
            return
        seen.sort(key=lambda r: (r[0], r[1]))
        reserve = self._sip_reserve(ct)
        try:
            bank = ct.get_global_resources()
            cost = ct.get_conveyor_cost()
        except Exception:
            return
        budget = [SIP_ROUTE_BUDGET]
        for _d, _bid, hpos in seen[:SIP_MAX_HARV]:
            if budget[0] <= 0:
                return
            self.sip_m_seen += 1
            n, ours, ok = self._sip_acceptors(ct, hpos.x, hpos.y)
            if not ok or ours:
                continue                     # unknown, or we already tap it
            if n > SIPHON_MAX_N or n >= SIP_ABORT_A1_N:
                self.sip_m_n += 1
                continue
            if not self._sip_lowest_id(ct, hpos):
                self.sip_m_rival += 1
                continue
            plan = self._sip_plan(ct, hpos, rnd, bank, reserve, cost, budget)
            if plan is None:
                continue
            queue, term = plan
            self.sip_tap = queue[0]
            self.sip_harv = (hpos.x, hpos.y)
            self.sip_queue = queue
            self.sip_term = term
            self.sip_claimed = rnd
            self.sip_last_ext = rnd
            self.sip_built = 0
            self.sip_tap_live = False
            self.sip_stacks = set()
            self.sip_taps += 1
            return

    # ------------------------------------------------------------------
    # prospecting -- getting a body to where a tap is legal at all
    # ------------------------------------------------------------------

    def _sip_ore_target(self, ct):
        """Their ore field as an ORDERED SITE LIST, nearest home first.

        Enemy harvesters sit on ore (`engine_mechanics.md` A: no pool map has
        ore beside a core footprint, so every harvester is out in a field).  Of
        the tiles on THEIR side -- strictly nearer their anchor than ours -- the
        nearest home is the right place to look first: it is where their line
        starts, and it is the tap whose chain home is shortest, which is what
        the corpus ROI table rewards (cheb <= 6 taps take a median 13 stacks
        against 5-8 further out, siphon.md 4.2).  Sites are kept >= 3 tiles
        apart so the cursor cannot crawl across one patch a tile at a time.
        """
        if self.sip_ore_sites is None:
            sites = []
            if self.map_ores and self.core is not None:
                try:
                    ec = enemy_core_for(self.mw, self.mh, self.core)
                except Exception:
                    ec = None
                if ec is not None:
                    cx, cy = self.core.x, self.core.y
                    theirs = []
                    for o in self.map_ores:
                        dh = abs(o.x - cx) + abs(o.y - cy)
                        de = abs(o.x - ec.x) + abs(o.y - ec.y)
                        if de >= dh:
                            continue          # ours, or contested toward us
                        theirs.append((dh, o.x, o.y, o))
                    theirs.sort()
                    for _dh, ox, oy, o in theirs:
                        if len(sites) >= SIP_PROSPECT_SITES:
                            break
                        if any(max(abs(ox - s.x), abs(oy - s.y)) < 3 for s in sites):
                            continue
                        sites.append(o)
            self.sip_ore_sites = tuple(sites)
            self.sip_ore_i = 0
        if self.sip_ore_i >= len(self.sip_ore_sites):
            return None
        return self.sip_ore_sites[self.sip_ore_i]

    def _sip_ore_next(self, ct):
        self.sip_ore_i += 1
        return self._sip_ore_target(ct)

    def _sip_prospect(self, ct, rnd):
        """Walk the carrier to their ore field.  True iff it spent the turn.

        DEVIATION FROM `siphon.md` 4.1, stated plainly.  That section's carrier
        is a body whose forward trunk already runs along the victim's
        harvesters, so its trigger is simply "an enemy harvester is in vision".
        Our forward bodies are raiders and they stand on the enemy CORE ring;
        `get_nearby_buildings` is bounded by builder vision (r^2 = 20), and a
        smoke game on royale measured an enemy harvester in vision of an
        eligible body ZERO times in 413 rounds.  With no walk there is no
        denominator and F-S1.8 fires on a plank that was never tried.  So the
        walk is part of the arm, behind its own sub-flag, and it is bounded:
        ONE body, never before `arrival`, never the rider or E1/E2, at most
        `SIP_PROSPECT_RNDS` rounds in a lifetime, spent once.
        """
        if not SIP_PROSPECT_ON:
            return False
        tgt = self.sip_prospect
        if tgt is False:
            return False
        if tgt is None:
            tgt = self._sip_ore_target(ct)
            if tgt is None:
                self.sip_prospect = False
                return False
            self.sip_prospect = tgt
            self.sip_prospect_r0 = rnd
        if rnd - self.sip_prospect_r0 > SIP_PROSPECT_RNDS:
            self.sip_prospect = False
            if SIPHON_LOG:
                print("SIP giveup (%d,%d) r=%d" % (tgt.x, tgt.y, rnd))
                print("SIP miss seen=%d n=%d route=%d money=%d rival=%d r=%d" % (
                    self.sip_m_seen, self.sip_m_n, self.sip_m_route,
                    self.sip_m_money, self.sip_m_rival, rnd))
            return False
        try:
            p = ct.get_position()
        except Exception:
            return False
        if p.distance_squared(tgt) > 4:
            self.sip_hold_r0 = 0
            try:
                if ct.get_move_cooldown() != 0:
                    return True
            except Exception:
                return False
            self.tgt = tgt
            self._nav(ct, pave=False)
            return True
        # Standing on a site with nothing legal in sight.  Give it
        # SIP_PROSPECT_HOLD rounds -- the scan runs EVERY round while we are
        # here -- and then walk to the next site rather than stand still, which
        # is the worst possible use of the remaining budget.
        if self.sip_hold_r0 == 0:
            self.sip_hold_r0 = rnd
        elif rnd - self.sip_hold_r0 >= SIP_PROSPECT_HOLD:
            nxt = self._sip_ore_next(ct)
            if nxt is None:
                self.sip_prospect = False
                if SIPHON_LOG:
                    print("SIP giveup (%d,%d) r=%d" % (tgt.x, tgt.y, rnd))
                    print("SIP miss seen=%d n=%d route=%d money=%d rival=%d r=%d" % (
                        self.sip_m_seen, self.sip_m_n, self.sip_m_route,
                        self.sip_m_money, self.sip_m_rival, rnd))
                return False
            self.sip_prospect = nxt
            self.sip_hold_r0 = 0
            return True
        # Hand the otherwise-idle round to the incumbent zero-idle pass so it
        # still buys a heal or a trunk repair.
        if T5_ZERO_IDLE_ON:
            self._t5_zero_idle(ct)
        return True

    # ------------------------------------------------------------------
    # aborts and yield
    # ------------------------------------------------------------------

    def _sip_release(self, ct, rnd, why):
        """Drop the chain where it is.  Everything already laid keeps its
        buffer value (siphon.md 2.2), so release is never a loss."""
        if SIPHON_LOG:
            tap = self.sip_tap
            print("SIP drop %s (%d,%d) built=%d r=%d" % (
                why, -1 if tap is None else tap.x, -1 if tap is None else tap.y,
                self.sip_built, rnd))
        self.sip_queue = None
        self.sip_harv = None
        self.sip_term = None
        if self.tgt is not None and self.sip_tap is not None \
                and self.tgt.x == self.sip_tap.x and self.tgt.y == self.sip_tap.y:
            self.tgt = None

    def _sip_ban_tile(self, t, rnd):
        if self.sip_ban is None:
            self.sip_ban = {}
        self.sip_ban[(t.x, t.y)] = rnd + SIPHON_BAN_RNDS_TAP

    def _sip_watch_tap(self, ct, rnd):
        """Abort A2 + the yield marker + falsifiers F-S1.1 / F-S1.6 / F-S1.7.

        Everything here is read-only and costs at most three engine calls, and
        only while the tap tile is inside our vision.
        """
        tap = self.sip_tap
        if tap is None:
            return
        try:
            if not ct.is_in_vision(tap):
                return
            bid = ct.get_tile_building_id(tap)
        except Exception:
            return
        mine = False
        if bid is not None:
            try:
                mine = (ct.get_team(bid) == self.team
                        and ct.get_entity_type(bid) in SIP_BELT_TYPES)
            except Exception:
                mine = False
        if mine:
            self.sip_tap_live = True
            getter = getattr(ct, "get_stored_resource_id", None)
            if getter is None:
                return
            try:
                sid = getter(bid)
            except Exception:
                return
            if sid is None:
                return
            if self.sip_stacks is None:
                self.sip_stacks = set()
            if sid in self.sip_stacks:
                return
            self.sip_stacks.add(sid)
            if SIPHON_LOG:
                print("SIP yield (%d,%d) stacks=%d built=%d r=%d" % (
                    tap.x, tap.y, len(self.sip_stacks), self.sip_built, rnd))
            return
        if not self.sip_tap_live:
            return
        # It stood and now it does not: they shot it (they cannot destroy it).
        self.sip_tap_live = False
        if self.sip_kills is None:
            self.sip_kills = {}
        key = (tap.x, tap.y)
        hits = self.sip_kills.get(key)
        if hits is None:
            hits = []
            self.sip_kills[key] = hits
        hits.append(rnd)
        if len(hits) >= 2 and rnd - hits[-2] <= SIPHON_RETAP_WINDOW:
            self._sip_ban_tile(tap, rnd)
            if SIPHON_LOG:
                print("SIP ban (%d,%d) r=%d" % (tap.x, tap.y, rnd))

    def _sip_aborts(self, ct, rnd):
        """A1/A3/A5/A6.  True iff the chain survives this round."""
        # A5 -- survival outranks income.  The Core writes `max_hp - hp` into
        # the bleed beacon every round, which is the one fact a body outside
        # its own r^2 = 20 vision cannot obtain.
        if T4_BLEED_BEACON_ON:
            try:
                bleed = ct.read_store(SLOT_HEAL_BUDGET) & ARCH_BLEED_MASK
            except Exception:
                bleed = 0
            if bleed > GameConstants.CORE_MAX_HP - SIP_CORE_HP_HOME:
                self._sip_release(ct, rnd, "A5")
                return False
        # Hard lifetime on one claim.  A6 below is refreshed by the A4 money
        # pause on purpose, so this is what stops a permanently broke body
        # holding the role for the rest of the match.
        if rnd - self.sip_claimed > SIP_CLAIM_MAX_RNDS:
            self._sip_release(ct, rnd, "life")
            return False
        # A6 -- the chain has not grown; release the role so the next-lowest id
        # may adopt it.  This is the plank's expected failure mode against a
        # resident evictor and F-S1.7 is the bar that will say so.
        if rnd - self.sip_last_ext > SIPHON_STALL_RNDS:
            self._sip_release(ct, rnd, "A6")
            return False
        h = self.sip_harv
        if h is None:
            return True
        hp_ = Position(h[0], h[1])
        try:
            visible = ct.is_in_vision(hp_)
        except Exception:
            visible = False
        if not visible:
            return True
        # A3 -- the victim harvester died.  Drop the chain, never re-route.
        try:
            bid = ct.get_tile_building_id(hp_)
            alive = bid is not None and ct.get_entity_type(bid) == EntityType.HARVESTER \
                and ct.get_team(bid) != self.team
        except Exception:
            alive = True
        if not alive:
            self._sip_release(ct, rnd, "A3")
            return False
        # A1 -- they widened the round robin until our share is <= 25 %.  Stop
        # extending; keep every tile already laid.
        n, ours, ok = self._sip_acceptors(ct, h[0], h[1])
        if ok and (n - ours) >= SIP_ABORT_A1_N:
            self._sip_release(ct, rnd, "A1")
            return False
        return True

    # ------------------------------------------------------------------
    # the chain, head-first
    # ------------------------------------------------------------------

    def _sip_facing(self, tile, nxt):
        """Cardinal facing for `tile`: at the next chain tile, or -- for the
        last one -- at the terminus, or at our own core ring."""
        if nxt is None:
            nxt = self.sip_term
        if nxt is None:
            nxt = nearest_core_tile(tile, self.core)
        f = tile.cardinal_direction_to(nxt)
        if f == Direction.CENTRE:
            f = nearest_cardinal(tile.direction_to(nxt))
        if f == Direction.CENTRE:
            f = Direction.NORTH
        return f

    def _sip_trim(self, ct):
        """Pop tiles of the queue that are already one of our own belts."""
        q = self.sip_queue
        while q:
            t = q[0]
            try:
                bid = ct.get_tile_building_id(t)
            except Exception:
                return
            if bid is None:
                return
            try:
                ours = (ct.get_team(bid) == self.team
                        and ct.get_entity_type(bid) in SIP_BELT_TYPES)
            except Exception:
                return
            if not ours:
                return
            if len(q) == 1:
                self.sip_term = t
            q.pop(0)

    def _sip_run(self, ct, rnd):
        """Drive the committed chain.  True iff this turn is spent on it."""
        self._sip_watch_tap(ct, rnd)
        if not self._sip_aborts(ct, rnd):
            return False
        self._sip_trim(ct)
        if not self.sip_queue:
            if SIPHON_LOG:
                print("SIP chain done built=%d r=%d" % (self.sip_built, rnd))
            self._sip_release(ct, rnd, "done")
            return False
        tile = self.sip_queue[0]
        nxt = self.sip_queue[1] if len(self.sip_queue) >= 2 else None
        try:
            p = ct.get_position()
        except Exception:
            return False

        # A4 -- pause on money, never abandon.  Returning False leaves the
        # queue standing and lets the body do its ordinary raid work.
        try:
            bank = ct.get_global_resources()
            cost = ct.get_conveyor_cost()
        except Exception:
            return False
        if bank - self._sip_reserve(ct) < 2 * cost:
            # ABORT A4 -- pause, never abandon.  The pause must NOT count
            # toward A6: A6 is the eviction/blocked test ("release the role so
            # the next-lowest id may adopt it") and handing the role to another
            # body does not create money.  Keeping the two separable is what
            # lets the mechanism table say "no money" rather than "no logic",
            # which is the same distinction PLAN 2.3 F2.4 draws for A3.
            self.sip_last_ext = rnd
            return False

        try:
            acted = ct.get_action_cooldown() != 0
        except Exception:
            acted = True
        if not acted and abs(p.x - tile.x) + abs(p.y - tile.y) == 1:
            f = self._sip_facing(tile, nxt)
            built = False
            try:
                if ct.can_build_conveyor(tile, f):
                    ct.build_conveyor(tile, f)
                    built = True
            except Exception:
                built = False
            if built:
                first = (self.sip_built == 0)
                self.sip_built += 1
                self.sip_last_ext = rnd
                self.sip_queue.pop(0)
                if first:
                    self.sip_tap_live = True
                if SIPHON_LOG:
                    if first:
                        h = self.sip_harv or (-1, -1)
                        print("SIP tap (%d,%d) h=(%d,%d) f=%s k=%d r=%d" % (
                            tile.x, tile.y, h[0], h[1], f,
                            len(self.sip_queue) + 1, rnd))
                    else:
                        print("SIP link (%d,%d) left=%d r=%d" % (
                            tile.x, tile.y, len(self.sip_queue), rnd))
                return True

        try:
            if ct.get_move_cooldown() != 0:
                return True
        except Exception:
            return True
        # Walk to the tile we build the NEXT link from -- which is the next
        # chain tile itself, because conveyors are passable to both teams
        # (engine_mechanics.md G).  That is build / step / build: one conveyor
        # per two builder-rounds, siphon.md 1.3's measured cadence.
        stand = nxt if nxt is not None else self.sip_term
        if stand is None or (stand.x == p.x and stand.y == p.y):
            stand = tile
        if stand.x == p.x and stand.y == p.y:
            return True
        self.tgt = stand
        self._nav(ct, pave=False)
        return True

    # ------------------------------------------------------------------
    # entry point -- the arm's single call site
    # ------------------------------------------------------------------

    def _sip_tick(self, ct):
        if not SIPHON_ON or self.core is None:
            return False
        try:
            rnd = ct.get_current_round()
        except Exception:
            return False
        if not self._sip_geom(ct):
            return False
        # Band C never fires: 0.03 taps/game measured, 0 in 20 ragnarok +
        # drakkarfjord games, because the trunk is ~1.8 x c2c long.
        if self.sip_need > SIPHON_BAND_MAX_NEED:
            return False
        # F-S1.3, the hard tempo gate.  Nothing above this line has touched the
        # board, so a pre-arrival round costs one BFS-cached comparison.
        if rnd < self.sip_arrival or rnd < SIPHON_MIN_ROUND:
            return False
        if not self._sip_carrier_ok():
            return False
        if self._cpu_exhausted(ct):
            return False
        if self.sip_queue:
            return self._sip_run(ct, rnd)
        if self.sip_taps >= SIP_MAX_TAPS:
            return False
        # The scan is cadenced while we are still walking (nothing can be in
        # vision anyway) and every round once we are standing on the field,
        # because by then a harvester appearing is the whole point.
        onsite = self.sip_prospect not in (None, False)
        if onsite:
            try:
                onsite = ct.get_position().distance_squared(self.sip_prospect) <= 4
            except Exception:
                onsite = False
        if ((onsite and not (rnd + self.idx) % SIP_ONSITE_EVERY)
                or not (rnd + self.idx) % SIPHON_GATE_EVERY):
            self._sip_scan(ct, rnd)
            if self.sip_queue:
                self.sip_prospect = False
                return False
        return self._sip_prospect(ct, rnd)
