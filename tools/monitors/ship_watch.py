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
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
LOG = ROOT / "corpus" / "ship_watch.log"
ALERT = ROOT / "corpus" / "SHIP_ALERT"
STATE = ROOT / "corpus" / "ship_watch_state.json"

sys.path.insert(0, str(ROOT / "tools"))
import slot_rule                              # noqa: E402  the RULE
import slot_sprt                              # noqa: E402  the ADVISORY
from slot_sprt import bound, run_sprt, MU0, ALPHA   # noqa: E402

BOUND = bound()


def _n5(v) -> str:
    """net5 is None until the holder's window fills. Formatting it without a
    guard crashed --selftest under a mutated WINDOW — a diagnostic that dies on
    a degenerate input is a diagnostic that stops reporting exactly when
    something is wrong."""
    return "n/a" if v is None else f"{v:+.1f}"


def assess(tape, version=None, baseline=None):
    """Return (state, sprt_verdict, sprt_events, line, alert_text|None).

    The rule decides the alarm. The SPRT is reported alongside it and never
    suppresses it — an advisory that can veto a rule is not an advisory.
    """
    st = slot_rule.evaluate(tape, version)
    if st is None or st.k <= 0:
        return None, None, None, None, None

    verdict, events, _, _ = run_sprt(st.rows, MU0, ALPHA)

    n5 = _n5(st.net5)
    net_act = "" if baseline is None else f"\tnet_act={st.rating - baseline:+.1f}"
    ruling = ("SLOT FREE" if st.slot_free else
              "held" if st.armed else "unarmed")
    # LEVEL, not just slope. net5 is a five-match SLOPE and it RELAXES as a bad
    # result ages out of the window: on 2026-08-09 v102 fell 6 Elo while net5
    # IMPROVED 7, and "recovering" was reported off it. Worse, a steady bleed
    # slower than -4.2/match holds net5 above -21 forever — measured, a -4.0
    # bleed loses 240 Elo over 60 matches and trips neither this rule nor the
    # SPRT. The drawdown column cannot fix that (the alarm still belongs to the
    # rule) but it makes the blind spot legible instead of invisible.
    peak = max(r for _, r, _ in st.rows)
    line = (f"{datetime.now().isoformat(timespec='seconds')}\t{st.version}\t"
            f"k={st.k}\trating={st.rating:.0f}\tnet5={n5}\t"
            f"peak={peak:.0f}\tdrawdown={st.rating - peak:+.1f}\t"
            f"armed={st.armed}\tRULE={ruling}\tsprt={verdict}{net_act}")

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
    elif verdict == "BLEED":
        alert = (
            line + "\n\n"
            f"SPRT ADVISORY accepted BLEED for {st.version} (llr <= -{BOUND:.2f}).\n"
            f"The -21 rolling-5 rule has NOT freed the slot (net5 {n5}); the rule\n"
            "is the rule. This is the statable-error-rate read, raised because a\n"
            "sequential test accepting bleed is worth a human look.\n")
    return st, verdict, events, line, alert


def selftest() -> int:
    """Corrupt the input; require the alarm. Every case here is a bug this file
    or its ancestor actually had."""
    hdr = "ts\trating\tmatches\tversion\trank\n"

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

    print(f"\n{'SELFTEST PASSED' if not fails else 'SELFTEST FAILED: ' + ', '.join(fails)}")
    return 1 if fails else 0


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

    # version is REPORTING-ONLY; the rule follows whoever the tape says is live.
    st, verdict, events, line, alert = assess(slot_rule.TAPE, None, baseline)
    if line is None:
        print("no holder run on the tape yet", file=sys.stderr)
        return 0

    LOG.parent.mkdir(parents=True, exist_ok=True)
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
