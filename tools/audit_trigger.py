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
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ---- `--help` CONTRACT (enforced by tests/test_instruments.py) --------------
# Side-effect-free, prints this module's docstring, exits 0.
#
# ⛔ WHY. Probing an unknown tool with `--help` is the first thing anyone does.
# Before 2026-08-15, 40 of 86 tools here had no argparse, so `--help` was just an
# unrecognised argument and THE TOOL RAN FOR REAL -- printing VERDICT-SHAPED text
# that reads as a finding:
#     tools/freshness.py --help  ->  "BLIND: --help has no parseable timestamp"
#     tools/leg_read.py  --help  ->  "LEG: no completed games"
# Both are this repo's own verdict vocabulary. A reader asking a harmless
# question got an authoritative-looking sentence about nothing.
#
# ⛔ GATED ON `__main__`: several of these modules are IMPORTED by other tools
# (freshness by now.py). Ungated, this would fire during that import and make the
# PARENT exit 0 mid-run while printing the CHILD's docstring.
# ⛔ SELF-CONTAINED `import sys`: a first attempt used the file's own import, and
# broke on `import sys as _sys` (NameError) and on files whose imports come in
# two blocks. The guard must not depend on what the host file happens to import.
if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__ + "  (no module docstring)"))
        raise SystemExit(0)

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
    # ⭐ RE-VOCABULARIED s57 (M1). The s25 note above froze this cell's decision
    # set "so the 2026-08-08 calibration stays valid" — the s55 audit measured
    # that frozen set recognizing 6 of the last 50 rows (12%) while auto_gate
    # wrote 28 `cancellation` rows it could not see. A counter blind to 88% of
    # its tape is not calibrated, it is decorative; the shared vocabulary wins.
    rows = _OVERRIDE.get("tape") or list(csv.reader((ROOT / "results.tsv").read_text().splitlines(), delimiter="\t"))[1:]
    tail = [r for r in rows if len(r) > 5][-WINDOW_ROWS:]
    c = Counter(_row_kind(r) for r in tail)
    analysis = sum(c[k] for k in ANALYSIS_KINDS)
    decisions = sum(c[k] for k in DECISION_KINDS)
    fork = c[None]                     # schema-fork rows: reported, never guessed
    ratio = analysis / max(decisions, 1)
    detail = f"{analysis} analysis rows / {decisions} decision rows (last {len(tail)})"
    if fork:
        detail += f" [+{fork} SCHEMA-FORK row(s) unclassifiable — see _row_kind]"
    return ratio, detail


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
    # ⛔ NAIVE **UTC**, NOT NAIVE LOCAL. `elo_history.tsv` was migrated to
    # UTC-with-`Z` on 2026-08-15; this comparison is naive on both sides, so if
    # `now` stayed `datetime.now()` (LOCAL CEST) the 24h churn window would sit
    # TWO HOURS off the rows it filters -- silently including or dropping
    # activations at the edge. Both sides are UTC now. The `_OVERRIDE` seam is
    # preserved (tests pass a naive datetime and still control the clock).
    # ⭐ M5 REPAIRS (s55 audit, fixed s57 on Magnus's direct order), three:
    #
    # (1) POLICY HOLD IS NOT DRIFT. Under PROGRAMME.md `STEALTH_UNTIL_DROP: yes`
    #     a zero-activation day is the DIRECTIVE being followed, and the
    #     account-wide numerator (teammates ship too) has no our-subject left
    #     to score. The cell reports HELD and refuses a verdict rather than
    #     tripping on obedience. Overridable ("stealth") so the selftest can
    #     force both states.
    # (2) A ROLLBACK IS NOT A SHIP. The old count scored every active_bot
    #     TRANSITION, so one fire→rollback window read as 2+ "decisions".
    #     Now only a transition to a version NEVER SEEN BEFORE in the tape
    #     counts — a restore returns to a seen version and scores zero.
    # (3) SUBJECTS DISCLOSED, BLINDNESS DISCLOSED. The numerator is ACCOUNT-
    #     WIDE (elo_history cannot attribute an activation to a lane or a
    #     teammate) over OUR-git active hours, and a 5-minute poller cannot
    #     see a sub-poll activation window at all (measured: v180's entire
    #     rated exposure left 0 rows in 288). The detail line now says so —
    #     numbers carry subjects.
    stealth = _OVERRIDE.get("stealth")
    if stealth is None:
        try:
            stealth = "STEALTH_UNTIL_DROP: yes" in (ROOT / "PROGRAMME.md").read_text()
        except OSError:
            stealth = False
    if stealth:
        return None, ("HELD BY POLICY — PROGRAMME.md STEALTH_UNTIL_DROP: yes; "
                      "zero activations is the directive, not drift (activation "
                      "cadence not scored)")

    now = _OVERRIDE.get("now") or datetime.now(timezone.utc).replace(tzinfo=None)
    cutoff = now - timedelta(hours=CHURN_HOURS)
    rows = _OVERRIDE.get("elo") or list(csv.reader((ROOT / "elo_history.tsv").read_text().splitlines(), delimiter="\t"))[1:]

    ships, prev, seen = 0, None, set()
    for r in rows:
        if len(r) < 4 or not r[0]:
            continue
        try:
            when = datetime.strptime(r[0][:16], "%Y-%m-%dT%H:%M")
        except ValueError:
            continue
        if (prev is not None and r[3] != prev and r[3] not in seen
                and when >= cutoff):
            ships += 1
        seen.add(r[3])
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
    return rate, (f"{ships} first-time activations (ACCOUNT-WIDE incl. teammates; "
                  f"5-min poller misses sub-poll windows) in the last "
                  f"{CHURN_HOURS}h over ~{active_hours} our-git active hours")


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
    # Audit M6 (2026-08-13): MANDATED_PROSE was honoured by doc_code_churn and
    # never by this sibling — 4 of the 10 files behind that day's FIRE were
    # preregs. Retros are mandated too (each lane's wrap REQUIRES one), so they
    # are excluded here for the same reason preregs are.
    # ⭐ M4 (s55 audit): a READOUT document — a build report, a decode, a
    # powered/transfer read — is a decision being PUBLISHED, and counting it as
    # analysis made the "no decisions" alarm louder every time a decision
    # landed (25 of the 31 docs behind the s55 FIRE carried disposition
    # language; 11 were BUILD-REPORT-*). Excluded from the numerator; the
    # decision itself is counted on the tape side when its row lands.
    def _is_readout(name):
        n = Path(name).name
        return n.startswith(("BUILD-REPORT-", "DECODE-")) or "-READ-" in n

    docs = sum(1 for ln in out.splitlines()
               if ln.strip().startswith("docs/") and ln.strip().endswith(".md")
               and not any(ln.strip().startswith(m) for m in MANDATED_PROSE)
               and "retro" not in Path(ln.strip()).name.lower()
               and not _is_readout(ln.strip()))
    decisions = _decisions_in_window()
    ratio = docs / max(decisions, 1)
    return ratio, (f"{docs} new analysis docs / {decisions} decision rows ADDED "
                   f"(BOTH sides last {CHURN_HOURS}h, same git window)")


