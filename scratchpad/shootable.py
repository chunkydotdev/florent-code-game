#!/usr/bin/env python3
"""TRUE shootable-on-build rate for sentinels, using the DECODED facing.

Definitions, matched to the LOKI-17 autopsy so the numbers are comparable:
  build tile    = position on the FIRST placeEntity carrying that entity id
  target        = the NEAREST tile of the enemy Core's 2x2 footprint
                  (map.cores anchor is the NW corner)
  in range      = nearest-footprint d^2 <= 32
  UPPER BOUND   = exists a footprint tile with d^2 <= 32 that lies on ANY of the
                  8 compass rays from the build tile  (what the autopsy could
                  measure without facing)
  TRUE          = exists a footprint tile with d^2 <= 32 that lies on the ray in
                  the facing the sentinel was ACTUALLY BUILT WITH

Compass: (0,0) is the map NORTHWEST corner, x east, y south -> NORTH = (0,-1).
Validated empirically in scratchpad/facing_validate2.py (conveyor delivery tile
and gunner shot ray both 1.0000 RAW; FLIP-Y control collapses).
"""
from __future__ import annotations
import csv, sys, statistics
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa

DELTA = {0: (0, 0), 1: (0, -1), 2: (1, -1), 3: (1, 0), 4: (1, 1),
         5: (0, 1), 6: (-1, 1), 7: (-1, 0), 8: (-1, -1)}
NAME = {0: "CENTRE", 1: "N", 2: "NE", 3: "E", 4: "SE",
        5: "S", 6: "SW", 7: "W", 8: "NW"}
RANGE_DSQ = 32


def core_tiles(anchor):
    x, y = anchor
    return ((x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1))


def on_ray(frm, to, d):
    dx, dy = DELTA[d]
    if (dx, dy) == (0, 0):
        return False
    ex, ey = to[0] - frm[0], to[1] - frm[1]
    if dx == 0:
        return ex == 0 and ey * dy > 0
    if dy == 0:
        return ey == 0 and ex * dx > 0
    return ex * dy == ey * dx and ex * dx > 0 and ey * dy > 0


def any_ray(frm, to):
    ex, ey = to[0] - frm[0], to[1] - frm[1]
    if (ex, ey) == (0, 0):
        return False
    return ex == 0 or ey == 0 or abs(ex) == abs(ey)


def sentinels(path: Path):
    """yield (team, build_pos, direction, cores{team:anchor})"""
    data = path.read_bytes()
    map_buf, turn_bufs = None, []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if map_buf is None:
        return
    cores = {}
    for num, wire, value in fields(map_buf):
        if num == 4 and wire == WIRE_LEN:
            team, pos = 0, None
            for cn, cw, cv in fields(value):
                if cn == 2:
                    team = cv
                elif cn == 3 and cw == WIRE_LEN:
                    pos = read_pos(cv)
            if pos is not None:
                cores[team] = tuple(pos)
    if len(cores) < 2:
        return
    seen = set()
    for rnd, tb in enumerate(turn_bufs):
        for _n, _w, ub in fields(tb):
            for un, _uw, uv in fields(ub):
                if un != 1:
                    continue
                for en, _ew, ev in fields(uv):
                    if en != 1:
                        continue
                    e = parse_entity(ev, rnd)
                    if e is None or e.kind != "sentinel" or e.id in seen:
                        continue
                    seen.add(e.id)
                    yield e.team, tuple(e.pos), (e.direction or 0), cores, rnd


class Acc:
    def __init__(self):
        self.n = 0
        self.inrange = 0
        self.upper = 0
        self.true = 0
        self.d2 = []
        self.dirs = Counter()
        self.rounds = []

    def add(self, bp, d, foe_anchor, rnd):
        tiles = core_tiles(foe_anchor)
        near = min((bp[0] - t[0]) ** 2 + (bp[1] - t[1]) ** 2 for t in tiles)
        self.n += 1
        self.d2.append(near)
        self.dirs[d] += 1
        self.rounds.append(rnd)
        if near <= RANGE_DSQ:
            self.inrange += 1
        if any((bp[0] - t[0]) ** 2 + (bp[1] - t[1]) ** 2 <= RANGE_DSQ and any_ray(bp, t)
               for t in tiles):
            self.upper += 1
        if any((bp[0] - t[0]) ** 2 + (bp[1] - t[1]) ** 2 <= RANGE_DSQ and on_ray(bp, t, d)
               for t in tiles):
            self.true += 1

    def row(self, label):
        if not self.n:
            return f"{label}\tn=0"
        pc = lambda k: f"{100*k/self.n:.1f}%"
        return (f"{label}\tn={self.n}\tmedian_d2={statistics.median(self.d2):.0f}\t"
                f"in_range={pc(self.inrange)}\tUPPER={pc(self.upper)}\t"
                f"TRUE={pc(self.true)}\tgap={100*(self.upper-self.true)/self.n:.1f}pp")


def main():
    arch = ROOT / "replay_archive"
    rows = list(csv.DictReader(open(ROOT / "corpus/meta_join.tsv"), delimiter="\t"))
    US = "OpenSverige"
    targets = {"Ouroboros": "Ouroboros", "Askar City": "Askar City"}

    groups = {}   # key -> Acc
    files = {}    # opp -> [(file, our_team_byte)]
    for r in rows:
        a, b = r["teamAName"], r["teamBName"]
        if US not in (a, b):
            continue
        opp = b if a == US else a
        if opp not in targets:
            continue
        our_team = 0 if a == US else 1
        files.setdefault(opp, []).append((r["file"], our_team))

    for opp, lst in files.items():
        seen_files = set()
        for fn, our_team in lst:
            if fn in seen_files:
                continue
            seen_files.add(fn)
            p = arch / fn
            if not p.exists():
                continue
            for team, bp, d, cores, rnd in sentinels(p):
                foe = cores[1 - team]
                key = (opp, "ours" if team == our_team else "theirs")
                groups.setdefault(key, Acc()).add(bp, d, foe, rnd)
        print(f"# {opp}: {len(seen_files)} replays", file=sys.stderr)

    print("population\tstats")
    for key in [("Ouroboros", "ours"), ("Askar City", "ours"),
                ("Askar City", "theirs"), ("Ouroboros", "theirs")]:
        acc = groups.get(key)
        label = f"{key[1]} vs {key[0]}" if key[1] == "ours" else f"{key[0]}'s OWN"
        print(acc.row(label) if acc else f"{label}\tn=0")

    print("\nFACING HISTOGRAM (built facing, sentinels)")
    print("population\t" + "\t".join(NAME[d] for d in range(9)))
    for key, acc in groups.items():
        print(f"{key[0]}/{key[1]}\t" + "\t".join(str(acc.dirs.get(d, 0)) for d in range(9)))


if __name__ == "__main__":
    main()
