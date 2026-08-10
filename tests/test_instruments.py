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
from datetime import datetime, timedelta
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
        """Regression: the trigger summoned an audit session by reporting on itself.

        REWRITTEN 2026-08-09 s26. The original asserted `rate > 0.5` against the
        LIVE tape. It passed at boot (11 activations / ~20 active hours = 0.55)
        and failed 16 minutes later at 10/20 = 0.50, because an activation aged
        out of the 24h window. Nothing was broken: the check trips at `< 0.5`,
        so 0.50 reads `ok` — the TEST was stricter than the instrument it
        guarded, and it was asserting a fact about how much we shipped today
        rather than about the calibration of the check.

        A test whose truth changes with the wall clock is an alarm on the team's
        activity wearing a unit test's clothes. Both directions now run on
        fixtures, and both are asserted, so it cannot pass vacuously.

        REPAIRED 2026-08-10 s28 — AND THE PREVIOUS REPAIR IS WHY IT BROKE. The
        s26 rewrite above de-live-ified `hours` and the row CONTENTS, then dated
        those rows with the LITERAL `2026-08-09T10:00`. `ship_cadence` discards
        any row older than `datetime.now() - 24h`. So on 2026-08-10 the entire
        fixture aged out of the window, the check counted 0 transitions, and the
        test failed reporting `0.0` — i.e. **the same wall-clock coupling it was
        rewritten to escape, one layer down and one day later.**

        THAT FAILURE WAS THEN READ AS A FINDING ABOUT THE INSTRUMENT. The s27
        HANDOVER recorded it as proof that `audit_trigger`'s ship-cadence signal
        "would summon an audit on a normal working day", and left it red on
        purpose on that basis. **The check was never miscalibrated.** Pinned to
        a fixed clock it returns 0.60/hr for the normal day (ok) and 0.10/hr for
        the stalled one (trips) — correct in both directions.

        A RED TEST IS EVIDENCE OF A DEFECT, NOT EVIDENCE OF *WHICH* DEFECT.
        This one named the wrong component for an unknown length of time, and
        the naming was propagated into HANDOVER as an instrument fact.

        `now` is now pinned alongside `elo` and `hours`, so no clock reaches
        this test at all and it cannot rot a third time.
        """
        BASE = datetime(2026, 8, 9, 10, 0)

        def rate_for(activations, hours):
            rows, tag = [], "v1"
            for i in range(activations + 1):
                when = BASE + timedelta(minutes=10 * i)
                rows.append([when.strftime("%Y-%m-%dT%H:%M"), "1500", str(i), tag])
                tag = f"v{i + 2}"          # every row is a new activation
            self.mod._OVERRIDE.clear()
            # Pin the clock the cutoff is measured from, not just the rows.
            self.mod._OVERRIDE.update({
                "elo": rows, "hours": hours,
                "now": BASE + timedelta(hours=activations // 6 + 1),
            })
            try:
                return self.mod.ship_cadence()[0]
            finally:
                self.mod._OVERRIDE.clear()

        normal = rate_for(activations=12, hours=20)      # 0.60/hr
        self.assertGreaterEqual(
            normal, 0.5,
            "a 12-activation, 20-hour day reads as a cadence STALL. The check "
            "is miscalibrated: it would summon an audit on a normal day.",
        )
        stalled = rate_for(activations=2, hours=20)       # 0.10/hr
        self.assertLess(
            stalled, 0.5,
            "a 2-activation, 20-hour day does NOT trip the cadence check — the "
            "alarm cannot fire, so its silence means nothing.",
        )

    def test_ship_cadence_reads_the_live_tape_without_raising(self):
        """The live coupling that IS worth asserting: the real tape still parses
        and yields a number. What that number IS depends on the day, and is the
        instrument's business, not this test's."""
        rate, detail = self.mod.ship_cadence()
        self.assertGreaterEqual(rate, 0.0)
        self.assertIn("activation", detail)


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


class TestSlotRuleAndTheAlarmThatReportsIt(unittest.TestCase):
    """The stop-loss. Two implementations of one rule existed (2026-08-09,
    s26): `elo_logger` had it inline and correct, `ship_watch` had something
    else and durable. `tools/slot_rule.py` is now the single statement; these
    tests exist so the two can never silently diverge again.

    NON-VACUITY IS THE POINT. A test that only asserts "both silent" passes
    when both are broken. Every case here asserts the ALARM STATE in BOTH
    directions on the SAME series."""

    import importlib as _il
    slot_rule = _il.import_module("slot_rule")
    sys.path.insert(0, str(ROOT / "tools" / "monitors"))
    ship_watch = _il.import_module("ship_watch")
    elo_logger = _il.import_module("elo_logger")

    HDR = "ts\trating\tmatches\tversion\trank\n"

    def _tape(self, rows, tag="v900"):
        import tempfile
        fh = tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False)
        fh.write(self.HDR)
        for i, (r, m) in enumerate(rows):
            fh.write(f"2026-01-01T00:{i:02d}\t{r}\t{m}\t{tag}\trank #1\n")
        fh.close()
        return fh.name, rows[-1][0], rows[-1][1], tag

    def _elo_logger_says_slot_free(self, tape, rating, matches, tag):
        """Drive elo_logger's INLINE rule over the same tape and report whether
        it announces SLOT FREE. Uses its real code path, not a reimplementation
        — reimplementing it here would recreate the bug this test guards."""
        import io, json, tempfile, contextlib, os
        el = self.elo_logger
        status = {"rating": {"rating": rating, "matches_played": matches},
                  "rank": {"rank": 1},
                  "active_submission": {"version": int(tag.lstrip("v")), "name": "t"}}
        payload = json.dumps(status) + "---SPLIT---" + json.dumps(
            [{"version": int(tag.lstrip("v")), "name": "t"}])
        state = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        state.write("{}")
        state.close()
        old_hist, old_state, old_stdin = el.HIST, el.STATE, sys.stdin
        buf = io.StringIO()
        try:
            el.HIST, el.STATE, sys.stdin = tape, state.name, io.StringIO(payload)
            with contextlib.redirect_stdout(buf):
                el.main()
        finally:
            el.HIST, el.STATE, sys.stdin = old_hist, old_state, old_stdin
            os.unlink(state.name)
        out = buf.getvalue()
        # elo_logger APPENDS a row to the tape it is given; that is fine, the
        # tape is a throwaway. We only read its announcement.
        return "SLOT FREE" in out

    def _both(self, rows, tag="v900"):
        tape, rating, matches, tag = self._tape(rows, tag)
        st = self.slot_rule.evaluate(tape)
        _, _, _, _, alert = self.ship_watch.assess(tape)
        return st, (alert is not None and "FREED THE SLOT" in (alert or "")), \
            self._elo_logger_says_slot_free(tape, rating, matches, tag)

    def test_a_bleeding_holder_alarms_in_BOTH_implementations(self):
        """The non-vacuous direction: both MUST fire on the same series."""
        rows = [(1500, 100 + i) for i in range(10)] + \
               [(1500 - 8 * (i + 1), 110 + i) for i in range(5)]   # net5 -40
        st, ship, elo = self._both(rows)
        self.assertEqual(st.net5, -40)
        self.assertTrue(st.slot_free, "slot_rule failed to free the slot at net5 -40")
        self.assertTrue(ship, "ship_watch raised NO alert on a -40 window")
        self.assertTrue(elo, "elo_logger announced NO slot-free on a -40 window")

    def test_a_healthy_holder_alarms_in_NEITHER(self):
        rows = [(1500 + 3 * i, 100 + i) for i in range(15)]
        st, ship, elo = self._both(rows)
        self.assertFalse(st.slot_free)
        self.assertFalse(ship, "ship_watch cried wolf on a rising holder")
        self.assertFalse(elo, "elo_logger cried wolf on a rising holder")

    def test_the_two_agree_across_the_threshold_in_both_directions(self):
        """Walk the window from healthy to bleeding. The two implementations
        must flip on the SAME step — and the sweep must actually contain a
        flip, or it proves nothing."""
        seen = set()
        for drop in (0, 2, 4, 5, 6, 8, 10):
            rows = [(1500, 100 + i) for i in range(10)] + \
                   [(1500 - drop * (i + 1), 110 + i) for i in range(5)]
            st, ship, elo = self._both(rows)
            self.assertEqual(ship, st.slot_free, f"ship_watch disagrees at drop={drop}")
            self.assertEqual(elo, st.slot_free, f"elo_logger disagrees at drop={drop}")
            seen.add(st.slot_free)
        self.assertEqual(seen, {True, False},
                         "the sweep never crossed the threshold — vacuous")

    def test_unarmed_holder_cannot_free_the_slot_in_either(self):
        rows = [(1500 - 100 * i, 100 + i) for i in range(7)]     # k=6, catastrophic
        st, ship, elo = self._both(rows)
        self.assertFalse(st.armed)
        self.assertFalse(st.slot_free)
        self.assertFalse(ship)
        self.assertFalse(elo)

    def test_ship_watch_selftest_passes(self):
        """The selftest is itself an instrument; if it stops passing, the alarm
        is unverified. Mutation-tested 2026-08-09 against 5 mutations
        (no-restart, dead threshold, ARM_AFTER=0, WINDOW 5->50, WINDOW->1);
        all five made it fail."""
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = self.ship_watch.selftest()
        self.assertEqual(rc, 0, "ship_watch --selftest FAILED:\n" + buf.getvalue())

    def test_restart_on_OK_is_live_in_ship_watch(self):
        """D13's exact regression: cleared early, then bleeds. A no-restart
        design reads the CUMULATIVE llr as OK and never alarms."""
        import slot_sprt
        rows = [(1500 + 12 * i, 100 + i) for i in range(6)]
        r, m = rows[-1]
        rows += [(r - 8 * (i + 1), m + 1 + i) for i in range(10)]
        tape, *_ = self._tape(rows)
        _, verdict, _, _, _ = self.ship_watch.assess(tape)
        cumulative = slot_sprt.llr(rows[-1][0] - rows[0][0],
                                   rows[-1][1] - rows[0][1])
        self.assertGreaterEqual(cumulative, slot_sprt.bound(),
                                "fixture does not fool a no-restart design; "
                                "this test would pass for the wrong reason")
        self.assertEqual(verdict, "BLEED",
                         "ship_watch missed a post-clear bleed — restart-on-OK is gone")


