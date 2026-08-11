#!/usr/bin/env python3
"""Audit trigger — is the project producing analysis instead of decisions?

WHY THIS EXISTS (2026-08-08 s19). A third session, doing nothing but auditing
our process, found that our standard n=120 battery had **19% power** against a
true +5pp plank. Neither arm found it in fifteen hours of intensive measuring,
because both arms were *inside* the loop: one had just rewritten the ship gate,
the other had built the probes. Nobody audits their own instrument.

The signature was visible in the repo for hours before anyone looked. All four
signals below are computable from files we already keep. When analysis output
rises while decisions fall, spawn a short-lived audit session whose ONLY job is
to ask whether the instruments can support the decisions being made — then let
it stop. The auditor's value came from having no stake; a permanent third arm
would eventually acquire one.

Run it on boot (it is in .claude/commands/builder.md step 4). Costs ~1 second.

    .venv/bin/python tools/audit_trigger.py

Thresholds are calibrated on the 2026-08-08 deadlock, which is the only
confirmed instance — treat them as a smoke alarm, not a p-value. FIRE when 2+
of 4 signals trip.
"""
import csv
import subprocess
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

# --selftest overrides. Every check below reads a file or `git log`; the only
# way to prove a check CAN fire is to feed it something that must trip it. See
# the SELFTEST block at the bottom for why this is not optional.
_OVERRIDE: dict = {}

ROOT = Path(__file__).resolve().parent.parent
WINDOW_ROWS = 50          # tape rows to look back over (25 biases toward
                          # wrap time, when analysis rows legitimately cluster)
CHURN_HOURS = 24


def note_verdict_ratio():
    """Analysis rows vs decision rows ON THE BUILDER TAPE ONLY.

    Tonight's deadlock read 14 notes/caveats against 6 verdicts in the last 25
    rows — the project was documenting faster than it was deciding.

    SCOPE, ADDED s25 AND THE REASON THE ROW BELOW EXISTS. `results.tsv` is
    written by the BUILDER arm alone. The research arm and the side lane publish
    analysis into `docs/research/*.md` and `docs/coordination.md` and never touch
    this file. So this row has been scoring "is the PROJECT producing analysis
    instead of decisions" while seeing roughly one lane of three — it reported
    `ok` all day about lanes it cannot see. It is deliberately left CALIBRATED AS
    IS (its threshold was tuned on the 2026-08-08 deadlock and changing the
    numerator would silently invalidate that), and the blindness is closed by
    `cross_lane_analysis` instead, which is a new row with its own calibration.
    """
    rows = _OVERRIDE.get("tape") or list(csv.reader((ROOT / "results.tsv").read_text().splitlines(), delimiter="\t"))[1:]
    tail = [r for r in rows if len(r) > 5][-WINDOW_ROWS:]
    c = Counter(r[5] for r in tail)
    analysis = c["note"] + c["caveat"] + c["info"]
    # baseline and ship ARE decisions — a baseline row records an activation.
    # Excluding them inflated this ratio ~2.4x (instrument-audit-2026-08-08-late
    # :203-210; fix adopted 2026-08-09 with the process review).
    decisions = (c["verdict"] + c["keep"] + c["discard"] + c["refuted"] + c["gate"]
                 + c["baseline"] + c["ship"])
    ratio = analysis / max(decisions, 1)
    return ratio, f"{analysis} analysis rows / {decisions} decision rows (last {len(tail)})"


# Prose surfaces this repo's METHOD REQUIRES. Writing them is doing the work,
# not avoiding it, so they must not count as drift. See doc_code_churn().
MANDATED_PROSE = ("docs/coordination.md", "HANDOVER.md", "docs/prereg/")


