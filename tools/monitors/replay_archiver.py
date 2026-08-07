"""Ladder replay archiver — passive whole-ladder data harvest.

Every completed ladder/unrated match on the platform is downloadable,
including matches we are not in. Replays + match metadata are the unbounded
read-only data source (decode corpora, probe freezing, retired-map insurance)
— unlike unrated challenges, which are deterministic per (team, map, version),
rate-limited, and covered by the no-platform-writes-from-loops rule.

Cadence: 30 min, max 8 matches/cycle (each match = up to 5 game files),
2s pause between downloads. Quiet on success; speaks only on failure.

Arm (from repo root):
  while true; do .venv/bin/python tools/monitors/replay_archiver.py; sleep 1800; done

Archive layout: replay_archive/<matchId>_game_<N>.replay26 plus
<matchId>.meta.json (the match-list row: teams, versions, ratings, timestamps
— none of which is recoverable from the replay filename). manifest.json
tracks archived/abandoned ids. The dir is gitignored.
"""
import json
import os
import subprocess
import sys
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FCODE = os.path.join(ROOT, ".venv", "bin", "fcode")
ARCHIVE = os.environ.get("REPLAY_ARCHIVE_DIR", os.path.join(ROOT, "replay_archive"))
MANIFEST = os.path.join(ARCHIVE, "manifest.json")
PER_CYCLE = 8


def main() -> None:
    os.makedirs(ARCHIVE, exist_ok=True)
    # Our own matches first, every cycle — the global list is deep enough to
    # rotate our games out between passes (measured: missed our Memtrace match
    # entirely on 2026-08-07), and our matches are the ones both sessions
    # decode same-day.
    matches = []
    try:
        mine = subprocess.run(
            [FCODE, "match", "list", "--mine", "--json", "--limit", "20"],
            capture_output=True, text=True, timeout=120,
        )
        mine_rows = json.loads(mine.stdout)["matches"]
        # Tag ours so the newest-first sort below cannot rotate them out of
        # the PER_CYCLE window (session-14 catch: the plain merge+sort made
        # "our matches first" a comment, not a behavior — 6 of our matches
        # sat unarchived behind fresher globals; also explains the earlier
        # Memtrace miss).
        for m in mine_rows:
            m["_mine"] = True
        matches.extend(mine_rows)
    except Exception:
        pass
    try:
        out = subprocess.run(
            [FCODE, "match", "list", "--json", "--limit", "100"],
            capture_output=True, text=True, timeout=120,
        )
        matches.extend(json.loads(out.stdout)["matches"])
    except Exception:
        if not matches:
            print("REPLAY ARCHIVER: match-list fetch failed this cycle")
            return

    st = {"archived": [], "failed": {}}
    if os.path.exists(MANIFEST):
        try:
            with open(MANIFEST) as f:
                st = json.load(f)
        except Exception:
            pass
    done = set(st.get("archived", []))
    failed = st.get("failed", {})

    seen_ids = set()
    todo = []
    for m in matches:
        if m.get("status") == "complete" and m["id"] not in done and m["id"] not in seen_ids:
            seen_ids.add(m["id"])
            todo.append(m)
    todo.sort(key=lambda m: m.get("completedAt") or "", reverse=True)
    todo.sort(key=lambda m: 0 if m.get("_mine") else 1)  # stable: ours first, each group newest-first
    for m in todo[:PER_CYCLE]:
        mid = m["id"]
        try:
            r = subprocess.run(
                [FCODE, "match", "replay", mid],
                cwd=ARCHIVE, capture_output=True, text=True, timeout=300,
            )
            if r.returncode == 0:
                with open(os.path.join(ARCHIVE, f"{mid}.meta.json"), "w") as f:
                    json.dump(m, f)
                done.add(mid)
                failed.pop(mid, None)
            else:
                n = failed.get(mid, 0) + 1
                failed[mid] = n
                if n >= 3:
                    print(f"REPLAY ARCHIVER: {mid} failed {n} cycles, abandoning")
                    done.add(mid)
        except Exception:
            pass
        time.sleep(2)

    st["archived"] = sorted(done)
    st["failed"] = failed
    with open(MANIFEST, "w") as f:
        json.dump(st, f)


main()
