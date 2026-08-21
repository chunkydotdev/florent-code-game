#!/usr/bin/env python3
"""Pooled + per-game autopsy tables from tape30_deaths.decode (read-only)."""
from __future__ import annotations
import sys, json, statistics
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from tape30_deaths import decode, dsq_foot, reach_tiles

D = Path('/Users/junghard/Projects/Work/florent-code-game/scratchpad/s54_fidtape/replays_tape30')
ONLY_S11 = "--all" not in sys.argv
files = sorted(D.glob('*_s11.replay26')) if ONLY_S11 else sorted(D.glob('*.replay26'))

ROLE = ("HOME_KEEPER", "CAGE_WALKER", "ORE_DENIER", "SIEGE_ENGINEER")

games = []
for p in files:
    r = decode(p)
    our, them = r['our'], 1 - r['our']
    ocore, ecore = r['corepos'][our], r['corepos'][them]
    # ---- role assignment by spawn order / lowest free slot (HEURISTIC) ------
    ev = sorted([(rnd, 'b', team, kind, eid, pos)
                 for (rnd, team, kind, eid, pos) in r['births']] +
                [(d['rnd'], 'd', d['team'], d['kind'], d['id'], d['pos'])
                 for d in r['deaths']], key=lambda x: (x[0], x[1] == 'b'))
    holder = [None] * 4
    role_of = {}
    for rnd, tag, team, kind, eid, pos in ev:
        if team != our or kind != 'builder_bot':
            continue
        if tag == 'd':
            for i in range(4):
                if holder[i] == eid:
                    holder[i] = None
        else:
            for i in range(4):
                if holder[i] is None:
                    holder[i] = eid
                    role_of[eid] = i
                    break
            else:
                role_of[eid] = None
    r['role_of'] = role_of
    r['ocore'], r['ecore'] = ocore, ecore
    r['map'] = p.name.rsplit('_', 1)[0]
    games.append(r)

W = sys.stdout.write


def pct(a, b):
    return f"{100.0*a/b:.1f}% ({a}/{b})" if b else "n/a (0/0)"


def med(xs):
    return f"{statistics.median(xs):.0f}" if xs else "-"


# =============== Q1 HARVESTERS ==============================================
harv_deaths, harv_all = [], []
for g in games:
    our = g['our']
    born = {}
    for (rnd, team, kind, eid, pos) in g['births']:
        if team == our and kind == 'harvester':
            born[eid] = (rnd, pos)
    ends = {e.id for e in g['ents'].values() if e.team == our and e.kind == 'harvester'}
    for eid, (b, pos) in born.items():
        harv_all.append((g['map'], eid, b, eid in ends))
    for d in g['deaths']:
        if d['team'] != our or d['kind'] != 'harvester':
            continue
        kp = d['killer_pos']
        harv_deaths.append({
            'map': g['map'], 'rnd': d['rnd'], 'born': d['born'], 'life': d['life'],
            'kk': d['killer_kind'] or 'NONE', 'n_src': d['n_src'],
            'kdsq_ours': dsq_foot(kp, g['ocore']) if kp else None,
            'kdsq_theirs': dsq_foot(kp, g['ecore']) if kp else None,
            'wired': (eid_del := g['harv_delivered'].get(d['id'])) is not None
                     and eid_del <= d['rnd'],
            'emitted': g['harv_emitted'].get(d['id'], 0),
            'dsq_home': dsq_foot(d['pos'], g['ocore']),
            'turrets': d['our_turrets_live'], 'pos': d['pos'],
            'id': d['id'],
        })

W("\n================ Q1  OUR HARVESTER DEATHS ================\n")
W(f"harvesters built (subject): {len(harv_all)}   alive at end: "
  f"{sum(1 for x in harv_all if x[3])}   died: {len(harv_deaths)}\n")
kk = {}
for d in harv_deaths:
    kk[d['kk']] = kk.get(d['kk'], 0) + 1
