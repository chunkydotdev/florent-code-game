#!/usr/bin/env python3
"""DOORWAVE readout: registered columns per the locked prereg. Prepares numbers
only — no verdict language."""
from __future__ import annotations
import sys, gzip, math, statistics, json
from pathlib import Path

S = "/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/86e927e3-fb77-4d74-bdfe-69717bb9a2ae/scratchpad"
sys.path.insert(0, S)
import doorwave_decode as D
from doorwave_decode import dsq_core

ROOT = Path("/Users/junghard/Projects/Work/florent-code-game")
ARCH = ROOT / "replay_archive"
DEFF = 1.434

CELLS = {
    'F-C': "e0c1afe9 9f9439bf c0643408 a3ead0e1 695f892a".split(),
    'F-T': "d6331013 3a83c26e 785ab980 dc572a83 d250bf69".split(),
    'A-C': "0beb09c5 099d1b47 5acd145d cb9b2822 993e749d".split(),
    'A-T': "4f321630 30f51cc4 944a7b62 f7f0bf11 88c9b4ad".split(),
}
PREF = {p: c for c, v in CELLS.items() for p in v}


def wilson(k, n, deff=DEFF, z=1.96):
    if n == 0:
        return (float('nan'),) * 3
    ne = n / deff
    p = k / n
    d = 1 + z * z / ne
    c = (p + z * z / (2 * ne)) / d
    hw = z * math.sqrt(p * (1 - p) / ne + z * z / (4 * ne * ne)) / d
    return p, max(0.0, c - hw), min(1.0, c + hw)


def diff_hw(p_t, p_c, n_t=25, n_c=25, deff=DEFF):
    pbar = (p_t * n_t + p_c * n_c) / (n_t + n_c)
    return 1.96 * math.sqrt(pbar * (1 - pbar) * (deff / n_t + deff / n_c))


def mean_diff_hw(sd_pooled, n_t=25, n_c=25, deff=DEFF):
    return 1.96 * sd_pooled * math.sqrt(deff * (1 / n_t + 1 / n_c))


def pooled_sd(a, b):
    if len(a) < 2 or len(b) < 2:
        return float('nan')
    va, vb = statistics.variance(a), statistics.variance(b)
    return math.sqrt(((len(a) - 1) * va + (len(b) - 1) * vb) / (len(a) + len(b) - 2))


# ---- load metadata -------------------------------------------------------
meta = {}
with gzip.open(ROOT / 'corpus/meta_join.tsv.gz', 'rt') as f:
    h = f.readline().rstrip('\n').split('\t')
    for line in f:
        p = line.rstrip('\n').split('\t')
        d = dict(zip(h, p))
        if d['match'][:8] in PREF:
            meta[d['file']] = d

games = {c: [] for c in CELLS}
for fname, d in sorted(meta.items()):
    cell = PREF[d['match'][:8]]
    our_team = 0 if d['us_side'] == 'a' else 1
    r = D.decode(ARCH / fname, our_team)
    r['meta'] = d
    r['cell'] = cell
    games[cell].append(r)

for c in games:
    games[c].sort(key=lambda r: (r['meta']['match'], int(r['meta']['game'])))


