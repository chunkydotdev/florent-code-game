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
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WINDOW_ROWS = 50          # tape rows to look back over (25 biases toward
                          # wrap time, when analysis rows legitimately cluster)
CHURN_HOURS = 24


def note_verdict_ratio():
    """Analysis rows vs decision rows on the verdict tape.

    Tonight's deadlock read 14 notes/caveats against 6 verdicts in the last 25
    rows — the project was documenting faster than it was deciding.
    """
    rows = list(csv.reader((ROOT / "results.tsv").open(), delimiter="\t"))[1:]
    tail = [r for r in rows if len(r) > 5][-WINDOW_ROWS:]
    c = Counter(r[5] for r in tail)
    analysis = c["note"] + c["caveat"] + c["info"]
    decisions = c["verdict"] + c["keep"] + c["discard"] + c["refuted"] + c["gate"]
    ratio = analysis / max(decisions, 1)
    return ratio, f"{analysis} analysis rows / {decisions} decision rows (last {len(tail)})"


def doc_code_churn():
    """Lines changed in prose vs in code, over the last day of commits.

    0.14 on the productive day; 1.88 on the deadlocked one.
    """
    out = subprocess.run(
        ["git", "log", f"--since={CHURN_HOURS}.hours", "--numstat", "--pretty=format:"],
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
            doc += n
        elif p[2].startswith(("bots/", "tools/")):
            code += n
    ratio = doc / max(code, 1)
    return ratio, f"{doc} prose lines / {code} code lines (last {CHURN_HOURS}h)"


def ship_cadence():
    """Ships per hour of active work, from the tape's own baseline rows."""
    rows = list(csv.reader((ROOT / "results.tsv").open(), delimiter="\t"))[1:]
    ships = [r for r in rows if len(r) > 6 and r[5] == "baseline" and "SHIP" in r[6][:60]]
    out = subprocess.run(
        ["git", "log", f"--since={CHURN_HOURS}.hours", "--pretty=format:%ad", "--date=format:%H"],
        capture_output=True, text=True, cwd=ROOT).stdout.split()
    active_hours = max(len(set(out)), 1)
    recent = len([r for r in ships][-12:])          # ships still visible on the tape tail
    rate = recent / active_hours
    return rate, f"~{recent} recent ships over ~{active_hours} active hours"


def stuck_planks():
    """Planks parked in KEEP-dev — the state that should not exist.

    docs/ship-gate.md: a plank is shipping, being fixed, or refuted. Anything
    that survives two windows in KEEP-dev is refuted by neglect.
    """
    rows = list(csv.reader((ROOT / "results.tsv").open(), delimiter="\t"))[1:]
    n = sum(1 for r in rows[-60:] if len(r) > 6 and "KEEP-dev" in r[6])
    return n, f"{n} KEEP-dev mentions in the last 60 tape rows"


CHECKS = [
    ("note:verdict ratio", note_verdict_ratio, 1.5, "analysis is outpacing decisions"),
    ("doc:code churn",     doc_code_churn,     1.0, "writing about the work faster than doing it"),
    ("ship cadence",       ship_cadence,       None, "decisions per hour has fallen"),
    ("stuck planks",       stuck_planks,       3,   "planks parked instead of shipped or refuted"),
]


def main():
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
        print(f"*** FIRE: {len(tripped)}/4 signals tripped ***")
        for n, why in tripped:
            print(f"      - {n}: {why}")
        print()
        print("  Spawn a SHORT-LIVED AUDIT SESSION. Its only job: ask whether the")
        print("  instruments can support the decisions being made. Give it no stake")
        print("  in the current queue and let it stop when it reports.")
        print("  Prior art: docs/workflow-analysis/ (2026-08-08, found 19% power).")
        return 1
    print(f"OK — {len(tripped)}/4 tripped; audit not indicated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
