#!/usr/bin/env python3
"""Split-half stability of the per-opponent nest rate + leave-one-match-out CV.

Splitting unit is the MATCH (5 games), because games inside a match share
opponent version, day, map pool and our own bot version.
Split A  = interleaved by chronological match order (odd/even rank): balanced
           in time, so it isolates SAMPLING NOISE.
Split B  = chronological halves: adds real drift (their new versions, our new
           versions, rating movement).
"""
import csv, collections, math, random, statistics

S = ("/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/"
     "628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/oppnest/")
B = "/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/oppnest/snap/"

created = {}
for r in csv.DictReader(open(B + "ladder_games.tsv"), delimiter="\t"):
    created[r["match"]] = r["created"]

seeds = list(csv.DictReader(open(S + "seeds.tsv"), delimiter="\t"))
for s in seeds:
    s["nest"] = int(s["nest"])

by_match = collections.defaultdict(lambda: [0, 0])
mopp = {}
for s in seeds:
    by_match[s["match"]][0] += s["nest"]; by_match[s["match"]][1] += 1
    mopp[s["match"]] = s["opp"]
print(f"matches with >=1 seed: {len(by_match)}; "
      f"missing created: {sum(1 for m in by_match if m not in created)}")

opp_m = collections.defaultdict(list)
for m in by_match:
    opp_m[mopp[m]].append(m)
for o in opp_m:
    opp_m[o].sort(key=lambda m: created.get(m, ""))

MINM, MINS = 6, 60
BIG = [o for o in opp_m
       if len(opp_m[o]) >= MINM and sum(by_match[m][1] for m in opp_m[o]) >= MINS]
BIG.sort()
print(f"opponents with >={MINM} matches and >={MINS} seeds: {len(BIG)}  {BIG}\n")


def rate(ms):
    k = sum(by_match[m][0] for m in ms); n = sum(by_match[m][1] for m in ms)
    return (k / n if n else float("nan")), n, k


def pearson(x, y):
    n = len(x)
    mx, my = statistics.mean(x), statistics.mean(y)
    sx = math.sqrt(sum((a - mx) ** 2 for a in x))
    sy = math.sqrt(sum((b - my) ** 2 for b in y))
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy) if sx and sy else float("nan")


def spearman(x, y):
    def rk(v):
        o = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        for pos, i in enumerate(o):
            r[i] = pos
        return r
    return pearson(rk(x), rk(y))


for name, splitter in (
        ("A  interleaved (odd/even chronological rank) - sampling noise only",
         lambda ms: (ms[0::2], ms[1::2])),
        ("B  chronological halves - noise + drift",
         lambda ms: (ms[:len(ms) // 2], ms[len(ms) // 2:]))):
    print(f"=== SPLIT {name} ===")
    print(f"{'opponent':<24}{'h1 rate':>9}{'h1 n':>7}{'h1 m':>5}"
          f"{'h2 rate':>10}{'h2 n':>7}{'h2 m':>5}{'delta':>8}")
    x, y, w = [], [], []
    for o in BIG:
        a, b = splitter(opp_m[o])
        ra, na, _ = rate(a); rb, nb, _ = rate(b)
        print(f"{o:<24}{ra:>9.1%}{na:>7}{len(a):>5}{rb:>10.1%}{nb:>7}{len(b):>5}"
              f"{(rb-ra)*100:>+7.1f}pp")
        x.append(ra); y.append(rb); w.append(min(na, nb))
    print(f"  Pearson r = {pearson(x, y):.3f}   Spearman rho = {spearman(x, y):.3f}"
          f"   (n = {len(x)} opponents)")
    # regression slope h2 ~ h1
    mx, my = statistics.mean(x), statistics.mean(y)
    sl = (sum((a - mx) * (b - my) for a, b in zip(x, y)) /
          sum((a - mx) ** 2 for a in x))
    print(f"  slope(h2 on h1) = {sl:.2f}  (1.0 = perfectly stable, "
          f"0 = pure noise)\n")

# ---- LEAVE-ONE-MATCH-OUT: would a runtime prior have paid? -----------------
print("=== LEAVE-ONE-MATCH-OUT prediction at the SEED level ===")
tot_k = sum(v[0] for v in by_match.values())
tot_n = sum(v[1] for v in by_match.values())
opp_tot = collections.defaultdict(lambda: [0, 0])
for m, (k, n) in by_match.items():
    opp_tot[mopp[m]][0] += k; opp_tot[mopp[m]][1] += n

def score(pred_fn, label):
    br = ll = 0.0; N = 0
    for m, (k, n) in by_match.items():
        p = pred_fn(m, k, n)
        p = min(max(p, 1e-4), 1 - 1e-4)
        br += k * (1 - p) ** 2 + (n - k) * p ** 2
        ll += -(k * math.log(p) + (n - k) * math.log(1 - p))
        N += n
    print(f"  {label:<48} Brier {br/N:.4f}   logloss {ll/N:.4f}   n={N}")
    return br / N

g = score(lambda m, k, n: (tot_k - k) / (tot_n - n), "global base rate (LOMO)")
o = score(lambda m, k, n: ((opp_tot[mopp[m]][0] - k) /
                           (opp_tot[mopp[m]][1] - n))
          if opp_tot[mopp[m]][1] - n > 0 else (tot_k - k) / (tot_n - n),
          "per-opponent prior (LOMO)")
print(f"  Brier skill of the opponent prior over the base rate: "
      f"{(g-o)/g:+.1%}")

# shrunk prior (empirical-Bayes, k0 pseudo-seeds toward the global rate)
for k0 in (10, 25, 50, 100):
    def f(m, k, n, k0=k0):
        kk = opp_tot[mopp[m]][0] - k; nn = opp_tot[mopp[m]][1] - n
        gb = (tot_k - k) / (tot_n - n)
        return (kk + k0 * gb) / (nn + k0)
    score(f, f"shrunk opponent prior (k0={k0})")
