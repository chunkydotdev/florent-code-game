#!/usr/bin/env python3
"""s53 / QUEUE #109 -- BOTH-WAYS DRIVE of every conjunct on v541's additive
core-peck path, against the SHIPPED bytes of bots/_v542wave (= v177).

METHOD (declared, per the commission): UNIT-LEVEL drive of the shipped
predicate functions with a mocked Controller.  No engine game is played.  The
functions under test are imported from the shipped modules unmodified; the only
mutation is to module-level FLAG CONSTANTS, and that mutation IS the treatment
in the "must allow" cells (it is what a fix would change).

A clause is only reported as TESTED when the SAME shipped function returns both
True and False under two states differing in that clause alone.
"""
import os
import sys

BOT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "bots", "_v542wave")
BOT = os.path.normpath(BOT)
sys.path.insert(0, BOT)

from fcode import EntityType, Position          # noqa: E402
import doctrine                                  # noqa: E402
import siege                                     # noqa: E402
from siege import SiegeMixin                     # noqa: E402

TEAM = "A"
ENEMY_CORE = Position(20, 20)          # footprint (20,20),(21,20),(20,21),(21,21)
ADJ = Position(19, 20)                 # orthogonally adjacent to (20,20)
FAR = Position(5, 5)                   # not adjacent to anything


class Ctl:
    """Mock Controller.  Every getter is a plain attribute so a cell can set
    exactly one input and leave the rest at the permissive default."""

    def __init__(self, **kw):
        self.round = 100
        self.move_cd = 0
        self.action_cd = 0
        self.ammo = 10_000            # permissive: magazine "full"
        self.ti = 10_000              # permissive: bank enormous
        self.barrier_cost = 3
        self.sentinel_cost = 30
        self.buildings = {}           # bid -> (etype, team, pos)
        self.tile_bid = {}            # (x,y) -> bid
        self.hp = {}                  # bid -> hp
        self.store = {}
        self.can_fire_ok = True
        self.fired = []
        self.raise_on = set()         # names of getters that should raise
        self.__dict__.update(kw)

    def _chk(self, name):
        if name in self.raise_on:
            raise RuntimeError("probe-forced failure in " + name)

    # --- info -----------------------------------------------------------
    def get_id(self):
        return 7

    def get_current_round(self):
        self._chk("get_current_round")
        return self.round

    def get_move_cooldown(self):
        self._chk("get_move_cooldown")
        return self.move_cd

    def get_action_cooldown(self):
        self._chk("get_action_cooldown")
        return self.action_cd

    def get_global_ammo(self):
        self._chk("get_global_ammo")
        return self.ammo

    def get_global_resources(self):
        self._chk("get_global_resources")
        return self.ti

    def get_barrier_cost(self):
        return self.barrier_cost

    def get_sentinel_cost(self):
        return self.sentinel_cost

    def get_nearby_buildings(self, dist_sq=None):
        self._chk("get_nearby_buildings")
        return list(self.buildings)

    def get_entity_type(self, bid=None):
        return self.buildings[bid][0]

    def get_team(self, bid=None):
        return self.buildings[bid][1]

    def get_position(self, bid=None):
        return self.buildings[bid][2]

    def get_tile_building_id(self, pos):
        self._chk("get_tile_building_id")
        return self.tile_bid.get((pos.x, pos.y))

    def get_hp(self, bid=None):
        self._chk("get_hp")
        return self.hp[bid]

    def read_store(self, i):
        return self.store.get(i, 0)

    def is_tile_passable(self, pos):
        return True

    # --- act ------------------------------------------------------------
    def can_fire(self, tgt):
        self._chk("can_fire")
        return self.can_fire_ok

    def fire(self, tgt):
        self.fired.append((tgt.x, tgt.y))


class Body(SiegeMixin):
    """Minimal chassis carrying only the per-body state the v541 path reads."""

    def __init__(self, station=None):
        self.team = TEAM
        self.mw = 40
        self.mh = 40
        self.v541_pecks = 0
        self.v541_st_rnd = -1
        self.v541_st = None
        self.fs_blocked_now = set()
        self.fs_supp_seat = None
        self._station = station        # oracle for _fs_stand_target
        self.stand_calls = 0

    # `_fs_stand_target` is the INPUT ORACLE of `_v541_idle_ok`, not part of
    # the clause under test.  Stubbed so the idle predicate's three documented
    # branches can be addressed directly.  Declared in the readout.
    def _fs_stand_target(self, ct, E, p, needed):
        self.stand_calls += 1
        if self._station == "RAISE":
            raise RuntimeError("probe-forced stand_target failure")
        return self._station


def core_with_hp(hp):
    """A Ctl whose enemy core tile (20,20) reads `hp`."""
    c = Ctl()
    c.buildings[99] = (EntityType.CORE, "B", ENEMY_CORE)
    c.tile_bid[(20, 20)] = 99
    c.hp[99] = hp
    return c


