#!/usr/bin/env python3
"""Q1/Q2/Q3/Q4: loiter, approach, multiplicity, visibility -- nest vs lone."""
import csv, collections, math, statistics as st
S = "/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/precursor/"
B = "/Users/junghard/Projects/Work/florent-code-game/corpus/"

J = {r["file"]: r for r in csv.DictReader(open(B + "join.tsv"), delimiter="\t")}
P = list(csv.DictReader(open(S + "plants2.tsv"), delimiter="\t"))
for p in P:
    for k in ("rnd", "d2", "pid", "ncand", "plt_d2", "loiter32", "loiter36",
              "loiter50", "zone_total", "age", "ep_len", "ep_other_builds",
              "ep_entry_d2", "moves_w10", "mind2_w10", "closing_w10",
              "nb32_m1", "nb36_m1", "nb32_max_w10", "nb36_max_w10",
              "nb36_max_loiter", "nb36_distinct_w10", "vis_oth_m1",
              "pre_t8", "pre_gs8", "new_t8_30", "new_gs8_30", "new_x0_30",
              "new_coex_30", "died", "drnd",
              "lastrnd", "reuse_idx", "seat", "ep_throw_in"):
        p[k] = int(p[k])
    p["vis_oth_frac"] = float(p["vis_oth_frac"])
    j = J[p["file"]]
    p["opp"] = j["opp"]; p["map"] = j["map"]; p["won"] = int(j["won"])

print(f"plants: {len(P)}")

# ---- population for the nest question -------------------------------------
# a SEED plant = no enemy turret already within d2<=8 at plant time.
# NEST = at least one further enemy turret built within d2<=8 in the next 30 rnd
# (so >=2 turrets within d2<=8 inside 30 rounds, counting the seed).
# 30 rounds of game must actually remain, else the label is right-censored.
EL = [p for p in P if p["lastrnd"] - p["rnd"] >= 30]
SEED = [p for p in EL if p["pre_t8"] == 0]
print(f"  with >=30 rounds of game left: {len(EL)}")
print(f"  of those, SEED (no enemy turret already within d2<=8): {len(SEED)}")
NEST = [p for p in SEED if p["new_coex_30"] >= 1]
LONE = [p for p in SEED if p["new_coex_30"] == 0]
print(f"  -> becomes a NEST within 30 rounds: {len(NEST)}   stays LONE: {len(LONE)}")


def q(v):
    v = sorted(v)
    n = len(v)
    if not n:
        return "n=0"
    def pct(x):
        return v[min(n - 1, int(x * n))]
    return (f"n={n} p10={pct(.10)} p25={pct(.25)} med={pct(.50)} "
            f"p75={pct(.75)} p90={pct(.90)} mean={sum(v)/n:.1f}")


def share(rows, pred):
    n = len(rows)
    k = sum(1 for r in rows if pred(r))
    return k, n, (k / n if n else 0)


