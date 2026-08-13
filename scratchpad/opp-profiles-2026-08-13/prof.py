#!/usr/bin/env python3
"""Generic opponent profile over the tri-arm leg (2026-08-13).

Usage: prof.py <OpponentName>
Reads corpus/meta_join.tsv to find that opponent's games among the tri-arm
match ids, then dumps a per-game report (same shape as the team-lazy profile
script, docs/research/lazy-profile-scripts-2026-08-13/lazy_profile.py, which
this is a generalisation of) plus aggregates.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "docs/research/lazy-profile-scripts-2026-08-13"))
sys.path.insert(0, str(ROOT / "tools"))
import lazy_profile as LP  # noqa: E402

TRIARM = [l.split('"')[3] for l in
          (ROOT / "scratchpad/triarm_fires.tsv").read_text().splitlines()
          if "ACCEPT" in l]


def games_for(opp: str):
    """-> list of (replay_path, opp_team_index, our_version, our_won, match)"""
    out = []
    with open(ROOT / "corpus/meta_join.tsv") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row["match"] not in TRIARM:
                continue
            names = (row["teamAName"], row["teamBName"])
            if opp not in names:
                continue
            # us_side 'a' -> our team index 0
            us = 0 if row["us_side"] == "a" else 1
            opp_i = 1 - us
            ourver = row["teamAVersion"] if us == 0 else row["teamBVersion"]
            oppver = row["teamBVersion"] if us == 0 else row["teamAVersion"]
            out.append((ROOT / "replay_archive" / row["file"], opp_i, ourver,
                        oppver, row["our_won"] == "1", row["match"], row["game"]))
    out.sort(key=lambda r: (r[5], int(r[6])))
    return out


def main():
    opp = sys.argv[1]
    gs = games_for(opp)
    print(f"### {opp}: {len(gs)} games, "
          f"oppver={sorted({g[3] for g in gs})}, "
          f"ourver={sorted({g[2] for g in gs})}, "
          f"we won {sum(1 for g in gs if g[4])}/{len(gs)}")
    for path, opp_i, ourver, oppver, won, match, gm in gs:
        LP.SEAT[path.name] = opp_i
        print(f"\n===== match {match[:8]} g{gm} ourver=v{ourver} "
              f"oppver=v{oppver} our_won={won}")
        LP.report(LP.parse(path))


if __name__ == "__main__":
    main()
