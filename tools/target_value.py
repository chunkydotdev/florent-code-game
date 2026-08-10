#!/usr/bin/env python3
"""TARGET VALUE GATE — what does beating this opponent actually PAY?

    .venv/bin/python tools/target_value.py vjg Troupe "The Bisons" 0033
    .venv/bin/python tools/target_value.py --band          # who is reachable
    .venv/bin/python tools/target_value.py --selftest

RUN THIS BEFORE WRITING A PRE-REGISTRATION. One line in the prereg:
    TARGET BAND: <opponents>, gaps <a..b>, win pays <x..y>, reachable YES/NO

WHY THIS EXISTS — and the case is s28 itself, not a hypothetical.
On 2026-08-10 we built and fired a crash-induction leg that passed **every check
this repo has**: pre-registered before the fact, 8 ADD-only amendments all blind
to the data, a placebo reading exactly 0/164, the dose delivered 150 times,
every control driven to the other verdict, lock cert two-clock clean, holder
asserted before every challenge, prototype exposure 10 seconds per cycle.

**It was aimed at four teams 550-860 points BELOW us, where a win pays ~0.2-1.0
rating points and a loss costs ~31.**

**The machinery inspects the EXPERIMENT and never asks whether the QUESTION is
worth answering.** No amount of rigour inside a leg reaches that, which is why
this is a gate in front of pre-registration rather than another clause inside
one. It takes thirty seconds and it would have redirected the whole session.

THE TWO FACTS IT ENCODES, both measured on our own tape:

1. **The ladder scores GAME SHARE: `delta = 32 x (S - E)`, S = games/5.**
   Verified residual 0.000000 across 100 matches (research: 0.0000 across 678).
   So the value of a matchup is not "can we win" but "how much margin moves".

2. **The ladder only pairs neighbours.** 94.0% of 678 matches within +-100;
   since passing 1600 the entire observed range is -78.1 to +122.3. **Anything
   outside ~`us-80 .. us+125` cannot be met** -- it is a destination, not an
   opponent.

NOT A VETO. A low-value target can still be the right leg (LOKI-14b's negative
closes a road properly, and closing a road is worth something). **The gate makes
you write the number down BEFORE the work, not defend it after.**
"""
from __future__ import annotations

import csv
import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FCODE = str(ROOT / ".venv" / "bin" / "fcode")
OUR_TEAM = "OpenSverige"

K = 32
BAND_LO, BAND_HI = -80, 125      # measured reachable window, relative to us

_OVERRIDE: dict = {}


def _live_ratings() -> tuple[float, dict[str, float]]:
    """(our rating, {team: rating}) from the freshest source available.

    `league_matches.tsv` is kept current by the keeper (s28); each team's most
    recent `rating*Before` is its latest known rating.
    """
    if "ratings" in _OVERRIDE:
        return _OVERRIDE["ours"], _OVERRIDE["ratings"]
    ours, best = 0.0, {}
    seen: dict[str, str] = {}
    path = ROOT / "corpus" / "league_matches.tsv"
    if path.exists():
        for r in csv.DictReader(path.open(), delimiter="\t"):
            when = r.get("createdAt") or ""
            for side, other in (("A", "B"), ("B", "A")):
                name = r.get(f"team{side}Name")
                rt = r.get(f"rating{side}Before")
                if not name or not rt:
                    continue
                try:
                    rt = float(rt)
                except ValueError:
                    continue
                if when >= seen.get(name, ""):
                    seen[name] = when
                    best[name] = rt
    ours = best.get(OUR_TEAM, 0.0)
    # prefer the platform for OUR rating -- it is one cheap call and it is the
    # number every gap is measured from
    try:
        out = subprocess.run([FCODE, "status"], capture_output=True, text=True).stdout
        for line in out.splitlines():
            if "Rating:" in line:
                ours = float(line.split("Rating:")[1].split()[0])
    except Exception:
        pass
    return ours, best


def value(gap: float) -> tuple[float, float, float]:
    """(E, rating gained by a 5-0, rating lost by a 0-5) at this rating gap.

    gap = opponent - us. Uses the exact ladder rule delta = K*(S-E).
    """
    e = 1.0 / (1.0 + 10 ** (gap / 400.0))
    return e, K * (1.0 - e), K * (0.0 - e)


