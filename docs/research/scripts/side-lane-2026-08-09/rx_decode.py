#!/usr/bin/env python3
"""Per-opponent REACTION decoder (read-only; scratchpad output only).

Emits event-level tables needed for the reaction atlas.  Traps honoured
(docs/research/corpus-howto.md):
  1. build = FIRST placeEntity carrying an id; re-emits are rotations/state.
  3. launcher throws emit no FireTurret; a throw is a moveBuilderBot whose `to`
     is >1 tile (chebyshev) from `frm`, thrower = a launcher at d2<=2 of the
     pre-throw tile.  Ambiguous (both teams in range) -> dropped, not guessed.
"""
from __future__ import annotations

import os
import sys
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa: E402

DEF_KINDS = {"gunner", "sentinel", "barrier"}
SIGHT_D2 = 32          # proxy: "a sentinel standing there would have seen it"
NEAR_D2 = 4            # "at/near X"

SHOT_CLASSES = ["bot_enemy", "bot_own", "empty", "b_own",
                "b_conveyor", "b_splitter", "b_harvester", "b_barrier",
                "b_gunner", "b_sentinel", "b_launcher", "b_core"]


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def d2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def decode(path: Path):
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
    name = path.name
    nrounds = len(turn_bufs)

    team_of, kind_of, pos_of, dir_of, born = {}, {}, {}, {}, {}
    pos_ever = {}   # never popped: kept so the shooter table can place
                    # DESTROYED turrets (fix 2026-08-09: pos_of.pop on
                    # removeEntity made x=-1 for 57%% of core-shooters --
                    # a survivorship bias in every geography drawn from it)
    bldg_at, bot_at = {}, {}
    for c in cores:
        team_of[c["id"]] = c["team"]
        kind_of[c["id"]] = "core"
        pos_of[c["id"]] = c["pos"]
        pos_ever[c["id"]] = c["pos"]
        born[c["id"]] = 0
        for dx in (0, 1):
            for dy in (0, 1):
                bldg_at[(c["pos"][0] + dx, c["pos"][1] + dy)] = c["id"]

    shot = {}       # (team, shooter_kind) -> counters
    oor = {}        # (team, shooter_kind) -> shots beyond nominal attack range

    def sc(t, k):
        if (t, k) not in shot:
            shot[(t, k)] = dict.fromkeys(SHOT_CLASSES, 0)
            oor[(t, k)] = 0
        return shot[(t, k)]

    reemit_dir = {0: 0, 1: 0}
    bshots = []       # (rnd, shooter_team, tid, tx, ty, kind)  shots at enemy bldg
    botpos = []       # per round: list of (team, x, y)
    defb = []         # (team, rnd, kind, x, y)
    rots = []         # (team, rnd, kind, x, y)
    heal_ev = []      # (rnd, team, healer_id, x, y)
    dmg_first = {}    # enemy building id -> (rnd, attacker_team, x, y, kind)
    throws = []       # (rnd, lteam, lid, bot_id, bot_team)
    adj_state = {}
    adj_eps = []      # (rnd, lteam, lid, bot_id)
    shooters = {}
    lau_alive = set()
    gun_alive = set()
    gun_rounds = {0: 0, 1: 0}
    gun_rounds_near = {0: 0, 1: 0}

    for rnd, turn_buf in enumerate(turn_bufs):
        for _n, _w2, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:                                    # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        if e.id in pos_of:                       # re-emit
                            old = pos_of[e.id]
                            k = kind_of[e.id]
                            if old != e.pos:
                                if k == "builder_bot":
                                    if bot_at.get(old) == e.id:
                                        del bot_at[old]
                                    bot_at[e.pos] = e.id
                                else:
                                    if bldg_at.get(old) == e.id:
                                        del bldg_at[old]
                                    bldg_at[e.pos] = e.id
                                pos_of[e.id] = e.pos
                                pos_ever[e.id] = e.pos
                            od = dir_of.get(e.id)
                            if e.direction is not None and od is not None \
                                    and e.direction != od:
                                reemit_dir[e.team] += 1
                                if k in ("gunner", "sentinel"):
                                    rots.append((e.team, rnd, k,
                                                 e.pos[0], e.pos[1]))
                            if e.direction is not None:
                                dir_of[e.id] = e.direction
                            continue
                        team_of[e.id] = e.team
                        kind_of[e.id] = e.kind
                        pos_of[e.id] = e.pos
                        pos_ever[e.id] = e.pos
                        born[e.id] = rnd
                        if e.direction is not None:
                            dir_of[e.id] = e.direction
                        if e.kind == "builder_bot":
                            bot_at[e.pos] = e.id
                        else:
                            bldg_at[e.pos] = e.id
                        if e.kind in DEF_KINDS:
                            defb.append((e.team, rnd, e.kind, e.pos[0], e.pos[1]))
                        if e.kind == "launcher":
                            lau_alive.add(e.id)
                        elif e.kind == "gunner":
                            gun_alive.add(e.id)
                elif unum == 2:                                  # moveBuilderBot
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid not in pos_of or to is None:
                        continue
                    old = pos_of[eid]
                    if cheb(old, to) > 1:                        # THROW
                        cands = [lid for lid in lau_alive
                                 if d2(pos_of[lid], old) <= 2]
                        tms = {team_of[l] for l in cands}
                        if len(tms) == 1:
                            lt0 = tms.pop()
                            throws.append((rnd, lt0, cands[0], eid,
                                           team_of[eid], len(cands)))
                    if bot_at.get(old) == eid:
                        del bot_at[old]
                    bot_at[to] = eid
                    pos_of[eid] = to
                    pos_ever[eid] = to
                elif unum == 3:                                  # removeEntity
                    for _rn, _rw, rv in fields(ubuf):
                        if rv not in pos_of:
                            continue
                        p = pos_of.pop(rv)
                        if kind_of.get(rv) == "builder_bot":
                            if bot_at.get(p) == rv:
                                del bot_at[p]
                        else:
                            if bldg_at.get(p) == rv:
                                del bldg_at[p]
                        lau_alive.discard(rv)
                        gun_alive.discard(rv)
                        s = shooters.get(rv)
                        if s is not None:
                            s["died"] = rnd
                elif unum == 12:                                 # fireTurret
                    frm = to = None
                    for fn, _fw, fv in fields(ubuf):
                        if fn == 1:
                            frm = read_pos(fv)
                        elif fn == 2:
                            to = read_pos(fv)
                    sid = bldg_at.get(frm)
                    if sid is None:
                        continue
                    t = team_of.get(sid)
                    if t is None:
                        continue
                    s = shooters.get(sid)
                    if s is None:
                        s = shooters[sid] = dict(first=rnd, last=rnd, n=0,
                                                 ncore=0, died=-1)
                    s["last"] = rnd
                    s["n"] += 1
                    if to is None:
                        continue
                    sk = kind_of.get(sid, "?")
                    cnt = sc(t, sk)
                    lim = 13 if sk == "gunner" else (32 if sk == "sentinel" else 99)
                    if d2(frm, to) > lim:
                        oor[(t, sk)] += 1
                    bid = bot_at.get(to)
                    if bid is not None:
                        cnt["bot_enemy" if team_of.get(bid) != t
                            else "bot_own"] += 1
                        continue
                    tid = bldg_at.get(to)
                    if tid is None:
                        cnt["empty"] += 1
                        continue
                    if team_of.get(tid) == t:
                        cnt["b_own"] += 1
                        continue
                    k = kind_of.get(tid, "?")
                    key = "b_" + k
                    if key in cnt:
                        cnt[key] += 1
                    bshots.append((rnd, t, tid, to[0], to[1], k, sid))
                    if k == "core":
                        s["ncore"] += 1
                    elif tid not in dmg_first:
                        dmg_first[tid] = (rnd, t, to[0], to[1], k)
                elif unum == 13:                                 # builderAttack
                    eid = tgt = None
                    for an, _aw, av in fields(ubuf):
                        if an == 1:
                            eid = av
                        elif an == 2:
                            tgt = read_pos(av)
                    t = team_of.get(eid)
                    if t is None or tgt is None:
                        continue
                    tid = bldg_at.get(tgt)
                    if tid is not None and team_of.get(tid) != t \
                            and kind_of.get(tid) != "core" and tid not in dmg_first:
                        dmg_first[tid] = (rnd, t, tgt[0], tgt[1], kind_of[tid])
                elif unum == 15:                                 # builderHeal
                    eid = tgt = None
                    for an, _aw, av in fields(ubuf):
                        if an == 1:
                            eid = av
                        elif an == 2:
                            tgt = read_pos(av)
                    t = team_of.get(eid)
                    if t is None or tgt is None:
                        continue
                    heal_ev.append((rnd, t, eid, tgt[0], tgt[1]))

        botpos.append([(team_of[b], p[0], p[1]) for p, b in bot_at.items()])
        for gid in gun_alive:
            gp = pos_of[gid]
            gt = team_of[gid]
            gun_rounds[gt] += 1
            for bp3, bid3 in bot_at.items():
                if team_of.get(bid3) != gt and d2(gp, bp3) <= 13:
                    gun_rounds_near[gt] += 1
                    break
        for lid in lau_alive:
            lp = pos_of[lid]
            lt = team_of[lid]
            for bp2, bid in bot_at.items():
                if team_of.get(bid) == lt or d2(lp, bp2) > 2:
                    continue
                key = (lid, bid)
                if adj_state.get(key) != rnd - 1:
                    adj_eps.append((rnd, lt, lid, bid))
                adj_state[key] = rnd

    return dict(name=name, nrounds=nrounds, team_of=team_of, kind_of=kind_of,
                born=born, shot=shot, oor=oor, reemit_dir=reemit_dir, botpos=botpos,
                defb=defb, rots=rots, heal_ev=heal_ev, dmg_first=dmg_first,
                throws=throws, adj_eps=adj_eps, shooters=shooters, gun_rounds=gun_rounds,
                gun_rounds_near=gun_rounds_near,
                pos_of=pos_of, pos_ever=pos_ever, bshots=bshots)


