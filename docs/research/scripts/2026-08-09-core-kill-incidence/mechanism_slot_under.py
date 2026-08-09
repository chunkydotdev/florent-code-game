#!/usr/bin/env python3
"""PRE-REGISTERED MECHANISM TEST -- "the shelled core pins our raiders at home".

THE HYPOTHESIS AS HANDED TO ME (builder arm, 2026-08-09)
-------------------------------------------------------
A raider within `dsq 25` of a DAMAGED home core heals it and RETURNS from run()
before `_raid` is ever called -- no move, no raid, that round. `SLOT_UNDER` is a
50-round latch re-armed by enemy fire. Against an opponent that shells our core
continuously the latch never clears, so our raiders never leave home, and we
almost never land a core kill.

Predicted signature, all three parts:
  (1) DOSE-RESPONSE   more enemy fire at our core -> fewer of our builder-bot
                      position samples outside d2=25 of our own core.
  (2) DISCONTINUITY   a STEP at d2 = 25, not a smooth gradient.
  (3) PERSISTENCE     suppression lasting ~50 rounds after the last arming event,
                      not tracking fire contemporaneously.
Plus a within-game PLACEBO: the heal only fires when the core is DAMAGED, so the
suppression must be ABSENT while our core sits at full HP.

WHAT THIS DECODER MEASURES
--------------------------
Per round, for every builder bot of OURS that was alive at the START of the round:
its d2 to our own core BEFORE it moved, and whether a moveBuilderBot was emitted
for it that round. Cross-tabulated by:
    d2 bucket  x  core damaged (HP < max)  x  rounds since our core last lost HP
That gives P(move) as a function of distance, conditioned on exactly the two
state bits the hypothesised code path reads.

Our core's HP is tracked from its initial max_hp and Update field 5 (updateHp),
whose `delta` is a 64-bit TWO'S-COMPLEMENT varint (18446744073709551609 == -7).
Both signs are counted and reported, per the standing trap.

Note that `moveBuilderBot` is the mobility ground truth -- the same stream
replay_throws.py reads -- so "did not move" here includes both "chose not to
move" and "was on move cooldown". The placebo split is what separates those:
cooldown does not care whether our core is damaged.

Usage: mechanism_slot_under.py OUTPREFIX FILE [FILE ...]
Emits OUTPREFIX.moves.tsv and OUTPREFIX.games.tsv
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa: E402

TWO64 = 1 << 64
LATCH_BUCKETS = [(0, 1), (1, 5), (5, 10), (10, 25), (25, 50), (50, 75),
                 (75, 150), (150, 10 ** 9)]


def latch_bucket(age):
    if age is None:
        return "never"
    for lo, hi in LATCH_BUCKETS:
        if lo <= age < hi:
            return f"{lo}-{hi}" if hi < 10 ** 9 else f"{lo}+"
    return "?"


def d2b(d):
    """Exact d2 up to 60 (so a step at 25 is visible at 1-unit resolution),
    coarse above."""
    if d <= 60:
        return str(d)
    if d <= 100:
        return "61-100"
    if d <= 200:
        return "101-200"
    return "201+"


def census(path: Path, mv, gm) -> None:
    data = path.read_bytes()
    map_buf, turn_bufs = None, []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if map_buf is None:
        return
    cores = []
    for num, _w, value in fields(map_buf):
        if num == 4:
            c = {"id": 0, "team": 0, "pos": (0, 0)}
            for cn, _cw, cv in fields(value):
                if cn == 1:
                    c["id"] = cv
                elif cn == 2:
                    c["team"] = cv
                elif cn == 3:
                    c["pos"] = read_pos(cv)
            cores.append(c)
    if len(cores) != 2:
        return
    corepos = {c["team"]: c["pos"] for c in cores}
    coreid = {c["team"]: c["id"] for c in cores}

    bots: dict[int, tuple[int, tuple[int, int]]] = {}
    # Core HP: seeded from GameConstants (CORE_MAX_HP = 500) and corrected the
    # moment the core's own placeEntity arrives with its real hp/max_hp.
    hp = {0: 500, 1: 500}
    maxhp = {0: 500, 1: 500}
    last_dmg = {0: None, 1: None}
    neg = pos_ = 0
    acc: dict[tuple, list[int]] = {}
    gstats = {0: [0, 0, 0, 0], 1: [0, 0, 0, 0]}   # samples, outside25, sum_d2, dmg_rounds

    for rnd, turn_buf in enumerate(turn_bufs):
        # --- state at the START of the round
        pre = {bid: (t, p) for bid, (t, p) in bots.items()}
        pre_hp = dict(hp)
        pre_max = dict(maxhp)
        pre_age = {t: (None if last_dmg[t] is None else rnd - last_dmg[t]) for t in (0, 1)}
        moved = set()

        for _n, _w2, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        if e.kind == "core":
                            if e.max_hp:
                                maxhp[e.team] = e.max_hp
                            if e.hp:
                                hp[e.team] = e.hp
                        if e.id in bots:
                            bots[e.id] = (e.team, e.pos)
                            continue
                        if e.kind == "builder_bot":
                            bots[e.id] = (e.team, e.pos)
                elif unum == 2:
                    eid = to = None
                    for mn, _mw, mval in fields(ubuf):   # NB: not `mv` -- that is the file handle
                        if mn == 1:
                            eid = mval
                        elif mn == 2:
                            to = read_pos(mval)
                    if eid in bots and to:
                        if bots[eid][1] != to:
                            moved.add(eid)
                        bots[eid] = (bots[eid][0], to)
                elif unum == 3:
                    for _rn, _rw, rv in fields(ubuf):
                        bots.pop(rv, None)
                elif unum == 5:                       # updateHp
                    eid = delta = None
                    for hn, _hw, hv in fields(ubuf):
                        if hn == 1:
                            eid = hv
                        elif hn == 2:
                            delta = hv - TWO64 if hv > (1 << 63) else hv
                    if delta is None:
                        continue
                    if delta < 0:
                        neg += 1
                    elif delta > 0:
                        pos_ += 1
                    for t in (0, 1):
                        if eid == coreid[t] and hp[t] is not None:
                            hp[t] = max(0, min(maxhp[t] or 10 ** 9, hp[t] + delta))
                            if delta < 0:
                                last_dmg[t] = rnd

        # --- emit one sample per bot alive at the start of the round
        for bid, (t, p) in pre.items():
            c = corepos[t]
            d = (p[0] - c[0]) ** 2 + (p[1] - c[1]) ** 2
            mh, h = pre_max[t], pre_hp[t]
            dmg = 1 if (mh is not None and h is not None and h < mh) else 0
            key = (t, "r0-150" if rnd < 150 else "r150+", d2b(d), dmg,
                   latch_bucket(pre_age[t]))
            cell = acc.setdefault(key, [0, 0])
            cell[0] += 1
            cell[1] += 1 if bid in moved else 0
            g = gstats[t]
            g[0] += 1
            g[1] += 1 if d > 25 else 0
            g[2] += d
            g[3] += dmg

    name = path.name
    for (t, band, d, dmg, lb), (n, m) in acc.items():
        mv.write(f"{name}\t{t}\t{band}\t{d}\t{dmg}\t{lb}\t{n}\t{m}\n")
    for t in (0, 1):
        g = gstats[t]
        gm.write(f"{name}\t{t}\t{g[0]}\t{g[1]}\t{g[2]}\t{g[3]}\t"
                 f"{maxhp[t]}\t{hp[t]}\t{neg}\t{pos_}\n")


def main(argv):
    pre = argv[0]
    mv = open(pre + ".moves.tsv", "w")
    gm = open(pre + ".games.tsv", "w")
    mv.write("file\tteam\tband\td2\tcore_dmg\tlatch_age\tn\tmoved\n")
    gm.write("file\tteam\tsamples\toutside25\tsum_d2\tdmg_rounds\tmaxhp\tendhp\t"
             "hp_neg_events\thp_pos_events\n")
    bad = 0
    files = argv[1:]
    for i, p in enumerate(Path(x) for x in files):
        try:
            census(p, mv, gm)
        except Exception as exc:                     # noqa: BLE001
            bad += 1
            print(f"ERR {p.name}: {exc}", file=sys.stderr)
        if (i + 1) % 250 == 0:
            print(f"  ...{i+1}/{len(files)} ({bad} err)", file=sys.stderr, flush=True)
    mv.close(); gm.close()
    print(f"done {len(files)} files, {bad} errors", file=sys.stderr, flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
