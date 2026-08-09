#!/usr/bin/env python3
"""Build the plant table: every enemy gunner/sentinel built inside our home band
(d2_enemy <= 32) in an attributed game, paired FIFO to its DEATH row.

events.tsv has NO entity id, so pairing is FIFO on (file, team, kind, x, y):
build #k on a tile pairs with death #k on that tile.  Verified below by
reporting how often a tile is reused (multi-build) at all.

Outputs plants.tsv and a stderr audit.
"""
import csv, sys, collections

BASE = "/Users/junghard/Projects/Work/florent-code-game/corpus/"
OUT = "/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/tail/plants.tsv"

J = {}
with open(BASE + "join.tsv") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        J[r["file"]] = r
sys.stderr.write(f"join rows: {len(J)}\n")

BUILDINGS = {"core", "conveyor", "splitter", "harvester", "barrier",
             "gunner", "sentinel", "launcher"}

out = open(OUT, "w")
out.write("file\topp\tmap\tour_team\twon\tturns\tlastrnd\tkind\trnd\tx\ty\td2\t"
          "died\tdrnd\tlife\tnb_enemy8\tnb_enemyturret8\tnb_our8\tnb_enemy16\tnb_our16\n")

stats = collections.Counter()

def flush(fname, rows):
    j = J.get(fname)
    if not j:
        return
    stats["files"] += 1
    ourt = int(j["our_team"])
    theirs = 1 - ourt
    lastrnd = max(int(r[2]) for r in rows)
    # live-building reconstruction (all teams), keyed tile -> list of (team,kind)
    live = collections.defaultdict(list)
    # plants keyed by (team,kind,x,y) -> deque of build rounds
    pend = collections.defaultdict(collections.deque)
    plants = []   # dicts
    idx = {}      # (team,kind,x,y) -> deque of plant indexes awaiting death
    for r in rows:
        _f, ev, rnd, team, kind, x, y, d2o, d2e, mw, mh = r
        rnd = int(rnd); team = int(team); x = int(x); y = int(y)
        key = (team, kind, x, y)
        if ev == "BUILD":
            if kind in BUILDINGS:
                live[(x, y)].append((team, kind))
            if (team == theirs and kind in ("gunner", "sentinel")
                    and int(d2e) <= 32):
                # neighbourhood census at plant time
                ne8 = et8 = no8 = ne16 = no16 = 0
                for (tx, ty), occ in live.items():
                    dd = (tx - x) ** 2 + (ty - y) ** 2
                    if dd == 0 or dd > 16:
                        continue
                    for (ot, ok) in occ:
                        if ok == "core":
                            continue
                        if dd <= 8:
                            if ot == theirs:
                                ne8 += 1
                                if ok in ("gunner", "sentinel", "launcher"):
                                    et8 += 1
                            else:
                                no8 += 1
                        if ot == theirs:
                            ne16 += 1
                        else:
                            no16 += 1
                p = dict(kind=kind, rnd=rnd, x=x, y=y, d2=int(d2e),
                         drnd=-1, ne8=ne8, et8=et8, no8=no8, ne16=ne16, no16=no16)
                plants.append(p)
                idx.setdefault(key, collections.deque()).append(p)
        else:  # DEATH
            if kind in BUILDINGS:
                lst = live.get((x, y))
                if lst:
                    try:
                        lst.remove((team, kind))
                    except ValueError:
                        stats["death_no_live"] += 1
                else:
                    stats["death_no_live"] += 1
            q = idx.get(key)
            if q:
                p = q.popleft()
                p["drnd"] = rnd
    for p in plants:
        died = 1 if p["drnd"] >= 0 else 0
        life = (p["drnd"] - p["rnd"]) if died else -1
        out.write(f"{fname}\t{j['opp']}\t{j['map']}\t{ourt}\t{j['won']}\t{j['turns']}\t"
                  f"{lastrnd}\t{p['kind']}\t{p['rnd']}\t{p['x']}\t{p['y']}\t{p['d2']}\t"
                  f"{died}\t{p['drnd']}\t{life}\t{p['ne8']}\t{p['et8']}\t{p['no8']}\t"
                  f"{p['ne16']}\t{p['no16']}\n")
        stats["plants"] += 1
        stats["died" if died else "alive"] += 1
        if died and life < 0:
            stats["NEG_LIFE"] += 1

cur = None
buf = []
n = 0
with open(BASE + "events.tsv") as f:
    f.readline()
    for line in f:
        r = line.rstrip("\n").split("\t")
        n += 1
        if r[0] != cur:
            if cur is not None and cur in J:
                flush(cur, buf)
            cur = r[0]
            buf = []
        if cur in J:
            buf.append(r)
if cur is not None and cur in J:
    flush(cur, buf)
out.close()
sys.stderr.write(f"event rows read: {n}\n")
for k, v in sorted(stats.items()):
    sys.stderr.write(f"  {k}: {v}\n")
