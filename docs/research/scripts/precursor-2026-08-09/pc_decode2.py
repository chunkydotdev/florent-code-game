#!/usr/bin/env python3
"""PRECURSOR decoder v2 -- enemy builder tracks before an in-base turret plant.

Derived from docs/research/scripts/side-lane-2026-08-09/bb_decode.py (validated
builder-bot position tracker).  WHAT CHANGED vs that file:

  * tracks EVERY entity's position/team/kind (bb_decode kept only builder bots +
    the two cores) -- needed for enemy turret geometry and our own sensors;
  * UNCENSORED per-bot loiter streaks at three thresholds (d2<=32 the plant
    band, d2<=36 our core's vision radius, d2<=50 an outer approach ring);
  * PLANT rows: one per enemy gunner/sentinel built at d2<=32 of OUR core, with
    the planting builder attributed by orthogonal adjacency at the instant the
    placeEntity is read, plus its loiter / approach / multiplicity / visibility;
  * EPISODE rows: one per maximal run of consecutive rounds an enemy builder
    spends inside d2<=36 of our core (the zone our core can actually see) --
    the negative control;
  * generic build attribution, so an episode records whether the loiterer built
    a turret, built something else, or built nothing;
  * drops bb_decode's core-damage/heal accounting.

Traps honoured (docs/research/corpus-howto.md):
  1. build = FIRST placeEntity carrying an id (rotate re-emits) -- guarded.
  2. updateHp.delta two's-complement -- not used here.
  3. throws = moveBuilderBot with |to-frm|>1 -- flagged, not dropped.

Read-only over replay_archive/ + corpus/; writes only into the scratchpad.
"""
from __future__ import annotations

import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game/tools")
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa: E402

BAND = 32
ZONE = 36           # our core's vision radius squared -> the detectable zone
OUTER = 50
HIST = 20
NEST_W = 30
TURRETS = ("gunner", "sentinel", "launcher")
GS = ("gunner", "sentinel")
BUILDINGS = ("conveyor", "splitter", "harvester", "barrier",
             "gunner", "sentinel", "launcher")
VIS = {"builder_bot": 20, "core": 36, "gunner": 13, "sentinel": 32,
       "launcher": 26}

PCOLS = ["file", "seat", "rnd", "kind", "x", "y", "d2", "reuse_idx",
         "pid", "ncand", "plt_d2",
         "loiter32", "loiter36", "loiter50", "zone_total", "age",
         "ep_start", "ep_entry_d2", "ep_throw_in", "ep_len", "ep_other_builds",
         "moves_w10", "mind2_w10", "closing_w10", "d2trace",
         "nb32_m1", "nb36_m1", "nb32_max_w10", "nb36_max_w10",
         "nb36_max_loiter", "nb36_distinct_w10",
         "vis_oth_m1", "vis_oth_frac", "vis_oth_any",
         "pre_t8", "pre_gs8", "new_t8_30", "new_gs8_30",
         "new_x0_30", "new_coex_30", "lag_x0", "died", "drnd",
         "lastrnd"]

ECOLS = ["file", "seat", "bid", "start", "end", "length", "len32", "mind2",
         "entry_d2", "throw_in", "moves", "nother_max", "vis_oth_frac",
         "planted", "plant_lag", "other_builds", "ended", "spawn_rnd",
         "lastrnd"]


