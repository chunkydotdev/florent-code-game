#!/usr/bin/env python3
"""A generic DEAD-GUARD detector for the live bot's predicates.

Run:  .venv/bin/python -m unittest discover -s tests -v
Point at another arm:  BOT=bots/_v230sent41 .venv/bin/python -m unittest discover -s tests
See the full sweep:    LIVENESS_REPORT=1 .venv/bin/python -m unittest tests.test_predicate_liveness

WHAT THIS IS.  For each predicate it can call, the harness enumerates a bounded
synthetic input space and records whether the predicate ever returned True and
whether it ever returned False.  Anything CONSTANT across its whole space is
reported as a SUSPECTED DEAD GUARD.

⛔⛔ THE EPISTEMIC ASYMMETRY, AND IT IS THE WHOLE REASON THIS FILE NEEDS A
DOCSTRING RATHER THAN JUST A TEST.

  * FINDING BOTH VERDICTS IS PROOF.  If a predicate returned True on one input
    and False on another, it is live.  Nothing about the sampling can take that
    back -- a witness is a witness.

  * FINDING ONE VERDICT IS NOT PROOF OF ANYTHING.  A predicate that is constant
    over this space may be perfectly live over the real one; the space may
    simply be too small, or miss the axis that matters.  The harness therefore
    says **"never observed to return X over N inputs"** and never
    "unsatisfiable", "impossible" or "dead".  `test_the_report_wording_stays_
    honest` asserts that in the string itself, because the temptation to
    upgrade a suspicion into a finding is exactly what put a
    "dose-verified, cert-clean" tree with an empty satisfying set on the tape.

  So: a green run of this file is EVIDENCE OF LIVENESS for everything it
  cleared, and a QUEUE OF THINGS TO READ for everything it flagged.  Only a
  human read of the code turns a flag into a defect.

THE THREE DEFECTS THIS SHAPE PRODUCED ON 2026-08-15, all of which this harness
would have surfaced as flags:
  1. `_v230sent41._try_fwd_barrier` -- needed a tile both cardinal-adjacent to
     the raider and Manhattan-1 from the sentinel; after a plant every such
     tile is Manhattan-2.  Empty satisfying set.
  2. a gunner-ray guard calling `can_fire_from(..., GUNNER, <the empty build
     tile>)` -- False on every empty tile, so it could never veto.
  3. a turret priority table that ranked CORE 0 and HARVESTER 5 and so never
     selected the harvester it was sequenced to kill.

VALIDATING THE DETECTOR.  A detector that has never flagged anything has not
been seen to detect.  `TestTheHarnessItself` feeds it four synthetic controls --
a dead conjunction, a dead disjunction, a live predicate, and a live-but-rare
predicate -- and asserts it flags exactly the two dead ones.  The rare control
is the one that matters: it proves the rule is "never observed", not "observed
seldom".  A fifth control is live only OUTSIDE the sampled space and is flagged,
which is the asymmetry above made executable.
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
HAVE_BOT = (L.BOT_DIR / "main.py").exists()
REPORT = bool(os.environ.get("LIVENESS_REPORT"))


def setUpModule():
    global BOT
    if HAVE_BOT:
        BOT = L.load_bot()


# ===========================================================================
# THE HARNESS
# ===========================================================================

LIVE = "live"                      # must return both verdicts
CONST_TRUE = "constant_true"       # known-total; assert it stays constant TRUE
CONST_FALSE = "constant_false"     # known-dead; assert it stays constant FALSE


class Verdict:
    """What one bounded sweep of one predicate saw."""

    __slots__ = ("name", "n", "trues", "falses", "errors",
                 "witness_true", "witness_false", "first_error", "expect")

    def __init__(self, name, expect):
        self.name = name
        self.expect = expect
        self.n = self.trues = self.falses = self.errors = 0
        self.witness_true = self.witness_false = self.first_error = None

    def record(self, case, value):
        self.n += 1
        if value:
            self.trues += 1
            if self.witness_true is None:
                self.witness_true = case
        else:
            self.falses += 1
            if self.witness_false is None:
                self.witness_false = case

    def record_error(self, case, exc):
        self.n += 1
        self.errors += 1
        if self.first_error is None:
            self.first_error = (case, repr(exc))

    @property
    def evaluated(self):
        return self.n - self.errors

    @property
    def is_live(self):
        """PROVEN live: a True witness and a False witness both exist."""
        return self.trues > 0 and self.falses > 0

    @property
    def flagged(self):
        return not self.is_live

    def message(self):
        """⛔ Wording is load-bearing.  See `test_the_report_wording_stays_honest`.

        A constant sweep is a SUSPICION -- 'never observed', with the sample
        size attached so a reader can judge it.  It is never phrased as proof.
        """
        if self.evaluated == 0:
            return (f"{self.name}: NEVER EVALUATED -- all {self.n} inputs raised. "
                    f"first: {self.first_error}")
        if self.is_live:
            return (f"{self.name}: LIVE (proven) -- True at {self.witness_true}, "
                    f"False at {self.witness_false}; {self.evaluated} inputs")
        missing = "False" if self.falses == 0 else "True"
        seen = "True" if self.falses == 0 else "False"
        witness = self.witness_true if self.falses == 0 else self.witness_false
        return (f"{self.name}: SUSPECTED DEAD GUARD -- never observed to return "
                f"{missing} over {self.evaluated} inputs (always {seen}, e.g. at "
                f"{witness}). This is a suspicion, not a proof: the space may be "
                f"too small. Read the code.")


def sweep(name, predicate, cases, expect=LIVE, verdict=bool):
    """Run `predicate` over `cases` and report which verdicts were observed.

    `verdict` maps the return value onto a boolean, so a predicate that returns
    a count or None-or-a-value can still be swept on the question that matters
    (`is not None`, `> 0`, ...).  State the question in the cell NAME.
    """
    v = Verdict(name, expect)
    for case in cases:
        try:
            v.record(case, verdict(predicate(case)))
        except Exception as exc:      # an exception is not a verdict
            v.record_error(case, exc)
    return v


# ===========================================================================
# 1.  VALIDATING THE DETECTOR
# ===========================================================================

@unittest.skipUnless(HAVE_BOT, f"{L.BOT} not present")
class TestTheHarnessItself(unittest.TestCase):

    SPACE = [Position(x, y) for x in range(-4, 5) for y in range(-4, 5)]

    def test_it_flags_a_dead_conjunction(self):
        """The `_try_fwd_barrier` shape in miniature: two conditions that
        cannot hold at once, so the satisfying set is empty."""
        origin = Position(0, 0)
        v = sweep("control.dead_conjunction",
                  lambda p: manhattan(p, origin) == 1 and manhattan(p, origin) == 2,
                  self.SPACE)
        self.assertTrue(v.flagged, "a provably empty conjunction was NOT flagged")
        self.assertEqual(v.trues, 0)
        self.assertIn("never observed to return True", v.message())

    def test_it_flags_a_dead_disjunction(self):
        origin = Position(0, 0)
        v = sweep("control.dead_disjunction",
                  lambda p: manhattan(p, origin) >= 0 or p.x > 99, self.SPACE)
        self.assertTrue(v.flagged, "a constant-TRUE guard was NOT flagged")
        self.assertEqual(v.falses, 0)
        self.assertIn("never observed to return False", v.message())

    def test_it_does_NOT_flag_a_live_predicate(self):
        origin = Position(0, 0)
        v = sweep("control.live", lambda p: manhattan(p, origin) == 1, self.SPACE)
        self.assertFalse(v.flagged, f"a live predicate was flagged: {v.message()}")
        self.assertTrue(v.is_live)
        self.assertIn("LIVE (proven)", v.message())

    def test_it_does_NOT_flag_a_live_but_RARE_predicate(self):
        """The control that proves the rule is 'never observed', not 'observed
        seldom'.  A frequency threshold would flag this and be wrong."""
        v = sweep("control.rare",
                  lambda p: p.x == 4 and p.y == 4, self.SPACE)
        self.assertEqual(v.trues, 1, "the fixture is not actually 1-in-81")
        self.assertFalse(v.flagged, "a 1-in-81 live predicate was flagged as dead")

    def test_it_flags_a_predicate_that_is_live_only_OUTSIDE_the_sampled_space(self):
        """⛔ THE ASYMMETRY, executable.

        This predicate IS satisfiable -- at x == 50 -- and the harness still
        flags it, because the space stops at 4.  That is correct behaviour and
        it is exactly why a flag is a suspicion and never a proof.  The same
        sweep widened to include 50 clears it.
        """
        v = sweep("control.outside_space", lambda p: p.x == 50, self.SPACE)
        self.assertTrue(v.flagged)
        wider = self.SPACE + [Position(50, 0)]
        v2 = sweep("control.outside_space.wider", lambda p: p.x == 50, wider)
        self.assertFalse(v2.flagged,
                         "widening the space did not clear a satisfiable predicate "
                         "-- the harness is not measuring what it claims")

    def test_it_reports_a_predicate_that_never_evaluated_at_all(self):
        def boom(p):
            raise RuntimeError("no")

        v = sweep("control.always_raises", boom, self.SPACE)
        self.assertEqual(v.evaluated, 0)
        self.assertIn("NEVER EVALUATED", v.message())
        self.assertTrue(v.flagged)

    def test_the_report_wording_stays_honest(self):
        """A flag must never be phrased as proof of impossibility."""
        origin = Position(0, 0)
        msg = sweep("w", lambda p: manhattan(p, origin) == 1 and
                    manhattan(p, origin) == 2, self.SPACE).message()
        self.assertIn("never observed", msg)
        self.assertIn("suspicion, not a proof", msg)
        for banned in ("unsatisfiable", "impossible", "cannot be", "proves"):
            self.assertNotIn(banned, msg.lower(),
                             f"the flag message claims more than a bounded sweep "
                             f"can support: {banned!r}")


