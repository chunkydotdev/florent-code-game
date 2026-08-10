#!/usr/bin/env python3
"""Read a LIVE-UNRATED LEG in the programme's currency, from the platform.

    .venv/bin/python tools/leg_read.py MATCHID [MATCHID ...]
    .venv/bin/python tools/leg_read.py --file scratchpad/loki11_leg_ids.txt
    .venv/bin/python tools/leg_read.py --file A.txt --vs B.txt     # paired compare

WHY THIS EXISTS. `fcode match info` reports `scoreA`/`scoreB`, which are
PLATFORM-SEAT columns, not statements about us. On 2026-08-10 a lane published
an aggregate of 7-18 that was really 14-11 because two matches where we sat in
seat B were read straight off `scoreA`. **This tool never touches scoreA/scoreB.
It joins on `winnerId == OUR_TEAM_ID`, per game.** That is the whole reason it is
a file instead of a one-liner.

WHAT IT REPORTS, and the order is deliberate — mechanism and currency BEFORE
win rate, because `PROGRAMME.md` says win rate is not a verdict:

  * r1000_rate   -- under R1000_IS_DEFEAT this is a LOSS RATE, counting
                    tiebreak WINS as losses.
  * core_kill_share -- ours / all games. THE DEFINITION IS PRINTED WITH THE
                    NUMBER, every time, because an audit on 2026-08-10 found
                    THREE definitions of this statistic in live use, two of
                    which give opposite signs on the same 384 games. A currency
                    without its denominator attached is how that happened.
  * time-to-kill vs KILL_WINDOW_RND, ours and theirs, with the per-map split.

Seats are printed per opponent. A paired comparison whose seat mix differs from
its control is NOT paired, and this prints the mix so that is visible rather
than assumed.
"""
from __future__ import annotations

import json
import math
import statistics
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FCODE = str(ROOT / ".venv" / "bin" / "fcode")
OUR_TEAM_ID = "379a5d80-9921-4c9e-949b-f9b1dcba16be"   # OpenSverige
KILL_WINDOW_RND = 250


