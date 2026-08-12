#!/usr/bin/env python3
"""Per-game attacker-oriented summary.  Read-only."""
import json
from collections import Counter, defaultdict

DMG = {'sentinel': 18, 'gunner': 7, 'builder_atk': 2}
POPS = {p['file']: p for p in json.load(open('scratchpad/dv_pops.json'))}
TL = {}
for line in open('scratchpad/dv_tl.ndjson'):
    r = json.loads(line)
    TL[r['file']] = r


def orient(fn):
    """(attacker_team, victim_team, pop) -- attacker is the team we want to study."""
    p = POPS[fn]
    pop = p['pop']
    if pop == 'DV_THIRD':
        dv = 0 if p['dv_side'] == 'a' else 1
        return dv, 1 - dv, pop
    us = 0 if p['us_side'] == 'a' else 1
    if pop in ('US_FASTWIN', 'DV_FASTWIN', 'DV_SLOWWIN'):
        return us, 1 - us, pop           # WE are the attacker
    return 1 - us, us, pop               # they are the attacker


def summary(fn):
    r = TL[fn]
    A, V, pop = orient(fn)
    p = POPS[fn]
    cd = [c for c in r['core_dmg'] if c[1] == V and c[2] == A]
    s = {'file': fn, 'pop': pop, 'turns': r['turns'], 'wincond': r['wincond'],
         'w': r['w'], 'h': r['h'], 'core_d2': r['core_d2'],
         'A': A, 'V': V, 'opp': p.get('opp'), 'map': p.get('map'),
         'ourver': p.get('ourver'), 'created': p.get('created')}
    s['A_won'] = (r['winner'] == A)
    s['n_core_hits'] = len(cd)
    s['core_dmg_total'] = sum(DMG.get(c[3], 0) for c in cd)
    s['t_first_core_dmg'] = min((c[0] for c in cd), default=None)
    kc = Counter(c[3] for c in cd)
    s['hits_by_kind'] = dict(kc)
    s['dmg_by_kind'] = {k: v * DMG.get(k, 0) for k, v in kc.items()}
    srcs = {}
    for rnd, vt, at, kind, sx, sy, sid in cd:
        srcs.setdefault(sid, [kind, sx, sy, rnd, 0])[4] += DMG.get(kind, 0)
    s['n_src'] = len(srcs)
    s['src'] = [[v[0], v[1], v[2], v[3], v[4]] for v in srcs.values()]
    vcore = r['corepos'][str(V)]
    acore = r['corepos'][str(A)]
    def d2(a, b): return (a[0]-b[0])**2 + (a[1]-b[1])**2
    s['src_d2_victim'] = [d2((v[1], v[2]), vcore) for v in srcs.values()]
    s['src_d2_own'] = [d2((v[1], v[2]), acore) for v in srcs.values()]
    # builds by attacker
    fb = {}
    cnt = Counter()
    fwd = Counter()          # built closer to victim core than to own
    tfd = s['t_first_core_dmg'] if s['t_first_core_dmg'] is not None else 10**9
    pre = Counter()
    for rnd, t, kind, x, y in r['builds']:
        if t != A:
            continue
        cnt[kind] += 1
        fb.setdefault(kind, rnd)
        if d2((x, y), vcore) < d2((x, y), acore):
            fwd[kind] += 1
        if rnd <= tfd:
            pre[kind] += 1
    s['first_build'] = fb
    s['builds_total'] = dict(cnt)
    s['builds_fwd'] = dict(fwd)
    s['builds_pre'] = dict(pre)
    s['reach'] = {k.split(':')[1]: v for k, v in r['reach'].items() if k.startswith(f'{A}:')}
    s['reach_V'] = {k.split(':')[1]: v for k, v in r['reach'].items() if k.startswith(f'{V}:')}
    # economy at the moment of first core damage
    ec = None
    for row in r['econ']:
        if row[0] <= tfd:
            ec = row
        else:
            break
    if ec:
        off = 1 if A == 0 else 4
        s['ti_at_commit'] = ec[off]
        s['coll_at_commit'] = ec[off+1]
        s['ammo_at_commit'] = ec[off+2]
    # victim core HP trace: rounds from first damage to death
    s['kill_span'] = (r['turns'] - 1 - s['t_first_core_dmg']) if s['t_first_core_dmg'] is not None else None
    # did the victim core die?
    s['victim_core_died'] = any(d[1] == V and d[2] == 'core' for d in r['deaths'])
    return s


ALL = [summary(fn) for fn in TL]
if __name__ == '__main__':
    json.dump(ALL, open('scratchpad/dv_sum.json', 'w'))
    print(Counter(s['pop'] for s in ALL))