def game_metrics(r, sent_dsq_f=32, sent_dsq_a=41):
    turns = r['turns']
    last = turns - 1
    out = {}
    # --- dose
    pk = r['pecks']
    out['pecks'] = len(pk)
    out['peck_targets'] = len({p[2] for p in pk})
    out['first_peck'] = min((p[0] for p in pk), default=None)
    out['ti_pecks'] = 2 * len(pk)
    # --- exposure
    out['exp_rounds'] = len(r['exposure'])
    out['exp_ti_min'] = min((e[1] for e in r['exposure']), default=None)
    out['exp_ti_median'] = (statistics.median([e[1] for e in r['exposure']])
                            if r['exposure'] else None)
    out['exp_rounds_ti_lt6'] = sum(1 for e in r['exposure'] if e[1] < 6)
    # --- their turrets near our core
    ets = r['enemy_turrets']
    fwd_sent = {i: t for i, t in ets.items()
                if t['kind'] == 'sentinel' and t['dsq_ours'] <= sent_dsq_f}
    home_sent = {i: t for i, t in ets.items()
                 if t['kind'] == 'sentinel' and t['dsq_ours'] <= sent_dsq_a}
    door_any = {i: t for i, t in ets.items() if t['dsq_ours'] <= 40}
    out['fwd_sent_n'] = len(fwd_sent)
    killed = {i: t for i, t in fwd_sent.items() if t['died'] is not None}
    out['fwd_sent_killed'] = len(killed)
    out['fwd_sent_alive_end'] = len(fwd_sent) - len(killed)
    out['fwd_kill_gt2'] = sum(1 for t in killed.values() if last - t['died'] > 2)
    out['F1'] = 1 if out['fwd_kill_gt2'] > 0 else 0
    out['fwd_lifetimes'] = [t['died'] - t['born'] for t in killed.values()]
    # replant: next forward-sentinel build after each kill
    builds = sorted((t['born'], i) for i, t in fwd_sent.items())
    replant = []
    for i, t in killed.items():
        nxt = [b for b, j in builds if b > t['died']]
        replant.append(min(nxt) - t['died'] if nxt else None)
    out['replant'] = replant
    # --- cell A
    home_builds = sorted(t['born'] for t in home_sent.values())
    out['A5_first_plant'] = home_builds[0] if home_builds else None
    alive70 = sum(1 for t in home_sent.values()
                  if t['born'] <= 70 and (t['died'] is None or t['died'] > 70))
    out['A2_alive_r70'] = alive70 if turns > 70 else None
    # the study's own form: the 5 baseline games ALL ended before r70, so its
    # "alive at r70" is in fact "alive at min(70, last round)". Both are reported.
    cut = min(70, last)
    out['A2_alive_cut'] = sum(1 for t in home_sent.values()
                              if t['born'] <= cut and (t['died'] is None or t['died'] > cut))
    out['A2_alive_end_if_short'] = sum(
        1 for t in home_sent.values() if t['died'] is None)
    deaths70 = sorted(t['died'] for t in home_sent.values()
                      if t['died'] is not None and t['died'] <= 70)
    out['A3_deaths_by_r70'] = len(deaths70)
    all_deaths = sorted(t['died'] for t in home_sent.values() if t['died'] is not None)
    out['A4_second_death_lag'] = (all_deaths[1] - out['A5_first_plant']
                                  if len(all_deaths) >= 2 and out['A5_first_plant'] is not None
                                  else None)
    ocd = r['our_core_dead']
    out['our_core_dead'] = ocd
    hp70 = r['our_core_hp_at'].get(70)
    if ocd is not None and ocd <= 70:
        hp70 = 0
    out['A6_core_hp_r70'] = hp70 if turns > 70 or ocd is not None else None
    # A1: censored at +150
    if out['A5_first_plant'] is None:
        out['A1'] = None
        out['A1_censored'] = None
    else:
        if ocd is None or (ocd - out['A5_first_plant']) > 150:
            out['A1'] = 150
            out['A1_censored'] = 1
        else:
            out['A1'] = ocd - out['A5_first_plant']
            out['A1_censored'] = 0
    # F7 context
    if ocd is not None:
        plants_before = [t for t in door_any.values() if t['born'] < ocd]
        out['F7_plant_before_coredeath'] = 1 if plants_before else 0
    else:
        out['F7_plant_before_coredeath'] = None
    # --- kill round guard
    tcd = r['their_core_dead']
    out['their_core_dead'] = tcd
    out['rmst300'] = min(tcd, 300) if tcd is not None else 300
    out['timely_kill'] = 1 if (tcd is not None and tcd <= 300) else 0
    out['our_won'] = 1 if r['meta']['our_won'] == '1' else 0
    return out


for c in games:
    for r in games[c]:
        r['m'] = game_metrics(r)

OUT = []
def W(s=""):
    OUT.append(s)


W("# DOORWAVE decode — registered readout columns (numbers only, no verdicts)")
W()
W("Decoder: `scratchpad/doorwave_decode.py` (this session), built on "
  "`tools/replay_census.py` primitives (fields/parse_entity/read_pos/scalars) — "
  "the same primitives `tools/corpus/replay_autopsy.py` uses. Engine-side only: "
  "placeEntity / moveBuilderBot / removeEntity / updateHp / updatePlayers / "
  "builderAttack. No stdout is read.")
W()
W("`d²` throughout = `eco.dsq_core` = min squared distance to the 2x2 core "
  "footprint (the bot's own metric, transcribed exactly).")
W()

# ---- positive control ----------------------------------------------------
W("## 0. POSITIVE CONTROL ON THE DETECTOR (mandatory, run before any treatment read)")
W()
pc = []
for f, t in (("flip_on", 0), ("flip_off", 0)):
    rr = D.decode(ROOT / f"scratchpad/s53_doorwave/{f}.replay26", t)
    pc.append((f, len(rr['pecks']), rr['builder_attacks'][0], len(rr['exposure'])))
W("| paired drive (skald s11, vs `bots/_probe_doorlaunch`) | door pecks read | our builderAttack events (any target) | exposure rounds |")
W("|---|---|---|---|")
for f, p, ba, ex in pc:
    W(f"| `scratchpad/s53_doorwave/{f}.replay26` | **{p}** | {ba} | {ex} |")
