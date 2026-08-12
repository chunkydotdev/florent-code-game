#!/usr/bin/env python3
"""DWELL BY ROUND BAND — where in the game does our forward-dwell excess sit?

Commissioned by the research arm, s31 (2026-08-11), as the band decomposition of
Instrument B in docs/research/QUEUE-forward-efficiency-2026-08-11.md
(pooled: US 54.55 forward builder-rounds per forward build vs TOP 23.93, 2.28x).

READ-ONLY.  Decodes replay_archive/*.replay26 and corpus/meta_join.tsv.  Writes
nothing except stdout.

Definitions are inherited verbatim from scratchpad/dwell.py (Instrument B):
  * a builder-round is FORWARD when d2(bot, enemy_core) < d2(bot, own_core)
  * a build is FORWARD by the same test on the new entity's position,
    excluding kind == 'builder_bot'
  * cores are the map's two cores (NW corner of the 2x2 footprint)
  * a build is the FIRST placeEntity carrying a given entity id (corpus-howto
    TRAP 1: rotate() re-emits placeEntity).  dwell.py keyed this on the live
    position table; this script keys it on a persistent `seen` set, which is
    strictly the documented rule.  Both are reported.

ESTIMATOR (named in full, per the commission):
  PRIMARY = pooled ratio within band
          = (sum over games of forward builder-rounds in band b)
          / (sum over games of forward builds in band b)
  Uncertainty = game-resampled bootstrap, 1000 resamples, unit = GAME.
  Mean-of-per-game-ratios is NOT reported as primary (CV 2.60, queue doc).

ROBUSTNESS FRAMING (attribution artefact):
  Each forward builder-round is attributed to the band of THAT BUILDER's NEXT
  forward build.  Rounds with no subsequent forward build by that builder are
  RIGHT-CENSORED and reported separately, never dropped silently.
  Build -> builder attribution: the friendly builder bot orthogonally adjacent
  (d2 == 1) to the new entity's tile at the moment of the placeEntity; ties
  broken by lowest entity id and counted as ambiguous.

GROUPS:
  US  = meta_join rows where teamAId or teamBId is our team id; the measured
        side is ours.
  TOP = meta_join rows with NEITHER side us, and at least one side among the
        nine >=1900 teams named in the queue doc; the measured side(s) are the
        TOP one(s).  A game with TOP on both sides contributes BOTH sides, and
        the bootstrap resamples the GAME (so both sides move together).
"""
from __future__ import annotations

import bisect
import csv
import json
import os
import random
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
UNIFORM = [(0, 99), (100, 199), (200, 299), (300, 499), (500, 999)]
# CONTROL 3 scheme: r0-0 and r1000-1999 can hold nothing at all; r999-999 is
# reachable but almost never carries a forward build.  All three force the
# undefined-denominator path on REAL data rather than on an assertion.
NARROW = [(0, 0), (1, 1), (998, 998), (999, 999), (1000, 1999)]
SCHEMES = {"doctrine": DOCTRINE, "uniform": UNIFORM, "narrow": NARROW}
NB = 5
SEED = 20260811


def band_of(rnd, bands):
    for i, (lo, hi) in enumerate(bands):
        if lo <= rnd <= hi:
            return i
    return None


