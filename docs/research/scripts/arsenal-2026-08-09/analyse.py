#!/usr/bin/env python3
"""Arsenal analysis: prices the six items off the arsenal decode + join.tsv."""
import csv
import statistics as st
import sys
from collections import defaultdict, Counter

OUT, FROZ = sys.argv[1], sys.argv[2]


def rd(p):
    with open(p) as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


J = {r["file"]: r for r in rd(f"{FROZ}/join.tsv")}


def side(r):
    """US / THEM label for a (file, team) row."""
    j = J.get(r["file"])
    if not j:
        return None
    return "US" if r["team"] == j["our_team"] else "THEM"


def pct(a, b):
    return f"{100*a/b:.2f}%" if b else "n/a"


def q(xs, p):
    if not xs:
        return None
    xs = sorted(xs)
    i = min(len(xs) - 1, int(p * len(xs)))
    return xs[i]


def hdr(t):
    print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)


# =========================================================================== #
hdr("ITEM 1 — THE FULL LOCK: ring occupancy census")
ring = rd(f"{OUT}/ars_ring.tsv")
by = defaultdict(list)
for r in ring:
    s = side(r)
    if s:
        by[s].append(r)
print(f"team-sides: US {len(by['US'])}  THEM {len(by['THEM'])}  "
      f"total {len(by['US'])+len(by['THEM'])}")

print("\n(a) MAX HOSTILE occupancy of the 12-tile spawn ring, per team-side")
print("    (hostile = an entity of the OTHER team on a ring tile)")
print(f"    {'k':>3} | {'US sides >=k':>13} {'':>8} | {'THEM sides >=k':>15}")
for k in range(0, 13):
    u = sum(1 for r in by["US"] if int(r["hst12_max"]) >= k)
    t = sum(1 for r in by["THEM"] if int(r["hst12_max"]) >= k)
    print(f"    {k:>3} | {u:>13} {pct(u,len(by['US'])):>8} | "
          f"{t:>7} {pct(t,len(by['THEM'])):>8}")

print("\n(b) MAX occupancy by ANY entity (own buildings included) — 12-ring")
for k in (6, 8, 10, 11, 12):
    u = sum(1 for r in by["US"] if int(r["occ12_max"]) >= k)
    t = sum(1 for r in by["THEM"] if int(r["occ12_max"]) >= k)
    print(f"    >={k:<3} US {u:>5} {pct(u,len(by['US'])):>8}   "
          f"THEM {t:>5} {pct(t,len(by['THEM'])):>8}")

print("\n(c) MAX HOSTILE occupancy of the 8 ORTHOGONALS (heal + delivery lock)")
for k in range(0, 9):
    u = sum(1 for r in by["US"] if int(r["hst8_max"]) >= k)
    t = sum(1 for r in by["THEM"] if int(r["hst8_max"]) >= k)
    print(f"    >={k:<3} US {u:>5} {pct(u,len(by['US'])):>8}   "
          f"THEM {t:>5} {pct(t,len(by['THEM'])):>8}")

print("\n(d) hostile ring occupancy: BODIES vs BUILDINGS (max, pooled)")
allr = by["US"] + by["THEM"]
print(f"    max hostile BODIES on the 12-ring, distribution:")
c = Counter(int(r["hstbody12_max"]) for r in allr)
for k in sorted(c):
    print(f"       {k:>2}: {c[k]:>5}  {pct(c[k],len(allr))}")
c = Counter(int(r["hstbldg12_max"]) for r in allr)
print(f"    max hostile BUILDINGS on the 12-ring, distribution:")
for k in sorted(c):
    print(f"       {k:>2}: {c[k]:>5}  {pct(c[k],len(allr))}")

print("\n(e) WHAT HAPPENED TO THE CORE, conditional on max hostile 12-ring occ")
print(f"    {'occ':>5} {'sides':>7} {'core died':>10} {'share':>8} "
      f"{'med rnds first-reach -> death':>30}")
for lo, hi in ((0, 0), (1, 1), (2, 2), (3, 3), (4, 5), (6, 7), (8, 12)):
    sub = [r for r in allr if lo <= int(r["hst12_max"]) <= hi]
    if not sub:
        continue
    dead = [r for r in sub if int(r["core_dead_rnd"]) >= 0]
    # first round the side reached its own max bucket lower bound
    lags = []
    key = {0: None, 1: "f_hst12_1", 2: "f_hst12_2", 3: "f_hst12_3",
           4: "f_hst12_4", 6: "f_hst12_6", 8: "f_hst12_8"}[lo]
    if key:
        for r in dead:
            f = int(r[key])
            if f >= 0:
                lags.append(int(r["core_dead_rnd"]) - f)
    lab = f"{lo}" if lo == hi else f"{lo}-{hi}"
    m = f"{st.median(lags):.0f} (n={len(lags)})" if lags else "-"
    print(f"    {lab:>5} {len(sub):>7} {len(dead):>10} "
          f"{pct(len(dead),len(sub)):>8} {m:>30}")

