"""LOKI-SENTSHELL (#73) -- the fixture, every cell driven to BOTH verdicts.

WHAT IS BEING ASSERTED, and why each cell has a complement.  A guard is not
done when it passes, it is done when it has been driven to the answer it is
supposed to refuse; a check that has never produced the other verdict has not
been seen to check.

  1. ORDER.  A builder must be orthogonally adjacent to build, and the only
     tiles orthogonally adjacent to the sentinel tile ARE the shell tiles, so a
     completed shell built first makes the sentinel UNBUILDABLE.  Cell: the
     shell path refuses to fire while no friendly sentinel exists, the plant
     registers the obligation, and a pre-built 4-tile shell leaves no legal
     standing tile for the plant.  COMPLEMENT: with the shell absent, the same
     site IS buildable.

  2. THREE SIDES, NEVER FOUR.  Exactly LOKI_SHELL_MAX barriers land and the
     heal seat -- the cardinal neighbour farthest from the enemy Core, i.e. our
     approach -- stays open and passable.  COMPLEMENT: raise LOKI_SHELL_MAX to
     4 on the same fixture and the 4th barrier DOES land, proving the constant
     is what holds the seat open and not an accident of the geometry.

  3. LIVE GUNNER RAY PRIORITY.  A DIAGONAL neighbour that an enemy gunner
     actually holds outranks a cardinal that nobody threatens (gunners are
     67.1% of the final blows on our forward sentinels and gunner fire is
     obstacle-blocked; melee is 13.2%).  COMPLEMENT: the same gunner with its
     ray broken by a wall must NOT promote that diagonal.

  4. ESCAPE GUARD.  A barrier that would seal this body's last passable
     cardinal neighbour is refused (ported from _v70sb/main.py:1508-1522; we
     have a field observation of a bot self-immuring for 221 rounds and there
     is no ct.destroy() anywhere in this tree).  COMPLEMENT: open one other
     neighbour on the identical board and the same barrier IS laid.

  5. TOGGLE OFF == BASE.  A transcript of every decision the shell touches
     (_try_forward_sentinel's build site and facing, its store writes,
     _try_shell, _shell_station) is recorded over a scenario grid in a
     SUBPROCESS per tree -- the two trees share module names, so they cannot be
     imported into one interpreter -- and the base tree's transcript must equal
     the variant's with LOKI_SENTSHELL_ON monkeypatched False.  COMPLEMENT: the
     variant with the toggle ON must DIFFER, or the transcript is measuring
     nothing.

THE STUB ENCODES THE DISASSEMBLED ENGINE, not the organisers' doc: a sentinel's
can_fire_from is a pure arithmetic ray walk with NO obstacle test, a gunner's
walks every tile before the target and fails on any hit, build/heal/attack are
Manhattan-1 exactly, and only conveyors/splitters are bot-passable.

RUN: .venv/bin/python tests/test_sentshell.py
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_TREE = os.path.join(ROOT, "bots", "_v223sealrepair")
VAR_TREE = os.path.join(ROOT, "bots", "_v273sentshell")

from fcode import Direction, EntityType, Environment, Position, Team  # noqa: E402

PASSABLE_BUILDINGS = (EntityType.CONVEYOR, EntityType.SPLITTER)


# ---------------------------------------------------------------------------
# the stub controller
# ---------------------------------------------------------------------------

class Stub:
    """A grid the size of a unit test, with the engine's OWN predicates.

    Only the calls this plank makes are implemented; anything else raising is
    a feature, because it means the fixture never silently answers a question
    the real Controller would have answered differently.
    """

    def __init__(self, w, h, pos, team=Team.A, ti=4000, rnd=60):
        self.w, self.h = w, h
        self.pos = pos
        self.team = team
        self.ti = ti
        self.rnd = rnd
        self.walls = set()
        self.buildings = {}          # (x,y) -> dict(id, type, team, dir)
        self.by_id = {}
        self.bots = {}               # (x,y) -> dict(id, team)
        self.store = [0] * 16
        self.built = []              # (kind, Position, Direction|None)
        self.writes = []             # (slot, value)
        self.next_id = 1000
        self.vision_dsq = 20         # builder bot

    # --- fixture helpers (not Controller API) ---
    def add_building(self, pos, etype, team=None, direction=None):
        self.next_id += 1
        rec = {"id": self.next_id, "type": etype,
               "team": self.team if team is None else team, "dir": direction,
               "pos": pos}
        self.buildings[(pos.x, pos.y)] = rec
        self.by_id[rec["id"]] = rec
        return rec["id"]

    def add_wall(self, pos):
        self.walls.add((pos.x, pos.y))

    def add_bot(self, pos, team=None):
        self.next_id += 1
        self.bots[(pos.x, pos.y)] = {
            "id": self.next_id, "team": self.team if team is None else team}
        return self.next_id

    def _in(self, pos):
        return 0 <= pos.x < self.w and 0 <= pos.y < self.h

    # --- info ---
    def get_id(self):
        return 1

    def get_team(self, id=None):
        if id is None or id == 1:
            return self.team
        return self.by_id[id]["team"]

    def get_position(self, id=None):
        if id is None or id == 1:
            return self.pos
        return self.by_id[id]["pos"]

    def get_entity_type(self, id=None):
        if id is None or id == 1:
            return EntityType.BUILDER_BOT
        return self.by_id[id]["type"]

    def get_direction(self, id=None):
        d = self.by_id[id]["dir"]
        if d is None:
            raise ValueError("no direction")
        return d

    def get_current_round(self):
        return self.rnd

    def get_global_resources(self):
        return self.ti

    def get_map_width(self):
        return self.w

    def get_map_height(self):
        return self.h

    def get_cpu_time_elapsed(self):
        return 0

    def get_barrier_cost(self):
        return 3

    def get_sentinel_cost(self):
        return 30

    def read_store(self, i):
        return self.store[i]

    def write_store(self, i, v):
        self.writes.append((i, v))
        self.store[i] = v

    def get_action_cooldown(self):
        return 0

    def get_move_cooldown(self):
        return 0

    # --- tiles.  get_tile_* RAISES off-map; is_in_vision returns False. ---
    def get_tile_env(self, pos):
        if not self._in(pos):
            raise IndexError("off map")
        return Environment.WALL if (pos.x, pos.y) in self.walls else Environment.EMPTY

    def get_tile_building_id(self, pos):
        if not self._in(pos):
            raise IndexError("off map")
        rec = self.buildings.get((pos.x, pos.y))
        return None if rec is None else rec["id"]

    def get_tile_builder_bot_id(self, pos):
        if not self._in(pos):
            raise IndexError("off map")
        rec = self.bots.get((pos.x, pos.y))
        return None if rec is None else rec["id"]

    def is_in_vision(self, pos):
        if not self._in(pos):
            return False
        return self.pos.distance_squared(pos) <= self.vision_dsq

    def is_tile_empty(self, pos):
        if not self._in(pos):
            raise IndexError("off map")
        return (pos.x, pos.y) not in self.walls and (pos.x, pos.y) not in self.buildings

    def is_tile_passable(self, pos):
        """Engine: kinds 1 (conveyor) and 2 (splitter) are the only
        bot-passable buildings -- which is what makes a BARRIER shell
        launcher-proof and a conveyor shell an invitation."""
        if not self._in(pos):
            return False
        if (pos.x, pos.y) in self.walls:
            return False
        if (pos.x, pos.y) in self.bots:
            return False
        rec = self.buildings.get((pos.x, pos.y))
        if rec is not None and rec["type"] not in PASSABLE_BUILDINGS:
            return False
        return True

    def get_nearby_buildings(self, dist_sq=None):
        lim = self.vision_dsq if dist_sq is None else dist_sq
        return [r["id"] for r in self.buildings.values()
                if self.pos.distance_squared(r["pos"]) <= lim]

    def get_nearby_entities(self, dist_sq=None):
        return self.get_nearby_buildings(dist_sq)

    # --- turret geometry, straight off the disassembly ---
    @staticmethod
    def _ray(origin, direction, target):
        dx, dy = direction.delta()
        if dx == 0 and dy == 0:
            return None
        ox, oy = target.x - origin.x, target.y - origin.y
        for k in range(1, 9):
            if ox == dx * k and oy == dy * k:
                return k
        return None

    def can_fire_from(self, position, direction, turret_type, target):
        k = self._ray(position, direction, target)
        if k is None:
            return False
        d2 = position.distance_squared(target)
        if turret_type == EntityType.SENTINEL:
            # PURE ARITHMETIC: range then dx^2+dy^2.  No tile is ever loaded,
            # so obstacle-blindness is unreachable rather than merely unchecked.
            return d2 <= 32
        if turret_type == EntityType.GUNNER:
            if d2 > 13:
                return False
            dx, dy = direction.delta()
            for j in range(1, k):
                q = Position(position.x + dx * j, position.y + dy * j)
                if not self._in(q):
                    return False
                if (q.x, q.y) in self.walls or (q.x, q.y) in self.buildings:
                    return False
                if (q.x, q.y) in self.bots:
                    return False
            return True
        raise ValueError(turret_type)

    def get_attackable_tiles_from(self, position, direction, turret_type):
        lim = 13 if turret_type == EntityType.GUNNER else 32
        dx, dy = direction.delta()
        out = []
        for k in range(1, 9):
            q = Position(position.x + dx * k, position.y + dy * k)
            if position.distance_squared(q) > lim:
                break
            if self._in(q):
                out.append(q)
        return out

    # --- building ---
    def _buildable(self, pos, cost):
        if not self._in(pos):
            return False
        if abs(pos.x - self.pos.x) + abs(pos.y - self.pos.y) != 1:
            return False        # MANHATTAN-1 EXACTLY: no own tile, no diagonal
        if (pos.x, pos.y) in self.walls:
            return False
        if (pos.x, pos.y) in self.buildings or (pos.x, pos.y) in self.bots:
            return False
        return self.ti >= cost

    def can_build_barrier(self, pos):
        return self._buildable(pos, 3)

    def build_barrier(self, pos):
        if not self.can_build_barrier(pos):
            raise RuntimeError("illegal barrier")
        self.ti -= 3
        self.built.append(("barrier", (pos.x, pos.y), None))
        return self.add_building(pos, EntityType.BARRIER)

    def can_build_sentinel(self, pos, direction):
        return self._buildable(pos, 30)

    def build_sentinel(self, pos, direction):
        if not self.can_build_sentinel(pos, direction):
            raise RuntimeError("illegal sentinel")
        self.ti -= 30
        self.built.append(("sentinel", (pos.x, pos.y), direction.name))
        return self.add_building(pos, EntityType.SENTINEL, direction=direction)


# ---------------------------------------------------------------------------
# tree loading
# ---------------------------------------------------------------------------

def load(tree):
    for m in ("doctrine", "eco", "raid", "main"):
        sys.modules.pop(m, None)
    sys.path.insert(0, tree)
    import main as mainmod
    import raid as raidmod
    return mainmod, raidmod


def make_player(mainmod, w, h, core, enemy):
    p = mainmod.Player()
    p.team = Team.A
    p.core = core
    p.enemy = enemy
    p.mw, p.mh = w, h
    p.map_grid = None
    return p


# ---------------------------------------------------------------------------
# the scenario grid, shared by the transcript mode and the assertions
# ---------------------------------------------------------------------------

W, H = 20, 20
ENEMY = Position(14, 14)      # 2x2 footprint anchor
OURCORE = Position(2, 2)


def scenarios():
    """(name, raider position, walls, extra buildings) -- covers in-band and
    out-of-band sites, a border site, and a site with terrain on one side."""
    out = []
    for pos in (Position(10, 10), Position(11, 11), Position(12, 12),
                Position(13, 13), Position(9, 14), Position(14, 9),
                Position(12, 10), Position(10, 12), Position(11, 14),
                Position(14, 11), Position(13, 10), Position(8, 8)):
        out.append(("open@%d,%d" % (pos.x, pos.y), pos, [], []))
    out.append(("walled@11,11", Position(11, 11),
                [Position(10, 11), Position(11, 10)], []))
    out.append(("clutter@12,12", Position(12, 12), [],
                [(Position(12, 11), EntityType.BARRIER)]))
    return out


def transcript(tree, force_off):
    mainmod, raidmod = load(tree)
    if force_off:
        # `from doctrine import *` binds the flag into raid's namespace, so the
        # override has to land THERE, not on doctrine.
        raidmod.LOKI_SENTSHELL_ON = False
    rows = []
    for name, pos, walls, blds in scenarios():
        ct = Stub(W, H, pos)
        for wpos in walls:
            ct.add_wall(wpos)
        for bpos, bt in blds:
            ct.add_building(bpos, bt, team=Team.B)
        ct.store[4] = 4          # SLOT_HARVESTERS -- clears the eco gate
        pl = make_player(mainmod, W, H, OURCORE, ENEMY)
        got = pl._try_forward_sentinel(ct, ENEMY)
        rows.append({
            "case": name,
            "ret": bool(got),
            "built": ct.built,
            "writes": ct.writes,
        })
    return rows


# ---------------------------------------------------------------------------
# assertions
# ---------------------------------------------------------------------------

FAILS = []
CHECKS = [0]


def check(label, cond):
    CHECKS[0] += 1
    print(("  ok   " if cond else "  FAIL ") + label)
    if not cond:
        FAILS.append(label)


def shell_positions(ct):
    return sorted(b[1] for b in ct.built if b[0] == "barrier")


def run_shell_loop(pl, ct, S, limit=30):
    """Drive the plank the way the game does: act if we can, else WALK to the
    seat the plank asks for.  The walk is a teleport to _shell_station's answer
    -- the real one goes through the tree's own _nav/_bfs_direction, which this
    fixture is not re-implementing (and must not: there is exactly one
    pathfinder in this tree and it is eco.py's)."""
    for _ in range(limit):
        if pl._try_shell(ct, ENEMY):
            ct.rnd += 1
            continue
        st = pl._shell_station(ct, ENEMY)
        if st is None:
            return
        if (st.x, st.y) == (ct.pos.x, ct.pos.y):
            return                     # asked for a seat we are on and still no build
        ct.pos = st
        ct.rnd += 1


def test_order():
    print("\n1. ORDER: sentinel first, then shell")
    mainmod, raidmod = load(VAR_TREE)
    pos = Position(11, 11)
    ct = Stub(W, H, pos)
    ct.store[4] = 4
    pl = make_player(mainmod, W, H, OURCORE, ENEMY)

    check("shell path refuses to fire with no friendly sentinel on the board",
          pl._try_shell(ct, ENEMY) is False and ct.built == [])
    check("no obligation registered before any plant", pl.shell_sent is None)

    built = pl._try_forward_sentinel(ct, ENEMY)
    sent = [b for b in ct.built if b[0] == "sentinel"]
    check("the sentinel is planted first", built is True and len(sent) == 1)
    check("nothing but the sentinel was built on that turn", len(ct.built) == 1)
    S = Position(*sent[0][1])
    check("the plant registers the shell obligation on the planter",
          pl.shell_sent == (S.x, S.y) and pl.shell_rnd == ct.rnd)
    check("the site is IN BAND (d^2 >= LOKI_SHELL_MIN_DSQ of the enemy Core)",
          min(S.distance_squared(c)
              for c in raidmod.core_tiles(ENEMY)) >= raidmod.LOKI_SHELL_MIN_DSQ)

    # COMPLEMENT: the same site with a completed 4-tile shell already down is
    # unbuildable, which is the reason the order is a hard constraint.
    ct2 = Stub(W, H, pos)
    ct2.store[4] = 4
    for d in (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST):
        ct2.add_building(S.add(d), EntityType.BARRIER)
    stands = [S.add(d) for d in
              (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)]
    check("shell-first: NO tile a builder could stand on to plant it remains",
          all(not ct2.is_tile_passable(t) for t in stands))
    check("complement -- with the shell absent those same tiles ARE standable",
          all(Stub(W, H, pos).is_tile_passable(t) for t in stands))


def test_three_sides():
    print("\n2. EXACTLY THREE BARRIERS, HEAL SEAT LEFT OPEN")
    mainmod, raidmod = load(VAR_TREE)
    S = Position(11, 11)
    ct = Stub(W, H, Position(11, 12))
    pl = make_player(mainmod, W, H, OURCORE, ENEMY)
    ct.add_building(S, EntityType.SENTINEL, direction=Direction.SOUTHEAST)
    pl.shell_sent = (S.x, S.y)
    pl.shell_rnd = ct.rnd
    run_shell_loop(pl, ct, S)

    bars = shell_positions(ct)
    seat = pl._shell_seat(ct, S, ENEMY)
    check("exactly LOKI_SHELL_MAX barriers were laid (%d)" % len(bars),
          len(bars) == raidmod.LOKI_SHELL_MAX)
    check("the heal seat is NOT one of them", (seat.x, seat.y) not in bars)
    check("the heal seat is Manhattan-1 from the sentinel (can_heal's rule)",
          abs(seat.x - S.x) + abs(seat.y - S.y) == 1)
    check("the heal seat is still passable, so a raider can sit and heal",
          ct.is_tile_passable(seat))
    tiles = raidmod.core_tiles(ENEMY)
    seat_d = min(seat.distance_squared(c) for c in tiles)
    others = [S.add(d) for d in (Direction.NORTH, Direction.EAST,
                                 Direction.SOUTH, Direction.WEST)
              if (S.add(d).x, S.add(d).y) != (seat.x, seat.y)]
    check("the open side faces OUR approach (farthest cardinal from their Core)",
          all(seat_d >= min(o.distance_squared(c) for c in tiles) for o in others))
    check("all three barriers are orthogonal neighbours of the sentinel",
          all(abs(bx - S.x) + abs(by - S.y) == 1 for bx, by in bars))
    check("the budget is spent: no further shell action is offered",
          pl._try_shell(ct, ENEMY) is False
          and pl._shell_station(ct, ENEMY) is None
          and pl.shell_sent is None)

    # COMPLEMENT: the 3 is the CONSTANT, not the geometry.  Raise the budget on
    # the identical board and the fourth side must close.
    old = raidmod.LOKI_SHELL_MAX
    try:
        raidmod.LOKI_SHELL_MAX = 4
        ct2 = Stub(W, H, Position(11, 12))
        pl2 = make_player(mainmod, W, H, OURCORE, ENEMY)
        ct2.add_building(S, EntityType.SENTINEL, direction=Direction.SOUTHEAST)
        pl2.shell_sent = (S.x, S.y)
        pl2.shell_rnd = ct2.rnd
        run_shell_loop(pl2, ct2, S)
        check("complement -- with LOKI_SHELL_MAX=4 the fourth barrier DOES land",
              len(shell_positions(ct2)) == 4)
    finally:
        raidmod.LOKI_SHELL_MAX = old


def test_ray_priority():
    print("\n3. A LIVE GUNNER RAY OUTRANKS A DEAD ONE")
    mainmod, raidmod = load(VAR_TREE)
    S = Position(11, 11)
    # An enemy gunner on the NORTHWEST diagonal, facing SOUTHEAST at the
    # sentinel: d^2 = 8 <= 13 and the line is clear, so its ray is LIVE and the
    # tile that closes it is the DIAGONAL neighbour S+NORTHWEST.
    G = Position(9, 9)
    block = S.add(Direction.NORTHWEST)

    ct = Stub(W, H, Position(11, 12))
    pl = make_player(mainmod, W, H, OURCORE, ENEMY)
    ct.add_building(S, EntityType.SENTINEL, direction=Direction.SOUTHEAST)
    ct.add_building(G, EntityType.GUNNER, team=Team.B, direction=Direction.SOUTHEAST)
    check("the fixture's gunner really can hit the sentinel right now",
          ct.can_fire_from(G, Direction.SOUTHEAST, EntityType.GUNNER, S))
    rays = pl._shell_rays(ct, S)
    check("the ray's blocking tile is the DIAGONAL neighbour",
          (block.x, block.y) in rays)
    wanted, _ = pl._shell_plan(ct, S, ENEMY)
    check("the held diagonal is ranked FIRST, ahead of every unthreatened cardinal",
          (wanted[0].x, wanted[0].y) == (block.x, block.y))
    check("cardinals still outrank the unheld diagonals behind it",
          all(abs(t.x - S.x) + abs(t.y - S.y) == 1 for t in wanted[1:3]))

    # COMPLEMENT: the SAME gunner on the SAME tile, turned away.  (A wall is
    # not available as the complement here and that is itself a finding: a
    # gunner's reach is d^2 <= 13, so on a diagonal the only tile strictly
    # between it and the sentinel IS the adjacent one -- a diagonal ray can be
    # broken ONLY at the tile the shell wants anyway.)
    ct2 = Stub(W, H, Position(11, 12))
    pl2 = make_player(mainmod, W, H, OURCORE, ENEMY)
    ct2.add_building(S, EntityType.SENTINEL, direction=Direction.SOUTHEAST)
    ct2.add_building(G, EntityType.GUNNER, team=Team.B, direction=Direction.SOUTH)
    check("complement -- a facing that does not contain S kills can_fire_from",
          not ct2.can_fire_from(G, Direction.SOUTH, EntityType.GUNNER, S))
    check("complement -- with the ray dead the diagonal is NOT promoted",
          (block.x, block.y) not in pl2._shell_rays(ct2, S))
    w2, _ = pl2._shell_plan(ct2, S, ENEMY)
    check("complement -- a cardinal takes first place instead",
          abs(w2[0].x - S.x) + abs(w2[0].y - S.y) == 1)
    check("complement -- and the tile itself is still a candidate, just later",
          any((t.x, t.y) == (block.x, block.y) for t in w2))

    # AND THE SENTINEL DOES NOT CARE: the shell is free for us, by construction.
    ct3 = Stub(W, H, Position(11, 12))
    for d in (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST,
              Direction.NORTHEAST, Direction.NORTHWEST, Direction.SOUTHEAST,
              Direction.SOUTHWEST):
        ct3.add_building(S.add(d), EntityType.BARRIER)
    check("a COMPLETELY walled-in sentinel still has line to the enemy Core",
          ct3.can_fire_from(S, Direction.SOUTHEAST, EntityType.SENTINEL,
                            Position(14, 14)))
    check("complement -- a walled-in GUNNER does not",
          not ct3.can_fire_from(S, Direction.SOUTHEAST, EntityType.GUNNER,
                                Position(13, 13)))


def test_escape_guard():
    print("\n4. ESCAPE GUARD: no barrier that immures this body")
    mainmod, raidmod = load(VAR_TREE)
    S = Position(11, 11)
    P = Position(11, 12)        # stands south of the sentinel
    # From P the only shell tile in reach is... none (Manhattan-2), so put the
    # body where it can actually build one: diagonal to S, beside S+EAST.
    P = Position(12, 12)
    T = Position(12, 11)        # == S + EAST, a wanted cardinal shell tile

    def board(open_escape):
        ct = Stub(W, H, P)
        ct.add_building(S, EntityType.SENTINEL, direction=Direction.SOUTHEAST)
        # Seal every cardinal neighbour of P except T itself...
        ct.add_wall(Position(11, 12))
        ct.add_wall(Position(12, 13))
        if open_escape:
            pass                     # ...and leave (13,12) open
        else:
            ct.add_wall(Position(13, 12))
        return ct

    ct_trap = board(open_escape=False)
    pl = make_player(mainmod, W, H, OURCORE, ENEMY)
    check("the trap board really would leave zero exits",
          all(not ct_trap.is_tile_passable(Position(*q))
              for q in ((11, 12), (12, 13), (13, 12))))
    check("the barrier is legal by every OTHER rule (can_build_barrier True)",
          ct_trap.can_build_barrier(T))
    check("_shell_tile_ok REFUSES it", pl._shell_tile_ok(ct_trap, P, T) is False)
    check("and no barrier is laid", pl._try_shell(ct_trap, ENEMY) is False
          and shell_positions(ct_trap) == [])

    ct_ok = board(open_escape=True)
    pl2 = make_player(mainmod, W, H, OURCORE, ENEMY)
    check("complement -- one open exit and _shell_tile_ok ALLOWS it",
          pl2._shell_tile_ok(ct_ok, P, T) is True)
    check("complement -- the same barrier IS laid",
          pl2._try_shell(ct_ok, ENEMY) is True
          and shell_positions(ct_ok) == [(T.x, T.y)])

    # FRIENDLY GUNNER RAY GUARD, same shape.
    ct_g = board(open_escape=True)
    ct_g.add_building(Position(12, 9), EntityType.GUNNER, team=Team.A,
                      direction=Direction.SOUTH)
    pl3 = make_player(mainmod, W, H, OURCORE, ENEMY)
    check("a shell tile inside OUR OWN gunner's pattern is refused",
          pl3._shell_friendly_ray(ct_g, T) is True
          and pl3._shell_tile_ok(ct_g, P, T) is False)
    ct_g2 = board(open_escape=True)
    ct_g2.add_building(Position(12, 9), EntityType.GUNNER, team=Team.B,
                       direction=Direction.SOUTH)
    pl4 = make_player(mainmod, W, H, OURCORE, ENEMY)
    check("complement -- the identical gunner on the ENEMY team does not veto",
          pl4._shell_friendly_ray(ct_g2, T) is False
          and pl4._shell_tile_ok(ct_g2, P, T) is True)


def test_stall_release():
    print("\n4b. STALL RELEASE: an undischargeable obligation lets the body go")
    mainmod, raidmod = load(VAR_TREE)
    S = Position(11, 11)
    P = Position(12, 12)
    T = Position(12, 11)        # S + EAST: the top-ranked wanted tile

    def board():
        # Every guard PASSES on T -- the only thing refusing the build is a
        # friendly body parked on the tile, i.e. a refusal that walking cannot
        # fix and that _shell_station cannot see when it picks the seat.
        ct = Stub(W, H, P)
        ct.add_building(S, EntityType.SENTINEL, direction=Direction.SOUTHEAST)
        ct.add_bot(T)
        # Wall off the only OTHER wanted tile this body can reach, or the plank
        # correctly builds that one instead and the stall is never exercised.
        ct.add_wall(Position(11, 12))
        return ct

    ct = board()
    pl = make_player(mainmod, W, H, OURCORE, ENEMY)
    pl.shell_sent = (S.x, S.y)
    pl.shell_rnd = ct.rnd
    check("the fixture really does refuse this build for a non-guard reason",
          pl._shell_tile_ok(ct, P, T) is True and ct.can_build_barrier(T) is False)
    check("and the plank declines to act on it",
          pl._try_shell(ct, ENEMY) is False)
    held = 0
    for _ in range(raidmod.LOKI_SHELL_WINDOW + 6):
        st = pl._shell_station(ct, ENEMY)
        if st is None:
            break
        held += 1
        check_seat = (st.x, st.y) == (P.x, P.y)
        ct.pos = st
        ct.rnd += 1
    check("the seat it asks for is the one it is already on (%s)" % check_seat,
          check_seat)
    check("released after ~LOKI_SHELL_STALL rounds, not the whole window "
          "(held %d, stall %d, window %d)"
          % (held, raidmod.LOKI_SHELL_STALL, raidmod.LOKI_SHELL_WINDOW),
          0 < held <= raidmod.LOKI_SHELL_STALL + 2
          and held < raidmod.LOKI_SHELL_WINDOW)
    check("and the obligation is cleared, so the next plant is unblocked",
          pl.shell_sent is None and pl._shell_owed(ct, ENEMY) is False)

    # COMPLEMENT: a NON-zero action cooldown is exactly the case where standing
    # still is correct, and it must NOT count toward the stall.
    ct2 = board()
    ct2.get_action_cooldown = lambda: 1
    pl2 = make_player(mainmod, W, H, OURCORE, ENEMY)
    pl2.shell_sent = (S.x, S.y)
    pl2.shell_rnd = ct2.rnd
    held2 = 0
    for _ in range(raidmod.LOKI_SHELL_WINDOW + 6):
        st = pl2._shell_station(ct2, ENEMY)
        if st is None:
            break
        held2 += 1
        ct2.pos = st
        ct2.rnd += 1
    check("complement -- on a live cooldown the body waits, and it is the "
          "WINDOW that releases it (held %d)" % held2,
          held2 > raidmod.LOKI_SHELL_STALL + 2)


def test_toggle_off_is_base():
    print("\n5. TOGGLE OFF == BASE (subprocess transcripts, one per tree)")
    here = os.path.abspath(__file__)
    base = json.loads(subprocess.run(
        [sys.executable, here, "--transcript", BASE_TREE],
        capture_output=True, text=True, check=True).stdout)
    off = json.loads(subprocess.run(
        [sys.executable, here, "--transcript", VAR_TREE, "--off"],
        capture_output=True, text=True, check=True).stdout)
    on = json.loads(subprocess.run(
        [sys.executable, here, "--transcript", VAR_TREE],
        capture_output=True, text=True, check=True).stdout)
    check("the grid is not empty (%d cases)" % len(base), len(base) >= 12)
    check("LOKI_SENTSHELL_ON=False reproduces the base tree exactly",
          off == base)
    diffs = [b["case"] for b, o in zip(base, on) if b != o]
    check("complement -- LOKI_SENTSHELL_ON=True DIFFERS (%d of %d cases: %s)"
          % (len(diffs), len(base), ", ".join(diffs[:4])), len(diffs) > 0)

    # And the OFF path must be inert in the two entry points that are new.
    mainmod, raidmod = load(VAR_TREE)
    raidmod.LOKI_SENTSHELL_ON = False
    S = Position(11, 11)
    ct = Stub(W, H, Position(11, 12))
    pl = make_player(mainmod, W, H, OURCORE, ENEMY)
    ct.add_building(S, EntityType.SENTINEL, direction=Direction.SOUTHEAST)
    pl.shell_sent = (S.x, S.y)
    pl.shell_rnd = ct.rnd
    check("OFF: _try_shell is inert", pl._try_shell(ct, ENEMY) is False)
    check("OFF: _shell_station is inert", pl._shell_station(ct, ENEMY) is None)
    check("OFF: nothing was built", ct.built == [])
    raidmod.LOKI_SENTSHELL_ON = True
    check("complement -- flipped back ON the same board DOES act",
          pl._shell_station(ct, ENEMY) is not None)


def main():
    if "--transcript" in sys.argv:
        tree = sys.argv[sys.argv.index("--transcript") + 1]
        print(json.dumps(transcript(tree, "--off" in sys.argv)))
        return 0
    test_order()
    test_three_sides()
    test_ray_priority()
    test_escape_guard()
    test_stall_release()
    test_toggle_off_is_base()
    print("\n%d checks, %d failed" % (CHECKS[0], len(FAILS)))
    for f in FAILS:
        print("  FAILED: " + f)
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