# --------------------------------------------------------------------------
# replay walk
# --------------------------------------------------------------------------
def walk(path):
    """Return (turns, {team: side_record}) or None."""
    data = path.read_bytes()
    mapbuf = None
    turns = []
    winner = None
    for n, w, v in fields(data):
        if n == 1 and w == WIRE_LEN:
            mapbuf = v
        elif n == 3 and w == WIRE_LEN:
            turns.append(v)
        elif n == 4 and w != WIRE_LEN:
            winner = v
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

    def d2(a, b):
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

    pos, team, kind = {}, {}, {}
    seen = set()
    btm = {}                                           # bot id -> team, survives death
    # per team
    fwd_rounds = {0: Counter(), 1: Counter()}          # round -> n forward builder-rounds
    fwd_builds = {0: Counter(), 1: Counter()}          # round -> n forward builds
    fwd_builds_posonly = {0: 0, 1: 0}                  # dwell.py's `new = id not in pos` variant
    bot_fwd = defaultdict(list)                        # bot id -> [rounds forward]
    bot_build = defaultdict(list)                      # bot id -> [rounds of its forward builds]
    attr = {0: [0, 0, 0], 1: [0, 0, 0]}                # ok, ambiguous, unattributed

    for rnd, tb in enumerate(turns):
        for _a, _b, ub in fields(tb):
            for un, _w, ubuf in fields(ub):
                if un == 1:
                    for en, _e, eb in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(eb, rnd)
                        if e is None:
                            continue
                        first_seen = e.id not in seen
                        first_pos = e.id not in pos
                        seen.add(e.id)
                        pos[e.id] = e.pos
                        team[e.id] = e.team
                        kind[e.id] = e.kind
                        if e.kind == "builder_bot":
                            btm[e.id] = e.team
                            continue
                        t = e.team
                        forward = d2(e.pos, home[1 - t]) < d2(e.pos, home[t])
                        if forward and first_pos:
                            fwd_builds_posonly[t] += 1
                        if not (forward and first_seen):
                            continue
                        fwd_builds[t][rnd] += 1
                        # attribute to the adjacent friendly builder bot
                        cands = [
                            bid for bid, bp in pos.items()
                            if kind.get(bid) == "builder_bot" and team.get(bid) == t
                            and d2(bp, e.pos) == 1
                        ]
                        if len(cands) == 1:
                            attr[t][0] += 1
                            bot_build[cands[0]].append(rnd)
                        elif cands:
                            attr[t][1] += 1
                            bot_build[min(cands)].append(rnd)
                        else:
                            attr[t][2] += 1
                elif un == 2:
                    d = {k: v for k, _x, v in fields(ubuf)}
                    if 1 in d and 2 in d and d[1] in pos:
                        pos[d[1]] = read_pos(d[2])
                elif un == 3:
                    for _rn, _rw, rv in fields(ubuf):
                        pos.pop(rv, None)
                        team.pop(rv, None)
                        kind.pop(rv, None)
        for eid, p in pos.items():
            if kind.get(eid) != "builder_bot":
                continue
            t = team[eid]
            if d2(p, home[1 - t]) < d2(p, home[t]):
                fwd_rounds[t][rnd] += 1
                bot_fwd[eid].append(rnd)

    # waiting-time framing: forward round -> band of that bot's NEXT forward build
    wt = {0: Counter(), 1: Counter()}     # next-build round -> n forward rounds
    cw = {0: Counter(), 1: Counter()}     # CENSORED forward rounds, by their OWN round
    cens = {0: 0, 1: 0}
    for bid, rlist in bot_fwd.items():
        t = btm.get(bid)
        if t is None:
            continue
        blist = sorted(bot_build.get(bid, ()))
        for r in rlist:
            j = bisect.bisect_left(blist, r)
            if j < len(blist):
                wt[t][blist[j]] += 1
            else:
                cens[t] += 1
                cw[t][r] += 1

    out = {}
    for t in (0, 1):
        out[t] = dict(
            fr=dict(fwd_rounds[t]), fb=dict(fwd_builds[t]), wt=dict(wt[t]),
            cw=dict(cw[t]),
            cens=cens[t], attr=attr[t], fb_posonly=fwd_builds_posonly[t],
        )
    return len(turns), out, winner


def worker(args):
    fn, our_side, top_sides, exp_win = args
    p = AR / fn
    try:
        r = walk(p)
    except Exception as exc:  # noqa: BLE001
        return ("ERR", fn, repr(exc))
    if r is None:
        return None
    T, rec, winner = r
    return ("OK", fn, T, rec, winner, our_side, top_sides, exp_win)


# --------------------------------------------------------------------------
# aggregation
# --------------------------------------------------------------------------
def to_bands(counter, bands):
    v = [0] * NB
    for rnd, n in counter.items():
        b = band_of(rnd, bands)
        if b is not None:
            v[b] += n
    return v


class Group:
    """Per-game packed records for one group and one measured-side policy."""

    def __init__(self, label):
        self.label = label
        self.games = []          # list of dict(T=..., vectors)

    def add(self, T, sides, rng):
        # sides: list of per-side records to sum into ONE game record
        g = {"T": T}
        for sname, bands in SCHEMES.items():
            fr = [0] * NB
            fb = [0] * NB
            wt = [0] * NB
            cw = [0] * NB
            shfb = [0] * NB
            for rec in sides:
                for i, x in enumerate(to_bands(rec["fr"], bands)):
                    fr[i] += x
                for i, x in enumerate(to_bands(rec["fb"], bands)):
                    fb[i] += x
                for i, x in enumerate(to_bands(rec["wt"], bands)):
                    wt[i] += x
                for i, x in enumerate(to_bands(rec["cw"], bands)):
                    cw[i] += x
                # CONTROL 2 (exposure-matched build reassignment): draw each
                # forward build's round from this side's own forward-exposure
                # distribution.  Under this null the ratio must be flat.
                rounds = list(rec["fr"].keys())
                wts = [rec["fr"][r] for r in rounds]
                nb_builds = sum(rec["fb"].values())
                if nb_builds:
                    if rounds:
                        drawn = rng.choices(rounds, weights=wts, k=nb_builds)
                    else:
                        drawn = [r for r, n in rec["fb"].items() for _ in range(n)]
                    for r in drawn:
                        b = band_of(r, bands)
                        if b is not None:
                            shfb[b] += 1
            g[sname] = dict(fr=fr, fb=fb, wt=wt, cw=cw, shfb=shfb)
        g["cens"] = sum(r["cens"] for r in sides)
        g["fr_tot"] = sum(sum(r["fr"].values()) for r in sides)
        g["fb_tot"] = sum(sum(r["fb"].values()) for r in sides)
        g["fb_posonly"] = sum(r["fb_posonly"] for r in sides)
        g["attr"] = [sum(r["attr"][i] for r in sides) for i in range(3)]
        g["nsides"] = len(sides)
        self.games.append(g)


