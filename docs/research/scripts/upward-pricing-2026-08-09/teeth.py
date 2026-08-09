#!/usr/bin/env python3
"""TEETH TEST for the upward-pricing pipeline.

RULE (adopted 2026-08-09): prove teeth PER GUARD, not per tool.  A check that
reports 100% proves nothing until it has been shown it CAN report less.

The pipeline under test is: replay team INDEX (0/1, all the decoders know)
  -> meta_join seat (teamA = index 0, teamB = index 1)
  -> team NAME and at-match ratingABefore/ratingBBefore.

The corruption: a SEAT-FLIPPED attribution -- swap which meta_join column
supplies the focal side.  Every number below must collapse.

Three guards, because they partition differently:

  G1  OUTCOME.  The side my decoder says lost its core must be the side the
      PLATFORM metadata says lost the game.  Decoder output vs an entirely
      independent source.  (Only games that ended in a core kill are testable.)
  G2  IDENTITY.  OpenSverige's collar occupancy is 67.2% and the field's is
      ~50%; under a flip "our" rows become our opponents' and must regress.
  G3  RATING GRADIENT.  Weaker victims die earlier.  The kill-round gradient
      across victim rating bands must flatten/invert under a flip.

    python teeth.py <freezedir>
"""
from __future__ import annotations
import csv, statistics, sys


def f(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def main(argv):
    fz = argv[0]
    M = {r["file"]: r for r in csv.DictReader(open(f"{fz}/meta_join.tsv"), delimiter="\t")}
    games = list(csv.DictReader(open(f"{fz}/collar/collar_games.tsv"), delimiter="\t"))
    # index rows by (file, side); side US == replay index 0
    by = {}
    for g in games:
        by.setdefault(g["file"], {})[g["side"]] = g

    for flip in (False, True):
        tag = "FLIPPED (corrupted)" if flip else "TRUE attribution"
        # seat -> meta column suffix
        seat = {"US": "B", "THEM": "A"} if flip else {"US": "A", "THEM": "B"}
        side_letter = {"US": "b", "THEM": "a"} if flip else {"US": "a", "THEM": "b"}

        # ---- G1 outcome ------------------------------------------------
        ok = tot = 0
        for fn, sides in by.items():
            m = M.get(fn)
            if not m or len(sides) != 2:
                continue
            dead = [s for s in ("US", "THEM") if int(sides[s]["core_death_own"]) >= 0]
            if len(dead) != 1:
                continue                      # no kill, or (impossible) both
            tot += 1
            loser_side = side_letter[dead[0]]
            if m["game_winner_side"] != loser_side:
                ok += 1                       # winner is the OTHER side: agrees
        print(f"\n=== {tag} ===")
        print(f"G1 outcome: {ok}/{tot} core-kill games agree with platform winner "
              f"= {100*ok/tot:.4f}%")

        # ---- G2 identity ------------------------------------------------
        occ = {}
        rounds_seen = {}
        # collar occupancy needs the round table; use a cheap per-game proxy that
        # the round table backs: recomputed below in analyse.py.  Here use
        # tot_heal_core / builder_rounds and core heals per 100 rounds, which is
        # the same identity question and is available per game.
        for fn, sides in by.items():
            m = M.get(fn)
            if not m or len(sides) != 2:
                continue
            for s in ("US", "THEM"):
                nm = m[f"team{seat[s]}Name"]
                g = sides[s]
                occ[nm] = occ.get(nm, 0) + int(g["tot_heal_core"])
                rounds_seen[nm] = rounds_seen.get(nm, 0) + int(g["nr"])
        for nm in ("OpenSverige", "CtrlAltDefeat", "sporks", "Pantheon"):
            if nm in occ and rounds_seen[nm]:
                print(f"G2 identity: {nm:16s} core-heals/100r = "
                      f"{100*occ[nm]/rounds_seen[nm]:6.2f}  (rounds {rounds_seen[nm]})")

        # ---- G3 rating gradient -----------------------------------------
        bands = {}
        for fn, sides in by.items():
            m = M.get(fn)
            if not m or len(sides) != 2:
                continue
            if m["us_side"] != "none" or m["related"] != "none":
                continue
            for s in ("US", "THEM"):
                g = sides[s]
                d = int(g["core_death_own"])
                if d < 0:
                    continue
                r = f(m[f"rating{seat[s]}Before"])
                if r is None:
                    continue
                b = ("<1400" if r < 1400 else "1400-1549" if r < 1550 else
                     "1550-1699" if r < 1700 else ">=1700")
                bands.setdefault(b, []).append(d)
        print("G3 gradient (median kill round by VICTIM band, third-party):")
        for b in ("<1400", "1400-1549", "1550-1699", ">=1700"):
            v = bands.get(b, [])
            if v:
                print(f"     {b:10s} n={len(v):5d}  median r{statistics.median(v):.0f}")


if __name__ == "__main__":
    main(sys.argv[1:])
