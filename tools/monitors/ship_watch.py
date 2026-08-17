#!/usr/bin/env python3
"""Ship watch — evaluate the live holder against the ladder stop-loss, and SAY SO.

WHY THIS EXISTS. Monitors in this project survive session resets; the SESSION
does not. `elo_logger` records the tape and `keeper` ingests replays, but
nothing was evaluating the SLOT DECISION onto a DURABLE SURFACE — `elo_logger`
prints its wake to stdout, and the arming loop has no redirect, so on a detached
monitor that print goes to the terminal of a session that no longer exists.
"Named wake path or state there is none" is a standing rule here. A print into
the void is "there is none" wearing a wake path's clothes. This is the fix: the
alarm is a FILE in the repo, `corpus/SHIP_ALERT`.

WHAT IT EVALUATES — the RULE first, the advisory second.

  1. THE RULE (`tools/slot_rule.py`): rolling last-5 net <= -21, armed after the
     holder's 8th match. This is what writes SHIP_ALERT. It is the stop-loss in
     ship-gate.md and in `elo_logger`; this file does not get its own opinion.
  2. THE ADVISORY (`tools/slot_sprt.py`): the sequential test, WITH
     RESTART-ON-OK, via `slot_sprt.run_sprt` — imported, never re-derived.

=== THE BUG THIS FILE SHIPPED WITH, 2026-08-09, AND WHAT IT COST ===

The first version imported the SPRT's CONSTANTS and then hand-rolled its
SEGMENTATION: one `(net, k)` measured from a fixed activation baseline to the
latest row, forever. `slot_sprt.run_sprt` restarts the segment on every OK
acceptance, and its comment says exactly why — the no-restart design missed v56,
which "cleared at k=3 then bled -38". ship_watch reintroduced that miss.

Measured on the live v102 numbers before the fix: once cleared at k=10, a bleed
of -5 Elo/match for 40 matches — 1584 down to 1384, off the ladder — logged
**CLEARED at every single evaluation**. The first BLEEDING verdict needed
-8/match sustained 40 matches, at which point the rating is 1264.

The docstring of the broken version already contained the sentence "a stop-loss
that cannot fire is worse than none, because its silence reads as safety." It
fixed that in the constants and reintroduced it in the segmentation. THE LESSON
IS NOT "IMPORT THE CONSTANTS." IT IS "IMPORT THE TEST." Anything you retype is
a second implementation, and the second implementation is the one nobody tests.

Hence `--selftest`, which corrupts the input and REQUIRES the alarm, including
the specific cleared-then-bleeds regression above. Run it after any edit here.

    .venv/bin/python tools/monitors/ship_watch.py --selftest

CADENCE. 10 min; ladder slots fire every ~10 min, so a faster loop re-tests the
same data. Arm detached from the repo root:

    while true; do .venv/bin/python tools/monitors/ship_watch.py; sleep 600; done

SHIP_BASELINE / SHIP_VERSION are OPTIONAL and REPORTING-ONLY now. The alarm
reads the holder's own run off the tape, so it cannot be armed against a wrong
baseline. (It was: v102 was armed at 1577.5, which is the rating before v101's
LAST game — the platform's per-match `teamAVersion` says so. The true activation
rating was 1567.44. The tape row tagged v102 is not the first v102 MATCH.)
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
LOG = ROOT / "corpus" / "ship_watch.log"
ALERT = ROOT / "corpus" / "SHIP_ALERT"
STATE = ROOT / "corpus" / "ship_watch_state.json"
LADDER = ROOT / "corpus" / "ladder_games.tsv"   # denominators only, never the rule

sys.path.insert(0, str(ROOT / "tools"))
import slot_rule
from freshness import assert_fresh                              # noqa: E402  the RULE
import slot_sprt                              # noqa: E402  the ADVISORY
import slot_denoms                            # noqa: E402  the DENOMINATORS (s33)
from slot_sprt import bound, run_sprt, MU0, ALPHA   # noqa: E402

BOUND = bound()


def _n5(v) -> str:
    """net5 is None until the holder's window fills. Formatting it without a
    guard crashed --selftest under a mutated WINDOW — a diagnostic that dies on
    a degenerate input is a diagnostic that stops reporting exactly when
    something is wrong."""
    return "n/a" if v is None else f"{v:+.1f}"


def assess(tape, version=None, baseline=None, ctx=None, baseline_version=None):
    """Return (state, sprt_verdict, sprt_events, line, alert_text|None).

    The rule decides the alarm. The SPRT is reported alongside it and never
    suppresses it — an advisory that can veto a rule is not an advisory.

    `baseline_version` is the holder the `baseline` fallback BELONGS TO (the
    state file's / SHIP_VERSION's own version tag). See the REFUSED-STALE block
    below: a baseline whose owner is not the live holder is refused outright.
    """
    st = slot_rule.evaluate(tape, version)
    if st is None or st.k <= 0:
        return None, None, None, None, None

    # BOTH bounds, reported separately and never merged into one word — they
    # answer different questions (fast = collapsing now, slow = bleeding
    # steadily) and collapsing them would hide which one fired.
    pair = slot_sprt.run_both(st.rows, ALPHA)
    verdict, events, _, _ = run_sprt(st.rows, MU0, ALPHA)

    n5 = _n5(st.net5)
    # ⛔ THE BASELINE IS DERIVED, NOT PASSED — s33 2026-08-12. `SHIP_BASELINE`
    # is a HAND-SET env var and on 2026-08-12 it was 1689, which is `ourbef` of
    # v112's LAST match (1688.8986); v114's FIRST match carries 1685.6150, so a
    # v112 game costing -3.28 was being credited to v114's drawdown. That is the
    # defect this file documents at :52-54 for v102/v101 -- the repair hardened
    # the ALARM (cell 6) and left the REPORTING column on the env var, and the
    # reporting column is the one TWO LANES MISREAD WITHIN ONE HOUR that day.
    # `net_act_src` is printed so a successor can see which number they have.
    _ctx = ctx or {}
    derived = _ctx.get("baseline_derived")
    if derived is None and _ctx.get("ladder"):
        derived = slot_denoms.activation_baseline(st.version, _ctx["ladder"])
    # ⛔ THE FALLBACK IS REFUSED WHEN ITS OWNER IS NOT THE LIVE HOLDER — s50
    # 2026-08-17. `corpus/ship_watch_state.json` read {"version": "v116",
    # "baseline": 1655.0} while the tape's holder was v160 at ~1822: THREE
    # holders stale. It was inert only because the derivation off
    # `ladder_games.tsv` happened to be succeeding; drive the derivation to
    # fail (unreadable ladder, or a holder with no ladder rows yet — which is
    # exactly the state a FRESHLY SHIPPED bot is in) and the same code emitted
    # `net_act=+186.0 net_act_src=env`, a confident number off a dead constant.
    # That is the identical defect this file already documents at :52-54 (v102
    # armed at v101's baseline) and at :106-113 (v114 charged with v112's game),
    # arriving a third time through the one path those two repairs left open.
    # ⭐ REFUSE, DO NOT GUESS — the same discipline as the tape's STALE branch:
    # the column reads UNKNOWN and NAMES the disagreement, so a reader cannot
    # mistake a withheld number for a measured one. FAIL-OPEN as ever: this is
    # a DIAGNOSTIC column, so a refusal must never touch the RULE (driven).
    if derived is not None:
        base_act, src = derived, "derived"
    elif baseline is None:
        base_act, src = None, "none"
    elif baseline_version is not None and baseline_version != st.version:
        base_act, src = None, f"REFUSED-STALE({baseline_version}!={st.version})"
    else:
        base_act, src = baseline, "env"
    net_act = ("\tnet_act=UNKNOWN" if base_act is None and src.startswith("REFUSED")
               else "" if base_act is None else
               f"\tnet_act={st.rating - base_act:+.1f}")
    ruling = ("SLOT FREE" if st.slot_free else
              # Magnus 2026-08-16: SLOT_STOP_LOSS: off — the rule computes but
              # never rules; say RETIRED, not "held", so a reader cannot
              # mistake suppression for health.
              "RETIRED" if not slot_rule.stop_loss_active() else
              "held" if st.armed else "unarmed")
    # LEVEL, not just slope. net5 is a five-match SLOPE and it RELAXES as a bad
    # result ages out of the window: on 2026-08-09 v102 fell 6 Elo while net5
    # IMPROVED 7, and "recovering" was reported off it. Worse, a steady bleed
    # slower than -4.2/match holds net5 above -21 forever — measured, a -4.0
    # bleed loses 240 Elo over 60 matches and trips neither this rule nor the
    # SPRT. The drawdown column cannot fix that (the alarm still belongs to the
    # rule) but it makes the blind spot legible instead of invisible.
    peak = max(r for _, r, _ in st.rows)
    # ---- THE DENOMINATORS, s33 2026-08-12 -----------------------------------
    # The comment above says the drawdown column "makes the blind spot legible".
    # It did not: it was printed with NO n and NO base rate, and :112 instructs
    # the reader "Check DRAWDOWN, not net5" -- correct advice with a missing
    # denominator, which is how two lanes independently alarmed on drawdown=-36
    # at k=27, a value inside ONE sd. Three columns close that:
    #   dd_z          the drawdown in units of its own noise
    #   resolvable_k  matches this holder's OBSERVED rate would need to be called
    #                 ⚠ IT RISES AS THE OBSERVED EFFECT SHRINKS, AND THAT IS
    #                 CORRECT BUT READS BACKWARDS. Observed live within 10
    #                 minutes of shipping: k=29 -> 107, k=30 -> 144. Nothing got
    #                 worse; the holder's mean/match got SMALLER (-45.6/29 ->
    #                 -40.6/30), and a smaller effect needs more matches to call.
    #                 So a RISING resolvable_k beside a SHRINKING |net_act| is
    #                 mildly GOOD news, and a reader watching the column climb
    #                 will infer the opposite. Written here because every defect
    #                 this session was a number printed without the sentence that
    #                 makes it readable, and this column is mine.
    #   p_null        how often a bot with NO EFFECT would have freed the slot
    #                 by now -- 14% at k=8, 75% at k=27, 97% at k=60
    # ⭐ p_null INVERTS HOW THE RULING READS: `SLOT FREE` is close to
    # uninformative on its own (it is the MAJORITY outcome for a neutral holder
    # by k=27) and `RULE=held` is the informative half. See
    # docs/research/SPEC-slot-rule-base-rate-2026-08-12.md.
    # ⛔ FAIL-OPEN BY CONSTRUCTION: every helper returns None rather than
    # raising, and the columns print `NA`. A monitor that dies because its
    # DIAGNOSTIC could not be computed is worse than one without the diagnostic.
    ivs = _ctx.get("intervals") or []
    sd_pm = slot_denoms.sd_of(ivs)
    peak_m = max((m for _, r, m in st.rows if r == peak), default=None)
    k_dd = None if peak_m is None else st.matches - peak_m
    ddz = slot_denoms.dd_z(st.rating - peak, k_dd, sd_pm) if k_dd else None
    rate = ((st.rating - base_act) / st.k
            if base_act is not None and st.k else None)
    res_k = slot_denoms.resolvable_k(rate, sd_pm)
    p0 = slot_denoms.p_null(st.k, ivs) if ivs else None
    # fa_union is the figure the ship preregs REQUIRE at read-out (audit M2);
    # p_null (net5 alone) is kept beside it because existing readers parse it.
    fu = slot_denoms.fa_union(st.k)
    fu_s = "NA" if fu is None else f"{fu[0]:.2f}" + ("+" if fu[1] else "")
    _na = lambda v, f: "NA" if v is None else format(v, f)
    denoms = (f"\tdd_z={_na(ddz, '+.2f')}\tdd_k={_na(k_dd, 'd')}"
              f"\tresolvable_k={_na(res_k, '.0f')}\tfa_union={fu_s}"
              f"\tp_null={_na(p0, '.2f')}"
              f"\tsd_pm={_na(sd_pm, '.2f')}\tnet_act_src={src}"
              # THE SECOND FILE THIS MONITOR NOW READS GETS ITS AGE PRINTED,
              # under the same standing rule the tape's `tape_age_min` serves:
              # "a monitor that reads a file must report that file's FRESHNESS."
              # A stale ladder table cannot make the RULE wrong (the rule reads
              # the elo tape) but it silently ages `sd_pm` and can leave a new
              # holder's baseline UNDERIVED — both visible here instead of not.
              f"\tlg_age_min={_na(_ctx.get('ladder_age_min'), '.1f')}")
    # ⛔ UTC WITH AN EXPLICIT `Z`, s30 2026-08-11. This line stamped LOCAL CEST
    # with NO zone marker for the whole life of the file -- read naively as UTC
    # it reports rows from the FUTURE, which is precisely how stale data looks
    # live, and it is the hazard three lanes have flagged all session.
    # It was changed the same hour the BLIND line was added, because that line
    # is UTC-marked and a log carrying TWO conventions is worse for a reader
    # than either uniform one: sorted chronologically, a BLIND row would land
    # ~2 hours BEFORE the verdicts that bracket it, so the one row saying "I was
    # blind here" sorts away from the window it describes. The convention change
    # is recorded IN THE LOG by a one-time marker row (see _mark_convention),
    # because a log that silently switches clocks mid-file is its own trap.
    line = (f"{datetime.now(timezone.utc):%Y-%m-%dT%H:%M:%S}Z\t{st.version}\t"
            f"k={st.k}\trating={st.rating:.0f}\tnet5={n5}\t"
            f"peak={peak:.0f}\tdrawdown={st.rating - peak:+.1f}\t"
            f"armed={st.armed}\tRULE={ruling}\t"
            f"sprt_fast={pair['fast']}\tsprt_slow={pair['slow']}{net_act}{denoms}")

    alert = None
    if st.slot_free:
        alert = (
            line + "\n\n"
            f"THE SLOT RULE HAS FREED THE SLOT: {st.version} rolling last-5 net "
            f"{n5} (<= {slot_rule.SWAP_THRESHOLD}) after {st.k} matches.\n"
            "This is a STOP-LOSS and a WAKE, not an evaluation of the bot — it\n"
            "permits a swap, it does not order one.\n"
            "ROLLBACK: .venv/bin/fcode submission activate <rollback version>\n"
            "See HANDOVER.md for the current rollback target.\n")
    elif "BLEED" in pair.values():
        which = [k for k, v in pair.items() if v == "BLEED"]
        why = {"fast": f"a COLLAPSE (MU0={slot_sprt.MU0:+.0f}/match)",
               "slow": f"a STEADY BLEED (MU0={slot_sprt.MU0_SLOW:+.0f}/match) — the "
                       "hole net5 cannot see"}
        alert = (
            line + "\n\n"
            f"SPRT ADVISORY accepted BLEED for {st.version} on the "
            f"{'/'.join(which)} bound: " + "; ".join(why[k] for k in which) + ".\n"
            f"The -21 rolling-5 rule has NOT freed the slot (net5 {n5}); the rule\n"
            "is the rule. This is the statable-error-rate read, raised because a\n"
            "sequential test accepting bleed is worth a human look.\n"
            "NOTE the slow bound exists because a steady bleed slower than\n"
            "-4.2/match holds net5 above -21 FOREVER: -4.0/match is -240 Elo over\n"
            "60 matches with the rule silent throughout. Check DRAWDOWN, not net5.\n")
    # Magnus 2026-08-16 (SLOT_STOP_LOSS: off): no stop-loss alarm of ANY kind
    # — the slot-free path is already dead inside slot_rule, and this nulls
    # the SPRT bleed ADVISORIES too, which are stop-loss-family wakes. The
    # log line keeps every diagnostic; only the alarm is withheld. Single
    # choke point, here, so every consumer of assess() inherits it.
    if alert is not None and not slot_rule.stop_loss_active():
        alert = None
    return st, verdict, events, line, alert


def selftest() -> int:
    """Corrupt the input; require the alarm. Every case here is a bug this file
    or its ancestor actually had."""
    hdr = "ts\trating\tmatches\tversion\trank\n"

    # ⭐ PIN THE STOP-LOSS ON for the mechanism cells below: the live
    # PROGRAMME.md may carry SLOT_STOP_LOSS: off (Magnus 2026-08-16), and
    # these cells test the MACHINERY, which is kept intact for the day the
    # field flips back. The off-state gets its own driven cell at the end.
    # ⛔ THE FOUR LEADING SPACES ARE LOAD-BEARING (s47, 2026-08-16). PROGRAMME.md
    # fields are INDENTED lines and nothing else — prose that happens to contain
    # `SLOT_STOP_LOSS: off` must not move a live rule, which is what the unified
    # parse in tools/programme.py enforces. These fixtures were unindented, so
    # they had the shape a real PROGRAMME.md CANNOT have; matching the real file
    # is the point of a fixture.
    _prog_on = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
    _prog_on.write("    SLOT_STOP_LOSS: on\n")
    _prog_on.close()
    _prog_off = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
    _prog_off.write("    SLOT_STOP_LOSS: off\n")
    _prog_off.close()
    _real_programme = slot_rule.PROGRAMME_MD
    slot_rule.PROGRAMME_MD = Path(_prog_on.name)

    def tape(pairs, tag="v900"):
        fh = tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False)
        fh.write(hdr)
        for i, (r, m) in enumerate(pairs):
            fh.write(f"2026-01-01T00:{i:02d}\t{r}\t{m}\t{tag}\trank #1\n")
        fh.close()
        return fh.name

    fails = []

    def check(name, cond, detail=""):
        print(f"  [{'ok  ' if cond else 'FAIL'}] {name}{'  ' + detail if detail else ''}")
        if not cond:
            fails.append(name)

    print("ship_watch --selftest")

    # 1. Healthy holder: rising rating, armed. No alarm.
    t = tape([(1500 + 3 * i, 100 + i) for i in range(15)])
    st, v, _, _, alert = assess(t)
    check("healthy holder raises no alarm", alert is None, f"net5={_n5(st.net5)}")

    # 2. THE GOVERNING RULE HAS TEETH: armed holder, last-5 net -40.
    rows = [(1500, 100 + i) for i in range(10)] + \
           [(1500 - 8 * (i + 1), 110 + i) for i in range(5)]
    t = tape(rows)
    st, v, _, _, alert = assess(t)
    check("armed holder at net5 -40 FREES THE SLOT", st.slot_free and alert is not None,
          f"net5={_n5(st.net5)}")
    check("...and the alert text names the rule",
          alert is not None and "SLOT RULE HAS FREED THE SLOT" in alert)

    # 3. THE REGRESSION THAT SHIPPED: cleared early, then bleeds.
    #    v56 shape — clears at low k, then bleeds. The no-restart design logs
    #    CLEARED forever; run_sprt must restart on OK and catch it.
    #
    #    THIS FIXTURE IS TUNED TO DISCRIMINATE, and the first draft was not.
    #    A bleed deep enough (-9/match for 30) is caught by the BROKEN design
    #    too, because it swamps the prior gain — so that fixture proved nothing
    #    about restart-on-OK while appearing to pass. Mutation testing caught it.
    #    Here the prior gain (+60) keeps the CUMULATIVE llr firmly in OK
    #    territory (+7.6) while the POST-CLEAR SEGMENT alone accepts BLEED
    #    (-2.34). Only a design that restarts can see it.
    rows = [(1500 + 12 * i, 100 + i) for i in range(6)]        # +60 fast: clears
    last_r, last_m = rows[-1][0], rows[-1][1]
    rows += [(last_r - 8 * (i + 1), last_m + 1 + i) for i in range(10)]   # -80 over 10
    t = tape(rows)
    st, v, events, _, alert = assess(t)
    cum = slot_sprt.llr(rows[-1][0] - rows[0][0], rows[-1][1] - rows[0][1])
    check("cleared-then-bleeds is CAUGHT (restart-on-OK)", v == "BLEED",
          f"sprt={v} cumulative_llr={cum:+.2f} (a no-restart design reads this and says OK)")
    check("...and the fixture really does fool the no-restart design", cum >= BOUND,
          f"cumulative llr {cum:+.2f} >= +{BOUND:.2f}")
    check("...and cleared-then-bleeds raises an alarm", alert is not None)

    # 4. Unarmed holder cannot free the slot however bad the window looks.
    rows = [(1500, 100), (1400, 101), (1300, 102), (1200, 103),
            (1100, 104), (1000, 105), (900, 106)]
    t = tape(rows)
    st, v, _, _, alert = assess(t)
    check("unarmed holder never frees the slot", not st.slot_free,
          f"k={st.k} armed={st.armed}")

    # 5. A holder change resets the window: the PREVIOUS holder's collapse must
    #    not be charged to the new one. This is D12's shape.
    fh = tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False)
    fh.write(hdr)
    for i in range(12):
        fh.write(f"2026-01-01T00:{i:02d}\t{1600 - 20 * i}\t{100 + i}\tv901\trank #1\n")
    for i in range(12):
        fh.write(f"2026-01-01T01:{i:02d}\t{1360 + 5 * i}\t{112 + i}\tv902\trank #1\n")
    fh.close()
    st, v, _, _, alert = assess(fh.name)
    check("holder change resets the window", st.version == "v902" and not st.slot_free,
          f"holder={st.version} net5={_n5(st.net5)}")

    # 6. The alarm must not depend on SHIP_BASELINE — a wrong baseline was the
    #    other live defect, and it must not be able to silence the rule.
    rows = [(1500, 100 + i) for i in range(10)] + \
           [(1500 - 8 * (i + 1), 110 + i) for i in range(5)]
    t = tape(rows)
    _, _, _, _, a_none = assess(t, baseline=None)
    _, _, _, _, a_wrong = assess(t, baseline=99999.0)
    check("a wrong SHIP_BASELINE cannot silence the rule",
          (a_none is not None) and (a_wrong is not None))

    # 7. THE SLOW BOUND (Magnus-approved pair, s26). A steady -4.0/match bleed:
    #    net5 sits at -20 and NEVER reaches -21, so the RULE is silent forever,
    #    and the fast bound (MU0=-10) reads OK. Only the slow bound (MU0=-4)
    #    sees it. This fixture is the whole reason the second bound exists, and
    #    it asserts the fast bound stays OK so it cannot pass for the wrong
    #    reason — if the fast bound ever caught this, the pair would be
    #    redundant rather than complementary.
    rows = [(1580 - 4.0 * i, 900 + i) for i in range(61)]
    t = tape(rows)
    st, _, _, _, alert = assess(t)
    pair = slot_sprt.run_both(st.rows, ALPHA)
    check("slow bleed -4/match: the RULE is silent (net5 never reaches -21)",
          not st.slot_free, f"net5={_n5(st.net5)} over k={st.k}, "
          f"total {rows[-1][0] - rows[0][0]:+.0f} Elo")
    check("...the FAST bound reads OK (so the fixture is not redundant)",
          pair["fast"] == "OK", f"fast={pair['fast']}")
    check("...the SLOW bound CATCHES it", pair["slow"] == "BLEED",
          f"slow={pair['slow']}")
    check("...and an alarm is raised naming the slow bound",
          alert is not None and "slow bound" in alert)

    # ---- THE BLIND BRANCH, s30. Without this the freshness guard is untested
    # wiring in the exact monitor whose documented failure was printing five
    # byte-identical healthy verdicts off a dead tape. Drives BOTH directions:
    # a stale tape must REFUSE, a fresh one must still print.
    import slot_rule as _sr
    _real_tape, _real_log = _sr.TAPE, LOG
    with tempfile.TemporaryDirectory() as _td:
        _d = Path(_td)
        def _body(stamp_fn):
            # assess() needs a RUN, not a single row -- a one-row fixture returns
            # line=None and main() exits before writing anything, which made the
            # FRESH cell pass its emptiness off as a refusal.
            return "".join(
                f"{stamp_fn(i)}\t{1650 + i * 5}\t{730 + i}\tv104\trank #25\n"
                for i in range(8))
        def _run_with(tape_body, when):
            f = _d / f"tape_{when}.tsv"
            f.write_text("ts\trating\tmatches\tver\trank\n" + tape_body)
            _sr.TAPE = f
            globals()["LOG"] = _d / f"out_{when}.log"   # per-run: a shared log
            # made the FRESH cell read the STALE run's line and fail for the
            # wrong reason -- the fixture's bug, not the guard's.
            # main() dispatches on argv, so it must not see --selftest or it
            # re-enters this function. (First cut did, and recursed to the
            # interpreter limit -- kept as a comment because a selftest that
            # calls its own entry point is a trap anyone would walk into.)
            _argv = sys.argv[:]
            sys.argv = [_argv[0]]
            try:
                rc = main()
            finally:
                sys.argv = _argv
            lg = _d / f"out_{when}.log"
            return rc, lg.read_text() if lg.exists() else ""

        # STALE: a row from 1970 is unambiguously past two cadences.
        _rc, _out = _run_with(
            _body(lambda i: f"1970-01-01T00:{i:02d}"), "stale")
        _blind = "BLIND" in _out and "RULE=" not in _out
        check("BLIND: a stale tape REFUSES and prints no verdict", _blind,
              f"log={_out.strip()[:60]!r}")
        if not _blind:
            fails.append("blind-refuses")

        # FRESH: the same code path must still produce a verdict, or the guard
        # is just an off switch. Timestamps are LOCAL CEST in this tape, which is
        # why main() passes assume_local=True -- a fixture written in UTC would
        # read two hours stale and pass this cell for the wrong reason.
        _base = datetime.now()
        _rc, _out = _run_with(
            _body(lambda i: (_base - timedelta(minutes=7 - i)).strftime(
                "%Y-%m-%dT%H:%M")), "fresh")
        _live = "tape_age_min=" in _out and "BLIND" not in _out
        check("...and a FRESH tape still prints a verdict with its age", _live,
              f"log={_out.strip()[:70]!r}")
        if not _live:
            fails.append("fresh-still-prints")
    # ---- 8. THE DENOMINATOR COLUMNS, s33 ------------------------------------
    # Added WITH the columns, because the lesson three lanes learned today is
    # that a selftest can certify the bug: `effective_n`'s independent-fixture
    # cell asserted "eff_n near the row count" -- the CEILING read -- as its PASS
    # condition, and `queue_check` had three marker cells that passed on a
    # missing grep and would have passed with the marker code deleted.
    # So every cell here drives the column to TWO DIFFERENT VALUES, and the last
    # two assert the monitor SURVIVES losing the new data source.
    _ivs = [8.664 * z for z in (-1.7, -1.1, -0.7, -0.4, -0.15, 0.05, 0.25, 0.5,
                                0.8, 1.2, 1.7, -0.9, 0.35, -0.5, 0.65)]
    _slow = lambda n: tape([(1685 - 1.5 * i, 900 + i) for i in range(n)])
    _c = {"intervals": _ivs, "baseline_derived": 1685.0}
    _, _, _, l27, _ = assess(_slow(28), ctx=_c)
    _, _, _, l9, _ = assess(_slow(10), ctx=_c)
    _get = lambda ln, key: ln.split(key)[1].split("\t")[0]
    p27, p9 = float(_get(l27, "p_null=")), float(_get(l9, "p_null="))
    check("p_null: the neutral base rate RISES with k (not a constant column)",
          p27 > p9 + 0.30, f"k=9 {p9:.2f} -> k=27 {p27:.2f}")
    z27 = float(_get(l27, "dd_z="))
    check("dd_z: a -40 drawdown at k=27 reads INSIDE one sd -- i.e. nothing",
          -1.4 < z27 < -0.5, f"dd_z={z27:+.2f}")
    _, _, _, lfast, _ = assess(
        tape([(1685 - 12.0 * i, 900 + i) for i in range(28)]), ctx=_c)
    zf = float(_get(lfast, "dd_z="))
    check("dd_z: a REAL collapse over the same k reads far outside",
          zf < -3 and abs(zf - z27) > 2, f"dd_z={zf:+.2f} vs {z27:+.2f}")
    check("net_act_src: says `derived` when a baseline was derived",
          "net_act_src=derived" in l27)
    _, _, _, lenv, _ = assess(_slow(28), baseline=1700.0,
                              ctx={"intervals": _ivs})
    check("net_act_src: says `env` when it fell back to the hand-set value",
          "net_act_src=env" in lenv, "so a reader can see WHICH number they have")

    # ---- 8b. THE STALE-BASELINE REFUSAL, s50 2026-08-17 ---------------------
    # The live `corpus/ship_watch_state.json` held {"version": "v116",
    # "baseline": 1655.0} against a v160 holder. Both directions, and the ONLY
    # thing that changes between the first two cells is who the baseline
    # belongs to — same tape, same number, same holder.
    _hold = "v900"                       # the tag `tape()` writes on every row
    _, _, _, l_own, _ = assess(_slow(28), baseline=1700.0,
                               ctx={"intervals": _ivs}, baseline_version=_hold)
    check("baseline OWNED by the live holder is USED",
          "net_act_src=env" in l_own and "net_act=UNKNOWN" not in l_own,
          f"baseline_version={_hold} == holder {_hold}")
    _, _, _, l_stale, _ = assess(_slow(28), baseline=1700.0,
                                 ctx={"intervals": _ivs}, baseline_version="v116")
    check("...and a baseline owned by a DEAD holder is REFUSED, not printed",
          "net_act=UNKNOWN" in l_stale and "REFUSED-STALE(v116!=v900)" in l_stale,
          "the column NAMES the disagreement")
    check("...so the two lines are NOT byte-identical (a refusal must be visible)",
          l_own.split("net_act")[1] != l_stale.split("net_act")[1])
    # ⛔ FAIL-OPEN: refusing a DIAGNOSTIC must never touch the ALARM. Same
    # bleeding tape as cell 2, with a stale baseline attached.
    _rows_free = [(1500, 100 + i) for i in range(10)] + \
                 [(1500 - 8 * (i + 1), 110 + i) for i in range(5)]
    _, _, _, l_free, a_free2 = assess(tape(_rows_free), baseline=1655.0,
                                      baseline_version="v116")
    check("...and a REFUSED baseline still lets the RULE free the slot",
          a_free2 is not None and "REFUSED-STALE" in l_free)

    # ⛔ FAIL-OPEN. The columns read a SECOND file; the rule reads only the tape.
    # Losing the second file must degrade the DIAGNOSTIC and leave the ALARM
    # intact. A monitor that dies because its diagnostic could not be computed
    # is strictly worse than one without the diagnostic.
    _, _, _, lbad, _ = assess(_slow(28), ctx={"ladder": "/nonexistent/nope.tsv"})
    check("fail-open: an unreadable ladder degrades the columns to NA",
          "p_null=NA" in lbad and "sd_pm=NA" in lbad and "dd_z=NA" in lbad)
    _, _, _, _, a_free = assess(
        tape([(1600 - 8.0 * i, 900 + i) for i in range(12)]),
        ctx={"ladder": "/nonexistent/nope.tsv"})
    check("...and the RULE STILL FREES THE SLOT with the ladder unreadable",
          a_free is not None and "SLOT RULE HAS FREED" in a_free)

    _sr.TAPE = _real_tape
    globals()["LOG"] = _real_log

    # ---- 9. THE RETIREMENT SWITCH (Magnus 2026-08-16), driven BOTH ways -----
    # Same bleeding tape that freed the slot in cell 2; only the programme
    # field changes. If the off-state cell ever fails while the on-state cell
    # passes, the switch is the defect, not the rule.
    rows = [(1500, 100 + i) for i in range(10)] + \
           [(1500 - 8 * (i + 1), 110 + i) for i in range(5)]
    t = tape(rows)
    slot_rule.PROGRAMME_MD = Path(_prog_off.name)
    st, v, _, line9, alert = assess(t)
    check("RETIRED: the same -40 bleed frees NOTHING and raises NO alert",
          not st.slot_free and alert is None, f"net5={_n5(st.net5)}")
    check("...and the log line says RETIRED, never 'held'",
          "RULE=RETIRED" in line9, f"line={line9[:90]!r}")
    slot_rule.PROGRAMME_MD = Path(_prog_on.name)
    st, v, _, _, alert = assess(t)
    check("...and flipping the field back ON restores the firing",
          st.slot_free and alert is not None, f"net5={_n5(st.net5)}")
    slot_rule.PROGRAMME_MD = _real_programme

    print(f"\n{'SELFTEST PASSED' if not fails else 'SELFTEST FAILED: ' + ', '.join(fails)}")
    return 1 if fails else 0


STALE_H = 20 / 60.0      # two 10-minute cadences


CONVENTION_MARK = ("# CLOCK CONVENTION CHANGED HERE: rows ABOVE this line stamp "
                   "LOCAL time with no zone marker; rows BELOW stamp UTC with an "
                   "explicit Z. Written once, by tools/monitors/ship_watch.py, "
                   "s30 2026-08-11.")


def _mark_convention() -> None:
    """Write the convention marker once, ever. A log that switches clocks
    mid-file with nothing recording when is a trap for whoever parses it later
    -- and the switch is invisible in the data because both conventions produce
    a plausible ISO timestamp."""
    try:
        if LOG.exists() and CONVENTION_MARK in LOG.read_text():
            return
        with open(LOG, "a") as fh:
            fh.write(CONVENTION_MARK + "\n")
    except Exception:
        pass          # never let bookkeeping break the stop-loss


def main() -> int:
    if "--selftest" in sys.argv:
        return selftest()

    state = {}
    if STATE.exists():
        try:
            state = json.loads(STATE.read_text())
        except Exception:
            state = {}
    version = os.environ.get("SHIP_VERSION") or state.get("version")
    baseline = os.environ.get("SHIP_BASELINE") or state.get("baseline")
    baseline = float(baseline) if baseline is not None else None
    if version:
        STATE.write_text(json.dumps({"version": version, "baseline": baseline}))

    # ⛔ FRESHNESS FIRST, s30 2026-08-11. THIS MONITOR IS THE ONE CLAUDE.md's
    # "a monitor that reads a file must report that file's FRESHNESS" rule was
    # WRITTEN ABOUT, and it still asserted nothing until now.
    #
    # MEASURED (side lane, `elo_history.tsv`, 1,243 rows over 08-06..08-11):
    # median inter-row gap 5.0 min against this monitor's 10-min cadence, but
    # TEN stalls exceed two cadences, totalling 338 of 6,693 min = 5.1% of the
    # tape's life, longest 50 min. On the documented 08-10 outage this monitor
    # printed FIVE CONSECUTIVE verdict lines, byte-identical but for the
    # timestamp, off a dead tape -- and when it recovered, k jumped 63 -> 68 and
    # rating 1599 -> 1631. **Five matches and +32 Elo were invisible to the ship
    # monitor for fifty minutes while it printed `armed=True RULE=held` and
    # reported drawdown=-17.0 for a state that had reached +0.0.**
    #
    # ⭐ AND THE CONTROL IS WHY NO AMOUNT OF ATTENTION FIXES IT: the healthy
    # stretch immediately after is ALSO byte-identical across two cadences
    # (08:02:09 and 08:12:09, k=68 rating=1631) -- because that is simply what a
    # quiet ten minutes looks like. **"The same line twice" carries no
    # information in either direction.** A reader cannot distinguish "no match
    # completed" from "the tape is dead".
    #
    # So the monitor REFUSES rather than guessing, per the rule's own wording:
    # "emit the age of the newest row, or refuse to print a verdict past ~2
    # cadences." Threshold is 2 cadences = 20 min = 0.34 h.
    # assume_local=True: elo_history stamps LOCAL CEST with NO zone marker, so
    # read naively as UTC it reports rows from the FUTURE, which makes stale data
    # look live. That hazard is exactly what freshness.py's CLOCK ERROR branch is
    # for, and getting the flag wrong here would invert the check.
    ok, age_h, fmsg = assert_fresh(slot_rule.TAPE, max_age_h=STALE_H,
                                   assume_local=True)
    if not ok:
        print(f"SHIP_WATCH BLIND -- refusing to print a verdict. {fmsg}",
              file=sys.stderr)
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG, "a") as fh:
            fh.write(f"{datetime.now(timezone.utc):%Y-%m-%dT%H:%M:%S}Z\t"
                     f"BLIND\t{fmsg}\n")
        return 0

    # ---- DENOMINATOR CONTEXT, s33 -------------------------------------------
    # `ladder_games.tsv` supplies the per-match sd (for dd_z / resolvable_k /
    # p_null) and the DERIVED activation baseline. It is read best-effort: a
    # failure here must degrade the DIAGNOSTIC columns to `NA` and must never
    # touch the RULE, which reads the elo tape alone. Its age is printed.
    ctx = {"ladder": LADDER}
    try:
        ctx["intervals"] = slot_denoms.intervals_from_ladder(LADDER)
        _lok, _lage, _ = assert_fresh(LADDER, max_age_h=24.0)
        ctx["ladder_age_min"] = _lage * 60 if _lage is not None else None
    except Exception:
        ctx["intervals"] = []

    # version is REPORTING-ONLY; the rule follows whoever the tape says is live.
    # It IS passed as `baseline_version` though — not to select a holder, but so
    # assess() can refuse the hand-set baseline when that baseline belongs to a
    # holder who is no longer live (s50; see the REFUSED-STALE block).
    st, verdict, events, line, alert = assess(slot_rule.TAPE, None, baseline, ctx,
                                              baseline_version=version)
    if line is None:
        print("no holder run on the tape yet", file=sys.stderr)
        return 0
    # The age travels WITH the verdict, so a healthy line and a nearly-stale one
    # are no longer byte-identical.
    line = f"{line}\ttape_age_min={age_h*60:.1f}"

    LOG.parent.mkdir(parents=True, exist_ok=True)
    _mark_convention()
    with open(LOG, "a") as fh:
        fh.write(line + "\n")
    print(line)

    if alert is not None:
        ALERT.write_text(alert)
        print("*** SHIP_ALERT WRITTEN ***", file=sys.stderr)
    elif ALERT.exists():
        ALERT.unlink()      # recovered; do not leave a stale alarm standing
    return 0


if __name__ == "__main__":
    sys.exit(main())