def d2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def decode(path: Path, our_team: int):
    data = path.read_bytes()
    map_buf, turn_bufs = None, []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if map_buf is None:
        return None
    cores = []
    for num, wire, value in fields(map_buf):
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
        return None
    corepos = {c["team"]: c["pos"] for c in cores}
    ours = corepos[our_team]
    them = 1 - our_team
    name = path.name
    lastrnd = len(turn_bufs) - 1

    pos_of = {c["id"]: c["pos"] for c in cores}
    team_of = {c["id"]: c["team"] for c in cores}
    kind_of = {c["id"]: "core" for c in cores}
    live_ids = set(pos_of)
    ebots = set()
    sensors = {c["id"] for c in cores if c["team"] == our_team}

    spawn_rnd, zone_total = {}, {}
    st32, st36, st50 = {}, {}, {}          # uncensored streaks (rounds so far)
    ep = {}
    erows_raw = []
    plants, turret_builds = [], []
    reuse = {}
    zrows = []
    hist = deque(maxlen=HIST)
    plant_by_bot = {}

    def vis_other(p):
        for sid in sensors:
            if kind_of.get(sid) == "core":
                continue
            sp = pos_of.get(sid)
            if sp is not None and d2(sp, p) <= VIS[kind_of[sid]]:
                return 1
        return 0

    def adj_enemy_builders(tile):
        return [b for b in ebots
                if (bp := pos_of.get(b)) is not None and d2(bp, tile) == 1]

    for rnd, turn_buf in enumerate(turn_bufs):
        moves = {}
        throws = {}
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
                        if e.team != them:
                            continue
                        if e.kind == "builder_bot":
                            ebots.add(e.id)
                            spawn_rnd[e.id] = rnd
                            continue
                        if e.kind in TURRETS:
                            turret_builds.append([rnd, e.pos[0], e.pos[1],
                                                  e.kind, e.id, 10 ** 9])
                        dd = d2(e.pos, ours)
                        if e.kind in BUILDINGS and dd <= ZONE:
                            cand = adj_enemy_builders(e.pos)
                            isplant = e.kind in GS and dd <= BAND
                            for b in cand if not isplant else ():
                                if b in ep:
                                    ep[b]["other_builds"] += 1
                            if not isplant:
                                continue
                            k = (e.pos[0], e.pos[1])
                            reuse[k] = reuse.get(k, 0) + 1
                            pre_t = pre_gs = 0
                            for oid in live_ids:
                                if oid == e.id or team_of.get(oid) != them:
                                    continue
                                ok = kind_of.get(oid)
                                if ok in TURRETS and d2(pos_of[oid], e.pos) <= 8:
                                    pre_t += 1
                                    if ok in GS:
                                        pre_gs += 1
                            plants.append(dict(
                                eid=e.id, rnd=rnd, kind=e.kind, x=e.pos[0],
                                y=e.pos[1], d2=dd, reuse_idx=reuse[k],
                                cand=cand, pre_t=pre_t, pre_gs=pre_gs, drnd=-1))
                elif unum == 2:                                 # moveBuilderBot
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid in pos_of and to:
                        old = pos_of[eid]
                        step = abs(to[0] - old[0]) + abs(to[1] - old[1])
                        pos_of[eid] = to
                        if eid in ebots:
                            moves[eid] = moves.get(eid, 0) + 1
                            if step > 1:
                                throws[eid] = 1
                elif unum == 3:                                 # removeEntity
                    for _rn, _rw, rv in fields(ubuf):
                        if rv not in live_ids:
                            continue
                        live_ids.discard(rv)
                        pos_of.pop(rv, None)
                        sensors.discard(rv)
                        if rv in ebots:
                            ebots.discard(rv)
                            st32.pop(rv, None)
                            st36.pop(rv, None)
                            st50.pop(rv, None)
                            if rv in ep:
                                e0 = ep.pop(rv)
                                e0["ended"] = "death"
                                erows_raw.append((rv, e0))
                        if team_of.get(rv) == them and kind_of.get(rv) in TURRETS:
                            for p in plants:
                                if p["eid"] == rv and p["drnd"] < 0:
                                    p["drnd"] = rnd
                            for tb in turret_builds:
                                if tb[4] == rv and tb[5] > 10 ** 8:
                                    tb[5] = rnd

        # ---------- plant rows are written using the state STRICTLY BEFORE
        # this round's snapshot, i.e. the streaks/history as of round rnd-1 ----
        for p in plants:
            if p["rnd"] != rnd or "row" in p:
                continue
            cand = p["cand"]
            pid = cand[0] if cand else -1
            r = dict(file=name, seat=our_team, rnd=rnd, kind=p["kind"],
                     x=p["x"], y=p["y"], d2=p["d2"], reuse_idx=p["reuse_idx"],
                     pid=pid, ncand=len(cand), lastrnd=lastrnd)
            bp = pos_of.get(pid)
            r["plt_d2"] = d2(bp, ours) if bp else -1
            r["loiter32"] = st32.get(pid, 0)
            r["loiter36"] = st36.get(pid, 0)
            r["loiter50"] = st50.get(pid, 0)
            r["zone_total"] = zone_total.get(pid, 0)
            r["age"] = rnd - spawn_rnd[pid] if pid in spawn_rnd else -1
            e0 = ep.get(pid)
            r["ep_start"] = e0["start"] if e0 else -1
            r["ep_entry_d2"] = e0["entry_d2"] if e0 else -1
            r["ep_throw_in"] = e0["throw_in"] if e0 else -1
            r["ep_len"] = e0["len"] if e0 else 0
            r["ep_other_builds"] = e0["other_builds"] if e0 else -1
            r["vis_oth_frac"] = round(e0["vis_n"] / e0["len"], 4) \
                if (e0 and e0["len"]) else -1
            r["vis_oth_any"] = (1 if e0["vis_n"] else 0) if e0 else -1
            mv = 0
            mind = 9999
            trace = []
            for hh in hist:                       # oldest -> newest, all < rnd
                v = hh["d2"].get(pid, -1)
                trace.append(v)
                mv += hh["moves"].get(pid, 0)
                if 0 <= v:
                    mind = min(mind, v)
            r["d2trace"] = ",".join(str(v) for v in trace[-HIST:])
            w10 = list(hist)[-10:]
            r["moves_w10"] = sum(hh["moves"].get(pid, 0) for hh in w10)
            m10 = [hh["d2"][pid] for hh in w10 if pid in hh["d2"]]
            r["mind2_w10"] = min(m10) if m10 else -1
            r["closing_w10"] = (m10[0] - m10[-1]) if len(m10) >= 2 else -9999
            h1 = hist[-1] if hist else None
            r["nb32_m1"] = len(h1["b32"]) if h1 else -1
            r["nb36_m1"] = len(h1["b36"]) if h1 else -1
            r["nb32_max_w10"] = max((len(hh["b32"]) for hh in w10), default=-1)
            r["nb36_max_w10"] = max((len(hh["b36"]) for hh in w10), default=-1)
            L = min(r["loiter36"], len(hist))
            wl = list(hist)[len(hist) - L:] if L else []
            r["nb36_max_loiter"] = max((len(hh["b36"]) for hh in wl), default=0)
            s = set()
            for hh in w10:
                s |= hh["b36"]
            r["nb36_distinct_w10"] = len(s)
            r["vis_oth_m1"] = h1["vis"].get(pid, 0) if h1 else -1
            r["pre_t8"] = p["pre_t"]
            r["pre_gs8"] = p["pre_gs"]
            p["row"] = r
            if pid >= 0:
                plant_by_bot.setdefault(pid, []).append(rnd)

        # ---------- end-of-round snapshot ----------
        cur_d2, b32, b36, cur_vis = {}, set(), set(), {}
        for bid in ebots:
            bpp = pos_of.get(bid)
            if bpp is None:
                continue
            dd = d2(bpp, ours)
            cur_d2[bid] = dd
            st32[bid] = st32.get(bid, 0) + 1 if dd <= BAND else 0
            st50[bid] = st50.get(bid, 0) + 1 if dd <= OUTER else 0
            if dd <= BAND:
                b32.add(bid)
            if dd <= ZONE:
                b36.add(bid)
                st36[bid] = st36.get(bid, 0) + 1
                zone_total[bid] = zone_total.get(bid, 0) + 1
                cur_vis[bid] = vis_other(bpp)
            else:
                st36[bid] = 0
        n36 = len(b36)
        for bid in b36:
            e0 = ep.get(bid)
            if e0 is None:
                e0 = dict(start=rnd, entry_d2=cur_d2[bid],
                          throw_in=throws.get(bid, 0), mind2=cur_d2[bid],
                          vis_n=0, len=0, len32=0, moves=0, nother_max=0,
                          other_builds=0)
                ep[bid] = e0
            e0["len"] += 1
            if cur_d2[bid] <= BAND:
                e0["len32"] += 1
            e0["mind2"] = min(e0["mind2"], cur_d2[bid])
            e0["vis_n"] += cur_vis[bid]
            e0["moves"] += moves.get(bid, 0)
            e0["nother_max"] = max(e0["nother_max"], n36 - 1)
        for bid in list(ep):
            if bid not in b36:
                e0 = ep.pop(bid)
                e0["ended"] = "exit"
                erows_raw.append((bid, e0))
        hist.append(dict(d2=cur_d2, b32=b32, b36=b36, vis=cur_vis,
                         moves=dict(moves)))
        if b36:
            zrows.append((name, our_team, rnd, len(b36), len(b32),
                          max(st36[b] for b in b36),
                          max((st32[b] for b in b32), default=0), lastrnd))

    for bid, e0 in ep.items():
        e0["ended"] = "gameend"
        erows_raw.append((bid, e0))

    prows = []
    for p in plants:
        r = p.get("row")
        if r is None:
            continue
        nt = ngs = nx0 = ncx = 0
        lag_x0 = -1
        seed_death = p["drnd"] if p["drnd"] >= 0 else 10 ** 9
        for (r2, tx, ty, tk, tid, td) in turret_builds:
            dd = (tx - p["x"]) ** 2 + (ty - p["y"]) ** 2
            if dd and 0 < dd <= 8 and r2 > p["rnd"] and \
                    (lag_x0 < 0 or r2 - p["rnd"] < lag_x0):
                lag_x0 = r2 - p["rnd"]
            if not (p["rnd"] < r2 <= p["rnd"] + NEST_W and dd <= 8):
                continue
            nt += 1
            if tk in GS:
                ngs += 1
            if dd == 0:                 # same tile == a REBUILD, not a nest
                continue
            nx0 += 1
            if r2 <= seed_death:        # the two turrets coexisted
                ncx += 1
        r["new_t8_30"] = nt
        r["new_gs8_30"] = ngs
        r["new_x0_30"] = nx0
        r["new_coex_30"] = ncx
        r["lag_x0"] = lag_x0
        r["died"] = 1 if p["drnd"] >= 0 else 0
        r["drnd"] = p["drnd"]
        prows.append(r)

    erows = []
    for bid, e0 in erows_raw:
        end = e0["start"] + e0["len"] - 1
        pr = [x for x in plant_by_bot.get(bid, []) if e0["start"] <= x <= end + 1]
        erows.append(dict(file=name, seat=our_team, bid=bid, start=e0["start"],
                          end=end, length=e0["len"], len32=e0["len32"],
                          mind2=e0["mind2"], entry_d2=e0["entry_d2"],
                          throw_in=e0["throw_in"], moves=e0["moves"],
                          nother_max=e0["nother_max"],
                          vis_oth_frac=round(e0["vis_n"] / e0["len"], 4)
                          if e0["len"] else -1,
                          planted=len(pr),
                          plant_lag=(min(pr) - e0["start"]) if pr else -1,
                          other_builds=e0["other_builds"], ended=e0["ended"],
                          spawn_rnd=spawn_rnd.get(bid, -1), lastrnd=lastrnd))
    return prows, erows, zrows


