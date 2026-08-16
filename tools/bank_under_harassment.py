#!/usr/bin/env python3
"""Per-round BANKED TITANIUM vs INCOMING HARASSMENT, decoded from replays.

WHY THIS EXISTS (QUEUE #80 precondition, 2026-08-16)
====================================================
QUEUE #80 proposes a bank-triggered offense surge: when we are sitting on
titanium and the kill has not landed, spend it on kill hardware. The whole idea
presupposes a surplus exists. `docs/research/BELT-TOPOLOGY-CENSUS-2026-08-16.md`
read our median bank at r150 at 44 Ti, which would mean no trigger ever fires.
The counter-hypothesis is that HARASSMENT stalls SPENDING (contested build
sites, cut belts, dead builders) while passive income keeps paying, so harassed
games are exactly where surplus piles up.

⛔ WHY THE CORPUS TAPES CANNOT ANSWER IT AND A DECODER IS REQUIRED.
`corpus/econ.tsv` is the only tape carrying a titanium BALANCE (`ti_end`), and
its grain is `file x team x BAND` with only four bands
(`r0-150 / r150-200 / r200-300 / r300+`, `tools/corpus/replay_econ.py:band`).
That yields the bank at exactly FOUR round boundaries — r150, r200, r300, end —
and **nothing at r50, r100 or r250**. A trajectory cannot be read off it.
Likewise `build_agg.tsv`'s `batk` (builder attacks) is banded, so "harassment by
round t" is not available at any t other than 150/200/300. Both quantities ARE
on the wire per round (`updatePlayers`, Update field 6; `builderAttack`,
Update field 13) — they were simply aggregated away at decode time.

WHAT THIS READS OFF THE WIRE, PER ROUND
---------------------------------------
  updatePlayers  (6)   PlayerState.titanium (1), .titaniumCollected (4),
                       .ammo (7), for BOTH teams -> the bank trajectory.
  builderAttack  (13)  {attacker id, target Pos} -> attacks BY the enemy ON a
                       tile we own = the harassment dose, per round.
  builderBuild   (16)  our build actions per round -> the SPENDING side of the
                       stall hypothesis.
  placeEntity/removeEntity (1/3)  entity census -> live harvesters/conveyors/
                       builder bots per team, and enemy buildings planted in
                       our half.

HARASSMENT IS DEFINED FROM THINGS DONE TO US, NEVER FROM OUR OUTCOMES.
The dose column is `eatk_us` — enemy builderAttack events whose TARGET TILE is
occupied by one of our entities at that moment. Our own losses are NOT used:
"our conveyor died" is confounded by our own `destroy()` (free, uncooldowned,
and `eco.py` uses it for reroutes), and "we lost" is a collider.

OUTPUT: one row per (file, sampled round) while the game is still running.

USAGE
  .venv/bin/python tools/bank_under_harassment.py OUT.tsv --ver 140
  .venv/bin/python tools/bank_under_harassment.py OUT.tsv --files a.replay26 b...
  .venv/bin/python tools/bank_under_harassment.py OUT.tsv --ver 140 --step 10
  .venv/bin/python tools/bank_under_harassment.py --report OUT.tsv 140,152

⚠ USE --step 1 FOR ANY PEAK OR THRESHOLD CLAIM. The bank is spiky: at
`--step 10` the v140 pool reads 6.7% of games ever touching 260 Ti, at
`--step 1` the same pool reads 19.7%. Coarse sampling walks straight past the
spikes, and the answer to "does a trigger ever fire" is exactly a spike
question.
"""
from __future__ import annotations

import csv
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import fields, read_pos, parse_entity, WIRE_LEN, WIRE_VARINT  # noqa: E402

ARCHIVE = Path("replay_archive")
JOIN = Path("corpus/join.tsv")

