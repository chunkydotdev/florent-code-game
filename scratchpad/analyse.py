#!/usr/bin/env python3
"""Fidelity + recency analysis for the LOKI-14b natural-border-crash control."""
import json, collections, math, sys

res = []
for i in range(6):
    res += json.load(open(f'scratchpad/out_{i}.json'))
meta = json.load(open('scratchpad/jobmeta.json'))
FREEZE = '2026-08-10T04:05:34'
CARRIERS = ['vjg', 'Troupe', 'S', 'Ship Happens']


def key(r):
    return f"{r['file']}|{r['tag'].split('|')[0]}"


def rows(pred=lambda m: True, midgame=True):
    """Yield (carrier, meta, result) for results whose meta passes pred."""
    for r in res:
        m = meta[key(r)]
        if pred(m):
            yield r['tag'].split('|')[0], m, r


def agg(pred, midgame_only=True, exclude_thrown=True):
    A = collections.defaultdict(lambda: dict(games=0, br=0, obr=0, ub=0, uo=0,
                                             dmg=0, thrown_und=0, ub_final=0,
                                             uo_final=0, dmg_b=0))
    for c, m, r in rows(pred):
        a = A[c]
        a['games'] += 1
        a['br'] += r['border_builder_rounds']
        a['obr'] += r['offborder_builder_rounds']
        for e in r['undamaged']:
            if midgame_only and e['final']:
                (a['ub_final'] if e['border'] else a['uo_final'])
                a['ub_final' if e['border'] else 'uo_final'] += 1
                continue
            if exclude_thrown and e['thrown3']:
                a['thrown_und'] += 1
                continue
            a['ub' if e['border'] else 'uo'] += 1
        for e in r['damage_killed']:
            if midgame_only and e['final']:
                continue
            a['dmg'] += 1
            if e['border']:
                a['dmg_b'] += 1
    return A


def haz(n, d):
    return (n / d * 1e4) if d else float('nan')


def show(title, A):
    print(f"\n=== {title} ===")
    print(f"{'team':14s}{'games':>7s}{'brdRnds':>10s}{'offRnds':>10s}"
          f"{'U_brd':>7s}{'U_off':>7s}{'haz_brd/10k':>13s}{'haz_off/10k':>13s}"
          f"{'D':>6s}{'U_final':>9s}{'thrown':>8s}")
    tot = collections.Counter()
    for c in CARRIERS:
        a = A.get(c)
        if not a:
            continue
        for k, v in a.items():
            tot[k] += v
        print(f"{c:14s}{a['games']:>7d}{a['br']:>10,d}{a['obr']:>10,d}"
              f"{a['ub']:>7d}{a['uo']:>7d}{haz(a['ub'], a['br']):>13.2f}"
              f"{haz(a['uo'], a['obr']):>13.3f}{a['dmg']:>6d}"
              f"{a['ub_final']+a['uo_final']:>9d}{a['thrown_und']:>8d}")
    print(f"{'POOLED':14s}{tot['games']:>7d}{tot['br']:>10,d}{tot['obr']:>10,d}"
          f"{tot['ub']:>7d}{tot['uo']:>7d}{haz(tot['ub'], tot['br']):>13.2f}"
          f"{haz(tot['uo'], tot['obr']):>13.3f}{tot['dmg']:>6d}"
          f"{tot['ub_final']+tot['uo_final']:>9d}{tot['thrown_und']:>8d}")
    return tot


# 1. FIDELITY: pre-freeze population, mid-game (exclude final-round removals)
show("FIDELITY: pre-freeze (completedAt < %s), mid-game, thrown excluded" % FREEZE,
     agg(lambda m: m['completedAt'] < FREEZE))
# variant: include final-round removals
show("variant: pre-freeze, ALL removals incl. final round",
     agg(lambda m: m['completedAt'] < FREEZE, midgame_only=False))
# 2. FULL archive
show("FULL ARCHIVE (all archived ladder games, mid-game)", agg(lambda m: True))

# 3. per-day buckets
print("\n=== PER-DAY (completedAt date), mid-game, thrown excluded ===")
print(f"{'team':14s}{'date':12s}{'ver':>5s}{'games':>7s}{'brdRnds':>10s}"
      f"{'U_brd':>7s}{'U_off':>7s}{'haz_brd/10k':>13s}{'offRnds':>10s}")
for c in CARRIERS:
    days = sorted({m['date'] for cc, m, r in rows() if cc == c})
    for d in days:
        A = agg(lambda m, d=d: m['date'] == d)
        a = A.get(c)
        if not a:
            continue
        vers = sorted({m['ver'] for cc, m, r in rows(lambda m, d=d: m['date'] == d)
                       if cc == c})
        print(f"{c:14s}{d:12s}{'/'.join(vers):>5s}{a['games']:>7d}{a['br']:>10,d}"
              f"{a['ub']:>7d}{a['uo']:>7d}{haz(a['ub'], a['br']):>13.2f}{a['obr']:>10,d}")

# 4. most recent event + exposure since
print("\n=== MOST RECENT NATURAL BORDER EVENT, and exposure since ===")
for c in CARRIERS:
    evs = []
    games = []
    for cc, m, r in rows():
        if cc != c:
            continue
        n = sum(1 for e in r['undamaged']
                if e['border'] and not e['final'] and not e['thrown3'])
        games.append((m['completedAt'], r['border_builder_rounds'],
                      r['offborder_builder_rounds'], n, m['ver'], r['file']))
    games.sort()
    lastev = max((g for g in games if g[3] > 0), default=None)
    if lastev is None:
        print(f"{c}: NO natural border events at all in archive")
        continue
    after = [g for g in games if g[0] > lastev[0]]
    print(f"{c:14s} last event {lastev[0]}  (ver {lastev[4]}, {lastev[3]} event(s), "
          f"file {lastev[5]})")
    print(f"{'':14s} games completed AFTER that: {len(after)}  "
          f"border builder-rounds since: {sum(g[1] for g in after):,}  "
          f"events since: {sum(g[3] for g in after)}")
    # trailing-window views
    for cut in ('2026-08-10T00:00:00', '2026-08-09T12:00:00', '2026-08-10T06:00:00'):
        w = [g for g in games if g[0] >= cut]
        print(f"{'':14s} since {cut}: {len(w):3d} games, "
              f"{sum(g[1] for g in w):>8,d} border builder-rounds, "
              f"{sum(g[3] for g in w):>4d} events, "
              f"haz {haz(sum(g[3] for g in w), sum(g[1] for g in w)):.2f}/10k")

# 5. exposure threshold: border rounds needed so that P(0 | historical rate) < 5%
print("\n=== MINIMUM-EXPOSURE THRESHOLD (per carrier, derived) ===")
A = agg(lambda m: m['completedAt'] < FREEZE)
for c in CARRIERS:
    a = A[c]
    h = a['ub'] / a['br']            # per border builder-round
    n95 = math.log(0.05) / math.log(1 - h)
    n3 = 3 / h
    print(f"{c:14s} historical hazard {h*1e4:7.2f}/10k -> "
          f"P(0)<5% at {n95:,.0f} border builder-rounds; "
          f"E[events]=3 at {n3:,.0f}")