def run_one(args):
    path, our_team = args
    try:
        res = decode(Path(path), our_team)
    except Exception as exc:                                    # noqa: BLE001
        return [], [], [], f"ERR {Path(path).name}: {exc}"
    if res is None:
        return [], [], [], None
    return res[0], res[1], res[2], None


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
    print(f"{len(jobs)} attributed replays", file=sys.stderr)
    pf = open(out / "plants2.tsv", "w")
    ef = open(out / "episodes2.tsv", "w")
    zf = open(out / "zone_rounds.tsv", "w")
    pf.write("\t".join(PCOLS) + "\n")
    ef.write("\t".join(ECOLS) + "\n")
    zf.write("file\tseat\trnd\tnb36\tnb32\tmaxstreak36\tmaxstreak32\tlastrnd\n")
    np = ne = nz = bad = 0
    with Pool(8) as pool:
        for i, (pr, er, zr, err) in enumerate(
                pool.imap_unordered(run_one, jobs, chunksize=8)):
            if err:
                bad += 1
                print(err, file=sys.stderr)
                continue
            for r in pr:
                pf.write("\t".join(str(r.get(c, "")) for c in PCOLS) + "\n")
                np += 1
            for r in er:
                ef.write("\t".join(str(r.get(c, "")) for c in ECOLS) + "\n")
                ne += 1
            for r in zr:
                zf.write("\t".join(str(x) for x in r) + "\n")
                nz += 1
            if (i + 1) % 400 == 0:
                print(f"  ...{i+1}/{len(jobs)}", file=sys.stderr, flush=True)
    pf.close()
    ef.close()
    zf.close()
    print(f"done: {np} plants, {ne} episodes, {nz} zone-rounds, {bad} errors",
          file=sys.stderr)


if __name__ == "__main__":
    main()
