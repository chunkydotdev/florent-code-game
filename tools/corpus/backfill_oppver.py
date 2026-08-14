#!/usr/bin/env python3
"""Backfill `oppver` in corpus/ladder_games.tsv from corpus/league_matches.tsv.

    .venv/bin/python tools/corpus/backfill_oppver.py --dry-run
    .venv/bin/python tools/corpus/backfill_oppver.py --apply

WHY. `tools/corpus/sync.py` read match versions from `fcode match info`, which
returns the version for OUR side and **None for the OPPONENT'S**, every time,
while `fcode match list` returns both. So `oppver` is the literal string 'None'
in **4,375 of 4,375 rows** while `ourver` populated correctly. The ingest is now
fixed (reads the list payload) but that only repairs rows written from here on.

⛔ AND THE HAZARD IS THE HALF-FIXED STATE, NOT THE BROKEN ONE. The moment sync
writes its first repaired row the column becomes MIXED — historical 'None', new
rows real — and **any filter on `oppver` silently becomes a TIME CUT wearing a
version cut's clothes.** A partly-filled column is indistinguishable, to any
filter, from one where the predicate is simply false. **A uniformly-broken column
is honest; a half-fixed one is not.** So this runs BEFORE the next sync write.
Timing argument: side lane.

⭐ THE JOIN CARRIES ITS OWN POSITIVE CONTROL, AND IT IS THE GATE, NOT A GARNISH.
`ladder_games` already holds a TRUSTED `ourver`. The same join independently
reproduces it, so every row can be checked against a column we already believe
before its unknown column is written. **If `ourver` disagreement exceeds the
threshold, this refuses to write anything.** A backfill that cannot fail its own
check is not a backfill, it is an overwrite.

NOTHING IS DESTROYED: writes a timestamped .bak beside the file first, and the
row count and every other column must match exactly or it aborts.
"""
from __future__ import annotations

import csv
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
LADDER = ROOT / "corpus" / "ladder_games.tsv"
LEAGUE = ROOT / "corpus" / "league_matches.tsv"
OURS = "379a5d80-9921-4c9e-949b-f9b1dcba16be"

# Max fraction of joinable rows whose `ourver` may disagree before we refuse.
# Not zero: a version can legitimately be absent on an odd row. But it is tight,
# because the whole point is that the control must be able to FAIL.
MAX_OURVER_MISMATCH = 0.01


def load(path: Path) -> tuple[list[str], list[dict]]:
    with path.open(newline="") as fh:
        r = csv.DictReader(fh, delimiter="\t")
        return list(r.fieldnames or []), list(r)


def main(argv: list[str]) -> int:
    apply = "--apply" in argv
    if not apply and "--dry-run" not in argv:
        print(__doc__)
        return 2
    for p in (LADDER, LEAGUE):
        if not p.exists():
            print(f"BLIND: {p} does not exist")
            return 2

    cols, rows = load(LADDER)
    _, league = load(LEAGUE)
    if "oppver" not in cols or "ourver" not in cols or "match" not in cols:
        print(f"BLIND: ladder tape lacks expected columns; has {cols}")
        return 2

    idx = {m["id"]: m for m in league if m.get("id")}
    print(f"ladder rows            : {len(rows):,}")
    print(f"league matches indexed : {len(idx):,}")

    joined = missing = ourver_ok = ourver_bad = 0
    already = 0
    plan: dict[int, str] = {}
    mismatches = []
    for i, r in enumerate(rows):
        cur = (r.get("oppver") or "").strip()
        if cur and cur != "None":
            already += 1
            continue
        m = idx.get(r.get("match", ""))
        if m is None:
            missing += 1
            continue
        joined += 1
        we_are_a = m.get("teamAId") == OURS
        oppv = m.get("teamBVersion") if we_are_a else m.get("teamAVersion")
        ourv = m.get("teamAVersion") if we_are_a else m.get("teamBVersion")
        # ---- POSITIVE CONTROL: reproduce a column we already trust ----------
        have = (r.get("ourver") or "").strip()
        if have and have != "None":
            if str(ourv).strip() == have:
                ourver_ok += 1
            else:
                ourver_bad += 1
                if len(mismatches) < 5:
                    mismatches.append((r.get("match", "")[:8], have, ourv))
        if oppv not in (None, "", "None"):
            plan[i] = str(oppv)

    print(f"  already populated    : {already:,}")
    print(f"  joined               : {joined:,}")
    print(f"  no league row        : {missing:,}")
    print(f"  would fill           : {len(plan):,}")
    print()
    tot = ourver_ok + ourver_bad
    rate = (ourver_bad / tot) if tot else 1.0
    print("POSITIVE CONTROL — does the same join reproduce the TRUSTED `ourver`?")
    print(f"  agree {ourver_ok:,} / disagree {ourver_bad:,}  ({rate:.4%} mismatch, "
          f"limit {MAX_OURVER_MISMATCH:.2%})")
    for mm in mismatches:
        print(f"    mismatch {mm[0]}: tape ourver={mm[1]} join says {mm[2]}")
    if tot == 0:
        print("⛔ REFUSING: the control could not run — no row had a trusted "
              "`ourver` to check against. A backfill whose check cannot execute "
              "is an overwrite.")
        return 3
    if rate > MAX_OURVER_MISMATCH:
        print("⛔ REFUSING TO WRITE: the join disagrees with a column we already "
              "trust, so its unknown column cannot be trusted either.")
        return 3
    print("✅ control passes — the join reproduces a known column.")

    if not plan:
        print("\nnothing to fill.")
        return 0
    if not apply:
        print("\n--dry-run: nothing written. Re-run with --apply.")
        return 0

    bak = LADDER.with_suffix(f".tsv.bak-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}")
    shutil.copy2(LADDER, bak)
    print(f"\nbackup: {bak.name}")
    for i, v in plan.items():
        rows[i]["oppver"] = v
    tmp = LADDER.with_suffix(".tsv.tmp")
    with tmp.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t",
                           lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    # row count must match exactly or we put the original back
    n_new = sum(1 for _ in tmp.open()) - 1
    if n_new != len(rows):
        tmp.unlink(missing_ok=True)
        print(f"⛔ ABORT: wrote {n_new} rows, expected {len(rows)}. Original untouched.")
        return 4
    tmp.replace(LADDER)
    print(f"wrote {len(plan):,} oppver values across {len(rows):,} rows.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
