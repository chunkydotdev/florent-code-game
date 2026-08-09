#!/usr/bin/env python3
"""Per-GAME detail for a selected slice of the league match table.

`league_matches.py` gets 27k matches from the cheap list channel, but the list
payload has no per-game rows. This adds `match info` for a chosen subset —
one call per match — to get mapName / winCondition / turnsPlayed / winnerSide /
replayS3Key per game.

`turnsPlayed` on a `core_destroyed` game IS the kill round, which is what the
hazard tables are built from. Running this over TOP-vs-TOP matches answers the
question our own corpus structurally cannot: is the r150 conversion wall a fact
about us, or a fact about the game?

    # every match between teams averaging >=1800 at-match rating
    .venv/bin/python tools/corpus/league_games.py corpus/league_games.tsv --min-rating 1800

    # or an explicit team
    .venv/bin/python tools/corpus/league_games.py out.tsv --team sporks
"""
from __future__ import annotations

import argparse
import csv
import json
import statistics
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FC = str(ROOT / ".venv/bin/fcode")
SRC = ROOT / "corpus/league_matches.tsv"

COLS = ["match", "createdAt", "teamA", "verA", "teamB", "verB",
        "ratA", "ratB", "game", "map", "winnerSide", "winnerIsA",
        "cond", "turns", "s3"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--min-rating", type=float, default=None,
                    help="both teams' mean at-match rating must be >= this")
    ap.add_argument("--team", default=None, help="matches involving this team name")
    ap.add_argument("--limit", type=int, default=2000)
    a = ap.parse_args()

    rows = list(csv.DictReader(SRC.open(), delimiter="\t"))
    rat: dict[str, list[float]] = {}
    for r in rows:
        for s in "AB":
            try:
                rat.setdefault(r[f"team{s}Name"], []).append(float(r[f"rating{s}Before"]))
            except (ValueError, KeyError):
                pass
    mean = {k: statistics.fmean(v) for k, v in rat.items() if v}

    sel = []
    for r in rows:
        A, B = r["teamAName"], r["teamBName"]
        if a.min_rating is not None:
            if mean.get(A, 0) < a.min_rating or mean.get(B, 0) < a.min_rating:
                continue
        if a.team and a.team not in (A, B):
            continue
        sel.append(r)
    sel.sort(key=lambda r: r["createdAt"], reverse=True)
    sel = sel[:a.limit]
    print(f"selected {len(sel)} matches -> {len(sel)} `match info` calls", file=sys.stderr)

    t0 = time.time()
    n = 0
    with Path(a.out).open("w") as fh:
        fh.write("\t".join(COLS) + "\n")
        for i, m in enumerate(sel):
            p = subprocess.run([FC, "match", "info", m["id"], "--json"],
                               cwd=ROOT, text=True, capture_output=True)
            try:
                d = json.loads(p.stdout)
            except Exception:
                continue
            mm = d["match"]
            aid = mm["teamAId"]
            for gi, g in enumerate(d.get("games", []), 1):
                fh.write("\t".join(str(x) for x in [
                    m["id"], mm.get("createdAt", ""), mm["teamAName"],
                    mm.get("teamAVersion", ""), mm["teamBName"], mm.get("teamBVersion", ""),
                    mm.get("ratingABefore", ""), mm.get("ratingBBefore", ""),
                    gi, g.get("mapName", ""), g.get("winnerSide", ""),
                    int(g.get("winnerId") == aid), g.get("winCondition", ""),
                    g.get("turnsPlayed", 0), g.get("replayS3Key", "") or "",
                ]) + "\n")
                n += 1
            if (i + 1) % 100 == 0:
                print(f"  ...{i+1}/{len(sel)} matches, {n} games, "
                      f"{time.time()-t0:.0f}s", file=sys.stderr, flush=True)
    print(f"WROTE {n} games from {len(sel)} matches in {time.time()-t0:.0f}s",
          file=sys.stderr)


if __name__ == "__main__":
    main()
