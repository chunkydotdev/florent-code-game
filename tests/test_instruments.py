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
import os
import re
import subprocess
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

    def setUp(self):
        """Pin SLOT_STOP_LOSS: on for the mechanism tests. The LIVE
        PROGRAMME.md carries `off` (Magnus 2026-08-16, stop-loss retired) but
        the machinery is kept intact for the day the field flips back — these
        tests guard the machinery; test_the_retirement_switch guards the
        switch, in both directions."""
        import tempfile
        from pathlib import Path as _P
        on = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
        on.write("SLOT_STOP_LOSS: on\n")
        on.close()
        off = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
        off.write("SLOT_STOP_LOSS: off\n")
        off.close()
        self._prog_on, self._prog_off = _P(on.name), _P(off.name)
        self._saved_programme = (self.slot_rule.PROGRAMME_MD,
                                 self.elo_logger.PROGRAMME)
        self.slot_rule.PROGRAMME_MD = self._prog_on
        self.elo_logger.PROGRAMME = on.name

    def tearDown(self):
        self.slot_rule.PROGRAMME_MD, self.elo_logger.PROGRAMME = \
            self._saved_programme

    def test_the_retirement_switch_suppresses_and_restores_all_three(self):
        """Magnus 2026-08-16: SLOT_STOP_LOSS: off retires the stop-loss in
        EVERY implementation — slot_rule, ship_watch's alert (SPRT advisories
        included, they share the choke point), elo_logger's announcement.
        Driven both ways on the same bleeding tape: off suppresses all three,
        on restores all three. One direction alone would be vacuous."""
        rows = [(1500, 100 + i) for i in range(10)] + \
               [(1500 - 8 * (i + 1), 110 + i) for i in range(5)]   # net5 -40
        self.slot_rule.PROGRAMME_MD = self._prog_off
        self.elo_logger.PROGRAMME = str(self._prog_off)
        st, ship, elo = self._both(rows)
        self.assertFalse(st.slot_free, "slot_rule freed a slot while RETIRED")
        self.assertFalse(ship, "ship_watch alerted while RETIRED")
        self.assertFalse(elo, "elo_logger announced while RETIRED")
        self.assertEqual(st.net5, -40,
                         "diagnostics must keep computing while retired")
        self.slot_rule.PROGRAMME_MD = self._prog_on
        self.elo_logger.PROGRAMME = str(self._prog_on)
        st, ship, elo = self._both(rows)
        self.assertTrue(st.slot_free and ship and elo,
                        "flipping the field back ON must restore all three")

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
        — reimplementing it here would recreate the bug this test guards.

        ⛔ sys.argv IS PART OF THE PIN, AND LEAVING IT OUT MADE THIS HARNESS
        RUNNER-DEPENDENT (found s47, 2026-08-16). `elo_logger.main()` refuses
        any invocation with arguments (elo_logger.py:55 — `if len(sys.argv) > 1`,
        added so `--selftest` and typos cannot exit 0 in silence) and prints its
        usage instead of running. It therefore announced NOTHING whenever the
        RUNNER carried arguments:

            .venv/bin/python tests/test_instruments.py           argv==1  -> 158 OK
            .venv/bin/python -m unittest tests.test_instruments  argv==3  -> 3 FAIL

        The three failures were all `elo_logger announced NO slot-free`, i.e. the
        harness read a REFUSAL as a negative verdict — the vacuity this class
        exists to prevent, in the class's own helper. The fix is to pin argv the
        same way HIST/STATE/stdin are already pinned; the SEMANTICS of the rule
        are untouched. Guarded below by
        test_the_elo_logger_harness_is_runner_independent, which fails without
        this pin.
        """
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
        old_argv = sys.argv
        buf = io.StringIO()
        try:
            el.HIST, el.STATE, sys.stdin = tape, state.name, io.StringIO(payload)
            sys.argv = ["elo_logger.py"]      # the module's own no-argument contract
            with contextlib.redirect_stdout(buf):
                el.main()
        finally:
            el.HIST, el.STATE, sys.stdin = old_hist, old_state, old_stdin
            sys.argv = old_argv
            os.unlink(state.name)
        out = buf.getvalue()
        # NON-VACUITY: a REFUSAL is not a negative verdict. If the module printed
        # its no-arguments usage, this harness measured nothing and must say so
        # rather than return False — that False is exactly what hid the defect.
        if "takes NO arguments" in out:
            raise AssertionError(
                "elo_logger REFUSED the invocation (no-argument contract) instead "
                "of running — the argv pin above is broken, so every 'elo_logger "
                f"announced nothing' assert in this class is vacuous. Output:\n{out}")
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

    def test_the_elo_logger_harness_is_runner_independent(self):
        """The s47 defect, pinned: this class's verdict must not depend on how
        the SUITE was invoked.

        `elo_logger.main()` refuses argv with arguments. The harness reads that
        refusal as "did not announce", so with `python -m unittest ...` (argv
        length 3) three tests here failed while the same code passed under
        `python tests/test_instruments.py` (argv length 1). Both directions:
        a polluted argv must still announce (the pin works), and the harness
        must REFUSE to return a verdict at all if the pin ever comes out
        (the AssertionError in `_elo_logger_says_slot_free`).

        Without the argv pin this test FAILS — verified 2026-08-16 by removing
        the pin: `AssertionError: elo_logger REFUSED the invocation`.
        """
        rows = [(1500, 100 + i) for i in range(10)] + \
               [(1500 - 8 * (i + 1), 110 + i) for i in range(5)]   # net5 -40
        old = sys.argv
        try:
            sys.argv = ["runner", "tests.test_instruments", "-v", "--some-flag"]
            st, ship, elo = self._both(rows)
        finally:
            sys.argv = old
        self.assertTrue(st.slot_free, "fixture must be a firing one or this is vacuous")
        self.assertTrue(elo, "elo_logger did not announce under a polluted argv — "
                             "the harness is runner-dependent again")

    def test_a_restored_holder_refuses_the_widened_window(self):
        """The 2026-08-16 displacement class: a foreign hole inside a holder's
        run re-merges in holder_rows(), so base5 lands PAST the hole and the
        rule evaluates net5 over WINDOW+hole matches while carrying the
        WINDOW-calibrated threshold (-21 is -1 sd at 5 matches, -0.80 sd at 8).
        The rule must REFUSE (net5=None, the same path as an unfilled window),
        and the contiguous complement must STILL fire — both directions on
        matched series, or this test is vacuous."""
        import tempfile
        fh = tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False)
        fh.write(self.HDR)
        holed = [("v953", 1500, 1100), ("v953", 1500, 1101), ("v953", 1500, 1102),
                 ("v952", 1495, 1103), ("v952", 1495, 1104), ("v952", 1495, 1105),
                 ("v953", 1490, 1106), ("v953", 1480, 1107), ("v953", 1470, 1108)]
        for i, (tag, r, m) in enumerate(holed):
            fh.write(f"2026-01-01T00:{i:02d}\t{r}\t{m}\t{tag}\trank #1\n")
        fh.close()
        st = self.slot_rule.evaluate(fh.name)
        self.assertEqual(st.version, "v953")
        self.assertTrue(st.armed, "k spans the hole, so the holder IS armed here")
        self.assertIsNone(st.net5,
                          "base row is 6 matches back (past a 3-match foreign "
                          "hole); a WINDOW=5 rule must refuse, not widen")
        self.assertFalse(st.slot_free, "slot freed over a widened window")
        _, _, _, _, alert = self.ship_watch.assess(fh.name)
        self.assertIsNone(alert, "ship_watch alerted on a refused window")

        # The complement: same drop, contiguous rows — the refusal must not
        # have eaten the rule's ability to fire.
        rows = [(1500, 1100 + i) for i in range(4)] + \
               [(1500 - 10 * (i + 1), 1104 + i) for i in range(5)]  # net5 -50, span exactly 5
        st2, ship2, _ = self._both(rows, tag="v953")
        self.assertEqual(st2.net5, -50)
        self.assertTrue(st2.slot_free, "contiguous bleeding holder must still fire")
        self.assertTrue(ship2, "ship_watch must still alert on the contiguous case")

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


class TestClaimCheck(unittest.TestCase):
    """Every "mutation-tested" claim in tools/ must point at its own record.

    ADDED s28 after the builder wrote that claim THREE TIMES IN ONE DAY without
    committing the record -- panel2_cal.sh's header, the deficit-first count
    predicate, and panel3_cal.sh citing PANEL-2's leg doc. In all three the code
    was correct and the evidence was absent; all three were caught by another
    lane, none by the author.

    This lives in the boot suite deliberately. A prose rule saying "commit the
    record" is exactly the kind of convention D25 says has zero firings at
    birth -- and this one had three violations by its own enforcer inside eight
    hours. A test that runs every boot has a firing path.
    """

    def setUp(self):
        sys.path.insert(0, str(ROOT / "tools"))
        import claim_check
        self.mod = claim_check

    def test_the_checker_itself_can_fail(self):
        """It must flag an unbacked claim and a sibling citation, and stay
        silent otherwise -- otherwise its `ok` means nothing."""
        self.assertEqual(self.mod.selftest(), 0)

    def test_no_unbacked_claims_in_tools(self):
        unbacked = self.mod.check()
        self.assertEqual(
            unbacked, [],
            "a tools/ file claims a mutation test with no record naming it. "
            "Either commit the record (the record IS the test) or drop the "
            "claim:\n  " + "\n  ".join(unbacked),
        )


def _docstring_head(path):
    """First meaningful docstring line, read WITHOUT importing the module."""
    import ast as _ast
    try:
        d = _ast.get_docstring(_ast.parse(path.read_text()))
    except (SyntaxError, OSError):
        return None
    if not d:
        return None
    for line in d.splitlines():
        if line.strip():
            return line.strip()[:40]
    return None


class TestHelpContract(unittest.TestCase):
    """`--help` must be SAFE, SILENT-ON-SIDE-EFFECTS, and EXIT 0.

    ⛔ WHY THIS TEST EXISTS. Measured 2026-08-15: 40 of 86 files in tools/ had no
    argparse, so `--help` was an unrecognised argument and THE TOOL RAN. Seven of
    twelve sampled printed VERDICT-SHAPED text in this repo's own vocabulary:

        tools/freshness.py --help  ->  "BLIND: --help has no parseable timestamp"
        tools/leg_read.py  --help  ->  "LEG: no completed games"

    `BLIND` and the `LEG:` prefix are real verdicts here. A reader probing an
    unknown tool got back an authoritative sentence about nothing -- the single
    most likely source of "the session was confused from start to end", because
    the failure is INVISIBLE: nothing in the output says "this is not an answer".

    Three assertions, and the third is the one that actually protects data:
      1. exit 0 -- so a probe is not also an error
      2. non-empty stdout -- so the tool says what it is
      3. NO FILESYSTEM WRITES -- 21 of the 40 wrote files or shelled out
    """

    # Tools allowed to fail (1) and (2), each with the reason on the record.
    # ⚠ An exception list is how a contract rots, so each entry names WHY and is
    # asserted to still behave the way its exemption claims.
    EXEMPT = {
        "ring_retention.py": "RETIRED: refuses every invocation (exit 2) and "
                             "prints its replacement. The refusal IS its help.",
    }

    def _tools(self):
        return sorted((ROOT / "tools").glob("*.py"))

    def _fs_signature(self):
        sig = {}
        for d in ("scratchpad", "corpus", "."):
            for f in (ROOT / d).glob("*"):
                if f.is_file():
                    try:
                        sig[str(f)] = f.stat().st_mtime_ns
                    except OSError:
                        pass
        return sig

    # Paths owned by the LIVE FLEET, not by any tool under test. A timing
    # control alone cannot cover these: `corefill.log` is written every 60s and
    # a 6-second control window misses it, so it was attributed to game_census
    # -- a tool that never opens it. Named here rather than excluded silently,
    # because a widened window would also hide a REAL slow write.
    DAEMON_WRITTEN = (
        "corefill.log", "corefill_forever.log", "watchdog.log",
        "watchdog.launchd.out", "watchdog.launchd.err",
        "auto_gate.log", "fleet_dispatch.log", "ship_watch.log",
        "ship_watch_state.json", "vps_pull.log", "cores_idle.log",
        "cores_idle_state.json", "cpu_watch.log", "cpu_watch_state.json",
        "keeper.log", "keeper.out", "keeper_state.json", "breakin_watch.log",
        "elo_history.tsv", "elo_logger.log", "match_watcher.log",
        "opp_watcher.log", "replay_archiver.log",
        # Corpus tables the KEEPER rebuilds each sync cycle (~30 min, so the
        # 6s churn window cannot learn them). Observed 2026-08-16:
        # corpus/join.tsv rewritten mid-suite and attributed to camp_detect/
        # ceiling/choke_census — tools that never open it. join.tsv's suffix
        # also covers meta_join.tsv, which is keeper-owned too.
        "corpus/join.tsv", "corpus/ladder_games.tsv",
        "corpus/league_matches.tsv", "corpus/manifest.json",
    )
    # Session-NUMBERED daemon logs a static filename list cannot cover: the
    # side lane's drift watch writes `drift_watch_s<NN>.log` on a ~60s cadence,
    # so the 6s churn control misses it and the suffix list above cannot name
    # it in advance. Observed 2026-08-16: `drift_watch_s44.log` attributed to
    # collar_census.py — a tool that never opens it — making the suite flaky
    # whenever a probe overlapped the daemon's write.
    DAEMON_PATTERNS = (r"drift_watch_s\d+\.log$",)

    def _background_churn(self, seconds=6.0):
        """Paths that change on their own, with no tool running.

        ⛔ WITHOUT THIS CONTROL THE TEST IS A FALSE-POSITIVE MACHINE, and it
        produced three on its first run: `corpus/ship_watch.log`,
        `corpus/vps_pull.log` and `corpus/cores_idle_state.json` were attributed
        to game_census/stub_engine/triarm_read, which touch none of them. They
        are written by the LIVE DAEMONS every few seconds.

        ⭐ This is the repo's own "a measurement of a moving base is a
        measurement onto a snapshot" (side-lane retro s43, Q4) landing on a
        test written the same day. The control is the fix: learn which paths
        move by themselves, then attribute only the rest.
        """
        import time
        before = self._fs_signature()
        time.sleep(seconds)
        after = self._fs_signature()
        return {k for k in after if before.get(k) != after.get(k)} | set(after) - set(before)

    def test_help_is_safe_and_exits_zero(self):
        churn = self._background_churn()
        bad_exit, empty, wrote, not_help = [], [], [], []
        for f in self._tools():
            before = self._fs_signature()
            try:
                r = subprocess.run([sys.executable, str(f), "--help"],
                                   capture_output=True, text=True, timeout=120)
            except subprocess.TimeoutExpired:
                bad_exit.append(f"{f.name}: TIMED OUT on --help (it ran for real)")
                continue
            after = self._fs_signature()
            touched = [k for k in after
                       if before.get(k) != after.get(k) and k not in churn
                       and not k.endswith(self.DAEMON_WRITTEN)
                       and not any(re.search(p, k) for p in self.DAEMON_PATTERNS)]
            if touched:
                wrote.append(f"{f.name}: WROTE {touched[:3]}")
            if f.name in self.EXEMPT:
                continue
            if r.returncode != 0:
                bad_exit.append(f"{f.name}: exit {r.returncode} :: "
                                f"{((r.stdout or '') + (r.stderr or ''))[:70]!r}")
            out = r.stdout or ""
            if not out.strip():
                empty.append(f"{f.name}: printed nothing")
                continue
            # ⭐ THE ASSERTION THAT ACTUALLY CATCHES THE ORIGINAL DEFECT.
            # exit 0 + non-empty output CANNOT distinguish "printed its help"
            # from "ran for real and printed a verdict" -- and the original bug
            # was precisely a tool running and printing verdict-shaped text.
            # Proven by mutation: stripping the guard from leg_read.py left the
            # first three assertions GREEN, because `LEG: no completed games`
            # is exit 0 and non-empty. The output must be traceable to the
            # tool's OWN documentation: argparse's `usage:` or its docstring.
            head = _docstring_head(f)
            if "usage:" not in out.lower() and (not head or head not in out):
                not_help.append(f"{f.name}: --help printed something that is "
                                f"neither a usage line nor its docstring "
                                f"({out.strip()[:60]!r}) — it probably RAN")

        # (3) first: a --help that mutates state is the dangerous one.
        self.assertEqual(wrote, [], "\n⛔ --help MUTATED THE FILESYSTEM. A probe "
                         "must never be an action:\n  " + "\n  ".join(wrote))
        self.assertEqual(bad_exit, [], "\n⛔ --help did not exit 0. Add the guard "
                         "block (see any tool in tools/) or an EXEMPT entry with a "
                         "reason:\n  " + "\n  ".join(bad_exit))
        self.assertEqual(empty, [], "\n⛔ --help printed nothing. A tool must say "
                         "what it is:\n  " + "\n  ".join(empty))
        self.assertEqual(not_help, [], "\n⛔ --help RAN THE TOOL instead of "
                         "describing it. This is the original defect:\n  "
                         + "\n  ".join(not_help))

    def test_the_exemptions_still_behave_as_claimed(self):
        """An exemption that has stopped being true is a hole, not an exception."""
        f = ROOT / "tools" / "ring_retention.py"
        if not f.exists():
            self.skipTest("ring_retention.py removed")
        r = subprocess.run([sys.executable, str(f), "--help"],
                           capture_output=True, text=True, timeout=60)
        self.assertNotEqual(r.returncode, 0,
                            "ring_retention.py now exits 0 — it is no longer "
                            "'retired and refusing', so drop its EXEMPT entry.")
        self.assertIn("RETIRED", (r.stdout or "") + (r.stderr or ""),
                      "ring_retention.py no longer announces its retirement.")

    def test_the_guard_does_not_fire_on_import(self):
        """The guard is `__main__`-gated; an import must not swallow --help.

        Without the gate, `now.py --help` would import freshness, freshness's
        guard would see `--help` in the PARENT's argv, print freshness's
        docstring and exit 0 — the parent silently replaced by its dependency.
        """
        r = subprocess.run(
            [sys.executable, "-c",
             "import sys; sys.argv = ['x', '--help']; sys.path.insert(0, %r);"
             "import freshness; print('IMPORT_SURVIVED')" % str(ROOT / "tools")],
            capture_output=True, text=True, timeout=60)
        self.assertIn("IMPORT_SURVIVED", r.stdout,
                      "importing a tool with --help in argv exited early:\n"
                      + (r.stdout or "") + (r.stderr or ""))


class TestWatchdog(unittest.TestCase):
    """`tools/watchdog.sh` — the OS-level supervisor for the supervisors.

    ⛔ WHY THESE EXIST. When the watchdog was built (2026-08-15) it was verified
    ONLY by live end-to-end runs, and that gap was stated rather than closed:
    **nothing failed if `AbandonProcessGroup` was removed from the plist.**
    Without that key launchd REAPS the job's children on exit, so the watchdog
    restarts a daemon, logs `CONFIRMED alive` 3 seconds later (true at that
    instant), exits, and launchd immediately kills what it just started.
    ⇒ **The log reads healthier than doing nothing at all.** A self-confirming
    no-op is the worst failure a watchdog can have, and it is invisible.
    """

    WD = ROOT / "tools" / "watchdog.sh"
    PLIST = ROOT / "tools" / "watchdog.plist"

    def _run(self, fixture_json, extra_env=None, args=()):
        """Drive watchdog.sh against a FIXTURE fleet_health, not the live fleet."""
        import json as _json
        import tempfile
        fx = Path(tempfile.mktemp(suffix=".json"))
        fx.write_text(_json.dumps(fixture_json))
        log = Path(tempfile.mktemp(suffix=".log"))
        env = dict(os.environ,
                   WATCHDOG_LOG=str(log),
                   WATCHDOG_FH=f"cat {fx}")
        env.update(extra_env or {})
        r = subprocess.run(["zsh", str(self.WD), *args], capture_output=True,
                           text=True, timeout=120, env=env, cwd=ROOT)
        return r, (log.read_text() if log.exists() else "")

    @staticmethod
    def _row(label, state, auto, found=0, pids=(), fix="true"):
        return {"label": label, "state": state, "found": found,
                "expected": 1, "pids": list(pids), "auto": auto,
                "fix": fix, "why": "test fixture"}

    def test_blind_refuses_and_does_not_act(self):
        """An unreadable process table is UNKNOWN. Acting on it would start a
        second copy of every daemon — the worst available move."""
        r, log = self._run({"blind": True, "problems": 0, "rows": []})
        self.assertEqual(r.returncode, 2, f"expected rc 2 on BLIND, log:\n{log}")
        self.assertIn("BLIND", log)
        self.assertNotIn("RESTARTING", log)

    def test_zero_actionable_says_so_rather_than_going_silent(self):
        """A silent no-op is indistinguishable from a working pass. Two real
        launchd passes did exactly that on 2026-08-15."""
        r, log = self._run({"blind": False, "problems": 0,
                            "rows": [self._row("keeper", "ok", True, found=1)]})
        self.assertEqual(r.returncode, 0)
        self.assertIn("PASS COMPLETE: 0 actionable", log)

    def test_duplicates_are_reported_but_never_killed(self):
        """Choosing which of two live daemons dies is a human judgement."""
        r, log = self._run({"blind": False, "problems": 1, "rows": [
            self._row("auto_gate --apply", "DUPLICATE", False, found=2,
                      pids=[111, 222])]})
        self.assertIn("DUPLICATE (NOT killed, by policy)", log)
        self.assertIn("kill 222", log, "must nominate the NEWCOMER for a human")
        self.assertNotIn("RESTARTING", log)

    def test_missing_but_not_auto_is_left_for_a_human(self):
        """AUTO is a safety boundary: a wrong restart of these costs data."""
        r, log = self._run({"blind": False, "problems": 1, "rows": [
            self._row("shard runners", "MISSING", False)]})
        self.assertIn("NOT auto-restartable", log)
        self.assertNotIn("RESTARTING", log)

    def test_missing_and_auto_is_restarted_and_confirmed(self):
        """The one path that acts. The fix command must actually be run."""
        import tempfile
        marker = Path(tempfile.mktemp())
        r, log = self._run({"blind": False, "problems": 1, "rows": [
            self._row("keeper", "MISSING", True, fix=f"touch {marker}")]})
        self.assertIn("RESTARTING (MISSING + AUTO): keeper", log)
        self.assertTrue(marker.exists(),
                        f"the fix command was never executed. log:\n{log}")

    def test_a_deliberate_pause_is_never_undone(self):
        """If automation can undo COREFILL_STOP, the pause button is a lie."""
        stop = ROOT / "scratchpad" / "COREFILL_STOP"
        pre_existing = stop.exists()
        if not pre_existing:
            stop.touch()
        try:
            r, log = self._run({"blind": False, "problems": 1, "rows": [
                self._row("keeper", "MISSING", True, fix="echo SHOULD_NOT_RUN")]})
            self.assertIn("PAUSED", log)
            self.assertNotIn("RESTARTING", log)
        finally:
            if not pre_existing:
                stop.unlink(missing_ok=True)

    def test_plist_carries_AbandonProcessGroup(self):
        """⛔ THE NAMED GAP THIS CLASS WAS WRITTEN TO CLOSE.

        Without this key the watchdog is WORSE than useless: it reports
        successful restarts of daemons launchd then immediately kills.
        """
        # ⛔ PARSE THE PLIST, DO NOT GREP IT. The first version searched the raw
        # text and asserted `<true/>` within 120 chars of the first match of the
        # string "AbandonProcessGroup" — which later matched a COMMENT
        # mentioning the key by name, and the test went red on a plist that was
        # correct, installed, and reporting `abandon process group` in
        # `launchctl print`. A guard that fails on prose about itself is not
        # checking the artefact.
        import plistlib
        self.assertTrue(self.PLIST.exists(), "watchdog.plist is missing")
        with self.PLIST.open("rb") as fh:
            pl = plistlib.load(fh)
        self.assertIs(pl.get("AbandonProcessGroup"), True,
                      "⛔ watchdog.plist lost AbandonProcessGroup (or it is not "
                      "true). launchd will reap every daemon the watchdog "
                      "starts, and the log will still say CONFIRMED alive.")

    def test_plist_paths_still_resolve(self):
        """launchd has no working directory and no shell profile: an absolute
        path that has gone stale makes the agent fail SILENTLY."""
        import plistlib
        with self.PLIST.open("rb") as fh:
            # strip the XML comment block plistlib rejects? it does not — comments are legal
            pl = plistlib.load(fh)
        args = pl["ProgramArguments"]
        self.assertTrue(Path(args[0]).exists(), f"interpreter missing: {args[0]}")
        self.assertTrue(Path(args[1]).exists(),
                        f"⛔ watchdog.plist points at {args[1]}, which does not "
                        "exist. The repo moved and the agent is silently dead.")
        self.assertTrue(Path(pl["WorkingDirectory"]).exists())


class LiveProgrammeLineDirsInvariant(unittest.TestCase):
    """The one live-file check in this suite, on purpose.

    gate.py's selftest is fixture-only by design, so a stale LINE_DIRS (an
    INCUMBENT no pattern matches) is invisible to it — and that exact state
    held for ~47h across s44-s46 (incumbent _v223sealrepair, patterns capped
    at v199) with 26/27 batteries bypassing the gate via --off-programme.
    This suite runs at every lane's boot, so the invariant fires at the next
    boot after the naming convention outruns the patterns, instead of sitting
    for days. (Side lane finding, 2026-08-16, f1b04e7e.)
    """

    def test_live_incumbent_matches_line_dirs(self):
        from gate import incumbent_matches_line_dirs
        raw = (ROOT / "PROGRAMME.md").read_text()
        got = incumbent_matches_line_dirs(raw)
        self.assertIsNotNone(got, "PROGRAMME.md lost its INCUMBENT or LINE_DIRS field")
        self.assertTrue(got, "LINE_DIRS STALE: the live INCUMBENT matches no "
                             "LINE_DIRS pattern — widen LINE_DIRS (Magnus's "
                             "directive) before trusting any gate refusal")

    def test_checker_fires_on_the_historical_stale_line_dirs_state(self):
        # "line_dirs" is in the NAME on purpose: the side lane found that
        # `-k line_dirs` — the natural filter for this invariant — silently
        # skipped this twin under its old name. A twin a filter drops is the
        # same shape as a guard nobody invokes.
        # The negative twin: the exact pre-widening s46 state must FAIL the
        # invariant, or the live test above has never been seen to check.
        from gate import incumbent_matches_line_dirs
        stale = ("    LINE_DIRS: bots/_v105loki1 bots/_v10?loki* "
                 "bots/_v1??loki* bots/_v1[3-9]?*\n"
                 "    INCUMBENT: bots/_v223sealrepair\n")
        self.assertFalse(incumbent_matches_line_dirs(stale))
