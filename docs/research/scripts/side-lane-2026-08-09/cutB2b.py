#!/usr/bin/env python3
"""CUT B part 2, corrected: WORK SEAT vs TRANSIT, with the exposure control.

Fixes over the first pass:
  * band label is 'FWD', not 'FORWARD'
  * core position is not in events.tsv (only core DEATH rows), so it is
    trilaterated per file from (x, y, d2_own) of that team's own builds
  * FIELD_vsUS is classified against THAT team's own buildings, not ours
"""
import csv, collections

DC = '/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/dc/dc_deaths.tsv'
J = {r['file']: r for r in csv.DictReader(open('corpus/join.tsv'), delimiter='\t')}

# ---- trilaterate each team's core NW corner from its own turret builds -------
obs = collections.defaultdict(list)     # (file,team) -> [(x,y,d2_own)]
for r in csv.DictReader(open('corpus/builds.tsv'), delimiter='\t'):
    if r['file'] in J:
        obs[(r['file'], r['team'])].append((int(r['x']), int(r['y']), int(r['d2_own'])))
core = {}
for key, pts in obs.items():
    cands = None
    for x, y, d in pts[:6]:
        s = {(x - dx, y - dy) for dx in range(-30, 31) for dy in range(-30, 31)
             if dx * dx + dy * dy == d}
        cands = s if cands is None else (cands & s)
        if len(cands) == 1:
            break
    if cands and len(cands) == 1:
        core[key] = next(iter(cands))
print(f"core position resolved for {len(core)} of {len(obs)} (file,team) pairs")

# ---- each team's own buildings ---------------------------------------------
bld = collections.defaultdict(lambda: collections.defaultdict(set))  # (file,team)->kind->tiles
for r in csv.DictReader(open('corpus/events.tsv'), delimiter='\t'):
    if r['ev'] != 'BUILD' or r['file'] not in J or r['kind'] == 'builder_bot':
        continue
    bld[(r['file'], r['team'])][r['kind']].add((int(r['x']), int(r['y'])))

N4 = ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1))
WORK = (('HEAL_SEAT', None), ('HARVESTER', 'harvester'),
        ('CONVEYOR', 'conveyor'), ('OUR_TURRET', 'gunner'))


def classify(key, tile):
    lbl = set()
    c = core.get(key)
    if c:
        foot = {(c[0] + a, c[1] + b) for a in (0, 1) for b in (0, 1)}
        if any((tile[0] + dx, tile[1] + dy) in foot for dx, dy in N4):
            lbl.add('HEAL_SEAT')
    o = bld.get(key, {})
    for kinds, name in ((('conveyor', 'splitter'), 'CONVEYOR'),
                        (('harvester',), 'HARVESTER'),
                        (('gunner', 'sentinel', 'launcher', 'barrier'), 'OWN_TURRET')):
        s = set().union(*(o.get(k, set()) for k in kinds)) if o else set()
        if s and any((tile[0] + dx, tile[1] + dy) in s for dx, dy in N4):
            lbl.add(name)
    return lbl


PRIO = ('HEAL_SEAT', 'HARVESTER', 'CONVEYOR', 'OWN_TURRET')


def prio_of(lbl):
    for p in PRIO:
        if p in lbl:
            return p
    return 'TRANSIT'


deaths = collections.defaultdict(collections.Counter)
ndeath = collections.Counter()
for r in csv.DictReader(open(DC), delimiter='\t'):
    j = J.get(r['file'])
    if not j or not r['killer'].startswith('ENEMY'):
        continue
    mine = (r['team'] == j['our_team'])
    key = (r['file'], r['team'])
    if key not in core:
        continue
    who = 'US' if mine else 'FIELD_vsUS'
    grp = (who, r['band'])
    ndeath[grp] += 1
    deaths[grp][prio_of(classify(key, (int(r['x']), int(r['y']))))] += 1

# ---- EXPOSURE CONTROL: the band's own composition ---------------------------
expo = collections.defaultdict(collections.Counter)
for key in core:
    f, team = key
    j = J[f]
    who = 'US' if team == j['our_team'] else 'FIELD_vsUS'
    c = core[key]
    for dx in range(-6, 8):
        for dy in range(-6, 8):
            if dx * dx + dy * dy > 32:
                continue
            expo[who][prio_of(classify(key, (c[0] + dx, c[1] + dy)))] += 1

print("\n=== WORK SEAT vs TRANSIT — deaths, against the band's own composition ===")
print("'lift' = death share / band-tile share. >1 means dying there more than")
print("standing there would predict. This is the number that decides the build.\n")
for who in ('US', 'FIELD_vsUS'):
    e = expo[who]; te = sum(e.values())
    for band in ('HOME', 'FWD'):
        grp = (who, band)
        d = deaths[grp]; n = ndeath[grp]
        if not n:
            continue
        print(f"--- {who} {band}: n={n} enemy-turret deaths "
              f"(band composition from {te} tile-observations) ---")
        print(f"    {'class':<12}{'deaths':>8}{'death%':>9}{'band%':>8}{'lift':>7}")
        for k in PRIO + ('TRANSIT',):
            if not d[k] and not e[k]:
                continue
            ds = d[k] / n * 100
            bs = e[k] / te * 100
            print(f"    {k:<12}{d[k]:>8}{ds:>8.1f}%{bs:>7.1f}%"
                  f"{(ds/bs if bs else float('nan')):>7.2f}")
        print()
