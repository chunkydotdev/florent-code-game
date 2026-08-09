#!/usr/bin/env python3
"""The two cuts that decide it, added after the first pass surfaced a fourth
confound the brief did not anticipate: CAD IS BROKE.

1. THE PERMANENT-LATCH SIGNATURE.  The hypothesis, as stated by its author, is
   not "a lower build rate" but "CAD never executed another build action" --
   total, for the rest of the game, with money in hand.  So count games where
   CAD's build count from first core damage to the final round is EXACTLY ZERO,
   over a long enough tail to mean anything, with a builder alive.  A depressed
   rate is explicitly NOT this mechanism.

2. MONEY.  CAD's scripted r4 all-in ammo conversion leaves it at single-digit to
   ~100 titanium, and an opponent close enough to hit the core by r13 is also
   close enough to be eating the harvesters that would refill it.  So "zero
   builds" may be "cannot afford anything".  The discriminator is IDLE-RICH
   ROUNDS: rounds in the window where CAD built nothing WHILE holding enough
   titanium to build.  Paralysis predicts many idle-rich rounds; poverty
   predicts almost none.

   Threshold: 36 Ti, the scaled builder-bot cost after a couple of builds
   (base 30, +20% each).  A cheaper floor (a 3 Ti barrier / conveyor) is also
   reported, because "could not afford ANYTHING" is the strongest poverty claim.

Usage: latch.py <freeze_dir>
"""
from __future__ import annotations

import collections
import statistics
import sys

sys.path.insert(0, "docs/research/scripts/cad-lockout-2026-08-09")
from analyse import summarise, band_of, win, i, BANDS  # noqa: E402

RICH = 36     # scaled builder-bot money
CHEAP = 6     # a splitter; below this CAD can build literally nothing


