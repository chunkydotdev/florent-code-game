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

    # Slot-swap rule (Magnus+x3r0 2026-08-08, revised same day): a live bot at
    # <=0 net Elo over the rolling LAST 5 MATCHES is free to swap. Wake on the
    # condition crossing in either direction; the rating five matches back is
    # read from our own tape (latest row at matches <= now-5).
    swappable = st.get("swappable")
    try:
        base = None
        with open(os.path.abspath(HIST)) as f:
            for row in f:
                parts = row.rstrip("\n").split("\t")
                if len(parts) >= 3 and parts[2].isdigit() and int(parts[2]) <= matches - 5:
                    base = float(parts[1])
        if base is not None:
            net5 = rating - base
            now_swappable = net5 <= 0
            if swappable is not None and now_swappable != swappable:
                state_txt = "SLOT FREE (swap rule)" if now_swappable else "slot held again"
                print(
                    f"SWAP RULE: {state_txt} — v{ver} rolling last-5 net "
                    f"{round(net5):+d} ({round(base)} -> {round(rating)}), {matches} matches"
                )
            swappable = now_swappable
    except Exception:
        pass  # tape unreadable this poll; keep old flag

    with open(STATE, "w") as f:
        json.dump({"rating": rating, "active_version": ver, "max_version": max_ver,
                   "swappable": swappable}, f)


main()