# ---- bootstrap via big-int packing (no numpy in this venv) ----------------
FW = 44                                   # bits per packed field
MASK = (1 << FW) - 1


def pack(vals):
    x = 0
    for i, v in enumerate(vals):
        x |= int(v) << (FW * i)
    return x


def unpack(x, k):
    return [(x >> (FW * i)) & MASK for i in range(k)]


def bootstrap(vectors, k, nres=1000, seed=SEED):
    """vectors: list of packed per-game ints.  Returns list of nres unpacked lists."""
    rng = random.Random(seed)
    G = len(vectors)
    out = []
    rr = rng.randrange
    for _ in range(nres):
        s = 0
        for _i in range(G):
            s += vectors[rr(G)]
        out.append(unpack(s, k))
    return out


def ci(samples):
    s = sorted(samples)
    n = len(s)
    return s[int(0.025 * n)], s[min(n - 1, int(0.975 * n))]


def ratio(n, d):
    return None if d == 0 else n / d


def fmt_ratio(r):
    return "  UNDEFINED" if r is None else f"{r:10.2f}"


# --------------------------------------------------------------------------
def select():
    rows = list(csv.DictReader(open("corpus/meta_join.tsv"), delimiter="\t"))
    us, top = [], []
    for r in rows:
        a_us = r["teamAId"] == OURS
        b_us = r["teamBId"] == OURS
        if a_us or b_us:
            us.append((r["file"], 0 if a_us else 1, None, r))
        else:
            sides = []
            if r["teamAName"] in TOP_TEAMS:
                sides.append(0)
            if r["teamBName"] in TOP_TEAMS:
                sides.append(1)
            if sides:
                top.append((r["file"], None, tuple(sides), r))
    us = [x for x in us if (AR / x[0]).exists()]
    top = [x for x in top if (AR / x[0]).exists()]
    return us, top


def run_group(label, sel, limit=None, invert=False):
    items = sel if limit is None else sel[:limit]
    args = []
    for f, o, t, r in items:
        w = {"a": 0, "b": 1}.get(r.get("game_winner_side", ""), None)
        args.append((f, o, t, w))
    grp = Group(label)
    rng = random.Random(SEED)
    errs = 0
    skipped = 0
    seatcheck = [0, 0]
    with Pool(processes=min(8, os.cpu_count() or 4)) as pool:
        for res in pool.imap_unordered(worker, args, chunksize=32):
            if res is None:
                skipped += 1
                continue
            if res[0] == "ERR":
                errs += 1
                continue
            _ok, fn, T, rec, winner, our_side, top_sides, exp_win = res
            if our_side is not None:
                sides = [1 - our_side] if invert else [our_side]
            else:
                if invert:
                    sides = sorted({1 - s for s in top_sides} - set(top_sides))
                    if not sides:
                        skipped += 1
                        continue
                else:
                    sides = list(top_sides)
            grp.add(T, [rec[s] for s in sides], rng)
            if winner is not None and exp_win is not None:
                seatcheck[0] += 1
                seatcheck[1] += int(winner == exp_win)
    return grp, errs, skipped, seatcheck


