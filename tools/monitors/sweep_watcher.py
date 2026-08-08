"""Sweep watcher — early warning for opponent ships (retrodiction study, 2026-08-08).

Measured basis: a self-test sweep (>=3 unrated matches inside <=180s by one
team against >=3 distinct opponents) preceded that team's next version stamp
11/11 in the archive, median lead ~32 min. Waking on the sweep converts
version-churn wakes from reactive to predictive.

Cadence: 5 min. Silent except on a NEW sweep signature.

Arm (from repo root; STATE_DIR = session scratchpad):
  while true; do
    OUT=$(.venv/bin/fcode match list --json --limit 100 2>/dev/null | \
      STATE_DIR=<scratchpad> .venv/bin/python tools/monitors/sweep_watcher.py)
    if [ -n "$OUT" ]; then echo "$OUT"; break; fi; sleep 300
  done
(exit-on-wake shape, same as the other monitors)
"""
import json
import os
import sys
from datetime import datetime

STATE = os.path.join(os.environ.get("STATE_DIR", "."), "sweep_watcher_state.json")
WINDOW_S = 180
MIN_MATCHES = 3
MIN_OPPONENTS = 3


def ts(row):
    v = row.get("createdAt") or ""
    try:
        return datetime.fromisoformat(v.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def main() -> None:
    try:
        matches = json.loads(sys.stdin.read())["matches"]
    except Exception:
        return
    unrated = []
    for m in matches:
        if m.get("triggeredBy") == "ladder" or m.get("type") == "ladder":
            continue
        t = ts(m)
        if t is None:
            continue
        unrated.append((t, m.get("teamAName", ""), m.get("teamBName", ""), m.get("id", "")))
    unrated.sort()

    st = {}
    if os.path.exists(STATE):
        try:
            with open(STATE) as f:
                st = json.load(f)
        except Exception:
            st = {}
    seen = set(st.get("seen", []))
    first = not os.path.exists(STATE)  # first poll = silent baseline

    # Group by candidate sweeper: any team appearing in >=MIN_MATCHES unrated
    # rows inside a WINDOW_S span vs >=MIN_OPPONENTS distinct opponents.
    wakes = []
    teams = {t for _, a, b, _ in unrated for t in (a, b)}
    for team in teams:
        rows = [(t, b if a == team else a, mid) for t, a, b, mid in unrated if team in (a, b)]
        for i in range(len(rows)):
            j = i
            while j + 1 < len(rows) and rows[j + 1][0] - rows[i][0] <= WINDOW_S:
                j += 1
            burst = rows[i : j + 1]
            opps = {o for _, o, _ in burst}
            if len(burst) >= MIN_MATCHES and len(opps) >= MIN_OPPONENTS:
                sig = f"{team}:{int(rows[i][0])}"
                if sig not in seen:
                    seen.add(sig)
                    wakes.append(
                        f"SWEEP: {team} self-testing ({len(burst)} unrated vs "
                        f"{len(opps)} opponents in {int(rows[j][0]-rows[i][0])}s) "
                        f"— next stamp expected ~32min median (retrodiction 11/11)"
                    )
                break

    with open(STATE, "w") as f:
        json.dump({"seen": sorted(seen)[-200:]}, f)
    if not first:
        for w in wakes:
            print(w)


if __name__ == "__main__":
    main()
