#!/usr/bin/env python3
"""Q5: the negative control.  How often does the precursor fire without a plant?

Two grains:
  (a) EPISODE grain -- one enemy builder's visit inside d2<=36 of our core.
  (b) ROUND grain    -- every (game, round) in which at least one enemy builder
      is inside d2<=36.  This is the grain an in-bot trigger actually lives at:
      the core evaluates it once per round.
"""
import csv, collections, math
S = "/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/precursor/"

E = list(csv.DictReader(open(S + "episodes2.tsv"), delimiter="\t"))
for e in E:
    for k in ("start", "end", "length", "len32", "mind2", "planted",
              "plant_lag", "other_builds", "lastrnd", "seat", "nother_max"):
        e[k] = int(e[k])
print(f"episodes (enemy builder visits inside d2<=36 of our core): {len(E)} "
      f"over {len(set(e['file'] for e in E))} games")

print("\n--- (a) EPISODE GRAIN ---")
print(f"  {'visit length >= T':>20} {'visits':>8} {'planted a turret':>18} "
      f"{'built nothing at all':>22}")
for T in (1, 2, 3, 5, 10, 20, 30, 50, 100, 200):
    sub = [e for e in E if e["length"] >= T]
    if not sub:
        continue
    k = sum(1 for e in sub if e["planted"])
    nb = sum(1 for e in sub if not e["planted"] and not e["other_builds"])
    print(f"  {T:>20} {len(sub):>8} {k:>8} = {k/len(sub):6.1%} "
          f"{nb:>10} = {nb/len(sub):6.1%}")
print("  same, restricted to visits that ever reached the plant band d2<=32:")
E32 = [e for e in E if e["len32"] >= 1]
for T in (1, 5, 10, 20, 50):
    sub = [e for e in E32 if e["length"] >= T]
    k = sum(1 for e in sub if e["planted"])
    print(f"    len>=T {T:>4}: {k}/{len(sub)} = {k/len(sub):.1%} plant")
lens = sorted(e["length"] for e in E)
print(f"  visit-length distribution: n={len(lens)} med={lens[len(lens)//2]} "
      f"p90={lens[int(.9*len(lens))]} p99={lens[int(.99*len(lens))]} max={lens[-1]}")
print(f"  visits per game: {len(E)/len(set(e['file'] for e in E)):.1f}")

# ---------- (b) ROUND GRAIN ----------
Z = collections.defaultdict(dict)
games = {}
with open(S + "zone_rounds.tsv") as f:
    f.readline()
    for line in f:
        fn, seat, rnd, nb36, nb32, ms36, ms32, lastrnd = line.split("\t")
        Z[fn][int(rnd)] = (int(nb36), int(nb32), int(ms36), int(ms32))
        games[fn] = (int(seat), int(lastrnd))
P = list(csv.DictReader(open(S + "plants2.tsv"), delimiter="\t"))
plant_rounds = collections.defaultdict(set)
seed_rounds = collections.defaultdict(set)
for p in P:
    plant_rounds[p["file"]].add(int(p["rnd"]))
    if int(p["pre_t8"]) == 0:
        seed_rounds[p["file"]].add(int(p["rnd"]))

TOTROUNDS = sum(lr + 1 for (_s, lr) in games.values())
TOTZ = sum(len(v) for v in Z.values())
print(f"\n--- (b) ROUND GRAIN ---")
print(f"  games {len(games)}   total rounds played {TOTROUNDS}   "
      f"rounds with >=1 enemy builder inside d2<=36: {TOTZ} ({TOTZ/TOTROUNDS:.1%})")

K = 10


def eval_trigger(name, pred):
    fired = hit = 0
    firing_games = set()
    for fn, rounds in Z.items():
        pr = plant_rounds[fn]
        for rnd, v in rounds.items():
            if not pred(v):
                continue
            fired += 1
            firing_games.add(fn)
            if any((rnd + 1) <= t <= (rnd + K) for t in pr):
                hit += 1
    prec = hit / fired if fired else 0
    print(f"  {name:<46} fires {fired:>7} rounds "
          f"({fired/TOTROUNDS:5.1%} of all rounds), plant within {K} rnd: "
          f"{prec:6.1%}  -> FALSE POSITIVE {1-prec:6.1%}")
    return fired, hit


# base rate: over every round of every game, is there a plant in the next K?
base_f = base_h = 0
for fn, (seat, lr) in games.items():
    pr = plant_rounds[fn]
    for rnd in range(lr + 1):
        base_f += 1
        if any((rnd + 1) <= t <= (rnd + K) for t in pr):
            base_h += 1
print(f"  BASELINE (no trigger, every round): plant in next {K} rounds "
      f"{base_h/base_f:.1%} of {base_f} rounds")
eval_trigger(">=1 enemy builder inside d2<=36", lambda v: v[0] >= 1)
eval_trigger(">=1 enemy builder inside the band d2<=32", lambda v: v[1] >= 1)
eval_trigger(">=2 enemy builders inside d2<=36", lambda v: v[0] >= 2)
eval_trigger(">=3 enemy builders inside d2<=36", lambda v: v[0] >= 3)
for T in (3, 5, 10, 20):
    eval_trigger(f"some enemy builder loitering >= {T} rounds",
                 lambda v, T=T: v[2] >= T)
eval_trigger(">=2 builders AND one loitering >=5", lambda v: v[0] >= 2 and v[2] >= 5)
eval_trigger("a builder in band d2<=32 for >=3 rounds", lambda v: v[3] >= 3)

# recall: what share of plants have >=1 enemy builder in zone the round before?
cov = collections.Counter()
for p in P:
    fn, rnd = p["file"], int(p["rnd"])
    v = Z.get(fn, {}).get(rnd - 1)
    cov["any_zone"] += 1 if (v and v[0] >= 1) else 0
    cov["two_zone"] += 1 if (v and v[0] >= 2) else 0
    cov["loiter5"] += 1 if (v and v[2] >= 5) else 0
    cov["n"] += 1
print(f"\n  RECALL at t-1 over all {cov['n']} plants: "
      f">=1 builder in zone {cov['any_zone']/cov['n']:.1%}, "
      f">=2 builders {cov['two_zone']/cov['n']:.1%}, "
      f"some builder loitering>=5 {cov['loiter5']/cov['n']:.1%}")

# how many rounds per game would each trigger fire?
for nm, pred in ((">=1 in zone", lambda v: v[0] >= 1),
                 (">=2 in zone", lambda v: v[0] >= 2),
                 ("loiter>=10", lambda v: v[2] >= 10)):
    per = [sum(1 for v in r.values() if pred(v)) for r in Z.values()]
    per.sort()
    print(f"  rounds/game the trigger '{nm}' is true: med={per[len(per)//2]} "
          f"p90={per[int(.9*len(per))]} mean={sum(per)/len(per):.0f}")