print("\n(f) CONTROL: base rate of core death, and of death inside r250")
dead = [r for r in allr if int(r["core_dead_rnd"]) >= 0]
d250 = [r for r in dead if int(r["core_dead_rnd"]) < 250]
print(f"    cores destroyed at all : {len(dead)}/{len(allr)} "
      f"{pct(len(dead),len(allr))}")
print(f"    ...inside round 250    : {len(d250)}/{len(allr)} "
      f"{pct(len(d250),len(allr))}")
for s in ("US", "THEM"):
    dd = [r for r in by[s] if int(r["core_dead_rnd"]) >= 0]
    d2 = [r for r in dd if int(r["core_dead_rnd"]) < 250]
    print(f"    {s:<4} core died {len(dd):>5} {pct(len(dd),len(by[s])):>8}  "
          f"| inside r250 {len(d2):>4} {pct(len(d2),len(by[s])):>8}")

print("\n(g) SELF-LOCK: a team's OWN buildings on its own 12-ring")
c = Counter(int(r["ownb12_max"]) for r in allr)
print("    max own-building ring occupancy:", dict(sorted(c.items())))
z = [r for r in allr if int(r["n_free0"]) > 0]
print(f"    sides with >=1 round of ZERO free spawn slots: {len(z)}/{len(allr)} "
      f"{pct(len(z),len(allr))}")
if z:
    n = [int(r["n_free0"]) for r in z]
    print(f"    rounds spent fully spawn-locked: median {st.median(n):.0f} "
          f"p90 {q(n,0.9)} max {max(n)}")

# =========================================================================== #
hdr("ITEM 2 + 3 — KIDNAP OPPORTUNITY (rounds < 250)")
kid = rd(f"{OUT}/ars_kid.tsv")
kby = defaultdict(list)
for r in kid:
    s = side(r)
    if s:
        kby[s].append(r)
for s in ("US", "THEM"):
    R = kby[s]
    tot = sum(int(r["opp_bot_rounds"]) for r in R)
    ka = sum(int(r["k_any"]) for r in R)
    kr = sum(int(r["k_reach"]) for r in R)
    kn = sum(int(r["k_reach_next"]) for r in R)
    fa = sum(int(r["ff_their_ray_any"]) for r in R)
    fl = sum(int(r["ff_their_line_any"]) for r in R)
    flr = sum(int(r["ff_their_line_reach"]) for r in R)
    fo = sum(int(r["ff_ours_line_reach"]) for r in R)
    lb = sum(int(r["launchers_built_lt250"]) for r in R)
    tm = sum(int(r["throws_made_lt250"]) for r in R)
    print(f"\n  {s} as the KIDNAPPER (n={len(R)} sides)")
    print(f"    enemy-builder-rounds observed, r<250      : {tot:>9}")
    print(f"    ...an empty tile adjacent to it (any)     : {ka:>9} {pct(ka,tot)}")
    print(f"    ...that tile ALSO adjacent to our builder : {kr:>9} {pct(kr,tot)}")
    print(f"    ...and the same bot still there next rnd  : {kn:>9} {pct(kn,tot)}")
    print(f"    THEIR turret RAY reachable from some L    : {fa:>9} {pct(fa,tot)}")
    print(f"    THEIR live blocked LINE, any L            : {fl:>9} {pct(fl,tot)}")
    print(f"    THEIR live LINE, L we can actually build  : {flr:>9} {pct(flr,tot)}")
    print(f"    OUR  live LINE, L we can actually build   : {fo:>9} {pct(fo,tot)}")
    print(f"    launchers this side built before r250     : {lb:>9} "
          f"({lb/len(R):.2f}/side)")
    print(f"    throws this side RECEIVED before r250     : {tm:>9}")
    rr = [int(r["rnds_reach"]) for r in R]
    ff = [int(r["rnds_ff"]) for r in R]
    br = [int(r["bots_reach"]) for r in R]
    bf = [int(r["bots_ff"]) for r in R]
    print(f"    per game: rounds with >=1 reachable kidnap  "
          f"median {st.median(rr):.0f} p75 {q(rr,.75)} p90 {q(rr,.90)} max {max(rr)}")
    print(f"    per game: rounds with >=1 friendly-fire one "
          f"median {st.median(ff):.0f} p75 {q(ff,.75)} p90 {q(ff,.90)} max {max(ff)}")
    print(f"    per game: distinct enemy bots kidnappable  "
          f"median {st.median(br):.0f} p90 {q(br,.90)} max {max(br)}")
    print(f"    per game: distinct enemy bots -> their line "
          f"median {st.median(bf):.0f} p90 {q(bf,.90)} max {max(bf)}")
    z = sum(1 for x in rr if x == 0)
    zf = sum(1 for x in ff if x == 0)
    print(f"    games with ZERO reachable kidnap rounds   : {z}/{len(R)} "
          f"{pct(z,len(R))}")
    print(f"    games with ZERO friendly-fire rounds      : {zf}/{len(R)} "
          f"{pct(zf,len(R))}")

