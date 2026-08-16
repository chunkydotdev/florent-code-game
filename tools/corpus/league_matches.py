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

# ---- `--help` CONTRACT (enforced by tests/test_instruments.py) --------------
# Side-effect-free, prints this module's docstring, exits 0.
#
# ⛔ WHY THIS FILE NEEDED IT (measured 2026-08-16, s47). `tools/corpus/` sat
# OUTSIDE the help-contract sweep, which globbed `tools/*.py` only. Probed:
# 11 of 18 corpus tools violated the contract, and three of the failures are
# the dangerous classes the sweep exists to catch —
#   * `unrated_games.py --help` REWROTE corpus/unrated_games.tsv (1.1 MB)
#   * `ladder_meta.py`, `league_maps.py`, `league_matches.py`, `meta_attrib.py`
#     --help went to the NETWORK and ran until killed at 20 s
#   * `replay_autopsy.py --help` raised TypeError out of replay_census.fields()
# and the rest printed verdict-shaped text in this repo's own vocabulary
# ("no *.replay26 under --help", "sides loaded: 0 (from 0 matches) — --help").
#
# ⛔ GATED ON `__main__`: several of these modules are IMPORTED by build_corpus /
# keeper. Ungated, this would fire during that import and make the PARENT exit 0
# mid-run while printing the CHILD's docstring.
# ⛔ SELF-CONTAINED `import sys`: the guard must not depend on what the host file
# happens to import, or on the order its imports appear in.
# ⛔ MUST SIT AFTER `from __future__ import ...`, which the language requires to
# be the first statement after the docstring.
if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__ + "  (no module docstring)"))
        raise SystemExit(0)

import csv
import fcntl
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


def update(out_path: Path) -> int:
    """INCREMENTAL refresh: pull only matches not already in the file.

    WHY THIS EXISTS (s28, 2026-08-10, on Magnus's instruction "fix that with a
    script that keeps it updated"). The full rebuild below walks 116 teams x up
    to 40 pages -- thousands of calls -- so it was only ever run BY HAND. The
    result: `league_matches.tsv` sat **20.9 hours stale** and `league_games.tsv`
    **33.3 hours** while `keeper.py` ran healthily every 10 minutes and logged a
    fresh `meta_join` each cycle. The replay half of the corpus was minutes old;
    the match-metadata half had not moved since the previous evening, **and
    nothing said so.**

    It cost real work before anyone noticed: an opponent record verified at 31
    matches when the platform had 32, a ratings table quoted at "~22h stale",
    and a `diverge` cell reading 5 in the corpus against 13 on the platform --
    the two sources disagreeing about the SAME opponent by 8 matches, which is
    what finally exposed it.

    Incremental mode stops paging a team as soon as it is well into known
    territory, which turns an hours-long rebuild into a cheap top-up that the
    keeper can run unattended.
    """
    known: set[str] = set()
    if out_path.exists():
        with out_path.open() as fh:
            rows = csv.DictReader(fh, delimiter="\t")
            known = {r["id"] for r in rows if r.get("id")}
    fresh: dict[str, dict] = {}
    for tid, name, _rating, _played in teams():
        cursor, pages, seen_known = None, 0, 0
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
                if m["id"] in known:
                    seen_known += 1
                else:
                    fresh.setdefault(m["id"], m)
            pages += 1
            cursor = d.get("next_cursor") if isinstance(d, dict) else None
            # STOP EARLY once we are into already-known history. The list is
            # newest-first, so a page dominated by known ids means the rest of
            # this team's history is already banked.
            if seen_known >= 60 or not cursor:
                break
    if not fresh:
        print("league_matches: +0 new (up to date)")
        return 0

    # 2026-08-14 119-DUPLICATE INCIDENT: this function used to append `fresh`
    # straight off the `known` set read at the top of this call, with no
    # lock. Two processes (keeper + a lane boot sync, both re-armed by the
    # same 18:56:33Z reboot) read `known` before either had written, both
    # classified the SAME rows as fresh, and both appended them -- 119 ids
    # landed twice, byte-identical, in two contiguous tail blocks (41 + 78
    # rows) matching the two writers' own batch sizes. Caught by TRAP 9 in
    # tools/corpus_sanity.py. Fix: take an exclusive flock on a sibling
    # `.lock` file, RE-READ `known` under the lock (a concurrent writer may
    # have landed between our first read and now), and drop anything that is
    # no longer actually fresh before writing.
    # Spec: docs/research/SPEC-corpus-sanity-trap9-duplicate-keys-2026-08-14.md
    lock_path = out_path.with_name(out_path.name + ".lock")
    lock_path.touch(exist_ok=True)
    with lock_path.open("r+") as lockfh:
        fcntl.flock(lockfh, fcntl.LOCK_EX)
        try:
            known_now: set[str] = set()
            if out_path.exists():
                with out_path.open() as fh:
                    rows = csv.DictReader(fh, delimiter="\t")
                    known_now = {r["id"] for r in rows if r.get("id")}
            fresh_now = {mid: m for mid, m in fresh.items() if mid not in known_now}
            if not fresh_now:
                print("league_matches: +0 new (another writer landed the batch first)")
                return 0
            write_header = not out_path.exists()
            with out_path.open("a") as fh:
                if write_header:
                    fh.write("\t".join(COLS) + "\n")
                for m in fresh_now.values():
                    fh.write("\t".join(str(m.get(c, "")) for c in COLS) + "\n")
            newest = max((m.get("createdAt") or "") for m in fresh_now.values())
            print(f"league_matches: +{len(fresh_now)} new (newest {newest[:19]})")
            return len(fresh_now)
        finally:
            fcntl.flock(lockfh, fcntl.LOCK_UN)


def main():
    if sys.argv[1] == "--update":
        raise SystemExit(0 if update(Path(sys.argv[2])) >= 0 else 1)
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
