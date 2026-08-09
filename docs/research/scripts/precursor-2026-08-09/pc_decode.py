#!/usr/bin/env python3
"""PRECURSOR decoder: enemy builder-bot tracks BEFORE an in-base turret plant.

Derived from docs/research/scripts/side-lane-2026-08-09/bb_decode.py (the
validated builder-bot position tracker).  WHAT CHANGED vs that file:

  * tracks EVERY entity's position/team/kind (bb_decode only kept builder bots
    plus the two cores), because we need enemy turret positions for the nest
    label and our own sensor positions for the visibility approximation;
  * adds per-round history (last 12 rounds) of every enemy builder's d2 to OUR
    core, its in-band flag, its move count and its visibility flag;
  * emits PLANT rows (one per enemy gunner/sentinel built at d2<=32 of our core)
    with the planting builder attributed by orthogonal adjacency at the moment
    the placeEntity is read, plus that builder's loiter/approach history;
  * emits EPISODE rows (one per maximal run of consecutive in-band rounds by an
    enemy builder) as the negative control;
  * drops all the core-damage/heal accounting bb_decode existed for.

Traps honoured (docs/research/corpus-howto.md):
  1. build = FIRST placeEntity carrying an id (rotate re-emits) -- guarded.
  2. updateHp.delta is a 64-bit two's-complement varint -- not used here.
  3. launcher throws are moveBuilderBot with |to-frm|>1 -- counted, flagged.

Read-only over replay_archive/ + corpus/.  Writes only into the scratchpad.
"""
from __future__ import annotations

import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game/tools")
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa: E402

BAND = 32           # d2 to our core's NW corner, matches corpus d2_enemy<=32
HIST = 12           # rounds of per-bot history kept
NEST_W = 30         # nest window, rounds
TURRETS = ("gunner", "sentinel", "launcher")
GS = ("gunner", "sentinel")
# vision radius squared, from CLAUDE.md
VIS = {"builder_bot": 20, "core": 36, "gunner": 13, "sentinel": 32,
       "launcher": 26}

PCOLS = ["file", "seat", "rnd", "kind", "x", "y", "d2", "reuse_idx",
         "pid", "ncand",
         "loiter", "band_total", "age", "ep_entry_d2", "ep_throw_in",
         "moves_w10", "netdisp_w10", "mind2_w10",
         "d2_m1", "d2_m2", "d2_m3", "d2_m5", "d2_m10",
         "nbots_m1", "nbots_w10", "nbots_max_w10", "nbots_loiter_max",
         "vis_core_m1", "vis_oth_m1", "vis_oth_frac", "vis_oth_any",
         "pre_t8", "pre_gs8", "new_t8_30", "new_gs8_30",
         "died", "drnd"]

ECOLS = ["file", "seat", "bid", "start", "end", "length", "mind2",
         "entry_d2", "throw_in", "moves", "nother_max", "vis_oth_frac",
         "planted", "plant_lag", "ended", "spawn_rnd"]