def match_info(mid: str) -> dict | None:
    r = subprocess.run([FCODE, "match", "info", mid, "--json"],
                       capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return None


def ids_from_file(p: Path) -> list[str]:
    out = []
    for line in p.read_text().splitlines():
        if '"matchId"' in line:
            out.append(json.loads(line[line.index("{"):])["matchId"])
    return out


def collect(mids: list[str]) -> tuple[list[dict], list[str]]:
    games, pending = [], []
    for mid in mids:
        d = match_info(mid)
        if not d:
            pending.append(f"{mid} UNREADABLE")
            continue
        m = d["match"]
        if m["status"] != "complete" or not d["games"]:
            pending.append(f"{m.get('teamBName') or mid} {m['status']} "
                           f"({len(d['games'])}/5 games)")
        we_are_a = m["teamAId"] == OUR_TEAM_ID
        opp = m["teamBName"] if we_are_a else m["teamAName"]
        for g in d["games"]:
            games.append({
                "opp": opp, "seat": "A" if we_are_a else "B",
                "map": g["mapName"], "turns": g["turnsPlayed"],
                "cond": g["winCondition"],
                "we_won": g["winnerId"] == OUR_TEAM_ID,
            })
    return games, pending


def report(games: list[dict], label: str) -> dict:
    n = len(games)
    if not n:
        print(f"{label}: no completed games")
        return {}
    r1000 = [g for g in games if g["turns"] >= 1000]
    kills = [g for g in games if g["cond"] == "core_destroyed"]
    ours = [g for g in kills if g["we_won"]]
    theirs = [g for g in kills if not g["we_won"]]
    wins = [g for g in games if g["we_won"]]

    print(f"\n=== {label}  (n={n} games) ===")
    print(f"  r1000 rate (DEFEAT)   {len(r1000):>3}/{n} = {len(r1000)/n:6.1%}")
    print(f"  core_kill_share       {len(ours):>3}/{n} = {len(ours)/n:6.1%}"
          f"   [definition: OUR kills / ALL games]")
    print(f"     ...their kills     {len(theirs):>3}/{n} = {len(theirs)/n:6.1%}")
    print(f"  win rate              {len(wins):>3}/{n} = {len(wins)/n:6.1%}"
          f"   [NOT A VERDICT -- PROGRAMME.md]")
    if ours:
        t = [g["turns"] for g in ours]
        print(f"  our kill turns        median {statistics.median(t):>5.0f}  "
              f"range {min(t)}-{max(t)}  "
              f"<= {KILL_WINDOW_RND}: {len([x for x in t if x <= KILL_WINDOW_RND])}/{len(t)}")
    if theirs:
        t = [g["turns"] for g in theirs]
        print(f"  THEIR kill turns      median {statistics.median(t):>5.0f}  "
              f"range {min(t)}-{max(t)}")
    seats = {}
    for g in games:
        seats.setdefault(g["opp"], g["seat"])
    print(f"  seat mix              {sorted(seats.items())}")

    # PER-OPPONENT SPLIT (added s28 on the cross-lane audit's recommendation).
    # collect() has built "opp" per game since this tool existed and report()
    # threw it away, so every currency number this project published was a
    # POOLED read over cells nobody had decomposed. The decomposition that
    # exposed three inert cells was eventually done BY HAND, into a prereg,
    # AFTER two separate 18pp claims had already died on the pooled number.
    # A floor cell and a ceiling cell contribute denominator and no information;
    # printing them next to the pooled figure is the whole point.
    print("  per opponent (core_kill_share; admission band 0.20-0.80):")
    cells = {}
    for op in sorted({g["opp"] for g in games}):
        oo = [g for g in games if g["opp"] == op]
        ok = [g for g in oo if g["we_won"] and g["cond"] == "core_destroyed"]
        share = len(ok) / len(oo)
        cells[op] = (share, len(oo))
        if len(oo) < 5:
            tag = "(n<5, no read)"
        elif share < 0.20:
            tag = "** FLOOR -- inert, contributes denominator only **"
        elif share > 0.80:
            tag = "** CEILING -- inert, contributes denominator only **"
        else:
            tag = "live"
        print(f"    {op:<20} {len(ok):>3}/{len(oo):<4} = {share:6.1%}  {tag}")
    # BAND IS INCLUSIVE: the prereg admits a cell whose share is IN
    # [0.20, 0.80]. My first pass used strict `<=` / `>=` and threw out
    # cells sitting EXACTLY on 0.80 -- on the LOKI-16 treatment arm that
    # is 12/15 twice, so the effective n read 30/75 instead of 60/75 and
    # the MDE was overstated. An admission rule must match the prereg's
    # brackets exactly; off-by-one on a boundary is a silent re-scoping
    # of the instrument.
    live_n = sum(n_ for s, n_ in cells.values() if 0.20 <= s <= 0.80 and n_ >= 5)
    if live_n < n:
        print(f"    EFFECTIVE n = {live_n}/{n} games sit on cells that can move"
              f"  ({live_n/n:.0%} of the denominator carries the information)")
    print("  per map:")
    for mp in sorted({g["map"] for g in games}):
        mm = [g for g in games if g["map"] == mp]
        ok = [g for g in mm if g["we_won"] and g["cond"] == "core_destroyed"]
        print(f"    {mp:<12} kills {len(ok)}/{len(mm)}  turns {sorted(g['turns'] for g in mm)}")
    return {"n": n, "r1000": len(r1000)/n, "cks": len(ours)/n,
            "win": len(wins)/n, "kills": len(ours),
            "cells": cells, "live_n": live_n}


def main(argv: list[str]) -> int:
    a_file = b_file = None
    bar = None
    mids: list[str] = []
    i = 0
    while i < len(argv):
        if argv[i] == "--bar":
            bar = float(argv[i + 1]) / 100.0; i += 2
        elif argv[i] == "--file":
            a_file = Path(argv[i + 1]); i += 2
        elif argv[i] == "--vs":
            b_file = Path(argv[i + 1]); i += 2
        else:
            mids.append(argv[i]); i += 1

    if a_file:
        mids = ids_from_file(a_file)
    if not mids:
        print(__doc__)
        return 2

    games, pending = collect(mids)
    a = report(games, a_file.name if a_file else "LEG")
    if pending:
        print("\n  ** NOT YET COMPLETE -- these numbers are PARTIAL:")
        for p in pending:
            print(f"     {p}")

    if b_file:
        bgames, bpending = collect(ids_from_file(b_file))
        b = report(bgames, b_file.name)
        if bpending:
            print("\n  ** control incomplete:")
            for p in bpending:
                print(f"     {p}")
        if a and b:
            print(f"\n=== PAIRED DELTA ({a_file.name} minus {b_file.name}) ===")
            print(f"  core_kill_share  {a['cks']:.1%} - {b['cks']:.1%} = "
                  f"{(a['cks']-b['cks'])*100:+.1f}pp   PRIMARY")
            print(f"  r1000 rate       {a['r1000']:.1%} - {b['r1000']:.1%} = "
                  f"{(a['r1000']-b['r1000'])*100:+.1f}pp")
            print(f"  n {a['n']} vs {b['n']}"
                  + ("   ** DENOMINATORS DIFFER -- not a clean pair **"
                     if a["n"] != b["n"] else ""))
            # COMPUTED MDE (s28). This line used to be the hardcoded string
            # "with n~25 per arm this resolves ~20pp at best" -- which printed
            # the SAME sentence at n=25 and at n=150. A constant column
            # validates anything; this one reassured two legs that had already
            # spent their power. Now it is computed, and it is computed on the
            # LIVE cells, because a floor or ceiling cell adds denominator and
            # no information: the audit's worked case is a true 18pp on live
            # cells showing as 7.2pp pooled at ~20% power, which is exactly the
            # p=0.303 this project has now produced twice.
            # 2.802 = z(0.975) + z(0.80), two-sided alpha 0.05 at 80% power;
            # 0.25 = p(1-p) at its worst case.
            for lbl, arm in (("treatment", a), ("control", b)):
                if arm["live_n"] < arm["n"]:
                    print(f"  {lbl:<10} effective n {arm['live_n']}/{arm['n']}"
                          f"  ({arm['n'] - arm['live_n']} games on inert cells)")
            n1, n2 = a["live_n"] or a["n"], b["live_n"] or b["n"]
            mde = 2.802 * math.sqrt(0.25 * (1 / n1 + 1 / n2))
            print(f"  MDE (80% power, a=0.05, on live cells n={n1}/{n2})"
                  f"   {mde*100:.1f}pp")
            # --bar IS DENOMINATED IN THE PRIMARY CURRENCY (core_kill_share
            # percentage points) AND IN NOTHING ELSE. A plank whose
            # pre-registered bar is a MECHANISM statistic -- LOKI-16's ring
            # coverage, LOKI-14's undamaged-removal count -- must not be fed to
            # this flag: the MDE printed above is the MDE of the currency, and
            # comparing a coverage bar to it is a units error wearing a
            # verdict's clothes. Use it for currency bars; resolve mechanism
            # bars on their own estimator, named in the prereg.
            if bar is not None:
                if bar < mde:
                    print(f"  ** BAR BELOW MDE -- THIS LEG CANNOT RESOLVE ITS "
                          f"OWN CLAIM ** (bar {bar*100:.1f}pp < MDE {mde*100:.1f}pp)")
                else:
                    print(f"  bar {bar*100:.1f}pp is above MDE -- resolvable at this n")
            else:
                print("  (pass --bar <pp> to check the leg against its own "
                      "pre-registered effect size)")
            dead = [f"{op} {s:.0%}" for op, (s, n_) in
                    {**b["cells"], **a["cells"]}.items()
                    if n_ >= 5 and not (0.20 <= s <= 0.80)]
            if dead:
                print(f"  inert cells in this pair: {', '.join(sorted(dead))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
