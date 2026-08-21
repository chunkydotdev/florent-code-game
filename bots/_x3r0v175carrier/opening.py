"""WAVE 22, ARM A1 -- THE INTEGRATED OPENING.  Master flag `OPEN_ON`.

Implements `analysis/wave22/OPENING.md` on top of `bots/loki_leap16`:

  * the band variable is `need_eff`, computed ONCE at r0 from a BFS walk
    distance between the two Core rings -- never from a map name, so it is
    rotation-safe (OPENING.md 1.1, 9);
  * SOCKET-PREFILL: exactly TWO of our own sockets, on TWO different core
    FACES, carrying our own CONVEYORS, by r3.  Never a barrier (blocks our own
    delivery), never a harvester or turret (impassable -> kills the heal seat)
    (OPENING.md 4.3 rules 1-2);
  * the two economy builders SPAWN ON THE DIAGONAL CORNERS, each of which is
    orthogonally adjacent to two sockets on two different faces, so the socket
    is bought with an action and zero moves (OPENING.md 3.1 correction 2);
  * the feeder is built CORE-OUTWARD -- socket, then trunk, then harvester
    last -- so no stack is ever buffered and the socket is occupied at r2
    instead of r8 (OPENING.md 3.1 correction 1);
  * the ORE GATE: `L` (walk distance socket -> nearest ore) decides whether a
    socket is a feeder or a PLUG whose trunk is laid behind it (OPENING.md 2.4);
  * a 3-builder cap while the ferry is live (4 in band A) that lifts at arrival
    and only when the bank clears the counter-battery reserve (OPENING.md 2.2);
  * a rung budget of exactly `need_eff` UNCONDITIONAL rungs at the flat
    `floor(20*scale)` disposable price (OPENING.md 2.3, E4);
  * band A's payload switch: an own-ring sentinel PAIR in A-1, the same ladder
    carrying a TURRET payload in A-2 (`A2_TURRET`).  `A2_ECO` is NOT in this
    build -- it is a separately-flagged variant (PLAN 2.1, OPENING.md 1.4).

CARRIER HYGIENE (PLAN 1.5).  Every occupancy test here uses
`get_tile_building_id` / `get_tile_builder_bot_id` and never `is_tile_empty`
(P0-B).  The plank adds NO comm slot: all 16 are assigned in the base, so the
socket assignment, the trunk, the cap and the sentinel pair are all derived
from GEOMETRY that every unit computes identically, and the pair is bounded by
a per-unit latch plus the rider seat number rather than by a shared counter
(the store is buffered -- fixtures.md 2 measured three pair sentinels when a
count was trusted).  Sandbox: no bare `except`, no `try`/`finally`, every
handler is `except Exception:`.
"""
import math

from fcode import Direction, EntityType, GameConstants, Position

from doctrine import *  # noqa: F401,F403
from eco import (
    SG_SOCKET_FACE, _decode_grid, core_corners, dsq_core, enemy_core_for,
    heal_seats, known_map_for, nearest_core_tile, sg_socket,
)

# The four cardinal steps, in the fixed order N, E, S, W.  Deterministic, so
# every unit that walks the same flood produces the same trunk.
_CARD4 = ((0, -1), (1, 0), (0, 1), (-1, 0))

# Which of `core_corners`' four diagonals each of the eight sockets touches.
# `core_corners` order is NW, NE, SW, SE; `SG_SOCKET_DELTAS` order is the wire
# format of the Core's rebuild request and may never be permuted, so this is a
# table rather than a computation.
_SOCKET_CORNER = (0, 1, 1, 3, 3, 2, 2, 0)

# Resolved openings, keyed by (mw, mh, core.x, core.y).  Module scope, exactly
# like `eco._GRID_CACHE`: up to eleven of our units ask the same question about
# the same match and the two floods below are the most expensive thing this
# plank does.
_OPEN_CACHE = {}

_BIG = 10 ** 6

# WAVE 69, ARM 2 build A -- MVETO_ROY.  royale's FULL decoded grid, resolved
# once at import next to `_OPEN_CACHE` for the same reason that cache exists:
# up to eleven of our units ask the same question about the same match.  It is
# a tuple of row strings, exactly what `eco.known_map_for` hands back and what
# `Player.map_grid` holds, so the comparison in `_op_geom` is a tuple equality
# over the WHOLE terrain -- never the (w, h, anchor) key, which collides.
_MVETO_ROY_GRID = _decode_grid(MVETO_ROY_CODE, MVETO_ROY_W, MVETO_ROY_H)


