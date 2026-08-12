#!/usr/bin/env python3
"""ARE THE ~5 BUILDERS ALIVE AT CORE DEATH ACTUALLY *IDLE*?

s31, research subagent, 2026-08-11.  READ-ONLY: decodes replay_archive/*.replay26
plus corpus/meta_join.tsv and corpus/events.tsv.  Writes nothing but stdout.

The anchor (docs/research/CORE-DEATH-BUILDER-STATE-2026-08-11.md) measured that
~5 of our builders are ALIVE when our core dies.  It did NOT measure that they
are IDLE.  This script classifies every one of OUR builder-rounds in the window
[T-20, T], T = the round a core is destroyed, into:

  A  IDLE AND FREE     actionCooldown == 0 and moveCooldown == 0 (both READ off
                       SetActionCooldown / SetMoveCooldown, not inferred) and the
                       unit emitted NO verb that round -- no MoveBuilderBot (2),
                       no BuilderBuild (16) / BuilderAttack (13) / BuilderHeal (15).
  B  ACTIVE, HOME      emitted a verb, d2_enemy >= d2_own at round start.
  C  ACTIVE, FORWARD   emitted a verb, d2_enemy <  d2_own at round start.
  D  ON COOLDOWN       no verb, and either cooldown > 0 at round start.

"Did nothing" is READ, not inferred: the verb updates are per-unit and explicit
on the wire (tools/replay_schema.md), and so are both cooldowns.

Forward test and core geometry inherited verbatim from scratchpad/dwell.py.
Seat keyed on meta_join teamAId/teamBId (corpus-howto TRAP 7: never us_side).
"""
from __future__ import annotations

import csv
import os
import statistics
import sys
from collections import Counter, defaultdict
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
sys.path.insert(0, "tools")
from replay_census import fields, read_pos, KIND_FIELDS, WIRE_LEN  # noqa: E402

AR = Path("replay_archive")
OURS = "379a5d80-9921-4c9e-949b-f9b1dcba16be"
WIN_BACK = 20          # window is [T-WIN_BACK, T] inclusive
CTRL_ROUND = 60        # control 2: early round, raiders known active forward
CTRL_BACK = 20

VERB_UPDATES = {2: "move", 13: "attack", 15: "heal", 16: "build"}


# ---------------------------------------------------------------- seats
def load_sides():
    """file -> our replay team index (0/1), keyed on teamAId/teamBId ONLY."""
    side = {}
    with open("corpus/meta_join.tsv") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            if r["teamAId"] == OURS:
                side[r["file"]] = 0
            elif r["teamBId"] == OURS:
                side[r["file"]] = 1
    return side


# ---------------------------------------------------------------- entity parse
def parse_ent(buf):
    """(id, team, pos, kind, act_cd, mv_cd) -- cooldowns only for builder bots."""
    eid = team = 0
    pos = kind = None
    acd = mcd = 0
    for num, wire, value in fields(buf):
        if num == 1:
            eid = value
        elif num == 2:
            team = value
        elif num == 3:
            pos = read_pos(value)
        elif num in KIND_FIELDS:
            kind = KIND_FIELDS[num]
            if kind == "builder_bot" and wire == WIRE_LEN and value:
                d = {a: b for a, _c, b in fields(value)}
                acd, mcd = d.get(1, 0), d.get(2, 0)
    if kind is None or pos is None:
        return None
    return eid, team, pos, kind, acd, mcd


