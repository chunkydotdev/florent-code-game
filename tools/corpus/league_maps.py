#!/usr/bin/env python3
"""Per-GAME map surface for a NAMED opponent set, era-bounded, league-wide.

WHY THIS EXISTS. `league_matches.tsv` has 44,691 matches and no map column.
`meta_join.tsv` (the replay-derived surface) covers only the ~3,293 matches
that have an archived replay locally — that's OUR games, plus whatever
opponents happened to face us. Neither answers "which maps is opponent X weak
on" for a team we haven't played. `fcode match info <id>` returns a per-game
table (map, winner, condition, turns) for ANY match on the free metadata
channel — this is `league_games.py`'s trick, narrowed to a fixed named-team
roster and a fixed recent era instead of a rating floor, and made resumable.

SCOPE IS DELIBERATELY NARROW. Only matches involving a fixed 16-team roster,
`createdAt >= 2026-08-12`. An all-time pull for the same teams is ~8x more
matches and describes a pool of opponent versions that no longer exists — this
project made era-pooling mistakes three times in one day (2026-08-13) before
this rule got written down. Do not widen the window without a new reason
written down next to the widening.

RESUMABLE BY CONSTRUCTION -- FOR INTERRUPTION, NOT FOR A CODE FIX. Output is
appended to, never rewritten, and a sibling `.done` ledger records match ids
that produced a WRITTEN row. A match is only added to the ledger once its
rows are flushed to disk, so a kill mid-run reprocesses at most the one match
in flight. Matches skipped for `status != complete` or a transient
parse/rate-limit failure are NOT added to the ledger -- they're retried on
the next invocation.
⛔ THE LEDGER CARRIES NO VERSION TAG FOR THE CODE THAT PRODUCED IT. If you
change what a row MEANS -- which field a column is sourced from, a new dedup
rule, anything semantic -- an old ledger will happily tell the fixed code
"already done" about rows that are now wrong under the new logic, and it will
never re-fetch them. Two real incidents, 2026-08-14, same session: (1) a
version-sourcing bug (below) shipped `None` into every version cell across a
full clean-looking run; (2) `load_scope()` didn't dedupe against
`league_matches.tsv`'s own duplicate ids (41 of them league-wide) and doubled
9 matches' rows. Both times the correct fix was `rm league_maps.tsv
league_maps.done` and a full clean rerun -- NOT trusting the ledger through
the fix. Do the same: after any change to row semantics, wipe both files.

⛔ EXIT CODE FROM `fcode` IS NOT A HEALTH SIGNAL ON THIS PLATFORM (measured:
exits 0 while printing an error body, exits 1 on an unrelated failure). This
gates on the presence of `d["games"]` with a non-empty `mapName` per game --
the load-bearing field -- never on the subprocess return code.

    .venv/bin/python tools/corpus/league_maps.py corpus/league_maps.tsv
"""
from __future__ import annotations

import csv
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FC = str(ROOT / ".venv/bin/fcode")
SRC = ROOT / "corpus/league_matches.tsv"

TEAMS = {
    "Pantheon", "team lazy", "0033", "Erebus", "farming_200s", "LingLing40",
    "lingling_40h", "HTTP 418", "diverge", "The Bisons", "Big O", "Jython",
    "arsonist duck", "Coreflood", "Juusto", "OpenSverige",
}
ERA_START = "2026-08-12"

COLS = ["match_id", "created_at", "teamA_name", "teamA_version",
        "teamB_name", "teamB_version", "game_index", "map", "winner_side",
        "win_condition", "turns"]

REQUEST_INTERVAL_S = 1.0
MAX_RETRIES = 5


def fetch_match_info(mid: str) -> tuple[dict | None, str]:
    """`fcode match info <mid> --json`, retrying transient failures.

    ⛔ Only inspect the raw text for rate-limit language AFTER json.loads has
    already failed on it. A valid response body is full of UUIDs and hex ids
    -- "429", "too many", etc. occur there BY CHANCE at non-trivial rate over
    a payload this size, so scanning a payload that already parsed as JSON
    for error phrasing is a guaranteed false-positive generator. Checked live
    (2026-08-14): a clean, valid `match info` response for a real match
    tripped a naive whole-blob "429" substring check on this exact bug.

    Returns (parsed_dict_or_None, last_raw_text).
    """
    last_text = ""
    for attempt in range(MAX_RETRIES):
        r = subprocess.run([FC] + ["match", "info", mid, "--json"],
                            cwd=ROOT, text=True, capture_output=True)
        last_text = r.stdout
        try:
            return json.loads(last_text), last_text
        except Exception:
            pass
        low = (r.stdout + r.stderr).lower()
        is_rate_limit = ("rate limit" in low or "too many requests" in low
                          or "429" in low)
        wait = 5 * (attempt + 1) if is_rate_limit else 2
        reason = "rate-limited" if is_rate_limit else "unparseable response"
        print(f"  {reason} on {mid}, retry in {wait}s "
              f"(attempt {attempt+1}/{MAX_RETRIES})", file=sys.stderr, flush=True)
        time.sleep(wait)
    return None, last_text


