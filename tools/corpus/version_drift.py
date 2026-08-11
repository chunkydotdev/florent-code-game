#!/usr/bin/env python3
"""version_drift.py — TACTICS SWEEP 22 instrument (research arm, 2026-08-11).

THE QUESTION: our experiments assume the opponent population is stationary. It is not.
This measures, league-wide off `corpus/league_matches.tsv` (per-match `teamAVersion` /
`teamBVersion` for every team, not just ours):

  1  FIELD   — how fast the field re-versions, and how long a version lives.
  2  BIAS    — what pooling a per-opponent statistic across an opponent's versions
               costs, BLOCKED so our own version is frozen inside the block.
  3  FRESH   — whether a freshly-shipped version is weaker (the "un-debugged" read).
  4  ROLLBACK— the A->B->A excursion signature of a rival's own prototype window.

EVERY CUT CARRIES A CONTROL THAT MUST PRODUCE THE OTHER VERDICT. Specifically:
  - coinflip split inside the block          -> must be null (it is: |t| < 1)
  - opponent version debut order shuffled    -> must be null (it is: t = +1.25)
  - opponent version CONSTANT, split by TIME -> must be null, and this is the one that
    kills the censoring story (a block ENDS when the team ships, and teams ship after a
    bad run, so a pure time trend would fake the whole effect). It is null: t = -0.61.
  - timestamp-ambiguity guard on the rollback cut (within-second ordering could
    MANUFACTURE excursions). Measured 0.00% ambiguous; strict == naive.

Usage:  python3 tools/corpus/version_drift.py [path/to/league_matches.tsv]
No dependencies beyond the stdlib.
"""
import csv
import random
import statistics as st
import sys
from collections import defaultdict
from datetime import datetime

DEFAULT = "corpus/league_matches.tsv"


def ts(s):
    return datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")


def load(path):
    """-> list of (team, own_version, opponent, opp_version, time, game_share, elo_delta)."""
    out = []
    with open(path) as f:
        for r in csv.DictReader(f, delimiter="\t"):
            try:
                sa, sb = int(r["scoreA"]), int(r["scoreB"])
                da, db = float(r["eloDeltaA"]), float(r["eloDeltaB"])
                t = ts(r["createdAt"])
            except (ValueError, KeyError, TypeError):
                continue
            tot = sa + sb
            if tot == 0:
                continue
            out.append((r["teamAName"], r["teamAVersion"], r["teamBName"],
                        r["teamBVersion"], t, sa / tot, da))
            out.append((r["teamBName"], r["teamBVersion"], r["teamAName"],
                        r["teamAVersion"], t, sb / tot, db))
    return out


def mean_se(v):
    m = st.mean(v)
    se = st.stdev(v) / len(v) ** 0.5 if len(v) > 1 else float("nan")
    return m, se, (m / se if se == se and se > 0 else float("nan"))


# ---------------------------------------------------------------- 1. FIELD
def field(recs):
    print("\n=== 1. HOW FAST THE FIELD RE-VERSIONS ===")
    side = defaultdict(list)
    for tm, mv, opp, ov, t, s, e in recs:
        side[tm].append((t, mv))
    for k in side:
        side[k].sort()
    active = {k: v for k, v in side.items() if len(v) >= 20}
    vers = {k: len({v for _, v in g}) for k, g in active.items()}
    chg = {k: sum(1 for a, b in zip(g, g[1:]) if a[1] != b[1]) for k, g in active.items()}
    print(f"teams with >=20 matches: {len(active)}")
    print(f"distinct versions/team: median {st.median(vers.values())}, max {max(vers.values())}")
    print(f"version CHANGES/team:   median {st.median(chg.values())}, max {max(chg.values())}")
    print(f"teams that never changed version: {sum(1 for v in chg.values() if v == 0)}/{len(chg)}")

    # version lifetime = time from a version's debut until that team's NEXT version debuts
    seen = defaultdict(list)
    for tm, g in side.items():
        for t, v in g:
            seen[(tm, v)].append(t)
    bytm = defaultdict(list)
    for (tm, v), lst in seen.items():
        bytm[tm].append((min(lst), v))
    lives, censored = [], 0
    for tm, lst in bytm.items():
        if len(lst) < 5:
            continue
        lst.sort()
        for i, (a, v) in enumerate(lst):
            nxt = [x[0] for x in lst[i + 1:] if x[0] > a]
            if not nxt:
                censored += 1
                continue
            lives.append((min(nxt) - a).total_seconds() / 3600)
    lives.sort()
    print(f"\nVERSION LIFETIME (hours), n={len(lives)} (right-censored dropped: {censored})")
    for p in (10, 25, 50, 75, 90):
        print(f"   p{p:<3d} = {lives[int(len(lives) * p / 100)]:7.2f} h")
    for h in (1, 6, 24):
        print(f"   replaced within {h:2d}h: {100 * sum(1 for x in lives if x <= h) / len(lives):5.1f}%")


