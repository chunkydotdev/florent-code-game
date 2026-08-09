#!/usr/bin/env python3
"""Validation of pc_decode output before anything is read off it."""
import csv, collections, sys
S = "/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/precursor/"
B = "/Users/junghard/Projects/Work/florent-code-game/corpus/"

P = list(csv.DictReader(open(S + "plants.tsv"), delimiter="\t"))
E = list(csv.DictReader(open(S + "episodes.tsv"), delimiter="\t"))
print(f"plants {len(P)}  episodes {len(E)}")

# 1. reproduce the published plant count / kind split from events.tsv
J = {r["file"]: r for r in csv.DictReader(open(B + "join.tsv"), delimiter="\t")}
ref = collections.Counter()
refset = collections.Counter()
with open(B + "events.tsv") as f:
    f.readline()
    for line in f:
        r = line.rstrip("\n").split("\t")
        j = J.get(r[0])
        if not j or r[1] != "BUILD":
            continue
        if r[4] in ("gunner", "sentinel") and int(r[8]) <= 32 and r[3] != j["our_team"]:
            ref[r[4]] += 1
            refset[(r[0], r[2], r[4], r[5], r[6])] += 1
mine = collections.Counter(p["kind"] for p in P)
mineset = collections.Counter((p["file"], p["rnd"], p["kind"], p["x"], p["y"]) for p in P)
print("events.tsv:", dict(ref), " pc_decode:", dict(mine))
print("exact (file,rnd,kind,x,y) multiset match:", refset == mineset,
      " sym-diff:", sum((refset - mineset).values()) + sum((mineset - refset).values()))

# 2. planter attribution quality
nc = collections.Counter(int(p["ncand"]) for p in P)
print("adjacent-enemy-builder candidates at build moment:", dict(sorted(nc.items())))
tot = len(P)
print(f"  attributed uniquely: {nc[1]/tot:.1%}   ambiguous(>=2): {sum(v for k,v in nc.items() if k>=2)/tot:.1%}"
      f"   none found: {nc[0]/tot:.1%}")

# 3. d2 to core sanity: all plants <=32
print("max d2:", max(int(p["d2"]) for p in P), " min:", min(int(p["d2"]) for p in P))

# 4. episode sanity
bad = sum(1 for e in E if int(e["length"]) < 1 or int(e["end"]) < int(e["start"]))
print("episodes with bad length/bounds:", bad)
print("episode length dist:", collections.Counter(min(int(e["length"]),50) for e in E).most_common(8))
# every plant with a pid should sit inside an episode of that bot
epk = collections.defaultdict(list)
for e in E:
    epk[(e["file"], e["bid"])].append((int(e["start"]), int(e["end"])))
inside = out = 0
for p in P:
    if int(p["pid"]) < 0:
        continue
    r = int(p["rnd"])
    if any(a <= r <= b + 1 for a, b in epk.get((p["file"], p["pid"]), [])):
        inside += 1
    else:
        out += 1
print(f"plants whose planter is inside one of its own in-band episodes: {inside} / {inside+out}")

# 5. vis_core_m1 -- is the band inside core vision by construction?
vc = collections.Counter(p["vis_core_m1"] for p in P)
print("vis_core_m1 (planter within d2<=36 of our core anchor at t-1):", dict(vc))
