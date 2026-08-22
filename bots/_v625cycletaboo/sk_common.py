"""SKALMAN v1 -- shared infrastructure: bounds, store, displacement, pathing.

Import provenance (`docs/research/SKALMAN-IMPORT-MANIFEST-2026-08-21.md`):

  * `_cpu_exhausted`            VERBATIM  eco.py:444-464          (manifest §4.2)
  * `_flat_template`            VERBATIM  eco.py:902-917          (manifest §6.1)
  * `_nav_template`             VERBATIM  eco.py:919-930          (manifest §6.1)
  * `_bfs_direction`            VERBATIM  eco.py:2074-2267        (manifest §6.1)
      ⛔ ONE EDIT, and the manifest §6.3.2 requires it: the neighbour-order
        mirror was keyed on `self.idx & 1` (a RAID seat-parity tie-break so two
        raiders spread).  Re-keyed on `self.role_parity` so the four fixed
        roles do not inherit an arbitrary split.
  * `_nav`                      VERBATIM  eco.py:2271-2283, minus `pave`
  * `_move`                     REWRITTEN pave-free (manifest §6.3.1:
        `PAVE_TRAIL_ON = False` in the shipped benchmark, so both pave blocks
        are DEAD CODE there; cutting them drops _move 51 -> ~12 lines and the
        closure loses `_eco_spendable`, `pave_blocked`, `dist_core`,
        `nearest_core_tile`, `nearest_cardinal` and `SLOT_HARVESTERS`).
  * `pack_pos` / `unpack_pos`   VERBATIM  eco.py:237-244          (manifest §5.3.1)
  * geometry helpers            VERBATIM  eco.py:247-325
  * `in_bounds`                 NEW -- manifest item 2 is REWRITE-ADVISED: the
        benchmark ships no such helper in 19,596 lines and open-codes the rule
        at 71 sites.  BUILD RULE: every computed position passes through
        `in_bounds`/`self.ib` before any `get_tile_*` / `is_tile_*` /
        `can_build_*`.  `is_in_vision` is NEVER the guard (CLAUDE.md s50: it is
        a pure radius test, returned True for an off-map tile on atoll, and the
        next `get_tile_*` raised -- which permanently destroys the unit).
  * displacement guard          NEEDS-CUT eco/raid.py:205-225 -> the 7 generic
        lines, RE-SITED to the shared movement path (in the benchmark it lived
        only inside `_raid()`, the code SKALMAN deletes) and extended to clear
        EVERY cached plan, which the benchmark's does not do (manifest §3.3:
        "that is a latent defect, not a design; do not copy it").
"""

from fcode import Direction, EntityType, Environment, Position

from sk_maps import (
    BFS_BLOCKING_TYPES, CARDINALS, CARD_DELTAS, CARD_OPPOSITE,
    CPU_BUDGET_US,
    DELTA, NAV_NODE_BUDGET, SK_BEAT_MASK, SK_CYCLE_BREAK, SK_CYCLE_HIST,
    SK_DANGER_DETOUR_MAX, SK_DANGER_GUNNER_REACH, SK_DANGER_NAV,
    SK_DANGER_SENT_REACH, SK_ORE_SENSE, SK_SENSE_NAV, SK_STORE_MASK,
    SK_TELEPORT_DSQ,
    # --- v604 ---
    SK_CYCLE_HIST_K, SK_CYCLE_K, SK_CYCLE_K_MAX, SK_DANGER_COST, SK_DANGER_K,
    SK_DANGER_MAXCOST,
    # --- v605 ---
    SK_PATH_ARBITER, SK_PATH_ARBITER_BUDGET, SK_PATH_ARBITER_MEMO,
    SK_BLOCK_MEMO,
    # --- v606 ---
    SK_BLOCK_MEMO_EXPIRY, SK_BLOCK_TTL, SK_BLOCK_TTL_V605,
    SK_CAGE_WALKER, SK_DISENGAGE, SK_DISENGAGE_HP, SK_SIEGE_ENGINEER,
    SK_CAGE_CYCLE_TABOO, SK_CYCLE_TABOO_ROUNDS,
    # --- v607 ---
    SK_BLOCK_MEMO_SCOPE, SK_BLOCK_MEMO_DSQ, SK_HOME_KEEPER,
    SK_STALL_NETDISP, SK_STALL_W, SK_STALL_BOX, SK_STALL_MOVES,
    # --- v609 ---
    SK_COUNTER_SOFT_BODIES,
)


# ===========================================================================
# BOUNDS -- the helper the benchmark never had (manifest item 2)
# ===========================================================================

# v605 FIX 1: the 8-neighbourhood in CIRCULAR order.  Consecutive entries are
# CARDINALLY adjacent to one another (N/NE differ by one in x, NE/E by one in
# y, ...), which is what makes a contiguous run in this ring the same object as
# a locally connected group under builder-bot movement.  Order matters; do not
# sort it.
RING8 = ((0, -1), (1, -1), (1, 0), (1, 1),
         (0, 1), (-1, 1), (-1, 0), (-1, -1))


def in_bounds(x, y, w, h):
    return 0 <= x < w and 0 <= y < h


# ===========================================================================
# STORE -- pack/unpack (VERBATIM eco.py:237-244) and the masking idioms
# ===========================================================================

def pack_pos(pos):
    return ((pos.x + 1) << 16) | (pos.y + 1)


def unpack_pos(val):
    if not val:
        return None
    return Position((val >> 16) - 1, (val & 0xFFFF) - 1)


def pack_tile(pos):
    """Compact 10-bit position for bit-packed slots.  0 = unset.

    pack_pos costs the whole 32-bit word; a slot that also carries a beat
    cannot afford it.  Maps are <= 30x30 so 5 bits each is exact, and the +1
    keeps 0 meaning "unset" exactly as unpack_pos does.
    """
    return ((pos.x << 5) | pos.y) + 1


def unpack_tile(val):
    if not val:
        return None
    v = val - 1
    return Position(v >> 5, v & 31)


# ===========================================================================
# GEOMETRY (VERBATIM eco.py:247-325)
# ===========================================================================

def nearest_cardinal(d):
    return {
        Direction.NORTH: Direction.NORTH, Direction.NORTHEAST: Direction.EAST,
        Direction.EAST: Direction.EAST, Direction.SOUTHEAST: Direction.EAST,
        Direction.SOUTH: Direction.SOUTH, Direction.SOUTHWEST: Direction.SOUTH,
        Direction.WEST: Direction.WEST, Direction.NORTHWEST: Direction.WEST,
        Direction.CENTRE: Direction.NORTH,
    }[d]


def core_tiles(o):
    return [o, Position(o.x + 1, o.y), Position(o.x, o.y + 1), Position(o.x + 1, o.y + 1)]


def core_tiles_xy(o):
    ox, oy = o.x, o.y
    return ((ox, oy), (ox + 1, oy), (ox, oy + 1), (ox + 1, oy + 1))


def adjacent_to_core(p, o):
    ox, oy = o.x, o.y
    px, py = p.x, p.y
    for cx, cy in ((ox, oy), (ox + 1, oy), (ox, oy + 1), (ox + 1, oy + 1)):
        dx = px - cx
        if dx < 0:
            dx = -dx
        dy = py - cy
        if dy < 0:
            dy = -dy
        if dx + dy == 1:
            return True
    return False


def core_seats(o):
    """The eight DELIVERY SEATS of a 2x2 Core, in a CANONICAL order.

    ⛔ THE ORDER IS THE WHOLE POINT (v604 FIX 4).  These eight tiles are the
    only belt tiles whose identity can be shared through the 16-int store,
    because their index is a pure function of the Core anchor -- every body
    derives the same list without agreeing on anything else.  A belt PLAN index
    cannot do that: the plan is recomputed per body from per-body state, so
    "plan tile 7" means different tiles to different keepers, which is exactly
    the class of bug the store's one-writer discipline exists to prevent.

    N pair, E pair, S pair, W pair -- reading order within each pair.
    """
    ox, oy = o.x, o.y
    return ((ox, oy - 1), (ox + 1, oy - 1),
            (ox + 2, oy), (ox + 2, oy + 1),
            (ox, oy + 2), (ox + 1, oy + 2),
            (ox - 1, oy), (ox - 1, oy + 1))


def dist_core(pos, o):
    """Chebyshev distance from `pos` to the 2x2 Core footprint anchored at o."""
    ox, oy = o.x, o.y
    dx = pos.x - ox
    if dx < 0:
        dx = -dx
    elif dx > 1:
        dx -= 1
    else:
        dx = 0
    dy = pos.y - oy
    if dy < 0:
        dy = -dy
    elif dy > 1:
        dy -= 1
    else:
        dy = 0
    return dx if dx > dy else dy


def dsq_core(pos, o):
    """min(pos.distance_squared(c) for c in core_tiles(o)), without the list."""
    ox, oy = o.x, o.y
    dx = pos.x - ox
    if dx < 0:
        dx = -dx
    elif dx > 1:
        dx -= 1
    else:
        dx = 0
    dy = pos.y - oy
    if dy < 0:
        dy = -dy
    elif dy > 1:
        dy -= 1
    else:
        dy = 0
    return dx * dx + dy * dy


