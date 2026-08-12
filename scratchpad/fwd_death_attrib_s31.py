#!/usr/bin/env python3
"""FORWARD BUILDER DEATH ATTRIBUTION — what accounts for the 3.47x hazard gap?

Commissioned s31 (2026-08-11).  The anchor being explained
(docs/research/QUEUE-forward-efficiency-2026-08-11.md):

    forward builder deaths per 1,000 forward builder-rounds
        US  2.92   TOP 0.84   ratio 3.47x

and docs/research/FORWARD-HAZARD-geometry-2026-08-11.md prices tile exposure at
1.53x, leaving ~2.3x unaccounted.

READ-ONLY.  Decodes replay_archive/*.replay26 + corpus/meta_join.tsv.  Writes
nothing but stdout (and, with --dump, a TSV of death rows into scratchpad/).

DEFINITIONS (inherited verbatim from scratchpad/dwell.py / fwd_deaths.py)
  * a builder-round is FORWARD when d2(bot, enemy_core) < d2(bot, own_core).
    ⭐ COUNTED ON A ROUND-START CLOCK (the tile and the transit state the bot
    holds when the round begins), NOT dwell.py's post-move clock.  Reason, found
    in the pilot: turret fire can resolve before a bot's own move, so a bot that
    moves every round but is shot first emits no move that round.  On dwell.py's
    clock that bot is TRANSIT in the denominator and STATION in the numerator,
    which manufactures the entire transit-vs-station result.  dwell.py's total is
    still computed and printed as `fwd_rounds_end` so the two conventions can be
    compared; they differ only by spawn/death boundary rounds.
  * cores are map.cores, position = NW corner of the 2x2 footprint.
  * a death is a removeEntity carrying the id of a live builder bot.  Band and
    forward/home are taken from the victim's ROUND-START tile.

POPULATIONS (corpus-howto TRAP 7: side keyed on teamAId/teamBId, never us_side)
  US  = meta_join rows where either team id is ours; measured side = ours.
  TOP = meta_join rows with NEITHER side us and at least one side among the nine
        >=1900 teams; measured side(s) = the TOP one(s).  A TOP-vs-TOP game
        contributes TWO measured sides, and every numerator AND denominator in
        this script is summed over exactly the same side-set.
  VSUS = (context only, always labelled) our opponents' sides in OUR games, i.e.
        builders killed BY US.  Reported separately, never pooled into TOP.

ATTRIBUTION (method reused from docs/research/builder-death-attribution-2026-08-09.md)
  * damage ground truth = the UpdateHp ledger (Update field 5; delta is a 64-bit
    two's-complement varint -- corpus-howto TRAP 2).
  * "who" = FireTurret (field 12); shooter = the turret standing on `from` at
    ROUND START (the S1 ordering trap: FireTurret can be emitted after the
    victim's removeEntity in the same round).
  * FOR A DEATH, a shot counts against the victim when its `to` is any tile the
    victim held during the round (round-start tile plus every move destination).
    Validated by the HP ledger: attributed damage must equal death-round HP loss.
  * FOR THE NON-FATAL SHOT CENSUS that rule over-counts (a shot at the tile a bot
    LEFT this round is credited to it), so the census uses the documented
    round-start-occupancy rule instead and is reconciled against the HP ledger.
  * gunner 7 dmg, sentinel 18 dmg, launcher 0.  Friendly fire kept and labelled.
  * builder attacks are counted but CANNOT kill a bot (engine damage-target law:
    a builder attack hits the BUILDING on the tile) -- reported as a control.

TRANSIT vs STATION (the hypothesis that decides the launcher-delivery plank)
  Every forward builder-round is bucketed by `since_move` = rounds since that
  bot last emitted a MoveBuilderBot, evaluated AT ROUND START (so 1 = moved on
  the previous round; NEVER = has not moved since spawn).  Deaths are bucketed
  on the same clock, so hazard per 1,000
  builder-rounds is computed WITHIN each transit state -- numerator and
  denominator over the same side-set and the same state.
  Long moves (d2 > 2) are launcher throws; a throw is a move on the wire and is
  counted separately.

Usage:
    .venv/bin/python scratchpad/fwd_death_attrib_s31.py [--limit N] [--procs P] [--dump]
"""
from __future__ import annotations

import argparse
import csv
import math
import os
import sys
from collections import Counter, defaultdict
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
sys.path.insert(0, "tools")
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa: E402

AR = Path("replay_archive")
OURS = "379a5d80-9921-4c9e-949b-f9b1dcba16be"
TOP_TEAMS = {
    "sporks", "Clankers", "Jython", "Lorem Ipsum", "not adgato",
    "Erebus", "The Flotte Experience", "Pantheon", "O(1)",
}
DOCTRINE = [(0, 59), (60, 179), (180, 249), (250, 499), (500, 999)]
NB = len(DOCTRINE)
TURRETS = {"gunner", "sentinel", "launcher"}
DMG = {"gunner": 7, "sentinel": 18, "launcher": 0}
GUN_R2, SENT_R2 = 13, 32

# transit-state buckets, by rounds since this bot last moved
SM_LABELS = ["moved last rnd", "2 rnds ago", "3-9", "10-29", "30+", "NEVER moved"]
NSM = len(SM_LABELS)


def sm_bucket(since):
    """`since` is measured at ROUND START, so it is >= 1 for any bot that has moved."""
    if since < 0:
        return 5
    if since <= 1:
        return 0
    if since == 2:
        return 1
    if since <= 9:
        return 2
    if since <= 29:
        return 3
    return 4


def band_of(rnd):
    for i, (lo, hi) in enumerate(DOCTRINE):
        if lo <= rnd <= hi:
            return i
    return NB - 1


def s64(v):
    return v - (1 << 64) if v >= (1 << 63) else v


# ---------------------------------------------------------------------------
def new_side():
    return {
        "fwd_rounds": 0, "home_rounds": 0,
        "fwd_rounds_end": 0,            # dwell.py convention (post-move), anchor cross-check
        "fwd_rounds_band": [0] * NB,
        "fwd_sm": [0] * NSM,            # forward builder-rounds by transit state
        "fwd_sa": [0] * NSM,            # forward builder-rounds by "rounds since acted"
        "home_sm": [0] * NSM,
        "fwd_depth_sum": 0.0,           # sum of sqrt(d2 enemy core)/core-dist
        "fwd_dmg": 0,                   # HP lost by builders standing forward (ledger)
        "home_dmg": 0,
        "fwd_heal": 0,                  # HP gained by builders standing forward
        "fwd_shots_gun": 0,             # round-start-occupancy shot census
        "fwd_shots_sent": 0,
        "fwd_shot_dmg": 0,              # implied damage of that census (recon check)
        "fwd_gun_inrange": 0,           # sum over fwd builder-rounds of enemy gunners d2<=13
        "fwd_sent_inrange": 0,          # ... enemy sentinels d2<=32
        "fwd_gun_alive": 0,             # ... enemy gunners alive anywhere
        "fwd_sent_alive": 0,
        "fwd_t3": 0, "fwd_t10": 0,      # forward rounds with since_move <= 3 / <= 10
        "fwd_dmg_band": [0] * NB,
        "fwd_alive_band": [0] * NB,     # enemy turrets alive, summed over fwd rounds, by band
        "fwd_inrange_band": [0] * NB,   # enemy turrets in range, summed over fwd rounds, by band
        "deaths": [],
        "games": 0, "rounds": 0,
    }


