#!/usr/bin/env python3
"""s51 eviction autopsy parser.

Reads the per-game .err (FS stderr tags) + .out (fcode summary) and emits one
TSV row per game.  DRIVEN BOTH WAYS on a synthetic fixture (fixture.py) --
a parser that has only ever read zero has not been seen to count.

Columns
  game            <arm>-<map>-s<seed>-<seat>
  outcome         winner label from the fcode summary
  cond            'core_destroyed' | 'r1000' | 'other'
  end_r           the turn the match ended on
  evicts          (a)  FS EVICT lines = enemy bodies actually thrown
  evictor_r       (b)  round the RUNG-2 eviction launcher was BUILT (FS EVICTOR)
  first_lau_r     round any of our launchers first read inside FS_RING_DSQ of
                  the enemy core (this includes a FERRY launcher that happened
                  to land in-ring -- the distinction matters, see report)
  ring_rounds     DL lines' distinct rounds (raider at ring)
  dead_rounds     (c)  distinct rounds with >=1 enemy body on an OPEN orth seat
                  AND no in-ring launcher of ours
  dead_first      first such round
  close_r         (d)  first round orth_open == 0, else -1
  g_obs           dead_rounds in which healer-obs minimum (5) was unmet
  g_pend          dead_rounds in which the seal-wait (_fs_seal_pending) was on
  g_fund          dead_rounds passing obs+pend but failing the Ti floor
  g_open          dead_rounds passing all three (gate open, no build)
"""
import os
import re
import sys

FS_HEALER_MIN_OBS = 5
FS_EVICT_TI_FLOOR = 12
FS_SEAL_MARGIN = 6

DL = re.compile(
    r"^FS DL (\d+) id (\d+) role (\S+) orth (\d+) need (\d+) ebody (\d+) "
    r"lau (\d+) ti (\d+) lcost (\d+) bar (\d+) obs (\d+) hist (\d+) pend (-?\d+)")


def parse_game(err_path, out_path):
    evicts = 0
    evictor_r = -1
    close_r = -1
    first_lau_r = -1
    ring_rounds = set()
    dead = {}          # round -> (obs, pend, ti, lcost, need, bar)
    with open(err_path, errors="replace") as fh:
        for line in fh:
            if not line.startswith("FS "):
                continue
            if line.startswith("FS EVICT "):
                evicts += 1
                continue
            if line.startswith("FS EVICTOR "):
                r = int(line.split()[2])
                if evictor_r < 0 or r < evictor_r:
                    evictor_r = r
                continue
            m = DL.match(line)
            if not m:
                continue
            (rnd, _id, _role, orth, need, ebody, lau, ti,
             lcost, bar, obs, _hist, pend) = (int(x) if x.lstrip("-").isdigit()
                                              else x for x in m.groups())
            ring_rounds.add(rnd)
            if lau >= 1 and (first_lau_r < 0 or rnd < first_lau_r):
                first_lau_r = rnd
            if orth == 0 and (close_r < 0 or rnd < close_r):
                close_r = rnd
            if ebody >= 1 and lau == 0:
                dead[rnd] = (obs, pend, ti, lcost, need, bar)
    g_obs = g_pend = g_fund = g_open = 0
    for rnd, (obs, pend, ti, lcost, need, bar) in dead.items():
        if obs < FS_HEALER_MIN_OBS:
            g_obs += 1
        elif pend == 1:
            g_pend += 1
        elif ti < lcost + FS_EVICT_TI_FLOOR + need * bar + FS_SEAL_MARGIN:
            g_fund += 1
        else:
            g_open += 1
    outcome, cond, end_r = "?", "?", -1
    try:
        txt = open(out_path, errors="replace").read()
    except OSError:
        txt = ""
    m = re.search(r"Winner: (\S+)\s+\((.*), turn (\d+)\)", txt)
    if m:
        outcome, end_r = m.group(1), int(m.group(3))
        cond = m.group(2).replace(" ", "_")
    elif "Draw" in txt or "draw" in txt:
        outcome, cond = "draw", "r1000"
        m2 = re.search(r"turn (\d+)", txt)
        end_r = int(m2.group(1)) if m2 else 1000
    return dict(evicts=evicts, evictor_r=evictor_r, first_lau_r=first_lau_r,
                ring_rounds=len(ring_rounds), dead_rounds=len(dead),
                dead_first=min(dead) if dead else -1, close_r=close_r,
                g_obs=g_obs, g_pend=g_pend, g_fund=g_fund, g_open=g_open,
                outcome=outcome, cond=cond, end_r=end_r)


COLS = ["game", "outcome", "cond", "end_r", "evicts", "evictor_r",
        "first_lau_r", "ring_rounds", "dead_rounds", "dead_first", "close_r",
        "g_obs", "g_pend", "g_fund", "g_open"]


def main(d):
    print("\t".join(COLS))
    for f in sorted(os.listdir(d)):
        if not f.endswith(".err"):
            continue
        base = f[:-4]
        row = parse_game(os.path.join(d, f), os.path.join(d, base + ".out"))
        row["game"] = base
        print("\t".join(str(row[c]) for c in COLS))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else
         "scratchpad/s51_evict_autopsy/logs")
