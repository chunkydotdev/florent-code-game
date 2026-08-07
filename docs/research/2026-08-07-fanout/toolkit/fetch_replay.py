#!/usr/bin/env python3
"""fetch_replay — cached, rate-limit-polite downloader for .replay26 files.

The cache under SCRATCH/replay_cache/replays/ is SHARED by every analyst agent
in this session.  Always go through this script (or its `fetch()` function) so
we never hammer the platform for a file another agent already pulled.

CLI
---
    .venv/bin/python toolkit/fetch_replay.py <match_id> <game_number>
    .venv/bin/python toolkit/fetch_replay.py <match_id> 1 2 3 4 5
    .venv/bin/python toolkit/fetch_replay.py --all <match_id>      # games 1-5

Prints the cached path(s) on stdout, one per line.  Exit 0 on success.

Python
------
    import sys; sys.path.insert(0, "<SCRATCH>/toolkit")
    from fetch_replay import fetch
    from replay_lib import load_replay
    r = load_replay(fetch("8ed4d332-2968-453e-a23e-bb4c1f83f28e", 1))

Behaviour
---------
  * Already cached (non-trivial size)  -> returns immediately, no network, no sleep.
  * Not cached                         -> `fcode match replay ... -g N -o <path>`
                                          then sleeps SLEEP_AFTER_DOWNLOAD seconds.
  * A cross-process lock file stops two agents downloading the same game at once;
    the loser waits for the winner's file instead of issuing its own request.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time

SCRATCH = ("/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/"
           "8c290b06-f7e1-40b4-b90c-7343eb7e2e8e/scratchpad")
REPO = "/Users/junghard/Projects/Work/florent-code-game"
FCODE = os.path.join(REPO, ".venv/bin/fcode")
REPLAY_DIR = os.path.join(SCRATCH, "replay_cache", "replays")

SLEEP_AFTER_DOWNLOAD = 4.0     # seconds; courtesy pause, shared cache
MIN_SIZE = 1024                # anything smaller is a failed/partial download
LOCK_TIMEOUT = 180.0           # give up waiting on another agent's download


def cache_path(match_id: str, game: int) -> str:
    return os.path.join(REPLAY_DIR, f"{match_id}_g{game}.replay26")


def is_cached(match_id: str, game: int) -> bool:
    p = cache_path(match_id, game)
    return os.path.exists(p) and os.path.getsize(p) >= MIN_SIZE


def fetch(match_id: str, game: int, *, verbose: bool = False) -> str:
    """Return a local path to <match_id> game <game>, downloading if needed."""
    os.makedirs(REPLAY_DIR, exist_ok=True)
    path = cache_path(match_id, game)
    if is_cached(match_id, game):
        return path

    lock = path + ".lock"
    deadline = time.time() + LOCK_TIMEOUT
    while True:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            break
        except FileExistsError:
            # someone else is downloading this exact game — wait for their file
            if is_cached(match_id, game):
                return path
            if time.time() > deadline:
                try:                       # stale lock, take it over
                    os.unlink(lock)
                except OSError:
                    pass
                deadline = time.time() + LOCK_TIMEOUT
                continue
            time.sleep(1.0)

    try:
        if is_cached(match_id, game):      # won the race but it landed meanwhile
            return path
        tmp = path + ".part"
        cmd = [FCODE, "match", "replay", match_id, "-g", str(game), "-o", tmp]
        if verbose:
            print("  $ " + " ".join(cmd), file=sys.stderr)
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO)
        if r.returncode != 0 or not os.path.exists(tmp) or os.path.getsize(tmp) < MIN_SIZE:
            if os.path.exists(tmp):
                os.unlink(tmp)
            raise RuntimeError(
                f"download failed for {match_id} g{game} (rc={r.returncode}): "
                f"{(r.stderr or r.stdout or '').strip()[:300]}")
        os.replace(tmp, path)
        time.sleep(SLEEP_AFTER_DOWNLOAD)   # rate-limit courtesy
        return path
    finally:
        try:
            os.unlink(lock)
        except OSError:
            pass


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\nCLI")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("match_id")
    ap.add_argument("games", nargs="*", type=int, help="game numbers 1-5")
    ap.add_argument("--all", action="store_true", help="fetch games 1-5")
    ap.add_argument("-q", "--quiet", action="store_true")
    args = ap.parse_args()

    games = list(range(1, 6)) if args.all else (args.games or [1])
    rc = 0
    for g in games:
        try:
            cached = is_cached(args.match_id, g)
            p = fetch(args.match_id, g, verbose=not args.quiet)
            if not args.quiet:
                print(("cached  " if cached else "download") + f" g{g}", file=sys.stderr)
            print(p)
        except Exception as exc:                    # noqa: BLE001
            print(f"{args.match_id} g{g}: {exc}", file=sys.stderr)
            rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
