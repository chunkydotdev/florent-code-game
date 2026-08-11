"""LOKI-29 seat-relative scan order -- the fixture, driven to BOTH verdicts.

WHY THIS FILE EXISTS AND WHY IT IS SHAPED LIKE THIS.  s31's one load-bearing
finding was five guards that could not fire, four of them written while their
author was explicitly hunting for that defect.  The rule that came out of it:
A GUARD IS NOT DONE WHEN IT PASSES, IT IS DONE WHEN IT HAS BEEN DRIVEN TO THE
ANSWER IT IS SUPPOSED TO REFUSE.  So every check below runs TWICE -- once on the
treatment (SEAT_RELATIVE_SCAN = True) where it must PASS, and once on the
control (the shipped absolute order) where the canonicalisation check MUST FAIL.
A cell that has never come out the other way has not been seen to check.

WHAT IS ACTUALLY BEING ASSERTED, in the order that matters:

  1. CANONICALISATION.  The two seats' scan orders are point reflections of each
     other, so both seats execute the same scan in their own frame.  This is the
     whole plank; if it does not hold the arm tests nothing.
     NEGATIVE CELL: the shipped absolute [N,E,S,W] must FAIL this.

  2. THE CLOCKWISE 4-CYCLE SURVIVES.  eco.py:588-590, :703-711 and :743-744 read
     CARDINALS[(i+1)%4] and CARDINALS[(i-1)%4] as "the two PERPENDICULARS of
     desired".  That is only true while the list is a rotational cycle.  This is
     the check that catches a reorder that looks fine and silently turns
     "perpendicular" into "opposite" at three live sites.

  3. IDEMPOTENCE.  orient_cardinals runs on EVERY Core turn, ~1000 times a game.

  4. IT IS A PERMUTATION.  A rotation that dropped or duplicated a direction
     would starve some scans and double-scan others; cheap to assert, and it is
     the failure a hand-written rotation actually makes.

RUN: .venv/bin/python tests/test_seat_relative.py
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TREE = os.path.join(ROOT, "bots", "_v151seatrel")
sys.path.insert(0, TREE)

from fcode import Direction, Position  # noqa: E402

import doctrine  # noqa: E402

BASE = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)
OPPOSITE = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST,
}

# The 8 maps in the local battery (tools/overnight.sh:50, tools/h2h.sh:50) with
# the dimensions `fcode maps list` reports, plus archipelago/saga/snowflake from
# the wider pool.  Core anchors are the point reflections of a plausible seat-A
# anchor -- the CANONICALISATION property is a statement about the two seats'
# relative geometry, so it holds for ANY anchor pair related by point
# reflection.  (Whether our TABLE of anchors is right is a separate question,
# audited separately; this fixture must not depend on that answer.)
MAPS = [
    ("antler", 14, 18, 2, 2),
    ("atoll", 18, 18, 2, 14),
    ("drumlin", 25, 25, 2, 20),
    ("fjordgate", 10, 10, 1, 1),
    ("heart", 28, 20, 7, 9),
    ("hive", 25, 25, 2, 20),
    ("meander", 25, 15, 11, 3),
    ("nordkap", 20, 26, 9, 6),
    ("archipelago", 26, 26, 5, 5),
    ("saga", 24, 24, 2, 19),
    ("snowflake", 26, 26, 3, 22),
]

FAILS = []


def check(name, got, want, forced_by):
    ok = got == want
    print(f"  [{'ok' if ok else 'FAIL'}] {name:<52} got={got} want={want}")
    if not ok:
        print(f"         forced by: {forced_by}")
        FAILS.append(name)
    return ok


def order_for(core, enemy):
    """The CARDINALS the bot would scan with, from this seat."""
    doctrine.orient_cardinals(core, enemy)
    return list(doctrine.CARDINALS)


def reflect(order):
    """Point-reflect a scan order: N<->S, E<->W, positions unchanged."""
    return [OPPOSITE[d] for d in order]


def is_cycle(order):
    """True iff `order` is a rotation of N,E,S,W in either handedness.

    This is the property eco.py's (i+1)%4 / (i-1)%4 arithmetic depends on:
    every neighbour in the list must be a 90-degree turn, never a 180.
    """
    if sorted(order, key=lambda d: d.name) != sorted(BASE, key=lambda d: d.name):
        return False
    fwd = [BASE[(BASE.index(order[0]) + k) % 4] for k in range(4)]
    rev = [BASE[(BASE.index(order[0]) - k) % 4] for k in range(4)]
    return order == fwd or order == rev


def run_pass(label, seat_relative):
    """Run every check under one setting of the flag.

    Returns the number of maps whose two seats canonicalise.  The TREATMENT pass
    must return len(MAPS); the CONTROL pass must return 0 -- that zero is what
    makes the treatment's result mean something.
    """
    print(f"\n--- {label} (SEAT_RELATIVE_SCAN = {seat_relative}) ---")
    doctrine.SEAT_RELATIVE_SCAN = seat_relative
    doctrine.CARDINALS[:] = list(BASE)

    canonical = 0
    for name, w, h, ax, ay in MAPS:
        a = Position(ax, ay)
        b = Position(w - 2 - ax, h - 2 - ay)
        order_a = order_for(a, b)
        order_b = order_for(b, a)

        if reflect(order_b) == order_a:
            canonical += 1
        else:
            print(f"      {name:<12} A={order_a and [d.name for d in order_a]}")
            print(f"      {' ':<12} B={[d.name for d in order_b]} "
                  f"reflected={[d.name for d in reflect(order_b)]}  NOT CANONICAL")

        if not is_cycle(order_a) or not is_cycle(order_b):
            FAILS.append(f"{label}:{name}:cycle")
            print(f"      {name}: NOT A 4-CYCLE -- eco.py's (i+-1)%4 "
                  f"perpendicular arithmetic is broken by this order")

        if sorted(order_a, key=lambda d: d.name) != sorted(BASE, key=lambda d: d.name):
            FAILS.append(f"{label}:{name}:permutation")
            print(f"      {name}: order is not a permutation of the 4 cardinals")

    return canonical


print(__doc__.split("RUN:")[0].strip().splitlines()[0])
print()

# ---------------------------------------------------------------- TREATMENT
treat = run_pass("TREATMENT", True)
check("both seats canonicalise, all maps", treat, len(MAPS),
      "this IS the plank -- if the two seats do not execute the same scan in "
      "their own frame, the arm changes the bot without testing the hypothesis")

# The clockwise cycle, at every one of the four possible orientations.
doctrine.SEAT_RELATIVE_SCAN = True
cycles = 0
for first in BASE:
    doctrine.CARDINALS[:] = list(BASE)
    dx, dy = {Direction.NORTH: (0, -5), Direction.SOUTH: (0, 5),
              Direction.EAST: (5, 0), Direction.WEST: (-5, 0)}[first]
    got = order_for(Position(10, 10), Position(10 + dx, 10 + dy))
    if got[0] == first and is_cycle(got):
        cycles += 1
    else:
        print(f"      orientation {first.name}: got {[d.name for d in got]}")
check("all 4 orientations start at the enemy and stay a cycle", cycles, 4,
      "eco.py:588-590/:703-711/:743-744 take (i+-1)%4 as the two PERPENDICULARS "
      "of a direction; that is false the moment the list stops being a 4-cycle")

# Idempotence -- this runs on every Core turn, ~1000x per game.
doctrine.CARDINALS[:] = list(BASE)
once = order_for(Position(2, 2), Position(10, 14))
for _ in range(50):
    twice = order_for(Position(2, 2), Position(10, 14))
check("idempotent over 50 calls", twice, once,
      "orient_cardinals is called from _core every round; a non-idempotent "
      "rotation would walk the scan order around the compass mid-game")

# The tiebreak itself must be reflection-invariant, or the canonicalisation
# above holds only by accident on the anchors that happen to be in MAPS.
doctrine.CARDINALS[:] = list(BASE)
tie_a = order_for(Position(0, 0), Position(6, 6))
tie_b = order_for(Position(6, 6), Position(0, 0))
check("abs(dx)>=abs(dy) tiebreak is reflection-invariant", reflect(tie_b), tie_a,
      "a diagonal enemy is the case where the branch could differ by seat; if "
      "it does, the canonicalisation is anchor-dependent rather than general")

# ------------------------------------------------------------------ CONTROL
# The negative cell.  Without it, a check that passes on everything looks
# correct -- which is this repo's most-repeated defect.
ctrl = run_pass("CONTROL (shipped absolute order)", False)
check("shipped [N,E,S,W] canonicalises on ZERO maps", ctrl, 0,
      "THE NEGATIVE CELL. The absolute order reflects to [S,W,N,E], which is a "
      "different list, so seat A and seat B genuinely do execute different "
      "scans today. If this cell ever reads non-zero the check is vacuous and "
      "the TREATMENT result above means nothing")

doctrine.SEAT_RELATIVE_SCAN = True
doctrine.CARDINALS[:] = list(BASE)

print()
if FAILS:
    print(f"SEAT_RELATIVE_SELFTEST: FAIL ({len(FAILS)}) -> {FAILS}")
    sys.exit(1)
print("SEAT_RELATIVE_SELFTEST: PASS "
      f"({len(MAPS)}/{len(MAPS)} maps canonicalise under treatment, "
      "0 under the shipped order)")