def selftest() -> int:
    """Drive the gate to both verdicts: a worthless target and a valuable one."""
    print("TARGET VALUE SELFTEST\n")
    bad = 0
    cases = [
        ("parity", 0, 0.500, 16.00, -16.00, True),
        ("900 below (the s28 carriers)", -900, 0.9931, 0.22, -31.78, False),
        ("+400 above (unreachable)", 400, 0.0909, 29.09, -2.91, False),
        ("+111 (0033, reachable)", 111, 0.3450, 20.96, -11.04, True),
    ]
    for label, gap, we, wwin, wloss, wreach in cases:
        e, win, loss = value(gap)
        reach = BAND_LO <= gap <= BAND_HI
        ok = (abs(e - we) < 0.005 and abs(win - wwin) < 0.05
              and abs(loss - wloss) < 0.05 and reach == wreach)
        print(f"  [{'ok' if ok else 'FAIL'}] {label:<30} gap {gap:+5} "
              f"E={e:.3f} win {win:+6.2f} loss {loss:+6.2f} "
              f"reachable={'YES' if reach else 'NO '}")
        if not ok:
            bad += 1
            print(f"          expected E={we} win={wwin} loss={wloss} reach={wreach}")
    print()
    if bad:
        print(f"*** {bad} case(s) wrong ***")
        return 1
    print("PASS: values a worthless target near zero and a reachable one near "
          "parity, and the band flag separates them.")
    return 0


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    ours, ratings = _live_ratings()
    if not ours:
        print("REFUSING: could not establish our own rating -- the gap every "
              "number here depends on. Check `fcode status`.")
        return 1

    if "--band" in argv:
        rows = [(n, r, r - ours) for n, r in ratings.items() if n != OUR_TEAM]
        rows = [x for x in rows if BAND_LO <= x[2] <= BAND_HI]
        rows.sort(key=lambda x: -x[2])
        print(f"REACHABLE BAND at our {ours:.0f}: "
              f"us{BAND_LO:+d} .. us{BAND_HI:+d}  ({len(rows)} teams)\n")
        print(f"  {'team':<26}{'rating':>8}{'gap':>7}{'5-0 pays':>10}{'0-5 costs':>11}")
        for n, r, g in rows:
            _e, w, l = value(g)
            print(f"  {n[:26]:<26}{r:>8.0f}{g:>+7.0f}{w:>+10.2f}{l:>+11.2f}")
        return 0

    names = [a for a in argv if not a.startswith("--")]
    if not names:
        print(__doc__)
        return 2

    print(f"our rating {ours:.0f}   (reachable band us{BAND_LO:+d}..us{BAND_HI:+d})\n")
    print(f"  {'opponent':<26}{'rating':>8}{'gap':>7}{'5-0 pays':>10}"
          f"{'0-5 costs':>11}  reachable")
    gaps, pays = [], []
    unknown = []
    for n in names:
        r = ratings.get(n)
        if r is None:
            unknown.append(n)
            continue
        g = r - ours
        _e, w, l = value(g)
        gaps.append(g)
        pays.append(w)
        print(f"  {n[:26]:<26}{r:>8.0f}{g:>+7.0f}{w:>+10.2f}{l:>+11.2f}"
              f"  {'YES' if BAND_LO <= g <= BAND_HI else '** NO **'}")
    for n in unknown:
        print(f"  {n[:26]:<26}{'?':>8}{'?':>7}{'?':>10}{'?':>11}  ** UNKNOWN **")
    if not gaps:
        print("\nno known opponents -- cannot value this target")
        return 1

    reach = sum(1 for g in gaps if BAND_LO <= g <= BAND_HI)
    print(f"\nTARGET BAND: gaps {min(gaps):+.0f}..{max(gaps):+.0f}, "
          f"a 5-0 pays {min(pays):.2f}..{max(pays):.2f}, "
          f"reachable {reach}/{len(gaps)}")
    if reach == 0:
        print("** NO TARGET IS REACHABLE ON THE LADDER. Even a total success "
              "here cannot be converted into rating by playing them. **")
    if max(pays) < 5.0:
        print(f"** A PERFECT RESULT PAYS UNDER 5 RATING POINTS ({max(pays):.2f}). "
              f"Say in the prereg why the leg is worth running anyway. **")
    print("\nCopy this line into the pre-registration as `TARGET BAND:`.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