BELT = ("conveyor", "splitter")
COLS = [
    "file", "our_team", "turns", "rnd",
    # --- bank / income, OUR side and THEIRS ---
    "ti_us", "ti_them", "ticol_us", "ticol_them", "ammo_us",
    # --- harassment DONE TO US, cumulative through this round ---
    "eatk_us",          # enemy builder attacks landing on a tile WE own
    "eatk_us_belt",     # ... of those, on our conveyor/splitter/harvester
    "eatk_us_barrier",  # ... of those, on our barriers (the seal)
    "eatk_us_turret",   # ... of those, on our gunner/sentinel/launcher
    "eatk_us_core",     # ... of those, on our core footprint
    "ebuild_ourhalf",   # enemy buildings placed nearer OUR core than theirs
    "eshots",           # enemy turret shots fired (attributed by shooter tile)
    "obot_deaths",      # OUR builder bots removed (the v140 tree never
                        # self-destructs, so every one of these is done to us)
    # --- what WE did (spending side; NOT part of the harassment definition) ---
    "oatk_them", "obuilds", "ospend_events", "oheals", "oconv_ti", "obots_built",
    # --- live census, our side ---
    "harv_us", "belt_us", "bot_us", "turret_us",
    "harv_them", "bot_them",
]


def _cores(map_buf):
    """[(id, team, (x,y))] from Map.cores (field 4). Cores are NEVER emitted as
    placeEntity — tools/replay_census.py:312."""
    out = []
    for num, wire, value in fields(map_buf):
        if num != 4 or wire != WIRE_LEN:
            continue
        cid = team = 0
        pos = (0, 0)
        for cn, cw, cv in fields(value):
            if cn == 1 and cw == WIRE_VARINT:
                cid = cv
            elif cn == 2 and cw == WIRE_VARINT:
                team = cv
            elif cn == 3 and cw == WIRE_LEN:
                pos = read_pos(cv)
        out.append((cid, team, pos))
    return out