def band_table(grp, scheme, key_n="fr", key_d="fb", nres=1000, title=""):
    bands = SCHEMES[scheme]
    games = grp.games
    # packed vectors: [n0..n4, d0..d4]
    vecs = [pack(g[scheme][key_n] + g[scheme][key_d]) for g in games]
    boots = bootstrap(vecs, 2 * NB, nres=nres)
    tot_n = [sum(g[scheme][key_n][b] for g in games) for b in range(NB)]
    tot_d = [sum(g[scheme][key_d][b] for g in games) for b in range(NB)]
    alive = [sum(1 for g in games if g["T"] > bands[b][0]) for b in range(NB)]
    sides_alive = [sum(g["nsides"] for g in games if g["T"] > bands[b][0]) for b in range(NB)]
    lines = []
    lines.append(f"  {title}   [{grp.label}]  games={len(games)}  sides={sum(g['nsides'] for g in games)}")
    lines.append(f"  {'band':<10}{'fwd b-rounds':>14}{'fwd builds':>12}{'ROUNDS/BUILD':>14}"
                 f"{'95% CI':>20}{'games alive':>13}{'rnds/side-alive':>17}{'blds/side-alive':>17}")
    for b, (lo, hi) in enumerate(bands):
        pt = ratio(tot_n[b], tot_d[b])
        rs = [x[b] / x[NB + b] for x in boots if x[NB + b] > 0]
        cistr = "        UNDEFINED" if not rs else "%8.2f -%8.2f" % ci(rs)
        sa = sides_alive[b] or 1
        lines.append(f"  r{lo}-{hi:<6}{tot_n[b]:>14,}{tot_d[b]:>12,}{fmt_ratio(pt):>14}"
                     f"{cistr:>20}{alive[b]:>13,}{tot_n[b]/sa:>17.1f}{tot_d[b]/sa:>17.2f}")
    pn, pd = sum(tot_n), sum(tot_d)
    lines.append(f"  {'POOLED':<10}{pn:>14,}{pd:>12,}{fmt_ratio(ratio(pn, pd)):>14}")
    return "\n".join(lines)


def pooled(grp, key_n="fr", key_d="fb", scheme="doctrine"):
    n = sum(sum(g[scheme][key_n]) for g in grp.games)
    d = sum(sum(g[scheme][key_d]) for g in grp.games)
    return n, d, ratio(n, d)


