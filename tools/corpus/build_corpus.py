#!/usr/bin/env python3
"""Build the whole-archive corpus: three decoders, a join table, and a manifest.

WHY THIS EXISTS.  `replay_archive/` reached 3,800+ files (1.2 GB) while the
largest replay-based read in the repo was 219 games; every session hand-rolled a
decoder for 5-35 games and threw it away (HANDOVER: "session scratchpads DIE with
the session ... budget ~10 min for that on first use").  A whole-archive pass
costs about three minutes.  This script makes that pass reproducible and its
output committable, so a session ASKS the corpus instead of rebuilding it.

    .venv/bin/python tools/corpus/build_corpus.py            # incremental
    .venv/bin/python tools/corpus/build_corpus.py --force    # rebuild all
    .venv/bin/python tools/corpus/build_corpus.py --no-net   # skip fcode calls

OUTPUTS (in corpus/, committed gzipped):
    ladder_games.tsv   one row per GAME of our ladder matches (free metadata)
    throws.tsv         one row per launcher throw, with what the raider achieved
    builds.tsv         one row per turret/launcher build, with placement geometry
    build_agg.tsv      per file/team/band counters (builds, shots, builder attacks)
    join.tsv           replay file -> match -> opponent -> OUR team index
    manifest.json      archive size, git sha, row counts, build time

THE JOIN IS THE POINT.  A replay knows only "team 0" and "team 1".  join.tsv maps
each archived file to the opponent name and to WHICH index is us, which is what
turns 58k anonymous throw events into "Ouroboros has never thrown a builder".
It is RECONCILED on build: the seat derived from the free metadata must equal the
winner recorded inside the replay, or the row is dropped and counted.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from atomicio import (atomic_open, atomic_write_text,  # noqa: E402
                      atomic_subprocess_target)

ARCHIVE = ROOT / "replay_archive"
OUT = ROOT / "corpus"
PY = str(ROOT / ".venv/bin/python")
HERE = Path(__file__).resolve().parent

MATCH_ID = re.compile(r"^(.*)_game_\d+\.replay26$")


def match_id_of(name: str) -> str | None:
    m = MATCH_ID.match(name)
    return m.group(1) if m else None


def sh(args, **kw):
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, **kw)


def replay_files() -> list[Path]:
    return sorted(ARCHIVE.rglob("*.replay26"))


def stage_ladder_meta(force: bool, no_net: bool) -> Path:
    dst = OUT / "ladder_games.tsv"
    if dst.exists() and not force:
        print(f"  ladder_games.tsv exists ({sum(1 for _ in dst.open())-1} rows) — skip")
        return dst
    if no_net:
        print("  --no-net: skipping ladder metadata")
        return dst
    print("  pulling ladder metadata (paginated match list + one match info each)...")
    r = sh([PY, str(HERE / "ladder_meta.py"), str(dst)])
    sys.stderr.write(r.stderr[-400:])
    return dst


def stage_replays(files: list[Path], force: bool) -> None:
    throws = OUT / "throws.tsv"
    builds = OUT / "builds.tsv"
    agg = OUT / "build_agg.tsv"
    args = [str(p) for p in files]
    if force or not throws.exists():
        print(f"  decoding throws over {len(files)} replays...")
        # ATOMIC (s50): a --force rebuild is MINUTES of decode with the old
        # table truncated to zero the whole time. Any lane reading throws.tsv in
        # that window read an empty or short table, silently.
        with atomic_subprocess_target(throws) as tmp:
            with open(tmp, "w") as fh:
                r = subprocess.run([PY, str(HERE / "replay_throws.py")] + args,
                                   cwd=ROOT, text=True, stdout=fh,
                                   stderr=subprocess.PIPE)
        print("   ", r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "ok")
    else:
        print("  throws.tsv exists — skip")
    if force or not builds.exists():
        print(f"  decoding builds/placement over {len(files)} replays...")
        # Same for the two-output decoder: it writes both paths itself, so the
        # temps are handed to it as argv and renamed only once it returns.
        with atomic_subprocess_target(builds) as tb, \
                atomic_subprocess_target(agg) as ta:
            r = subprocess.run([PY, str(HERE / "replay_builds.py"), str(tb), str(ta)] + args,
                               cwd=ROOT, text=True, capture_output=True)
        print("   ", r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "ok")
    else:
        print("  builds.tsv exists — skip")


GAME_N = re.compile(r"_game_(\d+)\.replay26$")


def stage_join(files: list[Path]) -> dict:
    """replay file -> (match, opponent, our team index), RECONCILED against the replay.

    The reconciliation test (standing rule, tape 2026-08-09): the seat derived
    from the free metadata must independently predict the winner recorded inside
    the replay binary. `winnerSide` + `won` give us our team index; the replay's
    own `winner` field must then equal our index iff we won that game. A row that
    fails is DROPPED, not silently kept -- a join that merely looks right is not
    evidence, and a wrong seat would invert every per-team claim built on it.
    """
    games_path = OUT / "ladder_games.tsv"
    # per match, games in listing order -> game_1, game_2, ...
    per_match: dict[str, list[dict]] = {}
    if games_path.exists():
        for row in csv.DictReader(games_path.open(), delimiter="\t"):
            per_match.setdefault(row["match"], []).append(row)

    # winner recorded INSIDE each replay
    replay_winner: dict[str, int] = {}
    tp = OUT / "throws.tsv"
    if tp.exists():
        for row in csv.DictReader(tp.open(), delimiter="\t"):
            replay_winner.setdefault(row["file"], int(row["winner"]))
    bp = OUT / "builds.tsv"
    if bp.exists():
        for row in csv.DictReader(bp.open(), delimiter="\t"):
            replay_winner.setdefault(row["file"], int(row["winner"]))

    dst = OUT / "join.tsv"
    kept = dropped = unmatched = untested = 0
    # ATOMIC (s50): `join.tsv` is rebuilt on EVERY keeper sync (~10 min) and it
    # is the file the DAEMON_WRITTEN list in tests/test_instruments.py already
    # names as keeper-owned — i.e. it is known to be rewritten under readers.
    with atomic_open(dst) as fh:
        fh.write("file\tmatch\tgame\topp\toppver\tourver\toppbef\tmap\tcond\tturns"
                 "\twon\tour_team\n")
        for p in files:
            mid = match_id_of(p.name)
            gm = GAME_N.search(p.name)
            games = per_match.get(mid or "")
            if not games or not gm:
                unmatched += 1
                continue
            idx = int(gm.group(1)) - 1
            if idx >= len(games):
                unmatched += 1
                continue
            row = games[idx]
            won = row["won"] == "1"
            # `winner_seat` is the WINNING seat, not ours -- the flip below is
            # what turns it into ours. Reads the legacy `seat` key too so an
            # un-rebuilt ladder_games.tsv keeps working through the rename.
            ws = row.get("winner_seat") or row.get("seat", "")
            ours = ws if won else ("b" if ws == "a" else "a")
            our_team = 0 if ours == "a" else 1
            # --- reconciliation ---
            rw = replay_winner.get(p.name)
            if rw is None:
                untested += 1              # no throw/build rows -> winner unseen
            elif rw >= 0:
                expect = our_team if won else 1 - our_team
                if rw != expect:
                    dropped += 1
                    continue
            fh.write(f"{p.name}\t{mid}\t{idx+1}\t{row['opp']}\t{row['oppver']}\t"
                     f"{row['ourver']}\t{row['oppbef']}\t{row['map']}\t{row['cond']}\t"
                     f"{row['turns']}\t{int(won)}\t{our_team}\n")
            kept += 1
    tested = kept + dropped - untested
    rate = (1 - dropped / tested) if tested > 0 else float("nan")
    print(f"  join.tsv: {kept} files mapped, {unmatched} unmatched "
          f"(unrated / other teams'), {dropped} DROPPED on reconciliation")
    print(f"  RECONCILIATION: {tested} rows testable against the replay's own "
          f"winner field, {rate:.4%} agree")
    return dict(joined=kept, unmatched=unmatched, dropped=dropped,
                reconciled=tested, agree_rate=None if tested <= 0 else round(rate, 6))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--no-net", action="store_true")
    a = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    files = replay_files()
    print(f"archive: {len(files)} replays")
    stage_ladder_meta(a.force, a.no_net)
    stage_replays(files, a.force)
    j = stage_join(files)

    def rows(name):
        p = OUT / name
        return (sum(1 for _ in p.open()) - 1) if p.exists() else 0

    sha = sh(["git", "rev-parse", "--short", "HEAD"]).stdout.strip()
    stamp = sh(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"]).stdout.strip()
    manifest = dict(
        built_utc=stamp, git_sha=sha, archive_replays=len(files),
        rows={n: rows(n) for n in ("ladder_games.tsv", "throws.tsv", "builds.tsv",
                                   "build_agg.tsv", "join.tsv")},
        join=j,
    )
    # ATOMIC: `sync.py --check` and the freshness tools read this manifest; an
    # empty read is indistinguishable from "the corpus was never built".
    atomic_write_text(OUT / "manifest.json", json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