# ---------------------------------------------------------------- the walk
def walk(path, our):
    data = path.read_bytes()
    mapbuf = None
    turns = []
    for n, w, v in fields(data):
        if n == 1 and w == WIRE_LEN:
            mapbuf = v
        elif n == 3 and w == WIRE_LEN:
            turns.append(v)
    if mapbuf is None:
        return {"err": "no map"}
    cores = []
    for n, w, v in fields(mapbuf):
        if n == 4 and w == WIRE_LEN:
            d = {a: b for a, _c, b in fields(v)}
            cores.append((d.get(1, 0), d.get(2, 0), read_pos(d[3])))
    home, core_team = {}, {}
    for cid, t, p in cores:
        home.setdefault(t, p)
        core_team[cid] = t
    if 0 not in home or 1 not in home:
        return {"err": "cores"}

    def d2(a, b):
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

    def fwd(p, t):
        return d2(p, home[1 - t]) < d2(p, home[t])

    pos, team, kind = {}, {}, {}
    # Cores are NEVER emitted as an update (tools/replay_schema.md) -- seed them
    # from map.cores or removeEntity on a core id has nothing to remove.
    for cid, t, p in cores:
        pos[cid], team[cid], kind[cid] = p, t, "core"
    acd, mcd = {}, {}
    core_deaths = []            # (round, team_of_core)
    ti = {0: 0, 1: 0}
    cdvals = Counter()          # (7|8, value) -> n, builder bots only
    spawncd = Counter()         # (actionCd, moveCd) at placement, our builders

    # per-round snapshot of what we need, only for our team's builders
    rec = {}                    # rnd -> list of (bid, bucket)
    alive_start = {}            # rnd -> n our builders alive at round start
    alive_end = {}              # rnd -> n our builders alive at round end
    ti_at = {}                  # rnd -> our titanium at round end
    anomalies = 0
    vk = defaultdict(list)      # rnd -> [(bucket, verb)]

    for rnd, tb in enumerate(turns):
        # ---- round-start snapshot (before this round's updates)
        start_pos = {i: p for i, p in pos.items()
                     if kind.get(i) == "builder_bot" and team.get(i) == our}
        start_acd = {i: acd.get(i, 0) for i in start_pos}
        start_mcd = {i: mcd.get(i, 0) for i in start_pos}
        alive_start[rnd] = len(start_pos)
        moved, acted = set(), set()
        tled, ran = set(), set()
        died = set()
        which = {}

        for _a, _b, ub in fields(tb):
            for un, _w, ubuf in fields(ub):
                if un == 1:
                    for en, _e, eb in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_ent(eb)
                        if e is None:
                            continue
                        eid, t, p, k, a0, m0 = e
                        pos[eid] = p
                        team[eid] = t
                        kind[eid] = k
                        if k == "builder_bot":
                            acd[eid] = a0
                            mcd[eid] = m0
                            spawncd[(a0, m0)] += 1
                elif un == 2:
                    d = {k: v for k, _x, v in fields(ubuf)}
                    if 1 in d and 2 in d:
                        if d[1] in pos:
                            pos[d[1]] = read_pos(d[2])
                        moved.add(d[1])
                elif un in (13, 15, 16):
                    d = {k: v for k, _x, v in fields(ubuf)}
                    if 1 in d:
                        acted.add(d[1])
                        which.setdefault(d[1], set()).add(
                            {13: "attack", 15: "heal", 16: "build"}[un])
                elif un == 9:
                    d = {k: v for k, _x, v in fields(ubuf)}
                    if 1 in d:
                        ran.add(d[1])
                        if d.get(4, 0):
                            tled.add(d[1])
                elif un == 3:
                    for _rn, _rw, rv in fields(ubuf):
                        died.add(rv)
                        if kind.get(rv) == "core":
                            core_deaths.append((rnd, team.get(rv, core_team.get(rv))))
                        pos.pop(rv, None)
                        team.pop(rv, None)
                        kind.pop(rv, None)
                        acd.pop(rv, None)
                        mcd.pop(rv, None)
                elif un in (7, 8):
                    d = {k: v for k, _x, v in fields(ubuf)}
                    if 1 in d:
                        (acd if un == 7 else mcd)[d[1]] = d.get(2, 0)
                        if kind.get(d[1]) == "builder_bot":
                            cdvals[(un, d.get(2, 0))] += 1
                elif un == 6:
                    for pn, _pw, pv in fields(ubuf):
                        if pn != 1:
                            continue
                        for sn, _sw, sv in fields(pv):
                            if sn in (1, 2):
                                dd = {k: v for k, _x, v in fields(sv)}
                                ti[sn - 1] = dd.get(1, 0)

        # ---- classify this round's builder-rounds
        out = []
        for bid, p in start_pos.items():
            vmask = (1 if bid in moved else 0) | (2 if bid in acted else 0)
            cd_block = start_acd[bid] > 0 or start_mcd[bid] > 0
            f = fwd(p, our)
            # flags: bit0 forward, bit1 tled this round, bit2 died this round,
            # bit3 the engine ran its code at all (a BotOutput was emitted)
            fl = ((1 if f else 0) | (2 if bid in tled else 0)
                  | (4 if bid in died else 0) | (8 if bid in ran else 0))
            vk[rnd].extend((("C" if f else "B"), _wv) for _wv in which.get(bid, ()))
            if vmask:
                if cd_block:
                    anomalies += 1
                out.append((bid, "C" if f else "B", vmask, fl))
            elif cd_block:
                out.append((bid, "D", 0, fl))
            else:
                out.append((bid, "A", 0, fl))
        rec[rnd] = out
        alive_end[rnd] = sum(1 for i in pos
                             if kind.get(i) == "builder_bot" and team.get(i) == our)
        ti_at[rnd] = ti[our]

        # ---- end of round: cooldowns tick down by 1
        for dct in (acd, mcd):
            for i in list(dct):
                if dct[i] > 0:
                    dct[i] -= 1

    return {"rec": rec, "alive_start": alive_start, "alive_end": alive_end,
            "core_deaths": core_deaths, "nturns": len(turns), "ti": ti_at,
            "anom": anomalies, "cdvals": cdvals, "spawncd": spawncd, "vk": vk}