def main():
    us_sel, top_sel = select()
    print("=" * 100)
    print("POPULATION SELECTION (corpus/meta_join.tsv, side keyed on teamAId/teamBId, "
          "NOT on us_side — corpus-howto TRAP 7)")
    print(f"  US   games with a replay on disk : {len(us_sel):,}   (queue doc Instrument A: 5,143)")
    print(f"  TOP  third-party games on disk   : {len(top_sel):,}   (queue doc: 3,080)")
    both = sum(1 for x in top_sel if len(x[2]) == 2)
    print(f"       of which TOP on BOTH sides  : {both:,}  -> contribute two measured sides each")
    print("=" * 100)

    limit = None
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        limit = int(sys.argv[1])
    nres = 1000

    US, e1, s1, sc1 = run_group("US", us_sel, limit)
    TOP, e2, s2, sc2 = run_group("TOP", top_sel, limit)
    print(f"\ndecoded: US {len(US.games):,} games (err {e1}, skipped {s1})   "
          f"TOP {len(TOP.games):,} games (err {e2}, skipped {s2})")
    print("SEAT VALIDATION (independent of us_side): does the replay-internal winner byte")
    print("  agree with meta_join's game_winner_side under TEAM_A == 0?")
    for lab, sc in (("US", sc1), ("TOP", sc2)):
        print(f"  {lab}: {sc[1]:,} / {sc[0]:,} agree "
              f"({100*sc[1]/max(sc[0],1):.4f}%)  -- must be ~100%, and a swapped "
              f"convention would read ~0%")

    # ---------------- CONTROL 4: pooled reproduction -----------------------
    print("\n" + "=" * 100)
    print("CONTROL 4 — POOLED REPRODUCTION vs the queue doc (US 54.55, TOP 23.93, ratio 2.28x)")
    print("=" * 100)
    for grp in (US, TOP):
        n, d, r = pooled(grp)
        np_ = sum(x["fr_tot"] for x in grp.games)
        dp = sum(x["fb_posonly"] for x in grp.games)
        ng = len(grp.games)
        print(f"  {grp.label:<4} n={ng:,} games   fwd builder-rounds/game {n/ng:8.1f}   "
              f"fwd builds/game {d/ng:6.2f}   ROUNDS PER FORWARD BUILD {r:7.2f}")
        print(f"       (dwell.py's `id not in pos` build rule instead of `seen`: "
              f"builds {dp:,} vs {d:,}, dwell {np_/max(dp,1):.2f})")
    ru = pooled(US)[2]
    rt = pooled(TOP)[2]
    print(f"  RATIO US/TOP = {ru/rt:.2f}x   (queue doc 2.28x)")

    # ---------------- primary band tables ---------------------------------
    for scheme in ("doctrine", "uniform"):
        print("\n" + "=" * 100)
        print(f"PRIMARY — pooled ratio within band, {scheme.upper()} bands "
              f"(numerator round in band b / build in band b)")
        print("=" * 100)
        print(band_table(US, scheme, nres=nres, title="US "))
        print()
        print(band_table(TOP, scheme, nres=nres, title="TOP"))
        print("\n  US/TOP ratio by band:")
        bands = SCHEMES[scheme]
        for b, (lo, hi) in enumerate(bands):
            un = sum(g[scheme]["fr"][b] for g in US.games)
            ud = sum(g[scheme]["fb"][b] for g in US.games)
            tn = sum(g[scheme]["fr"][b] for g in TOP.games)
            td = sum(g[scheme]["fb"][b] for g in TOP.games)
            u, t = ratio(un, ud), ratio(tn, td)
            rr = "UNDEFINED" if (u is None or t is None or t == 0) else f"{u/t:.2f}x"
            print(f"    r{lo}-{hi:<6} US {fmt_ratio(u)}   TOP {fmt_ratio(t)}   ratio {rr}")

    # ---------------- robustness: waiting-time framing --------------------
    print("\n" + "=" * 100)
    print("ROBUSTNESS — WAITING-TIME framing: each forward builder-round attributed to the")
    print("band of THAT BUILDER's NEXT forward build.  Right-censored rounds reported, not dropped.")
    print("=" * 100)
    for g in (US, TOP):
        cens = sum(x["cens"] for x in g.games)
        tot = sum(x["fr_tot"] for x in g.games)
        ok, amb, non = [sum(x["attr"][i] for x in g.games) for i in range(3)]
        print(f"  {g.label}: censored forward builder-rounds {cens:,} of {tot:,} "
              f"({100*cens/max(tot,1):.1f}%)  |  build->builder attribution: "
              f"unique {ok:,}, ambiguous {amb:,}, none {non:,} "
              f"({100*non/max(ok+amb+non,1):.1f}% unattributed)")
    for scheme in ("doctrine", "uniform"):
        print()
        print(band_table(US, scheme, key_n="wt", nres=nres, title=f"US  WAIT/{scheme}"))
        print()
        print(band_table(TOP, scheme, key_n="wt", nres=nres, title=f"TOP WAIT/{scheme}"))

    print("\n" + "-" * 100)
    print("CENSORED MASS BY ITS OWN ROUND — forward builder-rounds that are never followed by")
    print("a forward build FROM THAT BUILDER.  This is the part the waiting-time framing drops,")
    print("so it is reported in full rather than as a footnote.")
    print("-" * 100)
    for scheme in ("doctrine", "uniform"):
        bands = SCHEMES[scheme]
        print(f"  {scheme}:")
        print(f"    {'band':<12}{'US censored':>13}{'US fwd-rnds':>13}{'US cens%':>10}"
              f"{'TOP censored':>15}{'TOP fwd-rnds':>14}{'TOP cens%':>11}"
              f"{'US-TOP pp':>11}")
        for b, (lo, hi) in enumerate(bands):
            uc = sum(x[scheme]["cw"][b] for x in US.games)
            ur = sum(x[scheme]["fr"][b] for x in US.games)
            tc = sum(x[scheme]["cw"][b] for x in TOP.games)
            tr = sum(x[scheme]["fr"][b] for x in TOP.games)
            up = 100 * uc / max(ur, 1)
            tp = 100 * tc / max(tr, 1)
            print(f"    r{lo}-{hi:<8}{uc:>13,}{ur:>13,}{up:>9.1f}%"
                  f"{tc:>15,}{tr:>14,}{tp:>10.1f}%{up-tp:>10.1f}pp")

    # ---------------- CONTROL 1: team swap --------------------------------
    print("\n" + "=" * 100)
    print("CONTROL 1 — TEAM SWAP: recompute with the measured side inverted.")
    print("  US group -> measures our OPPONENTS in our games.")
    print("  TOP group -> measures the NON-TOP side in the same third-party games")
    print("               (games with TOP on both sides drop out; n falls, as it must).")
    print("=" * 100)
    USi, _, _, _ = run_group("US-INV", us_sel, limit, invert=True)
    TOPi, _, si, _ = run_group("TOP-INV", top_sel, limit, invert=True)
    for g in (US, USi, TOP, TOPi):
        n, d, r = pooled(g)
        print(f"  {g.label:<8} n={len(g.games):<6,} fwd-rounds {n:>10,}  fwd-builds {d:>8,}  "
              f"ROUNDS/BUILD {fmt_ratio(r)}")
    print(f"  swap moved US   {pooled(US)[2]:.2f} -> {pooled(USi)[2]:.2f}")
    print(f"  swap moved TOP  {pooled(TOP)[2]:.2f} -> {pooled(TOPi)[2]:.2f}")
    print(f"  ({si:,} both-TOP games dropped from TOP-INV by construction)")

    # ---------------- CONTROL 2: band shuffle -----------------------------
    print("\n" + "=" * 100)
    print("CONTROL 2 — BAND SHUFFLE")
    print("=" * 100)
    print("  2a. THE LITERAL FORM AS COMMISSIONED ('permute the band label of each forward")
    print("      builder-round within a game') IS A NO-OP and I am showing that rather than")
    print("      substituting silently: permuting labels among the numerator items leaves the")
    print("      per-band multiset — hence every band total and every ratio — bit-identical.")
    for scheme in ("doctrine",):
        for g in (US, TOP):
            tot = [sum(x[scheme]["fr"][b] for x in g.games) for b in range(NB)]
            rng = random.Random(7)
            items = [b for b in range(NB) for _ in range(tot[b])] if sum(tot) < 4_000_000 else None
            if items is not None:
                rng.shuffle(items)
                c = Counter(items)
                shuf = [c[b] for b in range(NB)]
            else:
                shuf = tot
            print(f"      {g.label}: pre-shuffle {tot}  post-shuffle {shuf}  "
                  f"identical={tot == shuf}")
    print()
    print("  2b. THE FORM THAT TESTS THE STATED INTENT ('is the effect an artefact of")
    print("      exposure?'): within each game, redraw every forward build's ROUND from that")
    print("      side's OWN forward-builder-round distribution.  Under this null the rate of")
    print("      building is proportional to forward presence, so rounds-per-build MUST be flat")
    print("      at the pooled value in every band.")
    for scheme in ("doctrine", "uniform"):
        for g in (US, TOP):
            bands = SCHEMES[scheme]
            print(f"      {g.label} / {scheme}:")
            pn = sum(sum(x[scheme]["fr"]) for x in g.games)
            pd = sum(sum(x[scheme]["shfb"]) for x in g.games)
            reals, shufs = [], []
            for b, (lo, hi) in enumerate(bands):
                n = sum(x[scheme]["fr"][b] for x in g.games)
                d = sum(x[scheme]["shfb"][b] for x in g.games)
                real = ratio(sum(x[scheme]["fr"][b] for x in g.games),
                             sum(x[scheme]["fb"][b] for x in g.games))
                sh = ratio(n, d)
                if real:
                    reals.append(real)
                if sh:
                    shufs.append(sh)
                print(f"        r{lo}-{hi:<6} shuffled {fmt_ratio(sh)}   "
                      f"(real {fmt_ratio(real)})   pooled {fmt_ratio(ratio(pn, pd))}")
            if reals and shufs:
                print(f"        SPREAD max/min across bands: real {max(reals)/min(reals):.2f}x"
                      f"  ->  shuffled {max(shufs)/min(shufs):.2f}x   "
                      f"(flattening is the required direction)")

    # ---------------- CONTROL 3: empty band -------------------------------
    print("\n" + "=" * 100)
    print("CONTROL 3 — EMPTY BAND: a band no game reaches must report UNDEFINED, not 0.")
    print("=" * 100)
    for grp in (US, TOP):
        maxT = max(x["T"] for x in grp.games)
        print(f"  {grp.label}: longest game {maxT} rounds")
        print(band_table(grp, "narrow", nres=200, title=f"{grp.label} NARROW"))
    print(f"  sanity: ratio(0,0) = {ratio(0,0)!r} -> printed as '{fmt_ratio(ratio(0,0))}'; "
          f"ratio(7,0) = {ratio(7,0)!r}; ratio(0,7) = {ratio(0,7)!r} -> "
          f"'{fmt_ratio(ratio(0,7))}'  (a REAL zero still prints 0.00, so the two are "
          f"distinguishable)")

    # ---------------- game-length confound --------------------------------
    print("\n" + "=" * 100)
    print("GAME-LENGTH CONFOUND — survival profile of the two groups")
    print("=" * 100)
    print(f"  {'threshold':<12}{'US games alive':>16}{'US %':>9}{'TOP games alive':>18}{'TOP %':>9}")
    for thr in (0, 60, 100, 180, 200, 250, 300, 500, 999):
        ua = sum(1 for x in US.games if x["T"] > thr)
        ta = sum(1 for x in TOP.games if x["T"] > thr)
        print(f"  r>{thr:<10}{ua:>16,}{100*ua/len(US.games):>8.1f}%{ta:>18,}"
              f"{100*ta/len(TOP.games):>8.1f}%")
    for g in (US, TOP):
        ls = sorted(x["T"] for x in g.games)
        n = len(ls)
        print(f"  {g.label} game length: median {ls[n//2]}, mean {sum(ls)/n:.0f}, "
              f"p25 {ls[n//4]}, p75 {ls[3*n//4]}")


