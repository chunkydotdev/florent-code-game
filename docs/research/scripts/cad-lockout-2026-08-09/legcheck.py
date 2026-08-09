#!/usr/bin/env python3
"""What the leg actually rests on: does early core damage convert into a kill?

The autopsy's pre-registrable prediction is not really about build counts.  It
is: "first core shot <= r13 -> CAD executes zero build actions thereafter, core
kill ~r70-85 even sentinel-only."  The build half is tested elsewhere in this
directory.  This is the outcome half, which is the half a leg is fired on.

Usage: legcheck.py <freeze_dir>
"""
from __future__ import annotations

import statistics
import sys

sys.path.insert(0, "docs/research/scripts/cad-lockout-2026-08-09")
from analyse import summarise, band_of, win, i, BANDS  # noqa: E402


def main(d):
    games = summarise(d)
    P = sys.stdout.write
    P("# Does early core damage convert into a CAD core kill?\n\n")

    for label, sel in (("all opponents", lambda g: True),
                       ("vs us only", lambda g: g["pop"]["vs_us"] == "1"),
                       ("vs third parties", lambda g: g["pop"]["vs_us"] == "0")):
        P(f"\n## {label}\n")
        P(f"{'band':8s} {'n':>4s} {'CAD core died':>14s} {'rate':>6s} "
          f"{'median kill round':>18s} {'kill by r85':>12s}\n")
        for name, _lo, _hi in BANDS + [("never", None, None)]:
            fs = [f for f, g in games.items()
                  if band_of(g["first_dmg"]) == name and sel(g)]
            if not fs:
                continue
            died = [f for f in fs if games[f]["cad_core_died"]]
            kr = [games[f]["n"] - 1 for f in died]
            fast = sum(1 for x in kr if x <= 85)
            P(f"{name:8s} {len(fs):>4d} {len(died):>14d} "
              f"{100.0*len(died)/len(fs):>5.0f}% "
              f"{(statistics.median(kr) if kr else float('nan')):>18.0f} "
              f"{fast:>12d}\n")

    P("\n## The autopsy's exact prediction, scored on the population\n")
    P("'first core damage <= r13' -> (a) zero builds after, (b) kill by ~r70-85\n\n")
    fs = [f for f, g in games.items() if band_of(g["first_dmg"]) == "<=r13"]
    zero_after = sum(1 for f in fs
                     if win(games[f]["rs"], games[f]["first_dmg"], 10 ** 6,
                            "cad_builds") == 0)
    killed85 = sum(1 for f in fs
                   if games[f]["cad_core_died"] and games[f]["n"] - 1 <= 85)
    killed = sum(1 for f in fs if games[f]["cad_core_died"])
    both = sum(1 for f in fs
               if games[f]["cad_core_died"] and games[f]["n"] - 1 <= 85
               and win(games[f]["rs"], games[f]["first_dmg"], 10 ** 6,
                       "cad_builds") == 0)
    P(f"  trigger cell n = {len(fs)}\n")
    P(f"  (a) zero builds after first damage: {zero_after}/{len(fs)}\n")
    P(f"  (b) CAD core killed at all:          {killed}/{len(fs)}\n")
    P(f"  (b) CAD core killed by r85:          {killed85}/{len(fs)}\n")
    P(f"  both (a) and (b):                    {both}/{len(fs)}\n")

    P("\n## distribution of post-damage build counts in the trigger cell\n")
    v = sorted(win(games[f]["rs"], games[f]["first_dmg"], 10 ** 6, "cad_builds")
               for f in fs)
    P(f"  min {v[0]}  p25 {v[len(v)//4]}  median {statistics.median(v):.0f}  "
      f"p75 {v[3*len(v)//4]}  max {v[-1]}\n")
    P(f"  games with 0: {v.count(0)}   with <=2: {sum(1 for x in v if x <= 2)}"
      f"   with >=10: {sum(1 for x in v if x >= 10)}\n")


if __name__ == "__main__":
    main(sys.argv[1])