# ⭐ M1 REPAIR (s55 audit, fixed s57 2026-08-22 on Magnus's direct order): the
# tape's disposition vocabulary, reconciled with what the lanes and auto_gate
# ACTUALLY write. Before this, `cancellation` — written by tools/auto_gate.py
# as the tape's second-most-common row type (28 of the last 50 rows) — was
# invisible to every counter, along with no-verdict/hold/negative/correction/
# inert/frozen. The counters recognized 6 of the last 50 rows (12%).
#
# THE JUDGMENT CALLS, typed by the builder so the next reader argues with a
# decision instead of an accident:
#   * cancellation IS a decision — auto_gate stopping an arm is a disposition
#     (the stop-vs-verdict distinction in auto_gate's own header governs what
#     the row may CLAIM, not whether deciding to stop was a decision).
#   * no-verdict / hold / refusal / deferral ARE decisions — the s55 audit
#     measured 29% of real window decisions as refusals/deferrals with no row
#     type to land on; an explicit withhold is the era's modal disposition.
#     `refusal` and `deferral` are NEW row types lanes may now write.
#   * negative / correction / inert / frozen ARE decisions (a road closed or a
#     number retracted is a disposition).
#   * screen / probe / calibration / cert are NOT decisions — they are
#     measurement or verification acts; the decision they feed gets its own row.
DECISION_KINDS = ("verdict", "keep", "discard", "refuted", "gate", "baseline",
                  "ship", "cancellation", "no-verdict", "hold", "negative",
                  "correction", "refusal", "deferral", "inert", "frozen")
