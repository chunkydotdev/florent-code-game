#!/usr/bin/env python3
"""⭐⭐ THE DECOMPOSITION OF THE 81-ROUND `arrive -> sent` GAP (v518 change 2's
BEFORE baseline, and its mutant's readout).

v517's phase budget measured the gap and could not say what it was made of.
This joins, per game:

  * the REPLAY marks (`phase.marks` -> arrive, sent), which are engine-side
    facts and owe nothing to our own stdout; and
  * the bot-side GAP518 tape (stderr), one line per RING round carrying the
    first reason no forward sentinel was bought that round.

and buckets every round in the half-open window [arrive, sent) by reason.
Rounds in the window with NO GAP518 line are `NOBODY`: no raider of ours was
taking a ring turn at all (dead, walking in, or not yet spawned as the
replacement).  That bucket is a finding, not a hole -- v517 open item 1 says
the twin's real blocker is the raider's life, and this is the same question on
the FIRST sentinel.

⛔ GUARDS, DRIVEN BOTH WAYS (`--guard`):
  * a synthetic game with a known code histogram must return exactly it;
  * NOBODY must be computed as (window length - lines in window), and a
    synthetic game with a hole must report the hole;
  * a game that never buys a sentinel (sent = -1) must use [arrive, last_round]
    and must NOT be silently dropped;
  * a game that never arrives (arrive = -1) must be dropped and COUNTED;
  * ⛔ THE MUTATION CONTROL: re-running the fold with every code rewritten to
    GATE must move every cell -- a folder that ignores the code column would
    return the same table and is what this catches.
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game")
sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game/"
                   "scratchpad/s51_rush_autopsy")

CODES = ("GATE", "FUND", "SITE", "BUSY1", "BUSYW", "BUSY23", "OPEN",
         "DODGE", "RETREAT", "HAVE", "ERR")
LINE = re.compile(r"^GAP518 (\d+) id (\d+) code (\w+) ")


def read_gap(errpath: Path):
    """{round: code} -- FIRST line of a round wins (one raider in the fired
    config; with a crew the sealer runs first in unit order)."""
    out = {}
    if not errpath.exists():
        return out
    for line in open(errpath, errors="replace"):
        m = LINE.match(line)
        if not m:
            continue
        r = int(m.group(1))
        if r not in out:
            out[r] = m.group(3)
    return out


def fold_game(arrive, sent, last, gap):
    """Bucket [arrive, sent) (or [arrive, last] when sent < 0)."""
    if arrive < 0:
        return None
    end = sent if sent >= 0 else last + 1
    if end <= arrive:
        return Counter()
    c = Counter()
    for r in range(arrive, end):
        c[gap.get(r, "NOBODY")] += 1
    return c


def guard():
    ok = True
    gap = {10: "GATE", 11: "GATE", 12: "BUSY1", 14: "SITE"}
    c = fold_game(10, 15, 99, gap)
    want = Counter({"GATE": 2, "BUSY1": 1, "NOBODY": 1, "SITE": 1})
    if c != want:
        print("GUARD FAIL known histogram", c, want)
        ok = False
    # the hole is counted, not dropped
    if c["NOBODY"] != 1:
        print("GUARD FAIL hole", c)
        ok = False
    # never-bought game uses [arrive, last]
    c2 = fold_game(10, -1, 12, {10: "GATE"})
    if c2 != Counter({"GATE": 1, "NOBODY": 2}):
        print("GUARD FAIL never-bought", c2)
        ok = False
    # never-arrived game is dropped
    if fold_game(-1, 50, 99, {}) is not None:
        print("GUARD FAIL never-arrived not dropped")
        ok = False
    # empty window
    if fold_game(10, 10, 99, {}) != Counter():
        print("GUARD FAIL empty window")
        ok = False
    # ⛔ MUTATION CONTROL: rewriting every code must move the table
    mut = dict((k, "GATE") for k in gap)
    cm = fold_game(10, 15, 99, mut)
    if cm == c:
        print("GUARD FAIL mutation: folder ignores the code column")
        ok = False
    print("GUARD synthetic:", "PASS" if ok else "FAIL",
          "(mutation moved the table: %s -> %s)" % (dict(c), dict(cm)))
    return ok


def run(repdir: Path, logdir: Path, tsv: Path | None):
    from phase import marks
    from tape import Tape
    rows = []
    dropped = 0
    for p in sorted(repdir.glob("*.replay26")):
        tag = p.stem
        our = 0 if tag.endswith("_A") else 1
        t = Tape(p, our)
        a, s, f, k = marks(t.rows)
        last = t.rows[-1]["r"] if t.rows else 0
        gap = read_gap(logdir / (tag + ".err"))
        c = fold_game(a, s, last, gap)
        if c is None:
            dropped += 1
            continue
        # ⛔ THE `NOBODY` CROSS-CHECK, AND IT IS WHAT MAKES THAT BUCKET
        # READABLE.  `NOBODY` is "no GAP518 line", which is an ABSENCE, and an
        # absence has two possible causes: no raider was taking a ring turn, or
        # the instrument silently stopped.  The replay's own `near_bot` column
        # (our builder bots within d^2 <= 8 of their core, engine-side) settles
        # it: a NOBODY round with near_bot > 0 is an instrument hole, a NOBODY
        # round with near_bot == 0 is the finding.
        near = dict((r["r"], r["near_bot"]) for r in t.rows)
        end = s if s >= 0 else last + 1
        hole = sum(1 for r in range(a, end)
                   if r not in gap and near.get(r, 0) > 0)
        rows.append((tag, a, s, k, c, len(gap), hole))
    return rows, dropped


def _table(title, rows):
    import statistics as st
    tot = Counter()
    hole = 0
    for r in rows:
        tot += r[4]
        hole += r[6]
    n = sum(tot.values())
    print("  -- %s: %d games, %d rounds in window" % (title, len(rows), n))
    for code, v in sorted(tot.items(), key=lambda kv: -kv[1]):
        print("     %-8s %6d  %5.1f%%" % (code, v, 100.0 * v / max(1, n)))
    wins = [sum(r[4].values()) for r in rows]
    print("     window length: median %s  mean %.1f"
          % (st.median(wins) if wins else -1,
             (sum(wins) / len(wins)) if wins else -1))
    _nb = tot.get("NOBODY", 0)
    print("     NOBODY cross-check: %d of %d NOBODY rounds (%.1f%%) had a "
          "builder bot of ours inside d^2<=8 (replay-side) = residual.  %s"
          % (hole, _nb, 100.0 * hole / max(1, _nb),
             "<=5%% is the known seam (the bot logs at ITS turn, the replay "
             "row is end-of-round state, so the round a body first steps "
             "inside d^2<=8 has no line); above that, do not read"))
    return tot


def report(name, rows, dropped):
    print("\n=== GAP DECOMPOSITION  %s   games=%d (dropped, never arrived: %d)"
          % (name, len(rows), dropped))
    tot = _table("ALL GAMES  [arrive, sent) or [arrive, end]", rows)
    # ⭐ THE CUT THAT MATTERS.  Pooling a game that NEVER buys a sentinel with
    # one that buys at r76 lets a single 900-round window dominate every cell,
    # and the two are different questions: "how long did the purchase take"
    # vs "did it happen at all".
    buy = [r for r in rows if r[2] >= 0]
    nobuy = [r for r in rows if r[2] < 0]
    print()
    _table("BOUGHT A FORWARD SENTINEL  [arrive, sent)", buy)
    print()
    _table("NEVER BOUGHT ONE  [arrive, end]", nobuy)
    return tot


if __name__ == "__main__":
    if not guard():
        sys.exit(1)
    if sys.argv[1] == "--guard":
        sys.exit(0)
    name = sys.argv[1]
    allrows, drop = [], 0
    for d in sys.argv[2:]:
        d = Path(d)
        r, dr = run(d / "rep", d / "log", None)
        allrows += r
        drop += dr
    report(name, allrows, drop)
    print("\n    per-game (tag arrive sent kill | top codes):")
    for tag, a, s, k, c, _n, _h in sorted(allrows)[:40]:
        top = " ".join("%s=%d" % kv for kv in
                       sorted(c.items(), key=lambda kv: -kv[1])[:4])
        print("      %-22s a=%-4s s=%-5s k=%-5s %s" % (tag, a, s, k, top))