def census(path: Path, our_team: int, step: int, max_round: int):
    data = path.read_bytes()
    map_buf, turn_bufs = None, []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if map_buf is None or not turn_bufs:
        return []
    cores = _cores(map_buf)
    if len(cores) != 2:
        return []
    corepos = {t: p for _i, t, p in cores}
    foot = {t: {(p[0] + dx, p[1] + dy) for dx in (0, 1) for dy in (0, 1)}
            for t, p in corepos.items()}

    them = 1 - our_team

    # id -> (team, kind); pos -> id  (buildings are immovable; bots move)
    # ⛔ BUILDINGS AND BOTS SHARE TILES. A builder bot may stand ON a conveyor
    # (`is_tile_passable`), so ONE pos->id map silently reassigns a belt tile to
    # whichever bot is parked on it, and an enemy attack on that belt resolves to
    # "they attacked a builder bot" — which is not even a legal target.
    # Measured on the first smoke file: 16 of 138 enemy attacks mis-resolved that
    # way, and `eatk_belt` read 0 while the true belt figure was non-zero.
    # builderAttack targets a BUILDING, so it resolves against `bldg_at` only.
    ents: dict[int, tuple[int, str]] = {}
    bldg_at: dict[tuple[int, int], int] = {}
    bot_at: dict[tuple[int, int], int] = {}
    id_pos: dict[int, tuple[int, int]] = {}
    for cid, t, p in cores:
        ents[cid] = (t, "core")
        id_pos[cid] = p
        for f in foot[t]:
            bldg_at[f] = cid

    def d2(a, b):
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

    c = dict.fromkeys(
        ("eatk_us", "eatk_us_belt", "eatk_us_barrier", "eatk_us_turret",
         "eatk_us_core", "ebuild_ourhalf", "eshots", "obot_deaths",
         "oatk_them", "obuilds", "ospend_events", "oheals", "oconv_ti",
         "obots_built"), 0)
    ti = {0: 0, 1: 0}
    ticol = {0: 0, 1: 0}
    ammo = {0: 0, 1: 0}

    rows = []
    turns = len(turn_bufs)
    for rnd, turn_buf in enumerate(turn_bufs):
        for _n, _w, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:                                    # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        if e.id in ents:                         # rotation re-emit
                            continue
                        ents[e.id] = (e.team, e.kind)
                        id_pos[e.id] = e.pos
                        if e.kind == "builder_bot":
                            bot_at[e.pos] = e.id
                        else:
                            bldg_at[e.pos] = e.id
                        if e.team == our_team:
                            if e.kind == "builder_bot":
                                c["obots_built"] += 1
                            else:
                                c["ospend_events"] += 1
                        if e.team == them and e.kind != "builder_bot":
                            if d2(e.pos, corepos[our_team]) < d2(e.pos, corepos[them]):
                                c["ebuild_ourhalf"] += 1
                elif unum == 2:                                  # moveBuilderBot
                    eid = to = None
                    for mn, mw, mv in fields(ubuf):
                        if mn == 1 and mw == WIRE_VARINT:
                            eid = mv
                        elif mn == 2 and mw == WIRE_LEN:
                            to = read_pos(mv)
                    if eid is not None and to is not None:
                        old = id_pos.get(eid)
                        if old is not None and bot_at.get(old) == eid:
                            del bot_at[old]
                        id_pos[eid] = to
                        bot_at[to] = eid
                elif unum == 3:                                  # removeEntity
                    for rn, rw, rv in fields(ubuf):
                        if rw != WIRE_VARINT:
                            continue
                        gone = ents.pop(rv, None)
                        if gone is not None:
                            if gone == (our_team, "builder_bot"):
                                c["obot_deaths"] += 1
                            old = id_pos.pop(rv, None)
                            if old is not None:
                                if bot_at.get(old) == rv:
                                    del bot_at[old]
                                if bldg_at.get(old) == rv:
                                    del bldg_at[old]
                                if gone[1] == "core":
                                    for f in foot[gone[0]]:
                                        if bldg_at.get(f) == rv:
                                            del bldg_at[f]
                elif unum == 13:                                 # builderAttack
                    aid = tgt = None
                    for an, aw, av in fields(ubuf):
                        if an == 1 and aw == WIRE_VARINT:
                            aid = av
                        elif an == 2 and aw == WIRE_LEN:
                            tgt = read_pos(av)
                    ent = ents.get(aid)
                    if ent is None or tgt is None:
                        continue
                    if ent[0] == them:
                        vid = bldg_at.get(tgt)
                        victim = ents.get(vid) if vid is not None else None
                        if victim is not None and victim[0] == our_team:
                            c["eatk_us"] += 1
                            if victim[1] in BELT or victim[1] == "harvester":
                                c["eatk_us_belt"] += 1
                            elif victim[1] == "barrier":
                                c["eatk_us_barrier"] += 1
                            elif victim[1] in ("gunner", "sentinel", "launcher"):
                                c["eatk_us_turret"] += 1
                            elif victim[1] == "core":
                                c["eatk_us_core"] += 1
                    else:
                        c["oatk_them"] += 1
                elif unum == 14:                                 # coreConvertAmmo
                    d = {k: v for k, w2, v in fields(ubuf) if w2 == WIRE_VARINT}
                    if d.get(1, 0) == our_team:
                        c["oconv_ti"] += d.get(2, 0)
                elif unum == 15:                                 # builderHeal
                    aid = None
                    for an, aw, av in fields(ubuf):
                        if an == 1 and aw == WIRE_VARINT:
                            aid = av
                    ent = ents.get(aid)
                    if ent is not None and ent[0] == our_team:
                        c["oheals"] += 1
                elif unum == 12:                                 # fireTurret
                    # FireTurret carries only {from, to} — no id, no team
                    # (replay_econ.py:288). Turrets are immovable buildings, so
                    # the shooter tile resolves the team exactly.
                    frm = None
                    for fn, fw, fv in fields(ubuf):
                        if fn == 1 and fw == WIRE_LEN:
                            frm = read_pos(fv)
                            break
                    if frm is not None:
                        sid = bldg_at.get(frm)
                        sh = ents.get(sid) if sid is not None else None
                        if sh is not None and sh[0] == them:
                            c["eshots"] += 1
                elif unum == 16:                                 # builderBuild
                    aid = None
                    for an, aw, av in fields(ubuf):
                        if an == 1 and aw == WIRE_VARINT:
                            aid = av
                    ent = ents.get(aid)
                    if ent is not None and ent[0] == our_team:
                        c["obuilds"] += 1
                elif unum == 6:                                  # updatePlayers
                    for pn, pw, pv in fields(ubuf):
                        if pn != 1 or pw != WIRE_LEN:
                            continue
                        for tn, tw, tv in fields(pv):
                            if tn not in (1, 2) or tw != WIRE_LEN:
                                continue
                            d = {k: v for k, w2, v in fields(tv) if w2 == WIRE_VARINT}
                            t = tn - 1
                            ti[t] = d.get(1, 0)
                            ticol[t] = d.get(4, 0)
                            ammo[t] = d.get(7, 0)

        if rnd % step == 0 and rnd <= max_round:
            live = {}
            for t, k in ents.values():
                live[(t, k)] = live.get((t, k), 0) + 1
            rows.append([
                path.name, our_team, turns, rnd,
                ti[our_team], ti[them], ticol[our_team], ticol[them], ammo[our_team],
                c["eatk_us"], c["eatk_us_belt"], c["eatk_us_barrier"],
                c["eatk_us_turret"], c["eatk_us_core"], c["ebuild_ourhalf"],
                c["eshots"], c["obot_deaths"],
                c["oatk_them"], c["obuilds"], c["ospend_events"],
                c["oheals"], c["oconv_ti"], c["obots_built"],
                live.get((our_team, "harvester"), 0),
                sum(live.get((our_team, k), 0) for k in BELT),
                live.get((our_team, "builder_bot"), 0),
                sum(live.get((our_team, k), 0) for k in ("gunner", "sentinel", "launcher")),
                live.get((them, "harvester"), 0),
                live.get((them, "builder_bot"), 0),
            ])
    return rows


