#!/usr/bin/env python3
"""Analysis over collar_decode.py output.

  python analyse.py <outdir> <join.tsv>

Section A -- VALIDATION: reproduce the published cells of
`docs/research/heal-seat-census-2026-08-09.md` (US side, CAD loss games,
siege window) with the two-sided decoder.
Section B -- per-opponent collar staffing + core-heal rate, US vs THEM.
Section C -- round-band split (r0-150 / r151-300 / r301+).
"""
from __future__ import annotations

import collections
import csv
import statistics
import sys


def load(outdir, joinp):
    J = {r["file"]: r for r in csv.DictReader(open(joinp), delimiter="\t")}
    rounds = collections.defaultdict(list)     # (file, side) -> list of dict
    with open(f"{outdir}/collar_rounds.tsv") as fh:
        rd = csv.DictReader(fh, delimiter="\t")
        for r in rd:
            for k in r:
                if k not in ("file", "side"):
                    r[k] = int(r[k])
            rounds[(r["file"], r["side"])].append(r)
    games = {}
    with open(f"{outdir}/collar_games.tsv") as fh:
        for g in csv.DictReader(fh, delimiter="\t"):
            games[(g["file"], g["side"])] = g
    return J, rounds, games


def pct(a, b):
    return 100.0 * a / b if b else float("nan")


