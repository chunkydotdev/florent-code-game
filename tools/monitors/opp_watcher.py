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

# --- the Elo tee ------------------------------------------------------------
# Magnus, 2026-08-09: "Don't we have a script that scrapes our games, why don't
# we loop in this there?"  He is right and it is nearly free.
#
# This watcher already pulls `match list --json --limit 100` LEAGUE-WIDE every
# 10 minutes, and every row carries ratingABefore/ratingBBefore and
# eloDeltaA/B for BOTH teams. All of it was being read for a version check and
# then thrown away. Appending it costs ZERO extra platform calls and makes the
# field's Elo history a query instead of a scrape: an append-only match log IS
# the trajectory, so no snapshot files are needed.
#
# WHY IT MATTERS RIGHT NOW, from a live incident: the Loki benchmark fixture
# included Orizon, who had quietly fallen below 1400 and out of our bracket.
# Nobody noticed until Magnus said so, and a headline p-value had already been
# computed on games against a team we no longer meet. With this log the slide
# is visible the same day it happens.
#
# Failure is contained on purpose: the whole tee is wrapped, and any error is
# swallowed so a logging problem can never break the version alarm this file
# exists for.
LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "corpus", "league_elo_log.tsv")
LOG_COLS = ("id", "createdAt", "status", "triggeredBy", "scoreA", "scoreB",
            "teamAId", "teamAName", "teamAVersion", "ratingABefore", "eloDeltaA",
            "teamBId", "teamBName", "teamBVersion", "ratingBBefore", "eloDeltaB")


def tee_elo(matches) -> None:
    """Append unseen match rows to the league Elo log. Never raises."""
    try:
        seen = set()
        if os.path.exists(LOG):
            with open(LOG) as fh:
                next(fh, None)
                for line in fh:
                    seen.add(line.split("\t", 1)[0])
        new = []
        for m in matches:
            mid = str(m.get("id") or "")
            if not mid or mid in seen:
                continue
            seen.add(mid)
            new.append("\t".join(str(m.get(c, "")).replace("\t", " ").replace("\n", " ")
                                 for c in LOG_COLS))
        if not new:
            return
        fresh = not os.path.exists(LOG)
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        with open(LOG, "a") as fh:
            if fresh:
                fh.write("\t".join(LOG_COLS) + "\n")
            fh.write("\n".join(new) + "\n")
    except Exception:
        return          # a logging fault must never silence the version alarm

NEMESES = ("lunds", "ctrlaltdefeat", "ouroboros", "kladde", "flotte", "powerpuff",
           "clanker", "0033", "leviathan", "o(1)")
STATE = os.path.join(os.environ.get("STATE_DIR", "."), "opp_watcher_state.json")


def main() -> None:
    try:
        matches = json.loads(sys.stdin.read())["matches"]
    except Exception:
        return

    tee_elo(matches)

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
