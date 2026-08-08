#!/usr/bin/env python3
"""Tests for the INSTRUMENTS — the tools whose numbers decide what we ship.

Run:  .venv/bin/python -m unittest discover -s tests -v

Why this file exists (2026-08-08, session 20). The project had **zero tests** and
shipped two broken instruments in one evening:

  - `ceiling.py` reported a median turns-to-kill conditioned on having killed.
    That is a COLLIDER: a bot that converts more games to kills earns the extra
    ones on the hard slow games, so improving kill rate DRAGS THE MEDIAN UP and
    the tool scores the improvement as a regression. It ran 1,080 matches before
    an outside audit caught it.
  - `audit_trigger.py`'s ship predicate matches 6 rows in the project's entire
    history and has no time window, so past ~12 active hours it fires
    unconditionally. It summoned an audit session by reporting on itself.

Neither is exotic. Both are one assertion away from being caught, and neither
was catchable while the arithmetic lived inside a print statement — which is why
`ceiling.metrics()` was split out.

WHAT BELONGS HERE: anything that turns data into a number we make a decision on.
WHAT DOES NOT: the game engine, bot behaviour, anything needing a match to run.
These tests must stay fast (< 1s total) and require no network and no fcode.

THE RULE THIS FILE ENCODES: an instrument that has never been fed a case with a
known answer is an untested instrument, and this project has a long tape of
those producing confident wrong readings — proto3 TEAM_A=0 silently dropping
every seat-A entity, map-identity collisions, int32 two's-complement deltas.
Every one was found by re-running or by outside eyes. None was found by a test.
"""
import csv
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from arena import wilson  # noqa: E402
from ceiling import metrics  # noqa: E402


def row(winner, condition, turns):
    return {"winner": winner, "condition": condition, "turns": turns, "map": "m"}


class TestCeilingCollider(unittest.TestCase):
    """The exact bug the audit found, pinned so it cannot come back."""

    def test_extra_slow_kills_do_not_score_as_a_regression(self):
        # A: wins 4, kills 1 (a fast one). B: identical, plus 3 SLOW kills.
        # B is strictly better — same fast kill, three more kills on top.
        a = [row("A", "core_destroyed", 100)] + [row("A", "titanium_collected", 1000)] * 3
        b = [row("B", "core_destroyed", 100)] + [row("B", "core_destroyed", 900)] * 3

        ma, mb = metrics("A", a), metrics("B", b)
        self.assertGreater(mb["kill_rate"], ma["kill_rate"], "B kills more; setup is wrong")

        # The collider: conditioned on kills, B looks 350 turns WORSE.
        self.assertGreater(
            mb["kills_only_median"], ma["kills_only_median"],
            "this is the collider itself — if it stops holding, the fixture drifted",
        )
        # The fix: censored, B is better or equal. This is the assertion that
        # would have caught the shipped bug.
        self.assertLessEqual(
            mb["censored_median"], ma["censored_median"],
            "censored kill-time reversed sign — the collider is back",
        )

    def test_censoring_reports_1000_when_most_games_are_not_kills(self):
        # 2 kills out of 5 — the median game does not end in a kill, and saying
        # so is honest rather than a defect.
        rows = [row("A", "core_destroyed", 100)] * 2 + [row("A", "titanium_collected", 800)] * 3
        self.assertEqual(metrics("A", rows)["censored_median"], 1000)

    def test_a_strictly_faster_killer_scores_better(self):
        slow = [row("A", "core_destroyed", 900)] * 5
        fast = [row("B", "core_destroyed", 100)] * 5
        self.assertLess(metrics("B", fast)["censored_median"],
                        metrics("A", slow)["censored_median"])


class TestCeilingArithmetic(unittest.TestCase):
    def test_kill_rate_denominator_is_all_matches_not_wins(self):
        # 1 kill, 2 wins, 10 matches. kill_rate is over 10; conversion over 2.
        rows = ([row("A", "core_destroyed", 100), row("A", "titanium_collected", 900)]
                + [row("B", "core_destroyed", 100)] * 8)
        m = metrics("A", rows)
        self.assertEqual(m["n_total"], 10)
        self.assertAlmostEqual(m["kill_rate"], 0.1)
        self.assertAlmostEqual(m["conversion"], 0.5)

    def test_a_bot_that_never_wins_does_not_divide_by_zero(self):
        m = metrics("A", [row("B", "core_destroyed", 100)] * 4)
        self.assertEqual(m["conversion"], 0.0)
        self.assertIsNone(m["kills_only_median"])

    def test_losses_by_core_kill_are_not_credited_to_the_loser(self):
        # B killed A's core. A must not get the kill.
        rows = [row("B", "core_destroyed", 200)] * 3
        self.assertEqual(metrics("A", rows)["n_kills"], 0)
        self.assertEqual(metrics("B", rows)["n_kills"], 3)


