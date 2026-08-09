#!/usr/bin/env python3
"""Every ladder match in the league, not just ours.

`fcode match list --team <id>` works for ANY team, paginated, on the cheap
channel. Until now every corpus in this repo was `--mine`, which means every
behavioural claim we have made carries the caveat "...against us". This removes
it: with the whole league's match table we can ask how the top tier performs
against the TOP TIER, which is a population we never play.

Per match (from the list payload alone, no `match info` needed):
    both team names + VERSIONS, scoreA/scoreB, winnerId, eloDeltaA/B,
    ratingABefore/ratingBBefore (the reconciled at-match field), createdAt.

That is enough for: per-pair game share, per-version performance, opponent ship
and ROLLBACK detection, and reaction-latency timing — all without a single
`match info` or replay download.

    .venv/bin/python tools/corpus/league_matches.py corpus/league_matches.tsv
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FC = str(ROOT / ".venv/bin/fcode")
MAX_PAGES = 40          # 4,000 matches per team; log if any team hits it


def fc(args):
    r = subprocess.run([FC] + args, cwd=ROOT, text=True, capture_output=True)
    return r.stdout


def teams():
    d = json.loads(fc(["ladder", "--limit", "200", "--json"]))
    rows = d if isinstance(d, list) else (d.get("teams") or d.get("rankings")
                                          or list(d.values())[0])
    return [(t["teamId"], t["teamName"], t["rating"], t["matchesPlayed"]) for t in rows]


COLS = ["id", "createdAt", "teamAName", "teamAVersion", "teamBName", "teamBVersion",
        "scoreA", "scoreB", "winnerId", "teamAId", "teamBId",
        "ratingABefore", "ratingBBefore", "eloDeltaA", "eloDeltaB"]


def main():
    out_path = Path(sys.argv[1])
    ts = teams()
    print(f"ladder: {len(ts)} teams", file=sys.stderr)
    seen: dict[str, dict] = {}
    capped = []
    t0 = time.time()
    for i, (tid, name, rating, played) in enumerate(ts):
        cursor, pages, got = None, 0, 0
        while pages < MAX_PAGES:
            args = ["match", "list", "--team", tid, "--type", "ladder",
                    "--json", "--limit", "100"]
            if cursor:
                args += ["--cursor", cursor]
            try:
                d = json.loads(fc(args))
            except Exception:
                break
            page = d["matches"] if isinstance(d, dict) else d
            if not page:
                break
            for m in page:
                seen.setdefault(m["id"], m)
            got += len(page)
            pages += 1
            cursor = d.get("next_cursor") if isinstance(d, dict) else None
            if not cursor:
                break
        if pages >= MAX_PAGES:
            capped.append((name, got, played))
        print(f"  [{i+1}/{len(ts)}] {name[:24]:<24} rating {rating:7.0f} "
              f"played {played:5} -> pulled {got:5}  (unique so far {len(seen)})",
              file=sys.stderr, flush=True)
    with out_path.open("w") as fh:
        fh.write("\t".join(COLS) + "\n")
        for m in seen.values():
            fh.write("\t".join(str(m.get(c, "")) for c in COLS) + "\n")
    print(f"\nWROTE {len(seen)} unique ladder matches in {time.time()-t0:.0f}s "
          f"-> {out_path}", file=sys.stderr)
    if capped:
        print(f"CAPPED at {MAX_PAGES} pages (incomplete history): {capped}",
              file=sys.stderr)


if __name__ == "__main__":
    main()
