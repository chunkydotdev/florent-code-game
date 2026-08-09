"""Window watcher — fires ONCE when a pre-registered evaluation point is reached.

WHY THIS EXISTS (2026-08-09, s20). The v80 window was pre-registered to settle at
n=20 and nobody was watching for n=20. It closed at 00:26:36Z; the builder scored
it ~3 hours later and only after the research arm happened to notice. In that gap
v80 played 19 more matches and lost 40.92 Elo, with a measured, identity-
controlled fix sitting KEEP-dev the whole time.

Both arms failed the same window from opposite directions — research dropped a
loop re-arm, the builder stalled — which is the point: **a recurring loop is not
the instrument for this.** The evaluation point is an EVENT (matches_played hits
a target), not a cadence. A loop that ticks every 25 minutes can still sail past
it, and one did. This fires once, on the condition, and then exits.

The four existing monitors watch streaks, rating jumps, opponent ships and replay
archiving. None of them watched the thing both arms had agreed was the most
informative event on the board.

Arm at the same moment the window is pre-registered, never later:

    TARGET=461 nohup bash -c 'while true; do
      .venv/bin/fcode status --json 2>/dev/null | \
        TARGET=$TARGET .venv/bin/python tools/monitors/window_watcher.py && break
      sleep 120
    done' &

Exits 0 (and prints, which wakes the session) once matches_played >= TARGET.
Exits 1 silently otherwise, so the `&& break` above only fires on the real event.

CAVEAT THAT IS NOT OPTIONAL: this dies with the session, like every monitor here.
It closes the "nobody noticed" hole for a live session only. For an unattended
window, the evaluation point needs a cloud routine (`/schedule`), not this.
"""
import json
import os
import sys


def main() -> int:
    target = int(os.environ.get("TARGET", "0"))
    if not target:
        print("window_watcher: no TARGET set — refusing to run blind", file=sys.stderr)
        return 1
    try:
        d = json.loads(sys.stdin.read())
        played = d["rating"]["matches_played"]
        rating = d["rating"]["rating"]
        rank = d["rank"]["rank"]
        ver = d["active_submission"]["version"]
    except Exception as e:
        print(f"window_watcher: unreadable status ({e})", file=sys.stderr)
        return 1

    if played < target:
        return 1

    over = played - target
    print(
        f"\n*** WINDOW CLOSED: {played} matches played, target was {target}"
        + (f" (ALREADY {over} MATCHES PAST IT — every one of these is unscored)" if over else "")
        + f"\n    live v{ver}  rating {rating:.2f}  rank #{rank}"
        "\n    SCORE THE PRE-REGISTRATION NOW. The window is only worth what the"
        "\n    decision at its evaluation point is worth, and the slot keeps"
        "\n    playing while it goes unscored — that cost 40.92 Elo on 2026-08-09."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