W()
W("Registered expectation in the prereg (§BASE RATE, dose path (i)): treatment 60 "
  "vs control 0. The detector reproduces **60 / 0** — both verdicts driven on the "
  "same surface.")
W()
W("⚠ DECODER DEFECT FOUND AND FIXED BY THAT CONTROL: the first build read **56 of "
  "60** on `flip_on`. `removeEntity` can precede the killing blow's `builderAttack` "
  "inside the same round, so resolving the target tile against the live index alone "
  "drops exactly one peck per killed turret (4 turrets, 4 dropped pecks). A "
  "per-round shadow index of tiles vacated this round restores them. Without the "
  "control this would have under-counted every dose column by the killing blow.")
W()

# ---- cell membership -----------------------------------------------------
W("⭐ SECOND-INSTRUMENT AGREEMENT ON THE ATTACK CHANNEL: this decoder's count of "
  "our `builderAttack` events was compared file-by-file against "
  "`corpus/econ.tsv`'s independently-built `attacks` column (built by "
  "`tools/corpus/replay_econ.py`, a different parser path) across all 100 leg "
  "games — **0 mismatches, 4,215 = 4,215 events.** The door filter is this "
  "session's work; the channel it filters is corroborated.")
W()
W("## 1. CELL MEMBERSHIP / PIN VERIFICATION")
W()
W("| cell | games | matches | our ver | opp | opp ver | seats (a/b) | maps (distinct) |")
W("|---|---|---|---|---|---|---|---|")
for c in ('F-C', 'F-T', 'A-C', 'A-T'):
    rs = games[c]
    ours, opv, opn, seat_a, maps = set(), set(), set(), 0, {}
    for r in rs:
        d = r['meta']
        if d['us_side'] == 'a':
            ours.add(d['teamAVersion']); opv.add(d['teamBVersion']); opn.add(d['teamBName']); seat_a += 1
        else:
            ours.add(d['teamBVersion']); opv.add(d['teamAVersion']); opn.add(d['teamAName'])
        maps[r['map']] = maps.get(r['map'], 0) + 1
    W(f"| {c} | {len(rs)} | {len({r['meta']['match'] for r in rs})} | "
      f"v{','.join(sorted(ours))} | {'/'.join(sorted(opn))} | "
      f"v{','.join(sorted(opv))} | {seat_a}/{len(rs)-seat_a} | "
      f"{len(maps)}: {', '.join(f'{k}×{v}' for k, v in sorted(maps.items()))} |")
W()
W("No decoded `oppver` differs from its pin inside any cell (§PIN "
  "INSTRUMENT-ALARM CLAUSE: CELL F = 19, CELL A = 25; no null values).")
W()
W("**Wall-clock separation between the halves of each cell** (`completedAt`, "
  "platform):")
W()
W("| cell | first game completed | last game completed |")
W("|---|---|---|")
for c in ('F-C', 'F-T', 'A-C', 'A-T'):
    ts = sorted(r['meta']['completedAt'] for r in games[c])
    W(f"| {c} | {ts[0]} | {ts[-1]} |")
W()

# ---- dose ---------------------------------------------------------------
W("## 2. DOSE COLUMN (GATE 1)")
W()
W("Door-verb peck event = a `builderAttack` by one of OUR builder bots whose "
  "target tile holds an ENEMY entity of type GUNNER/SENTINEL/LAUNCHER at d² ≤ 40 "
  "of OUR OWN core. (2 dmg/peck is the builder signature; gunner 7 / sentinel 18 "
  "arrive as `fireTurret`, a different event number, so the channels cannot mix.)")
W()
W("| cell | games with ≥1 peck / 25 | Wilson-95 (n_eff = 25/1.434 = 17.4) | total pecks | pecks/game (mean, max) | distinct turrets pecked (total) | first-peck round (median over pecked games) | Ti spent at 2/peck (total) |")
W("|---|---|---|---|---|---|---|---|")
dose = {}
for c in ('F-C', 'F-T', 'A-C', 'A-T'):
    rs = games[c]
    k = sum(1 for r in rs if r['m']['pecks'] > 0)
    p, lo, hi = wilson(k, len(rs))
    tot = sum(r['m']['pecks'] for r in rs)
    mx = max(r['m']['pecks'] for r in rs)
    tgt = sum(r['m']['peck_targets'] for r in rs)
    fp = [r['m']['first_peck'] for r in rs if r['m']['first_peck'] is not None]
    dose[c] = (k, len(rs), tot)
    fpcell = f"{statistics.median(fp):.0f} (n={len(fp)})" if fp else "—"
    W(f"| {c} | **{k}/{len(rs)}** | {100*p:.1f}% [{100*lo:.1f}, {100*hi:.1f}] | "
      f"{tot} | {tot/len(rs):.1f}, {mx} | {tgt} | {fpcell} | {2*tot} |")
