#!/usr/bin/env python3
"""Follow-up probes on the six features that survived every stratification in
analyze.py. These are POST-HOC and are labelled as such in the deliverable --
they characterise an already-established discriminator, they do not add tests to
the pre-registered family.

  A. MAP stratification (a 5th confounder analyze.py did not use).
  B. Redundancy: are "their early economy is small" and "we are already shooting"
     the same latent, or two independent signals?
  C. The actionable 2x2: core-kill incidence in each quadrant of the two.
  D. Earliest readable round: does the signal exist at r25, or only by r50?
  E. Runtime readability: what fraction of their r0-50 harvesters/conveyors sit
     close enough to THEIR OWN core that a scout at their ring could count them.
  F. Ouroboros cell (underpowered, reported separately).
  G. Opponent holdout.
  H. Does the trigger also predict SPEED (time to kill), or only incidence?

Usage: probe.py dataset.tsv OUTFILE
"""
from __future__ import annotations

import csv
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from analyze import van_elteren, load, holm  # noqa: E402

ROBUST = [
    ("THEM_ti_collected_end_w50", "[THEM] titanium collected by r50"),
    ("THEM_b_harvester_w50", "[THEM] harvesters built r0-50"),
    ("THEM_b_conveyor_w50", "[THEM] conveyors built r0-50"),
    ("THEM_ti_end_w50", "[THEM] titanium banked at r50"),
    ("US_shot_w50", "[US] turret shots fired r0-50"),
    ("US_ammo_converted_w50", "[US] titanium converted to ammo r0-50"),
]


def strat_auc(rows, col, keyf, min_n=8):
    g = {}
    for r in rows:
        g.setdefault(keyf(r), []).append(r)
    st = [([float(x[col]) for x in v], [int(x["y_corekill"]) for x in v])
          for v in g.values() if len(v) >= min_n]
    return van_elteren(st)


