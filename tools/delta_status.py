#!/usr/bin/env python3
"""DELTA STATUS — which retro deltas are ENFORCED, and which are only prose?

    .venv/bin/python tools/delta_status.py            # the ledger
    .venv/bin/python tools/delta_status.py --open     # only the undischarged
    .venv/bin/python tools/delta_status.py --selftest

===== WHY THIS EXISTS, AND IT IS A MEASUREMENT, NOT A SUSPICION =====
Magnus, 2026-08-11, at the s29 wrap: *"How do you handle actionable items from
the retro?"* I went to check instead of answering, and the answer was bad:

    of s28's EIGHT deltas (D33-D40), exactly ONE (D34) is referenced by any
    tool. Seven are prose. There are 35 D-numbered rules in a 30,000-line
    coordination.md.

**A retro that produces prose produces nothing.** This repo's own standard says
so — *"every prose-only rule in this repo has a recorded violation by its own
author; the two durable surfaces are this file and tools that exit 1."* The
deltas are written on the surface the standard names as NOT durable.

**AND IT IS D52b APPLIED TO THE RETRO ITSELF:** a correction lands where it was
discovered — in the wrap, in `coordination.md` — never where it will be read.

===== WHAT COUNTS AS DISCHARGED, AND THE BAR IS DELIBERATELY LOW =====
A delta is ENFORCED if its number appears in `tools/` (a tool implements or cites
it) or in an always-loaded file (`CLAUDE.md`, `.claude/commands/*.md`,
`PROGRAMME.md`). That is a WEAK test on purpose: citation is not enforcement, and
a delta can be cited by a tool that ignores it. **This measures the FLOOR — if a
delta is not even mentioned anywhere durable, it is certainly prose.** A number
that looks bad under a weak test is worse than it looks, not better.

**NOT EVERY DELTA SHOULD BE ENFORCED.** Some are judgement ("ask what in the diff
can change the metric"), and mechanising judgement produces a checkbox. The point
is not to drive OPEN to zero — it is that **the count should be a DECISION rather
than an accident**, and right now nobody has ever seen it.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COORD = ROOT / "docs" / "coordination.md"
# Surfaces that are actually loaded or actually run. `docs/` is deliberately
# EXCLUDED: a delta cited only by another doc is prose citing prose, which is the
# failure mode rather than the fix.
DURABLE_DIRS = ["tools", ".claude"]
DURABLE_FILES = ["CLAUDE.md", "PROGRAMME.md", "HANDOVER.md"]

_DELTA = re.compile(r"^#{2,4}\s*(D\d+[a-z]?)\s*[—\-–]\s*(.+)$")


def deltas(path: Path = COORD) -> list[tuple[str, str]]:
    """(id, headline) for every delta heading, newest last, de-duplicated."""
    if not path.exists():
        return []
    seen: dict[str, str] = {}
    for line in path.read_text(errors="replace").splitlines():
        m = _DELTA.match(line.strip())
        if m:
            seen.setdefault(m.group(1), m.group(2).strip())
    return sorted(seen.items(), key=lambda kv: (len(kv[0]), kv[0]))


def _grep(token: str) -> list[str]:
    """Files on a durable surface mentioning the delta id, word-bounded.

    Word boundaries matter: plain `D4` matches D41-D49 and every `D40`-ish
    string, which is the same substring bug that made `plank_status` report
    `loki1` stale for `loki19` commits."""
    # ⛔ NOT `git grep -E "\bD34\b"`. git grep's ERE engine does NOT support \b
    # and matches NOTHING silently -- the first run of this tool reported
    # "0/17 enforced" while `git grep -n D34` found three files. Its own selftest
    # caught it, which is the only reason the 0 was never published as a finding.
    # A regex feature that is unsupported rather than wrong is the worst kind:
    # it fails to the empty set, which reads as a clean answer.
    args = ["git", "grep", "-l", "-F", token, "--", *DURABLE_DIRS, *DURABLE_FILES]
    r = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    pat = re.compile(rf"(?<![A-Za-z0-9]){re.escape(token)}(?![A-Za-z0-9])")
    out = []
    for f in r.stdout.strip().splitlines():
        if not f:
            continue
        try:
            if pat.search((ROOT / f).read_text(errors="replace")):
                out.append(f)          # word-bounded in PYTHON, where \b works
        except OSError:
            continue
    return out


def status(path: Path = COORD):
    rows = []
    for did, headline in deltas(path):
        hits = _grep(did)
        rows.append((did, headline, hits))
    return rows


def main(argv):
    if "--selftest" in argv:
        return selftest()
    only_open = "--open" in argv
    rows = status()
    if not rows:
        print("no deltas found -- has coordination.md moved?")
        return 1
    enforced = [r for r in rows if r[2]]
    openr = [r for r in rows if not r[2]]
    show = openr if only_open else rows
    for did, headline, hits in show:
        tag = f"ENFORCED  {', '.join(hits[:2])}" if hits else "PROSE ONLY"
        print(f"  [{tag:<44}] {did:<5} {headline[:76]}")
    n = len(rows)
    print(f"\n{len(enforced)}/{n} deltas appear on a durable surface "
          f"({len(openr)} prose-only).")
    if openr:
        print("PROSE-ONLY IS NOT AUTOMATICALLY WRONG -- some deltas are judgement and "
              "\nmechanising judgement produces a checkbox. The point is that this "
              "count\nshould be a DECISION, not an accident. Triage, do not "
              "reflexively drive it to zero.")
    # Deliberately exits 0. This is a LEDGER, not a gate: a boot check that fails
    # on "you have unenforced ideas" is one every session learns to skip, and this
    # repo has already logged what a disbelieved alarm is worth.
    print(f"\nDELTA_STATUS: {len(enforced)} enforced / {len(openr)} prose-only")
    return 0


def selftest() -> int:
    """Drive it to BOTH verdicts on a fixture, not on the live repo."""
    import tempfile
    bad = 0
    with tempfile.TemporaryDirectory() as td:
        f = Path(td) / "coord.md"
        f.write_text(
            "### D99 — a delta no tool mentions\n"
            "some prose\n"
            "### D34 — a delta a tool DOES mention\n"
            "more prose\n"
            "## D99 — duplicate heading, must not double-count\n"
        )
        ds = deltas(f)
        ids = [d for d, _ in ds]
        for label, got, want in [
            ("parses both deltas", sorted(ids), ["D34", "D99"]),
            ("de-duplicates a repeated id", len(ids), 2),
            ("keeps the headline", ds[ids.index("D34")][1][:24], "a delta a tool DOES ment"),
        ]:
            ok = got == want
            bad += 0 if ok else 1
            print(f"  [{'ok' if ok else 'FAIL'}] {label:<38} got={got!r}")

        # The live half: D34 IS cited by tools/map_admits.py and D99 is not.
        # If these came out the same, the grep would be doing nothing.
        d34, d99 = _grep("D34"), _grep("D99")
        for label, got, want in [
            ("D34 (real, cited by a tool) -> found", bool(d34), True),
            ("D99 (invented) -> NOT found", bool(d99), False),
        ]:
            ok = got == want
            bad += 0 if ok else 1
            print(f"  [{'ok' if ok else 'FAIL'}] {label:<38} got={got}")
    print("\nPASS: parses and de-duplicates, and separates a cited delta from an "
          "uncited one on the live tree."
          if not bad else f"\n*** {bad} case(s) wrong ***")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