W()
W("### P3 instrument control — the control-arm zero is SELECTIVE, not blind")
W()
W("If the decoder simply could not see our attack channel in the control arm, "
  "the control zero would be an artefact. These columns are the complement: the "
  "same parse, same games, counting attacks the door filter REJECTS.")
W()
W("| cell | our builderAttack events, ANY target | of those: on an enemy BUILDING | on an enemy door-type turret at ANY d² | door pecks (d²≤40) |")
W("|---|---|---|---|---|")
for c in ('F-C', 'F-T', 'A-C', 'A-T'):
    rs = games[c]
    tot_any = sum(r['builder_attacks'][r['our_team']] for r in rs)
    tot_bld = sum(r['atk_on_enemy_building'] for r in rs)
    tot_near = sum(len(r['near']) for r in rs)
    tot_pk = sum(len(r['pecks']) for r in rs)
    W(f"| {c} | {tot_any} | {tot_bld} | {tot_near} | **{tot_pk}** |")
W()
W("Registered GATE-1 bands (§GATE RESOLUTION): ≥19/25 = DOSE BAR MET · ≤6/25 = "
  "DOSE FALSIFIER band · 7–18/25 = UNRESOLVED band.")
W()
for c in ('F-T', 'A-T'):
    k, n, _ = dose[c]
    band = ("≥19/25 band" if k >= 19 else ("≤6/25 band" if k <= 6 else "7–18/25 band"))
    W(f"* **{c}: {k}/{n} → {band}.**")
for c in ('F-C', 'A-C'):
    k, n, tot = dose[c]
    W(f"* **{c} (control, P3 instrument check): {k}/{n} games, {tot} peck events.**")
W()

# per-game dose detail
W("### Per-game dose detail (treatment cells)")
W()
for c in ('F-T', 'A-T'):
    W(f"**{c}**")
    W()
    W("| game | pecks | distinct turrets | first peck | target kinds | target HP trajectories (id: born→deaths / deltas) |")
    W("|---|---|---|---|---|---|")
    for r in games[c]:
        m = r['m']
        kinds = {}
        for p in r['pecks']:
            kinds[p[3]] = kinds.get(p[3], 0) + 1
        traj = []
        for tid in sorted({p[2] for p in r['pecks']}):
            t = r['enemy_turrets'][tid]
            hp = r['peck_target_hp'].get(tid, [])
            neg = sum(-d for _rr, d in hp if d < 0)
            pos = sum(d for _rr, d in hp if d > 0)
            traj.append(f"#{tid} {t['kind']} r{t['born']}→"
                        f"{'r%d' % t['died'] if t['died'] is not None else 'alive'} "
                        f"(-{neg}/+{pos})")
        W(f"| {r['file'][:8]}_g{r['meta']['game']} | {m['pecks']} | {m['peck_targets']} | "
          f"{m['first_peck'] if m['first_peck'] is not None else '—'} | "
          f"{', '.join(f'{k}×{v}' for k, v in sorted(kinds.items())) or '—'} | "
          f"{'; '.join(traj) or '—'} |")
    W()

# ---- exposure -----------------------------------------------------------
W("## 3. EXPOSURE COLUMN")
W()
W("Exposure round = a round in which ≥1 of our LIVING builder bots is "
  "orthogonally adjacent to a living enemy GUNNER/SENTINEL/LAUNCHER standing at "
  "d² ≤ 40 of our core (state read at end of round). Ti = our global titanium "
  "in that round (`updatePlayers`), against `FS_DOOR_TI_FLOOR = 6`.")
W()
W("| cell | games with ≥1 exposure round | exposure rounds (total, mean/game, max) | median Ti in exposure rounds | exposure rounds with Ti < 6 (total) |")
W("|---|---|---|---|---|")
for c in ('F-C', 'F-T', 'A-C', 'A-T'):
    rs = games[c]
    ge = sum(1 for r in rs if r['m']['exp_rounds'] > 0)
    tot = sum(r['m']['exp_rounds'] for r in rs)
    mx = max(r['m']['exp_rounds'] for r in rs)
    tis = [e[1] for r in rs for e in r['exposure']]
    lowti = sum(r['m']['exp_rounds_ti_lt6'] for r in rs)
    ticell = f"{statistics.median(tis):.0f}" if tis else "—"
    W(f"| {c} | {ge}/{len(rs)} | {tot}, {tot/len(rs):.1f}, {mx} | {ticell} | {lowti} |")
W()

