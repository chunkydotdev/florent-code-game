#!/usr/bin/env python3
"""Build the CtrlAltDefeat game population from archived match metadata.

`join.tsv` only attributes OUR ladder games (85 CAD games).  But every archived
match carries a sibling `<id>.meta.json` with teamAName/teamBName and
teamAVersion/teamBVersion, which gives BOTH the seat and the version — including
for 115 CAD-vs-third-party games that `join.tsv` cannot see at all.  Those are
the uncontaminated population for a "does CAD lock out" test, because our own
bot is not in them.

SEAT VALIDATION (run before trusting this): for the 85 games that appear in both
sources, meta's teamA==OpenSverige must agree with join.tsv's `our_team` == 0.
Measured 2026-08-09: 85/85 agree, 0 disagree.  So replay team 0 == meta teamA.

VERSION: this is the working version source.  join.tsv.oppver,
ladder_games.tsv.oppver and league_games.tsv.verA/verB are all the literal
string "None" (dead columns) and cannot stratify anything.

Emits: file, match, game, cad_team, cad_ver, opp, opp_ver, triggered, vs_us
"""
from __future__ import annotations

import glob
import json
import os
import sys

CAD = "CtrlAltDefeat"
US = "OpenSverige"


def main(archive: str, out_path: str) -> None:
    rows = []
    for p in glob.glob(os.path.join(archive, "*.meta.json")):
        try:
            d = json.load(open(p))
        except Exception:                                    # noqa: BLE001
            continue
        a, b = d.get("teamAName"), d.get("teamBName")
        if CAD not in (a, b):
            continue
        cad_team = 0 if a == CAD else 1
        cad_ver = d.get("teamAVersion") if cad_team == 0 else d.get("teamBVersion")
        opp = b if cad_team == 0 else a
        opp_ver = d.get("teamBVersion") if cad_team == 0 else d.get("teamAVersion")
        mid = d["id"]
        for g in sorted(glob.glob(os.path.join(archive, f"{mid}_game_*.replay26"))):
            fn = os.path.basename(g)
            gi = fn.split("_game_")[1].split(".")[0]
            rows.append([fn, mid, gi, cad_team, cad_ver, opp, opp_ver,
                         d.get("triggeredBy"), int(opp == US)])
    rows.sort()
    with open(out_path, "w") as f:
        f.write("file\tmatch\tgame\tcad_team\tcad_ver\topp\topp_ver\ttriggered\tvs_us\n")
        for r in rows:
            f.write("\t".join(str(x) for x in r) + "\n")
    print(f"{len(rows)} CAD game files from "
          f"{len({r[1] for r in rows})} matches", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