ANALYSIS_KINDS = ("note", "caveat", "info", "screen", "probe", "calibration", "cert")
KNOWN_KINDS = DECISION_KINDS + ANALYSIS_KINDS


def _row_kind(r):
    """Kind of a tape row under the 7-field header schema, else None.

    ⛔ M2 (s55 audit): results.tsv carries a second, 9-field dialect (powered-
    read rows: id/date/trees/share/CI/n/note) whose index 5 is a NUMBER. The
    old `len(r) > 5 and r[5]` parse silently read those as unknown kinds and
    they zeroed the decision denominator on the day six n=5,400 verdicts
    landed. A fork row is NOT guessed at — it returns None and the callers
    COUNT and REPORT it, so schema drift is surfaced instead of swallowed.
    The schema unification itself is auto_gate/lane-side wrap debt."""
    if len(r) == 7:
        return r[5]
    return None


def _decisions_in_window(hours=None):
    """Decision rows NET-ADDED to results.tsv inside the git window.

    Matched to the numerator's population by construction: same `--since`, same
    git log, same definition of "new". A row that already existed is not a
    decision made in the window, and that is the whole bug this replaces.

    ⛔ NET, NOT GROSS, AND THE REASON IS A MEASURED FALSE SILENCE. The first
    version of this counted `+` lines only. The side lane then asked the one
    question a can-it-fire selftest cannot — *has the repaired row ever been
    able to read `ok`?* — and found its only non-degenerate quiet day in nine
    was an artefact:

        T-2d   79 docs / 527 "decisions" = 0.15  ok
        ...where 527 came from THREE commits whose diffs rewrote the whole file
           c380ae8  -1,308 +1,309  -> 309 phantom "rows added"
           3c3bedf  -1,308 +1,308  -> 308
           eea3be8  initial add    -> 235
        Two of those are ordinary content edits ("Lunds fixture unblocked",
        "Correct my own gate row") on a day that also carries commits titled
        "Repair shell-mangled backtick content in the tape row".

    **So a trailing-whitespace normalisation, a line-ending change, a column
    addition or any repair that rewrites the tape injected hundreds of phantom
    decisions and silenced the alarm for a full 24 hours — and it did so exactly
    when someone was doing bulk housekeeping on the decision tape, which is not
    independent of periods when decisions are not being made.**

    Subtracting removed decision rows fixes it without a magic constant: a
    rewrite removes 308 and adds 309, netting **1**; an honest append removes 0
    and adds 1, netting **1**. A genuine deletion lowers the count, which is the
    correct sign.
    """
    hours = CHURN_HOURS if hours is None else hours
    patch = _OVERRIDE.get("tape_patch")
    if patch is None:
        patch = subprocess.run(
            # --diff-filter=M excludes the commit that CREATED results.tsv.
            # A file creation is not a day's decisions: on 2026-08-09 `eea3be8`
            # contributed 235 phantom rows with nothing to net them against,
            # and net-counting alone left 170 of the 527. Modified-only leaves
            # 36, which matches the side lane's per-commit read of that day
            # ("every other commit 1-3 rows each") -- i.e. the residual is REAL.
            ["git", "log", f"--since={hours}.hours", "-p", "--unified=0",
             "--diff-filter=M", "--pretty=format:", "--", "results.tsv"],
            capture_output=True, text=True, cwd=ROOT).stdout
    added = removed = 0
    for ln in patch.splitlines():
        if ln.startswith("+++") or ln.startswith("---"):
            continue                       # diff headers, not content
        if ln.startswith("+"):
            f = ln[1:].split("\t")
            if len(f) > 5 and f[5] in DECISION_KINDS:
                added += 1
        elif ln.startswith("-"):
            f = ln[1:].split("\t")
            if len(f) > 5 and f[5] in DECISION_KINDS:
                removed += 1
    return max(added - removed, 0)