def doc_code_churn(hours=None):
    """Lines changed in prose vs in code, over the last day of commits.

    0.14 on the productive day; 1.88 on the deadlocked one.

    ⛔ RE-SPECIFIED s30, 2026-08-11, AFTER AN OUTSIDE AUDIT SHOWED THE ROW WAS
    RETURNING NOISE. Two defects, both measured, neither hypothetical:

    1. **IT HOVERED ON ITS OWN THRESHOLD, so the verdict was set by WHEN you ran
       it.** Recomputed at six window offsets on one unchanged tree:
           20h 1.0043 TRIP · 22h 0.9536 ok · 24h 0.9333 ok
           26h 1.0279 TRIP · 28h 0.9939 ok · 30h 1.0691 TRIP
       Three of six trip, with no trend. Two lanes booting four minutes apart
       got opposite verdicts off the same tree (1.002820 TRIP at 06:05Z,
       0.998839 ok at 06:09Z) purely from prose commits ageing out.
       **AND `{val:.2f}` PRINTS `1.00` ON BOTH SIDES OF A 1.0 THRESHOLD**, so
       the two readings were byte-identical except for the TRIP/ok tag.
    2. **~43% of the numerator was artefacts the method MANDATES** —
       `coordination.md` 4,517 lines (26.8%), `HANDOVER.md` 1,109 (6.6%), three
       preregs 1,692 (10.0%) in one 24h window. **A leg run CORRECTLY raised
       this signal.** The IN-FLIGHT registry, the handover and a pre-registration
       are the work; counting them as drift inverts the row's meaning.

    THE FIX, both halves:
      * MANDATED_PROSE is excluded from the numerator.
      * The row TRIPS ONLY IF IT TRIPS AT 20h, 24h AND 28h. A signal that cannot
        survive a +/-4h window shift is a phase of the commit lumpiness, not a
        property of the work. The reported value is the 24h one; the detail line
        prints all three so a near-miss is visible instead of rounded away.
    """
    if hours is not None:                      # single-window mode, used by the
        return _churn_at(hours)                # stability check below
        # (and by the selftest, which needs one deterministic window)
    vals = {h: _churn_at(h)[0] for h in (20, 24, 28)}
    v24, detail = _churn_at(24)
    stable = all(v >= 1.0 for v in vals.values())
    # Report BELOW threshold unless all three windows agree, so `main`'s
    # `val >= thresh` comparison implements the stability rule without needing
    # to know about it.
    shown = v24 if stable else min(v24, 0.999)
    return shown, (f"{detail}   [20h {vals[20]:.3f} · 24h {vals[24]:.3f} · "
                   f"28h {vals[28]:.3f}; trips only if ALL THREE >= 1.0]")


def _churn_at(hours):
    out = _OVERRIDE.get("numstat")
    if out is None:
        out = subprocess.run(
            ["git", "log", f"--since={hours}.hours", "--numstat", "--pretty=format:"],
            capture_output=True, text=True, cwd=ROOT).stdout
    doc = code = 0
    for line in out.splitlines():
        p = line.split("\t")
        if len(p) < 3:
            continue
        try:
            n = int(p[0]) + int(p[1])
        except ValueError:
            continue          # binary file
        # Cap per-file churn. Copying a 7,000-line bot dir into bots/_vNN is one
        # `cp`, not seven thousand lines of thought, and uncapped it drowns the
        # signal entirely (measured: 364k "code lines" in a day that shipped
        # three one-line flag changes).
        n = min(n, 500)
        if p[2].endswith(".md"):
            if p[2].startswith(MANDATED_PROSE):
                continue      # the method requires these; they are not drift
            doc += n
        elif p[2].startswith(("bots/", "tools/")):
            code += n
    ratio = doc / max(code, 1)
    return ratio, f"{doc} prose lines / {code} code lines (last {hours}h, mandated prose excluded)"


