#!/usr/bin/env python3
"""Confounding: opponent VERSION, MAP, SEAT, and our own bot version."""
import csv, collections, math, statistics

S = ("/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/"
     "628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/oppnest/")
B = "/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/oppnest/snap/"

LM = {r["id"]: r for r in csv.DictReader(open(B + "league_matches.tsv"),
                                         delimiter="\t")}
seeds = list(csv.DictReader(open(S + "seeds.tsv"), delimiter="\t"))
for s in seeds:
    s["nest"] = int(s["nest"]); s["seat"] = int(s["seat"])
    r = LM.get(s["match"])
    v = None
    if r:
        for side in ("A", "B"):
            if r[f"team{side}Name"] == s["opp"]:
                v = r[f"team{side}Version"]
    s["ov"] = v

cov = sum(1 for s in seeds if s["ov"])
print(f"seeds {len(seeds)}; opponent VERSION recovered from "
      f"league_matches.tsv for {cov} ({cov/len(seeds):.1%})\n")


def tab(rows, key):
    d = collections.defaultdict(lambda: [0, 0, set()])
    for r in rows:
        d[key(r)][0] += r["nest"]; d[key(r)][1] += 1; d[key(r)][2].add(r["match"])
    return d


def z2(k1, n1, k2, n2):
    if not n1 or not n2:
        return 0.0
    p = (k1 + k2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    return (k1 / n1 - k2 / n2) / se if se else 0.0


# ---------- 1. OPPONENT VERSION -------------------------------------------
print("=== nest rate by OPPONENT VERSION, within opponent ===")
print("(m = distinct matches on that version; a version is one bot submission)")
big = [o for o, v in tab(seeds, lambda r: r["opp"]).items() if v[1] >= 60]
wv_num = wv_den = 0.0
for o in sorted(big):
    rows = [s for s in seeds if s["opp"] == o and s["ov"]]
    if not rows:
        continue
    t = tab(rows, lambda r: r["ov"])
    if len(t) < 2:
        tot = sum(v[1] for v in t.values())
        print(f"{o:<24} SINGLE VERSION {list(t)[0]:>4}  n={tot}")
        continue
    parts = sorted(t.items(), key=lambda kv: -kv[1][1])
    tot_k = sum(v[0] for _, v in parts); tot_n = sum(v[1] for _, v in parts)
    gm = tot_k / tot_n
    var = sum(v[1] * (v[0] / v[1] - gm) ** 2 for _, v in parts) / tot_n
    wv_num += var * tot_n; wv_den += tot_n
    desc = "  ".join(f"v{k}:{v[0]/v[1]:.0%}(n={v[1]},m={len(v[2])})"
                     for k, v in parts if v[1] >= 15)
    print(f"{o:<24} pooled {gm:.1%} (n={tot_n})  {desc}")
print(f"\nmean within-opponent BETWEEN-VERSION variance = {wv_num/wv_den:.5f}")

# same quantity computed between MATCHES within (opponent,version) -> noise floor
num = den = 0.0
for (o, v), rows in collections.defaultdict(list, {
        k: [s for s in seeds if (s["opp"], s["ov"]) == k]
        for k in {(s["opp"], s["ov"]) for s in seeds if s["ov"]}}).items():
    t = tab(rows, lambda r: r["match"])
    if len(t) < 2:
        continue
    tk = sum(x[0] for x in t.values()); tn = sum(x[1] for x in t.values())
    gm = tk / tn
    num += sum(x[1] * (x[0] / x[1] - gm) ** 2 for x in t.values()); den += tn
print(f"between-MATCH variance within (opponent,version) = {num/den:.5f}"
      "   <- the noise floor")
tot = tab(seeds, lambda r: r["opp"])
tk = sum(v[0] for v in tot.values()); tn = sum(v[1] for v in tot.values())
gm = tk / tn
bo = sum(v[1] * (v[0] / v[1] - gm) ** 2 for v in tot.values() if v[1] >= 60) / \
     sum(v[1] for v in tot.values() if v[1] >= 60)
print(f"BETWEEN-OPPONENT variance (opponents with n>=60)   = {bo:.5f}")

# ---------- 2. MAP ---------------------------------------------------------
print("\n=== MAP ===")
mt = tab(seeds, lambda r: r["map"])
for m, v in sorted(mt.items(), key=lambda kv: -kv[1][0] / max(kv[1][1], 1)):
    if v[1] >= 80:
        print(f"  {m:<12}{v[0]/v[1]:>7.1%}  n={v[1]:<6} matches={len(v[2])}")
# how concentrated is each opponent's map mix?
print("\n  map concentration per big opponent (share of seeds on top map):")
for o in sorted(big):
    rows = [s for s in seeds if s["opp"] == o]
    c = collections.Counter(r["map"] for r in rows)
    top, n = c.most_common(1)[0]
    print(f"    {o:<24} {len(c):>3} maps, top {top} {n/len(rows):.0%}")

# indirect standardisation: expected nest rate from each opponent's map mix
print("\n  opponent rate OBSERVED vs EXPECTED-from-map-mix (indirect standardisation):")
maprate = {m: v[0] / v[1] for m, v in mt.items()}
for o in sorted(big, key=lambda o: -tot[o][0] / tot[o][1]):
    rows = [s for s in seeds if s["opp"] == o]
    exp = statistics.mean(maprate[r["map"]] for r in rows)
    obs = sum(r["nest"] for r in rows) / len(rows)
    print(f"    {o:<24} obs {obs:>6.1%}  exp {exp:>6.1%}  O/E {obs/exp:>5.2f}"
          f"   n={len(rows)}")

# within-map opponent contrast on the maps we see most
print("\n  WITHIN-MAP opponent spread (maps with >=4 big opponents present):")
for m, v in sorted(mt.items(), key=lambda kv: -kv[1][1])[:8]:
    per = [(o, sum(r["nest"] for r in seeds if r["opp"] == o and r["map"] == m),
            sum(1 for r in seeds if r["opp"] == o and r["map"] == m))
           for o in big]
    per = [p for p in per if p[2] >= 15]
    if len(per) < 4:
        continue
    per.sort(key=lambda p: -p[1] / p[2])
    s_ = "  ".join(f"{o.split()[0][:10]}:{k/n:.0%}(n={n})" for o, k, n in per)
    print(f"    {m:<11} n={v[1]:<5} {s_}")

# ---------- 3. SEAT --------------------------------------------------------
print("\n=== SEAT (our_team index; 0 = NW-ish core) ===")
st = tab(seeds, lambda r: r["seat"])
for k in (0, 1):
    v = st[k]
    print(f"  seat {k}: {v[0]/v[1]:.1%}  n={v[1]}  matches={len(v[2])}")
print(f"  z = {z2(st[0][0], st[0][1], st[1][0], st[1][1]):.2f}")
print("  per-opponent seat split:")
for o in sorted(big):
    r0 = [s for s in seeds if s["opp"] == o and s["seat"] == 0]
    r1 = [s for s in seeds if s["opp"] == o and s["seat"] == 1]
    if len(r0) < 20 or len(r1) < 20:
        continue
    a = sum(x["nest"] for x in r0) / len(r0)
    b = sum(x["nest"] for x in r1) / len(r1)
    print(f"    {o:<24} seat0 {a:>6.1%}(n={len(r0)})  seat1 {b:>6.1%}"
          f"(n={len(r1)})  {(b-a)*100:+5.1f}pp")

# ---------- 4. OUR OWN VERSION --------------------------------------------
print("\n=== OUR bot version (confounded with ladder time and opponent mix) ===")
ot = tab(seeds, lambda r: int(r["ourver"]))
for k, v in sorted(ot.items()):
    if v[1] >= 60:
        print(f"  ourver {k}: {v[0]/v[1]:>6.1%}  n={v[1]:<5} matches={len(v[2])}")