def _op_flood(sources, blocked, w, h):
    """Multi-source cardinal BFS.  Returns {(x, y): steps}.

    `sources` are at distance 0 even when they are themselves blocked (the
    ore flood starts on ore tiles, the ring flood on ring tiles), because the
    question is always "how far to walk to here", not "may I stand here".
    """
    dist = {}
    frontier = []
    for s in sources:
        if s in dist:
            continue
        if not (0 <= s[0] < w and 0 <= s[1] < h):
            continue
        dist[s] = 0
        frontier.append(s)
    d = 0
    while frontier:
        nxt = []
        d += 1
        for x, y in frontier:
            for dx, dy in _CARD4:
                t = (x + dx, y + dy)
                if t in dist:
                    continue
                if not (0 <= t[0] < w and 0 <= t[1] < h):
                    continue
                if t in blocked:
                    continue
                dist[t] = d
                nxt.append(t)
        frontier = nxt
    return dist


def _op_walk_down(start, dist, blocked, w, h):
    """Steepest-descent path from `start` down `dist` to a 0-cell.

    Returns the tile list INCLUDING `start` and the 0-cell, or None.  The
    tie-break is the fixed `_CARD4` order, so the path is identical for every
    unit that computes it.
    """
    here = start
    d = dist.get(here)
    if d is None:
        return None
    out = [here]
    guard = 0
    while d > 0 and guard < 4 * (w + h):
        guard += 1
        nxt = None
        for dx, dy in _CARD4:
            t = (here[0] + dx, here[1] + dy)
            if dist.get(t) == d - 1:
                nxt = t
                break
        if nxt is None:
            return None
        out.append(nxt)
        here = nxt
        d -= 1
    if d != 0:
        return None
    return out