def core_ring(o):
    """The EIGHT orthogonally-adjacent tiles of a 2x2 footprint, in lap order.

    COPY 9 is denominated in "7 of 8", and this is that 8: two tiles per face.
    Returned clockwise starting north-west-most so a lap is `ring[(i+1) % 8]`.
    """
    ox, oy = o.x, o.y
    return [
        Position(ox, oy - 1), Position(ox + 1, oy - 1),      # north face
        Position(ox + 2, oy), Position(ox + 2, oy + 1),      # east face
        Position(ox + 1, oy + 2), Position(ox, oy + 2),      # south face
        Position(ox - 1, oy + 1), Position(ox - 1, oy),      # west face
    ]


# ===========================================================================
# THE TILE-OWNERSHIP ARBITER (ledger V2 + V8)
# ===========================================================================
# V8 measured 0.52 tiles/game rebuilt >= 5 times in the doctrine we replicate,
# worst 893 builds on ONE tile, and a 2-round barrier<->conveyor oscillation
# running 28+ rounds.  V2 measured 74% of lost ring barriers self-demolished.
# Both are one defect: two subroutines owning one tile.  SKALMAN answers with a
# single arbiter -- ONE map tile -> ONE owning verb -- consulted before every
# build and before every destroy.  It is deliberately geometric (not a
# registry) so it needs no store slot and cannot go stale.
OWNER_NONE = 0
OWNER_BELT = 1      # home half, on the globally planned belt
OWNER_CAGE = 2      # the 8 ring tiles of the ENEMY core
OWNER_NEST = 3      # the siege engineer's band site and its prep barriers
OWNER_DENY = 4      # ore tiles in the enemy half
OWNER_DOOR = 5      # the 8 ring tiles of OUR core (home clearance answers)