def add_sentinel(c, n=1, team=TEAM, pos=Position(22, 22)):
    for k in range(n):
        bid = 200 + k
        c.buildings[bid] = (EntityType.SENTINEL, team, pos)
    return c


RESULTS = []


def cell(name, expect, fn):
    got = fn()
    ok = (bool(got) == expect)
    RESULTS.append((name, expect, bool(got), ok))
    print("%-58s expect=%-5s got=%-5s %s"
          % (name, expect, bool(got), "OK" if ok else "**MISMATCH**"))
    return got


def hdr(t):
    print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)


# =====================================================================
def main():
    print("shipped flag values read off the SHIPPED module namespace:")
    for f in ("FS_V541_COREPECK", "FS_V541_COREFIRST", "FS_V541_IDLEPECK",
              "FS_V541_FINISH_ON", "FS_V541_FINISH_HP", "FS_V541_TI_FLOOR",
              "FS_V541_KEEP_SENT", "FS_V541_AMMO_AWARE", "FS_V541_AMMO_MIN",
              "FS_V541_MAX_PECKS", "FS_V541_RAID_ON", "FS_V541_NEED_SENTINEL",
              "FS_SEAL_MARGIN"):
        print("   %-24s = %r   (siege ns)  %r (doctrine ns)"
              % (f, getattr(siege, f), getattr(doctrine, f)))

    # -----------------------------------------------------------------
    hdr("C0  THE MASTER GATE  siege.py:4567  `FS_V541_COREPECK and "
        "FS_V541_IDLEPECK`")
    # MUST REFUSE: shipped configuration, EVERY other clause satisfied.
    c = add_sentinel(core_with_hp(30))      # finishable, sentinel alive
    c.ammo = 10_000                         # ammo clause satisfied
    c.ti = 10_000                           # reserve satisfied
    b = Body()
    cell("C0.refuse  shipped IDLEPECK=False, all else satisfied", False,
         lambda: b._v541_core_attack(c, ENEMY_CORE, ADJ, []))
    assert c.fired == [], c.fired

    # MUST ALLOW: identical state, IDLEPECK flipped True.
    siege.FS_V541_IDLEPECK = True
    c2 = add_sentinel(core_with_hp(30))
    b2 = Body()
    cell("C0.allow   IDLEPECK=True, same state", True,
         lambda: b2._v541_core_attack(c2, ENEMY_CORE, ADJ, []))
    print("   fired:", c2.fired)

    # ---- with the master gate open, every downstream clause is drivable ----
    hdr("C1  TARGET  `_v541_core_target`  siege.py:4395  (orthogonal adjacency)")
    c = add_sentinel(core_with_hp(30))
    b = Body()
    cell("C1.refuse  body NOT orthogonally adjacent (5,5)", False,
         lambda: b._v541_core_attack(c, ENEMY_CORE, FAR, []))
    c = add_sentinel(core_with_hp(30))
    b = Body()
    cell("C1.refuse  body DIAGONAL to footprint (19,19)", False,
         lambda: b._v541_core_attack(c, ENEMY_CORE, Position(19, 19), []))
    c = add_sentinel(core_with_hp(30))
    b = Body()
    cell("C1.allow   body orthogonally adjacent (19,20)", True,
         lambda: b._v541_core_attack(c, ENEMY_CORE, ADJ, []))

    hdr("C2  `FS_V541_NEED_SENTINEL`  siege.py:4572  (ships False)")
    c = core_with_hp(30)                      # NO sentinel of ours
    b = Body()
    cell("C2.allow   NEED_SENTINEL=False, zero live sentinels", True,
         lambda: b._v541_core_attack(c, ENEMY_CORE, ADJ, []))
    siege.FS_V541_NEED_SENTINEL = True
    c = core_with_hp(30)
    b = Body()
    cell("C2.refuse  NEED_SENTINEL=True, zero live sentinels", False,
         lambda: b._v541_core_attack(c, ENEMY_CORE, ADJ, []))
    c = add_sentinel(core_with_hp(30))
    b = Body()
    cell("C2.allow   NEED_SENTINEL=True, one live sentinel", True,
         lambda: b._v541_core_attack(c, ENEMY_CORE, ADJ, []))
    siege.FS_V541_NEED_SENTINEL = False

    hdr("C3  THE AMMUNITION CLAUSE  siege.py:4360-4361  "
        "`AMMO_AWARE and live>0 and ammo < AMMO_MIN`")
    # refuse: live sentinel AND magazine below 120
    c = add_sentinel(core_with_hp(30)); c.ammo = 119
    b = Body()
    cell("C3.refuse  live sentinel, ammo=119 (< AMMO_MIN=120)", False,
         lambda: b._v541_core_attack(c, ENEMY_CORE, ADJ, []))
    # allow (a): NO live sentinel -> clause inert even at ammo 0
    c = core_with_hp(30); c.ammo = 0
    b = Body()
    cell("C3.allow   NO live sentinel, ammo=0 (branch (a))", True,
         lambda: b._v541_core_attack(c, ENEMY_CORE, ADJ, []))
    # allow (b): magazine full
    c = add_sentinel(core_with_hp(30)); c.ammo = 120
    b = Body()
    cell("C3.allow   live sentinel, ammo=120 (branch (b), boundary)", True,
         lambda: b._v541_core_attack(c, ENEMY_CORE, ADJ, []))
    # flag off reproduces the first build
    siege.FS_V541_AMMO_AWARE = False
    c = add_sentinel(core_with_hp(30)); c.ammo = 0
    b = Body()
    cell("C3.allow   AMMO_AWARE=False, live sentinel, ammo=0", True,
         lambda: b._v541_core_attack(c, ENEMY_CORE, ADJ, []))
    siege.FS_V541_AMMO_AWARE = True

    hdr("C4  THE BUILD RESERVE  siege.py:4385-4391  "
        "`ti >= len(needed)*barrier + FS_SEAL_MARGIN + FS_V541_TI_FLOOR "
        "(+ sentinel if KEEP_SENT and none live)`")
    # no sentinel alive -> reserve = 0*3 + 6 + 8 + 30 = 44
    for ti, exp in ((43, False), (44, True)):
        c = core_with_hp(30); c.ti = ti; c.ammo = 0
        b = Body()
        cell("C4.%s  needed=[] KEEP_SENT & none live, ti=%d (reserve 44)"
             % ("refuse" if not exp else "allow ", ti), exp,
             lambda c=c, b=b: b._v541_core_attack(c, ENEMY_CORE, ADJ, []))
    # sentinel alive -> reserve = 6 + 8 = 14
    for ti, exp in ((13, False), (14, True)):
        c = add_sentinel(core_with_hp(30)); c.ti = ti; c.ammo = 10_000
        b = Body()
        cell("C4.%s  needed=[] sentinel live, ti=%d (reserve 14)"
             % ("refuse" if not exp else "allow ", ti), exp,
             lambda c=c, b=b: b._v541_core_attack(c, ENEMY_CORE, ADJ, []))
    # TI_FLOOR alone, held at the boundary
    siege.FS_V541_TI_FLOOR = 9
    c = add_sentinel(core_with_hp(30)); c.ti = 14
    b = Body()
    cell("C4.refuse  TI_FLOOR 8->9 with ti=14 (reserve now 15)", False,
         lambda: b._v541_core_attack(c, ENEMY_CORE, ADJ, []))
    siege.FS_V541_TI_FLOOR = 8
    # collar term: needed of length 3
    c = add_sentinel(core_with_hp(30)); c.ti = 22
    b = Body()
    cell("C4.refuse  needed=3 barriers, ti=22 (reserve 3*3+6+8=23)", False,
         lambda: b._v541_core_attack(c, ENEMY_CORE, ADJ,
                                     [ADJ, ADJ, ADJ]))
    c = add_sentinel(core_with_hp(30)); c.ti = 23
    b = Body()
    cell("C4.allow   needed=3 barriers, ti=23", True,
         lambda: b._v541_core_attack(c, ENEMY_CORE, ADJ,
                                     [ADJ, ADJ, ADJ]))
    # KEEP_SENT off removes the 30 Ti term
    siege.FS_V541_KEEP_SENT = False
    c = core_with_hp(30); c.ti = 14; c.ammo = 0
    b = Body()
    cell("C4.allow   KEEP_SENT=False, none live, ti=14", True,
         lambda: b._v541_core_attack(c, ENEMY_CORE, ADJ, []))
    siege.FS_V541_KEEP_SENT = True

    hdr("C5  THE PECK BUDGET / FIRE GATE  siege.py:4408-4418")
    c = add_sentinel(core_with_hp(30))
    b = Body(); b.v541_pecks = siege.FS_V541_MAX_PECKS
    cell("C5.refuse  v541_pecks == MAX_PECKS (60)", False,
         lambda: b._v541_core_attack(c, ENEMY_CORE, ADJ, []))
    c = add_sentinel(core_with_hp(30))
    b = Body(); b.v541_pecks = siege.FS_V541_MAX_PECKS - 1
    cell("C5.allow   v541_pecks == 59", True,
         lambda: b._v541_core_attack(c, ENEMY_CORE, ADJ, []))
    c = add_sentinel(core_with_hp(30)); c.action_cd = 1
    b = Body()
    cell("C5.refuse  action cooldown = 1", False,
         lambda: b._v541_core_attack(c, ENEMY_CORE, ADJ, []))
    c = add_sentinel(core_with_hp(30)); c.can_fire_ok = False
    b = Body()
    cell("C5.refuse  ct.can_fire() False", False,
         lambda: b._v541_core_attack(c, ENEMY_CORE, ADJ, []))

    # restore the shipped value before the idle/redirect sections
    siege.FS_V541_IDLEPECK = False

    hdr("C6  THE IDLE PREDICATE  `_v541_idle_ok`  siege.py:4265  "
        "(call-site conjunct at :3711 / :3786)")
    c = Ctl(); c.move_cd = 1
    b = Body(station=Position(1, 1))
    cell("C6.allow   move cooldown != 0 (round free by construction)", True,
         lambda: b._v541_idle_ok(c, ENEMY_CORE, ADJ, []))
    c = Ctl()
    b = Body(station=None)
    cell("C6.allow   no station (st is None)", True,
         lambda: b._v541_idle_ok(c, ENEMY_CORE, ADJ, []))
    c = Ctl()
    b = Body(station=ADJ)
    cell("C6.allow   already standing on its station", True,
         lambda: b._v541_idle_ok(c, ENEMY_CORE, ADJ, []))
    c = Ctl()
    b = Body(station=Position(1, 1))
    cell("C6.refuse  station elsewhere -> parent would WALK", False,
         lambda: b._v541_idle_ok(c, ENEMY_CORE, ADJ, []))
    c = Ctl(); c.raise_on = {"get_move_cooldown"}
    b = Body(station=None)
    cell("C6.refuse  get_move_cooldown raises -> fails CLOSED", False,
         lambda: b._v541_idle_ok(c, ENEMY_CORE, ADJ, []))
    c = Ctl()
    b = Body(station="RAISE")
    cell("C6.refuse  _fs_stand_target raises -> fails CLOSED", False,
         lambda: b._v541_idle_ok(c, ENEMY_CORE, ADJ, []))

    hdr("C7  THE CALL SITE IS AN `and` -- does C6's verdict reach anything?")
    # Reproduce the exact conjunct of siege.py:3711 in the SHIPPED config.
    c = add_sentinel(core_with_hp(30))
    b = Body(station=ADJ)               # idle_ok True
    site = (siege.FS_V541_COREPECK
            and b._v541_idle_ok(c, ENEMY_CORE, ADJ, [])
            and b._v541_core_attack(c, ENEMY_CORE, ADJ, []))
    cell("C7  siege.py:3711 conjunct, idle_ok=True, shipped flags", False,
         lambda: site)
    print("   -> idle_ok returned True and the rung STILL did not fire: "
          "the idle predicate is NOT the binding term.")

    hdr("C8  THE REDIRECT HALF  `_v541_corefirst` / `_v541_finishable`  "
        "siege.py:4429 / :4479")
    for hp, exp in ((500, False), (121, False), (120, True), (30, True)):
        c = add_sentinel(core_with_hp(hp)); c.ti = 10_000
        b = Body()
        cell("C8.%s  enemy core HP=%d (FINISH_HP=120)"
             % ("allow " if exp else "refuse", hp), exp,
             lambda c=c, b=b: b._v541_corefirst(c, ENEMY_CORE, ADJ))
    # budget arm: 55 pecks spent -> budget = 2*(60-55) = 10
    c = add_sentinel(core_with_hp(12)); b = Body(); b.v541_pecks = 55
    cell("C8.refuse  HP=12 but budget=10 (55 pecks spent)", False,
         lambda: b._v541_corefirst(c, ENEMY_CORE, ADJ))
    c = add_sentinel(core_with_hp(10)); b = Body(); b.v541_pecks = 55
    cell("C8.allow   HP=10, budget=10", True,
         lambda: b._v541_corefirst(c, ENEMY_CORE, ADJ))
    # unreadable core fails CLOSED
    c = add_sentinel(core_with_hp(30)); c.raise_on = {"get_hp"}
    b = Body()
    cell("C8.refuse  get_hp raises -> fails CLOSED", False,
         lambda: b._v541_corefirst(c, ENEMY_CORE, ADJ))
    # FINISH_ON off -> unconditional redirect (the refuted form)
    siege.FS_V541_FINISH_ON = False
    c = add_sentinel(core_with_hp(500)); b = Body()
    cell("C8.allow   FINISH_ON=False, HP=500 (the REFUTED unconditional form)",
         True, lambda: b._v541_corefirst(c, ENEMY_CORE, ADJ))
    siege.FS_V541_FINISH_ON = True

    hdr("SUMMARY")
    bad = [r for r in RESULTS if not r[3]]
    print("cells: %d   mismatches: %d" % (len(RESULTS), len(bad)))
    for r in bad:
        print("  MISMATCH", r)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
