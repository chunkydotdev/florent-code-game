#!/usr/bin/env python3
"""Validate the FIFO pairing (buildings cannot co-occupy a tile, so build/death
on one tile MUST alternate -- check that empirically), and re-run the headline
after de-duplicating rebuild churn, which is a non-independence hazard."""
import csv, collections

D = "/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/tail/"
rows = []
for r in csv.DictReader(open(D + "plants2.tsv"), delimiter="\t"):
    for k in ("our_team", "won", "lastrnd", "rnd", "x", "y", "d2", "died", "life",
              "nb_sameturret8", "reuse"):
        r[k] = int(r[k])
    r["fu"] = r["lastrnd"] - r["rnd"]
    rows.append(r)
them = [r for r in rows if r["side"] == "THEM"]

# --- alternation check
byk = collections.defaultdict(list)
for r in them:
    byk[(r["file"], r["kind"], r["x"], r["y"])].append(r)
bad = tot = 0
for k, v in byk.items():
    v.sort(key=lambda r: r["rnd"])
    for a, b in zip(v, v[1:]):
        tot += 1
        # a must be dead before b is built
        if a["died"] == 0 or a["drnd"] if False else (a["died"] == 0 or int(a["drnd"]) > b["rnd"]):
            bad += 1
print(f"PAIRING CHECK: consecutive plants on the same tile: {tot}; "
      f"overlapping lifetimes (would mean mis-pairing): {bad} ({bad/max(1,tot):.3%})")

print(f"\nCHURN: plants per (game, tile): "
      f"{len(them)} plants on {len(byk)} distinct (game, tile) keys")
c = collections.Counter(len(v) for v in byk.values())
top = sorted(byk.items(), key=lambda t: -len(t[1]))[:5]
for k, v in top:
    print(f"  hot key {k[1]} at ({k[2]},{k[3]}) in {k[0][:8]}...: {len(v)} rebuilds, "
          f"opp={v[0]['opp']}, survived-to-end={sum(1 for r in v if r['died']==0)}")
share = sum(n for n in c.elements() if n >= 10) if False else \
    sum(len(v) for v in byk.values() if len(v) >= 10)
print(f"  plants living on keys with >=10 rebuilds: {share} = {share/len(them):.1%} of all plants,"
      f" from {sum(1 for v in byk.values() if len(v)>=10)} keys")

T = 200
for lab, pop in (("ALL plants", [r for r in them if r["fu"] >= T]),
                 ("one row per (game,tile) = FIRST plant only",
                  [sorted(v, key=lambda r: r["rnd"])[0] for v in byk.values()
                   if sorted(v, key=lambda r: r["rnd"])[0]["fu"] >= T]),
                 ("drop keys with >=10 rebuilds",
                  [r for r in them if r["fu"] >= T and r["reuse"] < 10])):
    a = sum(1 for r in pop if (not r["died"]) or r["life"] > T)
    print(f"\n{lab}: at-risk n={len(pop)}  alive at +200 {a/len(pop):.1%}")
    # and the two headline discriminators re-checked on this population
    for nm, f in (("near d2<=8", lambda r: r["d2"] <= 8),
                  ("far d2>=18", lambda r: r["d2"] >= 18),
                  ("0 friendly turrets nearby", lambda r: r["nb_sameturret8"] == 0),
                  (">=2 friendly turrets nearby", lambda r: r["nb_sameturret8"] >= 2)):
        g = [r for r in pop if f(r)]
        if g:
            aa = sum(1 for r in g if (not r["died"]) or r["life"] > T)
            print(f"    {nm:28s} {aa/len(g):6.1%}  n={len(g)}")