def _op_solve(grid, w, h, core):
    """The whole opening, from geometry.  Pure; no controller, no map name."""
    enemy = enemy_core_for(w, h, core)
    blocked = set()
    ores = []
    if grid is not None:
        y = 0
        for row in grid:
            i = row.find("#")
            while i >= 0:
                blocked.add((i, y))
                i = row.find("#", i + 1)
            i = row.find("o")
            while i >= 0:
                ores.append((i, y))
                i = row.find("o", i + 1)
            y += 1
    # Both Core footprints reject every build and every step (engine G).
    for anchor in (core, enemy):
        for dx in (0, 1):
            for dy in (0, 1):
                blocked.add((anchor.x + dx, anchor.y + dy))

    our_ring = [(s.x, s.y) for s in heal_seats(core, w, h)]
    our_ring += [(c.x, c.y) for c in core_corners(core, w, h)]
    foe_ring = [(s.x, s.y) for s in heal_seats(enemy, w, h)]
    foe_ring += [(c.x, c.y) for c in core_corners(enemy, w, h)]

    # --- pathlen, and the rider's spawn tile, from ONE flood ---------------
    # Flooding from THEIR ring rather than ours gives both numbers: the walk
    # distance between the rings is the minimum over our own twelve tiles, and
    # the ring tile that minimises it is the one the rider starts on.
    dist_foe = _op_flood(foe_ring, blocked, w, h)
    pathlen = None
    for t in our_ring:
        v = dist_foe.get(t)
        if v is not None and (pathlen is None or v < pathlen):
            pathlen = v
    if pathlen is None:
        # No walkable route known (unknown map / walled pool).  Fall back to
        # the straight-line Core distance, which is what the closed forms in
        # the corpus were derived from anyway.
        pathlen = int(math.sqrt(dsq_core(Position(enemy.x, enemy.y), core)))
    num = pathlen * 100 - OPEN_ENV_NUM
    need = 1 if num <= 0 else (num + OPEN_HOP_NUM - 1) // OPEN_HOP_NUM
    if need < 1:
        need = 1
    if need == 1:
        band = "A1"
    elif need == 2:
        band = "A2"
    elif need < OPEN_BAND_C_NEED:
        band = "B"
    else:
        band = "C"

    # --- the ore flood: L per socket, and the trunk behind it -------------
    dist_ore = _op_flood(ores, blocked, w, h) if ores else {}

    socks = []
    for i in range(8):
        s = sg_socket(core, i)
        if not (0 <= s.x < w and 0 <= s.y < h):
            continue
        if (s.x, s.y) in blocked:
            continue
        socks.append((dist_ore.get((s.x, s.y), _BIG), i))
    socks.sort()

    s1 = s2 = None
    if socks:
        s1 = socks[0]
        f1 = SG_SOCKET_FACE[s1[1]]
        c1 = _SOCKET_CORNER[s1[1]]
        # Rule 1: a DIFFERENT core face -- the two sockets of one face are
        # orthogonally adjacent, so one enemy body bricks both without moving.
        # Preferred with a different DIAGONAL too, so the two economy builders
        # spawn on two tiles and neither has to move to reach its socket.
        for cand in socks[1:]:
            if SG_SOCKET_FACE[cand[1]] != f1 and _SOCKET_CORNER[cand[1]] != c1:
                s2 = cand
                break
        if s2 is None:
            for cand in socks[1:]:
                if SG_SOCKET_FACE[cand[1]] != f1:
                    s2 = cand
                    break

    corners = core_corners(core, w, h)
    ckeys = [(c.x, c.y) for c in corners]

    def _pack(entry, feed_max):
        if entry is None:
            return None
        L, i = entry
        s = sg_socket(core, i)
        ci = _SOCKET_CORNER[i]
        diag = None
        if 0 <= ci < 4:
            c = Position(core.x + ((-1, 2, -1, 2)[ci]), core.y + ((-1, -1, 2, 2)[ci]))
            if (c.x, c.y) in ckeys and (c.x, c.y) not in blocked:
                diag = c
        if diag is None:
            # The diagonal is a wall or off the map.  Fall back to the tile one
            # step further OUT from the socket -- which is the first trunk tile
            # anyway, so the body is standing where it needs to stand next.
            ctile = nearest_core_tile(s, core)
            o = Position(2 * s.x - ctile.x, 2 * s.y - ctile.y)
            if 0 <= o.x < w and 0 <= o.y < h and (o.x, o.y) not in blocked:
                diag = o
        trunk = None
        if L < _BIG and L <= feed_max:
            walk = _op_walk_down((s.x, s.y), dist_ore, blocked, w, h)
            if walk is not None and len(walk) >= 2:
                trunk = tuple(Position(t[0], t[1]) for t in walk)
        return {"sock": s, "idx": i, "face": SG_SOCKET_FACE[i],
                "L": (None if L >= _BIG else L), "diag": diag, "trunk": trunk}

    e1 = _pack(s1, PREFILL_FEED_MAX_L1)
    e2 = _pack(s2, PREFILL_FEED_MAX_L)

    # --- spawn tiles -------------------------------------------------------
    taken = set()
    for e in (e1, e2):
        if e is not None:
            taken.add((e["sock"].x, e["sock"].y))
            if e["diag"] is not None:
                taken.add((e["diag"].x, e["diag"].y))
    riders = []
    for t in sorted(our_ring, key=lambda q: (dist_foe.get(q, _BIG), q[1], q[0])):
        if t in taken or t in blocked:
            continue
        riders.append(Position(t[0], t[1]))
        if len(riders) >= 2:
            break

    return {
        "need": need, "band": band, "path": pathlen, "enemy": enemy,
        "e1": e1, "e2": e2, "riders": tuple(riders),
        # ARRIVAL, and therefore the round the builder cap lifts.  PLAN 2.1
        # fixes the ferry budget at `arrival = 2*ceil(c2c/5.66) - 1` and NOT
        # the published `1 + 2*ceil(c2c/5.66)`, which is two rounds late on 12
        # of 15 maps (evidence_fixes.md 5.1); with `need_eff` counting rungs
        # off the ring-to-ring walk that is `2*need_eff + 1`.  The floor of 6
        # is band A, where there is no ferry to wait for but the cap must still
        # hold through the r5-r7 turret-pair window (OPENING.md 2.5 prices the
        # band-A lift at r6).
        "arrival": max(OPEN_LIFT_MIN, 2 * need + 1),
        "rungs": (0 if need <= 1 else need),
    }


