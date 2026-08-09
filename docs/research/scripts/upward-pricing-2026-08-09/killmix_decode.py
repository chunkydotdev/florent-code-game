#!/usr/bin/env python3
"""HOW CORES DIE -- per-file, per-VICTIM-side weapon mix on the core.

Event-decoding core is LIFTED UNCHANGED from
`docs/research/scripts/collar-heal-2026-08-09/collar_decode.py`:
same placeEntity/rotate guard (a build is the FIRST placeEntity for an id),
same 64-bit two's-complement HP varint (`s64`), same field numbers
(1 placeEntity, 2 moveBuilderBot, 3 removeEntity, 5 updateHp, 12 fireTurret,
13 builderAttack, 15 builderHeal).

For each replay we emit ONE ROW PER SIDE, that side being the VICTIM: the side
whose 2x2 core footprint is being shot at.  Columns:

  death_rnd     round this side's core was removed (-1 if it survived)
  coredmg       observed HP lost by this core (sum of negative updateHp)
  coreheal      observed HP gained
  sh_gunner/sh_sentinel/sh_other   enemy fireTurret events landing on the
                                   footprint, split by the SHOOTER's entity kind
                                   (looked up from the building standing on the
                                   `frm` tile)
  batk          enemy builderAttack events targeting the footprint
  pred_dmg      7*gunner + 18*sentinel + 2*batk  -- the rules arithmetic
  *_l100        same four counters restricted to the last 100 rounds before the
                core died (0 if it never died)

`pred_dmg` vs `coredmg` is the internal validation: if the weapon attribution is
right they must track each other.  An exact zero anywhere is a bug signature.

Usage: python killmix_decode.py <out.tsv> @<filelist>
"""
from __future__ import annotations

import os
import sys
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import fields, read_pos, parse_entity, packed_varints, WIRE_LEN  # noqa: E402

ENV_WALL = 1
GUN_DMG, SEN_DMG, BATK_DMG = 7, 18, 2
COLS = ["file", "victim_idx", "nr", "death_rnd", "coredmg", "coreheal",
        "sh_gunner", "sh_sentinel", "sh_other", "batk", "pred_dmg",
        "sh_gunner_l100", "sh_sentinel_l100", "sh_other_l100", "batk_l100",
        "n_gunner_enemy", "n_sentinel_enemy", "n_launcher_enemy"]


