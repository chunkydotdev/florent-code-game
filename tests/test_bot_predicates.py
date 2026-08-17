#!/usr/bin/env python3
"""Unit tests for the LIVE bot's stateless predicates and geometric gates.

Run:  .venv/bin/python -m unittest discover -s tests -v
Point at another arm:  BOT=bots/_v230sent41 .venv/bin/python -m unittest discover -s tests

WHY THIS FILE EXISTS, and it is NOT "coverage".

`tests/test_bot_helpers.py` covers eleven pure helpers and argues -- correctly --
that stateful turn logic belongs to `tools/det.py`, not to a mock.  That argument
leaves a gap, and three defects fell through it on 2026-08-15, all the same
shape: **a predicate or geometric condition whose satisfying set is empty, or
whose answer is a constant.**

  1. `_v230sent41._try_fwd_barrier` needed a tile simultaneously cardinal-
     adjacent to the raider AND Manhattan-1 from the sentinel.  After a plant
     the raider is at `p` and the sentinel at `p+d`, so every OTHER neighbour of
     `p` is Manhattan-2 from it.  THE SATISFYING SET IS EMPTY.  That tree was
     banked as "dose-verified, cert-clean".
  2. A gunner-ray guard called `can_fire_from(gun, dir, GUNNER, tile)` on the
     tile about to be BUILT on.  A gunner's `can_fire_from` is False on every
     EMPTY tile and a build tile is empty by definition, so the guard could
     never veto.  CONSTANT FALSE.
  3. A keeper turret's target ranking put CORE at 0 and HARVESTER at 5, so the
     harvester it was sequenced to kill was never selected.

None of the three raises, none shows up in a diff review, and all three produce
a plausible replay.  `det.py` cannot see them either: a dead branch is dead in
both parent and child, so a 0-flip identity run is exactly what they produce.

So the standing repo rule -- *"a guard is done when it has been driven to the
answer it is supposed to refuse; a check that has never produced the other
verdict has not been seen to check"* -- is applied here to the BOT's own
predicates.  **Every test below drives BOTH verdicts.**  A cell that only ever
asserts True is the defect this file is looking for, not the test.

Companion: `test_predicate_liveness.py` sweeps a bounded input space per
predicate and flags anything constant across it.  This file asserts the
SPECIFIC facts; that one hunts for the general shape.
"""
import io
import os
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _botlab as L  # noqa: E402
from _botlab import manhattan  # noqa: E402
from fcode import (  # noqa: E402
    Direction, EntityType, Environment, GameConstants, Position, Team,
)

CARDINALS = L.CARDINALS
DIAGONALS = L.DIAGONALS
HAVE_BOT = (L.BOT_DIR / "main.py").exists()


def setUpModule():
    global BOT
    if HAVE_BOT:
        BOT = L.load_bot()


@unittest.skipUnless(HAVE_BOT, f"{L.BOT} not present")
class BotCase(unittest.TestCase):
    """Base: exposes the tree and the module-level helpers by name."""

    @classmethod
    def setUpClass(cls):
        cls.b = BOT
        cls.heal_seats = staticmethod(BOT.fn("heal_seats"))
        cls.core_corners = staticmethod(BOT.fn("core_corners"))
        cls.core_tiles = staticmethod(BOT.fn("core_tiles"))

    def seats(self, o, mw=20, mh=20):
        return self.b.fn("heal_seats")(o, mw, mh)

    def corners(self, o, mw=20, mh=20):
        return self.b.fn("core_corners")(o, mw, mh)

    def tiles(self, o):
        return self.b.fn("core_tiles")(o)


# ===========================================================================
# 1.  THE CORE RING -- against CORE_SPAWNING_RADIUS_SQ, not against the code
# ===========================================================================

class TestCoreRingAgainstGroundTruth(BotCase):
    """GT-3: the spawn envelope is EXACTLY 12 tiles at d^2 <= 2 from the 2x2.

    The tree derives that envelope in two halves -- `heal_seats` (8) and
    `core_corners` (4) -- and the ENTIRE raid doctrine is built on the halves
    having the properties their docstrings claim.  Both halves are re-derived
    here from the constant, not from the functions.
    """

    def test_seats_plus_corners_are_exactly_the_spawn_envelope(self):
        for o in (Position(8, 8), Position(3, 11), Position(14, 5)):
            got = {(p.x, p.y) for p in self.seats(o) + self.corners(o)}
            foot = {(t.x, t.y) for t in self.tiles(o)}
            want = {
                (t.x + dx, t.y + dy)
                for (t) in self.tiles(o)
                for dx in (-1, 0, 1) for dy in (-1, 0, 1)
            } - foot
            self.assertEqual(len(want), 12, "the independent derivation itself")
            self.assertEqual(
                got, want,
                f"seats+corners != the d^2<={GameConstants.CORE_SPAWNING_RADIUS_SQ} "
                f"spawn envelope at {o}",
            )

    def test_the_envelope_is_twelve_and_the_two_halves_are_disjoint(self):
        o = Position(8, 8)
        s = {(p.x, p.y) for p in self.seats(o)}
        c = {(p.x, p.y) for p in self.corners(o)}
        self.assertEqual(len(s), 8)
        self.assertEqual(len(c), 4)
        self.assertEqual(s & c, set(), "a tile is both a seat and a corner")
        self.assertEqual(len(s | c), GameConstants.CORE_SPAWNING_RADIUS_SQ * 6)

    def test_a_seat_is_a_peck_station_and_a_corner_is_never_one(self):
        """`core_corners.__doc__`: a corner is adjacent to no Core tile.

        This is the claim `raid.py` `_raid_act` step 1 depends on -- and it is
        exactly the shape of the `_try_fwd_barrier` defect, so it is checked
        rather than trusted.  BOTH verdicts: seats must be non-empty, corners
        must be empty.
        """
        o = Position(8, 8)
        for s in self.seats(o):
            n = sum(1 for c in self.tiles(o) if manhattan(s, c) == 1)
            self.assertEqual(
                n, 1, f"seat {s} is Manhattan-1 from {n} Core tiles, want 1 -- "
                      f"the seat peck in _raid_act step 1 would be unreachable")
        for c in self.corners(o):
            n = sum(1 for t in self.tiles(o) if manhattan(c, t) == 1)
            self.assertEqual(
                n, 0, f"corner {c} is Manhattan-1 from a Core tile -- "
                      f"core_corners.__doc__ says it never is")

    def test_a_corner_seals_exactly_two_seats_and_a_seat_seals_exactly_one(self):
        """`core_corners.__doc__`: 'it can seal two seats'.  Four corners, eight seats.

        `_raid_act` step 2 and `_open_seats_by` both walk CARDINALS from the
        station and keep what lands in `seatkeys`.  If that intersection were
        empty the whole collar would be a no-op -- the `_try_fwd_barrier` class.
        """
        o = Position(8, 8)
        keys = {(s.x, s.y) for s in self.seats(o)}
        for c in self.corners(o):
            n = sum(1 for d in CARDINALS if (c.add(d).x, c.add(d).y) in keys)
            self.assertEqual(n, 2, f"corner {c} flanks {n} seats, docstring says 2")
        for s in self.seats(o):
            n = sum(1 for d in CARDINALS if (s.add(d).x, s.add(d).y) in keys)
            self.assertEqual(n, 1, f"seat {s} abuts {n} other seats, want 1")

    def test_four_corner_raiders_can_seal_all_eight_seats(self):
        """raid.py's headline claim: 'four corner raiders can seal all eight seats'."""
        o = Position(8, 8)
        keys = {(s.x, s.y) for s in self.seats(o)}
        covered = set()
        for c in self.corners(o):
            for d in CARDINALS:
                t = c.add(d)
                if (t.x, t.y) in keys:
                    covered.add((t.x, t.y))
        self.assertEqual(covered, keys, "the four corners do NOT cover all 8 seats")

    def test_seats_and_corners_clip_to_the_map_in_every_corner(self):
        for o in (Position(0, 0), Position(18, 18), Position(0, 18), Position(18, 0)):
            for p in self.seats(o, 20, 20) + self.corners(o, 20, 20):
                self.assertTrue(0 <= p.x < 20 and 0 <= p.y < 20, f"{p} off map for {o}")
        # ... and the clipping is REAL, not vacuous: a corner anchor loses tiles.
        self.assertLess(len(self.seats(Position(0, 0), 20, 20)), 8)
        self.assertLess(len(self.corners(Position(0, 0), 20, 20)), 4)


# ===========================================================================
# 2.  BUILDER ADJACENCY -- GT-1, Manhattan-1 EXACTLY
# ===========================================================================

