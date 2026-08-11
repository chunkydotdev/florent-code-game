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

⛔⛔ IF YOU FOUND THIS PROCESS NOT RUNNING, THAT IS CORRECT. DO NOT RE-ARM IT.
It hands back to the slot rule at k >= 8 and EXITS WHEN IT DOES. v104 is at
k=86. **It is down because it FINISHED, not because it died.**
**This has now been re-flagged as a dead monitor by three separate readers on
three lanes** (two other lanes at their boots, and one lane's own boot
verification). It was recorded in HANDOVER's boot block and in a process-deltas
ledger, and it got rediscovered anyway — because **a completed handoff and a
crashed daemon look identical in `ps`, and the place people look is the file.**
So it is written HERE, where the rediscovery happens.
**RE-ARM IT BEFORE THE NEXT ACTIVATION-AS-A-SHIP, NEVER BEFORE AN UNRATED LEG:**
a leg activates for ~16 s and rolls back, so there is no 8-match break-in window
to guard. *(Struck from the deltas ledger 2026-08-11: it is a FACT with nothing
to enforce, and a rule ledger is the wrong home for a fact — leaving it there
guaranteed a fourth firing.)*

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


def selftest():
    """Show this watch producing BOTH verdicts, and its blind branch too.

    A monitor whose silence has never been contrasted with its alarm has not
    been seen to check. ship_watch logged RULE=held for 45 minutes today off a
    stalled tape and looked exactly like a healthy monitor doing its job.
    """
    import io, contextlib
    ok = True
    tag = rows()[-1][3] if rows() else None
    if tag is None:
        print("SELFTEST INCONCLUSIVE: tape unreadable"); return 1

    def run(env):
        buf = io.StringIO()
        old = dict(os.environ); os.environ.update(env)
        try:
            with contextlib.redirect_stderr(buf):
                globals()["FLOOR"] = float(os.environ["BREAKIN_FLOOR"])
                globals()["VERSION"] = os.environ["BREAKIN_VERSION"]
                globals()["STALE_S"] = float(os.environ["BREAKIN_STALE_S"])
                r = rows(); mine = [x for x in r if x[3] == VERSION]
                age = time.time() - TAPE.stat().st_mtime
                if age > STALE_S:
                    alert(f"BLIND: tape unwritten for {age/60:.0f} min.")
                elif mine and float(mine[-1][1]) < FLOOR:
                    alert(f"*** BREAK-IN FLOOR BREACHED *** {VERSION} "
                          f"{float(mine[-1][1]):.0f} < {FLOOR:.0f}")
        finally:
            os.environ.clear(); os.environ.update(old)
        return buf.getvalue()

    breach = run({"BREAKIN_FLOOR": "99999", "BREAKIN_VERSION": tag, "BREAKIN_STALE_S": "999999"})
    quiet  = run({"BREAKIN_FLOOR": "1",     "BREAKIN_VERSION": tag, "BREAKIN_STALE_S": "999999"})
    blind  = run({"BREAKIN_FLOOR": "1",     "BREAKIN_VERSION": tag, "BREAKIN_STALE_S": "0"})
    for name, out, want in (("breach", breach, "BREACHED"),
                            ("blind",  blind,  "BLIND")):
        good = want in out
        print(f"  [{'ok' if good else 'FAIL'}] {name}: {out.strip()[:80] or '(silent)'}")
        ok &= good
    good = quiet.strip() == ""
    print(f"  [{'ok' if good else 'FAIL'}] no-breach: {quiet.strip()[:80] or '(silent, correct)'}")
    ok &= good
    if ALERT.exists():
        ALERT.unlink()
    print("SELFTEST PASS" if ok else "SELFTEST FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(main())