def main(d):
    games = summarise(d)
    P = sys.stdout.write

    P("# The permanent-latch signature and the money confound\n\n")

    P("## 1. PERMANENT LATCH: zero builds from first core damage to game end\n")
    P("Restricted to games with a tail of >= 30 rounds after first damage, so a\n")
    P("game that simply ended cannot masquerade as a latch.\n\n")
    P(f"{'band':8s} {'n(tail>=30)':>12s} {'latched(0 builds)':>18s} "
      f"{'latched w/ builder alive':>25s} {'median builds in tail':>22s}\n")
    latched_games = []
    for name, lo, hi in BANDS:
        fs = [f for f, g in games.items()
              if band_of(g["first_dmg"]) == name
              and g["n"] - g["first_dmg"] >= 30]
        tails, lat, latb = [], 0, 0
        for f in fs:
            g = games[f]
            t = win(g["rs"], g["first_dmg"], 10 ** 6, "cad_builds")
            tails.append(t)
            if t == 0:
                lat += 1
                alive = max(i(r, "cad_bots") for r in g["rs"]
                            if i(r, "rnd") >= g["first_dmg"])
                if alive > 0:
                    latb += 1
                    latched_games.append((name, f, g))
        P(f"{name:8s} {len(fs):>12d} {lat:>18d} {latb:>25d} "
          f"{statistics.median(tails) if tails else '-':>22}\n")

    P("\nThe latched games, individually:\n")
    for name, f, g in latched_games:
        P(f"  [{name}] {f[:8]} g{g['pop']['game']} v{g['pop']['cad_ver']} vs "
          f"{g['pop']['opp'][:18]:18s} {g['mapname'][:16]:16s} first_dmg r"
          f"{g['first_dmg']:>3d} rounds {g['n']:>4d} coredied "
          f"{int(g['cad_core_died'])}\n")
    if not latched_games:
        P("  (none)\n")

    P("\n## 2. MONEY: are the zero-build windows poverty or paralysis?\n")
    P(f"IDLE-RICH = a round in the window with 0 builds and >= {RICH} Ti "
      f"(scaled builder-bot money).\n")
    P(f"BROKE = a round with < {CHEAP} Ti, when CAD could not build anything "
      f"at all.\n\n")
    for wa, wb in ((14, 40),):
        P(f"### window r{wa}-r{wb}\n")
        P(f"{'band':8s} {'n':>4s} {'med Ti':>7s} {'med idle-rich rnds':>19s} "
          f"{'med broke rnds':>15s} {'zero-build games':>17s} "
          f"{'  of those, med idle-rich':>25s}\n")
        for name, lo, hi in BANDS + [("never", None, None)]:
            fs = [f for f, g in games.items()
                  if band_of(g["first_dmg"]) == name and g["n"] > wb]
            if not fs:
                continue
            med_ti, idle, broke, zb, zb_idle = [], [], [], 0, []
            for f in fs:
                rs = [r for r in games[f]["rs"] if wa <= i(r, "rnd") <= wb]
                tis = [i(r, "cad_ti") for r in rs]
                med_ti.append(statistics.median(tis))
                ir = sum(1 for r in rs
                         if i(r, "cad_builds") == 0 and i(r, "cad_ti") >= RICH)
                br = sum(1 for r in rs if i(r, "cad_ti") < CHEAP)
                idle.append(ir)
                broke.append(br)
                if sum(i(r, "cad_builds") for r in rs) == 0:
                    zb += 1
                    zb_idle.append(ir)
            P(f"{name:8s} {len(fs):>4d} {statistics.median(med_ti):>7.0f} "
              f"{statistics.median(idle):>19.0f} {statistics.median(broke):>15.0f} "
              f"{zb:>17d} "
              f"{(statistics.median(zb_idle) if zb_idle else float('nan')):>25.0f}\n")

    P("\n### the zero-build games in the <=r13 band, individually "
      "(window r14-r40)\n")
    P(f"{'file':10s} {'v':>4s} {'opp':18s} {'medTi':>6s} {'maxTi':>6s} "
      f"{'idle-rich':>10s} {'broke':>6s} {'bots':>5s} {'harv+conv alive?':>10s}\n")
    for f, g in sorted(games.items(), key=lambda kv: kv[0]):
        if band_of(g["first_dmg"]) != "<=r13" or g["n"] <= 40:
            continue
        rs = [r for r in g["rs"] if 14 <= i(r, "rnd") <= 40]
        if sum(i(r, "cad_builds") for r in rs) != 0:
            continue
        tis = [i(r, "cad_ti") for r in rs]
        ir = sum(1 for r in rs if i(r, "cad_ti") >= RICH)
        br = sum(1 for r in rs if i(r, "cad_ti") < CHEAP)
        P(f"{f[:8]:10s} {g['pop']['cad_ver']:>4s} {g['pop']['opp'][:18]:18s} "
          f"{statistics.median(tis):>6.0f} {max(tis):>6d} {ir:>10d} {br:>6d} "
          f"{statistics.median([i(r,'cad_bots') for r in rs]):>5.0f}\n")

    P("\n## 3. CLEAN PRE-DAMAGE BUILD RATE (reverse causation, per game)\n")
    P("builds in rounds [6, first_dmg-1], per round -- strictly BEFORE any\n")
    P("damage landed in that game. Empty for games damaged at/below r6.\n\n")
    for name, lo, hi in BANDS + [("never", None, None)]:
        fs = [f for f, g in games.items() if band_of(g["first_dmg"]) == name]
        rates = []
        for f in fs:
            g = games[f]
            end = (g["first_dmg"] - 1) if g["first_dmg"] is not None else 13
            if end < 6:
                continue
            n = end - 6 + 1
            rates.append(win(g["rs"], 6, end, "cad_builds") / n)
        P(f"  {name:8s} n={len(rates):3d}  median builds/round pre-damage "
          f"{statistics.median(rates) if rates else '-':.2f}\n"
          if rates else f"  {name:8s} n=0\n")

    P("\n## 4. DOES CAD RESUME? builds in the LATE tail of trigger-cell games\n")
    for name, lo, hi in BANDS:
        fs = [f for f, g in games.items()
              if band_of(g["first_dmg"]) == name and g["n"] > 120]
        if not fs:
            continue
        a = [win(games[f]["rs"], 41, 80, "cad_builds") for f in fs]
        b = [win(games[f]["rs"], 81, 120, "cad_builds") for f in fs]
        P(f"  {name:8s} n={len(fs):3d}  r41-80 median {statistics.median(a):.1f}"
          f"   r81-120 median {statistics.median(b):.1f}\n")


if __name__ == "__main__":
    main(sys.argv[1])