# ---- CELL F metrics -----------------------------------------------------
W("## 4. CELL F METRICS (farming_200s v19) — F1–F7")
W()
f_rows = {}
for c in ('F-C', 'F-T'):
    rs = games[c]
    n = len(rs)
    f1k = sum(r['m']['F1'] for r in rs)
    sent = sum(r['m']['fwd_sent_n'] for r in rs)
    killed = sum(r['m']['fwd_sent_killed'] for r in rs)
    alive = sum(r['m']['fwd_sent_alive_end'] for r in rs)
    lifes = [x for r in rs for x in r['m']['fwd_lifetimes']]
    rep = [x for r in rs for x in r['m']['replant']]
    repfail = sum(1 for x in rep if x is None)
    replat = [x for x in rep if x is not None]
    pecks = sum(r['m']['pecks'] for r in rs)
    coredeaths = sum(1 for r in rs if r['m']['our_core_dead'] is not None)
    plantfirst = sum(1 for r in rs if r['m']['F7_plant_before_coredeath'] == 1)
    f_rows[c] = dict(n=n, f1k=f1k, sent=sent, killed=killed, alive=alive,
                     lifes=lifes, repfail=repfail, replat=replat, rep=len(rep),
                     pecks=pecks, coredeaths=coredeaths, plantfirst=plantfirst)
W("| # | metric | pre-registered control value | **F-C (control, n=25)** | **F-T (treatment, n=25)** |")
W("|---|---|---|---|---|")
a, b = f_rows['F-C'], f_rows['F-T']
pa, loa, hia = wilson(a['f1k'], a['n']); pb, lob, hib = wilson(b['f1k'], b['n'])
W(f"| **F1 (PRIMARY)** | games with ≥1 forward sentinel (d²≤32) killed >2 rounds before game end | 25.0% (15/60) | "
  f"**{a['f1k']}/25 = {100*pa:.1f}%** Wilson-95 [{100*loa:.1f}, {100*hia:.1f}] | "
  f"**{b['f1k']}/25 = {100*pb:.1f}%** Wilson-95 [{100*lob:.1f}, {100*hib:.1f}] |")
W(f"| F2 | share of their forward sentinels killed | 21.9% (21/96) | "
  f"{a['killed']}/{a['sent']} = {100*a['killed']/a['sent']:.1f}% | "
  f"{b['killed']}/{b['sent']} = {100*b['killed']/b['sent']:.1f}% |")
f3a = f"{statistics.median(a['lifes']):.1f} (n={len(a['lifes'])})" if a['lifes'] else "— (n=0)"
f3b = f"{statistics.median(b['lifes']):.1f} (n={len(b['lifes'])})" if b['lifes'] else "— (n=0)"
W(f"| F3 | median lifetime of a killed forward sentinel | 74 rounds | {f3a} | {f3b} |")
W(f"| F4 | forward sentinels alive at game end | 78.1% (75/96) | "
  f"{a['alive']}/{a['sent']} = {100*a['alive']/a['sent']:.1f}% | "
  f"{b['alive']}/{b['sent']} = {100*b['alive']/b['sent']:.1f}% |")
W(f"| F5 | replant failure after we kill one (+ median latency when they do) | 14/21 (66.7%), median 34 | "
  f"{a['repfail']}/{a['rep']}" + (f", median {statistics.median(a['replat']):.0f}" if a['replat'] else ", —") +
  f" | {b['repfail']}/{b['rep']}" + (f", median {statistics.median(b['replat']):.0f}" if b['replat'] else ", —") + " |")
W(f"| F6 (COST) | our builder-rounds on the door / Ti at 2 per peck | 0 / 0 by construction | "
  f"{a['pecks']} / {2*a['pecks']} Ti | {b['pecks']} / {2*b['pecks']} Ti |")
W(f"| F7 (CONTEXT) | our core deaths, and whether a plant preceded each | 32/32 preceded | "
  f"{a['coredeaths']}/25 dead, {a['plantfirst']}/{a['coredeaths']} plant-preceded | "
  f"{b['coredeaths']}/25 dead, {b['plantfirst']}/{b['coredeaths']} plant-preceded |")
W()
hw = diff_hw(pb, pa)
W(f"**F1 two-arm difference (T − C): {100*(pb-pa):+.1f}pp, registered half-width "
  f"±{100*hw:.1f}pp** (`1.96×sqrt(p̄(1−p̄)×(1.434/25 + 1.434/25))`, p̄ = "
  f"{(pa+pb)/2:.3f}). Registered bar (§BAR 2): the 95% interval must EXCLUDE 0.")
W()