# --- post-pass: turn raw events into atlas rows ------------------------------

def rows(R):
    """Yield (table_name, row_tuple)."""
    name = R["name"]
    botpos, team_of, kind_of, born = R["botpos"], R["team_of"], R["kind_of"], R["born"]
    nr = R["nrounds"]

    def sighted(t, x, y, r, win, rad=SIGHT_D2, back=0):
        """(latest round, #rounds seen) in [r-win-back, r-1-back] with enemy near."""
        best, cnt = -1, 0
        hi = r - back
        lo = max(0, hi - win)
        for rr in range(lo, min(hi, len(botpos))):
            for (bt, bx, by) in botpos[rr]:
                if bt == t:
                    continue
                if (bx - x) ** 2 + (by - y) ** 2 <= rad:
                    best = rr
                    cnt += 1
                    break
        return best, cnt

    # 1. shot classes, per shooter kind
    for (t, sk), cnt in R["shot"].items():
        yield "shot", (name, t, sk, R["reemit_dir"][t], R["oor"][(t, sk)]) + tuple(
            cnt[c] for c in SHOT_CLASSES)

    # shots at buildings that were being healed (heal on same tile within +/-2 r)
    heal_tiles = {}
    for (r, t, hid, x, y) in R["heal_ev"]:
        heal_tiles.setdefault((t, x, y), []).append(r)
    healed_shots = {0: 0, 1: 0}
    tot_bshots = {0: 0, 1: 0}
    per_tgt = {}
    run = {}
    for (r, t, tid, x, y, k, sid) in R["bshots"]:
        tot_bshots[t] += 1
        hs = heal_tiles.get((1 - t, x, y))
        healed = bool(hs and any(abs(h - r) <= 2 for h in hs))
        if healed:
            healed_shots[t] += 1
        pt = per_tgt.get(tid)
        if pt is None:
            pt = per_tgt[tid] = [t, k, 0, 0, r, r]
        pt[2] += 1
        pt[3] += healed
        pt[5] = r
        rk = (sid, tid)
        cur = run.get(sid)
        if cur and cur[0] == tid:
            cur[1] += 1
        else:
            if cur:
                yield "run", (name, cur[2], cur[3], cur[1])
            run[sid] = [tid, 1, t, k]
    for sid, cur in run.items():
        yield "run", (name, cur[2], cur[3], cur[1])
    for tid, (t, k, n, nh, r0, r1) in per_tgt.items():
        yield "tgt", (name, t, k, n, nh, r1 - r0)
    for t in (0, 1):
        yield "healshot", (name, t, tot_bshots[t], healed_shots[t])

    # 2. defensive builds + sighting, with a place-permutation control
    db = R["defb"]
    bypos = {}
    for (t, r, k, x, y) in db:
        bypos.setdefault(t, []).append((x, y))
    for i, (t, r, k, x, y) in enumerate(db):
        s20, n20 = sighted(t, x, y, r, 20)
        _s13, n13 = sighted(t, x, y, r, 20, rad=13)
        p20, pn20 = sighted(t, x, y, r, 20, back=40)     # same place, r-60..r-41
        _p13, pn13 = sighted(t, x, y, r, 20, rad=13, back=40)
        pool = bypos[t]
        cx, cy = pool[(i * 7 + 3) % len(pool)]
        c20, _cn = sighted(t, cx, cy, r, 20)
        yield "defb", (name, t, r, k, x, y, s20, n20, n13, p20, pn20, pn13, c20)

    # 3. rotations
    for t in (0, 1):
        yield "gunbase", (name, t, R["gun_rounds"][t], R["gun_rounds_near"][t])
    for (t, r, k, x, y) in R["rots"]:
        near = -1
        lo = max(0, r - 3)
        for rr in range(lo, min(r + 1, len(botpos))):
            for (bt, bx, by) in botpos[rr]:
                if bt != t and (bx - x) ** 2 + (by - y) ** 2 <= 13:
                    near = rr
        yield "rot", (name, t, r, k, x, y, near)

    # 4. heal-latency after first damage on a building
    heals_by_team = {}
    for (r, t, hid, x, y) in R["heal_ev"]:
        heals_by_team.setdefault(t, []).append((r, hid, x, y))
    for tid, (dr, atk, x, y, k) in R["dmg_first"].items():
        vt = 1 - atk
        hl = heals_by_team.get(vt, [])
        best = None
        for (r, hid, hx, hy) in hl:
            if r < dr:
                continue
            if (hx - x) ** 2 + (hy - y) ** 2 <= NEAR_D2:
                if best is None or r < best[0]:
                    best = (r, hid)
        if best is None:
            yield "heal", (name, vt, k, dr, -1, -1, "none")
            continue
        hr, hid = best
        if born.get(hid, 0) > dr:
            mode = "spawned"
        else:
            here = False
            if dr < len(botpos):
                for (bt, bx, by) in botpos[dr]:
                    if bt == vt and (bx - x) ** 2 + (by - y) ** 2 <= NEAR_D2:
                        here = True
                        break
            mode = "already" if here else "walked"
        yield "heal", (name, vt, k, dr, hr, hr - dr, mode)

    # 5. launcher throw-on-adjacency
    thr = {}
    for (r, lt, lid, bid, bteam, nl) in R["throws"]:
        thr.setdefault((lid, bid), []).append(r)
    seen_imm = set()
    for (r, lt, lid, bid) in R["adj_eps"]:
        ts = thr.get((lid, bid), [])
        hit = [x for x in ts if r <= x <= r + 3]
        if hit:
            seen_imm.add((lid, bid, hit[0]))
        yield "adj", (name, lt, lid, bid, r, 1 if hit else 0,
                      (hit[0] - r) if hit else -1)
    # throws with no prior end-of-round adjacency = same-round pickup (latency 0)
    adj_rounds = {}
    for (r, lt, lid, bid) in R["adj_eps"]:
        adj_rounds.setdefault((lid, bid), set()).add(r)
    for (r, lt, lid, bid, bteam, nl) in R["throws"]:
        if bteam == lt:
            continue
        ar = adj_rounds.get((lid, bid), set())
        if not any(r - 3 <= a <= r for a in ar):
            yield "adj", (name, lt, lid, bid, r, 1, 0)
    # inter-throw intervals per launcher
    per_l = {}
    nen = now = 0
    for (r, lt, lid, bid, bteam, nl) in R["throws"]:
        if bteam == lt:
            now += 1
        else:
            nen += 1
        if nl == 1:
            per_l.setdefault((lt, lid), []).append(r)
    for (lt, lid), rs in per_l.items():
        rs.sort()
        for a, b in zip(rs, rs[1:]):
            yield "tint", (name, lt, lid, b - a)
    for t in (0, 1):
        nlau = sum(1 for i, k in R["kind_of"].items()
                   if k == "launcher" and R["team_of"][i] == t)
        if nlau or nen or now:
            yield "lstat", (name, t, nlau,
                            sum(1 for x in R["throws"] if x[1] == t and x[4] != t),
                            sum(1 for x in R["throws"] if x[1] == t and x[4] == t))

    # 6. shooters (siege persistence)
    for sid, s in R["shooters"].items():
        p = R["pos_ever"].get(sid, (-1, -1))
        yield "shooter", (name, team_of.get(sid, -1), kind_of.get(sid, "?"),
                          born.get(sid, -1), s["died"], p[0], p[1],
                          s["first"], s["last"], s["n"], s["ncore"], nr)


