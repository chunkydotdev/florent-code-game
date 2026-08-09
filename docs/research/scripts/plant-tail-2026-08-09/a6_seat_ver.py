#!/usr/bin/env python3
"""Seat geometry caveat, batk endogeneity, and our-version trend."""
import csv, collections, math

D = "/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/tail/"
BASE = "/Users/junghard/Projects/Work/florent-code-game/corpus/"

J = {r["file"]: r for r in csv.DictReader(open(BASE + "join.tsv"), delimiter="\t")}

# --- where is each team's core?  round-0 builder bots spawn adjacent to it.
seatpos = collections.defaultdict(list)
with open(BASE + "events.tsv") as f:
    f.readline()
    for line in f:
        p = line.rstrip("\n").split("\t")
        if p[1] != "BUILD" or p[2] != "0" or p[4] != "builder_bot":
            continue
        j = J.get(p[0])
        if not j:
            continue
        who = "US" if p[3] == j["our_team"] else "THEM"
        seatpos[(j["our_team"], who)].append((int(p[5])/int(p[9]), int(p[6])/int(p[10])))
print("=== core side of map (mean normalised x,y of round-0 builder spawns)")
for k, v in sorted(seatpos.items()):
    mx = sum(a for a, b in v)/len(v); my = sum(b for a, b in v)/len(v)
    print(f"  our_team={k[0]} {k[1]:5s}  x={mx:.2f} y={my:.2f}  n={len(v)}")

rows = []
for r in csv.DictReader(open(D + "plants2.tsv"), delimiter="\t"):
    for k in ("our_team", "won", "lastrnd", "rnd", "d2", "died", "life",
              "nb_sameturret8"):
        r[k] = int(r[k])
    r["fu"] = r["lastrnd"] - r["rnd"]
    rows.append(r)
batk = collections.Counter()
for r in csv.DictReader(open(BASE + "build_agg.tsv"), delimiter="\t"):
    if r["metric"] == "batk":
        batk[(r["file"], r["team"])] += int(r["n"])
T = 200
pop = [r for r in rows if r["side"] == "THEM" and r["fu"] >= T]
for r in pop:
    r["alive"] = 1 if ((not r["died"]) or r["life"] > T) else 0
    j = J[r["file"]]
    r["ourver"] = j["ourver"]
    r["rate"] = batk[(r["file"], str(r["our_team"]))] / max(1, r["lastrnd"])

print("\n=== BATK endogeneity: is 'we attacked a lot' just 'the game was short/we won'?")
for lab, f in (("we WON", lambda r: r["won"]), ("we LOST", lambda r: not r["won"])):
    g = [r for r in pop if f(r)]
    print(f"  {lab}: mean batk/round {sum(r['rate'] for r in g)/len(g):.2f} n={len(g)}")
print("  survival by batk rate, STRATIFIED by win/loss:")
for lab, f in (("WON", lambda r: r["won"]), ("LOST", lambda r: not r["won"])):
    for bl, bf in (("<0.2", lambda r: r["rate"] < .2), (">=0.2", lambda r: r["rate"] >= .2)):
        g = [r for r in pop if f(r) and bf(r)]
        if g:
            print(f"    {lab:5s} batk{bl:6s} alive {sum(r['alive'] for r in g)/len(g):6.1%} "
                  f"n={len(g):5d} games={len(set(r['file'] for r in g))}")

print("\n=== OUR VERSION trend (at-risk plants, T=200), versions with >=60 plants")
byv = collections.defaultdict(list)
for r in pop:
    byv[r["ourver"]].append(r)
out = []
for v, g in byv.items():
    if len(g) >= 60:
        out.append((int(v) if v.isdigit() else -1, v, sum(r["alive"] for r in g)/len(g),
                    len(g), len(set(r["file"] for r in g))))
out.sort()
for _, v, a, n, gm in out:
    print(f"  v{v:>4s}  alive {a:6.1%}  n={n:5d} games={gm:4d}")
if len(out) >= 4:
    early = [o for o in out[:len(out)//2]]
    late = [o for o in out[len(out)//2:]]
    ea = sum(o[2]*o[3] for o in early)/sum(o[3] for o in early)
    la = sum(o[2]*o[3] for o in late)/sum(o[3] for o in late)
    print(f"  older half {ea:.1%} (n={sum(o[3] for o in early)})  "
          f"newer half {la:.1%} (n={sum(o[3] for o in late)})  diff {(la-ea)*100:+.1f}pp")
    print("  NOTE: opponent mix changes with version (ladder rating moves), so this is"
          " confounded by opponent.")