class TestBuilderAdjacencyIsManhattanOne(BotCase):
    """GT-1: build / attack / heal / destroy are Manhattan-1, NOT d^2 <= 2.

    Every place the tree enumerates a builder's action targets it iterates
    CARDINALS.  This asserts that the iteration set and the engine rule agree
    IN BOTH DIRECTIONS: every cardinal step is legal, and nothing else is.
    """

    def test_the_cardinal_set_is_exactly_the_manhattan_one_neighbourhood(self):
        p = Position(6, 6)
        card = {(p.add(d).x, p.add(d).y) for d in CARDINALS}
        want = {(p.x + dx, p.y + dy)
                for dx in range(-2, 3) for dy in range(-2, 3)
                if abs(dx) + abs(dy) == 1}
        self.assertEqual(card, want)
        # the OTHER verdict: diagonals and the own tile are excluded
        for d in DIAGONALS:
            self.assertNotIn((p.add(d).x, p.add(d).y), want, f"{d} is not Manhattan-1")
        self.assertNotIn((p.x, p.y), want, "own tile is not Manhattan-1")

    def test_the_engine_rule_refuses_diagonals_and_accepts_cardinals(self):
        """Drives the stub's GT-1 rule to both verdicts, so later tests mean something."""
        w = L.World(20, 20, ore=[(6, 5)])
        me = w.add(EntityType.BUILDER_BOT, (6, 6))
        ct = w.controller(me)
        self.assertTrue(ct.can_build_barrier(Position(6, 5)))
        self.assertFalse(ct.can_build_barrier(Position(5, 5)), "diagonal accepted")
        self.assertFalse(ct.can_build_barrier(Position(6, 6)), "own tile accepted")
        self.assertFalse(ct.can_build_barrier(Position(6, 4)), "Manhattan-2 accepted")

    def test_every_tree_site_that_walks_cardinals_reaches_the_whole_neighbourhood(self):
        """A regression net for the `_try_fwd_barrier` shape.

        `_raid_act`, `_raid_peck`, `_sabotage_prio`, `_has_acceptor`,
        `_l4_harvester_starved`, `_salt_beside_belt` and `_open_seats_by` all
        scan `for d in CARDINALS`.  If CARDINALS ever loses a member, every one
        of them silently narrows.  Four, distinct, all cardinal.
        """
        cs = self.b.const("CARDINALS")
        self.assertEqual(len(cs), 4)
        self.assertEqual(len(set(cs)), 4)
        for d in cs:
            self.assertTrue(d.is_cardinal(), f"{d} in CARDINALS is not cardinal (GT-7)")

    def test_DIRECTIONS_is_all_eight_and_excludes_CENTRE(self):
        ds = self.b.const("DIRECTIONS")
        self.assertEqual(len(ds), 8)
        self.assertNotIn(Direction.CENTRE, ds)

    def test_only_the_four_cardinal_neighbours_are_ever_buildable(self):
        """Ore on all eight neighbours; four sites, not eight.  BOTH verdicts."""
        w = L.World(20, 20, ore=[(6 + dx, 6 + dy)
                                 for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                                 if (dx, dy) != (0, 0)],
                    resources=500)
        me = w.add(EntityType.BUILDER_BOT, (6, 6), team=Team.A)
        ct = w.controller(me)
        ok = [d for d in self.b.const("DIRECTIONS")
              if ct.can_build_harvester(me.pos.add(d))]
        self.assertEqual(set(ok), set(CARDINALS),
                         f"buildable set is {ok}, want exactly the 4 cardinals (GT-1)")

    def test_the_harvester_siting_loop_spends_half_its_iterations_on_diagonals(self):
        """⚠ FINDING (CPU, not correctness): `_expand`'s harvester loop is the
        ONE build site in the tree that iterates DIRECTIONS instead of CARDINALS
        (`eco.py`, `for d in DIRECTIONS` under the harvester gate).

        GT-1 makes the four diagonal iterations guaranteed-False, so they are
        four wasted `can_build_harvester` engine calls per eligible builder-turn
        on the hot economy path.  Behaviour is unaffected -- DIRECTIONS visits
        N, E, S, W in the same relative order as CARDINALS and the loop breaks
        on success -- which is exactly why nothing has ever caught it.

        Driven BOTH ways: ore on the diagonals ONLY builds nothing, ore on a
        cardinal builds.  The first half is the finding; the second proves the
        fixture can produce a build at all.
        """
        def run(ore):
            w = L.World(20, 20, ore=ore, resources=500)
            w.add(EntityType.CORE, (2, 2), team=Team.A)
            me = w.add(EntityType.BUILDER_BOT, (10, 10), team=Team.A)
            ct = w.controller(me)
            ct.omniscient = True
            p = L.make_player(self.b, core=Position(2, 2), mw=20, mh=20,
                              role="expand", role_n=1, map_walls=set(),
                              map_ores=[Position(*t) for t in ore],
                              map_grid=tuple("." * 20 for _ in range(20)), idx=0)
            p._expand(ct)
            return [e for e in w.log if e[0] == "build"]

        diagonal_only = [(9, 9), (11, 9), (9, 11), (11, 11)]
        self.assertEqual(run(diagonal_only), [],
                         "a harvester was built on a DIAGONAL ore tile -- GT-1 says "
                         "builder builds are Manhattan-1 exactly")
        built = run([(10, 11)])
        self.assertTrue(built, "the fixture cannot produce a build at all")
        self.assertEqual(built[0][1], EntityType.HARVESTER)
        self.assertEqual((built[0][2].x, built[0][2].y), (10, 11))


# ===========================================================================
# 3.  THE RAID RING PREDICATES -- satisfying sets, both verdicts
# ===========================================================================

def _raid_world(mw=24, mh=24, E=(18, 18), me_at=(17, 17), ti=500, rnd=100):
    w = L.World(mw, mh, resources=ti, rnd=rnd)
    w.add(EntityType.CORE, (2, 2), team=Team.A)
    w.add(EntityType.CORE, E, team=Team.B)
    me = w.add(EntityType.BUILDER_BOT, me_at, team=Team.A)
    return w, me


class TestRaidRingPredicates(BotCase):

    def _player(self, **kw):
        kw.setdefault("core", Position(2, 2))
        kw.setdefault("enemy", Position(18, 18))
        kw.setdefault("mw", 24)
        kw.setdefault("mh", 24)
        return L.make_player(self.b, **kw)

    def test_ring_caches_and_INVALIDATES_when_the_anchor_moves(self):
        p = self._player()
        c1, s1 = p._ring(Position(18, 18))
        self.assertEqual(len(c1), 4)
        self.assertEqual(len(s1), 8)
        c2, s2 = p._ring(Position(4, 4))
        self.assertNotEqual(
            {(t.x, t.y) for t in s1}, {(t.x, t.y) for t in s2},
            "the per-unit ring cache did not invalidate on a new anchor -- a "
            "raider thrown across the map would collar the wrong Core")

    def test_open_seats_by_reports_two_when_blind_and_zero_when_sealed(self):
        """BOTH verdicts, and the pessimistic direction its docstring claims."""
        w, me = _raid_world(me_at=(17, 17))
        ct = w.controller(me)
        p = self._player()
        p._ring(Position(18, 18))
        corner = Position(17, 17)
        self.assertIn((corner.x, corner.y),
                      {(c.x, c.y) for c in self.corners(Position(18, 18), 24, 24)})
        # unreadable == OPEN (docstring), and every seat here is empty anyway
        self.assertEqual(p._open_seats_by(ct, corner), 2)
        # now seal both flanking seats -> the other verdict
        for d in CARDINALS:
            t = corner.add(d)
            if (t.x, t.y) in p.raid_seatkeys:
                w.add(EntityType.BARRIER, t, team=Team.A)
        self.assertEqual(p._open_seats_by(ct, corner), 0)

    def test_open_seats_by_never_exceeds_two_at_any_corner(self):
        """If it could return 3 or 4 the corner scoring would be reading noise."""
        w, me = _raid_world()
        ct = w.controller(me)
        p = self._player()
        p._ring(Position(18, 18))
        for corner in self.corners(Position(18, 18), 24, 24):
            self.assertLessEqual(p._open_seats_by(ct, corner), 2)

    def test_salt_forward_splits_the_board_and_refuses_the_tie(self):
        p = self._player(core=Position(2, 2))
        E = Position(18, 18)
        self.assertTrue(p._salt_forward(Position(17, 17), E))
        self.assertFalse(p._salt_forward(Position(3, 3), E))
        self.assertFalse(p._salt_forward(Position(10, 10), E),
                         "the exact midpoint must not count as forward")
        # and it fails CLOSED when the anchors are unknown
        self.assertFalse(self._player(core=None)._salt_forward(Position(17, 17), E))
        self.assertFalse(p._salt_forward(Position(17, 17), None))

    def test_foothold_live_drives_both_verdicts_across_the_staleness_edge(self):
        w, me = _raid_world()
        ct = w.controller(me)
        p = self._player()
        slot = self.b.const("SLOT_RAID_LIVE")
        stale = self.b.const("LOKI_FOOTHOLD_STALE")
        w.store[Team.A][slot] = 0
        self.assertFalse(p._foothold_live(ct, 50), "an unwritten slot read as live")
        # heartbeat is stored as round+1 so that round 0 is distinguishable
        w.store[Team.A][slot] = 41
        self.assertTrue(p._foothold_live(ct, 40 + stale))
        self.assertFalse(p._foothold_live(ct, 40 + stale + 1))

    def test_raid_open_has_three_doors_and_all_three_can_be_shut(self):
        w, me = _raid_world()
        ct = w.controller(me)
        p = self._player()
        cold = self.b.const("LOKI_COLD_INSERT_RND")
        slot = self.b.const("SLOT_RAID_LIVE")
        w.store[Team.A][slot] = 0
        self.assertTrue(p._raid_open(ct, cold + 500, True), "established was refused")
        self.assertTrue(p._raid_open(ct, cold - 1, False), "cold insert was refused")
        self.assertFalse(p._raid_open(ct, cold, False), "cold window did not close")
        w.store[Team.A][slot] = cold + 1
        self.assertTrue(p._raid_open(ct, cold + 5, False), "reinforcement was refused")

    def test_enemy_anchor_prefers_the_store_then_falls_back_to_symmetry(self):
        w, me = _raid_world()
        ct = w.controller(me)
        pack = self.b.fn("pack_pos")
        slot = self.b.const("SLOT_ENEMY_CORE")
        p = self._player(enemy=None)
        self.assertEqual(p._enemy_anchor(ct),
                         self.b.fn("enemy_core_for")(24, 24, Position(2, 2)))
        p2 = self._player(enemy=None)
        w.store[Team.A][slot] = pack(Position(19, 3))
        self.assertEqual(p2._enemy_anchor(ct), Position(19, 3),
                         "a SEEN Core did not beat map symmetry")


# ===========================================================================
# 4.  THE FORWARD-SENTINEL RANGE GUARD -- a superset, exhaustively
# ===========================================================================

