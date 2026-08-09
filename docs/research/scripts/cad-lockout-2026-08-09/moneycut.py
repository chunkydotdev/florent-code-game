#!/usr/bin/env python3
"""THE DECISIVE CUT.

The first pass found the landmark effect is real: CAD builds far less in r14-r40
in games where its core was already damaged.  It also found a confound the brief
did not anticipate -- CAD is often BROKE.

`opening.py` then found why, and it is not uniform: CAD's r4 all-in ammo
conversion (~187 Ti) fires on 5 of 15 maps and essentially never on the other
10.  On dump maps CAD holds a median 28 Ti through r6-r13; on no-dump maps it
holds 204.

That gives a natural experiment the corpus can run for free:

  IF the suppression is a LOCKOUT (core damage latches the build branch), it
  should appear on BOTH map classes -- CAD's build branch does not know how much
  money it has.

  IF the suppression is POVERTY (CAD cannot afford to rebuild what it lost, and
  an opponent close enough to hit the core early is also eating the economy that
  would refill it), it should appear on dump maps and shrink or vanish on
  no-dump maps, where CAD has 204 Ti in hand.

Usage: moneycut.py <freeze_dir>
"""
from __future__ import annotations

import collections
import statistics
import sys

sys.path.insert(0, "docs/research/scripts/cad-lockout-2026-08-09")
from analyse import summarise, band_of, win, i, BANDS  # noqa: E402

DUMP_MAPS = {"antler", "eider", "heart", "moonrise", "nordkap"}


def main(d):
    games = summarise(d)
    P = sys.stdout.write
    P("# The decisive cut: is the suppression a lockout or poverty?\n\n")

    def klass(g):
        return "dump" if g["mapname"] in DUMP_MAPS else "nodump"

    # sanity: the dump classification actually predicts money
    P("## sanity: money by map class and damage band, r14-r40\n")
    P(f"{'class':8s} {'band':8s} {'n':>4s} {'median Ti':>10s}\n")
    for k in ("dump", "nodump"):
        for name, _lo, _hi in BANDS + [("never", None, None)]:
            fs = [f for f, g in games.items()
                  if klass(g) == k and band_of(g["first_dmg"]) == name
                  and g["n"] > 40]
            if not fs:
                continue
            med = [statistics.median(i(r, "cad_ti") for r in games[f]["rs"]
                                     if 14 <= i(r, "rnd") <= 40) for f in fs]
            P(f"{k:8s} {name:8s} {len(fs):>4d} {statistics.median(med):>10.0f}\n")

    P("\n## THE CUT: landmark build counts r14-r40, within each map class\n")
    for k in ("dump", "nodump"):
        P(f"\n### {k} maps "
          f"({'CAD broke after the r4 dump' if k == 'dump' else 'CAD holds ~200 Ti'})\n")
        P(f"{'band':8s} {'n':>4s} {'mean builds':>12s} {'median':>7s} "
          f"{'ZERO':>10s}\n")
        for name, _lo, _hi in BANDS + [("never", None, None)]:
            fs = [f for f, g in games.items()
                  if klass(g) == k and band_of(g["first_dmg"]) == name
                  and g["n"] > 40]
            if not fs:
                continue
            v = [win(games[f]["rs"], 14, 40, "cad_builds") for f in fs]
            z = sum(1 for x in v if x == 0)
            P(f"{name:8s} {len(fs):>4d} {statistics.mean(v):>12.1f} "
              f"{statistics.median(v):>7.1f} {f'{z}/{len(v)}':>10s}\n")

    P("\n## same cut, the damaged/undamaged landmark rather than bands\n")
    for k in ("dump", "nodump"):
        P(f"\n### {k} maps, window r14-r40\n")
        for label, pred in (
                ("damaged before r14",
                 lambda g: g["first_dmg"] is not None and g["first_dmg"] < 14),
                ("undamaged at r14",
                 lambda g: g["first_dmg"] is None or g["first_dmg"] >= 14)):
            fs = [f for f, g in games.items()
                  if klass(g) == k and pred(g) and g["n"] > 40]
            if not fs:
                continue
            v = [win(games[f]["rs"], 14, 40, "cad_builds") for f in fs]
            z = sum(1 for x in v if x == 0)
            P(f"  {label:20s} n={len(v):>3d}  mean={statistics.mean(v):5.1f}  "
              f"median={statistics.median(v):5.1f}  ZERO {z}/{len(v)} "
              f"({100.0*z/len(v):.0f}%)\n")

    P("\n## and the same for the ORIGINATING game's own map (nordkap)\n")
    fs = [f for f, g in games.items() if g["mapname"] == "nordkap"]
    P(f"nordkap games in the archive: n={len(fs)}\n")
    for f in sorted(fs, key=lambda f: (games[f]["first_dmg"] is None,
                                       games[f]["first_dmg"] or 0)):
        g = games[f]
        P(f"  {f[:8]} g{g['pop']['game']} v{g['pop']['cad_ver']:>3s} vs "
          f"{g['pop']['opp'][:16]:16s} first_dmg "
          f"{('r'+str(g['first_dmg'])) if g['first_dmg'] is not None else 'never':>6s}"
          f" rounds {g['n']:>4d} builds r14-40 "
          f"{win(g['rs'],14,40,'cad_builds'):>3d} builds after dmg "
          f"{win(g['rs'],g['first_dmg'] or 0,10**6,'cad_builds'):>4d} "
          f"coredied {int(g['cad_core_died'])}\n")


if __name__ == "__main__":
    main(sys.argv[1])