W("killer class: " + str(kk) + "\n")
lives = [d['life'] for d in harv_deaths]
W(f"lifespan (rounds): median {med(lives)} mean {statistics.mean(lives):.0f} "
  f"min {min(lives)} max {max(lives)}  quartiles "
  f"{sorted(lives)[len(lives)//4]}/{sorted(lives)[len(lives)//2]}/{sorted(lives)[3*len(lives)//4]}\n")
W(f"WIRED at death (had delivered to core): {pct(sum(1 for d in harv_deaths if d['wired']), len(harv_deaths))}\n")
W(f"emitted >=1 stack: {pct(sum(1 for d in harv_deaths if d['emitted']), len(harv_deaths))}\n")
ann = {'ring<=13': 0, 'annulus 14-100': 0, '>100 (their half)': 0, 'peck/adjacent': 0, 'unknown': 0}
for d in harv_deaths:
    if d['kdsq_ours'] is None:
        ann['unknown'] += 1
    elif d['kk'] == 'peck':
        ann['peck/adjacent'] += 1
    elif d['kdsq_ours'] <= 13:
        ann['ring<=13'] += 1
    elif d['kdsq_ours'] <= 100:
        ann['annulus 14-100'] += 1
    else:
        ann['>100 (their half)'] += 1
W("killer STANDING position (d^2 to OUR core): " + str(ann) + "\n")
kd = [d['kdsq_ours'] for d in harv_deaths if d['kdsq_ours'] is not None]
W(f"killer d^2 to our core: median {med(kd)}  range {min(kd)}..{max(kd)}\n")
W(f"harvester death round: median {med([d['rnd'] for d in harv_deaths])}\n")

# =============== Q2 BUILDERS ================================================
W("\n================ Q2  OUR BUILDER-BOT DEATHS ================\n")
bd = []
for g in games:
    our = g['our']
    for d in g['deaths']:
        if d['team'] != our or d['kind'] != 'builder_bot':
            continue
        kp = d['killer_pos']
        bd.append({'map': g['map'], 'rnd': d['rnd'], 'life': d['life'],
                   'role': g['role_of'].get(d['id']),
                   'kk': d['killer_kind'] or 'NONE', 'n_src': d['n_src'],
                   'dsq_our': dsq_foot(d['pos'], g['ocore']),
                   'dsq_their': dsq_foot(d['pos'], g['ecore']),
                   'kdsq_ours': dsq_foot(kp, g['ocore']) if kp else None,
                   'hp': d['hp_at_death'], 'attr': d['attributed'],
                   'hpd': d['hp_delta_round']})
tot_b = sum(1 for g in games for (rnd, t, k, i, p) in g['births']
            if t == g['our'] and k == 'builder_bot')
W(f"builder bots spawned (subject): {tot_b}   died: {len(bd)}   "
  f"alive at end: {tot_b - len(bd)}\n")
kk = {}
for d in bd:
    kk[d['kk']] = kk.get(d['kk'], 0) + 1
W("killer class: " + str(kk) + "\n")
W(f"NON-COMBAT removals (no damage event in death round) = "
  f"{sum(1 for d in bd if d['n_src'] == 0)}   "
  f"** EXCEPTION/self-destruct ALARM CHANNEL **\n")
W(f"died in OUR half: {pct(sum(1 for d in bd if d['dsq_our'] < d['dsq_their']), len(bd))}"
  f"   in THEIR half: {pct(sum(1 for d in bd if d['dsq_our'] >= d['dsq_their']), len(bd))}\n")
W(f"lifespan: median {med([d['life'] for d in bd])}  "
  f"death round median {med([d['rnd'] for d in bd])}\n")
W("\nby inferred role (HEURISTIC: spawn order -> lowest free role slot):\n")
W(f"  {'role':16s} {'deaths':>6s} {'med life':>9s} {'our half':>9s} "
  f"{'gunner':>7s} {'sent':>6s} {'peck':>6s} {'none':>6s}\n")
