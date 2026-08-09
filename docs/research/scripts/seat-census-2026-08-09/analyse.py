#!/usr/bin/env python3
"""GATE 1 (seat staffing) + GATE 2 (idle supply) over seat_decode output."""
import csv
import sys
import collections

SC = '/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/seats'


def load(outdir):
    G = {r['file']: r for r in csv.DictReader(open(f'{outdir}/seat_games.tsv'),
                                              delimiter='\t')}
    R = collections.defaultdict(list)
    for r in csv.DictReader(open(f'{outdir}/seat_rounds.tsv'), delimiter='\t'):
        R[r['file']].append(r)
    return G, R


def outcome(j):
    if j['cond'] == 'core_destroyed':
        return 'LOSS_CORE_DIED' if j['won'] == '0' else 'WIN_CORE_KILL'
    return 'TIEBREAK'


BUCKETS = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 5), (6, 8), (9, 12)]


def bucketise(vals):
    c = collections.Counter()
    for v in vals:
        for lo, hi in BUCKETS:
            if lo <= v <= hi:
                c[(lo, hi)] += 1
                break
        else:
            c[('13+', '')] += 1
    return c


def show(name, vals, n_label='rounds'):
    n = len(vals)
    if not n:
        print(f'  {name}: n=0')
        return
    c = bucketise(vals)
    parts = []
    for k in BUCKETS + [('13+', '')]:
        if c[k]:
            lab = str(k[0]) if k[0] == k[1] else (f'{k[0]}-{k[1]}' if k[1] != ''
                                                  else '13+')
            parts.append(f'{lab}:{100*c[k]/n:.1f}%')
    mean = sum(vals) / n
    sv = sorted(vals)
    print(f'  {name:<34} n={n:<7} mean={mean:5.2f} med={sv[n//2]:<3} '
          f'p90={sv[int(.9*n)]:<3} max={sv[-1]:<3} | ' + ' '.join(parts))


