#!/usr/bin/env python3
"""Core-kill INCIDENCE cut -- what distinguishes the games where we land a core
kill from the games where we do not.

METHOD (the two defences that make this different from "winners have more stuff")
--------------------------------------------------------------------------------
1. LANDMARK. Every feature is accumulated strictly inside [0, T). The population
   at landmark T is every joined ladder game still running at round T. At T=50
   the earliest core kill in the whole corpus is round 61, so the landmark
   population is the FULL population and there is zero survival censoring: no
   feature can be a consequence of an outcome that has not happened yet.
2. STRATIFICATION. Opponent identity is the dominant confounder. Every test is a
   van Elteren stratified rank test (the stratified Wilcoxon), run twice:
   strata = opponent-rating band (`oppbef` quartiles), and strata = opponent
   NAME. A feature that only works because weak opponents are easier dies in the
   second form.
3. MULTIPLICITY. K features are pre-listed below and Holm-adjusted together.
   Anything that survives Holm is reported as a finding; anything with raw
   p<0.05 that does not is reported as a LEAD and labelled.
4. CONTROLS. One pure negative control (a seeded shuffle of a real feature --
   must be null) and one positive control (a late, admittedly-consequential
   feature -- must be huge). If either misbehaves the machinery is wrong.

Pure stdlib: the project venv has no numpy.

Usage: analyze.py SNAPDIR/out/dataset.tsv OUTDIR
"""
from __future__ import annotations

import csv
import math
import random
import statistics
import sys
from pathlib import Path

# ---------------------------------------------------------------- pre-registered features
BASE = [
    # ---- economy / production
    ("b_builder_bot", "builder bots built"),
    ("b_harvester", "harvesters built"),
    ("b_conveyor", "conveyors built"),
    ("b_barrier", "barriers built"),
    ("ti_end", "titanium banked at T"),
    ("ti_collected_end", "titanium collected by T"),
    # ---- military production
    ("b_gunner", "gunners built"),
    ("b_sentinel", "sentinels built"),
    ("b_launcher", "launchers built"),
    ("b_turret", "turrets built (all types)"),
    ("ammo_converted", "titanium converted to ammo"),
    ("shot", "turret shots fired"),
    # ---- aggression / contact
    ("batk", "builder attacks"),
    ("batk_core", "builder attacks on enemy CORE"),
    ("heals", "builder heals"),
    ("throws", "launcher throws made"),
    # ---- geometry: where the stuff is
    ("turfwd", "turrets built on the enemy half"),
    ("tur36", "turrets built inside d2<=36 of enemy core"),
    ("turmind", "closest turret to enemy core (d2; lower=deeper)"),
    ("botmind", "closest builder bot to enemy core (d2; lower=deeper)"),
    ("r20", "rounds with a builder bot inside d2<=20 of enemy core"),
    # ---- unit disposition
    ("bots_mean", "mean builder bots alive"),
    ("collar8_mean", "mean builder bots on own core collar (d2<=8)"),
    ("collar2_mean", "mean builder bots orthogonally adjacent to own core"),
    ("fwd_mean", "mean builder bots on the enemy half"),
    # ---- attrition
    ("d_builder_bot", "builder bots lost"),
    ("d_conveyor", "conveyors lost"),
    ("d_harvester", "harvesters lost"),
    ("d_gunner", "gunners lost"),
    ("tled", "unit-turns lost to CPU timeout"),
]
STRUCT = [("maparea", "map area (w*h)"), ("oppbef", "opponent rating at match time")]