def ship_cadence():
    """Activations per hour of active work, from elo_history's own timestamps.

    FIXED 2026-08-08 s20, after the instrument audit caught this check firing on
    itself. It used to prose-match results.tsv: `r[5] == "baseline" and "SHIP"
    in r[6][:60]`. That predicate matched **6 rows in the project's entire
    history** — v82, v84 and v86 all went live and matched none of them, because
    whether a ship gets a "SHIP —" row or only a "... FINAL:" row depends on how
    the writing session happened to word it. Worse, it had no time window at
    all: `ships[-12:]` slices an all-time list, so `recent` was pinned at
    min(12, 6) = 6 forever and the check tripped unconditionally past ~12 active
    hours. The 2/4 FIRE that summoned the audit session was substantially this.

    Now it counts active_bot TRANSITIONS in elo_history.tsv, which the elo_logger
    writes with a real timestamp every 5 minutes. An activation is what we
    actually mean by "a decision landed"; it is recorded by a monitor rather than
    by prose, so it cannot drift with anyone's phrasing. 45 transitions are
    visible where the old predicate saw 6.

    STANDING CAUTION: every "analysis is outpacing decisions" reading taken
    before this fix is suspect, including the ones both arms acted on tonight.
    """
    # `now` is overridable for the SAME reason `elo` and `hours` are, and its
    # absence was a live defect for an unknown length of time (found s28,
    # 2026-08-10). The sibling test below pinned `hours` and the row CONTENTS
    # but dated those rows `2026-08-09T10:00` — a literal. Once the wall clock
    # passed 2026-08-10T10:00 every fixture row fell outside `now - 24h`, the
    # loop counted ZERO transitions, and the test failed reporting `0.0` as a
    # cadence stall. It was then recorded in HANDOVER as proof that the CHECK
    # is miscalibrated and "would summon an audit on a normal working day."
    # IT IS NOT. With the fixture dated relative to the same clock the cutoff
    # uses, the check returns 0.60/hr on the normal day (ok, threshold 0.5) and
    # 0.10/hr on the stalled one (trips). THE FIXTURE ROTTED, NOT THE CHECK —
    # which is the exact family the sibling docstring says it was rewritten to
    # escape: it de-live-ified `hours` and left the timestamps live, so the
    # test's truth still changed with the wall clock, just a day later.
    now = _OVERRIDE.get("now") or datetime.now()
    cutoff = now - timedelta(hours=CHURN_HOURS)
    rows = _OVERRIDE.get("elo") or list(csv.reader((ROOT / "elo_history.tsv").read_text().splitlines(), delimiter="\t"))[1:]

    ships, prev = 0, None
    for r in rows:
        if len(r) < 4 or not r[0]:
            continue
        try:
            when = datetime.strptime(r[0][:16], "%Y-%m-%dT%H:%M")
        except ValueError:
            continue
        if prev is not None and r[3] != prev and when >= cutoff:
            ships += 1
        prev = r[3]

    # `hours` is overridable for the same reason `elo` is: without it a test of
    # this check is still half-live, and the assertion silently becomes "did the
    # team commit much today". That is precisely how the sibling test rotted —
    # it asserted rate > 0.5 against the LIVE tape, passed at 11 activations/20h
    # = 0.55, and failed 16 minutes later at 10/20 = 0.50 when one aged out of
    # the window. The instrument was correct at both readings (it trips at
    # < 0.5, so 0.50 is fine); only the test was wrong.
    if _OVERRIDE.get("hours"):
        active_hours = _OVERRIDE["hours"]
    else:
        out = subprocess.run(
            ["git", "log", f"--since={CHURN_HOURS}.hours", "--pretty=format:%ad", "--date=format:%H"],
            capture_output=True, text=True, cwd=ROOT).stdout.split()
        active_hours = max(len(set(out)), 1)
    rate = ships / active_hours
    return rate, f"{ships} activations in the last {CHURN_HOURS}h over ~{active_hours} active hours"