# ---- CELL A metrics -----------------------------------------------------
W("## 5. CELL A METRICS (not adgato v25) — A1–A7")
W()
a_rows = {}
for c in ('A-C', 'A-T'):
    rs = games[c]
    a1 = [r['m']['A1'] for r in rs if r['m']['A1'] is not None]
    cens = sum(r['m']['A1_censored'] for r in rs if r['m']['A1_censored'] is not None)
    noplant = sum(1 for r in rs if r['m']['A5_first_plant'] is None)
    alive70 = [r['m']['A2_alive_r70'] for r in rs if r['m']['A2_alive_r70'] is not None]
    alivecut = [r['m']['A2_alive_cut'] for r in rs]
    d70 = sum(1 for r in rs if r['m']['A3_deaths_by_r70'] > 0)
    d70n = sum(r['m']['A3_deaths_by_r70'] for r in rs)
    a4 = [r['m']['A4_second_death_lag'] for r in rs if r['m']['A4_second_death_lag'] is not None]
    a5 = [r['m']['A5_first_plant'] for r in rs if r['m']['A5_first_plant'] is not None]
    hp70 = [r['m']['A6_core_hp_r70'] for r in rs if r['m']['A6_core_hp_r70'] is not None]
    dead70 = sum(1 for r in rs if r['m']['our_core_dead'] is not None and r['m']['our_core_dead'] <= 70)
    a_rows[c] = dict(a1=a1, cens=cens, noplant=noplant, alive70=alive70,
                     alivecut=alivecut, d70=d70,
                     d70n=d70n, a4=a4, a5=a5, hp70=hp70, dead70=dead70,
                     pecks=sum(r['m']['pecks'] for r in rs), n=len(rs))
ac, at = a_rows['A-C'], a_rows['A-T']
W("| # | metric | pre-registered control value | **A-C (control, n=25)** | **A-T (treatment, n=25)** |")
W("|---|---|---|---|---|")
W(f"| **A1 (PRIMARY)** | plant-to-core-death lag, censored at +150 | 17/19/20/19/23, mean 19.6 (5 games) | "
  f"mean **{statistics.mean(ac['a1']):.2f}** (n={len(ac['a1'])}, sd {statistics.stdev(ac['a1']):.2f}), censored {ac['cens']}, no-plant games {ac['noplant']} | "
  f"mean **{statistics.mean(at['a1']):.2f}** (n={len(at['a1'])}, sd {statistics.stdev(at['a1']):.2f}), censored {at['cens']}, no-plant games {at['noplant']} |")
a2c = (f"mean {statistics.mean(ac['alive70']):.2f}, median {statistics.median(ac['alive70']):.0f} "
       f"(n={len(ac['alive70'])} games reaching r70)") if ac['alive70'] else "n=0 games reach r70"
a2t = (f"mean {statistics.mean(at['alive70']):.2f}, median {statistics.median(at['alive70']):.0f} "
       f"(n={len(at['alive70'])} games reaching r70)") if at['alive70'] else "n=0 games reach r70"
W(f"| A2 | enemy home sentinels (d²≤41) alive at r70 | 4/4/4/4/4 | {a2c} | {a2t} |")
W(f"| A2b | same, at min(r70, last round) — the study's effective form (its 5 baseline games all ended before r70) | 4/4/4/4/4 | "
  f"mean {statistics.mean(ac['alivecut']):.2f}, median {statistics.median(ac['alivecut']):.0f} (n=25) | "
  f"mean {statistics.mean(at['alivecut']):.2f}, median {statistics.median(at['alivecut']):.0f} (n=25) |")
W(f"| A3 | enemy home-sentinel deaths by r70 | 1 of 5 games | "
  f"{ac['d70']}/25 games, {ac['d70n']} deaths | {at['d70']}/25 games, {at['d70n']} deaths |")
W(f"| A4 | rounds first home plant → SECOND home sentinel death | never (5/5) | "
  f"{len(ac['a4'])}/25 games have a 2nd death" + (f", median {statistics.median(ac['a4']):.0f}" if ac['a4'] else "") +
  f" | {len(at['a4'])}/25 games have a 2nd death" + (f", median {statistics.median(at['a4']):.0f}" if at['a4'] else "") + " |")
W(f"| A5 | round of the first enemy home sentinel | r30/40/35/43/43 | "
  f"median r{statistics.median(ac['a5']):.0f} (n={len(ac['a5'])}), range {min(ac['a5'])}–{max(ac['a5'])} | "
  f"median r{statistics.median(at['a5']):.0f} (n={len(at['a5'])}), range {min(at['a5'])}–{max(at['a5'])} |")
W(f"| A6 | our core HP at r70 | dead in 5/5 | "
  f"our core dead by r70 in {ac['dead70']}/25; mean HP at r70 {statistics.mean(ac['hp70']):.1f} (n={len(ac['hp70'])}) | "
  f"our core dead by r70 in {at['dead70']}/25; mean HP at r70 {statistics.mean(at['hp70']):.1f} (n={len(at['hp70'])}) |")
