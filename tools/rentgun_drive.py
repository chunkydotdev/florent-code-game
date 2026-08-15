"""SCENARIO DRIVE for LOKI-RENTGUN (bots/_v313rentgun) on the stub engine.

WHY A STUB AND NOT ONLY `fcode run`.  The local match proves the sequence fires
end to end (19 opens / 16 returns / 0 stranded over six maps), but it cannot
CONSTRUCT the cases that matter most: an empty ammo pool, a raider boxed in on
three sides, a raider teleported away from its own live turret.  Those are the
paths where the plank either loses 30 Ti quietly or holds a permanent +20%, and
a fixture that never reaches them has not tested them.

Every check below is a PAIR wherever a pair is meaningful -- the same scenario
driven to the opposite verdict -- because a guard that has only ever returned
one answer has not been seen to guard.  Run:

    .venv/bin/python tools/rentgun_drive.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BOT = os.path.join(ROOT, "bots", "_v313rentgun")

sys.path.insert(0, HERE)
from stub_engine import (  # noqa: E402
    Direction, EntityType, Environment, GameError, Position, StubController,
    Team, World, run_bot,
)

# The bot imports `fcode`; the stub provides the same names.  Install it under
# that module name BEFORE the bot package is imported.
import types  # noqa: E402
import stub_engine  # noqa: E402

fake = types.ModuleType("fcode")
for _n in ("Direction", "EntityType", "Environment", "GameError", "Position",
           "Team", "ResourceType", "GameConstants", "Controller"):
    if hasattr(stub_engine, _n):
        setattr(fake, _n, getattr(stub_engine, _n))
if not hasattr(fake, "Controller"):
    fake.Controller = stub_engine.StubController
sys.modules["fcode"] = fake
sys.path.insert(0, BOT)

import doctrine  # noqa: E402
import raid  # noqa: E402  (imported for side effects / mixin availability)
from main import Player  # noqa: E402

# ---- `--help` CONTRACT (enforced by tests/test_instruments.py) --------------
# Side-effect-free, prints this module's docstring, exits 0.
#
# ⛔ WHY. Probing an unknown tool with `--help` is the first thing anyone does.
# Before 2026-08-15, 40 of 86 tools here had no argparse, so `--help` was just an
# unrecognised argument and THE TOOL RAN FOR REAL -- printing VERDICT-SHAPED text
# that reads as a finding:
#     tools/freshness.py --help  ->  "BLIND: --help has no parseable timestamp"
#     tools/leg_read.py  --help  ->  "LEG: no completed games"
# Both are this repo's own verdict vocabulary. A reader asking a harmless
# question got an authoritative-looking sentence about nothing.
#
# ⛔ GATED ON `__main__`: several of these modules are IMPORTED by other tools
# (freshness by now.py). Ungated, this would fire during that import and make the
# PARENT exit 0 mid-run while printing the CHILD's docstring.
# ⛔ SELF-CONTAINED `import sys`: a first attempt used the file's own import, and
# broke on `import sys as _sys` (NameError) and on files whose imports come in
# two blocks. The guard must not depend on what the host file happens to import.
if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__ + "  (no module docstring)"))
        raise SystemExit(0)

PASS, FAIL = [], []


def check(name, got, want):
    ok = got == want
    (PASS if ok else FAIL).append(name)
    print(("  ok   " if ok else "  FAIL ") + "%-58s got=%r want=%r" % (name, got, want))
    return ok


def board(w=16, h=16):
    """A world with our core west, theirs east, and an ore tile between."""
    world = World(w, h)
    world.add(EntityType.CORE, Team.A, Position(2, 8))
    world.add(EntityType.CORE, Team.B, Position(13, 8))
    return world


def raider(world, pos, slot=0):
    """A live builder bot of ours, already initialised as a raider."""
    bid = world.add(EntityType.BUILDER_BOT, Team.A, pos)
    pl = Player()
    pl.team = Team.A
    pl.mw, pl.mh = world.width, world.height
    pl.core = Position(2, 8)
    pl.enemy = Position(13, 8)
    pl.role = "raid"
    pl.raid_slot = slot
    pl.map_ores = []
    return bid, pl


def ct_for(world, eid):
    return StubController(world, eid)


# ---------------------------------------------------------------------------
print("\n1. TURRET IS BUILT IN RANGE OF THE HARVESTER, FROM AN ADJACENT TILE")
w = board()
w.set_terrain(Position(9, 8), Environment.ORE_TITANIUM)
hid = w.add(EntityType.HARVESTER, Team.B, Position(9, 8))
bid, pl = raider(w, Position(8, 8))
w.titanium[Team.A] = 500
w.ammo[Team.A] = 40
ct = ct_for(w, bid)
spent = pl._rent_turn(ct, Position(13, 8), False)
check("rent_turn consumed the turn", spent, True)
check("a sentinel was planted", pl.rent_turret is not None, True)
tp = pl.rent_turret_pos
check("turret is orthogonally adjacent to the raider",
      abs(tp.x - 8) + abs(tp.y - 8) == 1, True)
check("harvester lies on the planted sentinel's ray",
      ct.can_fire_from(tp, w.entities[pl.rent_turret]["direction"],
                       EntityType.SENTINEL, Position(9, 8)), True)
check("rent_ore is the ore tile itself", (pl.rent_ore.x, pl.rent_ore.y), (9, 8))

# ---------------------------------------------------------------------------
print("\n2. AMMO GATE -- the pair: 20 builds, 19 refuses")
for ammo, want in ((20, True), (19, False)):
    w = board()
    w.set_terrain(Position(9, 8), Environment.ORE_TITANIUM)
    w.add(EntityType.HARVESTER, Team.B, Position(9, 8))
    bid, pl = raider(w, Position(8, 8))
    w.titanium[Team.A] = 500
    w.ammo[Team.A] = ammo
    pl._rent_turn(ct_for(w, bid), Position(13, 8), False)
    check("ammo=%d -> turret planted" % ammo, pl.rent_turret is not None, want)

# ---------------------------------------------------------------------------
print("\n3. FULL SEQUENCE: harvester dies -> ore barriered -> turret destroyed")
w = board()
w.set_terrain(Position(9, 8), Environment.ORE_TITANIUM)
hid = w.add(EntityType.HARVESTER, Team.B, Position(9, 8))
bid, pl = raider(w, Position(8, 8))
w.titanium[Team.A] = 500
w.ammo[Team.A] = 60
ct = ct_for(w, bid)
pl._rent_turn(ct, Position(13, 8), False)
turret_id, turret_pos = pl.rent_turret, pl.rent_turret_pos
scale_with_turret = w.scale_pct[Team.A]
turret_pl = Player()
for rnd in range(12):
    w.end_round()
    if turret_id in w.entities:                    # let the turret shoot
        run_bot(w, turret_pl, turret_id)
    if hid not in w.entities:
        break
    pl._rent_turn(ct_for(w, bid), Position(13, 8), False)
check("harvester was killed by the rented sentinel", hid not in w.entities, True)
rounds_to_kill = rnd
w.end_round()
pl._rent_turn(ct_for(w, bid), Position(13, 8), False)
bar = w.building_at(Position(9, 8))
check("ore tile now holds one of OUR barriers",
      bar is not None and w.entities[bar]["type"] == EntityType.BARRIER
      and w.entities[bar]["team"] == Team.A, True)
check("the rented turret was destroyed", turret_id not in w.entities, True)
check("scale fell back below the with-turret reading",
      w.scale_pct[Team.A] < scale_with_turret, True)
check("rental state was cleared", pl.rent_turret_pos, None)
check("hop memory recorded the finished ore", (9, 8) in pl.rent_seen, True)
print("     (kill took %d stub rounds; live matches close at age 4)" % rounds_to_kill)

# ---------------------------------------------------------------------------
print("\n4. ESCAPE GUARD -- the pair: boxed-in raider vetoes, open raider allows")
for walls, want in ((((7, 8), (8, 7), (8, 9)), False), (((7, 8),), True)):
    w = board()
    for (x, y) in walls:
        w.set_terrain(Position(x, y), Environment.WALL)
    bid, pl = raider(w, Position(8, 8))
    ct = ct_for(w, bid)
    got = pl._rent_escapes(ct, Position(8, 8), Position(9, 8))
    check("walls=%d -> build on (9,8) allowed" % len(walls), got, want)

# ---------------------------------------------------------------------------
print("\n5. FRIENDLY GUNNER RAY -- the pair (this guard was a constant False once)")
w = board()
w.add(EntityType.GUNNER, Team.A, Position(6, 8), Direction.EAST)
bid, pl = raider(w, Position(8, 8))
ct = ct_for(w, bid)
check("tile ON our gunner's ray is vetoed", pl._friendly_gun_ray(ct, Position(9, 8)), True)
check("tile OFF our gunner's ray is allowed", pl._friendly_gun_ray(ct, Position(9, 9)), False)

# ---------------------------------------------------------------------------
print("\n6a. DISPLACED BUT RECOVERABLE -- the raider walks back and returns the rent")
w = board()
w.set_terrain(Position(9, 8), Environment.ORE_TITANIUM)
hid = w.add(EntityType.HARVESTER, Team.B, Position(9, 8))
bid, pl = raider(w, Position(8, 8))
w.titanium[Team.A] = 500
w.ammo[Team.A] = 60
pl._rent_turn(ct_for(w, bid), Position(13, 8), False)
turret_id = pl.rent_turret
w.entities[bid]["pos"] = Position(2, 2)          # a launcher threw us home
walked = 0
for _ in range(doctrine.LOKI_RENT_HOLD_MAX + doctrine.LOKI_RENT_RECOVER_MAX + 4):
    w.end_round()
    before = w.entities[bid]["pos"]
    pl._rent_turn(ct_for(w, bid), Position(13, 8), False)
    if w.entities[bid]["pos"] != before:
        walked += 1
    if pl.rent_turret_pos is None:
        break
check("displaced raider tried to walk back", walked > 0, True)
check("state was released, not held for the match", pl.rent_turret_pos, None)
# It got back inside the clock, so this is the RECOVERY leg, not the strand.
check("the rent was actually recovered (turret gone)", turret_id not in w.entities, True)
check("recovery is accounted, not silent", pl.rent_done, 1)

# ---------------------------------------------------------------------------
print("\n6b. UNRECOVERABLE -- thrown too far to return; the strand must be COUNTED")
w = board(30, 30)
w.set_terrain(Position(9, 8), Environment.ORE_TITANIUM)
hid = w.add(EntityType.HARVESTER, Team.B, Position(9, 8))
bid, pl = raider(w, Position(8, 8))
pl.mw, pl.mh = 30, 30
w.titanium[Team.A] = 500
w.ammo[Team.A] = 60
pl._rent_turn(ct_for(w, bid), Position(13, 8), False)
turret_id = pl.rent_turret
w.entities[bid]["pos"] = Position(29, 29)        # far corner, cannot get back
for _ in range(doctrine.LOKI_RENT_HOLD_MAX + doctrine.LOKI_RENT_RECOVER_MAX + 4):
    w.end_round()
    pl._rent_turn(ct_for(w, bid), Position(13, 8), False)
    if pl.rent_turret_pos is None:
        break
check("the strand was COUNTED, not silent", pl.rent_stranded, 1)
check("the body was released rather than orbiting rubble", pl.rent_turret_pos, None)
check("the ore was still retired so the raider HOPS", (9, 8) in pl.rent_seen, True)

# ---------------------------------------------------------------------------
print("\n7. AIMED KEEP -- a core-aligned sentinel is NOT handed back")
w = board(20, 20)
w.set_terrain(Position(10, 10), Environment.ORE_TITANIUM)
hid = w.add(EntityType.HARVESTER, Team.B, Position(10, 10))
E = Position(12, 10)                              # enemy core beyond the ore
w.entities[[i for i, e in w.entities.items() if e["type"] == EntityType.CORE
            and e["team"] == Team.B][0]]["pos"] = E
bid, pl = raider(w, Position(9, 10))
pl.enemy = E
w.titanium[Team.A] = 500
w.ammo[Team.A] = 60
pl._rent_turn(ct_for(w, bid), E, False)
check("an aligned site was recognised as a KEEPER", pl.rent_keep, True)
keep_id = pl.rent_turret
turret_pl = Player()
for _ in range(14):
    w.end_round()
    if keep_id in w.entities:
        run_bot(w, turret_pl, keep_id)
    pl._rent_turn(ct_for(w, bid), E, False)
    if pl.rent_turret_pos is None:
        break
check("the keeper survived the close", keep_id in w.entities, True)
check("its harvester WAS killed first (LOKI_RENT_HARV_FIRST)", hid not in w.entities, True)
check("the freed ore was salted", pl.rent_walled or (10, 10) in pl.rent_seen, True)
check("rental state was still cleared so the raider hops", pl.rent_turret_pos, None)

# ---------------------------------------------------------------------------
print("\n8. TOGGLE OFF -- the plank is inert")
doctrine.LOKI_RENTGUN_ON = False
raid.LOKI_RENTGUN_ON = False
w = board()
w.set_terrain(Position(9, 8), Environment.ORE_TITANIUM)
w.add(EntityType.HARVESTER, Team.B, Position(9, 8))
bid, pl = raider(w, Position(8, 8))
w.titanium[Team.A] = 500
w.ammo[Team.A] = 60
check("_rent_turn is a no-op with the toggle off",
      pl._rent_turn(ct_for(w, bid), Position(13, 8), False), False)
check("nothing was built", pl.rent_turret, None)
doctrine.LOKI_RENTGUN_ON = True
raid.LOKI_RENTGUN_ON = True

# ---------------------------------------------------------------------------
print("\n%d passed, %d failed" % (len(PASS), len(FAIL)))
if FAIL:
    print("FAILED: " + ", ".join(FAIL))
    sys.exit(1)
print("RENTGUN DRIVE OK")