# ---------------------------------------------------------------- per-game reduce
def summarise(w, our, T):
    """Bucket counters for the window ending at T, plus per-builder A-share."""
    lo = max(0, T - WIN_BACK)
    win_rounds = list(range(lo, T + 1))
    bucket_rounds = Counter()
    vsplit = Counter()                 # (bucket, vmask) -> n
    per_builder = defaultdict(Counter)
    act_rounds = defaultdict(list)     # bid -> rounds with a BUILD/ATTACK/HEAL
    fwd_all = [0, 0]                   # [forward builder-rounds, all]
    prof = Counter()                   # offset from T -> (n_A, n_all)
    profn = Counter()
    flags = Counter()                  # (bucket, flagname) -> n
    verbkind = Counter()               # (bucket, verb) -> n, in-window
    for r in win_rounds:
        for bid, k, vmask, fl in w["rec"].get(r, ()):
            f = fl & 1
            bucket_rounds[k] += 1
            per_builder[bid][k] += 1
            fwd_all[1] += 1
            fwd_all[0] += 1 if f else 0
            if fl & 2:
                flags[(k, "tled")] += 1
            if fl & 4:
                flags[(k, "died")] += 1
            if not fl & 8:
                flags[(k, "no_botoutput")] += 1
            profn[r - T] += 1
            if k == "A":
                prof[r - T] += 1
            if k in "BC":
                vsplit[(k, vmask)] += 1
            if vmask & 2:
                act_rounds[bid].append(r)
    for r in win_rounds:
        for bk in w["vk"].get(r, ()):
            verbkind[bk] += 1
    gaps = Counter()
    for bid, rr in act_rounds.items():
        for a, b in zip(rr, rr[1:]):
            gaps[min(b - a, 9)] += 1
    # headcount at T-1 (the anchor round)
    head = Counter(k for _b, k, _v, _f in w["rec"].get(max(T - 1, 0), ()))
    headv = Counter((k, vmask) for _b, k, vmask, _f in w["rec"].get(max(T - 1, 0), ()))
    alive_T1_start = w["alive_start"].get(max(T - 1, 0), 0)
    alive_T1_end = w["alive_end"].get(max(T - 1, 0), 0)
    # persistent idleness among builders alive at T-1
    live = {b for b, _k, _v, _f in w["rec"].get(max(T - 1, 0), ())}
    shares = []
    for b in live:
        c = per_builder[b]
        tot = sum(c.values())
        if tot:
            shares.append(c["A"] / tot)
    return dict(bucket_rounds=bucket_rounds, head=head, headv=headv,
                vsplit=vsplit, gaps=gaps, fwd_all=fwd_all, flags=flags,
                verbkind=verbkind,
                prof=prof, profn=profn,
                alive_T1_start=alive_T1_start, alive_T1_end=alive_T1_end,
                shares=shares, n_win_rounds=len(win_rounds),
                ti_T1=w["ti"].get(max(T - 1, 0), 0))