def main(ds, outp):
    rows = [r for r in load(ds) if int(r["turns"]) > 50]
    out = []

    # ---------------- A. map stratification
    out.append("## A. MAP stratification (5th confounder, not in the pre-registered family)")
    maps = {}
    for r in rows:
        maps.setdefault(r["map"], []).append(r)
    out.append(f"\n{len(maps)} distinct maps; "
               + ", ".join(f"{k}={len(v)}" for k, v in
                           sorted(maps.items(), key=lambda kv: -len(kv[1]))[:12]))
    out.append("")
    out.append("| feature | AUC (strata=map) | z | p |")
    out.append("| --- | ---: | ---: | ---: |")
    for c, lab in ROBUST:
        z, p, auc, _n1, _n0 = strat_auc(rows, c, lambda r: r["map"])
        out.append(f"| `{c}` {lab} | {auc:.3f} | {z:+.2f} | {p:.2e} |")

    # ---------------- B. redundancy
    out.append("\n## B. REDUNDANCY -- one latent or two?")
    out.append("\nSpearman-style rank correlation between the two constructs, whole population:")
    out.append("")
    out.append("| a | b | rank corr |")
    out.append("| --- | --- | ---: |")

    def rankcorr(a, b):
        from analyze import ranks
        ra, rb = ranks([float(r[a]) for r in rows]), ranks([float(r[b]) for r in rows])
        n = len(ra)
        ma, mb = sum(ra) / n, sum(rb) / n
        num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
        den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5
        return num / den if den else 0.0

    for a, _ in ROBUST:
        for b, _ in ROBUST:
            if a < b:
                out.append(f"| `{a}` | `{b}` | {rankcorr(a, b):+.3f} |")

    out.append("\nCONDITIONAL: does each survive inside tertiles of the other construct?")
    out.append("(strata = opponent x tertile of the conditioning variable)")
    out.append("")
    out.append("| tested feature | conditioned on | AUC | z | p |")
    out.append("| --- | --- | ---: | ---: | ---: |")

    def tertile(rows_, col):
        v = sorted(float(r[col]) for r in rows_)
        return v[len(v) // 3], v[2 * len(v) // 3]

    pairs = [("US_shot_w50", "THEM_ti_collected_end_w50"),
             ("THEM_ti_collected_end_w50", "US_shot_w50"),
             ("US_ammo_converted_w50", "US_shot_w50"),
             ("US_shot_w50", "US_ammo_converted_w50"),
             ("THEM_b_harvester_w50", "US_shot_w50"),
             ("US_shot_w50", "THEM_b_harvester_w50")]
    for test, cond in pairs:
        t1, t2 = tertile(rows, cond)

        def keyf(r, cond=cond, t1=t1, t2=t2):
            v = float(r[cond])
            return (r["opp"], 0 if v <= t1 else 1 if v <= t2 else 2)
        z, p, auc, _a, _b = strat_auc(rows, test, keyf)
        out.append(f"| `{test}` | `{cond}` tertile x opp | {auc:.3f} | {z:+.2f} | {p:.2e} |")

    # ---------------- C. actionable 2x2
    out.append("\n## C. THE ACTIONABLE 2x2 -- core-kill incidence by quadrant")
    med_s = statistics.median(float(r["US_shot_w50"]) for r in rows)
    med_t = statistics.median(float(r["THEM_ti_collected_end_w50"]) for r in rows)
    out.append(f"\nSplit at the population medians: US shots by r50 = {med_s:.0f}, "
               f"THEIR titanium collected by r50 = {med_t:.0f}.")
    out.append("")
    out.append("| our shots r0-50 | their Ti collected by r50 | n | core-kill wins | incidence |")
    out.append("| --- | --- | ---: | ---: | ---: |")
    for slo in (True, False):
        for tlo in (True, False):
            v = [r for r in rows
                 if (float(r["US_shot_w50"]) <= med_s) == slo
                 and (float(r["THEM_ti_collected_end_w50"]) <= med_t) == tlo]
            if not v:
                continue
            k = sum(1 for r in v if r["y_corekill"] == "1")
            out.append(f"| {'<=' if slo else '>'}{med_s:.0f} | {'<=' if tlo else '>'}{med_t:.0f} | "
                       f"{len(v)} | {k} | **{100*k/len(v):.1f}%** |")
    # quintiles of a simple composite
    out.append("\nAnd as a single ordered signal -- rank(US shots) - rank(their Ti collected):")
    from analyze import ranks
    rs = ranks([float(r["US_shot_w50"]) for r in rows])
    rt = ranks([float(r["THEM_ti_collected_end_w50"]) for r in rows])
    comp = sorted(zip([a - b for a, b in zip(rs, rt)], range(len(rows))))
    out.append("")
    out.append("| composite quintile | n | core-kill wins | incidence | median kill round |")
    out.append("| --- | ---: | ---: | ---: | ---: |")
    n = len(comp)
    for q in range(5):
        idxs = [i for _v, i in comp[n * q // 5: n * (q + 1) // 5]]
        v = [rows[i] for i in idxs]
        k = [r for r in v if r["y_corekill"] == "1"]
        mk = statistics.median([int(r["turns"]) for r in k]) if k else float("nan")
        out.append(f"| Q{q+1} {'(least violent)' if q==0 else '(most violent)' if q==4 else ''} "
                   f"| {len(v)} | {len(k)} | **{100*len(k)/len(v):.1f}%** | {mk:.0f} |")

    # ---------------- D. earliest readable round
    out.append("\n## D. WHEN DOES THE SIGNAL EXIST? (same features at earlier windows)")
    out.append("")
    out.append("| feature | AUC w25 | AUC w50 | AUC w75 | AUC w100 |")
    out.append("| --- | ---: | ---: | ---: | ---: |")
    for c, lab in ROBUST:
        base = c.replace("_w50", "")
        cells = []
        for W in (25, 50, 75, 100):
            pop = [r for r in rows if int(r["turns"]) > W]
            _z, _p, auc, _a, _b = strat_auc(pop, f"{base}_w{W}", lambda r: r["opp"])
            cells.append(f"{auc:.3f}")
        out.append(f"| `{base}` {lab} | " + " | ".join(cells) + " |")
    out.append("\n(w75 and w100 are CENSORED -- games that ended before the window closes "
               "are dropped, which preferentially removes fast kills. Read the trend, not "
               "the level.)")

    # ---------------- E. runtime readability of the enemy-economy signal
    out.append("\n## E. RUNTIME READABILITY of the enemy-economy signal")
    out.append("\nWhere do their r0-50 harvesters and conveyors actually sit, relative to "
               "THEIR OWN core? A scout builder bot has vision r^2=20; our core has r^2=36 "
               "but cannot move. So the question is how deep a scout must go.")
    out.append("")
    ev = Path(sys.argv[3]) if len(sys.argv) > 3 else None
    if ev and ev.exists():
        J = {r["file"]: r for r in csv.DictReader(open(ev.parent / "join.tsv"), delimiter="\t")}
        buckets = {"harvester": [], "conveyor": []}
        for r in csv.DictReader(open(ev), delimiter="\t"):
            if r["ev"] != "BUILD" or int(r["rnd"]) >= 50:
                continue
            j = J.get(r["file"])
            if not j or r["team"] == j["our_team"]:
                continue
            if r["kind"] in buckets:
                buckets[r["kind"]].append(int(r["d2_own"]))
        out.append("| their building (r0-50) | n | median d2 to their core | "
                   "share within d2<=20 | within d2<=36 | within d2<=64 |")
        out.append("| --- | ---: | ---: | ---: | ---: | ---: |")
        for k, v in buckets.items():
            if not v:
                continue
            out.append(f"| {k} | {len(v)} | {statistics.median(v):.0f} | "
                       f"{100*sum(1 for x in v if x<=20)/len(v):.1f}% | "
                       f"{100*sum(1 for x in v if x<=36)/len(v):.1f}% | "
                       f"{100*sum(1 for x in v if x<=64)/len(v):.1f}% |")

    # ---------------- F. Ouroboros
    out.append("\n## F. OUROBOROS CELL -- UNDERPOWERED, reported not concluded from")
    ou = [r for r in rows if r["opp"] == "Ouroboros"]
    k = sum(1 for r in ou if r["y_corekill"] == "1")
    out.append(f"\nn={len(ou)} archived joined games alive at r50, {k} core-kill wins "
               f"({100*k/len(ou):.1f}%).")
    out.append("")
    out.append("| feature | mean in kill games | mean in non-kill | median kill | median non-kill | "
               "unstratified Mann-Whitney p |")
    out.append("| --- | ---: | ---: | ---: | ---: | ---: |")
    for c, lab in ROBUST:
        k1 = [float(r[c]) for r in ou if r["y_corekill"] == "1"]
        k0 = [float(r[c]) for r in ou if r["y_corekill"] == "0"]
        z, p, _auc, _a, _b = van_elteren([([float(r[c]) for r in ou],
                                           [int(r["y_corekill"]) for r in ou])])
        out.append(f"| `{c}` {lab} | {statistics.mean(k1):.1f} | {statistics.mean(k0):.1f} | "
                   f"{statistics.median(k1):.1f} | {statistics.median(k0):.1f} | {p:.3f} |")

    # ---------------- G. opponent holdout
    out.append("\n## G. OPPONENT HOLDOUT -- is the discriminator opponent-fitted?")
    byopp = {}
    for r in rows:
        byopp.setdefault(r["opp"], []).append(r)
    opps = sorted(byopp, key=lambda o: -len(byopp[o]))
    A, B = set(opps[0::2]), set(opps[1::2])
    out.append(f"\nHalf A = {len(A)} opponents, half B = {len(B)}, split by alternating "
               f"corpus size so both halves span the rating range.")
    out.append("")
    out.append("| feature | AUC half A | n A | AUC half B | n B |")
    out.append("| --- | ---: | ---: | ---: | ---: |")
    for c, lab in ROBUST:
        cells = []
        for half in (A, B):
            sub = [r for r in rows if r["opp"] in half]
            _z, _p, auc, n1, n0 = strat_auc(sub, c, lambda r: r["opp"])
            cells.append(f"{auc:.3f} | {n1+n0}")
        out.append(f"| `{c}` {lab} | " + " | ".join(cells) + " |")

    # ---------------- H. incidence vs speed
    out.append("\n## H. DOES THE SIGNAL PREDICT SPEED TOO, OR ONLY INCIDENCE?")
    out.append("\nAmong core-kill wins ONLY, is the kill faster when the signal is stronger?")
    out.append("")
    out.append("| feature | rank corr with kill round (kills only, n=%d) |"
               % sum(1 for r in rows if r["y_corekill"] == "1"))
    out.append("| --- | ---: |")
    kills = [r for r in rows if r["y_corekill"] == "1"]
    from analyze import ranks as _ranks
    for c, lab in ROBUST:
        ra = _ranks([float(r[c]) for r in kills])
        rb = _ranks([float(r["turns"]) for r in kills])
        n = len(ra)
        ma, mb = sum(ra) / n, sum(rb) / n
        num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
        den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5
        out.append(f"| `{c}` {lab} | {num/den if den else 0:+.3f} |")

    Path(outp).write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