# ===========================================================================
# 2.  THE REGISTRY -- one cell per predicate
# ===========================================================================

def _mk(bot, **kw):
    kw.setdefault("core", Position(2, 2))
    kw.setdefault("mw", 24)
    kw.setdefault("mh", 24)
    return L.make_player(bot, **kw)


def _base_world(ti=500, rnd=100, mw=24, mh=24):
    w = L.World(mw, mh, resources=ti, rnd=rnd)
    w.add(EntityType.CORE, (2, 2), team=Team.A)
    w.add(EntityType.CORE, (18, 18), team=Team.B)
    return w


# --- neighbourhood case generator -------------------------------------------
# Four orthogonal neighbours, each drawn from a small alphabet of contents.
# 4^4 = 256 configurations, which is the whole space these predicates read.

NBR_KINDS = (
    None,
    ("own_conveyor", EntityType.CONVEYOR, Team.A, Direction.EAST),
    ("enemy_conveyor", EntityType.CONVEYOR, Team.B, Direction.EAST),
    ("own_barrier", EntityType.BARRIER, Team.A, None),
)


def _nbr_cases():
    out = []
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    out.append((a, b, c, d))
    return out


def _build_nbrs(w, centre, code):
    for d, k in zip(CARDINALS, code):
        kind = NBR_KINDS[k]
        if kind is None:
            continue
        _, etype, team, facing = kind
        w.add(etype, centre.add(d), team=team, direction=facing)


