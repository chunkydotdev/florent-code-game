#!/usr/bin/env python3
"""Read the C63 probe tape.  Cells C1-C4 of DESIGN-63 §4.

Row: gid map ord seed turns win C63 team unit round <22 counters>
Counters are CUMULATIVE per unit; one row per unit is its game total.
"""
import glob
import random
import sys
from collections import defaultdict

KEYS = ('nav', 'nav_centre', 'ok', 'ok_prog', 'ok_noprog', 'ref',
        'r_bot', 'r_bot_friend', 'r_bot_enemy', 'r_bot_unk', 'r_bot_and_bld',
        'r_bld', 'r_wall', 'r_other', 'r_other_ore', 'r_oob', 'r_unread',
        'r_exc', 'perp', 'back', 'stuck4', 'osc2')
KEYS2 = KEYS + ('r_bld_belt', 'r_bld_other', 'r_free_mcd', 'r_free_acd')
KEYS3 = KEYS2 + ('r_bld_core', 'r_bld_harv', 'r_bld_barrier', 'r_bld_turret',
                 'r_bld_unk')
PRIMARY = {'midgard', 'ragnarok'}
CONTROL = {'valkyrie', 'glacierkeep'}

rows = []
for f in sys.argv[1:] or glob.glob('c63_rows_w*.tsv'):
    for ln in open(f):
        p = ln.rstrip('\n').split('\t')
        if p[6] != 'C63':
            continue
        if len(p) == 10 + len(KEYS):
            kk = KEYS
        elif len(p) == 10 + len(KEYS2):
            kk = KEYS2
        elif len(p) == 10 + len(KEYS3):
            kk = KEYS3
        else:
            continue
        c = dict.fromkeys(KEYS3, 0)
        c.update(zip(kk, map(int, p[10:])))
        rows.append((p[0], p[1], p[2], p[3], p[4], p[5], p[8], c))

games = defaultdict(list)
for gid, m, o, sd, tn, win, unit, c in rows:
    games[(gid, m, o, sd, tn, win)].append(c)

print("TAPE: %d unit-rows, %d games, maps=%s"
      % (len(rows), len(games), sorted({k[1] for k in games})))

# ---- instrument health: accounting identities -----------------------------
bad = defaultdict(int)
for _, _, _, _, _, _, _, c in rows:
    if c['nav'] != c['ok'] + c['ref']:
        bad['nav != ok+ref'] += 1
    if c['ref'] != (c['r_bot'] + c['r_bld'] + c['r_wall'] + c['r_other']
                    + c['r_oob']):
        bad['ref != sum(reasons)'] += 1
    if c['ref'] != c['perp'] + c['back'] + c['stuck4']:
        bad['ref != perp+back+stuck4'] += 1
    if c['r_bot'] != c['r_bot_friend'] + c['r_bot_enemy'] + c['r_bot_unk']:
        bad['r_bot != friend+enemy'] += 1
    if c['ok'] != c['ok_prog'] + c['ok_noprog']:
        bad['ok != prog+noprog'] += 1
print("ACCOUNTING: %s" % (dict(bad) or "all 5 identities hold on every row"))

wins = sum(1 for k in games if k[5] == 'INSTR')
print("INSTRUMENT-COST CHECK: instrumented tree won %d/%d = %.1f%% of self-play "
      "games (50%% = instrumentation is not costing games)"
      % (wins, len(games), 100.0 * wins / max(1, len(games))))


def agg(sel):
    t = dict.fromkeys(KEYS3, 0)
    n = 0
    for k, cs in games.items():
        if not sel(k):
            continue
        n += 1
        for c in cs:
            for kk in KEYS3:
                t[kk] += c[kk]
    return n, t


def pct(a, b):
    return "n/a" if not b else "%.1f%%" % (100.0 * a / b)


def boot(sel, num, den, iters=4000):
    """Cluster-robust (by GAME) 95% interval for num/den.

    `num` may be a tuple of keys -- the numerator is then their sum, so the
    interval always belongs to the number printed beside it.  (This was a real
    defect in the first draft: the C2 count was r_bld+r_wall while its interval
    was computed on r_bld alone.)
    """
    nums = (num,) if isinstance(num, str) else num
    gs = [(sum(sum(c[n] for n in nums) for c in cs), sum(c[den] for c in cs))
          for k, cs in games.items() if sel(k)]
    gs = [g for g in gs]
    if not gs:
        return "n/a"
    rnd = random.Random(20260815)
    out = []
    for _ in range(iters):
        s = [gs[rnd.randrange(len(gs))] for _ in range(len(gs))]
        a = sum(x for x, _ in s)
        b = sum(y for _, y in s)
        if b:
            out.append(100.0 * a / b)
    out.sort()
    if not out:
        return "n/a"
    return "[%.1f, %.1f]" % (out[int(0.025 * len(out))], out[int(0.975 * len(out))])


