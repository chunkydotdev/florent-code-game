#!/usr/bin/env python3
"""s51 CRATER-vs-SWEEP -- cuts over scratchpad/s51_route/route_games.tsv.

Usage: analyse.py <cut> [...]
  guards      instrument cross-checks that must produce BOTH verdicts
  permap      per-map opening/route table
  contrast    crater trio vs sweep pair, column by column
  pair        royale vs yulerune matched pair
  chain       ranked failure chain on crater losses
  ferry       the ferry / greedy-descent cut
"""
from __future__ import annotations

import math
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
TSV = HERE / "route_games.tsv"
SWEEP = ["ragnarok", "royale"]
CRATER = ["icefloe", "auroraveil", "yulerune"]
ORDER = ["ragnarok", "royale", "nordkap", "frostgate", "drakkarfjord",
         "midgard", "valkyrie", "antler", "archipelago", "fjordgate",
         "drumlin", "glacierkeep", "yulerune", "auroraveil", "icefloe"]
DEFF = 1.130   # measured on THIS fixture's (map,seed) pairs -- ring study 3


def load():
    rows = []
    with open(TSV) as f:
        hdr = f.readline().rstrip("\n").split("\t")
        for ln in f:
            d = dict(zip(hdr, ln.rstrip("\n").split("\t")))
            for k, v in list(d.items()):
                try:
                    d[k] = int(v)
                except ValueError:
                    try:
                        d[k] = float(v)
                    except ValueError:
                        pass
            rows.append(d)
    return rows


def mean(xs):
    xs = [x for x in xs if isinstance(x, (int, float))]
    return sum(xs) / len(xs) if xs else float("nan")


def share_ci(k, n, deff=DEFF):
    if not n:
        return 0.0, 0.0
    p = k / n
    hw = 1.96 * math.sqrt(max(p * (1 - p), 1e-9) * deff / n)
    return p, hw


def guards(rows):
    print("GUARD A -- eco-connectivity column vs the ENGINE's titaniumCollected")
    print("  (wired100>0 should coincide with coll100>0; both cells must exist)")
    tab = defaultdict(int)
    for r in rows:
        tab[(r["harv_wired100"] > 0, r["ti_coll100"] > 0)] += 1
    for k in ((True, True), (True, False), (False, True), (False, False)):
        print(f"    wired={k[0]!s:5s} coll>0={k[1]!s:5s}  n={tab[k]}")
    agree = tab[(True, True)] + tab[(False, False)]
    print(f"  agreement {agree}/{sum(tab.values())} = "
          f"{100.0*agree/sum(tab.values()):.1f}%")
    print("  -- FALSE-POSITIVE branch (wired but nothing collected) and")
    print("     FALSE-NEGATIVE branch (collected but read unwired) both shown.")

    print("\nGUARD B -- every headline column must take BOTH values within ONE map")
    for m in ("royale", "icefloe"):
        sub = [r for r in rows if r["map"] == m]
        for c in ("harv_wired100", "ti_coll100", "arr16_rnd", "throws_ours"):
            vs = {r[c] for r in sub}
            zero = sum(1 for r in sub if r[c] in (0, -1))
            print(f"    {m:10s} {c:16s} distinct={len(vs):3d} "
                  f"zero/absent={zero:2d}/{len(sub)}")

    print("\nGUARD C -- a column that is FLAT across all 15 maps is a broken column")
    for c in ("spawn_fwd4", "harv1_rnd", "rev_rate", "harv_wired100",
              "ti_coll100", "arr16_rnd", "throw_gain", "fwdbuild_n",
              "death_apron", "fc_rnd"):
        per = [mean([r[c] for r in rows if r["map"] == m]) for m in ORDER]
        lo, hi = min(per), max(per)
        flag = "FLAT<-SUSPECT" if hi - lo < 1e-6 else ""
        print(f"    {c:16s} min={lo:9.3f} max={hi:9.3f} {flag}")

    print("\nGUARD D -- seat balance (A/B must not carry the map effect)")
    for m in ("royale", "icefloe", "yulerune", "ragnarok", "auroraveil"):
        for s in ("A", "B"):
            sub = [r for r in rows if r["map"] == m and r["seat"] == s]
            print(f"    {m:10s} seat {s}  win {sum(r['won'] for r in sub)}/{len(sub)}"
                  f"  wired100>0 {sum(1 for r in sub if r['harv_wired100']>0)}/{len(sub)}")