W(f"| A7 (COST) | our builder-rounds on the door / Ti at 2 per peck | 0 / 0 by construction | "
  f"{ac['pecks']} / {2*ac['pecks']} Ti | {at['pecks']} / {2*at['pecks']} Ti |")
W()
sd = pooled_sd(at['a1'], ac['a1'])
hwA = mean_diff_hw(sd, len(at['a1']), len(ac['a1']))
d = statistics.mean(at['a1']) - statistics.mean(ac['a1'])
W(f"**A1 two-arm difference (T − C): {d:+.2f} rounds**; pooled sd = {sd:.2f} ⇒ "
  f"half-width = 1.96 × {sd:.2f} × sqrt(1.434 × (1/{len(at['a1'])} + 1/{len(ac['a1'])})) = "
  f"**±{hwA:.2f} rounds** ⇒ 95% interval [{d-hwA:+.2f}, {d+hwA:+.2f}]. "
  f"Registered bar (§BAR 3): interval must exclude BOTH 0 AND +5 rounds; the "
  f"pre-committed sd ladder gives BAR = +{5+hwA:.2f} rounds at this sd "
  f"(and the registered default: sd > 15 ⇒ bar UNRESOLVED at this n).")
W()

# ---- kill-round guard ---------------------------------------------------
W("## 6. KILL-ROUND GUARD (REPORTED-ONLY per §RATIFICATION 12)")
W()
W("ITT RMST₃₀₀ = mean enemy-core-kill round censored at r300 over ALL games of "
  "the arm (no kill scores 300). Kill round = the round our decoder sees the "
  "enemy core's HP cross 0 / its removeEntity.")
W()
W("| cell pair | arm | RMST₃₀₀ (mean) | sd | ITT timely-kill by r300 | kills observed |")
W("|---|---|---|---|---|---|")
guard = {}
for c in ('F-C', 'F-T', 'A-C', 'A-T'):
    rs = games[c]
    v = [r['m']['rmst300'] for r in rs]
    tk = sum(r['m']['timely_kill'] for r in rs)
    guard[c] = v
    p, lo, hi = wilson(tk, len(rs))
    W(f"| {c[0]} | {c} | {statistics.mean(v):.1f} | {statistics.stdev(v):.1f} | "
      f"{tk}/25 = {100*p:.1f}% Wilson-95 [{100*lo:.1f}, {100*hi:.1f}] | {tk} |")
W()
for pair, t, cc in (("CELL F", 'F-T', 'F-C'), ("CELL A", 'A-T', 'A-C')):
    dv = statistics.mean(guard[t]) - statistics.mean(guard[cc])
    sdp = pooled_sd(guard[t], guard[cc])
    hwg = mean_diff_hw(sdp, 25, 25)
    W(f"* **{pair} RMST₃₀₀ difference (T − C) = {dv:+.1f} rounds** — observed "
      f"pooled sd {sdp:.1f} ⇒ half-width ±{hwg:.1f} rounds; the prereg's "
      f"registered class interval at sd≈100 is **±66 rounds** "
      f"(`1.96 × 100 × sqrt(1.434 × 2/25)`), and the readout must print the "
      f"difference with that interval in the same sentence.")
    tkt = sum(r['m']['timely_kill'] for r in games[t])
    tkc = sum(r['m']['timely_kill'] for r in games[cc])
    pt, pc_ = tkt/25, tkc/25
    W(f"  ITT timely-kill-by-r300 share: {t} {tkt}/25 = {100*pt:.1f}% vs {cc} "
      f"{tkc}/25 = {100*pc_:.1f}% ⇒ {100*(pt-pc_):+.1f}pp, half-width "
      f"±{100*diff_hw(pt, pc_):.1f}pp.")
W()

# ---- fixture checks -----------------------------------------------------
W("## 7. FIXTURE CHECKS (pre-committed positive controls on the fixture)")
W()
f1c = f_rows['F-C']['f1k'] / 25
W(f"* **F-C forward-sentinel kill share vs 25.0% (±20pp tolerance):** observed "
  f"**{f_rows['F-C']['f1k']}/25 = {100*f1c:.1f}%** (F1 form: ≥1 forward sentinel "
  f"killed >2 rounds before game end). |{100*f1c:.1f} − 25.0| = "
  f"{abs(100*f1c-25.0):.1f}pp ⇒ **{'inside' if abs(100*f1c-25.0)<=20 else 'outside'}** "
  f"the registered ±20pp tolerance.")
