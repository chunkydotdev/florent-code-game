#!/usr/bin/env python3
"""SEAT decoder -- per-round core-heal-seat staffing and IDLE builder supply.

DERIVED FROM `docs/research/scripts/side-lane-2026-08-09/bb_decode.py`
(preserved + validated: heal x4HP vs UpdateHp median ratio 0.9941, builds-deaths
identity 5,470/5,470, throws match corpus/throws.tsv on 1,313 files).  Extended
in the style of `dwell_decode.py` (same family).  What was ADDED:

  1. Map TILES parsed (walls) + a live BUILDING occupancy map, so "can a builder
     stand on this seat" is answered against the real board, not assumed.
  2. bot_at is a tile -> SET of builder ids (bb_decode/dwell_decode used a
     tile->id dict, which silently drops co-occupation; co-occupation is exactly
     what the on-footprint seats depend on).
  3. Per-builder, per-round ACTION CLASSIFICATION from the event stream:
     builderBuild (16), builderAttack (13), builderHeal (15), moveBuilderBot (2,
     split into step vs throw), botOutput (9, incl. the `tled` flag), spawn round,
     death round.  IDLE = alive at start of round, ran, and emitted none of
     build/attack/heal/move/throw.
  4. Cooldown RECONSTRUCTION from setActionCooldown (7) / setMoveCooldown (8),
     which are emitted only when an action sets them -- so a full simulation is
     possible.  Measured: builder action cooldown is ALWAYS set to 1 and move
     cooldown ALWAYS to 1, i.e. a builder that acted in round r is free again in
     r+1.  Emitted in the validation table so the claim is checkable.
  5. SEAT geometry computed from the 2x2 footprint directly (never from a corpus
     d2 column): ring = the 8 tiles orthogonally adjacent to the footprint;
     fp = the 4 footprint tiles themselves.  H_loose = ring|fp (12), H_strict =
     ring only (8).
  6. Per-round IDLE SUPPLY tiers by cardinal-step BFS (depth<=3) over standable
     tiles: (a) idle and already on a heal-capable tile, (b) idle and 1 step from
     a FREE heal-capable tile, (c) idle and 2-3 steps away.

Everything else -- the placeEntity/rotate trap, the two's-complement HP varint,
the throw-vs-step rule -- is bb_decode.py behaviour.

Usage:  python seat_decode.py <outdir> <join.tsv> <replay...>
Outputs: seat_rounds.tsv (one row per round per game, our team only)
         seat_games.tsv  (one row per game: window, outcome, validation totals)
"""
from __future__ import annotations

import csv
import os
import sys
from collections import deque
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import (fields, read_pos, parse_entity, packed_varints,  # noqa: E402
                           scalars, WIRE_LEN)

ENV_WALL = 1
CO_OK = ("conveyor", "splitter", "core")     # s23 co-occupation probe (PRIOR)
CARD = ((0, -1), (0, 1), (-1, 0), (1, 0))


def s64(v):
    return v - (1 << 64) if v >= (1 << 63) else v


def d2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


ROUND_COLS = [
    "file", "rnd",
    "corehp", "coredmg", "coreheal",            # our core, this round
    "shots_on_core", "shots_odd", "batk_on_core",   # incoming events on our fp
    "live0", "live1",                           # our builders start / end
    "healers", "heal_core_ev", "heal_any_ev",   # core healers this round
    "seat0", "fp0", "seat1", "fp1",             # our builders on ring / fp
    "free_loose", "free_strict",                # free heal-capable tiles
    "n_moved", "n_acted", "n_built", "n_atk", "n_born", "n_born_idle",
    "n_died",
    "n_idle", "n_idle_tled", "n_idle_ran", "n_ran",
    "ia", "ib", "ic",                           # idle supply tiers (LOOSE)
    "ia_s", "ib_s",                             # idle supply tiers (STRICT ring)
    "seat_moved", "seat_other",                 # bots ON a heal tile that
                                                # walked away / acted on
                                                # something else instead
    "idle_adj_rm",                              # idle bots next to an own bldg
                                                # removed this round (destroy UB)
    "own_bldg_rm",
]

