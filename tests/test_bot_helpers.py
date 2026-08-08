#!/usr/bin/env python3
"""Unit tests for the LIVE bot's pure helpers.

Run:  .venv/bin/python -m unittest discover -s tests -v
Point at another bot:  BOT=bots/_v99mag .venv/bin/python -m unittest discover -s tests

WHAT THIS FILE IS FOR, and what it deliberately is not.

main.py is ~5,000 lines in one class with a 411-line `_builder` and a 314-line
`_core`. Almost none of that is unit-testable: it is stateful, it reads the world
through a live Controller, and its correctness is "does the bot win", which no
assertion can express. **Do not try to unit-test the turn logic.** The instrument
for that already exists and is better: `tools/det.py` runs paired identical
(map, seed, seat) triples and reports FLIPS and identical-end-state rate, so a
refactor that is meant to change nothing is PROVEN by a 0-flip / 100%-identical
run against its parent. That is a characterization test, and the parent's
behaviour is the spec.

What IS unit-testable is the pure layer: 11 of the 13 top-level helpers are
plain math on positions and map dimensions, with no `ct` and no `self`. That
layer is small, it is called from inside the hot path, and it is exactly where
this project's silent bugs have lived — arithmetic that looks right, is wrong,
and produces a plausible table instead of a crash. Two on the tape:

  - a prescription was built on a d^2=41 hunt band without noticing that builder
    vision is r^2=20, so the band could never be observed. Pure arithmetic, wrong,
    invisible until someone re-derived it by hand.
  - v86 hand-inlined `dist_core` into four `abs()` expressions for speed. That is
    a correct-looking rewrite of a correct function, and nothing in the project
    would have caught it if a sign were flipped. `test_dist_core_matches_naive`
    below is that test, written against the definition rather than the rewrite.

So: pure helpers get unit tests here; stateful turn logic gets det identity runs.
Anything that cannot be reached by either is a reason to extract a pure helper,
not a reason to write a mock.
"""
import importlib.util
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOT = Path(os.environ.get("BOT", "bots/_v89sh"))
BOT_MAIN = ROOT / BOT / "main.py"

from fcode import Direction, Position  # noqa: E402


def _load_bot():
    sys.path.insert(0, str(ROOT / BOT))
    spec = importlib.util.spec_from_file_location("livebot", BOT_MAIN)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@unittest.skipUnless(BOT_MAIN.exists(), f"{BOT} not present")