def stuck_planks():
    """Planks parked in KEEP-dev — the state that should not exist.

    docs/ship-gate.md: a plank is shipping, being fixed, or refuted. Anything
    that survives two windows in KEEP-dev is refuted by neglect.
    """
    rows = _OVERRIDE.get("tape") or list(csv.reader((ROOT / "results.tsv").read_text().splitlines(), delimiter="\t"))[1:]
    n = sum(1 for r in rows[-60:] if len(r) > 6 and "KEEP-dev" in r[6])
    return n, f"{n} KEEP-dev mentions in the last 60 tape rows"



def delegation_drought():
    """Decisions typed per subagent spawned — the drift Magnus has now caught
    TWICE by hand (s38: one agent in the first five hours while ~15 verdicts
    were typed inline; the standing-permission paragraph in the boot file did
    not prevent it, so a boot-run instrument does the asking instead).

    Numerator: dated coordination blocks in the last 24h whose header window
    carries a decision word (VERDICT/GATE/FINAL/TRIAGE/SHIP). Denominator:
    spawn announcements (the IN-FLIGHT convention names the model). High =
    many decisions, no delegation. Spawn-mentions must match SPAWN phrasing,
    not the word "agent" (retros discuss agents without spawning any).
    """
    # ⭐ M3 REPAIRS (s55 audit, fixed s57), three:
    #   (1) WHOLE FILE, not tail-2500 — the tail slice could fail to cover the
    #       24h window on a busy day and silently window on less than it claims.
    #   (2) 8-LINE BLOCK WINDOW, not 3 — real headers wrap over 4-6 lines and
    #       both regexes matched 0 of 7 real in-window headers under the old
    #       window. Vocabulary extended to the era's actual disposition words
    #       (ADOPTED/BANKED/REFUTED/CANCELLED) and spawn phrasing
    #       ("commissioned").
    #   (3) 0/0 WITH ACTIVITY IS BLIND, NOT HEALTHY. If dated in-window blocks
    #       exist and BOTH regexes match zero, the cell cannot distinguish a
    #       quiet day from format drift and must say so — it raises, and
    #       main()'s BLIND path reports it. A genuinely empty window (no dated
    #       blocks at all) still reads 0.0/ok.
    import re as _re
    from datetime import datetime, timedelta, timezone
    text = _OVERRIDE.get("deleg_coord")
    if text is None:
        text = (ROOT / "docs" / "coordination.md").read_text()
    now = _OVERRIDE.get("deleg_now") or datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=24)
    spawn_re = _re.compile(r"(sonnet|opus)\s+agent\b|agent\s+spawn|spawn(ed|ing)\b[^\n]{0,60}\bagent|commissioned\b[^\n]{0,80}\bagent", _re.I)
    dec_re = _re.compile(r"VERDICT|GATE[: ]|FINAL[: ]|TRIAGE|SHIP ANNOUNCEMENT|ADOPTED|BANKED|REFUTED|CANCELLED", _re.I)
    lines = text.splitlines()
    spawns = decisions = headers = 0
    for i, ln in enumerate(lines):
        m = _re.search(r"(\d{4}-\d{2}-\d{2})T(\d{2}):(\d{2}):(\d{2})Z", ln)
        if not m or not ln.lstrip().startswith("#"):
            continue
        try:
            ts = datetime.fromisoformat(f"{m.group(1)}T{m.group(2)}:{m.group(3)}:{m.group(4)}+00:00")
        except ValueError:
            continue
        if ts < cutoff:
            continue
        headers += 1
        window = "\n".join(lines[i:i + 8])
        if spawn_re.search(window):
            spawns += 1
        if dec_re.search(window):
            decisions += 1
    if headers >= 5 and spawns == 0 and decisions == 0:
        raise RuntimeError(
            f"matched 0 of {headers} dated in-window blocks on BOTH regexes — "
            "format drift, not a quiet day; the cell is BLIND")
    val = decisions / (spawns + 1)
    return val, (f"{decisions} decision blocks / {spawns} spawn announcements "
                 f"(24h, {headers} dated blocks scanned)")