class TestForwardSentinelRangeGuard(BotCase):
    """`_try_forward_sentinel` early-outs at `min d^2(p, core tile) > 50`.

    That is a FAST PATH over the real condition (`d^2(bp, target) <= 32` for
    some cardinal `bp = p + d`).  A fast path that is not a superset silently
    drops legal plants; a fast path whose complement is empty is dead code.
    Both directions are checked exhaustively over the offset lattice.
    """

    def test_the_fifty_guard_never_rejects_a_reachable_build_site(self):
        violations = [
            (dx, dy)
            for dx in range(-12, 13) for dy in range(-12, 13)
            if dx * dx + dy * dy > 50
            and any((dx + ex) ** 2 + (dy + ey) ** 2 <= 32
                    for ex, ey in ((0, -1), (1, 0), (0, 1), (-1, 0)))
        ]
        self.assertEqual(violations, [],
                         "the >50 early-out drops offsets that CAN align a Sentinel")

    def test_the_fifty_guard_is_not_vacuous_in_either_direction(self):
        admits = sum(
            1 for dx in range(-12, 13) for dy in range(-12, 13)
            if dx * dx + dy * dy <= 50
            and any((dx + ex) ** 2 + (dy + ey) ** 2 <= 32
                    for ex, ey in ((0, -1), (1, 0), (0, 1), (-1, 0)))
        )
        rejects = sum(1 for dx in range(-12, 13) for dy in range(-12, 13)
                      if dx * dx + dy * dy > 50)
        self.assertGreater(admits, 0, "no offset can ever plant a forward Sentinel")
        self.assertGreater(rejects, 0, "the guard never rejects anything")

    def test_a_sentinel_planted_beside_the_enemy_core_actually_fires_at_it(self):
        """End to end on the geometry: the plant lands and its ray holds a Core tile."""
        E = Position(18, 18)
        w, me = _raid_world(me_at=(18, 14), ti=500, rnd=30)
        ct = w.controller(me)
        w.store[Team.A][self.b.const("SLOT_HARVESTERS")] = 9
        p = L.make_player(self.b, core=Position(2, 2), enemy=E, mw=24, mh=24)
        self.assertTrue(p._try_forward_sentinel(ct, E), "no Sentinel site was found")
        built = [e for e in w.ents.values() if e.etype == EntityType.SENTINEL]
        self.assertEqual(len(built), 1)
        s = built[0]
        ray = ct.get_attackable_tiles_from(s.pos, s.direction, EntityType.SENTINEL)
        core_tiles = {(t.x, t.y) for t in self.tiles(E)}
        self.assertTrue(any((t.x, t.y) in core_tiles for t in ray),
                        f"planted Sentinel at {s.pos} facing {s.direction} does not "
                        f"cover any enemy Core tile")

    def test_the_forward_sentinel_is_refused_when_the_LIVE_cap_is_full(self):
        """The other verdict, and it must come from the cap and not from geometry."""
        E = Position(18, 18)
        w, me = _raid_world(me_at=(18, 13), ti=500, rnd=30)
        ct = w.controller(me)
        ct.omniscient = True     # so the census sees the band, not just r^2=20
        w.store[Team.A][self.b.const("SLOT_HARVESTERS")] = 9
        for t in ((16, 14), (17, 14), (19, 14)):
            w.add(EntityType.SENTINEL, t, team=Team.A, direction=Direction.SOUTH)
        p = L.make_player(self.b, core=Position(2, 2), enemy=E, mw=24, mh=24)
        self.assertEqual(p._live_fwd_guns(ct, E), self.b.const("LOKI_FWD_GUN_CAP"))
        self.assertFalse(p._try_forward_sentinel(ct, E))

    def test_the_LIVE_census_overrides_the_monotone_store(self):
        """LOKI2B by design: three DEAD forward sentinels must not close the cap.

        `SLOT_FWD_GUN` is monotone (incremented on build, never decremented on
        death), so if the store governed, the third loss would end the siege
        permanently.  Store pinned AT the cap, census 0 -> the plant proceeds.
        """
        E = Position(18, 18)
        w, me = _raid_world(me_at=(18, 14), ti=500, rnd=30)
        ct = w.controller(me)
        w.store[Team.A][self.b.const("SLOT_HARVESTERS")] = 9
        w.store[Team.A][self.b.const("SLOT_FWD_GUN")] = self.b.const("LOKI_FWD_GUN_CAP")
        p = L.make_player(self.b, core=Position(2, 2), enemy=E, mw=24, mh=24)
        self.assertEqual(p._live_fwd_guns(ct, E), 0)
        self.assertTrue(p._try_forward_sentinel(ct, E),
                        "the monotone store vetoed a plant the live census allows")

    def test_the_store_fallback_in_the_cap_check_cannot_change_the_outcome(self):
        """⚠ FINDING: dead-on-the-normal-path, by arithmetic between two constants.

        `_try_forward_sentinel` consults `SLOT_FWD_GUN` only when
        `_live_fwd_guns` returns None.  On the normal path that happens exactly
        when `min d^2(p, enemy Core tile) > LOKI2B_CENSUS_DSQ * 2` -- and three
        statements later the function returns False for anything past 50.  With
        `LOKI2B_CENSUS_DSQ = 50` the census window is 100, so **every position
        that reaches the store fallback is already refused by the range guard**:
        the fallback can only ever return False where False was returned anyway.

        ⛔ HONEST SCOPE.  This is NOT unsatisfiable.  `_live_fwd_guns` also
        returns None from its blanket `except`, so a raid-band unit whose
        `get_nearby_buildings` raises DOES reach the store branch meaningfully.
        The claim is only that the DISTANCE route to it is inert -- which is
        what makes the `LOKI2B_CENSUS_DSQ * 2 >= 50` relation load-bearing and
        worth pinning, since halving that constant would silently revive it.
        """
        census_window = self.b.const("LOKI2B_CENSUS_DSQ") * 2
        self.assertGreaterEqual(
            census_window, 50,
            "LOKI2B_CENSUS_DSQ * 2 has dropped below the 50 range guard: the "
            "monotone-store fallback is now reachable by DISTANCE and the live "
            "cap no longer governs alone -- re-read _try_forward_sentinel")

    def test_the_forward_sentinel_is_refused_below_the_harvester_prerequisite(self):
        E = Position(18, 18)
        w, me = _raid_world(me_at=(18, 14), ti=500, rnd=30)
        ct = w.controller(me)
        w.store[Team.A][self.b.const("SLOT_HARVESTERS")] = 0
        p = L.make_player(self.b, core=Position(2, 2), enemy=E, mw=24, mh=24)
        self.assertFalse(p._try_forward_sentinel(ct, E))


# ===========================================================================
# 5.  THE LAUNCHER THROW ENVELOPE -- GT-2
# ===========================================================================

class TestLauncherThrowEnvelope(BotCase):
    """GT-2: pickup d^2 <= 2, throw 1 <= d^2 <= 26 measured FROM THE LAUNCHER."""

    def _sites(self, lp, w, h):
        """The tree's own site enumeration, lifted from `_launcher_turn`."""
        return [Position(lp.x + dx, lp.y + dy)
                for dx in range(-5, 6) for dy in range(-5, 6)
                if dx * dx + dy * dy <= 26
                and 0 <= lp.x + dx < w and 0 <= lp.y + dy < h]

    def test_the_site_scan_covers_the_whole_legal_throw_envelope(self):
        lp = Position(12, 12)
        got = {(t.x, t.y) for t in self._sites(lp, 30, 30)}
        want = {(lp.x + dx, lp.y + dy)
                for dx in range(-8, 9) for dy in range(-8, 9)
                if 1 <= dx * dx + dy * dy <= 26}
        self.assertEqual(got - want, {(lp.x, lp.y)},
                         "the site scan reaches tiles outside 1 <= d^2 <= 26")
        self.assertEqual(want - got, set(),
                         "the -5..5 box MISSES legal throw destinations")

    def test_the_site_scan_includes_the_launchers_own_tile_which_is_never_legal(self):
        """FINDING (benign): `dx == dy == 0` passes `d^2 <= 26` and is enumerated.

        GT-2 is 1 <= d^2, so `can_launch` refuses it and nothing breaks -- the
        cost is one wasted predicate call per throw.  Asserted rather than left
        implicit so that if the engine ever stops refusing d^2 == 0 (a throw
        onto the launcher's own impassable tile) this test names the site.
        """
        lp = Position(12, 12)
        self.assertIn((lp.x, lp.y), {(t.x, t.y) for t in self._sites(lp, 30, 30)})
        w = L.World(30, 30)
        lch = w.add(EntityType.LAUNCHER, lp, team=Team.A)
        w.add(EntityType.BUILDER_BOT, (12, 11), team=Team.B)
        ct = w.controller(lch)
        self.assertFalse(ct.can_launch(Position(12, 11), lp),
                         "the engine model accepted a d^2 == 0 throw")

    def test_exile_throws_the_enemy_body_as_far_from_our_core_as_it_can(self):
        w = L.World(30, 30, resources=500)
        w.add(EntityType.CORE, (2, 2), team=Team.A)
        lch = w.add(EntityType.LAUNCHER, (6, 6), team=Team.A)
        w.add(EntityType.BUILDER_BOT, (6, 5), team=Team.B)
        ct = w.controller(lch)
        p = L.make_player(self.b, core=Position(2, 2), enemy=Position(26, 26),
                          mw=30, mh=30)
        p._launcher_turn(ct)
        thrown = [e for e in w.log if e[0] == "launch"]
        self.assertEqual(len(thrown), 1, f"no exile throw happened: {w.log}")
        dest = thrown[0][2]
        self.assertGreater(dest.distance_squared(Position(2, 2)),
                           Position(6, 5).distance_squared(Position(2, 2)),
                           "the exile threw the intruder TOWARD our Core")

    def test_a_friendly_body_is_never_exiled(self):
        """The other verdict: `can_launch` has no team check, so the BOT must."""
        w = L.World(30, 30, resources=500)
        w.add(EntityType.CORE, (2, 2), team=Team.A)
        lch = w.add(EntityType.LAUNCHER, (6, 6), team=Team.A)
        w.add(EntityType.BUILDER_BOT, (6, 5), team=Team.A)
        ct = w.controller(lch)
        p = L.make_player(self.b, core=Position(2, 2), enemy=Position(26, 26),
                          mw=30, mh=30)
        p._launcher_turn(ct)
        self.assertEqual([e for e in w.log if e[0] == "launch"], [],
                         "a FRIENDLY builder was exiled")


# ===========================================================================
# 6.  ECONOMY / BUDGET GATES
# ===========================================================================

class TestEconomyGates(BotCase):

    def _core_ct(self, ti=500, rnd=0, mw=20, mh=20):
        w = L.World(mw, mh, resources=ti, rnd=rnd)
        c = w.add(EntityType.CORE, (2, 2), team=Team.A)
        return w, w.controller(c)

    def test_eco_spendable_both_verdicts_and_the_siege_reserve_actually_bites(self):
        w, ct = self._core_ct(ti=100)
        p = L.make_player(self.b, core=Position(2, 2))
        self.assertTrue(p._eco_spendable(ct, 100), "exact-bank spend refused")
        self.assertFalse(p._eco_spendable(ct, 101))
        reserve = self.b.const("SIEGE_HEAL_RESERVE_TI")
        w.store[Team.A][self.b.const("SLOT_UNDER")] = 1
        w.round = self.b.const("HUNT_MIN_RND")
        self.assertFalse(p._eco_spendable(ct, 100),
                         "the siege heal reserve did not raise the bar")
        self.assertTrue(p._eco_spendable(ct, 100 - reserve))

    def test_eco_spendable_ignores_the_reserve_before_HUNT_MIN_RND(self):
        """Both halves of the AND, driven separately."""
        w, ct = self._core_ct(ti=100)
        p = L.make_player(self.b, core=Position(2, 2))
        w.store[Team.A][self.b.const("SLOT_UNDER")] = 1
        w.round = self.b.const("HUNT_MIN_RND") - 1
        self.assertTrue(p._eco_spendable(ct, 100), "the round half of the gate is dead")
        w.round = self.b.const("HUNT_MIN_RND")
        w.store[Team.A][self.b.const("SLOT_UNDER")] = 0
        self.assertTrue(p._eco_spendable(ct, 100), "the siege half of the gate is dead")

    def test_eco_cap_switches_to_surge_at_the_exact_boundary(self):
        floor = self.b.const("SURGE_TI_FLOOR")
        minrnd = self.b.const("SURGE_MIN_RND")
        base, surge = self.b.const("ECO_CAP"), self.b.const("SURGE_ECO_CAP")
        self.assertNotEqual(base, surge, "the surge cap equals the base cap")
        w, ct = self._core_ct(ti=floor, rnd=minrnd)
        p = L.make_player(self.b, core=Position(2, 2))
        self.assertEqual(p._eco_cap(ct), surge)
        w.resources[Team.A] = floor - 1
        self.assertEqual(p._eco_cap(ct), base)
        w.resources[Team.A] = floor
        w.round = minrnd - 1
        self.assertEqual(p._eco_cap(ct), base)

    def test_cpu_guard_trips_at_the_budget_and_fails_OPEN_when_blind(self):
        budget = self.b.const("CPU_BUDGET_US")
        w, ct = self._core_ct()
        p = L.make_player(self.b, core=Position(2, 2))
        w.cpu_us = budget - 1
        self.assertFalse(p._cpu_exhausted(ct))
        w.cpu_us = budget
        with redirect_stderr(io.StringIO()) as err:
            self.assertTrue(p._cpu_exhausted(ct))
        self.assertIn("CPU-GUARD tripped", err.getvalue(),
                      "the guard tripped silently -- the one-per-unit report is gone")
        # ... and it reports ONCE per unit lifetime, so a bug cannot flood stderr
        with redirect_stderr(io.StringIO()) as err2:
            self.assertTrue(p._cpu_exhausted(ct))
        self.assertEqual(err2.getvalue(), "", "the CPU report repeated")

        class Blind:
            def get_cpu_time_elapsed(self):
                raise RuntimeError("no clock")

        p2 = L.make_player(self.b, core=Position(2, 2))
        self.assertFalse(p2._cpu_exhausted(Blind()),
                         "a blind CPU clock must fail OPEN, not freeze the unit")

    def test_seat_ban_partitions_the_eight_seats_into_kept_and_banned(self):
        p = L.make_player(self.b, core=Position(4, 4), mw=20, mh=20,
                          map_walls=set(), map_ores=[])
        ban = p._seat_ban()
        self.assertIsNotNone(ban)
        seats = {(s.x, s.y) for s in self.seats(Position(4, 4))}
        keep = {(s.x, s.y) for s in p.seat_keep}
        self.assertEqual(ban | keep, seats, "ban+keep is not the seat set")
        self.assertEqual(ban & keep, set(), "a seat is both kept and banned")
        self.assertEqual(len(keep), self.b.const("HS_DELIVERY_SEATS"))
        self.assertTrue(ban, "the ban is empty -- seat protection would be a no-op")

    def test_seat_ban_is_None_without_a_known_core(self):
        self.assertIsNone(L.make_player(self.b, core=None)._seat_ban())
        self.assertIsNone(L.make_player(self.b, core=Position(4, 4), mw=0, mh=0)
                          ._seat_ban())

    def test_delivery_seats_prefers_non_wall_seats_and_is_deterministic(self):
        o = Position(6, 6)
        ds = self.b.fn("delivery_seats")
        seats = {(s.x, s.y) for s in self.seats(o)}
        plain = ds(o, 20, 20, set(), [])
        self.assertEqual(len(plain), self.b.const("HS_DELIVERY_SEATS"))
        self.assertTrue({(s.x, s.y) for s in plain} <= seats)
        self.assertEqual(plain, ds(o, 20, 20, set(), []), "not deterministic")
        # walls on the chosen seats must push the choice elsewhere -- both verdicts
        walled = {(s.x, s.y) for s in plain}
        moved = ds(o, 20, 20, walled, [])
        self.assertEqual(set(), {(s.x, s.y) for s in moved} & walled,
                         "a walled seat was still chosen for delivery")
        # ore steers the choice: with ore hard west, a west seat must be chosen
        west = ds(o, 20, 20, set(), [Position(0, 6), Position(0, 7)])
        self.assertTrue(min(s.x for s in west) < min(s.x for s in plain) + 1)

    def test_delivery_seats_falls_back_when_every_seat_is_walled(self):
        o = Position(6, 6)
        ds = self.b.fn("delivery_seats")
        allwall = {(s.x, s.y) for s in self.seats(o)}
        got = ds(o, 20, 20, allwall, [])
        self.assertTrue(got, "an all-walled ring returned no delivery seat at all")