GAME_COLS = [
    "file", "our_team", "nr", "w", "h",
    "win_start", "core_death", "core_hp_end",
    "tot_heal_core", "tot_coreheal_hp", "tot_coredmg",
    "tot_builder_rounds", "tot_botoutput", "tot_tled", "tot_crash",
    "acd_vals", "mcd_vals", "spawn_acd", "spawn_mcd",
    "max_seat", "max_fp", "bad_pos", "co_occ_rounds", "n_bots",
]


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
    w = h = 0
    tiles, cores = [], []
    for num, wire, value in fields(map_buf):
        if num == 1:
            w = value
        elif num == 2:
            h = value
        elif num == 3:
            row = []
            for rnum, rwire, rvalue in fields(value):
                if rnum == 1:
                    row.extend(packed_varints(rvalue) if rwire == WIRE_LEN
                               else [rvalue])
            tiles.append(row)
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
    if len(cores) != 2 or not (0 <= our_team <= 1):
        return None

    def is_wall(t):
        x, y = t
        return not (0 <= y < len(tiles) and 0 <= x < len(tiles[y])) or \
            tiles[y][x] == ENV_WALL

    corepos = {c["team"]: c["pos"] for c in cores}
    core_id = {c["team"]: c["id"] for c in cores}
    us, enemy = our_team, 1 - our_team

    footprint = {}
    for t, (cx, cy) in corepos.items():
        for dx in (0, 1):
            for dy in (0, 1):
                footprint[(cx + dx, cy + dy)] = t
    FP = {(p) for p, t in footprint.items() if t == us}
    RING = set()
    for (fx, fy) in FP:
        for dx, dy in CARD:
            p = (fx + dx, fy + dy)
            if p not in footprint and 0 <= p[0] < w and 0 <= p[1] < h \
                    and not is_wall(p):
                RING.add(p)
    H_LOOSE = RING | FP
    H_STRICT = set(RING)

    # --- live state ---------------------------------------------------------
    pos_of, team_of, kind_of = {}, {}, {}
    bot_at = {}                     # tile -> set(builder id)
    bldg_at = {}                    # tile -> building id
    bots = {0: set(), 1: set()}
    for c in cores:
        pos_of[c["id"]] = c["pos"]
        team_of[c["id"]] = c["team"]
        kind_of[c["id"]] = "core"
        for dx in (0, 1):
            for dy in (0, 1):
                bldg_at[(c["pos"][0] + dx, c["pos"][1] + dy)] = c["id"]

    core_hp = {0: 500, 1: 500}
    core_death = -1
    win_start = -1
    V = dict.fromkeys(GAME_COLS[5:], 0)
    V["win_start"] = -1
    V["core_death"] = -1
    acd_vals, mcd_vals, spawn_acd, spawn_mcd = {}, {}, {}, {}
    cd_act, cd_mov = {}, {}          # reconstructed cooldowns
    n_bots = 0
    co_occ_rounds = 0
    rows = []

    def standable(p, exclude_bot=None, loose=True):
        """Could one of our builders occupy p (ignoring our own presence)?"""
        if not (0 <= p[0] < w and 0 <= p[1] < h) or is_wall(p):
            return False
        b = bldg_at.get(p)
        if b is not None:
            if not loose:
                return False
            k = kind_of.get(b)
            if k not in CO_OK:
                return False
            if k == "core" and team_of.get(b) != us:
                return False
        occ = bot_at.get(p)
        if occ:
            if exclude_bot is None or occ - {exclude_bot}:
                return False
        return True

    for rnd, turn_buf in enumerate(turn_bufs):
        # ---- START-OF-ROUND snapshot ----
        start_pos = {b: pos_of[b] for b in bots[us] if b in pos_of}
        live0 = len(start_pos)
        seat0 = sum(1 for p in start_pos.values() if p in RING)
        fp0 = sum(1 for p in start_pos.values() if p in FP)
        free_loose = sum(1 for p in H_LOOSE if standable(p, loose=True))
        free_strict = sum(1 for p in H_STRICT if standable(p, loose=False))
        occ_tiles = {}
        for b, p in start_pos.items():
            occ_tiles.setdefault(p, set()).add(b)
        if any(len(s) > 1 for s in bot_at.values()):
            co_occ_rounds += 1

        moved, thrown, healed, attacked, built = set(), set(), set(), set(), set()
        ran, tled = set(), set()
        heal_core_ev = heal_any_ev = shots_on_core_odd = 0
        healers = set()
        coredmg = coreheal = 0
        shots_on_core = batk_on_core = 0
        born, died = set(), set()
        rm_own_bldg_tiles = set()

        for _n, _w2, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:                                   # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        if e.id in pos_of:                      # re-emit
                            old = pos_of[e.id]
                            if old != e.pos:
                                if kind_of[e.id] == "builder_bot":
                                    s = bot_at.get(old)
                                    if s:
                                        s.discard(e.id)
                                    bot_at.setdefault(e.pos, set()).add(e.id)
                                else:
                                    if bldg_at.get(old) == e.id:
                                        del bldg_at[old]
                                    bldg_at[e.pos] = e.id
                                pos_of[e.id] = e.pos
                            continue
                        pos_of[e.id] = e.pos
                        team_of[e.id] = e.team
                        kind_of[e.id] = e.kind
                        if e.kind == "builder_bot":
                            bots[e.team].add(e.id)
                            bot_at.setdefault(e.pos, set()).add(e.id)
                            if e.team == us:
                                born.add(e.id)
                                n_bots += 1
                                if not (0 <= e.pos[0] < w
                                        and 0 <= e.pos[1] < h):
                                    V["bad_pos"] += 1
                                sub = None
                                for sn, _sw, sv in fields(ebuf):
                                    if sn == 10 and isinstance(sv, bytes):
                                        sub = scalars(sv)
                                if sub:
                                    spawn_acd[sub.get(1, 0)] = \
                                        spawn_acd.get(sub.get(1, 0), 0) + 1
                                    spawn_mcd[sub.get(2, 0)] = \
                                        spawn_mcd.get(sub.get(2, 0), 0) + 1
                        else:
                            bldg_at[e.pos] = e.id
                elif unum == 2:                                 # moveBuilderBot
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid in pos_of and to:
                        old = pos_of[eid]
                        s = bot_at.get(old)
                        if s:
                            s.discard(eid)
                        bot_at.setdefault(to, set()).add(eid)
                        pos_of[eid] = to
                        if team_of.get(eid) == us:
                            if abs(to[0] - old[0]) + abs(to[1] - old[1]) == 1:
                                moved.add(eid)
                            else:
                                thrown.add(eid)
                elif unum == 3:                                 # removeEntity
                    for _rn, _rw, rv in fields(ubuf):
                        if rv not in pos_of:
                            continue
                        p = pos_of.pop(rv)
                        t = team_of.get(rv)
                        if kind_of.get(rv) == "builder_bot":
                            s = bot_at.get(p)
                            if s:
                                s.discard(rv)
                            bots[t].discard(rv)
                            if t == us:
                                died.add(rv)
                        else:
                            if bldg_at.get(p) == rv:
                                del bldg_at[p]
                            if rv == core_id.get(us) and core_death < 0:
                                core_death = rnd
                            if t == us:
                                rm_own_bldg_tiles.add(p)
                elif unum == 5:                                 # updateHp
                    eid = None
                    delta = 0
                    for hn, _hw, hv in fields(ubuf):
                        if hn == 1:
                            eid = hv
                        elif hn == 2:
                            delta = s64(hv)
                    if eid == core_id.get(us):
                        core_hp[us] += delta
                        if delta < 0:
                            coredmg += -delta
                        else:
                            coreheal += delta
                elif unum == 7:                                 # setActionCooldown
                    d = {n: v for n, _wq, v in fields(ubuf)}
                    eid, val = d.get(1), d.get(2, 0)
                    if kind_of.get(eid) == "builder_bot" and \
                            team_of.get(eid) == us:
                        acd_vals[val] = acd_vals.get(val, 0) + 1
                        cd_act[eid] = val
                elif unum == 8:                                 # setMoveCooldown
                    d = {n: v for n, _wq, v in fields(ubuf)}
                    eid, val = d.get(1), d.get(2, 0)
                    if kind_of.get(eid) == "builder_bot" and \
                            team_of.get(eid) == us:
                        mcd_vals[val] = mcd_vals.get(val, 0) + 1
                        cd_mov[eid] = val
                elif unum == 9:                                 # botOutput
                    eid, out, tl = None, b"", False
                    for bn, _bw, bv in fields(ubuf):
                        if bn == 1:
                            eid = bv
                        elif bn == 2:
                            out = bv
                        elif bn == 4:
                            tl = bool(bv)
                    if kind_of.get(eid) == "builder_bot" and \
                            team_of.get(eid) == us:
                        ran.add(eid)
                        V["tot_botoutput"] += 1
                        if tl:
                            tled.add(eid)
                            V["tot_tled"] += 1
                        if out and b"Traceback" in out:
                            V["tot_crash"] += 1
                elif unum == 12:                                # fireTurret
                    frm = to = None
                    for fn, _fw, fv in fields(ubuf):
                        if fn == 1:
                            frm = read_pos(fv)
                        elif fn == 2:
                            to = read_pos(fv)
                    if to is not None and to in FP:
                        sid = bldg_at.get(frm) if frm is not None else None
                        if team_of.get(sid) == enemy:
                            shots_on_core += 1
                            if win_start < 0:
                                win_start = rnd
                        else:
                            shots_on_core_odd += 1
                elif unum == 13:                                # builderAttack
                    eid = tgt = None
                    for an, _aw, av in fields(ubuf):
                        if an == 1:
                            eid = av
                        elif an == 2:
                            tgt = read_pos(av)
                    if team_of.get(eid) == us:
                        attacked.add(eid)
                    if tgt is not None and tgt in FP:
                        batk_on_core += 1
                elif unum == 15:                                # builderHeal
                    eid = tgt = None
                    for hn, _hw, hv in fields(ubuf):
                        if hn == 1:
                            eid = hv
                        elif hn == 2:
                            tgt = read_pos(hv)
                    if team_of.get(eid) != us:
                        continue
                    healed.add(eid)
                    heal_any_ev += 1
                    V["tot_heal_ev"] = V.get("tot_heal_ev", 0) + 1
                    if tgt is not None and tgt in FP:
                        heal_core_ev += 1
                        healers.add(eid)
                elif unum == 16:                                # builderBuild
                    eid = None
                    for bn, _bw, bv in fields(ubuf):
                        if bn == 1:
                            eid = bv
                    if team_of.get(eid) == us:
                        built.add(eid)

        # ---- END-OF-ROUND snapshot ----
        end_pos = {b: pos_of[b] for b in bots[us] if b in pos_of}
        live1 = len(end_pos)
        seat1 = sum(1 for p in end_pos.values() if p in RING)
        fp1 = sum(1 for p in end_pos.values() if p in FP)

        # ---- IDLE classification (over builders ALIVE AT START) ----
        acted = healed | attacked | built
        busy = acted | moved | thrown
        idle = set()
        for b in start_pos:
            if b in busy or b in born:
                continue
            idle.add(b)
        n_idle_tled = len(idle & tled)

        # ---- SUPPLY tiers, from START positions ----
        ia = ib = ic = 0
        ia_s = ib_s = 0
        if idle:
            for b in idle:
                p = start_pos[b]
                if p in H_LOOSE:
                    ia += 1
                if p in H_STRICT:
                    ia_s += 1
            # BFS from each idle bot up to 3 cardinal steps
            for b in idle:
                p = start_pos[b]
                if p in H_LOOSE:
                    continue
                seen = {p}
                q = deque([(p, 0)])
                best = -1
                best_s = -1
                while q:
                    cur, dist = q.popleft()
                    if dist >= 3:
                        continue
                    for dx, dy in CARD:
                        nxt = (cur[0] + dx, cur[1] + dy)
                        if nxt in seen:
                            continue
                        seen.add(nxt)
                        if not standable(nxt, exclude_bot=b, loose=True):
                            continue
                        if best < 0 and nxt in H_LOOSE:
                            best = dist + 1
                        if best_s < 0 and nxt in H_STRICT and \
                                standable(nxt, exclude_bot=b, loose=False):
                            best_s = dist + 1
                        q.append((nxt, dist + 1))
                if best == 1:
                    ib += 1
                elif best in (2, 3):
                    ic += 1
                if best_s == 1:
                    ib_s += 1

        idle_adj_rm = 0
        if rm_own_bldg_tiles:
            for b in idle:
                p = start_pos[b]
                if any((p[0] + dx, p[1] + dy) in rm_own_bldg_tiles
                       for dx, dy in CARD):
                    idle_adj_rm += 1

        V["tot_heal_core"] += heal_core_ev
        V["tot_coreheal_hp"] += coreheal
        V["tot_coredmg"] += coredmg
        V["tot_builder_rounds"] += live0
        V["max_seat"] = max(V["max_seat"], seat1, seat0)
        V["max_fp"] = max(V["max_fp"], fp1, fp0)

        n_born_idle = sum(1 for b in born if b not in busy)
        seat_moved = seat_other = 0
        for b, p in start_pos.items():
            if p not in H_LOOSE:
                continue
            if b in moved or b in thrown:
                seat_moved += 1
            elif b in acted and b not in healers:
                seat_other += 1
        rows.append((path.name, rnd, core_hp[us], coredmg, coreheal,
                     shots_on_core, shots_on_core_odd, batk_on_core,
                     live0, live1,
                     len(healers), heal_core_ev, heal_any_ev,
                     seat0, fp0, seat1, fp1, free_loose, free_strict,
                     len(moved) + len(thrown), len(acted), len(built),
                     len(attacked), len(born), n_born_idle, len(died),
                     len(idle), n_idle_tled, len(idle & ran), len(ran),
                     ia, ib, ic, ia_s, ib_s, seat_moved, seat_other,
                     idle_adj_rm,
                     len(rm_own_bldg_tiles)))

        if core_death >= 0 and rnd >= core_death:
            break

    game = (path.name, us, len(turn_bufs), w, h, win_start, core_death,
            core_hp[us], V["tot_heal_core"], V["tot_coreheal_hp"],
            V["tot_coredmg"], V["tot_builder_rounds"], V["tot_botoutput"],
            V["tot_tled"], V["tot_crash"],
            ";".join(f"{k}:{v}" for k, v in sorted(acd_vals.items())),
            ";".join(f"{k}:{v}" for k, v in sorted(mcd_vals.items())),
            ";".join(f"{k}:{v}" for k, v in sorted(spawn_acd.items())),
            ";".join(f"{k}:{v}" for k, v in sorted(spawn_mcd.items())),
            V["max_seat"], V["max_fp"], V["bad_pos"], co_occ_rounds, n_bots)
    return rows, game