# ---------------------------------------------------------------------------
# KEEP THIS BLOCK LAST IN THE FILE, ALWAYS.
#
# It used to sit in the middle (before `TestSlotRuleAndTheAlarmThatReportsIt`),
# so running this file as a SCRIPT -- which is exactly what the builder boot
# sequence prescribes -- collected only the 14 classes defined above it and
# reported "Ran 14 tests ... OK". The 18 below never ran, and they include
# ALL SIX guards on the stop-loss (`slot_rule` / `ship_watch` / `elo_logger`
# agreement) -- the rule that fired twice on 2026-08-09 and governs the live
# rollback. Every boot block on the tape records "14/14 OK" as though 14 were
# the file.
#
# That is s26 D17 in its purest form: THE TESTS WRITTEN BECAUSE ship_watch
# COULD NOT FIRE WERE NOT RUN BY THE PROCEDURE THAT REPORTED THEM GREEN.
# Found 2026-08-10 by an outside audit session, not by either working lane.
#
# The guard against a repeat is the assertion below, not this comment.
# ---------------------------------------------------------------------------

MODULE_TEST_FLOOR = 20   # classes in THIS file
SUITE_TEST_FLOOR = 32    # every test under tests/ -- what the boot check must run


if __name__ == "__main__":
    # Run the WHOLE tests/ directory, not just this module. The builder boot
    # sequence invokes this file directly, and before 2026-08-10 that executed
    # 14 of 32 tests while printing "OK" -- silently skipping `test_bot_helpers`
    # entirely AND every class below the old mid-file __main__ block.
    _mod = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    _suite = unittest.TestLoader().discover(start_dir=str(Path(__file__).parent))
    _m, _s = _mod.countTestCases(), _suite.countTestCases()
    if _m < MODULE_TEST_FLOOR or _s < SUITE_TEST_FLOOR:
        sys.stderr.write(
            f"REFUSING TO RUN: this module collected {_m} (floor {MODULE_TEST_FLOOR}), "
            f"the tests/ suite collected {_s} (floor {SUITE_TEST_FLOOR}).\n"
            "Either a class is defined after the __main__ block again, a test "
            "file stopped being discovered, or tests were deleted. Raise the "
            "floors DELIBERATELY when adding tests -- never lower them to go green.\n")
        raise SystemExit(1)
    _result = unittest.TextTestRunner(verbosity=1).run(_suite)
    raise SystemExit(0 if _result.wasSuccessful() else 1)