class CommonMixin:
    """Bounds, store, CPU, displacement and pathing.  Mixed into Player."""

    # ⭐ v609 GATE E -- CLASS-LEVEL DEFAULTS, and they are here rather than in
    # `_clear_plans` because `_bfs_direction` reads them on the FIRST turn of a
    # body whose plans have never been cleared.  Putting them only in
    # `_clear_plans` raised `AttributeError: 'Player' object has no attribute
    # 'nav_soft_bodies'` on every arm run and destroyed the unit -- caught by
    # the tape's own traceback gate on the first fire of this flag.
    nav_soft_bodies = False
    nav_held = False

    # --- bounds ------------------------------------------------------------

    def ib(self, x, y):
        return 0 <= x < self.mw and 0 <= y < self.mh

    def ibp(self, p):
        return 0 <= p.x < self.mw and 0 <= p.y < self.mh

    # --- store -------------------------------------------------------------

    def wstore(self, ct, slot, value):
        """The ONLY write path.  ⛔ write_store raises OverflowError -- NOT
        GameError -- on a negative or >2**32-1 value (manifest §5.3.2,
        double-probed), and an escaping exception destroys the unit
        permanently.  Masking here is what makes that unreachable, so no
        handler anywhere in this tree needs to narrow to OverflowError.
        """
        ct.write_store(slot, value & SK_STORE_MASK)

    def beat(self, ct, slot, rnd, field=0, mask=SK_BEAT_MASK):
        """Write an ABSOLUTE round+1 beat into `mask` at bit `field`."""
        cur = ct.read_store(slot)
        self.wstore(ct, slot,
                    (cur & ~(mask << field)) | (((rnd + 1) & mask) << field))

    def beat_fresh(self, ct, slot, rnd, stale, field=0, mask=SK_BEAT_MASK):
        """True if slot's beat exists and is younger than `stale` rounds."""
        b = (ct.read_store(slot) >> field) & mask
        if b == 0:
            return False
        return rnd - (b - 1) <= stale

    # --- CPU (VERBATIM eco.py:444-464) -------------------------------------

    def _cpu_exhausted(self, ct):
        """True once this unit has spent CPU_BUDGET_US of its 10 ms turn.

        An overrun truncates run() mid-statement at a boundary the engine
        picks; this lets the file pick one instead.  Reported once per unit
        lifetime to stderr (print() goes to the replay, not the console).

        ⚠ ct.get_cpu_time_elapsed() reads 0 under local `fcode run` even with
        --tle, so this guard has NEVER produced its other verdict locally.
        """
        try:
            if ct.get_cpu_time_elapsed() < CPU_BUDGET_US:
                return False
        except Exception:
            return False
        if not self.reported_cpu:
            self.reported_cpu = True
            import sys
            print(
                f"SK CPU-GUARD tripped: round={ct.get_current_round()} "
                f"elapsed_us={ct.get_cpu_time_elapsed()}",
                file=sys.stderr,
            )
        return True

    # --- displacement guard (manifest item 3, re-sited) --------------------

    def _displacement_guard(self, ct, p):
        """A launcher throws any adjacent builder from EITHER team, so a jump
        of more than one step since our last turn proves we were picked up.

        Re-sited to the SHARED movement path: in the benchmark this lived only
        inside `_raid()`, the one method SKALMAN deletes (manifest surprise 7).

        ⛔ AND IT CLEARS EVERY CACHED PLAN, which the benchmark's does not --
        it left `link_queue`/`samestop_*` stale, so a body thrown mid-wiring
        resumed a build queue for a place it no longer stands (manifest §3.3,
        surprise 8).  Registering the clear list here is what keeps the guard
        SUFFICIENT; the other half of the contract is manifest §3.4's
        no-cached-routes property -- `_bfs_direction` re-reads get_position()
        every call and caches only the target TILE, never a route.  BUILD RULE:
        no cross-round Position cache for a throwable body unless it is cleared
        here.
        """
        if self.prev_pos is not None and p.distance_squared(self.prev_pos) > SK_TELEPORT_DSQ:
            self.thrown_rnd = ct.get_current_round()
            self.tgt = None
            self.stuck = 0
            self._clear_plans()
        self.prev_pos = p
        # v602 FIX 3: the position ring the 2-cycle detector reads.  Recorded
        # BEFORE this round's move, so entry k is where the body DECIDED from.
        h = self.pos_hist
        h.append((p.x, p.y))
        # v604 FIX 2: the ring is twelve deep under SK_CYCLE_K so a period up to
        # SK_CYCLE_K_MAX can be seen TWICE.  SK_CYCLE_K off restores the v602
        # four-entry ring exactly (the ablation identity).
        cap = SK_CYCLE_HIST_K if SK_CYCLE_K else SK_CYCLE_HIST
        # v607 ITEM 4: the net-displacement detector reads a LONGER window than
        # the period detector, so the ring grows to hold it.  ⛔ THIS CANNOT
        # CHANGE `period_cycle()`: that reads only the last 2k entries and k is
        # capped at SK_CYCLE_K_MAX, so extra history behind them is unread.  The
        # `SK_STALL_NETDISP` OFF path keeps the v606 cap exactly.
        if SK_STALL_NETDISP and SK_STALL_W > cap:
            cap = SK_STALL_W
        while len(h) > cap:
            del h[0]

    def _clear_plans(self):
        """Every per-role plan cache, in one place (the guard's clear list)."""
        # v602 FIX 3: the position ring is a cross-round POSITION cache, so
        # build rule 5 puts it on the guard's clear list -- a thrown body's
        # A-B-A-B history describes a place it no longer stands.
        self.pos_hist = []
        self.cycle_len = 0
        self.cycle_blocked = 0
        self.cycle_taboo_tile = None
        self.cycle_taboo_until = -1
        self.danger_detour = 0
        # v604 FIX 2/3: both are cross-round decisions about a place the body no
        # longer stands, so both go on the guard's clear list (build rule 5).
        self.cycle_k = 0
        self.commit_until = -1
        # v609 GATE E: scoped nav flags.  `nav_soft_bodies` is set ONLY around
        # `_counter_march`'s own step_to and cleared right after (the sandbox
        # rejects `finally` blocks -- see sk_roles `_counter_march`); `nav_held`
        # reports back that the routed tile was plugged by a 1-round obstacle
        # and this body stood its ground rather than sidestepping.
        self.nav_soft_bodies = False
        self.nav_held = False
        self.commit_tgt = None
        self.cursor_kind = None       # CAGE WALKER: the one objective
        self.cursor_tile = None
        self.cursor_since = -1
        self.belt_cursor = None       # HOME KEEPER: next belt tile being laid
        self.lap_i = None             # CAGE WALKER: lap cursor
        self.melee_tile = None        # CAGE WALKER: ring tile being chewed
        self.melee_since = -1
        self.deny_tile = None         # ORE DENIER: ore tile being denied
        self.nest_site = None         # SIEGE ENGINEER: chosen gun tile
        self.nest_prepped = 0
        # v607 ITEM 1: an anchor tile and a "site we were holding" are both
        # cross-round POSITION caches about a place a thrown body no longer
        # stands, so build rule 5 puts them on this list beside `nest_site`.
        self.nest_anchor = None
        self.nest_anchor_rnd = -1
        self.nest_prev_site = None

    # --- templates (VERBATIM eco.py:902-930) -------------------------------

    def _flat_template(self, blocked_xy):
        w2 = self.mw + 2
        h2 = self.mh + 2
        t = bytearray(w2 * h2)
        last = (h2 - 1) * w2
        for x in range(w2):
            t[x] = 1
            t[last + x] = 1
        for y in range(h2):
            t[y * w2] = 1
            t[y * w2 + w2 - 1] = 1
        mw, mh = self.mw, self.mh
        for x, y in blocked_xy:
            if 0 <= x < mw and 0 <= y < mh:
                t[(y + 1) * w2 + x + 1] = 1
        return t

    def _memo_nav_on(self, target_dsq=None):
        """v607 ITEM 3 -- is the blocker memo consulted for THIS flood?

        v606 proved the memo's MECHANISM (helheim orbit 58r -> 18r) and removed
        its death cost (the missing expiry), and still shipped it OFF: as a
        GLOBAL it cost +38 rounds of median kill.  The hypothesis this predicate
        exists to test is that the cost and the product live in different
        places -- the product is on LONG FORWARD routes where the flood forgets
        a blocker between two adjacent tiles, the cost is on SHORT HOME routes
        where a remembered blocker is a stale commitment around the belt.
          scope 0  ALL          -- v605/v606's global form, the measured -38.
          scope 1  FORWARD      -- every role except the HOME KEEPER, whose
                                   routes are short and whose logistics paid the
                                   commitment cost.
          scope 2  FAR          -- any role, but only when the target is beyond
                                   SK_BLOCK_MEMO_DSQ: long routes need memory,
                                   short ones need freshness.
        ⚠ DISCLOSED: `target_dsq is None` is the route-feasibility caller
        (`_route_blocked`), which has no walking target.  Under scope 2 it keeps
        the memo, because that flood asks "does a route exist at all" -- a
        board-scale question, which is the same class scope 2 is selecting for.
        """
        if not SK_BLOCK_MEMO:
            return False
        if SK_BLOCK_MEMO_SCOPE == 1:
            return self.role != SK_HOME_KEEPER
        if SK_BLOCK_MEMO_SCOPE == 2:
            return target_dsq is None or target_dsq > SK_BLOCK_MEMO_DSQ
        return True

    def _nav_template(self, use_memo=False):
        """(w2, template) for `_bfs_direction`: border + walls + both Cores.

        The blocked 1-tile border IS the bounds test, so the inner flood runs
        no comparison at all (manifest §6.5: lift `_bfs_direction` without this
        and the bounds test silently disappears from the hot loop).
        """
        # v601: `len(self.map_walls)` is IN THE KEY.  Without a confirmed grid
        # the wall set GROWS as the body sees more of the board, and a template
        # cached on (core, enemy, w, h) alone would freeze the first, emptiest
        # version of the map for the whole match.
        # v605 FIX 2: `_block_rev` IS IN THE KEY for exactly the reason
        # `len(self.map_walls)` is -- the template must rebuild when the set of
        # things it blocks changes, and the blocker memo changes far more often
        # than the wall set does.
        # ⭐ v607 ITEM 3: `use_memo` IS IN THE KEY, for the same reason
        # `_block_rev` is.  The conditional forms decide PER CALL whether the
        # memo is consulted, so a template cached without it would serve a
        # memo-free flood to a memo-on caller (and the other way round) for as
        # long as nothing else in the key moved.
        key = (self.core, self.enemy, self.mw, self.mh, len(self.map_walls),
               self._block_rev, use_memo)
        if self._nav_key != key:
            hit = self._nav_alt.get(bool(use_memo))
            if hit is not None and hit[0] == key:
                self._nav_key, self._nav_tpl = hit
                return self.mw + 2, self._nav_tpl
            blocked = set(self.map_walls)
            if use_memo:
                blocked.update(self.block_memo)
            if self.core is not None:
                blocked.update(core_tiles_xy(self.core))
            if self.enemy is not None:
                blocked.update(core_tiles_xy(self.enemy))
            self._nav_tpl = bytes(self._flat_template(blocked))
            self._nav_key = key
            # ⛔ v607 ITEM 3, CPU: TWO SLOTS, NOT ONE.  Under a conditional scope
            # two callers in the SAME round can want different templates
            # (`_route_blocked` with the memo, a short-target flood without it),
            # and a single-slot cache would rebuild the whole padded grid on
            # every alternation -- a per-call O(w*h) cost inside a 10 ms turn.
            # The second slot makes the alternation free; the key still decides.
            self._nav_alt[bool(use_memo)] = (key, self._nav_tpl)
        return self.mw + 2, self._nav_tpl

    # --- v605 FIX 2: the BLOCKER MEMO (SK_BLOCK_MEMO) ----------------------

    def _block_update(self, ct, p, seen, rnd):
        """Fold one entity pass into the per-unit blocker memo.

        `seen` is EVERY impassable building this body can see right now, from
        the single `get_nearby_entities` walk `_bfs_direction` already makes --
        so both halves of the memo are free of extra engine calls:
          ADD    every tile in `seen`;
          FORGET every remembered tile INSIDE the vision disc that is not in
                 `seen` (a blocker there would have been in the list we just
                 read), and every tile whose newest sighting is older than the
                 TTL wherever it is.
        `_block_rev` is bumped only when membership actually changes, because it
        keys the nav template and a per-round bump would rebuild it every call.

        v606 ITEM 3: the TTL is SK_BLOCK_TTL (40) when SK_BLOCK_MEMO_EXPIRY is
        on and SK_BLOCK_TTL_V605 (150, v605's value) when it is off -- the whole
        v606 delta to this verb, so the expiry can be ablated on its own.
        """
        if not SK_BLOCK_MEMO:
            return
        try:
            vis = ct.get_vision_radius_sq()
        except Exception:
            return
        ttl = SK_BLOCK_TTL if SK_BLOCK_MEMO_EXPIRY else SK_BLOCK_TTL_V605
        memo = self.block_memo
        changed = False
        for xy in seen:
            if xy not in memo:
                changed = True
            memo[xy] = rnd
        px, py = p.x, p.y
        for xy in list(memo):
            if xy in seen:
                continue
            dx = xy[0] - px
            dy = xy[1] - py
            if dx * dx + dy * dy <= vis or rnd - memo[xy] > ttl:
                del memo[xy]
                changed = True
        if changed:
            self._block_rev += 1

    # --- v602 FIX 2: the danger term (SK_DANGER_NAV) -----------------------

    def _danger_tiles(self):
        """The tiles remembered enemy turrets COVER.  Empty when the flag is off.

        ⛔ THE DEFECT THIS FIXES.  `self.armed_memo` (written `sk_roles._sense`)
        has recorded every seen enemy ARMED tile since v601, keyed on the tile
        because a turret is a building and cannot move -- and its only two
        consumers were `_infer_killer` and `_killer_dead`.  NO MOVER READ IT.
        On fimbulwinter seat A the bot knew gunner (8,7) from r43 onward and
        walked 42 bodies into its two-tile ray, 39 of which died there.

        A RAY, NOT A DISC (the same distinction PLANK 2's siting turns on): a
        gunner covers the line along its facing out to r^2 13, a sentinel to
        r^2 32.  Facing comes from `armed_facing`, read once per turret (a
        sentinel cannot rotate; a gunner can, which is why an UNKNOWN facing is
        priced as all four cardinals rather than as safe).

        ⛔ OBSTACLES ARE NOT MODELLED, deliberately: a gunner's shot is blocked
        by terrain and a sentinel's is not, so the unblocked ray is a SUPERSET
        of what a gunner can really hit.  Over-marking costs a detour; under-
        marking costs a body.  The cache is keyed on `_armed_rev`, bumped by
        `_sense` on every new tile or new facing, so it rebuilds only on news.
        """
        if not SK_DANGER_NAV:
            return frozenset()
        if self._danger_key == self._armed_rev:
            return self._danger_set
        out = set()
        for xy, v in self.armed_memo.items():
            et = v[0]
            if et == EntityType.GUNNER:
                reach = SK_DANGER_GUNNER_REACH
            elif et == EntityType.SENTINEL:
                reach = SK_DANGER_SENT_REACH
            else:
                continue                    # a launcher shoots nothing
            f = self.armed_facing.get(xy)
            rays = (f,) if f is not None else ((0, -1), (1, 0), (0, 1), (-1, 0))
            for ray in rays:
                dx, dy = ray
                if dx == 0 and dy == 0:
                    continue
                step = dx * dx + dy * dy
                k = 1
                while k * k * step <= reach:
                    qx = xy[0] + dx * k
                    qy = xy[1] + dy * k
                    if not self.ib(qx, qy):
                        break
                    out.add((qx, qy))
                    k += 1
        self._danger_key = self._armed_rev
        self._danger_set = out
        return out

    # --- v602 FIX 3: the 2-cycle detector (SK_CYCLE_BREAK) -----------------

    def _two_cycle_back(self):
        """The tile a 2-cycle would send us back to, or None.

        A-B-A-B over four consecutive recorded positions.  Endemic, measured on
        BOTH bots and BOTH seats (81.3% / 97.9% of v601 builder steps on
        fimbulwinter, 91.0% / 72.7% for the v600 control): the greedy step tie
        breaks horizontally, the blocked side's fallback offers the OPPOSITE
        direction, and the pair repeats forever.  All four stavkirke seat-B
        builders spent 1000 rounds in one and built nothing.
        """
        if not SK_CYCLE_BREAK:
            return None
        h = self.pos_hist
        if len(h) < 4:
            return None
        if h[-1] == h[-3] and h[-2] == h[-4] and h[-1] != h[-2]:
            return h[-2]
        return None

    # --- v604 FIX 2: the period-k detector (SK_CYCLE_K) ---------------------

    def period_cycle(self):
        """The period k of a repeating position cycle, or 0.

        ⛔ WHY A SECOND DETECTOR RATHER THAN A WIDER `_two_cycle_back`.  The two
        answer different questions and have different responses.  `_two_cycle_back`
        asks "is my NEXT STEP the one I just undid" and answers with a step to
        strike out; that is a STEPPING fix and it is right for period 2, where the
        pair really is one tie-break fighting one fallback.  This asks "has my
        BODY been on a closed orbit for two full laps", and the measured period-6
        to period-10 orbits are not a stepping bug at all -- they are two
        TARGETING authorities each undoing the other's decision (v603 diag:
        midgard_A, the forward lap tile blocked by an enemy body for 41 rounds,
        the one-step detour re-picked away by the off-lap seal pool every round).
        A step-level answer cannot fix that; the caller's answer is to COMMIT to
        one target for k + SK_CYCLE_COMMIT_SLACK rounds.

        Two full repeats are required (2k history entries), because a lap that
        legitimately circles an 8-seat ring revisits tiles once by design.  A
        degenerate all-one-tile window is NOT a cycle -- a body standing still is
        `stuck`, which has its own counter and its own answer.
        """
        if not SK_CYCLE_K:
            return 0
        h = self.pos_hist
        n = len(h)
        for k in range(2, SK_CYCLE_K_MAX + 1):
            if n < 2 * k:
                break
            ok = True
            for i in range(1, k + 1):
                if h[-i] != h[-i - k]:
                    ok = False
                    break
            if not ok:
                continue
            win = h[-k:]
            if len(set(win)) < 2:
                return 0            # standing still, not orbiting
            return k
        return 0

    def netdisp_stall(self):
        """v607 ITEM 4 -- an orbit detected by NET DISPLACEMENT, not by period.

        ⛔ WHY NOT A WIDER k.  v606 built exactly that (`SK_CYCLE_K_MAX` 6 -> 10,
        ring 12 -> 20) and it was an EXACT NULL -- 30 byte-identical replays --
        because the orbit that survived on the diagnosed cell has period TWELVE.
        Extending k again is a measured dead end and this item does not.
        THE MEASUREMENT THAT SET THESE CONSTANTS (s55, `orbit_geom.py`, all 30
        games of the v606 shipped tape, 24 labelled period-k episodes of >= 30
        rounds):
          * box, i.e. max(dx, dy) of a 24-round window, is DEAD CONSTANT inside
            an episode -- coverage is 0% or 100% per episode, never in between.
            B1 8/24 · B2 16/24 · **B3 20/24** · B4 22/24 · B5 22/24.
          * ⛔ B = 2 IS REFUTED BY THE CELL THE ITEM NAMES.  fimbulwinter seat A
            bot 8 (ORE_DENIER, k=12, 130 rounds) has box 3 in EVERY one of its
            107 windows -- `max(dx,dy) <= 2` covers it 0% of the time.  The
            brief's constant would have shipped a detector blind to its own
            headline cell.
          * the two episodes B3 misses are 1-tile-wide SHUTTLES with boxes of 8
            and 10.  No net-displacement threshold reaches them; the period
            detector does, which is why BOTH stay.
          * the move test is nearly free: every one of the 24 episodes moves >= 17
            of a possible 23 rounds.  Its whole job is excluding a body that is
            STANDING STILL (that is `stuck`'s counter, not this one) and it does
            that completely -- pure standing-still fires are 0 at every M >= 8,
            against 5,430 windows that the box test ALONE would sweep in.
          * overlap with the shipped period detector is 31.8%; 68.2% of fires are
            new, and the shipped k<=6 sees >= half the windows of only 5 of the
            24 episodes.  This is a different net, not a refinement.
        ⚠ AND THE ONE SOFT SPOT, on the record: 66 of 99 fire episodes land on a
        body whose lifetime action rate is >= 0.05 acts/round -- it is CIRCLING
        WHILE BUILDING.  Movement-only, the false-positive rate is 6.7%; counting
        "productive" as false it is 67%.  That is why the response is the commit
        window and nothing heavier: freezing the MOVEMENT target is idempotent
        and touches no in-flight build plan.
        """
        if not SK_STALL_NETDISP:
            return False
        h = self.pos_hist
        n = len(h)
        if n < SK_STALL_W:
            return False
        win = h[-SK_STALL_W:]
        xs = [q[0] for q in win]
        ys = [q[1] for q in win]
        if max(xs) - min(xs) > SK_STALL_BOX or max(ys) - min(ys) > SK_STALL_BOX:
            return False
        moves = 0
        prev = win[0]
        for q in win:
            if q != prev:
                moves += 1
            prev = q
        return moves >= SK_STALL_MOVES

    # --- v604 FIX 1: danger as a PATH COST (SK_DANGER_COST) ----------------

    def _danger_mask(self, w2, h2):
        """`_danger_tiles()` as a flat mask over the padded nav grid, or None.

        None means "no danger term this call" and the caller takes the plain
        unweighted flood -- which is the fast path and the common one, so the
        weighted machinery costs nothing until a turret has actually been seen.
        """
        if not SK_DANGER_COST:
            return None
        danger = self._danger_tiles()
        if not danger:
            return None
        key = (self._danger_key, w2, h2)
        if self._dmask_key == key:
            return self._dmask
        m = bytearray(w2 * h2)
        mw, mh = self.mw, self.mh
        for xy in danger:
            x, y = xy
            if 0 <= x < mw and 0 <= y < mh:
                m[(y + 1) * w2 + x + 1] = 1
        self._dmask_key = key
        self._dmask = m
        return m

    def _weighted_flood(self, st, w2, start, flat, oi, dmask, budget, K=None):
        """Dial's algorithm over the same padded byte grid: entering a covered
        tile costs 1 + SK_DANGER_K instead of being refused.

        ⛔ WHY NOT THE CHEAPER TWO-PASS FORM (flood danger-free, and only if the
        goal is unreachable re-flood allowing danger).  That form prices a
        covered tile at INFINITY-or-zero: it takes a sixty-step detour to avoid
        one covered tile, and the KILL_TARGET is a median kill round of 180.  A
        real cost is what makes "cross one covered tile" and "walk around the
        map" comparable at all, and K is the exchange rate.

        Edge weights are 1 and 1 + K, so K + 2 circular buckets are exactly
        enough: draining bucket d can only insert into d+1 .. d+1+K, and
        (d+1+K) mod (K+2) == (d-1) mod (K+2), the slot drained one step ago.

        Returns (Direction, nodes) when a goal is settled, (None, nodes) when no
        goal is reachable at all, and (False, nodes) when the node budget or the
        cost cap was hit -- the caller answers the last two the same way the
        unweighted flood does.
        """
        # v609 GATE E passes its own K (bodies are priced, not walled); every
        # other caller keeps the shipped danger exchange rate.
        if K is None:
            K = SK_DANGER_K
        nb = K + 2
        size = len(st)
        dc = bytearray([255]) * size          # 255 = unreached
        fs = bytearray(size)                  # first cardinal index of the route
        buckets = [[] for _ in range(nb)]
        pending = 0
        # ⛔ SEEDED IN REVERSE PREFERENCE ORDER: the buckets are LIFO, so this is
        # what makes the preferred direction settle FIRST at equal cost, i.e. it
        # reproduces the unweighted flood's `oi` tie-break instead of inverting it.
        for j in (3, 2, 1, 0):
            di = oi[j]
            n = start + flat[di]
            if st[n] == 1:
                continue
            c = 1 + (K if dmask[n] else 0)
            if c >= dc[n]:
                continue
            dc[n] = c
            fs[n] = di
            buckets[c % nb].append(n)
            pending += 1
        nodes = 0
        d = 0
        while pending > 0:
            b = buckets[d % nb]
            while b:
                node = b.pop()
                pending -= 1
                if dc[node] != d:
                    continue                  # superseded by a cheaper route
                if st[node] == 2:
                    return CARDINALS[fs[node]], nodes
                st[node] = 1                  # settled
                nodes += 1
                if nodes > budget:
                    return False, nodes
                f = fs[node]
                d1 = d + 1
                dk = d1 + K
                for fl in flat:
                    n = node + fl
                    if st[n] == 1:
                        continue
                    c = dk if dmask[n] else d1
                    if c >= dc[n] or c >= SK_DANGER_MAXCOST:
                        continue
                    dc[n] = c
                    fs[n] = f
                    buckets[c % nb].append(n)
                    pending += 1
            d += 1
            if d >= SK_DANGER_MAXCOST:
                return False, nodes
        return None, nodes

    # --- the flood (VERBATIM eco.py:2074-2267, one re-key) -----------------

    def _bfs_direction(self, ct, target):
        """One exact static-terrain step toward target, visible units avoided.

        Padded-flat-bytearray BFS.  The state byte is 0 = free, 1 = blocked or
        already seen, 2 = goal.  Two passes: pass 0 treats builder bodies (both
        teams) as blocked, pass 1 retries body-free if pass 0 found no goal --
        BOTH charged to ONE NAV_NODE_BUDGET.  The CPU probe is asked once per
        CALL, up front, never per pass and never mid-flood.

        Returns a STEP, never a route (manifest §3.4) -- which is what keeps
        the displacement guard sufficient.
        """
        p = ct.get_position()
        # ⛔ v602 FIX 5(a).  v601 read `if self.map_grid is None: return greedy`
        # -- and `known_map_for` returns None on 10 of the 15 pool maps, so on
        # two thirds of the pool NAVIGATION HAD NO WALL KNOWLEDGE AT ALL, every
        # call, all game.  That is the shared upstream of the fimbulwinter storm
        # (§2.5: the flood never ran, greedy walked into a wall, the fallback
        # produced the 2-cycle).  `map_walls` is filled from the catalogue grid
        # when there is one and from `_ore_scan`'s live sensing otherwise;
        # `terrain_known()` is the same >= 8 sensed-tiles gate the belt planner
        # uses, and UNSEEN reads as passable exactly as it does there.
        if self.map_grid is None and not (SK_SENSE_NAV and self.terrain_known()):
            return p.cardinal_direction_to(target)
        mw, mh = self.mw, self.mh
        tx, ty = target.x, target.y
        if not (0 <= tx < mw and 0 <= ty < mh):
            return p.cardinal_direction_to(target)

        # ⭐ v605 FIX 2 REORDERED THIS: the entity pass now runs BEFORE the
        # template is asked for, because it feeds the blocker memo and the memo
        # is IN the template.  Same single `get_nearby_entities` walk, same
        # engine calls -- only the order and the destinations changed.
        bodies_xy = []
        cores_xy = []
        seen_blk = set()
        scanned = False
        try:
            me = ct.get_id()
            for eid in ct.get_nearby_entities():
                if eid == me:
                    continue
                et = ct.get_entity_type(eid)
                ep = ct.get_position(eid)
                if et == EntityType.CORE:
                    cores_xy.append(ep)
                elif et == EntityType.BUILDER_BOT:
                    ex, ey = ep.x, ep.y
                    if 0 <= ex < mw and 0 <= ey < mh:
                        bodies_xy.append((ex, ey))              # both teams
                elif et in BFS_BLOCKING_TYPES:
                    ex, ey = ep.x, ep.y
                    if 0 <= ex < mw and 0 <= ey < mh:
                        seen_blk.add((ex, ey))
                # ⛔⛔ DO NOT BLOCK CONVEYOR / SPLITTER HERE.  It was tried in
                # this build, on the tape601 autopsy's latent note 1 ("the flood
                # treats our own belt as walkable and emits steps the engine
                # refuses"), AND THE ENGINE SAYS OTHERWISE.  Measured s54 on
                # glacierkeep r200-201, our own keeper, `_v602skalman` debug
                # copy, four cardinal neighbours printed:
                #     (15,12) building=163 CONVEYOR env=EMPTY
                #             is_tile_passable=True   can_move=True
                #     (15,14) building=161 HARVESTER env=ORE
                #             is_tile_passable=False  can_move=False
                # ⇒ A BUILDER BOT CAN WALK ONTO A FRIENDLY CONVEYOR TILE.  The
                # note is refuted; the flood was right.  Blocking them cost a
                # 250-ROUND FREEZE: `_home_keeper_move`'s step-off branch picked
                # the (passable) conveyor tile, `_bfs_direction` then answered
                # CENTRE because its goal was blocked and the body already stood
                # on one of the goal's neighbours, and the keeper never moved
                # again (glacierkeep, r155 to the end of the match).
            scanned = True
        except Exception:
            pass

        # ⛔ THE MEMO IS ONLY UPDATED ON A SCAN THAT COMPLETED.  A partial walk
        # would have a short `seen_blk`, and the FORGET half reads an absence as
        # evidence -- so a raised call must not be allowed to erase memory.
        if scanned:
            try:
                self._block_update(ct, p, seen_blk, ct.get_current_round())
            except Exception:
                pass

        # v607 ITEM 3: the conditional memo is decided HERE, where the target is
        # known, and nowhere else.
        w2, tpl = self._nav_template(self._memo_nav_on(p.distance_squared(target)))
        base = bytearray(tpl)
        for ep in cores_xy:
            for cx, cy in core_tiles_xy(ep):
                if 0 <= cx < mw and 0 <= cy < mh:
                    base[(cy + 1) * w2 + cx + 1] = 1
        for ex, ey in seen_blk:
            base[(ey + 1) * w2 + ex + 1] = 1
        bodies = [(ey + 1) * w2 + ex + 1 for ex, ey in bodies_xy]

        start = (p.y + 1) * w2 + p.x + 1
        base[start] = 0
        if bodies:
            bodies = [bi for bi in bodies if bi != start]

        desired = p.cardinal_direction_to(target)
        if desired in CARDINALS:
            i = CARDINALS.index(desired)
            # ⛔ RE-KEY (manifest §6.3.2): the benchmark mirrored on
            # `self.idx & 1`, a raid seat-parity tie-break so two raiders
            # spread rather than trail.  SKALMAN's four bodies are fixed roles,
            # so it is keyed on the role instead.
            side = 1 if (self.role_parity & 1) else -1
            oi = (i, (i + side) % 4, (i - side) % 4, CARD_OPPOSITE[i])
        else:
            oi = (0, 1, 2, 3)
        flat = (-w2, 1, w2, -1)             # CARDINALS order: N, E, S, W
        d0, d1, d2, d3 = flat[oi[0]], flat[oi[1]], flat[oi[2]], flat[oi[3]]

        tidx = (ty + 1) * w2 + tx + 1
        nodes = 0                           # ONE budget across BOTH passes
        cpu_checked = False
        # v604 FIX 1: None on the fast path (flag off, or no turret ever seen).
        dmask = self._danger_mask(w2, len(tpl) // w2)
        for _pass in (0, 1):
            if _pass == 1 and not bodies:
                break
            soft = SK_COUNTER_SOFT_BODIES and self.nav_soft_bodies and bool(bodies)
            st = bytearray(base)
            if _pass == 0 and not soft:
                for bi in bodies:
                    st[bi] = 1

            goals = []
            if st[tidx] == 0:
                goals.append(tidx)
            elif target == self.core or target == self.enemy:
                for cx, cy in core_tiles_xy(target):
                    for dx, dy in CARD_DELTAS:
                        qx, qy = cx + dx, cy + dy
                        if not (0 <= qx < mw and 0 <= qy < mh):
                            continue
                        if tx <= qx <= tx + 1 and ty <= qy <= ty + 1:
                            continue
                        gi = (qy + 1) * w2 + qx + 1
                        if st[gi] == 0:
                            goals.append(gi)
            else:
                for dx, dy in CARD_DELTAS:
                    qx, qy = tx + dx, ty + dy
                    if not (0 <= qx < mw and 0 <= qy < mh):
                        continue
                    gi = (qy + 1) * w2 + qx + 1
                    if st[gi] == 0:
                        goals.append(gi)
            if start in goals:
                return Direction.CENTRE
            if not goals:
                continue
            for gi in goals:
                st[gi] = 2
            st[start] = 1

            if not cpu_checked:
                cpu_checked = True
                if self._cpu_exhausted(ct):
                    return p.cardinal_direction_to(target)

            if soft and _pass == 0:
                # ⭐ v609 GATE E.  A builder body is a 1-round obstacle, not a
                # wall: price it through the SAME Dial's flood the danger mask
                # already uses, at K = 2.  This is what stops one transient body
                # entering vision from flipping the route between two homotopy
                # classes on alternating tiles (bifrost seat A: (3,8) says EAST,
                # (4,8) says WEST, 53 rounds, zero net displacement).  Danger, if
                # live, is priced at the same K here -- the march's target is a
                # turret, so its ray is entered by construction.
                bm = (bytearray(dmask) if dmask is not None
                      else bytearray(len(st)))
                for bi in bodies:
                    bm[bi] = 1
                got, used = self._weighted_flood(
                    st, w2, start, flat, oi, bm, NAV_NODE_BUDGET - nodes, 2)
                nodes += used
                if got is False:
                    return p.cardinal_direction_to(target)
                if got is not None:
                    return got
                continue

            if dmask is not None:
                # v604 FIX 1.  Same budget, same passes, same greedy fallback --
                # only the edge weights change.
                got, used = self._weighted_flood(
                    st, w2, start, flat, oi, dmask, NAV_NODE_BUDGET - nodes)
                nodes += used
                if got is False:
                    return p.cardinal_direction_to(target)
                if got is not None:
                    return got
                continue                    # no goal this pass; try body-free

            cur = []
            cf = []
            for j in (0, 1, 2, 3):
                n = start + flat[oi[j]]
                v = st[n]
                if v == 0:
                    st[n] = 1
                    cur.append(n)
                    cf.append(j)
                elif v == 2:
                    return CARDINALS[oi[j]]
            nodes += len(cur)
            while cur:
                nxt = []
                nf = []
                for k in range(len(cur)):
                    node = cur[k]
                    f = cf[k]
                    n = node + d0
                    v = st[n]
                    if v == 0:
                        st[n] = 1
                        nxt.append(n)
                        nf.append(f)
                    elif v == 2:
                        return CARDINALS[oi[f]]
                    n = node + d1
                    v = st[n]
                    if v == 0:
                        st[n] = 1
                        nxt.append(n)
                        nf.append(f)
                    elif v == 2:
                        return CARDINALS[oi[f]]
                    n = node + d2
                    v = st[n]
                    if v == 0:
                        st[n] = 1
                        nxt.append(n)
                        nf.append(f)
                    elif v == 2:
                        return CARDINALS[oi[f]]
                    n = node + d3
                    v = st[n]
                    if v == 0:
                        st[n] = 1
                        nxt.append(n)
                        nf.append(f)
                    elif v == 2:
                        return CARDINALS[oi[f]]
                nodes += len(nxt)
                if nodes > NAV_NODE_BUDGET:
                    return p.cardinal_direction_to(target)
                cur = nxt
                cf = nf
            continue
        return p.cardinal_direction_to(target)

    # --- movement (VERBATIM _nav; _move rewritten pave-free) ---------------

    def _nav(self, ct):
        """One step toward self.tgt.  Returns True iff the body actually moved.

        ⭐ v602 REWRITE, and the return value is load-bearing: FIX 1 lets the
        cage walker peck ONLY when it has no lap action, and "the lap advance
        did not happen" is a fact only this method knows.  v601 returned None
        from every path.

        Two terms are added around the v601 candidate order (desired, the two
        perpendiculars, the opposite):
          * FIX 3 -- if the last four recorded positions are A-B-A-B, the step
            BACK is struck out and the perpendiculars are tried first.  With
            neither available the body HOLDS: standing still for one round is
            cheaper than another lap of a shuttle, and holding also breaks the
            alternation, so the detector switches itself off next round rather
            than latching.
          * FIX 2 -- a step onto a tile a remembered enemy turret covers is
            taken only when no uncovered step exists (or the detour budget is
            spent, `SK_DANGER_DETOUR_MAX`).
        """
        if self.tgt is None or ct.get_move_cooldown() != 0:
            return False
        desired = self._bfs_direction(ct, self.tgt)
        if desired == Direction.CENTRE:
            return False
        p = ct.get_position()
        idx = CARDINALS.index(desired) if desired in CARDINALS else 0
        cands = [CARDINALS[idx], CARDINALS[(idx + 1) % 4],
                 CARDINALS[(idx + 3) % 4], CARDINALS[(idx + 2) % 4]]
        back = self._two_cycle_back()
        if back is not None:
            self.cycle_len += 1
            # perpendicular FIRST: the desired direction is the one the tie
            # break keeps choosing, and the opposite is the return leg.
            cands = [CARDINALS[(idx + 1) % 4], CARDINALS[(idx + 3) % 4],
                     CARDINALS[idx], CARDINALS[(idx + 2) % 4]]
        else:
            self.cycle_len = 0
            self.cycle_blocked = 0
        # ⭐ v604 FIX 1.  WITH THE COST FORM LIVE THE STEP-LEVEL RE-RANK IS THE
        # BUG, NOT THE FIX.  `safe + risky` here means ANY legal step off the
        # covered tile beats the step the flood asked for, so at a throat whose
        # only route is covered the body steps sideways every round and the
        # bounded counter buys one forward step per SK_DANGER_DETOUR_MAX --
        # measured as a 40-round stand on helheim_A with the lap tile adjacent.
        # The flood has now PRICED the danger; re-ranking its answer here would
        # charge for it twice and re-create exactly that stall.  The 2-cycle
        # strike-out below stays: that is a stepping fact, not a danger fact.
        # ⭐ v606 ITEM 1 (SK_DISENGAGE) -- THE WAIVER IS SUSPENDED FOR A BODY
        # ONE HIT FROM DEAD.  The cost form's argument for dropping the
        # step-level veto is that the flood already PRICED the danger -- true
        # for a full-HP body choosing a route, false for a 4-HP walker choosing
        # whether to stand in the ray for one more round.  49 of the 51 builder
        # deaths on the v605 tape are forward bodies on the enemy lap, none from
        # full HP, modal entry to the killing round exactly 4 HP.  ⛔ `forced`
        # goes FALSE too, or the detour budget hands the hurt body back to the
        # ray it just stepped out of; the `safe + risky` fallback below is what
        # stops that becoming the 40-round stand the veto was removed for.
        hurt = False
        if SK_DISENGAGE and self.role in (SK_CAGE_WALKER, SK_SIEGE_ENGINEER):
            try:
                hurt = ct.get_hp() <= SK_DISENGAGE_HP
            except Exception:
                hurt = False
        if SK_DANGER_COST and not hurt:
            danger = frozenset()
            forced = True
        else:
            danger = self._danger_tiles()
            forced = (not hurt) and self.danger_detour >= SK_DANGER_DETOUR_MAX
        # ⭐ v609 GATE E, second half -- HOLD RATHER THAN SIDESTEP WHEN THE
        # THROAT IS PLUGGED BY A BODY.  Sidestepping around a 1-round obstacle
        # costs the tile AND locks the phase: measured on bifrost seat A
        # r128-157, the enemy body shuttled (0,5)<->(0,6) in exact antiphase
        # with our sidestep for 30 rounds at zero progress, one tile from the
        # only peck seat.  Standing still breaks the phase and takes the tile
        # the round it opens.  Scoped: `nav_soft_bodies` is only ever set around
        # the counter-march's own step_to.
        if SK_COUNTER_SOFT_BODIES and self.nav_soft_bodies and desired in CARDINALS:
            _q = p.add(desired)
            if self.ibp(_q):
                try:
                    if ct.get_tile_builder_bot_id(_q) is not None:
                        self.nav_held = True
                        return False
                except Exception:
                    pass
        safe = []
        risky = []
        for d in cands:
            ndx, ndy = DELTA[d]
            qx, qy = p.x + ndx, p.y + ndy
            if not self.ib(qx, qy):
                continue
            if back is not None and qx == back[0] and qy == back[1]:
                continue                      # FIX 3: never the return leg
            # ⭐ v625 L2: while the post-hold taboo is armed, the tile the last
            # 2-cycle shuttled to stays struck (CAGE walker, not hurt) -- see
            # SK_CAGE_CYCLE_TABOO in sk_maps.
            if (SK_CAGE_CYCLE_TABOO and self.role == SK_CAGE_WALKER
                    and not hurt and self.cycle_taboo_tile is not None
                    and (qx, qy) == self.cycle_taboo_tile):
                try:
                    if ct.get_current_round() <= self.cycle_taboo_until:
                        continue
                    self.cycle_taboo_tile = None
                except Exception:
                    pass
            if forced or (qx, qy) not in danger:
                safe.append(d)
            else:
                risky.append(d)
        for d in safe + risky:
            if self._move(ct, d):
                # ⛔ `forced` RESETS TOO, or a body whose forced step turned out
                # to be illegal would keep incrementing past the cap and the
                # danger term would be permanently off for the rest of its life.
                if forced or d == cands[0]:
                    self.danger_detour = 0
                else:
                    self.danger_detour += 1
                return True
        if back is not None:
            self.cycle_blocked += 1
            # ⭐ v625 L2 (SK_CAGE_CYCLE_TABOO): the hold breaks the alternation,
            # which switches FIX 3 off next round -- and the cycle restarts.
            # Remember the struck tile for a few rounds so it cannot.
            if (SK_CAGE_CYCLE_TABOO and self.role == SK_CAGE_WALKER
                    and not hurt):
                self.cycle_taboo_tile = (back[0], back[1])
                try:
                    self.cycle_taboo_until = (ct.get_current_round()
                                              + SK_CYCLE_TABOO_ROUNDS)
                except Exception:
                    self.cycle_taboo_until = -1
            return False                      # hold, do not feed the ray
        self.stuck += 1
        return False

    def _move(self, ct, d):
        """Pave-free.  Builder bots move CARDINALS only; a diagonal move()
        raises GameError and can_move(diagonal) is False.
        """
        if d == Direction.CENTRE or d not in CARDINALS:
            return False
        p0 = ct.get_position()
        ndx, ndy = DELTA[d]
        if not self.ib(p0.x + ndx, p0.y + ndy):   # explicit bounds, item 2
            return False
        if ct.can_move(d):
            ct.move(d)
            return True
        return False

    def free_neighbours(self, ct, p, exclude=None):
        """How many cardinal neighbours this body could step onto.

        ⛔ THE SELF-TRAP GUARD, and it is measured, not theoretical: in a local
        game the home keeper built its own conveyor onto the one open tile
        beside it and stood frozen at (7,9) from r19 to the end of the match --
        harvester east, its own belt west, wall north and south.  A builder
        cannot stand on its own building, which is the same engine fact that
        produces ledger V2's self-inflicted seal holes.  Every build site is
        checked with `exclude=` set to the tile about to be built.

        ⭐ v605 FIX 3 WIDENED `exclude` TO A SEQUENCE, and the reason is a
        measured defect this guard was one tile short of catching.  `_prep_barrier`
        reserved an exit against THE BARRIER IT WAS PLACING AND NOTHING ELSE --
        but the nest SITE is an orthogonal neighbour by construction, it is still
        empty while the barriers go down, so it counted AS the reserved exit, and
        the sentinel filled it the round after.  Measured on the v604 30-game
        tape: in 9 of 30 games the siege engineer had ZERO passable neighbours
        from the round after its first plant until the end of its life (68-271
        rounds each, 1,059 idle rounds), and ALL NINE never got a second
        sentinel -- 9 of the 13 games that never got one at all.  A guard that
        prices one of the two buildings it is about to be surrounded by is not a
        guard.
        """
        ex = ()
        if exclude is not None:
            ex = ((exclude.x, exclude.y),) if hasattr(exclude, "x") else \
                 tuple((e.x, e.y) for e in exclude if e is not None)
        n = 0
        for d in CARDINALS:
            q = p.add(d)
            if not self.ibp(q):
                continue
            if (q.x, q.y) in ex:
                continue
            try:
                if ct.is_tile_passable(q):
                    n += 1
            except Exception:
                continue
        return n

    # --- v605 FIX 1: THE PATH ARBITER (SK_PATH_ARBITER) --------------------

    def _route_grid(self, ct, rnd):
        """(w2, blocked bytearray) for the reachability test, cached one round.

        The nav template (padded border + known walls + BOTH core footprints)
        with every IMPASSABLE building this body can currently see stamped on.
        ⛔ CONVEYOR AND SPLITTER ARE DELIBERATELY ABSENT: `_bfs_direction`'s
        engine measurement stands -- a builder bot walks onto a friendly
        conveyor tile -- so a belt piece is not a route blocker and stamping it
        here would invent blockades the engine does not have.
        ⚠ WHAT IS NOT IN IT: buildings outside this body's vision, and walls on
        an unconfirmed map that nobody has sensed.  Both read PASSABLE, so the
        test FAILS OPEN.  That is the direction a veto must fail in.
        """
        if self._route_key == rnd and self._route_blocked is not None:
            return self._route_w2, self._route_blocked
        # v607 ITEM 3: no walking target here -- see `_memo_nav_on`'s disclosure.
        w2, tpl = self._nav_template(self._memo_nav_on(None))
        base = bytearray(tpl)
        mw, mh = self.mw, self.mh
        try:
            for bid in ct.get_nearby_buildings():
                if ct.get_entity_type(bid) not in BFS_BLOCKING_TYPES:
                    continue
                bp = ct.get_position(bid)
                if 0 <= bp.x < mw and 0 <= bp.y < mh:
                    base[(bp.y + 1) * w2 + bp.x + 1] = 1
        except Exception:
            pass
        self._route_key = rnd
        self._route_w2 = w2
        self._route_blocked = base
        return w2, base

    def _ring_runs(self, ct, p, rnd):
        """Circular runs of passable tiles in p's 8-neighbourhood.

        ⭐ THE PRE-FILTER, and it is what makes the arbiter affordable.  Under
        4-connected movement a tile can only be a CUT VERTEX if its ring of
        passable neighbours falls into two or more circular runs -- consecutive
        RING8 entries are cardinally adjacent to each other, so a run IS a
        locally connected group.  Fewer than two runs ⇒ blocking p provably
        disconnects nothing, no flood needed.  The converse does not hold (two
        runs may still be joined the long way round), so this NOMINATES rather
        than decides: it is conservative in the only safe direction.
        """
        w2, g = self._route_grid(ct, rnd)
        idx = (p.y + 1) * w2 + p.x + 1
        free = [g[idx + dy * w2 + dx] == 0 for dx, dy in RING8]
        runs = 0
        for i in range(8):
            if free[i] and not free[i - 1]:
                runs += 1
        return runs

    def _route_reachable(self, ct, rnd, block):
        """Can our core still reach the enemy core with `block` built?

        Plain unweighted flood over `_route_grid`, seeded on the passable tiles
        of OUR core ring, goal = any passable tile of the ENEMY core ring.  No
        danger term: this asks whether a route EXISTS, not which one to walk.
        Budget exhaustion returns True (fail open).
        """
        w2, base = self._route_grid(ct, rnd)
        st = bytearray(base)
        if block is not None:
            st[(block.y + 1) * w2 + block.x + 1] = 1
        goals = 0
        for q in core_ring(self.enemy):
            if not self.ibp(q):
                continue
            gi = (q.y + 1) * w2 + q.x + 1
            if st[gi] == 0:
                st[gi] = 2
                goals += 1
        if goals == 0:
            return True             # the ring is already shut: nothing to lose
        cur = []
        for q in core_ring(self.core):
            if not self.ibp(q):
                continue
            si = (q.y + 1) * w2 + q.x + 1
            v = st[si]
            if v == 2:
                return True
            if v == 0:
                st[si] = 1
                cur.append(si)
        nodes = len(cur)
        flat = (-w2, 1, w2, -1)
        while cur:
            nxt = []
            for node in cur:
                for fl in flat:
                    n = node + fl
                    v = st[n]
                    if v == 2:
                        return True
                    if v == 0:
                        st[n] = 1
                        nxt.append(n)
            nodes += len(nxt)
            if nodes > SK_PATH_ARBITER_BUDGET:
                return True         # runaway guard: fail open
            cur = nxt
        return False

    def path_arbiter_ok(self, ct, site, rnd):
        """THE ARBITER, EXTENDED FROM BODIES TO ROUTES (v605 FIX 1).

        False iff putting an IMPASSABLE building on `site` would remove the LAST
        route from our core to the enemy core.  `free_neighbours` refuses a
        build that leaves a BODY with no step; this refuses one that leaves the
        TEAM with no lane -- the helheim throat, where our own nest (two prep
        barriers plus the band sentinel) sealed the map's only corridor and the
        cage walker reached 1 of 12 lap tiles in v603 AND v604.

        ⛔ THE SECOND FLOOD IS NOT OPTIONAL.  Refusing on "unreachable after"
        alone would freeze every forward build the moment the route is lost for
        any other reason (an enemy seal, a body we cannot see) -- the veto has to
        be about THIS BUILD, so a tile is refused only when the route existed
        before it and not after.  That second flood runs only in the refusal
        candidate case, which the pre-filter already makes rare.
        """
        if not SK_PATH_ARBITER:
            return True
        if self.core is None or self.enemy is None or not self.ibp(site):
            return True
        key = (site.x, site.y)
        seen = self.path_veto.get(key)
        if seen is not None:
            if rnd - seen < SK_PATH_ARBITER_MEMO:
                return False        # CPU memo, not a refutation -- it expires
            del self.path_veto[key]
        if self._ring_runs(ct, site, rnd) < 2:
            return True             # cannot be a cut vertex
        if self._cpu_exhausted(ct):
            return True             # fail open, same as the nav probe
        if self._route_reachable(ct, rnd, site):
            return True
        if not self._route_reachable(ct, rnd, None):
            return True             # already lost; not this build's doing
        self.path_veto[key] = rnd
        self.path_vetoes += 1
        return False

    def step_to(self, ct, target):
        """Set the target tile and take one step.  The ONLY movement entry.

        v602: returns True iff a move was actually executed (FIX 1 reads it).
        """
        self.tgt = target
        return self._nav(ct)

    # --- shared sensing ----------------------------------------------------

    def _boot(self, ct, p):
        """First-turn identity + map bootstrap, shared by every unit kind."""
        if self.team is None:
            self.team = ct.get_team()
            self.mw, self.mh = ct.get_map_width(), ct.get_map_height()
            self.idx = ct.get_id() & 0xFF
            self.role_parity = self.idx & 1     # replaced by the role on claim

    def _load_grid(self, ct):
        """Adopt the catalogued grid ONLY if visible terrain confirms it.

        `known_map_for` runs F1 (`_maptrust_pick`); on a mismatch or an
        unsurveyed board it returns None and every consumer falls back to live
        sensing -- map_grid stays None and `_bfs_direction` degrades to
        `cardinal_direction_to`.  Callers gate on `map_grid is None`, so this
        costs one bounded scan per unit, not per round.
        """
        from sk_maps import known_map_for
        if self.map_grid is not None or self.core is None:
            return
        grid = known_map_for(self.mw, self.mh, self.core, ct)
        if grid is None:
            return
        walls = set()
        ores = []
        for y, row in enumerate(grid):
            i = row.find("#")
            while i >= 0:
                walls.add((i, y))
                i = row.find("#", i + 1)
            i = row.find("o")
            while i >= 0:
                ores.append(Position(i, y))
                i = row.find("o", i + 1)
        self.map_grid = grid
        self.map_walls = walls
        self.map_ores = ores

    # --- v601 BUGFIX: live-sensed ore (SK_ORE_SENSE) -----------------------

    def _ore_scan(self, ct, p):
        """The ore fallback `_load_grid` promised and did not have.

        ⛔ THE DEFECT THIS FIXES, reproduced before it was written (s54,
        `maps/stavkirke.map26` seed 11, trace on a scratchpad copy):

            TRACE r1  keeper at (9,1) grid=False ores=0 harv=0 plan=0
            TRACE r20 keeper at (8,3) grid=False ores=0 harv=0 plan=0
            ... to the end of the match ...

        `known_map_for` returns None on any map whose terrain the catalogue
        cannot confirm -- **10 of the 15 maps in the current pool**, measured by
        re-encoding each `maps/*.map26` and comparing against MAP_CODES +
        EXTRA_MAP_CODES.  `_load_grid` then leaves `map_ores` EMPTY, and
        `_home_keeper_move`'s ore loop is the ONLY code in the tree that ever
        walks a keeper toward ore.  With no ore in the list the keeper targets
        its own core, stands on the doorstep and never builds a harvester: 7 of
        15 tape games finished with ZERO harvesters built.

        THE SCAN IS BOUNDED BY MAP AREA, NOT BY ROUNDS.  `ore_scanned` records
        every tile already classified, so a tile costs exactly one
        `get_tile_env` over this unit's whole life; a fresh vision disc is ~61
        tiles on the first turn and a handful per step after that.  A tile whose
        read RAISES is un-recorded so a later turn retries it.
        """
        if not SK_ORE_SENSE or self.map_ores:
            return
        try:
            tiles = ct.get_nearby_tiles()
        except Exception:
            return
        for q in tiles:
            xy = (q.x, q.y)
            if xy in self.ore_scanned:
                continue
            # ⛔ EXPLICIT BOUNDS TEST before any get_tile_*: get_nearby_tiles is
            # documented in-bounds, and `is_in_vision` was documented as a
            # bounds guard too (s50) and is not.
            if not self.ibp(q):
                continue
            try:
                env = ct.get_tile_env(q)
            except Exception:
                continue
            self.ore_scanned.add(xy)
            if env == Environment.ORE_TITANIUM:
                self.sensed_ores.append(q)
                self.sensed_ore_xy.add(xy)
            elif env == Environment.WALL:
                # ⛔ WALLS GO INTO `map_walls`, THE SAME SET `_load_grid` fills.
                # Two consumers depend on it and both were silently degraded on
                # an unconfirmed map: `_nav_template` (whose flood then paths
                # through walls) and the belt planner below.
                self.map_walls.add(xy)

    def wall_at(self, x, y):
        """Terrain wall test that works with OR without a confirmed grid.

        `map_walls` is filled from the grid by `_load_grid` when the catalogue
        confirms the map, and from `_ore_scan` otherwise.
        """
        return (x, y) in self.map_walls

    def ore_at(self, x, y):
        if self.map_grid is not None:
            return self.map_grid[y][x] == "o"
        return (x, y) in self.sensed_ore_xy

    def terrain_known(self):
        """Enough terrain to plan a belt on.  A confirmed grid is complete; a
        sensed board is optimistic (UNSEEN reads as passable), which is why
        `_belt_watch` bans a planned tile the moment vision shows it to be a
        wall -- the plan is a hypothesis until walked."""
        return self.map_grid is not None or len(self.ore_scanned) >= 8

    def ore_list(self):
        """Ore tiles to work from: the confirmed catalogue grid, else what this
        unit has actually SEEN.  Never both -- a confirmed grid is complete and
        the sensed list is a strict subset of it."""
        if self.map_ores:
            return self.map_ores
        return self.sensed_ores

    def explore_step(self, ct, p, rnd):
        """Where to walk when there is no ore in the list yet and no grid.

        Sensing alone only helps if the keeper is ever somewhere new; on
        stavkirke it oscillated between two tiles beside its own core for the
        whole match.  This is a coarse home-half sweep -- eight compass bearings
        at three radii from the core -- advanced when reached or after 40 rounds
        so a blocked bearing cannot own the keeper.  ⛔ IT STAYS IN THE HOME
        HALF: `_home_keeper_move`'s "forward-action share 0.000" property is a
        measured feature of this role and must survive the fix.
        """
        if self.core is None:
            return None
        if rnd >= self.explore_until:
            self.explore_i += 1
            self.explore_until = rnd + 40
        probes = []
        for r in (4, 7, 10):
            for dx, dy in ((0, -1), (1, -1), (1, 0), (1, 1),
                           (0, 1), (-1, 1), (-1, 0), (-1, -1)):
                q = Position(self.core.x + dx * r, self.core.y + dy * r)
                if not self.ibp(q):
                    continue
                if not self.is_home_half(q):
                    continue
                if (q.x, q.y) in self.map_walls:
                    continue
                probes.append(q)
        if not probes:
            return None
        q = probes[self.explore_i % len(probes)]
        if p.distance_squared(q) <= 2:
            self.explore_until = rnd          # reached: advance next turn
        return q

    def is_home_half(self, p):
        """Our half by distance to the two anchors -- the HOME KEEPER's fence
        and the ORE DENIER's hunting ground, from opposite sides."""
        if self.core is None or self.enemy is None:
            return True
        return dsq_core(p, self.core) <= dsq_core(p, self.enemy)

    def enemy_ids_near(self, ct, dsq=None):
        """(id, type, position) for every visible enemy entity.  One pass."""
        out = []
        try:
            ids = ct.get_nearby_entities() if dsq is None else ct.get_nearby_entities(dsq)
        except Exception:
            return out
        for eid in ids:
            try:
                if ct.get_team(eid) == self.team:
                    continue
                out.append((eid, ct.get_entity_type(eid), ct.get_position(eid)))
            except Exception:
                continue
        return out

    def tile_owner(self, p):
        """THE ARBITER (V2/V8): one map tile -> one owning verb.

        Consulted before every build and every destroy.  Geometric, so it
        cannot go stale and costs no store slot.
        """
        # ⛔ ORDER MATTERS AND IT IS NOT ARBITRARY: the belt's TERMINAL tile is
        # orthogonally adjacent to our own core, i.e. it is also a door tile.
        # The belt claims first, or a terminated belt can never be built --
        # and an unterminated belt delivers nothing, which is the whole point
        # of the plank (`titanium_collected` counts delivery, not emission).
        if (p.x, p.y) in self.belt_plan:
            return OWNER_BELT
        if self.enemy is not None and adjacent_to_core(p, self.enemy):
            return OWNER_CAGE
        if self.core is not None and adjacent_to_core(p, self.core):
            return OWNER_DOOR
        if self.nest_site is not None and p.distance_squared(self.nest_site) <= 2:
            return OWNER_NEST
        if not self.is_home_half(p) and self.map_grid is not None:
            if self.ibp(p) and self.map_grid[p.y][p.x] == "o":
                return OWNER_DENY
        return OWNER_NONE

    def may_build(self, p, verb):
        """True if `verb` owns tile p (or nobody does)."""
        o = self.tile_owner(p)
        return o == OWNER_NONE or o == verb

    # --- V7: the target give-up rule ---------------------------------------

    def hp_trend_ok(self, ct, tid, rnd):
        """False once a target has failed to trend down for SK_HP_TREND_WINDOW
        rounds (ledger V7: 38 rounds and 152 Ti of ammunition were spent on a
        target being healed +8/round against 7 damage).  Per-unit memory.
        """
        from sk_maps import SK_HP_TREND_WINDOW
        try:
            hp = ct.get_hp(tid)
        except Exception:
            return False
        prev = self.hp_memo.get(tid)
        if prev is None or hp < prev[0]:
            self.hp_memo[tid] = (hp, rnd)
            return True
        if rnd - prev[1] >= SK_HP_TREND_WINDOW:
            self.give_up[tid] = rnd
            return False
        return True

    def gave_up(self, tid, rnd):
        r = self.give_up.get(tid)
        return r is not None and rnd - r < 40