def main(outdir, tag, only_cad):
    J = {r['file']: r for r in csv.DictReader(open(f'{SC}/join_frozen.tsv'),
                                              delimiter='\t')}
    G, R = load(outdir)
    print(f'==== {tag}  games decoded: {len(G)} ====')

    # ---------------- validation ----------------
    bad = collections.Counter()
    ratios = []
    for f, g in G.items():
        hc, hp = int(g['tot_heal_core']), int(g['tot_coreheal_hp'])
        if hc:
            ratios.append(hp / (4 * hc))
        if int(g['max_seat']) > 8:
            bad['max_seat>8'] += 1
        if int(g['max_fp']) > 4:
            bad['max_fp>4'] += 1
        if g['acd_vals'] and not all(x.startswith('1:')
                                     for x in g['acd_vals'].split(';')):
            bad['acd!=1'] += 1
        if g['mcd_vals'] and not all(x.startswith('1:')
                                     for x in g['mcd_vals'].split(';')):
            bad['mcd!=1'] += 1
        if int(g['bad_pos']):
            bad['bad_pos'] += 1
    ratios.sort()
    print(f'VALID heal-HP / (4 x heal_core_events): n={len(ratios)} '
          f'median={ratios[len(ratios)//2]:.4f} '
          f'min={ratios[0]:.4f} max={ratios[-1]:.4f}')
    tot_bo = sum(int(g['tot_botoutput']) for g in G.values())
    tot_br = sum(int(g['tot_builder_rounds']) for g in G.values())
    print(f'VALID botOutput rows {tot_bo} vs builder-rounds {tot_br} '
          f'({100*tot_bo/tot_br:.4f}%)')
    print(f'VALID max_fp>0 games: '
          f'{sum(1 for g in G.values() if int(g["max_fp"])>0)}/{len(G)}; '
          f'max over set = {max(int(g["max_fp"]) for g in G.values())}')
    print(f'VALID co-occupancy(2 bots same tile) rounds: '
          f'{sum(int(g["co_occ_rounds"]) for g in G.values())}')
    tot_shots_odd = 0
    inv_bad = inv_n = 0
    for f, rows in R.items():
        for r in rows:
            tot_shots_odd += int(r['shots_odd'])
            inv_n += 1
            if int(r['healers']) > int(r['seat0']) + int(r['fp0']) + \
                    int(r['n_born']):
                inv_bad += 1
    print(f'VALID non-enemy shots on our footprint: {tot_shots_odd}')
    print(f'VALID healers <= seats_at_start(+born): '
          f'{inv_n-inv_bad}/{inv_n} ok, {inv_bad} violations')
    print(f'VALID other: {dict(bad) or "none"}')
    print(f'VALID crashes(total builder Tracebacks): '
          f'{sum(int(g["tot_crash"]) for g in G.values())}, '
          f'TLE builder-turns: {sum(int(g["tot_tled"]) for g in G.values())}')

    # ---------------- window construction ----------------
    strata = collections.defaultdict(list)   # outcome -> list of round dicts
    gstat = collections.defaultdict(list)
    nowin = collections.Counter()
    for f, g in G.items():
        j = J.get(f)
        if j is None:
            continue
        if only_cad and j['opp'] != 'CtrlAltDefeat':
            continue
        oc = outcome(j)
        ws = int(g['win_start'])
        if ws < 0:
            nowin[oc] += 1
            continue
        cd = int(g['core_death'])
        rows = [r for r in R[f] if int(r['rnd']) >= ws]
        if not rows:
            nowin[oc + '_emptywin'] += 1
            continue
        strata[oc].extend(rows)
        gstat[oc].append((f, ws, cd, len(rows)))
    print(f'games with NO turret shot on our core (excluded): {dict(nowin)}')
    for oc in ('LOSS_CORE_DIED', 'TIEBREAK', 'WIN_CORE_KILL'):
        gs = gstat[oc]
        if not gs:
            continue
        L = sorted(x[3] for x in gs)
        ws = sorted(x[1] for x in gs)
        print(f'{oc}: games={len(gs)} siege-rounds={sum(L)} '
              f'median window len={L[len(L)//2]} median start=r{ws[len(ws)//2]}')

    # ---------------- GATE 1 ----------------
    print('\n---- GATE 1: healers / staffed seats per siege round ----')
    for oc in ('LOSS_CORE_DIED', 'TIEBREAK', 'WIN_CORE_KILL'):
        rows = strata[oc]
        if not rows:
            continue
        print(f'[{oc}]')
        show('ACTUAL core healers/round', [int(r['healers']) for r in rows])
        show('STAFFED heal-tiles (ring+fp)',
             [int(r['seat0']) + int(r['fp0']) for r in rows])
        show('STAFFED ring only (8 seats)', [int(r['seat0']) for r in rows])
        dmg = [r for r in rows if int(r['coredmg']) > 0]
        show('healers | core TOOK DAMAGE', [int(r['healers']) for r in dmg])
        show('staffed | core TOOK DAMAGE',
             [int(r['seat0']) + int(r['fp0']) for r in dmg])
        nz = [int(r['healers']) for r in rows if int(r['healers']) > 0]
        print(f'  rounds with >=1 healer: {len(nz)}/{len(rows)} '
              f'({100*len(nz)/len(rows):.1f}%); mean healers WHEN >0 = '
              f'{sum(nz)/max(1,len(nz)):.2f}')
        live = [int(r['live0']) for r in rows]
        print(f'  live builders/round mean={sum(live)/len(live):.2f} '
              f'median={sorted(live)[len(live)//2]}')

    # ---------------- GATE 2 ----------------
    print('\n---- GATE 2: idle builder supply per siege round ----')
    for oc in ('LOSS_CORE_DIED', 'TIEBREAK', 'WIN_CORE_KILL'):
        rows = strata[oc]
        if not rows:
            continue
        print(f'[{oc}]')
        show('IDLE builders/round', [int(r['n_idle']) for r in rows])
        show('(a) idle ON a heal tile', [int(r['ia']) for r in rows])
        show('(a-strict) idle on ring seat', [int(r['ia_s']) for r in rows])
        show('(b) idle 1 step from free tile', [int(r['ib']) for r in rows])
        show('(c) idle 2-3 steps away', [int(r['ic']) for r in rows])
        show('free heal tiles (ring+fp)', [int(r['free_loose']) for r in rows])
        n = len(rows)
        za = sum(1 for r in rows if int(r['ia']) == 0)
        zab = sum(1 for r in rows
                  if int(r['ia']) == 0 and int(r['ib']) == 0)
        zabc = sum(1 for r in rows if int(r['ia']) == 0 and int(r['ib']) == 0
                   and int(r['ic']) == 0)
        zi = sum(1 for r in rows if int(r['n_idle']) == 0)
        print(f'  share of siege-rounds with (a)=0: {100*za/n:.1f}%  '
              f'(a)=(b)=0: {100*zab/n:.1f}%  (a)=(b)=(c)=0: {100*zabc/n:.1f}%  '
              f'no idle builder at all: {100*zi/n:.1f}%')
        dmg = [r for r in rows if int(r['coredmg']) > 0]
        if dmg:
            zad = sum(1 for r in dmg if int(r['ia']) == 0)
            print(f'  on rounds the core TOOK DAMAGE (n={len(dmg)}): '
                  f'(a)=0 in {100*zad/len(dmg):.1f}%; '
                  f'mean (a)={sum(int(r["ia"]) for r in dmg)/len(dmg):.2f} '
                  f'mean (b)={sum(int(r["ib"]) for r in dmg)/len(dmg):.2f} '
                  f'mean idle={sum(int(r["n_idle"]) for r in dmg)/len(dmg):.2f}')
        tl = sum(int(r['n_idle_tled']) for r in rows)
        ti = sum(int(r['n_idle']) for r in rows)
        bi = sum(int(r['n_born_idle']) for r in rows)
        ar = sum(int(r['idle_adj_rm']) for r in rows)
        print(f'  idle builder-turns total={ti}; of which TLE={tl} '
              f'({100*tl/max(1,ti):.2f}%); idle-adjacent-to-own-building-'
              f'removed-this-round (destroy upper bound)={ar} '
              f'({100*ar/max(1,ti):.2f}%); newborn-idle turns={bi}')
        sm = sum(int(r['seat_moved']) for r in rows)
        so = sum(int(r['seat_other']) for r in rows)
        hs = sum(int(r['healers']) for r in rows)
        st = sum(int(r['seat0']) + int(r['fp0']) for r in rows)
        print(f'  SEAT-TURNS in window: {st} builder-turns spent standing on a '
              f'heal-capable tile -> healed core {hs} ({100*hs/max(1,st):.1f}%), '
              f'walked away {sm} ({100*sm/max(1,st):.1f}%), acted on something '
              f'else {so} ({100*so/max(1,st):.1f}%), idle {sum(int(r["ia"]) for r in rows)} '
              f'({100*sum(int(r["ia"]) for r in rows)/max(1,st):.1f}%)')
        dmg_tot = sum(int(r['coredmg']) for r in rows)
        heal_tot = sum(int(r['coreheal']) for r in rows)
        print(f'  CORE LEDGER in window: dmg={dmg_tot} heal={heal_tot} '
              f'ratio={heal_tot/max(1,dmg_tot):.3f}; per round '
              f'dmg={dmg_tot/len(rows):.2f} heal={heal_tot/len(rows):.2f} '
              f'DEFICIT={(dmg_tot-heal_tot)/len(rows):.2f} HP/rd; '
              f'idle-tier(a) could add '
              f'{4*sum(int(r["ia"]) for r in rows)/len(rows):.2f} HP/rd '
              f'= {100*4*sum(int(r["ia"]) for r in rows)/max(1,dmg_tot-heal_tot):.1f}% '
              f'of the deficit')
        act = sum(int(r['n_acted']) for r in rows)
        mov = sum(int(r['n_moved']) for r in rows)
        brr = sum(int(r['live0']) for r in rows)
        print(f'  builder-turn budget in window: {brr} turns = '
              f'{100*act/brr:.1f}% act, {100*mov/brr:.1f}% move, '
              f'{100*ti/brr:.1f}% idle')

    # ---------------- bimodality ----------------
    print('\n---- bimodality probe: healers by phase of the siege window ----')
    for oc in ('LOSS_CORE_DIED', 'TIEBREAK'):
        per = collections.defaultdict(list)
        for f, ws, cd, L in gstat[oc]:
            rows = [r for r in R[f] if int(r['rnd']) >= ws]
            for i, r in enumerate(rows):
                q = min(4, int(5 * i / len(rows)))
                per[q].append(int(r['healers']))
        print(f'[{oc}] mean healers by window quintile: ' +
              '  '.join(f'Q{q+1}={sum(v)/len(v):.2f}' for q, v in
                        sorted(per.items())))
    print('\n---- healers vs incoming damage in the same round ----')
    for oc in ('LOSS_CORE_DIED', 'TIEBREAK', 'WIN_CORE_KILL'):
        rows = strata[oc]
        if not rows:
            continue
        d0 = [int(r['healers']) for r in rows if int(r['coredmg']) == 0]
        d1 = [int(r['healers']) for r in rows if int(r['coredmg']) > 0]
        if d0 and d1:
            print(f'[{oc}] mean healers when core took 0 dmg = '
                  f'{sum(d0)/len(d0):.2f} (n={len(d0)}); when it took dmg = '
                  f'{sum(d1)/len(d1):.2f} (n={len(d1)})')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3] == '1')