CHECKS = [
    ("note:verdict ratio", note_verdict_ratio, 1.5, "analysis is outpacing decisions"),
    ("doc:code churn",     doc_code_churn,     1.0, "writing about the work faster than doing it"),
    ("ship cadence",       ship_cadence,       None, "decisions per hour has fallen"),
    ("stuck planks",       stuck_planks,       3,   "planks parked instead of shipped or refuted"),
    ("cross-lane analysis", cross_lane_analysis, 4.0, "analysis docs piling up across all lanes"),
    ("delegation drought", delegation_drought, 12.0, "verdicts typed inline while no subagent runs — context is the scarce resource"),
]


# Synthetic inputs that MUST trip each row. Deliberately extreme: the question
# is "can this alarm fire at all", not "does it fire at the right threshold".
_TRIPPERS = {
    "note:verdict ratio":  {"tape": [["", "", "", "", "", "note", "x"]] * 40},
    "doc:code churn":      {"numstat": "900\t0\tdocs/a.md\n1\t0\ttools/b.py\n"},
    "ship cadence":        {"elo": [["2026-08-09T10:00", "1", "1", "vX"]] * 5,
                            "hours": 20, "stealth": False},
    "stuck planks":        {"tape": [["", "", "", "", "", "note", "KEEP-dev"]] * 9},
    # cross-lane now reads NET-ADDED decision rows out of a git patch, not the
    # tape tail, so its tripper feeds a patch with exactly one added row.
    # The `+++` header line is included DELIBERATELY: it starts with `+` and a
    # parser that forgets to skip it would count it, so this fixture doubles as
    # the guard for that off-by-one.
    "cross-lane analysis": {"namestat": "docs/a.md\ndocs/b.md\ndocs/c.md\ndocs/d.md\n"
                                        "docs/e.md\n",
                            "tape_patch": "+++ b/results.tsv\n"
                                          "+a\tb\tc\td\te\tverdict\tx\n"},
    "delegation drought": {"deleg_coord": "\n".join(
        f"# 2026-08-14T0{i%10}:00:00Z — **BUILDER GATE: X FINAL typed**" for i in range(30)),
        "deleg_now": __import__("datetime").datetime(2026, 8, 14, 12, 0, tzinfo=__import__("datetime").timezone.utc)},
}

# THE QUIET DIRECTION. _TRIPPERS above only prove a row CAN fire; a row stuck at
# TRIP would pass that test, and so would a row that goes quiet for the wrong
# reason. These fixtures assert the row must still SAY THE UNCOMFORTABLE THING.
# Built from real history, not invented: the whole-file-rewrite case below is
# `c380ae8`/`3c3bedf` (hunk headers -1,308 +1,309 and -1,308 +1,308), which
# silenced this alarm for a full 24 hours on 2026-08-09.
_MUST_STILL_TRIP = {
    "cross-lane analysis": (
        {"namestat": "docs/a.md\ndocs/b.md\ndocs/c.md\ndocs/d.md\ndocs/e.md\n",
         # 300 decision rows REMOVED and 301 ADDED = a reformat, net 1 decision.
         "tape_patch": "+++ b/results.tsv\n---- a/results.tsv\n"
                       + "".join(f"-r{i}\tb\tc\td\te\tverdict\tx\n" for i in range(300))
                       + "".join(f"+r{i}\tb\tc\td\te\tverdict\tx\n" for i in range(301))},
        "a whole-file rewrite of the tape must NOT read as 301 decisions"),
    "delegation drought": (
        {"deleg_coord": "\n".join(
            f"# 2026-08-14T0{i%10}:00:00Z — **BUILDER VERDICT: the agent report was read; no agent needed**"
            for i in range(30)),
         "deleg_now": __import__("datetime").datetime(2026, 8, 14, 12, 0, tzinfo=__import__("datetime").timezone.utc)},
        "the word 'agent' in prose (reports READ, not spawned) must not silence the drought"),
    # M5(2): a day of fire→rollback churn. The OLD transition count read 12
    # transitions = 0.60/hr and stayed silent; only 6 are first-time versions,
    # 0.30/hr, and a churn day with no lasting ship MUST still read as a stall.
    "ship cadence": (
        {"elo": [["2026-08-09T10:%02d" % (i * 4), "1500", str(i), v]
                 for i, v in enumerate(
                     ["vBase"] + [x for k in range(6) for x in (f"vP{k}", "vBase")])],
         "now": __import__("datetime").datetime(2026, 8, 9, 12, 0),
         "hours": 20, "stealth": False},
        "6 fire+rollback pairs must read 6 ships (0.30/hr, TRIP), not 12 transitions (0.60, silent)"),
}