def load_scope() -> list[dict]:
    """⛔ `league_matches.tsv` itself carries duplicate match ids -- 41 of them
    league-wide as of 2026-08-14 (44,773 rows, 44,732 unique ids), a defect in
    the incremental updater that owns that file. This is a READ-ONLY source
    (hard limit: never edit an existing file under `corpus/`), so the dedup
    has to happen here. Without it, a duplicated id produces a duplicated
    block of output rows -- caught live: 9 of the 41 source dupes fell inside
    this tool's scope+era filter and doubled 9 matches' worth of rows before
    this guard existed. First occurrence wins; order is otherwise arbitrary
    since duplicate rows for the same id are identical in every column that
    matters here."""
    rows = list(csv.DictReader(SRC.open(), delimiter="\t"))
    seen_ids: set[str] = set()
    sel = []
    for r in rows:
        if (r["teamAName"] in TEAMS or r["teamBName"] in TEAMS) \
                and r["createdAt"] >= ERA_START and r["id"] not in seen_ids:
            seen_ids.add(r["id"])
            sel.append(r)
    sel.sort(key=lambda r: r["createdAt"])
    return sel


def load_ledger(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {ln.strip() for ln in path.read_text().splitlines() if ln.strip()}


def main() -> None:
    out_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "corpus/league_maps.tsv"
    ledger_path = out_path.with_suffix(".done")

    sel = load_scope()
    print(f"scope: {len(sel)} matches involving {len(TEAMS)} named teams, "
          f"createdAt >= {ERA_START}", file=sys.stderr)

    done = load_ledger(ledger_path)
    print(f"ledger: {len(done)} matches already banked", file=sys.stderr)

    write_header = not out_path.exists()
    out_f = out_path.open("a")
    ledger_f = ledger_path.open("a")
    if write_header:
        gen = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        out_f.write(f"# built by tools/corpus/league_maps.py; "
                    f"scope: {len(TEAMS)} named teams (see TEAMS in the script), "
                    f"createdAt >= {ERA_START}; generated {gen}\n")
        out_f.write("\t".join(COLS) + "\n")
        out_f.flush()

    n_ok = n_fail = n_noncomplete = 0
    n_cached = len(done)
    t0 = time.time()
    todo = [m for m in sel if m["id"] not in done]
    print(f"to fetch: {len(todo)}", file=sys.stderr)

    for i, m in enumerate(todo):
        mid = m["id"]
        d, last_text = fetch_match_info(mid)
        if d is None:
            n_fail += 1
            print(f"  BAD JSON {mid} after {MAX_RETRIES} attempts: "
                  f"{last_text[:120]!r}", file=sys.stderr)
            time.sleep(REQUEST_INTERVAL_S)
            continue

        mm = d.get("match")
        if not mm:
            n_fail += 1
            print(f"  NO match KEY {mid}", file=sys.stderr)
            time.sleep(REQUEST_INTERVAL_S)
            continue
        if mm.get("status") != "complete":
            n_noncomplete += 1
            time.sleep(REQUEST_INTERVAL_S)
            continue

        games = d.get("games") or []
        if not games:
            n_fail += 1
            print(f"  NO GAMES {mid} (status={mm.get('status')})", file=sys.stderr)
            time.sleep(REQUEST_INTERVAL_S)
            continue

        rows_buf = []
        ok = True
        for g in games:
            mp = g.get("mapName")
            side = g.get("winnerSide")
            if not mp or not side:
                ok = False
                print(f"  MISSING map/winnerSide {mid} game {g.get('gameNumber')}",
                      file=sys.stderr)
                break
            # Name/version/createdAt come from the ALREADY-LOADED
            # league_matches.tsv row `m` (from `match list`), never from
            # `match info`'s `mm` -- verified live (2026-08-14) that
            # `match info --json` returns teamAVersion/teamBVersion as JSON
            # null on every sampled match while `match list` carries the
            # real number for the same match. Side alignment (A/B) between
            # the two endpoints was spot-checked 8/8 consistent; only the
            # display NAME can legitimately drift between snapshots (a team
            # rename caught mid-scope, e.g. LingLing40 -> lingling_40h),
            # which is exactly why both spellings are in TEAMS.
            rows_buf.append("\t".join(str(x) for x in [
                mid, m.get("createdAt", ""), m.get("teamAName", ""),
                m.get("teamAVersion", ""), m.get("teamBName", ""),
                m.get("teamBVersion", ""), g.get("gameNumber", ""),
                mp, side.upper(), g.get("winCondition", ""),
                g.get("turnsPlayed", 0),
            ]))
        if not ok:
            n_fail += 1
            time.sleep(REQUEST_INTERVAL_S)
            continue

        for line in rows_buf:
            out_f.write(line + "\n")
        out_f.flush()
        ledger_f.write(mid + "\n")
        ledger_f.flush()
        n_ok += 1

        if (i + 1) % 50 == 0:
            print(f"  ...{i+1}/{len(todo)} fetched, {n_ok} ok, {n_fail} fail, "
                  f"{n_noncomplete} non-complete, {time.time()-t0:.0f}s",
                  file=sys.stderr, flush=True)
        time.sleep(REQUEST_INTERVAL_S)

    out_f.close()
    ledger_f.close()
    print(f"DONE: {n_ok} ok, {n_fail} fail, {n_noncomplete} non-complete "
          f"(will retry next run), {n_cached} pre-cached, out of {len(sel)} "
          f"scope matches ({len(todo)} attempted this run) -> {out_path}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