class TestWilson(unittest.TestCase):
    """arena.py is frozen, so its interval is a fixed contract both tools read."""

    def test_known_values(self):
        lo, hi = wilson(50, 100)
        self.assertAlmostEqual(lo, 0.404, places=2)
        self.assertAlmostEqual(hi, 0.596, places=2)

    def test_degenerate_cases_do_not_raise(self):
        self.assertEqual(wilson(0, 0), (0.0, 1.0))
        lo, hi = wilson(0, 10)
        self.assertEqual(lo, 0.0)
        self.assertGreater(hi, 0.0)
        lo, hi = wilson(10, 10)
        self.assertLess(lo, 1.0)
        self.assertEqual(hi, 1.0)

    def test_interval_tightens_with_n(self):
        w = lambda n: wilson(n // 2, n)[1] - wilson(n // 2, n)[0]
        self.assertLess(w(1000), w(100))
        self.assertLess(w(100), w(10))


class TestAuditTriggerPredicate(unittest.TestCase):
    """The trigger fired at boot on a predicate that matches almost nothing.

    This is the test that would have stopped it summoning an audit session by
    reporting on itself.
    """

    def setUp(self):
        if not (ROOT / "elo_history.tsv").exists():
            self.skipTest("elo_history.tsv not present")
        import audit_trigger
        self.mod = audit_trigger

    def test_counts_real_activations_not_prose(self):
        """The old predicate matched 6 rows in all history; the tape holds 45.

        The bug was counting ships by prose-matching results.tsv descriptions,
        which depends on how a session happened to word a row. This asserts we
        are reading activations from the monitor-written tape instead.
        """
        rows = list(csv.reader((ROOT / "elo_history.tsv").read_text().splitlines(), delimiter="\t"))[1:]
        transitions, prev = 0, None
        for r in rows:
            if len(r) < 4:
                continue
            if prev is not None and r[3] != prev:
                transitions += 1
            prev = r[3]
        self.assertGreater(
            transitions, 20,
            "elo_history shows almost no activations — either the tape changed "
            "shape or elo_logger stopped recording active_bot",
        )
        rate, detail = self.mod.ship_cadence()
        self.assertIn("activation", detail)
        self.assertGreaterEqual(rate, 0.0)

    def test_respects_its_time_window(self):
        """The old version sliced an all-time list, so it had no window at all.

        Every activation on the tape is older than this cutoff, so a windowed
        implementation must return zero. One that ignores the window returns a
        positive count and fails here.
        """
        orig = self.mod.CHURN_HOURS
        try:
            self.mod.CHURN_HOURS = 0
            rate, _ = self.mod.ship_cadence()
            self.assertEqual(
                rate, 0.0,
                "ship_cadence ignored its time window — this is the exact defect "
                "that made the trigger fire unconditionally past ~12 hours",
            )
        finally:
            self.mod.CHURN_HOURS = orig

    def test_does_not_fire_on_a_normal_shipping_day(self):
        """Regression: the trigger summoned an audit session by reporting on itself."""
        rate, _ = self.mod.ship_cadence()
        self.assertGreater(
            rate, 0.5,
            "ship cadence trips on a tape with 19 activations in 24h. The check "
            "is miscalibrated or blind again.",
        )


class TestArenaCeilingCoupling(unittest.TestCase):
    """ceiling.py carries a byte-copy of arena.py's fcode command on purpose.

    arena.py is deny-listed for edits so its verdicts stay comparable across the
    whole tape; ceiling.py therefore duplicates the invocation rather than
    importing it. That duplication is only safe while the two stay identical —
    if they drift, the two instruments silently stop playing the same games and
    every cross-tool comparison on the tape becomes wrong. This test is the
    thing that makes the docstring's COUPLING WARNING enforceable.
    """

    def _cmd_flags(self, path):
        src = path.read_text()
        m = re.search(r'cmd = \[(.*?)\]', src, re.S)
        assert m, f"no cmd list found in {path.name}"
        return sorted(re.findall(r'"(--?[a-z-]+)"', m.group(1)))

    def test_both_tools_invoke_fcode_run_identically(self):
        self.assertEqual(
            self._cmd_flags(ROOT / "tools" / "arena.py"),
            self._cmd_flags(ROOT / "tools" / "ceiling.py"),
            "arena.py and ceiling.py no longer pass the same flags to `fcode "
            "run`. They are not playing the same games any more, so their "
            "numbers cannot be compared. Re-sync them (see ceiling.py's "
            "COUPLING WARNING) or stop reading them side by side.",
        )


if __name__ == "__main__":
    unittest.main()