def build_registry(bot):
    """Every cell the harness can call.  (name, predicate, cases, expect, verdict)."""
    cells = []

    def cell(name, fn, cases, expect=LIVE, verdict=bool):
        cells.append((name, fn, cases, expect, verdict))

    seats = bot.fn("heal_seats")
    corners = bot.fn("core_corners")
    core_tiles = bot.fn("core_tiles")
    pack_pos = bot.fn("pack_pos")

    # -- pure geometry -----------------------------------------------------
    E = Position(18, 18)
    ring12 = seats(E, 24, 24) + corners(E, 24, 24)
    cell("geom.raid_act_step1: a station has a Manhattan-1 enemy Core tile",
         lambda c: any(manhattan(c, t) == 1 for t in core_tiles(E)),
         list(ring12))
    cell("geom.raid_act_step2: a station has a cardinal neighbour that is a seat",
         lambda c: any((c.add(d).x, c.add(d).y)
                       in {(s.x, s.y) for s in seats(E, 24, 24)}
                       for d in CARDINALS),
         list(ring12), expect=CONST_TRUE)
    # THE `_try_fwd_barrier` SHAPE, as a pure parity fact.  Runs on EVERY arm.
    # Manhattan distance has a parity: if manhattan(p, s) is ODD then every tile
    # at Manhattan-1 from p is at EVEN Manhattan from s.  So "cardinal-adjacent
    # to the raider AND Manhattan-1 from the sentinel" has an EMPTY satisfying
    # set whenever the sentinel sits on a cardinal neighbour of the raider --
    # which is exactly the state a fresh plant creates.  This cell is a POSITIVE
    # CONTROL: a detector that has never flagged a REAL historical defect has
    # not been seen to detect one.
    cell("geom.KNOWN DEFECT (_v230sent41._try_fwd_barrier): a tile is Manhattan-1 "
         "from BOTH the raider and a sentinel on its cardinal neighbour",
         lambda c: any(manhattan(c[0], t) == 1 for d in CARDINALS
                       for t in (c[0].add(d),) if manhattan(t, c[1]) == 1),
         [(Position(10, 10), Position(10, 10).add(d)) for d in CARDINALS],
         expect=CONST_FALSE)
    cell("geom.the same condition with the sentinel at Manhattan-2 (the parity "
         "flips, so the guard is live once the raider steps off)",
         lambda c: any(manhattan(c[0].add(d), c[1]) == 1 for d in CARDINALS),
         [(Position(10, 10), Position(10 + dx, 10 + dy))
          for dx, dy in ((2, 0), (0, 2), (1, 1), (3, 0), (0, 1))])

    cell("geom.fwd_sentinel: the >50 early-out admits this offset",
         lambda c: c[0] * c[0] + c[1] * c[1] <= 50,
         [(dx, dy) for dx in range(-9, 10) for dy in range(-9, 10)])
    cell("geom.fwd_sentinel: some cardinal build site is within d^2 32",
         lambda c: any((c[0] + ex) ** 2 + (c[1] + ey) ** 2 <= 32
                       for ex, ey in ((0, -1), (1, 0), (0, 1), (-1, 0))),
         [(dx, dy) for dx in range(-9, 10) for dy in range(-9, 10)])
    cell("geom.launcher: site offset is a legal throw (1 <= d^2 <= 26)",
         lambda c: 1 <= c[0] ** 2 + c[1] ** 2 <= 26,
         [(dx, dy) for dx in range(-5, 6) for dy in range(-5, 6)
          if dx * dx + dy * dy <= 26])

    lat = [Position(x, y) for x in range(0, 24, 2) for y in range(0, 24, 2)]
    cell("_salt_forward",
         lambda t: _mk(bot, enemy=E)._salt_forward(t, E), lat)

    # -- budget / bank gates ------------------------------------------------
    def eco_spendable(case):
        ti, cost, under, rnd = case
        w = _base_world(ti=ti, rnd=rnd)
        w.store[Team.A][bot.const("SLOT_UNDER")] = under
        ct = w.controller(w.add(EntityType.BUILDER_BOT, (5, 5), team=Team.A))
        return _mk(bot)._eco_spendable(ct, cost)

    cell("_eco_spendable", eco_spendable,
         [(ti, cost, u, r)
          for ti in (0, 20, 100, 2000) for cost in (3, 30, 120)
          for u in (0, 1)
          for r in (0, bot.const("HUNT_MIN_RND"), bot.const("HUNT_MIN_RND") + 50)])

    def eco_cap(case):
        ti, rnd = case
        w = _base_world(ti=ti, rnd=rnd)
        ct = w.controller(w.add(EntityType.BUILDER_BOT, (5, 5), team=Team.A))
        return _mk(bot)._eco_cap(ct) == bot.const("SURGE_ECO_CAP")

    cell("_eco_cap returns the SURGE cap",
         eco_cap,
         [(ti, r) for ti in (0, 500, bot.const("SURGE_TI_FLOOR") - 1,
                             bot.const("SURGE_TI_FLOOR"), 5000)
          for r in (0, 100, bot.const("SURGE_MIN_RND") - 1,
                    bot.const("SURGE_MIN_RND"), 900)])

    def cpu(case):
        w = _base_world()
        w.cpu_us = case
        ct = w.controller(w.add(EntityType.BUILDER_BOT, (5, 5), team=Team.A))
        with redirect_stderr(io.StringIO()):
            return _mk(bot)._cpu_exhausted(ct)

    budget = bot.const("CPU_BUDGET_US")
    cell("_cpu_exhausted", cpu, [0, 1, budget // 2, budget - 1, budget, budget * 2])

    def seat_ban(case):
        core, mw, mh = case
        return _mk(bot, core=core, mw=mw, mh=mh, map_walls=set(),
                   map_ores=[])._seat_ban()

    cell("_seat_ban is not None",
         seat_ban,
         [(Position(4, 4), 24, 24), (Position(0, 0), 24, 24),
          (None, 24, 24), (Position(4, 4), 0, 0)],
         verdict=lambda r: r is not None)

    cell("_pave_ban is not None",
         lambda case: _mk(bot, core=Position(4, 4), map_walls=set(),
                          map_ores=[])._pave_ban(),
         [Position(4, 4), Position(9, 9)],
         expect=CONST_FALSE, verdict=lambda r: r is not None)

    # -- raid gates ---------------------------------------------------------
    def foothold(case):
        beat, rnd = case
        w = _base_world(rnd=rnd)
        w.store[Team.A][bot.const("SLOT_RAID_LIVE")] = beat
        ct = w.controller(w.add(EntityType.BUILDER_BOT, (5, 5), team=Team.A))
        return _mk(bot, enemy=E)._foothold_live(ct, rnd)

    stale = bot.const("LOKI_FOOTHOLD_STALE")
    cell("_foothold_live", foothold,
         [(b, r) for b in (0, 1, 50, 101) for r in (0, 50, 100, 100 + stale, 400)])

    def raid_open(case):
        rnd, est, beat = case
        w = _base_world(rnd=rnd)
        w.store[Team.A][bot.const("SLOT_RAID_LIVE")] = beat
        ct = w.controller(w.add(EntityType.BUILDER_BOT, (5, 5), team=Team.A))
        return _mk(bot, enemy=E)._raid_open(ct, rnd, est)

    cold = bot.const("LOKI_COLD_INSERT_RND")
    cell("_raid_open", raid_open,
         [(r, e, b) for r in (0, cold - 1, cold, cold + 100)
          for e in (False, True) for b in (0, cold + 1)])

    def open_seats(case):
        corner, sealed = case
        w = _base_world()
        me = w.add(EntityType.BUILDER_BOT, corner, team=Team.A)
        p = _mk(bot, enemy=E)
        p._ring(E)
        if sealed:
            for d in CARDINALS:
                t = corner.add(d)
                if (t.x, t.y) in p.raid_seatkeys:
                    w.add(EntityType.BARRIER, t, team=Team.A)
        ct = w.controller(me)
        ct.omniscient = True
        return p._open_seats_by(ct, corner)

    cell("_open_seats_by > 0",
         open_seats,
         [(c, s) for c in corners(E, 24, 24) for s in (False, True)],
         verdict=lambda n: n > 0)

    def live_fwd(case):
        me_at, n_sent = case
        w = _base_world()
        me = w.add(EntityType.BUILDER_BOT, me_at, team=Team.A)
        for i in range(n_sent):
            w.add(EntityType.SENTINEL, Position(15 + i, 14), team=Team.A,
                  direction=Direction.SOUTH)
        ct = w.controller(me)
        ct.omniscient = True
        return _mk(bot, enemy=E)._live_fwd_guns(ct, E)

    cell("_live_fwd_guns is not None (it can SEE the band)",
         live_fwd,
         [(Position(x, y), n) for x, y in ((17, 17), (12, 12), (3, 3))
          for n in (0, 2)],
         verdict=lambda r: r is not None)
    cell("_live_fwd_guns counts at least one",
         live_fwd,
         [(Position(x, y), n) for x, y in ((17, 17), (3, 3)) for n in (0, 2)],
         verdict=lambda r: bool(r))

    # -- four-neighbour predicates -----------------------------------------
    def has_acceptor(code):
        w = _base_world()
        me = w.add(EntityType.BUILDER_BOT, (10, 10), team=Team.A)
        bp = Position(10, 11)
        _build_nbrs(w, bp, code)
        return _mk(bot)._has_acceptor(w.controller(me), bp)

    cell("_has_acceptor", has_acceptor, _nbr_cases())

    def starved(code):
        w = _base_world()
        me = w.add(EntityType.BUILDER_BOT, (10, 10), team=Team.A)
        h = Position(10, 11)
        w.add(EntityType.HARVESTER, h, team=Team.A)
        _build_nbrs(w, h, code)
        return _mk(bot)._l4_harvester_starved(w.controller(me), h, Position(10, 10))

    cell("_l4_harvester_starved", starved,
         [c for c in _nbr_cases() if c[0] == 0])   # keep the gap tile empty

    # `_l4_repair` is the incumbent's closest structural analogue to
    # `_try_fwd_barrier`: it needs TWO different conditions to hold among one
    # tile's four neighbours (a FEEDER and an ACCEPTOR).  Swept over every
    # configuration of the gap's three free neighbours.
    def l4_repair(code):
        w = _base_world()
        me = w.add(EntityType.BUILDER_BOT, (6, 6), team=Team.A)
        g = Position(6, 7)
        spots = ((Position(5, 7), Direction.EAST, Direction.WEST),
                 (Position(7, 7), Direction.WEST, Direction.EAST),
                 (Position(6, 8), Direction.NORTH, Direction.SOUTH))
        for k, (at, toward_g, away) in zip(code, spots):
            if k == 1:
                w.add(EntityType.CONVEYOR, at, team=Team.A, direction=toward_g)
            elif k == 2:
                w.add(EntityType.CONVEYOR, at, team=Team.A, direction=away)
            elif k == 3:
                w.add(EntityType.HARVESTER, at, team=Team.A)
        ct = w.controller(me)
        ct.omniscient = True
        p = _mk(bot, enemy=E, map_walls=set(), map_ores=[])
        with redirect_stderr(io.StringIO()), redirect_stdout(io.StringIO()):
            return p._l4_repair(ct)

    cell("_l4_repair (needs BOTH a feeder and an acceptor beside the gap)",
         l4_repair,
         [(a, b, c) for a in range(4) for b in range(4) for c in range(4)])

    def beside_belt(code):
        w = _base_world()
        me = w.add(EntityType.BUILDER_BOT, (10, 10), team=Team.A)
        t = Position(10, 11)
        _build_nbrs(w, t, code)
        return _mk(bot)._salt_beside_belt(w.controller(me), t)

    cell("_salt_beside_belt", beside_belt, _nbr_cases())

    def siphon_taken(case):
        who, where = case
        w = _base_world()
        me = w.add(EntityType.BUILDER_BOT, (10, 10), team=Team.A)
        belt = Position(12, 10)
        if who is not None:
            w.add(EntityType.BUILDER_BOT, belt.add(where), team=who)
        return _mk(bot)._siphon_taken(w.controller(me), belt, me.eid)

    cell("_siphon_taken", siphon_taken,
         [(who, d) for who in (None, Team.A, Team.B) for d in CARDINALS])

    # -- home-band predicates ----------------------------------------------
    def home_gun(case):
        at, team = case
        w = _base_world()
        me = w.add(EntityType.BUILDER_BOT, (5, 5), team=Team.A)
        if at is not None:
            w.add(EntityType.GUNNER, at, team=team, direction=Direction.EAST)
        ct = w.controller(me)
        ct.omniscient = True
        return _mk(bot)._live_home_gun(ct)

    cell("_live_home_gun", home_gun,
         [(at, t) for at in (None, Position(4, 2), Position(2, 20))
          for t in (Team.A, Team.B)])

    def shelled(case):
        w = _base_world()
        core = [e for e in w.ents.values()
                if e.etype == EntityType.CORE and e.team == Team.A][0]
        core.hp -= case
        me = w.add(EntityType.BUILDER_BOT, (5, 5), team=Team.A)
        ct = w.controller(me)
        ct.omniscient = True
        return _mk(bot)._core_shelled(ct)

    cell("_core_shelled", shelled, [0, 1, 100, 499])

    def free_seats(case):
        blocked = case
        w = _base_world()
        me = w.add(EntityType.BUILDER_BOT, (5, 5), team=Team.A)
        p = _mk(bot)
        for s in seats(Position(2, 2), 24, 24)[:blocked]:
            w.add(EntityType.BARRIER, s, team=Team.A)
        ct = w.controller(me)
        ct.omniscient = True
        return p._free_seats(ct)

    cell("_free_seats is non-empty", free_seats, [0, 3, 8],
         verdict=lambda r: bool(r))

    # -- turret predicates --------------------------------------------------
    def hostile_at(case):
        at, team = case
        w = _base_world()
        g = w.add(EntityType.GUNNER, (10, 10), team=Team.A, direction=Direction.EAST)
        if team is not None:
            w.add(EntityType.BARRIER, at, team=team)
        return _mk(bot)._hostile_at(w.controller(g), at)

    cell("_hostile_at", hostile_at,
         [(Position(11, 10), t) for t in (None, Team.A, Team.B)]
         + [(Position(-1, -1), None)])

    def facing_has_target(case):
        at, team = case
        w = _base_world()
        g = w.add(EntityType.GUNNER, (10, 10), team=Team.A, direction=Direction.EAST)
        if team is not None:
            w.add(EntityType.BUILDER_BOT, at, team=team)
        return _mk(bot)._facing_has_target(w.controller(g))

    cell("_facing_has_target", facing_has_target,
         [(Position(11, 10), t) for t in (None, Team.A, Team.B)])

    def ray_lands(case):
        facing, tgt, blocker = case
        w = _base_world()
        g = w.add(EntityType.GUNNER, (10, 10), team=Team.A, direction=Direction.EAST)
        w.add(EntityType.BUILDER_BOT, tgt, team=Team.B)
        if blocker is not None:
            w.add(EntityType.BARRIER, blocker, team=Team.A)
        return _mk(bot)._ray_lands(w.controller(g), g.pos, facing, tgt)

    cell("_ray_lands", ray_lands,
         [(f, Position(12, 10), b)
          for f in (Direction.EAST, Direction.NORTH, Direction.SOUTHEAST)
          for b in (None, Position(11, 10))])

    def rotate_allowed(case):
        gap, want, prev, lock, has_tgt = case
        w = _base_world(rnd=200)
        g = w.add(EntityType.GUNNER, (10, 10), team=Team.A, direction=Direction.EAST)
        if has_tgt:
            w.add(EntityType.BUILDER_BOT, (11, 10), team=Team.B)
        p = _mk(bot)
        p.rot_rnd = 200 - gap
        p.rot_prev_dir = prev
        p.rot_lock_d = lock
        return p._rotate_allowed(w.controller(g), g.pos, want, Position(14, 10))

    cd = bot.const("ROTATE_COOLDOWN_RNDS")
    cell("_rotate_allowed", rotate_allowed,
         [(gap, Direction.NORTH, prev, lock, tgt)
          for gap in (0, cd - 1, cd, cd + 5)
          for prev in (Direction.NORTH, Direction.SOUTH)
          for lock in (0, 10 ** 9)
          for tgt in (False, True)])

    def cb_over_heal(case):
        role, threat, ti, gun = case
        w = _base_world(ti=ti)
        me = w.add(EntityType.BUILDER_BOT, (4, 3), team=Team.A)
        if threat is not None:
            w.store[Team.A][bot.const("SLOT_THREAT")] = pack_pos(threat)
        if gun:
            w.add(EntityType.GUNNER, (4, 2), team=Team.A, direction=Direction.EAST)
        ct = w.controller(me)
        ct.omniscient = True
        return _mk(bot, role=role)._cb_over_heal(ct)

    cell("_cb_over_heal", cb_over_heal,
         [(role, threat, ti, gun)
          for role in ("defend", "expand", "raid")
          for threat in (None, Position(4, 4), Position(22, 22))
          for ti in (1, 500)
          for gun in (False, True)])

    def sabotage(case):
        team, etype = case
        w = _base_world()
        me = w.add(EntityType.BUILDER_BOT, (5, 5), team=Team.A)
        w.add(etype, (5, 4), team=team, direction=Direction.SOUTH)
        return _mk(bot)._sabotage_prio(w.controller(me))

    cell("_sabotage_prio", sabotage,
         [(t, e) for t in (Team.A, Team.B)
          for e in (EntityType.GUNNER, EntityType.HARVESTER, EntityType.CONVEYOR,
                    EntityType.BARRIER)],
         expect=CONST_FALSE)

    # -- pave helpers -------------------------------------------------------
    pb_ore = bot.fn("pave_blocked_by_ore")
    pb = bot.fn("pave_blocked")

    def pave_ore(case):
        w = L.World(24, 24, ore=[(6, 5)])
        me = w.add(EntityType.BUILDER_BOT, (6, 6), team=Team.A)
        return pb_ore(w.controller(me), case)

    cell("pave_blocked_by_ore", pave_ore,
         [Position(6, 5), Position(6, 7), Position(23, 23), Position(-1, 0)])

    def pave_ban_case(case):
        tile, ban = case
        w = L.World(24, 24)
        me = w.add(EntityType.BUILDER_BOT, (6, 6), team=Team.A)
        return pb(w.controller(me), tile, ban)

    cell("pave_blocked", pave_ban_case,
         [(Position(6, 7), b) for b in (None, frozenset({(6, 7)}),
                                        frozenset({(1, 1)}))])

    # -- heal actions -------------------------------------------------------
    def heal_core(case):
        dmg, at = case
        w = _base_world()
        core = [e for e in w.ents.values()
                if e.etype == EntityType.CORE and e.team == Team.A][0]
        core.hp -= dmg
        me = w.add(EntityType.BUILDER_BOT, at, team=Team.A)
        return _mk(bot)._heal_core(w.controller(me))

    cell("_heal_core", heal_core,
         [(d, a) for d in (0, 100) for a in (Position(2, 1), Position(8, 8))])

    def heal_adjacent(case):
        dmg, team = case
        w = _base_world()
        me = w.add(EntityType.BUILDER_BOT, (10, 10), team=Team.A)
        b = w.add(EntityType.BARRIER, (10, 11), team=team)
        b.hp -= dmg
        return _mk(bot)._heal_adjacent(w.controller(me))

    cell("_heal_adjacent", heal_adjacent,
         [(d, t) for d in (0, 10) for t in (Team.A, Team.B)])

    # -- raid station / salt gate ------------------------------------------
    def raid_station(case):
        me_at, near, wall_the_ring = case
        w = _base_world()
        me = w.add(EntityType.BUILDER_BOT, me_at, team=Team.A)
        if wall_the_ring:
            # Every one of the twelve stations impassable (GT-4: a barrier is
            # not bot-passable), which is how `best` can stay None.
            for t in seats(E, 24, 24) + corners(E, 24, 24):
                w.add(EntityType.BARRIER, t, team=Team.B)
        ct = w.controller(me)
        ct.omniscient = True
        p = _mk(bot, enemy=E)
        return p._raid_station(ct, E, near)

    cell("_raid_station is not None", raid_station,
         [(Position(x, y), n, wall)
          for x, y in ((17, 17), (10, 10), (3, 3))
          for n in (False, True) for wall in (False, True)],
         verdict=lambda r: r is not None)

    def salt_idle(case):
        me_at, mcd = case
        w = _base_world()
        me = w.add(EntityType.BUILDER_BOT, me_at, team=Team.A)
        ct = w.controller(me)
        ct.omniscient = True
        ct.move_cooldown = mcd
        p = _mk(bot, enemy=E)
        return p._salt_idle_ok(ct, E, me.pos, near=True)

    cell("_salt_idle_ok", salt_idle,
         [(Position(x, y), m) for x, y in ((17, 17), (10, 10), (16, 17))
          for m in (0, 1)])

    def enemy_anchor(case):
        stored, core = case
        w = _base_world()
        if stored is not None:
            w.store[Team.A][bot.const("SLOT_ENEMY_CORE")] = pack_pos(stored)
        me = w.add(EntityType.BUILDER_BOT, (5, 5), team=Team.A)
        return _mk(bot, core=core, enemy=None)._enemy_anchor(w.controller(me))

    cell("_enemy_anchor is not None", enemy_anchor,
         [(s, c) for s in (None, Position(19, 3))
          for c in (Position(2, 2), None)],
         verdict=lambda r: r is not None)

    # -- arm-conditional cells ---------------------------------------------
    # Predicates that only some arms carry.  `_try_fwd_barrier` is the 2026-08-15
    # defect itself, so pointing this suite at `bots/_v230sent41` reproduces it
    # rather than merely describing it.
    if hasattr(bot.Player, "_try_fwd_barrier"):
        def fwd_barrier(case):
            p_at, s_at = case
            w = _base_world(ti=500, rnd=50)
            me = w.add(EntityType.BUILDER_BOT, p_at, team=Team.A)
            w.add(EntityType.SENTINEL, s_at, team=Team.A,
                  direction=Direction.SOUTHEAST)
            pl = _mk(bot, enemy=E)
            pl.fwd_bar_due = (s_at.x, s_at.y)
            pl.fwd_bar_rnd = 50
            ct = w.controller(me)
            ct.omniscient = True
            return pl._try_fwd_barrier(ct, E)

        # (a) THE STATE THE CALLER CREATES: the plant put the sentinel on a
        #     cardinal neighbour and the builder could not move that round
        #     (acting and moving are mutually exclusive), so the very next
        #     round's attempt sees Manhattan-1.  Parity says: no candidate.
        cell("KNOWN DEFECT _try_fwd_barrier in the POST-PLANT state "
             "(sentinel on a cardinal neighbour)",
             fwd_barrier,
             [(Position(14, 14), Position(14, 14).add(d)) for d in CARDINALS],
             expect=CONST_FALSE)
        # (b) ... and it is NOT unsatisfiable in general.  Once the raider steps
        #     away the parity flips and the guard can fire, which is why this is
        #     "dead in the state its caller reaches", not "dead".
        cell("_try_fwd_barrier once the raider has stepped to Manhattan-2",
             fwd_barrier,
             [(Position(14, 14), Position(14, 16)),
              (Position(14, 14), Position(16, 14)),
              (Position(14, 14), Position(15, 15)),
              (Position(14, 14), Position(12, 14)),
              (Position(14, 14), Position(14, 12))])

    def seat_seek(case):
        blocked, at = case
        w = _base_world()
        me = w.add(EntityType.BUILDER_BOT, at, team=Team.A)
        for s in seats(Position(2, 2), 24, 24)[:blocked]:
            w.add(EntityType.BARRIER, s, team=Team.A)
        ct = w.controller(me)
        ct.omniscient = True
        return _mk(bot)._seat_seek_target(ct)

    cell("_seat_seek_target is not None", seat_seek,
         [(b, a) for b in (0, 8) for a in (Position(5, 5), Position(2, 1))],
         verdict=lambda r: r is not None)

    return cells


# ===========================================================================
# 3.  THE SWEEP
# ===========================================================================

@unittest.skipUnless(HAVE_BOT, f"{L.BOT} not present")
class TestPredicateLiveness(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.b = BOT
        cls.results = [sweep(n, f, c, e, v)
                       for n, f, c, e, v in build_registry(BOT)]
        cls.by_name = {r.name: r for r in cls.results}
        if REPORT:
            print(f"\n=== PREDICATE LIVENESS SWEEP: {L.BOT} ===", file=sys.stderr)
            for r in cls.results:
                mark = "  " if r.is_live else "!!"
                print(f"{mark} {r.message()}", file=sys.stderr)

    def test_the_sweep_actually_ran(self):
        self.assertGreaterEqual(len(self.results), 25,
                                "the registry shrank -- did a cell stop building?")
        self.assertGreater(sum(r.evaluated for r in self.results), 500)

    def test_no_cell_failed_to_evaluate_at_all(self):
        broken = [r.message() for r in self.results if r.evaluated == 0]
        self.assertEqual(broken, [], "cells raised on every input:\n" + "\n".join(broken))

    def test_no_cell_raises_on_a_MAJORITY_of_its_inputs(self):
        """A predicate that mostly explodes is not being swept, it is being poked."""
        bad = [f"{r.name}: {r.errors}/{r.n} raised, first={r.first_error}"
               for r in self.results if r.errors * 2 > r.n]
        self.assertEqual(bad, [], "\n".join(bad))

    def test_every_cell_marked_LIVE_produced_BOTH_verdicts(self):
        """The headline assertion.  A constant here is a suspected dead guard."""
        flagged = [r.message() for r in self.results
                   if r.expect == LIVE and not r.is_live]
        self.assertEqual(
            flagged, [],
            "SUSPECTED DEAD GUARDS (each is a suspicion, not a proof -- read the "
            "code before calling it a defect):\n  " + "\n  ".join(flagged))

    def test_the_known_constant_cells_are_STILL_constant(self):
        """The allowlist is an assertion, not an exemption.

        Two cells are known to be constant in the SHIPPED configuration and are
        documented in `test_bot_predicates.TestQuietFlagDeadBranches` /
        `TestPaveBanIsConstantNone`.  If either ever goes live, that is a
        behaviour change and this test says so rather than silently passing.
        """
        for r in self.results:
            if r.expect == L_CONST_FALSE:
                self.assertEqual(
                    r.trues, 0,
                    f"{r.name} was expected constant-FALSE and returned True at "
                    f"{r.witness_true} -- the shipped configuration changed")
                self.assertGreater(r.falses, 0)
            elif r.expect == L_CONST_TRUE:
                self.assertEqual(
                    r.falses, 0,
                    f"{r.name} was expected constant-TRUE and returned False at "
                    f"{r.witness_false}")
                self.assertGreater(r.trues, 0)

    def test_the_detector_flagged_something_on_this_tree(self):
        """A detector that has never flagged anything has not been seen to detect.

        On the incumbent it must flag at least the two known-dead cells.  If the
        tree is ever cleaned up so that nothing is constant, this test SHOULD be
        retired deliberately -- not silently, which is why it is an assertion.
        """
        flagged = [r.name for r in self.results if not r.is_live]
        self.assertTrue(
            flagged,
            "nothing was flagged at all on this tree -- either the tree is clean "
            "(retire this test on purpose) or the harness stopped detecting")

    def test_the_two_halves_of_the_forward_sentinel_guard_disagree_somewhere(self):
        """A fast path is only useful if it is STRICTLY weaker than what it guards.

        Both halves are swept as cells above; here their witnesses are compared.
        `admits && !reachable` must be non-empty (the guard is doing work) and
        `!admits && reachable` must be EMPTY (the guard is a superset).
        """
        offsets = [(dx, dy) for dx in range(-9, 10) for dy in range(-9, 10)]
        def admits(c):
            return c[0] * c[0] + c[1] * c[1] <= 50

        def reachable(c):
            return any((c[0] + ex) ** 2 + (c[1] + ey) ** 2 <= 32
                       for ex, ey in ((0, -1), (1, 0), (0, 1), (-1, 0)))

        self.assertTrue([c for c in offsets if admits(c) and not reachable(c)],
                        "the >50 guard admits nothing it should not -- it is exact, "
                        "not a fast path; re-read _try_forward_sentinel")
        self.assertEqual([c for c in offsets if reachable(c) and not admits(c)], [],
                         "the >50 guard REJECTS reachable build sites")


# module-level aliases so the class body above reads cleanly
L_CONST_FALSE = CONST_FALSE
L_CONST_TRUE = CONST_TRUE


if __name__ == "__main__":
    unittest.main()
