#!/usr/bin/env python3
"""(C) multivariate logistic (L2, plain-python IRLS-free gradient descent),
(E) distance x clustering joint stratification, and
(F) does the surviving tail actually track home harm?
"""
import csv, collections, math, random

D = "/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/tail/"
BASE = "/Users/junghard/Projects/Work/florent-code-game/corpus/"

rows = []
for r in csv.DictReader(open(D + "plants2.tsv"), delimiter="\t"):
    for k in ("our_team", "won", "lastrnd", "rnd", "d2", "died", "life",
              "nb_same8", "nb_sameturret8", "nb_opp8"):
        r[k] = int(r[k])
    r["fu"] = r["lastrnd"] - r["rnd"]
    rows.append(r)

batk = collections.Counter(); bbot = collections.Counter()
for r in csv.DictReader(open(BASE + "build_agg.tsv"), delimiter="\t"):
    if r["metric"] == "batk":
        batk[(r["file"], r["team"])] += int(r["n"])
    elif r["metric"] == "build_builder_bot":
        bbot[(r["file"], r["team"])] += int(r["n"])
for r in rows:
    r["batk_rate"] = batk[(r["file"], str(r["our_team"]))] / max(1, r["lastrnd"])
    r["nbot"] = bbot[(r["file"], str(r["our_team"]))]

T = 200
pop = [r for r in rows if r["side"] == "THEM" and r["fu"] >= T]
for r in pop:
    r["alive"] = 1 if ((not r["died"]) or r["life"] > T) else 0
print(f"model population n={len(pop)} games={len(set(r['file'] for r in pop))} "
      f"alive {sum(r['alive'] for r in pop)/len(pop):.1%}")

# ---------------- (E) distance x clustering joint ----------------
print("\n(E) DISTANCE x CLUSTERING (are they the same variable?)")
print("    cell = alive%% (n)   rows: friendly turrets within d2<=8   cols: d2 bucket")
buck = lambda r: "near<=8" if r["d2"] <= 8 else "mid9-17" if r["d2"] <= 17 else "far18-32"
cl = lambda r: "0turr" if r["nb_sameturret8"] == 0 else "1turr" if r["nb_sameturret8"] == 1 else "2+turr"
tab = collections.defaultdict(lambda: [0, 0])
for r in pop:
    c = tab[(cl(r), buck(r))]
    c[0] += r["alive"]; c[1] += 1
print(f"    {'':8s}" + "".join(f"{b:>18s}" for b in ("near<=8", "mid9-17", "far18-32")))
for c in ("0turr", "1turr", "2+turr"):
    line = f"    {c:8s}"
    for b in ("near<=8", "mid9-17", "far18-32"):
        a, n = tab[(c, b)]
        line += f"{(a/n if n else 0):9.1%} ({n:4d})" if n else f"{'-':>18s}"
    print(line)

# ---------------- (C) logistic regression ----------------
def fit(feat_names, X, y, lam=1.0, iters=4000, lr=0.4):
    k = len(feat_names)
    w = [0.0] * k
    n = len(y)
    for it in range(iters):
        g = [0.0] * k
        for i in range(n):
            xi = X[i]
            z = sum(w[j] * xi[j] for j in range(k))
            p = 1 / (1 + math.exp(-max(-30, min(30, z))))
            e = p - y[i]
            for j in range(k):
                if xi[j]:
                    g[j] += e * xi[j]
        for j in range(k):
            g[j] = g[j] / n + (lam / n) * w[j] * (0 if feat_names[j] == "intercept" else 1)
            w[j] -= lr * g[j] * 10
    return w