# =========================================================================== #
hdr("ITEM 4 — ORE POISONING")
mp = {r["file"]: r for r in rd(f"{OUT}/ars_map.tsv")}
ore = rd(f"{OUT}/ars_ore.tsv")
per = defaultdict(list)
for r in ore:
    per[(r["file"], r["team"])].append(r)
rows = defaultdict(list)
for (f, t), rs in per.items():
    j = J.get(f)
    if not j:
        continue
    s = "US" if t == j["our_team"] else "THEM"
    n = [int(x["n_built"]) for x in rs]
    n.sort(reverse=True)
    tot = sum(n)
    rows[s].append((len(rs), tot, n[0] / tot, sum(n[:3]) / tot,
                    j["opp"], f, t))
print(f"map ore census (n={len(mp)} files): "
      f"mean ore tiles {st.mean(int(r['n_ore']) for r in mp.values()):.1f}, "
      f"median {st.median(int(r['n_ore']) for r in mp.values()):.0f}")
o0 = [int(r["ore_side0"]) for r in mp.values()]
print(f"   ore nearer team-0 core: mean {st.mean(o0):.1f}; "
      f"neutral (equidistant): mean "
      f"{st.mean(int(r['ore_neutral']) for r in mp.values()):.1f}")
for s in ("US", "THEM"):
    R = rows[s]
    d = [x[0] for x in R]
    h = [x[1] for x in R]
    t1 = [x[2] for x in R]
    t3 = [x[3] for x in R]
    print(f"\n  {s} (n={len(R)} team-sides that built >=1 harvester)")
    print(f"    DISTINCT ore tiles harvested : median {st.median(d):.0f}  "
          f"mean {st.mean(d):.2f}  p75 {q(d,.75)}  p90 {q(d,.90)}  max {max(d)}")
    print(f"    harvesters built             : median {st.median(h):.0f}  "
          f"mean {st.mean(h):.2f}  max {max(h)}")
    print(f"    top-1 tile share of harvesters: median {st.median(t1)*100:.1f}%  "
          f"mean {st.mean(t1)*100:.1f}%")
    print(f"    top-3 tile share of harvesters: median {st.median(t3)*100:.1f}%  "
          f"mean {st.mean(t3)*100:.1f}%")
    one = sum(1 for x in d if x == 1)
    le3 = sum(1 for x in d if x <= 3)
    print(f"    sides using exactly 1 tile   : {one} {pct(one,len(R))}")
    print(f"    sides using <=3 tiles        : {le3} {pct(le3,len(R))}")
print("\n  per-opponent distinct-ore-tile use (THEM side, opponents with n>=15)")
po = defaultdict(list)
for x in rows["THEM"]:
    po[x[4]].append(x[0])
for opp, v in sorted(po.items(), key=lambda kv: -len(kv[1])):
    if len(v) < 15:
        continue
    print(f"    {opp:<20} n={len(v):>4}  median {st.median(v):>4.0f}  "
          f"mean {st.mean(v):>5.2f}  max {max(v)}")

trav = rd(f"{OUT}/ars_trav.tsv")
tby = defaultdict(list)
for r in trav:
    s = side(r)
    if s:
        tby[s].append(r)
print("\n  OBSERVED TRAVEL (not straight-line): first round a builder of this "
      "side\n  stood ORTHOGONALLY ADJACENT to an ENEMY-SIDE ore tile")
for s in ("US", "THEM"):
    v = [int(r["r_enemy_ore_adj"]) for r in tby[s]]
    got = [x for x in v if x >= 0]
    lt = lambda k: sum(1 for x in got if x < k)  # noqa: E731
    print(f"    {s:<5} reached at all {len(got)}/{len(v)} {pct(len(got),len(v))}"
          f" | median r{st.median(got):.0f} p25 r{q(got,.25)} p10 r{q(got,.10)}"
          f" | <r50 {pct(lt(50),len(v))} <r100 {pct(lt(100),len(v))} "
          f"<r250 {pct(lt(250),len(v))}")
    v2 = [int(r["r_nearest_enemy_ore"]) for r in tby[s]]
    g2 = [x for x in v2 if x >= 0]
    print(f"          the SINGLE NEAREST enemy-side ore tile: reached "
          f"{len(g2)}/{len(v2)} {pct(len(g2),len(v2))}, median r"
          f"{st.median(g2):.0f}" if g2 else "          nearest: never")