# ---------------------------------------------------------------- stats (stdlib only)
def ranks(vals):
    """mid-ranks, 1-based."""
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    r = [0.0] * len(vals)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and vals[order[j + 1]] == vals[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r


def normcdf(z):
    return 0.5 * math.erfc(-z / math.sqrt(2))


def van_elteren(strata):
    """strata: list of (values, labels 0/1). Returns (z, p, weighted_auc, n1, n0)."""
    T = ET = VT = 0.0
    auc_num = auc_den = 0.0
    n1t = n0t = 0
    for vals, lab in strata:
        n = len(vals)
        n1 = sum(lab)
        n0 = n - n1
        if n1 == 0 or n0 == 0 or n < 2:
            continue
        w = 1.0 / (n + 1)
        R = ranks(vals)
        s1 = sum(R[i] for i in range(n) if lab[i])
        T += w * s1
        ET += w * n1 * (n + 1) / 2.0
        rbar = (n + 1) / 2.0
        ss = sum((x - rbar) ** 2 for x in R)
        VT += w * w * n1 * n0 / (n * (n - 1)) * ss
        # Effect size: stratum AUCs averaged with the SAME weights the test uses
        # (w_k * n1k * n0k), so the reported AUC can never disagree in sign with z.
        U = s1 - n1 * (n1 + 1) / 2.0
        wk = w * n1 * n0
        auc_num += wk * (U / (n1 * n0))
        auc_den += wk
        n1t += n1
        n0t += n0
    if VT <= 0 or auc_den == 0:
        return (0.0, 1.0, 0.5, n1t, n0t)
    z = (T - ET) / math.sqrt(VT)
    p = 2 * (1 - normcdf(abs(z)))
    return (z, p, auc_num / auc_den, n1t, n0t)


def holm(pvals):
    idx = sorted(range(len(pvals)), key=lambda i: pvals[i])
    adj = [0.0] * len(pvals)
    running = 0.0
    m = len(pvals)
    for rank, i in enumerate(idx):
        a = min(1.0, (m - rank) * pvals[i])
        running = max(running, a)
        adj[i] = running
    return adj


# ---------------------------------------------------------------- driver
def load(path):
    rows = list(csv.DictReader(open(path), delimiter="\t"))
    for r in rows:
        r["maparea"] = int(r["mw"]) * int(r["mh"])
        r["oppbef_f"] = float(r["oppbef"])
    return rows


def band_of_rating(x, cuts):
    for i, c in enumerate(cuts):
        if x < c:
            return f"b{i}"
    return f"b{len(cuts)}"


def run(rows, T, feats, strat_key, out, title, min_stratum=8):
    """feats: list of (colname, side_or_None, label)."""
    pop = [r for r in rows if int(r["turns"]) > T]
    groups = {}
    for r in pop:
        groups.setdefault(strat_key(r), []).append(r)
    groups = {k: v for k, v in groups.items() if len(v) >= min_stratum}
    used = [r for v in groups.values() for r in v]
    res = []
    for col, label in feats:
        strata = []
        for k, v in groups.items():
            vals = [float(r[col]) for r in v]
            lab = [int(r["y_corekill"]) for r in v]
            strata.append((vals, lab))
        z, p, auc, n1, n0 = van_elteren(strata)
        k1 = [float(r[col]) for r in used if r["y_corekill"] == "1"]
        k0 = [float(r[col]) for r in used if r["y_corekill"] == "0"]
        res.append({
            "col": col, "label": label, "z": z, "p": p, "auc": auc,
            "n1": n1, "n0": n0,
            "med1": statistics.median(k1) if k1 else 0,
            "med0": statistics.median(k0) if k0 else 0,
            "mean1": statistics.mean(k1) if k1 else 0,
            "mean0": statistics.mean(k0) if k0 else 0,
        })
    adj = holm([r["p"] for r in res])
    for r, a in zip(res, adj):
        r["padj"] = a
    res.sort(key=lambda r: abs(r["z"]), reverse=True)
    out.append(f"\n### {title}")
    out.append(f"population n={len(used)} (of {len(pop)} alive at T={T}); "
               f"strata={len(groups)}; kills={sum(1 for r in used if r['y_corekill']=='1')}; "
               f"K={len(feats)} features, Holm-adjusted together")
    out.append("")
    out.append("| feature | med kill | med no-kill | AUC | z | p | Holm p | verdict |")
    out.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |")
    for r in res:
        v = ("**FINDING**" if r["padj"] < 0.05 else
             "lead" if r["p"] < 0.05 else "null")
        out.append(f"| `{r['col']}` {r['label']} | {r['med1']:.2f} | {r['med0']:.2f} | "
                   f"{r['auc']:.3f} | {r['z']:+.2f} | {r['p']:.2e} | {r['padj']:.2e} | {v} |")
    return res


def main(dspath, outdir):
    rows = load(dspath)
    O = Path(outdir)
    O.mkdir(parents=True, exist_ok=True)
    out = []

    # ---- seeded negative control + positive control
    rnd = random.Random(20260809)
    shuf = [r["THEM_b_gunner_w50"] for r in rows]
    rnd.shuffle(shuf)
    for r, v in zip(rows, shuf):
        r["NEGCTRL_shuffled_w50"] = v
        # positive control: an admittedly-consequential LATE feature
        r["POSCTRL_them_lost_conveyors_w150"] = r["THEM_d_conveyor_w150"]

    ob = sorted(r["oppbef_f"] for r in rows)
    cuts = [ob[len(ob) * i // 4] for i in (1, 2, 3)]
    out.append(f"opponent-rating quartile cuts: {[round(c,1) for c in cuts]}")

    def by_rating(r):
        return band_of_rating(r["oppbef_f"], cuts)

    def by_opp(r):
        return r["opp"]

    def by_ourver(r):
        # OUR OWN bot version. 27 versions appear in the corpus and their
        # core-kill share runs 0%-100%, so version is a first-class confounder
        # for every US_* feature: "we healed more in kill games" could just be
        # "the versions that heal more are the versions that kill more".
        return r["ourver"]

    def by_opp_ver(r):
        return (r["opp"], r["ourver"])

    T = 50
    feats = []
    for side in ("US", "THEM"):
        for c, lab in BASE:
            feats.append((f"{side}_{c}_w{T}", f"[{side}] {lab}"))
    for c, lab in STRUCT:
        feats.append((c if c != "oppbef" else "oppbef_f", f"[STRUCT] {lab}"))
    feats.append(("NEGCTRL_shuffled_w50", "[CONTROL-] seeded shuffle, must be null"))
    feats.append(("POSCTRL_them_lost_conveyors_w150", "[CONTROL+] their conveyors lost by r150, must be huge"))

    out.append("\n## PRIMARY -- landmark T=50, strata = opponent-rating quartile")
    res_rating = run(rows, T, feats, by_rating, out,
                     "T=50, strata = oppbef quartile")
    out.append("\n## SECONDARY -- same features, strata = OPPONENT IDENTITY (tighter confound control)")
    res_opp = run(rows, T, feats, by_opp, out, "T=50, strata = opponent name")
    out.append("\n## SECONDARY -- same features, strata = OUR OWN BOT VERSION "
               "(kills the 'that feature is just a version signature' reading)")
    res_ver = run(rows, T, feats, by_ourver, out, "T=50, strata = ourver")
    out.append("\n## TIGHTEST -- strata = (opponent x our version). "
               "Small strata, low power; a survivor here is confound-proof.")
    res_ov = run(rows, T, feats, by_opp_ver, out, "T=50, strata = opp x ourver",
                 min_stratum=8)

    # ---- ROBUSTNESS SUMMARY: survive ALL FOUR stratifications, same sign
    out.append("\n## ROBUSTNESS SUMMARY -- which features survive EVERY stratification")
    out.append("A feature is ROBUST only if Holm-adjusted p < 0.05 under all four "
               "stratifications AND the sign of z is the same in all four.")
    out.append("")
    out.append("| feature | AUC rating | AUC opp | AUC ourver | AUC opp x ver | "
               "Holm p (worst) | robust? |")
    out.append("| --- | ---: | ---: | ---: | ---: | ---: | --- |")
    idx = {name: {r["col"]: r for r in res}
           for name, res in (("rating", res_rating), ("opp", res_opp),
                             ("ver", res_ver), ("ov", res_ov))}
    summary = []
    for col, label in feats:
        rr = [idx[k][col] for k in ("rating", "opp", "ver", "ov")]
        signs = {1 if r["z"] > 0 else -1 for r in rr}
        worst = max(r["padj"] for r in rr)
        ok = worst < 0.05 and len(signs) == 1
        summary.append((worst, col, label, rr, ok))
    summary.sort(key=lambda x: (not x[4], x[0]))
    for worst, col, label, rr, ok in summary:
        out.append(f"| `{col}` {label} | " +
                   " | ".join(f"{r['auc']:.3f}" for r in rr) +
                   f" | {worst:.2e} | {'**ROBUST**' if ok else 'no'} |")
    robust = [s for s in summary if s[4]]
    out.append(f"\n**{len(robust)} of {len(feats)} features are ROBUST.**")

    # ---- deeper landmarks (censored -- label them)
    for T2 in (100, 150):
        f2 = []
        for side in ("US", "THEM"):
            for c, lab in BASE:
                f2.append((f"{side}_{c}_w{T2}", f"[{side}] {lab}"))
        out.append(f"\n## LANDMARK T={T2} (CENSORED: games ending before r{T2} are dropped, "
                   f"which removes fast kills -- read as secondary)")
        run(rows, T2, f2, by_opp, out, f"T={T2}, strata = opponent name")

    # ---- "our opening is a constant" test
    out.append("\n## THE 'OUR OPENING IS A CONSTANT' TEST")
    out.append("Medians of OUR OWN r0-50 build counters, kill games vs non-kill games, "
               "whole population (no stratification -- this is the claim as stated).")
    out.append("")
    out.append("| our feature | med kill | med no-kill | mean kill | mean no-kill | identical medians? |")
    out.append("| --- | ---: | ---: | ---: | ---: | --- |")
    us_cols = [f"US_{c}_w50" for c, _ in BASE]
    same = 0
    for c in us_cols:
        k1 = [float(r[c]) for r in rows if r["y_corekill"] == "1"]
        k0 = [float(r[c]) for r in rows if r["y_corekill"] == "0"]
        m1, m0 = statistics.median(k1), statistics.median(k0)
        ident = "YES" if m1 == m0 else "no"
        same += m1 == m0
        out.append(f"| `{c}` | {m1:.2f} | {m0:.2f} | {statistics.mean(k1):.2f} | "
                   f"{statistics.mean(k0):.2f} | {ident} |")
    out.append(f"\n{same} of {len(us_cols)} of our own r0-50 medians are IDENTICAL "
               f"between kill and non-kill games.")

    # ---- coefficient of variation: whose side carries the variance?
    out.append("\n## WHOSE SIDE CARRIES THE VARIANCE (r0-50, whole population)")
    out.append("")
    out.append("| feature | US mean | US sd | US CV | THEM mean | THEM sd | THEM CV | CV ratio THEM/US |")
    out.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for c, lab in BASE:
        u = [float(r[f"US_{c}_w50"]) for r in rows]
        t = [float(r[f"THEM_{c}_w50"]) for r in rows]
        mu, mt = statistics.mean(u), statistics.mean(t)
        su, st = statistics.pstdev(u), statistics.pstdev(t)
        cu = su / mu if mu else 0
        ctt = st / mt if mt else 0
        out.append(f"| {lab} | {mu:.2f} | {su:.2f} | {cu:.2f} | {mt:.2f} | {st:.2f} | "
                   f"{ctt:.2f} | {(ctt/cu if cu else 0):.2f} |")

    # ---- Ouroboros cell
    out.append("\n## OUROBOROS CELL (named, and UNDERPOWERED -- reported, not concluded from)")
    ou = [r for r in rows if r["opp"] == "Ouroboros"]
    nk = sum(1 for r in ou if r["y_corekill"] == "1")
    out.append(f"n={len(ou)} archived games, {nk} core-kill wins "
               f"({100*nk/len(ou):.1f}%). Any test here has ~{nk} positives.")
    out.append("")
    out.append("| feature | mean kill | mean no-kill | median kill | median no-kill |")
    out.append("| --- | ---: | ---: | ---: | ---: |")
    for side in ("US", "THEM"):
        for c, lab in BASE:
            col = f"{side}_{c}_w50"
            k1 = [float(r[col]) for r in ou if r["y_corekill"] == "1"]
            k0 = [float(r[col]) for r in ou if r["y_corekill"] == "0"]
            if not k1 or not k0:
                continue
            out.append(f"| [{side}] {lab} | {statistics.mean(k1):.2f} | {statistics.mean(k0):.2f} | "
                       f"{statistics.median(k1):.2f} | {statistics.median(k0):.2f} |")

    # ---- per-opponent incidence, for context
    out.append("\n## CORE-KILL INCIDENCE BY OPPONENT (archived, joined games only)")
    out.append("")
    out.append("| opponent | n | core-kill wins | share | mean THEM turrets r0-50 | mean THEM harvesters r0-50 |")
    out.append("| --- | ---: | ---: | ---: | ---: | ---: |")
    byopp = {}
    for r in rows:
        byopp.setdefault(r["opp"], []).append(r)
    for opp, v in sorted(byopp.items(), key=lambda kv: -len(kv[1])):
        if len(v) < 10:
            continue
        k = sum(1 for r in v if r["y_corekill"] == "1")
        out.append(f"| {opp} | {len(v)} | {k} | {100*k/len(v):.1f}% | "
                   f"{statistics.mean(float(r['THEM_b_turret_w50']) for r in v):.2f} | "
                   f"{statistics.mean(float(r['THEM_b_harvester_w50']) for r in v):.2f} |")

    # ---- opponent holdout for the top surviving discriminators
    out.append("\n## OPPONENT HOLDOUT (is the top discriminator opponent-fitted?)")
    top = [r for r in res_opp if r["padj"] < 0.05][:6]
    opps = sorted(byopp, key=lambda o: -len(byopp[o]))
    A = set(opps[0::2])
    B = set(opps[1::2])
    out.append("")
    out.append("| feature | AUC half A | n A | AUC half B | n B |")
    out.append("| --- | ---: | ---: | ---: | ---: |")
    for r in top:
        line = [f"| `{r['col']}`"]
        for half in (A, B):
            sub = [x for x in rows if x["opp"] in half and int(x["turns"]) > 50]
            st = []
            g = {}
            for x in sub:
                g.setdefault(x["opp"], []).append(x)
            for _k, v in g.items():
                if len(v) < 8:
                    continue
                st.append(([float(x[r["col"]]) for x in v],
                           [int(x["y_corekill"]) for x in v]))
            _z, _p, auc, n1, n0 = van_elteren(st)
            line.append(f"| {auc:.3f} | {n1+n0} ")
        out.append("".join(line) + "|")

    (O / "results.md").write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
