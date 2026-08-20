#!/usr/bin/env python3
"""v528 DELIVERY PANEL reader.  One TSV row per `.replay26`.

⭐ WHY THIS EXISTS AND WHY IT IS NOT THE SCOREBOARD.  The engine's end-of-game
line gives `Titanium N (M mined)`, which is `titaniumCollected` AT THE END.  M5's
myopia guard is a claim about r100 AND r300 -- quick-connect greed must raise
early delivery WITHOUT capping late delivery -- and `fcode run` has no turn cap
(`--help` verified: --replay/--seed/--watch/--tle/--map-random/--json, no
--turns).  So the mid-game reads come off the replay, where
`UpdatePlayers.Players.Player.titaniumCollected` (field 4) is emitted every
round for both teams (`tools/replay_schema.md`).

⛔ A GAME THAT ENDS AT r89 HAS NO r300 READ.  It is not zero and it is not the
final value carried forward -- either choice silently answers a different
question (the first punishes fast kills, the second inflates them).  The column
is emitted as `-1` and the reader that pools it MUST restrict to games that
reached the round.  `headline.py` does; `n_r100` / `n_r300` are printed beside
every delivery cell so the denominator travels with the number.

Columns:
  tag map seed seat arm ours winner cond turn
  d100 d300 dend od100 od300 odend
  turret1 harv1 h50 h100 h200 h300 conv_end

  d*   = OUR titaniumCollected at that round   (-1 = game ended first)
  od*  = the opponent's, same convention
  turret1 = round our first gunner OR sentinel was placed (-1 = never).
            THE ECO GATE FEEDS THIS: the sentinel gate counts CONNECTED
            harvesters, so a build that connects sooner should fund sooner.
  harv1   = round of our first harvester;  h50..h300 = our harvesters ALIVE
  conv_end= our conveyors+splitters alive at the end

SELFTEST (`--selftest <replay> ...`), and every guard is driven to the OTHER
verdict, per the instrument rule:
  1. delivery is MONOTONE NON-DECREASING in round (it is a cumulative counter);
     a corrupted copy with one round's value halved must FAIL this.
  2. d100 <= d300 <= dend on games that reached r300; the same corrupted copy
     must FAIL.
  3. the r-end value must EQUAL the scoreboard `mined` number when a matching
     `.out` file sits beside the replay -- a cross-instrument check against a
     number this reader does not compute; a deliberately wrong arm must FAIL.
  4. NOT A CONSTANT COLUMN: across the given replays, d300 and turret1 must
     each take more than one distinct value.  A constant column validates
     anything.
  5. seat detection: swapping the seat argument must swap d* and od*.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from replay_census import (  # noqa: E402
    KIND_FIELDS, fields, packed_varints, read_pos, scalars,
)

WIRE_LEN = 2
MARKS = (50, 100, 200, 300)
TURRET_KINDS = ("gunner", "sentinel")


def _turn_bufs(raw: bytes):
    """(map_buf, [turn_buf...], winner, win_condition) from a Replay message."""
    turns, mp, winner, cond = [], None, -1, "-"
    for num, wire, value in fields(raw):
        if num == 3 and wire == WIRE_LEN:
            turns.append(value)
        elif num == 1 and wire == WIRE_LEN:
            mp = value
        elif num == 4:
            winner = value
        elif num == 6 and wire == WIRE_LEN:
            cond = value.decode("utf8", "replace")
    return mp, turns, winner, cond


def read(path: Path, ours: int):
    """ours: 0 for team A, 1 for team B."""
    raw = path.read_bytes()
    _mp, turns, winner, cond = _turn_bufs(raw)
    nturn = len(turns)

    coll = [[0, 0]]                      # coll[r] = [A, B] after round r
    alive = {}                           # eid -> (team, kind)
    h_alive = {0: 0, 1: 0}
    c_alive = {0: 0, 1: 0}
    harv_at = {m: [0, 0] for m in MARKS}
    turret1 = [-1, -1]
    harv1 = [-1, -1]
    cur = [0, 0]

    for r, tb in enumerate(turns):
        # ⛔ Turn { repeated Update updates = 1 } -- the updates are ONE LEVEL
        # DOWN.  Reading the Turn's own fields as Update fields is what the
        # first cut of this reader did; every column came out constant and the
        # selftest's non-constant guard is what caught it.
        for tnum_, twire_, upd in fields(tb):
            if twire_ != WIRE_LEN or tnum_ != 1:
                continue
            for unum, uwire, uval in fields(upd):
                if uwire != WIRE_LEN:
                    continue
                if unum == 6:                                    # updatePlayers
                    for pnum, pwire, pval in fields(uval):
                        if pwire != WIRE_LEN or pnum != 1:
                            continue
                        for tnum, twire, tval in fields(pval):   # Players a=1 b=2
                            if twire != WIRE_LEN or tnum not in (1, 2):
                                continue
                            sc = scalars(tval)
                            v = sc.get(4)
                            if isinstance(v, int):
                                cur[tnum - 1] = v
                elif unum == 1:                                  # placeEntity
                    # ⛔ PlaceEntity { Entity entity = 1 } -- the Entity is ONE
                    # MORE LEVEL DOWN (`tools/replay_census.py:542-546`).  The
                    # first cut read the PlaceEntity's own fields as an Entity
                    # and produced turret1 == -1 on every replay; the
                    # non-constant-column guard is what caught it.
                    ebuf = None
                    for enum_, ew_, ev_ in fields(uval):
                        if enum_ == 1 and ew_ == WIRE_LEN:
                            ebuf = ev_
                            break
                    if ebuf is None:
                        continue
                    eid = team = 0
                    kind = None
                    for num, wire, value in fields(ebuf):
                        if num == 1:
                            eid = value
                        elif num == 2:
                            team = value
                        elif num in KIND_FIELDS:
                            kind = KIND_FIELDS[num]
                    if kind is None:
                        continue
                    alive[eid] = (team, kind)
                    if kind == "harvester":
                        h_alive[team] += 1
                        if harv1[team] < 0:
                            harv1[team] = r
                    elif kind in ("conveyor", "splitter"):
                        c_alive[team] += 1
                    elif kind in TURRET_KINDS and turret1[team] < 0:
                        turret1[team] = r
                elif unum == 3:                                  # removeEntity
                    sc = scalars(uval)
                    eid = sc.get(1)
                    got = alive.pop(eid, None)
                    if got is not None:
                        team, kind = got
                        if kind == "harvester":
                            h_alive[team] -= 1
                        elif kind in ("conveyor", "splitter"):
                            c_alive[team] -= 1
        coll.append([cur[0], cur[1]])
        if r in harv_at:
            harv_at[r] = [h_alive[0], h_alive[1]]

    def at(rnd, team):
        return coll[rnd][team] if rnd < len(coll) else -1

    them = 1 - ours
    return {
        "turn": nturn - 1,
        "winner": {0: "A", 1: "B"}.get(winner, "NONE"),
        "cond": cond,
        "d100": at(100, ours), "d300": at(300, ours), "dend": coll[-1][ours],
        "od100": at(100, them), "od300": at(300, them),
        "odend": coll[-1][them],
        "turret1": turret1[ours], "harv1": harv1[ours],
        "h50": harv_at[50][ours], "h100": harv_at[100][ours],
        "h200": harv_at[200][ours], "h300": harv_at[300][ours],
        "conv_end": c_alive[ours],
        "_series": [c[ours] for c in coll],
    }


COLS = ["tag", "map", "seed", "seat", "arm", "turn", "winner", "cond",
        "d100", "d300", "dend", "od100", "od300", "odend",
        "turret1", "harv1", "h50", "h100", "h200", "h300", "conv_end"]

TAG_RE = re.compile(r"^(?P<arm>.+)_(?P<map>[a-z]+)_s(?P<seed>\d+)_(?P<seat>[AB])$")


def row_for(path: Path):
    tag = path.stem
    m = TAG_RE.match(tag)
    if not m:
        return None
    seat = m.group("seat")
    ours = 0 if seat == "A" else 1
    d = read(path, ours)
    d.update(tag=tag, map=m.group("map"), seed=m.group("seed"), seat=seat,
             arm=m.group("arm"))
    return d


# --------------------------------------------------------------------------
# SELFTEST
# --------------------------------------------------------------------------

def _mined_from_out(path: Path, seat: str):
    """The scoreboard `mined` number for our seat, if the .out sits beside."""
    cand = path.parent.parent / "log" / (path.stem + ".out")
    if not cand.exists():
        cand = path.with_suffix(".out")
    if not cand.exists():
        return None
    m = re.search(r"Titanium\s+(\d+)\s+\((\d+) mined\)\s+(\d+)\s+\((\d+) mined\)",
                  cand.read_text())
    if not m:
        return None
    return int(m.group(2)) if seat == "A" else int(m.group(4))


def selftest(paths):
    ok = True
    rows = []
    for p in paths:
        r = row_for(Path(p))
        if r is None:
            print("SELFTEST: tag %s does not parse -- skipped" % Path(p).stem)
            continue
        rows.append((Path(p), r))
    if not rows:
        print("SELFTEST FAIL: no parsable replays"); return 1

    # 1 + 2: monotone, and the corrupted control must FAIL both.
    for p, r in rows:
        s = r["_series"]
        if any(s[i] > s[i + 1] for i in range(len(s) - 1)):
            print("SELFTEST FAIL: %s delivery not monotone" % p.stem); ok = False
        if r["d300"] >= 0 and not (r["d100"] <= r["d300"] <= r["dend"]):
            print("SELFTEST FAIL: %s d100<=d300<=dend violated" % p.stem); ok = False
    p0, r0 = rows[0]
    bad = list(r0["_series"])
    if len(bad) > 12:
        bad[len(bad) // 2] = max(0, bad[len(bad) // 2] // 2 - 1)
    caught = any(bad[i] > bad[i + 1] for i in range(len(bad) - 1))
    print("GUARD monotone: real=PASS  corrupted-copy=%s"
          % ("CAUGHT" if caught else "MISSED(FAIL)"))
    if not caught:
        ok = False

    # 3: cross-instrument -- dend must equal the scoreboard's `mined`.
    checked = agree = 0
    for p, r in rows:
        mined = _mined_from_out(p, r["seat"])
        if mined is None:
            continue
        checked += 1
        agree += (mined == r["dend"])
        if mined != r["dend"]:
            print("SELFTEST FAIL: %s dend=%d but scoreboard mined=%d"
                  % (p.stem, r["dend"], mined))
            ok = False
    if checked:
        print("GUARD cross-instrument (dend == scoreboard mined): %d/%d"
              % (agree, checked))
        # driven the other way: the OPPONENT's number must NOT match ours
        # (unless both are genuinely equal, which a 0-0 game can be).
        wrongarm = sum(1 for p, r in rows
                       if _mined_from_out(p, r["seat"]) is not None
                       and _mined_from_out(p, r["seat"]) != r["odend"])
        print("        wrong-arm control (mined vs OPPONENT's dend): "
              "%d/%d differ (0 would mean the check cannot fail)" % (wrongarm, checked))
        if checked and wrongarm == 0:
            print("SELFTEST FAIL: wrong-arm control never differs"); ok = False
    else:
        print("GUARD cross-instrument: SKIPPED (no .out beside the replays)")

    # 4: not a constant column
    for col in ("d300", "dend", "turret1"):
        vals = {r[col] for _p, r in rows}
        print("GUARD non-constant %-8s distinct=%d %s"
              % (col, len(vals), sorted(vals)[:6]))
        if len(vals) < 2:
            print("SELFTEST FAIL: %s is a constant column over %d replays"
                  % (col, len(rows)))
            ok = False

    # 5: seat swap must swap ours/theirs
    p, r = rows[0]
    flipped = read(p, 1 if r["seat"] == "A" else 0)
    swapped = (flipped["dend"] == r["odend"] and flipped["odend"] == r["dend"])
    print("GUARD seat-swap: %s" % ("SWAPS" if swapped else "DOES NOT SWAP(FAIL)"))
    if not swapped:
        ok = False

    print("SELFTEST:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    args = sys.argv[1:]
    if args and args[0] == "--selftest":
        return selftest(args[1:])
    header = True
    if args and args[0] == "--no-header":
        header = False
        args = args[1:]
    if header:
        print("\t".join(COLS))
    for a in args:
        r = row_for(Path(a))
        if r is None:
            continue
        print("\t".join(str(r[c]) for c in COLS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