def _job(args):
    fname, our_team, step, max_round = args
    try:
        return census(ARCHIVE / fname, our_team, step, max_round)
    except Exception as exc:                                     # noqa: BLE001
        print(f"SKIP {fname}: {exc}", file=sys.stderr)
        return []


# ======================================================================
# REPORT MODE — every cell in docs/research/BANK-UNDER-HARASSMENT-2026-08-16.md
# ======================================================================
# The harassment index is built ONLY from things DONE TO US. Nothing
# downstream of the outcome enters the label: no win flag, no game length,
# no count of our own losses that we might have caused ourselves with
# `destroy()`. Win rate and game length are read back out afterwards as
# INSTRUMENT VALIDATION — the index has to track real damage or it is noise —
# and are never used to define a group.

HARASS_COLS = ("eatk_us", "eshots", "obot_deaths", "ebuild_ourhalf")
DEFF_RATED_POOLED = 1.529      # CLAUDE.md: match AND opponent clusters live


def _q(v, p):
    v = sorted(v)
    if not v:
        return float("nan")
    i = (len(v) - 1) * p
    lo = int(i)
    hi = min(lo + 1, len(v) - 1)
    return v[lo] + (v[hi] - v[lo]) * (i - lo)


def _median(v):
    import statistics
    return statistics.median(v) if v else float("nan")


def _load(path):
    import collections
    by = collections.defaultdict(dict)
    with open(path) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            by[r["file"]][int(r["rnd"])] = r
    return by


def _index_at(by, pop, t):
    """z-summed harassment index over games alive at round t."""
    import statistics
    fs = [f for f in pop if t in by[f]]
    if not fs:
        return [], {}
    idx = {f: 0.0 for f in fs}
    for c in HARASS_COLS:
        raw = [int(by[f][t][c]) for f in fs]
        m = statistics.mean(raw)
        sd = statistics.pstdev(raw) or 1.0
        for f, v in zip(fs, raw):
            idx[f] += (v - m) / sd
    return fs, idx


