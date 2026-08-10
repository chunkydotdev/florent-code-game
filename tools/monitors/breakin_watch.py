#!/usr/bin/env python3
"""BREAK-IN WATCH — the stop-loss for a freshly shipped bot's first 8 matches.

WHY THIS EXISTS. Both automated stop-losses segment the tape by the LIVE
version and arm only at k >= ARM_AFTER (8). So the moment a new bot is
activated it is at k=0 and **there is no automated stop-loss on the rated
ladder bot at all** until it has played 8 matches. That is precisely the window
in which a bad ship does its damage, and it was open for v104 "Loki v2".

THE FLOOR IS 1567, AND THE NUMBER MEANS SOMETHING RATHER THAN BEING ROUND.
v102 was activated at 1567.44 and climbed ~48 points from there over a night.
**If v104 falls to 1567 it has given back the entire gain its predecessor
earned** — that is a real line, not a noise threshold, and at the observed
~+-9 per rated match it is ~5 consecutive bad matches away.

SILENCE IS NOT SAFE. This reads `elo_history.tsv`, which stalled for ~45
minutes today while `ship_watch` cheerfully reported rows 7 minutes old as
current. So a stale tape is itself an alert here: a monitor that reads a file
must report that file's freshness or its blindness and its confidence look
identical.

Hands back to the slot rule at k >= 8; exits when it does.
"""
import os, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
TAPE = ROOT / "elo_history.tsv"
ALERT = ROOT / "corpus" / "BREAKIN_ALERT"
FLOOR = float(os.environ.get("BREAKIN_FLOOR", "1567"))
VERSION = os.environ.get("BREAKIN_VERSION", "v104")
STALE_S = float(os.environ.get("BREAKIN_STALE_S", "900"))


def rows():
    try:
        out = []
        for ln in TAPE.read_text().splitlines()[1:]:
            f = ln.split("\t")
            if len(f) >= 4:
                out.append(f)
        return out
    except Exception:
        return []


def alert(msg):
    ALERT.write_text(msg + "\n")
    sys.stderr.write(msg + "\n")


def main():
    while True:
        r = rows()
        mine = [x for x in r if x[3] == VERSION]
        if not r:
            alert(f"BREAK-IN WATCH BLIND: cannot read {TAPE}")
        else:
            age = time.time() - TAPE.stat().st_mtime
            if age > STALE_S:
                alert(f"BREAK-IN WATCH BLIND: tape unwritten for {age/60:.0f} min. "
                      f"Silence is NOT 'no breach'. Check the platform.")
            elif mine:
                rating = float(mine[-1][1])
                k = len(mine)
                if rating < FLOOR:
                    alert(f"*** BREAK-IN FLOOR BREACHED *** {VERSION} rating "
                          f"{rating:.0f} < {FLOOR:.0f} at k={k}.\n"
                          f"ROLLBACK: .venv/bin/fcode submission activate 102"
                          f"   # VERSION INT, THEN VERIFY with `fcode status`")
                elif k >= 8:
                    sys.stderr.write(f"{VERSION} reached k={k}; slot rule is armed. "
                                     f"Break-in watch standing down.\n")
                    if ALERT.exists():
                        ALERT.unlink()
                    return 0
                else:
                    if ALERT.exists():
                        ALERT.unlink()
        time.sleep(120)


if __name__ == "__main__":
    sys.exit(main())