for i in range(4):
    rs = [d for d in bd if d['role'] == i]
    if not rs:
        W(f"  {ROLE[i]:16s} {0:>6d}\n")
        continue
    W(f"  {ROLE[i]:16s} {len(rs):>6d} {med([d['life'] for d in rs]):>9s} "
      f"{sum(1 for d in rs if d['dsq_our'] < d['dsq_their']):>9d} "
      f"{sum(1 for d in rs if d['kk']=='gunner'):>7d} "
      f"{sum(1 for d in rs if d['kk']=='sentinel'):>6d} "
      f"{sum(1 for d in rs if d['kk']=='peck'):>6d} "
      f"{sum(1 for d in rs if d['kk']=='NONE'):>6d}\n")
unk = [d for d in bd if d['role'] is None]
if unk:
    W(f"  {'(unassigned)':16s} {len(unk):>6d}\n")

# =============== Q3 OUR TURRETS =============================================
W("\n================ Q3  OUR TURRET DEATHS ================\n")
ot = [t for g in games for t in g['our_turrets'].values()]
byk = {}
for t in ot:
    byk.setdefault(t['kind'], []).append(t)
for k, ts in sorted(byk.items()):
    dead = [t for t in ts if t['died'] is not None]
    W(f"  {k:9s} built {len(ts):3d}  died {len(dead):3d} "
      f"({100.0*len(dead)/len(ts):.0f}%)  median life "
      f"{med([t['died']-t['born'] for t in dead])}  killers: "
      f"{ {x: sum(1 for t in dead if t['killer']==x) for x in sorted({t['killer'] or 'NONE' for t in dead})} }\n")
fwd_ours = [t for t in ot if t['dsq_them'] < t['dsq_our']]
W(f"  of ours, FORWARD (nearer their core): {len(fwd_ours)}  died "
  f"{sum(1 for t in fwd_ours if t['died'] is not None)}  median life "
  f"{med([t['died']-t['born'] for t in fwd_ours if t['died'] is not None])}\n")
home_ours = [t for t in ot if t['dsq_our'] <= 13]
W(f"  of ours, HOME RING (d^2<=13 of our core): {len(home_ours)}  died "
  f"{sum(1 for t in home_ours if t['died'] is not None)}\n")
# replant: turret builds per game over time
W(f"  turret builds per game: median "
  f"{med([sum(1 for t in g['our_turrets'].values()) for g in games])}\n")

# =============== Q4 KILL CHAIN ==============================================
W("\n================ Q4  ENEMY KILL-CHAIN TIMELINE (pooled medians) ================\n")
rows = [("enemy builder first enters our half", [g['tl']['enemy_in_our_half'] for g in games]),
        ("enemy plants first FORWARD turret", [g['tl']['first_fwd_turret'] for g in games]),
        ("enemy first shoots one of our HARVESTERS", [g['tl']['first_shot_our_harv'] for g in games]),
        ("enemy first shoots one of our BUILDERS", [g['tl']['first_shot_our_builder'] for g in games]),
        ("our core takes first damage", [g['core_first_dmg'][g['our']] for g in games]),
        ("our core dies", [g['core_dead'][g['our']] for g in games])]
for name, xs in rows:
    ok = [x for x in xs if x is not None]
    W(f"  {name:42s} median r{med(ok):>4s}   n={len(ok)}/{len(games)} games\n")
W(f"\n  game length: median r{med([g['rounds'] for g in games])}   "
  f"our core destroyed in {sum(1 for g in games if g['core_dead'][g['our']] is not None)}/{len(games)}   "
  f"we won {sum(1 for g in games if g['winner']==g['our'])}/{len(games)}\n")
# forward-gunner standing distance when they kill belt pieces
belt_kill_pos = []
for g in games:
    for d in g['deaths']:
        if d['team'] != g['our'] or d['kind'] not in ('conveyor', 'splitter', 'harvester'):
            continue
        if d['killer_pos'] and d['killer_kind'] in ('gunner', 'sentinel'):
            belt_kill_pos.append((d['killer_kind'], dsq_foot(d['killer_pos'], g['ocore'])))