def d2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def decode(path: Path, our_team: int, pout, eout):
    data = path.read_bytes()
    map_buf, turn_bufs = None, []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if map_buf is None:
        return
    w = h = 0
    cores = []
    for num, wire, value in fields(map_buf):
        if num == 1:
            w = value
        elif num == 2:
            h = value
        elif num == 4:
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
    ours = corepos[our_team]
    them = 1 - our_team

    name = path.name
    pos_of = {c["id"]: c["pos"] for c in cores}
    team_of = {c["id"]: c["team"] for c in cores}
    kind_of = {c["id"]: "core" for c in cores}
    ebots = set()                    # live ENEMY builder bot ids
    sensors = {c["id"] for c in cores if c["team"] == our_team}   # our seeing units
    live_ids = set(pos_of)

    spawn_rnd = {}
    band_total = {}
    ep = {}          # bid -> dict(start, entry_d2, throw_in, mind2, vis_n, len)
    plants = []      # dicts, post-processed
    turret_builds = []   # (rnd, x, y, kind) for ENEMY turrets, whole map
    hist = deque(maxlen=HIST)   # per-round dicts
    reuse = {}
    move_this_round = {}
    throw_this_round = {}

    def vis_other(p):
        """Any of OUR non-core sensing units within its vision radius of p."""
        for sid in sensors:
            if kind_of.get(sid) == "core":
                continue
            sp = pos_of.get(sid)
            if sp is None:
                continue
            if d2(sp, p) <= VIS[kind_of[sid]]:
                return 1
        return 0

    for rnd, turn_buf in enumerate(turn_bufs):
        move_this_round = {}
        throw_this_round = {}
        for _n, _w2, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:                                   # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        if e.id in live_ids:                    # rotate re-emit
                            pos_of[e.id] = e.pos
                            continue
                        live_ids.add(e.id)
                        pos_of[e.id] = e.pos
                        team_of[e.id] = e.team
                        kind_of[e.id] = e.kind
                        if e.team == our_team and e.kind in VIS:
                            sensors.add(e.id)
                        if e.team == them:
                            if e.kind == "builder_bot":
                                ebots.add(e.id)
                                spawn_rnd[e.id] = rnd
                                band_total.setdefault(e.id, 0)
                            elif e.kind in TURRETS:
                                turret_builds.append((rnd, e.pos[0], e.pos[1],
                                                      e.kind))
                                if e.kind in GS and d2(e.pos, ours) <= BAND:
                                    # candidate planting builders: enemy bots
                                    # orthogonally adjacent right now
                                    cand = []
                                    for bid in ebots:
                                        bp = pos_of.get(bid)
                                        if bp is not None and d2(bp, e.pos) == 1:
                                            cand.append(bid)
                                    k = (e.pos[0], e.pos[1])
                                    reuse[k] = reuse.get(k, 0) + 1
                                    pre_t = pre_gs = 0
                                    for oid in live_ids:
                                        if oid == e.id or team_of.get(oid) != them:
                                            continue
                                        ok = kind_of.get(oid)
                                        if ok in TURRETS and \
                                                d2(pos_of[oid], e.pos) <= 8:
                                            pre_t += 1
                                            if ok in GS:
                                                pre_gs += 1
                                    plants.append(dict(
                                        eid=e.id, rnd=rnd, kind=e.kind,
                                        x=e.pos[0], y=e.pos[1],
                                        d2=d2(e.pos, ours), reuse_idx=reuse[k],
                                        cand=cand, pre_t=pre_t, pre_gs=pre_gs,
                                        drnd=-1))
                elif unum == 2:                                 # moveBuilderBot
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid in pos_of and to:
                        old = pos_of[eid]
                        dd = abs(to[0] - old[0]) + abs(to[1] - old[1])
                        pos_of[eid] = to
                        if eid in ebots:
                            move_this_round[eid] = move_this_round.get(eid, 0) + 1
                            if dd > 1:
                                throw_this_round[eid] = 1
                elif unum == 3:                                 # removeEntity
                    for _rn, _rw, rv in fields(ubuf):
                        if rv not in live_ids:
                            continue
                        live_ids.discard(rv)
                        pos_of.pop(rv, None)
                        sensors.discard(rv)
                        ebots.discard(rv)
                        if team_of.get(rv) == them and \
                                kind_of.get(rv) in GS:
                            pass
                        # close plant lifetimes
                        for p in plants:
                            if p["eid"] == rv and p["drnd"] < 0:
                                p["drnd"] = rnd
                        if rv in ep:
                            e0 = ep.pop(rv)
                            e0["ended"] = "death"
                            e0["end"] = rnd - 1 if e0["len"] else rnd
                            eout.append((rv, e0))

        # ---- end of round snapshot ----
        cur_d2, cur_band, cur_vis = {}, set(), {}
        for bid in ebots:
            bp = pos_of.get(bid)
            if bp is None:
                continue
            dd = d2(bp, ours)
            cur_d2[bid] = dd
            if dd <= BAND:
                cur_band.add(bid)
                cur_vis[bid] = vis_other(bp)
                band_total[bid] = band_total.get(bid, 0) + 1
        nband = len(cur_band)
        for bid in cur_band:
            e0 = ep.get(bid)
            if e0 is None:
                e0 = dict(start=rnd, entry_d2=cur_d2[bid],
                          throw_in=throw_this_round.get(bid, 0),
                          mind2=cur_d2[bid], vis_n=0, len=0, moves=0,
                          nother_max=0)
                ep[bid] = e0
            e0["len"] += 1
            e0["mind2"] = min(e0["mind2"], cur_d2[bid])
            e0["vis_n"] += cur_vis[bid]
            e0["moves"] += move_this_round.get(bid, 0)
            e0["nother_max"] = max(e0["nother_max"], nband - 1)
        for bid in list(ep):
            if bid not in cur_band:
                e0 = ep.pop(bid)
                e0["ended"] = "exit"
                e0["end"] = rnd - 1
                eout.append((bid, e0))
        hist.append(dict(d2=cur_d2, band=cur_band, vis=cur_vis,
                         moves=dict(move_this_round),
                         pos={b: pos_of[b] for b in ebots if b in pos_of}))

        # ---- write plant rows for plants created THIS round ----
        for p in plants:
            if p["rnd"] != rnd or p.get("written"):
                continue
            p["written"] = True
            cand = p["cand"]
            pid = cand[0] if len(cand) == 1 else (cand[0] if cand else -1)
            row = dict(file=name, seat=our_team, rnd=rnd, kind=p["kind"],
                       x=p["x"], y=p["y"], d2=p["d2"],
                       reuse_idx=p["reuse_idx"], pid=pid, ncand=len(cand))
            # history: hist[-1] is THIS round; t-1 is hist[-2]
            def hget(k, back):
                i = len(hist) - 1 - back
                return hist[i] if 0 <= i else None
            loiter = 0
            for back in range(1, len(hist)):
                hh = hget(None, back)
                if hh and pid in hh["band"]:
                    loiter += 1
                else:
                    break
            e0 = ep.get(pid)
            row["loiter"] = loiter
            row["band_total"] = band_total.get(pid, 0)
            row["age"] = rnd - spawn_rnd.get(pid, -1) if pid in spawn_rnd else -1
            row["ep_entry_d2"] = e0["entry_d2"] if e0 else -1
            row["ep_throw_in"] = e0["throw_in"] if e0 else -1
            mv = 0
            mind = 9999
            firstp = lastp = None
            for back in range(1, min(11, len(hist))):
                hh = hget(None, back)
                if hh is None:
                    continue
                mv += hh["moves"].get(pid, 0)
                if pid in hh["d2"]:
                    mind = min(mind, hh["d2"][pid])
                    if firstp is None or back > 0:
                        pass
            # net displacement over the window: pos at t-10ish vs t-1
            p1 = hget(None, 1)
            pk = None
            for back in range(min(10, len(hist) - 1), 0, -1):
                hh = hget(None, back)
                if hh and pid in hh["pos"]:
                    pk = hh["pos"][pid]
                    break
            row["moves_w10"] = mv
            row["netdisp_w10"] = (abs(p1["pos"][pid][0] - pk[0]) +
                                  abs(p1["pos"][pid][1] - pk[1])) \
                if (p1 and pk and pid in p1.get("pos", {})) else -1
            row["mind2_w10"] = mind if mind < 9999 else -1
            for back in (1, 2, 3, 5, 10):
                hh = hget(None, back)
                row[f"d2_m{back}"] = hh["d2"].get(pid, -1) if hh else -1
            hh1 = hget(None, 1)
            row["nbots_m1"] = len(hh1["band"]) if hh1 else -1
            seen = set()
            mx = 0
            for back in range(1, min(11, len(hist))):
                hh = hget(None, back)
                if hh:
                    seen |= hh["band"]
                    mx = max(mx, len(hh["band"]))
            row["nbots_w10"] = len(seen)
            row["nbots_max_w10"] = mx
            lm = 0
            for back in range(1, max(2, loiter + 1)):
                hh = hget(None, back)
                if hh:
                    lm = max(lm, len(hh["band"]))
            row["nbots_loiter_max"] = lm
            bp = pos_of.get(pid)
            row["vis_core_m1"] = 1 if (hh1 and pid in hh1["d2"] and
                                       hh1["d2"][pid] <= VIS["core"]) else 0
            row["vis_oth_m1"] = hh1["vis"].get(pid, 0) if hh1 else 0
            if e0 and e0["len"]:
                row["vis_oth_frac"] = round(e0["vis_n"] / e0["len"], 4)
                row["vis_oth_any"] = 1 if e0["vis_n"] else 0
            else:
                row["vis_oth_frac"] = -1
                row["vis_oth_any"] = -1
            row["pre_t8"] = p["pre_t"]
            row["pre_gs8"] = p["pre_gs"]
            p["row"] = row

    # flush open episodes
    for bid, e0 in ep.items():
        e0["ended"] = "gameend"
        e0["end"] = len(turn_bufs) - 1
        eout.append((bid, e0))

    # post-process plants: nest label + death
    plant_by_bot = {}
    for p in plants:
        row = p.get("row")
        if row is None:
            continue
        nt = ngs = 0
        for (r2, tx, ty, tk) in turret_builds:
            if r2 <= p["rnd"] or r2 > p["rnd"] + NEST_W:
                continue
            if (tx - p["x"]) ** 2 + (ty - p["y"]) ** 2 <= 8:
                nt += 1
                if tk in GS:
                    ngs += 1
        row["new_t8_30"] = nt
        row["new_gs8_30"] = ngs
        row["died"] = 1 if p["drnd"] >= 0 else 0
        row["drnd"] = p["drnd"]
        pout.append(row)
        if row["pid"] >= 0:
            plant_by_bot.setdefault(row["pid"], []).append(p["rnd"])
    return plant_by_bot, spawn_rnd, our_team, name