def ztest(k1, n1, k2, n2):
    if not n1 or not n2:
        return 0.0
    p1, p2 = k1 / n1, k2 / n2
    p = (k1 + k2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    return (p1 - p2) / se if se else 0.0


def mh(rows, grp, out):
    """Mantel-Haenszel OR of out vs grp, stratified by replay file."""
    a = b = c = d = 0.0
    byf = collections.defaultdict(list)
    for r in rows:
        byf[r["file"]].append(r)
    num = den = 0.0
    strata = 0
    for f, rs in byf.items():
        n11 = sum(1 for r in rs if grp(r) and out(r))
        n10 = sum(1 for r in rs if grp(r) and not out(r))
        n01 = sum(1 for r in rs if not grp(r) and out(r))
        n00 = sum(1 for r in rs if not grp(r) and not out(r))
        n = n11 + n10 + n01 + n00
        if (n11 + n10) == 0 or (n01 + n00) == 0 or (n11 + n01) == 0 or (n10 + n00) == 0:
            continue
        strata += 1
        num += n11 * n00 / n
        den += n10 * n01 / n
    return (num / den if den else float("nan")), strata


print("\n=== Q1  LOITER (consecutive rounds the planting builder had already")
print("        spent inside d2<=36 of our core, uncensored) ===")
for lab, rows in (("NEST-seed", NEST), ("LONE-seed", LONE)):
    print(f"  {lab:10s} loiter36  {q([p['loiter36'] for p in rows])}")
for lab, rows in (("NEST-seed", NEST), ("LONE-seed", LONE)):
    print(f"  {lab:10s} loiter32  {q([p['loiter32'] for p in rows])}")
print("  loiter36 >= T, share:")
print(f"    {'T':>4} {'NEST':>18} {'LONE':>18} {'diff':>8} {'z':>7}")
for T in (1, 2, 3, 5, 10, 20, 30, 50, 100):
    k1, n1, s1 = share(NEST, lambda r: r["loiter36"] >= T)
    k2, n2, s2 = share(LONE, lambda r: r["loiter36"] >= T)
    print(f"    {T:>4} {k1:>6}/{n1:<6}{s1:>6.1%} {k2:>6}/{n2:<6}{s2:>6.1%} "
          f"{(s1-s2)*100:>+7.1f}pp {ztest(k1,n1,k2,n2):>7.2f}")
orr, ns = mh(SEED, lambda r: r["loiter36"] >= 10, lambda r: r["new_coex_30"] >= 1)
print(f"  within-replay MH-OR, loiter36>=10 -> nest: {orr:.3f} over {ns} informative replays")

print("\n=== Q2  APPROACH ===")
for nm, key in (("age (rounds since spawn)", "age"),
                ("zone_total (all rounds ever in d2<=36)", "zone_total"),
                ("ep_len (this visit's length incl. plant round)", "ep_len"),
                ("ep_entry_d2 (d2 on entering the zone)", "ep_entry_d2"),
                ("moves_w10 (move events in the 10 rounds before)", "moves_w10"),
                ("closing_w10 (d2 drop across the 10-round window)", "closing_w10"),
                ("mind2_w10", "mind2_w10"),
                ("plt_d2 (planter's own d2 when it built)", "plt_d2"),
                ("d2 of the planted tile", "d2")):
    a = [p[key] for p in NEST if p[key] > -9000]
    b = [p[key] for p in LONE if p[key] > -9000]
    print(f"  {nm}\n      NEST {q(a)}\n      LONE {q(b)}")
k1, n1, s1 = share(NEST, lambda r: r["ep_throw_in"] == 1)
k2, n2, s2 = share(LONE, lambda r: r["ep_throw_in"] == 1)
print(f"  arrived in the zone by LAUNCHER THROW: NEST {k1}/{n1} {s1:.1%} | "
      f"LONE {k2}/{n2} {s2:.1%}  z={ztest(k1,n1,k2,n2):.2f}")
k1, n1, s1 = share(NEST, lambda r: r["ep_other_builds"] > 0)
k2, n2, s2 = share(LONE, lambda r: r["ep_other_builds"] > 0)
print(f"  built a NON-turret building in the zone earlier this visit: "
      f"NEST {k1}/{n1} {s1:.1%} | LONE {k2}/{n2} {s2:.1%}  z={ztest(k1,n1,k2,n2):.2f}")

print("\n=== Q3  MULTIPLICITY (distinct enemy builders inside d2<=36) ===")
for nm, key in (("at t-1 (nb36_m1)", "nb36_m1"),
                ("max concurrent over the 10 rounds before", "nb36_max_w10"),
                ("DISTINCT bots seen over the 10 rounds before", "nb36_distinct_w10"),
                ("max concurrent over the whole loiter", "nb36_max_loiter"),
                ("at t-1 inside the plant band d2<=32", "nb32_m1")):
    print(f"  {nm}\n      NEST {q([p[key] for p in NEST])}\n"
          f"      LONE {q([p[key] for p in LONE])}")
print("  P(nest) by number of enemy builders in the zone at t-1:")
byn = collections.defaultdict(lambda: [0, 0])
for p in SEED:
    c = byn[min(p["nb36_m1"], 5)]
    c[1] += 1
    c[0] += 1 if p["new_coex_30"] >= 1 else 0
for k in sorted(byn):
    a, n = byn[k]
    print(f"    {k}{'+' if k==5 else ' '} builders: {a}/{n} = {a/n:6.1%}")

print("\n=== Q4  WAS IT VISIBLE TO US (reconstructed from positions) ===")
k1, n1, s1 = share(SEED, lambda r: r["d2"] <= 36)
print(f"  plant tiles inside our CORE's own vision radius (d2<=36): {s1:.2%} "
      f"({k1}/{n1}) -- by construction, the band is d2<=32")
kk, nn, ss = share([p for p in P if p["plt_d2"] >= 0],
                   lambda r: r["plt_d2"] <= 36)
print(f"  the PLANTER itself stood inside core vision when it built: {ss:.2%} ({kk}/{nn})")
for lab, rows in (("NEST-seed", NEST), ("LONE-seed", LONE)):
    k1, n1, s1 = share(rows, lambda r: r["vis_oth_m1"] == 1)
    k2, n2, s2 = share(rows, lambda r: r["vis_oth_any"] == "1")
    print(f"  {lab}: seen by one of our NON-core units at t-1 {s1:.1%} ({k1}/{n1}); "
          f"at some point this visit {s2:.1%}")
print("  vis_oth_frac over the visit: NEST", q([p["vis_oth_frac"] for p in NEST]))
print("  vis_oth_frac over the visit: LONE", q([p["vis_oth_frac"] for p in LONE]))

print("\n=== SEAT SPLIT on the headline loiter contrast ===")
for seat in (0, 1):
    ns = [p for p in NEST if p["seat"] == seat]
    ls = [p for p in LONE if p["seat"] == seat]
    k1, n1, s1 = share(ns, lambda r: r["loiter36"] >= 10)
    k2, n2, s2 = share(ls, lambda r: r["loiter36"] >= 10)
    print(f"  seat {seat}: loiter36>=10  NEST {s1:.1%} (n={n1}) vs LONE {s2:.1%} (n={n2})"
          f"   nest rate {len(ns)/(len(ns)+len(ls)):.1%}")

print("\n=== HOT-TILE DEDUPLICATION (first plant per (game,tile)) ===")
D = [p for p in SEED if p["reuse_idx"] == 1]
DN = [p for p in D if p["new_coex_30"] >= 1]
DL = [p for p in D if p["new_coex_30"] == 0]
print(f"  seeds after dedup: {len(D)}  nest {len(DN)}  lone {len(DL)}")
print(f"  loiter36 NEST {q([p['loiter36'] for p in DN])}")
print(f"  loiter36 LONE {q([p['loiter36'] for p in DL])}")
for T in (5, 10, 20):
    k1, n1, s1 = share(DN, lambda r: r["loiter36"] >= T)
    k2, n2, s2 = share(DL, lambda r: r["loiter36"] >= T)
    print(f"    T={T:>3}: NEST {s1:.1%} ({k1}/{n1})  LONE {s2:.1%} ({k2}/{n2})  "
          f"{(s1-s2)*100:+.1f}pp z={ztest(k1,n1,k2,n2):.2f}")

print("\n=== CONFOUND: do we lose the games where nests form? ===")
for lab, rows in (("NEST-seed", NEST), ("LONE-seed", LONE)):
    k, n, s = share(rows, lambda r: r["won"] == 1)
    print(f"  {lab}: plant occurred in a game we WON {s:.1%} ({k}/{n})")
byo = collections.defaultdict(lambda: [0, 0])
for p in SEED:
    c = byo[p["opp"]]
    c[1] += 1
    c[0] += 1 if p["new_coex_30"] >= 1 else 0
print("  nest rate by opponent (>=100 seeds):")
for o, (a, n) in sorted(byo.items(), key=lambda kv: -kv[1][0] / max(1, kv[1][1])):
    if n >= 100:
        print(f"    {o:<22} {a/n:6.1%}  (n={n})")
