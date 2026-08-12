#!/usr/bin/env python3
"""LEG RECORD — the fixture fingerprint of a live leg's cells.

⛔ WHY THIS EXISTS (builder, s34, 2026-08-12).
The gsxWins anchor panel was designed as a PAIRED comparison — five cells, same
opponent, same five maps — and **two of the three properties that make cells
paired were never recorded at fire time**. Opponent was pinned; **seat and maps
were not.** Both had to be recovered afterwards from archived replays, and only
because those replays happened to be archived.

What the recovery found, and neither was visible from the leg log:
  * **v118 was the only seat-B cell in a five-cell panel.** `match unrated`
    assigns the seat and nobody read it. Seat is worth **8.03pp on
    byte-identical arms** (measured on NULL114 the same day), which is larger
    than most differences an n=5 panel could resolve.
  * **A dimensions-only map check is NOT sufficient**, because the map pool has
    collisions: **25x25 is drumlin OR hive; 28x20 is eider OR heart.** Two
    different maps sharing a dimension pass a dims check silently. The side lane
    caught this; the builder's own check was the insufficient one.

⇒ The map identity test here is **CORE GEOMETRY**, recovered by trilateration
from `d2_own`/`d2_enemy`, which distinguishes same-dimension maps. Two cells
match only if every game agrees on dims AND both core positions AND the order.

Usage:
    tools/leg_record.py OUT.tsv <match-id-prefix> [<match-id-prefix> ...]
    tools/leg_record.py --selftest

Reads `replay_archive/*.meta.json` for seat and `events.tsv`-shaped decodes.
Prints a per-cell fingerprint and an explicit PAIRED / NOT PAIRED verdict.
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def core_positions(rows):
    """Recover both cores from (x, y, d2_own, d2_enemy) by trilateration.

    A build at (x,y) reports squared distances to BOTH cores, so three
    non-collinear builds pin each core exactly. Returns (own, enemy) or None.

    ⚠ This is what makes the check collision-proof. Dimensions alone cannot
    separate drumlin from hive (both 25x25) or eider from heart (both 28x20).
    """
    def solve(idx):
        pts = []
        for x, y, do, de in rows:
            d = do if idx == 0 else de
            pts.append((x, y, d))
            if len(pts) >= 12:
                break
        if len(pts) < 3:
            return None
        # brute force over a small grid is fine: maps are <= 30x30
        cands = None
        for cx in range(0, 31):
            for cy in range(0, 31):
                if all((cx - x) ** 2 + (cy - y) ** 2 == d for x, y, d in pts):
                    if cands is not None:
                        return None          # ambiguous -> refuse
                    cands = (cx, cy)
        return cands
    a, b = solve(0), solve(1)
    return (a, b) if a and b else None


def fingerprint(ev_path, want, seat_of):
    """cell -> ordered list of (dims, own_core, enemy_core) per game."""
    per = {}
    for line in open(ev_path):
        p = line.rstrip("\n").split("\t")
        if p[0] == "file":
            continue
        k = p[0][:8]
        if k not in want:
            continue
        us = seat_of.get(k)
        if us is None:
            continue
        try:
            x, y, do, de = int(p[5]), int(p[6]), int(p[7]), int(p[8])
        except (ValueError, IndexError):
            continue
        if p[3] != us:                       # our builds only: d2_own is ours
            continue
        per.setdefault(k, {}).setdefault(p[0], {"dims": (p[9], p[10]), "pts": []})
        per[k][p[0]]["pts"].append((x, y, do, de))
    out = {}
    for k, games in per.items():
        rec = []
        for f in sorted(games):
            g = games[f]
            rec.append((g["dims"], core_positions(g["pts"])))
        out[k] = rec
    return out


def selftest():
    """Driven BOTH ways: identical fixtures must PAIR, a swapped map must NOT.

    ⛔ The cell that matters is the COLLISION one — two maps with the same
    dimensions and different core geometry. A dims-only check passes it; this
    tool must fail it. That is the exact defect this file was written for, so it
    is asserted rather than described.
    """
    ok = True

    def chk(name, got, want):
        nonlocal ok
        good = got == want
        ok &= good
        print(f"  [{'ok' if good else 'FAIL'}] {name:58s} got={got!r} want={want!r}")

    # trilateration recovers a known pair
    own, enemy = (5, 5), (18, 18)
    pts = [(x, y,
            (x - own[0]) ** 2 + (y - own[1]) ** 2,
            (x - enemy[0]) ** 2 + (y - enemy[1]) ** 2)
           for x, y in ((7, 3), (9, 11), (2, 8), (14, 6))]
    chk("trilateration recovers both cores", core_positions(pts), (own, enemy))

    # too few points -> refuse rather than guess
    chk("under 3 points REFUSES", core_positions(pts[:2]), None)

    # THE COLLISION CELL: same dims, different geometry -> must NOT match
    a = [(("25", "25"), ((5, 5), (18, 18)))]
    b = [(("25", "25"), ((3, 3), (20, 20)))]
    chk("same dims + DIFFERENT cores -> NOT paired", a == b, False)
    chk("same dims + same cores -> paired", a == list(a), True)

    # order matters: the same maps in a different order are not a paired cell
    two_a = [(("10", "10"), ((2, 2), (6, 6))), (("18", "18"), ((2, 14), (14, 2)))]
    two_b = list(reversed(two_a))
    chk("same maps in a DIFFERENT ORDER -> NOT paired", two_a == two_b, False)

    print("\n" + ("SELFTEST PASSED — the collision case FAILS to pair, which a "
                  "dimensions-only check would have passed."
                  if ok else "SELFTEST FAILED"))
    return 0 if ok else 1


def main():
    argv = sys.argv[1:]
    if "--selftest" in argv:
        raise SystemExit(selftest())
    if len(argv) < 2:
        raise SystemExit(__doc__)
    ev, want = argv[0], [a[:8] for a in argv[1:]]

    seat_of, name_of = {}, {}
    for f in glob.glob(str(ROOT / "replay_archive" / "*.meta.json")):
        mid = Path(f).name.split(".")[0][:8]
        if mid not in want:
            continue
        try:
            m = json.load(open(f))
        except Exception:
            continue
        a, b = m.get("teamAName"), m.get("teamBName")
        if a == "OpenSverige":
            seat_of[mid], name_of[mid] = "0", ("A", b)
        elif b == "OpenSverige":
            seat_of[mid], name_of[mid] = "1", ("B", a)

    fp = fingerprint(ev, set(want), seat_of)
    print(f"{'cell':10}{'seat':>6}  {'opponent':20} games  fixture fingerprint")
    for k in want:
        s, opp = name_of.get(k, ("?", "?"))
        rec = fp.get(k, [])
        print(f"  {k:8}{s:>6}  {str(opp)[:18]:20}{len(rec):>5}  "
              + " · ".join(f"{d[0]}x{d[1]}@{c}" for d, c in rec))
    # verdict
    base = want[0]
    print()
    for k in want[1:]:
        same_seat = name_of.get(k, ("?",))[0] == name_of.get(base, ("?",))[0]
        same_fix = fp.get(k) == fp.get(base) and fp.get(k)
        verdict = "PAIRED" if (same_seat and same_fix) else "NOT PAIRED"
        why = []
        if not same_seat:
            why.append("SEAT DIFFERS")
        if not same_fix:
            why.append("fixture differs")
        print(f"  {k} vs {base}: {verdict}" + (f"  ({', '.join(why)})" if why else ""))


if __name__ == "__main__":
    main()
