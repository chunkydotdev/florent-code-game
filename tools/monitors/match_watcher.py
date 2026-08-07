"""Match watcher — wakes the session on 4+ win/loss streaks in ladder play.

Cadence: 2 min. Silent otherwise (the Elo logger owns rating-jump wakes).

Arm (from repo root; STATE_DIR = session scratchpad):
  while true; do
    .venv/bin/fcode match list --mine --type ladder --json --limit 20 2>/dev/null | \
      STATE_DIR=<scratchpad> .venv/bin/python tools/monitors/match_watcher.py
    sleep 120
  done
"""
import json
import os
import sys

OUR_TEAM_ID = "379a5d80-9921-4c9e-949b-f9b1dcba16be"  # OpenSverige
STATE = os.path.join(os.environ.get("STATE_DIR", "."), "match_watcher_state.json")


def main() -> None:
    try:
        matches = json.loads(sys.stdin.read())["matches"]
    except Exception:
        return
    done = [m for m in matches if m.get("status") == "complete" and m.get("triggeredBy") == "ladder"]
    done.sort(key=lambda m: m["completedAt"], reverse=True)
    if not done:
        return

    st = {}
    if os.path.exists(STATE):
        try:
            with open(STATE) as f:
                st = json.load(f)
        except Exception:
            st = {}

    newest_id = done[0]["id"]
    last_seen = st.get("last_id")
    with open(STATE, "w") as f:
        json.dump({"last_id": newest_id}, f)
    if last_seen is None or newest_id == last_seen:
        return  # first poll (baseline) or nothing new

    streak, won = 0, None
    for m in done:
        w = m.get("winnerId") == OUR_TEAM_ID
        if won is None:
            won, streak = w, 1
        elif w == won:
            streak += 1
        else:
            break

    if streak >= 4:
        latest = done[0]
        we_are_a = latest["teamAId"] == OUR_TEAM_ID
        opp = latest["teamBName"] if we_are_a else latest["teamAName"]
        us = latest["scoreA"] if we_are_a else latest["scoreB"]
        them = latest["scoreB"] if we_are_a else latest["scoreA"]
        rating = latest["teamARating"] if we_are_a else latest["teamBRating"]
        kind = "win" if won else "LOSS"
        print(
            f"STREAK {'W' if won else 'L'}{streak}: latest {kind} vs {opp} "
            f"{us}-{them}, rating ~{round(rating)}"
        )


main()