# THE OTHER VERDICT. The standing instrument rule requires every guard driven to
# BOTH verdicts — _TRIPPERS/_MUST_STILL_TRIP prove the alarm fires; these prove
# it can also stay QUIET on input that must not fire (a row stuck at TRIP passes
# every fixture above). Each entry: (override, must_not_trip_reason).
_MUST_NOT_TRIP = {
    # M4: five READOUT docs (published decisions) and one tape decision — the
    # old numerator read 5/1 = 5.0 TRIP; publishing decisions must not raise
    # the "no decisions" alarm.
    "cross-lane analysis": (
        {"namestat": "docs/research/BUILD-REPORT-a.md\ndocs/research/DECODE-b.md\n"
                     "docs/research/POWERED-READ-c.md\ndocs/research/TRANSFER-READ-d.md\n"
                     "docs/research/BUILD-REPORT-e.md\n",
         "tape_patch": "+++ b/results.tsv\n+a\tb\tc\td\te\tverdict\tx\n"},
        "readout docs are decisions being published, not analysis piling up"),
    # M3(3): a genuinely empty window (no dated blocks at all) is a quiet day,
    # not format drift — it must read 0.0/ok and must NOT raise BLIND.
    "delegation drought": (
        {"deleg_coord": "no dated headers here at all\n",
         "deleg_now": __import__("datetime").datetime(2026, 8, 14, 12, 0, tzinfo=__import__("datetime").timezone.utc)},
        "an empty 24h window is a quiet day, not a blind cell"),
    # M5(1): under STEALTH_UNTIL_DROP a zero-activation day is the directive —
    # the cell must report HELD (val None), never trip.
    "ship cadence": (
        {"elo": [["2026-08-09T10:00", "1500", "1", "vX"]] * 5,
         "hours": 20, "stealth": True},
        "a policy hold must read HELD, not a cadence stall"),
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
    # THE QUIET DIRECTION -- see _MUST_STILL_TRIP. Without these, a row that has
    # a known way to go silent for the wrong reason still passes above.
    if _MUST_STILL_TRIP:
        print("\n  -- and must it still fire on the input that WRONGLY silenced it? --")
    for name, fn, thresh, _why in CHECKS:
        fx = _MUST_STILL_TRIP.get(name)
        if not fx:
            continue
        override, why = fx
        _OVERRIDE.clear()
        _OVERRIDE.update(override)
        try:
            val, detail = fn()
        except Exception as e:
            print(f"  [ERROR] {name}: {e}")
            bad.append(f"{name} (quiet-direction)")
            continue
        trip = val < 0.5 if name == "ship cadence" else val >= thresh
        print(f"  [{'PASS' if trip else 'FAIL'}] {name:<20} -> {val:.2f}   ({why})")
        print(f"         {detail}")
        if not trip:
            bad.append(f"{name} (quiet-direction)")
    _OVERRIDE.clear()
    # THE OTHER VERDICT -- see _MUST_NOT_TRIP. A row stuck at TRIP passes every
    # fixture above; these drive each repaired guard to its quiet verdict.
    if _MUST_NOT_TRIP:
        print("\n  -- and does it stay QUIET on input that must not fire? --")
    for name, fn, thresh, _why in CHECKS:
        fx = _MUST_NOT_TRIP.get(name)
        if not fx:
            continue
        override, why = fx
        _OVERRIDE.clear()
        _OVERRIDE.update(override)
        try:
            val, detail = fn()
        except Exception as e:
            print(f"  [ERROR] {name}: {type(e).__name__}: {e}")
            bad.append(f"{name} (must-not-trip)")
            continue
        if val is None:
            trip = False
        elif name == "ship cadence":
            trip = val < 0.5
        else:
            trip = val >= thresh
        shown = "held" if val is None else f"{val:.2f}"
        print(f"  [{'FAIL' if trip else 'PASS'}] {name:<20} -> {shown}   ({why})")
        print(f"         {detail}")
        if trip:
            bad.append(f"{name} (must-not-trip)")
    _OVERRIDE.clear()
    # LIVE-TAIL -- the s55 audit's item (d): every fixture above is FROZEN, and
    # a frozen-fixture selftest passes 6/6 while the live surfaces drift out
    # from under the parsers (that is exactly what happened: 12% kind coverage,
    # 0/7 header matches, and this selftest was green throughout). These two
    # checks run against TODAY'S tape and TODAY'S coordination tail, so format
    # drift turns the boot check red instead of silently blinding a cell.
    print("\n  -- LIVE-TAIL: do the parsers recognize the surfaces as written TODAY? --")
    try:
        rows = list(csv.reader((ROOT / "results.tsv").read_text().splitlines(),
                               delimiter="\t"))[1:]
        tail = rows[-WINDOW_ROWS:]
        known = sum(1 for r in tail if _row_kind(r) in KNOWN_KINDS)
        fork = sum(1 for r in tail if len(r) != 7)
        frac = known / max(len(tail), 1)
        ok = frac >= 0.6
        print(f"  [{'PASS' if ok else 'FAIL'}] tape kind coverage    "
              f"{known}/{len(tail)} rows classified ({frac:.0%}; "
              f"{fork} schema-fork) -- FAIL below 60%")
        if not ok:
            bad.append("tape kind coverage (live-tail)")
    except Exception as e:
        print(f"  [ERROR] tape kind coverage: {type(e).__name__}: {e}")
        bad.append("tape kind coverage (live-tail)")
    try:
        val, detail = delegation_drought()      # raises if blocks exist and
        print(f"  [PASS] delegation regexes    {detail}")   # both regexes miss
    except RuntimeError as e:
        print(f"  [FAIL] delegation regexes    {e}")
        bad.append("delegation regexes (live-tail)")
    except Exception as e:
        print(f"  [ERROR] delegation regexes: {type(e).__name__}: {e}")
        bad.append("delegation regexes (live-tail)")
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
    blind = []
    print("AUDIT TRIGGER — is analysis outpacing decisions?\n")
    for name, fn, thresh, why in CHECKS:
        try:
            val, detail = fn()
        except Exception as e:                     # never let the alarm break a boot
            # ⛔ A CELL THAT COULD NOT EVALUATE IS **UNKNOWN**, NOT **NOT-TRIPPED**.
            # Measured 2026-08-15: a NameError in ship_cadence printed
            # `[skip] ship cadence: name 'timezone' is not defined` and the
            # summary then read `OK — 0/6 tripped; audit not indicated.` The one
            # cell that WAS tripping had gone silent and the verdict got
            # HEALTHIER for it. That is this repo's most-repeated defect --
            # "an alarm that cannot tell it is blind" -- living inside the boot
            # check whose whole job is to notice such things.
            print(f"  [BLIND] {name}: {type(e).__name__}: {e}")
            blind.append(name)
            continue
        if val is None:                    # a cell that REFUSES a verdict by
            print(f"  [held] {name:<20} {'—':<10} {detail}")     # policy (see
            continue                       # ship_cadence M5(1)) is neither
                                           # tripped nor blind, and says why.
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
    if blind:
        # Printed BEFORE any verdict, because it bounds what the verdict can mean.
        print(f"⚠ {len(blind)}/{len(CHECKS)} CELL(S) COULD NOT BE EVALUATED: "
              f"{', '.join(blind)}")
        print("  The count below is over the cells that RAN. A silent cell is not "
              "a passing cell —")
        print("  fix the error before reading 'audit not indicated' as reassurance.")
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
    ran = len(CHECKS) - len(blind)
    if blind:
        print(f"UNKNOWN — {len(tripped)}/{ran} of the cells that RAN tripped, "
              f"{len(blind)} BLIND. Not a clean bill of health.")
        return 2
    print(f"OK — {len(tripped)}/{len(CHECKS)} tripped; audit not indicated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