# ===========================================================================
# 7.  NEIGHBOURHOOD PREDICATES -- the ones that read four tiles
# ===========================================================================

class TestNeighbourhoodPredicates(BotCase):

    def _world(self, ti=500):
        w = L.World(20, 20, resources=ti)
        w.add(EntityType.CORE, (2, 2), team=Team.A)
        me = w.add(EntityType.BUILDER_BOT, (10, 10), team=Team.A)
        return w, me, w.controller(me)

    def test_has_acceptor_both_verdicts_and_an_ENEMY_belt_is_not_one(self):
        w, me, ct = self._world()
        p = L.make_player(self.b, core=Position(2, 2))
        bp = Position(10, 11)
        self.assertFalse(p._has_acceptor(ct, bp))
        w.add(EntityType.CONVEYOR, (10, 12), team=Team.B,
              direction=Direction.SOUTH)
        self.assertFalse(p._has_acceptor(ct, bp),
                         "an ENEMY conveyor counted as our acceptor")
        w.add(EntityType.CONVEYOR, (11, 11), team=Team.A,
              direction=Direction.EAST)
        self.assertTrue(p._has_acceptor(ct, bp))

    def test_has_acceptor_accepts_the_core_itself(self):
        w, me, ct = self._world()
        p = L.make_player(self.b, core=Position(2, 2))
        w.add(EntityType.SPLITTER, (10, 11), team=Team.A, direction=Direction.NORTH)
        self.assertTrue(p._has_acceptor(ct, Position(10, 10)))

    def test_l4_harvester_starved_both_verdicts(self):
        w, me, ct = self._world()
        p = L.make_player(self.b, core=Position(2, 2))
        h = Position(10, 11)
        gap = Position(10, 10)
        w.add(EntityType.HARVESTER, h, team=Team.A)
        self.assertTrue(p._l4_harvester_starved(ct, h, gap),
                        "a harvester with no route home read as fed")
        w.add(EntityType.CONVEYOR, (11, 11), team=Team.A, direction=Direction.EAST)
        self.assertFalse(p._l4_harvester_starved(ct, h, gap),
                         "a harvester WITH a route home read as starved -- "
                         "the gate would buy a second route for nothing")

    def test_l4_a_conveyor_pointing_INTO_the_harvester_is_not_a_route_home(self):
        w, me, ct = self._world()
        p = L.make_player(self.b, core=Position(2, 2))
        h = Position(10, 11)
        w.add(EntityType.HARVESTER, h, team=Team.A)
        # output faces the harvester -> it feeds the harvester, it does not drain it
        w.add(EntityType.CONVEYOR, (11, 11), team=Team.A, direction=Direction.WEST)
        self.assertTrue(p._l4_harvester_starved(ct, h, Position(10, 10)))

    def test_l4_an_ENEMY_belt_beside_our_harvester_is_the_siphon_not_a_route(self):
        """`_l4_harvester_starved.__doc__` states this explicitly."""
        w, me, ct = self._world()
        p = L.make_player(self.b, core=Position(2, 2))
        h = Position(10, 11)
        w.add(EntityType.HARVESTER, h, team=Team.A)
        w.add(EntityType.CONVEYOR, (11, 11), team=Team.B, direction=Direction.EAST)
        self.assertTrue(p._l4_harvester_starved(ct, h, Position(10, 10)),
                        "an ENEMY belt counted as our harvester's route home")

    def test_l4_skips_the_gap_tile_itself(self):
        w, me, ct = self._world()
        p = L.make_player(self.b, core=Position(2, 2))
        h = Position(10, 11)
        gap = Position(11, 11)
        w.add(EntityType.HARVESTER, h, team=Team.A)
        w.add(EntityType.CONVEYOR, gap, team=Team.A, direction=Direction.EAST)
        self.assertTrue(p._l4_harvester_starved(ct, h, gap),
                        "the gap tile was counted as an existing acceptor")

    def test_l4_repair_fills_a_ONE_wide_hole_and_leaves_a_TWO_wide_one_alone(self):
        """`_l4_repair.__doc__`: 'a two-wide hole has no side with both a feeder
        and an acceptor, so it is left alone'.

        This is the incumbent's most `_try_fwd_barrier`-shaped predicate -- two
        distinct conditions required among ONE tile's four neighbours -- so its
        satisfying set is checked in both directions rather than trusted.
        """
        def run(acceptor_at, acceptor_dir):
            w = L.World(20, 20, resources=500)
            w.add(EntityType.CORE, (2, 2), team=Team.A)
            me = w.add(EntityType.BUILDER_BOT, (6, 6), team=Team.A)
            ct = w.controller(me)
            ct.omniscient = True
            w.add(EntityType.CONVEYOR, (5, 7), team=Team.A, direction=Direction.EAST)
            w.add(EntityType.CONVEYOR, acceptor_at, team=Team.A,
                  direction=acceptor_dir)
            p = L.make_player(self.b, core=Position(2, 2), enemy=Position(18, 18),
                              mw=20, mh=20, map_walls=set(), map_ores=[])
            with redirect_stderr(io.StringIO()), redirect_stdout(io.StringIO()):
                fired = p._l4_repair(ct)
            return fired, [e for e in w.log if e[0] == "build"]

        # one-wide hole at (6,7): feeder west of it, acceptor south of it
        fired, built = run((6, 8), Direction.SOUTH)
        self.assertTrue(fired, "the one-wide hole was not repaired")
        self.assertEqual((built[0][2].x, built[0][2].y), (6, 7))
        # two-wide hole: the acceptor is one tile further, so no single gap
        # tile has both a feeder and an acceptor beside it
        fired2, built2 = run((6, 9), Direction.SOUTH)
        self.assertFalse(fired2, "a TWO-wide hole was repaired -- the rule can now "
                                 "walk, and its 'cannot spam' argument is void")
        self.assertEqual(built2, [])

    def test_salt_beside_belt_both_verdicts_and_ignores_our_own_belt(self):
        w, me, ct = self._world()
        p = L.make_player(self.b, core=Position(2, 2))
        t = Position(10, 11)
        self.assertFalse(p._salt_beside_belt(ct, t))
        w.add(EntityType.CONVEYOR, (10, 12), team=Team.A, direction=Direction.SOUTH)
        self.assertFalse(p._salt_beside_belt(ct, t), "our OWN belt triggered salt")
        w.add(EntityType.CONVEYOR, (11, 11), team=Team.B, direction=Direction.EAST)
        self.assertTrue(p._salt_beside_belt(ct, t))

    def test_live_home_gun_both_verdicts_and_respects_the_band_and_the_team(self):
        band = self.b.const("HUNT_BAND_DSQ")
        w = L.World(30, 30)
        w.add(EntityType.CORE, (2, 2), team=Team.A)
        me = w.add(EntityType.BUILDER_BOT, (4, 4), team=Team.A)
        ct = w.controller(me)
        ct.omniscient = True
        p = L.make_player(self.b, core=Position(2, 2), mw=30, mh=30)
        self.assertFalse(p._live_home_gun(ct))
        far = w.add(EntityType.SENTINEL, (2, 20), team=Team.A, direction=Direction.NORTH)
        self.assertFalse(p._live_home_gun(ct), "a turret far outside the band counted")
        w.remove(far.eid)
        w.add(EntityType.GUNNER, (2, 6), team=Team.B, direction=Direction.NORTH)
        self.assertFalse(p._live_home_gun(ct), "an ENEMY turret counted as ours")
        w.add(EntityType.GUNNER, (4, 2), team=Team.A, direction=Direction.EAST)
        self.assertTrue(p._live_home_gun(ct))
        # and the band edge is where it says it is
        d = min(t.distance_squared(Position(4, 2)) for t in self.tiles(Position(2, 2)))
        self.assertLessEqual(d, band)

    def test_core_shelled_both_verdicts(self):
        w = L.World(20, 20)
        core = w.add(EntityType.CORE, (2, 2), team=Team.A)
        me = w.add(EntityType.BUILDER_BOT, (4, 4), team=Team.A)
        ct = w.controller(me)
        p = L.make_player(self.b, core=Position(2, 2))
        self.assertFalse(p._core_shelled(ct))
        core.hp -= 1
        self.assertTrue(p._core_shelled(ct))

    def test_siphon_taken_both_verdicts_and_ignores_self_and_enemies(self):
        w, me, ct = self._world()
        p = L.make_player(self.b, core=Position(2, 2))
        belt = Position(12, 10)
        self.assertFalse(p._siphon_taken(ct, belt, me.eid))
        w.add(EntityType.BUILDER_BOT, (12, 11), team=Team.B)
        self.assertFalse(p._siphon_taken(ct, belt, me.eid), "an enemy body claimed it")
        w.add(EntityType.BUILDER_BOT, (13, 10), team=Team.A)
        self.assertTrue(p._siphon_taken(ct, belt, me.eid))