class OpenMixin:
    """Arm A1.  Every method is a no-op when `OPEN_ON` is False."""

    # ------------------------------------------------------------------
    # geometry
    # ------------------------------------------------------------------

    def _op_geom(self, ct):
        """The resolved opening, or None while the Core anchor is unknown."""
        if not OPEN_ON:
            return None
        # WAVE 69, MVETO_ROY -- THE LATCH SHORT-CIRCUIT.  Once royale has been
        # resolved for this unit the opening is DOWN for the rest of the match,
        # and re-resolving costs a `known_map_for` scan of ~44 map entries on
        # EVERY call (the `self.op_geom` fast path below is never armed under a
        # veto, because a vetoed geometry is never cached).  Under `OPEN_ON`
        # False the parent pays nothing here; the veto must not either.
        if MVETO_ROY_ON and self.op_map_veto:
            return None
        g = self.op_geom
        if g is not None:
            return g
        if self.core is None or not (self.mw and self.mh):
            return None
        grid = self.map_grid
        if grid is None:
            grid = known_map_for(self.mw, self.mh, self.core, ct)
        # WAVE 69, ARM 2 build A -- MVETO_ROY, THE VETO ITSELF.  Placed here,
        # immediately after `grid` resolves and BEFORE the cache key, because
        # this is the one point in the file where map identity is known and
        # nothing has been committed to yet.
        #
        #   * `tuple(grid)` is mandatory, not cosmetic: the grid arrives either
        #     as `self.map_grid` or as `known_map_for`'s freshly decoded
        #     candidate, and a silent type mismatch is a veto that never fires
        #     -- which passes a byte-identity tripwire in perfect silence.
        #   * `grid is not None` is mandatory too: `known_map_for` returns None
        #     on an unknown map, and `tuple(None)` is a TypeError that escapes
        #     `run()` and makes the engine delete this unit for the match.
        #   * returning None is the EXACT value `_op_geom` returns when
        #     `OPEN_ON` is False, so `_op_band_a` (main.py), `_op_socket_keys`
        #     (main.py) and the three OPEN walks (eco.py) all take their
        #     audited None-paths and the parent book runs unaltered.
        if MVETO_ROY_ON and grid is not None and tuple(grid) == _MVETO_ROY_GRID:
            self.op_map_veto = True
            return None
        # THE GRID IS PART OF THE KEY, not just the dimensions and the anchor.
        # `doctrine.MAP_CODES` + `EXTRA_MAP_CODES` contain EIGHT colliding
        # (w, h, anchor) triples, and `known_map_for` disambiguates them by
        # what the asking unit can SEE -- so two of our units can legitimately
        # hold different grids for the same anchor, and a cache keyed on the
        # anchor alone would hand one of them the other one's map.
        key = (self.mw, self.mh, self.core.x, self.core.y, grid)
        g = _OPEN_CACHE.get(key)
        if g is None:
            g = _op_solve(grid, self.mw, self.mh, self.core)
            _OPEN_CACHE[key] = g
        self.op_geom = g
        if OPEN_LOG and not self.op_band_log:
            self.op_band_log = True
            e1, e2 = g["e1"], g["e2"]
            print("OP band=%s need=%d path=%d arr=%d rungs=%d L1=%s L2=%s"
                  % (g["band"], g["need"], g["path"], g["arrival"], g["rungs"],
                     "-" if e1 is None else e1["L"],
                     "-" if e2 is None else e2["L"]))
        return g

    def _op_band(self, ct):
        g = self._op_geom(ct)
        return None if g is None else g["band"]

    def _op_band_a(self, ct):
        b = self._op_band(ct)
        return b == "A1" or b == "A2"

    def _op_need(self, ct):
        g = self._op_geom(ct)
        return 0 if g is None else g["need"]

    def _op_rungs(self, ct):
        """The unconditional rung budget: exactly `need_eff` (0 in band A-1)."""
        g = self._op_geom(ct)
        return 0 if g is None else g["rungs"]

    def _op_line(self, ct):
        """This body's own prefill line, or None.  Seats 1 and 2 only."""
        g = self._op_geom(ct)
        if g is None:
            return None
        if self.role_n == 1:
            return g["e1"]
        if self.role_n == 2:
            return g["e2"]
        return None

    def _op_socket_keys(self, ct):
        """The two prefill socket tiles, as a frozenset of (x, y)."""
        if self.op_sock_keys is not None:
            return self.op_sock_keys
        g = self._op_geom(ct)
        if g is None:
            return frozenset()
        out = []
        for e in (g["e1"], g["e2"]):
            if e is not None:
                out.append((e["sock"].x, e["sock"].y))
        self.op_sock_keys = frozenset(out)
        return self.op_sock_keys

    # ------------------------------------------------------------------
    # occupancy -- P0-B: never `is_tile_empty`
    # ------------------------------------------------------------------

    def _op_ours_at(self, ct, t):
        """Is one of OUR buildings standing on `t`?  (None = cannot tell.)"""
        try:
            bid = ct.get_tile_building_id(t)
        except Exception:
            return None
        if bid is None:
            return False
        try:
            return ct.get_team(bid) == self.team
        except Exception:
            return None

    def _op_filled(self, ct, t):
        """Is `t` a FILLED socket -- our own conveyor/splitter standing on it?

        Rule 4: a body stations on a FILLED socket (already unspawnable, so it
        costs no spawn tile, and it heals).  Rule 3: a body on an EMPTY socket
        blocks our own feeder build and is the wave-20 M3 self-seal.
        """
        try:
            bid = ct.get_tile_building_id(t)
            if bid is None:
                return False
            if ct.get_team(bid) != self.team:
                return False
            return ct.get_entity_type(bid) in (EntityType.CONVEYOR,
                                               EntityType.SPLITTER)
        except Exception:
            return False

    def _op_empty_socket_keys(self, ct):
        """Prefill sockets that are still EMPTY, as (x, y).  The body ban."""
        if not OPEN_ON:
            return frozenset()
        keys = self._op_socket_keys(ct)
        if not keys:
            return keys
        out = []
        for k in keys:
            t = Position(k[0], k[1])
            if self._op_ours_at(ct, t) is not True:
                out.append(k)
        return frozenset(out)

    # ------------------------------------------------------------------
    # THE PREFILL -- 2 sockets, 2 faces, conveyors, by r3
    # ------------------------------------------------------------------

    def _op_prefill(self, ct, rnd):
        """Build this body's socket conveyor.  True = the action was spent."""
        if not OPEN_ON or self.op_prefill_done:
            return False
        line = self._op_line(ct)
        if line is None:
            self.op_prefill_done = True
            return False
        s = line["sock"]
        if self._op_ours_at(ct, s) is True:
            # A teammate got there, or this body already did.  Either way the
            # socket is ours and the occupancy half of the plank is bought.
            self.op_prefill_done = True
            return False
        if ct.get_action_cooldown() != 0:
            return False
        p = ct.get_position()
        if abs(p.x - s.x) + abs(p.y - s.y) != 1:
            return False
        # Deliver INTO the core: a socket is orthogonally adjacent to the 2x2
        # footprint, so the cardinal to its nearest core tile is exact.
        f = s.cardinal_direction_to(nearest_core_tile(s, self.core))
        if f == Direction.CENTRE:
            return False
        try:
            if ct.get_global_resources() < ct.get_conveyor_cost():
                return False
            if not ct.can_build_conveyor(s, f):
                return False
            ct.build_conveyor(s, f)
        except Exception:
            return False
        self.op_prefill_done = True
        self.op_stage = 1
        if OPEN_LOG:
            print("OP prefill (%d,%d) face=%d seat=%d r=%d L=%s"
                  % (s.x, s.y, line["face"], self.role_n, rnd, line["L"]))
        return True

    def _op_prefill_walk(self, ct, rnd):
        """Walk to the diagonal that owns this body's socket.  True = moved.

        Only ever needed when the Core could not spawn the body on its
        diagonal (`can_spawn` refused); on a healthy game this costs one
        distance test and never fires.
        """
        if not OPEN_ON or self.op_prefill_done:
            return False
        if rnd > OPEN_PREFILL_WALK_RND:
            return False
        line = self._op_line(ct)
        if line is None:
            return False
        s = line["sock"]
        if self._op_ours_at(ct, s) is True:
            self.op_prefill_done = True
            return False
        p = ct.get_position()
        if abs(p.x - s.x) + abs(p.y - s.y) == 1:
            return False                     # already in place; build instead
        stand = line["diag"]
        if stand is None:
            # No legal tile beside the socket at all (walled in).  Do NOT walk
            # onto the socket itself -- a body on an EMPTY socket is rule 3's
            # ban and would block the very build it came for.  Fall through to
            # the ordinary economy; `_sg_rebuild` owns the socket from here.
            return False
        if ct.get_move_cooldown() != 0:
            return False
        self.tgt = stand
        self._nav(ct, pave=False)
        return True

    # ------------------------------------------------------------------
    # THE FEEDER -- core-outward, harvester LAST
    # ------------------------------------------------------------------

    def _op_trunk(self, ct, rnd):
        """Lay this body's trunk from the socket OUTWARD.  True = action spent.

        `trunk` is `(socket, t1, ... , ore)`.  The socket is built by
        `_op_prefill`; this lays `t1..t(L-1)` facing back toward the tile
        behind them, and the HARVESTER last, on the ore tile.  Nothing is ever
        buffered because the line is complete before the harvester exists
        (OPENING.md 3.1 correction 1).

        The ORE GATE lives in `_op_solve`: a line longer than its band's
        `PREFILL_FEED_MAX_L*` gets no `trunk` at all, so its socket stays a
        3-Ti PLUG and the ordinary economy lays the trunk behind it.
        """
        if not (OPEN_ON and OPEN_TRUNK_ON) or self.op_trunk_done:
            return False
        line = self._op_line(ct)
        if line is None or line["trunk"] is None:
            self.op_trunk_done = True
            return False
        trunk = line["trunk"]
        if ct.get_action_cooldown() != 0:
            return False
        p = ct.get_position()
        n = len(trunk)
        # Find the first tile of the line that is not standing yet.  A tile we
        # cannot READ (`_op_ours_at` -> None) is a tile outside this body's
        # r^2 = 20 vision, which on a 5-tile line is only ever one BEHIND us --
        # i.e. one we laid ourselves -- so it counts as standing.  What it may
        # NOT do is let us declare the line finished: a body thrown off by a
        # launcher reads every tile blind, and `op_trunk_done` is a one-way
        # latch that would cancel the harvester for the rest of the game.
        k = 0
        blind = False
        while k < n:
            got = self._op_ours_at(ct, trunk[k])
            if got is False:
                break
            if got is None:
                blind = True
            k += 1
        if k >= n:
            if not blind:
                self.op_trunk_done = True
            return False
        if k == 0:
            return False                     # the socket itself; _op_prefill
        t = trunk[k]
        if abs(p.x - t.x) + abs(p.y - t.y) != 1:
            return False                     # not adjacent yet; walk first
        if k == n - 1:
            # The terminus: the harvester, on the ore, LAST.
            try:
                if ct.get_global_resources() < ct.get_harvester_cost():
                    return False
                if not ct.can_build_harvester(t):
                    return False
                ct.build_harvester(t)
            except Exception:
                return False
            self.op_trunk_done = True
            try:
                ct.write_store(SLOT_HARVESTERS, ct.read_store(SLOT_HARVESTERS) + 1)
                if ct.read_store(SLOT_HARVESTERS) >= ECO_NEED:
                    ct.write_store(SLOT_ECO_READY, 1)
            except Exception:
                self.op_trunk_done = True
            if OPEN_LOG:
                print("OP feeder (%d,%d) seat=%d r=%d L=%d"
                      % (t.x, t.y, self.role_n, rnd, n - 1))
            return True
        f = t.cardinal_direction_to(trunk[k - 1])
        if f == Direction.CENTRE:
            return False
        try:
            if ct.get_global_resources() < ct.get_conveyor_cost():
                return False
            if not ct.can_build_conveyor(t, f):
                return False
            ct.build_conveyor(t, f)
        except Exception:
            return False
        return True

    def _op_trunk_walk(self, ct, rnd):
        """Step OUT along the trunk toward the next unbuilt tile.  True = moved.

        Conveyors are passable and stacks pass under bodies (engine G, N.10),
        so the body walks along its own finished line.
        """
        if not (OPEN_ON and OPEN_TRUNK_ON) or self.op_trunk_done:
            return False
        line = self._op_line(ct)
        if line is None or line["trunk"] is None:
            return False
        trunk = line["trunk"]
        n = len(trunk)
        k = 0
        while k < n:
            got = self._op_ours_at(ct, trunk[k])
            if got is False:
                break
            k += 1                           # ours, or blind behind us
        if k >= n or k == 0:
            return False
        p = ct.get_position()
        t = trunk[k]
        if abs(p.x - t.x) + abs(p.y - t.y) <= 1:
            return False                     # adjacent (or on it): build
        if ct.get_move_cooldown() != 0:
            return False
        self.tgt = trunk[k - 1]
        self._nav(ct, pave=False)
        return True

    # ------------------------------------------------------------------
    # THE STATION -- on FILLED sockets, never empty ones, never diagonals
    # ------------------------------------------------------------------

    def _op_station(self, ct, rnd):
        """Walk this body back onto its own filled socket.  True = moved.

        Bounded to the ferry window: while the cap holds, the two economy
        bodies ARE the heal wall (OPENING.md 4.4 -- 2 bodies = 8 HP/rd, the
        50-round kill window).  Once the cap lifts, fresh builders arrive and
        these two go back to the ordinary economy, where the base's own
        SEATHOLD and convergence planks keep the seats manned.
        """
        if not (OPEN_ON and OPEN_STATION_ON):
            return False
        if not self.op_trunk_done or rnd < OPEN_STATION_RND:
            return False
        g = self._op_geom(ct)
        if g is None:
            return False
        # "While the cap holds", read off the ONE signal that already exists:
        # SLOT_ROLE_N is the monotone count of builders that have ever taken a
        # turn, written by each body on its first turn.  No new slot, and no
        # dependence on the Core's own latch, which a builder cannot see.
        cap = OPEN_CAP_BAND_A if g["band"] in ("A1", "A2") else OPEN_CAP
        try:
            if ct.read_store(SLOT_ROLE_N) > cap:
                return False
        except Exception:
            return False
        line = self._op_line(ct)
        if line is None:
            return False
        if line["trunk"] is None:
            # PLUG-ONLY line (the ore gate refused the trunk): the socket is
            # bought, but the trunk behind it has still to be laid by the
            # ordinary economy, and a body standing still is a body not laying
            # it.  glacierkeep is L = 10; freezing two of three builders there
            # is the zero-collection game this whole arm exists to prevent.
            return False
        s = line["sock"]
        p = ct.get_position()
        if p.x == s.x and p.y == s.y:
            return True                      # holding: spend no move
        if not self._op_filled(ct, s):
            return False                     # never a body on an EMPTY socket
        try:
            if ct.get_tile_builder_bot_id(s) is not None:
                return False
        except Exception:
            return False
        if ct.get_move_cooldown() != 0:
            return False
        self.tgt = s
        self._nav(ct, pave=False)
        return True

    # ------------------------------------------------------------------
    # THE CAP, and the lift
    # ------------------------------------------------------------------

    # `_op_reserve` IS DELETED IN loki_leap18, AND THIS PARAGRAPH IS THE
    # RECORD.  It returned `2 * gunner cost + CB_RESERVE_EXTRA` and the cap
    # lift was gated on `bank - CB_RESERVE >= builder cost`.  Arm A3
    # (COUNTER-BATTERY, `CB_READY_ON`) was KILLED -- PLAN.md AMENDMENT
    # 2026-08-18 A1, on `results/wave22/cb_verdict.md` (1080 games, seeds
    # 191-199, -7.8 pp on mimic_jython2) -- and that amendment registers this
    # exact reference as the one that must be resolved before stage 1:
    # "Leaving a dead reserve in the opening arm would silently hold ~100 Ti
    # out of the economy for a plank that no longer exists."
    #
    # It is resolved by DELETION, not by `CB_RESERVE = 0`, so that no later
    # edit can re-arm a reserve for an arm that is gone.  `CB_RESERVE_EXTRA`
    # survives in doctrine.py as the record of the killed arm's price and is
    # now READ BY NOTHING.  The gate below is `bank >= builder cost`.
    #
    # The same kill applies to A4's `SIP_RESERVE_ON` (sip.py `_sip_reserve`):
    # its doctrine comment says "flip it True in the stage-3 integration build
    # (where A3 exists)".  A3 does not exist in this build either, so it stays
    # False and the tap is funded from `SIP_BANK_FLOOR`.  Flipping it True
    # here would hold 154-162 Ti against a measured 2-95 Ti bank and make the
    # siphon inert by arithmetic -- the measured finding in its own doctrine.

    def _op_cap(self, ct, rnd, ti, cost):
        """The builder ceiling this round, or None for "no opinion".

        3 while the ferry is live, 4 in band A.  The lift is at ARRIVAL and is
        gated on the counter-battery reserve, and it LATCHES: a bank that dips
        below the reserve later must not re-close a population that is already
        spawned.
        """
        if not OPEN_ON:
            return None
        g = self._op_geom(ct)
        if g is None:
            return None
        if self.op_lift:
            return None
        cap = OPEN_CAP_BAND_A if g["band"] in ("A1", "A2") else OPEN_CAP
        # THE CAP-LIFT GATE, POST-A3-KILL: `bank >= builder cost`, and nothing
        # else.  See the paragraph above `_op_cap`'s neighbour for why the
        # counter-battery reserve term is gone rather than zeroed.
        if rnd >= g["arrival"] and ti >= cost:
            self.op_lift = True
            if OPEN_LOG and not self.op_lift_log:
                self.op_lift_log = True
                print("OP capliftr=%d ti=%d resv=0 cap=%d band=%s"
                      % (rnd, ti, cap, g["band"]))
            return None
        return cap

    def _op_spawn_tile(self, ct, n):
        """The seat-`n` spawn tile this opening wants, or None.

        Seat 0 is the rider and starts on the ring tile with the smallest walk
        distance to their ring; seats 1 and 2 are the economy and start on the
        DIAGONAL that owns their socket, which is what makes the socket cost
        one action and zero moves; seat 3 is band A's second turret rider.
        """
        if not OPEN_ON:
            return None
        g = self._op_geom(ct)
        if g is None:
            return None
        if n == 1 and g["e1"] is not None:
            return g["e1"]["diag"]
        if n == 2 and g["e2"] is not None:
            return g["e2"]["diag"]
        riders = g["riders"]
        if n == 0 and riders:
            return riders[0]
        if n == 3 and g["band"] in ("A1", "A2") and len(riders) >= 2:
            return riders[1]
        return None

    # ------------------------------------------------------------------
    # BAND A -- the payload switch
    # ------------------------------------------------------------------

    def _op_pair_seat(self):
        """May THIS body build one of the two band-A pair sentinels?

        ZERO-COMM by construction (PLAN 1.5): the two eligible bodies are the
        two lowest raid slots, and each carries its own one-shot latch.  The
        buffered store cannot be trusted for a count -- fixtures.md 2 measured
        THREE pair sentinels the one time it was.
        """
        return (self.role == "raid" and self.raid_slot < OPEN_PAIR_N
                and not self.op_pair_built)

    def _op_pair(self, ct, E, rnd):
        """Band A's forward sentinel pair.  True = the action was spent.

        A-1 builds it from our own ring (the map is short enough that our own
        ring already sits within ~6 of their Core); A-2 rides the 1-2 rung
        mini-ferry out first and builds the same turret payload forward.  Same
        mechanism, different cargo -- one book with a payload switch, which is
        what retires the "two doctrines to maintain" risk (OPENING.md 5.1).
        """
        if not (OPEN_ON and A2_TURRET):
            return False
        if not self._op_pair_seat():
            return False
        if rnd < OPEN_PAIR_EARLIEST or rnd > OPEN_PAIR_DEADLINE:
            return False
        g = self._op_geom(ct)
        if g is None or g["band"] not in ("A1", "A2"):
            return False
        if ct.get_action_cooldown() != 0:
            return False
        if E is None:
            E = g["enemy"]
        if E is None:
            return False
        try:
            cost = ct.get_sentinel_cost()
            if ct.get_global_resources() < cost + OPEN_PAIR_TI_FLOOR:
                return False
        except Exception:
            return False
        p = ct.get_position()
        hard = rnd >= OPEN_PAIR_DEADLINE
        # Different axes, so a single approach cannot be shielded: rider 0
        # prefers the axis of the larger offset to their Core, rider 1 the
        # other.  Derived from the seat, so the two never argue.
        dx, dy = E.x - p.x, E.y - p.y
        if (abs(dx) >= abs(dy)) == (self.raid_slot == 0):
            order = (Direction.EAST if dx > 0 else Direction.WEST,
                     Direction.SOUTH if dy > 0 else Direction.NORTH)
        else:
            order = (Direction.SOUTH if dy > 0 else Direction.NORTH,
                     Direction.EAST if dx > 0 else Direction.WEST)
        best = None
        for ddx, ddy in _CARD4:
            tx, ty = p.x + ddx, p.y + ddy
            if not (0 <= tx < self.mw and 0 <= ty < self.mh):
                continue
            t = Position(tx, ty)
            if dsq_core(t, E) > OPEN_PAIR_MAX_DSQ and not hard:
                continue
            # Never on one of our OWN twelve ring tiles: a turret there is
            # impassable, plugs our own spawns and kills a heal seat.
            if self.core is not None and dsq_core(t, self.core) <= 2:
                continue
            for f in order:
                try:
                    if not ct.can_build_sentinel(t, f):
                        continue
                except Exception:
                    continue
                key = (0 if self._op_ray_hits(t, f, E) else 1, dsq_core(t, E))
                if best is None or key < best[0]:
                    best = (key, t, f)
            if best is not None and best[0][0] == 0:
                break
        if best is None:
            return False
        if best[0][0] != 0 and not hard:
            return False                     # before the deadline, aim or wait
        t, f = best[1], best[2]
        try:
            ct.build_sentinel(t, f)
        except Exception:
            return False
        self.op_pair_built = True
        try:
            ct.write_store(SLOT_FWD_GUN, ct.read_store(SLOT_FWD_GUN) + 1)
        except Exception:
            self.op_pair_built = True
        if OPEN_LOG:
            print("OP pair (%d,%d) f=%s r=%d s=%d d=%d"
                  % (t.x, t.y, f.value, rnd, self.raid_slot, dsq_core(t, E)))
        return True

    def _op_ray_hits(self, t, f, E):
        """Does the 5-tile fixed cardinal line from `t` facing `f` cover their
        Core footprint?  Walls and units do not block a turret line (engine D),
        so this is pure geometry."""
        dx, dy = f.delta()
        x, y = t.x, t.y
        i = 0
        while i < 5:
            i += 1
            x += dx
            y += dy
            if E.x <= x <= E.x + 1 and E.y <= y <= E.y + 1:
                return True
        return False

    def _op_cage_ok(self, ct, rnd):
        """May we spend on the barrier cage this round?

        Band A does not build it: `rb30 <= 2` is a registered bar (F7.1) and
        the band-A counter-book is a live turret pair before their ferry
        lands, not a seal.  Every other band is unchanged.
        """
        if not OPEN_ON:
            return True
        if rnd >= OPEN_A_CAGE_RND:
            return True
        g = self._op_geom(ct)
        if g is None:
            return True
        return g["band"] not in ("A1", "A2")
