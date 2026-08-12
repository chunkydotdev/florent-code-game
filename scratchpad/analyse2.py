#!/usr/bin/env python3
"""Fidelity gate + controls + recency split. Read-only, scratch."""
import json, collections, math

res = []
for i in range(6):
    res += json.load(open(f'scratchpad/out_{i}.json'))
meta = json.load(open('scratchpad/jobmeta.json'))
FREEZE = '2026-08-10T04:05:34'
CARRIERS = ['vjg', 'Troupe', 'S', 'Ship Happens']
CONTROLS = ['Cookie', 'Ouroboros']


def team(r):
    return r['tag'].split('|')[0]


def m_of(r):
    return meta[f"{r['file']}|{team(r)}"]


def classify(r, rule):
    """Yield (border, event) for each undamaged builder removal under `rule`.

    rule 'strict'  -> crash_census: NO updateHp ever (what the leg's estimator uses)
    rule 'loose'   -> census doc: reconstructed hp at removal > 0
    """
    for e in r['undamaged'] + r['damage_killed']:
        if e['final'] or e['thrown3']:
            continue
        if rule == 'strict':
            ok = e['nohp']
        else:
            ok = e['hp_at'] is not None and e['hp_at'] > 0
        if ok:
            yield e['border']


def agg(pred, rule):
    A = collections.defaultdict(lambda: dict(g=0, br=0, obr=0, ub=0, uo=0,
                                             thr=0, thrown_ev=0, dfinal=0))
    for r in res:
        m = m_of(r)
        if not pred(m, r):
            continue
        a = A[team(r)]
        a['g'] += 1
        a['br'] += r['border_builder_rounds']
        a['obr'] += r['offborder_builder_rounds']
        a['thr'] += r['throws_of_own_builders']
        for b in classify(r, rule):
            a['ub' if b else 'uo'] += 1
        for e in r['undamaged'] + r['damage_killed']:
            if e['thrown3'] and (e['nohp'] if rule == 'strict'
                                 else (e['hp_at'] or 0) > 0):
                a['thrown_ev'] += 1
            if e['final'] and (e['nohp'] if rule == 'strict'
                               else (e['hp_at'] or 0) > 0):
                a['dfinal'] += 1
    return A


def h(n, d):
    return n / d * 1e4 if d else float('nan')


def table(title, A, teams):
    print(f"\n=== {title} ===")
    print(f"{'team':14s}{'games':>6s}{'brdRnds':>10s}{'offRnds':>11s}{'U_brd':>7s}"
          f"{'U_off':>7s}{'haz_brd/10k':>12s}{'haz_off/10k':>12s}{'thrws':>7s}")
    tot = collections.Counter()
    for c in teams:
        a = A.get(c)
        if not a:
            continue
        for k, v in a.items():
            tot[k] += v
        print(f"{c:14s}{a['g']:>6d}{a['br']:>10,d}{a['obr']:>11,d}{a['ub']:>7d}"
              f"{a['uo']:>7d}{h(a['ub'],a['br']):>12.2f}{h(a['uo'],a['obr']):>12.3f}"
              f"{a['thr']:>7d}")
    if len(teams) > 1:
        print(f"{'POOLED':14s}{tot['g']:>6d}{tot['br']:>10,d}{tot['obr']:>11,d}"
              f"{tot['ub']:>7d}{tot['uo']:>7d}{h(tot['ub'],tot['br']):>12.2f}"
              f"{h(tot['uo'],tot['obr']):>12.3f}{tot['thr']:>7d}")
    return tot


print("### FIDELITY GATE — pre-freeze population (completedAt < %s)" % FREEZE)
pre = lambda m, r: m['completedAt'] < FREEZE
table("rule=LOOSE (census doc: hp_at_removal > 0)  vs prereg 1517/345/293/246",
      agg(pre, 'loose'), CARRIERS)
table("rule=STRICT (crash_census.py: no updateHp ever) — the LEG's estimator",
      agg(pre, 'strict'), CARRIERS)
print("\n### CONTROLS — the decoder must return the OTHER verdict somewhere")
table("controls, pre-freeze, rule=LOOSE (doc: Cookie 119 U, 106 off-border; "
      "Ouroboros 56 U, 44 off-border)", agg(pre, 'loose'), CONTROLS)

print("\n### FULL ARCHIVE (every archived ladder game, up to now)")
table("rule=STRICT", agg(lambda m, r: True, 'strict'), CARRIERS)
table("rule=LOOSE", agg(lambda m, r: True, 'loose'), CARRIERS)

print("\n### PER-DAY, rule=STRICT")
print(f"{'team':14s}{'date':11s}{'ver':>4s}{'games':>6s}{'brdRnds':>9s}{'U_brd':>7s}"
      f"{'haz/10k':>9s}{'offRnds':>10s}{'U_off':>6s}")
for c in CARRIERS + CONTROLS:
    for d in sorted({m_of(r)['date'] for r in res if team(r) == c}):
        a = agg(lambda m, r, d=d: m['date'] == d, 'strict').get(c)
        vers = '/'.join(sorted({m_of(r)['ver'] for r in res
                                if team(r) == c and m_of(r)['date'] == d}))
        print(f"{c:14s}{d:11s}{vers:>4s}{a['g']:>6d}{a['br']:>9,d}{a['ub']:>7d}"
              f"{h(a['ub'],a['br']):>9.2f}{a['obr']:>10,d}{a['uo']:>6d}")

print("\n### RECENCY — last natural border event + exposure since, rule=STRICT")
now_games = collections.defaultdict(list)
for r in res:
    m = m_of(r)
    n = sum(1 for b in classify(r, 'strict') if b)
    now_games[team(r)].append((m['completedAt'], r['border_builder_rounds'],
                               n, m['ver'], r['file']))
for c in CARRIERS:
    g = sorted(now_games[c])
    ev = [x for x in g if x[2] > 0]
    last = ev[-1]
    after = [x for x in g if x[0] > last[0]]
    print(f"\n{c}: {len(g)} archived ladder games, "
          f"{sum(x[1] for x in g):,} border builder-rounds, "
          f"{sum(x[2] for x in g)} natural border events; version(s) "
          f"{sorted({x[3] for x in g})}")
    print(f"  LAST natural border event: {last[0]} (their version {last[3]})")
    print(f"  since then: {len(after)} games, {sum(x[1] for x in after):,} "
          f"border builder-rounds, {sum(x[2] for x in after)} events")
    for cut in ('2026-08-10T00:00:00', '2026-08-10T06:00:00',
                '2026-08-10T10:00:00', '2026-08-10T12:00:00'):
        w = [x for x in g if x[0] >= cut]
        br = sum(x[1] for x in w)
        n = sum(x[2] for x in w)
        print(f"  since {cut}Z: {len(w):3d} games, {br:>7,d} border "
              f"builder-rounds, {n:>4d} events, haz {h(n,br):8.2f}/10k")

print("\n### DERIVED MINIMUM-EXPOSURE THRESHOLD (per carrier)")
A = agg(pre, 'strict')
for c in CARRIERS:
    a = A[c]
    p = a['ub'] / a['br']
    print(f"{c:14s} historical hazard {p*1e4:7.2f}/10k  -> "
          f"P(0 events)<5% once exposure >= {math.log(0.05)/math.log(1-p):,.0f} "
          f"border builder-rounds (E[events]=3 at {3/p:,.0f})")
