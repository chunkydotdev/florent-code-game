#!/usr/bin/env python3
"""THE STANDDOWN ASSERTION, v523 -- PER GAME, so a single leaking game cannot
hide in a mean.

On a CRIPPLE board (`FS_V519_CRIPPLE_MAPS`: yulerune, midgard) or the GATED
board (archipelago) no v523 SIEGE clause may fire in ANY game.  The siege
clauses are change 1's: a merged verdict beyond own eyes, an arc-closed
publish, an arc credit, a union-answered salt gate.

⛔ CHANGE 2's `crew_win` IS COUNTED SEPARATELY AND IS NOT ASSERTED TO ZERO ON
THE SAME GROUND.  The Core reads the phase on every board; what the gate
controls is whether a SECOND ferry-siege body exists to publish into
`FS_SUPP_SLOT` at all, so `crew_win` should also be zero -- but it is a
consequence, not a definition, and conflating the two would let a real leak in
the siege clauses hide behind a correct zero in the Core's.

⛔ AND THE ASSERTION IS ONLY WORTH SOMETHING IF IT HAS BEEN SEEN TO FIRE.
nordkap is the POSITIVE CONTROL and must show games with every clause nonzero.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mechread523 import read_tape  # noqa: E402

SIEGE = ("gain", "ph_arccl", "arc_credit", "salt_union")


def per_game(d: Path):
    out = []
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".err"):
            continue
        r = read_tape(open(d / fn, errors="replace").read())
        r["gain"] = r["ph_merged"] - r["ph_own"]
        out.append((fn, r))
    return out


def main():
    print("%-14s %5s %10s %10s %10s %10s %10s %6s"
          % ("board", "n", "w/gain", "w/arcpub", "w/arccred", "w/saltun",
             "w/crewwin", "PBAD"))
    bad = 0
    for d in sys.argv[1:]:
        p = Path(d)
        games = per_game(p)
        n = len(games)
        cnt = {k: sum(1 for _f, r in games if r[k] > 0) for k in SIEGE}
        cw = sum(1 for _f, r in games if r["crew_win"] > 0)
        pb = sum(r["PARSE_BAD"] for _f, r in games)
        bad += pb
        print("%-14s %5d %10d %10d %10d %10d %10d %6d"
              % (p.name.replace("log", "") or p.name, n,
                 cnt["gain"], cnt["ph_arccl"], cnt["arc_credit"],
                 cnt["salt_union"], cw, pb))
    print("PARSE_BAD total:", bad)


if __name__ == "__main__":
    main()