def worker(arg):
    fn, our = arg
    try:
        w = walk(AR / fn, our)
    except Exception as exc:                                     # noqa: BLE001
        return ("ERR", fn, repr(exc))
    if "err" in w:
        return ("ERR", fn, w["err"])
    cd = w["core_deaths"]
    if len(cd) != 1:
        return ("SKIP", fn, len(cd))
    T, dead_team = cd[0]
    arm = "LOSS" if dead_team == our else "WIN"
    main = summarise(w, our, T)
    ctrl = None
    if w["nturns"] > CTRL_ROUND and T > CTRL_ROUND:
        ctrl = summarise(w, our, CTRL_ROUND)
    early = summarise(w, our, 10) if T > 10 else None
    return ("OK", fn, arm, T, main, ctrl, early, w["anom"], w["cdvals"], w["spawncd"])


# ---------------------------------------------------------------- reporting
def pct(n, d):
    return f"{100.0*n/d:6.2f}%" if d else "   n/a"


def anchor_from_events(side):
    """CONTROL 1a: the ANCHOR's own instrument -- corpus/events.tsv, builder
    BUILD/DEATH counted up to T-1, T from the DEATH/core row."""
    core = {}                       # file -> [(rnd, team)]
    builds = defaultdict(list)      # (file, team) -> [rnd]
    deaths = defaultdict(list)
    with open("corpus/events.tsv") as fh:
        rd = csv.reader(fh, delimiter="\t")
        next(rd)
        for row in rd:
            f = row[0]
            if f not in side:
                continue
            ev, rnd, team, kind = row[1], int(row[2]), int(row[3]), row[4]
            if kind == "core":
                if ev == "DEATH":
                    core.setdefault(f, []).append((rnd, team))
            elif kind == "builder_bot":
                (builds if ev == "BUILD" else deaths)[(f, team)].append(rnd)
    out = {"LOSS": [], "WIN": []}
    Ts = {"LOSS": [], "WIN": []}
    for f, cds in core.items():
        if len(cds) != 1:
            continue
        T, dead = cds[0]
        our = side[f]
        arm = "LOSS" if dead == our else "WIN"
        cut = T - 1
        n = (sum(1 for r in builds[(f, our)] if r <= cut)
             - sum(1 for r in deaths[(f, our)] if r <= cut))
        out[arm].append(n)
        Ts[arm].append(T)
    return out, Ts


def bucket_table(label, rows, key):
    tot = Counter()
    for r in rows:
        tot.update(r[key]["bucket_rounds"])
    n = sum(tot.values())
    print(f"  {label}  games={len(rows)}  builder-rounds={n:,}")
    for b, name in (("A", "IDLE AND FREE"), ("B", "ACTIVE, HOME"),
                    ("C", "ACTIVE, FORWARD"), ("D", "ON COOLDOWN")):
        print(f"     {b}  {name:<18} {tot[b]:>9,}  {pct(tot[b], n)}")
    return tot, n


def head_table(label, rows, key):
    n = len(rows)
    print(f"  {label}  n={n} games -- MEAN HEADCOUNT at T-1 (per game)")
    tot = Counter()
    for r in rows:
        tot.update(r[key]["head"])
    for b, name in (("A", "IDLE AND FREE"), ("B", "ACTIVE, HOME"),
                    ("C", "ACTIVE, FORWARD"), ("D", "ON COOLDOWN")):
        print(f"     {b}  {name:<18} mean {tot[b]/n:6.2f} builders/game")
    print(f"     TOTAL alive                mean {sum(tot.values())/n:6.2f}")
    return tot