ann = {'<=13 (on our door)': 0, '14-19': 0, '20-100 (ANNULUS)': 0, '>100': 0}
for k, dq in belt_kill_pos:
    if dq <= 13:
        ann['<=13 (on our door)'] += 1
    elif dq < 20:
        ann['14-19'] += 1
    elif dq <= 100:
        ann['20-100 (ANNULUS)'] += 1
    else:
        ann['>100'] += 1
W(f"\n  belt-piece kills by enemy turret fire: n={len(belt_kill_pos)}  "
  f"shooter standing d^2 to OUR core: {ann}\n")
kb = {}
for k, dq in belt_kill_pos:
    kb[k] = kb.get(k, 0) + 1
W(f"  shooter type on belt kills: {kb}\n")

# =============== Q5 COVERAGE OF OUR DEAD BELT TILES =========================
W("\n================ Q5  WERE OUR DEAD BELT TILES COVERED BY OUR OWN TURRETS? ================\n")
cov_ray = cov_rad = no_turret = tot = 0
by_kind = {}
for g in games:
    w, h = g['w'], g['h']
    for d in g['deaths']:
        if d['team'] != g['our'] or d['kind'] not in ('conveyor', 'splitter', 'harvester'):
            continue
        tot += 1
        rec = by_kind.setdefault(d['kind'], [0, 0, 0, 0])
        rec[0] += 1
        ts = d['our_turrets_live']
        if not ts:
            no_turret += 1
            rec[3] += 1
            continue
        ray = set()
        rad = set()
        for (tp, tk, td) in ts:
            ray |= reach_tiles(tp, tk, td, w, h, False)
            rad |= reach_tiles(tp, tk, td, w, h, True)
        if d['pos'] in ray:
            cov_ray += 1
            rec[1] += 1
        if d['pos'] in rad:
            cov_rad += 1
            rec[2] += 1
W(f"  our belt pieces (conveyor/splitter/harvester) destroyed: {tot}\n")
W(f"  NO live turret of ours existed at all at that moment: {pct(no_turret, tot)}\n")
W(f"  inside a live turret's ACTUAL FIRING LINE (facing ray, r^2 13/32): {pct(cov_ray, tot)}\n")
W(f"  inside a live turret's RADIUS on ANY of 8 facings (rotate-if-you-could, loose upper bound): {pct(cov_rad, tot)}\n")
W(f"  {'kind':11s} {'died':>5s} {'ray-cov':>9s} {'any-facing':>11s} {'no turret':>10s}\n")
for k, v in sorted(by_kind.items()):
    W(f"  {k:11s} {v[0]:>5d} {pct(v[1],v[0]):>16s} {pct(v[2],v[0]):>18s} {pct(v[3],v[0]):>17s}\n")

# =============== Q6 FORWARD TURRET ANSWER ===================================
W("\n================ Q6  THE DOOR ANSWER (enemy FORWARD turrets, M7 denominator) ================\n")
W("  [M7 scope = gunner+sentinel only, matching tools/skalman_fidelity.py TURRETS]\n")
ft = [t for g in games for t in g['fwd_turrets'].values()
      if t['kind'] in ('gunner', 'sentinel')]
ftl = [t for g in games for t in g['fwd_turrets'].values() if t['kind'] == 'launcher']
W(f"  (enemy forward LAUNCHERS excluded from M7: {len(ftl)} built, "
  f"{sum(1 for t in ftl if t['died'] is not None)} removed, of which "
  f"{sum(1 for t in ftl if t['died'] is not None and t['killer'] is None)} with NO damage event "
  f"= their own destroy/self-destruct, not our answer)\n")
rem = [t for t in ft if t['died'] is not None]
W(f"  enemy forward turrets built (nearer OUR core than theirs): {len(ft)}\n")
W(f"  removed:   {pct(len(rem), len(ft))}\n")
kk = {}
for t in rem:
    kk[t['killer'] or 'NONE'] = kk.get(t['killer'] or 'NONE', 0) + 1
