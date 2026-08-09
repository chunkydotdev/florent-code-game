#!/usr/bin/env python3
"""Per-team Elo TRAJECTORY from corpus/league_matches.tsv.

The league table already carries `ratingABefore`/`ratingBBefore` per match --
the at-match rating that reconciles to eleven decimals against `eloDelta`
(docs/fcode-cli.md trap 2: `teamARating` is a LIVE JOIN and must never be used).
So the whole field's rating HISTORY is recoverable from rows we already have;
we do not only have the latest state.

  .venv/bin/python elo_traj.py corpus/league_matches.tsv [--since ISO] [--top N]

Emits: current standings, movement over the window, and the sharpest movers.
"""
from __future__ import annotations
import csv, sys, collections, datetime


def load(path):
    per = collections.defaultdict(list)          # team -> [(ts, before, delta)]
    with open(path) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            ts = r.get("createdAt") or ""
            if not ts:
                continue
            try:
                da = float(r["eloDeltaA"]) if r.get("eloDeltaA") not in ("", "None", None) else None
                ra = float(r["ratingABefore"]); rb = float(r["ratingBBefore"])
            except (ValueError, KeyError, TypeError):
                continue
            db = -da if da is not None else None
            per[r["teamAName"]].append((ts, ra, da))
            per[r["teamBName"]].append((ts, rb, db))
    for t in per:
        per[t].sort(key=lambda x: x[0])
    return per


def rating_at(rows, cutoff):
    """Last known rating at or before cutoff (before+delta of the last match)."""
    best = None
    for ts, before, delta in rows:
        if ts <= cutoff:
            best = before + (delta or 0.0)
        else:
            break
    return best


def main(argv):
    path = argv[0]
    since = None
    top = 15
    for i, a in enumerate(argv):
        if a == "--since":
            since = argv[i + 1]
        if a == "--top":
            top = int(argv[i + 1])
    per = load(path)
    allts = sorted({ts for rows in per.values() for ts, _, _ in rows})
    newest, oldest = allts[-1], allts[0]
    if since is None:
        since = newest[:10] + "T00:00:00Z"
    print(f"teams {len(per)}  matches-rows {sum(len(v) for v in per.values())}")
    print(f"window  oldest {oldest}  newest {newest}")
    print(f"movement measured from {since}\n")

    rowsout = []
    for team, rows in per.items():
        cur = rows[-1][1] + (rows[-1][2] or 0.0)
        base = rating_at(rows, since)
        played = sum(1 for ts, _, _ in rows if ts > since)
        rowsout.append((team, cur, (cur - base) if base is not None else None, played, len(rows)))
    rowsout.sort(key=lambda x: -x[1])

    print(f"{'#':>3} {'team':<32}{'Elo now':>9}{'Δ window':>10}{'games':>7}{'total':>7}")
    for i, (t, cur, d, p, n) in enumerate(rowsout[:top], 1):
        ds = f"{d:+.1f}" if d is not None else "   n/a"
        print(f"{i:>3} {t:<32}{cur:9.1f}{ds:>10}{p:>7}{n:>7}")

    moved = [r for r in rowsout if r[2] is not None and r[3] > 0]
    moved.sort(key=lambda x: x[2])
    print(f"\nSHARPEST FALLS in window (n={len(moved)} teams played):")
    for t, cur, d, p, n in moved[:8]:
        print(f"   {t:<32}{cur:9.1f}  {d:+8.1f} over {p} games")
    print("\nSHARPEST CLIMBS in window:")
    for t, cur, d, p, n in moved[-8:][::-1]:
        print(f"   {t:<32}{cur:9.1f}  {d:+8.1f} over {p} games")


if __name__ == "__main__":
    main(sys.argv[1:])
