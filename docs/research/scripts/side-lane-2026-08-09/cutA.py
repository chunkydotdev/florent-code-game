#!/usr/bin/env python3
"""CUT A (builder's ASK, kill grain): do TRAIN-derived killer tiles predict
HELD-OUT US home builder deaths?

Grain difference that matters: my earlier work was the PLANT grain (where enemy
turrets get built). This is the KILL grain (which shooter tiles actually kill our
builders). A tile can be planted on often and kill nobody.

Decoder: docs/research/scripts/side-lane-2026-08-09/dc_decode.py (preserved,
validated). 4,897 files, 0 errors.
"""
import csv, collections, statistics, random, sys

random.seed(0)
DC = '/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/dc/dc_deaths.tsv'
J = {r['file']: r for r in csv.DictReader(open('corpus/join.tsv'), delimiter='\t')}

rows = []
seen_files = set()
cls_c = collections.Counter()
for r in csv.DictReader(open(DC), delimiter='\t'):
    j = J.get(r['file'])
    if not j:
        continue
    seen_files.add(r['file'])
    mine = (r['team'] == j['our_team'])
    rows.append((r, j, mine))

print(f"attributed files with death rows: {len(seen_files)}  death rows: {len(rows)}")

# ---- VALIDATION against the published attribution doc before using anything ----
us = [(r, j) for r, j, m in rows if m]
us_home = [(r, j) for r, j in us if r['band'] == 'HOME']
print(f"\nVALIDATION vs builder-death-attribution-2026-08-09.md "
      f"(that doc used 2,735 files; I have {len(seen_files)} attributed here, so")
print("exact equality is NOT expected -- I am checking the SHAPE reproduces.)")
c = collections.Counter(r['cls'] for r, j in us_home)
tot = sum(c.values())
for k, v in c.most_common():
    print(f"   US HOME cls={k:<16} {v:6d}  {v/tot*100:5.2f}%   (doc: gunner 83.22, sentinel 15.64)")

# ---- CUT A ----
# killer tile = (sx, sy) where an ENEMY turret killed one of OUR builders at home
by_cell = collections.defaultdict(list)   # (map,seat) -> [(file, tile, opp)]
for r, j in us_home:
    if r['cls'] not in ('ENEMY_GUNNER', 'ENEMY_SENTINEL', 'ENEMY_MIXED',
                        'gunner', 'sentinel', 'mixed'):
        # accept whatever the label vocabulary actually is; filter on shooter tile
        pass
    if r['sx'] in ('', 'None') or r['sy'] in ('', 'None'):
        continue
    by_cell[(j['map'], j['our_team'])].append(
        (r['file'], (int(r['sx']), int(r['sy'])), j['opp'], r['cls']))

print(f"\nUS HOME deaths with an attributed shooter tile: "
      f"{sum(len(v) for v in by_cell.values())}")

KS = (1, 2, 3, 5, 8, 12)
print("\n=== CUT A: held-out coverage of US home deaths by TRAIN-derived top-k "
      "killer tiles ===")
print("split rule: per (map,seat), sort games by filename, first half = train.")
print("baseline  : k tiles drawn at random from the tiles that EVER kill us in "
      "that cell.\n")
hdr = f"{'map':<12}{'seat':>5}{'trG':>5}{'teG':>4}{'teD':>5}"
for k in KS:
    hdr += f"{'k='+str(k):>13}"
print(hdr)
agg = {k: [] for k in KS}
aggb = {k: [] for k in KS}
for cell in sorted(by_cell, key=lambda c: -len(by_cell[c])):
    recs = by_cell[cell]
    files = sorted({f for f, t, o, c in recs})
    if len(files) < 10 or len(recs) < 40:
        continue
    cut = len(files) // 2
    tr, te = set(files[:cut]), set(files[cut:])
    train = [x for x in recs if x[0] in tr]
    test = [x for x in recs if x[0] in te]
    if len(test) < 15 or not train:
        continue
    cnt = collections.Counter(t for f, t, o, c in train)
    univ = sorted({t for f, t, o, c in recs})
    line = f"{cell[0]:<12}{cell[1]:>5}{len(tr):>5}{len(te):>4}{len(test):>5}"
    for k in KS:
        top = {t for t, _ in cnt.most_common(k)}
        cov = sum(1 for f, t, o, c in test if t in top) / len(test) * 100
        kk = min(k, len(univ))
        base = statistics.mean(
            sum(1 for f, t, o, c in test if t in set(random.sample(univ, kk)))
            / len(test) * 100 for _ in range(300))
        agg[k].append(cov); aggb[k].append(base)
        line += f"{cov:>6.1f}/{base:<6.1f}"
    print(line)
print(f"\n{'MEAN over ' + str(len(agg[1])) + ' cells':<26}", end="")
for k in KS:
    print(f"{statistics.mean(agg[k]):>6.1f}/{statistics.mean(aggb[k]):<6.1f}", end="")
print()
print(f"{'LIFT (pp)':<26}", end="")
for k in KS:
    print(f"{statistics.mean(agg[k]) - statistics.mean(aggb[k]):>+12.1f} ", end="")
print("\n")

# ---- per-opponent split ----
print("=== Is the recurrence field-wide, or only against the three teams that "
      "hurt us most? ===")
print("(same held-out test, restricted to deaths caused while playing that "
      "opponent; k=8)\n")
print(f"{'opponent':<22}{'cells':>6}{'testDeaths':>12}{'k=8 cover':>11}"
      f"{'baseline':>10}{'lift':>8}")
opps = collections.Counter(o for v in by_cell.values() for f, t, o, c in v)
for opp, n in opps.most_common(10):
    covs, bases, cells, td = [], [], 0, 0
    for cell, recs in by_cell.items():
        recs = [x for x in recs if x[2] == opp]
        files = sorted({f for f, t, o, c in recs})
        if len(files) < 8 or len(recs) < 30:
            continue
        cut = len(files) // 2
        tr, te = set(files[:cut]), set(files[cut:])
        train = [x for x in recs if x[0] in tr]
        test = [x for x in recs if x[0] in te]
        if len(test) < 10 or not train:
            continue
        cnt = collections.Counter(t for f, t, o, c in train)
        univ = sorted({t for f, t, o, c in recs})
        top = {t for t, _ in cnt.most_common(8)}
        covs.append(sum(1 for f, t, o, c in test if t in top) / len(test) * 100)
        kk = min(8, len(univ))
        bases.append(statistics.mean(
            sum(1 for f, t, o, c in test if t in set(random.sample(univ, kk)))
            / len(test) * 100 for _ in range(300)))
        cells += 1; td += len(test)
    if cells:
        print(f"{opp:<22}{cells:>6}{td:>12}{statistics.mean(covs):>10.1f}%"
              f"{statistics.mean(bases):>9.1f}%"
              f"{statistics.mean(covs)-statistics.mean(bases):>+8.1f}")
    else:
        print(f"{opp:<22}{'-':>6}{'(n too small)':>12}")