TABLES = {
    "shot": ["file", "team", "skind", "reemit_dir", "oor"] + SHOT_CLASSES,
    "tgt": ["file", "team", "kind", "nshots", "nshots_healed", "span"],
    "run": ["file", "team", "kind", "runlen"],
    "healshot": ["file", "team", "bldg_shots", "bldg_shots_on_healed"],
    "defb": ["file", "team", "rnd", "kind", "x", "y", "s20", "n20", "n13",
             "p20", "pn20", "pn13", "ctrl20"],
    "gunbase": ["file", "team", "gun_rounds", "gun_rounds_near"],
    "rot": ["file", "team", "rnd", "kind", "x", "y", "enemy_near_r"],
    "heal": ["file", "team", "kind", "dmg_r", "heal_r", "lat", "mode"],
    "adj": ["file", "lteam", "lid", "bid", "rnd", "thrown3", "lat"],
    "tint": ["file", "team", "lid", "gap"],
    "lstat": ["file", "team", "nlauncher", "nthrow_enemy", "nthrow_own"],
    "shooter": ["file", "team", "kind", "born", "died", "x", "y",
                "first", "last", "n", "ncore", "nrounds"],
}


def work(p):
    try:
        R = decode(Path(p))
    except Exception as exc:                                     # noqa: BLE001
        return ("ERR", str(p), repr(exc))
    if R is None:
        return ("ERR", str(p), "no map")
    out = {k: [] for k in TABLES}
    for tbl, row in rows(R):
        out[tbl].append("\t".join(str(v) for v in row))
    return ("OK", out)


def main(argv):
    outdir = argv[0]
    files = argv[1:]
    fh = {k: open(os.path.join(outdir, f"rx_{k}.tsv"), "w") for k in TABLES}
    for k, cols in TABLES.items():
        fh[k].write("\t".join(cols) + "\n")
    bad = 0
    with Pool(8) as pool:
        for i, res in enumerate(pool.imap_unordered(work, files, chunksize=8)):
            if res[0] == "ERR":
                bad += 1
                print("ERR", res[1], res[2], file=sys.stderr)
                continue
            for k, lines in res[1].items():
                if lines:
                    fh[k].write("\n".join(lines) + "\n")
            if (i + 1) % 250 == 0:
                print(f"  ...{i+1}/{len(files)} ({bad} err)", file=sys.stderr,
                      flush=True)
    for f in fh.values():
        f.close()
    print(f"done {len(files)} files, {bad} errors", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