# ===========================================================================
# 8.  TURRET PREDICATES
# ===========================================================================

class TestTurretPredicates(BotCase):

    def _gunner(self, facing=Direction.EAST, at=(10, 10), ti=500):
        w = L.World(24, 24, resources=ti)
        w.add(EntityType.CORE, (2, 2), team=Team.A)
        g = w.add(EntityType.GUNNER, at, team=Team.A, direction=facing)
        return w, g, w.controller(g)

    def test_hostile_at_both_verdicts_and_off_map_fails_closed(self):
        w, g, ct = self._gunner()
        p = L.make_player(self.b, core=Position(2, 2), mw=24, mh=24)
        self.assertFalse(p._hostile_at(ct, Position(11, 10)))
        w.add(EntityType.BARRIER, (11, 10), team=Team.A)
        self.assertFalse(p._hostile_at(ct, Position(11, 10)), "our own barrier is hostile")
        w.add(EntityType.BUILDER_BOT, (12, 10), team=Team.B)
        self.assertTrue(p._hostile_at(ct, Position(12, 10)))
        self.assertFalse(p._hostile_at(ct, Position(-1, -1)),
                         "an off-map read did not fail closed")

    def test_facing_has_target_both_verdicts_and_fails_CLOSED_on_error(self):
        w, g, ct = self._gunner()
        p = L.make_player(self.b, core=Position(2, 2), mw=24, mh=24)
        self.assertFalse(p._facing_has_target(ct), "an empty ray reported a target")
        w.add(EntityType.BUILDER_BOT, (12, 10), team=Team.B)
        self.assertTrue(p._facing_has_target(ct))

        class Broken:
            def get_gunner_target(self):
                raise RuntimeError("blind")

        self.assertTrue(L.make_player(self.b)._facing_has_target(Broken()),
                        "on error this must claim a target, so rotation is REFUSED")

    def test_ray_lands_both_verdicts_and_an_EMPTY_target_never_lands(self):
        """M-1, and defect #2 of the three this file exists for.

        A gunner's `can_fire_from` is False on an empty tile.  `_ray_lands` is
        only ever called with a tile that holds a live entity -- assert both
        that it lands there and that it does NOT land on the empty tile one
        step further along the same ray, which is the confusion that produced
        the constant-false guard in `_v230sent41`.
        """
        w, g, ct = self._gunner()
        p = L.make_player(self.b, core=Position(2, 2), mw=24, mh=24)
        w.add(EntityType.BUILDER_BOT, (12, 10), team=Team.B)
        tgt = Position(12, 10)
        self.assertTrue(p._ray_lands(ct, g.pos, Direction.EAST, tgt))
        self.assertFalse(p._ray_lands(ct, g.pos, Direction.NORTH, tgt),
                         "the ray landed on a target that is not on it")
        self.assertFalse(p._ray_lands(ct, g.pos, Direction.EAST, Position(13, 10)),
                         "a gunner ray 'landed' on an EMPTY tile")

    def test_ray_lands_is_blocked_by_an_intervening_body(self):
        w, g, ct = self._gunner()
        p = L.make_player(self.b, core=Position(2, 2), mw=24, mh=24)
        w.add(EntityType.BUILDER_BOT, (12, 10), team=Team.B)
        self.assertTrue(p._ray_lands(ct, g.pos, Direction.EAST, Position(12, 10)))
        w.add(EntityType.BARRIER, (11, 10), team=Team.A)
        self.assertFalse(p._ray_lands(ct, g.pos, Direction.EAST, Position(12, 10)),
                         "GT-5: a gunner ray is obstacle-blocked")

    def test_rotate_allowed_reaches_all_four_of_its_returns(self):
        w, g, ct = self._gunner()
        cd = self.b.const("ROTATE_COOLDOWN_RNDS")
        p = L.make_player(self.b, core=Position(2, 2), mw=24, mh=24)
        tgt = Position(12, 10)

        # (a) cooldown expired -> unconditionally allowed
        p.rot_rnd = -10 ** 9
        self.assertTrue(p._rotate_allowed(ct, g.pos, Direction.NORTH, tgt))

        # (b) inside the cooldown, rotating straight back -> refused
        w.round = 5
        p.rot_rnd = 5 - (cd - 1)
        p.rot_prev_dir = Direction.NORTH
        p.rot_lock_d = 10 ** 9
        self.assertFalse(p._rotate_allowed(ct, g.pos, Direction.NORTH, tgt),
                         "the anti-thrash 'never straight back' rule is dead")

        # (c) inside the cooldown with a live target on the current facing
        p.rot_prev_dir = Direction.SOUTH
        w.add(EntityType.BUILDER_BOT, (11, 10), team=Team.B)
        self.assertFalse(p._rotate_allowed(ct, g.pos, Direction.NORTH, tgt),
                         "rotated away from a facing that still has a target")

        # (d) inside the cooldown, no current target, must beat the lock distance
        w.remove(w.bot_at(Position(11, 10)).eid)
        p.rot_lock_d = 10 ** 9
        self.assertTrue(p._rotate_allowed(ct, g.pos, Direction.NORTH, tgt))
        p.rot_lock_d = 0
        self.assertFalse(p._rotate_allowed(ct, g.pos, Direction.NORTH, tgt),
                         "the 3x-closer lock never refuses anything")

    def test_a_sentinel_prefers_the_core_over_a_nearer_soft_target(self):
        """Defect #3's shape: a priority table that never selects its own target.

        Ranks are CORE 0 ... HARVESTER 5, so a Core anywhere on the ray must
        outrank a harvester standing closer.  Driven BOTH ways: with the Core
        removed the harvester IS taken, which proves the harvester branch is
        reachable at all.
        """
        w = L.World(30, 30, resources=500)
        w.add(EntityType.CORE, (2, 2), team=Team.A)
        s = w.add(EntityType.SENTINEL, (10, 10), team=Team.A, direction=Direction.EAST)
        ct = w.controller(s)
        harv = w.add(EntityType.HARVESTER, (12, 10), team=Team.B)
        ecore = w.add(EntityType.CORE, (14, 9), team=Team.B)
        p = L.make_player(self.b, core=Position(2, 2), mw=30, mh=30)
        p._turret(ct)
        fired = [e for e in w.log if e[0] == "fire"]
        self.assertEqual(len(fired), 1, f"the sentinel did not fire: {w.log}")
        self.assertIn((fired[0][1].x, fired[0][1].y),
                      {(t.x, t.y) for t in ecore.tiles},
                      "the sentinel shot the harvester while an enemy CORE was on "
                      "its ray -- the priority table does not select its own target")
        # the other verdict: no Core -> the harvester IS the pick
        w.remove(ecore.eid)
        w.log.clear()
        p2 = L.make_player(self.b, core=Position(2, 2), mw=30, mh=30)
        p2._turret(ct)
        fired = [e for e in w.log if e[0] == "fire"]
        self.assertEqual([(f[1].x, f[1].y) for f in fired], [(harv.pos.x, harv.pos.y)])

    def test_a_gunner_never_shoots_through_a_friendly_blocker(self):
        w = L.World(30, 30, resources=500)
        w.add(EntityType.CORE, (2, 2), team=Team.A)
        g = w.add(EntityType.GUNNER, (10, 10), team=Team.A, direction=Direction.EAST)
        ct = w.controller(g)
        w.add(EntityType.BARRIER, (11, 10), team=Team.A)
        w.add(EntityType.BUILDER_BOT, (12, 10), team=Team.B)
        p = L.make_player(self.b, core=Position(2, 2), mw=30, mh=30)
        p._turret(ct)
        self.assertEqual([e for e in w.log if e[0] == "fire"], [],
                         "the gunner fired through its own barrier")

    def test_a_gunner_does_fire_when_the_lane_is_clear(self):
        w = L.World(30, 30, resources=500)
        w.add(EntityType.CORE, (2, 2), team=Team.A)
        g = w.add(EntityType.GUNNER, (10, 10), team=Team.A, direction=Direction.EAST)
        ct = w.controller(g)
        w.add(EntityType.BUILDER_BOT, (12, 10), team=Team.B)
        p = L.make_player(self.b, core=Position(2, 2), mw=30, mh=30)
        p._turret(ct)
        self.assertEqual([(e[1].x, e[1].y) for e in w.log if e[0] == "fire"],
                         [(12, 10)])


# ===========================================================================
# 9.  THE COUNTERBATTERY GATE
# ===========================================================================

class TestCounterbatteryGate(BotCase):

    def _setup(self, ti=500, role="defend", threat=(4, 4)):
        w = L.World(24, 24, resources=ti)
        w.add(EntityType.CORE, (2, 2), team=Team.A)
        me = w.add(EntityType.BUILDER_BOT, (4, 3), team=Team.A)
        ct = w.controller(me)
        ct.omniscient = True
        if threat is not None:
            w.store[Team.A][self.b.const("SLOT_THREAT")] = \
                self.b.fn("pack_pos")(Position(*threat))
        p = L.make_player(self.b, core=Position(2, 2), mw=24, mh=24, role=role)
        return w, me, ct, p

    def test_cb_over_heal_is_reachable_and_every_one_of_its_gates_can_shut_it(self):
        w, me, ct, p = self._setup()
        self.assertTrue(p._cb_over_heal(ct), "the counterbattery-over-heal state "
                                             "is unreachable as configured")
        # gate 1: role
        w2, _, ct2, p2 = self._setup(role="expand")
        self.assertFalse(p2._cb_over_heal(ct2))
        # gate 2: no reported threat
        w3, _, ct3, p3 = self._setup(threat=None)
        self.assertFalse(p3._cb_over_heal(ct3))
        # gate 3: threat outside the home band
        w4, _, ct4, p4 = self._setup(threat=(22, 22))
        self.assertFalse(p4._cb_over_heal(ct4))
        # gate 4: bank below sentinel + reserve
        w5, _, ct5, p5 = self._setup(ti=1)
        self.assertFalse(p5._cb_over_heal(ct5))
        # gate 5: a live home gun already exists
        w6, _, ct6, p6 = self._setup()
        w6.add(EntityType.GUNNER, (4, 2), team=Team.A, direction=Direction.EAST)
        self.assertFalse(p6._cb_over_heal(ct6))

    def test_try_counterbattery_builds_a_ray_that_contains_the_threat(self):
        w, me, ct, p = self._setup(threat=(4, 6))
        w.store[Team.A][self.b.const("SLOT_HARVESTERS")] = 9
        w.add(EntityType.BUILDER_BOT, (4, 6), team=Team.B)
        self.assertTrue(p._try_counterbattery(ct), f"nothing was built: {w.log}")
        built = [e for e in w.ents.values()
                 if e.etype in (EntityType.GUNNER, EntityType.SENTINEL)
                 and e.team == Team.A]
        self.assertEqual(len(built), 1)
        t = built[0]
        self.assertTrue(
            ct.can_fire_from(t.pos, t.direction, t.etype, Position(4, 6)),
            f"built a {t.etype} at {t.pos} facing {t.direction} whose ray does NOT "
            f"contain the reported threat")

    def test_try_counterbattery_refuses_when_no_threat_is_reported(self):
        w, me, ct, p = self._setup(threat=None)
        self.assertFalse(p._try_counterbattery(ct))

    def test_try_counterbattery_never_plants_on_a_banned_delivery_seat(self):
        """A turret is impassable, so one on a kept seat costs +4 HP/round forever."""
        w = L.World(24, 24, resources=500)
        w.add(EntityType.CORE, (2, 2), team=Team.A)
        p = L.make_player(self.b, core=Position(2, 2), mw=24, mh=24, role="defend",
                          map_walls=set(), map_ores=[])
        ban = p._seat_ban()
        seat = Position(*sorted(ban)[0])
        # stand orthogonally beside a banned seat, with the threat on its ray
        stand = seat.add(Direction.NORTH) if seat.y > 0 else seat.add(Direction.SOUTH)
        me = w.add(EntityType.BUILDER_BOT, stand, team=Team.A)
        ct = w.controller(me)
        ct.omniscient = True
        w.store[Team.A][self.b.const("SLOT_HARVESTERS")] = 9
        threat = Position(seat.x, seat.y + 2) if seat.y + 2 < 24 else Position(seat.x, 0)
        w.store[Team.A][self.b.const("SLOT_THREAT")] = self.b.fn("pack_pos")(threat)
        w.add(EntityType.BUILDER_BOT, threat, team=Team.B)
        p._try_counterbattery(ct)
        planted = [(e.pos.x, e.pos.y) for e in w.ents.values()
                   if e.team == Team.A
                   and e.etype in (EntityType.GUNNER, EntityType.SENTINEL)]
        self.assertNotIn((seat.x, seat.y), planted,
                         "a turret was planted on a BANNED heal seat")