class TestPureHelpers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b = _load_bot()

    # ---- position packing: used for the 16-slot comms store -----------------
    # A packing bug here is silent and team-wide: every unit reads the corrupted
    # value for the whole round and nothing raises.

    def test_pack_unpack_round_trips_over_the_whole_legal_board(self):
        # Maps run 8x8 to 30x30, so cover past the largest legal coordinate.
        for x in range(0, 32):
            for y in range(0, 32):
                p = Position(x, y)
                self.assertEqual(
                    self.b.unpack_pos(self.b.pack_pos(p)), p,
                    f"pack/unpack lost {p} — every unit would read a corrupted "
                    f"position from the comms store for a whole round",
                )

    def test_packed_positions_are_distinct(self):
        seen = {}
        for x in range(32):
            for y in range(32):
                v = self.b.pack_pos(Position(x, y))
                self.assertNotIn(v, seen, f"{Position(x,y)} collides with {seen.get(v)}")
                seen[v] = Position(x, y)

    # ---- core geometry ------------------------------------------------------

    def test_core_tiles_is_the_2x2_footprint(self):
        o = Position(4, 7)
        self.assertEqual(
            sorted(self.b.core_tiles(o)),
            sorted([Position(4, 7), Position(5, 7), Position(4, 8), Position(5, 8)]),
        )

    def test_dist_core_matches_naive(self):
        """Guards hand-inlined rewrites of dist_core against its definition.

        v86 replaced the generator over core_tiles() with four inlined abs()
        expressions for speed. This asserts any such rewrite still equals the
        definition — Chebyshev distance to the nearest of the 2x2 core tiles.
        """
        def naive(pos, o):
            return min(max(abs(pos.x - c.x), abs(pos.y - c.y))
                       for c in self.b.core_tiles(o))

        for ox in range(0, 12):
            for oy in range(0, 12):
                o = Position(ox, oy)
                for px in range(0, 16):
                    for py in range(0, 16):
                        p = Position(px, py)
                        self.assertEqual(
                            self.b.dist_core(p, o), naive(p, o),
                            f"dist_core disagrees with its definition at "
                            f"pos={p} core={o}",
                        )

    def test_dist_core_is_zero_on_the_footprint_and_one_beside_it(self):
        o = Position(5, 5)
        for c in self.b.core_tiles(o):
            self.assertEqual(self.b.dist_core(c, o), 0)
        # Footprint is (5,5),(6,5),(5,6),(6,6) — so (7,5) is ADJACENT to (6,5)
        # and reads 1, not 2. Getting this wrong in the test on the first pass
        # is the argument for the differential test above: it checks the
        # function against its definition rather than against my arithmetic.
        self.assertEqual(self.b.dist_core(Position(4, 5), o), 1)
        self.assertEqual(self.b.dist_core(Position(7, 5), o), 1)
        self.assertEqual(self.b.dist_core(Position(8, 5), o), 2)

    def test_nearest_core_tile_returns_an_actual_core_tile(self):
        o = Position(3, 9)
        tiles = set(self.b.core_tiles(o))
        for px in range(0, 14):
            for py in range(0, 14):
                self.assertIn(self.b.nearest_core_tile(Position(px, py), o), tiles)

    # ---- heal seats: the 8 tiles around the core ----------------------------
    # "Free the core's 8 heal seats" is a measured lever on the tape (8 free
    # seats = 32 HP/rnd against a max measured siege DPS of 23.22), so the seat
    # set being right is load-bearing.

    def test_heal_seats_are_eight_distinct_tiles_adjacent_to_the_footprint(self):
        o = Position(6, 6)
        seats = self.b.heal_seats(o, 20, 20)
        self.assertEqual(len(seats), 8)
        self.assertEqual(len(set(seats)), 8, "duplicate heal seats")
        foot = set(self.b.core_tiles(o))
        for s in seats:
            self.assertNotIn(s, foot, "a heal seat sits ON the core footprint")
            self.assertEqual(self.b.dist_core(s, o), 1)

    def test_heal_seats_are_clipped_to_the_map(self):
        # Core in the northwest corner: seats off the board must be dropped,
        # not returned as negative coordinates.
        seats = self.b.heal_seats(Position(0, 0), 20, 20)
        for s in seats:
            self.assertGreaterEqual(s.x, 0)
            self.assertGreaterEqual(s.y, 0)
            self.assertLess(s.x, 20)
            self.assertLess(s.y, 20)

    # ---- misc pure helpers --------------------------------------------------

    def test_nearest_cardinal_maps_every_direction_to_a_cardinal(self):
        cards = {Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST}
        for d in Direction:
            self.assertIn(self.b.nearest_cardinal(d), cards,
                          f"{d} did not map to a cardinal — builder bots can only "
                          f"move N/E/S/W and move(<diagonal>) raises GameError")

    def test_nearest_cardinal_is_identity_on_cardinals(self):
        for d in (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST):
            self.assertEqual(self.b.nearest_cardinal(d), d)

    def test_ring_excludes_its_own_origin_and_is_symmetric(self):
        o = Position(9, 9)
        r = self.b.ring(o, 2)
        self.assertNotIn(o, r)
        self.assertEqual(len(r), len(set(r)), "ring contains duplicates")
        # A ring about a centre should be symmetric under reflection.
        mirrored = {Position(2 * o.x - p.x, p.y) for p in r}
        self.assertEqual(set(r), mirrored, "ring is not left-right symmetric")

    def test_enemy_core_is_the_mirror_of_our_own(self):
        """Maps are symmetric by reflection or rotation, so this must invert."""
        w, h = 24, 24
        own = Position(3, 3)
        enemy = self.b.enemy_core_for(w, h, own)
        self.assertNotEqual(enemy, own)
        # Applying it to the enemy core must return our own.
        self.assertEqual(self.b.enemy_core_for(w, h, enemy), own)


if __name__ == "__main__":
    unittest.main()