def merge_side(a, b):
    for k, v in b.items():
        if k == "deaths":
            a[k].extend(v)
        elif isinstance(v, list):
            for i in range(len(v)):
                a[k][i] += v[i]
        else:
            a[k] += v


DEATH_COLS = [
    "fwd", "band", "rnd", "cause", "n_shooters", "n_shots", "gun_shots",
    "sent_shots", "ff_shots", "dmg_round", "hp_start", "max_hp", "age",
    "since_move", "sm_bucket", "since_act", "thrown_ever", "d2_enemy",
    "depth_norm", "batk_on_tile", "healed_ever", "n_enemy_bots_adj",
    "rounds_since_first_dmg", "n_dmg_rounds", "gun_inrange", "sent_inrange",
]
C = {k: i for i, k in enumerate(DEATH_COLS)}


# ---------------------------------------------------------------------------
def walk(path, sides):
    data = path.read_bytes()
    mapbuf = None
    turns = []
    for n, w, v in fields(data):
        if n == 1 and w == WIRE_LEN:
            mapbuf = v
        elif n == 3 and w == WIRE_LEN:
            turns.append(v)
    if mapbuf is None:
        return None
    cores = []
    for n, w, v in fields(mapbuf):
        if n == 4 and w == WIRE_LEN:
            d = {a: b for a, _c, b in fields(v)}
            cores.append((d.get(2, 0), read_pos(d[3])))
    home = {}
    for t, c in cores:
        home.setdefault(t, c)
    if 0 not in home or 1 not in home:
        return None
    cc = math.dist(home[0], home[1]) or 1.0

    def d2(a, b):
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

    out = {s: new_side() for s in sides}
    measured = set(sides)

    bot_pos, bot_team, bot_hp, bot_max = {}, {}, {}, {}
    bot_spawn, bot_lastmove, bot_lastact = {}, {}, {}
    bot_thrown, bot_healed = {}, {}
    bot_firstdmg, bot_ndmg = {}, {}
    turret_at = {}        # pos -> (kind, team)
    turret_pos = {}       # id -> pos

    for rnd, tb in enumerate(turns):
        start_pos = dict(bot_pos)
        start_hp = dict(bot_hp)
        start_turret = dict(turret_at)
        start_lastmove = dict(bot_lastmove)
        start_lastact = dict(bot_lastact)
        # enemy turret positions AT ROUND START, per team
        enemy_gun = {0: [], 1: []}
        enemy_sent = {0: [], 1: []}
        for _p, (_kd, _tm) in start_turret.items():
            if _kd == "gunner":
                enemy_gun[1 - _tm].append(_p)
            elif _kd == "sentinel":
                enemy_sent[1 - _tm].append(_p)
        # ---- EXPOSURE, ON THE ROUND-START CLOCK ----------------------------
        # Counted here (not after the update block) so that the numerator and the
        # denominator of every hazard below share one clock.  A bot that moves every
        # round but is shot before its move would otherwise be counted as TRANSIT in
        # the denominator and as STATION in the numerator.
        for bi, p in start_pos.items():
            t = bot_team.get(bi)
            if t not in measured:
                continue
            o = out[t]
            lm = start_lastmove.get(bi, -1)
            smb = sm_bucket(-1 if lm < 0 else rnd - lm)
            if d2(p, home[1 - t]) < d2(p, home[t]):
                o["fwd_rounds"] += 1
                o["fwd_rounds_band"][band_of(rnd)] += 1
                o["fwd_depth_sum"] += math.sqrt(d2(p, home[1 - t])) / cc
                o["fwd_sm"][smb] += 1
                _sv = -1 if lm < 0 else rnd - lm
                if 0 <= _sv <= 3:
                    o["fwd_t3"] += 1
                if 0 <= _sv <= 10:
                    o["fwd_t10"] += 1
                la = start_lastact.get(bi, -1)
                o["fwd_sa"][sm_bucket(-1 if la < 0 else rnd - la)] += 1
                ng = ns = 0
                for q in enemy_gun[t]:
                    if d2(q, p) <= GUN_R2:
                        ng += 1
                for q in enemy_sent[t]:
                    if d2(q, p) <= SENT_R2:
                        ns += 1
                o["fwd_gun_inrange"] += ng
                o["fwd_sent_inrange"] += ns
                o["fwd_gun_alive"] += len(enemy_gun[t])
                o["fwd_sent_alive"] += len(enemy_sent[t])
                _bb = band_of(rnd)
                o["fwd_alive_band"][_bb] += len(enemy_gun[t]) + len(enemy_sent[t])
                o["fwd_inrange_band"][_bb] += ng + ns
            else:
                o["home_rounds"] += 1
                o["home_sm"][smb] += 1
        # round-start occupancy, for the documented shot-resolution rule
        start_bot_at = defaultdict(list)
        for i, p in start_pos.items():
            start_bot_at[p].append(i)
        held = defaultdict(list)
        for i, p in start_pos.items():
            held[i].append(p)
        shots = []
        batks = []
        dmg = Counter()
        heal = Counter()
        removed = []
        moved_this = set()

        for _a, _b, ub in fields(tb):
            for un, _w, ubuf in fields(ub):
                if un == 1:                                   # placeEntity
                    for en, _e, eb in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(eb, rnd)
                        if e is None:
                            continue
                        if e.kind == "builder_bot":
                            if e.id not in bot_pos:
                                bot_spawn[e.id] = rnd
                                bot_lastmove[e.id] = -1
                                bot_lastact[e.id] = -1
                                bot_thrown[e.id] = 0
                                bot_healed[e.id] = 0
                                bot_firstdmg[e.id] = -1
                                bot_ndmg[e.id] = 0
                                held[e.id].append(e.pos)
                            bot_pos[e.id] = e.pos
                            bot_team[e.id] = e.team
                            bot_hp[e.id] = e.hp
                            bot_max[e.id] = e.max_hp or 40
                        elif e.kind in TURRETS:
                            old = turret_pos.get(e.id)
                            if old is not None and old != e.pos:
                                turret_at.pop(old, None)
                            turret_pos[e.id] = e.pos
                            turret_at[e.pos] = (e.kind, e.team)
                elif un == 2:                                 # moveBuilderBot
                    d = {k: v for k, _x, v in fields(ubuf)}
                    if 1 in d and 2 in d and d[1] in bot_pos:
                        bid = d[1]
                        to = read_pos(d[2])
                        if d2(bot_pos[bid], to) > 2:
                            bot_thrown[bid] = bot_thrown.get(bid, 0) + 1
                        bot_pos[bid] = to
                        held[bid].append(to)
                        bot_lastmove[bid] = rnd
                        moved_this.add(bid)
                elif un == 3:                                 # removeEntity
                    for _rn, _rw, rv in fields(ubuf):
                        if rv in bot_pos:
                            removed.append(rv)
                        p = turret_pos.pop(rv, None)
                        if p is not None:
                            turret_at.pop(p, None)
                elif un == 5:                                 # updateHp
                    d = {k: v for k, _x, v in fields(ubuf)}
                    if 1 in d:
                        i = d[1]
                        if i in bot_pos:
                            delta = s64(d.get(2, 0))
                            if delta < 0:
                                dmg[i] -= delta
                            else:
                                heal[i] += delta
                            bot_hp[i] = bot_hp.get(i, 0) + delta
                elif un == 12:                                # fireTurret
                    d = {k: v for k, _x, v in fields(ubuf)}
                    if 1 in d and 2 in d:
                        shots.append((read_pos(d[1]), read_pos(d[2])))
                elif un in (13, 15, 16):                      # builder attack/heal/build
                    d = {k: v for k, _x, v in fields(ubuf)}
                    if 1 in d:
                        bot_lastact[d[1]] = rnd
                    if un == 13 and 1 in d and 2 in d:
                        batks.append((read_pos(d[2]), bot_team.get(d[1])))
                    if un == 15 and 2 in d:
                        tp = read_pos(d[2])
                        for bi in start_bot_at.get(tp, ()):
                            bot_healed[bi] = bot_healed.get(bi, 0) + 1

        # ---- non-fatal shot census: documented ROUND-START occupancy rule ----
        for frm, to in shots:
            sk = start_turret.get(frm)
            if sk is None:
                continue
            kindk, _steam = sk
            if kindk == "launcher":
                continue
            occ = start_bot_at.get(to)
            if not occ or len(occ) != 1:
                continue
            bi = occ[0]
            t = bot_team.get(bi)
            if t not in measured:
                continue
            sp = start_pos[bi]
            if d2(sp, home[1 - t]) < d2(sp, home[t]):
                o = out[t]
                if kindk == "gunner":
                    o["fwd_shots_gun"] += 1
                else:
                    o["fwd_shots_sent"] += 1
                o["fwd_shot_dmg"] += DMG[kindk]

        # ---- ledger damage / heal, by band of the ROUND-START tile -----------
        for bi, v in dmg.items():
            t = bot_team.get(bi)
            if t not in measured:
                continue
            sp = start_pos.get(bi)
            if sp is None:
                continue
            if d2(sp, home[1 - t]) < d2(sp, home[t]):
                out[t]["fwd_dmg"] += v
                out[t]["fwd_dmg_band"][band_of(rnd)] += v
            else:
                out[t]["home_dmg"] += v
        for bi, v in heal.items():
            t = bot_team.get(bi)
            if t not in measured:
                continue
            sp = start_pos.get(bi)
            if sp is not None and d2(sp, home[1 - t]) < d2(sp, home[t]):
                out[t]["fwd_heal"] += v

        # ---- deaths ----------------------------------------------------------
        for vid in removed:
            t = bot_team.get(vid)
            if t not in measured:
                for dct in (bot_pos, bot_hp, bot_team):
                    dct.pop(vid, None)
                continue
            sp = start_pos.get(vid, bot_pos.get(vid))
            if sp is None:
                for dct in (bot_pos, bot_hp, bot_team):
                    dct.pop(vid, None)
                continue
            fwd = 1 if d2(sp, home[1 - t]) < d2(sp, home[t]) else 0
            tiles = set(held.get(vid, [sp]))
            shooters = set()
            gs = ss = ffs = adm = 0
            for frm, to in shots:
                if to not in tiles:
                    continue
                sk = start_turret.get(frm)
                if sk is None:
                    continue
                kindk, steam = sk
                if kindk == "launcher":
                    continue
                shooters.add(frm)
                if kindk == "gunner":
                    gs += 1
                else:
                    ss += 1
                if steam == t:
                    ffs += 1
                adm += DMG[kindk]
            dr = dmg.get(vid, 0)
            nsh = gs + ss
            if nsh == 0 and dr == 0:
                cause = "NO_DAMAGE"
            elif nsh == 0:
                cause = "DMG_UNATTRIB"
            elif adm == dr:
                cause = "EXACT"
            elif adm > dr:
                cause = "OVER"
            else:
                cause = "PARTIAL"
            batk_on = sum(1 for p, bt in batks if p in tiles and bt != t)
            nadj = 0
            for bi, bp in start_pos.items():
                if bot_team.get(bi) != t and d2(bp, sp) <= 2:
                    nadj += 1
            de = d2(sp, home[1 - t])
            lm = start_lastmove.get(vid, -1)          # ROUND-START clock, see above
            since_m = -1 if lm < 0 else rnd - lm
            la = start_lastact.get(vid, -1)
            since_a = -1 if la < 0 else rnd - la
            fd = bot_firstdmg.get(vid, -1)
            gir = sum(1 for p in enemy_gun[t] if d2(p, sp) <= GUN_R2)
            sir = sum(1 for p in enemy_sent[t] if d2(p, sp) <= SENT_R2)
            out[t]["deaths"].append((
                fwd, band_of(rnd), rnd, cause, len(shooters), nsh, gs, ss, ffs,
                dr, start_hp.get(vid, bot_hp.get(vid, 0)), bot_max.get(vid, 40),
                rnd - bot_spawn.get(vid, rnd), since_m, sm_bucket(since_m),
                since_a, bot_thrown.get(vid, 0), de, math.sqrt(de) / cc,
                batk_on, bot_healed.get(vid, 0), nadj,
                -1 if fd < 0 else rnd - fd, bot_ndmg.get(vid, 0), gir, sir,
            ))
            for dct in (bot_pos, bot_hp, bot_team):
                dct.pop(vid, None)

        for bi in dmg:
            if bi in bot_pos:
                if bot_firstdmg.get(bi, -1) < 0:
                    bot_firstdmg[bi] = rnd
                bot_ndmg[bi] = bot_ndmg.get(bi, 0) + 1

        # ---- dwell.py-convention exposure (post-move), anchor cross-check only
        for bi, p in bot_pos.items():
            t = bot_team.get(bi)
            if t in measured and d2(p, home[1 - t]) < d2(p, home[t]):
                out[t]["fwd_rounds_end"] += 1

    for s in sides:
        out[s]["games"] = 1
        out[s]["rounds"] = len(turns)
    return out


