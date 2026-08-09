#!/usr/bin/env python3
"""Nest formation: is it predictable at SEED time, and how much time do we get?"""
import csv, collections, math
S = "/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/precursor/"
B = "/Users/junghard/Projects/Work/florent-code-game/corpus/"
J = {r["file"]: r for r in csv.DictReader(open(B + "join.tsv"), delimiter="\t")}
P = list(csv.DictReader(open(S + "plants2.tsv"), delimiter="\t"))
INT = ("rnd", "d2", "loiter32", "loiter36", "loiter50", "zone_total", "age",
       "ep_len", "ep_other_builds", "moves_w10", "mind2_w10", "closing_w10",
       "nb32_m1", "nb36_m1", "nb32_max_w10", "nb36_max_w10",
       "nb36_distinct_w10", "vis_oth_m1", "pre_t8", "new_t8_30", "new_x0_30",
       "new_coex_30", "died", "drnd", "lastrnd", "reuse_idx", "seat",
       "ep_throw_in", "plt_d2")
for p in P:
    for k in INT:
        p[k] = int(p[k])
    p["opp"] = J[p["file"]]["opp"]
    p["won"] = int(J[p["file"]]["won"])
SEED = [p for p in P if p["lastrnd"] - p["rnd"] >= 30 and p["pre_t8"] == 0]
NEST = [p for p in SEED if p["new_coex_30"] >= 1]
print(f"seeds {len(SEED)}  nest {len(NEST)} ({len(NEST)/len(SEED):.1%})")


def ztest(k1, n1, k2, n2):
    if not n1 or not n2:
        return 0.0
    p1, p2 = k1 / n1, k2 / n2
    p = (k1 + k2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    return (p1 - p2) / se if se else 0.0


print("\n--- P(nest within 30 rounds) by SEED-TIME feature (all observable in-bot) ---")
def tab(name, keyf, buckets):
    print(f"  {name}")
    for lab, f in buckets:
        sub = [p for p in SEED if f(keyf(p))]
        if len(sub) < 30:
            continue
        k = sum(1 for p in sub if p["new_coex_30"] >= 1)
        print(f"    {lab:<16} {k:>5}/{len(sub):<5} = {k/len(sub):6.1%}")

tab("planter's loiter inside d2<=36 before the plant", lambda p: p["loiter36"],
    [("0-1", lambda v: v <= 1), ("2-4", lambda v: 2 <= v <= 4),
     ("5-9", lambda v: 5 <= v <= 9), ("10-19", lambda v: 10 <= v <= 19),
     ("20-49", lambda v: 20 <= v <= 49), ("50+", lambda v: v >= 50)])
tab("enemy builders in zone at t-1", lambda p: p["nb36_m1"],
    [(str(i), lambda v, i=i: v == i) for i in range(5)] +
    [("5+", lambda v: v >= 5)])
tab("round the seed was planted", lambda p: p["rnd"],
    [("r0-50", lambda v: v <= 50), ("r51-150", lambda v: 51 <= v <= 150),
     ("r151-300", lambda v: 151 <= v <= 300), ("r301+", lambda v: v >= 301)])
tab("d2 of the seed tile", lambda p: p["d2"],
    [("<=8 near", lambda v: v <= 8), ("9-17 mid", lambda v: 9 <= v <= 17),
     ("18-32 far", lambda v: v >= 18)])
tab("seed kind", lambda p: p["kind"],
    [("gunner", lambda v: v == "gunner"), ("sentinel", lambda v: v == "sentinel")])
tab("we won that game", lambda p: p["won"],
    [("lost", lambda v: v == 0), ("won", lambda v: v == 1)])

print("\n--- loiter inversion: does it survive stratification? ---")
for lab, sub in (("round <=50", [p for p in SEED if p["rnd"] <= 50]),
                 ("round 51-150", [p for p in SEED if 51 <= p["rnd"] <= 150]),
                 ("round 151-300", [p for p in SEED if 151 <= p["rnd"] <= 300]),
                 ("round 301+", [p for p in SEED if p["rnd"] >= 301]),
                 ("games we WON", [p for p in SEED if p["won"] == 1]),
                 ("games we LOST", [p for p in SEED if p["won"] == 0]),
                 ("first plant on that tile", [p for p in SEED if p["reuse_idx"] == 1]),
                 ("seat 0", [p for p in SEED if p["seat"] == 0]),
                 ("seat 1", [p for p in SEED if p["seat"] == 1])):
    a = [p for p in sub if p["loiter36"] >= 10]
    b = [p for p in sub if p["loiter36"] < 10]
    if len(a) < 30 or len(b) < 30:
        continue
    ka = sum(1 for p in a if p["new_coex_30"] >= 1)
    kb = sum(1 for p in b if p["new_coex_30"] >= 1)
    print(f"  {lab:<26} loiter>=10 {ka/len(a):6.1%} (n={len(a):<5}) vs "
          f"loiter<10 {kb/len(b):6.1%} (n={len(b):<5})  "
          f"{(ka/len(a)-kb/len(b))*100:+6.1f}pp z={ztest(ka,len(a),kb,len(b)):.2f}")

print("\n--- HOW MUCH TIME DOES THE SEED ITSELF BUY US ---")
# lag from seed to the second turret, among nests
lags = []
# recompute lag: we only stored counts, so use the corpus-independent proxy:
# nests where the second turret arrived within w rounds
print("  cumulative share of seeds that have a 2nd distinct-tile turret within:")
for w in (5, 10, 15, 20, 30):
    # new_coex_30 counts a 30-round window; recompute needs the decoder, so
    # report the 30-round total and the two sub-windows we do have below.
    pass
print("    (see a5_lag.py -- lag needs the decoder, run separately)")

print("\n--- would 'kill the seed fast' prevent the nest? ---")
# among nests, was the seed still alive when the 2nd turret landed?  new_coex
# requires coexistence by construction, so compare against new_x0_30.
n_x0 = sum(1 for p in SEED if p["new_x0_30"] >= 1)
n_cx = sum(1 for p in SEED if p["new_coex_30"] >= 1)
print(f"  seeds with a 2nd distinct-tile turret within 30 rounds: {n_x0} "
      f"({n_x0/len(SEED):.1%})")
print(f"  ... of which the seed was still alive when it landed: {n_cx} "
      f"({n_cx/n_x0:.1%} of those)")
print(f"  ... so {n_x0-n_cx} ({1-n_cx/n_x0:.1%}) second turrets arrived after "
      f"the seed was already dead -- killing the seed did not stop them")
