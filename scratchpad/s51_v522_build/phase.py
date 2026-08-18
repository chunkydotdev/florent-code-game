#!/usr/bin/env python3
"""PHASE BUDGET — where the rounds go between spawn and the kill.

Added on the s51 mid-build KILL_TARGET directive (median kill <= r180, tracked
metric = share of kills by r200).  Replay-side only.

Per game, the four marks:
  arrive   first round a BUILDER BOT of ours is inside d^2 <= 8 of the enemy
           core centre -- the ring.  (`Tape.near_bot`, the same test the
           autopsy used.)
  sent     first round a FORWARD sentinel of ours (d^2 <= 40) is alive.
  funded   first round a forward sentinel of ours is alive AND team ammunition
           is >= 10, i.e. the first round the turret could actually SHOOT.
           ⭐ This is the SENTBEAT + ammo join in replay coordinates: it is the
           quantity v516's GLOBALSENT moved (funding 0.249 -> 0.421) and the
           one the kill clock actually starts on.
  kill     the round the enemy core reaches 0 (or -1 if it never does).

and the three gaps: arrive, sent-arrive, funded-sent, kill-funded.

⛔ GUARDS, DRIVEN BOTH WAYS (--guard):
  * a synthetic tape with no bot ever near, no sentinel and no ammo must report
    all four marks as -1, NOT as 0.  ("never happened" and "happened at round
    0" are different findings and a -1/0 confusion would silently move every
    median.)
  * a synthetic tape with each mark at a known round must return exactly those
    rounds, and the ORDER of the marks must be recovered.
  * REAL DATA: `kill` from this walker must agree with the grid TSV's
    `Core destroyed` turn for the games we won, and must be -1 for every game
    the TSV does not call a core-destroyed win of ours.  A disagreement is an
    instrument alarm, not a row.
"""
from __future__ import annotations

import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game")
sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game/"
                   "scratchpad/s51_rush_autopsy")
from tape import Tape  # noqa: E402

AMMO_SHOT = 10


def marks(rows):
    """(arrive, sent, funded, kill) from a Tape row list.  -1 = never."""
    arrive = sent = funded = kill = -1
    for r in rows:
        if arrive < 0 and r["near_bot"] > 0:
            arrive = r["r"]
        if sent < 0 and r["near_sent"] > 0:
            sent = r["r"]
        if funded < 0 and r["near_sent"] > 0 and r["our_ammo"] >= AMMO_SHOT:
            funded = r["r"]
        if kill < 0 and r["opp_core_hp"] <= 0:
            kill = r["r"]
    return arrive, sent, funded, kill


def guard():
    ok = True
    empty = [{"r": i, "near_bot": 0, "near_sent": 0, "our_ammo": 0,
              "opp_core_hp": 500} for i in range(100)]
    if marks(empty) != (-1, -1, -1, -1):
        print("GUARD FAIL: empty tape did not report -1", marks(empty))
        ok = False
    known = []
    for i in range(100):
        known.append({"r": i,
                      "near_bot": 1 if i >= 20 else 0,
                      "near_sent": 1 if i >= 40 else 0,
                      "our_ammo": 50 if i >= 55 else 0,
                      "opp_core_hp": 0 if i >= 80 else 500})
    if marks(known) != (20, 40, 55, 80):
        print("GUARD FAIL: known tape", marks(known))
        ok = False
    # ammo present BEFORE the sentinel must not make `funded` precede `sent`
    early = []
    for i in range(100):
        early.append({"r": i, "near_bot": 0,
                      "near_sent": 1 if i >= 40 else 0,
                      "our_ammo": 999,
                      "opp_core_hp": 500})
    if marks(early)[2] != 40:
        print("GUARD FAIL: funded preceded sent", marks(early))
        ok = False
    print("GUARD synthetic:", "PASS" if ok else "FAIL")
    return ok


