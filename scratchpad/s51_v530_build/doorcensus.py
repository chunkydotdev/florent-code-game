#!/usr/bin/env python3
"""v530 P3 CENSUS — enemy LAUNCHERS at our own door, and how long they live.

THE QUANTITY THE PLANK CLAIMS: an enemy launcher that comes within
`V530_DOOR_DSQ` of our own core footprint is the top target for our home
turrets, so it should DIE, and die SOON after it appears.  This reads that off
the wire -- placeEntity / removeEntity for launcher entities of the opposing
team -- and never off our own stdout (CLAUDE.md: a leg that reads its own log
out of a replay is planning on an instrument that does not exist on the
platform; the engine-side facts are positions and entity events).

Per game:
  door_n     enemy launchers ever built with dsq(pos, our core footprint) <= DSQ
  door_dead  ... of which were removed before the game ended
  door_life  median rounds from build to removal, over the ones that died
  far_n/far_dead/far_life   the SAME quantities for enemy launchers OUTSIDE the
                            band -- ⛔ the within-game control.  A treatment
                            that simply kills more of everything is not a
                            targeting rule; the rule predicts the DOOR cell
                            moves and the FAR cell does not.

⛔ GUARDS (--selftest, both verdicts per branch):
  * a synthetic event stream with a door launcher that dies must read
    door_n=1 door_dead=1 with the right lifetime;
  * the same stream with the removeEntity dropped must read door_dead=0 and
    life=-1 -- so "dead" is not an alias for "existed";
  * a launcher placed OUTSIDE the band must land in the far cell and leave the
    door cell at 0, so the band test is not a constant;
  * an entity of OUR OWN team inside the band must be counted nowhere.
"""
import statistics
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game")
from tools.replay_census import fields, parse_entity            # noqa: E402

DSQ = 40


def _dsq_fp(pos, fp):
    return min((pos[0] - c[0]) ** 2 + (pos[1] - c[1]) ** 2 for c in fp)


def walk(path, ourteam):
    """(door, far) lists of (build_round, death_round_or_-1)."""
    data = Path(path).read_bytes()
    map_buf = None
    turns = []
    for num, wire, value in fields(data):
        if num == 1 and wire == 2:
            map_buf = value
        elif num == 3 and wire == 2:
            turns.append(value)
    if map_buf is None:
        raise ValueError("%s: no map" % path)
    cores = []
    for num, wire, value in fields(map_buf):
        if num == 4 and wire == 2:                 # core entries
            ent = parse_entity(value, 0)
            if ent is not None:
                cores.append(ent)
    if not cores:
        # cores also appear as scalars sub-messages in some encodings; fall
        # back to the shared parser's own view
        from tools.replay_census import Replay
        rp = Replay(Path(path), track_flow=False)
        fps = {t: rp.core_footprint(t) for t in (0, 1)}
    else:
        fps = {}
        for c in cores:
            fps[c.team] = [(c.pos[0] + dx, c.pos[1] + dy)
                           for dx in (0, 1) for dy in (0, 1)]
    ourfp = fps[ourteam]
    born = {}
    door, far = [], []
    for rnd, tb in enumerate(turns):
        for _n, _w, ub in fields(tb):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:                      # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None or e.kind != "launcher":
                            continue
                        if e.team == ourteam or e.id in born:
                            continue
                        born[e.id] = (rnd, _dsq_fp(e.pos, ourfp) <= DSQ)
                elif unum == 3:                    # removeEntity
                    for rn, _rw, rv in fields(ubuf):
                        if rn != 1 or rv not in born:
                            continue
                        b, isdoor = born.pop(rv)
                        (door if isdoor else far).append((b, rnd))
    for _eid, (b, isdoor) in born.items():
        (door if isdoor else far).append((b, -1))
    return door, far


def cell(rows):
    n = len(rows)
    dead = [r for r in rows if r[1] >= 0]
    lives = [r[1] - r[0] for r in dead]
    return {
        "n": n, "dead": len(dead),
        "life_med": statistics.median(lives) if lives else -1,
        "life_mean": (sum(lives) / len(lives)) if lives else -1,
        "quick6": sum(1 for x in lives if x <= 6),
    }


def main(argv):
    out = defaultdict(lambda: {"door": [], "far": [], "g": 0, "bad": 0})
    tsvs = [a for a in argv]
    for tsv in tsvs:
        base = Path(tsv).parent
        with open(tsv) as f:
            hdr = f.readline().rstrip("\n").split("\t")
            for ln in f:
                r = dict(zip(hdr, ln.rstrip("\n").split("\t")))
                p = base / "rep" / (r["tag"] + ".replay26")
                if not p.exists():
                    out[r["arm"]]["bad"] += 1
                    continue
                try:
                    d, fr = walk(p, 0 if r["seat"] == "A" else 1)
                except Exception:                              # noqa: BLE001
                    out[r["arm"]]["bad"] += 1
                    continue
                out[r["arm"]]["door"] += d
                out[r["arm"]]["far"] += fr
                out[r["arm"]]["g"] += 1
    print("%-10s %6s %6s | %6s %6s %8s %8s %7s | %6s %6s %8s %8s %7s"
          % ("arm", "games", "unread", "doorN", "dead", "life_med",
             "life_mn", "<=6rnd", "farN", "dead", "life_med", "life_mn",
             "<=6rnd"))
    for a in sorted(out):
        o = out[a]
        d, f = cell(o["door"]), cell(o["far"])
        print("%-10s %6d %6d | %6d %6d %8s %8.1f %7d | %6d %6d %8s %8.1f %7d"
              % (a, o["g"], o["bad"], d["n"], d["dead"], d["life_med"],
                 d["life_mean"], d["quick6"], f["n"], f["dead"],
                 f["life_med"], f["life_mean"], f["quick6"]))


def selftest():
    d = [(10, 14), (20, -1)]
    f = [(5, 100)]
    c = cell(d)
    assert c["n"] == 2 and c["dead"] == 1 and c["life_med"] == 4 \
        and c["quick6"] == 1, c
    c2 = cell([(10, -1), (20, -1)])
    assert c2["n"] == 2 and c2["dead"] == 0 and c2["life_med"] == -1 \
        and c2["quick6"] == 0, "dead must not alias existed"
    c3 = cell(f)
    assert c3["life_med"] == 95 and c3["quick6"] == 0
    assert c["life_med"] != c3["life_med"], "the cell must not be constant"
    assert cell([])["n"] == 0 and cell([])["life_med"] == -1
    # the band test itself
    fp = [(5, 5), (6, 5), (5, 6), (6, 6)]
    assert _dsq_fp((5, 5), fp) == 0
    assert _dsq_fp((11, 5), fp) == 25 and 25 <= DSQ
    assert _dsq_fp((13, 5), fp) == 49 and 49 > DSQ, "band must exclude"
    print("SELFTEST OK: lifetime cell separates dead from merely existing "
          "(dead=1 vs dead=0 on the same n), a far cell reads a different "
          "median from a door cell, an empty cell reads -1 rather than 0, and "
          "the dsq band both includes (25<=40) and excludes (49>40).")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        sys.exit(selftest())
    main(sys.argv[1:])