def main_repro():
    """CONTROL 4 diagnostic: the queue doc's Instrument B is a 120-game-per-group
    sample.  This asks whether 54.55 / 23.93 / 2.28x is reproducible at n=120 from
    the full population, i.e. whether the discrepancy is SAMPLING or METHOD."""
    us_sel, top_sel = select()
    US, _, _, _ = run_group("US", us_sel)
    TOP, _, _, _ = run_group("TOP", top_sel)
    print("=" * 100)
    print("CONTROL 4 DIAGNOSTIC — is the queue doc's Instrument B reproducible at n=120?")
    print("=" * 100)
    for lab, g in (("US", US), ("TOP", TOP)):
        n, d, r = pooled(g)
        print(f"  {lab} FULL POPULATION n={len(g.games):,}: "
              f"fwd-rounds/game {n/len(g.games):.1f}  builds/game {d/len(g.games):.2f}  "
              f"ROUNDS/BUILD {r:.2f}")
    print(f"  FULL RATIO US/TOP = {pooled(US)[2]/pooled(TOP)[2]:.2f}x    "
          f"(queue doc 2.28x on n=120/group)")

    print("\n  -- head-of-order 120 (meta_join row order, the cheapest thing a 120-game cut does):")
    for lab, g in (("US", US), ("TOP", TOP)):
        # run_group uses imap_unordered, so re-derive the head by re-decoding it
        pass
    for lab, sel in (("US", us_sel), ("TOP", top_sel)):
        h, _, _, _ = run_group(lab + "-head120", sel[:120])
        n, d, r = pooled(h)
        print(f"     {lab}: n={len(h.games)}  fwd-rounds/game {n/len(h.games):.1f}  "
              f"builds/game {d/len(h.games):.2f}  ROUNDS/BUILD {r:.2f}")

    print("\n  -- distribution of a RANDOM 120-game subsample (2,000 draws, without replacement):")
    rng = random.Random(SEED)
    def sub(g, k=120, B=2000):
        recs = [(sum(x["doctrine"]["fr"]), sum(x["doctrine"]["fb"]), x["T"]) for x in g.games]
        out = []
        for _ in range(B):
            s = rng.sample(recs, k)
            n = sum(a for a, _b, _c in s)
            d = sum(b for _a, b, _c in s)
            L = sum(c for _a, _b, c in s) / k
            out.append((n / d if d else None, L))
        return out
    su, st = sub(US), sub(TOP)
    for lab, s in (("US", su), ("TOP", st)):
        v = sorted(x[0] for x in s)
        print(f"     {lab}: median {v[len(v)//2]:.2f}   2.5% {v[int(.025*len(v))]:.2f}   "
              f"97.5% {v[int(.975*len(v))]:.2f}   min {v[0]:.2f} max {v[-1]:.2f}")
    rr = sorted(a[0] / b[0] for a, b in zip(su, st))
    print(f"     US/TOP ratio at n=120/group: median {rr[len(rr)//2]:.2f}x   "
          f"2.5% {rr[int(.025*len(rr))]:.2f}x   97.5% {rr[int(.975*len(rr))]:.2f}x   "
          f"max {rr[-1]:.2f}x")
    above = sum(1 for x in rr if x >= 2.28) / len(rr)
    print(f"     P(sampled ratio >= 2.28x | full population) = {above:.4f}")

    print("\n  -- is the sampled pooled ratio driven by the sample's MEAN GAME LENGTH?")
    for lab, s in (("US", su), ("TOP", st)):
        xs = [x[1] for x in s]
        ys = [x[0] for x in s]
        mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
        cov = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
        vx = sum((a - mx) ** 2 for a in xs) ** .5
        vy = sum((b - my) ** 2 for b in ys) ** .5
        print(f"     {lab}: r(mean game length, pooled rounds/build) = {cov/(vx*vy):+.3f}   "
              f"(mean length {mx:.0f})")

    print("\n  -- one game per match (the doc says Instrument B sampled one game per match):")
    for lab, g, sel in (("US", US, us_sel), ("TOP", TOP, top_sel)):
        first = [x for x in sel if x[0].endswith("_game_1.replay26")]
        h, _, _, _ = run_group(lab + "-g1", first)
        n, d, r = pooled(h)
        print(f"     {lab}: n={len(h.games):,}  ROUNDS/BUILD {r:.2f}")