def worker(arg):
    fn, sides = arg
    try:
        r = walk(AR / fn, sides)
    except Exception as exc:                                   # noqa: BLE001
        return ("ERR", fn, f"{type(exc).__name__}: {exc}")
    if r is None:
        return ("SKIP", fn, "no map/cores")
    return ("OK", fn, r)


# ---------------------------------------------------------------------------
def select():
    rows = list(csv.DictReader(open("corpus/meta_join.tsv"), delimiter="\t"))
    us, top, vsus, us_vtop, top_vtop, top_voth = [], [], [], [], [], []
    for r in rows:
        a_us = r["teamAId"] == OURS
        b_us = r["teamBId"] == OURS
        if a_us or b_us:
            us.append((r["file"], (0 if a_us else 1,)))
            vsus.append((r["file"], (1 if a_us else 0,)))
            oppname = r["teamBName"] if a_us else r["teamAName"]
            if oppname in TOP_TEAMS:
                us_vtop.append((r["file"], (0 if a_us else 1,)))
        else:
            sides = []
            if r["teamAName"] in TOP_TEAMS:
                sides.append(0)
            if r["teamBName"] in TOP_TEAMS:
                sides.append(1)
            if sides:
                top.append((r["file"], tuple(sides)))
                if len(sides) == 2:
                    top_vtop.append((r["file"], (0, 1)))
                else:
                    top_voth.append((r["file"], tuple(sides)))
    keep = lambda L: [x for x in L if (AR / x[0]).exists()]     # noqa: E731
    return (keep(us), keep(top), keep(vsus),
            keep(us_vtop), keep(top_vtop), keep(top_voth))