def run_one(args):
    path, our_team = args
    pout, eraw = [], []
    try:
        res = decode(Path(path), our_team, pout, eraw)
    except Exception as exc:                                    # noqa: BLE001
        return None, None, f"ERR {Path(path).name}: {exc}"
    if res is None:
        return [], [], None
    plant_by_bot, spawn_rnd, seat, name = res
    erows = []
    for bid, e0 in eraw:
        pr = [r for r in plant_by_bot.get(bid, [])
              if e0["start"] <= r <= e0["end"] + 2]
        erows.append(dict(file=name, seat=seat, bid=bid, start=e0["start"],
                          end=e0["end"], length=e0["len"], mind2=e0["mind2"],
                          entry_d2=e0["entry_d2"], throw_in=e0["throw_in"],
                          moves=e0["moves"], nother_max=e0["nother_max"],
                          vis_oth_frac=round(e0["vis_n"] / e0["len"], 4)
                          if e0["len"] else -1,
                          planted=len(pr),
                          plant_lag=(min(pr) - e0["start"]) if pr else -1,
                          ended=e0["ended"],
                          spawn_rnd=spawn_rnd.get(bid, -1)))
    return pout, erows, None


def main():
    import csv
    from multiprocessing import Pool
    base = "/Users/junghard/Projects/Work/florent-code-game/"
    out = Path(sys.argv[1])
    jobs = []
    with open(base + "corpus/join.tsv") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            p = base + "replay_archive/" + r["file"]
            if Path(p).exists():
                jobs.append((p, int(r["our_team"])))
    if len(sys.argv) > 2:
        jobs = jobs[:int(sys.argv[2])]
    print(f"{len(jobs)} attributed replays on disk", file=sys.stderr)
    pf = open(out / "plants.tsv", "w")
    ef = open(out / "episodes.tsv", "w")
    pf.write("\t".join(PCOLS) + "\n")
    ef.write("\t".join(ECOLS) + "\n")
    np = ne = bad = 0
    with Pool(8) as pool:
        for i, (prow, erow, err) in enumerate(
                pool.imap_unordered(run_one, jobs, chunksize=8)):
            if err:
                bad += 1
                print(err, file=sys.stderr)
                continue
            for r in prow:
                pf.write("\t".join(str(r.get(c, "")) for c in PCOLS) + "\n")
                np += 1
            for r in erow:
                ef.write("\t".join(str(r.get(c, "")) for c in ECOLS) + "\n")
                ne += 1
            if (i + 1) % 250 == 0:
                print(f"  ...{i+1}/{len(jobs)}", file=sys.stderr, flush=True)
    pf.close()
    ef.close()
    print(f"done: {np} plants, {ne} episodes, {bad} errors", file=sys.stderr)


if __name__ == "__main__":
    main()