def decode_keyed(sel):
    """Decode once, keep the file identity, return light per-game records."""
    args = [(f, o, t, None) for f, o, t, _r in sel]
    meta = {f: r for f, _o, _t, r in sel}
    sides_of = {f: (o, t) for f, o, t, _r in sel}
    out = []
    with Pool(processes=min(8, os.cpu_count() or 4)) as pool:
        for res in pool.imap_unordered(worker, args, chunksize=32):
            if res is None or res[0] == "ERR":
                continue
            _ok, fn, T, rec, _w, our_side, top_sides, _e = res
            sides = [our_side] if our_side is not None else list(top_sides)
            n = sum(sum(rec[s]["fr"].values()) for s in sides)
            d = sum(sum(rec[s]["fb"].values()) for s in sides)
            out.append(dict(file=fn, T=T, n=n, d=d, meta=meta[fn],
                            nsides=len(sides)))
    return out


def show(label, recs):
    n = sum(r["n"] for r in recs)
    d = sum(r["d"] for r in recs)
    g = len(recs)
    if not g:
        print(f"    {label:<34} n=0")
        return
    L = sum(r["T"] for r in recs) / g
    print(f"    {label:<34} games {g:>6,}  rounds/game {n/g:>7.1f}  builds/game {d/g:>6.2f}"
          f"  ROUNDS/BUILD {fmt_ratio(ratio(n, d))}  meanlen {L:>5.0f}")


