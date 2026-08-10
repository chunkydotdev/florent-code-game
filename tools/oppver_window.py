#!/usr/bin/env python3
"""OPPONENT-VERSION WINDOW CHECK — did a cell ship a new bot mid-leg?

    .venv/bin/python tools/oppver_window.py scratchpad/arm_panel3.txt
    .venv/bin/python tools/oppver_window.py --selftest

WHY THIS EXISTS (s28). We pin OUR version, assert the holder before every
challenge, and verify `teamAVersion` on the platform. **Nothing pins or reads
THEIRS** — and if an opponent ships mid-leg, "our treatment is worse" and "their
bot got better" fit the data identically.

**`match info` returns `teamBVersion = None` for UNRATED matches**, which is the
fixture every one of our legs runs on. I recorded that as *"D18 is structurally
impossible on our main fixture"*. **That was too strong and the side lane was
right to push back: the opponent's version is RECOVERABLE BY TIMESTAMP JOIN,
because our panel cells play the rated ladder too**, and `league_matches.tsv`
carries `teamAVersion`/`teamBVersion` league-wide.

**It is not theoretical.** `Lunds Stallions` — a PANEL-3 cell — shipped **six
versions in under eighteen hours**. Any leg spanning more than a couple of hours
can straddle a boundary, and PANEL-3 itself ran 15:43-18:00Z.

**The route was already proven before it was named:** the same join is what
killed the Ouroboros "frozen v8" finding and what checked The Bisons. This
turns it from something done when a result looks surprising into something a leg
declares up front.

VERDICT PER CELL:
  CLEAN        — one version across the whole leg window; D18 satisfiable.
  STRADDLED    — the cell shipped inside the window; that cell's games are
                 UNATTRIBUTABLE between our change and theirs, and must say so.
  UNKNOWN      — no ladder appearances near the window; we cannot tell, which
                 is not the same as clean.
"""
from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FCODE = str(ROOT / ".venv" / "bin" / "fcode")
US = "379a5d80-9921-4c9e-949b-f9b1dcba16be"

_OVERRIDE: dict = {}


def timeline(team: str) -> list[tuple[str, str]]:
    """[(first_seen_utc, version)] for a team, from the league-wide tape."""
    if "timeline" in _OVERRIDE:
        return _OVERRIDE["timeline"].get(team, [])
    seen: dict[str, str] = {}
    path = ROOT / "corpus" / "league_matches.tsv"
    if not path.exists():
        return []
    for r in csv.DictReader(path.open(), delimiter="\t"):
        for s, _o in (("A", "B"), ("B", "A")):
            if r.get(f"team{s}Name") != team:
                continue
            v, when = r.get(f"team{s}Version"), r.get("createdAt") or ""
            if not v or v == "None" or not when:
                continue
            if v not in seen or when < seen[v]:
                seen[v] = when
    return sorted(((w, v) for v, w in seen.items()))


def leg_window(arm_file: Path) -> tuple[str, str, dict[str, list[str]]]:
    """(start, end, {cell: [match ids]}) read from the PLATFORM, not the file."""
    if "window" in _OVERRIDE:
        return _OVERRIDE["window"]
    ids = re.findall(r'"matchId": "([0-9a-f-]+)"', arm_file.read_text())
    cells: dict[str, list[str]] = {}
    stamps = []
    r = subprocess.run([FCODE, "match", "list", "--mine", "--json", "--limit", "200"],
                       capture_output=True, text=True)
    body = r.stdout[r.stdout.find("{"):] if "{" in r.stdout else ""
    if not body:
        return "", "", {}
    for m in json.loads(body).get("matches", []):
        if m["id"] not in ids:
            continue
        opp = m["teamBName"] if m["teamAId"] == US else m["teamAName"]
        cells.setdefault(opp, []).append(m["id"])
        stamps.append(m["createdAt"])
    if not stamps:
        return "", "", {}
    return min(stamps), max(stamps), cells


def classify(cell: str, start: str, end: str) -> tuple[str, str]:
    tl = timeline(cell)
    if not tl:
        return "UNKNOWN", "no ladder appearances on the league tape"
    inside = [(w, v) for w, v in tl if start <= w <= end]
    before = [(w, v) for w, v in tl if w < start]
    cur = before[-1][1] if before else (tl[0][1] if tl else "?")
    if inside:
        shipped = ", ".join(f"v{v}@{w[11:16]}" for w, v in inside)
        return "STRADDLED", f"was v{cur}; shipped {shipped} INSIDE the window"
    if not before:
        return "UNKNOWN", "first seen after the window started"
    return "CLEAN", f"v{cur} throughout ({len(tl)} versions on record all-time)"


def selftest() -> int:
    print("OPPVER WINDOW SELFTEST\n")
    tl = {"Shipper": [("2026-08-10T10:00:00Z", "1"), ("2026-08-10T16:00:00Z", "2")],
          "Steady":  [("2026-08-09T10:00:00Z", "7")],
          "Ghost":   []}
    _OVERRIDE["timeline"] = tl
    cases = [("Shipper", "STRADDLED"), ("Steady", "CLEAN"), ("Ghost", "UNKNOWN")]
    bad = 0
    for cell, want in cases:
        got, why = classify(cell, "2026-08-10T15:00:00Z", "2026-08-10T18:00:00Z")
        ok = got == want
        print(f"  [{'ok' if ok else 'FAIL'}] {cell:<10} -> {got:<10} {why}")
        if not ok:
            bad += 1
            print(f"          expected {want}")
    _OVERRIDE.clear()
    print()
    if bad:
        print(f"*** {bad} wrong ***")
        return 1
    print("PASS: separates a mid-window ship from a steady cell, and refuses to "
          "call an unobserved cell clean.")
    return 0


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    if not argv:
        print(__doc__)
        return 2
    arm = Path(argv[0])
    start, end, cells = leg_window(arm)
    if not cells:
        print(f"no matches resolved from {arm}")
        return 1
    print(f"LEG WINDOW {start[:19]} -> {end[:19]}   ({len(cells)} cells)\n")
    straddled = 0
    for cell in sorted(cells):
        verdict, why = classify(cell, start, end)
        flag = "**" if verdict == "STRADDLED" else "  "
        print(f"  {flag} {cell[:24]:<24} {verdict:<10} {why}")
        straddled += verdict == "STRADDLED"
    if straddled:
        print(f"\n** {straddled} cell(s) SHIPPED INSIDE THE LEG WINDOW. Those "
              f"games cannot separate our change from theirs. Say so in the "
              f"read-out. **")
        return 1
    print("\n  no cell shipped inside the window — D18 satisfied for this leg")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