def main(argv):
    outdir, joinp = argv[0], argv[1]
    J, rounds, games = load(outdir, joinp)
    files = sorted({f for f, _s in rounds})
    print(f"files {len(files)}  round-rows {sum(len(v) for v in rounds.values())}")

    # ---------------- A. VALIDATION -------------------------------------
    print("\n=== A. VALIDATION vs heal-seat-census-2026-08-09.md ===")
    cad = [f for f in files if J[f]["opp"] == "CtrlAltDefeat"]
    # "loss games" in the published doc = games where OUR CORE WAS DESTROYED
    # (85 CAD = 54 core-death losses + 18 tiebreak losses + 10 wins + 3 no-window).
    # Using won==0 instead gives 58 and does not reproduce; core_death does.
    cad_loss = [f for f in cad if int(games[(f, "US")]["core_death_own"]) >= 0]
    print(f"CAD files {len(cad)} (published 85); loss games {len(cad_loss)} "
          f"(published 54)")

    def siege_rows(fs):
        out = []
        for f in fs:
            rs = rounds[(f, "US")]
            ws = next((r["rnd"] for r in rs if r["shots_on_core"] > 0), None)
            if ws is None:
                continue
            out.append([r for r in rs if r["rnd"] >= ws])
        return out

    sg = siege_rows(cad_loss)
    flat = [r for g in sg for r in g]
    print(f"siege-rounds {len(flat)} (published 19,393); "
          f"games with a window {len(sg)}")
    hl = [r["healers"] for r in flat]
    dist = collections.Counter(min(h, 9) for h in hl)
    print(f"healers/round mean {statistics.mean(hl):.2f} (pub 1.10)  "
          f"median {statistics.median(hl):.0f} (pub 0)  "
          f"share0 {pct(dist[0], len(hl)):.1f}% (pub 56.7%)  max {max(hl)}")
    nd = [r["healers"] for r in flat if r["coredmg"] == 0]
    dd = [r["healers"] for r in flat if r["coredmg"] > 0]
    print(f"  no-damage rounds n={len(nd)} mean {statistics.mean(nd):.2f} "
          f"(pub 0.45, n 12,388)")
    print(f"  damage rounds    n={len(dd)} mean {statistics.mean(dd):.2f} "
          f"(pub 2.24, n 7,005)")
    inc = [r["coredmg"] for r in flat]
    print(f"  incoming HP/rd {statistics.mean(inc):.2f} (pub 5.67); "
          f"on damage rounds "
          f"{statistics.mean([r['coredmg'] for r in flat if r['coredmg']>0]):.2f}"
          f" (pub 15.70)")
    # terminal 25
    term = [r for g in sg for r in g[-25:]]
    print(f"  terminal-25 n={len(term)} (pub 1,350) healers "
          f"{statistics.mean([r['healers'] for r in term]):.2f} (pub 1.99) "
          f"staffed {statistics.mean([r['orth_bots0']+r['fp0'] for r in term]):.2f}"
          f" (pub 2.22) incoming "
          f"{statistics.mean([r['coredmg'] for r in term]):.2f} (pub 18.79)")
    # seat-turn ledger
    st = sum(r["orth_bots0"] + r["fp0"] for r in flat)
    hh = sum(r["healers"] for r in flat)
    mv = sum(r["seat_moved"] for r in flat)
    ot = sum(r["seat_other"] for r in flat)
    idl = st - hh - mv - ot
    print(f"  seat-turn ledger n={st} (pub 30,109): healed "
          f"{pct(hh,st):.1f}% (pub 70.5) walked {pct(mv,st):.1f}% (pub 17.2) "
          f"other {pct(ot,st):.1f}% (pub 2.6) idle {pct(idl,st):.1f}% (pub 9.7)")
    # heal HP vs 4x events, both signs present
    tot_ev = sum(int(games[(f, 'US')]["tot_heal_core"]) for f in cad)
    tot_hp = sum(int(games[(f, 'US')]["tot_coreheal_hp"]) for f in cad)
    tot_dmg = sum(int(games[(f, 'US')]["tot_coredmg"]) for f in cad)
    print(f"  HP-stream cross-check (CAD, US): heal events {tot_ev}, "
          f"heal HP {tot_hp}, ratio {tot_hp/(4*tot_ev):.4f} (pub 0.9750); "
          f"damage HP {tot_dmg} -- BOTH SIGNS present")
    mo = max(int(games[(f, 'US')]["max_orth"]) for f in cad)
    mf = max(int(games[(f, 'US')]["max_fp"]) for f in cad)
    nfp = sum(1 for f in cad if int(games[(f, 'US')]["max_fp"]) > 0)
    print(f"  max distinct ORTH8 seats occupied (CAD, US) {mo} (pub max 7 bots);"
          f" max on-footprint {mf} in {nfp} of {len(cad)} games (pub 1 in 4/85)")
    geo = collections.Counter((int(g['orth_n']), int(g['cheb_n']))
                              for g in games.values())
    print(f"  ring geometry (orth_n, cheb_n) after wall exclusion: "
          f"{dict(geo.most_common(5))}")

    # ---------------- B/C. per-opponent -----------------------------------
    BANDS = (("r0-150", 0, 150), ("r151-300", 151, 300), ("r301+", 301, 10**9))

    def agg(fs, side):
        n_games = 0
        n_rounds = 0
        occ_rounds = 0
        seats = 0
        cheb = 0
        heal_ev = 0
        heal_any = 0
        games_any_heal = 0
        band = {b[0]: [0, 0, 0, 0] for b in BANDS}  # rounds, occ, seats, heals
        for f in fs:
            rs = rounds.get((f, side))
            if not rs:
                continue
            n_games += 1
            g_heal = 0
            for r in rs:
                n_rounds += 1
                if r["orth_seats0"] > 0:
                    occ_rounds += 1
                seats += r["orth_seats0"]
                cheb += r["cheb_seats0"]
                heal_ev += r["heal_core_ev"]
                heal_any += r["heal_any_ev"]
                g_heal += r["heal_core_ev"]
                for name, lo, hi in BANDS:
                    if lo <= r["rnd"] <= hi:
                        b = band[name]
                        b[0] += 1
                        b[1] += 1 if r["orth_seats0"] > 0 else 0
                        b[2] += r["orth_seats0"]
                        b[3] += r["heal_core_ev"]
                        break
            if g_heal:
                games_any_heal += 1
        return dict(n_games=n_games, n_rounds=n_rounds, occ_rounds=occ_rounds,
                    seats=seats, cheb=cheb, heal_ev=heal_ev, heal_any=heal_any,
                    games_any_heal=games_any_heal, band=band)

    by_opp = collections.defaultdict(list)
    for f in files:
        by_opp[J[f]["opp"]].append(f)
    order = sorted(by_opp, key=lambda k: -len(by_opp[k]))

    print("\n=== B. COLLAR STAFFING + CORE HEALS (ORTH8 = the 8 heal-capable "
          "seats), start-of-round ===")
    hdr = (f"{'opponent':<26} {'side':<5} {'games':>5} {'rounds':>8} "
           f"{'%rnd>=1':>8} {'seats/rd':>9} {'cheb/rd':>8} "
           f"{'heals/game':>10} {'heals/100rd':>11} {'%games':>7} "
           f"{'heal_any/100rd':>14}")
    print(hdr)
    rowsout = []
    for opp in order:
        fs = by_opp[opp]
        if len(fs) < 5:
            continue
        for side in ("THEM", "US"):
            a = agg(fs, side)
            if not a["n_games"]:
                continue
            print(f"{opp[:26]:<26} {side:<5} {a['n_games']:>5} "
                  f"{a['n_rounds']:>8} {pct(a['occ_rounds'],a['n_rounds']):>7.1f}% "
                  f"{a['seats']/a['n_rounds']:>9.3f} "
                  f"{a['cheb']/a['n_rounds']:>8.3f} "
                  f"{a['heal_ev']/a['n_games']:>10.1f} "
                  f"{100*a['heal_ev']/a['n_rounds']:>11.2f} "
                  f"{pct(a['games_any_heal'],a['n_games']):>6.0f}% "
                  f"{100*a['heal_any']/a['n_rounds']:>14.2f}")
            rowsout.append((opp, side, a))

    print("\n--- US aggregate over all attributed games ---")
    for side in ("US", "THEM"):
        a = agg(files, side)
        print(f"ALL {side:<5} games {a['n_games']} rounds {a['n_rounds']} "
              f"%rnd>=1 {pct(a['occ_rounds'],a['n_rounds']):.1f}% "
              f"seats/rd {a['seats']/a['n_rounds']:.3f} "
              f"cheb/rd {a['cheb']/a['n_rounds']:.3f} "
              f"heals/game {a['heal_ev']/a['n_games']:.1f} "
              f"heals/100rd {100*a['heal_ev']/a['n_rounds']:.2f} "
              f"%games {pct(a['games_any_heal'],a['n_games']):.0f}%")

    print("\n=== C. BAND SPLIT (r0-150 / r151-300 / r301+) ===")
    print(f"{'opponent':<26} {'side':<5} {'band':<9} {'rounds':>8} "
          f"{'%rnd>=1':>8} {'seats/rd':>9} {'heals/100rd':>11}")
    for opp, side, a in rowsout:
        for name, _lo, _hi in BANDS:
            n, o, s, hv = a["band"][name]
            if not n:
                continue
            print(f"{opp[:26]:<26} {side:<5} {name:<9} {n:>8} "
                  f"{pct(o,n):>7.1f}% {s/n:>9.3f} {100*hv/n:>11.2f}")


if __name__ == "__main__":
    main(sys.argv[1:])