def permap(rows):
    cols = [("win", lambda s: f"{sum(r['won'] for r in s)}/{len(s)}"),
            ("wired100>0", lambda s: f"{sum(1 for r in s if r['harv_wired100']>0)*100//len(s)}%"),
            ("coll100", lambda s: f"{mean([r['ti_coll100'] for r in s]):.0f}"),
            ("oppcoll100", lambda s: f"{mean([r['opp_coll100'] for r in s]):.0f}"),
            ("harv1", lambda s: f"{mean([r['harv1_rnd'] for r in s]):.1f}"),
            ("conv_n30", lambda s: f"{mean([r['conv_n30'] for r in s]):.1f}"),
            ("goodconv30", lambda s: f"{mean([r['conv_good30'] for r in s]):.1f}"),
            ("arr16", lambda s: f"{mean([r['arr16_rnd'] for r in s if r['arr16_rnd']>=0]):.1f}"),
            ("arr16 n/a", lambda s: f"{sum(1 for r in s if r['arr16_rnd']<0)}"),
            ("throws", lambda s: f"{mean([r['throws_ours'] for r in s]):.0f}"),
            ("thr_back", lambda s: f"{mean([r['throw_back'] for r in s]):.1f}"),
            ("fwdbld", lambda s: f"{mean([r['fwdbuild_n'] for r in s]):.0f}"),
            ("rev", lambda s: f"{mean([r['rev_rate'] for r in s]):.3f}"),
            ("fc", lambda s: f"{mean([r['fc_rnd'] for r in s]):.1f}"),
            ("fc@theirs", lambda s: f"{sum(1 for r in s if r['fc_basin']=='theirs')*100//len(s)}%"),
            ("deaths", lambda s: f"{mean([r['ourbot_deaths'] for r in s]):.1f}"),
            ("d_mid", lambda s: f"{mean([r['death_mid'] for r in s]):.1f}"),
            ("d_apron", lambda s: f"{mean([r['death_apron'] for r in s]):.1f}"),
            ("oppcore_hit", lambda s: f"{sum(1 for r in s if r['oppcore_firsthit']>=0)*100//len(s)}%"),
            ("ourcore_min", lambda s: f"{mean([r['ourcore_min'] for r in s]):.0f}"),
            ]
    print("| map | " + " | ".join(c[0] for c in cols) + " |")
    print("|" + "---|" * (len(cols) + 1))
    for m in ORDER:
        s = [r for r in rows if r["map"] == m]
        print(f"| {m} | " + " | ".join(c[1](s) for c in cols) + " |")


def contrast(rows):
    sw = [r for r in rows if r["map"] in SWEEP]
    cr = [r for r in rows if r["map"] in CRATER]
    print(f"sweep n={len(sw)} (ragnarok+royale)   crater n={len(cr)} "
          f"(icefloe+auroraveil+yulerune)")
    keys = [k for k in rows[0]
            if isinstance(rows[0][k], (int, float)) and k not in ("seed",)]
    out = []
    for k in keys:
        a, b = mean([r[k] for r in sw]), mean([r[k] for r in cr])
        if math.isnan(a) or math.isnan(b):
            continue
        denom = max(abs(a), abs(b), 1e-9)
        out.append((abs(a - b) / denom, k, a, b))
    out.sort(reverse=True)
    print(f"{'column':24s} {'sweep':>10s} {'crater':>10s} {'rel gap':>8s}")
    for g, k, a, b in out[:40]:
        print(f"{k:24s} {a:10.3f} {b:10.3f} {g:8.2f}")


def pair(rows):
    for m in ("royale", "yulerune"):
        s = [r for r in rows if r["map"] == m]
        w = [r for r in s if r["won"]]
        l = [r for r in s if not r["won"]]
        print(f"\n### {m}  ({len(w)}W/{len(l)}L)")
        for k in ("harv1_rnd", "harv_n30", "conv_n30", "conv_good30",
                  "harv_wired30", "harv_wired100", "ti_coll30", "ti_coll100",
                  "opp_coll100", "arr16_rnd", "arr16_hops", "throws_ours",
                  "throws_ours30", "throw_back", "turret_dmin", "fwdbuild_n",
                  "fwdbuild1_rnd", "fc_rnd", "ourbot_deaths", "death_apron",
                  "death_mid", "our_recv_sent", "our_recv_gun",
                  "oppcore_firsthit", "ourcore_firsthit", "oppcore_min",
                  "ourcore_min", "rounds"):
            print(f"  {k:18s} all={mean([r[k] for r in s]):9.2f}"
                  f"  W={mean([r[k] for r in w]):9.2f}"
                  f"  L={mean([r[k] for r in l]):9.2f}")


