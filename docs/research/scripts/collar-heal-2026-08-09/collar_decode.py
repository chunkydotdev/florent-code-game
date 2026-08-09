#!/usr/bin/env python3
"""COLLAR decoder -- per-round core-collar staffing and core-heal rate, BOTH TEAMS.

DERIVED FROM `docs/research/scripts/seat-census-2026-08-09/seat_decode.py`
(itself derived from the preserved+validated `side-lane-2026-08-09/bb_decode.py`).
The event-decoding core is UNCHANGED -- same placeEntity/rotate guard, same
64-bit two's-complement HP varint (`s64`), same throw-vs-step rule, same
builderHeal (Update field 15) / builderAttack (13) / builderBuild (16) handling.

WHAT WAS CHANGED, and only this:

  1. `decode(path, side_team)` is run TWICE per replay -- once with side_team =
     our team index (from join.tsv) and once with the opponent's index.  Every
     "us"-relative quantity in the original decoder therefore becomes
     "this side"-relative.  Rows carry a `side` column, US or THEM.
  2. Loop truncation is now symmetric: the round loop stops when EITHER core is
     removed, so the US and THEM rows for a file cover the SAME rounds and are
     directly comparable.  (The original stopped only on our own core's death.)
  3. SEAT GEOMETRY is reported in three explicit flavours instead of one:
       ORTH8  -- the 8 tiles ORTHOGONALLY adjacent to the 2x2 footprint (2 per
                 side).  THIS IS THE PRIMARY DEFINITION: a builder bot's heal
                 requires an orthogonally adjacent tile, so these 8 tiles are
                 exactly the tiles from which the core can be healed.
       CHEB12 -- the 12-tile Chebyshev-1 ring (ORTH8 + the 4 diagonal corners).
                 Reported as a secondary OCCUPANCY number only; the 4 corners
                 cannot heal the core.
       FP     -- the 4 footprint tiles themselves (a bot standing on one of them
                 is also orthogonally adjacent to another footprint tile and so
                 could heal; in practice this essentially never happens).
     Wall/out-of-bounds tiles are excluded from the *free/standable* counts but
     the ring SIZE is reported per game so a truncated collar is visible.
  4. Occupancy is counted as DISTINCT SEATS occupied (a set of tiles), not as a
     count of bots, so co-occupation cannot inflate it.  Bot counts are kept
     alongside for cross-check.
  5. The idle-supply BFS of the original is OPTIONAL (`--bfs`), off by default:
     this question does not need it and it dominates runtime.

Usage:
    python collar_decode.py <outdir> <join.tsv> [--bfs] <replay...|@filelist>

Outputs (in <outdir>):
    collar_rounds.tsv  one row per (file, side, round)
    collar_games.tsv   one row per (file, side): geometry + validation totals
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
CO_OK = ("conveyor", "splitter", "core")
CARD = ((0, -1), (0, 1), (-1, 0), (1, 0))
CHEB = tuple((dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)
             if (dx, dy) != (0, 0))

DO_BFS = False


def s64(v):
    return v - (1 << 64) if v >= (1 << 63) else v


ROUND_COLS = [
    "file", "side", "rnd",
    "corehp", "coredmg", "coreheal",              # THIS side's core
    "shots_on_core", "batk_on_core",
    "live0", "live1",                             # this side's builders
    "healers", "heal_core_ev", "heal_any_ev",     # heals landing on own core
    "orth_seats0", "orth_bots0", "cheb_seats0", "fp0",   # start-of-round
    "orth_seats1", "cheb_seats1",                        # end-of-round
    "free_orth",                                  # free standable ORTH8 tiles
    "n_moved", "n_acted", "n_built", "n_atk", "n_born", "n_died",
    "n_idle", "n_ran",
    "ia", "ib",                                   # idle supply (only if --bfs)
    "seat_moved", "seat_other",
]

GAME_COLS = [
    "file", "side", "team_idx", "nr", "w", "h",
    "orth_n", "cheb_n", "core_death_own", "core_death_any", "core_hp_end",
    "tot_heal_core", "tot_coreheal_hp", "tot_coredmg", "tot_heal_any",
    "tot_builder_rounds", "tot_botoutput", "tot_tled", "tot_crash",
    "max_orth", "max_fp", "co_occ_rounds", "n_bots",
]


def decode(path: Path, side_team: int):
    """Decode one replay from the point of view of `side_team`."""
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
    if len(cores) != 2 or not (0 <= side_team <= 1):
        return None

    def is_wall(t):
        x, y = t
        return not (0 <= y < len(tiles) and 0 <= x < len(tiles[y])) or \
            tiles[y][x] == ENV_WALL

    corepos = {c["team"]: c["pos"] for c in cores}
    core_id = {c["team"]: c["id"] for c in cores}
    us, enemy = side_team, 1 - side_team

    footprint = {}
    for t, (cx, cy) in corepos.items():
        for dx in (0, 1):
            for dy in (0, 1):
                footprint[(cx + dx, cy + dy)] = t
    FP = {p for p, t in footprint.items() if t == us}

    # --- the three seat rings, built from the footprint directly -------------
    ORTH = set()          # 8 orthogonally-adjacent tiles (heal-capable)
    for (fx, fy) in FP:
        for dx, dy in CARD:
            p = (fx + dx, fy + dy)
            if p not in footprint and 0 <= p[0] < w and 0 <= p[1] < h \
                    and not is_wall(p):
                ORTH.add(p)
    CHEB12 = set()        # 12-tile Chebyshev-1 ring (ORTH8 + 4 corners)
    for (fx, fy) in FP:
        for dx, dy in CHEB:
            p = (fx + dx, fy + dy)
            if p not in footprint and 0 <= p[0] < w and 0 <= p[1] < h \
                    and not is_wall(p):
                CHEB12.add(p)
    H_LOOSE = ORTH | FP

    # --- live state ---------------------------------------------------------
    pos_of, team_of, kind_of = {}, {}, {}
    bot_at = {}
    bldg_at = {}
    bots = {0: set(), 1: set()}
    for c in cores:
        pos_of[c["id"]] = c["pos"]
        team_of[c["id"]] = c["team"]
        kind_of[c["id"]] = "core"
        for dx in (0, 1):
            for dy in (0, 1):
                bldg_at[(c["pos"][0] + dx, c["pos"][1] + dy)] = c["id"]

    core_hp = {0: 500, 1: 500}
    core_death_own = -1
    core_death_any = -1
    tot = dict.fromkeys(
        ("tot_heal_core", "tot_coreheal_hp", "tot_coredmg", "tot_heal_any",
         "tot_builder_rounds", "tot_botoutput", "tot_tled", "tot_crash",
         "max_orth", "max_fp"), 0)
    n_bots = 0
    co_occ_rounds = 0
    rows = []
    last_rnd = -1

    def standable(p, exclude_bot=None, loose=True):
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
        last_rnd = rnd
        start_pos = {b: pos_of[b] for b in bots[us] if b in pos_of}
        live0 = len(start_pos)
        occ_orth0 = {p for p in start_pos.values() if p in ORTH}
        orth_bots0 = sum(1 for p in start_pos.values() if p in ORTH)
        occ_cheb0 = {p for p in start_pos.values() if p in CHEB12}
        fp0 = sum(1 for p in start_pos.values() if p in FP)
        free_orth = sum(1 for p in ORTH if standable(p, loose=False))
        if any(len(s) > 1 for s in bot_at.values()):
            co_occ_rounds += 1

        moved, thrown, healed, attacked, built = set(), set(), set(), set(), set()
        ran, tled = set(), set()
        heal_core_ev = heal_any_ev = 0
        healers = set()
        coredmg = coreheal = 0
        shots_on_core = batk_on_core = 0
        born, died = set(), set()

        for _n, _w2, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:                                   # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        if e.id in pos_of:                      # rotate re-emit
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
                            if rv in (core_id.get(0), core_id.get(1)) \
                                    and core_death_any < 0:
                                core_death_any = rnd
                            if rv == core_id.get(us) and core_death_own < 0:
                                core_death_own = rnd
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
                        tot["tot_botoutput"] += 1
                        if tl:
                            tled.add(eid)
                            tot["tot_tled"] += 1
                        if out and b"Traceback" in out:
                            tot["tot_crash"] += 1
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

        end_pos = {b: pos_of[b] for b in bots[us] if b in pos_of}
        live1 = len(end_pos)
        occ_orth1 = {p for p in end_pos.values() if p in ORTH}
        occ_cheb1 = {p for p in end_pos.values() if p in CHEB12}
        fp1 = sum(1 for p in end_pos.values() if p in FP)

        acted = healed | attacked | built
        busy = acted | moved | thrown
        idle = {b for b in start_pos if b not in busy and b not in born}

        ia = ib = 0
        if DO_BFS and idle:
            for b in idle:
                if start_pos[b] in H_LOOSE:
                    ia += 1
            for b in idle:
                p = start_pos[b]
                if p in H_LOOSE:
                    continue
                seen = {p}
                q = deque([(p, 0)])
                best = -1
                while q:
                    cur, dist = q.popleft()
                    if dist >= 1:
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
                        q.append((nxt, dist + 1))
                if best == 1:
                    ib += 1

        seat_moved = seat_other = 0
        for b, p in start_pos.items():
            if p not in H_LOOSE:
                continue
            if b in moved or b in thrown:
                seat_moved += 1
            elif b in acted and b not in healers:
                seat_other += 1

        tot["tot_heal_core"] += heal_core_ev
        tot["tot_heal_any"] += heal_any_ev
        tot["tot_coreheal_hp"] += coreheal
        tot["tot_coredmg"] += coredmg
        tot["tot_builder_rounds"] += live0
        tot["max_orth"] = max(tot["max_orth"], len(occ_orth0), len(occ_orth1))
        tot["max_fp"] = max(tot["max_fp"], fp0, fp1)

        rows.append((path.name, "", rnd, core_hp[us], coredmg, coreheal,
                     shots_on_core, batk_on_core, live0, live1,
                     len(healers), heal_core_ev, heal_any_ev,
                     len(occ_orth0), orth_bots0, len(occ_cheb0), fp0,
                     len(occ_orth1), len(occ_cheb1), free_orth,
                     len(moved) + len(thrown), len(acted), len(built),
                     len(attacked), len(born), len(died),
                     len(idle), len(ran), ia, ib, seat_moved, seat_other))

        # SYMMETRIC truncation: stop as soon as EITHER core is gone, so the
        # US and THEM passes over the same file cover identical rounds.
        if core_death_any >= 0 and rnd >= core_death_any:
            break

    game = (path.name, "", us, last_rnd + 1, w, h, len(ORTH), len(CHEB12),
            core_death_own, core_death_any, core_hp[us],
            tot["tot_heal_core"], tot["tot_coreheal_hp"], tot["tot_coredmg"],
            tot["tot_heal_any"], tot["tot_builder_rounds"],
            tot["tot_botoutput"], tot["tot_tled"], tot["tot_crash"],
            tot["max_orth"], tot["max_fp"], co_occ_rounds, n_bots)
    return rows, game


def work(args):
    p, our_team = args
    out_rows, out_games = [], []
    for label, t in (("US", our_team), ("THEM", 1 - our_team)):
        try:
            r = decode(Path(p), t)
        except Exception as exc:                                # noqa: BLE001
            return ("ERR", str(p), f"{label}: {exc!r}")
        if r is None:
            return ("ERR", str(p), f"{label}: no map/cores")
        rows, game = r
        for row in rows:
            out_rows.append((row[0], label) + row[2:])
        out_games.append((game[0], label) + game[2:])
    return ("OK", out_rows, out_games)


def main(argv):
    global DO_BFS
    if "--bfs" in argv:
        DO_BFS = True
        argv = [a for a in argv if a != "--bfs"]
    outdir, joinp = argv[0], argv[1]
    J = {r["file"]: int(r["our_team"])
         for r in csv.DictReader(open(joinp), delimiter="\t")
         if r["our_team"] not in ("", "None")}
    files = argv[2:]
    if len(files) == 1 and files[0].startswith("@"):
        files = [x.strip() for x in open(files[0][1:]) if x.strip()]
    tasks = [(f, J[os.path.basename(f)]) for f in files
             if os.path.basename(f) in J]
    os.makedirs(outdir, exist_ok=True)
    fr = open(os.path.join(outdir, "collar_rounds.tsv"), "w")
    fg = open(os.path.join(outdir, "collar_games.tsv"), "w")
    fr.write("\t".join(ROUND_COLS) + "\n")
    fg.write("\t".join(GAME_COLS) + "\n")
    bad = nrows = 0
    with Pool(8) as pool:
        for i, res in enumerate(pool.imap_unordered(work, tasks, chunksize=2)):
            if res[0] == "ERR":
                bad += 1
                print("ERR", res[1], res[2], file=sys.stderr)
                continue
            for row in res[1]:
                fr.write("\t".join(str(v) for v in row) + "\n")
            nrows += len(res[1])
            for g in res[2]:
                fg.write("\t".join(str(v) for v in g) + "\n")
            if (i + 1) % 200 == 0:
                print(f"  ...{i+1}/{len(tasks)} ({bad} err)", file=sys.stderr,
                      flush=True)
    fr.close()
    fg.close()
    print(f"done {len(tasks)} files x2 sides, {bad} errors, {nrows} round rows",
          file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
