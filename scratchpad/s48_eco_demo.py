#!/usr/bin/env python3
"""s48 BUILDER demo decoder: does an eco plank FIRE, and does the eco stand up?

Runs one local match and reads the replay for the three things the s48 trees
are built to move, plus the two things that would disqualify any of them:

  * HARVESTER CONNECT: every harvester built, the round it first becomes
    STRUCTURALLY CONNECTED to its own Core (harvester -> acceptor -> conveyor
    chain -> Core footprint), and the never-connected share.  This is the
    study's 25.1% metric, recomputed locally.
  * OSCILLATION: A->B->A reversals -- a builder move on round r whose delta is
    the exact negation of its own move on round r-1.  Counted per team and
    divided by that team's total moves.
  * DOSE TAGS: the per-plank print() tags (EC1DEFER/EC1ADOPT, FR2SKIP/FR2FORCE,
    RS3PICK) read out of the replay's BotOutput.stdout, which IS populated
    locally (it is stripped only on platform-downloaded replays).
  * TLE and TRACEBACKS: any of either is a build failure, not a result.

⛔ NOT A VERDICT INSTRUMENT.  One game is a demo that a mechanism fires. It is
not a screen and nothing here is a bar.

Usage:
    python3 scratchpad/s48_eco_demo.py <bot_a> <bot_b> <map> [--seed N] [--tag T]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from replay_census import fields, read_pos, scalars, parse_entity  # noqa: E402

FCODE = ROOT / ".venv" / "bin" / "fcode"

# Direction enum -> (dx, dy). Compass: (0,0) is NW, y grows south.
DELTA = {
    0: (0, 0), 1: (0, -1), 2: (1, -1), 3: (1, 0), 4: (1, 1),
    5: (0, 1), 6: (-1, 1), 7: (-1, 0), 8: (-1, -1),
}
CARD = ((0, -1), (1, 0), (0, 1), (-1, 0))
BELT = ("conveyor", "splitter")


def run_match(bot_a, bot_b, map_path, seed, replay_path, tle=10):
    cmd = [str(FCODE), "run", bot_a, bot_b, str(map_path), "--seed", str(seed),
           "--tle", str(tle), "--json", "--replay", str(replay_path)]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    result = None
    for line in reversed(proc.stdout.splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                result = json.loads(line)
                break
            except json.JSONDecodeError:
                continue
    tb = proc.stderr.count("Traceback (most recent call last)")
    return result, tb, proc.stderr


class World:
    """Live building map + core footprints, replayed round by round."""

    def __init__(self, cores, width, height):
        self.w, self.h = width, height
        self.b = {}                       # (x,y) -> (team, kind, direction)
        self.core_tiles = {0: set(), 1: set()}
        for c in cores:
            x, y = c["pos"]
            self.core_tiles[c["team"]] |= {(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)}
            for t in self.core_tiles[c["team"]]:
                self.b[t] = (c["team"], "core", None)

    def out(self, xy, kind, d):
        if kind != "conveyor" or d is None:
            return None
        dx, dy = DELTA.get(d, (0, 0))
        if (dx, dy) == (0, 0):
            return None
        return (xy[0] + dx, xy[1] + dy)

    def connected(self, hpos, team):
        """Harvester at hpos has a structural route to its OWN core."""
        seen = set()
        for dx, dy in CARD:
            t = (hpos[0] + dx, hpos[1] + dy)
            cell = self.b.get(t)
            if cell is None or cell[0] != team:
                continue
            if cell[1] == "core":
                return True
            if cell[1] not in BELT:
                continue
            if self.out(t, cell[1], cell[2]) == hpos:
                continue          # aimed back at the harvester: not an acceptor
            if self._follow(t, team, seen):
                return True
        return False

    def _follow(self, xy, team, seen):
        cur = xy
        while cur is not None and cur not in seen:
            seen.add(cur)
            cell = self.b.get(cur)
            if cell is None or cell[0] != team:
                return False
            if cell[1] == "core":
                return True
            if cell[1] == "splitter":
                # We build none; a splitter rotates output among three sides,
                # so treat any adjacent own-core tile as delivery and stop.
                return any((cur[0] + dx, cur[1] + dy) in self.core_tiles[team]
                           for dx, dy in CARD)
            if cell[1] != "conveyor":
                return False
            nxt = self.out(cur, "conveyor", cell[2])
            if nxt is None:
                return False
            if nxt in self.core_tiles[team]:
                return True
            cur = nxt
        return False


def decode(path: Path, at_round=25):
    data = path.read_bytes()
    map_buf, turn_bufs = None, []
    winner, wincond = None, ""
    for num, wire, value in fields(data):
        if num == 1 and wire == 2:
            map_buf = value
        elif num == 3 and wire == 2:
            turn_bufs.append(value)
        elif num == 4:
            winner = value
        elif num == 6 and wire == 2:
            wincond = value.decode("utf-8", "replace")

    width = height = 0
    cores = []
    for num, wire, value in fields(map_buf):
        if num == 1:
            width = value
        elif num == 2:
            height = value
        elif num == 4 and wire == 2:
            d = {}
            for cn, cw, cv in fields(value):
                if cn == 1:
                    d["id"] = cv
                elif cn == 2:
                    d["team"] = cv
                elif cn == 3:
                    d["pos"] = read_pos(cv)
            d.setdefault("team", 0)
            cores.append(d)

    w = World(cores, width, height)
    ent_team, ent_kind, ent_pos = {}, {}, {}
    for c in cores:
        ent_team[c["id"]], ent_kind[c["id"]], ent_pos[c["id"]] = c["team"], "core", c["pos"]

    harv = {}                       # eid -> dict(team, pos, built, connect)
    moves = Counter()               # team -> total builder moves
    revs = Counter()                # team -> A->B->A reversals
    last_move = {}                  # eid -> (round, dx, dy)
    tags = Counter()
    tled = Counter()
    harv_at = {0: 0, 1: 0}
    builder_rounds = Counter()

    for rnd, turn_buf in enumerate(turn_bufs):
        for _n, _wi, ubuf in fields(turn_buf):
            for unum, _uw, uval in fields(ubuf):
                if unum == 1:                                   # placeEntity
                    for en, _ew, ebuf in fields(uval):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        new = e.id not in ent_kind
                        ent_team[e.id], ent_kind[e.id], ent_pos[e.id] = e.team, e.kind, e.pos
                        if e.kind != "builder_bot":
                            w.b[e.pos] = (e.team, e.kind, e.direction)
                        if new and e.kind == "harvester":
                            harv[e.id] = {"team": e.team, "pos": e.pos,
                                          "built": rnd, "connect": None}
                elif unum == 2:                                 # moveBuilderBot
                    eid = to = None
                    for mn, _mw, mv in fields(uval):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid is None or to is None:
                        continue
                    frm = ent_pos.get(eid)
                    ent_pos[eid] = to
                    t = ent_team.get(eid, 0)
                    if frm is None:
                        continue
                    d = (to[0] - frm[0], to[1] - frm[1])
                    moves[t] += 1
                    prev = last_move.get(eid)
                    if prev is not None and prev[0] == rnd - 1 \
                            and (d[0], d[1]) == (-prev[1], -prev[2]):
                        revs[t] += 1
                    last_move[eid] = (rnd, d[0], d[1])
                elif unum == 3:                                 # removeEntity
                    for rn, _rw, rv in fields(uval):
                        if rn != 1:
                            continue
                        p = ent_pos.pop(rv, None)
                        k = ent_kind.pop(rv, None)
                        ent_team.pop(rv, None)
                        if p is not None and k not in (None, "builder_bot") \
                                and p not in w.core_tiles[0] and p not in w.core_tiles[1]:
                            w.b.pop(p, None)
                        if rv in harv:
                            harv[rv]["died"] = rnd
                elif unum == 9:                                 # botOutput
                    d = scalars(uval)
                    eid = d.get(1)
                    t = ent_team.get(eid, 0)
                    if ent_kind.get(eid) == "builder_bot":
                        builder_rounds[t] += 1
                    if d.get(4):
                        tled[t] += 1
                    so = d.get(2)
                    if isinstance(so, bytes) and so:
                        for line in so.decode("utf-8", "replace").splitlines():
                            parts = line.strip().split(" ")
                            head = parts[0]
                            if not head:
                                continue
                            # A gate with three refusal reasons that all log the
                            # same tag is one number nobody can act on: keep the
                            # `why=` qualifier so a demo can say WHICH gate fired.
                            for q in parts[1:]:
                                if q.startswith("why="):
                                    head = head + "/" + q[4:]
                                    break
                            tags[head] += 1

        for hid, h in harv.items():
            if h["connect"] is None and "died" not in h:
                if w.connected(h["pos"], h["team"]):
                    h["connect"] = rnd
        if rnd == at_round:
            for h in harv.values():
                harv_at[h["team"]] += 1

    return {
        "rounds": len(turn_bufs), "winner": winner, "wincond": wincond,
        "harv": harv, "moves": dict(moves), "revs": dict(revs),
        "tags": tags, "tled": dict(tled), "harv_at": harv_at,
        "builder_rounds": dict(builder_rounds),
    }


def report(name, seat, d, at_round):
    hs = [h for h in d["harv"].values() if h["team"] == seat]
    conn = [h for h in hs if h["connect"] is not None]
    lat = sorted(h["connect"] - h["built"] for h in conn)
    med = lat[len(lat) // 2] if lat else None
    mv, rv = d["moves"].get(seat, 0), d["revs"].get(seat, 0)
    print(f"  {name} (seat {'AB'[seat]}): harv_built={len(hs)} "
          f"connected={len(conn)} ({100.0 * len(conn) / len(hs) if hs else 0:.1f}%) "
          f"median_connect_latency={med} harv_by_r{at_round}={d['harv_at'][seat]}")
    print(f"    moves={mv} A->B->A={rv} ({100.0 * rv / mv if mv else 0:.1f}%) "
          f"builder_rounds={d['builder_rounds'].get(seat, 0)} tled={d['tled'].get(seat, 0)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("bot_a")
    ap.add_argument("bot_b")
    ap.add_argument("map")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--at-round", type=int, default=25)
    ap.add_argument("--replay", default=None)
    a = ap.parse_args()

    rp = Path(a.replay) if a.replay else Path("/tmp/s48demo.replay26")
    res, tb, err = run_match(a.bot_a, a.bot_b, a.map, a.seed, rp)
    if res is None:
        print("MATCH FAILED\n" + err[-2000:])
        return 1
    d = decode(rp, a.at_round)
    print(f"== {a.bot_a} (A) vs {a.bot_b} (B) on {Path(a.map).stem} seed={a.seed}")
    print(f"  result: winner={res['winner']} turns={res['turns']} "
          f"cond={res['win_condition']} tracebacks={tb}")
    report(a.bot_a, 0, d, a.at_round)
    report(a.bot_b, 1, d, a.at_round)
    if d["tags"]:
        print("  dose tags: " + " ".join(f"{k}={v}" for k, v in sorted(d["tags"].items())))
    else:
        print("  dose tags: (none)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
