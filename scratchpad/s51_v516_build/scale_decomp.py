#!/usr/bin/env python3
"""Live-scale decomposition from a replay: what actually prices our sentinel?

scale = 1.0 + sum over LIVE own entities of their build contribution
        (conveyor/splitter/barrier +1%, harvester +5%, launcher +10%,
         builder_bot/gunner/sentinel +20%; the core contributes nothing).
Destruction removes the contribution (CLAUDE.md, engine-confirmed s26).

Reported per game at a chosen round (default: the round of our first sentinel
build beyond dsq_opp<=40, i.e. a forward/siege sentinel; falls back to r300):
  scale_pct, and the pp contributed by each type, plus the implied sentinel
  price floor(scale * 30).

GUARD: run with --guard to print the same decomposition at r0 (must be 100.0
plus exactly the starting bodies) and at the last round.
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game")
from tools.replay_census import WIRE_LEN, fields, parse_entity, read_pos  # noqa: E402

CONTRIB = {"conveyor": 1, "splitter": 1, "barrier": 1, "harvester": 5,
           "launcher": 10, "builder_bot": 20, "gunner": 20, "sentinel": 20}


def dsq(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def trace(path: Path, our_team: int):
    data = path.read_bytes()
    mb, turns = None, []
    for n, w, v in fields(data):
        if n == 1 and w == WIRE_LEN:
            mb = v
        elif n == 3 and w == WIRE_LEN:
            turns.append(v)
    cores = []
    for n, _w, v in fields(mb):
        if n == 4:
            c = {"team": 0, "pos": (0, 0)}
            for cn, _cw, cv in fields(v):
                if cn == 2:
                    c["team"] = cv
                elif cn == 3:
                    c["pos"] = read_pos(cv)
            cores.append(c)
    ctr = {c["team"]: (c["pos"][0] + .5, c["pos"][1] + .5) for c in cores}
    live = {}                     # id -> kind (ours only)
    ents = set()
    out = []                      # per round: dict kind->pp
    sent_fwd = []                 # rounds of forward sentinel builds
    for rnd, tb in enumerate(turns):
        for _n, _w, ub in fields(tb):
            for un, _uw, ubuf in fields(ub):
                if un == 1:
                    for en, _ew, eb in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(eb, rnd)
                        if e is None or e.id in ents:
                            continue
                        ents.add(e.id)
                        if e.team != our_team or e.kind == "core":
                            continue
                        live[e.id] = e.kind
                        if e.kind == "sentinel" and \
                                dsq(e.pos, ctr[1 - our_team]) <= 40:
                            sent_fwd.append(rnd)
                elif un == 3:
                    for rn, _rw, rv in fields(ubuf):
                        if rn == 1:
                            ents.discard(rv)
                            live.pop(rv, None)
        d = defaultdict(int)
        for k in live.values():
            d[k] += CONTRIB.get(k, 0)
        out.append(dict(d))
    return out, sent_fwd, len(turns)


KINDS = ["builder_bot", "conveyor", "splitter", "barrier", "harvester",
         "launcher", "gunner", "sentinel"]


def main():
    d = Path(sys.argv[1])
    print("\t".join(["tag", "rnd", "why", "scale_pct", "sent_price"] + KINDS))
    for p in sorted(d.glob("*.replay26")):
        tag = p.stem
        our = 0 if tag.endswith("_A") else 1
        tr, sent_fwd, n = trace(p, our)
        picks = []
        if sent_fwd:
            picks.append((sent_fwd[0], "first_fwd_sentinel"))
        picks.append((min(300, n - 1), "r300"))
        picks.append((n - 1, "end"))
        picks.append((0, "r0"))
        for rnd, why in picks:
            d0 = tr[rnd]
            tot = 100 + sum(d0.values())
            print("\t".join(str(x) for x in
                            [tag, rnd, why, tot, int(tot / 100.0 * 30)] +
                            [d0.get(k, 0) for k in KINDS]))


if __name__ == "__main__":
    main()
