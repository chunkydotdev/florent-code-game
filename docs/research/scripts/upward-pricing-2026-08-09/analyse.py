#!/usr/bin/env python3
"""UPWARD PRICING -- the three questions, on the top of the ladder.

Inputs (all read from the FREEZE dir, never from corpus/, which a keeper daemon
appends to every ~10 minutes):
  meta_join.tsv            attribution: seat -> team, version, ratingXBefore
  killmix.tsv              this cut's decoder: per-victim-side weapon mix on core
  collar/collar_games.tsv  shipped collar decoder, per side-game totals
  collar/collar_rounds.tsv shipped collar decoder, per side-round

BANDING IS ON ratingABefore / ratingBBefore ONLY.  teamARating/teamBRating are
live joins and are never touched.

    python analyse.py <freezedir> [q1|q2|q3]
"""
from __future__ import annotations
import csv, statistics, sys
from collections import defaultdict

SEAT = {"US": "A", "THEM": "B"}          # replay index 0 == meta teamA


def f(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def load(fz):
    M = {r["file"]: r for r in csv.DictReader(open(f"{fz}/meta_join.tsv"), delimiter="\t")}
    K = list(csv.DictReader(open(f"{fz}/killmix.tsv"), delimiter="\t"))
    return M, K


def pct(a, b):
    return f"{100*a/b:5.1f}%" if b else "  n/a"


def q1(fz, M, K):
    """HOW DO TOP-TIER CORES DIE, and does anyone kill a 1700+ core inside r250?"""
    print("\n" + "=" * 78)
    print("Q1 -- kill round and weapon mix, banded on the VICTIM's ratingBefore")
    print("=" * 78)
    pop = defaultdict(list)
    for r in K:
        m = M.get(r["file"])
        if not m:
            continue
        side = "US" if r["victim_idx"] == "0" else "THEM"
        vr = f(m[f"rating{SEAT[side]}Before"])
        kr = f(m[f"rating{SEAT['THEM' if side=='US' else 'US']}Before"])
        if vr is None or kr is None:
            continue
        clean_tp = m["us_side"] == "none" and m["related"] == "none"
        r["_vr"], r["_kr"] = vr, kr
        r["_vname"] = m[f"team{SEAT[side]}Name"]
        r["_kname"] = m[f"team{SEAT['THEM' if side=='US' else 'US']}Name"]
        if clean_tp:
            pop["tp"].append(r)
        elif m["related"] == "none":
            pop["ours"].append(r)

    def band(rows, lo, hi=None, killer_lo=None):
        out = []
        for r in rows:
            if r["_vr"] < lo or (hi is not None and r["_vr"] >= hi):
                continue
            if killer_lo is not None and r["_kr"] < killer_lo:
                continue
            out.append(r)
        return out

    def report(label, rows):
        dead = [r for r in rows if int(r["death_rnd"]) >= 0]
        if not dead:
            print(f"{label:44s} side-games {len(rows):5d}   NO KILLS")
            return
        d = sorted(int(r["death_rnd"]) for r in dead)
        n = len(d)
        q = lambda p: d[min(n - 1, int(p * n))]
        ins = sum(1 for x in d if x <= 250)
        print(f"{label:44s} side-games {len(rows):5d}  killed {n:5d} "
              f"({100*n/len(rows):4.1f}%)  median r{statistics.median(d):4.0f} "
              f"q1 r{q(.25):4.0f} q3 r{q(.75):4.0f} | <=r250 {pct(ins,n)} "
              f"<=r150 {pct(sum(1 for x in d if x<=150),n)} "
              f"<=r100 {pct(sum(1 for x in d if x<=100),n)}")

    print("\n-- CLEAN THIRD-PARTY (us absent), by VICTIM band --")
    for lo, hi, nm in ((0, 1400, "<1400"), (1400, 1550, "1400-1549"),
                       (1550, 1700, "1550-1699"), (1700, 1800, "1700-1799"),
                       (1800, 1900, "1800-1899"), (1900, 9999, ">=1900"),
                       (1700, 9999, ">=1700 (ALL)"), (1800, 9999, ">=1800 (ALL)")):
        report(f"victim {nm}", band(pop["tp"], lo, hi))
    print("\n-- top-vs-top: victim >=1700 AND killer >=1700 --")
    report("victim >=1700, killer >=1700", band(pop["tp"], 1700, None, 1700))
    report("victim >=1800, killer >=1800", band(pop["tp"], 1800, None, 1800))
    print("\n-- reference arms (our own games) --")
    ours_victim_us = [r for r in pop["ours"] if r["_vname"] == "OpenSverige"]
    ours_victim_them = [r for r in pop["ours"] if r["_vname"] != "OpenSverige"]
    report("OUR core is the victim", ours_victim_us)
    report("WE are the killer (field core victim)", ours_victim_them)

    print("\n-- WEAPON MIX on the core (damage points, victim band) --")
    print(f"{'population':44s} {'N kills':>8s} {'gunner':>8s} {'sentinel':>9s} "
          f"{'batk':>8s} | {'dmg/kill':>9s} {'pred/obs':>9s}")
    def mix(label, rows):
        dead = [r for r in rows if int(r["death_rnd"]) >= 0]
        if not dead:
            return
        g = sum(int(r["sh_gunner"]) for r in dead) * 7
        s = sum(int(r["sh_sentinel"]) for r in dead) * 18
        b = sum(int(r["batk"]) for r in dead) * 2
        tt = g + s + b
        obs = sum(int(r["coredmg"]) for r in dead)
        print(f"{label:44s} {len(dead):8d} {pct(g,tt):>8s} {pct(s,tt):>9s} "
              f"{pct(b,tt):>8s} | {tt/len(dead):9.0f} {tt/obs if obs else 0:9.4f}")
    for lo, hi, nm in ((0, 1550, "<1550"), (1550, 1700, "1550-1699"),
                       (1700, 1800, "1700-1799"), (1800, 9999, ">=1800"),
                       (1700, 9999, ">=1700 (ALL)")):
        mix(f"third-party, victim {nm}", band(pop["tp"], lo, hi))
    mix("third-party, victim>=1700 killer>=1700", band(pop["tp"], 1700, None, 1700))
    mix("OUR core is the victim", ours_victim_us)
    mix("WE are the killer", ours_victim_them)

    print("\n-- FAST kills only (<=r250), weapon mix --")
    def fastmix(label, rows):
        dead = [r for r in rows if 0 <= int(r["death_rnd"]) <= 250]
        mix(label + f"  (n={len(dead)})", dead)
    fastmix("third-party victim >=1700", band(pop["tp"], 1700))
    fastmix("third-party victim >=1800", band(pop["tp"], 1800))
    fastmix("WE are the killer", ours_victim_them)
    return pop


def collar(fz, M):
    """Per-team collar occupancy + core-heal, from the SHIPPED collar decoder."""
    agg = defaultdict(lambda: defaultdict(float))
    for r in csv.DictReader(open(f"{fz}/collar/collar_rounds.tsv"), delimiter="\t"):
        m = M.get(r["file"])
        if not m:
            continue
        side = r["side"]
        nm = m[f"team{SEAT[side]}Name"]
        clean_tp = m["us_side"] == "none" and m["related"] == "none"
        keys = [(nm, "tp" if clean_tp else "vsus")]
        for k in keys:
            a = agg[k]
            a["rounds"] += 1
            if int(r["orth_seats0"]) >= 1:
                a["occ"] += 1
            a["seats"] += int(r["orth_seats0"])
            a["heal_core"] += int(r["heal_core_ev"])
            a["heal_any"] += int(r["heal_any_ev"])
            a["coredmg"] += int(r["coredmg"])
            a["coreheal"] += int(r["coreheal"])
    return agg


def q2(fz, M, agg):
    print("\n" + "=" * 78)
    print("Q2 -- collar defence at the top, vs the hard-five comparators")
    print("=" * 78)
    rat = defaultdict(list)
    games = defaultdict(int)
    for m in M.values():
        for s in "AB":
            v = f(m[f"rating{s}Before"])
            if v is not None:
                rat[m[f"team{s}Name"]].append(v)
        for s in "AB":
            games[m[f"team{s}Name"]] += 1
    rows = []
    for (nm, popn), a in agg.items():
        if a["rounds"] < 20000:
            continue
        med = statistics.median(rat[nm]) if rat[nm] else 0
        rows.append((med, nm, popn, a))
    rows.sort(reverse=True)
    print(f"\n{'team':30s} {'pop':5s} {'medRat':>7s} {'rounds':>9s} {'collar%':>8s} "
          f"{'seats':>6s} {'coreheal/100r':>13s} {'own-core share':>14s} {'%dmg healed':>11s}")
    for med, nm, popn, a in rows:
        share = a["heal_core"] / a["heal_any"] if a["heal_any"] else 0
        healed = a["coreheal"] / a["coredmg"] if a["coredmg"] else 0
        print(f"{nm[:30]:30s} {popn:5s} {med:7.0f} {a['rounds']:9.0f} "
              f"{100*a['occ']/a['rounds']:7.2f}% {a['seats']/a['rounds']:6.3f} "
              f"{100*a['heal_core']/a['rounds']:13.2f} {100*share:13.1f}% "
              f"{100*healed:10.1f}%")

    # rating-banded pooled
    print("\n-- pooled by median rating band (clean third-party only) --")
    pool = defaultdict(lambda: defaultdict(float))
    for (nm, popn), a in agg.items():
        if popn != "tp":
            continue
        med = statistics.median(rat[nm]) if rat[nm] else 0
        b = ("<1550" if med < 1550 else "1550-1699" if med < 1700 else
             "1700-1799" if med < 1800 else "1800-1899" if med < 1900 else ">=1900")
        for k, v in a.items():
            pool[b][k] += v
        pool[b]["teams"] += 0
    for b in ("<1550", "1550-1699", "1700-1799", "1800-1899", ">=1900"):
        a = pool[b]
        if not a["rounds"]:
            continue
        share = a["heal_core"] / a["heal_any"] if a["heal_any"] else 0
        healed = a["coreheal"] / a["coredmg"] if a["coredmg"] else 0
        print(f"{b:30s} {'tp':5s} {'':7s} {a['rounds']:9.0f} "
              f"{100*a['occ']/a['rounds']:7.2f}% {a['seats']/a['rounds']:6.3f} "
              f"{100*a['heal_core']/a['rounds']:13.2f} {100*share:13.1f}% "
              f"{100*healed:10.1f}%")


def q3(fz, M, K, agg):
    print("\n" + "=" * 78)
    print("Q3 -- softest legitimate target: per-team VICTIM profile, third-party")
    print("=" * 78)
    rat = defaultdict(list)
    for m in M.values():
        for s in "AB":
            v = f(m[f"rating{s}Before"])
            if v is not None:
                rat[m[f"team{s}Name"]].append(v)
    per = defaultdict(lambda: defaultdict(float))
    for r in K:
        m = M.get(r["file"])
        if not m or m["us_side"] != "none" or m["related"] != "none":
            continue
        side = "US" if r["victim_idx"] == "0" else "THEM"
        nm = m[f"team{SEAT[side]}Name"]
        p = per[nm]
        p["sg"] += 1
        d = int(r["death_rnd"])
        if d >= 0:
            p["killed"] += 1
            if d <= 250:
                p["k250"] += 1
            if d <= 150:
                p["k150"] += 1
            p["sumd"] += d
            p.setdefault("_ds", [])
            p["_ds"] = p["_ds"] if isinstance(p.get("_ds"), list) else []
        p["batk"] += int(r["batk"]) * 2
        p["gun"] += int(r["sh_gunner"]) * 7
        p["sen"] += int(r["sh_sentinel"]) * 18
    print(f"\n{'team':30s} {'medRat':>7s} {'sideG':>6s} {'killed%':>8s} {'<=r250':>8s} "
          f"{'<=r150':>8s} {'medKill':>8s} {'batk%dmg':>9s} {'collar%':>8s} {'chl/100r':>9s}")
    med_of = {nm: (statistics.median(v) if v else 0) for nm, v in rat.items()}
    ds = defaultdict(list)
    for r in K:
        m = M.get(r["file"])
        if not m or m["us_side"] != "none" or m["related"] != "none":
            continue
        side = "US" if r["victim_idx"] == "0" else "THEM"
        d = int(r["death_rnd"])
        if d >= 0:
            ds[m[f"team{SEAT[side]}Name"]].append(d)
    out = []
    for nm, p in per.items():
        if p["sg"] < 60 or med_of.get(nm, 0) < 1550:
            continue
        a = agg.get((nm, "tp"))
        tt = p["batk"] + p["gun"] + p["sen"]
        out.append((med_of[nm], nm, p, a, tt))
    out.sort(reverse=True)
    for med, nm, p, a, tt in out:
        col = f"{100*a['occ']/a['rounds']:7.2f}%" if a and a["rounds"] else "     n/a"
        chl = f"{100*a['heal_core']/a['rounds']:9.2f}" if a and a["rounds"] else "      n/a"
        mk = statistics.median(ds[nm]) if ds[nm] else float("nan")
        print(f"{nm[:30]:30s} {med:7.0f} {p['sg']:6.0f} {pct(p['killed'],p['sg']):>8s} "
              f"{pct(p['k250'],p['sg']):>8s} {pct(p['k150'],p['sg']):>8s} "
              f"{mk:8.0f} {pct(p['batk'],tt):>9s} {col:>8s} {chl:>9s}")


def main(argv):
    fz = argv[0]
    which = argv[1] if len(argv) > 1 else "all"
    M, K = load(fz)
    if which in ("all", "q1"):
        q1(fz, M, K)
    if which in ("all", "q2", "q3"):
        agg = collar(fz, M)
        if which in ("all", "q2"):
            q2(fz, M, agg)
        if which in ("all", "q3"):
            q3(fz, M, K, agg)


if __name__ == "__main__":
    main(sys.argv[1:])