for s in ("US", "THEM"):
    v = [int(r["r_d2_8"]) for r in tby[s]]
    got = [x for x in v if x >= 0]
    print(f"    {s:<5} first round within d2<=8 of the ENEMY CORE: "
          f"{len(got)}/{len(v)} {pct(len(got),len(v))}, median r"
          f"{st.median(got):.0f}, p10 r{q(got,.10)}")

# =========================================================================== #
hdr("ITEM 5 — SPAWN STARVATION")
sp = rd(f"{OUT}/ars_spawn.tsv")
acc = defaultdict(lambda: [0, 0])
acc_all = defaultdict(lambda: [0, 0])
for r in sp:
    s = side(r)
    if not s or r["atcap"] == "1":
        continue
    f = int(r["free"])
    if r["band"] in ("r0-100", "r100-250"):
        a = acc[(s, f)]
        a[0] += int(r["rounds"])
        a[1] += int(r["spawns"])
    b = acc_all[(s, f)]
    b[0] += int(r["rounds"])
    b[1] += int(r["spawns"])
print("  spawns per core-round, by number of FREE spawn-ring tiles at the "
      "start of the round\n  (rounds where the team was at the 50-unit cap are "
      "EXCLUDED)")
for s in ("US", "THEM"):
    print(f"\n  {s}   free | {'rounds r<250':>13} {'spawns':>8} {'rate':>8} "
          f"| {'rounds all':>11} {'spawns':>8} {'rate':>8}")
    for f in range(0, 13):
        a, b = acc[(s, f)], acc_all[(s, f)]
        if b[0] == 0:
            continue
        r1 = f"{a[1]/a[0]:.4f}" if a[0] else "-"
        r2 = f"{b[1]/b[0]:.4f}" if b[0] else "-"
        print(f"       {f:>4} | {a[0]:>13} {a[1]:>8} {r1:>8} "
              f"| {b[0]:>11} {b[1]:>8} {r2:>8}")

# =========================================================================== #
hdr("ITEM 6 — CONVEYOR SIPHON")
fl = rd(f"{OUT}/ars_flow.tsv")
fby = defaultdict(list)
for r in fl:
    s = side(r)
    if s:
        fby[s].append(r)
for s in ("US", "THEM"):
    R = fby[s]
    dl = [int(r["in_core_any"]) * 10 for r in R]
    dn = [int(r["own_net"]) for r in R]
    xt = [int(r["in_core_xteam"]) * 10 for r in R]
    rc = sum(int(r["own_net_reach"]) for r in R)
    rn = sum(int(r["own_net"]) for r in R)
    rc2 = sum(int(r["own_net_reach_lt250"]) for r in R)
    rn2 = sum(int(r["own_net_lt250"]) for r in R)
    cc = sum(int(r["own_core_reach"]) for r in R)
    cn = sum(int(r["own_core"]) for r in R)
    print(f"\n  {s} (n={len(R)} team-sides)")
    print(f"    titanium DELIVERED into own core, per game: median "
          f"{st.median(dl):.0f} Ti  mean {st.mean(dl):.0f}  p90 {q(dl,.9)}  "
          f"max {max(dl)}")
    print(f"    conveyor/splitter HOPS inside own net, per game: median "
          f"{st.median(dn):.0f}  mean {st.mean(dn):.0f}")
    print(f"    ALREADY donated into this side's core by the OTHER team: "
          f"total {sum(xt)} Ti over {len(R)} games; "
          f"games with any: {sum(1 for x in xt if x)} "
          f"{pct(sum(1 for x in xt if x),len(R))}; "
          f"median among those {st.median([x for x in xt if x]):.0f} Ti"
          if any(xt) else "    no cross-team core deliveries")
    print(f"    own-net hops on a tile the ENEMY had already reached: "
          f"{rc}/{rn} = {pct(rc,rn)}  (r<250: {rc2}/{rn2} = {pct(rc2,rn2)})")
    print(f"    into-core hops on a tile the ENEMY had already reached: "
          f"{cc}/{cn} = {pct(cc,cn)}")
    en = [int(r["enemy_net"]) for r in R]
    print(f"    hops this side pushed onto the ENEMY network: total {sum(en)}, "
          f"median/game {st.median(en):.0f}, games with any "
          f"{sum(1 for x in en if x)} {pct(sum(1 for x in en if x),len(R))}")