def run(repdir: Path, tsv: Path | None):
    want = {}
    if tsv and tsv.exists():
        for line in open(tsv):
            f = line.rstrip("\n").split("\t")
            if len(f) < 8 or f[0] == "tag":
                continue
            want[f[0]] = (f[4], f[6], int(f[7]))
    out, alarms, offs = [], 0, {}
    for p in sorted(repdir.glob("*.replay26")):
        tag = p.stem
        our = 0 if tag.endswith("_A") else 1
        t = Tape(p, our)
        a, s, f, k = marks(t.rows)
        if tag in want:
            ours, cond, turn = want[tag]
            won = ours == "US" and cond.startswith("Core destroyed")
            if not won:
                if k != -1:
                    alarms += 1
                    if alarms <= 3:
                        print("ALARM: walker found a kill the TSV does not",
                              tag, k, file=sys.stderr)
            elif k < 0:
                alarms += 1
                if alarms <= 3:
                    print("ALARM: TSV says core destroyed, walker found none",
                          tag, file=sys.stderr)
            else:
                # ⛔ THE ENGINE'S "turn N" IS 1-INDEXED AND THE REPLAY'S ROUND
                # INDEX IS 0-INDEXED, so a CONSTANT offset of +1 is the correct
                # answer, not a mismatch.  What would be an alarm is an
                # INCONSISTENT offset -- so the offset histogram is reported and
                # anything other than a single value fails.
                offs[turn - k] = offs.get(turn - k, 0) + 1
        out.append((tag, a, s, f, k))
    return out, alarms, offs


def fold(name, rows):
    def med(v):
        v = [x for x in v if x >= 0]
        return st.median(v) if v else -1
    a = [r[1] for r in rows]
    s = [r[2] for r in rows]
    f = [r[3] for r in rows]
    k = [r[4] for r in rows]
    gap_as = [r[2] - r[1] for r in rows if r[1] >= 0 and r[2] >= 0]
    gap_sf = [r[3] - r[2] for r in rows if r[2] >= 0 and r[3] >= 0]
    gap_fk = [r[4] - r[3] for r in rows if r[3] >= 0 and r[4] >= 0]
    n = len(rows)
    print("%-12s n=%3d | med ARRIVE=%4s (%d/%d games) med SENT=%4s (%d) "
          "med FUNDED=%4s (%d) med KILL=%4s (%d)"
          % (name, n, med(a), sum(1 for x in a if x >= 0), n,
             med(s), sum(1 for x in s if x >= 0),
             med(f), sum(1 for x in f if x >= 0),
             med(k), sum(1 for x in k if x >= 0)))
    print("%-12s      | med GAPS: spawn->arrive %4s | arrive->sent %4s | "
          "sent->funded %4s | funded->kill %4s"
          % ("", med(a), st.median(gap_as) if gap_as else -1,
             st.median(gap_sf) if gap_sf else -1,
             st.median(gap_fk) if gap_fk else -1))


if __name__ == "__main__":
    if not guard():
        sys.exit(1)
    if sys.argv[1] == "--guard":
        sys.exit(0)
    name = sys.argv[1]
    allrows, alarms, OFF = [], 0, {}
    for d in sys.argv[2:]:
        d = Path(d)
        tsv = None
        _stem = d.name.replace("rep", "", 1)
        for cand in (d.parent / "res.tsv",
                     d.parent / (_stem + ".tsv"),
                     d.parent / ("v" + _stem + ".tsv")):
            if cand.exists():
                tsv = cand
                break
        r, al, off = run(d, tsv)
        allrows += r
        alarms += al
        for kk, vv in off.items():
            OFF[kk] = OFF.get(kk, 0) + vv
    print("kill-mark cross-check vs the grid TSV: alarms %d / %d games; "
          "tsv_turn - walker_round histogram %s%s"
          % (alarms, len(allrows), OFF,
             "  <- SINGLE VALUE = consistent indexing" if len(OFF) == 1
             else "  <- ⛔ INCONSISTENT, DO NOT READ"))
    fold(name, allrows)
