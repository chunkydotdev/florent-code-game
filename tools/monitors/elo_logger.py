"""Elo/submission logger — the appending monitor (exactly ONE at a time).

Cadence: 5 min. Appends a row to elo_history.tsv every poll; prints (= wakes
the session) ONLY on: activation change, new submission upload, |Δrating| > 25.

Arm (from repo root; STATE_DIR = session scratchpad):
  while true; do
    S=$(.venv/bin/fcode status --json 2>/dev/null || true)
    L=$(.venv/bin/fcode submission list --json 2>/dev/null || true)
    printf '%s\n---SPLIT---\n%s' "$S" "$L" | \
      STATE_DIR=<scratchpad> .venv/bin/python tools/monitors/elo_logger.py
    sleep 300
  done
"""
import json
import os
import sys
from datetime import datetime

HIST = os.path.join(os.path.dirname(__file__), "..", "..", "elo_history.tsv")
STATE = os.path.join(os.environ.get("STATE_DIR", "."), "elo_logger_state.json")


def main() -> None:
    raw = sys.stdin.read()
    status_raw, _, subs_raw = raw.partition("---SPLIT---")
    try:
        d = json.loads(status_raw)
        rating = d["rating"]["rating"]
        matches = d["rating"]["matches_played"]
        rank = d["rank"]["rank"]
        act = d["active_submission"]
        ver, name = act["version"], act.get("name", "")
    except Exception:
        return  # transient fetch failure; skip this poll

    st = {}
    if os.path.exists(STATE):
        try:
            with open(STATE) as f:
                st = json.load(f)
        except Exception:
            st = {}

    ts = datetime.now().strftime("%Y-%m-%dT%H:%M")
    with open(os.path.abspath(HIST), "a") as f:
        f.write(f"{ts}\t{round(rating)}\t{matches}\tv{ver}\trank #{rank}\n")

    prev_ver = st.get("active_version")
    if prev_ver is not None and ver != prev_ver:
        print(f'ACTIVATION CHANGE: v{prev_ver} -> v{ver} "{name}" now live')

    prev_rating = st.get("rating")
    if prev_rating is not None and abs(rating - prev_rating) > 25:
        print(
            f"RATING JUMP: {round(prev_rating)} -> {round(rating)} "
            f"({round(rating - prev_rating):+d}), rank #{rank}, {matches} matches"
        )

    max_ver = st.get("max_version")
    try:
        subs = json.loads(subs_raw)
        newest = max(subs, key=lambda s: s["version"])
        if max_ver is not None and newest["version"] > max_ver:
            print(
                f'NEW SUBMISSION: v{newest["version"]} "{newest["name"]}" '
                f'by {newest.get("submittedByName", "?")}'
            )
        max_ver = newest["version"]
    except Exception:
        pass  # submission list fetch failed; keep old max

    # Slot-swap rule (Magnus+x3r0 2026-08-08, REVISED 16:48; threshold
    # recalibrated 2026-08-09, process-review adoption — ship-gate.md
    # amendment 2 changes with this constant or not at all): the rolling
    # last-5 window (1) prices only the CURRENT holder's matches — tape rows
    # are filtered by the live version tag, so a holder change resets the
    # window naturally — and (2) arms only after the holder's 8th match.
    # net <= SWAP_THRESHOLD while armed frees the slot (never forces a swap).
    # -21 = -1 sd of the rolling-5 sum (per-match sd 9.25, workflow-analysis
    # v3); the old <=0 threshold sat at 0 sd of a 20.7-sd quantity and fired
    # on a coin flip (50.4% on a neutral holder at match 8). Wake on
    # crossings both directions, and on arming directly into the free state.
    SWAP_THRESHOLD = -21
    swappable = st.get("swappable")
    try:
        base = None
        holder_start = None
        tag = f"v{ver}"
        with open(os.path.abspath(HIST)) as f:
            for row in f:
                parts = row.rstrip("\n").split("\t")
                if len(parts) >= 4 and parts[2].isdigit() and parts[3] == tag:
                    m = int(parts[2])
                    if holder_start is None or m < holder_start:
                        holder_start = m
                    if m <= matches - 5:
                        base = float(parts[1])
        armed = holder_start is not None and matches - holder_start >= 8
        if not armed:
            swappable = None  # window not armed; no wake, no stale flag
        elif base is not None:
            net5 = rating - base
            now_swappable = net5 <= SWAP_THRESHOLD
            if swappable is None and now_swappable:
                print(
                    f"SWAP RULE: window ARMED into SLOT FREE — v{ver} rolling "
                    f"last-5 net {round(net5):+d} ({round(base)} -> "
                    f"{round(rating)}), {matches} matches "
                    f"(holder since @{holder_start})"
                )
            elif swappable is not None and now_swappable != swappable:
                state_txt = "SLOT FREE (swap rule)" if now_swappable else "slot held again"
                print(
                    f"SWAP RULE: {state_txt} — v{ver} rolling last-5 net "
                    f"{round(net5):+d} ({round(base)} -> {round(rating)}), "
                    f"{matches} matches (holder since @{holder_start})"
                )
            swappable = now_swappable
    except Exception:
        pass  # tape unreadable this poll; keep old flag

    with open(STATE, "w") as f:
        json.dump({"rating": rating, "active_version": ver, "max_version": max_ver,
                   "swappable": swappable}, f)


main()