# ===========================================================================
# 10.  NAVIGATION -- GT-7
# ===========================================================================

class TestNavigationIsCardinalOnly(BotCase):

    def test_bfs_direction_only_ever_returns_a_cardinal_or_CENTRE(self):
        """GT-7: `move(<diagonal>)` raises, and an escaping GameError DELETES the unit."""
        w = L.World(12, 12, walls=[(5, y) for y in range(1, 10)])
        me = w.add(EntityType.BUILDER_BOT, (2, 5), team=Team.A)
        ct = w.controller(me)
        ct.omniscient = True
        grid = tuple("".join("#" if (x, y) in {(5, yy) for yy in range(1, 10)} else "."
                             for x in range(12)) for y in range(12))
        legal = set(CARDINALS) | {Direction.CENTRE}
        for tx in range(12):
            for ty in range(12):
                p = L.make_player(self.b, core=Position(1, 1), mw=12, mh=12,
                                  map_grid=grid,
                                  map_walls={(5, yy) for yy in range(1, 10)})
                d = p._bfs_direction(ct, Position(tx, ty))
                self.assertIn(d, legal,
                              f"_bfs_direction returned {d} for target ({tx},{ty}) -- "
                              f"builders may only move N/E/S/W")

    def test_bfs_direction_routes_AROUND_a_wall_rather_than_into_it(self):
        walls = {(5, yy) for yy in range(0, 9)}
        w = L.World(12, 12, walls=sorted(walls))
        me = w.add(EntityType.BUILDER_BOT, (4, 3), team=Team.A)
        ct = w.controller(me)
        ct.omniscient = True
        grid = tuple("".join("#" if (x, y) in walls else "." for x in range(12))
                     for y in range(12))
        p = L.make_player(self.b, core=Position(1, 1), mw=12, mh=12,
                          map_grid=grid, map_walls=walls)
        d = p._bfs_direction(ct, Position(6, 3))
        self.assertNotEqual(d, Direction.EAST, "stepped straight into the wall")
        self.assertIn(d, (Direction.SOUTH, Direction.NORTH))
        # the other verdict: no wall in the way -> it goes straight there
        w2 = L.World(12, 12)
        me2 = w2.add(EntityType.BUILDER_BOT, (4, 3), team=Team.A)
        ct2 = w2.controller(me2)
        ct2.omniscient = True
        grid2 = tuple("." * 12 for _ in range(12))
        p2 = L.make_player(self.b, core=Position(1, 1), mw=12, mh=12,
                           map_grid=grid2, map_walls=set())
        self.assertEqual(p2._bfs_direction(ct2, Position(6, 3)), Direction.EAST)

    def test_nav_fallbacks_cover_all_three_remaining_cardinals(self):
        """`_nav` retries (+1, +3, opposite).  If those are not the other three,
        a boxed-in builder would loop on the same blocked step."""
        cs = list(self.b.const("CARDINALS"))
        for i, desired in enumerate(cs):
            tried = {cs[(i + 1) % 4], cs[(i + 3) % 4], desired.opposite()}
            self.assertEqual(tried, set(cs) - {desired},
                             f"_nav's fallbacks from {desired} are not the other three")


# ===========================================================================
# 11.  FINDINGS -- branches that cannot fire in the SHIPPED configuration
# ===========================================================================

class TestQuietFlagDeadBranches(BotCase):
    """LOKI_QUIET_ON = True makes four melee branches unreachable.

    That is INTENDED -- QUIET is a measured decision (2 damage a round against a
    500 HP Core that heals +4 for 1 Ti is not progress).  What is NOT obviously
    intended is that the scans in front of three of them still run every turn,
    and that `_siphon_deny` still WALKS a builder to a target it may not attack.

    Each test below drives BOTH verdicts by flipping the flag on the module
    object, which is what makes this a check rather than a characterisation of
    whatever the code happens to do: with QUIET off the melee fires, so the code
    under the flag is live and only the flag is holding it shut.
    """

    def setUp(self):
        self.quiet_modules = [m for m in (self.b.main, self.b.eco, self.b.raid)
                              if m is not None and hasattr(m, "LOKI_QUIET_ON")]
        self.assertTrue(self.quiet_modules, "LOKI_QUIET_ON not found in the tree")
        self._saved = [getattr(m, "LOKI_QUIET_ON") for m in self.quiet_modules]

    def tearDown(self):
        for m, v in zip(self.quiet_modules, self._saved):
            setattr(m, "LOKI_QUIET_ON", v)

    def _set_quiet(self, v):
        for m in self.quiet_modules:
            setattr(m, "LOKI_QUIET_ON", v)

    def _melee_world(self):
        w = L.World(20, 20, resources=500)
        w.add(EntityType.CORE, (2, 2), team=Team.A)
        me = w.add(EntityType.BUILDER_BOT, (5, 5), team=Team.A)
        w.add(EntityType.GUNNER, (5, 4), team=Team.B, direction=Direction.SOUTH)
        return w, me, w.controller(me)

    def test_sabotage_prio_is_CONSTANT_FALSE_while_QUIET_is_on(self):
        """FINDING: `_sabotage_prio` scans four tiles and can never act.

        Called from `_home_defend` and `_defend`, both on the action-cooldown-
        zero path, so the cost is up to 4 `get_tile_building_id` + 4
        `get_team` + 4 `get_entity_type` + 4 `can_fire` calls per defender turn
        for a branch that returns False by construction.
        """
        self.assertTrue(self.b.const("LOKI_QUIET_ON"),
                        "this test documents the SHIPPED configuration")
        w, me, ct = self._melee_world()
        p = L.make_player(self.b, core=Position(2, 2))
        self.assertFalse(p._sabotage_prio(ct),
                         "QUIET is on but the sabotage melee fired")
        self.assertEqual([e for e in w.log if e[0] == "fire"], [])

    def test_sabotage_prio_DOES_fire_with_QUIET_off(self):
        """The other verdict: the code under the flag is live, not rotten."""
        self._set_quiet(False)
        w, me, ct = self._melee_world()
        p = L.make_player(self.b, core=Position(2, 2))
        self.assertTrue(p._sabotage_prio(ct))
        self.assertEqual([(e[1].x, e[1].y) for e in w.log if e[0] == "fire"],
                         [(5, 4)])

    def _raid_setup(self, seat_at=None):
        E = Position(16, 16)
        w = L.World(24, 24, resources=500, rnd=100)
        w.add(EntityType.CORE, (2, 2), team=Team.A)
        w.add(EntityType.CORE, E, team=Team.B)
        seat = seat_at or Position(16, 15)
        me = w.add(EntityType.BUILDER_BOT, seat, team=Team.A)
        p = L.make_player(self.b, core=Position(2, 2), enemy=E, mw=24, mh=24)
        return w, me, w.controller(me), p, E

    def test_the_seat_peck_of_the_enemy_core_cannot_fire_while_QUIET_is_on(self):
        """FINDING: `_raid_act` step 1 is unreachable in the shipped build.

        A raider standing ON an enemy heal seat has an enemy Core tile at
        Manhattan-1 (asserted independently above), so the GEOMETRY is sound --
        this branch is shut by the flag, not by the `_try_fwd_barrier` defect.
        Both verdicts prove which.
        """
        w, me, ct, p, E = self._raid_setup()
        self.assertIn((me.pos.x, me.pos.y),
                      {(s.x, s.y) for s in self.seats(E, 24, 24)},
                      "the fixture did not actually put the raider on a seat")
        p._raid_act(ct, E, near=True)
        self.assertEqual([e for e in w.log if e[0] == "fire"], [],
                         "QUIET is on but the seat peck fired")

        w2, me2, ct2, p2, E2 = self._raid_setup()
        self._set_quiet(False)
        # block the seal branch so the peck is what we are measuring
        for d in CARDINALS:
            t = me2.pos.add(d)
            if (t.x, t.y) in {(s.x, s.y) for s in self.seats(E2, 24, 24)}:
                w2.add(EntityType.BARRIER, t, team=Team.A)
        p2._raid_act(ct2, E2, near=True)
        self.assertEqual(
            [(e[1].x, e[1].y) for e in w2.log if e[0] == "fire"],
            [(E2.x, E2.y)],
            "with QUIET off the seat peck must hit the adjacent enemy Core tile")

    def test_raid_peck_is_UNREACHABLE_from_its_only_call_site_while_QUIET_is_on(self):
        """FINDING: a 46-line ranked-melee function with no live caller.

        `_raid_peck` is called from exactly one place -- `_raid_act` step 6 --
        behind `not LOKI_QUIET_ON`.  Called directly it works (second half),
        so this is dead-by-flag, not dead-by-bug.
        """
        w, me, ct, p, E = self._raid_setup(seat_at=Position(10, 10))
        w.add(EntityType.CONVEYOR, (10, 11), team=Team.B, direction=Direction.SOUTH)
        p._ring(E)
        p._raid_act(ct, E, near=False)
        self.assertEqual([e for e in w.log if e[0] == "fire"], [],
                         "QUIET is on but _raid_act reached the peck")
        # direct call: the function itself is live
        self.assertTrue(p._raid_peck(ct, p.raid_seatkeys))
        self.assertEqual([(e[1].x, e[1].y) for e in w.log if e[0] == "fire"],
                         [(10, 11)])

    def test_raid_peck_ranks_a_seat_conveyor_above_a_plain_one(self):
        """The ranking still has to be right for the day QUIET is lifted."""
        w, me, ct, p, E = self._raid_setup(seat_at=Position(16, 14))
        p._ring(E)
        seat = Position(16, 15)
        self.assertIn((seat.x, seat.y), p.raid_seatkeys)
        w.add(EntityType.CONVEYOR, seat, team=Team.B, direction=Direction.SOUTH)
        w.add(EntityType.CONVEYOR, (15, 14), team=Team.B, direction=Direction.SOUTH)
        self.assertTrue(p._raid_peck(ct, p.raid_seatkeys))
        self.assertEqual([(e[1].x, e[1].y) for e in w.log if e[0] == "fire"],
                         [(seat.x, seat.y)],
                         "a plain belt outranked a belt standing on a heal seat")

    def test_siphon_deny_WALKS_to_a_belt_it_may_never_attack(self):
        """⚠ FINDING, and the most expensive of the four.

        Unlike the other QUIET branches this one is not merely a wasted scan:
        at d > 1 `_siphon_deny` sets `self.tgt` and calls `_nav`, spending the
        builder's MOVE to walk it to an enemy belt.  On arrival (d == 1) the
        QUIET branch returns False and the belt is never attacked, so the walk
        bought nothing.  `SIPHON_MAX_RNDS` eventually bans the tile and the
        builder picks the next one, so this repeats.
        """
        w = L.World(20, 20, resources=500, rnd=0)
        w.add(EntityType.CORE, (2, 2), team=Team.A)
        me = w.add(EntityType.BUILDER_BOT, (8, 8), team=Team.A)
        ct = w.controller(me)
        ct.omniscient = True
        w.add(EntityType.HARVESTER, (12, 8), team=Team.A)
        belt = Position(12, 9)
        w.add(EntityType.CONVEYOR, belt, team=Team.B, direction=Direction.SOUTH)
        grid = tuple("." * 20 for _ in range(20))
        p = L.make_player(self.b, core=Position(2, 2), mw=20, mh=20,
                          map_grid=grid, map_walls=set(), idx=0)

        # (a) far from the belt: the hunt CONSUMES the turn and walks
        self.assertTrue(p._siphon_deny(ct), "the siphon hunt did not engage")
        self.assertEqual((p.siphon_pos.x, p.siphon_pos.y), (belt.x, belt.y))
        self.assertTrue([e for e in w.log if e[0] == "move"],
                        "the siphon hunt claimed the turn without moving")

        # (b) standing beside it: the attack is refused and the turn is released
        me.pos = Position(12, 10)
        w.log.clear()
        self.assertFalse(p._siphon_deny(ct),
                         "QUIET is on but the siphon melee fired")
        self.assertEqual([e for e in w.log if e[0] == "fire"], [])

        # (c) the other verdict -- with QUIET off the arrival DOES kill the belt
        self._set_quiet(False)
        w.log.clear()
        self.assertTrue(p._siphon_deny(ct))
        self.assertEqual([(e[1].x, e[1].y) for e in w.log if e[0] == "fire"],
                         [(belt.x, belt.y)])