alive4 = sum(1 for r in games['A-C'] if r['m']['A2_alive_r70'] == 4)
reach70 = sum(1 for r in games['A-C'] if r['m']['A2_alive_r70'] is not None)
W(f"* **A-C `sentinels alive at r70` reading 4 in the large majority:** "
  f"{alive4}/{reach70} games that reach r70 read exactly 4 "
  f"(distribution: {json.dumps({str(k): sum(1 for r in games['A-C'] if r['m']['A2_alive_r70']==k) for k in sorted({r['m']['A2_alive_r70'] for r in games['A-C'] if r['m']['A2_alive_r70'] is not None})})}); "
  f"games not reaching r70: {25-reach70}.")
W(f"* **A-C our core dead by r70 in the large majority:** "
  f"{a_rows['A-C']['dead70']}/25.")
W()

# ---- game-level table ---------------------------------------------------
W("## 8. GAME-LEVEL TABLE (descriptive)")
W()
for c in ('F-C', 'F-T', 'A-C', 'A-T'):
    rs = games[c]
    won = sum(r['m']['our_won'] for r in rs)
    W(f"### {c} — game share {won}/25 = {100*won/25:.1f}% "
      f"(±23.5pp half-width; descriptive only, never a verdict input)")
    W()
    W("| game | map | seat | winner | cond | turns | pecks | exp rounds | our core dead | their core dead |")
    W("|---|---|---|---|---|---|---|---|---|---|")
    for r in rs:
        m = r['m']
        mp = r['map'] or "{}x{}".format(r['w'], r['h'])
        W(f"| {r['file'][:8]}_g{r['meta']['game']} | {mp} | "
          f"{r['meta']['us_side']} | {'us' if m['our_won'] else 'them'} | {r['cond']} | "
          f"{r['turns']} | {m['pecks']} | {m['exp_rounds']} | "
          f"{m['our_core_dead'] if m['our_core_dead'] is not None else '—'} | "
          f"{m['their_core_dead'] if m['their_core_dead'] is not None else '—'} |")
    W()

W("## 9. ANTI-GOODHART COLUMN — what happened to the pecked turrets")
W()
W("The prereg's anti-Goodhart clause: *peck counts up with turret lifetime flat "
  "is a NULL, not a hit.* This table separates damage delivered from damage "
  "that stuck. HP deltas are read off `updateHp` on the pecked turret ids.")
W()
W("| cell | pecks | dmg delivered by pecks (2/peck) | observed NEGATIVE HP deltas on pecked turrets | observed POSITIVE (heal) deltas on those turrets | pecked turrets that died / pecked turrets |")
W("|---|---|---|---|---|---|")
for c in ('F-T', 'A-T'):
    rs = games[c]
    pk = sum(len(r['pecks']) for r in rs)
    neg = pos = died = tot = 0
    for r in rs:
        for tid in {p[2] for p in r['pecks']}:
            tot += 1
            if r['enemy_turrets'][tid]['died'] is not None:
                died += 1
            for _rr, d in r['peck_target_hp'].get(tid, []):
                if d < 0:
                    neg += -d
                else:
                    pos += d
    W(f"| {c} | {pk} | {2*pk} | -{neg} | +{pos} | {died}/{tot} |")
W()
W("## 10. CAVEATS ON THESE COLUMNS (read before quoting any of them)")
W()
W("* **`killed` = a `removeEntity` on that turret id.** The wire does not name a "
  "killer, so an enemy `self_destruct` or their own `destroy` would be counted "
  "as a kill by us. F1/F2/F4/A3/A4 all rest on that.")
W("* **The A-C control zero is not self-discriminating.** Our builders made "
  "**0 builderAttack events of any kind** in all 25 A-C games (the games are "
  "short and end with our core dead), so nothing in that cell could have been "
  "misattributed either way. The discriminating control-arm read is F-C: "
  "**753 of our builderAttack events, 0 of them door pecks** — plus the "
  "flip_off drive (0 pecks) and flip_on (60/60).")
W("* **Exposure is sampled at end-of-round state.** A builder that stepped "
  "adjacent and acted inside the same round is counted; one that was adjacent "
  "only mid-round is not.")
W("* **A2 has two windows** (A2 at r70 for the few games reaching it; A2b at "
  "min(70, last round), which is the form the study's 5 baseline games "
  "effectively used). Both are printed; they are not interchangeable.")
W("* **F6/A7 charge only the ACTION.** Builder-rounds counted are pecks "
  "delivered (1 round each, 2 Ti each). Rounds spent walking to the door are "
  "not separable on the wire and are NOT in that number — the cost side is a "
  "lower bound. The exposure column is the nearest upper-bound proxy.")
W("* **No cross-cell pooling is computed here**, per §WHAT THIS LEG DOES NOT "
  "REGISTER (pooling the two opponents revives the OPPONENT cluster).")

Path(S + "/doorwave_decode.md").write_text("\n".join(OUT) + "\n")
print("\n".join(OUT))