def run_group(sel, procs, limit=None):
    items = sel if limit is None else sel[:limit]
    agg = new_side()
    errs = Counter()
    skips = 0
    nfiles = 0
    nsides = 0
    with Pool(processes=procs) as pool:
        for tag, fn, payload in pool.imap_unordered(worker, items, chunksize=16):
            if tag == "ERR":
                errs[payload] += 1
                continue
            if tag == "SKIP":
                skips += 1
                continue
            nfiles += 1
            for _s, rec in payload.items():
                nsides += 1
                merge_side(agg, rec)
    return agg, errs, skips, nfiles, nsides


def rate(n, d, per=1000):
    return float("nan") if d == 0 else per * n / d


def rr(a, b):
    return float("nan") if not b or b != b else a / b


def pct(n, d):
    return float("nan") if d == 0 else 100.0 * n / d


def fwd(g):
    return [d for d in g["deaths"] if d[0] == 1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--procs", type=int, default=min(8, os.cpu_count() or 4))
    ap.add_argument("--dump", action="store_true")
    args = ap.parse_args()

    us_sel, top_sel, vsus_sel, usvt_sel, tvt_sel, tvo_sel = select()
    W = 108
    print("=" * W)
    print("POPULATION (corpus/meta_join.tsv; side keyed on teamAId/teamBId, NOT us_side -- TRAP 7)")
    print(f"  US   games with replay on disk : {len(us_sel):,}")
    print(f"  TOP  third-party games on disk : {len(top_sel):,}"
          f"   (TOP on BOTH sides: {sum(1 for x in top_sel if len(x[1]) == 2):,}"
          f" -> two measured sides each)")
    print(f"  VSUS our opponents' sides      : {len(vsus_sel):,}  (context only, never pooled into TOP)")
    print("=" * W)

    groups = {}
    for label, sel in (("US", us_sel), ("TOP", top_sel), ("VSUS", vsus_sel),
                       ("US_vTOP", usvt_sel), ("TOP_vTOP", tvt_sel), ("TOP_vOTH", tvo_sel)):
        agg, errs, skips, nf, ns = run_group(sel, args.procs, args.limit)
        groups[label] = agg
        print(f"  decoded {label:<5} files={nf:,} sides={ns:,} skipped={skips} "
              f"PARSE FAILURES={sum(errs.values())} {dict(errs) if errs else ''}")
        sys.stdout.flush()

    US, TOP, VSUS = groups["US"], groups["TOP"], groups["VSUS"]
    ALL = (("US", US), ("TOP", TOP), ("VSUS", VSUS))

    # ---------------- CONTROL 1 -------------------------------------------
    print()
    print("=" * W)
    print("CONTROL 1 -- REPRODUCE THE ANCHOR (forward builder deaths per 1,000 forward builder-rounds)")
    print("  target: US 2.92, TOP 0.84, ratio 3.47x  (QUEUE-forward-efficiency-2026-08-11.md)")
    print("=" * W)
    print(f"  {'band':<10}{'US deaths':>11}{'US fwd-rnds':>14}{'US rate':>10}"
          f"{'TOP deaths':>12}{'TOP fwd-rnds':>15}{'TOP rate':>10}{'US/TOP':>9}")
    for b, (lo, hi) in enumerate(DOCTRINE):
        ud = sum(1 for d in US["deaths"] if d[0] == 1 and d[1] == b)
        td = sum(1 for d in TOP["deaths"] if d[0] == 1 and d[1] == b)
        ur = rate(ud, US["fwd_rounds_band"][b])
        tr = rate(td, TOP["fwd_rounds_band"][b])
        print(f"  r{lo}-{hi:<6}{ud:>11,}{US['fwd_rounds_band'][b]:>14,}{ur:>10.2f}"
              f"{td:>12,}{TOP['fwd_rounds_band'][b]:>15,}{tr:>10.2f}{rr(ur, tr):>8.2f}x")
    udf, tdf, vdf = len(fwd(US)), len(fwd(TOP)), len(fwd(VSUS))
    UR = rate(udf, US["fwd_rounds"])
    TR = rate(tdf, TOP["fwd_rounds"])
    print(f"  {'POOLED':<10}{udf:>11,}{US['fwd_rounds']:>14,}{UR:>10.2f}"
          f"{tdf:>12,}{TOP['fwd_rounds']:>15,}{TR:>10.2f}{rr(UR, TR):>8.2f}x")
    print(f"  [context] VSUS (our opponents, killed BY US): {vdf:,} fwd deaths / "
          f"{VSUS['fwd_rounds']:,} fwd-rounds = {rate(vdf, VSUS['fwd_rounds']):.2f}/1k -- NOT part of TOP")
    print(f"  ==> REPRODUCTION: US {UR:.2f} (doc 2.92)  TOP {TR:.2f} (doc 0.84)  "
          f"ratio {rr(UR, TR):.2f}x (doc 3.47x)")

    # ---------------- CONTROL 2 -------------------------------------------
    print()
    print("=" * W)
    print("CONTROL 2 -- ATTRIBUTION COMPLETENESS (share of FORWARD deaths by cause class)")
    print("  EXACT = attributed shot damage equals death-round HP loss from the ledger")
    print("=" * W)
    causes = ["EXACT", "OVER", "PARTIAL", "DMG_UNATTRIB", "NO_DAMAGE"]
    print(f"  {'group':<6}{'n fwd deaths':>14}" + "".join(f"{c:>15}" for c in causes)
          + f"{'UNATTRIB':>11}")
    for lab, g in ALL:
        ds = fwd(g)
        cnt = Counter(d[3] for d in ds)
        una = cnt["DMG_UNATTRIB"] + cnt["NO_DAMAGE"]
        print(f"  {lab:<6}{len(ds):>14,}"
              + "".join(f"{pct(cnt[c], len(ds)):>14.2f}%" for c in causes)
              + f"{pct(una, len(ds)):>10.2f}%")
    print("  RECONCILIATION of the NON-FATAL shot census (round-start-occupancy rule) "
          "against the HP ledger:")
    for lab, g in ALL:
        print(f"    {lab:<5} census implies {g['fwd_shot_dmg']:,} dmg vs ledger "
              f"{g['fwd_dmg']:,}  = {pct(g['fwd_shot_dmg'], g['fwd_dmg']):.1f}% "
              f"(shortfall = shots on tiles a bot moved onto mid-round; census is a LOWER BOUND)")

    # ---------------- H1 ---------------------------------------------------
    print()
    print("=" * W)
    print("H1 -- WHAT KILLS THEM (forward deaths carrying >=1 attributed shot)")
    print("=" * W)
    hdr = (f"  {'group':<6}{'n':>9}{'gunner-only':>13}{'sentinel-only':>15}{'mixed':>9}"
           f"{'friendly-fire':>15}{'dmg/death':>11}{'shots/death':>13}")

    def mixrow(lab, ds):
        go = sum(1 for d in ds if d[6] > 0 and d[7] == 0)
        so = sum(1 for d in ds if d[7] > 0 and d[6] == 0)
        mx = sum(1 for d in ds if d[6] > 0 and d[7] > 0)
        ff = sum(1 for d in ds if d[8] > 0)
        n = max(len(ds), 1)
        print(f"  {lab:<6}{len(ds):>9,}{pct(go, len(ds)):>12.2f}%{pct(so, len(ds)):>14.2f}%"
              f"{pct(mx, len(ds)):>8.2f}%{pct(ff, len(ds)):>14.2f}%"
              f"{sum(d[9] for d in ds)/n:>11.2f}{sum(d[5] for d in ds)/n:>13.2f}")
    print(hdr)
    for lab, g in ALL:
        mixrow(lab, [d for d in g["deaths"] if d[0] == 1 and d[5] > 0])
    print("  CONTROL 3 -- SAME INSTRUMENT ON *HOME* DEATHS. Must come out different; if it")
    print("               returns the forward numbers it is not measuring shooter type at all.")
    print(hdr)
    for lab, g in ALL:
        mixrow(lab, [d for d in g["deaths"] if d[0] == 0 and d[5] > 0])
    print("  CONTROL 3b -- builder melee (enemy BuilderAttack on the victim's tile, death round):")
    for lab, g in ALL:
        ds = fwd(g)
        n = sum(1 for d in ds if d[19] > 0)
        print(f"    {lab:<5} {n:,}/{len(ds):,} = {pct(n, len(ds)):.2f}%  "
              f"(engine damage-target law: a builder attack hits the BUILDING, never the bot)")
    print("  NON-FATAL shot census, forward, per 1,000 forward builder-rounds "
          "(round-start occupancy, LOWER BOUND):")
    for lab, g in ALL:
        print(f"    {lab:<5} gunner {rate(g['fwd_shots_gun'], g['fwd_rounds']):>6.2f}   "
              f"sentinel {rate(g['fwd_shots_sent'], g['fwd_rounds']):>6.2f}   "
              f"total {rate(g['fwd_shots_gun']+g['fwd_shots_sent'], g['fwd_rounds']):>6.2f}")

    # ---------------- THE DECOMPOSITION ------------------------------------
    print()
    print("=" * W)
    print("DECOMPOSITION -- deaths/round = (damage taken/round) x (deaths/damage taken)")
    print("  damage from the UpdateHp ledger, attributed to the band of the victim's ROUND-START tile")
    print("=" * W)
    print(f"  {'group':<6}{'fwd dmg':>12}{'fwd-rnds':>13}{'dmg/1k rnds':>14}"
          f"{'fwd deaths':>12}{'dmg/death':>11}{'heal fwd':>11}{'heal/dmg':>10}")
    for lab, g in ALL:
        n = max(len([d for d in g["deaths"] if d[0] == 1]), 1)
        print(f"  {lab:<6}{g['fwd_dmg']:>12,}{g['fwd_rounds']:>13,}"
              f"{rate(g['fwd_dmg'], g['fwd_rounds']):>14.2f}{n:>12,}"
              f"{g['fwd_dmg']/n:>11.2f}{g['fwd_heal']:>11,}"
              f"{pct(g['fwd_heal'], g['fwd_dmg']):>9.1f}%")
    dr_u = rate(US["fwd_dmg"], US["fwd_rounds"])
    dr_t = rate(TOP["fwd_dmg"], TOP["fwd_rounds"])
    dd_u = US["fwd_dmg"] / max(udf, 1)
    dd_t = TOP["fwd_dmg"] / max(tdf, 1)
    print(f"  ==> TERM 1  damage-taken per forward round, US/TOP = {rr(dr_u, dr_t):.2f}x")
    print(f"  ==> TERM 2  damage absorbed per death,      TOP/US = {rr(dd_t, dd_u):.2f}x")
    print(f"  ==> product = {rr(dr_u, dr_t)*rr(dd_t, dd_u):.2f}x   "
          f"(identity: must equal the {rr(UR, TR):.2f}x anchor)")
    print()
    print("  SUB-DECOMPOSITION OF TERM 1 -- is it more guns, or worse tiles?")
    print(f"  {'group':<6}{'enemy guns alive':>18}{'enemy sents alive':>19}"
          f"{'guns IN RANGE':>15}{'sents IN RANGE':>16}{'dmg per gun-in-range-rnd':>26}")
    for lab, g in ALL:
        fr = max(g["fwd_rounds"], 1)
        ir = g["fwd_gun_inrange"] + g["fwd_sent_inrange"]
        print(f"  {lab:<6}{g['fwd_gun_alive']/fr:>18.2f}{g['fwd_sent_alive']/fr:>19.2f}"
              f"{g['fwd_gun_inrange']/fr:>15.3f}{g['fwd_sent_inrange']/fr:>16.3f}"
              f"{rr(g['fwd_dmg'], ir):>26.2f}")
    print("  (per forward builder-round; IN RANGE ignores facing and line-of-sight, so it is")
    print("   an upper bound on threat and a clean population control: it says how many enemy")
    print("   turrets COULD reach the tile we chose to stand on.)")
    uir = (US["fwd_gun_inrange"] + US["fwd_sent_inrange"]) / max(US["fwd_rounds"], 1)
    tir = (TOP["fwd_gun_inrange"] + TOP["fwd_sent_inrange"]) / max(TOP["fwd_rounds"], 1)
    print(f"  ==> TERM 1a  turrets-in-range per forward round, US/TOP = {rr(uir, tir):.2f}x")
    print(f"  ==> TERM 1b  damage per turret-in-range-round,   US/TOP = "
          f"{rr(rr(US['fwd_dmg'], US['fwd_gun_inrange']+US['fwd_sent_inrange']), rr(TOP['fwd_dmg'], TOP['fwd_gun_inrange']+TOP['fwd_sent_inrange'])):.2f}x")
    print(f"      1a x 1b = {rr(uir, tir)*rr(rr(US['fwd_dmg'], US['fwd_gun_inrange']+US['fwd_sent_inrange']), rr(TOP['fwd_dmg'], TOP['fwd_gun_inrange']+TOP['fwd_sent_inrange'])):.2f}x  (must equal TERM 1)")

    # ---------------- H2 ---------------------------------------------------
    print()
    print("=" * W)
    print("H2 -- FOCUS (distinct turret TILES that fired on the victim's tile on the death round)")
    print("=" * W)
    print(f"  {'group':<6}{'n':>9}{'1 shooter':>12}{'2':>9}{'3+':>9}{'mean':>8}"
          f"{'guns in range':>15}{'sents in range':>16}")
    for lab, g in ALL:
        ds = [d for d in g["deaths"] if d[0] == 1 and d[4] > 0]
        n = max(len(ds), 1)
        print(f"  {lab:<6}{len(ds):>9,}{pct(sum(1 for d in ds if d[4] == 1), len(ds)):>11.2f}%"
              f"{pct(sum(1 for d in ds if d[4] == 2), len(ds)):>8.2f}%"
              f"{pct(sum(1 for d in ds if d[4] >= 3), len(ds)):>8.2f}%"
              f"{sum(d[4] for d in ds)/n:>8.2f}"
              f"{sum(d[24] for d in ds)/n:>15.2f}{sum(d[25] for d in ds)/n:>16.2f}")

    # ---------------- H3 ---------------------------------------------------
    print()
    print("=" * W)
    print("H3 -- DEPTH (distance to the ENEMY core, normalised by core-to-core distance;")
    print("      SMALLER = DEEPER inside the enemy half)")
    print("=" * W)
    print(f"  {'group':<6}{'median @death':>15}{'p25':>8}{'p75':>8}"
          f"{'mean over fwd ROUNDS':>23}{'deaths d2<=32':>15}{'deaths d2<=8':>14}")
    for lab, g in ALL:
        ds = sorted(d[18] for d in g["deaths"] if d[0] == 1)
        n = len(ds)
        md = ds[n // 2] if n else float("nan")
        p25 = ds[n // 4] if n else float("nan")
        p75 = ds[3 * n // 4] if n else float("nan")
        n32 = sum(1 for d in g["deaths"] if d[0] == 1 and d[17] <= 32)
        n8 = sum(1 for d in g["deaths"] if d[0] == 1 and d[17] <= 8)
        print(f"  {lab:<6}{md:>15.3f}{p25:>8.3f}{p75:>8.3f}"
              f"{g['fwd_depth_sum']/max(g['fwd_rounds'], 1):>23.3f}"
              f"{pct(n32, n):>14.2f}%{pct(n8, n):>13.2f}%")

    # ---------------- H4 ---------------------------------------------------
    print()
    print("=" * W)
    print("H4 -- TRANSIT vs STATION   *** THE ONE THAT DECIDES THE LAUNCHER-DELIVERY PLANK ***")
    print("  Every forward builder-round AND every forward death bucketed by rounds since that")
    print("  bot last moved.  Hazard is computed WITHIN each state -- same side-set both sides")
    print("  of the fraction.")
    print("=" * W)
    for lab, g in ALL:
        ds = fwd(g)
        dbk = Counter(d[14] for d in ds)
        print(f"  --- {lab} --- ({len(ds):,} forward deaths, {g['fwd_rounds']:,} forward builder-rounds)")
        print(f"    {'state':<16}{'fwd rounds':>13}{'% of rounds':>13}{'deaths':>9}"
              f"{'% of deaths':>13}{'deaths/1k rnds':>16}{'vs group mean':>15}")
        base = rate(len(ds), g["fwd_rounds"])
        for i, nm in enumerate(SM_LABELS):
            r = rate(dbk[i], g["fwd_sm"][i])
            print(f"    {nm:<16}{g['fwd_sm'][i]:>13,}{pct(g['fwd_sm'][i], g['fwd_rounds']):>12.2f}%"
                  f"{dbk[i]:>9,}{pct(dbk[i], len(ds)):>12.2f}%{r:>16.2f}{rr(r, base):>14.2f}x")
    print("  US/TOP hazard ratio WITHIN each transit state (this is the 3.47x, decomposed):")
    print(f"    {'state':<16}{'US rate':>10}{'TOP rate':>11}{'US/TOP':>10}"
          f"{'US round-share':>16}{'TOP round-share':>17}")
    ud_bk = Counter(d[14] for d in fwd(US))
    td_bk = Counter(d[14] for d in fwd(TOP))
    for i, nm in enumerate(SM_LABELS):
        ur = rate(ud_bk[i], US["fwd_sm"][i])
        tr = rate(td_bk[i], TOP["fwd_sm"][i])
        print(f"    {nm:<16}{ur:>10.2f}{tr:>11.2f}{rr(ur, tr):>9.2f}x"
              f"{pct(US['fwd_sm'][i], US['fwd_rounds']):>15.2f}%"
              f"{pct(TOP['fwd_sm'][i], TOP['fwd_rounds']):>16.2f}%")
    print("  STANDARDISATION -- what would the US rate be if we spent our forward rounds in")
    print("  TOP's transit-state MIX (removes the composition difference, keeps our hazards)?")
    std = sum(rate(ud_bk[i], US["fwd_sm"][i]) * (TOP["fwd_sm"][i] / max(TOP["fwd_rounds"], 1))
              for i in range(NSM) if US["fwd_sm"][i])
    print(f"    US observed {UR:.2f}/1k  ->  US standardised to TOP's mix {std:.2f}/1k   "
          f"(ratio to TOP {rr(std, TR):.2f}x vs observed {rr(UR, TR):.2f}x)")
    print("  ⭐ THE COMMISSIONED k=3 / k=10 FORM (moved within the last k rounds), exact:")
    print(f"    {'group':<9}{'k':>4}{'transit rnds':>14}{'transit%':>10}{'deaths T':>10}"
          f"{'deaths T%':>11}{'T rate/1k':>11}{'S rate/1k':>11}{'T/S':>8}")
    for lab, g in ALL:
        for k, key in ((3, "fwd_t3"), (10, "fwd_t10")):
            ds = fwd(g)
            dt = sum(1 for d in ds if 0 <= d[13] <= k)
            sr = g["fwd_rounds"] - g[key]
            print(f"    {lab:<9}{k:>4}{g[key]:>14,}{pct(g[key], g['fwd_rounds']):>9.2f}%"
                  f"{dt:>10,}{pct(dt, len(ds)):>10.2f}%{rate(dt, g[key]):>11.2f}"
                  f"{rate(len(ds)-dt, sr):>11.2f}{rr(rate(dt, g[key]), rate(len(ds)-dt, sr)):>7.2f}x")
    print("  ROUNDS SINCE THE BOT LAST *ACTED* (build/attack/heal), forward rounds only:")
    print(f"    {'state':<16}{'US % of rounds':>16}{'TOP % of rounds':>18}")
    for i, nm in enumerate(SM_LABELS):
        print(f"    {nm:<16}{pct(US['fwd_sa'][i], US['fwd_rounds']):>15.2f}%"
              f"{pct(TOP['fwd_sa'][i], TOP['fwd_rounds']):>17.2f}%")
    print("  CONTROL 3c -- same transit instrument on HOME rounds (composition must differ):")
    print(f"    {'state':<16}{'US home %':>12}{'TOP home %':>13}")
    for i, nm in enumerate(SM_LABELS):
        print(f"    {nm:<16}{pct(US['home_sm'][i], US['home_rounds']):>11.2f}%"
              f"{pct(TOP['home_sm'][i], TOP['home_rounds']):>12.2f}%")
    print("  thrown-at-least-once among forward deaths:")
    for lab, g in ALL:
        ds = fwd(g)
        print(f"    {lab:<5} {sum(1 for d in ds if d[16] > 0):,}/{len(ds):,} = "
              f"{pct(sum(1 for d in ds if d[16] > 0), len(ds)):.2f}%")

    # ---------------- H5 ---------------------------------------------------
    print()
    print("=" * W)
    print("H5 -- HP TRAJECTORY.  A builder has 40 HP; a gunner does 7 and a sentinel 18, so")
    print("      NO builder can die from full HP in one round.  The measurable question is how")
    print("      LONG the killing episode lasted and whether the bot could have left.")
    print("=" * W)
    print(f"  {'group':<6}{'n':>9}{'mean hp_start':>15}{'mean age':>10}"
          f"{'rnds first-dmg->death':>23}{'median':>9}{'n dmg rounds':>14}{'ever healed':>13}")
    for lab, g in ALL:
        ds = [d for d in g["deaths"] if d[0] == 1 and d[11] > 0]
        n = max(len(ds), 1)
        ep = sorted(d[22] for d in ds if d[22] >= 0)
        print(f"  {lab:<6}{len(ds):>9,}{sum(d[10] for d in ds)/n:>15.2f}"
              f"{sum(d[12] for d in ds)/n:>10.1f}"
              f"{(sum(ep)/max(len(ep), 1)):>23.2f}{(ep[len(ep)//2] if ep else float('nan')):>9.0f}"
              f"{sum(d[23] for d in ds)/n:>14.2f}{pct(sum(1 for d in ds if d[20] > 0), len(ds)):>12.2f}%")
    print("  DAMAGE EPISODE LENGTH (rounds between first damage ever taken and death):")
    print(f"    {'group':<6}{'<=1 rnd (burst)':>17}{'2-5':>9}{'6-20':>9}{'21-100':>9}{'>100':>9}{'never dmgd':>12}")
    for lab, g in ALL:
        ds = fwd(g)
        n = max(len(ds), 1)
        b = Counter()
        for d in ds:
            e = d[22]
            b["never" if e < 0 else "<=1" if e <= 1 else "2-5" if e <= 5 else
              "6-20" if e <= 20 else "21-100" if e <= 100 else ">100"] += 1
        print(f"    {lab:<6}{pct(b['<=1'], n):>16.2f}%{pct(b['2-5'], n):>8.2f}%"
              f"{pct(b['6-20'], n):>8.2f}%{pct(b['21-100'], n):>8.2f}%"
              f"{pct(b['>100'], n):>8.2f}%{pct(b['never'], n):>11.2f}%")
    print("  DID IT TRY TO LEAVE? (moved at least once AFTER first taking damage):")
    for lab, g in ALL:
        ds = [d for d in g["deaths"] if d[0] == 1 and d[22] >= 0 and d[13] >= 0]
        mv = sum(1 for d in ds if d[13] < d[22])
        print(f"    {lab:<5} {mv:,}/{len(ds):,} = {pct(mv, len(ds)):.2f}% moved after first damage")

    print()
    print("  BONUS -- enemy builder bots within d2<=2 of the victim at round start:")
    for lab, g in ALL:
        ds = fwd(g)
        print(f"    {lab:<5} {pct(sum(1 for d in ds if d[21] > 0), len(ds)):.2f}% of forward deaths "
              f"(mean {sum(d[21] for d in ds)/max(len(ds), 1):.2f})")

    # ---------------- CONTROL 4: opponent-matched ---------------------------
    print()
    print("=" * W)
    print("CONTROL 4 -- OPPONENT-MATCHED. The decomposition above says the biggest single term is")
    print("  HOW MANY ENEMY TURRETS EXIST, which is a property of the OPPONENT, not of us. If that")
    print("  is right, matching opponent quality must shrink the gap. US_vTOP = our 115 games against")
    print("  a >=1900 team; TOP_vTOP = both sides of TOP-vs-TOP games; TOP_vOTH = the TOP side against")
    print("  everyone else.  Same instrument, same definitions, different opponent populations.")
    print("=" * W)
    print(f"  {'group':<10}{'sides':>8}{'fwd deaths':>12}{'fwd-rnds':>12}{'deaths/1k':>11}"
          f"{'enemy turrets alive':>21}{'in range':>10}{'dmg/1k rnds':>13}")
    for lab in ("US", "US_vTOP", "TOP", "TOP_vTOP", "TOP_vOTH"):
        g = groups[lab]
        fr = max(g["fwd_rounds"], 1)
        n = len(fwd(g))
        print(f"  {lab:<10}{g['games']:>8,}{n:>12,}{g['fwd_rounds']:>12,}"
              f"{rate(n, g['fwd_rounds']):>11.2f}"
              f"{(g['fwd_gun_alive']+g['fwd_sent_alive'])/fr:>21.2f}"
              f"{(g['fwd_gun_inrange']+g['fwd_sent_inrange'])/fr:>10.3f}"
              f"{rate(g['fwd_dmg'], g['fwd_rounds']):>13.2f}")
    print()
    print("  ENEMY TURRETS ALIVE / IN RANGE per forward builder-round, BY ROUND BAND")
    print("  (separates 'our opponents own more guns' from 'we go forward later, when more guns exist')")
    print(f"  {'band':<10}" + "".join(f"{x:>13}" for x in
          ("US alive", "TOP alive", "US inrange", "TOP inrange", "alive US/TOP", "inrng US/TOP")))
    for b, (lo, hi) in enumerate(DOCTRINE):
        ua = US["fwd_alive_band"][b] / max(US["fwd_rounds_band"][b], 1)
        ta = TOP["fwd_alive_band"][b] / max(TOP["fwd_rounds_band"][b], 1)
        ui = US["fwd_inrange_band"][b] / max(US["fwd_rounds_band"][b], 1)
        ti = TOP["fwd_inrange_band"][b] / max(TOP["fwd_rounds_band"][b], 1)
        print(f"  r{lo}-{hi:<6}{ua:>13.2f}{ta:>13.2f}{ui:>13.3f}{ti:>13.3f}"
              f"{rr(ua, ta):>12.2f}x{rr(ui, ti):>12.2f}x")
    print()
    print("  ⭐ THE SAME FOUR TERMS, COMPUTED WITHIN EACH ROUND BAND -- because the pooled version")
    print("     is Simpson-ed: turret exposure is equal in r0-59 and 4x apart in r500-999, while the")
    print("     DEATH ratio is ~3.2x in both.")
    print(f"  {'band':<10}{'A pop':>8}{'B tile':>8}{'C dmg/turret-rnd':>18}"
          f"{'D absorb':>10}{'product':>9}{'observed':>10}")
    for b, (lo, hi) in enumerate(DOCTRINE):
        uA = US["fwd_alive_band"][b] / max(US["fwd_rounds_band"][b], 1)
        tA = TOP["fwd_alive_band"][b] / max(TOP["fwd_rounds_band"][b], 1)
        uI = US["fwd_inrange_band"][b] / max(US["fwd_rounds_band"][b], 1)
        tI = TOP["fwd_inrange_band"][b] / max(TOP["fwd_rounds_band"][b], 1)
        A = rr(uA, tA)
        B = rr(rr(uI, tI), A)
        Cc = rr(rr(US["fwd_dmg_band"][b], US["fwd_inrange_band"][b]),
                rr(TOP["fwd_dmg_band"][b], TOP["fwd_inrange_band"][b]))
        udb = sum(1 for d in US["deaths"] if d[0] == 1 and d[1] == b)
        tdb = sum(1 for d in TOP["deaths"] if d[0] == 1 and d[1] == b)
        D = rr(rr(TOP["fwd_dmg_band"][b], tdb), rr(US["fwd_dmg_band"][b], udb))
        obs = rr(rate(udb, US["fwd_rounds_band"][b]), rate(tdb, TOP["fwd_rounds_band"][b]))
        print(f"  r{lo}-{hi:<6}{A:>7.2f}x{B:>7.2f}x{Cc:>17.2f}x{D:>9.2f}x{A*B*Cc*D:>8.2f}x{obs:>9.2f}x")
    print("  damage taken per 1,000 forward builder-rounds, by band:")
    print(f"  {'band':<10}{'US':>10}{'TOP':>10}{'US/TOP':>9}")
    for b, (lo, hi) in enumerate(DOCTRINE):
        u = rate(US["fwd_dmg_band"][b], US["fwd_rounds_band"][b])
        t = rate(TOP["fwd_dmg_band"][b], TOP["fwd_rounds_band"][b])
        print(f"  r{lo}-{hi:<6}{u:>10.2f}{t:>10.2f}{rr(u, t):>8.2f}x")
    print()
    print("  FOUR-TERM PRODUCT (each term US/TOP; the product is the anchor by construction):")
    ua = (US["fwd_gun_alive"] + US["fwd_sent_alive"]) / max(US["fwd_rounds"], 1)
    ta = (TOP["fwd_gun_alive"] + TOP["fwd_sent_alive"]) / max(TOP["fwd_rounds"], 1)
    ui = (US["fwd_gun_inrange"] + US["fwd_sent_inrange"]) / max(US["fwd_rounds"], 1)
    ti = (TOP["fwd_gun_inrange"] + TOP["fwd_sent_inrange"]) / max(TOP["fwd_rounds"], 1)
    t_pop = rr(ua, ta)
    t_tile = rr(rr(ui, ti), t_pop)
    t_eff = rr(rr(US["fwd_dmg"], US["fwd_gun_inrange"] + US["fwd_sent_inrange"]),
               rr(TOP["fwd_dmg"], TOP["fwd_gun_inrange"] + TOP["fwd_sent_inrange"]))
    t_abs = rr(dd_t, dd_u)
    lg = math.log
    tot = lg(t_pop) + lg(t_tile) + lg(t_eff) + lg(t_abs)
    for nm, v in (("A. enemy turrets EXIST (opponent property)", t_pop),
                  ("B. share of them IN RANGE of our tile", t_tile),
                  ("C. damage per turret-in-range-round", t_eff),
                  ("D. damage absorbed per death", t_abs)):
        print(f"    {nm:<45}{v:>7.2f}x   log-share {100*lg(v)/tot:>6.1f}%")
    print(f"    {'PRODUCT':<45}{t_pop*t_tile*t_eff*t_abs:>7.2f}x   (anchor {rr(UR, TR):.2f}x)")

    if args.dump:
        p = Path("scratchpad/fwd_death_rows_s31.tsv")
        with p.open("w") as fh:
            fh.write("group\t" + "\t".join(DEATH_COLS) + "\n")
            for lab, g in ALL:
                for d in g["deaths"]:
                    fh.write(lab + "\t" + "\t".join(str(x) for x in d) + "\n")
        print(f"\n  dumped {p}")


if __name__ == "__main__":
    main()