def cross_lane_analysis():
    """Analysis DOCUMENTS produced across all three lanes vs decisions recorded.

    ADDED s25, after the research arm pointed out that `note:verdict ratio`
    reads a tape its lane never writes to. On 2026-08-09 the research arm and
    side lane published a dozen-plus dated analyses into docs/research/ while
    `note:verdict` reported `ok` throughout — not wrongly, but blindly: it was
    never looking there.

    Counts .md files ADDED under docs/ in the window (analysis output, any lane)
    against decision rows on the builder tape (verdicts, keeps, discards,
    refutations, gates, baselines, ships — the same decision set the row above
    uses, because a decision is still only recorded in one place).

    Threshold 4.0 is deliberately loose and is NOT calibrated on a confirmed
    incident — it is a smoke alarm for "many documents, no decisions", and it is
    labelled as uncalibrated so nobody quotes it as a p-value.

    ⛔ FIXED s30, 2026-08-11. THIS ROW WAS SUPPRESSING ITSELF, AND IT WAS THE
    ONLY ONE OF THE FIVE THAT GENUINELY WAS. Two lanes found it independently
    (the side lane's s29 sweep item, and an outside audit session spawned on the
    boot FIRE) and both landed on the same cause:

      **THE NUMERATOR WAS WINDOWED TO 24h OFF GIT AND THE DENOMINATOR WAS "THE
      LAST 50 TAPE ROWS", WHICH CARRY NO CLOCK AT ALL.** `results.tsv` has no
      timestamp column, so it could not be windowed in place, and the two sides
      were therefore counting different populations.

    Measured on 2026-08-11: `results.tsv` newest commit `4ad19ab`
    2026-08-09T18:38:18Z (35.6h old); 19 of 21 dateable decision rows ALL >=35.5h
    old; **zero rows added in 24h.** As shipped the row read 47/21 = 2.29 → `ok`.
    Same-window it reads **47/0 = 47.00 against a threshold of 4.0 → TRIP.**
    **On a day with 47 new analysis documents and ZERO recorded decisions, the
    row built to catch exactly that condition printed `ok`.** Shipped: 1/5,
    "audit not indicated". Consistently windowed: 2/5 = FIRE.

    **AND `freshness.py` WOULD NOT HAVE FIXED IT.** That helper makes an
    instrument REFUSE when its tape is stale; it does not make a ratio of two
    different populations mean anything when the tape is fresh. This needed a
    matched denominator, not a staleness gate — recorded because the standing
    queue item called this "one helper, four bugs" and it is not.

    THE FIX: count decision rows ADDED to `results.tsv` inside the SAME git
    window as the documents, read off `git log -p`. Same clock, same source,
    same population — `+` lines added, `+++` header excluded.
    """
    out = _OVERRIDE.get("namestat")
    if out is None:
        out = subprocess.run(
            ["git", "log", f"--since={CHURN_HOURS}.hours", "--diff-filter=A",
             "--name-only", "--pretty=format:"],
            capture_output=True, text=True, cwd=ROOT).stdout
    docs = sum(1 for ln in out.splitlines()
               if ln.strip().startswith("docs/") and ln.strip().endswith(".md"))
    decisions = _decisions_in_window()
    ratio = docs / max(decisions, 1)
    return ratio, (f"{docs} new analysis docs / {decisions} decision rows ADDED "
                   f"(BOTH sides last {CHURN_HOURS}h, same git window)")


DECISION_KINDS = ("verdict", "keep", "discard", "refuted", "gate", "baseline", "ship")


def _decisions_in_window(hours=None):
    """Decision rows ADDED to results.tsv inside the git window.

    Matched to the numerator's population by construction: same `--since`, same
    git log, same definition of "new". A row that already existed is not a
    decision made in the window, and that is the whole bug this replaces.
    """
    hours = CHURN_HOURS if hours is None else hours
    patch = _OVERRIDE.get("tape_patch")
    if patch is None:
        patch = subprocess.run(
            ["git", "log", f"--since={hours}.hours", "-p", "--unified=0",
             "--pretty=format:", "--", "results.tsv"],
            capture_output=True, text=True, cwd=ROOT).stdout
    n = 0
    for ln in patch.splitlines():
        if not ln.startswith("+") or ln.startswith("+++"):
            continue
        f = ln[1:].split("\t")
        if len(f) > 5 and f[5] in DECISION_KINDS:
            n += 1
    return n


def stuck_planks():
    """Planks parked in KEEP-dev — the state that should not exist.

    docs/ship-gate.md: a plank is shipping, being fixed, or refuted. Anything
    that survives two windows in KEEP-dev is refuted by neglect.
    """
    rows = _OVERRIDE.get("tape") or list(csv.reader((ROOT / "results.tsv").read_text().splitlines(), delimiter="\t"))[1:]
    n = sum(1 for r in rows[-60:] if len(r) > 6 and "KEEP-dev" in r[6])
    return n, f"{n} KEEP-dev mentions in the last 60 tape rows"


CHECKS = [
    ("note:verdict ratio", note_verdict_ratio, 1.5, "analysis is outpacing decisions"),
    ("doc:code churn",     doc_code_churn,     1.0, "writing about the work faster than doing it"),
    ("ship cadence",       ship_cadence,       None, "decisions per hour has fallen"),
    ("stuck planks",       stuck_planks,       3,   "planks parked instead of shipped or refuted"),
    ("cross-lane analysis", cross_lane_analysis, 4.0, "analysis docs piling up across all lanes"),
]