class TestPaveBanIsConstantNone(BotCase):
    """FINDING: `_pave_ban()` returns None unconditionally as shipped.

    `HS_SEAT_BAN_CONVEYORS = False`, so `_pave_ban` is `None` at all four of its
    call sites (`_link_path`, `_build_next_link`, `_l4_repair`, `_move`), and
    every `if ban is not None and ...` downstream is dead.  Intended (it is a
    flag) but worth a named test, because the `_seat_ban` machinery it wraps IS
    live and is used elsewhere -- so the two are easy to confuse when reading.
    """

    def test_pave_ban_is_None_as_shipped_and_a_real_set_when_the_flag_flips(self):
        p = L.make_player(self.b, core=Position(4, 4), mw=20, mh=20,
                          map_walls=set(), map_ores=[])
        self.assertFalse(self.b.const("HS_SEAT_BAN_CONVEYORS"),
                         "this test documents the SHIPPED configuration")
        self.assertIsNone(p._pave_ban())
        mods = [m for m in (self.b.eco, self.b.main, self.b.raid)
                if m is not None and hasattr(m, "HS_SEAT_BAN_CONVEYORS")]
        saved = [getattr(m, "HS_SEAT_BAN_CONVEYORS") for m in mods]
        try:
            for m in mods:
                setattr(m, "HS_SEAT_BAN_CONVEYORS", True)
            p2 = L.make_player(self.b, core=Position(4, 4), mw=20, mh=20,
                               map_walls=set(), map_ores=[])
            ban = p2._pave_ban()
            self.assertIsNotNone(ban)
            self.assertTrue(ban, "with the flag on the ban is still empty")
        finally:
            for m, v in zip(mods, saved):
                setattr(m, "HS_SEAT_BAN_CONVEYORS", v)


# ===========================================================================
# 12.  MAP TABLE HELPERS
# ===========================================================================

class TestMapTableHelpers(BotCase):

    def test_enemy_core_for_is_an_involution_on_every_CORE_PAIRS_row(self):
        f = self.b.fn("enemy_core_for")
        pairs = self.b.const("CORE_PAIRS")
        self.assertTrue(pairs, "CORE_PAIRS is empty")
        for mw, mh, ax, ay, bx, by in pairs:
            a, bb = Position(ax, ay), Position(bx, by)
            self.assertEqual(f(mw, mh, a), bb, f"{mw}x{mh} A->B")
            self.assertEqual(f(mw, mh, bb), a, f"{mw}x{mh} B->A")

    def test_enemy_core_for_falls_back_to_point_reflection_off_table(self):
        f = self.b.fn("enemy_core_for")
        own = Position(3, 4)
        got = f(31, 29, own)          # a size that is not in the table
        self.assertEqual(got, Position(31 - 2 - 3, 29 - 2 - 4))
        self.assertEqual(f(31, 29, got), own, "the fallback is not an involution")

    def test_known_map_for_returns_None_off_table_and_a_well_formed_grid_on_it(self):
        f = self.b.fn("known_map_for")
        self.assertIsNone(f(31, 29, Position(3, 4)), "an unknown map returned a grid")
        codes = self.b.const("MAP_CODES")
        alphabet = self.b.const("MAP_ALPHABET")
        hits = 0
        for (mw, mh, ax, ay, bx, by) in list(codes.keys())[:6]:
            for own in (Position(ax, ay), Position(bx, by)):
                grid = f(mw, mh, own)
                self.assertIsNotNone(grid, f"{mw}x{mh} from {own} decoded to None")
                self.assertEqual(len(grid), mh)
                for row in grid:
                    self.assertEqual(len(row), mw)
                    self.assertTrue(set(row) <= set(".#o"), f"bad chars: {set(row)}")
                hits += 1
        self.assertGreater(hits, 0)
        self.assertEqual(len(set(alphabet)), len(alphabet), "MAP_ALPHABET repeats")

    def test_known_map_for_puts_the_core_anchor_on_walkable_ground(self):
        """A decode that lands a wall on our own Core anchor is a decode bug."""
        f = self.b.fn("known_map_for")
        for (mw, mh, ax, ay, bx, by) in list(self.b.const("MAP_CODES").keys())[:8]:
            for own in (Position(ax, ay), Position(bx, by)):
                grid = f(mw, mh, own)
                if grid is None:
                    continue
                for c in self.tiles(own):
                    self.assertNotEqual(
                        grid[c.y][c.x], "#",
                        f"{mw}x{mh}: decoded a WALL on Core tile {c}")

    def test_pave_blocked_by_ore_fails_CLOSED_out_of_vision(self):
        f = self.b.fn("pave_blocked_by_ore")
        w = L.World(20, 20, ore=[(6, 5)])
        me = w.add(EntityType.BUILDER_BOT, (6, 6), team=Team.A)
        ct = w.controller(me)
        self.assertTrue(f(ct, Position(6, 5)), "ore tile not reported as blocked")
        self.assertFalse(f(ct, Position(6, 7)), "an empty visible tile read as blocked")
        self.assertTrue(f(ct, Position(19, 19)), "an out-of-vision tile failed OPEN")
        self.assertTrue(f(ct, Position(-1, -1)), "an off-map tile failed OPEN")

    def test_pave_blocked_honours_the_ban_set_and_both_verdicts(self):
        f = self.b.fn("pave_blocked")
        w = L.World(20, 20)
        me = w.add(EntityType.BUILDER_BOT, (6, 6), team=Team.A)
        ct = w.controller(me)
        self.assertFalse(f(ct, Position(6, 7), None))
        self.assertTrue(f(ct, Position(6, 7), frozenset({(6, 7)})))
        self.assertFalse(f(ct, Position(6, 7), frozenset({(1, 1)})))


# ===========================================================================
# 13.  THE TRUNK CHAIN AND HOME DEFENCE -- the rest of the GT-1 surface
# ===========================================================================

class TestTrunkChainGeometry(BotCase):

    def _w(self, ti=500):
        w = L.World(20, 20, resources=ti)
        w.add(EntityType.CORE, (2, 2), team=Team.A)
        me = w.add(EntityType.BUILDER_BOT, (6, 6), team=Team.A)
        ct = w.controller(me)
        ct.omniscient = True
        return w, me, ct

    def _p(self, queue, **kw):
        return L.make_player(self.b, core=Position(2, 2), mw=20, mh=20,
                             link_queue=list(queue), map_walls=set(),
                             map_ores=[], **kw)

    def test_build_next_link_lays_only_a_MANHATTAN_1_tile(self):
        """GT-1 again, on the economy's hot loop.  BOTH verdicts."""
        w, me, ct = self._w()
        p = self._p([Position(6, 7)])
        self.assertTrue(p._build_next_link(ct), "the adjacent link was not laid")
        self.assertEqual([(e[1], (e[2].x, e[2].y)) for e in w.log if e[0] == "build"],
                         [(EntityType.CONVEYOR, (6, 7))])
        # Manhattan-2 -> refused, and the queue is NOT consumed
        w2, me2, ct2 = self._w()
        p2 = self._p([Position(6, 8)])
        self.assertFalse(p2._build_next_link(ct2))
        self.assertEqual(len(p2.link_queue), 1, "a refused link was popped anyway")
        # diagonal -> also refused (Manhattan-2)
        w3, me3, ct3 = self._w()
        self.assertFalse(self._p([Position(7, 7)])._build_next_link(ct3))

    def test_build_next_link_refuses_the_tile_it_is_standing_on(self):
        w, me, ct = self._w()
        p = self._p([Position(6, 6)])
        self.assertFalse(p._build_next_link(ct),
                         "tried to build under its own feet -- GT-1 excludes the "
                         "own tile")
        self.assertEqual([e for e in w.log if e[0] == "build"], [])

    def test_build_next_link_pops_a_tile_that_is_already_occupied(self):
        w, me, ct = self._w()
        w.add(EntityType.CONVEYOR, (6, 7), team=Team.A, direction=Direction.WEST)
        p = self._p([Position(6, 7), Position(6, 5)])
        self.assertTrue(p._build_next_link(ct))
        self.assertEqual([(e[2].x, e[2].y) for e in w.log if e[0] == "build"],
                         [(6, 5)], "the occupied head was not skipped")

    def test_build_next_link_refuses_when_the_bank_cannot_pay(self):
        w, me, ct = self._w(ti=0)
        self.assertFalse(self._p([Position(6, 7)])._build_next_link(ct))

    def test_wire_tick_drops_a_pending_tile_once_it_has_an_acceptor(self):
        w, me, ct = self._w()
        w.add(EntityType.CONVEYOR, (7, 7), team=Team.A, direction=Direction.EAST)
        p = self._p([], wire_pending=[(Position(6, 7), 0)])
        p._wire_tick(ct)
        self.assertEqual(p.wire_pending, [], "a wired tile stayed on the queue")
        # the other verdict: no acceptor and inside the window -> it stays
        w2, me2, ct2 = self._w()
        p2 = self._p([Position(1, 1)], wire_pending=[(Position(6, 7), 0)])
        p2._wire_tick(ct2)
        self.assertEqual(len(p2.wire_pending), 1)

    def test_sync_harvesters_publishes_a_monotone_count_and_the_ready_flag(self):
        w, me, ct = self._w()
        p = self._p([])
        me.pos = Position(4, 4)
        need = self.b.const("ECO_NEED")
        for i in range(need):
            w.add(EntityType.HARVESTER, (6 + i, 4), team=Team.A)
        p._sync_harvesters(ct)
        w.commit_store()
        self.assertEqual(ct.read_store(self.b.const("SLOT_HARVESTERS")), need)
        self.assertEqual(ct.read_store(self.b.const("SLOT_ECO_READY")), 1)
        # monotone: a lower live count must NOT lower the published one
        for e in [e for e in w.ents.values() if e.etype == EntityType.HARVESTER]:
            w.remove(e.eid)
        p._sync_harvesters(ct)
        w.commit_store()
        self.assertEqual(ct.read_store(self.b.const("SLOT_HARVESTERS")), need)

    def test_step_off_link_only_ever_moves_in_a_CARDINAL(self):
        """GT-7.  It seeds its candidate list from `cardinal_direction_to`, which
        can return CENTRE -- so the loop must skip it or `move` raises and the
        engine deletes the unit."""
        for tgt in (Position(6, 6), Position(2, 2), Position(19, 19)):
            w, me, ct = self._w()
            p = self._p([Position(6, 6), tgt])
            w.log.clear()
            p._step_off_link(ct)
            for entry in w.log:
                if entry[0] == "move":
                    self.assertIn(entry[1], CARDINALS, f"moved {entry[1]}")

    def test_step_off_link_returns_False_when_completely_boxed_in(self):
        w, me, ct = self._w()
        for d in CARDINALS:
            w.add(EntityType.BARRIER, me.pos.add(d), team=Team.A)
        self.assertFalse(self._p([])._step_off_link(ct))


