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

from fcode import Direction, EntityType, Position

from sk_maps import (
    BFS_BLOCKING_TYPES, CARDINALS, CARD_DELTAS, CARD_OPPOSITE, CPU_BUDGET_US,
    DELTA, NAV_NODE_BUDGET, SK_BEAT_MASK, SK_STORE_MASK, SK_TELEPORT_DSQ,
)


# ===========================================================================
# BOUNDS -- the helper the benchmark never had (manifest item 2)
# ===========================================================================

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

    def _clear_plans(self):
        """Every per-role plan cache, in one place (the guard's clear list)."""
        self.belt_cursor = None       # HOME KEEPER: next belt tile being laid
        self.lap_i = None             # CAGE WALKER: lap cursor
        self.melee_tile = None        # CAGE WALKER: ring tile being chewed
        self.melee_since = -1
        self.deny_tile = None         # ORE DENIER: ore tile being denied
        self.nest_site = None         # SIEGE ENGINEER: chosen gun tile
        self.nest_prepped = 0

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

    def _nav_template(self):
        """(w2, template) for `_bfs_direction`: border + walls + both Cores.

        The blocked 1-tile border IS the bounds test, so the inner flood runs
        no comparison at all (manifest §6.5: lift `_bfs_direction` without this
        and the bounds test silently disappears from the hot loop).
        """
        key = (self.core, self.enemy, self.mw, self.mh)
        if self._nav_key != key:
            blocked = set(self.map_walls)
            if self.core is not None:
                blocked.update(core_tiles_xy(self.core))
            if self.enemy is not None:
                blocked.update(core_tiles_xy(self.enemy))
            self._nav_tpl = bytes(self._flat_template(blocked))
            self._nav_key = key
        return self.mw + 2, self._nav_tpl

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
        if self.map_grid is None:
            return p.cardinal_direction_to(target)
        mw, mh = self.mw, self.mh
        tx, ty = target.x, target.y
        if not (0 <= tx < mw and 0 <= ty < mh):
            return p.cardinal_direction_to(target)

        w2, tpl = self._nav_template()
        base = bytearray(tpl)
        bodies = []
        try:
            me = ct.get_id()
            for eid in ct.get_nearby_entities():
                if eid == me:
                    continue
                et = ct.get_entity_type(eid)
                ep = ct.get_position(eid)
                if et == EntityType.CORE:
                    for cx, cy in core_tiles_xy(ep):
                        if 0 <= cx < mw and 0 <= cy < mh:
                            base[(cy + 1) * w2 + cx + 1] = 1
                elif et == EntityType.BUILDER_BOT:
                    ex, ey = ep.x, ep.y
                    if 0 <= ex < mw and 0 <= ey < mh:
                        bodies.append((ey + 1) * w2 + ex + 1)   # both teams
                elif et in BFS_BLOCKING_TYPES:
                    ex, ey = ep.x, ep.y
                    if 0 <= ex < mw and 0 <= ey < mh:
                        base[(ey + 1) * w2 + ex + 1] = 1
        except Exception:
            pass

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
        for _pass in (0, 1):
            if _pass == 1 and not bodies:
                break
            st = bytearray(base)
            if _pass == 0:
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
        if self.tgt is None or ct.get_move_cooldown() != 0:
            return
        desired = self._bfs_direction(ct, self.tgt)
        if desired == Direction.CENTRE:
            return
        if self._move(ct, desired):
            return
        idx = CARDINALS.index(desired) if desired in CARDINALS else 0
        for d in (CARDINALS[(idx + 1) % 4], CARDINALS[(idx + 3) % 4], desired.opposite()):
            if self._move(ct, d):
                return
        self.stuck += 1

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
        """
        n = 0
        for d in CARDINALS:
            q = p.add(d)
            if not self.ibp(q):
                continue
            if exclude is not None and q.x == exclude.x and q.y == exclude.y:
                continue
            try:
                if ct.is_tile_passable(q):
                    n += 1
            except Exception:
                continue
        return n

    def step_to(self, ct, target):
        """Set the target tile and take one step.  The ONLY movement entry."""
        self.tgt = target
        self._nav(ct)

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