def build_design(pop, with_opp=True):
    opps = [o for o, c in collections.Counter(r["opp"] for r in pop).items() if c >= 40]
    opps = sorted(opps)
    names = ["intercept", "d2_z", "sentinel", "turr8_z", "same8_z", "our8_z",
             "rnd_z", "batkrate_z", "won", "seat1", "nbot_z"]
    if with_opp:
        names += ["opp:" + o for o in opps[1:]]

    def z(vals):
        m = sum(vals) / len(vals)
        s = (sum((v - m) ** 2 for v in vals) / len(vals)) ** .5 or 1
        return m, s
    md2 = z([r["d2"] for r in pop]); mt = z([r["nb_sameturret8"] for r in pop])
    ms = z([r["nb_same8"] for r in pop]); mo = z([r["nb_opp8"] for r in pop])
    mr = z([r["rnd"] for r in pop]); mb = z([r["batk_rate"] for r in pop])
    mn = z([r["nbot"] for r in pop])
    X, y = [], []
    for r in pop:
        v = [1.0,
             (r["d2"] - md2[0]) / md2[1],
             1.0 if r["kind"] == "sentinel" else 0.0,
             (r["nb_sameturret8"] - mt[0]) / mt[1],
             (r["nb_same8"] - ms[0]) / ms[1],
             (r["nb_opp8"] - mo[0]) / mo[1],
             (r["rnd"] - mr[0]) / mr[1],
             (r["batk_rate"] - mb[0]) / mb[1],
             float(r["won"]), 1.0 if r["our_team"] == 1 else 0.0,
             (r["nbot"] - mn[0]) / mn[1]]
        if with_opp:
            v += [1.0 if r["opp"] == o else 0.0 for o in opps[1:]]
        X.append(v); y.append(r["alive"])
    return names, X, y, opps


for with_opp in (False, True):
    names, X, y, opps = build_design(pop, with_opp)
    w = fit(names, X, y)
    print(f"\n(C) LOGISTIC {'WITH' if with_opp else 'WITHOUT'} opponent fixed effects "
          f"(n={len(y)}, {len(names)} terms, L2=1). Coefs are per 1 SD for z-scored terms;"
          f" exp(b) = odds ratio.")
    core = [(nm, b) for nm, b in zip(names, w) if not nm.startswith("opp:")]
    for nm, b in sorted(core, key=lambda t: -abs(t[1])):
        if nm == "intercept":
            continue
        print(f"     {nm:12s} b={b:+6.3f}  OR={math.exp(b):5.2f}")
    if with_opp:
        oc = sorted([(nm[4:], b) for nm, b in zip(names, w) if nm.startswith("opp:")],
                    key=lambda t: -t[1])
        print(f"     opponent FE (ref={opps[0]}): "
              f"max {oc[0][0]} b={oc[0][1]:+.2f}, min {oc[-1][0]} b={oc[-1][1]:+.2f}, "
              f"range {oc[0][1]-oc[-1][1]:.2f} log-odds")

# ---------------- (F) does the tail track home harm? ----------------
print("\n(F) HARM LINKAGE: our builder-bot deaths inside our own band (d2_own<=32),"
      " per game, vs number of enemy plants surviving 200+ rounds")
J = {r["file"]: r for r in csv.DictReader(open(BASE + "join.tsv"), delimiter="\t")}
homedeaths = collections.Counter()
with open(BASE + "events.tsv") as f:
    f.readline()
    for line in f:
        p = line.rstrip("\n").split("\t")
        if p[1] != "DEATH" or p[4] != "builder_bot":
            continue
        j = J.get(p[0])
        if not j or p[3] != j["our_team"]:
            continue
        if int(p[7]) <= 32:
            homedeaths[p[0]] += 1
byg = collections.defaultdict(list)
for r in pop:
    byg[r["file"]].append(r)
buckets = collections.defaultdict(list)
for f, v in byg.items():
    s = sum(x["alive"] for x in v)
    buckets[min(s, 5)].append(homedeaths.get(f, 0))
print("    surviving plants (>=200r) in game -> mean OUR builder deaths at home")
for k in sorted(buckets):
    v = buckets[k]
    print(f"      {k}{'+' if k==5 else ' '} survivors: games={len(v):4d}  "
          f"mean home builder deaths {sum(v)/len(v):6.1f}")
# correlation
xs = []; ys = []
for f, v in byg.items():
    xs.append(sum(x["alive"] for x in v)); ys.append(homedeaths.get(f, 0))
mx = sum(xs)/len(xs); my = sum(ys)/len(ys)
cov = sum((a-mx)*(b-my) for a, b in zip(xs, ys))
sx = math.sqrt(sum((a-mx)**2 for a in xs)); sy = math.sqrt(sum((b-my)**2 for b in ys))
print(f"    Pearson r = {cov/(sx*sy):.3f} over {len(xs)} games")
