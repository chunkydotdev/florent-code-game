"""Ladder replay archiver — passive whole-ladder data harvest.

Every completed ladder/unrated match on the platform is downloadable,
including matches we are not in. Replays + match metadata are the unbounded
read-only data source (decode corpora, probe freezing, retired-map insurance)
— unlike unrated challenges, which are deterministic per (team, map, version),
rate-limited, and covered by the no-platform-writes-from-loops rule.

Cadence: 30 min, max 8 matches/cycle (each match = up to 5 game files),
2s pause between downloads. Quiet on success; speaks only on failure.

PRIORITY REQUESTS (retro theme 5a, added s16): either arm may append match
ids (one per line, # comments ok) to replay_archive/priority_requests.txt.
Priority ids are front-queued ahead of the --mine pass every cycle — even if
they have rotated out of the match-list window — and are removed from the
file once archived or abandoned. Research names ids; the archiver serves them
first.

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
PRIORITY = os.path.join(ARCHIVE, "priority_requests.txt")
PER_CYCLE = 8


def read_priority() -> list:
    if not os.path.exists(PRIORITY):
        return []
    try:
        with open(PRIORITY) as f:
            return [ln.strip() for ln in f
                    if ln.strip() and not ln.strip().startswith("#")]
    except Exception:
        return []


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

    pri_ids = set(read_priority())
    seen_ids = set()
    todo = []
    for m in matches:
        if m.get("status") == "complete" and m["id"] not in done and m["id"] not in seen_ids:
            seen_ids.add(m["id"])
            if m["id"] in pri_ids:
                m["_pri"] = True
            todo.append(m)
    # Priority ids that have rotated out of both list windows still get an
    # attempt (stub meta; the failed-counter abandons after 3 cycles).
    for pid in pri_ids:
        if pid not in done and pid not in seen_ids:
            todo.append({"id": pid, "_pri": True, "_meta_stub": True})
    todo.sort(key=lambda m: m.get("completedAt") or "", reverse=True)
    # Stable sort: priority requests first, then ours, then globals —
    # each group newest-first.
    todo.sort(key=lambda m: 0 if m.get("_pri") else (1 if m.get("_mine") else 2))
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

    # Drop fulfilled/abandoned ids from the priority file, preserve the rest.
    if pri_ids:
        pending = [pid for pid in read_priority() if pid not in done]
        try:
            with open(PRIORITY, "w") as f:
                f.write("\n".join(pending) + ("\n" if pending else ""))
        except Exception:
            pass


main()