def report(traj, vers, out=sys.stdout):
    import collections
    import hashlib
    import math
    import statistics as st

    J = {r["file"]: r for r in csv.DictReader(open(JOIN), delimiter="\t")}
    by = _load(traj)
    pop = sorted(f for f in by if J.get(f, {}).get("ourver") in vers)
    P = lambda *a: print(*a, file=out)                          # noqa: E731

    P("POPULATION: corpus/join.tsv rows with ourver in %s that have a replay" % (sorted(vers),))
    P("  games %d | matches %d | opponents %d"
      % (len(pop), len({J[f]["match"] for f in pop}), len({J[f]["opp"] for f in pop})))
    P("  CLUSTERS PRESENT: match (5 games each) and opponent — both survive in")
    P("  every cell below, so the pooled rated DEFF %.3f applies." % DEFF_RATED_POOLED)

    P("\n== 1. BANK TRAJECTORY, whole population ==")
    P("%5s %8s %8s %7s %7s %7s %7s %7s" % ("rnd", "n_alive", "mean", "p25", "med", "p75", "p90", "max"))
    for t in (0, 25, 50, 75, 100, 150, 200, 250, 300):
        v = [int(by[f][t]["ti_us"]) for f in pop if t in by[f]]
        if not v:
            continue
        P("%5d %8d %8.1f %7.0f %7.0f %7.0f %7.0f %7d"
          % (t, len(v), st.mean(v), _q(v, .25), _q(v, .5), _q(v, .75), _q(v, .9), max(v)))

    P("\n== 2. TRIGGER FIRE RATE, kill window r21-300 ==")
    P("%7s %22s %20s %22s" % ("T (Ti)", "fires (>=1 round)", "median first rnd", "sustained >=10 rnds"))
    for T in (100, 150, 200, 250, 260, 300, 400, 500, 700, 1000, 1500):
        hits, sust = [], 0
        for f in pop:
            g = by[f]
            first, cur, best = None, 0, 0
            for t in sorted(g):
                if not 21 <= t <= 300:
                    continue
                if int(g[t]["ti_us"]) >= T:
                    if first is None:
                        first = t
                    cur += 1
                    best = max(best, cur)
                else:
                    cur = 0
            if first is not None:
                hits.append(first)
            if best >= 10:
                sust += 1
        P("%7d %13d/%-4d %4.1f%% %20s %14d/%-4d %4.1f%%"
          % (T, len(hits), len(pop), 100 * len(hits) / len(pop),
             ("%.0f" % _median(hits)) if hits else "-", sust, len(pop), 100 * sust / len(pop)))

    P("\n== 3. CONTEMPORANEOUS HARASSMENT SPLIT (index at t, bank at t) ==")
    P("%5s %5s %6s %5s %6s %6s %8s %8s %8s" %
      ("rnd", "n", "grp", "n", "eatk", "shots", "ti med", "ti p75", "ti p90"))
    for t in (50, 100, 150, 200, 250):
        fs, idx = _index_at(by, pop, t)
        if len(fs) < 30:
            continue
        vals = sorted(idx.values())
        c1, c2 = _q(vals, 1 / 3.), _q(vals, 2 / 3.)
        for k, sel in (("LOW", lambda x: x <= c1), ("MID", lambda x: c1 < x < c2),
                       ("HIGH", lambda x: x >= c2)):
            gf = [f for f in fs if sel(idx[f])]
            ti = [int(by[f][t]["ti_us"]) for f in gf]
            P("%5d %5d %6s %5d %6.0f %6.0f %8.0f %8.0f %8.0f"
              % (t, len(fs), k, len(gf),
                 _median([int(by[f][t]["eatk_us"]) for f in gf]),
                 _median([int(by[f][t]["eshots"]) for f in gf]),
                 _median(ti), _q(ti, .75), _q(ti, .9)))

    P("\n== 4. FORWARD-LOOKING: index at r100 -> bank in r101-300 ==")
    P("   The label uses NOTHING after r100, so the bank being scored is strictly")
    P("   in the future of the harassment that is supposed to cause it.")
    fs, idx = _index_at(by, pop, 100)
    vals = sorted(idx.values())
    c1, c2 = _q(vals, 1 / 3.), _q(vals, 2 / 3.)
    grp = {"LOW": [f for f in fs if idx[f] <= c1],
           "HIGH": [f for f in fs if idx[f] >= c2]}
    for k, gf in grp.items():
        pk = [max(int(by[f][t]["ti_us"]) for t in by[f] if 100 < t <= 300)
              for f in gf if any(100 < t <= 300 for t in by[f])]
        P("  %-5s n=%-4d peak bank med %5.0f  p75 %5.0f  p90 %5.0f  max %6d"
          % (k, len(gf), _median(pk), _q(pk, .75), _q(pk, .9), max(pk)))
    for T in (200, 260, 300):
        def ever(gf, T=T):
            return sum(1 for f in gf
                       if any(int(by[f][t]["ti_us"]) >= T for t in by[f] if 100 < t <= 300))
        a = ever(grp["LOW"]) / len(grp["LOW"])
        b = ever(grp["HIGH"]) / len(grp["HIGH"])
        se = math.sqrt(a * (1 - a) / len(grp["LOW"]) + b * (1 - b) / len(grp["HIGH"]))
        se *= math.sqrt(DEFF_RATED_POOLED)
        d = b - a
        P("  ever bank>=%-4d : LOW %5.1f%%  HIGH %5.1f%%  HIGH-LOW %+5.1fpp  95%% CI [%+.1f, %+.1f]pp"
          % (T, 100 * a, 100 * b, 100 * d, 100 * (d - 1.96 * se), 100 * (d + 1.96 * se)))
    P("  ^ read as an EXCLUSION (per CLAUDE.md's DEFF direction clause): the upper")
    P("    bound is how much harassment could possibly RAISE the fire rate.")

    P("\n== 5. WHERE THE INCOME ACTUALLY GOES (r20 -> r150) ==")
    tot = collections.Counter()
    n = 0
    for f in pop:
        g = by[f]
        if 150 not in g or 20 not in g:
            continue
        n += 1
        a, b = g[20], g[150]
        tot["income"] += int(b["ticol_us"]) - int(a["ticol_us"]) + 130 * 2.5
        tot["convert_ammo"] += int(b["oconv_ti"]) - int(a["oconv_ti"])
        tot["heal"] += int(b["oheals"]) - int(a["oheals"])
        tot["attack"] += 2 * (int(b["oatk_them"]) - int(a["oatk_them"]))
        tot["dBank"] += int(b["ti_us"]) - int(a["ti_us"])
    inc = tot["income"] or 1
    P("  n=%d games; income = harvester deliveries + passive 2.5 Ti/rnd = %.0f Ti"
      % (n, inc))
    resid = inc - tot["convert_ammo"] - tot["heal"] - tot["attack"] - tot["dBank"]
    for k in ("convert_ammo", "heal", "attack", "dBank"):
        P("    %-24s %10.0f  %6.1f%% of income" % (k, tot[k], 100 * tot[k] / inc))
    P("    %-24s %10.0f  %6.1f%% of income" % ("residual (builds+spawns)", resid, 100 * resid / inc))

    P("\n== 6. POSITIVE CONTROL — the same instrument on the tiebreak-turtle era ==")
    P("   If it cannot see a fat bank anywhere, a thin reading proves nothing.")
    for v in ("68", "72", "80", "90", "94", "104", "140", "152"):
        gf = [f for f in by if J.get(f, {}).get("ourver") == v]
        if not gf:
            continue
        pk = [max(int(by[f][t]["ti_us"]) for t in by[f] if t >= 21) for f in gf]
        P("   v%-4s n=%-4d med peak %6.0f  p90 %6.0f  max %6d  >=1500 Ti in %5.1f%% of games"
          % (v, len(gf), _median(pk), _q(pk, .9), max(pk),
             100 * sum(1 for x in pk if x >= 1500) / len(gf)))

    P("\n== 7. NEGATIVE CONTROL — md5(file) parity split, same statistics ==")
    for lbl in (0, 1):
        gf = [f for f in fs if int(hashlib.md5(f.encode()).hexdigest(), 16) % 2 == lbl]
        pk = [max(int(by[f][t]["ti_us"]) for t in by[f] if 100 < t <= 300)
              for f in gf if any(100 < t <= 300 for t in by[f])]
        e = sum(1 for f in gf
                if any(int(by[f][t]["ti_us"]) >= 260 for t in by[f] if 100 < t <= 300))
        P("   arm%d n=%-4d peak bank med %5.0f  p90 %5.0f  ever>=260 %5.1f%%"
          % (lbl, len(gf), _median(pk), _q(pk, .9), 100 * e / len(gf)))

    P("\n== 8. INSTRUMENT DISCRIMINATION — does the index track real damage? ==")
    P("   (read AFTER the split; never used to build it)")
    P("   %-5s %5s %9s %9s %11s %8s %9s" %
      ("grp", "n", "belt@150", "harv@150", "turret@150", "medlen", "win rate"))
    for k, gf in grp.items():
        def m(c, t):
            v = [int(by[f][t][c]) for f in gf if t in by[f]]
            return _median(v)
        wr = 100 * st.mean([1 if J[f]["won"] in ("1", "True", "true") else 0 for f in gf])
        P("   %-5s %5d %9.0f %9.0f %11.0f %8.0f %8.1f%%"
          % (k, len(gf), m("belt_us", 150), m("harv_us", 150), m("turret_us", 150),
             _median([int(by[f][0]["turns"]) for f in gf]), wr))


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        # A probe must never be an action: --help used to fall through to
        # `out_path = argv[0]` and run the full decode into a file named
        # "--help" (caught by test_instruments 2026-08-16).
        print(__doc__)
        raise SystemExit(0 if argv else 2)
    if argv[0] == "--report":
        traj = argv[1]
        vers = set(argv[2].split(",")) if len(argv) > 2 else {"140", "152"}
        report(traj, vers)
        return
    out_path = argv[0]
    if out_path.startswith("-"):
        raise SystemExit(f"first argument must be the output path, got flag-like {out_path!r}")
    ver = None
    step = 10
    max_round = 400
    files = None
    it = iter(argv[1:])
    for a in it:
        if a == "--ver":
            ver = next(it)
        elif a == "--step":
            step = int(next(it))
        elif a == "--max-round":
            max_round = int(next(it))
        elif a == "--files":
            files = list(it)
    jobs = []
    if files:
        J = {r["file"]: r for r in csv.DictReader(open(JOIN), delimiter="\t")}
        for f in files:
            jobs.append((f, int(J[f]["our_team"]), step, max_round))
    else:
        for r in csv.DictReader(open(JOIN), delimiter="\t"):
            if ver is not None and r["ourver"] != ver:
                continue
            if not (ARCHIVE / r["file"]).exists():
                continue
            jobs.append((r["file"], int(r["our_team"]), step, max_round))
    print(f"{len(jobs)} replays", file=sys.stderr)
    with open(out_path, "w") as out:
        out.write("\t".join(COLS) + "\n")
        with ProcessPoolExecutor(max_workers=max(1, (os.cpu_count() or 4) - 1)) as ex:
            for rows in ex.map(_job, jobs, chunksize=4):
                for row in rows:
                    out.write("\t".join(str(v) for v in row) + "\n")
    print("wrote " + out_path, file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
