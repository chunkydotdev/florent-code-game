#!/usr/bin/env python3
"""Terminal-phase cut: the last N rounds before our core dies, and the
damage-round ledger.  The core dies to SUSTAINED DPS, so the window average is
the wrong statistic; this is the right one."""
import csv
import sys
import collections

SC = ('/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/'
      '628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/seats')


def outcome(j):
    if j['cond'] == 'core_destroyed':
        return 'LOSS_CORE_DIED' if j['won'] == '0' else 'WIN_CORE_KILL'
    return 'TIEBREAK'


def dist(vals):
    n = len(vals)
    c = collections.Counter(min(v, 13) for v in vals)
    buck = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 5), (6, 8), (9, 12)]
    out = []
    for lo, hi in buck:
        k = sum(c[v] for v in range(lo, hi + 1))
        if k:
            out.append(f'{lo if lo==hi else str(lo)+"-"+str(hi)}:'
                       f'{100*k/n:.1f}%')
    return f'mean={sum(vals)/n:5.2f} med={sorted(vals)[n//2]} | ' + \
        ' '.join(out)


def main(outdir, tag, only_cad):
    J = {r['file']: r for r in csv.DictReader(open(f'{SC}/join_frozen.tsv'),
                                              delimiter='\t')}
    G = {r['file']: r for r in csv.DictReader(open(f'{outdir}/seat_games.tsv'),
                                              delimiter='\t')}
    R = collections.defaultdict(list)
    for r in csv.DictReader(open(f'{outdir}/seat_rounds.tsv'), delimiter='\t'):
        R[r['file']].append(r)
    print(f'==== {tag}: TERMINAL PHASE ====')
    for N in (25, 50, 100):
        acc = collections.defaultdict(list)
        ng = 0
        for f, g in G.items():
            j = J.get(f)
            if j is None or (only_cad and j['opp'] != 'CtrlAltDefeat'):
                continue
            if outcome(j) != 'LOSS_CORE_DIED':
                continue
            cd = int(g['core_death'])
            if cd < 0:
                continue
            rows = [r for r in R[f] if cd - N < int(r['rnd']) <= cd]
            if not rows:
                continue
            ng += 1
            for r in rows:
                for k in ('healers', 'seat0', 'fp0', 'n_idle', 'ia', 'ib',
                          'ic', 'coredmg', 'coreheal', 'live0', 'seat_moved',
                          'seat_other', 'free_loose'):
                    acc[k].append(int(r[k]))
        n = len(acc['healers'])
        print(f'\n-- last {N} rounds before core death: games={ng} rounds={n} --')
        print(f'  healers        {dist(acc["healers"])}')
        print('  staffed(ring+fp) ' +
              dist([a + b for a, b in zip(acc['seat0'], acc['fp0'])]))
        print(f'  live builders  {dist(acc["live0"])}')
        print(f'  IDLE           {dist(acc["n_idle"])}')
        print(f'  (a) idle-on-seat {dist(acc["ia"])}')
        print(f'  (b) idle 1-step  {dist(acc["ib"])}')
        print(f'  (c) idle 2-3     {dist(acc["ic"])}')
        za = sum(1 for v in acc['ia'] if v == 0)
        print(f'  share of terminal rounds with (a)=0: {100*za/n:.1f}%')
        d, hl = sum(acc['coredmg']), sum(acc['coreheal'])
        print(f'  core ledger: dmg={d/n:.2f} HP/rd heal={hl/n:.2f} HP/rd '
              f'deficit={(d-hl)/n:.2f} HP/rd  (ratio {hl/max(1,d):.3f})')
        add = 4 * sum(acc['ia']) / n
        print(f'  tier(a) headroom = {add:.2f} HP/rd = '
              f'{100*add/max(1e-9,(d-hl)/n):.1f}% of the terminal deficit')
        sm = sum(acc['seat_moved']) / n
        print(f'  seat-standers who WALKED AWAY instead: {sm:.2f}/rd '
              f'(= {4*sm:.2f} HP/rd if converted, '
              f'{100*4*sm/max(1e-9,(d-hl)/n):.1f}% of deficit)')

    # damage-round ledger over the whole window
    print('\n==== damage-round ledger (whole siege window) ====')
    for oc in ('LOSS_CORE_DIED', 'TIEBREAK'):
        dd = hh = nn = 0
        ia = ib = idl = hz = 0
        for f, g in G.items():
            j = J.get(f)
            if j is None or (only_cad and j['opp'] != 'CtrlAltDefeat'):
                continue
            if outcome(j) != oc:
                continue
            ws = int(g['win_start'])
            if ws < 0:
                continue
            for r in R[f]:
                if int(r['rnd']) < ws or int(r['coredmg']) == 0:
                    continue
                nn += 1
                dd += int(r['coredmg'])
                hh += int(r['coreheal'])
                ia += int(r['ia'])
                ib += int(r['ib'])
                idl += int(r['n_idle'])
                hz += int(r['healers'])
        if not nn:
            continue
        print(f'[{oc}] damage-rounds n={nn}: dmg={dd/nn:.2f} HP/rd '
              f'heal={hh/nn:.2f} HP/rd deficit={(dd-hh)/nn:.2f} HP/rd; '
              f'healers={hz/nn:.2f}; idle={idl/nn:.2f} '
              f'(a)={ia/nn:.2f} -> {4*ia/nn:.2f} HP/rd = '
              f'{100*4*ia/max(1e-9,dd-hh):.1f}% of deficit')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3] == '1')