# ------------------------------------------------- 2. THE POOLING BIAS (BLOCKED)
def pooling_bias(recs):
    print("\n=== 2. POOLING BIAS — BLOCK = (team, TEAM'S OWN VERSION, opponent) ===")
    print("    our side is FROZEN inside a block, so only the opponent's version moves")
    debut = {}
    for tm, mv, opp, ov, t, s, e in recs:
        k = (opp, ov)
        if k not in debut or t < debut[k]:
            debut[k] = t
    blocks = defaultdict(list)
    for tm, mv, opp, ov, t, s, e in recs:
        blocks[(tm, mv, opp)].append((ov, t, s))

    def split(keyfn, label, seed=None):
        rng = random.Random(seed)
        diffs, nb, ng, seps = [], 0, 0, []
        for (tm, mv, opp), g in blocks.items():
            keyed = [(keyfn(opp, ov, t, rng), t, s) for ov, t, s in g]
            vals = sorted({k for k, _, _ in keyed})
            if len(vals) < 2:
                continue
            cut = vals[len(vals) // 2]
            o = [(t, s) for k, t, s in keyed if k < cut]
            n = [(t, s) for k, t, s in keyed if k >= cut]
            if len(o) < 2 or len(n) < 2:
                continue
            nb += 1
            ng += len(g)
            diffs.append(st.mean(s for _, s in n) - st.mean(s for _, s in o))
            seps.append((st.mean(t.timestamp() for t, _ in n)
                         - st.mean(t.timestamp() for t, _ in o)) / 3600)
        if len(diffs) < 2:
            print(f"  {label}: too few blocks")
            return None
        m, se, t_ = mean_se(diffs)
        print(f"  {label}: blocks={nb:5d} games={ng:6d}  later-earlier={m:+.4f} +/- {se:.4f}  t={t_:+.2f}")
        return diffs, seps

    real = split(lambda opp, ov, t, rng: debut[(opp, ov)],
                 "REAL    opponent version order    ")
    # control i: shuffle debut labels within opponent
    byopp = defaultdict(list)
    for (opp, ov), d in debut.items():
        byopp[opp].append((ov, d))
    rng0 = random.Random(22)
    fake = {}
    for opp, lst in byopp.items():
        ds = [d for _, d in lst]
        rng0.shuffle(ds)
        for (ov, _), d in zip(lst, ds):
            fake[(opp, ov)] = d
    split(lambda opp, ov, t, rng: fake[(opp, ov)],
          "CTRL-i  shuffled version order    ")
    # control ii: coinflip, null by construction
    for s in (1, 2, 3):
        split(lambda opp, ov, t, rng: rng.random(),
              f"CTRL-ii coinflip split (seed {s})  ", seed=s)

    # control iii: THE DISCRIMINATING ONE — opponent version constant, split by time.
    # A block ends when the team ships, and teams ship after a bad run; if that censoring
    # drove the effect it MUST reappear here.
    diffs, nb, ng = [], 0, 0
    for k, g in blocks.items():
        if len({ov for ov, _, _ in g}) != 1 or len(g) < 4:
            continue
        g2 = sorted(g, key=lambda x: x[1])
        h = len(g2) // 2
        o = [s for _, _, s in g2[:h]]
        n = [s for _, _, s in g2[h:]]
        if len(o) < 2 or len(n) < 2:
            continue
        nb += 1
        ng += len(g2)
        diffs.append(st.mean(n) - st.mean(o))
    m, se, t_ = mean_se(diffs)
    print(f"  CTRL-iii opp version CONSTANT,")
    print(f"           split by median TIME     : blocks={nb:5d} games={ng:6d}  "
          f"later-earlier={m:+.4f} +/- {se:.4f}  t={t_:+.2f}")
    print("           ^ kills the censoring story: must be strongly negative if time drove it")

    if real:
        diffs, seps = real
        print(f"\n  median time separation between halves: {st.median(seps):.2f} h")
        print("  DOSE-RESPONSE by that separation (the effect is a STEP, not a per-day rate):")
        for lo, hi in ((0, 3), (3, 8), (8, 16), (16, 36), (36, 1e9)):
            sub = [d for d, sp in zip(diffs, seps) if lo <= sp < hi]
            if len(sub) < 20:
                continue
            m, se, t_ = mean_se(sub)
            hl = "inf" if hi > 1e8 else str(hi)
            print(f"    {lo:>3}-{hl:>4}h  n={len(sub):5d}  {m:+.4f} +/- {se:.4f}  t={t_:+.2f}")


# ------------------------------------------------------- 3. IS A FRESH VERSION WEAK?
def freshness(recs):
    print("\n=== 3. IS A FRESHLY-SHIPPED VERSION WEAKER? (outcome = eloDelta) ===")
    side = defaultdict(list)
    for tm, mv, opp, ov, t, s, e in recs:
        side[tm].append(dict(t=t, ver=mv, elo=e))
    for k in side:
        side[k].sort(key=lambda d: d["t"])
    teams = {k: v for k, v in side.items() if len(v) >= 40}

    K = 5
    pre = lambda g, i: st.mean(d["elo"] for d in g[i - K:i])
    post = lambda g, i: st.mean(d["elo"] for d in g[i:i + K])
    real, pool = [], defaultdict(list)
    for tm, g in teams.items():
        for i in range(K, len(g) - K):
            if g[i]["ver"] != g[i - 1]["ver"]:
                real.append((tm, pre(g, i), post(g, i)))
            elif g[i + K - 1]["ver"] == g[i]["ver"]:
                pool[tm].append((pre(g, i), post(g, i)))
    # NOTE: teams ship WHEN THEY ARE LOSING, so the naive pre/post gain is mostly mean
    # reversion. The control is matched on the pre-window to remove exactly that.
    rng = random.Random(22)
    rd, cd, unmatched = [], [], 0
    for tm, p, q in real:
        cands = [c for c in pool.get(tm, []) if abs(c[0] - p) <= 0.40]
        if not cands:
            unmatched += 1
            continue
        c = rng.choice(cands)
        rd.append(q - p)
        cd.append(c[1] - c[0])
    print(f"  matched pairs: {len(rd)} (unmatched dropped: {unmatched})")
    for lab, v in (("REAL version change", rd), ("MATCHED CONTROL   ", cd)):
        m, se, t_ = mean_se(v)
        print(f"  {lab}: {m:+.3f} +/- {se:.3f}  t={t_:+.2f}")
    m, se, t_ = mean_se([a - b for a, b in zip(rd, cd)])
    print(f"  DIFFERENCE-IN-DIFFERENCES: {m:+.3f} +/- {se:.3f}  t={t_:+.2f}"
          f"   (positive => a fresh version is STRONGER, not weaker)")

    print("\n  eloDelta by VERSION AGE, team-demeaned:")
    buckets = defaultdict(list)
    for tm, g in teams.items():
        tmean = st.mean(d["elo"] for d in g)
        age = None
        for i, d in enumerate(g):
            age = 0 if (i == 0 or g[i]["ver"] != g[i - 1]["ver"]) else age + 1
            b = 0 if age == 0 else 1 if age <= 2 else 2 if age <= 5 else 3 if age <= 10 else 4
            buckets[b].append(d["elo"] - tmean)
    lab = {0: "first match on new ver", 1: "matches 2-3", 2: "matches 4-6",
           3: "matches 7-11", 4: "matches 12+"}
    for b in sorted(buckets):
        m, se, t_ = mean_se(buckets[b])
        print(f"    {lab[b]:24s} n={len(buckets[b]):6d}  {m:+.3f} +/- {se:.3f}  "
              f"t={t_:+.2f}   SD={st.stdev(buckets[b]):.3f}")
    print("    ^ the SD column is the real 'un-debugged' signature: fresh versions are")
    print("      more ERRATIC, while their MEAN is no worse.")


# ------------------------------------------------------------- 4. ROLLBACK SIGNATURE
def rollback(recs):
    print("\n=== 4. THE A->B->A ROLLBACK EXCURSION (a rival's own prototype window) ===")
    side = defaultdict(list)
    for tm, mv, opp, ov, t, s, e in recs:
        side[tm].append((t, mv))
    for k in side:
        side[k].sort()
    # GUARD: if one team had two versions inside a single timestamp, within-second
    # ordering would MANUFACTURE excursions. Measure it before trusting the cut.
    amb = tot = 0
    for tm, g in side.items():
        bt = defaultdict(set)
        for t, v in g:
            bt[t].add(v)
        for t, vs in bt.items():
            tot += 1
            amb += len(vs) > 1
    print(f"  timestamp-ambiguity guard: {amb}/{tot} = {100 * amb / tot:.2f}% "
          f"of same-team timestamps carry >1 version")

    for strict in (False, True):
        nt = nex = exm = allm = 0
        rows = []
        for tm, g in side.items():
            if len(g) < 40:
                continue
            nt += 1
            allm += len(g)
            runs = []
            for t, v in g:
                if not runs or runs[-1][0] != v:
                    runs.append([v, t, t, 1])
                else:
                    runs[-1][2] = t
                    runs[-1][3] += 1
            exc = []
            for i in range(1, len(runs) - 1):
                if runs[i - 1][0] == runs[i + 1][0] and runs[i][0] != runs[i - 1][0]:
                    if strict and not (runs[i][1] > runs[i - 1][2] and runs[i + 1][1] > runs[i][2]):
                        continue
                    exc.append(runs[i])
            if exc:
                nex += 1
                exm += sum(x[3] for x in exc)
                rows.append((tm, len(exc), sum(x[3] for x in exc)))
        print(f"  [{'STRICT' if strict else 'NAIVE ':6s}] teams with an excursion: "
              f"{nex}/{nt} ({100 * nex / nt:.1f}%); matches inside: "
              f"{exm}/{allm} = {100 * exm / allm:.2f}%")
        if strict:
            for tm, n, m in sorted(rows, key=lambda x: -x[1])[:10]:
                print(f"      {tm[:34]:34s} {n:4d} excursions, {m:5d} matches")


def excursion_strength(recs):
    """5. THE DISCRIMINATOR for section 4: is a rolled-back version a HIDDEN STRONG bot
    (the CodinGame 'AI hiding' reading) or just a BAD SHIP? Compare each excursion version
    against the incumbent that brackets it, paired within excursion."""
    print("\n=== 5. ARE ROLLED-BACK VERSIONS STRONGER OR WEAKER THAN THE INCUMBENT? ===")
    side = defaultdict(list)
    for tm, mv, opp, ov, t, s, e in recs:
        side[tm].append((t, mv, s, e))
    for k in side:
        side[k].sort()
    ex_s, ho_s, ex_e, ho_e, n, g_n = [], [], [], [], 0, 0
    for tm, g in side.items():
        if len(g) < 40:
            continue
        runs = []
        for t, v, s, e in g:
            if not runs or runs[-1][0] != v:
                runs.append([v, [(s, e)]])
            else:
                runs[-1][1].append((s, e))
        for i in range(1, len(runs) - 1):
            if runs[i - 1][0] == runs[i + 1][0] and runs[i][0] != runs[i - 1][0]:
                ex, host = runs[i][1], runs[i - 1][1] + runs[i + 1][1]
                if len(host) < 3:
                    continue
                n += 1
                g_n += len(ex)
                ex_s.append(st.mean(x[0] for x in ex))
                ho_s.append(st.mean(x[0] for x in host))
                ex_e.append(st.mean(x[1] for x in ex))
                ho_e.append(st.mean(x[1] for x in host))
    if not ex_s:
        print("  no excursions found")
        return
    print(f"  excursions with >=3 bracketing incumbent games: {n} "
          f"(excursion games: {g_n})")
    for lab, a, b in (("game share", ex_s, ho_s), ("eloDelta  ", ex_e, ho_e)):
        m, se, t_ = mean_se([x - y for x, y in zip(a, b)])
        print(f"    {lab}: excursion {st.mean(a):+.4f} | incumbent {st.mean(b):+.4f} | "
              f"paired diff {m:+.4f} +/- {se:.4f}  t={t_:+.2f}")
    print("  NEGATIVE => rolled-back versions are BAD SHIPS, not hidden strength.")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
    recs = load(path)
    print(f"sides loaded: {len(recs)} (from {len(recs) // 2} matches) — {path}")
    field(recs)
    pooling_bias(recs)
    freshness(recs)
    rollback(recs)
    excursion_strength(recs)


if __name__ == "__main__":
    main()