def s64(v):
    return v - (1 << 64) if v >= (1 << 63) else v


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
    tiles, cores = [], []
    for num, wire, value in fields(map_buf):
        if num == 3:
            row = []
            for rnum, rwire, rvalue in fields(value):
                if rnum == 1:
                    row.extend(packed_varints(rvalue) if rwire == WIRE_LEN else [rvalue])
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
    if len(cores) != 2:
        return None

    corepos = {c["team"]: c["pos"] for c in cores}
    core_id = {c["team"]: c["id"] for c in cores}
    FP = {}
    for t, (cx, cy) in corepos.items():
        FP[t] = {(cx + dx, cy + dy) for dx in (0, 1) for dy in (0, 1)}
    owner_of_tile = {}
    for t, s in FP.items():
        for p in s:
            owner_of_tile[p] = t

    pos_of, team_of, kind_of = {}, {}, {}
    bldg_at = {}
    for c in cores:
        pos_of[c["id"]] = c["pos"]
        team_of[c["id"]] = c["team"]
        kind_of[c["id"]] = "core"
        for p in FP[c["team"]]:
            bldg_at[p] = c["id"]

    # per victim-team accumulators
    acc = {t: dict.fromkeys(
        ("coredmg", "coreheal", "sh_gunner", "sh_sentinel", "sh_other", "batk"), 0)
        for t in (0, 1)}
    # per-round event log for the trailing-100 window
    per_round = {0: [], 1: []}          # (rnd, key)
    death = {0: -1, 1: -1}
    built_turrets = {0: {"gunner": 0, "sentinel": 0, "launcher": 0},
                     1: {"gunner": 0, "sentinel": 0, "launcher": 0}}
    last_rnd = -1

    for rnd, turn_buf in enumerate(turn_bufs):
        last_rnd = rnd
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
                                if kind_of[e.id] != "builder_bot":
                                    if bldg_at.get(old) == e.id:
                                        del bldg_at[old]
                                    bldg_at[e.pos] = e.id
                                pos_of[e.id] = e.pos
                            continue
                        pos_of[e.id] = e.pos
                        team_of[e.id] = e.team
                        kind_of[e.id] = e.kind
                        if e.kind != "builder_bot":
                            bldg_at[e.pos] = e.id
                        if e.kind in ("gunner", "sentinel", "launcher"):
                            built_turrets[e.team][e.kind] += 1
                elif unum == 2:                                 # moveBuilderBot
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid in pos_of and to:
                        pos_of[eid] = to
                elif unum == 3:                                 # removeEntity
                    for _rn, _rw, rv in fields(ubuf):
                        if rv not in pos_of:
                            continue
                        p = pos_of.pop(rv)
                        if kind_of.get(rv) != "builder_bot":
                            if bldg_at.get(p) == rv:
                                del bldg_at[p]
                            for t in (0, 1):
                                if rv == core_id.get(t) and death[t] < 0:
                                    death[t] = rnd
                elif unum == 5:                                 # updateHp
                    eid, delta = None, 0
                    for hn, _hw, hv in fields(ubuf):
                        if hn == 1:
                            eid = hv
                        elif hn == 2:
                            delta = s64(hv)
                    for t in (0, 1):
                        if eid == core_id.get(t):
                            if delta < 0:
                                acc[t]["coredmg"] += -delta
                            else:
                                acc[t]["coreheal"] += delta
                elif unum == 12:                                # fireTurret
                    frm = to = None
                    for fn, _fw, fv in fields(ubuf):
                        if fn == 1:
                            frm = read_pos(fv)
                        elif fn == 2:
                            to = read_pos(fv)
                    vt = owner_of_tile.get(to) if to is not None else None
                    if vt is None:
                        continue
                    sid = bldg_at.get(frm) if frm is not None else None
                    if team_of.get(sid) == vt:            # friendly fire on own FP
                        continue
                    k = kind_of.get(sid)
                    key = ("sh_gunner" if k == "gunner" else
                           "sh_sentinel" if k == "sentinel" else "sh_other")
                    acc[vt][key] += 1
                    per_round[vt].append((rnd, key))
                elif unum == 13:                                # builderAttack
                    eid = tgt = None
                    for an, _aw, av in fields(ubuf):
                        if an == 1:
                            eid = av
                        elif an == 2:
                            tgt = read_pos(av)
                    vt = owner_of_tile.get(tgt) if tgt is not None else None
                    if vt is None or team_of.get(eid) == vt:
                        continue
                    acc[vt]["batk"] += 1
                    per_round[vt].append((rnd, "batk"))
        if death[0] >= 0 or death[1] >= 0:
            break

    out = []
    for t in (0, 1):
        a = acc[t]
        pred = GUN_DMG * a["sh_gunner"] + SEN_DMG * a["sh_sentinel"] + BATK_DMG * a["batk"]
        l = dict.fromkeys(("sh_gunner", "sh_sentinel", "sh_other", "batk"), 0)
        if death[t] >= 0:
            lo = death[t] - 100
            for rnd, key in per_round[t]:
                if rnd >= lo:
                    l[key] += 1
        e = 1 - t
        out.append((path.name, t, last_rnd + 1, death[t], a["coredmg"], a["coreheal"],
                    a["sh_gunner"], a["sh_sentinel"], a["sh_other"], a["batk"], pred,
                    l["sh_gunner"], l["sh_sentinel"], l["sh_other"], l["batk"],
                    built_turrets[e]["gunner"], built_turrets[e]["sentinel"],
                    built_turrets[e]["launcher"]))
    return out


def work(p):
    try:
        r = decode(Path(p))
    except Exception as exc:                                    # noqa: BLE001
        return ("ERR", str(p), repr(exc))
    if r is None:
        return ("ERR", str(p), "no map/cores")
    return ("OK", r)


def main(argv):
    outp = argv[0]
    files = argv[1:]
    if len(files) == 1 and files[0].startswith("@"):
        files = [x.strip() for x in open(files[0][1:]) if x.strip()]
    bad = n = 0
    with open(outp, "w") as fh:
        fh.write("\t".join(COLS) + "\n")
        with Pool(8) as pool:
            for i, res in enumerate(pool.imap_unordered(work, files, chunksize=8)):
                if res[0] == "ERR":
                    bad += 1
                    print("ERR", res[1], res[2], file=sys.stderr)
                    continue
                for row in res[1]:
                    fh.write("\t".join(str(v) for v in row) + "\n")
                    n += 1
                if (i + 1) % 500 == 0:
                    print(f"  ...{i+1}/{len(files)} ({bad} err)", file=sys.stderr, flush=True)
    print(f"done {len(files)} files, {bad} errors, {n} rows -> {outp}", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