# Synthetic inputs that MUST trip each row. Deliberately extreme: the question
# is "can this alarm fire at all", not "does it fire at the right threshold".
_TRIPPERS = {
    "note:verdict ratio":  {"tape": [["", "", "", "", "", "note", "x"]] * 40},
    "doc:code churn":      {"numstat": "900\t0\tdocs/a.md\n1\t0\ttools/b.py\n"},
    "ship cadence":        {"elo": [["2026-08-09T10:00", "1", "1", "vX"]] * 5},
    "stuck planks":        {"tape": [["", "", "", "", "", "note", "KEEP-dev"]] * 9},
    # cross-lane now reads ADDED decision rows out of a git patch, not the tape
    # tail, so its tripper feeds a patch with exactly one added decision row.
    # The `+++` header line is included DELIBERATELY: it starts with `+` and a
    # parser that forgets to skip it would count it, so this fixture doubles as
    # the guard for that off-by-one.
    "cross-lane analysis": {"namestat": "docs/a.md\ndocs/b.md\ndocs/c.md\ndocs/d.md\n"
                                        "docs/e.md\n",
                            "tape_patch": "+++ b/results.tsv\n"
                                          "+a\tb\tc\td\te\tverdict\tx\n"},
}


def selftest() -> int:
    """Prove every row CAN fire. A row that cannot is not a check.

    THE FIFTH INSTANCE OF ONE FAMILY IN A DAY, which is why this exists rather
    than a note asking someone to be careful: a treatment census that returned a
    confident 0/24 because it never located a core; a gunner ray bonus that would
    have scored zero in every game forever because the predicate refuses empty
    tiles; a `teamXRating` live join that looked right for a day; a
    reconciliation CHECK 2 whose teeth were never proven while CHECK 1's were;
    and a `--selftest` mode rejected by its own argument validator so the alarm
    could not fire. Every one of them printed something healthy.

    ⇒ AN INSTRUMENT THAT HAS NEVER BEEN OBSERVED TO FAIL IS NOT EVIDENCE, IT IS
      A CLAIM. Corrupt the input; require the alarm. If a row cannot be made to
      fire it should be deleted rather than left printing `ok`.
    """
    bad = []
    print("AUDIT TRIGGER SELFTEST — can each row fire at all?\n")
    for name, fn, thresh, _why in CHECKS:
        _OVERRIDE.clear()
        _OVERRIDE.update(_TRIPPERS.get(name, {}))
        try:
            val, detail = fn()
        except Exception as e:
            print(f"  [ERROR] {name}: {e}")
            bad.append(name)
            continue
        trip = val < 0.5 if name == "ship cadence" else val >= thresh
        print(f"  [{'PASS' if trip else 'FAIL'}] {name:<20} -> {val:.2f}   ({detail})")
        if not trip:
            bad.append(name)
    _OVERRIDE.clear()
    print()
    if bad:
        print(f"SELFTEST FAILED — {len(bad)} row(s) could not be made to fire: "
              f"{', '.join(bad)}.", file=sys.stderr)
        print("A row that cannot fire is not a check. Fix it or delete it.",
              file=sys.stderr)
        return 1
    print(f"SELFTEST PASS — all {len(CHECKS)} rows fire on a corrupted input.")
    return 0


def main():
    if "--selftest" in sys.argv[1:]:
        return selftest()
    tripped = []
    print("AUDIT TRIGGER — is analysis outpacing decisions?\n")
    for name, fn, thresh, why in CHECKS:
        try:
            val, detail = fn()
        except Exception as e:                     # never let the alarm break a boot
            print(f"  [skip] {name}: {e}")
            continue
        if name == "ship cadence":
            trip = val < 0.5
            shown = f"{val:.2f}/hr"
        else:
            trip = val >= thresh
            shown = f"{val:.2f}" if isinstance(val, float) else str(val)
        mark = "TRIP" if trip else "  ok"
        print(f"  [{mark}] {name:<20} {shown:<10} {detail}")
        if trip:
            tripped.append((name, why))

    print()
    if len(tripped) >= 2:
        print(f"*** FIRE: {len(tripped)}/{len(CHECKS)} signals tripped ***")
        for n, why in tripped:
            print(f"      - {n}: {why}")
        print()
        print("  Spawn a SHORT-LIVED AUDIT SESSION. Its only job: ask whether the")
        print("  instruments can support the decisions being made. Give it no stake")
        print("  in the current queue and let it stop when it reports.")
        print("  Prior art: docs/workflow-analysis/ (2026-08-08, found 19% power).")
        return 1
    print(f"OK — {len(tripped)}/{len(CHECKS)} tripped; audit not indicated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