W(f"  what removed them: {kk}\n")
W(f"  median life of a removed forward turret: {med([t['died']-t['born'] for t in rem])}\n")
unans = [t for t in ft if t['died'] is None]
W(f"  UNANSWERED (alive at game end / our core death): {len(unans)}\n")
W(f"    of the unanswered, EVER inside one of our turrets' firing line: "
  f"{pct(sum(1 for t in unans if t.get('cov_ray_ever')), len(unans))}\n")
W(f"    of the unanswered, EVER inside our turret radius any-facing: "
  f"{pct(sum(1 for t in unans if t.get('cov_rad_ever')), len(unans))}\n")
W(f"    of the unanswered, EVER orthogonally adjacent to one of our builders (peckable): "
  f"{pct(sum(1 for t in unans if t.get('adj_ever')), len(unans))}\n")
d_un = [t['dsq_our'] for t in unans]
d_rm = [t['dsq_our'] for t in rem]
W(f"    d^2 to OUR core: unanswered median {med(d_un)} (range {min(d_un)}..{max(d_un)}) | "
  f"removed median {med(d_rm)} (range {min(d_rm)}..{max(d_rm)})\n")
band = {'<=13 home ring': 0, '14-19': 0, '20-100 ANNULUS': 0, '>100': 0}
for t in unans:
    dq = t['dsq_our']
    if dq <= 13:
        band['<=13 home ring'] += 1
    elif dq < 20:
        band['14-19'] += 1
    elif dq <= 100:
        band['20-100 ANNULUS'] += 1
    else:
        band['>100'] += 1
W(f"    unanswered by band: {band}\n")
bandr = {'<=13 home ring': 0, '14-19': 0, '20-100 ANNULUS': 0, '>100': 0}
for t in rem:
    dq = t['dsq_our']
    if dq <= 13:
        bandr['<=13 home ring'] += 1
    elif dq < 20:
        bandr['14-19'] += 1
    elif dq <= 100:
        bandr['20-100 ANNULUS'] += 1
    else:
        bandr['>100'] += 1
W(f"    removed    by band: {bandr}\n")
kinds = {}
for t in ft:
    kinds.setdefault(t['kind'], [0, 0])
    kinds[t['kind']][0] += 1
    if t['died'] is not None:
        kinds[t['kind']][1] += 1
W(f"    by turret kind (built/removed): { {k: f'{v[1]}/{v[0]}' for k,v in sorted(kinds.items())} }\n")

# =============== PER-GAME TABLE =============================================
W("\n================ PER-GAME SUMMARY ================\n")
W(f"{'map':14s} {'rnds':>5s} {'harv b/d':>9s} {'blt b/d':>8s} {'belt d':>7s} "
  f"{'ourturr b/d':>12s} {'fwdT b/r':>9s} {'1stFwdT':>8s} {'coreDmg':>8s} {'coreDead':>9s}\n")
for g in games:
    our = g['our']
    hb = sum(1 for (r, t, k, i, p) in g['births'] if t == our and k == 'harvester')
    hd = sum(1 for d in g['deaths'] if d['team'] == our and d['kind'] == 'harvester')
    bb = sum(1 for (r, t, k, i, p) in g['births'] if t == our and k == 'builder_bot')
    bdn = sum(1 for d in g['deaths'] if d['team'] == our and d['kind'] == 'builder_bot')
    beltd = sum(1 for d in g['deaths'] if d['team'] == our and d['kind'] in ('conveyor', 'splitter'))
    tb = len(g['our_turrets'])
    td = sum(1 for t in g['our_turrets'].values() if t['died'] is not None)
    fb = len(g['fwd_turrets'])
    fr = sum(1 for t in g['fwd_turrets'].values() if t['died'] is not None)
    W(f"{g['map']:14s} {g['rounds']:>5d} {f'{hb}/{hd}':>9s} {f'{bb}/{bdn}':>8s} "
      f"{beltd:>7d} {f'{tb}/{td}':>12s} {f'{fb}/{fr}':>9s} "
      f"{str(g['tl']['first_fwd_turret']):>8s} "
      f"{str(g['core_first_dmg'][our]):>8s} {str(g['core_dead'][our]):>9s}\n")