def work(args):
    p, ot = args
    try:
        r = decode(Path(p), ot)
    except Exception as exc:                                    # noqa: BLE001
        return ("ERR", str(p), repr(exc))
    if r is None:
        return ("ERR", str(p), "no map/cores")
    return ("OK", r)


def main(argv):
    outdir, joinp = argv[0], argv[1]
    J = {r["file"]: int(r["our_team"])
         for r in csv.DictReader(open(joinp), delimiter="\t")
         if r["our_team"] not in ("", "None")}
    files = argv[2:]
    if len(files) == 1 and files[0].startswith("@"):
        files = [x.strip() for x in open(files[0][1:]) if x.strip()]
    tasks = [(f, J[os.path.basename(f)]) for f in files
             if os.path.basename(f) in J]
    fr = open(os.path.join(outdir, "seat_rounds.tsv"), "w")
    fg = open(os.path.join(outdir, "seat_games.tsv"), "w")
    fr.write("\t".join(ROUND_COLS) + "\n")
    fg.write("\t".join(GAME_COLS) + "\n")
    bad = nrows = 0
    with Pool(8) as pool:
        for i, res in enumerate(pool.imap_unordered(work, tasks, chunksize=2)):
            if res[0] == "ERR":
                bad += 1
                print("ERR", res[1], res[2], file=sys.stderr)
                continue
            rows, game = res[1]
            for row in rows:
                fr.write("\t".join(str(v) for v in row) + "\n")
            nrows += len(rows)
            fg.write("\t".join(str(v) for v in game) + "\n")
            if (i + 1) % 100 == 0:
                print(f"  ...{i+1}/{len(tasks)} ({bad} err)", file=sys.stderr,
                      flush=True)
    fr.close()
    fg.close()
    print(f"done {len(tasks)} files, {bad} errors, {nrows} round rows",
          file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
