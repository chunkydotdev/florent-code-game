"""Opponent-version watcher — wakes on nemesis version changes (bumps AND
rollbacks: CAD's v110->v107 rollback mattered too). A version change
invalidates A/B baselines and probe fidelity for that team.

Cadence: 10 min. Versions are read from the global match-list JSON (each
match row carries teamA/BVersion), so one call covers every nemesis that
played recently.

Arm (from repo root; STATE_DIR = session scratchpad):
  while true; do
    .venv/bin/fcode match list --json --limit 100 2>/dev/null | \
      STATE_DIR=<scratchpad> .venv/bin/python tools/monitors/opp_watcher.py
    sleep 600
  done
"""
import json
import os
import sys

NEMESES = ("lunds", "ctrlaltdefeat", "ouroboros", "kladde", "flotte", "powerpuff")
STATE = os.path.join(os.environ.get("STATE_DIR", "."), "opp_watcher_state.json")


def main() -> None:
    try:
        matches = json.loads(sys.stdin.read())["matches"]
    except Exception:
        return

    latest = {}  # team name -> (createdAt, version)
    for m in matches:
        for side in ("A", "B"):
            name = m.get(f"team{side}Name") or ""
            ver = m.get(f"team{side}Version")
            if ver is None or not any(n in name.lower() for n in NEMESES):
                continue
            t = m.get("createdAt") or ""
            if name not in latest or t > latest[name][0]:
                latest[name] = (t, ver)

    st = {}
    first_run = not os.path.exists(STATE)
    if not first_run:
        try:
            with open(STATE) as f:
                st = json.load(f)
        except Exception:
            st = {}

    for name, (t, ver) in latest.items():
        old = st.get(name)  # [createdAt, version]
        if old is not None and t > old[0] and ver != old[1]:
            print(
                f"OPPONENT VERSION CHANGE: {name} v{old[1]} -> v{ver} "
                f"(A/B baselines + probe fidelity for this team now suspect)"
            )
        if old is None or t > old[0]:
            st[name] = [t, ver]

    with open(STATE, "w") as f:
        json.dump(st, f)


main()