# =============== EXTRA: rebuild loops, killer identity, our fire ============
W("\n================ EXTRA  REBUILD LOOPS AND KILLER IDENTITY ================\n")
loops = []
for g in games:
    per_tile = {}
    for d in g['deaths']:
        if d['team'] == g['our'] and d['kind'] in ('harvester', 'conveyor', 'splitter'):
            per_tile.setdefault((d['kind'], d['pos']), []).append(d['rnd'])
    for (k, pos), rs in per_tile.items():
        if len(rs) >= 3:
            loops.append((g['map'], k, pos, len(rs), min(rs), max(rs)))
W(f"  tiles where the SAME kind died >=3 times (rebuild loop): {len(loops)}\n")
for m, k, pos, n, a, b in sorted(loops, key=lambda x: -x[3]):
    W(f"    {m:14s} {k:10s} @{pos}  {n} deaths  r{a}..r{b}\n")
# distinct killers
kill_ids = {}
for g in games:
    for d in g['deaths']:
        if d['team'] != g['our'] or d['kind'] not in ('harvester', 'conveyor', 'splitter'):
            continue
        if d['killer_pos']:
            kill_ids.setdefault((g['map'], d['killer_kind'], d['killer_pos']), 0)
            kill_ids[(g['map'], d['killer_kind'], d['killer_pos'])] += 1
W(f"\n  distinct enemy shooter POSITIONS responsible for all {sum(kill_ids.values())} "
  f"belt/harvester kills: {len(kill_ids)}\n")
for k, v in sorted(kill_ids.items(), key=lambda x: -x[1])[:12]:
    W(f"    {k[0]:14s} {k[1]:9s} @{k[2]}  {v} kills\n")
# our turret fire
W("\n  did our own turrets ever shoot?\n")
ourfire = othem = 0
ourhits = {}
for g in games:
    for (rnd, skind, steam, frm, vid, vkind, vteam, to) in g['damage_log']:
        if skind == 'peck':
            continue
        if steam == g['our']:
            ourfire += 1
            ourhits[vkind] = ourhits.get(vkind, 0) + 1
        elif steam == 1 - g['our']:
            othem += 1
W(f"    turret shots landing on an entity: ours {ourfire}  theirs {othem}\n")
W(f"    what our turret fire hit: {ourhits}\n")
opeck = tpeck = 0
opeck_t = {}
for g in games:
    for (rnd, skind, steam, frm, vid, vkind, vteam, to) in g['damage_log']:
        if skind != 'peck':
            continue
        if steam == g['our']:
            opeck += 1
            opeck_t[vkind] = opeck_t.get(vkind, 0) + 1
        else:
            tpeck += 1
W(f"    builder pecks landing on a building: ours {opeck}  theirs {tpeck}\n")
W(f"    what our pecks hit: {opeck_t}\n")

W("\n================ EXTRA  WHAT KILLS OUR CORE ================\n")
cd = {}
cd_pos = {}
for g in games:
    ocid = g['coreid'][g['our']]
    for (rnd, skind, steam, frm, vid, vkind, vteam, to) in g['damage_log']:
        if vid != ocid:
            continue
        dmg = {'gunner': 7, 'sentinel': 18, 'peck': 2}.get(skind, 0)
        cd[skind] = cd.get(skind, 0) + dmg
        if frm:
            cd_pos.setdefault(skind, []).append(dsq_foot(frm, g['ocore']))
tot = sum(cd.values())
W(f"  total damage landed on OUR core across {len(games)} games: {tot}\n")
for k, v in sorted(cd.items(), key=lambda x: -x[1]):
    ds = cd_pos.get(k, [])
    W(f"    {k:9s} {v:6d} ({100.0*v/tot:.1f}%)  shooter d^2 to our core median "
      f"{med(ds)} range {min(ds) if ds else '-'}..{max(ds) if ds else '-'}\n")