def main_diag():
    us_sel, top_sel = select()
    US = decode_keyed(us_sel)
    TOP = decode_keyed(top_sel)
    print("=" * 110)
    print("CONTROL 4 FOLLOW-UP — which cut, if any, reproduces the queue doc's "
          "Instrument B (US 54.55 / TOP 23.93)?")
    print("=" * 110)
    print("  BY GAME INDEX WITHIN THE MATCH (a match is 5 games; the doc says "
          "Instrument B sampled ONE game per match):")
    for lab, recs in (("US", US), ("TOP", TOP)):
        print(f"   {lab}:")
        for gi in range(1, 6):
            show(f"game_{gi}", [r for r in recs if r["file"].endswith(f"_game_{gi}.replay26")])
        show("ALL games", recs)
    print("\n  TOP BY TEAM (a side is counted for each TOP team in the game):")
    for team in sorted(TOP_TEAMS):
        show(team, [r for r in TOP
                    if team in (r["meta"]["teamAName"], r["meta"]["teamBName"])])
    print("\n  TOP BY GAME COMPOSITION:")
    show("TOP vs non-TOP", [r for r in TOP if r["nsides"] == 1])
    show("TOP vs TOP (both sides counted)", [r for r in TOP if r["nsides"] == 2])
    print("\n  LADDER vs UNRATED (both populations pool them; the primary does not "
          "control this):")
    for lab, recs in (("US", US), ("TOP", TOP)):
        for trig in ("ladder", "unrated"):
            show(f"{lab} {trig}", [r for r in recs if r["meta"]["triggeredBy"] == trig])
    print("\n  US BY OUR BOT VERSION (47 distinct versions in the pool):")
    vc = Counter(ourver(r["meta"]) for r in US)
    for v, _n in vc.most_common(8):
        show(f"US v{v}", [r for r in US if ourver(r["meta"]) == v])
    print("\n  US BY GAME LENGTH DECILE (the composition channel):")
    srt = sorted(US, key=lambda r: r["T"])
    for i in range(10):
        chunk = srt[i * len(srt) // 10:(i + 1) * len(srt) // 10]
        show(f"US len decile {i+1}", chunk)
    srt = sorted(TOP, key=lambda r: r["T"])
    for i in range(10):
        chunk = srt[i * len(srt) // 10:(i + 1) * len(srt) // 10]
        show(f"TOP len decile {i+1}", chunk)


def ourver(r):
    return r["teamAVersion"] if r["teamAId"] == OURS else r["teamBVersion"]


def main_sens():
    """Sensitivity cuts.  Both populations pool LADDER with UNRATED games and ours
    spans 47 bot versions; neither is controlled in the primary.  Decided by me,
    not commissioned — flagged as such in the report."""
    us_sel, top_sel = select()
    cuts = [
        ("US all", [x for x in us_sel]),
        ("US ladder", [x for x in us_sel if x[3]["triggeredBy"] == "ladder"]),
        ("US unrated", [x for x in us_sel if x[3]["triggeredBy"] == "unrated"]),
        ("US v104", [x for x in us_sel if ourver(x[3]) == "104"]),
        ("TOP all", [x for x in top_sel]),
        ("TOP ladder", [x for x in top_sel if x[3]["triggeredBy"] == "ladder"]),
        ("TOP unrated", [x for x in top_sel if x[3]["triggeredBy"] == "unrated"]),
        ("TOP vs non-TOP only", [x for x in top_sel if len(x[2]) == 1]),
        ("TOP ladder vs non-TOP", [x for x in top_sel
                                   if len(x[2]) == 1 and x[3]["triggeredBy"] == "ladder"]),
    ]
    print("=" * 100)
    print("SENSITIVITY — ladder/unrated pooling and our version mix (doctrine bands, primary framing)")
    print("=" * 100)
    for label, sel in cuts:
        g, e, s, sc = run_group(label, sel)
        print()
        print(band_table(g, "doctrine", nres=400, title=label))


if __name__ == "__main__":
    if "--diag" in sys.argv:
        main_diag()
    elif "--repro" in sys.argv:
        main_repro()
    elif "--sens" in sys.argv:
        main_sens()
    else:
        main()