def chain(rows):
    cr = [r for r in rows if r["map"] in CRATER]
    losses = [r for r in cr if not r["won"]]
    wins = [r for r in cr if r["won"]]
    sw = [r for r in rows if r["map"] in SWEEP]
    swW = [r for r in sw if r["won"]]
    print(f"crater losses n={len(losses)}  crater wins n={len(wins)}  "
          f"sweep wins n={len(swW)}")
    print("\nRANKED BY MEASURED COST -- each row: share of crater LOSSES showing")
    print("the condition, vs share of SWEEP WINS (the matched control).")
    conds = [
        ("eco never wired (harv_wired100 == 0)",
         lambda r: r["harv_wired100"] == 0),
        ("zero titanium delivered by r100", lambda r: r["ti_coll100"] == 0),
        ("zero titanium delivered ALL GAME", lambda r: r["ti_coll_end"] == 0),
        ("opp out-collects us 2:1 at r100",
         lambda r: r["opp_coll100"] > 2 * r["ti_coll100"]),
        ("no bot ever reaches their near band",
         lambda r: r["arr16_rnd"] < 0),
        ("arrival later than r20", lambda r: r["arr16_rnd"] > 20),
        ("their core never damaged", lambda r: r["oppcore_firsthit"] < 0),
        ("our core hit before theirs",
         lambda r: r["ourcore_firsthit"] >= 0 and
         (r["oppcore_firsthit"] < 0 or
          r["ourcore_firsthit"] < r["oppcore_firsthit"])),
        ("majority of our bot deaths in MID (route)",
         lambda r: r["ourbot_deaths"] > 0 and
         r["death_mid"] * 2 > r["ourbot_deaths"]),
        ("deaths concentrated on 1 tile (>=40%)",
         lambda r: r["ourbot_deaths"] >= 3 and r["death_conc"] >= 0.4),
        ("a bot was thrown BACKWARD (kidnap)", lambda r: r["throw_back"] > 0),
        ("stalled bot (never left our apron, 40+ rounds alive)",
         lambda r: r["stall_bots"] > 0),
    ]
    print(f"{'condition':52s} {'craterL':>9s} {'craterW':>9s} {'sweepW':>9s}")
    scored = []
    for name, f in conds:
        a = sum(1 for r in losses if f(r)) / len(losses)
        b = sum(1 for r in wins if f(r)) / max(1, len(wins))
        c = sum(1 for r in swW if f(r)) / len(swW)
        scored.append((a - c, name, a, b, c))
    scored.sort(reverse=True)
    for _s, name, a, b, c in scored:
        print(f"{name:52s} {a*100:8.1f}% {b*100:8.1f}% {c*100:8.1f}%")

    print("\nWITHIN-CRATER: does the eco failure track the loss?")
    for m in CRATER:
        s = [r for r in rows if r["map"] == m]
        for lab, f in (("wired100>0", lambda r: r["harv_wired100"] > 0),
                       ("wired100==0", lambda r: r["harv_wired100"] == 0)):
            g = [r for r in s if f(r)]
            if g:
                p, hw = share_ci(sum(r["won"] for r in g), len(g))
                print(f"  {m:11s} {lab:12s} n={len(g):3d} win={p*100:5.1f}% "
                      f"+/-{hw*100:.1f}")


def ferry(rows):
    print("FERRY / arrival cut -- all 15 maps")
    print(f"{'map':13s} {'win':>7s} {'arr16':>7s} {'noarr':>6s} {'hops':>6s} "
          f"{'throws':>7s} {'back':>6s} {'turr_dmin':>9s} {'fwdbld':>7s}")
    for m in ORDER:
        s = [r for r in rows if r["map"] == m]
        arr = [r["arr16_rnd"] for r in s if r["arr16_rnd"] >= 0]
        print(f"{m:13s} {sum(r['won'] for r in s):3d}/{len(s):3d} "
              f"{mean(arr):7.1f} {sum(1 for r in s if r['arr16_rnd']<0):6d} "
              f"{mean([r['arr16_hops'] for r in s if r['arr16_hops']>=0]):6.2f} "
              f"{mean([r['throws_ours'] for r in s]):7.1f} "
              f"{mean([r['throw_back'] for r in s]):6.2f} "
              f"{mean([r['turret_dmin'] for r in s]):9.2f} "
              f"{mean([r['fwdbuild_n'] for r in s]):7.1f}")

    print("\nPOOLED within-map: arrival by r15 vs later/never")
    for lab, f in (("arr16 <= 15", lambda r: 0 <= r["arr16_rnd"] <= 15),
                   ("arr16 16-40", lambda r: 16 <= r["arr16_rnd"] <= 40),
                   ("arr16 > 40", lambda r: r["arr16_rnd"] > 40),
                   ("never", lambda r: r["arr16_rnd"] < 0)):
        g = [r for r in rows if f(r)]
        if g:
            p, hw = share_ci(sum(r["won"] for r in g), len(g))
            print(f"  {lab:12s} n={len(g):4d}  win={p*100:5.1f}% +/-{hw*100:.1f}")

    print("\nPOOLED: eco wired at r100 vs not (ALL maps, and within crater trio)")
    for pop, name in ((rows, "all 15 maps"),
                      ([r for r in rows if r["map"] in CRATER], "crater trio"),
                      ([r for r in rows if r["map"] in SWEEP], "sweep pair")):
        for lab, f in (("wired>0", lambda r: r["harv_wired100"] > 0),
                       ("wired==0", lambda r: r["harv_wired100"] == 0)):
            g = [r for r in pop if f(r)]
            if g:
                p, hw = share_ci(sum(r["won"] for r in g), len(g))
                print(f"  {name:12s} {lab:9s} n={len(g):4d} "
                      f"win={p*100:5.1f}% +/-{hw*100:.1f}")


CUTS = {"guards": guards, "permap": permap, "contrast": contrast,
        "pair": pair, "chain": chain, "ferry": ferry}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        raise SystemExit(0)
    R = load()
    for c in sys.argv[1:]:
        print(f"\n{'='*70}\n== {c}\n{'='*70}")
        CUTS[c](R)