class TestHomeDefenceGeometry(BotCase):

    def test_nearest_home_intruder_respects_the_band_the_team_and_the_type(self):
        w = L.World(30, 30)
        w.add(EntityType.CORE, (2, 2), team=Team.A)
        me = w.add(EntityType.BUILDER_BOT, (5, 5), team=Team.A)
        ct = w.controller(me)
        ct.omniscient = True
        p = L.make_player(self.b, core=Position(2, 2), mw=30, mh=30)
        self.assertIsNone(p._nearest_home_intruder(ct))
        w.add(EntityType.BUILDER_BOT, (25, 25), team=Team.B)
        self.assertIsNone(p._nearest_home_intruder(ct), "an intruder outside d^2=36 "
                                                        "of the Core was reported")
        w.add(EntityType.GUNNER, (4, 4), team=Team.B, direction=Direction.EAST)
        self.assertIsNone(p._nearest_home_intruder(ct), "a TURRET was reported as a "
                                                        "builder intruder")
        w.add(EntityType.BUILDER_BOT, (6, 6), team=Team.A)
        self.assertIsNone(p._nearest_home_intruder(ct), "a FRIENDLY body was reported")
        w.add(EntityType.BUILDER_BOT, (4, 3), team=Team.B)
        self.assertEqual(p._nearest_home_intruder(ct), Position(4, 3))

    def test_nearest_home_intruder_picks_the_one_nearest_to_US_not_to_the_core(self):
        w = L.World(30, 30)
        w.add(EntityType.CORE, (2, 2), team=Team.A)
        me = w.add(EntityType.BUILDER_BOT, (7, 7), team=Team.A)
        ct = w.controller(me)
        ct.omniscient = True
        w.add(EntityType.BUILDER_BOT, (2, 4), team=Team.B)   # nearer the Core
        w.add(EntityType.BUILDER_BOT, (6, 6), team=Team.B)   # nearer to us
        p = L.make_player(self.b, core=Position(2, 2), mw=30, mh=30)
        self.assertEqual(p._nearest_home_intruder(ct), Position(6, 6))

    def test_a_launcher_is_never_planted_on_one_of_the_eight_heal_seats(self):
        """A launcher is bot-impassable, so one on a seat costs +4 HP/round forever.

        BOTH verdicts: standing beside only-seats builds nothing; one non-seat
        neighbour and it builds there.
        """
        core = Position(4, 4)
        seats = {(s.x, s.y) for s in self.seats(core)}
        stand = Position(4, 3)      # a seat itself: its N/E/W neighbours are ring
        w = L.World(20, 20, resources=5000,
                    rnd=self.b.const("LAUNCHER_MIN_RND"))
        w.add(EntityType.CORE, core, team=Team.A)
        me = w.add(EntityType.BUILDER_BOT, stand, team=Team.A)
        ct = w.controller(me)
        ct.omniscient = True
        w.store[Team.A][self.b.const("SLOT_HARVESTERS")] = 9
        w.store[Team.A][self.b.const("SLOT_ECO_READY")] = 1
        p = L.make_player(self.b, core=core, mw=20, mh=20)
        p._try_build_launcher(ct)
        planted = [(e.pos.x, e.pos.y) for e in w.ents.values()
                   if e.etype == EntityType.LAUNCHER]
        self.assertFalse(set(planted) & seats,
                         f"a launcher was planted on a heal seat: {planted}")
        self.assertTrue(planted, "the launcher was never built at all -- this test "
                                 "would pass vacuously")

    def test_the_launcher_is_refused_before_LAUNCHER_MIN_RND(self):
        """The other verdict for the deferral gate that made the test above
        pass vacuously on the first attempt."""
        core = Position(4, 4)
        w = L.World(20, 20, resources=5000,
                    rnd=self.b.const("LAUNCHER_MIN_RND") - 1)
        w.add(EntityType.CORE, core, team=Team.A)
        me = w.add(EntityType.BUILDER_BOT, (4, 3), team=Team.A)
        ct = w.controller(me)
        ct.omniscient = True
        w.store[Team.A][self.b.const("SLOT_HARVESTERS")] = 9
        p = L.make_player(self.b, core=core, mw=20, mh=20)
        self.assertFalse(p._try_build_launcher(ct))

    def test_try_build_launchers_prose_is_a_STRAY_STRING_not_a_docstring(self):
        """⚠ FINDING (cosmetic + a hot-path no-op).

        `_try_build_launcher` opens with ~20 lines of `#` comment, then a
        `return False` gate, and ONLY THEN the triple-quoted prose -- so Python
        parses that prose as a plain expression statement, not a docstring.
        `__doc__` is None (so it is invisible to `help()`, to `inspect.getdoc`
        and to any doc tooling) and the string object is evaluated on every call
        that gets past the round gate.  Harmless, and exactly the kind of thing
        that is never noticed without an assertion.
        """
        self.assertIsNone(
            self.b.Player._try_build_launcher.__doc__,
            "the prose is now a real docstring -- finding resolved, delete this")
        # control: a neighbouring method in the same class DOES carry its prose
        self.assertIsNotNone(self.b.Player._sabotage_prio.__doc__,
                             "the control method lost its docstring too, so this "
                             "test no longer discriminates")


class TestPureHelpersOnThisArm(BotCase):
    """`test_bot_helpers.py` covers these against its own default arm; these run
    against whatever `BOT=` points at, so an arm swap cannot skip them."""

    def test_nearest_cardinal_is_total_and_lands_only_on_cardinals(self):
        f = self.b.fn("nearest_cardinal")
        for d in Direction:
            got = f(d)
            self.assertIn(got, CARDINALS, f"{d} -> {got}, which is not cardinal")
        for d in CARDINALS:
            self.assertEqual(f(d), d, "not the identity on a cardinal")

    def test_nearest_core_tile_always_returns_a_real_footprint_tile(self):
        f = self.b.fn("nearest_core_tile")
        o = Position(5, 9)
        foot = {(t.x, t.y) for t in self.tiles(o)}
        for x in range(0, 16):
            for y in range(0, 16):
                got = f(Position(x, y), o)
                self.assertIn((got.x, got.y), foot)

    def test_ring_is_the_square_annulus_minus_its_own_centre(self):
        f = self.b.fn("ring")
        o = Position(9, 9)
        for r in (1, 2, 3):
            got = f(o, r)
            self.assertEqual(len(got), (2 * r + 1) ** 2 - 1)
            self.assertEqual(len(set(got)), len(got), "duplicates")
            self.assertNotIn(o, got)

    def test_pack_unpack_round_trips_over_the_whole_legal_board(self):
        pack, unpack = self.b.fn("pack_pos"), self.b.fn("unpack_pos")
        seen = {}
        for x in range(32):
            for y in range(32):
                p = Position(x, y)
                v = pack(p)
                self.assertEqual(unpack(v), p)
                self.assertNotIn(v, seen, f"{p} collides with {seen.get(v)}")
                seen[v] = p
        self.assertIsNone(unpack(0), "0 must decode as 'nothing stored'")


class TestDebugLoggingFlags(BotCase):
    """⚠ FINDING: `LOKI_L4_LOG` ships ON while its two siblings ship OFF.

    `_l4_repair` prints an f-string to stdout on every successful repair.  Two
    costs, both inside the 10 ms turn budget: the format and the write.  And per
    CLAUDE.md the platform STRIPS stdout from downloaded replays (30,664 of
    30,664 `BotOutput` events carry an empty `stdout`), so the line is
    unreadable exactly where it would be used.  `LOKI_SALTIDLE_LOG` and
    `LOKI_SALT_LOG` are both False, which is what makes this look left-on rather
    than chosen.
    """

    def test_the_L4_repair_log_flag_is_on_and_actually_prints(self):
        self.assertTrue(self.b.const("LOKI_L4_LOG"),
                        "LOKI_L4_LOG is now off -- delete this test, the finding "
                        "is resolved")
        for sibling in ("LOKI_SALTIDLE_LOG", "LOKI_SALT_LOG"):
            self.assertFalse(self.b.const(sibling),
                             f"{sibling} is now ON too -- re-read the finding")

        w = L.World(20, 20, resources=500)
        w.add(EntityType.CORE, (2, 2), team=Team.A)
        me = w.add(EntityType.BUILDER_BOT, (6, 6), team=Team.A)
        ct = w.controller(me)
        ct.omniscient = True
        w.add(EntityType.CONVEYOR, (5, 7), team=Team.A, direction=Direction.EAST)
        w.add(EntityType.CONVEYOR, (6, 8), team=Team.A, direction=Direction.SOUTH)
        p = L.make_player(self.b, core=Position(2, 2), enemy=Position(18, 18),
                          mw=20, mh=20, map_walls=set(), map_ores=[])
        with redirect_stderr(io.StringIO()), redirect_stdout(io.StringIO()) as out:
            self.assertTrue(p._l4_repair(ct))
        self.assertIn("L4REPAIR", out.getvalue(),
                      "the flag is on but nothing was printed")


if __name__ == "__main__":
    unittest.main()
