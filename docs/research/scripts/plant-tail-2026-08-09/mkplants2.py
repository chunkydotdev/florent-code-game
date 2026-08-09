#!/usr/bin/env python3
"""Plant table for BOTH sides.

A 'plant' = a gunner or sentinel built on a tile with d2_enemy <= 32, i.e. deep
inside the OTHER team's home band.  side=THEM means the opponent planted in OUR
base (the population the question is about); side=US is the mirror benchmark.

events.tsv carries no entity id, so a plant is paired to its death FIFO on
(file, team, kind, x, y).
"""
import csv, sys, collections

BASE = "/Users/junghard/Projects/Work/florent-code-game/corpus/"
OUT = "/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/tail/plants2.tsv"

J = {}
with open(BASE + "join.tsv") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        J[r["file"]] = r

BUILDINGS = {"core", "conveyor", "splitter", "harvester", "barrier",
             "gunner", "sentinel", "launcher"}

out = open(OUT, "w")
out.write("file\tside\topp\tmap\tour_team\twon\tturns\tlastrnd\tkind\trnd\tx\ty\td2\t"
          "died\tdrnd\tlife\tnb_same8\tnb_sameturret8\tnb_opp8\tnb_same16\tnb_opp16\t"
          "reuse\n")
stats = collections.Counter()


def flush(fname, rows):
    j = J.get(fname)
    if not j:
        return
    stats["files"] += 1
    ourt = int(j["our_team"])
    lastrnd = max(int(r[2]) for r in rows)
    live = collections.defaultdict(list)
    plants = []
    idx = {}
    nbuilds = collections.Counter()
    for r in rows:
        _f, ev, rnd, team, kind, x, y, d2o, d2e, mw, mh = r
        rnd = int(rnd); team = int(team); x = int(x); y = int(y)
        key = (team, kind, x, y)
        if ev == "BUILD":
            if kind in BUILDINGS:
                live[(x, y)].append((team, kind))
            if kind in ("gunner", "sentinel") and int(d2e) <= 32:
                nbuilds[key] += 1
                planter = team
                ns8 = st8 = no8 = ns16 = no16 = 0
                for (tx, ty), occ in live.items():
                    dd = (tx - x) ** 2 + (ty - y) ** 2
                    if dd == 0 or dd > 16:
                        continue
                    for (ot, ok) in occ:
                        if ok == "core":
                            continue
                        if dd <= 8:
                            if ot == planter:
                                ns8 += 1
                                if ok in ("gunner", "sentinel", "launcher"):
                                    st8 += 1
                            else:
                                no8 += 1
                        if ot == planter:
                            ns16 += 1
                        else:
                            no16 += 1
                p = dict(side=("US" if team == ourt else "THEM"), key=key,
                         kind=kind, rnd=rnd, x=x, y=y, d2=int(d2e), drnd=-1,
                         ns8=ns8, st8=st8, no8=no8, ns16=ns16, no16=no16)
                plants.append(p)
                idx.setdefault(key, collections.deque()).append(p)
        else:
            if kind in BUILDINGS:
                lst = live.get((x, y))
                if lst and (team, kind) in lst:
                    lst.remove((team, kind))
            q = idx.get(key)
            if q:
                q.popleft()["drnd"] = rnd
    for p in plants:
        died = 1 if p["drnd"] >= 0 else 0
        life = (p["drnd"] - p["rnd"]) if died else -1
        out.write(f"{fname}\t{p['side']}\t{j['opp']}\t{j['map']}\t{ourt}\t{j['won']}\t"
                  f"{j['turns']}\t{lastrnd}\t{p['kind']}\t{p['rnd']}\t{p['x']}\t{p['y']}\t"
                  f"{p['d2']}\t{died}\t{p['drnd']}\t{life}\t{p['ns8']}\t{p['st8']}\t"
                  f"{p['no8']}\t{p['ns16']}\t{p['no16']}\t{nbuilds[p['key']]}\n")
        stats["plants_" + p["side"]] += 1
        if died and life < 0:
            stats["NEG_LIFE"] += 1


cur, buf, n = None, [], 0
with open(BASE + "events.tsv") as f:
    f.readline()
    for line in f:
        r = line.rstrip("\n").split("\t")
        n += 1
        if r[0] != cur:
            if cur in J:
                flush(cur, buf)
            cur, buf = r[0], []
        if cur in J:
            buf.append(r)
if cur in J:
    flush(cur, buf)
out.close()
sys.stderr.write(f"event rows: {n}\n")
for k, v in sorted(stats.items()):
    sys.stderr.write(f"  {k}: {v}\n")
