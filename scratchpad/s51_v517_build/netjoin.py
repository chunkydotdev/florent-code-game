#!/usr/bin/env python3
"""⭐ CHANGE 1, VERIFICATION 1: do the sentinel's PUBLISHED core-HP readings
match the REPLAY's own core-HP series?

The sentinel reads the enemy core's HP with `get_hp` on a tile it can see and
drives the whole discipline off it.  If that number is wrong the plank is
noise.  Join `FIREDISC517 <rnd> ... hp <H>` (stderr, one line per sentinel per
round) to the replay's opp_core_hp at the same round.

⛔ THE NEGATIVE CONTROL IS IN THE SAME RUN, and it is what makes a high match
rate mean anything: the identical join is repeated at round offsets -2,-1,+1,+2.
A core whose HP never changes would match at EVERY offset, so a join that only
reports offset 0 has not been seen to check.  The report is the offset PROFILE.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game")
sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game/"
                   "scratchpad/s51_rush_autopsy")
from tape import Tape  # noqa: E402

OFFSETS = (-2, -1, 0, 1, 2)


def read_log(p: Path):
    out = []
    for line in p.read_text(errors="replace").splitlines():
        if not line.startswith("FIREDISC517"):
            continue
        f = line.split()
        try:
            rnd = int(f[1])
        except ValueError:
            continue
        hp = None
        for i in range(2, len(f) - 1):
            if f[i] == "hp":
                hp = f[i + 1]
                break
        if hp in (None, "None"):
            continue
        out.append((rnd, int(hp)))
    return out


def main():
    logdir, repdir = Path(sys.argv[1]), Path(sys.argv[2])
    tot = {o: [0, 0] for o in OFFSETS}
    brk = [0, 0]        # hp equals the START-of-round or the END-of-round value
    varied = 0
    games = 0
    for lp in sorted(logdir.glob("*.err")):
        tag = lp.stem
        rp = repdir / (tag + ".replay26")
        if not rp.exists():
            continue
        rows = read_log(lp)
        if not rows:
            continue
        our = 0 if tag.endswith("_A") else 1
        t = Tape(rp, our)
        series = [r["opp_core_hp"] for r in t.rows]
        games += 1
        if len(set(series)) > 1:
            varied += 1
        for rnd, hp in rows:
            for o in OFFSETS:
                j = rnd + o
                if 0 <= j < len(series):
                    tot[o][1] += 1
                    if series[j] == hp:
                        tot[o][0] += 1
            if 0 <= rnd < len(series):
                brk[1] += 1
                prev = series[rnd - 1] if rnd else 500
                if hp == series[rnd] or hp == prev:
                    brk[0] += 1
    print("games=%d (with a VARYING enemy-core HP series: %d)" % (games, varied))
    for o in OFFSETS:
        hit, n = tot[o]
        print("  offset %+d : %6d / %6d  = %.4f%s"
              % (o, hit, n, hit / n if n else -1,
                 "   <- the join under test" if o == 0 else ""))
    print("  BRACKET  : %6d / %6d  = %.4f   (the bot samples MID-round -- its "
          "read must equal the round's START or END value)"
          % (brk[0], brk[1], brk[0] / brk[1] if brk[1] else -1))


main()