def main():
    side = load_sides()
    files = sorted(side)
    print(f"population: {len(files)} archived games with us on a side "
          f"(meta_join, keyed on teamAId/teamBId)")

    args = [(f, side[f]) for f in files]
    res = []
    errs = Counter()
    skips = Counter()
    with Pool(os.cpu_count()) as pool:
        for r in pool.imap_unordered(worker, args, chunksize=16):
            if r[0] == "ERR":
                errs[r[2]] += 1
            elif r[0] == "SKIP":
                skips[r[2]] += 1
            else:
                res.append(r)
    print(f"parse failures: {sum(errs.values())}  {dict(errs)}")
    print(f"skipped (core-death count != 1): {sum(skips.values())}  "
          f"by n_core_deaths {dict(sorted(skips.items()))}")

    arms = {"LOSS": [], "WIN": []}
    anom = 0
    cdvals, spawncd = Counter(), Counter()
    for _ok, fn, arm, T, main_s, ctrl_s, early_s, a, cv, sc in res:
        anom += a
        cdvals.update(cv)
        spawncd.update(sc)
        arms[arm].append({"file": fn, "T": T, "main": main_s, "ctrl": ctrl_s,
                          "early": early_s})
    print(f"games with exactly one core death: {len(res)}  "
          f"LOSS={len(arms['LOSS'])}  WIN={len(arms['WIN'])}")
    print(f"anomalous builder-rounds (verb emitted while cooldown>0): {anom}")

    # ---------------- CONTROL 1: reproduce the anchor
    print("\n=== CONTROL 1 -- REPRODUCE THE ANCHOR (median 5.0 / mean 4.43 loss, "
          "mean 5.20 win) ===")
    ev_alive, ev_T = anchor_from_events(side)
    for arm in ("LOSS", "WIN"):
        v = ev_alive[arm]
        print(f"  [1a events.tsv, the anchor's OWN instrument] {arm:<4} n={len(v)}  "
              f"median {statistics.median(v):.1f}  mean {statistics.mean(v):.2f}   "
              f"T median {statistics.median(ev_T[arm]):.0f}")
    for arm in ("LOSS", "WIN"):
        rows = arms[arm]
        for tag in ("alive_T1_start", "alive_T1_end"):
            v = [r["main"][tag] for r in rows]
            print(f"  {arm:<4} OUR builders alive at T-1 ({tag:<14}) "
                  f"n={len(v)}  median {statistics.median(v):.1f}  "
                  f"mean {statistics.mean(v):.2f}")
        Ts = [r["T"] for r in rows]
        print(f"  {arm:<4} decisive round T   median {statistics.median(Ts):.0f}")

    # ---------------- the bucket tables
    print("\n=== BUCKET SHARES -- builder-rounds over the window [T-20, T] ===")
    for arm in ("LOSS", "WIN"):
        bucket_table(arm, arms[arm], "main")

    print("\n=== HEADCOUNT AT T-1 ===")
    for arm in ("LOSS", "WIN"):
        head_table(arm, arms[arm], "main")

    print("\n=== DISTRIBUTION OF THE 'IDLE AND FREE' HEADCOUNT AT T-1 "
          "(how many games have anything to redirect at all?) ===")
    for arm in ("LOSS", "WIN"):
        rows = arms[arm]
        v = sorted(r["main"]["head"]["A"] for r in rows)
        n = len(v)
        hist = Counter(min(x, 6) for x in v)
        print(f"  {arm:<4} n={n}  median {statistics.median(v):.1f}  "
              f"mean {statistics.mean(v):.2f}   "
              + "  ".join(f"{k}{'+' if k == 6 else ''}:{pct(hist[k], n).strip()}"
                          for k in sorted(hist)))

    print("\n=== PERSISTENTLY IDLE -- of the builders alive at T-1, what share of "
          "the 21-round window were they in bucket A? ===")
    for arm in ("LOSS", "WIN"):
        rows = arms[arm]
        allsh = [s for r in rows for s in r["main"]["shares"]]
        n = len(rows)
        h50 = sum(1 for r in rows for s in r["main"]["shares"] if s >= 0.5)
        h80 = sum(1 for r in rows for s in r["main"]["shares"] if s >= 0.8)
        h20 = sum(1 for r in rows for s in r["main"]["shares"] if s < 0.2)
        print(f"  {arm:<4} builders={len(allsh):,}  mean A-share {statistics.mean(allsh):.3f}"
              f"  median {statistics.median(allsh):.3f}")
        print(f"       mean per game: A-share>=0.8 {h80/n:5.2f}   >=0.5 {h50/n:5.2f}"
              f"   <0.2 {h20/n:5.2f}   builders/game")

    # ---------------- CONTROL 2: the same classifier at r60
    print("\n=== HEADCOUNT AT T-1, SPLIT BY WHICH VERB -- move-only is cheap to "
          "redirect, build/attack/heal is a committed turn ===")
    for arm in ("LOSS", "WIN"):
        rows = arms[arm]
        n = len(rows)
        hv = Counter()
        for r in rows:
            hv.update(r["main"]["headv"])
        for b in ("B", "C"):
            print(f"  {arm:<4} {b}: move-only {hv[(b,1)]/n:5.2f}   "
                  f"act(build/attack/heal) {(hv[(b,2)]+hv[(b,3)])/n:5.2f}  builders/game")

    print(f"\n=== CONTROL 2 -- SAME CLASSIFIER AT r{CTRL_ROUND} (window "
          f"[{CTRL_ROUND-CTRL_BACK}, {CTRL_ROUND}]) and at r10 (window [0,10]) ===")
    for key, lab in (("ctrl", f"r{CTRL_ROUND}"), ("early", "r10")):
        for arm in ("LOSS", "WIN"):
            rows = [r for r in arms[arm] if r[key]]
            if not rows:
                continue
            bucket_table(f"{arm} @{lab}", rows, key)
            n = len(rows)
            tot = Counter()
            for r in rows:
                tot.update(r[key]["head"])
            print("     headcount: " + "  ".join(
                f"{b} {tot[b]/n:.2f}" for b in "ABCD")
                + f"   TOTAL {sum(tot.values())/n:.2f}")

    print("\n=== CONTROL 2b -- FORWARD SHARE OF *ALL* BUILDER-ROUNDS (verb-blind), "
          "so a flat C can be told apart from a broken classifier ===")
    for key, lab in (("main", "[T-20,T]"), ("ctrl", "[40,60]"), ("early", "[0,10]")):
        for arm in ("LOSS", "WIN"):
            rows = [r for r in arms[arm] if r[key]]
            if not rows:
                continue
            f = sum(r[key]["fwd_all"][0] for r in rows)
            a = sum(r[key]["fwd_all"][1] for r in rows)
            print(f"  {arm:<4} {lab:<9} forward builder-rounds {f:>8,} / {a:>8,} = {pct(f, a)}")

    print("\n=== PER-ROUND PROFILE OF BUCKET A (share of builder-rounds idle), "
          "by offset from T ===")
    for arm in ("LOSS", "WIN"):
        prof = Counter()
        profn = Counter()
        for r in arms[arm]:
            prof.update(r["main"]["prof"])
            profn.update(r["main"]["profn"])
        line = "  ".join(f"{o:+d}:{100.0*prof[o]/profn[o]:.0f}%"
                         for o in range(-20, 1) if profn[o])
        print(f"  {arm:<4} {line}")

    # ---------------- CONTROL 3: cooldowns
    print("\n=== VERB SPLIT INSIDE B AND C -- move-only is cheap to redirect, "
          "build/attack/heal is not ===")
    for arm in ("LOSS", "WIN"):
        vs = Counter()
        for r in arms[arm]:
            vs.update(r["main"]["vsplit"])
        n = sum(vs.values())
        for b in ("B", "C"):
            mo, ac, both = vs[(b, 1)], vs[(b, 2)], vs[(b, 3)]
            t = mo + ac + both
            print(f"  {arm:<4} {b}: move-only {mo:>8,} ({pct(mo,t)})   "
                  f"act-only {ac:>8,} ({pct(ac,t)})   both {both:>7,} ({pct(both,t)})")

    print("\n=== WHICH ACTION are the ACTIVE builder-rounds spending, window "
          "[T-20,T] (one round can carry only one action) ===")
    for arm in ("LOSS", "WIN"):
        vk = Counter()
        for r in arms[arm]:
            vk.update(r["main"]["verbkind"])
        for b in ("B", "C"):
            t = sum(n for (bb, _v), n in vk.items() if bb == b)
            print(f"  {arm:<4} {b}: " + "   ".join(
                f"{v} {vk[(b, v)]:>7,} ({pct(vk[(b, v)], t)})"
                for v in ("build", "attack", "heal")))

    print("\n=== CONTROL 4 -- WHY ELSE COULD A BUILDER-ROUND LOOK IDLE? "
          "TLE / death-in-round / no BotOutput at all, per bucket, window [T-20,T] ===")
    for arm in ("LOSS", "WIN"):
        tot = Counter()
        fl = Counter()
        for r in arms[arm]:
            tot.update(r["main"]["bucket_rounds"])
            fl.update(r["main"]["flags"])
        for b in "ABCD":
            if not tot[b]:
                continue
            print(f"  {arm:<4} {b}: n={tot[b]:>8,}   tled {fl[(b,'tled')]:>6,} "
                  f"({pct(fl[(b,'tled')], tot[b])})   died-that-round "
                  f"{fl[(b,'died')]:>5,} ({pct(fl[(b,'died')], tot[b])})   "
                  f"no BotOutput {fl[(b,'no_botoutput')]:>6,} "
                  f"({pct(fl[(b,'no_botoutput')], tot[b])})")

    print("\n=== CONTROL 3 -- COOLDOWN SANITY ===")
    print(f"  every SetActionCooldown value ever written for a builder bot "
          f"(field 7): {dict(sorted((v, n) for (u, v), n in cdvals.items() if u == 7))}")
    print(f"  every SetMoveCooldown   value ever written for a builder bot "
          f"(field 8): {dict(sorted((v, n) for (u, v), n in cdvals.items() if u == 8))}")
    print(f"  (actionCooldown, moveCooldown) at PLACEMENT, all builder bots: "
          f"{dict(spawncd)}")
    for arm in ("LOSS", "WIN"):
        tot = Counter()
        gaps = Counter()
        for r in arms[arm]:
            tot.update(r["main"]["bucket_rounds"])
            gaps.update(r["main"]["gaps"])
        n = sum(tot.values())
        print(f"  {arm}: builder-rounds with a cooldown>0 at ROUND START and no "
              f"verb (bucket D): {tot['D']:,} / {n:,} = {pct(tot['D'], n)}")
        g = sum(gaps.values())
        print(f"        gap in rounds between one builder's consecutive "
              f"BUILD/ATTACK/HEAL actions, in-window (n={g:,}): "
              + "  ".join(f"{k}:{pct(gaps[k], g).strip()}" for k in sorted(gaps)))

    # ---------------- context: titanium
    print("\n=== CONTEXT -- our global titanium at T-1 ===")
    for arm in ("LOSS", "WIN"):
        v = sorted(r["main"]["ti_T1"] for r in arms[arm])
        q = statistics.quantiles(v, n=4)
        print(f"  {arm:<4} median {statistics.median(v):.0f}  mean {statistics.mean(v):.1f}"
              f"  q1 {q[0]:.0f}  q3 {q[2]:.0f}  share>=100 "
              f"{pct(sum(1 for x in v if x >= 100), len(v))}")


if __name__ == "__main__":
    main()