def report(label, sel):
    n, t = agg(sel)
    if not n:
        return
    nav, ref = t['nav'], t['ref']
    c1 = t['r_bot']
    c2 = t['r_bld'] + t['r_wall']
    print("\n=== %s  (games=%d, builder-unit-rows pooled)" % (label, n))
    print("  nav rounds (target held, cooldown 0, desired != CENTRE) : %d" % nav)
    print("    desired move SUCCEEDED            : %d (%s of nav)   [prog %s / noprog %s]"
          % (t['ok'], pct(t['ok'], nav), pct(t['ok_prog'], t['ok']),
             pct(t['ok_noprog'], t['ok'])))
    print("    desired move REFUSED              : %d (%s of nav)"
          % (ref, pct(ref, nav)))
    print("  --- classification of the FIRST REFUSED step (denominator = refusals) ---")
    print("    C1  BUILDER BOT on the tile       : %6d  %8s  %s"
          % (c1, pct(c1, ref), boot(sel, 'r_bot', 'ref')))
    print("          ... friendly                : %6d  %8s" % (t['r_bot_friend'], pct(t['r_bot_friend'], ref)))
    print("          ... enemy                   : %6d  %8s" % (t['r_bot_enemy'], pct(t['r_bot_enemy'], ref)))
    print("    C2  BUILDING / WALL on the tile   : %6d  %8s  %s"
          % (c2, pct(c2, ref), boot(sel, ('r_bld', 'r_wall'), 'ref')))
    print("          ... building                : %6d  %8s   [belt %d | core %d harv %d barrier %d turret %d other %d]"
          % (t['r_bld'], pct(t['r_bld'], ref), t['r_bld_belt'], t['r_bld_core'],
             t['r_bld_harv'], t['r_bld_barrier'], t['r_bld_turret'],
             t['r_bld_unk']))
    print("          ... wall                    : %6d  %8s" % (t['r_wall'], pct(t['r_wall'], ref)))
    print("    --  out of bounds                 : %6d  %8s" % (t['r_oob'], pct(t['r_oob'], ref)))
    print("    --  refused, tile reads FREE      : %6d  %8s  (%d on ore; move_cd!=0 in %d, action_cd!=0 in %d)"
          % (t['r_other'], pct(t['r_other'], ref), t['r_other_ore'],
             t['r_free_mcd'], t['r_free_acd']))
    print("  --- outcome of the refused round ---")
    print("    perpendicular succeeded           : %6d  %8s of refusals" % (t['perp'], pct(t['perp'], ref)))
    print("    C3  BACKSTEP succeeded (F3 fires) : %6d  %8s of refusals  %8s of nav  %s"
          % (t['back'], pct(t['back'], ref), pct(t['back'], nav), boot(sel, 'back', 'nav')))
    print("    C4  all four refused (stuck += 1) : %6d  %8s of refusals  %8s of nav  %s"
          % (t['stuck4'], pct(t['stuck4'], ref), pct(t['stuck4'], nav), boot(sel, 'stuck4', 'nav')))
    print("  --- bonus: 2-tile ping-pong (last 4 nav positions span <= 2 tiles) ---")
    print("    osc2 rounds                       : %6d  %8s of nav  %s"
          % (t['osc2'], pct(t['osc2'], nav), boot(sel, 'osc2', 'nav')))
    print("  C1 as a share of ALL nav rounds     : %s  %s"
          % (pct(c1, nav), boot(sel, 'r_bot', 'nav')))


report("POOLED (all 4 maps)", lambda k: True)
report("PRIMARY SEGMENT {midgard, ragnarok}", lambda k: k[1] in PRIMARY)
report("CONTROL SEGMENT {valkyrie, glacierkeep}", lambda k: k[1] in CONTROL)
for m in sorted({k[1] for k in games}):
    report("MAP %s" % m, lambda k, m=m: k[1] == m)
for o in ('A', 'B'):
    report("SEAT %s" % o, lambda k, o=o: k[2] == o)

# ---- per-unit lock profile ------------------------------------------------
print("\n=== PER-UNIT REFUSAL PROFILE (units with >= 20 nav rounds) ===")
for label, sel in (("PRIMARY", lambda m: m in PRIMARY),
                   ("CONTROL", lambda m: m in CONTROL)):
    us = [c for _, m, _, _, _, _, _, c in rows if sel(m) and c['nav'] >= 20]
    if not us:
        continue
    sh = sorted(c['ref'] / c['nav'] for c in us)
    hi = sum(1 for x in sh if x >= 0.5)
    osc = sorted(c['osc2'] / c['nav'] for c in us)
    print("  %s: %d units | refused-share median %.1f%% p90 %.1f%% | %d units (%.1f%%) refused >=50%% of nav rounds"
          % (label, len(us), 100 * sh[len(sh) // 2], 100 * sh[int(0.9 * len(sh))],
             hi, 100.0 * hi / len(us)))
    n5 = sum(1 for c in us if c['stuck4'] >= 5)
    n1 = sum(1 for c in us if c['stuck4'] >= 1)
    print("      F4 escape hatch: %d/%d units (%.1f%%) accumulated >=5 stuck "
          "events over the game (the re-pick threshold); >=1 in %d (%.1f%%)"
          % (n5, len(us), 100.0 * n5 / len(us), n1, 100.0 * n1 / len(us)))
    print("      osc2 share of nav: median %.1f%% p90 %.1f%%"
          % (100 * osc[len(osc) // 2], 100 * osc[int(0.9 * len(osc))]))