W("\n================ EXTRA  SITING: OUR TURRETS vs OUR DEAD BELT ================\n")
otd = sorted(t['dsq_our'] for g in games for t in g['our_turrets'].values())
bdd = sorted(dsq_foot(d['pos'], g['ocore']) for g in games for d in g['deaths']
             if d['team'] == g['our'] and d['kind'] in ('conveyor', 'splitter', 'harvester'))
W(f"  our turrets built (n={len(otd)}): d^2 to our core {otd}\n")
W(f"  our dead belt tiles (n={len(bdd)}): d^2 to our core median {med(bdd)} "
  f"range {min(bdd)}..{max(bdd)}\n")
W(f"  dead belt tiles at d^2 > 13 (outside our whole home-turret band): "
  f"{pct(sum(1 for x in bdd if x > 13), len(bdd))}\n")

W("\n================ EXTRA  UNANSWERED FORWARD TURRETS by kind x band ================\n")
for kind in ('gunner', 'sentinel'):
    ks = [t for g in games for t in g['fwd_turrets'].values() if t['kind'] == kind]
    un = [t for t in ks if t['died'] is None]
    W(f"  {kind:9s} built {len(ks):3d}  unanswered {len(un):3d}  "
      f"home-ring<=13 {sum(1 for t in un if t['dsq_our']<=13):3d}  "
      f"annulus20-100 {sum(1 for t in un if 20<=t['dsq_our']<=100):3d}\n")

W("\n================ EXTRA  HARVESTER SUPPLY ================\n")
zero = [g['map'] for g in games
        if not any(t == g['our'] and k == 'harvester' for (r, t, k, i, p) in g['births'])]
W(f"  games where we built ZERO harvesters: {pct(len(zero), len(games))} -> {zero}\n")
W(f"  harvesters built per game: "
  f"{[sum(1 for (r,t,k,i,p) in g['births'] if t==g['our'] and k=='harvester') for g in games]}\n")

W("\n================ EXTRA  TIMELINE SPLIT: turret vs launcher ================\n")
for kinds, label in ((('gunner', 'sentinel'), 'first enemy fwd GUNNER/SENTINEL'),
                     (('launcher',), 'first enemy fwd LAUNCHER')):
    xs = []
    for g in games:
        rs = [t['born'] for t in g['fwd_turrets'].values() if t['kind'] in kinds]
        xs.append(min(rs) if rs else None)
    ok = [x for x in xs if x is not None]
    W(f"  {label:34s} median r{med(ok):>4s}  n={len(ok)}/{len(games)}\n")

W(f"\nself-check: attributed damage == summed negative UpdateHp in the death round for "
  f"{sum(g['checked'] for g in games)} deaths, mismatches "
  f"{sum(g['mismatch'] for g in games)}\n")

W("\n================ EXTRA  LAUNCHER THROWS (kidnap / displacement) ================\n")
ours_thrown = theirs_thrown = 0
throw_rounds = []
thrown_died_soon = 0
for g in games:
    dead_at = {d['id']: d['rnd'] for d in g['deaths']}
    for (rnd, bteam, bid, frm, to) in g['throws']:
        if bteam == g['our']:
            ours_thrown += 1
            throw_rounds.append(rnd)
            dr = dead_at.get(bid)
            if dr is not None and dr - rnd <= 10:
                thrown_died_soon += 1
        else:
            theirs_thrown += 1
W(f"  our builders thrown by a launcher: {ours_thrown}   their builders thrown: {theirs_thrown}\n")
W(f"  of ours thrown, died within 10 rounds: {pct(thrown_died_soon, ours_thrown) if ours_thrown else 'n/a'}\n")
W(f"  throw rounds median: {med(throw_rounds)}\n")
per = {}
for g in games:
    per[g['map']] = sum(1 for (r, bt, bid, f, t) in g['throws'] if bt == g['our'])
W(f"  per game: {per}\n")
